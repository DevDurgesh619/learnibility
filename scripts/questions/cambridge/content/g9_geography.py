"""Cambridge IGCSE Geography 0460, year 1 (grade 9): geographical skills and the physical topics.

Mirrors the 0460 papers: Paper 1-style resource-based structured questions (figures and tables
described in words), named case studies with 7-mark levels-marked answers, and Paper 4-style
skills items (grid references, scale, gradient, statistics, graphs).

Each topic is built from a knowledge pack (key terms, MCQs, explanations, claims to check,
resource-based scenarios, case studies, extended-response claims) by the generic builders below,
plus topic-specific parameterised data templates whose answers are computed in code.
The builders are reused by g10_geography.py.
"""
import math
import re as _re
from ._lib import topic, mcq, compose, person, two_people, city, sf, fmt

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
MON = [m[:3] for m in MONTHS]


def cap(s):
    return s[:1].upper() + s[1:]


def low(s):
    return s[:1].lower() + s[1:]


def T(name, *extra):
    return topic(name, name.lower(), *extra)


def an(w):
    return ('an ' if w[:1].lower() in 'aeiou' else 'a ') + w


# ============================================================== generic builders

def add_terms(t, terms):
    """terms: [(term, definition)] -> C1 items (definition -> term, term -> definition)."""
    if len(terms) < 4:
        return
    t.fixed('C1', (1, 2), [(f'Name the geographical term that matches this definition: “{d}”.', cap(term), f'{cap(term)}: {d}. [1]',
                            [cap(x) for x, _ in terms if x != term]) for term, d in terms])
    n = len(terms)
    # rotate distractors so that no two items share the same option set
    t.fixed('C1', (2, 3), [(f'What is meant by the term “{term}”?', cap(d) + '.', f'{cap(term)}: {d}. [1]',
                            [cap(terms[(i + k) % n][1]) + '.' for k in (1, 2, 3)]) for i, (term, d) in enumerate(terms)])


def add_mcqs(t, C, D, entries):
    """entries: (stem, answer, [3+ distractors], key) as stand-alone MCQ templates."""
    for stem, ans, ds, key in entries:
        def fn(r, D_, stem=stem, ans=ans, ds=ds, key=key):
            opts, a = mcq(r, ans, list(ds))
            return {'stem': stem, 'options': opts, 'answer': a, 'key': key}
        fn.__name__ = 'mcq'
        t.add(C, D, 'mcq')(fn)


def add_explain(t, entries, D=(2, 3, 4)):
    t.fixed('C2', D, entries, type='explain')


CLAIM_LEADS = ['A student writes:', 'In a class discussion, a student says:', 'A revision website states:', 'A classmate claims:', 'A student’s exam answer states:']


def add_claims(t, claims):
    ents = []
    for i, (c, ok, why) in enumerate(claims):
        lead = CLAIM_LEADS[i % len(CLAIM_LEADS)]
        ents.append((f'{lead} “{c}” Is this correct? Explain your answer.', ('Correct. ' if ok else 'Not correct. ') + why,
                     '1 mark correct judgement; 1 mark accurate geographical explanation [2]'))
    t.fixed('C2', (1, 2, 3), ents, type='explain')


ESSAY_LEADS = [
    lambda c, p: f'“{cap(c)}.” To what extent do you agree with this statement? Support your answer with examples.',
    lambda c, p: f'To what extent do you agree that {c}? Use examples you have studied.',
    lambda c, p: f'Evaluate the view that {c}.',
    lambda c, p: f'{p} argues that {c}. How far do you agree? Give evidence for and against before reaching a judgement.',
    lambda c, p: f'“{cap(c)}.” Discuss this view, using named examples, and reach a supported conclusion.',
]
LEVELS7 = ('Levels marking. Level 1 (1-3 marks): simple, generalised statements. Level 2 (4-6 marks): developed statements with some '
           'explanation and some reference to examples. Level 3 (7 marks): comprehensive, well-developed answer with accurate, '
           'place-specific detail and a clear judgement. [7]')
LEVELS7CS = ('Levels marking. Level 1 (1-3 marks): simple statements, not place-specific. Level 2 (4-6 marks): developed statements, '
             'with some reference to the named example. Level 3 (7 marks): comprehensive, developed statements with accurate '
             'place-specific detail (names, figures, dates) from the named example. [7]')


def add_essay(t, claim, pro, con, judge, hints=(), D=(2, 3, 4, 5)):
    def fn(r, D_):
        p = person(r)
        if D_ <= 2:
            stem = f'Explain whether you agree that {claim}. Give one reason for and one reason against.'
            key = 'Level 1 (1-2 marks): one simple reason. Level 2 (3-4 marks): one developed reason for AND one against, with an example. [4]'
            mk = 4
        else:
            stem = r.choice(ESSAY_LEADS)(claim, p)
            if hints and r.random() < 0.7:
                hs = r.sample(list(hints), min(len(hints), r.choice([2, 3])))
                stem += ' You may wish to consider: ' + '; '.join(hs) + '.'
            key, mk = LEVELS7, 7
        ans = 'For: ' + ' '.join(pro) + ' Against: ' + ' '.join(con) + ' Judgement: ' + judge
        return {'stem': stem, 'answer': ans, 'key': key, 'type': 'long', 'marks': mk}
    fn.__name__ = 'essay'
    t.add('C4', D, 'long')(fn)


def add_case(t, intros, parts, C3=(2, 3, 4, 5), C4=(3, 4, 5)):
    """Resource-based / scenario structured question: intros (list of str), parts [(q, a, key-with-[n])]."""
    plist = [(lambda r, p=p: p) for p in parts]

    def mk(k):
        def fn(r, D):
            return compose(r, r.choice(intros), plist, k=k, type_='case')
        fn.__name__ = 'case'
        return fn
    if C3:
        t.add('C3', C3, 'case')(mk((2, 3)))
    if C4:
        t.add('C4', C4, 'case')(mk((3, 4)))


CS_LEADS = [
    lambda k, n, p: f'For a named example of {k} that you have studied, {p}.',
    lambda k, n, p: f'Using a case study of {k}, such as {n}, {p}.',
    lambda k, n, p: f'With reference to {n}, or another example of {k} you have studied, {p}.',
    lambda k, n, p: f'Name an example of {k}. For your chosen example, {p}.',
]


def add_cs(t, kind, cases, prompts):
    """Named case-study questions (0460 7-mark style).

    cases: [(name, {aspect: model answer text})]; prompts: [(prompt, aspect, indicative content)].
    C4: full 7-mark levels-marked answer (5 marks at D2). C3: shorter 4-mark place-specific answer.
    """
    def c4(r, D):
        name, facts = r.choice(cases)
        ok = [p for p in prompts if p[1] in facts]
        if not ok:
            return None
        pr, asp, ind = r.choice(ok)
        stem = r.choice(CS_LEADS)(kind, name, pr)
        if D <= 2:
            key = ('Level 1 (1-2 marks): simple statements. Level 2 (3-4 marks): developed statements. Level 3 (5 marks): developed '
                   'statements with place-specific detail. Indicative content: ' + ind + ' [5]')
            mk = 5
        else:
            key = 'Indicative content: ' + ind + ' ' + LEVELS7CS
            mk = 7
        return {'stem': stem, 'answer': f'Model answer ({name}): {facts[asp]}', 'key': key, 'type': 'long', 'marks': mk}
    c4.__name__ = 'cs'
    t.add('C4', (2, 3, 4, 5), 'long')(c4)

    def c3(r, D):
        name, facts = r.choice(cases)
        ok = [p for p in prompts if p[1] in facts]
        if not ok:
            return None
        pr, asp, ind = r.choice(ok)
        lead = r.choice([f'Name one example of {kind} you have studied and, for that example, {pr}.',
                         f'Study your case study of {kind} (for example {name}). Briefly {pr}.',
                         f'For {name} or another example of {kind}, briefly {pr}.'])
        return {'stem': lead, 'answer': f'{name}: {facts[asp]}', 'key': '1 mark for a named, located example; up to 3 marks for accurate, place-specific points. ' + ind + ' [4]',
                'type': 'case', 'marks': 4}
    c3.__name__ = 'cs3'
    t.add('C3', (2, 3, 4), 'case')(c3)


def _markify(t, start):
    for tpl in t.templates[start:]:
        if tpl.name != 'fixed':
            continue

        def fn(r, D, f=tpl.fn):
            q = f(r, D)
            if q and 'marks' not in q:
                m = _re.findall(r'\[(\d+)\]', q['key'])
                if m:
                    q['marks'] = int(m[-1])
            return q
        tpl.fn = fn


def build(t, P):
    start = len(t.templates)
    add_terms(t, P.get('terms', []))
    if P.get('mcq'):
        add_mcqs(t, 'C1', (1, 2, 3), P['mcq'])
    if P.get('explain'):
        add_explain(t, P['explain'])
    if P.get('claims'):
        add_claims(t, P['claims'])
    for c in P.get('cases', []):
        add_case(t, c[0], c[1], *c[2:])
    for cs in P.get('cs', []):
        add_cs(t, *cs)
    for e in P.get('essays', []):
        add_essay(t, *e)
    _markify(t, start)
    return t


# ============================================================== data helpers

def mean(xs):
    return sum(xs) / len(xs)


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def pct_change(a, b):
    return (b - a) / a * 100


def listing(labels, values, unit=''):
    return ', '.join(f'{l} {fmt(v, 1)}{unit}' for l, v in zip(labels, values))


def trend_words(labels, values, unit=''):
    """Describe a series: overall trend, peak and lowest with figures."""
    hi, lo = max(values), min(values)
    li, lj = labels[values.index(hi)], labels[values.index(lo)]
    up = values[-1] > values[0]
    rises = sum(1 for a, b in zip(values, values[1:]) if b > a)
    falls = sum(1 for a, b in zip(values, values[1:]) if b < a)
    if rises and falls:
        shape = 'with fluctuations'
    else:
        shape = 'steadily'
    return (f'Overall {"an increase" if up else "a decrease"} from {fmt(values[0], 1)}{unit} ({labels[0]}) to {fmt(values[-1], 1)}{unit} ({labels[-1]}), {shape}; '
            f'highest {fmt(hi, 1)}{unit} in {li}, lowest {fmt(lo, 1)}{unit} in {lj}.')


def dp(x, n=1):
    return fmt(round(x, n), n)


def nf(x):
    """Integer with a space as thousands separator (Cambridge style)."""
    return f'{x:,}'.replace(',', ' ')


# ============================================================== CHAPTER 1: Geographical skills

FEATURES = ['church with a tower', 'youth hostel', 'post office', 'school', 'bridge over the river', 'farm', 'railway station', 'campsite',
            'windmill', 'quarry', 'lighthouse', 'car park', 'radio mast', 'museum', 'golf course clubhouse', 'trig point']
DIRS = [('north', 0, 1, '000'), ('north-east', 1, 1, '045'), ('east', 1, 0, '090'), ('south-east', 1, -1, '135'),
        ('south', 0, -1, '180'), ('south-west', -1, -1, '225'), ('west', -1, 0, '270'), ('north-west', -1, 1, '315')]
RIVER_TOWNS = ['Lima', 'Cairo', 'Hanoi', 'Jakarta', 'Manila', 'Santiago', 'Toronto', 'Madrid', 'Bangkok', 'Kathmandu', 'Dhaka', 'Seoul', 'Lisbon', 'Kuala Lumpur', 'Nairobi', 'Bogotá']
COAST_TOWNS = ['Lima', 'Cape Town', 'Lisbon', 'Lagos', 'Doha', 'Muscat', 'Accra', 'Colombo', 'Auckland', 'Mumbai', 'Karachi', 'Dubai', 'Manila', 'Istanbul', 'Santiago de Cuba', 'Mombasa']


def place(r, kind='any'):
    """A town that suits the physical context (rivers need a river town, beaches a coastal one)."""
    if kind == 'river':
        return r.choice(RIVER_TOWNS)
    if kind == 'coast':
        return r.choice(COAST_TOWNS)
    if kind == 'tropical':
        return r.choice(['Mombasa', 'Lagos', 'Colombo', 'Mumbai', 'Karachi', 'Manila', 'Accra', 'Santiago de Cuba'])
    return city(r)


MAPNAMES = ['Fig. 1.1 (part of a 1:25 000 topographic map)', 'the topographic map extract (scale 1:50 000)', 'Fig. 4.1, a map of part of a rural area',
            'the map extract of a coastal area']

c1a = T('Topographic map skills: grid references, scale, distance and direction', 'grid references scale distance direction')
build(c1a, {
    'terms': [
        ('easting', 'a vertical grid line on a map, numbered from west to east and read first in a grid reference'),
        ('northing', 'a horizontal grid line on a map, numbered from south to north and read second in a grid reference'),
        ('representative fraction', 'a map scale written as a ratio, such as 1:50 000, meaning one unit on the map is 50 000 of the same units on the ground'),
        ('linear scale', 'a line drawn on a map divided into units that represent real distances on the ground'),
        ('six-figure grid reference', 'a location given by eastings and northings with tenths, which identifies a point to within 100 metres'),
        ('compass bearing', 'a direction measured clockwise from north in degrees, written with three figures'),
        ('map key', 'the part of a map that explains the meaning of its symbols and colours'),
        ('straight-line distance', 'the shortest distance between two points on a map, measured “as the crow flies”'),
    ],
    'mcq': [
        ('In a six-figure grid reference, which part is given first?', 'The easting', ['The northing', 'The spot height', 'The scale'], 'Eastings (along) before northings (up). [1]'),
        ('On a 1:25 000 map, what real distance does 4 cm represent?', '1 km', ['4 km', '0.25 km', '10 km'], '4 × 25 000 = 100 000 cm = 1 km. [1]'),
        ('Which map scale shows a small area in the greatest detail?', '1:10 000', ['1:50 000', '1:250 000', '1:1 000 000'], 'Smaller second number = larger scale = more detail. [1]'),
        ('A bearing of 225° points towards which direction?', 'South-west', ['North-east', 'South-east', 'North-west'], 'Clockwise from north: 180° south, 270° west, so 225° is SW. [1]'),
        ('Each grid square on a 1:50 000 map is 2 cm wide. What area does one grid square represent?', '1 km²', ['2 km²', '4 km²', '0.5 km²'], '2 cm × 50 000 = 1 km, so each square is 1 km × 1 km. [1]'),
        ('Which method gives the most accurate measurement of the length of a winding road on a map?', 'Marking each bend on the straight edge of a piece of paper and placing it against the linear scale',
         ['Measuring the straight-line distance between the ends with a ruler', 'Counting the number of grid squares the road crosses', 'Estimating from the contour lines'], 'Paper edge (or string) follows the bends. [1]'),
    ],
    'explain': [
        ('Explain why a six-figure grid reference is more useful than a four-figure reference for locating a building.', 'A four-figure reference only identifies a 1 km grid square; a six-figure reference divides the square into tenths in each direction, locating a point to within 100 m.', '1 mark four-figure = whole square; 1 mark six-figure = point within 100 m [2]'),
        ('Explain the difference between the straight-line distance and the distance by road between two places.', 'Straight-line distance is the shortest direct distance; roads bend around relief, rivers and buildings, so the road distance is longer.', '1 mark each [2]'),
        ('Explain why it is important to check the scale before measuring distances on a map.', 'The same map distance represents very different ground distances at different scales (e.g. 1 cm = 250 m at 1:25 000 but 500 m at 1:50 000).', '1 mark scale varies; 1 mark example [2]'),
        ('Describe how to give a compass bearing from point A to point B on a map.', 'Draw a line from A to B; place a protractor on A with 0° pointing to grid north; measure the angle clockwise from north to the line; write it as three figures.', '1 mark line and north; 1 mark clockwise; 1 mark three figures [3]'),
        ('Explain why map users need to be able to describe the location of a feature using both direction and distance.', 'Direction alone does not say how far; distance alone does not say which way; together they locate the feature precisely relative to another place.', '1 mark each [2]'),
    ],
    'claims': [
        ('In a grid reference you read the northing before the easting.', False, 'Eastings are always given first (along the corridor, then up the stairs).'),
        ('A 1:25 000 map shows more detail than a 1:50 000 map of the same area.', True, 'It is a larger scale: 1 cm represents 250 m instead of 500 m, so features are shown larger and in more detail.'),
        ('A bearing of 090° means travelling west.', False, 'Bearings are measured clockwise from north, so 090° is east and 270° is west.'),
        ('The six-figure reference 456 732 lies in the four-figure square 4573.', True, 'The first two digits of each half give the square: easting 45, northing 73.'),
    ],
    'essays': [
        ('paper topographic maps are no longer needed now that people use digital mapping and satellite navigation',
         ['Digital maps update quickly, zoom in and out and show live information such as traffic.', 'GPS gives an exact location without needing grid references.'],
         ['Phones lose signal and battery in remote areas, so walkers and rescue teams still carry paper maps.', 'Contours, symbols and scale are the same skills needed to read digital maps.', 'Paper maps show a wide area at once for planning.'],
         'Digital tools have changed map use, but map skills and paper maps are still needed, especially in remote areas and emergencies.',
         ['remote areas', 'reliability', 'interpreting relief', 'cost']),
    ],
})


@c1a.add('C3', (1, 2, 3, 4), 'numerical')
def c1a_grid(r, D):
    e, n = r.randint(11, 88), r.randint(11, 88)
    tx, ty = r.randint(1, 9), r.randint(1, 9)
    if tx == ty:
        ty = (ty % 9) + 1
    f = r.choice(FEATURES)
    four, six = f'{e:02d}{n:02d}', f'{e:02d}{tx}{n:02d}{ty}'
    src = r.choice(MAPNAMES)
    stem = (f'On {src}, the {f} lies in the grid square whose south-west corner is where easting {e:02d} meets northing {n:02d}. '
            f'The symbol is {tx} tenths of the way across the square (eastwards) and {ty} tenths of the way up (northwards).')
    if D == 1:
        opts, a = mcq(r, six, [f'{n:02d}{ty}{e:02d}{tx}', f'{e:02d}{ty}{n:02d}{tx}', f'{e + 1:02d}{tx}{n + 1:02d}{ty}', f'{e:02d}{n:02d}{tx}{ty}'])
        return {'stem': stem + f' What is the six-figure grid reference of the {f}?', 'options': opts, 'answer': a, 'key': f'Easting {e:02d} + {tx} tenths, then northing {n:02d} + {ty} tenths = {six}. [1]'}
    if D == 2:
        return {'stem': stem + f' Give (a) the four-figure and (b) the six-figure grid reference of the {f}.', 'answer': f'(a) {four} (b) {six}',
                'key': f'(a) {four} [1] (b) {six}: easting first, then northing [1]', 'marks': 2}
    dx, dy = r.choice([1, 2, 3, -1, -2]), r.choice([-2, -1, 1, 2, 3])
    g = r.choice([x for x in FEATURES if x != f])
    gx, gy = r.randint(1, 9), r.randint(1, 9)
    ex, ny = e * 10 + tx, n * 10 + ty
    ex2, ny2 = (e + dx) * 10 + gx, (n + dy) * 10 + gy
    six2 = f'{e + dx:02d}{gx}{n + dy:02d}{gy}'
    ddx, ddy = ex2 - ex, ny2 - ny
    ang = math.degrees(math.atan2(ddx, ddy)) % 360
    dname = DIRS[int(((ang + 22.5) % 360) // 45)][0]
    dist = math.hypot(ddx, ddy) / 10 * (1 if '25 000' not in src else 1)
    stem += f' A {g} is at {six2}. The grid lines are 1 km apart.'
    parts = [
        lambda r: (f'Give the six-figure grid reference of the {f}.', six, f'{six} (eastings first) [1]'),
        lambda r: (f'State the compass direction (eight points) of the {g} from the {f}.', cap(dname), f'Bearing about {round(ang):03d}°, so {dname} [1]'),
        lambda r: (f'Calculate the straight-line distance between the {f} and the {g}, to the nearest 0.1 km.', f'{dp(dist)} km',
                   f'Difference: {abs(ddx) / 10:.1f} km east-west and {abs(ddy) / 10:.1f} km north-south; √({abs(ddx) / 10:.1f}² + {abs(ddy) / 10:.1f}²) = {dp(dist)} km (accept ±0.1) [2]'),
        lambda r: (f'Suggest why a walker might travel further than this to get from the {f} to the {g}.', 'Paths and roads bend around steep slopes, rivers, woodland and private land, so the route is longer than a straight line.', '1 mark obstacle/relief; 1 mark route not straight [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c1a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c1a_scale(r, D):
    sc = r.choice([10000, 25000, 50000])
    cm = r.choice([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 6.5, 7, 7.5, 8, 9, 11, 12])
    km = cm * sc / 100000
    scs = f'1:{sc:,}'.replace(',', ' ')
    a, b = r.sample(FEATURES, 2)
    if D == 1:
        opts, ans = mcq(r, f'{fmt(km, 3)} km', [f'{fmt(km * 10, 3)} km', f'{fmt(km / 10, 3)} km', f'{fmt(cm * sc / 1000, 1)} km', f'{fmt(km * 2, 3)} km'])
        return {'stem': f'On a {scs} map, the {a} and the {b} are {fmt(cm, 1)} cm apart. What is the real distance between them?', 'options': opts, 'answer': ans,
                'key': f'{fmt(cm, 1)} × {sc} = {fmt(cm * sc, 0)} cm = {fmt(km, 3)} km. [1]'}
    if D <= 3:
        return {'stem': f'On a {scs} map, a footpath from the {a} to the {b} measures {fmt(cm, 1)} cm. Calculate the length of the footpath on the ground in kilometres. Show your working.',
                'answer': f'{fmt(km, 3)} km', 'key': f'{fmt(cm, 1)} cm × {sc} = {fmt(cm * sc, 0)} cm (1 mark); ÷ 100 000 = {fmt(km, 3)} km (1 mark) [2]', 'marks': 2}
    speed = r.choice([4, 5])
    mins = km / speed * 60
    climb = r.choice([0, 60, 120, 200])
    extra = climb / 10  # Naismith: 1 minute per 10 m of ascent
    parts = [
        lambda r: ('Calculate the real distance in km.', f'{fmt(km, 3)} km', f'{fmt(cm, 1)} × {sc} ÷ 100 000 = {fmt(km, 3)} km [2]'),
        lambda r: (f'The group walks at {speed} km/h. Calculate the walking time in minutes on flat ground.', f'{dp(mins)} minutes', f'time = distance ÷ speed = {fmt(km, 3)} ÷ {speed} h × 60 = {dp(mins)} min [2]'),
        lambda r: (f'The route climbs {climb} m. Using the rule of adding 1 minute for every 10 m of ascent, calculate the total time.' if climb else 'Suggest why the walk may take longer than this calculation.',
                   f'{dp(mins + extra)} minutes' if climb else 'Steep slopes (close contours), rough ground, winding paths, river crossings or rest stops.',
                   (f'{dp(mins)} + {climb} ÷ 10 = {dp(mins + extra)} min [1]') if climb else '1 mark valid reason [1]'),
    ]
    intro = f'A walking group plans a route on a {scs} map. The route from the {a} to the {b} measures {fmt(cm, 1)} cm.'
    return compose(r, intro, parts, k=(2, 3), type_='numerical')


@c1a.add('C3', (1, 2, 3), 'short')
def c1a_dir(r, D):
    a, b = r.sample(FEATURES, 2)
    i = r.randrange(8)
    name, dx, dy, brg = DIRS[i]
    opp = DIRS[(i + 4) % 8]
    k = r.choice([1, 1.5, 2, 3, 4])
    ps = []
    if dx:
        ps.append(f'{fmt(k, 1)} km {"east" if dx > 0 else "west"}')
    if dy:
        ps.append(f'{fmt(k, 1)} km {"north" if dy > 0 else "south"}')
    stem = f'On a map, the {b} is ' + ' and '.join(ps) + f' of the {a}.'
    if D == 1:
        opts, ans = mcq(r, cap(name), [cap(d[0]) for d in DIRS if d[0] != name])
        return {'stem': stem + f' In which direction is the {b} from the {a}?', 'options': opts, 'answer': ans, 'key': f'{cap(name)} (bearing {brg}°). [1]'}
    return {'stem': stem + f' (a) State the compass direction of the {b} from the {a}. (b) Give the three-figure bearing. (c) State the bearing you would follow to return from the {b} to the {a}.',
            'answer': f'(a) {cap(name)} (b) {brg}° (c) {opp[3]}° ({opp[0]})', 'key': f'(a) {name} [1] (b) {brg}° clockwise from north [1] (c) {opp[3]}°: add or subtract 180° [1]', 'marks': 3}


@c1a.add('C3', (2, 3, 4), 'numerical')
def c1a_area(r, D):
    sc = r.choice([25000, 50000])
    side = 4 if sc == 25000 else 2
    w, h = r.randint(2, 6), r.randint(2, 5)
    part = r.choice([0.5, 0.25, 0.75])
    feat = r.choice(['a forest', 'a reservoir', 'an area of farmland', 'a built-up area', 'a nature reserve'])
    full = w * h
    tot = full + part * r.choice([2, 4])
    halves = int(round((tot - full) / part))
    stem = f'On a 1:{nf(sc)} map ({side} cm grid squares, each 1 km²), {feat} completely covers {full} grid squares and covers about {fmt(part, 2)} of each of {halves} other squares.'
    parts = [
        lambda r: (f'Estimate the area of {feat} in km².', f'{fmt(tot, 2)} km²', f'{full} + {halves} × {fmt(part, 2)} = {fmt(tot, 2)} km² [2]'),
        lambda r: ('State the real length represented by the side of one grid square.', '1 km', f'{side} cm × {nf(sc)} = 100 000 cm = 1 km [1]'),
        lambda r: ('Explain why counting squares gives only an estimate of area.', 'Part-squares must be judged by eye, and the edge of the feature is irregular, so the total is approximate.', '1 mark partial squares; 1 mark irregular boundary [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


# --------------------------------------------------------------- 1.2 relief
c1b = T('Relief and gradient: contours, spot heights and drawing cross-sections', 'contours spot heights cross-sections')
build(c1b, {
    'terms': [
        ('contour line', 'a line on a map joining places of equal height above sea level'),
        ('contour interval', 'the difference in height between two neighbouring contour lines'),
        ('spot height', 'a dot on a map with a number showing the exact height of that point in metres'),
        ('gradient', 'the steepness of a slope, found by dividing the vertical difference in height by the horizontal distance'),
        ('cross-section', 'a side view of the shape of the land along a line drawn across a map'),
        ('spur', 'a ridge of high land sticking out into lower land, shown by V-shaped contours pointing downhill'),
        ('escarpment', 'a steep slope on one side of a ridge with a gentle slope on the other side'),
        ('plateau', 'a large area of fairly flat high land, often with steep edges'),
        ('vertical exaggeration', 'stretching the vertical scale of a cross-section compared with the horizontal scale so that relief can be seen clearly'),
    ],
    'mcq': [
        ('Contour lines that are very close together show', 'a steep slope', ['flat land', 'a gentle slope', 'a marsh'], 'Close contours = large height change over a short distance. [1]'),
        ('V-shaped contours pointing uphill (towards higher numbers) usually show', 'a river valley', ['a spur', 'a plateau', 'a hilltop'], 'Valleys: Vs point upstream/uphill; spurs: Vs point downhill. [1]'),
        ('A map shows a closed ring of contours with the highest value in the centre. This is', 'a hill or summit', ['a lake', 'a valley', 'a cliff'], '[1]'),
        ('Which map symbol gives the exact height of a single point?', 'A spot height', ['A contour line', 'Layer colouring', 'Hill shading'], '[1]'),
        ('A slope rises 50 m over a horizontal distance of 1 km. What is its gradient?', '1 : 20', ['1 : 50', '1 : 200', '20 : 1'], '1000 ÷ 50 = 20, so 1 : 20. [1]'),
        ('Contours that are evenly spaced show a slope that is', 'uniform (even)', ['concave', 'convex', 'vertical'], 'Concave: contours closer at the top; convex: closer at the bottom. [1]'),
    ],
    'explain': [
        ('Explain how you can tell from contour lines whether a slope is concave or convex.', 'Concave: contours close together at the top and wider apart lower down. Convex: contours wide apart at the top and close together lower down.', '1 mark each [2]'),
        ('Describe how to draw a cross-section between two points on a map.', 'Place the straight edge of paper between the points; mark and label each contour it crosses; transfer the marks to the horizontal axis of graph paper; plot each height and join with a smooth line; label features and add scales.', '1 mark marking contours; 1 mark plotting heights; 1 mark smooth line/labels [3]'),
        ('Explain how to tell a spur from a valley on a contour map.', 'In a valley the V-shaped contours point uphill (and a river often flows along it); on a spur the Vs point downhill towards lower land.', '1 mark valley; 1 mark spur [2]'),
        ('Explain why the vertical scale of a cross-section is often exaggerated.', 'Height differences are small compared with horizontal distances; exaggerating the vertical scale makes slopes and relief features visible.', '1 mark small vertical change; 1 mark makes relief clear [2]'),
        ('Explain why relief affects the location of roads and railways.', 'Routes follow valleys and gentle slopes because steep gradients are hard and costly to build on and difficult for vehicles; high, steep land is avoided or crossed by tunnels and zig-zags.', '1 mark gentle routes/valleys; 1 mark reason (cost/vehicles) [2]'),
    ],
    'claims': [
        ('If contour lines are far apart, the land must be very high.', False, 'Spacing shows steepness, not height; widely spaced contours show a gentle slope at any height. The contour values show height.'),
        ('Contour lines can never cross each other.', True, 'A point cannot have two different heights; only at a vertical cliff do contours appear to merge.'),
        ('A gradient of 1:10 is steeper than a gradient of 1:50.', True, '1:10 rises 1 m for every 10 m horizontally, while 1:50 rises 1 m in 50 m.'),
        ('Spot heights and contour lines show exactly the same information.', False, 'Contours show lines of equal height across an area; spot heights give the exact height of a single point.'),
    ],
    'cases': [
        (['Study Fig. 1.2, which describes a map extract. Contours at a 10 m interval run from 40 m beside a river in the west to 180 m at a summit in the east. In the west they are wide apart; east of the 120 m contour they are very close together. A spot height of 186 m marks the summit. V-shaped contours point east along a stream that flows west.',
          'Fig. 1.2 describes part of a topographic map. A river flows west in a wide valley at about 40 m. To the east the land rises: contours are widely spaced up to 120 m, then crowded together up to a summit marked by a spot height of 186 m. A small stream valley cuts into the slope, shown by contours forming Vs pointing east.'],
         [('State the height of the summit.', '186 m (spot height).', '[1]'),
          ('Describe the relief of the area shown.', 'Low, fairly flat land (about 40 m) by the river in the west; land rises gently to about 120 m, then steeply to a summit of 186 m in the east; the slope is cut by a small stream valley.', '1 mark low west; 1 mark gentle then steep; 1 mark figures quoted [3]'),
          ('State whether the slope east of the river is concave or convex. Give a reason.', 'Convex: contours are wide apart lower down and close together near the top.', '1 mark convex; 1 mark reason [2]'),
          ('Explain which direction the small stream flows and how you know.', 'West, downhill towards the river: the contour Vs point upstream (east), towards higher land.', '1 mark west; 1 mark V points uphill/upstream [2]'),
          ('Suggest why settlement is more likely in the west of the area.', 'Flat, low land near the river is easier to build on and farm, with water supply and easier routes; the steep east is hard to build on.', '1 mark flat land; 1 mark water/access [2]')]),
    ],
    'essays': [
        ('relief is the most important factor affecting how land is used in an area',
         ['Steep slopes limit building, roads and machinery; flat valley floors attract settlement, farming and routes.', 'Height affects temperature and so crops.'],
         ['Soil, drainage and climate also matter.', 'Human factors such as markets, transport, planning laws and technology (terracing, tunnels) can overcome relief.'],
         'Relief strongly influences land use, but human factors and technology can modify its effect.',
         ['slopes and farming', 'transport routes', 'settlement', 'technology']),
    ],
})


@c1b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c1b_grad(r, D):
    ci = r.choice([5, 10, 20])
    h1 = r.choice([40, 60, 80, 100, 120, 150, 200, 240])
    steps = r.choice([3, 4, 5, 6, 8, 10])
    rise = ci * steps
    h2 = h1 + rise
    sc = r.choice([25000, 50000])
    cm = r.choice([1, 1.5, 2, 2.5, 3, 4, 5, 6])
    dist = int(cm * sc / 100)  # metres
    grad = dist / rise
    a, b = r.sample(FEATURES, 2)
    stem = (f'On a 1:{nf(sc)} map with a contour interval of {ci} m, the {a} lies on the {h1} m contour and the {b} lies on the {h2} m contour. '
            f'They are {fmt(cm, 1)} cm apart on the map.')
    if D == 1:
        opts, ans = mcq(r, f'{rise} m', [f'{h2} m', f'{h1} m', f'{steps} m', f'{rise + ci} m'])
        return {'stem': stem + ' What is the difference in height between them?', 'options': opts, 'answer': ans, 'key': f'{h2} − {h1} = {rise} m. [1]'}
    parts = [
        lambda r: ('Calculate the difference in height.', f'{rise} m', f'{h2} − {h1} = {rise} m [1]'),
        lambda r: ('Calculate the horizontal distance between them in metres.', f'{dist} m', f'{fmt(cm, 1)} cm × {sc} ÷ 100 = {dist} m [1]'),
        lambda r: ('Calculate the average gradient, giving your answer as a ratio 1 : n.', f'1 : {dp(grad)}', f'gradient = vertical ÷ horizontal = {rise} : {dist} = 1 : {dp(grad)} [2]'),
        lambda r: ('State how many contour lines you cross walking between them, not counting the one you start on.', f'{steps}', f'{rise} ÷ {ci} = {steps} [1]'),
        lambda r: ('Suggest one reason why a cyclist would find this route difficult or easy.', ('Difficult: a gradient of 1 : ' + dp(grad) + ' is steep for cycling.') if grad < 15 else ('Fairly easy: 1 : ' + dp(grad) + ' is a gentle gradient.'),
                   '1 mark judgement linked to gradient value [1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c1b.add('C3', (2, 3, 4, 5), 'numerical')
def c1b_xsec(r, D):
    ci = r.choice([10, 20])
    n = r.choice([5, 6, 7])
    base = r.choice([20, 40, 60, 100])
    # heights at equally spaced points along X-Y (multiples of ci), single peak
    pk = r.randint(1, n - 2)
    hs = []
    for i in range(n):
        dist_from_pk = abs(i - pk)
        hs.append(base + ci * max(0, (n - 1 - dist_from_pk * r.choice([1, 2]))))
    if len(set(hs)) < 3:
        return None
    spacing = r.choice([250, 500])
    labels = [f'{i * spacing} m' for i in range(n)]
    top = max(hs)
    ipk = hs.index(top)
    stem = (f'A student draws a cross-section from X to Y. Heights read from the map every {spacing} m along the line are: '
            + '; '.join(f'{l} from X, {h} m' for l, h in zip(labels, hs)) + '.')
    left = hs[ipk] - hs[0]
    right = hs[ipk] - hs[-1]
    ldist = ipk * spacing
    rdist = (n - 1 - ipk) * spacing
    if left * rdist == right * ldist:
        return None
    steeper = 'X side' if left * rdist > right * ldist else 'Y side'
    parts = [
        lambda r: ('State the height and the distance from X of the highest point on the section.', f'{top} m at {ipk * spacing} m from X', '1 mark height; 1 mark distance [2]'),
        lambda r: ('Calculate the range of heights along the section.', f'{top - min(hs)} m', f'{top} − {min(hs)} = {top - min(hs)} m [1]'),
        lambda r: ('State which side of the highest point is steeper on average. Show your working.', cap(steeper),
                   f'X side: {left} m rise over {ldist} m; Y side: {right} m fall over {rdist} m; compare rise ÷ distance [2]'),
        lambda r: ('Describe how the student should complete the cross-section once the heights are plotted.', 'Join the points with a smooth curve (not straight lines), label X and Y and any features (e.g. river, road), and add a title and both scales.', '1 mark smooth line; 1 mark labels/scales [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 1.3 graphs and statistics
DATASETS = [
    ('rainfall (mm) at a weather station in {c}', 'mm', 'month', (20, 260)),
    ('number of pedestrians counted in 5 minutes at sites along a shopping street in {c}', '', 'site', (5, 120)),
    ('river velocity (m/s) at sites downstream along a river near {c}', ' m/s', 'site', None),
    ('daily maximum temperature (°C) recorded in {c}', ' °C', 'day', (18, 36)),
    ('number of vehicles per hour on a road into {c}', '', 'hour', (150, 900)),
    ('pebble length (mm) sampled along a beach near {c}', ' mm', 'sample', (12, 95)),
]


c1c = T('Describing and interpreting graphs, charts and statistical data', 'graphs charts statistical data')
build(c1c, {
    'terms': [
        ('mean', 'the average found by adding all the values and dividing by the number of values'),
        ('median', 'the middle value when all the values are placed in rank order'),
        ('mode', 'the value that occurs most often in a set of data'),
        ('range', 'the difference between the highest and the lowest values in a data set'),
        ('anomaly', 'a result that does not fit the general pattern or trend of the data'),
        ('positive correlation', 'a relationship in which one variable increases as the other increases'),
        ('negative correlation', 'a relationship in which one variable decreases as the other increases'),
        ('choropleth map', 'a map that uses different intensities of shading to show values for areas'),
        ('proportional symbol', 'a map symbol, such as a circle, whose size is drawn in proportion to the value it represents'),
        ('line of best fit', 'a straight line drawn through the middle of the points on a scatter graph to show the trend'),
    ],
    'mcq': [
        ('Which type of graph is best for showing change in a city’s population between 1950 and 2020?', 'Line graph', ['Pie chart', 'Scatter graph', 'Choropleth map'], 'Continuous change over time. [1]'),
        ('Which graph is best for showing whether there is a relationship between distance from a city centre and land value?', 'Scatter graph', ['Pie chart', 'Divided bar graph', 'Pictogram'], 'Two variables → scatter graph. [1]'),
        ('A pie chart has 360°. One category is 15% of the total. What angle should its sector be?', '54°', ['15°', '36°', '45°'], '0.15 × 360 = 54°. [1]'),
        ('Which statement about correlation is correct?', 'Correlation between two variables does not prove that one causes the other',
         ['A positive correlation proves cause and effect', 'A negative correlation means there is no relationship', 'Correlation can only be shown on a pie chart'], '[1]'),
        ('Which graph shows the direction and frequency of winds at a place?', 'Wind rose', ['Climate graph', 'Triangular graph', 'Population pyramid'], '[1]'),
        ('Which type of graph is used to show the percentages of three components that always add up to 100%, such as employment in three sectors?', 'Triangular graph', ['Line graph', 'Wind rose', 'Scatter graph'], '[1]'),
    ],
    'explain': [
        ('Explain why the median is sometimes a better average than the mean.', 'The median is not affected by extreme values (anomalies), so it better represents a typical value when data are uneven.', '1 mark median = middle value; 1 mark not distorted by extremes [2]'),
        ('Explain why a strong correlation on a scatter graph does not prove that one variable causes the other.', 'Both may be linked to a third factor, or the link may be coincidence; correlation only shows that they change together.', '1 mark third factor/coincidence; 1 mark correlation ≠ causation [2]'),
        ('Explain what you should include when describing the trend shown by a line graph.', 'The overall direction (increase/decrease), changes in rate, the highest and lowest points and any anomalies, with figures and dates quoted from the graph.', '1 mark trend; 1 mark use of data/units [2]'),
        ('Explain one advantage and one disadvantage of a choropleth map.', 'Advantage: shows the spatial pattern clearly at a glance. Disadvantage: suggests the value is the same across each whole area and hides variation within areas; sudden changes at boundaries.', '1 mark each [2]'),
        ('Explain why the range alone is not a good measure of the spread of data.', 'It uses only the two extreme values, so one anomaly can make the range very large and it ignores how the other values are distributed.', '1 mark uses extremes only; 1 mark affected by anomalies [2]'),
    ],
    'claims': [
        ('The range tells you the average value of a data set.', False, 'The range measures spread (highest minus lowest), not the average.'),
        ('A pie chart is the best way to show how rainfall changes through a year.', False, 'Change over time is best shown with a bar or line graph; pie charts show parts of a whole.'),
        ('If points on a scatter graph slope down from left to right, there is a negative correlation.', True, 'As one variable increases the other decreases.'),
        ('When describing a graph, you should quote figures with units.', True, 'Using data with units gives precise evidence and gains credit in 0460 mark schemes.'),
    ],
    'essays': [
        ('a single type of graph is enough to present the results of a geographical investigation',
         ['A simple bar or line graph may clearly show the main pattern.'],
         ['Different data need different techniques: scatter graphs for relationships, pie charts for proportions, maps for spatial patterns.', 'Combining graphs and maps (e.g. located bar graphs) shows both pattern and location.'],
         'Usually not: the best investigations choose a range of techniques suited to each type of data.',
         ['type of data', 'spatial patterns', 'relationships', 'clarity']),
    ],
})


@c1c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c1c_stats(r, D):
    desc, unit, lab, rng = r.choice(DATASETS)
    c = place(r, 'river' if 'river' in desc else 'coast' if 'beach' in desc else 'any')
    n = r.choice([7, 8, 9]) if D >= 3 else r.choice([5, 6, 7])
    if rng is None:
        vals = [round(r.uniform(0.2, 1.4), 2) for _ in range(n)]
        f = lambda x: fmt(round(x, 2), 2)
    else:
        vals = [r.randint(*rng) for _ in range(n)]
        f = lambda x: fmt(round(x, 1), 1)
    if len(set(vals)) < n:
        return None
    labels = MON[:n] if lab == 'month' else [f'{lab} {i + 1}' for i in range(n)]
    stem = f'The table shows {desc.format(c=c)}: ' + ', '.join(f'{l} {f(v)}' for l, v in zip(labels, vals)) + '.'
    mn, md, rg = mean(vals), median(vals), max(vals) - min(vals)
    if D == 1:
        opts, a = mcq(r, f(rg) + unit, [f(max(vals)) + unit, f(mn) + unit, f(md) + unit, f(min(vals)) + unit, f(rg + 1) + unit])
        return {'stem': stem + ' What is the range?', 'options': opts, 'answer': a, 'key': f'{f(max(vals))} − {f(min(vals))} = {f(rg)}{unit}. [1]'}
    srt = ', '.join(f(v) for v in sorted(vals))
    parts = [
        lambda r: ('Calculate the mean.', f(mn) + unit, f'{"+".join(f(v) for v in vals)} = {f(sum(vals))}; ÷ {n} = {f(mn)}{unit} [2]'),
        lambda r: ('Find the median.', f(md) + unit, f'Ranked: {srt}; middle value = {f(md)}{unit} [1]'),
        lambda r: ('Calculate the range.', f(rg) + unit, f'{f(max(vals))} − {f(min(vals))} = {f(rg)}{unit} [1]'),
        lambda r: ('Identify the ' + ('month' if lab == 'month' else lab) + ' with the highest value and state by how much it exceeds the mean.', f'{labels[vals.index(max(vals))]}, {f(max(vals) - mn)}{unit} above the mean', f'{f(max(vals))} − {f(mn)} = {f(max(vals) - mn)} [2]'),
        lambda r: ('Suggest one way of presenting these data and give a reason.', 'A bar graph, because the data are separate (discrete) categories that can be compared by bar height.' if lab != 'hour' and lab != 'month' else 'A bar or line graph against time, to show how values change through the period.', '1 mark technique; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


SERIES = [
    ('urban population of {c} (millions)', [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020], 'millions', 0.4, 2.2),
    ('international tourist arrivals to an island in the Caribbean (thousands)', [2000, 2004, 2008, 2012, 2016, 2020, 2024], 'thousands', 120, 900),
    ('area of mangrove forest along a coast near {c} (km²)', [1990, 1995, 2000, 2005, 2010, 2015, 2020], 'km²', 300, 900),
    ('annual rainfall at {c} (mm)', [2017, 2018, 2019, 2020, 2021, 2022, 2023], 'mm', 400, 1600),
    ('number of earthquakes above magnitude 4 recorded in a region per decade', [1950, 1960, 1970, 1980, 1990, 2000, 2010], '', 20, 90),
]


@c1c.add('C3', (2, 3, 4, 5), 'numerical')
def c1c_trend(r, D):
    desc, yrs, unit, lo, hi = r.choice(SERIES)
    c = place(r, 'tropical' if 'mangrove' in desc else 'any')
    n = len(yrs)
    v0 = r.uniform(lo, (lo + hi) / 2)
    vals = [v0]
    for _ in range(n - 1):
        vals.append(vals[-1] * r.uniform(0.85, 1.35))
    nd = 1 if unit in ('millions',) else 0
    vals = [round(v, nd) for v in vals]
    vals = [int(v) if nd == 0 else v for v in vals]
    if len(set(vals)) < n or vals[0] == 0:
        return None
    u = (' ' + unit) if unit else ''
    stem = f'Fig. 1.3 is a line graph showing the {desc.format(c=c)}. The values plotted are: ' + ', '.join(f'{y}: {fmt(v, 1)}' for y, v in zip(yrs, vals)) + '.'
    pc = pct_change(vals[0], vals[-1])
    gaps = [b - a for a, b in zip(vals, vals[1:])]
    k = max(range(n - 1), key=lambda i: gaps[i])
    parts = [
        lambda r: ('Describe the trend shown by Fig. 1.3. Use data in your answer.', trend_words([str(y) for y in yrs], vals, u), '1 mark overall trend; 1 mark change in rate/fluctuation; 1 mark data with units [3]'),
        lambda r: (f'Calculate the percentage change between {yrs[0]} and {yrs[-1]}.', f'{"+" if pc > 0 else ""}{dp(pc)}%', f'({fmt(vals[-1], 1)} − {fmt(vals[0], 1)}) ÷ {fmt(vals[0], 1)} × 100 = {dp(pc)}% [2]'),
        lambda r: ('Identify the period with the greatest increase.', f'{yrs[k]}-{yrs[k + 1]} (+{fmt(round(gaps[k], nd), 1)}{u})' if gaps[k] > 0 else 'There is no period of increase.', '[1]'),
        lambda r: ('Suggest why a line graph is suitable for these data.', 'The data are continuous over time, so a line shows the trend and rate of change between dates.', '[1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c1c.add('C3', (1, 2, 3, 4), 'numerical')
def c1c_pie(r, D):
    ctx = r.choice([('land use in a town', ['housing', 'industry', 'open space', 'shops and offices', 'roads']),
                    ('ways students travel to a school in {c}', ['walk', 'bus', 'car', 'bicycle', 'train']),
                    ('energy sources used to generate electricity in a country', ['coal', 'natural gas', 'hydro-electric', 'wind', 'solar']),
                    ('employment by sector in a region', ['primary', 'secondary', 'tertiary', 'quaternary'])])
    title, cats = ctx
    cats = cats[:r.choice([3, 4, len(cats)])] if len(cats) > 3 else cats
    k = len(cats)
    cuts = sorted(r.sample(range(1, 20), k - 1))
    pcts = [b - a for a, b in zip([0] + cuts, cuts + [20])]
    pcts = [p * 5 for p in pcts]
    if min(pcts) == 0:
        return None
    t = title.format(c=city(r))
    stem = f'A student surveys the {t}. Results (%): ' + ', '.join(f'{c} {p}%' for c, p in zip(cats, pcts)) + '.'
    i = r.randrange(k)
    ang = pcts[i] * 3.6
    if D == 1:
        opts, a = mcq(r, f'{fmt(ang, 1)}°', [f'{pcts[i]}°', f'{fmt(ang / 2, 1)}°', f'{fmt(ang * 2, 1)}°', f'{fmt(pcts[i] * 3, 1)}°'])
        return {'stem': stem + f' What angle should the sector for “{cats[i]}” be in a pie chart?', 'options': opts, 'answer': a, 'key': f'{pcts[i]} × 3.6 = {fmt(ang, 1)}°. [1]'}
    angs = [fmt(p * 3.6, 1) for p in pcts]
    parts = [
        lambda r: ('Calculate the angle of each sector for a pie chart.', ', '.join(f'{c} {a}°' for c, a in zip(cats, angs)), '% × 3.6 for each; total 360° [2]'),
        lambda r: ('Identify the largest category and state its share as a fraction in its simplest form.', f'{cats[pcts.index(max(pcts))]}: {_frac(max(pcts))}', '1 mark category; 1 mark fraction [2]'),
        lambda r: ('Suggest one other way of presenting these data and give one advantage of it.', 'A divided (compound) bar graph: it is easy to draw accurately and several surveys can be compared side by side.', '1 mark method; 1 mark advantage [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


def _frac(p):
    g = math.gcd(p, 100)
    return f'{p // g}/{100 // g}'


@c1c.add('C3', (2, 3, 4, 5), 'numerical')
def c1c_scatter(r, D):
    ctx = r.choice([('distance from the CBD (km)', 'land value ($ per m²)', -1, 'land is cheaper further from the CBD because accessibility falls'),
                    ('distance downstream (km)', 'channel width (m)', 1, 'the river gains water from tributaries, so discharge and width increase'),
                    ('GNI per capita (US$ thousands)', 'life expectancy (years)', 1, 'richer countries can afford more health care, clean water and food'),
                    ('distance from the volcano (km)', 'buildings damaged (%)', -1, 'ash fall, lava and pyroclastic flows are most intense close to the vent and weaken with distance'),
                    ('distance from the sea (km)', 'pebble size (mm)', 1, 'pebbles further up the beach are larger as only storm waves move them')])
    x, y, sgn, why = ctx
    n = 8
    xs = sorted(r.sample(range(1, 30), n))
    a = r.uniform(20, 60)
    b = r.uniform(1, 3) * sgn
    ys = [round(a + b * xi + r.uniform(-4, 4) + (60 if sgn < 0 else 0)) for xi in xs]
    anom = r.randrange(1, n - 1)
    ys[anom] += (25 if sgn < 0 else -25)
    if min(ys) <= 0 or ('%' in y and max(ys) >= 100):
        return None
    stem = f'Fig. 1.4 is a scatter graph of {y} against {x} for {n} places. Points (x, y): ' + ', '.join(f'({xi}, {yi})' for xi, yi in zip(xs, ys)) + '.'
    kind = 'negative' if sgn < 0 else 'positive'
    parts = [
        lambda r: ('Describe the relationship shown by Fig. 1.4.', f'A {kind} correlation: as {x.split(" (")[0]} increases, {y.split(" (")[0]} {"decreases" if sgn < 0 else "increases"}.', '1 mark type of correlation; 1 mark description with data [2]'),
        lambda r: ('Identify the anomaly and explain why it is an anomaly.', f'({xs[anom]}, {ys[anom]}): it lies far from the line of best fit and does not follow the {kind} trend.', '1 mark correct point; 1 mark reason [2]'),
        lambda r: ('Suggest a reason for the relationship.', cap(why) + '.', '1 mark reason; 1 mark development [2]'),
        lambda r: ('Explain how a line of best fit should be drawn on Fig. 1.4.', 'A straight line through the middle of the points with roughly equal numbers above and below, ignoring the anomaly; it need not pass through the origin.', '1 mark through the middle; 1 mark ignore anomaly [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 1.4 photographs and sketches
c1d = T('Interpreting photographs, satellite images and annotated sketches', 'photographs satellite images annotated sketches')
build(c1d, {
    'terms': [
        ('annotation', 'a detailed label on a sketch, map or photograph that explains or describes a feature'),
        ('label', 'a short name added to a diagram to identify a feature'),
        ('field sketch', 'a simple line drawing of a landscape made in the field, showing and annotating its main features'),
        ('foreground', 'the part of a photograph nearest to the camera'),
        ('background', 'the part of a photograph furthest from the camera'),
        ('satellite image', 'a picture of part of the Earth’s surface taken by a sensor on a satellite in orbit'),
        ('oblique aerial photograph', 'a photograph taken from the air at an angle, showing the side and top of features'),
        ('false-colour image', 'a satellite image in which colours are chosen to show features such as healthy vegetation, which may appear red'),
    ],
    'mcq': [
        ('What is the difference between a label and an annotation?', 'An annotation explains or describes a feature; a label only names it',
         ['They mean exactly the same', 'A label must include an arrow but an annotation must not', 'An annotation is only used on maps'], '[1]'),
        ('When describing a photograph, the part nearest the camera is called the', 'foreground', ['background', 'middle distance', 'horizon'], '[1]'),
        ('Which is the main advantage of satellite images for studying deforestation?', 'They show large areas repeatedly over time, so change can be measured',
         ['They show what people think about the forest', 'They are always cloud-free', 'They show soil nutrients directly'], '[1]'),
        ('A field sketch should mainly include', 'the main landforms and land uses, with labels and annotations', ['every tree and building in detail', 'colour shading only', 'the names of the people present'], '[1]'),
    ],
    'explain': [
        ('Explain why a field sketch can be more useful than a photograph.', 'It selects and simplifies the important features, which can be annotated to explain processes; photographs include irrelevant detail.', '1 mark selection/simplification; 1 mark annotations explain [2]'),
        ('Explain one advantage and one disadvantage of using satellite images in geography.', 'Advantage: cover large or remote areas and show change over time (e.g. floods, deforestation). Disadvantage: cloud can hide the ground; resolution may be too low for small features; they need interpretation.', '1 mark each [2]'),
        ('Describe how to use a photograph to estimate the height of a cliff.', 'Compare it with an object of known size in the photo (e.g. a person about 1.7 m tall, a house about 8 m) and estimate how many times taller the cliff is.', '1 mark object of known size; 1 mark multiply [2]'),
        ('Explain why it is useful to compare photographs of the same place taken in different years.', 'They show change over time, such as coastal erosion, urban growth or deforestation, and allow the rate of change to be estimated.', '1 mark change shown; 1 mark example/rate [2]'),
    ],
    'claims': [
        ('Annotations on a sketch should only name the features shown.', False, 'That is labelling; annotations add description or explanation, e.g. “wave-cut notch formed by hydraulic action”.'),
        ('A satellite image can show the extent of a flood that would be hard to see from the ground.', True, 'It covers a wide area at once, showing which land is under water.'),
        ('Everything in a photograph is shown at the same scale.', False, 'Objects in the background appear smaller than the same objects in the foreground.'),
    ],
    'cases': [
        (['Fig. 1.5 is a photograph of a coastline. In the foreground is a wide, rocky wave-cut platform exposed at low tide. In the middle distance a steep chalk cliff about 30 m high has a cave at its base and a narrow arch at the headland. In the background two isolated pillars of rock stand in the sea. Grass covers the cliff top, with a footpath close to the edge.',
          'Study Fig. 1.5, a photograph of a chalk headland. A rocky platform lies in front of a vertical cliff (about 30 m high) with a large cave at the bottom. At the end of the headland is an arch, and beyond it two stacks stand in the sea. A coastal path runs along the grassy cliff top.'],
         [('Identify two landforms of erosion shown in Fig. 1.5.', 'Any two: cliff, wave-cut platform, cave, arch, stack.', '1 mark each [2]'),
          ('Describe the cliff shown in Fig. 1.5.', 'Steep (vertical) chalk cliff about 30 m high, with a cave at its base; grass on top.', '1 mark steep; 1 mark height/rock/feature [2]'),
          ('Draw a labelled sketch to show the main features of the coastline. (Describe what your sketch would include.)', 'Outline of the cliff and headland; labels and annotations for wave-cut platform, cave, arch and stacks; sea and cliff-top path; title and direction of view.', '1 mark outline; 2 marks labelled features [3]'),
          ('Suggest one hazard for people using the footpath and explain it.', 'The path is close to the cliff edge; erosion and rock falls make the edge unstable, so people could fall.', '1 mark hazard; 1 mark explanation [2]'),
          ('Explain how the stacks in the background were formed.', 'Waves eroded a crack in the headland (hydraulic action, abrasion) into a cave, then through to form an arch; the arch roof collapsed by weathering and erosion, leaving the stack.', '1 mark cave; 1 mark arch; 1 mark collapse [3]')]),
        (['Fig. 1.6 is a pair of satellite images of the same area of tropical forest, taken in 2005 and 2025. In 2005 almost all the area is dark green forest with one road running east-west. In 2025 a “fishbone” pattern of light-coloured cleared strips runs north and south from the road; about 40% of the area is cleared, with small settlements and cattle pasture.',
          'Study Fig. 1.6, two satellite images of a rainforest area. The 2005 image shows continuous forest crossed by a single new road. By 2025, side roads branch off the main road and land on both sides has been cleared for pasture and crops, leaving about 60% of the forest.'],
         [('Describe the changes shown between the two images.', 'Forest cover fell from almost 100% to about 60%; clearings spread from the road in a fishbone pattern; settlements and pasture appeared.', '1 mark loss of forest with figure; 1 mark pattern along road; 1 mark new land use [3]'),
          ('Suggest why the clearing is concentrated near roads.', 'Roads give access for machinery and settlers and allow cattle, timber and crops to be transported to market.', '1 mark access; 1 mark transport to market [2]'),
          ('Explain one advantage of satellite images for monitoring deforestation.', 'They cover large, remote areas regularly so the rate and location of clearing can be measured and illegal clearing detected.', '1 mark coverage/repeat; 1 mark use [2]'),
          ('Suggest two impacts of the changes shown on the local environment.', 'Loss of habitat and biodiversity; soil erosion and nutrient loss; less evapotranspiration, so less rainfall; more CO₂ released.', '1 mark each [2]')]),
    ],
})


CHAPTERS[1] = [c1a, c1b, c1c, c1d]

# ============================================================== CHAPTER 2: Plate tectonics

BOUNDARIES = [
    ('the Mid-Atlantic Ridge through Iceland', 'Eurasian and North American', 'constructive', 'apart', 2.5),
    ('the East African Rift Valley', 'Somali (East African) and Nubian (African)', 'constructive', 'apart', 0.7),
    ('the west coast of South America (Andes)', 'Nazca and South American', 'destructive', 'together (oceanic plate subducted)', 7),
    ('the Japan Trench off north-east Japan', 'Pacific and North American (Okhotsk)', 'destructive', 'together (oceanic plate subducted)', 8),
    ('the Himalayas in Nepal', 'Indo-Australian and Eurasian', 'collision (destructive)', 'together (two continental plates)', 5),
    ('the San Andreas Fault in California', 'Pacific and North American', 'conservative', 'past each other', 4),
    ('the Sunda Trench south of Java, Indonesia', 'Indo-Australian and Eurasian', 'destructive', 'together (oceanic plate subducted)', 6),
    ('the Enriquillo fault zone in Haiti', 'Caribbean and North American', 'conservative', 'past each other', 2),
]
BFEAT = {'constructive': 'ocean ridges, rift valleys and gentle eruptions of runny basaltic lava from fissures and shield volcanoes, with frequent small, shallow earthquakes',
         'destructive': 'an ocean trench, explosive composite volcanoes and powerful earthquakes at a range of depths; tsunamis can occur',
         'collision (destructive)': 'fold mountains (the crust crumples upwards) and powerful earthquakes, but few or no volcanoes',
         'conservative': 'powerful shallow earthquakes along a fault, but no volcanoes because no crust is created or destroyed'}

c2a = T('Structure of the Earth and types of plate boundary: constructive, destructive and conservative', 'plate boundary constructive destructive conservative')
build(c2a, {
    'terms': [
        ('crust', 'the thin, solid outer layer of the Earth, 5-10 km thick under oceans and up to about 70 km under continents'),
        ('mantle', 'the thick layer of hot, mostly solid but slowly flowing rock between the crust and the core'),
        ('tectonic plate', 'a large, rigid section of the Earth’s crust and upper mantle that moves slowly over the mantle'),
        ('constructive plate boundary', 'a boundary where two plates move apart and new crust is formed as magma rises'),
        ('destructive plate boundary', 'a boundary where two plates move together and oceanic crust is subducted and destroyed'),
        ('conservative plate boundary', 'a boundary where two plates slide past each other and crust is neither created nor destroyed'),
        ('subduction zone', 'the area where a denser oceanic plate sinks beneath another plate into the mantle'),
        ('ocean trench', 'a deep, narrow depression in the sea floor where an oceanic plate is subducted'),
        ('convection current', 'the slow circular movement of heated mantle rock that helps to move tectonic plates'),
    ],
    'mcq': [
        ('Why does oceanic crust sink beneath continental crust at a destructive boundary?', 'Oceanic crust is denser', ['Oceanic crust is thicker', 'Continental crust is hotter', 'Oceanic crust is older and harder'], 'Basaltic oceanic crust is denser than granitic continental crust. [1]'),
        ('At which type of plate boundary do fold mountains such as the Himalayas form?', 'Collision boundary between two continental plates', ['Constructive boundary', 'Conservative boundary', 'Hotspot'], '[1]'),
        ('Which boundary type has earthquakes but no volcanoes?', 'Conservative', ['Constructive', 'Destructive (oceanic-continental)', 'Mid-ocean ridge'], 'No magma rises where plates slide past each other. [1]'),
        ('Which layer of the Earth is made of solid iron and nickel?', 'Inner core', ['Outer core', 'Mantle', 'Crust'], 'The outer core is liquid. [1]'),
        ('Iceland lies on which type of plate boundary?', 'Constructive', ['Destructive', 'Conservative', 'Collision'], 'Mid-Atlantic Ridge: Eurasian and North American plates move apart. [1]'),
        ('Roughly how thick is oceanic crust?', '5-10 km', ['25-70 km', '500 km', '2900 km'], '[1]'),
    ],
    'explain': [
        ('Explain why volcanoes form at destructive plate boundaries.', 'The oceanic plate is subducted into the mantle; friction and heat (and water released from the sinking plate) melt rock to form magma, which rises through cracks in the overriding plate and erupts.', '1 mark subduction; 1 mark melting; 1 mark magma rises [3]'),
        ('Explain why earthquakes occur at conservative boundaries.', 'The plates move past each other but friction makes them stick; stress builds up until the rocks suddenly slip, releasing energy as seismic waves.', '1 mark plates stick; 1 mark stress released suddenly [2]'),
        ('Describe the differences between oceanic and continental crust.', 'Oceanic: thinner (5-10 km), denser (basalt), younger, can be subducted. Continental: thicker (up to 70 km), less dense (granite), older, not subducted.', '1 mark each valid comparison up to [3]'),
        ('Explain how plates move.', 'Heat from the core creates convection currents in the mantle that drag plates; slab pull (sinking plates pull the rest) and ridge push at mid-ocean ridges also move plates.', '1 mark convection; 1 mark slab pull/ridge push [2]'),
        ('Explain why new crust forms at constructive boundaries.', 'As plates move apart, pressure falls and mantle rock partly melts; magma rises into the gap, erupts and cools to form new basaltic crust (e.g. the Mid-Atlantic Ridge).', '1 mark plates apart; 1 mark magma fills gap and cools [2]'),
    ],
    'claims': [
        ('The mantle is a layer of liquid lava.', False, 'The mantle is mostly solid rock that flows very slowly; only small amounts melt to form magma.'),
        ('Continental crust is less dense than oceanic crust.', True, 'Continental crust is mainly granite and oceanic crust is basalt, so oceanic crust is subducted.'),
        ('Earthquakes only happen at destructive plate boundaries.', False, 'They occur at all types of boundary, including constructive and conservative.'),
        ('Plates move at a rate of a few centimetres per year.', True, 'Typical rates are 2-10 cm per year, about the speed fingernails grow.'),
    ],
    'cases': [
        (['Fig. 2.1 is a world map showing plate boundaries. Boundary A runs north-south down the middle of the Atlantic Ocean; arrows point away from it. Boundary B runs along the west coast of South America; an arrow on the Nazca plate points east towards the South American plate. Boundary C runs through California; arrows on each side point in opposite directions parallel to the boundary.',
          'Study Fig. 2.1, a map of plate boundaries. At A, in the Atlantic, the plates move apart. At B, off Chile and Peru, the Nazca plate moves towards the South American plate and a deep trench lies offshore. At C, the San Andreas Fault, the Pacific and North American plates move side by side.'],
         [('Name the type of plate boundary at A, B and C.', 'A constructive; B destructive; C conservative.', '1 mark for two correct, 2 marks for three [2]'),
          ('Explain why there is a deep ocean trench at B.', 'The denser oceanic Nazca plate bends and is subducted beneath the continental South American plate, forming a trench.', '1 mark subduction; 1 mark denser oceanic plate [2]'),
          ('Describe the landforms and hazards found at A.', 'A mid-ocean ridge with fissure eruptions of runny basaltic lava, shield volcanoes (e.g. Iceland) and small shallow earthquakes.', '1 mark landform; 1 mark hazard [2]'),
          ('Explain why there are no volcanoes at C.', 'Crust is neither created nor destroyed; the plates slide past each other, so no magma is produced.', '1 mark no subduction/rifting; 1 mark no magma [2]'),
          ('Suggest why boundary B is more hazardous to people than boundary A.', 'B has explosive volcanoes and very large earthquakes and tsunamis near cities such as Santiago and Lima; A is mostly under the ocean with gentle eruptions.', '1 mark hazard size; 1 mark population exposed [2]')]),
    ],
    'essays': [
        ('destructive plate boundaries are more hazardous to people than constructive plate boundaries',
         ['They produce the largest earthquakes (Tōhoku 2011, magnitude 9.0), tsunamis and explosive eruptions (Merapi 2010).', 'Many densely populated cities lie near them, e.g. Tokyo, Jakarta, Lima.'],
         ['Constructive boundaries can be hazardous: Eyjafjallajökull (2010) disrupted about 100 000 flights; Laki (1783) caused famine.', 'Conservative boundaries also cause deadly earthquakes (Haiti 2010).', 'Risk depends on vulnerability and preparation as much as boundary type.'],
         'Generally true because of the scale of hazards at subduction zones, but the impact depends on population and level of development.',
         ['types of eruption', 'earthquake magnitude', 'population density', 'Iceland']),
    ],
})


@c2a.add('C3', (1, 2, 3, 4), 'numerical')
def c2a_rate(r, D):
    where, plates, btype, move, rate = r.choice(BOUNDARIES)
    yrs = r.choice([1000, 10000, 100000, 1000000, 5000000])
    km = rate * yrs / 100000
    ys = f'{yrs:,}'.replace(',', ' ')
    stem = f'At {where}, the {plates} plates move {move.split(" (")[0]} at about {fmt(rate, 1)} cm per year.'
    if D == 1:
        opts, a = mcq(r, f'{fmt(km, 3)} km', [f'{fmt(km * 10, 3)} km', f'{fmt(km / 10, 4)} km', f'{fmt(km * 100, 2)} km', f'{fmt(rate * yrs / 1000, 2)} km'])
        return {'stem': stem + f' How far will they move in {ys} years?', 'options': opts, 'answer': a, 'key': f'{fmt(rate, 1)} × {ys} = {fmt(rate * yrs, 0)} cm ÷ 100 000 = {fmt(km, 3)} km. [1]'}
    parts = [
        lambda r: (f'Calculate how far the plates move in {ys} years. Give your answer in km.', f'{fmt(km, 3)} km', f'{fmt(rate, 1)} × {ys} = {fmt(rate * yrs, 0)} cm; ÷ 100 000 = {fmt(km, 3)} km [2]'),
        lambda r: ('Name the type of plate boundary.', cap(btype), '[1]'),
        lambda r: ('Describe the landforms and hazards found at this type of boundary.', cap(BFEAT[btype]) + '.', '1 mark landform; 1 mark hazard [2]'),
        lambda r: ('Explain what causes the plates to move.', 'Convection currents in the mantle, driven by heat from the core, together with slab pull and ridge push.', '1 mark convection; 1 mark heat source/slab pull [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c2a.add('C2', (1, 2, 3), 'short')
def c2a_which(r, D):
    where, plates, btype, move, rate = r.choice(BOUNDARIES)
    if D == 1:
        opts, a = mcq(r, cap(btype), [cap(b) for b in ['constructive', 'destructive', 'conservative', 'collision (destructive)'] if b != btype])
        return {'stem': f'At {where}, the {plates} plates move {move}. Which type of plate boundary is this?', 'options': opts, 'answer': a, 'key': f'{cap(btype)}. [1]'}
    return {'stem': f'At {where}, the {plates} plates move {move}. Identify the type of plate boundary and explain what landforms and hazards you would expect there.',
            'answer': f'{cap(btype)} boundary: {BFEAT[btype]}.', 'key': '1 mark boundary type; 1 mark landform; 1 mark hazard linked to process [3]', 'marks': 3}


# --------------------------------------------------------------- 2.2 earthquakes
QUAKES = {
    'the Gorkha earthquake, Nepal, 2015': dict(date='25 April 2015', mag=7.8, depth=15, deaths=9000, where='about 80 km north-west of Kathmandu', plate='the Indo-Australian plate moving north into the Eurasian plate (collision boundary)', income='LIC',
        effects='About 9000 deaths and 22 000 injured; over 600 000 houses and historic temples in Kathmandu destroyed; landslides blocked roads and cut off mountain villages; an avalanche on Everest killed 19 climbers; tourism income collapsed.',
        responses='International search-and-rescue teams and aid from India, China and the UK; helicopters reached remote villages; tents and water purification supplied; later a National Reconstruction Authority rebuilt houses slowly, many to earthquake-resistant designs.'),
    'the Tōhoku earthquake, Japan, 2011': dict(date='11 March 2011', mag=9.0, depth=30, deaths=18000, where='about 70 km off the north-east coast of Honshu', plate='the Pacific plate subducting beneath the plate under northern Japan (destructive boundary)', income='HIC',
        effects='About 18 000 dead or missing, over 90% drowned by tsunami waves up to about 40 m high; towns such as Minamisanriku destroyed; meltdowns at Fukushima Daiichi nuclear plant and over 150 000 people evacuated; damage of about US$235 billion.',
        responses='Earthquake early warning stopped bullet trains and sent alerts; strict building codes meant most buildings survived the shaking; the Self-Defence Forces led rescue; higher sea walls and relocation of homes to higher ground followed.'),
    'the Haiti earthquake, 2010': dict(date='12 January 2010', mag=7.0, depth=13, deaths=220000, where='about 25 km west of the capital, Port-au-Prince', plate='the Caribbean and North American plates sliding past each other (conservative boundary)', income='LIC',
        effects='Estimates of deaths range from about 100 000 to over 220 000; about 1.5 million people homeless; the presidential palace, hospitals and port destroyed; a cholera outbreak began later in 2010.',
        responses='Aid was slow because the port and airport were damaged and government buildings destroyed; the USA took control of the airport; tent camps housed hundreds of thousands for years; reconstruction relied on foreign aid.'),
    'the Christchurch earthquake, New Zealand, 2011': dict(date='22 February 2011', mag=6.2, depth=5, deaths=185, where='about 10 km south-east of the city centre', plate='stresses near the boundary of the Pacific and Australian plates', income='HIC',
        effects='185 deaths, most in the collapse of two office buildings; liquefaction damaged homes in eastern suburbs; the cathedral spire fell; the city centre was closed for over two years.',
        responses='Civil Defence emergency declared; international rescue teams; the government bought out homes on land damaged by liquefaction (red zone) and rebuilt the centre to stronger codes.'),
}

c2b = T('Causes of earthquakes and features: focus, epicentre and magnitude scales', 'focus epicentre magnitude scales')
build(c2b, {
    'terms': [
        ('focus', 'the point underground where rocks break and an earthquake starts'),
        ('epicentre', 'the point on the Earth’s surface directly above the focus of an earthquake'),
        ('seismic waves', 'waves of energy released by an earthquake that travel outwards from the focus'),
        ('magnitude', 'a measure of the energy released by an earthquake, usually on the moment magnitude scale'),
        ('seismometer', 'an instrument that detects and records ground shaking caused by seismic waves'),
        ('Mercalli scale', 'a scale from I to XII that measures the intensity of an earthquake from its observed effects on people and buildings'),
        ('aftershock', 'a smaller earthquake that follows the main earthquake as the rocks settle'),
        ('liquefaction', 'when shaking makes waterlogged sediment behave like a liquid, so buildings sink or tilt'),
        ('tsunami', 'a series of large sea waves caused by sudden movement of the sea floor, usually by an earthquake'),
    ],
    'mcq': [
        ('On the moment magnitude scale, a magnitude 7 earthquake releases about how much more energy than a magnitude 6?', 'About 32 times more', ['About 2 times more', 'About 10 times less', 'The same'], 'Each whole number ≈ 32× energy, 10× ground motion. [1]'),
        ('Where is shaking usually strongest in an earthquake?', 'At the epicentre', ['At the focus deep underground', '100 km from the epicentre', 'At the nearest plate boundary on the other side of the ocean'], '[1]'),
        ('Which earthquake had the highest magnitude?', 'Tōhoku, Japan, 2011', ['Haiti, 2010', 'Christchurch, New Zealand, 2011', 'Gorkha, Nepal, 2015'], 'Mw 9.0, compared with 7.0, 6.2 and 7.8. [1]'),
        ('Which scale measures earthquake intensity from observed damage?', 'Mercalli scale', ['Moment magnitude scale', 'Beaufort scale', 'Volcanic Explosivity Index'], '[1]'),
        ('A shallow-focus earthquake usually has its focus less than', '70 km deep', ['700 km deep', '7000 km deep', '1 km deep'], 'Shallow: 0-70 km; intermediate: 70-300 km; deep: 300-700 km. [1]'),
    ],
    'explain': [
        ('Explain the difference between the focus and the epicentre of an earthquake.', 'The focus is the point underground where rocks break and energy is released; the epicentre is the point on the surface directly above the focus.', '1 mark each [2]'),
        ('Explain why shallow-focus earthquakes usually cause more damage than deep-focus ones.', 'Seismic waves travel a shorter distance to the surface and lose less energy, so surface shaking is stronger.', '1 mark shorter distance; 1 mark stronger shaking [2]'),
        ('Explain how an earthquake at sea can cause a tsunami.', 'Sudden uplift of the sea floor at a subduction zone displaces a huge volume of water; the waves travel quickly across the ocean and grow taller as they reach shallow water near the coast.', '1 mark displacement; 1 mark wave height increases in shallow water [2]'),
        ('Explain why the number of deaths from an earthquake does not depend only on its magnitude.', 'It also depends on depth, distance to cities, population density, building quality, time of day, preparedness and speed of rescue; e.g. Haiti 2010 (7.0) killed far more than Tōhoku 2011 (9.0) killed in collapsing buildings.', '1 mark factors; 1 mark example [2]'),
        ('Explain the difference between magnitude and intensity.', 'Magnitude measures the energy released at the source (one value per earthquake); intensity (Mercalli) measures the effects at a place and decreases away from the epicentre.', '1 mark each [2]'),
    ],
    'claims': [
        ('An earthquake of magnitude 8 is twice as powerful as one of magnitude 4.', False, 'The scale is logarithmic: each whole number is about 32 times more energy, so magnitude 8 releases about a million times more energy.'),
        ('Most deaths in earthquakes are caused by collapsing buildings rather than the ground shaking itself.', True, 'Collapsing buildings, fires, landslides and tsunamis cause most deaths.'),
        ('A tsunami is a single giant wave.', False, 'A tsunami is a series of waves, and the first is not always the largest.'),
        ('Earthquakes can be accurately predicted to the day.', False, 'Scientists can identify high-risk areas but cannot predict the exact time of an earthquake.'),
    ],
    'cs': [
        ('an earthquake', [(n, {'causes': f'On {q["date"]} an earthquake of magnitude {q["mag"]} struck {q["where"]}, at a focus depth of about {q["depth"]} km. It was caused by {q["plate"]}: friction locked the plates, stress built up and was released suddenly as seismic waves.',
                                 'effects': q['effects'], 'responses': q['responses']}) for n, q in QUAKES.items()],
         [('explain the causes of the earthquake', 'causes', 'Plate boundary type and plates named; locking/friction; build-up and sudden release of stress; focus depth and location of epicentre.'),
          ('describe the impacts of the earthquake on people and the environment', 'effects', 'Primary effects (deaths, building collapse) and secondary effects (fires, landslides, tsunami, disease, economic loss), with figures.'),
          ('describe and explain the primary and secondary effects of the earthquake', 'effects', 'Classify effects correctly as primary (shaking, collapse) or secondary (tsunami, fire, landslides, disease, homelessness).')]),
    ],
    'essays': [
        ('secondary effects of earthquakes are more serious than primary effects',
         ['Tōhoku (2011): the tsunami caused over 90% of deaths and the Fukushima nuclear accident.', 'Haiti (2010): cholera killed thousands in the months after.'],
         ['In Nepal (2015) and Haiti most deaths came from buildings collapsing during the shaking.', 'Primary effects destroy the infrastructure needed for recovery.'],
         'It depends on the event: for coastal subduction earthquakes secondary effects are often worse; for inland earthquakes primary effects usually dominate.',
         ['Tōhoku 2011', 'Nepal 2015', 'Haiti 2010', 'long-term economic effects']),
    ],
})


@c2b.add('C3', (1, 2, 3, 4), 'numerical')
def c2b_mag(r, D):
    m1 = r.choice([4.5, 5.0, 5.5, 5.8, 6.0, 6.2, 6.5])
    d = r.choice([1, 2, 3])
    m2 = m1 + d
    e, a = 32 ** d, 10 ** d
    es, as_ = f'{e:,}'.replace(',', ' '), f'{a:,}'.replace(',', ' ')
    stem = f'Earthquake P had a magnitude of {fmt(m1, 1)} and earthquake Q a magnitude of {fmt(m2, 1)}. Each increase of 1 on the magnitude scale means about 10 times more ground movement and about 32 times more energy released.'
    if D == 1:
        opts, ans = mcq(r, f'About {es} times', [f'About {d * 32} times', f'About {as_} times', f'About {d} times', f'About {2 * d} times'])
        return {'stem': stem + ' About how many times more energy did Q release than P?', 'options': opts, 'answer': ans, 'key': f'32^{d} = {es}. [1]'}
    parts = [
        lambda r: ('Calculate how many times more energy earthquake Q released.', f'about {es} times', f'32^{d} = {es} [2]'),
        lambda r: ('Calculate how many times greater the ground movement was in Q.', f'{as_} times', f'10^{d} = {as_} [1]'),
        lambda r: ('Explain why earthquake P could still cause more deaths than earthquake Q.', 'P might be shallow and close to a densely populated city with poorly built houses and little preparation, while Q might be deep, remote or in a well-prepared HIC.', '1 mark each factor up to [3]'),
        lambda r: ('Name the instrument used to measure earthquake magnitude.', 'A seismometer (seismograph).', '[1]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


@c2b.add('C3', (2, 3, 4, 5), 'case')
def c2b_table(r, D):
    names = r.sample(list(QUAKES), 3)
    rows = [(n, QUAKES[n]) for n in names]
    stem = 'Table 2.1 gives data for three earthquakes. ' + ' '.join(f'{cap(n)}: magnitude {q["mag"]}, focus depth {q["depth"]} km, deaths about {nf(q["deaths"])}, {q["income"]}.' for n, q in rows)
    hi = max(rows, key=lambda x: x[1]['mag'])
    hd = max(rows, key=lambda x: x[1]['deaths'])
    parts = [
        lambda r: ('Identify the earthquake with the highest magnitude.', cap(hi[0]), '[1]'),
        lambda r: ('Calculate how many times more deaths there were in the deadliest earthquake than in the least deadly.', f'{fmt(hd[1]["deaths"] / min(q["deaths"] for _, q in rows), 1)} times',
                   f'{hd[1]["deaths"]} ÷ {min(q["deaths"] for _, q in rows)} = {fmt(hd[1]["deaths"] / min(q["deaths"] for _, q in rows), 1)} [2]'),
        lambda r: ('Using the table, suggest whether there is a clear link between magnitude and number of deaths.', 'No clear link: ' + ('the highest-magnitude earthquake was not the deadliest; ' if hi[0] != hd[0] else 'although the strongest was also the deadliest, ') + 'deaths also depend on level of development, building quality, depth and population.', '1 mark judgement; 1 mark use of data [2]'),
        lambda r: ('Explain why earthquakes in LICs often cause more deaths than those in HICs.', 'Poorly constructed buildings, little enforcement of building codes, dense informal settlements, weak emergency services and limited money for preparation and rescue.', '1 mark each point up to [3]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


# --------------------------------------------------------------- 2.3 volcanoes
VOLCS = [
    ('Mauna Loa, Hawaii', 'shield', 'a hotspot in the middle of the Pacific plate', 'runny basaltic lava, gentle effusive eruptions, lava flows'),
    ('Kīlauea, Hawaii', 'shield', 'a hotspot in the middle of the Pacific plate', 'frequent effusive eruptions; in 2018 lava flows destroyed about 700 homes'),
    ('Mount Merapi, Indonesia', 'composite', 'a destructive boundary where the Indo-Australian plate subducts beneath the Eurasian plate', 'viscous andesitic lava, lava domes that collapse into pyroclastic flows; the 2010 eruption killed about 350 people'),
    ('Mount Pinatubo, Philippines', 'composite', 'a destructive boundary where the Eurasian (Philippine Sea region) plate subducts', 'the explosive 1991 eruption sent ash 35 km high; lahars followed; global temperatures fell by about 0.5 °C'),
    ('Mount St Helens, USA', 'composite', 'a destructive boundary where the Juan de Fuca plate subducts beneath the North American plate', 'the 1980 lateral blast removed the north side of the mountain; 57 deaths'),
    ('Eyjafjallajökull, Iceland', 'composite (stratovolcano on a constructive boundary)', 'the Mid-Atlantic Ridge, where the Eurasian and North American plates move apart', 'the 2010 eruption under a glacier produced fine ash that closed European airspace for six days'),
    ('Mount Etna, Italy', 'composite', 'a complex area where the African plate moves towards the Eurasian plate', 'frequent eruptions of lava fountains and flows; fertile slopes are farmed for vines and citrus'),
]

c2c = T('Types of volcano and features of eruptions', 'types of volcano features of eruptions')
build(c2c, {
    'terms': [
        ('magma', 'molten rock below the Earth’s surface'),
        ('lava', 'molten rock that has erupted onto the Earth’s surface'),
        ('shield volcano', 'a broad volcano with gentle slopes built from layers of runny basaltic lava'),
        ('composite volcano', 'a steep-sided cone made of alternate layers of ash and viscous lava, with explosive eruptions'),
        ('crater', 'the bowl-shaped hollow at the top of a volcano around the vent'),
        ('vent', 'the opening through which magma, gas and ash erupt'),
        ('pyroclastic flow', 'a fast-moving cloud of very hot gas, ash and rock that flows down the side of a volcano'),
        ('lahar', 'a mudflow of volcanic ash and water that rushes down valleys on a volcano'),
        ('viscosity', 'how thick and sticky a liquid is; viscous magma flows slowly and traps gas'),
        ('dormant volcano', 'a volcano that has not erupted for a long time but could erupt again'),
    ],
    'mcq': [
        ('Which type of volcano has gentle slopes and runny basaltic lava?', 'Shield volcano', ['Composite volcano', 'Caldera only', 'Cinder cone formed by explosions'], '[1]'),
        ('Why are eruptions at destructive boundaries often explosive?', 'The magma is viscous and traps gas until pressure builds up', ['The magma is very runny', 'The lava is cold', 'There is no gas in the magma'], '[1]'),
        ('Which volcanic hazard is a mixture of ash and water flowing down valleys?', 'Lahar', ['Pyroclastic flow', 'Lava bomb', 'Ash cloud'], '[1]'),
        ('Mauna Loa in Hawaii is an example of', 'a shield volcano over a hotspot', ['a composite volcano at a destructive boundary', 'a volcano on a conservative boundary', 'an extinct volcano'], '[1]'),
        ('Which feature of an eruption caused European airspace to close in 2010?', 'Fine volcanic ash from Eyjafjallajökull', ['Lava flows reaching France', 'A tsunami', 'Lahars in Italy'], '[1]'),
    ],
    'explain': [
        ('Explain why composite volcanoes have steep sides.', 'Their lava is viscous and does not flow far before cooling, so it builds up close to the vent with layers of ash.', '1 mark viscous lava cools quickly; 1 mark builds near vent/ash layers [2]'),
        ('Explain why shield volcanoes have gentle slopes.', 'Runny, low-silica basaltic lava flows long distances before solidifying, spreading out into a wide, low dome.', '1 mark runny lava; 1 mark flows far [2]'),
        ('Explain how pyroclastic flows form and why they are so dangerous.', 'An eruption column collapses or a lava dome breaks up, sending hot gas, ash and rock down the slope at over 100 km/h and several hundred °C; there is no time to escape and they burn and bury everything.', '1 mark formation; 1 mark speed/temperature [2]'),
        ('Explain how lahars can affect places many kilometres from a volcano.', 'Ash mixes with rain or meltwater from snow and glaciers; the mudflow follows river valleys at high speed, burying towns and bridges far downstream (e.g. Armero, Colombia, 1985).', '1 mark formation; 1 mark travel along valleys [2]'),
        ('Compare the hazards of shield volcanoes and composite volcanoes.', 'Shield: mainly slow lava flows that destroy property but rarely kill. Composite: explosive eruptions with ash, pyroclastic flows, lahars and volcanic bombs that can kill many people.', '1 mark each; 1 mark comparison [3]'),
    ],
    'claims': [
        ('All volcanoes erupt explosively.', False, 'Shield volcanoes erupt runny basaltic lava gently; explosive eruptions are typical of composite volcanoes.'),
        ('Lava flows are usually the deadliest volcanic hazard.', False, 'Most lava flows are slow enough to walk away from; pyroclastic flows and lahars kill far more people.'),
        ('Volcanoes can form away from plate boundaries.', True, 'Hotspots such as Hawaii form where a plume of hot mantle rises under the middle of a plate.'),
        ('A dormant volcano can never erupt again.', False, 'Dormant volcanoes are inactive but could erupt; extinct ones are not expected to erupt.'),
    ],
    'cs': [
        ('a volcanic eruption', [
            ('Mount Merapi, Indonesia, 2010', {'causes': 'Merapi is a composite volcano on the destructive boundary where the Indo-Australian plate subducts beneath the Eurasian plate; melting produces viscous, gas-rich magma that builds lava domes; in October-November 2010 dome collapses produced pyroclastic flows.',
                                              'effects': 'About 350 people died, mostly in pyroclastic flows; about 350 000 evacuated; villages and farmland on the slopes buried; ash closed Yogyakarta airport; lahars in the rainy season damaged bridges and homes.',
                                              'responses': 'Monitoring by Indonesia’s volcano agency raised the alert level and widened the exclusion zone to 20 km, saving many lives; evacuation centres housed people; some villages were relocated.'}),
            ('Eyjafjallajökull, Iceland, 2010', {'causes': 'Iceland lies on the Mid-Atlantic Ridge, a constructive boundary where the Eurasian and North American plates move apart; magma rose beneath an ice cap, and meltwater chilled it, making the eruption explosive and producing fine ash.',
                                                'effects': 'No deaths; about 800 people evacuated; meltwater floods damaged roads; ash closed European airspace for six days and about 100 000 flights were cancelled, costing airlines over US$1.7 billion; Kenyan flower exporters lost sales.',
                                                'responses': 'Rapid evacuation using warnings; roads breached to let floodwater pass; airspace closures; later new rules on safe ash levels for aircraft.'}),
            ('Kīlauea, Hawaii, 2018', {'causes': 'Kīlauea is a shield volcano above a hotspot in the middle of the Pacific plate; runny basaltic lava erupted from fissures on its eastern rift zone.',
                                       'effects': 'Lava flows destroyed about 700 homes and covered roads and farmland; volcanic gas (vog) affected health; no deaths.',
                                       'responses': 'Evacuation orders, monitoring by the Hawaiian Volcano Observatory, emergency shelters and government grants to residents.'}),
        ], [
            ('explain the causes of the eruption', 'causes', 'Plate setting/hotspot; magma formation; type of magma and explosivity.'),
            ('describe the impacts of the eruption on people and the environment', 'effects', 'Deaths, evacuation, damage to homes/farmland/transport, economic losses, environmental effects (ash, lahars, gas).'),
            ('describe how people responded to the eruption', 'responses', 'Monitoring, warnings, evacuation, shelters, aid, longer-term planning.'),
        ]),
    ],
})


@c2c.add('C2', (1, 2, 3, 4), 'short')
def c2c_type(r, D):
    v, typ, setting, feat = r.choice(VOLCS)
    if D <= 1:
        opts, a = mcq(r, 'Shield' if typ == 'shield' else 'Composite', ['Shield' if typ != 'shield' else 'Composite', 'Fold mountain', 'Ocean trench', 'Rift valley'])
        return {'stem': f'{v} lies at {setting}. Its eruptions are described as: {feat}. What type of volcano is it?', 'options': opts, 'answer': a, 'key': f'{cap(typ)}. [1]'}
    return {'stem': f'{v} lies at {setting}. Its eruptions are described as: {feat}. Identify the type of volcano and explain how its plate setting produces this type of eruption.',
            'answer': f'{cap(typ)} volcano. ' + ('Runny, low-silica basaltic magma rises from the mantle and lets gas escape easily, so eruptions are effusive and build gentle slopes.' if typ == 'shield' else
                                                'Viscous, gas-rich magma (from melting of subducted crust, or chilled by ice) traps gas until pressure builds, so eruptions are explosive and build steep layered cones.'),
            'key': '1 mark type; 1 mark magma type/viscosity; 1 mark link to eruption style [3]', 'marks': 3}


@c2c.add('C3', (2, 3, 4, 5), 'case')
def c2c_fig(r, D):
    v, typ, setting, feat = r.choice([x for x in VOLCS if x[1] != 'shield'])
    dist = r.choice([5, 8, 10, 12, 15])
    zone = r.choice([10, 15, 20])
    pop = r.choice([40, 60, 80, 120])
    stem = (f'Fig. 2.2 is a cross-section of {v}, a {typ.split(" (")[0]} volcano at {setting}. It shows a central vent, a crater, alternate layers of ash and lava, and a secondary vent on the flank. '
            f'A town of {pop} 000 people lies {dist} km from the summit, and the authorities have set an exclusion zone of {zone} km.')
    inside = dist <= zone
    parts = [
        lambda r: ('Label three features that would be shown on Fig. 2.2 and describe each briefly.', 'Main vent (opening for magma); crater (hollow at summit); layers of ash and lava (alternate eruptions); magma chamber; secondary vent/side cone.', '1 mark each feature with description [3]'),
        lambda r: ('State whether the town is inside the exclusion zone and how many people would need to be evacuated.', (f'Inside: all {pop} 000 people would need to evacuate.' if inside else f'Outside ({dist} km > {zone} km): no compulsory evacuation, though people should be ready to leave.'), '1 mark judgement using distances; 1 mark figure [2]'),
        lambda r: ('Describe two hazards the town could face in an eruption.', 'Ash fall collapsing roofs and damaging crops and lungs; pyroclastic flows; lahars along river valleys; volcanic bombs; gases.', '1 mark each hazard with brief description [2]'),
        lambda r: ('Explain why the volcano erupts explosively.', 'Its magma is viscous and gas-rich; gas cannot escape easily, so pressure builds until it is released violently.', '1 mark viscous; 1 mark gas pressure [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


# --------------------------------------------------------------- 2.4 why people live in hazard zones
c2d = T('Why people live in tectonic hazard zones', 'live tectonic hazard zones')
build(c2d, {
    'terms': [
        ('hazard', 'a natural event that threatens people, property and the environment'),
        ('risk', 'the likelihood that a hazard will cause loss of life or damage to property'),
        ('vulnerability', 'how exposed and unable to cope a person or community is when a hazard occurs'),
        ('geothermal energy', 'heat from inside the Earth used to generate electricity or heat buildings'),
        ('fertile soil', 'soil rich in nutrients and minerals, such as that formed by weathered volcanic ash and lava'),
        ('capacity to cope', 'the ability of a community to prepare for, respond to and recover from a hazard'),
        ('perception of risk', 'how serious people believe a hazard is, which may differ from the actual risk'),
    ],
    'mcq': [
        ('Which is the main reason farmers live on the slopes of volcanoes such as Merapi and Etna?', 'Weathered volcanic material forms fertile soils', ['The climate is always cooler there', 'There are no hazards', 'The land is completely flat'], '[1]'),
        ('Which country generates about a quarter of its electricity and heats about 90% of its homes using geothermal energy?', 'Iceland', ['Nepal', 'Haiti', 'Egypt'], '[1]'),
        ('Which of these increases people’s vulnerability to earthquakes?', 'Living in poorly built, unreinforced houses', ['Earthquake drills in schools', 'Strict building codes', 'An early warning system'], '[1]'),
        ('Which is an economic reason for living near volcanoes?', 'Tourism and the mining of minerals such as sulphur', ['Volcanoes prevent earthquakes', 'Land near volcanoes is never farmed', 'Volcanoes stop rainfall'], '[1]'),
    ],
    'explain': [
        ('Explain why many people continue to live near active volcanoes.', 'Fertile volcanic soils give high crop yields; geothermal energy and tourism provide jobs and income; minerals can be mined; families have lived there for generations; eruptions are infrequent and many can be predicted.', '1 mark each developed reason up to [3]'),
        ('Explain why many large cities have grown on or near plate boundaries.', 'Coastal sites and natural harbours, flat land, routes and trade grew there long before risks were understood; examples include Tokyo, Lima and Los Angeles. Once a city exists, jobs keep people there.', '1 mark site/economic reason; 1 mark example [2]'),
        ('Explain why poor people may have little choice about living in hazardous areas.', 'They cannot afford safer land or housing, depend on local farming or jobs, may lack information about risks and have no money to move.', '1 mark each [2]'),
        ('Explain how living near a volcano can benefit the economy of a country.', 'Tourism (e.g. Iceland’s Blue Lagoon, Etna), geothermal power, mining of sulphur and building materials, and high-yield farming earn income and create jobs.', '1 mark benefit; 1 mark development [2]'),
    ],
    'claims': [
        ('People only live near volcanoes because they do not know the dangers.', False, 'Many know the risks but stay for fertile soil, jobs, tourism, geothermal energy and family ties.'),
        ('Volcanic soils are often very fertile.', True, 'Weathered ash and lava release minerals such as potassium and phosphorus.'),
        ('The risk from a hazard depends only on how powerful the hazard is.', False, 'Risk also depends on how many people are exposed and how vulnerable they are.'),
    ],
    'cases': [
        (['Fig. 2.3 shows information about land use on the slopes of a composite volcano in a lower-income country. Below 600 m: rice terraces and villages, population density 900 people per km². 600-1500 m: coffee, vegetables and dairy cattle, 400 people per km². Above 1500 m: forest and tourist trails to the summit (2900 m). A geothermal power station lies at 1200 m.',
          'Study Fig. 2.3, a description of a volcano and its surroundings. The lower slopes are densely settled with rice terraces (about 900 people per km²); the middle slopes grow coffee and vegetables and have a geothermal power station; the upper slopes are forest used by trekkers visiting the 2900 m crater.'],
         [('Describe how land use changes with height.', 'Below 600 m dense villages and rice terraces; 600-1500 m coffee, vegetables, dairy and geothermal power; above 1500 m forest and tourism.', '1 mark each zone up to [3]'),
          ('Suggest two reasons why the population density is highest below 600 m.', 'Fertile volcanic soils and flatter land for rice; water from rivers; warmer; easier access and roads.', '1 mark each [2]'),
          ('Explain how the volcano provides income for local people.', 'Farming on fertile soils, jobs at the geothermal power station, and tourism (guides, homestays).', '1 mark each up to [3]'),
          ('Suggest why some people may refuse to leave when warnings are issued.', 'Fear of losing livestock, crops and property to looting; previous false alarms; strong attachment to land; lack of transport or a place to go.', '1 mark each [2]')]),
    ],
    'essays': [
        ('the benefits of living in tectonic hazard zones outweigh the risks',
         ['Fertile soils, geothermal energy, tourism and minerals support millions (e.g. Java, Iceland, Etna).', 'Major eruptions and earthquakes are rare in a person’s lifetime and prediction is improving.'],
         ['Catastrophic events kill thousands and destroy livelihoods (Haiti 2010, Merapi 2010).', 'The poorest have little choice and are the most vulnerable.'],
         'For most people, most of the time, benefits outweigh risks – especially where monitoring and preparation reduce vulnerability – but not for the poorest in high-risk areas.',
         ['farming', 'tourism', 'geothermal energy', 'level of development']),
    ],
})


@c2d.add('C3', (1, 2, 3, 4), 'numerical')
def c2d_data(r, D):
    v = r.choice(['Merapi', 'Etna', 'Mount Fuji', 'Popocatépetl', 'Vesuvius', 'Taal'])
    pops = [r.randint(5, 30) * 10 for _ in range(4)]
    rings = ['0-10 km', '10-20 km', '20-30 km', '30-50 km']
    pops.sort()
    tot = sum(pops)
    within20 = pops[0] + pops[1]
    pc = within20 / tot * 100
    stem = f'Table 2.2 shows the number of people living at different distances from {v}: ' + ', '.join(f'{a}: {p} 000' for a, p in zip(rings, pops)) + '.'
    if D == 1:
        opts, a = mcq(r, f'{tot} 000', [f'{pops[-1]} 000', f'{within20} 000', f'{tot + 100} 000', f'{tot // 2} 000'])
        return {'stem': stem + ' How many people live within 50 km?', 'options': opts, 'answer': a, 'key': f'{"+".join(map(str, pops))} = {tot} thousand. [1]'}
    parts = [
        lambda r: ('Calculate the total number of people living within 50 km.', f'{tot} 000', f'{" + ".join(map(str, pops))} = {tot} thousand [1]'),
        lambda r: ('Calculate the percentage of these people who live within 20 km of the volcano.', f'{dp(pc)}%', f'{within20} ÷ {tot} × 100 = {dp(pc)}% [2]'),
        lambda r: ('Describe how the number of people changes with distance from the volcano.', f'Numbers increase with distance, from {pops[0]} 000 within 10 km to {pops[-1]} 000 at 30-50 km, although the outer rings also cover a larger area.', '1 mark trend; 1 mark data [2]'),
        lambda r: ('Suggest why many people still live within 10 km of the summit.', 'Fertile soils, tourism and jobs, family land, and confidence in monitoring and warnings.', '1 mark each up to [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


# --------------------------------------------------------------- 2.5 reducing the impact
c2e = T('Reducing the impact: prediction, preparation, building design and emergency response', 'prediction preparation building design emergency response')
build(c2e, {
    'terms': [
        ('prediction', 'forecasting when and where a hazard will happen, for example from changes in a volcano before an eruption'),
        ('preparation', 'actions taken before a hazard to reduce its impact, such as drills, emergency kits and evacuation plans'),
        ('hazard map', 'a map showing the areas most at risk from a hazard, used to plan land use and evacuation'),
        ('aseismic building', 'a building designed to withstand earthquake shaking, for example with cross-bracing or a rubber base'),
        ('tiltmeter', 'an instrument that detects swelling of a volcano’s slopes as magma rises'),
        ('evacuation', 'moving people away from a dangerous area to a safer place'),
        ('emergency response', 'the immediate actions after a hazard, such as search and rescue, medical care, shelter and water'),
        ('building code', 'a set of laws setting the standards that new buildings must meet, such as earthquake resistance'),
    ],
    'mcq': [
        ('Which of these is used to monitor a volcano for signs of an eruption?', 'Measuring gas emissions such as sulphur dioxide', ['Measuring river discharge', 'Counting tourists', 'Recording wind direction only'], 'Also tiltmeters, seismometers and satellites. [1]'),
        ('Which building feature helps a tall building survive an earthquake?', 'A rubber shock absorber in the foundations (base isolation)', ['Heavy concrete roof', 'Large unreinforced brick walls', 'Glass panels without frames'], '[1]'),
        ('Why can earthquakes not be predicted as accurately as many volcanic eruptions?', 'Earthquakes give few reliable warning signs before they happen', ['Earthquakes always happen at night', 'Seismometers do not work', 'Earthquakes only happen under the sea'], '[1]'),
        ('Which is an example of preparation for an earthquake?', 'Holding earthquake drills in schools every year', ['Search and rescue after the event', 'Rebuilding roads', 'Sending food aid'], '[1]'),
        ('Japan holds national earthquake drills on 1 September each year. This is an example of', 'preparation', ['prediction', 'emergency response', 'long-term recovery'], '[1]'),
    ],
    'explain': [
        ('Explain how scientists can predict volcanic eruptions.', 'Rising magma causes small earthquakes (seismometers), swelling of the ground (tiltmeters, GPS, satellites), increased gas emissions and higher ground temperatures; these signs can give days or weeks of warning.', '1 mark each method linked to sign up to [3]'),
        ('Explain how building design can reduce deaths in an earthquake.', 'Cross-bracing and steel frames let buildings sway without collapsing; base isolators absorb shaking; lightweight roofs reduce weight; automatic shutters stop glass falling.', '1 mark each feature with explanation up to [3]'),
        ('Explain why emergency response is often slower in LICs than in HICs.', 'Roads, ports and airports may be damaged or poor; fewer trained rescue teams and equipment; weaker government organisation; reliance on foreign aid that takes time to arrive.', '1 mark each [3]'),
        ('Explain how hazard mapping helps reduce the impacts of a volcanic eruption.', 'It shows areas at risk from lava, pyroclastic flows and lahars, so building can be restricted there and evacuation routes and shelters can be planned.', '1 mark identifies risk areas; 1 mark land-use planning/evacuation [2]'),
    ],
    'claims': [
        ('Scientists can predict the exact time of an earthquake.', False, 'They can identify high-risk zones and give seconds of warning after shaking starts, but not the exact time in advance.'),
        ('Earthquake early-warning systems can give seconds of warning.', True, 'They detect the fast P-waves and send alerts before the more damaging S-waves arrive, giving time to stop trains and take cover.'),
        ('Building codes are only useful if they are enforced.', True, 'In many LICs codes exist but are ignored, so buildings still collapse.'),
        ('Rebuilding after an earthquake is part of the emergency response.', False, 'Emergency response is the immediate rescue and relief; rebuilding is long-term recovery.'),
    ],
    'cs': [
        ('a country’s response to a tectonic hazard', [
            ('Japan (Tōhoku earthquake and tsunami, 2011)', {'responses': 'Before: strict building codes, base-isolated buildings, sea walls, national drills on 1 September and an earthquake early-warning system. During: the warning stopped bullet trains and sent alerts to phones; tsunami warnings within 3 minutes. After: the Self-Defence Forces led rescue; temporary housing; sea walls raised and homes moved to higher ground.',
                                                             'evaluate': 'Very effective against shaking – few buildings collapsed – but the tsunami overtopped sea walls designed for smaller waves, so about 18 000 died; the nuclear accident showed planning gaps.'}),
            ('Nepal (Gorkha earthquake, 2015)', {'responses': 'Before: a building code existed but was poorly enforced; some schools had drills. After: international rescue teams, Indian and Chinese army helicopters, tents and water from NGOs; reconstruction grants to rebuild houses with earthquake-resistant designs.',
                                                 'evaluate': 'Limited: poor roads and landslides delayed help to remote villages; reconstruction was slow, with many families in temporary shelters for over a year; some reinforced schools survived, showing the value of preparation.'}),
            ('Indonesia (Merapi eruption, 2010)', {'responses': 'Before: monitoring of seismic activity, deformation and gas; hazard maps and alert levels. During: the exclusion zone was extended to 20 km and about 350 000 people were evacuated. After: evacuation centres, compensation, relocation of villages from the most dangerous slopes.',
                                                   'evaluate': 'Monitoring and evacuation saved thousands of lives, but about 350 people died, some refusing to leave their farms and livestock.'}),
        ], [
            ('describe the strategies used to reduce the impacts of the hazard', 'responses', 'Prediction/monitoring, preparation (codes, drills, warnings), emergency response and recovery, with named detail.'),
            ('evaluate how successful the strategies were in reducing the impacts of the hazard', 'evaluate', 'What worked and what did not, with evidence (deaths, damage, speed of response) and a judgement.'),
        ]),
    ],
    'essays': [
        ('the level of development of a country is the most important factor in reducing the impact of tectonic hazards',
         ['HICs such as Japan can afford building codes, warning systems and fast rescue; deaths in Christchurch (2011) were 185 compared with over 100 000 in Haiti (2010).'],
         ['The size and type of hazard matter: Tōhoku’s tsunami killed about 18 000 people even in a well-prepared HIC.', 'Community preparation, education and good governance can be cheap and effective in LICs (e.g. Merapi evacuation).'],
         'Development is very important because it pays for preparation and response, but hazard magnitude, location and governance also matter.',
         ['building codes', 'warning systems', 'Haiti and Japan', 'governance']),
    ],
})


@c2e.add('C3', (2, 3, 4, 5), 'numerical')
def c2e_compare(r, D):
    a, b = r.sample(list(QUAKES), 2)
    qa, qb = QUAKES[a], QUAKES[b]
    popa, popb = r.choice([3, 5, 8, 10, 12]), r.choice([2, 4, 6, 9, 15])
    pma, pmb = qa['deaths'] / popa, qb['deaths'] / popb
    stem = (f'Table 2.3 compares two earthquakes. {cap(a)}: magnitude {qa["mag"]}, {qa["income"]}, about {nf(qa["deaths"])} deaths, about {popa} million people in the affected region. '
            f'{cap(b)}: magnitude {qb["mag"]}, {qb["income"]}, about {nf(qb["deaths"])} deaths, about {popb} million people in the affected region.')
    parts = [
        lambda r: ('Calculate the number of deaths per million people in the affected region for each earthquake.', f'{cap(a)}: {fmt(round(pma), 0)}; {cap(b)}: {fmt(round(pmb), 0)} per million',
                   f'{qa["deaths"]} ÷ {popa} = {fmt(round(pma), 0)}; {qb["deaths"]} ÷ {popb} = {fmt(round(pmb), 0)} [2]'),
        lambda r: ('Suggest why deaths per million people is a fairer comparison than total deaths.', 'It allows for the different number of people exposed to the hazard.', '[1]'),
        lambda r: ('Suggest reasons, other than magnitude, for the difference in impact.', 'Level of development (building codes, enforcement), focus depth and distance from cities, preparation and warning systems, speed of rescue, time of day, secondary hazards such as tsunami.', '1 mark each reason up to [3]'),
        lambda r: ('Describe two ways in which the impacts of future earthquakes could be reduced in the poorer of these areas.', 'Retrofitting schools and hospitals with cross-bracing; enforcing building codes; community drills and education; emergency supplies stored locally; hazard maps limiting building on unstable slopes.', '1 mark each developed method [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c2e.add('C2', (2, 3, 4), 'explain')
def c2e_sort(r, D):
    acts = [('installing seismometers and tiltmeters on a volcano', 'prediction'), ('mapping areas likely to be hit by lahars', 'preparation'),
            ('holding school earthquake drills', 'preparation'), ('fitting rubber base isolators to new office blocks', 'preparation'),
            ('sending search-and-rescue teams with sniffer dogs', 'emergency response'), ('measuring sulphur dioxide emissions from the crater', 'prediction'),
            ('setting up field hospitals and distributing clean water', 'emergency response'), ('storing emergency kits with food, water and a torch at home', 'preparation'),
            ('using satellites to detect swelling of a volcano', 'prediction'), ('providing tents and blankets to homeless families', 'emergency response')]
    k = 4 if D <= 3 else 5
    pick = r.sample(acts, k)
    if len({p[1] for p in pick}) < 2:
        return None
    lab = 'ABCDE'
    stem = 'Classify each action as prediction, preparation or emergency response, and explain one of your choices. ' + ' '.join(f'{lab[i]}: {cap(a)}.' for i, (a, _) in enumerate(pick))
    return {'stem': stem, 'answer': '; '.join(f'{lab[i]} {c}' for i, (_, c) in enumerate(pick)) + '. E.g. prediction gives warning that an event is coming; preparation reduces its impact in advance; response happens after it.',
            'key': f'1 mark for every two correct classifications; 1 mark explanation [{k // 2 + 1}]', 'marks': k // 2 + 1, 'type': 'explain'}


CHAPTERS[2] = [c2a, c2b, c2c, c2d, c2e]


# ============================================================== CHAPTER 3: Rivers
RIVERS = ['River Severn', 'River Tees', 'Rhine', 'Mekong', 'Ganges', 'Nile', 'Amazon', 'Zambezi', 'Indus', 'Mississippi', 'Yangtze', 'Danube']

c3a = T('The drainage basin and the hydrological cycle', 'drainage basin hydrological cycle')
build(c3a, {
    'terms': [
        ('drainage basin', 'the area of land drained by a river and its tributaries'),
        ('watershed', 'the boundary of a drainage basin, usually a ridge of high land'),
        ('tributary', 'a smaller river or stream that joins a larger river'),
        ('confluence', 'the point where two rivers meet'),
        ('source', 'the starting point of a river, often in an upland area'),
        ('mouth', 'the point where a river flows into the sea, a lake or another river'),
        ('infiltration', 'the downward movement of water from the surface into the soil'),
        ('percolation', 'the slow downward movement of water from the soil into the rock below'),
        ('surface run-off', 'water flowing over the surface of the ground (overland flow) towards a river'),
        ('throughflow', 'the movement of water sideways through the soil towards a river'),
        ('evapotranspiration', 'the combined loss of water to the air by evaporation and by transpiration from plants'),
        ('interception', 'precipitation caught and held by vegetation before it reaches the ground'),
        ('lag time', 'the time between peak rainfall and peak discharge on a storm hydrograph'),
        ('discharge', 'the volume of water passing a point in a river per second, measured in cumecs (m³/s)'),
    ],
    'mcq': [
        ('Which of these is a store in the drainage basin system?', 'Groundwater', ['Infiltration', 'Throughflow', 'Evaporation'], 'Stores hold water; flows/transfers move it. [1]'),
        ('Which of these is an output from the drainage basin?', 'Evapotranspiration', ['Precipitation', 'Interception', 'Infiltration'], '[1]'),
        ('What does a short lag time on a storm hydrograph show?', 'Water reaches the river quickly, so flood risk is higher', ['Water reaches the river slowly', 'There was no rainfall', 'The river is very long'], '[1]'),
        ('Which surface would cause the most surface run-off?', 'Tarmac roads and concrete', ['Deciduous woodland', 'Grassland on sandy soil', 'Ploughed field with deep soil'], 'Impermeable surfaces prevent infiltration. [1]'),
        ('Discharge is measured in', 'cumecs (m³/s)', ['metres per second', 'millimetres', 'square metres'], '[1]'),
        ('The ridge of high land that separates two drainage basins is the', 'watershed', ['confluence', 'flood plain', 'source'], '[1]'),
    ],
    'explain': [
        ('Explain how vegetation affects the amount of water reaching a river.', 'Vegetation intercepts rain and slows it; roots help infiltration and plants take up water and transpire it, so less water reaches the river and more slowly.', '1 mark interception; 1 mark infiltration/transpiration [2]'),
        ('Explain why the lag time is shorter in an urban drainage basin than in a forested one.', 'Impermeable surfaces and drains carry water quickly to the river with little infiltration; in forest, interception and infiltration slow the water down.', '1 mark impermeable/drains; 1 mark contrast with forest [2]'),
        ('Explain how steep slopes and impermeable rock affect a storm hydrograph.', 'Water cannot soak into impermeable rock and flows quickly down steep slopes as surface run-off, so the peak discharge is higher and the lag time shorter.', '1 mark faster run-off; 1 mark higher peak/shorter lag [2]'),
        ('Describe the shape of a storm hydrograph and explain the rising limb.', 'Base flow, then a steep rising limb to peak discharge, then a gentler falling limb; the rising limb shows run-off and throughflow reaching the river after rain.', '1 mark shape; 1 mark rising limb explanation [2]'),
        ('Explain the difference between a store and a flow in the hydrological cycle, with an example of each.', 'A store holds water for a time (e.g. lakes, groundwater, soil moisture); a flow moves water between stores (e.g. infiltration, throughflow, run-off).', '1 mark each with example [2]'),
    ],
    'claims': [
        ('When soil is already saturated, more rain will soak into it.', False, 'Saturated soil cannot absorb more water, so rain becomes surface run-off and flood risk rises.'),
        ('Deforestation in a drainage basin can increase flood risk downstream.', True, 'Less interception and transpiration means more water reaches the river, more quickly.'),
        ('Throughflow is the movement of water through rock.', False, 'Throughflow is sideways movement through soil; movement through rock is groundwater flow.'),
        ('Peak discharge always occurs at the same time as peak rainfall.', False, 'There is a lag time while water travels over and through the ground to the river.'),
    ],
    'essays': [
        ('human activity has a greater effect than physical factors on the shape of a storm hydrograph',
         ['Urbanisation adds impermeable surfaces and drains, shortening lag time and raising peak discharge.', 'Deforestation removes interception; farming practices compact soil.'],
         ['Rock type, slope, basin shape, soil saturation and rainfall intensity control run-off speed in all basins.', 'In remote upland basins physical factors dominate.'],
         'In urban basins human factors often dominate; elsewhere physical factors such as rainfall intensity and geology are usually more important.',
         ['urbanisation', 'deforestation', 'rock type', 'rainfall intensity']),
    ],
})


@c3a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c3a_hydro(r, D):
    rain_t = r.choice([6, 8, 9, 10, 12, 14])  # hour of peak rainfall on day 1
    lag = r.choice([4, 6, 8, 10, 12, 16, 18, 20])
    base = r.choice([5, 8, 10, 12, 15, 20])
    peak = base + r.choice([15, 20, 25, 30, 40, 55, 70])
    rain = r.choice([12, 18, 25, 30, 35, 45])
    river = r.choice(RIVERS[:4] + ['Afon Llwyd', 'River Ock', 'Rio Piracicaba', 'Pasig River'])
    pt = rain_t + lag
    day = 'day 1' if pt < 24 else 'day 2'
    ptime = pt if pt < 24 else pt - 24
    stem = (f'Fig. 3.1 is a storm hydrograph for the {river}. Rainfall peaked at {rain} mm per hour at {rain_t:02d}:00 on day 1. '
            f'Discharge rose from a base flow of {base} cumecs to a peak of {peak} cumecs at {ptime:02d}:00 on {day}.')
    if D == 1:
        opts, a = mcq(r, f'{lag} hours', [f'{pt} hours', f'{lag + 2} hours', f'{max(1, lag - 2)} hours', f'{rain_t} hours'])
        return {'stem': stem + ' What is the lag time?', 'options': opts, 'answer': a, 'key': f'Time of peak discharge − time of peak rainfall = {lag} hours. [1]'}
    parts = [
        lambda r: ('Calculate the lag time.', f'{lag} hours', f'{ptime:02d}:00 on {day} − {rain_t:02d}:00 day 1 = {lag} h [1]'),
        lambda r: ('Calculate the increase in discharge from base flow to peak.', f'{peak - base} cumecs', f'{peak} − {base} = {peak - base} cumecs [1]'),
        lambda r: ('Suggest two reasons why the lag time may be ' + ('short' if lag <= 8 else 'long') + '.',
                   ('Steep slopes; impermeable rock or saturated soil; urban surfaces and drains; small, circular basin; little vegetation.' if lag <= 8 else
                    'Gentle slopes; permeable rock and soil allowing infiltration; dense forest intercepting rain; large or elongated basin; dry soil before the storm.'),
                   '1 mark each reason [2]'),
        lambda r: ('Explain why the falling limb is less steep than the rising limb.', 'After rainfall stops, water continues to reach the river slowly by throughflow and groundwater flow, so discharge falls gradually.', '1 mark slower flows; 1 mark gradual fall [2]'),
        lambda r: ('Describe how the hydrograph would change if the basin were urbanised.', 'Shorter lag time, higher and steeper peak, because impermeable surfaces and drains speed up run-off.', '1 mark change; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c3a.add('C3', (2, 3, 4), 'numerical')
def c3a_budget(r, D):
    p = r.choice([800, 1000, 1200, 1500, 1800, 2400])
    e = int(p * r.choice([0.3, 0.4, 0.5, 0.6]) / 10) * 10
    ro = int((p - e) * r.choice([0.4, 0.5, 0.6]) / 10) * 10
    g = p - e - ro
    stem = f'In one year a drainage basin receives {p} mm of precipitation. Evapotranspiration is {e} mm and river run-off is {ro} mm. The rest is added to storage (soil water and groundwater).'
    parts = [
        lambda r: ('Calculate the amount of water added to storage.', f'{g} mm', f'{p} − {e} − {ro} = {g} mm [1]'),
        lambda r: ('Calculate evapotranspiration as a percentage of precipitation.', f'{dp(e / p * 100)}%', f'{e} ÷ {p} × 100 = {dp(e / p * 100)}% [1]'),
        lambda r: ('Name two other stores in a drainage basin.', 'Any two: interception store on vegetation, surface stores (lakes, puddles), soil moisture, groundwater, river channel.', '1 mark each [2]'),
        lambda r: ('Suggest how the figures would differ in a hot, forested basin.', 'Evapotranspiration would be a larger share because of high temperatures and transpiration by trees; less run-off.', '1 mark more evapotranspiration; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


# --------------------------------------------------------------- 3.2 processes
c3b = T('River processes: erosion, transportation and deposition', 'erosion transportation deposition')
build(c3b, {
    'terms': [
        ('hydraulic action', 'erosion caused by the force of water hitting the bed and banks and forcing air into cracks'),
        ('abrasion', 'erosion when rocks carried by the river scrape and wear away the bed and banks'),
        ('attrition', 'erosion when rocks carried by the river knock into each other, becoming smaller and rounder'),
        ('solution', 'the chemical dissolving of rocks such as limestone by river water'),
        ('traction', 'the rolling of large boulders along the river bed'),
        ('saltation', 'the bouncing of pebbles and sand along the river bed'),
        ('suspension', 'the transport of fine particles of silt and clay held up within the water'),
        ('deposition', 'the dropping of load when the river loses energy and velocity'),
        ('vertical erosion', 'downward erosion of the river bed, which deepens the channel, mainly in the upper course'),
        ('lateral erosion', 'sideways erosion of the river banks, which widens the channel and valley, mainly in the middle and lower course'),
        ('load', 'the material, such as sand, pebbles and silt, carried by a river'),
    ],
    'mcq': [
        ('Which process makes river stones smaller and more rounded downstream?', 'Attrition', ['Hydraulic action', 'Solution', 'Traction'], '[1]'),
        ('How is fine clay and silt usually transported?', 'In suspension', ['By traction', 'By saltation', 'By solution only'], '[1]'),
        ('When does a river deposit its load?', 'When its velocity and energy fall', ['When discharge increases', 'During a flood peak', 'When the gradient increases'], '[1]'),
        ('Which process involves rocks carried by the river wearing away the bed and banks?', 'Abrasion', ['Attrition', 'Solution', 'Saltation'], '[1]'),
        ('In the upper course of a river, the dominant type of erosion is', 'vertical erosion', ['lateral erosion', 'deposition', 'longshore drift'], '[1]'),
    ],
    'explain': [
        ('Explain why rivers erode most during floods.', 'Velocity and discharge are higher, so the river has more energy; it carries more and larger load, increasing abrasion and hydraulic action.', '1 mark more energy/velocity; 1 mark more load and erosion [2]'),
        ('Explain why the load of a river becomes smaller and more rounded downstream.', 'Attrition knocks stones together and abrasion wears them, breaking off edges over a long distance.', '1 mark attrition; 1 mark over distance/time [2]'),
        ('Explain why a river deposits its load on the inside of a meander bend.', 'Water is shallower and slower on the inside bend, so it loses energy and drops sand and gravel, forming a slip-off slope.', '1 mark slower velocity; 1 mark deposition/slip-off slope [2]'),
        ('Compare traction and saltation.', 'Both move load along the bed; traction rolls the largest boulders, saltation bounces smaller pebbles and sand.', '1 mark each [2]'),
        ('Explain how velocity and discharge usually change downstream.', 'Discharge increases as tributaries join; velocity often increases slightly because the channel is wider, deeper and smoother, so less energy is lost to friction.', '1 mark discharge + reason; 1 mark velocity + reason [2]'),
    ],
    'claims': [
        ('Rivers flow fastest in their upper course because the gradient is steepest.', False, 'Upper channels are shallow and rough with boulders, so friction slows water; mean velocity often increases downstream.'),
        ('Solution is most important on limestone or chalk.', True, 'These rocks contain calcium carbonate, which dissolves in slightly acidic water.'),
        ('Deposition happens when a river gains energy.', False, 'Deposition happens when it loses energy, e.g. when velocity falls on inside bends or at the mouth.'),
    ],
    'essays': [
        ('erosion is the most important river process in shaping river landscapes',
         ['Vertical erosion forms V-shaped valleys, waterfalls and gorges; lateral erosion forms meanders and wide valleys.'],
         ['Deposition builds flood plains, levees, deltas and slip-off slopes in the lower course.', 'Transportation links them: load carried from upstream drives abrasion.'],
         'Erosion dominates in the upper course and deposition in the lower course; the landscape is the result of all three processes working together.',
         ['upper course', 'lower course', 'floods', 'landforms']),
    ],
})


@c3b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c3b_dis(r, D):
    w = r.choice([1.2, 1.8, 2.4, 3.0, 4.5, 6.0, 8.0, 12.0])
    d = r.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8])
    dist = r.choice([5, 10])
    t = r.choice([8, 10, 12.5, 16, 20, 25])
    v = dist / t
    area = w * d
    Q = area * v
    site = r.choice(['Site 1, near the source', 'Site 3, in the middle course', 'Site 5, near the confluence'])
    stem = f'Students measured the {r.choice(RIVERS[:3] + ["stream"])} at {site}. Width = {fmt(w, 2)} m, mean depth = {fmt(d, 2)} m. A float took {fmt(t, 1)} s to travel {dist} m.'
    if D == 1:
        opts, a = mcq(r, f'{fmt(round(area, 3), 3)} m²', [f'{fmt(w + d, 2)} m²', f'{fmt(round(area * 2, 3), 3)} m²', f'{fmt(round(w / d, 2), 2)} m²', f'{fmt(round(area / 2, 3), 3)} m²'])
        return {'stem': stem + ' What is the cross-sectional area of the channel?', 'options': opts, 'answer': a, 'key': f'width × mean depth = {fmt(w, 2)} × {fmt(d, 2)} = {fmt(round(area, 3), 3)} m². [1]'}
    parts = [
        lambda r: ('Calculate the velocity in m/s.', f'{fmt(round(v, 2), 2)} m/s', f'{dist} ÷ {fmt(t, 1)} = {fmt(round(v, 2), 2)} m/s [1]'),
        lambda r: ('Calculate the cross-sectional area.', f'{fmt(round(area, 3), 3)} m²', f'{fmt(w, 2)} × {fmt(d, 2)} = {fmt(round(area, 3), 3)} m² [1]'),
        lambda r: ('Calculate the discharge. Show your working and give units.', f'{fmt(round(Q, 3), 3)} m³/s (cumecs)', f'discharge = area × velocity = {fmt(round(area, 3), 3)} × {fmt(round(v, 2), 2)} = {fmt(round(Q, 3), 3)} cumecs [2]'),
        lambda r: ('Suggest why surface float velocity may be higher than the mean velocity.', 'Friction with the bed and banks slows water near them, so surface water in mid-channel flows fastest.', '1 mark friction; 1 mark surface fastest [2]'),
        lambda r: ('Suggest one way of making the velocity measurement more reliable.', 'Repeat the float timing three times and take the mean; use a flow meter; avoid windy conditions.', '[1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c3b.add('C3', (2, 3, 4, 5), 'numerical')
def c3b_bradshaw(r, D):
    n = 5
    dist = [0, 4, 9, 15, 22]
    w = sorted(round(r.uniform(0.8, 9), 1) for _ in range(n))
    sz = sorted((r.randint(15, 220) for _ in range(n)), reverse=True)
    if len(set(w)) < n or len(set(sz)) < n:
        return None
    swap = r.random() < 0.5
    if swap:
        i = r.randrange(1, n - 1)
        sz[i], sz[i + 1] = sz[i + 1], sz[i]
    stem = ('Table 3.1 shows measurements at five sites downstream along a river. ' + ' '.join(
        f'Site {k + 1} ({dist[k]} km from source): width {fmt(w[k], 1)} m, mean pebble size {sz[k]} mm.' for k in range(n)))
    anom = [k for k in range(1, n) if sz[k] > sz[k - 1]]
    parts = [
        lambda r: ('Describe how channel width changes downstream. Use data.', f'Width increases from {fmt(w[0], 1)} m at Site 1 to {fmt(w[-1], 1)} m at Site 5.', '1 mark trend; 1 mark data [2]'),
        lambda r: ('Describe how pebble size changes downstream.', f'Pebble size generally decreases from {sz[0]} mm to {sz[-1]} mm' + (f', except at Site {anom[0] + 1} where it is larger than upstream.' if anom else '.'), '1 mark trend; 1 mark data/anomaly [2]'),
        lambda r: ('Explain why pebble size changes downstream.', 'Attrition and abrasion break pebbles into smaller, rounder pieces as they are transported further.', '1 mark process; 1 mark distance/time [2]'),
        lambda r: ('Calculate the mean pebble size for the five sites.', f'{dp(mean(sz))} mm', f'{"+".join(map(str, sz))} = {sum(sz)}; ÷ 5 = {dp(mean(sz))} mm [1]'),
        lambda r: ('Suggest a reason for the anomaly in pebble size.' if anom else 'Explain why the width increases downstream.',
                   ('A tributary or eroding bank may have added fresh, larger material at that site; or the sample was too small.' if anom else 'Tributaries add water, so discharge increases and lateral erosion widens the channel.'),
                   '1 mark reason; 1 mark development [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 3.3 landforms
c3c = T('River landforms from source to mouth: waterfalls, meanders, ox-bow lakes, levees and deltas', 'waterfalls meanders ox-bow lakes levees deltas')
build(c3c, {
    'terms': [
        ('waterfall', 'a steep drop in a river’s course where water falls over a band of hard rock lying on top of softer rock'),
        ('plunge pool', 'a deep pool at the foot of a waterfall eroded by hydraulic action and abrasion'),
        ('gorge', 'a narrow, steep-sided valley formed as a waterfall retreats upstream'),
        ('interlocking spurs', 'ridges of higher land that the river winds around in the upper course'),
        ('meander', 'a bend in a river formed by lateral erosion on the outside and deposition on the inside'),
        ('river cliff', 'a steep bank on the outside of a meander bend formed by erosion'),
        ('slip-off slope', 'a gentle slope of deposited material on the inside of a meander bend'),
        ('ox-bow lake', 'a horseshoe-shaped lake left when a meander is cut off from the main channel'),
        ('levee', 'a raised bank of sediment along the side of a river built up by repeated flooding'),
        ('flood plain', 'the wide, flat area of land on either side of a river in its lower course that floods'),
        ('delta', 'an area of sediment deposited at a river mouth where the river enters a sea or lake faster than it can be removed'),
    ],
    'mcq': [
        ('Where is a waterfall most likely to form?', 'Where a band of hard rock overlies softer rock', ['Where the river enters the sea', 'On the inside of a meander bend', 'On a wide flood plain'], '[1]'),
        ('On which side of a meander is a river cliff found?', 'The outside of the bend', ['The inside of the bend', 'In the middle of the channel', 'At the river mouth'], '[1]'),
        ('Which landform is formed when a meander neck is cut through during a flood?', 'Ox-bow lake', ['Delta', 'Gorge', 'Levee'], '[1]'),
        ('Why are levees made of coarser material near the river?', 'When the river floods, velocity drops sharply at the banks and the heaviest material is deposited first', ['Coarse material floats', 'Fine material is too heavy to move', 'Levees are made by people'], '[1]'),
        ('The Nile delta is an example of which type of delta?', 'Arcuate (fan-shaped)', ['Bird’s foot', 'Cuspate', 'Estuarine'], 'The Mississippi is a bird’s foot delta. [1]'),
        ('Victoria Falls on the Zambezi forms where the river flows over', 'basalt with joints eroded into a series of gorges', ['soft clay on a flood plain', 'a delta', 'a sand bar'], '[1]'),
    ],
    'explain': [
        ('Explain how a waterfall and gorge form.', 'Hard rock lies over soft rock; the soft rock is eroded faster by hydraulic action and abrasion, undercutting the hard rock to leave an overhang; the overhang collapses into the plunge pool; repeated collapse makes the waterfall retreat upstream, leaving a gorge.', '1 mark rock bands; 1 mark undercut/overhang; 1 mark collapse; 1 mark retreat/gorge [4]'),
        ('Explain how an ox-bow lake forms.', 'Erosion on the outside of meander bends narrows the meander neck; during a flood the river cuts through the neck and takes the shorter, straighter course; deposition seals off the old bend, leaving an ox-bow lake.', '1 mark erosion of outer bends; 1 mark neck cut in flood; 1 mark deposition seals [3]'),
        ('Explain how levees are formed.', 'When the river floods it loses velocity as it spreads over the flood plain; the largest, heaviest sediment is deposited first next to the channel; repeated floods build up raised banks.', '1 mark loss of velocity; 1 mark coarse material first; 1 mark repeated floods [3]'),
        ('Explain why deltas form at some river mouths but not at others.', 'Deltas form where a river carries a large load and enters calm, shallow water with little tide or current; where strong tides or currents remove sediment, an estuary forms instead.', '1 mark large load/calm sea; 1 mark strong tides prevent [2]'),
        ('Describe the cross-section of a meander.', 'Asymmetrical: deep water and a steep river cliff on the outside bend; shallow water and a gently sloping slip-off slope of sand and gravel on the inside.', '1 mark outside; 1 mark inside [2]'),
    ],
    'claims': [
        ('Meanders stay in the same place for hundreds of years.', False, 'Erosion on the outside and deposition on the inside make meanders migrate across and down the flood plain.'),
        ('Waterfalls slowly retreat upstream.', True, 'Undercutting and collapse of the overhang move the waterfall back, leaving a gorge.'),
        ('Flood plains are formed mainly by vertical erosion.', False, 'They are formed by lateral erosion and the deposition of alluvium during floods.'),
        ('Ox-bow lakes are found in the upper course of a river.', False, 'They form from meanders, which are found in the middle and lower course on flatter land.'),
    ],
    'cases': [
        (['Fig. 3.2 is a sketch of a river in its middle course. The river forms a large bend. On the outside of the bend is a steep bank 3 m high with exposed tree roots; on the inside is a gently sloping bank of sand and gravel. Further downstream, a narrow neck of land separates two bends that are only 40 m apart.',
          'Study Fig. 3.2, a sketch map of a meandering river. A steep, eroding bank lies on the outside of one bend and a gently sloping beach of sand and gravel on the inside. Downstream, two meander loops almost meet across a narrow neck of land.'],
         [('Name the landforms on the outside and inside of the bend.', 'Outside: river cliff. Inside: slip-off slope.', '1 mark each [2]'),
          ('Explain the difference between the two banks.', 'Water is deeper and faster on the outside, so lateral erosion (hydraulic action, abrasion) undercuts the bank; on the inside water is slow and shallow, so sediment is deposited.', '1 mark outside; 1 mark inside [2]'),
          ('Explain what is likely to happen to the narrow neck of land in the future.', 'Erosion on the outside bends will narrow the neck further; in a flood the river will cut through, forming a straight channel and later an ox-bow lake.', '1 mark erosion narrows; 1 mark cut-off in flood; 1 mark ox-bow [3]'),
          ('Draw and describe a cross-section from the river cliff to the slip-off slope.', 'Steep cliff on one side, deepest water close to it, channel becoming shallow towards the gently sloping deposits on the other side (asymmetrical).', '1 mark asymmetry; 1 mark labels [2]')]),
        (['Fig. 3.3 shows a waterfall in the upper course of a river. The river flows over a band of hard sandstone 8 m thick lying on top of soft shale. There is an overhang of sandstone above a deep plunge pool. Downstream is a narrow steep-sided gorge 250 m long.',
          'Study Fig. 3.3, a diagram of a waterfall. A layer of resistant rock caps a softer rock below. The water falls 20 m into a plunge pool; an overhang has formed at the lip. Below the falls the river flows through a gorge.'],
         [('Explain how the overhang has formed.', 'Soft rock beneath is eroded faster by hydraulic action and abrasion (splashback), undercutting the hard rock.', '1 mark differential erosion; 1 mark undercutting [2]'),
          ('Describe how the plunge pool forms.', 'Falling water and swirling boulders erode the bed by hydraulic action and abrasion, deepening a pool.', '[2]'),
          ('Explain how the gorge has formed.', 'The overhang collapses repeatedly and the waterfall retreats upstream, leaving a steep-sided gorge.', '1 mark collapse; 1 mark retreat [2]'),
          ('Suggest why this landform is found in the upper course rather than the lower course.', 'Steep gradient, vertical erosion and outcrops of hard and soft rock are typical of upland areas.', '1 mark each [2]')]),
    ],
    'essays': [
        ('deposition is more important than erosion in forming the landforms of the lower course of a river',
         ['Levees, flood plains, deltas and slip-off slopes are all depositional.'],
         ['Meanders and ox-bow lakes need lateral erosion on outer bends.', 'River cliffs are erosional.'],
         'Deposition is dominant in the lower course, but many lower-course landforms result from erosion and deposition acting together.',
         ['flood plains', 'meanders', 'deltas', 'levees']),
    ],
})


@c3c.add('C2', (1, 2, 3), 'short')
def c3c_seq(r, D):
    seqs = {
        'a waterfall and gorge': ['A band of hard rock lies over softer rock.', 'The softer rock is eroded faster, undercutting the hard rock.', 'An overhang forms above a plunge pool.', 'The overhang collapses into the plunge pool.', 'The waterfall retreats upstream, forming a gorge.'],
        'an ox-bow lake': ['Erosion is greatest on the outside of two meander bends.', 'The meander neck becomes narrower.', 'During a flood the river cuts through the neck.', 'The river flows along the new, straighter channel.', 'Deposition seals off the old bend to leave a lake.'],
        'a levee': ['The river floods and spreads over the flood plain.', 'Velocity falls suddenly at the edge of the channel.', 'The coarsest sediment is deposited closest to the river.', 'Finer silt is carried further and deposited on the flood plain.', 'Repeated floods build up raised banks.'],
    }
    land = r.choice(list(seqs))
    st = seqs[land]
    k = 4 if D <= 2 else 5
    steps = st[:k] if k == 4 and r.random() < 0.5 else (st[1:] if k == 4 else st)
    lab = 'PQRST'[:len(steps)]
    order = list(range(len(steps)))
    r.shuffle(order)
    if order == sorted(order):
        order = order[::-1]
    shown = [steps[i] for i in order]
    ans = ', '.join(lab[order.index(i)] for i in range(len(steps)))
    return {'stem': f'Put these statements about the formation of {land} into the correct order. ' + ' '.join(f'{lab[j]}: {s}' for j, s in enumerate(shown)),
            'answer': ans, 'key': f'Correct order {ans}. 2 marks all correct; 1 mark if one pair reversed. [2]', 'marks': 2, 'type': 'short'}


# --------------------------------------------------------------- 3.4 flooding and opportunities
c3d = T('Causes and hazards of river flooding and the opportunities rivers offer', 'river flooding opportunities rivers')
build(c3d, {
    'terms': [
        ('flood', 'when a river overflows its banks and covers land that is normally dry'),
        ('bankfull discharge', 'the maximum discharge a river channel can hold before it overflows'),
        ('flash flood', 'a sudden flood after very intense rainfall, with little warning'),
        ('monsoon', 'a seasonal reversal of winds bringing a very wet season, as in South Asia from June to September'),
        ('alluvium', 'fine, fertile silt deposited by a river when it floods'),
        ('saturated soil', 'soil whose pore spaces are completely full of water so that no more can infiltrate'),
        ('impermeable surface', 'a surface such as concrete or clay that does not let water pass through'),
    ],
    'mcq': [
        ('Which is a physical cause of river flooding?', 'Prolonged heavy rainfall on saturated ground', ['Building houses on the flood plain', 'Deforestation for farming', 'Building drains in towns'], 'The others are human causes. [1]'),
        ('Why do people farm on flood plains?', 'Flooding deposits fertile alluvium and the land is flat', ['Flood plains never flood', 'The soil is very stony', 'Flood plains are always high above the river'], '[1]'),
        ('Which of these is a human cause of flooding?', 'Urbanisation increasing impermeable surfaces', ['Snowmelt in spring', 'A tropical storm', 'Steep slopes in the basin'], '[1]'),
        ('Which country has about 80% of its land on the flood plains and delta of the Ganges, Brahmaputra and Meghna rivers?', 'Bangladesh', ['Egypt', 'Iceland', 'Chile'], '[1]'),
        ('Which is an opportunity offered by rivers?', 'Water for irrigation and hydro-electric power', ['Increased flood risk', 'Waterborne disease', 'Bank erosion'], '[1]'),
    ],
    'explain': [
        ('Explain how deforestation upstream can increase flooding downstream.', 'With fewer trees, less rain is intercepted and transpired, and soil is eroded into the river, reducing channel capacity; more water reaches the river faster.', '1 mark less interception; 1 mark faster run-off; 1 mark sediment reduces capacity [3]'),
        ('Explain why river flooding is both a hazard and a benefit to people living on flood plains.', 'Hazard: destroys homes, crops and roads, causes deaths and disease. Benefit: deposits fertile alluvium, provides water for crops and fish.', '1 mark hazard; 1 mark benefit [2]'),
        ('Explain why the impacts of floods are often greater in LICs than HICs.', 'Dense populations on flood plains, poorly built homes, few defences, weak warning systems and less money for rescue and insurance.', '1 mark each [3]'),
        ('Describe three opportunities rivers offer to people.', 'Water supply for homes, industry and irrigation; fertile flood plains for farming; transport routes and trade; hydro-electric power; fishing; tourism and recreation.', '1 mark each [3]'),
    ],
    'claims': [
        ('Floods are always caused by heavy rainfall alone.', False, 'Snowmelt, saturated ground, impermeable rock, deforestation, urbanisation and storm surges can all contribute.'),
        ('Floods can bring benefits as well as problems.', True, 'They deposit fertile silt and recharge groundwater; Egyptian farming depended on Nile floods for thousands of years.'),
        ('Building on a flood plain reduces flood risk.', False, 'It adds impermeable surfaces and drains that speed up run-off, and puts more people and property at risk.'),
    ],
    'cs': [
        ('a river flood', [
            ('the Pakistan floods, 2022', {'causes': 'Exceptionally heavy monsoon rains from June to August (about three times the 30-year average in August), on top of a heatwave that increased glacial melt in the Himalayas and Karakoram; the Indus and its tributaries overflowed; poor drainage and deforestation added to the problem.',
                                          'impacts': 'About one-third of the country under water; about 1700 deaths; 33 million people affected; over 2 million homes damaged; crops and livestock lost in Sindh and Balochistan; damage estimated at about US$30 billion; outbreaks of malaria and waterborne disease.',
                                          'responses': 'Government and army rescue; UN appeal; international aid for food, tents and medical care; rebuilding of homes and embankments; debate about climate finance for vulnerable countries.'}),
            ('flooding in Bangladesh, 1998', {'causes': 'Heavy monsoon rainfall, Himalayan snowmelt and the meeting of the Ganges, Brahmaputra and Meghna rivers on a low-lying delta; deforestation in Nepal increased run-off and silt; high tides blocked water from draining.',
                                             'impacts': 'About two-thirds of the country flooded for over two months; over 1000 deaths; 30 million people homeless; rice crops destroyed and food shortages; waterborne diseases spread; roads and bridges damaged.',
                                             'responses': 'Emergency food aid and boats; later the Flood Action Plan: embankments, cyclone and flood shelters on raised platforms, improved warnings and raised houses.'}),
            ('the Boscastle flash flood, UK, 2004', {'causes': 'About 75 mm of rain fell in two hours on 16 August 2004 on already saturated ground; the small, steep, impermeable drainage basin funnelled water to the village where two rivers meet.',
                                                    'impacts': 'No deaths, but about 100 people rescued by helicopter; 58 properties flooded and cars swept into the sea; bridges destroyed; local tourism businesses lost income.',
                                                    'responses': 'Large helicopter rescue; later a flood defence scheme widened and deepened the river channel and replaced the bridge with a higher one.'}),
        ], [
            ('explain the causes of the flood', 'causes', 'Physical causes (rainfall intensity/duration, snowmelt, saturated soil, relief) and human causes (deforestation, urbanisation), linked to the named river.'),
            ('describe the impacts of the flood on people and the environment', 'impacts', 'Deaths, homelessness, damage to farmland/infrastructure, disease, economic cost, environmental effects – with figures.'),
            ('describe the responses to the flood', 'responses', 'Short-term rescue and aid; long-term management and planning.'),
        ]),
    ],
    'essays': [
        ('human activity is now the main cause of river flooding',
         ['Urbanisation, deforestation and building on flood plains increase run-off and exposure.', 'Climate change is intensifying rainfall (Pakistan 2022).'],
         ['Monsoon rainfall, snowmelt and storms are natural causes; Bangladesh has always flooded.', 'Flash floods in steep impermeable basins (Boscastle) are mainly physical.'],
         'Physical factors trigger most floods, but human activity increasingly makes them more frequent and more damaging.',
         ['urbanisation', 'deforestation', 'monsoon', 'climate change']),
    ],
})


@c3d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c3d_rain(r, D):
    c = place(r, 'river')
    days = r.choice([5, 6, 7])
    rain = [r.choice([0, 2, 5, 8, 12, 18, 25, 30, 42, 55, 70]) for _ in range(days)]
    if sum(rain) == 0 or len(set(rain)) < 3:
        return None
    cap_ = r.choice([90, 110, 140])
    q = [round(cap_ * r.uniform(0.3, 0.6))]
    for x in rain[1:]:
        q.append(round(q[-1] * 0.8 + x * r.uniform(1.2, 2.2)))
    labs = [f'day {i + 1}' for i in range(days)]
    over = [labs[i] for i in range(days) if q[i] > cap_]
    stem = (f'A river near {c} has a bankfull discharge of {cap_} cumecs. Table 3.2 shows daily rainfall and mean river discharge. '
            + ' '.join(f'{l}: {x} mm, {y} cumecs.' for l, x, y in zip(labs, rain, q)))
    if D == 1:
        opts, a = mcq(r, f'{sum(rain)} mm', [f'{max(rain)} mm', f'{sum(rain) + 10} mm', f'{round(mean(rain))} mm', f'{sum(rain) - min(10, sum(rain) - 1)} mm'])
        return {'stem': stem + ' What was the total rainfall?', 'options': opts, 'answer': a, 'key': f'{"+".join(map(str, rain))} = {sum(rain)} mm. [1]'}
    parts = [
        lambda r: ('Calculate the total rainfall for the period.', f'{sum(rain)} mm', f'{"+".join(map(str, rain))} = {sum(rain)} mm [1]'),
        lambda r: ('State on which days the river would have flooded.', (', '.join(over) if over else 'None: discharge stayed below bankfull'), f'Days with discharge above {cap_} cumecs [1]'),
        lambda r: ('Describe the relationship between rainfall and discharge.', 'Discharge rises after days of heavy rain, with a delay (lag), and stays high when rain falls on several days in a row because the soil becomes saturated.', '1 mark positive link; 1 mark lag/saturation [2]'),
        lambda r: ('Suggest two human actions that could increase the flood risk in this drainage basin.', 'Building on the flood plain (impermeable surfaces, drains); deforestation upstream; draining wetlands; overgrazing.', '1 mark each [2]'),
        lambda r: ('Explain why the discharge does not fall to zero on dry days.', 'Base flow is maintained by groundwater and throughflow reaching the river slowly.', '1 mark base flow; 1 mark groundwater/throughflow [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 3.5 managing flood risk
SCHEMES = [('raise and extend embankments (levees)', 'hard'), ('build a flood relief channel', 'hard'), ('build a dam and reservoir upstream', 'hard'),
           ('plant trees in the upper basin (afforestation)', 'soft'), ('restrict building on the flood plain (land-use zoning)', 'soft'),
           ('install a flood warning system', 'soft'), ('restore wetlands and allow some fields to flood', 'soft'), ('straighten and deepen the channel', 'hard')]

c3e = T('Managing river flood risk', 'managing river flood risk')
build(c3e, {
    'terms': [
        ('hard engineering', 'building artificial structures, such as dams, embankments and relief channels, to control rivers'),
        ('soft engineering', 'working with natural processes to reduce flood risk, such as afforestation, wetlands and land-use zoning'),
        ('embankment', 'a raised artificial bank along a river that increases the channel’s capacity'),
        ('flood relief channel', 'an artificial channel that diverts excess water away from a settlement during a flood'),
        ('channel straightening', 'removing meanders to make water flow away faster'),
        ('afforestation', 'planting trees in a drainage basin to increase interception and slow run-off'),
        ('land-use zoning', 'planning rules that restrict development in areas at high risk of flooding'),
        ('cost-benefit analysis', 'comparing the costs of a scheme with the value of the damage it prevents'),
    ],
    'mcq': [
        ('Which of these is an example of soft engineering?', 'Planting trees in the upper drainage basin', ['Building a concrete flood wall', 'Building a dam', 'Straightening the channel'], '[1]'),
        ('What is a disadvantage of straightening a river channel?', 'Flooding may be moved further downstream', ['It slows water down', 'It is completely natural', 'It increases meanders'], '[1]'),
        ('The Three Gorges Dam is on which river?', 'Yangtze', ['Mekong', 'Ganges', 'Nile'], 'Completed 2006/2012; about 1.3 million people relocated. [1]'),
        ('Which of these schemes would be cheapest for a low-income country?', 'Community flood warnings and raised houses', ['A large multi-purpose dam', 'Concrete flood walls along the whole river', 'A relief channel through a city'], '[1]'),
    ],
    'explain': [
        ('Explain how a dam and reservoir reduce flood risk.', 'The reservoir stores water during heavy rain and releases it slowly, controlling discharge downstream.', '1 mark stores water; 1 mark controlled release [2]'),
        ('Explain one advantage and one disadvantage of building embankments.', 'Advantage: increase channel capacity so water stays in the channel. Disadvantage: expensive, may fail catastrophically, stop fertile silt reaching fields and move flooding downstream.', '1 mark each [2]'),
        ('Explain why soft engineering is often considered more sustainable than hard engineering.', 'It works with natural processes, costs less to build and maintain, creates habitats (wetlands) and does not transfer the problem downstream.', '1 mark each point up to [3]'),
        ('Explain how land-use zoning reduces the cost of floods.', 'Only low-value uses (parks, playing fields, farmland) are allowed on land most likely to flood, so less property is damaged and water can be stored.', '1 mark restricts development; 1 mark less damage [2]'),
    ],
    'claims': [
        ('Hard engineering always stops floods completely.', False, 'Structures are designed for floods of a certain size and can be overtopped or fail, as levees did in New Orleans in 2005.'),
        ('Flood warnings do not stop floods but can reduce their impacts.', True, 'They give time to move people, valuables and vehicles to safety.'),
        ('A relief channel moves water away from a town during a flood.', True, 'E.g. the Jubilee River protects Maidenhead and Windsor in the UK.'),
    ],
    'cs': [
        ('a river management scheme', [
            ('the Three Gorges Dam, Yangtze River, China', {'scheme': 'A 2.3 km-wide, 185 m-high concrete dam completed in 2006 (fully operational 2012) with a 600 km-long reservoir; stores floodwater to protect millions downstream; 32 turbines generate up to 22.5 GW of hydro-electric power; ship locks improve navigation.',
                                                           'evaluate': 'Benefits: reduces flood risk downstream (e.g. Wuhan), produces clean electricity and improves shipping. Problems: about 1.3 million people relocated; farmland and heritage sites flooded; silt trapped behind the dam reduces fertility downstream; risk of landslides; cost about US$30 billion. Overall: big benefits but high social and environmental costs.'}),
            ('the Jubilee River flood relief channel, UK', {'scheme': 'An 11.6 km artificial channel opened in 2002 at a cost of about £110 million, diverting water from the River Thames around Maidenhead, Windsor and Eton; designed to look natural with wetlands and reed beds.',
                                                         'evaluate': 'It protects about 3000 properties and created wildlife habitats; however, during the 2014 floods it was blamed for increasing flooding in villages downstream, and it was expensive.'}),
            ('flood management in Bangladesh', {'scheme': 'The Flood Action Plan built embankments along major rivers, raised flood shelters and houses on earth platforms, and improved flood warnings sent by radio and mobile phone; soft measures include floating gardens and community training.',
                                               'evaluate': 'Shelters and warnings have cut deaths sharply, but embankments are costly to maintain, can fail and stop fertile silt reaching fields; the scale of flooding means management reduces impacts rather than stopping floods.'}),
        ], [
            ('describe the methods used to manage the river', 'scheme', 'Named structures/techniques with dimensions, dates, costs; how each reduces flood risk.'),
            ('evaluate the success of the scheme', 'evaluate', 'Advantages and disadvantages for people, the economy and the environment, with a judgement.'),
        ]),
    ],
    'essays': [
        ('hard engineering is the best way to manage river flood risk',
         ['Dams and embankments can protect large cities and valuable land; the Three Gorges Dam reduced flood risk downstream.'],
         ['Hard engineering is expensive, can fail and move flooding downstream.', 'Soft engineering (afforestation, wetlands, zoning, warnings) is cheaper, sustainable and suits LICs.'],
         'The best approach usually combines hard engineering where valuable property is at risk with soft measures across the drainage basin.',
         ['cost', 'sustainability', 'level of development', 'downstream effects']),
    ],
})


@c3e.add('C3', (2, 3, 4, 5), 'numerical')
def c3e_cba(r, D):
    opts = r.sample(SCHEMES, 3)
    c = place(r, 'river')
    rows = []
    for name, kind in opts:
        cost = r.choice([2, 4, 5, 8, 12, 15, 20, 30]) if kind == 'hard' else r.choice([0.5, 1, 1.5, 2, 3, 4])
        props = r.choice([200, 400, 500, 800, 1200, 1500, 2000]) if kind == 'hard' else r.choice([100, 150, 300, 400, 600])
        rows.append((name, kind, cost, props))
    per = [(n, cst * 1e6 / p) for n, _, cst, p in rows]
    best = min(per, key=lambda x: x[1])
    if sorted(x[1] for x in per)[0] == sorted(x[1] for x in per)[1]:
        return None
    stem = f'A town in a river valley near {c} must choose a flood scheme. Table 3.3: ' + ' '.join(f'Option {i + 1}: {n} – cost ${fmt(cst, 1)} million, protects {p} properties.' for i, (n, _, cst, p) in enumerate(rows))
    parts = [
        lambda r: ('Calculate the cost per property protected for each option.', '; '.join(f'Option {i + 1}: ${fmt(round(v), 0)}' for i, (_, v) in enumerate(per)), 'cost ÷ properties for each (1 mark for two correct, 2 for three) [2]'),
        lambda r: ('Identify which options are hard engineering and which are soft engineering.', '; '.join(f'Option {i + 1}: {k}' for i, (_, k, _, _) in enumerate(rows)), '[2]'),
        lambda r: ('Which option gives the best value for money? Use your answer to support your choice.', f'Option {[x[0] for x in per].index(best[0]) + 1} ({best[0]}), lowest cost per property (${fmt(round(best[1]), 0)}).', '1 mark choice; 1 mark use of data [2]'),
        lambda r: ('Suggest why the town might not choose the option with the lowest cost per property.', 'It may protect too few properties, may harm the environment or move flooding downstream, may need high maintenance, or local people may oppose it; social and environmental costs are not included.', '1 mark each point up to [3]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c3e.add('C2', (1, 2, 3), 'short')
def c3e_classify(r, D):
    name, kind = r.choice(SCHEMES)
    if D == 1:
        opts, a = mcq(r, cap(kind) + ' engineering', ['Hard engineering' if kind == 'soft' else 'Soft engineering', 'Neither: it increases flood risk', 'Prediction only', 'Emergency response'])
        return {'stem': f'A council decides to {name}. How is this method classified?', 'options': opts, 'answer': a, 'key': f'{cap(kind)} engineering. [1]'}
    why = {'hard': 'it uses built structures to control the river', 'soft': 'it works with natural processes or changes how people use the land'}[kind]
    return {'stem': f'A council decides to {name}. Classify this as hard or soft engineering, and explain how it reduces flood risk.',
            'answer': f'{cap(kind)} engineering, because {why}. ' + {
                'raise and extend embankments (levees)': 'Higher banks increase the volume the channel can hold.', 'build a flood relief channel': 'Excess water is diverted around the town.',
                'build a dam and reservoir upstream': 'Water is stored and released slowly.', 'plant trees in the upper basin (afforestation)': 'More interception and infiltration slow run-off and lengthen lag time.',
                'restrict building on the flood plain (land-use zoning)': 'Fewer buildings at risk and less impermeable surface.', 'install a flood warning system': 'People can move belongings and evacuate in time.',
                'restore wetlands and allow some fields to flood': 'Water is stored on low-value land, reducing peaks downstream.', 'straighten and deepen the channel': 'Water flows away faster and the channel holds more.'}[name],
            'key': '1 mark classification; 1 mark explanation of how it works [2]', 'marks': 2, 'type': 'explain'}


CHAPTERS[3] = [c3a, c3b, c3c, c3d, c3e]


# ============================================================== CHAPTER 4: Coasts

c4a = T('Wave types and coastal processes: erosion, transportation, deposition and longshore drift', 'wave types coastal processes longshore drift')
build(c4a, {
    'terms': [
        ('fetch', 'the distance of open water over which the wind blows to form waves'),
        ('swash', 'the movement of water up a beach after a wave breaks'),
        ('backwash', 'the movement of water back down a beach towards the sea under gravity'),
        ('constructive wave', 'a low, gentle wave with a strong swash and weak backwash that builds up beaches'),
        ('destructive wave', 'a tall, steep, frequent wave with a weak swash and strong backwash that erodes beaches'),
        ('longshore drift', 'the zig-zag movement of sediment along a coast caused by waves approaching at an angle to the shore'),
        ('prevailing wind', 'the direction from which the wind most often blows at a place'),
        ('hydraulic action', 'erosion caused by waves forcing water and compressed air into cracks in the cliff'),
        ('abrasion', 'erosion when waves throw sand and pebbles against the cliff, wearing it away'),
        ('sub-aerial processes', 'weathering and mass movement acting on the cliff face above the level of the waves'),
    ],
    'mcq': [
        ('Which type of wave has a strong backwash and erodes beaches?', 'Destructive wave', ['Constructive wave', 'Spilling swash wave', 'Tidal bore'], '[1]'),
        ('In longshore drift, sediment moves up the beach at an angle because', 'the swash follows the direction of the prevailing wind', ['the backwash is always at an angle', 'tides flow sideways', 'sediment is pushed by rivers'], 'Backwash returns straight down the beach under gravity. [1]'),
        ('Which factor makes waves larger?', 'A longer fetch', ['A shorter fetch', 'Lighter wind', 'Calmer weather'], 'Wave size depends on wind speed, duration and fetch. [1]'),
        ('Constructive waves typically break at about', '6-8 waves per minute', ['13-15 waves per minute', '1 wave per hour', '30 waves per minute'], '[1]'),
        ('Which process involves chemicals in seawater dissolving rocks such as chalk and limestone?', 'Solution (corrosion)', ['Attrition', 'Hydraulic action', 'Saltation'], '[1]'),
    ],
    'explain': [
        ('Describe the differences between constructive and destructive waves.', 'Constructive: low, long wavelength, 6-8 per minute, strong swash, weak backwash, build beaches. Destructive: high, steep, 13-15 per minute, weak swash, strong backwash, erode beaches.', '1 mark each valid difference up to [3]'),
        ('Explain the process of longshore drift.', 'Waves approach at an angle due to the prevailing wind; swash carries sediment up the beach at that angle; backwash returns it straight down under gravity; repeated, this moves sediment in a zig-zag along the coast.', '1 mark angle of swash; 1 mark backwash at right angles; 1 mark zig-zag movement [3]'),
        ('Explain how hydraulic action erodes a cliff.', 'Breaking waves force water and air into cracks; the air is compressed and, when the wave retreats, expands explosively, widening the cracks until pieces break off.', '1 mark compressed air in cracks; 1 mark repeated widening [2]'),
        ('Explain why erosion is greatest during storms.', 'Strong winds create large, destructive waves with more energy; they hurl more sediment at the cliffs (abrasion) and hydraulic action is greater.', '1 mark larger waves; 1 mark more abrasion/hydraulic action [2]'),
    ],
    'claims': [
        ('Backwash moves sediment along the coast at an angle.', False, 'Backwash runs straight down the beach under gravity; the swash moves at an angle.'),
        ('Destructive waves are more common in winter storms.', True, 'Stronger winds in storms produce taller, steeper, more frequent waves.'),
        ('A longer fetch generally produces bigger waves.', True, 'The wind has more distance to transfer energy to the water.'),
    ],
    'essays': [
        ('wave type is the most important factor affecting the rate of coastal erosion',
         ['Destructive waves with long fetch and storms cause rapid erosion.'],
         ['Rock type and structure matter: soft boulder clay at Holderness erodes about 2 m a year while granite erodes very slowly.', 'Beaches absorb wave energy; human defences and sub-aerial processes also affect rates.'],
         'Wave energy drives erosion, but geology often determines how fast it happens.',
         ['rock type', 'fetch', 'beaches', 'storms']),
    ],
})


@c4a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c4a_drift(r, D):
    beach = r.choice(['a beach near ' + place(r, 'coast'), 'Holderness, England', 'a spit on the Gulf of Guinea coast', 'a beach on the Black Sea coast'])
    trials = r.choice([4, 5])
    t = r.choice([10, 15, 20, 30])
    dists = [round(r.uniform(2, 14), 1) for _ in range(trials)]
    if len(set(dists)) < trials:
        return None
    mn = mean(dists)
    rate = mn / t  # m per minute
    dirn = r.choice(['east', 'west', 'north', 'south'])
    stem = (f'Students measured longshore drift at {beach}. They placed a painted pebble at the water line and measured how far it had moved {dirn} after {t} minutes. '
            f'Results for {trials} trials (m): ' + ', '.join(fmt(x, 1) for x in dists) + '.')
    if D == 1:
        opts, a = mcq(r, f'{dp(mn, 2)} m', [f'{dp(sum(dists), 1)} m', f'{dp(max(dists) - min(dists), 1)} m', f'{dp(mn / t, 2)} m', f'{dp(median(dists), 2)} m'])
        return {'stem': stem + ' What is the mean distance moved?', 'options': opts, 'answer': a, 'key': f'{dp(sum(dists), 1)} ÷ {trials} = {dp(mn, 2)} m. [1]'}
    hrs = rate * 60
    opp = {'east': 'west', 'west': 'east', 'north': 'south', 'south': 'north'}[dirn]
    parts = [
        lambda r: ('Calculate the mean distance moved.', f'{dp(mn, 2)} m', f'{"+".join(fmt(x, 1) for x in dists)} = {dp(sum(dists), 1)}; ÷ {trials} = {dp(mn, 2)} m [2]'),
        lambda r: ('Calculate the mean rate of movement in metres per hour.', f'{dp(hrs, 1)} m/h', f'{dp(mn, 2)} ÷ {t} × 60 = {dp(hrs, 1)} m per hour [2]'),
        lambda r: ('Suggest the direction of the prevailing wind. Explain your answer.', f'From the {opp} side (waves approach at an angle from the {opp}): swash pushes sediment in the direction the waves travel, which is set by the prevailing wind.', '1 mark direction; 1 mark explanation [2]'),
        lambda r: ('Suggest two reasons why the results varied between trials.', 'Changes in wave size or angle; the pebble may have been buried or moved by people; measurement error; different pebble sizes.', '1 mark each [2]'),
        lambda r: ('Describe one safety precaution the students should take.', 'Check tide times and work in groups away from cliffs; do not enter the water in rough conditions.', '[1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c4a.add('C2', (1, 2, 3), 'short')
def c4a_wave(r, D):
    f = r.choice([6, 7, 8, 13, 14, 15])
    h = r.choice([0.5, 0.8, 1.0]) if f <= 8 else r.choice([2.5, 3.0, 4.0])
    kind = 'constructive' if f <= 8 else 'destructive'
    stem = f'An observer counts {f} waves breaking per minute on a beach. Each wave is about {fmt(h, 1)} m high.'
    if D == 1:
        opts, a = mcq(r, cap(kind), ['Destructive' if kind == 'constructive' else 'Constructive', 'Tsunami', 'Tidal wave'])
        return {'stem': stem + ' What type of wave is this most likely to be?', 'options': opts, 'answer': a, 'key': f'{f} per minute = {kind}. [1]'}
    eff = 'build up the beach because the strong swash carries sediment up and the weak backwash leaves it there' if kind == 'constructive' else 'erode the beach because the weak swash and strong backwash drag sediment offshore, making the beach flatter'
    return {'stem': stem + ' Identify the type of wave and explain its likely effect on the beach.', 'answer': f'{cap(kind)} waves, which {eff}.',
            'key': '1 mark type; 1 mark swash/backwash; 1 mark effect on beach [3]', 'marks': 3, 'type': 'explain'}


# --------------------------------------------------------------- 4.2 erosional landforms
c4b = T('Erosional coastal landforms: cliffs, wave-cut platforms, caves, arches and stacks', 'cliffs wave-cut platforms caves arches stacks')
build(c4b, {
    'terms': [
        ('headland', 'a section of hard rock that sticks out into the sea, with water on three sides'),
        ('bay', 'a wide, curved inlet of the sea between two headlands, formed where softer rock is eroded'),
        ('wave-cut notch', 'an undercut at the base of a cliff between high and low tide, eroded by waves'),
        ('wave-cut platform', 'a flat, rocky area at the foot of a cliff, exposed at low tide, left as the cliff retreats'),
        ('cave', 'a hollow eroded into a weakness such as a joint or fault at the base of a headland'),
        ('arch', 'a gap through a headland formed when caves on either side are eroded until they meet'),
        ('stack', 'an isolated pillar of rock left when the roof of an arch collapses'),
        ('stump', 'a small remnant of a stack, eroded until it is covered at high tide'),
        ('discordant coastline', 'a coast where bands of hard and soft rock run at right angles to the coastline, forming headlands and bays'),
    ],
    'mcq': [
        ('What is the correct sequence of landforms as a headland is eroded?', 'Crack → cave → arch → stack → stump', ['Stack → arch → cave → stump', 'Cave → stack → arch → stump', 'Arch → cave → stump → stack'], '[1]'),
        ('Where do headlands and bays form?', 'Where bands of hard and soft rock meet the coast at right angles', ['Only where all the rock is soft', 'Where rivers enter the sea', 'Where coral grows'], '[1]'),
        ('Old Harry Rocks in Dorset, England, are an example of', 'chalk stacks', ['a spit', 'a delta', 'a coral atoll'], '[1]'),
        ('A wave-cut platform is exposed', 'at low tide', ['only during storms', 'at high tide', 'never'], '[1]'),
    ],
    'explain': [
        ('Explain how a wave-cut platform forms.', 'Waves erode the base of the cliff between high and low tide by hydraulic action and abrasion, forming a wave-cut notch; the overhang above collapses; the process repeats so the cliff retreats, leaving a gently sloping platform.', '1 mark notch; 1 mark collapse; 1 mark retreat leaves platform [3]'),
        ('Explain how a stack forms from a headland.', 'Waves erode a weakness (joint or fault) into a cave; caves on both sides meet to form an arch; the arch is widened and its roof is weakened by erosion and weathering until it collapses, leaving an isolated stack.', '1 mark cave; 1 mark arch; 1 mark roof collapse [3]'),
        ('Explain why headlands and bays form on a discordant coastline.', 'Soft rock (e.g. clay) is eroded quickly to form bays; hard rock (e.g. chalk, limestone) is more resistant and is left sticking out as headlands.', '1 mark differential erosion; 1 mark hard/soft outcome [2]'),
        ('Explain why the rate of cliff retreat varies from place to place.', 'Rock type and structure (soft clay vs granite), wave energy and fetch, presence of a protective beach, sub-aerial weathering, and human defences all differ.', '1 mark each factor up to [3]'),
    ],
    'claims': [
        ('Stacks form before arches.', False, 'An arch forms first; when its roof collapses a stack is left.'),
        ('Headlands are made of more resistant rock than bays.', True, 'Hard rock erodes more slowly than the soft rock in bays.'),
        ('Wave-cut platforms form at the top of the cliff.', False, 'They form at the base of a retreating cliff, between high and low tide.'),
    ],
    'cases': [
        (['Fig. 4.1 describes the coast of Dorset, England. Bands of chalk and limestone (hard) alternate with clay and sand (soft), running at right angles to the coast. At Old Harry Rocks a chalk headland ends in two stacks and a stump; at Durdle Door there is a limestone arch; Swanage Bay is cut into soft clay.',
          'Study Fig. 4.1, information about a discordant coastline in southern England. Hard chalk forms the headland at Handfast Point with the stacks of Old Harry Rocks; softer sands and clays form Studland Bay and Swanage Bay; further west a limestone arch stands at Durdle Door.'],
         [('Name the landforms formed in soft and in hard rock.', 'Soft rock: bays (Swanage, Studland). Hard rock: headlands, arches, stacks and stumps.', '1 mark each [2]'),
          ('Explain the formation of Old Harry Rocks.', 'Hydraulic action and abrasion widened joints in the chalk headland into caves, then an arch; the arch collapsed, leaving stacks; a stack has been eroded to a stump.', '1 mark cave; 1 mark arch; 1 mark collapse [3]'),
          ('Suggest why the bays are wide and curved.', 'Soft clay and sand were eroded quickly; waves refract into the bay and spread energy, depositing sand to form a beach.', '1 mark rapid erosion; 1 mark deposition/wave refraction [2]'),
          ('Suggest one way the landforms attract visitors and one problem visitors cause.', 'Attraction: spectacular scenery, walking, photography, beaches. Problem: footpath erosion, litter, traffic congestion in summer.', '1 mark each [2]')]),
    ],
})


@c4b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c4b_retreat(r, D):
    site = r.choice(['Holderness, England', 'a clay cliff near ' + place(r, 'coast'), 'a cliff on the Baltic coast', 'Happisburgh, England', 'a sandstone cliff on the Black Sea coast'])
    y1 = r.choice([1990, 1995, 2000, 2005])
    yrs = r.choice([10, 15, 20, 25])
    lost = round(r.uniform(8, 50))
    rate = lost / yrs
    house = r.choice([30, 40, 50, 60, 80, 100])
    years_left = house / rate
    stem = f'At {site}, the cliff edge retreated {lost} m between {y1} and {y1 + yrs}.'
    if D == 1:
        opts, a = mcq(r, f'{dp(rate, 2)} m per year', [f'{dp(rate * 2, 2)} m per year', f'{lost} m per year', f'{dp(yrs / lost, 2)} m per year', f'{dp(rate / 2, 2)} m per year'])
        return {'stem': stem + ' What is the mean rate of retreat?', 'options': opts, 'answer': a, 'key': f'{lost} ÷ {yrs} = {dp(rate, 2)} m/yr. [1]'}
    parts = [
        lambda r: ('Calculate the mean rate of cliff retreat per year.', f'{dp(rate, 2)} m per year', f'{lost} ÷ {yrs} = {dp(rate, 2)} m/yr [1]'),
        lambda r: (f'A house is now {house} m from the cliff edge. Estimate how many years it will be before the cliff reaches it, if the rate stays the same.', f'about {round(years_left)} years',
                   f'{house} ÷ {dp(rate, 2)} = {dp(years_left, 1)} ≈ {round(years_left)} years [2]'),
        lambda r: ('Suggest why the rate of retreat may not stay the same.', 'Storms and sea-level rise may speed it up; new defences or a wider beach may slow it; slumping happens in sudden events rather than steadily.', '1 mark each reason up to [2]'),
        lambda r: ('Explain why soft cliffs such as boulder clay retreat quickly.', 'Clay is weak and easily eroded by waves; rain saturates it, causing slumping; eroded material is easily washed away so the cliff base is not protected.', '1 mark weak rock; 1 mark slumping/weathering [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c4b.add('C2', (1, 2, 3), 'short')
def c4b_seq(r, D):
    st = ['Waves erode a joint or fault at the base of the headland by hydraulic action.', 'The crack is enlarged into a cave.', 'Caves on opposite sides of the headland meet to form an arch.',
          'The arch roof is weakened by erosion and weathering and collapses.', 'An isolated stack is left, which is eroded into a stump.']
    k = 4 if D <= 2 else 5
    steps = st[:4] if k == 4 and r.random() < 0.5 else (st[1:] if k == 4 else st)
    lab = 'PQRST'[:len(steps)]
    order = list(range(len(steps)))
    r.shuffle(order)
    if order == sorted(order):
        order = order[::-1]
    shown = [steps[i] for i in order]
    ans = ', '.join(lab[order.index(i)] for i in range(len(steps)))
    return {'stem': 'Put these statements about the erosion of a headland into the correct order. ' + ' '.join(f'{lab[j]}: {s}' for j, s in enumerate(shown)),
            'answer': ans, 'key': f'Correct order {ans}. 2 marks all correct; 1 mark if one pair reversed. [2]', 'marks': 2, 'type': 'short'}


# --------------------------------------------------------------- 4.3 depositional landforms
c4c = T('Depositional coastal landforms: beaches, spits and bars', 'beaches spits bars')
build(c4c, {
    'terms': [
        ('beach', 'an accumulation of sand and shingle deposited by waves between low tide and the highest storm waves'),
        ('spit', 'a long, narrow ridge of sand or shingle joined to the land at one end and extending out to sea, formed by longshore drift'),
        ('bar', 'a ridge of sand or shingle that extends across a bay, joining two headlands and trapping a lagoon behind it'),
        ('tombolo', 'a ridge of sand or shingle that joins an island to the mainland'),
        ('recurved end', 'the curved tip of a spit formed when waves from a different direction bend the end inland'),
        ('salt marsh', 'an area of mud and salt-tolerant plants that develops in the sheltered water behind a spit'),
        ('berm', 'a ridge of sand or shingle on a beach marking the high tide or storm limit'),
        ('sand dune', 'a hill of wind-blown sand found behind a beach, stabilised by plants such as marram grass'),
    ],
    'mcq': [
        ('Which process is mainly responsible for the formation of spits?', 'Longshore drift', ['Hydraulic action', 'Vertical erosion', 'Freeze-thaw weathering'], '[1]'),
        ('What usually forms in the sheltered area behind a spit?', 'Salt marsh', ['A stack', 'A wave-cut platform', 'A gorge'], '[1]'),
        ('A ridge of sand that joins an island to the mainland is called a', 'tombolo', ['bar', 'spit', 'stump'], '[1]'),
        ('Spurn Head at the mouth of the Humber estuary is an example of', 'a spit', ['a stack', 'a bar', 'a coral reef'], '[1]'),
        ('Why do spits often have a curved (recurved) end?', 'Waves from a second direction bend the end towards the land', ['The river pushes it straight', 'Tides always flow in circles', 'People build it that way'], '[1]'),
    ],
    'explain': [
        ('Explain how a spit forms.', 'Longshore drift carries sediment along the coast; where the coast changes direction (e.g. at a river mouth), sediment continues to be deposited in the same direction into the sea, building a ridge; waves from another direction curve the end; salt marsh forms behind.', '1 mark longshore drift; 1 mark change in coastline direction; 1 mark deposition builds out; 1 mark recurved end/salt marsh [4]'),
        ('Explain why a bar can form across a bay.', 'Longshore drift extends a spit across the bay; if no strong river current cuts through, it joins the far headland, trapping a lagoon.', '1 mark spit extends; 1 mark no river current; 1 mark lagoon [3]'),
        ('Explain why sand beaches are found in bays.', 'Waves refract in bays, spreading their energy, so they are lower-energy constructive waves that deposit sand.', '1 mark low energy; 1 mark deposition [2]'),
        ('Explain why a river mouth can prevent a spit from becoming a bar.', 'The river’s flow carries sediment away and keeps the channel open, so the spit cannot join the opposite shore.', '1 mark river current; 1 mark keeps gap open [2]'),
    ],
    'claims': [
        ('Spits form where destructive waves are eroding the coast.', False, 'Spits are depositional; they need a supply of sediment and longshore drift.'),
        ('Sand dunes are stabilised by plants such as marram grass.', True, 'Long roots bind the sand and the plant tolerates burial and salt.'),
        ('A bar can trap a lagoon behind it.', True, 'When a bar closes a bay, water behind it becomes a lagoon, e.g. Slapton Ley in Devon.'),
    ],
    'cases': [
        (['Fig. 4.2 is a map of Spurn Head, a spit at the mouth of the Humber estuary in England. Longshore drift moves sediment south along the Holderness coast. The spit is about 5 km long, curves west at its tip, and has salt marsh on its sheltered western side. The River Humber flows east into the sea past the end of the spit.',
          'Study Fig. 4.2, which describes a spit. Material eroded from boulder-clay cliffs to the north is carried south by longshore drift. The spit extends across the mouth of an estuary, its end curves inland, and mudflats and salt marsh lie behind it.'],
         [('State the direction of longshore drift shown in Fig. 4.2.', 'Southwards.', '[1]'),
          ('Explain how the spit has formed.', 'Longshore drift carries sediment south; where the coastline turns at the estuary, deposition continues out to sea, building a ridge of sand and shingle.', '1 mark longshore drift; 1 mark change in direction; 1 mark deposition [3]'),
          ('Explain why the end of the spit is curved.', 'Waves from a second direction (and the estuary currents) bend the tip inland.', '[2]'),
          ('Explain why the spit has not grown across the estuary to form a bar.', 'The river’s flow and tides scour the channel and carry sediment away.', '[2]'),
          ('Suggest how salt marsh has developed behind the spit.', 'Sheltered, calm water lets fine silt and mud settle; salt-tolerant plants colonise and trap more sediment.', '1 mark sheltered deposition; 1 mark vegetation [2]')]),
    ],
})


@c4c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c4c_profile(r, D):
    n = r.choice([5, 6])
    seg = r.choice([5, 10])
    angs = [r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15]) for _ in range(n)]
    sizes = sorted((r.randint(2, 90) for _ in range(n)))
    if len(set(sizes)) < n:
        return None
    beach = r.choice(['a beach near ' + place(r, 'coast'), 'a shingle beach', 'a bay beach', 'a beach beside a spit'])
    rise = [seg * math.sin(math.radians(a)) for a in angs]
    tot = sum(rise)
    stem = (f'Students measured the profile of {beach} from the sea to the back of the beach in {n} sections each {seg} m long. Slope angles (°): ' + ', '.join(map(str, angs)) +
            '. Mean pebble size (mm) for each section: ' + ', '.join(map(str, sizes)) + '.')
    if D == 1:
        opts, a = mcq(r, f'{seg * n} m', [f'{seg * (n - 1)} m', f'{seg} m', f'{n} m', f'{seg * n * 2} m'])
        return {'stem': stem + ' What is the total length of the profile?', 'options': opts, 'answer': a, 'key': f'{n} × {seg} = {seg * n} m. [1]'}
    parts = [
        lambda r: ('Calculate the mean slope angle.', f'{dp(mean(angs))}°', f'{sum(angs)} ÷ {n} = {dp(mean(angs))}° [1]'),
        lambda r: ('Identify the steepest section.', f'Section {angs.index(max(angs)) + 1} ({max(angs)}°)', '[1]'),
        lambda r: ('Describe how pebble size changes up the beach.', f'Pebble size increases from {sizes[0]} mm near the sea to {sizes[-1]} mm at the back of the beach.', '1 mark trend; 1 mark data [2]'),
        lambda r: ('Explain why larger pebbles are found at the back of the beach.', 'Only powerful storm-wave swash can throw large pebbles high up the beach; the weak backwash cannot carry them back down.', '1 mark storm swash; 1 mark weak backwash [2]'),
        lambda r: ('Describe how the students should have measured the slope angle.', 'Two ranging poles placed at each break of slope (or every 5/10 m); a clinometer used to sight between equal heights on the poles; distance measured with a tape.', '1 mark ranging poles/tape; 1 mark clinometer [2]'),
        lambda r: (f'Calculate the total height gained across the profile to one decimal place, using height = length × sin(angle) for each section.', f'{dp(tot, 1)} m',
                   '; '.join(f'{seg} sin {a}° = {dp(h, 2)}' for a, h in zip(angs, rise)) + f'; total = {dp(tot, 1)} m [2]'),
    ]
    k = (2, 3) if D <= 3 else (3, 4)
    return compose(r, stem, parts[:5] if D <= 3 else parts, k=k, type_='numerical')


# --------------------------------------------------------------- 4.4 coral reefs and mangroves
c4d = T('Coral reefs and mangrove swamps: conditions for formation and value', 'coral reefs mangrove swamps')
build(c4d, {
    'terms': [
        ('coral polyp', 'a tiny animal with a soft body that builds a hard skeleton of calcium carbonate; colonies of polyps form reefs'),
        ('zooxanthellae', 'algae living inside coral polyps that photosynthesise and provide food and colour to the coral'),
        ('fringing reef', 'a coral reef that grows close to the shore of a coastline or island'),
        ('barrier reef', 'a coral reef separated from the coast by a wide, deep lagoon, such as the Great Barrier Reef'),
        ('atoll', 'a ring of coral reef surrounding a lagoon, often formed around a sinking volcanic island'),
        ('coral bleaching', 'the whitening of coral when stressed by high water temperatures, which makes it expel its algae'),
        ('mangrove', 'a salt-tolerant tree that grows in the intertidal zone of tropical coasts, with roots above the mud'),
        ('pneumatophores', 'aerial roots of mangroves that stick up from the mud to take in oxygen'),
    ],
    'mcq': [
        ('Which water temperature range do reef-building corals need?', 'About 18-30 °C (ideally 23-25 °C)', ['Below 10 °C', 'About 35-40 °C', '0-5 °C'], '[1]'),
        ('Why do corals usually grow in water less than about 60 m deep?', 'Their algae need sunlight to photosynthesise', ['Deep water is too salty', 'Fish eat them in deep water', 'They need cold water'], '[1]'),
        ('Why do corals not grow at the mouths of large rivers?', 'The water is muddy and fresh, blocking light and lowering salinity', ['The water is too warm', 'There are no waves', 'The rock is too hard'], '[1]'),
        ('The Sundarbans, the world’s largest mangrove forest, is in', 'Bangladesh and India', ['Australia and New Zealand', 'Brazil', 'Egypt'], '[1]'),
        ('Which of these is the main cause of mass coral bleaching?', 'Sea temperatures rising above normal', ['Cold winters', 'Low tides', 'Too many fish'], '[1]'),
    ],
    'explain': [
        ('Describe the conditions needed for coral reefs to grow.', 'Warm water (about 18-30 °C), clear and shallow (less than about 60 m) so light reaches the algae, salt water (no river water) and low sediment, and a solid base to grow on.', '1 mark each condition up to [3]'),
        ('Explain the value of coral reefs to people.', 'Fishing and food; tourism (diving, snorkelling) income and jobs; coastal protection by absorbing wave energy; medicines from reef species; high biodiversity.', '1 mark each developed point up to [3]'),
        ('Explain how mangroves protect coastlines.', 'Dense roots slow waves and storm surges, trap sediment and reduce erosion, so cyclones such as Sidr (2007) caused less damage behind mangroves.', '1 mark absorb energy; 1 mark trap sediment [2]'),
        ('Explain why mangrove swamps are being destroyed.', 'Cleared for shrimp farms, rice, tourism resorts, ports and housing; cut for firewood and charcoal; polluted by oil and waste.', '1 mark each reason up to [3]'),
    ],
    'claims': [
        ('Coral reefs can grow in deep, cold water as long as there are waves.', False, 'Reef-building corals need warm, shallow, clear water so that their algae can photosynthesise.'),
        ('Mangroves are adapted to grow in salty water.', True, 'They have salt-filtering roots or excrete salt through their leaves.'),
        ('Coral bleaching means the coral has already died.', False, 'Bleached coral is stressed and has lost its algae; it can recover if temperatures fall, but dies if the stress continues.'),
    ],
    'cs': [
        ('a coral reef or mangrove ecosystem', [
            ('the Great Barrier Reef, Australia', {'value': 'About 2300 km long off Queensland; home to about 1500 fish species; tourism worth about AU$6 billion a year and about 64 000 jobs; protects the coast from waves.',
                                                  'threats': 'Mass bleaching in 2016, 2017, 2020, 2022 and 2024 caused by marine heatwaves; crown-of-thorns starfish; run-off of sediment and fertiliser from farms; cyclones; tourism and shipping.',
                                                  'manage': 'Great Barrier Reef Marine Park zoning limits fishing and shipping; Reef 2050 Plan to reduce farm run-off; culling crown-of-thorns starfish; reef restoration trials.'}),
            ('the Sundarbans mangroves, Bangladesh and India', {'value': 'About 10 000 km² of mangroves in the Ganges-Brahmaputra delta; habitat for Bengal tigers and fish nurseries; timber, honey and fishing for millions; protection from cyclones and storm surges.',
                                                               'threats': 'Clearance for shrimp farming and rice; sea-level rise and increasing salinity; cyclones; pollution from shipping and industry; over-harvesting.',
                                                               'manage': 'UNESCO World Heritage site and reserves; limits on wood cutting; mangrove replanting; community forest management.'}),
        ], [
            ('describe the value of the ecosystem to people', 'value', 'Economic (fishing, tourism, products), social and environmental (biodiversity, coastal protection) value, with figures.'),
            ('explain the threats to the ecosystem', 'threats', 'Natural and human threats (warming, bleaching, pollution, clearance, sea-level rise) with explanation.'),
            ('describe how the ecosystem is being managed sustainably', 'manage', 'Protected areas, zoning, restrictions, replanting/restoration, community schemes.'),
        ]),
    ],
})


@c4d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c4d_bleach(r, D):
    sites = r.choice([5, 6])
    names = [f'Reef {chr(65 + i)}' for i in range(sites)]
    temp = [round(r.uniform(26.5, 31.5), 1) for _ in range(sites)]
    bl = [max(0, min(95, round((t - 27.5) * 22 + r.uniform(-8, 8)))) for t in temp]
    if len(set(temp)) < sites:
        return None
    stem = 'Table 4.1 shows maximum sea surface temperature and the percentage of coral bleached at reef sites in one summer. ' + ' '.join(f'{n}: {fmt(t, 1)} °C, {b}% bleached.' for n, t, b in zip(names, temp, bl))
    if D == 1:
        i = bl.index(max(bl))
        opts, a = mcq(r, names[i], [n for n in names if n != names[i]])
        return {'stem': stem + ' Which reef had the most bleaching?', 'options': opts, 'answer': a, 'key': f'{names[i]}: {bl[i]}%. [1]'}
    parts = [
        lambda r: ('Describe the relationship between temperature and bleaching.', 'Positive correlation: higher sea temperatures are linked to more bleaching, especially above about 28-29 °C.', '1 mark positive; 1 mark use of data [2]'),
        lambda r: ('Calculate the mean percentage of coral bleached.', f'{dp(mean(bl))}%', f'{"+".join(map(str, bl))} = {sum(bl)}; ÷ {sites} = {dp(mean(bl))}% [1]'),
        lambda r: ('Explain why high temperatures cause bleaching.', 'Heat stress makes the coral expel its zooxanthellae algae, which give it food and colour; without them it turns white and may starve.', '1 mark algae expelled; 1 mark loss of food/colour [2]'),
        lambda r: ('Suggest two other human activities that damage coral reefs.', 'Pollution and sediment from farms and building; overfishing and blast fishing; tourist damage by divers and anchors; coral mining.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


# --------------------------------------------------------------- 4.5 coastal hazards and management
c4e = T('Coastal hazards and management strategies', 'coastal hazards management strategies')
build(c4e, {
    'terms': [
        ('sea wall', 'a concrete wall built along the coast to reflect wave energy and stop erosion and flooding'),
        ('groyne', 'a wooden or rock barrier built at right angles to the beach to trap sediment moved by longshore drift'),
        ('rock armour', 'large boulders placed at the foot of a cliff or in front of a sea wall to absorb wave energy (rip-rap)'),
        ('gabion', 'a wire cage filled with rocks used to absorb wave energy at the foot of a cliff'),
        ('beach nourishment', 'adding sand or shingle to a beach to make it wider and higher so it absorbs more wave energy'),
        ('managed retreat', 'allowing the sea to flood or erode an area of low-value land, creating new salt marsh as a natural defence'),
        ('storm surge', 'a rise in sea level caused by low pressure and strong winds pushing water towards the coast'),
        ('integrated coastal zone management', 'managing a whole stretch of coastline together so that a scheme in one place does not cause problems elsewhere'),
    ],
    'mcq': [
        ('Which coastal defence traps sediment moving by longshore drift?', 'Groynes', ['Sea wall', 'Managed retreat', 'Cliff drainage'], '[1]'),
        ('What is a problem caused by building groynes?', 'Beaches further down the coast become starved of sand and erode faster', ['They make beaches wider downdrift', 'They stop all waves', 'They increase cliff height'], '[1]'),
        ('Which is a soft engineering method of coastal management?', 'Beach nourishment', ['Sea wall', 'Rock armour', 'Concrete revetment'], '[1]'),
        ('About how fast does the Holderness coast in England erode on average?', 'About 2 m per year', ['About 2 cm per year', 'About 200 m per year', 'It does not erode'], 'One of the fastest-eroding coasts in Europe. [1]'),
    ],
    'explain': [
        ('Explain one advantage and one disadvantage of a sea wall.', 'Advantage: very effective at protecting buildings and roads behind it. Disadvantage: expensive (thousands of $ per metre), can be undermined by scouring, reflects energy and lowers the beach in front, looks unnatural.', '1 mark each [2]'),
        ('Explain how managed retreat can be a sustainable option.', 'Low-value farmland is allowed to flood, creating salt marsh that absorbs wave energy and provides habitats at little cost, instead of maintaining expensive defences.', '1 mark allowing flooding; 1 mark natural defence/cheap [2]'),
        ('Explain why coastal flooding is becoming a greater hazard.', 'Sea level is rising due to thermal expansion and melting ice; storms may be more intense; more people live in low-lying coastal cities.', '1 mark each [3]'),
        ('Explain why protecting one part of a coast can increase erosion elsewhere.', 'Defences such as groynes trap sediment, so less reaches beaches downdrift; narrower beaches there absorb less wave energy and the cliffs behind erode faster (e.g. south of Mappleton).', '1 mark sediment trapped; 1 mark effect downdrift [2]'),
    ],
    'claims': [
        ('Hard engineering is always the best way to protect a coastline.', False, 'It is expensive and can cause problems elsewhere; soft engineering or managed retreat may be cheaper and more sustainable.'),
        ('Rock armour absorbs wave energy.', True, 'Gaps between the boulders absorb and break up waves, reducing erosion.'),
        ('Beach nourishment is a permanent solution.', False, 'Waves and longshore drift remove the added sand, so it must be repeated regularly.'),
    ],
    'cs': [
        ('coastal management', [
            ('the Holderness coast, England', {'scheme': 'The boulder-clay coast erodes about 2 m a year; at Mappleton (1991) about £2 million was spent on two rock groynes and rock armour; Hornsea and Withernsea have sea walls and groynes; other stretches are left undefended.',
                                              'evaluate': 'Mappleton’s defences protected the village and the coast road, but trapped sediment so cliffs to the south eroded faster; protecting the whole coast would cost far more than the value of the farmland, so the shoreline management plan defends only towns.'}),
            ('coastal protection in the Maldives', {'scheme': 'Most islands are less than 1.5 m above sea level; Malé is surrounded by a 3 m concrete sea wall and tetrapods built with Japanese aid; Hulhumalé, a new artificial island about 2 m above sea level, is being built for housing; coral reef protection.',
                                                   'evaluate': 'The sea wall protected Malé from the 2004 tsunami, but is very expensive and damages reefs; raising land is costly; in the long term rising sea levels threaten the survival of many islands.'}),
        ], [
            ('describe the strategies used to manage the coast', 'scheme', 'Named hard and soft strategies, with locations, costs and dates.'),
            ('evaluate the strategies used to manage the coast', 'evaluate', 'Successes and problems (cost, effects downdrift, environment), with a judgement.'),
        ]),
    ],
    'essays': [
        ('soft engineering is a better way of managing coastlines than hard engineering',
         ['Beach nourishment, dune restoration and managed retreat work with natural processes, cost less and create habitats.'],
         ['Hard engineering such as sea walls is needed to protect valuable towns, ports and infrastructure (Malé, Hornsea).', 'Soft methods need repeating and may not stop rapid erosion.'],
         'Soft engineering is more sustainable, but hard engineering remains necessary where high-value land is at risk; integrated management combines both.',
         ['cost', 'sustainability', 'value of land', 'effects downdrift']),
    ],
})


@c4e.add('C3', (2, 3, 4, 5), 'numerical')
def c4e_cost(r, D):
    length = r.choice([400, 600, 800, 1000, 1500, 2000])
    opts = [('sea wall', r.choice([6000, 8000, 10000]), 50), ('rock armour', r.choice([1500, 2500, 3500]), 30), ('groynes', r.choice([1000, 1500, 2000]), 25), ('beach nourishment', r.choice([500, 800, 1200]), 5)]
    pick = r.sample(opts, 3)
    town = r.choice(['a seaside town', 'a fishing village', 'a holiday resort', 'a coastal village with a caravan park'])
    value = r.choice([20, 30, 50, 80])  # $ million of property protected
    rows = [(n, c, life, c * length / 1e6, c * length / life / 1e6) for n, c, life in pick]
    cheapest = min(rows, key=lambda x: x[4])
    if sorted(x[4] for x in rows)[0] == sorted(x[4] for x in rows)[1]:
        return None
    stem = (f'A council must protect {length} m of coast in front of {town}; the property protected is worth about ${value} million. Table 4.2: '
            + ' '.join(f'{cap(n)}: ${nf(c)} per metre, lasts about {l} years.' for n, c, l in pick))
    parts = [
        lambda r: ('Calculate the total cost of each option.', '; '.join(f'{n}: ${dp(t, 2)} million' for n, _, _, t, _ in rows), 'cost per metre × length for each [2]'),
        lambda r: ('Calculate the cost per year of life for each option and identify the cheapest per year.', '; '.join(f'{n}: ${dp(y, 3)} million/yr' for n, _, _, _, y in rows) + f'. Cheapest: {cheapest[0]}.', '1 mark total ÷ life; 1 mark correct choice [2]'),
        lambda r: ('Is the scheme worth paying for? Use the figures to support your answer.', f'Every option costs much less than the ${value} million of property protected (most expensive ${dp(max(x[3] for x in rows), 2)} million), so protection is justified economically.' if max(x[3] for x in rows) < value else 'Some options cost more than the value of property protected, so they cannot be justified economically.', '1 mark judgement; 1 mark data [2]'),
        lambda r: ('Suggest one disadvantage of each option other than cost.', 'Sea wall: reflects waves and lowers beach, ugly. Rock armour: hard to walk on, unnatural. Groynes: starve beaches downdrift. Beach nourishment: sand washed away, needs repeating, dredging harms sea bed.', '1 mark each up to [3]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


CHAPTERS[4] = [c4a, c4b, c4c, c4d, c4e]


# ============================================================== CHAPTER 5: Weather and climate

c5a = T('Measuring weather: the weather station and instruments', 'weather station instruments')
build(c5a, {
    'terms': [
        ('Stevenson screen', 'a white wooden box with louvred sides, on legs about 1.2 m above grass, that houses thermometers and a hygrometer'),
        ('maximum-minimum thermometer', 'an instrument that records the highest and lowest temperatures since it was last reset'),
        ('rain gauge', 'a container that collects precipitation so that it can be measured in millimetres'),
        ('anemometer', 'an instrument with rotating cups that measures wind speed'),
        ('wind vane', 'an instrument that shows the direction from which the wind is blowing'),
        ('barometer', 'an instrument that measures air pressure, usually in millibars or hectopascals'),
        ('hygrometer', 'an instrument with wet and dry bulb thermometers used to find relative humidity'),
        ('relative humidity', 'the amount of water vapour in the air as a percentage of the maximum it could hold at that temperature'),
        ('sunshine recorder', 'an instrument, such as a glass sphere that burns a card, that records hours of sunshine'),
        ('okta', 'a unit of cloud cover, measured in eighths of the sky covered'),
    ],
    'mcq': [
        ('Why is a Stevenson screen painted white?', 'To reflect the Sun’s rays so the thermometers measure air temperature, not direct sunshine', ['To make it easy to find', 'To absorb heat', 'To keep rain out'], '[1]'),
        ('Why is a rain gauge sunk into the ground with its rim about 30 cm above the surface?', 'To stop it being knocked over and to prevent rain splashing in from the ground', ['To keep it warm', 'To measure wind speed', 'To catch more sunlight'], '[1]'),
        ('Wind direction is recorded as', 'the direction the wind is blowing from', ['the direction the wind is blowing towards', 'the speed of the wind', 'the temperature of the wind'], '[1]'),
        ('If the wet bulb and dry bulb thermometers show the same temperature, the relative humidity is', '100%', ['0%', '50%', 'impossible to tell'], 'No evaporation from the wet bulb = air saturated. [1]'),
        ('Air pressure is measured in', 'millibars (hectopascals)', ['millimetres', 'oktas', 'knots'], '[1]'),
        ('Which instrument measures wind speed?', 'Anemometer', ['Wind vane', 'Barometer', 'Hygrometer'], '[1]'),
    ],
    'explain': [
        ('Explain why the Stevenson screen has louvred sides and stands on legs about 1.2 m above grass.', 'Louvres let air circulate freely while keeping out direct sun and rain; standing above grass avoids heat radiated from the ground, giving a standard air temperature.', '1 mark louvres; 1 mark height/grass [2]'),
        ('Describe how a maximum-minimum thermometer is used.', 'Read the bottom of each metal index: the maximum on the right-hand scale and the minimum on the left-hand scale; reset the indices with a magnet each day at the same time.', '1 mark reading indices; 1 mark reset daily [2]'),
        ('Explain how a hygrometer shows relative humidity.', 'Water evaporates from the muslin on the wet bulb, cooling it; the drier the air, the more evaporation and the bigger the difference between wet and dry bulb readings; tables convert the difference into relative humidity.', '1 mark evaporation cools wet bulb; 1 mark bigger difference = lower humidity [2]'),
        ('Explain how to site a weather station so that readings are accurate.', 'In an open area away from buildings and trees (which shelter instruments or cast shadows), on grass not tarmac, with instruments at standard heights; read at the same time each day.', '1 mark open site; 1 mark standard surface/height/time [2]'),
        ('Explain how changes in air pressure help forecast the weather.', 'Falling pressure usually means a depression with cloud, wind and rain is approaching; rising or high pressure usually brings settled, dry weather.', '1 mark falling = unsettled; 1 mark high = settled [2]'),
    ],
    'claims': [
        ('A thermometer should be placed in direct sunlight to measure air temperature accurately.', False, 'Direct sun heats the thermometer itself; it must be shaded in a Stevenson screen.'),
        ('A wind vane points in the direction the wind is blowing from.', True, 'The arrow points into the wind, and wind is named by its origin.'),
        ('A rain gauge should be placed under a tree to protect it.', False, 'Trees intercept rain and drip unevenly, so readings would be inaccurate; place it in the open.'),
    ],
    'cases': [
        (['Fig. 5.1 is a description of a school weather station. A white box with louvred sides stands on legs on the school field; a cylinder sunk into the ground has a funnel at the top; a pole 10 m high carries a set of three rotating cups and an arrow; a glass sphere sits on a stand facing south.',
          'Study Fig. 5.1, which describes the instruments at a weather station. Instrument A is a wooden box on legs; instrument B is a cylinder with a funnel; instrument C has three spinning cups on a tall mast; instrument D is an arrow that turns on a pole; instrument E is a glass ball above a strip of card.'],
         [('Name the instruments that measure wind speed and wind direction.', 'Anemometer (rotating cups) and wind vane (arrow).', '1 mark each [2]'),
          ('Name the white box and two instruments it contains.', 'Stevenson screen; any two: maximum-minimum thermometer, wet and dry bulb thermometers (hygrometer), barometer.', '1 mark name; 1 mark two instruments [2]'),
          ('Describe how precipitation is measured with the cylinder.', 'Rain falls into the funnel and collects in a container; each day at the same time it is poured into a measuring cylinder and read in mm; then emptied.', '1 mark collection; 1 mark measuring and emptying [2]'),
          ('Explain why the anemometer is mounted on a tall mast.', 'Above buildings and trees the wind is not sheltered or deflected, so readings are accurate and comparable.', '[2]'),
          ('Name the instrument that measures sunshine and explain how it works.', 'Sunshine recorder (Campbell-Stokes): the glass sphere focuses sunlight and burns a line on a card; the length of the burn gives hours of sunshine.', '1 mark name; 1 mark how it works [2]')]),
    ],
})


@c5a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5a_week(r, D):
    c = city(r)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][:r.choice([5, 7])]
    mx = [r.randint(18, 34) for _ in days]
    mn = [x - r.randint(4, 14) for x in mx]
    rain = [r.choice([0, 0, 0, 1, 3, 6, 12, 22]) for _ in days]
    stem = f'A school weather station in {c} recorded the following data. ' + ' '.join(f'{d}: max {a} °C, min {b} °C, rain {p} mm.' for d, a, b, p in zip(days, mx, mn, rain))
    ranges = [a - b for a, b in zip(mx, mn)]
    i = ranges.index(max(ranges))
    if D == 1:
        opts, a = mcq(r, days[i], [d for d in days if d != days[i]])
        return {'stem': stem + ' On which day was the daily (diurnal) temperature range greatest?', 'options': opts, 'answer': a, 'key': f'{days[i]}: {mx[i]} − {mn[i]} = {ranges[i]} °C. [1]'}
    wet = [d for d, p in zip(days, rain) if p > 0]
    parts = [
        lambda r: ('Calculate the mean maximum temperature.', f'{dp(mean(mx))} °C', f'{sum(mx)} ÷ {len(days)} = {dp(mean(mx))} °C [2]'),
        lambda r: ('Identify the day with the largest diurnal temperature range and state the range.', f'{days[i]}, {ranges[i]} °C', f'{mx[i]} − {mn[i]} [2]'),
        lambda r: ('Calculate the total rainfall.', f'{sum(rain)} mm', f'{"+".join(map(str, rain))} = {sum(rain)} mm [1]'),
        lambda r: ('Suggest why the diurnal range is often smaller on cloudy, wet days.', 'Cloud reflects incoming sunlight by day (cooler maximum) and traps outgoing heat at night (warmer minimum).', '1 mark day; 1 mark night [2]'),
        lambda r: ('Name the instrument used to record the maximum and minimum temperatures and state where it should be kept.', 'A maximum-minimum (Six’s) thermometer, kept in a Stevenson screen.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c5a.add('C3', (1, 2, 3), 'numerical')
def c5a_hum(r, D):
    dry = r.randint(14, 32)
    diff = r.choice([0, 1, 2, 3, 5, 7, 9])
    wet = dry - diff
    other = r.choice([d for d in [0, 1, 2, 3, 5, 7, 9] if d != diff])
    stem = f'At 09:00 the dry bulb thermometer read {dry} °C and the wet bulb read {wet} °C. On the next day the dry bulb read {dry} °C and the wet bulb {dry - other} °C.'
    higher = 'the first day' if diff < other else 'the second day'
    if D == 1:
        opts, a = mcq(r, cap(higher), ['The first day' if higher != 'the first day' else 'The second day', 'Both days were the same', 'It cannot be worked out from these readings'])
        return {'stem': stem + ' On which day was the relative humidity higher?', 'options': opts, 'answer': a, 'key': 'Smaller wet-dry difference = less evaporation = higher humidity. [1]'}
    return {'stem': stem + ' (a) Calculate the wet-bulb depression on each day. (b) State which day had higher relative humidity and explain why.',
            'answer': f'(a) {diff} °C and {other} °C (b) {cap(higher)}: the smaller difference means less evaporation from the wet bulb because the air was closer to saturation.',
            'key': '(a) 1 mark both differences. (b) 1 mark correct day; 1 mark explanation of evaporation/cooling. Total [3]', 'marks': 3}


# --------------------------------------------------------------- 5.2 interpreting weather data
c5b = T('Interpreting weather data and drawing weather graphs', 'interpreting weather data weather graphs')
build(c5b, {
    'terms': [
        ('weather', 'the day-to-day condition of the atmosphere at a place, such as temperature, precipitation and wind'),
        ('climate', 'the average weather conditions of a place measured over a long period, usually 30 years'),
        ('wind rose', 'a diagram showing how often the wind blows from each direction at a place over a period'),
        ('diurnal temperature range', 'the difference between the highest and lowest temperatures in a 24-hour period'),
        ('annual temperature range', 'the difference between the mean temperatures of the hottest and coldest months'),
        ('isobar', 'a line on a weather map joining places of equal air pressure'),
        ('convectional rainfall', 'rain formed when the ground heats the air above it, which rises, cools and condenses'),
        ('relief rainfall', 'rain formed when moist air is forced to rise over high land and cools'),
        ('rain shadow', 'an area on the sheltered (leeward) side of mountains that receives little rain because the air descends and warms'),
    ],
    'mcq': [
        ('On a climate graph, temperature is usually shown as', 'a line graph', ['bars', 'a pie chart', 'a wind rose'], 'Temperature = line; precipitation = bars. [1]'),
        ('On a wind rose, the longest arm points towards', 'the direction from which the wind most often blows', ['the direction the wind blows to', 'the strongest wind ever recorded', 'north always'], '[1]'),
        ('Isobars that are close together on a weather map show', 'strong winds', ['calm weather', 'high temperatures', 'heavy snow only'], '[1]'),
        ('Which type of rainfall is common on the windward side of mountains?', 'Relief rainfall', ['Convectional rainfall only', 'Frontal rainfall only', 'No rainfall'], '[1]'),
    ],
    'explain': [
        ('Explain the difference between weather and climate.', 'Weather is the short-term (day-to-day) state of the atmosphere; climate is the average of weather over about 30 years.', '1 mark each [2]'),
        ('Explain how relief rainfall forms.', 'Moist air from the sea is forced to rise over mountains; it cools as it rises, water vapour condenses to form cloud and rain falls on the windward side; air descends and warms on the leeward side, forming a rain shadow.', '1 mark forced ascent; 1 mark cooling/condensation; 1 mark rain shadow [3]'),
        ('Explain how convectional rainfall forms.', 'The Sun heats the ground, which heats the air above; warm air rises, cools, and water vapour condenses to form cumulonimbus clouds and heavy afternoon rain.', '1 mark heating and rising; 1 mark cooling/condensation [2]'),
        ('Explain why bar graphs are used for rainfall and line graphs for temperature.', 'Rainfall is a total for each separate period (discrete), while temperature changes continuously.', '1 mark each [2]'),
    ],
    'claims': [
        ('Climate can be found from one week of weather readings.', False, 'Climate is the long-term average (about 30 years); one week shows only weather.'),
        ('A rain shadow forms on the leeward side of mountains.', True, 'Air that has lost moisture on the windward side descends and warms, so little rain falls.'),
        ('Clear skies at night usually give lower minimum temperatures.', True, 'Without cloud, heat radiated from the ground escapes into space.'),
    ],
})


@c5b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5b_rose(r, D):
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    days = r.choice([30, 31])
    counts = [r.randint(0, 3) for _ in dirs]
    big = r.randrange(8)
    counts[big] += r.randint(6, 10)
    calm = days - sum(counts)
    if calm < 0:
        return None
    c = city(r)
    stem = f'A wind rose for {c} shows the number of days in one month on which the wind blew from each direction: ' + ', '.join(f'{d} {n}' for d, n in zip(dirs, counts)) + f'. There were {calm} calm days.'
    pc = counts[big] / days * 100
    if D == 1:
        opts, a = mcq(r, dirs[big], [d for d in dirs if d != dirs[big]])
        return {'stem': stem + ' What was the prevailing wind direction?', 'options': opts, 'answer': a, 'key': f'{dirs[big]} ({counts[big]} days). [1]'}
    opp = dirs[(big + 4) % 8]
    side = r.choice([dirs[big], opp])
    parts = [
        lambda r: ('State the prevailing wind direction.', dirs[big], '[1]'),
        lambda r: ('Calculate the percentage of days with wind from the prevailing direction.', f'{dp(pc)}%', f'{counts[big]} ÷ {days} × 100 = {dp(pc)}% [2]'),
        lambda r: (f'Check that the data total {days} days.', f'{sum(counts)} + {calm} calm = {days}', f'{"+".join(map(str, counts))} = {sum(counts)}; + {calm} = {days} [1]'),
        lambda r: (f'A factory is to be built on the {side} side of a town. Explain whether smoke from the factory is likely to affect the town.',
                   (f'Yes, often: the prevailing wind blows from the {dirs[big]}, so smoke from a factory on the {side} side would be carried across the town.' if side == dirs[big] else
                    f'Rarely: the prevailing wind blows from the {dirs[big]} towards the {opp}, so smoke from a factory on the {opp} side is carried away from the town.'),
                   '1 mark use of prevailing wind; 1 mark judgement [2]'),
        lambda r: ('Explain why the anemometer and wind vane should be placed in an open area.', 'Buildings and trees shelter or deflect the wind, giving false speeds and directions.', '[1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c5b.add('C3', (2, 3, 4, 5), 'numerical')
def c5b_press(r, D):
    days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6']
    p0 = r.randint(1018, 1030)
    falls = [r.randint(3, 9) for _ in range(3)]
    ps = [p0]
    for f in falls:
        ps.append(ps[-1] - f)
    for _ in range(2):
        ps.append(ps[-1] + r.randint(4, 10))
    rain = [0, r.choice([0, 1]), r.randint(4, 10), r.randint(12, 30), r.randint(2, 8), 0]
    cloud = [r.randint(0, 2), r.randint(2, 4), r.randint(5, 7), 8, r.randint(4, 6), r.randint(1, 3)]
    stem = 'Table 5.1 shows weather readings at 09:00 for six days. ' + ' '.join(f'{d}: pressure {p} mb, rain {x} mm, cloud {c} oktas.' for d, p, x, c in zip(days, ps, rain, cloud))
    lo = ps.index(min(ps))
    parts = [
        lambda r: ('Describe the changes in air pressure over the six days.', f'Pressure fell from {ps[0]} mb to a low of {min(ps)} mb on {days[lo]}, then rose to {ps[-1]} mb.', '1 mark fall then rise; 1 mark data [2]'),
        lambda r: ('Describe the relationship between pressure and rainfall.', 'As pressure falls, rainfall and cloud cover increase; the heaviest rain occurs at the lowest pressure; rain stops as pressure rises.', '1 mark relationship; 1 mark data [2]'),
        lambda r: ('Calculate the range of air pressure.', f'{max(ps) - min(ps)} mb', f'{max(ps)} − {min(ps)} [1]'),
        lambda r: ('Explain why low pressure is associated with cloud and rain.', 'In low pressure air rises; as it rises it cools, water vapour condenses into cloud and precipitation forms.', '1 mark rising air; 1 mark cooling/condensation [2]'),
        lambda r: ('Suggest a suitable graph to show pressure and rainfall together.', 'A combined graph: rainfall as bars and pressure as a line on a second vertical axis, with days on the horizontal axis.', '1 mark bars + line; 1 mark two axes [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- climate data
CLIM = {
    'Manaus, Brazil (3° S)': ('equatorial', [26.1, 26.0, 26.1, 26.3, 26.5, 26.6, 26.8, 27.5, 27.9, 27.7, 27.3, 26.7], [260, 290, 310, 290, 230, 110, 85, 60, 80, 110, 170, 220]),
    'Singapore (1° N)': ('equatorial', [26.5, 27.1, 27.6, 28.0, 28.3, 28.3, 27.9, 27.9, 27.6, 27.6, 27.0, 26.5], [240, 160, 180, 170, 170, 140, 150, 150, 140, 160, 250, 290]),
    'Kisangani, DR Congo (0.5° N)': ('equatorial', [25.4, 25.7, 25.8, 25.8, 25.6, 25.0, 24.3, 24.4, 24.8, 25.0, 25.1, 25.0], [80, 110, 160, 170, 160, 110, 120, 160, 180, 220, 190, 110]),
    'Iquitos, Peru (4° S)': ('equatorial', [26.8, 26.7, 26.5, 26.3, 26.0, 25.6, 25.4, 26.1, 26.6, 26.9, 27.0, 26.9], [260, 250, 300, 300, 260, 190, 170, 170, 210, 250, 270, 270]),
    'Riyadh, Saudi Arabia (25° N)': ('hot desert', [14.6, 17.1, 21.4, 26.8, 32.4, 35.0, 36.1, 35.8, 32.9, 27.4, 20.6, 15.8], [15, 8, 25, 30, 10, 0, 0, 0, 0, 2, 10, 15]),
    'Aswan, Egypt (24° N)': ('hot desert', [16.0, 17.9, 22.0, 26.9, 30.8, 33.0, 33.4, 33.0, 31.4, 28.1, 22.4, 17.6], [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0]),
    'In Salah, Algeria (27° N)': ('hot desert', [13.0, 16.0, 20.5, 25.0, 30.0, 35.0, 37.0, 36.0, 32.5, 26.0, 19.0, 14.0], [2, 1, 1, 1, 1, 0, 0, 1, 1, 1, 3, 4]),
    'Oodnadatta, Australia (27.5° S)': ('hot desert', [29.5, 29.0, 26.0, 21.0, 16.5, 13.0, 12.5, 14.5, 18.5, 22.5, 25.5, 28.0], [20, 20, 15, 10, 12, 10, 8, 7, 8, 15, 15, 20]),
}


def clim(r, kind):
    name = r.choice([k for k, v in CLIM.items() if v[0] == kind])
    _, tt, pp = CLIM[name]
    return name, list(tt), list(pp)


def clim_text(tt, pp):
    return ('Temperature (°C): ' + ', '.join(f'{m} {fmt(x, 1)}' for m, x in zip(MON, tt)) + '. Precipitation (mm): ' + ', '.join(f'{m} {p}' for m, p in zip(MON, pp)) + '.')


def clim_fig(r, kind, D, extra_parts):
    name, tt, pp = clim(r, kind)
    hi, lo = max(tt), min(tt)
    rng = round(hi - lo, 1)
    tot = sum(pp)
    wet = MONTHS[pp.index(max(pp))]
    hot = MONTHS[tt.index(hi)]
    stem = f'Fig. 5.2 is a climate graph for {name}. ' + clim_text(tt, pp)
    if D == 1:
        opts, a = mcq(r, f'{fmt(rng, 1)} °C', [f'{fmt(hi, 1)} °C', f'{fmt(round(mean(tt), 1), 1)} °C', f'{fmt(round(rng + 2, 1), 1)} °C', f'{fmt(lo, 1)} °C'])
        return {'stem': stem + ' What is the annual temperature range?', 'options': opts, 'answer': a, 'key': f'{fmt(hi, 1)} − {fmt(lo, 1)} = {fmt(rng, 1)} °C. [1]'}
    base = [
        lambda r: ('Calculate the annual temperature range.', f'{fmt(rng, 1)} °C', f'{fmt(hi, 1)} ({hot}) − {fmt(lo, 1)} = {fmt(rng, 1)} °C [1]'),
        lambda r: ('Calculate the total annual precipitation.', f'{tot} mm', f'sum of 12 months = {tot} mm [1]'),
        (lambda r: ('Identify the wettest month and its rainfall.', f'{wet}, {max(pp)} mm', '[1]')) if pp.count(max(pp)) == 1 else (lambda r: None),
        lambda r: ('Calculate the mean annual temperature.', f'{dp(mean(tt))} °C', f'{dp(sum(tt), 1)} ÷ 12 = {dp(mean(tt))} °C [1]'),
    ]
    return compose(r, stem, base + [(lambda r, p=p: p(name, tt, pp)) for p in extra_parts], k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c5c = T('Characteristics and causes of the equatorial climate', 'equatorial climate')
build(c5c, {
    'terms': [
        ('equatorial climate', 'a climate found within about 5° of the Equator with high temperatures all year, a very small annual range and heavy rainfall in all months'),
        ('insolation', 'incoming solar radiation reaching the Earth’s surface'),
        ('Inter-Tropical Convergence Zone (ITCZ)', 'the zone of low pressure near the Equator where the trade winds meet, air rises and heavy rain falls'),
        ('cumulonimbus cloud', 'a tall, dark storm cloud formed by strong rising air, bringing thunderstorms and heavy rain'),
        ('trade winds', 'steady winds blowing from the subtropical high-pressure belts towards the Equator'),
        ('humidity', 'the amount of water vapour in the air'),
        ('zenith', 'the position of the Sun directly overhead at midday'),
    ],
    'mcq': [
        ('Which best describes the annual temperature range in an equatorial climate?', 'Very small, about 1-3 °C', ['Very large, over 30 °C', 'About 15 °C', 'Zero, every day is identical'], '[1]'),
        ('Why is it hot all year in equatorial regions?', 'The Sun is always high in the sky, so insolation is concentrated on a small area', ['They are closer to the Sun', 'Ocean currents are always warm', 'There are no clouds'], '[1]'),
        ('At what time of day does rain usually fall in an equatorial climate?', 'Afternoon, in convectional thunderstorms', ['Early morning only', 'Midnight only', 'It never rains'], '[1]'),
        ('Total annual rainfall in an equatorial climate is usually', 'over 2000 mm', ['under 250 mm', 'about 500 mm', 'about 50 mm'], '[1]'),
    ],
    'explain': [
        ('Explain why temperatures are high throughout the year near the Equator.', 'The midday Sun is overhead or nearly overhead all year, so insolation is concentrated and passes through less atmosphere; day length is about 12 hours all year.', '1 mark high Sun angle; 1 mark less atmosphere/constant day length [2]'),
        ('Explain why equatorial regions have heavy rainfall.', 'Intense heating causes convection: hot, moist air rises, cools and condenses into cumulonimbus clouds; the trade winds converge at the ITCZ, forcing more air upwards; high evapotranspiration from the forest supplies moisture.', '1 mark heating and rising; 1 mark condensation; 1 mark ITCZ/moisture [3]'),
        ('Describe a typical day in an equatorial climate.', 'Clear, sunny morning and rising temperatures and humidity; cumulus clouds grow into cumulonimbus by midday; heavy thunderstorms in mid-afternoon; clear, warm evening.', '1 mark morning; 1 mark afternoon storm; 1 mark evening [3]'),
        ('Explain why there is little seasonal change in an equatorial climate.', 'Sun angle and day length change very little through the year, so temperatures stay high and convection gives rain in every month.', '1 mark each [2]'),
    ],
    'claims': [
        ('Equatorial regions are hot because they are nearer to the Sun.', False, 'The difference in distance is tiny; it is the high angle of the Sun that concentrates insolation.'),
        ('The ITCZ is a zone of low pressure with rising air.', True, 'Trade winds converge, air rises and heavy convectional rain falls.'),
        ('The diurnal temperature range in equatorial areas is often larger than the annual range.', True, 'Days may vary by 8-10 °C between day and night, while monthly means vary by only 1-3 °C.'),
    ],
    'essays': [
        ('the high angle of the Sun is the only reason for the climate of equatorial regions',
         ['The high Sun gives intense insolation and high temperatures all year, driving convection.'],
         ['Convergence of trade winds at the ITCZ forces air to rise.', 'High evapotranspiration from rainforests recycles moisture.', 'Maritime air from nearby oceans adds moisture.'],
         'The Sun’s angle is the main cause, but air pressure, winds and vegetation are needed to explain the heavy, all-year rainfall.',
         ['insolation', 'ITCZ', 'evapotranspiration', 'convection']),
    ],
})


def _eq_extra(name, tt, pp):
    return ('Describe the main features of the climate shown in Fig. 5.2.', f'Hot all year ({fmt(min(tt), 1)}-{fmt(max(tt), 1)} °C) with a very small annual range of {fmt(round(max(tt) - min(tt), 1), 1)} °C; heavy rain ({sum(pp)} mm a year) with rain in every month, wettest in ' + ' and '.join(MONTHS[i] for i in range(12) if pp[i] == max(pp)) + '.',
            '1 mark temperature with data; 1 mark range; 1 mark rainfall total/distribution [3]')


def _eq_cause(name, tt, pp):
    return ('Explain why this place has rainfall in every month.', 'High temperatures all year cause convection: hot, humid air rises, cools and condenses, giving afternoon thunderstorms; it lies near the ITCZ where trade winds converge.', '1 mark convection; 1 mark condensation; 1 mark ITCZ [3]')


def _eq_drier(name, tt, pp):
    if pp.count(min(pp)) > 1:
        return None
    dry = MONTHS[pp.index(min(pp))]
    return (f'Suggest why {dry} is the driest month.', 'The ITCZ moves north or south with the overhead Sun, so for a few months the place is further from the zone of strongest rising air and receives less convectional rain.', '1 mark ITCZ movement; 1 mark less rising air [2]')


@c5c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5c_fig(r, D):
    return clim_fig(r, 'equatorial', D, [_eq_extra, _eq_cause, _eq_drier])


@c5c.add('C2', (2, 3, 4), 'explain')
def c5c_compare(r, D):
    e, te, pe = clim(r, 'equatorial')
    d, td, pd = clim(r, 'hot desert')
    re_, rd = round(max(te) - min(te), 1), round(max(td) - min(td), 1)
    return {'stem': f'{e} has an annual temperature range of {fmt(re_, 1)} °C and {sum(pe)} mm of rain a year. {d} has an annual range of {fmt(rd, 1)} °C and {sum(pd)} mm of rain. Compare the two climates and explain one reason for the difference in rainfall.',
            'answer': f'{e} is hot all year with a much smaller range ({fmt(re_, 1)} °C v {fmt(rd, 1)} °C) and far more rain ({sum(pe)} mm v {sum(pd)} mm). Rising air at the ITCZ gives convectional rain at the Equator, whereas descending air in the subtropical high-pressure belt stops clouds forming in the desert.',
            'key': '1 mark temperature comparison with data; 1 mark rainfall comparison with data; 1 mark explanation (rising v sinking air) [3]', 'marks': 3, 'type': 'explain'}


# --------------------------------------------------------------- 5.4 hot desert climate
c5d = T('Characteristics and causes of the hot desert climate', 'hot desert climate')
build(c5d, {
    'terms': [
        ('hot desert', 'an area with less than 250 mm of precipitation a year and high temperatures, especially in summer'),
        ('subtropical high pressure', 'a belt of sinking air at about 20-30° north and south of the Equator that gives clear skies and very little rain'),
        ('cold ocean current', 'a current of cold water flowing towards the Equator along a coast, which cools the air and reduces rainfall'),
        ('continentality', 'the effect of being far from the sea, which gives dry air and large temperature ranges'),
        ('Hadley cell', 'the circulation in which air rises at the Equator, moves towards the poles and sinks at about 30° latitude'),
        ('diurnal range', 'the difference between the highest daytime and lowest night-time temperatures'),
        ('offshore wind', 'a wind blowing from the land towards the sea, which carries little moisture'),
    ],
    'mcq': [
        ('Why do hot deserts have very large diurnal temperature ranges?', 'Clear skies let strong sunshine in by day and heat escape at night', ['They are near the sea', 'It rains every night', 'Cloud cover is very thick'], '[1]'),
        ('Most hot deserts lie at about which latitude?', '20-30° north and south of the Equator', ['On the Equator', '50-60° north', 'Within the Arctic Circle'], '[1]'),
        ('The Atacama and Namib deserts are very dry partly because of', 'cold ocean currents offshore', ['warm ocean currents', 'the ITCZ', 'monsoon winds'], 'The Humboldt (Peru) and Benguela currents. [1]'),
        ('Annual rainfall in a hot desert is usually less than', '250 mm', ['2000 mm', '1000 mm', '750 mm'], '[1]'),
    ],
    'explain': [
        ('Explain why there is very little rain in hot deserts.', 'Air sinks in the subtropical high-pressure belt (the descending limb of the Hadley cell); sinking air warms and dries, so clouds cannot form; winds are often offshore and dry; some deserts are far from the sea or in rain shadows.', '1 mark sinking air; 1 mark warms/no condensation; 1 mark other factor [3]'),
        ('Explain how a cold ocean current can create a coastal desert.', 'The cold current cools the air above it, so the air cannot hold much moisture and is stable; fog forms over the sea but rain clouds do not develop, e.g. the Namib (Benguela current).', '1 mark cools air; 1 mark stable/little moisture [2]'),
        ('Explain why hot deserts are hotter in summer than equatorial areas.', 'With no cloud cover, intense sunshine reaches the ground; the high summer Sun at about 25° latitude and long days cause very high temperatures; bare ground heats quickly.', '1 mark clear skies; 1 mark summer Sun/long days [2]'),
        ('Explain why temperatures can fall below 5 °C at night in a hot desert.', 'Clear skies and dry air let heat radiated from the ground escape quickly into space; there is no cloud blanket.', '1 mark clear skies; 1 mark heat escapes [2]'),
    ],
    'claims': [
        ('Hot deserts are hot all year round.', False, 'Winters can be cool and nights cold; e.g. Riyadh averages about 15 °C in January.'),
        ('Sinking air is a major cause of hot deserts.', True, 'Air sinking in the subtropical high warms and dries, preventing cloud formation.'),
        ('All deserts are sandy.', False, 'Many are rocky or stony (reg and hamada); sand seas (ergs) cover only part of the Sahara.'),
    ],
    'essays': [
        ('subtropical high pressure is the most important cause of hot desert climates',
         ['Most hot deserts (Sahara, Arabian, Kalahari, Australian) lie at 20-30° under sinking air.'],
         ['Cold ocean currents cause coastal deserts such as the Atacama and Namib.', 'Rain shadows and continentality add dryness, e.g. the Gobi (cold desert) and parts of Australia.'],
         'Subtropical high pressure is the main cause for most hot deserts, but local factors explain why some are especially dry.',
         ['Hadley cell', 'ocean currents', 'rain shadow', 'continentality']),
    ],
})


def _de_extra(name, tt, pp):
    return ('Describe the main features of the climate shown in Fig. 5.2.', f'Very little rain ({sum(pp)} mm a year), with several months completely dry or almost dry; hot summers up to {fmt(max(tt), 1)} °C ({MONTHS[tt.index(max(tt))]}) and mild winters ({fmt(min(tt), 1)} °C); a large annual range of {fmt(round(max(tt) - min(tt), 1), 1)} °C.',
            '1 mark rainfall with data; 1 mark temperatures; 1 mark range [3]')


def _de_cause(name, tt, pp):
    return ('Explain why the place shown in Fig. 5.2 receives so little rain.', 'It lies at about 20-30° latitude under the subtropical high-pressure belt, where air sinks, warms and dries so clouds rarely form; winds are dry and offshore or it lies far from the sea.', '1 mark location/high pressure; 1 mark sinking air; 1 mark no condensation [3]')


def _de_hemi(name, tt, pp):
    s = 'S' in name.split('(')[1]
    return ('State which hemisphere this place is in. Use evidence from Fig. 5.2.', ('Southern: the hottest months are December to February.' if s else 'Northern: the hottest months are June to August.'), '1 mark hemisphere; 1 mark evidence [2]')


@c5d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c5d_fig(r, D):
    return clim_fig(r, 'hot desert', D, [_de_extra, _de_cause, _de_hemi])


@c5d.add('C3', (2, 3, 4), 'numerical')
def c5d_diurnal(r, D):
    place = r.choice(['In Salah, Algeria', 'Riyadh, Saudi Arabia', 'Aswan, Egypt', 'a weather station in the Sahara', 'a station in the Thar Desert, India'])
    hrs = ['03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', '24:00']
    lo = r.randint(6, 18)
    hi = lo + r.randint(16, 25)
    t = [lo + 2, lo, lo + (hi - lo) // 3, hi - 3, hi, hi - (hi - lo) // 3, lo + (hi - lo) // 4, lo + 3]
    stem = f'Fig. 5.3 shows air temperatures recorded over 24 hours in July at {place}: ' + ', '.join(f'{h} {x} °C' for h, x in zip(hrs, t)) + '. The sky was cloudless.'
    parts = [
        lambda r: ('Calculate the diurnal temperature range.', f'{hi - lo} °C', f'{hi} − {lo} = {hi - lo} °C [1]'),
        lambda r: ('State the times of the highest and lowest temperatures.', f'Highest at 15:00 ({hi} °C); lowest at 06:00 ({lo} °C).', '1 mark each [2]'),
        lambda r: ('Explain why the temperature range is so large.', 'Cloudless skies let intense sunshine heat the bare ground by day; at night heat radiates quickly to space because there is no cloud or water vapour to trap it.', '1 mark day; 1 mark night [2]'),
        lambda r: ('Explain why the highest temperature occurs in the afternoon rather than at noon.', 'The ground keeps absorbing more heat than it loses until mid-afternoon, and heats the air above it after a delay.', '[2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


CHAPTERS[5] = [c5a, c5b, c5c, c5d]


# ============================================================== CHAPTER 6: Ecosystems

c6a = T('Ecosystems, food webs and nutrient cycling in the tropical rainforest', 'ecosystems food webs nutrient cycling')
build(c6a, {
    'terms': [
        ('ecosystem', 'a community of plants and animals interacting with each other and with the non-living environment (climate, soil, water)'),
        ('producer', 'an organism, such as a green plant, that makes its own food by photosynthesis'),
        ('consumer', 'an organism that gets its energy by eating other organisms'),
        ('decomposer', 'an organism, such as a fungus or bacterium, that breaks down dead material and releases nutrients'),
        ('food web', 'a diagram showing the many linked food chains in an ecosystem'),
        ('biomass', 'the total mass of living material in an area'),
        ('nutrient cycle', 'the movement of nutrients between the biomass, the litter and the soil'),
        ('leaf litter', 'the layer of fallen leaves and dead plant material on the forest floor'),
        ('emergent', 'a very tall tree, up to about 50 m, that grows above the main rainforest canopy'),
        ('canopy', 'the dense, continuous layer of tree crowns about 30 m above the rainforest floor'),
        ('biodiversity', 'the variety of different species of plants and animals in an area'),
    ],
    'mcq': [
        ('In the tropical rainforest, where are most nutrients stored?', 'In the biomass (living plants)', ['In the soil', 'In the leaf litter', 'In the rivers'], 'Rapid uptake means few remain in the soil. [1]'),
        ('Why does leaf litter decompose very quickly in the rainforest?', 'Hot, wet conditions all year suit decomposers', ['There are no decomposers', 'It is cold at night', 'The litter is very thick'], '[1]'),
        ('Which layer of the rainforest receives the least sunlight?', 'The forest floor', ['The emergents', 'The canopy', 'The upper part of the under-canopy'], 'Only about 2% of sunlight reaches the floor. [1]'),
        ('In a food web, a jaguar that eats tapirs and monkeys is a', 'top (tertiary) consumer', ['producer', 'decomposer', 'primary consumer'], '[1]'),
        ('Rainforest soils (latosols) are usually', 'infertile and red, because nutrients are leached and quickly taken up by plants', ['very fertile and black', 'frozen', 'salty and white'], '[1]'),
    ],
    'explain': [
        ('Explain why rainforest soils are infertile even though the vegetation is very dense.', 'Most nutrients are held in the biomass; heavy rain leaches nutrients down through the soil; dead material decomposes and is taken up again by shallow roots so quickly that few nutrients stay in the soil.', '1 mark biomass store; 1 mark leaching; 1 mark rapid recycling [3]'),
        ('Describe the structure (layers) of the tropical rainforest.', 'Emergents up to 50 m; a dense canopy at about 30 m; an under-canopy of smaller trees at about 15-20 m; a shrub layer; and a dark forest floor with little vegetation.', '1 mark for every two layers with heights up to [3]'),
        ('Explain what would happen to a food web if a top predator were removed.', 'Its prey (e.g. herbivores) would increase, over-grazing plants and reducing food for other species, which upsets the balance of the whole web.', '1 mark prey increase; 1 mark knock-on effect [2]'),
        ('Explain why the nutrient cycle is easily broken if the forest is cleared.', 'Without trees there is no new litter and no biomass store; heavy rain washes away and leaches the thin soil nutrients, so the soil becomes infertile within a few years.', '1 mark no litter/biomass; 1 mark leaching/erosion [2]'),
        ('Explain why the tropical rainforest has very high biodiversity.', 'Hot, wet conditions all year allow plants to grow continuously; many layers create many habitats and niches; the forest has existed for millions of years without glaciation.', '1 mark climate; 1 mark layers/habitats [2]'),
    ],
    'claims': [
        ('Rainforest soils are very fertile because the forest is so lush.', False, 'The soil is thin and leached; nutrients are stored in the vegetation and recycled quickly.'),
        ('Decomposers are important because they release nutrients back into the soil.', True, 'Fungi and bacteria break down litter so that plants can reuse the nutrients.'),
        ('Energy is recycled round a food chain like nutrients are.', False, 'Energy flows one way and is lost as heat at each level; nutrients are recycled.'),
    ],
    'cases': [
        (['Fig. 6.1 is a nutrient cycle diagram for a tropical rainforest drawn as three circles: biomass (large), litter (very small) and soil (small). Thick arrows show fast transfers from litter to soil (decomposition) and from soil to biomass (uptake by roots). An arrow from soil labelled “leaching” and an arrow from litter labelled “run-off” are also shown.',
          'Study Fig. 6.1, a Gersmehl nutrient cycle for the tropical rainforest. The biomass store is much larger than the litter and soil stores. Transfers from litter to soil and from soil to biomass are very large; losses occur by leaching and surface run-off.'],
         [('Name the largest nutrient store.', 'Biomass.', '[1]'),
          ('Explain why the litter store is very small.', 'Hot, wet conditions all year mean decomposers break litter down very quickly, so it does not build up.', '1 mark rapid decomposition; 1 mark climate reason [2]'),
          ('Explain why the transfer from soil to biomass is large.', 'Plants grow all year and their dense, shallow roots absorb nutrients as soon as they are released.', '[2]'),
          ('Describe how the nutrient cycle would change after the forest is cleared for farming.', 'Biomass store shrinks; litter input stops; leaching and run-off losses increase so soil store falls; crops remove nutrients when harvested.', '1 mark each up to [3]')]),
    ],
})


@c6a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6a_store(r, D):
    bio = r.choice([60, 65, 70, 75, 80])
    lit = r.choice([2, 3, 4, 5])
    soil = 100 - bio - lit
    other = r.choice([('a temperate deciduous forest', 45, 10), ('a coniferous (taiga) forest', 25, 50), ('a temperate grassland', 10, 5)])
    ob, ol = other[1], other[2]
    os_ = 100 - ob - ol
    stem = (f'Table 6.1 shows the percentage of nutrients stored in the biomass, litter and soil. Tropical rainforest: biomass {bio}%, litter {lit}%, soil ?. '
            f'{cap(other[0])}: biomass {ob}%, litter {ol}%, soil {os_}%.')
    if D == 1:
        opts, a = mcq(r, f'{soil}%', [f'{bio}%', f'{100 - soil}%', f'{soil + 10}%', f'{lit}%'])
        return {'stem': stem + ' What percentage is stored in the rainforest soil?', 'options': opts, 'answer': a, 'key': f'100 − {bio} − {lit} = {soil}%. [1]'}
    parts = [
        lambda r: ('Calculate the percentage stored in the rainforest soil.', f'{soil}%', f'100 − {bio} − {lit} = {soil}% [1]'),
        lambda r: (f'Compare the rainforest with {other[0]}.', f'The rainforest stores much more in biomass ({bio}% v {ob}%) and much less in litter ({lit}% v {ol}%)' + (f' and soil ({soil}% v {os_}%).' if soil < os_ else '.'), '1 mark comparison with data for two stores [2]'),
        lambda r: ('Explain why so little is stored in the rainforest litter.', 'Decomposition is very rapid in the hot, wet climate.', '[1]'),
        lambda r: ('The rainforest data are to be drawn as a pie chart. Calculate the angle of the biomass sector.', f'{fmt(bio * 3.6, 1)}°', f'{bio} × 3.6 = {fmt(bio * 3.6, 1)}° [1]'),
        lambda r: ('Suggest why farmers who clear rainforest find that yields fall after a few years.', 'Once the biomass is removed, nutrients are no longer recycled; heavy rain leaches the thin soil, so fertility falls quickly.', '1 mark loss of store; 1 mark leaching [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c6a.add('C2', (1, 2, 3, 4), 'explain')
def c6a_web(r, D):
    webs = [
        ('fig trees and fruit', ['toucans', 'spider monkeys'], 'harpy eagles', 'fungi'),
        ('leaves of canopy trees', ['leafcutter ants', 'sloths'], 'jaguars', 'termites'),
        ('nectar and flowers', ['hummingbirds', 'butterflies'], 'tree snakes', 'bacteria'),
        ('fallen fruit and seeds', ['agoutis', 'tapirs'], 'jaguars', 'fungi'),
    ]
    prod, prim, top, dec = r.choice(webs)
    stem = f'A simple rainforest food web: {prod} are eaten by {prim[0]} and {prim[1]}; both are eaten by {top}; {dec} break down dead material.'
    if D == 1:
        opts, a = mcq(r, cap(top), [cap(prim[0]), cap(prim[1]), cap(dec), cap(prod)])
        return {'stem': stem + ' Which organism is the top consumer?', 'options': opts, 'answer': a, 'key': f'{cap(top)}. [1]'}
    return {'stem': stem + f' (a) Identify a producer, a primary consumer and a decomposer. (b) Explain what might happen to the food web if the {prim[0]} were removed.',
            'answer': f'(a) Producer: {prod}; primary consumer: {prim[0]} or {prim[1]}; decomposer: {dec}. (b) The {top} would eat more {prim[1]}, whose numbers would fall; {prod} might increase; the balance of the web would change.',
            'key': '(a) 2 marks all three correct, 1 mark two correct. (b) 1 mark effect on predator/other prey; 1 mark effect on producers. Total [4]', 'marks': 4}


# --------------------------------------------------------------- 6.2 adaptations
ADAPT = [
    ('buttress roots', 'rainforest', 'large ridged roots above ground that support very tall trees in shallow soil'),
    ('drip-tip leaves', 'rainforest', 'pointed leaf tips that let heavy rain run off quickly, preventing rot and the growth of algae'),
    ('lianas', 'rainforest', 'woody climbing plants rooted in the ground that climb trees to reach sunlight in the canopy'),
    ('epiphytes', 'rainforest', 'plants that grow on branches high in the canopy to reach light, taking moisture and nutrients from the air and rain'),
    ('thin, smooth bark', 'rainforest', 'there is no need to protect against cold or water loss, and the smooth surface stops other plants climbing'),
    ('prehensile tails of spider monkeys', 'rainforest', 'a gripping tail used as a fifth limb to move through the canopy'),
    ('camouflage of the sloth', 'rainforest', 'algae growing in its fur make it green, hiding it from harpy eagles'),
    ('cacti with spines instead of leaves', 'hot desert', 'spines reduce the surface area for water loss by transpiration and deter animals'),
    ('a thick waxy cuticle', 'hot desert', 'a waxy coating on stems and leaves that reduces water loss'),
    ('long tap roots', 'hot desert', 'roots up to tens of metres deep that reach groundwater'),
    ('shallow, widespread roots', 'hot desert', 'roots that spread out near the surface to absorb rain quickly after a rare shower'),
    ('swollen water-storing stems', 'hot desert', 'stems such as those of cacti that store water for long dry periods'),
    ('seeds that stay dormant', 'hot desert', 'seeds that can survive for years and germinate quickly only after rain'),
    ('the camel’s hump of fat', 'hot desert', 'fat stored in the hump provides energy, and body fat is concentrated so heat escapes easily from the rest of the body'),
    ('the fennec fox’s large ears', 'hot desert', 'large ears radiate body heat and help it hear prey at night'),
    ('nocturnal behaviour of desert animals', 'hot desert', 'animals are active at night when it is cooler and spend the day in burrows'),
]

c6b = T('Adaptations of plants and animals in tropical rainforests and hot deserts', 'adaptations plants animals')
build(c6b, {
    'terms': [
        ('adaptation', 'a feature of a plant or animal that helps it survive in its environment'),
        ('xerophyte', 'a plant adapted to survive in very dry conditions'),
        ('transpiration', 'the loss of water vapour from plants through tiny pores (stomata) in their leaves'),
        ('nocturnal', 'active at night and resting during the day'),
        ('ephemeral plant', 'a plant with a very short life cycle that grows, flowers and sets seed quickly after rain'),
        ('stomata', 'tiny pores, mainly on leaves, through which plants exchange gases and lose water'),
    ],
    'explain': [
        ('Explain two ways in which plants are adapted to the high rainfall of the tropical rainforest.', 'Drip-tip leaves shed water quickly so leaves do not rot; waxy leaf surfaces repel water; buttress roots support trees in waterlogged, shallow soils.', '2 marks each developed adaptation [4]'),
        ('Explain two ways in which desert plants reduce water loss.', 'Small or no leaves (spines) reduce surface area for transpiration; thick waxy cuticle; stomata that open only at night; hairs that trap moist air.', '2 marks each developed adaptation [4]'),
        ('Explain how a camel is adapted to the hot desert.', 'Can drink about 100 litres at once and survive weeks without water; fat stored in the hump; long eyelashes and closing nostrils keep out sand; wide padded feet do not sink in sand.', '1 mark each up to [3]'),
        ('Compare the competition for resources faced by plants in the rainforest and in the desert.', 'In the rainforest plants compete mainly for light, so they grow tall or climb; in the desert they compete mainly for water, so roots are deep or widespread and plants are widely spaced.', '1 mark rainforest; 1 mark desert; 1 mark comparison [3]'),
    ],
    'claims': [
        ('Rainforest trees have deep roots to reach groundwater.', False, 'Most nutrients are near the surface, so roots are shallow; buttress roots give support.'),
        ('Some desert plants complete their life cycle within a few weeks after rain.', True, 'Ephemerals germinate, flower and set seed quickly, then survive as dormant seeds.'),
        ('Large ears help the fennec fox lose heat.', True, 'Blood vessels in the ears radiate heat away from the body.'),
    ],
    'essays': [
        ('plants in hot deserts face greater challenges than plants in tropical rainforests',
         ['Water shortage, extreme heat and poor soils limit growth; adaptations such as spines, waxy cuticles and dormancy are needed.'],
         ['Rainforest plants face intense competition for light, heavy rain and nutrient-poor leached soils.', 'Both environments need specialised adaptations.'],
         'Each environment has different but equally severe challenges; deserts limit growth more, but rainforests demand fierce competition.',
         ['water', 'light', 'soils', 'competition']),
    ],
})


@c6b.add('C1', (1, 2, 3), 'mcq')
def c6b_match(r, D):
    a, env, why = r.choice(ADAPT)
    others = [w for x, e, w in ADAPT if x != a]
    opts, ans = mcq(r, cap(why), [cap(w) for w in r.sample(others, 5)])
    return {'stem': f'Which statement explains how {a} help(s) survival in the {env}?', 'options': opts, 'answer': ans, 'key': f'{cap(a)}: {why}. [1]'}


@c6b.add('C2', (1, 2, 3, 4), 'explain')
def c6b_explain(r, D):
    pick = r.sample(ADAPT, 2 if D <= 2 else 3)
    if len({p[1] for p in pick}) < 2 and D > 2:
        return None
    stem = 'For each adaptation, state whether it is found in the tropical rainforest or the hot desert and explain how it helps survival: ' + '; '.join(cap(p[0]) for p in pick) + '.'
    return {'stem': stem, 'answer': ' '.join(f'{cap(a)} ({e}): {w}.' for a, e, w in pick), 'key': f'For each: 1 mark environment, 1 mark explanation [{2 * len(pick)}]', 'marks': 2 * len(pick)}


# --------------------------------------------------------------- 6.3 deforestation and desertification
c6c = T('Causes and impacts of deforestation and desertification', 'deforestation desertification')
build(c6c, {
    'terms': [
        ('deforestation', 'the permanent clearing of forest for other land uses'),
        ('desertification', 'the gradual change of land in semi-arid areas into desert, caused by drought and human activity'),
        ('commercial logging', 'cutting down trees to sell timber for profit'),
        ('cattle ranching', 'large-scale commercial farming of beef cattle on pasture, the main cause of Amazon deforestation'),
        ('subsistence farming', 'growing food mainly to feed the farmer’s own family'),
        ('slash and burn', 'clearing forest by cutting and burning vegetation to farm for a few years before moving on'),
        ('overgrazing', 'keeping too many animals on land so that vegetation is removed faster than it can regrow'),
        ('soil erosion', 'the removal of topsoil by wind or water faster than it forms'),
        ('Sahel', 'the semi-arid zone south of the Sahara Desert, from Senegal to Sudan, at risk of desertification'),
    ],
    'mcq': [
        ('What is the main cause of deforestation in the Brazilian Amazon?', 'Cattle ranching', ['Tourism', 'Tsunamis', 'Fishing'], 'About 80% of cleared land becomes pasture. [1]'),
        ('Which crop has caused large-scale deforestation in Malaysia and Indonesia?', 'Oil palm', ['Wheat', 'Tea in Kenya', 'Barley'], '[1]'),
        ('Which of these is a human cause of desertification?', 'Overgrazing by livestock', ['Lower rainfall during a drought', 'Higher temperatures', 'Strong winds'], '[1]'),
        ('How does deforestation contribute to climate change?', 'Burning and decaying trees release carbon dioxide, and fewer trees absorb it', ['It cools the planet', 'It increases rainfall everywhere', 'It reduces methane only'], '[1]'),
        ('The Sahel is located', 'on the southern edge of the Sahara Desert', ['in the Amazon basin', 'in central Australia', 'along the Mediterranean coast'], '[1]'),
    ],
    'explain': [
        ('Explain how deforestation can lead to soil erosion.', 'Without a canopy to intercept rain and roots to bind the soil, heavy rain hits bare ground and washes the thin topsoil away; leaching removes nutrients.', '1 mark no interception/roots; 1 mark rain washes soil [2]'),
        ('Explain how deforestation can reduce rainfall in a region.', 'Fewer trees means less transpiration and evaporation, so less moisture enters the air to form clouds and convectional rain.', '1 mark less transpiration; 1 mark fewer clouds/rain [2]'),
        ('Explain how overgrazing and over-cultivation cause desertification.', 'Too many animals remove vegetation and trample the soil; repeated cropping without fallow exhausts nutrients; bare soil is eroded by wind and rain and becomes infertile.', '1 mark each process; 1 mark bare soil eroded [3]'),
        ('Explain why population growth in the Sahel has increased desertification.', 'More people need more food and firewood, so more land is grazed and cultivated, trees are cut for fuel and fallow periods are shortened.', '1 mark more demand; 1 mark land-use effect [2]'),
        ('Describe the impacts of deforestation on indigenous peoples.', 'Loss of land, hunting and gathering grounds; conflict with loggers, miners and ranchers; disease introduced by outsiders; loss of culture and traditional knowledge.', '1 mark each up to [3]'),
    ],
    'claims': [
        ('Desertification is caused only by climate change.', False, 'Drought and rising temperatures play a part, but overgrazing, over-cultivation and cutting trees for fuel are major causes.'),
        ('Deforestation can bring economic benefits to a country.', True, 'Timber, beef, soya, minerals and hydro-electric power earn export income and create jobs.'),
        ('Rainforest soils remain fertile for many decades after clearing.', False, 'Without the nutrient cycle they become infertile within a few years.'),
    ],
    'cs': [
        ('deforestation in a tropical rainforest', [
            ('the Amazon rainforest, Brazil', {'causes': 'Cattle ranching (about 80% of cleared land), soya farming, commercial logging, mining (e.g. Carajás iron ore), roads such as the Trans-Amazonian Highway opening the forest to settlers, and hydro-electric dams such as Belo Monte.',
                                              'impacts': 'Brazil has lost about 17-20% of its Amazon forest; loss of habitats and species; soil erosion and silting of rivers; carbon released, contributing to climate change; less rainfall in the region; indigenous groups lose land; but jobs and export income for Brazil.'}),
            ('deforestation in Borneo, Malaysia and Indonesia', {'causes': 'Clearance for oil palm plantations; commercial logging of hardwoods; forest fires used to clear land; road building and mining.',
                                                                'impacts': 'Habitat loss for orangutans, whose numbers have fallen sharply; smoke haze from fires affecting health in Singapore and Malaysia; peat soils releasing large amounts of carbon; land conflicts with local communities; income and jobs from palm oil.'}),
        ], [
            ('explain the causes of deforestation', 'causes', 'Named economic activities and their scale; government policies; roads opening access.'),
            ('describe the impacts of deforestation on people and the environment', 'impacts', 'Environmental (biodiversity, soils, climate, rivers) and human (indigenous peoples, economy) impacts with figures.'),
        ]),
        ('desertification', [
            ('the Sahel, Africa', {'causes': 'Long droughts since the 1970s and variable rainfall; rapid population growth increasing demand for food and fuelwood; overgrazing by cattle and goats; over-cultivation with shorter fallow periods; cutting trees for firewood.',
                                  'impacts': 'Loss of fertile topsoil; falling crop yields and famine (e.g. Niger 2005, 2010); loss of livestock; migration to cities such as Niamey and abroad; conflict over land and water between herders and farmers; dust storms.'}),
        ], [
            ('explain the causes of desertification', 'causes', 'Physical (drought, rainfall variability) and human (overgrazing, over-cultivation, deforestation, population growth) causes.'),
            ('describe the impacts of desertification on people', 'impacts', 'Food shortages, loss of income, migration, conflict and health impacts.'),
        ]),
    ],
})


@c6c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6c_loss(r, D):
    region = r.choice(['a state in the Brazilian Amazon', 'a province of Borneo', 'a rainforest region in the Congo Basin', 'a forest reserve in Central America'])
    y0 = r.choice([2000, 2005, 2010])
    a0 = r.choice([80, 100, 120, 150, 200]) * 1000
    losses = [r.randint(2, 9) * 500 for _ in range(4)]
    areas = [a0]
    for l in losses:
        areas.append(areas[-1] - l)
    yrs = [y0 + 3 * i for i in range(5)]
    tot = a0 - areas[-1]
    pc = tot / a0 * 100
    per = tot / (yrs[-1] - yrs[0])
    stem = f'Fig. 6.2 shows the area of forest (km²) in {region}: ' + ', '.join(f'{y}: {a:,}'.replace(',', ' ') for y, a in zip(yrs, areas)) + '.'
    if D == 1:
        opts, a = mcq(r, f'{tot:,} km²'.replace(',', ' '), [f'{areas[-1]:,} km²'.replace(',', ' '), f'{losses[-1]:,} km²'.replace(',', ' '), f'{tot * 2:,} km²'.replace(',', ' '), f'{max(losses):,} km²'.replace(',', ' ')])
        return {'stem': stem + f' How much forest was lost between {yrs[0]} and {yrs[-1]}?', 'options': opts, 'answer': a, 'key': f'{a0} − {areas[-1]} = {tot} km². [1]'}
    i = losses.index(max(losses))
    parts = [
        lambda r: (f'Calculate the percentage of the {yrs[0]} forest lost by {yrs[-1]}.', f'{dp(pc)}%', f'{a0} − {areas[-1]} = {tot}; ÷ {a0} × 100 = {dp(pc)}% [2]'),
        lambda r: ('Calculate the mean area lost per year.', f'{fmt(round(per), 0)} km² per year', f'{tot} ÷ {yrs[-1] - yrs[0]} = {fmt(round(per), 0)} km²/yr [1]'),
        lambda r: ('Identify the period with the greatest loss.', f'{yrs[i]}-{yrs[i + 1]} ({losses[i]} km²)', '[1]') if losses.count(max(losses)) == 1 else None,
        lambda r: ('Suggest two reasons for the loss of forest.', 'Clearing for cattle ranching or plantations (soya, oil palm); logging; mining; road building and new settlements; HEP reservoirs.', '1 mark each [2]'),
        lambda r: ('Explain two environmental impacts of the loss shown.', 'Loss of habitat and biodiversity; soil erosion and leaching; less transpiration so less rainfall; carbon released, adding to climate change.', '2 marks each developed impact [4]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 6.4 sustainable management
c6d = T('Sustainable management of tropical rainforests and hot deserts', 'sustainable management')
build(c6d, {
    'terms': [
        ('sustainable management', 'using an environment to meet people’s needs today without damaging it for future generations'),
        ('selective logging', 'cutting down only mature trees of certain species and leaving the rest of the forest standing'),
        ('agroforestry', 'growing crops between trees so that the trees protect and fertilise the soil'),
        ('ecotourism', 'small-scale tourism that protects the environment and benefits local people'),
        ('debt-for-nature swap', 'an agreement in which part of a country’s debt is cancelled in return for protecting its environment'),
        ('Forest Stewardship Council (FSC)', 'an organisation that certifies timber from sustainably managed forests'),
        ('magic stones (stone lines)', 'lines of stones laid along contours that slow run-off, trap soil and help water infiltrate in dry areas'),
        ('Great Green Wall', 'an African-led project to restore a belt of land across the Sahel by planting trees and improving land management'),
    ],
    'mcq': [
        ('Which of these is a sustainable way to manage a rainforest?', 'Selective logging with replanting', ['Clear-felling for cattle ranches', 'Building a large open-cast mine', 'Burning forest for soya farms'], '[1]'),
        ('What does an FSC label on timber show?', 'It comes from a forest managed sustainably', ['It is the cheapest timber', 'It was grown in a desert', 'It is plastic'], '[1]'),
        ('Which technique helps reduce desertification in the Sahel?', 'Laying lines of stones along contours to trap water and soil', ['Increasing herd sizes', 'Removing all trees for fuel', 'Ploughing up and down slopes'], '[1]'),
        ('Costa Rica protects about a quarter of its land in national parks and earns money from', 'ecotourism', ['oil drilling', 'coal mining', 'nuclear power'], '[1]'),
    ],
    'explain': [
        ('Explain how ecotourism can help protect rainforests.', 'It earns money for local people and governments from keeping the forest intact, provides jobs as guides, funds conservation and educates visitors.', '1 mark income/jobs; 1 mark incentive to conserve [2]'),
        ('Explain how agroforestry is more sustainable than slash-and-burn farming.', 'Trees remain, so the canopy protects the soil from heavy rain, roots hold soil, and leaf litter keeps adding nutrients, so the land can be farmed for longer.', '1 mark soil protected; 1 mark nutrient supply [2]'),
        ('Explain how planting trees can reduce desertification.', 'Roots bind the soil and reduce wind erosion; shade reduces evaporation; leaves add organic matter; trees act as windbreaks.', '1 mark each up to [3]'),
        ('Explain why international cooperation is needed to protect rainforests.', 'Demand for beef, soya, palm oil and timber comes from other countries; forests store carbon and biodiversity for the whole world; poorer countries need funding (e.g. debt-for-nature swaps, REDD+).', '1 mark global demand; 1 mark global benefit/funding [2]'),
    ],
    'claims': [
        ('Sustainable management means no one is allowed to use the forest.', False, 'It means using it in ways that let it recover, e.g. selective logging and ecotourism.'),
        ('Stone lines (bunds) help water soak into the soil in the Sahel.', True, 'They slow run-off so water infiltrates and soil is trapped.'),
        ('Buying FSC-certified timber can help reduce unsustainable logging.', True, 'Consumer demand for certified wood rewards sustainable forest managers.'),
    ],
    'cases': [
        (['Fig. 6.3 describes a rainforest area in Costa Rica. In 1985 the forest covered 21% of the country; by 2020 it covered over 50%. Since 1997 landowners have been paid to protect forest (Payments for Environmental Services), funded by a fuel tax. About a quarter of the land is in national parks, and tourism earns over US$4 billion a year.',
          'Study Fig. 6.3, information about forest protection in Costa Rica. Forest cover fell to about 21% in the 1980s, then recovered to over half the country by 2020. Farmers receive payments for keeping or replanting forest, and ecotourism lodges employ local guides.'],
         [('Describe the change in forest cover shown.', 'Forest cover rose from 21% in 1985 to over 50% by 2020 – it more than doubled.', '1 mark trend; 1 mark data [2]'),
          ('Explain how payments to landowners help protect the forest.', 'Farmers earn money from keeping trees, so they do not need to clear forest for cattle or crops.', '1 mark income; 1 mark less clearance [2]'),
          ('Explain how ecotourism benefits local people and the environment.', 'Jobs as guides and in lodges, income kept locally; money and incentive to protect wildlife and forest; small numbers of visitors cause little damage.', '1 mark people; 1 mark environment [2]'),
          ('Suggest why it may be difficult to copy Costa Rica’s approach in other countries.', 'It needs stable government, funding (fuel tax), enforcement against illegal logging, and a tourism industry; other countries may depend more on beef, soya or mining exports.', '1 mark each up to [3]')]),
    ],
    'essays': [
        ('sustainable management can protect tropical rainforests while still allowing economic development',
         ['Selective logging, agroforestry, ecotourism and payments for ecosystem services (Costa Rica) earn income without destroying the forest.'],
         ['Profits from beef, soya, palm oil and mining are much larger and quicker; enforcement is difficult in remote areas.', 'Population growth and poverty push farmers to clear land.'],
         'It can work where governments enforce laws and international funding rewards protection, but large-scale commercial pressures make it difficult.',
         ['ecotourism', 'selective logging', 'international agreements', 'enforcement']),
    ],
})


CHAPTERS[6] = [c6a, c6b, c6c, c6d]


# ============================================================== extra C4 material

def as_c4(t, fn, D=(4, 5)):
    """Register a data template again as a multi-step (C4) item using its fullest form."""
    def g(r, D_, fn=fn):
        q = fn(r, max(D_, 4))
        if q and q.get('options'):
            return None
        return q
    g.__name__ = fn.__name__ + '_c4'
    t.add('C4', D, 'multi_step')(g)


for _t, _f in [(c1a, c1a_scale), (c1a, c1a_grid), (c1b, c1b_grad), (c1b, c1b_xsec), (c1c, c1c_trend), (c1c, c1c_scatter), (c1c, c1c_stats),
               (c2a, c2a_rate), (c2b, c2b_table), (c2d, c2d_data), (c2e, c2e_compare), (c3a, c3a_hydro), (c3b, c3b_dis), (c3b, c3b_bradshaw),
               (c3d, c3d_rain), (c3e, c3e_cba), (c4a, c4a_drift), (c4b, c4b_retreat), (c4c, c4c_profile), (c4d, c4d_bleach), (c4e, c4e_cost),
               (c5a, c5a_week), (c5b, c5b_press), (c5b, c5b_rose), (c5c, c5c_fig), (c5d, c5d_fig), (c6a, c6a_store), (c6c, c6c_loss)]:
    as_c4(_t, _f)

add_essay(c4b, 'rock type is the most important factor in the formation of erosional coastal landforms',
          ['Headlands and bays form where hard and soft rocks alternate (Dorset); joints and faults in chalk and limestone are eroded into caves, arches and stacks.'],
          ['Wave energy, fetch and storms supply the erosive power; sub-aerial weathering weakens cliffs and arch roofs; sea-level change and human defences also matter.'],
          'Rock type and structure control where and what landforms develop, but wave energy determines how fast they form.',
          ['hard and soft rock', 'joints and faults', 'wave energy', 'weathering'])
add_essay(c4c, 'depositional coastal landforms such as spits and beaches are more easily damaged than erosional landforms',
          ['Spits and beaches are made of loose sand and shingle that storms can remove quickly; cutting off sediment supply (e.g. groynes updrift) starves them.'],
          ['Erosional landforms such as arches and stacks also collapse (e.g. Azure Window, Malta, 2017); spits can rebuild if sediment supply continues; dunes stabilised by vegetation are resilient.'],
          'Depositional landforms change faster and depend on sediment supply, so they are generally more fragile, though no coastal landform is permanent.',
          ['sediment supply', 'storms', 'vegetation', 'human interference'])
add_essay(c5a, 'satellites and automatic weather stations have made school weather stations unnecessary',
          ['Satellites and automatic stations give continuous, accurate data over large areas and are used for forecasts.'],
          ['School stations teach how instruments work and how to collect and check data; they record local conditions (microclimates) that satellites miss; they are cheap.'],
          'Professional data are more accurate, but school stations remain useful for learning and for local enquiries.',
          ['accuracy', 'cost', 'local conditions', 'learning'])
add_essay(c5b, 'relief is more important than latitude in explaining differences in rainfall between places',
          ['Windward slopes receive heavy relief rain while leeward areas lie in a rain shadow, e.g. the western Ghats compared with the Deccan plateau.'],
          ['Latitude controls pressure belts: rising air at the Equator gives heavy convectional rain; sinking air at 20-30° creates hot deserts.', 'Distance from the sea and ocean currents also matter.'],
          'Latitude sets the broad global pattern of rainfall, while relief explains many local differences.',
          ['relief rainfall', 'rain shadow', 'pressure belts', 'ocean currents'])
add_case(c5b, [
    'Fig. 5.4 describes a mountain range 2500 m high running north-south. The prevailing wind blows from the west off a warm ocean. Town P lies on the western slopes at 800 m and receives 2400 mm of rain a year; town Q lies on the eastern side at 600 m and receives 450 mm a year.',
    'Study Fig. 5.4. Moist westerly winds cross a coastal mountain range. Station P, on the windward slopes, records 2400 mm of rain a year; station Q, 60 km away on the leeward side, records only 450 mm.'],
    [('Calculate how many times more rain P receives than Q.', f'{fmt(2400 / 450, 2)} times (about 5.3)', '2400 ÷ 450 = 5.3 [1]'),
     ('Explain why P receives so much rain.', 'Moist westerly air is forced to rise over the mountains, cools, condenses and forms relief rain on the windward slopes.', '1 mark forced ascent; 1 mark cooling/condensation; 1 mark windward [3]'),
     ('Explain why Q receives little rain.', 'Q is in the rain shadow: air has lost much moisture and descends the leeward side, warming, so clouds evaporate.', '1 mark rain shadow; 1 mark descending/warming air [2]'),
     ('Suggest how the type of farming might differ between P and Q.', 'P: crops needing much rain (e.g. tea, rice) or forest; Q: drought-tolerant crops, irrigation or grazing.', '1 mark each [2]'),
     ('Suggest how a climate graph for Q would differ from one for P.', 'Shorter rainfall bars in most months; possibly higher summer temperatures and a larger range because of clearer skies.', '1 mark rainfall; 1 mark temperature [2]')])
add_essay(c6a, 'the nutrient cycle is the main reason why tropical rainforests are fragile ecosystems',
          ['Most nutrients are held in the biomass; once trees are removed, heavy rain leaches the thin soil and fertility collapses within a few years.'],
          ['Interdependence in food webs means removing one species affects many others; the forest also depends on recycling its own rainfall through transpiration.', 'Climate change and fire threaten even untouched forest.'],
          'The nutrient cycle is a key reason, because clearing breaks it so quickly, but interdependence and the water cycle add to the fragility.',
          ['nutrient stores', 'leaching', 'food webs', 'transpiration'])
add_case(c6b, [
    'Fig. 6.4 describes two plants. Plant X grows to 45 m, has large ridged roots spreading above the ground, smooth thin bark and leaves with pointed tips. Plant Y grows to 3 m, has a thick, swollen ribbed stem covered in a waxy layer, spines instead of leaves, and roots spreading 10 m just below the surface.',
    'Study Fig. 6.4. Plant X: a tall tree with buttress roots, drip-tip leaves and thin bark. Plant Y: a cactus with a swollen stem, a waxy coating, spines and a wide, shallow root system.'],
    [('State which plant grows in a tropical rainforest and which in a hot desert.', 'X: tropical rainforest. Y: hot desert.', '[1]'),
     ('Explain how two features help plant X to survive.', 'Buttress roots support the tall tree in shallow soil; drip tips shed heavy rain to stop rot; thin bark because no protection from cold is needed.', '2 marks each developed adaptation [4]'),
     ('Explain how two features help plant Y to survive.', 'Spines reduce water loss and deter animals; swollen stem stores water; waxy layer reduces transpiration; shallow widespread roots absorb rare rain quickly.', '2 marks each developed adaptation [4]'),
     ('Suggest why plant Y’s roots spread so widely near the surface.', 'Rain is rare and does not soak deeply, so roots must collect water from a large area quickly before it evaporates.', '1 mark rare rain; 1 mark quick absorption [2]')], C3=(1, 2, 3, 4, 5))
add_essay(c6b, 'animals in hot deserts are better adapted to their environment than animals in tropical rainforests',
          ['Desert animals survive extreme heat and little water: camels store fat and tolerate dehydration; fennec foxes lose heat through large ears; many are nocturnal.'],
          ['Rainforest animals are equally specialised: prehensile tails, camouflage (sloths), specialised diets and climbing skills for life in the canopy.', 'Both sets of adaptations suit very different challenges.'],
          'Neither is “better adapted”: each species is adapted to the particular pressures of its own ecosystem.',
          ['camels', 'monkeys', 'water and heat', 'competition'])
