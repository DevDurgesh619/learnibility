"""CBSE class 11 Geography: computed question families (practical work and physical geography numbers).

Used through g12_hum_engine's `extra` hook: EXTRA maps a subtopic id to a list of qbank Family objects.
Every answer is computed from the numbers in the stem: scale conversion (1 km = 100,000 cm, 1 mile = 63,360 in),
map and ground distance, graphical scale, local time (4 minutes per degree), IST (82°30' E = GMT + 5:30),
cylindrical equal area construction (2πR, R sin φ), gradient, Survey of India sheets, pixel counts,
normal lapse rate (6.5°C per 1,000 m), pressure fall with height (about 1 mb per 10 m), relative humidity,
salinity (parts per thousand) and the heat budget (NCERT figures: 35 / 14 / 51; 17 + 34; 48).
"""
from __future__ import annotations

import math

from qbank import F, num, num_distractors, mcq

S = 'cbse-g11-geography-ch'
PLACES = ['Place A', 'Place B', 'Place C', 'Place D', 'Place E', 'Station P', 'Station Q', 'Station R']


def _fmt(n: int) -> str:
    return f'{n:,}'


# ---------------------------------------------------------------- map scale (ch19)

KM_RF = [(1, 0.5), (1, 1), (1, 2), (1, 2.5), (1, 4), (1, 5), (1, 10), (2, 5), (1, 0.25), (1, 20), (1, 25), (1, 50), (1, 0.1)]


def stmt_to_rf(r):
    cm, km = r.choice(KM_RF)
    den = int(round(km * 100000 / cm))
    stem = f"Convert the statement of scale '{num(cm)} cm represents {num(km)} km' into a representative fraction."
    wrong = [f'1:{_fmt(x)}' for x in dict.fromkeys([den // 10, den * 10, int(km * 1000 / cm), den // 100 or 7]) if x != den]
    return mcq(stem, f'1:{_fmt(den)}', wrong, f'{num(km)} km = {_fmt(int(km * 100000))} cm, so RF = {num(cm)}:{_fmt(int(km * 100000))} = 1:{_fmt(den)}.', r)


def rf_to_stmt(r):
    den = r.choice([10000, 20000, 25000, 40000, 50000, 100000, 125000, 200000, 250000, 500000, 1000000, 5000000])
    km = den / 100000
    stem = f'Convert the representative fraction 1:{_fmt(den)} into a statement of scale in the metric system.'
    c = f'1 cm represents {num(km, 3)} km'
    wrong = [f'1 cm represents {num(x, 3)} km' for x in dict.fromkeys([km * 10, km / 10, km * 100, den / 1000]) if num(x, 3) != num(km, 3)]
    return mcq(stem, c, wrong, f'1 cm represents {_fmt(den)} cm = {_fmt(den)} ÷ 100,000 km = {num(km, 3)} km.', r)


def inch_to_rf(r):
    inch, miles = r.choice([(1, 1), (1, 2), (1, 4), (1, 8), (2, 1), (1, 16), (1, 10), (1, 5)])
    den = miles * 63360 // inch
    stem = f"Convert the statement '{inch} inch{'es' if inch > 1 else ''} represent{'' if inch > 1 else 's'} {miles} mile{'s' if miles > 1 else ''}' into a representative fraction."
    wrong = [f'1:{_fmt(x)}' for x in dict.fromkeys([miles * 100000 // inch, miles * 1760 // inch, miles * 5280 // inch, den * 2]) if x != den]
    return mcq(stem, f'1:{_fmt(den)}', wrong, f'1 mile = 63,360 inches, so {miles} mile(s) = {_fmt(miles * 63360)} inches; RF = 1:{_fmt(den)}.', r)


def map_to_ground(r):
    den = r.choice([25000, 50000, 100000, 200000, 250000, 500000, 1000000])
    d = r.choice([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 12])
    km = d * den / 100000
    stem = f'On a map with RF 1:{_fmt(den)}, the distance between two towns is {num(d)} cm. What is the actual ground distance?'
    wrong = num_distractors(km, km * 10, km / 10, d * den / 1000, km + d, dp=3)
    return mcq(stem, f'{num(km, 3)} km', [f'{w} km' for w in wrong], f'Ground distance = {num(d)} × {_fmt(den)} cm = {_fmt(int(d * den))} cm = {num(km, 3)} km.', r)


def ground_to_map(r):
    den = r.choice([50000, 100000, 200000, 250000, 500000, 1000000])
    cm = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    km = cm * den / 100000
    stem = f'Two places are {num(km, 3)} km apart on the ground. What will be the distance between them on a map of scale 1:{_fmt(den)}?'
    wrong = num_distractors(cm, cm * 10, cm / 10, km, cm * 2, dp=2)
    return mcq(stem, f'{num(cm)} cm', [f'{w} cm' for w in wrong], f'{num(km, 3)} km = {_fmt(int(km * 100000))} cm; map distance = {_fmt(int(km * 100000))} ÷ {_fmt(den)} = {num(cm)} cm.', r)


def scale_convert_long(r):
    cm, km = r.choice([(1, 5), (1, 2), (2, 5), (1, 10), (1, 4), (1, 25), (1, 0.5)])
    den = int(round(km * 100000 / cm))
    m2 = r.choice([2, 3, 4, 5, 6])
    gd = m2 * km / cm
    return {'stem': f"A map has the scale '{num(cm)} cm represents {num(km)} km'. (a) Express it as a representative fraction. "
                    f'(b) Find the ground distance between two points that are {m2} cm apart on this map.',
            'answer': f'(a) {num(km)} km = {_fmt(int(km * 100000))} cm, so RF = 1:{_fmt(den)}. (b) {m2} cm × {_fmt(den)} = {_fmt(int(m2 * den))} cm = {num(gd)} km.',
            'key': f'3 marks: (a) 2 – converting {num(km)} km to {_fmt(int(km * 100000))} cm and RF 1:{_fmt(den)}; (b) 1 – {num(gd)} km.',
            'marks': 3, 'minutes': 5}


def rf_english_long(r):
    den = r.choice([63360, 126720, 253440, 31680, 633600])
    miles = den / 63360
    km = den / 100000
    return {'stem': f'Convert the RF 1:{_fmt(den)} into a statement of scale in (a) the English system and (b) the metric system.',
            'answer': f'(a) 1 inch represents {_fmt(den)} inches = {_fmt(den)} ÷ 63,360 = {num(miles)} mile(s). '
                      f'(b) 1 cm represents {_fmt(den)} cm = {_fmt(den)} ÷ 100,000 = {num(km, 4)} km.',
            'key': f'3 marks: (a) 1½ – {num(miles)} mile(s) per inch using 1 mile = 63,360 inches; (b) 1½ – {num(km, 4)} km per cm using 1 km = 100,000 cm.',
            'marks': 3, 'minutes': 5}


def graphical_scale(r):
    den, total_km, prim = r.choice([(50000, 7, 1), (100000, 15, 3), (250000, 30, 5), (200000, 25, 5), (500000, 60, 10),
                                   (1000000, 120, 20), (25000, 3, 0.5), (125000, 15, 3)])
    cm_total = total_km * 100000 / den
    ndiv = int(round(total_km / prim))
    cm_div = prim * 100000 / den
    return {'stem': f'Construct a graphical scale for a map with RF 1:{_fmt(den)} to read kilometres. '
                    'State the length of the line, the number of primary divisions and the value and length of each division.',
            'answer': f'Choose a line of about 12–15 cm. 1 cm = {num(den / 100000, 3)} km, so a line of {num(cm_total, 2)} cm represents {num(total_km)} km. '
                      f'Divide it into {ndiv} primary divisions of {num(prim)} km each ({num(cm_div, 2)} cm each); subdivide the first primary division '
                      'into secondary divisions to the left of zero.',
            'key': f'3 marks: 1 for the length ({num(cm_total, 2)} cm for {num(total_km)} km), 1 for primary divisions ({ndiv} × {num(prim)} km), '
                   '1 for secondary divisions to the left of zero and labelling.',
            'marks': 3, 'minutes': 6}


# ---------------------------------------------------------------- time (ch20, ch13)

def _hm(minutes: int) -> str:
    h, m = divmod(minutes, 60)
    parts = []
    if h:
        parts.append(f'{h} hour{"s" if h != 1 else ""}')
    if m:
        parts.append(f'{m} minute{"s" if m != 1 else ""}')
    return ' '.join(parts) or '0 minutes'


def _clock(minutes: int) -> str:
    minutes %= 24 * 60
    h, m = divmod(minutes, 60)
    ap = 'a.m.' if h < 12 else 'p.m.'
    h12 = h % 12 or 12
    return f'{h12}:{m:02d} {ap}'


def time_diff(r):
    a = r.choice(range(0, 150, 5))
    b = a + r.choice([10, 15, 20, 25, 30, 37, 45, 60, 75, 90])
    da, db = r.choice(['E', 'W']), None
    db = da
    d = (b - a) * 4
    stem = f'What is the difference in local time between two places located at {a}° {da} and {b}° {db}?'
    wrong = [_hm(x) for x in dict.fromkeys([(b - a) * 15, (b - a), (b - a) * 2, d + 60]) if x != d and x > 0]
    return mcq(stem, _hm(d), wrong, f'Difference in longitude = {b - a}°; time = {b - a} × 4 minutes = {d} minutes = {_hm(d)}.', r)


def local_time(r):
    lon = r.choice(range(15, 165, 5)) + r.choice([0, 0, 0.5])
    side = r.choice(['E', 'W'])
    g = r.choice([0, 6, 8, 9, 10, 12, 14, 15, 18]) * 60
    diff = int(lon * 4)
    lt = g + diff if side == 'E' else g - diff
    lon_s = f"{int(lon)}°{' 30′' if lon % 1 else ''} {side}"
    stem = f'When it is {_clock(g)} at Greenwich (0°), what is the local time at a place located at {lon_s}?'
    wrongs = [_clock(g - diff if side == 'E' else g + diff), _clock(g + (diff // 4 if side == 'E' else -diff // 4)), _clock(lt + 60), _clock(lt - 60)]
    wrong = [w for w in dict.fromkeys(wrongs) if w != _clock(lt)]
    return mcq(stem, _clock(lt), wrong,
               f'{lon_s} is {num(lon)}° × 4 = {diff} minutes ({_hm(diff)}) {"ahead of" if side == "E" else "behind"} Greenwich, so local time = {_clock(lt)}'
               f'{" (previous day)" if lt < 0 else " (next day)" if lt >= 1440 else ""}.', r)


def ist_from_gmt(r):
    g = r.choice(range(0, 24 * 60, 30))
    ist = g + 330
    stem = f'When it is {_clock(g)} GMT, what is the Indian Standard Time?'
    wrong = [w for w in dict.fromkeys([_clock(g - 330), _clock(g + 300), _clock(g + 360), _clock(g + 270)]) if w != _clock(ist)]
    return mcq(stem, _clock(ist), wrong, f'IST is based on 82°30′ E: 82.5 × 4 = 330 minutes = 5 hours 30 minutes ahead of GMT, so IST = {_clock(ist)}'
               f'{" (next day)" if ist >= 1440 else ""}.', r)


def local_time_long(r):
    a = r.choice(range(60, 100, 5)) + r.choice([0, 0.5])
    b = r.choice(range(0, 60, 5))
    t = r.choice(range(6, 18)) * 60
    side_b = r.choice(['E', 'W'])
    diff_deg = a - b if side_b == 'E' else a + b
    diff = int(round(diff_deg * 4))
    lt = t - diff
    a_s = f"{int(a)}°{' 30′' if a % 1 else ''} E"
    return {'stem': f'The local time at a place X at {a_s} is {_clock(t)}. Calculate the local time at a place Y at {b}° {side_b}. Show your working.',
            'answer': f'Difference in longitude = {num(diff_deg)}°; time difference = {num(diff_deg)} × 4 = {diff} minutes ({_hm(diff)}). '
                      f'Y lies to the west of X, so its time is behind: {_clock(t)} − {_hm(diff)} = {_clock(lt)}{" (previous day)" if lt < 0 else ""}.',
            'key': f'3 marks: 1 for difference in longitude ({num(diff_deg)}°), 1 for time difference ({_hm(diff)} at 4 minutes per degree), '
                   f'1 for subtracting because Y is to the west ({_clock(lt)}).',
            'marks': 3, 'minutes': 5}


def idl_item(r):
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    i = r.randrange(7)
    west = r.choice([True, False])
    j = (i + 1) % 7 if west else (i - 1) % 7
    direction = 'from east to west (for example, from the USA towards Japan)' if west else 'from west to east (for example, from Japan towards the USA)'
    stem = f'A ship crosses the International Date Line {direction} on a {days[i]}. What day will it be on the other side of the line?'
    wrong = [d for d in dict.fromkeys([days[(i - 1) % 7] if west else days[(i + 1) % 7], days[i], days[(i + 2) % 7] if west else days[(i - 2) % 7]]) if d != days[j]]
    return mcq(stem, days[j], wrong, f'Crossing the Date Line {"westwards a day is gained (date advances)" if west else "eastwards a day is repeated (date goes back)"}: {days[j]}.', r)


# ---------------------------------------------------------------- projection (ch21)

def cea_long(r):
    den = r.choice([150000000, 200000000, 250000000, 300000000, 400000000])
    R = 640000000 / den
    step = r.choice([15, 30])
    lats = list(range(step, 91, step))
    eq = 2 * math.pi * R
    rows = '; '.join(f'{la}°: {num(R * math.sin(math.radians(la)), 2)} cm' for la in lats)
    return {'stem': f'Construct a cylindrical equal area projection for the world on a scale of 1:{_fmt(den)} with a parallel interval of {step}° '
                    '(earth radius 640,000,000 cm, π = 3.14). Calculate the radius of the reduced earth, the length of the equator '
                    'and the distance of each parallel from the equator.',
            'answer': f'R = 640,000,000 ÷ {_fmt(den)} = {num(R, 2)} cm. Equator = 2πR = 2 × 3.14 × {num(R, 2)} = {num(2 * 3.14 * R, 2)} cm. '
                      f'Distance of parallel from equator = R sin φ: {rows}. Meridians are equally spaced along the equator.',
            'key': '3 marks: 1 for R, 1 for the length of the equator (2πR), 1 for R sin φ distances of the parallels.',
            'marks': 3, 'minutes': 8}


def cea_mcq(r):
    den = r.choice([100000000, 160000000, 200000000, 320000000, 250000000])
    R = 640000000 / den
    la = r.choice([30, 60, 90])
    d = R * math.sin(math.radians(la))
    stem = (f'In a cylindrical equal area projection on a scale of 1:{_fmt(den)} (earth radius 640,000,000 cm), how far from the equator '
            f'is the {la}° parallel drawn?')
    wrong = num_distractors(d, R * math.cos(math.radians(la)) if la != 90 else R / 2, R * la / 90, 2 * d, R * math.tan(math.radians(min(la, 60))), dp=2)
    return mcq(stem, f'{num(d, 2)} cm', [f'{w} cm' for w in wrong], f'R = 640,000,000 ÷ {_fmt(den)} = {num(R, 2)} cm; distance = R sin {la}° = {num(d, 2)} cm.', r)


def equator_len(r):
    den = r.choice([100000000, 160000000, 200000000, 250000000, 320000000])
    R = 640000000 / den
    L = 2 * 3.14 * R
    stem = f'On a scale of 1:{_fmt(den)} (earth radius 640,000,000 cm, π = 3.14), what is the length of the equator in a cylindrical projection?'
    wrong = num_distractors(L, 3.14 * R, 2 * R, 3.14 * R * R, L * 2, dp=2)
    return mcq(stem, f'{num(L, 2)} cm', [f'{w} cm' for w in wrong], f'R = {num(R, 2)} cm; equator = 2πR = 2 × 3.14 × {num(R, 2)} = {num(L, 2)} cm.', r)


# ---------------------------------------------------------------- topographical maps (ch22)

def gradient_mcq(r):
    ci = r.choice([10, 20, 25, 50, 100])
    n = r.choice([2, 3, 4, 5, 6, 8])
    vi = ci * n
    he = vi * r.choice([5, 10, 20, 25, 40, 50])
    g = he // vi
    stem = (f'On a topographical map with a contour interval of {ci} m, a road crosses {n} contour intervals (from {ci * 2} m to {ci * 2 + vi} m) '
            f'over a horizontal distance of {_fmt(he)} m. What is its gradient?')
    wrong = [f'1 in {x}' for x in dict.fromkeys([he // ci, g * 2, max(2, g // 2), he // 100]) if x != g]
    return mcq(stem, f'1 in {g}', wrong, f'Vertical interval = {n} × {ci} = {vi} m; gradient = VI ÷ HE = {vi} ÷ {_fmt(he)} = 1 in {g}.', r)


def gradient_long(r):
    den = r.choice([50000, 25000, 63360])
    unit = 'cm' if den != 63360 else 'inch'
    d = r.choice([2, 3, 4, 5, 6])
    h1 = r.choice(range(100, 400, 20))
    vi = r.choice([100, 150, 200, 250, 300])
    he_m = d * den / 100 if unit == 'cm' else d * den * 0.0254
    g = he_m / vi
    return {'stem': f'On a topographical map of scale 1:{_fmt(den)}, point A has a spot height of {h1} m and point B of {h1 + vi} m. '
                    f'The map distance between them is {d} {unit}{"es" if unit == "inch" and d > 1 else ""}. Calculate the gradient between A and B.',
            'answer': f'VI = {h1 + vi} − {h1} = {vi} m. HE = {d} × {_fmt(den)} {unit} = {num(he_m, 1)} m. Gradient = VI ÷ HE = {vi} ÷ {num(he_m, 1)} = 1 in {num(g, 1)}.',
            'key': '3 marks: 1 for vertical interval, 1 for horizontal equivalent from the scale, 1 for the gradient.',
            'marks': 3, 'minutes': 5}


def contour_count(r):
    ci = r.choice([10, 20, 25, 50, 100])
    lo = ci * r.choice(range(1, 10))
    k = r.choice(range(3, 12))
    hi = lo + ci * k
    stem = f'On a map with a contour interval of {ci} m, how many contour lines will be crossed (including both ends) in going from the {lo} m contour to the {hi} m contour?'
    wrong = [str(x) for x in dict.fromkeys([k, k + 2, (hi - lo) // 10, k - 1]) if x != k + 1 and x > 0]
    return mcq(stem, str(k + 1), wrong, f'({hi} − {lo}) ÷ {ci} = {k} intervals, so {k + 1} contour lines including both ends.', r)


def sheet_count(r):
    a, b, n, label = r.choice([
        ('1:1,000,000 (4° × 4°)', '1:250,000 (1° × 1°)', 16, 'A to P'),
        ('1:250,000 (1° × 1°)', '1:50,000 (15′ × 15′)', 16, '1 to 16'),
        ('1:50,000 (15′ × 15′)', '1:25,000 (7′30″ × 7′30″)', 4, 'NE, NW, SE and SW'),
        ('1:1,000,000 (4° × 4°)', '1:50,000 (15′ × 15′)', 256, 'number/letter/number such as 53A/1'),
    ])
    stem = f'How many Survey of India sheets on the scale of {b} are there in one sheet of {a}?'
    wrong = [str(x) for x in dict.fromkeys([4, 16, 64, 256, 9]) if x != n][:3]
    return mcq(stem, str(n), wrong, f'Divide the extents: {a} ÷ {b} gives {n} sheets, designated {label}.', r)


# ---------------------------------------------------------------- remote sensing (ch23)

def pixel_count(r):
    res = r.choice([5, 10, 20, 25, 50, 100])
    w = r.choice([2, 3, 4, 5, 6, 10, 12, 15, 20])
    h = r.choice([2, 3, 4, 5, 6, 8, 10])
    nx, ny = int(w * 1000 / res), int(h * 1000 / res)
    cells = nx * ny
    stem = f'A satellite image has a spatial resolution of {res} m. How many pixels will cover an area of {w} km × {h} km?'
    wrong = [f'{x:,}' for x in dict.fromkeys([cells // 10, nx + ny, cells * 2, int(w * h * 1000 / res)]) if x != cells]
    return mcq(stem, f'{cells:,}', wrong, f'({w},000 ÷ {res}) × ({h},000 ÷ {res}) = {nx} × {ny} = {cells:,} pixels.', r)


def pixel_area(r):
    res = r.choice([5, 10, 20, 30, 50, 100])
    n = r.choice([100, 200, 400, 500, 1000, 2500])
    ha = n * res * res / 10000
    stem = f'A lake covers {n:,} pixels in an image of spatial resolution {res} m. What is the area of the lake?'
    wrong = num_distractors(ha, ha * 10, ha / 10, n * res / 10000, ha * 2, dp=2)
    return mcq(stem, f'{num(ha)} hectares', [f'{w} hectares' for w in wrong],
               f'Area = {n:,} × {res} m × {res} m = {_fmt(n * res * res)} m² = {num(ha)} hectares (1 hectare = 10,000 m²).', r)


# ---------------------------------------------------------------- physical geography numbers

def lapse_mcq(r):
    t0 = r.choice(range(20, 41))
    h = r.choice([1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000])
    t = t0 - 6.5 * h / 1000
    stem = (f'The temperature at sea level at a place is {t0}°C. Assuming the normal lapse rate of 6.5°C per 1,000 m, '
            f'what will be the temperature at a height of {_fmt(h)} m?')
    wrong = num_distractors(t, t0 + 6.5 * h / 1000, t0 - h / 1000, t0 - 6.5 * h / 100, t0 - 6.5, dp=2)
    return mcq(stem, f'{num(t)}°C', [f'{w}°C' for w in wrong], f'Fall = 6.5 × {_fmt(h)} ÷ 1,000 = {num(6.5 * h / 1000)}°C; temperature = {t0} − {num(6.5 * h / 1000)} = {num(t)}°C.', r)


def lapse_long(r):
    t_hill = r.choice(range(2, 20))
    h1 = r.choice([200, 300, 500])
    h2 = r.choice([2200, 2500, 3200, 1700, 2000])
    t_plain = t_hill + 6.5 * (h2 - h1) / 1000
    return {'stem': f'A hill station at {_fmt(h2)} m records a temperature of {t_hill}°C. Using the normal lapse rate, calculate the expected temperature '
                    f'at a town in the plains at {h1} m at the same time, and state one reason why actual temperatures may differ.',
            'answer': f'Difference in height = {_fmt(h2 - h1)} m; temperature difference = 6.5 × {_fmt(h2 - h1)} ÷ 1,000 = {num(6.5 * (h2 - h1) / 1000)}°C. '
                      f'Temperature in the plains ≈ {t_hill} + {num(6.5 * (h2 - h1) / 1000)} = {num(t_plain)}°C. Actual values may differ because of '
                      'inversion of temperature, aspect, winds or cloud cover.',
            'key': '3 marks: 1 for height difference, 1 for the computed temperature, 1 for a valid reason (inversion, aspect, local winds).',
            'marks': 3, 'minutes': 5}


def pressure_mcq(r):
    p0 = r.choice([1013, 1012, 1010, 1008, 1015])
    h = r.choice([100, 200, 300, 400, 500, 600, 800])
    p = p0 - h / 10
    stem = (f'The pressure at sea level is {p0} mb. Taking a fall of about 1 mb for every 10 m rise in the lower atmosphere, '
            f'what is the approximate pressure at a height of {h} m?')
    wrong = num_distractors(p, p0 - h, p0 - h / 100, p0 + h / 10, p0 - h / 5, dp=1)
    return mcq(stem, f'{num(p)} mb', [f'{w} mb' for w in wrong], f'Fall = {h} ÷ 10 = {num(h / 10)} mb; pressure ≈ {p0} − {num(h / 10)} = {num(p)} mb.', r)


def rh_mcq(r):
    cap = r.choice([10, 12, 15, 16, 20, 24, 25, 30, 40])
    pct = r.choice([20, 25, 40, 50, 60, 75, 80, 90])
    act = cap * pct / 100
    stem = (f'Air at a certain temperature can hold {cap} g of water vapour per cubic metre. It actually contains {num(act)} g per cubic metre. '
            'What is its relative humidity?')
    wrong = [f'{num(x)}%' for x in dict.fromkeys([100 - pct, act, cap / act * 10 if act else 5, pct / 2]) if num(x) != num(pct)]
    return mcq(stem, f'{pct}%', wrong, f'Relative humidity = actual ÷ capacity × 100 = {num(act)} ÷ {cap} × 100 = {pct}%.', r)


def rh_long(r):
    cap1 = r.choice([20, 24, 30, 40])
    act = r.choice([6, 8, 10, 12])
    cap2 = r.choice([x for x in [8, 10, 12, 15, 16] if x > act])
    rh1, rh2 = act / cap1 * 100, act / cap2 * 100
    return {'stem': f'In the afternoon, air can hold {cap1} g/m³ of water vapour and contains {act} g/m³. At night it cools and its capacity falls to '
                    f'{cap2} g/m³ with no change in moisture. Calculate the relative humidity in the afternoon and at night, and explain the change.',
            'answer': f'Afternoon RH = {act} ÷ {cap1} × 100 = {num(rh1, 1)}%. Night RH = {act} ÷ {cap2} × 100 = {num(rh2, 1)}%. '
                      'Relative humidity rises at night because cooler air can hold less moisture, though absolute humidity is unchanged.',
            'key': '3 marks: 1 for each relative humidity value, 1 for explaining that capacity falls with temperature.',
            'marks': 3, 'minutes': 5}


def salinity_mcq(r):
    g = r.choice([30, 32, 33, 35, 36, 37, 38, 40, 41])
    kg = r.choice([1, 2, 4, 5, 10])
    stem = f'A sample of {kg} kg of sea water contains {g * kg} g of dissolved salts. What is its salinity?'
    wrong = [f'{num(x)}‰' for x in dict.fromkeys([g * kg, g / 10, g * 10, g + 5]) if num(x) != num(g)]
    return mcq(stem, f'{g}‰', wrong, f'Salinity = grams of salt per 1,000 g of sea water = {g * kg} ÷ {kg} = {g} parts per thousand (‰).', r)


HB = [
    ('Of 100 units of insolation, 35 units are reflected back as albedo and 14 units are absorbed by the atmosphere. How many units are absorbed by the earth\'s surface?', '51', ['49', '65', '35'],
     '100 − 35 − 14 = 51 units.'),
    ('The earth radiates 51 units of terrestrial radiation, of which 34 units are absorbed by the atmosphere. How many units go directly to space?', '17', ['34', '14', '48'],
     '51 − 34 = 17 units.'),
    ('The atmosphere absorbs 14 units of insolation and 34 units of terrestrial radiation. How many units does it radiate back to space?', '48', ['34', '65', '20'],
     '14 + 34 = 48 units.'),
    ('Out of 100 units of insolation, 65 units are absorbed by the earth system. How many units make up the albedo?', '35', ['65', '51', '14'],
     '100 − 65 = 35 units.'),
    ('The atmosphere radiates 48 units and the earth radiates 17 units directly to space. What is the total outgoing radiation?', '65', ['48', '100', '31'],
     '48 + 17 = 65 units, which balances the 65 units absorbed.'),
    ('Of the 35 units of albedo, 27 units are reflected from the tops of clouds and 2 units from snow and ice. How many units are reflected by scattering in the atmosphere?', '6', ['8', '29', '2'],
     '35 − 27 − 2 = 6 units.'),
]


def heat_budget(r):
    i = r.randrange(len(HB))
    s, a, w, k = HB[i]
    return mcq(s, f'{a} units', [f'{x} units' for x in w], k, r)


def heat_budget_long(r):
    return {'stem': 'Using 100 units of insolation, show with calculations how the heat budget of the earth balances.',
            'answer': '35 units reflected (albedo); 14 absorbed by atmosphere; 51 by surface (100 − 35 − 14). The surface radiates 51: 17 to space, 34 to atmosphere. '
                      'The atmosphere radiates 14 + 34 = 48 to space. Total outgoing = 17 + 48 = 65 = units absorbed, so the budget balances.',
            'key': '3 marks: 1 for 35/14/51, 1 for 17 + 34, 1 for 48 and the balance 65 = 65.', 'marks': 3, 'minutes': 5}


# ---------------------------------------------------------------- registry

def _m(C, D, g):
    return F(C, D, 'mcq', g)


def _n(C, D, g, marks=3, minutes=5, typ='numerical'):
    return F(C, D, typ, g, marks=marks, minutes=minutes)


EXTRA = {
    S + '08-st2': [_m('C3', 'D2', heat_budget), _n('C3', 'D3', heat_budget_long)],
    S + '08-st3': [_m('C3', 'D2', lapse_mcq), _n('C3', 'D3', lapse_long)],
    S + '09-st1': [_m('C3', 'D2', pressure_mcq)],
    S + '10-st1': [_m('C3', 'D2', rh_mcq), _n('C3', 'D3', rh_long)],
    S + '11-st3': [_m('C3', 'D2', salinity_mcq)],
    S + '19-st1': [_m('C3', 'D2', map_to_ground), _m('C3', 'D2', ground_to_map)],
    S + '19-st2': [_m('C3', 'D2', stmt_to_rf), _m('C3', 'D2', rf_to_stmt), _m('C3', 'D3', inch_to_rf),
                   _n('C3', 'D3', scale_convert_long), _n('C3', 'D3', rf_english_long)],
    S + '19-st3': [_n('C3', 'D3', graphical_scale, minutes=6)],
    S + '20-st2': [_m('C3', 'D2', time_diff), _m('C3', 'D3', local_time), _n('C3', 'D3', local_time_long)],
    S + '20-st3': [_m('C3', 'D2', ist_from_gmt), _m('C3', 'D3', idl_item)],
    S + '21-st3': [_m('C3', 'D3', cea_mcq), _m('C3', 'D2', equator_len), _n('C3', 'D4', cea_long, minutes=8)],
    S + '22-st1': [_m('C3', 'D2', sheet_count)],
    S + '22-st2': [_m('C3', 'D3', gradient_mcq), _m('C3', 'D2', contour_count), _n('C3', 'D3', gradient_long)],
    S + '23-st2': [_m('C3', 'D2', pixel_count), _m('C3', 'D2', pixel_area)],
}
