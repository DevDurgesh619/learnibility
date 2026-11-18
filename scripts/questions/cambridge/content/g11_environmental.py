"""Cambridge International AS Level Environmental Management 8291 (grade 11, AS only).

Chapters follow the CUP coursebook order: lithosphere, hydrosphere, atmosphere, biosphere, human
population, natural resources (energy, water, food), environmental management and sustainability,
and research skills.

Paper 1 / Paper 2 styles: short knowledge items, structured questions built on data and resources
(tables described in words, with every computed value worked out in code), named case studies with
real places, evaluation questions and essays marked with levels, and research-skills items
(hypotheses, variables, random / systematic / stratified sampling, quadrats and transects,
Lincoln index, Simpson's index of diversity and Spearman's rank correlation with critical values).

Knowledge packs follow the g9/g10 geography builders; numerical templates are written here.
"""
import math
import re
from ._lib import topic, mcq, compose, person, two_people, city, sf, fmt

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}
MINUS = '−'


# ============================================================== helpers

def cap(s):
    return s[:1].upper() + s[1:]


def T(name, *extra):
    return topic(name, name.lower(), *extra)


def f1(x):
    """One decimal place, unicode minus."""
    v = round(x + 0.0, 1)
    s = f'{abs(v):.1f}'
    return (MINUS if v < 0 and s != '0.0' else '') + s


def f2(x):
    v = round(x + 0.0, 2)
    s = f'{abs(v):.2f}'
    return (MINUS if v < 0 and s != '0.00' else '') + s


def s3(x):
    """3 significant figures, unicode minus."""
    if abs(x) < 1e-12:
        return '0'
    return (MINUS if x < 0 else '') + sf(abs(x), 3)


def nf(x):
    """Integer with a space as thousands separator (Cambridge style)."""
    x = int(round(x))
    s = f'{abs(x):,}'.replace(',', ' ')
    return (MINUS if x < 0 else '') + s


def pc(a, b):
    return (b - a) / a * 100


def MCQ(r, stem, ans, ds, key):
    out = []
    for d in ds:
        if d != ans and d not in out:
            out.append(d)
    if len(out) < 3:
        return None
    opts, a = mcq(r, ans, out)
    return {'stem': stem, 'options': opts, 'answer': a, 'key': key}


def L(text, ans, key):
    return lambda r: (text, ans, key)


def comp(r, intro, parts, D, type_='numerical'):
    k = (1, 2) if D <= 1 else (2, 3) if D <= 3 else (3, 4)
    return compose(r, intro, parts, k=k, type_=type_)


_MK = re.compile(r'\[(\d+)\]')


def _marks(key):
    m = _MK.findall(key)
    return int(m[-1]) if m else None


# ---------------------------------------------------------------- knowledge packs

def add_terms(t, terms):
    if len(terms) < 4:
        return
    n = len(terms)
    t.fixed('C1', (1, 2), [(f'Which term matches this definition: “{d}”?', cap(term), f'{cap(term)}: {d}. [1]',
                            [cap(x) for x, _ in terms if x != term]) for term, d in terms])
    t.fixed('C1', (2, 3), [(f'What is meant by the term “{term}”?', cap(d) + '.', f'{cap(term)}: {d}. [1]',
                            [cap(terms[(i + k) % n][1]) + '.' for k in (1, 2, 3)]) for i, (term, d) in enumerate(terms)])
    t.fixed('C1', (1, 2, 3), [(f'Define the term {term}.', cap(d) + '.', f'1 mark for an accurate definition: {d}. [1]')
                              for term, d in terms], type='short')


def add_mcqs(t, entries):
    for stem, ans, ds, key in entries:
        def fn(r, D_, stem=stem, ans=ans, ds=ds, key=key):
            return MCQ(r, stem, ans, list(ds), key)
        fn.__name__ = 'mcq'
        t.add('C1', (1, 2, 3), 'mcq')(fn)


CLAIM_LEADS = ['A student writes:', 'In a class discussion, a student says:', 'A news article states:', 'A classmate claims:',
               'A student’s examination answer states:', 'A poster in a school corridor says:']


def add_claims(t, claims):
    ents = []
    for i, (c, ok, why) in enumerate(claims):
        lead = CLAIM_LEADS[i % len(CLAIM_LEADS)]
        ents.append((f'{lead} “{c}” Is this statement correct? Explain your answer.', ('Correct. ' if ok else 'Not correct. ') + why,
                     '1 mark correct judgement; 1 mark accurate explanation [2]'))
    t.fixed('C2', (1, 2, 3), ents, type='explain')


LEVELS = {
    6: ('Level 3 (5-6 marks): well-developed points on both sides with examples and a supported conclusion. Level 2 (3-4 marks): some '
        'developed points, limited balance or example. Level 1 (1-2 marks): simple statements. [6]'),
    8: ('Level 3 (6-8 marks): detailed, balanced discussion using named examples and data, with a reasoned judgement. Level 2 (3-5 marks): '
        'developed points but limited balance or exemplification. Level 1 (1-2 marks): simple, generalised points. [8]'),
    12: ('Level 4 (10-12 marks): detailed, balanced evaluation supported by named examples and a clear, justified conclusion. Level 3 (7-9 marks): '
         'developed discussion with examples, judgement partly supported. Level 2 (4-6 marks): some relevant points, mostly descriptive. '
         'Level 1 (1-3 marks): simple, unsupported statements. [12]'),
    20: ('Level 4 (16-20 marks): comprehensive, well-structured essay; detailed knowledge of named examples; sustained evaluation and a '
         'well-supported conclusion. Level 3 (11-15 marks): good knowledge and examples, some evaluation, conclusion partly supported. '
         'Level 2 (6-10 marks): relevant but mainly descriptive, limited examples or one-sided. Level 1 (1-5 marks): a few simple, '
         'generalised points with little or no evaluation. [20]'),
}
ESSAY_LEADS = [
    lambda c, p: f'“{cap(c)}.” To what extent do you agree with this statement? Refer to examples you have studied.',
    lambda c, p: f'Evaluate the view that {c}.',
    lambda c, p: f'{p} argues that {c}. Discuss this view, referring to named examples.',
    lambda c, p: f'To what extent is it true that {c}?',
    lambda c, p: f'“{cap(c)}.” Discuss.',
    lambda c, p: f'Assess the extent to which {c}. Support your answer with examples.',
]


def add_essay(t, claim, pro, con, judge, hints=()):
    def fn(r, D):
        p = person(r)
        mk = {2: 6, 3: 8, 4: 12, 5: 20}.get(D, 8)
        if D <= 2:
            stem = f'Discuss whether {claim}. Give arguments for and against.'
        else:
            stem = r.choice(ESSAY_LEADS)(claim, p)
            if hints and r.random() < 0.6:
                hs = r.sample(list(hints), min(len(hints), r.choice([2, 3])))
                stem += ' In your answer you should consider: ' + '; '.join(hs) + '.'
        ans = 'For: ' + ' '.join(pro) + ' Against: ' + ' '.join(con) + ' Judgement: ' + judge
        return {'stem': stem, 'answer': ans, 'key': 'Indicative content as in the model answer. ' + LEVELS[mk], 'type': 'long', 'marks': mk}
    fn.__name__ = 'essay'
    t.add('C4', (2, 3, 4, 5), 'long')(fn)


CS_LEADS = [
    lambda k, n, p: f'For a named example of {k} that you have studied, {p}.',
    lambda k, n, p: f'Using a case study of {k}, such as {n}, {p}.',
    lambda k, n, p: f'With reference to {n}, or another example of {k}, {p}.',
    lambda k, n, p: f'Name an example of {k}. For your chosen example, {p}.',
]


def add_cs(t, kind, cases, prompts):
    """cases: [(name, {aspect: model answer})]; prompts: [(prompt, aspect, indicative content)]."""
    def c4(r, D):
        name, facts = r.choice(cases)
        ok = [p for p in prompts if p[1] in facts]
        if not ok:
            return None
        pr, asp, ind = r.choice(ok)
        stem = r.choice(CS_LEADS)(kind, name, pr)
        mk = 6 if D <= 3 else 8
        key = (f'Indicative content: {ind} ' + LEVELS[mk].replace('named examples', 'place-specific detail from the named example'))
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
                         f'Refer to your case study of {kind} (for example {name}). Briefly {pr}.',
                         f'For {name} or another example of {kind}, briefly {pr}.'])
        return {'stem': lead, 'answer': f'{name}: {facts[asp]}', 'key': '1 mark named, located example; up to 3 marks for accurate, place-specific points. ' + ind + ' [4]',
                'type': 'case', 'marks': 4}
    c3.__name__ = 'cs3'
    t.add('C3', (2, 3, 4), 'case')(c3)


HILLS = ['the Ethiopian Highlands', 'northern Thailand', 'the Andes of Peru', 'Rwanda', 'the middle hills of Nepal', 'the Cordillera of the Philippines', 'the Western Ghats of India']
MANGROVES = ['Indonesia', 'the Sundarbans of Bangladesh', 'northern Australia', 'coastal Kenya', 'southern Florida', 'the Philippines', 'Vietnam’s Mekong Delta']
RIVER_CITIES = ['Hanoi', 'Dhaka', 'Bangkok', 'Jakarta', 'Manila', 'Kuala Lumpur', 'Bogotá', 'Seoul', 'Cairo', 'Lagos']


def add_case(t, intros, parts, C3=(2, 3, 4, 5), C4=(3, 4, 5)):
    plist = [(lambda r, p=p: p) for p in parts]

    def mk(k):
        def fn(r, D):
            intro = r.choice(intros)
            if '{' in intro:
                intro = intro.format(p=person(r), c=city(r), h=r.choice(HILLS), m=r.choice(MANGROVES), f=r.choice(RIVER_CITIES))
            return compose(r, intro, plist, k=k, type_='case')
        fn.__name__ = 'case'
        return fn
    if C3:
        t.add('C3', C3, 'case')(mk((2, 3)))
    if C4:
        t.add('C4', C4, 'case')(mk((3, 4)))


def _markify(t, start):
    for tpl in t.templates[start:]:
        if tpl.name != 'fixed':
            continue

        def fn(r, D, f=tpl.fn):
            q = f(r, D)
            if q and 'marks' not in q:
                m = _marks(q['key'])
                if m:
                    q['marks'] = m
            return q
        tpl.fn = fn


def build(t, P):
    start = len(t.templates)
    add_terms(t, P.get('terms', []))
    if P.get('mcq'):
        add_mcqs(t, P['mcq'])
    if P.get('explain'):
        t.fixed('C2', (2, 3, 4), P['explain'], type='explain')
    if P.get('claims'):
        add_claims(t, P['claims'])
    for c in P.get('cases', []):
        add_case(t, *c)
    for cs in P.get('cs', []):
        add_cs(t, *cs)
    for e in P.get('essays', []):
        add_essay(t, *e)
    _markify(t, start)
    return t


def compare_item(t, pairs, D=(2, 3, 4)):
    """C2 'compare X and Y' items: pairs [(x, y, difference text, similarity text)]."""
    def fn(r, D_):
        x, y, diff, sim = r.choice(pairs)
        if r.random() < 0.5:
            x, y = y, x
        if D_ <= 2:
            return {'stem': f'State one difference between {x} and {y}.', 'answer': diff, 'key': '1 mark for a clear comparative difference [1]', 'type': 'explain', 'marks': 1}
        lead = r.choice(['Compare', 'Explain the differences between', 'Outline one similarity and two differences between'])
        return {'stem': f'{lead} {x} and {y}.', 'answer': f'Differences: {diff} Similarity: {sim}', 'key': '1 mark similarity; 1 mark per comparative difference up to 2 [3]', 'type': 'explain', 'marks': 3}
    fn.__name__ = 'compare'
    t.add('C2', D, 'explain')(fn)


# ============================================================== CHAPTER 1: Lithosphere

l1 = T('Structure of the Earth and plate tectonics: plate boundaries and their landforms', 'plate tectonics', 'plate boundaries')
build(l1, {
    'terms': [
        ('crust', 'the thin, rigid outer layer of the Earth, 5-10 km thick under oceans and up to about 70 km under continents'),
        ('lithosphere', 'the rigid outer shell of the Earth made of the crust and the uppermost mantle, broken into tectonic plates'),
        ('asthenosphere', 'the partly molten, plastic layer of the upper mantle on which the lithospheric plates move'),
        ('convection current', 'the circulation of heated mantle rock that rises, spreads and sinks, helping to move the plates'),
        ('subduction', 'the process in which a denser oceanic plate sinks beneath another plate into the mantle at a destructive boundary'),
        ('sea-floor spreading', 'the formation of new oceanic crust as magma rises at a mid-ocean ridge and the plates move apart'),
        ('ridge push', 'the force produced as newly formed, raised lithosphere at a mid-ocean ridge slides away from the ridge'),
        ('slab pull', 'the force produced as the cold, dense edge of a subducting plate sinks and drags the rest of the plate with it'),
    ],
    'mcq': [
        ('At which type of plate boundary is the Mid-Atlantic Ridge found?', 'Constructive (divergent)', ['Destructive (convergent)', 'Conservative (transform)', 'Collision'], 'Plates move apart and new crust forms. [1]'),
        ('Which landform is formed where an oceanic plate is subducted beneath a continental plate?', 'An ocean trench and fold mountains with volcanoes', ['A mid-ocean ridge', 'A rift valley only', 'A hotspot island chain'], 'E.g. Peru-Chile Trench and the Andes. [1]'),
        ('The San Andreas Fault in California is an example of which boundary?', 'Conservative', ['Constructive', 'Destructive', 'Collision'], 'Pacific and North American plates slide past each other. [1]'),
        ('Why does oceanic crust subduct beneath continental crust?', 'Oceanic crust is denser', ['Oceanic crust is thicker', 'Continental crust is hotter', 'Continental crust is younger'], 'Basaltic oceanic crust (about 3.0 g/cm³) is denser than granitic continental crust (about 2.7 g/cm³). [1]'),
        ('Which range of mountains was formed by the collision of two continental plates?', 'The Himalayas', ['The Andes', 'The Mid-Atlantic Ridge', 'The Hawaiian Islands'], 'Indian and Eurasian plates. [1]'),
        ('Which layer of the Earth is liquid?', 'The outer core', ['The inner core', 'The lower mantle', 'The crust'], 'The outer core is liquid iron and nickel; the inner core is solid because of the pressure. [1]'),
    ],
    'explain': [
        ('Explain how a mid-ocean ridge is formed.', 'Plates move apart at a constructive boundary; pressure is reduced so the mantle partially melts; magma rises and cools to form new basaltic crust; hot, buoyant crust is raised to form a ridge.', 'plates diverge [1]; magma rises and solidifies [1]; new crust uplifted into a ridge [1] [3]'),
        ('Explain why volcanoes form at destructive plate boundaries.', 'The subducting oceanic plate is heated and releases water, which lowers the melting point of the mantle above; magma forms, rises through the overlying plate and erupts.', 'subduction [1]; melting / water lowers melting point [1]; magma rises to the surface [1] [3]'),
        ('Explain why there are no volcanoes at a collision boundary between two continental plates.', 'Neither plate is dense enough to be subducted, so no plate sinks into the mantle to melt; instead the crust is crumpled and pushed up into fold mountains.', 'both continental / similar low density [1]; no subduction so no magma [1] [2]'),
        ('Describe the evidence that the continents have moved.', 'Jigsaw fit of South America and Africa; matching rock types and fossils (e.g. Mesosaurus) on separate continents; glacial deposits in now-tropical areas; palaeomagnetic striping on the ocean floor, which is symmetrical about ridges.', '1 mark per piece of evidence up to [3]'),
        ('Explain how convection currents in the mantle may cause plate movement.', 'Heat from the core warms mantle rock, which becomes less dense and rises; it spreads out beneath the lithosphere, cools and sinks; the moving mantle drags the plates above it.', 'heating and rising [1]; lateral flow and sinking [1]; drag on the plates [1] [3]'),
    ],
    'claims': [
        ('Earthquakes only happen at destructive plate boundaries.', False, 'Earthquakes occur at all boundaries, including constructive and conservative ones (e.g. the San Andreas Fault); intraplate earthquakes also occur.'),
        ('Oceanic crust is younger than most continental crust.', True, 'Oceanic crust is recycled by subduction and is rarely older than about 200 million years, while continental crust can be over 4 billion years old.'),
        ('Hotspot volcanoes such as Hawaii are found at plate boundaries.', False, 'Hawaii lies in the middle of the Pacific plate above a mantle plume; the plate moves over the fixed hotspot to form a chain of islands.'),
        ('The plates move at a few centimetres per year.', True, 'Typical rates are 2-10 cm per year, similar to the rate at which fingernails grow.'),
    ],
    'cases': [(
        ['Fig. 1.1 is a cross-section across the west coast of South America, showing the Nazca plate moving east towards the South American plate, an ocean trench, and the Andes mountains with volcanoes.',
         'A student in {c} is studying a cross-section of a destructive plate boundary where oceanic crust meets continental crust, such as the boundary off Chile.'],
        [('Name the type of plate boundary shown.', 'Destructive (convergent, subduction) boundary.', '[1]'),
         ('Explain why an ocean trench forms at this boundary.', 'The denser oceanic plate bends down and sinks beneath the continental plate, creating a deep trench where it descends.', 'denser oceanic plate [1]; sinks / subducts, forming trench [1] [2]'),
         ('Explain the formation of the volcanoes.', 'The subducted plate is heated at depth and releases water; mantle melts; magma rises through the continental crust and erupts.', 'heat / water release [1]; melting [1]; magma rises [1] [3]'),
         ('Suggest why earthquakes here occur at a range of depths.', 'Friction between the plates causes earthquakes along the sloping subducting slab (Benioff zone), shallow near the trench and deeper inland.', 'friction / stress along slab [1]; slab slopes so foci get deeper inland [1] [2]'),
         ('Describe how the mountains were formed.', 'Compression as the plates converge folds and thickens the continental crust, and volcanic material adds to it, forming fold mountains.', 'compression / folding [1]; thickening and volcanic addition [1] [2]')])],
    'essays': [
        ('the movement of tectonic plates is mainly caused by convection currents in the mantle',
         ['Convection in the mantle transfers heat from the core and was the first explanation of plate motion; rising limbs coincide with ridges and sinking limbs with subduction zones.'],
         ['Slab pull at subduction zones is now thought to be the strongest force (plates with long subducting edges, such as the Pacific plate, move fastest); ridge push also contributes.'],
         'Convection supplies the heat, but slab pull and ridge push are probably the main direct drivers of plate movement.',
         ['convection', 'slab pull', 'ridge push', 'evidence from plate speeds']),
    ],
})
compare_item(l1, [
    ('oceanic crust', 'continental crust', 'Oceanic crust is thinner (5-10 km), denser (basaltic) and younger; continental crust is thicker (up to 70 km), less dense (granitic) and much older.', 'Both are part of the lithosphere and rest on the mantle.'),
    ('a constructive boundary', 'a destructive boundary', 'At a constructive boundary plates move apart and new crust forms; at a destructive boundary plates converge and crust is destroyed by subduction.', 'Both have volcanoes and earthquakes.'),
    ('a destructive boundary', 'a conservative boundary', 'Destructive boundaries have subduction and volcanoes; at conservative boundaries plates slide past each other with no volcanoes and crust is neither created nor destroyed.', 'Both have earthquakes, which can be powerful.'),
])

SPREAD = [('the Mid-Atlantic Ridge', 2.5), ('the East Pacific Rise', 14.0), ('the Mid-Atlantic Ridge near Iceland', 2.0), ('the Southeast Indian Ridge', 7.0), ('the Gakkel Ridge in the Arctic', 1.0)]


@l1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l1_rate(r, D):
    ridge, rate = r.choice(SPREAD)
    age = r.choice([2, 4, 5, 8, 10, 12, 15, 20, 25, 30])
    rate = round(rate * r.uniform(0.8, 1.2), 1)
    km = rate * age * 1e6 / 1e5        # cm/yr * yr -> cm -> km
    km = round(km)
    rate_exact = km * 1e5 / (age * 1e6)
    intro = f'Rock samples were collected from the ocean floor on one side of {ridge}. Basalt {nf(km)} km from the ridge axis has an age of {age} million years.'
    if D == 1:
        return MCQ(r, intro + ' What is the average rate at which this side of the plate has moved away from the ridge?', f'{f1(rate_exact)} cm per year',
                   [f'{f1(rate_exact * 10)} cm per year', f'{f1(rate_exact / 10)} cm per year', f'{f1(km / age)} cm per year', f'{f1(rate_exact * 2)} cm per year'],
                   f'{nf(km)} km = {nf(km * 1e5)} cm; ÷ {age} 000 000 years = {f1(rate_exact)} cm per year. [1]')
    full = rate_exact * 2
    yrs = r.choice([1000, 10000, 100000])
    parts = [
        L('Calculate the average rate of plate movement in cm per year. Show your working.', f'{f1(rate_exact)} cm per year',
          f'{nf(km)} × 100 000 = {nf(km * 1e5)} cm [1]; ÷ {nf(age * 1e6)} = {f1(rate_exact)} cm per year [1] [2]'),
        L('Assuming the other plate moves away at the same rate, calculate the total spreading rate across the ridge.', f'{f1(full)} cm per year', f'2 × {f1(rate_exact)} = {f1(full)} [1]'),
        L(f'Calculate how far apart, in metres, the two plates would move in {nf(yrs)} years at this total rate.', f'{s3(full * yrs / 100)} m', f'{f1(full)} × {nf(yrs)} ÷ 100 = {s3(full * yrs / 100)} m [1]'),
        L('Describe how the age of the ocean floor changes with distance from the ridge and explain why.', 'The ocean floor gets older with distance from the ridge, symmetrically on both sides, because new crust forms at the ridge and is carried away as the plates diverge.', 'older with distance [1]; new crust forms at ridge and moves outward [1] [2]'),
        L('Suggest one reason why the calculated rate is only an estimate.', 'The rate may not have been constant over time; dating and distance measurements have errors; only one sample was used.', '[1]'),
    ]
    return comp(r, intro, parts, D)


@l1.add('C2', (1, 2, 3), 'short')
def l1_identify(r, D):
    feats = [('a deep ocean trench next to a chain of explosive volcanoes on land', 'destructive (oceanic-continental)', 'the Peru-Chile Trench and the Andes'),
             ('a chain of volcanic islands in an arc beside a deep trench', 'destructive (oceanic-oceanic)', 'the Mariana Islands and Mariana Trench'),
             ('a rift valley with gentle eruptions of runny basaltic lava', 'constructive', 'the East African Rift Valley or Iceland'),
             ('a long submarine mountain range with a central rift and frequent shallow earthquakes', 'constructive', 'the Mid-Atlantic Ridge'),
             ('very high fold mountains with frequent earthquakes but no active volcanoes', 'collision', 'the Himalayas'),
             ('a long fault where frequent shallow earthquakes occur but there are no volcanoes', 'conservative', 'the San Andreas Fault'),
             ('a line of volcanic islands far from any plate boundary, getting older in one direction', 'none (hotspot)', 'the Hawaiian Islands')]
    f, b, eg = r.choice(feats)
    if D == 1:
        return MCQ(r, f'An area has {f}. Which type of plate setting is this?', cap(b), [cap(x[1]) for x in feats if x[1] != b], f'{cap(b)}, e.g. {eg}. [1]')
    return {'stem': f'An area has {f}. Identify the type of plate boundary or setting and name a real example. Give a reason for your identification.',
            'answer': f'{cap(b)}; e.g. {eg}. The landforms described are typical of this setting.', 'key': '1 mark type; 1 mark named example; 1 mark reason linked to the features [3]', 'type': 'explain', 'marks': 3}


l2 = T('The rock cycle: formation of igneous, sedimentary and metamorphic rocks', 'rock cycle', 'igneous', 'sedimentary', 'metamorphic')
build(l2, {
    'terms': [
        ('igneous rock', 'rock formed when molten magma or lava cools and crystallises'),
        ('sedimentary rock', 'rock formed from sediments that are deposited in layers, compacted and cemented'),
        ('metamorphic rock', 'rock formed when existing rock is changed by heat and/or pressure without melting'),
        ('weathering', 'the breakdown of rocks in situ by physical, chemical or biological processes'),
        ('erosion', 'the wearing away and removal of rock material by agents such as rivers, ice, wind and waves'),
        ('lithification', 'the process by which loose sediment is compacted and cemented into solid rock'),
        ('intrusive igneous rock', 'igneous rock that cools slowly underground, forming large crystals, such as granite'),
        ('extrusive igneous rock', 'igneous rock that cools quickly at the surface, forming small crystals, such as basalt'),
    ],
    'mcq': [
        ('Which rock is metamorphic?', 'Marble', ['Granite', 'Limestone', 'Sandstone'], 'Marble forms from limestone by heat and pressure. [1]'),
        ('Granite has large crystals because it', 'cooled slowly deep underground', ['cooled quickly at the surface', 'was formed from sediments', 'was changed by pressure'], 'Slow cooling allows large crystals to grow. [1]'),
        ('Which rock is most likely to contain fossils?', 'Limestone', ['Basalt', 'Granite', 'Slate'], 'Fossils are preserved in sedimentary rocks. [1]'),
        ('Slate is formed by the metamorphism of', 'shale (mudstone)', ['limestone', 'sandstone', 'granite'], 'Regional metamorphism of shale gives slate. [1]'),
        ('Which process changes sediment into sedimentary rock?', 'Compaction and cementation', ['Melting and cooling', 'Heat and pressure', 'Weathering and erosion'], 'Lithification. [1]'),
        ('Quartzite is the metamorphic form of', 'sandstone', ['shale', 'limestone', 'basalt'], '[1]'),
    ],
    'explain': [
        ('Explain why the rock cycle is described as a cycle.', 'Rocks are continually changed from one type to another: igneous rocks are weathered into sediments that form sedimentary rocks, which may be metamorphosed or melted to form magma and new igneous rock; there is no start or end.', 'changes between types [1]; named linking processes [1]; continuous / no start or end [1] [3]'),
        ('Describe how a sedimentary rock such as sandstone forms.', 'Rock is weathered and eroded; sediment is transported and deposited in layers (e.g. in seas); the weight of overlying layers compacts it; minerals in water cement the grains together.', 'weathering and erosion [1]; deposition in layers [1]; compaction and cementation [1] [3]'),
        ('Explain the difference in crystal size between basalt and granite.', 'Basalt is extrusive and cools quickly at the surface so crystals have little time to grow; granite is intrusive and cools slowly deep underground, forming large crystals.', 'basalt fast cooling small crystals [1]; granite slow cooling large crystals [1] [2]'),
        ('Explain how metamorphic rocks form at a destructive plate boundary.', 'Intense pressure from plate convergence and heat from nearby magma alter existing rocks without melting them, recrystallising minerals (regional and contact metamorphism).', 'pressure from convergence [1]; heat from magma [1]; recrystallisation without melting [1] [3]'),
        ('Explain why some rocks are more resistant to weathering than others.', 'Hard crystalline rocks such as granite have interlocking crystals and few pores, while sedimentary rocks such as chalk are porous, softer or soluble in weak acid, so they weather faster.', 'interlocking crystals / hardness [1]; porosity or solubility [1] [2]'),
    ],
    'claims': [
        ('Metamorphic rocks form when rocks melt and cool.', False, 'Melting and cooling forms igneous rock; metamorphic rock is changed by heat and pressure without melting.'),
        ('Limestone can be formed from the shells of marine organisms.', True, 'Calcium carbonate shells accumulate on the sea bed and are compacted and cemented into limestone.'),
        ('Igneous rocks usually contain fossils.', False, 'Organisms are destroyed by the high temperature of magma; fossils are found in sedimentary rocks.'),
    ],
    'cases': [(
        ['A geology student in {c} collected three rock samples. Sample A has large interlocking crystals of quartz, feldspar and mica. Sample B is made of rounded sand grains in layers and contains a fossil shell. Sample C has very fine grains and splits into thin flat sheets.',
         '{p} examined three rocks during fieldwork: rock A (coarse crystals, no layers), rock B (layered grains with fossils) and rock C (fine-grained, splits into flat sheets).'],
        [('Identify the type of rock for each sample.', 'A igneous (intrusive, e.g. granite); B sedimentary (e.g. sandstone or limestone); C metamorphic (e.g. slate).', '1 mark each [3]'),
         ('Explain how the large crystals in sample A formed.', 'Magma cooled slowly underground, giving time for large crystals to grow.', 'slow cooling [1]; underground / intrusive [1] [2]'),
         ('Explain why sample B contains fossils.', 'It formed from sediment deposited in layers, which buried organisms; low temperatures preserved their remains, which were lithified with the sediment.', 'deposition burying organisms [1]; no melting / preserved [1] [2]'),
         ('Describe how sample C could have formed from a sedimentary rock.', 'Shale or mudstone was subjected to high pressure (and heat), e.g. at a plate boundary; minerals realigned in parallel, so it splits into sheets (slate).', 'pressure / heat [1]; realignment / cleavage [1] [2]'),
         ('Suggest how sample A might eventually become part of a sedimentary rock.', 'It is uplifted and exposed, weathered and eroded; the sediment is transported, deposited, compacted and cemented.', '1 mark per stage up to [3]')])],
    'essays': [
        ('the rock cycle is mainly driven by plate tectonics',
         ['Plate movements cause melting at subduction zones (igneous rock), metamorphism under pressure at boundaries, and uplift of rocks so they can be weathered.'],
         ['Weathering, erosion and deposition at the surface are driven by solar energy through the water cycle and climate; sedimentary rocks form without plate activity.'],
         'Both internal (tectonic) and external (solar-driven) energy drive the cycle; plate tectonics dominate the deep processes and surface processes dominate the formation of sediments.',
         ['internal energy', 'solar energy', 'weathering and erosion']),
    ],
})
compare_item(l2, [
    ('granite', 'basalt', 'Granite is intrusive with large crystals and is pale and silica-rich; basalt is extrusive with small crystals and is dark and iron-rich.', 'Both are igneous rocks made of interlocking crystals.'),
    ('physical weathering', 'chemical weathering', 'Physical weathering breaks rock into smaller pieces without changing its minerals (e.g. freeze-thaw); chemical weathering changes the minerals (e.g. carbonation of limestone).', 'Both break down rock in situ.'),
    ('contact metamorphism', 'regional metamorphism', 'Contact metamorphism is caused mainly by heat near an intrusion over a small area; regional metamorphism is caused by heat and pressure over large areas at plate boundaries.', 'Both change rock without melting it.'),
])


@l2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l2_cool(r, D):
    """Crystal size data from a dyke or lava flow."""
    rock = r.choice(['a basalt dyke', 'a dolerite sill', 'a thick lava flow'])
    w = r.choice([4, 5, 6, 8, 10])
    dists = [0, w / 4, w / 2]
    base = r.choice([0.1, 0.2, 0.3])
    sizes = [base, round(base * r.uniform(3, 5), 1), round(base * r.uniform(8, 12), 1)]
    intro = (f'A student measured mean crystal size across {rock} {w} m wide. At the edge (0 m) the mean crystal size was {sizes[0]} mm, at {fmt(dists[1], 1)} m it was '
             f'{sizes[1]} mm and at the centre ({fmt(dists[2], 1)} m) it was {sizes[2]} mm.')
    ratio = sizes[2] / sizes[0]
    if D == 1:
        return MCQ(r, intro + ' How many times larger are the crystals at the centre than at the edge?', s3(ratio), [s3(ratio * 2), s3(sizes[2] - sizes[0]), s3(ratio / 2), s3(sizes[1] / sizes[0])],
                   f'{sizes[2]} ÷ {sizes[0]} = {s3(ratio)}. [1]')
    parts = [
        L('Describe the pattern in crystal size.', f'Crystal size increases from the edge ({sizes[0]} mm) to the centre ({sizes[2]} mm).', 'pattern [1]; data quoted [1] [2]'),
        L('Calculate how many times larger the crystals at the centre are than at the edge.', s3(ratio), f'{sizes[2]} ÷ {sizes[0]} = {s3(ratio)} [1]'),
        L('Explain the pattern.', 'Magma at the edge was in contact with cold surrounding rock and cooled quickly, so crystals had little time to grow; the centre was insulated and cooled slowly, forming larger crystals.', 'fast cooling at edge [1]; slow cooling at centre [1]; time for growth [1] [3]'),
        L('Suggest how the student could make the crystal measurements more reliable.', 'Measure several crystals at each distance (e.g. 10) with a hand lens and scale and calculate a mean; repeat along several lines across the intrusion.', 'repeats / mean [1]; more sample lines [1] [2]'),
        L('Suggest what would happen to rocks immediately next to the intrusion.', 'They would be baked by the heat and undergo contact metamorphism, e.g. shale to hornfels or limestone to marble.', 'contact metamorphism [1]; example [1] [2]'),
    ]
    return comp(r, intro, parts, D)


l3 = T('Natural hazards: earthquakes, volcanoes and tsunamis, their impacts and management', 'natural hazards', 'earthquakes', 'volcanoes', 'tsunamis')
build(l3, {
    'terms': [
        ('natural hazard', 'a natural event that threatens people, property or the environment'),
        ('focus (hypocentre)', 'the point underground where an earthquake originates'),
        ('epicentre', 'the point on the Earth’s surface directly above the focus of an earthquake'),
        ('tsunami', 'a series of long-wavelength sea waves caused by the sudden displacement of a large volume of water, often by a sea-floor earthquake'),
        ('pyroclastic flow', 'a fast-moving, very hot cloud of ash, gas and rock fragments that flows down the side of a volcano'),
        ('lahar', 'a volcanic mudflow of ash and water that travels down river valleys'),
        ('liquefaction', 'the process in which shaking makes saturated soil behave like a liquid, so buildings sink or tilt'),
        ('vulnerability', 'the degree to which people or property are likely to be harmed by a hazard'),
    ],
    'mcq': [
        ('The moment magnitude scale is logarithmic. An earthquake of magnitude 7 has ground shaking (amplitude) how many times greater than one of magnitude 5?', '100 times', ['2 times', '20 times', '1000 times'], '10² = 100. [1]'),
        ('Which hazard killed most of the people who died in the 2011 Tōhoku earthquake in Japan?', 'The tsunami', ['Collapsing buildings', 'Fires', 'Landslides'], 'Over 90% of the about 18 000 deaths were by drowning. [1]'),
        ('Which is an example of a method of preparing for an earthquake?', 'Holding regular earthquake drills', ['Building sea walls only after the event', 'Spraying lava with sea water', 'Digging diversion channels for lava'], '[1]'),
        ('Which type of volcano is formed by viscous, silica-rich lava and has explosive eruptions?', 'Composite (strato) volcano', ['Shield volcano', 'Fissure volcano', 'Basalt plateau'], 'E.g. Mount St Helens, Mount Pinatubo. [1]'),
        ('Which hazard is a volcanic mudflow?', 'Lahar', ['Pyroclastic flow', 'Tephra', 'Nuée ardente'], 'E.g. Nevado del Ruiz 1985 (Armero). [1]'),
        ('Which feature reduces earthquake damage to tall buildings?', 'Rubber shock absorbers in the foundations (base isolation)', ['Heavy concrete roofs', 'Unreinforced brick walls', 'Large glass windows'], '[1]'),
    ],
    'explain': [
        ('Explain why earthquakes of similar magnitude often cause more deaths in low-income countries than in high-income countries.', 'Buildings are often poorly constructed and not earthquake-resistant; emergency services and hospitals are less well equipped; there is less preparation and education; dense informal settlements; slower aid and reconstruction.', '1 mark per developed reason up to [3]'),
        ('Explain how a sea-floor earthquake can cause a tsunami.', 'Sudden vertical movement of the sea bed along a fault (often at a subduction zone) displaces the overlying water column; the energy travels outwards as long-wavelength waves that slow and grow in height in shallow water near the coast.', 'vertical displacement of sea bed [1]; water displaced [1]; waves increase in height in shallow water [1] [3]'),
        ('Explain why people continue to live near active volcanoes.', 'Fertile volcanic soils for farming; geothermal energy; tourism; minerals; eruptions are infrequent and people may perceive the risk as low or have no alternative.', '1 mark per reason up to [3]'),
        ('Describe how volcanic eruptions can be predicted.', 'Monitoring small earthquakes (seismometers), ground deformation (tiltmeters, GPS, satellite radar), increased gas emissions such as sulfur dioxide, and rising ground temperature.', '1 mark per method up to [3]'),
        ('Explain the role of a tsunami early warning system.', 'Seismometers and ocean buoys (e.g. DART) detect earthquakes and changes in sea level; warnings are sent quickly to coastal areas so people can evacuate to higher ground before waves arrive.', 'detection [1]; communication [1]; evacuation time [1] [3]'),
    ],
    'claims': [
        ('The magnitude of an earthquake is the only factor that determines how many people die.', False, 'Population density, building quality, time of day, depth of focus, preparation and secondary hazards (tsunami, landslides) are also important.'),
        ('Volcanic eruptions can have benefits as well as costs.', True, 'They produce fertile soils, geothermal energy, building materials and tourism.'),
        ('Earthquakes can now be predicted accurately to the day.', False, 'Scientists can identify high-risk zones and probabilities, but not the exact time of an earthquake.'),
        ('The 2004 Indian Ocean tsunami killed people in countries thousands of kilometres from the epicentre.', True, 'Waves reached Sri Lanka, India, Thailand and even Somalia; the lack of a warning system increased deaths.'),
    ],
    'cs': [('an earthquake or tsunami', [
        ('the 2011 Tōhoku earthquake and tsunami, Japan', {
            'causes': 'A magnitude 9.0-9.1 earthquake on the subduction zone where the Pacific plate is subducted beneath the plate carrying northern Japan; the sea bed rose several metres and displaced the sea, causing a tsunami up to about 40 m high.',
            'impacts': 'About 18 000 deaths, mostly drowning; about 120 000 buildings destroyed; the Fukushima Daiichi nuclear power station was flooded, causing meltdowns and the evacuation of over 150 000 people; economic cost about US$235 billion.',
            'management': 'Strict building codes meant few buildings collapsed from shaking; an early-warning system gave minutes of warning; drills saved many lives; but sea walls were overtopped, so later responses included higher sea walls and relocating homes to higher ground.'}),
        ('the 2015 Gorkha earthquake, Nepal', {
            'causes': 'A magnitude 7.8 earthquake caused by the Indian plate colliding with and moving under the Eurasian plate along the Himalayan thrust.',
            'impacts': 'About 9000 deaths and 22 000 injuries; around 600 000 homes destroyed; avalanches on Everest and landslides blocked roads; damage to historic buildings in Kathmandu; losses equal to about a third of GDP.',
            'management': 'International aid and search-and-rescue teams; reconstruction slowed by poor access and governance; programmes to train builders in earthquake-resistant designs.'}),
        ('the 2004 Indian Ocean tsunami', {
            'causes': 'A magnitude 9.1 earthquake off Sumatra where the Indian plate subducts beneath the Burma plate, raising the sea bed along a 1300 km rupture.',
            'impacts': 'About 230 000 deaths in 14 countries, including Indonesia (Aceh), Sri Lanka, India and Thailand; coastal villages, mangroves and coral reefs damaged; drinking water contaminated by salt.',
            'management': 'No warning system existed in the Indian Ocean; afterwards the Indian Ocean Tsunami Warning System was set up (2006), with evacuation routes, education and mangrove replanting as natural defences.'}),
    ], [
        ('describe the causes of the event', 'causes', 'plate setting; magnitude; mechanism (sea-floor uplift, collision)'),
        ('describe the social, economic and environmental impacts', 'impacts', 'deaths and injuries; damage; economic cost; environmental damage, with figures'),
        ('evaluate the effectiveness of the management of the hazard', 'management', 'preparation, prediction / warning, building design, response; judgement on effectiveness'),
    ])],
    'essays': [
        ('the impacts of earthquakes depend more on the level of development of a country than on the magnitude of the earthquake',
         ['Haiti 2010 (magnitude 7.0) killed over 200 000 people because of poor buildings and weak services, while Christchurch 2011 (6.2) killed 185.'],
         ['Magnitude, depth and secondary hazards matter: Tōhoku 2011 (9.0) killed about 18 000 people in a high-income country because of the tsunami.'],
         'Development strongly affects vulnerability and recovery, but very large events or tsunamis can overwhelm even well-prepared countries.',
         ['magnitude and depth', 'building standards', 'preparation and response', 'secondary hazards']),
        ('it is more effective to prepare for volcanic eruptions than to respond after them',
         ['Monitoring at Mount Pinatubo (1991) allowed evacuation of about 60 000 people and saved thousands of lives; hazard maps and land-use zoning reduce exposure.'],
         ['Prediction is uncertain and costly; evacuations disrupt lives (Montserrat 1995-97); response, aid and recovery are still essential after any eruption.'],
         'Preparation reduces loss of life most cost-effectively, but must be combined with an effective response and recovery plan.',
         ['monitoring', 'evacuation', 'cost', 'named volcanoes']),
    ],
})
compare_item(l3, [
    ('a shield volcano', 'a composite volcano', 'Shield volcanoes have gentle slopes and effusive eruptions of runny basaltic lava; composite volcanoes are steep-sided with explosive eruptions of viscous andesitic lava, ash and pyroclastic flows.', 'Both are formed by the eruption of magma from the mantle.'),
    ('a primary hazard', 'a secondary hazard', 'A primary hazard is caused directly by the event (ground shaking, lava); a secondary hazard results from it (tsunami, fire, landslide, disease).', 'Both can cause deaths and damage.'),
])

QUAKES = [('Haiti, 2010', 7.0, 'about 220 000'), ('Christchurch, New Zealand, 2011', 6.2, '185'), ('Tōhoku, Japan, 2011', 9.1, 'about 18 000'),
          ('Gorkha, Nepal, 2015', 7.8, 'about 9000'), ('Kahramanmaraş, Türkiye, 2023', 7.8, 'over 50 000'), ('Chile (Maule), 2010', 8.8, 'about 525'),
          ('Sichuan, China, 2008', 7.9, 'about 87 000'), ('Kashmir, Pakistan, 2005', 7.6, 'about 86 000'), ('Loma Prieta, USA, 1989', 6.9, '63')]


@l3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l3_mag(r, D):
    (a, ma, da), (b, mb, db) = r.sample(QUAKES, 2)
    if ma == mb:
        return None
    if ma < mb:
        a, ma, da, b, mb, db = b, mb, db, a, ma, da
    dm = round(ma - mb, 1)
    amp = 10 ** dm
    en = 10 ** (1.5 * dm)
    intro = f'The {a} earthquake had a moment magnitude of {ma} and the {b} earthquake had a magnitude of {mb}. Deaths: {a} {da}; {b} {db}.'
    if D == 1:
        return MCQ(r, intro + ' Each whole step on the magnitude scale is a 10-fold increase in ground shaking. How many times greater was the shaking in the larger earthquake?', s3(amp),
                   [s3(dm * 10), s3(amp * 10), s3(dm), s3(en)], f'10^{fmt(dm, 1)} = {s3(amp)}. [1]')
    parts = [
        L('Each whole step on the magnitude scale is a 10-fold increase in the amplitude of ground shaking. Calculate how many times greater the shaking was in the larger earthquake.', s3(amp), f'10^{fmt(dm, 1)} [1] = {s3(amp)} [1] [2]'),
        L('Each whole step releases about 32 times more energy (energy ∝ 10^(1.5M)). Calculate how many times more energy the larger earthquake released.', s3(en), f'10^(1.5 × {fmt(dm, 1)}) [1] = {s3(en)} [1] [2]'),
        L('Suggest reasons why the number of deaths does not simply depend on magnitude.', 'Building quality and codes; population density; depth of focus and distance from cities; time of day; secondary hazards such as tsunamis and landslides; preparedness and emergency response.', '1 mark per reason up to [3]'),
        L('Explain why a logarithmic scale is used to measure earthquake magnitude.', 'Earthquake sizes vary over many orders of magnitude, so a logarithmic scale compresses the range into manageable numbers.', 'wide range of sizes [1]; compresses scale [1] [2]'),
    ]
    return comp(r, intro, parts, D)


@l3.add('C3', (2, 3, 4, 5), 'numerical')
def l3_tsunami(r, D):
    depth = r.choice([2000, 3000, 4000, 5000])
    dist = r.choice([300, 500, 800, 1200, 1600, 2000])
    v = math.sqrt(9.8 * depth)   # m/s
    t_min = dist * 1000 / v / 60
    loc = r.choice(['Banda Aceh', 'Galle in Sri Lanka', 'Phuket in Thailand', 'Sendai in Japan', 'Hilo in Hawaii', 'Valparaíso in Chile'])
    intro = (f'Tsunami waves travel at a speed given by v = √(g × d), where g = 9.8 m/s² and d is the ocean depth in metres. A tsunami crosses ocean of average depth {nf(depth)} m '
             f'towards {loc}, {nf(dist)} km from the epicentre.')
    parts = [
        L('Calculate the speed of the waves in m/s and in km/h.', f'{s3(v)} m/s = {s3(v * 3.6)} km/h', f'√(9.8 × {depth}) = {s3(v)} m/s [1]; × 3.6 = {s3(v * 3.6)} km/h [1] [2]'),
        L(f'Calculate the time, in minutes, for the waves to reach {loc}.', f'{s3(t_min)} minutes', f'{nf(dist * 1000)} ÷ {s3(v)} [1] = {s3(t_min)} minutes [1] [2]'),
        L('Explain why the waves increase in height as they approach the coast.', 'In shallow water the waves slow down, so the wavelength shortens and the water piles up, increasing wave height.', 'slow down in shallow water [1]; energy concentrated / height increases [1] [2]'),
        L('Use your answer to explain the importance of an early warning system.', f'There are only about {s3(t_min)} minutes before the waves arrive, so rapid detection and communication are needed for people to evacuate to higher ground.', 'uses time [1]; evacuation linked [1] [2]'),
    ]
    return comp(r, intro, parts, D)


l4 = T('Soils: formation, composition, degradation and conservation', 'soils', 'soil degradation', 'soil conservation')
build(l4, {
    'terms': [
        ('soil', 'the loose upper layer of the Earth’s surface made of mineral particles, organic matter, water and air, in which plants grow'),
        ('humus', 'dark, decomposed organic matter in soil that holds water and nutrients'),
        ('soil horizon', 'a distinct layer in a soil profile, such as the O, A, B and C horizons'),
        ('leaching', 'the removal of soluble minerals and nutrients from the upper soil by water moving downwards'),
        ('salinisation', 'the build-up of salts in the upper soil, often as irrigation water evaporates in hot, dry climates'),
        ('soil erosion', 'the removal of topsoil by wind or water faster than it is formed'),
        ('contour ploughing', 'ploughing across a slope following the contours, so furrows slow runoff and reduce erosion'),
        ('terracing', 'cutting flat steps into a hillside to reduce slope length and gradient and so reduce soil erosion'),
    ],
    'mcq': [
        ('Which soil particle has the smallest size?', 'Clay', ['Silt', 'Sand', 'Gravel'], 'Clay < 0.002 mm, silt 0.002-0.05 mm, sand 0.05-2 mm. [1]'),
        ('A loam soil is best described as', 'a mixture of sand, silt and clay with organic matter', ['mostly clay', 'mostly sand', 'pure humus'], '[1]'),
        ('Which is a cause of salinisation?', 'Irrigation in a hot climate with poor drainage', ['Contour ploughing', 'Planting shelter belts', 'Adding organic matter'], '[1]'),
        ('Which method is used to reduce wind erosion of soil?', 'Planting shelter belts of trees', ['Overgrazing', 'Leaving fields bare after harvest', 'Ploughing up and down slopes'], '[1]'),
        ('The 1930s Dust Bowl in the USA was mainly caused by', 'ploughing the prairie grassland followed by severe drought', ['flooding of the Mississippi', 'volcanic ash', 'acid rain'], '[1]'),
        ('Which soil type drains most freely?', 'Sandy soil', ['Clay soil', 'Peat soil', 'Silty clay soil'], 'Large pores between sand grains. [1]'),
    ],
    'explain': [
        ('Explain how climate affects soil formation.', 'Temperature and rainfall control the rate of weathering and decomposition; high rainfall causes leaching; in hot, wet climates chemical weathering is rapid but nutrients are leached; in cold climates decomposition is slow so organic matter accumulates.', '1 mark per developed point up to [3]'),
        ('Explain why clay soils are often waterlogged.', 'Clay particles are tiny and pack closely, so pore spaces are very small; water drains slowly and air is excluded.', 'small particles / small pores [1]; slow drainage [1] [2]'),
        ('Explain how overgrazing leads to soil erosion.', 'Animals remove the vegetation cover and trample the soil; roots no longer bind the soil and the bare surface is exposed to wind and rain, so topsoil is removed.', 'loss of vegetation [1]; roots no longer bind / compaction [1]; exposure to wind and rain [1] [3]'),
        ('Explain why organic matter is important for soil fertility.', 'Humus releases nutrients as it decomposes, holds water and nutrients, improves soil structure and aeration, and supports soil organisms.', '1 mark per point up to [3]'),
        ('Describe how terracing reduces soil erosion on steep slopes.', 'Terraces break the slope into flat steps, reducing the gradient and length of slope, so runoff is slowed and water infiltrates, and soil is trapped behind terrace walls.', 'reduces gradient [1]; slows runoff / increases infiltration [1]; traps soil [1] [3]'),
    ],
    'claims': [
        ('Soil is a renewable resource that forms quickly.', False, 'Soil forms very slowly (often about 1 cm in 100-1000 years), so on human timescales it is effectively non-renewable.'),
        ('Removing vegetation increases the risk of soil erosion.', True, 'Plant cover intercepts rain and roots bind the soil; without it soil is exposed to wind and rain splash.'),
        ('Adding more irrigation water always improves crop yields.', False, 'Over-irrigation can cause waterlogging and salinisation, reducing yields.'),
    ],
    'cases': [(
        ['Fig. 1.4 shows a hillside farm in {h} where the soil has been eroded. Gullies have formed on the bare slopes and the river below has become muddy.',
         'A farming cooperative on steep hillsides has seen crop yields fall by a third in ten years because of soil erosion after forest clearance.'],
        [('Describe the evidence of soil erosion.', 'Gullies on the slopes, bare ground, muddy (high sediment) river, and falling crop yields.', '1 mark per piece of evidence up to [2]'),
         ('Explain how the removal of forest increased soil erosion.', 'Less interception so rain hits the ground directly (rain splash); fewer roots to bind the soil; more surface runoff on bare, compacted ground.', '1 mark per point up to [3]'),
         ('Suggest two methods of soil conservation suitable for this farm and explain how each works.', 'Terracing reduces slope gradient and runoff; contour ploughing / bunds slow water; agroforestry or cover crops protect the surface and bind soil.', '1 mark per method; 1 mark per explanation [4]'),
         ('Explain why soil erosion is a problem for people living downstream.', 'Sediment fills rivers and reservoirs, increasing flood risk and reducing water storage; it can damage fisheries and water quality.', '1 mark per point up to [2]'),
         ('Suggest why some farmers may not adopt soil conservation methods.', 'High labour or capital cost; lack of knowledge; insecure land tenure; benefits take years to appear.', '1 mark per point up to [2]')])],
    'cs': [('soil degradation and its management', [
        ('the Loess Plateau, China', {
            'causes': 'Centuries of deforestation, overgrazing and cultivation of steep slopes of fine, wind-blown loess soil led to extreme gully erosion; the Yellow River carried more sediment than almost any river in the world.',
            'management': 'The Loess Plateau Watershed Rehabilitation Project (from 1994, with the World Bank) built terraces, banned free grazing, planted trees and grasses on steep slopes and built check dams; incomes doubled for over 2.5 million people and sediment loads fell sharply.'}),
        ('the Sahel, West Africa', {
            'causes': 'Rapid population growth, overgrazing, removal of trees for fuelwood and cultivation of marginal land, combined with droughts in the 1970s-80s, caused desertification.',
            'management': 'Farmer-managed natural regeneration in Niger re-greened about 5 million hectares; stone lines (bunds) and zaï planting pits in Burkina Faso trap water and soil; the Great Green Wall initiative.'}),
    ], [
        ('explain the causes of soil degradation', 'causes', 'human and physical causes; processes of erosion'),
        ('evaluate the success of the strategies used to conserve the soil', 'management', 'named methods, outcomes with data, limitations, judgement'),
    ])],
    'essays': [
        ('soil degradation is caused more by human activities than by natural processes',
         ['Deforestation, overgrazing, poor irrigation (salinisation in the Aral Sea basin) and intensive ploughing (US Dust Bowl) greatly increase erosion rates.'],
         ['Drought, intense rainfall, steep slopes and wind are natural causes; climate change makes these more severe.'],
         'Natural factors set the conditions, but human land use usually triggers and accelerates degradation.',
         ['deforestation', 'farming methods', 'climate']),
    ],
})
compare_item(l4, [
    ('sandy soil', 'clay soil', 'Sandy soils have large particles and pores, drain quickly and are easy to work but nutrient-poor; clay soils have tiny particles, hold water and nutrients but are poorly aerated and easily waterlogged.', 'Both are made of mineral particles from weathered rock.'),
    ('wind erosion', 'water erosion', 'Wind erosion removes fine, dry soil from flat, bare land in dry areas; water erosion by rain splash, sheet wash and gullies is greatest on slopes during heavy rain.', 'Both remove fertile topsoil and are made worse by loss of vegetation.'),
])


@l4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l4_texture(r, D):
    m = r.choice([50, 80, 100, 120, 200])
    sand = r.randint(20, 60)
    clay = r.randint(8, 40)
    silt = 100 - sand - clay
    if silt < 5:
        return None
    ms = [round(m * x / 100, 1) for x in (sand, silt, clay)]
    tot = sum(ms)
    ps = [x / tot * 100 for x in ms]
    site = r.choice(['a field in ' + city(r), 'a forest plot', 'a river terrace', 'a school garden'])
    if ps[2] >= 35:
        cls = 'clay'
    elif ps[0] >= 50 and ps[2] < 20:
        cls = 'sandy loam'
    else:
        cls = 'loam (or clay loam)'
    intro = f'A soil sample from {site} was separated by sieving and sedimentation into sand {ms[0]} g, silt {ms[1]} g and clay {ms[2]} g.'
    if D == 1:
        return MCQ(r, intro + ' What percentage of the sample is clay?', f'{f1(ps[2])}%', [f'{f1(ps[0])}%', f'{f1(ps[1])}%', f'{f1(ms[2])}%', f'{f1(100 - ps[2])}%'], f'{ms[2]} ÷ {fmt(tot, 1)} × 100 = {f1(ps[2])}%. [1]')
    dry = round(r.uniform(40, 60), 1)
    ign = round(dry * (1 - r.uniform(0.04, 0.15)), 1)
    om = (dry - ign) / dry * 100
    parts = [
        L('Calculate the percentage of sand, silt and clay in the sample.', f'sand {f1(ps[0])}%, silt {f1(ps[1])}%, clay {f1(ps[2])}%', f'each mass ÷ {fmt(tot, 1)} × 100 [1]; all three correct [1] [2]'),
        L('Use a soil texture triangle (or your percentages) to suggest the soil texture class.', cap(cls), '[1]'),
        L(f'A {dry} g sample of dry soil was heated strongly and its mass fell to {ign} g. Calculate the percentage organic matter.', f'{f1(om)}%', f'({dry} − {ign}) ÷ {dry} × 100 [1] = {f1(om)}% [1] [2]'),
        L('Explain how the texture of this soil will affect its drainage and fertility.', ('A high clay content gives small pores: slow drainage, risk of waterlogging, but good nutrient retention.' if ps[2] >= 35 else
                                                                                          'A high sand content gives large pores: rapid drainage, low water and nutrient retention, so it may need organic matter added.' if ps[0] >= 50 else
                                                                                          'A balanced mixture gives good drainage and aeration while holding water and nutrients, so it is fertile.'), 'drainage linked to particle / pore size [1]; fertility linked [1] [2]'),
        L('Explain why the soil must be dried before it is weighed.', 'Water adds mass that varies between samples, so drying to constant mass makes results comparable.', '[1]'),
    ]
    return comp(r, intro, parts, D)


@l4.add('C3', (2, 3, 4, 5), 'numerical')
def l4_erosion(r, D):
    area = r.choice([2, 5, 10, 25, 50])
    loss = r.choice([8, 12, 15, 20, 30, 40])
    form = r.choice([0.5, 1.0])
    bd = 1.3  # t per m³
    depth_mm = loss / (bd * 10000) * 1000   # t/ha/yr -> m -> mm
    years_25 = 25 / depth_mm
    red = r.choice([50, 60, 70, 80])
    intro = (f'Measurements on a {area} ha sloping farm show soil loss of {loss} tonnes per hectare per year. Soil forms at about {form} tonnes per hectare per year. '
             f'The soil has a bulk density of 1.3 t/m³ (1 ha = 10 000 m²).')
    parts = [
        L('Calculate the total soil lost from the farm each year.', f'{nf(area * loss)} tonnes', f'{area} × {loss} = {nf(area * loss)} t [1]'),
        L('Calculate how many times faster soil is lost than it forms.', s3(loss / form), f'{loss} ÷ {form} = {s3(loss / form)} [1]'),
        L('Calculate the depth of soil, in mm, lost each year.', f'{s3(depth_mm)} mm', f'volume per ha = {loss} ÷ 1.3 = {s3(loss / bd)} m³ [1]; ÷ 10 000 m² × 1000 = {s3(depth_mm)} mm [1] [2]'),
        L('Estimate how many years it would take to lose a 25 cm (250 mm) layer of topsoil at this rate.', f'{s3(250 / depth_mm)} years', f'250 ÷ {s3(depth_mm)} = {s3(250 / depth_mm)} years [1]'),
        L(f'Contour ploughing and cover crops could reduce the loss by {red}%. Calculate the new rate of soil loss and state whether it would be sustainable.',
          f'{s3(loss * (1 - red / 100))} t/ha/yr; ' + ('sustainable, as it is no more than the rate of formation.' if loss * (1 - red / 100) <= form else 'still not sustainable, as it exceeds the rate of formation.'),
          f'{loss} × {1 - red / 100:.2f} = {s3(loss * (1 - red / 100))} [1]; comparison with {form} [1] [2]'),
    ]
    return comp(r, intro, parts, D)


l5 = T('Mineral extraction: mining methods, environmental impacts and restoration', 'mineral extraction', 'mining methods', 'restoration')
build(l5, {
    'terms': [
        ('ore', 'a rock containing enough of a mineral to make extraction economically worthwhile'),
        ('ore grade', 'the concentration of the useful mineral or metal in an ore, often given as a percentage'),
        ('open-pit mining', 'surface mining in which overburden is removed and ore is dug from a large, deep pit'),
        ('strip mining', 'surface mining in which long strips of overburden are removed to reach shallow, horizontal deposits such as coal'),
        ('overburden', 'the soil and rock lying above a mineral deposit that must be removed to reach it'),
        ('spoil heap', 'a pile of waste rock and overburden removed during mining'),
        ('tailings', 'the fine waste material left after the valuable mineral has been extracted from crushed ore'),
        ('acid mine drainage', 'acidic water containing dissolved metals that forms when sulfide minerals in mine waste react with air and water'),
    ],
    'mcq': [
        ('Which mining method would be used for a deep, narrow vein of gold?', 'Deep (shaft) mining', ['Strip mining', 'Open-pit mining', 'Dredging'], 'Deep, narrow deposits are mined underground. [1]'),
        ('Acid mine drainage forms when', 'sulfide minerals in exposed rock react with air and water', ['limestone is quarried', 'tailings are stored under water', 'land is reforested'], 'Oxidation of pyrite produces sulfuric acid. [1]'),
        ('Which is a method of restoring a former open-pit mine?', 'Filling with water to create a lake and planting vegetation around it', ['Increasing the size of spoil heaps', 'Releasing tailings into rivers', 'Leaving the land bare'], '[1]'),
        ('The Ok Tedi mine in Papua New Guinea is known for', 'polluting the Ok Tedi and Fly rivers with tailings', ['restoring rainforest', 'being an underground salt mine', 'having no environmental impacts'], '[1]'),
        ('Why is an ore with a low grade more environmentally damaging per tonne of metal produced?', 'More rock must be mined and processed, producing more waste', ['It contains more metal', 'It is always deeper', 'It needs no processing'], '[1]'),
    ],
    'explain': [
        ('Explain the factors that affect whether a mineral deposit is mined.', 'Ore grade and size of deposit; depth and accessibility; market price and demand; extraction and transport costs; technology; environmental regulations and political stability.', '1 mark per factor with brief explanation up to [3]'),
        ('Explain how mining can pollute water.', 'Acid mine drainage releases sulfuric acid and dissolved heavy metals; tailings dams can leak or collapse; sediment from bare land increases turbidity; chemicals such as cyanide or mercury used in processing can enter rivers.', '1 mark per point up to [3]'),
        ('Describe the stages in restoring land after open-pit mining.', 'Reshape spoil and fill the pit; replace stored topsoil; treat contaminated water; add fertiliser or lime; replant native species; monitor recovery over years.', '1 mark per stage up to [3]'),
        ('Explain why the environmental impacts of mining may continue after a mine closes.', 'Acid drainage and heavy metal leaching from spoil and tailings can continue for decades; unstable spoil heaps and tailings dams may fail; habitats take a long time to recover.', '1 mark per point up to [2]'),
    ],
    'claims': [
        ('Open-pit mining produces less waste rock than underground mining.', False, 'Open-pit mining must remove large amounts of overburden, so it usually produces much more waste rock.'),
        ('Mining can bring economic benefits to a region.', True, 'It creates jobs, tax revenue and export earnings, and can lead to new infrastructure such as roads.'),
        ('The 2019 Brumadinho tailings dam collapse in Brazil shows that mining waste can be a hazard to people.', True, 'The collapse released a mudflow of tailings that killed about 270 people and polluted the Paraopeba River.'),
    ],
    'cases': [(
        ['A company plans an open-pit copper mine in a forested valley near {c}. The ore grade is low and the processing plant will produce large volumes of tailings.',
         'Fig. 1.5 shows land use around a large open-pit mine: the pit, spoil heaps, a tailings dam above a river, a processing plant and a new town for workers.'],
        [('Describe two environmental impacts of the mine.', 'Loss of forest habitat; dust and noise; water pollution from tailings or acid drainage; visual impact of pit and spoil; lower water table.', '1 mark per impact up to [2]'),
         ('Explain why the tailings dam is a risk to the river.', 'Tailings contain heavy metals and chemicals; seepage or dam failure (e.g. after heavy rain or earthquakes) would release them into the river, killing aquatic life and contaminating water supplies.', 'contents [1]; seepage / failure [1]; effect on river [1] [3]'),
         ('Suggest two ways the company could reduce the environmental impact during operation.', 'Line and monitor the tailings dam; treat water before release; control dust with water sprays; store topsoil for later; replant spoil heaps progressively.', '1 mark per strategy up to [2]'),
         ('Describe how the site could be restored after mining ends.', 'Reshape and stabilise spoil, replace topsoil, plant native species, create a lake or wetland in the pit, and monitor water quality.', '1 mark per point up to [3]'),
         ('Suggest why local people may support the mine.', 'Jobs, higher incomes, new roads, schools and health care, and tax revenue for the government.', '1 mark per point up to [2]')])],
    'essays': [
        ('the economic benefits of mineral extraction outweigh its environmental costs',
         ['Mining provides jobs, exports and tax revenue (e.g. copper in Chile, about 10% of GDP) and raw materials for technology, including renewable energy.'],
         ['Habitat loss, water pollution (Ok Tedi, Papua New Guinea), tailings disasters (Brumadinho, Brazil, 2019) and long-term contamination impose high costs, often on local and indigenous communities.'],
         'Benefits can outweigh costs only if strong regulation, restoration and fair sharing of income are in place.',
         ['employment', 'pollution', 'restoration', 'regulation']),
    ],
})
compare_item(l5, [
    ('open-pit mining', 'underground (deep) mining', 'Open-pit mining removes overburden to dig ore from a large pit, so it disturbs large areas of land and produces much waste rock but is cheaper and safer; underground mining reaches deep ores through shafts and tunnels with less surface disturbance but higher costs and risks to miners.', 'Both remove ore and produce waste such as tailings.'),
])


@l5.add('C3', (1, 2, 3, 4, 5), 'numerical')
def l5_grade(r, D):
    metal, grades = r.choice([('copper', [0.4, 0.5, 0.6, 0.8, 1.0]), ('gold', [None]), ('zinc', [3, 5, 8]), ('iron', [40, 55, 62])])
    if metal == 'gold':
        g = r.choice([1.5, 2, 3, 5])   # g per tonne
        target = r.choice([10, 20, 50])   # tonnes of gold
        ore = target * 1e6 / g
        intro = f'A gold mine processes ore with a grade of {g} g of gold per tonne of ore.'
        if D == 1:
            return MCQ(r, intro + f' How many tonnes of ore must be mined to produce {target} tonnes of gold?', f'{nf(ore)} t',
                       [f'{nf(ore / 1000)} t', f'{nf(ore * 10)} t', f'{nf(target * g)} t', f'{nf(ore / 10)} t'], f'{target} t = {nf(target * 1e6)} g; ÷ {g} = {nf(ore)} t. [1]')
        parts = [L(f'Calculate the mass of ore that must be mined to produce {target} tonnes of gold.', f'{nf(ore)} t', f'{target} × 1 000 000 g ÷ {g} [1] = {nf(ore)} t [1] [2]'),
                 L('Calculate the mass of waste produced (assume all ore except the gold becomes waste).', f'{nf(ore - target)} t', f'{nf(ore)} − {target} = {nf(ore - target)} t [1]'),
                 L('Suggest why gold mines produce very large amounts of waste.', 'The grade is extremely low (a few grams per tonne), so almost all the rock mined is waste.', '[1]'),
                 L('Explain one environmental risk from processing gold ore.', 'Cyanide or mercury is used to extract gold; leaks or spills poison rivers and wildlife (e.g. Baia Mare, Romania, 2000).', 'chemical named [1]; effect [1] [2]')]
        return comp(r, intro, parts, D)
    g = r.choice(grades)
    ore = r.choice([10, 20, 50, 100]) * 1e6   # tonnes per year
    rec = r.choice([85, 90, 95])
    metal_t = ore * g / 100 * rec / 100
    strip = r.choice([1.5, 2, 3])
    intro = (f'An open-pit {metal} mine extracts {nf(ore / 1e6)} million tonnes of ore per year with a grade of {fmt(g, 1)}% {metal}. '
             f'{rec}% of the metal in the ore is recovered by processing. For each tonne of ore, {fmt(strip, 1)} tonnes of overburden must also be removed.')
    if D == 1:
        return MCQ(r, intro + f' What mass of {metal} is produced per year?', f'{nf(metal_t)} t',
                   [f'{nf(ore * g / 100)} t', f'{nf(metal_t * 10)} t', f'{nf(ore * g * rec / 100)} t', f'{nf(metal_t / 10)} t'], f'{nf(ore)} × {fmt(g / 100, 4)} × {rec / 100:.2f} = {nf(metal_t)} t. [1]')
    waste = ore - metal_t + ore * strip
    parts = [
        L(f'Calculate the mass of {metal} produced per year.', f'{nf(metal_t)} t', f'{nf(ore)} × {fmt(g, 1)}/100 [1] × {rec}/100 = {nf(metal_t)} t [1] [2]'),
        L('Calculate the total mass of waste (overburden plus processed ore) produced per year.', f'{nf(waste)} t', f'overburden {nf(ore * strip)} + tailings {nf(ore - metal_t)} [1] = {nf(waste)} t [1] [2]'),
        L(f'Calculate the mass of waste produced per tonne of {metal}.', f'{s3(waste / metal_t)} t', f'{nf(waste)} ÷ {nf(metal_t)} = {s3(waste / metal_t)} t [1]'),
        L('Explain why the ratio of waste to metal tends to increase over time at many mines.', 'The highest-grade ore is mined first; later ore is lower grade and the pit is deeper, so more overburden must be removed per tonne of metal.', 'declining grade [1]; deeper pit / more overburden [1] [2]'),
        L('Suggest one way the waste could be managed to reduce environmental impacts.', 'Store tailings in lined, monitored dams or as dry stacks; use overburden to backfill and restore the pit; cover sulfide waste to prevent acid drainage.', '[1]'),
    ]
    return comp(r, intro, parts, D)


CHAPTERS[1] = [l1, l2, l3, l4, l5]


# ============================================================== CHAPTER 2: Hydrosphere

h1 = T('The hydrological cycle: stores, flows and processes', 'hydrological cycle', 'stores, flows')
build(h1, {
    'terms': [
        ('evapotranspiration', 'the combined loss of water to the atmosphere by evaporation from surfaces and transpiration from plants'),
        ('infiltration', 'the downward movement of water from the ground surface into the soil'),
        ('percolation', 'the downward movement of water through soil and rock into groundwater stores'),
        ('interception', 'the capture of precipitation by vegetation before it reaches the ground'),
        ('surface runoff', 'water flowing over the ground surface when it cannot infiltrate'),
        ('residence time', 'the average length of time a molecule of water stays in a store'),
        ('aquifer', 'a permeable rock that stores water and allows it to flow through it'),
        ('water table', 'the upper surface of the saturated zone in the ground'),
    ],
    'mcq': [
        ('About what percentage of the Earth’s water is fresh water?', 'About 2.5%', ['About 25%', 'About 50%', 'About 0.01%'], 'About 97.5% is salt water in the oceans. [1]'),
        ('Which is the largest store of fresh water?', 'Ice sheets and glaciers', ['Lakes', 'Rivers', 'The atmosphere'], 'About 69% of fresh water is ice; about 30% is groundwater. [1]'),
        ('Which process transfers water from plants to the atmosphere?', 'Transpiration', ['Infiltration', 'Percolation', 'Condensation'], '[1]'),
        ('Urbanisation usually causes', 'more surface runoff and less infiltration', ['more infiltration and less runoff', 'more interception', 'a rise in the water table'], 'Impermeable surfaces. [1]'),
        ('Which energy source drives evaporation in the hydrological cycle?', 'Solar radiation', ['Geothermal heat', 'Tidal energy', 'Wind alone'], '[1]'),
        ('The average residence time of water in the atmosphere is about', '9 days', ['9 hours', '9 years', '900 years'], 'About 12 900 km³ stored ÷ about 500 000 km³ per year. [1]'),
    ],
    'explain': [
        ('Explain how deforestation affects the hydrological cycle of a drainage basin.', 'Less interception and transpiration, so less water returns to the atmosphere and local rainfall may fall; more rain reaches the ground and, with less root binding and organic matter, infiltration falls and surface runoff increases, causing faster, higher river peaks and more soil erosion.', '1 mark per developed point up to [3]'),
        ('Explain why the hydrological cycle is a closed system at the global scale but an open system at the drainage-basin scale.', 'Globally no water enters or leaves the Earth system, only energy; a drainage basin receives inputs of precipitation and loses outputs such as evapotranspiration and river discharge to the sea.', 'global: no input/output of water [1]; basin: inputs and outputs [1] [2]'),
        ('Describe the processes by which water moves from the ocean to a river.', 'Evaporation from the ocean; condensation to form clouds; transport by wind; precipitation over land; then infiltration, throughflow, groundwater flow or surface runoff into the river.', '1 mark per process in sequence up to [3]'),
        ('Explain why groundwater has a much longer residence time than river water.', 'Water moves very slowly through the pores and fractures of rock, and aquifers hold very large volumes relative to the flow through them.', 'slow movement through rock [1]; large store relative to flux [1] [2]'),
    ],
    'claims': [
        ('Climate change could speed up the hydrological cycle.', True, 'A warmer atmosphere increases evaporation and can hold about 7% more water vapour per °C, giving more intense rainfall and droughts.'),
        ('Most precipitation over land falls directly into rivers.', False, 'Most falls on the ground or vegetation and reaches rivers by runoff, throughflow or groundwater flow, or is evaporated.'),
        ('Rivers and lakes hold most of the world’s fresh water.', False, 'They hold well under 1%; most is in ice and groundwater.'),
    ],
    'cases': [(
        ['Fig. 2.1 shows a systems diagram of a drainage basin, with precipitation as the input, stores (interception, surface, soil, groundwater, channel) and outputs of evapotranspiration and river discharge.',
         'A hydrologist in {c} is comparing two small drainage basins: one forested and one recently converted to housing and roads.'],
        [('Name two stores and two flows in a drainage basin.', 'Stores: interception, soil moisture, groundwater, surface storage, channel. Flows: infiltration, percolation, throughflow, surface runoff, groundwater flow.', '1 mark per two correct [2]'),
         ('Explain why river discharge rises faster after rain in the urban basin.', 'Impermeable surfaces (roads, roofs) prevent infiltration, so more surface runoff; drains carry water quickly to the river; less vegetation means little interception.', '1 mark per point up to [3]'),
         ('Suggest why the forested basin has a higher base flow in dry weather.', 'More water infiltrates and recharges soil and groundwater, which slowly feed the river between storms.', 'infiltration / recharge [1]; slow release to river [1] [2]'),
         ('Suggest one sustainable drainage (SuDS) method for the urban basin and explain how it works.', 'Permeable paving, green roofs, swales or retention ponds increase infiltration or store water, slowing runoff.', 'method [1]; explanation [1] [2]'),
         ('Explain the role of the Sun in driving the cycle.', 'Solar energy evaporates water and drives atmospheric circulation that moves vapour; gravity then returns water as precipitation and flow.', 'evaporation [1]; circulation / transport [1] [2]')])],
    'essays': [
        ('human activity now has a greater effect on the hydrological cycle than natural variation',
         ['Deforestation, urbanisation, groundwater abstraction (e.g. the Ogallala aquifer), dams and irrigation (the Aral Sea) have changed stores and flows dramatically; climate change intensifies the cycle.'],
         ['Natural cycles such as ENSO, monsoon variability and long-term climate change cause large changes in rainfall and storage; the global volume of water is unchanged.'],
         'At the local and regional scale human impacts are often dominant; globally natural processes still control most flows, though human-caused warming is increasing their intensity.',
         ['land-use change', 'abstraction', 'climate change', 'ENSO']),
    ],
})
compare_item(h1, [
    ('infiltration', 'percolation', 'Infiltration is the movement of water from the surface into the soil; percolation is the deeper movement of water from soil into underlying rock and groundwater.', 'Both are downward movements of water that reduce surface runoff.'),
    ('throughflow', 'surface runoff', 'Throughflow is the lateral movement of water through the soil; surface runoff flows over the ground surface and reaches rivers much faster.', 'Both transfer water downslope to river channels.'),
])

STORES = [('the atmosphere', 12900, 'evaporation (and precipitation)', 505000, 'days'), ('rivers', 2120, 'discharge to the oceans', 45000, 'days'),
          ('the oceans', 1338000000, 'evaporation from the oceans', 434000, 'years'), ('groundwater', 23400000, 'groundwater discharge', 2200, 'years'),
          ('soil moisture', 16500, 'evapotranspiration and drainage', 90000, 'days'), ('lakes', 176400, 'outflow and evaporation', 10000, 'years')]


@h1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def h1_res(r, D):
    name, store, flux_name, flux, unit = r.choice(STORES)
    store = round(store * r.uniform(0.95, 1.05), -1 if store < 1e5 else -3)
    flux = round(flux * r.uniform(0.95, 1.05), -2 if flux > 1000 else 0)
    t_years = store / flux
    val = t_years * 365 if unit == 'days' else t_years
    intro = f'The volume of water stored in {name} is about {nf(store)} km³. The flow of water out of this store by {flux_name} is about {nf(flux)} km³ per year.'
    if D == 1:
        return MCQ(r, intro + f' What is the residence time of water in {name}?', f'{s3(val)} {unit}',
                   [f'{s3(val * 10)} {unit}', f'{s3(val / 10)} {unit}', f'{s3(t_years if unit == "days" else val * 365)} {"years" if unit == "days" else "days"}', f'{s3(val * 2)} {unit}'],
                   f'residence time = store ÷ flow = {nf(store)} ÷ {nf(flux)} = {s3(t_years)} years' + (f' = {s3(val)} days. [1]' if unit == 'days' else '. [1]'))
    parts = [
        L(f'Calculate the residence time of water in {name}, in {unit}. Show your working.', f'{s3(val)} {unit}',
          f'store ÷ flow = {nf(store)} ÷ {nf(flux)} = {s3(t_years)} years [1]' + (f'; × 365 = {s3(val)} days [1] [2]' if unit == 'days' else ' [1] [2]')),
        L('Explain what is meant by residence time.', 'The average time a water molecule spends in a store before moving to another part of the cycle.', '[1]'),
        L('Suggest why pollution in a store with a long residence time is a serious problem.', 'Pollutants are flushed out very slowly, so contamination persists for decades or longer and is hard to clean up (e.g. nitrates in groundwater).', 'slow flushing [1]; persistence / example [1] [2]'),
        L('Explain why the residence time is only an average.', 'Some water passes through quickly and some stays much longer; flows vary with season and location.', '[1]'),
    ]
    return comp(r, intro, parts, D)


@h1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def h1_budget(r, D):
    P = r.randint(60, 220) * 10
    E = round(P * r.uniform(0.3, 0.7), -1)
    dS = r.choice([-60, -40, -20, 0, 20, 40, 60])
    Q = P - E - dS
    basin = r.choice(['the upper Rhine basin', 'a small basin near ' + city(r), 'the Mekong headwaters', 'a forested basin in the Western Ghats', 'a chalk catchment in southern England'])
    intro = f'In one year {basin} received {nf(P)} mm of precipitation. Evapotranspiration was {nf(E)} mm and the change in storage (soil and groundwater) was {"+" if dS > 0 else MINUS if dS < 0 else ""}{abs(dS)} mm.'
    if D == 1:
        return MCQ(r, intro + ' Using P = Q + E ± ΔS, what was the river discharge (Q), in mm?', f'{nf(Q)} mm',
                   [f'{nf(P - E + dS)} mm', f'{nf(P - E)} mm' if dS else f'{nf(P + E)} mm', f'{nf(P + E - dS)} mm', f'{nf(E - dS)} mm'], f'Q = {nf(P)} − {nf(E)} − ({dS}) = {nf(Q)} mm. [1]')
    area = r.choice([50, 120, 300, 800])
    vol = Q / 1000 * area * 1e6   # m³
    parts = [
        L('Using the water balance equation P = Q + E ± ΔS, calculate the river discharge (Q) in mm.', f'{nf(Q)} mm', f'Q = P − E − ΔS = {nf(P)} − {nf(E)} − ({dS}) [1] = {nf(Q)} mm [1] [2]'),
        L('Calculate the percentage of precipitation lost by evapotranspiration.', f'{f1(E / P * 100)}%', f'{nf(E)} ÷ {nf(P)} × 100 = {f1(E / P * 100)}% [1]'),
        L(f'The basin has an area of {area} km². Calculate the volume of river discharge in the year in m³.', f'{s3(vol)} m³ ({sf(vol / 1e6, 3)} million m³)', f'{nf(Q)} mm = {Q / 1000:g} m [1]; × {area} × 10⁶ m² = {s3(vol)} m³ [1] [2]'),
        L('Suggest what the change in storage tells you about the year.', ('Storage increased, so it was a wet year: soil and groundwater were recharged.' if dS > 0 else 'Storage fell, so water was drawn from soil and groundwater: a dry year or heavy abstraction.' if dS < 0 else 'There was no net change in storage: inputs and outputs balanced.'), '[1]'),
        L('Explain how evapotranspiration would change if the basin was deforested.', 'It would fall because there is less transpiration and less interception loss, so more water becomes runoff.', 'less transpiration / interception [1]; more runoff [1] [2]'),
    ]
    return comp(r, intro, parts, D)


h2 = T('Oceans: ocean currents, upwelling and El Niño Southern Oscillation', 'ocean currents', 'upwelling', 'el niño')
build(h2, {
    'terms': [
        ('ocean current', 'a continuous, directed movement of sea water driven by winds, the Earth’s rotation and differences in density'),
        ('thermohaline circulation', 'the global ocean conveyor belt driven by differences in water density caused by temperature and salinity'),
        ('upwelling', 'the rise of cold, nutrient-rich water from the deep ocean to the surface'),
        ('El Niño', 'the warm phase of ENSO, when trade winds weaken and warm water spreads east across the Pacific towards South America'),
        ('La Niña', 'the cold phase of ENSO, when trade winds strengthen and cold upwelling off South America intensifies'),
        ('gyre', 'a large system of rotating ocean currents in an ocean basin'),
        ('Walker circulation', 'the east-west atmospheric circulation over the tropical Pacific, with rising air in the west and sinking air in the east in normal years'),
        ('Southern Oscillation', 'the see-saw in air pressure between the western and eastern tropical Pacific that accompanies El Niño and La Niña'),
    ],
    'mcq': [
        ('Which ocean current keeps north-west Europe warmer than other places at the same latitude?', 'The Gulf Stream / North Atlantic Drift', ['The Humboldt Current', 'The Canary Current', 'The Benguela Current'], '[1]'),
        ('During an El Niño event, the sea surface off Peru becomes', 'warmer, and upwelling weakens', ['colder, and upwelling strengthens', 'saltier and colder', 'unchanged'], '[1]'),
        ('Why are areas of upwelling important for fisheries?', 'Upwelled water brings nutrients that support plankton growth', ['Upwelled water is warmer', 'Upwelling reduces salinity', 'Upwelling increases wave height'], 'E.g. the Peruvian anchoveta fishery. [1]'),
        ('Cold water sinks in the North Atlantic because it is', 'cold and salty, so dense', ['warm and fresh', 'less dense', 'pushed by tides'], '[1]'),
        ('During El Niño, which area often experiences drought?', 'Indonesia and eastern Australia', ['Peru and Ecuador', 'The southern USA', 'Central Pacific islands'], 'Rising air and rain move east. [1]'),
    ],
    'explain': [
        ('Explain why upwelling occurs off the coast of Peru in a normal year.', 'South-east trade winds blow surface water offshore and westwards (helped by the Coriolis effect); cold, nutrient-rich water rises from below to replace it.', 'winds move surface water offshore [1]; deep cold water rises to replace it [1] [2]'),
        ('Describe the changes in the Pacific during an El Niño event.', 'Trade winds weaken or reverse; warm water moves east towards South America; upwelling off Peru is suppressed; the area of rising air and rainfall shifts to the central and eastern Pacific; pressure falls in the east and rises in the west.', '1 mark per change up to [3]'),
        ('Explain the impacts of El Niño on the Peruvian fishing industry.', 'Warm water suppresses upwelling so nutrient supply falls; plankton decline; anchoveta stocks fall or move, so catches collapse (e.g. 1972-73 and 1997-98), causing job losses and less fishmeal for export.', 'less upwelling / nutrients [1]; food chain effect [1]; economic impact [1] [3]'),
        ('Explain how ocean currents redistribute heat around the Earth.', 'Warm surface currents carry heat from the tropics towards the poles (e.g. Gulf Stream), and cold currents return cooler water towards the equator, reducing the temperature difference between latitudes.', 'warm currents poleward [1]; cold currents equatorward [1]; effect on climate [1] [3]'),
    ],
    'claims': [
        ('El Niño events affect only the countries next to the Pacific Ocean.', False, 'Through teleconnections they affect weather worldwide, e.g. drought in southern Africa and India and wetter winters in the southern USA.'),
        ('Coastal deserts such as the Atacama are linked to cold ocean currents.', True, 'Cold currents cool the air above, making it stable so little rain falls.'),
        ('Melting of Arctic ice could weaken the thermohaline circulation.', True, 'Fresh meltwater lowers salinity and density, so less water sinks in the North Atlantic.'),
    ],
    'cases': [(
        ['Fig. 2.2 shows sea surface temperatures across the tropical Pacific in December of a normal year and of an El Niño year, with arrows showing the trade winds.',
         'A newspaper in {c} reports that scientists have declared an El Niño event, with sea surface temperatures in the eastern Pacific 1.5 °C above average.'],
        [('Describe the normal pattern of sea surface temperature across the Pacific.', 'Warm water (about 28-30 °C) builds up in the west near Indonesia and Australia; cooler water (about 20-24 °C) in the east near Peru.', 'warm west [1]; cool east with data [1] [2]'),
         ('Explain how the trade winds produce this pattern.', 'Easterly trade winds push warm surface water westwards; this allows cold water to upwell in the east.', '[2]'),
         ('Describe and explain the effects of El Niño on rainfall in South America and Australia.', 'Warm water in the east causes air to rise, giving heavy rain and floods in Peru and Ecuador; sinking air over the western Pacific gives drought and bushfires in eastern Australia.', '1 mark each region with explanation up to [4]'),
         ('Suggest how countries can prepare for El Niño events.', 'Forecasting from ocean buoys and satellites; storing water and food; adjusting crops and fishing quotas; flood defences and emergency planning.', '1 mark per point up to [2]')])],
    'essays': [
        ('the impacts of El Niño are mainly negative',
         ['El Niño causes floods in Peru and Ecuador, drought and fires in Indonesia and Australia, fishery collapse off Peru, and coral bleaching; the 1997-98 event caused about US$35 billion of damage.'],
         ['Some areas benefit: fewer Atlantic hurricanes, milder winters in North America, more rain for some dry regions and growth of shrimp catches in Ecuador.'],
         'The impacts are mostly negative, especially for vulnerable economies, but they vary between regions and some places benefit.',
         ['fisheries', 'droughts and floods', 'teleconnections']),
    ],
})
compare_item(h2, [
    ('El Niño', 'La Niña', 'In El Niño the trade winds weaken and warm water moves east, so Peru is wetter and Australia drier; in La Niña the trade winds strengthen, upwelling off Peru increases and Australia is wetter.', 'Both are phases of ENSO that affect weather around the world.'),
    ('a warm ocean current', 'a cold ocean current', 'Warm currents flow from the tropics towards the poles and warm coastal climates; cold currents flow towards the equator, cool coasts and are linked to dry climates and upwelling.', 'Both redistribute heat around the globe.'),
])


@h2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def h2_oni(r, D):
    yrs = r.choice([('1997', '1998'), ('2015', '2016'), ('2023', '2024'), ('1982', '1983')])
    base = [r.uniform(-0.3, 0.3)]
    peak = r.choice([1.2, 1.6, 2.0, 2.4])
    vals = [round(v, 1) for v in [0.1, 0.4, 0.7, 1.0, peak * 0.8, peak, peak * 0.9, peak * 0.6, 0.3]]
    labs = ['JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ', 'DJF', 'JFM', 'FMA']
    run = 0
    best = 0
    for v in vals:
        run = run + 1 if v >= 0.5 else 0
        best = max(best, run)
    intro = (f'Table 2.2 shows the Oceanic Niño Index (3-month mean sea surface temperature anomaly, °C, in the central Pacific) from mid-{yrs[0]} to early {yrs[1]}: '
             + ', '.join(f'{l} {"+" if v > 0 else ""}{v:.1f}' for l, v in zip(labs, vals)) + '. An El Niño is declared when the anomaly is +0.5 °C or more for at least five consecutive overlapping periods.')
    mean = sum(vals) / len(vals)
    if D == 1:
        return MCQ(r, intro + ' What was the maximum anomaly?', f'+{f1(max(vals))} °C', [f'+{f1(vals[0])} °C', f'+{f1(mean)} °C', f'+{f1(vals[-1])} °C', f'+{f1(max(vals) + 0.5)} °C'], f'Highest value in the table ({labs[vals.index(max(vals))]}). [1]')
    parts = [
        L('State the period with the highest anomaly and its value.', f'{labs[vals.index(max(vals))]}: +{f1(max(vals))} °C', '[1]'),
        L('Calculate the mean anomaly over the nine periods.', f'+{f2(mean)} °C', f'sum {f1(sum(vals))} ÷ 9 = {f2(mean)} [1]'),
        L('Determine whether these data meet the definition of an El Niño. Justify your answer.', f'Yes: the anomaly is +0.5 °C or more for {best} consecutive periods (at least five).', 'uses threshold [1]; counts consecutive periods [1] [2]'),
        L('Classify the strength of the event (weak 0.5-0.9, moderate 1.0-1.4, strong 1.5-1.9, very strong ≥ 2.0 °C peak).',
          'Very strong' if max(vals) >= 2.0 else 'Strong' if max(vals) >= 1.5 else 'Moderate' if max(vals) >= 1.0 else 'Weak', '[1]'),
        L('Suggest the likely impact of this event on the anchoveta catch off Peru, giving a reason.', 'The catch would fall because warmer water suppresses upwelling, so fewer nutrients and less plankton support fewer fish.', 'catch falls [1]; reason [1] [2]'),
    ]
    return comp(r, intro, parts, D)


h3 = T('Fresh water supply: groundwater, surface water and water pollution', 'fresh water supply', 'groundwater', 'water pollution')
build(h3, {
    'terms': [
        ('eutrophication', 'the enrichment of water with nutrients such as nitrates and phosphates, causing algal blooms and oxygen depletion'),
        ('biochemical oxygen demand (BOD)', 'the amount of dissolved oxygen used by microorganisms to break down organic matter in a water sample'),
        ('point source pollution', 'pollution entering water from a single identifiable source, such as a sewage outfall or factory pipe'),
        ('diffuse (non-point) source pollution', 'pollution entering water from many scattered sources, such as fertiliser runoff from farmland'),
        ('confined aquifer', 'an aquifer sandwiched between impermeable rock layers, so water is under pressure'),
        ('artesian well', 'a well into a confined aquifer where pressure forces water to rise without pumping'),
        ('bioaccumulation', 'the build-up of a persistent substance in the tissues of an organism over its lifetime'),
        ('indicator species', 'an organism whose presence or absence shows the level of pollution, such as stonefly nymphs in clean water'),
    ],
    'mcq': [
        ('Which organism indicates clean, well-oxygenated river water?', 'Stonefly nymph', ['Rat-tailed maggot', 'Sludge worm (Tubifex)', 'Bloodworm'], '[1]'),
        ('Which pollutant is the main cause of eutrophication?', 'Nitrates and phosphates', ['Mercury', 'Plastics', 'Heat'], '[1]'),
        ('Water that has a high BOD contains', 'a lot of organic matter being decomposed by microorganisms', ['a lot of dissolved oxygen', 'no bacteria', 'very little organic matter'], '[1]'),
        ('Arsenic in groundwater has affected millions of people in', 'Bangladesh', ['Iceland', 'Canada', 'New Zealand'], 'Naturally occurring arsenic in tube wells. [1]'),
        ('Which treatment stage kills pathogens in drinking water?', 'Chlorination or UV disinfection', ['Screening', 'Sedimentation', 'Flocculation'], '[1]'),
        ('Thermal pollution from a power station reduces river life mainly because warm water', 'holds less dissolved oxygen', ['is more acidic', 'contains more nitrate', 'is more turbid'], '[1]'),
    ],
    'explain': [
        ('Describe the stages of eutrophication.', 'Nutrients (nitrates, phosphates) enter water; algae grow rapidly forming a bloom; light is blocked so plants below die; algae and plants die and are decomposed by bacteria; bacteria use up dissolved oxygen; fish and other animals die.', '1 mark per stage in sequence up to [4]'),
        ('Explain why over-abstraction of groundwater is a problem in coastal areas.', 'The water table falls and the pressure of fresh water drops, so salt water from the sea moves into the aquifer (saltwater intrusion), making wells unusable; land may also subside.', 'falling water table [1]; saltwater intrusion [1]; consequence [1] [3]'),
        ('Explain how persistent pollutants such as mercury can harm top predators.', 'Mercury is not broken down and is stored in tissues (bioaccumulation); at each trophic level organisms eat many prey, so concentration increases (biomagnification); top predators and humans receive toxic doses (e.g. Minamata, Japan).', 'bioaccumulation [1]; biomagnification [1]; effect / example [1] [3]'),
        ('Explain why groundwater is an important source of water in many countries.', 'It is available all year, even in droughts; it is usually naturally filtered and cleaner than surface water; it is widely distributed and can be reached by wells close to users.', '1 mark per reason up to [3]'),
        ('Describe how sewage is treated before discharge into a river.', 'Screening removes large objects; primary sedimentation removes solids; secondary (biological) treatment uses bacteria in aeration tanks or trickling filters to break down organic matter; tertiary treatment may remove nutrients or disinfect.', '1 mark per stage up to [3]'),
    ],
    'claims': [
        ('Groundwater is always safe to drink because it is filtered by rocks.', False, 'It can contain natural contaminants such as arsenic or fluoride, and can be polluted by nitrates, leaking septic tanks or industrial chemicals.'),
        ('Diffuse pollution is harder to control than point source pollution.', True, 'It comes from many scattered sources, so it is difficult to identify and regulate each one.'),
        ('Fish die in eutrophic lakes because the nutrients are poisonous.', False, 'They die because decomposition by bacteria uses up the dissolved oxygen.'),
    ],
    'cs': [('a polluted freshwater body', [
        ('the Ganges (Ganga), India', {
            'causes': 'About 3 billion litres per day of mostly untreated sewage from over 100 cities; industrial waste from tanneries in Kanpur (chromium); agricultural runoff; religious offerings and cremation remains.',
            'management': 'The Ganga Action Plan (1985) and Namami Gange programme (2014) built sewage treatment plants, cleaned riverfronts and monitored industry; progress has been slow because treatment capacity is still far below sewage volumes.'}),
        ('Lake Erie, USA and Canada', {
            'causes': 'Phosphates from detergents, sewage and farm fertiliser caused severe eutrophication in the 1960s-70s and harmful algal blooms again since 2011, e.g. the 2014 Toledo drinking water ban.',
            'management': 'The 1972 Great Lakes Water Quality Agreement limited phosphates in detergents and upgraded sewage works, so the lake recovered by the 1980s; current targets aim to cut phosphorus loads by 40% from farms.'}),
    ], [
        ('explain the causes of the pollution', 'causes', 'sources (point and diffuse), named pollutants, effects'),
        ('evaluate the strategies used to improve water quality', 'management', 'named strategies with outcomes; limitations; judgement'),
    ])],
    'essays': [
        ('pollution is a greater threat to fresh water supply than over-abstraction',
         ['Untreated sewage, industrial waste and fertiliser runoff make water unsafe (e.g. the Ganges, Lake Erie); about 2 billion people use a drinking water source contaminated with faeces.'],
         ['Over-abstraction empties aquifers and rivers (e.g. the Ogallala aquifer, the Aral Sea, Chennai in 2019) and causes saltwater intrusion and subsidence, permanently reducing supply.'],
         'Both are serious; pollution can often be treated, while over-abstraction of fossil groundwater may be irreversible.',
         ['sewage', 'agriculture', 'groundwater depletion']),
    ],
})
compare_item(h3, [
    ('point source pollution', 'diffuse pollution', 'Point source pollution comes from one identifiable outlet such as a sewage pipe and is easier to monitor and regulate; diffuse pollution comes from many scattered sources such as fields and roads and is hard to control.', 'Both reduce water quality and can cause eutrophication.'),
    ('surface water', 'groundwater', 'Surface water (rivers, lakes) is easy to access but varies with season and is easily polluted; groundwater is stored in aquifers, is more reliable and naturally filtered but expensive to pump and slow to recharge.', 'Both are sources of fresh water that depend on precipitation.'),
])


@h3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def h3_river(r, D):
    src = r.choice(['a sewage treatment works outfall', 'a food-processing factory', 'a dairy farm', 'a paper mill'])
    river = r.choice(['River Tisza', 'a tributary of the Mekong', 'River Tees', 'a river flowing through ' + city(r), 'River Densu in Ghana', 'a stream in the Cameron Highlands'])
    do_up = round(r.uniform(9.0, 11.0), 1)
    do_at = round(r.uniform(3.0, 5.5), 1)
    do_dn = round(r.uniform(6.5, 8.5), 1)
    bod = [round(r.uniform(1.5, 3), 1), round(r.uniform(8, 15), 1), round(r.uniform(3.5, 6), 1)]
    intro = (f'Students measured water quality on {river} at site A (500 m upstream of {src}), site B (50 m downstream) and site C (2 km downstream). '
             f'Dissolved oxygen (mg/l): A {do_up}, B {do_at}, C {do_dn}. BOD (mg/l): A {bod[0]}, B {bod[1]}, C {bod[2]}.')
    drop = pc(do_up, do_at)
    if D == 1:
        return MCQ(r, intro + ' What is the percentage decrease in dissolved oxygen from site A to site B?', f'{f1(-drop)}%',
                   [f'{f1(do_up - do_at)}%', f'{f1(-pc(do_at, do_up))}%', f'{f1(do_at / do_up * 100)}%', f'{f1(-drop / 2)}%'], f'({do_up} − {do_at}) ÷ {do_up} × 100 = {f1(-drop)}%. [1]')
    parts = [
        L('Calculate the percentage decrease in dissolved oxygen between site A and site B.', f'{f1(-drop)}%', f'({do_up} − {do_at}) ÷ {do_up} × 100 [1] = {f1(-drop)}% [1] [2]'),
        L('Describe the changes in BOD downstream.', f'BOD rises sharply from {bod[0]} mg/l at A to {bod[1]} mg/l at B, then falls to {bod[2]} mg/l at C but stays above the upstream value.', 'rise then fall [1]; data [1] [2]'),
        L('Explain the relationship between BOD and dissolved oxygen at site B.', 'Organic waste from the discharge is decomposed by aerobic bacteria; high BOD means the bacteria use up dissolved oxygen, so oxygen falls.', 'organic matter decomposed [1]; bacteria use oxygen [1] [2]'),
        L('Explain why the water quality improves by site C.', 'Dilution by the river and tributaries; bacteria have broken down much of the organic matter (self-purification); re-oxygenation from the air, especially in turbulent riffles, and from photosynthesis.', '1 mark per point up to [2]'),
        L('Suggest which invertebrates you would expect to find at sites A and B.', 'A: pollution-intolerant species such as stonefly and mayfly nymphs; B: tolerant species such as sludge worms, bloodworms and rat-tailed maggots.', '1 mark each site [2]'),
        L('Suggest how the students could make their measurements reliable.', 'Take several readings at each site and calculate a mean; sample at the same time of day and depth; calibrate the oxygen meter.', '1 mark per point up to [2]'),
    ]
    return comp(r, intro, parts, D)


@h3.add('C3', (2, 3, 4, 5), 'numerical')
def h3_aquifer(r, D):
    aq = r.choice(['the Ogallala aquifer in the USA', 'an aquifer beneath Chennai', 'the aquifer under the North China Plain', 'a coastal aquifer near Gaza', 'an aquifer in Punjab, India'])
    store = r.choice([20, 40, 60, 100, 150])        # km³ usable
    rech = round(r.uniform(0.3, 1.5), 1)            # km³/yr
    abst = round(rech * r.uniform(1.8, 4.0), 1)
    deficit = abst - rech
    yrs = store / deficit
    cut = r.choice([20, 30, 40, 50])
    new_abs = abst * (1 - cut / 100)
    intro = f'Recharge of {aq} is about {fmt(rech, 1)} km³ per year, but abstraction for irrigation and towns is {fmt(abst, 1)} km³ per year. About {store} km³ of usable water remains in storage.'
    parts = [
        L('Calculate the annual deficit.', f'{fmt(round(deficit, 1), 1)} km³ per year', f'{fmt(abst, 1)} − {fmt(rech, 1)} = {fmt(round(deficit, 1), 1)} [1]'),
        L('Estimate how many years the usable water will last at the current rate.', f'{s3(yrs)} years', f'{store} ÷ {fmt(round(deficit, 1), 1)} [1] = {s3(yrs)} years [1] [2]'),
        L(f'Water-saving irrigation reduces abstraction by {cut}%. Calculate the new lifetime of the aquifer, or state whether it would become sustainable.',
          (f'New abstraction {s3(new_abs)} km³; deficit {s3(new_abs - rech)} km³; lifetime {s3(store / (new_abs - rech))} years.' if new_abs > rech else f'New abstraction {s3(new_abs)} km³ is no more than recharge, so use becomes sustainable.'),
          f'new abstraction {s3(new_abs)} [1]; comparison / new lifetime [1] [2]'),
        L('Describe two consequences of the falling water table.', 'Wells must be deepened and pumping costs rise; wells dry up; land subsidence; rivers and wetlands fed by groundwater dry; saltwater intrusion in coastal aquifers.', '1 mark per consequence up to [2]'),
        L('Suggest two strategies to manage the aquifer more sustainably.', 'Drip irrigation; growing less water-intensive crops; metering and pricing water; licensing wells; artificial recharge using stored storm water or treated wastewater.', '1 mark per strategy up to [2]'),
    ]
    return comp(r, intro, parts, D)


h4 = T('Flooding and drought: causes, impacts and management', 'flooding', 'drought')
build(h4, {
    'terms': [
        ('flood', 'a temporary covering by water of land that is not normally covered, often when a river overflows its banks'),
        ('drought', 'an extended period of below-average precipitation causing a shortage of water'),
        ('flood hydrograph', 'a graph showing river discharge and rainfall over time during and after a storm'),
        ('lag time', 'the time between peak rainfall and peak discharge'),
        ('recurrence interval', 'the average time between events of a given size, such as a 1-in-100-year flood'),
        ('hard engineering', 'the use of artificial structures such as dams, levees and channels to control natural processes'),
        ('soft engineering', 'working with natural processes to manage hazards, such as floodplain zoning, wetland restoration and afforestation'),
        ('flash flood', 'a sudden flood with a very short lag time, often after intense rain on steep or impermeable ground'),
    ],
    'mcq': [
        ('Which factor shortens the lag time of a river?', 'Impermeable urban surfaces', ['Dense forest', 'Permeable sandstone', 'Gentle slopes'], '[1]'),
        ('A 1-in-100-year flood has a probability in any one year of', '1%', ['10%', '0.1%', '100%'], '1 ÷ 100. [1]'),
        ('Which is an example of soft engineering for flood management?', 'Restoring wetlands on the floodplain', ['Building levees', 'Straightening the channel', 'Building a dam'], '[1]'),
        ('Which country is most affected by flooding from monsoon rain and Himalayan snowmelt in the Ganges-Brahmaputra delta?', 'Bangladesh', ['Egypt', 'Chile', 'Mongolia'], '[1]'),
        ('Which is a strategy for coping with drought?', 'Building reservoirs and rainwater harvesting', ['Planting water-hungry crops', 'Increasing irrigation from rivers that are drying', 'Draining wetlands'], '[1]'),
    ],
    'explain': [
        ('Explain how physical factors in a drainage basin can increase flood risk.', 'Intense or prolonged rainfall; saturated or frozen ground; steep slopes; impermeable rock or clay soils; small, circular basins with a high drainage density; snowmelt.', '1 mark per factor with explanation up to [3]'),
        ('Explain how human activities can increase the risk of flooding.', 'Urbanisation (impermeable surfaces, drains); deforestation (less interception, more runoff); building on floodplains; channel straightening that speeds water downstream; farming that compacts soil.', '1 mark per developed point up to [3]'),
        ('Explain why droughts may become more frequent with climate change.', 'Higher temperatures increase evaporation; rainfall patterns shift with more variable and less reliable rain in some regions; earlier snowmelt reduces summer flows.', '1 mark per point up to [3]'),
        ('Describe the impacts of drought on people and the environment.', 'Crop failure and livestock deaths, food shortages and rising prices; water shortages and disease; wildfires; loss of habitats and wetland drying; soil erosion; migration.', '1 mark per impact up to [3]'),
    ],
    'claims': [
        ('Building a dam removes all flood risk downstream.', False, 'Dams reduce flood peaks but can be overtopped or fail; they may give a false sense of security encouraging building on floodplains.'),
        ('Floods can bring benefits to farmers.', True, 'They deposit fertile silt and recharge soil water, e.g. on the floodplains of Bangladesh.'),
        ('Drought is only caused by a lack of rainfall.', False, 'High temperatures, evaporation and human over-use of water also cause water shortages.'),
    ],
    'cases': [(
        ['Fig. 2.4 shows flood hydrographs for two drainage basins after the same storm. Basin X (urban) peaks at 85 cumecs 6 hours after peak rainfall; basin Y (forested) peaks at 30 cumecs 18 hours after peak rainfall.',
         'A town near {f} built on a floodplain has flooded three times in ten years. The council is considering levees, a flood-relief channel or upstream tree planting.'],
        [('Calculate the difference in lag time between the two basins.', '12 hours (18 − 6)', '[1]'),
         ('Explain why the urban basin has a higher and earlier peak.', 'Impermeable surfaces and drains send rainwater quickly to the river with little infiltration or interception.', '1 mark per point up to [2]'),
         ('Compare hard and soft engineering approaches to reducing the flood risk.', 'Hard (levees, channels, dams) give immediate high protection but are costly, may move the problem downstream and look unnatural; soft (afforestation, wetlands, zoning) are cheaper, sustainable and support wildlife but take time and may protect less in extreme floods.', '1 mark each comparative point up to [4]'),
         ('Suggest why some people may oppose upstream tree planting.', 'It takes land from farmers, takes many years to reduce flood peaks and may not prevent extreme floods.', '1 mark per point up to [2]'),
         ('Explain the purpose of land-use zoning on floodplains.', 'It restricts building in high-risk areas, so fewer people and property are exposed, and keeps the floodplain free to store water.', '[2]')])],
    'cs': [('a flood or drought event', [
        ('the 2022 Pakistan floods', {
            'causes': 'Record monsoon rainfall (about three times the average in August), intensified by high temperatures, plus glacier melt in the north; the Indus overflowed and flat land in Sindh was submerged.',
            'impacts': 'About 1700 deaths; 33 million people affected; about 2 million homes damaged; 4 million hectares of crops lost; outbreaks of malaria and waterborne disease; damage about US$30 billion.',
            'management': 'Rescue by the army and NGOs; international appeals; limited early warning and poor drainage in Sindh; afterwards plans for climate-resilient rebuilding and the Living Indus restoration initiative.'}),
        ('the 2019 Chennai water crisis, India', {
            'causes': 'A weak 2018 north-east monsoon left the four reservoirs almost empty; rapid urban growth, the loss of lakes and wetlands to building, and over-pumping of groundwater.',
            'impacts': 'Piped supply cut; residents queued for tankers; offices and restaurants closed; water prices rose sharply, hitting the poor hardest.',
            'management': 'Water brought by train from Jolarpettai; desalination plants expanded; compulsory rainwater harvesting on buildings; plans to restore lakes and recycle wastewater.'}),
        ('the Somerset Levels floods, UK, 2014', {
            'causes': 'The wettest January on record on low-lying, flat land with clay soils; rivers had not been dredged and were silted; high tides prevented drainage.',
            'impacts': 'About 600 homes flooded; 65 km² of farmland under water for weeks; villages cut off; £10 million cost to agriculture.',
            'management': 'The Somerset Levels and Moors Flood Action Plan: dredging 8 km of the Parrett and Tone, raising roads, a tidal barrier planned at Bridgwater and upstream tree planting.'}),
    ], [
        ('describe the causes of the event', 'causes', 'physical and human causes, with data'),
        ('describe the impacts on people and the environment', 'impacts', 'social, economic and environmental impacts with figures'),
        ('evaluate the effectiveness of the responses', 'management', 'short- and long-term responses; judgement'),
    ])],
    'essays': [
        ('hard engineering is the most effective way to manage flood risk',
         ['Dams (e.g. the Three Gorges Dam) and levees give high levels of protection to cities; the Thames Barrier protects London.'],
         ['Hard engineering is expensive, can fail in extreme events (New Orleans levees, 2005), moves flooding downstream and damages ecosystems; soft approaches such as wetland restoration and zoning are cheaper and sustainable.'],
         'An integrated approach combining hard defences for high-value areas with soft engineering and planning is most effective.',
         ['cost', 'sustainability', 'named schemes']),
    ],
})


@h4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def h4_ri(r, D):
    n = r.choice([30, 40, 50, 60, 80, 100])
    ranks = sorted(r.sample(range(1, 11), 4))
    q = sorted([r.randint(300, 1500) for _ in range(4)], reverse=True)
    river = r.choice(['River Severn at Bewdley', 'the Brahmaputra at Bahadurabad', 'the Mekong at Vientiane', 'the Rhine at Cologne', 'a river near ' + city(r)])
    ri = [(n + 1) / m for m in ranks]
    intro = (f'Annual maximum discharges were recorded for {river} over {n} years and ranked (1 = largest). Recurrence interval RI = (n + 1) ÷ m, where n is the number of years and m the rank. '
             + '; '.join(f'rank {m}: {nf(x)} cumecs' for m, x in zip(ranks, q)) + '.')
    if D == 1:
        return MCQ(r, intro + f' What is the recurrence interval of the flood ranked {ranks[0]}?', f'{s3(ri[0])} years',
                   [f'{s3(n / ranks[0] / 2)} years', f'{s3(ranks[0] / (n + 1))} years', f'{s3((n - 1) / ranks[0])} years' if ranks[0] > 1 else f'{n + 2} years', f'{s3(ri[0] * 2)} years'],
                   f'({n} + 1) ÷ {ranks[0]} = {s3(ri[0])} years. [1]')
    i = r.randrange(4)
    parts = [
        L(f'Calculate the recurrence interval of the flood of {nf(q[i])} cumecs.', f'{s3(ri[i])} years', f'({n} + 1) ÷ {ranks[i]} = {s3(ri[i])} years [1]'),
        L(f'Calculate the probability that a flood at least as large as {nf(q[i])} cumecs occurs in any one year.', f'{s3(1 / ri[i])} ({s3(100 / ri[i])}%)', f'1 ÷ {s3(ri[i])} = {s3(1 / ri[i])} [1]'),
        L(f'Calculate the probability that at least one flood of this size occurs in the next 10 years.', s3(1 - (1 - 1 / ri[i]) ** 10), f'1 − (1 − {s3(1 / ri[i])})¹⁰ [1] = {s3(1 - (1 - 1 / ri[i]) ** 10)} [1] [2]'),
        L('Explain why recurrence intervals should be used with caution when planning flood defences.', 'The record may be short; climate change and land-use change alter flood frequency; a 1-in-100-year flood can occur in consecutive years.', '1 mark per point up to [2]'),
    ]
    return comp(r, intro, parts, D)


@h4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def h4_hydro(r, D):
    rain_t = r.choice([6, 8, 9, 10, 12])
    lag = r.choice([4, 6, 8, 10, 14, 18, 24])
    base = r.randint(5, 20)
    peak = base + r.randint(20, 120)
    basin = r.choice(['an urban catchment', 'a rural catchment', 'a small upland basin', 'a catchment in ' + city(r)])
    intro = (f'A flood hydrograph for {basin} shows peak rainfall at {rain_t:02d}:00 on day 1 and peak discharge of {peak} cumecs at {(rain_t + lag) % 24:02d}:00'
             f'{" on day 2" if rain_t + lag >= 24 else " on day 1"}. Base flow before the storm was {base} cumecs.')
    if D == 1:
        return MCQ(r, intro + ' What is the lag time?', f'{lag} hours', [f'{lag + 2} hours', f'{rain_t + lag} hours', f'{max(1, lag - 3)} hours', f'{lag * 2} hours'], f'{lag} hours from peak rainfall to peak discharge. [1]')
    parts = [
        L('State the lag time.', f'{lag} hours', '[1]'),
        L('Calculate the rise in discharge from base flow to peak.', f'{peak - base} cumecs', f'{peak} − {base} = {peak - base} [1]'),
        L(f'Suggest whether this is ' + ('a flashy or a subdued' if r.random() < 0.5 else 'a short or a long lag') + ' response and give reasons.',
          ('A flashy response with a short lag: likely urban, steep or saturated, impermeable ground.' if lag <= 8 else 'A subdued response with a longer lag: likely forested, gentle slopes and permeable rock or soils.'), 'judgement [1]; reasons [1] [2]'),
        L('Explain how afforestation of the basin would change the hydrograph.', 'Interception and infiltration increase, so less surface runoff; lag time increases and peak discharge falls.', 'process [1]; longer lag and lower peak [1] [2]'),
    ]
    return comp(r, intro, parts, D)


CHAPTERS[2] = [h1, h2, h3, h4]


# ============================================================== CHAPTER 3: Atmosphere

a1 = T('Structure and composition of the atmosphere', 'structure and composition of the atmosphere', 'composition of the atmosphere')
build(a1, {
    'terms': [
        ('troposphere', 'the lowest layer of the atmosphere, up to about 8-17 km, where temperature falls with height and weather occurs'),
        ('stratosphere', 'the layer above the troposphere, to about 50 km, where temperature rises with height because ozone absorbs ultraviolet radiation'),
        ('mesosphere', 'the layer from about 50 to 80 km in which temperature falls with height to the coldest part of the atmosphere'),
        ('thermosphere', 'the outermost layer above about 80 km, where temperature rises with height as gases absorb high-energy solar radiation'),
        ('tropopause', 'the boundary between the troposphere and stratosphere, where temperature stops falling with height'),
        ('environmental lapse rate', 'the rate at which air temperature falls with height in the troposphere, on average about 6.5 °C per km'),
        ('albedo', 'the proportion of incoming solar radiation reflected by a surface'),
        ('ozone layer', 'the region of the stratosphere, about 15-35 km up, with a relatively high concentration of ozone that absorbs ultraviolet radiation'),
    ],
    'mcq': [
        ('Which gas makes up about 78% of dry air by volume?', 'Nitrogen', ['Oxygen', 'Argon', 'Carbon dioxide'], 'N₂ 78%, O₂ 21%, Ar 0.93%, CO₂ about 0.04%. [1]'),
        ('In which layer does almost all weather occur?', 'Troposphere', ['Stratosphere', 'Mesosphere', 'Thermosphere'], '[1]'),
        ('Why does temperature increase with height in the stratosphere?', 'Ozone absorbs ultraviolet radiation', ['It is closer to the Sun', 'Clouds trap heat', 'Air pressure increases'], '[1]'),
        ('About what percentage of the atmosphere’s mass lies in the troposphere?', 'About 75-80%', ['About 10%', 'About 50%', 'About 99.9%'], 'Air is compressed by gravity near the surface. [1]'),
        ('Which surface has the highest albedo?', 'Fresh snow', ['Tropical forest', 'Ocean', 'Tarmac'], 'Fresh snow reflects about 80-90%. [1]'),
        ('The concentration of carbon dioxide in the atmosphere in 2023 was about', '420 ppm', ['280 ppm', '42 ppm', '4200 ppm'], 'Pre-industrial about 280 ppm. [1]'),
    ],
    'explain': [
        ('Explain why temperature decreases with height in the troposphere.', 'The atmosphere is heated mainly from below by the ground, which absorbs solar radiation and emits infrared; air further from the surface receives less heat, and rising air expands and cools as pressure falls.', 'heated from the ground [1]; expansion / lower pressure [1] [2]'),
        ('Describe how the composition of the atmosphere has changed since 1750.', 'Carbon dioxide has risen from about 280 to over 420 ppm; methane has more than doubled; nitrous oxide has increased; new gases such as CFCs have been added; stratospheric ozone was depleted.', '1 mark per change, with data up to [3]'),
        ('Explain the importance of the atmosphere for life on Earth.', 'It supplies oxygen for respiration and carbon dioxide for photosynthesis; the ozone layer absorbs harmful UV; the greenhouse effect keeps the mean temperature about 33 °C warmer; it redistributes heat and water.', '1 mark per point up to [3]'),
        ('Explain why the height of the tropopause is greater at the equator than at the poles.', 'Strong heating at the equator causes vigorous convection, which lifts air to greater heights (about 17 km) than over the cold poles (about 8 km).', 'stronger heating / convection at equator [1]; greater height [1] [2]'),
    ],
    'claims': [
        ('The atmosphere gets thinner with height.', True, 'Air pressure and density fall with altitude because gravity holds most of the air near the surface.'),
        ('Oxygen is the most abundant gas in the atmosphere.', False, 'Nitrogen is the most abundant (about 78%); oxygen is about 21%.'),
        ('Water vapour is a greenhouse gas.', True, 'It absorbs infrared radiation and is the largest contributor to the natural greenhouse effect.'),
    ],
    'essays': [
        ('the composition of the atmosphere is now controlled more by human activities than by natural processes',
         ['Burning fossil fuels and deforestation have raised CO₂ by about 50%; methane from agriculture has more than doubled; CFCs damaged the ozone layer.'],
         ['Nitrogen, oxygen and argon (over 99% of dry air) are controlled by natural cycles; volcanic eruptions and photosynthesis still dominate many fluxes.'],
         'Natural processes still control the bulk composition, but human activity now controls the trace gases that matter most for climate and ozone.',
         ['major gases', 'trace gases', 'carbon cycle']),
    ],
})
compare_item(a1, [
    ('the troposphere', 'the stratosphere', 'Temperature falls with height in the troposphere but rises in the stratosphere; the troposphere contains weather and most water vapour, while the stratosphere is dry, stable and contains the ozone layer.', 'Both contain the same main gases, nitrogen and oxygen.'),
])

PEAKS = [('Mount Kilimanjaro', 5895), ('Mount Kenya', 5199), ('Aconcagua', 6961), ('Mont Blanc', 4806), ('Mount Fuji', 3776), ('Mount Kinabalu', 4095), ('Huascarán', 6768), ('Mount Everest', 8849)]


@a1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def a1_lapse(r, D):
    peak, h = r.choice(PEAKS)
    base = r.choice([500, 800, 1000, 1200, 1500, 2000])
    tb = r.randint(14, 30)
    lr = 6.5
    tt = tb - lr * (h - base) / 1000
    intro = f'At a town at the foot of {peak} ({nf(base)} m above sea level) the air temperature is {tb} °C. The summit is {nf(h)} m above sea level. Assume an environmental lapse rate of 6.5 °C per 1000 m.'
    if D == 1:
        return MCQ(r, intro + ' What is the expected temperature at the summit?', f'{f1(tt)} °C',
                   [f'{f1(tb - lr * h / 1000)} °C', f'{f1(tb - (h - base) / 100)} °C', f'{f1(tb + lr * (h - base) / 1000)} °C', f'{f1(tb - 6.5)} °C'],
                   f'{tb} − 6.5 × ({nf(h)} − {nf(base)}) ÷ 1000 = {f1(tt)} °C. [1]')
    parts = [
        L('Calculate the expected temperature at the summit.', f'{f1(tt)} °C', f'height difference {nf(h - base)} m [1]; {tb} − 6.5 × {fmt((h - base) / 1000, 3)} = {f1(tt)} °C [1] [2]'),
        L('Calculate the height above sea level at which the temperature would be 0 °C.', f'{nf(base + tb / lr * 1000)} m', f'{tb} ÷ 6.5 × 1000 = {nf(tb / lr * 1000)} m above the town [1]; + {nf(base)} = {nf(base + tb / lr * 1000)} m [1] [2]'),
        L('Explain why air temperature falls with height in the troposphere.', 'The troposphere is heated from the ground; air pressure falls with height, so air expands and cools.', 'heated from below [1]; expansion with lower pressure [1] [2]'),
        L('Suggest why the actual temperature at the summit may differ from your calculation.', 'The lapse rate varies with humidity, time of day, cloud and weather; temperature inversions may occur; wind and aspect affect local temperature.', '1 mark per reason up to [2]'),
    ]
    return comp(r, intro, parts, D)


@a1.add('C3', (1, 2, 3), 'numerical')
def a1_comp(r, D):
    gases = [('nitrogen', 78.08), ('oxygen', 20.95), ('argon', 0.93)]
    vol = r.choice([5, 10, 20, 50, 250, 500, 1000])
    room = r.choice(['a classroom', 'a laboratory', 'a greenhouse', 'a bedroom', 'a hall'])
    g, p = r.choice(gases)
    v = vol * p / 100
    if r.random() < 0.4:
        ppm = r.choice([415, 420, 425])
        v = vol * ppm / 1e6 * 1000   # litres
        stem = f'{cap(room)} contains {vol} m³ of air with a carbon dioxide concentration of {ppm} ppm. What volume of carbon dioxide, in litres, does it contain?'
        return MCQ(r, stem, f'{s3(v)} l', [f'{s3(v * 10)} l', f'{s3(v / 10)} l', f'{s3(v * 1000)} l', f'{s3(v / 1000)} l'], f'{vol} × {ppm} ÷ 1 000 000 = {s3(v / 1000)} m³ = {s3(v)} l. [1]')
    stem = f'{cap(room)} contains {vol} m³ of dry air. Dry air is {p}% {g} by volume. What volume of {g} is present?'
    return MCQ(r, stem, f'{s3(v)} m³', [f'{s3(v * 10)} m³', f'{s3(v / 10)} m³', f'{s3(vol * (100 - p) / 100)} m³', f'{s3(v * 2)} m³'], f'{vol} × {p} ÷ 100 = {s3(v)} m³. [1]')


a2 = T('Atmospheric circulation, weather and climate: tricellular model', 'atmospheric circulation', 'tricellular model', 'weather and climate')
build(a2, {
    'terms': [
        ('Hadley cell', 'the circulation cell between the equator and about 30° latitude, with rising air at the equator and sinking air in the subtropics'),
        ('Ferrel cell', 'the middle-latitude circulation cell, between about 30° and 60°, driven by the Hadley and polar cells'),
        ('polar cell', 'the circulation cell between about 60° and the poles, with cold air sinking at the poles'),
        ('Intertropical Convergence Zone (ITCZ)', 'the low-pressure belt near the equator where the trade winds meet and air rises, giving heavy convectional rain'),
        ('trade winds', 'the steady surface winds blowing from the subtropical high-pressure belts towards the equator'),
        ('Coriolis effect', 'the deflection of moving air and water by the Earth’s rotation, to the right in the northern hemisphere and to the left in the southern'),
        ('weather', 'the state of the atmosphere at a particular place and time'),
        ('climate', 'the average weather conditions of a place, usually over at least 30 years'),
    ],
    'mcq': [
        ('At about which latitude do the major hot deserts occur?', '30° north and south', ['0°', '60° north and south', '90° north and south'], 'Sinking air of the Hadley cell gives high pressure. [1]'),
        ('Air at the ITCZ', 'rises, causing low pressure and heavy rain', ['sinks, causing high pressure', 'is cold and dry', 'moves towards the poles at the surface'], '[1]'),
        ('Why does the equator receive more solar energy per square metre than the poles?', 'The Sun’s rays strike the surface at a higher angle and are concentrated on a smaller area', ['The equator is nearer the Sun', 'The equator has more cloud', 'The poles reflect no light'], '[1]'),
        ('The westerly winds of the mid-latitudes are part of which cell?', 'Ferrel cell', ['Hadley cell', 'Polar cell', 'Walker cell'], '[1]'),
        ('The seasonal reversal of winds that brings heavy summer rain to South Asia is called', 'the monsoon', ['El Niño', 'the jet stream', 'a temperature inversion'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of the Hadley cell.', 'Intense heating at the equator causes air to rise (low pressure, ITCZ); it cools and moves polewards at high altitude; it sinks at about 30°, forming high pressure; surface trade winds return air to the equator.', 'rising at equator [1]; poleward flow aloft [1]; sinking at 30° [1]; trade winds return [1] [4]'),
        ('Explain why the tropical rainforest has high rainfall throughout the year.', 'Strong heating causes convection; air rises at the ITCZ, cools, water vapour condenses and heavy convectional rain falls most afternoons; the ITCZ stays close to the equator.', 'heating / rising air [1]; condensation [1]; ITCZ position [1] [3]'),
        ('Explain how the movement of the ITCZ causes wet and dry seasons in the savanna.', 'The ITCZ follows the overhead Sun; when it moves over the savanna, rising air brings rain (wet season); when it moves away, subtropical high pressure brings sinking, dry air (dry season).', 'ITCZ follows overhead sun [1]; rain when overhead [1]; high pressure / dry when away [1] [3]'),
        ('Explain why the tricellular model is a simplification.', 'Real circulation is affected by the distribution of land and sea, mountains, seasonal shifts, jet streams, monsoons and ocean currents; cells vary in position and strength.', '1 mark per point up to [2]'),
    ],
    'claims': [
        ('The tricellular model explains why the world’s hot deserts are found near the equator.', False, 'Hot deserts are found at about 30°, where air sinks in the subtropical high-pressure belt.'),
        ('Climate is the average weather over a long period.', True, 'Usually calculated over at least 30 years.'),
        ('The Coriolis effect makes winds blow straight from high to low pressure.', False, 'The Coriolis effect deflects winds, so they blow at an angle, e.g. the north-east and south-east trade winds.'),
    ],
    'cases': [(
        ['Fig. 3.2 shows the tricellular model of atmospheric circulation, with the Hadley, Ferrel and polar cells and the main pressure belts and surface winds.',
         'A student in {c} is comparing climate graphs for Manaus (3° S, tropical rainforest), Kano (12° N, savanna) and Riyadh (25° N, hot desert).'],
        [('Describe the pattern of pressure at the surface from the equator to 30° N.', 'Low pressure at the equator (ITCZ), rising to high pressure at about 30° N (subtropical high).', '[2]'),
         ('Explain why Manaus has high rainfall all year.', 'It lies near the ITCZ all year; intense heating causes rising air, condensation and convectional rain.', '[2]'),
         ('Explain why Riyadh receives very little rain.', 'It lies under the descending limb of the Hadley cell; sinking air warms and is dry, giving high pressure and clear skies.', '[2]'),
         ('Explain the seasonal pattern of rainfall in Kano.', 'Rain falls in summer when the ITCZ moves north over the area; in winter the ITCZ moves south and dry north-east trade winds (the Harmattan) bring a dry season.', '[3]'),
         ('Suggest one limitation of the tricellular model.', 'It ignores the effects of land and sea, mountains, seasonal shifts and monsoons.', '[1]')])],
    'essays': [
        ('the tricellular model explains the distribution of the world’s climates',
         ['It explains the wet equatorial belt (ITCZ), subtropical deserts at 30°, wet mid-latitudes with westerly winds and polar highs.'],
         ['It ignores monsoons, ocean currents (cold currents creating coastal deserts such as the Atacama), altitude, continentality and seasonal shifts; real cells are not continuous bands.'],
         'The model explains the broad zonal pattern but must be combined with other factors to explain regional climates.',
         ['latitude', 'ocean currents', 'monsoons', 'relief']),
    ],
})


@a2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def a2_climate(r, D):
    stations = {
        'Manaus (3° S)': ([26.5, 26.4, 26.6, 26.7, 26.8, 26.9, 27.0, 27.6, 28.0, 27.8, 27.4, 26.9], [264, 279, 300, 287, 193, 99, 61, 41, 62, 112, 165, 220]),
        'Kano (12° N)': ([21.7, 24.4, 28.4, 31.1, 30.7, 28.3, 26.1, 25.3, 26.5, 27.1, 24.6, 22.1], [0, 0, 2, 8, 70, 117, 206, 268, 128, 14, 0, 0]),
        'Riyadh (25° N)': ([14.6, 17.0, 21.0, 26.6, 32.4, 34.8, 36.1, 35.7, 32.7, 27.5, 20.8, 16.0], [15, 8, 21, 25, 7, 0, 0, 0, 0, 1, 7, 14]),
        'London (51° N)': ([5.2, 5.3, 7.6, 9.9, 13.3, 16.5, 18.7, 18.5, 15.7, 12.0, 8.0, 5.5], [55, 41, 42, 44, 49, 45, 45, 50, 49, 69, 59, 55]),
        'Darwin (12° S)': ([28.6, 28.3, 28.3, 28.4, 27.3, 25.6, 25.1, 26.1, 28.0, 29.1, 29.4, 29.1], [427, 374, 317, 102, 21, 2, 1, 5, 15, 71, 141, 252]),
    }
    name = r.choice(list(stations))
    Tm, Pm = stations[name]
    mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    rng = max(Tm) - min(Tm)
    tot = sum(Pm)
    intro = f'Climate data for {name}: mean monthly temperature (°C) ' + ', '.join(f'{m} {fmt(t, 1)}' for m, t in zip(mon, Tm)) + '; mean monthly rainfall (mm) ' + ', '.join(f'{m} {p}' for m, p in zip(mon, Pm)) + '.'
    if D == 1:
        return MCQ(r, intro + ' What is the annual temperature range?', f'{f1(rng)} °C', [f'{f1(max(Tm))} °C', f'{f1(sum(Tm) / 12)} °C', f'{f1(rng + 2)} °C', f'{f1(max(Tm) + min(Tm))} °C'], f'{fmt(max(Tm), 1)} − {fmt(min(Tm), 1)} = {f1(rng)} °C. [1]')
    wet = [m for m, p in zip(mon, Pm) if p >= 60]
    expl = {'Manaus (3° S)': 'Near the equator the ITCZ is overhead or close all year, so rising air gives convectional rain; high sun all year keeps temperatures high and the range small.',
            'Kano (12° N)': 'The ITCZ moves north over Kano in summer, bringing rain; in winter it moves south and dry winds from the Sahara give a long dry season.',
            'Riyadh (25° N)': 'Riyadh lies under the subtropical high-pressure belt where air from the Hadley cell sinks, so it is very dry with hot summers.',
            'London (51° N)': 'London lies in the mid-latitudes with westerly winds and depressions from the Atlantic, giving rain all year; the ocean moderates the temperature range.',
            'Darwin (12° S)': 'The ITCZ and monsoon move south over northern Australia in the southern summer (Dec-Mar), bringing heavy rain; in winter dry south-east trade winds dominate.'}[name]
    parts = [
        L('Calculate the annual temperature range.', f'{f1(rng)} °C', f'{fmt(max(Tm), 1)} − {fmt(min(Tm), 1)} = {f1(rng)} °C [1]'),
        L('Calculate the total annual rainfall.', f'{nf(tot)} mm', f'sum of 12 months = {nf(tot)} mm [1]'),
        L('Calculate the percentage of the annual rainfall that falls in the three wettest months.', f'{f1(sum(sorted(Pm)[-3:]) / tot * 100)}%', f'{sum(sorted(Pm)[-3:])} ÷ {tot} × 100 = {f1(sum(sorted(Pm)[-3:]) / tot * 100)}% [2]'),
        L('Describe the pattern of rainfall through the year.', (f'Wetter months (60 mm or more): {", ".join(wet)}; ' if wet else 'No month has 60 mm or more; ') + f'wettest {mon[Pm.index(max(Pm))]} ({max(Pm)} mm), driest {mon[Pm.index(min(Pm))]} ({min(Pm)} mm).', 'pattern [1]; data [1] [2]'),
        L('Use atmospheric circulation to explain the climate of this place.', expl, 'pressure belt / ITCZ or westerlies [1]; link to rainfall [1]; link to temperature [1] [3]'),
    ]
    return comp(r, intro, parts, D)


a3 = T('The enhanced greenhouse effect and climate change: causes, impacts and responses', 'enhanced greenhouse effect', 'climate change')
build(a3, {
    'terms': [
        ('greenhouse effect', 'the natural warming of the Earth as greenhouse gases absorb and re-emit infrared radiation from the surface'),
        ('enhanced greenhouse effect', 'the extra warming caused by increased concentrations of greenhouse gases from human activities'),
        ('global warming potential (GWP)', 'a measure of how much heat a greenhouse gas traps over a period (usually 100 years) compared with the same mass of carbon dioxide'),
        ('mitigation', 'actions that reduce greenhouse gas emissions or remove them from the atmosphere to limit climate change'),
        ('adaptation', 'actions that reduce the harmful effects of climate change, such as sea walls or drought-resistant crops'),
        ('carbon sink', 'a store that absorbs more carbon than it releases, such as forests and oceans'),
        ('positive feedback', 'a process in which a change causes further change in the same direction, such as melting ice lowering albedo and causing more warming'),
        ('carbon capture and storage', 'trapping carbon dioxide from power stations or industry and storing it underground'),
    ],
    'mcq': [
        ('Which greenhouse gas is released by rice paddies and cattle?', 'Methane', ['Carbon dioxide', 'Nitrous oxide', 'Sulfur dioxide'], '[1]'),
        ('Which radiation do greenhouse gases absorb?', 'Infrared (long-wave) radiation emitted by the Earth', ['Ultraviolet from the Sun', 'Visible light only', 'Gamma rays'], '[1]'),
        ('Which is an adaptation to climate change?', 'Building higher sea walls', ['Switching to wind power', 'Planting forests to absorb CO₂', 'Taxing carbon emissions'], 'The others are mitigation. [1]'),
        ('Global mean surface temperature in 2011-2020 was about how much higher than in 1850-1900?', '1.1 °C', ['0.1 °C', '4 °C', '11 °C'], 'IPCC AR6. [1]'),
        ('Which international agreement aims to keep warming well below 2 °C and pursue 1.5 °C?', 'The Paris Agreement (2015)', ['The Montreal Protocol (1987)', 'The Kyoto Protocol (1997)', 'CITES (1973)'], '[1]'),
        ('Thermal expansion contributes to sea level rise because', 'water expands as it warms', ['sea ice melts', 'it increases rainfall', 'land rises'], 'Melting floating sea ice does not raise sea level. [1]'),
    ],
    'explain': [
        ('Explain how the greenhouse effect warms the Earth.', 'Short-wave solar radiation passes through the atmosphere and heats the surface; the surface emits long-wave infrared radiation; greenhouse gases absorb it and re-emit some back towards the surface, keeping the lower atmosphere warmer.', 'short-wave in [1]; long-wave out [1]; absorption and re-emission [1] [3]'),
        ('Explain two positive feedback mechanisms that could accelerate global warming.', 'Melting ice and snow expose darker surfaces with lower albedo, absorbing more heat; thawing permafrost releases methane and CO₂; warmer air holds more water vapour, a greenhouse gas; warmer oceans absorb less CO₂.', '1 mark per mechanism, 1 mark per explanation [4]'),
        ('Explain why low-lying coastal countries are vulnerable to climate change.', 'Sea level rise causes flooding, coastal erosion and saltwater intrusion into farmland and aquifers; stronger storms increase storm surges; e.g. Bangladesh, the Maldives.', '1 mark per point up to [3]'),
        ('Describe the evidence that the climate is changing.', 'Rising global temperatures in instrumental records; shrinking glaciers and Arctic sea ice; rising sea level; ice cores showing CO₂ and temperature; changes in species ranges and earlier spring events.', '1 mark per piece of evidence up to [3]'),
        ('Explain why it is difficult to reach international agreement on reducing emissions.', 'Countries differ in responsibility and wealth; emerging economies want to develop; fossil-fuel exporters lose income; costs are immediate but benefits are long-term and shared (free-rider problem); enforcement is weak.', '1 mark per point up to [3]'),
    ],
    'claims': [
        ('The greenhouse effect is entirely harmful.', False, 'The natural greenhouse effect keeps the Earth about 33 °C warmer than it would be, making life possible; the problem is the enhanced effect.'),
        ('Methane is a more powerful greenhouse gas than carbon dioxide per molecule.', True, 'Its global warming potential is about 28-30 times that of CO₂ over 100 years, though it stays in the atmosphere for a shorter time.'),
        ('The hole in the ozone layer is the main cause of global warming.', False, 'Ozone depletion and global warming are different problems; warming is caused mainly by increased greenhouse gases.'),
        ('Climate change will affect all regions equally.', False, 'The Arctic is warming much faster than average; some regions will get wetter and others drier; poorer countries are often more vulnerable.'),
    ],
    'cs': [('a country vulnerable to climate change', [
        ('Bangladesh', {
            'impacts': 'Much of the country is less than 10 m above sea level; sea level rise and stronger cyclones increase storm surges; saltwater intrusion damages rice fields and drinking water; more intense monsoon floods; millions may be displaced by 2050.',
            'management': 'Over 4000 cyclone shelters and an early warning system have cut cyclone deaths dramatically; floating gardens and salt-tolerant rice; embankments; the Bangladesh Delta Plan 2100.'}),
        ('the Maldives', {
            'impacts': 'About 80% of land is less than 1 m above sea level; sea level rise threatens to submerge islands; coral bleaching damages reefs that protect islands and support tourism and fishing; freshwater lenses become salty.',
            'management': 'A sea wall around the capital Malé; the artificial raised island of Hulhumalé; coral restoration; the government campaigns internationally for deep emissions cuts.'}),
    ], [
        ('describe the impacts of climate change on the country', 'impacts', 'sea level, storms, flooding, agriculture, water, with data'),
        ('evaluate the strategies used to respond to climate change', 'management', 'adaptation (and mitigation) measures; success and limits; judgement'),
    ])],
    'essays': [
        ('adaptation is now more important than mitigation in responding to climate change',
         ['Some warming is already locked in, so sea walls, drought-resistant crops and early warning systems (Bangladesh) are urgently needed to protect people now.'],
         ['Without mitigation (renewables, efficiency, forest protection) warming could exceed 3 °C and overwhelm adaptation; mitigation addresses the cause and is cheaper in the long term.'],
         'Both are essential: mitigation limits future damage while adaptation manages unavoidable impacts, especially in vulnerable countries.',
         ['the Paris Agreement', 'costs', 'vulnerable countries']),
        ('the impacts of climate change will be greater for low-income countries than for high-income countries',
         ['Low-income countries depend on rain-fed farming, have less money for defences and are often in hot or low-lying regions (the Sahel, Bangladesh).'],
         ['High-income countries also face severe heatwaves, wildfires and floods (Europe 2021, Australia 2019-20); some high-latitude areas may benefit from longer growing seasons.'],
         'Impacts are global, but vulnerability and capacity to adapt make them most severe for low-income countries.',
         ['agriculture', 'sea level rise', 'capacity to adapt']),
    ],
})
compare_item(a3, [
    ('mitigation', 'adaptation', 'Mitigation reduces the cause by cutting emissions or increasing sinks (e.g. renewable energy, afforestation); adaptation reduces the harmful effects (e.g. sea walls, drought-resistant crops).', 'Both are responses to climate change that need investment and planning.'),
    ('the natural greenhouse effect', 'the enhanced greenhouse effect', 'The natural effect keeps Earth habitable at about 15 °C; the enhanced effect is the additional warming from human emissions of CO₂, methane and other gases.', 'Both involve greenhouse gases absorbing infrared radiation.'),
])

CO2 = [(1960, 317), (1970, 326), (1980, 339), (1990, 354), (2000, 370), (2010, 390), (2020, 414), (2023, 421)]


@a3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def a3_co2(r, D):
    pts = sorted(r.sample(CO2, 3))
    intro = 'Atmospheric carbon dioxide concentrations measured at Mauna Loa, Hawaii (annual means, ppm): ' + ', '.join(f'{y}: {c}' for y, c in pts) + '. The pre-industrial concentration was about 280 ppm.'
    (y0, c0), (y1, c1), (y2, c2) = pts
    if D == 1:
        return MCQ(r, intro + f' What is the percentage increase from {y0} to {y2}?', f'{f1(pc(c0, c2))}%', [f'{f1(c2 - c0)}%', f'{f1(pc(c2, c0) * -1)}%', f'{f1(pc(280, c2))}%', f'{f1(pc(c0, c2) / 2)}%'],
                   f'({c2} − {c0}) ÷ {c0} × 100 = {f1(pc(c0, c2))}%. [1]')
    r1 = (c1 - c0) / (y1 - y0)
    r2 = (c2 - c1) / (y2 - y1)
    target = 450
    yrs = (target - c2) / r2 if r2 > 0 else None
    parts = [
        L(f'Calculate the percentage increase from {y0} to {y2}.', f'{f1(pc(c0, c2))}%', f'({c2} − {c0}) ÷ {c0} × 100 [1] = {f1(pc(c0, c2))}% [1] [2]'),
        L(f'Calculate the mean rate of increase in ppm per year for {y0}-{y1} and for {y1}-{y2}.', f'{f2(r1)} and {f2(r2)} ppm per year', f'{c1 - c0} ÷ {y1 - y0} = {f2(r1)} [1]; {c2 - c1} ÷ {y2 - y1} = {f2(r2)} [1] [2]'),
        L('Describe what your answers show about the trend.', ('The concentration is rising and the rate of increase is accelerating.' if r2 > r1 else 'The concentration is rising, though not faster in the later period.'), '[1]'),
        L(f'Assuming the {y1}-{y2} rate continues, estimate the year in which the concentration will reach 450 ppm.', f'about {round(y2 + yrs)}' if yrs else 'not reached', f'(450 − {c2}) ÷ {f2(r2)} = {s3(yrs) if yrs else "-"} years [1]; year ≈ {round(y2 + yrs) if yrs else "-"} [1] [2]'),
        L(f'Calculate the increase above the pre-industrial level in {y2} as a percentage.', f'{f1(pc(280, c2))}%', f'({c2} − 280) ÷ 280 × 100 = {f1(pc(280, c2))}% [1]'),
        L('Explain why carbon dioxide concentrations have increased.', 'Burning of fossil fuels for energy, transport and industry; deforestation reduces the carbon sink and releases stored carbon; cement production.', '1 mark per cause up to [2]'),
    ]
    return comp(r, intro, parts, D)


@a3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def a3_percap(r, D):
    data = [('China', 11400, 1412), ('USA', 5000, 333), ('India', 2800, 1417), ('Germany', 670, 84), ('Brazil', 480, 215), ('Nigeria', 130, 218),
            ('Australia', 390, 26), ('Qatar', 100, 2.7), ('Indonesia', 620, 276), ('United Kingdom', 330, 67), ('Saudi Arabia', 650, 36), ('Bangladesh', 100, 171)]
    rows = r.sample(data, 3 if D <= 3 else 4)
    pcap = [(n, e / p) for n, e, p in rows]
    intro = 'Table 3.3 shows annual carbon dioxide emissions (million tonnes) and population (millions) for selected countries (2022 estimates): ' + '; '.join(f'{n} {nf(e)} Mt, {fmt(p, 1)} million' for n, e, p in rows) + '.'
    hi = max(pcap, key=lambda x: x[1])
    lo = min(pcap, key=lambda x: x[1])
    if D == 1:
        n, e, p = rows[0]
        return MCQ(r, intro + f' What are the emissions per person in {n}?', f'{s3(e / p)} t', [f'{s3(e / p * 10)} t', f'{s3(p / e)} t', f'{s3(e / p / 10)} t', f'{s3(e * p / 1000)} t'], f'{nf(e)} ÷ {fmt(p, 1)} = {s3(e / p)} tonnes per person. [1]')
    parts = [
        L('Calculate the emissions per person (tonnes) for each country.', '; '.join(f'{n} {s3(v)} t' for n, v in pcap), 'emissions ÷ population [1]; all correct [1] [2]'),
        L('Identify the country with the highest emissions per person and suggest reasons.', f'{hi[0]} ({s3(hi[1])} t): high incomes and energy use, reliance on fossil fuels (coal or oil and gas), car use, energy-intensive industry or air conditioning.', 'country [1]; reasons [1] [2]'),
        L('Explain why total emissions and emissions per person give different pictures of responsibility.', f'Large-population countries such as {max(rows, key=lambda x: x[2])[0]} have high totals, but per person emissions may be low; small wealthy countries may have high per-person emissions but small totals.', '[2]'),
        L(f'Suggest why {lo[0]} has low emissions per person.', 'Lower incomes and energy use per person, less industry and car ownership, and in some cases more renewable energy.', '[2]'),
    ]
    return comp(r, intro, parts, D)


a4 = T('Ozone depletion: causes, impacts and the Montreal Protocol', 'ozone depletion', 'montreal protocol')
build(a4, {
    'terms': [
        ('ozone', 'a gas made of molecules of three oxygen atoms (O₃) that absorbs ultraviolet radiation in the stratosphere'),
        ('chlorofluorocarbons (CFCs)', 'stable compounds of chlorine, fluorine and carbon once used in aerosols, refrigerators and foams, which destroy stratospheric ozone'),
        ('ozone hole', 'an area of severe seasonal thinning of the ozone layer, mainly over Antarctica in spring'),
        ('Dobson unit', 'the unit used to measure the total amount of ozone in a column of the atmosphere'),
        ('Montreal Protocol', 'the 1987 international agreement to phase out the production of ozone-depleting substances'),
        ('ultraviolet radiation', 'high-energy solar radiation with a shorter wavelength than visible light, which can damage living cells'),
        ('polar stratospheric clouds', 'very cold clouds in the polar stratosphere on whose surfaces chlorine is converted to forms that destroy ozone in spring'),
        ('hydrofluorocarbons (HFCs)', 'replacements for CFCs that do not destroy ozone but are powerful greenhouse gases, phased down by the Kigali Amendment (2016)'),
    ],
    'mcq': [
        ('Which element released from CFCs destroys ozone?', 'Chlorine', ['Fluorine', 'Carbon', 'Nitrogen'], 'One chlorine atom can destroy thousands of ozone molecules. [1]'),
        ('The ozone hole is largest over Antarctica in', 'September-October (southern spring)', ['June-July', 'December-January', 'March-April'], '[1]'),
        ('Which health effect is linked to increased UV-B radiation?', 'Skin cancer and cataracts', ['Asthma', 'Malaria', 'Lead poisoning'], '[1]'),
        ('Why are CFCs able to reach the stratosphere?', 'They are very stable and unreactive in the troposphere', ['They are lighter than hydrogen', 'They are produced in the stratosphere', 'They dissolve in rain'], '[1]'),
        ('The Montreal Protocol is regarded as successful because', 'production of ozone-depleting substances fell by about 99%', ['the ozone hole disappeared in 1990', 'it stopped climate change', 'it banned all greenhouse gases'], '[1]'),
    ],
    'explain': [
        ('Explain how CFCs cause ozone depletion.', 'CFCs drift into the stratosphere where UV breaks them down, releasing chlorine atoms; chlorine reacts with ozone (Cl + O₃ → ClO + O₂) and is regenerated, so a single atom destroys many ozone molecules.', 'UV breaks CFC [1]; chlorine released [1]; catalytic chain reaction [1] [3]'),
        ('Explain why ozone depletion is greatest over Antarctica.', 'Very cold winter temperatures form polar stratospheric clouds; reactions on their surfaces convert chlorine into reactive forms; when sunlight returns in spring, rapid ozone destruction occurs; the polar vortex isolates the air.', 'cold / clouds [1]; chlorine activated [1]; spring sunlight / vortex [1] [3]'),
        ('Explain why the Montreal Protocol was more successful than climate agreements.', 'Few industries were affected and substitutes (HCFCs, HFCs) were available; the science and harm were clear; developing countries received funding and longer timetables; trade restrictions encouraged compliance.', '1 mark per reason up to [3]'),
        ('Describe the impacts of ozone depletion on ecosystems.', 'More UV-B damages phytoplankton, reducing productivity at the base of marine food chains; damages DNA in plants and animals; reduces crop yields; harms amphibian eggs.', '1 mark per impact up to [2]'),
    ],
    'claims': [
        ('The ozone layer is expected to recover by the middle of this century.', True, 'Scientists predict recovery to 1980 levels by about 2066 over Antarctica and about 2040 elsewhere because of the Montreal Protocol.'),
        ('CFC replacements such as HFCs are harmless to the environment.', False, 'HFCs do not deplete ozone but are powerful greenhouse gases, so the Kigali Amendment phases them down.'),
        ('Ozone at ground level is beneficial.', False, 'Ground-level ozone is a pollutant in photochemical smog that harms lungs and plants; ozone is beneficial in the stratosphere.'),
    ],
    'essays': [
        ('the Montreal Protocol shows that international agreements can solve global environmental problems',
         ['Ratified by all 198 UN members; ozone-depleting substance production fell by about 99%; the ozone layer is recovering; it also avoided warming because CFCs are greenhouse gases.'],
         ['Ozone depletion was easier to solve than climate change: few producers, cheap substitutes and clear evidence; illegal CFC-11 emissions from China were detected in 2018; recovery will take decades.'],
         'It shows that agreements can succeed when science is clear and alternatives exist, but its success may be hard to repeat for more complex problems.',
         ['ratification', 'substitutes', 'climate change comparison']),
    ],
})


@a4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def a4_dobson(r, D):
    base = r.choice([290, 300, 310, 320])
    low = r.choice([95, 110, 120, 140, 160])
    yr_low = r.choice([1994, 1998, 2000, 2006])
    now = r.choice([140, 150, 165, 180])
    intro = (f'Mean minimum total ozone over Antarctica in October was about {base} Dobson units (DU) in the 1970s, fell to {low} DU in {yr_low} and was {now} DU in 2022. '
             'Values below 220 DU are classed as an ozone hole.')
    if D == 1:
        return MCQ(r, intro + f' What is the percentage decrease from the 1970s to {yr_low}?', f'{f1(-pc(base, low))}%', [f'{f1(base - low)}%', f'{f1(low / base * 100)}%', f'{f1(-pc(low, base))}%', f'{f1(-pc(base, now))}%'],
                   f'({base} − {low}) ÷ {base} × 100 = {f1(-pc(base, low))}%. [1]')
    parts = [
        L(f'Calculate the percentage decrease in ozone from the 1970s to {yr_low}.', f'{f1(-pc(base, low))}%', f'({base} − {low}) ÷ {base} × 100 [1] = {f1(-pc(base, low))}% [1] [2]'),
        L(f'Calculate the percentage recovery from {yr_low} to 2022.', f'{f1(pc(low, now))}%', f'({now} − {low}) ÷ {low} × 100 = {f1(pc(low, now))}% [1]'),
        L(f'Recovery is about 1 DU per year on average. Estimate the year in which ozone would return above 220 DU.', f'about {2022 + math.ceil(220 - now)}', f'(220 − {now}) ÷ 1 = {220 - now} years [1]; year {2022 + math.ceil(220 - now)} [1] [2]'),
        L('Explain why the ozone layer is recovering only slowly.', 'CFCs have long atmospheric lifetimes (50-100 years), so chlorine remains in the stratosphere for decades after production stopped.', 'long lifetime [1]; continued chlorine [1] [2]'),
        L('Explain one reason why the minimum value varies from year to year.', 'Stratospheric temperature and the strength of the polar vortex vary; colder winters give more polar stratospheric clouds and more ozone loss; volcanic eruptions add aerosols.', '[1]'),
    ]
    return comp(r, intro, parts, D)


a5 = T('Air pollution: acid rain, photochemical smog and particulates', 'air pollution', 'acid rain', 'photochemical smog', 'particulates')
build(a5, {
    'terms': [
        ('acid rain', 'precipitation with a pH below about 5.6, caused by sulfur dioxide and nitrogen oxides dissolving in water in the atmosphere'),
        ('photochemical smog', 'a brown haze formed when sunlight acts on nitrogen oxides and volatile organic compounds, producing ground-level ozone'),
        ('particulate matter (PM2.5)', 'tiny solid or liquid particles less than 2.5 micrometres across that can enter the lungs and bloodstream'),
        ('temperature inversion', 'a layer of warm air above cooler air near the ground, which traps pollutants'),
        ('flue gas desulfurisation', 'removing sulfur dioxide from power station exhaust, often by reacting it with limestone'),
        ('catalytic converter', 'a device in vehicle exhausts that converts carbon monoxide, nitrogen oxides and unburnt hydrocarbons into less harmful gases'),
        ('liming', 'adding powdered limestone to lakes or soils to neutralise acidity'),
        ('primary pollutant', 'a pollutant emitted directly from a source, such as sulfur dioxide from a power station'),
    ],
    'mcq': [
        ('Which gas is the main cause of acid rain from coal-fired power stations?', 'Sulfur dioxide', ['Carbon monoxide', 'Methane', 'Ozone'], '[1]'),
        ('Which condition makes photochemical smog most likely?', 'Strong sunshine, heavy traffic and a temperature inversion', ['Strong winds and rain', 'Cold, cloudy weather', 'Low traffic and high pressure in winter at night'], '[1]'),
        ('Rain with a pH of 4 is how many times more acidic than rain with a pH of 6?', '100 times', ['2 times', '10 times', '20 times'], 'Each pH unit is a factor of 10. [1]'),
        ('Which city is well known for photochemical smog caused by traffic and a basin location?', 'Los Angeles', ['Reykjavik', 'Wellington', 'Nuuk'], '[1]'),
        ('Ground-level ozone is a', 'secondary pollutant', ['primary pollutant', 'greenhouse gas only', 'harmless gas'], 'Formed by reactions in sunlight. [1]'),
        ('The World Health Organization guideline (2021) for annual mean PM2.5 is', '5 μg/m³', ['50 μg/m³', '500 μg/m³', '0.5 μg/m³'], '[1]'),
    ],
    'explain': [
        ('Explain how acid rain damages forests and lakes.', 'Acid rain leaches nutrients such as calcium and magnesium from soils and releases toxic aluminium, damaging roots and weakening trees; in lakes low pH and aluminium damage fish gills and kill eggs and invertebrates.', 'soil leaching / aluminium [1]; tree damage [1]; aquatic effects [1] [3]'),
        ('Explain why acid rain is a transboundary problem.', 'Pollutants can travel hundreds of kilometres on prevailing winds before falling, so emissions from one country (e.g. the UK) caused acid rain in another (e.g. Scandinavia).', 'long-distance transport [1]; example [1] [2]'),
        ('Explain how a temperature inversion makes air pollution worse.', 'A layer of warm air above cooler air prevents air rising and mixing, so pollutants are trapped near the ground and concentrations build up.', 'warm layer above cool [1]; no vertical mixing / trapping [1] [2]'),
        ('Describe ways in which cities can reduce air pollution from traffic.', 'Low-emission zones and congestion charges; investment in public transport; electric vehicles; catalytic converters and emission standards; restricting vehicles by number plate; cycle lanes.', '1 mark per strategy up to [3]'),
        ('Explain the effects of particulate matter on human health.', 'Fine particles penetrate deep into the lungs and enter the bloodstream, causing asthma, bronchitis, heart disease, lung cancer and premature deaths.', '1 mark per effect up to [2]'),
    ],
    'claims': [
        ('Acid rain has become much less of a problem in Europe and North America since the 1980s.', True, 'Flue gas desulfurisation, low-sulfur fuels, the decline of coal and international agreements reduced SO₂ emissions by over 80%.'),
        ('Photochemical smog is worst on cold, cloudy winter days.', False, 'It needs strong sunlight to drive the reactions, so it is worst on hot, sunny, still days.'),
        ('Indoor air pollution is a major cause of death in low-income countries.', True, 'Burning wood, charcoal and dung for cooking produces smoke and particulates; WHO estimates over 3 million deaths a year.'),
    ],
    'cs': [('a city with severe air pollution', [
        ('Delhi, India', {
            'causes': 'Over 10 million vehicles, coal power stations and industry, construction dust, burning of crop stubble in Punjab and Haryana in October-November, and winter temperature inversions with low wind speeds.',
            'impacts': 'Winter PM2.5 often exceeds 300 μg/m³ (60 times the WHO guideline); high rates of asthma and lung disease; schools and building sites closed on the worst days; reduced life expectancy.',
            'management': 'Odd-even number-plate schemes, conversion of buses and auto-rickshaws to CNG, closure of coal power stations near the city, bans on construction during smog, and subsidies for machines to manage stubble; improvements have been limited.'}),
        ('Mexico City', {
            'causes': 'A high-altitude basin surrounded by mountains traps pollutants; temperature inversions; millions of vehicles and industry; strong sunlight produces photochemical smog.',
            'impacts': 'In 1992 the UN named it the most polluted city in the world; high ozone levels caused respiratory illness.',
            'management': 'Hoy No Circula (no-driving days), removal of lead from petrol, catalytic converters, relocation of refineries, the Metrobús and EcoBici; ozone and lead fell greatly, though ozone still often exceeds standards.'}),
        ('Beijing, China', {
            'causes': 'Coal burning for heating and industry, rapid growth in vehicles, dust storms from the Gobi, and winter inversions.',
            'impacts': '“Airpocalypse” in January 2013 with PM2.5 above 800 μg/m³; health costs and lower tourism.',
            'management': 'The 2013 Air Pollution Action Plan: coal boilers replaced by gas and electric heating, factories moved, car purchases limited by lottery, electric buses; PM2.5 fell by about a third by 2017.'}),
    ], [
        ('explain the causes of the air pollution', 'causes', 'sources, physical factors (relief, inversions), named pollutants'),
        ('describe the impacts of the air pollution', 'impacts', 'health, economic, environmental, with data'),
        ('evaluate the strategies used to reduce air pollution', 'management', 'named strategies with outcomes and limitations; judgement'),
    ])],
    'essays': [
        ('air pollution is a local problem that can be solved by local actions',
         ['Smog in Mexico City and Beijing has been reduced by city-level measures such as vehicle restrictions and replacing coal heating.'],
         ['Acid rain and particulates cross borders (stubble burning in Punjab affects Delhi; UK emissions affected Scandinavia), requiring national and international agreements such as the 1979 LRTAP Convention.'],
         'Local actions are essential for urban air quality, but many pollutants are regional or transboundary and need wider cooperation.',
         ['transboundary pollution', 'named cities', 'international agreements']),
    ],
})


@a5.add('C3', (1, 2, 3, 4, 5), 'numerical')
def a5_ph(r, D):
    lake = r.choice(['a lake in southern Norway', 'a lake in the Adirondack Mountains', 'a reservoir near ' + city(r), 'a lake in Sweden'])
    p1 = round(r.uniform(4.0, 4.8), 1)
    p2 = round(r.uniform(5.6, 6.8), 1)
    yr1, yr2 = r.choice([(1980, 2020), (1985, 2015), (1975, 2010)])
    factor = 10 ** (p2 - p1)
    intro = f'The pH of {lake} was {p1} in {yr1}. After emissions of sulfur dioxide were reduced and the lake was limed, the pH in {yr2} was {p2}.'
    if D == 1:
        return MCQ(r, intro + f' How many times more acidic was the lake in {yr1} than in {yr2}?', s3(factor), [s3(p2 - p1), s3(factor * 10), s3(factor / 10), s3(p2 / p1)], f'10^({p2} − {p1}) = {s3(factor)}. [1]')
    parts = [
        L(f'Calculate how many times more acidic the lake was in {yr1} than in {yr2}.', s3(factor), f'pH difference {fmt(round(p2 - p1, 1), 1)} [1]; 10^{fmt(round(p2 - p1, 1), 1)} = {s3(factor)} [1] [2]'),
        L(f'Explain why fish populations may have declined in the lake by {yr1}.', 'Low pH and dissolved aluminium damage fish gills and prevent eggs from hatching; invertebrate food sources die.', 'gills / aluminium [1]; reproduction or food chain [1] [2]'),
        L('Explain how liming increases the pH of the lake.', 'Powdered limestone (calcium carbonate) neutralises the acid in the water.', '[1]'),
        L('Suggest why liming is not a long-term solution.', 'It treats symptoms not causes; it must be repeated regularly and is expensive; it can harm some species such as acid-loving mosses.', '1 mark per point up to [2]'),
        L('Describe two ways of reducing sulfur dioxide emissions at source.', 'Flue gas desulfurisation; burning low-sulfur coal or switching to gas or renewables; reducing energy demand.', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D)


@a5.add('C3', (1, 2, 3, 4, 5), 'numerical')
def a5_pm(r, D):
    cty = r.choice(['Delhi', 'Lahore', 'Dhaka', 'Beijing', 'Cairo', 'Jakarta', 'Lima', 'Bangkok', 'Lagos', 'Ulaanbaatar'])
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    base = r.randint(40, 160)
    vals = [max(8, base + r.randint(-35, 60)) for _ in days]
    mean = sum(vals) / 7
    guide = 15   # WHO 24-hour guideline 2021
    over = sum(1 for v in vals if v > guide)
    intro = f'Daily mean PM2.5 concentrations (μg/m³) recorded in {cty} during one week: ' + ', '.join(f'{d} {v}' for d, v in zip(days, vals)) + '. The WHO 24-hour guideline is 15 μg/m³.'
    if D == 1:
        return MCQ(r, intro + ' What is the mean concentration for the week?', f'{f1(mean)} μg/m³', [f'{f1(sorted(vals)[3])} μg/m³' if sorted(vals)[3] != round(mean, 1) else f'{f1(mean + 5)} μg/m³', f'{f1(sum(vals) / 6)} μg/m³', f'{f1(max(vals) - min(vals))} μg/m³', f'{f1(mean / guide)} μg/m³'],
                   f'{sum(vals)} ÷ 7 = {f1(mean)}. [1]')
    parts = [
        L('Calculate the mean concentration for the week.', f'{f1(mean)} μg/m³', f'{sum(vals)} ÷ 7 = {f1(mean)} [1]'),
        L('Calculate how many times greater the mean is than the WHO guideline.', s3(mean / guide), f'{f1(mean)} ÷ 15 = {s3(mean / guide)} [1]'),
        L('Calculate the range of the daily values.', f'{max(vals) - min(vals)} μg/m³', f'{max(vals)} − {min(vals)} = {max(vals) - min(vals)} [1]'),
        L('Suggest reasons for the variation between days.', 'Changes in weather (wind speed, rain, inversions); traffic differences between weekdays and weekends; episodes of burning or industrial activity.', '1 mark per reason up to [2]'),
        L('Explain why PM2.5 is particularly harmful to health.', 'The particles are so small that they penetrate deep into the alveoli and enter the bloodstream, causing respiratory and heart disease.', '[2]'),
    ]
    return comp(r, intro, parts, D)


CHAPTERS[3] = [a1, a2, a3, a4, a5]


# ============================================================== CHAPTER 4: Biosphere

b1 = T('Ecosystems: energy flow, trophic levels, food chains and food webs, and productivity', 'ecosystems', 'energy flow', 'trophic levels', 'productivity')
build(b1, {
    'terms': [
        ('ecosystem', 'a community of interacting organisms and their physical environment'),
        ('trophic level', 'the position an organism occupies in a food chain, such as producer or primary consumer'),
        ('producer', 'an organism that makes its own food from simple inorganic substances, usually by photosynthesis'),
        ('decomposer', 'an organism such as a bacterium or fungus that breaks down dead organic matter and releases nutrients'),
        ('gross primary productivity (GPP)', 'the total rate at which producers convert light energy into chemical energy by photosynthesis'),
        ('net primary productivity (NPP)', 'the rate at which energy is stored in plant biomass after respiration losses, NPP = GPP − R'),
        ('food web', 'a network of interconnected food chains in an ecosystem'),
        ('pyramid of energy', 'a diagram showing the energy flowing through each trophic level per unit area per year'),
    ],
    'mcq': [
        ('Approximately what percentage of energy is passed from one trophic level to the next?', 'About 10%', ['About 50%', 'About 90%', 'About 1%'], 'Most energy is lost in respiration, heat, egestion and uneaten parts. [1]'),
        ('Which ecosystem has the highest net primary productivity per square metre?', 'Tropical rainforest', ['Desert', 'Tundra', 'Open ocean'], 'About 2200 g/m²/yr. [1]'),
        ('Why are food chains rarely longer than four or five links?', 'Too little energy remains at higher trophic levels', ['Predators eat plants', 'Decomposers remove the top level', 'Producers cannot photosynthesise enough'], '[1]'),
        ('In a food chain grass → grasshopper → frog → snake, the frog is the', 'secondary consumer', ['primary consumer', 'producer', 'tertiary consumer'], '[1]'),
        ('Which pyramid can never be inverted?', 'Pyramid of energy', ['Pyramid of numbers', 'Pyramid of biomass', 'All of them can be inverted'], 'Energy is lost at each step. [1]'),
    ],
    'explain': [
        ('Explain why energy is lost between trophic levels.', 'Not all the organism is eaten (roots, bones); not all eaten material is digested (lost in faeces); energy is used in respiration and lost as heat; energy is used for movement.', '1 mark per reason up to [3]'),
        ('Explain why the open ocean has low productivity per square metre even though it covers a large area.', 'Nutrients are scarce in surface waters because dead material sinks; light penetrates only the upper layers, so phytoplankton growth is limited except in upwelling zones.', 'nutrient shortage [1]; light limited with depth [1] [2]'),
        ('Explain why eating lower in the food chain can feed more people.', 'Energy is lost at each trophic level, so crops eaten directly provide about ten times more energy per hectare than meat from animals fed on crops.', 'energy loss per level [1]; more food energy per area [1] [2]'),
        ('Explain the role of decomposers in an ecosystem.', 'They break down dead organisms and waste, releasing nutrients such as nitrates and phosphates back into the soil for producers, and releasing CO₂ by respiration.', 'break down dead matter [1]; recycle nutrients [1] [2]'),
    ],
    'claims': [
        ('Most of the energy from the Sun that reaches a leaf is converted into plant biomass.', False, 'Only about 1-3% is fixed by photosynthesis; the rest is reflected, transmitted or not absorbed by chlorophyll.'),
        ('Removing a top predator can affect producers in an ecosystem.', True, 'Trophic cascades: e.g. reintroducing wolves to Yellowstone reduced elk browsing and allowed willows and aspen to recover.'),
        ('Decomposers are a trophic level that gains no energy.', False, 'Decomposers obtain energy from dead organic matter by respiring it.'),
    ],
    'cases': [(
        ['Fig. 4.1 shows a food web for a mangrove ecosystem in {m}: mangrove leaves and algae are eaten by crabs, snails and small fish; these are eaten by larger fish and wading birds; crocodiles and sea eagles are top predators.',
         'A student studied a freshwater pond food web: algae and pondweed → water fleas and snails → small fish and dragonfly larvae → herons.'],
        [('Draw a food chain with four organisms from the food web.', 'e.g. algae → snail → small fish → heron (or mangrove leaves → crab → larger fish → sea eagle).', '[1]'),
         ('Explain why there are fewer top predators than primary consumers.', 'Energy is lost at each trophic level, so less energy is available to support top predators.', '[2]'),
         ('Suggest the effect on the food web if one primary consumer were removed.', 'Its food (producers) would increase; its predators would decline or switch to other prey, increasing pressure on other primary consumers.', '1 mark per developed effect up to [3]'),
         ('Explain the importance of the producers in this ecosystem.', 'They convert light energy into chemical energy in biomass by photosynthesis, which supports all other trophic levels; they also release oxygen and provide habitats.', '[2]'),
         ('Suggest how a pollutant could reach high concentrations in the top predator.', 'A persistent pollutant (e.g. mercury, DDT) is not broken down or excreted; it accumulates in each organism and is concentrated up the food chain (biomagnification).', '[2]')])],
    'essays': [
        ('energy flow, not nutrient cycling, limits the size of ecosystems',
         ['Energy is lost as heat at each trophic level, limiting food chain length and the biomass of top predators.'],
         ['Nutrients (nitrogen, phosphorus) often limit productivity, e.g. in the open ocean or tropical rainforest soils; water and temperature also limit NPP.'],
         'Energy flow limits food chain length, but nutrients, water and temperature often limit the productivity of the producers.',
         ['trophic efficiency', 'limiting factors', 'productivity data']),
    ],
})


@b1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def b1_energy(r, D):
    eco = r.choice(['a grassland in Kenya', 'a temperate forest', 'a lake ecosystem', 'a coral reef', 'a salt marsh'])
    p = r.choice([8000, 12000, 20000, 25000, 36000, 50000])
    e1 = r.uniform(0.08, 0.15)
    e2 = r.uniform(0.08, 0.15)
    c1 = round(p * e1, -1)
    c2 = round(c1 * e2)
    eff1 = c1 / p * 100
    eff2 = c2 / c1 * 100
    intro = f'In {eco}, energy flow (kJ/m²/year) at each trophic level was measured: producers {nf(p)}, primary consumers {nf(c1)}, secondary consumers {nf(c2)}.'
    if D == 1:
        return MCQ(r, intro + ' What is the efficiency of energy transfer from producers to primary consumers?', f'{f1(eff1)}%', [f'{f1(eff2)}%', f'{f1(100 - eff1)}%', f'{f1(eff1 * 10)}%', f'{f1(c2 / p * 100)}%'],
                   f'{nf(c1)} ÷ {nf(p)} × 100 = {f1(eff1)}%. [1]')
    gpp = round(p * r.uniform(1.6, 2.2), -2)
    parts = [
        L('Calculate the efficiency of energy transfer from producers to primary consumers.', f'{f1(eff1)}%', f'{nf(c1)} ÷ {nf(p)} × 100 [1] = {f1(eff1)}% [1] [2]'),
        L('Calculate the efficiency of energy transfer from primary to secondary consumers.', f'{f1(eff2)}%', f'{nf(c2)} ÷ {nf(c1)} × 100 = {f1(eff2)}% [1]'),
        L(f'The gross primary productivity of the producers is {nf(gpp)} kJ/m²/year and the value given for producers is their net primary productivity. Calculate the energy used in respiration by the producers.', f'{nf(gpp - p)} kJ/m²/year',
          f'R = GPP − NPP = {nf(gpp)} − {nf(p)} = {nf(gpp - p)} [1]'),
        L('State three ways in which energy is lost between trophic levels.', 'Respiration (heat); parts not eaten; undigested material lost in faeces; excretion.', '1 mark each [3]'),
        L('Suggest why a fourth trophic level is unlikely in this ecosystem.', f'Only {nf(c2)} kJ/m²/year reaches secondary consumers; about 10% of this ({nf(c2 * 0.1)}) would be too little to support a viable population of predators.', '[2]'),
    ]
    return comp(r, intro, parts, D)


b2 = T('Biogeochemical cycles: carbon and nitrogen cycles', 'biogeochemical cycles', 'carbon cycle', 'nitrogen cycle')
build(b2, {
    'terms': [
        ('nitrogen fixation', 'the conversion of nitrogen gas into ammonia or nitrates, by bacteria such as Rhizobium, by lightning or by the Haber process'),
        ('nitrification', 'the conversion of ammonium ions to nitrites and then nitrates by nitrifying bacteria in the soil'),
        ('denitrification', 'the conversion of nitrates back to nitrogen gas by denitrifying bacteria in waterlogged, anaerobic soils'),
        ('ammonification', 'the conversion of nitrogen in dead organic matter and waste into ammonium by decomposers'),
        ('carbon store', 'a reservoir in which carbon is held, such as the atmosphere, oceans, soils, vegetation or fossil fuels'),
        ('carbon flux', 'the transfer of carbon between stores, such as photosynthesis, respiration or combustion'),
        ('carbon sequestration', 'the long-term capture and storage of carbon dioxide, naturally in forests, soils and oceans or by technology'),
        ('leaching', 'the loss of soluble nutrients such as nitrates from the soil into groundwater and rivers by water draining through'),
    ],
    'mcq': [
        ('Which process removes carbon dioxide from the atmosphere?', 'Photosynthesis', ['Respiration', 'Combustion', 'Decomposition'], '[1]'),
        ('Which bacteria live in the root nodules of legumes such as peas and beans?', 'Nitrogen-fixing bacteria (Rhizobium)', ['Denitrifying bacteria', 'Nitrifying bacteria only', 'Decomposing fungi'], '[1]'),
        ('Which is the largest store of carbon on Earth?', 'Sedimentary rocks such as limestone', ['The atmosphere', 'Vegetation', 'Soils'], 'Over 60 million Gt C, far more than any other store. [1]'),
        ('Denitrification is most likely in', 'waterlogged soils with little oxygen', ['well-aerated sandy soils', 'the leaves of plants', 'the upper atmosphere'], '[1]'),
        ('In which form do plants absorb most of their nitrogen?', 'Nitrate ions', ['Nitrogen gas', 'Proteins', 'Nitrous oxide'], '[1]'),
        ('About what proportion of human CO₂ emissions is absorbed by the oceans?', 'About a quarter', ['About 1%', 'About three quarters', 'All of it'], '[1]'),
    ],
    'explain': [
        ('Describe how carbon is transferred from the atmosphere to the soil.', 'Plants absorb CO₂ in photosynthesis and build organic compounds; leaves, roots and dead plants (and animals that ate them) fall to the ground; decomposers incorporate part of the carbon into humus.', 'photosynthesis [1]; death / litter fall [1]; decomposition to humus [1] [3]'),
        ('Explain how human activities have altered the carbon cycle.', 'Burning fossil fuels transfers carbon from long-term stores to the atmosphere; deforestation reduces photosynthesis and releases carbon from biomass and soils; cement production releases CO₂; farming disturbs soil carbon.', '1 mark per developed point up to [3]'),
        ('Explain how the use of nitrogen fertilisers affects the nitrogen cycle.', 'The Haber process fixes very large amounts of atmospheric nitrogen; excess nitrate leaches into rivers causing eutrophication; denitrification releases nitrous oxide, a greenhouse gas.', '1 mark per point up to [3]'),
        ('Explain why ocean acidification is linked to the carbon cycle.', 'Oceans absorb CO₂ from the atmosphere; it dissolves to form carbonic acid, lowering pH and reducing carbonate ions that corals and shellfish need to build shells and skeletons.', 'CO₂ absorbed [1]; carbonic acid / lower pH [1]; effect on organisms [1] [3]'),
        ('Describe the role of bacteria in the nitrogen cycle.', 'Nitrogen-fixing bacteria convert N₂ to ammonium; decomposers produce ammonium from dead matter; nitrifying bacteria convert ammonium to nitrite and nitrate; denitrifying bacteria return nitrate to N₂.', '1 mark per type up to [3]'),
    ],
    'claims': [
        ('Planting forests can help to reduce atmospheric carbon dioxide.', True, 'Growing trees remove CO₂ by photosynthesis and store carbon in wood and soil, though the store can be lost by fire or felling.'),
        ('Plants can take nitrogen directly from the air.', False, 'Most plants cannot use N₂; they absorb nitrates from soil; legumes rely on bacteria in their root nodules.'),
        ('Burning fossil fuels moves carbon from a slow cycle to a fast cycle.', True, 'Carbon stored for millions of years in coal, oil and gas is released into the atmosphere in decades.'),
    ],
    'cases': [(
        ['Fig. 4.2 shows a simplified nitrogen cycle for a farm in {c}, with fertiliser input, legumes, livestock manure, crops harvested and nitrate leaching into a stream.',
         'A farm applies 180 kg of nitrogen fertiliser per hectare each year to wheat. Measurements show high nitrate concentrations in a stream draining the farm.'],
        [('Name the process by which bacteria convert ammonium in manure to nitrate.', 'Nitrification', '[1]'),
         ('Explain why nitrate is easily lost from the soil.', 'Nitrate ions are very soluble and are not held by negatively charged soil particles, so they are washed out by drainage water (leaching).', '[2]'),
         ('Describe the possible effects of the leached nitrate on the stream.', 'Eutrophication: algal blooms, death of plants, oxygen depletion by bacteria, fish deaths; drinking water may exceed safe nitrate limits.', '1 mark per effect up to [3]'),
         ('Suggest how the farmer could reduce nitrate losses.', 'Apply fertiliser in smaller amounts at times when crops are growing; avoid applying before heavy rain; plant cover crops in winter; grow legumes; leave buffer strips beside the stream.', '1 mark per method up to [3]'),
         ('Explain the role of legumes in the nitrogen cycle on the farm.', 'Nitrogen-fixing bacteria in their root nodules convert N₂ into ammonium, adding nitrogen to the soil and reducing fertiliser needs.', '[2]')])],
    'essays': [
        ('human activities have changed the nitrogen cycle more than the carbon cycle',
         ['The Haber process and legume crops now fix more nitrogen than all natural land processes combined, roughly doubling nitrogen inputs; this causes eutrophication, dead zones (Gulf of Mexico) and N₂O emissions.'],
         ['Fossil-fuel burning and deforestation have increased atmospheric CO₂ by about 50%, causing climate change and ocean acidification with global consequences.'],
         'Proportionally the nitrogen cycle has been changed more, but changes to the carbon cycle have the greatest global impact.',
         ['fertilisers', 'fossil fuels', 'scale of change']),
    ],
})


@b2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def b2_carbon(r, D):
    atm = r.choice([860, 875, 880])
    ff = r.choice([9.4, 9.6, 9.9, 10.0])
    luc = r.choice([1.1, 1.2, 1.3])
    ocean = r.choice([2.6, 2.8, 2.9])
    land = r.choice([3.0, 3.1, 3.3, 3.5])
    gain = ff + luc - ocean - land
    ppm = gain / 2.12
    intro = (f'Estimated global carbon fluxes (Gt C per year): fossil fuels and cement {fmt(ff, 1)}; land-use change {fmt(luc, 1)}; uptake by the ocean {fmt(ocean, 1)}; uptake by land vegetation {fmt(land, 1)}. '
             f'The atmosphere stores about {atm} Gt C. 1 ppm of CO₂ ≈ 2.12 Gt C.')
    if D == 1:
        return MCQ(r, intro + ' What is the net increase in atmospheric carbon each year?', f'{f1(gain)} Gt C', [f'{f1(ff + luc)} Gt C', f'{f1(ocean + land)} Gt C', f'{f1(ff - ocean - land)} Gt C', f'{f1(gain + 2)} Gt C'],
                   f'{fmt(ff, 1)} + {fmt(luc, 1)} − {fmt(ocean, 1)} − {fmt(land, 1)} = {f1(gain)}. [1]')
    parts = [
        L('Calculate the net annual increase in carbon in the atmosphere.', f'{f1(gain)} Gt C', f'sources {f1(ff + luc)} − sinks {f1(ocean + land)} [1] = {f1(gain)} [1] [2]'),
        L('Calculate the percentage of human emissions that remains in the atmosphere.', f'{f1(gain / (ff + luc) * 100)}%', f'{f1(gain)} ÷ {f1(ff + luc)} × 100 = {f1(gain / (ff + luc) * 100)}% [1]'),
        L('Convert the annual increase into ppm of CO₂.', f'{f2(ppm)} ppm per year', f'{f1(gain)} ÷ 2.12 = {f2(ppm)} [1]'),
        L('Calculate the percentage increase in the atmospheric store in one year.', f'{f2(gain / atm * 100)}%', f'{f1(gain)} ÷ {atm} × 100 = {f2(gain / atm * 100)}% [1]'),
        L('Explain why the oceans and land are described as carbon sinks.', 'They absorb more carbon than they release: oceans dissolve CO₂ and phytoplankton photosynthesise; vegetation absorbs CO₂ by photosynthesis and stores it in biomass and soils.', '[2]'),
        L('Suggest one reason why the land sink may weaken in future.', 'Deforestation, drought, wildfires and higher temperatures increase respiration and decomposition, releasing stored carbon.', '[1]'),
    ]
    return comp(r, intro, parts, D)


@b2.add('C3', (2, 3, 4, 5), 'numerical')
def b2_nitro(r, D):
    applied = r.choice([120, 150, 180, 200, 250])
    up = r.randint(45, 70)
    leach = r.randint(10, 30)
    deni = r.randint(5, 15)
    rest = 100 - up - leach - deni
    if rest < 0:
        return None
    area = r.choice([20, 50, 80, 120])
    crop = r.choice(['maize', 'wheat', 'rice', 'potatoes', 'cotton'])
    intro = (f'A farmer in {city(r)} applies {applied} kg of nitrogen fertiliser per hectare to a {area} ha field of {crop}. Of the nitrogen applied, {up}% is taken up by the crop, '
             f'{leach}% is lost by leaching, {deni}% is lost by denitrification and the rest remains in the soil.')
    parts = [
        L('Calculate the mass of nitrogen leached from the whole field.', f'{nf(applied * area * leach / 100)} kg', f'{applied} × {area} = {nf(applied * area)} kg [1]; × {leach}% = {nf(applied * area * leach / 100)} kg [1] [2]'),
        L('Calculate the percentage of nitrogen that remains in the soil.', f'{rest}%', f'100 − {up} − {leach} − {deni} = {rest}% [1]'),
        L('Calculate the mass of nitrogen per hectare that is not used by the crop.', f'{fmt(applied * (100 - up) / 100, 1)} kg/ha', f'{applied} × {100 - up}% = {fmt(applied * (100 - up) / 100, 1)} [1]'),
        L('Explain why denitrification is an environmental concern.', 'It releases nitrous oxide (N₂O), a powerful greenhouse gas that also damages ozone, as well as wasting fertiliser.', '[2]'),
        L('Suggest two ways the farmer could increase the percentage taken up by the crop.', 'Split applications timed to crop growth; precision application using soil tests; slow-release fertilisers; avoid application before rain; improve soil organic matter.', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D)


b3 = T('Biomes, biodiversity and ecological succession', 'biomes', 'biodiversity', 'ecological succession')
build(b3, {
    'terms': [
        ('biome', 'a large global ecosystem defined by its climate and dominant vegetation, such as tropical rainforest or tundra'),
        ('biodiversity', 'the variety of life in an area, including genetic, species and ecosystem (habitat) diversity'),
        ('species richness', 'the number of different species in an area'),
        ('species evenness', 'how similar the population sizes of the different species in an area are'),
        ('ecological succession', 'the gradual change in the species of a community over time'),
        ('primary succession', 'succession on newly formed bare ground with no soil, such as lava or sand dunes'),
        ('climax community', 'the stable, final community at the end of succession, in balance with the climate'),
        ('pioneer species', 'the first species to colonise bare ground, such as lichens or marram grass, which tolerate harsh conditions'),
    ],
    'mcq': [
        ('Which biome has the highest biodiversity?', 'Tropical rainforest', ['Tundra', 'Hot desert', 'Boreal forest (taiga)'], '[1]'),
        ('Which species is a typical pioneer on sand dunes?', 'Marram grass', ['Oak', 'Pine', 'Heather'], 'It tolerates burial, salt and drought, and its roots stabilise sand. [1]'),
        ('Secondary succession begins on', 'land where a community has been removed but soil remains', ['bare rock', 'new volcanic islands', 'glacial moraine with no soil'], 'E.g. abandoned farmland or after fire. [1]'),
        ('Which biome is found at about 60° N with long, cold winters and coniferous trees?', 'Taiga (boreal forest)', ['Savanna', 'Temperate grassland', 'Mediterranean scrub'], '[1]'),
        ('Genetic diversity refers to', 'the variety of genes within a species', ['the number of species', 'the variety of habitats', 'the number of individuals'], '[1]'),
    ],
    'explain': [
        ('Explain why tropical rainforests have high biodiversity.', 'High temperatures and rainfall all year give high productivity; a stable climate over long periods allowed many species to evolve; layered structure provides many niches.', '1 mark per developed reason up to [3]'),
        ('Describe the changes that take place during primary succession on bare rock.', 'Pioneer lichens and mosses colonise and weather the rock; they die and add organic matter, forming thin soil; grasses and herbs grow, then shrubs and finally trees; soil deepens, biodiversity and biomass increase until a climax community forms.', '1 mark per stage up to [4]'),
        ('Explain why biodiversity is important.', 'It provides food, medicines and materials; ecosystem services such as pollination, water purification and climate regulation; resilience of ecosystems; cultural and aesthetic value; intrinsic value.', '1 mark per point up to [3]'),
        ('Explain how a climax community may be prevented from developing.', 'Human activities such as grazing, burning, mowing or felling keep the community at an earlier stage (a plagioclimax), e.g. heather moorland maintained by burning.', 'named arresting factor [1]; plagioclimax [1] [2]'),
        ('Explain how the climate of the tundra affects its vegetation.', 'Long, very cold winters, a short growing season and permafrost mean plants are low-growing, slow-growing and shallow-rooted (mosses, lichens, dwarf shrubs); low productivity.', '[3]'),
    ],
    'claims': [
        ('Biodiversity always increases steadily throughout succession.', False, 'It usually increases through the middle stages but may fall slightly at the climax when a few dominant species (e.g. trees) shade out others.'),
        ('Biomes are distributed mainly according to climate.', True, 'Temperature and precipitation determine the dominant vegetation, so biomes form broad latitudinal belts.'),
        ('A habitat with many individuals of one species has high biodiversity.', False, 'Biodiversity depends on the number of species and evenness, not just the number of individuals.'),
    ],
    'cases': [(
        ['Fig. 4.3 shows a transect across sand dunes at a coastal site, from embryo dunes near the sea to woodland 400 m inland. Species number, soil organic matter and pH were recorded every 50 m.',
         'Students in {c} studied succession on a sand dune system. Near the sea only marram grass and sea couch grew; 300 m inland there was heath and woodland with over 20 species.'],
        [('Describe how the number of species changes with distance from the sea.', 'It increases inland from very few on embryo dunes to many in fixed dunes and woodland.', '[2]'),
         ('Explain why marram grass is able to grow on the young dunes.', 'It tolerates burial, salt spray and drought; it has long roots to reach water and grows upward when buried.', '1 mark per adaptation up to [2]'),
         ('Explain how the pioneer plants change the environment to allow other species to grow.', 'They stabilise sand, reduce wind speed, add organic matter as they die so soil forms and retains water and nutrients.', '1 mark per point up to [3]'),
         ('Suggest why soil pH falls with distance inland.', 'Shell fragments (calcium carbonate) are leached and humus from plants adds organic acids.', '[2]'),
         ('Suggest how trampling by tourists could affect the succession.', 'It destroys vegetation and exposes sand to wind erosion (blowouts), setting succession back.', '[2]')])],
    'essays': [
        ('the main value of biodiversity is economic',
         ['Biodiversity provides food, timber, medicines (about 25% of drugs come from plants), tourism income and ecosystem services worth trillions of dollars a year.'],
         ['It also has ecological value (resilience, stability), cultural and spiritual value, and intrinsic value; many species have no known economic use.'],
         'Economic value is a powerful argument for conservation, but biodiversity also has ecological and ethical value that cannot be measured in money.',
         ['ecosystem services', 'medicines', 'intrinsic value']),
    ],
})
compare_item(b3, [
    ('primary succession', 'secondary succession', 'Primary succession starts on bare ground with no soil and takes centuries; secondary succession starts where soil remains after disturbance and is much faster.', 'Both lead towards a climax community with increasing biomass.'),
    ('tropical rainforest', 'tundra', 'Rainforest is hot and wet all year with very high productivity and biodiversity; tundra is cold with a short growing season, permafrost, low productivity and few species.', 'Both are fragile biomes that are slow to recover from damage.'),
])


@b3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def b3_succ(r, D):
    dist = [0, 50, 100, 150, 200, 250, 300]
    sp = sorted(r.sample(range(1, 26), 7))
    om = [round(x, 1) for x in sorted([r.uniform(0.2, 12) for _ in range(7)])]
    intro = ('Students sampled vegetation every 50 m along a transect across a sand dune system. Number of plant species: ' + ', '.join(f'{d} m: {s}' for d, s in zip(dist, sp))
             + '. Soil organic matter (%): ' + ', '.join(f'{d} m: {fmt(o, 1)}' for d, o in zip(dist, om)) + '.')
    if D == 1:
        return MCQ(r, intro + ' What is the increase in the number of species from 0 m to 300 m?', str(sp[-1] - sp[0]), [str(sp[-1]), str(sp[-1] + sp[0]), str(sp[3] - sp[0]), str(sp[-1] - sp[0] + 2)], f'{sp[-1]} − {sp[0]} = {sp[-1] - sp[0]}. [1]')
    parts = [
        L('Describe how the number of species changes with distance inland. Use data.', f'Species number increases from {sp[0]} at 0 m to {sp[-1]} at 300 m.', 'trend [1]; data [1] [2]'),
        L('Calculate the percentage increase in soil organic matter from 0 m to 300 m.', f'{nf(pc(om[0], om[-1]))}%', f'({fmt(om[-1], 1)} − {fmt(om[0], 1)}) ÷ {fmt(om[0], 1)} × 100 = {nf(pc(om[0], om[-1]))}% [1]'),
        L('Explain the relationship between soil organic matter and the number of species.', 'As pioneers die and decompose, organic matter increases; soil holds more water and nutrients, allowing more species, which add more organic matter.', 'positive relationship [1]; explanation [1] [2]'),
        L('Explain why a transect is a suitable sampling method here.', 'It records changes along an environmental gradient from the sea inland.', '[1]'),
        L('Suggest one improvement to the method.', 'Use more sample points (e.g. every 25 m); repeat along several parallel transects; use quadrats of the same size at each point.', '[1]'),
    ]
    return comp(r, intro, parts, D)


b4 = T('Threats to biodiversity and conservation strategies: in situ and ex situ', 'threats to biodiversity', 'conservation strategies', 'in situ', 'ex situ')
build(b4, {
    'terms': [
        ('in situ conservation', 'protecting species in their natural habitats, for example in national parks and nature reserves'),
        ('ex situ conservation', 'protecting species outside their natural habitats, for example in zoos, botanic gardens and seed banks'),
        ('habitat fragmentation', 'the breaking up of a continuous habitat into small isolated patches, for example by roads and farmland'),
        ('invasive species', 'a non-native species that spreads rapidly and harms native species and ecosystems'),
        ('endemic species', 'a species found naturally in only one geographical area'),
        ('biodiversity hotspot', 'a region with very high numbers of endemic species that has lost at least 70% of its original habitat'),
        ('wildlife corridor', 'a strip of habitat that links isolated areas so animals can move between them'),
        ('captive breeding', 'breeding endangered animals in zoos or centres, often with the aim of releasing them into the wild'),
    ],
    'mcq': [
        ('Which is an example of ex situ conservation?', 'The Millennium Seed Bank at Kew, UK', ['The Serengeti National Park', 'A marine protected area', 'A wildlife corridor'], '[1]'),
        ('Which international agreement controls trade in endangered species?', 'CITES', ['The Ramsar Convention', 'The Montreal Protocol', 'The Basel Convention'], '[1]'),
        ('Which is the biggest single cause of biodiversity loss worldwide?', 'Habitat loss and change in land use', ['Volcanic eruptions', 'Ozone depletion', 'Zoos'], 'IPBES 2019. [1]'),
        ('The cane toad in Australia is an example of', 'an invasive species', ['an endemic species', 'a keystone species reintroduced', 'a pioneer species'], '[1]'),
        ('Why do small, isolated populations have a high risk of extinction?', 'Low genetic diversity and vulnerability to chance events', ['They have no predators', 'They reproduce too quickly', 'They are protected by law'], '[1]'),
    ],
    'explain': [
        ('Explain how habitat fragmentation threatens species.', 'Small patches support only small populations; edges change conditions; animals cannot move to find mates or food; inbreeding reduces genetic diversity; populations are vulnerable to local extinction.', '1 mark per point up to [3]'),
        ('Explain the advantages of in situ conservation compared with ex situ conservation.', 'Species stay in their natural habitat with natural behaviour, food and interactions; whole ecosystems and many species are protected together; evolution continues; usually cheaper per species.', '1 mark per advantage up to [3]'),
        ('Explain the role of seed banks in conservation.', 'Seeds of many plant species are dried and frozen, storing genetic diversity for decades; they can be used to restore habitats or crops if species are lost in the wild; they take little space.', '1 mark per point up to [3]'),
        ('Explain why the illegal wildlife trade threatens species such as rhinos and pangolins.', 'High prices for horn and scales (used in traditional medicine or as status items) encourage poaching; slow-breeding species cannot replace losses; poverty and weak enforcement make poaching attractive.', '1 mark per point up to [3]'),
    ],
    'claims': [
        ('Zoos are the best way to conserve endangered species.', False, 'Zoos can support captive breeding and education, but they hold small populations and cannot conserve whole ecosystems; in situ protection is usually more effective.'),
        ('Climate change is becoming a major threat to biodiversity.', True, 'Species ranges shift, coral reefs bleach and species unable to move or adapt may become extinct.'),
        ('Protected areas always stop biodiversity loss.', False, 'Some are “paper parks” with weak enforcement, are too small, or are affected by pollution, climate change and invasive species.'),
    ],
    'cs': [('a conservation project', [
        ('the Galápagos Islands, Ecuador', {
            'threats': 'Invasive goats, rats and plants; overfishing; tourism growth (over 250 000 visitors a year); climate change and El Niño affecting marine food supply.',
            'management': 'A national park (97% of land) and marine reserve; eradication of goats from Santiago and Isabela; captive breeding of giant tortoises; strict tourism rules with licensed guides; biosecurity inspections.'}),
        ('the Amazon rainforest, Brazil', {
            'threats': 'Cattle ranching, soya farming, logging, mining and road building; about 17% of the forest has been lost; fires; climate change may cause dieback.',
            'management': 'Protected areas and indigenous reserves cover about half the Brazilian Amazon; satellite monitoring (DETER); the Soy Moratorium (2006); the Amazon Fund; deforestation fell by about 80% from 2004 to 2012 but rose again after 2015 before falling in 2023.'}),
        ('the Kew Millennium Seed Bank, UK', {
            'threats': 'Around 40% of plant species are threatened with extinction by habitat loss, climate change and invasive species.',
            'management': 'Stores seeds of over 40 000 species from more than 190 countries at −20 °C; partners worldwide; seeds used for research and to restore habitats, but seeds of some species (e.g. many tropical trees) cannot be stored.'}),
    ], [
        ('describe the threats to biodiversity', 'threats', 'named threats with explanation and data'),
        ('evaluate the effectiveness of the conservation strategies used', 'management', 'in situ / ex situ methods, evidence of success, limitations, judgement'),
    ])],
    'essays': [
        ('in situ conservation is more effective than ex situ conservation',
         ['Protecting habitats conserves whole ecosystems, natural behaviour and evolution (e.g. Galápagos, Serengeti); it is cheaper per species.'],
         ['Ex situ methods are vital when habitats are destroyed or populations are tiny: the Arabian oryx and California condor were saved by captive breeding; seed banks store huge genetic diversity.'],
         'The two are complementary: in situ is generally more effective, but ex situ provides an insurance policy and supports reintroductions.',
         ['named examples', 'costs', 'reintroduction']),
        ('habitat loss is a greater threat to biodiversity than climate change',
         ['Land-use change is currently the leading cause of species decline (IPBES), e.g. palm oil in Borneo and cattle ranching in the Amazon.'],
         ['Climate change is accelerating: coral bleaching on the Great Barrier Reef, range shifts and predicted extinctions; it interacts with other threats.'],
         'Habitat loss is the main threat now, but climate change may become as important later this century.',
         ['deforestation', 'coral reefs', 'interactions between threats']),
    ],
})


@b4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def b4_defor(r, D):
    region, area0 = r.choice([('the Brazilian Amazon', 4100000), ('Borneo', 740000), ('the Congo Basin', 1700000), ('Sumatra', 480000)])
    pct_lost = r.choice([12, 15, 17, 20, 25, 30])
    rate = r.choice([6000, 8000, 10000, 13000])
    if region != 'the Brazilian Amazon':
        rate = r.choice([1500, 2500, 3500, 5000])
    remain = area0 * (1 - pct_lost / 100)
    intro = f'The original forest area of {region} was about {nf(area0)} km². About {pct_lost}% has been cleared, and current clearance is about {nf(rate)} km² per year.'
    if D == 1:
        return MCQ(r, intro + ' What area of forest remains?', f'{nf(remain)} km²', [f'{nf(area0 * pct_lost / 100)} km²', f'{nf(area0 - rate)} km²', f'{nf(remain * 0.9)} km²', f'{nf(remain * 1.1)} km²'],
                   f'{nf(area0)} × {(100 - pct_lost) / 100:.2f} = {nf(remain)}. [1]')
    yrs = remain * 0.25 / rate
    parts = [
        L('Calculate the area of forest remaining.', f'{nf(remain)} km²', f'{nf(area0)} × {100 - pct_lost}% = {nf(remain)} [1]'),
        L('Calculate the annual clearance as a percentage of the remaining forest.', f'{f2(rate / remain * 100)}%', f'{nf(rate)} ÷ {nf(remain)} × 100 = {f2(rate / remain * 100)}% [1]'),
        L('Scientists suggest a tipping point if a further quarter of the remaining forest is lost. Estimate how many years this would take at the current rate.', f'{s3(yrs)} years', f'0.25 × {nf(remain)} = {nf(remain * 0.25)} km² [1]; ÷ {nf(rate)} = {s3(yrs)} years [1] [2]'),
        L('Explain two impacts of the deforestation on biodiversity.', 'Habitat loss leads to population decline and extinction of endemic species; fragmentation isolates populations; edge effects; loss of food sources for dependent species.', '1 mark each impact with explanation [2]'),
        L('Suggest two strategies to reduce the rate of deforestation.', 'Protected areas and indigenous land rights with enforcement; satellite monitoring; certification (FSC, RSPO) and supply-chain bans; payments for ecosystem services (REDD+).', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D)


@b4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def b4_pop(r, D):
    sp = r.choice([('mountain gorilla', 'the Virunga Mountains', 620, 1063, 1989, 2018), ('giant panda', 'China', 1114, 1864, 1988, 2014),
                   ('black rhino', 'Africa', 2410, 6487, 1995, 2022), ('Amur tiger', 'the Russian Far East', 330, 540, 1996, 2015),
                   ('Iberian lynx', 'Spain and Portugal', 94, 1668, 2002, 2022), ('greater one-horned rhino', 'India and Nepal', 1500, 4014, 1985, 2021)])
    name, where, a, b, y1, y2 = sp
    ch = pc(a, b)
    intro = f'The wild population of the {name} in {where} was estimated at {nf(a)} in {y1} and {nf(b)} in {y2}.'
    if D == 1:
        return MCQ(r, intro + ' What was the percentage change?', f'+{f1(ch)}%', [f'+{f1(b - a)}%', f'+{f1(b / a * 10)}%', f'{f1(-pc(b, a))}%', f'+{f1(ch / 2)}%'], f'({nf(b)} − {nf(a)}) ÷ {nf(a)} × 100 = {f1(ch)}%. [1]')
    rate = (b / a) ** (1 / (y2 - y1)) - 1
    parts = [
        L('Calculate the percentage change in the population.', f'+{f1(ch)}%', f'({nf(b)} − {nf(a)}) ÷ {nf(a)} × 100 [1] = {f1(ch)}% [1] [2]'),
        L('Calculate the mean increase in individuals per year.', f'{s3((b - a) / (y2 - y1))} per year', f'{nf(b - a)} ÷ {y2 - y1} = {s3((b - a) / (y2 - y1))} [1]'),
        L('Suggest conservation measures that may explain this change.', 'Anti-poaching patrols and law enforcement; protected areas; captive breeding and reintroduction; community-based tourism giving income to local people; CITES trade bans.', '1 mark per measure up to [3]'),
        L('Explain why the species may still be at risk.', 'Population is still small with low genetic diversity; habitat is limited and fragmented; continuing poaching, disease or conflict; climate change.', '1 mark per point up to [2]'),
        L('Suggest why population estimates of wild animals are uncertain.', 'Animals are hard to see or count in dense or remote habitats; methods (camera traps, dung counts, DNA) differ between surveys.', '[1]'),
    ]
    return comp(r, intro, parts, D)


CHAPTERS[4] = [b1, b2, b3, b4]


# ============================================================== CHAPTER 5: Human population

COUNTRIES_BD = [('Niger', 45, 8), ('Nigeria', 36, 12), ('India', 16, 7), ('Bangladesh', 18, 5), ('Brazil', 12, 7), ('United Kingdom', 10, 9), ('Japan', 6, 13), ('Italy', 7, 12),
                ('Kenya', 27, 5), ('Egypt', 22, 6), ('Mexico', 15, 7), ('USA', 11, 10), ('Germany', 9, 12), ('Pakistan', 27, 7), ('South Korea', 5, 7), ('Ethiopia', 31, 6)]

p1 = T('Population growth and change: birth rate, death rate and natural increase', 'population growth', 'birth rate', 'death rate', 'natural increase')
build(p1, {
    'terms': [
        ('crude birth rate', 'the number of live births per 1000 people in a population per year'),
        ('crude death rate', 'the number of deaths per 1000 people in a population per year'),
        ('natural increase', 'the difference between the birth rate and the death rate, usually given as a percentage'),
        ('total fertility rate', 'the average number of children a woman would have during her lifetime at current birth rates'),
        ('infant mortality rate', 'the number of deaths of infants under one year old per 1000 live births per year'),
        ('replacement fertility', 'a total fertility rate of about 2.1, at which a population replaces itself in the long term'),
        ('doubling time', 'the number of years it would take a population to double at its current growth rate, about 70 ÷ growth rate (%)'),
        ('life expectancy', 'the average number of years a newborn baby is expected to live if current death rates continue'),
    ],
    'mcq': [
        ('The world population passed 8 billion in', '2022', ['1999', '2011', '2035'], 'UN estimate, 15 November 2022. [1]'),
        ('A population growing at 2% per year will double in about', '35 years', ['20 years', '50 years', '70 years'], 'Rule of 70: 70 ÷ 2 = 35. [1]'),
        ('Which country had the highest total fertility rate in the early 2020s?', 'Niger (about 6.7)', ['India (about 2.0)', 'Brazil (about 1.6)', 'South Korea (about 0.8)'], '[1]'),
        ('A falling infant mortality rate usually leads, after some time, to', 'a falling birth rate', ['a rising birth rate', 'a rising death rate', 'more emigration'], 'Parents no longer need many children to ensure some survive. [1]'),
        ('Population change in a country is calculated as', 'births − deaths + immigration − emigration', ['births + deaths', 'birth rate × death rate', 'immigration − births'], '[1]'),
    ],
    'explain': [
        ('Explain why death rates have fallen in most countries since 1950.', 'Improved health care, vaccination and antibiotics; clean water and sanitation; better nutrition and food supply; education about hygiene.', '1 mark per developed reason up to [3]'),
        ('Explain why birth rates are high in many low-income countries.', 'Children work on farms and support parents in old age; high infant mortality; limited access to contraception and education for women; early marriage; cultural and religious traditions.', '1 mark per reason up to [3]'),
        ('Explain why the total fertility rate falls as women gain access to education and employment.', 'Women marry later, have careers, understand and use contraception, and want fewer children who are more costly to educate; they have more say in family decisions.', '1 mark per point up to [3]'),
        ('Explain why world population growth is expected to slow down this century.', 'Fertility is falling in most regions as incomes, urbanisation and female education increase; many countries are below replacement level; populations are ageing.', '1 mark per point up to [2]'),
    ],
    'claims': [
        ('A country with a high birth rate must have a fast-growing population.', False, 'Growth depends also on the death rate and migration; a high death rate could offset births.'),
        ('Most future world population growth will occur in sub-Saharan Africa.', True, 'Africa’s population is projected to roughly double by 2050 because of high fertility and a young population.'),
        ('Life expectancy has increased in almost all countries since 1950.', True, 'Global life expectancy rose from about 46 years in 1950 to about 73 years in 2023.'),
    ],
    'essays': [
        ('rapid population growth is the main cause of environmental problems',
         ['More people increase demand for food, water and energy, causing deforestation, soil degradation and water stress (e.g. the Sahel).'],
         ['Consumption per person matters more: high-income countries with slow growth have the largest ecological footprints; technology and governance determine impacts (I = PAT).'],
         'Population growth is one factor, but levels of consumption, technology and management are often more important.',
         ['I = PAT', 'ecological footprint', 'named countries']),
    ],
})


@p1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p1_ni(r, D):
    k = 4 if D >= 3 else 3
    rows = r.sample(COUNTRIES_BD, k)
    rows = [(n, b + r.choice([-1, 0, 0, 1]), d + r.choice([-1, 0, 0, 1])) for n, b, d in rows]
    stem = 'Table 5.1 shows birth and death rates (per 1000 per year) for selected countries. ' + ' '.join(f'{n}: birth rate {b}, death rate {d}.' for n, b, d in rows)
    ni = [(n, (b - d) / 10) for n, b, d in rows]
    if D == 1:
        n, b, d = rows[0]
        v = (b - d) / 10
        return MCQ(r, stem + f' What is the rate of natural increase for {n}?', f'{f1(v)}%', [f'{f1(b - d)}%', f'{f1((b + d) / 10)}%', f'{f1(v * 2)}%', f'{f2(v / 10)}%'], f'({b} − {d}) ÷ 10 = {f1(v)}%. [1]')
    hi = max(ni, key=lambda x: x[1])
    neg = [n for n, v in ni if v < 0]
    parts = [
        L('Calculate the rate of natural increase (%) for each country.', '; '.join(f'{n} {f1(v)}%' for n, v in ni), '(birth rate − death rate) ÷ 10; two correct [1]; all correct [1] [2]'),
        (lambda r: ('Identify the country with the fastest natural increase.', f'{hi[0]} ({f1(hi[1])}%)', '[1]')) if [v for _, v in ni].count(hi[1]) == 1 else (lambda r: None),
        L('Name a country in the table with natural decrease and suggest why.', (f'{neg[0]}: very low birth rate and an ageing population with a relatively high death rate.' if neg else 'None: no country has a death rate higher than its birth rate.'), 'identification [1]; reason [1] [2]'),
        L(f'Using the rule of 70, estimate the doubling time of the population of {hi[0]}.', (f'About {round(70 / hi[1])} years' if hi[1] > 0 else 'It would not double.'), f'70 ÷ {f1(hi[1])} [1]'),
        L(f'Suggest the environmental pressures that a population growing as fast as {hi[0]} may face.', 'Increased demand for farmland, fuelwood and water; deforestation, soil erosion and water stress; growth of informal settlements with poor sanitation.', '1 mark per pressure up to [2]'),
    ]
    return comp(r, stem, parts, D)


@p1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p1_change(r, D):
    cty = r.choice(['Kenya', 'Vietnam', 'Peru', 'Morocco', 'Malaysia', 'Ghana', 'Nepal', 'Colombia', 'Uzbekistan', 'Sri Lanka'])
    pop = r.randint(10, 60) * 1e6
    br = r.randint(14, 32)
    dr = r.randint(5, 10)
    nm = r.choice([-3, -2, -1, 1, 2])
    births = pop * br / 1000
    deaths = pop * dr / 1000
    mig = pop * nm / 1000
    change = births - deaths + mig
    intro = f'{cty} has a population of {nf(pop / 1e6)} million, a birth rate of {br} per 1000, a death rate of {dr} per 1000 and a net migration rate of {"+" if nm > 0 else MINUS}{abs(nm)} per 1000 per year.'
    if D == 1:
        return MCQ(r, intro + ' How many births occur each year?', nf(births), [nf(deaths), nf(births / 10), nf(births * 10), nf(change)], f'{nf(pop)} × {br} ÷ 1000 = {nf(births)}. [1]')
    gr = change / pop * 100
    parts = [
        L('Calculate the number of births and deaths per year.', f'births {nf(births)}; deaths {nf(deaths)}', f'{nf(pop)} × {br}/1000 [1]; × {dr}/1000 [1] [2]'),
        L('Calculate the total population change in one year, including migration.', f'{"+" if change > 0 else ""}{nf(change)}', f'{nf(births)} − {nf(deaths)} {"+" if nm > 0 else MINUS} {nf(abs(mig))} [1] = {nf(change)} [1] [2]'),
        L('Calculate the overall growth rate as a percentage.', f'{f2(gr)}%', f'{nf(change)} ÷ {nf(pop)} × 100 = {f2(gr)}% [1]'),
        L('Estimate the doubling time using the rule of 70.', f'about {round(70 / gr)} years' if gr > 0.05 else 'the population is not growing fast enough to double', f'70 ÷ {f2(gr)} [1]'),
        L('Suggest one reason for the net migration figure.', ('Emigration for work and higher wages abroad (economic push factors).' if nm < 0 else 'Immigration attracted by jobs and a growing economy, or refugees from neighbouring countries.'), '[1]'),
    ]
    return comp(r, intro, parts, D)


p2 = T('The demographic transition model and population structure: population pyramids', 'demographic transition model', 'population structure', 'population pyramids')
build(p2, {
    'terms': [
        ('demographic transition model (DTM)', 'a model showing how birth rates, death rates and total population change as a country develops, in five stages'),
        ('population pyramid', 'a pair of horizontal bar charts showing the percentage or number of males and females in each age group'),
        ('dependency ratio', 'the number of dependants (aged 0-14 and 65+) per 100 people of working age (15-64)'),
        ('ageing population', 'a population in which the proportion of older people is increasing'),
        ('youthful population', 'a population with a high proportion of people under 15'),
        ('population momentum', 'continued population growth after fertility falls to replacement level, because of the large number of young people entering child-bearing age'),
        ('baby boom', 'a sudden rise in the birth rate, such as in many countries after the Second World War'),
        ('cohort', 'a group of people born in the same period, shown as one bar on a population pyramid'),
    ],
    'mcq': [
        ('In which stage of the DTM is the death rate falling rapidly while the birth rate remains high?', 'Stage 2', ['Stage 1', 'Stage 4', 'Stage 5'], '[1]'),
        ('A population pyramid with a wide base and narrow top indicates', 'high birth rates and low life expectancy', ['an ageing population', 'low birth rates', 'high immigration of older people'], '[1]'),
        ('Which country is an example of stage 5 of the DTM, with natural decrease?', 'Japan', ['Niger', 'Nigeria', 'Afghanistan'], '[1]'),
        ('A population has 30 million aged 0-14, 50 million aged 15-64 and 10 million aged 65+. What is the dependency ratio?', '80', ['40', '60', '20'], '(30 + 10) ÷ 50 × 100 = 80. [1]'),
        ('A bulge in the 20-34 age groups for males only in a Gulf state such as Qatar is caused by', 'immigration of male migrant workers', ['a baby boom', 'a war', 'high female mortality'], '[1]'),
    ],
    'explain': [
        ('Explain the shape of a population pyramid for a country in stage 2 of the DTM.', 'A wide base because the birth rate is high; sides that narrow quickly and a narrow top because the death rate, though falling, is still relatively high and life expectancy is low.', 'wide base / high births [1]; narrow top / low life expectancy [1] [2]'),
        ('Explain the problems that an ageing population may cause.', 'Higher costs of pensions and health care; a shrinking workforce paying taxes; labour shortages; fewer people to care for the elderly; possibly slower economic growth.', '1 mark per developed problem up to [3]'),
        ('Explain the limitations of the demographic transition model.', 'It is based on European experience; it does not include migration; it assumes all countries will follow the same path; it does not predict timing; some countries have skipped stages or been affected by AIDS or policies.', '1 mark per limitation up to [3]'),
        ('Explain why a youthful population can be both an opportunity and a challenge.', 'Opportunity: a large future workforce (demographic dividend) if jobs and education are provided. Challenge: high demand for schools, health care, jobs and housing, and continued growth from population momentum.', 'opportunity [1]; challenge [1]; development [1] [3]'),
    ],
    'claims': [
        ('All countries will eventually reach stage 4 of the DTM.', False, 'The model is based on Europe; some countries may stall or be affected by disease, conflict or policy, and stage 5 shows populations can decline.'),
        ('A high dependency ratio means more people depend on each worker.', True, 'It measures dependants per 100 people of working age.'),
        ('Population pyramids only show the effects of births and deaths.', False, 'They also show migration (e.g. a bulge of working-age males in Gulf states) and events such as wars and epidemics.'),
    ],
    'essays': [
        ('the demographic transition model is of limited use in understanding population change in low-income countries today',
         ['It is based on 19th-century Europe; today death rates in LICs fell faster because of imported medicine; migration, HIV/AIDS and policies (China’s one-child policy) are not included.'],
         ['It still describes the broad sequence seen in Bangladesh, Brazil and Iran, where falling death rates were followed by falling birth rates; it helps predict future needs.'],
         'The model is a useful general framework but must be adapted to each country’s circumstances.',
         ['stages', 'named countries', 'migration and policy']),
    ],
})


@p2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p2_dep(r, D):
    cty = r.choice(['Uganda', 'Japan', 'Italy', 'India', 'Brazil', 'Niger', 'Germany', 'Mexico', 'Indonesia', 'South Korea', 'Egypt', 'Canada'])
    young = {'Uganda': 45, 'Niger': 49, 'Japan': 12, 'Italy': 13, 'Germany': 14, 'South Korea': 12, 'India': 26, 'Brazil': 20, 'Mexico': 25, 'Indonesia': 25, 'Egypt': 33, 'Canada': 16}[cty]
    old = {'Uganda': 2, 'Niger': 3, 'Japan': 29, 'Italy': 24, 'Germany': 22, 'South Korea': 17, 'India': 7, 'Brazil': 10, 'Mexico': 8, 'Indonesia': 7, 'Egypt': 5, 'Canada': 19}[cty]
    young += r.choice([-1, 0, 1])
    old += r.choice([-1, 0, 1])
    work = 100 - young - old
    dr = (young + old) / work * 100
    intro = f'In {cty}, {young}% of the population is aged 0-14, {work}% is aged 15-64 and {old}% is aged 65 and over.'
    if D == 1:
        return MCQ(r, intro + ' What is the dependency ratio?', f'{f1(dr)}', [f'{f1(young + old)}', f'{f1(work / (young + old) * 100)}', f'{f1(young / work * 100)}', f'{f1(old / work * 100)}'],
                   f'({young} + {old}) ÷ {work} × 100 = {f1(dr)}. [1]')
    yd = young / work * 100
    od = old / work * 100
    stage = 'stage 2 or early stage 3' if young >= 35 else 'stage 3' if young >= 22 else 'stage 4' if old < 20 else 'stage 4 or 5'
    parts = [
        L('Calculate the dependency ratio.', f'{f1(dr)}', f'({young} + {old}) ÷ {work} × 100 [1] = {f1(dr)} [1] [2]'),
        L('Calculate the young and old dependency ratios separately.', f'young {f1(yd)}; old {f1(od)}', f'{young} ÷ {work} × 100 [1]; {old} ÷ {work} × 100 [1] [2]'),
        L('Suggest which stage of the DTM the country is in. Give a reason.', f'{cap(stage)}, because ' + ('a large proportion of the population is young, indicating high birth rates.' if young >= 22 else 'there are few young people and a large elderly population, indicating low birth rates and high life expectancy.'), 'stage [1]; reason using data [1] [2]'),
        L('Describe the likely shape of the population pyramid.', ('Wide base narrowing rapidly towards a narrow top.' if young >= 30 else 'Narrow base, wide middle and top (column or inverted shape).' if old >= 18 else 'Fairly straight sides with a slightly narrower base than middle.'), '[1]'),
        L('Suggest one problem caused by this population structure and one way the government could respond.',
          ('Pressure on schools, health care and future jobs; invest in education and family planning.' if young >= 30 else 'Rising pension and health costs with fewer workers; raise the retirement age or encourage immigration.' if old >= 18 else 'A growing working-age population needs jobs; invest in skills and industry.'),
          'problem [1]; response [1] [2]'),
    ]
    return comp(r, intro, parts, D)


p3 = T('Migration: push and pull factors and its impacts', 'migration', 'push and pull factors')
build(p3, {
    'terms': [
        ('migration', 'the movement of people from one place to another to live, either permanently or for a long period'),
        ('push factor', 'a negative feature of a place that encourages people to leave, such as unemployment, conflict or drought'),
        ('pull factor', 'a positive feature of a place that attracts people, such as jobs, safety or better services'),
        ('refugee', 'a person forced to leave their country because of persecution, war or violence'),
        ('internally displaced person', 'a person forced to flee their home who remains within their own country'),
        ('remittances', 'money sent home by migrants to their families in their country of origin'),
        ('rural-urban migration', 'the movement of people from the countryside to towns and cities'),
        ('environmental migrant', 'a person who moves because of sudden or gradual environmental change, such as drought, floods or sea level rise'),
    ],
    'mcq': [
        ('Which is a pull factor for a rural migrant moving to a city?', 'Better job opportunities', ['Crop failure', 'Lack of schools in the village', 'Land shortage'], 'The others are push factors. [1]'),
        ('Which country received the largest value of remittances in the early 2020s?', 'India', ['Germany', 'Japan', 'Australia'], 'Over US$100 billion in 2022. [1]'),
        ('A person who flees war but stays within their own country is', 'an internally displaced person', ['a refugee', 'an economic migrant', 'an emigrant'], '[1]'),
        ('Which is an environmental push factor?', 'Desertification reducing crop yields', ['Higher wages abroad', 'Family reunification', 'University places'], '[1]'),
        ('Net migration is', 'immigration minus emigration', ['emigration minus immigration', 'births minus deaths', 'immigration plus emigration'], '[1]'),
    ],
    'explain': [
        ('Explain the impacts of out-migration on rural areas in low-income countries.', 'Loss of young, economically active people; fewer farm workers so land may be abandoned; ageing population and more women-headed households; remittances can improve incomes and housing; skills may return later.', '1 mark per developed impact up to [3]'),
        ('Explain the environmental impacts of rapid rural-urban migration on cities.', 'Growth of informal settlements on hazardous land; inadequate sanitation and waste collection polluting water; air pollution from traffic and industry; loss of farmland and habitats at the urban fringe.', '1 mark per developed point up to [3]'),
        ('Explain how climate change may increase migration.', 'Sea level rise, droughts, floods and stronger storms damage homes and farmland and reduce water supplies, pushing people to move, e.g. from coastal Bangladesh or the Sahel.', 'environmental change [1]; loss of livelihoods [1]; example [1] [3]'),
        ('Explain the benefits of immigration for a host country with an ageing population.', 'Migrants fill labour shortages, pay taxes that support pensions and health care, raise the birth rate and bring skills and cultural diversity.', '1 mark per point up to [3]'),
    ],
    'claims': [
        ('Most migrants move from low-income countries to high-income countries.', False, 'A large share of migration is between low- and middle-income countries or within countries; most refugees are hosted by neighbouring countries.'),
        ('Remittances can contribute to development in the source country.', True, 'They fund education, health care, housing and small businesses, and exceed foreign aid for many countries.'),
        ('Migration only has economic causes.', False, 'People also move because of conflict, persecution, environmental disasters, family and education.'),
    ],
    'essays': [
        ('the impacts of migration are greater for the source area than for the destination',
         ['Source areas lose young workers and skills (brain drain), changing their population structures, but gain remittances (e.g. Nepal, about a quarter of GDP).'],
         ['Destinations gain labour and taxes but face pressure on housing, services and the environment, especially in rapidly growing cities such as Lagos or Dhaka.'],
         'Impacts are significant at both ends; their balance depends on the scale and type of migration and how it is managed.',
         ['remittances', 'brain drain', 'urban growth']),
    ],
})


@p3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p3_net(r, D):
    cty = r.choice(['Canada', 'the United Arab Emirates', 'Germany', 'Australia', 'Lebanon', 'the Philippines', 'Nepal', 'Mexico', 'Poland', 'Jordan'])
    pop = r.randint(5, 80) * 1e6
    imm = r.randint(50, 900) * 1000
    emi = r.randint(30, 700) * 1000
    net = imm - emi
    rate = net / pop * 1000
    intro = f'In one year {cty} (population {nf(pop / 1e6)} million) had {nf(imm)} immigrants and {nf(emi)} emigrants.'
    if D == 1:
        return MCQ(r, intro + ' What was the net migration rate per 1000 people?', f'{"+" if rate > 0 else ""}{f1(rate)}', [f'{"+" if rate > 0 else ""}{f1(rate * 10)}', f'{f1((imm + emi) / pop * 1000)}', f'{"+" if rate < 0 else MINUS}{f1(abs(rate))}', f'{f1(net / 1000)}'],
                   f'({nf(imm)} − {nf(emi)}) ÷ {nf(pop)} × 1000 = {f1(rate)}. [1]')
    rem = r.choice([2, 5, 8, 12, 20, 25])
    parts = [
        L('Calculate the net migration.', f'{"+" if net > 0 else ""}{nf(net)}', f'{nf(imm)} − {nf(emi)} = {nf(net)} [1]'),
        L('Calculate the net migration rate per 1000 people.', f'{f1(rate)} per 1000', f'{nf(net)} ÷ {nf(pop)} [1] × 1000 = {f1(rate)} [1] [2]'),
        L('Suggest two pull factors that may attract immigrants to a country.', 'Job opportunities and higher wages; political stability and safety; better education and health care; family already living there.', '1 mark each [2]'),
        L(f'Remittances sent home by migrants are worth {rem}% of the GDP of their country of origin. Explain why this is important for that country.', 'Remittances provide income to families for food, schooling, health care and housing, support local businesses and bring foreign currency into the economy.', '1 mark per point up to [2]'),
        L('Describe one environmental impact of large-scale immigration into cities.', 'Increased demand for housing, water and energy; urban sprawl onto farmland and habitats; more waste and pollution.', '[1]'),
    ]
    return comp(r, intro, parts, D)


p4 = T('Population management policies: pro-natalist and anti-natalist', 'population management policies', 'pro-natalist', 'anti-natalist')
build(p4, {
    'terms': [
        ('anti-natalist policy', 'a government policy that aims to reduce the birth rate'),
        ('pro-natalist policy', 'a government policy that aims to increase the birth rate'),
        ('family planning', 'the use of contraception and other methods to control the number and spacing of children'),
        ('one-child policy', 'China’s anti-natalist policy (1979-2015) that limited most urban couples to one child'),
        ('baby bonus', 'a payment from the government to parents when a child is born, used in pro-natalist policies'),
        ('sex ratio at birth', 'the number of boys born for every 100 girls, normally about 105'),
        ('immigration policy', 'government rules controlling who may enter and settle in a country, sometimes used to offset an ageing population'),
        ('population policy', 'a deliberate set of measures by a government to influence the size, growth or structure of its population'),
    ],
    'mcq': [
        ('Which country used a one-child policy from 1979 to 2015?', 'China', ['India', 'Singapore', 'France'], '[1]'),
        ('Which is a pro-natalist measure?', 'Generous paid parental leave and child benefits', ['Free contraception', 'Sterilisation campaigns', 'Raising the legal marriage age'], '[1]'),
        ('Singapore’s “Stop at Two” campaign of the 1970s was later replaced by', 'policies encouraging couples to have three or more children', ['a one-child policy', 'a ban on immigration', 'compulsory sterilisation'], '“Have three or more if you can afford it” (1987). [1]'),
        ('Which effect of China’s one-child policy led to a high sex ratio at birth?', 'Preference for sons combined with sex-selective abortion', ['High infant mortality', 'Immigration of men', 'Low life expectancy for women'], '[1]'),
        ('Which country has a long-standing pro-natalist policy with family allowances and tax benefits?', 'France', ['Niger', 'Bangladesh', 'Ethiopia'], '[1]'),
    ],
    'explain': [
        ('Explain why some governments introduce pro-natalist policies.', 'Fertility below replacement level leads to population decline and ageing; fewer workers and taxpayers to support pensions and health care; concerns about economic growth and national security.', '1 mark per reason up to [3]'),
        ('Explain why pro-natalist policies often have limited success.', 'The costs of raising children (housing, education), careers, later marriage and changing attitudes are hard to offset with payments; effects are often small and temporary.', '1 mark per point up to [2]'),
        ('Explain the unintended consequences of China’s one-child policy.', 'Gender imbalance (about 117 boys per 100 girls at its peak); rapid ageing and a shrinking workforce; “4-2-1” family structure with one child supporting parents and grandparents; human rights concerns.', '1 mark per consequence up to [3]'),
        ('Explain how education of girls can reduce birth rates without a formal policy.', 'Educated women marry later, understand and use contraception, have careers and choose smaller families; their children are more likely to survive.', '1 mark per point up to [3]'),
    ],
    'claims': [
        ('Anti-natalist policies always involve compulsion.', False, 'Many use education, free contraception and incentives (e.g. Bangladesh, Iran), not force.'),
        ('Iran reduced its fertility rate very rapidly in the 1990s.', True, 'Through a voluntary family planning programme, free contraception and female education, TFR fell from about 6.5 in the mid-1980s to about 2 by 2000.'),
        ('Pro-natalist policies are mainly found in low-income countries.', False, 'They are mainly found in high-income countries with low fertility such as France, Singapore, South Korea and Hungary.'),
    ],
    'cs': [('a population policy', [
        ('China’s one-child policy (1979-2015)', {
            'aims': 'To slow population growth and support economic development by limiting most urban couples to one child, using incentives for compliance and fines for extra births.',
            'evaluation': 'The fertility rate fell from about 2.8 to about 1.6 and an estimated 200-400 million births may have been prevented, though fertility was already falling; problems included a sex ratio of about 117:100, rapid ageing and a shrinking workforce, leading to a two-child policy in 2016 and three children in 2021.'}),
        ('Singapore’s population policies', {
            'aims': 'From 1966 anti-natalist (“Stop at Two”) to slow growth; from 1987 pro-natalist (“Have three or more if you can afford it”) with baby bonuses, tax relief and housing priority to raise fertility.',
            'evaluation': 'The anti-natalist phase was very successful, with TFR falling below replacement by 1975; the pro-natalist phase has had little success, with TFR about 1.0 in 2023, so the government relies on immigration.'}),
    ], [
        ('describe the aims and methods of the policy', 'aims', 'named measures, incentives and penalties'),
        ('evaluate the success of the policy', 'evaluation', 'evidence of changes in fertility; side-effects; judgement'),
    ])],
    'essays': [
        ('government population policies have little effect on birth rates',
         ['China’s one-child policy and Singapore’s “Stop at Two” were followed by rapid falls in fertility; Iran’s family planning programme was highly effective.'],
         ['Fertility was already falling in China before 1979; pro-natalist policies in Singapore, Japan and South Korea have failed to raise fertility much; education and urbanisation have greater effects.'],
         'Policies can speed up change, especially anti-natalist ones, but social and economic factors usually have a larger effect.',
         ['anti-natalist policies', 'pro-natalist policies', 'female education']),
    ],
})


@p4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p4_tfr(r, D):
    cty, data = r.choice([('China', [(1970, 5.8), (1980, 2.7), (1990, 2.5), (2000, 1.6), (2015, 1.7), (2022, 1.2)]),
                          ('Iran', [(1985, 6.4), (1990, 4.8), (1995, 3.0), (2000, 2.2), (2010, 1.8), (2022, 1.7)]),
                          ('Bangladesh', [(1975, 6.6), (1985, 5.0), (1995, 3.6), (2005, 2.6), (2015, 2.1), (2022, 2.0)]),
                          ('South Korea', [(1970, 4.5), (1985, 1.7), (2000, 1.5), (2010, 1.2), (2018, 1.0), (2023, 0.72)]),
                          ('Singapore', [(1965, 4.7), (1975, 2.1), (1985, 1.6), (2000, 1.6), (2010, 1.15), (2023, 0.97)])])
    pts = sorted(r.sample(data, 3))
    intro = f'Total fertility rate (TFR) in {cty}: ' + ', '.join(f'{y}: {fmt(v, 2)}' for y, v in pts) + '. Replacement level is about 2.1.'
    (y0, v0), (y1, v1), (y2, v2) = pts
    if D == 1:
        return MCQ(r, intro + f' What was the percentage fall in TFR from {y0} to {y2}?', f'{f1(-pc(v0, v2))}%', [f'{f1(v0 - v2)}%', f'{f1(v2 / v0 * 100)}%', f'{f1(-pc(v0, v1))}%', f'{f1(pc(v2, v0))}%'],
                   f'({fmt(v0, 2)} − {fmt(v2, 2)}) ÷ {fmt(v0, 2)} × 100 = {f1(-pc(v0, v2))}%. [1]')
    parts = [
        L(f'Calculate the percentage fall in TFR from {y0} to {y2}.', f'{f1(-pc(v0, v2))}%', f'({fmt(v0, 2)} − {fmt(v2, 2)}) ÷ {fmt(v0, 2)} × 100 [1] = {f1(-pc(v0, v2))}% [1] [2]'),
        L(f'Calculate the mean fall in TFR per year between {y0} and {y1}.', f'{s3((v0 - v1) / (y1 - y0))} per year', f'({fmt(v0, 2)} − {fmt(v1, 2)}) ÷ {y1 - y0} = {s3((v0 - v1) / (y1 - y0))} [1]'),
        L(f'State whether the TFR in {y2} is above or below replacement level and explain what this means for future population.', ('Below replacement: in the long term the population will decline unless there is immigration (after any population momentum).' if v2 < 2.1 else 'At or above replacement: the population will continue to grow or remain stable.'), 'comparison [1]; consequence [1] [2]'),
        L('Suggest reasons, other than government policy, for the fall in fertility.', 'Female education and employment, urbanisation, lower infant mortality, higher costs of raising children and access to contraception.', '1 mark per reason up to [2]'),
        L(f'Suggest the type of population policy {cty} is likely to need now. Explain your answer.', ('A pro-natalist policy (and/or immigration), because fertility is far below replacement and the population is ageing.' if v2 < 1.8 else 'Continued voluntary family planning while investing in education and jobs for the young population.'), 'type [1]; reason [1] [2]'),
    ]
    return comp(r, intro, parts, D)


p5 = T('Carrying capacity, overpopulation and the ecological footprint', 'carrying capacity', 'overpopulation', 'ecological footprint')
build(p5, {
    'terms': [
        ('carrying capacity', 'the maximum population that an environment can support indefinitely with its available resources'),
        ('overpopulation', 'when there are too many people for the resources and technology available to maintain an adequate standard of living'),
        ('underpopulation', 'when there are too few people to make full use of the resources available'),
        ('optimum population', 'the number of people that gives the highest standard of living with the available resources and technology'),
        ('ecological footprint', 'the area of biologically productive land and water needed to supply the resources a person or population uses and absorb their wastes'),
        ('biocapacity', 'the ability of an area’s ecosystems to produce resources and absorb wastes, measured in global hectares'),
        ('Earth Overshoot Day', 'the date in a year when humanity’s demand for resources exceeds what the Earth can regenerate in that year'),
        ('global hectare', 'a hectare of land with world-average biological productivity, used to measure ecological footprints'),
    ],
    'mcq': [
        ('Thomas Malthus (1798) argued that', 'population grows geometrically while food supply grows arithmetically', ['technology will always increase food supply faster than population', 'population cannot exceed 1 billion', 'birth rates fall as incomes rise'], '[1]'),
        ('Ester Boserup argued that', 'population pressure stimulates new farming technology', ['famine is inevitable', 'population should be controlled by war', 'carrying capacity is fixed'], '“Necessity is the mother of invention.” [1]'),
        ('The global average ecological footprint is about 2.6 gha per person while biocapacity is about 1.5 gha. This means humanity uses resources equivalent to about', '1.7 Earths', ['0.6 Earths', '1 Earth', '4 Earths'], '2.6 ÷ 1.5 ≈ 1.7. [1]'),
        ('Which country has one of the largest ecological footprints per person?', 'Qatar', ['Bangladesh', 'Haiti', 'Eritrea'], '[1]'),
        ('The largest component of the global ecological footprint is', 'the carbon footprint', ['the fishing grounds footprint', 'built-up land', 'grazing land'], 'About 60%. [1]'),
    ],
    'explain': [
        ('Explain why carrying capacity is difficult to calculate for human populations.', 'Humans use technology to increase resources, trade to import resources, and have very different levels of consumption; resource needs change over time.', '1 mark per point up to [3]'),
        ('Explain why high-income countries have larger ecological footprints than low-income countries.', 'Higher consumption of energy, meat, manufactured goods and travel; more waste; higher carbon emissions from fossil fuels.', '1 mark per point up to [3]'),
        ('Describe ways in which individuals can reduce their ecological footprint.', 'Use public transport, cycle or walk; reduce meat consumption; save energy; buy local, seasonal food; reduce, reuse and recycle; fly less.', '1 mark per way up to [3]'),
        ('Compare the views of Malthus and Boserup on population and resources.', 'Malthus believed population growth would outstrip food supply, leading to famine, disease and war (positive checks); Boserup believed population growth stimulates innovation that increases food production (e.g. the Green Revolution).', 'Malthus [1]; Boserup [1]; comparison / evidence [1] [3]'),
    ],
    'claims': [
        ('A country with a high population density must be overpopulated.', False, 'Singapore and the Netherlands have very high densities but high living standards, because of technology and trade.'),
        ('The Green Revolution supports Boserup’s ideas.', True, 'High-yielding varieties, irrigation and fertilisers greatly increased food production as population grew.'),
        ('Earth Overshoot Day has moved earlier in the year since the 1970s.', True, 'It moved from late December in 1971 to about the start of August in recent years, as demand has grown faster than biocapacity.'),
    ],
    'essays': [
        ('the world is overpopulated',
         ['Humanity’s ecological footprint exceeds biocapacity by about 70%; biodiversity loss, climate change and water stress suggest limits are being exceeded.'],
         ['Food production has kept pace with population (Boserup); the problem is unequal consumption and distribution; fertility is falling and population may peak this century.'],
         'The world is not overpopulated in terms of numbers alone, but current levels of consumption are unsustainable.',
         ['Malthus and Boserup', 'ecological footprint', 'consumption']),
    ],
})


@p5.add('C3', (1, 2, 3, 4, 5), 'numerical')
def p5_footprint(r, D):
    data = [('Qatar', 14.3, 1.0), ('USA', 8.0, 3.4), ('Australia', 7.0, 12.3), ('Germany', 4.7, 1.5), ('China', 3.6, 0.9), ('Brazil', 2.6, 8.6), ('India', 1.2, 0.4),
            ('Bangladesh', 0.8, 0.4), ('Nigeria', 1.1, 0.6), ('United Kingdom', 4.2, 1.1), ('Japan', 4.6, 0.6), ('Indonesia', 1.7, 1.3), ('Canada', 8.1, 15.0)]
    rows = r.sample(data, 3 if D <= 3 else 4)
    world_bc = 1.6
    intro = 'Table 5.5 shows ecological footprint and biocapacity per person (global hectares, gha): ' + '; '.join(f'{n} footprint {fmt(f, 1)}, biocapacity {fmt(b, 1)}' for n, f, b in rows) + '. World biocapacity is about 1.6 gha per person.'
    n0, f0, b0 = rows[0]
    if D == 1:
        return MCQ(r, intro + f' How many Earths would be needed if everyone lived like the average person in {n0}?', s3(f0 / world_bc), [s3(f0 / b0), s3(world_bc / f0), s3(f0 - world_bc), s3(f0 / world_bc * 2)],
                   f'{fmt(f0, 1)} ÷ 1.6 = {s3(f0 / world_bc)}. [1]')
    deficit = [(n, b - f) for n, f, b in rows]
    parts = [
        L('Calculate the ecological balance (biocapacity − footprint) for each country and identify those in ecological deficit.', '; '.join(f'{n} {"+" if v > 0 else ""}{f1(v)}' for n, v in deficit) + '. Deficit: ' + (', '.join(n for n, v in deficit if v < 0) or 'none'), 'calculations [1]; deficit countries identified [1] [2]'),
        L(f'Calculate how many Earths would be needed if everyone lived like the average person in {n0}.', s3(f0 / world_bc), f'{fmt(f0, 1)} ÷ 1.6 = {s3(f0 / world_bc)} [1]'),
        L('Suggest how a country can have a footprint larger than its biocapacity.', 'It imports resources (food, timber, energy) from other countries, uses up stocks (fossil fuels, overfishing) and emits more CO₂ than its ecosystems absorb.', '1 mark per point up to [2]'),
        L('Explain why a country with a large biocapacity per person may still be unsustainable.', 'Biocapacity may be degraded by deforestation or overgrazing; exports reduce it; high per-person consumption and carbon emissions affect the global commons.', '[2]'),
        L('Suggest two limitations of the ecological footprint as a measure.', 'It uses averages that hide inequality; it simplifies impacts into area; it omits some pollution and biodiversity loss; data quality varies.', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D)


CHAPTERS[5] = [p1, p2, p3, p4, p5]


# ============================================================== CHAPTER 6: Natural resources: energy, water and food

e1 = T('Energy resources: renewable and non-renewable, energy demand and energy security', 'energy resources', 'renewable and non-renewable', 'energy security')
build(e1, {
    'terms': [
        ('non-renewable resource', 'a resource that is finite and cannot be replaced on a human timescale once used, such as coal, oil and natural gas'),
        ('renewable resource', 'a resource that is naturally replenished and will not run out if managed properly, such as solar, wind and hydroelectric power'),
        ('energy security', 'reliable, uninterrupted access to sufficient energy at an affordable price'),
        ('energy mix', 'the combination of different energy sources used by a country to meet its demand'),
        ('fracking', 'hydraulic fracturing: pumping water, sand and chemicals at high pressure into shale rock to release natural gas or oil'),
        ('capacity factor', 'the actual electricity output of a power station over a period as a percentage of its maximum possible output'),
        ('reserves-to-production ratio', 'the number of years known reserves would last at the current rate of production'),
        ('energy efficiency', 'using less energy to provide the same service, such as LED lighting or building insulation'),
    ],
    'mcq': [
        ('Which energy source is renewable?', 'Geothermal', ['Uranium (nuclear)', 'Natural gas', 'Coal'], '[1]'),
        ('Which country generates almost all of its electricity from hydroelectric and geothermal power?', 'Iceland', ['Saudi Arabia', 'Poland', 'Qatar'], '[1]'),
        ('The main disadvantage of wind and solar power is that', 'their output is intermittent', ['they produce large amounts of CO₂ when generating', 'they use finite fuel', 'they produce radioactive waste'], '[1]'),
        ('Which energy source has the problem of long-lived radioactive waste?', 'Nuclear power', ['Tidal power', 'Biomass', 'Wind power'], '[1]'),
        ('Which is the world’s largest hydroelectric power station by installed capacity?', 'The Three Gorges Dam, China', ['The Hoover Dam, USA', 'Itaipu, Brazil-Paraguay', 'Aswan High Dam, Egypt'], 'About 22 500 MW. [1]'),
        ('A country that imports most of its energy from a single supplier has', 'low energy security', ['high energy security', 'a renewable energy mix', 'no energy demand'], '[1]'),
    ],
    'explain': [
        ('Explain why global energy demand has increased.', 'Population growth; economic development and industrialisation in emerging economies (China, India); rising living standards with more appliances, air conditioning and cars; urbanisation.', '1 mark per developed reason up to [3]'),
        ('Explain the factors that affect a country’s energy security.', 'Availability of domestic resources; reliance on imports and number of suppliers; political stability of suppliers; infrastructure and storage; diversity of the energy mix; price volatility.', '1 mark per factor up to [3]'),
        ('Explain the environmental advantages and disadvantages of hydroelectric power.', 'Advantages: no CO₂ emissions during generation, reliable and controllable, reservoir stores water. Disadvantages: flooding of land and habitats, displacement of people, methane from rotting vegetation, blocks fish migration and traps sediment.', 'advantage [1]; disadvantages [2] [3]'),
        ('Explain why many countries are increasing their use of renewable energy.', 'To reduce greenhouse gas emissions and meet climate targets; to improve energy security by reducing imports; falling costs of solar and wind; to reduce air pollution; to create jobs.', '1 mark per reason up to [3]'),
        ('Describe the environmental impacts of fracking.', 'Contamination of groundwater by chemicals or methane; very large water use; small earthquakes; methane leaks; traffic, noise and land use at well sites.', '1 mark per impact up to [3]'),
    ],
    'claims': [
        ('Renewable energy sources have no environmental impacts.', False, 'They have impacts such as land use (solar farms), bird and bat deaths (wind), habitat flooding (HEP) and mining of materials for batteries and panels.'),
        ('Coal is still the largest single source of electricity worldwide.', True, 'Coal generated about a third of global electricity in the early 2020s, mainly in China and India.'),
        ('Nuclear power produces large amounts of carbon dioxide when generating electricity.', False, 'Nuclear generation emits almost no CO₂; emissions come from mining, construction and decommissioning.'),
    ],
    'cs': [('an energy strategy', [
        ('Germany’s Energiewende', {
            'strategy': 'A transition to renewable energy: feed-in tariffs from 2000 encouraged solar and wind; renewables supplied over 50% of electricity by 2023; nuclear power phased out in 2023; coal to be phased out by 2038.',
            'evaluation': 'Large growth in renewables and falling emissions, but high electricity prices, continued reliance on lignite coal and imported gas (exposed by the 2022 energy crisis), and a need for new transmission lines from the windy north to the industrial south.'}),
        ('geothermal and HEP in Iceland', {
            'strategy': 'Uses its position on the Mid-Atlantic Ridge: geothermal energy heats about 90% of homes and, with HEP, supplies almost all electricity; cheap energy attracts aluminium smelters.',
            'evaluation': 'Very high energy security and low emissions from electricity; but HEP schemes such as Kárahnjúkar flooded wilderness; transport still uses imported oil.'}),
        ('Kenya’s geothermal development at Olkaria', {
            'strategy': 'Development of geothermal power in the East African Rift Valley at Olkaria near Lake Naivasha; geothermal supplies about 45% of electricity, with HEP and wind (Lake Turkana wind farm).',
            'evaluation': 'Reliable, low-carbon base-load power that reduces dependence on drought-sensitive HEP and imported oil; but Maasai communities were displaced and access to electricity in rural areas is still limited.'}),
    ], [
        ('describe the energy strategy', 'strategy', 'named sources, data on the energy mix, reasons'),
        ('evaluate the success of the strategy in providing secure and sustainable energy', 'evaluation', 'security, cost, environmental impacts, social impacts; judgement'),
    ])],
    'essays': [
        ('renewable energy can meet all of the world’s energy needs',
         ['Solar and wind costs have fallen by about 90% and 70% since 2010; countries such as Iceland, Norway, Costa Rica and Paraguay generate nearly all electricity from renewables.'],
         ['Intermittency requires storage and grids; transport, heavy industry and aviation are hard to electrify; materials such as lithium and rare earths are limited; renewables supplied only about 15% of primary energy in the early 2020s.'],
         'Renewables could meet most needs in the long term with storage, efficiency and new technology, but the transition will take decades.',
         ['intermittency', 'costs', 'named countries']),
    ],
})
compare_item(e1, [
    ('solar power', 'wind power', 'Solar produces electricity only in daylight and best in sunny, low-latitude places; wind power works day and night where winds are strong and steady but is variable and has visual and noise impacts.', 'Both are renewable, intermittent and emit no CO₂ when generating.'),
    ('nuclear power', 'coal-fired power', 'Nuclear produces almost no CO₂ or air pollution but creates radioactive waste and accident risk; coal is cheap and reliable but emits large amounts of CO₂, SO₂ and particulates.', 'Both provide reliable base-load electricity from finite fuels.'),
])


@e1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e1_mix(r, D):
    cty = r.choice(['Country A', 'Country B', 'Country X', 'a middle-income country', 'an island state'])
    src = ['coal', 'natural gas', 'oil', 'nuclear', 'hydroelectric', 'wind', 'solar']
    vals = [r.randint(5, 40) for _ in src]
    tot = sum(vals)
    ren = vals[4] + vals[5] + vals[6]
    fos = vals[0] + vals[1] + vals[2]
    intro = f'Electricity generation in {cty} in one year (TWh): ' + ', '.join(f'{s} {v}' for s, v in zip(src, vals)) + '.'
    if D == 1:
        return MCQ(r, intro + ' What percentage of the electricity was generated from renewable sources?', f'{f1(ren / tot * 100)}%', [f'{f1(fos / tot * 100)}%', f'{f1((ren + vals[3]) / tot * 100)}%', f'{f1(ren)}%', f'{f1(vals[4] / tot * 100)}%'],
                   f'({vals[4]} + {vals[5]} + {vals[6]}) ÷ {tot} × 100 = {f1(ren / tot * 100)}%. [1]')
    grow = r.choice([10, 15, 20, 25])
    parts = [
        L('Calculate the percentage of electricity generated from renewable sources.', f'{f1(ren / tot * 100)}%', f'renewables {ren} TWh [1]; ÷ {tot} × 100 = {f1(ren / tot * 100)}% [1] [2]'),
        L('Calculate the percentage generated from fossil fuels.', f'{f1(fos / tot * 100)}%', f'{fos} ÷ {tot} × 100 = {f1(fos / tot * 100)}% [1]'),
        L(f'Solar generation grows by {grow}% per year. Calculate solar generation after 3 years.', f'{s3(vals[6] * (1 + grow / 100) ** 3)} TWh', f'{vals[6]} × {1 + grow / 100:.2f}³ [1] = {s3(vals[6] * (1 + grow / 100) ** 3)} TWh [1] [2]'),
        L('Suggest two reasons why the country may want to increase the proportion of renewable electricity.', 'Reduce CO₂ emissions to meet targets; reduce dependence on imported fuels (energy security); reduce air pollution; falling costs.', '1 mark each [2]'),
        L('Explain one challenge of increasing the share of wind and solar power.', 'They are intermittent, so storage (batteries, pumped hydro), back-up generation or stronger grids are needed to match supply and demand.', '[2]'),
    ]
    return comp(r, intro, parts, D)


@e1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e1_cf(r, D):
    kind, cf = r.choice([('wind farm', r.choice([25, 30, 35, 40])), ('solar farm', r.choice([12, 15, 18, 22])), ('nuclear power station', r.choice([85, 90, 92])),
                         ('hydroelectric power station', r.choice([40, 45, 50]))])
    cap_mw = r.choice([50, 100, 200, 400, 1000])
    out = cap_mw * 8760 * cf / 100   # MWh
    homes = r.choice([3, 4, 5])   # MWh per home per year
    intro = f'A {kind} has an installed capacity of {cap_mw} MW and a capacity factor of {cf}%. There are 8760 hours in a year.'
    if D == 1:
        return MCQ(r, intro + ' How much electricity does it generate in a year?', f'{nf(out)} MWh', [f'{nf(cap_mw * 8760)} MWh', f'{nf(out / 10)} MWh', f'{nf(cap_mw * 365 * cf / 100)} MWh', f'{nf(out * 2)} MWh'],
                   f'{cap_mw} × 8760 × {cf / 100:.2f} = {nf(out)} MWh. [1]')
    parts = [
        L('Calculate the electricity generated in a year in MWh.', f'{nf(out)} MWh', f'{cap_mw} × 8760 [1] × {cf}% = {nf(out)} MWh [1] [2]'),
        L(f'An average home uses {homes} MWh per year. Calculate how many homes could be supplied.', nf(out / homes), f'{nf(out)} ÷ {homes} = {nf(out / homes)} [1]'),
        L('Explain why the capacity factor is less than 100%.', {'wind farm': 'Wind speeds vary and are sometimes too low or too high; maintenance.', 'solar farm': 'No output at night, less in cloudy weather and winter; maintenance.',
                                                                 'nuclear power station': 'Shutdowns for refuelling and maintenance.', 'hydroelectric power station': 'Water availability varies with season and drought; output is varied to match demand.'}[kind], '[2]'),
        L('Calculate the capacity needed from this type of plant to generate 1 000 000 MWh per year.', f'{s3(1e6 / (8760 * cf / 100))} MW', f'1 000 000 ÷ (8760 × {cf / 100:.2f}) = {s3(1e6 / (8760 * cf / 100))} MW [1]'),
    ]
    return comp(r, intro, parts, D)


@e1.add('C3', (2, 3, 4, 5), 'numerical')
def e1_rp(r, D):
    fuel, unit = r.choice([('oil', 'billion barrels'), ('natural gas', 'trillion m³'), ('coal', 'billion tonnes')])
    res = {'oil': r.choice([48, 160, 250, 300]), 'natural gas': r.choice([6, 12, 24, 37]), 'coal': r.choice([30, 110, 140, 250])}[fuel]
    prod = {'oil': round(res / r.uniform(15, 70), 2), 'natural gas': round(res / r.uniform(20, 80), 3), 'coal': round(res / r.uniform(40, 150), 2)}[fuel]
    g = r.choice([2, 3, 5])
    rp = res / prod
    # years until exhausted with production growing g% per year
    yrs, used, p = 0, 0.0, prod
    while used < res and yrs < 500:
        used += p
        p *= 1 + g / 100
        yrs += 1
    intro = f'A country has proven {fuel} reserves of {fmt(res, 2)} {unit} and produces {fmt(prod, 3)} {unit} per year.'
    parts = [
        L('Calculate the reserves-to-production (R/P) ratio.', f'{s3(rp)} years', f'{fmt(res, 2)} ÷ {fmt(prod, 3)} = {s3(rp)} years [1]'),
        L(f'If production increases by {g}% each year, the reserves would be used up after about {yrs} years. Explain why this is shorter than the R/P ratio.', 'The R/P ratio assumes production stays constant; increasing production uses the reserves faster.', '[1]'),
        L('Explain why the R/P ratio may increase in future even though the fuel is being used.', 'New reserves are discovered; new technology (e.g. fracking, deep-water drilling) or higher prices make more of the resource economic to extract; demand may fall.', '1 mark per point up to [2]'),
        L('Suggest how the country could improve its long-term energy security.', 'Diversify the energy mix, develop renewables and nuclear, improve efficiency, build storage and invest in interconnectors or diverse suppliers.', '1 mark per point up to [2]'),
    ]
    return comp(r, intro, parts, D)


e2 = T('Water resources: supply, demand, water scarcity and management strategies', 'water resources', 'water scarcity', 'supply, demand')
build(e2, {
    'terms': [
        ('water stress', 'when renewable water supply is below about 1700 m³ per person per year'),
        ('water scarcity', 'when renewable water supply is below about 1000 m³ per person per year, or demand exceeds available supply'),
        ('physical water scarcity', 'a shortage of water because demand exceeds the natural supply, as in arid regions'),
        ('economic water scarcity', 'a shortage of water caused by lack of investment, infrastructure or ability to pay, even where water is available'),
        ('desalination', 'the removal of salt from sea water or brackish water to produce fresh water'),
        ('virtual water', 'the water used to produce goods and food, which is effectively traded when they are exported'),
        ('water footprint', 'the total volume of fresh water used to produce the goods and services consumed by a person or country'),
        ('grey water', 'lightly used water from baths, sinks and washing machines that can be reused for purposes such as flushing toilets or irrigation'),
    ],
    'mcq': [
        ('Which sector uses about 70% of the world’s fresh water withdrawals?', 'Agriculture', ['Industry', 'Domestic use', 'Energy production'], '[1]'),
        ('Under the Falkenmark indicator, a country with 800 m³ of renewable water per person per year has', 'water scarcity', ['no water stress', 'water stress only', 'absolute water scarcity'], '< 1000 scarcity; < 500 absolute scarcity. [1]'),
        ('Singapore’s NEWater is', 'highly treated recycled wastewater', ['desalinated sea water', 'imported water from Malaysia', 'rainwater from roofs only'], '[1]'),
        ('Which irrigation method uses water most efficiently?', 'Drip irrigation', ['Flood irrigation', 'Furrow irrigation', 'Sprinklers at midday'], '[1]'),
        ('The shrinking of the Aral Sea was caused mainly by', 'diversion of the Amu Darya and Syr Darya rivers to irrigate cotton', ['climate change only', 'oil drilling', 'earthquakes'], '[1]'),
        ('Which country produces much of its drinking water by desalination?', 'Israel', ['Norway', 'Brazil', 'Canada'], 'About 80% of domestic water. [1]'),
    ],
    'explain': [
        ('Explain why demand for water is increasing.', 'Population growth; more irrigated agriculture to feed people; industrialisation and energy production; rising living standards (showers, washing machines, diets with more meat); urbanisation.', '1 mark per reason up to [3]'),
        ('Explain the difference between physical and economic water scarcity.', 'Physical scarcity is a natural shortage where demand exceeds supply, e.g. the Middle East; economic scarcity is where water exists but there is no money or infrastructure to supply it, e.g. much of sub-Saharan Africa.', 'physical with example [1]; economic with example [1] [2]'),
        ('Evaluate desalination as a solution to water scarcity.', 'It provides a reliable, drought-proof supply for coastal areas (Israel, Saudi Arabia, Singapore); but it is energy-intensive and expensive, emits CO₂ unless renewable energy is used, and returns concentrated brine that harms marine life.', 'advantage [1]; disadvantages [2]; judgement [1] [4]'),
        ('Explain how water transfers between river basins can cause conflict.', 'Taking water from one basin reduces flow for downstream users, farmers and ecosystems; regions or countries compete for limited supply, e.g. the Nile (Grand Ethiopian Renaissance Dam) or China’s South-North Water Transfer.', '1 mark per point up to [3]'),
    ],
    'claims': [
        ('Water scarcity only affects countries with dry climates.', False, 'Economic water scarcity affects many wet countries without infrastructure, and over-use can cause scarcity anywhere.'),
        ('Reducing leaks in water pipes can save large amounts of water.', True, 'Some cities lose 30-50% of treated water through leaks; repairing pipes increases supply without new sources.'),
        ('Building more dams is the only way to increase water supply.', False, 'Recycling, desalination, rainwater harvesting, reducing demand and fixing leaks also increase available water.'),
    ],
    'cs': [('water management in a water-scarce country', [
        ('Singapore', {
            'strategy': 'The “four national taps”: local catchment in reservoirs (about two-thirds of land is catchment), imported water from Johor (Malaysia), NEWater (recycled wastewater, about 40% of demand) and desalination (about 25%); plus water pricing, efficiency labels and education.',
            'evaluation': 'Supply has become diverse and secure, with plans to be self-sufficient by 2061 when the Malaysian agreement ends; but desalination and NEWater are energy-intensive and costly.'}),
        ('Israel', {
            'strategy': 'Desalination plants (e.g. Sorek) supply about 80% of domestic water; about 85-90% of wastewater is treated and reused for irrigation; drip irrigation was invented and is widely used; national water carrier; strict pricing.',
            'evaluation': 'Israel has moved from scarcity to a water surplus, but desalination uses much energy and brine is discharged to the Mediterranean; access to water for Palestinians remains unequal and contested.'}),
    ], [
        ('describe the strategies used to increase water supply and manage demand', 'strategy', 'named schemes with data'),
        ('evaluate the sustainability of the water management strategies', 'evaluation', 'economic, social and environmental sustainability; judgement'),
    ])],
    'essays': [
        ('managing demand is more sustainable than increasing supply for solving water scarcity',
         ['Drip irrigation, fixing leaks, pricing and grey-water recycling reduce demand cheaply and have few environmental impacts.'],
         ['Rapidly growing cities and dry countries need new supplies: desalination (Israel), recycling (Singapore NEWater) and reservoirs; demand reduction alone may not be enough.'],
         'Demand management should come first as the cheapest and most sustainable option, but most countries need a combination of both.',
         ['agriculture', 'technology', 'named countries']),
    ],
})


@e2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e2_falk(r, D):
    data = [('Egypt', 57, 111), ('Saudi Arabia', 2.4, 36), ('India', 1911, 1417), ('Kenya', 31, 54), ('Brazil', 8647, 215), ('Jordan', 0.94, 11), ('Pakistan', 247, 236),
            ('China', 2840, 1412), ('United Kingdom', 147, 67), ('Ethiopia', 122, 123), ('South Africa', 51, 60), ('Bangladesh', 1227, 171)]
    rows = r.sample(data, 3 if D <= 3 else 4)

    def cls(v):
        return 'no stress' if v >= 1700 else 'water stress' if v >= 1000 else 'water scarcity' if v >= 500 else 'absolute scarcity'
    per = [(n, w * 1e9 / (p * 1e6)) for n, w, p in rows]
    intro = ('Table 6.2 shows total renewable water resources (km³ per year) and population (millions): ' + '; '.join(f'{n} {fmt(w, 2)} km³, {fmt(p, 1)} million' for n, w, p in rows)
             + '. Falkenmark indicator (m³ per person per year): 1700 or more no stress; 1000-1699 water stress; 500-999 water scarcity; below 500 absolute scarcity. 1 km³ = 10⁹ m³.')
    n0, v0 = per[0]
    if D == 1:
        return MCQ(r, intro + f' What is the renewable water per person in {n0}?', f'{nf(v0)} m³', [f'{nf(v0 / 1000)} m³', f'{nf(v0 * 10)} m³', f'{nf(v0 / 10)} m³', f'{nf(v0 * 2)} m³'],
                   f'{fmt(rows[0][1], 2)} × 10⁹ ÷ {fmt(rows[0][2], 1)} × 10⁶ = {nf(v0)} m³. [1]')
    parts = [
        L('Calculate the renewable water available per person per year for each country.', '; '.join(f'{n} {nf(v)} m³' for n, v in per), 'conversion of units [1]; all correct [1] [2]'),
        L('Classify each country using the Falkenmark indicator.', '; '.join(f'{n}: {cls(v)}' for n, v in per), 'all correct [2], two correct [1] [2]'),
        L('Suggest why a country with no water stress on this indicator may still have water shortages.', 'Water may be unevenly distributed in space and time (seasons, regions); lack of infrastructure or money (economic scarcity); pollution makes water unusable.', '1 mark per point up to [2]'),
        L('Suggest two strategies that a country with absolute scarcity could use.', 'Desalination; recycling wastewater; importing virtual water as food; drip irrigation and reducing agricultural use; reducing leaks.', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D)


@e2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e2_use(r, D):
    cty = r.choice(['a city in ' + r.choice(['India', 'Egypt', 'Mexico', 'Morocco', 'Australia', 'Spain']), 'a town in a semi-arid region', 'a coastal city'])
    pop = r.choice([200000, 500000, 1200000, 3000000])
    lpd = r.choice([90, 120, 150, 200, 250])
    leak = r.choice([20, 25, 30, 40])
    need = pop * lpd / 1000   # m³ per day delivered
    treat = need / (1 - leak / 100)
    intro = f'{cap(cty)} has {nf(pop)} people who each use on average {lpd} litres of water per day. {leak}% of the water put into the supply network is lost through leaks.'
    if D == 1:
        return MCQ(r, intro + ' How much water, in m³, do the people use each day?', f'{nf(need)} m³', [f'{nf(need * 1000)} m³', f'{nf(need / 10)} m³', f'{nf(treat)} m³', f'{nf(need * 365)} m³'], f'{nf(pop)} × {lpd} ÷ 1000 = {nf(need)} m³. [1]')
    cut = r.choice([10, 15, 20])
    parts = [
        L('Calculate the volume of water used by the population per day in m³ (1 m³ = 1000 litres).', f'{nf(need)} m³', f'{nf(pop)} × {lpd} = {nf(pop * lpd)} litres [1]; ÷ 1000 = {nf(need)} m³ [1] [2]'),
        L('Calculate the volume that must be put into the network each day to allow for leakage.', f'{nf(treat)} m³', f'{nf(need)} ÷ {1 - leak / 100:.2f} = {nf(treat)} m³ [1]'),
        L('Calculate the volume lost through leaks in a year.', f'{nf((treat - need) * 365)} m³', f'({nf(treat)} − {nf(need)}) × 365 = {nf((treat - need) * 365)} m³ [1]'),
        L(f'A water-saving campaign reduces use per person by {cut}%. Calculate the new daily use in m³.', f'{nf(need * (1 - cut / 100))} m³', f'{nf(need)} × {1 - cut / 100:.2f} = {nf(need * (1 - cut / 100))} [1]'),
        L('Suggest two ways the city could reduce water demand.', 'Water metering and pricing; efficient appliances such as low-flow showers and dual-flush toilets; grey-water reuse; education campaigns; hosepipe bans.', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D)


e3 = T('Food production systems: agriculture types and their environmental impacts', 'food production systems', 'agriculture types')
build(e3, {
    'terms': [
        ('subsistence farming', 'farming to produce food mainly for the farmer’s own family, with little left to sell'),
        ('commercial farming', 'farming to produce crops or animals for sale at a profit'),
        ('intensive farming', 'farming with high inputs of labour, capital or chemicals per unit area to obtain high yields'),
        ('extensive farming', 'farming with low inputs per unit area over large areas, such as cattle ranching'),
        ('monoculture', 'growing a single crop over a large area, often year after year'),
        ('pastoral farming', 'the rearing of animals for meat, milk, wool or hides'),
        ('arable farming', 'the growing of crops'),
        ('aquaculture', 'the farming of fish, shellfish or aquatic plants in controlled conditions'),
    ],
    'mcq': [
        ('Which farming type is intensive and commercial?', 'Battery poultry farming', ['Nomadic herding', 'Shifting cultivation', 'Ranching in the Australian outback'], '[1]'),
        ('Shifting cultivation is sustainable when', 'population density is low and plots are left fallow for many years', ['fertilisers are added every year', 'the same plot is farmed continuously', 'forest is permanently cleared'], '[1]'),
        ('Which environmental impact is linked to shrimp farming in South-East Asia?', 'Destruction of mangrove forests', ['Acid rain', 'Ozone depletion', 'Glacier retreat'], '[1]'),
        ('Which is an input to a farming system?', 'Fertiliser', ['Milk', 'Harvesting', 'Profit'], 'Inputs → processes → outputs. [1]'),
        ('Livestock produce methane mainly through', 'digestion in ruminants such as cattle', ['photosynthesis', 'combustion of fuel', 'fertiliser runoff'], 'Enteric fermentation. [1]'),
    ],
    'explain': [
        ('Explain the environmental impacts of intensive arable farming.', 'Fertiliser runoff causes eutrophication; pesticides harm non-target species and accumulate in food chains; removal of hedgerows reduces habitats and increases wind erosion; heavy machinery compacts soil; monoculture lowers biodiversity; high fossil fuel use.', '1 mark per developed impact up to [4]'),
        ('Explain why meat production has a greater environmental impact than crop production.', 'Energy is lost between trophic levels, so far more land, water and feed are needed per kilogram of food; cattle emit methane; forests are cleared for pasture and feed crops such as soya.', 'trophic efficiency [1]; land / water use [1]; methane or deforestation [1] [3]'),
        ('Describe the characteristics of a nomadic pastoral farming system.', 'Herders move with animals (camels, goats, cattle) seasonally to find water and grazing; low inputs; subsistence with some trade; adapted to dry environments such as the Sahel.', '1 mark per characteristic up to [3]'),
        ('Explain how aquaculture can be both a solution and a problem for fish supply.', 'It reduces pressure on wild stocks and provides protein and income; but it can destroy mangroves, pollute water with waste and antibiotics, spread disease to wild fish, and uses wild fish for feed.', 'solution [1]; problems [2] [3]'),
    ],
    'claims': [
        ('Organic farming produces no environmental impacts.', False, 'It avoids synthetic chemicals but often has lower yields, so more land may be needed; manure can still cause pollution.'),
        ('Livestock farming is a significant source of greenhouse gas emissions.', True, 'Livestock account for about 14.5% of human greenhouse gas emissions (FAO), mainly methane and emissions linked to land clearance.'),
        ('Monocultures increase biodiversity on farms.', False, 'They replace varied habitats with a single species, reducing biodiversity and increasing vulnerability to pests.'),
    ],
    'cases': [(
        ['Fig. 6.3 is a systems diagram of a commercial dairy farm in {c}: inputs include feed, fertiliser, water and energy; processes include milking and grazing; outputs include milk, calves, manure and methane.',
         'A palm oil plantation has replaced lowland rainforest in Borneo. It covers 5000 ha and uses fertilisers and pesticides.'],
        [('Identify one input, one process and one output of the farming system.', 'Input: feed, fertiliser, labour or machinery; process: grazing, milking, planting or harvesting; output: milk, palm oil, crops or waste.', '1 mark each [3]'),
         ('Describe two environmental impacts of this farming system.', 'Loss of habitat and biodiversity; greenhouse gas emissions; water pollution from fertilisers and manure; soil degradation.', '1 mark each up to [2]'),
         ('Explain how the farm could reduce its impact on nearby rivers.', 'Buffer strips of vegetation; precise fertiliser application; store manure safely; prevent animals from entering rivers.', '1 mark per method up to [2]'),
         ('Suggest why governments in some countries support the expansion of such farms.', 'Export earnings, jobs, rural development and tax revenue; food or fuel production for growing demand.', '[2]')])],
    'essays': [
        ('intensive farming is necessary to feed the world’s growing population',
         ['Intensive methods (high-yielding varieties, fertiliser, irrigation) roughly tripled cereal production since 1960 and use less land per tonne than extensive systems.'],
         ['Intensive farming causes eutrophication, soil degradation, biodiversity loss and high emissions; about a third of food is wasted; sustainable intensification, agroecology and reducing meat consumption may be better.'],
         'High yields are needed, but they must be achieved sustainably, with less waste and fairer distribution.',
         ['Green Revolution', 'environmental costs', 'alternatives']),
    ],
})
compare_item(e3, [
    ('intensive farming', 'extensive farming', 'Intensive farming uses high inputs per hectare on small areas for high yields; extensive farming uses low inputs over large areas, giving low yields per hectare.', 'Both can be commercial and both alter natural ecosystems.'),
    ('subsistence farming', 'commercial farming', 'Subsistence farming produces food mainly for the family with low inputs; commercial farming produces for sale at a profit, often using machinery and chemicals.', 'Both depend on climate and soil and can cause land degradation if mismanaged.'),
])


@e3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e3_yield(r, D):
    crop = r.choice(['maize', 'wheat', 'rice', 'soya beans', 'potatoes', 'sorghum'])
    area = r.choice([2, 4, 5, 8, 12, 20])
    y0 = round(r.uniform(1.0, 2.5), 1)
    y1 = round(y0 * r.uniform(1.5, 3.0), 1)
    fert = r.choice([60, 100, 150, 200])
    intro = (f'A farmer in {r.choice(["Malawi", "India", "Vietnam", "Kenya", "Brazil", "Bangladesh", "Ethiopia", "Mexico"])} grows {crop} on {area} ha. Traditional methods gave a yield of {fmt(y0, 1)} t/ha. '
             f'After using improved seeds, irrigation and {fert} kg/ha of fertiliser the yield rose to {fmt(y1, 1)} t/ha.')
    if D == 1:
        return MCQ(r, intro + ' What was the percentage increase in yield?', f'{f1(pc(y0, y1))}%', [f'{f1(y1 - y0)}%', f'{f1(y1 / y0 * 10)}%', f'{f1(-pc(y1, y0))}%', f'{f1(pc(y0, y1) / 2)}%'],
                   f'({fmt(y1, 1)} − {fmt(y0, 1)}) ÷ {fmt(y0, 1)} × 100 = {f1(pc(y0, y1))}%. [1]')
    extra = (y1 - y0) * area
    parts = [
        L('Calculate the percentage increase in yield.', f'{f1(pc(y0, y1))}%', f'({fmt(y1, 1)} − {fmt(y0, 1)}) ÷ {fmt(y0, 1)} × 100 [1] = {f1(pc(y0, y1))}% [1] [2]'),
        L('Calculate the extra production from the whole farm.', f'{s3(extra)} t', f'({fmt(y1, 1)} − {fmt(y0, 1)}) × {area} = {s3(extra)} t [1]'),
        L('Calculate the extra grain produced per kg of fertiliser applied.', f'{s3((y1 - y0) * 1000 / fert)} kg', f'({fmt(y1 - y0, 1)} × 1000) ÷ {fert} = {s3((y1 - y0) * 1000 / fert)} kg [1]'),
        L('Explain two environmental risks of the new methods.', 'Fertiliser runoff causing eutrophication; over-irrigation causing salinisation or waterlogging; lowering water tables; loss of crop genetic diversity; pesticide pollution.', '1 mark each risk with explanation [2]'),
        L('Suggest why some small farmers cannot adopt these methods.', 'High cost of seeds, fertiliser and irrigation; lack of credit; no access to water or markets; seeds must be bought every year.', '1 mark per reason up to [2]'),
    ]
    return comp(r, intro, parts, D)


@e3.add('C3', (2, 3, 4, 5), 'numerical')
def e3_footprint(r, D):
    foods = [('beef', 15400, 25, 60), ('chicken', 4300, 7.5, 6), ('rice', 2500, 1.3, 4), ('wheat bread', 1600, 0.6, 2), ('lentils', 5900, 0.8, 3), ('potatoes', 290, 0.3, 1), ('milk', 1020, 1.4, 2)]
    a, b = r.sample(foods, 2)
    if a[1] < b[1]:
        a, b = b, a
    m = r.choice([0.5, 1, 2, 5])
    intro = (f'Approximate water footprints and greenhouse gas emissions per kg of food: {a[0]} {nf(a[1])} litres and {fmt(a[2], 1)} kg CO₂e; '
             f'{b[0]} {nf(b[1])} litres and {fmt(b[2], 1)} kg CO₂e.')
    parts = [
        L(f'Calculate the water saved by replacing {fmt(m, 1)} kg of {a[0]} with the same mass of {b[0]}.', f'{nf((a[1] - b[1]) * m)} litres', f'({nf(a[1])} − {nf(b[1])}) × {fmt(m, 1)} = {nf((a[1] - b[1]) * m)} [1]'),
        L(f'Calculate how many times more water is needed per kg of {a[0]} than {b[0]}.', s3(a[1] / b[1]), f'{nf(a[1])} ÷ {nf(b[1])} = {s3(a[1] / b[1])} [1]'),
        L(f'Calculate the percentage reduction in emissions if a family replaces {a[0]} with {b[0]}.', f'{f1((a[2] - b[2]) / a[2] * 100)}%' if a[2] > b[2] else 'There is no reduction: emissions rise.',
          f'({fmt(a[2], 1)} − {fmt(b[2], 1)}) ÷ {fmt(a[2], 1)} × 100 [1] = {f1((a[2] - b[2]) / a[2] * 100)}% [1] [2]' if a[2] > b[2] else 'comparison [2]'),
        L('Explain why animal products usually have larger water footprints than crops.', 'Animals eat feed crops that require water, and energy is lost between trophic levels, so much more crop (and water) is needed per kg of food; animals also drink water.', '[2]'),
        L('Suggest one limitation of using water footprint figures to compare foods.', 'They are global averages; much of the water may be rainfall (green water) rather than irrigation; local scarcity differs.', '[1]'),
    ]
    return comp(r, intro, parts, D)


e4 = T('Food security and sustainable agriculture', 'food security', 'sustainable agriculture')
build(e4, {
    'terms': [
        ('food security', 'when all people at all times have physical and economic access to sufficient, safe and nutritious food to meet their dietary needs'),
        ('food insecurity', 'a lack of reliable access to sufficient, affordable, nutritious food'),
        ('undernutrition', 'a condition caused by eating too little energy or protein for a healthy life'),
        ('malnutrition', 'a condition caused by a diet lacking the right balance of nutrients, including undernutrition and obesity'),
        ('Green Revolution', 'the use from the 1960s of high-yielding crop varieties, irrigation, fertilisers and pesticides to increase food production in LICs'),
        ('agroforestry', 'growing trees together with crops and/or livestock on the same land'),
        ('genetically modified (GM) crop', 'a crop whose DNA has been altered to give a desired characteristic, such as pest or drought resistance'),
        ('integrated pest management', 'controlling pests using a combination of biological control, crop rotation, resistant varieties and minimal pesticide use'),
    ],
    'mcq': [
        ('Which of these is one of the four pillars of food security?', 'Access', ['Profit', 'Exports', 'Mechanisation'], 'Availability, access, utilisation and stability. [1]'),
        ('About what proportion of food produced globally is lost or wasted?', 'About one third', ['About 1%', 'About two thirds', 'About 90%'], 'FAO estimate. [1]'),
        ('Golden rice is genetically modified to contain', 'beta-carotene (provitamin A)', ['extra protein', 'iron only', 'resistance to frost'], '[1]'),
        ('Which method is part of sustainable agriculture?', 'Crop rotation with legumes', ['Continuous monoculture', 'Draining wetlands', 'Burning crop residues'], '[1]'),
        ('Which country is often cited as a Green Revolution success story for wheat and rice?', 'India (Punjab)', ['Mongolia', 'Iceland', 'Chad'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of food insecurity in low-income countries.', 'Poverty prevents people buying food; drought, floods and pests reduce harvests; conflict disrupts farming and supply; poor storage and transport cause losses; rapid population growth; rising food prices.', '1 mark per cause up to [4]'),
        ('Explain how the Green Revolution increased food production but also caused problems.', 'High-yielding varieties with fertiliser and irrigation doubled or tripled yields; but costs excluded poorer farmers, increased debt and inequality, caused salinisation and falling water tables, pollution from chemicals and loss of crop diversity.', 'benefit [1]; problems [2] [3]'),
        ('Explain how agroforestry can improve food security and the environment.', 'Trees protect soil from erosion, add organic matter and nitrogen (legume trees), provide shade, fuel, fruit and fodder; diverse products reduce risk; trees store carbon and provide habitat.', '1 mark per point up to [3]'),
        ('Explain the arguments for and against growing GM crops.', 'For: higher yields, pest and drought resistance, less pesticide use, added nutrients. Against: cross-pollination with wild relatives, pest resistance evolving, loss of biodiversity, corporate control of seeds and costs for farmers, consumer concerns.', 'for [1-2]; against [1-2] [4]'),
    ],
    'claims': [
        ('Hunger is caused mainly by the world not producing enough food.', False, 'The world produces enough calories for everyone; hunger is mainly caused by poverty, conflict, waste and unequal distribution.'),
        ('Reducing food waste can improve food security.', True, 'Less waste means more food available and lower prices, and less pressure on land, water and energy.'),
        ('Sustainable agriculture always produces lower yields.', False, 'Methods such as agroforestry, conservation agriculture and integrated pest management can maintain or increase yields over time.'),
    ],
    'cs': [('a strategy to increase food security', [
        ('the Green Revolution in Punjab, India', {
            'strategy': 'From the 1960s high-yielding wheat and rice varieties, tube-well irrigation, fertiliser and pesticides, supported by government price guarantees.',
            'evaluation': 'Punjab became India’s breadbasket and India became self-sufficient in grain; but the water table is falling by up to 1 m per year, soils are degraded, pesticide use is linked to health problems, and many farmers are in debt.'}),
        ('farmer-managed natural regeneration in Niger', {
            'strategy': 'Farmers protect and manage tree stumps that regrow in their fields, pruning them for fuel and fodder, instead of clearing them.',
            'evaluation': 'About 5 million hectares re-greened since the 1980s; trees reduce wind erosion, improve soil fertility and provide food and income, increasing grain yields; low-cost and farmer-led, though it depends on secure land rights.'}),
    ], [
        ('describe the strategy', 'strategy', 'named methods, scale, organisation'),
        ('evaluate the success of the strategy in improving food security sustainably', 'evaluation', 'yields, social and environmental effects, judgement'),
    ])],
    'essays': [
        ('technology is the key to achieving global food security',
         ['High-yielding and GM varieties, precision farming and irrigation have greatly increased production (Green Revolution); new drought-resistant crops can help adapt to climate change.'],
         ['Food insecurity is mainly caused by poverty, conflict and waste; technology can be costly and damage the environment; land rights, fair trade, reducing waste and empowering women farmers are also essential.'],
         'Technology is necessary but not sufficient; access, distribution and sustainability are as important as production.',
         ['Green Revolution', 'GM crops', 'access and distribution']),
    ],
})


@e4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def e4_cal(r, D):
    cty = r.choice(['Country P', 'Country Q', 'a Sahel country', 'an island state', 'a landlocked country'])
    pop = r.choice([5, 12, 20, 35, 60]) * 1e6
    prod = round(pop * r.uniform(0.12, 0.32) / 1e5) * 1e5   # t grain
    loss = r.choice([10, 15, 20, 25, 30])
    kcal_per_kg = 3500
    need = 2100
    avail = prod * (1 - loss / 100) * 1000 * kcal_per_kg / pop / 365
    intro = (f'{cap(cty)} has a population of {nf(pop / 1e6)} million and produces {fmt(prod / 1e6, 1)} million tonnes of grain a year. {loss}% is lost after harvest. '
             f'Grain provides about 3500 kcal per kg and each person needs about 2100 kcal per day.')
    if D == 1:
        return MCQ(r, intro + ' How much grain is lost after harvest each year?', f'{nf(prod * loss / 100)} t', [f'{nf(prod * (1 - loss / 100))} t', f'{nf(prod * loss / 1000)} t', f'{nf(prod)} t', f'{nf(prod * loss / 50)} t'],
                   f'{nf(prod)} × {loss}% = {nf(prod * loss / 100)} t. [1]')
    parts = [
        L('Calculate the mass of grain available after losses.', f'{nf(prod * (1 - loss / 100))} t', f'{nf(prod)} × {1 - loss / 100:.2f} = {nf(prod * (1 - loss / 100))} t [1]'),
        L('Calculate the grain energy available per person per day.', f'{nf(avail)} kcal', f'{nf(prod * (1 - loss / 100) * 1000)} kg × 3500 [1]; ÷ ({nf(pop)} × 365) = {nf(avail)} kcal [1] [2]'),
        L('State whether grain production can meet the population’s energy needs and calculate the surplus or shortfall per person per day.',
          (f'Yes: surplus of {nf(avail - need)} kcal per person per day.' if avail >= need else f'No: shortfall of {nf(need - avail)} kcal per person per day.'), f'comparison with 2100 [1]; difference [1] [2]'),
        L('Suggest two ways of reducing post-harvest losses.', 'Improved storage (hermetic bags, silos) to keep out pests and moisture; better drying; better roads and transport to markets; cold chains.', '1 mark each [2]'),
        L('Explain why sufficient food production does not guarantee food security.', 'People may not be able to afford food (access); distribution may be unequal; food may be exported; diets may lack nutrients (utilisation); supply may be unstable.', '1 mark per point up to [2]'),
    ]
    return comp(r, intro, parts, D)


CHAPTERS[6] = [e1, e2, e3, e4]


# ============================================================== CHAPTER 7: Environmental management and sustainability

m1 = T('Sustainable development: definitions, the triple bottom line and the SDGs', 'sustainable development', 'triple bottom line', 'sdgs')
build(m1, {
    'terms': [
        ('sustainable development', 'development that meets the needs of the present without compromising the ability of future generations to meet their own needs (Brundtland Report, 1987)'),
        ('triple bottom line', 'judging the success of a project or business by its social, environmental and economic performance (people, planet, profit)'),
        ('Sustainable Development Goals (SDGs)', 'the 17 goals agreed by UN member states in 2015 to be achieved by 2030, such as ending poverty and taking climate action'),
        ('natural capital', 'the world’s stocks of natural resources, such as soils, water, forests and biodiversity, that provide goods and services'),
        ('ecosystem services', 'the benefits that people obtain from ecosystems, such as food, clean water, pollination and climate regulation'),
        ('intergenerational equity', 'fairness between present and future generations in the use of resources'),
        ('circular economy', 'an economic system that keeps materials in use for as long as possible through reuse, repair and recycling, designing out waste'),
        ('environmental stewardship', 'the responsible use and protection of the environment for present and future generations'),
    ],
    'mcq': [
        ('How many Sustainable Development Goals are there?', '17', ['8', '12', '25'], 'Replaced the 8 Millennium Development Goals in 2015. [1]'),
        ('The Brundtland Report that defined sustainable development was published in', '1987', ['1972', '1992', '2015'], '“Our Common Future”. [1]'),
        ('The three elements of the triple bottom line are', 'social, environmental and economic', ['local, national and global', 'reduce, reuse and recycle', 'land, labour and capital'], '[1]'),
        ('SDG 13 is', 'Climate action', ['Zero hunger', 'Life below water', 'Quality education'], '[1]'),
        ('Which is an example of an ecosystem service provided by wetlands?', 'Flood regulation and water purification', ['Mineral extraction', 'Fossil fuel formation', 'Ozone production'], '[1]'),
    ],
    'explain': [
        ('Explain why there can be conflict between economic development and environmental sustainability.', 'Economic growth often relies on resource extraction, fossil fuels and land conversion, causing pollution and habitat loss; environmental protection may raise costs or limit jobs in the short term.', '1 mark per developed point up to [3]'),
        ('Explain how the triple bottom line can be used to evaluate a development project.', 'The project is judged on its social impacts (jobs, health, communities), environmental impacts (pollution, habitats, emissions) and economic impacts (profit, income); a sustainable project performs well on all three.', 'three elements explained [2]; application [1] [3]'),
        ('Explain why progress towards the SDGs varies between countries.', 'Differences in wealth and investment, governance and corruption, conflict, debt, climate vulnerability and population growth; the COVID-19 pandemic reversed progress in many LICs.', '1 mark per reason up to [3]'),
        ('Explain the idea of a circular economy and its environmental benefits.', 'Products are designed to be durable, repaired, reused and recycled, keeping materials in use; this reduces extraction of raw materials, energy use, waste and pollution.', 'definition [1]; benefits [2] [3]'),
    ],
    'claims': [
        ('Sustainable development means stopping all economic growth.', False, 'It aims to meet present needs while protecting resources for the future, through more efficient and fairer growth rather than no growth.'),
        ('The SDGs apply only to low-income countries.', False, 'Unlike the Millennium Development Goals, the SDGs apply to all countries, including high-income ones.'),
        ('Ecosystem services have economic value.', True, 'Services such as pollination, flood control and water purification are estimated to be worth trillions of dollars per year.'),
    ],
    'essays': [
        ('sustainable development is an unachievable goal',
         ['Global resource use exceeds biocapacity; emissions are still rising; many SDG targets are off track for 2030; there are conflicts between growth and protection.'],
         ['Many countries have decoupled growth from emissions (e.g. the UK, Sweden); renewable energy is growing quickly; local projects (agroforestry, ecotourism) show sustainable development in practice.'],
         'Full sustainability is difficult but progress is possible; it is better seen as a direction of travel than a fixed end point.',
         ['SDGs', 'decoupling', 'named projects']),
    ],
})


@m1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m1_sdg(r, D):
    ind = r.choice([('the percentage of the population with access to safely managed drinking water', 'SDG 6', 100, 'clean water and sanitation'),
                    ('the percentage of the population with access to electricity', 'SDG 7', 100, 'affordable and clean energy'),
                    ('the percentage of children completing primary school', 'SDG 4', 100, 'quality education'),
                    ('the percentage of land area covered by forest', 'SDG 15', None, 'life on land'),
                    ('the percentage of the population that is undernourished', 'SDG 2', 0, 'zero hunger')])
    name, sdg, target, title = ind
    y0, y1 = r.choice([(2010, 2020), (2005, 2020), (2012, 2022)])
    if target == 0:
        v0 = r.randint(18, 35)
        v1 = v0 - r.randint(2, 10)
    elif target is None:
        v0 = r.randint(30, 60)
        v1 = v0 - r.randint(1, 6)
    else:
        v0 = r.randint(40, 75)
        v1 = min(98, v0 + r.randint(5, 18))
    cty = r.choice(['Country A', 'Country B', 'a low-income country', 'a lower-middle-income country'])
    rate = (v1 - v0) / (y1 - y0)
    intro = f'In {cty}, {name} was {v0}% in {y0} and {v1}% in {y1}. This is an indicator for {sdg} ({title}).'
    if D == 1:
        return MCQ(r, intro + ' What was the mean change in percentage points per year?', f'{"+" if rate > 0 else ""}{f2(rate)}', [f'{"+" if rate > 0 else ""}{f2(rate * 2)}', f'{f2(-rate)}', f'{"+" if rate > 0 else ""}{f2((v1 - v0) / 100)}', f'{"+" if rate > 0 else ""}{f2(rate / 2)}'],
                   f'({v1} − {v0}) ÷ {y1 - y0} = {f2(rate)}. [1]')
    parts = [
        L('Calculate the mean change in percentage points per year.', f'{f2(rate)} per year', f'({v1} − {v0}) ÷ {y1 - y0} = {f2(rate)} [1]'),
    ]
    if target is not None:
        yrs = (target - v1) / rate if rate else None
        on = yrs is not None and y1 + yrs <= 2030
        parts.append(L(f'Assuming this rate continues, determine whether the country will reach the target of {target}% by 2030.', (f'It would reach {target}% in about {round(y1 + yrs)}, so ' + ('it is on track.' if on else 'it is not on track.')) if yrs else 'No progress, so not on track.',
                       f'({target} − {v1}) ÷ {f2(rate)} = {s3(yrs) if yrs else "-"} years [1]; conclusion [1] [2]'))
    else:
        parts.append(L('Explain why this trend is a concern for sustainable development.', 'Forest loss reduces biodiversity, carbon storage, soil and water protection and the livelihoods of forest communities, so future generations lose natural capital.', '1 mark per point up to [2]'))
    parts += [
        L('Suggest why progress may slow as the indicator approaches the target.', 'The remaining people are hardest to reach: remote rural areas, the poorest groups and conflict zones, where costs are highest.', '[2]'),
        L('Explain how progress on this goal could support other SDGs.', {'SDG 6': 'Clean water reduces disease (SDG 3), saves time collecting water so girls can attend school (SDG 4) and supports work (SDG 8).',
                                                                          'SDG 7': 'Electricity supports education, health clinics, businesses and clean cooking, reducing indoor air pollution (SDGs 3, 4, 8).',
                                                                          'SDG 4': 'Education raises incomes (SDG 1), improves health (SDG 3), empowers women (SDG 5) and lowers fertility.',
                                                                          'SDG 15': 'Forests regulate water (SDG 6), store carbon (SDG 13) and support livelihoods (SDG 1).',
                                                                          'SDG 2': 'Better nutrition improves health (SDG 3) and school performance (SDG 4) and productivity (SDG 8).'}[sdg], '1 mark per link up to [2]'),
    ]
    return comp(r, intro, parts, D)


m2 = T('Environmental impact assessment and monitoring', 'environmental impact assessment', 'monitoring')
build(m2, {
    'terms': [
        ('environmental impact assessment (EIA)', 'a formal process to predict and evaluate the environmental effects of a proposed development before a decision is made'),
        ('baseline study', 'a survey of environmental conditions before a development begins, used for comparison later'),
        ('screening', 'the first stage of EIA, deciding whether a project needs a full assessment'),
        ('scoping', 'the stage of EIA that identifies which impacts are likely to be significant and should be studied'),
        ('mitigation measures', 'actions planned to avoid, reduce or compensate for the negative impacts of a development'),
        ('environmental monitoring', 'repeated measurement of environmental indicators over time to detect change'),
        ('stakeholder', 'a person or group with an interest in, or affected by, a development'),
        ('cumulative impact', 'the combined effect of several developments or activities on the environment over time'),
    ],
    'mcq': [
        ('Which stage of EIA comes first?', 'Screening', ['Monitoring', 'Decision-making', 'Mitigation'], '[1]'),
        ('Why is a baseline study needed?', 'To provide data on conditions before development for later comparison', ['To build the project faster', 'To calculate profits', 'To avoid public consultation'], '[1]'),
        ('Which is an example of a mitigation measure for a new road?', 'Wildlife underpasses and noise barriers', ['Increasing the speed limit', 'Removing hedgerows', 'Building more junctions'], '[1]'),
        ('Satellite imagery is most useful for monitoring', 'changes in forest cover over large areas', ['the pH of a stream', 'the diversity of soil invertebrates', 'noise levels in a classroom'], '[1]'),
        ('A criticism of EIA is that', 'it is often paid for by the developer and may be biased', ['it always stops developments', 'it never includes public consultation', 'it is only used for small projects'], '[1]'),
    ],
    'explain': [
        ('Describe the main stages of an environmental impact assessment.', 'Screening; scoping of key impacts; baseline survey; prediction and evaluation of impacts; mitigation measures; public consultation; environmental impact statement; decision; monitoring after approval.', '1 mark per stage in order up to [4]'),
        ('Explain the importance of public consultation in an EIA.', 'Local people know the area and may identify impacts experts miss; it allows stakeholders to raise concerns and influence decisions; it increases transparency and acceptance of the project.', '1 mark per point up to [3]'),
        ('Explain the limitations of environmental impact assessment.', 'Predictions are uncertain; it may be done quickly or by consultants paid by the developer; cumulative and long-term impacts may be missed; recommendations may not be enforced; monitoring may not happen.', '1 mark per limitation up to [3]'),
        ('Explain why long-term monitoring is needed after a development is completed.', 'To check whether predicted impacts were accurate and mitigation is working, detect unexpected impacts early and take action, and improve future assessments.', '1 mark per point up to [3]'),
    ],
    'claims': [
        ('An EIA decides whether a project goes ahead.', False, 'The EIA informs decision-makers; the decision is made by a government or planning authority, which may approve projects with significant impacts.'),
        ('An EIA should consider social as well as environmental impacts.', True, 'Impacts on communities, health, cultural heritage and livelihoods are usually included.'),
        ('Monitoring is only needed before a project starts.', False, 'Monitoring during and after construction checks impacts and whether mitigation is effective.'),
    ],
    'cases': [(
        ['A government is considering a proposal to build a large hydroelectric dam in {h} that would flood 120 km² of forested valley, including two villages, to supply electricity and water for irrigation.',
         'A company proposes a new coastal resort on a mangrove-fringed bay in {m}, with a hotel, a marina and a golf course.'],
        [('Explain why an environmental impact assessment is needed for this project.', 'It is a large project with potentially significant impacts on habitats, water, and communities; the EIA identifies and evaluates impacts and mitigation before a decision is made.', '[2]'),
         ('Identify three stakeholders and suggest the view of each.', 'Local residents (concern over displacement or loss of livelihoods; possible jobs); developer or company (profit, wants approval); environmental NGOs (concern for habitats); government (economic growth, energy or tourism revenue).', '1 mark per stakeholder with view [3]'),
         ('Describe how a baseline survey of the area could be carried out.', 'Map habitats; quadrat and transect surveys of vegetation; bird and mammal counts; water quality and flow measurements; questionnaires with local people; air and noise measurements.', '1 mark per method up to [3]'),
         ('Suggest mitigation measures that could reduce the impacts.', 'Fish ladders or buffer zones; relocation and compensation for residents; replanting or protecting equivalent habitat; controlling runoff and waste; limiting construction to certain seasons.', '1 mark per measure up to [3]'),
         ('Explain why monitoring should continue after construction.', 'To check that predicted impacts were accurate and mitigation is working, and to detect unexpected impacts.', '[2]')])],
    'essays': [
        ('environmental impact assessments are effective in protecting the environment from development',
         ['EIA has led to changes in project design, mitigation and sometimes cancellation; it gives the public a voice and creates baseline data.'],
         ['EIAs are often biased, rushed or ignored; large projects such as the Belo Monte Dam in Brazil went ahead despite serious concerns; cumulative impacts are often missed; monitoring is weak.'],
         'EIA is valuable but its effectiveness depends on independent assessment, public participation and enforcement.',
         ['stages of EIA', 'named projects', 'enforcement']),
    ],
})


@m2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m2_matrix(r, D):
    proj = r.choice(['a new airport runway', 'a quarry', 'a motorway', 'a wind farm', 'a shrimp farm', 'a coastal resort'])
    factors = r.sample(['air quality', 'noise', 'water quality', 'habitats and wildlife', 'landscape', 'employment', 'traffic', 'soil', 'local economy'], 4)
    vals = []
    for f in factors:
        sign = 1 if f in ('employment', 'local economy') else -1
        mag = r.randint(1, 5)
        imp = r.randint(1, 5)
        vals.append((f, sign * mag, imp))
    tot = sum(m * i for _, m, i in vals)
    intro = (f'Part of an impact matrix for {proj} gives each impact a magnitude (−5 to +5) and an importance (1 to 5). The score for each factor is magnitude × importance. '
             + '; '.join(f'{f}: magnitude {"+" if m > 0 else MINUS}{abs(m)}, importance {i}' for f, m, i in vals) + '.')
    if D == 1:
        f, m, i = vals[0]
        return MCQ(r, intro + f' What is the score for {f}?', f'{"+" if m * i > 0 else MINUS}{abs(m * i)}', [f'{"+" if m * i < 0 else MINUS}{abs(m * i)}', f'{"+" if m + i > 0 else MINUS}{abs(m + i)}', f'{abs(m * i) + 2}', f'{abs(m) + i}'],
                   f'{m} × {i} = {m * i}. [1]')
    worst = min(vals, key=lambda x: x[1] * x[2])
    parts = [
        L('Calculate the score for each factor and the total score.', '; '.join(f'{f} {m * i}' for f, m, i in vals) + f'; total {tot}', 'scores [1]; total [1] [2]'),
        L('Identify the most significant negative impact.', f'{cap(worst[0])} (score {worst[1] * worst[2]})', '[1]'),
        L(f'Suggest a mitigation measure for the impact on {worst[0]}.', {'air quality': 'Dust suppression with water sprays, vehicle emission controls.', 'noise': 'Noise barriers, restricted working hours.', 'water quality': 'Settling ponds and treatment of runoff.',
                                                                          'habitats and wildlife': 'Wildlife corridors, habitat creation elsewhere (offsetting), timing works outside breeding seasons.', 'landscape': 'Screening with trees, careful design and restoration.',
                                                                          'traffic': 'Restricted lorry routes and times, improved junctions.', 'soil': 'Store topsoil, control erosion with vegetation.', 'employment': 'Train local people for jobs.', 'local economy': 'Use local suppliers.'}[worst[0]], '[1]'),
        L('Explain two limitations of using an impact matrix.', 'Scores are subjective and may be biased; very different impacts are added as if equal; indirect and cumulative impacts are hard to score; it does not show who is affected.', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D)


m3 = T('Waste management: reduce, reuse, recycle, landfill and incineration', 'waste management', 'recycle', 'landfill', 'incineration')
build(m3, {
    'terms': [
        ('waste hierarchy', 'the order of preference for managing waste: prevent and reduce, reuse, recycle, recover energy, and finally disposal'),
        ('landfill', 'the disposal of waste by burying it in the ground in a specially engineered site'),
        ('leachate', 'the polluted liquid that drains from waste in a landfill site'),
        ('incineration', 'the burning of waste at high temperatures, often to generate electricity (energy from waste)'),
        ('composting', 'the controlled aerobic decomposition of organic waste to produce a soil conditioner'),
        ('e-waste', 'discarded electrical and electronic equipment such as phones and computers, which contain valuable and toxic materials'),
        ('municipal solid waste', 'everyday waste from households and businesses collected by local authorities'),
        ('anaerobic digestion', 'the breakdown of organic waste by bacteria without oxygen, producing biogas and digestate'),
    ],
    'mcq': [
        ('Which is highest in the waste hierarchy?', 'Reduce (prevent) waste', ['Recycle', 'Incinerate with energy recovery', 'Landfill'], '[1]'),
        ('Which gas produced in landfill sites is a powerful greenhouse gas?', 'Methane', ['Oxygen', 'Nitrogen', 'Argon'], '[1]'),
        ('Agbogbloshie in Accra, Ghana became known for', 'informal processing of e-waste with burning of cables', ['a modern incinerator', 'zero waste policies', 'composting of food waste'], '[1]'),
        ('Which material can be recycled repeatedly without loss of quality?', 'Aluminium', ['Paper', 'Most plastics', 'Food waste'], '[1]'),
        ('A clay or plastic liner in a landfill site is used to', 'prevent leachate entering groundwater', ['generate electricity', 'speed up decomposition', 'attract birds'], '[1]'),
        ('Which country sends less than 1% of its household waste to landfill, using recycling and energy from waste?', 'Sweden', ['Egypt', 'Indonesia', 'Nigeria'], '[1]'),
    ],
    'explain': [
        ('Explain the environmental problems caused by landfill sites.', 'Leachate pollutes groundwater and rivers; methane is released, contributing to climate change and fire risk; land is used up; odour, pests and litter; plastics persist for centuries.', '1 mark per problem up to [3]'),
        ('Evaluate incineration as a method of waste disposal.', 'Advantages: reduces waste volume by about 90%; generates electricity or heat; less land needed. Disadvantages: emits CO₂ and pollutants such as dioxins if poorly controlled; toxic ash must be disposed of; may discourage recycling; expensive to build.', 'advantages [1-2]; disadvantages [1-2] [4]'),
        ('Explain why recycling rates are low in many low-income countries.', 'Limited collection services and infrastructure; little investment; much recycling is done informally by waste pickers; lack of markets for recycled materials; low awareness.', '1 mark per point up to [3]'),
        ('Explain why reducing waste is preferred to recycling it.', 'Reduction avoids the use of raw materials, energy and transport altogether; recycling still needs energy for collection and processing and some quality is lost.', '[2]'),
    ],
    'claims': [
        ('All plastics are easily recycled.', False, 'Many plastics are mixed, contaminated or low value; only about 9% of plastic ever produced has been recycled.'),
        ('Composting food waste can reduce methane emissions from landfill.', True, 'Aerobic composting produces CO₂ rather than methane, and diverts organic waste from landfill.'),
        ('Exporting waste to other countries solves the waste problem.', False, 'It moves the problem; poorly managed imported waste pollutes the receiving countries, which led to China’s 2018 ban and the Basel Convention plastics amendment.'),
    ],
    'cs': [('a waste management strategy', [
        ('Kamikatsu, Japan', {
            'strategy': 'A zero-waste town since 2003: residents sort waste into about 45 categories at a recycling centre; no rubbish collection or incineration; a reuse shop and crafts from waste.',
            'evaluation': 'About 80% of waste is recycled or composted, compared with about 20% nationally; costs of incineration were saved; but sorting is time-consuming, the town is small (about 1500 people) and some waste still cannot be recycled.'}),
        ('Sweden', {
            'strategy': 'Landfill taxes and a ban on landfilling organic and combustible waste; extensive recycling, deposit schemes for bottles and cans; about half of household waste is burned in energy-from-waste plants supplying district heating.',
            'evaluation': 'Less than 1% of household waste goes to landfill; but incineration emits CO₂, and Sweden imports waste to keep plants running, which may discourage waste reduction.'}),
        ('Lagos, Nigeria', {
            'strategy': 'Rapid growth produces over 10 000 tonnes of waste a day; much goes to open dumps such as Olusosun; the state introduced private collectors (PSP scheme), recycling start-ups such as Wecyclers and plans for energy-from-waste.',
            'evaluation': 'Collection has improved in wealthier districts, but much waste is dumped in drains and lagoons, causing flooding; dumpsite fires release toxic smoke; informal waste pickers face health risks.'}),
    ], [
        ('describe the strategies used to manage waste', 'strategy', 'named methods, scale, data'),
        ('evaluate the sustainability of the waste management strategy', 'evaluation', 'environmental, social, economic outcomes; judgement'),
    ])],
    'essays': [
        ('recycling is the most sustainable way to manage waste',
         ['Recycling saves raw materials and energy (aluminium recycling uses about 95% less energy), reduces landfill and creates jobs.'],
         ['Reduction and reuse are higher in the waste hierarchy; recycling uses energy, often downcycles plastics and depends on markets; much is exported or not actually recycled.'],
         'Recycling is better than disposal but less sustainable than reducing and reusing; it works best within a circular economy.',
         ['waste hierarchy', 'named examples', 'circular economy']),
    ],
})


@m3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m3_waste(r, D):
    cty = r.choice(['a city in ' + r.choice(['Kenya', 'Brazil', 'Indonesia', 'Turkey', 'Mexico', 'Vietnam']), 'a European city', 'a rapidly growing city'])
    pop = r.choice([250000, 600000, 1500000, 4000000])
    kg = round(r.uniform(0.4, 1.6), 1)
    rec = r.choice([5, 10, 15, 25, 35, 45])
    comp_ = r.choice([0, 5, 10, 15])
    lf = 100 - rec - comp_
    tot = pop * kg * 365 / 1000   # t/yr
    capm3 = r.choice([2, 5, 10]) * 1e6
    dens = 0.8   # t per m³ compacted
    life = capm3 * dens / (tot * lf / 100)
    intro = (f'{cap(cty)} has {nf(pop)} people, each producing {fmt(kg, 1)} kg of municipal solid waste per day. {rec}% is recycled, {comp_}% is composted and the rest is landfilled. '
             f'The landfill site has {nf(capm3 / 1e6)} million m³ of space left and compacted waste has a density of 0.8 t/m³.')
    if D == 1:
        return MCQ(r, intro + ' How much waste does the city produce in a year?', f'{nf(tot)} t', [f'{nf(tot * 1000)} t', f'{nf(pop * kg / 1000)} t', f'{nf(tot / 365)} t', f'{nf(tot * lf / 100)} t'],
                   f'{nf(pop)} × {fmt(kg, 1)} × 365 ÷ 1000 = {nf(tot)} t. [1]')
    newrec = min(70, rec + r.choice([15, 20, 25]))
    life2 = capm3 * dens / (tot * (100 - newrec - comp_) / 100)
    parts = [
        L('Calculate the total waste produced per year in tonnes.', f'{nf(tot)} t', f'{nf(pop)} × {fmt(kg, 1)} × 365 [1] ÷ 1000 = {nf(tot)} t [1] [2]'),
        L('Calculate the mass of waste sent to landfill each year.', f'{nf(tot * lf / 100)} t', f'{nf(tot)} × {lf}% = {nf(tot * lf / 100)} t [1]'),
        L('Calculate the remaining lifetime of the landfill site.', f'{s3(life)} years', f'capacity {nf(capm3 * dens)} t [1]; ÷ {nf(tot * lf / 100)} = {s3(life)} years [1] [2]'),
        L(f'Calculate the new lifetime if the recycling rate increases to {newrec}%.', f'{s3(life2)} years', f'landfilled {nf(tot * (100 - newrec - comp_) / 100)} t/yr [1]; {s3(life2)} years [1] [2]'),
        L('Suggest two ways the city could increase its recycling rate.', 'Separate kerbside collections; deposit-return schemes; landfill taxes; support and formalise waste pickers; education campaigns; recycling centres.', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D)


m4 = T('International agreements and the role of governments, NGOs and individuals', 'international agreements', 'governments, ngos and individuals', 'ngos')
build(m4, {
    'terms': [
        ('non-governmental organisation (NGO)', 'a non-profit organisation independent of government, such as WWF, Greenpeace or Friends of the Earth'),
        ('international agreement', 'a treaty or convention between countries to achieve a shared goal, such as reducing emissions or protecting species'),
        ('Kyoto Protocol', 'the 1997 agreement that set legally binding emission reduction targets for developed countries'),
        ('Paris Agreement', 'the 2015 agreement in which countries set nationally determined contributions to keep warming well below 2 °C'),
        ('nationally determined contribution (NDC)', 'a country’s own pledge under the Paris Agreement to reduce emissions and adapt to climate change'),
        ('Ramsar Convention', 'the 1971 international treaty for the conservation and wise use of wetlands'),
        ('CITES', 'the Convention on International Trade in Endangered Species of Wild Fauna and Flora (1973), which regulates trade in threatened species'),
        ('carbon tax', 'a charge on the carbon content of fuels, designed to reduce greenhouse gas emissions'),
    ],
    'mcq': [
        ('Which agreement regulates the trade in ivory?', 'CITES', ['The Ramsar Convention', 'The Paris Agreement', 'The Montreal Protocol'], '[1]'),
        ('The Basel Convention (1989) controls', 'transboundary movements of hazardous waste', ['whaling', 'ozone-depleting substances', 'carbon emissions'], '[1]'),
        ('Which NGO is known for direct-action campaigns such as protests against whaling and oil drilling?', 'Greenpeace', ['The World Bank', 'The IPCC', 'UNEP'], '[1]'),
        ('Under the Paris Agreement, emission targets are', 'set by each country (NDCs)', ['imposed by the UN on developed countries only', 'the same for every country', 'legally enforced with fines'], '[1]'),
        ('The International Whaling Commission introduced a moratorium on commercial whaling in', '1986', ['1946', '1972', '2015'], 'Agreed 1982, effective 1986. [1]'),
    ],
    'explain': [
        ('Explain why international agreements are needed to solve some environmental problems.', 'Problems such as climate change, ozone depletion and ocean pollution cross borders; no single country can solve them; agreements share responsibility, avoid free-riding and coordinate action.', '1 mark per point up to [3]'),
        ('Explain the roles of NGOs in environmental management.', 'Campaigning and raising awareness; lobbying governments; carrying out research and monitoring; running conservation projects; working with local communities; holding companies to account.', '1 mark per role up to [3]'),
        ('Explain how governments can encourage individuals to reduce their environmental impact.', 'Taxes (carbon or landfill taxes), subsidies (solar panels, electric cars), regulations (bans on single-use plastics), labelling, education campaigns and investment in public transport and recycling.', '1 mark per method up to [3]'),
        ('Explain why the Kyoto Protocol had limited success.', 'The USA never ratified it; developing countries including China and India had no binding targets; Canada withdrew; targets were small; global emissions continued to rise.', '1 mark per reason up to [3]'),
    ],
    'claims': [
        ('Individual actions make no difference to environmental problems.', False, 'Collective individual choices (diet, transport, energy, consumption) add up and influence businesses and governments.'),
        ('The Paris Agreement includes almost every country in the world.', True, 'Nearly 200 parties signed it, including developing countries, unlike the Kyoto Protocol’s binding targets for developed countries only.'),
        ('NGOs can pass environmental laws.', False, 'NGOs can campaign and influence, but only governments and legislatures pass laws.'),
    ],
    'essays': [
        ('governments are more important than individuals in solving environmental problems',
         ['Governments can pass laws, set taxes and subsidies, invest in infrastructure and negotiate international agreements (Montreal Protocol, Paris Agreement).'],
         ['Individuals change consumption, vote, protest (e.g. Fridays for Future) and support NGOs; without public support policies fail; NGOs and businesses also play key roles.'],
         'Governments have the greatest power, but they respond to pressure from individuals and NGOs; all levels must act together.',
         ['laws and taxes', 'NGOs', 'consumer choices']),
    ],
})


@m4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def m4_target(r, D):
    cty = r.choice(['the European Union', 'the United Kingdom', 'Country X', 'Japan', 'a middle-income country'])
    base_y = r.choice([1990, 2005])
    base = r.choice([400, 600, 800, 1200, 4500])
    target_pc = r.choice([40, 45, 50, 55, 68])
    now_pc = r.randint(15, 45)
    now = base * (1 - now_pc / 100)
    tgt = base * (1 - target_pc / 100)
    yr_now = 2022
    left = 2030 - yr_now
    need = (now - tgt) / left
    intro = (f'Under the Paris Agreement {cty} pledged to cut greenhouse gas emissions by {target_pc}% by 2030 compared with {base_y}. Emissions were {nf(base)} Mt CO₂e in {base_y} and '
             f'{nf(now)} Mt CO₂e in {yr_now}.')
    if D == 1:
        return MCQ(r, intro + ' What is the 2030 target in Mt CO₂e?', f'{nf(tgt)}', [f'{nf(base * target_pc / 100)}', f'{nf(now * (1 - target_pc / 100))}', f'{nf(tgt * 1.1)}', f'{nf(base - target_pc)}'],
                   f'{nf(base)} × (1 − {target_pc / 100:.2f}) = {nf(tgt)}. [1]')
    parts = [
        L(f'Calculate the percentage reduction already achieved by {yr_now}.', f'{f1(now_pc)}%', f'({nf(base)} − {nf(now)}) ÷ {nf(base)} × 100 = {f1(now_pc)}% [1]'),
        L('Calculate the target emissions for 2030.', f'{nf(tgt)} Mt CO₂e', f'{nf(base)} × {1 - target_pc / 100:.2f} = {nf(tgt)} [1]'),
        L(f'Calculate the average annual reduction needed from {yr_now} to 2030.', f'{s3(need)} Mt CO₂e per year', f'({nf(now)} − {nf(tgt)}) ÷ {left} [1] = {s3(need)} [1] [2]'),
        L('Suggest two policies the government could use to achieve this reduction.', 'Carbon tax or emissions trading; subsidies for renewables and electric vehicles; phase-out of coal; building insulation standards; investment in public transport.', '1 mark each [2]'),
        L('Explain why it is difficult to enforce targets under the Paris Agreement.', 'Targets (NDCs) are set by each country and are not legally binding; there are no penalties; countries can change their pledges or withdraw.', '[2]'),
    ]
    return comp(r, intro, parts, D)


CHAPTERS[7] = [m1, m2, m3, m4]


# ============================================================== CHAPTER 8: Research skills

# (context, independent variable, dependent variable, controlled variables, hypothesis, null hypothesis)
STUDIES = [
    ('Students in {c} want to find out whether distance from a road affects the abundance of lichens on tree trunks.', 'distance from the road', 'lichen abundance (percentage cover on the trunk)',
     'tree species, height on trunk, aspect of the trunk (e.g. north side), size of quadrat', 'Lichen cover increases with distance from the road.', 'There is no relationship between distance from the road and lichen cover.'),
    ('A group is investigating whether trampling on a footpath affects plant species diversity in a park near {c}.', 'intensity of trampling (distance from the centre of the path)', 'number of plant species per quadrat',
     'quadrat size, time of year, soil type, slope', 'Species diversity increases with distance from the centre of the path.', 'There is no relationship between distance from the path and species diversity.'),
    ('{p} is studying whether the concentration of nitrate in a river increases downstream of farmland.', 'distance downstream / land use upstream', 'nitrate concentration (mg/l)',
     'time of day, weather conditions, depth of sampling, the same test kit', 'Nitrate concentration is higher downstream of farmland than upstream.', 'There is no difference in nitrate concentration upstream and downstream of the farmland.'),
    ('Students want to know whether soil moisture affects the number of earthworms in a school field in {c}.', 'soil moisture (%)', 'number of earthworms per 0.25 m² quadrat',
     'time of day, sampling depth, method of extraction, soil type', 'The number of earthworms increases as soil moisture increases.', 'There is no relationship between soil moisture and the number of earthworms.'),
    ('A researcher is investigating whether noise from traffic affects the number of bird species heard in urban parks in {c}.', 'traffic noise level (dB)', 'number of bird species recorded in 10 minutes',
     'time of day, season, weather, duration of each count, the same observer', 'Fewer bird species are recorded where traffic noise is higher.', 'There is no relationship between traffic noise and the number of bird species.'),
    ('{p} is investigating whether light intensity affects the height of plants growing under a woodland canopy.', 'light intensity (lux)', 'mean plant height (cm)',
     'plant species, soil type, time of day light is measured, slope', 'Plant height increases with light intensity.', 'There is no relationship between light intensity and plant height.'),
    ('A class investigates whether the number of people using a beach affects the amount of litter found on beaches near {s}.', 'number of visitors', 'mass or number of litter items per 10 m of beach',
     'time since last clean-up, tide state, section width, weather', 'There is more litter on beaches with more visitors.', 'There is no relationship between visitor numbers and litter.'),
    ('Students investigate whether attitudes to recycling differ between age groups in {c}.', 'age group', 'stated frequency of recycling (from a questionnaire)',
     'the same questions, same location and time of day, similar sample size in each group', 'Younger people recycle more frequently than older people.', 'There is no difference in recycling frequency between age groups.'),
]


def _who(ctx, p):
    """Name used later in the stem: the person in the context, or the students as a group."""
    if p in ctx:
        return p
    for a, b in (('A researcher', 'The researcher'), ('A group', 'The group'), ('A class', 'The class'), ('A team', 'The team'), ('A scientist', 'The scientist')):
        if ctx.startswith(a):
            return b
    return 'The students'


def _study(r, p=None):
    s = list(r.choice(STUDIES))
    s[0] = s[0].format(c=city(r), p=p or person(r), s=r.choice(['Cape Town', 'Lisbon', 'Muscat', 'Accra', 'Colombo', 'Auckland', 'Mumbai', 'Lima', 'Dubai', 'Manila']))
    return s


r1 = T('Research design: aims, hypotheses and identifying variables', 'research design', 'hypotheses', 'identifying variables')
build(r1, {
    'terms': [
        ('hypothesis', 'a testable statement that predicts the relationship between two variables'),
        ('null hypothesis', 'a statement that there is no relationship or difference between the variables being studied'),
        ('independent variable', 'the variable that is changed or selected by the investigator'),
        ('dependent variable', 'the variable that is measured, which may change in response to the independent variable'),
        ('controlled variable', 'a variable kept constant so that it does not affect the results'),
        ('aim', 'a general statement of what an investigation sets out to find out'),
        ('pilot study', 'a small-scale trial of an investigation used to test and improve methods before the main study'),
        ('primary data', 'data collected first-hand by the investigator, for example by fieldwork or questionnaires'),
    ],
    'mcq': [
        ('Which is a testable hypothesis?', 'Soil pH decreases with distance from the limestone outcrop', ['Pollution is bad for rivers', 'What affects plant growth?', 'Forests are important'], 'It states a measurable relationship. [1]'),
        ('Data from a government census is an example of', 'secondary data', ['primary data', 'a controlled variable', 'a null hypothesis'], '[1]'),
        ('In an investigation of the effect of altitude on air temperature, air temperature is the', 'dependent variable', ['independent variable', 'controlled variable', 'null hypothesis'], '[1]'),
        ('Why is a null hypothesis used?', 'It can be tested statistically and accepted or rejected', ['It proves the hypothesis', 'It removes the need for data', 'It is always correct'], '[1]'),
        ('Which is a qualitative method?', 'An open-ended interview', ['Measuring river velocity', 'Counting cars', 'Measuring soil pH'], '[1]'),
    ],
    'explain': [
        ('Explain why controlled variables are important in an investigation.', 'If other variables change, they could affect the dependent variable, so any pattern could not be attributed to the independent variable; controlling them makes the test fair and results valid.', 'other factors affect results [1]; makes conclusions valid [1] [2]'),
        ('Explain the purpose of a pilot study.', 'To test equipment, methods and questionnaires on a small scale, identify problems, estimate time needed and decide sample size, so the main study is more reliable.', '1 mark per point up to [3]'),
        ('Explain why risk assessment is part of planning fieldwork.', 'Fieldwork may involve hazards such as rivers, traffic, weather or chemicals; identifying risks and precautions keeps investigators safe.', '[2]'),
        ('Explain the difference between primary and secondary data and give one advantage of each.', 'Primary data is collected by the investigator (e.g. quadrat counts) and is specific to the aim; secondary data is collected by others (e.g. census, Met Office records) and may cover larger areas or longer periods.', 'definitions [1]; advantages [1] [2]'),
    ],
    'claims': [
        ('A hypothesis must always be proved correct for an investigation to be useful.', False, 'Rejecting a hypothesis is also a valid and useful result.'),
        ('An investigation should change only one independent variable at a time.', True, 'Otherwise it is impossible to tell which variable caused any change.'),
        ('Ethical considerations are only needed in laboratory experiments.', False, 'Fieldwork involving people (questionnaires, interviews) needs consent, anonymity and respect; work in habitats should minimise disturbance.'),
    ],
})


@r1.add('C2', (1, 2, 3, 4), 'explain')
def r1_vars(r, D):
    ctx, iv, dv, cv, h, h0 = _study(r)
    if D == 1:
        other = [s[1] for s in STUDIES if s[1] != iv]
        return MCQ(r, ctx + ' What is the independent variable?', cap(iv), [cap(dv)] + [cap(x) for x in r.sample(other, 3)], f'The independent variable is the one selected or changed: {iv}. [1]')
    if D == 2:
        return {'stem': ctx + ' Identify the independent and dependent variables.', 'answer': f'Independent: {iv}. Dependent: {dv}.', 'key': '1 mark each [2]', 'marks': 2}
    return {'stem': ctx + ' Identify the independent variable, the dependent variable and two variables that should be controlled. Explain why one of them should be controlled.',
            'answer': f'Independent: {iv}. Dependent: {dv}. Controlled: {cv}. Each could also affect the dependent variable, so it must be kept the same to make the test fair.',
            'key': 'IV [1]; DV [1]; two controlled variables [1]; explanation [1] [4]', 'marks': 4}


@r1.add('C3', (1, 2, 3, 4, 5), 'case')
def r1_hyp(r, D):
    ctx, iv, dv, cv, h, h0 = _study(r)
    if D == 1:
        other = [s[4] for s in STUDIES if s[4] != h]
        return MCQ(r, ctx + ' Which is the most suitable hypothesis for this investigation?', h, r.sample(other, 3), 'It must match the variables in the investigation and be testable. [1]')
    parts = [
        L('Write a hypothesis for this investigation.', h, 'testable, names both variables [1]'),
        L('Write a null hypothesis.', h0, '[1]'),
        L('Identify the independent and dependent variables.', f'Independent: {iv}. Dependent: {dv}.', '1 mark each [2]'),
        L('State two variables that should be controlled.', cap(cv) + '.', '1 mark each [2]'),
        L('Explain why a pilot study would be useful.', 'To test the method and equipment, check timing and sample size, and identify problems before the main data collection.', '[2]'),
        L('Suggest one ethical or safety consideration for this investigation.', 'Obtain permission from landowners or respondents; keep respondents anonymous; avoid damaging habitats; take care near roads or water; work in groups.', '[1]'),
    ]
    return comp(r, ctx, parts, D, 'case')


@r1.add('C4', (2, 3, 4, 5), 'case')
def r1_plan(r, D):
    p = person(r)
    ctx, iv, dv, cv, h, h0 = _study(r, p)
    p = _who(ctx, p)
    stem = f'{ctx} {p} {"have" if p == "The students" else "has"} one day for data collection. The hypothesis is: “{h}”'
    parts = [
        L('Plan an investigation to test this hypothesis. Include the method of sampling, the measurements to be made and how variables will be controlled.', f'Select sites across the range of the independent variable ({iv}); use systematic or stratified sampling with enough samples (at least 10); measure {dv} with the same equipment and method each time; control {cv}; repeat measurements and record in a table.', 'sampling [1]; measurement of DV [1]; range of IV [1]; control of variables [1]; repeats / sample size [1] [5]'),
        L('Explain how the data could be analysed to test the hypothesis.', 'Plot a scatter graph (or bar chart for groups) and use Spearman’s rank correlation (or compare means) to test whether the relationship is significant at the 0.05 level, accepting or rejecting the null hypothesis.', 'graph [1]; statistical test [1]; significance / null hypothesis [1] [3]'),
        L('Explain two limitations of a one-day study.', 'Conditions on one day may not be typical (weather, season); limited sample size; no repeats on other days; time constraints may lead to rushed measurements.', '1 mark per limitation with explanation up to [2]'),
        L('Explain how the reliability of the results could be improved.', 'Increase the number of samples; repeat on different days or seasons; use calibrated equipment; take means of repeats.', '[2]'),
    ]
    return comp(r, stem, parts, D, 'case')


r2 = T('Sampling techniques: random, systematic, stratified, quadrats and transects', 'sampling techniques', 'random, systematic, stratified', 'quadrats', 'transects')
build(r2, {
    'terms': [
        ('random sampling', 'a method in which every individual or point has an equal chance of being selected, for example using random number tables to choose coordinates'),
        ('systematic sampling', 'taking samples at regular intervals, for example every 5 m along a transect or every 10th person'),
        ('stratified sampling', 'dividing the population into groups (strata) and sampling each in proportion to its size'),
        ('quadrat', 'a square frame of known area used to sample plants or slow-moving animals'),
        ('line transect', 'a line across an area along which organisms touching the line are recorded at intervals'),
        ('belt transect', 'a strip along which quadrats are placed at regular intervals to record changes across a habitat'),
        ('mark-release-recapture', 'a method of estimating the population of mobile animals by marking a sample, releasing it and recapturing a second sample (Lincoln index)'),
        ('opportunistic sampling', 'choosing samples that are convenient or available, such as people willing to answer questions'),
    ],
    'mcq': [
        ('Which sampling method is best for studying how vegetation changes from a river bank up a valley side?', 'A belt transect with systematic quadrats', ['Random quadrats over the whole area', 'Opportunistic sampling', 'Mark-release-recapture'], 'There is an environmental gradient. [1]'),
        ('Which method is used to estimate the population of beetles in a woodland?', 'Pitfall traps with mark-release-recapture', ['Quadrats', 'Kick sampling', 'Line transect'], '[1]'),
        ('Why is random sampling used?', 'To avoid bias in choosing sample sites', ['To make sampling faster', 'To make sure all rare species are found', 'To sample along a gradient'], '[1]'),
        ('Kick sampling is used to collect', 'freshwater invertebrates from a stream bed', ['soil samples', 'flying insects', 'air pollutants'], '[1]'),
        ('Which assumption is made in mark-release-recapture?', 'Marked animals mix randomly back into the population', ['Marks wash off quickly', 'Many animals are born between samples', 'Marked animals are easier to catch'], '[1]'),
        ('A 0.5 m × 0.5 m quadrat has an area of', '0.25 m²', ['1 m²', '0.5 m²', '2.5 m²'], '[1]'),
    ],
    'explain': [
        ('Describe how random sampling with quadrats would be carried out in a field.', 'Lay two tape measures at right angles along two edges to make a grid; use random number tables or a calculator to generate coordinates; place the quadrat at each coordinate; record species or percentage cover; repeat for at least 10 quadrats.', '1 mark per step up to [4]'),
        ('Explain the advantages and disadvantages of systematic sampling.', 'Advantages: quick and easy, gives even coverage, good for showing change along a gradient. Disadvantages: may miss or over-represent features that occur at regular intervals; not all points have an equal chance of selection.', 'advantage [1]; disadvantage [1] [2]'),
        ('Explain when stratified sampling should be used.', 'When the area or population contains distinct sub-groups (e.g. different habitats, land uses or age groups) of different sizes, so that each is represented in proportion.', '[2]'),
        ('Explain the assumptions of the Lincoln index method.', 'No births, deaths, immigration or emigration between samples; marks are not lost and do not affect survival; marked animals mix randomly; each animal has an equal chance of being caught.', '1 mark per assumption up to [3]'),
        ('Explain how to estimate percentage cover using a quadrat divided into 100 small squares.', 'Count the number of small squares that are more than half covered by the species; each square is 1%, so the count gives the percentage cover.', '[2]'),
    ],
    'claims': [
        ('Larger samples usually give more reliable results.', True, 'Larger samples reduce the effect of unusual individual results and are more representative of the population.'),
        ('Systematic sampling is always free from bias.', False, 'It can be biased if features occur at the same regular interval as the sampling points.'),
        ('Quadrats are suitable for sampling fast-moving animals such as birds.', False, 'Quadrats suit plants and slow-moving animals; birds need point counts or transects.'),
    ],
})


@r2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r2_lincoln(r, D):
    sp = r.choice(['woodlice under logs', 'ground beetles in pitfall traps', 'freshwater shrimps in a pond', 'snails in a garden', 'grasshoppers in a meadow', 'crabs on a rocky shore'])
    n1 = r.randint(20, 80)
    n2 = r.randint(20, 80)
    m2 = r.randint(3, min(n1, n2) // 2)
    N = n1 * n2 / m2
    intro = f'Students estimated a population of {sp} near {city(r)}. In the first sample they caught and marked {n1}. A day later they caught {n2}, of which {m2} were marked.'
    if D == 1:
        return MCQ(r, intro + ' Using the Lincoln index N = (n₁ × n₂) ÷ m₂, what is the estimated population?', nf(N), [nf(n1 + n2), nf(n1 * m2 / n2), nf(N / 2), nf(n1 * n2)], f'({n1} × {n2}) ÷ {m2} = {nf(N)}. [1]')
    parts = [
        L('Use the Lincoln index N = (n₁ × n₂) ÷ m₂ to estimate the population.', nf(N), f'({n1} × {n2}) ÷ {m2} [1] = {nf(N)} [1] [2]'),
        L('State two assumptions made when using this method.', 'No migration, births or deaths between samples; marks do not affect survival or catchability; marked animals mix randomly with the population.', '1 mark each [2]'),
        L('Suggest why the marks should be small and non-toxic.', 'Large or bright marks could make animals easier for predators to see; toxic marks could kill them; both would reduce recaptures and overestimate the population.', '[2]'),
        L(f'Calculate the new estimate if {m2 + 2} marked animals had been recaptured instead, and explain what this shows.', f'{nf(n1 * n2 / (m2 + 2))}; the estimate is very sensitive to the number recaptured, so small errors matter.', f'({n1} × {n2}) ÷ {m2 + 2} = {nf(n1 * n2 / (m2 + 2))} [1]; comment [1] [2]'),
        L('Suggest how the reliability of the estimate could be improved.', 'Repeat the capture several times and calculate a mean; increase the sample sizes; leave enough time for mixing.', '[1]'),
    ]
    return comp(r, intro, parts, D)


@r2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r2_quadrat(r, D):
    sp = r.choice(['daisies', 'dandelions', 'plantain', 'clover', 'buttercups', 'thistles'])
    side = r.choice([0.5, 1.0])
    n = r.choice([8, 10, 12])
    counts = [r.randint(0, 14) for _ in range(n)]
    if sum(counts) == 0:
        return None
    area_q = side * side
    mean = sum(counts) / n
    dens = mean / area_q
    field = r.choice([400, 1200, 2500, 5000])
    present = sum(1 for c in counts if c > 0)
    intro = f'{person(r)} placed {n} {fmt(side, 1)} m × {fmt(side, 1)} m quadrats at random in a {nf(field)} m² field and counted {sp} in each: ' + ', '.join(map(str, counts)) + '.'
    if D == 1:
        return MCQ(r, intro + ' What is the mean number per quadrat?', f'{f1(mean)}', [f'{f1(sum(counts) / (n - 1))}', f'{f1(dens * 2) if side == 0.5 else f1(mean * 2)}', f'{f1(sorted(counts)[n // 2] + 0.5)}', f'{f1(mean / 2)}'],
                   f'{sum(counts)} ÷ {n} = {f1(mean)}. [1]')
    parts = [
        L('Calculate the mean number per quadrat.', f1(mean), f'{sum(counts)} ÷ {n} = {f1(mean)} [1]'),
        L('Calculate the population density per m².', f'{s3(dens)} per m²', f'{f1(mean)} ÷ {fmt(area_q, 2)} m² = {s3(dens)} [1]'),
        L('Estimate the total population in the field.', nf(dens * field), f'{s3(dens)} × {nf(field)} = {nf(dens * field)} [1]'),
        L('Calculate the percentage frequency of the species.', f'{f1(present / n * 100)}%', f'present in {present} of {n} quadrats [1]; {f1(present / n * 100)}% [1] [2]'),
        L('Explain why random sampling was used.', 'To avoid bias in choosing where to place quadrats, so the sample is representative of the field.', '[1]'),
        L('Suggest two ways to improve the reliability of the estimate.', 'Use more quadrats; repeat on another day; use a larger quadrat; use the same rule for plants on the edge of the quadrat.', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D)


@r2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r2_strat(r, D):
    kind = r.choice(['habitat', 'people'])
    if kind == 'habitat':
        zones = r.sample(['woodland', 'grassland', 'scrub', 'wetland', 'farmland', 'heath'], 3)
        pcts = r.choice([(50, 30, 20), (60, 25, 15), (45, 35, 20), (40, 40, 20), (70, 20, 10)])
        tot = r.choice([20, 30, 40, 50])
        alloc = [tot * p / 100 for p in pcts]
        intro = f'A nature reserve near {city(r)} is made up of {zones[0]} ({pcts[0]}%), {zones[1]} ({pcts[1]}%) and {zones[2]} ({pcts[2]}%). An ecologist plans to place {tot} quadrats using stratified sampling.'
        unit = 'quadrats'
    else:
        zones = ['aged 16-29', 'aged 30-59', 'aged 60 and over']
        popn = [r.randint(2, 9) * 1000 for _ in range(3)]
        tot = r.choice([60, 80, 100, 120])
        s = sum(popn)
        pcts = [p / s * 100 for p in popn]
        alloc = [tot * p / s for p in popn]
        intro = f'A village near {city(r)} has {nf(popn[0])} people {zones[0]}, {nf(popn[1])} {zones[1]} and {nf(popn[2])} {zones[2]}. Students will ask {tot} people about their views on a proposed wind farm, using stratified sampling.'
        unit = 'people'
    if any(abs(a - round(a)) > 1e-9 for a in alloc) and kind == 'habitat':
        return None
    al = [round(a) for a in alloc]
    if D == 1:
        return MCQ(r, intro + f' How many {unit} should be sampled in the {zones[0]} group?', str(al[0]), [str(al[1]), str(tot // 3), str(al[2]), str(al[0] + 5)], f'{tot} × {fmt(pcts[0], 1)}% = {fmt(alloc[0], 1)}. [1]')
    parts = [
        L(f'Calculate how many {unit} should be sampled in each group.', '; '.join(f'{z}: {a}' for z, a in zip(zones, al)), f'proportion × {tot} for each [1]; all correct [1] [2]'),
        L('Explain why stratified sampling is more suitable than simple random sampling here.', 'The groups are different sizes and may differ in their characteristics; stratified sampling ensures each is represented in proportion, so the sample is more representative.', '[2]'),
        L('Describe how the samples would be chosen within each group.', ('Use random coordinates within each zone (random numbers on a grid of the reserve).' if kind == 'habitat' else 'Within each age group, choose people randomly (e.g. every nth house or random numbers from the electoral roll) and ask their age before the survey.'), '[2]'),
        L('Suggest one possible source of bias in carrying out the survey.', ('Placing quadrats where it is easy to walk; boundaries between zones are not clear.' if kind == 'habitat' else 'Only people at home during the day are surveyed; some people refuse to answer; wording of questions.'), '[1]'),
    ]
    return comp(r, intro, parts, D)


r3 = T('Data collection: questionnaires, interviews and measuring abiotic factors', 'data collection', 'questionnaires', 'interviews', 'abiotic factors')
build(r3, {
    'terms': [
        ('abiotic factor', 'a non-living physical or chemical feature of the environment, such as temperature, light, pH or soil moisture'),
        ('biotic factor', 'a living feature of the environment that affects organisms, such as predation, competition or disease'),
        ('questionnaire', 'a set of written questions used to collect information from a sample of people'),
        ('closed question', 'a question with a fixed set of possible answers, such as yes/no or a rating scale'),
        ('open question', 'a question that allows the respondent to answer freely in their own words'),
        ('Likert scale', 'a rating scale, for example from strongly agree to strongly disagree, used to measure attitudes'),
        ('semi-structured interview', 'an interview with prepared questions that allows the interviewer to ask follow-up questions'),
        ('anemometer', 'an instrument used to measure wind speed'),
    ],
    'mcq': [
        ('Which instrument measures light intensity?', 'A light meter (lux meter)', ['An anemometer', 'A clinometer', 'A hygrometer'], '[1]'),
        ('Which instrument measures relative humidity?', 'A hygrometer (wet and dry bulb thermometer)', ['A barometer', 'An anemometer', 'A pH meter'], '[1]'),
        ('Which type of question produces data that is easiest to analyse statistically?', 'Closed questions', ['Open questions', 'Leading questions', 'Unstructured interviews'], '[1]'),
        ('Which is a leading question?', '“Don’t you agree that the new dam will be harmful?”', ['“How often do you use public transport?”', '“What is your age group?”', '“Do you recycle plastic?”'], 'It suggests the expected answer. [1]'),
        ('Soil moisture content can be found by', 'weighing a sample before and after drying in an oven at about 105 °C', ['measuring its pH', 'burning it at 500 °C', 'counting earthworms'], '[1]'),
        ('Turbidity of river water can be measured with', 'a Secchi disc or turbidity tube', ['a flow meter', 'an anemometer', 'a quadrat'], '[1]'),
    ],
    'explain': [
        ('Explain the advantages and disadvantages of questionnaires compared with interviews.', 'Questionnaires: quick, many respondents, easy to analyse, anonymous; but shallow answers, low response rates and misunderstood questions. Interviews: detailed, follow-up questions, explanation of views; but time-consuming, small samples, interviewer bias, harder to compare.', '1 mark per point, balance required, up to [4]'),
        ('Explain how to design a good questionnaire.', 'Clear, simple, unambiguous questions; a mix of closed and some open questions; avoid leading questions; keep it short; logical order; pilot it first; include ethical statements on anonymity and consent.', '1 mark per point up to [3]'),
        ('Describe how to measure the velocity of a stream.', 'Measure a set distance (e.g. 10 m); drop a float upstream; time how long it takes to travel the distance; repeat three times and calculate mean time; velocity = distance ÷ time (or use a flow meter).', '1 mark per step up to [3]'),
        ('Explain why abiotic measurements should be taken at the same time as biotic sampling.', 'Abiotic conditions such as light, temperature and moisture change through the day and with weather; measuring together allows valid comparison and explanation of distributions.', '[2]'),
    ],
    'claims': [
        ('Open questions are better than closed questions in every questionnaire.', False, 'Open questions give detail but are harder to analyse; closed questions are quick and easy to compare.'),
        ('Instruments such as pH meters should be calibrated before use.', True, 'Calibration with buffer solutions of known pH ensures readings are accurate.'),
        ('Respondents should always be told how their answers will be used.', True, 'Informed consent and anonymity are ethical requirements of social research.'),
    ],
})


ABIOTIC = [('soil pH', 'a soil pH meter or a soil test kit with barium sulfate and indicator', 'calibrate with buffer solutions; mix soil with distilled water'),
           ('light intensity', 'a light meter (lux)', 'hold at the same height and angle; avoid shading the sensor'),
           ('air temperature', 'a thermometer or digital temperature probe', 'measure in the shade at a set height, e.g. 1 m'),
           ('wind speed', 'an anemometer', 'hold at a set height, facing into the wind, for a set time'),
           ('soil moisture', 'weighing a soil sample before and after drying in an oven at 105 °C, or a moisture probe', 'dry to constant mass'),
           ('dissolved oxygen', 'a dissolved oxygen meter or test kit', 'sample at the same depth and avoid trapping air bubbles'),
           ('stream velocity', 'a flow meter or float timed over a measured distance', 'repeat three times and take a mean'),
           ('relative humidity', 'a whirling hygrometer (wet and dry bulb)', 'use a humidity table for the wet and dry bulb readings'),
           ('slope angle', 'a clinometer with ranging poles', 'take readings between poles at the same height')]


@r3.add('C2', (1, 2, 3, 4), 'explain')
def r3_equip(r, D):
    f, eq, tip = r.choice(ABIOTIC)
    if D == 1:
        return MCQ(r, f'Which equipment is used to measure {f} in the field?', cap(eq), [cap(x[1]) for x in ABIOTIC if x[0] != f], f'{cap(f)}: {eq}. [1]')
    return {'stem': f'Describe how {f} could be measured accurately during fieldwork in {city(r)}.', 'answer': f'Use {eq}; {tip}; take repeat readings at each site and calculate a mean.',
            'key': 'equipment [1]; technique for accuracy [1]; repeats / mean [1] [3]', 'marks': 3}


@r3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r3_moist(r, D):
    sites = ['A', 'B', 'C']
    wet = [round(r.uniform(40, 80), 1) for _ in sites]
    dry = [round(w * (1 - r.uniform(0.08, 0.45)), 1) for w in wet]
    pcs = [(w - d) / w * 100 for w, d in zip(wet, dry)]
    intro = 'Soil samples were taken at three sites on a slope. Wet mass (g): ' + ', '.join(f'{s} {fmt(w, 1)}' for s, w in zip(sites, wet)) + '. Mass after oven-drying at 105 °C (g): ' + ', '.join(f'{s} {fmt(d, 1)}' for s, d in zip(sites, dry)) + '.'
    if D == 1:
        return MCQ(r, intro + ' What is the percentage moisture content of site A (calculated from the wet mass)?', f'{f1(pcs[0])}%', [f'{f1((wet[0] - dry[0]) / dry[0] * 100)}%', f'{f1(dry[0] / wet[0] * 100)}%', f'{f1(wet[0] - dry[0])}%', f'{f1(pcs[1])}%' if f1(pcs[1]) != f1(pcs[0]) else f'{f1(pcs[0] + 3)}%'],
                   f'({fmt(wet[0], 1)} − {fmt(dry[0], 1)}) ÷ {fmt(wet[0], 1)} × 100 = {f1(pcs[0])}%. [1]')
    hi = sites[pcs.index(max(pcs))]
    parts = [
        L('Calculate the percentage moisture content of each sample (as a percentage of wet mass).', '; '.join(f'{s} {f1(p)}%' for s, p in zip(sites, pcs)), 'method [1]; all correct [1] [2]'),
        L('Explain why the samples were dried to constant mass.', 'To make sure all the water had evaporated, so the mass lost is the total water content.', '[1]'),
        L('Explain why the oven was set at 105 °C and not a much higher temperature.', 'Hot enough to evaporate the water but not to burn off organic matter, which would add to the mass lost.', '[2]'),
        L(f'Suggest why site {hi} has the highest moisture content.', 'It may be lower on the slope where water collects, have more clay or organic matter, or be shaded so less evaporation.', '[1]'),
        L('Suggest one source of error in the method.', 'Water lost from samples before weighing; samples not dried completely; different sample sizes or depths; balance precision.', '[1]'),
    ]
    return comp(r, intro, parts, D)


@r3.add('C3', (2, 3, 4, 5), 'case')
def r3_questionnaire(r, D):
    topic_ = r.choice(['a proposed landfill site', 'a new wind farm', 'a congestion charge', 'the closure of a coal mine', 'a ban on plastic bags', 'a new national park'])
    n = r.choice([40, 50, 60, 80, 100])
    yes = r.randint(int(n * 0.2), int(n * 0.8))
    intro = f'Students in {city(r)} designed a questionnaire about attitudes to {topic_}. They asked {n} people in the town centre on a weekday morning; {yes} supported the proposal.'
    parts = [
        L('Calculate the percentage of respondents who supported the proposal.', f'{f1(yes / n * 100)}%', f'{yes} ÷ {n} × 100 = {f1(yes / n * 100)}% [1]'),
        L('Write one closed question and one open question for the questionnaire.', f'Closed: “Do you support {topic_}? Yes / No / Not sure.” Open: “What effects do you think {topic_} would have on the town?”', '1 mark each [2]'),
        L('Explain why the sample may not be representative of the town’s population.', 'Only people in the town centre on a weekday morning were asked, so workers, students and people living further away were under-represented (opportunistic, biased sample).', '1 mark per point up to [2]'),
        L('Suggest how the sampling could be improved.', 'Stratified sampling by age or area; survey at different times and days and in different places; a larger sample.', '1 mark per point up to [2]'),
        L('Explain two ethical considerations in carrying out the survey.', 'Obtain informed consent; keep answers anonymous and confidential; allow people to refuse or withdraw; avoid asking young children without consent.', '1 mark each [2]'),
    ]
    return comp(r, intro, parts, D, 'case')


def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: -xs[i])
    rk = [0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            rk[order[k]] = avg
        i = j + 1
    return rk


CRIT = {6: 0.886, 7: 0.786, 8: 0.738, 9: 0.700, 10: 0.648, 11: 0.618, 12: 0.587}

r4 = T("Data presentation and analysis: graphs, Simpson's diversity index and Spearman's rank correlation", 'data presentation and analysis', "simpson's diversity index", "spearman's rank correlation")
build(r4, {
    'terms': [
        ("Simpson's index of diversity", 'a measure of biodiversity that takes into account both species richness and the evenness of their abundance'),
        ("Spearman's rank correlation coefficient", 'a statistic between −1 and +1 that measures the strength and direction of the relationship between two ranked variables'),
        ('scatter graph', 'a graph that plots two variables against each other to show whether they are related'),
        ('kite diagram', 'a graph used to show changes in the abundance of species along a transect'),
        ('critical value', 'the value a test statistic must reach for the result to be significant at a given level'),
        ('significance level', 'the probability that the result occurred by chance, usually set at 0.05 (5%)'),
        ('positive correlation', 'a relationship in which one variable increases as the other increases'),
        ('interquartile range', 'the range of the middle 50% of a data set, the upper quartile minus the lower quartile'),
    ],
    'mcq': [
        ("A Spearman's rank correlation coefficient of −0.92 indicates", 'a strong negative correlation', ['a weak positive correlation', 'no correlation', 'that one variable causes the other'], '[1]'),
        ('Which graph is most suitable for showing the percentages of land use in a region?', 'A pie chart or divided bar chart', ['A scatter graph', 'A kite diagram', 'A line graph'], '[1]'),
        ('Which graph is used to show the distribution of species along a transect?', 'A kite diagram', ['A pie chart', 'A climate graph', 'A population pyramid'], '[1]'),
        ('A result significant at the 0.05 level means', 'there is a less than 5% probability that the result occurred by chance', ['the hypothesis is proved', 'there is a 95% chance of error', '5 samples were taken'], '[1]'),
        ("On the scale used for Simpson's index of diversity (D = 1 − Σn(n−1)/N(N−1)), a value close to 1 indicates", 'high diversity', ['low diversity', 'only one species', 'an invalid calculation'], '[1]'),
    ],
    'explain': [
        ('Explain why correlation does not prove causation.', 'Two variables may be related by chance, or both may be affected by a third variable; an explanation must be supported by knowledge of processes.', '[2]'),
        ("Explain why Simpson's index is more useful than species richness alone.", 'It accounts for evenness as well as the number of species; a habitat dominated by one species has low diversity even if many species are present.', '[2]'),
        ("Describe how to test a relationship using Spearman's rank.", 'State null hypothesis; rank each variable; find the difference d for each pair and square it; calculate rs = 1 − 6Σd²/(n(n² − 1)); compare with the critical value for n at 0.05; accept or reject the null hypothesis.', '1 mark per step up to [4]'),
        ('Explain the choice between a line graph and a bar chart.', 'Line graphs show continuous data changing over time or distance; bar charts compare discrete categories.', '[2]'),
    ],
    'claims': [
        ("A Spearman's rank value of +1 shows a perfect positive correlation between the ranks.", True, 'Every pair of ranks is the same.'),
        ('A correlation coefficient of 0.4 is always significant.', False, 'Significance depends on the number of pairs; with small samples a much higher value is needed.'),
        ('A higher Simpson’s index means the habitat is more stable and diverse.', True, 'Higher diversity usually means more complex food webs and greater resilience to change.'),
    ],
})


@r4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r4_simpson(r, D):
    hab = r.choice(['a hedgerow', 'a rocky shore', 'a woodland floor', 'a meadow', 'a mangrove fringe', 'a stream riffle', 'a sand dune slack'])
    k = 4 if D <= 2 else r.choice([5, 6])
    ns = [r.randint(2, 30) for _ in range(k)]
    names = r.sample(['species A', 'species B', 'species C', 'species D', 'species E', 'species F'], k)
    names.sort()
    N = sum(ns)
    s = sum(n * (n - 1) for n in ns)
    Dv = 1 - s / (N * (N - 1))
    intro = f'Students counted organisms in {hab}: ' + ', '.join(f'{a} {n}' for a, n in zip(names, ns)) + ". Simpson's index of diversity D = 1 − [Σn(n − 1) ÷ N(N − 1)]."
    if D == 1:
        return MCQ(r, intro + ' What is the value of N(N − 1)?', nf(N * (N - 1)), [nf(N * N), nf(s), nf(N * (N + 1)), nf((N - 1) ** 2)], f'N = {N}; {N} × {N - 1} = {nf(N * (N - 1))}. [1]')
    other = [r.randint(2, 30) for _ in range(k)]
    No = sum(other)
    Do = 1 - sum(n * (n - 1) for n in other) / (No * (No - 1))
    parts = [
        L("Calculate Simpson's index of diversity for the habitat. Show your working.", s3(Dv),
          f'N = {N}; Σn(n − 1) = {nf(s)} [1]; N(N − 1) = {nf(N * (N - 1))} [1]; D = 1 − {nf(s)}/{nf(N * (N - 1))} = {s3(Dv)} [1] [3]'),
        L(f'A second site had D = {s3(Do)}. Calculate D for the first habitat and compare the diversity of the two sites.', f'D = {s3(Dv)} for the first habitat. ' + ('The first site is more diverse.' if Dv > Do else 'The second site is more diverse.' if Do > Dv else 'They have the same diversity.') + ' A higher D means more species and/or a more even spread of individuals.', f'D = {s3(Dv)} [1]; correct comparison [1]; reason (richness and evenness) [1] [3]'),
        L('Explain why the index takes account of evenness.', 'The n(n − 1) terms give much more weight to abundant species, so a habitat dominated by one species has a low value even if many species are present.', '[2]'),
        L('Suggest one human activity that could reduce the diversity of this habitat.', 'Trampling, pollution, removal of vegetation, introduction of invasive species, use of herbicides or pesticides.', '[1]'),
    ]
    return comp(r, intro, parts, D)


SPEAR_CTX = [('distance from the road (m)', 'lichen cover (%)', 1), ('distance downstream (km)', 'channel width (m)', 1), ('altitude (m)', 'air temperature (°C)', -1),
             ('distance from the city centre (km)', 'PM2.5 concentration (μg/m³)', -1), ('soil moisture (%)', 'number of earthworms', 1),
             ('distance from the sea (m)', 'soil organic matter (%)', 1), ('trampling (people per hour)', 'number of plant species', -1), ('light intensity (lux)', 'plant height (cm)', 1),
             ('GDP per capita (US$ thousand)', 'ecological footprint (gha per person)', 1), ('distance from a sewage outfall (m)', 'dissolved oxygen (mg/l)', 1)]


@r4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r4_spearman(r, D):
    xn, yn, sign = r.choice(SPEAR_CTX)
    n = r.choice([8, 10]) if D >= 3 else 8
    xs = sorted(r.sample(range(5, 200), n))
    noise = r.choice([0.15, 0.3, 0.5, 0.8])
    base = [sign * (x / 200) + r.gauss(0, noise) for x in xs]
    lo, hi = min(base), max(base)
    ys = [round(10 + 90 * (b - lo) / ((hi - lo) or 1), 1) for b in base]
    if yn.startswith('number'):
        ys = [int(round(y / 2)) for y in ys]
    if len(set(ys)) < n:
        return None
    rx, ry = _ranks(xs), _ranks(ys)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rs = 1 - 6 * d2 / (n * (n * n - 1))
    crit = CRIT[n]
    sig = abs(rs) >= crit
    intro = (f'Students recorded {xn} and {yn} at {n} sites: ' + '; '.join(f'site {i + 1}: {x}, {fmt(y, 1)}' for i, (x, y) in enumerate(zip(xs, ys)))
             + f". Spearman's rank correlation coefficient rs = 1 − 6Σd² ÷ (n(n² − 1)). The critical value for n = {n} at the 0.05 significance level is {crit}.")
    if D == 1:
        return MCQ(r, intro + f' The value of Σd² is {fmt(d2, 1)}. What is rs?', f2(rs), [f2(-rs) if f2(-rs) != f2(rs) else f2(rs + 0.2), f2(1 - d2 / (n * (n * n - 1))), f2(6 * d2 / (n * (n * n - 1))), f2(1 - 6 * d2 / (n * n))],
                   f'1 − (6 × {fmt(d2, 1)}) ÷ ({n} × {n * n - 1}) = {f2(rs)}. [1]')
    parts = [
        L('State a null hypothesis for this investigation.', f'There is no relationship between {xn.split(" (")[0]} and {yn.split(" (")[0]}.', '[1]'),
        L("Calculate Spearman's rank correlation coefficient and use the critical value to decide whether the relationship is significant. State your conclusion about the null hypothesis.",
          f'Σd² = {fmt(d2, 1)}; rs = {f2(rs)}. ' + (f'|rs| ≥ {crit}, so the correlation is significant at the 0.05 level; reject the null hypothesis.' if sig else f'|rs| < {crit}, so the correlation is not significant at the 0.05 level; accept the null hypothesis.'),
          f'ranks assigned [1]; Σd² = {fmt(d2, 1)} [1]; rs = 1 − (6 × {fmt(d2, 1)}) ÷ ({n} × {n * n - 1}) = {f2(rs)} [1]; comparison with {crit} [1]; decision on null hypothesis [1] [5]'),
        L('Describe the direction and strength of the relationship.', ('Positive' if rs > 0 else 'Negative') + (' and strong' if abs(rs) >= 0.7 else ' and moderate' if abs(rs) >= 0.4 else ' and weak') + f' (rs = {f2(rs)}).', '[1]'),
        L('Explain why a scatter graph should also be drawn.', 'It shows the pattern visually, including anomalies and whether the relationship is linear or curved.', '[1]'),
    ]
    return comp(r, intro, parts, D)


@r4.add('C2', (1, 2, 3, 4), 'explain')
def r4_graph(r, D):
    data = r.choice([('the percentage of energy from each source in a country', 'a pie chart or divided bar chart', 'the data are parts of a whole'),
                     ('monthly rainfall and temperature for a city', 'a climate graph (bars for rainfall, line for temperature)', 'it shows two variables over the same months'),
                     ('the distribution of four plant species along a 50 m transect', 'a kite diagram', 'it shows changes in abundance of several species with distance'),
                     ('the relationship between distance from a factory and soil lead concentration', 'a scatter graph', 'it shows whether two continuous variables are related'),
                     ('the number of males and females in each age group', 'a population pyramid', 'it compares age and sex structure'),
                     ('the change in CO₂ concentration from 1960 to 2020', 'a line graph', 'it shows continuous change over time'),
                     ('the number of bird species recorded in five parks', 'a bar chart', 'the categories are discrete'),
                     ('the direction and frequency of winds at a site', 'a wind rose (radial diagram)', 'it shows direction and frequency together')])
    what, g, why = data
    if D == 1:
        others = ['A pie chart or divided bar chart', 'A kite diagram', 'A scatter graph', 'A population pyramid', 'A line graph', 'A bar chart', 'A wind rose (radial diagram)', 'A climate graph (bars for rainfall, line for temperature)']
        return MCQ(r, f'Which is the most suitable way to present {what}?', cap(g), [o for o in others if o != cap(g)], f'{cap(g)}: {why}. [1]')
    return {'stem': f'Suggest the most suitable method of presenting {what}, and justify your choice.', 'answer': f'{cap(g)}, because {why}.', 'key': 'method [1]; justification [1] [2]', 'marks': 2}


r5 = T('Evaluating methods, reliability and limitations of research', 'evaluating methods', 'reliability', 'limitations of research')
build(r5, {
    'terms': [
        ('reliability', 'the extent to which a method gives consistent results when it is repeated'),
        ('validity', 'the extent to which an investigation measures what it intends to measure and the conclusions are justified'),
        ('accuracy', 'how close a measurement is to the true value'),
        ('precision', 'how close repeated measurements are to each other'),
        ('anomaly', 'a result that does not fit the pattern of the other results'),
        ('systematic error', 'an error that shifts all readings in the same direction, for example from an uncalibrated instrument'),
        ('random error', 'unpredictable variation in readings that can be reduced by repeating measurements and calculating a mean'),
        ('bias', 'a systematic distortion of results caused by the way data are collected or the sample is chosen'),
    ],
    'mcq': [
        ('Repeating measurements and calculating a mean mainly improves', 'reliability', ['validity of the hypothesis', 'the number of variables', 'the significance level'], '[1]'),
        ('A pH meter that always reads 0.3 too high has', 'a systematic error', ['a random error', 'high precision only', 'no error'], '[1]'),
        ('Which is the best way to deal with an anomalous result?', 'Identify it, suggest a reason and repeat the measurement if possible', ['Ignore all other results', 'Change it to fit the pattern', 'Include it without comment'], '[1]'),
        ('An investigation using only one stream to draw conclusions about all streams has limited', 'validity (representativeness)', ['precision', 'calibration', 'accuracy of the equipment'], '[1]'),
    ],
    'explain': [
        ('Explain the difference between accuracy and precision.', 'Accuracy is how close a result is to the true value; precision is how close repeated readings are to each other. Results can be precise but inaccurate if there is a systematic error.', 'accuracy [1]; precision [1] [2]'),
        ('Explain how an investigator could improve the reliability of fieldwork data.', 'Take larger samples; repeat measurements and calculate means; use the same equipment and methods; collect data on several days; use calibrated digital instruments; have the same person take readings.', '1 mark per point up to [3]'),
        ('Explain why the conclusions of a small-scale investigation should be treated with caution.', 'Small samples may not be representative; data collected on one day or season may be unusual; other variables may not have been controlled; correlation may not show cause.', '1 mark per point up to [3]'),
        ('Explain the limitations of using secondary data.', 'It may be out of date, collected for a different purpose, use different methods or definitions, contain errors or bias, and the reliability may be unknown.', '1 mark per point up to [3]'),
    ],
    'claims': [
        ('If results support the hypothesis, the investigation must have been reliable.', False, 'Results could support the hypothesis by chance or because of bias; reliability depends on the method and repeatability.'),
        ('Anomalous results should be discussed in an evaluation.', True, 'Explaining possible causes of anomalies shows understanding of the method’s limitations.'),
        ('Using more precise equipment can reduce random error.', True, 'Better resolution and digital meters reduce variation between readings.'),
    ],
})


@r5.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r5_repeat(r, D):
    meas, unit = r.choice([('stream velocity', 'm/s'), ('soil pH', ''), ('noise level', 'dB'), ('light intensity', 'lux'), ('infiltration time', 's'), ('air temperature', '°C')])
    sites = ['1', '2', '3', '4']
    base = {'stream velocity': 0.4, 'soil pH': 6.0, 'noise level': 60, 'light intensity': 800, 'infiltration time': 45, 'air temperature': 18}[meas]
    sc = {'stream velocity': 0.05, 'soil pH': 0.2, 'noise level': 3, 'light intensity': 60, 'infiltration time': 4, 'air temperature': 0.6}[meas]
    dp = 2 if meas in ('stream velocity',) else 1 if meas in ('soil pH', 'air temperature') else 0
    reps = [round(base + r.uniform(-1, 1) * sc, dp) for _ in range(3)]
    anom_i = r.randrange(3)
    anom = round(base + r.choice([-1, 1]) * sc * r.uniform(4, 6), dp)
    reps[anom_i] = anom
    if meas == 'stream velocity' and anom <= 0:
        return None
    good = [x for i, x in enumerate(reps) if i != anom_i]
    m_all = sum(reps) / 3
    m_good = sum(good) / 2

    def fx(x):
        return fmt(round(x, dp + 1), dp + 1)
    u = (' ' + unit) if unit else ''
    intro = f'Three repeat readings of {meas} were taken at one site: ' + ', '.join(f'{fmt(x, dp)}{u}' for x in reps) + '.'
    if D == 1:
        return MCQ(r, intro + ' Which reading is anomalous?', f'{fmt(anom, dp)}{u}', [f'{fmt(x, dp)}{u}' for x in good] + [f'{fx(m_all)}{u}', f'{fx(m_good)}{u}'], f'{fmt(anom, dp)} is far from the other two readings. [1]')
    parts = [
        L('Identify the anomalous reading.', f'{fmt(anom, dp)}{u}', '[1]'),
        L('Calculate the mean of the readings, excluding the anomaly.', f'{fx(m_good)}{u}', f'({" + ".join(fmt(x, dp) for x in good)}) ÷ 2 = {fx(m_good)} [1]'),
        L('Calculate the percentage difference between the mean including the anomaly and the mean excluding it.', f'{f1(abs(m_all - m_good) / m_good * 100)}%', f'mean with anomaly {fx(m_all)} [1]; |{fx(m_all)} − {fx(m_good)}| ÷ {fx(m_good)} × 100 = {f1(abs(m_all - m_good) / m_good * 100)}% [1] [2]'),
        L('Suggest two possible causes of the anomalous reading.', 'Error in reading or recording the instrument; a change in conditions (e.g. a gust of wind, cloud, obstruction in the stream); equipment fault or not calibrated; measuring at a different point.', '1 mark each [2]'),
        L('Explain how the investigator should deal with the anomaly.', 'Repeat the measurement to check it; if confirmed as an error, exclude it from the mean and explain why in the evaluation.', '[2]'),
    ]
    return comp(r, intro, parts, D)


@r5.add('C4', (2, 3, 4, 5), 'case')
def r5_eval(r, D):
    p = person(r)
    ctx, iv, dv, cv, h, h0 = _study(r, p)
    p = _who(ctx, p)
    n = r.choice([5, 6, 8])
    issue, ev = r.choice([(f'{p} sampled only {n} sites, all on one afternoon, and took one reading at each site.',
                           f'Reliability is low: only {n} sites is a small sample; single readings cannot be checked for errors or anomalies; one afternoon may not be typical of other times or weather.'),
                          (f'{p} chose sites where it was easy to reach, took single readings and did not record the weather.',
                           'Site choice was opportunistic, so the sample may be biased and unrepresentative; single readings cannot be checked; weather was not recorded, so its effect on the results cannot be judged.'),
                          (f'{p} used a different piece of equipment at the last two sites after the first one broke, and collected data on two different days.',
                           'Changing equipment may introduce a systematic difference between sites; conditions differed between the two days, so differences may not be caused by the independent variable; results are not directly comparable.')])
    stem = f'{ctx} {issue}'
    parts = [
        L('Evaluate the reliability of the method.', ev, '1 mark per developed point up to [3]'),
        L('Suggest improvements to the method and explain how each would improve the investigation.', f'Increase the number of sites (e.g. 10-15) across the full range of {iv}; take three repeats and calculate means; random or systematic site selection to avoid bias; use the same calibrated equipment; collect all data under similar conditions.', '1 mark per improvement with explanation up to [4]'),
        L('Explain whether the conclusions would be valid.', f'Conclusions are of limited validity because other variables ({cv}) may not have been controlled and the sample may not be representative; a correlation would not prove that {iv} causes changes in {dv}.', '[2]'),
        L('Suggest how secondary data could support the findings.', 'Compare with published studies, government monitoring data or long-term records for the same area to see if the pattern is consistent.', '[1]'),
    ]
    return comp(r, stem, parts, D, 'case')


CHAPTERS[8] = [r1, r2, r3, r4, r5]
