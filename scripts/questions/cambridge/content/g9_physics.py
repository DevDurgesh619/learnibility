"""Cambridge IGCSE Physics 0625 (2026-28), CUP coursebook chapters 1-13 (grade 9).

Chapters: 1 Making measurements, 2 Describing motion, 3 Forces and motion, 4 Turning effects,
5 Forces and matter, 6 Energy stores and transfers, 7 Energy resources, 8 Work and power,
9 Kinetic particle model, 10 Thermal properties, 11 Thermal energy transfers, 12 Sound, 13 Light.

One Topic per W2 subtopic (name = subtopic name). Fixed C1/C2 lists carry recall and explanation
(auto-paired into two-part items); parameterised templates carry calculations and data work and
scale with D; compose() builds Paper 4 / Paper 6 style structured items with "[n]" part marks.
g = 9.8 N/kg throughout (as on 0625 papers).
"""
import math
import re
from ._lib import topic, mcq, relation, sf, sci, person, two_people, city, num_mcq, near
from ._lib import compose as _compose

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}
G = 9.8

# ===================================================================== helpers
_MK = re.compile(r'\[(\d+)\]')


def g(x, n=3):
    """Number for display: n significant figures (half-up), trailing zeros removed, thin grouping for >= 10 000."""
    if isinstance(x, int):
        return str(x) if abs(x) < 10000 else f'{x:,}'.replace(',', ' ')
    if x == 0:
        return '0'
    from decimal import Decimal, ROUND_HALF_UP
    d = n - int(math.floor(math.log10(abs(x)))) - 1
    v = Decimal(repr(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if d <= 0:
        iv = int(v)
        return str(iv) if abs(iv) < 10000 else f'{iv:,}'.replace(',', ' ')
    s = f'{v:.{d}f}'
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s


def cap(s):
    return s[0].upper() + s[1:] if s else s


_NEG = re.compile(r'(?<![\w)\]])-(?=\d)')


def neg(x):
    return _NEG.sub('−', x) if isinstance(x, str) else x


def Q(stem, answer, key, typ=None, opts=None):
    stem, answer, key = neg(stem), neg(answer), neg(key)
    opts = [neg(o) for o in opts] if opts else opts
    d = {'stem': stem, 'answer': answer, 'key': key}
    if opts:
        d['options'] = opts
        d['marks'] = 1
    else:
        m = _MK.findall(key)
        if m:
            d['marks'] = max(1, min(20, int(m[-1])))
    if typ:
        d['type'] = typ
    return d


_NUMANS = re.compile(r'^[−\-]?\d')


def _fix_key(a, k):
    """Turn a bare part key such as "[2]" or "mgh [2]" into mark points."""
    m = re.fullmatch(r'\s*(.*?)\s*\[(\d+)\]\s*', k)
    if not m or ';' in m.group(1) or '[' in m.group(1):
        return k
    body, n = m.group(1).rstrip(' :'), int(m.group(2))
    a0 = a.strip().rstrip('.')
    if _NUMANS.match(a0):
        wu = ' with unit' if re.search(r'\d\s*[A-Za-z°%µΩ]', a0) else ''
        if n == 1:
            return f'{body + ": " if body else ""}{a0} [1]'
        if n == 2:
            return f'{body + " (method/substitution)" if body else "correct method/substitution"} [1]; answer {a0}{wu} [1] [2]'
        return f'{body + " (equation)" if body else "correct equation"} [1]; substitution [1]; answer {a0}{wu} [1] [{n}]'
    pieces = [x.strip(' .') for x in re.split(r';\s*|:\s+|\.\s+(?=[A-Z])|,\s+(?=and\b)|,?\s+(?=(?:so|because|which|as)\s)', a0) if x.strip(' .')]
    if body:
        pieces = [body] + pieces if n > 1 and len(pieces) < n else pieces
    if n == 1:
        return f'{a0} [1]'
    if len(pieces) < n and ', ' in a0:
        pieces = [x.strip(' .') for x in a0.split(', ') if x.strip(' .')]
    if len(pieces) >= n:
        return '; '.join(f'{pc} [1]' for pc in pieces[:n - 1]) + '; ' + ', '.join(pieces[n - 1:]) + f' [1] [{n}]'
    return f'{a0} (1 mark per correct point, max {n}) [{n}]'


def compose(r, intro, parts, **kw):
    def wrap(p):
        def f(r_):
            x = p(r_)
            return (neg(x[0]), neg(x[1]), neg(_fix_key(x[1], x[2]))) if x else x
        return f
    return _compose(r, neg(intro), [wrap(p) for p in parts], **kw)


def FX(t, C, D, entries, typ=None):
    """t.fixed + marks taken from each key (MCQ = 1 mark). Incomplete MCQ stems get an ellipsis."""
    entries = [((e[0] if re.search(r'[?.:)…]$', e[0]) else e[0] + ' …'),) + tuple(e[1:]) for e in entries]
    n0 = len(t.templates)
    t.fixed(C, D, entries, typ)
    for tp in t.templates[n0:]:
        base = tp.fn

        def fn(r, D_, base=base):
            q = base(r, D_)
            if q.get('options'):
                q['marks'] = 1
            else:
                m = _MK.findall(q['key'])
                if m:
                    q['marks'] = int(m[-1])
            return q
        tp.fn = fn
    return t


def numq(r, D, setup, qty, val, unit, working, wrong, marks=None, fm=g, typ='numerical'):
    """Single-answer calculation. D1 -> MCQ; otherwise a structured answer with [n] marks."""
    setup, working = neg(setup), neg(working)
    ans = neg(fm(val) + unit)
    if D <= 1:
        opts, a = num_mcq(r, val, [w for w in wrong if w > 0] + [val * 2, val / 2, val * 10], fmtf=fm, unit=unit)
        opts, a = [neg(o) for o in opts], neg(a)
        return {'stem': f'{setup} What is the {qty}?', 'options': opts, 'answer': a, 'key': f'{working} = {ans}.', 'marks': 1}
    m = marks or (2 if D <= 2 else 3 if D == 3 else 4)
    lead = r.choice(['Calculate', 'Calculate', 'Determine', 'Work out'])
    return Q(f'{setup} {lead} the {qty}.', ans, f'{working} = {ans}. (equation/substitution, then answer with unit) [{m}]', typ)


COAST = ['Lisbon', 'Cape Town', 'Singapore', 'Lagos', 'Mumbai', 'Manila', 'Colombo', 'Auckland', 'Muscat', 'Accra', 'Karachi', 'Jakarta', 'Doha', 'Dubai', 'Istanbul', 'Kuala Lumpur']


def coast(r):
    return r.choice(COAST)


def scene_pick(r, frames, **kw):
    return r.choice(frames).format(p=person(r), c=city(r), **kw)


# =========================================================== 1 Making measurements
N11 = 'Measuring length, volume and time including multiple readings'
t11 = topic(N11, N11.lower(), 'measuring length', 'multiple readings')
FX(t11, 'C1', (1, 2), [
    ('Which instrument is most suitable for measuring the length of a laboratory bench?', 'A metre rule', 'A metre rule (or tape) covers the length with millimetre resolution.',
     ['A measuring cylinder', 'A stopwatch', 'A thermometer']),
    ('How should the volume of water in a measuring cylinder be read?', 'At the bottom of the meniscus with the eye level with the surface', 'Read the bottom of the curved meniscus, eye level to avoid parallax error.',
     ['At the top of the meniscus looking down from above', 'At the highest point the water reaches on the glass', 'At any point, as long as the cylinder is tilted']),
    ('What is the SI unit of time?', 'second (s)', 'The SI base unit of time is the second.', ['minute (min)', 'hour (h)', 'hertz (Hz)']),
    ('A volume of 1 cm³ is the same as', '1 ml', '1 cm³ = 1 ml; 1000 cm³ = 1 litre.', ['1 litre', '1 m³', '10 ml']),
    ('How many cubic centimetres are there in 1 m³?', '1 000 000 cm³', '1 m = 100 cm so 1 m³ = 100³ cm³ = 10⁶ cm³.', ['100 cm³', '1000 cm³', '10 000 cm³']),
    ('Why does a student time 20 swings of a pendulum rather than one swing?', 'To reduce the effect of reaction-time error on the period', 'A longer total time makes the human reaction-time error a smaller fraction of the reading.',
     ['To make the pendulum swing faster', 'Because one swing cannot be seen', 'To increase the period of the pendulum']),
    ('State what is meant by the period of a pendulum.', 'The time taken for one complete oscillation (there and back).', 'Time for one complete swing from one side to the other and back [1]'),
    ('State how a student can find the thickness of one sheet of paper using a ruler.', 'Measure the thickness of a large stack (e.g. 100 sheets) and divide by the number of sheets.', 'measure many sheets [1]; divide by number of sheets [1] [2]'),
])
FX(t11, 'C2', (1, 2, 3), [
    ('Explain why a measurement of the time for one swing of a pendulum is less reliable than a measurement of the time for twenty swings.', 'Reaction time (about 0.2 s) is the same for each timing, so for twenty swings it is a much smaller fraction of the total time; dividing by twenty gives a more accurate period.', 'reaction time error similar for both [1]; smaller percentage of a longer time / divided by 20 [1] [2]'),
    ('Explain what is meant by parallax error when reading a ruler, and how to avoid it.', 'Reading the scale from an angle makes the object appear against the wrong mark; avoid it by looking perpendicular to the scale (eye directly in line with the mark).', 'describes viewing at an angle [1]; eye perpendicular / in line with the mark [1] [2]'),
    ('Explain why a student should start a stopwatch as the pendulum passes through the centre of its swing rather than at the end of the swing.', 'The bob moves fastest at the centre, so the moment it passes a fiducial mark there is easiest to judge; at the end it is momentarily still, so the exact moment is hard to judge.', 'fastest at centre so passing moment clear [1]; end of swing is hard to judge [1] [2]'),
    ('Explain why taking several readings of the same length and calculating the mean gives a more reliable result.', 'Random errors make individual readings scatter above and below the true value; averaging reduces the effect of random errors and allows anomalous readings to be spotted.', 'random errors / scatter [1]; averaging reduces their effect or anomalies identified [1] [2]'),
    ('A student uses a 30 cm ruler to measure the length of a corridor about 12 m long. Explain why this is a poor choice and suggest a better instrument.', 'The ruler must be moved many times, so small errors add up at each move; a measuring tape or trundle wheel covers the length in one measurement.', 'errors accumulate with repeated moves [1]; tape measure / trundle wheel [1] [2]'),
    ('Explain why the zero end of a worn ruler should not be used as the starting point for a measurement.', 'The end may be damaged so 0 is not at the true zero (zero error); start from another mark such as 1.0 cm and subtract it.', 'zero error from worn end [1]; start from another mark and subtract [1] [2]'),
])
STACKS = [('sheets of paper in a ream', 'paper', (200, 500), (0.09, 0.11)), ('identical coins in a stack', 'coin', (10, 30), (1.5, 2.3)),
          ('identical CDs in a spindle', 'CD', (20, 50), (1.1, 1.3)), ('identical glass microscope slides', 'slide', (20, 50), (0.9, 1.2)),
          ('identical steel washers on a bolt', 'washer', (10, 40), (1.4, 2.6)), ('pages of a textbook (excluding the covers)', 'page', (150, 400), (0.06, 0.1))]


@t11.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_stack(r, D):
    what, one, (n1, n2), (a, b) = r.choice(STACKS)
    n = r.randrange(n1, n2 + 1, 10 if n2 > 100 else 1)
    tot = max(5, round(n * r.uniform(a, b)))  # whole millimetres, as read from a ruler
    th = tot / n
    if D <= 2:
        return numq(r, D, f'{person(r)} measures the total thickness of {n} {what} as {g(tot / 10, 3)} cm.', f'thickness of one {one} in mm', th, ' mm',
                    f'thickness = {g(tot, 3)} mm / {n}', [tot / n / 10, tot / 10 * n, th * 10], fm=lambda x: g(x, 3))
    start = round(r.choice([0.5, 1.0, 1.5, 2.0, 3.0]), 1)
    end = start + tot / 10
    if D == 3:
        return Q(f'{person(r)} places a stack of {n} {what} against a ruler. The bottom of the stack is at the {g(start)} cm mark and the top is at the {g(end, 4)} cm mark. Calculate the thickness of one {one} in millimetres.',
                 f'{g(th, 3)} mm', f'stack = {g(end, 4)} − {g(start)} = {g(tot / 10, 3)} cm = {g(tot, 3)} mm [1]; ÷ {n} [1]; = {g(th, 3)} mm [1] [3]')
    k = r.choice([2, 3, 4])
    return Q(f'{person(r)} wants the thickness of one {one}. The bottom of a stack of {n} {what} is at the {g(start)} cm mark of a ruler and the top is at {g(end, 4)} cm. (a) Calculate the thickness of one {one} in mm. (b) Calculate the height of a stack of {k * n} of them in cm. (c) Explain why measuring a stack is better than measuring one {one}.',
             f'(a) {g(th, 3)} mm (b) {g(k * tot / 10, 3)} cm (c) one {one} is too thin to measure precisely with a ruler; the reading error is shared over {n} items.',
             f'(a) {g(end, 4)} − {g(start)} = {g(tot / 10, 3)} cm; ÷ {n} = {g(th, 3)} mm [2] (b) {k * n} × {g(th, 3)} mm = {g(k * tot / 10, 3)} cm [1] (c) ruler resolution 1 mm too coarse for one item; error divided by number in stack [2] [5]', 'multi_step')


PEND = ['a simple pendulum made from a lump of modelling clay on a thread', 'a pendulum made from a metal bob on a string', 'a child on a playground swing',
        'a mass hanging from a spring bouncing up and down', 'a metronome arm', 'a ruler clamped to the bench and set vibrating']


@t11.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_period(r, D):
    thing = r.choice(PEND)
    n = r.choice([10, 20, 25, 30, 40, 50]) if 'swing' not in thing else r.choice([5, 8, 10])
    T = round(r.uniform(0.5, 2.4), 2) if 'swing' not in thing else round(r.uniform(2.0, 3.5), 2)
    if D <= 2:
        tt = n * T
        return numq(r, D, f'{person(r)} times {n} complete oscillations of {thing} and records {g(tt, 4)} s.', 'period of one oscillation', T, ' s',
                    f'T = {g(tt, 4)} / {n}', [tt, T * 2, tt / (n + 1)], fm=lambda x: g(x, 3))
    times = [round(n * T + r.uniform(-0.3, 0.3), 1) for _ in range(3)]
    mean = sum(times) / 3
    if D == 3:
        return Q(f'{person(r)} times {n} oscillations of {thing} three times: ' + ', '.join(f'{x:.1f} s' for x in times) + '. Calculate the mean time and hence the period.',
                 f'mean = {g(mean, 4)} s; T = {g(mean / n, 3)} s', f'mean = ({" + ".join(f"{x:.1f}" for x in times)})/3 = {g(mean, 4)} s [1]; T = mean/{n} [1] = {g(mean / n, 3)} s [1] [3]')
    bad = round(n * T * r.choice([0.8, 1.2, 0.85, 1.15]), 1)
    data = times + [bad]
    r.shuffle(data)
    return Q(f'{person(r)} records the time for {n} oscillations of {thing} four times: ' + ', '.join(f'{x:.1f} s' for x in data) + '. (a) Identify the anomalous reading and suggest a cause. (b) Calculate the period using the remaining readings. (c) Suggest one further improvement to the method.',
             f'(a) {bad:.1f} s; e.g. miscounted oscillations or late start/stop. (b) {g(mean / n, 3)} s (c) use a fiducial marker at the centre of the swing / time more oscillations / repeat more.',
             f'(a) identifies {bad:.1f} s [1]; plausible cause (miscount, reaction time) [1] (b) mean of other three = {g(mean, 4)} s [1]; ÷ {n} = {g(mean / n, 3)} s [1] (c) any sensible improvement [1] [5]' if D >= 5 else
             f'(a) identifies {bad:.1f} s with plausible cause [1] (b) mean of other three = {g(mean, 4)} s [1]; ÷ {n} = {g(mean / n, 3)} s [1] (c) fiducial marker / more oscillations / more repeats [1] [4]', 'case')


@t11.add('C3', (1, 2, 3), 'numerical')
def t11_cyl(r, D):
    v1 = r.choice([20, 25, 30, 35, 40, 45, 50, 60])
    dv = r.choice([4, 6, 7.5, 8, 9, 12, 14, 15, 18])
    obj = r.choice(['a small stone', 'a glass marble', 'a brass key', 'a piece of gravel', 'a metal nut', 'a plastic toy figure (held under with a thin pin)'])
    if D == 3:
        return Q(f'A measuring cylinder contains {v1} cm³ of water. When {obj} is lowered in, the reading rises to {g(v1 + dv)} cm³. State the volume of the object in cm³ and in m³, and state one precaution when taking the readings.',
                 f'{g(dv)} cm³ = {sci(dv * 1e-6, 2)} m³; read the bottom of the meniscus at eye level / lower gently so no water splashes out.',
                 f'V = {g(v1 + dv)} − {v1} = {g(dv)} cm³ [1]; ÷ 10⁶ = {sci(dv * 1e-6, 2)} m³ [1]; precaution [1] [3]')
    return numq(r, D, f'A measuring cylinder contains {v1} cm³ of water. {cap(obj)} is lowered in and the water level rises to {g(v1 + dv)} cm³.', 'volume of the object', dv, ' cm³',
                f'V = {g(v1 + dv)} − {v1}', [v1 + dv, v1, dv * 2])


def _meas_c4(r, D):
    thing = r.choice(PEND[:3] + PEND[4:])
    n = r.choice([10, 20, 25])
    T = round(r.uniform(0.8, 2.2), 2)
    tt = round(n * T, 1)
    intro = r.choice([f'{person(r)} investigates {thing} in a school laboratory in {city(r)}.', f'In a practical exam, a candidate is given {thing} and a stopwatch reading to 0.01 s.',
                      f'{person(r)} is asked to find the period of {thing} as accurately as possible.'])
    parts = [
        lambda r: (f'The time for {n} oscillations is {tt} s. Calculate the period.', f'{g(tt / n, 3)} s', f'T = {tt}/{n} = {g(tt / n, 3)} s [2]'),
        lambda r: ('Explain why the stopwatch reading to 0.01 s does not make each timing accurate to 0.01 s.', 'Human reaction time (about 0.1–0.3 s) at start and stop is much larger than 0.01 s.', 'reaction time [1]; much larger than resolution [1] [2]'),
        lambda r: ('Describe how the student should use a fiducial marker.', 'Place a marker (pin or line) at the centre of the swing and start/stop timing as the bob passes it in the same direction.', 'marker at centre/rest position [1]; time as bob passes it in same direction [1] [2]'),
        lambda r: ('State two variables that should be kept constant when comparing the periods of two pendulums of different lengths.', 'Mass of bob and amplitude (starting angle) of swing; same timing method.', 'any two [2]'),
        lambda r: ('Suggest why the number of oscillations should not be counted as "1" when the timer is started.', 'Counting must start from zero at the start so that the number of complete oscillations is correct; starting at 1 gives one too many.', 'count 0 at start [1]; otherwise one oscillation too many [1] [2]'),
        lambda r: (f'Another student times only 1 oscillation and gets {g(T + r.choice([0.2, -0.2, 0.3]), 3)} s. Comment on this result.', 'Less reliable: reaction-time error is a large fraction of a single period, so the value differs noticeably from the value from many oscillations.', 'compares with multiple-oscillation value [1]; reaction time large fraction [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t11.add('C4', (2, 3, 4, 5), 'multi_step')(_meas_c4)

N12 = 'Density: measuring and calculating ρ = m/V for liquids and regular and irregular solids'
t12 = topic(N12, N12.lower(), 'density')
DENS = [('aluminium', 2.7), ('iron', 7.9), ('copper', 8.9), ('lead', 11.3), ('gold', 19.3), ('silver', 10.5), ('zinc', 7.1), ('brass', 8.5),
        ('glass', 2.5), ('oak wood', 0.75), ('pine wood', 0.5), ('ice', 0.92), ('cork', 0.24), ('granite', 2.7), ('marble', 2.6), ('polythene', 0.93)]
LIQ = [('water', 1.0), ('olive oil', 0.92), ('sea water', 1.03), ('ethanol', 0.79), ('glycerol', 1.26), ('mercury', 13.6), ('paraffin', 0.80), ('milk', 1.03)]
FX(t12, 'C1', (1, 2), [
    ('Which equation defines density?', 'density = mass ÷ volume', 'ρ = m/V.', ['density = volume ÷ mass', 'density = mass × volume', 'density = weight × volume']),
    ('What is the SI unit of density?', 'kg/m³', 'Mass in kg divided by volume in m³ gives kg/m³ (g/cm³ is also used).', ['kg/m²', 'N/m³', 'kg m³']),
    ('The density of water is 1000 kg/m³. What is this in g/cm³?', '1.0 g/cm³', '1000 kg/m³ = 1.0 g/cm³ (divide by 1000).', ['1000 g/cm³', '0.001 g/cm³', '100 g/cm³']),
    ('An object will float on water if', 'its density is less than the density of water', 'Objects less dense than the liquid float; denser objects sink.', ['its mass is less than 1 kg', 'its volume is greater than that of the water', 'its density is greater than that of water']),
    ('Which method is used to find the volume of an irregularly shaped stone?', 'Displacement of water in a measuring cylinder', 'The rise in water level equals the volume of the stone.', ['Measuring its length, width and height', 'Weighing it on a balance', 'Timing how long it takes to sink']),
    ('Two liquids that do not mix are poured into a beaker. Which liquid forms the bottom layer?', 'The liquid with the greater density', 'Denser liquids sink below less dense liquids.', ['The liquid with the greater volume', 'The liquid poured in first', 'The liquid with the smaller mass']),
    ('State the apparatus needed to find the density of a liquid.', 'A measuring cylinder and a balance (top-pan balance).', 'measuring cylinder [1]; balance [1] [2]'),
])
FX(t12, 'C2', (1, 2, 3, 4), [
    ('A block of wood and a block of iron have the same mass. Explain which has the larger volume.', 'The wood, because it is less dense; V = m/ρ, so for the same mass a smaller density means a larger volume.', 'wood [1]; V = m/ρ with smaller ρ [1] [2]'),
    ('Explain why a large ship made of steel floats although steel is denser than water.', 'The ship is hollow and full of air, so its average density (total mass ÷ total volume enclosed) is less than that of water.', 'hollow/air [1]; average density less than water [1] [2]'),
    ('Describe how to find the density of an irregular stone.', 'Find its mass on a balance; put water in a measuring cylinder, read the volume, lower the stone in and read again; volume = difference; density = mass ÷ volume.', 'mass on balance [1]; displacement readings and subtract [1]; ρ = m/V [1] [3]'),
    ('Describe how to find the density of a liquid such as cooking oil.', 'Weigh an empty measuring cylinder, add a measured volume of oil and weigh again; mass of oil = difference; density = mass ÷ volume.', 'mass of empty cylinder and with oil [1]; volume read from cylinder [1]; ρ = m/V [1] [3]'),
    ('Ice floats on water, but solid wax sinks in liquid wax. Explain what this tells you about each substance when it freezes.', 'Water expands on freezing so ice is less dense than water; wax contracts on freezing so solid wax is denser than liquid wax.', 'ice less dense / water expands [1]; solid wax denser / contracts [1] [2]'),
    ('A student says a heavier object always has a greater density. Explain why this is wrong.', 'Density depends on mass and volume; a heavy object may have a very large volume, e.g. a large log is heavier than a small steel bolt but less dense.', 'density is mass per unit volume [1]; valid counter-example [1] [2]'),
])


@t12.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_reg(r, D):
    mat, rho = r.choice(DENS)
    a, b, c = r.choice([2, 2.5, 3, 4, 5]), r.choice([2, 3, 4, 5, 6]), r.choice([1, 1.5, 2, 2.5, 4, 10])
    V = a * b * c
    m = rho * V
    frame = r.choice(['A rectangular block of {mat}', 'A cuboid cut from {mat}', 'A small {mat} brick', 'A sample of {mat} shaped as a cuboid'])
    obj = frame.format(mat=mat)
    if D <= 2:
        return numq(r, D, f'{obj} has a mass of {g(m, 3)} g and a volume of {g(V)} cm³.', 'density in g/cm³', rho, ' g/cm³', f'ρ = m/V = {g(m, 3)} / {g(V)}', [V / m, m * V / 100, rho * 1000])
    if D == 3:
        return Q(f'{obj} measures {g(a)} cm × {g(b)} cm × {g(c)} cm and has a mass of {g(m, 3)} g. Calculate its density in g/cm³.', f'{g(rho, 3)} g/cm³',
                 f'V = {g(a)} × {g(b)} × {g(c)} = {g(V)} cm³ [1]; ρ = m/V = {g(m, 3)}/{g(V)} [1] = {g(rho, 3)} g/cm³ [1] [3]')
    ans = rho * 1000
    extra = '' if D == 4 else f' Use the table of densities (aluminium 2700, iron 7900, copper 8900, lead 11 300 kg/m³) to say whether it could be one of these metals.'
    k = f'V = {g(V)} cm³ = {sci(V * 1e-6, 3)} m³ [1]; m = {g(m / 1000, 3)} kg [1]; ρ = m/V [1] = {g(ans, 3)} kg/m³ [1]' + ('' if D == 4 else ' ; correct identification or "none of these" [1]') + (' [4]' if D == 4 else ' [5]')
    tab = {'aluminium': 2.7, 'iron': 7.9, 'copper': 8.9, 'lead': 11.3}
    ident = next((k2 for k2, v in tab.items() if abs(v - rho) < 0.05), None)
    return Q(f'{obj} measures {g(a)} cm × {g(b)} cm × {g(c)} cm and has a mass of {g(m / 1000, 3)} kg. Calculate its density in kg/m³.{extra}', f'{g(ans, 3)} kg/m³' + ('' if D == 4 else f'; {"it could be " + ident if ident else "it is none of these metals"}'), k, 'multi_step' if D > 4 else 'numerical')


@t12.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_irreg(r, D):
    mat, rho = r.choice([x for x in DENS if x[1] > 1.1])
    v1 = r.choice([30, 40, 50, 55, 60, 70])
    dv = r.choice([5, 6, 8, 10, 12, 15, 20])
    m = rho * dv
    obj = r.choice([f'an irregular piece of {mat}', f'a lump of {mat}', f'a small {mat} ornament', f'a broken fragment of {mat}'])
    if D <= 2:
        return numq(r, D, f'{person(r)} finds that {obj} has a mass of {g(m, 3)} g. It is lowered into a measuring cylinder and the water level rises from {v1} cm³ to {v1 + dv} cm³.', 'density of the object', rho, ' g/cm³',
                    f'V = {v1 + dv} − {v1} = {dv} cm³; ρ = {g(m, 3)}/{dv}', [m / (v1 + dv), m / v1, dv / m])
    tot_m = m + r.choice([0, 0])
    if D == 3:
        return Q(f'{person(r)} finds the mass of {obj} is {g(m, 3)} g. The water in a measuring cylinder reads {v1} cm³ before and {v1 + dv} cm³ after the object is fully submerged. Calculate the density in kg/m³.', f'{g(rho * 1000, 3)} kg/m³',
                 f'V = {dv} cm³ [1]; ρ = {g(m, 3)}/{dv} = {g(rho, 3)} g/cm³ [1]; × 1000 = {g(rho * 1000, 3)} kg/m³ [1] [3]')
    ov = r.choice([2, 3, 4])
    return Q(f'{person(r)} measures the density of {obj}. Its mass is {g(m, 3)} g. The measuring cylinder reads {v1} cm³ before and {v1 + dv} cm³ after the object is submerged, but {ov} cm³ of water splashed out as it was dropped in. (a) Calculate the density obtained if the splash is ignored. (b) Calculate the true density. (c) Suggest how to avoid this error.',
             f'(a) {g(m / dv, 3)} g/cm³ (b) {g(m / (dv + ov), 3)} g/cm³ (c) lower the object gently on a thread / tilt the cylinder / use a displacement (Eureka) can.',
             f'(a) {g(m, 3)}/{dv} = {g(m / dv, 3)} g/cm³ [1] (b) true V = {dv} + {ov} = {dv + ov} cm³ [1]; ρ = {g(m / (dv + ov), 3)} g/cm³ [1] (c) sensible method [1] [4]', 'multi_step')


@t12.add('C3', (1, 2, 3, 4), 'numerical')
def t12_liquid(r, D):
    liq, rho = r.choice(LIQ)
    me = r.choice([82.4, 95.0, 110.6, 124.2, 136.8, 150.5])
    V = r.choice([50, 75, 80, 100, 120, 150, 200])
    m = rho * V
    if D <= 2:
        return numq(r, D, f'{V} cm³ of {liq} has a mass of {g(m, 3)} g.', f'density of {liq}', rho, ' g/cm³', f'ρ = {g(m, 3)}/{V}', [V / m, m * V / 1000, rho * 10])
    s = f'An empty measuring cylinder has a mass of {me} g. After {V} cm³ of {liq} is added, the total mass is {g(me + m, 4)} g.'
    if D == 3:
        return Q(s + f' Calculate the density of the {liq} in g/cm³.', f'{g(rho, 3)} g/cm³', f'mass of liquid = {g(me + m, 4)} − {me} = {g(m, 3)} g [1]; ρ = {g(m, 3)}/{V} [1] = {g(rho, 3)} g/cm³ [1] [3]')
    V2 = r.choice([250, 500, 750, 1000, 2000])
    return Q(s + f' (a) Calculate the density of the {liq}. (b) Calculate the mass of {V2} cm³ of the {liq} in kg.', f'(a) {g(rho, 3)} g/cm³ (b) {g(rho * V2 / 1000, 3)} kg',
             f'(a) m = {g(m, 3)} g [1]; ρ = {g(rho, 3)} g/cm³ [1] (b) m = ρV = {g(rho, 3)} × {V2} = {g(rho * V2, 4)} g [1] = {g(rho * V2 / 1000, 3)} kg [1] [4]', 'multi_step')


@t12.add('C2', (2, 3, 4), 'explain')
def t12_float(r, D):
    mat, rho = r.choice(DENS)
    liq, rl = r.choice([x for x in LIQ if abs(x[1] - rho) > 0.04])
    fl = rho < rl
    return Q(f'A solid piece of {mat} (density {g(rho * 1000, 3)} kg/m³) is placed in {liq} (density {g(rl * 1000, 3)} kg/m³). Predict whether it floats or sinks and explain your answer.',
             f'It {"floats" if fl else "sinks"}, because its density is {"less" if fl else "greater"} than the density of the {liq}.', f'correct prediction [1]; comparison of densities [1] [2]')


@t12.add('C2', (2, 3, 4), 'explain')
def t12_err(r, D):
    mat, rho = r.choice([x for x in DENS if x[1] > 1.5])
    V = r.choice([4, 5, 8, 10, 12, 20])
    m = rho * V
    who = person(r)
    return Q(f'{who} calculates the density of a {mat} sample of mass {g(m, 3)} g and volume {V} cm³ as "{g(V / m, 3)} g/cm³". Identify the error, give the correct value and explain how {who} could have spotted the mistake.',
             f'{who} divided volume by mass; ρ = m/V = {g(rho, 3)} g/cm³. A value below 1 g/cm³ would mean a metal floats on water, which is unrealistic.',
             f'error: V/m instead of m/V [1]; correct {g(rho, 3)} g/cm³ [1]; sense check (metals are denser than water) [1] [3]')


def _dens_c4(r, D):
    mat, rho = r.choice([x for x in DENS if x[1] > 1.1])
    a, b, c = r.choice([2, 3, 4]), r.choice([2, 2.5, 5]), r.choice([1, 2, 3])
    V = a * b * c
    m = rho * V
    liq, rl = r.choice(LIQ)
    intro = r.choice([f'A jeweller in {city(r)} is offered a block said to be {mat}. It measures {a} cm × {g(b)} cm × {c} cm and has a mass of {g(m, 3)} g.',
                      f'{person(r)} is given a cuboid of an unknown material measuring {a} cm × {g(b)} cm × {c} cm. Its mass is {g(m, 3)} g.',
                      f'A metal sample in a school laboratory is a cuboid {a} cm by {g(b)} cm by {c} cm, with a mass of {g(m, 3)} g.'])
    parts = [
        lambda r: ('Calculate its volume.', f'{g(V)} cm³', f'V = {a} × {g(b)} × {c} = {g(V)} cm³ [1]'),
        lambda r: ('Calculate its density in g/cm³.', f'{g(rho, 3)} g/cm³', f'ρ = m/V = {g(m, 3)}/{g(V)} = {g(rho, 3)} g/cm³ [2]'),
        lambda r: ('Convert the density to kg/m³.', f'{g(rho * 1000, 3)} kg/m³', '× 1000 [1]'),
        lambda r: (f'State and explain whether it would float in {liq} of density {g(rl, 3)} g/cm³.', ('Floats' if rho < rl else 'Sinks') + f': its density is {"less" if rho < rl else "greater"} than {g(rl, 3)} g/cm³.', 'prediction with density comparison [2]'),
        lambda r: ('Describe a different method to find its volume that would also work for an irregular shape.', 'Lower it into a measuring cylinder of water (or displacement can) and find the rise in volume.', 'displacement method [1]; volume = rise in level [1] [2]'),
        lambda r: (f'A second block of the same material has twice the length, width and height. State its density and its mass.', f'Density unchanged at {g(rho, 3)} g/cm³; mass = 8 × {g(m, 3)} = {g(8 * m, 3)} g.', 'density same [1]; volume ×8 so mass ×8 [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t12.add('C4', (2, 3, 4, 5), 'multi_step')(_dens_c4)
t12.add('C3', (3, 4), 'multi_step')(_dens_c4)

N13 = 'Scalar and vector quantities and finding a resultant vector'
t13 = topic(N13, N13.lower(), 'scalar and vector', 'resultant vector')
VEC = ['force', 'weight', 'velocity', 'acceleration', 'momentum', 'displacement', 'gravitational field strength', 'electric field strength']
SCA = ['distance', 'speed', 'time', 'mass', 'energy', 'temperature', 'density', 'power', 'volume']
FX(t13, 'C1', (1, 2), [
    ('What is the difference between a scalar and a vector quantity?', 'A vector has magnitude and direction; a scalar has magnitude only', 'Vector: size and direction; scalar: size only.',
     ['A vector has magnitude only; a scalar has direction only', 'A scalar is always larger than a vector', 'A vector cannot be added; a scalar can']),
    ('Two forces of 5 N and 3 N act on an object in opposite directions. What is the resultant force?', '2 N in the direction of the 5 N force', 'Opposite directions: subtract; 5 − 3 = 2 N towards the larger force.', ['8 N', '2 N in the direction of the 3 N force', '15 N']),
    ('Two forces of 6 N and 8 N act at right angles. What is the magnitude of the resultant?', '10 N', '√(6² + 8²) = √100 = 10 N.', ['14 N', '2 N', '48 N']),
    ('Which method can be used to find the resultant of two forces at an angle other than 90°?', 'A scale drawing (parallelogram or triangle of vectors)', 'Draw the vectors to scale, tip to tail, and measure the resultant.', ['Adding their magnitudes', 'Subtracting their magnitudes', 'Multiplying their magnitudes']),
    ('State what is meant by the resultant of two vectors.', 'The single vector that has the same effect as the two vectors acting together.', 'single vector with same effect [1]'),
])
FX(t13, 'C2', (1, 2, 3, 4), [
    ('A runner completes one lap of a 400 m track and returns to the start. Explain why the distance is 400 m but the displacement is zero.', 'Distance is a scalar measuring the length of the path; displacement is a vector from start to finish, and start and finish are the same point.', 'distance = path length (scalar) [1]; displacement = straight-line from start to finish, here zero (vector) [1] [2]'),
    ('Explain why a car going round a roundabout at a steady 20 km/h has a changing velocity.', 'Velocity is a vector; the direction of motion is changing, so the velocity changes even though the speed is constant.', 'velocity has direction [1]; direction changes [1] [2]'),
    ('Explain why two forces of 4 N and 7 N cannot have a resultant of 12 N.', 'The largest resultant is when they act in the same direction: 4 + 7 = 11 N; any other angle gives less.', 'maximum is sum 11 N [1]; so 12 N impossible [1] [2]'),
    ('A student says "temperature is a vector because it can be negative". Explain why the student is wrong.', 'A negative temperature only means below zero on the scale; it has no direction in space, so it is a scalar.', 'negative sign is not a direction [1]; temperature has magnitude only [1] [2]'),
    ('Explain how to use a scale drawing to find the resultant of two forces acting at 60° to each other.', 'Choose a scale; draw one force as an arrow of the right length, then draw the second from its tip at the correct angle; the line from the start to the final tip is the resultant: measure its length and angle.', 'scale chosen [1]; tip-to-tail at correct angle [1]; measure length and direction of closing side [1] [3]'),
])


@t13.add('C1', (1, 2, 3))
def t13_class(r, D):
    if r.random() < 0.5:
        v = r.choice(VEC)
        opts, a = mcq(r, v, r.sample(SCA, 3))
        return Q(f'Which of these quantities is a vector?', a, f'{cap(v)} has both magnitude and direction; the others are scalars.', opts=opts) if D < 3 else \
            Q(f'Which of these is a vector quantity: {", ".join(opts)}? Give a reason.', f'{cap(v)}: it has direction as well as magnitude.', 'correct choice [1]; reason [1] [2]', 'short')
    s = r.choice(SCA)
    opts, a = mcq(r, s, r.sample(VEC, 3))
    return Q('Which of these quantities is a scalar?', a, f'{cap(s)} has magnitude only.', opts=opts) if D < 3 else \
        Q(f'Which of these is a scalar quantity: {", ".join(opts)}? Give a reason.', f'{cap(s)}: it has magnitude only, no direction.', 'correct choice [1]; reason [1] [2]', 'short')


PERP = [('A boat heads straight across a river at {a} m/s while the current flows downstream at {b} m/s.', 'velocity', 'm/s'),
        ('An aircraft flies due north at {a} m/s in a wind blowing due east at {b} m/s.', 'velocity', 'm/s'),
        ('Two tugboats pull a ship with forces of {a} kN and {b} kN at right angles to each other.', 'force', 'kN'),
        ('{p} pulls a sledge with a force of {a} N forwards while {q} pulls it sideways with {b} N, at right angles.', 'force', 'N'),
        ('A hiker walks {a} km due east and then {b} km due north.', 'displacement', 'km'),
        ('A drone flies at {a} m/s due west while a wind blows it due south at {b} m/s.', 'velocity', 'm/s')]
TRIPLES = [(3, 4), (6, 8), (5, 12), (8, 15), (9, 12), (12, 16), (7, 24), (20, 21), (2, 5), (4, 7), (10, 6), (15, 9), (30, 40), (120, 50)]


@t13.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_perp(r, D):
    fr, kind, u = r.choice(PERP)
    a, b = r.choice(TRIPLES)
    p, q2 = two_people(r)
    s = fr.format(a=a, b=b, p=p, q=q2)
    R = math.hypot(a, b)
    ang = math.degrees(math.atan(b / a))
    if D <= 2:
        return numq(r, D, s, f'magnitude of the resultant {kind}', R, ' ' + u, f'R = √({a}² + {b}²)', [a + b, abs(a - b), R * R])
    if D == 3:
        return Q(s + f' Calculate the magnitude of the resultant {kind} and the angle it makes with the {a} {u} vector.', f'{g(R)} {u} at {g(ang, 3)}°',
                 f'R = √({a}² + {b}²) = {g(R)} {u} [1]; tan θ = {b}/{a} [1]; θ = {g(ang, 3)}° [1] [3]')
    return Q(s + f' (a) Calculate the magnitude of the resultant {kind}. (b) Calculate its direction relative to the {a} {u} vector. (c) Explain why the answer to (a) is less than {a + b} {u}.',
             f'(a) {g(R)} {u} (b) {g(ang, 3)}° (c) the vectors are not in the same direction; only parallel vectors add arithmetically.',
             f'(a) Pythagoras [1] = {g(R)} {u} [1] (b) tan θ = {b}/{a} [1]; {g(ang, 3)}° [1] (c) direction matters for vectors [1] [5]' if D >= 5 else
             f'(a) Pythagoras = {g(R)} {u} [1] (b) tan θ = {b}/{a} [1]; {g(ang, 3)}° [1] (c) vectors not parallel [1] [4]', 'multi_step')


LINE = [('a tug-of-war rope', 'team'), ('a box pushed across a floor', 'push'), ('a car on a straight road', 'force'), ('a boat being rowed against the wind', 'force'), ('a crate being pulled by two ropes in a line', 'pull')]


@t13.add('C3', (1, 2, 3), 'numerical')
def t13_line(r, D):
    ctx, _ = r.choice(LINE)
    f1 = r.choice([120, 150, 200, 250, 300, 340, 400, 480])
    f2 = r.choice([60, 80, 90, 100, 140, 160, 180, 220])
    f3 = r.choice([10, 20, 30, 40, 50])
    if D == 3:
        R = f1 + f3 - f2
        return Q(f'Forces act along a straight line on {ctx}: {f1} N and {f3} N to the right, and {f2} N to the left. Calculate the resultant force, giving its direction, and state whether the forces are balanced.',
                 f'{abs(R)} N to the {"right" if R > 0 else "left"}; not balanced.' if R else '0 N; balanced.', f'R = {f1} + {f3} − {f2} [1] = {abs(R)} N [1]; direction / balanced statement [1] [3]')
    R = f1 - f2
    return numq(r, D, f'Two forces act on {ctx} along the same line in opposite directions: {f1} N to the right and {f2} N to the left.', 'resultant force (to the right)', R, ' N', f'R = {f1} − {f2}', [f1 + f2, R / 2])


@t13.add('C4', (3, 4, 5), 'multi_step')
def t13_scale(r, D):
    a, b = r.choice([(30, 40), (40, 30), (50, 20), (60, 25), (35, 35), (45, 20)])
    th = r.choice([60, 90, 120]) if D >= 4 else 90
    R = math.sqrt(a * a + b * b + 2 * a * b * math.cos(math.radians(th)))
    sc = r.choice([5, 10])
    ctx = r.choice(['Two ropes pull a stuck car out of mud.', 'Two dogs pull on a toy with leads attached to the same point.', 'Two cables hold a load at a construction site in ' + city(r) + '.'])
    return compose(r, f'{ctx} The forces are {a} N and {b} N and the angle between them is {th}°.', [
        lambda r: (f'Using a scale of 1 cm to {sc} N, describe how to draw a scale diagram to find the resultant.', f'Draw a {g(a / sc)} cm arrow, then from its tip a {g(b / sc)} cm arrow at {180 - th}° to it (angle between vectors {th}°); join start to finish and measure.', 'arrow lengths correct for scale [1]; tip-to-tail at correct angle [1]; measure closing side [1] [3]'),
        lambda r: ('State the magnitude of the resultant (from an accurate drawing).', f'about {g(R, 2)} N', f'{g(R, 3)} N (accept ±1 N) [2]'),
        lambda r: ('Explain why the resultant is smaller than the sum of the two forces.', 'The forces are not in the same direction, so part of each force acts in different directions.', 'direction matters for vectors [1]'),
        lambda r: ('State how the resultant changes if the angle between the forces is reduced.', 'It increases, towards a maximum of the sum when the angle is 0°.', 'increases [1]; max = sum at 0° [1] [2]'),
    ], k=(2, 3, 4), type_='multi_step')


CHAPTERS[1] = [t11, t12, t13]

# =========================================================== 2 Describing motion
N21 = 'Speed and velocity: v = s/t and average speed'
t21 = topic(N21, N21.lower(), 'speed and velocity', 'average speed')
FX(t21, 'C1', (1, 2), [
    ('Which equation is used to calculate average speed?', 'average speed = total distance ÷ total time', 'v = s/t using totals for the whole journey.', ['average speed = total time ÷ total distance', 'average speed = distance × time', 'average speed = (first speed + last speed) ÷ 2 always']),
    ('What is the SI unit of speed?', 'm/s', 'Metres per second.', ['km/h', 'm/s²', 'm s']),
    ('Velocity differs from speed because velocity', 'includes direction', 'Velocity is speed in a given direction (a vector).', ['is always larger', 'is measured in different units', 'can only be used for cars']),
    ('A speed of 36 km/h is the same as', '10 m/s', '36 km/h = 36 000 m / 3600 s = 10 m/s.', ['36 m/s', '3.6 m/s', '100 m/s']),
    ('A train travels 120 km in 2 hours. What is its average speed?', '60 km/h', '120/2 = 60 km/h.', ['240 km/h', '30 km/h', '122 km/h']),
    ('State the difference between average speed and instantaneous speed.', 'Average speed is total distance ÷ total time for a journey; instantaneous speed is the speed at a particular moment.', 'both correctly described [2]'),
])
FX(t21, 'C2', (1, 2, 3, 4), [
    ('Explain why the average speed for a whole journey is not usually equal to the mean of the speeds on each part.', 'The parts usually take different times; average speed = total distance ÷ total time, so slower parts (which last longer) count more.', 'definition with totals [1]; parts take different times [1] [2]'),
    ('Describe how to measure the average speed of a cyclist using equipment in a school.', 'Measure a distance along the road with a tape (e.g. 100 m); time the cyclist over it with a stopwatch; speed = distance ÷ time; repeat and average.', 'measure distance with tape [1]; time with stopwatch [1]; v = s/t [1] [3]'),
    ('Two cars travel at 50 km/h, one north and one south. Explain whether they have the same speed and the same velocity.', 'Same speed (50 km/h) but different velocities because they move in different directions.', 'same speed [1]; velocity differs due to direction [1] [2]'),
    ('Explain why light gates connected to a timer give a more accurate speed than a hand-held stopwatch.', 'Light gates start and stop the timer automatically, removing human reaction-time error, and can time very short intervals.', 'no reaction time [1]; short intervals measured precisely [1] [2]'),
])
TRIPS = [('{p} cycles to school', (2, 9), 'km', 'min'), ('A bus in {c} travels between two stops', (0.6, 3), 'km', 'min'), ('A sprinter runs', (100, 400), 'm', 's'),
         ('A train travels between two stations near {c}', (20, 180), 'km', 'h'), ('A tortoise crawls', (2, 12), 'm', 'min'), ('A swimmer swims', (50, 400), 'm', 's'),
         ('A ferry crosses a bay from {k}', (5, 30), 'km', 'min'), ('A delivery drone flies', (1, 8), 'km', 'min')]


@t21.add('C3', (1, 2, 3, 4), 'numerical')
def t21_speed(r, D):
    fr, (lo, hi), du, tu = r.choice(TRIPS)
    s = fr.format(p=person(r), c=city(r), k=coast(r))
    d = r.choice([lo, (lo + hi) / 2, hi, lo * 2 if lo * 2 < hi else hi]) if du != 'm' or hi < 50 else r.choice([100, 200, 400] if hi == 400 else [lo, hi])
    t = {'min': r.choice([4, 5, 8, 10, 12, 15, 20, 25, 30]), 's': r.choice([12, 20, 25, 40, 50, 60, 80, 100]), 'h': r.choice([0.5, 1, 1.5, 2, 2.5])}[tu]
    if tu == 's' and du == 'm' and hi == 400:
        t = round(d / r.uniform(6.5, 9.5), 1)
    if tu == 's' and 'swim' in s:
        t = round(d / r.uniform(1.2, 2.0))
    d = round(d, 1)
    if D <= 2:
        v = d / t
        return numq(r, D, f'{s} {g(d)} {du} in {g(t)} {tu}.', f'average speed in {du}/{tu}', v, f' {du}/{tu}', f'v = s/t = {g(d)}/{g(t)}', [t / d, d * t, v * 2])
    dm = d * (1000 if du == 'km' else 1)
    ts = t * {'min': 60, 's': 1, 'h': 3600}[tu]
    v = dm / ts
    if D == 3:
        return Q(f'{s} {g(d)} {du} in {g(t)} {tu}. Calculate the average speed in m/s.', f'{g(v)} m/s', f'convert: {g(dm)} m and {g(ts)} s [1]; v = s/t [1] = {g(v)} m/s [1] [3]')
    t2 = round(t * r.choice([1.5, 2, 2.5]), 1)
    tm = round(t * r.choice([0.2, 0.25, 0.5]), 1)
    tot_t = t + tm + t2
    d2 = round(d * r.choice([0.5, 1, 1.5]), 1)
    av = (d + d2) / tot_t
    return Q(f'{s} {g(d)} {du} in {g(t)} {tu}, stops for {g(tm)} {tu}, then travels a further {g(d2)} {du} in {g(t2)} {tu}. (a) Calculate the speed on the first part. (b) Calculate the average speed for the whole journey in {du}/{tu}. (c) Explain why (b) is not the mean of the two moving speeds.',
             f'(a) {g(d / t)} {du}/{tu} (b) {g(av)} {du}/{tu} (c) the stop adds time without distance and the parts take different times.',
             f'(a) {g(d)}/{g(t)} = {g(d / t)} {du}/{tu} [1] (b) total distance {g(d + d2)} {du} [1]; total time {g(tot_t)} {tu} [1]; = {g(av)} {du}/{tu} [1] (c) stop / unequal times [1] [5]', 'multi_step')


@t21.add('C3', (1, 2, 3, 4), 'numerical')
def t21_rearr(r, D):
    v = r.choice([1.5, 2.5, 4, 8, 12, 15, 20, 25, 30, 340])
    t = r.choice([5, 8, 12, 20, 30, 45, 90])
    obj = {340: 'Sound'}.get(v, r.choice(['A car', 'A cyclist', 'A runner', 'A horse', 'A motorbike', 'A rowing boat']))
    if r.random() < 0.5:
        d = v * t
        return numq(r, D, f'{obj} moves at a constant speed of {g(v)} m/s for {t} s.', 'distance travelled', d, ' m', f's = vt = {g(v)} × {t}', [v / t, t / v, d / 2])
    d = v * t
    return numq(r, D, f'{obj} travels {g(d)} m at a constant speed of {g(v)} m/s.', 'time taken', t, ' s', f't = s/v = {g(d)}/{g(v)}', [d * v, v / d * 1000, t * 2])


@t21.add('C2', (2, 3, 4), 'explain')
def t21_wrong(r, D):
    v1, v2 = r.sample([20, 30, 40, 60, 80, 90, 100], 2)
    d = r.choice([60, 120, 240, 360])
    av = 2 * d / (d / v1 + d / v2)
    who = person(r)
    return Q(f'{who} drives {d} km at {v1} km/h and then another {d} km at {v2} km/h. {who} says the average speed is {(v1 + v2) / 2:g} km/h. Explain why this is wrong and calculate the correct average speed.',
             f'The slower half takes longer, so it counts more; average = {2 * d}/({g(d / v1)} + {g(d / v2)}) = {g(av)} km/h.',
             f'times are unequal [1]; times {g(d / v1)} h and {g(d / v2)} h [1]; average = total distance/total time = {g(av)} km/h [1] [3]')


def _speed_c4(r, D):
    who = person(r)
    d1, t1 = r.choice([(1.2, 6), (2.4, 10), (1.5, 5), (3.0, 12)])
    tw = r.choice([4, 5, 8, 10])
    d2, t2 = r.choice([(3.6, 9), (4.5, 15), (6.0, 15), (2.0, 4)])
    tot = (d1 + d2) * 1000 / ((t1 + tw + t2) * 60)
    intro = r.choice([f'{who} travels to a market in {city(r)}: walks {d1} km in {t1} min, waits {tw} min for a bus, then rides {d2} km in {t2} min.',
                      f'A courier in {city(r)} jogs {d1} km in {t1} min, waits {tw} min at a crossing, then cycles {d2} km in {t2} min.'])
    parts = [
        lambda r: ('Calculate the average speed for the first stage in m/s.', f'{g(d1 * 1000 / (t1 * 60))} m/s', f'{g(d1 * 1000)} m / {t1 * 60} s = {g(d1 * 1000 / (t1 * 60))} m/s [2]'),
        lambda r: ('Calculate the average speed for the whole journey in m/s.', f'{g(tot)} m/s', f'total distance {g((d1 + d2) * 1000)} m [1]; total time {(t1 + tw + t2) * 60} s [1]; = {g(tot)} m/s [1] [3]'),
        lambda r: ('Calculate the speed for the last stage in km/h.', f'{g(d2 / (t2 / 60))} km/h', f'{d2} km / {g(t2 / 60, 3)} h = {g(d2 / (t2 / 60))} km/h [2]'),
        lambda r: ('Explain the difference between the speed shown on the bus speedometer and the average speed for the bus ride.', 'The speedometer shows instantaneous speed at each moment; the average is total distance ÷ total time, including speeding up and slowing down.', 'instantaneous vs average [2]'),
        lambda r: ('State one reason why the journey has a velocity that changes even if the speed were steady.', 'The direction of travel changes (turns in the road), and velocity is a vector.', 'direction changes [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t21.add('C4', (2, 3, 4, 5), 'multi_step')(_speed_c4)

N22 = 'Distance-time graphs and gradient as speed'
t22 = topic(N22, N22.lower(), 'distance-time graphs', 'gradient as speed')
FX(t22, 'C1', (1, 2), [
    ('On a distance-time graph, what does a horizontal line show?', 'The object is stationary', 'Distance not changing → at rest.', ['Constant speed', 'Constant acceleration', 'Deceleration']),
    ('On a distance-time graph, what does the gradient represent?', 'Speed', 'Gradient = Δdistance/Δtime = speed.', ['Acceleration', 'Distance travelled', 'Time taken']),
    ('A straight, sloping line on a distance-time graph shows', 'constant speed', 'Constant gradient → constant speed.', ['increasing speed', 'stationary object', 'decreasing acceleration']),
    ('A distance-time graph that curves upwards (gets steeper) shows an object that is', 'accelerating', 'Increasing gradient → increasing speed.', ['decelerating', 'at rest', 'moving at constant speed']),
    ('On a distance-time graph, the steeper of two straight lines shows', 'the greater speed', 'Larger gradient = larger speed.', ['the smaller speed', 'the longer time', 'the shorter distance']),
    ('Describe how to find the speed at one instant from a curved distance-time graph.', 'Draw a tangent to the curve at that time and find its gradient.', 'tangent [1]; gradient of tangent [1] [2]'),
])
FX(t22, 'C2', (1, 2, 3, 4), [
    ('Explain why a distance-time graph can never slope downwards, but a displacement-time graph can.', 'Distance travelled can only increase or stay the same; displacement is measured from the start and can decrease when the object comes back.', 'distance never decreases [1]; displacement can return towards start [1] [2]'),
    ('Two runners start together. On a distance-time graph, runner A’s line is steeper than runner B’s. Explain what this shows and who wins a race of fixed length.', 'A has the greater speed (bigger gradient), so A covers the fixed distance in less time and wins.', 'steeper = faster [1]; A wins [1] [2]'),
    ('Explain how a distance-time graph shows that a car is slowing down.', 'The gradient (slope) decreases with time: the curve becomes less steep, flattening out.', 'gradient = speed [1]; decreasing gradient / flattening [1] [2]'),
    ('Describe the shape of the distance-time graph for a ball thrown up a short distance, falling back, considering total distance travelled.', 'The line rises with decreasing gradient to the top (slowing), then continues rising with increasing gradient as it falls (speeding up); it never goes down.', 'decreasing gradient up [1]; increasing gradient on way down [1]; always increasing [1] [3]'),
])
DT_OBJ = ['a cyclist', 'a delivery van', 'a jogger', 'a model train', 'a remote-controlled car', 'a lift moving up a tower in {c}', 'a ferry']


def _dt_graph(r):
    t1, s1 = r.choice([(10, 50), (20, 80), (20, 120), (30, 150), (40, 200), (15, 90), (25, 100)])
    tw = r.choice([10, 15, 20])
    t3 = r.choice([10, 20, 25, 30])
    s3 = r.choice([50, 60, 100, 150, 200])
    pts = [(0, 0), (t1, s1), (t1 + tw, s1), (t1 + tw + t3, s1 + s3)]
    return pts


@t22.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_graph(r, D):
    o = r.choice(DT_OBJ).format(c=city(r))
    pts = _dt_graph(r)
    desc = 'The distance-time graph for ' + o + ' is made of straight lines joining (' + '), ('.join(f'{a} s, {b} m' for a, b in pts) + ').'
    (t0, s0), (t1, s1), (t2, s2), (t3, s3) = pts
    v1 = s1 / t1
    v3 = (s3 - s2) / (t3 - t2)
    if D <= 2:
        return numq(r, D, desc, 'speed during the first section', v1, ' m/s', f'gradient = {s1}/{t1}', [t1 / s1, s1 * t1 / 100, s3 / t3])
    if D == 3:
        return Q(desc + ' Describe the motion in each section and calculate the speed in the last section.', f'Constant speed {g(v1)} m/s; stationary for {t2 - t1} s; constant speed {g(v3)} m/s.',
                 f'section 1 constant speed [1]; section 2 stationary [1]; last section gradient = {s3 - s2}/{t3 - t2} = {g(v3)} m/s [1] [3]')
    av = s3 / t3
    return Q(desc + ' (a) Calculate the speed in the first and last sections. (b) Calculate the average speed for the whole motion. (c) State in which section the object was fastest and explain how the graph shows this.',
             f'(a) {g(v1)} m/s and {g(v3)} m/s (b) {g(av)} m/s (c) {"first" if v1 > v3 else "last"} section: steepest gradient.',
             f'(a) {s1}/{t1} = {g(v1)} m/s [1]; {s3 - s2}/{t3 - t2} = {g(v3)} m/s [1] (b) {s3}/{t3} [1] = {g(av)} m/s [1] (c) steepest line [1] [5]' if D >= 5 else
             f'(a) {g(v1)} m/s and {g(v3)} m/s [2] (b) {s3}/{t3} = {g(av)} m/s [1] (c) steepest gradient [1] [4]', 'multi_step')


@t22.add('C3', (2, 3, 4), 'numerical')
def t22_table(r, D):
    v = r.choice([1.5, 2, 2.5, 3, 4, 5, 6])
    dt = r.choice([2, 4, 5])
    ts = [i * dt for i in range(6)]
    ds = [round(v * t, 1) for t in ts]
    bad = r.randrange(2, 5)
    ds2 = ds[:]
    ds2[bad] = round(ds[bad] + r.choice([-1, 1]) * v * dt * 0.4, 1)
    o = r.choice(['a toy car rolling along a corridor', 'a trolley on a level bench', 'a snail on a ruler (distance in mm, time in s)', 'a bubble rising in a tube of oil (distance in cm)'])
    unit = 'mm' if 'mm' in o else 'cm' if 'cm' in o else 'm'
    o = o.split(' (')[0]
    return Q(f'Readings for {o}: time/s = {", ".join(map(str, ts))}; distance/{unit} = {", ".join(g(x) for x in ds2)}. (a) Identify the anomalous reading. (b) Using the other readings, determine the speed. (c) Describe the shape of the distance-time graph you would draw.',
             f'(a) {g(ds2[bad])} {unit} at {ts[bad]} s (b) {g(v)} {unit}/s (c) a straight line through the origin (constant speed).',
             f'(a) anomaly identified [1] (b) gradient = {g(ds[-1])}/{ts[-1]} = {g(v)} {unit}/s [2] (c) straight line through origin [1] [4]', 'case')


@t22.add('C2', (2, 3, 4), 'explain')
def t22_compare(r, D):
    a, b = two_people(r)
    va, vb = r.sample([2, 3, 4, 5, 6, 8], 2)
    ta = r.choice([0, 0, 5, 10])
    return Q(f'{a} and {b} walk along the same path. On a distance-time graph, {a}’s line is straight with gradient {va} m/s and {b}’s is straight with gradient {vb} m/s{"; " + b + " starts " + str(ta) + " s later" if ta else ""}. Compare their motion and state who reaches a point 120 m along the path first.',
             f'Both move at constant speed; {a if va > vb else b} is faster. Times: {a} {g(120 / va)} s, {b} {g(ta + 120 / vb)} s, so {a if 120 / va < ta + 120 / vb else b} arrives first.',
             f'both constant speed [1]; compares speeds via gradient [1]; times calculated [1]; correct conclusion [1] [4]' if ta else 'both constant speed [1]; compares gradients [1]; correct conclusion with times [1] [3]')


def _dt_c4(r, D):
    o = r.choice(DT_OBJ).format(c=city(r))
    pts = _dt_graph(r)
    (t0, s0), (t1, s1), (t2, s2), (t3, s3) = pts
    intro = f'A distance-time graph for {o} is made of straight lines joining (' + '), ('.join(f'{a} s, {b} m' for a, b in pts) + ').'
    parts = [
        lambda r: ('Describe the motion between ' + f'{t1} s and {t2} s.', 'Stationary (distance constant).', '[1]'),
        lambda r: ('Calculate the speed in the first section.', f'{g(s1 / t1)} m/s', f'gradient = {s1}/{t1} [2]'),
        lambda r: ('Calculate the speed in the last section.', f'{g((s3 - s2) / (t3 - t2))} m/s', f'({s3} − {s2})/({t3} − {t2}) [2]'),
        lambda r: ('Calculate the average speed for the whole motion.', f'{g(s3 / t3)} m/s', f'{s3}/{t3} [2]'),
        lambda r: ('In reality the changes in speed are not instant. Describe how the graph would really look at the corners.', 'The corners would be smooth curves, showing the object speeding up or slowing down gradually.', 'curved corners [1]; gradual change of speed [1] [2]'),
        lambda r: ('Sketch-describe the speed-time graph for the same motion.', f'Horizontal line at {g(s1 / t1)} m/s, then at 0 from {t1} s to {t2} s, then horizontal at {g((s3 - s2) / (t3 - t2))} m/s.', 'three levels correct [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t22.add('C4', (2, 3, 4, 5), 'multi_step')(_dt_c4)

N23 = 'Speed-time graphs, acceleration and distance from area under the graph'
t23 = topic(N23, N23.lower(), 'speed-time graphs', 'acceleration')
FX(t23, 'C1', (1, 2), [
    ('What does the gradient of a speed-time graph represent?', 'Acceleration', 'Gradient = Δv/Δt = acceleration.', ['Distance', 'Speed', 'Time']),
    ('What does the area under a speed-time graph represent?', 'Distance travelled', 'Area = speed × time = distance.', ['Acceleration', 'Speed', 'Force']),
    ('What is the unit of acceleration?', 'm/s²', 'Change in velocity (m/s) per second.', ['m/s', 'm²/s', 'N/kg²']),
    ('A horizontal line on a speed-time graph shows', 'constant speed', 'Speed not changing: zero acceleration.', ['the object is at rest', 'constant acceleration', 'deceleration']),
    ('A car increases its speed from 10 m/s to 30 m/s in 5 s. What is its acceleration?', '4 m/s²', 'a = (30 − 10)/5 = 4 m/s².', ['6 m/s²', '8 m/s²', '20 m/s²']),
    ('A line sloping downwards on a speed-time graph shows', 'deceleration', 'Negative gradient → decreasing speed.', ['the object is moving backwards', 'constant speed', 'the object is at rest']),
    ('Define acceleration.', 'The change in velocity per unit time (a = Δv/Δt).', 'change of velocity [1] per unit time [1] [2]'),
])
FX(t23, 'C2', (1, 2, 3, 4), [
    ('Explain how a speed-time graph shows that the acceleration of an object is decreasing.', 'The line is curved with a decreasing gradient (becoming less steep).', 'gradient = acceleration [1]; gradient decreasing [1] [2]'),
    ('A student says "a negative acceleration means the object is moving backwards". Explain why this is not necessarily true.', 'Negative acceleration means the velocity is decreasing (deceleration) in the direction of motion; the object can still be moving forwards while slowing down.', 'means slowing down [1]; can still move forward [1] [2]'),
    ('Explain why the distance travelled by a car that accelerates uniformly from rest is half of speed × time.', 'The area under the speed-time graph is a triangle: ½ × base × height = ½ × t × v.', 'area under graph = distance [1]; triangle area ½vt [1] [2]'),
    ('Describe the motion shown by a speed-time graph that rises steeply, levels off, then falls to zero.', 'The object accelerates from rest, travels at constant speed, then decelerates to a stop.', 'accelerates [1]; constant speed [1]; decelerates to rest [1] [3]'),
])
VEH = ['A car', 'A bus', 'A motorbike', 'A train', 'An aircraft on a runway', 'A sprinter', 'A cyclist']


def veh(r, v):
    """A moving object for which a top speed of v m/s is realistic (None if none fits)."""
    opts = []
    if v <= 10:
        opts += ['A sprinter', 'A cyclist', 'A horse']
    if v <= 15:
        opts += ['A cyclist', 'An electric scooter']
    if v <= 25:
        opts += ['A bus', 'A tram']
    if v <= 45:
        opts += ['A car', 'A motorbike', 'A train']
    if 20 <= v <= 90:
        opts += ['An aircraft on a runway', 'A high-speed train']
    return r.choice(opts) if opts else None


@t23.add('C3', (1, 2, 3, 4), 'numerical')
def t23_acc(r, D):
    u = r.choice([0, 0, 2, 4, 5, 8, 10, 12, 15])
    a = r.choice([0.5, 0.8, 1.2, 1.5, 2, 2.5, 3, 4])
    t = r.choice([2, 4, 5, 6, 8, 10, 12, 15])
    v = u + a * t
    o = veh(r, v)
    if not o:
        return None
    st = f'{o} starts from rest and reaches {g(v)} m/s in {t} s.' if u == 0 else f'{o} travelling at {g(u)} m/s speeds up to {g(v)} m/s in {t} s.'
    if D <= 3:
        return numq(r, D, st, 'acceleration', a, ' m/s²', f'a = Δv/Δt = ({g(v)} − {g(u)})/{t}', [v / t, (v + u) / t, a * t])
    if r.random() < 0.5:
        dec = r.choice([1.5, 2, 2.5, 4, 5])
        tt = v / dec
        return Q(f'{o} travelling at {g(v)} m/s slows down with a constant deceleration of {g(dec)} m/s². Calculate the time taken to stop and the braking distance.', f'{g(tt)} s; {g(0.5 * v * tt)} m',
                 f't = Δv/a = {g(v)}/{g(dec)} = {g(tt)} s [2]; area = ½ × {g(tt)} × {g(v)} = {g(0.5 * v * tt)} m [2] [4]', 'multi_step')
    return Q(st + ' Calculate the acceleration and the distance travelled in this time.', f'{g(a)} m/s²; {g((u + v) / 2 * t)} m',
             f'a = ({g(v)} − {g(u)})/{t} = {g(a)} m/s² [2]; distance = area = ½({g(u)} + {g(v)}) × {t} = {g((u + v) / 2 * t)} m [2] [4]', 'multi_step')


def _vt(r):
    v = r.choice([6, 8, 10, 12, 15, 18, 20, 24, 25, 30])
    t1 = r.choice([2, 4, 5, 6, 8, 10])
    t2 = r.choice([10, 15, 20, 30])
    t3 = r.choice([3, 4, 5, 6, 10])
    return v, t1, t2, t3


@t23.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_area(r, D):
    v, t1, t2, t3 = _vt(r)
    o = veh(r, v)
    s1, s2, s3 = 0.5 * v * t1, v * t2, 0.5 * v * t3
    desc = f'{o} accelerates uniformly from rest to {v} m/s in {t1} s, travels at {v} m/s for {t2} s, then decelerates uniformly to rest in {t3} s.'
    if D <= 2:
        return numq(r, D, desc, 'distance travelled while accelerating', s1, ' m', f'area = ½ × {t1} × {v}', [v * t1, v / t1, s1 * 4])
    if D == 3:
        return Q(desc + ' Use the speed-time graph to calculate the total distance travelled.', f'{g(s1 + s2 + s3)} m', f'triangles ½×{t1}×{v} + ½×{t3}×{v} [1]; rectangle {t2}×{v} [1]; total {g(s1 + s2 + s3)} m [1] [3]')
    tot = t1 + t2 + t3
    return Q(desc + ' (a) Calculate the acceleration and the deceleration. (b) Calculate the total distance. (c) Calculate the average speed for the whole journey.',
             f'(a) {g(v / t1)} m/s² and {g(v / t3)} m/s² (b) {g(s1 + s2 + s3)} m (c) {g((s1 + s2 + s3) / tot)} m/s',
             f'(a) {v}/{t1} [1]; {v}/{t3} [1] (b) sum of areas = {g(s1 + s2 + s3)} m [2] (c) ÷ {tot} s = {g((s1 + s2 + s3) / tot)} m/s [1] [5]' if D >= 5 else
             f'(a) {v}/{t1} and {v}/{t3} [1] (b) areas = {g(s1 + s2 + s3)} m [2] (c) ÷ {tot} s = {g((s1 + s2 + s3) / tot)} m/s [1] [4]', 'multi_step')


@t23.add('C2', (2, 3, 4), 'explain')
def t23_err(r, D):
    v, t1, t2, t3 = _vt(r)
    who = person(r)
    return Q(f'A car accelerates uniformly from rest to {v} m/s in {t1} s. {who} calculates the distance travelled as {v} × {t1} = {v * t1} m. Explain the mistake and give the correct distance.',
             f'{who} used the area of a rectangle; the speed was not {v} m/s throughout. Area of triangle = ½ × {t1} × {v} = {g(0.5 * v * t1)} m.',
             f'identifies rectangle instead of triangle / average speed is {g(v / 2)} m/s [1]; correct {g(0.5 * v * t1)} m [1] [2]')


def _vt_c4(r, D):
    v, t1, t2, t3 = _vt(r)
    o = veh(r, v)
    intro = f'{o} accelerates uniformly from rest to {v} m/s in {t1} s, travels at constant speed for {t2} s and then decelerates uniformly to rest in {t3} s.'
    s = 0.5 * v * t1 + v * t2 + 0.5 * v * t3
    parts = [
        lambda r: ('Calculate the acceleration in the first stage.', f'{g(v / t1)} m/s²', f'a = {v}/{t1} [2]'),
        lambda r: ('Calculate the deceleration in the last stage.', f'{g(v / t3)} m/s²', f'{v}/{t3} [1]'),
        lambda r: ('Calculate the total distance travelled.', f'{g(s)} m', 'areas of two triangles and a rectangle [1]; total [2] [3]'),
        lambda r: ('Calculate the average speed for the whole journey.', f'{g(s / (t1 + t2 + t3))} m/s', f'{g(s)}/{t1 + t2 + t3} [2]'),
        lambda r: ('State the resultant force on the vehicle during the constant-speed stage and explain.', 'Zero: the speed is constant so there is no acceleration (forces balanced).', 'zero [1]; no acceleration [1] [2]'),
        lambda r: ('Describe how the graph would differ if the deceleration were not uniform but became less as the vehicle slowed.', 'The last section would be a curve that becomes less steep as it approaches zero speed.', 'curve [1]; decreasing gradient [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t23.add('C4', (2, 3, 4, 5), 'multi_step')(_vt_c4)
t23.add('C3', (4, 5), 'multi_step')(_vt_c4)

N24 = 'Acceleration of free fall g'
t24 = topic(N24, N24.lower(), 'free fall')
FX(t24, 'C1', (1, 2), [
    ('What is the approximate acceleration of free fall near the Earth’s surface?', '9.8 m/s²', 'g ≈ 9.8 m/s² (often rounded to 10 m/s²).', ['1.6 m/s²', '98 m/s²', '0.98 m/s²']),
    ('In a vacuum, a feather and a hammer are dropped together. Which statement is correct?', 'They hit the ground at the same time', 'With no air resistance all objects fall with the same acceleration g.', ['The hammer lands first', 'The feather lands first', 'The feather does not fall']),
    ('An object falls freely from rest. What is its speed after 2 s? (g = 9.8 m/s²)', '19.6 m/s', 'v = gt = 9.8 × 2 = 19.6 m/s.', ['9.8 m/s', '4.9 m/s', '39.2 m/s']),
    ('The acceleration of free fall on the Moon is about', '1.6 m/s²', 'g on the Moon is about one sixth of that on Earth.', ['9.8 m/s²', '0 m/s²', '25 m/s²']),
    ('State the meaning of "free fall".', 'Falling under the action of gravity alone, with no air resistance.', 'only gravity acting [1]'),
])
FX(t24, 'C2', (1, 2, 3, 4), [
    ('Explain why, in air, a sheet of paper falls more slowly than the same sheet crumpled into a ball.', 'The flat sheet has a larger surface area, so it experiences more air resistance; its resultant force and acceleration are smaller.', 'larger area → more air resistance [1]; smaller resultant force / acceleration [1] [2]'),
    ('Describe an experiment to measure g using a falling ball and light gates.', 'Drop a ball from rest through two light gates a measured distance apart; the timer records the speeds at each gate and the time between them; g = change in speed ÷ time.', 'drop from rest through light gates [1]; measure speeds and time [1]; g = Δv/Δt [1] [3]'),
    ('Explain why the acceleration of a dropped heavy ball is the same as that of a light ball (ignoring air resistance).', 'The heavier ball has a larger weight but also a larger mass; a = W/m = g for both.', 'larger weight and mass in proportion [1]; a = W/m = g [1] [2]'),
    ('Explain why a ball thrown upwards has an acceleration of 9.8 m/s² downwards even at the very top of its flight.', 'At the top its velocity is momentarily zero, but gravity (its weight) still acts, so it still accelerates downwards at g.', 'weight still acts [1]; acceleration is g downwards even when v = 0 [1] [2]'),
])
PLAN = [('Earth', 9.8), ('the Moon', 1.6), ('Mars', 3.7), ('Jupiter', 25), ('Venus', 8.9)]


@t24.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t24_fall(r, D):
    pl, gv = r.choice(PLAN) if D >= 3 else ('Earth', 9.8)
    t = r.choice([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0])
    obj = r.choice(['A stone', 'A coin', 'A tennis ball', 'A small steel ball', 'A dropped key', 'An apple'])
    v = gv * t
    if D <= 2:
        return numq(r, D, f'{obj} is dropped from rest near the Earth’s surface and falls freely for {g(t)} s (g = 9.8 m/s²).', 'speed reached', v, ' m/s', f'v = gt = 9.8 × {g(t)}', [v / 2, 9.8 / t, v * t])
    s = 0.5 * v * t
    if D == 3:
        return Q(f'{obj} is dropped from rest on {pl}, where g = {gv} m/s². Calculate its speed after {g(t)} s and the distance it has fallen (use the area under the speed-time graph).', f'{g(v)} m/s; {g(s)} m',
                 f'v = gt = {g(v)} m/s [1]; area = ½ × {g(t)} × {g(v)} [1] = {g(s)} m [1] [3]')
    t2 = r.choice([1.0, 1.5, 2.0])
    return Q(f'{obj} is dropped from rest from a cliff on Earth (g = 9.8 m/s²) and takes {g(t)} s to land. (a) Calculate its speed just before landing. (b) Calculate the height of the cliff. (c) The same experiment is repeated on {PLAN[2][0]} (g = 3.7 m/s²). Calculate the speed after {g(t2)} s there. (d) State one assumption.',
             f'(a) {g(v)} m/s (b) {g(s)} m (c) {g(3.7 * t2)} m/s (d) air resistance is negligible.',
             f'(a) v = 9.8 × {g(t)} = {g(v)} m/s [1] (b) ½ × {g(t)} × {g(v)} = {g(s)} m [2] (c) 3.7 × {g(t2)} = {g(3.7 * t2)} m/s [1] (d) no air resistance [1] [5]', 'multi_step')


@t24.add('C3', (2, 3, 4), 'case')
def t24_data(r, D):
    gv = round(r.uniform(9.2, 9.7), 2)
    t = r.choice([0.2, 0.25, 0.3, 0.4])
    u = round(r.uniform(0.8, 1.5), 2)
    v = round(u + gv * t, 2)
    who = person(r)
    return Q(f'In an experiment, {who} drops a card through two light gates. The speed at the upper gate is {u} m/s, the speed at the lower gate is {v} m/s and the time between gates is {t} s. (a) Calculate the acceleration. (b) Suggest why the value is not exactly 9.8 m/s².',
             f'(a) {g((v - u) / t)} m/s² (b) air resistance on the card acts upwards, reducing the resultant force and so the acceleration (also timing/measurement uncertainty).', f'(a) a = ({v} − {u})/{t} [1] = {g((v - u) / t)} m/s² [1] (b) air resistance or uncertainty [1] [3]')


def _g_c4(r, D):
    t = r.choice([2, 2.5, 3, 4])
    obj = r.choice(['a ball dropped from a tall bridge in ' + city(r), 'a parcel released from a hovering helicopter', 'a stone dropped down a deep well'])
    v = 9.8 * t
    parts = [
        lambda r: (f'Calculate the speed after {t} s, ignoring air resistance.', f'{g(v)} m/s', f'v = gt = 9.8 × {t} [2]'),
        lambda r: (f'Calculate the distance fallen in {t} s.', f'{g(0.5 * v * t)} m', f'area = ½ × {t} × {g(v)} [2]'),
        lambda r: ('Sketch-describe the speed-time graph if air resistance is ignored.', 'A straight line through the origin with gradient 9.8 m/s².', 'straight line from origin [1]; gradient g [1] [2]'),
        lambda r: ('Describe how the graph changes when air resistance is significant.', 'The gradient decreases as speed increases; the curve levels off at terminal velocity.', 'decreasing gradient [1]; levels off [1] [2]'),
        lambda r: ('State the acceleration at the start of the fall and explain.', '9.8 m/s²: at the start speed is zero, so air resistance is zero and only weight acts.', 'g [1]; no air resistance at v = 0 [1] [2]'),
    ]
    return compose(r, f'Consider {obj}.', parts, k=(2, 3, 4), type_='multi_step')


t24.add('C4', (2, 3, 4, 5), 'multi_step')(_g_c4)


@t24.add('C2', (2, 3, 4), 'explain')
def t24_claim(r, D):
    m1, m2 = r.sample([0.1, 0.5, 1, 2, 5, 10], 2)
    h = r.choice([1.5, 2, 5, 10, 20])
    who = person(r)
    heavy = max(m1, m2)
    return Q(f'{who} drops a {g(m1)} kg steel ball and a {g(m2)} kg steel ball together from a height of {g(h)} m and claims the {g(heavy)} kg ball "must land first because it is heavier". Explain whether {who} is correct, ignoring air resistance.',
             'Not correct: both fall with the same acceleration g = 9.8 m/s², because the larger weight acts on a proportionally larger mass (a = W/m = g), so they land together.',
             'land together [1]; same acceleration g [1]; weight ∝ mass so a = W/m = g [1] [3]' if D >= 3 else 'land together [1]; same acceleration g [1] [2]')


relation(t24, 'C2', (2, 3), 'v = gt', 'speed reached', {'time of fall': 1}, ['A stone is dropped from rest down a deep well (no air resistance).', 'A ball falls freely from rest on the Moon.', 'A coin is dropped from a tall tower, ignoring air resistance.'])

CHAPTERS[2] = [t21, t22, t23, t24]

# =========================================================== 3 Forces and motion
N31 = 'Mass, weight and gravitational field strength W = mg'
t31 = topic(N31, N31.lower(), 'mass, weight', 'gravitational field strength')
FX(t31, 'C1', (1, 2), [
    ('What is the unit of weight?', 'newton (N)', 'Weight is a force, measured in newtons.', ['kilogram (kg)', 'gram (g)', 'newton per kilogram (N/kg)']),
    ('Which statement about mass and weight is correct?', 'Mass is the same everywhere; weight depends on gravitational field strength', 'Mass = amount of matter; weight = gravitational force = mg.', ['Weight is the same everywhere; mass depends on gravity', 'Mass and weight are the same thing', 'Both are measured in newtons']),
    ('What is the weight of a 2.0 kg bag on Earth (g = 9.8 N/kg)?', '19.6 N', 'W = mg = 2.0 × 9.8 = 19.6 N.', ['2.0 N', '9.8 N', '0.20 N']),
    ('Which instrument measures weight directly?', 'A newton meter (forcemeter)', 'A spring-based newton meter measures force; a beam balance compares masses.', ['A beam balance', 'A measuring cylinder', 'A ruler']),
    ('Gravitational field strength is defined as', 'the force per unit mass', 'g = W/m, in N/kg.', ['the mass per unit force', 'the force per unit area', 'the energy per unit mass']),
    ('Define weight.', 'The gravitational force on an object that has mass.', 'gravitational force on a mass [1]'),
])
FX(t31, 'C2', (1, 2, 3, 4), [
    ('An astronaut has a mass of 70 kg on Earth. Explain what happens to her mass and her weight on the Moon.', 'Her mass stays 70 kg because the amount of matter is unchanged; her weight is less because g on the Moon is smaller.', 'mass unchanged [1]; weight smaller due to smaller g [1] [2]'),
    ('Explain why a beam balance gives the same reading on the Moon as on Earth, but a newton meter does not.', 'A beam balance compares the weight of the object with standard masses, and both are affected equally by g; a newton meter measures the force itself, which depends on g.', 'balance compares with masses, g cancels [1]; newton meter measures force ∝ g [1] [2]'),
    ('Explain why it is easier to lift a 20 kg rock on the Moon than on Earth, but just as hard to start it sliding sideways on a smooth surface.', 'Lifting depends on weight, which is smaller on the Moon; starting it moving depends on mass (inertia), which is unchanged.', 'weight smaller on Moon [1]; mass/inertia unchanged [1] [2]'),
    ('Describe the gravitational field near the Earth’s surface and explain the meaning of g = 9.8 N/kg.', 'Each kilogram of mass experiences a gravitational force of 9.8 N directed towards the centre of the Earth.', 'force per kg [1]; directed towards Earth’s centre [1] [2]'),
])
BODIES = [('Earth', 9.8), ('the Moon', 1.6), ('Mars', 3.7), ('Jupiter', 25), ('Venus', 8.9), ('Mercury', 3.7), ('Saturn', 10.4)]
OBJS = [('a robot rover', (80, 900)), ('an astronaut in a spacesuit', (100, 160)), ('a bag of rice', (1, 25)), ('a suitcase', (8, 30)), ('a lander module', (300, 2000)), ('a laboratory mass', (0.1, 1)), ('a car', (900, 1800))]


@t31.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t31_w(r, D):
    o, (lo, hi) = r.choice(OBJS)
    m = round(r.uniform(lo, hi), 1 if hi < 30 else 0)
    if D <= 2:
        return numq(r, D, f'{cap(o)} has a mass of {g(m)} kg on Earth (g = 9.8 N/kg).', 'weight', m * 9.8, ' N', f'W = mg = {g(m)} × 9.8', [m, m / 9.8, m * 10 * 9.8])
    b, gb = r.choice(BODIES[1:])
    W = m * gb
    if D == 3:
        if r.random() < 0.5:
            return Q(f'{cap(o)} has a weight of {g(W, 3)} N on {b}, where g = {gb} N/kg. Calculate its mass and its weight on Earth (g = 9.8 N/kg).', f'{g(m, 3)} kg; {g(m * 9.8, 3)} N',
                     f'm = W/g = {g(W, 3)}/{gb} = {g(m, 3)} kg [2]; W = {g(m, 3)} × 9.8 = {g(m * 9.8, 3)} N [1] [3]')
        return Q(f'{cap(o)} has a mass of {g(m)} kg. Calculate the difference between its weight on Earth (9.8 N/kg) and on {b} ({gb} N/kg).', f'{g(abs(m * 9.8 - W), 3)} N',
                 f'{g(m * 9.8, 3)} N and {g(W, 3)} N [2]; difference {g(abs(m * 9.8 - W), 3)} N [1] [3]')
    gm = round(W / m, 1)
    return Q(f'{cap(o)} of mass {g(m)} kg is weighed with a newton meter on an unknown planet and reads {g(W, 3)} N. (a) Calculate g on this planet. (b) Using the data (Earth 9.8, Mars 3.7, Jupiter 25, Venus 8.9, Moon 1.6, Saturn 10.4 N/kg), identify the body. (c) Explain whether a beam balance would give a different reading of its mass there.',
             f'(a) {g(gm, 3)} N/kg (b) {b} (c) no: a beam balance compares masses, and g affects both sides equally.',
             f'(a) g = W/m = {g(W, 3)}/{g(m)} [1] = {g(gm, 3)} N/kg [1] (b) correct match [1] (c) mass unchanged / balance compares [1] [4]', 'multi_step')


relation(t31, 'C2', (2, 3), 'W = mg', 'weight', {'mass': 1, 'gravitational field strength': 1},
         ['A space agency compares the weight of a rover on different worlds.', 'A student studies how the weight of an object depends on mass and gravity.', 'Engineers design a lunar lander.'])


def _w_c4(r, D):
    o, (lo, hi) = r.choice(OBJS[:5])
    m = round(r.uniform(lo, hi))
    b, gb = r.choice(BODIES[1:4])
    intro = f'{cap(o)} with a mass of {m} kg is sent from Earth (g = 9.8 N/kg) to {b} (g = {gb} N/kg).'
    parts = [
        lambda r: ('Calculate its weight on Earth.', f'{g(m * 9.8, 3)} N', f'W = mg = {m} × 9.8 [2]'),
        lambda r: (f'Calculate its weight on {b}.', f'{g(m * gb, 3)} N', f'{m} × {gb} [1]'),
        lambda r: (f'State its mass on {b} and explain.', f'{m} kg: mass is the amount of matter and does not depend on location.', 'value [1]; reason [1] [2]'),
        lambda r: ('Explain why a smaller rocket force is needed to lift it off the surface of ' + b + (' than of Earth.' if gb < 9.8 else '.') if gb < 9.8 else 'Explain why a larger force is needed to lift it off Jupiter than off Earth.',
                   'Its weight there is smaller, so less upward force is needed to give a resultant upward force.' if gb < 9.8 else 'Its weight is larger there.', 'weight comparison [1]; link to required upward force [1] [2]'),
        lambda r: ('Describe how the weight of a small rock sample could be measured there with apparatus carried on the mission.', 'Hang it from a calibrated newton meter (spring balance) and read the force when it is still.', 'newton meter [1]; reading at equilibrium [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t31.add('C4', (2, 3, 4, 5), 'multi_step')(_w_c4)

N32 = "Resultant force, Newton's laws and F = ma"
t32 = topic(N32, N32.lower(), "newton's laws", 'f = ma')
FX(t32, 'C1', (1, 2), [
    ('A resultant force of 12 N acts on a 3 kg mass. What is its acceleration?', '4 m/s²', 'a = F/m = 12/3 = 4 m/s².', ['36 m/s²', '0.25 m/s²', '15 m/s²']),
    ('An object moves at a constant velocity. What is the resultant force on it?', 'Zero', 'Newton’s first law: constant velocity ⇒ balanced forces.', ['Equal to its weight', 'In the direction of motion', 'Opposite to its motion']),
    ('Which equation links resultant force, mass and acceleration?', 'F = ma', 'Newton’s second law.', ['F = m/a', 'F = a/m', 'F = mv']),
    ('The unit 1 newton is the force that', 'gives a mass of 1 kg an acceleration of 1 m/s²', '1 N = 1 kg m/s².', ['gives a mass of 1 g an acceleration of 1 m/s²', 'lifts 1 kg by 1 m', 'acts on 1 kg in a gravitational field']),
    ('A book rests on a table. According to Newton’s third law, the partner of the Earth’s gravitational pull on the book is', 'the book’s gravitational pull on the Earth', 'Third-law pairs: same type of force, on different objects.', ['the table’s upward push on the book', 'friction on the book', 'the book’s push on the table']),
    ('State Newton’s first law.', 'An object stays at rest or moves at constant velocity unless acted on by a resultant force.', 'at rest or constant velocity [1]; unless resultant force [1] [2]'),
])
FX(t32, 'C2', (1, 2, 3, 4), [
    ('A car moves along a straight road at constant speed. Explain why the engine must still provide a forward force.', 'Friction and air resistance act backwards; the forward force must balance them so the resultant force is zero and speed stays constant.', 'resistive forces present [1]; forward force balances them, resultant zero [1] [2]'),
    ('Explain why passengers lurch forwards when a bus brakes suddenly.', 'The braking force acts on the bus, not on the passengers; by inertia (first law) their bodies continue moving forward until a force (seatbelt, seat) acts on them.', 'inertia / first law [1]; no force on passenger initially [1] [2]'),
    ('Explain in terms of forces why a rocket accelerates upwards at lift-off.', 'Thrust from the engines is greater than its weight (and drag), so there is an upward resultant force; F = ma gives an upward acceleration.', 'thrust > weight [1]; resultant upward gives acceleration [1] [2]'),
    ('A swimmer pushes water backwards and moves forwards. Explain this using Newton’s third law.', 'The swimmer exerts a backward force on the water; the water exerts an equal and opposite (forward) force on the swimmer.', 'force on water backwards [1]; equal opposite force on swimmer forwards [1] [2]'),
    ('Explain why a fully loaded lorry takes longer to reach 50 km/h than the same lorry when empty, with the same engine force.', 'The loaded lorry has a greater mass, so for the same resultant force its acceleration (a = F/m) is smaller.', 'greater mass [1]; a = F/m smaller [1] [2]'),
])
FMA = [('A car', (900, 1600), (1500, 6000)), ('A lorry', (8000, 20000), (8000, 30000)), ('A cyclist and bicycle', (60, 100), (80, 300)), ('A rocket', (5000, 50000), (1e5, 8e5)),
       ('A trolley', (0.5, 2.0), (0.4, 4.0)), ('A sledge', (20, 60), (40, 200)), ('A shopping cart', (15, 40), (20, 90)), ('A hockey puck', (0.16, 0.17), (2, 15))]


@t32.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t32_fma(r, D):
    o, (m1, m2), (f1, f2) = r.choice(FMA)
    m = r.choice([round(r.uniform(m1, m2), 2 if m2 < 5 else 0)])
    F = round(r.uniform(f1, f2), 1 if f2 < 20 else 0)
    if 'rocket' in o:
        F = round(F, -3)
    a = F / m
    k = r.random()
    if D <= 2:
        if k < 0.5:
            return numq(r, D, f'{o} of mass {g(m)} kg has a resultant force of {g(F)} N acting on it.', 'acceleration', a, ' m/s²', f'a = F/m = {g(F)}/{g(m)}', [F * m, m / F, a * 2])
        return numq(r, D, f'{o} of mass {g(m)} kg accelerates at {g(a)} m/s².', 'resultant force', F, ' N', f'F = ma = {g(m)} × {g(a)}', [m / a, a / m, F * 2])
    fr = round(F * r.choice([0.2, 0.25, 0.3, 0.4]), -1 if F > 100 else 1)
    Fd = F + fr
    if D == 3:
        return Q(f'{o} of mass {g(m)} kg has a driving force of {g(Fd)} N and total resistive forces of {g(fr)} N. Calculate the resultant force and the acceleration.', f'{g(F)} N; {g(a)} m/s²',
                 f'resultant = {g(Fd)} − {g(fr)} = {g(F)} N [1]; a = F/m [1] = {g(a)} m/s² [1] [3]')
    t = r.choice([2, 4, 5, 8, 10])
    return Q(f'{o} of mass {g(m)} kg starts from rest. The driving force is {g(Fd)} N and the resistive forces total {g(fr)} N. (a) Calculate the acceleration. (b) Calculate the speed after {t} s. (c) Explain why, at higher speeds, the acceleration decreases even if the driving force is unchanged.',
             f'(a) {g(a)} m/s² (b) {g(a * t)} m/s (c) air resistance increases with speed, so the resultant force decreases.',
             f'(a) resultant {g(F)} N [1]; a = {g(a)} m/s² [1] (b) v = at = {g(a * t)} m/s [1] (c) drag increases with speed, resultant smaller [1] [4]' if D == 4 else
             f'(a) resultant {g(F)} N [1]; a = F/m [1] = {g(a)} m/s² [1] (b) v = at = {g(a * t)} m/s [1] (c) drag rises with speed so resultant falls [1] [5]', 'multi_step')


@t32.add('C2', (2, 3, 4), 'explain')
def t32_pairs(r, D):
    sc = r.choice([('a person standing on the floor', 'the floor pushes up on the person', 'the person pushes down on the floor'),
                   ('a hammer hitting a nail', 'the hammer pushes the nail into the wood', 'the nail pushes back on the hammer'),
                   ('a gun firing a bullet', 'the gun pushes the bullet forwards', 'the bullet pushes the gun backwards (recoil)'),
                   ('a boat being rowed', 'the oar pushes the water backwards', 'the water pushes the oar (and boat) forwards'),
                   ('the Earth and the Moon', 'the Earth pulls the Moon', 'the Moon pulls the Earth'),
                   ('a magnet attracting an iron nail', 'the magnet pulls the nail', 'the nail pulls the magnet')])
    return Q(f'For {sc[0]}, one force is: "{sc[1]}". State the Newton’s third law partner of this force and give two ways in which the two forces are the same.',
             f'{cap(sc[2])}. They are equal in size, of the same type, act along the same line (but in opposite directions on different objects).', f'partner force [1]; any two of: equal size, same type, same line [2] [3]')


@t32.add('C3', (2, 3, 4), 'numerical')
def t32_two(r, D):
    m = r.choice([0.5, 0.8, 1.0, 1.2, 2.0, 2.5])
    F1 = r.choice([2, 3, 4, 5, 6, 8])
    F2 = r.choice([1, 1.5, 2, 2.5, 3])
    a = (F1 - F2) / m
    return Q(f'A trolley of mass {g(m)} kg is pulled to the right by a force of {F1} N while friction of {g(F2)} N acts to the left. Calculate the acceleration of the trolley and state its direction.', f'{g(a)} m/s² to the right',
             f'resultant = {F1} − {g(F2)} = {g(F1 - F2)} N [1]; a = {g(F1 - F2)}/{g(m)} [1] = {g(a)} m/s² to the right [1] [3]')


def _fma_c4(r, D):
    m = r.choice([800, 1000, 1200, 1500])
    Fd = r.choice([3000, 3600, 4000, 4800])
    fr = r.choice([600, 800, 1000, 1200])
    a = (Fd - fr) / m
    t = r.choice([4, 5, 6, 8])
    intro = r.choice([f'A car of mass {m} kg pulls away from traffic lights in {city(r)}. The engine provides a forward force of {Fd} N and resistive forces total {fr} N.',
                      f'An electric taxi of mass {m} kg accelerates from rest. The driving force is {Fd} N; friction and air resistance together are {fr} N.'])
    parts = [
        lambda r: ('Calculate the resultant force.', f'{Fd - fr} N', f'{Fd} − {fr} [1]'),
        lambda r: ('Calculate the acceleration.', f'{g(a)} m/s²', f'a = F/m = {Fd - fr}/{m} [2]'),
        lambda r: (f'Calculate the speed after {t} s.', f'{g(a * t)} m/s', f'v = at [2]'),
        lambda r: ('Later the car travels at a steady speed. State the size of the driving force then, if the resistive forces have risen to ' + str(Fd) + ' N, and explain.', f'{Fd} N: constant speed means zero resultant force.', 'value [1]; balanced forces [1] [2]'),
        lambda r: ('Explain, using Newton’s third law, how the tyres produce a forward force on the car.', 'The tyres push backwards on the road; the road pushes forwards on the tyres with an equal force (friction).', 'tyre pushes road back [1]; road pushes car forward equally [1] [2]'),
        lambda r: (f'Four passengers with total mass 300 kg get in. Calculate the new initial acceleration with the same forces.', f'{g((Fd - fr) / (m + 300))} m/s²', f'{Fd - fr}/{m + 300} [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t32.add('C4', (2, 3, 4, 5), 'multi_step')(_fma_c4)
t32.add('C3', (4, 5), 'multi_step')(_fma_c4)

N33 = 'Friction, drag and terminal velocity'
t33 = topic(N33, N33.lower(), 'friction', 'terminal velocity')
FX(t33, 'C1', (1, 2), [
    ('Friction always acts', 'in the opposite direction to the motion (or attempted motion)', 'Friction opposes relative motion between surfaces.', ['in the direction of motion', 'vertically upwards', 'towards the centre of the Earth']),
    ('Air resistance on a moving object increases when', 'its speed increases', 'Drag increases with speed (and area).', ['its speed decreases', 'its mass increases', 'it stops moving']),
    ('A skydiver falls at terminal velocity. Which statement is correct?', 'Air resistance equals weight', 'At terminal velocity forces are balanced, resultant force zero.', ['Air resistance is zero', 'Weight is greater than air resistance', 'The skydiver is accelerating at 9.8 m/s²']),
    ('Which change reduces friction between two surfaces?', 'Adding a lubricant such as oil', 'Lubricants separate the surfaces.', ['Pressing the surfaces together harder', 'Making the surfaces rougher', 'Adding sand between them']),
    ('Drag is the name for', 'friction acting on an object moving through a fluid', 'Air resistance and water resistance are types of drag.', ['the force of gravity on an object', 'the push from an engine', 'the upward force from a liquid only']),
    ('State one useful effect and one problem caused by friction.', 'Useful: grip of tyres/shoes, brakes. Problem: wear, heating, wasted energy in machines.', 'useful [1]; problem [1] [2]'),
])
FX(t33, 'C2', (1, 2, 3, 4), [
    ('A skydiver jumps from a plane. Explain why her acceleration decreases as she falls.', 'As her speed increases, air resistance increases; the resultant force (weight − air resistance) decreases, so a = F/m decreases.', 'drag increases with speed [1]; resultant force decreases [1]; a = F/m [1] [3]'),
    ('Explain why a skydiver slows down when the parachute opens.', 'The parachute greatly increases surface area, so air resistance becomes larger than weight; the resultant force is upwards so she decelerates.', 'larger area → more drag [1]; drag > weight, upward resultant [1] [2]'),
    ('Explain why a parachutist reaches a new, lower terminal velocity after the parachute opens.', 'As she slows, drag decreases until it equals her weight again; the forces balance at a lower speed because of the larger area.', 'drag decreases as speed falls [1]; balances weight at lower speed [1] [2]'),
    ('Explain why cyclists crouch low over the handlebars in a race.', 'Smaller frontal area means less air resistance, so for the same force they reach a higher top speed.', 'less area → less drag [1]; higher speed / less energy [1] [2]'),
    ('Explain why a car’s top speed is limited even when the engine gives its maximum force.', 'Air resistance increases with speed until it (with friction) equals the maximum driving force; then the resultant force is zero and the car cannot accelerate further.', 'drag increases with speed [1]; balances max driving force, zero resultant [1] [2]'),
])
FALLERS = [('a skydiver', (60, 100)), ('a skydiver with equipment', (80, 120)), ('a falling raindrop (mass in g)', None), ('a base jumper', (60, 90)), ('a parachuted supply crate', (50, 200))]


@t33.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t33_res(r, D):
    who = r.choice(['skydiver', 'base jumper', 'skydiver with a camera', 'parachuted supply crate'])
    m = r.choice([60, 65, 70, 75, 80, 85, 90, 100, 120])
    W = m * 9.8
    Fd = round(W * r.choice([0.2, 0.25, 0.4, 0.5, 0.6, 0.75]))
    a = (W - Fd) / m
    if D <= 2:
        return numq(r, D, f'A {who} of total mass {m} kg is falling. At one instant the air resistance is {Fd} N (g = 9.8 N/kg).', 'resultant force', W - Fd, ' N', f'W = {g(W, 3)} N; resultant = {g(W, 3)} − {Fd}', [W, Fd, W + Fd])
    if D == 3:
        return Q(f'A {who} of total mass {m} kg is falling. At one instant the air resistance is {Fd} N (g = 9.8 N/kg). Calculate the acceleration at this instant.', f'{g(a)} m/s² downwards',
                 f'W = mg = {g(W, 3)} N [1]; resultant = {g(W - Fd, 3)} N [1]; a = F/m = {g(a)} m/s² [1] [3]')
    up = round(W * r.choice([1.5, 2, 2.5, 3]))
    return Q(f'A {who} of total mass {m} kg (g = 9.8 N/kg) falls at terminal velocity. The parachute then opens and the air resistance immediately becomes {up} N. (a) State the air resistance just before the parachute opens. (b) Calculate the deceleration just after it opens. (c) Describe what happens to the speed and the air resistance after this until a new steady state is reached.',
             f'(a) {g(W, 3)} N (b) {g((up - W) / m)} m/s² (c) speed decreases, so air resistance decreases until it equals the weight again; new lower terminal velocity.',
             f'(a) equals weight = {g(W, 3)} N [1] (b) resultant = {up} − {g(W, 3)} = {g(up - W, 3)} N upwards [1]; a = {g((up - W) / m)} m/s² [1] (c) speed and drag decrease [1]; lower terminal velocity when drag = weight [1] [5]', 'multi_step')


@t33.add('C3', (2, 3, 4), 'case')
def t33_data(r, D):
    v = [0, 9.0, 16.5, 22.0, 25.5, 27.5, 28.5, 29.0, 29.0, 29.0]
    k = r.choice([0.9, 1.0, 1.1, 1.2])
    vs = [round(x * k, 1) for x in v]
    who = person(r)
    return Q(f'{who} records the speed of a falling object every second: time/s = 0, 1, 2, …, 9; speed/m/s = ' + ', '.join(g(x) for x in vs) + '. (a) State the terminal velocity. (b) Calculate the average acceleration in the first second. (c) Explain why the speed stops increasing.',
             f'(a) {g(vs[-1])} m/s (b) {g(vs[1])} m/s² (c) air resistance rises with speed until it equals the weight; resultant force zero.',
             f'(a) {g(vs[-1])} m/s [1] (b) {g(vs[1])}/1 [1] (c) drag increases [1]; balances weight [1] [4]' if D >= 4 else f'(a) {g(vs[-1])} m/s [1] (b) {g(vs[1])} m/s² [1] (c) drag balances weight [1] [3]')


def _term_c4(r, D):
    m = r.choice([70, 75, 80, 90])
    W = m * 9.8
    intro = r.choice([f'A skydiver of total mass {m} kg jumps from a helicopter above {city(r)}. (g = 9.8 N/kg)', f'A wingsuit flyer of mass {m} kg jumps from a cliff. (g = 9.8 N/kg)'])
    parts = [
        lambda r: ('Calculate the weight.', f'{g(W, 3)} N', 'W = mg [1]'),
        lambda r: ('State the acceleration at the moment of jumping and explain.', '9.8 m/s²: speed is zero so there is no air resistance.', 'value [1]; reason [1] [2]'),
        lambda r: ('Explain why the acceleration decreases as the speed increases.', 'Air resistance increases, so resultant force (W − drag) decreases; a = F/m.', '[2]'),
        lambda r: ('Describe the forces when terminal velocity is reached.', f'Air resistance = weight = {g(W, 3)} N; resultant zero.', '[2]'),
        lambda r: ('Sketch-describe the speed-time graph from jumping until just before the parachute opens.', 'Curve starting at origin with gradient 9.8 m/s², becoming less steep, levelling off at terminal velocity.', 'curve from origin [1]; levels off [1] [2]'),
        lambda r: ('State and explain one way the skydiver can increase her terminal velocity.', 'Dive head-first/tuck in to reduce area, reducing drag at each speed.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t33.add('C4', (2, 3, 4, 5), 'multi_step')(_term_c4)

N34 = 'Circular motion and the force towards the centre'
t34 = topic(N34, N34.lower(), 'circular motion')
FX(t34, 'C1', (1, 2), [
    ('An object moves in a circle at constant speed. In which direction is the resultant force on it?', 'Towards the centre of the circle', 'A force perpendicular to the velocity, towards the centre, changes direction but not speed.', ['Along the direction of motion', 'Away from the centre', 'Zero, because the speed is constant']),
    ('What provides the force towards the centre for a satellite orbiting the Earth?', 'Gravity (the Earth’s gravitational pull)', 'Gravitational attraction acts towards Earth’s centre.', ['The satellite’s engines', 'Air resistance', 'Friction with space']),
    ('What provides the force towards the centre when a car drives round a bend?', 'Friction between the tyres and the road', 'Sideways friction on the tyres.', ['The engine’s forward force', 'The car’s weight', 'Air resistance']),
    ('If the string of a ball being whirled in a horizontal circle breaks, the ball moves', 'in a straight line along the tangent', 'With no force towards the centre the ball continues in a straight line (first law).', ['outwards along the radius', 'towards the centre', 'in a larger circle']),
    ('Explain why an object moving in a circle at constant speed is accelerating.', 'Its direction (and so its velocity) is continuously changing.', 'velocity changes because direction changes [1]'),
])
FX(t34, 'C2', (1, 2, 3, 4), [
    ('Explain why a car can skid off a wet, icy bend if it goes too fast.', 'A larger speed needs a larger force towards the centre; on ice the friction cannot provide enough, so the car moves in a wider path (straight on).', 'faster needs bigger centripetal force [1]; friction too small on ice [1] [2]'),
    ('A hammer thrower spins a heavy ball on a wire. Explain why the force needed in the wire is larger for a heavier ball at the same speed and radius.', 'A larger mass needs a larger force towards the centre to keep it moving in the same circle at the same speed.', 'greater mass [1]; larger force needed for same speed and radius [1] [2]'),
    ('Describe what happens to the radius of the path if the force towards the centre is increased while the speed and mass stay the same.', 'The radius decreases: the object moves in a tighter circle.', 'radius decreases [1]'),
    ('Explain why the speed of an object moving in a circle does not change, even though a force acts on it.', 'The force is perpendicular to the velocity, so it changes only the direction of motion, not the speed.', 'force perpendicular to motion [1]; changes direction only [1] [2]'),
])
CIRC = [('a stone whirled on a string', 'the tension in the string'), ('a car going round a roundabout', 'friction between the tyres and the road'), ('the Moon orbiting the Earth', 'the gravitational pull of the Earth'),
        ('a cyclist going round a curved track', 'friction on the tyres (and the track banking)'), ('a satellite in orbit', 'gravity'), ('clothes in a spinning washing machine drum', 'the push of the drum wall'),
        ('a passenger on a fairground carousel', 'the push of the seat and the chain tension'), ('an electron orbiting a nucleus (model)', 'electrostatic attraction')]
CHG = [('the speed increases', 'mass and radius are unchanged', 'a larger force towards the centre is needed'),
       ('the mass increases', 'speed and radius are unchanged', 'a larger force towards the centre is needed'),
       ('the force towards the centre increases', 'speed and mass are unchanged', 'the radius of the circle decreases'),
       ('the force towards the centre increases', 'mass and radius are unchanged', 'the speed must increase'),
       ('the force towards the centre suddenly becomes zero', 'nothing else acts', 'the object moves off in a straight line along the tangent')]


@t34.add('C1', (1, 2, 3))
def t34_what(r, D):
    a, f = r.choice(CIRC)
    others = [x[1] for x in CIRC if x[1] != f]
    opts, ans = mcq(r, f, others)
    return Q(f'What provides the force towards the centre for {a}?', ans, f'{cap(f)} acts towards the centre of the circular path.', opts=opts)


@t34.add('C2', (2, 3, 4), 'explain')
def t34_change(r, D):
    a, f = r.choice(CIRC[:4] + CIRC[5:7])
    c, keep, res = r.choice(CHG)
    return Q(f'Consider {a}. The force towards the centre is provided by {f}. Describe and explain what happens if {c} while {keep}.', cap(res) + '.',
             'correct effect [1]; reasoning: force towards centre needed to change direction / depends on mass, speed and radius [1] [2]')


@t34.add('C3', (2, 3, 4), 'case')
def t34_data(r, D):
    m = r.choice([0.05, 0.1, 0.2])
    rows = [(0.5, 2.0), (0.5, 3.0), (0.5, 4.0)]
    k = r.choice([1, 1.5, 2])
    F = [round(m * v * v / rr * k, 2) for rr, v in rows]
    return Q(f'A student whirls a bung of mass {g(m * 1000)} g on a string in a horizontal circle of radius 0.5 m and measures the tension needed at different speeds: speed/m/s 2.0, 3.0, 4.0; tension/N {", ".join(g(x) for x in F)}. (a) Describe the trend. (b) Predict, with a reason, whether the tension needed at 3.0 m/s would be larger or smaller for a radius of 1.0 m.',
             '(a) The force needed increases as speed increases (more than proportionally). (b) Smaller: a larger radius needs a smaller force for the same speed and mass.',
             '(a) trend [1]; not proportional/increases faster [1] (b) smaller with reason [1] [3]')


def _circ_c4(r, D):
    a, f = r.choice(CIRC[:7])
    parts = [
        lambda r: ('State the direction of the resultant force.', 'Towards the centre of the circle.', '[1]'),
        lambda r: ('Name the force that provides it.', cap(f) + '.', '[1]'),
        lambda r: ('Explain why the object is accelerating even if its speed is constant.', 'Velocity is a vector; its direction keeps changing.', '[2]'),
        lambda r: ('Describe what would happen if this force suddenly stopped acting.', 'It would move off in a straight line along the tangent at constant speed.', 'straight line [1]; tangent [1] [2]'),
        lambda r: ('State how the force must change if the speed increases but the radius stays the same.', 'It must increase.', '[1]'),
        lambda r: ('State one way of keeping the same force but making the object move faster.', 'Increase the radius of the circle (or reduce the mass).', '[1]'),
    ]
    return compose(r, f'Consider {a}, moving at a steady speed in a circle.', parts, k=(2, 3, 4), type_='multi_step')


t34.add('C4', (2, 3, 4, 5), 'multi_step')(_circ_c4)
t34.add('C3', (3, 4), 'multi_step')(_circ_c4)

N35 = 'Momentum, impulse and conservation of momentum'
t35 = topic(N35, N35.lower(), 'momentum', 'impulse')
FX(t35, 'C1', (1, 2), [
    ('What is the unit of momentum?', 'kg m/s', 'p = mv: kg × m/s.', ['N/s', 'kg/m s', 'J']),
    ('Impulse is equal to', 'force × time (the change in momentum)', 'Impulse = FΔt = Δ(mv).', ['force ÷ time', 'mass × acceleration', 'force × distance']),
    ('Momentum is conserved in a collision when', 'no external resultant force acts', 'In a closed system total momentum before = total momentum after.', ['the objects stick together', 'the objects are the same mass', 'the objects bounce apart']),
    ('A 2 kg ball moves at 3 m/s. What is its momentum?', '6 kg m/s', 'p = mv = 2 × 3 = 6 kg m/s.', ['1.5 kg m/s', '9 kg m/s', '18 kg m/s']),
    ('Resultant force is equal to', 'the rate of change of momentum', 'F = Δp/Δt.', ['the momentum × time', 'the change in kinetic energy', 'the momentum ÷ mass']),
    ('State the principle of conservation of momentum.', 'In a closed system (no external forces), the total momentum before an event equals the total momentum after it.', 'total momentum constant / before = after [1]; no external force [1] [2]'),
])
FX(t35, 'C2', (1, 2, 3, 4), [
    ('Explain how the crumple zone of a car reduces the force on the passengers in a crash.', 'The crumple zone increases the time taken for the car to stop; the change in momentum is the same, so the force (Δp/Δt) is smaller.', 'longer time [1]; same Δp so smaller F = Δp/Δt [1] [2]'),
    ('Explain why a gun recoils when it fires a bullet.', 'Total momentum before is zero; after, the bullet has forward momentum, so the gun must have equal momentum backwards to keep the total zero.', 'initial momentum zero [1]; equal and opposite momentum [1] [2]'),
    ('Explain why a gymnast bends her knees when landing.', 'Bending the knees increases the time to stop; for the same change in momentum the force on her legs is smaller.', 'longer time [1]; smaller force for same Δp [1] [2]'),
    ('Explain why momentum is a vector quantity and how this matters in a head-on collision.', 'Momentum has direction (velocity is a vector); momenta in opposite directions must be given opposite signs, so they can partly cancel.', 'direction from velocity [1]; opposite signs / can cancel [1] [2]'),
    ('Explain why airbags and seat belts are designed to stretch or deflate slightly in a crash.', 'They extend the stopping time of the passenger, reducing the force for the same change in momentum, and spread the force over a larger area.', 'longer time [1]; smaller force [1] [2]'),
])


@t35.add('C3', (1, 2, 3), 'numerical')
def t35_p(r, D):
    o = r.choice([('A football', 0.43, (5, 30)), ('A car', 1200, (5, 30)), ('A cricket ball', 0.16, (10, 40)), ('A cyclist with bike', 85, (3, 12)), ('A truck', 9000, (5, 25)), ('A bowling ball', 6.0, (2, 8))])
    v = round(r.uniform(*o[2]), 1)
    p = o[1] * v
    if D <= 2:
        return numq(r, D, f'{o[0]} of mass {g(o[1])} kg moves at {g(v)} m/s.', 'momentum', p, ' kg m/s', f'p = mv = {g(o[1])} × {g(v)}', [o[1] / v, 0.5 * o[1] * v * v, v / o[1]])
    return Q(f'{o[0]} of mass {g(o[1])} kg has a momentum of {g(p, 3)} kg m/s. Calculate its speed and its kinetic energy.', f'{g(v, 3)} m/s; {g(0.5 * o[1] * v * v, 3)} J',
             f'v = p/m = {g(p, 3)}/{g(o[1])} = {g(v, 3)} m/s [2]; KE = ½mv² = {g(0.5 * o[1] * v * v, 3)} J [1] [3]')


@t35.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t35_coll(r, D):
    m1 = r.choice([0.5, 1.0, 1.5, 2.0, 800, 1000, 1200, 3.0])
    m2 = r.choice([0.5, 1.0, 1.5, 2.0, 2.5]) if m1 < 10 else r.choice([600, 900, 1100, 1500, 2000])
    u1 = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    things = ('trolley', 'trolleys') if m1 < 10 else ('car', 'cars')
    if D <= 3:
        v = m1 * u1 / (m1 + m2)
        return numq(r, D, f'A {things[0]} of mass {g(m1)} kg moving at {u1} m/s collides with a stationary {things[0]} of mass {g(m2)} kg and they stick together.', 'speed of the joined ' + things[1] + ' just after the collision', v, ' m/s',
                    f'{g(m1)} × {u1} = ({g(m1)} + {g(m2)})v; v = {g(m1 * u1)}/{g(m1 + m2)}', [u1 * m2 / (m1 + m2), u1 / 2, m1 * u1 / m2], marks=3 if D == 3 else None)
    u2 = r.choice([1, 2, 3, 4])
    v = (m1 * u1 - m2 * u2) / (m1 + m2)
    dke = 0.5 * m1 * u1 ** 2 + 0.5 * m2 * u2 ** 2 - 0.5 * (m1 + m2) * v * v
    return Q(f'A {things[0]} of mass {g(m1)} kg moving at {u1} m/s to the right collides head-on with a {things[0]} of mass {g(m2)} kg moving at {u2} m/s to the left. They stick together. (a) Calculate the total momentum before the collision. (b) Calculate the velocity just after the collision. (c) Calculate the kinetic energy lost' + (' and state where it goes.' if D >= 5 else '.'),
             f'(a) {g(m1 * u1 - m2 * u2, 3)} kg m/s to the {"right" if v >= 0 else "left"} (b) {g(abs(v), 3)} m/s to the {"right" if v >= 0 else "left"} (c) {g(dke, 3)} J' + (' – transferred to thermal energy and sound, and work done deforming the objects.' if D >= 5 else ''),
             f'(a) {g(m1)}×{u1} − {g(m2)}×{u2} = {g(m1 * u1 - m2 * u2, 3)} kg m/s (signs) [2] (b) ÷ {g(m1 + m2)} = {g(abs(v), 3)} m/s with direction [1] (c) KE before − after = {g(dke, 3)} J [1]' + (' ; thermal/sound/deformation [1] [5]' if D >= 5 else ' [4]'), 'multi_step')


@t35.add('C3', (1, 2, 3, 4), 'numerical')
def t35_imp(r, D):
    sc = r.choice([('A footballer kicks a stationary ball of mass 0.45 kg', 0.45, 0, (10, 30), (0.008, 0.02)), ('A tennis racket hits a ball of mass 0.058 kg, initially at rest,', 0.058, 0, (20, 50), (0.004, 0.006)),
                   ('A golf club strikes a stationary ball of mass 0.046 kg', 0.046, 0, (30, 70), (0.0005, 0.001)), ('A car of mass 1000 kg crashes into a barrier and stops; it was travelling', 1000, None, (10, 25), (0.1, 0.4))])
    v = round(r.uniform(*sc[3]))
    t = round(r.uniform(*sc[4]), 4 if sc[4][1] < 0.01 else 3)
    dp = sc[1] * v
    F = dp / t
    s = f'{sc[0]} {"at" if sc[2] is None else "so that it leaves at"} {v} m/s. The contact time is {g(t)} s.'
    if D <= 2:
        return numq(r, D, s, 'change in momentum (impulse)', dp, ' kg m/s', f'Δp = m Δv = {g(sc[1])} × {v}', [dp * t, F, sc[1] / v])
    if D == 3:
        return Q(s + ' Calculate the average force.', f'{g(F, 3)} N', f'Δp = {g(dp, 3)} kg m/s [1]; F = Δp/Δt [1] = {g(F, 3)} N [1] [3]')
    t2 = t * r.choice([2, 3, 4])
    return Q(s + f' (a) Calculate the impulse. (b) Calculate the average force. (c) Calculate the average force if the contact time were {g(t2)} s and explain why this is safer or less effective.',
             f'(a) {g(dp, 3)} N s (b) {g(F, 3)} N (c) {g(dp / t2, 3)} N: the same change of momentum over a longer time needs a smaller force.',
             f'(a) {g(dp, 3)} N s [1] (b) F = Δp/Δt = {g(F, 3)} N [1] (c) {g(dp / t2, 3)} N [1]; longer time, smaller force [1] [4]', 'multi_step')


def _mom_c4(r, D):
    mg_ = r.choice([2, 3, 4, 5])
    mb = r.choice([0.01, 0.02, 0.025, 0.05])
    vb = r.choice([200, 250, 300, 400])
    vg = mb * vb / mg_
    sc = r.choice([('rifle', 'bullet'), ('cannon on a frictionless track', 'cannonball'), ('toy spring launcher', 'ball bearing')])
    if 'cannon' in sc[0]:
        mg_, mb, vb = r.choice([800, 1000, 1200]), r.choice([5, 8, 10]), r.choice([100, 150, 200])
        vg = mb * vb / mg_
    if 'toy' in sc[0]:
        mg_, mb, vb = r.choice([0.4, 0.5, 0.6]), r.choice([0.02, 0.03, 0.05]), r.choice([3, 4, 5, 6])
        vg = mb * vb / mg_
    name = sc[0].split(' on ')[0]
    where = ', mounted on a frictionless track,' if ' on ' in sc[0] else ''
    intro = f'A {name} of mass {g(mg_)} kg{where} fires a {sc[1]} of mass {g(mb)} kg forwards at {g(vb)} m/s. Both are initially at rest.'
    parts = [
        lambda r: ('State the total momentum before firing.', '0', '[1]'),
        lambda r: (f'Calculate the momentum of the {sc[1]}.', f'{g(mb * vb, 3)} kg m/s', 'p = mv [1]'),
        lambda r: (f'Calculate the recoil speed of the {sc[0].split(" on")[0]}.', f'{g(vg, 3)} m/s', f'{g(mb * vb, 3)} = {g(mg_)} × v [1]; v = {g(vg, 3)} m/s [1] [2]'),
        lambda r: ('Explain why the recoil speed is much smaller than the speed of the ' + sc[1] + '.', 'Equal momentum but much larger mass, so smaller speed.', '[2]'),
        lambda r: (f'The {sc[1]} is accelerated for {g(0.002 if "toy" not in sc[0] else 0.05)} s. Calculate the average force on it.', f'{g(mb * vb / (0.002 if "toy" not in sc[0] else 0.05), 3)} N', 'F = Δp/Δt [2]'),
        lambda r: ('Compare the kinetic energies after firing and explain where the energy came from.', f'{sc[1]}: {g(0.5 * mb * vb * vb, 3)} J; launcher: {g(0.5 * mg_ * vg * vg, 3)} J; from chemical (or elastic) energy.', 'both KEs [2]; source [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t35.add('C4', (2, 3, 4, 5), 'multi_step')(_mom_c4)

CHAPTERS[3] = [t31, t32, t33, t34, t35]

# =========================================================== 4 Turning effects of forces
N41 = 'Moment of a force as force × perpendicular distance'
t41 = topic(N41, N41.lower(), 'moment of a force')
FX(t41, 'C1', (1, 2), [
    ('What is the unit of the moment of a force?', 'N m', 'Moment = force (N) × perpendicular distance (m).', ['N/m', 'N', 'J/s']),
    ('The moment of a force about a pivot is', 'force × perpendicular distance from the pivot to the line of action of the force', 'Moment = F × d, with d perpendicular to the line of action.', ['force ÷ distance from the pivot', 'force × time', 'mass × distance from the pivot']),
    ('A force of 20 N acts at a perpendicular distance of 0.5 m from a pivot. What is its moment?', '10 N m', '20 × 0.5 = 10 N m.', ['40 N m', '20.5 N m', '0.025 N m']),
    ('Which change makes it easier to undo a tight nut with a spanner?', 'Using a longer spanner', 'Greater distance gives a greater moment for the same force.', ['Pushing nearer the nut', 'Pushing along the handle towards the nut', 'Using a shorter spanner']),
    ('Where should a door handle be placed so the door opens with the least force?', 'As far as possible from the hinges', 'Largest perpendicular distance from the pivot (hinge).', ['Next to the hinges', 'In the middle of the door', 'At the top of the hinge side']),
    ('Define the moment of a force.', 'The turning effect of a force about a pivot, equal to force × perpendicular distance from the pivot.', 'turning effect [1]; F × perpendicular distance [1] [2]'),
])
FX(t41, 'C2', (1, 2, 3, 4), [
    ('Explain why it is easier to push a door open at the handle than near the hinges.', 'The handle is further from the pivot, so a smaller force gives the same moment.', 'larger distance from pivot [1]; same moment with smaller force [1] [2]'),
    ('Explain why pushing along the length of a spanner towards the nut has no turning effect.', 'The line of action passes through the pivot, so the perpendicular distance is zero and the moment is zero.', 'line of action through pivot [1]; zero perpendicular distance → zero moment [1] [2]'),
    ('Explain why a wheelbarrow makes it easier to lift a heavy load.', 'The handles are much further from the pivot (wheel) than the load, so a small upward force on the handles gives a moment equal to that of the load.', 'pivot at wheel [1]; larger distance for effort [1] [2]'),
    ('A force is applied at an angle to a spanner rather than at 90°. Explain why the turning effect is smaller.', 'Only the perpendicular distance from the pivot to the line of action counts; at an angle this distance is less than the length of the spanner.', 'perpendicular distance [1]; smaller than full length [1] [2]'),
])
MOM = [('a spanner tightening a wheel nut', 'spanner'), ('a door being pushed open', 'door'), ('a crowbar lifting a paving slab', 'crowbar'), ('a bottle opener', 'opener'),
       ('a pair of scissors cutting card', 'scissors'), ('a tap being turned', 'tap handle'), ('a bicycle pedal crank', 'crank'), ('a steering wheel', 'wheel rim')]


@t41.add('C3', (1, 2, 3, 4), 'numerical')
def t41_mom(r, D):
    ctx, part = r.choice(MOM)
    F = r.choice([15, 20, 25, 40, 50, 60, 80, 120, 150])
    dcm = r.choice([8, 10, 12, 15, 20, 25, 30, 40, 50])
    M = F * dcm / 100
    if D <= 2:
        return numq(r, D, f'In {ctx}, a force of {F} N acts at right angles to the {part} at a perpendicular distance of {dcm / 100:g} m from the pivot.', 'moment of the force', M, ' N m', f'M = Fd = {F} × {dcm / 100:g}', [F * dcm, F / (dcm / 100), M / 2])
    if D == 3:
        if r.random() < 0.5:
            return Q(f'In {ctx}, a force of {F} N acts at right angles to the {part}, {dcm} cm from the pivot. Calculate the moment in N m.', f'{g(M)} N m', f'd = {dcm / 100:g} m [1]; M = {F} × {dcm / 100:g} [1] = {g(M)} N m [1] [3]')
        return Q(f'A moment of {g(M)} N m is needed for {ctx}. The force is applied at right angles, {dcm} cm from the pivot. Calculate the force needed.', f'{g(F)} N', f'd = {dcm / 100:g} m [1]; F = M/d [1] = {g(F)} N [1] [3]')
    d2 = dcm * r.choice([1.5, 2, 2.5])
    return Q(f'A moment of {g(M)} N m is needed for {ctx}. (a) Calculate the force needed at right angles {dcm} cm from the pivot. (b) Calculate the force needed if it is applied {g(d2)} cm from the pivot. (c) Explain why the force must be at right angles to the {part} for the answers to be correct.',
             f'(a) {g(F)} N (b) {g(M / (d2 / 100))} N (c) the moment uses the perpendicular distance; at another angle the perpendicular distance is less so more force is needed.',
             f'(a) {g(M)}/{dcm / 100:g} = {g(F)} N [1] (b) {g(M)}/{g(d2 / 100)} = {g(M / (d2 / 100))} N [1] (c) perpendicular distance [1]; smaller at other angles [1] [4]', 'multi_step')


@t41.add('C2', (2, 3, 4), 'explain')
def t41_err(r, D):
    F = r.choice([20, 30, 40, 50])
    dcm = r.choice([20, 25, 40, 50])
    who = person(r)
    return Q(f'{who} calculates the moment of a {F} N force acting {dcm} cm from a pivot as {F * dcm} N m. Identify the error and give the correct value.', f'{who} did not convert cm to m; M = {F} × {dcm / 100:g} = {g(F * dcm / 100)} N m.',
             f'unit error (cm not converted) [1]; {g(F * dcm / 100)} N m [1] [2]')


def _mom_c4(r, D):
    ctx, part = r.choice(MOM[:3] + MOM[6:])
    F = r.choice([40, 50, 60, 80])
    L = r.choice([0.2, 0.25, 0.3, 0.4])
    parts = [
        lambda r: (f'A force of {F} N is applied at right angles to the {part}, {L} m from the pivot. Calculate the moment.', f'{g(F * L)} N m', f'M = Fd [1] = {g(F * L)} N m [1] [2]'),
        lambda r: (f'Calculate the force needed to give the same moment at {g(L * 2)} m from the pivot.', f'{g(F / 2)} N', f'F = {g(F * L)}/{g(L * 2)} [2]'),
        lambda r: ('Explain why a force applied at 45° to the ' + part + ' at the same point has a smaller moment.', 'The perpendicular distance to the line of action is less than the full distance.', '[2]'),
        lambda r: ('State the conditions for a force to have zero moment about the pivot.', 'Its line of action passes through the pivot (or the force is zero).', '[1]'),
        lambda r: ('Suggest one change to the design to make the job easier.', f'A longer {part} / handle, so a smaller force gives the same moment.', 'design change with reason [2]'),
    ]
    return compose(r, f'Consider {ctx}.', parts, k=(2, 3, 4), type_='multi_step')


t41.add('C4', (2, 3, 4, 5), 'multi_step')(_mom_c4)

N42 = 'The principle of moments and equilibrium'
t42 = topic(N42, N42.lower(), 'principle of moments', 'equilibrium')
FX(t42, 'C1', (1, 2), [
    ('An object is in equilibrium when', 'there is no resultant force and no resultant moment', 'Both conditions are needed.', ['the clockwise moments are larger than the anticlockwise moments', 'there is no resultant force only', 'it is moving in a circle']),
    ('A 2 N weight hangs 30 cm to the left of a pivot. Where must a 3 N weight hang to balance it?', '20 cm to the right of the pivot', '2 × 30 = 3 × d, d = 20 cm.', ['30 cm to the right', '45 cm to the right', '20 cm to the left']),
    ('In the principle of moments, for a balanced object', 'sum of clockwise moments = sum of anticlockwise moments', 'Principle of moments about any point.', ['clockwise moments = 0', 'sum of forces up = sum of moments', 'clockwise forces = anticlockwise forces only']),
    ('A uniform metre rule is balanced on a pivot at its 50 cm mark. Where does its weight act?', 'At the 50 cm mark', 'For a uniform rule the centre of gravity is at the middle.', ['At the 0 cm mark', 'At the 100 cm mark', 'It has no weight when balanced']),
    ('State the principle of moments.', 'For an object in equilibrium, the sum of the clockwise moments about any point equals the sum of the anticlockwise moments about that point.', 'sum clockwise = sum anticlockwise [1]; about the same point, in equilibrium [1] [2]'),
])
FX(t42, 'C2', (1, 2, 3, 4), [
    ('Explain how a light child can balance a heavy adult on a see-saw.', 'The child sits further from the pivot so that child’s weight × distance equals adult’s weight × distance.', 'moments equal [1]; child further from pivot [1] [2]'),
    ('Describe an experiment to verify the principle of moments using a metre rule.', 'Balance a metre rule on a pivot at its centre; hang known weights at measured distances on both sides until it balances; compare Σ(clockwise F × d) with Σ(anticlockwise F × d) for several arrangements.', 'balanced rule on pivot [1]; weights at measured distances [1]; compare sums of moments [1] [3]'),
    ('A uniform plank rests on two supports. Explain why the support nearer to a heavy box on the plank pushes up with the greater force.', 'Taking moments about the other support, the box’s moment is large and must be balanced by the nearer support; the box is closer to it so it carries more of the load.', 'moments about one support [1]; nearer support carries more [1] [2]'),
    ('Explain why both conditions (no resultant force and no resultant moment) are needed for equilibrium.', 'Without resultant force the object could still rotate if moments are unbalanced; without balanced moments it would start to turn.', 'force condition prevents acceleration [1]; moment condition prevents rotation [1] [2]'),
])
SEE = [('a see-saw in a park in {c}', '{a}', '{b}', 'N'), ('a uniform metre rule balanced at its centre', 'load P', 'load Q', 'N'), ('a mobile hanging from a ceiling', 'a toy bird', 'a toy fish', 'N'),
       ('a crane jib balanced on its tower', 'the load', 'the counterweight', 'kN'), ('a beam balance in a market in {c}', 'a bag of spices', 'a set of brass weights', 'N')]


@t42.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t42_bal(r, D):
    ctx, A, B, u = r.choice(SEE)
    a_, b_ = two_people(r)
    ctx = ctx.format(c=city(r)); A = A.format(a=a_); B = B.format(b=b_)
    if u == 'N' and 'see-saw' in ctx:
        W1, W2 = r.choice([300, 350, 400, 450, 500, 600]), r.choice([200, 240, 250, 300, 320, 360])
        d1 = r.choice([1.0, 1.2, 1.5, 0.8])
        du = 'm'
    elif u == 'kN':
        W1, W2 = r.choice([10, 12, 15, 20, 30]), r.choice([40, 50, 60, 80])
        d1 = r.choice([12, 15, 18, 20, 24])
        du = 'm'
    else:
        W1, W2 = r.choice([1, 1.5, 2, 3, 4, 5]), r.choice([0.5, 1, 2, 2.5, 3, 6])
        d1 = r.choice([10, 12, 15, 20, 24, 30, 40])
        du = 'cm'
    if W1 == W2:
        W2 = W2 * 2
    d2 = W1 * d1 / W2
    s = f'On {ctx}, {A} of weight {g(W1)} {u} is {g(d1)} {du} from the pivot on one side. {cap(B)} of weight {g(W2)} {u} is on the other side.'
    if D <= 2:
        return numq(r, D, s + ' The system balances.', f'distance of {B} from the pivot', d2, ' ' + du, f'{g(W1)} × {g(d1)} = {g(W2)} × d; d = {g(W1 * d1)}/{g(W2)}', [W2 * d1 / W1, d1, d1 * W1 * W2 / 10])
    if D == 3:
        return Q(s + f' Calculate how far from the pivot {B} must be for balance, and state the principle you used.', f'{g(d2)} {du}; principle of moments (clockwise = anticlockwise).',
                 f'principle of moments [1]; {g(W1)} × {g(d1)} = {g(W2)} × d [1]; d = {g(d2)} {du} [1] [3]')
    W3 = W1 * r.choice([0.25, 0.5]) if u != 'kN' else 5
    d3 = d1 * r.choice([0.5, 0.75])
    dn = (W1 * d1 + W3 * d3) / W2
    return Q(s + f' A further object of weight {g(W3)} {u} is then placed {g(d3)} {du} from the pivot on the same side as {A}. (a) Calculate the total anticlockwise moment on that side. (b) Calculate the new distance of {B} from the pivot for balance. (c) State the force exerted by the pivot (ignore the weight of the beam).',
             f'(a) {g(W1 * d1 + W3 * d3)} {u} {du} (b) {g(dn)} {du} (c) {g(W1 + W2 + W3)} {u} upwards',
             f'(a) {g(W1)}×{g(d1)} + {g(W3)}×{g(d3)} = {g(W1 * d1 + W3 * d3)} [1] (b) = {g(W2)} × d [1]; d = {g(dn)} {du} [1] (c) sum of weights, upwards [1]' + (' [4]' if D == 4 else '; no resultant force condition stated [1] [5]'), 'multi_step')


@t42.add('C3', (3, 4, 5), 'multi_step')
def t42_beam(r, D):
    L = r.choice([2.0, 3.0, 4.0, 5.0, 6.0])
    Wb = r.choice([100, 150, 200, 300, 400])
    Wl = r.choice([200, 300, 400, 500, 600, 800])
    x = round(L * r.choice([0.25, 0.3, 0.4, 0.75, 0.8]), 2)
    RB = (Wb * L / 2 + Wl * x) / L
    RA = Wb + Wl - RB
    ctx = r.choice(['A uniform plank', 'A uniform bridge section', 'A uniform shelf', 'A uniform scaffold board'])
    return Q(f'{ctx} of length {g(L)} m and weight {Wb} N rests on supports A and B at its two ends. A load of {Wl} N is placed {g(x)} m from A. (a) Take moments about A to find the upward force at B. (b) Find the upward force at A.',
             f'(a) {g(RB, 3)} N (b) {g(RA, 3)} N', f'(a) clockwise: {Wb} × {g(L / 2)} + {Wl} × {g(x)} [1]; = R_B × {g(L)} [1]; R_B = {g(RB, 3)} N [1] (b) R_A = {Wb + Wl} − {g(RB, 3)} = {g(RA, 3)} N [1] [4]' if D < 5 else
             f'(a) clockwise: {Wb} × {g(L / 2)} + {Wl} × {g(x)} [1]; uses beam weight at centre [1]; R_B × {g(L)} [1]; R_B = {g(RB, 3)} N [1] (b) R_A = {g(RA, 3)} N [1] [5]')


@t42.add('C2', (2, 3, 4), 'explain')
def t42_check(r, D):
    W1, d1, W2, d2 = r.choice([(4, 30, 3, 40), (6, 20, 4, 30), (5, 40, 8, 25), (2, 45, 3, 30), (3, 20, 4, 18), (5, 30, 6, 28)])
    bal = W1 * d1 == W2 * d2
    return Q(f'A metre rule pivoted at its centre has {W1} N hanging {d1} cm to the left and {W2} N hanging {d2} cm to the right. Determine whether it balances; if not, state which way it turns and explain.',
             'It balances: both moments are equal (' + f'{W1 * d1} N cm).' if bal else f'It does not balance: anticlockwise {W1 * d1} N cm vs clockwise {W2 * d2} N cm, so it turns {"anticlockwise (left side down)" if W1 * d1 > W2 * d2 else "clockwise (right side down)"}.',
             'both moments calculated [1]; comparison and conclusion [1] [2]')


def _pom_c4(r, D):
    W1 = r.choice([300, 400, 500, 600])
    W2 = r.choice([250, 350, 450])
    d1 = r.choice([1.0, 1.2, 1.5])
    a, b = two_people(r)
    intro = f'{a} (weight {W1} N) and {b} (weight {W2} N) sit on a see-saw pivoted at its centre. {a} sits {d1} m from the pivot.'
    parts = [
        lambda r: (f'Calculate the moment of {a}’s weight about the pivot.', f'{g(W1 * d1)} N m', '[1]'),
        lambda r: (f'Calculate where {b} must sit to balance.', f'{g(W1 * d1 / W2)} m from the pivot on the other side', 'principle of moments [1]; answer [1] [2]'),
        lambda r: ('State the size and direction of the force from the pivot when balanced (ignore the see-saw’s weight).', f'{W1 + W2} N upwards', '[2]'),
        lambda r: (f'{b} first sits at the balancing position and then moves 0.2 m further out. Describe and explain what happens.', f'{b}’s side goes down: {b}’s moment is now larger than {a}’s.', '[2]'),
        lambda r: ('Explain why the weight of a uniform see-saw pivoted at its centre does not affect the balance.', 'Its weight acts at the pivot, so it has no moment about the pivot.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t42.add('C4', (2, 3, 4, 5), 'multi_step')(_pom_c4)

N43 = 'Centre of gravity and stability'
t43 = topic(N43, N43.lower(), 'centre of gravity', 'stability')
FX(t43, 'C1', (1, 2), [
    ('What is meant by the centre of gravity of an object?', 'The point through which its whole weight appears to act', 'Weight can be treated as acting at one point.', ['The point where its mass is zero', 'The heaviest part of the object', 'Always the geometric centre of any object']),
    ('Which change makes a bus more stable?', 'Lowering its centre of gravity', 'Low centre of gravity and wide base increase stability.', ['Loading luggage on the roof', 'Making the wheelbase narrower', 'Raising the seats']),
    ('An object will topple when', 'the line of action of its weight falls outside its base', 'Then the weight has a moment that turns it further over.', ['its centre of gravity is low', 'its base is wide', 'it is tilted by any small angle']),
    ('Where is the centre of gravity of a uniform rectangular sheet?', 'Where the diagonals cross', 'By symmetry, at the centre.', ['At one corner', 'Half-way along one edge', 'Outside the sheet']),
    ('Which apparatus is used to find the centre of gravity of an irregular flat card?', 'A plumb line and a pin', 'Hang the card from a pin and draw the vertical plumb line from two or more points.', ['A newton meter only', 'A measuring cylinder', 'A thermometer']),
    ('State two features that make an object stable.', 'A low centre of gravity and a wide base.', 'low CG [1]; wide base [1] [2]'),
])
FX(t43, 'C2', (1, 2, 3, 4), [
    ('Describe how to find the centre of gravity of an irregularly shaped piece of card.', 'Hang the card freely from a pin through a hole near the edge; hang a plumb line from the pin and mark its line; repeat from another hole; the centre of gravity is where the lines cross.', 'suspend freely from a point [1]; plumb line marked [1]; repeat; intersection [1] [3]'),
    ('Explain why a racing car is built low and wide.', 'Low centre of gravity and wide wheelbase mean the line of action of the weight stays inside the base even when tilted on bends, so it is less likely to topple.', 'low CG [1]; wide base [1]; line of action stays inside base [1] [3]'),
    ('Explain why a tall glass of water is more likely to fall over than a short wide one.', 'The tall glass has a higher centre of gravity and narrower base, so a smaller tilt moves the line of action of the weight outside the base.', 'higher CG / narrower base [1]; smaller tilt needed to move weight outside base [1] [2]'),
    ('Explain, using moments, why a tilted object falls back to its original position if the line of action of its weight is inside the base.', 'The weight then has a moment about the edge of the base that turns the object back towards its original position.', 'weight’s moment about pivot edge [1]; restoring direction [1] [2]'),
    ('Explain why a person carrying a heavy bag in one hand leans the other way.', 'Leaning moves the combined centre of gravity back over the feet (base), so the line of action of the weight stays within the base.', 'combined CG [1]; kept over feet / base [1] [2]'),
])


@t43.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t43_tip(r, D):
    obj = r.choice(['A filing cabinet', 'A tall bookcase', 'A loaded van', 'A lamp', 'A wooden block', 'A tractor on a hillside', 'A traffic cone'])
    w = r.choice([0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1.6, 2.0])
    h = round(w * r.choice([0.6, 0.8, 1.0, 1.25, 1.5, 2.0]), 2)
    ang = math.degrees(math.atan((w / 2) / h))
    if D <= 2:
        th = r.choice([10, 15, 20, 25, 30, 40, 50])
        tips = th > ang
        opts, a = mcq(r, 'Yes, the weight acts outside the base' if tips else 'No, the weight still acts inside the base',
                      ['Yes, the weight acts outside the base' if not tips else 'No, the weight still acts inside the base', 'Yes, because its centre of gravity is above the base', 'No, because tilting never changes stability'])
        if D == 1:
            return Q(f'{obj} has a base {g(w)} m wide and its centre of gravity is {g(h)} m above the centre of the base. The critical tilt angle is {g(ang, 3)}°. It is tilted by {th}°. Will it topple?', a, f'Topples if the tilt exceeds {g(ang, 3)}°: {th}° {">" if tips else "<"} {g(ang, 3)}°.', opts=opts)
        return Q(f'{obj} has a base {g(w)} m wide and its centre of gravity is {g(h)} m above the centre of the base. It is tilted about one edge by {th}°. Its critical angle is {g(ang, 3)}°. State whether it falls over and explain.',
                 ('It topples: ' if tips else 'It falls back: ') + f'the tilt is {"more" if tips else "less"} than {g(ang, 3)}°, so the line of action of the weight is {"outside" if tips else "inside"} the base.', 'decision [1]; line of action vs base [1] [2]')
    if D == 3:
        return Q(f'{obj} has a base {g(w)} m wide and its centre of gravity is {g(h)} m above the centre of the base. Calculate the angle through which it can be tilted about one edge before it topples.', f'{g(ang, 3)}°',
                 f'topples when CG is vertically above the edge [1]; tan θ = {g(w / 2)}/{g(h)} [1]; θ = {g(ang, 3)}° [1] [3]')
    h2 = round(h * r.choice([0.5, 0.6, 0.75]), 2)
    a2 = math.degrees(math.atan((w / 2) / h2))
    return Q(f'{obj} has a base {g(w)} m wide and its centre of gravity is {g(h)} m above the centre of the base. (a) Calculate the maximum tilt before it topples. (b) Heavy items are moved to the bottom, lowering the centre of gravity to {g(h2)} m. Calculate the new maximum tilt. (c) Explain why this makes it more stable.',
             f'(a) {g(ang, 3)}° (b) {g(a2, 3)}° (c) a lower centre of gravity must be tilted further before the line of action of the weight passes outside the base.',
             f'(a) tan θ = {g(w / 2)}/{g(h)}; {g(ang, 3)}° [2] (b) tan θ = {g(w / 2)}/{g(h2)}; {g(a2, 3)}° [1] (c) larger angle before weight acts outside base [1]' + (' [4]' if D == 4 else '; restoring moment explained [1] [5]'), 'multi_step')


@t43.add('C2', (2, 3, 4), 'explain')
def t43_design(r, D):
    o = r.choice(['a baby’s high chair', 'a desk lamp', 'a double-decker bus', 'a wine glass', 'a laboratory Bunsen burner', 'a racing car', 'a camera tripod', 'a step-ladder'])
    return Q(f'Suggest and explain two design features that make {o} stable.', 'Wide base (feet spread out) and low centre of gravity (heavy base / weight kept low), so the line of action of the weight stays within the base when it is tilted.',
             'wide base with reason [1]; low CG with reason [1]; link to line of action of weight within base [1] [3]')


def _cg_c4(r, D):
    o = r.choice(['a tall cupboard', 'a delivery lorry', 'a lamp post-base', 'a stacking robot'])
    w = r.choice([0.6, 0.8, 1.0])
    h = r.choice([0.8, 1.0, 1.2, 1.5])
    ang = math.degrees(math.atan(w / 2 / h))
    W = r.choice([300, 500, 800, 1200])
    parts = [
        lambda r: ('State what is meant by its centre of gravity.', 'The point through which its weight appears to act.', '[1]'),
        lambda r: ('Calculate the maximum angle it can be tilted before toppling.', f'{g(ang, 3)}°', f'tan θ = {g(w / 2)}/{g(h)} [2]'),
        lambda r: (f'It is tilted slightly about one bottom edge. Calculate the moment of its {W} N weight about that edge when the weight acts 0.1 m horizontally inside the edge.', f'{g(W * 0.1)} N m', f'{W} × 0.1 [1]'),
        lambda r: ('Explain why it returns to upright when released from a small tilt.', 'The weight acts inside the base, giving a moment about the edge that turns it back.', '[2]'),
        lambda r: ('Suggest two ways to make it harder to topple.', 'Lower the centre of gravity (heavy items at the bottom); widen the base.', '[2]'),
    ]
    return compose(r, f'Consider {o} with a base {g(w)} m wide and its centre of gravity {g(h)} m above the centre of the base.', parts, k=(2, 3, 4), type_='multi_step')


t43.add('C4', (2, 3, 4, 5), 'multi_step')(_cg_c4)

CHAPTERS[4] = [t41, t42, t43]

# =========================================================== 5 Forces and matter
N51 = "Effects of forces on shape: load-extension graphs, Hooke's law and limit of proportionality"
t51 = topic(N51, N51.lower(), "hooke's law", 'load-extension graphs', 'limit of proportionality')
FX(t51, 'C1', (1, 2), [
    ('Which of these is an effect a force can have on an object?', 'Changing its shape', 'Forces can change speed, direction or shape (size).', ['Changing its mass', 'Changing its density permanently by heating', 'Changing its colour']),
    ('The extension of a spring is', 'its stretched length minus its original length', 'extension = new length − original (unloaded) length.', ['its stretched length', 'its original length', 'the load divided by its length']),
    ('Hooke’s law states that, up to the limit of proportionality,', 'the extension is directly proportional to the load', 'F ∝ x for a spring obeying Hooke’s law.', ['the length is proportional to the load', 'the extension is inversely proportional to the load', 'the extension is constant']),
    ('On a load-extension graph, where does the limit of proportionality occur?', 'Where the straight line starts to curve', 'Beyond this point extension is no longer proportional to load.', ['At the origin', 'Where the graph is steepest', 'Where the load is zero']),
    ('A spring is stretched beyond its elastic limit. When the load is removed, it', 'does not return to its original length', 'Permanent deformation beyond the elastic limit.', ['returns to its original length', 'becomes shorter than originally', 'snaps immediately']),
    ('State what is meant by the limit of proportionality.', 'The point beyond which the extension is no longer proportional to the load.', '[1]'),
])
FX(t51, 'C2', (1, 2, 3, 4), [
    ('Describe how to obtain a load-extension graph for a spring.', 'Clamp the spring next to a vertical metre rule; record the unloaded length; add masses one at a time, recording the length each time; extension = length − original length; plot load against extension.', 'set-up with ruler and pointer [1]; add loads and record length [1]; calculate extension and plot [1] [3]'),
    ('Explain how a load-extension graph shows that a spring obeys Hooke’s law.', 'The graph is a straight line through the origin, showing extension is directly proportional to load.', 'straight line [1]; through origin [1] [2]'),
    ('Explain why a student should check the spring’s length after removing the loads.', 'If the length has not returned to the original, the spring has been stretched beyond its elastic limit and permanently deformed.', 'check return to original length [1]; elastic limit / permanent deformation [1] [2]'),
    ('Describe how the load-extension graph for a rubber band differs from that for a steel spring.', 'The rubber band’s graph is curved (not proportional) from early on, and it does not obey Hooke’s law; the spring is straight up to its limit of proportionality.', 'rubber curved / non-linear [1]; spring straight to limit [1] [2]'),
    ('Explain why a pointer and eye-level reading are used when measuring the length of a loaded spring.', 'A pointer fixed to the bottom of the spring gives a definite mark on the scale; reading at eye level avoids parallax error.', 'pointer [1]; parallax [1] [2]'),
])


def _spring_data(r):
    L0 = r.choice([2.0, 3.0, 4.0, 5.0, 6.0, 8.0])
    k = r.choice([0.5, 0.8, 1.0, 1.25, 2.0, 2.5])  # cm per N
    loads = [0, 1, 2, 3, 4, 5, 6]
    lp = r.choice([4, 5])
    lens = []
    for F in loads:
        x = F * k if F <= lp else lp * k + (F - lp) * k * r.choice([1.6, 1.8, 2.0])
        lens.append(round(L0 + x, 1))
    return L0, k, loads, lens, lp


@t51.add('C3', (1, 2, 3, 4, 5), 'case')
def t51_table(r, D):
    L0, k, loads, lens, lp = _spring_data(r)
    who = person(r)
    tab = f'{who} loads a spring and records: load/N = {", ".join(map(str, loads))}; length/cm = {", ".join(g(x) for x in lens)}.'
    if D <= 2:
        F = r.choice([1, 2, 3])
        x = lens[F] - L0
        return numq(r, D, tab, f'extension for a load of {F} N', x, ' cm', f'extension = {g(lens[F])} − {g(L0)}', [lens[F], L0, x * 2])
    if D == 3:
        return Q(tab + ' Calculate the extension for each load up to 3 N and state whether the spring obeys Hooke’s law over this range, giving a reason.', f'{", ".join(g(lens[i] - L0) for i in range(4))} cm; yes: extension is proportional to load ({g(k)} cm per N).',
                 f'extensions correct [1]; equal increases of {g(k)} cm per N / proportional [1]; conclusion [1] [3]')
    return Q(tab + ' (a) Calculate the extension at each load. (b) Identify the load at which the limit of proportionality is passed and explain how the data show this. (c) Predict the extension for a load of 2.5 N.',
             f'(a) {", ".join(g(x - L0) for x in lens)} cm (b) after {lp} N: the extension increases by more than {g(k)} cm per newton. (c) {g(2.5 * k)} cm',
             f'(a) extensions [1] (b) limit between {lp} and {lp + 1} N [1]; increments no longer equal [1] (c) 2.5 × {g(k)} = {g(2.5 * k)} cm [1]' + (' [4]' if D == 4 else '; graph straight line through origin up to the limit then curving [1] [5]'), 'case')


@t51.add('C2', (2, 3, 4), 'explain')
def t51_err(r, D):
    L0, k, loads, lens, lp = _spring_data(r)
    who = person(r)
    F = r.choice([2, 3])
    return Q(f'A spring has an unloaded length of {g(L0)} cm and is {g(lens[F])} cm long with a load of {F} N. {who} predicts that a {2 * F} N load will make the spring {g(2 * lens[F])} cm long. Explain the mistake and give the correct prediction (assume Hooke’s law applies).',
             f'{who} doubled the length instead of the extension. Extension = {g(lens[F] - L0)} cm, so for {2 * F} N it is {g(2 * (lens[F] - L0))} cm and the length is {g(L0 + 2 * (lens[F] - L0))} cm.',
             f'extension (not length) ∝ load [1]; correct extension [1]; correct length [1] [3]')


def _hooke_c4(r, D):
    L0, k, loads, lens, lp = _spring_data(r)
    intro = f'A student hangs loads on a spring of original length {g(L0)} cm: load/N 0–6 in 1 N steps; length/cm = {", ".join(g(x) for x in lens)}.'
    parts = [
        lambda r: ('Calculate the extension for a load of 3 N.', f'{g(lens[3] - L0)} cm', '[1]'),
        lambda r: ('Describe the shape of the load-extension graph.', f'Straight line through the origin up to {lp} N, then curving (extension increasing faster).', 'straight through origin [1]; curves after limit [1] [2]'),
        lambda r: ('Calculate the spring constant in N/m using the straight part.', f'{g(1 / (k / 100))} N/m', f'k = F/x = 1 N/{g(k / 100)} m [2]'),
        lambda r: ('State the load at the limit of proportionality.', f'{lp} N (approximately)', '[1]'),
        lambda r: ('Describe how the student could test whether the spring has gone beyond its elastic limit.', 'Remove all loads and see whether the spring returns to its original length.', '[2]'),
        lambda r: ('State two safety precautions.', 'Wear eye protection; place a tray/soft surface under the masses; do not overload.', 'any two [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t51.add('C4', (2, 3, 4, 5), 'case')(_hooke_c4)

N52 = 'Spring constant k = F/x'
t52 = topic(N52, N52.lower(), 'spring constant')
FX(t52, 'C1', (1, 2, 3), [
    ('What is the unit of the spring constant?', 'N/m', 'k = F/x: newtons per metre.', ['N m', 'm/N', 'N/m²']),
    ('A spring with k = 50 N/m is stretched by 0.10 m. What force is needed?', '5.0 N', 'F = kx = 50 × 0.10 = 5.0 N.', ['500 N', '0.002 N', '50.1 N']),
    ('A stiffer spring has', 'a larger spring constant', 'Larger k: more force per metre of extension.', ['a smaller spring constant', 'no spring constant', 'a larger extension for the same load']),
    ('On a load-extension graph (load on y-axis), the spring constant is', 'the gradient of the straight part', 'k = ΔF/Δx.', ['the area under the graph', 'the intercept', 'the reciprocal of the area']),
    ('Define the spring constant.', 'The force per unit extension (k = F/x).', '[1]'),
])
FX(t52, 'C2', (1, 2, 3, 4), [
    ('Two springs are tested. Spring P extends 4 cm and spring Q extends 8 cm under the same load. Explain which has the larger spring constant.', 'P: k = F/x, so for the same force a smaller extension means a larger k (stiffer).', 'P [1]; k = F/x with smaller x [1] [2]'),
    ('Explain why the spring constant can only be calculated from the straight part of a load-extension graph.', 'Only there is extension proportional to load, so F/x is constant; beyond the limit of proportionality F/x changes.', 'proportional region [1]; F/x not constant beyond [1] [2]'),
    ('Explain why the extension must be in metres when calculating k in N/m.', 'The unit N/m requires force in newtons divided by extension in metres; using cm would give a value 100 times too small.', 'unit consistency [1]; factor of 100 [1] [2]'),
])
SPRK = {'a car suspension spring': [20000, 25000, 30000, 40000, 50000], 'a spring in a newton meter': [20, 25, 40, 50, 80, 100], 'a trampoline spring': [2000, 2500, 4000, 5000],
        'a spring in a ballpoint pen': [100, 200, 250, 400, 500], 'a bungee cord (in its linear region)': [40, 50, 80, 100, 120], 'a mattress spring': [500, 800, 1000, 1200], 'a door-closer spring': [200, 250, 400, 500]}
SPR = list(SPRK)


@t52.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t52_k(r, D):
    o = r.choice(SPR)
    k = r.choice(SPRK[o])
    xcm = r.choice([1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12])
    if 'car' in o or 'trampoline' in o or 'mattress' in o:
        xcm = r.choice([1, 1.5, 2, 3, 4, 5])
    if 'pen' in o:
        xcm = r.choice([0.2, 0.25, 0.4, 0.5, 0.8])
    x = xcm / 100
    F = k * x
    which = r.choice(['k', 'F', 'x'])
    if D <= 2:
        if which == 'k':
            return numq(r, D, f'A force of {g(F)} N stretches {o} by {g(x)} m.', 'spring constant', k, ' N/m', f'k = F/x = {g(F)}/{g(x)}', [F * x, x / F, k / 100])
        if which == 'F':
            return numq(r, D, f'{cap(o)} has a spring constant of {g(k)} N/m and is stretched by {g(x)} m.', 'force needed', F, ' N', f'F = kx = {g(k)} × {g(x)}', [k / x, k * xcm, x / k])
        return numq(r, D, f'{cap(o)} has a spring constant of {g(k)} N/m. A force of {g(F)} N is applied.', 'extension', x, ' m', f'x = F/k = {g(F)}/{g(k)}', [F * k, k / F, xcm])
    if D == 3:
        return Q(f'A force of {g(F)} N stretches {o} by {g(xcm)} cm. Calculate the spring constant in N/m.', f'{g(k)} N/m', f'x = {g(x)} m [1]; k = F/x [1] = {g(k)} N/m [1] [3]')
    m = round(F / 9.8, 2)
    F2 = F * r.choice([0.5, 1.5, 2])
    return Q(f'A mass of {g(m)} kg hung on {o} stretches it by {g(xcm, 3)} cm (g = 9.8 N/kg). (a) Calculate the weight of the mass. (b) Calculate the spring constant. (c) Calculate the extension for a load of {g(F2, 3)} N, assuming the limit of proportionality is not reached.',
             f'(a) {g(m * 9.8, 3)} N (b) {g(m * 9.8 / x, 3)} N/m (c) {g(F2 / (m * 9.8 / x) * 100, 3)} cm',
             f'(a) W = mg = {g(m * 9.8, 3)} N [1] (b) k = {g(m * 9.8, 3)}/{g(x)} = {g(m * 9.8 / x, 3)} N/m [2] (c) x = F/k = {g(F2 / (m * 9.8 / x) * 100, 3)} cm [1]' + (' [4]' if D == 4 else '; assumption stated (Hooke’s law / within limit) [1] [5]'), 'multi_step')


relation(t52, 'C2', (2, 3), 'F = kx', 'extension', {'load': 1}, ['A spring obeys Hooke’s law.', 'A newton meter spring is used within its limit of proportionality.', 'A suspension spring is loaded in its linear region.'])


def _k_c4(r, D):
    k1, k2 = r.sample([20, 25, 40, 50, 80, 100], 2)
    F = r.choice([2, 4, 5, 8, 10])
    intro = f'Two springs A (k = {k1} N/m) and B (k = {k2} N/m) are tested by {person(r)}.'
    parts = [
        lambda r: (f'Calculate the extension of A for a load of {F} N.', f'{g(F / k1)} m', 'x = F/k [2]'),
        lambda r: (f'Calculate the extension of B for the same load.', f'{g(F / k2)} m', '[1]'),
        lambda r: ('State which spring is stiffer and explain.', f'{"A" if k1 > k2 else "B"}: larger k, smaller extension per newton.', '[2]'),
        lambda r: ('Describe how the load-extension graphs of the two springs would differ.', f'Both straight lines through the origin (in the linear region); the stiffer spring has the steeper line if load is on the y-axis.', '[2]'),
        lambda r: ('Suggest which spring would be better for a newton meter that must measure forces up to 1 N precisely, and why.', f'{"A" if k1 < k2 else "B"}: lower k gives larger extension per newton, so readings are more precise.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t52.add('C4', (2, 3, 4, 5), 'multi_step')(_k_c4)

N53 = 'Pressure p = F/A'
t53 = topic(N53, N53.lower(), 'pressure')
FX(t53, 'C1', (1, 2), [
    ('Which equation defines pressure?', 'pressure = force ÷ area', 'p = F/A.', ['pressure = force × area', 'pressure = area ÷ force', 'pressure = mass ÷ area']),
    ('What is the unit of pressure?', 'pascal (Pa)', '1 Pa = 1 N/m².', ['newton (N)', 'joule (J)', 'N m']),
    ('Why do snowshoes stop a person sinking into snow?', 'They spread the weight over a larger area, reducing the pressure', 'Larger area → smaller pressure for the same force.', ['They increase the person’s weight', 'They reduce the person’s mass', 'They increase the pressure on the snow']),
    ('Why is a sharp knife better for cutting than a blunt one?', 'The small area of the blade gives a large pressure', 'Same force on smaller area → larger pressure.', ['The sharp knife is heavier', 'The sharp knife has a larger area', 'Pressure does not affect cutting']),
    ('A force of 100 N acts on an area of 2 m². What is the pressure?', '50 Pa', 'p = 100/2 = 50 Pa.', ['200 Pa', '0.02 Pa', '102 Pa']),
    ('How many square metres are there in 1 cm²?', '0.0001 m²', '1 cm² = (0.01 m)² = 1 × 10⁻⁴ m².', ['0.01 m²', '0.001 m²', '100 m²']),
])
FX(t53, 'C2', (1, 2, 3, 4), [
    ('Explain why a drawing pin has a broad head and a sharp point.', 'The sharp point has a tiny area so the pressure is large enough to pierce the board; the broad head spreads the force over a large area so the pressure on the thumb is small.', 'point small area → high pressure [1]; head large area → low pressure on thumb [1] [2]'),
    ('Explain why tractors have wide tyres.', 'Wide tyres spread the weight over a larger area, reducing the pressure on soft ground so the tractor does not sink.', 'larger area [1]; smaller pressure, less sinking [1] [2]'),
    ('Explain why a woman in stiletto heels can damage a wooden floor that an elephant walking on it would not.', 'The heel area is tiny so the pressure under it can be very large even though her weight is much smaller; the elephant’s weight is spread over large feet.', 'small area high pressure [1]; comparison with large area [1] [2]'),
    ('Explain why a brick exerts different pressures on the ground depending on which face it rests on, although its weight is the same.', 'Pressure = weight ÷ area of contact; different faces have different areas, so the smallest face gives the largest pressure.', 'p = F/A [1]; smallest area gives largest pressure [1] [2]'),
])
PRESS = [('A brick of weight {F} N rests on a face measuring {a} cm × {b} cm.', 'brick'), ('A person of weight {F} N stands on both feet, each with a contact area of {a} cm × {b} cm.', 'feet2'),
         ('A crate of weight {F} N stands on a base {a} cm × {b} cm.', 'crate'), ('An elephant of weight {F} N stands on four feet, each of area {a} cm × {b} cm.', 'feet4'),
         ('A car tyre presses on the road with a force of {F} N over a contact patch {a} cm × {b} cm.', 'tyre')]


@t53.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t53_p(r, D):
    if D <= 2:
        F = r.choice([20, 40, 50, 60, 100, 120, 200, 500, 600, 750])
        A = r.choice([0.01, 0.02, 0.04, 0.05, 0.1, 0.2, 0.25, 0.5, 2])
        o = r.choice(['A box', 'A stack of books', 'A table leg', 'A concrete block', 'A suitcase', 'A water tank'])
        if r.random() < 0.6:
            return numq(r, D, f'{o} exerts a force of {F} N on an area of {g(A)} m².', 'pressure', F / A, ' Pa', f'p = F/A = {F}/{g(A)}', [F * A, A / F, F / A / 100])
        p = F / A
        return numq(r, D, f'{o} exerts a pressure of {g(p)} Pa on an area of {g(A)} m².', 'force', F, ' N', f'F = pA = {g(p)} × {g(A)}', [p / A, A / p * 1e4, F * 10])
    fr, kind = r.choice(PRESS)
    a, b = r.choice([(10, 20), (20, 10), (8, 25), (12, 15), (20, 30), (15, 10), (6, 4), (5, 12)])
    F = {'brick': r.choice([20, 25, 30, 40]), 'feet2': r.choice([500, 600, 700, 800]), 'crate': r.choice([800, 1200, 2000]), 'feet4': r.choice([40000, 50000, 60000]), 'tyre': r.choice([3000, 3500, 4000])}[kind]
    if kind == 'feet4':
        a, b = r.choice([(40, 40), (45, 40), (50, 40)])
    n = {'feet2': 2, 'feet4': 4}.get(kind, 1)
    A = n * a * b / 1e4
    p = F / A
    s = fr.format(F=F, a=a, b=b)
    if D == 3:
        return Q(s + ' Calculate the pressure on the ground in Pa.', f'{g(p, 3)} Pa', f'A = {n if n > 1 else ""}{" × " if n > 1 else ""}{a} × {b} cm² = {g(A, 3)} m² [1]; p = F/A [1] = {g(p, 3)} Pa [1] [3]')
    return Q(s + f' (a) Calculate the total contact area in m². (b) Calculate the pressure. (c) Calculate the pressure if the {"person stands on one foot" if kind == "feet2" else "contact area is halved"} and explain the effect on soft ground.',
             f'(a) {g(A, 3)} m² (b) {g(p, 3)} Pa (c) {g(2 * p, 3)} Pa: doubled pressure, so it sinks further into soft ground.',
             f'(a) cm² → m² ({g(A, 3)} m²) [1] (b) p = F/A = {g(p, 3)} Pa [1] (c) {g(2 * p, 3)} Pa [1]; sinks more [1]' + (' [4]' if D == 4 else '; area halves so pressure doubles (inverse proportion) [1] [5]'), 'multi_step')


relation(t53, 'C2', (2, 3), 'p = F/A', 'pressure', {'force': 1, 'contact area': -1}, ['A forklift truck stands on a warehouse floor.', 'A hiker walks across soft snow.', 'An engineer designs the base of a heavy machine.'])


def _p_c4(r, D):
    m = r.choice([600, 800, 1000, 1200])
    W = m * 9.8
    A = r.choice([0.2, 0.25, 0.4, 0.5])
    pmax = r.choice([5000, 8000, 10000, 15000])
    intro = f'A machine of mass {m} kg is to be placed on a floor in {city(r)} that can safely withstand a pressure of {pmax} Pa. Its base has an area of {A} m² (g = 9.8 N/kg).'
    parts = [
        lambda r: ('Calculate the weight of the machine.', f'{g(W, 3)} N', '[1]'),
        lambda r: ('Calculate the pressure under the base.', f'{g(W / A, 3)} Pa', 'p = F/A [2]'),
        lambda r: ('State whether the floor is safe and justify your answer.', 'Safe' + ('' if W / A <= pmax else ' only if a larger base is used') + f': {g(W / A, 3)} Pa {"≤" if W / A <= pmax else ">"} {pmax} Pa.', '[1]'),
        lambda r: ('Calculate the minimum area of base needed.', f'{g(W / pmax, 3)} m²', f'A = F/p = {g(W, 3)}/{pmax} [2]'),
        lambda r: ('Suggest how this area could be achieved.', 'Stand the machine on a wide metal plate / board to spread its weight.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t53.add('C4', (2, 3, 4, 5), 'multi_step')(_p_c4)

N54 = 'Pressure in liquids Δp = ρgΔh'
t54 = topic(N54, N54.lower(), 'pressure in liquids')
FX(t54, 'C1', (1, 2), [
    ('Pressure in a liquid increases with', 'depth and density of the liquid', 'Δp = ρgΔh.', ['the area of the container', 'the shape of the container', 'the volume of liquid only']),
    ('At a given depth, the pressure in a liquid acts', 'equally in all directions', 'Liquid pressure acts in all directions at a point.', ['only downwards', 'only upwards', 'only sideways']),
    ('Why are dams built thicker at the bottom than at the top?', 'Water pressure is greater at greater depth', 'Pressure increases with depth, so the base must withstand a larger force.', ['Water is denser at the top', 'The top must hold more water', 'Air pressure is greater at the bottom']),
    ('Water has density 1000 kg/m³. What is the pressure due to the water 2.0 m below the surface? (g = 9.8 N/kg)', '19 600 Pa', 'Δp = ρgh = 1000 × 9.8 × 2.0 = 19 600 Pa.', ['2000 Pa', '9800 Pa', '196 Pa']),
    ('Atmospheric pressure at sea level is about', '100 000 Pa (100 kPa)', 'About 1.0 × 10⁵ Pa.', ['100 Pa', '10 Pa', '1 Pa']),
])
FX(t54, 'C2', (1, 2, 3, 4), [
    ('Water spurts from holes at different heights in the side of a tall container. Explain why water from the lowest hole travels furthest.', 'The lowest hole is deepest, so the pressure there is greatest and water is pushed out fastest.', 'deepest point [1]; greatest pressure [1] [2]'),
    ('Explain why a diver’s ears hurt more at 10 m depth than at 2 m.', 'Pressure increases with depth (Δp = ρgh); at 10 m the extra pressure on the eardrum is five times larger.', 'pressure increases with depth [1]; quantitative or force on eardrum [1] [2]'),
    ('Explain why the pressure at the bottom of a narrow tube of water 0.5 m tall is the same as at the bottom of a wide tank of water 0.5 m deep.', 'Liquid pressure depends only on depth, density and g, not on the width or volume of the container.', 'depends on ρ, g, h only [1]; not area/volume [1] [2]'),
    ('Explain why the total pressure on a diver is greater than ρgh.', 'Atmospheric pressure also acts on the water surface, so total pressure = atmospheric pressure + ρgh.', 'atmospheric pressure adds [1]; p = p_atm + ρgh [1] [2]'),
])
FLU = [('fresh water', 1000), ('sea water', 1030), ('oil', 800), ('mercury', 13600), ('brine', 1200)]

DEP = {'fresh water': ['at the bottom of a swimming pool', 'at the base of a water tower', 'at the bottom of a lake near {c}', 'at the bottom of a reservoir'],
       'sea water': ['at the depth of a submarine', 'at the depth of a scuba diver', 'on the hull of a ship', 'at the depth of a coral reef'],
       'oil': ['at the bottom of an oil storage tank', 'at the base of a tanker’s oil hold'], 'brine': ['at the bottom of a salt-works brine tank', 'at the bottom of a pickling vat'],
       'mercury': ['at the bottom of a mercury column in a barometer tube', 'at the bottom of a tube of mercury in a laboratory']}


@t54.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t54_p(r, D):
    liq, rho = r.choice(FLU)
    h = r.choice([0.5, 1.2, 2.0, 2.5, 3.0, 4.0, 5.0, 8.0, 12, 20, 40])
    if liq == 'mercury':
        h = r.choice([0.1, 0.2, 0.25, 0.5, 0.76])
    if liq in ('oil', 'brine'):
        h = r.choice([0.8, 1.2, 2.0, 2.5, 3.0, 4.0, 6.0])
    where = r.choice(DEP[liq]).format(c=city(r))
    p = rho * G * h
    if D <= 2:
        return numq(r, D, f'A point {where} is {g(h)} m below the surface of {liq} (density {g(rho)} kg/m³, g = 9.8 N/kg).', 'pressure due to the liquid', p, ' Pa', f'Δp = ρgΔh = {rho} × 9.8 × {g(h)}', [rho * h, p / 9.8 / 9.8, rho * G / h])
    if D == 3:
        if r.random() < 0.5:
            return Q(f'The pressure due to {liq} (density {g(rho)} kg/m³) {where} is {g(p, 3)} Pa (g = 9.8 N/kg). Calculate the depth.', f'{g(h, 3)} m', f'Δh = Δp/(ρg) [1] = {g(p, 3)}/({rho} × 9.8) [1] = {g(h, 3)} m [1] [3]')
        return Q(f'A point {where} is {g(h)} m below the surface of {liq} (density {g(rho)} kg/m³, g = 9.8 N/kg). Calculate the pressure due to the liquid in kPa.', f'{g(p / 1000, 3)} kPa', f'Δp = ρgΔh [1] = {g(p, 3)} Pa [1] = {g(p / 1000, 3)} kPa [1] [3]')
    patm = 1.0e5
    A = r.choice([0.01, 0.02, 0.05, 0.1])
    return Q(f'A window of area {g(A)} m² is {g(h)} m below the surface of {liq} (density {g(rho)} kg/m³, g = 9.8 N/kg; atmospheric pressure = 1.0 × 10⁵ Pa). (a) Calculate the pressure due to the liquid. (b) Calculate the total pressure on the window. (c) Calculate the force on the window due to the total pressure.',
             f'(a) {g(p, 3)} Pa (b) {g(p + patm, 3)} Pa (c) {g((p + patm) * A, 3)} N',
             f'(a) ρgΔh = {g(p, 3)} Pa [1] (b) + 1.0 × 10⁵ = {g(p + patm, 3)} Pa [1] (c) F = pA = {g((p + patm) * A, 3)} N [2]' + (' [4]' if D == 4 else '; units/significant figures [1] [5]'), 'multi_step')


@t54.add('C3', (2, 3, 4), 'numerical')
def t54_compare(r, D):
    (l1, r1), (l2, r2) = r.sample(FLU[:3] + FLU[4:], 2)
    h1 = r.choice([1.0, 2.0, 3.0, 4.0])
    h2 = h1 * r1 / r2
    return Q(f'At a depth of {g(h1)} m in {l1} (density {r1} kg/m³), the pressure due to the liquid is p. Calculate the depth in {l2} (density {r2} kg/m³) at which the liquid pressure is also p.', f'{g(h2, 3)} m',
             f'ρ₁gh₁ = ρ₂gh₂ [1]; h₂ = {r1} × {g(h1)}/{r2} [1] = {g(h2, 3)} m [1] [3]')


relation(t54, 'C2', (2, 3), 'Δp = ρgΔh', 'pressure due to the liquid', {'depth': 1, 'density of the liquid': 1}, ['An engineer studies the pressure on the wall of a storage tank.', 'A diver investigates pressure underwater.', 'A student studies pressure at the bottom of a column of liquid.'])


def _lp_c4(r, D):
    h = r.choice([10, 15, 20, 30, 50])
    rho = 1030
    p = rho * G * h
    intro = r.choice([f'A diver descends to {h} m in sea water (density 1030 kg/m³) near {coast(r)}. Atmospheric pressure is 1.0 × 10⁵ Pa; g = 9.8 N/kg.',
                      f'A remotely operated camera is lowered {h} m into the sea (density 1030 kg/m³). Atmospheric pressure is 1.0 × 10⁵ Pa; g = 9.8 N/kg.'])
    parts = [
        lambda r: ('Calculate the pressure due to the water at this depth.', f'{g(p, 3)} Pa', 'ρgh [2]'),
        lambda r: ('Calculate the total pressure.', f'{g(p + 1e5, 3)} Pa', '[1]'),
        lambda r: ('Calculate the force from the total pressure on a viewing window of area 0.015 m².', f'{g((p + 1e5) * 0.015, 3)} N', 'F = pA [2]'),
        lambda r: ('Explain why the pressure acts on the mask from all directions.', 'Pressure in a fluid at a point acts equally in all directions.', '[1]'),
        lambda r: ('Calculate the depth at which the pressure due to the water equals atmospheric pressure.', f'{g(1e5 / (rho * G), 3)} m', 'h = p/(ρg) [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t54.add('C4', (2, 3, 4, 5), 'multi_step')(_lp_c4)

CHAPTERS[5] = [t51, t52, t53, t54]

# =========================================================== 6 Energy stores and transfers
STORES = ['kinetic', 'gravitational potential', 'chemical', 'elastic (strain)', 'nuclear', 'electrostatic', 'internal (thermal)', 'magnetic']
SCN = [  # scenario, from store, to store(s), transfer pathway
    ('a battery-powered torch is switched on', 'chemical', 'internal (thermal) of the surroundings', 'electrically, then by light (radiation) and heating'),
    ('a ball is dropped and falls towards the ground', 'gravitational potential', 'kinetic', 'mechanically by the force of gravity'),
    ('a stretched catapult fires a stone', 'elastic (strain)', 'kinetic', 'mechanically by the force of the elastic'),
    ('a kettle boils water', 'chemical (fuel at the power station) / electrical supply', 'internal (thermal) of the water', 'electrically and by heating'),
    ('a car brakes to a stop', 'kinetic', 'internal (thermal) of the brakes and surroundings', 'mechanically by friction, then by heating'),
    ('a person climbs a flight of stairs', 'chemical (in the muscles)', 'gravitational potential', 'mechanically by forces from the muscles'),
    ('a log burns on a campfire', 'chemical', 'internal (thermal) of the surroundings', 'by heating and radiation (light and infrared)'),
    ('a wind-up toy car runs across the floor', 'elastic (strain)', 'kinetic, then internal (thermal)', 'mechanically'),
    ('a solar-powered calculator works', 'nuclear (in the Sun)', 'internal (thermal) of the surroundings', 'by radiation (light) and electrically'),
    ('a pendulum swings from its highest point to its lowest point', 'gravitational potential', 'kinetic', 'mechanically by gravity'),
    ('a rocket launches', 'chemical', 'kinetic and gravitational potential', 'mechanically by thrust, and by heating'),
    ('a bow is used to shoot an arrow upwards', 'elastic (strain)', 'kinetic, then gravitational potential', 'mechanically'),
]
N61 = 'Energy stores and transfers and the principle of conservation of energy'
t61 = topic(N61, N61.lower(), 'energy stores', 'conservation of energy')
FX(t61, 'C1', (1, 2), [
    ('State the principle of conservation of energy.', 'Energy cannot be created or destroyed; it can only be transferred from one store to another (total energy is constant).', 'cannot be created or destroyed [1]; only transferred/total constant [1] [2]'),
    ('In which store is energy held in a stretched spring?', 'Elastic (strain)', 'Deformed elastic objects store elastic (strain) energy.', ['Kinetic', 'Chemical', 'Nuclear']),
    ('In which store is energy held in food and fuels?', 'Chemical', 'Chemical energy is released in reactions such as burning or respiration.', ['Elastic', 'Kinetic', 'Gravitational potential']),
    ('Which is NOT a way of transferring energy between stores?', 'By changing the mass of an object without any force', 'Transfers are by forces (mechanical work), electrical currents, heating, and waves (light, sound).', ['By an electric current', 'By heating', 'By a force moving an object (mechanical work)']),
    ('A moving car has energy in its', 'kinetic store', 'Moving objects have kinetic energy.', ['elastic store', 'nuclear store', 'electrostatic store']),
    ('Energy is measured in', 'joules (J)', 'SI unit of energy: joule.', ['watts (W)', 'newtons (N)', 'pascals (Pa)']),
])
FX(t61, 'C2', (1, 2, 3, 4), [
    ('Explain why a bouncing ball rises to a lower height after each bounce, using the principle of conservation of energy.', 'At each bounce some energy is transferred to the internal (thermal) store of the ball and floor and as sound, so less is left in the gravitational potential store at the top; the total energy is still conserved.', 'energy dissipated as thermal/sound [1]; less GPE at top [1]; total conserved [1] [3]'),
    ('Explain what is meant by saying that energy is "wasted" in an electric motor.', 'Some of the input energy is transferred to stores that are not useful, such as the internal store of the motor and surroundings (by heating) and sound; it spreads out and cannot easily be used.', 'transferred to non-useful stores [1]; dissipated to surroundings [1] [2]'),
    ('A student says "energy is used up when a torch battery goes flat". Explain why this is not correct.', 'The energy is not destroyed; it has been transferred from the chemical store of the battery to the internal (thermal) store of the surroundings by light and heating.', 'energy not destroyed [1]; transferred to surroundings [1] [2]'),
    ('Explain why the total energy of a system is the same before and after a transfer even when the transfer is inefficient.', 'Energy is conserved: wasted energy goes into stores such as thermal energy of the surroundings; useful + wasted = total input.', 'conservation [1]; useful + wasted = input [1] [2]'),
])


@t61.add('C2', (1, 2, 3, 4), 'explain')
def t61_scn(r, D):
    s, a, b, how = r.choice(SCN)
    if D <= 1:
        return Q(f'When {s}, name the main energy store that decreases.', cap(a) + '.', f'{cap(a)} store decreases [1]', 'short')
    return Q(f'Describe the energy transfers that take place when {s}. Name the stores involved and how the energy is transferred.', f'Energy is transferred from the {a} store to the {b} store, {how}. Some energy is dissipated to the surroundings.',
             f'initial store: {a} [1]; final store(s) [1]; transfer pathway / dissipation [1] [3]' if D >= 3 else f'initial store [1]; final store [1] [2]')


@t61.add('C1', (1, 2, 3))
def t61_store(r, D):
    s, a, b, how = r.choice([x for x in SCN if '/' not in x[1]])
    first = a.split(' (')[0] if '(' in a and 'strain' not in a else a
    opts, ans = mcq(r, a, [x for x in STORES if x != a and x.split(' (')[0] != a.split(' (')[0]])
    return Q(f'When {s}, which energy store decreases?', ans, f'{cap(a)} store decreases; energy goes to the {b} store.', opts=opts)


@t61.add('C3', (1, 2, 3, 4), 'numerical')
def t61_cons(r, D):
    dev = r.choice([('an electric motor', 'kinetic', 'thermal and sound'), ('a filament lamp', 'light', 'thermal'), ('a loudspeaker', 'sound', 'thermal'), ('a petrol engine', 'kinetic', 'thermal'),
                    ('a hairdryer', 'thermal (of the air) and kinetic', 'sound'), ('an LED lamp', 'light', 'thermal'), ('a solar panel', 'electrical', 'thermal')])
    Ein = r.choice([200, 500, 800, 1000, 1200, 2000, 2400, 5000])
    frac = r.choice([0.05, 0.1, 0.2, 0.25, 0.3, 0.4, 0.6, 0.75, 0.85])
    use = Ein * frac
    if D <= 2:
        return numq(r, D, f'{cap(dev[0])} is supplied with {Ein} J of energy and transfers {g(use)} J usefully as {dev[1]} energy.', 'energy wasted', Ein - use, ' J', f'wasted = {Ein} − {g(use)}', [Ein + use, use, Ein])
    s1 = round((Ein - use) * r.choice([0.6, 0.7, 0.8]))
    s2 = Ein - use - s1
    return Q(f'{cap(dev[0])} is supplied with {Ein} J. It transfers {g(use)} J usefully and {s1} J to the internal store of its surroundings by heating; the rest is transferred as sound. Calculate the energy transferred as sound and state the principle you used.',
             f'{g(s2)} J; conservation of energy (total output = input).', f'principle of conservation [1]; {Ein} − {g(use)} − {s1} [1] = {g(s2)} J [1] [3]')


def _e_c4(r, D):
    s, a, b, how = r.choice(SCN)
    Ein = r.choice([100, 400, 500, 1000, 1500])
    w = r.choice([0.1, 0.2, 0.3, 0.4])
    parts = [
        lambda r: ('Name the store that energy is transferred from.', cap(a) + '.', '[1]'),
        lambda r: ('Name the useful store that energy is transferred to.', cap(b) + '.', '[1]'),
        lambda r: ('Describe how the energy is transferred.', cap(how) + '.', '[2]'),
        lambda r: (f'{Ein} J leaves the first store and {g(Ein * w)} J is wasted. Calculate the useful energy transferred.', f'{g(Ein * (1 - w))} J', 'conservation of energy [2]'),
        lambda r: ('Explain what happens to the wasted energy in the end.', 'It is dissipated: spread out into the internal store of the surroundings, warming them slightly.', '[2]'),
        lambda r: ('Explain why the wasted energy is hard to use again.', 'It is spread thinly over a large amount of matter at low temperature.', '[1]'),
    ]
    return compose(r, f'Consider the moment when {s}.', parts, k=(2, 3, 4), type_='multi_step')


t61.add('C4', (2, 3, 4, 5), 'multi_step')(_e_c4)

N62 = 'Kinetic energy ½mv² and gravitational potential energy mgΔh'
t62 = topic(N62, N62.lower(), 'kinetic energy', 'gravitational potential energy')
FX(t62, 'C1', (1, 2), [
    ('Which equation gives kinetic energy?', 'Eₖ = ½mv²', 'Kinetic energy = ½ × mass × speed².', ['Eₖ = mv', 'Eₖ = mgh', 'Eₖ = ½mv']),
    ('Which equation gives the change in gravitational potential energy?', 'ΔEₚ = mgΔh', 'ΔGPE = mass × g × change in height.', ['ΔEₚ = ½mv²', 'ΔEₚ = mg/Δh', 'ΔEₚ = m/(gΔh)']),
    ('If the speed of a car doubles, its kinetic energy', 'becomes four times larger', 'Eₖ ∝ v², so 2² = 4.', ['doubles', 'halves', 'stays the same']),
    ('A 2 kg book is lifted 1.5 m. What is its gain in GPE? (g = 9.8 N/kg)', '29.4 J', 'mgΔh = 2 × 9.8 × 1.5 = 29.4 J.', ['3.0 J', '14.7 J', '19.6 J']),
    ('A 4 kg object moves at 3 m/s. What is its kinetic energy?', '18 J', '½ × 4 × 3² = 18 J.', ['6 J', '12 J', '36 J']),
])
FX(t62, 'C2', (1, 2, 3, 4), [
    ('Explain why a car travelling at 60 km/h needs much more than twice the braking distance of one at 30 km/h.', 'Kinetic energy is proportional to speed squared, so at double the speed it has four times the kinetic energy; with the same braking force, about four times the distance is needed.', 'KE ∝ v² [1]; four times energy, distance ∝ energy [1] [2]'),
    ('A ball is thrown upwards. Describe the energy changes as it rises and falls, ignoring air resistance.', 'Rising: kinetic store decreases and gravitational potential store increases; at the top KE is minimum; falling: GPE transferred back to KE; total constant.', 'rising KE → GPE [1]; falling GPE → KE [1]; total constant [1] [3]'),
    ('Explain why the speed of an object falling from a height h (without air resistance) does not depend on its mass.', 'mgh = ½mv², so m cancels and v = √(2gh).', 'equates GPE and KE [1]; mass cancels [1] [2]'),
    ('Explain why the actual speed of a falling object is less than that calculated from mgh = ½mv².', 'Air resistance does work on the object, transferring some energy to the internal store of the air and object, so less is transferred to kinetic energy.', 'air resistance [1]; energy dissipated not to KE [1] [2]'),
])
KOBJ = [('A sprinter', (55, 85), (7, 10)), ('A car', (900, 1500), (10, 30)), ('A cricket ball', (0.16, 0.16), (15, 40)), ('A cyclist with bicycle', (70, 95), (4, 12)),
        ('A lorry', (8000, 15000), (10, 25)), ('A football', (0.43, 0.43), (8, 25)), ('A dog', (10, 35), (3, 9)), ('A train carriage', (25000, 40000), (10, 30))]


@t62.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t62_ke(r, D):
    o, (m1, m2), (v1, v2) = r.choice(KOBJ)
    m = round(r.uniform(m1, m2), 2 if m2 < 1 else 0)
    v = round(r.uniform(v1, v2), 1 if v2 < 12 else 0)
    E = 0.5 * m * v * v
    if D <= 2:
        return numq(r, D, f'{o} of mass {g(m)} kg moves at {g(v)} m/s.', 'kinetic energy', E, ' J', f'Eₖ = ½mv² = ½ × {g(m)} × {g(v)}²', [m * v, 0.5 * m * v, m * v * v])
    if D == 3:
        return Q(f'{o} of mass {g(m)} kg has {g(E, 3)} J of kinetic energy. Calculate its speed.', f'{g(v, 3)} m/s', f'v² = 2Eₖ/m [1] = {g(2 * E / m, 3)} [1]; v = {g(v, 3)} m/s [1] [3]')
    v2_ = round(v * r.choice([0.5, 1.5, 2]), 1)
    E2 = 0.5 * m * v2_ ** 2
    return Q(f'{o} of mass {g(m)} kg changes speed from {g(v)} m/s to {g(v2_)} m/s. (a) Calculate the kinetic energy at each speed. (b) Calculate the change in kinetic energy. (c) State how many times larger or smaller the kinetic energy has become and explain why this is not the same as the speed ratio.',
             f'(a) {g(E, 3)} J and {g(E2, 3)} J (b) {g(abs(E2 - E), 3)} J {"gained" if E2 > E else "lost"} (c) × {g(E2 / E, 3)}: KE ∝ v², so the ratio is the square of the speed ratio ({g(v2_ / v, 3)}).',
             f'(a) both KEs [2] (b) difference [1] (c) ratio with v² reasoning [1]' + (' [4]' if D == 4 else '; correct ratio value [1] [5]'), 'multi_step')


GOBJ = [('a box lifted onto a shelf', (2, 15), (1, 2.5)), ('a climber ascending a cliff', (55, 80), (10, 60)), ('a lift carrying passengers', (500, 1000), (10, 40)), ('water raised by a pump', (100, 2000), (5, 30)),
        ('a crane lifting a steel beam', (300, 1500), (8, 40)), ('a rucksack carried up a mountain', (8, 20), (200, 900)), ('a skier on a chairlift', (60, 90), (100, 400))]


@t62.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t62_gpe(r, D):
    o, (m1, m2), (h1, h2) = r.choice(GOBJ)
    m = round(r.uniform(m1, m2))
    h = round(r.uniform(h1, h2), 1 if h2 < 5 else 0)
    E = m * G * h
    if D <= 2:
        return numq(r, D, f'Consider {o}: mass {m} kg, raised through {g(h)} m (g = 9.8 N/kg).', 'gain in gravitational potential energy', E, ' J', f'ΔEₚ = mgΔh = {m} × 9.8 × {g(h)}', [m * h, E / 9.8 / 9.8, 0.5 * m * h * h])
    if D == 3:
        return Q(f'Consider {o}: the gain in gravitational potential energy is {g(E, 3)} J and the mass is {m} kg (g = 9.8 N/kg). Calculate the height gained.', f'{g(h, 3)} m', f'Δh = ΔEₚ/(mg) [1] = {g(E, 3)}/({m} × 9.8) [1] = {g(h, 3)} m [1] [3]')
    hh = r.choice([1.25, 2.0, 3.2, 5.0, 7.2, 11.25, 20.0])
    v = math.sqrt(2 * G * hh)
    mm = r.choice([0.2, 0.5, 1.5, 2.0, 60])
    obj = r.choice(['A stone', 'A diver', 'A mango', 'A steel ball', 'A water droplet from a fountain'])
    return Q(f'{obj} of mass {g(mm)} kg falls from rest through a height of {g(hh)} m (g = 9.8 N/kg). Ignore air resistance. (a) Calculate the GPE lost. (b) State the KE gained. (c) Calculate the speed just before impact. (d) State one reason why the real speed is lower.',
             f'(a) {g(mm * G * hh, 3)} J (b) {g(mm * G * hh, 3)} J (c) {g(v, 3)} m/s (d) air resistance transfers energy to thermal stores.',
             f'(a) mgh [1] (b) equal, by conservation [1] (c) ½mv² = mgh, v = √(2gh) = {g(v, 3)} m/s [1]' + (' [3]' if False else '') + (' (d) air resistance [1] [4]' if D == 4 else '; mass cancels shown [1] (d) air resistance [1] [5]'), 'multi_step')


relation(t62, 'C2', (2, 3), 'Eₖ = ½mv²', 'kinetic energy', {'speed': 2, 'mass': 1}, ['A road-safety campaign compares cars travelling at different speeds.', 'A cyclist and bicycle move along a flat road.', 'Engineers study the energy of trains.'])


def _ke_c4(r, D):
    m = r.choice([0.5, 1.0, 2.0, 50, 60, 400, 500])
    h = r.choice([5, 10, 20, 45])
    v = math.sqrt(2 * G * h)
    sc = r.choice([('A roller-coaster car', 400, 'a track'), ('A child', 30, 'a long slide'), ('A skateboarder', 55, 'a ramp'), ('A ball', 0.5, 'a long slope')])
    m = sc[1]
    lost = r.choice([0.1, 0.2, 0.3])
    intro = f'{sc[0]} of mass {g(m)} kg starts from rest at the top of {sc[2]} {h} m high (g = 9.8 N/kg).'
    parts = [
        lambda r: ('Calculate the GPE lost in reaching the bottom.', f'{g(m * G * h, 3)} J', 'mgΔh [2]'),
        lambda r: ('Calculate the speed at the bottom if no energy is wasted.', f'{g(v, 3)} m/s', 'mgh = ½mv² [1]; v = √(2gh) [1] [2]'),
        lambda r: (f'In fact {int(lost * 100)}% of the energy is transferred to thermal stores. Calculate the actual speed at the bottom.', f'{g(math.sqrt(2 * G * h * (1 - lost)), 3)} m/s', f'KE = {g(m * G * h * (1 - lost), 3)} J [1]; v [2] [3]'),
        lambda r: ('Explain why the actual speed does not depend on the mass if the same percentage is wasted.', 'Both GPE and KE are proportional to m, so m cancels.', '[2]'),
        lambda r: ('Name two forces that cause energy to be wasted.', 'Friction (between wheels/body and track) and air resistance.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t62.add('C4', (2, 3, 4, 5), 'multi_step')(_ke_c4)
t62.add('C3', (4, 5), 'multi_step')(_ke_c4)

DEV = [('filament lamp', 'light', [('thermal (heating surroundings)', 0.9)]), ('LED lamp', 'light', [('thermal (heating surroundings)', 0.2)]), ('electric motor', 'kinetic', [('thermal', 0.25), ('sound', 0.05)]),
       ('petrol car engine', 'kinetic', [('thermal (exhaust and engine)', 0.7), ('sound', 0.05)]), ('television', 'light and sound', [('thermal', 0.6)]), ('kettle', 'thermal (of the water)', [('thermal (of the kettle and air)', 0.1), ('sound', 0.02)]),
       ('coal-fired power station', 'electrical', [('thermal (cooling towers and flue gases)', 0.62)]), ('loudspeaker', 'sound', [('thermal', 0.9)]), ('solar panel', 'electrical', [('thermal and reflected light', 0.8)])]
N63 = 'Energy transfer diagrams and Sankey diagrams'
t63 = topic(N63, N63.lower(), 'sankey diagrams', 'energy transfer diagrams')
FX(t63, 'C1', (1, 2), [
    ('In a Sankey diagram, what does the width of each arrow represent?', 'The amount of energy transferred', 'Widths are drawn to scale with energy.', ['The speed of the energy transfer', 'The time taken', 'The temperature of the device']),
    ('In a Sankey diagram, wasted energy is usually shown', 'by arrows bending downwards (or away) from the main arrow', 'Useful output continues straight on; wasted outputs bend away.', ['by the widest arrow pointing straight on', 'as a separate diagram', 'by a circle']),
    ('Why must the total width of the output arrows equal the width of the input arrow?', 'Energy is conserved', 'Input = useful + wasted.', ['Energy is created in the device', 'The device stores all the energy', 'Sankey diagrams are drawn this way only for neatness']),
    ('A Sankey diagram for a lamp has an input of 100 J and a useful light output of 10 J. How much energy is wasted?', '90 J', '100 − 10 = 90 J.', ['110 J', '10 J', '1000 J']),
    ('State what an energy transfer diagram (flow diagram) shows.', 'The stores that energy is transferred from and to, and how it is transferred, for a process.', 'stores and transfers [1]'),
])
FX(t63, 'C2', (1, 2, 3, 4), [
    ('Explain why the Sankey diagram for an LED lamp would look different from that for a filament lamp of the same light output.', 'The LED wastes much less energy as heat, so its wasted arrow would be much narrower and the input arrow narrower for the same useful light.', 'LED wastes less [1]; narrower wasted arrow / input [1] [2]'),
    ('Describe how to draw a Sankey diagram to scale for a device.', 'Choose a scale (e.g. 1 mm = 10 J); draw the input arrow with width for the total input; split into the useful arrow straight on and wasted arrows bending away, each with width proportional to its energy, so the widths add to the input.', 'scale [1]; useful straight, wasted bent [1]; widths add to input [1] [3]'),
    ('Explain how a Sankey diagram shows the efficiency of a device.', 'Efficiency = width of useful output arrow ÷ width of input arrow; the wider the useful arrow relative to the input, the more efficient.', 'ratio useful/input widths [1]; wider useful = more efficient [1] [2]'),
])


@t63.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t63_sankey(r, D):
    name, useful, wastes = r.choice(DEV)
    Ein = r.choice([100, 200, 500, 1000, 1200, 2000, 2500])
    W = [(w, round(Ein * f)) for w, f in wastes]
    U = Ein - sum(x for _, x in W)
    s = f'A Sankey diagram for a {name} shows an input of {Ein} J of electrical energy' if 'engine' not in name and 'station' not in name else f'A Sankey diagram for a {name} shows an input of {Ein} J of chemical energy'
    if D <= 2:
        return numq(r, D, s + ', ' + ', '.join(f'{x} J wasted as {w}' for w, x in W) + f' and a useful output as {useful}.', 'useful energy output', U, ' J', f'useful = {Ein} − ' + ' − '.join(str(x) for _, x in W), [Ein + sum(x for _, x in W), sum(x for _, x in W), Ein])
    eff = U / Ein * 100
    if D == 3:
        sc_ = r.choice([1, 2, 5, 10, 20])
        return Q(s + ', ' + ', '.join(f'{x} J wasted as {w}' for w, x in W) + f' and a useful {useful} output. The diagram is drawn with 1 mm representing {sc_ * Ein // 100} J. Calculate the useful output and the width of its arrow.',
                 f'{U} J; {g(U / (sc_ * Ein / 100), 3)} mm', f'useful = {U} J [1]; width = {U}/{sc_ * Ein // 100} [1] = {g(U / (sc_ * Ein / 100), 3)} mm [1] [3]')
    return Q(s + ', ' + ', '.join(f'{x} J wasted as {w}' for w, x in W) + f' and a useful {useful} output. (a) Calculate the useful output. (b) Calculate the efficiency. (c) Describe how the arrows in the diagram show which output is largest.',
             f'(a) {U} J (b) {g(eff, 3)}% (c) the widest output arrow shows the largest energy transfer.',
             f'(a) {U} J [1] (b) {U}/{Ein} × 100 [1] = {g(eff, 3)}% [1] (c) width proportional to energy [1]' + (' [4]' if D == 4 else '; plus statement that widths sum to input [1] [5]'), 'multi_step')


@t63.add('C2', (1, 2, 3, 4), 'explain')
def t63_flow(r, D):
    s, a, b, how = r.choice(SCN)
    return Q(f'Draw (describe) an energy transfer diagram for the following: {s}. Label the stores and the transfer pathway.', f'{cap(a)} store → ({how}) → {b} store, with a branch to the thermal store of the surroundings (wasted).',
             'correct starting store [1]; correct useful final store [1]; pathway/wasted branch [1] [3]' if D >= 3 else 'starting store [1]; final store [1] [2]')


def _sk_c4(r, D):
    name, useful, wastes = r.choice(DEV)
    Ein = r.choice([500, 1000, 2000])
    W = [(w, round(Ein * f)) for w, f in wastes]
    U = Ein - sum(x for _, x in W)
    intro = f'A {name} is supplied with {Ein} J. It wastes ' + ' and '.join(f'{x} J as {w}' for w, x in W) + '.'
    parts = [
        lambda r: (f'Calculate the useful {useful} output.', f'{U} J', '[1]'),
        lambda r: ('Calculate the efficiency.', f'{g(U / Ein * 100, 3)}%', '[2]'),
        lambda r: ('Describe the Sankey diagram for this device, using a scale of 1 mm to 20 J.', f'Input {g(Ein / 20)} mm wide; useful {g(U / 20, 3)} mm straight on; wasted arrows ' + ', '.join(f'{g(x / 20, 3)} mm' for _, x in W) + ' bending away.', 'widths correct [2]; layout [1] [3]'),
        lambda r: ('Explain what eventually happens to all of the energy output.', 'It is dissipated to the internal store of the surroundings.', '[1]'),
        lambda r: ('Suggest how the device could be made more efficient.', 'Reduce the wasted transfers, e.g. lubricate/insulate/use a more efficient technology.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t63.add('C4', (2, 3, 4, 5), 'multi_step')(_sk_c4)

N64 = 'Efficiency of energy transfers'
t64 = topic(N64, N64.lower(), 'efficiency of energy')
FX(t64, 'C1', (1, 2), [
    ('Which equation gives efficiency?', 'efficiency = useful energy output ÷ total energy input (× 100%)', 'Efficiency compares useful output with total input.', ['efficiency = total input ÷ useful output', 'efficiency = wasted energy ÷ useful output', 'efficiency = useful output × total input']),
    ('A device has an efficiency of 0.25. What does this mean?', '25% of the input energy is transferred usefully', '0.25 = 25% useful; 75% wasted.', ['25 J is wasted', 'The device wastes 25% of the input', 'It produces 25 J of output']),
    ('Why can no device have an efficiency greater than 100%?', 'It would need to output more energy than it receives, which breaks conservation of energy', 'Useful output can never exceed input.', ['Because devices always break', 'Because energy is weightless', 'Because efficiency has no units']),
    ('A motor is supplied with 500 J and does 400 J of useful work. What is its efficiency?', '80%', '400/500 × 100 = 80%.', ['125%', '20%', '90%']),
    ('State one way of reducing wasted energy in a machine with moving parts.', 'Lubricate the moving parts to reduce friction.', '[1]'),
])
FX(t64, 'C2', (1, 2, 3, 4), [
    ('Explain why LED lamps are replacing filament lamps.', 'LEDs transfer a much higher proportion of electrical energy to light and less to thermal energy, so they are more efficient, cheaper to run and last longer.', 'higher efficiency/less heating [1]; cheaper to run [1] [2]'),
    ('Explain why efficiency has no unit.', 'It is a ratio of two energies (J/J), so the units cancel.', 'ratio of same quantity [1]'),
    ('A student says a 95% efficient heater is better than a 30% efficient lamp. Explain why comparing these efficiencies is not useful.', 'They have different useful outputs (thermal vs light); for a heater nearly all energy becomes thermal energy, which is its useful output, so efficiency only compares devices with the same purpose.', 'different useful outputs [1]; compare like with like [1] [2]'),
])


@t64.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t64_eff(r, D):
    name, useful, wastes = r.choice(DEV)
    Ein = r.choice([400, 500, 800, 1000, 1500, 2000, 2500, 4000])
    e = round(1 - sum(f for _, f in wastes), 2)
    U = Ein * e
    if D <= 2:
        return numq(r, D, f'A {name} is supplied with {Ein} J and transfers {g(U)} J usefully as {useful}.', 'efficiency', e * 100, '%', f'efficiency = {g(U)}/{Ein} × 100', [Ein / U * 100, (1 - e) * 100, e * 1000])
    if D == 3:
        U2 = r.choice([60, 120, 240, 300, 450, 600])
        u = ' MJ' if 'station' in name else ' J'
        return Q(f'A {name} has an efficiency of {g(e * 100)}%. Calculate the energy input needed for a useful {useful} output of {U2}{u}, and the energy wasted.', f'{g(U2 / e, 3)}{u}; {g(U2 / e - U2, 3)}{u} wasted',
                 f'input = useful/efficiency [1] = {U2}/{g(e)} = {g(U2 / e, 3)}{u} [1]; wasted = {g(U2 / e - U2, 3)}{u} [1] [3]')
    n2, u2, w2 = r.choice([d for d in DEV if d[1] == useful and d[0] != name] or [r.choice(DEV)])
    e2 = round(1 - sum(f for _, f in w2), 2)
    return Q(f'Device A ({name}) has an efficiency of {g(e * 100)}%; device B ({n2}) has an efficiency of {g(e2 * 100)}%. Each is supplied with {Ein} J. (a) Calculate the useful output of each. (b) Calculate the energy wasted by each. (c) Explain which device is better at its job, if they have the same purpose.' if n2 != name else
             f'A {name} has an efficiency of {g(e * 100)}% and is supplied with {Ein} J. (a) Calculate the useful output. (b) Calculate the energy wasted. (c) Explain what happens to the wasted energy.',
             (f'(a) A {g(Ein * e)} J, B {g(Ein * e2)} J (b) A {g(Ein * (1 - e))} J, B {g(Ein * (1 - e2))} J (c) the one with higher efficiency wastes less of the same input.' if n2 != name else f'(a) {g(Ein * e)} J (b) {g(Ein * (1 - e))} J (c) it is dissipated to the surroundings as thermal energy.'),
             '(a) useful = efficiency × input [2] (b) wasted = input − useful [1] (c) reasoned comparison/explanation [1]' + (' [4]' if D == 4 else '; mentions conservation of energy [1] [5]'), 'multi_step')


@t64.add('C2', (2, 3, 4), 'explain')
def t64_err(r, D):
    Ein, U = r.choice([(200, 50), (400, 100), (500, 400), (800, 200), (1000, 350)])
    who = person(r)
    return Q(f'{who} says a machine that takes in {Ein} J and gives out {U} J of useful energy has an efficiency of {g(Ein / U * 100)}%. Identify the error and give the correct value.', f'{who} divided input by output; efficiency = {U}/{Ein} × 100 = {g(U / Ein * 100)}%. A value over 100% is impossible.',
             f'inverted ratio [1]; {g(U / Ein * 100)}% [1]; >100% impossible [1] [3]')


t64.add('C4', (2, 3, 4, 5), 'multi_step')(_sk_c4)

CHAPTERS[6] = [t61, t62, t63, t64]

# =========================================================== 7 Energy resources
RES = {  # name: (renewable, from Sun?, how electricity is produced, advantages, disadvantages)
    'coal': (False, True, 'burned to boil water; steam drives turbines connected to generators', 'reliable; large output; flexible', 'releases CO₂ (global warming) and SO₂ (acid rain); finite'),
    'oil': (False, True, 'burned to boil water or in engines driving generators', 'reliable; energy-dense; easy to transport', 'CO₂ emissions; finite; spills'),
    'natural gas': (False, True, 'burned in gas turbines (or to make steam)', 'quick start-up; less CO₂ than coal', 'CO₂ emissions; finite'),
    'nuclear fission': (False, False, 'fission of uranium releases thermal energy to make steam for turbines', 'no CO₂ when running; reliable; huge energy from small fuel mass', 'radioactive waste; risk of accidents; expensive to build and decommission'),
    'solar cells': (True, True, 'light is transferred directly to electrical energy in photovoltaic cells', 'no fuel cost; no emissions when running; good for remote places', 'no output at night, low in cloud; large area needed'),
    'wind': (True, True, 'wind turns turbine blades connected to a generator', 'no fuel cost or emissions when running', 'unreliable (depends on wind); noise; visual impact'),
    'hydroelectric': (True, True, 'water stored behind a dam falls through turbines', 'reliable; quick to respond to demand', 'flooding of valleys; habitat loss; few suitable sites'),
    'tidal': (True, False, 'tidal water flows through turbines in a barrage', 'predictable; no emissions when running', 'only twice-daily peaks; affects estuary habitats; few sites'),
    'waves': (True, True, 'up-and-down motion of waves drives a generator', 'no fuel cost', 'unreliable; small output; difficult to build at sea'),
    'geothermal': (True, False, 'hot rocks heat water to steam to drive turbines', 'reliable; low emissions', 'only in volcanic regions; drilling cost'),
    'biofuels': (True, True, 'plant material or alcohol is burned to make steam for turbines', 'carbon-neutral overall if replanted; reliable', 'uses farmland; CO₂ released when burned'),
}
N71 = 'Non-renewable energy resources: fossil fuels and nuclear fission'
t71 = topic(N71, N71.lower(), 'non-renewable', 'fossil fuels')
FX(t71, 'C1', (1, 2), [
    ('Which is a non-renewable energy resource?', 'Natural gas', 'Fossil fuels and nuclear fuels are non-renewable: they will run out.', ['Wind', 'Solar', 'Tidal']),
    ('In a fossil-fuel power station, what turns the generator?', 'A turbine driven by steam (or hot gas)', 'Burning fuel boils water; steam drives a turbine connected to a generator.', ['The fuel itself', 'An electric motor', 'Sunlight']),
    ('Which energy store does a nuclear fuel hold?', 'Nuclear', 'Fission releases energy from the nucleus.', ['Chemical', 'Elastic', 'Kinetic']),
    ('Burning fossil fuels releases carbon dioxide, which', 'contributes to global warming (greenhouse effect)', 'CO₂ traps infrared radiation in the atmosphere.', ['causes acid rain only', 'destroys radioactive waste', 'reduces global temperatures']),
    ('What is meant by "non-renewable"?', 'It cannot be replaced as fast as it is used, so it will eventually run out.', '[1]'),
    ('In nuclear fission,', 'a large nucleus splits into smaller nuclei, releasing energy', 'Uranium-235 nuclei split when they absorb a neutron.', ['small nuclei join together', 'electrons are removed from atoms', 'fuel is burned in oxygen']),
])
FX(t71, 'C2', (1, 2, 3, 4), [
    ('Describe how electricity is generated in a coal-fired power station, naming the energy stores involved.', 'Coal is burned (chemical store) to heat water into high-pressure steam (thermal store), which turns a turbine (kinetic) connected to a generator producing electricity.', 'burn coal → steam [1]; turbine [1]; generator / stores named [1] [3]'),
    ('Give one advantage and one disadvantage of nuclear power compared with coal.', 'Advantage: no CO₂ produced when operating / much more energy per kg of fuel. Disadvantage: radioactive waste that stays dangerous for thousands of years / risk of accidents.', 'advantage [1]; disadvantage [1] [2]'),
    ('Explain why fossil fuels are described as having energy that came originally from the Sun.', 'They formed from plants (and animals that ate plants) that stored energy from sunlight by photosynthesis millions of years ago.', 'plants photosynthesised [1]; buried over millions of years [1] [2]'),
    ('Explain why a gas-fired power station is useful for meeting sudden increases in demand.', 'Gas turbines can be started up and increased in output quickly, unlike coal or nuclear stations.', 'fast start-up [1]; meets peaks [1] [2]'),
])


@t71.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t71_fuel(r, D):
    fuel, ed = r.choice([('coal', 30), ('natural gas', 55), ('oil', 45), ('wood pellets', 18)])
    P = r.choice([500, 600, 800, 1000, 1200, 2000])  # MW electrical
    eff = r.choice([0.33, 0.35, 0.38, 0.4, 0.45, 0.5])
    Pin = P / eff
    rate = Pin / ed  # kg/s (MJ/s / MJ/kg)
    if D <= 2:
        return numq(r, D, f'A {fuel}-fired power station has an output of {P} MW and an efficiency of {g(eff * 100)}%.', 'power input from the fuel in MW', Pin, ' MW', f'input = {P}/{g(eff)}', [P * eff, P - P * eff, Pin * 2])
    if D == 3:
        return Q(f'A {fuel}-fired power station has an output of {P} MW and an efficiency of {g(eff * 100)}%. Each kilogram of {fuel} releases {ed} MJ. Calculate the input power and the mass of {fuel} burned each second.', f'{g(Pin, 3)} MW; {g(rate, 3)} kg/s',
                 f'input = {P}/{g(eff)} = {g(Pin, 3)} MW [1]; {g(Pin, 3)} MJ/s ÷ {ed} MJ/kg [1] = {g(rate, 3)} kg/s [1] [3]')
    day = rate * 86400 / 1000
    return Q(f'A {fuel}-fired power station has an output of {P} MW and an efficiency of {g(eff * 100)}%. Each kilogram of {fuel} releases {ed} MJ. (a) Calculate the power wasted. (b) Calculate the mass of {fuel} burned per second. (c) Calculate the mass burned per day in tonnes. (d) State where most of the wasted energy goes.',
             f'(a) {g(Pin - P, 3)} MW (b) {g(rate, 3)} kg/s (c) {g(day, 3)} tonnes (d) to the surroundings as thermal energy, mainly via cooling water/towers and flue gases.',
             f'(a) {g(Pin, 3)} − {P} [1] (b) {g(Pin, 3)}/{ed} = {g(rate, 3)} kg/s [1] (c) × 86 400 ÷ 1000 [1] (d) thermal energy to surroundings [1]' + (' [4]' if D == 4 else '; CO₂ consequence mentioned [1] [5]'), 'multi_step')


@t71.add('C2', (2, 3, 4), 'explain')
def t71_cmp(r, D):
    a, b = r.sample(['coal', 'oil', 'natural gas', 'nuclear fission'], 2)
    return Q(f'Compare {a} and {b} as energy resources for generating electricity. Give one similarity and one difference.', f'Similarity: both are non-renewable and used to produce steam that drives turbines (reliable output). Difference: {a}: {RES[a][4]}; {b}: {RES[b][4]}.',
             'similarity [1]; difference with specific detail for each [2] [3]')


def _nr_c4(r, D):
    fuel = r.choice(['coal', 'natural gas', 'nuclear fission'])
    P = r.choice([600, 1000, 1200])
    eff = r.choice([0.35, 0.4, 0.45])
    parts = [
        lambda r: ('Describe how the station produces electricity.', cap(RES[fuel][2]) + '.', 'heat → steam [1]; turbine → generator [1] [2]'),
        lambda r: (f'The station outputs {P} MW at an efficiency of {g(eff * 100)}%. Calculate the input power.', f'{g(P / eff, 3)} MW', '[2]'),
        lambda r: ('Calculate the power wasted.', f'{g(P / eff - P, 3)} MW', '[1]'),
        lambda r: ('Give one environmental disadvantage.', cap(RES[fuel][4].split(';')[0]) + '.', '[1]'),
        lambda r: ('Explain why this resource is called non-renewable.', 'The fuel cannot be replaced as quickly as it is used; supplies are finite.', '[1]'),
        lambda r: ('Suggest one reason the government may still choose this resource.', cap(RES[fuel][3].split(';')[0]) + '.', '[1]'),
    ]
    return compose(r, f'A country plans a new {fuel} power station.', parts, k=(2, 3, 4), type_='multi_step')


t71.add('C4', (2, 3, 4, 5), 'multi_step')(_nr_c4)

N72 = 'Renewable energy resources: solar, wind, hydroelectric, tidal, waves, geothermal and biofuels'
t72 = topic(N72, N72.lower(), 'renewable energy')
REN = [k for k, v in RES.items() if v[0]]


@t72.add('C1', (1, 2, 3))
def t72_how(r, D):
    k = r.choice(REN)
    opts, a = mcq(r, k, [x for x in REN if x != k])
    return Q(f'In which energy resource is electricity produced like this: {RES[k][2]}?', a, f'{cap(k)}: {RES[k][2]}.', opts=opts)


@t72.add('C1', (1, 2, 3))
def t72_sun(r, D):
    notsun = [k for k in REN if not RES[k][1]]
    sun = [k for k in REN if RES[k][1]]
    a = r.choice(notsun)
    opts, ans = mcq(r, a, r.sample(sun, 4))
    return Q('Which renewable energy resource does NOT get its energy from the Sun?', ans, 'Tidal (Moon’s gravity) and geothermal (hot rocks/radioactive decay inside the Earth) do not come from the Sun.', opts=opts)


FX(t72, 'C1', (1, 2), [
    ('What is meant by a renewable energy resource?', 'One that is replaced naturally as fast as it is used, so it will not run out.', '[1]'),
    ('Which renewable resource gives the most predictable output?', 'Tidal', 'Tides are caused by the Moon and are predictable years in advance.', ['Wind', 'Waves', 'Solar']),
])
FX(t72, 'C2', (1, 2, 3, 4), [
    ('Explain why biofuels are described as "carbon neutral".', 'The plants absorb CO₂ from the atmosphere as they grow, roughly equal to the CO₂ released when the fuel is burned.', 'CO₂ absorbed in growth [1]; balances CO₂ released [1] [2]'),
    ('Explain why a hydroelectric station can respond quickly to a sudden rise in demand.', 'Water stored behind the dam can be released through the turbines almost immediately by opening the gates.', 'stored water [1]; released quickly [1] [2]'),
    ('Describe the energy transfers in a wind turbine.', 'Kinetic energy of the moving air is transferred to kinetic energy of the blades and generator, then transferred electrically.', 'kinetic of air → blades [1]; generator, electrical [1] [2]'),
    ('Explain why geothermal power is only used in a few countries.', 'It needs hot rocks close to the surface, which occur mainly in volcanic regions such as Iceland or Kenya.', 'needs hot rocks near surface [1]; volcanic regions [1] [2]'),
])


@t72.add('C2', (2, 3, 4), 'explain')
def t72_adv(r, D):
    k = r.choice(REN)
    return Q(f'Give one advantage and one disadvantage of using {k} to generate electricity.', f'Advantage: {RES[k][3].split(";")[0]}. Disadvantage: {RES[k][4].split(";")[0]}.', 'advantage [1]; disadvantage [1] [2]')


@t72.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t72_calc(r, D):
    kind = r.choice(['hydro', 'solar', 'wind'])
    if kind == 'hydro':
        h = r.choice([50, 80, 100, 120, 150, 200])
        q = r.choice([10, 20, 50, 100, 200])  # m³/s -> kg/s ×1000
        eff = r.choice([0.8, 0.85, 0.9])
        Pin = q * 1000 * G * h
        if D <= 2:
            return numq(r, D, f'At a hydroelectric dam, {q * 1000} kg of water falls through a height of {h} m every second (g = 9.8 N/kg).', 'gravitational potential energy lost by the water each second', Pin, ' J', f'mgΔh = {q * 1000} × 9.8 × {h}', [q * 1000 * h, Pin / 9.8 / 9.8, Pin / 1000])
        return Q(f'At a hydroelectric dam, {q} m³ of water (density 1000 kg/m³) falls {h} m through the turbines every second (g = 9.8 N/kg). The efficiency is {g(eff * 100)}%. Calculate the electrical power output in MW.', f'{g(Pin * eff / 1e6, 3)} MW',
                 f'mass per second = {q * 1000} kg [1]; GPE per second = {g(Pin, 3)} J [1]; × {g(eff)} = {g(Pin * eff / 1e6, 3)} MW [1]' + (' [3]' if D == 3 else '; correct unit conversion [1] [4]'))
    if kind == 'solar':
        I = r.choice([600, 800, 1000])
        A = r.choice([1.5, 2, 4, 10, 20])
        eff = r.choice([0.15, 0.18, 0.2, 0.22])
        P = I * A * eff
        if D <= 2:
            return numq(r, D, f'Sunlight delivers {I} W to each square metre of a solar panel of area {g(A)} m².', 'total power of sunlight on the panel', I * A, ' W', f'{I} × {g(A)}', [I / A, I * A * eff, I])
        hrs = r.choice([4, 5, 6])
        return Q(f'Sunlight delivers {I} W per square metre to solar panels of total area {g(A)} m² with efficiency {g(eff * 100)}%. (a) Calculate the electrical power output. (b) Calculate the electrical energy produced in {hrs} hours of such sunshine in MJ.', f'(a) {g(P, 3)} W (b) {g(P * hrs * 3600 / 1e6, 3)} MJ',
                 f'(a) {I} × {g(A)} × {g(eff)} [1] = {g(P, 3)} W [1] (b) E = Pt = {g(P, 3)} × {hrs * 3600} [1] = {g(P * hrs * 3600 / 1e6, 3)} MJ [1]' + (' [4]' if D <= 4 else '; one reason the real output is lower (cloud, angle) [1] [5]'), 'multi_step')
    Pt = r.choice([2, 2.5, 3, 4, 5])  # MW
    cf = r.choice([0.25, 0.3, 0.35, 0.4])
    Pst = r.choice([500, 1000, 1200])
    n = Pst / (Pt * cf)
    if D <= 2:
        return numq(r, D, f'A wind turbine has a maximum output of {g(Pt)} MW. A power station has an output of {Pst} MW.', 'number of turbines, at maximum output, needed to match the power station', Pst / Pt, '', f'{Pst}/{g(Pt)}', [Pst * Pt, Pst / Pt / 2, Pst / Pt * 1.5], fm=lambda x: g(x, 4))
    return Q(f'A wind turbine has a maximum output of {g(Pt)} MW, but on average it produces only {g(cf * 100)}% of this. Calculate how many turbines are needed to produce the same average power as a {Pst} MW gas power station, and give one reason why the gas station may still be needed.', f'{math.ceil(n)} turbines; wind is unreliable, so backup is needed on calm days.',
             f'average output = {g(Pt * cf, 3)} MW [1]; {Pst}/{g(Pt * cf, 3)} = {g(n, 4)} → {math.ceil(n)} [1]; reliability point [1]' + (' [3]' if D == 3 else '; space/land use or cost point [1] [4]'))


def _ren_c4(r, D):
    k = r.choice(REN)
    place = city(r)
    parts = [
        lambda r: (f'Describe how electricity is generated using {k}.', cap(RES[k][2]) + '.', '[2]'),
        lambda r: ('State whether the energy originally came from the Sun.', 'Yes' if RES[k][1] else 'No' + (' (Moon’s gravity).' if k == 'tidal' else ' (thermal energy inside the Earth).'), '[1]'),
        lambda r: ('Give two advantages.', RES[k][3] + '.', '[2]'),
        lambda r: ('Give two disadvantages.', RES[k][4] + '.', '[2]'),
        lambda r: ('Explain whether it can supply electricity at all times.', 'Yes, it is reliable.' if k in ('hydroelectric', 'geothermal', 'biofuels') else 'No: output varies (' + ('tides' if k == 'tidal' else 'weather / daylight') + '), so backup or storage is needed.', '[2]'),
    ]
    lab = {'solar cells': 'solar-cell', 'waves': 'wave', 'biofuels': 'biofuel'}.get(k, k)
    return compose(r, f'A town near {place} is considering {lab} power.', parts, k=(2, 3, 4), type_='multi_step')


t72.add('C4', (2, 3, 4, 5), 'multi_step')(_ren_c4)

N73 = 'Comparing energy resources: availability, reliability, cost and environmental impact'
t73 = topic(N73, N73.lower(), 'comparing energy resources')
FX(t73, 'C1', (1, 2), [
    ('Which energy resource is the least reliable for continuous electricity supply?', 'Wind', 'Wind speed varies; no output on calm days.', ['Nuclear', 'Coal', 'Geothermal']),
    ('Which resource has no fuel cost but a very high initial building cost and floods land?', 'Hydroelectric', 'Dams are expensive to build and flood valleys.', ['Natural gas', 'Coal', 'Biofuel']),
    ('Which resource produces long-lived radioactive waste?', 'Nuclear fission', 'Spent fuel stays radioactive for thousands of years.', ['Solar', 'Tidal', 'Wind']),
    ('Which pair are both renewable and reliable?', 'Geothermal and hydroelectric', 'Both provide steady outputs where available.', ['Wind and waves', 'Coal and oil', 'Solar and wind']),
    ('State two factors to consider when choosing an energy resource for a region.', 'Any two of: availability, reliability, cost (building and running), environmental impact.', '[2]'),
])
FX(t73, 'C2', (1, 2, 3, 4), [
    ('Explain why many countries use a mix of energy resources rather than one.', 'Different resources have different strengths: reliable ones (nuclear, gas, hydro) cover base load and peaks, while renewables cut emissions; a mix protects supply when one is unavailable.', 'reliability/backup [1]; reduce emissions/cost balance [1] [2]'),
    ('Explain why solar power is more suitable for a country near the equator than for one far from it.', 'Near the equator there is more intense sunlight and more consistent day length all year, so panels produce more energy.', 'more intense sunlight [1]; consistent through the year [1] [2]'),
    ('Explain why the cost of electricity from a resource depends on more than just the fuel cost.', 'Building, maintenance, decommissioning and waste disposal costs must be included, as well as how often the station actually runs.', 'capital/maintenance [1]; decommissioning/capacity factor [1] [2]'),
])
COMP = [('A remote island in the Pacific with strong winds and frequent sunshine', 'wind and solar with battery storage', 'no fuel needs shipping; both available; storage covers calm/night'),
        ('A mountainous country with high rainfall and deep valleys', 'hydroelectric', 'large reliable supply from stored water'),
        ('A volcanic island such as Iceland', 'geothermal', 'hot rocks near the surface give reliable low-carbon power'),
        ('A coastal city with a large tidal range in its estuary', 'tidal barrage', 'predictable tides and suitable site'),
        ('A desert region near the equator', 'solar (photovoltaic or solar thermal)', 'intense sunshine nearly every day'),
        ('An industrial country with no suitable rivers that wants low CO₂ but reliable base load', 'nuclear (with renewables)', 'reliable large output with no CO₂ when running'),
        ('A farming region with spare land and crop waste', 'biofuels', 'uses local waste; reliable; nearly carbon neutral')]


@t73.add('C3', (2, 3, 4), 'case')
def t73_choose(r, D):
    p, res, why = r.choice(COMP)
    return Q(f'{p} needs a new source of electricity. Suggest the most suitable energy resource and justify your choice, including one disadvantage.', f'{cap(res)}: {why}. Disadvantage, e.g. ' + (RES.get(res.split(' ')[0].replace('tidal', 'tidal'), RES['wind'])[4].split(';')[0] if res.split(' ')[0] in RES else 'high building cost / environmental impact') + '.',
             'sensible choice [1]; justified by local conditions [1]; disadvantage [1]' + (' [3]' if D < 4 else '; comparison with an alternative [1] [4]'))


TAB = [('coal', 7, 'high', 'high', 900), ('gas', 6, 'high', 'medium', 450), ('nuclear', 11, 'high', 'low', 12), ('wind (onshore)', 5, 'low', 'low', 11), ('solar', 6, 'low', 'low', 45), ('hydroelectric', 8, 'high', 'medium', 24)]


@t73.add('C3', (2, 3, 4, 5), 'case')
def t73_table(r, D):
    rows = r.sample(TAB, 4)
    s = 'Data for four resources (cost of electricity in cents per kWh; reliability; land impact; CO₂ in g per kWh): ' + '; '.join(f'{a}: {b}, {c}, {d}, {e}' for a, b, c, d, e in rows) + '.'
    low = min(rows, key=lambda x: x[4])
    cheap = min(rows, key=lambda x: x[1])
    return Q(s + ' (a) Identify the resource with the lowest CO₂ emissions and the cheapest resource. (b) Evaluate which resource would be best for a country that wants low emissions and a reliable supply.',
             f'(a) Lowest CO₂: {low[0]}; cheapest: {cheap[0]}. (b) A reliable low-CO₂ option such as ' + (', '.join(x[0] for x in rows if x[2] == 'high' and x[4] < 100) or 'a mix of renewables with storage') + ' is best; renewables need backup when unreliable.',
             '(a) both identified [2] (b) uses reliability and CO₂ data [1]; justified conclusion [1]' + (' [4]' if D < 5 else '; considers cost trade-off [1] [5]'))


@t73.add('C4', (3, 4, 5), 'long')
def t73_eval(r, D):
    a, b = r.sample(['coal', 'natural gas', 'nuclear fission', 'wind', 'solar cells', 'hydroelectric', 'tidal', 'geothermal'], 2)
    return Q(f'A government in {city(r)} must choose between {a} and {b} for a new power station. Evaluate the two options, considering availability, reliability, cost and environmental impact, and give a justified recommendation.',
             f'{cap(a)}: advantages {RES[a][3]}; disadvantages {RES[a][4]}. {cap(b)}: advantages {RES[b][3]}; disadvantages {RES[b][4]}. A justified conclusion weighing reliability against emissions and cost.',
             '1 mark each (max 6): availability; reliability; cost; environmental impact; comparison of the two; justified conclusion [6]')


t73.add('C4', (2, 3, 4), 'multi_step')(_ren_c4)


@t73.add('C2', (2, 3, 4), 'explain')
def t73_rel(r, D):
    a = r.choice(['coal', 'natural gas', 'nuclear fission', 'hydroelectric', 'geothermal', 'biofuels'])
    b = r.choice(['wind', 'solar cells', 'waves', 'tidal'])
    why = {'wind': 'no output on calm days', 'solar cells': 'no output at night and less in cloudy weather', 'waves': 'output depends on the weather and sea state', 'tidal': 'output peaks only at certain times of day as the tide flows'}[b]
    return Q(f'Explain why {a} is more reliable than {b} for supplying electricity, and give one reason why a country might still choose {b}.',
             f'{cap(a)} can produce electricity whenever needed ({RES[a][3].split(";")[0]}); {b}: {why}. A country may still choose {b} because {RES[b][3].split(";")[0]}.',
             'reliability of first resource [1]; variability of second with reason [1]; valid reason to choose it [1] [3]')

N74 = 'The Sun as the main source of energy and nuclear fusion'
t74 = topic(N74, N74.lower(), 'nuclear fusion', 'the sun')
FX(t74, 'C1', (1, 2, 3), [
    ('What process releases energy in the Sun?', 'Nuclear fusion of hydrogen into helium', 'Light nuclei fuse at very high temperature and pressure.', ['Nuclear fission of uranium', 'Burning of hydrogen in oxygen', 'Radioactive decay of carbon']),
    ('Which energy resource does NOT ultimately come from the Sun?', 'Geothermal', 'Geothermal energy comes from inside the Earth.', ['Wind', 'Coal', 'Hydroelectric']),
    ('In nuclear fusion,', 'two light nuclei join to form a heavier nucleus', 'Fusion joins nuclei; fission splits them.', ['a heavy nucleus splits into two', 'electrons join the nucleus', 'atoms combine with oxygen']),
    ('Energy from the Sun reaches the Earth mainly as', 'electromagnetic radiation (light and infrared)', 'Radiation travels through the vacuum of space.', ['convection currents', 'conduction through space', 'sound waves']),
    ('Why does fusion need a very high temperature?', 'The nuclei must move fast enough to overcome their electrostatic repulsion', 'Nuclei are positive and repel each other.', ['To melt the hydrogen', 'To make the hydrogen burn', 'To slow the nuclei down']),
    ('State why wind energy is said to come from the Sun.', 'The Sun heats the Earth’s surface unevenly, causing convection currents in the air (winds).', 'uneven heating [1]; convection → wind [1] [2]'),
])
FX(t74, 'C2', (1, 2, 3, 4), [
    ('Explain how the energy in hydroelectric power originally came from the Sun.', 'The Sun evaporates water, which rises and falls as rain on high ground; the water gains gravitational potential energy that is released through turbines.', 'evaporation by Sun [1]; water raised to high ground (GPE) [1] [2]'),
    ('Explain why fusion is difficult to use in a power station on Earth.', 'Extremely high temperatures and pressures are needed to make nuclei fuse, and it is very hard to contain such hot plasma.', 'very high temperature/pressure [1]; containment difficult [1] [2]'),
    ('Compare nuclear fusion and nuclear fission.', 'Fusion joins light nuclei (e.g. hydrogen → helium); fission splits heavy nuclei (e.g. uranium); both release energy from the nuclear store; fusion powers stars, fission powers nuclear power stations.', 'fusion joins [1]; fission splits [1]; where each occurs [1] [3]'),
    ('Explain why fossil fuels are an indirect form of solar energy.', 'They come from ancient plants that stored the Sun’s energy by photosynthesis.', 'photosynthesis [1]; stored over millions of years [1] [2]'),
])


@t74.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t74_solar(r, D):
    I = r.choice([1000, 1360, 800, 1100])
    A = r.choice([0.5, 1.0, 1.5, 2.0, 3.0, 5.0])
    t = r.choice([60, 300, 600, 3600])
    if D <= 2:
        return numq(r, D, f'Radiation from the Sun delivers {I} J each second to every square metre of a surface facing it.', f'energy reaching an area of {g(A)} m² in {t} s', I * A * t, ' J', f'{I} × {g(A)} × {t}', [I * A, I * t, I * A * t / 60], fm=lambda x: sci(x, 3) if x >= 1e5 else g(x))
    eff = r.choice([0.2, 0.3, 0.4, 0.5, 0.6])
    m = r.choice([5, 10, 20, 50])
    E = I * A * t * eff
    dT = E / (m * 4200)
    return Q(f'A solar water heater has a collecting area of {g(A)} m². Sunlight delivers {I} W/m², and {g(eff * 100)}% of this is transferred to {m} kg of water (specific heat capacity 4200 J/(kg °C)). (a) Calculate the energy transferred to the water in {t} s. (b) Calculate the temperature rise. (c) Name the process in the Sun that releases this energy.',
             f'(a) {sci(E, 3) if E >= 1e5 else g(E, 3)} J (b) {g(dT, 3)} °C (c) nuclear fusion (hydrogen to helium).',
             f'(a) {I} × {g(A)} × {t} × {g(eff)} [1] (b) ΔT = E/(mc) [1] = {g(dT, 3)} °C [1] (c) fusion [1]' + (' [4]' if D <= 4 else '; why real rise is smaller (losses) [1] [5]'), 'multi_step')


@t74.add('C2', (2, 3, 4), 'explain')
def t74_chain(r, D):
    k = r.choice(['wind', 'waves', 'hydroelectric', 'biofuels', 'coal', 'oil', 'solar cells'])
    chain = {'wind': 'Sun heats the ground and air unevenly → convection currents → wind → turbines', 'waves': 'Sun → winds (uneven heating) → winds blow over the sea making waves → wave generators',
             'hydroelectric': 'Sun evaporates water → rain on high ground (GPE) → falls through turbines', 'biofuels': 'Sun → photosynthesis stores chemical energy in plants → fuel burned',
             'coal': 'Sun → photosynthesis in ancient plants → buried and compressed into coal → burned', 'oil': 'Sun → photosynthesis in ancient sea organisms → buried, formed oil → burned',
             'solar cells': 'Sun’s fusion → light radiation → photovoltaic cells'}[k]
    return Q(f'Trace the energy in {k} back to nuclear fusion in the Sun, describing each stage.', chain + '.', 'fusion in Sun → radiation [1]; intermediate stage(s) [1]; final use [1] [3]')


def _sun_c4(r, D):
    parts = [
        lambda r: ('Name the process that releases energy in the Sun.', 'Nuclear fusion.', '[1]'),
        lambda r: ('Describe what happens in this process.', 'Hydrogen nuclei join to form helium nuclei, releasing energy.', '[2]'),
        lambda r: ('Explain how energy travels from the Sun to the Earth.', 'As electromagnetic radiation, which can travel through a vacuum.', '[2]'),
        lambda r: ('Name two energy resources that do not depend on the Sun.', 'Tidal, geothermal (and nuclear fission).', '[2]'),
        lambda r: ('Explain how the Sun is the source of energy for wind power.', 'Uneven heating of the Earth causes convection currents in the atmosphere.', '[2]'),
    ]
    return compose(r, r.choice(['Almost all of our energy resources depend on the Sun.', f'A science museum in {city(r)} has an exhibit called "Powered by the Sun".']), parts, k=(2, 3, 4), type_='multi_step')


t74.add('C4', (2, 3, 4, 5), 'multi_step')(_sun_c4)

CHAPTERS[7] = [t71, t72, t73, t74]

# =========================================================== 8 Work and power
N81 = 'Work done W = Fd = ΔE'
t81 = topic(N81, N81.lower(), 'work done')
FX(t81, 'C1', (1, 2), [
    ('Work done on an object is equal to', 'force × distance moved in the direction of the force', 'W = Fd.', ['force ÷ distance', 'mass × distance', 'force × time']),
    ('What is the unit of work done?', 'joule (J)', '1 J = 1 N m of work.', ['watt (W)', 'newton (N)', 'pascal (Pa)']),
    ('A force of 50 N pushes a box 4 m along the floor. How much work is done?', '200 J', 'W = 50 × 4 = 200 J.', ['12.5 J', '54 J', '0.08 J']),
    ('When work is done on an object, energy is', 'transferred', 'Work done = energy transferred (W = ΔE).', ['destroyed', 'created', 'always stored as kinetic energy']),
    ('A person holds a heavy bag still at arm’s length. How much work is done on the bag?', 'None, because the bag does not move', 'No distance moved in the direction of the force ⇒ W = 0.', ['Its weight × its height', 'Its weight × time held', 'Infinite work']),
    ('Define one joule.', 'The work done when a force of 1 N moves an object 1 m in the direction of the force.', '1 N × 1 m [1]; in direction of force [1] [2]'),
])
FX(t81, 'C2', (1, 2, 3, 4), [
    ('Explain why work is done against friction when a box is pushed across a floor at constant speed, even though its kinetic energy does not change.', 'The pushing force moves through a distance, transferring energy; this energy goes to the internal (thermal) store of the box and floor via friction, not to kinetic energy.', 'force × distance → energy transferred [1]; goes to thermal store via friction [1] [2]'),
    ('Explain the link between work done and energy transferred when a crane lifts a load.', 'The work done by the crane’s upward force (force × height) equals the gain in the load’s gravitational potential energy (plus any energy wasted).', 'W = ΔE [1]; = gain in GPE [1] [2]'),
    ('A car brakes to a stop. Explain how the braking distance is related to the car’s kinetic energy.', 'Work done by the braking force (F × d) equals the kinetic energy removed, so d = Eₖ/F; more kinetic energy means a longer braking distance for the same force.', 'F × d = KE [1]; larger KE → longer distance [1] [2]'),
])
WORK = [('{p} pushes a shopping trolley', (20, 60), (5, 40)), ('A horse pulls a cart', (300, 900), (50, 400)), ('A tractor drags a log', (1500, 4000), (10, 80)),
        ('A crane lifts a load with a steady force', (2000, 20000), (5, 30)), ('A winch pulls a boat up a slipway', (800, 3000), (5, 20)), ('{p} pulls a suitcase through an airport in {c}', (15, 40), (50, 300)),
        ('An engine pushes a train', (50000, 200000), (100, 2000))]


@t81.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t81_w(r, D):
    fr, (f1, f2), (d1, d2) = r.choice(WORK)
    s = fr.format(p=person(r), c=city(r))
    F = r.choice([f1, round((f1 + f2) / 2, -1 if f2 < 1000 else -2), f2])
    d = r.choice([d1, round((d1 + d2) / 2), d2])
    W = F * d
    fm = lambda x: sci(x, 3) if x >= 1e6 else g(x)
    if D <= 2:
        return numq(r, D, f'{s} with a force of {g(F)} N through {g(d)} m in the direction of the force.', 'work done', W, ' J', f'W = Fd = {g(F)} × {g(d)}', [F / d, F + d, W / 10], fm=fm)
    if D == 3:
        if r.random() < 0.5:
            return Q(f'{s}. The work done is {fm(W)} J over a distance of {g(d)} m. Calculate the force, assuming it acts in the direction of motion.', f'{g(F)} N', f'F = W/d [1] = {fm(W)}/{g(d)} [1] = {g(F)} N [1] [3]')
        return Q(f'{s} with a force of {g(F / 1000, 3)} kN through {g(d / 1000, 3) if d >= 1000 else g(d)} {"km" if d >= 1000 else "m"}. Calculate the work done in J.', f'{fm(W)} J', f'convert to N and m [1]; W = Fd [1] = {fm(W)} J [1] [3]')
    m = r.choice([50, 80, 120, 200, 500])
    h = r.choice([2, 3, 5, 8, 10, 12])
    fr2 = r.choice([20, 40, 60, 100])
    Wl = m * G * h
    return Q(f'A motor lifts a {m} kg load through {h} m at a steady speed (g = 9.8 N/kg). Friction in the pulley adds a resistive force of {fr2} N throughout. (a) Calculate the weight of the load. (b) Calculate the work done against gravity. (c) Calculate the total work done by the motor. (d) State the gain in GPE of the load.',
             f'(a) {g(m * G, 3)} N (b) {g(Wl, 3)} J (c) {g(Wl + fr2 * h, 3)} J (d) {g(Wl, 3)} J',
             f'(a) mg [1] (b) W = Fd = {g(m * G, 3)} × {h} [1] (c) + {fr2} × {h} = {g(Wl + fr2 * h, 3)} J [1] (d) equals work against gravity [1]' + (' [4]' if D == 4 else '; energy against friction becomes thermal [1] [5]'), 'multi_step')


@t81.add('C2', (2, 3, 4), 'explain')
def t81_zero(r, D):
    sc = r.choice([('A waiter carries a tray horizontally across a room at constant height.', 'The upward force on the tray is perpendicular to the motion, so no work is done against gravity (ignoring starting and stopping).'),
                   ('A weightlifter holds a bar above his head for 5 s.', 'The bar does not move, so the distance is zero and no work is done on it, even though he gets tired.'),
                   ('A satellite moves in a circular orbit at constant speed.', 'Gravity acts towards the centre, perpendicular to the motion, so it does no work and the KE stays constant.'),
                   ('A student pushes hard against a brick wall that does not move.', 'There is no movement in the direction of the force, so no work is done on the wall.')])
    return Q(f'{sc[0]} Explain whether work is done by the force named or implied.', sc[1], 'work needs movement in direction of force [1]; applied correctly [1] [2]')


def _w_c4(r, D):
    m = r.choice([60, 70, 80])
    h = r.choice([3, 4, 6, 10])
    F = r.choice([200, 300, 400])
    d = r.choice([10, 20, 30])
    intro = f'{person(r)} (mass {m} kg) climbs stairs of vertical height {h} m and then pushes a box with a force of {F} N for {d} m along a corridor (g = 9.8 N/kg).'
    parts = [
        lambda r: ('Calculate the work done against gravity in climbing the stairs.', f'{g(m * G * h, 3)} J', 'W = mgh [2]'),
        lambda r: ('Calculate the work done pushing the box.', f'{F * d} J', 'W = Fd [1]'),
        lambda r: ('State where the energy transferred to the box ends up if the box moves at constant speed.', 'In the internal (thermal) store of the box, floor and air (via friction).', '[1]'),
        lambda r: ('Explain why the total chemical energy used by the person is greater than the total work done.', 'The body is not 100% efficient; much energy is transferred to the thermal store (body heat).', '[2]'),
        lambda r: ('State the energy store that increases when the stairs are climbed.', 'Gravitational potential.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t81.add('C4', (2, 3, 4, 5), 'multi_step')(_w_c4)


@t81.add('C2', (2, 3, 4), 'explain')
def t81_err(r, D):
    F = r.choice([20, 40, 50, 80, 120, 250])
    d = r.choice([2, 4, 5, 8, 10])
    who = person(r)
    return Q(f'{who} pushes a crate with a force of {F} N for {d} m and writes "work done = {F} ÷ {d} = {g(F / d)} J". Identify the error, give the correct work done and state where the energy goes if the crate moves at constant speed.',
             f'Work = force × distance, not force ÷ distance: W = {F} × {d} = {F * d} J. At constant speed the energy goes to the thermal store of the crate, floor and air (work against friction).',
             f'W = Fd not F/d [1]; {F * d} J [1]; energy to thermal store via friction [1] [3]')


relation(t81, 'C2', (2, 3), 'W = Fd', 'work done', {'force': 1, 'distance moved in the direction of the force': 1}, ['A tractor drags a log across a field.', 'A crane lifts a load with a steady force.', 'A student pushes a box across a floor.'])

N82 = 'Power P = W/t = ΔE/t'
t82 = topic(N82, N82.lower(), 'power')
FX(t82, 'C1', (1, 2), [
    ('Power is defined as', 'the rate of doing work (energy transferred per second)', 'P = W/t = ΔE/t.', ['force × distance', 'energy × time', 'the total energy used']),
    ('What is the unit of power?', 'watt (W)', '1 W = 1 J/s.', ['joule (J)', 'newton (N)', 'kilogram (kg)']),
    ('A motor transfers 600 J in 20 s. What is its power?', '30 W', 'P = 600/20 = 30 W.', ['12 000 W', '0.033 W', '620 W']),
    ('How much energy does a 2 kW heater transfer in 10 s?', '20 000 J', 'E = Pt = 2000 × 10 = 20 000 J.', ['200 J', '20 J', '5 J']),
    ('1 kW is equal to', '1000 W', 'kilo = 1000.', ['100 W', '1 000 000 W', '10 W']),
    ('State the meaning of a power of 1 watt.', 'One joule of energy transferred per second.', '[1]'),
])
FX(t82, 'C2', (1, 2, 3, 4), [
    ('Two students of equal weight climb the same stairs; one runs and one walks. Explain who does more work and who develops more power.', 'They do the same work (same weight × same height); the runner develops more power because the work is done in less time.', 'same work [1]; runner more power, less time [1] [2]'),
    ('Describe how to measure your own power when running up a flight of stairs.', 'Measure your mass (weight = mg), measure the vertical height of the stairs with a tape, time the climb with a stopwatch; P = mgh/t.', 'weight [1]; vertical height [1]; time and P = mgh/t [1] [3]'),
    ('Explain why a more powerful car can accelerate to 100 km/h in less time than a less powerful car of the same mass.', 'Both need the same gain in kinetic energy; the more powerful engine transfers energy at a greater rate, so it takes less time.', 'same KE needed [1]; more energy per second [1] [2]'),
])
PWR = [('An electric kettle', (1800, 3000)), ('A lift motor', (5000, 20000)), ('A hairdryer', (800, 2000)), ('A crane motor', (10000, 50000)), ('A microwave oven', (700, 1200)), ('An LED lamp', (5, 15)), ('A vacuum cleaner', (600, 1600))]


@t82.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t82_p(r, D):
    o, (p1, p2) = r.choice(PWR)
    P = r.choice([p1, round((p1 + p2) / 2, -1), p2])
    t = r.choice([5, 10, 20, 30, 60, 90, 120])
    E = P * t
    fm = lambda x: sci(x, 3) if x >= 1e6 else g(x)
    if D <= 2:
        if r.random() < 0.5:
            return numq(r, D, f'{o} transfers {fm(E)} J of energy in {t} s.', 'power', P, ' W', f'P = E/t = {fm(E)}/{t}', [E * t, t / E * 1e6, P / 1000], fm=fm)
        return numq(r, D, f'{o} has a power of {g(P)} W and is used for {t} s.', 'energy transferred', E, ' J', f'E = Pt = {g(P)} × {t}', [P / t, P * t / 60, P + t], fm=fm)
    if D == 3:
        tm = r.choice([2, 3, 5, 10, 15])
        return Q(f'{o} has a power of {g(P / 1000, 3)} kW and is switched on for {tm} minutes. Calculate the energy transferred in J.', f'{fm(P * tm * 60)} J', f'P = {g(P)} W, t = {tm * 60} s [1]; E = Pt [1] = {fm(P * tm * 60)} J [1] [3]')
    m = r.choice([600, 800, 1000, 1200])
    h = r.choice([10, 15, 20, 30])
    tt = r.choice([10, 15, 20, 25])
    Pu = m * G * h / tt
    return Q(f'A lift of total mass {m} kg rises {h} m in {tt} s at constant speed (g = 9.8 N/kg). (a) Calculate the gain in GPE. (b) Calculate the useful power output of the motor. (c) The motor’s input power is {g(round(Pu * 1.6, -2))} W. Calculate the energy wasted during the journey.',
             f'(a) {g(m * G * h, 3)} J (b) {g(Pu, 3)} W (c) {g(round(Pu * 1.6, -2) * tt - m * G * h, 3)} J',
             f'(a) mgh [1] (b) P = E/t [1] = {g(Pu, 3)} W [1] (c) input energy {g(round(Pu * 1.6, -2) * tt, 3)} J − useful [1]' + (' [4]' if D == 4 else '; where wasted energy goes (thermal in motor/cables, sound) [1] [5]'), 'multi_step')


@t82.add('C3', (2, 3, 4), 'numerical')
def t82_stairs(r, D):
    who = person(r)
    m = r.choice([45, 50, 55, 60, 65, 70])
    h = r.choice([3.0, 3.6, 4.2, 4.8, 6.0])
    t = r.choice([3.5, 4.0, 4.5, 5.0, 6.0, 8.0])
    P = m * G * h / t
    return Q(f'{who} (mass {m} kg) runs up a staircase of vertical height {g(h)} m in {g(t)} s (g = 9.8 N/kg). Calculate {who}’s useful power.', f'{g(P, 3)} W',
             f'work = mgh = {m} × 9.8 × {g(h)} = {g(m * G * h, 3)} J [1]; P = W/t [1] = {g(P, 3)} W [1] [3]')


relation(t82, 'C2', (2, 3), 'P = ΔE/t', 'power', {'energy transferred': 1, 'time taken': -1}, ['A motor lifts loads on a building site.', 'A student compares two kettles.', 'An athlete trains by running up stairs.'])


def _p_c4b(r, D):
    P = r.choice([1500, 2000, 2400, 3000])
    t = r.choice([60, 90, 120, 150])
    m = r.choice([0.5, 1.0, 1.5])
    intro = f'An electric kettle rated at {P} W heats {m} kg of water for {t} s.'
    parts = [
        lambda r: ('Calculate the electrical energy transferred.', f'{P * t} J', 'E = Pt [2]'),
        lambda r: (f'Only {int(0.9 * P * t)} J reaches the water. Calculate the energy wasted.', f'{P * t - int(0.9 * P * t)} J', '[1]'),
        lambda r: ('Calculate the useful power.', f'{g(0.9 * P)} W', '[1]'),
        lambda r: ('Explain what is meant by a power of ' + str(P) + ' W.', f'{P} J of energy is transferred each second.', '[1]'),
        lambda r: ('Suggest why a more powerful kettle boils the same water faster.', 'It transfers the same energy at a greater rate, so less time is needed.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t82.add('C4', (2, 3, 4, 5), 'multi_step')(_p_c4b)

N83 = 'Efficiency calculations using energy and power'
t83 = topic(N83, N83.lower(), 'efficiency calculations')
FX(t83, 'C1', (1, 2), [
    ('Which equation gives efficiency in terms of power?', 'efficiency = useful power output ÷ total power input × 100%', 'Same idea as energy efficiency, per second.', ['efficiency = total power input ÷ useful power output', 'efficiency = useful power × time', 'efficiency = wasted power ÷ total power']),
    ('A motor has an input power of 200 W and a useful output power of 150 W. What is its efficiency?', '75%', '150/200 × 100 = 75%.', ['133%', '25%', '50%']),
    ('A 60% efficient motor has an input of 500 W. What is its useful output power?', '300 W', '0.60 × 500 = 300 W.', ['833 W', '200 W', '560 W']),
    ('A device has an efficiency of 40%. What fraction of its input is wasted?', '0.60', '1 − 0.40 = 0.60.', ['0.40', '0.04', '1.40']),
    ('State why the efficiency of a real machine is always less than 100%.', 'Some energy is always wasted, e.g. by friction or heating, and dissipated to the surroundings.', '[1]'),
])
FX(t83, 'C2', (1, 2, 3, 4), [
    ('Explain why a motor lifting a load becomes less efficient if its bearings are not lubricated.', 'More friction means more of the input energy is transferred to thermal energy, so a smaller fraction becomes useful work.', 'more friction [1]; more wasted, smaller useful fraction [1] [2]'),
    ('Explain why efficiency calculated using powers gives the same result as using energies over the same time.', 'Power = energy/time; for the same time both useful and input energies are divided by the same t, so the ratio is unchanged.', 'P = E/t [1]; t cancels in ratio [1] [2]'),
    ('Describe an experiment to find the efficiency of a small electric motor lifting a mass.', 'Measure input power from voltmeter and ammeter readings (P = IV) and time; measure the mass and height lifted; useful energy = mgh; efficiency = mgh ÷ (IVt) × 100%.', 'electrical input measured [1]; mgh measured [1]; ratio [1] [3]'),
])
MOT = [('A crane motor', 'lifts a steel girder'), ('A winch motor', 'raises a boat'), ('A toy motor', 'lifts a small mass'), ('A lift motor', 'raises a lift car'), ('A pump motor', 'raises water into a tank'), ('A conveyor motor', 'lifts bags of cement up a ramp')]


@t83.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t83_eff(r, D):
    o, act = r.choice(MOT)
    small = 'toy' in o
    m = r.choice([0.1, 0.2, 0.25, 0.5]) if small else r.choice([200, 300, 500, 800, 1000, 1500])
    h = r.choice([0.5, 0.8, 1.0, 1.2]) if small else r.choice([5, 8, 10, 12, 20])
    t = r.choice([2, 4, 5, 8]) if small else r.choice([10, 15, 20, 30, 40])
    eff = r.choice([0.2, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8])
    Eu = m * G * h
    Pu = Eu / t
    Pin = Pu / eff
    if D <= 2:
        return numq(r, D, f'{o} has a useful power output of {g(Pu, 3)} W and an input power of {g(Pin, 3)} W.', 'efficiency', eff * 100, '%', f'efficiency = {g(Pu, 3)}/{g(Pin, 3)} × 100', [Pin / Pu * 100, (1 - eff) * 100, eff * 10])
    if D == 3:
        return Q(f'{o} {act} of mass {g(m)} kg through {g(h)} m in {t} s (g = 9.8 N/kg). Its input power is {g(Pin, 3)} W. Calculate its efficiency.', f'{g(eff * 100, 3)}%',
                 f'useful energy = mgh = {g(Eu, 3)} J [1]; useful power = {g(Pu, 3)} W [1]; efficiency = {g(eff * 100, 3)}% [1] [3]')
    V = r.choice([6, 12, 230]) if not small else r.choice([3, 4.5, 6])
    I = Pin / V
    return Q(f'{o} {act} of mass {g(m)} kg through {g(h)} m in {t} s (g = 9.8 N/kg). The supply provides {g(Pin, 3)} W. (a) Calculate the useful energy output. (b) Calculate the total energy input. (c) Calculate the efficiency. (d) Calculate the energy wasted and suggest where it goes.',
             f'(a) {g(Eu, 3)} J (b) {g(Pin * t, 3)} J (c) {g(eff * 100, 3)}% (d) {g(Pin * t - Eu, 3)} J; thermal energy in the motor windings and bearings, and sound.',
             f'(a) mgh [1] (b) Pt [1] (c) ratio × 100 [1] (d) difference [1]' + (' [4]' if D == 4 else '; plausible destination [1] [5]'), 'multi_step')


@t83.add('C2', (2, 3, 4), 'explain')
def t83_cmp(r, D):
    a, b = two_people(r)
    e1, e2 = r.sample([30, 45, 60, 70, 85, 90], 2)
    P = r.choice([500, 1000, 2000])
    return Q(f'Two pumps each take {P} W from the supply. Pump A is {e1}% efficient and pump B is {e2}% efficient. Explain which pump raises water faster and calculate the difference in useful power.', f'Pump {"A" if e1 > e2 else "B"}: more useful power. Difference = {g(abs(e1 - e2) / 100 * P)} W.',
             'higher efficiency → more useful power from same input [1]; both useful powers [1]; difference [1] [3]')


def _eff_c4(r, D):
    o, act = r.choice(MOT[:2] + MOT[3:])
    m = r.choice([400, 500, 800])
    h = r.choice([10, 15, 20])
    t = r.choice([20, 25, 40])
    Pin = r.choice([5000, 6000, 8000])
    Eu = m * G * h
    parts = [
        lambda r: ('Calculate the useful energy output.', f'{g(Eu, 3)} J', 'mgh [2]'),
        lambda r: ('Calculate the useful power output.', f'{g(Eu / t, 3)} W', '[1]'),
        lambda r: ('Calculate the efficiency.', f'{g(Eu / t / Pin * 100, 3)}%', '[2]'),
        lambda r: ('Explain why the efficiency is less than 100%.', 'Energy is wasted as thermal energy (friction, resistance of coils) and sound.', '[2]'),
        lambda r: ('Suggest one way to improve the efficiency.', 'Lubricate moving parts / use lower-resistance wires.', '[1]'),
    ]
    return compose(r, f'{o} {act} of mass {m} kg through {h} m in {t} s. The input power is {Pin} W (g = 9.8 N/kg).', parts, k=(2, 3, 4), type_='multi_step')


t83.add('C4', (2, 3, 4, 5), 'multi_step')(_eff_c4)
t83.add('C3', (4, 5), 'multi_step')(_eff_c4)

CHAPTERS[8] = [t81, t82, t83]

# =========================================================== 9 Kinetic particle model of matter
SUBS = [('water', 0, 100), ('ethanol', -114, 78), ('oxygen', -218, -183), ('nitrogen', -210, -196), ('iron', 1538, 2862), ('mercury', -39, 357), ('sodium chloride', 801, 1413), ('copper', 1085, 2562),
        ('paraffin wax', 55, 370), ('butane', -138, -1), ('lead', 327, 1749), ('bromine', -7, 59)]
N91 = 'States of matter and the particle model of solids, liquids and gases'
t91 = topic(N91, N91.lower(), 'states of matter', 'particle model')
FX(t91, 'C1', (1, 2), [
    ('In which state are the particles close together but free to move past each other?', 'Liquid', 'Liquid: close, random arrangement, can slide past each other.', ['Solid', 'Gas', 'Plasma']),
    ('Which state has a fixed shape and a fixed volume?', 'Solid', 'Solid particles vibrate about fixed positions.', ['Liquid', 'Gas', 'Both liquid and gas']),
    ('Why can gases be compressed easily?', 'There are large spaces between the particles', 'Gas particles are far apart.', ['The particles are very small', 'The particles do not move', 'The particles attract strongly']),
    ('How do the particles in a solid move?', 'They vibrate about fixed positions', 'Strong forces hold them in a regular lattice.', ['They move randomly at high speed', 'They slide past each other', 'They do not move at all']),
    ('Changing from a gas to a liquid is called', 'condensation', 'Gas → liquid: condensing.', ['evaporation', 'melting', 'sublimation']),
    ('Which state of matter takes the shape of its container but has a fixed volume?', 'Liquid', 'Liquids flow but are nearly incompressible.', ['Gas', 'Solid', 'None']),
])
FX(t91, 'C2', (1, 2, 3, 4), [
    ('Explain, using the particle model, why a solid has a fixed shape.', 'The particles are held in fixed positions in a regular arrangement by strong forces between them; they can only vibrate.', 'strong forces / fixed positions [1]; only vibrate [1] [2]'),
    ('Explain why a liquid can flow but cannot easily be compressed.', 'The particles can move past each other, so it flows, but they are already touching, so there is little space to squeeze them into.', 'particles move past each other [1]; close together, no space [1] [2]'),
    ('Explain why a gas fills any container it is put into.', 'The particles move randomly at high speed in all directions with negligible forces between them, so they spread out to fill all the space.', 'random fast motion [1]; weak forces, spread out [1] [2]'),
    ('Describe the differences in the arrangement and motion of particles in a solid and a gas.', 'Solid: close, regular arrangement, vibrate about fixed positions. Gas: far apart, random arrangement, move rapidly in random directions.', 'arrangement contrast [1]; motion contrast [1] [2]'),
    ('Explain why gases have much lower densities than solids.', 'The particles are much further apart, so a given volume contains far fewer particles and less mass.', 'particles far apart [1]; less mass per volume [1] [2]'),
])


@t91.add('C3', (1, 2, 3, 4), 'numerical')
def t91_state(r, D):
    (n, mp, bp) = r.choice(SUBS)
    T = r.choice([mp - 20, (mp + bp) // 2, bp + 30, mp - 50, bp + 100, 20, 25])
    st = 'solid' if T < mp else 'liquid' if T < bp else 'gas'
    if D <= 2:
        opts, a = mcq(r, st, ['solid', 'liquid', 'gas', 'all three at once'])
        return Q(f'{cap(n)} melts at {mp} °C and boils at {bp} °C. What is its state at {T} °C?', a, f'{T} °C is {"below the melting point" if st == "solid" else "between melting and boiling points" if st == "liquid" else "above the boiling point"}: {st}.', opts=opts)
    (n2, mp2, bp2) = r.choice([x for x in SUBS if x[0] != n])
    st2 = 'solid' if T < mp2 else 'liquid' if T < bp2 else 'gas'
    return Q(f'Melting and boiling points: {n} {mp} °C and {bp} °C; {n2} {mp2} °C and {bp2} °C. State the state of each at {T} °C and describe the motion of the particles in each.',
             f'{cap(n)}: {st}; {n2}: {st2}. ' + ' '.join({'solid': 'Solid: particles vibrate about fixed positions.', 'liquid': 'Liquid: particles move past each other.', 'gas': 'Gas: particles move rapidly and randomly, far apart.'}[x] for x in dict.fromkeys([st, st2])),
             'state of each [2]; particle motion description [1]' + (' [3]' if D == 3 else '; explains in terms of temperature relative to mp/bp [1] [4]'))


@t91.add('C2', (2, 3, 4), 'explain')
def t91_prop(r, D):
    prop = r.choice([('can be poured', 'liquid and gas', 'particles can move past each other'), ('can be compressed easily', 'gas', 'large spaces between particles'), ('has a fixed volume', 'solid and liquid', 'particles are close together, held by attractive forces'),
                     ('has a fixed shape', 'solid', 'particles are held in fixed positions'), ('diffuses quickly', 'gas', 'particles move rapidly and randomly with large spaces')])
    return Q(f'State which state(s) of matter {prop[0]} and explain this using the particle model.', f'{cap(prop[1])}: {prop[2]}.', 'correct state(s) [1]; particle explanation [1] [2]')


def _pm_c4(r, D):
    (n, mp, bp) = r.choice(SUBS)
    parts = [
        lambda r: (f'State the state of {n} at {mp - 10} °C.', 'Solid.', '[1]'),
        lambda r: (f'State the state of {n} at {bp + 10} °C.', 'Gas.', '[1]'),
        lambda r: ('Describe the arrangement and motion of the particles in the liquid state.', 'Close together, irregular arrangement, moving past each other.', '[2]'),
        lambda r: ('Explain what happens to the particles when the substance melts.', 'They gain energy and vibrate more until they break free of fixed positions and can move past each other.', '[2]'),
        lambda r: ('Explain why the gas is much less dense than the liquid.', 'Gas particles are much further apart.', '[1]'),
        lambda r: ('Explain why the gas can be compressed but the liquid cannot easily be.', 'Gas has large spaces between particles; in the liquid they are touching.', '[2]'),
    ]
    return compose(r, f'{cap(n)} melts at {mp} °C and boils at {bp} °C.', parts, k=(2, 3, 4), type_='multi_step')


t91.add('C4', (2, 3, 4, 5), 'multi_step')(_pm_c4)
t91.add('C3', (3, 4), 'multi_step')(_pm_c4)

N92 = 'Brownian motion and gas pressure from particle collisions'
t92 = topic(N92, N92.lower(), 'brownian motion', 'gas pressure')
FX(t92, 'C1', (1, 2), [
    ('Brownian motion of smoke particles seen under a microscope is', 'random, jerky movement', 'Smoke particles move randomly as they are hit by air molecules.', ['steady movement in one direction', 'circular motion', 'no movement at all']),
    ('What causes Brownian motion of smoke particles in air?', 'Collisions with fast-moving air molecules', 'Many random, unequal impacts from air molecules.', ['Convection currents in the cell', 'Gravity pulling the smoke down', 'Light from the microscope pushing them']),
    ('How does a gas exert a pressure on the walls of its container?', 'Its particles collide with the walls, exerting forces on them', 'Pressure = total force of collisions per unit area.', ['Its particles stick to the walls', 'Its particles repel the walls without touching', 'Gravity pulls the gas onto the walls']),
    ('When a gas in a sealed rigid container is heated, its pressure', 'increases', 'Particles move faster, hitting walls harder and more often.', ['decreases', 'stays the same', 'becomes zero']),
    ('In Brownian motion, why are the air molecules themselves not seen?', 'They are far too small to be seen with a light microscope', 'Only the much larger smoke particles are visible.', ['They are transparent', 'They do not move', 'They are too fast to exist']),
    ('State what Brownian motion provides evidence for.', 'That the particles of a fluid (air) are moving randomly and continuously.', '[1]'),
])
FX(t92, 'C2', (1, 2, 3, 4), [
    ('Explain why smoke particles in air move randomly.', 'They are bombarded by many much smaller, fast-moving air molecules from all sides; at any instant the collisions are unbalanced, so the smoke particle is pushed in a random direction.', 'collisions with air molecules [1]; unbalanced, random [1]; molecules small and fast [1] [3]'),
    ('Explain, in terms of particles, why the pressure of a gas increases when it is heated at constant volume.', 'The particles gain kinetic energy and move faster, so they hit the walls more often and with more force; force per unit area increases.', 'faster particles [1]; more frequent collisions [1]; harder collisions / more force [1] [3]'),
    ('Explain why the Brownian motion of smaller smoke particles is more vigorous than that of larger ones.', 'Smaller particles have less mass, so the unbalanced forces from collisions give them a larger acceleration.', 'smaller mass [1]; larger effect of unbalanced collisions [1] [2]'),
    ('Explain why a balloon expands when more air is pumped into it.', 'More particles inside mean more collisions per second with the inside wall, increasing pressure inside above the pressure outside, so the rubber stretches.', 'more particles → more collisions [1]; pressure inside > outside [1] [2]'),
])
GASSC = [('a car tyre on a hot day in {c}', 'heated', 'increase'), ('an aerosol can left in the sun', 'heated', 'increase'), ('a sealed bottle put into a fridge', 'cooled', 'decrease'),
         ('a gas cylinder stored in a cold warehouse', 'cooled', 'decrease'), ('a football left in a hot car', 'heated', 'increase'), ('a sealed food container put into a freezer', 'cooled', 'decrease')]


@t92.add('C2', (1, 2, 3, 4), 'explain')
def t92_sc(r, D):
    sc, how, ch = r.choice(GASSC)
    sc = sc.format(c=city(r))
    return Q(f'Consider the air inside {sc}. The air is {how} at constant volume. Predict how the pressure changes and explain in terms of the particles.', f'Pressure will {ch}: particles move {"faster" if ch == "increase" else "slower"}, hitting the walls {"more" if ch == "increase" else "less"} often and with {"more" if ch == "increase" else "less"} force.',
             'prediction [1]; speed of particles [1]; collisions frequency/force [1] [3]' if D >= 3 else 'prediction [1]; particle explanation [1] [2]')


@t92.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t92_force(r, D):
    p = r.choice([100, 120, 150, 200, 250, 300]) * 1000
    A = r.choice([0.01, 0.02, 0.05, 0.1, 0.2, 0.5])
    o = r.choice(['the inside wall of a gas cylinder', 'a piston in a cylinder of gas', 'the lid of a pressure cooker', 'a square panel of a sealed tank', 'the end of a bicycle pump'])
    if D <= 2:
        return numq(r, D, f'Gas at a pressure of {g(p / 1000)} kPa acts on {o} of area {g(A)} m².', 'force exerted by the gas', p * A, ' N', f'F = pA = {g(p)} × {g(A)}', [p / A, p * A / 1000, A / p])
    if D == 3:
        return Q(f'Gas particles colliding with {o} of area {g(A * 1e4)} cm² exert a total force of {g(p * A)} N. Calculate the gas pressure in kPa and explain how the particles produce this force.', f'{g(p / 1000)} kPa; the particles collide with the surface and change momentum, exerting a force.',
                 f'A = {g(A)} m² [1]; p = F/A = {g(p / 1000)} kPa [1]; collisions with surface exert force [1] [3]')
    return Q(f'Gas at {g(p / 1000)} kPa acts on {o} of area {g(A)} m². (a) Calculate the force on it. (b) The gas is heated at constant volume and the pressure rises by 20%. Calculate the new force. (c) Explain the increase using the kinetic particle model.',
             f'(a) {g(p * A)} N (b) {g(1.2 * p * A)} N (c) particles move faster, hitting the surface more often and harder.',
             f'(a) F = pA [1] (b) × 1.2 [1] (c) faster particles [1]; more frequent and harder collisions [1]' + (' [4]' if D == 4 else '; force = rate of change of momentum stated [1] [5]'), 'multi_step')


def _bm_c4(r, D):
    parts = [
        lambda r: ('Describe what is seen through the microscope.', 'Bright specks (smoke particles) moving in a random, jerky way.', '[2]'),
        lambda r: ('Explain what causes this motion.', 'Random collisions from invisible, fast-moving air molecules.', '[2]'),
        lambda r: ('State what this tells us about air molecules.', 'They are very small and moving rapidly and randomly.', '[2]'),
        lambda r: ('Predict how the motion changes if the air is warmed, and explain.', 'More vigorous: air molecules move faster, so collisions are harder.', '[2]'),
        lambda r: ('Explain why larger particles show less Brownian motion.', 'More mass: unbalanced forces produce smaller accelerations, and more collisions average out.', '[2]'),
    ]
    return compose(r, r.choice([f'{person(r)} looks at a smoke cell through a microscope.', 'Smoke is trapped in a small glass cell and lit from the side.', 'A teacher demonstrates Brownian motion using pollen grains in water.']), parts, k=(2, 3, 4), type_='multi_step')


t92.add('C4', (2, 3, 4, 5), 'multi_step')(_bm_c4)

N93 = 'Gas pressure and volume at constant temperature: pV = constant'
t93 = topic(N93, N93.lower(), 'pv = constant', 'gas pressure and volume')
FX(t93, 'C1', (1, 2), [
    ('For a fixed mass of gas at constant temperature, if the volume is halved, the pressure', 'doubles', 'pV = constant: p ∝ 1/V.', ['halves', 'stays the same', 'quadruples']),
    ('Which equation applies to a fixed mass of gas at constant temperature?', 'p₁V₁ = p₂V₂', 'Boyle’s law: pV = constant.', ['p₁/V₁ = p₂/V₂', 'p₁ + V₁ = p₂ + V₂', 'p₁V₂ = p₂V₁']),
    ('A gas at 100 kPa occupies 300 cm³. It is compressed to 150 cm³ at constant temperature. What is the new pressure?', '200 kPa', '100 × 300 = p × 150 → 200 kPa.', ['50 kPa', '150 kPa', '450 kPa']),
    ('A graph of p against 1/V for a gas at constant temperature is', 'a straight line through the origin', 'p ∝ 1/V.', ['a horizontal line', 'a curve rising steeply', 'a straight line with negative gradient']),
    ('State two quantities that must be kept constant for pV = constant to apply.', 'The temperature and the mass (amount) of gas.', '[2]'),
])
FX(t93, 'C2', (1, 2, 3, 4), [
    ('Explain, in terms of particles, why compressing a gas at constant temperature increases its pressure.', 'The same number of particles are in a smaller volume, so they hit the walls more often per unit area; their speed is unchanged (constant temperature) but the collision rate increases.', 'same particles, smaller volume [1]; more frequent collisions per unit area [1]; same speed at constant T [1] [3]'),
    ('Explain why the gas should be compressed slowly in an experiment to test pV = constant.', 'Compressing quickly does work on the gas and warms it; going slowly lets thermal energy escape so the temperature stays constant.', 'fast compression heats gas [1]; slow keeps T constant [1] [2]'),
    ('Explain why air bubbles released by a diver get bigger as they rise.', 'The water pressure decreases as the bubble rises (less depth), so at roughly constant temperature its volume increases (pV = constant).', 'pressure decreases with smaller depth [1]; V increases as p decreases [1] [2]'),
])
GASV = [('Air trapped in a bicycle pump', 'cm³', 'kPa'), ('Gas in a syringe sealed at the nozzle', 'cm³', 'kPa'), ('Air in a diver’s lungs', 'litres', 'kPa'), ('Gas in a cylinder fitted with a piston', 'cm³', 'kPa'),
        ('Air in a weather balloon (at roughly constant temperature)', 'm³', 'kPa'), ('Helium in a party balloon', 'litres', 'kPa')]


@t93.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t93_boyle(r, D):
    o, vu, pu = r.choice(GASV)
    p1 = r.choice([80, 100, 101, 120, 150, 200, 250])
    V1 = r.choice([20, 30, 40, 50, 60, 80, 100, 120]) if vu == 'cm³' else r.choice([2, 3, 4, 5, 6, 8])
    f = r.choice([0.5, 0.25, 0.4, 0.6, 0.8, 1.5, 2, 2.5])
    V2 = V1 * f
    p2 = p1 * V1 / V2
    s = f'{o} has a volume of {g(V1)} {vu} at a pressure of {p1} {pu}. The volume changes to {g(V2)} {vu} at constant temperature.'
    if D <= 2:
        return numq(r, D, s, 'new pressure', p2, ' ' + pu, f'p₂ = p₁V₁/V₂ = {p1} × {g(V1)}/{g(V2)}', [p1 * V2 / V1, p1 * f, p1 + V1 - V2])
    if D == 3:
        p2b = r.choice([150, 200, 250, 300, 400])
        V2b = p1 * V1 / p2b
        return Q(f'{o} has a volume of {g(V1)} {vu} at {p1} {pu}. It is compressed slowly at constant temperature until the pressure is {p2b} {pu}. Calculate the new volume.', f'{g(V2b, 3)} {vu}',
                 f'p₁V₁ = p₂V₂ [1]; V₂ = {p1} × {g(V1)}/{p2b} [1] = {g(V2b, 3)} {vu} [1] [3]')
    h = r.choice([10, 20, 30])
    pd = 100 + 1030 * G * h / 1000
    Vb = r.choice([2, 4, 5, 8])
    Vs = pd * Vb / 100
    return Q(f'A diver at a depth of {h} m in sea water (density 1030 kg/m³) releases an air bubble of volume {Vb} cm³. Atmospheric pressure is 100 kPa; g = 9.8 N/kg; the temperature is constant. (a) Calculate the total pressure at {h} m. (b) Calculate the volume of the bubble just below the surface. (c) Explain, using the particle model, why the bubble expands as it rises.',
             f'(a) {g(pd, 3)} kPa (b) {g(Vs, 3)} cm³ (c) pressure outside falls, so the gas particles push the bubble wall out until the pressure inside matches; the same particles spread over a larger volume.',
             f'(a) 100 + ρgh/1000 = {g(pd, 3)} kPa [1] (b) p₁V₁ = p₂V₂ [1]; {g(Vs, 3)} cm³ [1] (c) lower outside pressure / fewer collisions per unit area at larger volume [1]' + (' [4]' if D == 4 else '; assumption of constant temperature stated [1] [5]'), 'multi_step')


@t93.add('C3', (2, 3, 4), 'case')
def t93_table(r, D):
    k = r.choice([2400, 3000, 3600, 4800, 6000])
    Vs = r.sample([20, 24, 30, 40, 48, 60, 80], 4)
    Vs.sort()
    ps = [k / v for v in Vs]
    bad = r.randrange(4)
    ps2 = ps[:]
    ps2[bad] = ps[bad] * r.choice([0.85, 1.15])
    return Q(f'{person(r)} compresses air in a syringe at constant temperature: volume/cm³ = {", ".join(map(str, Vs))}; pressure/kPa = {", ".join(g(p, 3) for p in ps2)}. (a) Calculate pV for each reading. (b) Identify the reading that does not fit and suggest a cause. (c) State the conclusion.',
             f'(a) pV ≈ {k} for all except the reading at {Vs[bad]} cm³ ({g(ps2[bad] * Vs[bad], 3)}). (b) {Vs[bad]} cm³ reading – e.g. temperature changed (compressed too quickly) or misread gauge. (c) pV is constant: p is inversely proportional to V.',
             '(a) products calculated [1] (b) anomaly identified with cause [1] (c) inverse proportion [1]' + (' [3]' if D < 4 else '; suggests plotting p against 1/V for a straight line [1] [4]'))


relation(t93, 'C2', (2, 3), 'pV = constant', 'pressure', {'volume': -1}, ['A fixed mass of air is trapped in a sealed syringe at constant temperature.', 'Gas in a cylinder with a piston is kept at room temperature.', 'Air in a pump is compressed slowly.'])


def _pv_c4(r, D):
    p1 = r.choice([100, 120])
    V1 = r.choice([60, 80, 100, 120])
    intro = f'A sealed syringe contains {V1} cm³ of air at {p1} kPa. The plunger is pushed in slowly at constant temperature.'
    parts = [
        lambda r: (f'Calculate the pressure when the volume is {V1 // 2} cm³.', f'{2 * p1} kPa', 'p₁V₁ = p₂V₂ [2]'),
        lambda r: (f'Calculate the volume when the pressure is {3 * p1} kPa.', f'{g(V1 / 3, 3)} cm³', '[2]'),
        lambda r: ('Explain why the plunger must be pushed in slowly.', 'To keep the temperature constant; fast compression warms the gas.', '[1]'),
        lambda r: ('Explain the pressure increase in terms of particles.', 'Same number of particles in a smaller volume hit the walls more often per unit area.', '[2]'),
        lambda r: ('Sketch-describe the graph of p against V.', 'A curve (hyperbola): p decreases as V increases, never touching the axes.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t93.add('C4', (2, 3, 4, 5), 'multi_step')(_pv_c4)

N94 = 'Temperature, absolute zero and the Kelvin scale'
t94 = topic(N94, N94.lower(), 'absolute zero', 'kelvin scale')
FX(t94, 'C1', (1, 2), [
    ('What is absolute zero on the Celsius scale?', '−273 °C', 'Absolute zero = 0 K = −273 °C.', ['0 °C', '−100 °C', '273 °C']),
    ('How is a temperature in °C converted to kelvin?', 'Add 273', 'T (K) = θ (°C) + 273.', ['Subtract 273', 'Multiply by 273', 'Divide by 273']),
    ('What is 27 °C on the Kelvin scale?', '300 K', '27 + 273 = 300 K.', ['246 K', '27 K', '−246 K']),
    ('At absolute zero, the particles of a substance', 'have the least possible kinetic energy', 'No lower temperature is possible.', ['move fastest', 'turn into a gas', 'have infinite energy']),
    ('A temperature rise of 10 °C is the same as a rise of', '10 K', 'The degree intervals are the same size.', ['283 K', '263 K', '2.73 K']),
    ('Explain what is meant by absolute zero.', 'The lowest possible temperature, at which particles have the least (minimum) kinetic energy.', '[1]'),
])
FX(t94, 'C2', (1, 2, 3, 4), [
    ('Explain how the average speed of gas particles is related to temperature.', 'Higher temperature means a higher average kinetic energy of the particles, so they move faster on average; the Kelvin temperature is proportional to the average kinetic energy.', 'temperature ∝ average KE [1]; higher T faster particles [1] [2]'),
    ('Explain why there cannot be a temperature lower than absolute zero.', 'At absolute zero the particles have their minimum possible kinetic energy; they cannot have less, so the temperature cannot fall further.', 'minimum KE [1]; cannot be reduced [1] [2]'),
    ('A student says "a gas at 40 °C has twice the particle energy of the same gas at 20 °C". Explain why this is wrong.', 'Average kinetic energy is proportional to the Kelvin temperature: 313 K vs 293 K, an increase of only about 7%.', 'must use kelvin [1]; 313/293 ≈ 1.07 [1] [2]'),
])


@t94.add('C3', (1, 2, 3, 4), 'numerical')
def t94_conv(r, D):
    ctx = r.choice(['The temperature on a winter morning in Toronto is', 'Liquid nitrogen boils at', 'A hot day in Dubai reaches', 'The surface of a pan is', 'Body temperature is', 'A freezer is set to', 'The boiling point of water is', 'Dry ice sublimes at'])
    th = {'Toronto': -18, 'nitrogen': -196, 'Dubai': 46, 'pan': 180, 'Body': 37, 'freezer': -20, 'boiling': 100, 'Dry ice': -78}
    c = next(v for k, v in th.items() if k in ctx)
    if D <= 2:
        if r.random() < 0.5:
            return numq(r, D, f'{ctx} {c} °C.', 'temperature in kelvin', c + 273, ' K', f'T = {c} + 273', [c - 273 if c - 273 > 0 else abs(c - 273), abs(c) + 100, 273 - c], fm=lambda x: str(int(round(x))))
        return numq(r, D, f'{ctx} {c + 273} K.', 'temperature in degrees Celsius', c, ' °C', f'θ = {c + 273} − 273', [], fm=lambda x: str(int(round(x)))) if c > 0 else \
            Q(f'{ctx} {c + 273} K. What is this in °C?', f'{c} °C', f'θ = T − 273 = {c} °C.', opts=mcq(r, f'{c} °C', [f'{c + 546} °C', f'{-c} °C', f'{c + 273} °C'])[0])
    c2 = r.choice([20, 25, 40, 60, 80, 100])
    if D == 3:
        rise = r.choice([30, 50, 80, 120])
        return Q(f'{ctx} {c} °C. The sample is then heated to {c + rise} °C. Convert both temperatures to kelvin and state the temperature rise in kelvin.',
                 f'{c + 273} K to {c + rise + 273} K; rise = {rise} K', f'add 273 to each [2]; rise in K = rise in °C = {rise} K [1] [3]')
    T1, T2 = c2 + 273, 2 * (c2 + 273)
    return Q(f'A gas at {c2} °C is heated until the average kinetic energy of its particles doubles. (a) Convert {c2} °C to kelvin. (b) Calculate the final temperature in K and in °C. (c) Explain why you cannot simply double {c2} °C.',
             f'(a) {T1} K (b) {T2} K = {T2 - 273} °C (c) average KE is proportional to the Kelvin temperature; the Celsius zero is not absolute zero.',
             f'(a) {T1} K [1] (b) {T2} K [1]; {T2 - 273} °C [1] (c) KE ∝ T in kelvin [1] [4]', 'multi_step')


def _k_c4b(r, D):
    a = r.choice([-196, -78, -40, 0])
    b = r.choice([20, 37, 100, 250])
    parts = [
        lambda r: (f'Convert {a} °C to kelvin.', f'{a + 273} K', '[1]'),
        lambda r: (f'Convert {b} °C to kelvin.', f'{b + 273} K', '[1]'),
        lambda r: ('State the temperature change in kelvin.', f'{b - a} K', '[1]'),
        lambda r: ('Describe the motion of the particles at absolute zero.', 'They have minimum kinetic energy (as little motion as possible).', '[1]'),
        lambda r: ('Explain why scientists prefer the Kelvin scale when studying gases.', 'Kelvin temperature is proportional to the average kinetic energy of particles and has no negative values.', '[2]'),
        lambda r: ('Calculate the ratio of the average kinetic energy of the particles at the higher temperature to that at the lower temperature.', f'{g((b + 273) / (a + 273), 3)}', 'ratio of kelvin temperatures [2]'),
    ]
    return compose(r, f'A sample of gas is warmed from {a} °C to {b} °C.', parts, k=(2, 3, 4), type_='multi_step')


t94.add('C4', (2, 3, 4, 5), 'multi_step')(_k_c4b)

CHAPTERS[9] = [t91, t92, t93, t94]

# =========================================================== 10 Thermal properties of matter
N101 = 'Thermal expansion of solids, liquids and gases and its applications'
t101 = topic(N101, N101.lower(), 'thermal expansion')
FX(t101, 'C1', (1, 2, 3), [
    ('Which state of matter expands the most for the same temperature rise?', 'Gas', 'Gases expand most, then liquids, then solids.', ['Solid', 'Liquid', 'They all expand equally']),
    ('Why are gaps left between sections of a railway track?', 'To allow the rails to expand in hot weather without buckling', 'Thermal expansion of steel rails.', ['To let rain drain away', 'To make the train quieter', 'To save steel']),
    ('A bimetallic strip bends when heated because', 'the two metals expand by different amounts', 'One metal expands more, so the strip curves with that metal on the outside.', ['both metals contract', 'the metals melt', 'the strip becomes magnetic']),
    ('When a solid is heated, its particles', 'vibrate more and move slightly further apart', 'Expansion: larger vibrations increase the average separation.', ['get bigger', 'stop moving', 'become fewer']),
    ('A liquid-in-glass thermometer works because', 'the liquid expands as its temperature rises', 'The liquid expands more than the glass and rises up the narrow tube.', ['the glass expands more than the liquid', 'the liquid contracts as it warms', 'the liquid evaporates']),
    ('State one application of thermal expansion.', 'Liquid-in-glass thermometer, bimetallic strip thermostat, fitting a metal tyre onto a wheel, loosening a tight metal lid with hot water.', '[1]'),
])
FX(t101, 'C2', (1, 2, 3, 4), [
    ('Explain, in terms of particles, why solids expand when heated.', 'The particles gain energy and vibrate with larger amplitude, so their average separation increases and the solid gets bigger.', 'more vibration [1]; larger separation [1] [2]'),
    ('Explain why a tight metal lid on a glass jar can be loosened by running hot water over it.', 'The metal expands more than the glass for the same temperature rise, so the lid becomes slightly larger and looser.', 'metal expands more than glass [1]; lid looser [1] [2]'),
    ('Explain why gases expand much more than solids for the same temperature rise.', 'In a gas the forces between particles are negligible, so faster particles easily spread out; in solids strong forces hold the particles close together.', 'weak forces in gas [1]; strong forces in solid [1] [2]'),
    ('Describe how a bimetallic strip can be used as a thermostat to switch off a heater.', 'The strip is part of the circuit; as it warms, the metal that expands more makes it bend away from a contact, breaking the circuit; it cools, straightens and reconnects.', 'bends when heated [1]; breaks contact [1]; reconnects on cooling [1] [3]'),
    ('Explain why overhead power cables are hung loosely in summer.', 'In winter they contract; if fitted tight in summer they could snap from the tension when they contract in cold weather.', 'contract when cold [1]; avoid breaking [1] [2]'),
])
EXPN = [('a steel bridge', 12e-6, (100, 500)), ('a copper pipe', 17e-6, (5, 30)), ('an aluminium rail', 23e-6, (10, 50)), ('a concrete motorway section', 12e-6, (20, 100)), ('a steel railway rail', 12e-6, (20, 120))]


@t101.add('C3', (1, 2, 3, 4), 'numerical')
def t101_calc(r, D):
    o, a, (L1, L2) = r.choice(EXPN)
    L = r.choice([L1, (L1 + L2) // 2, L2])
    dT = r.choice([20, 30, 40, 50, 60])
    dL = a * L * dT
    per = a * L * 10
    if D <= 2:
        return numq(r, D, f'{cap(o)} {L} m long increases in length by {g(per * 1000, 3)} mm for every 10 °C rise in temperature.', f'increase in length for a {dT} °C rise', dL * 1000, ' mm', f'{g(per * 1000, 3)} × {dT}/10', [per * 1000, dL * 100, dL * 1000 * 10])
    return Q(f'{cap(o)} {L} m long increases in length by {g(per * 1000, 3)} mm for every 10 °C rise. The temperature ranges from {r.choice([-10, -5, 0, 5])} °C in winter to {dT} °C above that in summer. (a) Calculate the total change in length. (b) Explain why engineers include expansion gaps or joints.',
             f'(a) {g(dL * 1000, 3)} mm (b) without gaps the expanding structure would push against fixed points, causing large forces that could buckle or crack it.',
             f'(a) {g(per * 1000, 3)} × {dT}/10 [1] = {g(dL * 1000, 3)} mm [1] (b) prevents buckling / large forces [1]' + (' [3]' if D == 3 else '; particle explanation of expansion [1] [4]'))


@t101.add('C2', (2, 3, 4), 'explain')
def t101_strip(r, D):
    m1, m2 = r.choice([('brass', 'iron'), ('copper', 'invar'), ('aluminium', 'steel'), ('brass', 'invar')])
    how = r.choice(['heated', 'cooled'])
    return Q(f'A bimetallic strip is made of {m1} (expands more) bonded to {m2} (expands less). It is straight at room temperature. Describe and explain what happens when it is {how}.',
             f'It bends with the {m1 if how == "heated" else m2} on the outside of the curve, because {m1} {"expands more" if how == "heated" else "contracts more"} than {m2}.', 'direction of bending [1]; different expansion explained [1] [2]')


def _exp_c4(r, D):
    parts = [
        lambda r: ('Explain in terms of particles why the liquid expands when heated.', 'Particles move faster and slightly further apart on average.', '[2]'),
        lambda r: ('Explain why the bore (tube) of the thermometer is very narrow.', 'A small expansion of the liquid gives a large rise in the thread, so the thermometer is more sensitive.', '[2]'),
        lambda r: ('Explain why the glass bulb is thin.', 'So thermal energy passes quickly to the liquid; faster response.', '[1]'),
        lambda r: ('Explain why the expansion of the glass does not cancel the expansion of the liquid.', 'Liquids expand much more than solids for the same temperature rise.', '[1]'),
        lambda r: ('Suggest why alcohol is used instead of mercury for measuring very low temperatures.', 'Alcohol has a much lower freezing point (−114 °C) than mercury (−39 °C).', '[1]'),
        lambda r: ('Name one other device that uses thermal expansion.', 'Bimetallic thermostat (or fire alarm, or fitting a tyre).', '[1]'),
    ]
    return compose(r, r.choice(['A liquid-in-glass thermometer contains alcohol in a thin glass bulb.', f'{person(r)} designs a thermometer for a weather station in {city(r)}.']), parts, k=(2, 3, 4), type_='multi_step')


t101.add('C4', (2, 3, 4, 5), 'multi_step')(_exp_c4)

N102 = 'Specific heat capacity: ΔE = mcΔT'
t102 = topic(N102, N102.lower(), 'specific heat capacity')
SHC = [('water', 4200), ('aluminium', 900), ('copper', 390), ('iron', 450), ('olive oil', 2000), ('concrete', 880), ('ethanol', 2400), ('glass', 670), ('lead', 130)]
FX(t102, 'C1', (1, 2), [
    ('Specific heat capacity is the energy needed to', 'raise the temperature of 1 kg of a substance by 1 °C', 'c = ΔE/(mΔT).', ['melt 1 kg of a substance', 'raise the temperature of any mass by 1 °C', 'boil 1 kg of water']),
    ('What is the unit of specific heat capacity?', 'J/(kg °C)', 'Joules per kilogram per degree Celsius.', ['J/kg', 'J/°C', 'W/(kg °C)']),
    ('Which equation links energy, mass, specific heat capacity and temperature change?', 'ΔE = mcΔT', 'Energy = mass × shc × temperature change.', ['ΔE = mc/ΔT', 'ΔE = mΔT/c', 'ΔE = cΔT/m']),
    ('Water has a high specific heat capacity. This means it', 'needs a lot of energy to change its temperature', 'High c → large energy for small ΔT.', ['heats up very quickly', 'boils at a low temperature', 'cannot store energy']),
    ('How much energy is needed to warm 2 kg of water by 10 °C? (c = 4200 J/(kg °C))', '84 000 J', '2 × 4200 × 10 = 84 000 J.', ['8400 J', '42 000 J', '840 J']),
    ('Define specific heat capacity.', 'The energy required per unit mass per unit temperature increase.', 'energy per kg [1]; per °C [1] [2]'),
])
FX(t102, 'C2', (1, 2, 3, 4), [
    ('Describe an experiment to measure the specific heat capacity of an aluminium block.', 'Measure the mass of the block; insert an immersion heater and thermometer; record the start temperature; switch on for a measured time with a joulemeter (or P × t); record the final temperature; c = E/(mΔT). Insulate the block.', 'mass and temperatures measured [1]; energy from joulemeter or Pt [1]; c = E/(mΔT) [1]; insulation [1] [4]'),
    ('Explain why the value of specific heat capacity found in a school experiment is usually higher than the true value.', 'Some of the energy supplied is lost to the surroundings, so the measured temperature rise is smaller than it should be; c = E/(mΔT) comes out too large.', 'energy lost to surroundings [1]; ΔT too small → c too large [1] [2]'),
    ('Explain why coastal cities often have milder climates than inland cities.', 'Water has a high specific heat capacity, so the sea warms and cools slowly, keeping nearby air temperatures more even.', 'high shc of water [1]; slow temperature change moderates climate [1] [2]'),
    ('Explain why water is used in central-heating radiators and car cooling systems.', 'Its high specific heat capacity means each kilogram carries a lot of thermal energy for a given temperature change.', 'high shc [1]; carries much energy per kg [1] [2]'),
])


@t102.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t102_mc(r, D):
    sub, c = r.choice(SHC)
    m = r.choice([0.2, 0.25, 0.5, 0.8, 1.0, 1.5, 2.0, 5.0])
    dT = r.choice([5, 8, 10, 12, 15, 20, 25, 30, 40, 50])
    E = m * c * dT
    fm = lambda x: sci(x, 3) if x >= 1e6 else g(x)
    which = r.choice(['E', 'T', 'c'])
    if D <= 2:
        if which == 'E':
            return numq(r, D, f'A {g(m)} kg mass of {sub} (c = {c} J/(kg °C)) is heated through {dT} °C.', 'energy needed', E, ' J', f'ΔE = mcΔT = {g(m)} × {c} × {dT}', [m * c, c * dT, E / 10], fm=fm)
        if which == 'T':
            return numq(r, D, f'{fm(E)} J of energy is transferred to {g(m)} kg of {sub} (c = {c} J/(kg °C)).', 'temperature rise', dT, ' °C', f'ΔT = E/(mc) = {fm(E)}/({g(m)} × {c})', [E / c, E / m / 1000, dT * 2])
        return numq(r, D, f'{fm(E)} J raises the temperature of {g(m)} kg of a material by {dT} °C.', 'specific heat capacity', c, ' J/(kg °C)', f'c = E/(mΔT) = {fm(E)}/({g(m)} × {dT})', [E / m, E / dT, c * 10])
    if D == 3:
        T1 = r.choice([15, 18, 20, 22, 25])
        mg_ = int(m * 1000)
        return Q(f'{mg_} g of {sub} (c = {c} J/(kg °C)) is heated from {T1} °C to {T1 + dT} °C. Calculate the energy transferred.', f'{fm(E)} J', f'm = {g(m)} kg and ΔT = {dT} °C [1]; ΔE = mcΔT [1] = {fm(E)} J [1] [3]')
    P = r.choice([50, 100, 200, 500, 1000, 2000])
    t = E / P
    mb = r.choice([0.5, 1.0])
    T1 = r.choice([18, 20, 22])
    return Q(f'An immersion heater of power {P} W heats a {g(m)} kg block of {sub}. In {g(t, 3)} s the temperature rises from {T1} °C to {T1 + dT} °C. (a) Calculate the energy supplied. (b) Calculate the specific heat capacity from these results. (c) The accepted value is {c} J/(kg °C); in a repeat with no insulation the temperature rose by only {g(dT * 0.85, 3)} °C. Calculate the value obtained and explain the difference.',
             f'(a) {fm(P * t)} J (b) {c} J/(kg °C) (c) {g(c / 0.85, 3)} J/(kg °C): energy was lost to the surroundings, so ΔT was smaller and c came out too high.',
             f'(a) E = Pt = {fm(P * t)} J [1] (b) c = E/(mΔT) [1] = {c} J/(kg °C) [1] (c) {g(c / 0.85, 3)} J/(kg °C) [1]' + (' [4]' if D == 4 else '; heat loss explanation [1] [5]'), 'multi_step')


@t102.add('C2', (2, 3, 4), 'explain')
def t102_cmp(r, D):
    (a, ca), (b, cb) = r.sample(SHC, 2)
    m = r.choice([0.5, 1.0, 2.0])
    return Q(f'Equal masses ({g(m)} kg) of {a} (c = {ca} J/(kg °C)) and {b} (c = {cb} J/(kg °C)) receive the same amount of energy. Predict which has the larger temperature rise and explain.', f'{cap(a if ca < cb else b)}: smaller c, so ΔT = E/(mc) is larger.',
             'correct substance [1]; ΔT ∝ 1/c reasoning [1] [2]')


def _shc_c4(r, D):
    sub, c = r.choice(SHC[:4] + SHC[5:6])
    m = r.choice([0.5, 1.0, 2.0])
    P = r.choice([50, 100, 200])
    t = r.choice([300, 600, 900])
    dT = P * t / (m * c)
    if dT > 80:
        t = 300
        dT = P * t / (m * c)
    intro = f'In an experiment, a {P} W heater is placed in a {g(m)} kg block of {sub} for {t} s.'
    parts = [
        lambda r: ('Calculate the energy supplied.', f'{P * t} J', 'E = Pt [2]'),
        lambda r: (f'The specific heat capacity of {sub} is {c} J/(kg °C). Calculate the expected temperature rise.', f'{g(dT, 3)} °C', 'ΔT = E/(mc) [2]'),
        lambda r: ('Explain why the measured temperature rise is likely to be less.', 'Energy is lost to the surroundings by conduction, convection and radiation.', '[2]'),
        lambda r: ('Suggest two improvements to the method.', 'Insulate the block; put oil in the thermometer hole for good thermal contact; use a lid.', '[2]'),
        lambda r: ('State why the temperature should be read a short time after switching off.', 'The temperature keeps rising for a while as thermal energy spreads from the heater through the block.', '[1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t102.add('C4', (2, 3, 4, 5), 'case')(_shc_c4)
t102.add('C3', (4, 5), 'case')(_shc_c4)

N103 = 'Melting, boiling and evaporation'
t103 = topic(N103, N103.lower(), 'melting, boiling', 'evaporation')
FX(t103, 'C1', (1, 2), [
    ('During melting, the temperature of a pure substance', 'stays constant', 'Energy is used to break bonds, not to raise temperature.', ['rises steadily', 'falls', 'rises then falls']),
    ('Evaporation differs from boiling because evaporation', 'happens at the surface at any temperature', 'Boiling occurs throughout the liquid at the boiling point.', ['happens throughout the liquid', 'happens only at 100 °C', 'needs bubbles to form']),
    ('Which change increases the rate of evaporation?', 'Blowing air across the surface', 'Moving air removes vapour; also higher temperature and larger surface area.', ['Reducing the surface area', 'Lowering the temperature', 'Covering the liquid']),
    ('What is the melting point of pure ice at standard atmospheric pressure?', '0 °C', 'Ice melts at 0 °C; water boils at 100 °C.', ['100 °C', '−273 °C', '4 °C']),
    ('Evaporation cools a liquid because', 'the most energetic particles escape, lowering the average kinetic energy of those left', 'The remaining particles have lower average KE, so lower temperature.', ['the liquid gains energy', 'the least energetic particles escape', 'the container cools it']),
    ('State two differences between boiling and evaporation.', 'Boiling occurs throughout the liquid, only at the boiling point, with bubbles; evaporation occurs only at the surface, at any temperature.', 'any two [2]'),
])
FX(t103, 'C2', (1, 2, 3, 4), [
    ('Explain why sweating helps to keep you cool.', 'Sweat evaporates from the skin; the most energetic molecules escape, taking energy from the skin, so the skin cools.', 'evaporation [1]; energetic molecules leave, removing energy from skin [1] [2]'),
    ('Explain why washing dries faster on a warm, windy day.', 'Warmer water molecules have more energy so more escape; wind removes the vapour so fewer molecules return to the liquid.', 'temperature effect [1]; wind removes vapour [1] [2]'),
    ('Explain, in terms of particles, why the temperature of boiling water stays at 100 °C even though it is still being heated.', 'The energy supplied is used to overcome the attractive forces between particles so they escape as gas, not to increase their kinetic energy.', 'energy breaks forces/bonds [1]; KE (temperature) unchanged [1] [2]'),
    ('Explain why a cooling curve for stearic acid has a flat section.', 'While it is freezing, energy is released as bonds form between particles, which balances the energy lost to the surroundings, so the temperature stays constant.', 'change of state [1]; energy released balances losses [1] [2]'),
])


@t103.add('C3', (2, 3, 4, 5), 'case')
def t103_curve(r, D):
    sub, mp = r.choice([('stearic acid', 69), ('paraffin wax', 55), ('salol', 43), ('naphthalene', 80), ('lauric acid', 44)])
    start = mp + r.choice([15, 20, 25])
    temps = []
    T = start
    for i in range(10):
        if T > mp + 0.5:
            T = max(mp, T - r.choice([4, 5, 6]))
            temps.append(T)
        elif len([x for x in temps if x == mp]) < 4:
            temps.append(mp)
        else:
            T = T - r.choice([3, 4])
            temps.append(T)
    return Q(f'Liquid {sub} is left to cool and its temperature is recorded every minute: ' + ', '.join(f'{x} °C' for x in [start] + temps) + '. (a) State the melting point. (b) Describe the state(s) of the substance during the flat part. (c) Explain why the temperature stays constant there.',
             f'(a) {mp} °C (b) a mixture of liquid and solid: it is solidifying. (c) energy released as particles bond into a solid balances energy lost to the surroundings.',
             '(a) melting point [1] (b) liquid and solid / freezing [1] (c) energy released on solidifying [1]' + (' [3]' if D < 4 else '; balances heat loss so KE unchanged [1] [4]' if D == 4 else '; balances heat loss so KE unchanged [1]; sketch shape described [1] [5]'))


EVAP = [('a puddle on a road', ['temperature of the air', 'wind speed', 'surface area of the puddle', 'humidity of the air']), ('washing on a line', ['temperature', 'wind', 'spreading the clothes out', 'humidity']),
        ('a cup of hot tea', ['temperature of the tea', 'surface area of the cup opening', 'air movement', 'humidity']), ('sweat on an athlete', ['air temperature', 'wind', 'area of exposed skin', 'humidity'])]


@t103.add('C2', (2, 3, 4), 'explain')
def t103_evap(r, D):
    o, fs = r.choice(EVAP)
    f = r.sample(fs, 2)
    return Q(f'State two factors that affect how quickly {o} evaporates and explain, using particles, how each one changes the rate.', f'{cap(f[0])} and {f[1]}: ' + ('higher temperature gives more particles with enough energy to escape; ' if any('temp' in x for x in f) else '') + 'moving air removes escaped particles; a larger surface area lets more particles escape; humid air means more particles return.',
             'two factors [2]; particle explanation for each [2] [4]' if D >= 4 else 'two factors [1]; explanation [1] [2]')


def _mb_c4(r, D):
    parts = [
        lambda r: ('Explain why the temperature stays at 0 °C while the ice melts.', 'Energy is used to break bonds between particles, not to raise their KE.', '[2]'),
        lambda r: ('Describe what happens to the particles when the water then boils.', 'They gain enough energy to overcome attractive forces completely and escape as a gas throughout the liquid.', '[2]'),
        lambda r: ('State two differences between this boiling and the evaporation of water from a puddle.', 'Boiling at 100 °C throughout the liquid with bubbles; evaporation at any temperature from the surface only.', '[2]'),
        lambda r: ('Explain why water left in a beaker cools as it evaporates.', 'The most energetic particles escape, so the average KE of the remaining particles falls.', '[2]'),
        lambda r: ('State the boiling point of pure water at standard pressure.', '100 °C', '[1]'),
    ]
    return compose(r, r.choice(['Ice cubes at 0 °C are heated in a beaker until the water boils.', f'{person(r)} heats crushed ice and records the temperature every 30 s until it has been boiling for a few minutes.']), parts, k=(2, 3, 4), type_='multi_step')


t103.add('C4', (2, 3, 4, 5), 'multi_step')(_mb_c4)

N104 = 'Specific latent heat of fusion and vaporisation'
t104 = topic(N104, N104.lower(), 'specific latent heat')
LH = [('ice (fusion)', 334000, 'melt'), ('water (vaporisation)', 2260000, 'boil away'), ('lead (fusion)', 23000, 'melt'), ('ethanol (vaporisation)', 850000, 'boil away'), ('aluminium (fusion)', 397000, 'melt'), ('copper (fusion)', 205000, 'melt')]
FX(t104, 'C1', (1, 2), [
    ('Specific latent heat is the energy needed to', 'change the state of 1 kg of a substance without changing its temperature', 'E = lm.', ['raise 1 kg by 1 °C', 'change the state of any mass while heating it', 'melt and boil a substance']),
    ('Which equation is used for latent heat?', 'E = lm', 'Energy = specific latent heat × mass.', ['E = mcΔT', 'E = l/m', 'E = m/l']),
    ('The specific latent heat of vaporisation of water is larger than that of fusion because', 'boiling separates the particles completely, needing more energy than loosening them in melting', 'Vaporisation overcomes nearly all the attractive forces.', ['water is hotter when it boils', 'ice is lighter than water', 'melting needs no energy']),
    ('What is the unit of specific latent heat?', 'J/kg', 'Energy per kilogram.', ['J/(kg °C)', 'J', 'W/kg']),
    ('Define specific latent heat of fusion.', 'The energy needed to change 1 kg of a substance from solid to liquid at its melting point without a change in temperature.', '1 kg solid → liquid [1]; at constant temperature [1] [2]'),
])
FX(t104, 'C2', (1, 2, 3, 4), [
    ('Explain why a burn from steam at 100 °C is more severe than a burn from water at 100 °C.', 'Steam releases its large latent heat of vaporisation as it condenses on the skin, in addition to the energy released as the water then cools.', 'condensation releases latent heat [1]; extra energy to skin [1] [2]'),
    ('Describe an experiment to measure the specific latent heat of fusion of ice.', 'Put crushed ice in a funnel with an immersion heater; collect the meltwater for a measured time with the heater off (control) and on; the extra mass melted by the heater = m; E from joulemeter; l = E/m.', 'heater in ice with joulemeter [1]; control funnel to allow for room melting [1]; mass melted measured [1]; l = E/m [1] [4]'),
    ('Explain why a control funnel (without a heater) is used in the latent heat of fusion experiment.', 'Some ice melts by absorbing energy from the warm room; the control measures this so it can be subtracted from the mass melted in the heated funnel.', 'room melting [1]; subtract to find mass melted by heater [1] [2]'),
])


@t104.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t104_l(r, D):
    sub, l, verb = r.choice(LH)
    m = r.choice([0.02, 0.05, 0.1, 0.2, 0.25, 0.5, 1.5, 2.0])
    E = l * m
    fm = lambda x: sci(x, 3) if x >= 1e5 else g(x)
    name = sub.split(' (')[0]
    kind = sub.split('(')[1].rstrip(')')
    if D <= 2:
        if r.random() < 0.6:
            return numq(r, D, f'The specific latent heat of {kind} of {name} is {sci(l, 3)} J/kg.', f'energy needed to {verb} {g(m)} kg of {name} at its {"melting" if verb == "melt" else "boiling"} point', E, ' J', f'E = lm = {sci(l, 3)} × {g(m)}', [l / m, m / l * 1e10, E * 10], fm=fm)
        return numq(r, D, f'{fm(E)} J is needed to {verb} {g(m)} kg of {name} at constant temperature.', 'specific latent heat', l, ' J/kg', f'l = E/m = {fm(E)}/{g(m)}', [E * m, l / 10, l * 10], fm=fm)
    if D == 3:
        P = r.choice([50, 100, 200, 500, 1000, 2000])
        t = E / P
        return Q(f'A {P} W heater is used to {verb} {g(m * 1000)} g of {name} at its {"melting" if verb == "melt" else "boiling"} point. Calculate the time needed, assuming all the energy goes to the {name}. (specific latent heat = {sci(l, 3)} J/kg)', f'{g(t, 3)} s',
                 f'E = lm = {fm(E)} J [1]; t = E/P [1] = {g(t, 3)} s [1] [3]')
    mi = r.choice([0.1, 0.2, 0.25, 0.5])
    Ti = r.choice([-10, -15, -20, -5])
    E1 = mi * 2100 * (-Ti)
    E2 = mi * 334000
    E3 = mi * 4200 * 20
    tot = E1 + E2 + E3
    return Q(f'{g(mi)} kg of ice at {Ti} °C is turned into water at 20 °C. (c of ice = 2100 J/(kg °C), c of water = 4200 J/(kg °C), l of fusion of ice = 3.34 × 10⁵ J/kg.) (a) Calculate the energy to warm the ice to 0 °C. (b) Calculate the energy to melt it. (c) Calculate the energy to warm the water to 20 °C. (d) Calculate the total energy.',
             f'(a) {g(E1, 3)} J (b) {fm(E2)} J (c) {fm(E3)} J (d) {fm(tot)} J',
             f'(a) mcΔT = {g(E1, 3)} J [1] (b) lm = {fm(E2)} J [1] (c) mcΔT = {fm(E3)} J [1] (d) sum [1]' + (' [4]' if D == 4 else '; identifies melting as the largest stage [1] [5]'), 'multi_step')


@t104.add('C2', (2, 3, 4), 'explain')
def t104_flat(r, D):
    return Q(f'A heating curve for {r.choice(["water", "ethanol", "a pure wax"])} shows two flat sections. Explain why the second flat section (boiling) is {r.choice(["longer", "about seven times longer"])} than the first (melting) when heated at a constant rate.', 'The specific latent heat of vaporisation is much larger than that of fusion: boiling must separate the particles completely, needing much more energy, which takes longer at the same power.',
             'flat sections = changes of state [1]; l_v > l_f [1]; more energy at same power takes longer [1] [3]')


def _lh_c4(r, D):
    m = r.choice([0.1, 0.2, 0.25])
    P = r.choice([100, 200, 400])
    E = 334000 * m
    parts = [
        lambda r: ('Calculate the energy needed to melt the ice.', f'{sci(E, 3)} J', 'E = lm [2]'),
        lambda r: ('Calculate the time the heater takes to supply this energy.', f'{g(E / P, 3)} s', 't = E/P [2]'),
        lambda r: ('Explain why the temperature stays at 0 °C while the ice melts.', 'The energy breaks bonds between particles, not increasing their KE.', '[2]'),
        lambda r: ('The ice actually takes longer to melt. Suggest why.', 'Some energy heats the funnel/beaker and surroundings.', '[1]'),
        lambda r: ('Calculate the energy then needed to warm the meltwater to 30 °C (c = 4200 J/(kg °C)).', f'{g(m * 4200 * 30, 3)} J', 'mcΔT [2]'),
    ]
    return compose(r, f'{g(m * 1000)} g of ice at 0 °C is melted by a {P} W heater (specific latent heat of fusion of ice = 3.34 × 10⁵ J/kg).', parts, k=(2, 3, 4), type_='multi_step')


t104.add('C4', (2, 3, 4, 5), 'multi_step')(_lh_c4)


@t104.add('C2', (2, 3, 4), 'explain')
def t104_cmp(r, D):
    m = r.choice([0.1, 0.2, 0.5, 1.0])
    Ef, Ev = 334000 * m, 2260000 * m
    return Q(f'Calculate the energy needed to melt {g(m)} kg of ice at 0 °C and to boil away {g(m)} kg of water at 100 °C (l_f = 3.34 × 10⁵ J/kg, l_v = 2.26 × 10⁶ J/kg), and explain why the second is so much larger.',
             f'{sci(Ef, 3)} J and {sci(Ev, 3)} J. Boiling separates the particles completely, overcoming almost all the attractive forces, whereas melting only loosens them.',
             f'both energies (E = lm) [1]; boiling must separate particles completely [1]; melting only loosens/rearranges [1] [3]')


relation(t104, 'C2', (2, 3), 'E = lm', 'energy needed to change state', {'mass': 1}, ['Ice at 0 °C is melted in a drinks cooler.', 'Water at 100 °C is boiled away in a kettle.', 'Solid wax at its melting point is melted in a candle factory.'])

CHAPTERS[10] = [t101, t102, t103, t104]

# =========================================================== 11 Thermal energy transfers
COND = [('copper', 'good'), ('aluminium', 'good'), ('iron', 'good'), ('steel', 'good'), ('silver', 'good'), ('brass', 'good'), ('glass', 'poor'), ('wood', 'poor'), ('plastic', 'poor'),
        ('air', 'poor'), ('wool', 'poor'), ('polystyrene foam', 'poor'), ('water', 'poor'), ('rubber', 'poor')]
N111 = 'Conduction: good and bad thermal conductors'
t111 = topic(N111, N111.lower(), 'conduction', 'thermal conductors')
FX(t111, 'C1', (1, 2), [
    ('Which is the best thermal conductor?', 'Copper', 'Metals are good conductors; copper is one of the best.', ['Wood', 'Air', 'Plastic']),
    ('Why are metals good thermal conductors?', 'They have free (delocalised) electrons that carry energy quickly', 'Free electrons transfer energy as well as lattice vibrations.', ['Their atoms are far apart', 'They contain trapped air', 'They are always hot']),
    ('Conduction occurs mainly in', 'solids', 'Particles must be close together to pass on vibrations.', ['gases', 'a vacuum', 'liquids and gases only']),
    ('Why does a woollen jumper keep you warm?', 'It traps air, which is a poor conductor', 'Trapped air reduces conduction (and convection).', ['Wool is a good conductor', 'Wool produces heat', 'Wool reflects all infrared']),
    ('A thermal insulator is a material that', 'is a poor conductor of thermal energy', 'Insulators reduce the rate of thermal energy transfer.', ['conducts thermal energy well', 'conducts electricity well', 'stores no energy']),
    ('State how thermal energy is conducted in a non-metal solid.', 'By atoms/particles vibrating and passing the vibrations on to neighbouring particles (lattice vibrations).', '[1]'),
])
FX(t111, 'C2', (1, 2, 3, 4), [
    ('Explain why metals conduct thermal energy much better than non-metals.', 'In both, vibrating particles pass energy to neighbours, but metals also have free electrons that move quickly through the metal and collide with distant particles, transferring energy much faster.', 'lattice vibrations in both [1]; free electrons in metals [1]; move rapidly, transfer energy further [1] [3]'),
    ('Explain why a metal spoon feels colder than a wooden spoon in the same drawer, although both are at the same temperature.', 'The metal conducts thermal energy away from your hand much faster, so your skin cools more quickly.', 'same temperature [1]; metal conducts energy from hand faster [1] [2]'),
    ('Explain why saucepans are made of metal but have plastic or wooden handles.', 'Metal conducts thermal energy quickly from the cooker to the food; the handle is an insulator so it stays cool enough to hold.', 'metal pan conducts to food [1]; insulating handle [1] [2]'),
    ('Explain why liquids and gases are poor conductors.', 'Their particles are further apart (especially in gases), so vibrations are passed on less effectively, and there are no free electrons.', 'particles far apart [1]; no free electrons [1] [2]'),
])


@t111.add('C1', (1, 2, 3))
def t111_pick(r, D):
    q = r.choice(['good', 'poor'])
    right = r.choice([m for m, k in COND if k == q])
    wrong = [m for m, k in COND if k != q]
    opts, a = mcq(r, right, r.sample(wrong, 3))
    return Q(f'Which of these is a {"good thermal conductor" if q == "good" else "good thermal insulator"}?', a, f'{cap(right)} is a {"metal (free electrons)" if q == "good" else "poor conductor (insulator)"}.', opts=opts)


@t111.add('C3', (2, 3, 4, 5), 'case')
def t111_rods(r, D):
    mets = r.sample(['copper', 'aluminium', 'brass', 'iron', 'steel', 'glass'], 4)
    order = {'copper': 1, 'aluminium': 2, 'brass': 3, 'iron': 4, 'steel': 5, 'glass': 6}
    base = {'copper': 25, 'aluminium': 40, 'brass': 70, 'iron': 110, 'steel': 140, 'glass': 600}
    times = {m: int(base[m] * r.uniform(0.9, 1.1)) for m in mets}
    ranked = sorted(mets, key=lambda m: times[m])
    return Q(f'{person(r)} heats one end of four rods of equal size, each with a ball of wax stuck to the far end with a dab of wax. Times for the wax to melt and the ball to fall: ' + ', '.join(f'{m} {times[m]} s' for m in mets) + '. (a) Rank the rods from best to worst conductor. (b) State two variables that must be controlled. (c) Explain why the best conductor transfers energy fastest.',
             f'(a) {", ".join(ranked)} (b) same length and thickness of rods; same heating (same flame position/temperature); same amount of wax (c) {ranked[0]} is a metal with many free electrons moving quickly to transfer energy.',
             '(a) correct order (shortest time = best) [1] (b) two control variables [2] (c) free electrons [1]' + (' [4]' if D < 5 else '; lattice vibrations also mentioned [1] [5]'))


@t111.add('C2', (2, 3, 4), 'explain')
def t111_why(r, D):
    sc = r.choice([('Double-glazed windows have a layer of air or argon between two panes of glass.', 'Gas is a very poor conductor and the gap is narrow so convection is small, reducing thermal energy loss.'),
                   ('Birds fluff up their feathers on cold days.', 'Fluffed feathers trap more air, a poor conductor, reducing conduction from the body.'),
                   ('Cooks use a metal skewer pushed through a potato to make it bake faster.', 'The metal conducts thermal energy quickly into the centre of the potato.'),
                   ('A tiled floor feels colder to bare feet than a carpet in the same room.', 'Tiles conduct thermal energy away from the feet faster than carpet, which traps air.'),
                   ('Polystyrene cups are used for hot drinks.', 'Polystyrene contains trapped air and is a poor conductor, so the drink stays hot and the cup is comfortable to hold.'),
                   ('Heat sinks on computer chips are made of aluminium with fins.', 'Aluminium conducts energy away from the chip quickly; fins give a large surface area to lose it.')])
    return Q(f'{sc[0]} Explain why.', sc[1], 'identifies conductor/insulator property [1]; applies to context [1] [2]')


def _cond_c4(r, D):
    parts = [
        lambda r: ('Explain why the base of the pan is made of copper.', 'Copper is an excellent conductor (free electrons), so energy reaches the food quickly.', '[2]'),
        lambda r: ('Explain why the handle is made of plastic.', 'Plastic is a poor conductor, so the handle stays cool.', '[1]'),
        lambda r: ('Describe how energy is conducted through the copper base.', 'Vibrating ions pass energy to neighbours and free electrons move through the metal, colliding with ions.', '[2]'),
        lambda r: ('Suggest why the lid reduces the time needed to heat the food.', 'Reduces energy loss by convection and evaporation.', '[1]'),
        lambda r: ('Explain why a thin layer of air under a pan on an uneven hob slows heating.', 'Air is a poor conductor, so less energy is conducted to the pan.', '[2]'),
    ]
    return compose(r, r.choice(['A saucepan has a copper base and a plastic handle.', f'A cook in {city(r)} chooses a pan with a copper base, steel sides and a plastic handle.']), parts, k=(2, 3, 4), type_='multi_step')


t111.add('C4', (2, 3, 4, 5), 'multi_step')(_cond_c4)

N112 = 'Convection and convection currents'
t112 = topic(N112, N112.lower(), 'convection')
FX(t112, 'C1', (1, 2), [
    ('Convection can occur in', 'liquids and gases', 'Convection needs a fluid that can flow.', ['solids only', 'a vacuum', 'solids and liquids only']),
    ('When a fluid is heated, it rises because', 'it expands and becomes less dense', 'Warm fluid is less dense, so it rises; cooler, denser fluid sinks.', ['it becomes denser', 'heat rises by itself', 'its particles get bigger']),
    ('Where should the heating element in a kettle be placed?', 'At the bottom', 'Hot water rises from the bottom, setting up convection currents.', ['At the top', 'Outside the kettle', 'In the lid']),
    ('Why is the freezing compartment placed at the top of a refrigerator?', 'Cold air sinks and sets up a convection current', 'Cooled, denser air sinks, and warmer air rises to be cooled.', ['Warm air sinks', 'Ice must be kept high up', 'Cold air rises']),
    ('Why can convection not happen in a solid?', 'The particles cannot move from place to place', 'Particles in a solid only vibrate about fixed positions.', ['Solids are too hot', 'Solids are not dense', 'Solids have no particles']),
    ('Describe what is meant by a convection current.', 'A circulating flow of fluid in which warmer, less dense fluid rises and cooler, denser fluid sinks.', '[1]'),
])
FX(t112, 'C2', (1, 2, 3, 4), [
    ('Explain how a convection current forms in a room heated by a radiator.', 'Air next to the radiator is heated, expands and becomes less dense, so it rises; cooler, denser air moves in to replace it; the warm air cools near the ceiling and far wall and sinks, forming a circulating current.', 'air heated and expands [1]; less dense rises [1]; cooler air sinks/replaces → circulation [1] [3]'),
    ('Explain why sea breezes blow from the sea towards the land during a sunny day.', 'The land heats up faster than the sea; air above the land is warmed and rises; cooler air from over the sea moves in to replace it.', 'land warms faster [1]; warm air rises over land [1]; cool air from sea replaces it [1] [3]'),
    ('Describe an experiment to show convection currents in water.', 'Drop a crystal of potassium permanganate into a beaker of water near one edge of the base; heat gently below the crystal; the purple colour rises above the heat, moves across the top and sinks at the other side.', 'crystal at side of base [1]; heat below it [1]; describe circulating path [1] [3]'),
    ('Explain why an air-conditioning unit is usually fitted high on a wall.', 'The cool air it produces is denser and sinks, spreading through the room and setting up a convection current.', 'cool air sinks [1]; circulation [1] [2]'),
])
CONV = [('a hot-water tank with the heater at the bottom', 'the bottom', 'water heated at the bottom rises; cooler water sinks to be heated'), ('a room heated by a radiator under the window', 'low down', 'warm air rises and circulates around the room'),
        ('a glider pilot rising over a sunny field', 'the ground', 'air warmed by the ground rises as a thermal'), ('a candle flame in still air', 'the flame', 'hot gases rise above the flame drawing fresh air in at the base'),
        ('a fridge with its freezing coil at the top', 'the top (cooling)', 'cold air sinks and warmer air rises to be cooled'), ('a chimney above a fire', 'the fire', 'hot gases rise up the chimney, drawing in air at the bottom'),
        ('a lake warming in spring sunshine', 'the surface', 'warm water stays at the top because it is less dense, so convection is weak'), ('magma in the Earth’s mantle', 'the core-mantle boundary', 'hot rock rises slowly and cooler rock sinks')]


@t112.add('C2', (1, 2, 3, 4), 'explain')
def t112_sc(r, D):
    o, where, how = r.choice(CONV)
    return Q(f'Describe and explain the convection in {o}.', cap(how) + '. Heated fluid expands and becomes less dense, so it rises; cooler, denser fluid sinks.',
             'heated fluid becomes less dense and rises [1]; cooler fluid sinks [1]; applied to the context [1] [3]' if D >= 3 else 'less dense rises [1]; applied to context [1] [2]')


CONV_DESIGN = [
    ('one electric heater and one air-conditioning unit in {room}', 'Heater low down (near the floor): warmed air expands, becomes less dense and rises, circulating around the room. Air-conditioner high up: cooled air is denser and sinks, spreading through the room.',
     'rises above the heater, across the ceiling, down the far wall, back along the floor'),
    ('the heating element in a new design of electric kettle', 'At the bottom: water heated there expands, becomes less dense and rises, while cooler, denser water sinks to be heated, so all the water is heated by convection.',
     'rises above the element, spreads at the surface, sinks at the sides and returns to the element'),
    ('the cooling unit in a new drinks refrigerator for a shop', 'At the top: air cooled there becomes denser and sinks over the drinks; warmer air rises to the top to be cooled, giving a convection current.',
     'sinks from the cooling unit past the shelves, then rises up the other side back to the unit'),
    ('the immersion heater in a domestic hot-water tank', 'Near the bottom: heated water rises to the top, where the hot tap is connected, and cold water sinks to be heated, so the whole tank warms.',
     'rises from the heater to the top of the tank, then cooler water moves down the sides to the heater'),
    ('the vents in a greenhouse that overheats on sunny days', 'Vents high in the roof let hot, less dense air escape, and vents low down let cooler air in, so a convection current ventilates the greenhouse.',
     'cool air enters low, is warmed, rises and leaves through the roof vents'),
]


@t112.add('C3', (2, 3, 4, 5), 'case')
def t112_design(r, D):
    what, ans, path = r.choice(CONV_DESIGN)
    room = r.choice(['a classroom', 'an office', 'a bedroom', 'a shipping container used as a site office', 'a hotel room'])
    what = what.format(room=room)
    lead = r.choice([f'An engineer in {city(r)} must decide where to put {what}.', f'{person(r)} is designing the position of {what}.', f'A company in {city(r)} asks for advice on the position of {what}.'])
    return Q(f'{lead} Suggest the best position and explain using ideas about density and convection.' + (' Describe the convection current that is set up.' if D >= 4 else ''),
             ans + (f' Current: {path}.' if D >= 4 else ''),
             'sensible position [1]; heated fluid expands/less dense rises or cooled fluid denser sinks [1]; applied to context [1]' + (' [3]' if D < 4 else '; current path [1] [4]' if D == 4 else '; current path [1]; continuous circulation explained [1] [5]'))


def _conv_c4(r, D):
    parts = [
        lambda r: ('Explain why the dye rises above the flame.', 'The water there is heated, expands, becomes less dense and rises.', '[2]'),
        lambda r: ('Describe the path of the dye after it reaches the surface.', 'It spreads across the top, then sinks down the cooler side and returns along the bottom: a convection current.', '[2]'),
        lambda r: ('Explain why this cannot happen in a solid.', 'Particles in a solid cannot flow from place to place.', '[1]'),
        lambda r: ('Predict what would happen if the beaker were heated at the top instead.', 'Hot water would stay at the top (less dense); little convection, so the bottom stays cool.', '[2]'),
        lambda r: ('Name one everyday device that relies on this process.', 'Kettle / hot-water tank / radiator / fridge.', '[1]'),
    ]
    return compose(r, r.choice(['A crystal of purple dye is placed at one side of the bottom of a beaker of water and the beaker is heated gently beneath the crystal.', f'{person(r)} adds a few grains of potassium permanganate to one corner of a tank of water and heats beneath them.']), parts, k=(2, 3, 4), type_='multi_step')


t112.add('C4', (2, 3, 4, 5), 'multi_step')(_conv_c4)

N113 = 'Thermal radiation: infrared, surface colour and texture'
t113 = topic(N113, N113.lower(), 'thermal radiation', 'infrared')
SURF = [('dull (matt) black', 1), ('shiny black', 2), ('dull white', 3), ('shiny white', 4), ('shiny silver', 5)]
FX(t113, 'C1', (1, 2), [
    ('Thermal radiation is mainly', 'infrared electromagnetic radiation', 'All objects emit infrared; hotter objects emit more.', ['ultraviolet radiation', 'sound waves', 'moving particles']),
    ('Which surface is the best emitter of infrared radiation?', 'Dull black', 'Dull black surfaces are the best emitters and absorbers.', ['Shiny silver', 'Shiny white', 'Polished aluminium']),
    ('Which surface is the poorest absorber of infrared radiation?', 'Shiny silver', 'Shiny, light surfaces reflect most infrared.', ['Dull black', 'Matt dark green', 'Rough black']),
    ('Thermal radiation can travel through', 'a vacuum', 'It is an electromagnetic wave and needs no medium.', ['solids only', 'liquids only', 'nothing at all']),
    ('Which change increases the rate at which an object emits radiation?', 'Increasing its surface temperature', 'Rate also increases with surface area.', ['Painting it shiny silver', 'Reducing its surface area', 'Cooling it down']),
    ('State two factors that affect the rate at which an object emits thermal radiation.', 'Surface temperature, surface area, and surface colour/texture.', 'any two [2]'),
])
FX(t113, 'C2', (1, 2, 3, 4), [
    ('Explain why the panels of a solar water heater are painted dull black.', 'Dull black is the best absorber of infrared (and light), so the water in the panels absorbs as much radiation as possible.', 'dull black best absorber [1]; more energy to water [1] [2]'),
    ('Explain why emergency space blankets are shiny.', 'Shiny surfaces are poor emitters of infrared, so the person loses less energy by radiation; they also reflect radiation back to the body.', 'poor emitter [1]; reflects radiation back [1] [2]'),
    ('Describe an experiment using a Leslie cube to compare the emission of radiation from different surfaces.', 'Fill the cube (with different faces: matt black, shiny black, white, silver) with hot water; place an infrared detector the same distance from each face; compare readings; the matt black face gives the highest reading.', 'cube with hot water [1]; detector same distance from each face [1]; compare/result [1] [3]'),
    ('Explain why thermal radiation is the only way the Sun’s energy can reach the Earth.', 'Space is a vacuum, so conduction and convection cannot occur; infrared radiation is an electromagnetic wave that travels through a vacuum.', 'vacuum no particles [1]; radiation needs no medium [1] [2]'),
    ('Explain why a person standing near a campfire feels warmer on the side facing the fire.', 'Infrared radiation from the fire travels in straight lines and is absorbed by the side facing it; the other side is not in the path of the radiation.', 'radiation travels in straight lines [1]; absorbed by facing side [1] [2]'),
])


@t113.add('C3', (2, 3, 4, 5), 'case')
def t113_cans(r, D):
    cans = r.sample(SURF, 3)
    T0 = r.choice([70, 75, 80, 85, 90])
    drops = {1: 18, 2: 14, 3: 11, 4: 8, 5: 6}
    t = r.choice([10, 15, 20])
    res = {c: T0 - round(drops[k] * r.uniform(0.9, 1.1) * t / 15) for c, k in cans}
    best = min(cans, key=lambda x: x[1])[0]
    return Q(f'{person(r)} fills three identical cans, painted {", ".join(c for c, _ in cans)}, with water at {T0} °C and records the temperature after {t} minutes: ' + ', '.join(f'{c} {res[c]} °C' for c, _ in cans) + '. (a) State which surface is the best emitter. (b) Explain how the results show this. (c) State two variables that should be controlled.',
             f'(a) {best} (b) it cooled the most (largest temperature drop in the same time). (c) same volume and starting temperature of water; same can size; same room conditions/no draughts; lids on.',
             '(a) correct surface [1] (b) largest drop in same time [1] (c) two controls [2]' + (' [4]' if D < 5 else '; reason for using lids (reduce evaporation/convection) [1] [5]'))


@t113.add('C2', (2, 3, 4), 'explain')
def t113_app(r, D):
    sc = r.choice([('Houses in hot countries are often painted white.', 'White surfaces are poor absorbers (good reflectors) of radiation, so the houses absorb less energy from the Sun and stay cooler.'),
                   ('The cooling fins on the back of a refrigerator are painted dull black.', 'Dull black surfaces are good emitters, so they radiate energy away quickly; fins give a large surface area.'),
                   ('Fuel storage tanks are painted silver.', 'Shiny silver reflects most radiation from the Sun, keeping the fuel cool and reducing evaporation and risk of fire.'),
                   ('Marathon runners are wrapped in shiny foil blankets after a race.', 'Shiny surfaces are poor emitters and reflect infrared back to the body, reducing energy loss.'),
                   ('Teapots are often shiny metal.', 'Shiny surfaces are poor emitters, so the tea loses energy by radiation more slowly.'),
                   ('Black car seats get much hotter than light-coloured seats in sunshine.', 'Dark surfaces absorb more of the radiation from the Sun.')])
    return Q(f'{sc[0]} Explain why, using ideas about thermal radiation.', sc[1], 'surface property (absorber/emitter/reflector) [1]; applied to context [1] [2]')


def _rad_c4(r, D):
    parts = [
        lambda r: ('Predict which face gives the highest reading on the infrared detector.', 'The matt (dull) black face.', '[1]'),
        lambda r: ('Predict which face gives the lowest reading.', 'The shiny silver face.', '[1]'),
        lambda r: ('Explain why the detector must be the same distance from each face.', 'Intensity decreases with distance; for a fair test only the surface should change.', '[2]'),
        lambda r: ('Explain why the readings fall slowly during the experiment.', 'The water cools, and a cooler surface emits less radiation.', '[2]'),
        lambda r: ('State the type of electromagnetic radiation detected.', 'Infrared.', '[1]'),
        lambda r: ('Suggest how the experiment could show which surface is the best absorber.', 'Place identical cans/plates with different surfaces the same distance from a heater and compare temperature rises.', '[2]'),
    ]
    return compose(r, r.choice(['A Leslie cube has four faces: matt black, shiny black, matt white and shiny silver. It is filled with boiling water.', f'{person(r)} uses a Leslie cube and an infrared detector.']), parts, k=(2, 3, 4), type_='case')


t113.add('C4', (2, 3, 4, 5), 'case')(_rad_c4)

N114 = "Consequences and applications of thermal energy transfer, including Earth's energy balance"
t114 = topic(N114, N114.lower(), "earth's energy balance", 'applications of thermal energy transfer')
FX(t114, 'C1', (1, 2), [
    ('A vacuum flask reduces thermal energy transfer by conduction and convection mainly because of', 'the vacuum between the double walls', 'No particles in the vacuum ⇒ no conduction or convection.', ['the silvered surfaces', 'the plastic case', 'the stopper only']),
    ('The silvered surfaces in a vacuum flask reduce', 'radiation', 'Shiny surfaces are poor emitters and good reflectors.', ['conduction', 'convection', 'evaporation only']),
    ('Loft insulation (fibreglass) reduces energy loss mainly because', 'it traps air, which is a poor conductor, and stops convection', 'Trapped air in fibres reduces conduction and convection.', ['it is shiny', 'it produces heat', 'it is a good conductor']),
    ('The Earth’s temperature stays roughly constant when', 'the rate of energy absorbed from the Sun equals the rate of energy radiated into space', 'Energy balance: in = out.', ['it absorbs no radiation', 'it emits no radiation', 'the Sun stops shining']),
    ('Greenhouse gases such as carbon dioxide', 'absorb infrared radiation emitted by the Earth’s surface', 'They re-emit some back, warming the Earth.', ['absorb all visible light from the Sun', 'reflect all sunlight into space', 'cool the Earth']),
    ('State how cavity wall insulation reduces energy loss from a house.', 'It fills the gap with foam/fibre that traps air, reducing convection currents in the cavity (and conduction).', '[1]'),
])
FX(t114, 'C2', (1, 2, 3, 4), [
    ('Explain how an increase in greenhouse gases leads to global warming.', 'The Earth’s surface emits infrared; greenhouse gases absorb it and re-emit some back towards the Earth; more gases mean less energy escapes, so the Earth must warm until the outgoing rate again equals the incoming rate.', 'surface emits infrared [1]; gases absorb/re-emit [1]; imbalance → temperature rise [1] [3]'),
    ('Explain how each feature of a vacuum flask reduces thermal energy transfer.', 'Vacuum: no conduction or convection; silvered walls: reduce radiation (poor emitter/good reflector); stopper: reduces convection and evaporation; insulating supports: reduce conduction.', 'vacuum [1]; silvering [1]; stopper/supports [1] [3]'),
    ('Explain why a house loses less energy if its walls and loft are insulated, using all three methods of transfer.', 'Insulating materials trap air, which reduces conduction; trapped air cannot circulate, reducing convection; foil backing reflects radiation.', 'conduction [1]; convection [1]; radiation [1] [3]'),
    ('Explain why ice and snow melting in the Arctic can speed up global warming.', 'Ice reflects most sunlight; when it melts, darker sea or land absorbs more radiation, warming the Earth further.', 'ice reflects [1]; darker surface absorbs more [1] [2]'),
])
INS = [('loft insulation', 300, 150), ('cavity wall insulation', 600, 160), ('double glazing', 4500, 120), ('draught excluders', 40, 30), ('hot-water tank jacket', 25, 40), ('floor insulation', 900, 60), ('reflective foil behind radiators', 20, 15)]


@t114.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t114_payback(r, D):
    a, cost, save = r.choice(INS)
    cost = round(cost * r.uniform(0.8, 1.3), -1 if cost > 50 else 0)
    save = round(save * r.uniform(0.8, 1.2))
    cur = r.choice(['$', '€', '£'])
    pb = cost / save
    if D <= 2:
        return numq(r, D, f'Installing {a} costs {cur}{g(cost)} and saves {cur}{save} per year on heating.', 'payback time in years', pb, ' years', f'payback = {g(cost)}/{save}', [save / cost, cost - save, pb * 2])
    b, cost2, save2 = r.choice([x for x in INS if x[0] != a])
    cost2 = round(cost2 * r.uniform(0.8, 1.3), -1 if cost2 > 50 else 0)
    save2 = round(save2 * r.uniform(0.8, 1.2))
    return Q(f'Option A, {a}, costs {cur}{g(cost)} and saves {cur}{save} per year; option B, {b}, costs {cur}{g(cost2)} and saves {cur}{save2} per year. (a) Calculate the payback time of each. (b) State which is more cost-effective in the long term over 20 years, showing your working.' + (' (c) Explain how option A reduces energy transfer.' if D >= 4 else ''),
             f'(a) A {g(pb, 3)} years, B {g(cost2 / save2, 3)} years (b) net saving over 20 years: A {cur}{g(20 * save - cost)}, B {cur}{g(20 * save2 - cost2)}; {"A" if 20 * save - cost > 20 * save2 - cost2 else "B"} saves more.' + (' (c) traps air / reduces conduction and convection or radiation as appropriate.' if D >= 4 else ''),
             '(a) both payback times [2] (b) 20-year net savings [1]' + (' [3]' if D == 3 else '; conclusion [1] (c) mechanism [1] [5]' if D >= 5 else ' (c) mechanism [1] [4]'))


@t114.add('C3', (2, 3, 4), 'case')
def t114_balance(r, D):
    Pin = r.choice([340, 342, 341])
    refl = r.choice([0.29, 0.3, 0.31])
    absb = Pin * (1 - refl)
    out = absb * r.choice([0.99, 0.995, 1.0, 1.005])
    st = 'warming' if out < absb else 'cooling' if out > absb else 'constant'
    return Q(f'On average {Pin} W/m² of solar radiation reaches the top of the Earth’s atmosphere and {int(refl * 100)}% is reflected straight back into space. The Earth emits {g(out, 4)} W/m² of infrared into space. (a) Calculate the power absorbed per square metre. (b) State whether the Earth’s average temperature is rising, falling or steady and explain.',
             f'(a) {g(absb, 4)} W/m² (b) {"rising" if st == "warming" else "falling" if st == "cooling" else "steady"}: absorbed {"more than" if st == "warming" else "less than" if st == "cooling" else "equal to"} emitted.',
             f'(a) {Pin} × {g(1 - refl)} = {g(absb, 4)} W/m² [1] (b) comparison [1]; conclusion [1]' + (' [3]' if D < 4 else '; links imbalance to greenhouse gases [1] [4]'))


@t114.add('C4', (3, 4, 5), 'long')
def t114_eval(r, D):
    q = r.choice([
        (f'A homeowner in {city(r)} can afford only one improvement: loft insulation, double glazing or cavity wall insulation. Evaluate the options using ideas about thermal energy transfer and cost, and recommend one.', 'Loft insulation is cheap with a short payback and reduces large losses through the roof (hot air rises); cavity wall reduces conduction/convection through walls; double glazing is expensive with long payback. A justified choice, usually loft insulation first.',
         'loft insulation reduces conduction/convection through the roof [1]; cheap with short payback [1]; cavity fill traps air, stopping convection in the cavity [1]; double glazing: gas gap reduces conduction but high cost/long payback [1]; cost compared with saving [1]; justified recommendation [1] [6]'),
        ('Discuss how human activities may be changing the Earth’s energy balance and what the consequences could be.', 'Burning fossil fuels and deforestation increase CO₂; more infrared is absorbed and re-emitted to the surface; less energy escapes so the Earth warms until a new balance; consequences: melting ice (less reflection, positive feedback), sea-level rise, extreme weather.',
         'CO₂ from burning fossil fuels/deforestation [1]; Earth’s surface emits infrared [1]; greenhouse gases absorb and re-emit infrared back [1]; less energy escapes so absorbed > emitted and the temperature rises [1]; one consequence [1]; second consequence or feedback [1] [6]'),
        ('Evaluate the design of a vacuum flask for keeping soup hot on a mountain expedition, suggesting improvements.', 'Vacuum stops conduction and convection; silvering reduces radiation; stopper reduces convection and evaporation; weak points are the neck and supports (conduction); improvements: insulated stopper, longer narrow neck, outer insulating case.',
         'vacuum stops conduction and convection [1]; silvering reduces radiation [1]; stopper reduces convection/evaporation [1]; weak point (neck/supports) identified [1]; first improvement [1]; second improvement [1] [6]'),
    ])
    return Q(q[0], q[1], q[2])


t114.add('C4', (2, 3, 4), 'multi_step')(_cond_c4)
t114.add('C4', (2, 3, 4), 'case')(_rad_c4)

CHAPTERS[11] = [t111, t112, t113, t114]

# =========================================================== 12 Sound
N121 = 'Sound produced by vibrations and as a longitudinal wave: compressions and rarefactions'
t121 = topic(N121, N121.lower(), 'longitudinal wave', 'compressions and rarefactions')
FX(t121, 'C1', (1, 2), [
    ('Sound is produced by', 'vibrating objects', 'All sound sources vibrate.', ['magnetic fields', 'light waves', 'objects at rest']),
    ('Sound waves are', 'longitudinal', 'Air particles vibrate parallel to the direction the wave travels.', ['transverse', 'electromagnetic', 'stationary']),
    ('In a sound wave, a region where the air particles are close together is called a', 'compression', 'Rarefactions are regions where particles are spread out.', ['rarefaction', 'crest', 'trough']),
    ('Why can sound not travel through a vacuum?', 'There are no particles to pass on the vibrations', 'Sound is a mechanical wave needing a medium.', ['A vacuum is too cold', 'Sound travels too fast in a vacuum', 'A vacuum absorbs all frequencies']),
    ('In a longitudinal wave the particles vibrate', 'parallel to the direction of energy transfer', 'Longitudinal: same direction as travel.', ['at right angles to the direction of energy transfer', 'in circles', 'not at all']),
    ('State what is meant by a rarefaction.', 'A region of a longitudinal wave where the particles are further apart than normal (lower pressure).', '[1]'),
])
FX(t121, 'C2', (1, 2, 3, 4), [
    ('Describe how a loudspeaker cone produces a sound wave in air.', 'The cone vibrates back and forth; moving forward it pushes air particles together (compression); moving back it leaves a region of spread-out particles (rarefaction); these travel outwards as a longitudinal wave.', 'cone vibrates [1]; compressions and rarefactions formed [1]; travel outward longitudinally [1] [3]'),
    ('Describe the bell-jar experiment and explain what it shows.', 'An electric bell rings inside a glass jar; as air is pumped out the sound becomes fainter although the hammer is still seen vibrating; this shows sound needs a medium and cannot travel through a vacuum.', 'air pumped out, sound fades [1]; bell still seen moving [1]; sound needs a medium [1] [3]'),
    ('Explain the difference between the motion of the air particles and the motion of the sound wave.', 'Each particle only oscillates back and forth about a fixed position; the wave (pattern of compressions and rarefactions, and energy) travels through the air.', 'particles oscillate about fixed positions [1]; energy/wave pattern moves [1] [2]'),
    ('Explain why astronauts on a spacewalk must use radios to talk to each other.', 'Space is a vacuum with no particles to carry sound; radio waves are electromagnetic and need no medium.', 'no medium for sound [1]; radio EM waves travel through vacuum [1] [2]'),
])


@t121.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t121_cd(r, D):
    src = r.choice(['a loudspeaker', 'a tuning fork', 'a vibrating guitar string (sound in air)', 'a siren', 'a slinky spring pushed back and forth'])
    n = r.choice([3, 4, 5, 6, 8])
    lam = r.choice([0.2, 0.25, 0.4, 0.5, 0.68, 0.8, 1.0, 1.36])
    d = lam * (n - 1)
    if D <= 2:
        return numq(r, D, f'A diagram of the sound wave from {src} shows {n} compressions spread over a distance of {g(d, 3)} m (from the first to the last compression).', 'wavelength', lam, ' m', f'λ = {g(d, 3)}/{n - 1}', [d / n, d, lam * 2])
    f = r.choice([250, 340, 425, 500, 680, 850])
    T = 1 / f
    if D == 3:
        return Q(f'{cap(src)} vibrates at {f} Hz. Calculate the time for one complete vibration and state how many compressions it produces in 2.0 s.', f'{sci(T, 3) if T < 0.001 else g(T, 3)} s; {2 * f} compressions',
                 f'T = 1/f [1] = {g(T, 3)} s [1]; {f} per second × 2 = {2 * f} [1] [3]')
    v = 340
    lam2 = v / f
    return Q(f'{cap(src)} vibrates at {f} Hz and the sound travels at 340 m/s in air. (a) Calculate the period. (b) Calculate the distance between neighbouring compressions. (c) Describe how an air particle moves as the wave passes.',
             f'(a) {g(T, 3)} s (b) {g(lam2, 3)} m (c) it oscillates back and forth about a fixed position, parallel to the direction of the wave.',
             f'(a) 1/{f} [1] (b) distance travelled in one period = 340 × {g(T, 3)} [1] = {g(lam2, 3)} m [1] (c) oscillates parallel, about fixed point [1]' + (' [4]' if D == 4 else '; no net movement of air [1] [5]'), 'multi_step')


def _snd_c4(r, D):
    f = r.choice([256, 320, 440, 512])
    parts = [
        lambda r: ('Describe how the tuning fork produces sound.', 'Its prongs vibrate, pushing and pulling the air to form compressions and rarefactions.', '[2]'),
        lambda r: ('State whether sound is a transverse or longitudinal wave and explain.', 'Longitudinal: air particles vibrate parallel to the direction of travel.', '[2]'),
        lambda r: ('Calculate the period of the vibration.', f'{g(1 / f, 3)} s', 'T = 1/f [1]'),
        lambda r: ('Explain why the sound cannot be heard if the fork is in a vacuum.', 'No particles to transmit the vibrations.', '[1]'),
        lambda r: ('Explain why the fork can be heard better if its base is pressed against a table.', 'The table is made to vibrate too; its large surface moves more air.', '[2]'),
    ]
    return compose(r, f'A tuning fork marked {f} Hz is struck in a laboratory in {city(r)}.', parts, k=(2, 3, 4), type_='multi_step')


t121.add('C4', (2, 3, 4, 5), 'multi_step')(_snd_c4)

N122 = 'Speed of sound in air and its measurement'
t122 = topic(N122, N122.lower(), 'speed of sound')
FX(t122, 'C1', (1, 2), [
    ('What is the approximate speed of sound in air?', '330–350 m/s', 'About 340 m/s at room temperature.', ['3.0 × 10⁸ m/s', '1500 m/s', '30 m/s']),
    ('In which material does sound travel fastest?', 'Steel', 'Sound is fastest in solids, slower in liquids, slowest in gases.', ['Air', 'Water', 'A vacuum']),
    ('During a thunderstorm you see lightning before you hear thunder because', 'light travels much faster than sound', 'Light 3 × 10⁸ m/s; sound ≈ 340 m/s.', ['the thunder is made later', 'sound travels faster than light', 'your ears are slower than your eyes']),
    ('The approximate speed of sound in water is', '1500 m/s', 'About 1500 m/s.', ['340 m/s', '15 m/s', '3.0 × 10⁸ m/s']),
    ('Describe one direct method of measuring the speed of sound in air.', 'Measure a large distance (e.g. 200 m); one person makes a sound with a visible action (clappers/starting pistol); another times from seeing to hearing it; v = d/t.', 'distance measured [1]; time from seeing to hearing; v = d/t [1] [2]'),
])
FX(t122, 'C2', (1, 2, 3, 4), [
    ('Explain why sound travels faster in solids than in gases.', 'The particles in solids are much closer together and strongly linked, so vibrations are passed on more quickly.', 'particles close/strongly bonded [1]; vibrations passed on faster [1] [2]'),
    ('Explain why the distance between the two people should be large when measuring the speed of sound by the flash-and-bang method.', 'Over a short distance the time is very small, so reaction time is a large fraction of it; a large distance gives a longer time and a smaller percentage error.', 'longer time [1]; reaction time smaller fraction [1] [2]'),
    ('Describe how to measure the speed of sound using two microphones and a fast timer.', 'Place two microphones a measured distance apart in line with a sound source; the first starts the timer and the second stops it as the sound passes; v = distance/time.', 'two microphones a measured distance apart [1]; timer started/stopped by each [1]; v = d/t [1] [3]'),
])
SPEED_SC = [('Two students stand {d} m apart on a sports field in {c}. One bangs two blocks together; the other starts a stopwatch on seeing the blocks hit and stops it on hearing the sound.', (150, 500)),
            ('A starting pistol is fired {d} m from a timekeeper who sees the smoke and hears the bang {t} s later.', (100, 400)),
            ('{p} stands {d} m from a large wall and claps. The echo is heard {t} s later.', 'echo'),
            ('During a storm, {p} counts {t} s between a lightning flash and the thunder.', 'storm')]


@t122.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t122_v(r, D):
    v = r.choice([330, 335, 340, 343, 345, 350])
    fr, rng = r.choice(SPEED_SC)
    p_, c_ = person(r), city(r)
    if rng == 'echo':
        d = r.choice([50, 80, 100, 120, 150, 170])
        t = 2 * d / v
        s = fr.format(p=p_, d=d, t=g(t, 3))
        if D <= 2:
            return numq(r, D, s, 'speed of sound', v, ' m/s', f'v = 2d/t = {2 * d}/{g(t, 3)}', [d / t, v / 2, v * 2], fm=lambda x: g(x, 3))
        return Q(s + ' Calculate the speed of sound and explain why the distance is doubled in your calculation.', f'{g(2 * d / float(g(t, 3)), 3)} m/s; the sound travels to the wall and back.', f'total distance = 2 × {d} = {2 * d} m [1]; v = {2 * d}/{g(t, 3)} [1] = {g(2 * d / float(g(t, 3)), 3)} m/s [1] [3]')
    if rng == 'storm':
        t = r.choice([2, 3, 4.5, 5, 6, 8, 10])
        d = v * t
        s = fr.format(p=p_, t=g(t))
        if D <= 2:
            return numq(r, D, s + f' Sound travels at {v} m/s.', 'distance to the lightning', d, ' m', f'd = vt = {v} × {g(t)}', [d / 2, v / t, d * 2])
        return Q(s + f' Sound travels at {v} m/s. Calculate the distance to the storm in km and explain why the time for the light can be ignored.', f'{g(d / 1000, 3)} km; light travels so fast (3 × 10⁸ m/s) that it arrives almost instantly.',
                 f'd = vt [1] = {g(d / 1000, 3)} km [1]; light time negligible [1] [3]')
    d = r.choice([r for r in range(rng[0], rng[1] + 1, 50)])
    t = round(d / v, 2)
    s = fr.format(c=c_, d=d, t=g(t))
    vm = d / t
    if D <= 2:
        return numq(r, D, s + (f' The time recorded is {g(t)} s.' if '{t}' not in fr else ''), 'speed of sound', vm, ' m/s', f'v = d/t = {d}/{g(t)}', [t / d * 1e5, d * t, vm / 2])
    times = [round(t + r.uniform(-0.08, 0.08), 2) for _ in range(4)]
    mt = sum(times) / 4
    return Q(f'{s.split(". One")[0] if ". One" in s else s} The times recorded are {", ".join(g(x) for x in times)} s. (a) Calculate the mean time. (b) Calculate the speed of sound. (c) Suggest why the readings vary and how the method could be improved.',
             f'(a) {g(mt, 3)} s (b) {g(d / mt, 3)} m/s (c) reaction time varies; use a larger distance, more repeats, or electronic timing with microphones.',
             f'(a) mean [1] (b) v = {d}/{g(mt, 3)} [1] = {g(d / mt, 3)} m/s [1] (c) reaction time / improvement [1]' + (' [4]' if D == 4 else '; second improvement [1] [5]'), 'multi_step')


@t122.add('C2', (2, 3, 4), 'explain')
def t122_media(r, D):
    a, b = r.sample([('steel', 5000), ('water', 1500), ('air', 340), ('wood', 4000), ('glass', 4500)], 2)
    return Q(f'Sound travels at about {a[1]} m/s in {a[0]} and {b[1]} m/s in {b[0]}. Explain this difference in terms of particles, and state in which material a sound would take less time to travel 1 km.', f'{cap(a[0] if a[1] > b[1] else b[0])}: particles are closer together / more strongly linked, so vibrations pass on faster; it takes {g(1000 / max(a[1], b[1]), 3)} s compared with {g(1000 / min(a[1], b[1]), 3)} s.',
             'particle explanation [1]; correct material [1]; times [1] [3]')


def _sp_c4(r, D):
    d = r.choice([100, 150, 200])
    v = 340
    parts = [
        lambda r: ('Describe how to carry out the experiment.', f'Measure {d} m with a tape; stand {d / 2:g} m from the wall and clap; clap in rhythm with the echo, timing 20 claps.', '[2]'),
        lambda r: (f'The sound travels {d} m to the wall and back in {g(d / v, 3)} s. Calculate the speed of sound.', f'{g(d / float(g(d / v, 3)), 3)} m/s', 'v = d/t [2]'),
        lambda r: ('Explain why timing many echoes gives a more accurate result.', 'Reaction-time error is shared over many intervals.', '[2]'),
        lambda r: ('State why the wall should be large and flat.', 'To give a clear, strong echo.', '[1]'),
        lambda r: ('Suggest why the value might differ on a cold day.', 'The speed of sound in air depends on temperature (slower in colder air).', '[1]'),
    ]
    return compose(r, f'{person(r)} uses echoes from a school wall to measure the speed of sound.', parts, k=(2, 3, 4), type_='case')


t122.add('C4', (2, 3, 4, 5), 'case')(_sp_c4)

N123 = 'Pitch, loudness, frequency, amplitude and the range of human hearing'
t123 = topic(N123, N123.lower(), 'pitch', 'loudness', 'range of human hearing')
FX(t123, 'C1', (1, 2), [
    ('The pitch of a sound depends on its', 'frequency', 'Higher frequency → higher pitch.', ['amplitude', 'speed', 'wavelength in a vacuum']),
    ('The loudness of a sound depends on its', 'amplitude', 'Larger amplitude → louder.', ['frequency', 'speed', 'period only']),
    ('What is the approximate range of human hearing?', '20 Hz to 20 000 Hz', 'Audible range 20 Hz–20 kHz.', ['2 Hz to 2000 Hz', '200 Hz to 200 000 Hz', '20 kHz to 20 MHz']),
    ('On an oscilloscope trace, a louder sound of the same pitch shows', 'taller waves with the same spacing', 'Amplitude increases; frequency unchanged.', ['more waves on the screen', 'fewer waves on the screen', 'a flat line']),
    ('Frequency is the number of', 'vibrations per second', 'Measured in hertz (Hz).', ['metres per second', 'seconds per vibration', 'decibels']),
    ('State what happens to the pitch of a note if its frequency is doubled.', 'The pitch becomes higher (one octave higher).', '[1]'),
])
FX(t123, 'C2', (1, 2, 3, 4), [
    ('Two oscilloscope traces show sounds A and B. A has twice as many waves on the screen as B, with the same height. Compare the sounds.', 'A has double the frequency so a higher pitch; same amplitude so the same loudness.', 'A higher pitch/frequency [1]; same loudness [1] [2]'),
    ('Explain why a dog can hear a dog whistle but its owner cannot.', 'The whistle’s frequency is above 20 kHz, beyond the upper limit of human hearing, but within a dog’s range.', 'above 20 kHz [1]; within dog’s range [1] [2]'),
    ('Explain why older people often cannot hear very high-pitched sounds.', 'The upper limit of hearing falls with age (and exposure to loud noise), so high frequencies are no longer detected.', 'upper limit decreases with age [1]; high frequencies not detected [1] [2]'),
    ('A guitar string is plucked harder. Explain how the sound changes and how it stays the same.', 'Larger amplitude of vibration so louder; frequency (pitch) depends on the string’s length and tension, so it stays the same.', 'louder, larger amplitude [1]; same pitch [1] [2]'),
])


@t123.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t123_cro(r, D):
    tb = r.choice([0.5, 1, 2, 5, 10])  # ms/div
    div = r.choice([2, 2.5, 4, 5, 8])
    T = tb * div / 1000
    f = 1 / T
    s = f'An oscilloscope is set to {g(tb)} ms per division. One complete wave of a sound occupies {g(div)} divisions horizontally.'
    if D <= 2:
        return numq(r, D, s, 'frequency of the sound', f, ' Hz', f'T = {g(tb)} × {g(div)} = {g(tb * div)} ms; f = 1/T', [T * 1000, f / 10, f * 2])
    if D == 3:
        aud = 20 <= f <= 20000
        return Q(s + ' Calculate the frequency and state whether a person with normal hearing could hear it.', f'{g(f, 3)} Hz; {"yes" if aud else "no"}, it is {"within" if aud else "outside"} 20 Hz–20 kHz.',
                 f'T = {g(T * 1000)} ms = {g(T)} s [1]; f = 1/T = {g(f, 3)} Hz [1]; audibility [1] [3]')
    v = 340
    return Q(s + f' The amplitude is 3 divisions. (a) Calculate the frequency. (b) Calculate the wavelength in air (speed of sound 340 m/s). (c) Describe how the trace would change if the sound were louder and an octave higher.',
             f'(a) {g(f, 3)} Hz (b) {g(v / f, 3)} m (c) taller waves (larger amplitude) and twice as many waves across the screen (half the spacing).',
             f'(a) {g(f, 3)} Hz [1] (b) λ = v/f [1] = {g(v / f, 3)} m [1] (c) taller and more waves [1]' + (' [4]' if D == 4 else '; spacing halved because f doubled [1] [5]'), 'multi_step')


@t123.add('C1', (1, 2, 3))
def t123_aud(r, D):
    fs = r.sample([5, 12, 50, 256, 1000, 8000, 15000, 25000, 40000, 2e6], 4)
    good = [x for x in fs if 20 <= x <= 20000]
    bad = [x for x in fs if not 20 <= x <= 20000]
    if not good or len(bad) < 1:
        return None
    if len(good) == 1:
        ans = good[0]
        opts, a = mcq(r, f'{g(ans)} Hz', [f'{g(x)} Hz' for x in fs if x != ans])
        return Q('Which of these frequencies can be heard by a person with normal hearing?', a, 'Audible range 20 Hz – 20 kHz.', opts=opts)
    if len(bad) == 1:
        ans = bad[0]
        opts, a = mcq(r, f'{g(ans)} Hz', [f'{g(x)} Hz' for x in fs if x != ans])
        return Q('Which of these frequencies CANNOT be heard by a person with normal hearing?', a, 'Outside 20 Hz – 20 kHz: ' + ('infrasound' if ans < 20 else 'ultrasound') + '.', opts=opts)
    return None


relation(t123, 'C2', (2, 3), 'f = 1/T', 'frequency', {'time period': -1}, ['A signal generator drives a loudspeaker.', 'A musician tunes a string.', 'A student studies oscilloscope traces of sounds.'])


def _pitch_c4(r, D):
    tb = r.choice([1, 2, 5])
    div = r.choice([2, 4, 5])
    T = tb * div / 1000
    parts = [
        lambda r: ('Calculate the period.', f'{g(T)} s', '[1]'),
        lambda r: ('Calculate the frequency.', f'{g(1 / T, 3)} Hz', '[2]'),
        lambda r: ('State whether the sound is audible to humans, giving a reason.', 'Yes' if 20 <= 1 / T <= 20000 else 'No', '[1]'),
        lambda r: ('Describe the trace for a quieter sound of the same pitch.', 'Same spacing, smaller height.', '[2]'),
        lambda r: ('Describe the trace for a higher-pitched sound of the same loudness.', 'Same height, waves closer together.', '[2]'),
    ]
    return compose(r, f'A microphone connected to an oscilloscope shows one full wave every {div} divisions at {tb} ms per division.', parts, k=(2, 3, 4), type_='multi_step')


t123.add('C4', (2, 3, 4, 5), 'multi_step')(_pitch_c4)

N124 = 'Echoes and ultrasound and their uses'
t124 = topic(N124, N124.lower(), 'echoes', 'ultrasound')
FX(t124, 'C1', (1, 2, 3), [
    ('Ultrasound is sound with a frequency', 'above 20 kHz', 'Above the upper limit of human hearing.', ['below 20 Hz', 'between 20 Hz and 20 kHz', 'equal to 20 kHz']),
    ('An echo is', 'a reflected sound wave', 'Sound reflects off hard surfaces.', ['a refracted light wave', 'a sound that has been amplified', 'a sound absorbed by a wall']),
    ('Which is a use of ultrasound?', 'Scanning an unborn baby', 'Prenatal scanning, sonar, cleaning, detecting cracks in metal.', ['Taking X-ray images of bones', 'Cooking food', 'Sterilising surgical instruments by heating']),
    ('In sonar, the depth of the sea is calculated using', 'depth = speed × time ÷ 2', 'The pulse travels down and back.', ['depth = speed × time', 'depth = speed ÷ time', 'depth = time ÷ speed']),
    ('Why is ultrasound used for scanning unborn babies rather than X-rays?', 'Ultrasound is not ionising and is considered safe for the baby', 'X-rays can damage cells.', ['Ultrasound is cheaper than light', 'X-rays cannot pass through skin', 'Ultrasound travels faster than X-rays']),
    ('State two uses of ultrasound.', 'Any two: prenatal scanning, sonar/echo sounding, detecting cracks in metal, cleaning delicate items.', '[2]'),
])
FX(t124, 'C2', (1, 2, 3, 4), [
    ('Explain how ultrasound is used to detect a crack inside a metal casting.', 'Ultrasound pulses are sent into the metal; some are reflected from the crack and return earlier than those reflected from the far side; the time delay shows the crack’s depth.', 'pulses sent in [1]; reflection from crack returns early [1]; time gives depth [1] [3]'),
    ('Explain why soft furnishings reduce echoes in a hall.', 'Soft, porous materials absorb sound energy instead of reflecting it, so less sound is reflected back.', 'absorb rather than reflect [1]; weaker echoes [1] [2]'),
    ('Explain why a ship’s sonar uses ultrasound rather than audible sound.', 'Ultrasound has a short wavelength, so it forms a narrow beam and gives detailed reflections; it is also not heard by people.', 'narrow beam / detail [1]; inaudible [1] [2]'),
])


@t124.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t124_sonar(r, D):
    kind = r.choice(['sonar', 'scan', 'crack', 'bat'])
    if kind == 'sonar':
        v = 1500
        t = r.choice([0.08, 0.1, 0.12, 0.2, 0.3, 0.4, 0.6, 1.2, 2.0])
        d = v * t / 2
        s = f'A ship’s sonar sends an ultrasound pulse to the sea bed; the echo returns after {g(t)} s. The speed of sound in sea water is {v} m/s.'
        unit, what = 'm', 'depth of the sea'
    elif kind == 'scan':
        v = 1540
        t = r.choice([2.6e-5, 3.9e-5, 5.2e-5, 6.5e-5, 1.3e-4])
        d = v * t / 2 * 100
        s = f'In a medical scan, an ultrasound pulse travels into the body at 1540 m/s and is reflected from an organ boundary, returning after {sci(t, 2)} s.'
        unit, what = 'cm', 'depth of the boundary below the skin'
    elif kind == 'crack':
        v = 5000
        t = r.choice([4e-5, 6e-5, 8e-5, 1e-4, 1.2e-4])
        d = v * t / 2 * 100
        s = f'An ultrasound pulse travels into a steel girder at 5000 m/s; an echo from a crack returns after {sci(t, 2)} s.'
        unit, what = 'cm', 'depth of the crack'
    else:
        v = 340
        t = r.choice([0.01, 0.02, 0.03, 0.05, 0.06])
        d = v * t / 2
        s = f'A bat emits an ultrasound pulse and hears the echo from a moth {g(t)} s later. The speed of sound in air is 340 m/s.'
        unit, what = 'm', 'distance to the moth'
    if D <= 2:
        return numq(r, D, s, what, d, ' ' + unit, f'd = vt/2 = {v} × {g(t) if t > 0.001 else sci(t, 2)} ÷ 2', [d * 2, d / 2, v / t])
    if D == 3:
        return Q(s + f' Calculate the {what} and explain why you divide by 2.', f'{g(d, 3)} {unit}; the pulse travels there and back.', f'distance travelled = vt [1]; ÷ 2 for the return journey [1] = {g(d, 3)} {unit} [1] [3]')
    d2 = d * r.choice([0.5, 1.5, 2])
    t2 = 2 * d2 / v / (100 if unit == 'cm' else 1)
    return Q(s + f' (a) Calculate the {what}. (b) A second echo comes from a point {g(d2, 3)} {unit} deep. Calculate when this echo returns. (c) Explain why ultrasound rather than audible sound is used.',
             f'(a) {g(d, 3)} {unit} (b) {sci(t2, 3) if t2 < 0.001 else g(t2, 3)} s (c) shorter wavelength gives a narrower beam and more detail; inaudible; safe (non-ionising).',
             f'(a) vt/2 = {g(d, 3)} {unit} [1] (b) t = 2d/v [1] = {sci(t2, 3) if t2 < 0.001 else g(t2, 3)} s [1] (c) reason [1]' + (' [4]' if D == 4 else '; unit conversion shown [1] [5]'), 'multi_step')


def _us_c4(r, D):
    t = r.choice([0.4, 0.6, 0.8, 1.0])
    parts = [
        lambda r: ('State what is meant by ultrasound.', 'Sound with frequency above 20 kHz.', '[1]'),
        lambda r: (f'The echo returns after {t} s (speed in water 1500 m/s). Calculate the depth.', f'{g(1500 * t / 2)} m', 'vt/2 [2]'),
        lambda r: ('A shoal of fish passes under the boat. Describe what the operator sees on the display.', 'An extra echo arriving earlier than the sea-bed echo.', '[2]'),
        lambda r: ('Explain why a pulse, rather than a continuous wave, is used.', 'So that the time for each reflection can be measured.', '[1]'),
        lambda r: ('Give one other use of ultrasound.', 'Prenatal scanning / crack detection / cleaning.', '[1]'),
    ]
    return compose(r, f'A fishing boat near {coast(r)} uses sonar.', parts, k=(2, 3, 4), type_='multi_step')


t124.add('C4', (2, 3, 4, 5), 'multi_step')(_us_c4)

CHAPTERS[12] = [t121, t122, t123, t124]

# =========================================================== 13 Light
N131 = 'Reflection of light: law of reflection and plane mirror images'
t131 = topic(N131, N131.lower(), 'law of reflection', 'plane mirror')
FX(t131, 'C1', (1, 2), [
    ('The law of reflection states that', 'the angle of incidence equals the angle of reflection', 'Both measured from the normal.', ['the angle of incidence is twice the angle of reflection', 'light always reflects at 90°', 'the angle of reflection is always 45°']),
    ('Angles of incidence and reflection are measured from', 'the normal', 'The normal is perpendicular to the surface at the point of incidence.', ['the mirror surface', 'the horizontal', 'the light source']),
    ('The image in a plane mirror is', 'virtual, upright and the same size as the object', 'Also laterally inverted and as far behind the mirror as the object is in front.', ['real, inverted and smaller', 'real, upright and larger', 'virtual, inverted and smaller']),
    ('A person stands 2 m in front of a plane mirror. How far is the person from their image?', '4 m', 'Image is 2 m behind the mirror: 2 + 2 = 4 m.', ['2 m', '1 m', '8 m']),
    ('A ray strikes a mirror at 30° to the mirror surface. What is the angle of reflection?', '60°', 'Angle of incidence = 90 − 30 = 60°, so reflection = 60°.', ['30°', '120°', '90°']),
    ('State what is meant by a virtual image.', 'An image that cannot be formed on a screen; the light rays only appear to come from it.', '[1]'),
])
FX(t131, 'C2', (1, 2, 3, 4), [
    ('Explain why the image in a plane mirror is described as virtual.', 'The reflected rays do not actually pass through the image position; they only appear to come from a point behind the mirror, so it cannot be put on a screen.', 'rays appear to come from behind mirror [1]; cannot be shown on screen [1] [2]'),
    ('Explain why "AMBULANCE" is written in reverse on the front of ambulances.', 'Drivers see it in their rear-view mirrors, which laterally invert the image, so it reads correctly.', 'lateral inversion [1]; reads correctly in mirror [1] [2]'),
    ('Describe how to verify the law of reflection using a ray box and a plane mirror.', 'Draw a normal on paper at the mirror; direct rays at different angles of incidence; mark incident and reflected rays; measure both angles from the normal with a protractor and compare.', 'normal drawn [1]; several angles measured with protractor [1]; compare i and r [1] [3]'),
    ('Describe how to locate the image of a pin in a plane mirror using ray tracing.', 'Place a pin in front of the mirror; view it from two positions and line up sighting pins with the image each time; draw the lines back behind the mirror; they cross at the image position.', 'sighting from two positions [1]; lines extended behind mirror [1]; intersection is image [1] [3]'),
])


@t131.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t131_ang(r, D):
    a = r.choice([15, 20, 25, 35, 40, 50, 55, 65, 70])
    if D <= 2:
        k = r.random()
        if D == 1:
            if k < 0.5:
                opts, ans = mcq(r, f'{a}°', [f'{90 - a}°', f'{2 * a}°', f'{180 - a}°'])
                return Q(f'A ray of light strikes a plane mirror with an angle of incidence of {a}°. What is the angle of reflection?', ans, f'i = r = {a}°.', opts=opts)
            opts, ans = mcq(r, f'{2 * a}°', [f'{a}°', f'{90 - a}°', f'{180 - 2 * a}°'])
            return Q(f'A ray strikes a plane mirror with an angle of incidence of {a}°. What is the angle between the incident and reflected rays?', ans, f'i + r = {a} + {a} = {2 * a}°.', opts=opts)
        if k < 0.5:
            return Q(f'A ray of light makes an angle of {90 - a}° with the surface of a plane mirror. State the angle of incidence and the angle of reflection.', f'Both {a}°', f'i = 90 − {90 - a} = {a}° [1]; r = i = {a}° [1] [2]')
        return Q(f'A ray strikes a plane mirror with an angle of incidence of {a}°. Calculate the angle between the incident ray and the reflected ray.', f'{2 * a}°', f'r = i = {a}° [1]; i + r = {2 * a}° [1] [2]')
    if D == 3:
        d = r.choice([1.0, 1.5, 2.0, 2.5, 3.0])
        w = r.choice([0.5, 0.8, 1.0])
        return Q(f'{person(r)} stands {g(d)} m in front of a plane mirror and then walks {g(w)} m towards it. Calculate the distance between them and their image before and after, and describe two other properties of the image.',
                 f'Before {g(2 * d)} m; after {g(2 * (d - w))} m. The image is virtual, upright, same size, laterally inverted.', f'image distance = object distance [1]; {g(2 * d)} m and {g(2 * (d - w))} m [1]; two properties [1] [3]')
    th = r.choice([60, 70, 80, 100, 110, 120])
    i1 = r.choice([20, 30, 40])
    g1 = 90 - i1  # glancing angle at first mirror
    g2 = 180 - th - g1  # glancing angle at second mirror (triangle)
    if g2 <= 0 or g2 >= 90:
        return None
    i2 = 90 - g2
    return Q(f'Two plane mirrors are placed with an angle of {th}° between their reflecting surfaces. A ray strikes the first mirror with an angle of incidence of {i1}° and then reflects onto the second mirror. (a) State the angle of reflection at the first mirror. (b) Calculate the angle of incidence at the second mirror. (c) State the law you used.',
             f'(a) {i1}° (b) {i2}° (c) angle of incidence = angle of reflection (from the normal).',
             f'(a) {i1}° [1] (b) ray makes {g1}° with mirror 1; triangle gives {g2}° with mirror 2 [1]; i₂ = 90 − {g2} = {i2}° [1] (c) law of reflection [1]' + (' [4]' if D == 4 else '; geometry clearly shown with angle sum of triangle [1] [5]'), 'multi_step')


def _refl_c4(r, D):
    d = r.choice([1.5, 2.0, 3.0])
    parts = [
        lambda r: ('State the distance from the person to the image.', f'{g(2 * d)} m', '[1]'),
        lambda r: ('Describe three properties of the image.', 'Virtual, upright, same size (laterally inverted).', '[3]'),
        lambda r: ('A ray from the person’s shoe meets the mirror at 35° to the normal. State its angle of reflection.', '35°', '[1]'),
        lambda r: ('Explain why the image cannot be formed on a screen.', 'Rays do not actually meet there; they only appear to come from behind the mirror.', '[2]'),
        lambda r: ('The person moves 0.5 m closer. State the new distance between person and image.', f'{g(2 * (d - 0.5))} m', '[1]'),
    ]
    return compose(r, f'{person(r)} stands {g(d)} m in front of a large plane mirror in a dance studio.', parts, k=(2, 3, 4), type_='multi_step')


t131.add('C4', (2, 3, 4, 5), 'multi_step')(_refl_c4)

N132 = 'Refraction of light: refractive index and n = sin i / sin r'
t132 = topic(N132, N132.lower(), 'refraction of light', 'refractive index')
MED = [('glass', 1.5), ('water', 1.33), ('Perspex', 1.49), ('diamond', 2.42), ('crown glass', 1.52), ('ice', 1.31), ('sapphire', 1.77), ('quartz', 1.54)]
FX(t132, 'C1', (1, 2), [
    ('When light passes from air into glass, it', 'slows down and bends towards the normal', 'Glass is optically denser: lower speed, ray bends towards the normal.', ['speeds up and bends away from the normal', 'slows down and bends away from the normal', 'does not change direction at any angle']),
    ('A ray enters a glass block along the normal. What happens to it?', 'It passes straight through without bending', 'At 0° incidence there is no change of direction (speed still changes).', ['It bends towards the normal', 'It is totally internally reflected', 'It bends away from the normal']),
    ('Which equation defines refractive index?', 'n = sin i / sin r', 'Ratio of sines of the angles in air (i) and in the medium (r).', ['n = sin r / sin i', 'n = i / r', 'n = sin i × sin r']),
    ('Refraction happens because light', 'changes speed when it enters a different medium', 'Change in speed at an angle causes a change of direction.', ['changes frequency', 'is absorbed by the medium', 'reflects off the boundary']),
    ('Light passes from glass into air at an angle. It', 'speeds up and bends away from the normal', 'Into a less dense medium: away from the normal.', ['slows down and bends towards the normal', 'stops', 'always reflects']),
    ('Define refractive index.', 'The ratio of the speed of light in a vacuum (air) to the speed of light in the material (= sin i / sin r).', '[1]'),
])
FX(t132, 'C2', (1, 2, 3, 4), [
    ('Explain why a swimming pool looks shallower than it really is.', 'Light from the bottom refracts away from the normal as it leaves the water; the eye traces the rays back in straight lines, so they appear to come from a shallower point.', 'refraction away from normal at surface [1]; eye traces back in straight line → apparent depth [1] [2]'),
    ('Describe an experiment to measure the refractive index of a glass block.', 'Shine a ray at a measured angle of incidence onto the block; mark the emergent ray; join entry and exit points to find the refracted ray; measure r from the normal; repeat for several i; plot sin i against sin r; gradient = n.', 'measure i and r with protractor [1]; repeat for several angles [1]; n = sin i/sin r or gradient [1] [3]'),
    ('Explain why a ray emerging from a parallel-sided glass block is parallel to the incident ray.', 'Refraction at the two parallel faces is equal and opposite, so the ray is displaced sideways but its direction is restored.', 'equal and opposite bending [1]; lateral displacement only [1] [2]'),
    ('Explain why a material with a higher refractive index bends light more.', 'Light slows more in it, so the change in speed at the boundary is greater, causing a larger change of direction.', 'greater slowing [1]; larger deviation [1] [2]'),
])


@t132.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t132_n(r, D):
    m, n = r.choice(MED)
    i = r.choice([20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
    rr = math.degrees(math.asin(math.sin(math.radians(i)) / n))
    if D <= 2:
        rr_ = round(rr)
        nn = math.sin(math.radians(i)) / math.sin(math.radians(rr_))
        return numq(r, D, f'A ray of light passes from air into {m}. The angle of incidence is {i}° and the angle of refraction is {rr_}°.', 'refractive index', nn, '', f'n = sin {i}° / sin {rr_}°', [i / rr_ * 0.9, 1 / nn, nn + 0.5], fm=lambda x: g(x, 3))
    if D == 3:
        return Q(f'A ray of light passes from air into {m} (refractive index {n}) with an angle of incidence of {i}°. Calculate the angle of refraction.', f'{g(rr, 3)}°',
                 f'sin r = sin {i}°/{n} [1] = {g(math.sin(math.radians(i)) / n, 3)} [1]; r = {g(rr, 3)}° [1] [3]')
    i2 = r.choice([x for x in [20, 30, 40, 50, 60] if x != i])
    r2 = math.degrees(math.asin(math.sin(math.radians(i2)) / n))
    return Q(f'A student shines rays into a block of {m}. With i = {i}° she measures r = {g(rr, 3)}°; with i = {i2}° she measures r = {g(r2, 3)}°. (a) Calculate the refractive index from each reading. (b) State the mean value. (c) Explain why the ray bends towards the normal on entering the block.',
             f'(a) {g(n, 3)} and {g(n, 3)} (b) {g(n, 3)} (c) light slows down in {m}, which is optically denser than air.',
             f'(a) n = sin i/sin r for each [2] (b) mean [1] (c) slows down in denser medium [1]' + (' [4]' if D == 4 else '; suggests plotting sin i against sin r for a better value [1] [5]'), 'multi_step')


@t132.add('C2', (2, 3, 4), 'explain')
def t132_cmp(r, D):
    (a, na), (b, nb) = r.sample(MED, 2)
    if na == nb:
        return None
    return Q(f'A ray enters {a} (n = {na}) and {b} (n = {nb}) from air at the same angle of incidence of 40°. State in which material it bends more and explain.', f'{cap(a if na > nb else b)}: higher refractive index, so light slows more and bends more towards the normal (smaller angle of refraction).',
             'correct material [1]; higher n → more slowing / smaller r [1] [2]')


def _refr_c4(r, D):
    m, n = r.choice(MED[:3] + MED[4:5])
    i = r.choice([30, 40, 50, 60])
    rr = math.degrees(math.asin(math.sin(math.radians(i)) / n))
    parts = [
        lambda r: ('Calculate the angle of refraction inside the block.', f'{g(rr, 3)}°', 'sin r = sin i/n [2]'),
        lambda r: ('State the angle at which the ray leaves the opposite parallel face, measured from the normal.', f'{i}°', '[1]'),
        lambda r: ('Explain why the ray changes direction at the first face.', 'It slows down on entering the denser medium at an angle.', '[2]'),
        lambda r: ('State what happens to the frequency of the light inside the block.', 'Unchanged.', '[1]'),
        lambda r: ('Describe how the path would differ if the ray entered along the normal.', 'It would pass straight through without bending.', '[1]'),
    ]
    return compose(r, f'A ray of light in air strikes a parallel-sided block of {m} (n = {n}) at an angle of incidence of {i}°.', parts, k=(2, 3, 4), type_='multi_step')


t132.add('C4', (2, 3, 4, 5), 'multi_step')(_refr_c4)

N133 = 'Total internal reflection, critical angle and optical fibres'
t133 = topic(N133, N133.lower(), 'total internal reflection', 'critical angle', 'optical fibres')
FX(t133, 'C1', (1, 2), [
    ('Total internal reflection can occur when light travels', 'from glass into air at an angle greater than the critical angle', 'Needs denser → less dense medium and i > c.', ['from air into glass at any angle', 'from glass into air at an angle less than the critical angle', 'along the normal']),
    ('Which equation links the critical angle c and refractive index n?', 'n = 1 / sin c', 'sin c = 1/n.', ['n = sin c', 'n = sin c / sin 90°', 'n = c / 90']),
    ('The critical angle for glass is about 42°. A ray inside the glass meets the surface at 50°. What happens?', 'It is totally internally reflected', '50° > 42° so TIR.', ['It refracts out along the surface', 'It passes straight out', 'It is absorbed']),
    ('Optical fibres carry signals using', 'total internal reflection', 'Light reflects repeatedly off the inner surface of the fibre.', ['refraction out of the fibre', 'diffraction', 'dispersion']),
    ('At the critical angle, the refracted ray', 'travels along the boundary (angle of refraction 90°)', 'Definition of the critical angle.', ['travels along the normal', 'is reflected back at 0°', 'disappears']),
    ('Define the critical angle.', 'The angle of incidence in the denser medium for which the angle of refraction is 90°.', '[1]'),
])
FX(t133, 'C2', (1, 2, 3, 4), [
    ('Explain why diamonds sparkle more than glass of the same shape.', 'Diamond has a very high refractive index and so a small critical angle (about 24°); light entering is totally internally reflected many times before it leaves.', 'high n / small critical angle [1]; many total internal reflections [1] [2]'),
    ('Explain how an endoscope lets a doctor see inside a patient’s body.', 'Bundles of optical fibres carry light into the body and carry the reflected image back by total internal reflection, even round bends.', 'optical fibres [1]; TIR carries light round bends [1] [2]'),
    ('Explain why a 45° glass prism can turn a ray through 90° in a periscope.', 'The ray meets the hypotenuse at 45°, which is greater than the critical angle of glass (about 42°), so it is totally internally reflected through 90°.', '45° > 42° [1]; TIR turns ray 90° [1] [2]'),
    ('Explain why optical fibres are used for broadband instead of copper wires.', 'They carry much more data with little loss, are not affected by electrical interference, and are lighter.', 'any two advantages [2]'),
])


@t133.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t133_c(r, D):
    m, n = r.choice(MED)
    c = math.degrees(math.asin(1 / n))
    if D <= 2:
        return numq(r, D, f'The refractive index of {m} is {n}.', 'critical angle', c, '°', f'sin c = 1/{n}; c = sin⁻¹(1/{n})', [90 - c, c / 2, math.degrees(math.asin(min(0.99, n / 3)))], fm=lambda x: g(x, 3))
    if D == 3:
        ang = r.choice([30, 35, 40, 45, 50, 55, 60, 70])
        tir = ang > c
        return Q(f'A ray inside a block of {m} (n = {n}) meets the {m}–air boundary at an angle of incidence of {ang}°. Calculate the critical angle and state what happens to the ray.', f'c = {g(c, 3)}°; {"total internal reflection" if tir else "it refracts out into the air (with some partial reflection)"}.',
                 f'sin c = 1/n [1]; c = {g(c, 3)}° [1]; {ang}° {">" if tir else "<"} c so {"TIR" if tir else "refraction"} [1] [3]')
    cc = r.choice([38, 40, 41, 42, 45, 48, 49])
    nn = 1 / math.sin(math.radians(cc))
    return Q(f'In an experiment, the critical angle for a new plastic is measured as {cc}°. (a) Calculate its refractive index. (b) A ray in the plastic meets the surface at {cc - 10}°. Calculate the angle of refraction in air. (c) Explain whether this plastic could be used in a 45° prism periscope.',
             f'(a) {g(nn, 3)} (b) {g(math.degrees(math.asin(min(1, nn * math.sin(math.radians(cc - 10))))), 3)}° (c) {"yes" if cc < 45 else "no"}: rays hit the long face at 45°, which is {"greater" if cc < 45 else "less"} than the critical angle, so {"TIR occurs" if cc < 45 else "light would refract out"}.',
             f'(a) n = 1/sin c [1] = {g(nn, 3)} [1] (b) sin r = n sin i [1] (c) compare 45° with c [1]' + (' [4]' if D == 4 else '; conclusion [1] [5]'), 'multi_step')


def _tir_c4(r, D):
    m, n = r.choice([('glass', 1.5), ('Perspex', 1.49), ('crown glass', 1.52)])
    c = math.degrees(math.asin(1 / n))
    parts = [
        lambda r: ('Calculate the critical angle of the fibre core.', f'{g(c, 3)}°', 'sin c = 1/n [2]'),
        lambda r: ('State the two conditions needed for total internal reflection.', 'Light travels from a denser to a less dense medium; angle of incidence greater than the critical angle.', '[2]'),
        lambda r: ('Explain how light is carried along a curved fibre.', 'It meets the wall at angles greater than c and is totally internally reflected repeatedly.', '[2]'),
        lambda r: ('Give one medical and one communication use of optical fibres.', 'Endoscope; broadband/telephone signals.', '[2]'),
        lambda r: ('Explain why a fibre bent too sharply loses light.', 'The angle of incidence at the bend falls below the critical angle, so some light refracts out.', '[2]'),
    ]
    return compose(r, f'An optical fibre has a core made of {m} (n = {n}).', parts, k=(2, 3, 4), type_='multi_step')


t133.add('C4', (2, 3, 4, 5), 'multi_step')(_tir_c4)

N134 = 'Thin converging and diverging lenses: ray diagrams, real and virtual images'
t134 = topic(N134, N134.lower(), 'converging and diverging lenses', 'ray diagrams')
FX(t134, 'C1', (1, 2), [
    ('A converging lens makes parallel rays of light', 'meet at the principal focus', 'Converging (convex) lens brings parallel rays to a focus.', ['spread out as if from a point', 'stay parallel', 'reflect back']),
    ('The focal length of a lens is the distance from', 'the centre of the lens to the principal focus', 'f = optical centre to F.', ['the object to the image', 'the lens to the object', 'one surface to the other']),
    ('An object is placed closer to a converging lens than its focal length. The image is', 'virtual, upright and magnified', 'Magnifying glass arrangement.', ['real, inverted and diminished', 'real, upright and the same size', 'virtual, inverted and diminished']),
    ('Which lens is used to correct short sight?', 'A diverging lens', 'Short sight: image forms in front of the retina; a diverging lens spreads the rays first.', ['A converging lens', 'A plane mirror', 'A prism']),
    ('A real image is one that', 'can be formed on a screen', 'Rays actually meet at a real image.', ['can never be seen', 'is always upright', 'is always larger than the object']),
    ('Which lens is used to correct long sight?', 'A converging lens', 'Long sight: image would form behind the retina.', ['A diverging lens', 'A concave mirror', 'A plane mirror']),
    ('State what happens to rays parallel to the principal axis after passing through a diverging lens.', 'They spread out as if they came from the principal focus on the same side as the incoming light.', '[1]'),
])
FX(t134, 'C2', (1, 2, 3, 4), [
    ('Describe the three rays used to draw a ray diagram for a converging lens.', 'A ray parallel to the axis refracts through F; a ray through the optical centre passes straight on; a ray through F on the object side emerges parallel to the axis.', 'parallel → through F [1]; through centre undeviated [1]; through F → parallel [1] [3]'),
    ('Explain why a camera with a converging lens produces a real, inverted image on its sensor.', 'The object is far beyond 2F, so rays from it converge to a point beyond F on the other side, forming a real, inverted, diminished image where the sensor is placed.', 'object beyond 2F [1]; rays converge to real inverted image [1] [2]'),
    ('Explain how a converging lens acts as a magnifying glass.', 'With the object closer than F, the rays leaving the lens diverge; the eye traces them back to a virtual, upright, magnified image on the same side as the object.', 'object inside F [1]; diverging rays traced back → virtual upright enlarged image [1] [2]'),
    ('Explain why a diverging lens can only form virtual images of real objects.', 'Rays leaving a diverging lens always spread out, so they never meet; they only appear to come from a point on the object side.', 'rays always diverge [1]; only appear to meet [1] [2]'),
])
POS = [('more than twice the focal length (beyond 2F)', 'real, inverted, diminished', 'between F and 2F on the other side', 'camera / eye'),
       ('exactly twice the focal length (at 2F)', 'real, inverted, same size', 'at 2F on the other side', 'photocopier at same size'),
       ('between F and 2F', 'real, inverted, magnified', 'beyond 2F on the other side', 'projector'),
       ('less than the focal length (inside F)', 'virtual, upright, magnified', 'on the same side as the object, further from the lens', 'magnifying glass')]


@t134.add('C1', (1, 2, 3))
def t134_pos(r, D):
    p, im, where, use = r.choice(POS)
    opts, a = mcq(r, im, [x[1] for x in POS if x[1] != im] + ['virtual, inverted, diminished'])
    return Q(f'An object is placed at a distance from a thin converging lens of {p}. Which describes the image?', a, f'Object {p}: image {im}, {where} (used in a {use}).', opts=opts)


@t134.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t134_diag(r, D):
    f = r.choice([5, 8, 10, 12, 15, 20])
    k = r.choice([1.25, 1.5, 3, 4, 0.5, 0.6, 2])
    u = f * k
    if abs(u - f) < 1e-9:
        return None
    v = 1 / (1 / f - 1 / u)  # real if > 0
    real = v > 0
    M = abs(v) / u
    h = r.choice([1, 2, 3, 4])
    desc = ('real, inverted, ' if real else 'virtual, upright, ') + ('magnified' if M > 1.01 else 'diminished' if M < 0.99 else 'same size')
    if D <= 2:
        opts, a = mcq(r, desc, [x for x in ['real, inverted, magnified', 'real, inverted, diminished', 'virtual, upright, magnified', 'virtual, inverted, diminished', 'real, inverted, same size'] if x != desc][:4])
        return Q(f'An object is placed {g(u)} cm from a converging lens of focal length {f} cm. What is the nature of the image?', a, f'u = {g(u)} cm, f = {f} cm: image {desc}.', opts=opts) if D == 1 else \
            Q(f'An object is placed {g(u)} cm from a converging lens of focal length {f} cm. State three properties of the image.', cap(desc) + '.', 'all three properties correct = 2 marks; two correct = 1 mark [2]')
    if D == 3:
        return Q(f'An object {h} cm tall is placed {g(u)} cm from a converging lens of focal length {f} cm. A scale ray diagram gives the image {g(abs(v), 3)} cm from the lens. Describe the image and calculate its height using magnification = image distance ÷ object distance.',
                 f'{cap(desc)}; height {g(M * h, 3)} cm', f'nature [1]; magnification = {g(abs(v), 3)}/{g(u)} = {g(M, 3)} [1]; height = {g(M * h, 3)} cm [1] [3]')
    return Q(f'An object {h} cm tall stands on the principal axis {g(u)} cm from a thin converging lens of focal length {f} cm. (a) Describe how to draw a scale ray diagram to locate the image. (b) The diagram gives an image distance of {g(abs(v), 3)} cm. State the nature of the image and where it is. (c) Calculate the image height. (d) Suggest a device that uses this arrangement.',
             f'(a) choose a scale; draw a ray parallel to the axis then through F; draw a ray through the optical centre undeviated; where they {"meet" if real else "appear to meet when extended back"} is the image. (b) {desc}, {g(abs(v), 3)} cm from the lens on the {"opposite" if real else "same"} side. (c) {g(M * h, 3)} cm (d) ' + next(x[3] for x in POS if (x[1].startswith('virtual') and not real) or (real and ((M > 1.01 and 'magnified' in x[1]) or (M < 0.99 and 'diminished' in x[1]) or (0.99 <= M <= 1.01 and 'same' in x[1])))) + '.',
             '(a) two correct construction rays [1] (b) nature and position [1] (c) magnification method [1] (d) device [1]' + (' [4]' if D == 4 else '; scale stated/used correctly [1] [5]'), 'multi_step')


@t134.add('C2', (2, 3, 4), 'explain')
def t134_sight(r, D):
    k = r.choice(['short sight', 'long sight'])
    return Q(f'Explain what causes {k} and how it is corrected with a lens.', ('The eye focuses light from distant objects in front of the retina (eye lens too strong / eyeball too long); a diverging lens spreads the rays so they focus on the retina.' if k == 'short sight' else
                                                                           'The eye focuses light from near objects behind the retina (eye lens too weak / eyeball too short); a converging lens converges the rays so they focus on the retina.'),
             'where image forms [1]; correct lens type [1]; how it fixes the focus [1] [3]')


def _lens_c4(r, D):
    f = r.choice([10, 15, 20])
    parts = [
        lambda r: ('Define the focal length.', 'Distance from the centre of the lens to the principal focus.', '[1]'),
        lambda r: (f'An object is placed {3 * f} cm from the lens. Describe the image.', 'Real, inverted, diminished, between F and 2F.', '[2]'),
        lambda r: (f'The object is moved to {f // 2} cm from the lens. Describe the new image.', 'Virtual, upright, magnified, on the same side as the object.', '[2]'),
        lambda r: ('Explain why the second image cannot be shown on a screen.', 'It is virtual: rays only appear to come from it.', '[1]'),
        lambda r: ('Name the arrangement used as a magnifying glass.', f'Object inside F (less than {f} cm from the lens).', '[1]'),
        lambda r: ('Describe a simple way to measure the focal length.', 'Focus an image of a distant object (window) onto a screen and measure lens–screen distance.', '[2]'),
    ]
    return compose(r, f'A thin converging lens has a focal length of {f} cm.', parts, k=(2, 3, 4), type_='multi_step')


t134.add('C4', (2, 3, 4, 5), 'multi_step')(_lens_c4)

N135 = 'Dispersion of light and the visible spectrum'
t135 = topic(N135, N135.lower(), 'dispersion', 'visible spectrum')
COLS = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
FX(t135, 'C1', (1, 2, 3), [
    ('When white light passes through a prism, which colour is refracted the most?', 'Violet', 'Violet has the highest frequency and is slowed most.', ['Red', 'Green', 'Yellow']),
    ('Dispersion is', 'the splitting of white light into its component colours', 'Different colours refract by different amounts.', ['the reflection of light from a mirror', 'the bending of light round an obstacle', 'the absorption of light by black surfaces']),
    ('Which colour of visible light has the longest wavelength?', 'Red', 'Red: longest wavelength, lowest frequency.', ['Violet', 'Blue', 'Green']),
    ('Monochromatic light is light of', 'a single frequency (one colour)', 'Lasers produce nearly monochromatic light.', ['many frequencies', 'all colours mixed', 'zero frequency']),
    ('State the order of the colours in the visible spectrum, starting with the least refracted.', 'Red, orange, yellow, green, blue, indigo, violet.', '[1]'),
])
FX(t135, 'C2', (1, 2, 3, 4), [
    ('Explain why a prism splits white light into a spectrum.', 'White light is a mixture of colours; each colour has a different frequency and travels at a slightly different speed in glass, so each is refracted by a different amount; violet is bent most and red least.', 'mixture of colours [1]; different speeds/refractive index [1]; different angles, violet most [1] [3]'),
    ('Explain how a rainbow is formed.', 'Sunlight enters raindrops and is refracted and dispersed, reflected off the back of the drop, then refracted again as it leaves, spreading the colours out.', 'refraction/dispersion in drops [1]; internal reflection [1]; second refraction [1] [3]'),
    ('Explain why no spectrum is seen when laser light passes through a prism.', 'Laser light is monochromatic (one frequency), so there is only one colour to refract and no splitting occurs.', 'monochromatic [1]; single angle of refraction [1] [2]'),
])


@t135.add('C1', (1, 2, 3))
def t135_order(r, D):
    a, b = r.sample(range(7), 2)
    q = r.choice(['more refracted', 'longer wavelength', 'higher frequency'])
    hi = COLS[max(a, b)] if q in ('more refracted', 'higher frequency') else COLS[min(a, b)]
    lo = COLS[min(a, b)] if hi == COLS[max(a, b)] else COLS[max(a, b)]
    opts, ans = mcq(r, hi, [c for c in COLS if c != hi])
    return Q(f'Which colour is {q}: {COLS[a]} or {COLS[b]}?', ans, f'Order red → violet: wavelength decreases, frequency and refraction increase. So {hi}.', opts=opts)


@t135.add('C3', (2, 3, 4), 'case')
def t135_n(r, D):
    nr = r.choice([1.510, 1.513, 1.514])
    nv = nr + r.choice([0.017, 0.019, 0.021])
    i = r.choice([30, 40, 45, 50, 60])
    rr = math.degrees(math.asin(math.sin(math.radians(i)) / nr))
    rv = math.degrees(math.asin(math.sin(math.radians(i)) / nv))
    return Q(f'A type of glass has refractive index {nr:.3f} for red light and {nv:.3f} for violet light. White light enters the glass from air at an angle of incidence of {i}°. (a) Calculate the angle of refraction for each colour. (b) Explain how this produces a spectrum.',
             f'(a) red {rr:.1f}°, violet {rv:.1f}° (b) the colours travel in slightly different directions, so they separate; violet is bent more (smaller r).',
             f'(a) sin r = sin i/n for each [2] (b) different angles → separation [1]' + (' [3]' if D < 4 else '; violet bent most, red least [1] [4]'))


def _disp_c4(r, D):
    parts = [
        lambda r: ('Name this effect.', 'Dispersion.', '[1]'),
        lambda r: ('State which colour appears at the top (least deviated) and which at the bottom.', 'Red least deviated; violet most.', '[2]'),
        lambda r: ('Explain why the colours separate.', 'Each colour has a different frequency and a different speed (refractive index) in glass, so each refracts by a different amount.', '[2]'),
        lambda r: ('State which colour travels slowest in the glass.', 'Violet.', '[1]'),
        lambda r: ('Describe what is seen if the spectrum passes through a second, inverted prism.', 'The colours recombine to give white light.', '[1]'),
        lambda r: ('Explain why a red laser beam is not split by the prism.', 'It is monochromatic.', '[1]'),
    ]
    return compose(r, r.choice(['A narrow beam of white light passes through a triangular glass prism onto a screen.', f'{person(r)} shines sunlight through a prism in a darkened room.']), parts, k=(2, 3, 4), type_='multi_step')


t135.add('C4', (2, 3, 4, 5), 'multi_step')(_disp_c4)

CHAPTERS[13] = [t131, t132, t133, t134, t135]
