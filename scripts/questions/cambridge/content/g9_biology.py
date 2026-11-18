"""Cambridge IGCSE Biology 0610 Extended (2026-28), CUP coursebook chapters 1-10 (grade 9).

Paper 2 (MCQ), Paper 4 (structured theory) and Paper 6 (Alternative to Practical) styles.
Each topic is built from a knowledge pack by the generic builders below (key terms,
explain items, misconceptions, long answers) plus parameterised data / calculation
templates. practical() builds ATP-style items from an experiment spec: a results table
with repeats (and sometimes an anomaly), variables, controls, mean, trend, explanation,
improvements and topic-specific calculations.

The builders are shared with g10_biology.py.
"""
import math
import re
from core import Tpl
from ._lib import topic, mcq, compose, sf, sci, person, two_people, city, num_mcq, near  # noqa: F401

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

# ===================================================================== builders
_TAG = re.compile(r'\[(\d+)\]')


def cap(s):
    if s[:2] == 'pH' or s[:2] == 'mR':
        return s
    return s[:1].upper() + s[1:]


def low(s):
    return s[:1].lower() + s[1:]


def mk(key):
    m = _TAG.findall(key)
    return int(m[-1]) if m else 1


def fx(x, dp=1):
    """Fixed decimals with trailing zeros stripped (mark-scheme style)."""
    s = f'{x:.{dp}f}'
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def Q(stem, ans, key, typ=None, marks=None):
    q = {'stem': stem, 'answer': ans, 'key': key, 'marks': marks or mk(key)}
    if typ:
        q['type'] = typ
    return q


def _nk(x):
    return ' '.join(str(x).lower().split())


def MQ(r, stem, correct, wrong, key):
    seen = {_nk(correct)}
    ws = []
    for w in wrong:
        if _nk(w) not in seen:
            seen.add(_nk(w))
            ws.append(w)
    if len(ws) < 3:
        return None
    opts, ans = mcq(r, correct, ws)
    return {'stem': stem, 'options': opts, 'answer': ans, 'key': key, 'marks': 1}


def NQ(r, stem, val, wrong, unit, key, f=None):
    f = f or (lambda x: sf(x, 3))
    c = f(val) + unit
    ws = []
    for w in wrong:
        s = f(w) + unit
        if _nk(s) != _nk(c) and _nk(s) not in [_nk(x) for x in ws]:
            ws.append(s)
    if len(ws) < 3:
        return None
    opts, ans = mcq(r, c, ws)
    return {'stem': stem, 'options': opts, 'answer': ans, 'key': key, 'marks': 1}


def T(name, *extra):
    return topic(name, name, *extra)


def _reg(t, C, D, fn, typ, name):
    t.templates.append(Tpl(C, tuple(D), fn, typ, name))


def facts(t, pairs, D=(1, 2, 3)):
    """pairs: [(term, definition)] -> C1 recall: definition -> term MCQ, term -> definition MCQ, 'Define' (D3)."""
    def fn(r, D_):
        term, dfn = r.choice(pairs)
        others = [p for p in pairs if p[0] != term]
        if len(others) < 3:
            return None
        mode = r.randrange(3) if D_ >= 3 else r.randrange(2)
        if mode == 0:
            st = r.choice(['Which term matches this description:', 'Which term is defined as', 'What is the name for'])
            return MQ(r, f'{st} "{dfn}"?', cap(term), [cap(o[0]) for o in others], f'{cap(term)}: {dfn}.')
        if mode == 1:
            # long options + short stem: the validator compares stem + options, so keep one phrasing and a fixed
            # (cyclic) distractor set per term; repeated asks of a term are then exact stem repeats that core skips.
            if len(pairs) < 5:
                return None
            i = pairs.index((term, dfn))
            ds = [pairs[(i + j) % len(pairs)][1] for j in (1, 2, 3)]
            return MQ(r, f'Which is the correct definition of the term "{term}"?', cap(dfn) + '.', [cap(o) + '.' for o in ds], f'{cap(term)}: {dfn}.')
        st = r.choice(['Define the term', 'State what is meant by the term', 'Give the meaning of the term'])
        return Q(f'{st} {term}.', cap(dfn) + '.', f'{cap(dfn)}. Main idea [1] + precise detail [1] [2]', 'short')
    _reg(t, 'C1', D, fn, 'mcq', 'facts')


def mcqs(t, entries, D=(1, 2), C='C1'):
    """entries: (stem, answer, key, [3+ distractors]) stand-alone MCQs."""
    for e in entries:
        def fn(r, D_, e=e):
            return MQ(r, e[0], e[1], e[3], e[2])
        _reg(t, C, D, fn, 'mcq', 'mcq')


def explain(t, entries, C='C2', D=(2, 3, 4), typ='explain'):
    """entries: (stem, answer, key ending in [n]). C1/C2 entries are also auto-paired by core.augment."""
    if not hasattr(t, 'entries'):
        t.entries = {}
    if C in ('C1', 'C2'):
        t.entries.setdefault(C, []).extend((e, tuple(D)) for e in entries)
    for e in entries:
        def fn(r, D_, e=e):
            return Q(e[0], e[1], e[2], typ)
        _reg(t, C, D, fn, typ, 'fixed')


def shorts(t, entries, D=(1, 2, 3)):
    explain(t, entries, 'C1', D, 'short')


def longs(t, entries, D=(3, 4, 5)):
    explain(t, entries, 'C4', D, 'long')


def myths(t, entries, D=(2, 3, 4)):
    """entries: (incorrect statement, correction). C2 spot-the-error."""
    def fn(r, D_):
        claim, fix = r.choice(entries)
        p = person(r)
        st = r.choice([f'{p} writes in a revision note: "{claim}" Identify the error and write a correct statement.',
                       f'A student in {city(r)} states: "{claim}" Explain why this statement is incorrect.',
                       f'{p} says: "{claim}" Explain whether {p} is correct.'])
        return Q(st, fix, f'1 mark: identifies the error / statement is incorrect; 1 mark: {fix} [2]', 'explain')
    _reg(t, 'C2', D, fn, 'explain', 'myth')


def pct(a, b):
    return (b - a) / a * 100


def trend_text(iv, dv, xs, ms, u='', xfmt=None):
    xf = xfmt or (lambda v: f'{v} {u}'.strip())
    n = len(ms)
    up = all(ms[i + 1] > ms[i] for i in range(n - 1))
    dn = all(ms[i + 1] < ms[i] for i in range(n - 1))
    hi = max(range(n), key=lambda i: ms[i])
    lo = min(range(n), key=lambda i: ms[i])
    rng = (max(ms) - min(ms)) or 1
    if up:
        if n >= 4 and (ms[-1] - ms[-2]) < 0.12 * rng:
            return f'As the {iv} increases, the {dv} increases and then levels off at about {xf(fx(xs[-2], 2))}.'
        return f'As the {iv} increases, the {dv} increases (from {fx(ms[0], 2)} to {fx(ms[-1], 2)}).'
    if dn:
        if n >= 4 and (ms[-2] - ms[-1]) < 0.12 * rng:
            return f'As the {iv} increases, the {dv} decreases and then levels off at about {xf(fx(xs[-2], 2))}.'
        return f'As the {iv} increases, the {dv} decreases (from {fx(ms[0], 2)} to {fx(ms[-1], 2)}).'
    if 0 < hi < n - 1:
        return f'The {dv} increases as the {iv} rises to {xf(fx(xs[hi], 2))}, which gives the highest value, then decreases.'
    if 0 < lo < n - 1:
        return f'The {dv} decreases as the {iv} rises to {xf(fx(xs[lo], 2))}, which gives the lowest value, then increases.'
    return f'There is no clear trend between {iv} and {dv}.'


def practical(r, D, ex, k=(2, 3), typ='case'):
    """ATP-style data item from an experiment spec (see module docstring)."""
    p = person(r)
    xs = ex['xs'](r)
    kk = r.uniform(0.88, 1.12)
    dp = ex.get('dp', 0)
    nrep = ex.get('reps', 3)
    ivn, ivu = ex['iv']
    dvn, dvu = ex['dv']
    rows = []
    for x in xs:
        base = ex['y'](x, kk)
        row = []
        for _ in range(nrep):
            v = base * (1 + r.uniform(-ex.get('noise', 0.04), ex.get('noise', 0.04)))
            row.append(v if ex.get('neg') else max(v, 10 ** -dp if dp else 1))
        rows.append(row)
    anom = None
    if nrep >= 3 and (D >= 3 or r.random() < 0.4):
        i = r.randrange(len(xs))
        j = r.randrange(nrep)
        rows[i][j] *= r.choice([1.45, 0.6])
        anom = (i, j)
    txt = [[fx(v, dp) for v in row] for row in rows]
    vals = [[float(s) for s in row] for row in txt]
    means = []
    for i, row in enumerate(vals):
        use = [v for j, v in enumerate(row) if anom != (i, j)]
        means.append(sum(use) / len(use))
    xsT = [x if isinstance(x, str) else fx(x, 3) for x in xs]
    xf_ = ex.get('xfmt') or (lambda s_: f'{s_} {ivu}'.strip())
    xl = lambda s_: f"{ex.get('prep', 'at')} {xf_(s_)}"  # noqa: E731
    hdr = f'{cap(ivn)} / {ivu}' if ivu else cap(ivn)
    hdr2 = f'{cap(dvn)} / {dvu}' if dvu else cap(dvn)
    if nrep > 1:
        reps = '; '.join(f'trial {j + 1}: ' + ', '.join(txt[i][j] for i in range(len(xs))) for j in range(nrep))
        table = f'Results table. {hdr}: {", ".join(xsT)}. {hdr2}, {reps}.'
    else:
        table = f'Results table. {hdr}: {", ".join(xsT)}. {hdr2}: {", ".join(t_[0] for t_ in txt)}.'
    intro = ex['setup'](r, p) + ' ' + table
    d = {'xs': xs, 'vals': vals, 'means': means, 'anom': anom, 'p': p, 'txt': txt, 'kk': kk}
    ctr = ex['controls']
    parts = [lambda r: ('Identify the independent variable and the dependent variable in this investigation.',
                        f'Independent: {ivn}; dependent: {dvn}.', f'independent variable = {ivn} [1]; dependent variable = {dvn} [1] [2]'),
             lambda r: ('State two variables that should be kept constant in this investigation.', f'{cap(ctr[0])}; {ctr[1]}.',
                        'Any two from: ' + '; '.join(ctr) + ' [2]')]
    if anom:
        i, j = anom
        parts.append(lambda r: ('Identify the anomalous result in the table and state what should be done with it.',
                                f'Trial {j + 1} {xl(xsT[i])} ({txt[i][j]} {dvu}); it should be ignored when calculating the mean (or repeated).',
                                f'trial {j + 1} {xl(xsT[i])} identified [1]; ignore / repeat it [1] [2]'))
    if nrep > 1:
        mi = anom[0] if anom and r.random() < 0.7 else r.randrange(len(xs))
        use = [txt[mi][j] for j in range(nrep) if anom != (mi, j)]
        mv = fx(means[mi], dp + 1)
        parts.append(lambda r: (f'Calculate the mean {dvn} {xl(xsT[mi])}' + (', ignoring any anomalous result.' if anom else '.'),
                                f'{mv} {dvu}', f'({" + ".join(use)}) ÷ {len(use)} [1] = {mv} {dvu} [1] [2]'))
    parts.append(lambda r: ('Describe the trend shown by the results.', (ex.get('trend') or (lambda d: trend_text(ivn, dvn, xs, means, ivu, ex.get('xfmt'))))(d),
                            'correct overall pattern [1]; data quoted with units / turning point given [1] [2]'))
    if ex.get('why'):
        w = ex['why'] if not callable(ex['why']) else ex['why'](d)
        parts.append(lambda r: ('Explain the results.', w[0], w[1]))
    imp = ex.get('improve', []) + ['repeat each test more times and calculate a mean (to improve reliability)', 'test more values of the ' + ivn + ' (smaller intervals), especially near the turning point / extremes']
    parts.append(lambda r: ('Suggest one way to improve this investigation.', cap(imp[0]) + '.', 'Any one from: ' + '; '.join(imp) + ' [1]'))
    if ex.get('control'):
        parts.append(lambda r: ('Describe a suitable control for this investigation and explain why it is needed.', ex['control'],
                                '1 mark: control described; 1 mark: shows that the change is caused by the independent variable [2]'))
    if ex.get('graph', True):
        parts.append(lambda r: ('State the type of graph you would draw to display these results and what you would plot on each axis.',
                                f'A line graph: {ivn} on the x-axis and mean {dvn} on the y-axis.',
                                f'line graph (continuous independent variable) [1]; {ivn} on x-axis and {dvn} on y-axis [1] [2]'))
    for e in ex.get('extra', []):
        def f_(r, e=e):
            return e(r, d)
        parts.append(f_)
    return compose(r, intro, parts, k=k, type_=typ)


def add_practical(t, ex, C3D=(2, 3, 4), C4D=(3, 4, 5)):
    if C3D:
        def c3(r, D):
            return practical(r, D, ex, k=(1, 2, 3), typ='case')
        _reg(t, 'C3', C3D, c3, 'case', 'practical')
    if C4D:
        def c4(r, D):
            return practical(r, D, ex, k=(3, 4, 5), typ='case')
        _reg(t, 'C4', C4D, c4, 'case', 'practical4')


def sample_join(r, xs, n):
    s = r.sample(list(xs), n)
    return s, ', '.join(s[:-1]) + ' and ' + s[-1]


# ===================================================================== 1 Characteristics and classification
MRS = [('movement', 'an action by an organism or part of an organism causing a change of position or place'),
       ('respiration', 'the chemical reactions in cells that break down nutrient molecules and release energy for metabolism'),
       ('sensitivity', 'the ability to detect and respond to changes in the internal or external environment'),
       ('growth', 'a permanent increase in size and dry mass'),
       ('reproduction', 'the processes that make more of the same kind of organism'),
       ('excretion', 'the removal of the waste products of metabolism and substances in excess of requirements'),
       ('nutrition', 'the taking in of materials for energy, growth and development')]
MRS_EG = [('a seedling bending towards a window', 'sensitivity'), ('the pupils of a cat narrowing in bright light', 'sensitivity'),
          ('a mimosa plant folding its leaves when touched', 'sensitivity'), ('a tadpole swimming towards food', 'movement'),
          ('chloroplasts moving around inside a leaf cell', 'movement'), ('an earthworm burrowing through soil', 'movement'),
          ('carbon dioxide leaving a fish through its gills', 'excretion'), ('urea being removed from the body in urine', 'excretion'),
          ('a plant releasing oxygen made in photosynthesis that it does not need', 'excretion'),
          ('yeast cells forming buds that separate', 'reproduction'), ('a strawberry plant producing runners that form new plants', 'reproduction'),
          ('a frog laying fertilised eggs', 'reproduction'), ('the dry mass of a bean seedling increasing over ten days', 'growth'),
          ('a child becoming taller and heavier over a year', 'growth'), ('a caterpillar eating a leaf', 'nutrition'),
          ('a plant absorbing nitrate ions from the soil', 'nutrition'), ('a leaf making glucose by photosynthesis', 'nutrition'),
          ('muscle cells breaking down glucose to release energy', 'respiration'), ('germinating seeds giving out heat and carbon dioxide', 'respiration'),
          ('a sunflower seedling increasing permanently in dry mass', 'growth'), ('an owl turning its head towards a rustling sound', 'sensitivity')]
t = T('Characteristics of living organisms (MRS GREN)', 'characteristics of living organisms', 'mrs gren')
facts(t, MRS)
mcqs(t, [
    ('Which list contains only characteristics shared by all living organisms?', 'excretion, growth, nutrition', 'All seven (movement, respiration, sensitivity, growth, reproduction, excretion, nutrition) are shown by every living organism.',
     ['excretion, photosynthesis, growth', 'breathing, growth, nutrition', 'digestion, sensitivity, movement', 'egestion, reproduction, respiration']),
    ('Which process releases energy from nutrient molecules in all living cells?', 'Respiration', 'Respiration is the chemical breakdown of nutrient molecules in cells to release energy; breathing is only the movement of air.',
     ['Breathing', 'Photosynthesis', 'Digestion']),
    ('Which of these is an example of excretion?', 'Removal of carbon dioxide from the lungs', 'CO₂ is a waste product of respiration (metabolism); faeces are egested, not excreted.',
     ['Removal of faeces from the anus', 'Loss of hair from the scalp', 'Release of saliva into the mouth']),
    ('Which change is evidence of growth?', 'A permanent increase in dry mass', 'Growth = permanent increase in size and dry mass; fresh mass changes with water content.',
     ['An increase in fresh mass after watering', 'A temporary increase in size when a cell takes up water', 'An increase in the number of leaves eaten']),
])
shorts(t, [
    ('State the seven characteristics of living organisms.', 'Movement, respiration, sensitivity, growth, reproduction, excretion, nutrition.', 'all seven [2]; five or six [1] [2]'),
    ('State the difference between respiration and breathing.', 'Respiration is chemical reactions in cells releasing energy; breathing is the movement of air into and out of the lungs.', 'respiration = chemical reactions in cells releasing energy [1]; breathing = ventilation / moving air [1] [2]'),
    ('Name two waste products of metabolism that are excreted by humans.', 'Carbon dioxide and urea.', 'any two from: carbon dioxide; urea; excess water / salts [2]'),
])
explain(t, [
    ('A car moves, uses fuel and oxygen, and releases carbon dioxide and water. Explain why a car is not a living organism.', 'It does not show all seven characteristics: it cannot grow, reproduce or respond (sensitivity) on its own, and its "fuel use" is combustion, not respiration in cells.', 'must show all seven characteristics [1]; cannot grow / reproduce / be sensitive [1]; no cells / combustion is not respiration [1] [3]'),
    ('Explain why scientists measure dry mass, not fresh mass, when measuring the growth of a plant.', 'Fresh mass changes with the amount of water the plant has taken up or lost; dry mass measures the permanent increase in organic material.', 'water content varies / is temporary [1]; dry mass shows permanent increase in biomass [1] [2]'),
    ('Explain the difference between excretion and egestion.', 'Excretion removes waste products of metabolism made inside cells (e.g. urea, CO₂); egestion removes undigested food (faeces) that was never absorbed into cells.', 'excretion = metabolic waste [1]; egestion = undigested food that was never part of metabolism [1] [2]'),
    ('Plants do not move from place to place. Explain why plants are still said to show movement.', 'Parts of plants move: leaves and stems turn towards light, flowers open and close, and cytoplasm and chloroplasts move inside cells.', 'movement can be of part of an organism [1]; valid plant example [1] [2]'),
    ('Salt crystals in a solution increase in size. Explain why this is not an example of growth in the biological sense.', 'Crystals are not living: they only add particles on the outside and do not respire, take in nutrients or show the other characteristics; growth in organisms involves cells increasing in number and size.', 'crystals do not show other characteristics of life [1]; biological growth = permanent increase in dry mass through cell division / enlargement [1] [2]'),
    ('Explain why respiration is described as a characteristic of all living organisms, including plants.', 'All living cells need energy for processes such as growth, active transport and making large molecules; this energy is released by respiration, which happens in every living cell, day and night.', 'all cells need energy [1]; respiration happens continuously in all cells, including plant cells [1] [2]'),
])
myths(t, [('Plants photosynthesise instead of respiring.', 'Plants respire all the time in every living cell; they also photosynthesise when there is light.'),
           ('Breathing and respiration are the same process.', 'Breathing moves air in and out of the lungs; respiration is the release of energy from nutrients in cells.'),
           ('Removing faeces is an example of excretion.', 'Removing faeces is egestion, because faeces are undigested food, not waste made by metabolism.'),
           ('A plant that gains mass after watering has grown.', 'The gain is mostly water; growth is a permanent increase in dry mass.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def mrs_apply(r, D):
    n = 1 if D <= 1 else (2 if D == 2 else 3 if D == 3 else 4)
    egs = r.sample(MRS_EG, n)
    if n == 1:
        e, c = egs[0]
        return MQ(r, f'Which characteristic of living organisms is shown by {e}?', cap(c), [cap(x[0]) for x in MRS if x[0] != c], f'{cap(c)}: {dict(MRS)[c]}.')
    labs = ['(i)', '(ii)', '(iii)', '(iv)']
    st = 'Name the characteristic of living organisms shown by each example. ' + ' '.join(f'{labs[i]} {cap(e)}.' for i, (e, c) in enumerate(egs))
    return Q(st, ' '.join(f'{labs[i]} {c}' for i, (e, c) in enumerate(egs)), '; '.join(f'{labs[i]} {c} [1]' for i, (e, c) in enumerate(egs)) + f' [{n}]', 'short', n)


@t.add('C3', (2, 3, 4), 'numerical')
def mrs_growth(r, D):
    d0 = r.choice([0.8, 1.2, 1.5, 2.0, 2.4, 3.0])
    f = r.choice([1.25, 1.4, 1.6, 1.75, 2.0, 2.5])
    days = r.choice([7, 10, 14, 21])
    d1 = round(d0 * f, 2)
    w0, w1 = round(d0 * r.uniform(8, 11), 1), round(d1 * r.uniform(8, 11), 1)
    pc = pct(d0, d1)
    st = (f'{person(r)} grew bean seedlings in {city(r)}. A sample of seedlings had a fresh mass of {w0} g and a dry mass of {fx(d0, 2)} g at the start. '
          f'After {days} days a similar sample had a fresh mass of {w1} g and a dry mass of {fx(d1, 2)} g. Calculate the percentage increase in dry mass'
          + (' and explain why dry mass is a better measure of growth than fresh mass.' if D >= 3 else '.'))
    key = f'({fx(d1, 2)} − {fx(d0, 2)}) ÷ {fx(d0, 2)} × 100 [1] = {sf(pc, 3)}% [1]' + ('; fresh mass varies with water content, dry mass is the permanent increase [1] [3]' if D >= 3 else ' [2]')
    return Q(st, f'{sf(pc, 3)}%' + ('; fresh mass depends on water content, which changes, so dry mass shows permanent growth.' if D >= 3 else ''), key, 'numerical', 3 if D >= 3 else 2)


OBJ = [('a sample of tiny shapes found in rock from a deep mine', {'growth': 'they get larger over several weeks in nutrient broth', 'reproduction': 'they appear to split into two',
        'respiration': 'carbon dioxide is detected above the broth'}),
       ('an unknown green film growing on a pond wall', {'nutrition': 'it gains mass only when light is present', 'growth': 'it spreads over the wall each week',
        'excretion': 'oxygen bubbles are released in light'}),
       ('some crystals in a cave that get larger over time', {'growth': 'they get larger as minerals are added to their surface'}),
       ('a robot vacuum cleaner', {'movement': 'it moves around a room', 'sensitivity': 'it changes direction when it touches a wall', 'nutrition': 'it takes in electrical energy from a charger'}),
       ('a soil sample containing small white threads', {'growth': 'the threads extend through bread placed on the soil', 'nutrition': 'the bread is digested', 'respiration': 'the soil gives out heat and carbon dioxide',
        'reproduction': 'spores are released'}),
       ('a jelly-like blob found on a forest log', {'movement': 'it creeps slowly across the log', 'nutrition': 'it engulfs bacteria', 'sensitivity': 'it moves away from bright light'})]


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def mrs_case(r, D):
    name, obs = r.choice(OBJ)
    p = person(r)
    shown = list(obs)
    missing = [c for c, _ in MRS if c not in shown]
    obs_t = '; '.join(obs.values())
    intro = f'{p}, a student in {city(r)}, investigates {name}. Observations: {obs_t}.'
    parts = [lambda r: ('List the characteristics of living organisms suggested by these observations.', ', '.join(shown) + '.', f'{", ".join(shown)} (all correct) [2]'),
             lambda r: ('Name two other characteristics that must be tested before concluding that it is alive, and suggest how one could be tested.', f'{missing[0]} and {missing[1]}; e.g. ' + {
                 'respiration': 'test for carbon dioxide release or oxygen uptake (e.g. hydrogencarbonate indicator)', 'excretion': 'test for waste products (e.g. carbon dioxide) released',
                 'reproduction': 'see whether it produces more of the same kind', 'growth': 'measure permanent increase in dry mass over time',
                 'sensitivity': 'see whether it responds to a stimulus such as light or touch', 'movement': 'observe it or its parts over time with a microscope',
                 'nutrition': 'see whether it takes in materials, e.g. uses up nutrients from a medium'}[missing[0]] + '.', 'two characteristics not yet observed [1]; valid test [1] [2]'),
             lambda r: ('Evaluate whether there is enough evidence to classify it as a living organism.', ('Not yet: ' if len(shown) < 7 else '') + f'only {len(shown)} of the seven characteristics are shown; a living organism must show all seven' + (' — machines and crystals can show one or two' if len(shown) <= 3 else '') + '.',
                        'all seven needed [1]; refers to the evidence given [1]; conclusion [1] [3]'),
             lambda r: ('Explain why seeing an increase in size alone is not enough evidence of growth in a living organism.', 'Increase in size could be temporary (e.g. water uptake) or non-living accumulation; growth must be a permanent increase in dry mass.', 'temporary / non-living increase possible [1]; permanent increase in dry mass needed [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how a scientist could show that a sample of soil contains living organisms. Refer to at least three characteristics of living organisms in your answer.',
           'Use two samples, one sterilised by heating as a control. Measure carbon dioxide release / oxygen use (respiration) with hydrogencarbonate indicator; look for an increase in the number of organisms (reproduction / growth) on agar; test whether organisms take in nutrients (e.g. starch broken down); keep the conditions the same.',
           'control (heated soil) [1]; respiration test with indicator [1]; growth / reproduction evidence [1]; nutrition evidence [1]; fair test / conditions controlled [1] [5]')])
t_c1a = t

KEY_SETS = {
    'leaf-litter invertebrates': {
        'earthworm': {'legs': False, 'shell': False, 'segmented body': True},
        'slug': {'legs': False, 'shell': False, 'segmented body': False},
        'snail': {'legs': False, 'shell': True, 'segmented body': False},
        'spider': {'legs': True, 'eight legs': True, 'wings': False},
        'beetle': {'legs': True, 'eight legs': False, 'six legs': True, 'wings': True},
        'woodlouse': {'legs': True, 'eight legs': False, 'six legs': False, 'many legs per segment': False},
        'millipede': {'legs': True, 'eight legs': False, 'six legs': False, 'many legs per segment': True},
        'ant': {'legs': True, 'eight legs': False, 'six legs': True, 'wings': False},
    },
    'leaves from trees in a park': {
        'horse chestnut': {'compound leaf': True, 'leaflets spread from one point': True},
        'ash': {'compound leaf': True, 'leaflets spread from one point': False},
        'holly': {'compound leaf': False, 'spiny edge': True},
        'oak': {'compound leaf': False, 'spiny edge': False, 'lobed edge': True},
        'beech': {'compound leaf': False, 'spiny edge': False, 'lobed edge': False, 'toothed edge': False},
        'birch': {'compound leaf': False, 'spiny edge': False, 'lobed edge': False, 'toothed edge': True},
        'maple': {'compound leaf': False, 'spiny edge': False, 'lobed edge': True, 'pointed lobes': True},
    },
    'pond animals': {
        'water flea': {'shell-like covering': True, 'jointed legs': True, 'tail': False},
        'pond snail': {'shell-like covering': True, 'jointed legs': False},
        'flatworm': {'shell-like covering': False, 'jointed legs': False, 'tail': False},
        'mayfly nymph': {'shell-like covering': False, 'jointed legs': True, 'tail': True, 'three tails': True},
        'damselfly nymph': {'shell-like covering': False, 'jointed legs': True, 'tail': True, 'three tails': False, 'flattened tail paddles': True},
        'water boatman': {'shell-like covering': False, 'jointed legs': True, 'tail': False, 'paddle-shaped back legs': True},
        'leech': {'shell-like covering': False, 'jointed legs': False, 'tail': False, 'suckers': True},
    },
}
FEAT_TXT = {'legs': ('has legs', 'has no legs'), 'shell': ('has a shell', 'has no shell'), 'segmented body': ('body is segmented', 'body is not segmented'),
            'eight legs': ('has eight legs', 'does not have eight legs'), 'six legs': ('has six legs', 'does not have six legs'), 'wings': ('has wings', 'has no wings'),
            'many legs per segment': ('has two pairs of legs on most body segments', 'has one pair of legs on each body segment'),
            'compound leaf': ('leaf is divided into leaflets', 'leaf is a single blade'), 'leaflets spread from one point': ('leaflets spread out from one point', 'leaflets arranged in pairs along a central stalk'),
            'spiny edge': ('leaf edge has spines', 'leaf edge has no spines'), 'lobed edge': ('leaf edge has rounded or pointed lobes', 'leaf edge has no lobes'),
            'toothed edge': ('leaf edge is finely toothed', 'leaf edge is smooth'), 'pointed lobes': ('lobes are pointed', 'lobes are rounded'),
            'shell-like covering': ('body enclosed in a shell-like covering', 'no shell-like covering'), 'jointed legs': ('has jointed legs', 'has no jointed legs'),
            'tail': ('has a tail or tail filaments', 'has no tail'), 'three tails': ('has three tail filaments', 'does not have three tail filaments'),
            'flattened tail paddles': ('tail ends in three flattened paddles', 'tail does not end in flattened paddles'),
            'paddle-shaped back legs': ('back legs are paddle-shaped', 'back legs are not paddle-shaped'), 'suckers': ('has suckers at each end', 'has no suckers')}


def build_key(orgs, feats):
    """orgs: {name: {feature: bool}} -> list of key lines, or None if not separable."""
    lines = []

    def split(group):
        if len(group) == 1:
            return group[0]
        best = None
        for f in FEAT_TXT:
            yes = [o for o in group if feats[o].get(f) is True]
            no = [o for o in group if feats[o].get(f) is False]
            if yes and no and len(yes) + len(no) == len(group):
                sc = abs(len(yes) - len(no))
                if best is None or sc < best[0]:
                    best = (sc, f, yes, no)
        if best is None:
            return None
        _, f, yes, no = best
        n = len(lines) + 1
        lines.append(None)
        a = split(yes)
        b = split(no)
        if a is None or b is None:
            return None
        lines[n - 1] = (n, f, a, b)
        return n
    if split(list(orgs)) is None:
        return None
    build_key.raw = lines
    out = []
    for n, f, a, b in lines:
        ya, na = FEAT_TXT[f]
        out.append(f'{n}a {ya} ... ' + (f'go to {a}' if isinstance(a, int) else a) + f'; {n}b {na} ... ' + (f'go to {b}' if isinstance(b, int) else b))
    return out


def key_q(r, D, construct=False):
    setn = r.choice(list(KEY_SETS))
    allo = KEY_SETS[setn]
    for _ in range(10):
        n = 4 if D <= 2 else 5
        orgs = r.sample(list(allo), min(n, len(allo)))
        lines = build_key(orgs, allo)
        if lines:
            raw = build_key.raw
            break
    else:
        return None

    def path(o):
        out, node = [], 1
        while isinstance(node, int):
            n, f, a, b = raw[node - 1]
            yes = allo[o].get(f)
            out.append(FEAT_TXT[f][0 if yes else 1])
            node = a if yes else b
        return out
    key_q.path = path
    tgt = r.choice(orgs)
    desc = [FEAT_TXT[f][0 if v else 1] for f, v in allo[tgt].items()]
    r.shuffle(desc)
    if construct:
        tab = '; '.join(f'{o}: ' + ', '.join(FEAT_TXT[f][0 if v else 1] for f, v in allo[o].items()) for o in orgs)
        return tab, lines, orgs, setn
    return setn, orgs, lines, tgt, desc


t = T('Binomial system and classification by shared features; using dichotomous keys', 'binomial system', 'dichotomous keys')
facts(t, [('species', 'a group of organisms that can reproduce to produce fertile offspring'),
          ('binomial system', 'an internationally agreed system in which the scientific name of an organism is made up of two parts showing the genus and the species'),
          ('genus', 'a group of closely related species; the first part of a binomial name'),
          ('dichotomous key', 'a key that uses a series of paired statements about visible features to identify organisms'),
          ('classification', 'sorting organisms into groups using the features they share'),
          ('hybrid', 'the offspring of two different species, which is usually infertile')])
mcqs(t, [('Which is the correct way to write the scientific name of the lion?', 'Panthera leo (genus capitalised, species in lower case, in italics)', 'Genus with a capital letter, species with a lower-case letter, both in italics (or underlined when handwritten).',
          ['Panthera Leo (both words capitalised)', 'panthera leo (both words in lower case)', 'leo Panthera (species written first)']),
         ('Felis catus (domestic cat) and Felis silvestris (wildcat) belong to the same', 'genus', 'The first part of the binomial name (Felis) is the genus.', ['species', 'variety', 'population']),
         ('A horse and a donkey can breed to produce a mule, which is infertile. What does this show?', 'Horses and donkeys are different species', 'Members of one species produce fertile offspring; mules are infertile hybrids.',
          ['Horses and donkeys are the same species', 'Mules form a new species', 'Horses and donkeys are in different kingdoms'])])
shorts(t, [('State two rules for writing a binomial name.', 'Genus starts with a capital letter, species with a lower-case letter; the name is written in italics (or underlined).', 'capital genus / lower-case species [1]; italics or underlined [1] [2]'),
           ('State why organisms are given internationally agreed scientific names.', 'Common names differ between languages and regions, so scientists everywhere use the same name for the same species.', 'common names vary [1]; avoids confusion / same name worldwide [1] [2]')])
explain(t, [('Explain why classification systems group organisms using shared features.', 'Organisms that share many features are likely to be closely related (share a recent common ancestor), so grouping by shared features reflects evolutionary relationships and makes organisms easier to identify and study.', 'shared features suggest relationship / common ancestry [1]; useful for identification / prediction [1] [2]'),
            ('Explain why a dichotomous key uses visible features rather than features such as diet or behaviour.', 'Visible features can be checked directly on the specimen at any time, so different people get the same result; diet or behaviour may not be observable.', 'features observable on specimen [1]; reliable / consistent identification [1] [2]'),
            ('Explain why each step of a dichotomous key has exactly two statements.', 'Dichotomous means dividing in two: each pair of opposite statements splits the group into two smaller groups until each organism is identified.', 'two contrasting statements [1]; group divided until one organism remains [1] [2]'),
            ('Panthera tigris and Panthera onca share a genus but Canis lupus does not. Explain what this suggests about their relationships.', 'The two Panthera species are more closely related to each other (share a more recent common ancestor) than either is to Canis lupus.', 'same genus = closely related [1]; more recent common ancestor [1] [2]'),
            ('Suggest why feature such as "large" or "dark" should not be used in a dichotomous key.', 'They are relative / subjective, so different people would make different decisions; key statements should be clear and measurable.', 'subjective / depends on comparison [1]; use definite features (e.g. number of legs) [1] [2]')])
myths(t, [('The species name is written first and starts with a capital letter.', 'The genus is written first with a capital letter; the species name follows with a lower-case letter.'),
           ('Any two organisms that can mate belong to the same species.', 'They must produce fertile offspring to be the same species; for example, horses and donkeys produce infertile mules.'),
           ('A dichotomous key can use three choices at each step.', 'A dichotomous key always has two contrasting statements at each step.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def key_use(r, D):
    x = key_q(r, D)
    if not x:
        return None
    setn, orgs, lines, tgt, desc = x
    st = f'A student uses this dichotomous key to identify {setn}. Key: ' + ' | '.join(lines) + f'. The specimen has these features: {"; ".join(desc)}.'
    if D == 1:
        return MQ(r, st + ' What is the specimen?', tgt, [o for o in orgs if o != tgt], f'Following the key with the features given leads to {tgt}.')
    if D >= 3:
        other = r.choice([o for o in orgs if o != tgt])
        path = key_q.path(other)
        return Q(st + f' (a) Use the key to identify the specimen. (b) State the features that the key gives for the {other}.',
                 f'(a) {tgt} (b) {"; ".join(path)}', f'(a) {tgt} [1] (b) features from the key: {"; ".join(path)} [2]', 'short', 3)
    return Q(st + ' Use the key to identify the specimen.', tgt, f'{tgt}: follow each pair of statements in turn [1]', 'short', 1)


BINOM = [('Panthera leo', 'lion'), ('Panthera tigris', 'tiger'), ('Panthera pardus', 'leopard'), ('Felis catus', 'domestic cat'), ('Canis lupus', 'grey wolf'), ('Canis latrans', 'coyote'),
         ('Vulpes vulpes', 'red fox'), ('Ursus arctos', 'brown bear'), ('Ursus maritimus', 'polar bear'), ('Equus caballus', 'horse'), ('Equus zebra', 'mountain zebra'),
         ('Quercus robur', 'English oak'), ('Quercus alba', 'white oak'), ('Acer saccharum', 'sugar maple'), ('Homo sapiens', 'human'), ('Rosa canina', 'dog rose')]


@t.add('C3', (2, 3, 4), 'short')
def binom_rel(r, D):
    gen = {}
    for b, c in BINOM:
        gen.setdefault(b.split()[0], []).append((b, c))
    g = r.choice([k for k in gen if len(gen[k]) >= 2])
    a, b = r.sample(gen[g], 2)
    c = r.choice([x for x in BINOM if x[0].split()[0] != g])
    lst = [a, b, c]
    r.shuffle(lst)
    st = f'Three organisms have the scientific names {", ".join(x[0] for x in lst[:2])} and {lst[2][0]}. (a) State which two are most closely related and give a reason.'
    ans = f'(a) {a[0]} and {b[0]}: they share the genus {g}.'
    key = f'(a) {a[0]} and {b[0]} [1]; same genus ({g}) [1]'
    m = 2
    if D >= 3:
        st += ' (b) State the genus of the third organism.'
        ans += f' (b) {c[0].split()[0]}'
        key += f' (b) {c[0].split()[0]} [1]'
        m = 3
    if D >= 4:
        st += ' (c) Explain why scientists use these names rather than common names such as "' + lst[0][1] + '".'
        ans += ' (c) Common names vary between languages and places; binomial names are the same worldwide.'
        key += ' (c) common names differ / confusing [1]; one agreed international name [1]'
        m += 2
    return Q(st, ans, key + f' [{m}]', 'short', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def key_build(r, D):
    x = key_q(r, max(D, 3), construct=True)
    if not x:
        return None
    tab, lines, orgs, setn = x
    intro = f'{person(r)} collects {setn} on a field trip near {city(r)}. Their features are: {tab}.'
    parts = [lambda r: ('Construct a dichotomous key to identify these organisms.', ' | '.join(lines), f'paired contrasting statements at each step [1]; each organism reached at a separate end-point [1]; uses features given, not size or colour [1]; {len(orgs) - 1} steps [1] [4]'),
             lambda r: ('Explain why the key must use features that do not change during the life of the organism or with the season.', 'Otherwise the same species could be identified differently at different times (e.g. juveniles or seasonal changes).', 'features must be constant [1]; reliable identification [1] [2]'),
             lambda r: ('Suggest one other method, apart from a key, that could be used to check the identification of an organism.', 'Compare its DNA base sequences with known species (or compare with a labelled reference specimen / field guide photograph).', 'DNA sequencing / reference collection [1]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t_c1b = t

# --- kingdoms and main groups
GROUPS = {
    'mammals': ['fur or hair on the skin', 'external ears (pinnae)', 'mammary glands producing milk', 'young that develop inside the mother, attached by a placenta', 'four limbs and a diaphragm'],
    'birds': ['feathers', 'a beak with no teeth', 'wings (front limbs)', 'eggs with hard shells', 'scales on the legs only'],
    'reptiles': ['dry, scaly skin', 'eggs with soft, leathery shells laid on land', 'lungs for breathing air', 'a body temperature that varies with the surroundings'],
    'amphibians': ['moist skin with no scales', 'eggs laid in water with no shell', 'larvae (tadpoles) with gills living in water', 'adults with lungs living on land'],
    'fish': ['wet scales on the skin', 'gills for gas exchange', 'fins', 'a lateral line'],
    'insects': ['three pairs of jointed legs', 'a body in three parts: head, thorax and abdomen', 'one pair of antennae', 'two pairs of wings in most species'],
    'arachnids': ['four pairs of jointed legs', 'a body in two parts: cephalothorax and abdomen', 'no antennae', 'no wings'],
    'crustaceans': ['more than four pairs of jointed legs', 'two pairs of antennae', 'an exoskeleton hardened with calcium carbonate', 'gas exchange through gills'],
    'myriapods': ['many body segments', 'one or two pairs of legs on each segment', 'one pair of antennae', 'a body not divided into thorax and abdomen'],
    'ferns': ['leaves called fronds', 'spores for reproduction', 'no flowers or seeds', 'roots, stems and leaves with xylem'],
    'flowering plants': ['flowers and seeds for reproduction', 'seeds enclosed in an ovary (fruit)', 'roots, stems and leaves'],
    'monocotyledons': ['one cotyledon in the seed', 'leaves with parallel veins', 'flower parts in multiples of three'],
    'dicotyledons': ['two cotyledons in the seed', 'leaves with branching (net) veins', 'flower parts in multiples of four or five'],
}
GEX = {'mammals': ['bat', 'whale', 'goat'], 'birds': ['penguin', 'ostrich', 'eagle'], 'reptiles': ['crocodile', 'lizard', 'tortoise'], 'amphibians': ['frog', 'newt', 'salamander'],
       'fish': ['shark', 'salmon', 'tuna'], 'insects': ['butterfly', 'locust', 'housefly'], 'arachnids': ['scorpion', 'spider', 'tick'], 'crustaceans': ['crab', 'shrimp', 'woodlouse'],
       'myriapods': ['centipede', 'millipede'], 'ferns': ['bracken', 'tree fern'], 'flowering plants': ['mango tree', 'sunflower'], 'monocotyledons': ['maize', 'rice', 'lily'], 'dicotyledons': ['bean', 'rose', 'oak']}
VERT = ['mammals', 'birds', 'reptiles', 'amphibians', 'fish']
ARTH = ['insects', 'arachnids', 'crustaceans', 'myriapods']

t = T('Kingdoms and main groups: vertebrates, arthropods, plants (ferns, flowering plants)', 'kingdoms and main groups', 'vertebrates', 'arthropods')
facts(t, [('vertebrate', 'an animal with a backbone (vertebral column)'), ('arthropod', 'an invertebrate with jointed legs, a segmented body and an exoskeleton'),
          ('exoskeleton', 'a hard external skeleton made of chitin that supports and protects an arthropod'), ('fern', 'a plant with roots, stems and fronds that reproduces by spores, not seeds'),
          ('monocotyledon', 'a flowering plant with one seed leaf, parallel leaf veins and flower parts in threes'),
          ('dicotyledon', 'a flowering plant with two seed leaves, branching leaf veins and flower parts in fours or fives')])
mcqs(t, [('Which feature is shared by all arthropods?', 'Jointed legs', 'All arthropods have jointed legs, a segmented body and an exoskeleton; wings and antennae vary between groups.', ['Wings', 'Two pairs of antennae', 'A backbone']),
         ('A frog is classified as an amphibian. Which feature does it have?', 'Moist skin without scales', 'Amphibians have moist, scale-free skin used in gas exchange.', ['Dry scaly skin', 'Feathers', 'Fur']),
         ('Which feature distinguishes ferns from flowering plants?', 'Ferns produce spores, not seeds', 'Ferns reproduce by spores from the underside of fronds; flowering plants make seeds in ovaries.', ['Ferns have no roots', 'Ferns have no xylem', 'Ferns have no leaves'])])
shorts(t, [('State three features of insects that are not shared by arachnids.', 'Three pairs of legs, body in three parts (head, thorax, abdomen), antennae (and usually wings).', 'any three [3]'),
           ('Name the five classes of vertebrates.', 'Mammals, birds, reptiles, amphibians and fish.', 'all five [2]; three or four [1] [2]')])
explain(t, [('Explain why a whale is classified as a mammal and not as a fish.', 'It has mammal features: hair (a few bristles), mammary glands producing milk, lungs breathing air, and the young develop in the uterus with a placenta; fish have gills and wet scales.', 'two mammal features [2]; lacks fish features (gills / scales) [1] [3]'),
            ('Explain why a bat is not a bird even though it can fly.', 'It has fur, external ears, gives birth to live young and feeds them milk, which are mammal features; it has no feathers or beak.', 'mammal features named [1]; no feathers / beak [1] [2]'),
            ('Explain why amphibians must return to water to reproduce.', 'Their eggs have no shell and would dry out on land, and the larvae (tadpoles) have gills and live in water.', 'eggs lack shells / would dry out [1]; larvae aquatic with gills [1] [2]'),
            ('Explain how the eggs of reptiles and birds are adapted to development on land.', 'They have a shell (leathery or hard) that reduces water loss and protects the embryo, so they need not be laid in water.', 'shell present [1]; prevents drying / protects embryo [1] [2]'),
            ('Spiders and scorpions are arachnids, not insects. Give two features you could use to show this.', 'They have four pairs of legs (not three) and a body in two parts with no antennae or wings.', 'four pairs of legs [1]; two body parts / no antennae [1] [2]')])
myths(t, [('A spider is an insect because it has jointed legs and an exoskeleton.', 'All arthropods have those features; a spider is an arachnid because it has four pairs of legs and two body sections.'),
           ('Whales and dolphins are fish because they live in water and have fins.', 'They are mammals: they breathe air with lungs, have hair and feed their young on milk.'),
           ('Ferns are flowering plants that have very small flowers.', 'Ferns have no flowers or seeds; they reproduce by spores.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def group_id(r, D):
    pool = r.choice([VERT, ARTH, ['ferns', 'monocotyledons', 'dicotyledons']])
    g = r.choice(pool)
    n = 2 if D <= 2 else 3
    fs = r.sample(GROUPS[g], min(n, len(GROUPS[g])))
    org = r.choice(['An animal', 'An organism', 'A specimen']) if g not in ('ferns', 'monocotyledons', 'dicotyledons') else 'A plant'
    st = f'{org} found near {city(r)} has these features: {"; ".join(fs)}.'
    if D <= 2:
        return MQ(r, st + ' To which group does it belong?', g, [x for x in pool if x != g] + ['molluscs'], f'{cap(g)}: ' + '; '.join(GROUPS[g]) + '.')
    other = r.choice([x for x in pool if x != g])
    ex = r.choice(GEX[g])
    return Q(st + f' (a) Name the group it belongs to. (b) Give one feature that would distinguish it from {other}. (c) Name one other organism in the same group.',
             f'(a) {g} (b) e.g. {GROUPS[g][0]} (not found in {other}) (c) e.g. {ex}', f'(a) {g} [1] (b) a feature of {g} absent in {other}, e.g. {GROUPS[g][0]} [1] (c) correct example such as {ex} [1] [3]', 'short', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def group_case(r, D):
    g1, g2 = r.sample(r.choice([VERT, ARTH]), 2)
    p = person(r)
    a1, a2 = r.sample(GROUPS[g1], 2)
    b1, b2 = r.sample(GROUPS[g2], 2)
    intro = f'On a field trip in {city(r)}, {p} finds two animals. Animal P has {a1} and {a2}. Animal Q has {b1} and {b2}.'
    parts = [lambda r: ('Name the group to which each animal belongs.', f'P: {g1}; Q: {g2}', f'P {g1} [1]; Q {g2} [1] [2]'),
             lambda r: (f'State one feature shared by both animals that places them in the same larger group.', 'Backbone (vertebrates).' if g1 in VERT else 'Jointed legs / exoskeleton / segmented body (arthropods).', '[1]'),
             lambda r: ('Explain why classifying organisms into groups is useful to scientists.', 'It shows how organisms are related (common ancestry), makes identification easier and allows predictions about features of newly found organisms.', 'relationships / evolution [1]; identification or prediction [1] [2]'),
             lambda r: (f'Suggest why a scientist might check the classification of animal Q by comparing DNA as well as visible features.', 'Visible features may be similar because of similar environments (not relationship); DNA base sequences show how closely related organisms are more accurately.', 'features can mislead (convergence) [1]; DNA similarity = relatedness [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Compare the features of a fern and a flowering plant.', 'Both: plants with roots, stems, leaves, chlorophyll and xylem/phloem. Fern: fronds, spores in sporangia under fronds, no flowers, seeds or fruits. Flowering plant: flowers, seeds in ovaries forming fruits, monocots or dicots.',
           'two similarities [2]; three differences [3] [5]'),
          ('Describe the features used to classify vertebrates into five groups.', 'Skin covering (fur, feathers, dry scales, moist skin, wet scales), gas exchange (lungs/gills), eggs (shelled or not / live young), body temperature control, presence of mammary glands / external ears.',
           'one valid feature each for five groups [5]')])
t_c1c = t

# --- DNA classification and five kingdoms
KING = {'animals': ['multicellular', 'cells have no cell wall', 'nucleus present', 'feed on organic molecules made by other organisms', 'many have a nervous system'],
        'plants': ['multicellular', 'cells have cellulose cell walls', 'chloroplasts present: photosynthesise', 'store carbohydrate as starch or sucrose'],
        'fungi': ['usually multicellular threads called hyphae (yeast is single-celled)', 'cell walls made of chitin', 'no chlorophyll', 'feed by extracellular digestion (saprotrophic)', 'store carbohydrate as glycogen'],
        'protoctists': ['mostly single-celled', 'nucleus present', 'some have chloroplasts, some feed like animals'],
        'prokaryotes': ['single-celled', 'no nucleus: circular DNA in the cytoplasm', 'plasmids present', 'cell wall not made of cellulose', 'very small ribosomes']}
KEX = {'animals': ['Amoeba-eating insects', 'a jellyfish'], 'plants': ['a moss', 'a maize plant'], 'fungi': ['a mushroom', 'yeast', 'Mucor (bread mould)'], 'protoctists': ['Amoeba', 'Chlorella', 'Plasmodium'], 'prokaryotes': ['Escherichia coli', 'Lactobacillus']}
t = T('Classification using DNA base sequences; features of the five kingdoms and viruses', 'classification using dna base sequences', 'five kingdoms', 'viruses')
facts(t, [('prokaryote', 'an organism whose single cell has no nucleus; its DNA is free in the cytoplasm'), ('virus', 'a non-cellular particle made of genetic material surrounded by a protein coat'),
          ('hypha', 'a thread-like structure that makes up the body of most fungi'), ('protoctist', 'a mostly single-celled organism with a nucleus that is not an animal, plant or fungus'),
          ('base sequence', 'the order of the bases A, T, C and G along a DNA molecule')])
mcqs(t, [('Which structure is found in all viruses?', 'A protein coat', 'Viruses have a protein coat around genetic material (DNA or RNA); they have no cytoplasm, ribosomes or cell membrane.', ['A cell membrane', 'Ribosomes', 'A nucleus']),
         ('Which kingdom contains organisms with cell walls made of chitin?', 'Fungi', 'Fungal walls are chitin; plant walls are cellulose.', ['Plants', 'Prokaryotes', 'Protoctists']),
         ('Why are viruses not placed in any of the five kingdoms?', 'They are not made of cells', 'Viruses are non-cellular and can only reproduce inside host cells.', ['They are too small to see', 'They contain DNA', 'They cause disease'])])
shorts(t, [('State two features of viruses.', 'Protein coat; genetic material (DNA or RNA); no cell structures; reproduce only inside living cells.', 'any two [2]'),
           ('State two features shown by all fungi.', 'No chlorophyll / cannot photosynthesise; cell walls of chitin; feed by extracellular digestion; store glycogen.', 'any two [2]')])
explain(t, [('Explain why DNA base sequences are used to classify organisms.', 'Closely related species share a recent common ancestor, so their DNA base sequences are more similar; the number of differences shows how closely related they are and can correct mistakes from visible features.', 'related organisms have similar sequences [1]; fewer differences = more recent common ancestor [1] [2]'),
            ('Explain why fungi were moved out of the plant kingdom.', 'Fungi have no chlorophyll and cannot photosynthesise, have cell walls of chitin not cellulose, and feed by extracellular digestion; DNA evidence shows they are a separate group.', 'two differences from plants [2]'),
            ('Explain why viruses are described as being on the boundary of living and non-living.', 'They contain genetic material and reproduce, but only inside a host cell; outside cells they show no respiration, nutrition, excretion or growth.', 'reproduce only in host cells [1]; do not show other characteristics on their own [1] [2]'),
            ('Compare the structure of a prokaryotic cell and a cell from the plant kingdom.', 'Both have a cell membrane, cytoplasm, cell wall and ribosomes. Prokaryote: no nucleus (circular DNA, plasmids), no chloroplasts or mitochondria, wall not cellulose. Plant: nucleus, chloroplasts, mitochondria, cellulose wall, vacuole.', 'one similarity [1]; two differences [2] [3]')])
myths(t, [('Viruses are the smallest type of bacteria.', 'Viruses are not cells at all; bacteria are prokaryotic cells.'),
           ('Mushrooms are plants because they grow in soil and do not move.', 'Mushrooms are fungi: they have no chlorophyll, cell walls of chitin and feed by extracellular digestion.'),
           ('Two species that look alike must be closely related.', 'Similar appearance can result from similar environments; DNA base sequences show relationships more reliably.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def dna_compare(r, D):
    L = 12 if D <= 2 else 16 if D <= 4 else 20
    ref = ''.join(r.choice('ATCG') for _ in range(L))
    sp = r.sample(['B', 'C', 'D', 'E'], 3)
    diffs = r.sample(range(1, 7), 3)
    seqs = {}
    for s, n in zip(sp, diffs):
        pos = r.sample(range(L), n)
        q = list(ref)
        for i in pos:
            q[i] = r.choice([b for b in 'ATCG' if b != ref[i]])
        seqs[s] = ''.join(q)
    best = min(sp, key=lambda s: sum(a != b for a, b in zip(ref, seqs[s])))
    nd = {s: sum(a != b for a, b in zip(ref, seqs[s])) for s in sp}
    tab = '; '.join(f'species {s}: {seqs[s]}' for s in sp)
    st = f'Part of the same gene was sequenced in four species. Species A: {ref}; {tab}.'
    if D == 1:
        return MQ(r, st + ' Which species is most closely related to species A?', f'Species {best}', [f'Species {s}' for s in sp if s != best] + ['Species A'], 'Differences from A: ' + ', '.join(f'{s} = {nd[s]}' for s in sp) + '; fewest differences = closest relationship.')
    pre = '(a) ' if D >= 3 else ''
    ans = pre + 'Differences from A: ' + ', '.join(f'{s} {nd[s]}' for s in sp) + f'. Species {best} is most closely related.'
    key = pre + 'counts differences correctly [1]; ' + f'species {best} (fewest differences) [1]'
    m = 2
    if D >= 3:
        pc = (L - nd[best]) / L * 100
        st += f' (a) Identify the species most closely related to A, showing your working. (b) Calculate the percentage of bases in species {best} that are the same as in species A.'
        ans += f' (b) {fx(pc, 1)}%'
        key += f' (b) ({L} − {nd[best]}) ÷ {L} × 100 = {fx(pc, 1)}% [1]'
        m = 3
    else:
        st += ' Identify the species most closely related to species A. Show your working.'
    if D >= 4:
        st += ' (c) Explain why comparing DNA is more reliable than comparing visible features.'
        ans += ' (c) DNA differences reflect how recently species shared a common ancestor; visible features can be similar for other reasons.'
        key += ' (c) DNA reflects common ancestry / features can evolve similarly in similar habitats [1]'
        m += 1
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (1, 2, 3), 'short')
def kingdom_id(r, D):
    k = r.choice(list(KING))
    fs = r.sample(KING[k], 2 if D <= 2 else 3)
    st = f'An organism has these features: {"; ".join(fs)}.'
    if D <= 2:
        return MQ(r, st + ' To which kingdom does it belong?', k, [x for x in KING if x != k], f'{cap(k)}: ' + '; '.join(KING[k]) + '.')
    other = r.choice([x for x in KING if x != k])
    return Q(st + f' Name the kingdom and state one feature that distinguishes it from {other}.', f'{cap(k)}; e.g. {KING[k][1]}.', f'{k} [1]; a valid distinguishing feature [1] [2]', 'short', 2)


@t.add('C4', (3, 4, 5), 'multi_step')
def dna_case(r, D):
    names = r.choice(['bird', 'frog', 'beetle', 'orchid'])
    p = person(r)
    a, b, c = sorted(r.sample(range(2, 30), 3))
    L = r.sample('XYZ', 3)
    P1, P2, P3 = (L[0] + L[1]), (L[0] + L[2]), (L[1] + L[2])
    intro = f'{p} compares a 200-base section of DNA from three {names} species, X, Y and Z, found in different valleys near {city(r)}. ' + cap('; '.join(sorted([f'{P1[0]} and {P1[1]} differ at {a} bases', f'{P2[0]} and {P2[1]} differ at {c} bases', f'{P3[0]} and {P3[1]} differ at {b} bases']))) + f'. {P2[0]} and {P2[1]} look very similar; {L[1]} looks different.'
    parts = [lambda r: ('State which two species are most closely related. Explain your answer.', f'{P1[0]} and {P1[1]}: fewest base differences ({a}).', f'{P1[0]} and {P1[1]} [1]; fewest differences / most similar sequence [1] [2]'),
             lambda r: (f'Calculate the percentage difference between the DNA of {P2[0]} and {P2[1]}.', f'{fx(c / 200 * 100, 2)}%', f'{c} ÷ 200 × 100 [1] = {fx(c / 200 * 100, 2)}% [1] [2]'),
             lambda r: (f'Suggest why {P2[0]} and {P2[1]} look similar even though they are less closely related.', 'They live in similar habitats, so similar features were selected (convergence); appearance does not always show relationship.', 'similar environment / selection pressures [1]; visible features not reliable [1] [2]'),
             lambda r: ('Evaluate the use of DNA evidence in classification compared with visible features.', 'DNA gives a quantitative, objective measure of relatedness and can show relationships hidden by appearance, but a short section may not represent the whole genome and sequencing costs money; best used with other evidence.', 'one advantage [1]; one limitation [1]; conclusion [1] [3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the main features of the five kingdoms of living organisms.', 'Animals: multicellular, no walls, nervous coordination, heterotrophic. Plants: multicellular, cellulose walls, chloroplasts. Fungi: hyphae, chitin walls, saprotrophic. Protoctists: mostly single-celled with nucleus. Prokaryotes: no nucleus, circular DNA, plasmids.',
           'one correct distinguishing feature for each of five kingdoms [5]')])
t_c1d = t
CHAPTERS[1] = [t_c1a, t_c1b, t_c1c, t_c1d]


# ===================================================================== 2 Organisation of the organism
ORG = {'nucleus': ('contains the genetic material (chromosomes made of DNA) that controls the activities of the cell', {'animal', 'plant'}),
       'cell membrane': ('controls the movement of substances into and out of the cell (partially permeable)', {'animal', 'plant', 'bacterial'}),
       'cytoplasm': ('jelly-like fluid where most of the chemical reactions of the cell take place', {'animal', 'plant', 'bacterial'}),
       'cell wall': ('surrounds the cell membrane; strengthens and supports the cell and stops it bursting', {'plant', 'bacterial'}),
       'chloroplast': ('contains chlorophyll, which absorbs light energy for photosynthesis', {'plant'}),
       'large permanent vacuole': ('contains cell sap; keeps the cell turgid and stores dissolved substances', {'plant'}),
       'mitochondrion': ('site of aerobic respiration, which releases energy for the cell', {'animal', 'plant'}),
       'ribosome': ('site of protein synthesis', {'animal', 'plant', 'bacterial'}),
       'circular DNA': ('a single loop of DNA free in the cytoplasm that carries the genes of a bacterium', {'bacterial'}),
       'plasmid': ('a small extra ring of DNA in a bacterial cell, carrying a few genes', {'bacterial'})}
CELLSRC = {'animal': ['cheek cells from the lining of the mouth', 'cells from a liver sample', 'a white blood cell from a blood smear'],
           'plant': ['a palisade cell from a leaf', 'a cell from the epidermis of an onion bulb', 'a cell from a moss leaf'],
           'bacterial': ['a cell from a sample of yoghurt', 'a cell from a culture of soil bacteria']}
t = T('Structure of animal, plant and bacterial cells and functions of their parts', 'structure of animal, plant and bacterial cells', 'cell structure')
facts(t, [(k, v[0]) for k, v in ORG.items() if k not in ('circular DNA',)])
mcqs(t, [('Which structures are found in both plant cells and bacterial cells?', 'Cell wall, cell membrane and ribosomes', 'Bacteria and plants both have walls (different materials), membranes, cytoplasm and ribosomes; bacteria lack a nucleus, mitochondria and chloroplasts.',
          ['Nucleus, cell wall and chloroplasts', 'Mitochondria, ribosomes and vacuole', 'Plasmids, nucleus and cell membrane']),
         ('Which structure is present in a cheek cell but absent from a bacterial cell?', 'Nucleus', 'Bacteria are prokaryotes: no nucleus or mitochondria.', ['Cell membrane', 'Ribosome', 'Cytoplasm']),
         ('A cell has a cell wall, chloroplasts and a large vacuole. What type of cell is it?', 'A plant cell', 'Chloroplasts and a permanent vacuole are found only in plant cells (of these types).', ['An animal cell', 'A bacterial cell', 'A red blood cell'])])
shorts(t, [('State three structures found in plant cells but not in animal cells.', 'Cell wall, chloroplasts, large permanent vacuole.', 'all three [2]; two [1] [2]'),
           ('State two structures found only in bacterial cells.', 'Circular DNA (not in a nucleus) and plasmids.', 'circular DNA [1]; plasmids [1] [2]')])
explain(t, [('Root hair cells are plant cells but they have no chloroplasts. Explain why.', 'They are underground, so they receive no light and cannot photosynthesise; chloroplasts would be of no use.', 'no light reaches roots [1]; chloroplasts only needed for photosynthesis [1] [2]'),
            ('Explain why a plant cell placed in water does not burst, but an animal cell may.', 'The plant cell wall is strong and resists further expansion as the cell becomes turgid; animal cells have only a cell membrane, which bursts.', 'cell wall resists expansion [1]; animal cell has no wall [1] [2]'),
            ('Explain why cells that need a lot of energy, such as muscle cells, contain many mitochondria.', 'Mitochondria are the site of aerobic respiration, which releases energy; more mitochondria allow more respiration and more energy release.', 'mitochondria = aerobic respiration [1]; more energy released for contraction [1] [2]'),
            ('Describe how you would prepare a slide of onion epidermis cells to view with a light microscope.', 'Peel a thin layer of epidermis, place it flat in a drop of water or iodine on a slide, lower a coverslip at an angle to avoid air bubbles, then view on low power first.', 'thin layer [1]; stain (iodine) [1]; coverslip lowered at angle [1] [3]'),
            ('Explain why iodine solution is added to onion cells before viewing them.', 'It stains the nucleus and cytoplasm (and starch) so that the cell structures can be seen more clearly; the cells are almost colourless otherwise.', 'stain gives contrast [1]; makes nucleus / cell parts visible [1] [2]'),
            ('Explain why the cell membrane is described as partially permeable.', 'It lets some substances (such as water, oxygen and glucose) pass through but stops others, such as large molecules, so it controls what enters and leaves the cell.', 'some substances pass, others do not [1]; controls entry and exit [1] [2]')])
myths(t, [('All plant cells contain chloroplasts.', 'Only cells that receive light, such as palisade and spongy mesophyll cells, contain chloroplasts; root cells do not.'),
           ('Bacteria have a nucleus but it is very small.', 'Bacteria have no nucleus; their DNA is a circular loop free in the cytoplasm.'),
           ('The cell wall controls what enters and leaves a plant cell.', 'The cell wall is fully permeable; the cell membrane controls movement of substances.'),
           ('Animal cells do not have mitochondria because only plant cells respire.', 'Animal and plant cells both contain mitochondria and respire aerobically.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def cell_id(r, D):
    kind = r.choice(list(CELLSRC))
    present = [k for k, v in ORG.items() if kind in v[1]]
    absent = [k for k, v in ORG.items() if kind not in v[1]]
    must = {'animal': (r.choice(['nucleus', 'mitochondrion']), 'cell wall'), 'plant': (r.choice(['chloroplast', 'large permanent vacuole']), 'circular DNA'),
            'bacterial': (r.choice(['circular DNA', 'plasmid']), 'nucleus')}[kind]
    seen = [must[0]] + r.sample([x for x in present if x != must[0]], min(len(present) - 1, 2 if D <= 2 else 3))
    abs_ = [must[1]] + r.sample([x for x in absent if x != must[1]], 1)
    r.shuffle(seen)
    reason = {'animal': f'it has a {must[0]} but no cell wall', 'plant': f'it has a {must[0]} and a nucleus' if must[0] != 'nucleus' else 'it has a cell wall and nucleus',
              'bacterial': f'it has {"a plasmid" if must[0] == "plasmid" else "circular DNA"} and no nucleus'}[kind]
    st = f'A cell is examined under a microscope. Structures seen: {", ".join(seen)}. Structures not present: {", ".join(abs_)}.'
    if D <= 2:
        return MQ(r, st + ' What type of cell is it?', f'A {kind} cell', ['A plant cell', 'An animal cell', 'A bacterial cell', 'A virus'], f'Present {", ".join(seen)} and absent {", ".join(abs_)} → {kind} cell.')
    src = r.choice(CELLSRC[kind])
    func = r.choice(seen)
    return Q(st + f' (a) Identify the type of cell and give a reason. (b) State the function of the {func}. (c) Suggest which of these samples it came from: {", ".join(r.sample([s for k in CELLSRC for s in CELLSRC[k] if k != kind], 2) + [src])}.',
             f'(a) {kind} cell: {reason}. (b) {cap(ORG[func][0])}. (c) {src}', f'(a) {kind} [1] with reason from structures [1] (b) {ORG[func][0]} [1] (c) {src} [1] [4]', 'short', 4)


@t.add('C3', (2, 3), 'short')
def cell_func(r, D):
    ks = r.sample(list(ORG), 3)
    labs = ['(i)', '(ii)', '(iii)']
    st = 'State the function of each cell structure: ' + ' '.join(f'{labs[i]} {k}' for i, k in enumerate(ks)) + '.'
    if D >= 3:
        st += ' For each one, name a type of cell (animal, plant or bacterial) in which it is found.'
    return Q(st, ' '.join(f'{labs[i]} {ORG[k][0]}' + (f' ({"/".join(sorted(ORG[k][1]))})' if D >= 3 else '') for i, k in enumerate(ks)),
             '; '.join(f'{labs[i]} {ORG[k][0]} [1]' for i, k in enumerate(ks)) + (' ; one correct cell type each [1]' if D >= 3 else '') + f' [{3 + (1 if D >= 3 else 0)}]', 'short', 3 + (1 if D >= 3 else 0))


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def cell_slide(r, D):
    p = person(r)
    tissue = r.choice([('onion epidermis', 'iodine solution', 'plant'), ('cheek cells', 'methylene blue', 'animal'), ('a moss leaf', 'water only', 'plant'), ('rhubarb epidermis', 'water only', 'plant')])
    intro = f'{p} prepares a slide of {tissue[0]} using {tissue[1]} and observes it with a light microscope in a school laboratory in {city(r)}.'
    vis = [k for k in ('nucleus', 'cell membrane', 'cytoplasm', 'cell wall', 'large permanent vacuole', 'chloroplast') if tissue[2] in ORG[k][1] and not (k == 'chloroplast' and 'onion' in tissue[0])]
    parts = [lambda r: ('Describe how the slide should be prepared.', 'Thin layer of cells on slide, drop of stain/water, coverslip lowered at an angle to avoid air bubbles, blot excess.', 'thin layer / single layer of cells [1]; add stain [1]; coverslip at angle to avoid bubbles [1] [3]'),
             lambda r: ('Name three structures that should be visible in these cells with a light microscope.', ', '.join(vis[:3]) + '.', f'any three from: {", ".join(vis)} [3]'),
             lambda r: ('State two rules for making a biological drawing of the cells.', 'Use a sharp pencil with clear continuous lines, no shading; draw large, label with ruled lines, include a title and magnification.', 'any two rules [2]'),
             lambda r: ('Explain why ribosomes cannot be seen in these cells with this microscope.', 'Ribosomes are too small; the light microscope does not have a high enough resolution (an electron microscope is needed).', 'too small [1]; need electron microscope / higher resolution [1] [2]'),
             lambda r: ('Explain why the cells must be a thin layer.', 'Light must pass through the specimen; a thin layer means cells do not overlap so individual structures can be seen.', 'light passes through [1]; cells do not overlap [1] [2]')]
    if tissue[2] == 'plant':
        parts.append(lambda r: ('Explain how the cells can be identified as plant cells.', 'They have a cell wall (regular shape) and a large permanent vacuole' + (', and chloroplasts' if 'chloroplast' in vis else '') + '.', 'two plant-only structures [2]'))
    else:
        parts.append(lambda r: ('Explain how the cells can be identified as animal cells.', 'They have no cell wall (irregular shape), no large vacuole and no chloroplasts.', 'two absent plant structures [2]'))
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Compare the structure of a palisade mesophyll cell with the structure of a bacterial cell.', 'Both: cell wall (cellulose in palisade, not cellulose in bacteria), cell membrane, cytoplasm, ribosomes. Palisade: nucleus, chloroplasts, mitochondria, large vacuole. Bacterium: no nucleus, circular DNA and plasmids, no chloroplasts or mitochondria, much smaller.',
           'two similarities [2]; three differences [3] [5]'),
          ('Describe the functions of the parts of a plant cell that are not found in animal cells.', 'Cell wall: made of cellulose, supports the cell, prevents bursting. Chloroplasts: contain chlorophyll, absorb light for photosynthesis. Large permanent vacuole: contains cell sap, keeps cell turgid, stores sugars and salts.', 'three structures named [1]; correct function each [3] [4]')])
t_c2a = t

SPEC = [('ciliated cell', 'cilia (tiny hairs) on its surface', 'moves mucus, which traps dust and pathogens, up the trachea and bronchi'),
        ('root hair cell', 'a long extension that increases the surface area', 'absorbs water and mineral ions from the soil'),
        ('palisade mesophyll cell', 'many chloroplasts near the upper surface of the leaf', 'carries out photosynthesis'),
        ('neurone', 'a long axon that carries impulses', 'conducts electrical impulses around the body'),
        ('red blood cell', 'no nucleus, a biconcave shape and haemoglobin', 'transports oxygen'),
        ('sperm cell', 'a flagellum and many mitochondria', 'swims to the egg and fertilises it'),
        ('egg cell', 'a large cytoplasm containing energy stores (jelly coat)', 'is fertilised and provides nutrients for the early embryo')]
LEVELS = {'cell': ['a red blood cell', 'a root hair cell', 'a sperm cell', 'a neurone', 'a guard cell'],
          'tissue': ['xylem', 'muscle tissue in the stomach wall', 'palisade mesophyll', 'blood', 'epithelium lining the trachea'],
          'organ': ['the heart', 'a leaf', 'the stomach', 'the kidney', 'the brain', 'a root'],
          'organ system': ['the digestive system', 'the circulatory system', 'the nervous system', 'the breathing system', 'a shoot system']}
t = T('Specialised cells, tissues, organs and organ systems', 'specialised cells', 'tissues, organs and organ systems')
facts(t, [('tissue', 'a group of cells with similar structures, working together to perform a shared function'), ('organ', 'a structure made of a group of tissues working together to perform specific functions'),
          ('organ system', 'a group of organs with related functions, working together to perform body functions'), ('specialised cell', 'a cell whose structure is adapted to carry out a particular function'),
          ('organism', 'a living thing made of one or more organ systems working together')])
mcqs(t, [('Which list shows the levels of organisation in the correct order, from smallest to largest?', 'cell → tissue → organ → organ system', 'Cells form tissues, tissues form organs, organs form organ systems.',
          ['tissue → cell → organ → organ system', 'cell → organ → tissue → organ system', 'organ → tissue → cell → organ system']),
         ('Which cell has a biconcave shape and no nucleus?', 'Red blood cell', 'More room for haemoglobin, larger surface area for diffusion of oxygen.', ['White blood cell', 'Neurone', 'Ciliated cell']),
         ('Which is an example of a tissue?', 'Xylem', 'Xylem is a group of similar cells working together to transport water; a leaf is an organ.', ['A leaf', 'A root hair cell', 'The circulatory system'])])
shorts(t, [('Name two specialised cells found in plants and state the function of each.', 'Root hair cell: absorbs water and mineral ions; palisade mesophyll cell: photosynthesis.', 'each cell with correct function [2]'),
           ('State what is meant by a specialised cell and give one example.', 'A cell adapted in structure for a particular function, e.g. red blood cell transporting oxygen.', 'definition [1]; example with function [1] [2]')])
explain(t, [('Explain how the structure of a red blood cell is adapted to its function.', 'No nucleus leaves more room for haemoglobin; biconcave shape gives a large surface area for oxygen diffusion; small and flexible to squeeze through capillaries.', 'two features linked to function [2] [2]'),
            ('Explain why a sperm cell contains many mitochondria.', 'Mitochondria carry out aerobic respiration, releasing energy for the flagellum to swim to the egg.', 'respiration releases energy [1]; for swimming / flagellum movement [1] [2]'),
            ('Explain how a root hair cell is adapted for absorbing water.', 'The long hair-like extension gives a large surface area for osmosis and active uptake of ions; thin wall; no chloroplasts needed.', 'large surface area [1]; linked to faster uptake [1] [2]'),
            ('Explain why the stomach is described as an organ.', 'It is made of several different tissues (muscle, glandular epithelium, connective tissue) working together to perform a function (digestion).', 'several tissues [1]; working together for a function [1] [2]'),
            ('Explain the role of ciliated cells in protecting the lungs.', 'Cilia beat to sweep mucus, which has trapped dust and pathogens, up and out of the airways so they do not reach the alveoli.', 'cilia move mucus [1]; removes trapped pathogens / dust [1] [2]'),
            ('Explain how the structure of a neurone is adapted to conduct impulses.', 'It has a long axon to carry impulses over long distances and many branched endings (dendrites) that connect with other neurones.', 'long axon [1]; many connections [1] [2]')])
myths(t, [('The heart is a tissue because it is made of muscle.', 'The heart is an organ: it contains several tissues, such as muscle, nervous and connective tissue.'),
           ('Red blood cells have a large nucleus to control oxygen transport.', 'Red blood cells have no nucleus, which leaves more space for haemoglobin.'),
           ('A tissue is a group of different organs working together.', 'A tissue is a group of similar cells working together; organs are made of tissues.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def spec_id(r, D):
    c, f, fn = r.choice(SPEC)
    if D <= 2:
        return MQ(r, f'A cell has {f}. Its function is that it {fn}. Which cell is it?', cap(c), [cap(x[0]) for x in SPEC if x[0] != c], f'{cap(c)}: {f} — adaptation for: {fn}.')
    c2, f2, fn2 = r.choice([x for x in SPEC if x[0] != c])
    return Q(f'Specialised cells have features related to their functions. (a) Name the cell that {fn} and describe one adaptation it has. (b) Describe how one feature of a {c2} is related to its function.',
             f'(a) {c}: {f}. (b) {cap(f2)}, so it {fn2}.', f'(a) {c} [1]; adaptation: {f} [1] (b) feature [1] linked to function: {fn2} [1] [4]', 'short', 4)


@t.add('C3', (1, 2, 3), 'short')
def level_sort(r, D):
    items = []
    for lv in LEVELS:
        items.append((r.choice(LEVELS[lv]), lv))
    r.shuffle(items)
    if D <= 1:
        x, lv = items[0]
        return MQ(r, f'Which level of organisation is {x}?', lv, list(LEVELS), f'{cap(x)} is an example of {"an" if lv[0] == "o" else "a"} {lv}.')
    labs = ['(i)', '(ii)', '(iii)', '(iv)']
    return Q('State whether each is a cell, a tissue, an organ or an organ system. ' + ' '.join(f'{labs[i]} {x}' for i, (x, _) in enumerate(items)) + '.',
             ' '.join(f'{labs[i]} {lv}' for i, (_, lv) in enumerate(items)), '; '.join(f'{labs[i]} {lv}' for i, (_, lv) in enumerate(items)) + ' (four correct [3]; three [2]; two [1]) [3]', 'short', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def spec_case(r, D):
    c, f, fn = r.choice(SPEC)
    intro = f'{person(r)} is studying a {c} using a microscope and an electron micrograph. The cell {fn}.'
    parts = [lambda r: (f'Describe one structural feature of the {c} that adapts it to this function.', cap(f) + '.', '[1] feature; [1] linked to function [2]'),
             lambda r: ('Name the next level of organisation formed when many of these cells work together, and give an example.', 'A tissue, e.g. ' + {'ciliated cell': 'ciliated epithelium', 'root hair cell': 'root epidermis', 'palisade mesophyll cell': 'palisade mesophyll tissue', 'neurone': 'nervous tissue',
                         'red blood cell': 'blood', 'sperm cell': 'testis tissue', 'egg cell': 'ovary tissue'}[c] + '.', 'tissue [1]; example [1] [2]'),
             lambda r: (f'Suggest what would happen to the function of the {c} if this feature were missing.', f'It would be less able to carry out its function ({fn}) efficiently.', 'reduced efficiency linked to feature [2]'),
             lambda r: ('Explain why multicellular organisms need specialised cells, while single-celled organisms do not.', 'In large organisms most cells are far from the surface and many functions are needed; division of labour lets cells become efficient at one job. A single cell must carry out all processes itself.', 'division of labour / efficiency [1]; large organisms need different functions in different places [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Using named examples, explain the differences between a cell, a tissue, an organ and an organ system.', 'Cell: basic unit, e.g. muscle cell. Tissue: group of similar cells with a shared function, e.g. muscle tissue. Organ: several tissues working together, e.g. heart. Organ system: organs with related functions, e.g. circulatory system.', 'each level defined with example [4] [4]'),
          ('Describe how the structures of a ciliated cell, a red blood cell and a sperm cell are adapted to their functions.', 'Ciliated: cilia beat to move mucus. RBC: no nucleus, biconcave, haemoglobin for oxygen transport. Sperm: flagellum to swim, mitochondria for energy, acrosome enzymes to digest egg coat.', 'one adaptation linked to function for each cell [3]; extra detail [2] [5]')])
t_c2b = t

# --- magnification
SPECIMENS = [('a cheek cell', 40, 70, 'μm'), ('a red blood cell', 6, 9, 'μm'), ('a palisade cell', 40, 80, 'μm'), ('a pollen grain', 20, 60, 'μm'), ('an onion epidermal cell', 150, 300, 'μm'),
             ('a bacterium', 1, 5, 'μm'), ('a chloroplast', 3, 8, 'μm'), ('a mitochondrion', 1, 3, 'μm'), ('a paramecium', 120, 250, 'μm'), ('a flea', 1.5, 3.3, 'mm'), ('an ant head', 0.8, 2, 'mm'),
             ('a root hair', 200, 900, 'μm'), ('a stoma (guard cell pair)', 25, 45, 'μm'), ('an amoeba', 250, 600, 'μm')]


def mag_parts(r, D):
    name, lo, hi, u = r.choice(SPECIMENS)
    actual = round(r.uniform(lo, hi), 1 if hi < 10 else 0)
    actual_um = actual * (1000 if u == 'mm' else 1)
    M = r.choice([x for x in (40, 50, 100, 200, 250, 400, 500, 1000, 1500, 2000, 2500, 4000, 5000, 10000) if 8 <= actual_um * x / 1000 <= 160] or [None])
    if M is None:
        return None
    img = actual_um * M / 1000  # mm
    img = round(img, 0 if img >= 20 else 1)
    act = img * 1000 / M
    return name, img, M, act, u


def mag_actual(r, D):
    x = mag_parts(r, D)
    if not x:
        return None
    name, img, M, act, u = x
    if D == 1:
        return NQ(r, f'An image of {name} is {fx(img)} mm long at a magnification of ×{M}. What is the actual length?', act, [act * 1000, act / 1000, img * M, img / M * 10], ' μm',
                  f'actual = image ÷ magnification = {fx(img)} mm ÷ {M} = {fx(img / M, 5)} mm = {sf(act)} μm.', f=lambda v: sf(v, 3))
    st = f'A drawing of {name} has a length of {fx(img)} mm. The magnification of the drawing is ×{M}. Calculate the actual length of {name} in micrometres (μm).'
    key = f'actual size = image size ÷ magnification [1]; {fx(img)} ÷ {M} = {sf(img / M, 3)} mm [1]; × 1000 = {sf(act, 3)} μm [1] [3]'
    m = 3
    if D >= 4:
        st += ' Show your working.'
    if D >= 5:
        st = st.replace('Calculate the actual length', 'Calculate the actual length').replace(' Show your working.', ' Give your answer to an appropriate number of significant figures and show your working.')
    return Q(st, f'{sf(act, 3)} μm', key, 'numerical', m)


def mag_M(r, D):
    x = mag_parts(r, D)
    if not x:
        return None
    name, img, M, act, u = x
    au = f'{sf(act, 3)} μm' if r.random() < 0.6 or act < 1000 else f'{sf(act / 1000, 3)} mm'
    if D == 1:
        return NQ(r, f'{cap(name)} with an actual length of {au} appears {fx(img)} mm long in a photograph. What is the magnification?', M, [M / 10, M * 10, M / 1000, act / img], '', f'M = image ÷ actual = {fx(img * 1000)} μm ÷ {sf(act, 3)} μm = ×{M}.', f=lambda v: '×' + sf(v, 3))
    st = f'{person(r)} photographs {name} through a microscope. The image is {fx(img)} mm long and the actual length is {au}. Calculate the magnification of the image.'
    if D >= 3:
        st += ' State the formula you use.'
    return Q(st, f'×{M}', f'magnification = image size ÷ actual size [1]; convert to same units: {fx(img)} mm = {fx(img * 1000)} μm [1]; {fx(img * 1000)} ÷ {sf(act, 3)} = ×{M} [1] [3]', 'numerical', 3)


def mag_scale(r, D):
    x = mag_parts(r, D)
    if not x:
        return None
    name, img, M, act, u = x
    bar_um = r.choice([v for v in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000) if 5 <= v * M / 1000 <= 60] or [None])
    if bar_um is None:
        return None
    bar_mm = bar_um * M / 1000
    st = f'A micrograph of {name} has a scale bar labelled {bar_um} μm. The scale bar measures {fx(bar_mm)} mm on the page and the image of {name} measures {fx(img)} mm. (a) Calculate the magnification of the micrograph. (b) Calculate the actual length of {name}.'
    return Q(st, f'(a) ×{M} (b) {sf(act, 3)} μm', f'(a) {fx(bar_mm)} mm = {fx(bar_mm * 1000)} μm; {fx(bar_mm * 1000)} ÷ {bar_um} = ×{M} [2] (b) {fx(img * 1000)} μm ÷ {M} = {sf(act, 3)} μm [2]', 'numerical', 4)


def mag_units(r, D):
    v = r.choice([0.05, 0.2, 0.35, 1.5, 2.4, 0.008, 0.75, 3.2, 0.012])
    to_um = r.random() < 0.6
    if to_um:
        c = v * 1000
        return NQ(r, f'Convert {fx(v, 3)} mm into micrometres (μm).', c, [v * 100, v * 10, v / 1000, v * 10000], ' μm', f'1 mm = 1000 μm, so {fx(v, 3)} × 1000 = {sf(c)} μm.', f=lambda z: fx(z, 6))
    um = v * 1000
    return NQ(r, f'Convert {fx(um, 3)} μm into millimetres.', v, [um / 100, um * 1000, um / 10, v * 10], ' mm', f'1 μm = 0.001 mm, so {fx(um, 3)} ÷ 1000 = {fx(v, 4)} mm.', f=lambda z: fx(z, 6))


t = T('Magnification calculations and converting between mm and μm', 'magnification calculations', 'converting between mm and μm')
t.templates += [x for x in [Tpl('C3', (1, 2, 3, 4, 5), mag_actual, 'numerical', 'mag_actual'), Tpl('C3', (1, 2, 3, 4), mag_M, 'numerical', 'mag_M'),
                            Tpl('C3', (2, 3, 4, 5), mag_scale, 'numerical', 'mag_scale'), Tpl('C1', (1, 2, 3), mag_units, 'mcq', 'mag_units')]]
facts(t, [('magnification', 'how many times larger an image is than the real object (image size ÷ actual size)'), ('micrometre', 'one thousandth of a millimetre (1 μm = 0.001 mm)'),
          ('scale bar', 'a line on a micrograph labelled with the actual length it represents'), ('resolution', 'the ability to distinguish two points that are close together as separate'),
          ('electron micrograph', 'an image produced using an electron microscope, showing more detail than a light microscope')])
shorts(t, [('Write the formula linking magnification, image size and actual size.', 'magnification = image size ÷ actual size', 'correct formula [1]'),
           ('State how many micrometres there are in one millimetre.', '1000 μm', '[1]'),
           ('State why image size and actual size must be in the same units before calculating magnification.', 'Magnification has no units; it is a ratio, so both lengths must be in the same unit or the answer is wrong by a factor (e.g. 1000).', 'ratio / no units [1]; same units avoids factor of 1000 error [1] [2]')])
explain(t, [('A student calculates that a cheek cell 8 mm long in a drawing at ×160 has an actual size of 0.05 μm. Explain the error and give the correct answer.', 'They divided correctly (8 ÷ 160 = 0.05) but the answer is in mm, not μm; 0.05 mm = 50 μm.', 'answer is in mm [1]; correct value 50 μm [1] [2]'),
            ('Explain why a scale bar is often more useful than a stated magnification on a printed micrograph.', 'If the image is enlarged or reduced when printed or on screen, the scale bar changes size with the image, so it still gives the correct scale; a stated magnification would then be wrong.', 'image size may change [1]; scale bar changes with it [1] [2]'),
            ('Explain why ribosomes can be seen in electron micrographs but not with a light microscope.', 'Electron microscopes have a much higher resolution (and magnification), so very small structures such as ribosomes can be distinguished.', 'higher resolution [1]; ribosomes too small for light microscope [1] [2]'),
            ('Describe how you would estimate the actual width of a cell using a light microscope and a ruler or eyepiece graticule.', 'Calibrate the graticule with a stage micrometer (or measure the field of view), count the divisions across the cell, convert divisions to μm using the calibration, repeat for several cells and find the mean.', 'calibrate [1]; measure divisions [1]; convert and average several cells [1] [3]')])
myths(t, [('To find the actual size you multiply the image size by the magnification.', 'Actual size = image size ÷ magnification.'),
           ('1 mm is equal to 100 μm.', '1 mm = 1000 μm.'),
           ('Magnification should be given in mm because the image was measured in mm.', 'Magnification is a ratio with no units, written as ×number.')])


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def mag_case(r, D):
    x = mag_parts(r, D)
    y = mag_parts(r, D)
    if not x or not y or x[0] == y[0]:
        return None
    name, img, M, act, u = x
    n2, img2, M2, act2, u2 = y
    intro = f'{person(r)} makes a drawing of {name} from a microscope slide. The drawing is {fx(img)} mm long and the actual length is {sf(act, 3)} μm. A textbook micrograph of {n2} is {fx(img2)} mm long at ×{M2}.'
    parts = [lambda r: ('Calculate the magnification of the drawing.', f'×{sf(img * 1000 / act, 3)}', f'convert {fx(img)} mm to {fx(img * 1000)} μm [1]; ÷ {sf(act, 3)} = ×{sf(img * 1000 / act, 3)} [1] [2]'),
             lambda r: (f'Calculate the actual length of {n2} in μm.', f'{sf(act2, 3)} μm', f'{fx(img2)} ÷ {M2} = {sf(img2 / M2, 3)} mm [1]; × 1000 = {sf(act2, 3)} μm [1] [2]'),
             lambda r: ('Calculate how many times longer the larger specimen is than the smaller one.', f'{sf(max(act, act2) / min(act, act2), 3)} times', f'{sf(max(act, act2), 3)} ÷ {sf(min(act, act2), 3)} = {sf(max(act, act2) / min(act, act2), 3)} [2]'),
             lambda r: ('Suggest why measuring several specimens and calculating a mean gives a better estimate of actual size.', 'Individual cells vary in size and measurements have errors; a mean of several reduces the effect of unusual cells and random error.', 'variation between specimens [1]; mean reduces effect of random error [1] [2]'),
             lambda r: ('State one rule for drawing biological specimens accurately.', 'Draw proportions accurately with clear continuous pencil lines and no shading.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how to calculate the actual size of a cell from a micrograph that has a scale bar.', 'Measure the scale bar in mm and convert to μm; magnification = measured bar length ÷ value written on the bar; measure the image of the cell; actual size = image size ÷ magnification; keep units consistent.', 'measure bar [1]; magnification from bar [1]; measure cell image [1]; actual = image ÷ M [1]; units consistent [1] [5]')])
t_c2c = t

# --- cell division and electron micrographs
EMS = [('mitochondria', 'aerobic respiration releasing energy'), ('ribosomes', 'protein synthesis'), ('rough endoplasmic reticulum', 'a network of membranes with ribosomes on which proteins are made and transported'),
       ('vesicles', 'small membrane-bound sacs that carry substances (e.g. proteins) around the cell or to the membrane for secretion')]
t = T('New cells produced by division of existing cells; cell structures seen in electron micrographs', 'new cells produced by division', 'electron micrographs')
facts(t, [('rough endoplasmic reticulum', 'a network of membranes covered with ribosomes, where proteins are made and transported'), ('vesicle', 'a small membrane-bound sac that transports substances within a cell'),
          ('ribosome', 'a very small structure where proteins are made'), ('mitochondrion', 'an organelle where aerobic respiration takes place'), ('cell division', 'the process by which an existing cell divides to produce new cells')])
mcqs(t, [('How are new cells produced?', 'By division of existing cells', 'All new cells come from the division of existing cells.', ['From non-living material in the cytoplasm', 'By the joining of two mature cells', 'From dead cells']),
         ('Which structure, seen only with an electron microscope, carries ribosomes on its surface?', 'Rough endoplasmic reticulum', 'RER is studded with ribosomes; proteins made there pass into vesicles.', ['Cell membrane', 'Nucleus', 'Chloroplast']),
         ('Which cell would be expected to contain the most mitochondria?', 'A muscle cell in the leg', 'Muscle cells need lots of energy from aerobic respiration.', ['A fat storage cell', 'A cell in the outer layer of skin', 'A red blood cell'])])
shorts(t, [('Name two cell structures that can be seen with an electron microscope but not with a light microscope.', 'Ribosomes and rough endoplasmic reticulum (also vesicles, internal structure of mitochondria).', 'any two [2]'),
           ('State the function of vesicles in a cell.', 'They transport substances, such as proteins, through the cytoplasm and to the cell membrane.', '[1]')])
explain(t, [('Cells in the pancreas make and secrete large amounts of enzymes. Explain why they contain a lot of rough endoplasmic reticulum and many vesicles.', 'Enzymes are proteins made on ribosomes on the RER; vesicles carry the enzymes to the cell membrane for secretion.', 'RER / ribosomes make protein [1]; vesicles transport for secretion [1] [2]'),
            ('Explain why a growing root tip contains many cells dividing, but a mature leaf contains few.', 'Growth needs new cells, which are produced only by division of existing cells; mature tissue has stopped growing so few cells divide.', 'new cells only from division [1]; growth regions need new cells [1] [2]'),
            ('Explain why the number of mitochondria differs between different types of cell.', 'Cells that need more energy (muscle, sperm, root hair cells taking up ions) carry out more aerobic respiration, so they have more mitochondria.', 'mitochondria = respiration / energy [1]; linked to energy demand [1] [2]'),
            ('Explain why bacteria contain ribosomes but no mitochondria.', 'All cells must make proteins, so they need ribosomes; bacteria are prokaryotes with no membrane-bound organelles, and respire using enzymes in the cytoplasm and membrane.', 'all cells make proteins [1]; prokaryotes lack membrane-bound organelles [1] [2]')])
myths(t, [('New cells can form from the cytoplasm of dead cells.', 'New cells are only produced by division of existing cells.'),
           ('Ribosomes make energy for the cell.', 'Ribosomes make proteins; mitochondria release energy by aerobic respiration.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def div_count(r, D):
    g = r.choice([20, 30, 40, 60]) if D <= 3 else r.choice([25, 45, 90, 120])
    n = r.choice([3, 4, 5, 6, 8]) if D <= 3 else r.choice([6, 8, 10])
    t_ = g * n
    start = r.choice([1, 1, 2, 5, 10]) if D >= 3 else 1
    cells = start * 2 ** n
    org = r.choice(['bacterium', 'yeast cell', 'cell in a culture']) if start == 1 else 'cells'
    tt = f'{t_} minutes' if t_ < 180 or t_ % 60 else f'{t_ // 60} hours'
    st = (f'A {org} divides every {g} minutes. Starting with one cell, how many cells will there be after {tt}?' if start == 1 else
          f'A culture starts with {start} cells, which divide every {g} minutes. Calculate the number of cells after {tt}.')
    key = f'number of divisions = {t_} ÷ {g} = {n} [1]; {start} × 2^{n} = {cells:,} [1] [2]'
    if D == 1:
        return NQ(r, st, cells, [2 * n * start, cells // 2, cells * 2, n * start], '', key, f=lambda v: f'{int(v):,}')
    if D >= 4:
        st += ' Suggest one reason why the population would not keep increasing at this rate.'
        key = key.replace(' [2]', '; nutrients run out / toxic waste builds up / space limited [1] [3]')
    return Q(st, f'{cells:,} cells' + ('; nutrients run out or waste builds up' if D >= 4 else ''), key, 'numerical')


@t.add('C3', (2, 3, 4), 'case')
def mito_data(r, D):
    cells = [('liver cell', 1500, 2200), ('heart muscle cell', 4000, 6000), ('skin surface cell', 50, 200), ('root hair cell', 300, 700), ('fat storage cell', 80, 300), ('neurone', 800, 1500)]
    pick = r.sample(cells, 3)
    vals = [(c, r.randrange(lo, hi)) for c, lo, hi in pick]
    hi = max(vals, key=lambda v: v[1])
    tab = '; '.join(f'{c}: {v}' for c, v in vals)
    st = f'A scientist counted the mean number of mitochondria per cell in electron micrographs of three cell types: {tab}. (a) Identify the cell type with the most mitochondria. (b) Explain why this cell type needs many mitochondria.'
    m = 3
    ans = f'(a) {hi[0]} (b) It needs a lot of energy (e.g. for contraction / active processes); mitochondria carry out aerobic respiration, which releases energy.'
    key = f'(a) {hi[0]} [1] (b) high energy demand [1]; mitochondria are the site of aerobic respiration [1]'
    if D >= 3:
        lo = min(vals, key=lambda v: v[1])
        st += f' (c) Calculate how many times more mitochondria the {hi[0]} has than the {lo[0]}.'
        ans += f' (c) {sf(hi[1] / lo[1], 3)} times'
        key += f' (c) {hi[1]} ÷ {lo[1]} = {sf(hi[1] / lo[1], 3)} [1]'
        m = 4
    return Q(st, ans, key + f' [{m}]', 'case', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def em_case(r, D):
    cell = r.choice([('a cell from the pancreas that secretes digestive enzymes', 'protein (enzyme) secretion'), ('a cell from the salivary gland that secretes amylase', 'protein (enzyme) secretion'),
                     ('a white blood cell that makes antibodies', 'antibody (protein) secretion')])
    intro = f'An electron micrograph shows {cell[0]}. It contains a large nucleus, many mitochondria, a lot of rough endoplasmic reticulum and many vesicles near the cell membrane.'
    parts = [lambda r: ('State the function of the rough endoplasmic reticulum.', 'Ribosomes on its surface make proteins, which are transported through the RER.', '[1] ribosomes / protein synthesis; [1] transport [2]'),
             lambda r: ('Suggest why there are many vesicles near the cell membrane.', f'The vesicles carry the proteins made by the cell to the membrane for release ({cell[1]}).', 'transport [1]; release/secretion of proteins at the membrane [1] [2]'),
             lambda r: ('Explain why the cell contains many mitochondria.', 'Making and secreting proteins needs a lot of energy, released by aerobic respiration in mitochondria.', 'energy needed [1]; aerobic respiration in mitochondria [1] [2]'),
             lambda r: ('Explain why these structures could not be seen with a light microscope.', 'They are smaller than the limit of resolution of a light microscope; an electron microscope has a much greater resolution.', 'too small / resolution [2]'),
             lambda r: ('State how the cell would have been produced.', 'By division of an existing cell (mitosis).', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structures visible in an electron micrograph of an animal cell and state the function of each.', 'Nucleus (DNA, controls cell), cell membrane (controls entry/exit), mitochondria (aerobic respiration), ribosomes (protein synthesis), rough ER (protein synthesis and transport), vesicles (transport/secretion).', 'five structures with correct functions [5]')])
t_c2d = t
CHAPTERS[2] = [t_c2a, t_c2b, t_c2c, t_c2d]


# ===================================================================== 3 Movement into and out of cells
t = T('Diffusion: net movement of particles down a concentration gradient and factors affecting rate', 'diffusion', 'factors affecting rate')
facts(t, [('diffusion', 'the net movement of particles from a region of their higher concentration to a region of their lower concentration, down a concentration gradient, as a result of their random movement'),
          ('concentration gradient', 'the difference in concentration of a substance between two regions'), ('kinetic energy', 'the energy of movement of particles, which drives diffusion'),
          ('surface area to volume ratio', 'the surface area of an object divided by its volume'), ('partially permeable membrane', 'a membrane that allows some molecules to pass through but not others')])
mcqs(t, [('Which change would increase the rate of diffusion of oxygen into a cell?', 'Increasing the concentration gradient', 'Steeper gradient, higher temperature, larger surface area and shorter distance all increase rate.',
          ['Decreasing the temperature', 'Increasing the distance', 'Decreasing the surface area']),
         ('What provides the energy for diffusion?', 'The kinetic energy of the random movement of particles', 'Diffusion is passive: it uses no energy from respiration.', ['Energy from respiration in the cell', 'ATP made in the mitochondria', 'Light energy']),
         ('Which substance moves into a respiring muscle cell by diffusion?', 'Oxygen', 'O₂ concentration is lower inside respiring cells; CO₂ diffuses out.', ['Carbon dioxide', 'Urea', 'Starch'])])
shorts(t, [('State four factors that affect the rate of diffusion.', 'Surface area, temperature, concentration gradient, distance (thickness of surface).', 'four [2]; two or three [1] [2]'),
           ('Name two substances that move into or out of cells by diffusion in the lungs.', 'Oxygen (into the blood) and carbon dioxide (out of the blood).', 'oxygen [1]; carbon dioxide [1] [2]')])
explain(t, [('Explain why diffusion is faster at higher temperatures.', 'Particles have more kinetic energy, so they move faster and spread down the concentration gradient more quickly.', 'more kinetic energy [1]; faster random movement [1] [2]'),
            ('Explain why small organisms can rely on diffusion across their surface, but large organisms need transport systems.', 'Small organisms have a large surface area to volume ratio and short diffusion distances; in large organisms the ratio is small and cells are far from the surface, so diffusion would be too slow.', 'SA:V ratio [1]; distance [1]; diffusion too slow in large organisms [1] [3]'),
            ('Explain why the walls of alveoli and capillaries are only one cell thick.', 'This gives a short diffusion distance so gases diffuse quickly between air and blood.', 'short distance [1]; faster diffusion [1] [2]'),
            ('Explain why the concentration gradient of oxygen between alveoli and blood is maintained.', 'Ventilation brings fresh air with high oxygen; blood flow carries oxygenated blood away and brings deoxygenated blood, keeping a steep gradient.', 'ventilation [1]; blood flow [1] [2]'),
            ('Explain why diffusion is described as a passive process.', 'It does not need energy from respiration; it relies on the random kinetic energy of particles moving down a concentration gradient.', 'no energy from respiration [1]; random movement down gradient [1] [2]'),
            ('A drop of food dye in still water spreads out slowly even though no one stirs it. Explain why.', 'The dye and water particles move randomly; there is a net movement of dye particles from where they are concentrated to where they are less concentrated until evenly spread.', 'random movement [1]; net movement high → low concentration [1] [2]')])
myths(t, [('Particles stop moving when diffusion is complete.', 'Particles keep moving randomly; there is just no net movement once concentrations are equal.'),
           ('Diffusion needs energy from respiration.', 'Diffusion is passive and uses the kinetic energy of particles; active transport uses energy from respiration.'),
           ('Larger cells absorb substances faster by diffusion because they have more surface.', 'Larger cells have a smaller surface area to volume ratio, so substances take longer to reach the centre.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def sav(r, D):
    sides = sorted(r.sample([0.5, 1, 2, 3, 4, 5], 2 if D <= 3 else 3))
    if D == 1:
        a = sides[-1]
        return NQ(r, f'What is the surface area to volume ratio of a cube with sides {fx(a)} cm?', 6 / a, [a / 6, 6 * a, 1 / a, 6 / a ** 2], ' : 1', f'SA = 6 × {fx(a)}² = {fx(6 * a * a)} cm²; V = {fx(a ** 3, 3)} cm³; ratio = {fx(6 / a, 2)} : 1.', f=lambda v: fx(v, 2))
    rows = [(a, 6 * a * a, a ** 3, 6 / a) for a in sides]
    st = f'{person(r)} cuts agar cubes containing an indicator, with sides of ' + ', '.join(f'{fx(a)} cm' for a in sides[:-1]) + f' and {fx(sides[-1])} cm. Calculate the surface area to volume ratio of each cube'
    ans = '; '.join(f'{fx(a)} cm cube: SA {fx(sa, 2)} cm², V {fx(v, 3)} cm³, ratio {fx(q, 2)} : 1' for a, sa, v, q in rows)
    key = '; '.join(f'{fx(sa, 2)} ÷ {fx(v, 3)} = {fx(q, 2)} : 1' for a, sa, v, q in rows) + ' (SA = 6a², V = a³)'
    m = len(sides) + 1
    if D >= 3:
        st += ' and predict which cube will change colour completely first when placed in acid. Explain your prediction.'
        ans += f'. The {fx(sides[0])} cm cube changes colour first: largest ratio and shortest distance to the centre.'
        key += f'; smallest cube first [1]; largest SA:V / shortest distance to centre [1]'
        m += 2
    else:
        st += '.'
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


DIFF_T = {'setup': lambda r, p: f'{p} placed cubes of agar containing alkali and phenolphthalein (pink) into dilute hydrochloric acid and timed how long each cube took to become colourless.',
          'iv': ('length of side of cube', 'mm'), 'xs': lambda r: r.choice([[5, 10, 15, 20], [4, 8, 12, 16, 20], [5, 10, 15, 20, 25]]),
          'dv': ('time to become colourless', 's'), 'y': lambda x, k: k * 1.6 * x * x + 20, 'dp': 0,
          'controls': ['concentration of acid', 'volume of acid', 'temperature of the acid', 'type and concentration of agar'],
          'trend': lambda d: 'As the cube size increases, the time to become colourless increases; larger cubes take much longer.',
          'why': ('Larger cubes have a smaller surface area to volume ratio and a greater distance from surface to centre, so acid takes longer to diffuse to the middle.', 'smaller SA:V ratio [1]; greater diffusion distance [1]; acid diffuses in to neutralise alkali [1] [3]'),
          'improve': ['use a white tile background to judge the colour change more accurately', 'cut the cubes more accurately with a scalpel and ruler'],
          'extra': [lambda r, d: (f'Calculate the rate of diffusion into the {fx(d["xs"][0])} mm cube as mm per second, using half the side length as the distance travelled.',
                                  f'{fx(d["xs"][0] / 2 / d["means"][0], 3)} mm/s', f'distance = {fx(d["xs"][0] / 2)} mm [1]; ÷ {fx(d["means"][0], 1)} s = {fx(d["xs"][0] / 2 / d["means"][0], 3)} mm/s [1] [2]')]}
DIFF_TEMP = {'setup': lambda r, p: f'{p} placed equal-sized agar cubes containing alkali and indicator into acid at different temperatures and timed how long they took to lose their colour.',
             'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[10, 20, 30, 40, 50], [15, 25, 35, 45], [20, 30, 40, 50, 60]]),
             'dv': ('time to lose colour', 's'), 'y': lambda x, k: k * 9000 / (x + 25), 'dp': 0,
             'controls': ['size of the agar cubes', 'concentration of acid', 'volume of acid', 'concentration of alkali in the agar'],
             'why': ('At higher temperatures the particles have more kinetic energy and move faster, so the acid diffuses into the cube more quickly.', 'more kinetic energy [1]; faster diffusion so shorter time [1] [2]'),
             'improve': ['use a thermostatically controlled water bath to keep each temperature constant', 'cut all cubes to exactly the same size']}
add_practical(t, DIFF_T)
add_practical(t, DIFF_TEMP, C3D=(2, 3, 4), C4D=(3, 4))


@t.add('C3', (2, 3), 'short')
def diff_dir(r, D):
    cases = [('oxygen', 'alveolus', 'blood in the capillary', 'it is used in respiration so its concentration in blood stays lower'),
             ('carbon dioxide', 'respiring muscle cell', 'blood in the capillary', 'it is made by respiration in the cell'),
             ('carbon dioxide', 'air spaces of a leaf in light', 'palisade cells', 'it is used in photosynthesis in the cells'),
             ('oxygen', 'palisade cells in light', 'air spaces of the leaf', 'it is produced by photosynthesis'),
             ('glucose', 'blood plasma', 'a respiring liver cell', 'it is used in respiration in the cell'),
             ('urea', 'liver cell', 'blood plasma', 'it is produced by deamination in the liver')]
    sub, a, b, why = r.choice(cases)
    return Q(f'State the direction in which {sub} diffuses between the {a} and the {b}, and explain why.', f'From the {a} to the {b}, because {why}, so there is a concentration gradient.',
             f'direction {a} → {b} [1]; higher concentration in {a} / gradient explained [1] [2]', 'short', 2)


longs(t, [('Describe and explain how surface area, temperature, concentration gradient and distance affect the rate of diffusion.', 'Larger surface area: more particles cross at once, faster. Higher temperature: more kinetic energy, faster. Steeper gradient: greater net movement, faster. Shorter distance: particles reach destination sooner, faster.',
           'each factor with correct direction and explanation [4]; example from living organisms [1] [5]')])
t_c3a = t

OSM_TISSUE = ['potato', 'sweet potato', 'carrot', 'beetroot', 'radish', 'cassava']


def osm_data(r, D):
    iso = r.choice([0.2, 0.25, 0.3, 0.35, 0.4])
    concs = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    tissue = r.choice(OSM_TISSUE)
    rows = []
    for c in concs:
        start = round(r.uniform(2.0, 3.0), 2)
        ch = (iso - c) * r.uniform(30, 40) if c < iso else (iso - c) * r.uniform(22, 28)
        ch = max(ch, -32)
        end = round(start * (1 + ch / 100), 2)
        rows.append((c, start, end, (end - start) / start * 100))
    return tissue, rows, iso


t = T('Osmosis: water potential and effects on plant and animal cells (turgor, plasmolysis, lysis)', 'osmosis', 'water potential', 'turgor, plasmolysis')
facts(t, [('osmosis', 'the net movement of water molecules from a region of higher water potential (dilute solution) to a region of lower water potential (concentrated solution), through a partially permeable membrane'),
          ('water potential', 'a measure of the tendency of water to move; it is highest in pure water and lower in more concentrated solutions'),
          ('turgid', 'describes a plant cell that is swollen and firm because water has entered and pushes the cytoplasm against the cell wall'),
          ('plasmolysis', 'the shrinking of the cytoplasm away from the cell wall when a plant cell loses water by osmosis'),
          ('flaccid', 'describes a plant cell that has lost water and is soft, with low turgor pressure'),
          ('turgor pressure', 'the pressure of the cell contents pushing outwards on the cell wall')])
mcqs(t, [('A red blood cell is placed in distilled water. What happens?', 'It swells and bursts', 'Water enters by osmosis (higher water potential outside); with no cell wall the membrane bursts.', ['It shrinks', 'It becomes plasmolysed', 'It stays the same']),
         ('A plant cell is placed in a concentrated sugar solution. What is it likely to become?', 'Plasmolysed', 'Water leaves by osmosis, the vacuole and cytoplasm shrink and pull away from the wall.', ['Turgid', 'Burst', 'Larger']),
         ('Which statement about osmosis is correct?', 'Water moves from a dilute solution to a concentrated solution through a partially permeable membrane', 'Water moves down its water potential gradient (high to low water potential).',
          ['Solute molecules move through the membrane from concentrated to dilute', 'Water moves from a concentrated solution to a dilute solution', 'Water moves only when energy from respiration is used'])])
shorts(t, [('State what happens to an animal cell placed in a concentrated salt solution.', 'It loses water by osmosis and shrinks (becomes crenated).', 'loses water [1]; shrinks [1] [2]'),
           ('State two ways in which turgor pressure is important to plants.', 'It supports soft tissues (keeps stems and leaves upright) and opens stomata / allows growth by cell expansion.', 'any two [2]')])
explain(t, [('Explain why a wilted plant recovers when it is watered.', 'Water enters cells by osmosis from the soil water (higher water potential); cells become turgid and press on each other, supporting the leaves and stems.', 'water enters by osmosis [1]; cells turgid [1]; support [1] [3]'),
            ('Explain why plant cells do not burst when placed in pure water.', 'Water enters by osmosis and the cell swells, but the strong cellulose cell wall resists further expansion so the cell becomes turgid, not burst.', 'water enters [1]; cell wall resists [1] [2]'),
            ('Explain why doctors use a drip with a salt concentration equal to that of blood plasma, not pure water.', 'Pure water has a higher water potential than cells, so water would enter red blood cells by osmosis and they would burst (lysis); an isotonic solution causes no net movement.', 'osmosis into cells [1]; lysis [1]; equal concentrations = no net movement [1] [3]'),
            ('Explain why putting salt on a slug kills it.', 'The salt solution on its moist skin has a lower water potential, so water leaves the slug cells by osmosis and it becomes dehydrated.', 'lower water potential outside [1]; water lost by osmosis [1] [2]'),
            ('Visking tubing containing sugar solution is placed in water. Explain why the liquid rises up a capillary tube attached to the tubing.', 'Water moves into the tubing by osmosis (from higher to lower water potential) through the partially permeable membrane; sugar molecules are too large to leave; the volume inside increases.', 'osmosis into tubing [1]; sugar cannot pass out [1]; volume increases [1] [3]')])
myths(t, [('In osmosis, sugar molecules move into the cell.', 'In osmosis water molecules move, through a partially permeable membrane, down a water potential gradient.'),
           ('Plant cells in pure water burst just like red blood cells.', 'Plant cells become turgid but do not burst because the cell wall resists expansion.'),
           ('Water moves from a concentrated solution to a dilute solution.', 'Water moves from a dilute solution (higher water potential) to a concentrated solution (lower water potential).')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def osm_pct(r, D):
    tissue, rows, iso = osm_data(r, D)
    if D <= 2:
        c, a, b, pc = r.choice(rows)
        st = f'A {tissue} cylinder had a mass of {fx(a, 2)} g. After 30 minutes in {fx(c)} mol/dm³ sucrose solution its mass was {fx(b, 2)} g. Calculate the percentage change in mass.'
        if D == 1:
            return NQ(r, st.replace('Calculate', 'What is'), pc, [pc * -1, (b - a) / b * 100, b - a, pc * 10], '%', f'({fx(b, 2)} − {fx(a, 2)}) ÷ {fx(a, 2)} × 100 = {fx(pc, 1)}%.', f=lambda v: fx(v, 1))
        return Q(st, f'{fx(pc, 1)}%', f'change = {fx(b - a, 2)} g [1]; ÷ {fx(a, 2)} × 100 = {fx(pc, 1)}% (sign shown) [1] [2]', 'numerical', 2)
    sel = rows if D >= 4 else rows[::2] + [rows[-1]]
    tab = '; '.join(f'{fx(c)} mol/dm³: {fx(a, 2)} g → {fx(b, 2)} g' for c, a, b, pc in sel)
    up = [x for x in rows if x[3] > 0]
    dn = [x for x in rows if x[3] < 0]
    lo, hi = up[-1], dn[0]
    est = lo[0] + (hi[0] - lo[0]) * lo[3] / (lo[3] - hi[3])
    st = f'{person(r)} placed {tissue} cylinders in sucrose solutions for one hour. Mass before → after: {tab}. (a) Calculate the percentage change in mass for each concentration.'
    ans = '(a) ' + '; '.join(f'{fx(c)}: {fx(pc, 1)}%' for c, a, b, pc in sel)
    key = '(a) ' + '; '.join(f'{fx(pc, 1)}%' for c, a, b, pc in sel) + ' (all correct with signs) [2]'
    m = 2
    if D >= 4:
        st += ' (b) Estimate the concentration of sucrose that would cause no change in mass. (c) Explain the change in mass at the highest concentration.'
        ans += f' (b) about {fx(est, 2)} mol/dm³ (c) The solution has a lower water potential than the cells, so water leaves the cells by osmosis; mass decreases.'
        key += f' (b) value where % change = 0, about {fx(est, 2)} mol/dm³ (±0.05) [1] (c) lower water potential outside [1]; water lost by osmosis through partially permeable membrane [1]'
        m = 5
    else:
        st += ' (b) State which concentration caused the largest loss in mass.'
        big = min(sel, key=lambda x: x[3])
        ans += f' (b) {fx(big[0])} mol/dm³'
        key += f' (b) {fx(big[0])} mol/dm³ [1]'
        m = 3
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


def _osm_spec():
    def setup(r, p):
        return f'{p} cut {r.choice(OSM_TISSUE)} cylinders of equal size, weighed them, placed them in sucrose solutions for 40 minutes, blotted and reweighed them. The results show the percentage change in mass.'
    return {'setup': setup, 'iv': ('concentration of sucrose', 'mol/dm³'), 'xs': lambda r: [0.0, 0.2, 0.4, 0.6, 0.8],
            'dv': ('percentage change in mass', '%'), 'y': lambda x, k: (0.3 * k - x) * 30, 'dp': 1, 'noise': 0.06, 'graph': True,
            'controls': ['size / surface area of the cylinders', 'time in the solution', 'temperature', 'volume of solution', 'source of the tissue'],
            'trend': lambda d: 'As the concentration increases, the percentage change in mass decreases: mass increases in dilute solutions and decreases in concentrated solutions.',
            'why': ('In dilute solutions water enters the cells by osmosis (higher water potential outside); in concentrated solutions water leaves the cells; where there is no change the water potentials are equal.', 'osmosis in [1]; osmosis out [1]; water potential comparison [1] [3]'),
            'improve': ['blot each cylinder in the same way before weighing', 'use more concentrations between 0.2 and 0.4 mol/dm³'],
            'extra': [lambda r, d: ('Use the results to estimate the concentration of sucrose that is equal in water potential to the cell contents.', f'About {fx(0.3 * d["kk"], 2)} mol/dm³ (where the change in mass is zero).', 'reads where % change = 0 [1]; value in correct range [1] [2]'),
                      lambda r, d: ('Explain why percentage change in mass is calculated instead of change in mass.', 'The cylinders have different starting masses, so percentage change allows a fair comparison.', 'different starting masses [1]; fair comparison [1] [2]')],
            'neg': True}


OSM = _osm_spec()
OSM['y'] = lambda x, k: (0.3 * k - x) * 30
add_practical(t, OSM, C3D=(3, 4), C4D=(3, 4, 5))


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def osm_cells(r, D):
    sol = r.choice([('distilled water', 'higher'), ('a concentrated salt solution', 'lower'), ('a 0.9% salt solution (same as blood plasma)', 'equal')])
    p = person(r)
    intro = f'{p} places red blood cells in one dish and onion epidermis cells in another, both in {sol[0]}, and observes them after 20 minutes.'
    res = {'higher': ('Red blood cells swell and burst (lysis); onion cells become turgid.', 'Water enters by osmosis because the solution has a higher water potential than the cytoplasm.'),
           'lower': ('Red blood cells shrink (crenate); onion cells become plasmolysed — cytoplasm pulls away from the cell wall.', 'Water leaves by osmosis because the solution has a lower water potential than the cytoplasm.'),
           'equal': ('No visible change in either type of cell.', 'Water potentials are equal, so there is no net movement of water by osmosis.')}[sol[1]]
    parts = [lambda r: ('Describe what you would expect to see happen to each type of cell.', res[0], 'red blood cells [1]; onion cells [1] [2]'),
             lambda r: ('Explain these observations.', res[1], 'water potential comparison [1]; osmosis through partially permeable membrane [1] [2]'),
             lambda r: ('Explain why the two types of cell respond differently.', 'Plant cells have a cellulose cell wall that resists expansion and supports the cell; animal cells have only a membrane.' if sol[1] != 'equal' else 'They would respond the same here; in other solutions they differ because only plant cells have a cell wall.', 'cell wall in plant cells [1]; not in animal cells [1] [2]'),
             lambda r: ('Suggest why a student should view the cells at the same magnification before and after.', 'So that changes in size can be compared fairly.', '[1]'),
             lambda r: ('Explain why turgor pressure is important for a non-woody plant.', 'Turgid cells press against each other, supporting stems and leaves so that leaves are held up to the light; loss of turgor causes wilting.', 'support [1]; wilting if lost [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe and explain what happens to a plant cell placed in (a) pure water and (b) a concentrated sucrose solution. Use the term water potential in your answer.', '(a) Water potential outside higher; water enters by osmosis through the partially permeable membrane; vacuole swells; cell becomes turgid; wall prevents bursting. (b) Water potential outside lower; water leaves; vacuole shrinks; cell becomes flaccid then plasmolysed, membrane pulls away from wall.',
           '(a) three points [3] (b) three points [3] [6]')])
t_c3b = t

t = T('Active transport against a concentration gradient using energy from respiration', 'active transport', 'against a concentration gradient')
facts(t, [('active transport', 'the movement of particles through a cell membrane from a region of lower concentration to a region of higher concentration, using energy from respiration'),
          ('carrier protein', 'a protein in the cell membrane that moves specific molecules or ions across the membrane during active transport'),
          ('respiration', 'the process in cells that releases the energy needed for active transport'), ('root hair cell', 'a specialised root cell that absorbs mineral ions by active transport and water by osmosis')])
mcqs(t, [('Which process moves nitrate ions into root hair cells from very dilute soil water?', 'Active transport', 'The ion concentration in the root is higher than in the soil, so energy is needed to move ions against the gradient.', ['Osmosis', 'Diffusion', 'Transpiration']),
         ('Which statement describes active transport?', 'It moves substances against a concentration gradient using energy', 'Active transport uses protein carriers and energy from respiration.', ['It moves water through a partially permeable membrane', 'It moves substances down a concentration gradient without energy', 'It only happens in plant cells']),
         ('A respiratory poison is added to root cells. Which process stops?', 'Uptake of ions by active transport', 'Without respiration there is no energy for active transport; diffusion and osmosis continue.', ['Osmosis', 'Diffusion of oxygen', 'Loss of water by evaporation'])])
shorts(t, [('Give two examples of active transport in living organisms.', 'Uptake of mineral ions by root hair cells; uptake of glucose by cells of the small intestine / kidney tubule.', 'any two [2]'),
           ('State two differences between active transport and diffusion.', 'Active transport needs energy from respiration and moves substances against a concentration gradient; diffusion is passive and down a gradient. Active transport uses carrier proteins.', 'any two differences [2]')])
explain(t, [('Root hair cells contain many mitochondria. Explain why.', 'They absorb mineral ions by active transport, which needs energy released by aerobic respiration in mitochondria.', 'active transport of ions [1]; energy from respiration in mitochondria [1] [2]'),
            ('Explain why waterlogged soils can reduce the uptake of mineral ions by plants.', 'Waterlogged soil has little oxygen, so root cells cannot respire aerobically and release less energy for active transport of ions.', 'little oxygen [1]; less respiration / energy [1]; less active transport [1] [3]'),
            ('Explain how protein carriers in the membrane are involved in active transport.', 'A carrier protein binds a specific molecule or ion on one side of the membrane, changes shape using energy from respiration and releases it on the other side.', 'binds specific substance [1]; shape change using energy / release on other side [1] [2]'),
            ('Explain why the concentration of glucose in the blood leaving the small intestine can be higher than in the gut contents after a meal is nearly absorbed.', 'Glucose continues to be absorbed by active transport into the villi cells against the concentration gradient, so it is absorbed even when the gut has less glucose than the blood.', 'against gradient [1]; active transport uses energy [1] [2]')])
myths(t, [('Active transport and diffusion both move particles down a concentration gradient.', 'Active transport moves particles against a concentration gradient using energy; diffusion is down the gradient.'),
           ('Active transport gets its energy from sunlight.', 'The energy for active transport comes from respiration in the cell.')])


@t.add('C3', (1, 2, 3, 4), 'case')
def at_data(r, D):
    ion = r.choice(['nitrate', 'potassium', 'magnesium', 'phosphate'])
    soil = round(r.uniform(0.02, 0.4), 2)
    f = r.choice([10, 20, 40, 50, 100, 150])
    cell = soil * f
    if D == 1:
        return MQ(r, f'The concentration of {ion} ions in soil water is {fx(soil, 2)} mmol/dm³ and in root hair cells is {fx(cell, 2)} mmol/dm³. How do the ions enter the root hair cells?', 'Active transport', ['Diffusion', 'Osmosis', 'Transpiration'],
                  'Ions move from low to high concentration, against the gradient, so active transport is needed.')
    st = f'The concentration of {ion} ions in soil water is {fx(soil, 2)} mmol/dm³ and in the root hair cells of a plant is {fx(cell, 2)} mmol/dm³. (a) Calculate how many times more concentrated the ions are inside the cells. (b) Name the process by which the ions are absorbed and explain your answer.'
    ans = f'(a) {f} times (b) Active transport: the ions move against a concentration gradient, which needs energy from respiration.'
    key = f'(a) {fx(cell, 2)} ÷ {fx(soil, 2)} = {f} [1] (b) active transport [1]; against concentration gradient using energy [1]'
    m = 3
    if D >= 3:
        st += ' (c) Predict and explain the effect on ion uptake if the soil is waterlogged.'
        ans += ' (c) Uptake decreases: little oxygen for aerobic respiration, so less energy for active transport.'
        key += ' (c) uptake falls [1]; less oxygen → less respiration → less energy [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'case', m)


AT_O2 = {'setup': lambda r, p: f'{p} placed barley roots in a solution of potassium ions and bubbled air containing different percentages of oxygen through it. After 3 hours the mass of potassium absorbed per gram of root was measured.',
         'iv': ('oxygen concentration', '%'), 'xs': lambda r: r.choice([[0, 3, 6, 12, 21], [0, 5, 10, 15, 20], [0, 2, 5, 10, 20]]),
         'dv': ('potassium absorbed', 'μg per g of root'), 'y': lambda x, k: k * (20 + 160 * (1 - math.exp(-x / 5))), 'dp': 0,
         'controls': ['temperature', 'concentration of potassium ions', 'mass of roots', 'time in the solution', 'type of plant'],
         'why': ('More oxygen allows more aerobic respiration in the root cells, releasing more energy for active transport of potassium ions; at high oxygen another factor (e.g. number of carrier proteins) limits uptake. Some uptake at 0% is by diffusion / anaerobic respiration.', 'more aerobic respiration [1]; more energy for active transport [1]; levelling off / other limiting factor [1] [3]'),
         'improve': ['keep the temperature constant with a water bath', 'use roots from plants of the same age and species']}
add_practical(t, AT_O2)


@t.add('C4', (3, 4, 5), 'multi_step')
def at_case(r, D):
    t1 = r.choice([10, 15, 20, 25])
    cy = r.choice([0.2, 0.25, 0.3])
    a0 = r.randrange(60, 90)
    a1 = round(a0 * cy)
    intro = f'Carrot discs were kept in a solution of potassium chloride at {t1} °C. In one beaker cyanide (which stops aerobic respiration) was added. The uptake of potassium ions in 2 hours was {a0} units without cyanide and {a1} units with cyanide.'
    parts = [lambda r: ('Calculate the percentage decrease in uptake caused by cyanide.', f'{fx((a0 - a1) / a0 * 100, 1)}%', f'({a0} − {a1}) ÷ {a0} × 100 [1] = {fx((a0 - a1) / a0 * 100, 1)}% [1] [2]'),
             lambda r: ('Explain why cyanide reduces the uptake of potassium ions.', 'Cyanide stops aerobic respiration, so less energy is released for active transport of ions against the concentration gradient.', 'stops respiration [1]; no energy for active transport [1] [2]'),
             lambda r: ('Suggest why some potassium is still absorbed in the presence of cyanide.', 'Some ions enter by diffusion down a concentration gradient (or energy from anaerobic respiration).', '[1]'),
             lambda r: ('Predict the effect of raising the temperature to 5 °C below the optimum for respiration enzymes, and explain.', 'Uptake increases because enzymes in respiration work faster, releasing energy more quickly for active transport.', 'increase [1]; faster respiration / more energy [1] [2]'),
             lambda r: ('Explain why the investigation used several carrot discs of the same size in each beaker.', 'Same surface area for uptake so comparison is fair; several discs reduce the effect of variation between discs.', 'same surface area / fair test [1]; reliability [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Compare diffusion, osmosis and active transport.', 'Diffusion: net movement of particles down a concentration gradient, passive. Osmosis: water through a partially permeable membrane from higher to lower water potential, passive. Active transport: particles against a concentration gradient using energy from respiration and carrier proteins.',
           'one correct point for each process [3]; two valid comparisons (energy, gradient, membrane) [2] [5]')])
t_c3c = t
CHAPTERS[3] = [t_c3a, t_c3b, t_c3c]


# ===================================================================== 4 Biological molecules
MOLS = {'starch': ('carbohydrate', 'glucose', 'C, H, O', 'energy store in plants'), 'glycogen': ('carbohydrate', 'glucose', 'C, H, O', 'energy store in animals (liver and muscles)'),
        'cellulose': ('carbohydrate', 'glucose', 'C, H, O', 'forms plant cell walls'), 'proteins': ('protein', 'amino acids', 'C, H, O, N (and sometimes S)', 'enzymes, antibodies, growth and repair'),
        'fats and oils': ('lipid', 'fatty acids and glycerol', 'C, H, O', 'energy store, insulation, cell membranes')}
t = T('Chemical elements in carbohydrates, fats and proteins; large molecules from smaller units', 'chemical elements in carbohydrates', 'large molecules from smaller units')
facts(t, [('carbohydrate', 'a compound containing carbon, hydrogen and oxygen, such as glucose, starch and cellulose'), ('protein', 'a large molecule made of a chain of amino acids, containing C, H, O and N'),
          ('lipid', 'a fat or oil, made from fatty acids and glycerol and containing C, H and O'), ('glycogen', 'a large carbohydrate made of glucose units, stored in liver and muscle cells'),
          ('amino acid', 'one of about 20 small molecules that join in chains to make proteins'), ('cellulose', 'a polymer of glucose that forms plant cell walls')])
mcqs(t, [('Which element is found in proteins but not in carbohydrates or fats?', 'Nitrogen', 'Proteins contain C, H, O and N (and sometimes S); carbohydrates and fats contain only C, H and O.', ['Carbon', 'Oxygen', 'Hydrogen']),
         ('Which smaller molecules join to make starch?', 'Glucose', 'Starch, glycogen and cellulose are all made of glucose units.', ['Amino acids', 'Fatty acids', 'Glycerol']),
         ('Which pair of molecules are the building blocks of fats and oils?', 'Fatty acids and glycerol', 'One glycerol joined to three fatty acids.', ['Glucose and amino acids', 'Amino acids and glycerol', 'Glucose and fatty acids'])])
shorts(t, [('Name the chemical elements found in carbohydrates.', 'Carbon, hydrogen and oxygen.', 'all three [1]'),
           ('Name three large carbohydrate molecules made from glucose.', 'Starch, glycogen and cellulose.', 'all three [2]; two [1] [2]')])
explain(t, [('Explain why plants store glucose as starch rather than as glucose.', 'Starch is insoluble, so it does not affect the water potential of cells (no osmosis) and it is compact; glucose is soluble and would draw water in.', 'insoluble [1]; does not affect osmosis / water potential [1] [2]'),
            ('Explain why proteins can have many different shapes and functions.', 'They are made from about 20 different amino acids joined in different sequences; the sequence determines how the chain folds, giving each protein a specific shape.', 'different amino acids / sequence [1]; sequence determines shape [1] [2]'),
            ('Explain why animals and plants need nitrogen-containing compounds in their diet or from the soil.', 'Nitrogen is needed to make amino acids and therefore proteins for growth, enzymes and repair (and DNA).', 'amino acids / proteins contain N [1]; needed for growth/enzymes [1] [2]'),
            ('Compare the structure of glycogen and cellulose.', 'Both are large carbohydrates made of many glucose units containing C, H and O. Glycogen is an energy store in animals; cellulose forms plant cell walls and the glucose units are joined differently.', 'one similarity [1]; one difference [1] [2]')])
myths(t, [('Fats contain nitrogen because they are made of amino acids.', 'Fats contain only C, H and O and are made of fatty acids and glycerol; proteins are made of amino acids.'),
           ('Starch is made of amino acids joined together.', 'Starch is made of many glucose molecules joined together.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def mol_id(r, D):
    m, (cls, unit, el, use) = r.choice(list(MOLS.items()))
    if D <= 2:
        mode = r.randrange(3)
        if mode == 0:
            return MQ(r, f'Which smaller molecules join together to form {m}?', unit, [v[1] for k, v in MOLS.items() if v[1] != unit] + ['nucleotides', 'sucrose'], f'{cap(m)} is made from {unit}.')
        if mode == 1:
            return MQ(r, f'A molecule contains {el} and is used for this function: {use}. Which molecule is it?', m, [k for k in MOLS if k != m and MOLS[k][3] != use], f'{cap(m)}: {cls} made of {unit}; {use}.')
        return MQ(r, f'Which elements are found in {m}?', el, ['C, H, O', 'C, H, O, N (and sometimes S)', 'C, H, N only', 'C, O, N, P only'], f'{cap(m)} contains {el}.')
    ks = r.sample(list(MOLS), 3)
    labs = ['(i)', '(ii)', '(iii)']
    return Q('Complete the information for each molecule by naming the smaller units it is made from and the elements it contains: ' + ', '.join(f'{labs[i]} {k}' for i, k in enumerate(ks)) + '.',
             ' '.join(f'{labs[i]} {MOLS[k][1]}; {MOLS[k][2]}' for i, k in enumerate(ks)), '; '.join(f'{labs[i]} {MOLS[k][1]} [1], {MOLS[k][2]} [1]' for i, k in enumerate(ks)) + ' [6]', 'short', 6) if D >= 4 else \
        Q('Name the smaller units used to make each molecule: ' + ', '.join(f'{labs[i]} {k}' for i, k in enumerate(ks)) + '.', ' '.join(f'{labs[i]} {MOLS[k][1]}' for i, k in enumerate(ks)),
          '; '.join(f'{labs[i]} {MOLS[k][1]}' for i, k in enumerate(ks)) + ' (1 mark each) [3]', 'short', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def mol_case(r, D):
    food = r.choice([('a peanut', 'fats and oils', 'proteins'), ('a potato', 'starch', 'cellulose'), ('a piece of chicken', 'proteins', 'fats and oils'), ('a grain of rice', 'starch', 'proteins')])
    intro = f'{person(r)} is studying the molecules in {food[0]}. The main molecules present are {food[1]} and {food[2]}.'
    parts = [lambda r: (f'Name the smaller molecules from which {food[1]} are made.'.replace('starch are', 'starch is'), MOLS[food[1]][1] + '.', '[1]'),
             lambda r: (f'State the chemical elements present in {food[2]}.', MOLS[food[2]][2] + '.', '[1]'),
             lambda r: (f'Describe one function of {food[1]} in living organisms.'.replace('starch in', 'starch in'), cap(MOLS[food[1]][3]) + '.', '[1]'),
             lambda r: ('Explain why large molecules must be broken down into smaller molecules during digestion.', 'Large molecules are insoluble / too big to pass through the gut wall into the blood; small soluble molecules can be absorbed.', 'too large / insoluble [1]; small molecules absorbed [1] [2]'),
             lambda r: ('Suggest how a scientist could show that this food contains protein.', 'Add biuret reagent; a purple colour shows protein is present.', 'biuret [1]; purple [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the chemical elements and smaller units that make up carbohydrates, fats and proteins, and give one function of each in the body.', 'Carbohydrates: C, H, O; made of glucose / simple sugars; energy. Fats: C, H, O; fatty acids and glycerol; energy store / insulation. Proteins: C, H, O, N (S); amino acids; growth, repair, enzymes.',
           'elements correct for each [2]; units correct for each [2]; functions [1] [5]')])
t_c4a = t

FT = {'starch': ('iodine solution', 'blue-black', 'stays orange-brown'), 'reducing sugar': ("Benedict's solution and heat in a water bath", 'brick-red (or green/yellow/orange) precipitate', 'stays blue'),
      'protein': ('biuret solution', 'purple / violet', 'stays blue'), 'fat': ('ethanol, then water (emulsion test)', 'cloudy white emulsion', 'stays clear'),
      'vitamin C': ('DCPIP solution', 'blue DCPIP becomes colourless', 'DCPIP stays blue')}
FTS = {'starch': ('iodine', 'blue-black', 'orange-brown'), 'reducing sugar': ("Benedict's (heated)", 'brick-red precipitate', 'blue'), 'protein': ('biuret', 'purple', 'blue'),
       'fat': ('ethanol emulsion', 'cloudy white', 'clear'), 'vitamin C': ('DCPIP', 'colourless', 'blue')}
FOODS = [('milk', {'reducing sugar', 'protein', 'fat'}), ('egg white', {'protein'}), ('potato', {'starch'}), ('grape juice', {'reducing sugar', 'vitamin C'}), ('orange juice', {'reducing sugar', 'vitamin C'}),
         ('cooking oil', {'fat'}), ('bread', {'starch', 'protein'}), ('peanuts', {'fat', 'protein'}), ('onion', {'reducing sugar'}), ('table sugar (sucrose) solution', set()),
         ('lemon juice', {'vitamin C', 'reducing sugar'}), ('cheese', {'fat', 'protein'}), ('rice flour', {'starch'}), ('banana', {'starch', 'reducing sugar'})]
t = T("Food tests: iodine, Benedict's, biuret, ethanol emulsion and DCPIP", 'food tests', "benedict's", 'biuret', 'dcpip')
facts(t, [('iodine test', 'a test for starch: orange-brown iodine solution turns blue-black'), ("Benedict's test", 'a test for reducing sugars: heated blue solution gives a brick-red precipitate'),
          ('biuret test', 'a test for protein: blue biuret solution turns purple'), ('emulsion test', 'a test for fats and oils: shaking with ethanol then adding water gives a cloudy white emulsion'),
          ('DCPIP test', 'a test for vitamin C: blue DCPIP solution becomes colourless')])
mcqs(t, [("Which food test requires heating?", "Benedict's test for reducing sugars", "Benedict's solution must be heated in a water bath (about 80 °C) for the colour change.", ['Biuret test for protein', 'Iodine test for starch', 'Emulsion test for fats']),
         ('A food sample turns biuret solution purple. Which nutrient is present?', 'Protein', 'Biuret: blue → purple/violet for protein.', ['Starch', 'Fat', 'Reducing sugar']),
         ('Which result shows that a liquid contains starch?', 'Iodine solution turns blue-black', 'Iodine changes from orange-brown to blue-black with starch.', ["Benedict's solution turns brick-red", 'Biuret turns purple', 'DCPIP turns colourless'])])
shorts(t, [("Describe how to carry out Benedict's test on a food sample.", "Add an equal volume of Benedict's solution to the food solution and heat in a water bath (about 80 °C) for a few minutes; a colour change from blue to green / yellow / orange / brick-red shows a reducing sugar.", 'add Benedict\'s and heat [1]; positive colour [1] [2]'),
           ('Describe the emulsion test for fat.', 'Shake the food with ethanol, pour the ethanol into water; a cloudy white emulsion shows fat.', 'ethanol then water [1]; cloudy white [1] [2]')])
explain(t, [("Explain why the colour of Benedict's test can be used to estimate the amount of reducing sugar.", 'More reducing sugar gives more precipitate, so the colour changes further from blue through green, yellow and orange to brick-red.', 'colour sequence [1]; more sugar → further along / more precipitate [1] [2]'),
            ('Sucrose solution gives a negative result with Benedict\'s solution. Explain why it gives a positive result after boiling with dilute acid and neutralising.', 'Sucrose is not a reducing sugar; acid hydrolyses (breaks) it into glucose and fructose, which are reducing sugars.', 'sucrose non-reducing [1]; broken into reducing sugars [1] [2]'),
            ('Explain why a control tube containing water instead of food should be set up for each food test.', 'It shows the colour of the reagent with no nutrient present, so a colour change in the food tube can be identified as a positive result.', 'comparison [1]; shows change is due to the food [1] [2]'),
            ('Explain why the emulsion test must not be done near a flame.', 'Ethanol is highly flammable.', '[1]'),
            ('Explain how the DCPIP test can compare the vitamin C content of two fruit juices.', 'Add each juice drop by drop to a fixed volume of DCPIP until it just becomes colourless; the fewer drops (smaller volume) needed, the more vitamin C the juice contains.', 'fixed volume of DCPIP [1]; count drops to decolourise [1]; fewer drops = more vitamin C [1] [3]')])
myths(t, [("Benedict's solution turns purple when protein is present.", "Biuret solution turns purple with protein; Benedict's solution tests for reducing sugars."),
           ('Iodine solution turns brick-red when starch is present.', 'Iodine turns blue-black with starch.'),
           ("Benedict's test works at room temperature.", "Benedict's test needs heating in a water bath.")])


@t.add('C3', (1, 2, 3, 4, 5), 'case')
def ft_table(r, D):
    n = 1 if D <= 1 else (2 if D == 2 else 3)
    foods = r.sample(FOODS, n)
    tests = r.sample(list(FT), 4 if D >= 3 else 3)
    labs = 'PQR'
    rows = []
    for i, (f, has) in enumerate(foods):
        rows.append(f'sample {labs[i]}: ' + ', '.join(f'{FTS[x][0]} → {FTS[x][1] if x in has else FTS[x][2]}' for x in tests))
    if D == 1:
        f, has = foods[0]
        if not (has & set(tests)):
            return None
        x = r.choice(sorted(has & set(tests)))
        return MQ(r, f'A food sample gives these results: {rows[0].split(": ", 1)[1]}. Which nutrient does it contain?', x, [k for k in FT if k not in has] + ['glycogen', 'cellulose'], f'{FTS[x][0]} → {FTS[x][1]} shows {x}.')
    st = f'{person(r)} tested food samples. Results: ' + '; '.join(rows) + '. State which nutrients each sample contains.'
    ans = '; '.join(f'{labs[i]}: ' + (', '.join(sorted(has & set(tests))) or 'none of those tested') for i, (f, has) in enumerate(foods))
    key = ans + f' (1 mark per sample fully correct) [{n}]'
    m = n
    if D >= 4:
        f, has = r.choice(foods)
        st += ' Suggest the identity of one sample from this list: ' + ', '.join(sorted({x[0] for x in r.sample(FOODS, 3)} | {f})) + '.'
        ans += f'. A sample with these results could be {f}.'
        key = key.replace(f' [{n}]', f'; identity consistent with results [1] [{n + 1}]')
        m = n + 1
    return Q(st, ans, key, 'case', m)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def dcpip(r, D):
    std = r.choice([1.0, 0.5, 2.0])
    v_std = r.choice([0.5, 0.8, 1.0, 1.2, 1.5])
    juices = r.sample(['orange juice', 'lemon juice', 'lime juice', 'apple juice', 'mango juice', 'kiwi fruit juice'], 2)
    vs = [round(v_std * r.choice([0.5, 0.8, 1.25, 2, 2.5, 4]), 2) for _ in juices]
    if vs[0] == vs[1]:
        vs[1] = round(vs[1] * 1.5, 2)
    conc = [std * v_std / v for v in vs]
    st = (f'{person(r)} found that {fx(v_std, 2)} cm³ of a {fx(std)} mg/cm³ vitamin C solution was needed to decolourise 1 cm³ of DCPIP. To decolourise 1 cm³ of DCPIP, {fx(vs[0], 2)} cm³ of {juices[0]} and {fx(vs[1], 2)} cm³ of {juices[1]} were needed. '
          f'(a) Calculate the concentration of vitamin C in each juice. (b) State which juice contains more vitamin C.')
    hi = juices[0] if conc[0] > conc[1] else juices[1]
    ans = f'(a) {juices[0]}: {sf(conc[0], 3)} mg/cm³; {juices[1]}: {sf(conc[1], 3)} mg/cm³ (b) {hi}'
    key = f'(a) mass of vitamin C to decolourise = {fx(std * v_std, 3)} mg [1]; {fx(std * v_std, 3)} ÷ {fx(vs[0], 2)} = {sf(conc[0], 3)} [1]; ÷ {fx(vs[1], 2)} = {sf(conc[1], 3)} mg/cm³ [1] (b) {hi} (smaller volume needed) [1]'
    m = 4
    if D >= 4:
        st += ' (c) State two variables that must be controlled to make the comparison fair.'
        ans += ' (c) volume and concentration of DCPIP; temperature / age of juice / mixing method.'
        key += ' (c) any two valid [2]'
        m = 6
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def ft_plan(r, D):
    f, has = r.choice([x for x in FOODS if x[1]])
    x = r.choice(sorted(has))
    intro = f'{person(r)} wants to find out whether {f} contains {x}, and to compare the amount with another food.'
    parts = [lambda r: (f'Describe how to test the food for {x}.', f'Prepare a solution/suspension of the food; {FT[x][0]}; positive result: {FT[x][1]}.', f'preparing sample (crush with water) [1]; reagent / method: {FT[x][0]} [1]; positive result {FT[x][1]} [1] [3]'),
             lambda r: ('State the result you would expect if the nutrient is absent.', cap(FT[x][2]) + '.', '[1]'),
             lambda r: ('Describe a suitable control for this test.', 'Repeat the test using distilled water instead of the food sample.', '[1]'),
             lambda r: ('Suggest how the method could be changed to compare the amount of the nutrient in two foods.', "Use the same mass of each food in the same volume of water and the same volume of reagent; compare colour intensity (or use a colour chart / colorimeter, or count drops for DCPIP).", 'same mass / volume [1]; compare colour or quantitative method [1] [2]'),
             lambda r: ('State one safety precaution for this test.', 'Wear eye protection' + ('; keep ethanol away from flames' if x == 'fat' else '; use a water bath, not a direct flame' if x == 'reducing sugar' else '') + '.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how you would test a sample of food for starch, reducing sugar, protein and fat. Give the positive result for each test.', 'Starch: iodine, orange-brown → blue-black. Reducing sugar: Benedict\'s, heat, blue → brick-red. Protein: biuret, blue → purple. Fat: ethanol then water, cloudy white emulsion.',
           'one mark per test with correct method and result [4]; control / safety point [1] [5]')])
t_c4b = t

PAIR = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
t = T('Structure of DNA: double helix and complementary base pairing', 'structure of dna', 'complementary base pairing', 'double helix')
facts(t, [('double helix', 'the shape of a DNA molecule: two strands coiled around each other'), ('complementary base pairing', 'the pairing of bases between DNA strands: A always with T and C always with G'),
          ('base', 'one of four chemicals (A, T, C, G) whose sequence along DNA forms the genetic code'), ('gene', 'a length of DNA that codes for a protein'),
          ('chromosome', 'a long thread of DNA made up of many genes')])
mcqs(t, [('Which base pairs with adenine in DNA?', 'Thymine', 'A–T and C–G.', ['Cytosine', 'Guanine', 'Uracil']), ('What holds the two strands of a DNA molecule together?', 'Bonds between complementary bases', 'Pairs of bases (A–T, C–G) are joined by bonds, holding the strands together.', ['Glucose molecules', 'Amino acids', 'Fatty acids']),
         ('What is the shape of a DNA molecule?', 'A double helix', 'Two strands coiled to form a double helix.', ['A single straight chain', 'A ring', 'A branched chain'])])
shorts(t, [('State the four bases found in DNA.', 'Adenine (A), thymine (T), cytosine (C), guanine (G).', 'all four [1]'), ('State the base pairing rules in DNA.', 'A pairs with T; C pairs with G.', 'both pairs [1]')])
explain(t, [('Explain why the amount of adenine in a DNA molecule is always equal to the amount of thymine.', 'Every adenine on one strand pairs with a thymine on the other (complementary pairing), so they occur in equal numbers.', 'A pairs only with T [1]; so numbers equal [1] [2]'),
            ('Explain how the structure of DNA allows it to carry genetic information.', 'The sequence of bases along one strand forms a code; the order of bases in a gene determines the order of amino acids in a protein.', 'base sequence = code [1]; determines amino acid order / protein [1] [2]'),
            ('Explain why complementary base pairing allows DNA to be copied accurately.', 'Each strand acts as a template: only A can pair with T and C with G, so the new strand has a sequence fixed by the old one.', 'template [1]; specific pairing gives identical copy [1] [2]')])
myths(t, [('In DNA, adenine pairs with guanine.', 'Adenine pairs with thymine; cytosine pairs with guanine.'), ('DNA is a single strand of bases.', 'DNA is two strands twisted into a double helix, joined by base pairs.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def dna_comp(r, D):
    L = 8 if D <= 2 else 12
    s = ''.join(r.choice('ATCG') for _ in range(L))
    c = ''.join(PAIR[b] for b in s)
    if D == 1:
        wrong = [s, s[::-1], ''.join({'A': 'G', 'G': 'A', 'C': 'T', 'T': 'C'}[b] for b in s), c[::-1]]
        return MQ(r, f'One strand of DNA has the base sequence {s}. What is the sequence of the complementary strand?', c, wrong, f'A–T, C–G: {s} → {c}.')
    st = f'One strand of a DNA molecule has the sequence {"-".join(s)}. Write the sequence of bases on the complementary strand.'
    m = 2
    ans, key = '-'.join(c), f'{"-".join(c)} (all correct; deduct 1 mark per error) [2]'
    if D >= 3:
        nA = s.count('A') + c.count('A')
        st += f' Then state how many adenine bases there are in this {L}-base-pair section of DNA.'
        ans += f'; {nA} adenine bases'
        key = f'{"-".join(c)} (all correct [2], deduct 1 per error); adenine = A on first strand ({s.count("A")}) + T on first strand ({s.count("T")}) = {nA} [1] [3]'
        m = 3
    return Q(st, ans, key, 'short', m)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def dna_pct(r, D):
    base = r.choice('ATCG')
    p = r.choice([12, 15, 18, 20, 22, 24, 26, 28, 30, 32, 35])
    partner = PAIR[base]
    others = [b for b in 'ATCG' if b not in (base, partner)]
    o = (100 - 2 * p) / 2
    names = {'A': 'adenine', 'T': 'thymine', 'C': 'cytosine', 'G': 'guanine'}
    st = f'In a sample of DNA, {p}% of the bases are {names[base]} ({base}). Calculate the percentage of each of the other three bases.'
    ans = f'{names[partner]} {p}%; {names[others[0]]} {fx(o)}%; {names[others[1]]} {fx(o)}%'
    key = f'{partner} = {p}% (pairs with {base}) [1]; remaining {100 - 2 * p}% shared equally [1]; {others[0]} = {others[1]} = {fx(o)}% [1] [3]'
    m = 3
    if D >= 4:
        n = r.choice([2000, 5000, 10000, 12000])
        st += f' If the section contains {n:,} bases in total, calculate the number of {names[others[0]]} bases.'
        ans += f'; {int(n * o / 100):,} {names[others[0]]} bases'
        key = key.replace(' [3]', f'; {fx(o)}% of {n:,} = {int(n * o / 100):,} [1] [4]')
        m = 4
    return Q(st, ans, key, 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def dna_case2(r, D):
    s = ''.join(r.choice('ATCG') for _ in range(9))
    intro = f'A student builds a model of a short section of DNA. One strand has the base sequence {s}.'
    parts = [lambda r: ('Write the sequence of the complementary strand.', ''.join(PAIR[b] for b in s), '[2]'),
             lambda r: ('Describe the overall shape of the DNA molecule.', 'Two strands coiled into a double helix, with bases paired in the middle.', 'two strands [1]; double helix [1] [2]'),
             lambda r: ('Explain how a change in one base in this sequence could affect the protein produced.', 'A change in base sequence (mutation) may change the amino acid coded for, changing the sequence and shape of the protein so it may not work.', 'changes code / amino acid [1]; protein shape / function changed [1] [2]'),
             lambda r: (f'Calculate the percentage of bases in this double-stranded section that are guanine or cytosine.', f'{fx((s.count("G") + s.count("C")) / 9 * 100, 1)}%', f'G + C pairs = {s.count("G") + s.count("C")} of 9 pairs [1]; = {fx((s.count("G") + s.count("C")) / 9 * 100, 1)}% [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of a DNA molecule.', 'Two strands coiled to form a double helix; each strand has a sequence of bases (A, T, C, G); bases on opposite strands pair (A with T, C with G); bonds between base pairs hold the strands together; sequence of bases forms the genetic code.',
           'double helix [1]; two strands [1]; four bases [1]; pairing rules [1]; bonds between bases / code [1] [5]')])
t_c4c = t
CHAPTERS[4] = [t_c4a, t_c4b, t_c4c]

# ===================================================================== 5 Enzymes
t = T('Enzymes as biological catalysts; active site and enzyme–substrate complex', 'enzymes as biological catalysts', 'active site', 'enzyme–substrate complex')
facts(t, [('catalyst', 'a substance that increases the rate of a chemical reaction and is not changed by the reaction'), ('enzyme', 'a protein that acts as a biological catalyst'),
          ('active site', 'the region of an enzyme with a specific shape into which the substrate fits'), ('substrate', 'the molecule on which an enzyme acts'),
          ('enzyme–substrate complex', 'the temporary structure formed when a substrate binds to the active site of an enzyme'), ('product', 'a molecule formed by an enzyme-catalysed reaction')])
mcqs(t, [('Why does each enzyme act on only one type of substrate?', 'The shape of the active site is complementary to only that substrate', 'Enzyme specificity: the substrate must fit the active site.', ['Enzymes are made of fat', 'Each enzyme is used up after one reaction', 'Substrates are all the same shape']),
         ('Which statement about enzymes is correct?', 'They can be used again after a reaction', 'Enzymes are catalysts: they are not changed or used up.', ['They are made of carbohydrate', 'They are destroyed after each reaction', 'They slow down reactions']),
         ('Amylase breaks down starch. In this reaction, starch is the', 'substrate', 'Starch binds to the active site and is broken down to maltose (the product).', ['product', 'enzyme', 'active site'])])
shorts(t, [('State why enzymes are important in living organisms.', 'They speed up reactions in cells so that reactions happen fast enough to sustain life at body temperature.', 'speed up reactions [1]; at body temperature / fast enough for life [1] [2]'),
           ('State what is meant by enzyme specificity.', 'Each enzyme catalyses only one reaction because only one substrate fits its active site.', '[1]')])
explain(t, [('Explain how an enzyme catalyses the breakdown of a substrate. Use the terms active site and enzyme–substrate complex.', 'The substrate collides with and fits into the complementary active site, forming an enzyme–substrate complex; the reaction occurs and products are released, leaving the enzyme unchanged.', 'complementary fit [1]; ES complex formed [1]; products released, enzyme unchanged [1] [3]'),
            ('Explain why protease cannot digest starch.', 'The shape of the active site of protease is complementary to proteins, not starch; starch cannot fit, so no enzyme–substrate complex forms.', 'active site shape specific [1]; starch does not fit [1] [2]'),
            ('Explain why only small amounts of enzymes are needed in cells.', 'Enzymes are not used up; each enzyme molecule can catalyse the reaction many times.', 'not used up [1]; reused many times [1] [2]'),
            ('Explain why enzymes are needed for reactions in cells even though the reactions would happen eventually without them.', 'Without enzymes the reactions would be far too slow at body temperature to supply energy and materials for life.', 'too slow [1]; at body temperature / for life processes [1] [2]')])
myths(t, [('Enzymes are living organisms that eat the substrate.', 'Enzymes are protein molecules that act as catalysts; they are not alive.'),
           ('An enzyme is used up when it catalyses a reaction.', 'Enzymes are unchanged by the reaction and can be reused.'),
           ('The substrate and active site are the same shape.', 'The active site has a shape complementary to the substrate, so the substrate fits into it.')])

ENZ = [('amylase', 'starch', 'maltose'), ('protease', 'protein', 'amino acids'), ('lipase', 'fats', 'fatty acids and glycerol'), ('catalase', 'hydrogen peroxide', 'water and oxygen'),
       ('maltase', 'maltose', 'glucose'), ('sucrase', 'sucrose', 'glucose and fructose'), ('pectinase', 'pectin', 'soluble sugars')]


@t.add('C3', (1, 2, 3), 'short')
def enz_sub(r, D):
    e, s_, p = r.choice(ENZ)
    if D <= 2:
        mode = r.randrange(2)
        if mode == 0:
            return MQ(r, f'Which substance is the substrate of {e}?', s_, [x[1] for x in ENZ if x[0] != e], f'{cap(e)}: {s_} → {p}.')
        return MQ(r, f'Which enzyme breaks down {s_}?', e, [x[0] for x in ENZ if x[0] != e], f'{cap(e)}: {s_} → {p}.')
    e2, s2, p2 = r.choice([x for x in ENZ if x[0] != e])
    return Q(f'(a) Name the products when {e} acts on {s_}. (b) Explain why {e} cannot act on {s2}.', f'(a) {p} (b) The active site of {e} is complementary to {s_} only; {s2} does not fit.',
             f'(a) {p} [1] (b) active site shape specific / complementary to {s_} [1]; {s2} cannot bind / no enzyme–substrate complex [1] [3]', 'short', 3)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def enz_rate(r, D):
    v = r.choice([12, 18, 24, 30, 36, 45, 48, 60])
    tm = r.choice([30, 40, 60, 90, 120, 150])
    rate = v / tm * 60
    st = f'Catalase from {r.choice(["potato", "liver", "yeast", "celery"])} released {v} cm³ of oxygen from hydrogen peroxide in {tm} s. Calculate the mean rate of oxygen production in cm³ per minute.'
    key = f'{v} ÷ {tm} = {fx(v / tm, 3)} cm³/s [1]; × 60 = {fx(rate, 2)} cm³/min [1] [2]'
    m = 2
    if D >= 4:
        f = r.choice([2, 0.5])
        st += f' Predict the volume of oxygen released in the same time if the enzyme concentration is {"doubled" if f == 2 else "halved"} (substrate in excess), and explain.'
        key = key.replace(' [2]', f'; {fx(v * f)} cm³ [1]; {"twice" if f == 2 else "half"} as many active sites so more / fewer enzyme–substrate complexes per second [1] [4]')
        m = 4
    return Q(st, f'{fx(rate, 2)} cm³/min' + (f'; about {fx(v * f)} cm³' if D >= 4 else ''), key, 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def enz_case(r, D):
    e, s_, p = r.choice(ENZ[:4])
    intro = f'{person(r)} investigates the enzyme {e}, which breaks down {s_} into {p}, in a laboratory in {city(r)}.'
    parts = [lambda r: ('Name the substrate and the product(s) of this reaction.', f'substrate {s_}; product(s) {p}', '[2]'),
             lambda r: ('Describe how the enzyme and substrate interact. Use the term enzyme–substrate complex.', 'Substrate fits into the complementary active site, forming an enzyme–substrate complex; the substrate is broken down and products leave the active site.', 'fit into active site [1]; ES complex [1]; products released [1] [3]'),
             lambda r: ('Explain why increasing the substrate concentration increases the rate only up to a point.', 'More substrate means more collisions and ES complexes; eventually all active sites are occupied, so enzyme concentration becomes limiting.', 'more collisions / complexes [1]; active sites saturated [1] [2]'),
             lambda r: ('Suggest a suitable control for this investigation.', 'Use boiled (denatured) enzyme instead of active enzyme, to show that the enzyme causes the reaction.', 'boiled enzyme [1]; shows the enzyme is responsible [1] [2]'),
             lambda r: ('Explain why the enzyme is described as a catalyst.', 'It speeds up the reaction and is not changed or used up by it.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how enzymes work, using the lock and key idea, and explain why each enzyme is specific.', 'Enzymes are proteins with an active site of specific shape; the substrate is complementary (lock and key) and fits, forming an ES complex; reaction happens and products released; enzyme reused; other substrates do not fit so enzyme is specific.',
           'protein / catalyst [1]; active site shape [1]; ES complex [1]; products released enzyme reused [1]; specificity explained [1] [5]')])
t_c5a = t

t = T('Effect of temperature on enzyme activity; denaturation', 'effect of temperature on enzyme activity', 'denaturation')
facts(t, [('optimum temperature', 'the temperature at which an enzyme works fastest'), ('denaturation', 'a permanent change in the shape of an enzyme\'s active site, caused by high temperature or extreme pH, so the substrate can no longer fit'),
          ('kinetic energy', 'the energy of moving molecules, which increases with temperature'), ('rate of reaction', 'how quickly substrate is used or product is formed per unit time'),
          ('collision', 'contact between enzyme and substrate molecules, which is needed to form an enzyme–substrate complex')])
mcqs(t, [('What is the optimum temperature of most human enzymes?', 'About 37 °C', 'Human enzymes work fastest at about body temperature.', ['About 0 °C', 'About 60 °C', 'About 100 °C']),
         ('Why does the rate of an enzyme reaction fall at temperatures above the optimum?', 'The active site changes shape so the substrate no longer fits', 'Denaturation: bonds in the protein break and the active site changes shape.', ['The enzyme molecules are killed', 'The substrate molecules stop moving', 'The enzyme is digested by other enzymes']),
         ('Amylase is kept at 5 °C. What happens to it?', 'It works slowly but is not denatured', 'Low temperature reduces kinetic energy and collisions; activity returns when warmed.', ['It is denatured', 'It works at its maximum rate', 'It turns into maltose'])])
shorts(t, [('State what is meant by the optimum temperature of an enzyme.', 'The temperature at which the enzyme works fastest / has its greatest activity.', '[1]'),
           ('State why enzymes from bacteria living in hot springs can work at 80 °C.', 'Their active sites keep their shape at high temperature (higher optimum; not denatured at 80 °C).', '[1]')])
explain(t, [('Explain why the rate of an enzyme-controlled reaction increases from 10 °C to 35 °C.', 'Molecules gain kinetic energy and move faster, so enzyme and substrate collide more often, forming more enzyme–substrate complexes per second.', 'more kinetic energy [1]; more frequent collisions / ES complexes [1] [2]'),
            ('Explain why an enzyme that has been boiled does not work when it is cooled again.', 'Boiling denatures the enzyme: the active site changes shape permanently, so the substrate can no longer fit even when cooled.', 'denatured [1]; permanent change in active site shape [1] [2]'),
            ('Explain the difference between the effect of a low temperature and a high temperature on an enzyme.', 'Low temperature: fewer collisions, slow rate, but enzyme not damaged and activity returns on warming. High temperature: enzyme denatured, active site permanently changed, activity lost.', 'low = slow but reversible [1]; high = denatured, permanent [1] [2]'),
            ('A person has a fever of 41 °C. Suggest why a very high fever can be dangerous.', 'Enzymes in the body start to denature above the optimum, so metabolic reactions slow down.', 'enzymes denature [1]; reactions slow [1] [2]')])
myths(t, [('Enzymes are killed at high temperatures.', 'Enzymes are not alive; they are denatured — the active site changes shape.'),
           ('At low temperature enzymes are denatured.', 'At low temperature enzymes are inactive or slow but not denatured; they work again when warmed.'),
           ('Above the optimum temperature the rate falls because molecules move more slowly.', 'Molecules move faster above the optimum, but the enzyme is denatured, so fewer substrate molecules fit.')])

ENZ_T = {'setup': lambda r, p: f'{p} mixed amylase with starch solution at different temperatures. A drop of the mixture was added to iodine solution every 30 seconds, and the time until the iodine no longer turned blue-black was recorded.',
         'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[10, 20, 30, 40, 50, 60], [15, 25, 35, 45, 55], [20, 30, 40, 50, 60], [25, 30, 35, 40, 45, 50, 55]]),
         'dv': ('time for starch to disappear', 's'), 'y': lambda x, k: 60 + 8 * (38 * k - x) ** 1.5 if x < 38 * k else 60 + (x - 38 * k) ** 2 * 0.9, 'dp': 0, 'noise': 0.05,
         'controls': ['volume and concentration of amylase', 'volume and concentration of starch', 'pH (buffer)', 'interval between samples', 'volume of iodine'],
         'trend': None,
         'why': ('Up to the optimum, molecules gain kinetic energy, collide more often and form more enzyme–substrate complexes, so starch is broken down faster (shorter time). Above the optimum the enzyme is denatured: the active site changes shape so starch no longer fits and the time increases.', 'more kinetic energy / collisions below optimum [1]; ES complexes [1]; denaturation above optimum [1]; active site shape changed [1] [4]'),
         'improve': ['test more often than every 30 s to time the end-point more precisely', 'leave the enzyme and starch at the temperature for 5 minutes before mixing (equilibrate)', 'use a thermostatically controlled water bath'],
         'control': 'Use boiled amylase (or water instead of amylase) with starch at each temperature; the iodine should stay blue-black, showing that the amylase causes the breakdown of starch.',
         'extra': [lambda r, d: ('Calculate the rate of reaction at the optimum temperature, using rate = 1000 ÷ time.', f'{fx(1000 / min(d["means"]), 1)} s⁻¹ (arbitrary units)', f'shortest mean time = {fx(min(d["means"]), 1)} s [1]; 1000 ÷ {fx(min(d["means"]), 1)} = {fx(1000 / min(d["means"]), 1)} [1] [2]'),
                   lambda r, d: ('Estimate the optimum temperature of the amylase from these results.', f'About {fx(d["xs"][min(range(len(d["means"])), key=lambda i: d["means"][i])], 0)} °C (shortest time).', 'temperature with shortest time [1]; need more readings around it to be precise [1] [2]')]}
ENZ_T['trend'] = lambda d: trend_text('temperature', 'time for starch to disappear', d['xs'], d['means'], '°C') + ' (A shorter time means a faster rate.)'
add_practical(t, ENZ_T, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4), 'numerical')
def temp_rate(r, D):
    temps = r.choice([[20, 30, 40, 50], [25, 35, 45, 55], [10, 25, 40, 55]])
    opt = r.choice([35, 37, 40, 42])
    times = [round(40 + abs(x - opt) ** 1.8 / 2.5 + (abs(x - opt) ** 2.2 / 5 if x > opt else 0)) for x in temps]
    rates = [1000 / t_ for t_ in times]
    i = r.randrange(len(temps))
    if D == 1:
        return NQ(r, f'An enzyme reaction finishes in {times[i]} s at {temps[i]} °C. Using rate = 1000 ÷ time, what is the rate?', rates[i], [times[i] / 1000, 1000 * times[i] / 100, rates[i] * 10, 100 / times[i]], ' s⁻¹', f'1000 ÷ {times[i]} = {fx(rates[i], 1)}.', f=lambda v: fx(v, 1))
    tab = ', '.join(f'{x} °C: {t_} s' for x, t_ in zip(temps, times))
    st = f'The time taken for an enzyme reaction to finish was measured at four temperatures: {tab}. Calculate the rate (1000 ÷ time) at each temperature and state the temperature at which the enzyme was most active.'
    best = temps[times.index(min(times))]
    ans = '; '.join(f'{x} °C: {fx(rt, 1)}' for x, rt in zip(temps, rates)) + f'. Most active at {best} °C.'
    key = '; '.join(fx(rt, 1) for rt in rates) + f' (all four [2]; two or three [1]); {best} °C [1]'
    m = 3
    if D >= 4:
        st += ' Explain why the rate is lower at the highest temperature.'
        ans += ' At the highest temperature the enzyme is denatured: the active site changes shape so fewer substrate molecules fit.'
        key += '; denaturation [1]; active site shape changed / fewer ES complexes [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def temp_case(r, D):
    org = r.choice([('a human', 37), ('a bacterium from a hot spring', 75), ('a fish from polar seas', 10), ('a desert lizard', 42)])
    intro = f'Scientists extracted the same type of enzyme from {org[0]}. The enzyme has an optimum temperature of about {org[1]} °C.'
    parts = [lambda r: (f'Sketch-describe the shape of the graph of rate against temperature for this enzyme from 0 °C to {org[1] + 30} °C.', f'Rate rises gradually to a peak at about {org[1]} °C, then falls steeply to zero by about {org[1] + 20} °C.', 'gradual rise [1]; peak at optimum [1]; steep fall [1] [3]'),
             lambda r: (f'Explain why the enzyme from {org[0]} has an optimum of about {org[1]} °C.', f'The organism lives / its cells are at about {org[1]} °C; enzymes have evolved active sites that are stable and most effective at that temperature.', 'matches body / habitat temperature [1]; active site stable [1] [2]'),
             lambda r: (f'Predict what would happen to the activity of the enzyme if it were kept at {org[1] + 25} °C for 10 minutes and then cooled to {org[1]} °C. Explain.', 'Little or no activity: the enzyme was denatured at the high temperature and the change in the active site is permanent.', 'no recovery [1]; denatured permanently [1] [2]'),
             lambda r: ('Suggest why enzymes from organisms living in hot springs are useful in industry.', 'They work at high temperatures where reactions are faster and are not denatured; e.g. used in DNA copying or washing powders.', 'stable at high temperature [1]; valid use [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe and explain the effect of temperature on the rate of an enzyme-catalysed reaction.', 'Rate increases with temperature up to the optimum because molecules have more kinetic energy and collide more often, forming more ES complexes. Above the optimum the enzyme denatures: bonds break and the active site changes shape, so substrate no longer fits; rate falls to zero.',
           'increase described [1]; kinetic energy / collisions [1]; optimum [1]; denaturation [1]; active site shape [1] [5]')])
t_c5b = t

t = T('Effect of pH on enzyme activity and investigating enzyme action', 'effect of ph on enzyme activity', 'investigating enzyme action')
facts(t, [('optimum pH', 'the pH at which an enzyme works fastest'), ('buffer solution', 'a solution that keeps the pH constant at a chosen value'),
          ('pH', 'a measure of how acidic or alkaline a solution is'), ('catalase', 'an enzyme in many tissues that breaks down hydrogen peroxide into water and oxygen'),
          ('pepsin', 'a protease in the stomach with an optimum pH of about 2')])
mcqs(t, [('The enzyme pepsin works in the stomach. What is its optimum pH likely to be?', 'pH 2', 'The stomach contains hydrochloric acid; pepsin works best in acid.', ['pH 7', 'pH 9', 'pH 12']),
         ('Why does an enzyme stop working at a pH far from its optimum?', 'The active site changes shape', 'Extreme pH changes the shape of the protein, denaturing the active site.', ['The enzyme molecules move too fast', 'The substrate is used up', 'The temperature rises']),
         ('Which is used to keep the pH constant in an enzyme investigation?', 'A buffer solution', 'Buffers resist changes in pH.', ['A water bath', 'Iodine solution', "Benedict's solution"])])
shorts(t, [('State two variables that must be controlled when investigating the effect of pH on amylase.', 'Temperature; concentration and volume of amylase and of starch.', 'any two [2]'),
           ('State the optimum pH of salivary amylase.', 'About pH 7 (neutral).', '[1]')])
explain(t, [('Explain why amylase from saliva stops working when it reaches the stomach.', 'The stomach has a low pH (acid); this is far from the optimum of amylase (about pH 7), so the active site changes shape and amylase is denatured.', 'stomach acidic [1]; active site shape changed / denatured [1] [2]'),
            ('Explain why different enzymes in the digestive system have different optimum pH values.', 'Each enzyme works in a region with a particular pH (stomach acid, small intestine slightly alkaline); each has an active site shape that is most stable at that pH.', 'different pH in regions [1]; active site best at that pH [1] [2]'),
            ('Explain how you could use a pH meter or universal indicator paper to check that a buffer is working during an enzyme experiment.', 'Measure the pH of each mixture at the start and end; if the buffer is working, the pH stays the same.', 'measure before and after [1]; pH unchanged [1] [2]'),
            ('Explain why the volume of oxygen collected from catalase and hydrogen peroxide can be used to measure the rate of reaction.', 'Oxygen is a product; the more oxygen produced per minute, the faster the substrate is being broken down.', 'oxygen is a product [1]; volume per unit time = rate [1] [2]')])
myths(t, [('All enzymes work best at pH 7.', 'Each enzyme has its own optimum pH; pepsin works best at about pH 2.'),
           ('Acid kills enzymes in the stomach.', 'Enzymes are not alive; an unsuitable pH denatures them by changing the shape of the active site.')])

ENZ_PH = {'setup': lambda r, p: f'{p} added discs of potato (containing catalase) to hydrogen peroxide solution buffered at different pH values and measured the volume of oxygen collected in 2 minutes.',
          'iv': ('pH', ''), 'xfmt': lambda v: f'pH {v}', 'xs': lambda r: r.choice([[4, 5, 6, 7, 8, 9], [3, 5, 7, 9, 11], [5, 6, 7, 8, 9, 10]]),
          'dv': ('volume of oxygen', 'cm³'), 'y': lambda x, k: max(1.5, 30 * k * math.exp(-((x - 7.5 * (0.95 + 0.1 * (k - 0.88) / 0.24)) ** 2) / 4)), 'dp': 1, 'noise': 0.05,
          'controls': ['temperature', 'volume and concentration of hydrogen peroxide', 'number and size of potato discs', 'time of collection'],
          'why': ('Near the optimum pH the active site has the correct shape and many enzyme–substrate complexes form. At pH values further from the optimum the active site changes shape (the enzyme is denatured), so fewer substrate molecules fit and less oxygen is released.', 'optimum pH named / active site fits [1]; shape changes away from optimum [1]; fewer ES complexes [1] [3]'),
          'improve': ['use a gas syringe instead of counting bubbles for more accurate volumes', 'cut potato discs with a cork borer to the same size and mass', 'keep the temperature constant with a water bath'],
          'control': 'Use boiled potato discs at each pH; no oxygen should be released, showing the enzyme causes the reaction.',
          'extra': [lambda r, d: ('Calculate the rate of oxygen production at the pH that gave the greatest volume, in cm³ per minute.', f'{fx(max(d["means"]) / 2, 2)} cm³/min', f'greatest mean = {fx(max(d["means"]), 2)} cm³ [1]; ÷ 2 = {fx(max(d["means"]) / 2, 2)} cm³/min [1] [2]')]}
add_practical(t, ENZ_PH, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4), 'short')
def ph_where(r, D):
    cases = [('pepsin', 'stomach', 2), ('salivary amylase', 'mouth', 7), ('pancreatic lipase', 'small intestine', 8), ('trypsin (a protease)', 'small intestine', 8), ('catalase', 'liver cells', 7)]
    e, where, ph = r.choice(cases)
    if D <= 2:
        return NQ(r, f'{cap(e)} acts in the {where}. Which is most likely to be its optimum pH?', ph, [x for x in (2, 4, 7, 8, 10, 12) if x != ph], '', f'{cap(e)} works in the {where}, optimum about pH {ph}.', f=lambda v: f'pH {int(v)}')
    e2, w2, ph2 = r.choice([c for c in cases if c[2] != ph])
    return Q(f'{cap(e)} works in the {where} and {e2} works in the {w2}. (a) Suggest the optimum pH of each enzyme. (b) Predict what would happen to {e} if it were placed in conditions at pH {ph2}, and explain.',
             f'(a) {e}: about pH {ph}; {e2}: about pH {ph2} (b) It would work slowly or not at all because the active site changes shape (denatured) away from its optimum pH.',
             f'(a) both pH values [2] (b) activity falls [1]; active site shape changes / denatured [1] [4]', 'short', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def ph_plan(r, D):
    e = r.choice([('amylase', 'starch', 'iodine solution', 'time until iodine no longer turns blue-black'), ('catalase', 'hydrogen peroxide', 'a gas syringe', 'volume of oxygen collected in 1 minute'),
                  ('protease', 'milk powder suspension (cloudy)', 'a timer', 'time for the milk to become clear')])
    intro = f'{person(r)} plans an investigation into the effect of pH on the activity of {e[0]} using {e[1]}, measuring the {e[3]}.'
    parts = [lambda r: ('Describe a method for this investigation.', f'Use buffer solutions of pH 3, 5, 7, 9, 11; equal volumes of {e[0]} and {e[1]} in each; same temperature (water bath); measure the {e[3]}; repeat three times.', 'range of at least five pH values with buffers [1]; same volumes / concentrations [1]; same temperature [1]; measurement [1]; repeats [1] [5]'),
             lambda r: ('Identify the independent and dependent variables.', f'Independent: pH; dependent: {e[3]}.', '[2]'),
             lambda r: ('Explain why the solutions should be placed in the water bath for several minutes before mixing.', 'So that the enzyme and substrate reach the required temperature before the reaction starts; temperature is controlled.', '[2]'),
             lambda r: ('State one safety precaution.', 'Wear eye protection (hydrogen peroxide / acid and alkali buffers can be irritant).', '[1]'),
             lambda r: ('Predict the results, giving a reason.', 'Activity is greatest near the optimum pH (about 7 for most, 2 for pepsin) and falls at more acidic or alkaline pH because the active site changes shape.', 'peak at optimum [1]; denaturation explanation [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Plan an investigation to find the optimum pH of amylase.', 'Mix equal volumes of amylase and starch in buffers at pH 4–10; keep at 37 °C in a water bath; every 30 s test a drop with iodine on a spotting tile; record time until no blue-black; repeat 3 times; calculate mean; optimum = shortest time; control with boiled amylase.',
           'buffers / pH range [1]; constant temperature [1]; iodine sampling method [1]; repeats and mean [1]; control [1]; identify optimum [1] [6]')])
t_c5c = t
CHAPTERS[5] = [t_c5a, t_c5b, t_c5c]


# ===================================================================== 6 Plant nutrition
t = T('Photosynthesis: word and balanced chemical equations; role of chlorophyll', 'photosynthesis: word and balanced chemical equations', 'role of chlorophyll')
facts(t, [('photosynthesis', 'the process by which plants synthesise carbohydrates from raw materials using energy from light'),
          ('chlorophyll', 'a green pigment found in chloroplasts that transfers light energy into chemical energy in molecules for the synthesis of carbohydrates'),
          ('chloroplast', 'the organelle in which photosynthesis takes place'), ('destarching', 'keeping a plant in the dark for 48 hours so that the starch in its leaves is used up'),
          ('variegated leaf', 'a leaf with green areas that contain chlorophyll and white areas that do not')])
mcqs(t, [('Which is the balanced equation for photosynthesis?', '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂', 'Carbon dioxide + water → glucose + oxygen, in light with chlorophyll.', ['C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', '6CO₂ + 6O₂ → C₆H₁₂O₆ + 6H₂O', 'CO₂ + H₂O → C₆H₁₂O₆ + O₂']),
         ('What is the role of chlorophyll in photosynthesis?', 'It transfers light energy into chemical energy', 'Chlorophyll absorbs light; the energy is used to make carbohydrates.', ['It absorbs carbon dioxide from the air', 'It releases oxygen from glucose', 'It transports water to the leaf']),
         ('Why is a plant destarched before testing a leaf for starch?', 'So that any starch found must have been made during the experiment', 'Starch present at the start would give a false positive.', ['To kill the leaf cells', 'To make the leaf green', 'To remove the chlorophyll'])])
shorts(t, [('Write the word equation for photosynthesis.', 'carbon dioxide + water → glucose + oxygen (in light, with chlorophyll)', 'reactants [1]; products [1] [2]'),
           ('State four uses of the glucose made in photosynthesis.', 'Respiration; converted to starch for storage; cellulose for cell walls; sucrose for transport; amino acids (with nitrate) / fats and oils / nectar.', 'any four [2]')])
explain(t, [('Describe how to test a leaf for starch.', 'Boil the leaf in water to kill it and break membranes; boil in ethanol (hot water bath) to remove chlorophyll; dip in water to soften; add iodine; blue-black shows starch.', 'boil in water [1]; ethanol to decolourise [1]; iodine → blue-black [1] [3]'),
            ('A variegated leaf is tested for starch. Explain why only the green parts turn blue-black.', 'Only the green parts contain chlorophyll, which absorbs light for photosynthesis; white parts cannot photosynthesise so do not make starch.', 'chlorophyll needed [1]; only green parts make starch [1] [2]'),
            ('Explain why the leaf is placed in boiling water and then in hot ethanol in the starch test.', 'Boiling water kills the cells and breaks down membranes so iodine can enter; ethanol dissolves chlorophyll so the colour change can be seen.', 'membranes broken [1]; chlorophyll removed so colour visible [1] [2]'),
            ('Explain why plants convert glucose to starch for storage.', 'Starch is insoluble, so it does not affect the water potential of cells, and it is compact; it can be converted back to glucose when needed.', 'insoluble [1]; no effect on osmosis [1] [2]'),
            ('Explain why a leaf kept in a flask containing sodium hydroxide (which absorbs CO₂) does not make starch.', 'Carbon dioxide is a raw material for photosynthesis; without it no glucose and therefore no starch can be made.', 'CO₂ absorbed / not available [1]; needed to make glucose [1] [2]'),
            ('Explain why hydrogencarbonate indicator around a water plant turns purple in bright light.', 'In bright light the rate of photosynthesis is greater than respiration, so the plant takes in carbon dioxide; less CO₂ makes the indicator purple.', 'photosynthesis > respiration [1]; CO₂ removed [1] [2]')])
myths(t, [('Plants get their food from the soil through their roots.', 'Plants make their own carbohydrates by photosynthesis; the soil provides water and mineral ions only.'),
           ('Chlorophyll is used up during photosynthesis.', 'Chlorophyll is not used up; it absorbs light energy and transfers it to chemical energy.'),
           ('Photosynthesis produces carbon dioxide.', 'Photosynthesis uses carbon dioxide and produces glucose and oxygen.')])

HCI = {'yellow': 'high carbon dioxide (respiration greater than photosynthesis)', 'orange': 'slightly increased carbon dioxide', 'red': 'atmospheric carbon dioxide (no net change)',
       'purple': 'low carbon dioxide (photosynthesis greater than respiration)'}


@t.add('C3', (1, 2, 3, 4), 'case')
def hci(r, D):
    tubes = [('A', 'with a leaf, in bright light', 'purple'), ('B', 'with a leaf, covered in foil (dark)', 'yellow'), ('C', 'with a leaf, covered in thin gauze (dim light)', 'red'), ('D', 'with no leaf, in bright light', 'red ')]
    org = r.choice(['leaf', 'piece of pondweed', 'leaf disc sample'])
    tubes = [(a, b.replace('a leaf', 'a ' + org), c) for a, b, c in tubes]
    pick = r.sample(tubes, 3 if D <= 2 else 4)
    pick.sort()
    pick = [(a, b, c) for a, b, c in pick]
    st = 'Hydrogencarbonate indicator is red at atmospheric CO₂ concentration, yellow at high CO₂ and purple at low CO₂. Tubes were set up and left for 2 hours: ' + '; '.join(f'tube {a} {b}' for a, b, c in pick) + '.'
    if D == 1:
        a, b, c = pick[0]
        return MQ(r, st + f' What colour would the indicator in tube {a} be?', c.strip(), ['yellow', 'red', 'purple', 'blue', 'orange'], f'Tube {a}: {HCI[c.strip()]}.')
    st += ' Predict the colour of the indicator in each tube and explain each prediction.'
    expl = {'purple': 'photosynthesis faster than respiration, CO₂ taken in', 'yellow': 'only respiration, CO₂ released', 'red': 'photosynthesis and respiration about equal (compensation point), no net change',
            'red ': 'no living material, so no change (control)'}
    ans = '; '.join(f'{a}: {c.strip()} — {expl[c]}' for a, b, c in pick)
    m = 2 * len(pick)
    if D >= 4:
        st += ' State the purpose of the tube with no living material, if included.'
        ans += '; the tube without a plant is a control, showing that light alone does not change the indicator.'
    return Q(st, ans, '; '.join(f'{a}: {c.strip()} [1], reason [1]' for a, b, c in pick) + f' [{m}]', 'case', m)


@t.add('C3', (2, 3, 4), 'short')
def ps_moles(r, D):
    n = r.choice([2, 3, 4, 5, 8, 10, 12])
    st = f'Use the balanced equation for photosynthesis, 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. How many molecules of carbon dioxide are needed to make {fx(n)} molecules of glucose, and how many molecules of oxygen are released?'
    return Q(st, f'{fx(6 * n)} CO₂ molecules; {fx(6 * n)} O₂ molecules', f'ratio 6 CO₂ : 1 glucose : 6 O₂ [1]; {fx(6 * n)} and {fx(6 * n)} [1] [2]', 'short', 2)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def ps_starch(r, D):
    cond = r.choice([('a variegated leaf', 'only the green areas turn blue-black', 'chlorophyll'), ('a leaf partly covered with a strip of black paper', 'the covered strip stays orange-brown; the rest turns blue-black', 'light'),
                     ('a leaf enclosed in a flask containing soda lime (absorbs CO₂)', 'the leaf stays orange-brown', 'carbon dioxide')])
    p = person(r)
    intro = f'{p} destarches a potted plant, then leaves {cond[0]} in light for 6 hours before testing it for starch. Result: {cond[1]}.'
    parts = [lambda r: ('Explain why the plant was destarched first.', 'To remove starch already present, so any starch found was made during the experiment.', 'removes starch [1]; fair test / starch must come from photosynthesis in experiment [1] [2]'),
             lambda r: ('Describe how the plant was destarched.', 'It was kept in the dark for about 48 hours.', '[1]'),
             lambda r: ('Describe how the leaf is tested for starch.', 'Boil in water, then in ethanol in a hot water bath, rinse, add iodine solution.', 'water [1]; ethanol [1]; iodine [1] [3]'),
             lambda r: ('State the conclusion of this investigation.', f'{cap(cond[2])} is needed for photosynthesis.', '[1]'),
             lambda r: ('State why ethanol must be heated in a water bath, not with a flame.', 'Ethanol is flammable.', '[1]'),
             lambda r: ('Write the balanced equation for photosynthesis.', '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂', 'formulae [1]; balancing [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how a plant makes and uses the glucose produced in photosynthesis.', 'Chlorophyll in chloroplasts absorbs light; energy used to combine CO₂ (from air via stomata) and water (from roots via xylem) to make glucose, releasing oxygen. Glucose used for respiration, stored as starch, made into cellulose, sucrose for transport, amino acids with nitrate ions, fats and oils.',
           'raw materials and source [1]; chlorophyll / light [1]; products [1]; three uses [3] [6]')])
t_c6a = t

t = T('Investigating limiting factors: light intensity, carbon dioxide and temperature', 'investigating limiting factors', 'light intensity, carbon dioxide and temperature')
facts(t, [('limiting factor', 'something present in the environment in such short supply that it restricts life processes'), ('light intensity', 'the amount of light energy reaching a given area; it decreases as the distance from the lamp increases'),
          ('rate of photosynthesis', 'the amount of product made (e.g. oxygen) or reactant used per unit time'), ('compensation point', 'the light intensity at which the rate of photosynthesis equals the rate of respiration'),
          ('greenhouse', 'a glass or plastic structure where temperature, light and carbon dioxide can be controlled to increase crop yield')])
mcqs(t, [('At low light intensity, which factor limits the rate of photosynthesis?', 'Light intensity', 'Increasing the limiting factor increases the rate.', ['Carbon dioxide concentration', 'Temperature', 'Oxygen concentration']),
         ('A lamp is moved from 20 cm to 10 cm from a plant. By what factor does the light intensity increase?', '4', 'Light intensity ∝ 1/distance²: halving the distance gives 2² = 4 times the intensity.', ['2', '0.5', '8']),
         ('Why does a farmer burn paraffin in a greenhouse in winter?', 'To increase carbon dioxide concentration and temperature', 'Combustion releases CO₂ and heat, both of which can be limiting.', ['To decrease humidity', 'To kill all insects', 'To increase oxygen concentration'])])
shorts(t, [('State three factors that can limit the rate of photosynthesis.', 'Light intensity, carbon dioxide concentration, temperature.', 'all three [2]; two [1] [2]'),
           ('State why a beaker of water is placed between the lamp and the pondweed.', 'To absorb heat from the lamp so that temperature stays constant.', '[1]')])
explain(t, [('Explain why the rate of photosynthesis stops increasing at high light intensity.', 'Another factor, such as carbon dioxide concentration or temperature, becomes limiting, so extra light has no effect.', 'another factor limiting [1]; named example [1] [2]'),
            ('Explain why increasing temperature above about 40 °C decreases the rate of photosynthesis.', 'The enzymes that catalyse photosynthesis become denatured; their active sites change shape.', 'enzymes [1]; denatured [1] [2]'),
            ('Explain why counting bubbles is not an accurate way to measure the rate of photosynthesis of pondweed.', 'Bubbles may be different sizes and some gas may dissolve in water; measuring the volume of gas in a gas syringe or capillary tube is more accurate.', 'bubble size varies [1]; better method [1] [2]'),
            ('Explain why the rate of photosynthesis is higher on a warm sunny day than on a cold sunny day, even though light intensity is the same.', 'Photosynthesis is controlled by enzymes; at higher temperatures molecules have more kinetic energy and collide more often, so temperature was limiting on the cold day.', 'temperature limiting [1]; enzymes / kinetic energy [1] [2]'),
            ('Explain why a greenhouse owner might not increase carbon dioxide above a certain concentration.', 'Above that level another factor (light or temperature) limits the rate, so the extra CO₂ gives no extra yield and costs money.', 'another factor limiting [1]; cost vs benefit [1] [2]')])
myths(t, [('Doubling the distance of the lamp halves the light intensity.', 'Light intensity is proportional to 1/distance², so doubling the distance reduces it to a quarter.'),
           ('The higher the temperature, the faster the rate of photosynthesis, at any temperature.', 'Above the optimum, enzymes are denatured and the rate falls.')])


def _lux(d, k):
    rel = 10000 / d ** 2
    return k * 60 * rel / (rel + 25) + 0.5


PS_L = {'setup': lambda r, p: f'{p} placed a piece of pondweed in a beaker of dilute sodium hydrogencarbonate solution and counted the bubbles of gas released in one minute with a lamp at different distances.',
        'iv': ('distance of lamp from pondweed', 'cm'), 'xs': lambda r: r.choice([[10, 20, 30, 40, 50], [5, 10, 15, 20, 25, 30], [10, 15, 20, 30, 40]]),
        'dv': ('number of bubbles per minute', 'bubbles/min'), 'y': lambda x, k: _lux(x, k), 'dp': 0, 'noise': 0.06,
        'controls': ['temperature of the water', 'concentration of sodium hydrogencarbonate (CO₂)', 'same piece / mass of pondweed', 'time allowed to adjust before counting', 'type of lamp / no other light'],
        'why': ('Closer to the lamp the light intensity is higher (∝ 1/d²), so more light energy is absorbed by chlorophyll and the rate of photosynthesis, and oxygen production, is greater. At the shortest distances another factor such as CO₂ or temperature may limit the rate.', 'light intensity greater when closer [1]; more photosynthesis / oxygen [1]; limiting factor at short distance [1] [3]'),
        'improve': ['measure the volume of gas with a gas syringe instead of counting bubbles', 'place a heat shield (beaker of water) between lamp and plant', 'carry out the experiment in a dark room'],
        'extra': [lambda r, d: (f'Calculate the relative light intensity at {fx(d["xs"][0])} cm and at {fx(d["xs"][1])} cm, using light intensity = 1 ÷ distance².', f'{sci(1 / d["xs"][0] ** 2, 3)} and {sci(1 / d["xs"][1] ** 2, 3)} (arbitrary units)',
                                f'1 ÷ {fx(d["xs"][0])}² = {sci(1 / d["xs"][0] ** 2, 3)} [1]; 1 ÷ {fx(d["xs"][1])}² = {sci(1 / d["xs"][1] ** 2, 3)} [1] [2]'),
                  lambda r, d: ('Name the gas in the bubbles and describe a test to confirm it.', 'Oxygen: it relights a glowing splint.', 'oxygen [1]; relights glowing splint [1] [2]')]}
PS_L['trend'] = lambda d: 'As the distance from the lamp increases, the number of bubbles per minute decreases (light intensity falls).'
PS_C = {'setup': lambda r, p: f'{p} placed equal lengths of pondweed in solutions of sodium hydrogencarbonate of different concentrations, with the lamp at a fixed distance, and measured the volume of oxygen produced in 5 minutes.',
        'iv': ('concentration of sodium hydrogencarbonate', '%'), 'xs': lambda r: r.choice([[0, 0.5, 1.0, 1.5, 2.0, 2.5], [0, 0.25, 0.5, 1.0, 2.0], [0.2, 0.4, 0.6, 0.8, 1.0]]),
        'dv': ('volume of oxygen', 'mm³'), 'y': lambda x, k: 4 + 80 * k * (1 - math.exp(-x / 0.6)), 'dp': 0,
        'controls': ['light intensity / distance of lamp', 'temperature', 'length / mass of pondweed', 'time of collection'],
        'why': ('Sodium hydrogencarbonate releases carbon dioxide, a raw material of photosynthesis; at low concentrations CO₂ is limiting so more CO₂ increases the rate; at high concentrations another factor (light or temperature) limits the rate, so the curve levels off.', 'CO₂ is a raw material [1]; CO₂ limiting at low concentration [1]; another factor limiting at high concentration [1] [3]'),
        'improve': ['use a water bath to keep the temperature constant', 'leave the pondweed to adjust for 5 minutes at each concentration']}
add_practical(t, PS_L, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))
add_practical(t, PS_C, C3D=(3, 4), C4D=(4, 5))


@t.add('C3', (1, 2, 3, 4), 'numerical')
def inv_sq(r, D):
    d1 = r.choice([10, 15, 20, 25, 30, 40])
    f = r.choice([2, 0.5, 3, 1 / 3, 1.5])
    d2 = d1 * f
    ratio = (d1 / d2) ** 2
    word = 'moved closer to' if d2 < d1 else 'moved further from'
    st = f'A lamp is {word} a plant, from {fx(d1)} cm to {fx(d2)} cm. By what factor does the light intensity change? (light intensity ∝ 1 ÷ distance²)'
    st2 = f'A lamp is {word} a plant, from {fx(d1)} cm to {fx(d2)} cm. Using light intensity ∝ 1 ÷ distance², calculate the factor by which the light intensity changes.'
    if D == 1:
        return NQ(r, st, ratio, [1 / f, f, ratio * 2, 1 / ratio if ratio != 1 else 3], '×', f'({fx(d1)} ÷ {fx(d2)})² = {fx(ratio, 3)}.', f=lambda v: fx(v, 3))
    if D == 2:
        return Q(st2, f'×{fx(ratio, 3)}', f'ratio of distances {fx(d1)} ÷ {fx(d2)} [1]; squared = {fx(ratio, 3)} [1] [2]', 'numerical', 2)
    st = st2 + ' Predict the effect on the rate of photosynthesis, assuming light is the limiting factor.'
    return Q(st, f'×{fx(ratio, 3)}; rate {"increases" if ratio > 1 else "decreases"} (but not necessarily by the same factor).',
             f'({fx(d1)} ÷ {fx(d2)})² [1] = {fx(ratio, 3)} [1]; rate {"increases" if ratio > 1 else "decreases"} [1] [3]', 'numerical', 3)


@t.add('C4', (3, 4, 5), 'case')
def lim_green(r, D):
    lo, hi = r.choice([(0.04, 0.1), (0.03, 0.12), (0.04, 0.15)])
    y1 = r.randrange(40, 60)
    y2 = round(y1 * r.uniform(1.25, 1.6))
    intro = f'A tomato grower in {city(r)} increases the carbon dioxide concentration in a greenhouse from {lo}% to {hi}% and the yield rises from {y1} kg to {y2} kg per row.'
    parts = [lambda r: ('Calculate the percentage increase in yield.', f'{fx(pct(y1, y2), 1)}%', f'({y2} − {y1}) ÷ {y1} × 100 [1] = {fx(pct(y1, y2), 1)}% [1] [2]'),
             lambda r: ('Explain why increasing carbon dioxide increased the yield.', 'CO₂ was a limiting factor; more CO₂ increases the rate of photosynthesis, so more glucose is made for growth (and fruit).', 'CO₂ limiting [1]; more photosynthesis → more carbohydrate for growth [1] [2]'),
             lambda r: ('Suggest two other conditions the grower could control to increase the yield further.', 'Light intensity (artificial lamps) and temperature (heaters), to the optimum.', 'two [2]'),
             lambda r: ('Evaluate whether the grower should increase carbon dioxide concentration even further.', 'Not necessarily: above a certain concentration another factor limits the rate, so yield would not increase; the cost of extra CO₂ may exceed extra income; very high CO₂ can harm workers.', 'another factor limiting [1]; cost / economic argument [1]; conclusion [1] [3]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


longs(t, [('Describe and explain how a grower could use a greenhouse to increase crop yield, referring to limiting factors.', 'Artificial lighting increases light intensity / hours; heaters keep the temperature near the optimum for enzymes; burning paraffin or adding CO₂ increases CO₂; each removes a limiting factor so the rate of photosynthesis and growth increases; balance cost against extra yield.',
           'light [1]; temperature [1]; CO₂ [1]; limiting factor idea [1]; cost-benefit [1] [5]')])
t_c6b = t

LEAF = [('waxy cuticle', 'reduces water loss by evaporation and is transparent to let light through'), ('upper epidermis', 'thin and transparent so light passes to the palisade layer'),
        ('palisade mesophyll', 'tightly packed cells with many chloroplasts near the upper surface, absorbing most light'), ('spongy mesophyll', 'cells with air spaces between them for diffusion of gases'),
        ('air spaces', 'allow carbon dioxide to diffuse to mesophyll cells and oxygen to diffuse out'), ('stomata', 'pores, mostly in the lower epidermis, that let carbon dioxide in and oxygen and water vapour out'),
        ('guard cells', 'open and close the stomata'), ('vascular bundle', 'contains xylem, bringing water and mineral ions, and phloem, carrying sucrose away')]
t = T('Leaf structure and its adaptations for photosynthesis', 'leaf structure', 'adaptations for photosynthesis')
facts(t, [(a, b) for a, b in LEAF[:7]])
mcqs(t, [('Where in a leaf are most chloroplasts found?', 'Palisade mesophyll', 'Palisade cells near the upper surface receive the most light.', ['Lower epidermis', 'Xylem', 'Waxy cuticle']),
         ('Why are leaves thin?', 'To give a short distance for gases to diffuse', 'Carbon dioxide reaches mesophyll cells quickly.', ['To reduce photosynthesis', 'To store more starch', 'To stop light entering']),
         ('Which tissue in a leaf carries water to the mesophyll cells?', 'Xylem', 'Xylem carries water and mineral ions; phloem carries sucrose and amino acids.', ['Phloem', 'Epidermis', 'Cuticle'])])
shorts(t, [('State two ways in which the shape of a leaf is adapted for photosynthesis.', 'Large surface area to absorb light; thin for short diffusion distance.', 'large surface area [1]; thin [1] [2]'),
           ('State the function of guard cells.', 'To open and close the stomata, controlling gas exchange and water loss.', '[1]')])
explain(t, [('Explain how the structure of the palisade mesophyll is adapted for photosynthesis.', 'Cells are near the upper surface, tightly packed and column-shaped with many chloroplasts, so they absorb as much light as possible.', 'position near top / packed [1]; many chloroplasts [1] [2]'),
            ('Explain why most stomata are on the lower surface of a leaf.', 'The lower surface is shaded and cooler, so less water is lost by evaporation, while gases can still diffuse in and out.', 'cooler / shaded [1]; less water loss [1] [2]'),
            ('Explain the importance of air spaces in the spongy mesophyll.', 'They allow carbon dioxide to diffuse from stomata to the mesophyll cells and oxygen to diffuse out; they give a large surface area for gas exchange.', 'diffusion of CO₂ / O₂ [1]; large surface for exchange [1] [2]'),
            ('Explain why the upper epidermis has no chloroplasts.', 'It is transparent so that light passes through to the palisade cells below where most photosynthesis happens.', 'transparent [1]; light reaches palisade [1] [2]'),
            ('Explain how the vascular bundles support photosynthesis in the leaf.', 'Xylem brings water (a raw material) and mineral ions; phloem carries away sucrose made from glucose so it does not build up.', 'xylem brings water [1]; phloem removes sugars [1] [2]')])
myths(t, [('Stomata are mainly on the upper surface so they receive more light.', 'Most stomata are on the lower surface, which reduces water loss; they are for gas exchange, not light absorption.'),
           ('The waxy cuticle helps carbon dioxide enter the leaf.', 'The cuticle is waterproof and reduces water loss; CO₂ enters through stomata.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def stomata(r, D):
    dia = r.choice([0.4, 0.5, 0.8, 1.0, 1.2])
    rad = dia / 2
    area = math.pi * rad * rad
    counts = [r.randrange(18, 60) for _ in range(5 if D >= 3 else 1)]
    mean = sum(counts) / len(counts)
    dens = mean / area
    plant = r.choice(['bean', 'privet', 'sunflower', 'hibiscus', 'maize', 'pea'])
    if D <= 2:
        c = counts[0]
        st = f'A nail-varnish peel from the lower surface of a {plant} leaf was viewed with a microscope. The field of view has a diameter of {fx(dia)} mm and contains {c} stomata. Calculate the number of stomata per mm².'
        key = f'area = π × {fx(rad, 3)}² = {fx(area, 3)} mm² [1]; {c} ÷ {fx(area, 3)} = {fx(c / area, 0)} per mm² [1] [2]'
        if D == 1:
            return NQ(r, st.replace('Calculate', 'What is'), c / area, [c / dia, c * area, c / (math.pi * dia), c / (math.pi * dia * dia)], ' per mm²', key.replace(' [1]', '').replace(' [2]', ''), f=lambda v: fx(v, 0))
        return Q(st, f'{fx(c / area, 0)} per mm²', key, 'numerical', 2)
    st = (f'{person(r)} counted stomata in five fields of view on the lower surface of a {plant} leaf. Counts: {", ".join(map(str, counts))}. The field of view has a diameter of {fx(dia)} mm. '
          '(a) Calculate the mean number of stomata per field of view. (b) Calculate the stomatal density in stomata per mm².')
    ans = f'(a) {fx(mean, 1)} (b) {fx(dens, 0)} per mm²'
    key = f'(a) {sum(counts)} ÷ 5 = {fx(mean, 1)} [1] (b) area = π × {fx(rad, 3)}² = {fx(area, 3)} mm² [1]; {fx(mean, 1)} ÷ {fx(area, 3)} = {fx(dens, 0)} [1]'
    m = 3
    if D >= 4:
        st += ' (c) Suggest how the stomatal density of the upper surface would differ, and explain why.'
        ans += ' (c) Lower: fewer stomata on the upper surface, reducing water loss where it is warmer and in direct sunlight.'
        key += ' (c) fewer on upper surface [1]; reduces water loss [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3), 'short')
def leaf_part(r, D):
    a, b = r.choice(LEAF)
    others = r.sample([x for x in LEAF if x[0] != a], 2)
    return Q(f'For each part of a leaf, describe how it is adapted for photosynthesis: (i) {a} (ii) {others[0][0]} (iii) {others[1][0]}.',
             f'(i) {b} (ii) {others[0][1]} (iii) {others[1][1]}', f'(i) {b} [1]; (ii) {others[0][1]} [1]; (iii) {others[1][1]} [1] [3]', 'short', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def leaf_case(r, D):
    habitat = r.choice([('the shaded floor of a rainforest', 'larger, thinner leaves with more chlorophyll to absorb the little light available'), ('a hot, dry desert', 'small leaves with a thick cuticle and fewer, sunken stomata to reduce water loss'),
                        ('the surface of a pond (floating leaves)', 'stomata on the upper surface only, because the lower surface is in water')])
    intro = f'Botanists compare the leaves of a plant growing in {habitat[0]} with those of a plant growing in a garden in {city(r)}.'
    parts = [lambda r: ('Suggest how the leaves of the plant from this habitat may differ, and explain why.', cap(habitat[1]) + '.', 'difference [1]; explanation linked to habitat [1] [2]'),
             lambda r: ('Describe the path taken by a carbon dioxide molecule from the air to a chloroplast in a palisade cell.', 'Through a stoma, into the air spaces of the spongy mesophyll, diffuses through the cell wall and membrane of the palisade cell into the chloroplast.', 'stoma [1]; air spaces [1]; diffuses into cell [1] [3]'),
             lambda r: ('Explain why leaves have a large surface area.', 'To absorb more light and to provide more surface for gas exchange.', '[2]'),
             lambda r: ('Name the tissue that carries sucrose away from the leaf.', 'Phloem.', '[1]'),
             lambda r: ('Explain how guard cells control the opening of stomata.', 'When guard cells take in water by osmosis they become turgid and curve apart, opening the stoma; when they lose water they become flaccid and close it.', 'turgid → open [1]; flaccid → close [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how the internal structure of a leaf is adapted for photosynthesis.', 'Transparent cuticle and epidermis let light in; palisade near top with many chloroplasts; spongy mesophyll with air spaces for diffusion; stomata for gas exchange with guard cells; xylem brings water, phloem removes sugars; thin for short diffusion distance.',
           'any five adaptations linked to function [5]')])
t_c6c = t

t = T('Mineral requirements of plants: nitrate and magnesium ions', 'mineral requirements of plants', 'nitrate and magnesium ions')
facts(t, [('nitrate ions', 'mineral ions needed by plants to make amino acids and proteins'), ('magnesium ions', 'mineral ions needed by plants to make chlorophyll'),
          ('chlorosis', 'yellowing of leaves caused by a lack of chlorophyll, for example from magnesium deficiency'), ('fertiliser', 'a substance added to soil to supply mineral ions such as nitrate, phosphate and potassium'),
          ('mineral deficiency', 'poor growth of a plant caused by a lack of a particular mineral ion')])
mcqs(t, [('Which mineral ion is needed to make chlorophyll?', 'Magnesium', 'Magnesium is part of the chlorophyll molecule; deficiency causes yellow leaves.', ['Nitrate', 'Calcium', 'Iron']),
         ('A plant has yellow older leaves and stunted growth. Which ion is most likely deficient?', 'Nitrate', 'Nitrate deficiency: poor growth (little protein) and yellowing of older leaves.', ['Magnesium only', 'Sodium', 'Chloride']),
         ('How do mineral ions enter a root hair cell from dilute soil water?', 'By active transport', 'Ions are more concentrated inside the root, so energy is needed.', ['By osmosis', 'By transpiration', 'By photosynthesis'])])
shorts(t, [('State why plants need nitrate ions.', 'To make amino acids and therefore proteins (for growth).', 'amino acids / proteins [1]'),
           ('State the symptom of magnesium deficiency in plants.', 'Yellowing of the leaves (chlorosis), often between the veins.', '[1]')])
explain(t, [('Explain why a plant lacking magnesium grows slowly.', 'Magnesium is needed for chlorophyll; with less chlorophyll less light is absorbed, so less photosynthesis and less glucose for growth.', 'less chlorophyll [1]; less photosynthesis / glucose [1] [2]'),
            ('Explain why a plant lacking nitrate has stunted growth.', 'Nitrate is needed to make amino acids and proteins; without proteins the plant cannot make new cells for growth.', 'amino acids / proteins [1]; new cells / growth [1] [2]'),
            ('Explain why farmers add fertilisers to fields where crops are harvested each year.', 'Harvesting removes the plants and the mineral ions they absorbed, so the soil runs short; fertilisers replace the ions to keep yields high.', 'ions removed with crop [1]; replaced [1] [2]')])
myths(t, [('Plants get their energy from the mineral ions in fertiliser.', 'Plants get energy from light; mineral ions are raw materials for making substances such as proteins and chlorophyll.')])


@t.add('C3', (1, 2, 3, 4, 5), 'case')
def min_data(r, D):
    full = round(r.uniform(4.0, 7.0), 1)
    noN = round(full * r.uniform(0.3, 0.5), 1)
    noMg = round(full * r.uniform(0.55, 0.75), 1)
    if D == 1:
        return MQ(r, f'Seedlings were grown in culture solutions for four weeks. Mean dry mass: complete solution {full} g; no nitrate {noN} g; no magnesium {noMg} g. Which conclusion is correct?', 'Lack of nitrate reduced growth the most',
                  ['Magnesium is not needed for growth', 'Lack of magnesium reduced growth the most', 'Nitrate is only needed for chlorophyll', 'The complete solution reduced growth'], 'Lowest dry mass without nitrate.')
    st = (f'{person(r)} grew seedlings in three culture solutions for four weeks. Mean dry mass: complete solution {full} g; lacking nitrate {noN} g; lacking magnesium {noMg} g. '
          '(a) Calculate the percentage decrease in dry mass caused by lack of nitrate. (b) Describe the appearance of the leaves of the seedlings lacking magnesium.')
    pN = (full - noN) / full * 100
    ans = f'(a) {fx(pN, 1)}% (b) yellow leaves (chlorosis)'
    key = f'(a) ({full} − {noN}) ÷ {full} × 100 [1] = {fx(pN, 1)}% [1] (b) yellow / chlorosis [1]'
    m = 3
    if D >= 3:
        st += ' (c) Explain why lack of nitrate reduced growth.'
        ans += ' (c) Nitrate is needed to make amino acids and proteins for new cells.'
        key += ' (c) amino acids / proteins [1]; growth / new cells [1]'
        m = 5
    if D >= 5:
        st += ' (d) Explain why the complete solution acts as a control.'
        ans += ' (d) It shows how the seedlings grow with all ions present, for comparison.'
        key += ' (d) comparison / shows effect is due to missing ion [1]'
        m = 6
    return Q(st, ans, key + f' [{m}]', 'case', m)


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def min_case(r, D):
    crop = r.choice(['maize', 'rice', 'cassava', 'wheat', 'tea'])
    intro = f'A farmer in {city(r)} notices that the {crop} plants in one field are small with pale yellow leaves.'
    parts = [lambda r: ('Suggest two mineral deficiencies that could cause these symptoms.', 'Nitrate deficiency and magnesium deficiency.', '[2]'),
             lambda r: ('Describe how a scientist could find out which ion is lacking.', 'Grow seedlings in culture solutions each lacking one ion, plus a complete solution as a control; compare growth and leaf colour after several weeks.', 'solutions lacking one ion [1]; control [1]; compare growth / colour [1] [3]'),
             lambda r: ('Explain how magnesium deficiency causes the yellow colour.', 'Magnesium is needed to make chlorophyll; without it less chlorophyll is made and leaves look yellow.', '[2]'),
             lambda r: ('Explain how the ions enter the roots of the plant.', 'By active transport into root hair cells, against a concentration gradient, using energy from respiration.', 'active transport [1]; against gradient using energy [1] [2]'),
             lambda r: ('Suggest one disadvantage of adding too much fertiliser.', 'Excess runs off into rivers, causing eutrophication (or it wastes money / damages roots).', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t_c6d = t
CHAPTERS[6] = [t_c6a, t_c6b, t_c6c, t_c6d]

# ===================================================================== 7 Human nutrition
DEF = [('vitamin C', 'scurvy', 'bleeding gums, poor wound healing', 'citrus fruit'), ('vitamin D', 'rickets', 'soft, weak bones that bend', 'oily fish, eggs, sunlight on skin'),
       ('calcium', 'rickets / weak bones and teeth', 'brittle bones and teeth, poor blood clotting', 'milk, cheese'), ('iron', 'anaemia', 'tiredness, lack of energy (too little haemoglobin)', 'red meat, spinach, beans'),
       ('dietary fibre', 'constipation', 'difficulty in passing faeces', 'wholemeal bread, vegetables, fruit'), ('protein', 'kwashiorkor', 'swollen abdomen, poor growth', 'meat, fish, beans')]
NUT = [('carbohydrates', 'a source of energy'), ('fats and oils', 'a source of energy, insulation and stored energy'), ('proteins', 'growth and repair of tissues; making enzymes and antibodies'),
       ('vitamins', 'needed in small amounts for good health, e.g. vitamin C for collagen, vitamin D for calcium absorption'), ('mineral ions', 'e.g. calcium for bones and teeth, iron for haemoglobin'),
       ('dietary fibre', 'adds bulk to food so that peristalsis moves it through the gut'), ('water', 'solvent for reactions and transport; removes waste')]
t = T('Balanced diet, nutrients and deficiency diseases (vitamin C, vitamin D, calcium, iron)', 'balanced diet', 'deficiency diseases')
facts(t, [('balanced diet', 'a diet containing all the nutrients in the correct proportions, and enough energy, for an individual'), ('deficiency disease', 'an illness caused by a lack of a particular nutrient in the diet'),
          ('scurvy', 'a deficiency disease caused by lack of vitamin C, with bleeding gums'), ('rickets', 'a deficiency disease caused by lack of vitamin D or calcium, in which bones are soft and bend'),
          ('anaemia', 'a condition caused by lack of iron, in which too little haemoglobin is made'), ('dietary fibre', 'indigestible material (mainly cellulose) that adds bulk and helps peristalsis')])
mcqs(t, [('A sailor has bleeding gums after months without fresh fruit. Which nutrient is lacking?', 'Vitamin C', 'Scurvy is caused by lack of vitamin C.', ['Vitamin D', 'Iron', 'Calcium']),
         ('Why does a pregnant woman need more iron in her diet?', 'To make extra haemoglobin for her own and the fetus\'s red blood cells', 'Iron is part of haemoglobin.', ['To make bones stronger', 'To digest more starch', 'To store more fat']),
         ('Which nutrient helps prevent constipation?', 'Dietary fibre', 'Fibre adds bulk, helping peristalsis.', ['Vitamin D', 'Protein', 'Fat'])])
shorts(t, [('List the seven components of a balanced diet.', 'Carbohydrates, fats and oils, proteins, vitamins, mineral ions, dietary fibre, water.', 'all seven [2]; five or six [1] [2]'),
           ('State two factors that affect the energy needs of a person.', 'Age, sex, activity level, pregnancy / breastfeeding.', 'any two [2]')])
explain(t, [('Explain why a teenager needs more protein per kilogram of body mass than an adult.', 'Teenagers are growing, and protein is needed to make new cells and tissues (and enzymes).', 'growth [1]; protein for new cells / tissues [1] [2]'),
            ('Explain why people who spend little time in sunlight may develop weak bones.', 'Skin makes vitamin D in sunlight; vitamin D is needed to absorb calcium; without it bones become soft (rickets).', 'vitamin D made in sunlight [1]; needed for calcium absorption [1]; weak bones [1] [3]'),
            ('Explain why a person with anaemia feels tired.', 'Lack of iron means less haemoglobin, so the blood carries less oxygen; less aerobic respiration releases less energy.', 'less haemoglobin [1]; less oxygen / respiration / energy [1] [2]'),
            ('Explain why an athlete in training needs more carbohydrate than an office worker.', 'More muscle activity needs more energy from respiration; carbohydrates provide glucose for respiration.', 'more energy needed [1]; carbohydrate provides glucose for respiration [1] [2]')])
myths(t, [('A balanced diet means eating equal amounts of every food group.', 'A balanced diet contains all nutrients in the correct proportions for that person, not equal amounts.'),
           ('Dietary fibre is digested to give energy.', 'Dietary fibre is not digested by humans; it adds bulk and helps peristalsis.'),
           ('Rickets is caused by lack of vitamin C.', 'Rickets is caused by lack of vitamin D or calcium; scurvy is caused by lack of vitamin C.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def def_id(r, D):
    n, dis, sym, src = r.choice(DEF)
    if D <= 2:
        mode = r.randrange(2)
        if mode == 0:
            return MQ(r, f'A person shows these symptoms: {sym}. Which nutrient is most likely lacking from their diet?', n, [x[0] for x in DEF if x[0] != n and x[1] != dis], f'{cap(dis)}: lack of {n}.')
        return MQ(r, f'Which deficiency disease is caused by a lack of {n}?', dis, [x[1] for x in DEF if x[0] != n and x[1] != dis] + ['diabetes'], f'Lack of {n} → {dis}.')
    return Q(f'A child in {city(r)} has {sym}. (a) Suggest the deficiency disease and the nutrient that is lacking. (b) Suggest two foods that would help prevent it.',
             f'(a) {dis}; {n} (b) e.g. {src}', f'(a) {dis} [1]; {n} [1] (b) two suitable foods, e.g. {src} [2] [4]', 'short', 4)


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def food_energy(r, D):
    food = r.choice(['peanut', 'cashew nut', 'crisp', 'piece of bread', 'cornflake', 'pasta piece'])
    m = round(r.uniform(0.4, 1.2), 2)
    vw = r.choice([10, 20, 25])
    dT = round(r.uniform(12, 38), 1)
    E = vw * 4.2 * dT
    Eg = E / m
    if D == 1:
        return NQ(r, f'Burning a {food} raised the temperature of {vw} cm³ of water by {fx(dT)} °C. How much energy was transferred to the water? (4.2 J raise 1 g of water by 1 °C; 1 cm³ water = 1 g)', E, [vw * dT, 4.2 * dT, E / 1000, vw * 4.2], ' J',
                  f'E = mass × 4.2 × ΔT = {vw} × 4.2 × {fx(dT)} = {fx(E, 1)} J.', f=lambda v: fx(v, 1))
    st = (f'{person(r)} burned a {fx(m, 2)} g {food} under a boiling tube containing {vw} cm³ of water. The temperature rose from 21.0 °C to {fx(21 + dT, 1)} °C. '
          'Calculate the energy in the food per gram, in J/g. (4.2 J raise the temperature of 1 g of water by 1 °C.)')
    key = f'ΔT = {fx(dT)} °C [1]; energy = {vw} × 4.2 × {fx(dT)} = {fx(E, 1)} J [1]; ÷ {fx(m, 2)} = {fx(Eg, 0)} J/g [1]'
    mk_ = 3
    ans = f'{fx(Eg, 0)} J/g'
    if D >= 4:
        st += ' The value on the food label is much higher. Suggest two reasons for the difference.'
        ans += '; heat lost to the air / tube and the food not burned completely.'
        key += '; heat lost to surroundings / heating the tube [1]; incomplete combustion [1]'
        mk_ = 5
    return Q(st, ans, key + f' [{mk_}]', 'numerical', mk_)


@t.add('C3', (2, 3, 4), 'numerical')
def label(r, D):
    per100 = r.choice([1450, 1600, 1720, 1890, 2100, 380, 620])
    serve = r.choice([30, 40, 45, 60, 125, 150])
    need = r.choice([9000, 10000, 11500, 12000])
    E = per100 * serve / 100
    st = f'A food label states {per100} kJ per 100 g. A serving is {serve} g. (a) Calculate the energy in one serving. (b) Calculate the percentage of a daily requirement of {need:,} kJ that this provides.'
    return Q(st, f'(a) {fx(E, 1)} kJ (b) {fx(E / need * 100, 1)}%', f'(a) {per100} × {serve} ÷ 100 = {fx(E, 1)} kJ [2] (b) {fx(E, 1)} ÷ {need:,} × 100 = {fx(E / need * 100, 1)}% [1] [3]', 'numerical', 3)


FOOD_E = {'setup': lambda r, p: f'{p} burned samples of different nuts, each of mass 1.0 g, under a boiling tube containing 20 cm³ of water and recorded the temperature rise.',
          'iv': ('type of nut', ''), 'xs': lambda r: r.sample(['peanut', 'almond', 'cashew', 'walnut', 'hazelnut', 'macadamia'], 4),
          'dv': ('temperature rise', '°C'), 'y': lambda x, k: k * {'peanut': 24, 'almond': 22, 'cashew': 21, 'walnut': 27, 'hazelnut': 25, 'macadamia': 30}[x], 'dp': 1, 'graph': False,
          'controls': ['mass of the nut', 'volume of water', 'distance of the burning nut from the tube', 'starting temperature of the water'],
          'trend': lambda d: f'The {d["xs"][max(range(len(d["means"])), key=lambda i: d["means"][i])]} gave the greatest temperature rise, so it releases the most energy per gram.',
          'why': ('A larger temperature rise means more energy was transferred to the water, so that nut contains more energy per gram (more fat).', 'more temperature rise = more energy [1]; linked to fat content [1] [2]'),
          'improve': ['insulate the boiling tube / use a calorimeter to reduce heat loss', 'relight the nut until it burns completely', 'stir the water before reading the thermometer']}
FOOD_E['extra'] = [lambda r, d: (f'Calculate the energy released by the {d["xs"][0]}, using energy = 20 × 4.2 × temperature rise.', f'{fx(20 * 4.2 * d["means"][0], 0)} J', f'20 × 4.2 × {fx(d["means"][0], 2)} [1] = {fx(20 * 4.2 * d["means"][0], 0)} J [1] [2]'),
                   lambda r, d: ('State the type of graph you would draw to display these results, and explain why.', 'A bar chart, because the independent variable (type of nut) is categoric.', 'bar chart [1]; categoric variable [1] [2]')]
FOOD_E['xfmt'] = lambda v: f'the {v}'
FOOD_E['prep'] = 'for'
add_practical(t, FOOD_E, C3D=(2, 3, 4), C4D=(3, 4, 5))


@t.add('C4', (3, 4, 5), 'multi_step')
def diet_case(r, D):
    who = r.choice([('a pregnant woman', 'iron, calcium and protein for the fetus'), ('an elderly man who rarely goes outside', 'vitamin D and calcium'), ('a vegan athlete', 'protein, iron and energy'),
                    ('a ten-year-old child', 'protein and calcium for growth')])
    intro = f'A dietitian in {city(r)} is planning meals for {who[0]}.'
    parts = [lambda r: ('Suggest which nutrients are especially important for this person, and why.', cap(who[1]) + '.', 'two nutrients [1]; linked reason [1] [2]'),
             lambda r: ('Explain the importance of dietary fibre in the diet.', 'Fibre adds bulk to the food so that the muscles of the gut can push it along by peristalsis; prevents constipation.', 'bulk [1]; peristalsis / prevents constipation [1] [2]'),
             lambda r: ('Describe the possible effects of a diet that provides more energy than the person uses.', 'Excess is stored as fat, leading to obesity, with greater risk of coronary heart disease and type 2 diabetes.', 'stored as fat / obesity [1]; health risk [1] [2]'),
             lambda r: ('Explain why vitamin D and calcium are often needed together.', 'Vitamin D is needed to absorb calcium from the gut; calcium is used to build bones and teeth.', '[2]'),
             lambda r: ('Suggest how the dietitian could check that the meals provide enough energy.', 'Add up the energy (kJ) from food labels / tables for each food and compare with the daily requirement for the person.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain what is meant by a balanced diet and how dietary needs change with age, activity and pregnancy.', 'All seven nutrient groups in the right proportions with energy matching needs. Growing children need more protein and calcium per kg; active people need more energy; pregnant women need more iron, calcium, folic acid and protein; elderly need less energy.',
           'definition [1]; age [1]; activity [1]; pregnancy [1]; further detail / example [1] [5]')])
t_c7a = t

GUT = [('mouth', 'mechanical digestion by teeth; chemical digestion of starch by amylase in saliva'), ('salivary glands', 'produce saliva containing amylase'), ('oesophagus', 'carries food from the mouth to the stomach by peristalsis'),
       ('stomach', 'mechanical digestion by muscular churning; protease (pepsin) digests protein; hydrochloric acid kills pathogens'), ('pancreas', 'produces amylase, protease and lipase, released into the duodenum'),
       ('liver', 'produces bile; stores glycogen; breaks down excess amino acids'), ('gall bladder', 'stores bile'), ('duodenum', 'first part of the small intestine where pancreatic juice and bile are added'),
       ('ileum', 'last part of the small intestine where most digested food is absorbed'), ('colon', 'absorbs water from undigested food'), ('rectum', 'stores faeces'), ('anus', 'faeces are egested through it')]
TEETH = [('incisors', 'chisel-shaped, for biting and cutting'), ('canines', 'pointed, for gripping and tearing'), ('premolars', 'broad with ridges (cusps), for crushing and grinding'), ('molars', 'large with cusps, for crushing and grinding')]
t = T('Organs of the digestive system and their functions; mechanical digestion and teeth', 'organs of the digestive system', 'mechanical digestion and teeth')
facts(t, [('ingestion', 'the taking of substances, such as food and drink, into the body through the mouth'), ('mechanical digestion', 'the breakdown of food into smaller pieces without chemical change to the food molecules'),
          ('peristalsis', 'waves of muscle contraction that move food along the alimentary canal'), ('egestion', 'the passing out of food that has not been digested or absorbed, as faeces, through the anus'),
          ('assimilation', 'the movement of digested food molecules into the cells of the body where they are used'), ('absorption', 'the movement of nutrients from the intestines into the blood')])
mcqs(t, [('Which part of the alimentary canal absorbs most water?', 'Small intestine', 'Most water is absorbed in the small intestine; the colon absorbs some more.', ['Stomach', 'Oesophagus', 'Rectum']),
         ('Which teeth are used for crushing and grinding food?', 'Molars', 'Molars and premolars have cusps for grinding.', ['Incisors', 'Canines', 'All teeth equally']),
         ('Why is mechanical digestion important?', 'It increases the surface area of food for enzymes to act on', 'Smaller pieces have a larger surface area for chemical digestion.', ['It breaks proteins into amino acids', 'It absorbs nutrients', 'It produces bile'])])
shorts(t, [('Name, in order, the parts of the alimentary canal that food passes through from the mouth to the anus.', 'Mouth, oesophagus, stomach, duodenum, ileum, colon, rectum, anus.', 'correct order [2]; one error [1] [2]'),
           ('Name the four types of human teeth.', 'Incisors, canines, premolars, molars.', '[1]')])
explain(t, [('Explain how tooth decay develops.', 'Bacteria in plaque feed on sugars and produce acid, which dissolves the enamel and then dentine, forming a cavity.', 'bacteria + sugar [1]; acid [1]; enamel dissolved [1] [3]'),
            ('Explain how regular brushing and limiting sugary foods reduce tooth decay.', 'Brushing removes plaque bacteria; less sugar means bacteria make less acid that dissolves enamel; fluoride toothpaste strengthens enamel.', 'removes plaque / bacteria [1]; less acid [1] [2]'),
            ('Explain how peristalsis moves food along the oesophagus.', 'Circular and longitudinal muscles contract and relax in waves; contraction of circular muscle behind the food squeezes it forward.', 'muscles contract in waves [1]; circular behind bolus pushes it [1] [2]'),
            ('Explain why the stomach wall is very muscular.', 'Muscular contractions churn the food, mixing it with gastric juice and breaking it into smaller pieces (mechanical digestion).', 'churning / mixing [1]; mechanical digestion [1] [2]')])
myths(t, [('Food passes through the liver and pancreas as it is digested.', 'Food passes only through the alimentary canal; the liver and pancreas release bile and enzymes into the duodenum.'),
           ('Mechanical digestion breaks large molecules into small molecules.', 'Mechanical digestion breaks food into smaller pieces; chemical digestion breaks large molecules into small ones.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def gut_id(r, D):
    o, f = r.choice(GUT)
    if D <= 2:
        return MQ(r, f'Which organ has this function: {f}?', o, [x[0] for x in GUT if x[0] != o], f'{cap(o)}: {f}.')
    xs = r.sample(GUT, 3)
    labs = ['(i)', '(ii)', '(iii)']
    return Q('State the function of each organ in digestion: ' + ', '.join(f'{labs[i]} {x[0]}' for i, x in enumerate(xs)) + '.', ' '.join(f'{labs[i]} {x[1]}' for i, x in enumerate(xs)),
             '; '.join(f'{labs[i]} {x[1]} [1]' for i, x in enumerate(xs)) + ' [3]', 'short', 3)


@t.add('C3', (1, 2, 3), 'short')
def teeth_q(r, D):
    a, b = r.choice(TEETH)
    if D <= 2:
        return MQ(r, f'Which type of tooth is {b}?', a, [x[0] for x in TEETH if x[0] != a] + ['wisdom teeth'], f'{cap(a)}: {b}.')
    diet = r.choice([('a lion', 'large canines for gripping and killing prey and tearing meat'), ('a sheep', 'large flat molars and premolars for grinding grass; no upper incisors'), ('a human', 'all four types for a mixed diet')])
    return Q(f'Describe the shape and function of {a}, and suggest how the teeth of {diet[0]} are adapted to its diet.', f'{cap(a)}: {b}. {cap(diet[0])}: {diet[1]}.', f'{a} shape [1]; function [1]; adaptation to diet [1] [3]', 'short', 3)


@t.add('C4', (3, 4, 5), 'multi_step')
def gut_case(r, D):
    meal = r.choice(['a cheese sandwich', 'a bowl of rice and beans', 'a boiled egg with toast', 'a plate of pasta with chicken'])
    intro = f'{person(r)} eats {meal}. The food passes through the alimentary canal over the next 24 hours.'
    parts = [lambda r: ('Describe the role of the teeth and the stomach in mechanical digestion.', 'Teeth cut and grind food into smaller pieces; the muscular stomach wall churns the food; both increase the surface area for enzymes.', 'teeth [1]; stomach churning [1]; surface area [1] [3]'),
             lambda r: ('Name the organ where most nutrients are absorbed.', 'Small intestine (ileum).', '[1]'),
             lambda r: ('Explain the function of the colon.', 'It absorbs water from the remaining undigested food, forming faeces.', '[2]'),
             lambda r: ('Distinguish between egestion and excretion.', 'Egestion removes undigested food as faeces; excretion removes metabolic waste such as urea and CO₂.', '[2]'),
             lambda r: ('Describe the role of the liver and pancreas in digestion, even though food does not pass through them.', 'The liver makes bile, stored in the gall bladder and released into the duodenum; the pancreas secretes amylase, protease and lipase into the duodenum.', 'liver bile [1]; pancreas enzymes [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the processes of ingestion, digestion, absorption, assimilation and egestion, naming where each happens.', 'Ingestion: taking food into mouth. Digestion: mechanical (teeth, stomach) and chemical (mouth, stomach, small intestine). Absorption: into blood in small intestine (water also in colon). Assimilation: nutrients used by body cells (e.g. liver). Egestion: faeces out through anus.',
           'one mark per process with location [5]')])
t_c7b = t

t = T('Chemical digestion: amylase, protease and lipase; role of hydrochloric acid and bile', 'chemical digestion', 'amylase, protease and lipase', 'hydrochloric acid and bile')
facts(t, [('chemical digestion', 'the breakdown of large insoluble molecules into small soluble molecules'), ('bile', 'an alkaline liquid made by the liver that neutralises stomach acid and emulsifies fats'),
          ('emulsification', 'breaking large fat droplets into smaller droplets, increasing the surface area for lipase'), ('pepsin', 'a protease made in the stomach that works best in acid'),
          ('trypsin', 'a protease secreted by the pancreas that acts in the small intestine'), ('maltase', 'an enzyme on the membranes of the small intestine epithelium that breaks maltose into glucose')])
mcqs(t, [('What is the function of hydrochloric acid in the stomach?', 'To kill pathogens in food and give the optimum pH for pepsin', 'The low pH (about 2) kills bacteria and suits pepsin.', ['To digest fats', 'To neutralise bile', 'To absorb glucose']),
         ('Bile emulsifies fats. What does this mean?', 'It breaks large fat droplets into smaller droplets', 'Emulsification is physical, increasing surface area for lipase.', ['It digests fats into fatty acids', 'It absorbs fats into lacteals', 'It turns fats into glucose']),
         ('Where is lipase produced?', 'Pancreas', 'Pancreatic lipase digests fats in the small intestine.', ['Salivary glands', 'Liver', 'Stomach'])])
shorts(t, [('Name the products of digestion of starch, protein and fat.', 'Starch → maltose (then glucose); protein → amino acids; fat → fatty acids and glycerol.', 'all three [2]; two [1] [2]'),
           ('State two functions of bile.', 'Neutralises acid from the stomach; emulsifies fats.', '[2]')])
explain(t, [('Explain why bile is needed for efficient fat digestion.', 'Bile emulsifies fats into tiny droplets, increasing the surface area for lipase; it also neutralises acid, giving a suitable pH for lipase.', 'emulsifies / surface area [1]; neutralises acid / pH for lipase [1] [2]'),
            ('Explain why the contents of the duodenum need to be neutralised.', 'Food arrives from the stomach at pH about 2; pancreatic enzymes work best at slightly alkaline pH, so bile and pancreatic juice raise the pH.', 'stomach contents acidic [1]; enzymes in duodenum need alkaline / neutral pH [1] [2]'),
            ('Explain why large molecules must be digested before absorption.', 'They are too large and insoluble to pass through the wall of the small intestine into the blood; small soluble molecules can be absorbed.', 'large / insoluble [1]; small molecules absorbed [1] [2]'),
            ('Describe how starch is digested completely to glucose in humans.', 'Amylase from salivary glands and the pancreas breaks starch into maltose; maltase on the membranes of the small intestine epithelium breaks maltose into glucose.', 'amylase → maltose [1]; sources [1]; maltase → glucose [1] [3]'),
            ('A person has their gall bladder removed. Suggest why they are advised to eat a low-fat diet.', 'Bile is no longer stored and released in large amounts after a meal, so fats are less emulsified and digested more slowly.', 'less bile released [1]; poorer fat emulsification / digestion [1] [2]')])
myths(t, [('Bile is an enzyme that digests fat.', 'Bile contains no enzymes; it emulsifies fat so that lipase can digest it.'),
           ('Hydrochloric acid digests protein in the stomach.', 'Pepsin (a protease) digests protein; the acid provides the optimum pH and kills pathogens.')])


@t.add('C3', (2, 3, 4, 5), 'numerical')
def emulsify(r, D):
    R = r.choice([1.0, 2.0, 3.0])
    n = r.choice([8, 27, 64, 125, 1000])
    rr = R / round(n ** (1 / 3))
    sa1 = 4 * math.pi * R * R
    sa2 = n * 4 * math.pi * rr * rr
    st = f'A fat droplet of radius {fx(R)} mm is emulsified by bile into {n} smaller droplets, each of radius {fx(rr, 3)} mm. (surface area of a sphere = 4πr²) Calculate the total surface area before and after emulsification, and the factor by which it increases.'
    ans = f'before {fx(sa1, 1)} mm²; after {fx(sa2, 1)} mm²; increase × {fx(sa2 / sa1, 2)}'
    key = f'4π × {fx(R)}² = {fx(sa1, 1)} mm² [1]; {n} × 4π × {fx(rr, 3)}² = {fx(sa2, 1)} mm² [1]; × {fx(sa2 / sa1, 2)} [1]'
    m = 3
    if D >= 4:
        st += ' Explain why this increases the rate of fat digestion.'
        ans += '; larger surface area for lipase to act on, so more enzyme–substrate collisions.'
        key += '; more surface for lipase / more collisions [1]'
        m = 4
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


VISK = {'setup': lambda r, p: f'{p} placed a mixture of starch and amylase in Visking tubing, stood it in a boiling tube of water at 37 °C, and tested the water outside the tubing for reducing sugar at intervals using Benedict\'s solution. The colour score (0 = blue, 5 = brick-red) is shown.',
        'iv': ('time', 'min'), 'xs': lambda r: [0, 10, 20, 30, 40], 'dv': ("Benedict's colour score", ''), 'y': lambda x, k: min(5, x * 0.13 * k), 'dp': 0, 'reps': 1, 'noise': 0.02, 'neg': True,
        'controls': ['temperature', 'volume and concentration of starch', 'volume and concentration of amylase', 'length of Visking tubing'],
        'trend': lambda d: 'The colour score increases with time: more reducing sugar appears in the water outside the tubing.',
        'why': ('Amylase digests starch into maltose; maltose molecules are small enough to diffuse through the partially permeable Visking tubing, but starch and amylase molecules are too large.', 'starch digested to maltose [1]; maltose small enough to pass through [1]; starch too large [1] [3]'),
        'control': 'Set up a tube with boiled amylase (or water) and starch; no sugar should appear outside, showing amylase is needed to digest starch.',
        'improve': ['use a colorimeter to measure the colour change rather than judging by eye', 'test the water with iodine to show that starch does not pass through'], 'graph': False}
add_practical(t, VISK, C3D=(2, 3, 4), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3), 'short')
def dig_enz(r, D):
    rows = [('amylase', 'starch', 'maltose', 'salivary glands and pancreas', 'mouth and duodenum'), ('protease (pepsin)', 'protein', 'amino acids (polypeptides)', 'stomach', 'stomach'),
            ('protease (trypsin)', 'protein', 'amino acids', 'pancreas', 'duodenum'), ('lipase', 'fats', 'fatty acids and glycerol', 'pancreas', 'duodenum'), ('maltase', 'maltose', 'glucose', 'epithelium of small intestine', 'small intestine')]
    e, s_, p, src, where = r.choice(rows)
    if D <= 2:
        k = r.randrange(2)
        if k == 0:
            return MQ(r, f'Which enzyme digests {s_} into {p}?', e, [x[0] for x in rows if x[1] != s_] + ['catalase'], f'{cap(e)}: {s_} → {p}; made in {src}.')
        return MQ(r, f'Where is {e} produced?', src, [x[3] for x in rows if x[3] != src] + ['liver', 'gall bladder'], f'{cap(e)} is produced in the {src}.')
    return Q(f'For the enzyme {e}, state (a) its substrate, (b) its products, (c) where it is produced and (d) where it acts.', f'(a) {s_} (b) {p} (c) {src} (d) {where}', f'(a) {s_} (b) {p} (c) {src} (d) {where}; 1 mark each [4]', 'short', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def bile_case(r, D):
    ph0 = r.choice([7.8, 8.0, 8.2])
    intro = f'{person(r)} set up three tubes each containing milk (which contains fat), lipase and sodium carbonate solution (pH {ph0}), with phenolphthalein indicator (pink in alkali, colourless at pH below 8.3). Tube A: lipase + bile salts; tube B: lipase only; tube C: boiled lipase. Times for the pink colour to disappear were A: 4 min, B: 11 min, C: no change after 30 min.'
    parts = [lambda r: ('Explain why the pink colour disappears.', 'Lipase digests fat into fatty acids and glycerol; the fatty acids lower the pH so the indicator becomes colourless.', 'fatty acids produced [1]; pH falls [1] [2]'),
             lambda r: ('Explain why tube A changed colour faster than tube B.', 'Bile salts emulsify the fat into smaller droplets, increasing the surface area for lipase.', 'emulsification [1]; surface area for lipase [1] [2]'),
             lambda r: ('Explain the result in tube C.', 'Boiling denatured the lipase, changing its active site, so no fat was digested.', '[2]'),
             lambda r: ('Calculate how many times faster the reaction was in tube A than in tube B.', f'{fx(11 / 4, 2)} times', '11 ÷ 4 [1] = 2.75 [1] [2]'),
             lambda r: ('State two variables that should be kept constant.', 'Temperature; volume of milk / lipase / indicator; concentration of lipase.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the digestion of protein and fat in the human alimentary canal.', 'Protein: pepsin in stomach (acid, pH 2, HCl) breaks protein into shorter chains; trypsin from pancreas in duodenum → amino acids. Fat: bile from liver emulsifies and neutralises; lipase from pancreas → fatty acids and glycerol in small intestine.',
           'pepsin / stomach / acid [2]; trypsin / pancreas / amino acids [1]; bile emulsification [1]; lipase products [1] [5]')])
t_c7c = t

t = T('Absorption in the small intestine and structure of villi', 'absorption in the small intestine', 'structure of villi')
facts(t, [('villus', 'a finger-like projection of the lining of the small intestine that increases the surface area for absorption'), ('microvilli', 'tiny projections on the surface membrane of epithelial cells of villi, further increasing surface area'),
          ('lacteal', 'a lymph vessel in the centre of a villus that absorbs fatty acids and glycerol'), ('capillary network', 'blood vessels in a villus that absorb glucose and amino acids'),
          ('hepatic portal vein', 'the blood vessel that carries absorbed nutrients from the small intestine to the liver')])
mcqs(t, [('Which structure in a villus absorbs fatty acids and glycerol?', 'Lacteal', 'Fat products enter the lacteal (lymph); glucose and amino acids enter the blood capillaries.', ['Capillary', 'Goblet cell', 'Artery']),
         ('Which feature of villi increases the rate of absorption?', 'A wall only one cell thick', 'Short diffusion distance; also large surface area and good blood supply.', ['A thick layer of muscle', 'Few capillaries', 'A waxy covering']),
         ('Where does most absorption of digested food take place?', 'Ileum', 'The ileum (small intestine) is long with villi and microvilli.', ['Stomach', 'Colon', 'Oesophagus'])])
shorts(t, [('State three ways in which villi are adapted for absorption.', 'Large surface area (with microvilli); wall one cell thick; good capillary network (and lacteal).', 'any three [3]'),
           ('Name two substances absorbed into the blood capillaries of villi.', 'Glucose and amino acids (also vitamins, mineral ions, water).', '[2]')])
explain(t, [('Explain why a good blood supply to the villi increases the rate of absorption.', 'Blood carries absorbed nutrients away quickly, maintaining a steep concentration gradient for diffusion.', 'carries nutrients away [1]; maintains gradient [1] [2]'),
            ('Explain why the epithelial cells of villi contain many mitochondria.', 'They absorb some substances, such as glucose, by active transport, which needs energy from respiration.', 'active transport [1]; energy from respiration [1] [2]'),
            ('Coeliac disease damages villi, making them flatter. Explain why people with untreated coeliac disease may lose weight.', 'Flattened villi have a smaller surface area, so fewer digested nutrients are absorbed into the blood.', 'smaller surface area [1]; less absorption [1] [2]'),
            ('Explain why the small intestine is very long.', 'A long intestine gives a large surface area and more time for digestion and absorption to be completed.', 'surface area [1]; time [1] [2]')])
myths(t, [('Digested food is absorbed in the stomach.', 'Most digested food is absorbed in the small intestine through the villi.'), ('Villi absorb food by osmosis.', 'Villi absorb nutrients by diffusion and active transport; water is absorbed by osmosis.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def villi_sa(r, D):
    flat = r.choice([0.3, 0.4, 0.5])
    f_v = r.choice([8, 10, 12])
    f_m = r.choice([15, 20, 25])
    tot = flat * f_v * f_m
    if D == 1:
        return NQ(r, f'Villi increase the surface area of the small intestine {f_v} times and microvilli increase it a further {f_m} times. By what factor do they increase it altogether?', f_v * f_m, [f_v + f_m, f_m, f_v * f_m / 10, f_v * f_m * 2], '×', f'{f_v} × {f_m} = {f_v * f_m}.', f=lambda v: fx(v, 1))
    st = f'The inner surface of a person\'s small intestine would be {flat} m² if it were a smooth tube. Folds and villi increase this {f_v} times and microvilli increase it a further {f_m} times. Calculate the total absorptive surface area.'
    key = f'{flat} × {f_v} = {fx(flat * f_v, 2)} m² [1]; × {f_m} = {fx(tot, 1)} m² [1]'
    m = 2
    if D >= 4:
        st += ' Explain why such a large surface area is important.'
        key += '; more nutrient molecules absorbed per second / faster diffusion and active transport [1]'
        m = 3
    return Q(st, f'{fx(tot, 1)} m²' + ('; it allows nutrients to be absorbed quickly before food leaves the intestine.' if D >= 4 else ''), key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4), 'case')
def abs_data(r, D):
    g_in = r.choice([5.0, 6.0, 7.5, 8.0])
    g_out = round(g_in * r.uniform(1.3, 2.2), 1)
    st = f'The glucose concentration in blood entering the small intestine is {g_in} mmol/dm³ and in blood leaving it in the hepatic portal vein after a meal is {g_out} mmol/dm³. (a) Calculate the percentage increase. (b) Name the blood vessel carrying blood from the small intestine to the liver.'
    ans = f'(a) {fx(pct(g_in, g_out), 1)}% (b) hepatic portal vein'
    key = f'(a) ({g_out} − {g_in}) ÷ {g_in} × 100 = {fx(pct(g_in, g_out), 1)}% [2] (b) hepatic portal vein [1]'
    m = 3
    if D >= 3:
        st += ' (c) Explain how glucose enters the blood in the villi.'
        ans += ' (c) By diffusion down a concentration gradient and by active transport into epithelial cells, then into the capillaries.'
        key += ' (c) diffusion [1]; active transport [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'case', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def villi_case(r, D):
    intro = f'A doctor in {city(r)} examines a sample of the lining of the small intestine under a microscope. It has many villi, each covered by a single layer of epithelial cells with microvilli.'
    parts = [lambda r: ('Describe three features of villi that increase the rate of absorption.', 'Large surface area (villi and microvilli); thin wall one cell thick; dense capillary network maintaining the concentration gradient.', 'three features [3]'),
             lambda r: ('Explain the role of the lacteal.', 'It absorbs fatty acids and glycerol, which pass into the lymph system and later into the blood.', '[2]'),
             lambda r: ('Explain why the epithelial cells contain many mitochondria.', 'To release energy by aerobic respiration for active transport of nutrients such as glucose.', '[2]'),
             lambda r: ('Name the organ that receives absorbed glucose and amino acids first, and state one thing it does with them.', 'The liver: stores glucose as glycogen / deaminates excess amino acids.', 'liver [1]; function [1] [2]'),
             lambda r: ('Explain why water absorption in the small intestine is described as osmosis.', 'As nutrients are absorbed, the cells and blood have a lower water potential than the gut contents, so water moves into them through partially permeable membranes.', 'water potential gradient [1]; partially permeable membrane [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe how the structure of the small intestine is adapted for the absorption of digested food.', 'Very long; folded inner wall; villi and microvilli give huge surface area; epithelium one cell thick; capillary network and lacteals; good blood supply maintains gradient; mitochondria for active transport.',
           'any five adaptations linked to absorption [5]')])
t_c7d = t
CHAPTERS[7] = [t_c7a, t_c7b, t_c7c, t_c7d]


# ===================================================================== 8 Transport in plants
t = T('Xylem and phloem: structure and position in roots, stems and leaves', 'xylem and phloem', 'structure and position in roots, stems and leaves')
facts(t, [('xylem', 'tissue of dead, hollow, lignified vessels that transports water and mineral ions from roots to leaves and supports the plant'),
          ('phloem', 'tissue of living cells that transports sucrose and amino acids around the plant'), ('lignin', 'a strong waterproof substance in the walls of xylem vessels'),
          ('vascular bundle', 'a group of xylem and phloem tissue running through stems and leaves'), ('sieve tube', 'a phloem cell with perforated end walls through which sugars flow')])
mcqs(t, [('In a root, where is the xylem found?', 'In the centre, often in a star shape', 'Roots have central xylem (resisting pulling forces) with phloem between the arms.', ['In a ring near the outside', 'Only in the root hairs', 'In the epidermis']),
         ('Which feature of xylem vessels allows water to flow easily?', 'They are hollow with no end walls or cytoplasm', 'Dead hollow cells form continuous tubes.', ['They contain many chloroplasts', 'They have living cytoplasm', 'They have sieve plates']),
         ('In a stem vascular bundle, where is the phloem in relation to the xylem?', 'Towards the outside', 'In dicot stems, bundles are arranged in a ring with phloem outside and xylem inside.', ['Towards the centre', 'Mixed randomly', 'Phloem is absent in stems'])])
shorts(t, [('State two functions of xylem.', 'Transports water and mineral ions; supports the plant (lignin).', '[2]'), ('Name two substances transported in phloem.', 'Sucrose and amino acids.', '[2]')])
explain(t, [('Explain how the structure of xylem vessels is related to their functions.', 'Hollow dead cells with no end walls form continuous tubes for water flow; lignified walls are strong (support) and waterproof; narrow tubes help water rise.', 'hollow / no end walls [1]; lignin strength [1]; continuous column [1] [3]'),
            ('A celery stalk is placed in water containing a red dye for several hours. Describe and explain where the dye appears when the stalk is cut across.', 'Red dots appear in a ring of vascular bundles near the outside, in the xylem, because the dye is carried up with water in the xylem.', 'ring of bundles [1]; xylem carries water/dye [1] [2]'),
            ('Explain why the xylem is in the centre of a root but in a ring near the outside of a stem.', 'In the root the central xylem resists pulling forces and is close to the water entering from all sides; in the stem a ring gives resistance to bending by wind.', 'root: central for pulling / anchorage [1]; stem: ring for bending [1] [2]'),
            ('Explain why phloem must be made of living cells but xylem need not be.', 'Phloem transport (translocation) needs energy and active loading at sources and sinks, so living cytoplasm is needed; water movement in xylem is passive (transpiration pull).', 'phloem needs energy / active [1]; xylem passive [1] [2]')])
myths(t, [('Xylem carries sugar down from the leaves.', 'Phloem carries sugar; xylem carries water and mineral ions up from the roots.'), ('Xylem vessels are living cells full of cytoplasm.', 'Xylem vessels are dead, hollow and lignified.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def xp_where(r, D):
    organ = r.choice(['root', 'stem', 'leaf'])
    pos = {'root': ('xylem in the centre (star-shaped), phloem between the arms of the xylem', 'resists pulling forces; anchorage'),
           'stem': ('vascular bundles in a ring near the outside: phloem towards the outside, xylem towards the inside', 'resists bending'),
           'leaf': ('in the veins (vascular bundles) of the midrib and leaf blade: xylem towards the upper surface, phloem towards the lower surface', 'supplies water close to mesophyll and removes sucrose')}[organ]
    if D <= 2:
        return MQ(r, f'Which describes the position of xylem and phloem in a {organ}?', pos[0], [x for x in ['xylem in the centre (star-shaped), phloem between the arms of the xylem', 'vascular bundles in a ring near the outside: phloem towards the outside, xylem towards the inside',
                               'in the veins (vascular bundles) of the midrib and leaf blade: xylem towards the upper surface, phloem towards the lower surface', 'phloem in the centre with xylem in the epidermis'] if x != pos[0]],
                  f'{cap(organ)}: {pos[0]}.')
    return Q(f'Describe the position of the xylem and phloem in a {organ} and suggest one advantage of this arrangement.', f'{cap(pos[0])}. Advantage: {pos[1]}.', f'xylem position [1]; phloem position [1]; advantage [1] [3]', 'short', 3)


DYE = {'setup': lambda r, p: f'{p} placed leafy celery stalks in beakers of red dye solution at different temperatures and measured how far the dye had travelled up the xylem after 30 minutes.',
       'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[10, 15, 20, 25, 30], [15, 20, 25, 30, 35], [5, 15, 25, 35]]),
       'dv': ('distance moved by dye', 'mm'), 'y': lambda x, k: k * (12 + 2.6 * x), 'dp': 0,
       'controls': ['concentration of dye', 'number of leaves / size of stalk', 'light intensity', 'humidity', 'time in the dye'],
       'why': ('Higher temperature increases the rate of evaporation from the leaves (transpiration), so water and dye are pulled up the xylem faster.', 'more evaporation / transpiration [1]; faster water movement in xylem [1] [2]'),
       'improve': ['cut all stalks to the same length with the same number of leaves', 'use a water bath to control each temperature']}
add_practical(t, DYE, C3D=(2, 3, 4), C4D=(3, 4))


@t.add('C4', (3, 4, 5), 'multi_step')
def xp_case(r, D):
    intro = f'A student in {city(r)} examines thin sections of a sunflower stem and root under a microscope after staining with a dye that colours lignin red.'
    parts = [lambda r: ('Describe where the red-stained tissue would appear in each section.', 'Stem: in the inner part of vascular bundles arranged in a ring near the outside. Root: in a star shape in the centre.', 'stem [1]; root [1] [2]'),
             lambda r: ('Name the tissue that is stained red and explain why it contains lignin.', 'Xylem: lignin makes the walls strong to support the plant and waterproof.', 'xylem [1]; support / waterproof [1] [2]'),
             lambda r: ('Compare the structure of xylem vessels and phloem sieve tubes.', 'Xylem: dead, hollow, lignified, no end walls. Phloem: living sieve tubes with perforated sieve plates, cytoplasm, no lignin.', 'two comparisons [2]'),
             lambda r: ('Suggest why the leaves of a plant would wilt if the xylem in its stem were blocked.', 'Water could not reach the leaves to replace water lost in transpiration, so cells lose turgor.', 'no water supply [1]; loss of turgor [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t_c8a = t

PATH = ['soil water', 'root hair cell', 'root cortex cells', 'xylem in the root', 'xylem in the stem', 'xylem in the leaf', 'mesophyll cells', 'air spaces', 'stomata']
t = T('Water uptake by root hair cells and the pathway through the plant', 'water uptake by root hair cells', 'pathway through the plant')
facts(t, [('root hair', 'a long, thin extension of a root epidermis cell that increases surface area for uptake of water and ions'),
          ('transpiration pull', 'the pulling of water up the xylem caused by evaporation of water from the leaves'),
          ('cortex', 'the tissue between the epidermis and the xylem of a root through which water passes'), ('water potential gradient', 'a difference in water potential that causes water to move by osmosis')])
mcqs(t, [('How does water enter root hair cells?', 'By osmosis', 'Soil water has a higher water potential than the cell sap.', ['By active transport', 'By diffusion of glucose', 'By translocation']),
         ('Which is the correct pathway of water through a plant?', 'root hair cell → root cortex cells → xylem → mesophyll cells', 'Water moves across the root to the xylem, up the stem and into leaf mesophyll.', ['xylem → root hair cell → phloem → stomata', 'root hair cell → phloem → mesophyll cells → xylem', 'stomata → xylem → root hair cell → soil']),
         ('Why does a root have many root hairs?', 'To increase the surface area for absorption', 'More surface for osmosis and ion uptake.', ['To anchor the plant only', 'To carry out photosynthesis', 'To store starch'])])
shorts(t, [('Describe the pathway of water from the soil to the leaves.', 'Soil → root hair cell (osmosis) → root cortex cells → xylem in root → xylem in stem → xylem in leaf → mesophyll cells.', 'correct sequence [2]; one omission [1] [2]'),
           ('State why root hair cells have no chloroplasts.', 'They are underground and receive no light.', '[1]')])
explain(t, [('Explain how water moves from the soil into a root hair cell.', 'Soil water has a higher water potential than the cell sap (which contains dissolved ions and sugars), so water moves in by osmosis through the partially permeable membrane.', 'water potential comparison [1]; osmosis through membrane [1] [2]'),
            ('Explain why plants that are transplanted often wilt.', 'Root hairs are damaged or torn off when the plant is dug up, reducing the surface area for water uptake, so less water is absorbed than is lost by transpiration.', 'root hairs damaged [1]; less uptake than loss [1] [2]'),
            ('Explain why adding a lot of fertiliser to dry soil can make plants wilt.', 'The soil water becomes concentrated (lower water potential than root cells), so water leaves the root cells by osmosis instead of entering.', 'lower water potential in soil [1]; water lost from roots [1] [2]'),
            ('Explain how water moves up the xylem in the stem.', 'Water evaporates from leaf mesophyll and diffuses out of stomata, creating a transpiration pull; water molecules stick together, so a continuous column is drawn up the xylem.', 'evaporation / transpiration pull [1]; cohesion / continuous column [1] [2]')])
myths(t, [('Water is pumped up the xylem by the heart of the plant.', 'Plants have no pump; water is pulled up by transpiration (evaporation from leaves).'), ('Water enters root hairs by active transport.', 'Water enters by osmosis; mineral ions enter by active transport.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def path_order(r, D):
    n = 4 if D <= 2 else 6
    start = r.randrange(0, len(PATH) - n + 1)
    seg = PATH[start:start + n]
    sh = seg[:]
    while sh == seg:
        r.shuffle(sh)
    if D == 1:
        x = r.randrange(len(seg) - 1)
        nxt = seg[x + 1]
        return MQ(r, f'Water moving through a plant passes from the {seg[x]} directly into which structure?', nxt, [p for p in PATH if p not in (nxt, seg[x])], f'Sequence: {" → ".join(PATH)}.')
    return Q(f'Put these in the order in which water passes through them on its way through a plant: {", ".join(sh)}.', ' → '.join(seg), f'{" → ".join(seg)} (all correct [2]; one pair reversed [1]) [2]', 'short', 2)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def roothair(r, D):
    n = r.choice([200, 300, 400, 500])
    L = r.choice([0.2, 0.5, 0.8, 1.0])
    d = r.choice([0.01, 0.012, 0.015])
    sa = math.pi * d * L
    tot = n * sa
    st = f'A 1 cm length of root has {n} root hairs. Each root hair is a cylinder {fx(L)} mm long and {fx(d, 3)} mm in diameter. Calculate the total surface area added by the root hairs (side area of cylinder = π × diameter × length).'
    key = f'one hair = π × {fx(d, 3)} × {fx(L)} = {sf(sa, 3)} mm² [1]; × {n} = {sf(tot, 3)} mm² [1]'
    m = 2
    if D >= 4:
        st += ' Explain why this large surface area is important.'
        key += '; faster uptake of water by osmosis and ions by active transport [1]'
        m = 3
    return Q(st, f'{sf(tot, 3)} mm²', key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def water_case(r, D):
    intro = f'{person(r)} waters a pot plant on a hot afternoon in {city(r)}. Within an hour the drooping leaves become firm again.'
    parts = [lambda r: ('Explain how water enters the roots.', 'By osmosis into root hair cells, from soil water with a higher water potential through partially permeable membranes.', 'osmosis [1]; water potential gradient [1] [2]'),
             lambda r: ('Describe the pathway taken by the water to reach the leaf cells.', 'Root hair → cortex cells → xylem of root → stem xylem → leaf xylem → mesophyll cells.', 'sequence [2]'),
             lambda r: ('Explain why the leaves become firm.', 'Water enters leaf cells by osmosis; vacuoles swell and cells become turgid, supporting the leaf.', 'turgid [1]; support [1] [2]'),
             lambda r: ('Explain why the plant drooped earlier in the afternoon.', 'On a hot day transpiration was faster than water uptake, so cells lost water, became flaccid and the plant wilted.', 'loss > uptake [1]; flaccid / wilting [1] [2]'),
             lambda r: ('Suggest why root hairs make the plant more efficient at taking up water.', 'They greatly increase the surface area of the root in contact with soil water.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t_c8b = t

t = T('Transpiration and factors affecting its rate; wilting', 'transpiration', 'factors affecting its rate', 'wilting')
facts(t, [('transpiration', 'the loss of water vapour from leaves, by evaporation from mesophyll cell surfaces and diffusion out through the stomata'), ('potometer', 'apparatus used to measure the rate of water uptake by a leafy shoot, which is close to the rate of transpiration'),
          ('wilting', 'drooping of a plant when cells lose turgor because water loss exceeds water uptake'), ('humidity', 'the amount of water vapour in the air'),
          ('stoma', 'a pore in the leaf surface, controlled by guard cells, through which water vapour diffuses out')])
mcqs(t, [('Which condition increases the rate of transpiration?', 'High wind speed', 'Wind removes water vapour, maintaining a steep diffusion gradient.', ['High humidity', 'Low temperature', 'Darkness']),
         ('Why does transpiration slow down in humid conditions?', 'The concentration gradient of water vapour between leaf and air is smaller', 'Less difference in water vapour concentration means slower diffusion.', ['Stomata get blocked by water', 'Xylem stops working', 'Roots stop absorbing water']),
         ('A potometer actually measures', 'the rate of water uptake by the shoot', 'Most water taken up is transpired, but some is used in photosynthesis or kept in cells.', ['the exact rate of transpiration', 'the rate of photosynthesis', 'the volume of sugar transported'])])
shorts(t, [('State four factors that affect the rate of transpiration.', 'Temperature, humidity, wind speed, light intensity.', 'four [2]; two or three [1] [2]'), ('State why a potometer must be set up with the shoot cut under water.', 'To prevent air entering the xylem and breaking the water column.', '[1]')])
explain(t, [('Explain why the rate of transpiration increases with temperature.', 'Water molecules have more kinetic energy, so evaporation from mesophyll cells and diffusion of water vapour out of the stomata are faster.', 'more kinetic energy / evaporation [1]; faster diffusion [1] [2]'),
            ('Explain why transpiration is faster in bright light than in darkness.', 'Stomata open in light (for photosynthesis), so more water vapour diffuses out; in darkness stomata close.', 'stomata open in light [1]; more diffusion [1] [2]'),
            ('Explain how wilting can help a plant survive a hot afternoon.', 'Drooping leaves are less exposed to the sun and stomata may close, reducing the surface area exposed and the rate of water loss.', 'less exposure / surface [1]; less water loss [1] [2]'),
            ('Explain why removing some leaves from a cutting before planting reduces wilting.', 'Fewer leaves means less surface area and fewer stomata for water loss, while the roots are too small to absorb much water.', 'less surface / stomata [1]; balance with limited uptake [1] [2]'),
            ('Explain why the bubble in a potometer moves more slowly when a plastic bag is placed over the shoot.', 'Humidity inside the bag increases, reducing the water vapour gradient between leaf and air, so transpiration and water uptake slow.', 'higher humidity [1]; smaller gradient / slower diffusion [1] [2]')])
myths(t, [('Transpiration happens mainly through the waxy cuticle.', 'Most water vapour is lost through the stomata; the cuticle reduces water loss.'), ('Windy weather reduces transpiration because it cools the leaves.', 'Wind increases transpiration by removing water vapour from around the leaf, keeping a steep gradient.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def potometer(r, D):
    dist = r.choice([24, 30, 36, 45, 48, 60, 72])
    tm = r.choice([3, 4, 5, 6, 10])
    rad = r.choice([0.5, 0.25, 0.4])
    rate = dist / tm
    vol = math.pi * rad * rad * dist
    if D == 1:
        return NQ(r, f'In a potometer the air bubble moved {dist} mm in {tm} minutes. What is the rate of movement of the bubble?', rate, [dist * tm, tm / dist, rate * 60, rate / 60], ' mm/min', f'{dist} ÷ {tm} = {fx(rate, 2)} mm/min.', f=lambda v: fx(v, 3))
    if D == 2:
        return Q(f'In a potometer the air bubble moved {dist} mm in {tm} minutes. Calculate the rate of water uptake in mm per minute.', f'{fx(rate, 2)} mm/min', f'{dist} ÷ {tm} [1] = {fx(rate, 2)} mm/min [1] [2]', 'numerical', 2)
    st = (f'A potometer has a capillary tube of radius {fx(rad, 2)} mm. The bubble moved {dist} mm in {tm} minutes. Calculate the volume of water taken up per minute in mm³ (volume = πr² × distance).')
    key = f'volume = π × {fx(rad, 2)}² × {dist} = {fx(vol, 1)} mm³ [1]; ÷ {tm} = {fx(vol / tm, 2)} mm³/min [1]'
    m = 2
    ans = f'{fx(vol / tm, 2)} mm³/min'
    if D >= 4:
        f = r.choice([0.6, 0.5, 0.4])
        st += f' When a fan was switched off the bubble moved only {fx(dist * f)} mm in the same time. Calculate the percentage decrease in the rate and explain the change.'
        ans += f'; decrease {fx((1 - f) * 100, 1)}%; without wind, water vapour builds up around the leaf, reducing the concentration gradient, so diffusion is slower.'
        key += f'; ({dist} − {fx(dist * f)}) ÷ {dist} × 100 = {fx((1 - f) * 100, 1)}% [1]; less air movement → water vapour not removed → smaller gradient [1]'
        m = 4
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


TR = {'setup': lambda r, p: f'{p} used a potometer to measure the distance moved by an air bubble in 5 minutes for a leafy shoot placed at different distances from a fan.',
      'iv': ('distance from fan', 'm'), 'xs': lambda r: r.choice([[0.5, 1.0, 1.5, 2.0, 2.5], [0.25, 0.5, 1.0, 2.0, 3.0]]),
      'dv': ('distance moved by bubble', 'mm'), 'y': lambda x, k: k * (12 + 40 / (x + 0.6)), 'dp': 0,
      'controls': ['temperature', 'humidity', 'light intensity', 'same leafy shoot'],
      'trend': lambda d: 'As the distance from the fan increases, the distance moved by the bubble decreases: the rate of water uptake falls.',
      'why': ('Closer to the fan the wind speed is higher; moving air removes water vapour from around the leaves, keeping a steep concentration gradient so water vapour diffuses out of the stomata faster.', 'higher wind speed [1]; water vapour removed / gradient maintained [1]; faster diffusion from stomata [1] [3]'),
      'improve': ['allow the shoot to adjust for 5 minutes at each new position', 'reset the bubble with the reservoir between readings', 'use an anemometer to measure wind speed directly'],
      'extra': [lambda r, d: ('Calculate the rate of water uptake closest to the fan, in mm per minute.', f'{fx(d["means"][0] / 5, 2)} mm/min', f'{fx(d["means"][0], 1)} ÷ 5 [1] = {fx(d["means"][0] / 5, 2)} mm/min [1] [2]'),
                lambda r, d: ('Explain why a potometer measures water uptake rather than transpiration.', 'Some water taken up is used by the plant (e.g. photosynthesis, turgor) and not transpired.', '[1]')]}
TR2 = {'setup': lambda r, p: f'{p} measured the mass lost by potted plants (with the soil surface sealed in plastic) over 24 hours at different temperatures.',
       'iv': ('temperature', '°C'), 'xs': lambda r: r.choice([[10, 15, 20, 25, 30], [15, 20, 25, 30, 35]]), 'dv': ('mass lost', 'g'), 'y': lambda x, k: k * (2 + 0.06 * x * x), 'dp': 1,
       'controls': ['humidity', 'light intensity', 'wind speed', 'size of plant / number of leaves', 'volume of water in soil at start'],
       'why': ('At higher temperatures water molecules have more kinetic energy, so more water evaporates from mesophyll cells and diffuses out of the stomata faster.', 'more kinetic energy [1]; faster evaporation and diffusion [1] [2]'),
       'improve': ['use plants of the same species and size', 'measure leaf area and calculate mass lost per cm²'],
       'control': 'Set up a pot with soil but no plant, sealed in the same way, to show that mass loss is due to transpiration from the leaves.',
       'extra': [lambda r, d: (f'Calculate the percentage increase in mass lost from {fx(d["xs"][0])} °C to {fx(d["xs"][-1])} °C.', f'{fx(pct(d["means"][0], d["means"][-1]), 0)}%', f'({fx(d["means"][-1], 2)} − {fx(d["means"][0], 2)}) ÷ {fx(d["means"][0], 2)} × 100 [1] = {fx(pct(d["means"][0], d["means"][-1]), 0)}% [1] [2]')]}
add_practical(t, TR, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))
add_practical(t, TR2, C3D=(3, 4), C4D=(3, 4, 5))


@t.add('C3', (2, 3), 'short')
def tr_predict(r, D):
    ch = r.choice([('the humidity of the air increases', 'decreases', 'smaller water vapour concentration gradient'), ('the temperature rises from 15 °C to 25 °C', 'increases', 'more kinetic energy, faster evaporation and diffusion'),
                   ('the plant is moved into darkness', 'decreases', 'stomata close'), ('a fan is switched on', 'increases', 'water vapour removed from around the leaf, steeper gradient'),
                   ('petroleum jelly is spread on the lower surface of the leaves', 'decreases', 'stomata on the lower surface are blocked'), ('the light intensity increases', 'increases', 'more stomata open')])
    return Q(f'Predict and explain how the rate of transpiration of a plant changes when {ch[0]}.', f'It {ch[1]}: {ch[2]}.', f'{ch[1]} [1]; {ch[2]} [1] [2]', 'short', 2)


longs(t, [('Describe how a potometer can be used to investigate the effect of wind speed on the rate of transpiration.', 'Cut a shoot under water and fit it into a water-filled potometer, sealing joints with petroleum jelly; introduce an air bubble; place a fan at different distances; measure the distance the bubble moves in a fixed time; reset with reservoir; repeat; keep temperature, light and humidity constant.',
           'shoot cut under water / airtight [1]; bubble measurement over fixed time [1]; vary wind (fan distance) [1]; control variables [1]; repeats / calculate rate [1] [5]')])
t_c8c = t

t = T('Translocation of sucrose and amino acids from sources to sinks', 'translocation', 'sources to sinks')
facts(t, [('translocation', 'the movement of sucrose and amino acids in phloem from regions of production (sources) to regions of storage or use (sinks)'),
          ('source', 'a part of a plant that releases sucrose or amino acids, such as a photosynthesising leaf'), ('sink', 'a part of a plant that uses or stores sucrose or amino acids, such as roots, fruits or growing buds'),
          ('sucrose', 'the sugar transported in the phloem'), ('aphid', 'a small insect that feeds on phloem sap by pushing its mouthparts into a sieve tube')])
mcqs(t, [('In spring, a potato tuber supplies sucrose to the growing shoots. What is the tuber acting as?', 'A source', 'A storage organ releasing sucrose is a source.', ['A sink', 'A stoma', 'A xylem vessel']),
         ('Which tissue carries out translocation?', 'Phloem', 'Sucrose and amino acids move in phloem sieve tubes.', ['Xylem', 'Epidermis', 'Palisade mesophyll']),
         ('In which direction can translocation take place?', 'Both up and down the plant', 'Phloem carries substances from sources to sinks wherever they are.', ['Only upwards', 'Only downwards', 'Only into leaves'])])
shorts(t, [('Give two examples of sinks in a plant.', 'Roots, developing fruits / seeds, growing buds, storage organs.', '[2]'), ('State why plants transport sucrose rather than glucose.', 'Sucrose is less reactive (and it is not used in respiration on the way), so it can be transported efficiently.', '[1]')])
explain(t, [('Explain why a part of a plant can be a source at one time of year and a sink at another.', 'A storage organ such as a tuber is a sink while it stores starch in summer, but a source when it releases sucrose for new growth in spring.', 'sink when storing [1]; source when releasing [1] [2]'),
            ('A ring of bark (including the phloem) is removed from a tree trunk. Explain why the bark just above the ring swells.', 'Sucrose moving down in the phloem from the leaves cannot pass the ring, so it accumulates above it, drawing in water and causing growth / swelling.', 'phloem removed [1]; sugars accumulate above [1] [2]'),
            ('Explain why aphids are useful to scientists studying translocation.', 'Their mouthparts enter a single sieve tube; if the aphid is removed, the mouthparts can be used to collect phloem sap for analysis.', 'feed from one sieve tube [1]; sap collected / analysed [1] [2]')])
myths(t, [('Translocation only moves sugar down to the roots.', 'Translocation moves sugar from sources to sinks in any direction, e.g. up to fruits and buds.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def src_sink(r, D):
    cases = [('a mature leaf photosynthesising in summer', 'source'), ('a developing mango fruit', 'sink'), ('the root tips of a seedling', 'sink'), ('a potato tuber in spring as shoots grow', 'source'),
             ('a potato tuber in summer as it stores starch', 'sink'), ('a growing shoot tip', 'sink'), ('a carrot root in its second year when the plant flowers', 'source'), ('developing seeds in a pea pod', 'sink')]
    if D <= 2:
        x, a = r.choice(cases)
        return MQ(r, f'Is {x} acting as a source or a sink?', a, ['source', 'sink', 'neither', 'both at once'], f'{cap(x)}: {a}.')
    xs = r.sample(cases, 3)
    labs = ['(i)', '(ii)', '(iii)']
    return Q('State whether each is acting as a source or a sink, giving a reason: ' + ' '.join(f'{labs[i]} {x}' for i, (x, _) in enumerate(xs)) + '.',
             ' '.join(f'{labs[i]} {a} — ' + ('releases sucrose' if a == 'source' else 'uses or stores sucrose') for i, (x, a) in enumerate(xs)),
             '; '.join(f'{labs[i]} {a} [1]' for i, (x, a) in enumerate(xs)) + '; one reason linked to releasing or using / storing sucrose [1] [4]', 'short', 4)


@t.add('C3', (2, 3, 4, 5), 'case')
def radio(r, D):
    l = r.randrange(40, 60)
    rt = r.randrange(10, 25)
    fr = 100 - l - rt
    st = f'A leaf was supplied with radioactive carbon dioxide. After 6 hours, the radioactivity was found in: leaf {l}%, roots {rt}%, developing fruits {fr}%. (a) Name the substance in which the radioactive carbon was transported. (b) Name the tissue it was carried in. (c) Explain why radioactivity was found in both the roots and the fruits.'
    ans = '(a) sucrose (b) phloem (c) translocation carries sucrose from the source (leaf) to sinks in any direction — down to the roots and up to the fruits.'
    key = '(a) sucrose [1] (b) phloem [1] (c) source to sinks [1]; both directions [1]'
    m = 4
    if D >= 4:
        st += ' (d) Suggest why the fruits received the largest share.'
        ans += ' (d) Developing fruits are strong sinks, growing fast and storing sugars.'
        key += ' (d) fruits use / store most sugar [1]'
        m = 5
    if fr <= rt:
        return None
    return Q(st, ans, key + f' [{m}]', 'case', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def trans_case(r, D):
    intro = f'A farmer in {city(r)} removes a complete ring of bark (including the phloem but not the xylem) from the branch of a fruit tree below a cluster of developing fruits.'
    parts = [lambda r: ('Predict the effect on the fruits above the ring, and explain.', 'They may grow larger: sucrose from leaves above the ring cannot move down past it, so more is available to the fruits.', 'larger fruits [1]; sucrose cannot leave the branch [1] [2]'),
             lambda r: ('Explain why the leaves on the branch do not wilt.', 'The xylem is intact, so water still reaches the leaves.', '[2]'),
             lambda r: ('Predict what would happen to the roots in the long term if a ring was removed from the main trunk.', 'Roots receive no sucrose for respiration, so they die, and then the whole tree dies.', 'no sucrose to roots [1]; die [1] [2]'),
             lambda r: ('Define translocation.', 'Movement of sucrose and amino acids in phloem from sources to sinks.', '[2]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


longs(t, [('Compare transport in the xylem and the phloem.', 'Xylem: water and mineral ions, upwards only, dead lignified hollow vessels, transpiration pull, no energy needed. Phloem: sucrose and amino acids, in both directions from sources to sinks, living sieve tubes, needs energy.',
           'substances [1]; direction [1]; cell structure [1]; mechanism / energy [1]; one similarity (both in vascular bundles) [1] [5]')])
t_c8d = t
CHAPTERS[8] = [t_c8a, t_c8b, t_c8c, t_c8d]

# ===================================================================== 9 Transport in animals
t = T('Single and double circulatory systems', 'single and double circulatory systems', 'circulatory systems')
facts(t, [('circulatory system', 'a system of blood vessels with a pump and valves to ensure one-way flow of blood'), ('double circulation', 'a system in which blood passes through the heart twice for each complete circuit of the body'),
          ('single circulation', 'a system, as in fish, in which blood passes through the heart once for each complete circuit'), ('pulmonary circulation', 'the circuit that carries blood between the heart and the lungs'),
          ('systemic circulation', 'the circuit that carries blood between the heart and the rest of the body')])
mcqs(t, [('In a fish, blood flows from the heart to the', 'gills, then to the body, then back to the heart', 'Single circulation: heart → gills → body → heart.', ['body, then to the heart, then to the gills', 'lungs, then to the heart, then to the body', 'gills, then back to the heart, then to the body']),
         ('What is an advantage of a double circulatory system?', 'Blood is pumped at high pressure to the body after the lungs', 'Blood returns to the heart after the lungs and is re-pressurised, so delivery to tissues is fast.', ['Blood flows through the gills twice', 'Oxygenated and deoxygenated blood mix', 'The heart needs only one chamber']),
         ('How many times does blood pass through the human heart in one complete circuit of the body?', 'Twice', 'Pulmonary and systemic circuits.', ['Once', 'Three times', 'Four times'])])
shorts(t, [('Describe the route of blood in a single circulation.', 'Heart → gills → body organs → heart.', '[2]'), ('State the two circuits of the human double circulation.', 'Pulmonary circulation (heart–lungs) and systemic circulation (heart–body).', '[2]')])
explain(t, [('Explain the advantages of a double circulation in mammals.', 'Blood returns to the heart after collecting oxygen in the lungs and is pumped again at high pressure, so oxygen is delivered quickly to respiring tissues; low pressure in lungs avoids damage to capillaries.', 'high pressure to body [1]; fast oxygen delivery for high metabolic rate [1]; low pressure to lungs [1] [3]'),
            ('Explain why fish can survive with a single circulation.', 'Fish are supported by water and their body temperature is the same as the water, so they need less energy and oxygen than mammals; slower delivery is enough.', 'lower energy / oxygen demand [1]; no need to maintain body temperature [1] [2]'),
            ('Explain why blood pressure is low after passing through the gills of a fish.', 'Pressure is lost as blood is pushed through the narrow capillaries of the gills, and it is not re-pumped before going to the body.', 'pressure lost in capillaries [1]; not re-pumped [1] [2]')])
myths(t, [('In a double circulation, blood is pumped to the lungs and body at the same time from the same chamber.', 'The right ventricle pumps blood to the lungs and the left ventricle pumps blood to the body.'), ('Fish have a double circulation because they have two gills.', 'Fish have a single circulation: blood passes through the heart once per circuit.')])


@t.add('C3', (1, 2, 3), 'short')
def circ_route(r, D):
    route = ['vena cava', 'right atrium', 'right ventricle', 'pulmonary artery', 'lungs', 'pulmonary vein', 'left atrium', 'left ventricle', 'aorta', 'body organs']
    n = 4 if D <= 2 else 6
    s0 = r.randrange(0, len(route) - n + 1)
    seg = route[s0:s0 + n]
    if D == 1:
        x = r.randrange(n - 1)
        return MQ(r, f'Blood leaving the {seg[x]} passes next into the', seg[x + 1], [y for y in route if y not in (seg[x], seg[x + 1])], f'Route: {" → ".join(route)}.')
    sh = seg[:]
    while sh == seg:
        r.shuffle(sh)
    return Q(f'Put these in the order in which blood flows through them in the human double circulation: {", ".join(sh)}.', ' → '.join(seg), f'{" → ".join(seg)} (all correct [2]; one error [1]) [2]', 'short', 2)


@t.add('C4', (3, 4, 5), 'multi_step')
def circ_case(r, D):
    p_fish = r.choice([25, 30, 35])
    p_gill = round(p_fish * r.uniform(0.35, 0.5))
    p_mam = r.choice([110, 120, 130])
    intro = f'Blood pressure was measured in a fish: {p_fish} mmHg leaving the heart and {p_gill} mmHg after the gills. In a mammal, pressure leaving the left ventricle is {p_mam} mmHg.'
    parts = [lambda r: ('Calculate the percentage decrease in blood pressure as blood passes through the gills.', f'{fx((p_fish - p_gill) / p_fish * 100, 1)}%', f'({p_fish} − {p_gill}) ÷ {p_fish} × 100 [1] = {fx((p_fish - p_gill) / p_fish * 100, 1)}% [1] [2]'),
             lambda r: ('Explain why the pressure falls in the gills.', 'Friction / resistance in the narrow gill capillaries.', '[1]'),
             lambda r: ('Explain how the double circulation of the mammal avoids this problem.', 'Blood returns to the heart from the lungs and is pumped again by the left ventricle at high pressure to the body.', 'returns to heart [1]; re-pumped at high pressure [1] [2]'),
             lambda r: ('Suggest why mammals need a higher blood pressure to their body than fish.', 'Mammals have high metabolic rates (maintaining body temperature) so need rapid delivery of oxygen and glucose to cells.', 'higher energy demand [1]; faster delivery [1] [2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t_c9a = t

t = T('Structure and function of the heart; heart rate and coronary heart disease', 'structure and function of the heart', 'heart rate', 'coronary heart disease')
facts(t, [('atrium', 'an upper chamber of the heart that receives blood from veins'), ('ventricle', 'a lower, muscular chamber of the heart that pumps blood into arteries'),
          ('septum', 'the wall of muscle that separates the left and right sides of the heart'), ('coronary arteries', 'arteries that supply the heart muscle with oxygen and glucose'),
          ('coronary heart disease', 'a disease in which the coronary arteries become blocked by fatty deposits, reducing the supply of oxygen to heart muscle'),
          ('heart rate', 'the number of times the heart beats per minute')])
mcqs(t, [('Why is the wall of the left ventricle thicker than the wall of the right ventricle?', 'It pumps blood all round the body at higher pressure', 'The right ventricle pumps only to the lungs (lower pressure).', ['It pumps blood to the lungs', 'It holds more blood', 'It receives blood from the vena cava']),
         ('What is the function of the valves in the heart?', 'To prevent the backflow of blood', 'Atrioventricular and semilunar valves keep flow one-way.', ['To pump blood', 'To oxygenate the blood', 'To produce red blood cells']),
         ('Which is a risk factor for coronary heart disease?', 'Smoking', 'Risk factors: diet high in saturated fat, smoking, stress, lack of exercise, genetics, age, sex.', ['Eating plenty of fibre', 'Regular exercise', 'Low blood pressure'])])
shorts(t, [('Name the four chambers of the heart.', 'Right atrium, right ventricle, left atrium, left ventricle.', '[1]'), ('State four risk factors for coronary heart disease.', 'Diet high in saturated fat, smoking, lack of exercise, stress, genetic factors, age, being male.', 'four [2]; two or three [1] [2]')])
explain(t, [('Explain why heart rate increases during exercise.', 'Muscles respire faster and need more oxygen and glucose and must remove more carbon dioxide; a faster heart rate pumps blood to them more quickly.', 'more oxygen / glucose needed [1]; remove CO₂ [1]; faster delivery [1] [3]'),
            ('Explain how a blocked coronary artery can cause a heart attack.', 'Heart muscle beyond the blockage receives no oxygen or glucose, so it cannot respire aerobically and stops contracting or dies.', 'no oxygen to heart muscle [1]; cannot respire / dies [1] [2]'),
            ('Explain why the septum is important.', 'It separates oxygenated blood in the left side from deoxygenated blood in the right side, so they do not mix and the body receives highly oxygenated blood.', 'prevents mixing [1]; more oxygen delivered [1] [2]'),
            ('Describe how stents and angioplasty treat coronary heart disease.', 'A balloon is inflated in the narrowed artery to widen it (angioplasty) and a mesh tube (stent) is left in place to hold it open, restoring blood flow.', 'balloon widens [1]; stent holds open [1] [2]'),
            ('Explain how regular exercise can reduce the risk of coronary heart disease.', 'Exercise strengthens the heart muscle, helps reduce blood pressure, body mass and blood cholesterol, so fewer fatty deposits form in coronary arteries.', 'lower cholesterol / mass / pressure [1]; less fatty deposit / blockage [1] [2]'),
            ('Explain how the atrioventricular valves work when the ventricles contract.', 'Pressure in the ventricles rises above that in the atria, pushing the valves shut so blood cannot flow back into the atria; it is forced into the arteries.', 'pressure difference closes valves [1]; prevents backflow into atria [1] [2]')])
myths(t, [('The left side of the heart pumps deoxygenated blood to the lungs.', 'The right side pumps deoxygenated blood to the lungs; the left side pumps oxygenated blood to the body.'),
           ('The heart muscle gets oxygen from the blood inside its chambers.', 'Heart muscle is supplied by the coronary arteries.'), ('Arteries always carry oxygenated blood.', 'The pulmonary artery carries deoxygenated blood to the lungs.')])

HR = {'setup': lambda r, p: f'{p} measured the pulse rate of a group of students at rest and then every minute after 2 minutes of step-ups.',
      'iv': ('time after exercise', 'min'), 'xs': lambda r: [0, 1, 2, 3, 4, 5, 6], 'dv': ('pulse rate', 'beats/min'), 'y': lambda x, k: 70 * (0.9 + 0.1 * k) + 60 * k * math.exp(-x / 1.8), 'dp': 0, 'noise': 0.03,
      'controls': ['duration and intensity of exercise (step height, rate)', 'same group of students', 'position (sitting) when measuring', 'method of counting pulse (e.g. 15 s × 4)'],
      'trend': lambda d: 'The pulse rate is highest immediately after exercise and then decreases, returning towards the resting rate after several minutes.',
      'why': ('During exercise muscles respire faster and need more oxygen and glucose; the heart rate rises to supply them. After exercise the demand falls, but the rate stays high for a while to remove CO₂ and lactic acid (repay the oxygen debt).', 'more respiration / oxygen needed [1]; heart rate supplies muscles [1]; recovery / oxygen debt [1] [3]'),
      'improve': ['use a pulse oximeter / heart rate monitor for accuracy', 'use a metronome so every student steps at the same rate'],
      'extra': [lambda r, d: ('Calculate the percentage increase in pulse rate from the value at 6 minutes to the value immediately after exercise.', f'{fx(pct(d["means"][-1], d["means"][0]), 0)}%', f'({fx(d["means"][0], 1)} − {fx(d["means"][-1], 1)}) ÷ {fx(d["means"][-1], 1)} × 100 [1] = {fx(pct(d["means"][-1], d["means"][0]), 0)}% [1] [2]')]}
add_practical(t, HR, C3D=(2, 3, 4, 5), C4D=(3, 4, 5))


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def hr_calc(r, D):
    beats = r.choice([17, 18, 19, 20, 21, 22, 24, 30])
    secs = r.choice([15, 20, 30])
    hr = beats * 60 / secs
    if D == 1:
        return NQ(r, f'A student counts {beats} pulse beats in {secs} seconds. What is the heart rate?', hr, [beats * secs, beats, hr / 2, hr * 2], ' beats/min', f'{beats} × (60 ÷ {secs}) = {fx(hr)} beats/min.', f=lambda v: fx(v, 1))
    st = f'{person(r)} counts {beats} pulse beats in {secs} seconds. Calculate the heart rate in beats per minute.'
    key = f'{beats} × 60 ÷ {secs} [1] = {fx(hr)} beats/min [1]'
    m = 2
    ans = f'{fx(hr)} beats/min'
    if D >= 3:
        sv = r.choice([70, 75, 80])
        co = hr * sv / 1000
        st += f' Each beat pumps {sv} cm³ of blood. Calculate the volume of blood pumped per minute (cardiac output) in dm³.'
        ans += f'; {fx(co, 2)} dm³/min'
        key += f'; {fx(hr)} × {sv} = {fx(hr * sv)} cm³ [1] = {fx(co, 2)} dm³/min [1]'
        m = 4
    if D >= 5:
        st += ' Suggest why counting for 60 seconds would be more accurate.'
        ans += '; a longer count reduces the error from a missed or extra beat.'
        key += '; smaller percentage error / missed beat matters less [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C3', (2, 3, 4), 'case')
def chd_data(r, D):
    groups = [('non-smokers', r.randrange(60, 110)), ('light smokers', r.randrange(140, 220)), ('heavy smokers', r.randrange(260, 420))]
    tab = '; '.join(f'{g}: {v}' for g, v in groups)
    a, b = groups[0][1], groups[2][1]
    st = f'Deaths from coronary heart disease per 100 000 men aged 45–64 in a study in {city(r)}: {tab}. (a) Calculate how many times greater the death rate is for heavy smokers than for non-smokers. (b) Explain how smoking increases the risk of coronary heart disease.'
    ans = f'(a) {fx(b / a, 2)} times (b) Chemicals in smoke (and nicotine) damage artery linings and raise blood pressure, encouraging fatty deposits in coronary arteries; carbon monoxide reduces oxygen carried.'
    key = f'(a) {b} ÷ {a} = {fx(b / a, 2)} [1] (b) damages artery walls / raises blood pressure [1]; fatty deposits block coronary arteries [1]'
    m = 3
    if D >= 4:
        st += ' (c) Explain why these data alone do not prove that smoking causes heart disease.'
        ans += ' (c) It shows a correlation; other factors (diet, exercise, stress) may differ between groups.'
        key += ' (c) correlation not causation / other variables [1]'
        m = 4
    return Q(st, ans, key + f' [{m}]', 'case', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def heart_case(r, D):
    intro = f'A doctor in {city(r)} listens to a patient\'s heart and explains how the heart pumps blood through the double circulation.'
    parts = [lambda r: ('Describe the pathway of blood through the heart from the vena cava to the aorta.', 'Vena cava → right atrium → right ventricle → pulmonary artery → lungs → pulmonary vein → left atrium → left ventricle → aorta.', 'right side [1]; lungs [1]; left side [1] [3]'),
             lambda r: ('Explain the function of the semilunar valves.', 'They stop blood flowing back from the arteries into the ventricles when the ventricles relax.', '[2]'),
             lambda r: ('Explain why the ventricle walls are thicker than the atrium walls.', 'Ventricles pump blood out of the heart to the lungs or body (further, higher pressure); atria pump only into the ventricles.', '[2]'),
             lambda r: ('The patient has a narrowed coronary artery. Suggest two lifestyle changes that could reduce the risk of a heart attack.', 'Stop smoking; eat less saturated fat / salt; exercise regularly; reduce stress; lose weight.', 'any two [2]'),
             lambda r: ('Describe one treatment for a narrowed coronary artery.', 'Angioplasty with a stent, or a bypass operation, or drugs such as aspirin / statins.', '[1]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the structure of the heart and explain how it is adapted to pump blood around the double circulation.', 'Four chambers; atria receive, ventricles pump; thick muscular left ventricle for high pressure to body, thinner right for lungs; septum prevents mixing; atrioventricular and semilunar valves prevent backflow; coronary arteries supply muscle.',
           'chambers and roles [1]; wall thickness [1]; septum [1]; valves [1]; coronary arteries [1]; vessels named [1] [6]')])
t_c9b = t

VES = {'artery': ('thick, elastic, muscular wall; narrow lumen', 'carries blood at high pressure away from the heart'), 'vein': ('thin wall, wide lumen, valves', 'carries blood at low pressure back to the heart'),
       'capillary': ('wall one cell thick; very narrow lumen', 'exchanges substances between blood and tissues')}
t = T('Blood vessels: arteries, veins and capillaries', 'blood vessels', 'arteries, veins and capillaries')
facts(t, [('artery', 'a blood vessel with a thick muscular, elastic wall that carries blood away from the heart at high pressure'), ('vein', 'a blood vessel with a thin wall, wide lumen and valves that carries blood back to the heart at low pressure'),
          ('capillary', 'a tiny blood vessel with a wall one cell thick where substances are exchanged with tissues'), ('lumen', 'the space inside a blood vessel through which blood flows'),
          ('hepatic portal vein', 'the vein that carries blood from the gut to the liver'), ('renal artery', 'the artery that carries blood to the kidney')])
mcqs(t, [('Why do veins contain valves?', 'To prevent backflow of blood at low pressure', 'Blood pressure in veins is low, so valves keep flow towards the heart.', ['To increase blood pressure', 'To allow exchange of gases', 'To pump blood']),
         ('Which vessel carries blood from the lungs to the heart?', 'Pulmonary vein', 'Pulmonary vein carries oxygenated blood to the left atrium.', ['Pulmonary artery', 'Aorta', 'Vena cava']),
         ('Why are capillary walls only one cell thick?', 'To give a short diffusion distance', 'Rapid exchange of oxygen, glucose and CO₂ with tissues.', ['To withstand high pressure', 'To prevent backflow', 'To store blood'])])
shorts(t, [('Name the blood vessels that carry blood to and from the kidneys.', 'Renal artery (to) and renal vein (from).', '[2]'), ('Name the main artery leaving the heart and the main vein returning blood from the body.', 'Aorta; vena cava.', '[2]')])
explain(t, [('Explain how the structure of an artery is related to its function.', 'Thick muscular and elastic walls withstand high pressure and stretch and recoil with each heartbeat to maintain pressure; narrow lumen keeps pressure high.', 'thick wall / high pressure [1]; elastic recoil [1] [2]'),
            ('Explain how blood in the veins of the legs returns to the heart.', 'Contraction of surrounding skeletal muscles squeezes the veins; valves prevent backflow, so blood is pushed towards the heart.', 'muscles squeeze [1]; valves prevent backflow [1] [2]'),
            ('Explain why capillaries form dense networks in active tissues such as muscles.', 'Every cell is close to a capillary, so the diffusion distance for oxygen and glucose is short and there is a large surface area for exchange.', 'short distance [1]; large surface area [1] [2]'),
            ('Explain why the pressure of blood in veins is lower than in arteries.', 'Pressure is lost as blood passes through narrow capillaries; veins are further from the heart.', '[2]')])
myths(t, [('Veins carry blood away from the heart.', 'Veins carry blood towards the heart; arteries carry blood away.'), ('Capillaries have thick walls to stop them bursting.', 'Capillary walls are one cell thick for fast diffusion; pressure in capillaries is lower than in arteries.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ves_id(r, D):
    v = r.choice(list(VES))
    if D <= 2:
        return MQ(r, f'Which blood vessel has this structure: {VES[v][0]}?', v, [x for x in VES if x != v] + ['lymph vessel'], f'{cap(v)}: {VES[v][0]}; {VES[v][1]}.')
    th = {'artery': r.randrange(800, 1200), 'vein': r.randrange(250, 500), 'capillary': 1}
    lum = {'artery': r.randrange(2000, 4000), 'vein': r.randrange(5000, 9000), 'capillary': 8}
    order = r.sample(list(VES), 3)
    labs = 'XYZ'
    tab = '; '.join(f'vessel {labs[i]}: wall {th[o]} μm, lumen {lum[o]} μm' for i, o in enumerate(order))
    return Q(f'Measurements of three blood vessels: {tab}. Identify each vessel and give a reason for each identification.', '; '.join(f'{labs[i]}: {o}' for i, o in enumerate(order)),
             '; '.join(f'{labs[i]} {o} [1]' for i, o in enumerate(order)) + '; reasons: artery thick wall / narrow lumen, vein thinner wall / wide lumen, capillary wall one cell (about 1 μm) [2] [5]', 'short', 5)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ves_pct(r, D):
    p1 = r.choice([110, 115, 120, 125])
    p2 = round(p1 * r.uniform(0.15, 0.3))
    p3 = r.randrange(3, 10)
    st = f'Blood pressure in the aorta is {p1} mmHg, in the capillaries {p2} mmHg and in the vena cava {p3} mmHg. Calculate the percentage decrease in pressure between the aorta and the capillaries.'
    key = f'({p1} − {p2}) ÷ {p1} × 100 [1] = {fx((p1 - p2) / p1 * 100, 1)}% [1]'
    ans = f'{fx((p1 - p2) / p1 * 100, 1)}%'
    m = 2
    if D >= 4:
        st += ' Explain why veins need valves but arteries do not (except at the heart).'
        ans += '; pressure in veins is very low, so blood could flow backwards; valves prevent backflow.'
        key += '; low pressure in veins [1]; valves prevent backflow [1]'
        m = 4
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def ves_case(r, D):
    intro = f'In a biology lesson in {city(r)}, students examine prepared slides of an artery and a vein cut in cross-section, and a capillary network in a muscle.'
    parts = [lambda r: ('Describe two differences between the artery and the vein that the students would see.', 'Artery: thicker, muscular, elastic wall and narrower lumen; vein: thinner wall, wider lumen (may look flattened) and valves.', '[2]'),
             lambda r: ('Explain how the structure of capillaries is adapted for exchange.', 'Walls one cell thick give short diffusion distance; many branches give large surface area; narrow lumen slows blood.', 'two points [2]'),
             lambda r: ('Name the vessels that carry blood to and from the liver.', 'Hepatic artery and hepatic portal vein (to); hepatic vein (from).', '[2]'),
             lambda r: ('Explain why the elastic fibres in artery walls are important.', 'They stretch when the ventricles pump blood and recoil between beats, smoothing flow and maintaining pressure.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t_c9c = t

BLOOD = [('red blood cells', 'transport oxygen (haemoglobin)'), ('phagocytes', 'engulf and digest pathogens (phagocytosis)'), ('lymphocytes', 'produce antibodies'),
         ('platelets', 'help blood to clot'), ('plasma', 'transports blood cells, ions, glucose, amino acids, hormones, CO₂, urea and plasma proteins')]
t = T('Components of blood and their functions; blood clotting', 'components of blood', 'blood clotting')
facts(t, [(a, b) for a, b in BLOOD] + [('fibrinogen', 'a soluble plasma protein that is converted into insoluble fibrin during clotting'), ('haemoglobin', 'the red protein in red blood cells that combines with oxygen')])
mcqs(t, [('Which blood component produces antibodies?', 'Lymphocytes', 'Lymphocytes make antibodies; phagocytes engulf pathogens.', ['Phagocytes', 'Platelets', 'Red blood cells']),
         ('What happens to fibrinogen during blood clotting?', 'It is converted into insoluble fibrin fibres', 'Fibrin forms a mesh that traps red blood cells.', ['It is converted into haemoglobin', 'It dissolves in plasma', 'It becomes a platelet']),
         ('Why is blood clotting important?', 'It prevents blood loss and entry of pathogens', 'A clot seals the wound.', ['It increases blood pressure', 'It carries oxygen', 'It digests pathogens'])])
shorts(t, [('Name the four main components of blood.', 'Red blood cells, white blood cells, platelets, plasma.', '[1]'), ('State two substances transported in plasma.', 'Glucose, amino acids, CO₂, urea, hormones, ions, plasma proteins.', '[2]')])
explain(t, [('Describe how a blood clot forms at a wound.', 'Platelets at the wound release chemicals; soluble fibrinogen is converted to insoluble fibrin; fibrin forms a mesh that traps red blood cells, forming a clot that dries to a scab.', 'platelets [1]; fibrinogen → fibrin [1]; mesh traps cells [1] [3]'),
            ('Explain why people living at high altitude have more red blood cells.', 'Air at altitude has less oxygen; more red blood cells (haemoglobin) allow enough oxygen to be carried to tissues.', 'less oxygen at altitude [1]; more haemoglobin to carry oxygen [1] [2]'),
            ('Explain how phagocytes protect the body.', 'They move towards pathogens, engulf them by phagocytosis and digest them with enzymes.', 'engulf [1]; digest [1] [2]'),
            ('Explain why a person with very few platelets bruises and bleeds easily.', 'Platelets are needed to start clotting; without enough, wounds do not seal quickly.', '[2]')])
myths(t, [('Platelets carry oxygen around the body.', 'Red blood cells carry oxygen; platelets help blood clot.'), ('White blood cells contain haemoglobin.', 'Red blood cells contain haemoglobin; white blood cells defend against pathogens.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def blood_id(r, D):
    a, b = r.choice(BLOOD)
    if D <= 2:
        return MQ(r, f'Which component of blood has this function: {b}?', a, [x[0] for x in BLOOD if x[0] != a], f'{cap(a)}: {b}.')
    xs = r.sample(BLOOD, 3)
    labs = ['(i)', '(ii)', '(iii)']
    return Q('State the function of each component of blood: ' + ', '.join(f'{labs[i]} {x[0]}' for i, x in enumerate(xs)) + '.', ' '.join(f'{labs[i]} {x[1]}' for i, x in enumerate(xs)), '; '.join(f'{labs[i]} {x[1]} [1]' for i, x in enumerate(xs)) + ' [3]', 'short', 3)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def blood_count(r, D):
    rbc = round(r.uniform(4.2, 5.8), 1)
    wbc = r.choice([5000, 6000, 7000, 8000, 9000, 15000, 20000])
    st = f'A blood test shows {rbc} million red blood cells and {wbc:,} white blood cells per mm³. Calculate the ratio of red blood cells to white blood cells, to the nearest whole number.'
    ratio = rbc * 1e6 / wbc
    key = f'{fx(rbc * 1e6, 0)} ÷ {wbc:,} [1] = {round(ratio)} : 1 [1]'
    ans = f'{round(ratio)} : 1'
    m = 2
    if D >= 4:
        normal = wbc <= 10000
        st += ' A normal white cell count is 4,000–10,000 per mm³. Suggest what the white cell count shows about this person.'
        ans += '; within the normal range.' if normal else '; high — the person may have an infection, as more lymphocytes and phagocytes are made.'
        key += '; normal [1]' if normal else '; high count [1]; suggests infection / immune response [1]'
        m = 3 if normal else 4
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def blood_case(r, D):
    intro = f'{person(r)} cuts a finger in the kitchen. Within a few minutes the bleeding stops and a scab forms. Two days later the area around the cut is red and swollen.'
    parts = [lambda r: ('Describe the process that stopped the bleeding.', 'Platelets trigger conversion of soluble fibrinogen to insoluble fibrin; fibrin mesh traps red blood cells forming a clot.', 'platelets [1]; fibrinogen → fibrin [1]; mesh / clot [1] [3]'),
             lambda r: ('Explain why the clot is important besides preventing blood loss.', 'It forms a barrier to the entry of pathogens.', '[1]'),
             lambda r: ('Suggest why the area became red and swollen.', 'Pathogens entered; more blood flows to the area and white blood cells move in to destroy pathogens.', 'infection [1]; white blood cells / blood flow [1] [2]'),
             lambda r: ('Describe how two types of white blood cell would respond.', 'Phagocytes engulf and digest pathogens; lymphocytes produce antibodies specific to the pathogen.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Describe the functions of the components of blood.', 'RBC: haemoglobin carries oxygen; phagocytes engulf pathogens; lymphocytes make antibodies; platelets help clotting (fibrinogen → fibrin); plasma transports nutrients, CO₂, urea, hormones, ions, heat.',
           'five components with correct function [5]')])
t_c9d = t
CHAPTERS[9] = [t_c9a, t_c9b, t_c9c, t_c9d]


# ===================================================================== 10 Diseases and immunity
DIS = [('cholera', 'bacterium (Vibrio cholerae)', 'contaminated drinking water and food', 'clean water supply, sewage treatment, boiling water'),
       ('tuberculosis (TB)', 'bacterium', 'droplets in the air from coughs and sneezes', 'vaccination (BCG), ventilation, isolating patients'),
       ('influenza', 'virus', 'droplets in the air from coughs and sneezes', 'vaccination, covering coughs, hand washing'),
       ('malaria', 'protoctist (Plasmodium)', 'bite of an infected female Anopheles mosquito (vector)', 'mosquito nets, draining standing water, insecticides'),
       ('HIV/AIDS', 'virus (HIV)', 'sexual contact, sharing needles, infected blood, mother to baby', 'condoms, not sharing needles, screening blood'),
       ('athlete\'s foot', 'fungus', 'direct contact with infected skin or contaminated surfaces (floors, towels)', 'not sharing towels, keeping feet dry, antifungal cream'),
       ('salmonella food poisoning', 'bacterium (Salmonella)', 'undercooked contaminated food such as chicken and eggs', 'cooking food thoroughly, avoiding cross-contamination'),
       ('measles', 'virus', 'droplets in the air', 'vaccination (MMR)')]
t = T('Pathogens, transmissible diseases and methods of transmission', 'pathogens', 'transmissible diseases', 'methods of transmission')
facts(t, [('pathogen', 'a disease-causing organism'), ('transmissible disease', 'a disease in which the pathogen can be passed from one host to another'),
          ('host', 'an organism in which a pathogen lives and reproduces'), ('vector', 'an organism, such as a mosquito, that carries a pathogen from one host to another'),
          ('direct contact', 'transmission of a pathogen through blood or other body fluids, or touching an infected person'), ('indirect contact', 'transmission of a pathogen through contaminated surfaces, food, water, animals or air')])
mcqs(t, [('Which disease is caused by a protoctist and spread by a vector?', 'Malaria', 'Plasmodium is carried by female Anopheles mosquitoes.', ['Cholera', 'Influenza', "Athlete's foot"]),
         ('Which is an example of indirect transmission of a pathogen?', 'Drinking water contaminated with faeces', 'Indirect: via contaminated water, food, surfaces, air or animals.', ['Receiving infected blood in a transfusion', 'Sexual contact', 'Mother to fetus across the placenta']),
         ('What are the four main types of pathogen?', 'Bacteria, viruses, fungi and protoctists', 'All four groups contain disease-causing species.', ['Bacteria, viruses, plants and insects', 'Viruses, worms, plants and fungi', 'Bacteria, enzymes, fungi and viruses'])])
shorts(t, [('State two ways in which pathogens can be transmitted directly.', 'Through blood (e.g. shared needles) and other body fluids (e.g. sexual contact).', '[2]'), ('State two ways in which pathogens are transmitted indirectly.', 'Contaminated food or water, surfaces, air (droplets), animals / vectors.', '[2]')])
explain(t, [('Explain why diseases spread quickly in crowded refugee camps.', 'People are close together so droplets pass easily; there may be poor sanitation and shared water supplies contaminated with faeces; poor nutrition weakens immune systems.', 'close contact / droplets [1]; poor sanitation / water [1]; weakened defences [1] [3]'),
            ('Explain why controlling mosquitoes reduces the spread of malaria.', 'The mosquito is the vector carrying Plasmodium between people; fewer mosquitoes means fewer bites from infected mosquitoes.', 'vector [1]; fewer transmissions [1] [2]'),
            ('Explain why a disease such as influenza spreads faster in winter in cold countries.', 'People spend more time indoors close together with less ventilation, so droplets from coughs and sneezes are breathed in more easily.', 'indoors / close contact [1]; droplets [1] [2]'),
            ('Explain why covering your mouth when you sneeze reduces the spread of disease.', 'It stops droplets containing pathogens being spread through the air to other people or onto surfaces.', '[2]')])
myths(t, [('All bacteria are pathogens.', 'Most bacteria are harmless or useful; only some cause disease.'), ('Malaria is caused by a mosquito.', 'Malaria is caused by the protoctist Plasmodium; the mosquito is the vector.'),
           ('Antibiotics can cure influenza.', 'Influenza is caused by a virus; antibiotics only kill bacteria.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def dis_q(r, D):
    d, path, tr, ctl = r.choice(DIS)
    if D <= 2:
        k = r.randrange(2)
        if k == 0:
            return MQ(r, f'How is {d} transmitted?', tr, [x[2] for x in DIS if x[2] != tr], f'{cap(d)}: caused by a {path}; spread by {tr}.')
        return MQ(r, f'What type of pathogen causes {d}?', path.split(' (')[0], ['bacterium', 'virus', 'fungus', 'protoctist'], f'{cap(d)}: caused by a {path}.')
    return Q(f'A health worker in {city(r)} is trying to reduce cases of {d}. (a) State the type of pathogen that causes it. (b) Describe how it is transmitted. (c) Suggest two ways to reduce its spread.',
             f'(a) {path} (b) {tr} (c) {ctl}', f'(a) {path.split(" (")[0]} [1] (b) {tr} [1] (c) two methods, e.g. {ctl} [2] [4]', 'short', 4)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def dis_growth(r, D):
    g = r.choice([20, 30])
    hrs = r.choice([2, 3, 4, 5])
    n0 = r.choice([10, 50, 100])
    n = n0 * 2 ** (hrs * 60 // g)
    st = f'Salmonella bacteria in food left at room temperature divide every {g} minutes. A piece of chicken contains {n0} bacteria. Calculate how many bacteria there will be after {hrs} hours.'
    key = f'divisions = {hrs * 60} ÷ {g} = {hrs * 60 // g} [1]; {n0} × 2^{hrs * 60 // g} = {n:,} [1]'
    ans = f'{n:,}'
    m = 2
    if D >= 4:
        st += ' Explain why food should be stored in a refrigerator and cooked thoroughly.'
        ans += '; low temperature slows bacterial enzymes and reproduction; thorough cooking kills the bacteria.'
        key += '; cold slows growth (enzymes) [1]; cooking kills bacteria / denatures their enzymes [1]'
        m = 4
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def dis_case(r, D):
    d, path, tr, ctl = r.choice([x for x in DIS if not x[0].startswith('HIV')])
    cases = [r.randrange(20, 60)]
    for _ in range(3):
        cases.append(round(cases[-1] * r.uniform(1.6, 2.4)))
    intro = f'An outbreak of {d} occurred in a district near {city(r)}. Weekly cases were: ' + ', '.join(f'week {i + 1}: {c}' for i, c in enumerate(cases)) + '.'
    parts = [lambda r: ('Calculate the percentage increase in cases from week 1 to week 4.', f'{fx(pct(cases[0], cases[-1]), 0)}%', f'({cases[-1]} − {cases[0]}) ÷ {cases[0]} × 100 [1] = {fx(pct(cases[0], cases[-1]), 0)}% [1] [2]'),
             lambda r: (f'State the type of pathogen that causes {d} and how it is transmitted.', f'{path}; {tr}', '[2]'),
             lambda r: ('Suggest and explain two measures the health authority should take.', cap(ctl) + '; each breaks the chain of transmission.', 'two measures [2]; linked to transmission route [1] [3]'),
             lambda r: ('Explain why it is important to identify the source of the outbreak.', 'So that the route of transmission can be blocked (e.g. contaminated water supply closed), preventing new infections.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


t_c10a = t

t = T('Body defences: skin, mucus, stomach acid and phagocytosis', 'body defences', 'skin, mucus, stomach acid', 'phagocytosis')
facts(t, [('phagocytosis', 'the process in which a white blood cell (phagocyte) engulfs and digests a pathogen'), ('mucus', 'a sticky substance made in the airways that traps pathogens and dust'),
          ('cilia', 'tiny hairs on cells lining the airways that sweep mucus up to the throat'), ('mechanical barrier', 'a physical barrier to pathogens, such as the skin or hairs in the nose'),
          ('chemical barrier', 'a substance that kills or traps pathogens, such as stomach acid or mucus')])
mcqs(t, [('Which is a chemical barrier to infection?', 'Hydrochloric acid in the stomach', 'Acid kills many pathogens in food; skin and nasal hairs are mechanical barriers.', ['The skin', 'Hairs in the nose', 'Blood clotting only']),
         ('What do phagocytes do?', 'Engulf and digest pathogens', 'Phagocytosis; lymphocytes produce antibodies.', ['Produce antibodies', 'Carry oxygen', 'Release fibrinogen']),
         ('How does the skin protect against pathogens?', 'It forms a tough outer barrier', 'Intact skin is a mechanical barrier.', ['It produces antibodies', 'It digests pathogens', 'It releases hydrochloric acid'])])
shorts(t, [('State two mechanical barriers to pathogens.', 'Skin; hairs in the nose.', '[2]'), ('State two chemical barriers to pathogens.', 'Mucus; stomach acid (hydrochloric acid).', '[2]')])
explain(t, [('Explain how the cells lining the trachea protect the lungs from infection.', 'Goblet cells make mucus that traps pathogens and dust; ciliated cells beat to sweep the mucus up to the throat, where it is swallowed and acid kills the pathogens.', 'mucus traps [1]; cilia move mucus away [1]; swallowed / removed [1] [3]'),
            ('Explain why smokers get more lung infections.', 'Chemicals in smoke paralyse and damage cilia, and more mucus is made, so mucus and pathogens build up in the airways.', 'cilia damaged [1]; mucus and pathogens accumulate [1] [2]'),
            ('Describe how a phagocyte destroys a bacterium.', 'It moves towards the bacterium, surrounds and engulfs it into a vacuole, and digests it with enzymes.', 'engulf [1]; digest with enzymes [1] [2]'),
            ('Explain why cuts and burns increase the risk of infection.', 'Damaged skin no longer forms a barrier, so pathogens can enter the body directly.', '[2]')])
myths(t, [('Phagocytes produce antibodies to kill bacteria.', 'Phagocytes engulf and digest pathogens; lymphocytes produce antibodies.'), ('Stomach acid digests pathogens using enzymes.', 'Stomach acid kills pathogens because of its low pH; it is not an enzyme.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def defence_q(r, D):
    ds = [('skin', 'mechanical', 'forms a tough barrier that pathogens cannot pass through'), ('hairs in the nose', 'mechanical', 'trap dust and pathogens in the air breathed in'),
          ('mucus', 'chemical', 'traps pathogens in the airways'), ('stomach acid', 'chemical', 'kills pathogens in food and drink'), ('phagocytes', 'cellular', 'engulf and digest pathogens'),
          ('lymphocytes', 'cellular', 'produce antibodies'), ('blood clotting', 'mechanical', 'seals wounds so pathogens cannot enter')]
    x, kind, how = r.choice(ds)
    if D <= 2:
        return MQ(r, f'Which type of defence is provided by {x}?', kind, ['mechanical', 'chemical', 'cellular', 'genetic'], f'{cap(x)}: {kind} defence — {how}.')
    xs = r.sample(ds, 3)
    labs = ['(i)', '(ii)', '(iii)']
    return Q('For each defence, state whether it is mechanical, chemical or cellular, and describe how it protects the body: ' + ', '.join(f'{labs[i]} {a}' for i, (a, _, _) in enumerate(xs)) + '.',
             ' '.join(f'{labs[i]} {k}: {h}' for i, (_, k, h) in enumerate(xs)), '; '.join(f'{labs[i]} {k} [1], {h} [1]' for i, (_, k, h) in enumerate(xs)) + ' [6]', 'short', 6)


@t.add('C3', (2, 3, 4), 'case')
def phago_data(r, D):
    t0 = r.choice([5, 10, 15])
    vals = [r.randrange(2, 6)]
    for _ in range(4):
        vals.append(vals[-1] + r.randrange(3, 9))
    tab = ', '.join(f'{i * t0} min: {v}' for i, v in enumerate(vals))
    st = f'Phagocytes were mixed with bacteria and the mean number of bacteria engulfed per phagocyte was counted: {tab}. (a) Calculate the mean rate of engulfing between 0 and {4 * t0} minutes, in bacteria per phagocyte per minute. (b) Describe how phagocytes destroy the bacteria they engulf.'
    rate = (vals[-1] - vals[0]) / (4 * t0)
    return Q(st, f'(a) {fx(rate, 2)} (b) engulf into a vacuole and digest with enzymes', f'(a) ({vals[-1]} − {vals[0]}) ÷ {4 * t0} = {fx(rate, 2)} [2] (b) engulf [1]; digest with enzymes [1] [4]', 'case', 4)


@t.add('C4', (3, 4, 5), 'multi_step')
def defence_case(r, D):
    intro = f'{person(r)} eats a sandwich that contains a small number of bacteria, and later breathes in air containing a virus in a crowded bus in {city(r)}.'
    parts = [lambda r: ('Explain how the body prevents the bacteria in the food from causing infection.', 'Hydrochloric acid in the stomach (pH 2) kills most bacteria before they reach the intestine.', 'acid [1]; kills bacteria [1] [2]'),
             lambda r: ('Describe how the breathing system traps and removes the virus particles.', 'Hairs in the nose filter air; mucus traps particles; cilia sweep the mucus to the throat to be swallowed.', 'mucus [1]; cilia [1] [2]'),
             lambda r: ('Explain what happens if some virus particles get past these barriers.', 'White blood cells respond: phagocytes engulf and digest pathogens and lymphocytes produce specific antibodies.', 'phagocytes [1]; lymphocytes / antibodies [1] [2]'),
             lambda r: ('Distinguish between mechanical, chemical and cellular defences, giving one example of each.', 'Mechanical: physical barrier, e.g. skin. Chemical: substance that traps/kills, e.g. stomach acid or mucus. Cellular: white blood cells, e.g. phagocytosis.', '[3]')]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t_c10b = t

t = T('Antibodies, active immunity, vaccination and passive immunity', 'antibodies', 'active immunity', 'vaccination', 'passive immunity')
facts(t, [('antibody', 'a protein that binds to a specific antigen, marking pathogens for destruction or directly neutralising them'), ('antigen', 'a molecule, usually a protein on the surface of a pathogen, that is recognised by the immune system'),
          ('active immunity', 'defence against a pathogen by antibody production in the body, after infection or vaccination'), ('passive immunity', 'short-term defence against a pathogen by antibodies acquired from another individual'),
          ('memory cell', 'a lymphocyte that remains after an immune response and produces antibodies quickly if the same antigen is met again'), ('vaccine', 'a preparation containing weakened or dead pathogens or their antigens, given to stimulate active immunity')])
mcqs(t, [('Why does a vaccine give long-term protection?', 'It causes memory cells to be made', 'Memory cells make antibodies rapidly on re-infection.', ['It contains antibodies from another person', 'It kills all pathogens in the body', 'It makes the skin thicker']),
         ('A baby receives antibodies in breast milk. What type of immunity is this?', 'Passive immunity', 'Antibodies come from another individual; no memory cells are made.', ['Active immunity', 'Natural vaccination', 'Herd immunity']),
         ('Why does each antibody only act against one type of pathogen?', 'Its shape is complementary to one specific antigen', 'Antibody–antigen binding is specific.', ['It only lives for one day', 'Pathogens all have the same antigens', 'It is made by phagocytes'])])
shorts(t, [('State two ways in which antibodies help to destroy pathogens.', 'Mark pathogens for destruction by phagocytes; neutralise toxins / stop pathogens entering cells; clump pathogens together.', '[2]'), ('Give two ways of acquiring passive immunity.', 'Antibodies across the placenta; antibodies in breast milk; antibody injection (e.g. antivenom).', '[2]')])
explain(t, [('Explain why passive immunity is only short-term.', 'Antibodies received are broken down over time and no memory cells are made, so the body cannot make more antibodies.', 'antibodies broken down [1]; no memory cells [1] [2]'),
            ('Explain how vaccination programmes can protect people who have not been vaccinated.', 'If most of the population is immune (herd immunity), the pathogen cannot spread easily, so unvaccinated people are less likely to meet it.', 'most people immune [1]; pathogen spread reduced [1] [2]'),
            ('Explain why a second infection by the same pathogen usually produces no symptoms.', 'Memory cells make large amounts of specific antibodies very quickly (secondary response), destroying the pathogen before it can reproduce enough to cause symptoms.', 'memory cells [1]; faster, greater antibody production [1]; before symptoms [1] [3]'),
            ('Explain why a new influenza vaccine is needed every year.', 'Influenza viruses mutate and change their antigens; antibodies and memory cells from last year no longer fit the new antigens.', 'antigens change [1]; old antibodies not complementary [1] [2]')])
myths(t, [('Vaccines contain antibodies that fight the disease.', 'Vaccines contain antigens (weakened/dead pathogens) that stimulate the body to make its own antibodies and memory cells.'),
           ('Passive immunity lasts for life because memory cells are passed on.', 'Passive immunity is short-term: antibodies are received but no memory cells are made.')])


@t.add('C3', (1, 2, 3, 4, 5), 'case')
def ab_resp(r, D):
    d1 = r.choice([10, 12, 14])
    peak1 = r.choice([20, 30, 40])
    f = r.choice([5, 8, 10, 12])
    d2 = r.choice([3, 4, 5])
    peak2 = peak1 * f
    if D == 1:
        return MQ(r, f'After a first vaccination, antibody concentration peaks at {peak1} units after {d1} days. After a booster, it peaks at {peak2} units after {d2} days. Why is the second response faster and larger?', 'Memory cells were made after the first vaccination',
                  ['The booster contained antibodies', 'Phagocytes made the antibodies', 'The pathogen had died', 'Platelets were activated'], 'Secondary response: memory cells produce antibodies quickly.')
    st = (f'A person was vaccinated on day 0 and given a booster dose of the same vaccine on day 30. After the first dose the antibody concentration peaked at {peak1} arbitrary units on day {d1}. '
          f'After the booster it peaked at {peak2} units on day {30 + d2}. (a) Calculate how many times greater the peak was after the booster. (b) Explain the difference between the two responses.')
    ans = f'(a) {f} times (b) The first dose produced memory cells; on the second exposure these produced antibodies faster and in greater amounts (secondary response).'
    key = f'(a) {peak2} ÷ {peak1} = {f} [1] (b) memory cells made after first dose [1]; faster / larger secondary response [1]'
    m = 3
    if D >= 4:
        st += ' (c) Explain why this is described as active immunity.'
        ans += ' (c) The person\'s own lymphocytes produced the antibodies and memory cells.'
        key += ' (c) own body makes antibodies [1]'
        m = 4
    if D >= 5:
        st += ' (d) Calculate the percentage decrease in time taken to reach the peak.'
        ans += f' (d) {fx((d1 - d2) / d1 * 100, 1)}%'
        key += f' (d) ({d1} − {d2}) ÷ {d1} × 100 = {fx((d1 - d2) / d1 * 100, 1)}% [1]'
        m = 5
    return Q(st, ans, key + f' [{m}]', 'case', m)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def herd(r, D):
    pop = r.choice([12000, 25000, 48000, 80000, 150000])
    pc = r.choice([60, 72, 85, 90, 95])
    need = r.choice([90, 95]) if pc < 90 else r.choice([80, 85])
    vacc = pop * pc / 100
    st = f'A town of {pop:,} people has a vaccination coverage of {pc}% for measles. (a) Calculate the number of people vaccinated. (b) Herd immunity needs {need}% coverage. State whether the town has herd immunity and calculate how many more people (if any) need to be vaccinated.'
    more = max(0, pop * need / 100 - vacc)
    ans = f'(a) {int(vacc):,} (b) ' + ('Yes — no more needed.' if more == 0 else f'No — {int(more):,} more people.')
    key = f'(a) {pop:,} × {pc} ÷ 100 = {int(vacc):,} [1] (b) ' + ('coverage ≥ target, herd immunity [1]' if more == 0 else f'{pop:,} × {need} ÷ 100 = {int(pop * need / 100):,}; − {int(vacc):,} = {int(more):,} [2]')
    m = 2 if more == 0 else 3
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def vacc_case(r, D):
    dz = r.choice(['measles', 'polio', 'tetanus', 'diphtheria', 'COVID-19'])
    intro = f'A health department in {city(r)} is running a vaccination programme against {dz}.'
    parts = [lambda r: ('Describe how a vaccine leads to immunity.', 'Vaccine contains weakened / dead pathogens or antigens; lymphocytes recognise antigens and produce specific antibodies; memory cells are made, giving long-term protection.', 'antigens [1]; lymphocytes / antibodies [1]; memory cells [1] [3]'),
             lambda r: ('Explain why a booster dose is often given.', 'It produces a larger secondary response, increasing the number of memory cells and antibodies so protection lasts longer.', '[2]'),
             lambda r: ('Explain why it is important to vaccinate a large proportion of the population.', 'Herd immunity: the pathogen cannot spread, protecting people who cannot be vaccinated (e.g. babies, people with weak immune systems).', '[2]'),
             lambda r: ('Compare active and passive immunity.', 'Active: own antibodies, memory cells, long-lasting, slower to develop. Passive: antibodies from another source, immediate, short-term, no memory cells.', 'two comparisons [2]'),
             lambda r: ('Suggest why some people are given an injection of antibodies rather than a vaccine after possible exposure (for example to tetanus).', 'Antibodies act immediately, whereas a vaccine takes days to produce antibodies, which may be too slow.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


longs(t, [('Explain how the body develops active immunity after infection or vaccination, and why passive immunity is different.', 'Antigens recognised; lymphocytes produce specific antibodies with complementary shape; antibodies mark/neutralise pathogens; memory cells remain; faster secondary response. Passive: antibodies acquired (placenta, breast milk), immediate, no memory cells, short-lived.',
           'antigen / specificity [1]; lymphocytes antibodies [1]; memory cells [1]; secondary response [1]; passive described [1]; contrast [1] [6]')])
t_c10c = t

t = T('Controlling the spread of disease: hygiene, sanitation and food safety; cholera', 'controlling the spread of disease', 'hygiene, sanitation and food safety', 'cholera')
facts(t, [('sanitation', 'the safe disposal of human waste (sewage) and provision of clean water'), ('cholera', 'a disease caused by the bacterium Vibrio cholerae, spread by contaminated water, causing severe diarrhoea'),
          ('oral rehydration therapy', 'a drink of water containing salts and glucose, given to replace water and ions lost in diarrhoea'), ('food hygiene', 'practices such as hand washing and correct cooking and storage that prevent food becoming contaminated'),
          ('toxin', 'a poisonous substance produced by some pathogens')])
mcqs(t, [('How does the cholera toxin cause diarrhoea?', 'It causes chloride ions to be secreted into the small intestine, so water follows by osmosis', 'Lower water potential in the gut draws water out of the blood.', ['It destroys red blood cells', 'It blocks the oesophagus', 'It stops bile production']),
         ('Which measure most reduces the spread of cholera?', 'Treating sewage and providing clean drinking water', 'Cholera spreads through water contaminated with faeces.', ['Wearing face masks', 'Killing mosquitoes', 'Washing clothes in cold water']),
         ('Why should raw meat be stored below cooked food in a fridge?', 'To stop juices containing pathogens dripping onto cooked food', 'Prevents cross-contamination.', ['To keep the meat colder', 'To stop the cooked food freezing', 'To save space'])])
shorts(t, [('State three ways of preventing the spread of disease through food.', 'Wash hands; cook food thoroughly; store food in a refrigerator; keep raw and cooked food separate; keep flies off food.', 'any three [3]'), ('State two ways in which waste disposal reduces disease.', 'Removes breeding sites / food for flies and rats (vectors); prevents contamination of water supplies.', '[2]')])
explain(t, [('Explain how cholera causes dehydration.', 'The toxin causes chloride ions to be secreted into the small intestine; this lowers the water potential of gut contents, so water moves out of the blood by osmosis and is lost in watery diarrhoea.', 'chloride ions secreted [1]; water potential lowered [1]; water leaves by osmosis [1]; diarrhoea [1] [4]'),
            ('Explain why oral rehydration therapy is effective for cholera patients.', 'It replaces the water and ions lost in diarrhoea; glucose helps the intestine absorb sodium ions and water.', 'replaces water and ions [1]; glucose aids absorption [1] [2]'),
            ('Explain why proper sewage treatment reduces the number of cases of cholera.', 'Faeces of infected people contain Vibrio bacteria; treatment kills them and stops them contaminating drinking water.', 'faeces contain bacteria [1]; prevents contamination of water [1] [2]'),
            ('Explain why hand washing after using the toilet reduces the spread of disease.', 'It removes pathogens from faeces on the hands, so they are not transferred to food or other people.', '[2]')])
myths(t, [('Cholera is spread by mosquitoes.', 'Cholera is spread by water or food contaminated with faeces containing Vibrio cholerae.'), ('Antibiotics are always needed to treat cholera.', 'The most important treatment is rehydration with water, salts and glucose; antibiotics may help in severe cases.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def cholera_data(r, D):
    before = r.randrange(800, 3000)
    after = round(before * r.uniform(0.05, 0.35))
    yr = r.choice([2010, 2012, 2015, 2018])
    if D == 1:
        pc = (before - after) / before * 100
        return NQ(r, f'Cholera cases in a district fell from {before} to {after} after a clean water supply was installed. What is the percentage decrease?', pc, [after / before * 100, (before - after) / after * 100, pc / 10, 100 - pc / 2], '%', f'({before} − {after}) ÷ {before} × 100 = {fx(pc, 1)}%.', f=lambda v: fx(v, 1))
    st = f'In a district near {city(r)}, there were {before} cases of cholera in {yr}. After a new water treatment plant and sewers were built, there were {after} cases in {yr + 3}. Calculate the percentage decrease in cases.'
    pc = (before - after) / before * 100
    key = f'({before} − {after}) ÷ {before} × 100 [1] = {fx(pc, 1)}% [1]'
    ans = f'{fx(pc, 1)}%'
    m = 2
    if D >= 3:
        st += ' Explain why the new water treatment plant reduced the number of cases.'
        ans += '; treatment kills Vibrio cholerae and sewers stop faeces contaminating drinking water.'
        key += '; kills bacteria / separates sewage from drinking water [1]'
        m = 3
    if D >= 5:
        st += ' Suggest one reason why some cases still occurred.'
        ans += ' Some people may still drink untreated water or eat contaminated food (or catch it while travelling).'
        key += '; valid reason [1]'
        m = 4
    return Q(st, ans, key + f' [{m}]', 'numerical', m)


@t.add('C4', (3, 4, 5), 'multi_step')
def cholera_case(r, D):
    intro = f'After a flood in a region near {city(r)}, many people developed severe watery diarrhoea. Tests showed the bacterium Vibrio cholerae.'
    parts = [lambda r: ('Explain why cholera outbreaks often follow floods.', 'Flood water mixes sewage with drinking water supplies, spreading the bacteria from faeces.', 'sewage contaminates water [1]; bacteria from faeces [1] [2]'),
             lambda r: ('Explain how the cholera toxin leads to loss of water from the body.', 'Toxin causes chloride ions to be secreted into the gut, lowering water potential; water moves from blood into the gut by osmosis; lost as diarrhoea.', 'chloride secretion [1]; osmosis [1]; diarrhoea / dehydration [1] [3]'),
             lambda r: ('Suggest two immediate actions that aid agencies should take.', 'Provide clean drinking water (or purification tablets / boiling); provide oral rehydration solution; build temporary latrines; health education on hand washing.', 'any two [2]'),
             lambda r: ('Explain why washing hands with soap reduces the spread of cholera.', 'Removes bacteria from faeces on hands so they are not transferred to food or water.', '[2]')]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


longs(t, [('Describe how hygiene, sanitation, food safety and waste disposal reduce the spread of transmissible diseases.', 'Personal hygiene (hand washing) removes pathogens; sanitation (sewage treatment, clean water) prevents water-borne diseases such as cholera; food hygiene (cooking, refrigeration, separating raw and cooked) prevents food poisoning; waste disposal removes vectors such as flies and rats.',
           'hygiene [1]; sanitation [1]; food safety [1]; waste disposal [1]; named example [1] [5]')])
t_c10d = t
CHAPTERS[10] = [t_c10a, t_c10b, t_c10c, t_c10d]
