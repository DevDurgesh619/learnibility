"""Cambridge IGCSE Mathematics 0580 Extended (2025-27), coursebook chapters 13-24 (grade 10).

Chapter order in the curriculum file (1-12) maps to coursebook chapters 13-24:
measurement; equations and inequalities; bearings and trigonometry; scatter diagrams; money;
curved graphs; symmetry; histograms and cumulative frequency; ratio, rate and proportion;
functions; transformations and vectors; tree and Venn probability.
"""
import math
import re
from fractions import Fraction as Fr
from ._lib import topic, mcq, compose, sf, person, two_people, city, num_mcq, fmt, sup

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.25, 1.25)}, 'wordy': False}
CHAPTERS = {}
MINUS = '−'


# ------------------------------------------------------------------ formatting helpers

def num(x, dp=2):
    """Number with unicode minus, no trailing zeros; exact fractions shown as a/b."""
    if isinstance(x, Fr):
        if x.denominator == 1:
            return num(int(x))
        return (MINUS if x < 0 else '') + f'{abs(x.numerator)}/{x.denominator}'
    if isinstance(x, float) and abs(x - round(x)) < 1e-9:
        x = int(round(x))
    if isinstance(x, int):
        s = f'{abs(x):,}' if abs(x) >= 10000 else str(abs(x))
        return (MINUS if x < 0 else '') + s
    s = fmt(abs(x), dp)
    if s == '0':
        return '0'
    return (MINUS if x < 0 else '') + s


def n3(x):
    """3 significant figures (Cambridge default for inexact answers), unicode minus."""
    if abs(x) < 1e-12:
        return '0'
    s = sf(abs(x), 3)
    return (MINUS if x < 0 else '') + s


def money(x, cur='$'):
    return f'{cur}{x:,.2f}'


def term_str(c, v):
    """A single term with coefficient c and variable string v (v='' for constant)."""
    c = Fr(c) if not isinstance(c, Fr) else c
    if v == '':
        return num(abs(c))
    if abs(c) == 1:
        return v
    return num(abs(c)) + v


def expr(*terms):
    """expr((3, 'x²'), (-2, 'x'), (5, '')) -> '3x² − 2x + 5'."""
    out = ''
    for c, v in terms:
        if c == 0:
            continue
        t = term_str(c, v)
        if not out:
            out = (MINUS if c < 0 else '') + t
        else:
            out += (' − ' if c < 0 else ' + ') + t
    return out or '0'


def lin(a, b, v='x'):
    return expr((a, v), (b, ''))


def quad(a, b, c, v='x'):
    return expr((a, v + '²'), (b, v), (c, ''))


def bracket(p, v='x'):
    """(x + p) form."""
    return f'({v} + {p})' if p > 0 else (f'({v} − {-p})' if p < 0 else v)


def frac(x):
    x = Fr(x)
    return num(x)


def sgn(x):
    """' + 3' or ' − 3' for appending a constant."""
    return f' + {num(x)}' if x >= 0 else f' − {num(-x)}'


def nn(x):
    """3 s.f. without padding zeros (1.00 -> 1, 42.0 -> 42)."""
    return ex(float(n3(x).replace(MINUS, '-')))


def lq(m, c):
    """'mx + c' for a line equation, 3 s.f., tidy signs and zero/unit terms."""
    ms = nn(m)
    ms = '' if ms == '1' else (MINUS if ms == MINUS + '1' else ms)
    cv = float(n3(c).replace(MINUS, '-'))
    return f'{ms}x' + ('' if cv == 0 else sgn(cv if cv != int(cv) else int(cv)))


_DUPEQ = re.compile(r'(?<![\d.])(\d+/\d+) = \1(?![\d/])')


def _dd(t):
    return _DUPEQ.sub(r'\1', t) if isinstance(t, str) else t


def Q(stem, answer, key, **kw):
    d = {'stem': stem, 'answer': _dd(answer), 'key': _dd(key)}
    d.update(kw)
    return d


def MC(r, stem, correct, distractors, key, fmtf=None, unit=''):
    """Numeric MCQ: correct value and wrong values; formats with num() unless fmtf given."""
    f = fmtf or num
    opts, ans = num_mcq(r, correct, distractors, fmtf=f, unit=unit)
    return {'stem': stem, 'options': opts, 'answer': ans, 'key': key}


def SMC(r, stem, correct, distractors, key):
    opts, ans = mcq(r, correct, distractors)
    return {'stem': stem, 'options': opts, 'answer': ans, 'key': key}


def P(text, ans, key, m):
    """A compose part; m = part marks."""
    return lambda r: (text, _dd(ans), _dd(f'{key} [{m}]'))


def cmp_(r, intro, parts, k=(2, 3, 4)):
    return compose(r, intro, parts, k=k, type_='multi_step')


def ctx_name(r):
    return person(r)


def deg(x, dp=1):
    return f'{x:.{dp}f}°'


TRY = 'Show your working.'


def ex(x, dp=6):
    """Exact decimal formatting (up to dp places), commas for large numbers, unicode minus."""
    if isinstance(x, float) and abs(x - round(x)) < 1e-9:
        x = int(round(x))
    if isinstance(x, int):
        return (MINUS if x < 0 else '') + (f'{abs(x):,}' if abs(x) >= 10000 else str(abs(x)))
    s = f'{abs(x):{"," if abs(x) >= 10000 else ""}.{dp}f}'.rstrip('0').rstrip('.')
    return (MINUS if x < 0 else '') + s


def hm(mins):
    """Minutes past midnight -> 'HH:MM' (24-hour clock)."""
    mins %= 1440
    return f'{mins // 60:02d}:{mins % 60:02d}'


def h12(mins):
    mins %= 1440
    h, m = divmod(mins, 60)
    suf = 'am' if h < 12 else 'pm'
    hh = h % 12 or 12
    return f'{hh}:{m:02d} {suf}'


def dur(mins):
    h, m = divmod(mins, 60)
    if h and m:
        return f'{h} h {m} min'
    return f'{h} h' if h else f'{m} min'


def an(n):
    s = str(n)
    return ('an ' if s[0] == '8' or s[:2] in ('11', '18') else 'a ') + s


def art(w):
    return ('an ' if w[0].lower() in 'aeiou' else 'a ') + w


# =========================================================== 1 Understanding measurement (Ch 13)
m1 = topic('Units of measurement and converting units', 'units of measurement', 'converting units of length, area, volume and capacity', 'converting units')
m1.fixed('C1', (1, 2), [
    ('How many square centimetres are there in 1 square metre?', '10 000 cm²', '1 m = 100 cm, so 1 m² = 100 × 100 = 10 000 cm².', ['100 cm²', '1000 cm²', '1 000 000 cm²']),
    ('How many cubic centimetres are there in 1 litre?', '1000 cm³', '1 litre = 1000 ml = 1000 cm³.', ['100 cm³', '10 cm³', '10 000 cm³']),
    ('1 m³ is equal to how many litres?', '1000 litres', '1 m³ = 1 000 000 cm³ = 1 000 000 ÷ 1000 = 1000 litres.', ['100 litres', '10 litres', '1 000 000 litres']),
    ('How many square metres are there in 1 km²?', '1 000 000 m²', '1 km = 1000 m, so 1 km² = 1000 × 1000 = 1 000 000 m².', ['1000 m²', '10 000 m²', '100 000 m²']),
    ('Which unit is the most suitable for measuring the capacity of a teaspoon?', 'millilitres', 'A teaspoon holds about 5 ml; litres and cubic metres are far too large.', ['litres', 'cubic metres', 'kilograms']),
    ('How many cubic millimetres are there in 1 cm³?', '1000 mm³', '1 cm = 10 mm, so 1 cm³ = 10 × 10 × 10 = 1000 mm³.', ['10 mm³', '100 mm³', '10 000 mm³']),
    ('Write down the number of millilitres equal to 1 cm³.', '1 ml', '1 cm³ = 1 ml by definition of the litre (1 litre = 1000 cm³ = 1000 ml).', ['10 ml', '100 ml', '1000 ml']),
    ('Which of these is a unit of area?', 'hectare', 'A hectare is 10 000 m²; the others measure length, volume and mass.', ['kilometre', 'litre', 'tonne']),
])
m1.fixed('C2', (2, 3), [
    ('Explain why 1 m² is not equal to 100 cm².', '1 m² is a square 100 cm by 100 cm, so its area is 100 × 100 = 10 000 cm².', 'B1 uses 1 m = 100 cm for both dimensions; B1 conclusion 10 000 cm² [2]'),
    ('Explain why the conversion factor from m³ to cm³ is 1 000 000 and not 100.', 'A cube of side 1 m is 100 cm × 100 cm × 100 cm = 1 000 000 cm³: the length factor 100 is cubed for volume.', 'B1 three dimensions each × 100; B1 100³ = 1 000 000 [2]'),
    ('Explain why the same area has a larger number when measured in mm² than when measured in cm².', 'Each cm² contains 10 × 10 = 100 mm², so the number of (smaller) units needed is 100 times larger.', 'B1 1 cm² = 100 mm²; B1 smaller unit so more of them [2]'),
    ('A carton is labelled 1.5 litres. Explain how you know its capacity is 1500 cm³.', '1 litre = 1000 cm³, so 1.5 litres = 1.5 × 1000 = 1500 cm³.', 'B1 1 litre = 1000 cm³; B1 × 1.5 [2]'),
    ('Describe how to convert an area in cm² to an area in m².', 'Divide by 10 000, because 1 m² = 100 cm × 100 cm = 10 000 cm².', 'B1 divide (not multiply); B1 by 10 000 with reason [2]'),
])

CONV = [('m', 'cm', 100, 'length'), ('km', 'm', 1000, 'length'), ('cm', 'mm', 10, 'length'), ('m²', 'cm²', 10 ** 4, 'area'),
        ('cm²', 'mm²', 100, 'area'), ('km²', 'm²', 10 ** 6, 'area'), ('m³', 'cm³', 10 ** 6, 'volume'), ('cm³', 'mm³', 1000, 'volume'),
        ('litres', 'ml', 1000, 'capacity'), ('m³', 'litres', 1000, 'capacity')]


@m1.add('C1', (1, 2, 3))
def m1_conv(r, D):
    big, small, f, kind = r.choice(CONV)
    lin = {'length': f, 'area': round(f ** 0.5), 'volume': round(f ** (1 / 3)), 'capacity': 10}[kind]
    v = r.choice([2, 3, 4, 5, 6, 8, 12, 15, 25]) if D == 1 else r.choice([0.4, 0.75, 1.2, 2.5, 3.6, 4.8, 7.25, 0.06])
    if r.random() < 0.5:
        stem = f'Convert {ex(v)} {big} to {small}.'
        c = v * f
        ds = [v * lin if lin != f else v * f * 10, v * f / 10, v / f, v * f * 10]
        key = f'1 {big} = {ex(f)} {small}, so multiply: {ex(v)} × {ex(f)} = {ex(c)} {small}.'
    else:
        w = v * f
        stem = f'Convert {ex(w)} {small} to {big}.'
        c = v
        ds = [w / lin if lin != f else w / (f * 10), w / (f / 10), w * f, w / (f * 10)]
        key = f'1 {big} = {ex(f)} {small}, so divide: {ex(w)} ÷ {ex(f)} = {ex(c)} {big}.'
    unit = ' ' + (small if 'to ' + small in stem else big)
    return MC(r, stem, c, ds, key, fmtf=ex, unit=unit)


@m1.add('C2', (2, 3, 4), 'explain')
def m1_err(r, D):
    nm = person(r)
    case = r.choice(['area', 'volume', 'cap'])
    if case == 'area':
        v = r.choice([2.5, 3.4, 0.8, 6, 12, 4.75, 1.6])
        a, b, f, wrongf = r.choice([('m²', 'cm²', 10 ** 4, 100), ('cm²', 'mm²', 100, 10), ('km²', 'm²', 10 ** 6, 1000)])
    elif case == 'volume':
        v = r.choice([0.6, 1.25, 2.4, 3, 5, 0.35, 7.5])
        a, b, f, wrongf = r.choice([('m³', 'cm³', 10 ** 6, 100), ('cm³', 'mm³', 1000, 10)])
    else:
        v = r.choice([0.45, 1.8, 2.25, 3.2, 6.5, 0.9])
        a, b, f, wrongf = ('m³', 'litres', 1000, 100)
    stem = f'{nm} converts {ex(v)} {a} to {b} by multiplying by {ex(wrongf)} and gets {ex(v * wrongf)} {b}. Explain the mistake and give the correct answer.'
    why = {('m²', 'cm²'): '1 m² = 100 cm × 100 cm = 10 000 cm²', ('cm²', 'mm²'): '1 cm² = 10 mm × 10 mm = 100 mm²', ('km²', 'm²'): '1 km² = 1000 m × 1000 m = 1 000 000 m²',
           ('m³', 'cm³'): '1 m³ = 100 × 100 × 100 = 1 000 000 cm³', ('cm³', 'mm³'): '1 cm³ = 10 × 10 × 10 = 1000 mm³', ('m³', 'litres'): '1 m³ = 1 000 000 cm³ = 1000 litres'}[(a, b)]
    return Q(stem, f'{nm} used a length (or wrong) factor; {why}, so the answer is {ex(v * f)} {b}.',
             f'B1 identifies the wrong conversion factor ({why}); B1 correct answer {ex(v * f)} {b} [2]')


@m1.add('C3', (1, 2, 3, 4))
def m1_tank(r, D):
    nm = person(r)
    if D <= 2:
        l, w, h = r.choice([40, 50, 60, 80]), r.choice([20, 25, 30, 40]), r.choice([20, 25, 30, 35])
        V = l * w * h
        stem = f'{nm} has a fish tank in the shape of a cuboid measuring {l} cm by {w} cm by {h} cm. Calculate the capacity of the tank in litres.'
        return Q(stem, f'{ex(V / 1000)} litres', f'M1 V = {l} × {w} × {h} = {ex(V)} cm³; A1 ÷ 1000 = {ex(V / 1000)} litres.')
    l, w, h = r.choice([1.2, 1.5, 2.4, 0.8]), r.choice([0.6, 0.75, 0.9, 1.1]), r.choice([0.5, 0.45, 0.8, 1.25])
    V = l * w * h
    pct = r.choice([60, 75, 80, 90])
    if D == 3:
        stem = f'A water trough in a farm near {city(r)} is a cuboid {ex(l)} m long, {ex(w)} m wide and {ex(h)} m deep. Calculate its capacity in litres.'
        return Q(stem, f'{ex(V * 1000, 3)} litres', f'M1 V = {ex(l)} × {ex(w)} × {ex(h)} = {ex(V, 4)} m³; M1 × 1000; A1 {ex(V * 1000, 3)} litres.')
    b = r.choice([8, 10, 12, 15])
    full = V * 1000 * pct / 100
    n = math.ceil(full / b - 1e-9)
    stem = f'A water trough near {city(r)} is a cuboid {ex(l)} m long, {ex(w)} m wide and {ex(h)} m deep. {nm} fills it to {pct}% of its depth using a bucket that holds {b} litres. Calculate the least number of full buckets {nm} must pour in to reach this level.'
    return Q(stem, f'{n} buckets', f'M1 V = {ex(V, 4)} m³ = {ex(V * 1000, 3)} litres; M1 × {pct}% = {ex(full, 3)} litres; M1 ÷ {b} = {ex(full / b, 3)}; A1 round up to {n}.')


@m1.add('C3', (2, 3, 4))
def m1_tiles(r, D):
    t1, t2 = r.choice([(20, 20), (25, 25), (30, 30), (40, 40), (50, 50), (25, 50), (30, 60), (40, 20)])
    k1, k2 = r.randint(8, 18), r.randint(6, 14)
    L, W = t1 * k1 / 100, t2 * k2 / 100
    n = k1 * k2
    room = r.choice(['kitchen floor', 'patio', 'bathroom wall', 'classroom floor', 'hotel lobby floor'])
    if D <= 2:
        stem = f'A rectangular {room} measures {ex(L)} m by {ex(W)} m. Calculate its area in cm².'
        return Q(stem, f'{ex(L * W * 10000)} cm²', f'M1 {ex(L * 100)} × {ex(W * 100)} or {ex(L * W, 4)} × 10 000; A1 {ex(L * W * 10000)} cm².')
    stem = f'A rectangular {room} in {city(r)} measures {ex(L)} m by {ex(W)} m. It is covered with rectangular tiles measuring {t1} cm by {t2} cm with no gaps. Calculate the number of tiles needed.'
    key = f'M1 {ex(L * 100)} ÷ {t1} = {k1} and {ex(W * 100)} ÷ {t2} = {k2} (or area {ex(L * W * 10000)} cm² ÷ {t1 * t2} cm²); A1 {n}.'
    if D >= 4:
        price = r.choice([12, 15, 18, 24])
        box = r.choice([10, 12, 20, 25])
        boxes = math.ceil(n / box)
        stem += f' Tiles are sold in boxes of {box} for ${price} a box. Calculate the cost of the tiles.'
        return Q(stem, f'{n} tiles; {boxes} boxes cost ${boxes * price}', key + f' M1 {n} ÷ {box} = {ex(n / box, 2)} → {boxes} boxes; A1 ${boxes * price}.')
    return Q(stem, f'{n} tiles', key)


@m1.add('C3', (2, 3))
def m1_stdform(r, D):
    m = r.choice([1.2, 2.5, 3.4, 4.8, 6.5, 7.2, 9.1])
    a, b, f, e = r.choice([('km²', 'm²', 10 ** 6, 6), ('m³', 'cm³', 10 ** 6, 6), ('m²', 'mm²', 10 ** 6, 6), ('km', 'cm', 10 ** 5, 5), ('m³', 'mm³', 10 ** 9, 9)])
    return Q(f'Convert {ex(m)} {a} to {b}, giving your answer in standard form.', f'{ex(m)} × 10{sup(e)} {b}',
             f'B1 1 {a} = 10{sup(e)} {b}; B1 {ex(m)} × 10{sup(e)} {b}.')


def m1_c4(r, D):
    kind = r.choice(['pool', 'tank', 'pond'])
    if kind == 'pool':
        L, W, d = r.choice([8, 10, 12, 15, 20, 25]), r.choice([4, 5, 6, 8, 10]), r.choice([1.2, 1.5, 1.8, 2])
        intro = f'A swimming pool in {city(r)} is a cuboid {L} m long and {W} m wide with a constant depth of {ex(d)} m.'
    elif kind == 'tank':
        L, W, d = r.choice([2.5, 3, 4]), r.choice([1.5, 2, 2.5]), r.choice([1.2, 1.6, 2])
        intro = f'A rainwater tank on a school roof in {city(r)} is a cuboid {ex(L)} m by {ex(W)} m by {ex(d)} m high.'
    else:
        L, W, d = r.choice([3, 4, 5, 6]), r.choice([2, 2.5, 3]), r.choice([0.6, 0.75, 0.8, 1])
        intro = f'An ornamental pond in a park in {city(r)} is a cuboid {L} m long, {ex(W)} m wide and {ex(d)} m deep.'
    V = L * W * d
    lit = V * 1000
    R = r.choice([150, 200, 250, 400, 500, 600])
    mins = lit / R
    mm = round(mins)
    parts = [
        P('Calculate the volume in m³.', f'{ex(V, 4)} m³', f'M1 {ex(L)} × {ex(W)} × {ex(d)}; A1 {ex(V, 4)} m³', 2),
        P('Write down the capacity in litres.', f'{ex(lit, 2)} litres', f'B1 × 1000 = {ex(lit, 2)} litres', 1),
        P(f'Water flows in at {R} litres per minute. Calculate the time taken to fill it from empty, in hours and minutes (to the nearest minute).', dur(mm),
          f'M1 {ex(lit, 2)} ÷ {R} = {ex(mins, 2)} minutes; M1 ÷ 60 for hours; A1 {dur(mm)}', 3),
        P('Calculate the area of the base in cm².', f'{ex(L * W * 10000)} cm²', f'M1 {ex(L * W, 4)} m² × 10 000; A1 {ex(L * W * 10000)} cm²', 2),
        P('Explain why the number of litres is 1000 times the number of m³.', '1 m³ = 100 × 100 × 100 cm³ = 1 000 000 cm³ and 1 litre = 1000 cm³, so 1 m³ = 1000 litres.', 'B1 1 m³ = 10⁶ cm³; B1 ÷ 1000 cm³ per litre', 2),
    ]
    return cmp_(r, intro, parts)


m1.add('C4', (2, 3, 4, 5))(m1_c4)

# ---------------------------------------------------------------- time
m2 = topic('Time: 12- and 24-hour clock and timetables', 'time', '12- and 24-hour clock', 'timetables')
m2.fixed('C1', (1, 2), [
    ('Write 4:35 pm using the 24-hour clock.', '16:35', 'pm times after 1 pm: add 12 to the hours, 4 + 12 = 16.', ['04:35', '14:35', '16:53']),
    ('Write 00:20 using the 12-hour clock.', '12:20 am', '00:xx is in the hour after midnight, written 12:xx am', ['12:20 pm', '0:20 pm', '10:20 am']),
    ('How many minutes are there in 2.25 hours?', '135 minutes', '2.25 × 60 = 135 minutes.', ['225 minutes', '125 minutes', '145 minutes']),
    ('Write 3 hours 45 minutes as a decimal number of hours.', '3.75 hours', '45 minutes = 45/60 = 0.75 hour.', ['3.45 hours', '3.34 hours', '3.65 hours']),
    ('How many seconds are there in 1 hour?', '3600', '60 × 60 = 3600 seconds.', ['360', '6000', '60']),
    ('Which 24-hour clock time is the same as midnight?', '00:00', 'Midnight is 00:00 (the start of a new day); 12:00 is midday.', ['12:00', '24:01', '01:00']),
])
m2.fixed('C2', (2, 3), [
    ('Kenji says 2.5 hours is 2 hours 50 minutes. Explain his mistake.', '0.5 hours is half of 60 minutes, which is 30 minutes, so 2.5 hours = 2 hours 30 minutes.', 'B1 0.5 h = 30 min (not 50); B1 2 h 30 min [2]'),
    ('Explain why you cannot find the time from 09:45 to 11:20 by working out 11.20 − 9.45.', 'An hour has 60 minutes, not 100, so times do not subtract like decimals. The correct duration is 1 h 35 min, not 1.75.', 'B1 60 minutes in an hour; B1 correct duration 1 h 35 min [2]'),
    ('Explain why bus, train and flight timetables use the 24-hour clock.', 'Every time of day has a unique four-digit form, so there is no confusion between am and pm', 'B1 avoids am/pm ambiguity; B1 each time unique [2]'),
    ('Describe how to convert a time given in decimal hours, such as 1.4 hours, into hours and minutes.', 'Keep the whole hours and multiply the decimal part by 60: 0.4 × 60 = 24, so 1.4 hours = 1 h 24 min.', 'B1 multiply decimal part by 60; B1 correct example [2]'),
])


@m2.add('C1', (1, 2, 3))
def m2_conv(r, D):
    t = r.randint(0, 1439)
    m = t % 60
    h = t // 60
    if r.random() < 0.5:
        c = hm(t)
        wrong = [f'{(h + 12) % 24:02d}:{m:02d}', f'{(h % 12 or 12):02d}:{m:02d}', f'{h:02d}:{(m + 10) % 60:02d}', f'{(h + 1) % 24:02d}:{m:02d}', f'{(h + 2) % 24:02d}:{m:02d}']
        return SMC(r, f'Write {h12(t)} using the 24-hour clock.', c, wrong, f'{h12(t)} = {c} ({"add 12 to pm hours from 1 pm" if h >= 13 else ("12 am hour is 00" if h == 0 else "am/12 noon hours keep their value")}).')
    c = h12(t)
    other = 'pm' if h < 12 else 'am'
    wrong = [f'{(h % 12 or 12)}:{m:02d} {other}', f'{(h % 12 or 12) + 1 if (h % 12 or 12) < 12 else 1}:{m:02d} {c.split()[1]}', f'{h}:{m:02d} {other}', f'{(h + 2) % 12 or 12}:{m:02d} {c.split()[1]}']
    return SMC(r, f'Write {hm(t)} using the 12-hour clock.', c, wrong, f'{hm(t)} = {c}')


@m2.add('C2', (2, 3, 4), 'explain')
def m2_err(r, D):
    nm = person(r)
    h1 = r.randint(6, 15)
    m1_ = r.choice([35, 40, 45, 50, 55])
    h2 = h1 + r.randint(1, 4)
    m2_ = r.choice([5, 10, 15, 20, 25])
    t1, t2 = h1 * 60 + m1_, h2 * 60 + m2_
    wrong = round((h2 + m2_ / 100) - (h1 + m1_ / 100), 2)
    return Q(f'{nm} wants the length of a journey from {hm(t1)} to {hm(t2)}. {nm} works out {h2}.{m2_:02d} − {h1}.{m1_:02d} = {wrong:.2f} and says the journey takes {int(wrong)} hours {round((wrong - int(wrong)) * 100)} minutes. Explain why this is wrong and find the correct time taken.',
             f'There are 60 minutes, not 100, in an hour, so times cannot be subtracted as decimals. Correct duration: {dur(t2 - t1)}.',
             f'B1 explains base 60 not 100; B1 {dur(t2 - t1)} (e.g. {hm(t1)} → {hm((h1 + 1) * 60)} is {60 - m1_} min, then to {hm(t2)}) [2]')


@m2.add('C3', (1, 2, 3, 4))
def m2_dur(r, D):
    nm = person(r)
    t1 = r.randint(5 * 12, 22 * 12) * 5
    d = r.randint(7, 60) * 5 if D <= 2 else r.randint(30, 160) * 5
    t2 = t1 + d
    what = r.choice(['a film', 'a bus journey', 'a football tournament', 'a ferry crossing', 'a school trip', 'a night flight'])
    if D == 1:
        return MC(r, f'{what.capitalize()} starts at {hm(t1)} and ends at {hm(t2)}. How long does it last?', d, [d + 40, d - 40 if d > 40 else d + 100, d + 60, d + 20],
                  f'From {hm(t1)} to {hm(t2)} is {dur(d)}.', fmtf=lambda x: dur(int(x)))
    stem = f'{nm} records that {what} started at {h12(t1)} and finished at {hm(t2)}{" the next day" if t2 >= 1440 else ""}. Calculate how long it lasted, in hours and minutes.'
    return Q(stem, dur(d), f'M1 converts to the same clock ({h12(t1)} = {hm(t1)}) and counts on{" past midnight" if t2 >= 1440 else ""}; A1 {dur(d)}.')


@m2.add('C3', (2, 3, 4, 5))
def m2_table(r, D):
    stops = r.sample(['Central', 'Harbour', 'Market', 'Airport', 'University', 'Stadium', 'Old Town', 'Hospital'], 4)
    gaps = [r.choice([12, 14, 18, 23, 26, 31]) for _ in range(3)]
    first = r.randint(6 * 12, 8 * 12) * 5
    every = r.choice([15, 20, 25, 30, 40])
    nbus = 4
    rows = []
    for i, s in enumerate(stops):
        off = sum(gaps[:i])
        rows.append(f'{s} ' + ' '.join(hm(first + k * every + off) for k in range(nbus)))
    table = 'Bus timetable — ' + '; '.join(rows) + '.'
    c = city(r)
    nm = person(r)
    k = r.randint(0, nbus - 2)
    arrive_b = first + k * every + gaps[0] + r.randint(1, every - 2)
    nxt = k + 1
    dep = first + nxt * every + gaps[0]
    arr = first + nxt * every + sum(gaps)
    if D <= 2:
        stem = f'The timetable shows buses in {c}. {table} How long does a bus take to travel from {stops[0]} to {stops[3]}?'
        return Q(stem, dur(sum(gaps)), f'B1 any column: {hm(first)} to {hm(first + sum(gaps))} = {dur(sum(gaps))}.')
    stem = f'The timetable shows buses in {c}. {table} {nm} arrives at the {stops[1]} stop at {h12(arrive_b)}. Find the time {nm} arrives at {stops[3]} on the next bus, and the total time from arriving at the stop to reaching {stops[3]}.'
    return Q(stem, f'Arrives {hm(arr)}; total time {dur(arr - arrive_b)}',
             f'B1 next bus from {stops[1]} at {hm(dep)}; B1 arrives {stops[3]} {hm(arr)}; M1 {hm(arr)} − {hm(arrive_b)}; A1 {dur(arr - arrive_b)}.')


@m2.add('C3', (3, 4, 5))
def m2_flight(r, D):
    c1, c2 = r.sample(['Dubai', 'Singapore', 'Nairobi', 'Lima', 'Toronto', 'Seoul', 'Lisbon', 'Mumbai', 'Auckland', 'Cairo'], 2)
    dep = r.randint(14 * 12, 23 * 12) * 5
    hrs = r.choice([2.4, 3.8, 5.6, 6.75, 7.2, 8.4, 9.15, 10.6, 11.25, 12.4])
    mins = round(hrs * 60)
    diff = r.choice([-5, -3, -2, 1, 2, 3, 4, 5, 6])
    arr = dep + mins
    loc = arr + diff * 60
    stem = f'A flight leaves {c1} at {hm(dep)} local time and the flight time is {ex(hrs)} hours. The local time in {c2} is {abs(diff)} hours {"ahead of" if diff > 0 else "behind"} {c1}. Find the local time in {c2} when the plane lands.'
    if D == 3:
        stem = f'A flight leaves {c1} at {hm(dep)} and the flight time is {ex(hrs)} hours. Find the time in {c1} when the plane lands in {c2}.'
        return Q(stem, f'{hm(arr)}{" the next day" if arr >= 1440 else ""}', f'M1 {ex(hrs)} h = {dur(mins)}; A1 {hm(dep)} + {dur(mins)} = {hm(arr)}.')
    return Q(stem, f'{hm(loc)}' + (' the next day' if loc >= 1440 else (' the previous day' if loc < 0 else '')),
             f'M1 {ex(hrs)} h = {dur(mins)}; M1 {c1} time of landing {hm(arr)}; M1 {"+" if diff > 0 else "−"} {abs(diff)} h; A1 {hm(loc)}.')


def m2_c4(r, D):
    c1, c2 = r.choice([('Lisbon', 'Porto'), ('Madrid', 'Seville'), ('Kuala Lumpur', 'Ipoh'), ('Cairo', 'Alexandria'), ('Toronto', 'Ottawa'), ('Mumbai', 'Pune'),
                       ('Hanoi', 'Hai Phong'), ('Santiago', 'Valparaíso'), ('Nairobi', 'Mombasa'), ('Bangkok', 'Hua Hin'), ('Seoul', 'Daejeon'), ('Istanbul', 'Ankara')])
    if r.random() < 0.5:
        c1, c2 = c2, c1
    sp = r.choice([72, 80, 88, 96, 104, 120, 132])
    du = r.choice([90, 105, 120, 135, 150, 165, 180, 210, 225, 240])
    dist = sp * du // 60
    dep = r.randint(5 * 12, 20 * 12) * 5
    arr = dep + du
    late = r.choice([15, 25, 35, 40, 50])
    nm = person(r)
    intro = f'{nm} takes a train from {c1} to {c2}. The train leaves at {hm(dep)} and is timetabled to arrive at {hm(arr)}. The distance is {dist} km.'
    parts = [
        P('Calculate the timetabled journey time.', dur(du), f'B1 {dur(du)}', 1),
        P('Calculate the average speed of the train in km/h.', f'{sp} km/h', f'M1 {dist} ÷ {ex(du / 60)}; A1 {sp} km/h', 2),
        P(f'The train is delayed by {late} minutes. Write down the new arrival time using the 12-hour clock.', h12(arr + late), f'M1 {hm(arr)} + {late} min = {hm(arr + late)}; A1 {h12(arr + late)}', 2),
        P(f'On a later day the train covers the same distance at an average speed of {sp + 8} km/h. Calculate the journey time, giving your answer in hours and minutes to the nearest minute.',
          dur(round(dist / (sp + 8) * 60)), f'M1 {dist} ÷ {sp + 8} = {ex(dist / (sp + 8), 3)} h; M1 × 60; A1 {dur(round(dist / (sp + 8) * 60))}', 3),
        P('Convert the departure time to the 12-hour clock.', h12(dep), f'B1 {h12(dep)}', 1),
    ]
    return cmp_(r, intro, parts)


m2.add('C4', (2, 3, 4, 5))(m2_c4)

# ---------------------------------------------------------------- bounds
m3 = topic('Upper and lower bounds', 'upper and lower bounds', 'calculations with bounds', 'bounds')
m3.fixed('C1', (1, 2), [
    ('A mass is 64 kg, correct to the nearest kilogram. Write down the lower bound.', '63.5 kg', 'Half of the 1 kg rounding unit below: 64 − 0.5 = 63.5 kg.', ['63 kg', '64.5 kg', '63.9 kg']),
    ('A length l is 2.4 m correct to 1 decimal place. Which is the error interval for l?', '2.35 ≤ l < 2.45', '±0.05 m; lower bound included, upper bound not included.', ['2.35 < l ≤ 2.45', '2.3 ≤ l < 2.5', '2.39 ≤ l ≤ 2.41']),
    ('To find the upper bound of a − b, you should use', 'upper bound of a − lower bound of b', 'The largest difference uses the largest a and the smallest b.', ['upper bound of a − upper bound of b', 'lower bound of a − lower bound of b', 'lower bound of a − upper bound of b']),
    ('To find the lower bound of a ÷ b (a, b positive), you should use', 'lower bound of a ÷ upper bound of b', 'Smallest quotient: smallest numerator over largest denominator.', ['lower bound of a ÷ lower bound of b', 'upper bound of a ÷ upper bound of b', 'upper bound of a ÷ lower bound of b']),
    ('To find the upper bound of a × b (a, b positive), you should use', 'upper bound of a × upper bound of b', 'Largest product: both factors as large as possible.', ['upper bound of a × lower bound of b', 'lower bound of a × lower bound of b', 'lower bound of a × upper bound of b']),
    ('A crowd is 3400 people, correct to the nearest hundred. What is the lower bound?', '3350', '3400 − 50 = 3350.', ['3300', '3399', '3390']),
])
m3.fixed('C2', (2, 3), [
    ('A length is 12 cm to the nearest centimetre. Explain why the upper bound is written as 12.5 cm and not 12.49 cm.', 'Every value up to, but not including, 12.5 rounds to 12, and there is no largest such value below 12.5 (12.49, 12.499, … all round to 12), so 12.5 is used as the boundary.', 'B1 values less than 12.5 round to 12; B1 no largest value below 12.5 so 12.5 is the bound [2]'),
    ('Explain why the upper bound of a − b uses the lower bound of b.', 'Subtracting a smaller number leaves a larger result, so the largest difference comes from the largest a and the smallest b.', 'B1 largest a; B1 smallest b gives largest difference [2]'),
    ('Explain why an answer worked out from rounded measurements may not be given to more significant figures than the bounds agree to.', 'The true value could be anywhere between the lower and upper bounds; only the figures that the bounds share are certain.', 'B1 true value lies between bounds; B1 only agreed figures are reliable [2]'),
    ('Explain why the error interval for a length of 8 m (nearest metre) is 7.5 ≤ l < 8.5 and not 7.5 ≤ l ≤ 8.5.', '8.5 rounds up to 9, so 8.5 itself is not included, but 7.5 rounds up to 8 so it is included.', 'B1 8.5 rounds to 9 (strict); B1 7.5 rounds to 8 (included) [2]'),
])

UNITS = [(1, 'to the nearest whole number', ''), (10, 'to the nearest 10', ''), (0.1, 'correct to 1 decimal place', ''), (5, 'to the nearest 5', ''), (100, 'to the nearest 100', ''), (0.01, 'correct to 2 decimal places', ''), (0.5, 'to the nearest 0.5', '')]


def _bnd(r, D):
    u, txt, _ = r.choice(UNITS if D >= 2 else UNITS[:3])
    k = r.randint(3, 99) if u >= 1 else r.randint(11, 999)
    x = round(k * u, 4)
    return x, u, txt


@m3.add('C1', (1, 2, 3))
def m3_b(r, D):
    x, u, txt = _bnd(r, D)
    item, unit = r.choice([('length of a rope', 'm'), ('mass of a parcel', 'kg'), ('time for a race', 's'), ('height of a tree', 'm'), ('volume of a bottle', 'ml'), ('distance', 'km')])
    lb, ub = round(x - u / 2, 6), round(x + u / 2, 6)
    if D == 3:
        c = f'{ex(lb)} ≤ d < {ex(ub)}'
        ds = [f'{ex(lb)} < d ≤ {ex(ub)}', f'{ex(lb)} ≤ d ≤ {ex(ub)}', f'{ex(round(x - u, 6))} ≤ d < {ex(round(x + u, 6))}', f'{ex(x)} ≤ d < {ex(ub)}']
        return SMC(r, f'The {item} is d = {ex(x)} {unit}, {txt}. Which is the error interval for d?', c, ds, f'Half the rounding unit is {ex(u / 2)}; {c}.')
    if r.random() < 0.5:
        return MC(r, f'The {item} is {ex(x)} {unit}, {txt}. What is the upper bound?', ub, [x + u, x + u / 10 if u / 10 != u / 2 else x + u * 0.4, x, round(x + u / 2 - u / 100, 6)], f'Upper bound = {ex(x)} + {ex(u / 2)} = {ex(ub)} {unit}.', fmtf=ex, unit=' ' + unit)
    return MC(r, f'The {item} is {ex(x)} {unit}, {txt}. What is the lower bound?', lb, [x - u, x - u / 10 if u / 10 != u / 2 else x - u * 0.4, ub, x], f'Lower bound = {ex(x)} − {ex(u / 2)} = {ex(lb)} {unit}.', fmtf=ex, unit=' ' + unit)


@m3.add('C2', (2, 3, 4), 'explain')
def m3_err(r, D):
    nm = person(r)
    case = r.choice(['sub', 'div'])
    if case == 'sub':
        a, b = r.randint(40, 95), r.randint(12, 38)
        stem = f'Two pieces of wood have lengths a = {a} cm and b = {b} cm, each correct to the nearest centimetre. {nm} says the upper bound of a − b is {a + 0.5} − {b + 0.5} = {a - b} cm. Explain why {nm} is wrong and find the correct upper bound.'
        return Q(stem, f'The largest difference uses the upper bound of a and the lower bound of b: {a + 0.5} − {b - 0.5} = {a - b + 1} cm.', f'B1 must use lower bound of b; B1 {a - b + 1} cm [2]')
    d, t = r.choice([100, 200, 400, 800, 1500]), r.choice([12.4, 25.8, 51.6, 98.2, 230.5])
    ub = (d + 0.5) / (t - 0.05)
    stem = f'A runner covers d = {d} m, correct to the nearest metre, in t = {t} s, correct to 1 decimal place. {nm} calculates the upper bound of the speed as {d + 0.5} ÷ {round(t + 0.05, 2)}. Explain the error and calculate the correct upper bound.'
    return Q(stem, f'The greatest speed uses the greatest distance and the least time: {d + 0.5} ÷ {round(t - 0.05, 2)} = {n3(ub)} m/s.', f'B1 divide by the lower bound of t; B1 {n3(ub)} m/s [2]')


@m3.add('C3', (2, 3, 4))
def m3_rect(r, D):
    a, b = r.randint(12, 48), r.randint(5, 30)
    u = 1 if D <= 2 else r.choice([1, 0.1])
    if u == 0.1:
        a, b = a / 10 + 2, b / 10 + 1
    h = u / 2
    q = r.choice(['UA', 'LA', 'UP', 'LP'])
    name = r.choice(['rectangular photograph', 'rectangular garden', 'rectangular sheet of metal', 'rectangular rug'])
    unit = 'cm' if 'photo' in name or 'metal' in name else 'm'
    txt = 'correct to the nearest ' + (unit if u == 1 else '0.1 ' + unit)
    A, B = round(a, 2), round(b, 2)
    if q in ('UA', 'LA'):
        s = 1 if q == 'UA' else -1
        v = (A + s * h) * (B + s * h)
        w = 'upper' if s > 0 else 'lower'
        return Q(f'A {name} measures {ex(A)} {unit} by {ex(B)} {unit}, each {txt}. Calculate the {w} bound of its area.', f'{ex(round(v, 4))} {unit}²',
                 f'B1 bounds {ex(A + s * h)} and {ex(B + s * h)}; M1 product; A1 {ex(round(v, 4))} {unit}².')
    s = 1 if q == 'UP' else -1
    v = 2 * (A + s * h) + 2 * (B + s * h)
    w = 'upper' if s > 0 else 'lower'
    return Q(f'A {name} measures {ex(A)} {unit} by {ex(B)} {unit}, each {txt}. Calculate the {w} bound of its perimeter.', f'{ex(round(v, 4))} {unit}',
             f'B1 bounds {ex(A + s * h)} and {ex(B + s * h)}; M1 2 × sum; A1 {ex(round(v, 4))} {unit}.')


@m3.add('C3', (3, 4, 5))
def m3_speed(r, D):
    unit_d, unit_t = ('m', 's') if D <= 3 else ('km', 'h')
    ud = 10 if D <= 3 else 0.1
    ut = 0.1
    if D <= 3:
        what, d, t = r.choice([('A cyclist', r.choice([120, 150, 240, 360]), r.choice([14.2, 18.6, 25.4, 31.8])), ('A remote-controlled car', r.choice([40, 60, 80, 90]), r.choice([6.4, 8.2, 9.5, 12.6])),
                               ('A sprinter', r.choice([60, 100, 200]), 0), ('A drone', r.choice([150, 240, 450, 600]), r.choice([18.4, 25.6, 47.5, 52.3]))])
        if what == 'A sprinter':
            t = {60: 7.8, 100: 12.4, 200: 25.3}[d] + r.choice([0, 0.3, 0.6, 0.9])
            ud = 1
    else:
        what, d, t = r.choice([('A marathon runner', 42.2, r.choice([2.8, 3.2, 3.6, 4.1])), ('A ferry', r.choice([12.5, 18.4, 22.6]), r.choice([0.6, 0.8, 0.9, 1.2])),
                               ('A delivery van', r.choice([26.2, 38.5, 54.8]), r.choice([0.7, 0.9, 1.1, 1.4])), ('A long-distance cyclist', r.choice([64.5, 88.2, 102.4]), r.choice([2.6, 3.4, 4.2]))])
    t = round(t, 2)
    w = r.choice(['upper', 'lower'])
    if w == 'upper':
        v = (d + ud / 2) / (t - ut / 2)
        k = f'M1 uses {ex(d + ud / 2)} and {ex(round(t - ut / 2, 3))}; M1 divides UB(d) by LB(t); A1 {n3(v)} {unit_d}/{unit_t}.'
    else:
        v = (d - ud / 2) / (t + ut / 2)
        k = f'M1 uses {ex(d - ud / 2)} and {ex(round(t + ut / 2, 3))}; M1 divides LB(d) by UB(t); A1 {n3(v)} {unit_d}/{unit_t}.'
    return Q(f'{what} travels {ex(d)} {unit_d}, correct to the nearest {ex(ud)} {unit_d}, in {ex(t)} {unit_t}, correct to 1 decimal place. Calculate the {w} bound of the average speed.', f'{n3(v)} {unit_d}/{unit_t}', k)


@m3.add('C3', (2, 3, 4))
def m3_diff(r, D):
    a = r.randint(150, 900)
    b = r.randint(40, a - 60)
    u = r.choice([5, 10]) if D >= 3 else 10
    a, b = round(a / u) * u, round(b / u) * u
    w = r.choice(['greatest', 'least'])
    h = u / 2
    v = (a + h) - (b - h) if w == 'greatest' else (a - h) - (b + h)
    return Q(f'A container holds {a} ml of juice, correct to the nearest {u} ml. {person(r)} pours out {b} ml, correct to the nearest {u} ml. Calculate the {w} possible volume of juice left in the container.',
             f'{ex(v)} ml', f'B1 bounds of both amounts; M1 {"UB − LB" if w == "greatest" else "LB − UB"}; A1 {ex(v)} ml.')


def m3_c4(r, D):
    L, W = r.randint(25, 80), r.randint(12, 40)
    p = r.choice([1.8, 2.4, 2.5, 3.2])
    intro = f'A rectangular field near {city(r)} is {L} m long and {W} m wide, each measurement correct to the nearest metre. Fence panels are {ex(p)} m long, correct to 1 decimal place.'
    ubp = 2 * (L + 0.5) + 2 * (W + 0.5)
    lbp = 2 * (L - 0.5) + 2 * (W - 0.5)
    lba = (L - 0.5) * (W - 0.5)
    uba = (L + 0.5) * (W + 0.5)
    lbpan = p - 0.05
    npan = math.ceil(ubp / lbpan - 1e-9)
    parts = [
        P('Write down the lower bound of the length.', f'{L - 0.5} m', 'B1', 1),
        P('Calculate the upper bound of the perimeter.', f'{ex(ubp)} m', f'M1 2 × ({L + 0.5} + {W + 0.5}); A1 {ex(ubp)} m', 2),
        P('Calculate the lower bound of the area.', f'{ex(lba)} m²', f'M1 {L - 0.5} × {W - 0.5}; A1 {ex(lba)} m²', 2),
        P('Calculate the difference between the upper and lower bounds of the area.', f'{ex(uba - lba)} m²', f'M1 {ex(uba)} − {ex(lba)}; A1 {ex(uba - lba)} m²', 2),
        P('Calculate the least number of panels that is certain to be enough to go all the way round the field.', f'{npan} panels',
          f'M1 uses UB perimeter {ex(ubp)}; M1 ÷ LB panel {ex(round(lbpan, 2))} = {ex(ubp / lbpan, 3)}; A1 round up to {npan}', 3),
        P('Explain why the area cannot be stated exactly.', f'The length and width are rounded, so the area could be anywhere from {ex(lba)} m² up to (not including) {ex(uba)} m².', 'B1 measurements rounded; B1 area lies between bounds', 2),
    ]
    return cmp_(r, intro, parts)


def m3_c4b(r, D):
    d = r.choice([100, 200, 400])
    t = r.choice([10.6, 11.4, 12.8, 21.3, 23.7, 48.2, 52.9, 55.4])
    if d == 100:
        t = r.choice([10.6, 11.4, 12.8, 13.5])
    elif d == 200:
        t = r.choice([21.3, 23.7, 25.1, 27.6])
    else:
        t = r.choice([48.2, 52.9, 55.4, 61.7])
    nm = person(r)
    ub = (d + 0.5) / (t - 0.05)
    lb = (d - 0.5) / (t + 0.05)
    best = 0
    for k in (1, 2, 3, 4):
        if sf(ub, k) == sf(lb, k):
            best = k
    acc = (f'{sf(ub, best)} m/s ({best} s.f.), since both bounds round to this' if best else 'not even to 1 s.f., since the bounds differ in the first figure')
    intro = f'{nm} runs {d} m, measured correct to the nearest metre, in a time of {t} s, correct to 1 decimal place, at a school athletics event in {city(r)}.'
    parts = [
        P('Write down the upper bound of the time.', f'{round(t + 0.05, 2)} s', 'B1', 1),
        P('Calculate the upper bound of the average speed.', f'{n3(ub)} m/s', f'M1 {d + 0.5} ÷ {round(t - 0.05, 2)}; A1 {n3(ub)}', 2),
        P('Calculate the lower bound of the average speed.', f'{n3(lb)} m/s', f'M1 {d - 0.5} ÷ {round(t + 0.05, 2)}; A1 {n3(lb)}', 2),
        P('Using your bounds, write down the average speed to an appropriate degree of accuracy, giving a reason.', acc, f'M1 compares rounded bounds ({ex(round(ub, 4))}, {ex(round(lb, 4))}); A1 conclusion', 2),
    ]
    return cmp_(r, intro, parts, k=(3, 4))


m3.add('C4', (2, 3, 4, 5))(m3_c4)
m3.add('C4', (3, 4, 5))(m3_c4b)

# ---------------------------------------------------------------- currency and conversion graphs
CURS = [('US dollars', '$', 'euros', '€', 0.92), ('euros', '€', 'US dollars', '$', 1.08), ('pounds', '£', 'US dollars', '$', 1.27),
        ('US dollars', '$', 'Malaysian ringgit', 'RM', 4.7), ('euros', '€', 'South African rand', 'R', 20.2), ('US dollars', '$', 'Indian rupees', '₹', 83.2),
        ('pounds', '£', 'euros', '€', 1.17), ('US dollars', '$', 'UAE dirhams', 'AED', 3.67), ('euros', '€', 'Japanese yen', '¥', 162.5)]


def cfmt(sym, x, dp=2):
    if sym in ('$', '€', '£'):
        return f'{sym}{x:,.2f}'
    return f'{sym}{x:,.{dp}f}' if sym in ('₹', '¥') else f'{sym} {x:,.{dp}f}'


m4 = topic('Conversion graphs and currency exchange', 'conversion graphs', 'money: currency exchange rates', 'currency exchange')
m4.fixed('C1', (1, 2), [
    ('On a conversion graph between two currencies, what does the gradient of the line represent?', 'The exchange rate', 'Gradient = change in one currency ÷ change in the other = exchange rate.', ['The commission charged', 'The total amount changed', 'The date of the exchange']),
    ('Why does a conversion graph between two currencies pass through the origin?', '0 in one currency is worth 0 in the other', 'The currencies are in direct proportion, so (0, 0) lies on the line.', ['Because the exchange rate is 1', 'Because there is always a commission', 'Because the graph is curved']),
    ('Which conversion graph does NOT pass through the origin?', 'degrees Celsius to degrees Fahrenheit', '0 °C = 32 °F, so the line has a y-intercept of 32.', ['kilometres to miles', 'kilograms to pounds', 'US dollars to euros']),
    ('£1 = $1.25. How many dollars do you get for £40?', '$50', '40 × 1.25 = 50.', ['$32', '$41.25', '$45']),
    ('€1 = $1.10. How many euros do you get for $55?', '€50', '55 ÷ 1.10 = 50.', ['€60.50', '€55', '€49.50']),
])
m4.fixed('C2', (2, 3), [
    ('Explain why the conversion graph from °C to °F does not pass through the origin.', '0 °C is 32 °F, not 0 °F, so the two scales are not in direct proportion and the line cuts the °F axis at 32.', 'B1 0 °C = 32 °F; B1 not direct proportion / intercept 32 [2]'),
    ('Explain why a value read from a conversion graph is only an estimate.', 'Reading a scale by eye is limited by the size of the squares and the thickness of the line, so the reading is approximate.', 'B1 reading by eye/scale; B1 approximate value [2]'),
    ('A tourist changes money and then immediately changes it back. Explain why they usually get back less than they started with.', 'Banks sell currency at a less favourable rate than they buy it and may also charge commission, so value is lost on each exchange.', 'B1 different buy/sell rates; B1 commission/fees [2]'),
    ('Describe how you would use a straight-line conversion graph from kilometres to miles to convert 250 km, if the graph only goes up to 100 km.', 'Read off a value such as 50 km (about 31 miles) and multiply by 5, because the quantities are in direct proportion.', 'B1 read a convenient value; B1 scale up using proportion [2]'),
])


@m4.add('C1', (1, 2, 3))
def m4_q(r, D):
    a, sa, b, sb, k = r.choice(CURS)
    amt = r.choice([20, 40, 50, 80, 100, 150, 200, 250, 500])
    c = amt * k
    return MC(r, f'The exchange rate is 1 {a[:-1] if a.endswith("s") else a} = {cfmt(sb, k, 2)}. How many {b} would you receive for {cfmt(sa, amt)}?', c,
              [amt / k, c * 10, c / 10, amt + k], f'{amt} × {ex(k)} = {ex(round(c, 2))}.', fmtf=lambda x: cfmt(sb, x))


@m4.add('C2', (2, 3, 4), 'explain')
def m4_err(r, D):
    a, sa, b, sb, k = r.choice(CURS)
    nm = person(r)
    amt = r.choice([120, 240, 350, 480, 640, 900, 1200]) * (10 if k > 50 else 1)
    wrong = amt * k
    right = amt / k
    return Q(f'The exchange rate is 1 {a[:-1] if a.endswith("s") else a} = {cfmt(sb, k, 2)}. {nm} wants to change {cfmt(sb, amt)} into {a} and works out {ex(amt)} × {ex(k)} = {ex(round(wrong, 2))}. Explain the mistake and find the correct amount.',
             f'{nm} should divide, because each unit of {a} costs {ex(k)} {b}: {ex(amt)} ÷ {ex(k)} = {cfmt(sa, right)}.',
             f'B1 should divide (converting from {b} to {a}); B1 {cfmt(sa, right)} [2]')


@m4.add('C3', (1, 2, 3, 4))
def m4_compare(r, D):
    a, sa, b, sb, k = r.choice(CURS)
    item = r.choice(['pair of trainers', 'phone case', 'headphones', 'school bag', 'football shirt', 'camera'])
    p1 = r.choice([45, 60, 75, 89, 120, 150])
    p2 = round(p1 * k * r.choice([0.85, 0.9, 1.08, 1.15]), 0 if k > 3 else 2)
    c1, c2 = city(r), city(r)
    conv = p2 / k
    cheaper = f'{c1}' if p1 < conv else f'{c2}'
    stem = f'A {item} costs {cfmt(sa, p1)} in {c1} and {cfmt(sb, p2)} in {c2}. The exchange rate is 1 {a[:-1] if a.endswith("s") else a} = {cfmt(sb, k, 2)}. Find where it is cheaper and by how much, in {a}.'
    return Q(stem, f'Cheaper in {cheaper} by {cfmt(sa, abs(p1 - conv))}', f'M1 {ex(p2)} ÷ {ex(k)} = {cfmt(sa, conv)}; A1 comparison and difference {cfmt(sa, abs(p1 - conv))}.')


@m4.add('C3', (2, 3, 4))
def m4_graph(r, D):
    case = r.choice(['km', 'temp', 'cur'])
    if case == 'km':
        x = r.choice([15, 20, 35, 45, 70, 110, 125])
        return Q(f'A straight-line conversion graph passes through (0, 0) and (50 miles, 80 km). Use it to convert {x} miles to kilometres.', f'{ex(x * 1.6)} km', f'M1 gradient 80 ÷ 50 = 1.6 km per mile; A1 {x} × 1.6 = {ex(x * 1.6)} km.')
    if case == 'temp':
        c = r.choice([15, 25, 35, 40, 65, 80, -10, -20])
        f = 1.8 * c + 32
        return Q(f'A conversion graph between °C and °F is a straight line through (0, 32) and (100, 212). Find the equation of the line and use it to convert {num(c)} °C to °F.', f'F = 1.8C + 32; {num(f)} °F',
                 f'M1 gradient (212 − 32) ÷ 100 = 1.8; B1 intercept 32; A1 {num(f)} °F.')
    a, sa, b, sb, k = r.choice(CURS)
    x0 = r.choice([10, 20, 50, 100])
    y0 = x0 * k
    amt = r.choice([35, 65, 140, 275, 380])
    return Q(f'A conversion graph between {a} and {b} is a straight line through (0, 0) and ({cfmt(sa, x0)}, {cfmt(sb, y0)}). Calculate the value of {cfmt(sb, amt * k)} in {a}.', cfmt(sa, amt),
             f'M1 rate {ex(round(y0, 4))} ÷ {x0} = {ex(k)}; A1 {ex(round(amt * k, 2))} ÷ {ex(k)} = {cfmt(sa, amt)}.')


@m4.add('C3', (2, 3, 4, 5))
def m4_comm(r, D):
    a, sa, b, sb, k = r.choice(CURS)
    amt = r.choice([200, 300, 450, 600, 750, 1000])
    cpc = r.choice([1.5, 2, 2.5, 3])
    after = amt * (1 - cpc / 100)
    got = after * k
    return Q(f'A bureau de change in {city(r)} charges {ex(cpc)}% commission on the amount changed, then converts at 1 {a[:-1] if a.endswith("s") else a} = {cfmt(sb, k, 2)}. {person(r)} changes {cfmt(sa, amt)}. Calculate the amount received in {b}.',
             cfmt(sb, got), f'M1 commission {ex(cpc)}% of {amt} = {ex(round(amt * cpc / 100, 2))}; M1 ({ex(round(after, 2))}) × {ex(k)}; A1 {cfmt(sb, got)}.')


def m4_c4(r, D):
    a, sa, b, sb, k = r.choice(CURS)
    nm = person(r)
    amt = r.choice([500, 800, 1000, 1200, 1500])
    spent_f = r.choice([0.6, 0.65, 0.7, 0.75, 0.8])
    k2 = round(k * r.choice([1.03, 1.05, 1.06]), 2 if sb in ('$', '€', '£') else (3 if k < 10 else 1))
    got = amt * k
    spent = round(got * spent_f, 2)
    left = got - spent
    back = left / k2
    one = a[:-1] if a.endswith('s') else a
    intro = f'{nm} is travelling from {city(r)}. {nm} changes {cfmt(sa, amt)} into {b} at a rate of 1 {one} = {cfmt(sb, k, 2)}. During the trip {nm} spends {cfmt(sb, spent)}.'
    parts = [
        P(f'Calculate how many {b} {nm} receives.', cfmt(sb, got), f'M1 {amt} × {ex(k)}; A1 {cfmt(sb, got)}', 2),
        P(f'Calculate the percentage of the money that is spent.', f'{ex(spent_f * 100)}%', f'M1 {ex(spent)} ÷ {ex(round(got, 2))} × 100; A1 {ex(spent_f * 100)}%', 2),
        P(f'At the end of the trip {nm} changes the money left back into {a} at a rate of 1 {one} = {cfmt(sb, k2, 3 if k2 < 10 else 1)}. Calculate how much {nm} receives, to the nearest cent.', cfmt(sa, back),
          f'M1 {ex(round(got, 2))} − {ex(spent)} = {ex(round(left, 2))}; M1 ÷ {ex(k2)}; A1 {cfmt(sa, back)}', 3),
        P('Explain why changing money back usually gives a worse result for the traveller.', 'The selling rate differs from the buying rate (and fees may be charged), so each exchange loses value.', 'B1 different rates/fees', 1),
    ]
    return cmp_(r, intro, parts)


m4.add('C4', (2, 3, 4, 5))(m4_c4)
CHAPTERS[1] = [m1, m2, m3, m4]


# =========================================================== 2 Further solving of equations and inequalities (Ch 14)
def d2(x):
    return f'{x:.2f}'.replace('-', MINUS)


def _sim(r, D):
    """Return (a1,b1,c1,a2,b2,c2,x,y) with integer solution."""
    for _ in range(200):
        if D <= 2:
            x, y = r.randint(1, 9), r.randint(1, 9)
        elif D <= 3:
            x, y = r.randint(-6, 9), r.randint(-6, 9)
        else:
            x, y = r.choice([r.randint(-8, 9), r.randint(-8, 9) + 0.5]), r.randint(-7, 9)
        if D <= 2:
            a = r.randint(1, 6)
            b1, b2 = r.randint(1, 6), r.randint(1, 6)
            a1, a2 = a, a
            if r.random() < 0.5:
                b2 = -b2
            if r.random() < 0.5:
                a1, a2, b1, b2 = b1, b2, a, a if b2 > 0 else -a
        elif D == 3:
            a1, b1 = r.randint(1, 7), r.choice([-1, 1]) * r.randint(1, 7)
            m = r.randint(2, 4)
            a2, b2 = r.randint(1, 7), b1 * m if r.random() < 0.5 else r.choice([-1, 1]) * r.randint(1, 7)
            if r.random() < 0.5:
                b2 = -b1 * m
        else:
            a1, a2 = r.randint(2, 7), r.randint(2, 7)
            b1, b2 = r.choice([-1, 1]) * r.randint(2, 7), r.choice([-1, 1]) * r.randint(2, 7)
        if a1 * b2 - a2 * b1 == 0 or 0 in (a1, a2, b1, b2):
            continue
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        if c1 != int(c1) or c2 != int(c2):
            continue
        return a1, b1, int(c1), a2, b2, int(c2), x, y
    return 2, 3, 2 * 2 + 3 * 1, 1, -1, 1, 2, 1


def eqn(a, b, c):
    return f'{expr((a, "x"), (b, "y"))} = {num(c)}'


e1 = topic('Simultaneous linear equations', 'simultaneous linear equations', 'elimination and substitution', 'simultaneous')
e1.fixed('C1', (1, 2), [
    ('To solve 3x + 2y = 12 and 5x − 2y = 4 by elimination, what should you do first?', 'Add the two equations', 'The y-coefficients are +2 and −2, so adding eliminates y: 8x = 16.', ['Subtract the two equations', 'Multiply both equations by 2', 'Divide the first equation by 3']),
    ('On a graph, the solution of a pair of simultaneous linear equations is shown by', 'the point where the two lines intersect', 'The intersection point satisfies both equations.', ['the y-intercept of the first line', 'the gradient of the lines', 'the point where a line crosses the x-axis']),
    ('Two simultaneous linear equations have no solution. What does this mean about their graphs?', 'The lines are parallel', 'Parallel lines never meet, so there is no common point.', ['The lines are perpendicular', 'The lines meet at the origin', 'The lines are the same line']),
    ('In the substitution method for y = 2x − 1 and 3x + y = 9, which equation do you get after substituting?', '3x + 2x − 1 = 9', 'Replace y with 2x − 1 in 3x + y = 9.', ['3x + 2x + 1 = 9', '3x − 2x − 1 = 9', '2x − 1 = 9']),
    ('Which method is most efficient for 4x + 3y = 17 and 4x − y = 5?', 'Subtract the equations to eliminate x', 'Both have 4x, so subtracting removes x: 4y = 12.', ['Add the equations to eliminate x', 'Multiply the first equation by 4', 'Draw the graphs to two decimal places']),
])
e1.fixed('C2', (2, 3), [
    ('Explain how you decide whether to add or subtract two equations when using elimination.', 'Make the coefficients of one variable equal in size. If they have the same sign, subtract; if they have opposite signs, add.', 'B1 equal coefficients; B1 same sign subtract / opposite signs add [2]'),
    ('Explain why the equations 2x + 3y = 7 and 4x + 6y = 10 have no solution.', 'Doubling the first gives 4x + 6y = 14, which contradicts 4x + 6y = 10; the lines are parallel and never meet.', 'B1 compare multiples; B1 parallel/contradiction [2]'),
    ('Explain why substitution is a good method for y = 3x − 4 and 5x − 2y = 6.', 'The first equation already gives y in terms of x, so it can be substituted directly into the second.', 'B1 y is already the subject; B1 substitute into other equation [2]'),
    ('Explain how you can check a solution to a pair of simultaneous equations.', 'Substitute both values into the equation not used in the final step (ideally both equations); each side must balance.', 'B1 substitute values; B1 into both / the other equation [2]'),
])


@e1.add('C1', (1, 2, 3))
def e1_pick(r, D):
    a1, b1, c1, a2, b2, c2, x, y = _sim(r, min(D, 3))
    c = f'x = {num(x)}, y = {num(y)}'
    ds = [f'x = {num(y)}, y = {num(x)}', f'x = {num(x)}, y = {num(-y)}', f'x = {num(x + 1)}, y = {num(y - 1)}', f'x = {num(-x)}, y = {num(y)}', f'x = {num(x + 2)}, y = {num(y)}']
    return SMC(r, f'Which values satisfy both {eqn(a1, b1, c1)} and {eqn(a2, b2, c2)}?', c, ds, f'Check in both: {num(a1)}({num(x)}) + {num(b1)}({num(y)}) = {num(c1)} and {num(a2)}({num(x)}) + {num(b2)}({num(y)}) = {num(c2)}.')


@e1.add('C2', (2, 3, 4), 'explain')
def e1_err(r, D):
    for _ in range(50):
        a, b, d = r.randint(2, 6), r.randint(1, 6), r.randint(1, 6)
        if b == d:
            continue
        x, y = r.randint(1, 8), r.randint(1, 8)
        c1, c2 = a * x + b * y, a * x - d * y
        break
    nm = person(r)
    wrong = Fr(c1 - c2, b - d)
    return Q(f'{nm} solves {eqn(a, b, c1)} and {eqn(a, -d, c2)} by subtracting the second equation from the first and writes {term_str(b - d, "y") if b - d > 0 else MINUS + term_str(d - b, "y")} = {num(c1 - c2)}. Explain the error and find the correct values of x and y.',
             f'{num(b)}y − ({MINUS}{num(d)}y) = {num(b + d)}y, not {num(b - d)}y. So {num(b + d)}y = {num(c1 - c2)}, y = {num(y)} and x = {num(x)}.',
             f'B1 subtracting a negative: {num(b)}y − ({MINUS}{num(d)}y) = {num(b + d)}y; M1 correct elimination; A1 x = {num(x)}, y = {num(y)} [3]', marks=3)


@e1.add('C3', (1, 2, 3, 4, 5))
def e1_solve(r, D):
    a1, b1, c1, a2, b2, c2, x, y = _sim(r, D)
    stem = f'Solve the simultaneous equations. {TRY} {eqn(a1, b1, c1)}, {eqn(a2, b2, c2)}'
    if D == 1:
        return MC(r, f'Solve {eqn(a1, b1, c1)} and {eqn(a2, b2, c2)}. What is the value of x?', x, [y, x + 1, -x if x else 3, x + 2], f'Eliminate y, solve for x = {num(x)} (y = {num(y)}).')
    key = 'M1 makes coefficients of one variable equal' + (' (multiplying one or both equations)' if D >= 3 else '') + f'; M1 adds/subtracts correctly; A1 x = {num(x)}; A1 y = {num(y)}.'
    return Q(stem, f'x = {num(x)}, y = {num(y)}', key)


@e1.add('C3', (2, 3, 4))
def e1_subs(r, D):
    m, k = r.randint(2, 5), r.randint(-6, 6)
    x = r.randint(-4, 7)
    y = m * x + k
    a, b = r.randint(2, 6), r.choice([-1, 1]) * r.randint(2, 5)
    c = a * x + b * y
    return Q(f'Use substitution to solve y = {lin(m, k)} and {eqn(a, b, c)}.', f'x = {num(x)}, y = {num(y)}',
             f'M1 {num(a)}x {"+" if b > 0 else "−"} {num(abs(b))}({lin(m, k)}) = {num(c)}; M1 collects: {num(a + b * m)}x = {num(c - b * k)}; A1 x = {num(x)}; A1 y = {num(y)}.')


SIM_CTX = [('adult', 'child', 'tickets for a concert in {c}'), ('large', 'small', 'bottles of juice at a market in {c}'), ('pen', 'notebook', 'items at a stationery shop in {c}'),
           ('coffee', 'cake', 'items at a café in {c}'), ('melon', 'pineapple', 'fruit at a market stall in {c}')]


@e1.add('C3', (2, 3, 4, 5))
def e1_word(r, D):
    A, B, what = r.choice(SIM_CTX)
    pa, pb = r.choice([4, 5, 6, 7.5, 8, 12, 15]), r.choice([1.5, 2, 2.5, 3, 3.5, 4, 6])
    if pa == pb:
        pa += 1
    m1_, n1 = r.randint(1, 5), r.randint(1, 5)
    m2_, n2 = r.randint(1, 5), r.randint(1, 5)
    if m1_ * n2 == m2_ * n1:
        n2 += 1
    t1, t2 = m1_ * pa + n1 * pb, m2_ * pa + n2 * pb
    nm1, nm2 = two_people(r)
    w = what.format(c=city(r))
    stem = f'Prices for {w}: {nm1} pays ${t1:.2f} for {m1_} {A} and {n1} {B}. {nm2} pays ${t2:.2f} for {m2_} {A} and {n2} {B}. Write down two equations and solve them to find the price of one {A} and one {B}.'
    return Q(stem, f'{A}: ${pa:.2f}; {B}: ${pb:.2f}', f'B1 {m1_}a + {n1}b = {ex(t1)}; B1 {m2_}a + {n2}b = {ex(t2)}; M1 elimination; A1 a = {ex(pa)}, b = {ex(pb)}.')


def e1_c4(r, D):
    A, B, what = r.choice(SIM_CTX)
    pa, pb = r.choice([5, 6, 8, 9, 12]), r.choice([2, 3, 4, 2.5, 3.5])
    m1_, n1, m2_, n2 = r.randint(2, 5), r.randint(1, 4), r.randint(1, 3), r.randint(3, 6)
    if m1_ * n2 == m2_ * n1:
        n2 += 1
    t1, t2 = m1_ * pa + n1 * pb, m2_ * pa + n2 * pb
    budget = r.choice([60, 75, 90, 100, 120])
    na = r.randint(2, 4)
    nb = int((budget - na * pa) // pb)
    w = what.format(c=city(r))
    intro = f'A school group buys {w}. {m1_} {A} and {n1} {B} cost ${t1:.2f}. {m2_} {A} and {n2} {B} cost ${t2:.2f}. Let the price of one {A} be $a and one {B} be $b.'
    parts = [
        P('Write down two equations in a and b.', f'{m1_}a + {n1}b = {ex(t1)}, {m2_}a + {n2}b = {ex(t2)}', 'B1 B1', 2),
        P('Solve your equations to find a and b.', f'a = {ex(pa)}, b = {ex(pb)}', 'M1 equal coefficients; M1 eliminate; A1 A1', 4),
        P(f'The group has ${budget}. They buy {na} {A}. Find the greatest number of {B} they can also buy.', f'{nb}', f'M1 ({budget} − {na} × {ex(pa)}) ÷ {ex(pb)}; A1 {nb} (round down)', 2),
        P('Describe how the solution could be found from a graph.', 'Draw both lines and read the coordinates of the point of intersection, (a, b).', 'B1 intersection of the two lines', 1),
    ]
    return cmp_(r, intro, parts)


e1.add('C4', (2, 3, 4, 5))(e1_c4)

# ---------------------------------------------------------------- quadratics
e2 = topic('Solving quadratic equations', 'solving quadratic equations', 'completing the square', 'quadratic formula')
e2.fixed('C1', (1, 2), [
    ('Which is the quadratic formula for ax² + bx + c = 0?', 'x = (−b ± √(b² − 4ac)) / 2a', 'Standard formula; the whole numerator is divided by 2a.', ['x = −b ± √(b² − 4ac) / 2a', 'x = (b ± √(b² − 4ac)) / 2a', 'x = (−b ± √(b² + 4ac)) / 2a']),
    ('A quadratic equation has b² − 4ac < 0. How many real solutions does it have?', 'None', 'The square root of a negative number is not real.', ['One', 'Two', 'Infinitely many']),
    ('Which of these is x² + 6x + 2 written in completed square form?', '(x + 3)² − 7', '(x + 3)² = x² + 6x + 9, so subtract 7.', ['(x + 6)² − 34', '(x + 3)² + 2', '(x + 3)² − 11']),
    ('What are the solutions of (x − 4)(x + 5) = 0?', 'x = 4 or x = −5', 'Each bracket equal to zero.', ['x = −4 or x = 5', 'x = 4 or x = 5', 'x = −4 or x = −5']),
    ('A quadratic equation has b² − 4ac = 0. How many distinct real solutions does it have?', 'One (a repeated root)', '±√0 gives the same value twice.', ['None', 'Two', 'Three']),
])
e2.fixed('C2', (2, 3), [
    ('Explain why the equation x² + 4x + 9 = 0 has no real solutions.', 'b² − 4ac = 16 − 36 = −20 < 0; there is no real square root of a negative number. Also (x + 2)² + 5 is always at least 5, so it is never 0.', 'B1 discriminant negative (or completed square ≥ 5); B1 conclusion [2]'),
    ('Explain why a quadratic equation can have at most two solutions.', 'Its graph is a parabola, which can cross a horizontal line (the x-axis) at most twice; equivalently the ± in the formula gives at most two values.', 'B1 parabola/±; B1 at most two crossings [2]'),
    ('In a problem, the length of a rectangle satisfies x² + 2x − 48 = 0, giving x = 6 or x = −8. Explain which solution should be used.', 'x = 6, because a length cannot be negative.', 'B1 x = 6; B1 reason (length positive) [2]'),
    ('Explain why x² = 5x cannot be solved by dividing both sides by x.', 'Dividing by x loses the solution x = 0. Write x² − 5x = 0, x(x − 5) = 0, so x = 0 or x = 5.', 'B1 loses x = 0; B1 factorise to get both [2]'),
])


@e2.add('C1', (1, 2, 3))
def e2_cs(r, D):
    p = r.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
    c = r.randint(-12, 15)
    q = c - p * p
    corr = f'{bracket(p)}²{sgn(q)}'
    ds = [f'{bracket(2 * p)}²{sgn(c - 4 * p * p)}', f'{bracket(p)}²{sgn(c + p * p)}', f'{bracket(-p)}²{sgn(q)}', f'{bracket(p)}²{sgn(c)}']
    return SMC(r, f'Write {quad(1, 2 * p, c)} in the form (x + p)² + q.', corr, ds, f'Halve the x coefficient: {bracket(p)}² = {quad(1, 2 * p, p * p)}; q = {num(c)} − {num(p * p)} = {num(q)}.')


@e2.add('C2', (2, 3, 4), 'explain')
def e2_err(r, D):
    for _ in range(100):
        a, b, c = r.choice([1, 2, 3]), r.randint(-9, 9), r.randint(-9, 6)
        disc = b * b - 4 * a * c
        if disc > 0 and b != 0 and int(math.isqrt(disc)) ** 2 != disc:
            break
    nm = person(r)
    x1, x2 = (-b + math.sqrt(disc)) / (2 * a), (-b - math.sqrt(disc)) / (2 * a)
    kind = r.choice(['sign', 'twoa'])
    if kind == 'sign':
        stem = f'{nm} solves {quad(a, b, c)} = 0 with the quadratic formula and writes x = ({num(b)} ± √{disc}) ÷ {2 * a}. Explain the error and give the correct solutions to 2 decimal places.'
        ans = f'The formula uses −b, so the numerator should start with {num(-b)}. x = {d2(x1)} or x = {d2(x2)}.'
    else:
        stem = f'{nm} solves {quad(a, b, c)} = 0 and writes x = {num(-b)} ± √{disc} ÷ {2 * a}, dividing only the square root by {2 * a}. Explain the error and give the correct solutions to 2 decimal places.'
        ans = f'The whole of −b ± √(b² − 4ac) must be divided by 2a. x = {d2(x1)} or x = {d2(x2)}.'
    return Q(stem, ans, f'B1 identifies the error; M1 correct substitution into formula, discriminant {disc}; A1 {d2(x1)} and {d2(x2)} [3]', marks=3)


@e2.add('C3', (1, 2, 3))
def e2_fact(r, D):
    p, q = r.sample([-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    if q == -p:
        q = -q + (1 if -q < 9 else -1) if False else (q + 1 if q + 1 not in (0, p, -p) else q - 1)
    a = 1 if D <= 2 else r.choice([1, 2, 3])
    if a == 1:
        b, c = -(p + q), p * q
        stem = f'Solve by factorising: {quad(1, b, c)} = 0.'
        sol = f'x = {num(p)} or x = {num(q)}'
        key = f'M1 ({lin(1, -p)})({lin(1, -q)}) = 0; A1 {sol}.'
        if D == 1:
            return SMC(r, f'Which are the solutions of {quad(1, b, c)} = 0?', sol, [f'x = {num(-p)} or x = {num(-q)}', f'x = {num(p)} or x = {num(-q)}', f'x = {num(c)} or x = {num(b)}', f'x = {num(-p)} or x = {num(q)}'], key)
        return Q(stem, sol, key)
    # (a x - p)(x - q) = a x² - (aq + p) x + pq
    b, c = -(a * q + p), p * q
    sol = f'x = {frac(Fr(p, a))} or x = {num(q)}'
    return Q(f'Solve by factorising: {quad(a, b, c)} = 0.', sol, f'M1 ({lin(a, -p)})({lin(1, -q)}) = 0; A1 {sol}.')


@e2.add('C3', (2, 3, 4, 5))
def e2_formula(r, D):
    for _ in range(200):
        a = 1 if D <= 2 else r.randint(1, 5)
        b, c = r.randint(-10, 10), r.randint(-12, 10)
        disc = b * b - 4 * a * c
        if disc > 0 and math.isqrt(disc) ** 2 != disc:
            break
    x1, x2 = (-b + math.sqrt(disc)) / (2 * a), (-b - math.sqrt(disc)) / (2 * a)
    if D >= 4 and r.random() < 0.6:
        k = r.randint(1, 6)
        lhs = f'{quad(a, b + k, c)}'
        stem = f'Solve the equation {lhs} = {term_str(k, "x")}. Give your answers correct to 2 decimal places.'
        key = f'M1 rearrange to {quad(a, b, c)} = 0; M1 x = ({num(-b)} ± √({disc})) / {2 * a}; A1 {d2(x1)}; A1 {d2(x2)}.'
    else:
        stem = f'Solve the equation {quad(a, b, c)} = 0. Show all your working and give your answers correct to 2 decimal places.'
        key = f'B1 discriminant b² − 4ac = {disc}; M1 x = ({num(-b)} ± √{disc}) / {2 * a}; A1 {d2(x1)}; A1 {d2(x2)}.'
    return Q(stem, f'x = {d2(x1)} or x = {d2(x2)}', key)


@e2.add('C3', (2, 3, 4, 5))
def e2_complete(r, D):
    if D <= 3:
        p = r.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6])
        c = r.randint(-10, 8)
        q = c - p * p
        if q >= 0:
            c -= q + 3
            q = -3
        x1, x2 = -p + math.sqrt(-q), -p - math.sqrt(-q)
        return Q(f'(a) Write {quad(1, 2 * p, c)} in the form (x + p)² + q. (b) Hence solve {quad(1, 2 * p, c)} = 0, giving your answers correct to 2 decimal places.',
                 f'(a) {bracket(p)}²{sgn(q)} (b) x = {d2(x1)} or x = {d2(x2)}',
                 f'(a) B1 p = {num(p)}; B1 q = {num(q)} (b) M1 x = {num(-p)} ± √{num(-q)}; A1 {d2(x1)}, {d2(x2)}.', type='multi_step', marks=4)
    a = r.choice([2, 3])
    p = r.choice([-3, -2, -1, 1, 2, 3])
    c = r.randint(-9, 4)
    b = 2 * a * p
    q = c - a * p * p
    tp = f'({num(-p)}, {num(q)})'
    return Q(f'Write {quad(a, b, c)} in the form a(x + p)² + q. Hence write down the coordinates of the turning point of y = {quad(a, b, c)}.',
             f'{num(a)}{bracket(p)}²{sgn(q)}; turning point {tp}', f'M1 factor out {a}: {a}(x² {"+" if p > 0 else "−"} {abs(2 * p)}x) {sgn(c).strip()}; A1 {num(a)}{bracket(p)}²; A1 q = {num(q)}; B1 turning point {tp}.')


def e2_c4(r, D):
    x = r.randint(4, 15)
    k = r.randint(2, 9)
    A = x * (x + k)
    nm = person(r)
    intro = f'{nm} designs a rectangular vegetable plot in {city(r)}. The width is x metres and the length is {k} metres more than the width. The area of the plot is {A} m².'
    diag = math.hypot(x, x + k)
    parts = [
        P(f'Show that x² + {k}x − {A} = 0.', 'x(x + ' + str(k) + f') = {A} so x² + {k}x − {A} = 0', f'M1 x(x + {k}) = {A}; A1 rearranged correctly', 2),
        P('Solve the equation to find the width of the plot.', f'x = {x} m', f'M1 (x − {x})(x + {x + k}) = 0 or formula; A1 x = {x}; B1 rejects x = {num(-(x + k))}', 3),
        P('Calculate the perimeter of the plot.', f'{2 * (2 * x + k)} m', f'M1 2({x} + {x + k}); A1 {2 * (2 * x + k)} m', 2),
        P('Calculate the length of a diagonal path across the plot.', f'{n3(diag)} m', f'M1 √({x}² + {x + k}²); A1 {n3(diag)} m', 2),
        P('Explain why one solution of the quadratic equation is rejected.', f'x = {num(-(x + k))} is negative and a width cannot be negative.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


def e2_c4b(r, D):
    u = r.choice([18, 20, 22, 24, 25, 28, 30])
    H = r.choice([10, 12, 15, 18, 20])
    while u * u - 20 * H <= 0:
        H -= 2
    t1, t2 = (u - math.sqrt(u * u - 20 * H)) / 10, (u + math.sqrt(u * u - 20 * H)) / 10
    tmax = u / 10
    hmax = u * tmax - 5 * tmax * tmax
    intro = f'A ball is kicked upwards in a stadium in {city(r)}. Its height, h metres, after t seconds is h = {u}t − 5t².'
    parts = [
        P(f'Show that when the ball is at a height of {H} m, 5t² − {u}t + {H} = 0.', f'{H} = {u}t − 5t² rearranges to 5t² − {u}t + {H} = 0', 'B1 substitution and rearrangement', 1),
        P(f'Solve 5t² − {u}t + {H} = 0, giving your answers correct to 2 decimal places.', f't = {d2(t1)} or t = {d2(t2)}', f'M1 t = ({u} ± √({u * u - 20 * H})) / 10; A1 {d2(t1)}; A1 {d2(t2)}', 3),
        P(f'Explain why the ball is at a height of {H} m at two different times.', f'The ball passes {H} m on the way up and again on the way down.', 'B1', 1),
        P('Find the time when the ball lands.', f'{ex(u / 5)} s', f'M1 t({u} − 5t) = 0; A1 t = {ex(u / 5)} s', 2),
        P('By completing the square or otherwise, find the greatest height of the ball.', f'{ex(hmax, 2)} m', f'M1 maximum at t = {ex(tmax)} (midpoint of roots); A1 h = {ex(hmax, 2)} m', 2),
    ]
    return cmp_(r, intro, parts)


e2.add('C4', (2, 3, 4, 5))(e2_c4)
e2.add('C4', (3, 4, 5))(e2_c4b)

# ---------------------------------------------------------------- linear inequalities
e3 = topic('Linear inequalities and the number line', 'linear inequalities', 'representing them on a number line', 'inequalities number line')
e3.fixed('C1', (1, 2), [
    ('On a number line, x > 3 is shown with', 'an open circle at 3 and an arrow to the right', 'Open circle: 3 not included; arrow to the right: greater values.', ['a filled circle at 3 and an arrow to the right', 'an open circle at 3 and an arrow to the left', 'a filled circle at 3 and an arrow to the left']),
    ('Which inequality does a filled circle at −2 with an arrow to the left represent?', 'x ≤ −2', 'Filled circle: −2 included; arrow left: smaller values.', ['x < −2', 'x ≥ −2', 'x > −2']),
    ('What must you do to the inequality sign when you multiply or divide both sides by a negative number?', 'Reverse it', 'For example −2x < 6 gives x > −3.', ['Keep it the same', 'Change it to an equals sign', 'Remove it']),
    ('Which integers satisfy −2 < n ≤ 2?', '−1, 0, 1, 2', '−2 is excluded (strict), 2 is included.', ['−2, −1, 0, 1, 2', '−2, −1, 0, 1', '−1, 0, 1']),
    ('Solve 3x − 5 > 7.', 'x > 4', '3x > 12, so x > 4.', ['x > 2/3', 'x < 4', 'x > 12']),
])
e3.fixed('C2', (2, 3), [
    ('Explain why the inequality sign must be reversed when dividing both sides by a negative number. Use 2 < 5 as an example.', '2 < 5 but −2 > −5: multiplying by −1 reverses the order of numbers on the number line, so the sign must be reversed.', 'B1 numerical illustration; B1 order reverses [2]'),
    ('Explain the difference between x < 4 and x ≤ 4 on a number line.', 'x < 4 uses an open circle at 4 (4 not included); x ≤ 4 uses a filled circle (4 included).', 'B1 open vs filled; B1 included/not included [2]'),
    ('Explain why −3 < x < 5 can be written as a single statement but x < −3 or x > 5 cannot.', 'The first describes one interval between −3 and 5; the second describes two separate regions, so they cannot be combined into one double inequality.', 'B1 single interval; B1 two separate regions [2]'),
    ('Describe how to find the integer values that satisfy 7 ≤ 2n + 1 < 15.', 'Subtract 1 throughout (6 ≤ 2n < 14), divide by 2 (3 ≤ n < 7), so n = 3, 4, 5, 6.', 'B1 operate on all three parts; B1 correct list [2]'),
])


@e3.add('C1', (1, 2, 3))
def e3_list(r, D):
    a = r.randint(-6, 3)
    b = a + r.randint(3, 6)
    sa, sb = r.choice(['<', '≤']), r.choice(['<', '≤'])
    lo = a + 1 if sa == '<' else a
    hi = b - 1 if sb == '<' else b
    c = ', '.join(num(i) for i in range(lo, hi + 1))
    ds = [', '.join(num(i) for i in range(a, b + 1)), ', '.join(num(i) for i in range(a + 1, b)), ', '.join(num(i) for i in range(lo, hi + 2)), ', '.join(num(i) for i in range(lo - 1, hi + 1)), ', '.join(num(i) for i in range(lo + 1, hi + 1))]
    return SMC(r, f'List the integers n such that {num(a)} {sa} n {sb} {num(b)}.', c, ds, f'{"Exclude" if sa == "<" else "Include"} {num(a)}; {"exclude" if sb == "<" else "include"} {num(b)}: {c}.')


@e3.add('C2', (2, 3, 4), 'explain')
def e3_err(r, D):
    a = r.randint(2, 6)
    b = r.randint(-8, 10)
    x0 = r.randint(-4, 6)
    c = b - a * x0
    nm = person(r)
    return Q(f'{nm} solves {num(b)} − {term_str(a, "x")} > {num(c)} and writes {MINUS}{term_str(a, "x")} > {num(c - b)}, so x > {num(x0)}. Explain the error and give the correct solution.',
             f'Dividing by {MINUS}{a} reverses the inequality: x < {num(x0)}.', f'B1 sign must reverse when dividing by a negative; B1 x < {num(x0)} [2]')


@e3.add('C3', (1, 2, 3, 4, 5))
def e3_solve(r, D):
    if D <= 2:
        a = r.randint(2, 7)
        x0 = r.randint(-5, 9)
        b = r.randint(-9, 12)
        s = r.choice(['<', '>', '≤', '≥'])
        stem = f'Solve the inequality {lin(a, b)} {s} {num(a * x0 + b)}.'
        if D == 1:
            return MC(r, stem.replace('Solve the inequality', 'Solve'), x0, [x0 + 1, -x0 if x0 else 2, (a * x0 + b) / a if b else x0 - 2, a * x0 + b], f'Subtract {num(b)} then divide by {a}: x {s} {num(x0)}.', fmtf=lambda v: f'x {s} {num(v)}')
        return Q(stem, f'x {s} {num(x0)}', f'M1 {term_str(a, "x")} {s} {num(a * x0)}; A1 x {s} {num(x0)}.')
    if D == 3:
        c = r.randint(1, 5)
        a = c + r.randint(1, 5)
        x0 = r.randint(-4, 8)
        b = r.randint(-10, 10)
        d = (a - c) * x0 + b
        s = r.choice(['<', '>', '≤', '≥'])
        flip = {'<': '>', '>': '<', '≤': '≥', '≥': '≤'}
        if r.random() < 0.5:
            return Q(f'Solve {lin(c, d)} {s} {lin(a, b)}.', f'x {flip[s]} {num(x0)}', f'M1 collect x terms: {num(d - b)} {s} {term_str(a - c, "x")}; A1 x {flip[s]} {num(x0)} (or {num(x0)} {s} x).')
        return Q(f'Solve {lin(a, b)} {s} {lin(c, d)}.', f'x {s} {num(x0)}', f'M1 {term_str(a - c, "x")} {s} {num(d - b)}; A1 x {s} {num(x0)}.')
    # double inequality with list
    a = r.randint(2, 5)
    b = r.randint(-7, 7)
    lo, hi = r.randint(-4, 1), r.randint(3, 7)
    L, U = a * lo + b - r.randint(0, a - 1), a * hi + b + r.randint(0, a - 1)
    # integers n with L <= a n + b < U
    sol = [n for n in range(-30, 30) if L <= a * n + b < U]
    return Q(f'Solve {num(L)} ≤ {lin(a, b)} < {num(U)} and list the integer values of x that satisfy it.',
             f'{frac(Fr(L - b, a))} ≤ x < {frac(Fr(U - b, a))}; x = ' + ', '.join(num(n) for n in sol),
             f'M1 subtract {num(b)} from all parts; M1 divide all parts by {a}; A1 {frac(Fr(L - b, a))} ≤ x < {frac(Fr(U - b, a))}; A1 list.')


@e3.add('C3', (3, 4, 5))
def e3_frac(r, D):
    a, d = r.randint(2, 5), r.randint(2, 4)
    b = r.randint(-5, 6)
    c = r.randint(1, 3)
    e = r.randint(-6, 6)
    # (a x + b)/d >= c x + e  ->  a x + b >= d c x + d e  -> (a - dc) x >= de - b
    k = a - d * c
    if k == 0:
        a += 1
        k = 1
    rhs = d * e - b
    bound = Fr(rhs, k)
    s = '≥' if k > 0 else '≤'
    return Q(f'Solve the inequality ({lin(a, b)}) / {d} ≥ {lin(c, e)}.', f'x {s} {frac(bound)}',
             f'M1 multiply by {d}: {lin(a, b)} ≥ {lin(d * c, d * e)}; M1 {term_str(k, "x") if k > 0 else MINUS + term_str(-k, "x")} ≥ {num(rhs)}; A1 x {s} {frac(bound)}' + (' (sign reversed when dividing by a negative)' if k < 0 else '') + '.')


def e3_c4(r, D):
    nm = person(r)
    fix = r.choice([3.5, 4, 4.5, 5])
    per = r.choice([1.2, 1.5, 1.8, 2.2, 2.5])
    budget = r.choice([30, 35, 40, 45, 50])
    nmax = math.floor((budget - fix) / per + 1e-9)
    minimum = r.choice([5, 6, 8])
    intro = f'A taxi company in {city(r)} charges a fixed fee of ${fix:.2f} plus ${per:.2f} per kilometre. {nm} has at most ${budget} to spend on a journey of k kilometres, where k is a whole number.'
    parts = [
        P('Write down an inequality in k.', f'{ex(fix)} + {ex(per)}k ≤ {budget}', 'B1', 1),
        P('Solve your inequality.', f'k ≤ {n3((budget - fix) / per)}', f'M1 {ex(per)}k ≤ {ex(budget - fix)}; A1', 2),
        P('Find the greatest number of kilometres the journey can be.', f'{nmax} km', 'B1 rounds down', 1),
        P(f'The journey must also be at least {minimum} km. Show the possible values of k on a number line and list them.', f'{minimum} ≤ k ≤ {nmax}: ' + ', '.join(str(i) for i in range(minimum, nmax + 1)),
          'B1 filled circles at both ends joined; B1 list', 2),
        P(f'Explain why the answer to the greatest distance is rounded down and not up.', f'A whole number of km greater than {ex(round((budget - fix) / per, 2))} would cost more than ${budget}.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


e3.add('C4', (2, 3, 4, 5))(e3_c4)

# ---------------------------------------------------------------- regions
e4 = topic('Regions defined by inequalities', 'regions in the cartesian plane', 'defined by inequalities', 'regions')
e4.fixed('C1', (1, 2), [
    ('Which inequality describes the region above the line y = 2x + 1, not including the line?', 'y > 2x + 1', 'Above the line: greater y-values; not including: strict.', ['y < 2x + 1', 'y ≥ 2x + 1', 'y ≤ 2x + 1']),
    ('When drawing the region y ≤ 3, how should the line y = 3 be drawn?', 'As a solid line', 'The line is included (≤), so it is solid; a strict inequality uses a broken line.', ['As a broken (dashed) line', 'It should not be drawn', 'As a curve']),
    ('Which region is described by x < −1?', 'To the left of the vertical line x = −1', 'x-values less than −1 lie to the left.', ['To the right of x = −1', 'Below the line y = −1', 'Above the line y = −1']),
    ('Which point lies in the region x + y < 5?', '(2, 1)', '2 + 1 = 3 < 5.', ['(3, 2)', '(4, 3)', '(6, 0)']),
    ('A boundary line is drawn as a broken line. What does this tell you?', 'Points on the line are not included', 'Broken line ↔ strict inequality (< or >).', ['Points on the line are included', 'The line has a negative gradient', 'The region is unbounded']),
])
e4.fixed('C2', (2, 3), [
    ('Explain how to decide which side of the line 3x + 2y = 12 represents 3x + 2y < 12.', 'Test a point not on the line, such as (0, 0): 0 < 12 is true, so the region containing the origin is 3x + 2y < 12.', 'B1 test a point; B1 conclusion [2]'),
    ('Explain why the line y = x is drawn broken for the region y > x but solid for y ≥ x.', 'For y > x the points on the line (where y = x) are not included, shown by a broken line; for y ≥ x they are included, shown solid.', 'B1 strict/not strict; B1 broken/solid meaning [2]'),
    ('Explain why (0, 0) cannot be used as a test point for the region y > 2x.', '(0, 0) lies on the line y = 2x, so it does not show which side is which; use a point such as (0, 1).', 'B1 origin on the line; B1 choose another point [2]'),
])


@e4.add('C1', (1, 2, 3))
def e4_pt(r, D):
    m, c = r.choice([-2, -1, 1, 2, 3]), r.randint(-3, 4)
    s = r.choice(['<', '>', '≤', '≥'])
    pts = [(x, y) for x in range(-3, 5) for y in range(-4, 8)]
    ok = lambda p: {'<': p[1] < m * p[0] + c, '>': p[1] > m * p[0] + c, '≤': p[1] <= m * p[0] + c, '≥': p[1] >= m * p[0] + c}[s]
    good = [p for p in pts if ok(p) and p[1] != m * p[0] + c]
    bad = [p for p in pts if not ok(p)]
    g = r.choice(good)
    b = r.sample(bad, 3)
    f = lambda p: f'({num(p[0])}, {num(p[1])})'
    return SMC(r, f'Which point satisfies the inequality y {s} {lin(m, c)}?', f(g), [f(p) for p in b], f'Substitute: at {f(g)}, y = {num(g[1])} and {lin(m, c)} = {num(m * g[0] + c)}, so y {s} {lin(m, c)} is true.')


@e4.add('C2', (2, 3, 4), 'explain')
def e4_err(r, D):
    a, b, c = r.randint(1, 4), r.randint(1, 4), r.randint(6, 16)
    nm = person(r)
    x0, y0 = r.randint(1, 5), r.randint(1, 5)
    v = a * x0 + b * y0
    s = r.choice(['<', '>'])
    truth = (v < c) if s == '<' else (v > c)
    claim = not truth
    if v == c:
        claim = True
        truth = False
    return Q(f'{nm} says the point ({x0}, {y0}) lies in the region {expr((a, "x"), (b, "y"))} {s} {c}. Explain whether {nm} is correct.',
             f'{"Correct" if truth else "Not correct"}: {a}({x0}) + {b}({y0}) = {v}, and {v} {s} {c} is {"true" if truth else "false"}.',
             f'M1 substitutes the point to get {v}; A1 compares with {c} and concludes [2]')


@e4.add('C3', (2, 3, 4))
def e4_list(r, D):
    a, b = r.randint(0, 2), r.randint(0, 2)
    c = r.randint(a + b + 3, a + b + 6)
    extra = D >= 3
    m = r.choice([1, 2])
    pts = [(x, y) for x in range(-2, 12) for y in range(-2, 12) if x >= a and y > b and x + y <= c and (not extra or y <= m * x)]
    cond = f'x ≥ {a}, y > {b}, x + y ≤ {c}' + (f' and y ≤ {term_str(m, "x")}' if extra else '')
    lst = ', '.join(f'({x}, {y})' for x, y in pts)
    return Q(f'The region R is defined by the inequalities {cond}. List all the points with integer coordinates that lie in R.', lst if lst else 'none',
             f'B1 uses boundaries correctly (y > {b} excludes y = {b}); B2 for the complete list of {len(pts)} points (B1 for at least half correct with no extras).')


@e4.add('C3', (3, 4, 5))
def e4_find(r, D):
    x1, y1 = 0, r.randint(3, 8)
    x2 = r.randint(3, 8)
    y2 = 0
    # line through (0, y1) and (x2, 0): y1 x + x2 y = x1*y2... -> y1 x + x2 y = y1 x2
    g = math.gcd(math.gcd(y1, x2), y1 * x2)
    A, B, C = y1 // g, x2 // g, y1 * x2 // g
    k = r.randint(1, min(y1, x2) - 1)
    return Q(f'The region R is bounded by the lines x = 0, y = 0 and the straight line through (0, {y1}) and ({x2}, 0). R includes all of its boundaries. Write down the three inequalities that define R.',
             f'x ≥ 0, y ≥ 0, {expr((A, "x"), (B, "y"))} ≤ {C}', f'B1 x ≥ 0; B1 y ≥ 0; M1 line gradient {frac(Fr(-y1, x2))}, equation {expr((A, "x"), (B, "y"))} = {C}; A1 ≤ with origin side.')


def e4_c4(r, D):
    pa, pb = r.choice([(3, 2), (4, 3), (5, 2), (6, 4), (5, 3)])
    budget = r.choice([24, 30, 36, 40, 42, 48])
    maxn = r.choice([8, 9, 10, 12])
    proa, prob = r.choice([(2, 1), (3, 2), (5, 3), (4, 1)])
    A, B = r.choice([('packs of pens', 'notebooks'), ('mangoes', 'papayas'), ('cupcakes', 'cookies'), ('plant pots', 'seed packets')])
    pts = [(x, y) for x in range(0, 40) for y in range(0, 40) if pa * x + pb * y <= budget and x + y <= maxn and x >= 1 and y >= 2]
    best = max(pts, key=lambda p: (proa * p[0] + prob * p[1], p[0]))
    bv = proa * best[0] + prob * best[1]
    ties = [p for p in pts if proa * p[0] + prob * p[1] == bv]
    nm = person(r)
    intro = f'{nm} runs a stall at a school fair in {city(r)} and buys x {A} at ${pa} each and y {B} at ${pb} each. {nm} spends no more than ${budget}, buys at most {maxn} items in total, at least 1 of the {A} and at least 2 of the {B}.'
    parts = [
        P(f'Show that {pa}x + {pb}y ≤ {budget}.', f'Cost {pa}x + {pb}y must not exceed {budget}.', 'B1', 1),
        P('Write down the other three inequalities.', f'x + y ≤ {maxn}, x ≥ 1, y ≥ 2', 'B1 B1', 2),
        P('Find the number of different combinations (x, y) that are possible.', f'{len(pts)}', f'M1 lists integer points in the region; A1 {len(pts)}', 2),
        P(f'Each of the {A} gives a profit of ${proa} and each of the {B} gives a profit of ${prob}. Find the greatest possible profit and the values of x and y that give it.',
          f'${bv} with ' + ' or '.join(f'x = {p[0]}, y = {p[1]}' for p in ties), f'M1 evaluates {proa}x + {prob}y at vertices/points of region; A1 ${bv}; A1 point', 3),
    ]
    return cmp_(r, intro, parts)


e4.add('C4', (2, 3, 4, 5))(e4_c4)

# ---------------------------------------------------------------- algebraic fractions
e5 = topic('Algebraic fractions', 'algebraic fractions', 'simplifying, adding, multiplying and solving equations', 'fractions algebraic')
e5.fixed('C1', (1, 2), [
    ('Simplify 6x²/(9x).', '2x/3', 'Divide numerator and denominator by 3x.', ['2x²/3', '3x/2', '2/(3x)']),
    ('Simplify (x² − 9)/(x + 3).', 'x − 3', 'x² − 9 = (x + 3)(x − 3); cancel (x + 3).', ['x + 3', 'x − 9', 'x² − 3']),
    ('Which is equal to 1/x + 1/y?', '(x + y)/(xy)', 'Common denominator xy: y/(xy) + x/(xy).', ['2/(x + y)', '1/(x + y)', '(x + y)/2']),
    ('Simplify (3/x) × (x²/6).', 'x/2', '3x²/(6x) = x/2.', ['x²/2', '2/x', '3x/6x²']),
    ('Simplify (4/x) ÷ (2/x²).', '2x', '(4/x) × (x²/2) = 2x.', ['8/x³', '2/x', 'x/2']),
])
e5.fixed('C2', (2, 3), [
    ('Explain why (x + 6)/x cannot be simplified to 6 by cancelling the x.', 'You can only cancel common factors. x is a term of the numerator, not a factor of the whole numerator; e.g. x = 2 gives 8/2 = 4, not 6.', 'B1 only factors cancel; B1 counter-example [2]'),
    ('Explain why x = 3 cannot be a solution of an equation containing 5/(x − 3).', 'When x = 3 the denominator is 0 and division by zero is undefined.', 'B1 denominator zero; B1 undefined [2]'),
    ('Explain the first step when adding 2/(x + 1) and 3/(x − 2).', 'Write both over the common denominator (x + 1)(x − 2): 2(x − 2) + 3(x + 1) over (x + 1)(x − 2).', 'B1 common denominator; B1 numerators adjusted [2]'),
    ('Explain why it is useful to factorise both numerator and denominator before simplifying an algebraic fraction.', 'Factorising shows common factors, which are the only things that can be cancelled.', 'B1 reveals factors; B1 only common factors cancel [2]'),
])


def fq(p, q):
    """(x+p)(x+q) expanded."""
    return quad(1, p + q, p * q)


@e5.add('C1', (1, 2, 3))
def e5_simp(r, D):
    p, q = r.sample([-7, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 8], 2)
    c = f'{bracket(q)}'.strip('()') if q else 'x'
    c = lin(1, q)
    ds = [lin(1, p), lin(1, -q), f'{lin(1, q)}/{lin(1, p)}', lin(1, p + q), lin(1, p * q)]
    return SMC(r, f'Simplify ({fq(p, q)}) / ({lin(1, p)}).', c, ds, f'{fq(p, q)} = {bracket(p)}{bracket(q)}; cancel {bracket(p)} to leave {c}.')


@e5.add('C2', (2, 3, 4), 'explain')
def e5_err(r, D):
    nm = person(r)
    a, b = r.randint(2, 7), r.randint(2, 9)
    if r.random() < 0.5:
        return Q(f'{nm} simplifies ({lin(1, a)})/({lin(1, b)}) to {frac(Fr(a, b))} by cancelling the x terms. Explain why this is wrong.',
                 f'x is not a common factor of the numerator and the denominator, so it cannot be cancelled; e.g. x = 1 gives {frac(Fr(1 + a, 1 + b))}, not {frac(Fr(a, b))}. The fraction does not simplify.',
                 'B1 only common factors cancel; B1 counter-example or conclusion [2]')
    c, d = r.randint(2, 6), r.randint(2, 6)
    return Q(f'{nm} adds {a}/x + {c}/(x + {d}) and writes {a + c}/(2x + {d}). Explain the error and give the correct single fraction.',
             f'Fractions are added over a common denominator, not by adding numerators and denominators. Correct: ({lin(a + c, a * d)})/(x(x + {d})).',
             f'B1 identifies error; M1 common denominator x(x + {d}); A1 ({lin(a + c, a * d)})/(x(x + {d})) [3]', marks=3)


@e5.add('C3', (2, 3, 4, 5))
def e5_simp2(r, D):
    p, q, s = r.sample([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 7], 3)
    if q == -p:
        q = q + 1 if q + 1 not in (0, -p, p) else q + 2
    if D <= 3:
        num_ = fq(p, q)
        den = fq(p, s)
        return Q(f'Simplify fully ({num_}) / ({den}).', f'({lin(1, q)})/({lin(1, s)})', f'M1 numerator {bracket(p)}{bracket(q)}; M1 denominator {bracket(p)}{bracket(s)}; A1 ({lin(1, q)})/({lin(1, s)}).')
    k = r.choice([2, 3])
    num_ = quad(k, k * (p + q), k * p * q)
    den = quad(1, 0, -p * p) if p > 0 else quad(1, 0, -p * p)
    # denominator x² - p² = (x - p)(x + p) ; common factor (x + p)
    return Q(f'Simplify fully ({num_}) / ({den}).', f'{k}({lin(1, q)})/({lin(1, -p)})',
             f'M1 numerator {k}{bracket(p)}{bracket(q)}; M1 denominator {bracket(p)}{bracket(-p)}; A1 {k}({lin(1, q)})/({lin(1, -p)}).')


@e5.add('C3', (2, 3, 4))
def e5_add(r, D):
    a, b = r.randint(1, 6), r.randint(1, 6)
    p, q = r.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
    op = r.choice(['+', '−']) if D >= 3 else '+'
    sb = b if op == '+' else -b
    numer = lin(a + sb, a * q + sb * p)
    return Q(f'Write as a single fraction in its simplest form: {a}/{bracket(p)} {op} {b}/{bracket(q)}.', f'({numer})/({bracket(p)}{bracket(q)})',
             f'M1 common denominator {bracket(p)}{bracket(q)}; M1 {a}{bracket(q)} {op} {b}{bracket(p)}; A1 ({numer})/({bracket(p)}{bracket(q)}).')


@e5.add('C3', (2, 3, 4, 5))
def e5_solve(r, D):
    if D <= 3:
        m, n = r.sample([2, 3, 4, 5], 2)
        x = r.randint(-5, 12)
        p, q = r.randint(-6, 6), r.randint(-6, 6)
        # (x+p)/m + (x+q)/n = k  with k rational -> choose so k integer
        for _ in range(60):
            tot = Fr(x + p, m) + Fr(x + q, n)
            if tot.denominator == 1:
                break
            p, q = r.randint(-6, 6), r.randint(-6, 6)
        return Q(f'Solve the equation ({lin(1, p)})/{m} + ({lin(1, q)})/{n} = {frac(tot)}.', f'x = {num(x)}',
                 f'M1 multiply by {m * n}: {n}({lin(1, p)}) + {m}({lin(1, q)}) = {frac(tot * m * n)}; M1 {lin(m + n, n * p + m * q)} = {frac(tot * m * n)}; A1 x = {num(x)}.')
    for _ in range(400):
        a, b = r.randint(1, 8), r.randint(1, 8)
        p, q = r.randint(-4, 5), r.randint(-4, 5)
        if p == q:
            continue
        # a/(x+p) + b/(x+q) = 1 -> x² + (p+q-a-b)x + pq - aq - bp = 0
        B, C = p + q - a - b, p * q - a * q - b * p
        disc = B * B - 4 * C
        if disc <= 0 or math.isqrt(disc) ** 2 != disc:
            continue
        s = math.isqrt(disc)
        if (-B + s) % 2:
            continue
        x1, x2 = (-B + s) // 2, (-B - s) // 2
        if x1 in (-p, -q) or x2 in (-p, -q) or x1 == x2:
            continue
        return Q(f'Solve the equation {a}/{bracket(p)} + {b}/{bracket(q)} = 1.', f'x = {num(x1)} or x = {num(x2)}',
                 f'M1 multiply by {bracket(p)}{bracket(q)}: {a}{bracket(q)} + {b}{bracket(p)} = {bracket(p)}{bracket(q)}; M1 {quad(1, B, C)} = 0; M1 factorise/formula; A1 x = {num(x1)}, {num(x2)}.')
    return None


def e5_c4(r, D):
    for _ in range(500):
        x = r.randint(6, 24)
        k = r.choice([2, 3, 4, 5, 6, 10])
        d1, d2 = r.choice(range(10, 65, 5)), r.choice(range(10, 65, 5))
        T = Fr(d1, x) + Fr(d2, x + k)
        if (T * 4).denominator == 1 and T < 8:
            break
    else:
        return None
    nm = person(r)
    Tm = T * 4
    # T x² + (T k - d1 - d2) x - d1 k = 0 ; times 4
    A, B, C = Tm, Tm * k - 4 * (d1 + d2), -4 * d1 * k
    g = math.gcd(math.gcd(int(A), int(B)), int(C))
    A, B, C = int(A) // g, int(B) // g, int(C) // g
    other = Fr(C, A) / x
    intro = f'{nm} cycles {d1} km at an average speed of x km/h and then {d2} km at an average speed of (x + {k}) km/h. The total time taken is {ex(float(T))} hours.'
    parts = [
        P(f'Write down an equation in x.', f'{d1}/x + {d2}/(x + {k}) = {ex(float(T))}', 'B1 time = distance ÷ speed for both parts', 1),
        P(f'Show that x satisfies the equation {quad(A, B, C)} = 0.', f'{quad(A, B, C)} = 0', f'M1 multiply by x(x + {k}); M1 expand and collect; A1 correct equation', 3),
        P('Solve the equation and find the speed for the first part of the journey.', f'x = {x} km/h', f'M1 factorise/formula; A1 x = {x}; B1 rejects x = {frac(other)} (negative)', 3),
        P('Calculate the time taken for the second part of the journey, in hours and minutes.', dur(round(d2 / (x + k) * 60)), f'M1 {d2} ÷ {x + k}; A1 {dur(round(d2 / (x + k) * 60))}', 2),
    ]
    return cmp_(r, intro, parts)


e5.add('C4', (2, 3, 4, 5))(e5_c4)
CHAPTERS[2] = [e1, e2, e3, e4, e5]


# =========================================================== 3 Scale drawings, bearings and trigonometry (Ch 15)
def brg(x):
    return f'{round(x) % 360:03d}°'


def brg1(x):
    x = x % 360
    s = f'{x:.1f}'
    return ('0' * (5 - len(s))) + s + '°'


def sind(x):
    return math.sin(math.radians(x))


def cosd(x):
    return math.cos(math.radians(x))


def tand(x):
    return math.tan(math.radians(x))


def bearing_of(dx, dy):
    return math.degrees(math.atan2(dx, dy)) % 360


t31 = topic('Scale drawings and bearings', 'scale drawings', 'three-figure bearings', 'bearings')
t31.fixed('C1', (1, 2), [
    ('What is the three-figure bearing of north-east?', '045°', 'North-east is halfway between north (000°) and east (090°).', ['45°', '135°', '315°']),
    ('The bearing of B from A is 070°. What is the bearing of A from B?', '250°', 'Back bearing: 070° + 180° = 250°.', ['110°', '290°', '070°']),
    ('A map has a scale of 1 : 50 000. What real distance is represented by 4 cm on the map?', '2 km', '4 × 50 000 = 200 000 cm = 2000 m = 2 km.', ['20 km', '200 m', '0.2 km']),
    ('Bearings are measured', 'clockwise from north', 'Three-figure bearings: clockwise from the north line.', ['anticlockwise from north', 'clockwise from east', 'anticlockwise from south']),
    ('What is the three-figure bearing of due west?', '270°', 'West is three right angles clockwise from north.', ['090°', '180°', '027°']),
    ('On a scale drawing 1 cm represents 5 m. How long is a 32 m wall on the drawing?', '6.4 cm', '32 ÷ 5 = 6.4 cm.', ['160 cm', '3.2 cm', '0.64 cm']),
])
t31.fixed('C2', (2, 3), [
    ('Explain why a bearing of 45° is written as 045°.', 'Bearings are always written with three figures so that they cannot be misread; zeros fill the empty places.', 'B1 three figures convention; B1 avoids misreading [2]'),
    ('Explain why the bearing of A from B differs from the bearing of B from A by 180°.', 'The two directions are opposite along the same line; the north lines at A and B are parallel, so the angles differ by 180° (co-interior/alternate angles).', 'B1 opposite directions; B1 parallel north lines [2]'),
    ('A map scale is 1 : 25 000. Explain why 1 cm on the map represents 250 m.', '1 cm on the map represents 25 000 cm in real life, and 25 000 cm = 250 m.', 'B1 25 000 cm; B1 convert to 250 m [2]'),
    ('Describe how to draw a bearing of 230° from a point P on a scale drawing.', 'Draw a north line at P, place the protractor on P and measure 230° clockwise from north (180° + 50°), then draw the line.', 'B1 north line at P; B1 clockwise 230° [2]'),
])


@t31.add('C1', (1, 2, 3))
def t31_back(r, D):
    th = r.randint(5, 355)
    if th in (180, 0):
        th = 125
    b = (th + 180) % 360
    return MC(r, f'The bearing of Q from P is {brg(th)}. What is the bearing of P from Q?', b, [(180 - th) % 360, (360 - th) % 360, th, (th + 90) % 360], f'{brg(th)} {"+" if th < 180 else "−"} 180° = {brg(b)}.', fmtf=lambda x: brg(x))


@t31.add('C2', (2, 3, 4), 'explain')
def t31_err(r, D):
    nm = person(r)
    if r.random() < 0.5:
        th = r.choice([35, 48, 62, 115, 128, 140, 205, 238, 300, 322])
        wrong = (180 - th) % 360 if th < 180 else th - 90
        return Q(f'The bearing of a lighthouse L from a boat B is {brg(th)}. {nm} says the bearing of B from L is {brg(wrong)}. Explain why {nm} is wrong and give the correct bearing.',
                 f'The back bearing is found by adding or subtracting 180°: {brg((th + 180) % 360)}.', f'B1 method ± 180°; B1 {brg((th + 180) % 360)} [2]')
    s = r.choice([20000, 25000, 50000, 100000])
    cm = r.choice([3, 4.5, 6, 7.2, 8.4])
    real_m = cm * s / 100
    return Q(f'A map has a scale of 1 : {s:,}. {nm} says {ex(cm)} cm on the map represents {ex(cm * s / 1000)} m. Explain the mistake and find the correct distance in kilometres.',
             f'{ex(cm)} × {s:,} = {ex(cm * s)} cm; there are 100 cm in a metre, so this is {ex(real_m)} m = {ex(real_m / 1000)} km.', f'B1 converts cm to m by ÷ 100 (not ÷ 1000); B1 {ex(real_m / 1000)} km [2]')


@t31.add('C3', (1, 2, 3))
def t31_scale(r, D):
    s = r.choice([10000, 20000, 25000, 50000, 200000])
    if r.random() < 0.5:
        cm = r.choice([2.5, 3.4, 4.8, 6.2, 7.5, 9])
        km = cm * s / 100000
        stem = f'A map of the area around {city(r)} has a scale of 1 : {s:,}. Two villages are {ex(cm)} cm apart on the map. Calculate the actual distance between them in kilometres.'
        if D == 1:
            return MC(r, stem.replace('Calculate the actual distance between them in kilometres.', 'What is the actual distance between them?'), km, [km * 10, km / 10, km * 100, cm * s / 1000], f'{ex(cm)} × {s:,} = {ex(cm * s)} cm = {ex(km)} km.', fmtf=ex, unit=' km')
        return Q(stem, f'{ex(km)} km', f'M1 {ex(cm)} × {s:,} = {ex(cm * s)} cm; A1 {ex(km)} km.')
    km = r.choice([1.2, 2.5, 3.6, 4.5, 7, 12])
    cm = km * 100000 / s
    return Q(f'A map has a scale of 1 : {s:,}. A straight road is {ex(km)} km long. Calculate the length of the road on the map, in centimetres.', f'{ex(cm)} cm',
             f'M1 {ex(km)} km = {ex(km * 100000)} cm; A1 ÷ {s:,} = {ex(cm)} cm.')


@t31.add('C3', (3, 4, 5))
def t31_comp(r, D):
    th = r.choice([32, 47, 58, 124, 137, 152, 213, 228, 246, 304, 318, 335])
    d = r.choice([12, 15, 18, 24, 35, 42, 56])
    N, E = d * cosd(th), d * sind(th)
    nm = person(r)
    if D == 3:
        a, b = r.randint(3, 15), r.randint(3, 15)
        dirs = r.choice([('north', 'east'), ('south', 'east'), ('north', 'west'), ('south', 'west')])
        dx = b if dirs[1] == 'east' else -b
        dy = a if dirs[0] == 'north' else -a
        bb = bearing_of(dx, dy)
        return Q(f'{nm} walks {a} km due {dirs[0]} and then {b} km due {dirs[1]}. Calculate the bearing of {nm}\'s final position from the starting point.', brg1(bb),
                 f'M1 tan θ = {b}/{a}, θ = {ex(round(math.degrees(math.atan(b / a)), 1))}°; M1 converts to a bearing; A1 {brg1(bb)}.')
    return Q(f'A ship sails {d} km on a bearing of {brg(th)} from a port. Calculate how far (a) {"north" if N >= 0 else "south"} and (b) {"east" if E >= 0 else "west"} of the port the ship is.',
             f'(a) {n3(abs(N))} km (b) {n3(abs(E))} km', f'M1 uses the angle {brg(th)} with the north line; (a) M1 {d} × cos; A1 {n3(abs(N))} km (b) M1 {d} × sin; A1 {n3(abs(E))} km.', type='multi_step')


def t31_c4(r, D):
    th1, th2 = r.choice([(40, 130), (65, 155), (120, 210), (30, 300), (75, 165), (210, 300), (150, 60)])
    a, b = r.choice([20, 24, 30, 36, 45]), r.choice([15, 18, 25, 32, 40])
    x = a * sind(th1) + b * sind(th2)
    y = a * cosd(th1) + b * cosd(th2)
    dist = math.hypot(x, y)
    back = bearing_of(-x, -y)
    s = r.choice([200000, 500000, 250000])
    nm = person(r)
    intro = f'A boat leaves harbour H and sails {a} km on a bearing of {brg(th1)} to a buoy B. It then sails {b} km on a bearing of {brg(th2)} to an island I. The angle HBI is 90°.'
    parts = [
        P('Write down the bearing of H from B.', brg(th1 + 180), 'B1', 1),
        P('Calculate the distance HI.', f'{n3(dist)} km', f'M1 √({a}² + {b}²); A1 {n3(dist)} km', 2),
        P('Calculate the bearing of I from H.', brg1(bearing_of(x, y)), f'M1 tan(BHI) = {b}/{a}, angle BHI = {ex(round(math.degrees(math.atan(b / a)), 1))}°; M1 {"adds to" if ((th2 - th1) % 360) == 90 else "subtracts from"} {brg(th1)}; A1 {brg1(bearing_of(x, y))}', 3),
        P('Calculate the bearing of H from I.', brg1(back), f'M1 bearing of I from H ± 180°; A1 {brg1(back)}', 2),
        P(f'A chart of the area has scale 1 : {s:,}. Calculate the length of HB on the chart.', f'{ex(a * 100000 / s)} cm', f'M1 {a} km = {a * 100000:,} cm ÷ {s:,}; A1 {ex(a * 100000 / s)} cm', 2),
    ]
    return cmp_(r, intro, parts)


t31.add('C4', (2, 3, 4, 5))(t31_c4)

# ---------------------------------------------------------------- right-angled trigonometry
t32 = topic('Right-angled trigonometry', 'right-angled trigonometry', 'sine, cosine and tangent ratios', 'trigonometric ratios')
t32.fixed('C1', (1, 2), [
    ('In a right-angled triangle, sin θ is equal to', 'opposite ÷ hypotenuse', 'SOH: sin = opp/hyp.', ['adjacent ÷ hypotenuse', 'opposite ÷ adjacent', 'hypotenuse ÷ opposite']),
    ('In a right-angled triangle, tan θ is equal to', 'opposite ÷ adjacent', 'TOA: tan = opp/adj.', ['adjacent ÷ opposite', 'opposite ÷ hypotenuse', 'adjacent ÷ hypotenuse']),
    ('What is the exact value of tan 45°?', '1', 'In an isosceles right-angled triangle opposite = adjacent.', ['0', '0.5', '√2']),
    ('What is the exact value of cos 60°?', '1/2', 'From an equilateral triangle of side 2 cut in half: adj 1, hyp 2.', ['√3/2', '1', '√2/2']),
    ('You know the hypotenuse and want the side adjacent to angle θ. Which ratio do you use?', 'cosine', 'CAH: cos θ = adj/hyp.', ['sine', 'tangent', 'Pythagoras only']),
    ('Which side of a right-angled triangle is always the longest?', 'The hypotenuse', 'The hypotenuse is opposite the right angle.', ['The opposite side', 'The adjacent side', 'It depends on the angle']),
])
t32.fixed('C2', (2, 3), [
    ('Explain why sin θ can never be greater than 1 in a right-angled triangle.', 'sin θ = opposite/hypotenuse and the hypotenuse is always the longest side, so the fraction is less than 1.', 'B1 definition; B1 hypotenuse longest [2]'),
    ('Explain how you decide which trigonometric ratio to use to find a missing side.', 'Label the sides relative to the given angle; choose the ratio that uses the side you know and the side you want (SOH CAH TOA).', 'B1 label opp/adj/hyp; B1 choose ratio containing known and unknown [2]'),
    ('A student gets cos 60° = −0.952 on a calculator. Explain what has gone wrong.', 'The calculator is in radian mode; in degree mode cos 60° = 0.5.', 'B1 radian mode; B1 correct value 0.5 [2]'),
    ('Explain why tan θ increases as θ increases from 0° to 90°.', 'For a fixed adjacent side, the opposite side gets longer as the angle increases, so opposite ÷ adjacent increases (without limit as θ → 90°).', 'B1 opposite grows; B1 ratio increases [2]'),
])


@t32.add('C1', (1, 2, 3))
def t32_which(r, D):
    know, want = r.choice([('hypotenuse', 'opposite'), ('hypotenuse', 'adjacent'), ('adjacent', 'opposite'), ('opposite', 'adjacent'), ('opposite', 'hypotenuse'), ('adjacent', 'hypotenuse')])
    ratio = {frozenset(['hypotenuse', 'opposite']): 'sine', frozenset(['hypotenuse', 'adjacent']): 'cosine', frozenset(['adjacent', 'opposite']): 'tangent'}[frozenset([know, want])]
    th = r.randint(20, 70)
    L = r.choice([5, 6.5, 8, 9.2, 12, 14.5])
    return SMC(r, f'In a right-angled triangle, angle θ = {th}° and the {know} is {ex(L)} cm. Which ratio should be used to find the {want}?', ratio, [x for x in ['sine', 'cosine', 'tangent', 'Pythagoras\' theorem'] if x != ratio],
               f'The {know} and {want} sides go together in {ratio} ({"SOH" if ratio == "sine" else ("CAH" if ratio == "cosine" else "TOA")}).')


@t32.add('C2', (2, 3, 4), 'explain')
def t32_err(r, D):
    th = r.randint(25, 65)
    h = r.choice([8, 10, 12, 15, 18, 20])
    nm = person(r)
    opp = h * sind(th)
    return Q(f'In triangle ABC, angle B = 90°, angle A = {th}° and the hypotenuse AC = {h} cm. {nm} writes BC = {h} × cos {th}° = {n3(h * cosd(th))} cm. Explain the error and find BC.',
             f'BC is opposite angle A, so sine should be used: BC = {h} sin {th}° = {n3(opp)} cm.', f'B1 BC is opposite A (not adjacent); M1 {h} sin {th}°; A1 {n3(opp)} cm [3]', marks=3)


@t32.add('C3', (1, 2, 3, 4))
def t32_side(r, D):
    th = r.randint(18, 72) if D < 4 else round(r.uniform(15, 75), 1)
    kind = r.choice(['opp_h', 'adj_h', 'opp_a', 'hyp_o', 'hyp_a', 'adj_o'])
    L = r.choice([4.5, 6, 7.2, 8, 9.6, 11, 12.5, 15]) if D < 4 else round(r.uniform(4, 25), 1)
    if kind == 'opp_h':
        v, how = L * sind(th), f'x = {ex(L)} sin {ex(th)}°'
        txt = f'the hypotenuse is {ex(L)} cm. Calculate the length of the side opposite the angle'
    elif kind == 'adj_h':
        v, how = L * cosd(th), f'x = {ex(L)} cos {ex(th)}°'
        txt = f'the hypotenuse is {ex(L)} cm. Calculate the length of the side adjacent to the angle'
    elif kind == 'opp_a':
        v, how = L * tand(th), f'x = {ex(L)} tan {ex(th)}°'
        txt = f'the side adjacent to the angle is {ex(L)} cm. Calculate the length of the side opposite the angle'
    elif kind == 'hyp_o':
        v, how = L / sind(th), f'x = {ex(L)} ÷ sin {ex(th)}°'
        txt = f'the side opposite the angle is {ex(L)} cm. Calculate the length of the hypotenuse'
    elif kind == 'hyp_a':
        v, how = L / cosd(th), f'x = {ex(L)} ÷ cos {ex(th)}°'
        txt = f'the side adjacent to the angle is {ex(L)} cm. Calculate the length of the hypotenuse'
    else:
        v, how = L / tand(th), f'x = {ex(L)} ÷ tan {ex(th)}°'
        txt = f'the side opposite the angle is {ex(L)} cm. Calculate the length of the side adjacent to the angle'
    stem = f'In a right-angled triangle, one angle is {ex(th)}° and {txt}.'
    if D == 1:
        return MC(r, stem.replace('Calculate the length', 'What is the length'), round(v, 1), [round(v * 1.3, 1), round(v * 0.7, 1), round(L * 1.1 if abs(L * 1.1 - v) > 0.2 else L * 1.5, 1), round(v + 2, 1)], f'{how} = {ex(round(v, 1))} cm (1 d.p.).', fmtf=lambda x: f'{x:.1f}', unit=' cm')
    return Q(stem, f'{n3(v)} cm', f'M1 {how}; A1 {n3(v)} cm.')


@t32.add('C3', (2, 3, 4, 5))
def t32_angle(r, D):
    a, b = r.choice([3, 4, 5, 6, 7.5, 8, 9]), r.choice([5, 10, 11, 12, 13, 14.5, 16])
    kind = r.choice(['tan', 'sin', 'cos'])
    if kind == 'tan':
        v = math.degrees(math.atan(a / b))
        txt, how = f'the sides adjacent to the right angle are {ex(a)} cm and {ex(b)} cm. Calculate the smallest angle of the triangle', f'tan θ = {ex(a)}/{ex(b)}'
    else:
        lo, hi = min(a, b), max(a, b) + (1 if a == b else 0)
        v = math.degrees(math.asin(lo / hi)) if kind == 'sin' else math.degrees(math.acos(lo / hi))
        txt = f'the hypotenuse is {ex(hi)} cm and one other side is {ex(lo)} cm. Calculate the angle {"opposite" if kind == "sin" else "between"} the {ex(lo)} cm side{"" if kind == "sin" else " and the hypotenuse"}'
        how = f'{"sin" if kind == "sin" else "cos"} θ = {ex(lo)}/{ex(hi)}'
    return Q(f'In a right-angled triangle, {txt}.', f'{v:.1f}°', f'M1 {how}; M1 inverse function; A1 {v:.1f}°.')


def t32_c4(r, D):
    kind = r.choice(['ladder', 'ramp', 'kite'])
    if kind == 'ladder':
        L = r.choice([4, 4.5, 5, 6, 6.5, 7.2])
        th = r.randint(65, 78)
        h, base = L * sind(th), L * cosd(th)
        safe = 75
        intro = f'A ladder of length {ex(L)} m leans against a vertical wall of a building in {city(r)}. The foot of the ladder is on horizontal ground and the ladder makes an angle of {th}° with the ground.'
        parts = [
            P('Calculate how far up the wall the ladder reaches.', f'{n3(h)} m', f'M1 {ex(L)} sin {th}°; A1 {n3(h)}', 2),
            P('Calculate the distance of the foot of the ladder from the wall.', f'{n3(base)} m', f'M1 {ex(L)} cos {th}°; A1 {n3(base)}', 2),
            P(f'For safety the angle should be {safe}°. The foot of the ladder is moved. Calculate the new distance from the wall.', f'{n3(L * cosd(safe))} m', f'M1 {ex(L)} cos {safe}°; A1 {n3(L * cosd(safe))}', 2),
            P('Explain why the ladder reaches higher up the wall when the angle with the ground is increased.', 'Height = L sin θ and sin θ increases as θ increases towards 90°.', 'B1', 1),
        ]
    elif kind == 'ramp':
        hgt = r.choice([0.45, 0.6, 0.75, 0.8, 0.9])
        run = r.choice([5, 6, 7.5, 8, 9])
        ang = math.degrees(math.atan(hgt / run))
        slope = math.hypot(hgt, run)
        intro = f'A wheelchair ramp at a library in {city(r)} rises {ex(hgt)} m over a horizontal distance of {ex(run)} m.'
        parts = [
            P('Calculate the angle the ramp makes with the horizontal.', f'{ang:.1f}°', f'M1 tan θ = {ex(hgt)}/{ex(run)}; A1 {ang:.1f}°', 2),
            P('Calculate the length of the sloping surface of the ramp.', f'{n3(slope)} m', f'M1 √({ex(hgt)}² + {ex(run)}²); A1 {n3(slope)} m', 2),
            P(f'The maximum safe angle is 4.8°. Calculate the least horizontal distance needed for a rise of {ex(hgt)} m.', f'{n3(hgt / tand(4.8))} m', f'M1 {ex(hgt)} ÷ tan 4.8°; A1 {n3(hgt / tand(4.8))} m', 2),
            P('State, with a reason, whether the ramp is safe.', 'Safe' if ang <= 4.8 else 'Not safe', f'B1 compares {ang:.1f}° with 4.8°', 1),
        ]
    else:
        s = r.choice([25, 30, 40, 50, 60])
        th = r.randint(35, 62)
        hgt = s * sind(th)
        hand = r.choice([1.2, 1.4, 1.5])
        nm = person(r)
        intro = f'{nm} flies a kite on a straight string of length {s} m on a beach near {city(r)}. The string makes an angle of {th}° with the horizontal, and {nm} holds it {ex(hand)} m above the ground.'
        parts = [
            P('Calculate the height of the kite above the ground.', f'{n3(hgt + hand)} m', f'M1 {s} sin {th}°; M1 + {ex(hand)}; A1 {n3(hgt + hand)} m', 3),
            P('Calculate the horizontal distance from the hand to the point directly below the kite.', f'{n3(s * cosd(th))} m', f'M1 {s} cos {th}°; A1', 2),
            P('The string is let out to 1.5 times its length at the same angle. Explain what happens to the height of the kite above the hand.', 'It is multiplied by 1.5, since height = length × sin θ and the angle is unchanged.', 'B1 B1', 2),
        ]
    return cmp_(r, intro, parts)


t32.add('C4', (2, 3, 4, 5))(t32_c4)

# ---------------------------------------------------------------- elevation and depression
t33 = topic('Angles of elevation and depression', 'angles of elevation and depression', 'angle of elevation', 'angle of depression')
t33.fixed('C1', (1, 2), [
    ('An angle of elevation is measured', 'upwards from the horizontal', 'Elevation: looking up from the horizontal line of sight.', ['downwards from the horizontal', 'upwards from the vertical', 'clockwise from north']),
    ('An angle of depression is measured', 'downwards from the horizontal', 'Depression: looking down from the horizontal.', ['upwards from the horizontal', 'downwards from the vertical', 'from the ground to the object']),
    ('The angle of depression from the top of a cliff to a boat is 28°. What is the angle of elevation of the top of the cliff from the boat?', '28°', 'Alternate angles between parallel horizontal lines are equal.', ['62°', '152°', '56°']),
    ('A tower is 40 m high. From a point on level ground the angle of elevation of the top is 45°. How far is the point from the foot of the tower?', '40 m', 'tan 45° = 1, so distance = height.', ['20 m', '80 m', '56.6 m']),
])
t33.fixed('C2', (2, 3), [
    ('Explain why the angle of depression from A to B is equal to the angle of elevation from B to A.', 'The horizontal lines at A and B are parallel, and the line AB is a transversal, so the two angles are alternate angles and are equal.', 'B1 parallel horizontals; B1 alternate angles [2]'),
    ('A student measures an angle of depression from the vertical instead of the horizontal and gets 65°. Explain how to correct this.', 'Angles of depression are measured from the horizontal, so the correct angle is 90° − 65° = 25°.', 'B1 from the horizontal; B1 25° [2]'),
    ('Explain why the height of an observer\'s eyes must be included when finding the height of a tree from an angle of elevation.', 'The angle is measured from eye level, so the trigonometry gives the height above the eyes; the eye height must be added to get the height above the ground.', 'B1 measured from eye level; B1 add eye height [2]'),
])


@t33.add('C1', (1, 2, 3))
def t33_q(r, D):
    a = r.randint(15, 70)
    return MC(r, f'The angle of elevation of the top of a mast from a point P is {a}°. What is the angle of depression of P from the top of the mast?', a, [90 - a, 180 - a, a + 90, 2 * a, a + 10, 360 - a],
              'Alternate angles between parallel horizontal lines are equal.', fmtf=lambda x: f'{num(x)}°')


@t33.add('C2', (2, 3, 4), 'explain')
def t33_err(r, D):
    a = r.randint(20, 55)
    d = r.choice([30, 40, 50, 60, 80, 120])
    nm = person(r)
    return Q(f'From a point {d} m from the foot of a building the angle of elevation of the top is {a}°. {nm} calculates the height as {d} × sin {a}° = {n3(d * sind(a))} m. Explain the error and find the correct height.',
             f'The {d} m is the adjacent side and the height is opposite, so tan should be used: {d} tan {a}° = {n3(d * tand(a))} m.', f'B1 should use tan (opp/adj); M1 {d} tan {a}°; A1 {n3(d * tand(a))} m [3]', marks=3)


@t33.add('C3', (1, 2, 3, 4, 5))
def t33_calc(r, D):
    a = r.randint(18, 64) if D < 4 else round(r.uniform(12, 68), 1)
    kind = r.choice(['height', 'dist', 'angle'])
    obj = r.choice(['a mobile phone mast', 'a lighthouse', 'a church tower', 'a tall tree', 'a skyscraper', 'a water tower'])
    if kind == 'height':
        d = r.choice([25, 30, 45, 60, 75, 90, 120])
        eye = r.choice([1.5, 1.6, 1.7]) if D >= 3 else 0
        h = d * tand(a) + eye
        nm = person(r)
        stem = f'{nm} stands {d} m from the foot of {obj} on level ground in {city(r)}. The angle of elevation of the top is {ex(a)}°' + (f', measured from {nm}\'s eye level, {ex(eye)} m above the ground.' if eye else '.') + ' Calculate the height of the ' + obj.split(' ', 1)[1] + '.'
        if D == 1:
            return MC(r, stem.replace('Calculate the height', 'What is the height'), round(h, 1), [round(d * sind(a), 1), round(d / tand(a), 1), round(d * cosd(a), 1), round(h + 5, 1)], f'h = {d} tan {ex(a)}° = {h:.1f} m.', fmtf=lambda x: f'{x:.1f}', unit=' m')
        return Q(stem, f'{n3(h)} m', f'M1 tan {ex(a)}° = h/{d}; M1 h = {d} tan {ex(a)}°' + (f' + {ex(eye)}' if eye else '') + f'; A1 {n3(h)} m.')
    if kind == 'dist':
        H = r.choice([35, 48, 60, 72, 85, 110])
        dd = H / tand(a)
        return Q(f'From the top of a cliff {H} m high, the angle of depression of a boat is {ex(a)}°. Calculate the horizontal distance of the boat from the foot of the cliff.', f'{n3(dd)} m',
                 f'M1 angle of elevation from boat = {ex(a)}°; M1 {H} ÷ tan {ex(a)}°; A1 {n3(dd)} m.')
    H = r.choice([12, 18, 24, 30, 45])
    dd = r.choice([20, 35, 50, 64, 80])
    ang = math.degrees(math.atan(H / dd))
    nm = person(r)
    return Q(f'A drone hovers {H} m above a point on level ground. {nm} stands {dd} m from that point. Calculate the angle of elevation of the drone from {nm}\'s feet.', f'{ang:.1f}°',
             f'M1 tan θ = {H}/{dd}; A1 {ang:.1f}°.')


def t33_c4(r, D):
    H = r.choice([40, 55, 60, 75, 90, 120])
    a, b = sorted(r.sample([14, 18, 22, 25, 31, 36, 42], 2))
    d1, d2 = H / tand(b), H / tand(a)
    intro = f'A lighthouse on the coast near {city(r)} has its light {H} m above sea level. From the light, the angles of depression of two boats P and Q, which are in a straight line with the foot of the lighthouse, are {b}° and {a}°.'
    parts = [
        P('Calculate the distance of P from the foot of the lighthouse.', f'{n3(d1)} m', f'M1 {H} ÷ tan {b}°; A1 {n3(d1)}', 2),
        P('Calculate the distance of Q from the foot of the lighthouse.', f'{n3(d2)} m', f'M1 {H} ÷ tan {a}°; A1 {n3(d2)}', 2),
        P('Calculate the distance between the two boats.', f'{n3(d2 - d1)} m', f'M1 subtracts distances; A1 {n3(d2 - d1)} m', 2),
        P('Write down the angle of elevation of the light from boat Q, giving a reason.', f'{a}°: alternate angles are equal.', 'B1 value; B1 reason', 2),
        P('Calculate the straight-line distance from boat P to the light.', f'{n3(H / sind(b))} m', f'M1 {H} ÷ sin {b}°; A1', 2),
    ]
    return cmp_(r, intro, parts)


def t33_c4b(r, D):
    a, b = r.choice([(28, 40), (25, 37), (30, 45), (22, 35), (32, 50)])
    d = r.choice([20, 25, 30, 40, 50])
    x = d * tand(a) / (tand(b) - tand(a))
    h = x * tand(b)
    nm = person(r)
    intro = f'{nm} measures the angle of elevation of the top T of a tower from a point A on level ground as {a}°. {nm} walks {d} m directly towards the tower to a point B, where the angle of elevation is {b}°. The foot of the tower is F.'
    parts = [
        P('Calculate the angle ATB.', f'{b - a}°', f'M1 exterior angle of triangle: {b}° − {a}°; A1', 2),
        P('Use the sine rule in triangle ABT to calculate BT.', f'{n3(d * sind(a) / sind(b - a))} m', f'M1 BT/sin {a}° = {d}/sin {b - a}°; A1 {n3(d * sind(a) / sind(b - a))} m', 2),
        P('Calculate the height of the tower.', f'{n3(h)} m', f'M1 BT sin {b}° (or h = x tan {b}° with x tan {b}° = (x + {d}) tan {a}°); A1 {n3(h)} m', 3),
        P('Calculate the distance BF.', f'{n3(x)} m', f'M1 h ÷ tan {b}°; A1 {n3(x)} m', 2),
    ]
    return cmp_(r, intro, parts)


t33.add('C4', (2, 3, 4))(t33_c4)
t33.add('C4', (3, 4, 5))(t33_c4b)

# ---------------------------------------------------------------- sine and cosine rules
t34 = topic('Sine rule, cosine rule and area of a triangle', 'sine rule', 'cosine rule', 'area of a triangle using ½ab sin c')
t34.fixed('C1', (1, 2), [
    ('Which is the sine rule for triangle ABC?', 'a/sin A = b/sin B = c/sin C', 'Each side over the sine of its opposite angle.', ['a/sin B = b/sin A', 'a sin A = b sin B', 'sin A/b = sin B/a']),
    ('Which is the cosine rule for finding side a?', 'a² = b² + c² − 2bc cos A', 'Side a is opposite angle A, between sides b and c.', ['a² = b² + c² + 2bc cos A', 'a² = b² − c² − 2bc cos A', 'a = b + c − 2bc cos A']),
    ('Which formula gives the area of triangle ABC?', '½ab sin C', 'Two sides and the included angle.', ['½ab cos C', 'ab sin C', '½bc sin B']),
    ('You know all three sides of a triangle and want an angle. Which rule should you use?', 'The cosine rule', 'Rearranged cosine rule: cos A = (b² + c² − a²)/2bc.', ['The sine rule', 'Pythagoras\' theorem', 'The area formula']),
    ('You know two angles and one side of a triangle. Which rule should you use to find another side?', 'The sine rule', 'Sine rule links sides with opposite angles.', ['The cosine rule', 'Pythagoras\' theorem', 'SOH CAH TOA only']),
    ('If cos A is negative in a triangle, what can you say about angle A?', 'It is obtuse', 'cos is negative for 90° < A < 180°.', ['It is acute', 'It is a right angle', 'It is reflex']),
])
t34.fixed('C2', (2, 3), [
    ('Explain why the sine rule can give two possible triangles when finding an angle.', 'sin θ = sin(180° − θ), so an acute angle and its obtuse supplement both have the same sine; both may fit the given information.', 'B1 sin θ = sin(180 − θ); B1 two possible angles [2]'),
    ('Explain how the cosine rule a² = b² + c² − 2bc cos A becomes Pythagoras\' theorem when A = 90°.', 'cos 90° = 0, so the term 2bc cos A disappears and a² = b² + c².', 'B1 cos 90° = 0; B1 result [2]'),
    ('Explain why ½ab sin C is used rather than ½ × base × height when the height is not known.', 'The height from the base b is a sin C, so ½ × b × a sin C gives the area without measuring the height.', 'B1 h = a sin C; B1 substitution [2]'),
    ('Describe how to decide between the sine rule and the cosine rule.', 'Use the sine rule when you have a side and its opposite angle (a pair); use the cosine rule when you have two sides and the included angle, or all three sides.', 'B1 sine rule condition; B1 cosine rule condition [2]'),
])


@t34.add('C1', (1, 2, 3))
def t34_area(r, D):
    a, b = r.choice([5, 6, 8, 10, 12]), r.choice([4, 7, 9, 11, 14])
    C = r.choice([30, 150])
    A = 0.5 * a * b * sind(C)
    return MC(r, f'Triangle PQR has PQ = {a} cm, PR = {b} cm and angle QPR = {C}°. What is its area?', A, [a * b * sind(C), 0.5 * a * b, 0.5 * a * b * abs(cosd(C)), a + b],
              f'½ × {a} × {b} × sin {C}° = ½ × {a * b} × 0.5 = {ex(A)} cm².', fmtf=lambda x: ex(round(x, 2)), unit=' cm²')


@t34.add('C2', (2, 3, 4), 'explain')
def t34_err(r, D):
    b, c = r.choice([7, 8, 9, 10, 12]), r.choice([5, 6, 11, 13])
    A = r.choice([105, 115, 120, 130, 140])
    nm = person(r)
    a = math.sqrt(b * b + c * c - 2 * b * c * cosd(A))
    wrong = math.sqrt(b * b + c * c + 2 * b * c * cosd(A)) if b * b + c * c + 2 * b * c * cosd(A) > 0 else None
    return Q(f'In triangle ABC, b = {b} cm, c = {c} cm and angle A = {A}°. {nm} says that because A is obtuse, cos A should be made positive, and calculates a² = {b}² + {c}² − 2 × {b} × {c} × {ex(round(abs(cosd(A)), 4))}. Explain the error and find a.',
             f'cos {A}° is negative ({ex(round(cosd(A), 4))}), and the sign must be kept, so −2bc cos A is added: a = {n3(a)} cm.', f'B1 cos of obtuse angle is negative and must be used as it is; M1 a² = {b}² + {c}² − 2({b})({c})cos {A}°; A1 {n3(a)} cm [3]', marks=3)


@t34.add('C3', (2, 3, 4, 5))
def t34_cos(r, D):
    if r.random() < 0.5:
        b, c = r.randint(5, 15), r.randint(5, 15)
        A = r.randint(25, 140)
        a = math.sqrt(b * b + c * c - 2 * b * c * cosd(A))
        return Q(f'In triangle ABC, AB = {c} cm, AC = {b} cm and angle BAC = {A}°. Calculate the length of BC.', f'{n3(a)} cm',
                 f'M1 BC² = {b}² + {c}² − 2 × {b} × {c} × cos {A}°; A1 BC² = {ex(round(a * a, 2))}; A1 {n3(a)} cm.')
    for _ in range(100):
        a, b, c = r.randint(4, 15), r.randint(4, 15), r.randint(4, 15)
        if a + b > c and a + c > b and b + c > a and len({a, b, c}) == 3:
            break
    ang = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
    return Q(f'A triangle has sides {a} cm, {b} cm and {c} cm. Calculate the angle opposite the {a} cm side.', f'{ang:.1f}°',
             f'M1 cos θ = ({b}² + {c}² − {a}²) ÷ (2 × {b} × {c}); A1 cos θ = {ex(round((b * b + c * c - a * a) / (2 * b * c), 4))}; A1 {ang:.1f}°.')


@t34.add('C3', (2, 3, 4, 5))
def t34_sin(r, D):
    A, B = r.randint(30, 80), r.randint(30, 80)
    a = r.choice([6, 7.5, 8, 9.4, 11, 12.6, 15])
    b = a * sind(B) / sind(A)
    if r.random() < 0.6:
        return Q(f'In triangle ABC, angle A = {A}°, angle B = {B}° and BC = {ex(a)} cm. Calculate the length of AC.', f'{n3(b)} cm',
                 f'M1 AC/sin {B}° = {ex(a)}/sin {A}°; A1 {n3(b)} cm.')
    b = round(b, 1)
    Bc = math.degrees(math.asin(b * sind(A) / a))
    return Q(f'In triangle ABC, angle A = {A}°, BC = {ex(a)} cm and AC = {ex(b)} cm. Angle B is acute. Calculate angle B.', f'{Bc:.1f}°',
             f'M1 sin B/{ex(b)} = sin {A}°/{ex(a)}; M1 sin B = {ex(round(b * sind(A) / a, 4))}; A1 {Bc:.1f}°.')


@t34.add('C3', (2, 3, 4))
def t34_area2(r, D):
    a, b = r.randint(5, 20), r.randint(5, 20)
    C = r.randint(25, 155)
    A = 0.5 * a * b * sind(C)
    if D >= 4:
        return Q(f'The area of triangle XYZ is {n3(A)} cm². XY = {a} cm and XZ = {b} cm. Angle YXZ is {"acute" if C < 90 else "obtuse"}. Calculate angle YXZ.', f'{C}°',
                 f'M1 ½ × {a} × {b} × sin X = {n3(A)}; M1 sin X = {ex(round(sind(C), 4))}; A1 {C}°' + (' (180° − acute value)' if C > 90 else '') + '.')
    return Q(f'Triangle XYZ has XY = {a} cm, XZ = {b} cm and angle YXZ = {C}°. Calculate the area of the triangle.', f'{n3(A)} cm²', f'M1 ½ × {a} × {b} × sin {C}°; A1 {n3(A)} cm².')


def t34_c4(r, D):
    a, b = r.choice([(120, 85), (150, 110), (95, 140), (200, 160), (75, 60)])
    C = r.randint(48, 125)
    c = math.sqrt(a * a + b * b - 2 * a * b * cosd(C))
    B = math.degrees(math.acos((a * a + c * c - b * b) / (2 * a * c)))
    area = 0.5 * a * b * sind(C)
    per = a + b + c
    price = r.choice([12, 15, 18, 25])
    intro = f'A triangular plot of land PQR near {city(r)} has PQ = {a} m, PR = {b} m and angle QPR = {C}°.'
    parts = [
        P('Calculate the length of QR.', f'{n3(c)} m', f'M1 QR² = {a}² + {b}² − 2({a})({b}) cos {C}°; A1 {n3(c)} m', 3),
        P('Calculate the area of the plot.', f'{n3(area)} m²', f'M1 ½ × {a} × {b} × sin {C}°; A1 {n3(area)} m²', 2),
        P('Calculate angle PQR.', f'{B:.1f}°', f'M1 cos Q = ({a}² + QR² − {b}²) ÷ (2 × {a} × QR) (or sine rule, checking for obtuse); A1 {B:.1f}°', 2),
        P(f'Fencing costs ${price} per metre. Calculate the cost of fencing the whole perimeter.', f'${per * price:,.0f} (to the nearest dollar)', f'M1 perimeter {n3(per)} m; A1 × {price} = ${per * price:,.0f}', 2),
        P('Calculate the shortest distance from R to the side PQ.', f'{n3(b * sind(C))} m', f'M1 {b} sin {C}° (or 2 × area ÷ {a}); A1 {n3(b * sind(C))} m', 2),
    ]
    return cmp_(r, intro, parts)


t34.add('C4', (2, 3, 4, 5))(t34_c4)

# ---------------------------------------------------------------- 3D and trig graphs
def solve_trig(f, k):
    if f == 'sin':
        b = math.degrees(math.asin(abs(k)))
        sols = [b, 180 - b] if k >= 0 else [180 + b, 360 - b]
    elif f == 'cos':
        b = math.degrees(math.acos(k))
        sols = [b, 360 - b]
    else:
        b = math.degrees(math.atan(k))
        b = b if b >= 0 else b + 180
        sols = [b, b + 180]
    return sorted(sols)


t35 = topic('Trigonometry in three dimensions and graphs of sine, cosine and tangent', 'trigonometry in three dimensions', 'graphs of sine, cosine and tangent', '3d trigonometry')
t35.fixed('C1', (1, 2), [
    ('What is the period of the graph of y = sin x?', '360°', 'The sine graph repeats every 360°.', ['180°', '90°', '720°']),
    ('What is the maximum value of y = cos x?', '1', 'cos x lies between −1 and 1.', ['90', '360', '0']),
    ('For which value of x between 0° and 360° is tan x undefined?', '90°', 'tan 90° = sin 90°/cos 90° = 1/0, undefined (also 270°).', ['0°', '45°', '180°']),
    ('Which is equal to sin 130°?', 'sin 50°', 'sin x = sin(180° − x).', ['cos 50°', 'sin 230°', '−sin 50°']),
    ('What is the period of the graph of y = tan x?', '180°', 'The tangent graph repeats every 180°.', ['360°', '90°', '270°']),
    ('Which is equal to cos 300°?', 'cos 60°', 'cos x = cos(360° − x).', ['−cos 60°', 'sin 60°', 'cos 120°']),
])
t35.fixed('C2', (2, 3), [
    ('Explain why the equation sin x = 1.4 has no solutions.', 'The value of sin x always lies between −1 and 1, so it can never equal 1.4.', 'B1 range −1 to 1; B1 conclusion [2]'),
    ('Explain why cos x = −0.5 has two solutions between 0° and 360°.', 'The cosine graph is below the x-axis between 90° and 270° and is symmetrical about x = 180°, so the line y = −0.5 crosses it twice: 120° and 240°.', 'B1 graph symmetry/two crossings; B1 120° and 240° [2]'),
    ('Explain how to find the angle between a space diagonal of a cuboid and its base.', 'Find the diagonal of the base (Pythagoras), then use the right-angled triangle formed by the base diagonal, the vertical edge and the space diagonal: tan θ = height ÷ base diagonal.', 'B1 base diagonal; B1 right-angled triangle with vertical edge [2]'),
    ('Explain why the angle between a line and a plane uses the projection of the line on the plane.', 'The angle is defined as the angle between the line and its projection (shadow) on the plane, which forms a right-angled triangle with the perpendicular.', 'B1 projection; B1 right-angled triangle [2]'),
])


@t35.add('C1', (1, 2, 3))
def t35_sym(r, D):
    x = r.randint(10, 80)
    f = r.choice(['sin', 'cos'])
    c = 180 - x if f == 'sin' else 360 - x
    return MC(r, f'Given that {f} {x}° = {ex(round(sind(x) if f == "sin" else cosd(x), 4))}, which other angle between 0° and 360° has the same {"sine" if f == "sin" else "cosine"}?', c,
              [180 + x, 360 - x if f == 'sin' else 180 - x, 90 + x, 90 - x], f'{f} x = {f}({"180° − x" if f == "sin" else "360° − x"}), so {c}°.', fmtf=lambda v: f'{num(v)}°')


@t35.add('C2', (2, 3, 4), 'explain')
def t35_err(r, D):
    k = r.choice([0.3, 0.45, 0.6, 0.75, 0.82])
    f = r.choice(['sin', 'cos'])
    sols = solve_trig(f, -k)
    nm = person(r)
    first = math.degrees(math.asin(-k)) if f == 'sin' else math.degrees(math.acos(-k))
    return Q(f'{nm} solves {f} x = {MINUS}{ex(k)} for 0° ≤ x ≤ 360° and gives only the calculator answer x = {first:.1f}°. Explain why this is not a complete (or correct) answer and find all the solutions.',
             f'The calculator gives one value only{" and it is outside the range" if first < 0 else ""}; the graph of y = {f} x crosses y = {MINUS}{ex(k)} twice in this range: x = {sols[0]:.1f}° and x = {sols[1]:.1f}°.',
             f'B1 explains second solution from graph symmetry{"/range" if first < 0 else ""}; A1 {sols[0]:.1f}°; A1 {sols[1]:.1f}° [3]', marks=3)


@t35.add('C3', (2, 3, 4, 5))
def t35_solve(r, D):
    f = r.choice(['sin', 'cos', 'tan'])
    k = r.choice([0.2, 0.35, 0.4, 0.55, 0.7, 0.85]) if f != 'tan' else r.choice([0.6, 1.5, 2, 2.4, 3.2])
    if D >= 4:
        k = -k
    sols = solve_trig(f, k)
    if D >= 5:
        m = r.choice([2, 3, 4, 5])
        d = r.choice([1, -1, 2, -2, 3])
        c = round(m * k + d, 2)
        return Q(f'Solve the equation {m} {f} x{sgn(d)} = {num(c)} for 0° ≤ x ≤ 360°.',
                 f'x = {sols[0]:.1f}° or x = {sols[1]:.1f}°', f'M1 {f} x = ({num(c)}{sgn(-d)}) ÷ {m} = {num(k)}; A1 {sols[0]:.1f}°; A1 {sols[1]:.1f}°.')
    return Q(f'Solve the equation {f} x = {num(k)} for 0° ≤ x ≤ 360°.', f'x = {sols[0]:.1f}° or x = {sols[1]:.1f}°', f'M1 principal value {f}⁻¹({num(k)}); M1 uses symmetry/period of the graph; A1 {sols[0]:.1f}° and {sols[1]:.1f}°.')


@t35.add('C3', (2, 3, 4, 5))
def t35_cuboid(r, D):
    l, w, h = r.choice([8, 10, 12, 15]), r.choice([4, 5, 6, 9]), r.choice([3, 5, 7, 8])
    bd = math.hypot(l, w)
    sd = math.sqrt(l * l + w * w + h * h)
    ang = math.degrees(math.atan(h / bd))
    if D <= 3:
        return Q(f'A cuboid ABCDEFGH has a rectangular base ABCD with AB = {l} cm and BC = {w} cm, and height {h} cm. Calculate the length of the space diagonal AG.', f'{n3(sd)} cm',
                 f'M1 AC² = {l}² + {w}²; M1 AG² = AC² + {h}²; A1 {n3(sd)} cm.')
    return Q(f'A cuboid ABCDEFGH has a rectangular base ABCD with AB = {l} cm and BC = {w} cm, and vertical edges of {h} cm (G is above C). Calculate the angle between the diagonal AG and the base ABCD.', f'{ang:.1f}°',
             f'M1 AC = √({l}² + {w}²) = {n3(bd)}; M1 tan θ = {h}/AC; A1 {ang:.1f}°.')


def t35_c4(r, D):
    s = r.choice([6, 8, 10, 12, 14])
    h = r.choice([5, 7, 9, 12, 15])
    half_d = s * math.sqrt(2) / 2
    edge = math.sqrt(half_d ** 2 + h * h)
    ang_e = math.degrees(math.atan(h / half_d))
    ang_f = math.degrees(math.atan(h / (s / 2)))
    vol = s * s * h / 3
    intro = f'A square-based pyramid VABCD has base side {s} cm. The vertex V is vertically above the centre M of the base and VM = {h} cm. The pyramid is a model of a monument in {city(r)}.'
    parts = [
        P('Calculate the length of the diagonal AC of the base.', f'{n3(2 * half_d)} cm', f'M1 √({s}² + {s}²); A1', 2),
        P('Calculate the length of the sloping edge VA.', f'{n3(edge)} cm', f'M1 AM = {n3(half_d)}; M1 √(AM² + {h}²); A1 {n3(edge)} cm', 3),
        P('Calculate the angle between VA and the base.', f'{ang_e:.1f}°', f'M1 tan θ = {h} ÷ AM; A1 {ang_e:.1f}°', 2),
        P('Calculate the angle between the triangular face VAB and the base.', f'{ang_f:.1f}°', f'M1 uses midpoint of AB, distance {ex(s / 2)} from M; M1 tan θ = {h}/{ex(s / 2)}; A1 {ang_f:.1f}°', 3),
        P('Calculate the volume of the pyramid.', f'{n3(vol)} cm³', f'M1 ⅓ × {s}² × {h}; A1', 2),
    ]
    return cmp_(r, intro, parts)


def t35_c4b(r, D):
    a = r.choice([2, 3, 4, 5])
    k = r.choice([1, 2])
    x1 = r.choice([30, 60, 150, 210])
    intro = f'The graph of y = {a} sin x + {k} is drawn for 0° ≤ x ≤ 360°.'
    s1 = solve_trig('sin', 0.5)
    parts = [
        P('Write down the maximum value of y and the value of x where it occurs.', f'y = {a + k} at x = 90°', 'B1 B1', 2),
        P('Write down the minimum value of y.', f'{num(k - a)}', 'B1', 1),
        P(f'Calculate the value of y when x = {x1}°.', f'{ex(round(a * sind(x1) + k, 3))}', f'M1 {a} sin {x1}° + {k}; A1', 2),
        P(f'Solve {a} sin x + {k} = {ex(a * 0.5 + k)} for 0° ≤ x ≤ 360°.', 'x = 30° or x = 150°', f'M1 sin x = 0.5; A1 30°; A1 150°', 3),
        P('Write down the period of the graph.', '360°', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


t35.add('C4', (2, 3, 4, 5))(t35_c4)
t35.add('C4', (2, 3, 4))(t35_c4b)
CHAPTERS[3] = [t31, t32, t33, t34, t35]


# =========================================================== 4 Scatter diagrams and correlation (Ch 16)
SCAT = [
    # x label, y label, sign, x range, slope, intercept, noise, x short, y short
    ('midday temperature (°C)', 'number of cold drinks sold', 1, (16, 36), 6, -40, 12, 'temperature', 'cold drink sales'),
    ('hours spent revising', 'test mark (%)', 1, (1, 14), 4.5, 22, 8, 'revision time', 'test mark'),
    ('age of a car (years)', 'value of the car ($1000s)', -1, (1, 11), -1.6, 22, 1.8, 'age', 'value'),
    ('height above sea level (m)', 'air temperature (°C)', -1, (200, 2400), -0.0065, 28, 1.2, 'height above sea level', 'temperature'),
    ('height of a student (cm)', 'arm span (cm)', 1, (148, 186), 1.0, 0, 4, 'height', 'arm span'),
    ('distance from the city centre (km)', 'monthly rent ($)', -1, (1, 18), -42, 1400, 70, 'distance from centre', 'rent'),
    ('daily hours of sunshine', 'daily rainfall (mm)', -1, (1, 11), -1.4, 17, 2.5, 'sunshine', 'rainfall'),
    ('engine size (litres)', 'fuel economy (km per litre)', -1, (1.0, 4.0), -3.2, 22, 1.2, 'engine size', 'fuel economy'),
    ('number of people in a household', 'weekly food bill ($)', 1, (1, 7), 38, 30, 18, 'household size', 'food bill'),
    ('time spent on social media (hours per day)', 'hours of sleep', -1, (0.5, 6), -0.5, 9, 0.5, 'social media time', 'sleep'),
    ('practice shots taken', 'shots scored', 1, (10, 60), 0.6, 2, 3, 'practice shots', 'shots scored'),
]
NONE = [('shoe size', 'mathematics test mark (%)'), ('house number', 'height of the occupant (cm)'), ('day of the month of birth', 'reaction time (ms)'),
        ('last digit of phone number', 'distance travelled to school (km)'), ('number of letters in first name', 'mass (kg)')]


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0


def describe(rv):
    a = abs(rv)
    if a < 0.3:
        return 'no correlation'
    s = 'strong' if a >= 0.8 else 'weak'
    return f'{s} {"positive" if rv > 0 else "negative"} correlation'


def lsq(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return b, my - b * mx


def dataset(r, D, ctx=None, n=None, outlier=False, noise_mult=1.0):
    c = ctx or r.choice(SCAT)
    xl, yl, sign, (lo, hi), m, k, noise, xs_, ys_ = c
    n = n or r.choice([8, 9, 10])
    span = hi - lo
    dec = 0 if span >= 10 else 1
    xs = sorted({round(lo + span * r.random(), dec) for _ in range(n * 3)})
    xs = r.sample(xs, min(n, len(xs)))
    xs.sort()
    ydec = 0 if abs(m) * span > 15 else 1
    ys = [round(m * x + k + r.uniform(-noise, noise) * noise_mult, ydec) for x in xs]
    out = None
    if outlier:
        i = r.randrange(1, len(xs) - 1)
        ys[i] = round(ys[i] - sign * (abs(m) * span * 0.6 + 3 * noise), ydec)
        out = (xs[i], ys[i])
    xs = [int(x) if dec == 0 else x for x in xs]
    ys = [int(y) if ydec == 0 else y for y in ys]
    return c, xs, ys, out


def table(xl, yl, xs, ys):
    return f'{xl[0].upper() + xl[1:]}: ' + ', '.join(num(x) for x in xs) + f'. {yl[0].upper() + yl[1:]}: ' + ', '.join(num(y) for y in ys) + '.'


s41 = topic('Scatter diagrams and describing correlation', 'drawing scatter diagrams', 'describing correlation', 'scatter diagrams')
s41.fixed('C1', (1, 2), [
    ('What type of correlation is shown when one variable tends to decrease as the other increases?', 'Negative correlation', 'Negative: as x increases, y tends to decrease.', ['Positive correlation', 'No correlation', 'Zero gradient']),
    ('On a scatter diagram the points lie very close to a straight line sloping upwards. How is this correlation described?', 'Strong positive', 'Close to a line: strong; upward slope: positive.', ['Weak positive', 'Strong negative', 'No correlation']),
    ('Which pair of variables is most likely to show no correlation?', 'shoe size and score in a spelling test', 'There is no reason for shoe size to be related to spelling scores.', ['height and arm span', 'temperature and ice cream sales', 'age of a car and its value']),
    ('A point that does not fit the general pattern on a scatter diagram is called', 'an outlier', 'Outliers lie well away from the trend of the other points.', ['the mean point', 'the median', 'the intercept']),
    ('Which pair is most likely to show negative correlation?', 'outside temperature and amount of heating fuel used', 'Warmer weather → less heating fuel.', ['height and mass of adults', 'hours worked and pay earned', 'distance travelled and taxi fare']),
    ('A scatter diagram is used to show', 'the relationship between two sets of numerical data', 'Each point plots a pair of values (x, y).', ['the frequency of one variable', 'the proportions of a whole', 'how one variable changes over time only']),
])
s41.fixed('C2', (2, 3), [
    ('Explain the difference between strong and weak correlation.', 'In strong correlation the points lie close to a straight line; in weak correlation there is a trend but the points are more spread out from the line.', 'B1 strong: close to line; B1 weak: more scattered [2]'),
    ('Explain why it is useful to draw a scatter diagram before making predictions from data.', 'It shows whether there is any correlation, how strong it is and whether there are outliers; predictions are only sensible if there is reasonable correlation.', 'B1 shows correlation/strength; B1 outliers/whether prediction is sensible [2]'),
    ('A scatter diagram of height against mass for a class shows positive correlation. Describe what this means in context.', 'Taller students tend to be heavier.', 'B1 in context, with "tend to" (not certainty) [2]'),
    ('Explain why one outlier should not be ignored without a reason.', 'It could be a recording error, but it might be a genuine value; it should be checked before removing it from the analysis.', 'B1 could be error; B1 could be genuine/check [2]'),
])


@s41.add('C1', (1, 2, 3))
def s41_type(r, D):
    if r.random() < 0.25:
        a, b = r.choice(NONE)
        c = 'No correlation'
        why = f'there is no reason for {a} to be linked to {b}'
    else:
        ctx = r.choice(SCAT)
        a, b, sgn_ = ctx[0], ctx[1], ctx[2]
        c = 'Positive correlation' if sgn_ > 0 else 'Negative correlation'
        why = f'as {ctx[7]} increases, {ctx[8]} tends to {"increase" if sgn_ > 0 else "decrease"}'
    return SMC(r, f'A survey in {city(r)} records the {a} and the {b}. Which type of correlation would you expect a scatter diagram to show?', c,
               [x for x in ['Positive correlation', 'Negative correlation', 'No correlation', 'Perfect positive correlation'] if x != c], f'{c}: {why}.')


@s41.add('C2', (2, 3, 4), 'explain')
def s41_desc(r, D):
    ctx, xs, ys, _ = dataset(r, D)
    rv = pearson(xs, ys)
    d = describe(rv)
    nm = person(r)
    rel = 'there is no clear relationship' if d == 'no correlation' else f'as the {ctx[7]} increases, the {ctx[8]} tends to {"increase" if rv > 0 else "decrease"}'
    return Q(f'{nm} collects data in {city(r)} on the {ctx[0]} and the {ctx[1]}. {table(ctx[0], ctx[1], xs, ys)} Describe the correlation and interpret it in context.',
             f'{d[0].upper() + d[1:]}: {rel}.', f'B1 {d}; B1 interpretation in context [2]')


@s41.add('C3', (1, 2, 3, 4, 5))
def s41_data(r, D):
    ctx, xs, ys, out = dataset(r, D, outlier=D >= 3)
    rv = pearson([x for x, y in zip(xs, ys) if (x, y) != out], [y for x, y in zip(xs, ys) if (x, y) != out])
    d = describe(rv)
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    if D <= 2:
        stem = f'The table shows the {ctx[0]} and the {ctx[1]} for a sample of {len(xs)}. {table(ctx[0], ctx[1], xs, ys)} Calculate the mean of the {ctx[0]} and the mean of the {ctx[1]}.'
        return Q(stem, f'mean x = {ex(round(mx, 2))}, mean y = {ex(round(my, 2))}', f'M1 sum ÷ {len(xs)} for each; A1 ({ex(round(mx, 2))}, {ex(round(my, 2))}).')
    stem = f'Data on the {ctx[0]} and the {ctx[1]} are collected. {table(ctx[0], ctx[1], xs, ys)} (a) Describe the correlation shown when the data are plotted. (b) Write down the coordinates of the point that is an outlier. (c) Calculate the coordinates of the mean point of all the data.'
    return Q(stem, f'(a) {d} (b) ({num(out[0])}, {num(out[1])}) (c) ({ex(round(mx, 2))}, {ex(round(my, 2))})',
             f'(a) B1 {d} (b) B1 outlier (c) M1 mean of each; A1 ({ex(round(mx, 2))}, {ex(round(my, 2))}).', type='multi_step', marks=4)


def s4_c4(r, D):
    ctx, xs, ys, out = dataset(r, D, outlier=True)
    xs2 = [x for x, y in zip(xs, ys) if (x, y) != out]
    ys2 = [y for x, y in zip(xs, ys) if (x, y) != out]
    b, a = lsq(xs2, ys2)
    mx, my = sum(xs2) / len(xs2), sum(ys2) / len(ys2)
    lo, hi = min(xs), max(xs)
    xin = round((lo + hi) / 2 + (hi - lo) * 0.15, 0 if hi - lo >= 10 else 1)
    xout = round(hi + (hi - lo) * 0.8, 0 if hi - lo >= 10 else 1)
    yin = a + b * xin
    d = describe(pearson(xs2, ys2))
    nm = person(r)
    intro = f'{nm} records the {ctx[0]} and the {ctx[1]} for a project in {city(r)}. {table(ctx[0], ctx[1], xs, ys)}'
    parts = [
        P('Describe the correlation shown by the data.', d, 'B1', 1),
        P('Identify the outlier and suggest one reason why it might have occurred.', f'({num(out[0])}, {num(out[1])}); e.g. a recording error or an unusual day/person.', 'B1 point; B1 sensible reason', 2),
        P('Ignoring the outlier, calculate the mean of each variable.', f'({ex(round(mx, 2))}, {ex(round(my, 2))})', 'M1 sums ÷ number of values; A1 both', 2),
        P(f'A line of best fit, drawn through the mean point and ignoring the outlier, has gradient {n3(b)}. Use it to estimate the {ctx[1]} when the {ctx[0]} is {num(xin)}.', f'{n3(yin)} (accept a sensible value close to this)',
          f'M1 y − {ex(round(my, 2))} = {n3(b)}(x − {ex(round(mx, 2))}); A1 {n3(yin)}', 2),
        P(f'Explain why using the line to estimate the {ctx[1]} when the {ctx[0]} is {num(xout)} would not be reliable.', f'{num(xout)} is outside the range of the data ({num(lo)} to {num(hi)}), so this is extrapolation and the trend may not continue.', 'B1 outside range; B1 extrapolation/trend may not continue', 2),
        P(f'The line of best fit has gradient {n3(b)}. Interpret this value in context.', f'For each increase of 1 in the {ctx[0]}, the {ctx[1]} {"increases" if b > 0 else "decreases"} by about {n3(abs(b))}.', 'B1', 1),
    ]
    return cmp_(r, intro, parts, k=(3, 4))


s41.add('C4', (2, 3, 4, 5))(s4_c4)

# ---------------------------------------------------------------- lines of best fit
s42 = topic('Lines of best fit, interpolation and extrapolation', 'lines of best fit', 'interpolation and extrapolation', 'line of best fit')
s42.fixed('C1', (1, 2), [
    ('A line of best fit should pass through', 'the mean point (x̄, ȳ)', 'The mean point is a good balance point for the data.', ['the origin', 'the first and last points', 'the highest point']),
    ('Using a line of best fit to estimate a value inside the range of the data is called', 'interpolation', 'Inside the range: interpolation; outside: extrapolation.', ['extrapolation', 'correlation', 'regression to zero']),
    ('Using a line of best fit to estimate a value outside the range of the data is called', 'extrapolation', 'Extrapolation can be unreliable as the trend may not continue.', ['interpolation', 'estimation by mean', 'causation']),
    ('A line of best fit is only appropriate when the scatter diagram shows', 'correlation', 'With no correlation there is no linear trend to model.', ['no correlation', 'only one outlier', 'all points on the x-axis']),
    ('On a line of best fit, there should be roughly', 'the same number of points on each side', 'The line follows the trend with points balanced above and below.', ['all the points above it', 'all the points below it', 'every point on the line']),
])
s42.fixed('C2', (2, 3), [
    ('Explain why extrapolation can give unreliable estimates.', 'The relationship has only been observed within the range of the data; outside it the trend may change, so the estimate may be wrong.', 'B1 outside range of data; B1 trend may not continue [2]'),
    ('Explain why a line of best fit does not have to pass through the origin.', 'It represents the trend of the data, which may not start at (0, 0); forcing it through the origin could misrepresent the data.', 'B1 follows the data; B1 origin may not be meaningful [2]'),
    ('Explain why estimates from a line of best fit are more reliable when the correlation is strong.', 'The points lie close to the line, so actual values are likely to be close to the values read from it.', 'B1 points close to line; B1 smaller error [2]'),
    ('Explain why a line of best fit for weak correlation still gives only a rough estimate.', 'The points are widely spread around the line, so individual values could differ a lot from the estimate.', 'B1 wide spread; B1 rough estimate [2]'),
])


@s42.add('C1', (1, 2, 3))
def s42_ie(r, D):
    lo, hi = r.choice([(10, 40), (2, 12), (150, 190), (5, 30), (100, 600)])
    inside = r.random() < 0.5
    x = r.randint(lo + 1, hi - 1) if inside else r.choice([hi + (hi - lo) // 2, max(0, lo - (hi - lo) // 2)])
    c = 'Interpolation, which is likely to be reliable' if inside else 'Extrapolation, which may be unreliable'
    return SMC(r, f'Data were collected for values of x from {lo} to {hi}. A line of best fit is used to estimate y when x = {x}. Which statement is correct?', c,
               [x_ for x_ in ['Interpolation, which is likely to be reliable', 'Extrapolation, which may be unreliable', 'Interpolation, which is always unreliable', 'Extrapolation, which is always exact'] if x_ != c],
               f'x = {x} is {"inside" if inside else "outside"} {lo} to {hi}.')


@s42.add('C2', (2, 3, 4), 'explain')
def s42_err(r, D):
    ctx = r.choice(SCAT)
    xl, yl, sign, (lo, hi), m, k = ctx[:6]
    nm = person(r)
    x = hi * 3 if hi > 10 else hi * 2.5
    x = round(x, 1)
    pred = m * x + k
    return Q(f'Data on the {xl} and the {yl} were collected for values of the {ctx[7]} between {num(lo)} and {num(hi)}. The line of best fit is y = {lq(m, round(k, 1))}. {nm} uses it to predict the {yl} when the {ctx[7]} is {num(x)}, getting {n3(pred)}. Explain why this prediction may not be reliable.',
             f'{num(x)} is far outside the range of the data, so this is extrapolation; the trend may not continue' + (' (the value is not even realistic).' if (pred < 0) else '.'),
             'B1 outside data range/extrapolation; B1 trend may not continue or value unrealistic [2]')


@s42.add('C3', (1, 2, 3, 4))
def s42_use(r, D):
    ctx = r.choice(SCAT)
    xl, yl, sign, (lo, hi), m, k = ctx[:6]
    x = round(lo + (hi - lo) * r.uniform(0.2, 0.8), 0 if hi - lo >= 10 else 1)
    y = m * x + k
    if D <= 2:
        stem = f'The equation of a line of best fit for the {yl} (y) against the {xl} (x) is y = {lq(m, round(k, 2))}. Use it to estimate the {yl} when the {xl.split(" (")[0]} is {num(x)}.'
        if D == 1:
            return MC(r, stem.replace('Use it to estimate', 'Estimate'), round(y, 1), [round(m * x, 1), round(y + abs(k) / 2 + 1, 1), round(m + x + k, 1), round(-y, 1) if y else 3, round(y * 1.1 + 1, 1), round(y * 0.9 - 1, 1), round(y + 5, 1)], f'y = {n3(m)} × {num(x)}{sgn(round(k, 2))} = {ex(round(y, 1))}.', fmtf=lambda v: ex(v))
        return Q(stem, f'{n3(y)}', f'M1 substitute x = {num(x)}; A1 {n3(y)}.')
    y0 = round(y, 0 if abs(y) > 20 else 1)
    xa = (y0 - k) / m
    return Q(f'A line of best fit for the {yl} (y) against the {xl} (x) is y = {lq(m, round(k, 2))}. (a) Estimate the {xl.split(" (")[0]} when the {yl.split(" (")[0]} is {num(y0)}. (b) Interpret the gradient of the line in context.',
             f'(a) {n3(xa)} (b) For each unit increase in {xl.split(" (")[0]}, the {yl.split(" (")[0]} {"increases" if m > 0 else "decreases"} by about {n3(abs(m))}.',
             f'(a) M1 {num(y0)} = {lq(m, round(k, 2))}; A1 {n3(xa)} (b) B1 rate of change in context' + ('; B1 negative/positive direction stated.' if D != 3 else '.'), type='multi_step', marks=3 if D == 3 else 4)


@s42.add('C3', (2, 3, 4, 5))
def s42_line(r, D):
    ctx, xs, ys, _ = dataset(r, D, noise_mult=0.6)
    b, a = lsq(xs, ys)
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    x2 = max(xs)
    y2 = a + b * x2
    return Q(f'{table(ctx[0], ctx[1], xs, ys)} A line of best fit passes through the mean point and the point ({num(x2)}, {n3(y2)}). Calculate the mean point and find the equation of the line in the form y = mx + c.',
             f'Mean point ({ex(round(mx, 2))}, {ex(round(my, 2))}); y = {lq(b, float(n3(a).replace(MINUS, "-")))}',
             f'M1 means; A1 mean point; M1 gradient ({n3(y2)} − {ex(round(my, 2))}) ÷ ({num(x2)} − {ex(round(mx, 2))}) = {n3(b)}; A1 c = {n3(a)}.')


s42.add('C4', (2, 3, 4, 5))(s4_c4)


def s42_c4(r, D):
    ctx = r.choice(SCAT)
    xl, yl, sign, (lo, hi), m, k = ctx[:6]
    x1 = round(lo + (hi - lo) * 0.25, 1)
    x2 = round(lo + (hi - lo) * 0.85, 1)
    y1, y2 = m * x1 + k, m * x2 + k
    grad = (y2 - y1) / (x2 - x1)
    c = y1 - grad * x1
    xi = round(lo + (hi - lo) * 0.5, 1)
    intro = f'A researcher in {city(r)} draws a line of best fit for the {yl} (y) against the {xl} (x). The line passes through ({num(x1)}, {n3(y1)}) and ({num(x2)}, {n3(y2)}). Data were collected for x from {num(lo)} to {num(hi)}.'
    parts = [
        P('Calculate the gradient of the line.', n3(grad), f'M1 ({n3(y2)} − {n3(y1)}) ÷ ({num(x2)} − {num(x1)}); A1', 2),
        P('Find the equation of the line in the form y = mx + c.', f'y = {lq(grad, float(n3(c).replace(MINUS, "-")))}', 'M1 substitute a point; A1', 2),
        P(f'Use the line to estimate y when x = {num(xi)}.', n3(grad * xi + c), 'M1 substitute; A1', 2),
        P('State whether your estimate is an interpolation or an extrapolation and comment on its reliability.', f'Interpolation ({num(xi)} is within the data range), so it is fairly reliable if the correlation is strong.', 'B1 interpolation; B1 reliability comment', 2),
        P('Interpret the value of the gradient in context.', f'For each increase of 1 in the {xl.split(" (")[0]}, the {yl.split(" (")[0]} changes by about {n3(grad)}.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


s42.add('C4', (2, 3, 4, 5))(s42_c4)

# ---------------------------------------------------------------- correlation and causation
CAUSE = [
    ('ice cream sales', 'the number of people who get sunburnt', 'hot, sunny weather increases both'),
    ('the number of fire engines sent to a fire', 'the amount of damage caused', 'bigger fires need more engines and also cause more damage'),
    ('the number of libraries in a town', 'the number of crimes recorded', 'larger populations have more of both'),
    ('shoe size of children', 'reading ability', 'older children have bigger feet and also read better'),
    ('the number of air conditioners sold', 'the number of drowning incidents', 'hot weather increases both'),
    ('hours of television watched', 'number of hours of sleep', 'free time and age affect both'),
    ('the number of mobile phones in a country', 'life expectancy', 'wealth of the country increases both'),
    ('coffee shops in a district', 'average house price', 'wealthier, busier districts have more of both'),
    ('umbrellas sold', 'number of traffic accidents', 'rainy weather increases both'),
    ('the number of teachers in a city', 'the number of cars', 'larger cities have more of both'),
]

s43 = topic('Correlation and causation', 'correlation and causation in context', 'causation', 'correlation causation')
s43.fixed('C1', (1, 2), [
    ('Two variables show strong positive correlation. Which statement must be true?', 'Higher values of one tend to go with higher values of the other', 'Correlation describes an association, not a cause.', ['One variable causes the other to increase', 'The variables are always equal', 'There are no outliers']),
    ('A third factor that affects both of two correlated variables is called', 'a confounding (hidden) variable', 'A hidden third variable can create a correlation without direct cause.', ['an outlier', 'a line of best fit', 'the mean point']),
    ('Which statement about correlation and causation is correct?', 'Correlation does not prove causation', 'An association alone does not show that one variable changes the other.', ['Correlation always proves causation', 'Causation is impossible if there is correlation', 'Weak correlation proves causation']),
    ('Which situation is most likely to be a genuine cause-and-effect relationship?', 'Distance driven and fuel used', 'Driving further directly uses more fuel.', ['Shoe size and reading ability in children', 'Ice cream sales and sunburn cases', 'Number of libraries and number of crimes']),
])
s43.fixed('C2', (2, 3), [
    ('Explain the difference between correlation and causation.', 'Correlation means two variables tend to change together; causation means a change in one directly produces a change in the other. Correlation alone does not show causation.', 'B1 correlation definition; B1 causation definition/distinction [2]'),
    ('Explain why a scientist would carry out a controlled experiment rather than rely on a scatter diagram to show causation.', 'In an experiment other variables can be kept the same, so any change can be linked to the variable being changed; a scatter diagram may reflect a hidden third variable.', 'B1 control other variables; B1 rules out confounders [2]'),
    ('Explain why a correlation found in a small sample may be misleading.', 'With few data points a pattern can happen by chance or be caused by one or two unusual values, so it may not hold for the whole population.', 'B1 chance/outliers; B1 may not generalise [2]'),
])


@s43.add('C1', (1, 2, 3))
def s43_conf(r, D):
    a, b, why = r.choice(CAUSE)
    return SMC(r, f'Data from {city(r)} show positive correlation between {a} and {b}. What is the most likely explanation?', f'A third factor: {why}',
               ['An increase in ' + a + ' directly causes ' + b + ' to increase', 'The data must have been recorded incorrectly', 'There is no relationship of any kind', f'{b[0].upper() + b[1:]} directly causes {a} to rise'],
               f'This is a correlation caused by a confounding variable: {why}.')


@s43.add('C2', (2, 3, 4), 'explain')
def s43_claim(r, D):
    a, b, why = r.choice(CAUSE)
    nm = person(r)
    st = r.choice(['strong', 'weak', 'clear'])
    return Q(f'A report from {city(r)} shows {st} positive correlation between {a} and {b}. {nm} concludes that increasing {a} causes {b} to increase. Explain why this conclusion may not be valid.',
             f'Correlation does not prove causation; both are likely to be linked to a third factor ({why}).', 'B1 correlation ≠ causation; B1 identifies a plausible confounding factor [2]')


@s43.add('C3', (2, 3, 4, 5))
def s43_data(r, D):
    a, b, why = r.choice(CAUSE)
    n = r.choice([7, 8, 9])
    xs = sorted(r.sample(range(10, 90), n))
    ys = [round(0.6 * x + 12 + r.uniform(-7, 7)) for x in xs]
    rv = pearson(xs, ys)
    mx, my = sum(xs) / n, sum(ys) / n
    return Q(f'A council in {city(r)} records, for {n} districts, an index of {a} (x) and of {b} (y). x: ' + ', '.join(map(str, xs)) + '. y: ' + ', '.join(map(str, ys)) +
             f'. (a) Describe the correlation. (b) Calculate the mean point. (c) A councillor says reducing {a} would reduce {b}. Evaluate this claim.',
             f'(a) {describe(rv)} (b) ({ex(round(mx, 2))}, {ex(round(my, 2))}) (c) Not justified: correlation does not show causation; likely third factor — {why}.',
             f'(a) B1 (b) M1 A1 (c) B1 correlation ≠ causation; B1 confounder named.', type='multi_step', marks=5)


def s43_c4(r, D):
    a, b, why = r.choice(CAUSE)
    nm = person(r)
    ctx = r.choice([c for c in SCAT if c[7] in ('temperature', 'revision time', 'household size', 'practice shots')])
    _, xs, ys, _ = dataset(r, D, ctx=ctx, noise_mult=0.8)
    rv = pearson(xs, ys)
    intro = f'{nm} is investigating claims made in a newspaper in {city(r)}. {table(ctx[0], ctx[1], xs, ys)}'
    parts = [
        P('Describe the correlation in these data.', describe(rv), 'B1', 1),
        P(f'State whether you think a change in the {ctx[7]} could directly cause a change in the {ctx[8]}. Give a reason.', 'A plausible direct link exists in this context, but the data alone cannot prove it.', 'B1 judgement; B1 reason referring to context', 2),
        P(f'The newspaper also reports correlation between {a} and {b}, and claims one causes the other. Explain why this is unlikely and suggest a third variable.', f'More likely a confounding variable: {why}.', 'B1 correlation ≠ causation; B1 third variable', 2),
        P('Suggest how a fair test could be designed to investigate whether one variable causes the other.', 'Change one variable while controlling all others (e.g. randomised groups), then compare the effect.', 'B1 control variables; B1 compare groups', 2),
    ]
    return cmp_(r, intro, parts)


s43.add('C4', (2, 3, 4, 5))(s43_c4)
CHAPTERS[4] = [s41, s42, s43]


# =========================================================== 5 Managing money (Ch 17)
def cur(r):
    return r.choice(['$', '€', '$', '£'])


def mon(c, x):
    return f'{c}{x:,.2f}'


JOBS = ['shop assistant', 'nurse', 'chef', 'delivery driver', 'lifeguard', 'hotel receptionist', 'factory worker', 'call-centre adviser', 'bus driver', 'gardener']

f1 = topic('Earning money', 'earning money', 'wages, salaries, commission and deductions', 'wages salaries')
f1.fixed('C1', (1, 2), [
    ('What is a salary?', 'A fixed amount paid per year, usually in equal monthly parts', 'Salary: annual amount; wages are paid per hour worked.', ['Pay for each hour worked', 'A percentage of the value of sales', 'Money paid only for overtime']),
    ('What is commission?', 'Pay calculated as a percentage of the value of sales made', 'Sales staff often earn commission on top of a basic wage.', ['A fixed weekly payment', 'Tax deducted from pay', 'Pay for working at weekends']),
    ('Gross pay is', 'total pay before any deductions', 'Net pay = gross pay − deductions (tax, pension, insurance).', ['pay after tax has been taken off', 'the amount of tax paid', 'pay for overtime only']),
    ('Overtime paid at "time and a half" means each hour is paid at', '1.5 times the normal hourly rate', '"Time and a half" = 1.5 × basic rate; "double time" = 2 ×.', ['half the normal rate', 'the normal rate plus $1.50', '2 times the normal rate']),
    ('A worker earns $12.50 per hour for 38 hours. What is the gross pay?', '$475', '12.50 × 38 = 475.', ['$450.50', '$487.50', '$380']),
    ('Which of these is usually a deduction from gross pay?', 'Income tax', 'Tax, pension and insurance contributions are deducted.', ['Overtime', 'Commission', 'Bonus']),
])
f1.fixed('C2', (2, 3), [
    ('Explain the difference between gross pay and net pay.', 'Gross pay is the total earned before deductions; net pay is what is left after deductions such as tax and pension have been taken off.', 'B1 gross before deductions; B1 net after deductions [2]'),
    ('Explain why a salesperson might prefer a lower basic wage with commission to a higher fixed wage.', 'If they make many sales, commission can make total pay higher than the fixed wage; their pay rewards their effort.', 'B1 commission increases with sales; B1 can exceed fixed wage [2]'),
    ('Explain why a person paid a salary does not receive more money for working extra hours, while a person on an hourly wage does.', 'A salary is a fixed amount for the year whatever the hours; a wage is paid per hour, so extra hours (often at overtime rates) increase pay.', 'B1 salary fixed; B1 wage per hour [2]'),
    ('Explain what a tax-free allowance is and how it affects the tax paid.', 'It is the amount of income on which no tax is charged; tax is only paid on income above the allowance.', 'B1 untaxed amount; B1 tax on remainder only [2]'),
])


@f1.add('C1', (1, 2, 3))
def f1_q(r, D):
    c = cur(r)
    rate = r.choice([9.5, 10, 11.2, 12.5, 14, 15.6, 18])
    h = r.choice([20, 25, 32, 35, 37.5, 40])
    p = rate * h
    return MC(r, f'A {r.choice(JOBS)} is paid {mon(c, rate)} per hour and works {ex(h)} hours in a week. What is the gross pay for the week?', p,
              [p * 1.5, rate + h, p / 2, rate * (h - 5), rate * (h + 5)], f'{ex(rate)} × {ex(h)} = {ex(round(p, 2))}.', fmtf=lambda x: mon(c, x))


@f1.add('C2', (2, 3, 4), 'explain')
def f1_err(r, D):
    c = cur(r)
    nm = person(r)
    rate = r.choice([10, 12, 13.5, 14.8, 16])
    base = r.choice([35, 37, 38, 40])
    ot = r.choice([4, 5, 6, 8])
    right = rate * base + rate * 1.5 * ot
    wrong = rate * 1.5 * (base + ot)
    return Q(f'{nm} is paid {mon(c, rate)} per hour for the first {base} hours each week and time and a half for any extra hours. {nm} works {base + ot} hours and says the pay is {base + ot} × {mon(c, rate * 1.5)} = {mon(c, wrong)}. Explain the error and calculate the correct pay.',
             f'Only the {ot} extra hours are paid at time and a half; the first {base} hours are at the normal rate. Correct pay = {mon(c, right)}.',
             f'B1 identifies that only overtime hours get 1.5 ×; M1 {base} × {ex(rate)} + {ot} × {ex(rate * 1.5)}; A1 {mon(c, right)} [3]', marks=3)


@f1.add('C3', (1, 2, 3, 4))
def f1_ot(r, D):
    c = cur(r)
    rate = r.choice([9, 10.5, 12, 13.6, 15, 16.4, 18.5])
    base = r.choice([35, 36, 38, 40])
    ot1 = r.choice([3, 4, 5, 6, 7.5])
    ot2 = r.choice([2, 3, 4]) if D >= 3 else 0
    pay = rate * base + 1.5 * rate * ot1 + 2 * rate * ot2
    job = r.choice(JOBS)
    if D == 1:
        return MC(r, f'A {job} earns {mon(c, rate)} per hour. Overtime is paid at time and a half. What is the overtime rate per hour?', rate * 1.5, [rate + 1.5, rate * 2, rate * 0.5, rate + 0.5], f'{ex(rate)} × 1.5 = {ex(rate * 1.5)}.', fmtf=lambda x: mon(c, x))
    stem = f'A {job} in {city(r)} is paid {mon(c, rate)} per hour for a basic {base}-hour week. Overtime on weekdays is paid at time and a half' + (' and on Sundays at double time' if ot2 else '') + f'. One week they work {base} basic hours, {ex(ot1)} hours of weekday overtime' + (f' and {ot2} hours on Sunday' if ot2 else '') + '. Calculate their gross pay.'
    return Q(stem, mon(c, pay), f'M1 {base} × {ex(rate)} = {ex(rate * base)}; M1 {ex(ot1)} × {ex(rate * 1.5)}' + (f'; M1 {ot2} × {ex(rate * 2)}' if ot2 else '') + f'; A1 {mon(c, pay)}.')


@f1.add('C3', (2, 3, 4, 5))
def f1_comm(r, D):
    c = cur(r)
    basic = r.choice([250, 300, 320, 350, 400])
    pct = r.choice([2, 2.5, 3, 4, 5, 6])
    sales = r.choice([4800, 6250, 8400, 9600, 12500, 15200])
    tot = basic + sales * pct / 100
    nm = person(r)
    item = r.choice(['cars', 'phones', 'furniture', 'holidays', 'solar panels'])
    if D >= 4:
        target = r.choice([700, 750, 800, 900])
        need = (target - basic) / (pct / 100)
        return Q(f'{nm} sells {item} in {city(r)} and earns a basic {mon(c, basic)} per week plus {ex(pct)}% commission on sales. Calculate the value of sales {nm} needs in one week to earn {mon(c, target)}.', mon(c, need),
                 f'M1 commission needed = {target} − {basic} = {target - basic}; M1 ÷ {ex(pct / 100)}; A1 {mon(c, need)}.')
    return Q(f'{nm} sells {item} and earns a basic {mon(c, basic)} per week plus {ex(pct)}% commission on all sales. One week {nm} sells {mon(c, sales)} worth of {item}. Calculate {nm}\'s total pay for the week.', mon(c, tot),
             f'M1 {ex(pct)}% of {sales} = {ex(sales * pct / 100)}; A1 {mon(c, tot)}.')


@f1.add('C3', (2, 3, 4, 5))
def f1_tax(r, D):
    c = cur(r)
    sal = r.choice([24000, 28500, 32000, 36400, 41000, 48500, 52000])
    allow = r.choice([10000, 12000, 12500, 15000])
    t = r.choice([15, 18, 20, 22, 25])
    tax = (sal - allow) * t / 100
    net = sal - tax
    nm = person(r)
    if D >= 4:
        pen = r.choice([3, 4, 5, 6])
        pv = sal * pen / 100
        netm = (sal - tax - pv) / 12
        return Q(f'{nm} earns an annual salary of {mon(c, sal)}. The first {mon(c, allow)} is tax-free and the rest is taxed at {t}%. {nm} also pays {pen}% of the full salary into a pension. Calculate {nm}\'s net monthly pay.', mon(c, netm),
                 f'M1 taxable = {sal - allow}; M1 tax = {ex(tax)}; M1 pension = {ex(pv)}; M1 ({sal} − {ex(tax)} − {ex(pv)}) ÷ 12; A1 {mon(c, netm)}.')
    return Q(f'{nm} earns {mon(c, sal)} per year. Income tax is not paid on the first {mon(c, allow)} and is {t}% on the rest. Calculate the amount of tax {nm} pays each year and the net annual pay.', f'Tax {mon(c, tax)}; net pay {mon(c, net)}',
             f'M1 {sal} − {allow} = {sal - allow}; M1 × {t}%; A1 tax {mon(c, tax)}; A1 net {mon(c, net)}.')


def f1_c4(r, D):
    c = cur(r)
    nm = person(r)
    rate = r.choice([11, 12.4, 13.5, 14.2, 15.8])
    base = r.choice([36, 38, 40])
    ot = r.choice([4, 5, 6, 8])
    gross = rate * base + rate * 1.5 * ot
    t = r.choice([12, 15, 18, 20])
    allow = r.choice([150, 200, 220, 250])
    tax = (gross - allow) * t / 100
    ins = r.choice([2, 3, 4])
    insv = gross * ins / 100
    net = gross - tax - insv
    sal = round(gross * 52 * r.choice([0.95, 0.97, 1.03, 1.05]), -2)
    intro = f'{nm} works as a {r.choice(JOBS)} in {city(r)}. The basic rate is {mon(c, rate)} per hour for {base} hours a week, with overtime at time and a half. One week {nm} works {base + ot} hours. Each week the first {mon(c, allow)} of pay is tax-free, the rest is taxed at {t}%, and {ins}% of gross pay is deducted for insurance.'
    parts = [
        P('Calculate the gross pay for the week.', mon(c, gross), f'M1 {base} × {ex(rate)}; M1 {ot} × {ex(rate * 1.5)}; A1 {mon(c, gross)}', 3),
        P('Calculate the tax paid.', mon(c, tax), f'M1 ({ex(round(gross, 2))} − {allow}) × {t}%; A1 {mon(c, tax)}', 2),
        P('Calculate the net pay.', mon(c, net), f'M1 gross − tax − {ins}% insurance ({ex(round(insv, 2))}); A1 {mon(c, net)}', 2),
        P('Calculate the net pay as a percentage of the gross pay.', f'{n3(net / gross * 100)}%', 'M1 net ÷ gross × 100; A1', 2),
        P(f'{nm} is offered an annual salary of {mon(c, sal)} instead. Assuming the same hours every week for 52 weeks, state with a reason which option gives the higher gross pay.',
          ('The hourly option' if gross * 52 > sal else 'The salary') + f' (hourly gives {mon(c, gross * 52)} a year)', f'M1 {ex(round(gross, 2))} × 52 = {ex(round(gross * 52, 2))}; A1 comparison', 2),
    ]
    return cmp_(r, intro, parts)


f1.add('C4', (2, 3, 4, 5))(f1_c4)

# ---------------------------------------------------------------- interest
f2 = topic('Simple and compound interest', 'simple and compound interest', 'simple interest', 'compound interest')
f2.fixed('C1', (1, 2), [
    ('Which formula gives simple interest I on principal P at rate r% per year for n years?', 'I = Prn/100', 'Simple interest is the same each year: P × r/100 × n.', ['I = P(1 + r/100)ⁿ', 'I = P + rn', 'I = Pr/100n']),
    ('Which formula gives the value A of P invested at r% compound interest for n years?', 'A = P(1 + r/100)ⁿ', 'Each year the value is multiplied by (1 + r/100).', ['A = P + Prn/100', 'A = P(1 + rn/100)', 'A = P(r/100)ⁿ']),
    ('$1000 is invested at 5% compound interest per year. What is the value after 2 years?', '$1102.50', '1000 × 1.05² = 1102.50.', ['$1100', '$1050', '$1105']),
    ('Compound interest is interest that is', 'paid on the original amount and on interest already earned', 'Interest is added to the balance, which then earns interest itself.', ['paid only on the original amount', 'the same every year', 'only paid once at the end']),
    ('What is the simple interest on $600 at 4% per year for 3 years?', '$72', '600 × 0.04 × 3 = 72.', ['$24', '$674.92', '$75']),
])
f2.fixed('C2', (2, 3), [
    ('Explain why compound interest gives more than simple interest at the same rate after several years.', 'With compound interest, interest is earned on previous interest as well as the principal, so the amount added grows each year; simple interest adds the same amount each year.', 'B1 interest on interest; B1 simple interest constant [2]'),
    ('Explain why after 1 year simple and compound interest give the same amount.', 'In the first year both calculate interest on the original principal only; the difference starts once interest is added to the balance.', 'B1 both on principal in year 1; B1 difference from year 2 [2]'),
    ('Explain what the number 1.035 represents in the calculation 2000 × 1.035⁴.', 'It is the multiplier for an increase of 3.5% each year (100% + 3.5%).', 'B1 multiplier; B1 3.5% increase per year [2]'),
])


@f2.add('C1', (1, 2, 3))
def f2_si(r, D):
    c = cur(r)
    P_ = r.choice([400, 500, 800, 1200, 1500, 2500])
    rt = r.choice([2, 3, 4, 5, 6])
    n = r.choice([2, 3, 4, 5])
    I = P_ * rt * n / 100
    return MC(r, f'Calculate the simple interest on {mon(c, P_)} invested at {rt}% per year for {n} years.', I,
              [P_ * rt / 100, P_ + I, P_ * ((1 + rt / 100) ** n - 1), I * 2, P_ * rt * n / 10], f'I = {P_} × {rt} × {n} ÷ 100 = {ex(I)}.', fmtf=lambda x: mon(c, x))


@f2.add('C2', (2, 3, 4), 'explain')
def f2_err(r, D):
    c = cur(r)
    nm = person(r)
    P_ = r.choice([2000, 3500, 5000, 8000])
    rt = r.choice([2.5, 3, 4, 4.5, 6])
    n = r.choice([3, 4, 5, 6])
    right = P_ * (1 + rt / 100) ** n
    if r.random() < 0.5:
        wrong = P_ * (1 + rt * n / 100)
        return Q(f'{nm} invests {mon(c, P_)} at {ex(rt)}% per year compound interest for {n} years and calculates the final amount as {P_} × (1 + {ex(rt)} × {n} ÷ 100) = {mon(c, wrong)}. Explain the error and find the correct amount.',
                 f'This is simple interest; compound interest multiplies by {ex(1 + rt / 100)} each year: {P_} × {ex(1 + rt / 100)}{sup(n)} = {mon(c, right)}.', f'B1 recognises simple interest used; M1 {P_} × {ex(1 + rt / 100)}{sup(n)}; A1 {mon(c, right)} [3]', marks=3)
    return Q(f'{nm} wants the value of {mon(c, P_)} after {n} years at {ex(rt)}% compound interest and types {P_} × {ex(rt)}{sup(n)} into a calculator. Explain the error and find the correct value.',
             f'The multiplier for a {ex(rt)}% increase is {ex(1 + rt / 100)}, not {ex(rt)}: {P_} × {ex(1 + rt / 100)}{sup(n)} = {mon(c, right)}.', f'B1 multiplier should be 1 + r/100; M1 correct calculation; A1 {mon(c, right)} [3]', marks=3)


@f2.add('C3', (1, 2, 3, 4))
def f2_ci(r, D):
    c = cur(r)
    P_ = r.choice([1500, 2400, 3000, 4500, 6000, 12000])
    rt = r.choice([2, 2.5, 3, 3.2, 4, 4.5, 5])
    n = r.choice([2, 3, 4, 5, 6, 8])
    A = P_ * (1 + rt / 100) ** n
    nm = person(r)
    if D <= 2:
        return Q(f'{nm} invests {mon(c, P_)} at {ex(rt)}% per year compound interest. Calculate the value of the investment after {n} years.', mon(c, A), f'M1 {P_} × {ex(1 + rt / 100)}{sup(n)}; A1 {mon(c, A)}.')
    return Q(f'{nm} invests {mon(c, P_)} in a bank in {city(r)} at {ex(rt)}% per year compound interest. Calculate the total interest earned after {n} years.', mon(c, A - P_),
             f'M1 {P_} × {ex(1 + rt / 100)}{sup(n)} = {ex(round(A, 2))}; M1 − {P_}; A1 {mon(c, A - P_)}.')


@f2.add('C3', (2, 3, 4, 5))
def f2_reverse(r, D):
    c = cur(r)
    kind = r.choice(['rate', 'time', 'principal', 'years'])
    nm = person(r)
    if kind == 'rate':
        P_, n = r.choice([800, 1200, 2000, 2500]), r.choice([2, 3, 4, 5])
        rt = r.choice([1.5, 2, 2.5, 3, 3.5, 4])
        I = P_ * rt * n / 100
        return Q(f'{nm} invests {mon(c, P_)} at simple interest. After {n} years the interest earned is {mon(c, I)}. Calculate the rate of interest per year.', f'{ex(rt)}%', f'M1 {ex(I)} = {P_} × r × {n} ÷ 100; A1 r = {ex(rt)}%.')
    if kind == 'time':
        P_, rt = r.choice([500, 1500, 2400, 3000]), r.choice([2, 3, 4, 5])
        n = r.choice([3, 4, 5, 6, 7])
        I = P_ * rt * n / 100
        return Q(f'How many years will it take for {mon(c, P_)} to earn {mon(c, I)} simple interest at {rt}% per year?', f'{n} years', f'M1 {ex(I)} ÷ ({P_} × {rt}/100); A1 {n} years.')
    if kind == 'principal':
        rt = r.choice([2, 3, 4, 5])
        n = r.choice([2, 3, 4])
        P_ = r.choice([2000, 2500, 4000, 5000])
        A = P_ * (1 + rt / 100) ** n
        return Q(f'An investment earns {rt}% per year compound interest. After {n} years it is worth {mon(c, A)}. Calculate the amount originally invested.', mon(c, P_),
                 f'M1 P × {ex(1 + rt / 100)}{sup(n)} = {ex(round(A, 2))}; M1 P = {ex(round(A, 2))} ÷ {ex(round((1 + rt / 100) ** n, 6))}; A1 {mon(c, P_)}.')
    P_ = r.choice([1000, 2000, 5000])
    rt = r.choice([3, 4, 5, 6, 7])
    target = P_ * r.choice([1.25, 1.4, 1.5, 2])
    n = math.ceil(math.log(target / P_) / math.log(1 + rt / 100) - 1e-12)
    return Q(f'{mon(c, P_)} is invested at {rt}% per year compound interest. Find the least number of complete years needed for the investment to be worth more than {mon(c, target)}.', f'{n} years',
             f'M1 trial {P_} × {ex(1 + rt / 100)}ⁿ; M1 shows n = {n - 1} gives {mon(c, P_ * (1 + rt / 100) ** (n - 1))} and n = {n} gives {mon(c, P_ * (1 + rt / 100) ** n)}; A1 {n}.')


def f2_c4(r, D):
    c = cur(r)
    nm = person(r)
    P_ = r.choice([3000, 4000, 5000, 8000, 10000])
    s_rt = r.choice([3.5, 4, 4.5, 5])
    c_rt = round(s_rt - r.choice([0.3, 0.5, 0.6]), 1)
    n = r.choice([4, 5, 6, 8, 10])
    S = P_ * (1 + s_rt * n / 100)
    C = P_ * (1 + c_rt / 100) ** n
    better = 'Bank A (simple)' if S > C else 'Bank B (compound)'
    nn = 1
    while P_ * (1 + c_rt / 100) ** nn <= P_ * (1 + s_rt * nn / 100):
        nn += 1
        if nn > 60:
            break
    intro = f'{nm} has {mon(c, P_)} to invest in {city(r)}. Bank A offers {ex(s_rt)}% per year simple interest. Bank B offers {ex(c_rt)}% per year compound interest.'
    parts = [
        P(f'Calculate the total value with Bank A after {n} years.', mon(c, S), f'M1 {P_} × {ex(s_rt)} × {n}/100; A1 {mon(c, S)}', 2),
        P(f'Calculate the total value with Bank B after {n} years.', mon(c, C), f'M1 {P_} × {ex(1 + c_rt / 100)}{sup(n)}; A1 {mon(c, C)}', 2),
        P(f'State which bank gives more after {n} years and by how much.', f'{better}, by {mon(c, abs(S - C))}', 'B1 B1', 2),
        P('Find the least number of complete years after which Bank B is worth more than Bank A.', f'{nn} years', 'M1 compares values year by year; A1', 3) if nn <= 60 else None,
        P('Explain why Bank B eventually overtakes Bank A even though its rate is lower.', 'Compound interest grows exponentially (interest on interest) while simple interest grows by a fixed amount each year.', 'B1', 1),
    ]
    return cmp_(r, intro, [p for p in parts if p])


f2.add('C4', (2, 3, 4, 5))(f2_c4)

# ---------------------------------------------------------------- profit, loss, discount
f3 = topic('Profit, loss, discount and percentage change', 'profit, loss, discount', 'percentage change in buying and selling', 'profit and loss')
f3.fixed('C1', (1, 2), [
    ('A shop buys a lamp for $40 and sells it for $50. What is the percentage profit?', '25%', 'Profit 10 ÷ cost 40 × 100 = 25%.', ['20%', '10%', '125%']),
    ('Which calculation gives the percentage change from an old value to a new value?', '(new − old) ÷ old × 100', 'Percentage change is always relative to the original value.', ['(new − old) ÷ new × 100', 'new ÷ old × 100', '(old − new) ÷ new × 100']),
    ('A price of $80 is reduced by 15%. What is the sale price?', '$68', '80 × 0.85 = 68.', ['$65', '$12', '$92']),
    ('After a 20% increase a price is $60. What was the original price?', '$50', '60 ÷ 1.2 = 50.', ['$48', '$72', '$40']),
    ('Which multiplier reduces an amount by 35%?', '0.65', '100% − 35% = 65% = 0.65.', ['0.35', '1.35', '−0.35']),
    ('Selling an item for less than it cost is called', 'a loss', 'Loss = cost price − selling price.', ['a profit', 'a discount', 'commission']),
])
f3.fixed('C2', (2, 3), [
    ('A price is increased by 10% and then decreased by 10%. Explain why it does not return to the original price.', 'The 10% decrease is taken from the larger, increased price, so more is taken off than was added: 1.1 × 0.9 = 0.99, a 1% loss overall.', 'B1 second percentage of a different amount; B1 overall multiplier 0.99 [2]'),
    ('Explain why you divide by 0.8, not multiply by 1.2, to find the original price of an item after a 20% discount.', 'The sale price is 80% of the original, so original = sale price ÷ 0.8; adding 20% of the sale price uses the wrong base.', 'B1 sale = 80% of original; B1 divide by 0.8 [2]'),
    ('Explain why percentage profit is calculated using the cost price and not the selling price.', 'Percentage profit measures the gain relative to the amount spent (the original value), which is the cost price.', 'B1 relative to original; B1 cost price is original [2]'),
])


@f3.add('C1', (1, 2, 3))
def f3_q(r, D):
    c = cur(r)
    p = r.choice([24, 36, 45, 60, 80, 120, 150, 240])
    pc = r.choice([5, 10, 15, 20, 25, 30, 40])
    up = r.random() < 0.5
    v = p * (1 + pc / 100) if up else p * (1 - pc / 100)
    return MC(r, f'A price of {mon(c, p)} is {"increased" if up else "decreased"} by {pc}%. What is the new price?', v,
              [p * pc / 100, p * (1 - pc / 100) if up else p * (1 + pc / 100), p + pc if up else p - pc, v + 1], f'Multiplier {ex(1 + pc / 100) if up else ex(1 - pc / 100)}: {p} × {ex(1 + pc / 100) if up else ex(1 - pc / 100)} = {ex(v)}.', fmtf=lambda x: mon(c, x))


@f3.add('C2', (2, 3, 4), 'explain')
def f3_err(r, D):
    c = cur(r)
    nm = person(r)
    orig = r.choice([40, 60, 75, 120, 150, 250, 320])
    pc = r.choice([10, 15, 20, 25, 30, 40])
    sale = orig * (1 - pc / 100)
    wrong = sale * (1 + pc / 100)
    item = r.choice(['jacket', 'tablet', 'bicycle', 'rug', 'printer', 'guitar'])
    return Q(f'In a sale, a {item} costs {mon(c, sale)} after {an(pc)}% discount. {nm} finds the original price by adding {pc}% of {mon(c, sale)} and gets {mon(c, wrong)}. Explain why this is wrong and find the original price.',
             f'The discount was {pc}% of the original price, not of the sale price. Sale price = {100 - pc}% of original, so original = {ex(sale)} ÷ {ex(1 - pc / 100)} = {mon(c, orig)}.',
             f'B1 percentage of the wrong amount; M1 ÷ {ex(1 - pc / 100)}; A1 {mon(c, orig)} [3]', marks=3)


@f3.add('C3', (1, 2, 3, 4, 5))
def f3_calc(r, D):
    c = cur(r)
    kind = r.choice(['profit', 'reverse', 'change', 'sell'])
    nm = person(r)
    item = r.choice(['smartwatch', 'sofa', 'pair of boots', 'microwave', 'scooter', 'painting', 'used car'])
    if kind == 'profit' or D == 1:
        cost = r.choice([40, 64, 80, 125, 160, 240, 450, 2400])
        pc = r.choice([12.5, 15, 20, 25, 35, 40, -10, -20])
        sell = cost * (1 + pc / 100)
        w = 'profit' if pc > 0 else 'loss'
        if D == 1:
            return MC(r, f'{nm} buys a {item} for {mon(c, cost)} and sells it for {mon(c, sell)}. What is the percentage {w}?', abs(pc), [abs(pc) * cost / sell, abs(sell - cost), 100 + abs(pc), abs(pc) / 2], f'{w.capitalize()} = {ex(abs(sell - cost))}; ÷ {cost} × 100 = {ex(abs(pc))}%.', fmtf=lambda x: f'{n3(x)}%')
        return Q(f'{nm} buys a {item} for {mon(c, cost)} and sells it for {mon(c, sell)}. Calculate the percentage {w}.', f'{ex(abs(pc))}%', f'M1 {w} = {ex(abs(sell - cost))}; M1 ÷ {cost} × 100; A1 {ex(abs(pc))}%.')
    if kind == 'reverse':
        orig = r.choice([45, 80, 120, 180, 250, 640, 1500])
        pc = r.choice([8, 12, 15, 20, 25, 35])
        up = r.random() < 0.5
        new = orig * (1 + pc / 100) if up else orig * (1 - pc / 100)
        why = r.choice(['including sales tax' if up else 'after a sale reduction', 'after a price rise' if up else 'after a discount'])
        return Q(f'The price of a {item} is {mon(c, new)} {why} of {pc}%. Calculate the price before the {"increase" if up else "reduction"}.', mon(c, orig),
                 f'M1 {mon(c, new)} = {ex(1 + pc / 100) if up else ex(1 - pc / 100)} × original; M1 ÷ {ex(1 + pc / 100) if up else ex(1 - pc / 100)}; A1 {mon(c, orig)}.')
    if kind == 'change':
        a = r.choice([1.85, 2.4, 3.2, 4.5, 12.8, 36, 250])
        b = round(a * r.uniform(0.7, 1.4), 2)
        ch = (b - a) / a * 100
        return Q(f'The price of a {r.choice(["litre of fuel", "loaf of bread", "bus ticket", "kilogram of rice", "concert ticket"])} in {city(r)} changed from {mon(c, a)} to {mon(c, b)}. Calculate the percentage change, stating whether it is an increase or a decrease.',
                 f'{n3(abs(ch))}% {"increase" if ch > 0 else "decrease"}', f'M1 ({ex(b)} − {ex(a)}) ÷ {ex(a)} × 100; A1 {n3(abs(ch))}% {"increase" if ch > 0 else "decrease"}.')
    cost = r.choice([12, 18, 25, 32, 48])
    mk = r.choice([40, 50, 60, 75, 80])
    disc = r.choice([10, 15, 20, 25])
    sp = cost * (1 + mk / 100) * (1 - disc / 100)
    prof = (sp - cost) / cost * 100
    return Q(f'A shop buys {item}s for {mon(c, cost)} each and marks the price up by {mk}%. In a sale the marked price is reduced by {disc}%. Calculate the sale price and the overall percentage profit.',
             f'Sale price {mon(c, sp)}; profit {n3(prof)}%', f'M1 {cost} × {ex(1 + mk / 100)} = {ex(cost * (1 + mk / 100))}; M1 × {ex(1 - disc / 100)}; A1 {mon(c, sp)}; A1 {n3(prof)}%.')


def f3_c4(r, D):
    c = cur(r)
    nm = person(r)
    n = r.choice([40, 50, 60, 80, 120])
    cost = r.choice([6, 7.5, 8, 12, 15])
    mk = r.choice([40, 50, 60, 80])
    sold = r.choice([0.6, 0.7, 0.75, 0.8])
    disc = r.choice([20, 25, 30, 40])
    price = cost * (1 + mk / 100)
    n1 = int(n * sold)
    n2 = n - n1
    rev = n1 * price + n2 * price * (1 - disc / 100)
    tc = n * cost
    pp = (rev - tc) / tc * 100
    item = r.choice(['T-shirts', 'phone cases', 'scarves', 'water bottles', 'caps'])
    intro = f'{nm} runs a market stall in {city(r)} and buys {n} {item} for {mon(c, cost)} each. {nm} sells them at {an(mk)}% mark-up. After selling {n1} of them, {nm} reduces the price of the rest by {disc}% and sells them all.'
    parts = [
        P('Calculate the original selling price of one item.', mon(c, price), f'M1 {ex(cost)} × {ex(1 + mk / 100)}; A1', 2),
        P('Calculate the reduced price of one item.', mon(c, price * (1 - disc / 100)), f'M1 × {ex(1 - disc / 100)}; A1', 2),
        P('Calculate the total money received.', mon(c, rev), f'M1 {n1} × {ex(price)} + {n2} × {ex(round(price * (1 - disc / 100), 2))}; A1 {mon(c, rev)}', 2),
        P('Calculate the overall percentage profit.', f'{n3(pp)}%', f'M1 profit = {ex(round(rev - tc, 2))}; M1 ÷ {ex(tc)} × 100; A1 {n3(pp)}%', 3),
        P(f'Explain why the overall percentage profit is less than {mk}%.', f'Some items were sold at a reduced price, so the average selling price is lower than the full {mk}% mark-up.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


f3.add('C4', (2, 3, 4, 5))(f3_c4)

# ---------------------------------------------------------------- growth and decay
f4 = topic('Exponential growth and decay', 'exponential growth and decay', 'exponential growth', 'depreciation')
f4.fixed('C1', (1, 2), [
    ('Which multiplier represents an increase of 4% each year?', '1.04', '100% + 4% = 104% = 1.04.', ['0.04', '1.4', '0.96']),
    ('Which multiplier represents a decrease of 12% each year?', '0.88', '100% − 12% = 88% = 0.88.', ['0.12', '1.12', '0.78']),
    ('A car worth $20 000 loses 10% of its value each year. What is it worth after 1 year?', '$18 000', '20 000 × 0.9 = 18 000.', ['$2000', '$19 000', '$22 000']),
    ('A population P grows by 3% per year. Which expression gives the population after n years?', 'P × 1.03ⁿ', 'Multiply by 1.03 each year, n times.', ['P × 1.3ⁿ', 'P + 0.03n', 'P × 0.03ⁿ']),
    ('The value of a quantity decreasing exponentially', 'never reaches zero', 'Multiplying by a positive factor less than 1 makes the value smaller but never zero.', ['reaches zero after 10 years', 'decreases by the same amount each year', 'becomes negative']),
])
f4.fixed('C2', (2, 3), [
    ('Explain the difference between a quantity decreasing by $500 each year and one decreasing by 10% each year.', 'A fixed $500 decrease is linear (same amount each year); a 10% decrease is exponential, so the amount lost each year gets smaller as the value falls.', 'B1 linear vs exponential; B1 amount lost changes [2]'),
    ('Explain why a population growing by 5% per year does not double in 20 years.', 'Compound growth: 1.05²⁰ ≈ 2.65, so it more than doubles; 20 × 5% = 100% would only apply to simple (linear) growth.', 'B1 compound not simple; B1 1.05²⁰ ≈ 2.65 [2]'),
    ('Explain why the graph of the value of a car that depreciates by 15% per year is a curve and not a straight line.', 'The value is multiplied by 0.85 each year, so the yearly decrease gets smaller; the rate of change is not constant.', 'B1 multiplied by constant factor; B1 decreasing drops/non-constant gradient [2]'),
])


@f4.add('C1', (1, 2, 3))
def f4_mult(r, D):
    pc = r.choice([1.5, 2, 2.5, 3, 4, 6, 8, 12, 15, 18, 22, 35])
    up = r.random() < 0.5
    m = 1 + pc / 100 if up else 1 - pc / 100
    return MC(r, f'A quantity {"increases" if up else "decreases"} by {ex(pc)}% each year. Which number should it be multiplied by each year?', m,
              [pc / 100, 1 - pc / 100 if up else 1 + pc / 100, 1 + 2 * pc / 100 if up else 1 - 2 * pc / 100, 1 + pc / 1000 if up else 1 - pc / 1000, pc / 100 + 1.1], f'{"100% + " if up else "100% − "}{ex(pc)}% = {ex(m * 100)}% = {ex(m)}.', fmtf=lambda x: ex(round(x, 4)))


@f4.add('C2', (2, 3, 4), 'explain')
def f4_err(r, D):
    nm = person(r)
    pc = r.choice([5, 8, 10, 12, 15, 20])
    n = r.choice([3, 4, 5])
    V = r.choice([12000, 15000, 18000, 24000])
    right = V * (1 - pc / 100) ** n
    wrong = V * (1 - pc * n / 100)
    return Q(f'A machine worth ${V:,} depreciates by {pc}% per year. {nm} says that after {n} years it has lost {pc * n}% of its value, so it is worth ${wrong:,.2f}. Explain the mistake and find the correct value.',
             f'Each year {pc}% is taken from the reduced value, so the losses are not simply added: value = {V} × {ex(1 - pc / 100)}{sup(n)} = ${right:,.2f}.',
             f'B1 depreciation is compound; M1 {V} × {ex(1 - pc / 100)}{sup(n)}; A1 ${right:,.2f} [3]', marks=3)


@f4.add('C3', (1, 2, 3, 4, 5))
def f4_calc(r, D):
    kind = r.choice(['pop', 'car', 'bact', 'years', 'rate'])
    c = city(r)
    if kind == 'pop':
        P0 = r.choice([45000, 120000, 350000, 1200000, 2400000])
        pc = r.choice([1.2, 1.8, 2.5, 3, 3.5])
        n = r.choice([3, 5, 8, 10])
        v = P0 * (1 + pc / 100) ** n
        return Q(f'The population of {c} is {P0:,} and is growing at {ex(pc)}% per year. Estimate the population after {n} years, giving your answer to the nearest thousand.', f'{round(v, -3):,.0f}',
                 f'M1 {P0:,} × {ex(1 + pc / 100)}{sup(n)}; A1 {round(v, -3):,.0f}.')
    if kind == 'car':
        V = r.choice([14000, 18500, 22000, 26000, 32000])
        pc = r.choice([8, 10, 12, 15, 18])
        n = r.choice([2, 3, 4, 5, 6])
        v = V * (1 - pc / 100) ** n
        return Q(f'A new car costs ${V:,}. Its value depreciates by {pc}% each year. Calculate its value after {n} years.', f'${v:,.2f}', f'M1 {V} × {ex(1 - pc / 100)}{sup(n)}; A1 ${v:,.2f}.')
    if kind == 'bact':
        N0 = r.choice([200, 500, 800, 1500])
        pc = r.choice([20, 25, 30, 40, 50])
        h = r.choice([4, 5, 6, 8])
        v = N0 * (1 + pc / 100) ** h
        return Q(f'A culture of bacteria starts with {N0} cells and the number increases by {pc}% every hour. Calculate the number of cells after {h} hours, to the nearest whole number.', f'{round(v):,}',
                 f'M1 {N0} × {ex(1 + pc / 100)}{sup(h)}; A1 {round(v):,}.')
    if kind == 'years':
        V = r.choice([10000, 25000, 40000])
        pc = r.choice([10, 12, 15, 20])
        f = r.choice([0.5, 0.4, 0.3])
        n = math.ceil(math.log(f) / math.log(1 - pc / 100) - 1e-12)
        return Q(f'A machine bought for ${V:,} loses {pc}% of its value each year. Find the number of complete years after which its value first falls below ${V * f:,.0f}.', f'{n} years',
                 f'M1 {V} × {ex(1 - pc / 100)}ⁿ by trial; M1 n = {n - 1}: ${V * (1 - pc / 100) ** (n - 1):,.0f}; n = {n}: ${V * (1 - pc / 100) ** n:,.0f}; A1 {n} years.')
    P0 = r.choice([5000, 8000, 12000])
    pc = r.choice([4, 5, 6, 8])
    n = r.choice([3, 4, 5])
    v = round(P0 * (1 + pc / 100) ** n)
    rr = ((v / P0) ** (1 / n) - 1) * 100
    return Q(f'The number of visitors to a museum in {c} grew from {P0:,} to {v:,} in {n} years. The number increased by the same percentage each year. Calculate this percentage.', f'{n3(rr)}%',
             f'M1 {P0} × x{sup(n)} = {v}; M1 x = ({v}/{P0})^(1/{n}) = {ex(round(1 + rr / 100, 4))}; A1 {n3(rr)}%.')


def f4_c4(r, D):
    kind = r.choice(['town', 'phone'])
    nm = person(r)
    if kind == 'town':
        P0 = r.choice([24000, 36000, 48000, 60000])
        pc = r.choice([2, 2.5, 3, 4])
        n = r.choice([5, 8, 10])
        v = P0 * (1 + pc / 100) ** n
        dbl = math.ceil(math.log(2) / math.log(1 + pc / 100) - 1e-12)
        intro = f'The population of a town near {city(r)} was {P0:,} at the start of 2020. It is predicted to grow by {ex(pc)}% each year.'
        parts = [
            P('Calculate the predicted population at the start of 2021.', f'{P0 * (1 + pc / 100):,.0f}', f'M1 {P0} × {ex(1 + pc / 100)}; A1', 2),
            P(f'Calculate the predicted population after {n} years, to the nearest hundred.', f'{round(v, -2):,.0f}', f'M1 {P0} × {ex(1 + pc / 100)}{sup(n)}; A1', 2),
            P('Find the number of complete years until the population first exceeds double its 2020 value.', f'{dbl} years', f'M1 {ex(1 + pc / 100)}ⁿ > 2 by trial; A1 {dbl}', 3),
            P('Calculate the population at the start of 2018, assuming the same rate of growth before 2020.', f'{P0 / (1 + pc / 100) ** 2:,.0f}', f'M1 {P0} ÷ {ex(1 + pc / 100)}²; A1', 2),
            P('Give one reason why this prediction may not be accurate.', 'Growth rates change (e.g. migration, housing, economy), so the rate may not stay constant.', 'B1', 1),
        ]
    else:
        V = r.choice([800, 950, 1200, 1500])
        pc = r.choice([20, 25, 30, 35])
        n = r.choice([2, 3, 4])
        v = V * (1 - pc / 100) ** n
        intro = f'{nm} buys a laptop in {city(r)} for ${V}. Its value falls by {pc}% each year.'
        parts = [
            P(f'Calculate its value after {n} years.', f'${v:,.2f}', f'M1 {V} × {ex(1 - pc / 100)}{sup(n)}; A1', 2),
            P(f'Calculate the total percentage loss in value over {n} years.', f'{n3((1 - (1 - pc / 100) ** n) * 100)}%', f'M1 1 − {ex(1 - pc / 100)}{sup(n)}; A1', 2),
            P(f'Find the first year in which its value is less than ${V // 4}.', f'Year {math.ceil(math.log(0.25) / math.log(1 - pc / 100) - 1e-12)}', 'M1 trial; A1', 2),
            P(f'{nm} says the laptop loses ${V * pc // 100} every year. Explain why this is wrong.', f'The {pc}% is taken from the current (falling) value, so the amount lost decreases each year.', 'B1 B1', 2),
        ]
    return cmp_(r, intro, parts)


f4.add('C4', (2, 3, 4, 5))(f4_c4)
CHAPTERS[5] = [f1, f2, f3, f4]


# =========================================================== 6 Curved graphs (Ch 18)
def xp(n, v='x'):
    return '' if n == 0 else (v if n == 1 else v + sup(n))


def pl(terms, v='x'):
    """terms: list of (coef, power) -> polynomial string."""
    terms = sorted([t for t in terms if t[0] != 0], key=lambda t: -t[1])
    return expr(*[(c, xp(n, v)) for c, n in terms])


def dpl(terms):
    return [(c * n, n - 1) for c, n in terms if n > 0]


def ev(terms, x):
    return sum(c * x ** n for c, n in terms)


g1 = topic('Quadratic graphs', 'quadratic graphs', 'plotting, roots, turning point and line of symmetry', 'parabola')
g1.fixed('C1', (1, 2), [
    ('What shape is the graph of y = x² − 4x + 1?', 'A U-shaped parabola with a minimum point', 'The coefficient of x² is positive, so the parabola opens upwards.', ['An ∩-shaped parabola with a maximum point', 'A straight line', 'A hyperbola']),
    ('What is the equation of the line of symmetry of y = (x − 2)(x − 6)?', 'x = 4', 'Halfway between the roots 2 and 6.', ['y = 4', 'x = 8', 'x = −4']),
    ('Where does the graph of y = x² − 3x + 5 cross the y-axis?', '(0, 5)', 'Put x = 0: y = 5.', ['(5, 0)', '(0, −3)', '(−3, 0)']),
    ('The roots of a quadratic equation can be read from its graph where the curve', 'crosses the x-axis', 'At the roots y = 0.', ['crosses the y-axis', 'has its turning point', 'is steepest']),
    ('What are the coordinates of the turning point of y = (x − 3)² + 2?', '(3, 2)', 'Minimum when x − 3 = 0, giving y = 2.', ['(−3, 2)', '(3, −2)', '(2, 3)']),
    ('Which graph has a maximum turning point?', 'y = 5 + 2x − x²', 'Negative x² coefficient: ∩-shaped.', ['y = x² + 2x − 5', 'y = 2x + 5', 'y = x² − 5']),
])
g1.fixed('C2', (2, 3), [
    ('Explain why the graph of y = 4 − x² has a maximum point.', 'The coefficient of x² is negative, so y decreases as x moves away from 0 in either direction; the greatest value is 4 at x = 0.', 'B1 negative x² coefficient; B1 maximum (0, 4) [2]'),
    ('Explain how the line of symmetry of a quadratic graph can be found from its two roots.', 'The parabola is symmetrical, so the line of symmetry is halfway between the roots: x = (p + q)/2.', 'B1 symmetry; B1 midpoint of roots [2]'),
    ('Explain why some quadratic graphs do not cross the x-axis.', 'If the turning point is above the x-axis for a U-shaped curve (or below for ∩-shaped), y is never 0, so the equation has no real roots.', 'B1 turning point position; B1 no real roots [2]'),
    ('When completing a table of values for y = x² − 2x, a student writes y = −8 when x = −2. Explain the mistake.', '(−2)² = 4, not −4, so y = 4 − 2(−2) = 4 + 4 = 8.', 'B1 squaring a negative gives a positive; B1 y = 8 [2]'),
])


@g1.add('C1', (1, 2, 3))
def g1_tab(r, D):
    b, c = r.randint(-5, 5), r.randint(-6, 6)
    x = r.choice([-4, -3, -2, -1, 2, 3, 4])
    y = x * x + b * x + c
    return MC(r, f'For y = {quad(1, b, c)}, find the value of y when x = {num(x)}.', y, [-x * x + b * x + c, x * x - b * x + c, 2 * x + b * x + c, y + 2, y - 3, -y if y else 4, y + 6], f'({num(x)})² {"+" if b >= 0 else "−"} {abs(b)}({num(x)}) {sgn(c).strip()} = {num(x * x)} {sgn(b * x).strip()} {sgn(c).strip()} = {num(y)}.')


@g1.add('C2', (2, 3, 4), 'explain')
def g1_err(r, D):
    p, q = r.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 6], 2)
    nm = person(r)
    b, c = -(p + q), p * q
    ls = Fr(p + q, 2)
    return Q(f'{nm} says the line of symmetry of y = {quad(1, b, c)} is x = {frac(-ls)} because it is "halfway between the roots {num(-p)} and {num(-q)}". Explain the error and give the correct line of symmetry.',
             f'The roots are x = {num(p)} and x = {num(q)} (from ({lin(1, -p)})({lin(1, -q)}) = 0), not their negatives. Line of symmetry x = {frac(ls)}.',
             f'B1 roots have the opposite sign to the numbers in the brackets; B1 x = {frac(ls)} [2]')


@g1.add('C3', (1, 2, 3, 4))
def g1_tab2(r, D):
    a = 1 if D <= 2 else r.choice([1, -1, 2])
    b, c = r.randint(-4, 4), r.randint(-5, 6)
    xs = list(range(-3, 4)) if D <= 2 else list(range(-2, 5))
    ys = [a * x * x + b * x + c for x in xs]
    miss = r.sample(range(len(xs)), 3)
    shown = ', '.join(f'x = {num(x)}: y = {"?" if i in miss else num(y)}' for i, (x, y) in enumerate(zip(xs, ys)))
    ans = ', '.join(f'x = {num(xs[i])}, y = {num(ys[i])}' for i in sorted(miss))
    return Q(f'Complete the table of values for y = {quad(a, b, c)}. {shown}.', ans, 'B1 for each correct missing value [3]' if D > 1 else 'B1 B1 B1', marks=3)


@g1.add('C3', (2, 3, 4, 5))
def g1_feat(r, D):
    p, q = r.sample([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 7], 2)
    a = 1 if D <= 3 else r.choice([1, -1])
    b, c = -a * (p + q), a * p * q
    ls = Fr(p + q, 2)
    tp_y = a * (ls - p) * (ls - q)
    return Q(f'For the graph of y = {quad(a, b, c)}, find (a) the coordinates of the points where it crosses the x-axis, (b) the equation of the line of symmetry and (c) the coordinates of the turning point, stating whether it is a maximum or a minimum.',
             f'(a) ({num(min(p, q))}, 0) and ({num(max(p, q))}, 0) (b) x = {frac(ls)} (c) ({frac(ls)}, {frac(tp_y)}), {"minimum" if a > 0 else "maximum"}',
             f'(a) M1 factorise {"−" if a < 0 else ""}({lin(1, -p)})({lin(1, -q)}); A1 both (b) B1 x = {frac(ls)} (c) M1 substitute x = {frac(ls)}; A1 {frac(tp_y)} and nature.', type='multi_step', marks=5)


def g1_c4(r, D):
    p, q = sorted(r.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 2))
    b, c = -(p + q), p * q
    ls = Fr(p + q, 2)
    tpy = (ls - p) * (ls - q)
    k = r.choice([1, 2, 3, 4])
    disc = b * b - 4 * (c - k)
    x1, x2 = (-b + math.sqrt(disc)) / 2, (-b - math.sqrt(disc)) / 2
    lo, hi = p - 1, q + 1
    intro = f'The curve y = {quad(1, b, c)} is drawn for {num(lo)} ≤ x ≤ {num(hi)}.'
    parts = [
        P(f'Calculate the value of y when x = {num(lo)} and when x = {num(hi)}.', f'{num(lo * lo + b * lo + c)} and {num(hi * hi + b * hi + c)}', 'B1 B1', 2),
        P('Write down the solutions of the equation ' + quad(1, b, c) + ' = 0.', f'x = {num(p)} or x = {num(q)}', 'B1 B1', 2),
        P('Find the coordinates of the turning point.', f'({frac(ls)}, {frac(tpy)})', f'M1 x = {frac(ls)} (midpoint of roots); A1 y = {frac(tpy)}', 2),
        P(f'Solve {quad(1, b, c)} = {k}, giving your answers correct to 1 decimal place.', f'x = {x2:.1f} or x = {x1:.1f}', f'M1 {quad(1, b, c - k)} = 0; M1 formula; A1 both', 3),
        P('Write down the range of values of k for which y = k meets the curve twice.', f'k > {frac(tpy)}', 'B1 above the minimum value', 1),
    ]
    return cmp_(r, intro, parts)


g1.add('C4', (2, 3, 4, 5))(g1_c4)

# ---------------------------------------------------------------- reciprocal, cubic, exponential
g2 = topic('Reciprocal, cubic and exponential graphs', 'reciprocal, cubic and exponential graphs', 'reciprocal graphs', 'exponential graphs')
g2.fixed('C1', (1, 2), [
    ('What are the asymptotes of y = 1/x?', 'x = 0 and y = 0', 'The curve approaches both axes but never meets them.', ['x = 1 and y = 1', 'y = x and y = −x', 'There are none']),
    ('Through which point does every graph of the form y = aˣ (a > 0) pass?', '(0, 1)', 'a⁰ = 1 for every positive a.', ['(0, 0)', '(1, 0)', '(1, 1)']),
    ('In which quadrants does the graph of y = 6/x lie?', 'First and third', 'x and y have the same sign when 6/x is positive.', ['First and second', 'Second and fourth', 'Third and fourth']),
    ('Which equation gives a cubic graph?', 'y = x³ − 4x', 'Highest power 3.', ['y = 3x − 4', 'y = 3/x', 'y = 3ˣ']),
    ('What happens to y = 2ˣ as x becomes large and negative?', 'y gets closer and closer to 0 but stays positive', 'The x-axis is an asymptote.', ['y becomes very negative', 'y equals 0 when x = −1', 'y increases']),
    ('Which equation is a reciprocal graph?', 'y = −4/x', 'Form y = a/x.', ['y = −4x', 'y = x⁻⁴ + x²', 'y = 4ˣ']),
])
g2.fixed('C2', (2, 3), [
    ('Explain why the graph of y = 5/x has no point where x = 0.', 'Division by zero is undefined, so there is no value of y when x = 0; the y-axis is an asymptote.', 'B1 division by zero; B1 asymptote [2]'),
    ('Explain why the graph of y = 3ˣ never goes below the x-axis.', 'A positive number raised to any power is positive, so y is always greater than 0.', 'B1 positive base; B1 always positive [2]'),
    ('Describe the difference between the shapes of y = x³ and y = −x³.', 'y = x³ rises from bottom left to top right; y = −x³ is its reflection in the x-axis, falling from top left to bottom right. Both pass through the origin.', 'B1 each shape described; B1 reflection [2]'),
    ('Explain why exponential growth eventually overtakes any quadratic growth such as y = x².', 'An exponential is multiplied by a constant factor for each step in x, so it increases ever faster; for large x, 2ˣ is far larger than x².', 'B1 constant multiplying factor; B1 comparison for large x [2]'),
])


@g2.add('C1', (1, 2, 3))
def g2_id(r, D):
    a = r.choice([2, 3, 4, 5, -2, -3])
    kind = r.choice(['quadratic', 'cubic', 'reciprocal', 'exponential', 'linear'])
    eq = {'quadratic': f'y = {quad(a, 1, -3)}', 'cubic': f'y = {pl([(a, 3), (-2, 1)])}', 'reciprocal': f'y = {num(a)}/x', 'exponential': f'y = {abs(a)}ˣ', 'linear': f'y = {lin(a, 7)}'}[kind]
    names = {'quadratic': 'Quadratic (parabola)', 'cubic': 'Cubic', 'reciprocal': 'Reciprocal (hyperbola)', 'exponential': 'Exponential', 'linear': 'Straight line'}
    return SMC(r, f'What type of graph does the equation {eq} give?', names[kind], [v for k, v in names.items() if k != kind], f'{names[kind]}: {"highest power 2" if kind == "quadratic" else ("highest power 3" if kind == "cubic" else ("x in the denominator" if kind == "reciprocal" else ("x is the power" if kind == "exponential" else "highest power 1")))}.')


@g2.add('C2', (2, 3, 4), 'explain')
def g2_err(r, D):
    nm = person(r)
    a = r.choice([2, 3, 4, 5])
    x = r.choice([-2, -3])
    right = Fr(1, a ** (-x))
    return Q(f'{nm} completes a table for y = {a}ˣ and writes y = {num(a * x)} when x = {num(x)}. Explain the error and give the correct value.',
             f'{a}{sup(x)} means 1/{a}{sup(-x)}, not {a} × ({num(x)}). y = {frac(right)}.', f'B1 negative power means reciprocal; B1 {frac(right)} [2]')


@g2.add('C3', (1, 2, 3, 4))
def g2_vals(r, D):
    kind = r.choice(['rec', 'cub', 'exp'])
    if kind == 'rec':
        a = r.choice([4, 6, 8, 12, -6, -12])
        b = r.randint(-3, 3) if D >= 3 else 0
        xs = [x for x in [-4, -3, -2, -1, 1, 2, 3, 4] if True]
        pick = r.sample(xs, 3)
        vals = ', '.join(f'x = {num(x)}: y = {frac(Fr(a, x) + b)}' for x in pick)
        eq = f'y = {num(a)}/x' + (sgn(b) if b else '')
        stem = f'For {eq}, calculate y when x = ' + ', '.join(num(x) for x in pick) + '.' + (' Write down the equations of the asymptotes.' if D >= 3 else '')
        return Q(stem, vals + (f'; asymptotes x = 0 and y = {num(b)}' if D >= 3 else ''), ' '.join('B1' for _ in pick) + ' (one per value)' + ('; B1 B1 asymptotes' if D >= 3 else '') + '.')
    if kind == 'cub':
        a, b, c = r.choice([1, 1, -1, 2]), r.randint(-4, 4), r.randint(-5, 5)
        terms = [(a, 3), (b, 1), (c, 0)]
        pick = r.sample([-3, -2, -1, 0, 1, 2, 3], 3)
        return Q(f'For y = {pl(terms)}, calculate y when x = ' + ', '.join(num(x) for x in pick) + '.', ', '.join(f'x = {num(x)}: y = {num(ev(terms, x))}' for x in pick), ' '.join('B1' for _ in pick) + ' (one per value); watch signs when cubing negatives.')
    k, a = r.choice([1, 2, 3, 5]), r.choice([2, 3])
    pick = r.sample([-2, -1, 0, 1, 2, 3, 4], 3)
    target = k * a ** r.randint(2, 5)
    xs = round(math.log(target / k, a))
    return Q(f'For y = {"" if k == 1 else str(k) + " × "}{a}ˣ, (a) calculate y when x = ' + ', '.join(num(x) for x in pick) + f' (b) find the value of x when y = {target}.',
             '(a) ' + ', '.join(f'x = {num(x)}: y = {frac(k * Fr(a) ** x)}' for x in pick) + f' (b) x = {xs}', f'(a) ' + ' '.join('B1' for _ in pick) + f' (b) M1 {a}ˣ = {target // k}; A1 x = {xs}.', type='multi_step', marks=len(pick) + 2)


@g2.add('C3', (3, 4, 5))
def g2_model(r, D):
    p = r.choice([2, 3, 4, 5, 10])
    q = r.choice([2, 3, 1.5, 0.5])
    x2 = r.choice([2, 3])
    y2 = p * q ** x2
    return Q(f'The curve y = p × qˣ passes through the points (0, {num(p)}) and ({x2}, {ex(y2)}). Find the values of p and q.', f'p = {num(p)}, q = {ex(q)}',
             f'B1 p = {num(p)} from x = 0; M1 q{sup(x2)} = {ex(y2)} ÷ {num(p)} = {ex(q ** x2)}; A1 q = {ex(q)}.')


def g2_c4(r, D):
    nm = person(r)
    N0 = r.choice([50, 80, 100, 200])
    f = r.choice([2, 3, 1.5])
    h = r.choice([3, 4, 5])
    tgt = N0 * f ** r.choice([5, 6, 7])
    tn = round(math.log(tgt / N0, f))
    intro = f'{nm} models the number of cells N in an experiment in {city(r)} by N = {N0} × {ex(f)}ᵗ, where t is the time in hours.'
    parts = [
        P('Write down the number of cells at the start.', f'{N0}', 'B1', 1),
        P(f'Calculate N when t = {h}.', f'{ex(N0 * f ** h)}', f'M1 {N0} × {ex(f)}{sup(h)}; A1', 2),
        P(f'Find the time when N = {ex(tgt)}.', f't = {tn} hours', f'M1 {ex(f)}ᵗ = {ex(tgt / N0)}; A1 {tn}', 2),
        P('Describe the shape of the graph of N against t.', 'An exponential growth curve: increasing ever more steeply, crossing the N-axis at ' + str(N0) + '.', 'B1 increasing curve; B1 intercept/steepening', 2),
        P('Explain why the model cannot be used for very large values of t.', 'The number would grow without limit, but in reality space/nutrients run out.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


g2.add('C4', (2, 3, 4, 5))(g2_c4)

# ---------------------------------------------------------------- solving graphically
g3 = topic('Solving equations graphically', 'solving equations graphically', 'finding intersections', 'graphical solution')
g3.fixed('C1', (1, 2), [
    ('The graph of y = f(x) is drawn. The solutions of f(x) = 0 are found where', 'the graph crosses the x-axis', 'At these points y = 0.', ['the graph crosses the y-axis', 'the graph has a turning point', 'x = 0']),
    ('The graphs of y = x² and y = x + 2 are drawn. Which equation is solved by their points of intersection?', 'x² = x + 2', 'At an intersection both y-values are equal.', ['x² + x + 2 = 0', 'x² = 0', 'x + 2 = 0']),
    ('The graph of y = x² − 4 is drawn. Which line should be drawn to solve x² − 4 = 3?', 'y = 3', 'Read where y = 3 meets the curve.', ['y = −3', 'x = 3', 'y = 7']),
    ('How many solutions does x² = 5 have, according to the graph of y = x²?', 'Two', 'The line y = 5 crosses the parabola twice.', ['One', 'None', 'Three']),
])
g3.fixed('C2', (2, 3), [
    ('Explain why solutions read from a graph are usually only approximate.', 'They depend on reading the scale accurately and on how accurately the curve has been drawn.', 'B1 reading scale; B1 accuracy of drawing [2]'),
    ('Explain how the graph of y = x² − 3x can be used to solve x² − 3x − 4 = 0.', 'Rearrange to x² − 3x = 4, draw y = 4 and read the x-coordinates of the intersections (x = −1 and x = 4).', 'B1 rearrange; B1 draw y = 4 and read x-values [2]'),
    ('Explain how you can tell from a graph that an equation has no real solutions.', 'The curve and the line (or x-axis) do not meet, so there is no x-value that satisfies both.', 'B1 no intersection; B1 meaning [2]'),
])


@g3.add('C2', (2, 3, 4), 'explain')
def g3_line(r, D):
    b, c = r.randint(-4, 4), r.randint(-5, 5)
    b2, c2 = r.randint(-5, 5), r.randint(-6, 6)
    if (b2, c2) == (b, c):
        b2 += 1
    m, k = b - b2, c - c2
    return Q(f'The graph of y = {quad(1, b, c)} has been drawn. Find the equation of the straight line that should be drawn on the same grid to solve {quad(1, b2, c2)} = 0, and explain your method.',
             f'y = {lin(m, k)}. Rearranging: {quad(1, b, c)} = {lin(m, k)} is the same as {quad(1, b2, c2)} = 0, so the x-coordinates of the intersections are the solutions.',
             f'M1 subtract the equation from y = {quad(1, b, c)}: y = {quad(1, b, c)} − ({quad(1, b2, c2)}); A1 y = {lin(m, k)} [2]')


@g3.add('C1', (1, 2, 3))
def g3_line_mcq(r, D):
    b, c = r.randint(-4, 4), r.randint(-4, 5)
    k = r.choice([-3, -2, 2, 3, 4, 5])
    c2 = c - k
    return SMC(r, f'The graph of y = {quad(1, b, c)} is drawn. Which line should be drawn to solve {quad(1, b, c2)} = 0?', f'y = {num(k)}',
               [f'y = {num(-k)}', f'x = {num(k)}', f'y = {num(c2)}', f'y = {num(c + k)}', f'y = {num(k + 1)}', f'y = {num(c)}', f'x = {num(-k)}'], f'{quad(1, b, c2)} = 0 ⇔ {quad(1, b, c)} = {num(k)}.')


@g3.add('C3', (2, 3, 4, 5))
def g3_inter(r, D):
    x1, x2 = r.sample([-4, -3, -2, -1, 0, 1, 2, 3, 4, 5], 2)
    m, k = r.randint(-3, 3), r.randint(-4, 6)
    # x² + bx + c - (mx + k) = (x - x1)(x - x2)
    b = m - (x1 + x2)
    c = k + x1 * x2
    pts = sorted([(x1, m * x1 + k), (x2, m * x2 + k)])
    return Q(f'Find the coordinates of the points where the line y = {lin(m, k)} meets the curve y = {quad(1, b, c)}.',
             ' and '.join(f'({num(x)}, {num(y)})' for x, y in pts), f'M1 {quad(1, b, c)} = {lin(m, k)}; M1 {quad(1, b - m, c - k)} = 0; M1 factorise; A1 x-values; A1 y-values.')


@g3.add('C3', (3, 4, 5))
def g3_trial(r, D):
    a = r.choice([1, 2])
    b = r.randint(1, 5)
    k = r.choice([12, 20, 30, 45, 60])
    f = lambda x: a * x ** 3 + b * x
    lo = 0
    while f(lo + 1) < k:
        lo += 1
    x = lo
    for _ in range(10):
        if f(x + 0.1) < k:
            x = round(x + 0.1, 1)
        else:
            break
    ans = x if abs(f(x + 0.05) - k) > 0 and f(x + 0.05) > k else round(x + 0.1, 1)
    return Q(f'The equation {pl([(a, 3), (b, 1)])} = {k} has a solution between {lo} and {lo + 1}. Use trial and improvement (or the graph of y = {pl([(a, 3), (b, 1)])}) to find this solution correct to 1 decimal place.', f'x = {ans:.1f}',
             f'M1 trials e.g. x = {x:.1f} gives {ex(round(f(x), 3))}, x = {x + 0.1:.1f} gives {ex(round(f(x + 0.1), 3))}; M1 tests x = {x + 0.05:.2f} gives {ex(round(f(x + 0.05), 3))}; A1 {ans:.1f}.')


def g3_c4(r, D):
    p, q = sorted(r.sample([-3, -2, -1, 1, 2, 3, 4], 2))
    b, c = -(p + q), p * q
    m = r.choice([1, 2, -1])
    x1 = r.choice([x for x in range(-3, 6) if x not in (p, q)])
    # choose line through (x1, y1) and second intersection
    disc_ok = None
    for k in range(-8, 9):
        B, C = b - m, c - k
        d = B * B - 4 * C
        if d > 0 and math.isqrt(d) ** 2 == d and (-B + math.isqrt(d)) % 2 == 0:
            disc_ok = (k, (-B + math.isqrt(d)) // 2, (-B - math.isqrt(d)) // 2)
            break
    if not disc_ok:
        return None
    k, xa, xb = disc_ok
    tpy = Fr(-(p - q) ** 2, 4)
    intro = f'The curve y = {quad(1, b, c)} and the line y = {lin(m, k)} are drawn on the same grid.'
    parts = [
        P(f'Use the curve to write down the solutions of {quad(1, b, c)} = 0.', f'x = {num(p)} or x = {num(q)}', 'B1 B1', 2),
        P(f'Show that the x-coordinates of the points of intersection satisfy {quad(1, b - m, c - k)} = 0.', 'Equate the two expressions and rearrange.', 'M1 equate; A1 rearrange', 2),
        P('Find the coordinates of the points of intersection.', f'({num(xb)}, {num(m * xb + k)}) and ({num(xa)}, {num(m * xa + k)})', 'M1 solve; A1 A1', 3),
        P(f'Write down the value of k for which {quad(1, b, c)} = k has exactly one solution.', f'k = {frac(tpy)}', 'B1 minimum value of the curve', 1),
        P(f'Find the equation of the line that should be drawn to solve {quad(1, b + 2, c - 1)} = 0 using the curve.', f'y = {lin(-2, 1)}', 'M1 subtract; A1', 2),
    ]
    return cmp_(r, intro, parts)


g3.add('C4', (2, 3, 4, 5))(g3_c4)

# ---------------------------------------------------------------- gradient and differentiation
g4 = topic('Gradient of a curve and differentiation', 'gradient of a curve', 'tangents and differentiation of ax^n', 'differentiation')
g4.fixed('C1', (1, 2), [
    ('If y = xⁿ, what is dy/dx?', 'nxⁿ⁻¹', 'Multiply by the power, then reduce the power by 1.', ['xⁿ⁻¹', 'nxⁿ', '(n − 1)xⁿ']),
    ('What is the derivative of a constant, such as y = 7?', '0', 'A horizontal line has gradient 0.', ['7', '1', '7x']),
    ('If y = 5x, what is dy/dx?', '5', 'The gradient of a straight line y = 5x is 5.', ['5x', '0', 'x']),
    ('The gradient of a curve at a point is equal to', 'the gradient of the tangent at that point', 'The tangent touches the curve with the same gradient.', ['the gradient of the chord to the origin', 'the y-coordinate of the point', 'the area under the curve']),
    ('If y = 4x³, what is dy/dx?', '12x²', '3 × 4 = 12, power 3 − 1 = 2.', ['12x³', '4x²', '7x²']),
])
g4.fixed('C2', (2, 3), [
    ('Explain why the gradient of a curve, unlike a straight line, is different at different points.', 'A curve changes direction, so how steep it is changes from point to point; the gradient must be found at a particular point using a tangent or the derivative.', 'B1 steepness changes; B1 tangent/derivative at a point [2]'),
    ('Describe how to estimate the gradient of a curve at a point from a graph.', 'Draw a tangent to the curve at the point, choose two points on the tangent far apart, and calculate change in y ÷ change in x.', 'B1 draw tangent; B1 rise over run [2]'),
    ('Explain what a negative value of dy/dx tells you about a curve at a point.', 'The curve is decreasing there: as x increases, y decreases.', 'B1 decreasing; B1 interpretation [2]'),
])


@g4.add('C1', (1, 2, 3))
def g4_d(r, D):
    a, n = r.choice([2, 3, 4, 5, 6, -2, -3, 7]), r.choice([2, 3, 4, 5])
    c = pl([(a * n, n - 1)])
    return SMC(r, f'Find dy/dx when y = {pl([(a, n)])}.', c, [pl([(a * n, n)]), pl([(a, n - 1)]), pl([(a * (n - 1), n - 1)]), pl([(a + n, n - 1)]), pl([(a * n, n + 1)])],
               f'dy/dx = {num(n)} × {num(a)}x{sup(n - 1)} = {c}.')


@g4.add('C2', (2, 3, 4), 'explain')
def g4_err(r, D):
    a, b, c = r.randint(2, 6), r.randint(-6, 6), r.randint(-9, 9)
    nm = person(r)
    terms = [(a, 3), (b, 1), (c, 0)]
    right = pl(dpl(terms))
    wrong = pl([(3 * a, 2), (b, 0), (c, 0)]) if c else pl([(3 * a, 3), (b, 0)])
    return Q(f'{nm} differentiates y = {pl(terms)} and writes dy/dx = {wrong}. Explain the error and give the correct derivative.',
             f'{"The derivative of the constant " + num(c) + " is 0" if c else "The power must be reduced by 1"}. Correct: dy/dx = {right}.',
             f'B1 identifies error; B1 dy/dx = {right} [2]')


@g4.add('C3', (1, 2, 3, 4, 5))
def g4_grad(r, D):
    n = 2 if D <= 2 else 3
    a = r.choice([1, 2, 3, -1, -2]) if n == 3 else r.choice([1, 2, 3, -1])
    terms = [(a, n), (r.randint(-6, 6), 2 if n == 3 else 1), (r.randint(-8, 8), 1 if n == 3 else 0)]
    if n == 3:
        terms.append((r.randint(-5, 5), 0))
    x = r.randint(-3, 4)
    d = dpl(terms)
    g = ev(d, x)
    if D == 1:
        return MC(r, f'For y = {pl(terms)}, what is the gradient of the curve at x = {num(x)}?', g, [ev(terms, x), g + 2, ev(dpl(terms), -x), g * 2 if g else 3, g - 3, -g if g else 5, g + 5], f'dy/dx = {pl(d)}; at x = {num(x)}: {num(g)}.')
    if D >= 4:
        y = ev(terms, x)
        cc = y - g * x
        return Q(f'Find the equation of the tangent to the curve y = {pl(terms)} at the point where x = {num(x)}.', f'y = {lin(g, cc)}',
                 f'B1 dy/dx = {pl(d)}; M1 gradient {num(g)}; B1 point ({num(x)}, {num(y)}); M1 y{sgn(-y)} = {num(g)}{bracket(-x)}; A1 y = {lin(g, cc)}.')
    return Q(f'Find the gradient of the curve y = {pl(terms)} at the point where x = {num(x)}.', num(g), f'B1 B1 dy/dx = {pl(d)}; M1 substitute x = {num(x)}; A1 {num(g)}.')


@g4.add('C3', (2, 3, 4, 5))
def g4_find(r, D):
    a = r.choice([1, 2, 3])
    b = r.randint(-8, 8)
    c = r.randint(-5, 5)
    x0 = r.randint(-4, 5)
    g = 2 * a * x0 + b
    terms = [(a, 2), (b, 1), (c, 0)]
    y0 = ev(terms, x0)
    return Q(f'Find the coordinates of the point on the curve y = {pl(terms)} where the gradient is {num(g)}.', f'({num(x0)}, {num(y0)})',
             f'B1 dy/dx = {pl(dpl(terms))}; M1 {pl(dpl(terms))} = {num(g)}; A1 x = {num(x0)}; A1 y = {num(y0)}.')


def g4_c4(r, D):
    a = r.choice([1, -1, 2])
    b, c, d0 = r.randint(-6, 6), r.randint(-9, 9), r.randint(-6, 6)
    terms = [(a, 3), (b, 2), (c, 1), (d0, 0)]
    x1 = r.randint(-2, 3)
    dd = dpl(terms)
    g = ev(dd, x1)
    y1 = ev(terms, x1)
    cc = y1 - g * x1
    intro = f'A curve has equation y = {pl(terms)}. The point P on the curve has x-coordinate {num(x1)}.'
    parts = [
        P('Find dy/dx.', pl(dd), 'B1 B1 B1 (one per term)', 3),
        P('Find the y-coordinate of P.', num(y1), 'B1', 1),
        P('Find the gradient of the curve at P.', num(g), 'M1 substitute; A1', 2),
        P('Find the equation of the tangent at P.', f'y = {lin(g, cc)}', 'M1 y − y₁ = m(x − x₁); A1', 2),
        P('Find the coordinates of the point where the tangent at P crosses the y-axis.', f'(0, {num(cc)})', 'M1 x = 0 in tangent equation; A1', 2),
        P(f'Find dy/dx when x = {num(x1 + 1)} and state whether the curve is increasing or decreasing there.', f'{num(ev(dd, x1 + 1))}; ' + ('increasing' if ev(dd, x1 + 1) > 0 else ('decreasing' if ev(dd, x1 + 1) < 0 else 'stationary')), 'M1 A1', 2),
    ]
    return cmp_(r, intro, parts)


g4.add('C4', (2, 3, 4, 5))(g4_c4)

# ---------------------------------------------------------------- stationary points
g5 = topic('Stationary points and their nature', 'stationary points', 'their nature using the derivative', 'turning points maxima minima')
g5.fixed('C1', (1, 2), [
    ('At a stationary point on a curve, dy/dx is', 'zero', 'The tangent is horizontal.', ['undefined', 'one', 'negative']),
    ('If d²y/dx² > 0 at a stationary point, the point is', 'a minimum', 'Gradient increasing through zero: minimum.', ['a maximum', 'a point of inflection only', 'not stationary']),
    ('If d²y/dx² < 0 at a stationary point, the point is', 'a maximum', 'Gradient decreasing through zero: maximum.', ['a minimum', 'the origin', 'a root']),
    ('How many stationary points can a cubic curve y = ax³ + bx² + cx + d have at most?', 'Two', 'dy/dx is a quadratic, with at most two roots.', ['One', 'Three', 'Four']),
    ('Find the x-coordinate of the stationary point of y = x² − 8x + 3.', 'x = 4', 'dy/dx = 2x − 8 = 0.', ['x = 8', 'x = −4', 'x = 3']),
])
g5.fixed('C2', (2, 3), [
    ('Explain how the sign of dy/dx either side of a stationary point shows whether it is a maximum or a minimum.', 'For a maximum the gradient changes from positive to negative; for a minimum it changes from negative to positive.', 'B1 maximum + to −; B1 minimum − to + [2]'),
    ('Explain why a stationary point is not always a maximum or minimum.', 'The gradient can be zero without changing sign (e.g. y = x³ at the origin), giving a stationary point of inflection.', 'B1 gradient zero but no change of sign; B1 example [2]'),
    ('Explain how differentiation can be used to find the maximum volume of a box.', 'Write the volume as a function of one variable, differentiate, set dV/dx = 0 to find stationary points, and check which gives a maximum (e.g. second derivative negative).', 'B1 dV/dx = 0; B1 check nature [2]'),
])


def _cubic(r, D):
    for _ in range(200):
        p, q = r.sample(range(-4, 5), 2)
        if (p + q) % 2:
            continue
        a = r.choice([1, -1]) if D >= 4 else 1
        # dy/dx = 3a(x - p)(x - q) = 3a x² - 3a(p+q) x + 3a pq
        B = Fr(-3 * a * (p + q), 2)
        C = 3 * a * p * q
        d0 = r.randint(-6, 6)
        terms = [(a, 3), (int(B), 2), (C, 1), (d0, 0)]
        return terms, sorted([p, q]), a
    return None


@g5.add('C1', (1, 2, 3))
def g5_q(r, D):
    a, b, c = r.choice([1, 2, 3, -1, -2]), r.choice([-12, -8, -6, -4, 4, 6, 8, 12]), r.randint(-5, 5)
    x0 = Fr(-b, 2 * a)
    return SMC(r, f'Find the x-coordinate of the stationary point of y = {quad(a, b, c)}.', f'x = {frac(x0)}', [f'x = {frac(-x0)}', f'x = {frac(Fr(-b, a))}', f'x = {frac(Fr(b, 2))}', f'x = {frac(x0 + 1)}', f'x = {num(c)}'],
               f'dy/dx = {lin(2 * a, b)} = 0 gives x = {frac(x0)}.')


@g5.add('C2', (2, 3, 4), 'explain')
def g5_err(r, D):
    a = r.choice([1, 2, 3])
    x0 = r.randint(-3, 4)
    b = -2 * a * x0
    c = r.randint(-6, 6)
    nm = person(r)
    return Q(f'{nm} finds the stationary point of y = {quad(a, b, c)} at x = {num(x0)}. Since d²y/dx² = {2 * a}, which is positive, {nm} says it is a maximum. Explain whether {nm} is correct.',
             f'Not correct: a positive second derivative means the gradient is increasing, so the point is a minimum (the parabola is U-shaped).', 'B1 positive second derivative ⇒ minimum; B1 reason [2]')


@g5.add('C3', (2, 3, 4, 5))
def g5_find(r, D):
    if D <= 2:
        a, x0 = r.choice([1, 2, -1, 3]), r.randint(-4, 4)
        b = -2 * a * x0
        c = r.randint(-7, 7)
        y0 = a * x0 * x0 + b * x0 + c
        return Q(f'Find the coordinates of the stationary point on y = {quad(a, b, c)} and state whether it is a maximum or a minimum.', f'({num(x0)}, {num(y0)}), {"minimum" if a > 0 else "maximum"}',
                 f'M1 dy/dx = {lin(2 * a, b)} = 0; A1 x = {num(x0)}; A1 y = {num(y0)}; B1 nature ({"a > 0" if a > 0 else "a < 0"}).')
    cub = _cubic(r, D)
    if not cub:
        return None
    terms, (p, q), a = cub
    d2 = dpl(dpl(terms))
    pts = [(x, ev(terms, x), 'minimum' if ev(d2, x) > 0 else 'maximum') for x in (p, q)]
    return Q(f'Find the coordinates of the stationary points on the curve y = {pl(terms)} and determine their nature.', '; '.join(f'({num(x)}, {num(y)}) {n}' for x, y, n in pts),
             f'B1 dy/dx = {pl(dpl(terms))}; M1 = 0, factorise {"3" if a == 1 else "−3"}(x − {p})(x − {q}) → x = {num(p)}, {num(q)}; A1 y-values; M1 d²y/dx² = {pl(d2)}; A1 natures.'.replace('(x − -', '(x + ').replace('− −', '+ '))


def g5_c4(r, D):
    if r.random() < 0.5:
        a = r.choice([12, 18, 24, 30, 36])
        x = Fr(a, 6)
        V = x * (a - 2 * x) ** 2
        nm = person(r)
        intro = f'{nm} makes an open box from a square sheet of card of side {a} cm by cutting a square of side x cm from each corner and folding up the sides.'
        parts = [
            P(f'Show that the volume V cm³ is given by V = {pl([(4, 3), (-4 * a, 2), (a * a, 1)])}.', f'V = x({a} − 2x)²', f'M1 base side {a} − 2x; A1 expansion', 2),
            P('Find dV/dx.', pl([(12, 2), (-8 * a, 1), (a * a, 0)]), 'B1 B1', 2),
            P('Find the value of x that gives the maximum volume.', f'x = {frac(x)}', f'M1 dV/dx = 0; M1 solve (6x − {a})(2x − {a}) = 0; A1 x = {frac(x)} (x = {a // 2} gives zero volume)', 3),
            P('Calculate the maximum volume.', f'{frac(V)} cm³', 'M1 substitute; A1', 2),
            P('Use the second derivative to show that this value gives a maximum.', f'd²V/dx² = 24x − {8 * a}; at x = {frac(x)} it is {num(24 * x - 8 * a)} < 0', 'M1 A1', 2),
        ]
        return cmp_(r, intro, parts)
    cub = _cubic(r, D)
    if not cub:
        return None
    terms, (p, q), a = cub
    d = dpl(terms)
    d2 = dpl(d)
    yp, yq = ev(terms, p), ev(terms, q)
    lo, hi = sorted([yp, yq])
    intro = f'A curve has equation y = {pl(terms)}.'
    parts = [
        P('Find dy/dx.', pl(d), 'B1 B1', 2),
        P('Find the coordinates of the two stationary points.', f'({num(p)}, {num(yp)}) and ({num(q)}, {num(yq)})', 'M1 dy/dx = 0; M1 solve; A1 A1', 4),
        P('Find d²y/dx² and use it to determine the nature of each stationary point.', f'd²y/dx² = {pl(d2)}; x = {num(p)}: {"minimum" if ev(d2, p) > 0 else "maximum"}; x = {num(q)}: {"minimum" if ev(d2, q) > 0 else "maximum"}', 'B1; M1 substitute; A1', 3),
        P('Write down the range of values of k for which the equation ' + pl(terms) + ' = k has three solutions.', f'{num(lo)} < k < {num(hi)}', 'B1 B1', 2),
    ]
    return cmp_(r, intro, parts)


g5.add('C4', (2, 3, 4, 5))(g5_c4)
CHAPTERS[6] = [g1, g2, g3, g4, g5]


# =========================================================== 7 Symmetry (Ch 19)
SH2 = [('square', 4, 4), ('rectangle (not a square)', 2, 2), ('rhombus (not a square)', 2, 2), ('parallelogram (not a rectangle or rhombus)', 0, 2), ('kite', 1, 1),
       ('isosceles trapezium', 1, 1), ('equilateral triangle', 3, 3), ('isosceles triangle', 1, 1), ('scalene triangle', 0, 1), ('regular pentagon', 5, 5),
       ('regular hexagon', 6, 6), ('regular octagon', 8, 8), ('regular decagon', 10, 10), ('capital letter H', 2, 2), ('capital letter N', 0, 2), ('capital letter S', 0, 2),
       ('capital letter A', 1, 1), ('capital letter X', 2, 2), ('capital letter Z', 0, 2), ('capital letter E', 1, 1)]
POLY = {3: 'equilateral triangle', 4: 'square', 5: 'regular pentagon', 6: 'regular hexagon', 8: 'regular octagon', 9: 'regular nonagon', 10: 'regular decagon', 12: 'regular dodecagon', 15: 'regular 15-sided polygon', 18: 'regular 18-sided polygon', 20: 'regular 20-sided polygon'}

y1 = topic('Line and rotational symmetry of 2D shapes', 'line and rotational symmetry', 'symmetry of 2d shapes', 'line symmetry')
y1.fixed('C1', (1, 2), [
    ('The order of rotational symmetry of a shape is', 'the number of times it fits onto itself in one full turn', 'Count the positions in 360° where the shape looks the same.', ['the number of lines of symmetry', 'the number of sides', 'the angle of rotation']),
    ('A shape with rotational symmetry of order 1', 'has no rotational symmetry', 'Every shape fits onto itself once in a full turn (the starting position).', ['has one line of symmetry', 'is a circle', 'has rotational symmetry of 360°']),
    ('How many lines of symmetry does a rectangle (not a square) have?', '2', 'The two lines through the midpoints of opposite sides; diagonals are not lines of symmetry.', ['4', '1', '0']),
    ('What is the order of rotational symmetry of a parallelogram?', '2', 'It fits onto itself after a half turn.', ['0', '1', '4']),
    ('How many lines of symmetry does a regular hexagon have?', '6', 'A regular n-sided polygon has n lines of symmetry.', ['3', '12', '4']),
    ('What is the smallest angle of rotation that maps a regular pentagon onto itself?', '72°', '360° ÷ 5 = 72°.', ['108°', '60°', '36°']),
])
y1.fixed('C2', (2, 3), [
    ('Explain why a diagonal of a rectangle (not a square) is not a line of symmetry.', 'Reflecting in a diagonal would swap the long and short sides, so the image would not fit exactly onto the rectangle.', 'B1 reflection swaps sides; B1 sides unequal [2]'),
    ('Explain why a parallelogram has rotational symmetry but no line symmetry.', 'A half turn about the centre maps it onto itself, but folding along any line does not match the slanting sides exactly.', 'B1 half turn; B1 no fold line matches [2]'),
    ('Explain why every regular polygon with n sides has n lines of symmetry and rotational symmetry of order n.', 'All sides and angles are equal, so there is a line through each vertex or side-midpoint and the centre, and rotating by 360°/n maps it onto itself n times.', 'B1 lines through centre; B1 rotation by 360°/n [2]'),
    ('Describe the difference between line symmetry and rotational symmetry.', 'Line symmetry: the shape folds onto itself along a mirror line. Rotational symmetry: the shape fits onto itself when turned about a centre point less than a full turn.', 'B1 line description; B1 rotation description [2]'),
])


@y1.add('C1', (1, 2, 3))
def y1_q(r, D):
    nm, L, O = r.choice(SH2)
    if r.random() < 0.5:
        return MC(r, f'How many lines of symmetry does {art(nm)} have?', L, [O + 1, L + 1, L * 2 if L else 2, max(0, L - 1) if L != 1 else 3, 4 if L != 4 else 3], f'{art(nm).capitalize()} has {L} line{"s" if L != 1 else ""} of symmetry and rotational symmetry of order {O}.')
    return MC(r, f'What is the order of rotational symmetry of {art(nm)}?', O, [0, O + 1, O * 2, L + 2 if L + 2 != O else 3, 3 if O != 3 else 5], f'{art(nm).capitalize()} fits onto itself {O} time{"s" if O != 1 else ""} in a full turn.')


@y1.add('C2', (2, 3, 4), 'explain')
def y1_cmp(r, D):
    (a, la, oa), (b, lb, ob) = r.sample(SH2, 2)
    nm = person(r)
    claim_true = la == lb and oa == ob
    return Q(f'{nm} says {art(a)} and {art(b)} have exactly the same symmetry. Explain whether {nm} is correct, stating the number of lines of symmetry and the order of rotational symmetry of each.',
             f'{"Correct" if claim_true else "Not correct"}: {a}: {la} line{"s" if la != 1 else ""}, order {oa}; {b}: {lb} line{"s" if lb != 1 else ""}, order {ob}.',
             'B1 each shape correct; B1 conclusion [3]', marks=3)


@y1.add('C3', (1, 2, 3, 4))
def y1_poly(r, D):
    n = r.choice(list(POLY))
    ang = Fr(360, n)
    intang = 180 - ang
    if D == 1:
        return MC(r, f'What is the smallest angle through which a {POLY[n]} can be rotated to fit onto itself?', ang, [intang, 180 / n, 360 - ang, 2 * ang, ang / 2, 180 + ang], f'360° ÷ {n} = {frac(ang)}°.', fmtf=lambda v: f'{frac(Fr(v).limit_denominator(100))}°')
    if D == 2:
        return Q(f'A {POLY[n]} is rotated about its centre. Write down its order of rotational symmetry and calculate the smallest angle of rotation that maps it onto itself.', f'Order {n}; {frac(ang)}°', f'B1 order {n}; B1 360° ÷ {n} = {frac(ang)}°.')
    return Q(f'The smallest angle of rotation that maps a regular polygon onto itself is {frac(ang)}°. Find the number of sides, the number of lines of symmetry and the size of one interior angle.',
             f'{n} sides; {n} lines of symmetry; interior angle {frac(intang)}°', f'M1 360 ÷ {frac(ang)} = {n}; A1 {n} sides and lines; M1 180 − {frac(ang)}; A1 {frac(intang)}°.')


@y1.add('C3', (2, 3, 4, 5))
def y1_coord(r, D):
    k = r.randint(-2, 4)
    pts = [(k - r.randint(1, 4), r.randint(-3, 5)) for _ in range(2)]
    if pts[0] == pts[1]:
        pts[1] = (pts[1][0] - 1, pts[1][1] + 2)
    line = r.choice(['x', 'y']) if D >= 3 else 'x'
    if line == 'x':
        img = [(2 * k - x, y) for x, y in pts]
    else:
        img = [(x, 2 * k - y) for x, y in pts]
    f = lambda p: f'({num(p[0])}, {num(p[1])})'
    return Q(f'A shape has the line {line} = {num(k)} as a line of symmetry. Two of its vertices are {f(pts[0])} and {f(pts[1])}. Write down the coordinates of the two vertices that are their images in this line.',
             f'{f(img[0])} and {f(img[1])}', f'B1 B1 (each point is the same distance from {line} = {num(k)} on the other side).')


def y1_c4(r, D):
    n = r.choice([5, 6, 8, 10, 12])
    s = r.choice([4, 5, 6, 8])
    ext = Fr(360, n)
    intang = 180 - ext
    apo = s / (2 * math.tan(math.pi / n))
    area = n * s * apo / 2
    intro = f'A logo for a company in {city(r)} is {art(POLY[n])} of side {s} cm.'
    parts = [
        P('Write down the number of lines of symmetry.', f'{n}', 'B1', 1),
        P('Write down the order of rotational symmetry.', f'{n}', 'B1', 1),
        P('Calculate the size of one exterior angle and one interior angle.', f'{frac(ext)}° and {frac(intang)}°', f'M1 360 ÷ {n}; A1 both', 2),
        P('Calculate the distance from the centre to the midpoint of one side.', f'{n3(apo)} cm', f'M1 tan({frac(Fr(180, n))}°) = {ex(s / 2)} ÷ d; A1 {n3(apo)} cm', 2),
        P('Calculate the area of the logo.', f'{n3(area)} cm²', f'M1 {n} triangles × ½ × {s} × {n3(apo)}; A1 {n3(area)} cm²', 2),
        P('The logo is rotated clockwise about its centre through 150°. Explain whether it looks the same as before.', ('Yes' if (Fr(150) / ext).denominator == 1 else 'No') + f': it maps onto itself only for multiples of {frac(ext)}°.', 'B1 conclusion; B1 reason', 2),
    ]
    return cmp_(r, intro, parts)


y1.add('C4', (2, 3, 4, 5))(y1_c4)

# ---------------------------------------------------------------- 3D symmetry
SOL = [('cube', 9, 'order 4 about an axis through the centres of opposite faces'), ('cuboid with three different edge lengths', 3, 'order 2 about each of three axes'),
       ('cuboid with a square base and height different from the base side', 5, 'order 4 about the vertical axis'),
       ('square-based right pyramid', 4, 'order 4 about the vertical axis'), ('cylinder', 'infinitely many', 'infinite order about its central axis'),
       ('cone', 'infinitely many', 'infinite order about its axis'), ('sphere', 'infinitely many', 'infinite order about any diameter'),
       ('right prism with an equilateral triangle cross-section', 4, 'order 3 about the axis through the centres of the triangular faces'),
       ('regular tetrahedron', 6, 'order 3 about an axis through a vertex and the centre of the opposite face'),
       ('right prism with a regular hexagon cross-section', 7, 'order 6 about the axis through the centres of the hexagonal faces')]

y2 = topic('Symmetry in 3D', 'symmetry in 3d', 'planes and axes of symmetry', 'planes of symmetry')
y2.fixed('C1', (1, 2), [
    ('A plane of symmetry divides a 3D shape into', 'two halves that are mirror images of each other', 'The plane acts like a mirror.', ['two congruent shapes of any orientation', 'three equal parts', 'two shapes of different volume']),
    ('How many planes of symmetry does a cube have?', '9', '3 parallel to pairs of faces and 6 through pairs of opposite edges.', ['6', '3', '12']),
    ('How many planes of symmetry does a cuboid with three different edge lengths have?', '3', 'Each plane is parallel to a pair of faces through the centre.', ['6', '9', '4']),
    ('How many planes of symmetry does a cylinder have?', 'Infinitely many', 'Any plane containing the axis, plus the plane through the middle perpendicular to the axis.', ['1', '2', '3']),
    ('A square-based right pyramid has an axis of rotational symmetry of order', '4', 'Rotating about the vertical axis through the apex, it fits onto itself 4 times.', ['1', '2', '5']),
])
y2.fixed('C2', (2, 3), [
    ('Explain why a cube has more planes of symmetry than a cuboid with three different edge lengths.', 'All faces of a cube are equal squares, so as well as the 3 planes parallel to faces there are 6 diagonal planes through opposite edges; in the cuboid the diagonal planes do not give mirror images.', 'B1 3 face-parallel planes in both; B1 6 extra diagonal planes for cube [2]'),
    ('Explain the difference between a plane of symmetry and an axis of rotational symmetry.', 'A plane of symmetry reflects the solid onto itself; an axis of symmetry is a line about which the solid can be rotated (less than a full turn) to fit onto itself.', 'B1 plane = reflection; B1 axis = rotation [2]'),
    ('Explain why a cone has infinitely many planes of symmetry but no plane of symmetry perpendicular to its axis.', 'Any plane containing the axis cuts it into mirror halves; a perpendicular plane would separate the pointed top from the circular base, which are not mirror images.', 'B1 planes through axis; B1 perpendicular plane fails [2]'),
])


@y2.add('C1', (1, 2, 3))
def y2_q(r, D):
    nm, p, ax = r.choice(SOL)
    c = str(p)
    ds = [str(x) for x in ([3, 4, 5, 6, 7, 9, 12, 'infinitely many'] if True else []) if str(x) != c]
    return SMC(r, f'How many planes of symmetry does a {nm} have?', c, ds, f'A {nm} has {p} planes of symmetry; rotational symmetry {ax}.')


@y2.add('C2', (2, 3, 4), 'explain')
def y2_err(r, D):
    n = r.choice([3, 4, 5, 6, 8])
    nm = person(r)
    return Q(f'{nm} says that a right prism whose cross-section is a regular polygon with {n} sides has {n} planes of symmetry, the same as the number of lines of symmetry of the cross-section. Explain why {nm} is not quite right.',
             f'There are {n} vertical planes through the lines of symmetry of the cross-section, plus one more plane halfway along the prism parallel to the ends, so {n + 1} planes.',
             f'B1 {n} planes from the cross-section; B1 extra plane through the middle, total {n + 1} [2]')


@y2.add('C3', (2, 3, 4))
def y2_calc(r, D):
    n = r.choice([3, 4, 5, 6, 7, 8, 10, 12])
    kind = r.choice(['prism', 'pyramid'])
    poly = POLY.get(n, f'regular {n}-sided polygon')
    if n == 4:
        poly = 'square'
    if kind == 'prism':
        extra = '' if n != 4 else ' (the prism is not a cube)'
        return Q(f'A right prism has a cross-section that is {art(poly)}{extra}. Write down (a) the number of planes of symmetry and (b) the order of rotational symmetry about the axis through the centres of its two end faces.',
                 f'(a) {n + 1} (b) {n}', f'(a) B1 {n} planes through the axis and 1 parallel to the ends (b) B1 {n}.', type='short', marks=2)
    return Q(f'A right pyramid has a base that is {art(poly)}, with its apex directly above the centre of the base. Write down (a) the number of planes of symmetry and (b) the order of rotational symmetry about the vertical axis.',
             f'(a) {n} (b) {n}', f'(a) B1 {n} planes, each containing the axis and a line of symmetry of the base (b) B1 {n}.', type='short', marks=2)


@y2.add('C3', (3, 4, 5))
def y2_faces(r, D):
    n = r.choice([3, 5, 6, 8])
    poly = POLY[n]
    F, E, V = n + 2, 3 * n, 2 * n
    return Q(f'A right prism has a {poly} as its cross-section. Find (a) the number of faces, edges and vertices and (b) the number of planes of symmetry. (c) Show that the numbers in (a) satisfy F + V − E = 2.',
             f'(a) F = {F}, E = {E}, V = {V} (b) {n + 1} (c) {F} + {V} − {E} = 2', 'B1 B1 B1 (a); B1 (b); B1 (c).', type='multi_step', marks=5)


def y2_c4(r, D):
    n = r.choice([3, 4, 6, 8])
    s = r.choice([2, 3, 4, 5])
    L = r.choice([10, 12, 15, 20])
    poly = POLY[n] if n != 4 else 'square'
    area = n * s * s / (4 * math.tan(math.pi / n))
    intro = f'A chocolate box made in {city(r)} is a right prism of length {L} cm. Its cross-section is {art(poly)} of side {s} cm.'
    parts = [
        P('Write down the number of planes of symmetry of the box.', f'{n + 1}', 'B1', 1),
        P('Write down the order of rotational symmetry about the axis through the centres of the end faces.', f'{n}', 'B1', 1),
        P('Calculate the area of the cross-section.', f'{n3(area)} cm²', 'M1 correct method (e.g. split into triangles and use ½ab sin C); A1', 2),
        P('Calculate the volume of the box.', f'{n3(area * L)} cm³', f'M1 area × {L}; A1', 2),
        P('Explain why this prism has exactly one plane of symmetry that is perpendicular to its length.', 'Only the plane halfway along the prism reflects one end face onto the other.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


y2.add('C4', (2, 3, 4, 5))(y2_c4)

# ---------------------------------------------------------------- circle symmetry: chords and tangents
y3 = topic('Symmetry properties of circles', 'symmetry properties of circles', 'chords and tangents', 'circle chords tangents')
y3.fixed('C1', (1, 2), [
    ('The angle between a tangent to a circle and the radius at the point of contact is', '90°', 'A tangent is perpendicular to the radius at the point of contact.', ['45°', '180°', '60°']),
    ('The perpendicular from the centre of a circle to a chord', 'bisects the chord', 'It meets the chord at its midpoint.', ['is equal to the radius', 'is a tangent', 'trisects the chord']),
    ('Two tangents are drawn from an external point P to a circle, touching at A and B. Which is true?', 'PA = PB', 'Tangents from an external point are equal in length.', ['PA = 2PB', 'PA is perpendicular to PB', 'PA = the radius']),
    ('Equal chords in a circle are', 'the same distance from the centre', 'By symmetry equal chords are equidistant from the centre.', ['parallel', 'perpendicular', 'diameters']),
    ('The line from the centre of a circle to the midpoint of a chord is', 'perpendicular to the chord', 'Converse of the bisecting property.', ['parallel to the chord', 'a tangent', 'equal in length to the chord']),
])
y3.fixed('C2', (2, 3), [
    ('Explain why the perpendicular from the centre O to a chord AB bisects AB.', 'OA = OB (radii), so triangle OAB is isosceles; the perpendicular from O is a line of symmetry, so it meets AB at its midpoint (RHS congruent triangles).', 'B1 radii equal/isosceles; B1 symmetry or congruence [2]'),
    ('Explain why the two tangents from an external point to a circle are equal in length.', 'The triangles formed with the centre are right-angled (tangent ⟂ radius), share the hypotenuse OP and have equal radii, so they are congruent (RHS) and the tangents are equal.', 'B1 right angles; B1 congruent triangles (RHS) [2]'),
    ('Explain why the line from the centre to an external point bisects the angle between the two tangents.', 'The two right-angled triangles are congruent (RHS), so the angles at the external point are equal.', 'B1 congruent triangles; B1 equal angles [2]'),
])


@y3.add('C1', (1, 2, 3))
def y3_q(r, D):
    r_, d = r.choice([(5, 3), (10, 6), (13, 5), (13, 12), (10, 8), (17, 8), (25, 7), (15, 9)])
    half = int(math.isqrt(r_ * r_ - d * d))
    return MC(r, f'A chord of a circle of radius {r_} cm is {d} cm from the centre. What is the length of the chord?', 2 * half, [half, r_ + d, 2 * d, 2 * r_ - d], f'Half-chord = √({r_}² − {d}²) = {half}; chord = {2 * half} cm.', unit=' cm')


@y3.add('C2', (2, 3, 4), 'explain')
def y3_err(r, D):
    r_ = r.choice([6, 7, 8, 9, 10, 12])
    d = r.choice([12, 15, 16, 20, 24])
    nm = person(r)
    t = math.sqrt(d * d - r_ * r_)
    return Q(f'A tangent from a point P touches a circle with centre O and radius {r_} cm at T. OP = {d} cm. {nm} calculates PT = √({d}² + {r_}²) = {n3(math.sqrt(d * d + r_ * r_))} cm. Explain the error and find PT.',
             f'Angle OTP = 90°, so OP is the hypotenuse: PT = √({d}² − {r_}²) = {n3(t)} cm.', f'B1 OP is hypotenuse (tangent ⟂ radius); M1 √({d}² − {r_}²); A1 {n3(t)} cm [3]', marks=3)


@y3.add('C3', (2, 3, 4, 5))
def y3_calc(r, D):
    kind = r.choice(['chord', 'dist', 'tangent', 'angle'])
    r_ = r.choice([5, 6.5, 7, 8, 9, 10, 12])
    if kind == 'chord':
        d = round(r_ * r.uniform(0.3, 0.8), 1)
        L = 2 * math.sqrt(r_ * r_ - d * d)
        return Q(f'A circle has centre O and radius {ex(r_)} cm. The chord AB is {ex(d)} cm from O. Calculate the length of AB.', f'{n3(L)} cm', f'B1 perpendicular from O bisects AB; M1 √({ex(r_)}² − {ex(d)}²) = {n3(L / 2)}; A1 {n3(L)} cm.')
    if kind == 'dist':
        L = round(r_ * r.uniform(0.8, 1.8), 1)
        d = math.sqrt(r_ * r_ - (L / 2) ** 2)
        return Q(f'A chord of length {ex(L)} cm is drawn in a circle of radius {ex(r_)} cm. Calculate the distance of the chord from the centre.', f'{n3(d)} cm', f'M1 half-chord {ex(L / 2)}; M1 √({ex(r_)}² − {ex(L / 2)}²); A1 {n3(d)} cm.')
    if kind == 'tangent':
        d = round(r_ * r.uniform(1.4, 3), 1)
        t = math.sqrt(d * d - r_ * r_)
        return Q(f'From a point P, {ex(d)} cm from the centre O of a circle of radius {ex(r_)} cm, a tangent touches the circle at T. Calculate the length PT and the angle OPT.', f'PT = {n3(t)} cm; angle OPT = {math.degrees(math.asin(r_ / d)):.1f}°',
                 f'B1 angle OTP = 90°; M1 √({ex(d)}² − {ex(r_)}²); A1 {n3(t)}; M1 sin OPT = {ex(r_)}/{ex(d)}; A1 {math.degrees(math.asin(r_ / d)):.1f}°.')
    a = r.randint(30, 80)
    return Q(f'PA and PB are tangents from P to a circle with centre O. Angle APB = {a}°. Calculate angle AOB, giving reasons.', f'{180 - a}°',
             f'B1 angle OAP = angle OBP = 90° (tangent ⟂ radius); M1 angles in quadrilateral sum to 360°: 360 − 90 − 90 − {a}; A1 {180 - a}°.')


def y3_c4(r, D):
    r_ = r.choice([5, 6, 8, 9, 10])
    d = r.choice([13, 15, 17, 20, 25]) if r_ < 10 else r.choice([20, 26, 30])
    t = math.sqrt(d * d - r_ * r_)
    apo = math.degrees(math.asin(r_ / d))
    intro = f'Tangents PA and PB are drawn from a point P to a circle with centre O and radius {r_} cm. OP = {d} cm.'
    parts = [
        P('Write down the size of angle OAP, giving a reason.', '90°: a tangent is perpendicular to the radius at the point of contact.', 'B1 B1', 2),
        P('Calculate the length PA.', f'{n3(t)} cm', f'M1 √({d}² − {r_}²); A1', 2),
        P('Calculate angle APB.', f'{2 * apo:.1f}°', f'M1 sin APO = {r_}/{d}; M1 × 2; A1', 3),
        P('Calculate the area of the kite OAPB.', f'{n3(r_ * t)} cm²', f'M1 2 × ½ × {r_} × PA; A1', 2),
        P('Explain why OP is a line of symmetry of OAPB.', 'Triangles OAP and OBP are congruent (RHS), so reflecting in OP maps A to B.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


y3.add('C4', (2, 3, 4, 5))(y3_c4)

# ---------------------------------------------------------------- angles in circles
y4 = topic('Angle relationships in circles and proofs', 'angle relationships in circles', 'circle theorems proofs', 'angles in circles')
y4.fixed('C1', (1, 2), [
    ('The angle subtended by an arc at the centre of a circle is', 'twice the angle subtended at the circumference', 'Angle at the centre = 2 × angle at the circumference.', ['equal to the angle at the circumference', 'half the angle at the circumference', '90°']),
    ('The angle in a semicircle is', '90°', 'An angle subtended by a diameter at the circumference is a right angle.', ['180°', '45°', '60°']),
    ('Opposite angles of a cyclic quadrilateral', 'add up to 180°', 'Cyclic quadrilateral: opposite angles are supplementary.', ['are equal', 'add up to 360°', 'add up to 90°']),
    ('Angles in the same segment of a circle', 'are equal', 'Angles subtended by the same chord on the same side are equal.', ['add up to 180°', 'are right angles', 'add up to 90°']),
    ('The alternate segment theorem says that the angle between a tangent and a chord is equal to', 'the angle in the alternate segment', 'Angle between tangent and chord = angle subtended by the chord in the opposite segment.', ['the angle at the centre', '90°', 'half the angle at the centre on the same side']),
])
y4.fixed('C2', (2, 3), [
    ('Explain why the angle in a semicircle is 90°.', 'The diameter subtends an angle of 180° at the centre, and the angle at the circumference is half the angle at the centre, so it is 90°.', 'B1 angle at centre 180°; B1 half is 90° [2]'),
    ('Explain why a quadrilateral with opposite angles of 100° and 70° cannot be cyclic.', 'Opposite angles of a cyclic quadrilateral must add up to 180°, but 100° + 70° = 170°.', 'B1 rule; B1 check [2]'),
    ('Give a reason why triangle OAB, where O is the centre and A and B are on the circle, is isosceles.', 'OA and OB are both radii, so they are equal.', 'B1 radii equal; B1 base angles equal [2]'),
])


@y4.add('C1', (1, 2, 3))
def y4_q(r, D):
    x = r.randint(20, 85)
    if r.random() < 0.5:
        return MC(r, f'A, B and C lie on a circle with centre O. Angle ACB = {x}°. What is angle AOB?', 2 * x, [x, x / 2, 180 - x, 180 - 2 * x if 180 - 2 * x > 0 else 3 * x, 90 + x], 'Angle at the centre is twice the angle at the circumference.', fmtf=lambda v: f'{num(v)}°')
    return MC(r, f'ABCD is a cyclic quadrilateral. Angle ABC = {x + 40}°. What is angle ADC?', 180 - (x + 40), [x + 40, 360 - (x + 40), 90 - (x + 40) / 2 if x < 50 else x, 2 * (x + 40) if 2 * (x + 40) < 360 else 45, (x + 40) / 2],
              'Opposite angles of a cyclic quadrilateral add up to 180°.', fmtf=lambda v: f'{num(v)}°')


@y4.add('C2', (2, 3, 4), 'explain')
def y4_err(r, D):
    x = r.randint(25, 80)
    nm = person(r)
    kind = r.choice(['centre', 'cyclic', 'segment'])
    if kind == 'centre':
        return Q(f'A, B and C lie on a circle with centre O. Angle AOB = {2 * x}°. {nm} says angle ACB = {2 * x}° because "they stand on the same arc". Explain the error and give the correct angle.',
                 f'The angle at the centre is twice the angle at the circumference, so angle ACB = {x}°.', f'B1 correct theorem; B1 {x}° [2]')
    if kind == 'cyclic':
        return Q(f'PQRS is a cyclic quadrilateral with angle PQR = {x + 50}°. {nm} says angle PSR = {x + 50}° because opposite angles are equal. Explain the error and find angle PSR.',
                 f'Opposite angles of a cyclic quadrilateral add to 180°, so angle PSR = {130 - x}°.', f'B1 supplementary; B1 {130 - x}° [2]')
    return Q(f'A, B, C and D lie on a circle, with C and D on the same side of AB. Angle ACB = {x}°. {nm} says angle ADB = {180 - x}°. Explain the error and give the correct angle.',
             f'Angles in the same segment are equal, so angle ADB = {x}°; {180 - x}° would only apply to a point on the other side of AB (cyclic quadrilateral).', f'B1 same segment theorem; B1 {x}° [2]')


@y4.add('C3', (2, 3, 4, 5))
def y4_calc(r, D):
    x = r.randint(25, 75)
    kind = r.choice(['iso', 'semi', 'alt', 'cyc2', 'tanrad'])
    if kind == 'iso':
        return Q(f'A, B and C lie on a circle with centre O. Angle ACB = {x}°. Calculate angle OAB, giving reasons for each step.', f'{90 - x}°',
                 f'B1 angle AOB = {2 * x}° (angle at centre = 2 × angle at circumference); M1 OA = OB radii so triangle isosceles; A1 (180 − {2 * x}) ÷ 2 = {90 - x}°.')
    if kind == 'semi':
        y = r.randint(20, 70)
        return Q(f'AB is a diameter of a circle and C is a point on the circumference. Angle CAB = {y}°. Calculate angle ABC, giving reasons.', f'{90 - y}°',
                 f'B1 angle ACB = 90° (angle in a semicircle); M1 angles in a triangle: 180 − 90 − {y}; A1 {90 - y}°.')
    if kind == 'alt':
        y = r.randint(30, 80)
        return Q(f'TA is a tangent to a circle at A. B and C are points on the circle. Angle TAB = {y}° and C is in the alternate segment. Find angle ACB and angle AOB, where O is the centre, giving reasons.', f'Angle ACB = {y}°; angle AOB = {2 * y}°',
                 f'B1 ACB = {y}° (alternate segment theorem); B1 AOB = {2 * y}° (angle at centre twice angle at circumference); B1 reasons.')
    if kind == 'cyc2':
        a, b = r.randint(60, 120), r.randint(55, 115)
        return Q(f'ABCD is a cyclic quadrilateral. Angle DAB = {a}° and angle ABC = {b}°. Find angle BCD and angle CDA, giving a reason.', f'Angle BCD = {180 - a}°; angle CDA = {180 - b}°',
                 f'B1 {180 - a}°; B1 {180 - b}°; B1 opposite angles of a cyclic quadrilateral add up to 180°.')
    y = r.randint(20, 65)
    return Q(f'PT is a tangent to a circle with centre O at the point T. Angle TOP = {y}°. Calculate angle OPT, giving a reason.', f'{90 - y}°', f'B1 angle OTP = 90° (tangent ⟂ radius); M1 180 − 90 − {y}; A1 {90 - y}°.')


def y4_c4(r, D):
    x = r.randint(28, 78)
    intro = f'A, B, C and D lie on a circle with centre O. C and D are on opposite sides of the chord AB, with C on the major arc. TA is the tangent at A, on the opposite side of AB from C. Angle ACB = {x}°.'
    parts = [
        P('Find angle AOB, giving a reason.', f'{2 * x}°: angle at the centre is twice the angle at the circumference.', 'B1 B1', 2),
        P('Find angle OAB, giving reasons.', f'{90 - x}°: triangle OAB is isosceles (OA = OB radii).', f'M1 (180 − {2 * x}) ÷ 2; A1 with reason', 2),
        P('Find angle TAB, giving a reason.', f'{x}°: alternate segment theorem (or 90° − {90 - x}° using tangent ⟂ radius).', 'B1 B1', 2),
        P('Find angle ADB, giving a reason.', f'{180 - x}°: opposite angles of the cyclic quadrilateral ACBD add up to 180°.', 'B1 B1', 2),
        P('Find angle OAT, giving a reason.', '90°: tangent is perpendicular to the radius.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


y4.add('C4', (2, 3, 4, 5))(y4_c4)
CHAPTERS[7] = [y1, y2, y3, y4]


# =========================================================== 8 Histograms and frequency distribution diagrams (Ch 20)
GCTX = [('time taken to complete a puzzle', 'minutes', 't', 1), ('mass of parcels at a depot', 'kg', 'm', 1), ('height of seedlings', 'cm', 'h', 1),
        ('journey time to school', 'minutes', 't', 1), ('length of phone calls', 'minutes', 't', 1), ('distance thrown in a javelin competition', 'm', 'd', 1),
        ('daily rainfall', 'mm', 'r', 1), ('waiting time at a clinic', 'minutes', 'w', 1), ('mass of apples', 'g', 'm', 2), ('length of fish caught', 'cm', 'l', 1)]
WPAT = [[10, 10, 5, 5, 10, 20], [5, 5, 10, 20, 20], [20, 10, 10, 20, 40], [10, 20, 10, 5, 15], [15, 5, 10, 10, 20], [25, 25, 50, 50, 100], [10, 5, 5, 10, 30]]


def grouped(r, D, equal=False):
    name, unit, v, sc = r.choice(GCTX)
    w = [10] * r.choice([4, 5, 6]) if equal else list(r.choice(WPAT))
    if sc == 2:
        w = [x * 2 for x in w]
    s0 = r.choice([0, 10, 20, 40, 50]) * (2 if sc == 2 else 1)
    b = [s0]
    for x in w:
        b.append(b[-1] + x)
    fds = [r.choice([0.4, 0.6, 0.8, 1, 1.2, 1.6, 2, 2.4, 3, 3.2, 3.6, 4, 4.4, 5]) for _ in w]
    f = [max(1, round(fd * x)) for fd, x in zip(fds, w)]
    return name, unit, v, b, f


def gtab(v, unit, b, f):
    return '; '.join(f'{num(b[i])} < {v} ≤ {num(b[i + 1])}: {f[i]}' for i in range(len(f))) + f' ({v} in {unit})'


def cfs(f):
    out, s = [], 0
    for x in f:
        s += x
        out.append(s)
    return out


def interp(b, f, pos):
    c = 0
    for i, x in enumerate(f):
        if c + x >= pos:
            return b[i] + (pos - c) / x * (b[i + 1] - b[i])
        c += x
    return b[-1]


def count_below(b, f, val):
    c = 0
    for i, x in enumerate(f):
        if val >= b[i + 1]:
            c += x
        elif val > b[i]:
            c += x * (val - b[i]) / (b[i + 1] - b[i])
    return c


h1 = topic('Histograms and frequency density', 'histograms with equal and unequal class widths', 'frequency density', 'histograms')
h1.fixed('C1', (1, 2), [
    ('How is frequency density calculated?', 'frequency ÷ class width', 'Frequency density = frequency / class width.', ['class width ÷ frequency', 'frequency × class width', 'frequency ÷ total frequency']),
    ('In a histogram, the frequency of a class is represented by', 'the area of its bar', 'Area = frequency density × class width = frequency.', ['the height of its bar', 'the width of its bar', 'the midpoint of the class']),
    ('What is plotted on the vertical axis of a histogram with unequal class widths?', 'Frequency density', 'Using frequency density makes the areas proportional to frequency.', ['Frequency', 'Cumulative frequency', 'Class width']),
    ('A class 20 < t ≤ 30 has frequency 15. What is its frequency density?', '1.5', '15 ÷ 10 = 1.5.', ['15', '0.67', '150']),
    ('In a histogram there are no gaps between the bars because', 'the data are continuous', 'Continuous data classes meet at their boundaries.', ['the frequencies are equal', 'the data are qualitative', 'it makes it easier to read']),
])
h1.fixed('C2', (2, 3), [
    ('Explain why frequency density, not frequency, is used for the heights of bars when class widths are unequal.', 'A wider class would look too important if height showed frequency; using frequency density makes the area of each bar proportional to its frequency.', 'B1 wider classes exaggerated; B1 area ∝ frequency [2]'),
    ('Explain how to find the frequency of a class from a histogram.', 'Multiply the frequency density (bar height) by the class width (bar width), i.e. find the area of the bar.', 'B1 height × width; B1 area = frequency [2]'),
    ('Explain why the modal class of data with unequal widths is the class with the highest frequency density, not the highest frequency.', 'The modal class is where the data are most concentrated per unit of the variable, which is shown by the tallest bar (largest frequency density).', 'B1 concentration per unit width; B1 tallest bar [2]'),
])


@h1.add('C1', (1, 2, 3))
def h1_fd(r, D):
    w = r.choice([5, 10, 15, 20, 25, 40, 50])
    f = r.choice([6, 12, 18, 24, 30, 36, 45, 60])
    a = r.choice([0, 10, 20, 30, 50, 100])
    return MC(r, f'A class {a} < x ≤ {a + w} has a frequency of {f}. What is the frequency density?', f / w, [f * w, w / f, f, f / (a + w)], f'{f} ÷ {w} = {ex(round(f / w, 4))}.', fmtf=lambda x: ex(round(x, 3)))


@h1.add('C2', (2, 3, 4), 'explain')
def h1_err(r, D):
    name, unit, v, b, f = grouped(r, D)
    i = max(range(len(f)), key=lambda j: b[j + 1] - b[j])
    nm = person(r)
    w = b[i + 1] - b[i]
    return Q(f'{nm} draws a histogram of the {name}. For the class {num(b[i])} < {v} ≤ {num(b[i + 1])}, which has frequency {f[i]}, {nm} draws a bar of height {f[i]}. Explain the error and give the correct height.',
             f'The class width is {w}, so the bar height must be the frequency density {f[i]} ÷ {w} = {ex(round(f[i] / w, 3))}.', f'B1 must use frequency density; B1 {ex(round(f[i] / w, 3))} [2]')


@h1.add('C3', (1, 2, 3, 4))
def h1_table(r, D):
    name, unit, v, b, f = grouped(r, D)
    fds = [ex(round(x / (b[i + 1] - b[i]), 3)) for i, x in enumerate(f)]
    if D <= 2:
        i = r.randrange(len(f))
        return Q(f'The table shows the {name}. {gtab(v, unit, b, f)}. Calculate the frequency density for the class {num(b[i])} < {v} ≤ {num(b[i + 1])}.', fds[i], f'M1 {f[i]} ÷ {b[i + 1] - b[i]}; A1 {fds[i]}.')
    return Q(f'The table shows the {name}. {gtab(v, unit, b, f)}. Calculate the frequency density of each class, ready to draw a histogram.', ', '.join(fds),
             'M1 frequency ÷ class width for each; A2 all correct (A1 for at least three correct).')


@h1.add('C3', (2, 3, 4, 5))
def h1_back(r, D):
    name, unit, v, b, f = grouped(r, D)
    fd = [x / (b[i + 1] - b[i]) for i, x in enumerate(f)]
    i, j = r.sample(range(len(f)), 2)
    desc = '; '.join(f'bar {num(b[k])}–{num(b[k + 1])} has height {ex(round(fd[k], 3))}' for k in (i, j))
    if D >= 4:
        val = b[i] + (b[i + 1] - b[i]) / 2
        est = count_below(b, f, b[-1]) - count_below(b, f, val)
        return Q(f'A histogram shows the {name} ({v} in {unit}). The class widths and bar heights (frequency density) are: ' + '; '.join(f'{num(b[k])} < {v} ≤ {num(b[k + 1])}, height {ex(round(fd[k], 3))}' for k in range(len(f))) +
                 f'. Estimate the number of values greater than {num(val)}.', ex(round(est, 1)), f'M1 frequencies = height × width; M1 half of class {num(b[i])}–{num(b[i + 1])} ({ex(f[i] / 2)}); A1 {ex(round(est, 1))}.')
    return Q(f'A histogram shows the {name}. In the histogram, {desc}. Calculate the frequency of each of these two classes.', f'{f[i]} and {f[j]}',
             f'M1 frequency = frequency density × class width; A1 {f[i]}; A1 {f[j]}.')


@h1.add('C3', (2, 3, 4))
def h1_mean(r, D):
    name, unit, v, b, f = grouped(r, D)
    mids = [(b[i] + b[i + 1]) / 2 for i in range(len(f))]
    tot = sum(f)
    m = sum(x * y for x, y in zip(mids, f)) / tot
    return Q(f'The table shows the {name}. {gtab(v, unit, b, f)}. Calculate an estimate of the mean.', f'{n3(m)} {unit}',
             f'M1 midpoints {", ".join(ex(x) for x in mids)}; M1 Σfx = {ex(round(sum(x * y for x, y in zip(mids, f)), 2))} ÷ {tot}; A1 {n3(m)}.')


def h1_c4(r, D):
    name, unit, v, b, f = grouped(r, D)
    fd = [x / (b[i + 1] - b[i]) for i, x in enumerate(f)]
    tot = sum(f)
    mids = [(b[i] + b[i + 1]) / 2 for i in range(len(f))]
    m = sum(x * y for x, y in zip(mids, f)) / tot
    mod = max(range(len(f)), key=lambda i: fd[i])
    cut = b[2] + (b[3] - b[2]) / 2 if len(b) > 3 else b[1]
    over = tot - count_below(b, f, cut)
    intro = f'A survey records the {name} for {tot} items in {city(r)}. {gtab(v, unit, b, f)}.'
    parts = [
        P('Calculate the frequency density for each class.', ', '.join(ex(round(x, 3)) for x in fd), 'M1 f ÷ w; A1 all', 2),
        P('Write down the modal class.', f'{num(b[mod])} < {v} ≤ {num(b[mod + 1])}', 'B1 highest frequency density', 1),
        P('Calculate an estimate of the mean.', f'{n3(m)} {unit}', 'M1 midpoints; M1 Σfx ÷ Σf; A1', 3),
        P(f'Estimate the number of items with {v} > {num(cut)}.', ex(round(over, 1)), 'M1 proportion of split class; A1', 2),
        P('Explain why the mean is only an estimate.', 'The exact values are not known; midpoints are used to represent each class.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


h1.add('C4', (2, 3, 4, 5))(h1_c4)

# ---------------------------------------------------------------- cumulative frequency
h2 = topic('Cumulative frequency tables and curves', 'cumulative frequency tables and curves', 'cumulative frequency', 'ogive')
h2.fixed('C1', (1, 2), [
    ('When drawing a cumulative frequency curve from grouped data, each point is plotted at', 'the upper class boundary', 'Cumulative frequency counts values up to the end of each class.', ['the class midpoint', 'the lower class boundary', 'the class width']),
    ('The last value in a cumulative frequency table is equal to', 'the total frequency', 'It counts all the values.', ['the largest frequency', 'the median', 'the class width']),
    ('Frequencies are 4, 9, 12 and 5. What are the cumulative frequencies?', '4, 13, 25, 30', 'Running totals: 4, 4 + 9, 13 + 12, 25 + 5.', ['4, 9, 12, 5', '4, 13, 21, 26', '30, 26, 17, 5']),
    ('A cumulative frequency curve', 'never decreases from left to right', 'Running totals can only increase or stay the same.', ['always passes through the origin', 'is always a straight line', 'has a maximum in the middle']),
])
h2.fixed('C2', (2, 3), [
    ('Explain why cumulative frequencies are plotted at upper class boundaries and not at midpoints.', 'The cumulative frequency is the number of values less than or equal to the end of the class; only at the upper boundary are all those values included.', 'B1 counts values up to end of class; B1 upper boundary [2]'),
    ('Explain why a cumulative frequency curve can never go down.', 'Each new class adds a frequency of zero or more to the running total, so the total never decreases.', 'B1 adding non-negative frequencies; B1 never decreases [2]'),
    ('Describe how to use a cumulative frequency curve to find how many values are greater than a given value.', 'Read the cumulative frequency at that value and subtract it from the total frequency.', 'B1 read CF; B1 subtract from total [2]'),
])


@h2.add('C1', (1, 2, 3))
def h2_q(r, D):
    f = [r.randint(2, 20) for _ in range(r.choice([4, 5]))]
    c = ', '.join(map(str, cfs(f)))
    wrong1 = ', '.join(map(str, f))
    wrong2 = ', '.join(map(str, cfs(f)[:-1] + [cfs(f)[-1] + 1]))
    wrong3 = ', '.join(map(str, cfs(list(reversed(f)))))
    wrong4 = ', '.join(map(str, [0] + cfs(f)[:-1]))
    return SMC(r, f'The frequencies in a grouped table are {", ".join(map(str, f))}. What are the cumulative frequencies?', c, [wrong1, wrong2, wrong3, wrong4], f'Running totals: {c}.')


@h2.add('C2', (2, 3, 4), 'explain')
def h2_err(r, D):
    name, unit, v, b, f = grouped(r, D, equal=True)
    nm = person(r)
    pts = ', '.join(f'({ex((b[i] + b[i + 1]) / 2)}, {c})' for i, c in enumerate(cfs(f)))
    right = ', '.join(f'({num(b[i + 1])}, {c})' for i, c in enumerate(cfs(f)))
    return Q(f'For the {name}, {gtab(v, unit, b, f)}. {nm} plots the cumulative frequency points {pts}. Explain the error and write down the correct points to plot.',
             f'Cumulative frequencies must be plotted at the upper class boundaries: ({num(b[0])}, 0), {right}.', 'B1 upper boundaries not midpoints; B1 correct points (including the start point) [2]')


@h2.add('C3', (1, 2, 3, 4))
def h2_table(r, D):
    name, unit, v, b, f = grouped(r, D, equal=D <= 2)
    cf = cfs(f)
    if D <= 2:
        k = r.randrange(1, len(f))
        return Q(f'The table shows the {name}. {gtab(v, unit, b, f)}. Complete a cumulative frequency table and find how many values are at most {num(b[k + 1])}.',
                 f'Cumulative frequencies {", ".join(map(str, cf))}; {cf[k]} values', f'M1 running totals; A1 {cf[k]}.')
    k = r.randrange(1, len(f) - 1)
    return Q(f'The table shows the {name}. {gtab(v, unit, b, f)}. (a) Write down the cumulative frequencies. (b) Write down the coordinates of the points to plot for the cumulative frequency curve. (c) Find how many values are greater than {num(b[k + 1])}.',
             f'(a) {", ".join(map(str, cf))} (b) ({num(b[0])}, 0), ' + ', '.join(f'({num(b[i + 1])}, {c})' for i, c in enumerate(cf)) + f' (c) {cf[-1] - cf[k]}',
             f'(a) B1 (b) B1 upper boundaries, B1 start point (c) M1 {cf[-1]} − {cf[k]}; A1 {cf[-1] - cf[k]}.', type='multi_step', marks=5)


def h2_c4(r, D):
    name, unit, v, b, f = grouped(r, D, equal=r.random() < 0.5)
    cf = cfs(f)
    n = cf[-1]
    med = interp(b, f, n / 2)
    k = r.randrange(1, len(f) - 1)
    cut = b[k] + (b[k + 1] - b[k]) / 2
    below = count_below(b, f, cut)
    intro = f'The {name} for {n} cases in {city(r)} is summarised as {gtab(v, unit, b, f)}.'
    parts = [
        P('Complete a cumulative frequency table.', ', '.join(map(str, cf)), 'B1 running totals', 1),
        P('Write down the points that should be plotted to draw the cumulative frequency curve.', f'({num(b[0])}, 0), ' + ', '.join(f'({num(b[i + 1])}, {c})' for i, c in enumerate(cf)), 'B1 upper boundaries; B1 start point', 2),
        P('Treating the curve as straight between plotted points, estimate the median.', f'{n3(med)} {unit}', f'M1 CF = {ex(n / 2)}; M1 interpolation within class; A1', 3),
        P(f'Estimate the percentage of cases with {v} > {num(cut)}.', f'{n3((n - below) / n * 100)}%', 'M1 read CF at value; M1 (n − CF) ÷ n × 100; A1', 3),
        P('Explain why the median from a cumulative frequency curve is an estimate.', 'The data are grouped, so the exact values are unknown; values are assumed to be spread through each class.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


h2.add('C4', (2, 3, 4, 5))(h2_c4)

# ---------------------------------------------------------------- median, quartiles, percentiles
h3 = topic('Median, quartiles, interquartile range and percentiles', 'median, quartiles, interquartile range', 'percentiles from cumulative frequency', 'interquartile range')
h3.fixed('C1', (1, 2), [
    ('For 200 values, at which cumulative frequency is the median read from a cumulative frequency curve?', '100', 'For large n, the median is at n/2.', ['50', '150', '101']),
    ('How is the interquartile range calculated?', 'Upper quartile − lower quartile', 'IQR = Q₃ − Q₁, the range of the middle 50%.', ['Largest value − smallest value', 'Median − lower quartile', 'Upper quartile + lower quartile']),
    ('For 80 values, at which cumulative frequency is the upper quartile read?', '60', '¾ × 80 = 60.', ['20', '40', '75']),
    ('The 90th percentile of a distribution is the value', 'below which 90% of the data lie', 'Read at 0.9n on the cumulative frequency axis.', ['above which 90% of the data lie', 'that occurs 90 times', 'that is 90 more than the median']),
    ('Which measure of spread is not affected by extreme values?', 'The interquartile range', 'It uses only the middle half of the data.', ['The range', 'The mean', 'The total']),
])
h3.fixed('C2', (2, 3), [
    ('Explain why the interquartile range is often a better measure of spread than the range.', 'The range depends only on the two extreme values, which may be outliers; the IQR covers the middle 50% so is not affected by extremes.', 'B1 range uses extremes; B1 IQR middle 50% [2]'),
    ('Explain what it means if the 10th percentile of journey times is 12 minutes.', '10% of the journeys took 12 minutes or less (and 90% took longer).', 'B1 10% at or below; B1 in context [2]'),
    ('Describe how to find the lower quartile from a cumulative frequency curve for 120 values.', 'Find 30 (one quarter of 120) on the cumulative frequency axis, go across to the curve and down to read the value.', 'B1 n/4 = 30; B1 read across and down [2]'),
])


@h3.add('C1', (1, 2, 3))
def h3_q(r, D):
    n = r.choice([40, 60, 80, 120, 160, 200, 240, 300])
    which = r.choice([('median', 0.5), ('lower quartile', 0.25), ('upper quartile', 0.75), ('90th percentile', 0.9), ('20th percentile', 0.2)])
    c = n * which[1]
    return MC(r, f'A cumulative frequency curve is drawn for {n} values. At what cumulative frequency should the {which[0]} be read?', c,
              [n * 0.5 if which[1] != 0.5 else n * 0.25, n * (1 - which[1]) if which[1] != 0.5 else n * 0.75, which[1] * 100, c + 1, n], f'{which[0].capitalize()} at {ex(which[1])} × {n} = {ex(c)}.', fmtf=ex)


@h3.add('C2', (2, 3, 4), 'explain')
def h3_err(r, D):
    nm = person(r)
    lq, uq = r.randint(20, 40), r.randint(45, 80)
    mx, mn = uq + r.randint(10, 40), lq - r.randint(5, 18)
    return Q(f'From a cumulative frequency curve, the lowest value is {mn}, the lower quartile is {lq}, the upper quartile is {uq} and the highest value is {mx}. {nm} says the interquartile range is {mx} − {mn} = {mx - mn}. Explain the error and find the correct interquartile range.',
             f'{nm} has found the range. IQR = upper quartile − lower quartile = {uq} − {lq} = {uq - lq}.', f'B1 range vs IQR; B1 {uq - lq} [2]')


@h3.add('C3', (2, 3, 4, 5))
def h3_calc(r, D):
    name, unit, v, b, f = grouped(r, D, equal=D <= 2)
    n = sum(f)
    med, lq, uq = interp(b, f, n / 2), interp(b, f, n / 4), interp(b, f, 3 * n / 4)
    cf = cfs(f)
    tbl = '; '.join(f'{v} ≤ {num(b[i + 1])}: {c}' for i, c in enumerate(cf))
    if D <= 2:
        return Q(f'A cumulative frequency table for the {name} ({v} in {unit}) gives {tbl}. Assuming the cumulative frequency curve is a straight line between the plotted points, estimate the median.', f'{n3(med)} {unit}',
                 f'M1 CF = {ex(n / 2)}; M1 within the correct class; A1 {n3(med)}.')
    if D == 3:
        return Q(f'A cumulative frequency table for the {name} ({v} in {unit}) gives {tbl}. Assuming the cumulative frequency curve is a straight line between the plotted points, estimate the lower quartile, the upper quartile and the interquartile range.',
                 f'LQ {n3(lq)}, UQ {n3(uq)}, IQR {n3(uq - lq)} {unit}', f'M1 CF = {ex(n / 4)} and CF = {ex(3 * n / 4)}; A1 LQ; A1 UQ; A1 IQR.')
    p = r.choice([10, 20, 80, 90])
    pv = interp(b, f, n * p / 100)
    return Q(f'A cumulative frequency table for the {name} ({v} in {unit}) gives {tbl}. Assuming the cumulative frequency curve is a straight line between the plotted points, estimate (a) the median and (b) the {p}th percentile.',
             f'(a) {n3(med)} {unit} (b) {n3(pv)} {unit}', f'(a) M1 CF = {ex(n / 2)}; A1 (b) M1 CF = {ex(n * p / 100)}; A1.', type='multi_step', marks=4)


def h3_c4(r, D):
    name, unit, v, b, f = grouped(r, D)
    n = sum(f)
    cf = cfs(f)
    med, lq, uq = interp(b, f, n / 2), interp(b, f, n / 4), interp(b, f, 3 * n / 4)
    p = r.choice([10, 90])
    pv = interp(b, f, n * p / 100)
    tbl = '; '.join(f'{v} ≤ {num(b[i + 1])}: {c}' for i, c in enumerate(cf))
    intro = f'A cumulative frequency curve is drawn for {n} measurements of the {name} in {city(r)} ({v} in {unit}). It passes through ({num(b[0])}, 0) and the points {tbl}. Assume it is straight between these points.'
    parts = [
        P('Estimate the median.', f'{n3(med)} {unit}', f'M1 CF = {ex(n / 2)}; A1', 2),
        P('Estimate the interquartile range.', f'{n3(uq - lq)} {unit}', f'M1 LQ {n3(lq)}; M1 UQ {n3(uq)}; A1', 3),
        P(f'Estimate the {p}th percentile.', f'{n3(pv)} {unit}', f'M1 CF = {ex(n * p / 100)}; A1', 2),
        P('Explain what the interquartile range tells you about the data.', f'The middle 50% of the {name.split(" of ")[0]} values lie within a range of about {n3(uq - lq)} {unit}.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


h3.add('C4', (2, 3, 4, 5))(h3_c4)

# ---------------------------------------------------------------- comparing distributions
CMP = [('Class A', 'Class B', 'test marks', '%', 'higher marks', 20), ('Team Lions', 'Team Hawks', 'times to swim 50 m', 's', 'longer times', 30),
       ('Farm P', 'Farm Q', 'masses of tomatoes', 'g', 'heavier tomatoes', 60), ('Route 1', 'Route 2', 'journey times', 'minutes', 'longer journeys', 10),
       ('Garden X', 'Garden Y', 'heights of sunflowers', 'cm', 'taller sunflowers', 100), ('Monday', 'Saturday', 'waiting times in a café queue', 'minutes', 'longer waits', 0)]

h4 = topic('Comparing distributions', 'comparing distributions using histograms and cumulative frequency', 'comparing distributions', 'compare')
h4.fixed('C1', (1, 2), [
    ('When comparing two distributions, which pair of statistics is most useful?', 'An average and a measure of spread', 'For example the median and the interquartile range.', ['Two averages', 'The smallest and largest values only', 'The modal class and total frequency']),
    ('Group A has IQR 8 and group B has IQR 15. Which statement is correct?', 'Group A is more consistent', 'A smaller IQR means the middle 50% of values are closer together.', ['Group B is more consistent', 'Group A has a higher median', 'Group B has lower values']),
    ('On two cumulative frequency curves drawn on the same axes for the same number of items, the curve further to the right shows', 'generally larger values', 'It reaches each cumulative frequency at a larger value.', ['generally smaller values', 'more items', 'less spread always']),
    ('Which statistic is best for comparing typical values when there are extreme values?', 'The median', 'The median is not affected by extremes.', ['The mean', 'The range', 'The total']),
])
h4.fixed('C2', (2, 3), [
    ('Explain why a comparison of two distributions should refer to the context.', 'Statements such as "the median is higher" only become meaningful when they say what this means, for example that Class A students generally scored higher marks.', 'B1 statistics alone not enough; B1 interpret in context [2]'),
    ('Explain why a histogram and a cumulative frequency curve might both be useful when comparing two distributions.', 'A histogram shows the shape and modal class; a cumulative frequency curve allows the median and quartiles to be estimated and compared.', 'B1 histogram shape; B1 CF for median/quartiles [2]'),
])


@h4.add('C1', (1, 2, 3))
def h4_q(r, D):
    A, B, what, unit, hi, off = r.choice(CMP)
    ma, mb = off + r.randint(10, 50), off + r.randint(10, 50)
    ia, ib = r.randint(5, 20), r.randint(5, 20)
    if ia == ib:
        ib += 3
    c = f'{A}' if ia < ib else f'{B}'
    return SMC(r, f'The {what} for {A} have median {ma} {unit} and IQR {ia} {unit}. For {B} the median is {mb} {unit} and the IQR is {ib} {unit}. Which group\'s {what} are more consistent?', c,
               [x for x in [A, B, 'Both are equally consistent', 'It cannot be decided from the IQR', f'{A} and {B} have no spread'] if x != c], f'Smaller IQR ({min(ia, ib)}) means more consistent: {c}.')


@h4.add('C2', (2, 3, 4), 'explain')
def h4_cmp(r, D):
    A, B, what, unit, hi, off = r.choice(CMP)
    ma, mb = off + r.randint(10, 50), off + r.randint(10, 50)
    if ma == mb:
        mb += 4
    ia, ib = r.randint(5, 20), r.randint(5, 20)
    if ia == ib:
        ib += 3
    bigger = A if ma > mb else B
    cons = A if ia < ib else B
    return Q(f'The {what} of {A} have median {ma} {unit} and interquartile range {ia} {unit}. The {what} of {B} have median {mb} {unit} and interquartile range {ib} {unit}. Make two comparisons between the distributions.',
             f'The median for {bigger} is higher, so {bigger} generally had {hi}. The IQR for {cons} is smaller, so the {what} for {cons} are more consistent (less spread).',
             'B1 comparison of medians in context; B1 comparison of IQRs in context [2]')


@h4.add('C3', (2, 3, 4, 5))
def h4_calc(r, D):
    A, B, what, unit, hi, off = r.choice(CMP)
    n = r.choice([40, 60, 80, 100])
    b = [off + 10 * i for i in range(7)]
    def mk():
        while True:
            f = [r.randint(1, 20) for _ in range(6)]
            s = sum(f)
            f = [max(0, round(x * n / s)) for x in f]
            f[-1] += n - sum(f)
            if f[-1] >= 0 and all(x > 0 for x in f):
                return f
    fa, fb = mk(), mk()
    st = [(interp(b, f, n / 2), interp(b, f, 3 * n / 4) - interp(b, f, n / 4)) for f in (fa, fb)]
    t = lambda f: '; '.join(f'≤ {b[i + 1]}: {c}' for i, c in enumerate(cfs(f)))
    bigger = A if st[0][0] > st[1][0] else B
    cons = A if st[0][1] < st[1][1] else B
    return Q(f'Cumulative frequency tables for the {what} ({unit}) recorded for {A} and {B} ({n} values each) are: {A}: {t(fa)}. {B}: {t(fb)}. Assuming straight lines between plotted points, estimate the median and interquartile range for each, and compare the two distributions.',
             f'{A}: median {n3(st[0][0])}, IQR {n3(st[0][1])}; {B}: median {n3(st[1][0])}, IQR {n3(st[1][1])}. {bigger} generally has {hi}; {cons} is more consistent.',
             'M1 medians; A1 both; M1 quartiles; A1 both IQRs; B1 comparison of average in context; B1 comparison of spread in context.', marks=6)


def h4_c4(r, D):
    A, B, what, unit, hi, off = r.choice(CMP)
    ma, mb = off + r.randint(20, 40), off + r.randint(20, 40)
    if ma == mb:
        ma += 5
    la, lb = ma - r.randint(4, 12), mb - r.randint(4, 12)
    ua, ub = ma + r.randint(4, 12), mb + r.randint(4, 12)
    if ua - la == ub - lb:
        ub += 2
    ra, rb = (la - r.randint(5, 15), ua + r.randint(5, 25)), (lb - r.randint(5, 15), ub + r.randint(5, 25))
    intro = f'A researcher in {city(r)} compares the {what} ({unit}) for {A} and {B}. {A}: lowest {ra[0]}, lower quartile {la}, median {ma}, upper quartile {ua}, highest {ra[1]}. {B}: lowest {rb[0]}, lower quartile {lb}, median {mb}, upper quartile {ub}, highest {rb[1]}.'
    bigger = A if ma > mb else B
    cons = A if ua - la < ub - lb else (B if ub - lb < ua - la else 'neither (equal IQRs)')
    parts = [
        P('Calculate the interquartile range for each group.', f'{A}: {ua - la}; {B}: {ub - lb}', 'B1 B1', 2),
        P('Calculate the range for each group.', f'{A}: {ra[1] - ra[0]}; {B}: {rb[1] - rb[0]}', 'B1 B1', 2),
        P('Compare the medians in context.', f'{bigger} has the higher median, so generally {hi}.', 'B1', 1),
        P('Compare the spreads in context, using the most suitable measure.', f'Using the IQR (not affected by extremes): {cons} is more consistent.', 'B1 IQR used; B1 conclusion', 2),
        P(f'Explain why the interquartile range may be better than the range for comparing these groups.', 'The range is affected by a single extreme value; the IQR uses the middle 50%.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


h4.add('C4', (2, 3, 4, 5))(h4_c4)
CHAPTERS[8] = [h1, h2, h3, h4]


# =========================================================== 9 Ratio, rate and proportion (Ch 21)
def rstr(*xs):
    return ' : '.join(num(x) for x in xs)


def simp(*xs):
    g = 0
    for x in xs:
        g = math.gcd(g, x)
    return tuple(x // g for x in xs)


r1 = topic('Working with ratio', 'working with ratio', 'simplifying and sharing in a given ratio', 'ratio')
r1.fixed('C1', (1, 2), [
    ('Write 12 : 18 in its simplest form.', '2 : 3', 'Divide both parts by the HCF, 6.', ['3 : 2', '4 : 6', '6 : 9']),
    ('$40 is shared in the ratio 3 : 5. How much is the larger share?', '$25', '8 parts; one part = $5; 5 × 5 = 25.', ['$15', '$24', '$35']),
    ('Write 4 : 10 in the form 1 : n.', '1 : 2.5', 'Divide both parts by 4.', ['1 : 6', '2 : 5', '1 : 0.4']),
    ('Write 50 cm : 2 m in its simplest form.', '1 : 4', '2 m = 200 cm; 50 : 200 = 1 : 4.', ['25 : 1', '50 : 2', '1 : 40']),
    ('In a class, the ratio of boys to girls is 2 : 3. What fraction of the class are girls?', '3/5', '3 out of every 5 students.', ['2/3', '3/2', '2/5']),
])
r1.fixed('C2', (2, 3), [
    ('Explain why 30 minutes : 2 hours is not equal to 30 : 2.', 'The units must be the same before simplifying: 2 hours = 120 minutes, so the ratio is 30 : 120 = 1 : 4.', 'B1 same units; B1 1 : 4 [2]'),
    ('Explain why sharing $60 in the ratio 1 : 2 does not give $30 and $60.', 'There are 1 + 2 = 3 parts, so each part is $20 and the shares are $20 and $40, which add up to $60.', 'B1 total parts 3; B1 shares $20 and $40 [2]'),
    ('Explain how a ratio a : b can be used to write each part as a fraction of the whole.', 'The whole has a + b parts, so the first is a/(a + b) and the second is b/(a + b).', 'B1 total parts; B1 fractions [2]'),
])


@r1.add('C1', (1, 2, 3))
def r1_simp(r, D):
    a, b = r.randint(1, 9), r.randint(1, 9)
    while math.gcd(a, b) != 1 or a == b:
        a, b = r.randint(1, 9), r.randint(2, 11)
    k = r.choice([2, 3, 4, 5, 6, 8, 12, 15])
    c = rstr(a, b)
    if D >= 3:
        u1, u2, f = r.choice([('cm', 'm', 100), ('g', 'kg', 1000), ('minutes', 'hours', 60), ('ml', 'litres', 1000)])
        A, B = a * k, b * k
        if (B % f == 0) and B // f > 0:
            return SMC(r, f'Write {A} {u1} : {B // f} {u2} in its simplest form.', c, [rstr(b, a), rstr(A, B // f), rstr(*simp(A, B // f)), rstr(a * 2, b * 3), rstr(a + 1, b)], f'Convert to {u1}: {A} : {B}, then divide by {k}.')
    return SMC(r, f'Write {a * k} : {b * k} in its simplest form.', c, [rstr(b, a), rstr(a * 2, b * 2), rstr(a + 1, b + 1), rstr(a * k // math.gcd(k, 2), b * k // math.gcd(k, 2)) if k > 2 else rstr(a, b + 1), rstr(a, b + 2)],
               f'HCF of {a * k} and {b * k} is {k}; {c}.')


@r1.add('C2', (2, 3, 4), 'explain')
def r1_err(r, D):
    a, b = r.choice([(2, 3), (3, 5), (4, 5), (5, 7), (2, 7), (3, 4)])
    T = (a + b) * r.choice([6, 8, 12, 15, 20, 25])
    nm = person(r)
    p = T // (a + b)
    return Q(f'{nm} shares ${T} between two friends in the ratio {a} : {b}. {nm} gives them ${T // a if T % a == 0 else round(T / a, 2)} and ${T // b if T % b == 0 else round(T / b, 2)} by dividing ${T} by {a} and by {b}. Explain the error and find the correct shares.',
             f'There are {a} + {b} = {a + b} parts, so one part is ${p}; the shares are ${a * p} and ${b * p}.', f'B1 total of {a + b} parts; B1 ${a * p} and ${b * p} [2]')


@r1.add('C3', (1, 2, 3, 4, 5))
def r1_share(r, D):
    nm1, nm2 = two_people(r)
    if D <= 2:
        a, b = r.choice([(2, 3), (3, 5), (1, 4), (5, 3), (7, 2), (4, 9)])
        T = (a + b) * r.choice([5, 6, 8, 12, 15, 25, 40])
        p = T // (a + b)
        if D == 1:
            return MC(r, f'{nm1} and {nm2} share ${T} in the ratio {a} : {b}. How much does {nm1} receive?', a * p, [b * p, T // a, p, T - p, T - b * p + p, (a + 1) * p, T // (a + b + 1)], f'{a + b} parts; 1 part = ${p}; {a} parts = ${a * p}.', fmtf=lambda x: f'${num(x)}')
        return Q(f'{nm1} and {nm2} share ${T} in the ratio {a} : {b}. Calculate how much each receives.', f'{nm1} ${a * p}, {nm2} ${b * p}', f'M1 ${T} ÷ {a + b} = ${p}; A1 both.')
    if D == 3:
        a, b, c = r.choice([(2, 3, 5), (1, 2, 4), (3, 4, 5), (2, 5, 6), (1, 3, 6)])
        T = (a + b + c) * r.choice([4, 6, 10, 12, 15])
        p = T // (a + b + c)
        nm3 = r.choice([p for p in ('Sam', 'Lina', 'Omar', 'Ines', 'Kwame') if p not in (nm1, nm2)])
        return Q(f'A prize of ${T} is shared between {nm1}, {nm2} and {nm3} in the ratio {a} : {b} : {c}. Calculate the largest share.', f'${max(a, b, c) * p}', f'M1 ÷ {a + b + c}; A1 ${max(a, b, c) * p}.')
    a, b = r.choice([(3, 5), (2, 7), (4, 7), (5, 8), (3, 11)])
    p = r.choice([6, 9, 12, 15, 24])
    kind = r.choice(['diff', 'one'])
    if kind == 'diff':
        return Q(f'Money is shared between {nm1} and {nm2} in the ratio {a} : {b}. {nm2} receives ${(b - a) * p} more than {nm1}. Calculate the total amount shared.', f'${(a + b) * p}',
                 f'M1 {b - a} parts = ${(b - a) * p}; M1 1 part = ${p}; A1 total ${(a + b) * p}.')
    return Q(f'The ratio of {r.choice(["red to blue counters", "adults to children at a concert", "flour to sugar in a recipe"])} is {a} : {b}. There are {a * p} of the first. Calculate the total and write the ratio in the form 1 : n.',
             f'Total {(a + b) * p}; 1 : {ex(round(b / a, 3))}', f'M1 1 part = {p}; A1 total {(a + b) * p}; B1 1 : {ex(round(b / a, 3))}.')


def r1_c4(r, D):
    a, b, c = r.choice([(1, 2, 4), (1, 3, 5), (2, 3, 5), (1, 2, 3)])
    M = (a + b + c) * r.choice([20, 25, 40, 50, 60])
    p = M // (a + b + c)
    add = r.choice([10, 20, 30])
    nm = person(r)
    intro = f'{nm} is mixing concrete for a building site in {city(r)}. Cement, sand and gravel are mixed in the ratio {a} : {b} : {c} by mass. {nm} makes {M} kg of concrete.'
    newr = simp(a * p, b * p + add, c * p)
    parts = [
        P('Calculate the mass of each ingredient.', f'cement {a * p} kg, sand {b * p} kg, gravel {c * p} kg', f'M1 {M} ÷ {a + b + c} = {p}; A2 all three', 3),
        P('What fraction of the concrete is gravel?', frac(Fr(c, a + b + c)), 'B1', 1),
        P(f'{nm} adds another {add} kg of sand. Find the new ratio of cement : sand : gravel in its simplest form.', rstr(*newr), f'M1 {a * p} : {b * p + add} : {c * p}; A1 simplified', 2),
        P(f'Cement costs $0.18 per kg, sand $0.05 per kg and gravel $0.04 per kg. Calculate the cost of the original {M} kg.', f'${a * p * 0.18 + b * p * 0.05 + c * p * 0.04:.2f}', 'M1 each cost; A1 total', 2),
        P('Write the ratio of cement to gravel in the form 1 : n.', f'1 : {ex(round(c / a, 3))}', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


r1.add('C4', (2, 3, 4, 5))(r1_c4)

# ---------------------------------------------------------------- rates and compound measures
r2 = topic('Rates and compound measures', 'rates and compound measures', 'speed, density and pressure', 'compound measures')
r2.fixed('C1', (1, 2), [
    ('Which formula gives density?', 'mass ÷ volume', 'Density = mass/volume, e.g. g/cm³.', ['volume ÷ mass', 'mass × volume', 'force ÷ area']),
    ('Which formula gives pressure?', 'force ÷ area', 'Pressure = force/area, e.g. N/m².', ['area ÷ force', 'force × area', 'mass ÷ area']),
    ('Convert 72 km/h to m/s.', '20 m/s', '72 000 m ÷ 3600 s = 20 m/s.', ['72 m/s', '1.2 m/s', '259.2 m/s']),
    ('A car travels 150 km in 2.5 hours. What is its average speed?', '60 km/h', '150 ÷ 2.5 = 60.', ['375 km/h', '37.5 km/h', '65 km/h']),
    ('A block has mass 240 g and volume 30 cm³. What is its density?', '8 g/cm³', '240 ÷ 30 = 8.', ['7200 g/cm³', '0.125 g/cm³', '210 g/cm³']),
    ('Which unit is a unit of pressure?', 'N/m²', 'Newtons per square metre (pascals).', ['kg/m³', 'm/s', 'N m']),
])
r2.fixed('C2', (2, 3), [
    ('A cyclist rides 20 km at 10 km/h and then 20 km at 20 km/h. Explain why the average speed is not 15 km/h.', 'More time is spent at the slower speed (2 h vs 1 h). Average speed = total distance ÷ total time = 40 ÷ 3 = 13.3 km/h.', 'B1 times differ; B1 40 ÷ 3 = 13.3 km/h [2]'),
    ('Explain how to convert a speed in m/s to km/h.', 'Multiply by 3600 to get metres per hour, then divide by 1000 to get km per hour (overall × 3.6).', 'B1 × 3600; B1 ÷ 1000 (× 3.6) [2]'),
    ('Explain why a person standing on one foot exerts a greater pressure on the floor than when standing on two feet.', 'The force (weight) is the same but the area in contact is halved, so pressure = force ÷ area doubles.', 'B1 same force; B1 smaller area so larger pressure [2]'),
])


@r2.add('C1', (1, 2, 3))
def r2_q(r, D):
    kind = r.choice(['speed', 'dens', 'press', 'conv'])
    if kind == 'speed':
        s, t = r.choice([40, 48, 60, 75, 80, 90, 120]), r.choice([1.5, 2, 2.5, 3, 4])
        return MC(r, f'A coach travels {ex(s * t)} km in {ex(t)} hours. What is its average speed?', s, [s * t * t, t / (s * t), s + 10, s * t / (t + 1)], f'{ex(s * t)} ÷ {ex(t)} = {s} km/h.', unit=' km/h', fmtf=lambda x: n3(x))
    if kind == 'dens':
        d, v = r.choice([0.8, 2.5, 2.7, 7.8, 8.9, 11.3, 19.3]), r.choice([10, 20, 25, 40, 50])
        return MC(r, f'A metal block has a volume of {v} cm³ and a mass of {ex(d * v)} g. What is its density?', d, [d * v * v, 1 / d, d * 10, d + v], f'{ex(d * v)} ÷ {v} = {ex(d)} g/cm³.', unit=' g/cm³', fmtf=lambda x: n3(x))
    if kind == 'press':
        F, A = r.choice([120, 200, 450, 600, 900]), r.choice([0.5, 2, 3, 4, 5])
        return MC(r, f'A force of {F} N acts on an area of {ex(A)} m². What is the pressure?', F / A, [F * A, A / F, F - A, F / (A * 10)], f'{F} ÷ {ex(A)} = {ex(round(F / A, 3))} N/m².', unit=' N/m²', fmtf=lambda x: n3(x))
    v = r.choice([36, 54, 72, 90, 108, 126, 144])
    return MC(r, f'Convert {v} km/h to m/s.', v / 3.6, [v * 3.6, v / 60, v * 1000 / 60, v / 36], f'{v} × 1000 ÷ 3600 = {ex(v / 3.6)} m/s.', unit=' m/s', fmtf=lambda x: n3(x))


@r2.add('C2', (2, 3, 4), 'explain')
def r2_err(r, D):
    nm = person(r)
    d = r.choice([30, 40, 60, 90, 120])
    s1, s2 = r.choice([(30, 60), (40, 60), (20, 30), (45, 90), (50, 75), (60, 90)])
    t = d / s1 + d / s2
    av = 2 * d / t
    return Q(f'{nm} drives {d} km at {s1} km/h and then another {d} km at {s2} km/h. {nm} says the average speed for the whole journey is ({s1} + {s2}) ÷ 2 = {ex((s1 + s2) / 2)} km/h. Explain the error and calculate the correct average speed.',
             f'Average speed = total distance ÷ total time; more time is spent at the lower speed. Time = {ex(round(d / s1, 3))} + {ex(round(d / s2, 3))} = {ex(round(t, 3))} h, so average speed = {2 * d} ÷ {ex(round(t, 3))} = {n3(av)} km/h.',
             f'B1 must use total distance ÷ total time; M1 times; A1 {n3(av)} km/h [3]', marks=3)


@r2.add('C3', (1, 2, 3, 4, 5))
def r2_calc(r, D):
    kind = r.choice(['sdt', 'dens', 'press', 'conv'])
    if kind == 'sdt':
        s = r.choice([12, 15, 18, 48, 64, 72, 85, 96, 110])
        mins = r.choice([25, 40, 45, 50, 75, 84, 96, 105, 135])
        d = s * mins / 60
        what = r.choice(['A cyclist', 'A ferry', 'A train', 'A coach', 'A delivery van'])
        q = r.choice(['d', 't', 's'])
        if q == 'd':
            return Q(f'{what} travels at an average speed of {s} km/h for {mins} minutes. Calculate the distance travelled.', f'{ex(round(d, 2))} km', f'M1 {mins} min = {ex(round(mins / 60, 4))} h; M1 {s} × {ex(round(mins / 60, 4))}; A1 {ex(round(d, 2))} km.')
        if q == 't':
            return Q(f'{what} travels {ex(round(d, 2))} km at an average speed of {s} km/h. Calculate the time taken, in hours and minutes.', dur(mins), f'M1 {ex(round(d, 2))} ÷ {s} = {ex(round(mins / 60, 4))} h; A1 {dur(mins)}.')
        return Q(f'{what} travels {ex(round(d, 2))} km in {dur(mins)}. Calculate its average speed in km/h.', f'{s} km/h', f'M1 time = {ex(round(mins / 60, 4))} h; M1 distance ÷ time; A1 {s} km/h.')
    if kind == 'dens':
        l, w, h = r.choice([2, 3, 4, 5, 8]), r.choice([2, 2.5, 3, 4, 6]), r.choice([1.5, 2, 3, 5])
        d = r.choice([0.9, 2.7, 7.9, 8.5, 10.5, 11.3])
        V = l * w * h
        m = d * V
        if D >= 4:
            return Q(f'A cuboid of {r.choice(["metal", "alloy", "stone", "plastic"])} measures {l} cm by {ex(w)} cm by {ex(h)} cm and has density {ex(d)} g/cm³. Calculate its mass in kilograms.', f'{ex(round(m / 1000, 4))} kg',
                     f'M1 V = {ex(V)} cm³; M1 m = {ex(d)} × {ex(V)} = {ex(round(m, 3))} g; A1 {ex(round(m / 1000, 4))} kg.')
        return Q(f'A cuboid measures {l} cm by {ex(w)} cm by {ex(h)} cm and has a mass of {ex(round(m, 3))} g. Calculate its density.', f'{ex(d)} g/cm³', f'M1 V = {ex(V)}; M1 {ex(round(m, 3))} ÷ {ex(V)}; A1 {ex(d)} g/cm³.')
    if kind == 'press':
        F = r.choice([240, 360, 480, 600, 750, 1200])
        a, b = r.choice([(20, 30), (40, 50), (25, 40), (10, 60), (50, 80)])
        A = a * b / 10000
        return Q(f'A box with a weight of {F} N rests on a rectangular face measuring {a} cm by {b} cm. Calculate the pressure on the floor in N/m².', f'{n3(F / A)} N/m²',
                 f'M1 area = {a * b} cm² = {ex(A)} m²; M1 {F} ÷ {ex(A)}; A1 {n3(F / A)} N/m².')
    if D <= 2:
        v = r.choice([5, 6.5, 7.2, 8, 9.5, 10])
        return Q(f'A sprinter runs at {ex(v)} m/s. Convert this speed to km/h.', f'{ex(v * 3.6)} km/h', f'M1 × 3600 ÷ 1000; A1 {ex(v * 3.6)} km/h.')
    v = r.choice([5, 12.5, 15, 25, 30, 40])
    return Q(f'Water flows from a pipe at {ex(v)} litres per minute. Calculate how many cubic metres flow out in 1 day.', f'{ex(v * 60 * 24 / 1000)} m³',
             f'M1 {ex(v)} × 60 × 24 = {ex(v * 60 * 24)} litres; M1 ÷ 1000; A1 {ex(v * 60 * 24 / 1000)} m³.')


def r2_c4(r, D):
    kind = r.choice(['journey', 'block'])
    nm = person(r)
    if kind == 'journey':
        d1, s1 = r.choice([(45, 90), (60, 80), (36, 72), (50, 100), (84, 112)])
        d2, t2 = r.choice([(30, 40), (25, 30), (42, 35), (54, 45)])
        stop = r.choice([10, 15, 20, 25])
        t1 = d1 / s1 * 60
        tot = t1 + t2 + stop
        av = (d1 + d2) / (tot / 60)
        intro = f'{nm} drives from {city(r)} to a nearby town. The first {d1} km are on a motorway at an average speed of {s1} km/h. {nm} then stops for {stop} minutes and drives the final {d2} km in {t2} minutes.'
        parts = [
            P('Calculate the time taken for the motorway section, in minutes.', f'{ex(t1)} minutes', f'M1 {d1} ÷ {s1} h × 60; A1', 2),
            P('Calculate the average speed for the final section in km/h.', f'{n3(d2 / (t2 / 60))} km/h', f'M1 {d2} ÷ ({t2}/60); A1', 2),
            P('Calculate the average speed for the whole journey, including the stop.', f'{n3(av)} km/h', f'M1 total distance {d1 + d2}; M1 total time {ex(tot)} min; A1 {n3(av)} km/h', 3),
            P('Convert the motorway speed to m/s.', f'{n3(s1 / 3.6)} m/s', 'M1 ÷ 3.6; A1', 2),
        ]
        return cmp_(r, intro, parts)
    l, w, h = r.choice([(10, 5, 4), (20, 10, 5), (12, 8, 3), (15, 6, 4)])
    d = r.choice([2.5, 7.8, 8.9, 11.3])
    m = l * w * h * d
    W = m / 1000 * 10
    areas = sorted([l * w, l * h, w * h])
    intro = f'A cuboid block of metal measuring {l} cm by {w} cm by {h} cm has density {ex(d)} g/cm³. Take the weight of 1 kg to be 10 N.'
    parts = [
        P('Calculate the mass of the block in kg.', f'{ex(round(m / 1000, 4))} kg', f'M1 V = {l * w * h} cm³; M1 × {ex(d)}; A1', 3),
        P('Calculate the weight of the block in newtons.', f'{ex(round(W, 3))} N', 'B1', 1),
        P('Calculate the greatest pressure the block can exert on a table, in N/m².', f'{n3(W / (areas[0] / 10000))} N/m²', f'M1 smallest face {areas[0]} cm² = {ex(areas[0] / 10000)} m²; M1 W ÷ area; A1', 3),
        P('Explain why the pressure depends on which face is in contact with the table.', 'The weight is the same but the contact area changes; smaller area gives greater pressure.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


r2.add('C4', (2, 3, 4, 5))(r2_c4)

# ---------------------------------------------------------------- direct and inverse proportion
VARY = [(1, 'x'), (2, 'x²'), (3, 'x³'), (Fr(1, 2), '√x')]

r3 = topic('Direct and inverse proportion', 'direct and inverse proportion', 'forming equations y = kx^n', 'proportion variation')
r3.fixed('C1', (1, 2), [
    ('y is directly proportional to x². Which equation is correct?', 'y = kx²', 'Direct proportion to x²: y = k × x².', ['y = k/x²', 'y = x² + k', 'y = kx']),
    ('y is inversely proportional to x. Which equation is correct?', 'y = k/x', 'Inverse proportion: y × x = constant.', ['y = kx', 'y = x/k', 'y = k − x']),
    ('y is directly proportional to x. When x = 4, y = 12. What is y when x = 10?', '30', 'k = 3, so y = 3 × 10.', ['18', '40', '120']),
    ('y is inversely proportional to x. If x is doubled, what happens to y?', 'It is halved', 'xy is constant, so y must halve.', ['It is doubled', 'It is quartered', 'It stays the same']),
    ('y is directly proportional to x². If x is multiplied by 3, y is multiplied by', '9', '3² = 9.', ['3', '6', '27']),
])
r3.fixed('C2', (2, 3), [
    ('Explain how you can tell from a table of values that y is inversely proportional to x.', 'The product xy is the same for every pair of values, so y = k/x.', 'B1 product constant; B1 conclusion [2]'),
    ('Explain why the graph of y against x for direct proportion is a straight line through the origin.', 'y = kx is a linear equation with gradient k and y-intercept 0.', 'B1 linear form; B1 intercept 0 [2]'),
    ('The time to build a wall is inversely proportional to the number of workers. Explain what happens to the time when the number of workers is tripled.', 'The time is divided by 3, because the time × number of workers stays constant.', 'B1 divided by 3; B1 reason [2]'),
])


@r3.add('C2', (2, 3, 4), 'explain')
def r3_fac(r, D):
    n, vs = r.choice(VARY)
    inv = r.random() < 0.5
    k, word = r.choice([(2, 'doubled'), (3, 'multiplied by 3'), (4, 'multiplied by 4'), (0.5, 'halved')])
    if vs == '√x':
        k, word = r.choice([(4, 'multiplied by 4'), (9, 'multiplied by 9'), (0.25, 'divided by 4')])
    f = k ** float(n)
    if inv:
        f = 1 / f
    f = Fr(f).limit_denominator(1000)
    rel = f'inversely proportional to {vs}' if inv else f'directly proportional to {vs}'
    return Q(f'y is {rel}. Explain what happens to y when x is {word}.', f'y is multiplied by {frac(f)}.',
             f'B1 y = k/{vs}' if inv else f'B1 y = k{vs}' + f'; B1 factor {frac(f)} [2]')


@r3.add('C3', (1, 2, 3, 4, 5))
def r3_calc(r, D):
    n, vs = r.choice(VARY[:2] if D <= 2 else VARY)
    inv = r.random() < 0.5 if D >= 2 else False
    x1 = r.choice([2, 3, 4, 5, 6]) if vs != '√x' else r.choice([4, 9, 16, 25])
    k = r.choice([2, 3, 4, 5, 0.5, 1.5, 12, 20, 36])
    xv = Fr(x1) ** int(n) if vs != '√x' else Fr(math.isqrt(x1))
    y1 = k / xv if inv else k * xv
    x2 = r.choice([3, 6, 8, 10]) if vs != '√x' else r.choice([36, 49, 64, 100])
    if x2 == x1:
        x2 += 1 if vs != '√x' else 0
    xv2 = Fr(x2) ** int(n) if vs != '√x' else Fr(math.isqrt(x2)) if math.isqrt(x2) ** 2 == x2 else math.sqrt(x2)
    y2 = k / xv2 if inv else k * xv2
    eq = f'y = {ex(k)}/{vs}' if inv else f'y = {ex(k)}{vs}'
    rel = f'inversely proportional to {"the square of x" if vs == "x²" else ("the cube of x" if vs == "x³" else ("the square root of x" if vs == "√x" else "x"))}' if inv else f'directly proportional to {"the square of x" if vs == "x²" else ("the cube of x" if vs == "x³" else ("the square root of x" if vs == "√x" else "x"))}'
    y1s = ex(round(float(y1), 4))
    if D == 1:
        return MC(r, f'y is {rel}. When x = {x1}, y = {y1s}. Find y when x = {x2}.', float(y2), [float(y1) * x2 / x1 + 1, float(y1) + x2 - x1, float(y1) * x1 / x2, float(y2) * 2], f'k = {ex(k)}; {eq}; y = {ex(round(float(y2), 4))}.', fmtf=lambda v: ex(round(v, 3)))
    if D >= 4 and r.random() < 0.5:
        ty = r.choice([2, 3, 4]) * k * (1 if inv else 1)
        # solve for x
        if inv:
            xx = (k / ty) ** (1 / float(n))
        else:
            xx = (ty / k) ** (1 / float(n))
        return Q(f'y is {rel}. When x = {x1}, y = {y1s}. (a) Find a formula for y in terms of x. (b) Find x when y = {ex(ty)}.', f'(a) {eq} (b) x = {n3(xx)}',
                 f'(a) M1 y = k{"/" if inv else ""}{vs}; A1 k = {ex(k)} (b) M1 rearrange; A1 {n3(xx)}.', type='multi_step', marks=4)
    return Q(f'y is {rel}. When x = {x1}, y = {y1s}. Find a formula for y in terms of x and calculate y when x = {x2}.', f'{eq}; y = {n3(float(y2))}',
             f'M1 y = k{"/" if inv else ""}{vs}; A1 k = {ex(k)}; A1 y = {n3(float(y2))}.')


PCTX = [
    ('The stopping distance d metres of a car is directly proportional to the square of its speed v km/h.', 2, False, 'v', 'd', (50, 30.0), [40, 60, 70, 90], 'km/h', 'm'),
    ('The intensity I of light from a lamp is inversely proportional to the square of the distance d metres from it.', 2, True, 'd', 'I', (2, 45.0), [1, 3, 4, 5, 6], 'm', 'units'),
    ('The time t hours to pick a field of tea is inversely proportional to the number of workers n.', 1, True, 'n', 't', (12, 10.0), [8, 15, 20, 24, 30], 'workers', 'hours'),
    ('The mass m grams of a metal ball is directly proportional to the cube of its radius r cm.', 3, False, 'r', 'm', (2, 268.0), [1, 3, 4, 5], 'cm', 'g'),
    ('The period T seconds of a pendulum is directly proportional to the square root of its length L metres.', Fr(1, 2), False, 'L', 'T', (1, 2.0), [0.25, 2.25, 4, 9], 'm', 's'),
]


def r3_c4(r, D):
    txt, n, inv, xv, yv, (x1, y1), x2s, xu, yu = r.choice(PCTX)
    nf = float(n)
    k = y1 * x1 ** nf if inv else y1 / x1 ** nf
    x2 = r.choice(x2s)
    y2 = k / x2 ** nf if inv else k * x2 ** nf
    ty = round(y1 * r.choice([0.5, 2, 1.5, 4]), 2)
    xt = (k / ty) ** (1 / nf) if inv else (ty / k) ** (1 / nf)
    pw = {1: '', 2: '²', 3: '³'}.get(n, '') if n != Fr(1, 2) else ''
    xs = f'√{xv}' if n == Fr(1, 2) else f'{xv}{pw}'
    ks = ex(round(k, 3)) if abs(k - round(k, 3)) < 1e-9 else n3(k)
    eq = f'{yv} = {ks}/{xs}' if inv else f'{yv} = {ks}{xs}'
    fac = 2
    eff = fac ** nf
    intro = f'{txt} When {xv} = {num(x1)}, {yv} = {ex(y1)}.'
    parts = [
        P(f'Find a formula for {yv} in terms of {xv}.', eq, f'M1 {yv} = k{"/" if inv else ""}{xs}; A1 k = {ks}', 2),
        P(f'Find {yv} when {xv} = {num(x2)}.', f'{n3(y2)} {yu}', 'M1 substitute; A1', 2),
        P(f'Find {xv} when {yv} = {ex(ty)}.', f'{n3(xt)} {xu}', 'M1 rearrange; A1', 2),
        P(f'Describe the effect on {yv} when {xv} is doubled.', f'{yv} is {"divided" if inv else "multiplied"} by ' + ('√2 ≈ 1.41' if n == Fr(1, 2) else ex(eff)) + '.', 'B1 multiplied/divided; B1 factor', 2),
    ]
    return cmp_(r, intro, parts)


r3.add('C4', (2, 3, 4, 5))(r3_c4)

# ---------------------------------------------------------------- increase/decrease in ratio, best buys
r4 = topic('Increasing and decreasing by a ratio; best buys', 'increasing and decreasing amounts by a given ratio', 'best buys', 'best buy value for money')
r4.fixed('C1', (1, 2), [
    ('Increase 40 in the ratio 5 : 4.', '50', '40 × 5/4 = 50.', ['32', '45', '200']),
    ('Decrease 36 in the ratio 2 : 3.', '24', '36 × 2/3 = 24.', ['54', '12', '33']),
    ('A 500 g pack costs $2.40 and a 1 kg pack costs $4.50. Which is the better buy?', 'The 1 kg pack', '500 g: $0.48 per 100 g; 1 kg: $0.45 per 100 g.', ['The 500 g pack', 'They are the same value', 'It cannot be decided']),
    ('A recipe for 4 people uses 300 g of rice. How much rice is needed for 10 people?', '750 g', '300 ÷ 4 × 10 = 750.', ['1200 g', '600 g', '3000 g']),
])
r4.fixed('C2', (2, 3), [
    ('Explain how to decide which of two different-sized packs is the better buy.', 'Work out the cost per unit (or the amount per unit of money) for each pack and compare; the lower cost per unit is the better buy.', 'B1 compare same unit; B1 lowest cost per unit [2]'),
    ('Explain why "increase in the ratio 3 : 2" multiplies an amount by 1.5.', 'The new amount : old amount = 3 : 2, so new = old × 3/2 = old × 1.5.', 'B1 new : old; B1 × 3/2 [2]'),
    ('Give one reason why the larger pack is not always the best choice even when it is cheaper per gram.', 'The buyer may not use it all before it expires, or may not be able to afford or store it.', 'B1 valid reason; B1 linked to the buyer [2]'),
])


@r4.add('C1', (1, 2, 3))
def r4_q(r, D):
    a, b = r.choice([(5, 4), (3, 2), (7, 5), (2, 3), (3, 5), (4, 5), (5, 2)])
    x = b * r.choice([4, 6, 8, 10, 12, 15, 20])
    v = x * a // b
    word = 'Increase' if a > b else 'Decrease'
    return MC(r, f'{word} {x} in the ratio {a} : {b}.', v, [x * b / a, x + a - b, x * a, x / b], f'{x} × {a}/{b} = {v}.', fmtf=lambda v_: ex(round(v_, 2)))


@r4.add('C2', (2, 3, 4), 'explain')
def r4_err(r, D):
    nm = person(r)
    g1, p1 = r.choice([(250, 1.8), (400, 2.6), (500, 3.2), (750, 4.4)])
    g2, p2 = r.choice([(1000, 5.4), (1200, 7.8), (2000, 11.5), (1500, 8.1)])
    u1, u2 = p1 / g1 * 100, p2 / g2 * 100
    best = f'{g1} g' if u1 < u2 else f'{g2} g'
    return Q(f'A small bag of {g1} g of coffee costs ${p1:.2f} and a large bag of {g2} g costs ${p2:.2f}. {nm} says the small bag is better value because it is cheaper. Explain whether {nm} is correct.',
             f'Compare cost per 100 g: small ${u1:.3f}, large ${u2:.3f}. The {best} bag is better value' + (f', so {nm} is correct for the wrong reason.' if best == f'{g1} g' else f', so {nm} is wrong.'),
             'M1 cost per unit for both; A1 comparison; B1 conclusion [3]', marks=3)


@r4.add('C3', (1, 2, 3, 4))
def r4_calc(r, D):
    kind = r.choice(['best', 'recipe', 'ratio'])
    if kind == 'best' or D >= 3:
        packs = r.sample([(330, 0.85), (500, 1.2), (750, 1.75), (1000, 2.25), (1500, 3.3), (2000, 4.2), (250, 0.65)], 3 if D >= 3 else 2)
        unit = [p / s * 1000 for s, p in packs]
        best = packs[unit.index(min(unit))]
        item = r.choice(['orange juice (ml)', 'olive oil (ml)', 'washing liquid (ml)', 'milk (ml)'])
        return Q(f'A supermarket in {city(r)} sells {item.split(" (")[0]} in these sizes: ' + ', '.join(f'{s} ml for ${p:.2f}' for s, p in packs) + '. Showing your working, find which size is the best buy.', f'{best[0]} ml',
                 'M1 cost per litre (or ml per $) for each: ' + ', '.join(f'{s} ml → ${u:.3f}/litre' for (s, _), u in zip(packs, unit)) + f'; A1 {best[0]} ml.')
    if kind == 'recipe':
        n1, n2 = r.choice([(4, 6), (4, 10), (6, 9), (8, 12), (5, 8)])
        g = r.choice([200, 240, 300, 360, 450])
        return Q(f'A recipe for {n1} people uses {g} g of flour. Calculate how much flour is needed for {n2} people.', f'{ex(g * n2 / n1)} g', f'M1 {g} ÷ {n1} × {n2}; A1 {ex(g * n2 / n1)} g.')
    a, b = r.choice([(5, 4), (3, 2), (7, 5), (2, 3), (3, 5)])
    x = b * r.choice([6, 9, 12, 15, 24])
    return Q(f'A photograph is {x} mm wide. It is {"enlarged" if a > b else "reduced"} in the ratio {a} : {b}. Calculate the new width.', f'{x * a // b} mm', f'M1 {x} × {a}/{b}; A1 {x * a // b} mm.')


def r4_c4(r, D):
    nm = person(r)
    item = r.choice(['rice', 'washing powder', 'pasta', 'dog food'])
    s1, p1 = r.choice([(2, 3.5), (2.5, 4.2), (1.5, 2.7)])
    s2, p2 = r.choice([(5, 8.25), (6, 9.6), (4, 6.9)])
    off = r.choice([20, 25, 15])
    p2o = p2 * (1 - off / 100)
    u1, u2, u2o = p1 / s1, p2 / s2, p2o / s2
    N = 2 * s1 + 2 * s2
    best = None
    for a in range(0, 30):
        for b in range(0, 10):
            if abs(a * s1 + b * s2 - N) < 1e-9:
                cst = a * p1 + b * p2o
                if best is None or cst < best[0] - 1e-9:
                    best = (cst, a, b)
    cst, ba, bb = best
    buy = ' and '.join(x for x in [f'{ba} bag{"s" if ba != 1 else ""} of {ex(s1)} kg' if ba else '', f'{bb} bag{"s" if bb != 1 else ""} of {s2} kg' if bb else ''] if x)
    intro = f'A shop in {city(r)} sells {item} in a {ex(s1)} kg bag for ${p1:.2f} and a {s2} kg bag for ${p2:.2f}.'
    parts = [
        P('Calculate the cost per kilogram of each bag.', f'${u1:.3f} and ${u2:.3f}', 'M1 price ÷ mass; A1 both', 2),
        P('State which bag is the better buy.', f'The {ex(s1) if u1 < u2 else s2} kg bag', 'B1 ft', 1),
        P(f'The large bag is reduced by {off}%. Calculate its new price and its new cost per kilogram.', f'${p2o:.2f}; ${u2o:.3f} per kg', f'M1 × {ex(1 - off / 100)}; A1; A1', 3),
        P(f'After the reduction, {nm} needs exactly {ex(N)} kg. Find the cheapest combination of bags and its cost.', f'{buy}, costing ${cst:.2f}', 'M1 considers combinations totalling the mass; A1', 2),
    ]
    return cmp_(r, intro, parts)


r4.add('C4', (2, 3, 4, 5))(r4_c4)
CHAPTERS[9] = [r1, r2, r3, r4]


# =========================================================== 10 More equations, formulae and functions (Ch 22)
q1 = topic('Constructing and solving equations from contexts', 'constructing and solving equations from contexts', 'forming equations', 'equations contexts')
q1.fixed('C1', (1, 2), [
    ('The sum of three consecutive integers is 48. If the smallest is n, which equation is correct?', '3n + 3 = 48', 'n + (n + 1) + (n + 2) = 3n + 3.', ['3n = 48', 'n + 3 = 48', '3n + 6 = 48']),
    ('A rectangle has length 2x cm and width x cm. Its perimeter is 36 cm. What is x?', '6', '2(2x + x) = 6x = 36.', ['9', '12', '18']),
    ('Make r the subject of C = 2πr.', 'r = C/(2π)', 'Divide both sides by 2π.', ['r = 2πC', 'r = C − 2π', 'r = 2C/π']),
    ('The angles of a triangle are x°, 2x° and 3x°. What is x?', '30', '6x = 180.', ['60', '36', '20']),
    ('Make x the subject of y = mx + c.', 'x = (y − c)/m', 'Subtract c, then divide by m.', ['x = y/m − c', 'x = (y + c)/m', 'x = m(y − c)']),
])
q1.fixed('C2', (2, 3), [
    ('Explain why a solution to an equation formed from a real context should be checked against the context.', 'The algebra may give values that are impossible in reality, such as a negative length or a non-whole number of people.', 'B1 context may restrict values; B1 example [2]'),
    ('A student writes "3 more than twice a number is 17" as 2(n + 3) = 17. Explain the error.', '"Twice a number, plus 3" is 2n + 3 = 17; the bracket would mean adding 3 first and then doubling.', 'B1 order of operations; B1 2n + 3 = 17 [2]'),
    ('Explain the steps needed to make h the subject of V = ⅓πr²h.', 'Multiply both sides by 3 (3V = πr²h), then divide by πr² to get h = 3V/(πr²).', 'B1 × 3; B1 ÷ πr² [2]'),
])


@q1.add('C1', (1, 2, 3))
def q1_q(r, D):
    a, b = r.randint(2, 6), r.randint(1, 12)
    x = r.randint(2, 15)
    tot = a * x + b
    nm = person(r)
    return MC(r, f'{nm} thinks of a number, multiplies it by {a} and adds {b}. The answer is {tot}. What was the number?', x, [tot // a, (tot + b) / a, x + 1, tot - b, x - 1, x + 2, tot / a], f'{a}n + {b} = {tot}, so n = {x}.', fmtf=lambda v: ex(round(v, 2)))


@q1.add('C2', (2, 3, 4), 'explain')
def q1_err(r, D):
    nm = person(r)
    a, b, c = r.randint(2, 5), r.randint(2, 9), r.randint(2, 6)
    x = r.randint(2, 9)
    rhs = c * (a * x + b)
    return Q(f'{nm} solves {c}({lin(a, b)}) = {rhs}. {nm} writes {lin(c * a, b)} = {rhs}, so x = {frac(Fr(rhs - b, c * a))}. Explain the error and find the correct value of x.',
             f'The {b} inside the bracket must also be multiplied by {c}: {lin(c * a, c * b)} = {rhs}, so x = {x}.', f'B1 expands bracket fully; M1 {c * a}x = {rhs - c * b}; A1 x = {x} [3]', marks=3)


@q1.add('C3', (1, 2, 3, 4, 5))
def q1_ctx(r, D):
    kind = r.choice(['tri', 'rect', 'consec', 'age', 'quad'])
    if kind == 'tri':
        a, b = r.randint(2, 4), r.randint(5, 30)
        x = r.randint(12, 30)
        c = 180 - (x + b) - a * x
        if c <= 10:
            return None
        return Q(f'The angles of a triangle are (x + {b})°, {a}x° and {c}°. Form an equation and solve it to find x. Hence find the largest angle.', f'x = {x}; largest angle {max(x + b, a * x, c)}°',
                 f'M1 x + {b} + {a}x + {c} = 180; M1 {a + 1}x = {180 - b - c}; A1 x = {x}; A1 {max(x + b, a * x, c)}°.')
    if kind == 'rect':
        a, b, c = r.randint(2, 4), r.randint(1, 8), r.randint(1, 6)
        x = r.randint(3, 12)
        P_ = 2 * (a * x + b + x - c) if x > c else None
        if not P_:
            return None
        return Q(f'A rectangle has length ({lin(a, b)}) cm and width ({lin(1, -c)}) cm. Its perimeter is {P_} cm. Find x and the area of the rectangle.', f'x = {x}; area {(a * x + b) * (x - c)} cm²',
                 f'M1 2({lin(a, b)} + {lin(1, -c)}) = {P_}; M1 {2 * (a + 1)}x = {P_ - 2 * (b - c)}; A1 x = {x}; A1 area {(a * x + b) * (x - c)} cm².')
    if kind == 'consec':
        k = r.choice([3, 4, 5])
        n = r.randint(5, 60)
        ev_ = r.random() < 0.5 and D >= 3
        step = 2 if ev_ else 1
        tot = sum(n * step + i * step for i in range(k)) if ev_ else sum(n + i for i in range(k))
        first = n * step if ev_ else n
        return Q(f'The sum of {k} consecutive {"even " if ev_ else ""}integers is {tot}. Form and solve an equation to find the smallest of them.', f'{first}',
                 f'M1 n + (n + {step}) + … = {tot}; M1 {k}n + {sum(i * step for i in range(k))} = {tot}; A1 n = {first}.')
    if kind == 'age':
        nm1, nm2 = two_people(r)
        a = r.randint(8, 16)
        k = r.choice([2, 3, 4])
        y = r.randint(2, 8)
        # parent = k*a now? in y years parent = m*(a+y)
        p = k * a
        m = Fr(p + y, a + y)
        if m.denominator != 1:
            return Q(f'{nm1} is {k} times as old as {nm2}. The sum of their ages is {p + a}. Form and solve an equation to find {nm2}\'s age.', f'{a}', f'M1 {k}x + x = {p + a}; A1 x = {a}.')
        return Q(f'{nm1} is {k} times as old as {nm2}. In {y} years\' time {nm1} will be {int(m)} times as old as {nm2}. Form and solve an equation to find their ages now.', f'{nm2} {a}, {nm1} {p}',
                 f'M1 {k}x + {y} = {int(m)}(x + {y}); M1 {k - int(m)}x = {int(m) * y - y}; A1 {nm2} {a}; A1 {nm1} {p}.')
    # rearrange formula
    f = r.choice([('v = u + at', 'a', 'a = (v − u)/t'), ('A = ½(a + b)h', 'h', 'h = 2A/(a + b)'), ('s = ut + ½at²', 'u', 'u = (s − ½at²)/t'), ('E = ½mv²', 'v', 'v = √(2E/m)'),
                  ('T = 2π√(L/g)', 'L', 'L = gT²/(4π²)'), ('y = (3x + 2)/(x − 1)', 'x', 'x = (y + 2)/(y − 3)'), ('V = πr²h', 'r', 'r = √(V/(πh))'), ('P = 2(l + w)', 'w', 'w = P/2 − l')])
    return Q(f'Make {f[1]} the subject of the formula {f[0]}.', f[2], 'M1 first correct step (isolate term); M1 second step; A1 correct rearrangement.')


def q1_c4(r, D):
    nm = person(r)
    a, b = r.choice([(12, 0.08), (15, 0.05), (8, 0.12), (20, 0.04)])
    c, d = r.choice([(0, 0.15), (5, 0.10), (3, 0.14)])
    if abs(b - d) < 1e-9:
        d += 0.02
    m = (a - c) / (d - b)
    intro = f'Two mobile phone plans are available in {city(r)}. Plan A costs ${a} per month plus ${b:.2f} per minute of calls. Plan B costs ${c} per month plus ${d:.2f} per minute.'
    mm = r.choice([60, 100, 150, 200])
    parts = [
        P('Write down an expression for the monthly cost of each plan for x minutes of calls.', f'A: {ex(a)} + {ex(b)}x; B: {ex(c)} + {ex(d)}x', 'B1 B1', 2),
        P('Form and solve an equation to find the number of minutes for which both plans cost the same.', f'{n3(m)} minutes', f'M1 {ex(a)} + {ex(b)}x = {ex(c)} + {ex(d)}x; M1 collect; A1 {n3(m)}', 3),
        P(f'{nm} uses about {mm} minutes per month. State which plan is cheaper and by how much.', f'Plan {"A" if a + b * mm < c + d * mm else "B"}, by ${abs((a + b * mm) - (c + d * mm)):.2f}', 'M1 both costs; A1', 2),
        P(f'Explain how knowing the number of minutes for which both plans cost the same (about {n3(m)}) helps a customer choose a plan.', f'Below about {n3(m)} minutes the plan with the lower fixed charge is cheaper; above it the plan with the lower rate per minute is cheaper.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


q1.add('C4', (2, 3, 4, 5))(q1_c4)

# ---------------------------------------------------------------- function notation, domain and range
q2 = topic('Function notation, domain and range', 'function notation', 'domain and range', 'functions')
q2.fixed('C1', (1, 2), [
    ('f(x) = 3x − 2. What is f(4)?', '10', '3 × 4 − 2 = 10.', ['12', '14', '6']),
    ('The domain of a function is', 'the set of input values', 'Domain: inputs (x); range: outputs.', ['the set of output values', 'the largest output', 'the gradient']),
    ('The range of a function is', 'the set of output values', 'Range: all values f(x) can take for the given domain.', ['the set of input values', 'the difference between largest and smallest input', 'the y-intercept']),
    ('Which value must be excluded from the domain of f(x) = 5/(x − 3)?', 'x = 3', 'Division by zero is undefined.', ['x = 5', 'x = −3', 'x = 0']),
    ('f(x) = x² + 1. What is the range of f for all real x?', 'f(x) ≥ 1', 'x² ≥ 0, so x² + 1 ≥ 1.', ['f(x) ≥ 0', 'all real numbers', 'f(x) ≤ 1']),
])
q2.fixed('C2', (2, 3), [
    ('Explain why x = 2 is not in the domain of f(x) = 1/(x − 2).', 'When x = 2 the denominator is zero, and division by zero is undefined.', 'B1 denominator 0; B1 undefined [2]'),
    ('Explain why the function f(x) = √(x − 4) has domain x ≥ 4.', 'The square root of a negative number is not real, so x − 4 must be at least 0.', 'B1 no real root of negative; B1 x − 4 ≥ 0 [2]'),
    ('Explain the difference between f(2x) and 2f(x) for f(x) = x + 3.', 'f(2x) = 2x + 3 (the input is doubled); 2f(x) = 2x + 6 (the output is doubled).', 'B1 f(2x); B1 2f(x) [2]'),
])


@q2.add('C1', (1, 2, 3))
def q2_eval(r, D):
    a, b = r.choice([2, 3, 4, 5, -2, -3]), r.randint(-9, 9)
    x = r.randint(-5, 6)
    if D >= 2 and r.random() < 0.5:
        c = r.randint(-5, 5)
        v = x * x + a * x + c
        return MC(r, f'f(x) = {quad(1, a, c)}. Find f({num(x)}).', v, [-x * x + a * x + c, x * x - a * x + c, 2 * x + a * x + c, v + 1, v - 2, -v if v else 3, v + 4], f'({num(x)})² {sgn(a * x).strip()} {sgn(c).strip()} = {num(v)}.')
    v = a * x + b
    return MC(r, f'f(x) = {lin(a, b)}. Find f({num(x)}).', v, [a + x + b, a * x - b, a * (x + b), v + a, v - 1, -v if v else 2, v + 3], f'{num(a)} × ({num(x)}){sgn(b)} = {num(v)}.')


@q2.add('C2', (2, 3, 4), 'explain')
def q2_err(r, D):
    nm = person(r)
    a, b = r.randint(2, 5), r.randint(1, 9)
    lo, hi = r.randint(-4, -1), r.randint(2, 6)
    if r.random() < 0.5:
        return Q(f'f(x) = {quad(1, 0, b)} for {num(lo)} ≤ x ≤ {hi}. {nm} says the range is {num(min(lo * lo, hi * hi) + b)} ≤ f(x) ≤ {max(lo * lo, hi * hi) + b} because these are the values at the ends of the domain. Explain the error and give the correct range.',
                 f'x² is smallest at x = 0, which is in the domain, so the least value is {b}, not {min(lo * lo, hi * hi) + b}. Range: {b} ≤ f(x) ≤ {max(lo * lo, hi * hi) + b}.',
                 f'B1 minimum at x = 0 inside domain; B1 {b} ≤ f(x) ≤ {max(lo * lo, hi * hi) + b} [2]')
    return Q(f'f(x) = {lin(a, b)}. {nm} says f(x + 2) = {lin(a, b)} + 2. Explain the error and find f(x + 2) correctly.',
             f'x + 2 replaces x everywhere: f(x + 2) = {a}(x + 2){sgn(b)} = {lin(a, 2 * a + b)}.', f'B1 substitute x + 2 for x; B1 {lin(a, 2 * a + b)} [2]')


@q2.add('C3', (1, 2, 3, 4, 5))
def q2_calc(r, D):
    kind = r.choice(['solve', 'range', 'exclude', 'quadsolve'])
    a, b = r.choice([2, 3, 4, 5, -2]), r.randint(-9, 9)
    if kind == 'solve' or D <= 2:
        x = r.randint(-6, 8)
        k = a * x + b
        return Q(f'f(x) = {lin(a, b)}. Solve f(x) = {num(k)}.', f'x = {num(x)}', f'M1 {lin(a, b)} = {num(k)}; A1 x = {num(x)}.')
    if kind == 'range':
        lo, hi = r.randint(-5, 0), r.randint(1, 6)
        if r.random() < 0.5:
            v1, v2 = sorted([a * lo + b, a * hi + b])
            return Q(f'f(x) = {lin(a, b)} with domain {num(lo)} ≤ x ≤ {hi}. Find the range of f.', f'{num(v1)} ≤ f(x) ≤ {num(v2)}', f'M1 f({num(lo)}) = {num(a * lo + b)} and f({hi}) = {num(a * hi + b)}; A1 range.')
        c = r.randint(-4, 6)
        top = max(lo * lo, hi * hi) + c
        return Q(f'g(x) = {quad(1, 0, c)} with domain {num(lo)} ≤ x ≤ {hi}. Find the range of g.', f'{num(c)} ≤ g(x) ≤ {num(top)}', f'B1 least value {num(c)} at x = 0; M1 checks both ends; A1 greatest {num(top)}.')
    if kind == 'exclude':
        p = r.randint(-6, 6)
        k = r.choice([2, 3, 5, 7])
        return Q(f'h(x) = {k}/({lin(1, -p)}). (a) Find h({p + 2}). (b) State the value of x that must be excluded from the domain. (c) Solve h(x) = {k * 2}.', f'(a) {frac(Fr(k, 2))} (b) x = {num(p)} (c) x = {frac(Fr(2 * p + 1, 2))}',
                 f'(a) B1 (b) B1 denominator zero (c) M1 {k} = {k * 2}({lin(1, -p)}); A1 x = {frac(Fr(2 * p + 1, 2))}.', type='multi_step', marks=4)
    p, q = r.sample(range(-5, 7), 2)
    c = r.randint(-6, 6)
    bb, cc = -(p + q), p * q + c
    return Q(f'f(x) = {quad(1, bb, cc)}. Solve f(x) = {num(c)}.', f'x = {num(min(p, q))} or x = {num(max(p, q))}', f'M1 {quad(1, bb, p * q)} = 0; M1 factorise; A1 both.')


def q2_c4(r, D):
    a, b = r.choice([2, 3, 4]), r.randint(-6, 6)
    c = r.randint(1, 6)
    lo, hi = r.randint(-3, -1), r.randint(2, 5)
    k = r.randint(1, 8)
    xs = (k - b) / a
    intro = f'f(x) = {lin(a, b)} and g(x) = x² + {c}, where the domain of g is {num(lo)} ≤ x ≤ {hi}.'
    parts = [
        P('Find f(−2).', num(-2 * a + b), 'B1', 1),
        P(f'Solve f(x) = {k}.', f'x = {frac(Fr(k - b, a))}', 'M1 A1', 2),
        P('Find the range of g.', f'{c} ≤ g(x) ≤ {max(lo * lo, hi * hi) + c}', 'B1 B1', 2),
        P('Find f(x + 1) in its simplest form.', lin(a, a + b), 'M1 substitute; A1', 2),
        P('Explain why the equation g(x) = 0 has no solutions.', f'x² ≥ 0 so g(x) ≥ {c} > 0.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


q2.add('C4', (2, 3, 4, 5))(q2_c4)

# ---------------------------------------------------------------- composite functions
def fstr(f):
    k, a, b = f
    if k == 'lin':
        return lin(a, b)
    if k == 'sq':
        return quad(1, 0, b) if a == 1 else f'{num(a)}x²{sgn(b)}' if b else f'{num(a)}x²'
    return f'{num(a)}/x' if b == 0 else f'{num(a)}/(x{sgn(b)})'


def fval(f, x):
    k, a, b = f
    if k == 'lin':
        return a * x + b
    if k == 'sq':
        return a * x * x + b
    return Fr(a) / (x + b)


q3 = topic('Composite functions', 'composite functions', 'fg(x)', 'composite')
q3.fixed('C1', (1, 2), [
    ('f(x) = 2x + 1 and g(x) = x². What is fg(3)?', '19', 'g(3) = 9, then f(9) = 19.', ['49', '13', '10']),
    ('f(x) = 2x + 1 and g(x) = x². What is gf(3)?', '49', 'f(3) = 7, then g(7) = 49.', ['19', '36', '14']),
    ('In fg(x), which function is applied first?', 'g', 'fg(x) = f(g(x)): g acts on x first.', ['f', 'Both at the same time', 'Whichever is linear']),
    ('f(x) = x + 4 and g(x) = 3x. Which is fg(x)?', '3x + 4', 'f(g(x)) = 3x + 4.', ['3x + 12', '3x² + 4', 'x + 12']),
])
q3.fixed('C2', (2, 3), [
    ('Explain why fg(x) is usually different from gf(x).', 'The order of applying the functions matters: in fg, g is applied first; in gf, f is applied first, so the results generally differ.', 'B1 order of application; B1 example or generality [2]'),
    ('f(x) = x − 5 and g(x) = x + 5. Explain why fg(x) = x.', 'g adds 5 and f subtracts 5, so they cancel: f(g(x)) = (x + 5) − 5 = x. The functions are inverses of each other.', 'B1 working; B1 inverses [2]'),
])


def _fg_pair(r, D):
    f = ('lin', r.choice([2, 3, 4, -2, 5]), r.randint(-7, 7))
    g = r.choice([('lin', r.choice([2, 3, -1, 4]), r.randint(-6, 6)), ('sq', 1, r.randint(-4, 4))] if D >= 3 else [('lin', r.choice([2, 3, -1, 4]), r.randint(-6, 6))])
    if r.random() < 0.5:
        f, g = (g, f) if g[0] == 'lin' else (f, g)
    return f, g


@q3.add('C1', (1, 2, 3))
def q3_q(r, D):
    f, g = _fg_pair(r, D)
    x = r.randint(-3, 4)
    c = fval(f, fval(g, x))
    w = fval(g, fval(f, x))
    return MC(r, f'f(x) = {fstr(f)} and g(x) = {fstr(g)}. Find fg({num(x)}).', c, [w, fval(f, x) * fval(g, x), fval(f, x) + fval(g, x), c + 2, c - 3], f'g({num(x)}) = {num(fval(g, x))}; f({num(fval(g, x))}) = {num(c)}.')


@q3.add('C2', (2, 3, 4), 'explain')
def q3_err(r, D):
    f, g = _fg_pair(r, D)
    x = r.randint(-3, 4)
    nm = person(r)
    c = fval(f, fval(g, x))
    w = fval(g, fval(f, x))
    if c == w:
        x += 1
        c, w = fval(f, fval(g, x)), fval(g, fval(f, x))
    return Q(f'f(x) = {fstr(f)} and g(x) = {fstr(g)}. {nm} works out fg({num(x)}) by finding f({num(x)}) = {num(fval(f, x))} first and then g({num(fval(f, x))}) = {num(w)}. Explain the error and find fg({num(x)}).',
             f'In fg(x), g is applied first. g({num(x)}) = {num(fval(g, x))}, then f({num(fval(g, x))}) = {num(c)}.', f'B1 g first; B1 {num(c)} [2]')


@q3.add('C3', (2, 3, 4, 5))
def q3_calc(r, D):
    a, b = r.choice([2, 3, 4, 5]), r.randint(-6, 6)
    c, d = r.choice([2, 3, -1, -2]), r.randint(-5, 5)
    kind = r.choice(['expr', 'solve', 'ff', 'sq'])
    if kind == 'expr' or D <= 2:
        return Q(f'f(x) = {lin(a, b)} and g(x) = {lin(c, d)}. Find fg(x) and gf(x) in their simplest forms.', f'fg(x) = {lin(a * c, a * d + b)}; gf(x) = {lin(c * a, c * b + d)}',
                 f'M1 {a}({lin(c, d)}){sgn(b)}; A1 {lin(a * c, a * d + b)}; M1 {num(c)}({lin(a, b)}){sgn(d)}; A1 {lin(c * a, c * b + d)}.')
    if kind == 'solve':
        x = r.randint(-4, 6)
        k = a * (c * x + d) + b
        return Q(f'f(x) = {lin(a, b)} and g(x) = {lin(c, d)}. Solve fg(x) = {num(k)}.', f'x = {num(x)}', f'M1 fg(x) = {lin(a * c, a * d + b)}; M1 = {num(k)}; A1 x = {num(x)}.')
    if kind == 'ff':
        return Q(f'f(x) = {lin(a, b)}. Find ff(x) in its simplest form and solve ff(x) = {num(a * a * 2 + a * b + b)}.', f'ff(x) = {lin(a * a, a * b + b)}; x = 2',
                 f'M1 {a}({lin(a, b)}){sgn(b)}; A1 {lin(a * a, a * b + b)}; M1 solve; A1 x = 2.')
    p = r.randint(-4, 4)
    k = r.choice([1, 4, 9, 16, 25])
    roots = sorted([(-p + math.isqrt(k)) / 1, (-p - math.isqrt(k)) / 1])
    return Q(f'f(x) = x² and g(x) = {lin(1, p)}. Find fg(x) and solve fg(x) = {k}.', f'fg(x) = ({lin(1, p)})²; x = {num(roots[0])} or x = {num(roots[1])}',
             f'B1 ({lin(1, p)})²; M1 {lin(1, p)} = ±{math.isqrt(k)}; A1 both.')


def q3_c4(r, D):
    a, b = r.choice([2, 3, 4]), r.randint(-5, 5)
    c = r.randint(-3, 4)
    h = r.choice([2, 3, 4, 6, 12])
    intro = f'f(x) = {lin(a, b)}, g(x) = x² {"+" if c >= 0 else "−"} {abs(c)} and h(x) = {h}/x, x ≠ 0.'
    x0 = r.randint(1, 3)
    parts = [
        P(f'Find fg({x0}).', num(a * (x0 * x0 + c) + b), f'M1 g({x0}) = {x0 * x0 + c}; A1', 2),
        P('Find gf(x), giving your answer in the form px² + qx + r.', quad(a * a, 2 * a * b, b * b + c), f'M1 ({lin(a, b)})² {sgn(c).strip()}; A1', 2),
        P('Find fh(x) as a single fraction.', f'({lin(b, a * h)})/x', f'M1 {a} × {h}/x{sgn(b)}; A1', 2),
        P(f'Solve hf(x) = 1.', f'x = {frac(Fr(h - b, a))}', f'M1 {h}/({lin(a, b)}) = 1; A1', 2),
        P(f'Explain why x = {frac(Fr(-b, a))} must be excluded from the domain of hf.', f'f({frac(Fr(-b, a))}) = 0, and h(0) is undefined.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


q3.add('C4', (2, 3, 4, 5))(q3_c4)

# ---------------------------------------------------------------- inverse functions
def inv_lin(a, b):
    """inverse of ax + b as a string"""
    top = f'x{sgn(-b)}' if b else 'x'
    if a == 1:
        return lin(1, -b)
    if a == -1:
        return lin(-1, b)
    return f'({top})/{num(a)}' if b else f'x/{num(a)}'


q4 = topic('Inverse functions', 'inverse functions', 'f⁻¹(x)', 'inverse function')
q4.fixed('C1', (1, 2), [
    ('f(x) = x + 5. What is f⁻¹(x)?', 'x − 5', 'The inverse undoes adding 5.', ['x + 5', '5 − x', '1/(x + 5)']),
    ('f(x) = 4x. What is f⁻¹(x)?', 'x/4', 'Inverse of multiplying by 4 is dividing by 4.', ['4/x', '−4x', 'x − 4']),
    ('If f(3) = 11, what is f⁻¹(11)?', '3', 'The inverse maps the output back to the input.', ['11', '1/11', '−3']),
    ('The graph of y = f⁻¹(x) is the reflection of y = f(x) in the line', 'y = x', 'Inputs and outputs swap.', ['y = 0', 'x = 0', 'y = −x']),
    ('What is ff⁻¹(x)?', 'x', 'A function followed by its inverse returns the input.', ['f(x)', '1', 'x²']),
])
q4.fixed('C2', (2, 3), [
    ('Explain why ff⁻¹(x) = x for any function f that has an inverse.', 'f⁻¹ reverses the effect of f, so applying f after f⁻¹ returns the original input.', 'B1 inverse undoes; B1 returns x [2]'),
    ('Explain why the graph of y = f⁻¹(x) is a reflection of y = f(x) in the line y = x.', 'If (a, b) lies on y = f(x) then (b, a) lies on y = f⁻¹(x); swapping coordinates is a reflection in y = x.', 'B1 coordinates swap; B1 reflection in y = x [2]'),
    ('Explain why f(x) = x² for all real x does not have an inverse function.', 'Two different inputs (e.g. 3 and −3) give the same output 9, so the inverse would not give a single value.', 'B1 many-to-one; B1 inverse not unique [2]'),
])


@q4.add('C1', (1, 2, 3))
def q4_q(r, D):
    a, b = r.choice([2, 3, 4, 5, 6]), r.choice([-7, -5, -3, -1, 1, 2, 3, 4, 8])
    c = inv_lin(a, b)
    ds = [inv_lin(a, -b), f'{num(a)}x{sgn(-b)}', f'x/{num(a)}{sgn(-b)}', f'1/({lin(a, b)})', f'({lin(1, b)})/{num(a)}']
    return SMC(r, f'f(x) = {lin(a, b)}. Find f⁻¹(x).', c, ds, f'y = {lin(a, b)} → x = (y{sgn(-b)})/{num(a)}, so f⁻¹(x) = {c}.')


@q4.add('C2', (2, 3, 4), 'explain')
def q4_err(r, D):
    a, b = r.choice([2, 3, 4, 5]), r.randint(1, 9)
    nm = person(r)
    return Q(f'{nm} finds the inverse of f(x) = {lin(a, b)} by "reversing the operations" and writes f⁻¹(x) = x/{a}{sgn(-b)}. Explain the error and find f⁻¹(x).',
             f'The operations must be reversed in reverse order: subtract {b} first, then divide by {a}. f⁻¹(x) = (x − {b})/{a}.', f'B1 order of reversing; B1 (x − {b})/{a} [2]')


@q4.add('C3', (2, 3, 4, 5))
def q4_calc(r, D):
    kind = r.choice(['lin', 'frac', 'eval', 'rec', 'self'])
    a, b = r.choice([2, 3, 4, 5]), r.randint(-8, 8)
    if b == 0:
        b = 3
    if kind == 'lin' or D <= 2:
        return Q(f'f(x) = {lin(a, b)}. Find f⁻¹(x).', inv_lin(a, b), f'M1 y = {lin(a, b)}, swap/rearrange: x = (y{sgn(-b)})/{a}; A1 f⁻¹(x) = {inv_lin(a, b)}.')
    if kind == 'frac':
        c = r.choice([2, 3, 4, 5])
        return Q(f'g(x) = ({lin(a, b)})/{c}. Find g⁻¹(x).', f'({lin(c, -b)})/{a}', f'M1 {c}y = {lin(a, b)}; M1 {term_str(a, "x")} = {lin(c, -b, "y")}; A1 g⁻¹(x) = ({lin(c, -b)})/{a}.')
    if kind == 'eval':
        k = r.randint(-6, 10)
        return Q(f'f(x) = {lin(a, b)}. Find f⁻¹({num(k)}).', frac(Fr(k - b, a)), f'M1 solve {lin(a, b)} = {num(k)} or use f⁻¹(x) = {inv_lin(a, b)}; A1 {frac(Fr(k - b, a))}.')
    if kind == 'rec':
        k = r.choice([2, 3, 4, 6])
        p = r.randint(-5, 5)
        return Q(f'h(x) = {k}/(x{sgn(p)}), x ≠ {num(-p)}. Find h⁻¹(x).', f'{k}/x{sgn(-p)}', f'M1 y(x{sgn(p)}) = {k}; M1 x = {k}/y{sgn(-p)}; A1 h⁻¹(x) = {k}/x{sgn(-p)}.')
    # f(x) = f^-1(x) for linear: ax + b = (x - b)/a -> a²x + ab = x - b -> x = -b(a+1)/(a²-1) = -b/(a-1)
    xs = Fr(-b, a - 1)
    return Q(f'f(x) = {lin(a, b)}. Find f⁻¹(x) and solve the equation f(x) = f⁻¹(x).', f'f⁻¹(x) = {inv_lin(a, b)}; x = {frac(xs)}',
             f'B1 f⁻¹(x); M1 {lin(a, b)} = {inv_lin(a, b)}; M1 {lin(a * a, a * b)} = {lin(1, -b)}; A1 x = {frac(xs)}.')


def q4_c4(r, D):
    a, b = r.choice([2, 3, 4, 5]), r.choice([-7, -5, -3, -1, 1, 2, 3, 6])
    c, d = r.choice([2, 3]), r.randint(-4, 4)
    k = r.randint(1, 9)
    intro = f'f(x) = {lin(a, b)} and g(x) = {lin(c, d)}.'
    fg_a, fg_b = a * c, a * d + b
    parts = [
        P('Find f⁻¹(x).', inv_lin(a, b), 'M1 A1', 2),
        P(f'Find f⁻¹({k}).', frac(Fr(k - b, a)), 'B1', 1),
        P('Find fg(x).', lin(fg_a, fg_b), 'M1 A1', 2),
        P('Find (fg)⁻¹(x).', inv_lin(fg_a, fg_b), 'M1 rearrange; A1', 2),
        P('Show that g⁻¹f⁻¹(x) = (fg)⁻¹(x).', f'g⁻¹(x) = {inv_lin(c, d)}; g⁻¹(f⁻¹(x)) simplifies to {inv_lin(fg_a, fg_b)}', 'M1 g⁻¹; M1 composition; A1 simplification', 3),
        P('Describe the relationship between the graphs of y = f(x) and y = f⁻¹(x).', 'Each is the reflection of the other in the line y = x.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


q4.add('C4', (2, 3, 4, 5))(q4_c4)
CHAPTERS[10] = [q1, q2, q3, q4]


# =========================================================== 11 Transformations and vectors (Ch 23)
def _dc(v):
    if isinstance(v, Fr) and v.denominator in (2, 4, 5, 10):
        return num(float(v))
    return num(v)


def pt(p):
    return f'({_dc(p[0])}, {_dc(p[1])})'


def nice(m):
    return num(int(round(m))) if abs(m - round(m)) < 1e-9 else n3(m)


def cv(p, q):
    return f'({num(p)}, {num(q)})'


TRANS = [
    ('reflection in the x-axis', lambda x, y: (x, -y)), ('reflection in the y-axis', lambda x, y: (-x, y)),
    ('reflection in the line y = x', lambda x, y: (y, x)), ('reflection in the line y = −x', lambda x, y: (-y, -x)),
    ('rotation of 90° clockwise about the origin', lambda x, y: (y, -x)), ('rotation of 90° anticlockwise about the origin', lambda x, y: (-y, x)),
    ('rotation of 180° about the origin', lambda x, y: (-x, -y)),
]


def trans_k(r):
    kind = r.choice(['rx', 'ry', 'rot', 'tr'])
    if kind == 'rx':
        k = r.choice([-2, -1, 1, 2, 3, 4])
        return f'reflection in the line x = {num(k)}', (lambda x, y, k=k: (2 * k - x, y))
    if kind == 'ry':
        k = r.choice([-3, -1, 1, 2, 3])
        return f'reflection in the line y = {num(k)}', (lambda x, y, k=k: (x, 2 * k - y))
    if kind == 'rot':
        a, b = r.randint(-2, 3), r.randint(-2, 3)
        d = r.choice(['90° clockwise', '90° anticlockwise', '180°'])
        if d == '90° clockwise':
            f = lambda x, y, a=a, b=b: (a + (y - b), b - (x - a))
        elif d == '90° anticlockwise':
            f = lambda x, y, a=a, b=b: (a - (y - b), b + (x - a))
        else:
            f = lambda x, y, a=a, b=b: (2 * a - x, 2 * b - y)
        return f'rotation of {d} about {pt((a, b))}', f
    p, q = r.randint(-6, 6), r.randint(-6, 6)
    if p == 0 and q == 0:
        p = 3
    return f'translation by the vector {cv(p, q)}', (lambda x, y, p=p, q=q: (x + p, y + q))


v1 = topic('Reflection, rotation and translation', 'reflection, rotation and translation', 'describing transformations fully', 'transformations')
v1.fixed('C1', (1, 2), [
    ('To describe a rotation fully you must give', 'the centre, the angle and the direction', 'All three are needed (except for 180°, where direction is not needed).', ['the angle only', 'the centre and the mirror line', 'the vector and the angle']),
    ('To describe a translation fully you must give', 'the column vector', 'The vector gives the horizontal and vertical movement.', ['the centre of translation', 'the angle and direction', 'the scale factor']),
    ('To describe a reflection fully you must give', 'the equation of the mirror line', 'For example "reflection in the line y = 2".', ['the centre of reflection', 'the angle of reflection', 'the vector']),
    ('Under which transformation is the image NOT congruent to the object?', 'Enlargement with scale factor 2', 'Reflections, rotations and translations preserve size and shape.', ['Reflection in y = x', 'Rotation of 90°', 'Translation by a vector']),
    ('The point (3, 5) is reflected in the y-axis. What is its image?', '(−3, 5)', 'Reflection in the y-axis changes the sign of x.', ['(3, −5)', '(5, 3)', '(−3, −5)']),
])
v1.fixed('C2', (2, 3), [
    ('Explain why "a rotation of 90°" is not a full description of a transformation.', 'It does not state the centre of rotation or the direction (clockwise or anticlockwise).', 'B1 centre missing; B1 direction missing [2]'),
    ('A shape is reflected in the x-axis and then in the y-axis. Explain which single transformation has the same effect.', '(x, y) → (x, −y) → (−x, −y), which is a rotation of 180° about the origin.', 'B1 working with coordinates; B1 rotation 180° about origin [2]'),
    ('Explain why the answer to a question asking for "a single transformation" must not describe two transformations.', 'The question asks for one transformation that maps the object directly onto the image; a combination is not a single transformation and scores no marks.', 'B1 one transformation required; B1 combinations not accepted [2]'),
])


@v1.add('C1', (1, 2, 3))
def v1_img(r, D):
    nm, f = r.choice(TRANS) if D <= 2 else trans_k(r)
    p = (r.choice([-5, -4, -3, -2, 1, 2, 3, 4, 5]), r.choice([-4, -3, -1, 1, 2, 3, 5, 6]))
    if abs(p[0]) == abs(p[1]):
        p = (p[0], p[1] + 1 if p[1] + 1 != 0 else 2)
    img = f(*p)
    ds = [pt((-img[0], img[1])), pt((img[0], -img[1])), pt((img[1], img[0])), pt((-img[1], -img[0])), pt(p), pt((img[0] + 1, img[1]))]
    return SMC(r, f'The point P{pt(p)} is mapped by a {nm}. What are the coordinates of the image of P?', pt(img), ds, f'Under a {nm}, {pt(p)} → {pt(img)}.')


@v1.add('C2', (2, 3, 4), 'explain')
def v1_err(r, D):
    nm = person(r)
    kind = r.choice(['rot', 'two', 'tr'])
    if kind == 'rot':
        a, b = r.randint(-3, 3), r.randint(-3, 3)
        d = r.choice(['clockwise', 'anticlockwise'])
        return Q(f'Triangle A is mapped onto triangle B by a rotation of 90° {d} about {pt((a, b))}. {nm} describes the transformation as "a turn of 90°". Explain why this description is incomplete and write a full description.',
                 f'It must include the centre and the direction: rotation, 90° {d}, centre {pt((a, b))}.', 'B1 identifies missing centre/direction; B1 full description [2]')
    if kind == 'two':
        return Q(f'Shape P is mapped onto shape Q by a reflection in the y-axis followed by a reflection in the x-axis. {nm} says the single transformation is "a reflection in both axes". Explain why this is not acceptable and give the correct single transformation.',
                 'A single transformation is required. (x, y) → (−x, y) → (−x, −y), which is a rotation of 180° about the origin.', 'B1 not a single transformation; B1 rotation 180° about (0, 0) [2]')
    p, q = r.randint(-6, 6), r.randint(-6, 6)
    if p == 0:
        p = 4
    return Q(f'A triangle moves {abs(p)} units {"right" if p > 0 else "left"} and {abs(q)} units {"up" if q >= 0 else "down"}. {nm} writes the translation vector as {cv(q, p)}. Explain the error and give the correct vector.',
             f'The top number is the horizontal movement and the bottom is the vertical movement: {cv(p, q)}.', f'B1 order of components; B1 {cv(p, q)} [2]')


@v1.add('C3', (1, 2, 3, 4))
def v1_tri(r, D):
    tri = [(r.randint(1, 3), r.randint(1, 3))]
    tri.append((tri[0][0] + r.randint(2, 4), tri[0][1]))
    tri.append((tri[0][0], tri[0][1] + r.randint(2, 4)))
    nm, f = r.choice(TRANS) if D <= 2 else trans_k(r)
    img = [f(*p) for p in tri]
    return Q(f'Triangle T has vertices {pt(tri[0])}, {pt(tri[1])} and {pt(tri[2])}. Find the coordinates of the vertices of the image of T after a {nm}.', ', '.join(pt(p) for p in img),
             'B2 all three vertices correct (B1 for two correct).', marks=2 if D <= 2 else 3)


@v1.add('C3', (2, 3, 4, 5))
def v1_describe(r, D):
    nm, f = trans_k(r) if D >= 3 else r.choice(TRANS)
    tri = [(1, 1), (r.randint(3, 4), 1), (1, r.randint(3, 4))]
    tri = [(x + r.choice([0, 1]), y + r.choice([0, 1])) for x, y in tri]
    img = [f(*p) for p in tri]
    return Q(f'Triangle A has vertices {", ".join(pt(p) for p in tri)}. Triangle B has vertices {", ".join(pt(p) for p in img)} (in the same order). Describe fully the single transformation that maps triangle A onto triangle B.',
             nm[0].upper() + nm[1:], ('B1 rotation; B1 centre; B1 angle and direction.' if 'otation' in nm else 'B1 type of transformation; B1 full details (mirror line / vector).'), marks=3 if 'otation' in nm else 2)


def v1_c4(r, D):
    tri = [(1, 1), (r.randint(3, 4), 1), (1, r.randint(2, 4))]
    p, q = r.randint(-6, -2), r.randint(1, 5)
    combo = r.choice([('reflection in the x-axis', lambda x, y: (x, -y), 'reflection in the y-axis', lambda x, y: (-x, y), 'rotation of 180° about the origin'),
                      ('reflection in the line y = x', lambda x, y: (y, x), 'reflection in the x-axis', lambda x, y: (x, -y), 'rotation of 90° clockwise about the origin'),
                      ('reflection in the y-axis', lambda x, y: (-x, y), 'reflection in the line y = x', lambda x, y: (y, x), 'rotation of 90° clockwise about the origin'),
                      ('rotation of 90° anticlockwise about the origin', lambda x, y: (-y, x), 'reflection in the x-axis', lambda x, y: (x, -y), 'reflection in the line y = −x')])
    n1, f1, n2, f2, single = combo
    A = [f1(*x) for x in tri]
    B = [f2(*x) for x in A]
    C = [(x + p, y + q) for x, y in tri]
    intro = f'Triangle T has vertices {", ".join(pt(x) for x in tri)}. Triangle A is the image of T after a {n1}. Triangle B is the image of A after a {n2}.'
    parts = [
        P('Write down the coordinates of the vertices of A.', ', '.join(pt(x) for x in A), 'B2 (B1 for two correct)', 2),
        P('Write down the coordinates of the vertices of B.', ', '.join(pt(x) for x in B), 'B2 (B1 for two correct)', 2),
        P('Describe fully the single transformation that maps T onto B.', single[0].upper() + single[1:], 'B1 type; B1 or B2 full details', 3 if 'rotation' in single else 2),
        P(f'Triangle C has vertices {", ".join(pt(x) for x in C)}. Describe fully the single transformation that maps T onto C.', f'Translation by the vector {cv(p, q)}', 'B1 translation; B1 vector', 2),
        P('Explain why T and B are congruent.', 'Reflections (and rotations) do not change lengths or angles, so the image has the same size and shape.', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


v1.add('C4', (2, 3, 4, 5))(v1_c4)

# ---------------------------------------------------------------- enlargement
SF = [2, 3, Fr(1, 2), Fr(1, 3), -1, -2, Fr(-1, 2), Fr(3, 2), Fr(5, 2)]


def enl(c, k, p):
    return (c[0] + k * (p[0] - c[0]), c[1] + k * (p[1] - c[1]))


v2 = topic('Enlargement', 'enlargement including fractional and negative scale factors', 'enlargement', 'scale factor')
v2.fixed('C1', (1, 2), [
    ('A shape is enlarged by scale factor 3. By what factor is its area multiplied?', '9', 'Area scale factor = (length scale factor)².', ['3', '6', '27']),
    ('An enlargement has scale factor ½. What happens to the lengths of the shape?', 'They are halved', 'A fractional scale factor between 0 and 1 makes the image smaller.', ['They are doubled', 'They stay the same', 'They are squared']),
    ('An enlargement with a negative scale factor produces an image that is', 'on the opposite side of the centre and upside down', 'Each point moves through the centre to the other side.', ['on the same side and the same way up', 'always smaller', 'a reflection of the object']),
    ('To describe an enlargement fully you must give', 'the scale factor and the centre of enlargement', 'Both are needed.', ['the scale factor only', 'the angle and the centre', 'the mirror line']),
    ('The point (2, 3) is enlarged by scale factor 2 with centre the origin. What is its image?', '(4, 6)', 'Multiply each coordinate by 2.', ['(4, 3)', '(2, 6)', '(1, 1.5)']),
])
v2.fixed('C2', (2, 3), [
    ('Explain why an enlargement with scale factor ½ is still called an enlargement even though the shape gets smaller.', 'In mathematics an enlargement is any transformation where lengths are multiplied by the same scale factor from a centre; a factor between 0 and 1 gives a smaller image.', 'B1 definition; B1 factor < 1 gives reduction [2]'),
    ('Explain how to find the centre of an enlargement from an object and its image on a grid.', 'Draw straight lines through corresponding vertices of the object and image; the centre is where these lines meet.', 'B1 join corresponding points; B1 intersection is centre [2]'),
    ('Explain how an enlargement with scale factor −1 is related to a rotation.', 'Scale factor −1 maps each point to the opposite side of the centre at the same distance, which is the same as a rotation of 180° about the centre.', 'B1 same distance opposite side; B1 rotation 180° [2]'),
])


@v2.add('C1', (1, 2, 3))
def v2_q(r, D):
    k = r.choice(SF[:4] if D <= 2 else SF)
    c = (0, 0) if D <= 2 else (r.randint(-2, 3), r.randint(-2, 3))
    p = (c[0] + r.choice([2, 4, 6, -2, -4]), c[1] + r.choice([2, 4, 6, -4]))
    img = enl(c, k, p)
    ds = [pt(enl(c, -k, p)), pt((p[0] * k, p[1] * k)) if c != (0, 0) else pt((p[0] + k, p[1] + k)), pt(enl(c, 1 / Fr(k), p)), pt((img[1], img[0])), pt((img[0], -img[1]))]
    return SMC(r, f'The point {pt(p)} is enlarged with scale factor {frac(k)} and centre {pt(c)}. What is its image?', pt(img), ds, f'Image = centre + {frac(k)} × (P − centre) = {pt(img)}.')


@v2.add('C2', (2, 3, 4), 'explain')
def v2_err(r, D):
    k = r.choice([2, 3, 4, Fr(1, 2), Fr(5, 2)])
    A = r.choice([6, 8, 10, 12, 20, 24])
    nm = person(r)
    return Q(f'A shape with area {A} cm² is enlarged by scale factor {frac(k)}. {nm} says the area of the image is {frac(A * k)} cm². Explain the error and find the correct area.',
             f'Area is multiplied by the square of the scale factor ({frac(k * k)}), so the area is {frac(A * k * k)} cm².', f'B1 area factor k²; B1 {frac(A * k * k)} cm² [2]')


@v2.add('C3', (1, 2, 3, 4, 5))
def v2_calc(r, D):
    if D <= 3:
        k = r.choice(SF[:4] if D <= 2 else SF)
        c = (0, 0) if D == 1 else (r.randint(-2, 2), r.randint(-2, 2))
        tri = [(c[0] + 2, c[1] + 2), (c[0] + 6, c[1] + 2), (c[0] + 2, c[1] + 4)]
        img = [enl(c, k, p) for p in tri]
        return Q(f'Triangle T has vertices {", ".join(pt(p) for p in tri)}. T is enlarged with scale factor {frac(k)} and centre {pt(c)}. Find the coordinates of the vertices of the image.', ', '.join(pt(p) for p in img),
                 'M1 vector from centre × scale factor; A1 one vertex correct; A2 all three vertices (A1 two).')
    k = r.choice([2, 3, Fr(1, 2), -1, -2, Fr(-1, 2)])
    c = (r.randint(-3, 3), r.randint(-3, 3))
    p, q = (c[0] + 2, c[1] + 2), (c[0] + 4, c[1] + 2 + r.choice([0, 2]))
    P1, Q1 = enl(c, k, p), enl(c, k, q)
    return Q(f'An enlargement maps A{pt(p)} to A′{pt(P1)} and B{pt(q)} to B′{pt(Q1)}. Find the scale factor and the centre of the enlargement.', f'Scale factor {frac(k)}; centre {pt(c)}',
             f'M1 A′B′ ÷ AB (with direction) gives {frac(k)}; M1 centre C satisfies A′ = C + k(A − C); A1 {pt(c)}.')


def v2_c4(r, D):
    k = r.choice([2, 3, Fr(1, 2), -2, Fr(-1, 2)])
    c = (r.randint(-2, 2), r.randint(-2, 2))
    tri = [(c[0] + 2, c[1] + 1), (c[0] + 6, c[1] + 1), (c[0] + 2, c[1] + 4)]
    img = [enl(c, k, p) for p in tri]
    area = Fr(1, 2) * 4 * 3
    intro = f'Triangle P has vertices {", ".join(pt(p) for p in tri)}. P is enlarged with scale factor {frac(k)}, centre {pt(c)}, to give triangle Q.'
    parts = [
        P('Find the coordinates of the vertices of Q.', ', '.join(pt(p) for p in img), 'M1; A2', 3),
        P('Calculate the area of P.', f'{frac(area)} square units', 'B1', 1),
        P('Calculate the area of Q.', f'{frac(area * k * k)} square units', f'M1 × ({frac(k)})²; A1', 2),
        P('Calculate the length of the longest side of Q.', f'{n3(5 * abs(float(k)))} units', f'M1 longest side of P = 5; A1 × {frac(abs(k))}', 2),
        P('Describe fully the single transformation that maps Q back onto P.', f'Enlargement, scale factor {frac(1 / Fr(k))}, centre {pt(c)}', 'B1 enlargement; B1 scale factor; B1 centre', 3),
    ]
    return cmp_(r, intro, parts)


v2.add('C4', (2, 3, 4, 5))(v2_c4)

# ---------------------------------------------------------------- vectors
UF = {Fr(1, 2): '½', Fr(1, 3): '⅓', Fr(2, 3): '⅔', Fr(1, 4): '¼', Fr(3, 4): '¾', Fr(1, 5): '⅕', Fr(2, 5): '⅖', Fr(3, 5): '⅗', Fr(4, 5): '⅘'}


def vterm(c, v):
    c = Fr(c)
    a = abs(c)
    if a == 1:
        s = v
    elif a.denominator == 1:
        s = f'{a.numerator}{v}'
    elif a in UF:
        s = f'{UF[a]}{v}'
    else:
        s = f'({a.numerator}/{a.denominator}){v}'
    return s


def vex(*terms):
    out = ''
    for c, v in terms:
        if c == 0:
            continue
        t = vterm(c, v)
        if not out:
            out = (MINUS if c < 0 else '') + t
        else:
            out += (' − ' if c < 0 else ' + ') + t
    return out or '0'


v3 = topic('Vector notation and operations', 'vector notation', 'addition, subtraction and scalar multiples', 'vectors')
v3.fixed('C1', (1, 2), [
    ('a = (3, −2) and b = (1, 4) are column vectors. What is a + b?', '(4, 2)', 'Add the components: 3 + 1 = 4, −2 + 4 = 2.', ['(2, −6)', '(3, −8)', '(4, −6)']),
    ('a = (2, 5). What is 3a?', '(6, 15)', 'Multiply each component by 3.', ['(5, 8)', '(6, 5)', '(2, 15)']),
    ('If AB = a, what is BA?', '−a', 'Reversing the direction changes the sign.', ['a', '2a', '½a']),
    ('Two vectors are parallel if', 'one is a scalar multiple of the other', 'For example 2a + 4b is parallel to a + 2b.', ['they have the same length', 'they start at the same point', 'their components add to zero']),
    ('The vector (0, −3) represents a movement of', '3 units down', 'Top component horizontal (0), bottom vertical (−3).', ['3 units left', '3 units right', '3 units up']),
])
v3.fixed('C2', (2, 3), [
    ('Explain why the vectors (2, 3) and (6, 9) are parallel.', '(6, 9) = 3 × (2, 3), so one is a scalar multiple of the other and they have the same direction.', 'B1 scalar multiple; B1 conclusion [2]'),
    ('Explain the difference between the vectors AB and BA.', 'They have the same length but opposite directions: BA = −AB.', 'B1 same magnitude; B1 opposite direction [2]'),
    ('Explain what a negative scalar multiple, such as −2a, represents.', 'A vector twice as long as a but in the opposite direction.', 'B1 length doubled; B1 opposite direction [2]'),
])


def rv(r, lo=-6, hi=6):
    while True:
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        if (a, b) != (0, 0):
            return a, b


@v3.add('C1', (1, 2, 3))
def v3_q(r, D):
    a, b = rv(r), rv(r)
    m, n = r.choice([1, 2, 3]), r.choice([1, -1, 2, -2])
    c = (m * a[0] + n * b[0], m * a[1] + n * b[1])
    ds = [cv(m * a[0] - n * b[0], m * a[1] - n * b[1]), cv(m * a[0] + n * b[1], m * a[1] + n * b[0]), cv(a[0] + n * b[0], a[1] + n * b[1]) if m != 1 else cv(c[0] + 1, c[1]), cv(c[1], c[0]), cv(-c[0], c[1])]
    return SMC(r, f'In column vector form, a = {cv(*a)} and b = {cv(*b)}. Find {vex((m, "a"), (n, "b"))}.', cv(*c), ds, f'{vex((m, "a"), (n, "b"))} = {cv(*c)}.')


@v3.add('C2', (2, 3, 4), 'explain')
def v3_err(r, D):
    a, b = rv(r, -5, 5), rv(r, -5, 5)
    nm = person(r)
    c = (2 * a[0] - 3 * b[0], 2 * a[1] - 3 * b[1])
    wrong = (2 * a[0] - 3 * b[0], 2 * a[1] + 3 * b[1]) if b[1] < 0 else (2 * a[0] + 3 * b[0], 2 * a[1] - 3 * b[1])
    if wrong == c:
        wrong = (c[0] + 2, c[1])
    return Q(f'a = {cv(*a)} and b = {cv(*b)}. {nm} calculates 2a − 3b = {cv(*wrong)}. Explain the error and find the correct answer.',
             f'Each component must be found as 2 × (a component) − 3 × (b component): 2a − 3b = {cv(*c)}.', f'B1 identifies sign/component error; B1 {cv(*c)} [2]')


@v3.add('C3', (1, 2, 3, 4, 5))
def v3_calc(r, D):
    kind = r.choice(['comb', 'solve', 'par', 'pts'])
    a, b = rv(r, -5, 5), rv(r, -5, 5)
    if kind == 'comb' or D == 1:
        m, n = r.choice([2, 3, 4, -1]), r.choice([-3, -2, 2, 3])
        c = (m * a[0] + n * b[0], m * a[1] + n * b[1])
        return Q(f'a = {cv(*a)} and b = {cv(*b)} are column vectors. Write {vex((m, "a"), (n, "b"))} as a column vector.', cv(*c), f'M1 {cv(m * a[0], m * a[1])} {"+" if n > 0 else "−"} {cv(abs(n) * b[0], abs(n) * b[1])}; A1 {cv(*c)}.')
    if kind == 'solve':
        m, n = r.randint(-3, 4), r.randint(-3, 4)
        if a[0] * b[1] - a[1] * b[0] == 0:
            b = (b[0] + 1, b[1])
        if a[0] * b[1] - a[1] * b[0] == 0:
            return None
        c = (m * a[0] + n * b[0], m * a[1] + n * b[1])
        return Q(f'a = {cv(*a)}, b = {cv(*b)} and c = {cv(*c)}. Find the values of m and n such that ma + nb = c.', f'm = {num(m)}, n = {num(n)}',
                 f'M1 {expr((a[0], "m"), (b[0], "n"))} = {num(c[0])} and {expr((a[1], "m"), (b[1], "n"))} = {num(c[1])}; M1 solve; A1 A1.')
    if kind == 'par':
        k = r.choice([2, 3, -2, Fr(1, 2)])
        q = (a[0] * k, a[1] * k)
        t = r.choice([q, (q[0] + 1, q[1])])
        par = t == q
        return Q(f'Show whether the vectors {cv(*a)} and {cv(*t)} are parallel.', f'{"Parallel" if par else "Not parallel"}' + (f': {cv(*t)} = {frac(k)} × {cv(*a)}.' if par else ': the components are not in the same ratio.'),
                 'M1 compares ratios of components; A1 conclusion.')
    A_, B_ = (r.randint(-5, 5), r.randint(-5, 5)), (r.randint(-5, 5), r.randint(-5, 5))
    if A_ == B_:
        B_ = (B_[0] + 3, B_[1])
    return Q(f'A is the point {pt(A_)} and B is the point {pt(B_)}. Write AB as a column vector, and find the coordinates of C where BC = AB.', f'AB = {cv(B_[0] - A_[0], B_[1] - A_[1])}; C {pt((2 * B_[0] - A_[0], 2 * B_[1] - A_[1]))}',
             f'B1 AB = B − A = {cv(B_[0] - A_[0], B_[1] - A_[1])}; M1 C = B + AB; A1 {pt((2 * B_[0] - A_[0], 2 * B_[1] - A_[1]))}.')


def v3_c4(r, D):
    a, b = rv(r, -4, 5), rv(r, -4, 5)
    if a[0] * b[1] == a[1] * b[0]:
        b = (b[0] + 1, b[1] + 2)
    O = (0, 0)
    A_ = a
    B_ = b
    intro = f'O is the origin. A and B are points with OA = a = {cv(*a)} and OB = b = {cv(*b)}.'
    AB = (b[0] - a[0], b[1] - a[1])
    M = (Fr(a[0] + b[0], 2), Fr(a[1] + b[1], 2))
    parts = [
        P('Write AB as a column vector.', cv(*AB), 'B1', 1),
        P('Find the coordinates of the midpoint M of AB.', pt(M), 'M1 a + ½AB; A1', 2),
        P('Find 2a − b as a column vector.', cv(2 * a[0] - b[0], 2 * a[1] - b[1]), 'B1 B1', 2),
        P(f'C is the point such that OC = a + b. Explain what type of quadrilateral OACB is.', 'A parallelogram, since AC = b = OB and BC = a = OA.', 'B1 parallelogram; B1 reason', 2),
        P('Find the value of k for which ka + b is parallel to the x-axis.' if a[1] != 0 else 'Find the value of k for which a + kb is parallel to the x-axis.',
          (f'k = {frac(Fr(-b[1], a[1]))}' if a[1] != 0 else (f'k = {frac(Fr(-a[1], b[1]))}' if b[1] != 0 else 'any k')), 'M1 y-component = 0; A1', 2),
    ]
    return cmp_(r, intro, parts)


v3.add('C4', (2, 3, 4, 5))(v3_c4)

# ---------------------------------------------------------------- magnitude and vector geometry
v4 = topic('Magnitude of a vector and vector geometry', 'magnitude of a vector', 'vector geometry', 'magnitude')
v4.fixed('C1', (1, 2), [
    ('What is the magnitude of the vector (3, 4)?', '5', '√(3² + 4²) = 5.', ['7', '12', '25']),
    ('O is the origin, OA = a and OB = b. Which vector is AB?', 'b − a', 'AB = AO + OB = −a + b.', ['a − b', 'a + b', '½(a + b)']),
    ('M is the midpoint of AB, where OA = a and OB = b. What is OM?', '½(a + b)', 'OM = a + ½(b − a) = ½(a + b).', ['a + b', '½(b − a)', 'b − a']),
    ('If AB = 2CD, which statement is true?', 'AB is parallel to CD and twice as long', 'A scalar multiple means parallel; factor 2 gives the length ratio.', ['AB and CD are perpendicular', 'AB is half as long as CD', 'A, B, C and D lie on a straight line']),
])
v4.fixed('C2', (2, 3), [
    ('Explain how vectors can be used to show that three points A, B and C lie on a straight line.', 'Show that AB is a scalar multiple of AC (or BC); then the lines are parallel and share the point A, so the points are collinear.', 'B1 scalar multiple; B1 common point [2]'),
    ('Explain why the magnitude of a vector can never be negative.', 'It is a length, found from √(x² + y²), and a square root of a sum of squares is never negative.', 'B1 length; B1 √ of squares ≥ 0 [2]'),
    ('Explain why |a + b| is usually not equal to |a| + |b|.', 'The vectors form two sides of a triangle; the third side is shorter than the sum of the other two unless a and b are in the same direction.', 'B1 triangle inequality; B1 equal only if same direction [2]'),
])

PYTH = [(3, 4), (5, 12), (6, 8), (8, 15), (7, 24), (9, 12), (12, 16), (2, 3), (1, 5), (4, 7), (2, 6), (5, 5)]


@v4.add('C1', (1, 2, 3))
def v4_q(r, D):
    x, y = r.choice(PYTH)
    x, y = x * r.choice([1, -1]), y * r.choice([1, -1])
    m = math.hypot(x, y)
    return MC(r, f'Find the magnitude of the vector {cv(x, y)}.', m, [abs(x) + abs(y), x * x + y * y, abs(abs(x) - abs(y)) if abs(x) != abs(y) else 1, m + 1], f'√(({num(x)})² + ({num(y)})²) = √{x * x + y * y} = {nice(m)}.', fmtf=lambda v: n3(v) if abs(v - round(v)) > 1e-9 else num(round(v)))


@v4.add('C2', (2, 3, 4), 'explain')
def v4_err(r, D):
    x, y = r.choice(PYTH[:6])
    x = -x
    nm = person(r)
    return Q(f'{nm} says the magnitude of {cv(x, y)} is √({num(x)} + {num(y)}) = √{x + y}. Explain the error and find the correct magnitude.' if x + y > 0 else
             f'{nm} says the magnitude of {cv(x, y)} is {num(x + y)}, by adding the components. Explain the error and find the correct magnitude.',
             f'Magnitude uses Pythagoras: √(({num(x)})² + {num(y)}²) = √{x * x + y * y} = {nice(math.hypot(x, y))}.', f'B1 must square components; B1 {nice(math.hypot(x, y))} [2]')


@v4.add('C3', (2, 3, 4, 5))
def v4_geo(r, D):
    kind = r.choice(['mid', 'ratio', 'mag', 'collinear'])
    if kind == 'mag':
        a, b = rv(r, -5, 5), rv(r, -5, 5)
        m, n = r.choice([2, 3, -1]), r.choice([1, -2, 2])
        c = (m * a[0] + n * b[0], m * a[1] + n * b[1])
        return Q(f'a = {cv(*a)} and b = {cv(*b)}. Find |{vex((m, "a"), (n, "b"))}|.', n3(math.hypot(*c)), f'M1 {vex((m, "a"), (n, "b"))} = {cv(*c)}; M1 √(({num(c[0])})² + ({num(c[1])})²); A1 {n3(math.hypot(*c))}.')
    if kind == 'mid':
        return Q('OAB is a triangle with OA = a and OB = b. M is the midpoint of AB. Find, in terms of a and b, (a) AB (b) AM (c) OM, giving each in its simplest form.',
                 '(a) b − a (b) ½b − ½a (c) ½a + ½b', '(a) B1 (b) B1 (c) M1 OA + AM; A1.', type='multi_step', marks=4) if D <= 3 else None
    m, n = r.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (1, 4)])
    if kind == 'ratio':
        t = Fr(m, m + n)
        return Q(f'OA = a and OB = b. P lies on AB such that AP : PB = {m} : {n}. Find OP in terms of a and b, in its simplest form.', vex((1 - t, 'a'), (t, 'b')),
                 f'M1 OP = OA + {frac(t)}AB; M1 a + {frac(t)}(b − a); A1 {vex((1 - t, "a"), (t, "b"))}.')
    k = r.choice([2, 3])
    return Q(f'OA = a, OB = b and OC = {vex((1 - k, "a"), (k, "b"))}. Show that A, B and C lie on a straight line.', f'AB = b − a and AC = {vex((-k, "a"), (k, "b"))} = {k}(b − a) = {k}AB, so AC is parallel to AB and they share point A.',
             f'M1 AB = b − a; M1 AC = OC − OA; A1 AC = {k}AB with conclusion (common point A).')


def v4_c4(r, D):
    m, n = r.choice([(1, 2), (2, 1), (1, 3), (2, 3)])
    t = Fr(m, m + n)
    intro = f'OABC is a parallelogram with OA = a and OC = c. M is the midpoint of AB. P lies on the diagonal OB such that OP : PB = {m} : {n}.'
    parts = [
        P('Find OB in terms of a and c.', 'a + c', 'B1', 1),
        P('Find OM in terms of a and c.', 'a + ½c', 'M1 OA + ½AB (AB = c); A1', 2),
        P('Find OP in terms of a and c.', vex((t, 'a'), (t, 'c')), f'M1 {frac(t)}OB; A1', 2),
        P('Find CM in terms of a and c.', vex((1, 'a'), (Fr(-1, 2), 'c')), 'M1 CO + OM; A1', 2),
        P(f'Given that a = (4, 0) and c = (2, 6), find |OB|.', n3(math.hypot(6, 6)), 'M1 OB = (6, 6); A1 √72 = 8.49', 2),
        P('Find CP in terms of a and c and hence state, with a reason, whether P lies on CM.', f'CP = {vex((t, "a"), (t - 1, "c"))}; ' + ('yes: CP = ⅔CM, a scalar multiple, so C, P and M are collinear.' if t == Fr(2, 3) else 'no: CP is not a scalar multiple of CM = a − ½c.'),
          'M1 CP = OP − OC; A1; B1 conclusion with reason', 3),
    ]
    return cmp_(r, intro, parts)


v4.add('C4', (2, 3, 4, 5))(v4_c4)
CHAPTERS[11] = [v1, v2, v3, v4]


# =========================================================== 12 Probability using tree diagrams and Venn diagrams (Ch 24)
BAGS = [('red', 'blue', 'counters', 'a bag'), ('green', 'yellow', 'sweets', 'a jar'), ('black', 'white', 'beads', 'a box'), ('milk', 'dark', 'chocolates', 'a tin'),
        ('orange', 'purple', 'marbles', 'a bag'), ('fiction', 'non-fiction', 'books', 'a shelf')]
EV = [('it rains on a given day in {c}', 'it does not rain'), ('the bus to school is late', 'the bus is on time'), ('a seed germinates', 'the seed does not germinate'),
      ('a penalty is scored', 'the penalty is missed'), ('a light bulb is faulty', 'the bulb works')]

p1 = topic('Tree diagrams for independent and dependent events', 'tree diagrams', 'independent and dependent events', 'tree diagram')
p1.fixed('C1', (1, 2), [
    ('On a tree diagram, to find the probability of a combined outcome along a path you should', 'multiply the probabilities along the branches', 'AND → multiply along the path.', ['add the probabilities along the branches', 'subtract the probabilities', 'divide the probabilities']),
    ('To find the probability that either of two separate outcomes happens on a tree diagram you should', 'add the probabilities of the paths', 'OR (mutually exclusive paths) → add.', ['multiply the probabilities of the paths', 'take the larger probability', 'subtract the smaller from the larger']),
    ('The probabilities on the branches from one point of a tree diagram', 'add up to 1', 'They cover all possible outcomes.', ['add up to 0', 'are always equal', 'multiply to 1']),
    ('A bag has 3 red and 2 blue counters. A counter is taken and not replaced. If the first is red, what is P(second is red)?', '2/4', '2 red left out of 4 counters.', ['3/5', '3/4', '2/5']),
    ('A fair coin is thrown twice. What is P(two heads)?', '1/4', '½ × ½ = ¼.', ['1/2', '1/3', '2/4 + 1/4']),
    ('Two events are independent if', 'the outcome of one does not affect the probability of the other', 'For example two throws of a die.', ['they cannot happen together', 'they have the same probability', 'one always follows the other']),
])
p1.fixed('C2', (2, 3), [
    ('Explain why the probabilities on the second branches change when counters are taken without replacement.', 'After the first counter is removed there are fewer counters in total and possibly fewer of that colour, so the probabilities for the second pick depend on the first.', 'B1 total decreases; B1 depends on first outcome (dependent) [2]'),
    ('Explain why P(at least one six in two throws of a die) is found by 1 − P(no sixes).', '"At least one six" includes several paths; the only other outcome is "no sixes", so it is quicker to subtract P(no sixes) = 25/36 from 1, giving 11/36.', 'B1 complement covers all other outcomes; B1 11/36 [2]'),
    ('Explain why P(one red and one blue) from two picks is the sum of two paths on a tree diagram.', 'It can happen as red then blue or blue then red; these are mutually exclusive, so their probabilities are added.', 'B1 two orders; B1 add [2]'),
])


@p1.add('C1', (1, 2, 3))
def p1_q(r, D):
    c1, c2, items, cont = r.choice(BAGS)
    a, b = r.randint(2, 7), r.randint(2, 7)
    n = a + b
    rep = D <= 2
    c = Fr(a, n) * (Fr(a, n) if rep else Fr(a - 1, n - 1))
    w = [Fr(a, n) * (Fr(a - 1, n - 1) if rep else Fr(a, n)), Fr(a, n) + Fr(a, n), Fr(a, n) * Fr(b, n), Fr(2 * a, 2 * n), Fr(a, n) ** 2 + Fr(1, n * n)]
    return SMC(r, f'{cont.capitalize()} contains {a} {c1} and {b} {c2} {items}. Two are taken at random {"with" if rep else "without"} replacement. What is the probability that both are {c1}?', frac(c), [frac(x) for x in w],
               f'{a}/{n} × {a if rep else a - 1}/{n if rep else n - 1} = {frac(c)}.')


@p1.add('C2', (2, 3, 4), 'explain')
def p1_err(r, D):
    c1, c2, items, cont = r.choice(BAGS)
    a, b = r.randint(3, 7), r.randint(2, 6)
    n = a + b
    nm = person(r)
    c = Fr(a, n) * Fr(a - 1, n - 1)
    if r.random() < 0.5:
        return Q(f'{cont.capitalize()} has {a} {c1} and {b} {c2} {items}. Two are taken without replacement. {nm} says P(both {c1}) = {a}/{n} × {a}/{n} = {frac(Fr(a * a, n * n))}. Explain the error and find the correct probability.',
                 f'Without replacement the second pick has {a - 1} {c1} out of {n - 1}: {a}/{n} × {a - 1}/{n - 1} = {frac(c)}.', f'B1 second probability changes; B1 {frac(c)} [2]')
    p = r.choice([Fr(1, 3), Fr(2, 5), Fr(1, 4), Fr(3, 10)])
    return Q(f'The probability that a {r.choice(["train", "ferry", "bus"])} is late on any day is {frac(p)}. {nm} says the probability that it is late on both of two days is {frac(p)} + {frac(p)} = {frac(2 * p)}. Explain the error and find the correct probability.',
             f'For both days (AND) the probabilities are multiplied: {frac(p)} × {frac(p)} = {frac(p * p)}.', f'B1 multiply for AND; B1 {frac(p * p)} [2]')


@p1.add('C3', (1, 2, 3, 4, 5))
def p1_calc(r, D):
    c1, c2, items, cont = r.choice(BAGS)
    a, b = r.randint(2, 8), r.randint(2, 8)
    n = a + b
    rep = D <= 2
    q = r.choice(['same', 'diff', 'atleast'])
    if rep:
        pa, pb = Fr(a, n), Fr(b, n)
        same, diff, al = pa * pa + pb * pb, 2 * pa * pb, 1 - pb * pb
    else:
        same = Fr(a, n) * Fr(a - 1, n - 1) + Fr(b, n) * Fr(b - 1, n - 1)
        diff = 2 * Fr(a, n) * Fr(b, n - 1)
        al = 1 - Fr(b, n) * Fr(b - 1, n - 1)
    v = {'same': same, 'diff': diff, 'atleast': al}[q]
    txt = {'same': 'both are the same colour', 'diff': f'one is {c1} and one is {c2}', 'atleast': f'at least one is {c1}'}[q]
    key = {'same': f'M1 P({c1}, {c1}) + P({c2}, {c2}); A1 {frac(v)}', 'diff': f'M1 P({c1}, {c2}) + P({c2}, {c1}); A1 {frac(v)}', 'atleast': f'M1 1 − P({c2}, {c2}); A1 {frac(v)}'}[q]
    if D == 1:
        return SMC(r, f'{cont.capitalize()} contains {a} {c1} and {b} {c2} {items}. One is taken at random, replaced, and a second is taken. What is the probability that {txt}?', frac(v),
                   list(dict.fromkeys(frac(x) for x in [v / 2, 1 - v, v + Fr(1, n * n), Fr(a, n), Fr(a * b, n * n), Fr(a + b - 1, n * n), v * v] if x != v and 0 < x < 1)), key)
    if D >= 4:
        e, ne = r.choice(EV)
        p = r.choice([Fr(1, 5), Fr(3, 10), Fr(2, 5), Fr(1, 4), Fr(3, 4), Fr(7, 10)])
        k = r.choice([2, 3])
        if k == 3:
            v2 = 3 * p * (1 - p) ** 2
            return Q(f'The probability that {e.format(c=city(r))} is {frac(p)}, independently each day. Calculate the probability that this happens on exactly one of three days.', frac(v2),
                     f'M1 p(1 − p)² = {frac(p * (1 - p) ** 2)}; M1 × 3 arrangements; A1 {frac(v2)}.')
        return Q(f'The probability that {e.format(c=city(r))} is {frac(p)}, independently each day. Calculate the probability that it happens on at least one of two days.', frac(1 - (1 - p) ** 2),
                 f'M1 1 − ({frac(1 - p)})²; A1 {frac(1 - (1 - p) ** 2)}.')
    return Q(f'{cont.capitalize()} contains {a} {c1} and {b} {c2} {items}. Two are taken at random {"with" if rep else "without"} replacement. Calculate the probability that {txt}.', frac(v), key + '.')


def p1_c4(r, D):
    c1, c2, items, cont = r.choice(BAGS)
    a, b = r.randint(3, 7), r.randint(2, 6)
    n = a + b
    nm = person(r)
    pAA = Fr(a, n) * Fr(a - 1, n - 1)
    pBB = Fr(b, n) * Fr(b - 1, n - 1)
    pAB = Fr(a, n) * Fr(b, n - 1)
    p3 = Fr(a, n) * Fr(a - 1, n - 1) * Fr(a - 2, n - 2)
    intro = f'{cont.capitalize()} contains {a} {c1} and {b} {c2} {items}. {nm} takes two at random without replacement.'
    parts = [
        P('Write down the probabilities on the branches of a tree diagram for the second pick, after a first pick that is ' + c1 + '.', f'{c1}: {a - 1}/{n - 1}, {c2}: {b}/{n - 1}', 'B1 B1', 2),
        P(f'Calculate the probability that both are {c2}.', frac(pBB), f'M1 {b}/{n} × {b - 1}/{n - 1}; A1', 2),
        P('Calculate the probability that the two are different colours.', frac(2 * pAB), 'M1 two paths; M1 add; A1', 3),
        P(f'Calculate the probability that at least one is {c1}.', frac(1 - pBB), 'M1 1 − P(both ' + c2 + '); A1', 2),
        P(f'{nm} now takes a third without replacement. Calculate the probability that all three are {c1}.', frac(p3), f'M1 {a}/{n} × {a - 1}/{n - 1} × {a - 2}/{n - 2}; A1', 2),
    ]
    return cmp_(r, intro, parts)


def p1_c4b(r, D):
    e, ne = r.choice(EV)
    p = r.choice([Fr(1, 5), Fr(3, 10), Fr(2, 5), Fr(1, 4)])
    q1 = r.choice([Fr(3, 5), Fr(7, 10), Fr(1, 2)])
    q2 = r.choice([Fr(1, 5), Fr(1, 10), Fr(1, 4)])
    c = city(r)
    nm = person(r)
    late = p * q1 + (1 - p) * q2
    intro = f'On a school day in {c}, the probability that it rains is {frac(p)}. If it rains, the probability that {nm} is late for school is {frac(q1)}. If it does not rain, the probability that {nm} is late is {frac(q2)}.'
    parts = [
        P('Calculate the probability that it rains and ' + nm + ' is late.', frac(p * q1), 'M1 multiply; A1', 2),
        P(f'Calculate the probability that {nm} is late.', frac(late), f'M1 {frac(p)} × {frac(q1)} + {frac(1 - p)} × {frac(q2)}; A1', 3),
        P(f'Calculate the probability that {nm} is on time on two days, assuming the days are independent.', f'{frac((1 - late) ** 2)} ≈ {n3(float((1 - late) ** 2))}', 'M1 (1 − P(late))²; A1', 2),
        P('Explain why being late and rain are not independent events here.', f'The probability of being late changes depending on whether it rains ({frac(q1)} vs {frac(q2)}).', 'B1', 1),
    ]
    return cmp_(r, intro, parts)


p1.add('C4', (2, 3, 4, 5))(p1_c4)
p1.add('C4', (2, 3, 4, 5))(p1_c4b)

# ---------------------------------------------------------------- Venn diagrams
VCTX = [('study French', 'study Spanish', 'students in a year group'), ('own a cat', 'own a dog', 'families in a street'), ('play football', 'play basketball', 'members of a sports club'),
        ('like tea', 'like coffee', 'office workers'), ('have visited Kenya', 'have visited Peru', 'members of a travel club'), ('take the bus', 'cycle', 'students')]


def venn(r, D):
    n = r.choice([30, 40, 50, 60, 80, 100, 120])
    x = r.randint(2, n // 6)
    oa, ob = r.randint(3, n // 3), r.randint(3, n // 3)
    ne = n - x - oa - ob
    if ne < 2:
        ob = max(2, ob + ne - 3)
        ne = n - x - oa - ob
    if ne < 1:
        raise ValueError('venn')
    return n, oa, x, ob, ne


q5 = topic('Venn diagrams and probability', 'venn diagrams and probability', 'venn diagrams', 'set notation')
q5.fixed('C1', (1, 2), [
    ('What does A ∩ B mean?', 'The elements in both A and B', 'Intersection: in A and in B.', ['The elements in A or B or both', 'The elements not in A', 'The number of elements in A']),
    ('What does A ∪ B mean?', 'The elements in A or B or both', 'Union: in at least one of the sets.', ['The elements in both A and B only', 'The elements in neither set', 'The elements in A but not B']),
    ('What does A′ mean?', 'The elements not in A', 'Complement of A within the universal set.', ['The elements in A only', 'The number of elements in A', 'The elements in both A and B']),
    ('n(A) = 12, n(B) = 9 and n(A ∩ B) = 4. What is n(A ∪ B)?', '17', '12 + 9 − 4 = 17.', ['21', '25', '13']),
    ('What does ξ represent in a Venn diagram?', 'The universal set', 'ξ contains every element being considered.', ['The empty set', 'The intersection', 'The complement']),
    ('Which symbol means "is an element of"?', '∈', 'x ∈ A means x is in A.', ['⊂', '∩', '∪']),
])
q5.fixed('C2', (2, 3), [
    ('Explain why n(A ∪ B) is not always equal to n(A) + n(B).', 'Elements in both A and B would be counted twice, so n(A ∩ B) must be subtracted: n(A ∪ B) = n(A) + n(B) − n(A ∩ B).', 'B1 double counting; B1 formula [2]'),
    ('Explain what it means for two sets to be disjoint and how this appears on a Venn diagram.', 'They have no elements in common (A ∩ B = ∅); the circles do not overlap.', 'B1 no common elements; B1 non-overlapping circles [2]'),
    ('Describe the region A ∩ B′ on a Venn diagram.', 'The part of circle A that is outside circle B, i.e. elements in A only.', 'B1 inside A; B1 outside B [2]'),
])


@q5.add('C1', (1, 2, 3))
def q5_q(r, D):
    n, oa, x, ob, ne = venn(r, D)
    A, B, who = r.choice(VCTX)
    q = r.choice(['union', 'onlyA', 'neither'])
    v = {'union': oa + x + ob, 'onlyA': oa, 'neither': ne}[q]
    ask = {'union': f'{A} or {B} (or both)', 'onlyA': f'{A} but not {B}', 'neither': 'do neither'}[q]
    stem = f'In a group of {n} {who}, {oa + x} {A}, {ob + x} {B} and {x} do both. How many {ask}?'
    return MC(r, stem, v, [oa + x + ob + x, oa + x, n - oa - ob, ne + x, v + 1], f'Regions: only first {oa}, both {x}, only second {ob}, neither {ne}; answer {v}.')


@q5.add('C2', (2, 3, 4), 'explain')
def q5_err(r, D):
    n, oa, x, ob, ne = venn(r, D)
    A, B, who = r.choice(VCTX)
    nm = person(r)
    return Q(f'In a group of {n} {who}, {oa + x} {A} and {ob + x} {B}; {x} do both. {nm} says {oa + x} + {ob + x} = {oa + ob + 2 * x} people {A} or {B}. Explain the error and find the correct number.',
             f'The {x} who do both have been counted twice. n(A ∪ B) = {oa + x} + {ob + x} − {x} = {oa + ob + x}.', f'B1 double counting; B1 {oa + ob + x} [2]')


@q5.add('C3', (1, 2, 3, 4, 5))
def q5_calc(r, D):
    n, oa, x, ob, ne = venn(r, D)
    A, B, who = r.choice(VCTX)
    if D <= 2:
        q = r.choice([('P(A ∩ B)', x), ('P(A ∪ B)', oa + x + ob), ('P(A′)', ob + ne), ('P(A ∩ B′)', oa)])
        return Q(f'ξ = {{{who}}}, n(ξ) = {n}, A = {{those who {A}}}, B = {{those who {B}}}. n(A) = {oa + x}, n(B) = {ob + x}, n(A ∩ B) = {x}. A person is chosen at random. Find {q[0]}.', frac(Fr(q[1], n)),
                 f'M1 completes Venn regions ({oa}, {x}, {ob}, {ne}); A1 {q[1]}/{n} = {frac(Fr(q[1], n))}.')
    if D == 3:
        return Q(f'In a survey of {n} {who}, {oa + x} {A}, {ob + x} {B} and {ne} do neither. Find the number who do both, and the probability that a person chosen at random does exactly one of the two.', f'{x}; {frac(Fr(oa + ob, n))}',
                 f'M1 {oa + x} + {ob + x} − x + {ne} = {n}; A1 x = {x}; M1 ({oa} + {ob}) ÷ {n}; A1 {frac(Fr(oa + ob, n))}.')
    k = r.choice([2, 3])
    # n(A only) = k * x , n(B only) = x + d ; unknown x
    d = r.randint(1, 6)
    x2 = r.randint(3, 9)
    ne2 = r.randint(2, 10)
    tot = k * x2 + x2 + x2 + d + ne2
    return Q(f'A Venn diagram for {tot} {who} has these regions: {A} only: {k}x; both: x; {B} only: x + {d}; neither: {ne2}. Find x. A person is chosen at random from those who {B}. Find the probability that they also {A}.',
             f'x = {x2}; {frac(Fr(x2, 2 * x2 + d))}', f'M1 {k + 2}x + {d + ne2} = {tot}; A1 x = {x2}; M1 n(B) = {2 * x2 + d}; A1 {x2}/{2 * x2 + d} = {frac(Fr(x2, 2 * x2 + d))}.')


def q5_c4(r, D):
    A, B, who = r.choice(VCTX)
    n = r.choice([50, 60, 80, 100])
    x = r.randint(4, 10)
    oa = r.randint(6, 15)
    ob = r.randint(5, 14)
    ne = n - oa - ob - x
    nm = person(r)
    intro = f'{nm} surveys {n} {who} in {city(r)}. {oa + x} {A}, {ob + x} {B} and {ne} do neither. A = {{{who} who {A}}}, B = {{{who} who {B}}}.'
    parts = [
        P('Find the number who do both and complete a Venn diagram.', f'{x}; regions {oa}, {x}, {ob}, {ne}', f'M1 {oa + x} + {ob + x} − x + {ne} = {n}; A1 x = {x}; B1 regions', 3),
        P(f'Find the probability that a person chosen at random is in the “{A}” group but not the “{B}” group.', frac(Fr(oa, n)), 'B1', 1),
        P('Find n(A′ ∩ B′).', f'{ne}', 'B1', 1),
        P('Find P(A ∪ B).', frac(Fr(oa + x + ob, n)), 'B1', 1),
        P('Two people are chosen at random without replacement. Find the probability that both do neither.', frac(Fr(ne, n) * Fr(ne - 1, n - 1)), f'M1 {ne}/{n} × {ne - 1}/{n - 1}; A1', 2),
        P('Given that a person is in B, find the probability that they are also in A.', frac(Fr(x, ob + x)), f'M1 {x}/{ob + x}; A1', 2),
    ]
    return cmp_(r, intro, parts)


q5.add('C4', (2, 3, 4, 5))(q5_c4)

# ---------------------------------------------------------------- conditional probability
p3 = topic('Conditional probability', 'conditional probability', 'given that', 'conditional')
p3.fixed('C1', (1, 2), [
    ('P(A | B) means', 'the probability of A given that B has happened', 'Conditional probability: B is known to have occurred.', ['the probability of A and B', 'the probability of A or B', 'the probability of B given A']),
    ('Which formula gives P(A | B)?', 'P(A ∩ B) ÷ P(B)', 'Restrict to outcomes in B.', ['P(A ∩ B) ÷ P(A)', 'P(A) × P(B)', 'P(A) + P(B)']),
    ('In a class of 30, 12 are girls and 4 girls wear glasses. A girl is chosen at random. What is P(wears glasses)?', '4/12', 'Only the 12 girls are considered.', ['4/30', '12/30', '4/26']),
    ('If A and B are independent, then P(A | B) is equal to', 'P(A)', 'B happening does not change the probability of A.', ['P(B)', 'P(A ∩ B)', '1']),
])
p3.fixed('C2', (2, 3), [
    ('Explain the difference between P(A | B) and P(A ∩ B).', 'P(A ∩ B) is the probability that both happen, out of all outcomes; P(A | B) is the probability of A among only the outcomes where B happens.', 'B1 both out of all; B1 restricted to B [2]'),
    ('Explain why P(A | B) is usually not equal to P(B | A).', 'They use different restricted groups: P(A | B) divides by P(B), P(B | A) divides by P(A); these are only equal if P(A) = P(B).', 'B1 different denominators; B1 condition [2]'),
    ('Explain how a two-way table can be used to find a conditional probability.', 'Use only the row (or column) for the given condition: divide the number in the required cell by the total of that row or column.', 'B1 restrict to row/column; B1 divide by that total [2]'),
])


def two_way(r):
    rows, cols = r.choice([(('Year 10 students', 'Year 11 students'), ('walking', 'bus', 'car')), (('boys', 'girls'), ('football', 'tennis', 'swimming')), (('adults', 'children'), ('morning', 'afternoon', 'evening')),
                           (('locals', 'tourists'), ('museum', 'beach', 'market'))])
    t = [[r.randint(4, 30) for _ in cols] for _ in rows]
    return rows, cols, t


def rowph(row):
    if row.startswith('Year'):
        return f'in {row}'
    return f'one of the {row}' if row.endswith('s') else art(row)


def tw_text(rows, cols, t):
    return '; '.join(f'{rw}: ' + ', '.join(f'{c} {v}' for c, v in zip(cols, t[i])) for i, rw in enumerate(rows))


@p3.add('C1', (1, 2, 3))
def p3_q(r, D):
    rows, cols, t = two_way(r)
    i, j = r.randrange(2), r.randrange(3)
    rt = sum(t[i])
    tot = sum(map(sum, t))
    ct = t[0][j] + t[1][j]
    c = frac(Fr(t[i][j], rt))
    return SMC(r, f'A survey in {city(r)} gives these counts: {tw_text(rows, cols, t)}. A person is chosen at random from the {rows[i]}. What is the probability that they chose {cols[j]}?', c,
               [frac(Fr(t[i][j], tot)), frac(Fr(t[i][j], ct)), frac(Fr(rt, tot)), frac(Fr(ct, tot)), frac(Fr(t[i][j], rt + 1))], f'{t[i][j]} out of the {rt} {rows[i]}: {c}.')


@p3.add('C2', (2, 3, 4), 'explain')
def p3_err(r, D):
    rows, cols, t = two_way(r)
    i, j = r.randrange(2), r.randrange(3)
    rt = sum(t[i])
    tot = sum(map(sum, t))
    nm = person(r)
    return Q(f'A survey gives {tw_text(rows, cols, t)}. {nm} wants the probability that a person chose {cols[j]}, given that they are {rowph(rows[i])}, and writes {t[i][j]}/{tot}. Explain the error and give the correct probability.',
             f'"Given that" restricts the choice to the {rt} {rows[i]}, so the probability is {t[i][j]}/{rt} = {frac(Fr(t[i][j], rt))}.', f'B1 restricted total {rt}; B1 {frac(Fr(t[i][j], rt))} [2]')


@p3.add('C3', (2, 3, 4, 5))
def p3_calc(r, D):
    kind = r.choice(['table', 'venn', 'tree', 'formula'])
    if kind == 'table':
        rows, cols, t = two_way(r)
        j = r.randrange(3)
        i = r.randrange(2)
        ct = t[0][j] + t[1][j]
        return Q(f'The table shows the results of a survey: {tw_text(rows, cols, t)}. A person who chose {cols[j]} is selected at random. Find the probability that they are {rowph(rows[i])}.', frac(Fr(t[i][j], ct)),
                 f'M1 column total {ct}; A1 {t[i][j]}/{ct} = {frac(Fr(t[i][j], ct))}.')
    if kind == 'venn':
        n, oa, x, ob, ne = venn(r, D)
        A, B, who = r.choice(VCTX)
        return Q(f'Of {n} {who}, {oa + x} {A}, {ob + x} {B} and {x} do both. A person is chosen at random from those who {A}. Find the probability that they also {B}.', frac(Fr(x, oa + x)),
                 f'M1 restrict to n(A) = {oa + x}; A1 {x}/{oa + x} = {frac(Fr(x, oa + x))}.')
    if kind == 'tree':
        c1, c2, items, cont = r.choice(BAGS)
        a, b = r.randint(3, 7), r.randint(2, 6)
        n = a + b
        pAA = Fr(a, n) * Fr(a - 1, n - 1)
        pBB = Fr(b, n) * Fr(b - 1, n - 1)
        same = pAA + pBB
        return Q(f'{cont.capitalize()} contains {a} {c1} and {b} {c2} {items}. Two are taken at random without replacement. Given that both are the same colour, find the probability that both are {c1}.', frac(pAA / same),
                 f'M1 P(both {c1}) = {frac(pAA)}; M1 P(same) = {frac(same)}; M1 divide; A1 {frac(pAA / same)}.')
    pa = r.choice([Fr(2, 5), Fr(1, 2), Fr(3, 5), Fr(7, 10)])
    pab = pa * r.choice([Fr(1, 3), Fr(1, 2), Fr(1, 4)])
    return Q(f'P(A) = {frac(pa)} and P(A ∩ B) = {frac(pab)}. Find P(B | A).', frac(pab / pa), f'M1 P(A ∩ B) ÷ P(A); A1 {frac(pab / pa)}.')


def p3_c4(r, D):
    prev = r.choice([Fr(1, 50), Fr(1, 20), Fr(1, 25), Fr(1, 10)])
    sens = r.choice([Fr(9, 10), Fr(19, 20), Fr(4, 5)])
    fp = r.choice([Fr(1, 10), Fr(1, 20), Fr(3, 50)])
    pos = prev * sens + (1 - prev) * fp
    intro = f'A screening test for a disease is used in {city(r)}. {frac(prev)} of the people tested have the disease. If a person has the disease, the probability of a positive test is {frac(sens)}. If a person does not have the disease, the probability of a positive test is {frac(fp)}.'
    parts = [
        P('Calculate the probability that a randomly chosen person has the disease and tests positive.', frac(prev * sens), 'M1 multiply; A1', 2),
        P('Calculate the probability that a randomly chosen person tests positive.', frac(pos), f'M1 {frac(prev)} × {frac(sens)} + {frac(1 - prev)} × {frac(fp)}; A1', 3),
        P('Given that a person tests positive, calculate the probability that they have the disease.', f'{frac(prev * sens / pos)} ≈ {n3(float(prev * sens / pos))}', 'M1 P(disease ∩ positive) ÷ P(positive); A1', 2),
        P('Comment on how likely it is that a person who tests positive actually has the disease.', 'Most positive results are false positives, because the disease is rare; a second test would be needed.', 'B1', 1),
        P(f'In a group of 1000 people, estimate how many would test positive.', ex(float(pos * 1000)), 'M1 × 1000; A1', 2),
    ]
    return cmp_(r, intro, parts)


p3.add('C4', (2, 3, 4, 5))(p3_c4)
CHAPTERS[12] = [p1, q5, p3]


# ---------------------------------------------------------------- robustness wrapper
# A parameterised draw can occasionally hit a degenerate case (e.g. too few distinct MCQ
# distractors). Retry with the same generator (whose state has advanced) before giving up.
def _key_marks(key):
    m = re.findall(r'\[(\d+)\]', key)
    if m:
        return sum(int(x) for x in m)
    m = re.findall(r'\b[MAB](\d)\b', key)
    return sum(int(x) for x in m)


def _with_marks(q):
    # Make the marks field agree with the marks shown in the marking key.
    if q and 'marks' not in q and not q.get('options'):
        k = _key_marks(q.get('key', ''))
        if k:
            q['marks'] = max(1, min(20, k))
    return q


def _robust(fn):
    def g(r, D):
        err = None
        for _ in range(12):
            try:
                q = fn(r, D)
                if q:
                    return _with_marks(q)
            except (ValueError, ZeroDivisionError, IndexError) as e:
                err = e
        if err:
            raise err
        return None
    g.__name__ = fn.__name__
    return g


for _tps in CHAPTERS.values():
    for _tp in _tps:
        for _t in _tp.templates:
            object.__setattr__(_t, 'fn', _robust(_t.fn))
