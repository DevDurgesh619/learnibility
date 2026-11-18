"""Cambridge International AS Level Geography 9696 (grade 11): the AS core.

Paper 1 (Core Physical Geography: hydrology and fluvial geomorphology, atmosphere and weather, rocks and
weathering) and Paper 2 (Core Human Geography: population, migration, settlement dynamics). Each paper has
structured, resource-based questions (figures and tables described in words, answers computed in code)
and essays marked out of 15 with the 9696 four-level mark scheme. Case-study items require named, located
examples (place-specific detail) and fieldwork/skills items use 9696 techniques (Spearman's rank, recurrence
intervals, water balance, lapse rates, dependency ratios, rates per 1000).

Knowledge packs reuse the generic builders from g9_geography.py (not modified here); essays and case
studies use the 9696 tariffs defined below. g12_geography.py imports these builders with level 'A2'.
"""
import math
from ._lib import topic, mcq, compose, person, two_people, city, sf, fmt, CTX
from .g9_geography import (T, cap, low, an, add_terms, add_mcqs, add_explain, add_claims, add_case, _markify, mean, median,
                           pct_change, nf, MON, MONTHS)
from .g9_geography import dp as _dp9


def dp(x, n=1):
    """Round to n decimal places. fmt() strips trailing zeros, which would turn 150.0 at 0 dp into "15", so whole
    numbers are formatted directly."""
    if n == 0:
        return str(int(round(x)))
    return _dp9(x, n)

# Mock sections: 'long' slots ask for essay-length marks (>= 12); 'case' (data / case-study / fieldwork) slots ask for
# 5, 7, 9 or 11 marks, values never requested by the mastery bank, so essays can stay out of those slots.
PROFILE = {'mark_scale': {'long': (3.75, 3.0), 'case': (1.8, 1.5)}, 'wordy': True}
CASE_SLOT = (7, 9, 11)


def want():
    return CTX.get('want_marks') or 0
CHAPTERS = {}

# ============================================================== 9696 mark schemes

LV = {
    15: ('Marked out of 15 [15] using levels of response. Level 4 (12-15): detailed, accurate knowledge and understanding of the '
         'topic, well-chosen and developed examples, a sustained evaluation and a well-supported conclusion that addresses '
         '"the extent". Level 3 (8-11): clear knowledge, some appropriate examples, evaluation that is present but partial or '
         'unbalanced. Level 2 (4-7): some knowledge, largely descriptive, examples general or not well linked, little '
         'evaluation. Level 1 (1-3): basic, generalised points with little relevance; no examples. Level 0: no creditable response.'),
    20: ('Marked out of 20 [20] using levels of response. Level 4 (16-20): detailed, accurate and well-integrated knowledge; '
         'well-chosen, place-specific examples; sustained evaluation and a strong, supported conclusion. Level 3 (11-15): clear '
         'knowledge with appropriate examples; evaluation present but uneven or not fully supported. Level 2 (6-10): some '
         'knowledge, mainly descriptive; limited or general examples; little evaluation. Level 1 (1-5): basic, fragmented '
         'points; no examples. Level 0: no creditable response.'),
    8: ('Marked out of 8 [8] using levels. Level 3 (6-8): detailed, accurate explanation with good use of examples or the '
        'resource. Level 2 (3-5): some explanation, partly developed, general examples. Level 1 (1-2): simple, descriptive '
        'points. Level 0: no creditable response.'),
    10: ('Marked out of 10 [10] using levels. Level 3 (8-10): detailed, accurate and well-developed answer with place-specific '
         'support. Level 2 (4-7): some development, examples general or partly relevant. Level 1 (1-3): simple, descriptive '
         'points. Level 0: no creditable response.'),
}
LEVEL = {'AS': (8, 15, 27.0), 'A2': (10, 20, 36.0)}

ESSAY_LEADS96 = [
    lambda c, p: f'“{cap(c)}.” How far do you agree with this statement?',
    lambda c, p: f'To what extent do you agree that {c}?',
    lambda c, p: f'Assess the view that {c}.',
    lambda c, p: f'With the help of examples, evaluate the claim that {c}.',
    lambda c, p: f'{p} argues that {c}. How far do you agree? Support your answer with examples.',
    lambda c, p: f'“{cap(c)}.” Discuss.',
]


def add_essay96(t, claim, pro, con, judge, hints=(), lvl='AS', D=(2, 3, 4, 5)):
    short, full, mins = LEVEL[lvl]

    def fn(r, D_):
        w = want()
        if w in CASE_SLOT:
            return None
        if w >= 12:
            D_ = max(D_, 3)
        p = person(r)
        ans = 'For: ' + ' '.join(pro) + ' Against: ' + ' '.join(con) + ' Conclusion: ' + judge
        if D_ <= 2:
            stem = r.choice([f'Explain the arguments for and against the view that {claim}.',
                             f'Outline the evidence that supports, and the evidence that challenges, the view that {claim}.'])
            return {'stem': stem, 'answer': ans, 'key': LV[short] + ' Indicative content: for and against, with examples; no overall judgement is required.',
                    'type': 'long', 'marks': short, 'minutes': round(short * 1.6)}
        stem = r.choice(ESSAY_LEADS96)(claim, p)
        if hints and r.random() < 0.6:
            hs = r.sample(list(hints), min(len(hints), r.choice([2, 3])))
            stem += ' In your answer you may refer to ' + ', '.join(hs[:-1]) + ' and ' + hs[-1] + '.'
        return {'stem': stem, 'answer': ans, 'key': LV[full] + ' Indicative content: ' + ' '.join(pro + con) + ' Judgement: ' + judge,
                'type': 'long', 'marks': full, 'minutes': mins}
    fn.__name__ = 'essay'
    t.add('C4', D, 'long')(fn)

    def fn3(r, D_):
        # only used for essay-length slots of mock papers (want >= 12); never in the mastery bank
        return fn(r, max(D_, 3)) if want() >= 12 else None
    fn3.__name__ = 'essay3'
    t.add('C3', (4, 5), 'long')(fn3)


CS96_LEADS = [
    lambda k, n, p: f'With reference to a case study of {k}, {p}.',
    lambda k, n, p: f'Using a named example of {k}, such as {n}, {p}.',
    lambda k, n, p: f'For {n}, or another example of {k} you have studied, {p}.',
    lambda k, n, p: f'With the help of a case study of {k} you have studied, {p}.',
]


def add_cs96(t, kind, cases, prompts, lvl='AS'):
    """Case-study recall. cases: [(name, {aspect: model answer})]; prompts: [(prompt, aspect, indicative[, evaluative prompt])].

    C3: short place-specific answer [5]. C4: D2 levels-marked part answer (8 AS / 10 A2); D3+ full essay (15 AS / 20 A2)
    built from the evaluative prompt.
    """
    short, full, mins = LEVEL[lvl]

    def c4(r, D):
        w = want()
        if w in CASE_SLOT:
            return None
        if w >= 12:
            D = max(D, 3)
        name, facts = r.choice(cases)
        ok = [p for p in prompts if p[1] in facts]
        if not ok:
            return None
        pr = r.choice(ok)
        ev = pr[3] if len(pr) > 3 else None
        if w >= 12 and not ev:
            ev = f'{pr[0]}. To what extent is your chosen example typical of {kind}?'
        if D <= 2 or not ev:
            stem = r.choice(CS96_LEADS)(kind, name, pr[0])
            return {'stem': stem, 'answer': f'Model answer ({name}): {facts[pr[1]]}', 'key': LV[short] + ' Indicative content: ' + pr[2],
                    'type': 'long', 'marks': short, 'minutes': round(short * 1.6)}
        stem = r.choice([f'With reference to a case study of {kind}, {ev}',
                         f'Using a named example of {kind} you have studied, {ev}',
                         f'Referring to {name} or another example of {kind}, {ev}'])
        return {'stem': stem, 'answer': f'Model answer ({name}): ' + ' '.join(facts.values()), 'key': LV[full] + ' Indicative content: ' + pr[2] + ' A balanced judgement is required for Level 4.',
                'type': 'long', 'marks': full, 'minutes': mins}
    c4.__name__ = 'cs'
    t.add('C4', (2, 3, 4, 5), 'long')(c4)

    def c3(r, D):
        if want() >= 12:
            return c4(r, max(D, 3))
        name, facts = r.choice(cases)
        ok = [p for p in prompts if p[1] in facts]
        if not ok:
            return None
        pr = r.choice(ok)
        lead = r.choice([f'Name a case study of {kind} you have studied. For your example, {pr[0]}.',
                         f'Briefly {pr[0]}, for {name} or another example of {kind}.',
                         f'Using one named example of {kind}, {pr[0]}.'])
        return {'stem': lead, 'answer': f'{name}: {facts[pr[1]]}', 'key': '1 mark for a named, located example; up to 4 marks for accurate, '
                'place-specific points (names, dates, figures), max 2 if general. ' + pr[2] + ' [5]', 'type': 'case', 'marks': 5}
    c3.__name__ = 'cs3'
    t.add('C3', (2, 3, 4), 'case')(c3)


def B(t, P, lvl='AS'):
    """Build a topic from a knowledge pack (see module docstring)."""
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
        add_cs96(t, *cs, lvl=lvl)
    for e in P.get('essays', []):
        add_essay96(t, *e, lvl=lvl)
    _markify(t, start)
    return t


def as_c4(t, fn, D=(3, 4, 5)):
    """Register a data template again as a multi-step (C4) item using its fullest form."""
    def g(r, D_, fn=fn):
        q = fn(r, max(D_, 4))
        if q and q.get('options'):
            return None
        return q
    g.__name__ = fn.__name__ + '_c4'
    t.add('C4', D, 'multi_step')(g)


def data(t, D=(1, 2, 3, 4, 5), c4=True, typ='numerical'):
    """Decorator: register a C3 data template (and, by default, its C4 multi-step version)."""
    def deco(fn):
        t.add('C3', D, typ)(fn)
        if c4:
            as_c4(t, fn)
        return fn
    return deco


def kk(D):
    return (2, 3) if D <= 3 else (3, 4)


def sgn(x, n=1):
    return ('+' if x > 0 else '−' if x < 0 else '') + dp(abs(x), n)


# ============================================================== skills: Spearman's rank

CRIT = {8: (0.643, 0.833), 9: (0.600, 0.783), 10: (0.564, 0.745), 11: (0.536, 0.709), 12: (0.503, 0.678)}


def ranks(xs, high_first=True):
    """Rank values (1 = highest by default); ties get the mean rank."""
    order = sorted(range(len(xs)), key=lambda i: -xs[i] if high_first else xs[i])
    rk = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            rk[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return rk


def spearman(xs, ys):
    rx, ry = ranks(xs), ranks(ys)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    n = len(xs)
    return 1 - 6 * d2 / (n ** 3 - n), d2, rx, ry


def _series(r, n, lo, hi, nd, distinct=True):
    for _ in range(50):
        unit = 10 ** -nd
        cnt = int(round((hi - lo) / unit))
        vals = [round(lo + r.randint(0, cnt) * unit, nd) if nd else lo + r.randint(0, cnt) for _ in range(n)]
        if not distinct or len(set(vals)) == n:
            return vals
    return None


def add_spearman(t, contexts, C3=(1, 2, 3, 4, 5)):
    """contexts: dicts with intro (str with {n}), label (site label prefix), x/y = (name, lo, hi, decimals),
    sign (+1/-1 expected), why (explanation), limit (limitation), h1 (hypothesis wording)."""
    def fn(r, D):
        c = r.choice(contexts)
        n = r.choice([8, 10]) if D <= 2 else r.choice([10, 11, 12])
        xs = _series(r, n, *c['x'][1:])
        if not xs:
            return None
        xs.sort()
        lo, hi, nd = c['y'][1:]
        strength = r.choice([0.15, 0.25, 0.45, 0.9])
        span = hi - lo
        ys = []
        x0, x1 = xs[0], xs[-1]
        for x in xs:
            frac = (x - x0) / ((x1 - x0) or 1)
            base = lo + span * (frac if c['sign'] > 0 else 1 - frac)
            v = base + r.uniform(-1, 1) * span * strength
            v = min(hi, max(lo, v))
            ys.append(round(v, nd) if nd else int(round(v)))
        if len(set(ys)) < n:
            return None
        rs, d2, rx, ry = spearman(xs, ys)
        crit5, crit1 = CRIT[n]
        lab = c['label']
        f = (lambda v, d: fmt(v, d) if d else str(int(v)))
        tab = ' '.join(f'{lab} {i + 1}: {f(x, c["x"][3])}, {f(y, nd)}.' for i, (x, y) in enumerate(zip(xs, ys)))
        stem = c['intro'].format(n=n) + f' Table {r.randint(1, 4)}.{r.randint(1, 3)} gives, for each {lab.lower()}, the {c["x"][0]} and the {c["y"][0]}. ' + tab
        sig = 'significant at the 0.01 level' if abs(rs) >= crit1 else 'significant at the 0.05 level' if abs(rs) >= crit5 else 'not significant at the 0.05 level'
        direction = 'positive' if rs > 0 else 'negative'
        conc = (f'rs = {fmt(rs, 3)}: a {direction} correlation that is {sig}' + ('; reject the null hypothesis.' if abs(rs) >= crit5 else '; accept the null hypothesis (the relationship could be due to chance).'))
        if D == 1:
            opts, a = mcq(r, fmt(rs, 3), [fmt(-rs, 3), fmt(6 * d2 / (n ** 3 - n), 3), fmt(1 - d2 / (n ** 3 - n), 3), fmt(rs + 0.1, 3), fmt(rs - 0.1, 3)])
            return {'stem': stem + f' The sum of the squared rank differences (Σd²) is {fmt(d2, 1)}. Using rs = 1 − 6Σd² ÷ (n³ − n), what is the value of rs?',
                    'options': opts, 'answer': a, 'key': f'rs = 1 − (6 × {fmt(d2, 1)}) ÷ ({n}³ − {n}) = {fmt(rs, 3)}. [1]'}
        given = f' Critical values of rs for n = {n}: {crit5} (0.05 level) and {crit1} (0.01 level).'
        parts = [
            lambda r: ('State a suitable null hypothesis for this investigation.', f'There is no relationship between the {c["x"][0]} and the {c["y"][0]}.', '[1]'),
            lambda r: (('Σd² = ' + fmt(d2, 1) + '. ' if D <= 3 else '') + 'Calculate Spearman’s rank correlation coefficient (rs), showing your working, and interpret the result using the critical values.',
                       fmt(rs, 3) + '. ' + conc,
                       f'Rank both variables, find d and d²; Σd² = {fmt(d2, 1)}; rs = 1 − (6 × {fmt(d2, 1)}) ÷ ({n}³ − {n}) = {fmt(rs, 3)}. Interpretation: {conc} '
                       + ('1 mark substitution, 1 mark rs, 1 mark direction/strength, 1 mark significance [4]' if D <= 3 else '1 mark ranks, 1 mark Σd², 1 mark rs, 1 mark direction/strength, 1 mark significance [5]')),
            lambda r: (f'Suggest reasons for the {"relationship" if abs(rs) >= crit5 else "result"} shown by the data.', c['why'] + ('' if abs(rs) >= crit5 else ' Here the relationship is weak, so other local factors or sampling error matter.'), '1 mark per developed reason [3]'),
            lambda r: ('Suggest one limitation of the method and how the investigation could be improved.', c['limit'], '1 mark limitation; 1 mark improvement [2]'),
        ]
        q = compose(r, stem + given, parts, k=kk(D), type_='numerical')
        return q
    fn.__name__ = 'spearman'
    t.add('C3', C3, 'numerical')(fn)
    as_c4(t, fn)
    return fn


# ============================================================== misc data helpers

def cm_pct(a, b):
    """percentage of a in b"""
    return a / b * 100


def ri(n, m):
    return (n + 1) / m


def letters(k):
    return list('ABCDEFGHJKLM'[:k])


# ============================================================== CHAPTER 1: The drainage basin system

BASINS = ['River Exe (UK)', 'River Tana (Kenya)', 'Rio Itajaí (Brazil)', 'River Kelani (Sri Lanka)', 'Mekong tributary (Laos)', 'River Ouse (UK)',
          'Waikato River (New Zealand)', 'River Rhône (France)', 'Ganges headwater (Nepal)', 'River Severn (UK)']

c1a = T('Inputs, outputs, stores and flows in the drainage basin system', 'drainage basin system inputs outputs stores flows')
B(c1a, {
    'terms': [
        ('drainage basin', 'the area of land drained by a river and its tributaries, bounded by a watershed'),
        ('watershed', 'the boundary of a drainage basin, usually a ridge of high land separating one basin from the next'),
        ('open system', 'a system that receives inputs from, and loses outputs to, outside its boundary, as the drainage basin does'),
        ('evapotranspiration', 'the combined loss of water to the atmosphere by evaporation from surfaces and transpiration from plants'),
        ('channel flow', 'the movement of water within a river channel towards the basin outlet'),
        ('channel storage', 'the water held at any one time within the river channel itself'),
        ('percolation', 'the downward movement of water from the soil into the underlying rock'),
        ('confluence', 'the point where two rivers or streams join'),
    ],
    'mcq': [
        ('Which of the following is an output from the drainage basin system?', 'Evapotranspiration', ['Precipitation', 'Interception storage', 'Throughflow'], 'Evapotranspiration and channel discharge leave the basin. [1]'),
        ('Which of the following is a store in the drainage basin hydrological cycle?', 'Groundwater', ['Percolation', 'Stemflow', 'Infiltration'], 'Percolation, stemflow and infiltration are flows (transfers). [1]'),
        ('The drainage basin is described as an open system because', 'it has inputs and outputs of water and energy that cross its boundary', ['water circulates within it without leaving', 'it has no boundary', 'its stores never change'], '[1]'),
        ('Which flow transfers water from the soil store to the groundwater store?', 'Percolation', ['Infiltration', 'Throughflow', 'Interception'], '[1]'),
        ('The water balance equation for a drainage basin is', 'P = Q + E ± ΔS', ['P = Q − E ± ΔS', 'Q = P + E ± ΔS', 'E = P + Q ± ΔS'], 'Precipitation = discharge + evapotranspiration ± change in storage. [1]'),
    ],
    'explain': [
        ('Explain why the drainage basin is regarded as an open system while the global hydrological cycle is a closed system.', 'The basin receives precipitation from outside and loses water by evapotranspiration and channel discharge across its boundary; the global cycle has a fixed amount of water that only moves between stores (oceans, atmosphere, ice, land).', '1 mark inputs/outputs of basin; 1 mark fixed global water; 1 mark energy still crosses the global boundary [3]'),
        ('Describe the pathways by which precipitation falling on a forested drainage basin may reach the river channel.', 'Intercepted then throughfall or stemflow to the ground; infiltration into the soil and throughflow downslope; percolation to groundwater and slow baseflow; overland flow when the soil is saturated or rainfall intense; direct channel precipitation.', '1 mark per pathway, max 2 if no sequence [4]'),
        ('Explain how the size of the groundwater store affects river flow during a dry season.', 'Groundwater drains slowly into the channel as baseflow; a large aquifer (e.g. permeable chalk or sandstone) maintains flow during dry months, whereas impermeable basins have little store and rivers may dry up.', '1 mark baseflow; 1 mark slow release; 1 mark rock type example [3]'),
        ('Explain how deforestation alters stores and flows in a drainage basin.', 'Less interception storage and transpiration; more rain reaches the ground quickly; soil compaction lowers infiltration so more overland flow; less soil moisture and groundwater recharge; faster channel flow and higher flood peaks.', '1 mark per developed change [4]'),
        ('Suggest why evapotranspiration is a much larger output in a tropical rainforest basin than in a sub-arctic basin.', 'High temperatures and insolation all year supply energy for evaporation; dense multi-layered vegetation transpires large volumes; abundant water is available; in sub-arctic basins low temperatures, frozen ground and sparse vegetation limit it.', '1 mark energy; 1 mark vegetation; 1 mark contrast [3]'),
    ],
    'claims': [
        ('All precipitation that falls in a drainage basin eventually leaves as river discharge.', False, 'Much is lost by evapotranspiration and some is held in long-term stores such as deep groundwater or ice.'),
        ('Throughflow is usually slower than overland flow.', True, 'Water moving through soil pores meets more resistance than water flowing over the surface.'),
        ('A watershed is a store of water at the head of a valley.', False, 'A watershed is the boundary (divide) of a drainage basin, not a store.'),
        ('Human activity can change the water balance of a basin.', True, 'Abstraction, irrigation, reservoirs, urbanisation and deforestation all change stores, flows and outputs.'),
    ],
    'cases': [
        (['Fig. 1.1 is a systems diagram of a drainage basin. It shows inputs (precipitation), stores (interception, surface, soil, groundwater, channel) and transfers (throughfall, stemflow, infiltration, percolation, throughflow, overland flow, baseflow) and outputs (evapotranspiration, discharge).',
          'A student draws a flow diagram of the drainage basin system for a small upland catchment in the Pennines, UK, with peat moorland on impermeable gritstone.'],
         [('Name two stores shown in the system.', 'Any two of: interception, surface (depression) storage, soil moisture, groundwater, channel storage.', '1 mark each [2]'),
          ('Distinguish between infiltration and percolation.', 'Infiltration is water entering the soil surface; percolation is water moving down from the soil into the rock below.', '1 mark each [2]'),
          ('Explain how saturated peat on impermeable rock would affect the transfers shown.', 'Infiltration and percolation are low; most water moves as saturated overland flow or throughflow in the peat; little groundwater and baseflow, so rapid flood peaks.', '1 mark per developed point [3]'),
          ('Explain why channel discharge continues during rainless periods in some basins.', 'Baseflow from groundwater and slow throughflow from the soil continue to supply the channel.', '1 mark baseflow; 1 mark source [2]'),
          ('Suggest how one human activity could increase the output of water from this basin.', 'Drainage ditches (gripping) on the moor or clearing vegetation speed flows and increase discharge; reservoirs may increase evaporation.', '1 mark activity; 1 mark explanation [2]')]),
    ],
    'cs': [
        ('a drainage basin', [
            ('the Amazon basin, South America', {'system': 'About 7 million km² with annual rainfall of 2000-3000 mm; around half of precipitation is recycled by evapotranspiration from the rainforest; mean discharge at the mouth about 200 000 m³/s, about 15-20% of all river water entering the oceans.',
                                                 'human': 'Deforestation for cattle ranching and soya (e.g. in Mato Grosso and Rondônia) reduces interception and evapotranspiration; research suggests reduced recycling of moisture lowers rainfall downwind and lengthens the dry season; dams such as Belo Monte on the Xingu alter channel flow.'}),
            ('the River Severn basin, UK', {'system': 'About 11 400 km²; rises on Plynlimon in Wales (over 2000 mm rain a year on impermeable rocks with peat) and flows about 350 km to the Bristol Channel; mean discharge about 107 m³/s at Bewdley; lower basin has permeable sandstones that store groundwater.',
                                            'human': 'Reservoirs (Clywedog, Vyrnwy) regulate flow; urban growth at Shrewsbury and Worcester increases runoff; conifer plantations on Plynlimon increased interception; flood barriers at Bewdley and Shrewsbury.'}),
        ], [
            ('describe the main inputs, stores and outputs of the basin', 'system', 'Inputs (precipitation figures), stores (soil, groundwater, vegetation), flows and outputs (evapotranspiration, discharge), with figures.',
             'assess the extent to which human activities have changed the stores and flows of the drainage basin.'),
            ('explain how human activities have changed the drainage basin system', 'human', 'Land-use change, dams, abstraction, urbanisation; effects on named stores and flows.',
             'evaluate whether physical or human factors have the greater influence on the drainage basin system.'),
        ]),
    ],
    'essays': [
        ('human activity has a greater effect than physical factors on the transfers of water within a drainage basin',
         ['Urbanisation replaces permeable soil with concrete, cutting infiltration; deforestation removes interception; field drains and channelisation speed throughflow and channel flow.'],
         ['Rock permeability, soil type, slope and vegetation set the basic pattern of transfers; climate (rainfall intensity, frozen ground) controls overland flow in most basins.'],
         'Physical factors set the baseline in all basins, but in heavily modified (urban or deforested) basins human activity dominates transfers.',
         ['urbanisation', 'rock type', 'vegetation', 'rainfall intensity']),
    ],
})


@data(c1a)
def c1a_balance(r, D):
    nm = r.choice(BASINS)
    A = r.choice([250, 400, 600, 800, 1200, 1500])
    P = r.randint(70, 260) * 10
    E = r.randint(int(P * 0.25 / 10), int(P * 0.6 / 10)) * 10
    S = r.choice([-60, -40, -20, 20, 40, 60, 80])
    Qmm = P - E - S
    vol = A * 1e6 * Qmm / 1000
    Qm3 = vol / 31_536_000
    stem = f'Table 1.1 gives annual water balance data for part of the {nm} catchment (area {nf(A)} km²): precipitation {nf(P)} mm, evapotranspiration {nf(E)} mm, and an estimated change in storage of {sgn(S, 0)} mm.'
    if D == 1:
        opts, a = mcq(r, f'{nf(Qmm)} mm', [f'{nf(P - E + S)} mm', f'{nf(P + E - S)} mm', f'{nf(P - E)} mm' if S else f'{nf(P)} mm', f'{nf(E + S)} mm'])
        return {'stem': stem + ' Using P = Q + E ± ΔS, what is the runoff (Q) in mm?', 'options': opts, 'answer': a, 'key': f'Q = P − E − ΔS = {P} − {E} − ({S}) = {Qmm} mm. [1]'}
    parts = [
        lambda r: ('Using the water balance equation, calculate the annual runoff (Q) in mm.', f'{nf(Qmm)} mm', f'Q = P − E − ΔS = {P} − {E} − ({S}) = {Qmm} [2]'),
        lambda r: ('Calculate the runoff as a percentage of precipitation (the runoff coefficient).', f'{dp(Qmm / P * 100)}%', f'{Qmm} ÷ {P} × 100 = {dp(Qmm / P * 100)}% [1]'),
        lambda r: ('Convert the annual runoff to a mean discharge at the basin outlet in m³/s (1 year ≈ 31.5 million seconds).', f'about {sf(Qm3)} m³/s',
                   f'volume = {nf(A)} × 10⁶ m² × {Qmm} ÷ 1000 m = {sf(vol)} m³; ÷ 31 536 000 s = {sf(Qm3)} m³/s [3]'),
        lambda r: ('State what a ' + ('negative' if S < 0 else 'positive') + ' change in storage suggests about the year.', ('Stores (soil moisture, groundwater) were drawn down: a drier than average year or heavy abstraction.' if S < 0 else 'Stores were recharged: a wetter year or reduced abstraction, so soil moisture and groundwater rose.'), '[1]'),
        lambda r: ('Suggest two reasons why evapotranspiration varies between drainage basins.', 'Temperature and insolation; vegetation type and density (transpiration); wind speed and humidity; water availability; surface type.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@c1a.add('C2', (1, 2, 3), 'short')
def c1a_classify(r, D):
    items = [('precipitation', 'input'), ('evapotranspiration', 'output'), ('river discharge at the mouth', 'output'), ('groundwater', 'store'),
             ('soil moisture', 'store'), ('interception by leaves', 'store'), ('channel storage', 'store'), ('infiltration', 'flow'), ('percolation', 'flow'),
             ('throughflow', 'flow'), ('stemflow', 'flow'), ('baseflow', 'flow'), ('overland flow', 'flow'), ('surface (depression) storage', 'store')]
    k = 4 if D <= 2 else 6
    pick = r.sample(items, k)
    stem = r.choice(['Classify each of the following components of the drainage basin system as an input, output, store or flow (transfer):',
                     'For each component, state whether it is an input, an output, a store or a transfer in the drainage basin system:']) + ' ' + '; '.join(p for p, _ in pick) + '.'
    return {'stem': stem, 'answer': '; '.join(f'{p}: {c}' for p, c in pick), 'key': f'1 mark for every two correct [{k // 2}]', 'marks': k // 2, 'type': 'short'}


# --------------------------------------------------------------- 1.2 interception and infiltration
c1b = T('Interception, infiltration, throughfall and stemflow', 'interception infiltration throughfall stemflow')
B(c1b, {
    'terms': [
        ('interception', 'the capture and temporary storage of precipitation by vegetation before it reaches the ground'),
        ('throughfall', 'precipitation that drips from leaves or falls through gaps in the canopy to the ground'),
        ('stemflow', 'water that flows down branches and trunks to the ground'),
        ('infiltration', 'the downward movement of water from the surface into the soil'),
        ('infiltration capacity', 'the maximum rate at which a soil can absorb water, usually measured in mm per hour'),
        ('interception loss', 'water that is caught by vegetation and evaporated back to the atmosphere without reaching the ground'),
        ('field capacity', 'the amount of water a soil can hold after excess water has drained away by gravity'),
    ],
    'mcq': [
        ('Interception losses are usually greatest from', 'a coniferous forest in light, intermittent rain', ['a cereal crop in heavy rain', 'bare soil in a storm', 'a deciduous woodland in winter'], 'Dense year-round needles hold water that evaporates between showers. [1]'),
        ('Infiltration capacity is highest on', 'a deep, dry sandy soil under woodland', ['a compacted clay footpath', 'tarmac in a car park', 'frozen ground'], '[1]'),
        ('If rainfall intensity is 25 mm/h and infiltration capacity is 10 mm/h, the excess 15 mm/h will mostly become', 'infiltration-excess (Hortonian) overland flow', ['percolation', 'stemflow', 'baseflow'], '[1]'),
        ('Which of the following increases infiltration?', 'Burrowing animals and plant roots creating macropores', ['Compaction by machinery', 'Raindrop impact sealing the surface', 'Soil already at field capacity'], '[1]'),
    ],
    'explain': [
        ('Explain why infiltration rates decrease during a long period of rainfall.', 'Soil pores fill and the soil approaches saturation; raindrop impact seals the surface (crusting); swelling clays close cracks; so infiltration falls towards a steady rate.', '1 mark per developed point [3]'),
        ('Explain the factors that influence the amount of interception.', 'Vegetation type and density (conifers > deciduous > grass); season (leaf cover); rainfall intensity and duration (light rain mostly intercepted, storage capacity filled in long storms); wind speed and evaporation between showers.', '1 mark per factor with explanation [4]'),
        ('Explain why stemflow is a larger proportion of rainfall under some trees than others.', 'Branches angled upwards and smooth bark channel water to the trunk (e.g. beech); rough bark and drooping branches lead to more throughfall.', '1 mark branch architecture; 1 mark bark [2]'),
        ('Explain how land use affects infiltration.', 'Forest litter and roots keep pores open (high infiltration); grazing and machinery compact soil; ploughing may increase it temporarily; urban surfaces are impermeable.', '1 mark per land use explained [3]'),
    ],
    'claims': [
        ('Interception is the same in a deciduous forest throughout the year.', False, 'In winter, leafless deciduous trees intercept far less than in summer.'),
        ('Saturated soils can produce overland flow even when rainfall intensity is low.', True, 'Saturation-excess overland flow occurs when there is no pore space left, whatever the rainfall rate.'),
        ('Stemflow increases the amount of water reaching the ground directly around tree trunks.', True, 'It concentrates water at the base of the trunk, where infiltration can be high along roots.'),
        ('Throughfall and interception are the same process.', False, 'Interception is the capture of rain by vegetation; throughfall is rain that reaches the ground through or from the canopy.'),
    ],
    'essays': [
        ('vegetation is the most important factor controlling how much precipitation infiltrates into the soil',
         ['Vegetation intercepts rain and slows its arrival; roots and soil fauna create macropores; litter protects soil from crusting; forest soils have very high infiltration capacities.'],
         ['Soil texture and structure (sand v clay), antecedent moisture, rainfall intensity, slope angle, frozen ground and urban surfaces can override vegetation.'],
         'Vegetation is very important in natural basins, but rainfall intensity and soil conditions (saturation, frost, compaction) often determine infiltration during storms.',
         ['soil type', 'rainfall intensity', 'antecedent conditions', 'land use']),
    ],
})

CANOPIES = [('tropical rainforest in Sabah, Malaysia', 0.12, 0.25), ('coniferous (Sitka spruce) plantation in Scotland', 0.25, 0.40), ('deciduous oak woodland in summer', 0.15, 0.30),
            ('deciduous oak woodland in winter', 0.05, 0.12), ('maize field in Kenya', 0.06, 0.15), ('eucalyptus plantation in Brazil', 0.10, 0.20)]


@data(c1b)
def c1b_intercept(r, D):
    nm, lo, hi = r.choice(CANOPIES)
    P = r.randint(20, 80)
    loss = round(P * r.uniform(lo, hi), 1)
    SF = round(P * r.uniform(0.01, 0.08), 1)
    TF = round(P - loss - SF, 1)
    L = round(P - TF - SF, 1)
    pc = L / P * 100
    stem = f'{person(r)} measured rainfall in a storm in a {nm}. A rain gauge in a nearby clearing collected {P} mm; gauges below the canopy recorded a mean throughfall of {fmt(TF, 1)} mm and stemflow collars recorded the equivalent of {fmt(SF, 1)} mm.'
    if D == 1:
        opts, a = mcq(r, f'{fmt(L, 1)} mm', [f'{fmt(P - TF, 1)} mm', f'{fmt(TF + SF, 1)} mm', f'{fmt(P - SF, 1)} mm', f'{fmt(L * 2, 1)} mm', f'{fmt(L / 2, 1)} mm'])
        return {'stem': stem + ' What was the interception loss?', 'options': opts, 'answer': a, 'key': f'{P} − ({fmt(TF, 1)} + {fmt(SF, 1)}) = {fmt(L, 1)} mm. [1]'}
    parts = [
        lambda r: ('Calculate the interception loss in mm.', f'{fmt(L, 1)} mm', f'gross rainfall − (throughfall + stemflow) = {P} − ({fmt(TF, 1)} + {fmt(SF, 1)}) = {fmt(L, 1)} [1]'),
        lambda r: ('Calculate the interception loss as a percentage of gross rainfall.', f'{dp(pc)}%', f'{fmt(L, 1)} ÷ {P} × 100 = {dp(pc)}% [2]'),
        lambda r: ('Suggest how the percentage would differ in a longer, more intense storm. Explain your answer.', 'Lower percentage: the canopy storage capacity is soon filled, so once leaves are saturated most extra rain becomes throughfall.', '1 mark lower; 1 mark storage capacity [2]'),
        lambda r: ('Suggest two sources of error in this method.', 'Gauges sample only a few points under a patchy canopy; splash in or out of gauges; evaporation from gauges; stemflow collars leak; the clearing gauge may be affected by nearby trees.', '1 mark each [2]'),
        lambda r: ('Explain how the interception loss affects the shape of the river’s storm hydrograph.', 'Less water reaches the ground and it arrives more slowly, so lag time increases and peak discharge is lower.', '1 mark lag; 1 mark peak [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@data(c1b)
def c1b_infil(r, D):
    site = r.choice(['an ungrazed woodland', 'a school playing field', 'a heavily used footpath', 'arable land after harvest', 'grazed pasture'])
    cap0 = {'an ungrazed woodland': 60, 'a school playing field': 25, 'a heavily used footpath': 8, 'arable land after harvest': 30, 'grazed pasture': 18}[site]
    times = [0, 5, 10, 15, 20, 30]
    rate = [round(cap0 * (1 + 2.0 * math.exp(-t / 8)) * r.uniform(0.95, 1.05)) for t in times]
    stem = f'A ring infiltrometer was used on {site}. The infiltration rates recorded (mm/h) after 0, 5, 10, 15, 20 and 30 minutes were: ' + ', '.join(str(x) for x in rate) + '.'
    pc = pct_change(rate[0], rate[-1])
    I = r.choice([10, 15, 20, 30, 40])
    over = I > rate[-1]
    if D == 1:
        opts, a = mcq(r, f'{dp(abs(pc))}%', [f'{dp(abs(pc) / 2)}%', f'{rate[0] - rate[-1]}%', f'{dp(rate[-1] / rate[0] * 100)}%', f'{dp(abs(pc) + 10)}%'])
        return {'stem': stem + ' By what percentage did the infiltration rate fall over the 30 minutes?', 'options': opts, 'answer': a,
                'key': f'({rate[0]} − {rate[-1]}) ÷ {rate[0]} × 100 = {dp(abs(pc))}%. [1]'}
    parts = [
        lambda r: ('Describe the change in infiltration rate. Use data.', f'Rapid fall at first, from {rate[0]} mm/h to {rate[2]} mm/h in 10 minutes, then levelling off towards about {rate[-1]} mm/h (the infiltration capacity of the saturated soil).', '1 mark trend; 1 mark levelling; 1 mark data [3]'),
        lambda r: ('Calculate the percentage decrease in infiltration rate between 0 and 30 minutes.', f'{dp(abs(pc))}%', f'({rate[0]} − {rate[-1]}) ÷ {rate[0]} × 100 = {dp(abs(pc))}% [2]'),
        lambda r: (f'A storm brings rain with an intensity of {I} mm/h for several hours. State, with a reason, whether infiltration-excess overland flow would occur here.',
                   (f'Yes: {I} mm/h exceeds the steady infiltration rate of about {rate[-1]} mm/h, so the excess flows over the surface.' if over else f'Probably not: {I} mm/h is below the steady infiltration rate of about {rate[-1]} mm/h, so rain can infiltrate (unless the soil becomes saturated).'), '1 mark decision; 1 mark comparison with data [2]'),
        lambda r: ('Explain why the infiltration rate falls with time.', 'Soil pores fill with water as the soil approaches saturation, and fine particles and raindrop impact seal the surface.', '1 mark pores filling; 1 mark further reason [2]'),
        lambda r: ('Suggest why the steady infiltration rate here may differ from that of an ungrazed woodland.' if site != 'an ungrazed woodland' else 'Suggest why the steady rate would be lower on a heavily used footpath.',
                   'Compaction by trampling, livestock or machinery reduces pore spaces; less organic matter and fewer roots and burrows; woodland litter protects the surface.', '1 mark compaction; 1 mark roots/organic matter [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


add_spearman(c1b, [
    {'intro': 'A student tested the hypothesis that infiltration rate increases with vegetation cover at {n} sites in a small catchment.', 'label': 'Site',
     'x': ('vegetation cover (%)', 5, 98, 0), 'y': ('infiltration rate (mm/h)', 4, 70, 0), 'sign': 1,
     'why': 'Vegetation protects the surface from raindrop impact and crusting; roots and soil organisms create macropores; organic matter improves soil structure, so more water enters the soil.',
     'limit': 'Only one reading per site and soils may differ in texture or moisture; take repeat readings at each site and record antecedent soil moisture.'},
    {'intro': 'A group measured infiltration rates at {n} points at increasing distance from a busy footpath in a national park.', 'label': 'Point',
     'x': ('distance from the footpath (m)', 0, 30, 0), 'y': ('infiltration rate (mm/h)', 3, 55, 0), 'sign': 1,
     'why': 'Trampling compacts the soil near the path, reducing pore space and destroying vegetation, so infiltration is lowest close to the path and rises away from it.',
     'limit': 'Points lie along one transect only and soil type may change; use several transects and measure soil compaction with a penetrometer.'},
])


# --------------------------------------------------------------- 1.3 overland flow, throughflow, groundwater, water balance
c1c = T('Overland flow, throughflow, groundwater and the water balance', 'overland flow throughflow groundwater water balance')
B(c1c, {
    'terms': [
        ('overland flow', 'water that flows across the ground surface when rainfall exceeds infiltration capacity or the soil is saturated'),
        ('throughflow', 'the lateral movement of water downslope through the soil'),
        ('groundwater flow', 'the slow movement of water through permeable rock below the water table'),
        ('baseflow', 'the part of river discharge supplied by groundwater, which maintains flow between storms'),
        ('water table', 'the upper surface of the saturated zone in soil or rock'),
        ('aquifer', 'a permeable rock, such as chalk or sandstone, that stores and transmits groundwater'),
        ('soil moisture deficit', 'the amount of water needed to bring a soil back up to field capacity'),
        ('groundwater recharge', 'the replenishment of groundwater stores by water percolating down from the surface'),
    ],
    'mcq': [
        ('In a water balance graph, the period when potential evapotranspiration exceeds precipitation and plants use stored soil water is called', 'soil moisture utilisation', ['soil moisture recharge', 'water surplus', 'field capacity'], '[1]'),
        ('Saturation-excess overland flow is most likely', 'on lower slopes near streams after prolonged rain', ['on steep upper slopes at the start of a storm', 'on deep sandy soils in summer', 'on ridge tops during light drizzle'], 'Throughflow accumulates downslope, so footslopes saturate first. [1]'),
        ('Which of the following is the slowest transfer?', 'Groundwater flow', ['Overland flow', 'Channel flow', 'Throughflow in macropores (pipeflow)'], '[1]'),
        ('Over-abstraction of groundwater for irrigation is most likely to cause', 'a falling water table and reduced baseflow', ['higher flood peaks', 'more interception', 'increased percolation'], '[1]'),
    ],
    'explain': [
        ('Distinguish between infiltration-excess and saturation-excess overland flow.', 'Infiltration-excess (Hortonian) occurs when rainfall intensity exceeds infiltration capacity, common on bare or compacted ground in intense storms; saturation-excess occurs when the soil is full, even in light rain, commonly on footslopes and valley floors.', '1 mark each definition; 1 mark location/condition [3]'),
        ('Explain the annual pattern of soil moisture in a temperate climate such as the UK.', 'Winter surplus when precipitation exceeds evapotranspiration; spring/summer utilisation as evapotranspiration rises and soil water is used; late summer deficit; autumn recharge as evapotranspiration falls.', '1 mark per stage in order [4]'),
        ('Explain why groundwater abstraction can lead to rivers drying up.', 'Lowering the water table below the river bed reduces or reverses baseflow, so in dry periods there is no supply to the channel.', '1 mark water table; 1 mark baseflow [2]'),
        ('Explain how soil type affects throughflow.', 'Sandy soils with large pores transmit water quickly; clays have small pores and slow throughflow; pipes and macropores (roots, cracks) allow rapid pipeflow.', '1 mark each point [3]'),
    ],
    'claims': [
        ('Groundwater stores can take many years to recover once they are depleted.', True, 'Recharge by percolation is slow; for example, aquifers under the North China Plain and Punjab have fallen for decades.'),
        ('Overland flow is the main route by which water reaches rivers in most humid temperate basins.', False, 'In vegetated humid basins most water reaches rivers by throughflow and groundwater flow; overland flow is local.'),
        ('A soil moisture deficit means the soil is completely dry.', False, 'It means the soil holds less than field capacity; it may still contain water.'),
    ],
    'cs': [
        ('groundwater depletion', [
            ('the Punjab and Haryana aquifers, north-west India', {'causes': 'Free or subsidised electricity for pumps since the Green Revolution; over a million tube wells; rice and wheat double cropping needs heavy irrigation; groundwater use exceeds recharge.',
                                                                    'impacts': 'Water tables falling by about 0.5-1 m a year in many districts; farmers must deepen wells at high cost; reduced baseflow; arsenic and salinity problems; schemes to delay rice transplanting to reduce pumping.'}),
            ('the Ogallala aquifer, Great Plains, USA', {'causes': 'Centre-pivot irrigation for maize and cattle feed across eight states draws water stored over thousands of years; recharge in the semi-arid southern plains is very slow.',
                                                         'impacts': 'Water levels down by more than 30 m in parts of Kansas and Texas; some farms have returned to dryland farming; local conservation districts limit pumping.'}),
        ], [
            ('explain why the groundwater store has been depleted', 'causes', 'Abstraction > recharge; irrigation, pricing, crops, climate.', 'evaluate the effectiveness of attempts to manage groundwater.'),
            ('describe the impacts of falling groundwater levels', 'impacts', 'Water table falls with figures; economic, environmental, river impacts.'),
        ]),
    ],
    'essays': [
        ('groundwater is the most important store in determining river flow',
         ['Baseflow from aquifers maintains discharge in dry periods; chalk rivers such as the Test flow steadily; groundwater stores regulate regimes.'],
         ['In impermeable or urban basins overland flow and throughflow dominate storm response; snow and glacier stores dominate regimes in mountain basins; soil moisture controls storm runoff.'],
         'Groundwater controls low flows and stable regimes in permeable basins, but other stores matter more for storm flows and in impermeable or glacial basins.',
         ['baseflow', 'rock type', 'soil moisture', 'snow and ice']),
    ],
})


@data(c1c)
def c1c_wb(r, D):
    loc = r.choice(['a station in southern England', 'a station in central France', 'a station near Toronto, Canada', 'a station in northern Japan'])
    Pm = [r.randint(45, 95) for _ in range(12)]
    PE = [5, 12, 30, 50, 75, 95, 105, 90, 60, 35, 15, 6]
    PE = [max(0, x + r.randint(-5, 5)) for x in PE]
    diff = [p - e for p, e in zip(Pm, PE)]
    sur = [MON[i] for i in range(12) if diff[i] > 0]
    defi = [MON[i] for i in range(12) if diff[i] < 0]
    if not defi:
        return None
    tp, te = sum(Pm), sum(PE)
    stem = f'Table 1.3 shows mean monthly precipitation (P) and potential evapotranspiration (PE), in mm, for {loc}. ' + ' '.join(f'{MON[i]}: P {Pm[i]}, PE {PE[i]}.' for i in range(12))
    big = min(range(12), key=lambda i: diff[i])
    if D == 1:
        opts, a = mcq(r, MON[big], [MON[(big + k) % 12] for k in (3, 5, 6, 8)])
        return {'stem': stem + ' In which month is the difference P − PE most negative?', 'options': opts, 'answer': a, 'key': f'{MON[big]}: {Pm[big]} − {PE[big]} = {diff[big]} mm. [1]'}
    parts = [
        lambda r: ('Calculate the annual totals of P and PE.', f'P = {tp} mm; PE = {te} mm', f'sum of monthly values [2]'),
        lambda r: ('Identify the months in which there is a water deficit (PE > P).', ', '.join(defi), '1 mark for all correct, 1 mark if one error [2]'),
        lambda r: (f'Calculate the total water surplus over the months when P exceeds PE.', f'{sum(d for d in diff if d > 0)} mm', 'sum of (P − PE) for surplus months [2]'),
        lambda r: ('Describe what happens to soil moisture between April and September.', 'PE rises above P, so plants use stored soil water (utilisation) and a soil moisture deficit develops by late summer.', '1 mark utilisation; 1 mark deficit [2]'),
        lambda r: ('Explain why river discharge is likely to be highest in winter at this station even though monthly precipitation is similar all year.', 'PE is low in winter so more of the precipitation becomes runoff; soils are at field capacity, so infiltration is limited and recharge feeds baseflow.', '1 mark low PE; 1 mark saturated soils/recharge [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[1] = [c1a, c1b, c1c]


# ============================================================== CHAPTER 2: Discharge relationships

def _hydro(r):
    """Synthetic storm hydrograph at 3-hour intervals. Returns times, rain (mm per 3 h), Q (m³/s), tR, L, Q0, Qp."""
    tR = r.choice([3, 6, 9])
    L = r.choice([6, 9, 12, 15, 18, 21, 24])
    Q0 = r.randint(3, 25)
    Qp = Q0 + r.randint(3, 20) * 5
    times = list(range(0, 49, 3))
    rain = [0] * len(times)
    i = times.index(tR)
    rain[i] = r.randint(14, 30)
    rain[i - 1] = r.randint(3, max(4, rain[i] - 4))
    if i + 1 < len(rain):
        rain[i + 1] = r.randint(2, max(3, rain[i] - 6))
    k = 3
    Q = []
    for t in times:
        tau = t - tR
        s = (tau / L) ** k * math.exp(k * (1 - tau / L)) if tau > 0 else 0.0
        Q.append(round(Q0 + (Qp - Q0) * s, 1))
    return times, rain, Q, tR, L, Q0, Qp


c2a = T('Storm hydrographs: components and lag time', 'storm hydrographs components lag time')
B(c2a, {
    'terms': [
        ('storm hydrograph', 'a graph showing how river discharge changes over a short period in response to a rainfall event'),
        ('lag time', 'the time between peak rainfall and peak discharge'),
        ('peak discharge', 'the maximum discharge reached during a storm event'),
        ('rising limb', 'the part of a storm hydrograph showing increasing discharge after rainfall begins'),
        ('falling (recession) limb', 'the part of a storm hydrograph showing the decline of discharge after the peak'),
        ('baseflow', 'the normal day-to-day discharge of a river, supplied mainly by groundwater'),
        ('stormflow (quickflow)', 'the extra discharge produced by a storm, from overland flow and rapid throughflow'),
        ('bankfull discharge', 'the discharge at which the river channel is completely full; above it the river floods'),
    ],
    'mcq': [
        ('On a storm hydrograph, lag time is measured from', 'peak rainfall to peak discharge', ['the start of rainfall to the start of the rising limb', 'peak discharge to the return to baseflow', 'the start of the rising limb to peak discharge'], '[1]'),
        ('River discharge is calculated as', 'cross-sectional area × mean velocity', ['width × depth', 'velocity ÷ cross-sectional area', 'gradient × velocity'], 'Q = A × V, in cumecs (m³/s). [1]'),
        ('Discharge is measured in', 'cumecs (m³/s)', ['metres per second', 'mm per hour', 'cubic metres'], '[1]'),
        ('The recession limb is usually less steep than the rising limb because', 'throughflow and groundwater flow continue to feed the river after the storm', ['rainfall continues to increase', 'evaporation stops after a storm', 'the channel becomes wider'], '[1]'),
    ],
    'explain': [
        ('Explain why the rising limb of a storm hydrograph is usually steeper than the falling limb.', 'Water reaches the river quickly by overland flow and channel precipitation, but afterwards slower throughflow and groundwater flow continue to drain into the river for a long time.', '1 mark quick inputs; 1 mark slow drainage [2]'),
        ('Explain why baseflow rises slightly during and after a storm.', 'Some rainfall percolates to groundwater and raises the water table, increasing groundwater flow to the river a little later.', '1 mark recharge; 1 mark delayed release [2]'),
        ('Describe the characteristics of a “flashy” hydrograph.', 'Short lag time, steep rising limb, high peak discharge and a quick return to baseflow.', '1 mark per feature [3]'),
        ('Explain why river discharge may remain high even after rainfall has stopped.', 'Water stored in soil, on the surface and in channels upstream continues to arrive at the gauging station; travel time from distant parts of the basin; throughflow and groundwater flow are slow.', '1 mark per point [3]'),
    ],
    'claims': [
        ('A short lag time means that there is a lower risk of flooding.', False, 'A short lag time means water arrives quickly and the peak is high, which increases flood risk.'),
        ('Two storms of the same size can produce different hydrographs in the same basin.', True, 'Antecedent soil moisture, frozen ground, storm path and intensity all differ between events.'),
        ('Baseflow is the water that flows over the surface during a storm.', False, 'Baseflow is groundwater-fed flow; surface flow during a storm is part of stormflow.'),
    ],
    'essays': [
        ('the shape of a storm hydrograph depends more on the characteristics of the storm than on the characteristics of the drainage basin',
         ['Rainfall intensity, duration and total; antecedent rainfall; snowmelt or rain on frozen ground; storm movement down the basin; e.g. the 2021 Ahr valley (Germany) flood after over 100 mm in 24 hours.'],
         ['Basin size and shape, slope, rock permeability, soils, drainage density and land use (urbanisation, forest cover) set lag time and peak; the same storm gives very different hydrographs in permeable chalk and impermeable clay basins.'],
         'Storm characteristics trigger each event and explain differences between storms in one basin, but basin characteristics explain the consistent differences between basins.',
         ['rainfall intensity', 'antecedent conditions', 'rock type', 'urbanisation']),
    ],
})


@data(c2a)
def c2a_hydro(r, D):
    times, rain, Q, tR, L, Q0, Qp = _hydro(r)
    nm = r.choice(BASINS)
    sel = [i for i in range(len(times)) if times[i] <= 45]
    stem = (f'Fig. 2.1 is a storm hydrograph for the {nm} at a gauging station. Rainfall (mm in each 3-hour period ending at the time shown) and discharge (m³/s) are: '
            + '; '.join(f'hour {times[i]}: rain {rain[i]}, discharge {fmt(Q[i], 1)}' for i in sel) + '.')
    tQ = tR + L
    rise = pct_change(Q0, Qp)
    if D == 1:
        opts, a = mcq(r, f'{L} hours', [f'{L + 3} hours', f'{tQ} hours', f'{max(3, L - 3)} hours', f'{L + 6} hours'])
        return {'stem': stem + ' What is the lag time?', 'options': opts, 'answer': a, 'key': f'peak rainfall at hour {tR}, peak discharge at hour {tQ}: lag = {L} h. [1]'}
    tot = sum(rain)
    parts = [
        lambda r: ('State the peak discharge and the time at which it occurred.', f'{fmt(Qp, 1)} m³/s at hour {tQ}', '1 mark value; 1 mark time [2]'),
        lambda r: ('Calculate the lag time.', f'{L} hours', f'peak rainfall hour {tR}; peak discharge hour {tQ}; {tQ} − {tR} = {L} h [2]'),
        lambda r: ('Calculate the total rainfall in the storm.', f'{tot} mm', ' + '.join(str(x) for x in rain if x) + f' = {tot} mm [1]'),
        lambda r: ('Calculate the percentage increase from baseflow to peak discharge.', f'{dp(rise)}%', f'({fmt(Qp, 1)} − {fmt(Q0, 1)}) ÷ {fmt(Q0, 1)} × 100 = {dp(rise)}% [2]'),
        lambda r: ('Suggest two characteristics of the drainage basin that could explain this lag time.', ('A short lag suggests: impermeable rock or saturated soil, steep slopes, high drainage density, urban surfaces, small circular basin.' if L <= 12 else 'A long lag suggests: permeable rock, forest cover, gentle slopes, low drainage density, a large or elongated basin.'), '1 mark each, linked to lag [2]'),
        lambda r: ('Explain why discharge was still above baseflow at the end of the record.', 'Throughflow and groundwater flow continue to drain stored water slowly into the channel (recession limb).', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@data(c2a)
def c2a_qav(r, D):
    w = r.randint(4, 30)
    depths = [round(r.uniform(0.2, 1.6), 2) for _ in range(5)]
    depths[0] = round(depths[0] * 0.4, 2) or 0.1
    depths[-1] = round(depths[-1] * 0.4, 2) or 0.1
    md = mean(depths)
    A = w * md
    d = r.choice([10, 20])
    tf = round(r.uniform(6, 40), 1)
    vs = d / tf
    vm = vs * 0.8
    Q = A * vm
    stem = (f'At a site on a river in {city(r)}’s region, students measured a channel width of {w} m and five equally spaced depths (m): ' + ', '.join(fmt(x, 2) for x in depths)
            + f'. A float took a mean of {fmt(tf, 1)} s to travel {d} m.')
    if D == 1:
        opts, a = mcq(r, f'{dp(A, 2)} m²', [f'{dp(w * max(depths), 2)} m²', f'{dp(w + md, 2)} m²', f'{dp(md, 2)} m²', f'{dp(A * 2, 2)} m²'])
        return {'stem': stem + ' What is the cross-sectional area (width × mean depth)?', 'options': opts, 'answer': a, 'key': f'{w} × {dp(md, 3)} = {dp(A, 2)} m². [1]'}
    parts = [
        lambda r: ('Calculate the cross-sectional area of the channel (width × mean depth).', f'{dp(A, 2)} m²', f'mean depth = {dp(md, 3)} m; {w} × {dp(md, 3)} = {dp(A, 2)} m² [2]'),
        lambda r: ('Calculate the surface velocity and the mean velocity, using a correction factor of 0.8.', f'{dp(vs, 2)} m/s; {dp(vm, 2)} m/s', f'{d} ÷ {fmt(tf, 1)} = {dp(vs, 2)}; × 0.8 = {dp(vm, 2)} m/s [2]'),
        lambda r: ('Calculate the discharge.', f'{dp(Q, 2)} m³/s', f'Q = A × V = {dp(A, 2)} × {dp(vm, 2)} = {dp(Q, 2)} m³/s [2]'),
        lambda r: ('Explain why the surface velocity of a float is multiplied by a correction factor.', 'Friction with the bed and banks slows water near them, so mean velocity in the cross-section is lower than surface velocity in mid-channel.', '[2]'),
        lambda r: ('Suggest two ways of improving the accuracy of the velocity measurement.', 'Repeat float timings and average; use a flow meter at several depths and points across the channel; avoid windy conditions; use a longer measured distance.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 2.2 influences on hydrograph shape
c2b = T('Physical and human influences on hydrograph shape', 'influences on hydrograph shape')
B(c2b, {
    'terms': [
        ('drainage density', 'the total length of streams in a basin divided by the basin area, in km per km²'),
        ('antecedent moisture', 'the amount of water already in the soil before a storm begins'),
        ('impermeable surface', 'a surface, such as tarmac, concrete or clay, through which water cannot pass'),
        ('urbanisation (hydrological effect)', 'the replacement of vegetation and soil by buildings and roads, increasing runoff and reducing lag time'),
        ('basin shape', 'the outline of a basin; circular basins give higher peaks than elongated ones because tributary flows arrive together'),
        ('afforestation', 'planting trees on land that was not previously forested, which increases interception and lag time'),
    ],
    'mcq': [
        ('Which change would shorten lag time in a drainage basin?', 'Building a housing estate with storm drains', ['Planting a forest', 'Building a reservoir upstream', 'Restoring a wetland on the floodplain'], '[1]'),
        ('A basin with a high drainage density usually has', 'impermeable rock and a short lag time', ['permeable rock and a long lag time', 'little surface runoff', 'a low peak discharge'], '[1]'),
        ('Which of the following basins would be expected to have the flashiest hydrograph?', 'A small, steep, circular basin on granite', ['A large, gently sloping basin on chalk', 'An elongated forested basin', 'A basin with many lakes'], '[1]'),
        ('Heavy rain on frozen ground produces a high peak discharge mainly because', 'infiltration is prevented, so most water becomes overland flow', ['evaporation is very high', 'interception increases', 'groundwater flow increases'], '[1]'),
    ],
    'explain': [
        ('Explain how urbanisation affects the shape of a storm hydrograph.', 'Impermeable surfaces reduce infiltration; drains and gutters carry water rapidly to rivers; less vegetation so less interception and evapotranspiration; channelised rivers; result: shorter lag, higher and steeper peak.', '1 mark per developed point [4]'),
        ('Explain how rock type influences the storm hydrograph.', 'Permeable rocks (chalk, sandstone) allow percolation, so more water travels slowly as groundwater: long lag, low peak; impermeable rocks (granite, clay) cause overland flow: short lag, high peak.', '1 mark each rock type with effect [3]'),
        ('Explain why a basin’s shape affects peak discharge.', 'In a circular basin water from all parts has a similar distance to travel and arrives at the outlet at about the same time, giving a high peak; in an elongated basin arrival is spread out.', '[2]'),
        ('Explain how afforestation could change the hydrograph of an upland basin.', 'More interception and evapotranspiration; roots and litter increase infiltration; less overland flow; longer lag, lower peak; but drainage ditches during planting can initially increase runoff.', '1 mark per point [3]'),
    ],
    'claims': [
        ('Large drainage basins usually have shorter lag times than small ones.', False, 'Water has further to travel in large basins, so lag times are usually longer.'),
        ('Reservoirs can reduce flood peaks downstream.', True, 'They store storm water and release it slowly, as on the Yangtze below the Three Gorges Dam.'),
        ('Steep slopes reduce the amount of infiltration.', True, 'Water moves downslope more quickly, so there is less time to infiltrate and more overland flow.'),
    ],
    'cases': [
        (['Fig. 2.2 shows storm hydrographs for two neighbouring basins after the same storm. Basin X (mainly forest on sandstone) had a lag time of 20 hours and a peak of 35 m³/s. Basin Y (40% urban, on clay) had a lag time of 6 hours and a peak of 95 m³/s.',
          'Two basins of similar size received the same 45 mm storm. In Basin X, on forested sandstone, discharge peaked 20 hours after peak rainfall at 35 m³/s; in Basin Y, a partly urbanised clay basin, discharge peaked after 6 hours at 95 m³/s.'],
         [('Compare the two hydrographs.', 'Y has a lag time 14 hours shorter and a peak 60 m³/s (about 2.7 times) higher than X; Y is flashier with a steeper rising limb.', '1 mark lag; 1 mark peak; 1 mark use of data [3]'),
          ('Explain the differences between the two basins’ responses.', 'Y: impermeable clay and urban surfaces, storm drains, little interception, so rapid overland flow. X: interception by trees, high infiltration and percolation into permeable sandstone, so slow throughflow and groundwater flow.', '1 mark per developed contrast [4]'),
          ('Suggest which basin would be more likely to flood and why.', 'Basin Y: higher peak reached quickly, giving less warning and more chance of exceeding bankfull discharge.', '1 mark choice; 1 mark reason [2]'),
          ('Suggest two ways the flood risk in Basin Y could be reduced.', 'Sustainable urban drainage (permeable paving, green roofs, retention ponds); planting trees upstream; flood storage areas; channel improvements.', '1 mark each [2]')]),
    ],
    'essays': [
        ('human activities now have more influence on flood hydrographs than physical factors',
         ['Urbanisation (e.g. Houston, where impervious surfaces made the 2017 Hurricane Harvey floods worse); deforestation in the Himalaya; field drainage; channelisation speeding flows downstream.'],
         ['Physical factors such as storm intensity, basin size, rock and slope still control most hydrographs; extreme rainfall can overwhelm any land use; reservoirs and afforestation can reduce peaks, so human influence is not only negative.'],
         'In urban and heavily modified basins human activity dominates, but in most basins physical factors remain more important, and human influence can lower as well as raise flood peaks.',
         ['urbanisation', 'deforestation', 'reservoirs', 'rainfall intensity']),
    ],
})


@data(c2b)
def c2b_dd(r, D):
    a1, a2 = r.randint(20, 120), r.randint(20, 120)
    l1 = round(a1 * r.uniform(0.6, 1.4), 1)
    l2 = round(a2 * r.uniform(1.6, 3.2), 1)
    if r.random() < 0.5:
        a1, a2, l1, l2 = a2, a1, l2, l1
    d1, d2 = l1 / a1, l2 / a2
    hi = 'Basin P' if d1 > d2 else 'Basin Q'
    stem = f'Table 2.2 gives data for two drainage basins. Basin P: area {a1} km², total stream length {fmt(l1, 1)} km. Basin Q: area {a2} km², total stream length {fmt(l2, 1)} km.'
    if D == 1:
        opts, a = mcq(r, f'{dp(d1, 2)} km/km²', [f'{dp(a1 / l1, 2)} km/km²', f'{dp(l1 * a1, 0)} km/km²', f'{dp(d2, 2)} km/km²' if abs(d1 - d2) > 0.02 else f'{dp(d1 + 0.5, 2)} km/km²', f'{dp(d1 * 2, 2)} km/km²'])
        return {'stem': stem + ' What is the drainage density of Basin P?', 'options': opts, 'answer': a, 'key': f'{fmt(l1, 1)} ÷ {a1} = {dp(d1, 2)} km/km². [1]'}
    parts = [
        lambda r: ('Calculate the drainage density of each basin.', f'P {dp(d1, 2)} km/km²; Q {dp(d2, 2)} km/km²', f'total stream length ÷ area: {fmt(l1, 1)} ÷ {a1}; {fmt(l2, 1)} ÷ {a2} [2]'),
        lambda r: ('Suggest which basin is more likely to be underlain by impermeable rock. Give a reason.', f'{hi}: the higher drainage density shows more surface streams because water cannot sink into the rock.', '1 mark basin; 1 mark reason [2]'),
        lambda r: (f'Explain how the hydrograph of {hi} is likely to differ from that of the other basin.', 'Shorter lag time and higher, steeper peak because water reaches a channel quickly; streams are close together so overland flow distances are short.', '1 mark lag; 1 mark peak; 1 mark explanation [3]'),
        lambda r: ('Suggest one other basin characteristic that should be compared before drawing conclusions about flood risk.', 'Slope angle, land use and vegetation cover, basin shape, soil type, urbanisation.', '1 mark characteristic; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 2.3 river regimes
c2c = T('River regimes and annual discharge patterns', 'river regimes annual discharge')
REGIMES = {
    'nival/glacial (snow and ice melt)': ([10, 9, 12, 25, 70, 100, 95, 75, 40, 20, 14, 11], 'Discharge is low in winter when precipitation is stored as snow and ice and peaks in early summer when snow and glaciers melt (e.g. the Rhône at Geneva or the Indus).'),
    'monsoonal': ([10, 8, 7, 8, 15, 45, 85, 100, 75, 35, 18, 12], 'Most rain falls during the summer monsoon (June-September) as the ITCZ moves north and moist south-west winds blow onshore, so discharge peaks in August (e.g. the Ganges or Mekong).'),
    'temperate oceanic (pluvial)': ([100, 95, 80, 60, 45, 35, 30, 32, 40, 60, 80, 95], 'Rainfall is spread through the year but evapotranspiration is high in summer and low in winter, so discharge peaks in winter (e.g. the Thames or Severn).'),
    'Mediterranean': ([100, 95, 75, 50, 25, 10, 4, 3, 8, 30, 70, 90], 'Rain falls mainly in the mild winter; summers are hot and dry with high evaporation, so flow is very low or the river dries up in summer (e.g. rivers in southern Spain).'),
    'equatorial': ([90, 92, 98, 100, 95, 85, 78, 75, 80, 88, 92, 90], 'Heavy convectional rain throughout the year gives high discharge in all months, with small peaks after the two rainy seasons (e.g. the Congo).'),
}
B(c2c, {
    'terms': [
        ('river regime', 'the annual variation in the discharge of a river'),
        ('simple regime', 'a regime with one period of high discharge and one of low discharge each year'),
        ('complex regime', 'a regime with more than one peak in the year, often in large rivers fed by tributaries with different climates'),
        ('nival regime', 'a regime dominated by snowmelt, with peak discharge in spring or early summer'),
        ('ephemeral river', 'a river that flows only after heavy rain, as in arid areas'),
        ('perennial river', 'a river that flows all year round'),
    ],
    'mcq': [
        ('A river with low discharge in winter and peak discharge in June is most likely fed by', 'snow and glacial meltwater', ['the summer monsoon', 'winter cyclonic rain', 'equatorial convectional rain'], '[1]'),
        ('The Nile at Cairo historically had a peak discharge in', 'August-September, from monsoon rain over the Ethiopian Highlands', ['January, from local winter rain', 'April, from snowmelt in the Alps', 'December, from the Mediterranean'], 'The Blue Nile supplies most of the flood. [1]'),
        ('Which factor best explains the low summer discharge of temperate oceanic rivers despite summer rainfall?', 'High evapotranspiration in summer', ['Frozen ground', 'Snow storage', 'Low temperatures'], '[1]'),
        ('Dams such as the Aswan High Dam change river regimes by', 'storing flood water and releasing more even flow through the year', ['increasing the annual flood peak', 'stopping evaporation', 'raising groundwater only'], '[1]'),
    ],
    'explain': [
        ('Explain why large rivers such as the Mississippi often have complex regimes.', 'Tributaries drain areas with different climates and relief (snowmelt from the Rockies, spring rain in the Ohio basin), so peaks arrive at different times.', '1 mark tributaries; 1 mark different climates; 1 mark example [3]'),
        ('Explain how climate influences river regimes.', 'The seasonal pattern of precipitation, whether it falls as snow, and seasonal evapotranspiration all control when water reaches the river.', '1 mark each [3]'),
        ('Explain how human activity can modify a river regime.', 'Dams and reservoirs even out flows; abstraction for irrigation lowers flows; urbanisation adds quickflow; inter-basin transfers add water.', '1 mark per activity explained [3]'),
    ],
    'claims': [
        ('A river regime and a storm hydrograph show the same thing.', False, 'A regime shows the annual pattern of discharge; a storm hydrograph shows the response to a single rainfall event over hours or days.'),
        ('Rock type can influence a river’s regime.', True, 'Permeable aquifers store water and release baseflow, giving a more even regime.'),
        ('Climate change may alter the regimes of glacier-fed rivers.', True, 'Glacier melt initially raises summer flows, but as glaciers shrink summer flows fall (e.g. rivers draining the Andes and Himalaya).'),
    ],
    'essays': [
        ('climate is the only important influence on river regimes',
         ['Seasonal rainfall, snowmelt and evapotranspiration explain most regimes (monsoonal Ganges, nival Rhône, Mediterranean rivers).'],
         ['Basin geology (aquifers smooth regimes), lakes and wetlands, basin size and tributaries, and human activity (dams such as Aswan, irrigation abstraction from the Colorado) also matter.'],
         'Climate is the dominant control, but geology, basin size and especially human regulation strongly modify regimes.',
         ['snowmelt', 'geology', 'dams', 'abstraction']),
    ],
})


@data(c2c)
def c2c_regime(r, D):
    kind = r.choice(list(REGIMES))
    shape, why = REGIMES[kind]
    scale = r.choice([20, 50, 120, 400, 1500])
    Q = [max(1, round(s * scale / 100 * r.uniform(0.92, 1.08))) for s in shape]
    nm = r.choice(['River K', 'River L', 'River M', 'River N'])
    stem = f'Table 2.3 shows mean monthly discharge (m³/s) of {nm}. ' + ', '.join(f'{MON[i]} {nf(Q[i])}' for i in range(12)) + '.'
    hi, lo = max(Q), min(Q)
    mi, mj = MON[Q.index(hi)], MON[Q.index(lo)]
    ratio = hi / lo
    others = [k for k in REGIMES if k != kind]
    if D == 1:
        opts, a = mcq(r, cap(kind), [cap(k) for k in others])
        return {'stem': stem + ' Which type of regime does this river most probably have?', 'options': opts, 'answer': a, 'key': why + ' [1]'}
    parts = [
        lambda r: ('Identify the months of highest and lowest discharge.', f'highest {mi} ({nf(hi)} m³/s); lowest {mj} ({nf(lo)} m³/s)', '1 mark each [2]'),
        lambda r: ('Calculate the ratio of maximum to minimum monthly discharge.', f'{dp(ratio)} : 1', f'{nf(hi)} ÷ {nf(lo)} = {dp(ratio)} [1]'),
        lambda r: ('Calculate the mean monthly discharge.', f'{dp(mean(Q))} m³/s', f'sum {nf(sum(Q))} ÷ 12 = {dp(mean(Q))} [2]'),
        lambda r: ('Suggest the type of regime and explain the pattern shown.', f'{cap(kind)}. {why}', '1 mark type; 2 marks explanation [3]'),
        lambda r: ('Suggest one problem the pattern of discharge creates for people living in the basin and one possible solution.', 'Seasonal floods or seasonal water shortages; solutions include reservoirs to store high flows for the dry season, flood embankments or water transfer.', '1 mark problem; 1 mark solution [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[2] = [c2a, c2b, c2c]


# ============================================================== CHAPTER 3: River channel processes, landforms and human impact

c3a = T('Channel processes: erosion, transportation, deposition and the Hjulström curve', 'channel processes erosion transportation deposition hjulström curve')
B(c3a, {
    'terms': [
        ('abrasion (corrasion)', 'erosion of the bed and banks by material carried by the river scraping and grinding against them'),
        ('hydraulic action', 'erosion caused by the force of moving water, including the compression of air in cracks and cavitation'),
        ('solution (corrosion)', 'the chemical dissolving of rocks such as limestone by slightly acidic river water'),
        ('attrition', 'the wearing down of load particles as they collide with each other, becoming smaller and rounder'),
        ('saltation', 'the bouncing of medium-sized particles such as sand and small pebbles along the river bed'),
        ('traction', 'the rolling and sliding of the largest particles along the river bed'),
        ('suspension', 'the transport of fine particles such as clay and silt held up within the flow by turbulence'),
        ('critical erosion velocity', 'the minimum velocity needed to pick up (entrain) particles of a given size'),
        ('competence', 'the size of the largest particle a river can carry at a given velocity'),
        ('capacity', 'the total load a river can carry at a given discharge'),
    ],
    'mcq': [
        ('On the Hjulström curve, which particles need the lowest velocity to be entrained?', 'Sand (about 0.1-1 mm)', ['Clay', 'Pebbles', 'Boulders'], 'Clay particles are cohesive and lie in the smooth bed layer, so they need a higher velocity. [1]'),
        ('Clay remains in suspension at very low velocities because', 'its settling velocity is extremely low', ['it is cohesive', 'it is dissolved', 'it is moved by traction'], '[1]'),
        ('Cavitation is a form of', 'hydraulic action', ['abrasion', 'attrition', 'solution'], 'Collapsing air bubbles in turbulent water. [1]'),
        ('Which process makes river load smaller and more rounded downstream?', 'Attrition', ['Solution', 'Traction', 'Flocculation'], '[1]'),
        ('Deposition occurs when', 'velocity falls below the settling velocity of the particles', ['velocity rises above the critical erosion velocity', 'discharge increases during a flood', 'gradient increases'], '[1]'),
    ],
    'explain': [
        ('Explain why clay particles need a higher velocity to be entrained than sand particles.', 'Clay particles are cohesive (stick together by electrostatic forces) and lie within the smooth laminar layer near the bed, so a high velocity is needed to lift them.', '1 mark cohesion; 1 mark bed roughness/laminar layer [2]'),
        ('Explain the difference between competence and capacity.', 'Competence is the largest particle size that can be moved at a given velocity; capacity is the total quantity of load that can be carried at a given discharge.', '1 mark each [2]'),
        ('Explain why rivers carry most of their load during floods.', 'Velocity and discharge increase, so competence and capacity rise sharply; more energy for erosion; banks are eroded; more sediment enters from slopes.', '1 mark per point [3]'),
        ('Describe the conditions in which deposition occurs in a river.', 'When velocity falls: on the inside of meanders, where the river enters a lake or the sea, when discharge falls after a flood, where the gradient decreases, or when load increases suddenly.', '1 mark each condition [3]'),
    ],
    'claims': [
        ('Velocity is the same throughout the cross-section of a river.', False, 'It is fastest just below the surface in mid-channel (thalweg) and slowest near the bed and banks because of friction.'),
        ('Once particles are entrained, they can be carried at velocities lower than those needed to pick them up.', True, 'The transport field on the Hjulström curve lies between the settling and erosion velocity curves.'),
        ('The dissolved load can be seen in the river.', False, 'Solution load is chemically dissolved and invisible.'),
    ],
    'essays': [
        ('velocity is the most important factor influencing erosion, transport and deposition in a river channel',
         ['Hjulström curve: entrainment, transport and settling depend on velocity; floods do most work; deposition when velocity falls on meander insides and at river mouths.'],
         ['Discharge and channel shape (hydraulic radius) control efficiency; load supply, particle size and cohesion, bedrock type, gradient and human activity (dams trapping sediment) also matter.'],
         'Velocity is the immediate control, but it is itself controlled by discharge, gradient and channel efficiency, and load supply limits what is actually moved.',
         ['the Hjulström curve', 'discharge', 'load', 'channel shape']),
    ],
})

# approximate values read from the Hjulström curve (cm/s)
HJUL = [('clay', 0.002, 120, 0.0003), ('fine silt', 0.01, 60, 0.008), ('fine sand', 0.1, 25, 0.8), ('coarse sand', 1, 30, 9),
        ('granules', 3, 60, 20), ('pebbles', 20, 150, 90), ('cobbles', 100, 330, 200)]


@data(c3a)
def c3a_hjul(r, D):
    rows = r.sample(HJUL, 4)
    rows.sort(key=lambda x: x[1])
    v = r.choice([0.5, 2, 5, 15, 40, 80, 100, 250, 400])
    stem = ('Table 3.1 gives values read from the Hjulström curve for four particle sizes: ' + ' '.join(f'{cap(n)} ({fmt(s, 3)} mm): critical erosion velocity {e} cm/s, settling velocity {fmt(st, 4)} cm/s.' for n, s, e, st in rows)
            + f' The mean velocity of a river is {fmt(v, 1)} cm/s.')

    def fate(e, st):
        return 'eroded (entrained) and transported' if v >= e else 'transported if already moving, but not picked up from the bed' if v >= st else 'deposited'
    res = [(n, fate(e, st)) for n, s, e, st in rows]
    n0, f0 = res[r.randrange(4)]
    if D == 1:
        opts, a = mcq(r, cap(f0), [cap(x) for x in ['eroded (entrained) and transported', 'transported if already moving, but not picked up from the bed', 'deposited', 'dissolved in solution'] if x != f0])
        return {'stem': stem + f' What happens to {n0} at this velocity?', 'options': opts, 'answer': a, 'key': f'Compare {fmt(v, 1)} cm/s with the erosion and settling velocities for {n0}. [1]'}
    parts = [
        lambda r: ('For each particle size, state whether it would be eroded, transported or deposited at this velocity.', '; '.join(f'{n}: {f}' for n, f in res), '1 mark for two correct, 2 marks all correct [2]'),
        lambda r: ('Explain why the critical erosion velocity for clay is higher than for sand.', 'Clay is cohesive and its particles lie in the laminar layer close to a smooth bed, so more energy is needed to lift them.', '[2]'),
        lambda r: ('Explain why fine particles may be carried in suspension for long distances.', 'Their settling velocity is very low, so even slow, turbulent flow keeps them suspended.', '[2]'),
        lambda r: ('Suggest how the river’s load would change if velocity fell to 1 cm/s.', 'Most sand and all coarser particles would be deposited; only silt and clay would stay in suspension (plus the dissolved load).', '1 mark deposition of coarse; 1 mark fines remain [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


add_spearman(c3a, [
    {'intro': 'Students tested the hypothesis that the mean size of bed load decreases with distance downstream. They measured the long axis of 20 pebbles at each of {n} sites along a river in northern Spain.', 'label': 'Site',
     'x': ('distance downstream from the source (km)', 1, 40, 1), 'y': ('mean pebble long axis (mm)', 12, 140, 0), 'sign': -1,
     'why': 'Attrition and abrasion reduce particle size as load is carried downstream; competence falls on lower gradients, so large particles are left upstream (sorting).',
     'limit': 'Sampling may be biased towards larger, easily picked pebbles; use random sampling (e.g. a quadrat grid) and more pebbles per site; tributaries may add coarse load.'},
    {'intro': 'A student measured roundness of bed load (Cailleux roundness index) at {n} sites downstream on a river in the Lake District, UK.', 'label': 'Site',
     'x': ('distance downstream (km)', 0.5, 25, 1), 'y': ('mean roundness index', 150, 650, 0), 'sign': 1,
     'why': 'Attrition and abrasion knock off edges as particles collide and are moved downstream, so particles become rounder with distance travelled.',
     'limit': 'Roundness judged visually or by measurement is subjective; use the same operator and a Powers chart or measuring frame; tributaries and bank collapse add angular material.'},
])


# --------------------------------------------------------------- 3.2 channel types, velocity, long profiles
c3b = T('Channel types, velocity and long profiles', 'channel types velocity long profiles')
B(c3b, {
    'terms': [
        ('hydraulic radius', 'the cross-sectional area of a channel divided by its wetted perimeter; a measure of channel efficiency'),
        ('wetted perimeter', 'the total length of the bed and banks in contact with the water in a cross-section'),
        ('long profile', 'the gradient of a river from its source to its mouth, usually concave in shape'),
        ('thalweg', 'the line of fastest flow (and deepest water) along a river channel'),
        ('base level', 'the lowest level to which a river can erode, normally sea level'),
        ('knickpoint', 'a sudden break of slope on a long profile, often where a waterfall or rapids occur, sometimes caused by rejuvenation'),
        ('turbulent flow', 'irregular, swirling flow with eddies that lifts sediment from the bed'),
        ('laminar flow', 'smooth flow in parallel layers, which is rare in natural rivers except near the bed'),
        ('channel roughness', 'the friction caused by the bed and banks, for example boulders and vegetation, often expressed as Manning’s n'),
    ],
    'mcq': [
        ('A channel with a high hydraulic radius is', 'efficient, because less water is in contact with the bed and banks', ['inefficient, with high friction', 'always shallow and wide', 'only found in mountain streams'], '[1]'),
        ('Mean velocity usually increases downstream because', 'channel efficiency increases and roughness decreases', ['the gradient increases', 'the load becomes coarser', 'discharge decreases'], 'Despite gentler gradients, deeper smoother channels lose less energy to friction. [1]'),
        ('A concave long profile results from', 'erosion being greatest in the steep upper course and the river adjusting towards base level', ['deposition in the upper course', 'uplift of the mouth', 'rock type being the same everywhere'], '[1]'),
        ('Which channel is most efficient for the same cross-sectional area?', 'A semicircular channel', ['A wide, shallow channel', 'A narrow, deep rectangular channel', 'A braided channel'], '[1]'),
    ],
    'explain': [
        ('Explain why rivers often flow faster in their lower course than in upland streams.', 'Upland channels are rough, shallow and boulder-strewn with a low hydraulic radius, so much energy is lost to friction; lower channels are deeper, smoother and more efficient with greater discharge.', '1 mark roughness; 1 mark hydraulic radius; 1 mark discharge [3]'),
        ('Explain the formation of a knickpoint on a long profile.', 'A fall in base level (sea-level fall or uplift) rejuvenates the river, which cuts down from the mouth; a break of slope marks the junction between the old and new profiles and migrates upstream; also hard rock bands.', '1 mark cause; 1 mark downcutting; 1 mark migration [3]'),
        ('Describe how channel shape changes downstream.', 'Width, depth and cross-sectional area increase; hydraulic radius increases; channels become smoother and more efficient; gradient decreases.', '1 mark each [3]'),
    ],
    'claims': [
        ('Rivers always flow fastest where the gradient is steepest.', False, 'Steep upland streams are often slower than lowland rivers because roughness and low hydraulic radius cause friction losses.'),
        ('A river can have more than one channel at the same point.', True, 'Braided channels divide around bars of sediment.'),
        ('The long profile of a river never changes.', False, 'Rejuvenation, rock type, dams and tectonic uplift alter it over time.'),
    ],
    'essays': [
        ('channel efficiency is more important than gradient in explaining river velocity',
         ['Hydraulic radius and roughness control friction losses; lowland rivers such as the Amazon flow quickly on very low gradients.'],
         ['Gradient provides the potential energy; steep mountain torrents can flow fast in floods; discharge, load and bedrock also influence velocity.'],
         'Over the length of most rivers efficiency and discharge outweigh the fall in gradient, so velocity tends to rise downstream, but locally gradient can dominate.',
         ['hydraulic radius', 'roughness', 'gradient', 'discharge']),
    ],
})


@data(c3b)
def c3b_hr(r, D):
    sites = []
    for nm in ('Site 1 (upper course)', 'Site 2 (lower course)'):
        up = nm.startswith('Site 1')
        w = round(r.uniform(2, 6) if up else r.uniform(10, 30), 1)
        d = round(r.uniform(0.15, 0.45) if up else r.uniform(0.8, 2.5), 2)
        sites.append((nm, w, d))
    rows = []
    for nm, w, d in sites:
        A = w * d
        P = w + 2 * d
        rows.append((nm, w, d, A, P, A / P))
    stem = 'Table 3.2 gives channel measurements at two sites on the same river (assume rectangular cross-sections). ' + ' '.join(f'{nm}: width {fmt(w, 1)} m, mean depth {fmt(d, 2)} m.' for nm, w, d, *_ in rows)
    a, b = rows
    if D == 1:
        opts, ans = mcq(r, dp(b[5], 2), [dp(b[3], 2), dp(b[4], 2), dp(b[4] / b[3], 2), dp(b[3] / b[1], 2) if abs(b[3] / b[1] - b[5]) > 0.01 else dp(b[5] * 2, 2)])
        return {'stem': stem + ' What is the hydraulic radius (m) at Site 2?', 'options': opts, 'answer': ans, 'key': f'A = {dp(b[3], 2)} m², P = {fmt(b[1], 1)} + 2 × {fmt(b[2], 2)} = {dp(b[4], 2)} m; R = {dp(b[5], 2)} m. [1]'}
    parts = [
        lambda r: ('Calculate the cross-sectional area at each site.', f'Site 1 {dp(a[3], 2)} m²; Site 2 {dp(b[3], 2)} m²', 'width × depth [2]'),
        lambda r: ('Calculate the wetted perimeter and the hydraulic radius at each site.', f'Site 1: P = {dp(a[4], 2)} m, R = {dp(a[5], 3)} m; Site 2: P = {dp(b[4], 2)} m, R = {dp(b[5], 3)} m', 'P = width + 2 × depth; R = A ÷ P; 1 mark each site [2]'),
        lambda r: ('Using the hydraulic radius (cross-sectional area ÷ wetted perimeter) at each site, explain why velocity is likely to be higher at Site 2.', f'Hydraulic radius is higher at Site 2 ({dp(b[5], 3)} v {dp(a[5], 3)} m), so a smaller proportion of the water is in contact with the bed and banks, less energy is lost to friction and flow is more efficient.', '1 mark data; 1 mark friction; 1 mark efficiency [3]'),
        lambda r: ('Suggest one other factor, apart from channel shape, that affects velocity.', 'Bed roughness (boulders, vegetation) / gradient / discharge.', '1 mark factor; 1 mark explanation [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@data(c3b)
def c3b_grad(r, D):
    pts = sorted(r.sample(range(2, 60), 3))
    h0 = r.randint(400, 900)
    hs = [h0]
    for _ in range(3):
        hs.append(hs[-1] - r.randint(30, 200))
    if hs[-1] < 0:
        return None
    ds = [0] + pts
    seg = [((hs[i] - hs[i + 1]) / ((ds[i + 1] - ds[i]) * 1000)) for i in range(3)]
    stem = 'A long profile of a river shows the following heights above sea level: ' + ', '.join(f'{d} km from the source: {h} m' for d, h in zip(ds, hs)) + '.'
    i = r.randrange(3)
    g = seg[i]
    if D == 1:
        opts, a = mcq(r, f'1 in {round(1 / g)}', [f'1 in {round(1 / g / 10)}', f'1 in {round(1 / g * 10)}', f'1 in {round((ds[i + 1] - ds[i]) * 1000 / hs[i])}', f'1 in {round(1 / g) + 50}'])
        return {'stem': stem + f' What is the average gradient between {ds[i]} km and {ds[i + 1]} km?', 'options': opts, 'answer': a,
                'key': f'fall {hs[i] - hs[i + 1]} m over {(ds[i + 1] - ds[i]) * 1000} m = 1 in {round(1 / g)}. [1]'}
    steep = max(range(3), key=lambda j: seg[j])
    parts = [
        lambda r: (f'Calculate the average gradient between {ds[i]} km and {ds[i + 1]} km, as a ratio 1 in x.', f'1 in {round(1 / g)}', f'vertical fall {hs[i] - hs[i + 1]} m ÷ horizontal distance {(ds[i + 1] - ds[i]) * 1000} m [2]'),
        lambda r: ('Identify the steepest section of the profile.', f'{ds[steep]}-{ds[steep + 1]} km (1 in {round(1 / seg[steep])})', '[1]'),
        lambda r: ('Describe the shape of a typical graded long profile and explain why it develops.', 'Smooth and concave: steep near the source where vertical erosion dominates, gentle near the mouth; the river erodes towards base level and adjusts so that it can just carry its load (graded).', '1 mark shape; 2 marks explanation [3]'),
        lambda r: ('Suggest two reasons why a real profile may not be smooth.', 'Bands of resistant rock forming waterfalls or rapids; lakes; rejuvenation knickpoints; tributary deposition; dams.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 3.3 landforms
c3c = T('River landforms: meanders, braiding, floodplains, levees and deltas', 'river landforms meanders braiding floodplains levees deltas')
B(c3c, {
    'terms': [
        ('meander', 'a sinuous bend in a river channel, with a river cliff on the outer bank and a point bar on the inner bank'),
        ('point bar', 'a deposit of sand and gravel on the inside of a meander bend, where velocity is low'),
        ('helicoidal flow', 'the corkscrew-like flow in a meander that moves water across the channel from the outer to the inner bank along the bed'),
        ('riffle', 'a shallow section of a channel with coarse deposits and fast, turbulent flow'),
        ('pool', 'a deep section of a channel, often on the outside of a meander bend'),
        ('braided channel', 'a channel divided into several threads separated by bars and islands of sediment'),
        ('levee', 'a raised bank of coarse sediment alongside a river channel, built up during floods'),
        ('oxbow lake', 'a crescent-shaped lake formed when a meander neck is cut through and the old loop is abandoned'),
        ('delta', 'a landform built of sediment deposited where a river enters a sea or lake faster than it can be removed'),
        ('sinuosity', 'the ratio of the actual channel length to the straight-line distance between two points'),
    ],
    'mcq': [
        ('Braiding is most likely where', 'discharge is variable and the river carries a large coarse load, as in glacial outwash', ['the channel has a high hydraulic radius and fine load', 'velocity is constant all year', 'the river flows over bare bedrock'], '[1]'),
        ('The Mississippi delta is described as', 'bird’s foot', ['arcuate', 'cuspate', 'estuarine'], 'The Nile delta is the classic arcuate delta. [1]'),
        ('Levees are made of coarser material close to the channel because', 'velocity falls rapidly when water spills over the banks, so the coarsest load is dropped first', ['finer material is eroded from them', 'people dump gravel there', 'the wind sorts the sediment'], '[1]'),
        ('A sinuosity index above 1.5 indicates', 'a meandering channel', ['a straight channel', 'a braided channel only', 'a river in its upper course'], '[1]'),
        ('Which deposits form the bedding of a delta from top to bottom?', 'topset, foreset, bottomset beds', ['bottomset, topset, foreset beds', 'foreset, bottomset, topset beds', 'point bar, levee, floodplain'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of a meander.', 'Riffle-pool sequences develop; flow is deflected to alternate banks; helicoidal flow erodes the outer bank (river cliff) by hydraulic action and abrasion where velocity is highest, and carries sediment to the inner bank to form a point bar; the bend migrates and becomes more pronounced.', '1 mark each stage up to [4]'),
        ('Explain how a floodplain is formed.', 'Lateral erosion by migrating meanders widens the valley floor; deposition of point bars; overbank deposition of silt during floods builds up layers of alluvium.', '1 mark lateral erosion; 1 mark point bars; 1 mark flood deposits [3]'),
        ('Explain the conditions needed for a delta to form.', 'Large sediment load; velocity drops on entering standing water; low tidal range and weak currents; flocculation of clay in salt water; shallow offshore gradient.', '1 mark per condition [3]'),
        ('Explain the formation of an oxbow lake.', 'Erosion on outer banks narrows the meander neck; during a flood the river cuts through the neck, taking the shorter route; deposition seals the ends of the old loop, leaving a lake that may become a swamp (meander scar).', '1 mark each stage [3]'),
    ],
    'claims': [
        ('Deltas only form where rivers enter the sea.', False, 'They can also form in lakes, for example where the Rhône enters Lake Geneva.'),
        ('Levees can be artificially raised to reduce flooding.', True, 'Artificial levees line the lower Mississippi, but if they fail flooding can be worse.'),
        ('Erosion and deposition occur at the same time in a meander.', True, 'The outer bank is eroded while the point bar on the inner bank is built up.'),
    ],
    'cs': [
        ('a river landform or delta', [
            ('the Ganges-Brahmaputra delta, Bangladesh', {'form': 'The world’s largest delta (about 100 000 km²) formed from over 1 billion tonnes of sediment a year eroded from the Himalaya; distributaries, char islands and the Sundarbans mangroves; active subsidence and tidal influence.',
                                                          'people': 'Home to over 150 million people; fertile alluvium for rice; frequent floods and cyclones (e.g. Cyclone Sidr 2007); sea-level rise, subsidence and dams upstream (Farakka barrage) reduce sediment supply.'}),
            ('the Nile delta, Egypt', {'form': 'A classic arcuate delta about 240 km wide, formed by sediment from the Ethiopian Highlands; built by the Rosetta and Damietta distributaries.',
                                       'people': 'Holds about 40% of Egypt’s population and most farmland; since the Aswan High Dam (1970) traps sediment, the coast retreats by up to 100 m a year in places such as Rosetta; salinisation and subsidence.'}),
        ], [
            ('explain how the landform developed', 'form', 'Sediment supply, deposition processes, distributaries, shape.'),
            ('describe the opportunities and challenges the landform presents for people', 'people', 'Farming, settlement, hazards, human impacts, with figures.', 'assess the extent to which human activities threaten the landform.'),
        ]),
    ],
    'essays': [
        ('deposition is more important than erosion in the formation of river landforms',
         ['Point bars, levees, floodplains, deltas and braided bars are depositional; floodplain alluvium is built by repeated floods.'],
         ['Meanders, river cliffs, oxbow lakes and floodplains also need lateral erosion; waterfalls, gorges and potholes are erosional; most landforms involve both.'],
         'Most lowland landforms are the result of erosion and deposition acting together, though depositional processes dominate in the lower course and in deltas.',
         ['meanders', 'levees', 'deltas', 'floodplains']),
    ],
})


@data(c3c)
def c3c_sin(r, D):
    k = r.choice([3, 4])
    rows = []
    for j in range(k):
        s = round(r.uniform(0.8, 6.0), 1)
        cl = round(s * r.choice([r.uniform(1.0, 1.4), r.uniform(1.5, 2.6)]), 1)
        rows.append((f'Reach {"ABCD"[j]}', cl, s))
    res = [(n, cl / s) for n, cl, s in rows]
    stem = 'Fig. 3.3 is a map of a river. Measurements for several reaches are: ' + ' '.join(f'{n}: channel length {fmt(cl, 1)} km, straight-line distance {fmt(s, 1)} km.' for n, cl, s in rows)
    hi = max(res, key=lambda x: x[1])
    if D == 1:
        n, cl, s = rows[0]
        opts, a = mcq(r, dp(cl / s, 2), [dp(s / cl, 2), dp(cl - s, 2), dp(cl * s, 2), dp(cl / s + 0.3, 2)])
        return {'stem': stem + f' What is the sinuosity of {n}?', 'options': opts, 'answer': a, 'key': f'{fmt(cl, 1)} ÷ {fmt(s, 1)} = {dp(cl / s, 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the sinuosity index of each reach.', '; '.join(f'{n} {dp(v, 2)}' for n, v in res), 'channel length ÷ straight-line distance; 1 mark half correct, 2 marks all [2]'),
        lambda r: ('Classify each reach as straight, sinuous or meandering (meandering > 1.5).', '; '.join(f'{n} {"meandering" if v > 1.5 else "sinuous" if v > 1.05 else "straight"}' for n, v in res), '[2]'),
        lambda r: (f'Explain the processes that produce the high sinuosity of {hi[0]}.', 'Helicoidal flow and erosion of outer banks with deposition on inner banks (point bars); bends migrate and grow; low gradient and cohesive banks favour meandering.', '1 mark per process [3]'),
        lambda r: ('Suggest why straightening a meandering reach could increase flood risk downstream.', 'A shorter, steeper and smoother channel carries water downstream faster, so flood peaks arrive sooner and higher downstream.', '1 mark faster flow; 1 mark downstream peak [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 3.4 human impact on rivers
c3d = T('Human impact on rivers: flood prediction, prevention and channel modification', 'human impact on rivers flood prediction prevention channel modification')
B(c3d, {
    'terms': [
        ('recurrence interval', 'the average time between floods of a given size, calculated as (n + 1) ÷ m'),
        ('channelisation', 'the artificial straightening, deepening or lining of a river channel to increase its capacity and velocity'),
        ('hard engineering (rivers)', 'structural flood defences such as dams, levees, flood walls and relief channels'),
        ('soft engineering (rivers)', 'working with natural processes, for example floodplain zoning, wetland restoration and afforestation'),
        ('floodplain zoning', 'restricting land uses on areas of the floodplain according to their flood risk'),
        ('flood relief channel', 'an artificial channel that diverts excess water around a settlement during high flows'),
        ('river restoration', 'returning a modified river to a more natural state, for example by re-creating meanders and wetlands'),
    ],
    'mcq': [
        ('In a record of 49 years, the third-largest flood has a recurrence interval of', '16.7 years', ['49 years', '3 years', '50 years'], '(n + 1) ÷ m = 50 ÷ 3 = 16.7. [1]'),
        ('A “100-year flood” has a probability in any one year of', '1%', ['100%', '10%', '0.1%'], 'Probability = 1 ÷ recurrence interval. [1]'),
        ('Which is a soft engineering approach to flood management?', 'Restoring wetlands upstream to store water', ['Building concrete flood walls', 'Straightening the channel', 'Constructing a large dam'], '[1]'),
        ('The Jubilee River near Maidenhead, UK, is an example of', 'a flood relief channel', ['a dam', 'a levee', 'a washland'], '[1]'),
    ],
    'explain': [
        ('Explain how flood prediction can reduce the impacts of floods.', 'Rainfall radar, river gauges and hydrological models give warnings hours or days ahead, so people can move belongings, evacuate, close barriers and deploy temporary defences.', '1 mark method; 1 mark use of warning; 1 mark example [3]'),
        ('Explain why channelisation in one place may increase flood risk elsewhere.', 'Faster flow carries the flood peak downstream more quickly and concentrates it, increasing peaks in unprotected settlements downstream.', '[2]'),
        ('Explain the advantages of floodplain zoning.', 'Keeps high-value buildings away from the highest-risk areas; low-value uses (parks, farmland) can flood safely; cheap; allows natural storage.', '1 mark each [3]'),
        ('Explain why river restoration is increasingly used in HICs.', 'Restores habitats and biodiversity, slows flow and stores water on floodplains, is cheaper to maintain than hard engineering, improves amenity; e.g. the River Skerne (UK) or the Isar in Munich.', '1 mark per reason [3]'),
    ],
    'claims': [
        ('A 100-year flood can only happen once a century.', False, 'It has a 1% chance in any year, so two can occur in consecutive years.'),
        ('Hard engineering can create a false sense of security.', True, 'People build behind levees; when they are overtopped, as in New Orleans in 2005, damage is greater.'),
        ('Dams have no effect on rivers downstream.', False, 'They trap sediment, alter regimes and cause downstream channel erosion and delta retreat.'),
    ],
    'cs': [
        ('flood management', [
            ('the Mississippi River, USA', {'measures': 'Over 5000 km of levees, flood walls, cut-offs straightening meanders, upstream dams, and floodways such as the Bonnet Carré Spillway and Morganza Floodway that divert water from New Orleans.',
                                           'evaluate': 'Levees protected cities in 2011, when the Morganza Floodway was opened; but 1993 flood breached over 1000 levees, and Hurricane Katrina (2005) overwhelmed defences in New Orleans; channel modifications increased flood heights and starved the delta of sediment.'}),
            ('the Yangtze River, China', {'measures': 'The Three Gorges Dam (2006-2012) with 22 billion m³ of flood storage; dykes along the middle reaches; flood diversion areas such as Jingjiang; returning farmland to lakes.',
                                          'evaluate': 'Reduced peak flows in 2010 and 2020 floods but could not prevent damage from heavy rain on downstream tributaries in 2020; 1.3 million people relocated; sediment trapped and downstream erosion.'}),
            ('Boscastle and the River Valency, UK', {'measures': 'After the 2004 flash flood, the channel was widened and deepened, a new bridge with larger capacity built, and woodland managed upstream at a cost of about £4.5 million.',
                                                    'evaluate': 'Designed to cope with a 1-in-75-year flood; the village coped better in 2007; but defences cannot cope with every extreme event and the scheme altered the natural channel.'}),
        ], [
            ('describe the methods used to manage flooding', 'measures', 'Hard and soft methods, scale, cost, dates.', 'evaluate the success of attempts to manage flooding.'),
            ('evaluate how successful the flood management has been', 'evaluate', 'Successes and failures with evidence; social, economic and environmental costs.'),
        ]),
    ],
    'essays': [
        ('soft engineering is a more sustainable way of managing river floods than hard engineering',
         ['Wetland restoration, afforestation, floodplain zoning and making space for water work with natural processes, are cheaper to maintain and improve habitats (e.g. Netherlands Room for the River).'],
         ['Soft methods need large areas of land and cannot protect existing dense cities; hard engineering such as the Thames Barrier or the Three Gorges Dam protects millions and high-value property.'],
         'A combined, catchment-wide approach is most sustainable: soft engineering upstream and on floodplains, with hard engineering where high-value urban areas need protection.',
         ['cost', 'environmental impact', 'urban areas', 'catchment management']),
    ],
})


@data(c3d)
def c3d_ri(r, D):
    n = r.choice([19, 24, 29, 39, 49])
    k = 6
    peaks = sorted(r.sample(range(150, 1200), k), reverse=True)
    yrs = r.sample(range(2025 - n, 2025), k)
    nm = r.choice(BASINS)
    stem = f'Table 3.4 lists the six largest annual peak discharges (m³/s) in a {n}-year record for the {nm}: ' + ', '.join(f'{y}: {p}' for y, p in zip(yrs, peaks)) + '.'
    m = r.randint(1, k)
    R = (n + 1) / m
    if D == 1:
        opts, a = mcq(r, f'{dp(R)} years', [f'{dp(n / m)} years' if n % m else f'{dp(R + 1)} years', f'{dp(m / (n + 1) * 100)} years', f'{dp((n + 1) / (m + 1))} years', f'{n + 1} years' if m > 1 else f'{dp(R / 2)} years'])
        return {'stem': stem + f' Using the formula (n + 1) ÷ m, what is the recurrence interval of the flood ranked {m}?', 'options': opts, 'answer': a, 'key': f'({n} + 1) ÷ {m} = {dp(R)} years. [1]'}
    p = peaks[m - 1]
    parts = [
        lambda r: (f'Calculate the recurrence interval of the {p} m³/s flood.', f'{dp(R)} years', f'rank m = {m}; ({n} + 1) ÷ {m} = {dp(R)} years [2]'),
        lambda r: (f'Calculate the probability of a flood of at least {p} m³/s occurring in any one year.', f'{dp(100 / R)}%', f'1 ÷ {dp(R)} × 100 = {dp(100 / R)}% [1]'),
        lambda r: ('Explain why estimates of the 100-year flood from this record are unreliable.', f'The record is only {n} years long, so extrapolating to 100 years is uncertain; land-use change and climate change mean past floods may not represent future ones.', '1 mark short record; 1 mark changing conditions [2]'),
        lambda r: ('Suggest how planners might use recurrence intervals.', 'To design defences to a standard (e.g. 1-in-100-year), to zone land use on floodplains, to set insurance premiums and to justify spending by cost-benefit analysis.', '1 mark each [2]'),
        lambda r: ('Suggest why the size of floods might be increasing in this basin.', 'Urbanisation, deforestation, field drainage, channelisation upstream, or more intense rainfall due to climate change.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@data(c3d)
def c3d_cba(r, D):
    schemes = [('raising flood embankments', 'hard'), ('a flood relief channel', 'hard'), ('upstream woodland planting and leaky dams', 'soft'), ('floodplain zoning and washlands', 'soft'), ('a flood wall with demountable barriers', 'hard')]
    pick = r.sample(schemes, 3)
    rows = []
    for nm, kind in pick:
        cost = r.randint(4, 60)
        ben = round(cost * r.uniform(0.6, 4.5), 1)
        rows.append((nm, kind, cost, ben, ben / cost))
    town = city(r)
    stem = f'Table 3.5 shows estimated costs and benefits (damage avoided over 50 years, US$ million) of three flood schemes for a town near {town}. ' + ' '.join(f'{cap(n)}: cost {c}, benefits {fmt(b, 1)}.' for n, _, c, b, _ in rows)
    best = max(rows, key=lambda x: x[4])
    if D == 1:
        opts, a = mcq(r, cap(best[0]), [cap(x[0]) for x in rows if x is not best] + [cap(s[0]) for s in schemes if s[0] not in [x[0] for x in rows]][:1])
        return {'stem': stem + ' Which scheme has the highest benefit-cost ratio?', 'options': opts, 'answer': a, 'key': '; '.join(f'{n}: {dp(v, 2)}' for n, _, _, _, v in rows) + ' [1]'}
    parts = [
        lambda r: ('Calculate the benefit-cost ratio for each scheme.', '; '.join(f'{n}: {dp(v, 2)}' for n, _, _, _, v in rows), 'benefits ÷ costs [2]'),
        lambda r: ('Identify which schemes are economically justified.', ', '.join(n for n, _, _, _, v in rows if v > 1) or 'none', 'ratio above 1 [1]'),
        lambda r: ('Explain why decision-makers might not simply choose the scheme with the highest ratio.', 'Environmental and social impacts (habitats, landscape, displacement) are hard to value; effects on communities downstream; the standard of protection; who pays; uncertainty of estimates.', '1 mark per point [3]'),
        lambda r: ('Classify each scheme as hard or soft engineering.', '; '.join(f'{n}: {k}' for n, k, *_ in rows), '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[3] = [c3a, c3b, c3c, c3d]


# ============================================================== CHAPTER 4: Local energy budgets

ALBEDO = [('fresh snow', 0.85), ('desert sand', 0.40), ('concrete', 0.30), ('grassland', 0.25), ('deciduous forest', 0.17), ('tropical rainforest', 0.13),
          ('asphalt road', 0.07), ('sea water (high sun)', 0.06), ('bare dark soil', 0.10), ('sea ice', 0.60)]

c4a = T('Daytime and night-time energy budgets', 'daytime night-time energy budgets')
B(c4a, {
    'terms': [
        ('energy budget', 'the balance between the energy received by a surface and the energy lost from it over a period'),
        ('albedo', 'the proportion of incoming solar radiation reflected by a surface'),
        ('incoming solar radiation (insolation)', 'short-wave radiation from the sun reaching the Earth’s surface'),
        ('long-wave radiation', 'infrared radiation emitted by the Earth’s surface and atmosphere'),
        ('sensible heat transfer', 'the movement of heat by conduction and convection between the surface and the air'),
        ('latent heat transfer', 'energy used in evaporation (taken from the surface) or released by condensation'),
        ('surface absorption', 'energy that passes into the ground or water by conduction and is stored below the surface'),
        ('counter-radiation', 'long-wave radiation emitted back towards the surface by clouds and greenhouse gases'),
    ],
    'mcq': [
        ('Which surface has the highest albedo?', 'Fresh snow', ['Asphalt', 'Tropical rainforest', 'Deep ocean water'], '[1]'),
        ('At night, the most important source of energy gain at the surface under cloudy skies is', 'counter-radiation from clouds', ['incoming solar radiation', 'reflected solar radiation', 'latent heat of evaporation'], '[1]'),
        ('Which component of the daytime energy budget is reduced most when a surface is dry?', 'Latent heat transfer (evaporation)', ['Incoming solar radiation', 'Reflected solar radiation', 'Long-wave counter-radiation'], '[1]'),
        ('Dew formation at night releases energy to the surface by', 'latent heat transfer (condensation)', ['sensible heat transfer', 'reflection', 'surface absorption'], '[1]'),
    ],
    'explain': [
        ('Explain why night-time temperatures fall more on clear nights than on cloudy nights.', 'Without cloud, long-wave radiation escapes to space; clouds absorb outgoing long-wave radiation and re-emit it back (counter-radiation), so heat loss is reduced.', '1 mark clear sky loss; 1 mark cloud counter-radiation [2]'),
        ('Explain the components of the daytime energy budget.', 'Incoming solar radiation is partly reflected (albedo); some energy is absorbed into the ground (surface absorption); some heats the air by sensible heat transfer; some is used for evaporation (latent heat); the surface emits long-wave radiation.', '1 mark per component [5]'),
        ('Explain why a wet soil heats up more slowly than a dry soil during the day.', 'Energy is used in evaporation (latent heat transfer) rather than raising temperature; water has a high specific heat capacity and conducts heat into the soil.', '1 mark latent heat; 1 mark heat capacity/conduction [2]'),
        ('Explain the night-time energy budget.', 'Net long-wave loss from the surface; partly offset by counter-radiation from clouds, sensible heat transfer from warmer air, subsurface supply of heat stored during the day and latent heat released by condensation (dew).', '1 mark per component [4]'),
    ],
    'claims': [
        ('Surfaces with a high albedo warm up quickly in the sun.', False, 'High albedo surfaces reflect much of the insolation, so less is absorbed and they warm slowly.'),
        ('The ground can act as a source of heat at night.', True, 'Heat absorbed during the day is conducted back to the surface at night (subsurface supply).'),
        ('Latent heat transfer always causes the surface to lose energy.', False, 'Evaporation removes energy, but condensation (dew) releases latent heat to the surface.'),
    ],
    'essays': [
        ('cloud cover is the most important factor influencing local energy budgets',
         ['Clouds reflect incoming solar radiation by day and give counter-radiation at night, so they reduce the diurnal range (e.g. humid tropics v deserts).'],
         ['Surface albedo, moisture availability (latent heat), wind speed (sensible heat), season and latitude (sun angle), and urban surfaces also control budgets.'],
         'Cloud cover is crucial for the diurnal range, but surface characteristics and sun angle decide how much energy is available in the first place.',
         ['albedo', 'moisture', 'wind', 'urban surfaces']),
    ],
})


@data(c4a)
def c4a_budget(r, D):
    surf, alb = r.choice(ALBEDO)
    I = r.randint(50, 90) * 10
    refl = round(I * alb)
    remain = I - refl
    LW = r.randint(8, 16) * 5
    LH = round(remain * r.uniform(0.25, 0.55))
    SA = round(remain * r.uniform(0.05, 0.15))
    SH = remain - LW - LH - SA
    if SH <= 0:
        return None
    stem = (f'Table 4.1 shows a midday energy budget (W/m²) for a surface of {surf} on a clear day: incoming solar radiation {I}; reflected solar radiation {refl}; '
            f'net long-wave radiation loss {LW}; latent heat transfer (evaporation) {LH}; surface absorption {SA}; sensible heat transfer to the air: not shown.')
    if D == 1:
        opts, a = mcq(r, f'{dp(alb * 100, 0)}%', [f'{dp((1 - alb) * 100, 0)}%', f'{dp(LW / I * 100, 0)}%', f'{dp(alb * 50, 0)}%', f'{dp(min(95, alb * 100 + 20), 0)}%'])
        return {'stem': stem + ' What is the albedo of the surface?', 'options': opts, 'answer': a, 'key': f'{refl} ÷ {I} × 100 = {dp(alb * 100, 0)}%. [1]'}
    parts = [
        lambda r: ('Calculate the albedo of the surface as a percentage.', f'{dp(alb * 100, 0)}%', f'{refl} ÷ {I} × 100 [1]'),
        lambda r: ('Calculate the sensible heat transfer, assuming the budget balances.', f'{SH} W/m²', f'{I} − {refl} − {LW} − {LH} − {SA} = {SH} [2]'),
        lambda r: ('Explain how the budget would differ if the surface were wet.', 'More energy would be used in evaporation (latent heat), so less would be available for sensible heat transfer and surface temperature would be lower.', '1 mark latent heat up; 1 mark sensible heat/temperature down [2]'),
        lambda r: ('Describe how the energy budget changes at night.', 'No incoming solar radiation; net long-wave loss dominates; energy is gained from the subsurface, from sensible heat transfer from the air and from latent heat released by dew formation.', '1 mark each [3]'),
        lambda r: ('Suggest why the albedo of this surface could change during the year.', 'Snow cover, leaf fall, crop growth or harvest, wetness, sun angle (especially for water).', '1 mark reason; 1 mark development [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@c4a.add('C3', (1, 2, 3, 4), 'numerical')
def c4a_alb(r, D):
    rows = r.sample(ALBEDO, 4)
    I = r.randint(40, 90) * 10
    stem = f'Incoming solar radiation at midday is {I} W/m². Albedo values for four surfaces are: ' + ', '.join(f'{s} {fmt(a, 2)}' for s, a in rows) + '.'
    s, a = rows[r.randrange(4)]
    ab = I * (1 - a)
    if D <= 2:
        opts, ans = mcq(r, f'{dp(ab, 0)} W/m²', [f'{dp(I * a, 0)} W/m²', f'{I} W/m²', f'{dp(ab / 2, 0)} W/m²', f'{dp(ab + 100, 0)} W/m²'])
        return {'stem': stem + f' How much solar radiation is absorbed by the {s}?', 'options': opts, 'answer': ans, 'key': f'{I} × (1 − {fmt(a, 2)}) = {dp(ab, 0)} W/m². [1]'}
    hi = max(rows, key=lambda x: 1 - x[1])
    return {'stem': stem + f' (a) Calculate the solar radiation absorbed by the {s}. (b) Identify which surface would warm most rapidly and explain why.',
            'answer': f'(a) {dp(ab, 0)} W/m² (b) {hi[0]}: the lowest albedo means the most radiation is absorbed (assuming similar moisture and heat capacity).',
            'key': f'(a) {I} × (1 − {fmt(a, 2)}) [2] (b) 1 mark surface; 1 mark reason [2]', 'marks': 4}


# --------------------------------------------------------------- 4.2 inversions, mist and fog
c4b = T('Temperature inversions, mist and fog', 'temperature inversions mist fog')
B(c4b, {
    'terms': [
        ('temperature inversion', 'a layer of the atmosphere in which temperature increases with height'),
        ('radiation fog', 'fog formed on clear, calm nights when the ground loses heat by radiation and cools the air above it to its dew point'),
        ('advection fog', 'fog formed when warm, moist air moves over a cold surface, such as a cold ocean current, and is cooled to its dew point'),
        ('dew point', 'the temperature at which air becomes saturated and condensation begins'),
        ('mist', 'suspended water droplets reducing visibility to between 1 and 2 km'),
        ('fog', 'suspended water droplets reducing visibility to below 1 km'),
        ('cold air drainage', 'the movement of dense, cold air downslope into valleys at night'),
        ('frost hollow', 'a valley floor or depression where cold air collects at night, giving frequent frost'),
    ],
    'mcq': [
        ('Radiation fog is most likely', 'on a clear, calm night in autumn over a moist valley floor', ['on a windy, cloudy night', 'at midday in summer', 'over a hot desert in the afternoon'], '[1]'),
        ('The frequent fogs along the coast of San Francisco and the Atacama coast are mainly', 'advection fogs over cold ocean currents', ['radiation fogs', 'frontal fogs', 'steam fogs'], 'The California and Humboldt (Peru) currents cool moist sea air. [1]'),
        ('Visibility of 600 m in a layer of water droplets is defined as', 'fog', ['mist', 'haze', 'smog'], 'Fog is below 1 km. [1]'),
        ('Which of these conditions helps break up a radiation fog in the morning?', 'Solar heating of the ground and an increase in wind speed', ['A drop in temperature', 'Calm, clear skies', 'Cold air drainage'], '[1]'),
    ],
    'explain': [
        ('Explain how a temperature inversion can form in a valley at night.', 'On clear, calm nights the ground loses heat by radiation and cools the air in contact with it; dense cold air drains downslope into the valley floor, so the coldest air lies beneath warmer air above.', '1 mark radiation loss; 1 mark cold air drainage; 1 mark warm air above [3]'),
        ('Explain why temperature inversions can lead to severe air pollution in cities.', 'Warm air above cold air is stable, so there is no convection; pollutants are trapped near the ground; e.g. Mexico City, Santiago, Delhi in winter, Los Angeles.', '1 mark stability; 1 mark trapped pollutants; 1 mark example [3]'),
        ('Distinguish between radiation fog and advection fog.', 'Radiation fog forms over land on clear, calm nights by radiative cooling; advection fog forms when moist air moves horizontally over a cold surface such as cold sea or snow.', '1 mark each [2]'),
        ('Explain why radiation fog is more common in autumn and winter.', 'Longer nights allow more cooling; air is often moist; low sun may not clear the fog during the day.', '1 mark per point [2]'),
    ],
    'claims': [
        ('Temperature always falls with height in the lower atmosphere.', False, 'In an inversion temperature rises with height, for example in valleys on clear nights.'),
        ('Wind can prevent radiation fog from forming.', True, 'Wind mixes the cold surface air with warmer air above, preventing cooling to dew point.'),
        ('Fog and cloud are formed by the same process of condensation.', True, 'Both form when air cools to its dew point and water vapour condenses on nuclei; fog is simply cloud at ground level.'),
    ],
    'essays': [
        ('temperature inversions are more of a problem in urban areas than in rural areas',
         ['Inversions trap pollutants from traffic and industry, causing smog (London 1952; Delhi; Mexico City); fog disrupts airports and roads.'],
         ['Rural valleys suffer frost hollows damaging crops and orchards; fog affects rural roads; urban heat islands can weaken inversions in city centres.'],
         'Urban inversions have the greatest human health impact because of pollution, though rural inversions bring frost and fog hazards.',
         ['air pollution', 'frost hollows', 'fog', 'urban heat island']),
    ],
})


@data(c4b)
def c4b_profile(r, D):
    hs = [0, 100, 200, 300, 400, 500, 600]
    t0 = r.randint(-2, 8)
    top = r.choice([200, 300, 400])
    rise = r.randint(3, 8)
    temps = []
    for h in hs:
        if h <= top:
            temps.append(round(t0 + rise * h / top, 1))
        else:
            temps.append(round(t0 + rise - 0.0065 * (h - top), 1))
    loc = r.choice(['a valley near Santiago, Chile', 'the Kathmandu valley, Nepal', 'a valley in the Swiss Alps', 'a valley in the Rocky Mountains, USA'])
    stem = f'Fig. 4.2 shows air temperatures measured by a weather balloon at dawn in {loc}: ' + ', '.join(f'{h} m: {fmt(t, 1)} °C' for h, t in zip(hs, temps)) + '.'
    rate = rise / top * 100
    lr = (temps[hs.index(top)] - temps[-1]) / (600 - top) * 1000
    if D == 1:
        opts, a = mcq(r, f'0-{top} m', [f'0-{top - 100} m', f'{top}-600 m', '0-600 m', f'100-{top + 100} m'])
        return {'stem': stem + ' Between which heights is there a temperature inversion?', 'options': opts, 'answer': a, 'key': 'Temperature rises with height up to the top of the inversion. [1]'}
    parts = [
        lambda r: ('Identify the height of the top of the inversion layer.', f'{top} m', '[1]'),
        lambda r: ('Calculate the rate of temperature change within the inversion layer in °C per 100 m.', f'+{dp(rate, 2)} °C per 100 m', f'{rise} °C rise over {top} m [2]'),
        lambda r: (f'Calculate the lapse rate between {top} m and 600 m in °C per 1000 m.', f'{dp(lr, 1)} °C per 1000 m', f'({fmt(temps[hs.index(top)], 1)} − {fmt(temps[-1], 1)}) ÷ {600 - top} × 1000 = {dp(lr, 1)} [2]'),
        lambda r: ('Explain how the inversion formed.', 'Clear skies allowed rapid long-wave radiation loss at night; calm conditions; cold dense air drained down the valley sides and settled on the valley floor beneath warmer air.', '1 mark each [3]'),
        lambda r: ('Explain why air pollution is likely to be high in the valley in the morning.', 'The inversion is stable and acts as a lid: there is no convection, so smoke and vehicle emissions are trapped near the ground until the sun heats the surface.', '1 mark stability; 1 mark trapping [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@data(c4b)
def c4b_fog(r, D):
    T0 = r.randint(8, 16)
    Td = T0 - r.randint(3, 8)
    rate = r.choice([0.5, 1.0, 1.5])
    h = (T0 - Td) / rate
    if h > 11:
        return None
    t = 18 + h
    clock = f'{int(t) % 24:02d}:{int(round((t % 1) * 60)):02d}'
    stem = f'At 18:00 on a clear, calm autumn evening the air temperature at a weather station was {T0} °C and the dew point was {Td} °C. The temperature then fell steadily by {fmt(rate, 1)} °C per hour.'
    if D == 1:
        opts, a = mcq(r, clock, [f'{(int(t) + 2) % 24:02d}:00', f'{(int(18 + (T0 - Td))) % 24:02d}:00' if rate != 1 else f'{(int(t) - 2) % 24:02d}:00', '18:00', f'{(int(t) + 4) % 24:02d}:30'])
        return {'stem': stem + ' At what time would the air reach its dew point?', 'options': opts, 'answer': a, 'key': f'({T0} − {Td}) ÷ {fmt(rate, 1)} = {dp(h)} hours after 18:00 = {clock}. [1]'}
    parts = [
        lambda r: ('Calculate the time at which the air would reach its dew point.', clock, f'({T0} − {Td}) ÷ {fmt(rate, 1)} = {dp(h)} h after 18:00 [2]'),
        lambda r: ('Name the type of fog likely to form and explain its formation.', 'Radiation fog: the ground loses heat by long-wave radiation under clear skies; air in contact is cooled to its dew point and water vapour condenses on nuclei.', '1 mark name; 2 marks explanation [3]'),
        lambda r: ('Suggest why the fog may be thickest in the valley bottom.', 'Cold dense air drains downslope and collects there; valley floors near rivers are moist.', '[2]'),
        lambda r: ('Explain how the fog would be affected if the wind speed increased.', 'Turbulent mixing brings warmer, drier air down, raising temperature above dew point and dispersing the fog (or lifting it into low stratus).', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 4.3 urban climates
c4c = T('Urban climates: the urban heat island, humidity, winds and air quality', 'urban climates urban heat island humidity winds air quality')
B(c4c, {
    'terms': [
        ('urban heat island', 'the higher temperature of a city compared with the surrounding rural area, greatest on calm, clear nights'),
        ('urban heat island intensity', 'the difference between the urban and rural temperature at the same time'),
        ('urban canyon', 'a street between tall buildings that traps radiation and channels winds'),
        ('photochemical smog', 'a haze formed when sunlight reacts with nitrogen oxides and hydrocarbons from vehicles, producing ozone'),
        ('particulate matter (PM2.5)', 'tiny solid or liquid particles less than 2.5 micrometres across, which damage lungs'),
        ('Venturi effect', 'the acceleration of wind as it is funnelled between tall buildings'),
        ('green roof', 'a roof covered with vegetation that reduces runoff and cools the building by evapotranspiration'),
    ],
    'mcq': [
        ('The urban heat island is usually most intense', 'on calm, clear nights', ['on windy, cloudy days', 'at midday in winter', 'during heavy rain'], '[1]'),
        ('Relative humidity is usually lower in city centres than in the countryside mainly because', 'temperatures are higher and there is less evapotranspiration', ['there is more vegetation', 'there are more lakes', 'cities receive less rain'], '[1]'),
        ('Which policy has been used in Delhi to reduce air pollution?', 'Converting buses and auto-rickshaws to compressed natural gas (CNG)', ['Building more coal power stations in the city', 'Burning crop stubble', 'Removing parks'], '[1]'),
        ('Mean wind speeds in cities are generally', 'lower than in rural areas, but gusts can be strong between tall buildings', ['always higher than in rural areas', 'the same as in rural areas', 'zero'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of the urban heat island.', 'Dark surfaces with low albedo absorb insolation; concrete and brick store heat and release it at night; heat from vehicles, industry and air conditioning; less evapotranspiration; pollution dome traps long-wave radiation; urban canyons reduce wind and trap radiation.', '1 mark per cause [5]'),
        ('Explain why urban areas can have more thunderstorms and rainfall than surrounding areas.', 'Higher temperatures cause convection; buildings increase turbulence and uplift; pollution provides condensation nuclei.', '1 mark each [3]'),
        ('Explain how urban structures affect wind speeds.', 'Tall buildings increase friction, reducing mean speeds; but funnel winds through urban canyons (Venturi effect) and cause eddies and gusts at the base of tower blocks.', '1 mark each [3]'),
        ('Explain how cities can reduce the urban heat island.', 'Green roofs and parks increase evapotranspiration; high-albedo (cool) roofs and pavements; water features; shading trees; reducing waste heat from vehicles and air conditioning.', '1 mark per strategy explained [4]'),
    ],
    'claims': [
        ('Urban areas are always warmer than rural areas at all times of day.', False, 'The heat island is strongest at night; by day the difference can be small, and parks can create cool islands.'),
        ('Air pollution in cities can reduce sunshine hours.', True, 'Particulates scatter and absorb sunlight, reducing direct insolation.'),
        ('Photochemical smog needs strong sunlight to form.', True, 'Ultraviolet light drives the reactions between nitrogen oxides and hydrocarbons that form ozone.'),
    ],
    'cs': [
        ('urban air quality management', [
            ('Mexico City', {'problem': 'High altitude basin (2240 m) surrounded by mountains, frequent winter inversions, over 5 million vehicles and industry; in 1992 the UN described it as the most polluted city in the world; ozone and PM2.5.',
                             'response': 'Hoy No Circula (no-drive days by number plate) since 1989; unleaded fuel; refinery closure; Metrobús and bicycle hire (Ecobici); air-quality alerts; ozone has fallen substantially since the 1990s though alerts still occur.'}),
            ('Delhi, India', {'problem': 'Among the world’s most polluted cities: winter PM2.5 often over 300 μg/m³; sources include vehicles, construction dust, industry, and crop-stubble burning in Punjab and Haryana; winter inversions and calm weather trap pollutants.',
                              'response': 'CNG conversion of buses and auto-rickshaws (2002); Delhi Metro; odd-even car rationing trials (2016); Graded Response Action Plan; closing coal power stations in the city; limited success because sources are regional.'}),
        ], [
            ('explain why air quality is poor', 'problem', 'Physical (relief, inversions, climate) and human causes, with figures.'),
            ('describe the strategies used to improve air quality', 'response', 'Named policies, dates, effects.', 'evaluate the success of attempts to improve urban air quality.'),
        ]),
    ],
    'essays': [
        ('human activity is the main cause of the distinctive climate of urban areas',
         ['Waste heat, pollution, low-albedo building materials, removal of vegetation and building geometry create the heat island, lower humidity and altered winds.'],
         ['Physical factors (site in a basin or valley, latitude, coastal location, weather type such as calm anticyclones) determine how strongly urban effects show.'],
         'Urban climates are created by human structures and activity, but weather and site determine their intensity.',
         ['heat island', 'pollution', 'relief and site', 'weather conditions']),
    ],
})


add_spearman(c4c, [
    {'intro': 'Students recorded air temperature at 22:00 on a calm, clear night at {n} sites along a transect from the CBD of a city to the rural fringe.', 'label': 'Site',
     'x': ('distance from the CBD (km)', 0.2, 18, 1), 'y': ('temperature (°C)', 9.0, 16.5, 1), 'sign': -1,
     'why': 'Near the CBD, dense buildings store heat, waste heat from traffic and air conditioning, low albedo and little evapotranspiration raise temperatures; towards the fringe vegetation and open space allow faster cooling.',
     'limit': 'Readings were taken at slightly different times as students moved along the transect; use simultaneous readings or data loggers at fixed heights.'},
    {'intro': 'A student measured particulate concentration (PM10) at {n} roadside sites in a city with different traffic flows.', 'label': 'Site',
     'x': ('vehicles per hour', 80, 3000, 0), 'y': ('PM10 (μg/m³)', 15, 140, 0), 'sign': 1,
     'why': 'Vehicle exhausts, brake and tyre wear and resuspended road dust add particulates, so concentrations rise with traffic flow, especially in urban canyons where dispersal is poor.',
     'limit': 'Single short readings vary with wind and weather; repeat at the same times on several days and record wind speed.'},
])


@data(c4c)
def c4c_uhi(r, D):
    cityn = r.choice(['Tokyo', 'London', 'São Paulo', 'Mumbai', 'Cairo', 'Toronto', 'Singapore', 'Paris'])
    hrs = ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00']
    rural = [r.randint(6, 10), r.randint(4, 8), r.randint(8, 12), r.randint(17, 22), r.randint(18, 23), r.randint(10, 14)]
    diff = [r.uniform(3, 6), r.uniform(3.5, 7), r.uniform(1, 2.5), r.uniform(0, 1.5), r.uniform(0.5, 1.5), r.uniform(2.5, 5)]
    urban = [round(a + b, 1) for a, b in zip(rural, diff)]
    uhi = [round(u - a, 1) for u, a in zip(urban, rural)]
    stem = f'Table 4.3 shows air temperatures (°C) on a calm, clear day in {cityn}. ' + ' '.join(f'{h}: city centre {fmt(u, 1)}, rural {a}.' for h, u, a in zip(hrs, urban, rural))
    mx = max(uhi)
    i = uhi.index(mx)
    if D == 1:
        opts, a = mcq(r, hrs[i], [h for h in hrs if h != hrs[i]])
        return {'stem': stem + ' At what time was the urban heat island intensity greatest?', 'options': opts, 'answer': a, 'key': f'{hrs[i]}: {fmt(urban[i], 1)} − {rural[i]} = {fmt(mx, 1)} °C. [1]'}
    parts = [
        lambda r: ('Calculate the urban heat island intensity at each time.', '; '.join(f'{h} {fmt(x, 1)} °C' for h, x in zip(hrs, uhi)), 'urban − rural [2]'),
        lambda r: ('Describe the daily pattern of urban heat island intensity.', f'Greatest at night (max {fmt(mx, 1)} °C at {hrs[i]}), smallest around midday and afternoon.', '1 mark pattern; 1 mark data [2]'),
        lambda r: ('Explain why the heat island is strongest at night.', 'Buildings and roads release heat stored during the day; urban canyons reduce long-wave radiation loss to the sky (low sky view factor); rural areas cool rapidly by radiation under clear skies.', '1 mark per point [3]'),
        lambda r: ('Explain how the heat island would differ on a windy, cloudy day.', 'Weaker: wind mixes urban and rural air; cloud reduces solar heating by day and radiation loss at night in both areas.', '[2]'),
        lambda r: ('Suggest two strategies to reduce the urban heat island.', 'Green roofs and walls; more parks and trees; high-albedo roofs and pavements; water features; reduce waste heat from vehicles.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[4] = [c4a, c4b, c4c]


# ============================================================== CHAPTER 5: Global energy budget and atmospheric circulation

c5a = T('The latitudinal pattern of radiation and heat transfer', 'latitudinal pattern of radiation heat transfer')
B(c5a, {
    'terms': [
        ('radiation surplus', 'where incoming solar radiation absorbed exceeds outgoing long-wave radiation, as between about 35°N and 35°S'),
        ('radiation deficit', 'where outgoing long-wave radiation exceeds incoming solar radiation absorbed, as at high latitudes'),
        ('angle of incidence', 'the angle at which the sun’s rays strike the surface; higher angles concentrate energy on a smaller area'),
        ('heat transfer', 'the movement of energy from low to high latitudes by winds and ocean currents'),
        ('global energy budget', 'the balance between incoming solar radiation and outgoing radiation for the Earth as a whole'),
        ('latent heat transfer (global)', 'the poleward movement of energy stored in water vapour and released when it condenses'),
    ],
    'mcq': [
        ('The radiation surplus between the tropics is balanced by', 'transfers of heat polewards by winds and ocean currents', ['higher albedo at the equator', 'more reflection at the poles', 'volcanic heat at high latitudes'], '[1]'),
        ('Polar regions receive less insolation per unit area mainly because', 'the sun’s rays strike at a low angle and pass through more atmosphere', ['they are further from the sun', 'they have no daylight in summer', 'their albedo is low'], '[1]'),
        ('About what proportion of the poleward heat transfer is carried by the atmosphere?', 'About 80%, with ocean currents carrying the rest', ['About 5%', 'About 50%, with volcanoes carrying the rest', 'All of it'], '[1]'),
        ('At approximately which latitudes does incoming radiation balance outgoing radiation?', 'About 35-40° north and south', ['The equator', 'The tropics (23.5°)', 'The Arctic and Antarctic Circles'], '[1]'),
    ],
    'explain': [
        ('Explain why there is a radiation surplus at low latitudes and a deficit at high latitudes.', 'High sun angles at low latitudes concentrate insolation and rays pass through less atmosphere; at high latitudes low angles spread energy over large areas, more is reflected (snow and ice albedo) and absorbed by the thicker atmosphere path.', '1 mark per factor [4]'),
        ('Explain how ocean currents transfer heat polewards.', 'Warm currents such as the Gulf Stream and Kuroshio carry warm water from the tropics to higher latitudes, releasing heat to the air; cold currents return cold water towards the equator.', '1 mark warm; 1 mark cold; 1 mark example [3]'),
        ('Explain the role of latent heat in the global transfer of energy.', 'Evaporation in the tropics stores energy in water vapour, which is carried polewards by winds; when it condenses at higher latitudes the latent heat is released, warming the atmosphere.', '[3]'),
    ],
    'claims': [
        ('Without heat transfer, the tropics would keep getting hotter and the poles colder.', True, 'The surplus and deficit would not be balanced, so temperature contrasts would grow.'),
        ('The poles receive no solar radiation at all.', False, 'They receive radiation in summer, including 24-hour daylight, but at very low angles.'),
        ('Ocean currents only move heat from west to east.', False, 'They move heat polewards (e.g. Gulf Stream) and cold water equatorwards (e.g. Canary, Benguela).'),
    ],
    'essays': [
        ('the atmosphere is more important than the oceans in transferring heat from the equator to the poles',
         ['Winds in the Hadley, Ferrel and polar cells and mid-latitude depressions carry sensible and latent heat; the atmosphere carries most of the transfer, especially in middle latitudes.'],
         ['Ocean currents carry much of the heat at low latitudes and warm western Europe through the North Atlantic Drift; the thermohaline circulation moves heat over long timescales.'],
         'The atmosphere carries most heat overall, but oceans dominate at low latitudes and have major regional effects.',
         ['tri-cellular model', 'ocean currents', 'latent heat', 'regional effects']),
    ],
})

LAT_IN = {0: 305, 10: 300, 20: 285, 30: 262, 40: 228, 50: 192, 60: 155, 70: 125, 80: 105, 90: 98}
LAT_OUT = {0: 248, 10: 248, 20: 246, 30: 240, 40: 228, 50: 216, 60: 205, 70: 195, 80: 186, 90: 180}


@data(c5a)
def c5a_lat(r, D):
    lats = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    j = lambda: r.randint(-4, 4)
    inc = [LAT_IN[l] + j() for l in lats]
    out = [LAT_OUT[l] + j() for l in lats]
    net = [a - b for a, b in zip(inc, out)]
    hemi = r.choice(['Northern', 'Southern'])
    stem = f'Table 5.1 shows mean annual absorbed solar radiation and outgoing long-wave radiation (W/m²) at latitudes in the {hemi} Hemisphere. ' + ' '.join(f'{l}°: in {a}, out {b}.' for l, a, b in zip(lats, inc, out))
    sur = [l for l, n in zip(lats, net) if n > 0]
    k = r.randrange(10)
    if D == 1:
        opts, a = mcq(r, f'{sgn(net[k], 0)} W/m²', [f'{sgn(-net[k], 0)} W/m²' if net[k] else '+10 W/m²', f'+{inc[k] + out[k]} W/m²', f'{sgn(net[k] + 20, 0)} W/m²', f'{sgn(net[k] - 15, 0)} W/m²'])
        return {'stem': stem + f' What is the net radiation balance at {lats[k]}°?', 'options': opts, 'answer': a, 'key': f'{inc[k]} − {out[k]} = {net[k]}. [1]'}
    parts = [
        lambda r: ('Calculate the net radiation balance at each latitude.', '; '.join(f'{l}° {sgn(n, 0)}' for l, n in zip(lats, net)), 'incoming − outgoing [2]'),
        lambda r: ('Identify the range of latitudes with a radiation surplus.', f'{min(sur)}° to {max(sur)}°' if sur else 'none', '[1]'),
        lambda r: ('Explain why outgoing radiation varies much less with latitude than incoming radiation.', 'Outgoing long-wave radiation depends on surface and atmospheric temperatures, which are evened out by heat transfer; incoming radiation depends strongly on sun angle and day length.', '[2]'),
        lambda r: ('Explain why the polar regions do not become steadily colder despite the deficit.', 'Heat is transferred from the surplus areas by winds (including depressions and latent heat) and ocean currents, balancing the budget.', '1 mark winds; 1 mark currents [2]'),
        lambda r: ('Suggest how melting sea ice could affect the radiation balance at high latitudes.', 'Lower albedo of open water means more absorption of insolation, increasing warming (positive feedback).', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 5.2 tri-cellular model
c5b = T('Tri-cellular model, pressure belts, winds and ocean currents', 'tri-cellular model pressure belts winds ocean currents')
B(c5b, {
    'terms': [
        ('Hadley cell', 'the atmospheric circulation cell between the equator and about 30°, with rising air at the ITCZ and sinking air in the subtropics'),
        ('Ferrel cell', 'the mid-latitude circulation cell between about 30° and 60°, driven by the Hadley and polar cells'),
        ('polar cell', 'the circulation cell between about 60° and the poles, with sinking cold air at the poles'),
        ('Coriolis effect', 'the apparent deflection of moving air and water caused by the Earth’s rotation: to the right in the Northern Hemisphere and to the left in the Southern'),
        ('pressure gradient', 'the rate of change of pressure over distance, which drives winds from high to low pressure'),
        ('trade winds', 'steady surface winds blowing from the subtropical highs towards the equator: north-east in the Northern Hemisphere and south-east in the Southern'),
        ('jet stream', 'a band of very fast winds in the upper troposphere, near the boundaries of the circulation cells'),
        ('geostrophic wind', 'an upper-air wind blowing parallel to isobars when the pressure gradient force and Coriolis force are balanced'),
    ],
    'mcq': [
        ('Air sinks at about 30° N and S, forming', 'the subtropical high-pressure belts', ['the equatorial low', 'the sub-polar low', 'the ITCZ'], '[1]'),
        ('Surface winds between 30° and 60° in the Southern Hemisphere blow mainly from the', 'north-west', ['north-east', 'south-east', 'south-west'], 'Westerlies are deflected to the left in the Southern Hemisphere. [1]'),
        ('Which of these is a cold ocean current?', 'The Benguela Current', ['The Gulf Stream', 'The Kuroshio Current', 'The Brazil Current'], '[1]'),
        ('Winds are deflected by the Coriolis effect to the', 'right in the Northern Hemisphere', ['left in the Northern Hemisphere', 'right in the Southern Hemisphere', 'east everywhere'], '[1]'),
        ('Ocean gyres in the Northern Hemisphere rotate', 'clockwise', ['anticlockwise', 'from north to south only', 'randomly'], '[1]'),
    ],
    'explain': [
        ('Explain the operation of the Hadley cell.', 'Intense heating at the equator causes air to rise (low pressure, ITCZ); it spreads polewards at high altitude, cools and sinks at about 30° (subtropical high); surface trade winds return air to the equator.', '1 mark each stage [4]'),
        ('Explain why winds do not blow directly from high to low pressure.', 'The Coriolis effect deflects moving air to the right in the Northern Hemisphere and to the left in the Southern; friction near the surface also alters direction.', '1 mark Coriolis; 1 mark direction; 1 mark friction [3]'),
        ('Explain how ocean currents influence the climate of coastal areas.', 'Warm currents raise temperatures and humidity (North Atlantic Drift keeps Norway’s ports ice-free); cold currents cool coasts, stabilise air and reduce rainfall, contributing to deserts (Atacama, Namib) and advection fog.', '1 mark warm; 1 mark cold; 1 mark example [3]'),
        ('Explain why the tri-cellular model is a simplification.', 'Land and sea heating differences, seasonal migration of pressure belts, mountain barriers, jet streams and Rossby waves, and monsoons all disrupt the idealised pattern.', '1 mark per point [3]'),
    ],
    'claims': [
        ('The trade winds blow from west to east.', False, 'They blow from the north-east and south-east towards the equator, i.e. from east to west.'),
        ('The ITCZ is an area of low pressure with rising air and heavy rain.', True, 'Converging trade winds and intense heating produce convection and cumulonimbus clouds.'),
        ('The Coriolis effect is strongest at the equator.', False, 'It is zero at the equator and strongest at the poles.'),
    ],
    'essays': [
        ('the tri-cellular model fully explains global patterns of pressure and winds',
         ['It explains the equatorial low, subtropical highs, mid-latitude westerlies, sub-polar lows and polar highs, and the trade winds.'],
         ['Real patterns are disrupted by continents and oceans (seasonal Asian high and low), relief, ocean currents, jet streams and Rossby waves, monsoons and the seasonal shift of belts with the overhead sun.'],
         'The model explains the broad zonal pattern well but not regional and seasonal variations.',
         ['seasonal migration', 'continentality', 'jet streams', 'monsoons']),
    ],
})

BELTS = [(0, 5, 'equatorial low pressure (ITCZ, doldrums)', 'light, variable winds with rising air', 'light, variable winds with rising air'),
         (6, 29, 'trade wind belt between the equatorial low and subtropical high', 'north-east trade winds', 'south-east trade winds'),
         (30, 34, 'subtropical high pressure', 'calm, sinking air (horse latitudes)', 'calm, sinking air (horse latitudes)'),
         (35, 57, 'mid-latitude westerlies between the subtropical high and sub-polar low', 'south-westerly winds', 'north-westerly winds'),
         (58, 62, 'sub-polar low pressure (polar front)', 'converging, rising air with depressions', 'converging, rising air with depressions'),
         (63, 85, 'polar easterlies between the polar high and sub-polar low', 'north-easterly winds', 'south-easterly winds')]
CURRENTS = [('Gulf Stream', 'warm'), ('North Atlantic Drift', 'warm'), ('Kuroshio Current', 'warm'), ('Brazil Current', 'warm'), ('Agulhas Current', 'warm'), ('East Australian Current', 'warm'),
            ('Canary Current', 'cold'), ('Benguela Current', 'cold'), ('Humboldt (Peru) Current', 'cold'), ('California Current', 'cold'), ('Labrador Current', 'cold'), ('West Australian Current', 'cold')]


@c5b.add('C3', (1, 2, 3, 4, 5), 'short')
def c5b_belt(r, D):
    k = 1 if D <= 2 else 3
    picks = []
    for _ in range(k):
        lo, hi, belt, wn, ws = r.choice(BELTS)
        lat = r.randint(lo, hi)
        hem = r.choice(['N', 'S'])
        picks.append((lat, hem, belt, wn if hem == 'N' else ws))
    if len({(p[0], p[1]) for p in picks}) < k:
        return None
    if k == 1:
        lat, hem, belt, wind = picks[0]
        others = [b[2] for b in BELTS if b[2] != belt]
        opts, a = mcq(r, cap(belt), [cap(o) for o in others])
        return {'stem': f'According to the tri-cellular model, a place at {lat}°{hem} lies in which part of the general circulation?', 'options': opts, 'answer': a, 'key': f'{cap(belt)}; surface winds: {wind}. [1]'}
    stem = 'Using the tri-cellular model, state the expected pressure belt or wind belt and the prevailing surface wind for each location: ' + '; '.join(f'{chr(65 + i)} {lat}°{hem}' for i, (lat, hem, _, _) in enumerate(picks)) + '. Explain one of your answers.'
    return {'stem': stem, 'answer': ' '.join(f'{chr(65 + i)}: {b}; {w}.' for i, (_, _, b, w) in enumerate(picks)) + ' Explanation: e.g. winds blow from high to low pressure and are deflected by the Coriolis effect (right in the north, left in the south).',
            'key': '1 mark per correct location (belt and wind) [3]; 1 mark explanation using pressure gradient and Coriolis [1]; total [4]', 'marks': 4, 'type': 'short'}


@c5b.add('C2', (1, 2, 3), 'short')
def c5b_curr(r, D):
    k = 4 if D <= 2 else 6
    pick = r.sample(CURRENTS, k)
    stem = r.choice(['Classify each ocean current as warm or cold:', 'State whether each of the following ocean currents is warm or cold:']) + ' ' + ', '.join(n for n, _ in pick) + '.'
    if D >= 3:
        stem += ' Explain the effect of one cold current on the climate of the adjacent coast.'
        return {'stem': stem, 'answer': '; '.join(f'{n} {w}' for n, w in pick) + '. Cold currents cool the air above, creating stable conditions, little rain and advection fog (e.g. Benguela and the Namib desert).', 'key': '1 mark per two correct [3]; explanation [2]; total [5]', 'marks': 5, 'type': 'short'}
    return {'stem': stem, 'answer': '; '.join(f'{n} {w}' for n, w in pick), 'key': f'1 mark per two correct [{k // 2}]', 'marks': k // 2, 'type': 'short'}


@data(c5b)
def c5b_pg(r, D):
    p1, p2 = r.randint(1020, 1036), r.randint(990, 1012)
    dist = r.choice([200, 300, 400, 500, 600, 800])
    g = (p1 - p2) / dist * 100
    hem = r.choice(['Northern', 'Southern'])
    stem = f'On a synoptic chart for a region in the {hem} Hemisphere, the centre of a high-pressure system is {p1} hPa and the centre of a low-pressure system {dist} km to the north is {p2} hPa.'
    if D == 1:
        opts, a = mcq(r, f'{dp(g, 1)} hPa per 100 km', [f'{dp(g * 10, 1)} hPa per 100 km', f'{dp((p1 + p2) / dist, 1)} hPa per 100 km', f'{dp(g / 2, 1)} hPa per 100 km', f'{p1 - p2} hPa per 100 km'])
        return {'stem': stem + ' What is the mean pressure gradient?', 'options': opts, 'answer': a, 'key': f'({p1} − {p2}) ÷ {dist} × 100 = {dp(g, 1)} hPa per 100 km. [1]'}
    dirn = 'from the south-west (a south-westerly wind)' if hem == 'Northern' else 'from the south-east (a south-easterly wind)'
    parts = [
        lambda r: ('Calculate the mean pressure gradient in hPa per 100 km.', f'{dp(g, 1)} hPa per 100 km', f'({p1} − {p2}) ÷ {dist} × 100 [2]'),
        lambda r: ('State the general direction from which the surface wind blows between the two systems, and explain why.', f'Air moves from high pressure (south) towards low pressure (north) but is deflected by the Coriolis effect ({"right" if hem == "Northern" else "left"}), so the wind blows {dirn}.', '1 mark direction; 1 mark pressure gradient; 1 mark Coriolis [3]'),
        lambda r: ('Explain how the wind speed would change if the isobars were closer together.', 'A steeper pressure gradient means a greater pressure gradient force, so stronger winds.', '[2]'),
        lambda r: ('Explain why surface winds cross isobars at an angle while upper winds blow parallel to them.', 'Surface friction reduces wind speed and so the Coriolis effect, so the pressure gradient force pulls the wind across isobars towards low pressure; aloft there is no friction (geostrophic balance).', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 5.3 ITCZ and monsoons
c5c = T('Seasonal variations: migration of the ITCZ and monsoons', 'seasonal variations migration of the itcz monsoons')
STATIONS = [
    ('a station in western India (19°N)', [1, 1, 0, 1, 14, 520, 840, 530, 330, 70, 15, 3], [24, 25, 27, 29, 30, 29, 28, 27, 28, 29, 28, 26], 'N'),
    ('a station in northern Nigeria (12°N)', [0, 0, 2, 9, 60, 110, 200, 300, 130, 15, 0, 0], [22, 25, 29, 31, 30, 28, 26, 25, 26, 27, 25, 22], 'N'),
    ('a station in northern Australia (12°S)', [420, 360, 320, 100, 20, 2, 1, 5, 15, 70, 140, 250], [28, 28, 28, 28, 27, 25, 25, 26, 28, 29, 29, 29], 'S'),
    ('a station in central Myanmar (21°N)', [3, 4, 8, 35, 160, 120, 90, 110, 150, 110, 30, 6], [21, 24, 28, 32, 31, 30, 29, 29, 29, 28, 25, 22], 'N'),
    ('a station in Zambia (15°S)', [230, 190, 140, 20, 3, 0, 0, 0, 1, 15, 90, 200], [22, 22, 22, 21, 19, 16, 16, 19, 23, 25, 24, 22], 'S'),
]
B(c5c, {
    'terms': [
        ('Inter-Tropical Convergence Zone (ITCZ)', 'the zone of low pressure where the trade winds converge near the equator, associated with rising air and heavy rain'),
        ('monsoon', 'a seasonal reversal of wind direction that brings a distinct wet season and dry season'),
        ('wet season', 'the part of the year when the ITCZ lies overhead and convectional rain falls'),
        ('thermal equator', 'the line of highest surface temperature around the globe, which moves north and south with the overhead sun'),
        ('south-west monsoon', 'the moist summer wind that blows onto South Asia from the Indian Ocean between June and September'),
        ('subtropical jet stream', 'a strong westerly upper-air wind whose position over South Asia helps control the timing of the monsoon'),
    ],
    'mcq': [
        ('In July the ITCZ over Asia lies at about', '20-25°N', ['the equator', '10°S', '40°N'], 'It moves furthest north over the heated Asian landmass. [1]'),
        ('The South Asian summer monsoon is caused mainly by', 'intense heating of the land creating low pressure that draws in moist air from the Indian Ocean', ['cold air sinking over the Himalaya in summer', 'the ITCZ moving south of the equator', 'cold ocean currents off India'], '[1]'),
        ('A station at 15°S would expect its wet season in', 'December to March', ['June to September', 'April only', 'all months equally'], 'The ITCZ moves south with the overhead sun in the southern summer. [1]'),
        ('Places close to the equator often have two rainfall maxima because', 'the ITCZ passes overhead twice a year', ['two monsoons meet', 'they have two summers caused by ocean currents', 'of the subtropical high'], '[1]'),
    ],
    'explain': [
        ('Explain why the ITCZ moves north and south during the year.', 'It follows the zone of maximum heating, the overhead sun, which migrates between the Tropics of Cancer and Capricorn; its movement is greater over land, which heats and cools faster than the sea.', '1 mark overhead sun; 1 mark land v sea [2]'),
        ('Explain the causes of the winter (north-east) monsoon in South Asia.', 'The land cools, forming high pressure over central Asia; the ITCZ moves south; dry, cool winds blow out from the land, giving a dry season (except south-east India and Sri Lanka, which receive rain from winds crossing the Bay of Bengal).', '1 mark per point [3]'),
        ('Explain why the monsoon is important for people in South Asia.', 'It provides around 70-80% of annual rainfall in much of India; recharges groundwater and reservoirs; essential for rice and kharif crops; but failure causes drought and excessive rain causes floods (e.g. Kerala 2018).', '1 mark per point [3]'),
    ],
    'claims': [
        ('The ITCZ stays over the equator all year.', False, 'It migrates seasonally, following the overhead sun, especially far over continents.'),
        ('A delayed monsoon can cause economic problems in India.', True, 'Farm output, rural incomes and food prices depend on timely monsoon rain.'),
        ('Places further from the equator in the tropics tend to have shorter wet seasons.', True, 'The ITCZ spends less time over them, so the wet season is shorter and rainfall totals lower.'),
    ],
    'essays': [
        ('the movement of the ITCZ is the only cause of seasonal rainfall in tropical areas',
         ['The ITCZ brings convectional rain as it follows the overhead sun, giving wet seasons in savanna and monsoon lands.'],
         ['Land-sea pressure differences and jet streams drive monsoons; relief (Western Ghats, Himalaya) produces orographic rain; tropical cyclones add rain; El Niño alters patterns.'],
         'The ITCZ is the main control, but monsoon pressure systems, relief and cyclones strongly modify seasonal rainfall.',
         ['monsoons', 'relief', 'tropical cyclones', 'El Niño']),
    ],
})


@data(c5c)
def c5c_clim(r, D):
    nm, rain, temp, hem = r.choice(STATIONS)
    rain = [max(0, round(x * r.uniform(0.9, 1.1))) for x in rain]
    tot = sum(rain)
    wet = [i for i in range(12) if rain[i] >= 60]
    wsum = sum(rain[i] for i in wet)
    tr = max(temp) - min(temp)
    stem = f'Table 5.3 shows climate data for {nm}. ' + ' '.join(f'{MON[i]}: {temp[i]} °C, {rain[i]} mm.' for i in range(12))
    if D == 1:
        opts, a = mcq(r, f'{nf(tot)} mm', [f'{nf(round(tot / 12))} mm', f'{nf(max(rain))} mm', f'{nf(tot + 100)} mm', f'{nf(wsum)} mm' if wsum != tot else f'{nf(tot - 150)} mm'])
        return {'stem': stem + ' What is the total annual rainfall?', 'options': opts, 'answer': a, 'key': f'Sum of monthly totals = {nf(tot)} mm. [1]'}
    parts = [
        lambda r: ('Calculate the total annual rainfall.', f'{nf(tot)} mm', 'sum [1]'),
        lambda r: ('Calculate the percentage of annual rainfall that falls in months with at least 60 mm.', f'{dp(wsum / tot * 100)}%', f'{nf(wsum)} ÷ {nf(tot)} × 100 [2]'),
        lambda r: ('Calculate the annual temperature range.', f'{tr} °C', f'{max(temp)} − {min(temp)} [1]'),
        lambda r: ('Explain the seasonal pattern of rainfall.', ('When the overhead sun and the ITCZ move north in the northern summer, convergence, convection and (in South Asia) onshore monsoon winds bring heavy rain; when the ITCZ moves south, dry winds from the subtropical high or the continental interior dominate.' if hem == 'N'
                                                                 else 'In the southern summer (December-March) the ITCZ and monsoon trough move south over the station, bringing convection and heavy rain; in the southern winter the subtropical high and dry south-east trade winds dominate.'), '1 mark ITCZ movement; 1 mark wet season; 1 mark dry season [3]'),
        lambda r: ('Suggest why the hottest month is not in the middle of the wet season.', 'Cloud cover and rain in the wet season reduce insolation and evaporation cools the surface, so temperatures peak just before the rains.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[5] = [c5a, c5b, c5c]


# ============================================================== CHAPTER 6: Weather processes and human impact

c6a = T('Atmospheric moisture: humidity, lapse rates and atmospheric stability', 'atmospheric moisture humidity lapse rates atmospheric stability')
B(c6a, {
    'terms': [
        ('environmental lapse rate (ELR)', 'the actual rate at which temperature falls with height in the atmosphere at a given time and place, on average about 6.5 °C per 1000 m'),
        ('dry adiabatic lapse rate (DALR)', 'the rate at which unsaturated rising air cools by expansion, about 10 °C per 1000 m'),
        ('saturated adiabatic lapse rate (SALR)', 'the rate at which saturated rising air cools, about 4-9 °C per 1000 m, slower because latent heat is released by condensation'),
        ('absolute stability', 'when the ELR is less than the SALR, so a rising parcel is always cooler than its surroundings and sinks back'),
        ('absolute instability', 'when the ELR is greater than the DALR, so a rising parcel stays warmer than its surroundings and keeps rising'),
        ('conditional instability', 'when the ELR lies between the SALR and DALR, so air becomes unstable only once it is saturated'),
        ('relative humidity', 'the amount of water vapour in the air as a percentage of the maximum it could hold at that temperature'),
        ('absolute humidity', 'the mass of water vapour in a given volume of air, in g/m³'),
        ('condensation level', 'the height at which rising air cools to its dew point and cloud begins to form'),
    ],
    'mcq': [
        ('The SALR is lower than the DALR because', 'latent heat is released as water vapour condenses', ['saturated air is denser', 'saturated air expands faster', 'clouds reflect sunlight'], '[1]'),
        ('If the ELR is 12 °C per 1000 m, the atmosphere is', 'absolutely unstable', ['absolutely stable', 'conditionally unstable', 'in an inversion'], 'ELR > DALR (about 10 °C/km). [1]'),
        ('Air at 20 °C holds 8.7 g/m³ of water vapour and could hold 17.3 g/m³. Its relative humidity is about', '50%', ['87%', '20%', '200%'], '8.7 ÷ 17.3 × 100 ≈ 50%. [1]'),
        ('Cumulonimbus clouds are most associated with', 'unstable air', ['stable air', 'temperature inversions', 'anticyclonic subsidence'], '[1]'),
    ],
    'explain': [
        ('Explain why rising air cools.', 'Pressure falls with height, so rising air expands; expansion uses energy, so the air cools adiabatically (without heat exchange with its surroundings).', '1 mark expansion; 1 mark energy/adiabatic [2]'),
        ('Explain conditional instability.', 'The ELR lies between the SALR and DALR; unsaturated rising air cools at the DALR and is cooler than its surroundings (stable); once condensation occurs it cools at the slower SALR and may become warmer than the surroundings, so it continues to rise (unstable).', '1 mark definition; 1 mark below condensation; 1 mark above [3]'),
        ('Explain how relative humidity changes during a clear day if absolute humidity stays constant.', 'As temperature rises the air can hold more vapour, so relative humidity falls; at night cooling raises relative humidity, possibly to 100% (dew or fog).', '[2]'),
        ('Explain the weather associated with stable air.', 'Rising air is suppressed: few clouds or layered stratus, little precipitation, possible fog and inversions, pollution trapped.', '1 mark per point [3]'),
    ],
    'claims': [
        ('The DALR changes from day to day.', False, 'The DALR is fixed (about 10 °C/km); it is the ELR that varies.'),
        ('Unstable air often produces towering cumulus clouds and showers.', True, 'Air keeps rising and cooling, condensing to form deep convective cloud.'),
        ('Relative humidity can be 100% without rain falling.', True, 'Saturated air may produce fog or cloud but droplets must grow large enough to fall.'),
    ],
    'essays': [
        ('atmospheric stability is the most important factor in determining the type of precipitation an area receives',
         ['Unstable air produces convective showers, thunderstorms and hail; stable air gives drizzle, fog and dry weather.'],
         ['Temperature (rain, snow or hail), moisture supply, uplift mechanisms (relief, fronts, convergence), condensation nuclei and cloud processes also matter.'],
         'Stability controls whether air rises far enough to give heavy precipitation, but moisture and temperature control the amount and form.',
         ['lapse rates', 'uplift', 'moisture', 'temperature']),
    ],
})


@data(c6a)
def c6a_parcel(r, D):
    T0 = r.randint(16, 30)
    Td = T0 - r.randint(4, 12)
    H = r.choice([2000, 2500, 3000, 3500])
    LCL = (T0 - Td) * 100
    if LCL >= H:
        return None
    salr = r.choice([5, 6, 7])
    Tl = T0 - 10 * LCL / 1000
    Ts = Tl - salr * (H - LCL) / 1000
    Tlee = Ts + 10 * H / 1000
    elr = r.choice([4, 6.5, 8, 11])
    Tenv = T0 - elr * H / 1000
    stab = 'absolutely stable' if elr < salr else 'conditionally unstable' if elr < 10 else 'absolutely unstable'
    stem = (f'Air at sea level with a temperature of {T0} °C and a dew point of {Td} °C is forced to rise over a mountain range {nf(H)} m high, then descends to sea level on the other side. '
            f'Assume a DALR of 10 °C per 1000 m, a SALR of {salr} °C per 1000 m, that condensation begins when the air has cooled to {Td} °C, and that all moisture is lost as precipitation on the windward side.')
    if D == 1:
        opts, a = mcq(r, f'{nf(LCL)} m', [f'{nf(LCL * 2)} m', f'{nf(round(LCL / 2))} m', f'{nf(Td * 100)} m', f'{nf(LCL + 500)} m'])
        return {'stem': stem + ' At what height does condensation begin?', 'options': opts, 'answer': a, 'key': f'cooling needed {T0 - Td} °C at 10 °C/1000 m = {nf(LCL)} m. [1]'}
    parts = [
        lambda r: ('Calculate the height of the condensation level.', f'{nf(LCL)} m', f'({T0} − {Td}) ÷ 10 × 1000 = {nf(LCL)} m [2]'),
        lambda r: ('Calculate the temperature of the air at the summit.', f'{dp(Ts)} °C', f'{T0} − 10 × {dp(LCL / 1000, 2)} = {dp(Tl)} °C at condensation level; then − {salr} × {dp((H - LCL) / 1000, 2)} = {dp(Ts)} °C [2]'),
        lambda r: ('Calculate the temperature of the air when it reaches sea level on the leeward side.', f'{dp(Tlee)} °C', f'descends dry at the DALR: {dp(Ts)} + 10 × {dp(H / 1000, 2)} = {dp(Tlee)} °C [2]'),
        lambda r: ('Explain why the air is warmer on the leeward side than at the same height on the windward side.', 'On the windward side, above the condensation level, air cooled at the slower SALR because latent heat was released; descending air warms at the faster DALR; this is the föhn effect.', '1 mark SALR/latent heat; 1 mark DALR descent; 1 mark föhn [3]'),
        lambda r: (f'On another day the ELR is {fmt(elr, 1)} °C per 1000 m. State the stability of the atmosphere and give a reason.', f'{cap(stab)}: the ELR is ' + ('less than the SALR, so rising air is always cooler than its surroundings.' if elr < salr else 'between the SALR and DALR, so air becomes unstable only after condensation.' if elr < 10 else 'greater than the DALR, so rising air is always warmer than its surroundings.'), '1 mark state; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


SATV = {0: 4.8, 5: 6.8, 10: 9.4, 15: 12.8, 20: 17.3, 25: 23.0, 30: 30.4, 35: 39.6}


@data(c6a)
def c6a_rh(r, D):
    temps = sorted(SATV)
    Tn = r.choice(temps[2:])
    ah = round(r.uniform(0.3, 0.95) * SATV[Tn], 1)
    rh = ah / SATV[Tn] * 100
    dew = max(t for t in temps if SATV[t] <= ah) if any(SATV[t] <= ah for t in temps) else None
    tab = ', '.join(f'{t} °C: {SATV[t]} g/m³' for t in temps)
    stem = f'Table 6.1 gives the maximum water vapour content (g/m³) of air at different temperatures: {tab}. At {city(r)} at midday the air temperature is {Tn} °C and the absolute humidity is {fmt(ah, 1)} g/m³.'
    if D == 1:
        opts, a = mcq(r, f'{dp(rh, 0)}%', [f'{dp(100 - rh, 0)}%', f'{dp(ah, 0)}%', f'{dp(SATV[Tn] / ah * 100, 0)}%', f'{dp(min(99, rh + 15), 0)}%'])
        return {'stem': stem + ' What is the relative humidity?', 'options': opts, 'answer': a, 'key': f'{fmt(ah, 1)} ÷ {SATV[Tn]} × 100 = {dp(rh, 0)}%. [1]'}
    parts = [
        lambda r: ('Calculate the relative humidity.', f'{dp(rh, 1)}%', f'{fmt(ah, 1)} ÷ {SATV[Tn]} × 100 [2]'),
        lambda r: ('Use the table to estimate the dew point of this air.', f'between {dew} and {dew + 5} °C' if dew is not None else 'below 0 °C', 'temperature at which maximum content equals the actual content [1]'),
        lambda r: ('Explain what would happen to the relative humidity if the air cooled overnight without any change in its moisture content.', 'Relative humidity would rise because cooler air can hold less vapour; at the dew point it reaches 100% and dew, fog or frost may form.', '[2]'),
        lambda r: ('Suggest why relative humidity is often higher in the early morning than in the afternoon.', 'Temperatures are lowest at dawn, so saturation vapour content is lowest and RH highest.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 6.2 precipitation
c6b = T('Precipitation processes and forms: rain, hail, snow and dew', 'precipitation processes forms rain hail snow dew')
B(c6b, {
    'terms': [
        ('Bergeron-Findeisen process', 'the growth of ice crystals at the expense of supercooled water droplets in clouds below 0 °C, producing precipitation'),
        ('collision-coalescence', 'the growth of raindrops in warm clouds as droplets collide and merge'),
        ('supercooled water', 'water droplets that remain liquid at temperatures below 0 °C'),
        ('condensation nuclei', 'tiny particles such as dust, salt or smoke on which water vapour condenses'),
        ('hail', 'balls of ice formed in cumulonimbus clouds as ice pellets are carried up and down by strong updraughts, gaining layers of ice'),
        ('dew', 'water droplets that condense directly on cold surfaces when air near the ground cools to its dew point'),
        ('orographic precipitation', 'precipitation caused when air is forced to rise over high ground'),
        ('rime', 'ice formed when supercooled fog droplets freeze on contact with cold surfaces'),
    ],
    'mcq': [
        ('Hailstones show concentric layers of ice because', 'they are carried up and down repeatedly by strong updraughts in a cumulonimbus cloud', ['they melt and refreeze on the ground', 'they form on cold surfaces like dew', 'they grow by condensation on salt particles'], '[1]'),
        ('In tropical (warm) clouds, raindrops grow mainly by', 'collision and coalescence', ['the Bergeron process', 'sublimation', 'freezing'], '[1]'),
        ('Snow reaches the ground as snow rather than rain when', 'the air between the cloud base and the ground is at or below about 2 °C', ['the cloud is very thin', 'the air is unstable and warm', 'the dew point is above 10 °C'], '[1]'),
        ('Dew forms most readily on', 'clear, calm nights with moist air', ['cloudy, windy nights', 'hot afternoons', 'days with strong sunshine'], '[1]'),
    ],
    'explain': [
        ('Explain the Bergeron-Findeisen process of precipitation formation.', 'In clouds between about 0 and −40 °C, ice crystals and supercooled droplets coexist; saturation vapour pressure is lower over ice, so vapour deposits on ice crystals, which grow at the expense of droplets, become heavy and fall, melting to rain if the air below is warm.', '1 mark coexistence; 1 mark vapour pressure; 1 mark growth and fall [3]'),
        ('Explain the formation of hail.', 'In tall cumulonimbus clouds strong updraughts carry ice pellets repeatedly through layers of supercooled water, adding layers of ice until they are too heavy to be held up.', '1 mark updraughts; 1 mark layers; 1 mark fall [3]'),
        ('Explain why condensation nuclei are needed for clouds to form.', 'Pure air would need to be supersaturated for droplets to form; nuclei provide surfaces for vapour to condense onto at about 100% relative humidity.', '[2]'),
        ('Explain the three main causes of uplift that lead to precipitation.', 'Convectional (surface heating causes air to rise), orographic (air forced over mountains), frontal/cyclonic (warm air rises over cold air at fronts or converges in depressions).', '1 mark each [3]'),
    ],
    'claims': [
        ('All rain begins as ice crystals.', False, 'In the tropics much rain forms in warm clouds by collision and coalescence.'),
        ('Dew is a form of precipitation that falls from clouds.', False, 'Dew forms by condensation directly on surfaces; it does not fall from clouds.'),
        ('Hail is most common in summer thunderstorms.', True, 'Strong convection is needed to produce the updraughts that keep hailstones in the cloud.'),
    ],
    'essays': [
        ('the type of uplift is more important than temperature in determining the form of precipitation',
         ['Strong convective uplift creates cumulonimbus with hail; gentle frontal uplift gives steady rain or drizzle; orographic uplift gives persistent rain.'],
         ['Temperature decides whether precipitation falls as rain, snow, sleet or hail; ice-crystal processes need sub-zero cloud tops; dew and rime depend on surface temperature.'],
         'Uplift controls the intensity and type of cloud, but temperature through the cloud and below it decides the form that reaches the ground.',
         ['convection', 'fronts', 'freezing level', 'dew and rime']),
    ],
})


@data(c6b, c4=False)
def c6b_wind(r, D):
    stns = [('windward coast (0 m)', 0), ('windward slope (800 m)', 800), ('summit (1500 m)', 1500), ('leeward slope (800 m)', 800), ('leeward lowland (100 m)', 100)]
    base = r.randint(900, 1500)
    rain = [base, round(base * r.uniform(1.6, 2.2)), round(base * r.uniform(2.0, 2.6)), round(base * r.uniform(0.4, 0.6)), round(base * r.uniform(0.2, 0.35))]
    reg = r.choice(['the Western Ghats, India', 'the Southern Alps, New Zealand', 'the Andes in southern Chile', 'the Cameroon Highlands'])
    stem = f'Table 6.2 shows mean annual precipitation (mm) along a transect across {reg}, in the direction of the prevailing wind: ' + ', '.join(f'{n} {nf(v)}' for (n, _), v in zip(stns, rain)) + '.'
    ratio = rain[2] / rain[4]
    if D == 1:
        opts, a = mcq(r, f'{dp(ratio)} times', [f'{dp(rain[2] / rain[0])} times', f'{dp(rain[4] / rain[2], 2)} times', f'{dp(ratio + 2)} times', f'{dp(ratio / 2)} times'])
        return {'stem': stem + ' How many times more precipitation does the summit receive than the leeward lowland?', 'options': opts, 'answer': a, 'key': f'{nf(rain[2])} ÷ {nf(rain[4])} = {dp(ratio)}. [1]'}
    parts = [
        lambda r: ('Calculate the percentage decrease in precipitation from the summit to the leeward lowland.', f'{dp((rain[2] - rain[4]) / rain[2] * 100)}%', f'({nf(rain[2])} − {nf(rain[4])}) ÷ {nf(rain[2])} × 100 [2]'),
        lambda r: ('Explain the increase in precipitation up the windward slope.', 'Moist air is forced to rise (orographic uplift), cools adiabatically to dew point, condenses into cloud and rain; uplift may trigger instability.', '1 mark per stage [3]'),
        lambda r: ('Explain why the leeward side is much drier.', 'Air has lost much moisture on the windward side; descending air warms adiabatically at the DALR, so relative humidity falls and clouds evaporate (rain shadow).', '1 mark moisture lost; 1 mark descending warming [2]'),
        lambda r: ('State one way in which the precipitation might be measured accurately at these sites.', 'Standard rain gauges sunk into the ground, away from buildings and trees, read at the same time each day; automatic tipping-bucket gauges.', '[1]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 6.3 enhanced greenhouse effect
c6c = T('Human impact on the atmosphere: the enhanced greenhouse effect and global warming', 'enhanced greenhouse effect global warming')
CO2 = [(1960, 316.9), (1970, 325.7), (1980, 338.8), (1990, 354.4), (2000, 369.7), (2010, 389.9), (2020, 414.2), (2023, 421.1)]
B(c6c, {
    'terms': [
        ('greenhouse effect', 'the natural warming of the Earth’s surface by gases that absorb and re-emit long-wave radiation'),
        ('enhanced greenhouse effect', 'the increase in the greenhouse effect caused by human emissions of greenhouse gases, leading to global warming'),
        ('greenhouse gas', 'a gas such as carbon dioxide, methane or nitrous oxide that absorbs long-wave radiation'),
        ('carbon sink', 'a store that absorbs more carbon than it releases, such as forests, soils and oceans'),
        ('positive feedback', 'a process that amplifies an initial change, for example melting ice lowering albedo and causing more warming'),
        ('mitigation', 'actions to reduce greenhouse gas emissions or increase carbon sinks to limit climate change'),
        ('adaptation', 'actions that reduce the harm caused by climate change, such as flood defences or drought-resistant crops'),
    ],
    'mcq': [
        ('The concentration of carbon dioxide in the atmosphere before the Industrial Revolution was about', '280 ppm', ['180 ppm', '420 ppm', '1000 ppm'], 'It passed 420 ppm in 2023. [1]'),
        ('Which greenhouse gas is released in large amounts by rice paddies and cattle?', 'Methane', ['Carbon dioxide only', 'Ozone', 'Nitrogen'], '[1]'),
        ('The 2015 Paris Agreement aims to limit global warming to', 'well below 2 °C above pre-industrial levels, pursuing 1.5 °C', ['0.5 °C', '4 °C', '10 °C'], '[1]'),
        ('Which of the following is an example of positive feedback in the climate system?', 'Thawing permafrost releasing methane, causing more warming', ['Increased cloud reflecting more sunlight', 'Forests absorbing more CO₂', 'Volcanic ash cooling the climate'], '[1]'),
    ],
    'explain': [
        ('Explain how the enhanced greenhouse effect leads to global warming.', 'Burning fossil fuels, deforestation and agriculture increase concentrations of CO₂, methane and nitrous oxide; these absorb more outgoing long-wave radiation and re-emit it towards the surface, raising mean temperatures.', '1 mark sources; 1 mark absorption; 1 mark re-emission/warming [3]'),
        ('Explain two possible impacts of global warming on people.', 'Sea-level rise threatening coastal cities and deltas (Bangladesh, Maldives); more intense droughts, heatwaves and floods; changing crop yields; spread of diseases such as malaria; loss of glaciers that supply water.', '1 mark impact; 1 mark development each [4]'),
        ('Explain why it is difficult to predict future global temperatures.', 'Uncertain future emissions (economic growth, policies); complex feedbacks (clouds, ice, permafrost); natural variability (El Niño, volcanoes); limitations of climate models.', '1 mark per point [3]'),
    ],
    'claims': [
        ('The greenhouse effect is entirely caused by human activity.', False, 'The natural greenhouse effect keeps the Earth about 33 °C warmer than it would be; humans have enhanced it.'),
        ('Global warming may cause some places to become colder or wetter.', True, 'Changes in circulation and ocean currents produce regional variations, not uniform warming.'),
        ('Deforestation contributes to the enhanced greenhouse effect.', True, 'Burning and decay release stored carbon and remove a carbon sink.'),
    ],
    'essays': [
        ('the effects of global warming will be felt most severely by people in low-income countries',
         ['LICs depend on rain-fed farming; low-lying deltas (Bangladesh) and small islands (Tuvalu, Maldives) face sea-level rise; less money for adaptation; heat stress; health systems weak.'],
         ['HICs also face wildfires (Australia, California), heatwaves (Europe 2003, 2022) and coastal flooding; some high-latitude areas may benefit from longer growing seasons; vulnerability varies within countries.'],
         'Impacts are global, but poverty, dependence on agriculture and limited adaptive capacity mean the poorest people are most severely affected.',
         ['sea-level rise', 'agriculture', 'adaptation', 'vulnerability']),
    ],
})


@data(c6c)
def c6c_co2(r, D):
    rows = CO2[:]
    a, b = sorted(r.sample(range(len(rows)), 2))
    (y1, c1), (y2, c2) = rows[a], rows[b]
    rate = (c2 - c1) / (y2 - y1)
    pc = pct_change(280, rows[-1][1])
    stem = 'Fig. 6.3 shows the annual mean concentration of carbon dioxide at Mauna Loa, Hawaii (ppm): ' + ', '.join(f'{y}: {fmt(c, 1)}' for y, c in rows) + '. The pre-industrial concentration was about 280 ppm.'
    if D == 1:
        opts, ans = mcq(r, f'{dp(rate, 2)} ppm per year', [f'{dp(c2 - c1, 1)} ppm per year', f'{dp(rate * 10, 2)} ppm per year', f'{dp(rate / 2, 2)} ppm per year', f'{dp(rate + 1, 2)} ppm per year'])
        return {'stem': stem + f' What was the mean rate of increase between {y1} and {y2}?', 'options': opts, 'answer': ans, 'key': f'({fmt(c2, 1)} − {fmt(c1, 1)}) ÷ {y2 - y1} = {dp(rate, 2)} ppm per year. [1]'}
    r1 = (CO2[3][1] - CO2[0][1]) / 30
    r2 = (CO2[6][1] - CO2[3][1]) / 30
    parts = [
        lambda r: (f'Calculate the mean annual rate of increase between {y1} and {y2}.', f'{dp(rate, 2)} ppm per year', f'({fmt(c2, 1)} − {fmt(c1, 1)}) ÷ {y2 - y1} [2]'),
        lambda r: ('Calculate the percentage increase in CO₂ between pre-industrial times and 2023.', f'{dp(pc)}%', f'(421.1 − 280) ÷ 280 × 100 [2]'),
        lambda r: ('Compare the rate of increase in 1960-1990 with that in 1990-2020.', f'1960-1990: {dp(r1, 2)} ppm/yr; 1990-2020: {dp(r2, 2)} ppm/yr; the rate has accelerated.', '1 mark each rate; 1 mark comparison [3]'),
        lambda r: ('Explain why the concentration has continued to rise despite international agreements.', 'Emissions from rapidly industrialising countries, rising energy demand, continued dependence on coal, oil and gas, deforestation; CO₂ remains in the atmosphere for a long time.', '1 mark per point [3]'),
        lambda r: ('Explain why a seasonal rise and fall is seen within each year at Mauna Loa.', 'Northern Hemisphere vegetation absorbs CO₂ by photosynthesis in summer and releases it by decay in winter.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[6] = [c6a, c6b, c6c]


# ============================================================== CHAPTER 7: Elementary plate tectonics

c7a = T('Plate boundaries and associated landforms: ridges, trenches, fold mountains and island arcs', 'plate boundaries landforms ridges trenches fold mountains island arcs')
B(c7a, {
    'terms': [
        ('constructive (divergent) boundary', 'a plate boundary where plates move apart and new crust is formed'),
        ('destructive (convergent) boundary', 'a plate boundary where plates move towards each other and one may be subducted'),
        ('conservative (transform) boundary', 'a plate boundary where plates slide past each other and crust is neither created nor destroyed'),
        ('ocean trench', 'a long, deep, narrow depression in the ocean floor where an oceanic plate is subducted'),
        ('island arc', 'a curved chain of volcanic islands formed where one oceanic plate is subducted beneath another'),
        ('fold mountains', 'mountain ranges formed when sediments are compressed and folded at a convergent boundary'),
        ('mid-ocean ridge', 'a submarine mountain chain at a constructive boundary, with a central rift valley'),
        ('rift valley', 'a valley formed where crust is stretched and a central block drops down between parallel faults'),
    ],
    'mcq': [
        ('The Mariana Trench is associated with', 'oceanic-oceanic subduction', ['continental-continental collision', 'a constructive boundary', 'a hot spot'], 'The Pacific Plate is subducted beneath the Philippine Sea Plate. [1]'),
        ('The Himalaya were formed by', 'the collision of the Indian and Eurasian plates', ['subduction of the Pacific Plate', 'the separation of Africa and Arabia', 'a hot spot under Nepal'], '[1]'),
        ('Which landform is found at a constructive boundary between two continental plates?', 'A rift valley, such as the East African Rift', ['An ocean trench', 'An island arc', 'Young fold mountains'], '[1]'),
        ('The San Andreas Fault is an example of', 'a conservative (transform) boundary', ['a constructive boundary', 'a collision boundary', 'a subduction zone'], '[1]'),
        ('The Andes are an example of', 'fold mountains with volcanoes formed by oceanic-continental subduction', ['an island arc', 'a mid-ocean ridge', 'a rift valley'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of an island arc.', 'Where two oceanic plates converge, the older, denser plate is subducted; it melts as it descends into the mantle (helped by water released from the slab); magma rises to form a curved chain of volcanic islands parallel to the trench, e.g. Japan, the Aleutians, the Mariana Islands.', '1 mark subduction; 1 mark melting; 1 mark volcanoes; 1 mark example [4]'),
        ('Explain the formation of fold mountains at an oceanic-continental boundary.', 'Denser oceanic plate is subducted beneath continental plate; sediments in the geosyncline/accretionary wedge are compressed, folded and uplifted; magma from melting slab forms volcanoes (e.g. Andes).', '1 mark per stage [3]'),
        ('Explain why there are no volcanoes at continental-continental collision zones.', 'Both plates have similar low density, so neither is subducted far into the mantle; no melting slab means little magma; crust thickens and is uplifted instead.', '[2]'),
        ('Explain the formation of a mid-ocean ridge.', 'Plates diverge; pressure is released and mantle rock partially melts; basaltic magma rises and erupts, forming new crust; the hot, less dense lithosphere stands high to form a ridge with a central rift.', '1 mark per point [3]'),
    ],
    'claims': [
        ('Ocean trenches are found at constructive plate boundaries.', False, 'Trenches mark subduction at destructive boundaries; constructive boundaries have ridges.'),
        ('Iceland is above sea level because a hot spot coincides with the Mid-Atlantic Ridge.', True, 'Extra volcanic output from the plume has built up the ridge above sea level.'),
        ('Fold mountains continue to rise today in some places.', True, 'The Himalaya are still rising by a few millimetres a year as India pushes north.'),
    ],
    'essays': [
        ('destructive plate boundaries produce a greater variety of landforms than constructive plate boundaries',
         ['Destructive boundaries produce trenches, island arcs (Japan), fold mountains (Andes, Himalaya), composite volcanoes and plateaux.'],
         ['Constructive boundaries produce mid-ocean ridges, transform faults, rift valleys (East Africa), shield volcanoes, fissure eruptions and new oceans (Red Sea).'],
         'Destructive boundaries have a slightly wider range because they include three types of convergence, but constructive boundaries create the most extensive landform (the ridge system).',
         ['ridges and rifts', 'trenches', 'island arcs', 'fold mountains']),
    ],
})

BOUNDS = [('Mid-Atlantic Ridge (Iceland)', 'constructive', 'mid-ocean ridge, fissure eruptions and a rift valley (Thingvellir)'), ('East African Rift', 'constructive', 'rift valley with volcanoes such as Kilimanjaro'),
          ('Andes (Nazca and South American plates)', 'destructive (oceanic-continental)', 'Peru-Chile trench, fold mountains and composite volcanoes'),
          ('Japan (Pacific and Eurasian/Philippine plates)', 'destructive (oceanic-oceanic and oceanic-continental)', 'Japan Trench and an island arc'),
          ('Himalaya (Indian and Eurasian plates)', 'collision (continental-continental)', 'young fold mountains and the Tibetan Plateau'),
          ('San Andreas Fault (Pacific and North American plates)', 'conservative', 'transform fault with offset streams and fault scarps'),
          ('Mariana Islands (Pacific and Philippine Sea plates)', 'destructive (oceanic-oceanic)', 'Mariana Trench and a volcanic island arc'),
          ('Red Sea (African and Arabian plates)', 'constructive', 'a young ocean formed by rifting'), ('Alps (African and Eurasian plates)', 'collision (continental-continental)', 'fold mountains with nappes')]


@c7a.add('C3', (1, 2, 3, 4), 'short')
def c7a_classify(r, D):
    if D <= 2:
        nm, kind, lf = r.choice(BOUNDS)
        opts, a = mcq(r, cap(kind), [cap(k) for k in ['constructive', 'destructive (oceanic-continental)', 'collision (continental-continental)', 'conservative', 'destructive (oceanic-oceanic)'] if k != kind and not (kind.startswith('destructive (oceanic-oceanic and') and k.startswith('destructive'))])
        return {'stem': f'Which type of plate boundary is found at the {nm}?', 'options': opts, 'answer': a, 'key': f'{cap(kind)}: {lf}. [1]'}
    pick = r.sample(BOUNDS, 3)
    stem = 'For each location, identify the type of plate boundary and name one landform found there: ' + '; '.join(f'{chr(65 + i)} {n}' for i, (n, _, _) in enumerate(pick)) + '.'
    return {'stem': stem, 'answer': ' '.join(f'{chr(65 + i)}: {k}; {lf}.' for i, (_, k, lf) in enumerate(pick)), 'key': '1 mark each boundary, 1 mark each landform [6]', 'marks': 6, 'type': 'short'}


@data(c7a, c4=False)
def c7a_conv(r, D):
    rate = r.randint(2, 9)  # cm per year
    yrs = r.choice([1, 5, 10, 20])  # million years
    dist = rate * yrs * 1e6 / 1e5  # km
    pair = r.choice(['the Nazca Plate beneath South America', 'the Pacific Plate beneath Japan', 'the Indian Plate into Eurasia', 'the Cocos Plate beneath Central America'])
    stem = f'GPS measurements show that {pair} is converging at about {rate} cm per year.'
    if D == 1:
        opts, a = mcq(r, f'{nf(int(dist))} km', [f'{nf(int(dist * 10))} km', f'{nf(int(dist / 10))} km', f'{nf(int(dist * 100))} km', f'{nf(rate * yrs)} km'])
        return {'stem': stem + f' How far would the plates converge in {yrs} million years at this rate?', 'options': opts, 'answer': a, 'key': f'{rate} cm × {yrs} 000 000 = {nf(int(rate * yrs * 1e6))} cm = {nf(int(dist))} km. [1]'}
    parts = [
        lambda r: (f'Calculate how far the plates would converge in {yrs} million years.', f'{nf(int(dist))} km', f'{rate} × {nf(yrs * 1000000)} cm ÷ 100 000 [2]'),
        lambda r: ('Name the landform found where the oceanic plate begins to descend.', 'An ocean trench' if 'Indian' not in pair else 'None: this is a collision zone, so there is no trench; fold mountains form.', '[1]'),
        lambda r: ('Explain why earthquakes occur at a range of depths at this boundary.' if 'Indian' not in pair else 'Explain why earthquakes here are mostly shallow.',
                   'Friction as the slab descends causes earthquakes from shallow depths near the trench to over 600 km deep along the Benioff zone.' if 'Indian' not in pair else 'Neither plate is subducted deeply, so stress builds up in the thickened crust and is released by shallow earthquakes (e.g. Nepal 2015).', '[2]'),
        lambda r: ('Explain how the rate of plate movement is measured.', 'GPS receivers fixed to the ground measure changes in position over years; also dating sea-floor rocks and magnetic stripes.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 7.2 sea-floor spreading
c7b = T('Sea-floor spreading, subduction and evidence for plate movement', 'sea-floor spreading subduction evidence for plate movement')
B(c7b, {
    'terms': [
        ('sea-floor spreading', 'the creation of new oceanic crust at mid-ocean ridges and its movement away from the ridge'),
        ('subduction', 'the sinking of a denser oceanic plate beneath another plate into the mantle'),
        ('palaeomagnetism', 'the record of the Earth’s past magnetic field preserved in rocks as they cool'),
        ('magnetic striping', 'symmetrical bands of normal and reversed magnetism in oceanic crust either side of a mid-ocean ridge'),
        ('Benioff zone', 'the inclined zone of earthquakes along a subducting plate'),
        ('mantle convection', 'the slow circulation of heat in the mantle, once thought to be the main driver of plate movement'),
        ('slab pull', 'the force exerted by a cold, dense subducting plate pulling the rest of the plate after it'),
        ('ridge push', 'the force created as newly formed, elevated lithosphere at a ridge slides away from it under gravity'),
    ],
    'mcq': [
        ('The age of oceanic crust', 'increases with distance from the mid-ocean ridge', ['decreases with distance from the ridge', 'is the same everywhere', 'is greatest at the ridge'], '[1]'),
        ('Magnetic stripes on the ocean floor are evidence of', 'reversals of the Earth’s magnetic field recorded in new crust at ridges', ['meteorite impacts', 'ancient coral reefs', 'glaciation'], '[1]'),
        ('The oldest oceanic crust is about', '180-200 million years old', ['4 billion years old', '10 000 years old', '1 billion years old'], 'Older crust has been subducted. [1]'),
        ('Which force is now thought to be the most important driver of plate motion?', 'Slab pull', ['Tidal forces', 'Earth’s magnetic field', 'Wind stress'], '[1]'),
    ],
    'explain': [
        ('Explain how palaeomagnetism provides evidence for sea-floor spreading.', 'As basalt cools at the ridge, iron minerals align with the magnetic field; the field reverses periodically; stripes of normal and reversed polarity are symmetrical either side of the ridge, showing crust forms at the ridge and moves outwards.', '1 mark alignment; 1 mark reversals; 1 mark symmetry [3]'),
        ('Explain why oceanic crust is subducted but continental crust is not.', 'Oceanic crust is basaltic and denser (about 3.0 g/cm³) than granitic continental crust (about 2.7 g/cm³), and becomes colder and denser with age.', '[2]'),
        ('Outline the evidence that continents have moved.', 'Fit of continents (South America and Africa); matching rock types and mountain belts; fossils (Mesosaurus, Glossopteris); glacial deposits in now-tropical areas; palaeomagnetism.', '1 mark each [4]'),
        ('Explain the processes that drive plate movement.', 'Slab pull by dense subducting plates; ridge push from elevated ridges; mantle convection currents and plumes driven by heat from the core and radioactive decay.', '1 mark each [3]'),
    ],
    'claims': [
        ('The Atlantic Ocean is getting wider.', True, 'Sea-floor spreading at the Mid-Atlantic Ridge moves the Americas away from Europe and Africa by about 2-5 cm a year.'),
        ('The oldest rocks on Earth are found in the ocean floor.', False, 'Oceanic crust is less than about 200 million years old because it is recycled; the oldest rocks are in continental shields.'),
        ('Wegener’s theory of continental drift was accepted immediately.', False, 'He could not explain the mechanism; acceptance came with evidence of sea-floor spreading in the 1960s.'),
    ],
    'essays': [
        ('palaeomagnetism provides the strongest evidence for the theory of plate tectonics',
         ['Symmetrical magnetic stripes prove sea-floor spreading and allow rates to be calculated; apparent polar wander curves show continents moved.'],
         ['Other evidence: age of sea-floor sediments, distribution of earthquakes and volcanoes along boundaries, Benioff zones, GPS measurements of plate motion today, fossils and rock matching.'],
         'Palaeomagnetism was decisive historically, but modern GPS gives the most direct proof, and the theory rests on the combined evidence.',
         ['magnetic stripes', 'GPS', 'earthquake distribution', 'fossils']),
    ],
})


@data(c7b)
def c7b_spread(r, D):
    rows = []
    rate = r.choice([1.2, 2.0, 2.5, 3.5, 5.0, 8.0])  # half rate cm/yr
    ridge = {1.2: 'the Mid-Atlantic Ridge near Iceland', 2.0: 'the Mid-Atlantic Ridge', 2.5: 'the Mid-Atlantic Ridge', 3.5: 'the Carlsberg Ridge (Indian Ocean)', 5.0: 'the East Pacific Rise', 8.0: 'the East Pacific Rise'}[rate]
    for d in sorted(r.sample(range(50, 900, 50), 4)):
        age = d * 1e5 / rate / 1e6
        rows.append((d, round(age, 1)))
    stem = f'Table 7.2 shows the age of basalt samples at different distances from {ridge}: ' + ', '.join(f'{d} km: {fmt(a, 1)} million years' for d, a in rows) + '.'
    d, a = rows[-1]
    v = d * 1e5 / (a * 1e6)
    if D == 1:
        opts, ans = mcq(r, f'{dp(v, 1)} cm per year', [f'{dp(v * 10, 1)} cm per year', f'{dp(v / 10, 2)} cm per year', f'{dp(v * 2, 1)} cm per year', f'{dp(d / a, 1)} cm per year' if abs(d / a - v) > 0.1 else f'{dp(v + 1.5, 1)} cm per year'])
        return {'stem': stem + ' What is the rate of spreading on this side of the ridge?', 'options': opts, 'answer': ans, 'key': f'{d} km = {nf(int(d * 1e5))} cm; ÷ {nf(int(a * 1e6))} years = {dp(v, 1)} cm/yr. [1]'}
    parts = [
        lambda r: ('Calculate the mean rate of spreading (cm per year) on this side of the ridge, using the furthest sample.', f'{dp(v, 1)} cm per year', f'{d} × 100 000 cm ÷ {fmt(a, 1)} × 10⁶ years [2]'),
        lambda r: ('Calculate the full rate at which the two plates are separating, assuming symmetrical spreading.', f'{dp(2 * v, 1)} cm per year', f'2 × {dp(v, 1)} [1]'),
        lambda r: ('Describe the relationship between distance from the ridge and age of the rocks.', 'Age increases with distance from the ridge in a near-linear way.', '[1]'),
        lambda r: ('Explain how this evidence supports sea-floor spreading.', 'New crust forms at the ridge and is carried away as the plates diverge, so the youngest rocks are at the ridge and older ones further away, symmetrically on each side.', '[2]'),
        lambda r: ('Explain why no oceanic crust older than about 200 million years exists.', 'Older, colder, denser crust is subducted and destroyed at trenches.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 7.3 rock types
c7c = T('Rock types and the rock cycle', 'rock types rock cycle')
ROCKS = [('granite', 'igneous (intrusive)'), ('basalt', 'igneous (extrusive)'), ('andesite', 'igneous (extrusive)'), ('limestone', 'sedimentary'), ('sandstone', 'sedimentary'),
         ('shale', 'sedimentary'), ('chalk', 'sedimentary'), ('marble', 'metamorphic'), ('slate', 'metamorphic'), ('schist', 'metamorphic'), ('gneiss', 'metamorphic'), ('quartzite', 'metamorphic')]
B(c7c, {
    'terms': [
        ('igneous rock', 'rock formed by the cooling and crystallisation of magma or lava'),
        ('sedimentary rock', 'rock formed from deposited particles or organic remains that have been compacted and cemented'),
        ('metamorphic rock', 'rock changed in form by intense heat and/or pressure without melting'),
        ('rock cycle', 'the continuous processes by which rocks are formed, broken down and re-formed over geological time'),
        ('lithification', 'the processes of compaction and cementation that turn sediments into rock'),
        ('intrusive igneous rock', 'igneous rock that cools slowly underground, forming large crystals'),
        ('extrusive igneous rock', 'igneous rock that cools quickly at the surface, forming small crystals'),
    ],
    'mcq': [
        ('Granite has large crystals because', 'it cooled slowly deep underground', ['it cooled quickly at the surface', 'it was formed from sediments', 'it was heated by a nearby intrusion'], '[1]'),
        ('Marble is formed by the metamorphism of', 'limestone', ['sandstone', 'granite', 'shale'], '[1]'),
        ('Slate is formed by the metamorphism of', 'shale or mudstone', ['limestone', 'basalt', 'chalk'], '[1]'),
        ('Which process in the rock cycle turns igneous rock into sediment?', 'Weathering and erosion', ['Melting', 'Metamorphism', 'Lithification'], '[1]'),
    ],
    'explain': [
        ('Explain the processes involved in the rock cycle.', 'Magma cools to form igneous rock; weathering and erosion break rocks down; transport and deposition of sediments; burial, compaction and cementation form sedimentary rock; heat and pressure form metamorphic rock; melting at subduction zones produces new magma.', '1 mark per process [5]'),
        ('Explain how the rock cycle is linked to plate tectonics.', 'Magma generated at ridges and subduction zones forms igneous rock; subduction carries rocks to depth where they melt or metamorphose; collision causes regional metamorphism and uplift, exposing rocks to weathering.', '1 mark per link [3]'),
        ('Explain why rock type influences landforms.', 'Resistance to weathering and erosion, permeability and structure (joints, bedding) vary: granite forms tors, limestone forms karst, clay forms lowlands and vales.', '1 mark per point [3]'),
    ],
    'claims': [
        ('Metamorphic rocks are formed by melting.', False, 'They form by heat and pressure in the solid state; melting would produce magma and igneous rock.'),
        ('Limestone and chalk are both sedimentary rocks made mainly of calcium carbonate.', True, 'They are formed largely from shells and skeletons of marine organisms.'),
        ('Basalt and granite form from the same type of magma.', False, 'Basalt forms from basic (low silica) magma; granite from acidic (high silica) magma.'),
    ],
    'essays': [
        ('rock type is more important than climate in influencing the landscape',
         ['Granite tors and inselbergs, limestone karst, chalk escarpments and clay vales reflect lithology and structure; jointing controls weathering.'],
         ['Climate controls the type and rate of weathering (deep chemical weathering in the humid tropics, frost in periglacial areas) and the processes shaping slopes; the same rock forms different landscapes in different climates.'],
         'Rock type sets the potential, but climate determines which processes operate and how fast, so both are essential.',
         ['granite', 'limestone', 'weathering', 'climate']),
    ],
})


@c7c.add('C2', (1, 2, 3), 'short')
def c7c_cls(r, D):
    k = 4 if D <= 2 else 6
    pick = r.sample(ROCKS, k)
    stem = r.choice(['Classify each rock as igneous, sedimentary or metamorphic:', 'State whether each rock is igneous, sedimentary or metamorphic:']) + ' ' + ', '.join(n for n, _ in pick) + '.'
    return {'stem': stem, 'answer': '; '.join(f'{n} {c}' for n, c in pick), 'key': f'1 mark for every two correct [{k // 2}]', 'marks': k // 2, 'type': 'short'}


@data(c7c, c4=False)
def c7c_cool(r, D):
    sites = [('A', 'a lava flow at the surface', 'fine-grained'), ('B', 'a dyke a few metres wide', 'medium-grained'), ('C', 'a large batholith several kilometres below the surface', 'coarse-grained')]
    sizes = [round(r.uniform(0.01, 0.2), 2), round(r.uniform(0.5, 1.5), 1), round(r.uniform(3, 12), 1)]
    stem = 'A student measured the mean crystal size (mm) in three igneous rocks from the same magma: ' + ' '.join(f'Sample {s} (from {w}): {fmt(z, 2)} mm.' for (s, w, _), z in zip(sites, sizes))
    ratio = sizes[2] / sizes[0]
    if D == 1:
        opts, a = mcq(r, 'Sample C', ['Sample A', 'Sample B', 'All cooled at the same rate'])
        return {'stem': stem + ' Which sample cooled most slowly?', 'options': opts, 'answer': a, 'key': 'Largest crystals = slowest cooling. [1]'}
    parts = [
        lambda r: ('Calculate how many times larger the crystals are in Sample C than in Sample A.', f'{dp(ratio, 0)} times', f'{fmt(sizes[2], 1)} ÷ {fmt(sizes[0], 2)} [1]'),
        lambda r: ('Explain the relationship between depth of formation and crystal size.', 'Deep intrusions are insulated, so magma cools slowly and crystals have time to grow; lava at the surface cools rapidly, forming small crystals.', '[2]'),
        lambda r: ('Name a rock likely to have formed at site A and at site C from a basic magma, and from an acidic magma.', 'Basic: basalt (A), gabbro (C). Acidic: rhyolite (A), granite (C).', '[2]'),
        lambda r: ('Explain how rock C could later be exposed at the surface.', 'Uplift and long-term weathering and erosion remove overlying rocks (unloading), e.g. granite batholiths of Dartmoor.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[7] = [c7a, c7b, c7c]


# ============================================================== CHAPTER 8: Weathering and rocks

c8a = T('Physical weathering: freeze-thaw, exfoliation, salt crystal growth and pressure release', 'physical weathering freeze-thaw exfoliation salt crystal growth pressure release')
B(c8a, {
    'terms': [
        ('weathering', 'the breakdown or decay of rock in situ, at or near the Earth’s surface'),
        ('freeze-thaw (frost shattering)', 'the breaking of rock when water in cracks freezes and expands by about 9%, then thaws repeatedly'),
        ('exfoliation (insolation weathering)', 'the peeling of outer layers of rock caused by repeated heating and cooling, especially in hot deserts'),
        ('salt crystal growth', 'the breaking of rock by the pressure of salt crystals growing in pores and cracks as saline water evaporates'),
        ('pressure release (dilatation)', 'the formation of sheet joints parallel to the surface when overlying rock is removed and the rock expands'),
        ('scree (talus)', 'angular rock fragments that accumulate at the foot of a slope, often produced by freeze-thaw'),
        ('granular disintegration', 'the breakdown of coarse-grained rock into individual grains as minerals expand and contract at different rates'),
    ],
    'mcq': [
        ('Freeze-thaw weathering is most effective where', 'temperatures fluctuate around 0 °C and water is available', ['temperatures are always below −20 °C', 'temperatures never fall below 10 °C', 'there is no water'], '[1]'),
        ('Sheeting joints in granite domes such as Half Dome (Yosemite) result from', 'pressure release', ['carbonation', 'freeze-thaw only', 'oxidation'], '[1]'),
        ('Salt crystal growth is most common in', 'hot deserts and coastal areas', ['tropical rainforests', 'polar ice caps', 'deep underground'], '[1]'),
        ('Water expands by about what percentage when it freezes?', '9%', ['0.9%', '50%', '90%'], '[1]'),
    ],
    'explain': [
        ('Explain how freeze-thaw weathering breaks down rock.', 'Water enters joints and pores; on freezing it expands by about 9%, exerting pressure; on thawing water penetrates further; repeated cycles widen cracks until fragments break off, forming scree.', '1 mark per stage [3]'),
        ('Explain how pressure release can cause rocks to break up.', 'When overlying rock is removed by erosion, the confining pressure falls; the rock expands and cracks develop parallel to the surface (sheet joints), allowing other weathering to act.', '[3]'),
        ('Explain why salt weathering is important in hot deserts.', 'Saline groundwater is drawn to the surface by capillary action; evaporation causes salt crystals to grow in pores, exerting pressure; heating also expands salts.', '[3]'),
    ],
    'claims': [
        ('Freeze-thaw is most effective in places with permanently frozen ground.', False, 'It needs repeated cycles of freezing and thawing; permanently frozen ground has few cycles.'),
        ('Physical weathering increases the surface area exposed to chemical weathering.', True, 'Breaking rock into smaller pieces exposes more surface to water and acids.'),
        ('Laboratory experiments suggest heating and cooling alone may not break dry rock.', True, 'Griggs’s experiments showed little effect without water, so moisture and salts are thought to be important in exfoliation.'),
    ],
    'essays': [
        ('physical weathering is more important than chemical weathering in shaping landscapes in cold environments',
         ['Freeze-thaw produces scree, blockfields and tors in periglacial areas; ice wedges and frost heave disturb soils.'],
         ['Chemical weathering continues at low rates (carbonation is enhanced because cold water holds more CO₂); biological weathering by lichens; limestone pavements show solution.'],
         'Physical weathering dominates in cold, dry environments, but chemical weathering is significant where water is abundant.',
         ['freeze-thaw', 'carbonation', 'scree', 'water availability']),
    ],
})


@data(c8a)
def c8a_ft(r, D):
    loc = r.choice(['a station in the Scottish Highlands', 'a station in the Andes of Peru (4000 m)', 'a station in the Tibetan Plateau', 'a station in northern Japan', 'a station in the Alps'])
    days = 10
    rows = []
    for _ in range(days):
        mn = r.randint(-9, 4)
        mx = mn + r.randint(2, 12)
        rows.append((mn, mx))
    cyc = sum(1 for mn, mx in rows if mn < 0 < mx)
    stem = f'Table 8.1 shows daily minimum and maximum air temperatures (°C) over 10 days in early spring at {loc}: ' + '; '.join(f'day {i + 1}: {mn} / {mx}' for i, (mn, mx) in enumerate(rows)) + '.'
    if D == 1:
        opts, a = mcq(r, str(cyc), [str(x) for x in {cyc + 1, cyc + 2, max(0, cyc - 1), max(0, cyc - 2), days} if x != cyc])
        return {'stem': stem + ' On how many days did temperatures cross 0 °C (a freeze-thaw cycle)?', 'options': opts, 'answer': a, 'key': f'Count days with minimum below 0 °C and maximum above 0 °C = {cyc}. [1]'}
    parts = [
        lambda r: ('Identify the number of freeze-thaw cycles (days when temperature passed through 0 °C).', str(cyc), 'minimum < 0 and maximum > 0 [2]'),
        lambda r: ('Calculate the mean diurnal temperature range.', f'{dp(mean([mx - mn for mn, mx in rows]))} °C', 'mean of (max − min) [2]'),
        lambda r: ('Explain why spring and autumn may be the most effective seasons for freeze-thaw weathering here.', 'Temperatures fluctuate around 0 °C most often, and meltwater is available to enter cracks.', '[2]'),
        lambda r: ('Explain how freeze-thaw weathering produces scree slopes.', 'Repeated freezing of water in joints prises off angular fragments, which fall and accumulate at the base of cliffs at about 35°.', '[2]'),
        lambda r: ('Suggest why air temperature data may not represent conditions inside rock cracks.', 'Rock surfaces heat and cool differently from air (sun, shade, aspect); snow insulates; temperatures within cracks lag behind air temperature.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 8.2 chemical and biological weathering
c8b = T('Chemical and biological weathering: hydrolysis, carbonation and oxidation', 'chemical biological weathering hydrolysis carbonation oxidation')
B(c8b, {
    'terms': [
        ('carbonation', 'the reaction of rainwater containing dissolved carbon dioxide (carbonic acid) with calcium carbonate in limestone to form soluble calcium bicarbonate'),
        ('hydrolysis', 'the reaction between rock minerals and water, especially the breakdown of feldspar in granite to form clay (kaolinite)'),
        ('oxidation', 'the reaction of minerals, especially iron, with oxygen, producing red-brown iron oxides that weaken rock'),
        ('hydration', 'the absorption of water into the structure of minerals, causing them to swell'),
        ('chelation', 'the removal of metal ions from rocks by organic acids produced by decaying vegetation'),
        ('biological weathering', 'the breakdown of rock by living organisms, such as root wedging or acids from lichens'),
        ('solution', 'the dissolving of soluble minerals such as rock salt in water'),
    ],
    'mcq': [
        ('Kaolin (china clay) in south-west England was formed by the', 'hydrolysis of feldspar in granite', ['carbonation of chalk', 'oxidation of sandstone', 'freeze-thaw of slate'], '[1]'),
        ('The equation CaCO₃ + H₂CO₃ → Ca(HCO₃)₂ describes', 'carbonation', ['hydrolysis', 'oxidation', 'hydration'], '[1]'),
        ('Rates of most chemical reactions roughly double for every rise in temperature of', '10 °C', ['1 °C', '50 °C', '100 °C'], 'Van ’t Hoff’s rule. [1]'),
        ('Red-brown staining of rocks is usually caused by', 'oxidation of iron minerals', ['carbonation', 'salt crystallisation', 'freeze-thaw'], '[1]'),
    ],
    'explain': [
        ('Explain why carbonation can be more rapid in cold climates than might be expected.', 'Cold water can hold more dissolved carbon dioxide, so rainwater and meltwater are more acidic; soils with decaying vegetation add CO₂.', '[2]'),
        ('Explain how hydrolysis breaks down granite.', 'Hydrogen ions in water react with feldspar crystals, converting them into soft clay minerals (kaolinite); quartz grains are released, so the rock crumbles (grus).', '1 mark reaction; 1 mark clay; 1 mark disintegration [3]'),
        ('Explain the ways in which plants and animals contribute to weathering.', 'Roots grow into cracks and exert pressure; lichens and mosses secrete organic acids (chelation); decaying vegetation adds CO₂ and humic acids; burrowing animals expose fresh rock.', '1 mark per point [3]'),
    ],
    'claims': [
        ('Chemical weathering is fastest in hot, wet climates.', True, 'High temperatures speed up reactions and abundant water is needed for them.'),
        ('Limestone is weathered mainly by hydrolysis.', False, 'Limestone is weathered mainly by carbonation.'),
        ('Biological weathering can be both physical and chemical.', True, 'Roots wedge rock apart physically, and organic acids break it down chemically.'),
    ],
    'essays': [
        ('chemical weathering is the most important type of weathering in all environments',
         ['Chemical weathering dominates in the humid tropics (weathering profiles over 60 m deep); carbonation shapes limestone landscapes worldwide; hydrolysis produces clays.'],
         ['In cold and arid environments physical weathering (freeze-thaw, salt crystal growth) dominates because water or warmth is limited; biological weathering matters in vegetated areas.'],
         'Chemical weathering is the most widespread and effective globally, but not in all environments.',
         ['humid tropics', 'deserts', 'periglacial areas', 'rock type']),
    ],
})


@data(c8b)
def c8b_rate(r, D):
    t1 = r.choice([0, 5])
    t2 = t1 + r.choice([15, 20, 25])
    f = 2 ** ((t2 - t1) / 10)
    p1, p2 = r.choice([('a station in Scotland', 'a station in Malaysia'), ('a station in Canada', 'a station in Brazil'), ('a station in the Alps', 'a station in Ghana')])
    stem = f'Assume that rates of chemical weathering double for every 10 °C rise in temperature. The mean annual temperature at {p1} is {t1} °C and at {p2} is {t2} °C, and both have abundant moisture.'
    if D == 1:
        opts, a = mcq(r, f'{dp(f, 1)} times', [f'{dp(x, 1)} times' for x in {(t2 - t1) / 10, t2 / max(t1, 1), f * 2, f / 2, f + 1, 2 * (t2 - t1) / 10} if abs(x - f) > 0.05])
        return {'stem': stem + f' How many times faster would chemical weathering be at {p2.replace("a station in ", "the station in ")}?', 'options': opts, 'answer': a, 'key': f'2^({t2 - t1} ÷ 10) = {dp(f, 1)}. [1]'}
    parts = [
        lambda r: ('Calculate how many times faster chemical weathering would be at the warmer station.', f'{dp(f, 1)} times', f'2^(({t2} − {t1}) ÷ 10) = {dp(f, 1)} [2]'),
        lambda r: ('Explain why the depth of weathered rock (regolith) is greatest in the humid tropics.', 'High temperatures and rainfall all year, abundant organic acids, and long periods of tectonic stability allow weathering fronts to penetrate tens of metres.', '1 mark per point [3]'),
        lambda r: ('Suggest why the predicted difference may not be found in reality.', 'Rock type, vegetation, water supply, time and removal of weathered material also affect rates; some reactions (carbonation) are faster in cold water.', '[2]'),
        lambda r: ('Name and describe one chemical weathering process that affects granite.', 'Hydrolysis: feldspars react with water to form kaolinite clay, releasing quartz grains.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 8.3 factors affecting weathering (Peltier)
c8c = T('Factors affecting weathering: climate (Peltier diagram), rock type and vegetation', 'factors affecting weathering climate peltier diagram rock type vegetation')
PELTIER = [('Singapore', 27, 2400, 'strong chemical weathering'), ('Manaus, Brazil', 27, 2300, 'strong chemical weathering'), ('Lagos, Nigeria', 27, 1500, 'strong chemical weathering'),
           ('Cairo, Egypt', 22, 25, 'very slight weathering'), ('Riyadh, Saudi Arabia', 26, 100, 'very slight weathering'), ('London, UK', 11, 600, 'moderate chemical weathering with some frost action'),
           ('Reykjavík, Iceland', 5, 850, 'frost action (freeze-thaw) dominant'), ('Tromsø, Norway', 3, 1000, 'frost action (freeze-thaw) dominant'),
           ('Toronto, Canada', 9, 830, 'moderate chemical weathering with some frost action')]
B(c8c, {
    'terms': [
        ('Peltier diagram', 'a graph showing how the likely type and intensity of weathering vary with mean annual temperature and rainfall'),
        ('joint', 'a crack in a rock, without displacement, which allows water to penetrate'),
        ('bedding plane', 'a horizontal boundary between layers of sedimentary rock'),
        ('permeability', 'the ability of a rock to allow water to pass through it'),
        ('porosity', 'the proportion of a rock’s volume made up of pore spaces'),
        ('mineral composition', 'the minerals in a rock, which determine how readily it reacts with water and acids'),
    ],
    'mcq': [
        ('On the Peltier diagram, strong chemical weathering occurs where', 'temperature and rainfall are both high', ['temperature is low and rainfall high', 'temperature is high and rainfall low', 'both are low'], '[1]'),
        ('Which feature of granite makes it vulnerable to weathering despite being hard?', 'Its joints and its feldspar crystals', ['Its high carbonate content', 'Its bedding planes full of fossils', 'Its glassy texture'], '[1]'),
        ('According to Peltier, weathering is slight in hot deserts mainly because', 'there is very little water', ['temperatures are too low', 'there are no rocks', 'vegetation is too dense'], '[1]'),
        ('Limestone is particularly susceptible to', 'carbonation', ['hydrolysis', 'frost heave only', 'oxidation of feldspar'], '[1]'),
    ],
    'explain': [
        ('Explain how rock structure influences the rate of weathering.', 'Joints, bedding planes and faults allow water to enter, increasing the surface area for weathering; closely jointed rock weathers faster; permeable rock allows water to penetrate deeply.', '1 mark per point [3]'),
        ('Explain how vegetation affects weathering.', 'Roots wedge open cracks; decaying vegetation releases humic acids and CO₂, increasing chemical weathering; vegetation keeps the ground moist; but it can also protect rock from extremes of temperature.', '1 mark per point [3]'),
        ('Explain the pattern of weathering shown on the Peltier diagram.', 'Chemical weathering increases with temperature and rainfall; frost action is greatest where temperatures are around 0 °C and moisture is moderate; weathering is slight where it is very dry or very cold.', '1 mark per zone [3]'),
    ],
    'claims': [
        ('Climate is the only factor that controls the rate of weathering.', False, 'Rock type, structure, vegetation, relief and time also influence rates.'),
        ('Hard rocks always weather slowly.', False, 'Hard granite can weather rapidly by hydrolysis if jointed and in a warm, wet climate.'),
        ('Mean annual figures can hide important seasonal variations in weathering conditions.', True, 'Seasonal freezing or wet seasons may be very important even if annual means look moderate.'),
    ],
    'essays': [
        ('climate is the most important factor affecting the type and rate of weathering',
         ['The Peltier diagram shows how temperature and rainfall determine whether chemical weathering, frost action or slight weathering dominates.'],
         ['Rock type (mineral composition, jointing, permeability), vegetation, relief and time strongly influence rates; limestone and granite weather very differently in the same climate.'],
         'Climate largely determines the type of weathering, but rock characteristics often control the rate locally.',
         ['the Peltier diagram', 'rock type', 'vegetation', 'jointing']),
    ],
})


@data(c8c, c4=False)
def c8c_pelt(r, D):
    nm, t, p, w = r.choice(PELTIER)
    if D <= 2:
        opts, a = mcq(r, cap(w), [cap(x) for x in {z[3] for z in PELTIER} if x != w])
        return {'stem': f'{nm} has a mean annual temperature of {t} °C and mean annual rainfall of {nf(p)} mm. According to the Peltier diagram, which weathering regime is most likely?', 'options': opts, 'answer': a, 'key': f'{cap(w)}. [1]'}
    nm2, t2, p2, w2 = r.choice([x for x in PELTIER if x[3] != w])
    stem = f'Station X ({nm}) has a mean annual temperature of {t} °C and rainfall of {nf(p)} mm. Station Y ({nm2}) has {t2} °C and {nf(p2)} mm.'
    parts = [
        lambda r: ('Using the Peltier diagram, identify the likely weathering regime at each station.', f'X: {w}; Y: {w2}', '1 mark each [2]'),
        lambda r: ('Explain the difference between the two stations.', 'Explanation in terms of temperature (reaction rates, freeze-thaw around 0 °C) and water availability.', '1 mark temperature; 1 mark moisture [2]'),
        lambda r: ('Suggest how rock type could cause the actual weathering to differ from that predicted.', 'Limestone weathers rapidly by carbonation; jointed granite by hydrolysis; massive quartzite resists weathering; porous sandstone suffers salt weathering.', '[2]'),
        lambda r: ('Suggest one limitation of the Peltier diagram.', 'Uses annual means, hiding seasonal and diurnal variations; ignores rock type, vegetation and microclimate.', '[1]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


add_spearman(c8c, [
    {'intro': 'A student measured the depth of lettering eroded on {n} limestone headstones of known age in a cemetery in a humid city.', 'label': 'Headstone',
     'x': ('age of the headstone (years)', 20, 200, 0), 'y': ('mean weathering depth (mm)', 0.2, 6.0, 1), 'sign': 1,
     'why': 'Carbonation by slightly acidic rainwater dissolves calcium carbonate over time, so older stones have been weathered for longer; urban air pollution (acid rain) increases rates.',
     'limit': 'Stones may differ in limestone type, aspect and exposure; choose headstones of the same rock and aspect, and measure several letters on each.'},
])


CHAPTERS[8] = [c8a, c8b, c8c]


# ============================================================== CHAPTER 9: Slope processes and human interaction

c9a = T('Mass movement: heaves, flows, slides and falls', 'mass movement heaves flows slides falls')
B(c9a, {
    'terms': [
        ('mass movement', 'the downslope movement of weathered material under the influence of gravity'),
        ('soil creep', 'the very slow downslope movement of soil particles by heave, mainly caused by wetting and drying or freezing and thawing'),
        ('rockfall', 'the rapid free fall of rock fragments from a steep cliff face'),
        ('rotational slide (slump)', 'the movement of a mass of material along a curved slip plane, often on clay'),
        ('translational slide', 'the movement of material along a planar slip surface such as a bedding plane'),
        ('mudflow', 'a rapid flow of fine, water-saturated material down a slope or channel'),
        ('shear strength', 'the internal resistance of a material to movement'),
        ('shear stress', 'the force acting on material that tends to move it downslope'),
        ('terracettes', 'small, step-like ridges on grassy slopes associated with soil creep'),
    ],
    'mcq': [
        ('Mass movement occurs when', 'shear stress exceeds shear strength', ['shear strength exceeds shear stress', 'the slope is completely dry', 'the slope angle is zero'], '[1]'),
        ('Leaning fence posts, terracettes and bulging walls are evidence of', 'soil creep', ['rockfall', 'rotational slide', 'avalanche'], '[1]'),
        ('A curved slip plane with back-tilted blocks is characteristic of', 'a rotational slide (slump)', ['a rockfall', 'soil creep', 'a translational slide'], '[1]'),
        ('Water increases the likelihood of mass movement mainly because', 'it adds weight and raises pore water pressure, reducing friction', ['it cements particles together', 'it reduces slope angle', 'it increases vegetation cover'], '[1]'),
    ],
    'explain': [
        ('Explain how heavy rainfall can trigger a landslide.', 'Water adds weight (shear stress); high pore-water pressure pushes particles apart, reducing friction and cohesion (shear strength); lubricates slip planes; erosion of the slope foot.', '1 mark per point [3]'),
        ('Explain the process of soil creep.', 'Particles are lifted at right angles to the slope by wetting or freezing (heave) and fall back vertically under gravity when they dry or thaw, so they move slowly downslope.', '[3]'),
        ('Classify mass movements by speed and water content.', 'Heaves (creep) slow and moderately wet; flows (mudflows, earthflows) fast and wet; slides (rotational, translational) fast, moderately dry along a slip plane; falls very fast and dry.', '1 mark per type [4]'),
        ('Explain why rotational slides are common on clay slopes.', 'Clay becomes saturated and loses strength; it is weak and impermeable, so water builds up; slopes over-steepened by river or wave erosion fail along a curved plane.', '[3]'),
    ],
    'claims': [
        ('All mass movements are rapid events.', False, 'Soil creep is extremely slow, perhaps only millimetres a year.'),
        ('Earthquakes can trigger landslides.', True, 'Shaking reduces shear strength and adds stress; e.g. the 2008 Sichuan and 2015 Nepal earthquakes triggered thousands of landslides.'),
        ('Vegetation always makes slopes less stable.', False, 'Roots usually bind soil and transpiration dries it, increasing stability; very large trees can add weight and wind stress.'),
    ],
    'essays': [
        ('water is the most important factor in causing mass movement',
         ['Rain and snowmelt raise pore water pressure and weight; most landslides follow heavy rain (e.g. Kerala 2018, Uttarakhand 2013); mudflows need saturation.'],
         ['Slope angle, rock structure (bedding dipping out of the slope), weathering, earthquakes, undercutting by rivers or waves and human activity (road cuts, deforestation, loading) also matter; rockfalls can be dry.'],
         'Water is the most common trigger, but slopes fail only where geology, angle and human activity have already reduced stability.',
         ['pore water pressure', 'slope angle', 'earthquakes', 'human activity']),
    ],
})


@data(c9a)
def c9a_fs(r, D):
    sites = []
    for nm in ('Slope A', 'Slope B', 'Slope C'):
        s = r.randint(40, 160)
        t = r.randint(40, 160)
        if s == t:
            t += 7
        sites.append((nm, s, t))
    res = [(n, s / t) for n, s, t in sites]
    loc = r.choice(['along a mountain road in Nepal', 'above a settlement in Rio de Janeiro', 'on a coastal cliff in Dorset, UK', 'beside roads in Hong Kong'])
    stem = f'Engineers estimated the shear strength and shear stress (kPa) on three slopes {loc}. ' + ' '.join(f'{n}: shear strength {s}, shear stress {t}.' for n, s, t in sites)
    unstable = [n for n, f in res if f < 1]
    if D == 1:
        n, s, t = sites[0]
        opts, a = mcq(r, dp(s / t, 2), [dp(t / s, 2), dp(s - t, 0), dp(s * t / 100, 2), dp(s / t + 0.5, 2)])
        return {'stem': stem + f' The factor of safety is shear strength ÷ shear stress. What is the factor of safety of {n}?', 'options': opts, 'answer': a, 'key': f'{s} ÷ {t} = {dp(s / t, 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the factor of safety (shear strength ÷ shear stress) for each slope.', '; '.join(f'{n} {dp(f, 2)}' for n, f in res), '1 mark two correct; 2 marks all [2]'),
        lambda r: ('Identify which slopes are likely to fail.', (', '.join(unstable) + ' (factor of safety below 1)') if unstable else 'None: all factors of safety are above 1.', '[1]'),
        lambda r: ('Explain how heavy rainfall could change the factor of safety.', 'Water adds weight (increasing shear stress) and raises pore water pressure (reducing shear strength), so the factor of safety falls.', '1 mark each [2]'),
        lambda r: ('Suggest two ways engineers could increase the factor of safety of an unstable slope.', 'Drainage to lower pore water pressure; regrading to a lower angle; retaining walls or rock bolts; soil nailing; vegetation; removing load from the top.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 9.2 rainsplash and sheetwash
c9b = T('Water and sediment movement on slopes: rainsplash and sheetwash', 'water sediment movement on slopes rainsplash sheetwash')
B(c9b, {
    'terms': [
        ('rainsplash', 'the detachment and movement of soil particles by the impact of raindrops'),
        ('sheetwash', 'unchannelled overland flow that moves as a thin sheet over the surface, carrying fine sediment'),
        ('rill', 'a small channel, a few centimetres deep, formed by concentrated overland flow'),
        ('gully', 'a deep channel formed when rills join and erode further, too large to remove by ploughing'),
        ('soil erosion', 'the removal of soil by water or wind faster than it can be formed'),
        ('kinetic energy of rainfall', 'the energy of falling raindrops, which increases with drop size and rainfall intensity'),
    ],
    'mcq': [
        ('On a slope, rainsplash moves more soil downslope than upslope because', 'particles splashed downslope travel further', ['raindrops only fall on the lower slope', 'gravity is stronger at the slope foot', 'particles cannot move upslope'], '[1]'),
        ('Sheetwash is most likely on', 'bare, compacted slopes during intense rain', ['forested slopes with deep litter', 'permeable sandy soils in light rain', 'flat ground under snow'], '[1]'),
        ('Rills develop into gullies when', 'flow concentrates and erodes downwards and headwards', ['vegetation recolonises them', 'rainfall stops', 'they are ploughed'], '[1]'),
        ('Which measure most directly reduces rainsplash erosion?', 'Maintaining a vegetation or mulch cover', ['Ploughing up and down slopes', 'Removing hedges', 'Compacting soil with machinery'], '[1]'),
    ],
    'explain': [
        ('Explain how rainsplash causes the net movement of soil downslope.', 'Raindrops detach particles and splash them in all directions; on a slope those moving downslope travel further and those moving upslope a shorter distance, so there is net downslope movement.', '[3]'),
        ('Explain the conditions that favour sheetwash.', 'Intense rainfall exceeding infiltration capacity; bare or crusted soil; smooth, gentle to moderate slopes; little vegetation, as in semi-arid areas or on cleared farmland.', '1 mark per condition [3]'),
        ('Explain why semi-arid areas often have high rates of soil erosion by water.', 'Sparse vegetation leaves soil exposed; rainfall is infrequent but intense; surface crusts reduce infiltration, producing overland flow.', '[3]'),
    ],
    'claims': [
        ('Rainsplash only moves soil on steep slopes.', False, 'It moves soil on all slopes; on flat ground movement is equal in all directions, so there is no net transport.'),
        ('Removing vegetation increases soil erosion by water.', True, 'Bare soil is exposed to raindrop impact and overland flow.'),
        ('Sheetwash forms deep channels.', False, 'Sheetwash is unchannelled; channels form when flow concentrates into rills and gullies.'),
    ],
    'essays': [
        ('rainsplash and sheetwash are more important than mass movement in shaping slopes',
         ['On gentle slopes in semi-arid and cultivated areas rainsplash and sheetwash remove topsoil continuously and shape pediments.'],
         ['On steep slopes, mass movement (landslides, rockfall, creep) moves far more material; humid vegetated slopes have little wash.'],
         'Their importance depends on climate, vegetation and slope angle: wash dominates on gentle, bare slopes, mass movement on steep ones.',
         ['climate', 'vegetation', 'slope angle', 'human activity']),
    ],
})


@data(c9b)
def c9b_plots(r, D):
    covers = [('bare soil', 1.0), ('maize (row crop)', 0.45), ('grass', 0.08), ('forest', 0.03), ('maize with mulch', 0.15)]
    pick = r.sample(covers, 4)
    base = r.randint(20, 60)
    loss = [round(base * f * r.uniform(0.85, 1.15), 1) for _, f in pick]
    loc = r.choice(['Ethiopia', 'Kenya', 'northern Thailand', 'Bolivia', 'Malawi'])
    stem = f'Table 9.2 shows annual soil loss (tonnes per hectare) from experimental plots on the same slope in {loc}: ' + ', '.join(f'{n} {fmt(v, 1)}' for (n, _), v in zip(pick, loss)) + '.'
    hi, lo = max(loss), min(loss)
    if D == 1:
        opts, a = mcq(r, f'{dp(hi / lo)} times', [f'{dp(hi - lo)} times', f'{dp(lo / hi, 2)} times', f'{dp(hi / lo / 2)} times', f'{dp(hi / lo + 3)} times'])
        return {'stem': stem + ' How many times greater is the highest soil loss than the lowest?', 'options': opts, 'answer': a, 'key': f'{fmt(hi, 1)} ÷ {fmt(lo, 1)} = {dp(hi / lo)}. [1]'}
    parts = [
        lambda r: ('Calculate the mean soil loss of the four plots.', f'{dp(mean(loss), 2)} t/ha', f'sum {dp(sum(loss), 1)} ÷ 4 [1]'),
        lambda r: (f'Calculate the percentage reduction in soil loss from the plot with the highest loss to the plot with the lowest.', f'{dp((hi - lo) / hi * 100)}%', f'({fmt(hi, 1)} − {fmt(lo, 1)}) ÷ {fmt(hi, 1)} × 100 [2]'),
        lambda r: ('Explain the differences in soil loss between the plots.', 'Vegetation and mulch intercept rain, reducing raindrop impact (rainsplash); roots bind soil; litter and organic matter increase infiltration and reduce sheetwash; bare and row-crop plots are exposed.', '1 mark per point [3]'),
        lambda r: ('Suggest two farming methods that could reduce soil loss on this slope.', 'Contour ploughing; terracing; mulching or cover crops; stone lines (bunds); agroforestry; strip cropping.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 9.3 slope stabilisation
c9c = T('Slope stabilisation and human interaction with slopes', 'slope stabilisation human interaction with slopes')
B(c9c, {
    'terms': [
        ('slope stabilisation', 'measures to increase the shear strength or reduce the shear stress of a slope'),
        ('regrading', 'reducing the angle of a slope by removing material, to increase stability'),
        ('rock bolts', 'steel rods drilled into a rock face to pin unstable blocks to stable rock behind'),
        ('soil nailing', 'inserting steel bars into a soil slope and covering it with sprayed concrete or mesh'),
        ('gabions', 'wire cages filled with rocks used to support slopes and riverbanks while allowing drainage'),
        ('retaining wall', 'a wall built at the foot of a slope to hold back material'),
        ('slope drainage', 'pipes or channels that remove water from a slope to lower pore water pressure'),
    ],
    'mcq': [
        ('Hong Kong reduced landslide deaths after 1977 mainly through', 'a government slope safety programme including soil nailing, drainage and warnings', ['banning all building on slopes', 'removing all vegetation', 'building only on reclaimed land'], 'The Geotechnical Engineering Office (GEO) was set up after the 1972 and 1976 disasters. [1]'),
        ('Which human activity is most likely to reduce slope stability?', 'Cutting into the base of a slope for a road', ['Planting trees', 'Installing drainage', 'Building a retaining wall'], '[1]'),
        ('Lowering pore water pressure in a slope can best be achieved by', 'installing drainage pipes', ['adding more weight at the top', 'irrigating the slope', 'removing vegetation'], '[1]'),
        ('Wire mesh fixed over a cliff face is used mainly to', 'stop falling rocks from reaching roads', ['increase pore water pressure', 'speed up weathering', 'encourage soil creep'], '[1]'),
    ],
    'explain': [
        ('Explain how human activities can make slopes less stable.', 'Undercutting by road and building construction steepens slopes; adding weight (buildings, tipping waste) increases shear stress; leaking pipes and irrigation raise pore water pressure; deforestation removes roots; vibrations from traffic or blasting.', '1 mark per activity explained [4]'),
        ('Explain how vegetation can stabilise slopes.', 'Roots bind soil and increase shear strength; interception and transpiration reduce soil moisture and pore water pressure; protects surface from rainsplash.', '[3]'),
        ('Explain how planning can reduce the risk from unstable slopes.', 'Hazard mapping and zoning prevent building on high-risk slopes; building regulations; early warning based on rainfall thresholds; monitoring with inclinometers.', '1 mark per point [3]'),
    ],
    'claims': [
        ('Engineering can make any slope completely safe.', False, 'Measures reduce risk but extreme rainfall or earthquakes can still trigger failures, and costs limit what is possible.'),
        ('Informal settlements on steep slopes are especially vulnerable to landslides.', True, 'Housing is built without engineering, with cut slopes and leaking water, as in Rio de Janeiro’s favelas or Freetown in 2017.'),
        ('Drainage is one of the most cost-effective ways of stabilising slopes.', True, 'Lowering pore water pressure increases shear strength at relatively low cost.'),
    ],
    'cs': [
        ('slope management', [
            ('Hong Kong', {'problem': 'Steep slopes of deeply weathered granite and volcanic rock, intense rain (over 2400 mm a year, typhoons) and dense development; 1972 landslides killed 138 people and the 1976 Sau Mau Ping slide killed 18.',
                           'response': 'The Geotechnical Engineering Office (1977) registered and upgraded over 60 000 man-made slopes using soil nails, drainage, shotcrete and vegetation; landslip warnings; strict building controls; annual landslide fatalities fell sharply.'}),
            ('Rio de Janeiro, Brazil', {'problem': 'Favelas on steep granite and gneiss hillsides; heavy summer rain; deforestation and cut slopes; landslides in 2010 and 2011 (Região Serrana) killed hundreds.',
                                        'response': 'Alerta Rio warning system with sirens; Geo-Rio slope works, retaining walls and drainage; relocation of some households; reforestation; limited by cost and continued informal building.'}),
        ], [
            ('explain why slopes are unstable in the area', 'problem', 'Geology, climate, relief, human activity, with events and dates.'),
            ('describe the methods used to manage the slopes', 'response', 'Engineering, warning, planning, with named examples.', 'evaluate the success of attempts to reduce the risk from slope failure.'),
        ]),
    ],
    'essays': [
        ('human activities are now the main cause of slope instability',
         ['Road cuts, quarrying, construction, deforestation, irrigation and leaking water pipes trigger many landslides, e.g. in the Himalaya, Hong Kong and Rio de Janeiro.'],
         ['Natural factors (heavy rain, earthquakes, weathering, undercutting by rivers and waves, slope angle and geology) remain the main causes in remote mountain areas.'],
         'Human activity is increasingly important near settlements and roads, but natural triggers still cause most slope failures globally.',
         ['construction', 'deforestation', 'earthquakes', 'rainfall']),
    ],
})


@data(c9c)
def c9c_angle(r, D):
    run = r.randint(8, 40)
    rise = round(run * math.tan(math.radians(r.randint(15, 50))), 1)
    ang = math.degrees(math.atan(rise / run))
    target = r.choice([25, 30])
    new_run = rise / math.tan(math.radians(target))
    stem = f'A surveyor measured an unstable cut slope above a road in {city(r)}’s hinterland. It rises {fmt(rise, 1)} m over a horizontal distance of {run} m.'
    if D == 1:
        opts, a = mcq(r, f'{dp(ang, 0)}°', [f'{dp(90 - ang, 0)}°', f'{dp(rise / run * 45, 0)}°' if abs(rise / run * 45 - ang) > 1 else f'{dp(ang + 10, 0)}°', f'{dp(ang / 2, 0)}°', f'{dp(min(89, ang + 15), 0)}°'])
        return {'stem': stem + ' What is the slope angle?', 'options': opts, 'answer': a, 'key': f'tan⁻¹({fmt(rise, 1)} ÷ {run}) = {dp(ang, 0)}°. [1]'}
    parts = [
        lambda r: ('Calculate the slope angle in degrees.', f'{dp(ang, 1)}°', f'tan⁻¹({fmt(rise, 1)} ÷ {run}) [2]'),
        lambda r: (f'Engineers want to regrade the slope to {target}°. Calculate the new horizontal distance needed for the same height.', f'{dp(new_run, 1)} m' if ang > target else f'None: the slope is already {dp(ang, 1)}°, below {target}°.', f'{fmt(rise, 1)} ÷ tan {target}° [2]'),
        lambda r: ('Explain why regrading increases slope stability.', 'A lower angle reduces the downslope component of gravity (shear stress), so the factor of safety increases.', '[2]'),
        lambda r: ('Suggest why regrading may not be possible here and suggest an alternative.', 'Space is limited by the road and buildings, and land is costly; alternatives include soil nailing, rock bolts, retaining walls, drainage or vegetation.', '1 mark reason; 1 mark alternative [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[9] = [c9a, c9b, c9c]


# ============================================================== CHAPTER 10: Natural increase

CTRY = [('Niger', 45, 8, 6.1, 60), ('Nigeria', 36, 12, 5.1, 70), ('Uganda', 37, 5, 4.5, 30), ('Pakistan', 27, 7, 3.4, 52), ('India', 16, 7, 2.0, 26),
        ('Bangladesh', 18, 5, 1.9, 23), ('Brazil', 12, 7, 1.6, 13), ('Mexico', 15, 7, 1.8, 11), ('China', 6, 8, 1.0, 5), ('UK', 10, 9, 1.4, 4),
        ('Japan', 6, 13, 1.2, 2), ('Italy', 7, 12, 1.2, 2), ('South Korea', 5, 7, 0.7, 3), ('Kenya', 27, 5, 3.3, 30), ('Ethiopia', 31, 6, 4.0, 35)]

c10a = T('Birth rate, death rate and fertility: measures and global patterns', 'birth rate death rate fertility measures global patterns')
B(c10a, {
    'terms': [
        ('crude birth rate', 'the number of live births per 1000 population per year'),
        ('crude death rate', 'the number of deaths per 1000 population per year'),
        ('total fertility rate', 'the average number of children a woman would have during her reproductive life (15-49) at current age-specific rates'),
        ('infant mortality rate', 'the number of deaths of infants under one year old per 1000 live births per year'),
        ('rate of natural increase', 'the crude birth rate minus the crude death rate, usually expressed as a percentage'),
        ('replacement level fertility', 'a total fertility rate of about 2.1, at which each generation replaces itself'),
        ('age-specific fertility rate', 'the number of births per year per 1000 women in a particular age group'),
        ('life expectancy at birth', 'the average number of years a newborn baby can expect to live if current death rates continue'),
    ],
    'mcq': [
        ('Which measure is the best indicator of a country’s future population growth from births?', 'Total fertility rate', ['Crude death rate', 'Population density', 'Life expectancy'], 'TFR is not affected by age structure. [1]'),
        ('A country with a crude birth rate of 30 and a crude death rate of 10 has a rate of natural increase of', '2.0%', ['20%', '0.2%', '3.0%'], '(30 − 10) ÷ 10 = 2.0%. [1]'),
        ('Why is the crude death rate of Japan higher than that of Mexico?', 'Japan has a much older population', ['Japan has worse health care', 'Mexico has a lower life expectancy', 'Japan has a higher infant mortality rate'], 'Crude rates are affected by age structure. [1]'),
        ('Which region has the highest total fertility rates?', 'Sub-Saharan Africa', ['East Asia', 'Europe', 'North America'], '[1]'),
        ('The world total fertility rate in the early 2020s was about', '2.3', ['5.0', '1.2', '3.5'], '[1]'),
    ],
    'explain': [
        ('Explain why crude birth and death rates can be misleading when comparing countries.', 'They are affected by age structure: a youthful population gives a low crude death rate even with poor health care, while an ageing population gives a high crude death rate despite good health; TFR and age-specific rates are better.', '1 mark age structure; 1 mark example; 1 mark better measure [3]'),
        ('Describe the global pattern of total fertility rates.', 'Highest in sub-Saharan Africa (e.g. Niger about 6), moderate in South Asia and parts of the Middle East, below replacement in Europe, East Asia (South Korea about 0.7), North America and much of Latin America.', '1 mark per region with data [3]'),
        ('Explain why infant mortality rate is often used as an indicator of development.', 'It reflects access to clean water, sanitation, maternal health care, nutrition and vaccination, so it is sensitive to living conditions.', '[2]'),
    ],
    'claims': [
        ('A country with a fertility rate below 2.1 will start to lose population immediately.', False, 'Population momentum from a youthful age structure and immigration can keep the population growing for decades.'),
        ('The rate of natural increase ignores migration.', True, 'It only compares births and deaths; total change also includes net migration.'),
        ('Life expectancy has increased in almost all countries since 1950.', True, 'Global life expectancy rose from about 46 years in 1950 to about 73 years by 2023.'),
    ],
    'essays': [
        ('the total fertility rate is the most useful measure of population change',
         ['TFR is independent of age structure and predicts long-term growth; it allows comparison between countries (Niger about 6 v South Korea about 0.7).'],
         ['Crude birth and death rates, infant mortality and life expectancy show other aspects; migration can dominate change (Gulf states); population momentum means TFR alone does not predict short-term change.'],
         'TFR is the best single indicator of future natural change, but full understanding needs mortality, age structure and migration data.',
         ['crude rates', 'age structure', 'migration', 'population momentum']),
    ],
})


@data(c10a)
def c10a_rates(r, D):
    nm = r.choice(['Country P', 'Country Q', 'Country R', 'Country S'])
    pop = r.choice([4.2, 7.5, 12.8, 25.6, 48.0, 90.5])  # millions
    cbr = r.randint(8, 44)
    cdr = r.randint(5, 14)
    births = round(pop * 1e6 * cbr / 1000 / 100) * 100
    deaths = round(pop * 1e6 * cdr / 1000 / 100) * 100
    imr = r.randint(3, 70)
    idead = round(births * imr / 1000)
    CBR = births / (pop * 1e6) * 1000
    CDR = deaths / (pop * 1e6) * 1000
    NI = (CBR - CDR) / 10
    stem = f'In one year {nm}, with a mid-year population of {fmt(pop, 1)} million, recorded {nf(births)} live births, {nf(deaths)} deaths and {nf(idead)} deaths of infants under one year old.'
    if D == 1:
        opts, a = mcq(r, f'{dp(CBR)} per 1000', [f'{dp(CBR / 10, 2)} per 1000', f'{dp(CBR * 10, 0)} per 1000', f'{dp(CDR)} per 1000', f'{dp(CBR + CDR)} per 1000', f'{dp(CBR + 5)} per 1000', f'{dp(CBR * 2)} per 1000'])
        return {'stem': stem + ' What was the crude birth rate?', 'options': opts, 'answer': a, 'key': f'{nf(births)} ÷ {nf(int(pop * 1e6))} × 1000 = {dp(CBR)}. [1]'}
    parts = [
        lambda r: ('Calculate the crude birth rate and the crude death rate.', f'CBR {dp(CBR)} per 1000; CDR {dp(CDR)} per 1000', 'births (deaths) ÷ population × 1000 [2]'),
        lambda r: ('Calculate the rate of natural increase as a percentage.', f'{sgn(NI, 2)}%', f'({dp(CBR)} − {dp(CDR)}) ÷ 10 [1]'),
        lambda r: ('Calculate the infant mortality rate.', f'{dp(idead / births * 1000)} per 1000 live births', f'{nf(idead)} ÷ {nf(births)} × 1000 [2]'),
        lambda r: ('Estimate the doubling time of the population if natural increase continues at this rate.', (f'about {round(70 / NI)} years (70 ÷ {dp(NI, 2)})' if NI > 0.05 else 'The population is not growing by natural increase, so it will not double.'), 'rule of 70 [1]'),
        lambda r: ('Suggest whether this country is an LIC or an HIC, using the data.', ('Probably an LIC: high birth rate and high infant mortality.' if cbr >= 25 and imr >= 30 else 'Probably an HIC or upper-middle-income country: low birth rate and low infant mortality.' if cbr < 15 and imr < 15 else 'Probably a middle-income country: indicators are intermediate or mixed.'), '1 mark judgement; 1 mark data [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@data(c10a)
def c10a_tfr(r, D):
    ages = ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49']
    hi = r.choice([False, True])
    shape = [0.3, 1.0, 1.0, 0.8, 0.5, 0.2, 0.05] if hi else [0.05, 0.35, 0.8, 1.0, 0.6, 0.15, 0.01]
    peak = r.randint(180, 280) if hi else r.randint(70, 120)
    asfr = [max(1, round(peak * s)) for s in shape]
    tfr = 5 * sum(asfr) / 1000
    nm = r.choice(['Country X', 'Country Y', 'Country Z'])
    stem = f'Table 10.2 shows age-specific fertility rates (births per 1000 women per year) for {nm}: ' + ', '.join(f'{a}: {v}' for a, v in zip(ages, asfr)) + '.'
    if D == 1:
        opts, a = mcq(r, dp(tfr, 2), [dp(sum(asfr) / 1000, 2), dp(tfr * 2, 2), dp(sum(asfr) / 7 / 10, 2), dp(tfr + 1, 2)])
        return {'stem': stem + ' Using TFR = 5 × Σ(ASFR) ÷ 1000, what is the total fertility rate?', 'options': opts, 'answer': a, 'key': f'5 × {sum(asfr)} ÷ 1000 = {dp(tfr, 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the total fertility rate (TFR = 5 × sum of age-specific rates ÷ 1000).', dp(tfr, 2), f'5 × {sum(asfr)} ÷ 1000 [2]'),
        lambda r: ('State whether fertility is above or below replacement level.', ('Above' if tfr > 2.1 else 'Below') + f' replacement level (2.1): TFR = {dp(tfr, 2)}.', '[1]'),
        lambda r: ('Identify the age group with the highest fertility and suggest a reason.', f'{ages[asfr.index(max(asfr))]}: ' + ('early marriage and childbearing, typical of LICs.' if hi else 'women delay childbirth because of education and careers, typical of HICs.'), '1 mark group; 1 mark reason [2]'),
        lambda r: ('Suggest two reasons for the level of fertility shown.', ('High: children as labour and old-age security, high infant mortality, limited contraception and female education, religious and cultural norms.' if tfr > 2.1 else 'Low: female education and employment, cost of raising children, contraception, late marriage, urban lifestyles.'), '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 10.2 factors affecting fertility and mortality
c10b = T('Factors affecting fertility and mortality', 'factors affecting fertility mortality')
B(c10b, {
    'terms': [
        ('pronatalist culture', 'social or religious values that encourage large families'),
        ('contraceptive prevalence', 'the percentage of women of reproductive age using a method of contraception'),
        ('epidemiological transition', 'the shift in the main causes of death from infectious diseases to degenerative diseases as countries develop'),
        ('maternal mortality ratio', 'the number of women who die from pregnancy-related causes per 100 000 live births'),
        ('child mortality rate', 'the number of deaths of children under five per 1000 live births'),
        ('status of women', 'the position of women in society, including access to education, employment and decision-making'),
    ],
    'mcq': [
        ('Which factor is most strongly associated with lower fertility across countries?', 'Female secondary education', ['Population density', 'Altitude', 'Distance from the coast'], '[1]'),
        ('A fall in infant mortality tends to be followed by a fall in fertility because', 'parents no longer need extra births to ensure some children survive', ['more babies are born', 'death rates rise', 'life expectancy falls'], '[1]'),
        ('Which of these is a degenerative disease that becomes a leading cause of death in HICs?', 'Heart disease', ['Cholera', 'Malaria', 'Measles'], '[1]'),
        ('The HIV/AIDS epidemic in southern Africa in the 1990s-2000s caused', 'a fall in life expectancy in countries such as Botswana and Zimbabwe', ['a rise in fertility to 8', 'falling infant mortality', 'no change in death rates'], '[1]'),
    ],
    'explain': [
        ('Explain the social and economic factors that keep fertility high in many LICs.', 'Children work on farms and support parents in old age; high infant mortality; low female education and status; early marriage; limited access to contraception; religious and cultural values.', '1 mark per factor explained [4]'),
        ('Explain why mortality rates have fallen in LICs since 1950.', 'Vaccination programmes, antibiotics, clean water and sanitation, better nutrition, oral rehydration therapy, improved maternal care and education.', '1 mark each [3]'),
        ('Explain why female education reduces fertility.', 'Educated women marry later, have more knowledge of and access to contraception, enter paid employment (raising the opportunity cost of children), and have more say in family size; children are more likely to survive.', '1 mark per point [3]'),
    ],
    'claims': [
        ('Economic development is the only cause of falling fertility.', False, 'Government policy (China, Iran), education, religion and access to contraception also matter, sometimes before significant development.'),
        ('In some HICs death rates are rising even though health care is improving.', True, 'Ageing populations mean more elderly people, so crude death rates rise (e.g. Japan, Italy).'),
        ('Urbanisation tends to reduce fertility.', True, 'Children are costlier and less economically useful in cities, and services and contraception are more accessible.'),
    ],
    'essays': [
        ('the status of women is the most important influence on fertility',
         ['Female education, employment and autonomy are strongly linked to lower TFR (Kerala, Bangladesh); women choose smaller families when they control decisions.'],
         ['Infant mortality, income and urbanisation, religion and culture, government policy (China’s one-child policy) and access to family planning also influence fertility.'],
         'The status of women is a key underlying factor, but its effect operates alongside mortality decline, economic change and policy.',
         ['education', 'infant mortality', 'religion', 'policy']),
    ],
})

add_spearman(c10b, [
    {'intro': 'A student collected data for {n} countries to test whether total fertility rate is related to female literacy.', 'label': 'Country',
     'x': ('female adult literacy rate (%)', 20, 99, 0), 'y': ('total fertility rate', 1.2, 6.8, 1), 'sign': -1,
     'why': 'Literate women marry later, use contraception, work outside the home and have more control over family size; literacy is also linked to lower infant mortality.',
     'limit': 'Correlation does not prove causation: income, urbanisation and policy also vary; use more countries and control for income.'},
    {'intro': 'A student tested the relationship between GNI per capita and infant mortality rate for {n} countries.', 'label': 'Country',
     'x': ('GNI per capita (US$ thousand)', 0.5, 60, 1), 'y': ('infant mortality rate (per 1000)', 2, 75, 0), 'sign': -1,
     'why': 'Richer countries can provide clean water, sanitation, health care, vaccination and better nutrition, so fewer babies die.',
     'limit': 'National averages hide regional inequality; some countries achieve low IMR at modest incomes (Sri Lanka, Cuba); include more countries and other variables.'},
])


# --------------------------------------------------------------- 10.3 age-sex structure and dependency
c10c = T('Age-sex structure and dependency', 'age-sex structure dependency')
B(c10c, {
    'terms': [
        ('age-sex structure', 'the composition of a population by age groups and sex, usually shown by a population pyramid'),
        ('dependency ratio', 'the ratio of the dependent population (0-14 and 65+) to the economically active population (15-64), multiplied by 100'),
        ('youth dependency ratio', 'the population aged 0-14 divided by the population aged 15-64, multiplied by 100'),
        ('old-age dependency ratio', 'the population aged 65 and over divided by the population aged 15-64, multiplied by 100'),
        ('sex ratio', 'the number of males per 100 females in a population'),
        ('population momentum', 'continued population growth after fertility falls to replacement level, because of a large number of young people entering reproductive ages'),
        ('demographic dividend', 'the economic benefit when the working-age share of a population is high and dependency is low'),
    ],
    'mcq': [
        ('A population pyramid with a narrow base, straight sides and a wide top represents', 'an ageing population with low birth rates', ['a youthful population', 'a population with high death rates', 'rapid population growth'], '[1]'),
        ('A large surplus of males aged 20-40 in Qatar and the UAE is caused by', 'immigration of male construction and service workers', ['high female mortality', 'a baby boom', 'sex-selective abortion'], '[1]'),
        ('A sex ratio at birth of about 111 boys per 100 girls in China in the 2010s was mainly due to', 'son preference and sex-selective abortion', ['higher female life expectancy', 'migration of women', 'war'], '[1]'),
        ('A country has 30% aged 0-14 and 10% aged 65+. Its dependency ratio is about', '67', ['40', '60', '150'], '(30 + 10) ÷ 60 × 100 = 66.7. [1]'),
    ],
    'explain': [
        ('Explain the limitations of the dependency ratio.', 'It assumes everyone aged 15-64 works and those outside it do not; many young people are in education, many older people work, unemployment and informal work are ignored; it does not show productivity.', '1 mark per point [3]'),
        ('Explain the impact of a youthful population structure on a country.', 'Pressure on schools, health care and future jobs and housing; high youth dependency; possible demographic dividend if jobs are created; population momentum.', '1 mark per point [3]'),
        ('Explain why females outnumber males in older age groups in most countries.', 'Women have a higher life expectancy due to biological factors and lower rates of risky behaviour, occupational hazards, smoking and alcohol; war deaths affect men.', '[2]'),
    ],
    'claims': [
        ('A high dependency ratio always means a country has many elderly people.', False, 'In most LICs it is high because of many young dependants.'),
        ('Population pyramids can show the effects of past wars and policies.', True, 'Indentations reveal low births or high deaths, e.g. the narrow cohorts born during China’s 1959-61 famine.'),
        ('Migration can change the shape of a population pyramid.', True, 'Labour migration adds working-age males (Gulf states) and emigration removes them (rural Nepal).'),
    ],
    'essays': [
        ('a youthful population structure brings more problems than opportunities',
         ['Pressure on schools, health care and housing; high youth unemployment and possible unrest; slow per capita growth (Niger, Uganda).'],
         ['A demographic dividend if young people are educated and employed (East Asian growth, India today); large labour force attracts investment; future workers support an older generation.'],
         'A youthful structure is a problem in the short term but can become an opportunity if investment in education and jobs is made.',
         ['education', 'employment', 'demographic dividend', 'services']),
    ],
})


@data(c10c)
def c10c_dep(r, D):
    kind = r.choice(['LIC', 'HIC', 'NIC'])
    y = {'LIC': r.randint(38, 48), 'HIC': r.randint(12, 17), 'NIC': r.randint(20, 28)}[kind]
    o = {'LIC': r.randint(2, 4), 'HIC': r.randint(18, 29), 'NIC': r.randint(7, 13)}[kind]
    w = 100 - y - o
    total = r.choice([5.0, 12.0, 30.0, 85.0])
    dr = (y + o) / w * 100
    ydr, odr = y / w * 100, o / w * 100
    nm = r.choice(['Country A', 'Country B', 'Country C'])
    stem = f'In {nm}, with a total population of {fmt(total, 1)} million, {y}% of people are aged 0-14, {w}% are aged 15-64 and {o}% are aged 65 and over.'
    if D == 1:
        opts, a = mcq(r, dp(dr), [dp(y + o), dp(w / (y + o) * 100), dp(ydr), dp(odr)])
        return {'stem': stem + ' What is the dependency ratio?', 'options': opts, 'answer': a, 'key': f'({y} + {o}) ÷ {w} × 100 = {dp(dr)}. [1]'}
    parts = [
        lambda r: ('Calculate the total dependency ratio.', dp(dr), f'({y} + {o}) ÷ {w} × 100 [2]'),
        lambda r: ('Calculate the youth and old-age dependency ratios.', f'youth {dp(ydr)}; old-age {dp(odr)}', f'{y} ÷ {w} × 100; {o} ÷ {w} × 100 [2]'),
        lambda r: ('Calculate the number of people aged 65 and over.', f'{fmt(round(total * o / 100, 2), 2)} million', f'{o}% of {fmt(total, 1)} million [1]'),
        lambda r: ('Describe the likely shape of the population pyramid.', {'LIC': 'Wide base, concave sides narrowing quickly to a small apex (triangular).', 'HIC': 'Narrow base, near-vertical sides and a wide top (beehive or inverted).', 'NIC': 'Base narrowing as fertility falls, bulge in young working ages, apex widening slowly.'}[kind], '[2]'),
        lambda r: ('Explain two challenges this structure creates for the government.', {'LIC': 'Providing schools and health care for many children; creating jobs for young people entering the labour force; feeding a growing population.', 'HIC': 'Funding pensions and health/social care for the elderly; shrinking workforce and tax base; labour shortages.', 'NIC': 'Creating enough jobs for a large working-age population; planning for future rapid ageing.'}[kind], '1 mark each challenge with development [4]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@data(c10c, c4=False)
def c10c_sex(r, D):
    m = r.randint(40, 2500)
    f = round(m * r.uniform(0.3, 1.2))
    ag = r.choice(['25-29', '30-34', '75-79', '0-4'])
    plc = r.choice(['Doha, Qatar', 'a rural district in Nepal', 'a retirement town in Florida', 'a mining town in Western Australia', 'a province in China'])
    sr = m / f * 100
    stem = f'In {plc}, the {ag} age group contains {nf(m * 100)} males and {nf(f * 100)} females.'
    if D == 1:
        opts, a = mcq(r, dp(sr), [dp(f / m * 100), dp(m / (m + f) * 100), dp(sr / 10, 2), dp(sr + 20)])
        return {'stem': stem + ' What is the sex ratio (males per 100 females)?', 'options': opts, 'answer': a, 'key': f'{nf(m * 100)} ÷ {nf(f * 100)} × 100 = {dp(sr)}. [1]'}
    parts = [
        lambda r: ('Calculate the sex ratio (males per 100 females).', dp(sr), 'males ÷ females × 100 [1]'),
        lambda r: ('Suggest reasons for this sex ratio in this place.', ('More males than females: ' if sr > 105 else 'More females than males: ' if sr < 95 else 'Roughly balanced: ') + 'possible causes include labour migration of men (into Gulf cities or mining towns, or out of rural Nepal), higher female life expectancy in older groups, or son preference.', '1 mark direction; 2 marks reasons linked to the place [3]'),
        lambda r: ('Explain one consequence of an unbalanced sex ratio.', 'Difficulty finding marriage partners; social problems; remittance-dependent households with absent men; changing roles of women.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[10] = [c10a, c10b, c10c]


# ============================================================== CHAPTER 11: Demographic transition

c11a = T('The demographic transition model and its stages', 'demographic transition model stages')
DTM = [(1, 'high stationary', (35, 50), (30, 45)), (2, 'early expanding', (35, 45), (12, 25)), (3, 'late expanding', (18, 28), (6, 10)), (4, 'low stationary', (9, 13), (8, 11)), (5, 'declining (natural decrease)', (6, 9), (10, 14))]
B(c11a, {
    'terms': [
        ('demographic transition model', 'a model describing the change from high birth and death rates to low birth and death rates as a country develops'),
        ('high stationary stage', 'stage 1, with high and fluctuating birth and death rates and little population growth'),
        ('early expanding stage', 'stage 2, in which death rates fall rapidly while birth rates remain high, causing rapid growth'),
        ('late expanding stage', 'stage 3, in which birth rates fall while death rates continue to fall slowly, so growth slows'),
        ('low stationary stage', 'stage 4, with low birth and death rates and little natural increase'),
        ('natural decrease', 'a situation in which deaths exceed births, as in stage 5 of the DTM'),
    ],
    'mcq': [
        ('The greatest rate of natural increase occurs in', 'stage 2', ['stage 1', 'stage 4', 'stage 5'], '[1]'),
        ('Which country is an example of stage 5 of the DTM?', 'Japan', ['Niger', 'India', 'Kenya'], '[1]'),
        ('Falling birth rates in stage 3 are mainly due to', 'urbanisation, female education and the availability of contraception', ['famine and disease', 'improvements in medicine only', 'rising infant mortality'], '[1]'),
        ('The DTM was originally based on the experience of', 'western Europe, especially England and Wales', ['sub-Saharan Africa', 'China', 'South America'], '[1]'),
    ],
    'explain': [
        ('Explain why death rates fall in stage 2 of the DTM.', 'Improved food supply, clean water and sanitation, medical advances (vaccination, antibiotics), better hygiene and education reduce deaths from infectious disease.', '1 mark each [3]'),
        ('Explain why birth rates fall in stage 3.', 'Falling infant mortality reduces the need for many children; urbanisation makes children costly; education and employment of women; contraception; compulsory schooling and child labour laws.', '1 mark each [4]'),
        ('Describe how population structure changes through the stages of the DTM.', 'Stage 1-2: wide base, narrow apex; stage 3: base narrows; stage 4: straight sides; stage 5: narrow base and wide top.', '1 mark per stage [3]'),
    ],
    'claims': [
        ('All countries must pass through all five stages of the DTM in the same order and at the same speed.', False, 'Many countries passed through the stages much faster (South Korea), some have stalled, and policy has shortened stages (China).'),
        ('Total population is highest at the end of the transition.', True, 'Population grows during stages 2 and 3, so it is far larger in stage 4 than in stage 1.'),
        ('Stage 1 has no countries today.', True, 'Some isolated groups may be close, but no country now has stage 1 death rates.'),
    ],
    'essays': [
        ('the demographic transition model is of little use in understanding population change in the 21st century',
         ['Based on 19th-century Europe; LICs experienced much faster death-rate decline due to imported medicine; HIV/AIDS, migration and policy are ignored; stage 5 was added later.'],
         ['It describes the broad sequence most countries follow; useful for comparing countries and predicting needs (schools, pensions); helps explain ageing in Japan and growth in Niger.'],
         'The DTM remains a useful descriptive framework but has limited predictive value and must be adapted to modern conditions.',
         ['speed of change', 'migration', 'policy', 'stage 5']),
    ],
})


@data(c11a)
def c11a_stage(r, D):
    st, nm_, (b1, b2), (d1, d2) = r.choice(DTM)
    b, d = r.randint(b1, b2), r.randint(d1, d2)
    if st == 4 and b < d:
        b = d + 1
    if st == 5 and b >= d:
        b = d - 1
    ni = (b - d) / 10
    stem = f'Country R has a crude birth rate of {b} per 1000 and a crude death rate of {d} per 1000.'
    if D == 1:
        opts, a = mcq(r, f'Stage {st}', [f'Stage {k}' for k in range(1, 6) if k != st])
        return {'stem': stem + ' Which stage of the demographic transition model is it most likely to be in?', 'options': opts, 'answer': a, 'key': f'Stage {st} ({nm_}). [1]'}
    parts = [
        lambda r: ('Calculate the rate of natural increase.', f'{sgn(ni, 1)}%', f'({b} − {d}) ÷ 10 [1]'),
        lambda r: ('Identify the stage of the demographic transition model. Give a reason.', f'Stage {st} ({nm_}): birth rate {b}, death rate {d}.', '1 mark stage; 1 mark reason with data [2]'),
        lambda r: ('Describe the likely population pyramid of the country.', {1: 'Very wide base and rapid narrowing; few elderly.', 2: 'Very wide base, concave sides, few elderly.', 3: 'Narrowing base, widening middle, more elderly.', 4: 'Narrow base, straight sides, broad top.', 5: 'Base narrower than the middle; large elderly share.'}[st], '[2]'),
        lambda r: ('Suggest one economic or social problem likely in this stage and how it could be managed.', {1: 'High infant mortality and famine: improve food supply and health care.', 2: 'Rapid growth puts pressure on food, schools and jobs: family planning and investment in education.',
                                                                                                                    3: 'Many young adults need jobs and housing: economic development and urban planning.', 4: 'Ageing workforce: raise retirement age, encourage immigration.', 5: 'Shrinking workforce and high pension costs: pro-natalist policies, immigration, automation.'}[st], '1 mark problem; 1 mark management [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 11.2 applicability
c11b = T('Applicability of the DTM to HICs and LICs', 'applicability of the dtm to hics lics')
B(c11b, {
    'terms': [
        ('Eurocentric model', 'a model based on the experience of European countries, which may not apply elsewhere'),
        ('imported mortality decline', 'the rapid fall in death rates in LICs after 1945 caused by medicines and health programmes introduced from abroad'),
        ('demographic trap', 'a situation in which death rates fall but birth rates stay high, so rapid growth hinders development'),
        ('fertility transition', 'the change from high to low fertility, which may occur faster or slower than the model suggests'),
        ('stalled transition', 'a situation in which fertility decline stops at a level well above replacement, as in several sub-Saharan African countries'),
    ],
    'mcq': [
        ('Death rates in many LICs fell much faster after 1945 than in 19th-century Britain because', 'modern medicines and health programmes were introduced from abroad', ['industrialisation was faster', 'birth rates were lower', 'there was more emigration'], '[1]'),
        ('South Korea’s fertility rate fell from about 6 in 1960 to below 2 by', 'the mid-1980s', ['1900', '2050', '1960'], '[1]'),
        ('A weakness of the DTM is that it does not include', 'migration', ['birth rates', 'death rates', 'time'], '[1]'),
        ('Which factor helps explain why some sub-Saharan African countries have kept high fertility?', 'Rural economies, low female education and strong cultural value placed on large families', ['Very high urbanisation', 'Ageing populations', 'Universal pension schemes'], '[1]'),
    ],
    'explain': [
        ('Explain why the DTM may not apply to LICs today.', 'Death rates fell faster through imported medicine; birth rates may remain high for cultural or economic reasons; HIV/AIDS and conflict raise death rates; government policy changes fertility rapidly; migration is ignored.', '1 mark per point [4]'),
        ('Explain why the transition took about 150-200 years in the UK but less than 50 years in some Asian countries.', 'In the UK medical and social change was slow and home-grown; Asian countries benefited from imported technology, rapid industrialisation and urbanisation, mass education and strong family-planning policies.', '[3]'),
        ('Explain how government policy can alter a country’s path through the DTM.', 'Anti-natalist policies (China’s one-child policy) speed fertility decline; pro-natalist policies (France, Singapore) try to raise fertility; health spending lowers mortality.', '[3]'),
    ],
    'claims': [
        ('The DTM predicts exactly when a country will reach each stage.', False, 'It describes a sequence but gives no timescale.'),
        ('Some countries have experienced rising death rates in stage 4 or 5 because of ageing.', True, 'An older population raises the crude death rate even when health care improves.'),
        ('The DTM can be applied in the same way to small island states with high emigration.', False, 'Large migration flows dominate population change in places such as Samoa or Tonga.'),
    ],
    'essays': [
        ('the demographic transition model applies better to HICs than to LICs',
         ['It was based on European HICs and fits their history; HICs are now in stages 4 or 5 as predicted.'],
         ['Even HICs show differences (USA baby boom, falling below replacement); many LICs (Bangladesh, Iran) have followed the model rapidly; others have stalled; migration matters in both.'],
         'The model fits HICs historically, but its sequence also describes many LICs, though at a different pace and for different reasons.',
         ['speed', 'causes of decline', 'stalled transition', 'migration']),
    ],
})


@data(c11b)
def c11b_speed(r, D):
    cases = [('England and Wales', 1800, 1940), ('Sweden', 1810, 1930), ('Japan', 1920, 1960), ('South Korea', 1955, 1985), ('Brazil', 1960, 2005), ('Bangladesh', 1975, 2015), ('Iran', 1985, 2005)]
    pick = r.sample(cases, 4)
    stem = 'Table 11.2 gives the approximate dates when total fertility rate began to fall from high levels and when it reached replacement level (2.1): ' + '; '.join(f'{n}: {a}-{b}' for n, a, b in pick) + '.'
    durs = [(n, b - a) for n, a, b in pick]
    fastest = min(durs, key=lambda x: x[1])
    if [d for _, d in durs].count(fastest[1]) > 1:
        return None
    if D == 1:
        opts, a = mcq(r, fastest[0], [n for n, _ in durs if n != fastest[0]])
        return {'stem': stem + ' Which country completed the fertility transition most quickly?', 'options': opts, 'answer': a, 'key': '; '.join(f'{n} {d} years' for n, d in durs) + ' [1]'}
    parts = [
        lambda r: ('Calculate the length of the fertility transition in each country.', '; '.join(f'{n} {d} years' for n, d in durs), '[2]'),
        lambda r: ('Calculate the mean length of the transition for these countries.', f'{dp(mean([d for _, d in durs]))} years', '[1]'),
        lambda r: ('Describe the relationship between the start date and the length of the transition.', 'Countries that began later generally completed it faster.', '[1]'),
        lambda r: ('Explain why later transitions were faster.', 'Access to modern contraception and medicine; family-planning programmes (Bangladesh, Iran); rapid urbanisation and female education; mass media spreading new norms.', '1 mark per reason [3]'),
        lambda r: ('Suggest what this means for the usefulness of the DTM.', 'The sequence holds but the timescale varies, so the DTM cannot predict timing and must be adapted for LICs.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 11.3 ageing and youthful populations
c11c = T('Ageing populations and youthful populations: consequences', 'ageing populations youthful populations consequences')
B(c11c, {
    'terms': [
        ('ageing population', 'a population in which the proportion of people aged 65 and over is rising'),
        ('youthful population', 'a population with a high proportion of people aged under 15'),
        ('grey economy', 'the spending power and economic activity of older people'),
        ('pension time bomb', 'the expected funding crisis as the number of pensioners rises relative to the number of workers'),
        ('median age', 'the age that divides a population into two equal halves'),
        ('super-aged society', 'a society in which more than 20% of the population is aged 65 or over, as in Japan, Italy and Germany'),
    ],
    'mcq': [
        ('Which country had the highest proportion of people aged 65 and over (about 29%) in the early 2020s?', 'Japan', ['Niger', 'India', 'Brazil'], '[1]'),
        ('The median age of Niger is about', '15 years', ['30 years', '45 years', '50 years'], 'Japan’s is about 49. [1]'),
        ('Which policy is a response to an ageing population?', 'Raising the state pension age', ['Building more primary schools', 'Introducing a one-child policy', 'Reducing immigration of young workers'], '[1]'),
        ('Which is a positive consequence of an ageing population?', 'Growth of the grey economy and volunteering', ['More taxpayers', 'Lower health spending', 'More young workers'], '[1]'),
    ],
    'explain': [
        ('Explain the economic consequences of an ageing population.', 'Rising pension and health-care costs; smaller workforce and tax base; labour shortages; higher taxes or borrowing; but grey economy and older people working longer.', '1 mark per point [4]'),
        ('Explain how governments respond to an ageing population.', 'Raising retirement age; encouraging private pensions; immigration of young workers; pro-natalist incentives; automation and robotics in care (Japan); promoting healthy ageing.', '1 mark per response [3]'),
        ('Explain the social consequences of a youthful population.', 'Large demand for schools and teachers; youth unemployment; pressure on housing in cities; potential for unrest; but energy, innovation and future workforce.', '1 mark per point [3]'),
    ],
    'claims': [
        ('An ageing population only creates problems.', False, 'Older people contribute through work, volunteering, childcare and spending (grey economy).'),
        ('Ageing is now happening in many middle-income countries as well as HICs.', True, 'China, Thailand and Brazil are ageing rapidly after fast fertility decline.'),
        ('Immigration alone can stop a population from ageing.', False, 'Migrants also age; very large, continuous inflows would be needed.'),
    ],
    'cs': [
        ('a country with an ageing population', [
            ('Japan', {'impacts': 'About 29% aged 65+ (2023); population falling since 2010 (about 124 million); pension and health costs over a third of the budget; labour shortages in care, construction and farming; rural depopulation and akiya (empty homes).',
                       'responses': 'Pension age raised towards 65-70; more women and older people in work; robots and technology in care homes; new visa schemes for foreign workers since 2019; child allowances to raise fertility (TFR about 1.2).'}),
            ('Italy', {'impacts': 'About 24% aged 65+; TFR about 1.2; high pension spending (about 15% of GDP); depopulation of southern and mountain villages; reliance on migrant carers.',
                       'responses': 'Pension reforms raising retirement age to 67; baby bonuses; €1 house schemes to repopulate villages; dependence on migrant labour.'}),
        ], [
            ('describe the impacts of an ageing population', 'impacts', 'Economic, social and spatial impacts with figures.'),
            ('evaluate the responses to the ageing population', 'responses', 'Named policies and their success.', 'assess the extent to which the country has managed the consequences of an ageing population.'),
        ]),
    ],
    'essays': [
        ('ageing populations are a greater challenge than youthful populations',
         ['Ageing raises pension and health costs while shrinking the workforce and tax base; difficult to reverse (Japan, Italy, South Korea).'],
         ['Youthful populations need schools, health care and millions of new jobs every year; youth unemployment and unrest (Sahel); but both can be managed and both have opportunities.'],
         'The challenges differ; ageing is harder to reverse, but youthful populations in poor countries face more immediate pressures on basic services.',
         ['pensions', 'jobs', 'services', 'policy responses']),
    ],
})


@data(c11c)
def c11c_oadr(r, D):
    yrs = [2000, 2020, 2040]
    w = [r.randint(64, 70), r.randint(58, 64), r.randint(50, 57)]
    o = [r.randint(10, 17), r.randint(18, 24), r.randint(26, 36)]
    y = [100 - a - b for a, b in zip(w, o)]
    if min(y) < 8:
        return None
    nm = r.choice(['Country J', 'Country K', 'Country L'])
    odr = [b / a * 100 for a, b in zip(w, o)]
    stem = f'Table 11.3 shows the population structure (%) of {nm}, with a projection for 2040: ' + ' '.join(f'{yr}: 0-14 {c}%, 15-64 {a}%, 65+ {b}%.' for yr, c, a, b in zip(yrs, y, w, o))
    if D == 1:
        opts, a = mcq(r, dp(odr[1]), [dp(o[1] / 100 * 100), dp(w[1] / o[1] * 100), dp(odr[0]), dp(odr[2])])
        return {'stem': stem + ' What was the old-age dependency ratio in 2020?', 'options': opts, 'answer': a, 'key': f'{o[1]} ÷ {w[1]} × 100 = {dp(odr[1])}. [1]'}
    parts = [
        lambda r: ('Calculate the old-age dependency ratio for each year.', '; '.join(f'{yr} {dp(v)}' for yr, v in zip(yrs, odr)), '65+ ÷ 15-64 × 100 [2]'),
        lambda r: ('Calculate the number of people of working age per person aged 65+ in 2040.', f'{dp(w[2] / o[2], 2)}', f'{w[2]} ÷ {o[2]} [1]'),
        lambda r: ('Explain two consequences of the projected change.', 'Higher pension and health-care costs; fewer taxpayers per pensioner; labour shortages; greater demand for care workers; possible rise in retirement age.', '1 mark each with development [4]'),
        lambda r: ('Suggest why the projection for 2040 may be inaccurate.', 'Future fertility, mortality and migration are uncertain; policy changes (immigration, pro-natalist incentives); pandemics.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[11] = [c11a, c11b, c11c]


# ============================================================== CHAPTER 12: Population-resource relationships

c12a = T('Optimum population, overpopulation and underpopulation', 'optimum population overpopulation underpopulation')
B(c12a, {
    'terms': [
        ('optimum population', 'the number of people that, working with all available resources and technology, gives the highest standard of living'),
        ('overpopulation', 'when there are too many people for the resources and technology available to maintain a reasonable standard of living'),
        ('underpopulation', 'when there are too few people to use the resources of an area efficiently'),
        ('carrying capacity', 'the maximum population an area can support without environmental damage'),
        ('population-resource ratio', 'the relationship between the number of people and the resources available to them'),
        ('ecological footprint', 'the area of productive land and water needed to supply a population’s resources and absorb its waste'),
    ],
    'mcq': [
        ('Australia and Canada are sometimes described as underpopulated because', 'they have vast resources that could support more people at a high standard of living', ['they have very high population densities', 'their resources are exhausted', 'they have high birth rates'], '[1]'),
        ('Optimum population is difficult to identify because', 'it changes with technology, trade and resource discoveries', ['it is always the same as the current population', 'it only depends on area', 'it is set by law'], '[1]'),
        ('Which measure compares resource consumption with what the planet can regenerate?', 'Ecological footprint', ['Crude birth rate', 'Dependency ratio', 'Sex ratio'], '[1]'),
        ('A country with high population density and a high standard of living, such as the Netherlands, shows that', 'density alone does not indicate overpopulation', ['it is overpopulated', 'it must be underpopulated', 'resources are unimportant'], '[1]'),
    ],
    'explain': [
        ('Explain why overpopulation is not the same as high population density.', 'Overpopulation depends on the balance between people and resources (including technology and trade); densely populated Singapore or the Netherlands have high living standards, whereas sparsely populated parts of the Sahel may be overpopulated.', '1 mark definition; 1 mark example each [3]'),
        ('Explain the indicators that an area may be overpopulated.', 'Food shortages and malnutrition; high unemployment and underemployment; overcrowded housing and informal settlements; pressure on water, fuelwood and soils; out-migration.', '1 mark per indicator [3]'),
        ('Explain how technology can change the optimum population.', 'New farming methods, irrigation, energy and trade allow more people to be supported at the same standard, raising the optimum.', '[2]'),
    ],
    'claims': [
        ('The optimum population of a country never changes.', False, 'It changes with technology, resource discovery, trade and expectations.'),
        ('A country can be both underpopulated and have areas that are overpopulated.', True, 'Brazil has sparsely populated Amazon regions and crowded cities.'),
        ('Overpopulation is only a problem in LICs.', False, 'HICs with high consumption may exceed sustainable resource use, as shown by large ecological footprints.'),
    ],
    'essays': [
        ('overpopulation is caused more by unequal distribution of resources than by population growth',
         ['Global food production is enough for all; hunger results from poverty, conflict, waste and unequal access; HICs consume far more per person.'],
         ['Rapid growth in the Sahel and parts of South Asia does increase pressure on land, water and fuelwood; resource limits are real in fragile environments.'],
         'Both matter, but inequality of access and consumption explains more of the imbalance than population numbers alone.',
         ['food distribution', 'consumption', 'technology', 'population growth']),
    ],
})


@data(c12a)
def c12a_index(r, D):
    yrs = [2000, 2005, 2010, 2015, 2020]
    pg = r.uniform(1.0, 3.2)
    fg = r.uniform(0.5, 3.8)
    pop = [round(100 * (1 + pg / 100) ** (y - 2000)) for y in yrs]
    food = [round(100 * (1 + fg / 100) ** (y - 2000) * r.uniform(0.97, 1.03)) for y in yrs]
    food[0] = 100
    pc = [f / p * 100 for f, p in zip(food, pop)]
    nm = r.choice(['Country F', 'Country G', 'Country H'])
    stem = f'Table 12.1 shows index numbers (2000 = 100) for population and food production in {nm}: ' + '; '.join(f'{y}: population {p}, food {f}' for y, p, f in zip(yrs, pop, food)) + '.'
    if D == 1:
        opts, a = mcq(r, dp(pc[-1]), [dp(pop[-1] / food[-1] * 100), dp(food[-1] - pop[-1] + 100), dp(food[-1]), dp(pc[-1] + 10), dp(pc[-1] - 12), dp(pop[-1])])
        return {'stem': stem + ' Calculate the index of food production per person in 2020 (food index ÷ population index × 100).', 'options': opts, 'answer': a, 'key': f'{food[-1]} ÷ {pop[-1]} × 100 = {dp(pc[-1])}. [1]'}
    parts = [
        lambda r: ('Calculate the index of food production per person for 2020.', dp(pc[-1]), f'{food[-1]} ÷ {pop[-1]} × 100 [2]'),
        lambda r: ('Describe the trend in food production per person.', ('Rising: food production grew faster than population.' if pc[-1] > 100 else 'Falling: population grew faster than food production.'), '1 mark trend; 1 mark data [2]'),
        lambda r: ('State whether the data support Malthus or Boserup. Explain your answer.', ('Boserup: food production has kept pace with or exceeded population growth, suggesting innovation.' if pc[-1] >= 100 else 'Malthus: population is outstripping food supply, so food per person is falling.'), '1 mark view; 1 mark reason [2]'),
        lambda r: ('Suggest two reasons why national data may not show whether people have enough to eat.', 'Unequal distribution between regions and social groups; food exports or imports; waste; prices and incomes; quality of diet.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 12.2 Malthus, Boserup, food security
c12b = T('Malthus, Boserup and the food security debate', 'malthus boserup food security debate')
B(c12b, {
    'terms': [
        ('Malthusian theory', 'the view (1798) that population grows geometrically while food supply grows arithmetically, so population will outstrip food'),
        ('positive checks', 'in Malthus’s theory, events such as famine, disease and war that raise the death rate and reduce population'),
        ('preventive checks', 'in Malthus’s theory, measures such as later marriage and abstinence that reduce the birth rate'),
        ('Boserup’s theory', 'the view (1965) that population pressure stimulates agricultural innovation and intensification, so food supply can increase'),
        ('food security', 'when all people at all times have physical and economic access to sufficient, safe and nutritious food'),
        ('neo-Malthusian', 'a modern view that population growth threatens resources and the environment, as in The Limits to Growth (1972)'),
        ('Green Revolution', 'the introduction from the 1960s of high-yielding seeds, fertilisers, pesticides and irrigation that raised crop yields in LICs'),
    ],
    'mcq': [
        ('According to Malthus, population increases', 'geometrically (1, 2, 4, 8 …)', ['arithmetically (1, 2, 3, 4 …)', 'not at all', 'only through migration'], '[1]'),
        ('Which development best supports Boserup’s ideas?', 'The Green Revolution in India in the 1960s-70s', ['The Irish famine of 1845-49', 'The 1984 Ethiopian famine', 'Desertification in the Sahel'], '[1]'),
        ('About how many people were estimated to face chronic hunger in 2023?', 'About 700-750 million', ['About 50 million', 'About 3 billion', 'About 10 million'], '[1]'),
        ('Malthus’s “preventive checks” include', 'later marriage', ['famine', 'war', 'epidemic disease'], '[1]'),
    ],
    'explain': [
        ('Explain Boserup’s theory of population and resources.', 'Population growth creates pressure on food supply; people respond by intensifying farming (shorter fallow, irrigation, terracing, new tools and technology), so food output rises; necessity is the mother of invention.', '1 mark pressure; 1 mark innovation; 1 mark example [3]'),
        ('Explain why Malthus’s predictions have not come true at a global scale.', 'Technological change in farming (mechanisation, fertilisers, Green Revolution); trade; birth rates fell with development; colonisation of new lands; food production grew faster than population.', '1 mark per point [3]'),
        ('Explain the factors that threaten food security.', 'Climate change and extreme weather; conflict (Sudan, Yemen); poverty and food prices; soil degradation; water shortages; waste; pests and disease; dependence on imports.', '1 mark per factor [4]'),
    ],
    'claims': [
        ('Famines are caused only by a lack of food.', False, 'Amartya Sen showed famines often result from loss of access to food (entitlement), e.g. Bengal 1943, rather than absolute shortage.'),
        ('Boserup’s ideas apply best to subsistence farming societies.', True, 'Her work was based on intensification in pre-industrial agricultural systems.'),
        ('Neo-Malthusians argue that environmental limits may still be reached.', True, 'They point to climate change, soil loss and water scarcity as modern checks.'),
    ],
    'essays': [
        ('Boserup’s ideas are more relevant than those of Malthus in the 21st century',
         ['Green Revolution, GM crops, precision farming and trade have raised food output faster than population; global famine has not occurred.'],
         ['Neo-Malthusian concerns: climate change, water stress, soil degradation, biodiversity loss; local famines (Somalia 2011) and food insecurity persist; innovation may not keep pace in fragile areas.'],
         'Boserup better describes global trends so far, but Malthusian limits remain relevant locally and environmentally.',
         ['technology', 'climate change', 'food security', 'scale']),
    ],
})


@data(c12b)
def c12b_mal(r, D):
    gen = r.choice([25, 30])
    p0 = r.choice([1, 2])
    f0 = r.choice([2, 3])
    df = r.choice([1, 1.5])
    steps = list(range(0, 7))
    pop = [p0 * 2 ** s for s in steps]
    food = [f0 + df * s for s in steps]
    cross = next((s for s in steps if pop[s] > food[s]), None)
    if cross is None:
        return None
    stem = (f'A model based on Malthus assumes population (millions) doubles every {gen} years from {p0} million, while food supply (enough for millions of people) rises by {fmt(df, 1)} million every {gen} years from {f0} million. '
            + 'Values: ' + '; '.join(f'year {s * gen}: population {pop[s]}, food {fmt(food[s], 1)}' for s in steps[:5]) + '.')
    yr = cross * gen
    if D == 1:
        opts, a = mcq(r, f'year {yr}', [f'year {x * gen}' for x in range(1, 7) if x != cross][:4])
        return {'stem': stem + ' In which year does population first exceed food supply?', 'options': opts, 'answer': a, 'key': f'year {yr}: population {pop[cross]} > food {fmt(food[cross], 1)}. [1]'}
    parts = [
        lambda r: ('Identify the year in which population first exceeds food supply.', f'year {yr}', '[1]'),
        lambda r: (f'Calculate the shortfall in food supply in year {6 * gen}.', f'{fmt(pop[6] - food[6], 1)} million people', f'{pop[6]} − {fmt(food[6], 1)} [2]'),
        lambda r: ('State what Malthus believed would happen when population exceeded food supply.', 'Positive checks (famine, disease, war) would raise the death rate and reduce population; preventive checks could delay it.', '[2]'),
        lambda r: ('Explain why Boserup would disagree with this model.', 'Food supply would not increase at a fixed arithmetic rate: population pressure would stimulate innovation and intensification, raising food output.', '[2]'),
        lambda r: ('Suggest one real-world example that supports each theorist.', 'Malthus: famines in the Sahel or Ethiopia (1984). Boserup: Green Revolution in India; terracing in Machakos, Kenya (“more people, less erosion”).', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 12.3 policies
c12c = T('Policies to manage natural increase: anti-natalist and pro-natalist', 'policies to manage natural increase anti-natalist pro-natalist')
B(c12c, {
    'terms': [
        ('anti-natalist policy', 'a government policy that aims to reduce the birth rate'),
        ('pro-natalist policy', 'a government policy that aims to increase the birth rate'),
        ('one-child policy', 'China’s policy (1979-2015) that limited most urban couples to one child'),
        ('family planning', 'the use of contraception and education to allow couples to choose the number and spacing of children'),
        ('baby bonus', 'a cash payment or tax benefit to parents for having children'),
        ('two-child policy', 'China’s policy from 2016 allowing all couples two children, replaced by a three-child policy in 2021'),
    ],
    'mcq': [
        ('China’s one-child policy was introduced in', '1979-80', ['1949', '1995', '2015'], '[1]'),
        ('Singapore’s policy since 1987 has been to encourage couples to “Have three or more if you can afford it”. This is', 'a pro-natalist policy', ['an anti-natalist policy', 'a migration policy', 'an ageing policy'], '[1]'),
        ('Which country has used generous family benefits, tax allowances and childcare to keep fertility relatively high in Europe?', 'France', ['China', 'India', 'Bangladesh'], '[1]'),
        ('Bangladesh reduced its fertility rate from about 6.9 in the 1970s to about 2 by 2020 mainly through', 'community family planning workers, female education and health programmes', ['a strict one-child law', 'large-scale emigration', 'banning marriage'], '[1]'),
    ],
    'explain': [
        ('Explain why some governments introduce pro-natalist policies.', 'Fertility well below replacement causes ageing and future population decline; shrinking workforce and tax base; pension costs; national security or cultural concerns (Russia, Hungary, Singapore).', '1 mark per reason [3]'),
        ('Explain the consequences of China’s one-child policy.', 'Fertility fell rapidly; around 400 million births were claimed to have been prevented (disputed); rapid ageing and the “4-2-1” family; male-biased sex ratio (about 118 boys per 100 girls at birth in the mid-2000s); labour shortages; human-rights abuses.', '1 mark per consequence [4]'),
        ('Explain why pro-natalist policies often have limited success.', 'Costs of housing, childcare and education, career pressures and changing values outweigh small financial incentives; effects may be on timing rather than total births.', '[3]'),
    ],
    'claims': [
        ('China’s one-child policy was the only reason Chinese fertility fell.', False, 'Fertility had already fallen from about 5.8 to 2.7 in the 1970s under the “later, longer, fewer” campaign, and development also reduced it.'),
        ('Singapore changed from an anti-natalist to a pro-natalist policy.', True, '“Stop at two” (1972) was replaced in 1987 when fertility fell well below replacement.'),
        ('Pro-natalist policies always increase the birth rate significantly.', False, 'Many, such as South Korea’s large spending, have had little effect: its TFR fell to about 0.7.'),
    ],
    'cs': [
        ('a population policy', [
            ('China’s one-child policy (1979-2015)', {'policy': 'Most urban couples limited to one child; incentives (housing, education) and penalties (fines, loss of jobs); exceptions for rural families whose first child was a girl and for ethnic minorities; replaced by two-child (2016) and three-child (2021) policies.',
                                                       'evaluate': 'TFR fell from 2.7 (1979) to about 1.6 (2000s); rapid economic growth; but forced abortions and sterilisations, gender imbalance, ageing (65+ about 14% in 2021) and a shrinking workforce; relaxation has not raised fertility (TFR about 1.0 in 2023).'}),
            ('Singapore’s population policies', {'policy': '“Stop at Two” (1972-1987) with penalties for larger families; then pro-natalist “Have three or more if you can afford it” (1987), Baby Bonus cash gifts, tax rebates, subsidised childcare and parental leave.',
                                                 'evaluate': 'TFR fell from 5.8 (1960) to 1.4 (1986); the pro-natalist phase has had limited effect, TFR about 1.0 in 2023; the government relies on immigration to maintain the workforce.'}),
        ], [
            ('describe the aims and methods of the policy', 'policy', 'Aims, measures, incentives and penalties, dates.'),
            ('evaluate the success of the policy', 'evaluate', 'Change in TFR with figures; social, economic and demographic consequences.', 'assess the extent to which the population policy has been successful.'),
        ]),
    ],
    'essays': [
        ('anti-natalist policies are more successful than pro-natalist policies',
         ['China and Singapore reduced fertility rapidly; Bangladesh and Iran succeeded with voluntary family planning.'],
         ['Anti-natalist success often coincided with development and had severe social costs; pro-natalist policies (France, Sweden) have kept fertility near 1.7-1.8, though Singapore and South Korea have struggled.'],
         'Reducing fertility has proved easier than raising it, because policies that reverse rising costs and changing values are difficult, but success depends on wider social and economic change.',
         ['China', 'Singapore', 'France', 'development']),
    ],
})


@data(c12c)
def c12c_tfr(r, D):
    sets = [('China', [(1970, 5.8), (1979, 2.7), (1990, 2.5), (2000, 1.6), (2010, 1.6), (2020, 1.3), (2023, 1.0)], 1979, 'one-child policy'),
            ('Singapore', [(1960, 5.8), (1970, 3.1), (1980, 1.8), (1987, 1.6), (2000, 1.6), (2010, 1.2), (2023, 1.0)], 1987, 'switch to pro-natalist policy'),
            ('Bangladesh', [(1975, 6.9), (1985, 5.5), (1995, 3.6), (2005, 2.7), (2015, 2.1), (2022, 1.9)], 1975, 'national family-planning programme'),
            ('Iran', [(1985, 6.4), (1990, 4.8), (1995, 3.3), (2000, 2.2), (2010, 1.8), (2022, 1.7)], 1989, 'family-planning programme')]
    nm, data_, yr, pol = r.choice(sets)
    a, b = sorted(r.sample(range(len(data_)), 2))
    (y1, t1), (y2, t2) = data_[a], data_[b]
    if t1 == t2:
        return None
    pc = pct_change(t1, t2)
    bef = [(y, t) for y, t in data_ if y <= yr]
    aft = [(y, t) for y, t in data_ if y >= yr]
    trend = ((f'Before {yr}: TFR fell from {fmt(bef[0][1], 1)} ({bef[0][0]}) to {fmt(bef[-1][1], 1)} ({bef[-1][0]}). ' if len(bef) > 1 else f'TFR was {fmt(bef[0][1], 1)} when the policy began. ')
             + f'After {yr}: it {"fell" if aft[-1][1] < aft[0][1] else "rose"} from {fmt(aft[0][1], 1)} to {fmt(aft[-1][1], 1)} by {aft[-1][0]}' + ('.' if len(aft) > 1 else '.'))
    stem = f'Fig. 12.3 shows the total fertility rate in {nm}: ' + ', '.join(f'{y}: {fmt(t, 1)}' for y, t in data_) + f'. A {pol} began in {yr}.'
    if D == 1:
        opts, ans = mcq(r, f'{dp(abs(pc))}%', [f'{dp(abs(t1 - t2), 1)}%', f'{dp(abs(pc) / 2)}%', f'{dp(t2 / t1 * 100)}%' if abs(t2 / t1 * 100 - abs(pc)) > 1 else f'{dp(abs(pc) + 12)}%', f'{dp(min(99, abs(pc) + 8))}%'])
        return {'stem': stem + f' By what percentage did TFR change between {y1} and {y2}?', 'options': opts, 'answer': ans, 'key': f'({fmt(t1, 1)} − {fmt(t2, 1)}) ÷ {fmt(t1, 1)} × 100 = {dp(abs(pc))}% fall. [1]'}
    parts = [
        lambda r: (f'Calculate the percentage change in TFR between {y1} and {y2}.', f'{sgn(pc)}%', f'({fmt(t2, 1)} − {fmt(t1, 1)}) ÷ {fmt(t1, 1)} × 100 [2]'),
        lambda r: (f'Describe the trend in TFR before and after {yr}.', trend, '1 mark each period with data [2]'),
        lambda r: ('Suggest why it is difficult to judge how far the policy caused the change in fertility.', 'Fertility was influenced by development, urbanisation, female education and changing attitudes at the same time; it was often already falling before the policy.', '[2]'),
        lambda r: ('Explain one demographic consequence of the change in TFR.', 'Rapid ageing as smaller cohorts follow large ones; falling working-age population; possible imbalanced sex ratio (China).', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[12] = [c12a, c12b, c12c]


# ============================================================== CHAPTER 13: Migration as a component of population change

c13a = T('Types of migration: voluntary and forced, temporary and permanent', 'types of migration voluntary forced temporary permanent')
MIGS = [('A nurse from the Philippines takes a three-year contract in a hospital in Riyadh.', 'voluntary, temporary, international'),
        ('A family flees fighting in Khartoum and crosses into Chad.', 'forced, international (refugees)'),
        ('A farmer in Bihar moves permanently to Mumbai to work in construction.', 'voluntary, permanent, internal (rural-urban)'),
        ('A retired couple from Manchester moves to the Algarve in Portugal.', 'voluntary, permanent, international (retirement)'),
        ('Villagers are resettled when their land is flooded by a new reservoir.', 'forced, permanent, internal (displacement)'),
        ('A student from Nigeria studies for four years at a university in Canada.', 'voluntary, temporary, international'),
        ('Fruit pickers travel from Morocco to Spain each summer and return home.', 'voluntary, temporary (seasonal), international'),
        ('Residents of Montserrat leave after the Soufrière Hills eruption in 1997.', 'forced, international and internal (environmental)'),
        ('A software engineer moves from Bengaluru to the San Francisco Bay Area on a work visa.', 'voluntary, international (skilled, possibly permanent)'),
        ('Herders in the Sahel move with their cattle between wet- and dry-season pastures.', 'voluntary, temporary, circulation (nomadic/transhumance)')]
B(c13a, {
    'terms': [
        ('migration', 'a permanent or semi-permanent change of residence, usually for at least a year'),
        ('voluntary migration', 'migration in which the migrant chooses freely to move, usually for economic or social reasons'),
        ('forced migration', 'migration in which people are compelled to move by conflict, persecution, disaster or development projects'),
        ('internally displaced person (IDP)', 'a person forced to flee their home who remains within their own country'),
        ('circulation', 'short-term, repetitive or cyclical movements such as commuting or seasonal migration, without a permanent change of residence'),
        ('economic migrant', 'a person who moves voluntarily to improve their income and employment'),
        ('emigration', 'the movement of people out of a country'),
        ('immigration', 'the movement of people into a country'),
    ],
    'mcq': [
        ('Which of these is an example of forced migration?', 'Rohingya fleeing Myanmar to Bangladesh in 2017', ['Polish workers moving to the UK after 2004', 'Retirees moving to Spain', 'Indian IT workers moving to the USA'], '[1]'),
        ('Daily commuting is an example of', 'circulation', ['permanent migration', 'forced migration', 'emigration'], '[1]'),
        ('Seasonal migration of farm workers is classified as', 'temporary migration', ['permanent migration', 'forced migration', 'counter-urbanisation'], '[1]'),
        ('A person displaced by a flood who remains in their own country is', 'an internally displaced person', ['a refugee', 'an asylum seeker', 'an economic migrant'], '[1]'),
    ],
    'explain': [
        ('Explain why the distinction between voluntary and forced migration is not always clear.', 'Many migrants are pushed by poverty, drought or insecurity yet choose when and where to move; environmental degradation can make staying impossible gradually; decisions are made within constraints.', '1 mark per point [3]'),
        ('Explain why migration is difficult to define and measure.', 'Different time thresholds (one year), undocumented migration, circulation that is not recorded, internal moves not registered, changing borders.', '1 mark per point [3]'),
        ('Distinguish between internal and international migration, with examples.', 'Internal: within a country, e.g. rural-urban migration to Lagos. International: across national borders, e.g. Mexicans to the USA.', '1 mark each with example [2]'),
    ],
    'claims': [
        ('All refugees are international migrants.', True, 'By definition a refugee has crossed an international border; those who have not are IDPs.'),
        ('Temporary migration has little effect on the source area.', False, 'Seasonal or contract migration brings remittances and skills but removes workers at key times.'),
        ('Commuting counts as migration.', False, 'It is circulation because there is no change of permanent residence.'),
    ],
    'essays': [
        ('classifying migration as either voluntary or forced is of little value',
         ['Many moves combine choice and compulsion (drought-driven migration from the Sahel; economic collapse in Venezuela); the line is blurred.'],
         ['The distinction matters legally (refugee status under the 1951 Convention), for aid and for understanding causes and impacts; extreme cases (Syria, Ukraine) are clearly forced.'],
         'Migration is better seen as a continuum, but the classification remains useful for policy and law.',
         ['refugees', 'economic migrants', 'environmental migration', 'law']),
    ],
})


@c13a.add('C2', (1, 2, 3, 4), 'short')
def c13a_cls(r, D):
    k = 1 if D <= 1 else 2 if D <= 2 else 3
    pick = r.sample(MIGS, k)
    if k == 1:
        s, a = pick[0]
        opts, ans = mcq(r, cap(a), [cap(x) for _, x in MIGS if x != a])
        return {'stem': f'{s} Which classification best describes this movement?', 'options': opts, 'answer': ans, 'key': '[1]'}
    stem = 'Classify each movement (voluntary or forced; temporary or permanent; internal or international) and give a reason for one of your answers. ' + ' '.join(f'({chr(97 + i)}) {s}' for i, (s, _) in enumerate(pick))
    return {'stem': stem, 'answer': ' '.join(f'({chr(97 + i)}) {a}.' for i, (_, a) in enumerate(pick)), 'key': f'1 mark per movement correctly classified; 1 mark reason [{k + 1}]', 'marks': k + 1, 'type': 'short'}


# --------------------------------------------------------------- 13.2 causes, Lee
c13b = T('Causes of migration: push and pull factors, Lee\'s model and intervening obstacles', 'causes of migration push pull factors lee model intervening obstacles')
B(c13b, {
    'terms': [
        ('push factor', 'a negative feature of the place of origin that encourages people to leave'),
        ('pull factor', 'a positive feature of a destination that attracts migrants'),
        ('intervening obstacle', 'a barrier between origin and destination that makes migration more difficult, such as distance, cost, borders or immigration laws'),
        ('intervening opportunity', 'an opportunity closer than the intended destination that causes migrants to stop'),
        ('distance decay', 'the decline in the volume of migration with increasing distance from the origin'),
        ('gravity model', 'a model predicting that migration between two places is proportional to the product of their populations divided by the square of the distance between them'),
        ('chain migration', 'migration encouraged by friends and relatives who have already moved and can help newcomers'),
    ],
    'mcq': [
        ('In Lee’s model, factors at origin and destination include', 'positive, negative and neutral factors', ['only push factors', 'only pull factors', 'only intervening obstacles'], '[1]'),
        ('Which of the following is an intervening obstacle?', 'Strict visa requirements', ['High wages at the destination', 'Unemployment at home', 'Family already at the destination'], '[1]'),
        ('Ravenstein’s “laws” of migration suggested that most migrants', 'move only short distances', ['move internationally', 'are elderly', 'move from towns to the countryside'], '[1]'),
        ('Lee argued that migration is selective because', 'people respond differently to the same factors according to age, education and personal circumstances', ['everyone migrates equally', 'only women migrate', 'only the poorest migrate'], '[1]'),
    ],
    'explain': [
        ('Explain Lee’s model of migration.', 'Origin and destination each have positive, negative and neutral factors perceived differently by individuals; intervening obstacles (distance, cost, laws) lie between; personal factors (age, education, family) affect the decision; migration is selective.', '1 mark per element [4]'),
        ('Explain why migration is often selective by age.', 'Young adults have fewest ties, most to gain from new jobs and education, and can adapt; older people have property and family commitments.', '[2]'),
        ('Explain how improvements in transport and communications affect migration.', 'They reduce the cost and difficulty of moving (intervening obstacles), spread information about opportunities, and allow migrants to keep in touch, encouraging chain migration.', '[3]'),
    ],
    'claims': [
        ('Push factors alone explain why people migrate.', False, 'Migration requires a destination with perceived advantages; pull factors, obstacles and personal factors also matter.'),
        ('Perception of a destination may differ from reality.', True, 'Migrants often have incomplete information, e.g. expectations of urban jobs that do not exist.'),
        ('The gravity model predicts more migration between large, nearby cities.', True, 'Flows are proportional to population size and decrease with distance.'),
    ],
    'essays': [
        ('economic factors are the main cause of migration',
         ['Most voluntary migrants seek higher wages and jobs (South Asians to the Gulf, Mexicans to the USA); remittances support families.'],
         ['Conflict and persecution (Syria, Sudan), environmental hazards, family reunification, education, retirement and lifestyle also cause migration; intervening obstacles and personal factors shape decisions.'],
         'Economic factors explain the largest share of voluntary migration, but forced and social migration are important and decisions combine many factors.',
         ['Lee’s model', 'refugees', 'family', 'intervening obstacles']),
    ],
})


@data(c13b)
def c13b_grav(r, D):
    o = r.choice(['Town O', 'City O'])
    pop0 = r.choice([50, 80, 120, 200])
    dests = []
    for nm in ('A', 'B', 'C'):
        dests.append((f'City {nm}', r.choice([150, 300, 500, 800, 1200, 2000]), r.choice([20, 40, 60, 80, 100, 150])))
    g = [(n, pop0 * p / d ** 2) for n, p, d in dests]
    if len({round(v, 6) for _, v in g}) < 3:
        return None
    stem = f'{o} has a population of {pop0} thousand. Three possible destinations are: ' + '; '.join(f'{n}, population {p} thousand, {d} km away' for n, p, d in dests) + '. The gravity model states that migration ∝ (P₁ × P₂) ÷ d².'
    best = max(g, key=lambda x: x[1])
    if D == 1:
        opts, a = mcq(r, best[0], [n for n, _ in g if n != best[0]] + ['All equal'])
        return {'stem': stem + ' Which destination would the model predict receives most migrants?', 'options': opts, 'answer': a, 'key': '; '.join(f'{n} {sf(v)}' for n, v in g) + ' [1]'}
    parts = [
        lambda r: ('Calculate the gravity model value for each destination.', '; '.join(f'{n} {sf(v)}' for n, v in g), '(P₁ × P₂) ÷ d², 1 mark two correct, 2 marks all [2]'),
        lambda r: ('Identify the destination predicted to attract most migrants.', best[0], '[1]'),
        lambda r: ('Explain why actual flows may differ from those predicted.', 'Intervening opportunities and obstacles; different job opportunities and wages; transport links; existing migrant networks (chain migration); cultural and language ties; government policies.', '1 mark per point [3]'),
        lambda r: ('Explain how the model reflects the idea of distance decay.', 'Flows fall with the square of distance because of the cost, effort and lack of information about distant places.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


add_spearman(c13b, [
    {'intro': 'A student surveyed migrants living in a city and recorded the number who had come from each of {n} source districts, together with the distance of each district from the city.', 'label': 'District',
     'x': ('distance from the city (km)', 10, 450, 0), 'y': ('number of migrants surveyed', 4, 95, 0), 'sign': -1,
     'why': 'Distance decay: cost, time and lack of information increase with distance, and nearer districts have stronger social links (chain migration), so more migrants come from nearby.',
     'limit': 'Districts differ in population size, so raw numbers are biased; express migrants per 10 000 population of each district and increase the sample size.'},
])


# --------------------------------------------------------------- 13.3 migration and population change at different scales
c13c = T('Migration as a component of population change at different scales', 'migration as a component of population change at different scales')
B(c13c, {
    'terms': [
        ('net migration', 'the difference between the number of immigrants and the number of emigrants'),
        ('net migration rate', 'net migration per 1000 population per year'),
        ('population change equation', 'population change = (births − deaths) + (immigrants − emigrants)'),
        ('net migration gain', 'when immigration exceeds emigration, adding to population'),
        ('net migration loss', 'when emigration exceeds immigration, reducing population'),
        ('replacement migration', 'international migration needed to offset declines in the size of a population or its workforce'),
    ],
    'mcq': [
        ('Which countries have populations made up mainly of international migrants?', 'Qatar and the United Arab Emirates', ['Japan and South Korea', 'Niger and Chad', 'Poland and Romania'], 'Around 85-90% of residents are foreign nationals. [1]'),
        ('A country of 10 million has 60 000 immigrants and 20 000 emigrants in a year. Its net migration rate is', '+4 per 1000', ['+8 per 1000', '+40 per 1000', '−4 per 1000'], '40 000 ÷ 10 000 000 × 1000 = 4. [1]'),
        ('In which country has emigration been a major cause of population decline since 1990?', 'Bulgaria', ['Australia', 'Saudi Arabia', 'Canada'], '[1]'),
        ('At the local scale, migration often affects population change more than natural increase because', 'net migration can be large relative to a small population', ['births do not occur locally', 'death rates are zero', 'it is not recorded'], '[1]'),
    ],
    'explain': [
        ('Explain why migration is more important than natural increase for population change in some countries.', 'Very low fertility gives little natural increase (Germany, Italy) so immigration determines growth; in Gulf states labour immigration dominates; emigration causes decline in Eastern Europe or Pacific islands.', '1 mark per developed example [3]'),
        ('Explain how migration affects the age-sex structure of source and destination areas.', 'Migrants are mainly young adults (often male), so destinations gain working-age people and source areas lose them, leaving older people and children; this alters future birth rates.', '[3]'),
        ('Explain how migration can affect natural increase.', 'Immigrants are often young adults, raising birth rates and lowering death rates in destinations; source areas have fewer births.', '[2]'),
    ],
    'claims': [
        ('Natural increase always explains most population change.', False, 'In many HICs, Gulf states and some LIC regions migration is the main component.'),
        ('Migration has demographic effects in both source and receiving areas.', True, 'Age, sex and fertility patterns change in both.'),
        ('Net migration can be negative even when many people are arriving.', True, 'If more people leave than arrive, net migration is negative.'),
    ],
    'essays': [
        ('migration is now more important than natural increase in causing population change',
         ['In HICs with low fertility (Germany, Canada, UK) immigration accounts for most growth; Gulf states; emigration causes decline in Bulgaria, Latvia, Puerto Rico.'],
         ['Globally migration does not change world population; in high-fertility LICs (Niger, DRC, Pakistan) natural increase dominates; migration effects vary by scale.'],
         'Migration dominates in many HICs and at local scales, but natural increase remains the main driver of growth globally and in LICs.',
         ['scale', 'HICs and LICs', 'age structure', 'fertility']),
    ],
})


@data(c13c)
def c13c_comp(r, D):
    nm = r.choice(['Country P', 'Country Q', 'Country R', 'Country S'])
    pop = r.choice([3.5, 8.0, 15.0, 40.0, 60.0])
    cbr, cdr = r.randint(7, 30), r.randint(6, 13)
    imm = round(pop * 1e6 * r.uniform(0.002, 0.015), -3)
    emi = round(pop * 1e6 * r.uniform(0.002, 0.015), -3)
    imm, emi = int(imm), int(emi)
    if imm == emi or min(imm, emi) <= 0:
        return None
    nat = round((cbr - cdr) * pop * 1000)
    net = imm - emi
    tot = nat + net
    nmr = net / (pop * 1e6) * 1000
    stem = f'{nm} had a population of {fmt(pop, 1)} million, a crude birth rate of {cbr} per 1000 and a crude death rate of {cdr} per 1000. In the same year {nf(imm)} people immigrated and {nf(emi)} emigrated.'
    if D == 1:
        opts, a = mcq(r, f'{sgn(nmr, 1)} per 1000', [f'{sgn(-nmr, 1)} per 1000', f'{sgn(nmr * 10, 1)} per 1000', f'{sgn((imm + emi) / (pop * 1e6) * 1000, 1)} per 1000', f'{sgn(cbr - cdr, 1)} per 1000' if abs(cbr - cdr - nmr) > 0.1 else f'{sgn(nmr + 3, 1)} per 1000'])
        return {'stem': stem + ' What was the net migration rate?', 'options': opts, 'answer': a, 'key': f'({nf(imm)} − {nf(emi)}) ÷ {nf(int(pop * 1e6))} × 1000 = {dp(nmr)}. [1]'}
    parts = [
        lambda r: ('Calculate the natural increase (number of people).', f'{"−" if nat < 0 else ""}{nf(abs(nat))}', f'({cbr} − {cdr}) per 1000 × {fmt(pop, 1)} million [2]'),
        lambda r: ('Calculate the net migration and the net migration rate per 1000.', f'{"−" if net < 0 else "+"}{nf(abs(net))}; {sgn(nmr, 1)} per 1000', f'{nf(imm)} − {nf(emi)}; ÷ population × 1000 [2]'),
        lambda r: ('Calculate the total population change and state which component contributed more.', f'{"−" if tot < 0 else "+"}{nf(abs(tot))}; ' + ('natural change' if abs(nat) > abs(net) else 'migration') + ' contributed more.', 'natural change + net migration [2]'),
        lambda r: ('Suggest one demographic effect of this migration on the country.', ('Gains young adults, raising the proportion of working age and future births.' if net > 0 else 'Loses young adults, so the population ages and future births fall.'), '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[13] = [c13a, c13b, c13c]


# ============================================================== CHAPTER 14: Internal migration

c14a = T('Rural-urban migration: causes and consequences for source and destination', 'rural-urban migration causes consequences source destination')
B(c14a, {
    'terms': [
        ('rural-urban migration', 'the movement of people from the countryside to towns and cities'),
        ('rural depopulation', 'a decline in the population of rural areas, usually because of out-migration'),
        ('urban bias', 'the concentration of investment, services and jobs in cities, which encourages rural-urban migration'),
        ('hukou', 'China’s household registration system, which ties access to services to a person’s registered place of origin'),
        ('floating population', 'migrants in Chinese cities who do not have local hukou registration'),
        ('remittances (internal)', 'money sent by migrants in cities to their families in rural areas'),
    ],
    'mcq': [
        ('China’s internal migrant (“floating”) population was estimated at about', '375 million in 2020', ['3 million', '1.4 billion', '30 million'], 'Seventh national census. [1]'),
        ('Which is a consequence of rural-urban migration for the source area?', 'An ageing population and a shortage of farm labour', ['Rapid growth of informal settlements in the village', 'Overcrowded rural schools', 'Rising rural birth rates'], '[1]'),
        ('Rural-urban migration in LICs is mostly by', 'young adults', ['the elderly', 'young children alone', 'retired people'], '[1]'),
        ('Todaro’s model suggests migrants move to cities because of', 'expected (not actual) urban incomes', ['guaranteed jobs', 'lower urban wages', 'government orders'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of rural-urban migration in LICs.', 'Push: rural poverty, lack of land, mechanisation, drought and environmental degradation, few services, conflict. Pull: perceived jobs in formal and informal sectors, higher wages, schools and hospitals, bright lights, family networks.', '1 mark per factor up to [4]'),
        ('Explain the consequences of rural-urban migration for the destination city.', 'Rapid growth and informal settlements; pressure on water, sanitation, transport and schools; growth of the informal sector; youthful population; but supply of cheap labour and economic growth.', '1 mark per point [4]'),
        ('Explain the positive effects of rural-urban migration on rural source areas.', 'Remittances fund housing, education and farm improvements; reduced pressure on land; returning migrants bring skills and ideas.', '[3]'),
    ],
    'claims': [
        ('Rural-urban migration only harms rural areas.', False, 'Remittances and reduced pressure on land can benefit rural households.'),
        ('Most urban growth in LICs today is caused by migration alone.', False, 'Natural increase in cities now contributes about half or more of urban growth in many LICs.'),
        ('China’s hukou system has limited migrants’ access to urban services.', True, 'Migrants without local hukou have faced restricted access to schooling, health care and housing.'),
    ],
    'cs': [
        ('rural-urban migration in an LIC or MIC', [
            ('rural-urban migration to Dhaka, Bangladesh', {'causes': 'River erosion and flooding in districts such as Bhola and Kurigram, landlessness, cyclones and salinity in the south; pull of over 4 million garment-industry jobs; family networks.',
                                                             'impacts': 'Dhaka grew from about 6.6 million (1990) to over 23 million (2024); about 40% live in informal settlements such as Korail; pressure on water, sanitation and traffic; remittances support rural families; villages lose young adults.'}),
            ('internal migration in China', {'causes': 'Economic reforms from 1978, special economic zones (Shenzhen), factory jobs on the coast, rural incomes about a third of urban; relaxation of hukou controls.',
                                             'impacts': 'Shenzhen grew from about 30 000 (1980) to over 17 million; about 375 million internal migrants by 2020; “left-behind” children (about 60 million) and elderly in villages; urban villages and dormitories; remittances to Sichuan, Anhui and Henan.'}),
        ], [
            ('explain the causes of the migration', 'causes', 'Push and pull factors linked to named places.'),
            ('describe the consequences of the migration for the areas of origin and destination', 'impacts', 'Demographic, economic, social, environmental consequences with figures.', 'assess the extent to which rural-urban migration has benefited both the source areas and the destination.'),
        ]),
    ],
    'essays': [
        ('rural-urban migration benefits source areas more than destination cities',
         ['Remittances, reduced pressure on land and returning skills improve rural livelihoods (Bangladesh, Nepal).'],
         ['Cities gain workers that drive industrial growth (Shenzhen, Dhaka garment industry) but face informal settlements and service pressure; source areas lose young adults, farms are abandoned, families split.'],
         'Impacts are mixed in both; cities gain most economically, while source areas depend heavily on remittances and suffer demographic loss.',
         ['remittances', 'informal settlements', 'ageing', 'economic growth']),
    ],
})


@data(c14a)
def c14a_growth(r, D):
    cityn = r.choice(['Lagos', 'Dhaka', 'Kinshasa', 'Karachi', 'Nairobi', 'Lima', 'Hanoi', 'Addis Ababa'])
    p1 = r.randint(30, 140) / 10  # millions
    years = r.choice([10, 20])
    g = r.uniform(2.5, 5.0)
    p2 = round(p1 * (1 + g / 100) ** years, 1)
    inc = p2 - p1
    ni_share = r.randint(35, 65)
    ni = inc * ni_share / 100
    mig = inc - ni
    yr1 = r.choice([1990, 2000])
    stem = f'The population of {cityn} grew from {fmt(p1, 1)} million in {yr1} to {fmt(p2, 1)} million in {yr1 + years}. Natural increase within the city accounted for {ni_share}% of the growth; the rest came from net in-migration.'
    agr = ((p2 / p1) ** (1 / years) - 1) * 100
    if D == 1:
        opts, a = mcq(r, f'{dp(mig, 2)} million', [f'{dp(ni, 2)} million', f'{dp(inc, 2)} million', f'{dp(p2 * (100 - ni_share) / 100, 2)} million', f'{dp(mig / 2, 2)} million'])
        return {'stem': stem + ' How many people did net in-migration add?', 'options': opts, 'answer': a, 'key': f'growth {dp(inc, 2)} million × {100 - ni_share}% = {dp(mig, 2)} million. [1]'}
    parts = [
        lambda r: ('Calculate the population added by net in-migration.', f'{dp(mig, 2)} million', f'({fmt(p2, 1)} − {fmt(p1, 1)}) × {100 - ni_share}% [2]'),
        lambda r: ('Calculate the mean annual growth rate (compound).', f'{dp(agr, 2)}% per year', f'({fmt(p2, 1)} ÷ {fmt(p1, 1)})^(1/{years}) − 1 [3]'),
        lambda r: ('Explain why natural increase contributes a large share of urban growth.', 'Migrants are mostly young adults of child-bearing age; urban death rates are lower than rural; fertility, although lower than rural, remains above replacement.', '[2]'),
        lambda r: ('Explain two consequences of this growth for the city.', 'Informal settlements expand; shortages of water, sanitation and power; traffic congestion; informal sector employment; pressure on schools and health care.', '1 mark each with development [4]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 14.2 stepped, intra-urban, counter-urbanisation
c14b = T('Stepped migration, intra-urban movements and counter-urbanisation', 'stepped migration intra-urban movements counter-urbanisation')
B(c14b, {
    'terms': [
        ('stepped (step) migration', 'migration that takes place in stages, from village to small town to larger city'),
        ('intra-urban migration', 'movement of people from one part of a city to another'),
        ('counter-urbanisation', 'the movement of people and employment from large cities to smaller towns and rural areas'),
        ('suburbanisation', 'the outward growth of urban areas as people and services move to the edges of cities'),
        ('filtering', 'the movement of households through the housing stock, with higher-income groups moving to newer housing and their older housing passing to lower-income groups'),
        ('commuter village (dormitory settlement)', 'a rural settlement where many residents work in a nearby city and travel daily'),
    ],
    'mcq': [
        ('A migrant who moves from a village to a district town and later to the capital is an example of', 'stepped migration', ['circulation', 'counter-urbanisation', 'forced migration'], '[1]'),
        ('Counter-urbanisation was first widely observed in the', '1970s in the USA and the UK', ['1850s in Europe', '2000s in sub-Saharan Africa', '1920s in China'], '[1]'),
        ('Which factor has encouraged counter-urbanisation in HICs?', 'Improved transport and internet access allowing remote work', ['Rising rural unemployment', 'Closure of rural roads', 'Decline in car ownership'], '[1]'),
        ('Families moving from inner-city flats to new suburban houses is an example of', 'intra-urban migration', ['international migration', 'stepped migration', 'forced migration'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of counter-urbanisation.', 'Push from cities (congestion, crime, pollution, high house prices); pull of rural areas (space, quieter environment, cheaper housing); improved transport and IT enabling commuting and teleworking; retirement migration; decentralisation of employment.', '1 mark per factor [4]'),
        ('Explain why stepped migration occurs.', 'Migrants lack money and information to move directly; smaller towns are closer and offer first jobs and experience; information and contacts are gained before moving to the largest city.', '[3]'),
        ('Explain how the life cycle influences intra-urban migration.', 'Young single adults rent near the city centre; families move to suburbs for space and schools; older people may downsize or return to central areas or move to retirement areas.', '[3]'),
    ],
    'claims': [
        ('Counter-urbanisation only affects HICs.', False, 'It is also seen around some MIC cities, e.g. population moving to satellite towns beyond São Paulo or Mexico City.'),
        ('The COVID-19 pandemic encouraged some counter-urbanisation in HICs.', True, 'Remote working allowed some households to move to smaller towns and rural areas.'),
        ('Counter-urbanisation always benefits rural communities.', False, 'House prices rise beyond local people’s reach and some services close as newcomers commute.'),
    ],
    'essays': [
        ('counter-urbanisation brings more benefits than problems to rural areas',
         ['Newcomers bring spending, skills and renovated housing; schools and some services survive; population decline is reversed.'],
         ['House prices rise beyond local people’s reach; second homes and commuters leave villages empty by day; shops and bus services still close; traffic increases; conflicts over development.'],
         'The effects depend on the type of incomer and the area: accessible villages may gain, but local young people and services often lose.',
         ['house prices', 'services', 'commuting', 'second homes']),
    ],
})


@data(c14b)
def c14b_zone(r, D):
    zones = ['inner city', 'outer suburbs', 'rural ring within 50 km', 'remote rural areas']
    p1 = [r.randint(300, 900), r.randint(400, 900), r.randint(150, 400), r.randint(60, 200)]
    ch = [r.uniform(-25, -5), r.uniform(-5, 10), r.uniform(10, 35), r.uniform(-8, 12)]
    p2 = [round(a * (1 + c / 100)) for a, c in zip(p1, ch)]
    pc = [pct_change(a, b) for a, b in zip(p1, p2)]
    reg = r.choice(['a city region in the UK', 'the Paris region', 'a metropolitan area in the USA', 'a city region in Germany'])
    stem = f'Table 14.2 shows population (thousands) in zones of {reg} in 1971 and 2001: ' + '; '.join(f'{z}: {a} to {b}' for z, a, b in zip(zones, p1, p2)) + '.'
    if D == 1:
        best = max(range(4), key=lambda i: pc[i])
        opts, a = mcq(r, cap(zones[best]), [cap(z) for z in zones if z != zones[best]])
        return {'stem': stem + ' Which zone had the greatest percentage increase?', 'options': opts, 'answer': a, 'key': '; '.join(f'{z} {sgn(v)}%' for z, v in zip(zones, pc)) + ' [1]'}
    parts = [
        lambda r: ('Calculate the percentage change in population for each zone.', '; '.join(f'{z} {sgn(v)}%' for z, v in zip(zones, pc)), '(new − old) ÷ old × 100 [3]'),
        lambda r: ('Explain how the data provide evidence of counter-urbanisation.', 'Population declined in the inner city and grew fastest in the accessible rural ring, showing movement down the urban hierarchy to smaller settlements beyond the city.', '1 mark pattern; 1 mark data [2]'),
        lambda r: ('Explain the causes of the population decline in the inner city.', 'Slum clearance and redevelopment; deindustrialisation and job losses; poor environment; families moving to suburbs and rural areas for space and cheaper housing.', '1 mark per cause [3]'),
        lambda r: ('Suggest why remote rural areas may not have gained as much as the rural ring.', 'They are too far for daily commuting and have fewer services and jobs; young people still leave.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 14.3 circulation and return migration
c14c = T('Circulation and return migration', 'circulation return migration')
B(c14c, {
    'terms': [
        ('circulation', 'repeated short-term movements away from and back to a usual place of residence'),
        ('return migration', 'the movement of migrants back to their place of origin after a period living elsewhere'),
        ('seasonal migration', 'regular movement for part of the year, often to work in harvests or tourism'),
        ('pendular migration', 'regular back-and-forth movement such as weekly or daily commuting'),
        ('transhumance', 'the seasonal movement of herders and livestock between summer and winter pastures'),
        ('brain gain', 'the return of skilled migrants who bring knowledge, savings and contacts to their home area'),
    ],
    'mcq': [
        ('Migrants returning to their home village for the Chinese New Year festival is an example of', 'circulation', ['permanent migration', 'forced migration', 'counter-urbanisation'], 'Chunyun is the largest annual human movement. [1]'),
        ('Which is a common reason for return migration?', 'Retirement or reaching savings targets', ['Rising unemployment at home', 'Gaining citizenship abroad', 'Natural disasters abroad only'], '[1]'),
        ('Seasonal migration of sugar-cane cutters in Maharashtra, India is', 'temporary labour migration', ['permanent migration', 'international migration', 'refugee movement'], '[1]'),
        ('Transhumance is practised by', 'pastoralists moving livestock between seasonal pastures', ['urban commuters', 'factory workers', 'retired migrants'], '[1]'),
    ],
    'explain': [
        ('Explain the reasons for return migration.', 'Achieving savings targets; retirement; family obligations; failure to find work or discrimination; economic improvement at home; changes in immigration rules or recession abroad.', '1 mark per reason [3]'),
        ('Explain the impacts of return migration on source areas.', 'Investment of savings in housing and businesses; new skills and ideas (brain gain); but may also bring readjustment problems or unemployment if returnees cannot find work.', '[3]'),
        ('Explain why circulation is important in many LIC households.', 'It spreads risk by combining rural farming with urban wages; seasonal work fills gaps in the farming calendar; migrants keep land rights and family ties in villages.', '[3]'),
    ],
    'claims': [
        ('Circulation involves a permanent change of residence.', False, 'Circulation is movement that returns to the usual place of residence.'),
        ('Return migrants can help development in their home areas.', True, 'Their savings, skills and contacts can create businesses and jobs.'),
        ('Many Polish migrants returned home from the UK after 2008 and after the Brexit vote.', True, 'Recession, a weaker pound, Brexit uncertainty and rising wages in Poland encouraged return.'),
    ],
    'essays': [
        ('return migration brings greater benefits to source areas than remittances do',
         ['Returnees bring skills, capital, entrepreneurship and new ideas that create jobs (brain gain).'],
         ['Remittances are larger, regular and reach many more households, funding education and health (Nepal, Philippines); many returnees are elderly or unsuccessful migrants.'],
         'Remittances provide wider, more regular benefits, but skilled return migration can have a greater long-term effect on development.',
         ['remittances', 'skills', 'investment', 'scale']),
    ],
})


@data(c14c)
def c14c_survey(r, D):
    n = r.choice([40, 50, 60, 80])
    reasons = ['family obligations', 'retirement', 'savings target reached', 'could not find work', 'better opportunities at home']
    k = [r.randint(2, 20) for _ in reasons]
    s = sum(k)
    k = [max(1, round(x * n / s)) for x in k]
    k[0] += n - sum(k)
    if min(k) <= 0:
        return None
    vil = r.choice(['a village in Kerala, India', 'a town in central Mexico', 'a village in Nepal', 'a town in Ghana', 'a village in southern Poland'])
    stem = f'A survey of {n} return migrants in {vil} recorded their main reason for returning: ' + ', '.join(f'{a} {b}' for a, b in zip(reasons, k)) + '.'
    i = r.randrange(5)
    pc = k[i] / n * 100
    if D == 1:
        opts, a = mcq(r, f'{dp(pc)}%', [f'{dp(pc / 2)}%', f'{k[i]}%', f'{dp(k[i] / (n - k[i]) * 100)}%', f'{dp(pc + 10)}%'])
        return {'stem': stem + f' What percentage gave “{reasons[i]}” as their reason?', 'options': opts, 'answer': a, 'key': f'{k[i]} ÷ {n} × 100 = {dp(pc)}%. [1]'}
    parts = [
        lambda r: (f'Calculate the percentage of returnees who gave “{reasons[i]}”.', f'{dp(pc)}%', f'{k[i]} ÷ {n} × 100 [1]'),
        lambda r: (f'Calculate the angle needed for “{reasons[i]}” on a pie chart.', f'{dp(k[i] / n * 360)}°', f'{k[i]} ÷ {n} × 360 [1]'),
        lambda r: ('Suggest how the reasons could be grouped into positive and negative reasons for return.', 'Positive: savings target, retirement, better opportunities at home; negative: could not find work; family obligations can be either.', '[2]'),
        lambda r: ('Suggest two ways the survey could be improved.', 'Larger or stratified random sample; include returnees from different destinations; allow multiple reasons; pilot the questionnaire; ask about length of time away.', '1 mark each [2]'),
        lambda r: ('Explain how returnees may affect the economy of the area.', 'Investing savings in houses, land and businesses; bringing skills; creating jobs; but pressure on local jobs if many return at once.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[14] = [c14a, c14b, c14c]


# ============================================================== CHAPTER 15: International migration

REMIT = [('India', 120, 3550), ('Mexico', 66, 1790), ('Philippines', 39, 437), ('Pakistan', 27, 338), ('Bangladesh', 23, 437), ('Egypt', 20, 396),
         ('Nepal', 11, 41), ('Tajikistan', 5.7, 12), ('Guatemala', 20, 104), ('Honduras', 9.2, 34), ('Kyrgyzstan', 2.6, 14)]

c15a = T('Patterns and trends in international labour migration', 'patterns trends in international labour migration')
B(c15a, {
    'terms': [
        ('labour migration', 'movement of people across borders for the purpose of employment'),
        ('remittances', 'money sent home by migrants to families in their country of origin'),
        ('brain drain', 'the emigration of highly skilled and educated people from a country'),
        ('guest worker', 'a migrant admitted temporarily to work, such as Turkish Gastarbeiter in West Germany from 1961'),
        ('kafala system', 'a sponsorship system in Gulf states that ties migrant workers’ legal status to their employer'),
        ('migration corridor', 'a major route between a source country and a destination country, such as Mexico-USA or India-UAE'),
    ],
    'mcq': [
        ('Which country received the largest value of remittances in 2023 (about US$120 billion)?', 'India', ['Mexico', 'China', 'Nigeria'], '[1]'),
        ('The world’s largest number of international migrants live in', 'the USA (about 50 million)', ['India', 'Qatar', 'Japan'], '[1]'),
        ('Tajikistan, Tonga and Nepal are notable because', 'remittances equal a quarter or more of their GDP', ['they receive large numbers of immigrants', 'they have no emigration', 'they are HICs'], '[1]'),
        ('About how many international migrants were there in 2020?', 'About 281 million', ['About 28 million', 'About 2.8 billion', 'About 800 million'], 'UN DESA, about 3.6% of world population. [1]'),
    ],
    'explain': [
        ('Explain the growth of labour migration to the Gulf states since the 1970s.', 'Oil wealth after 1973 funded construction and services; small native populations; demand for labour in construction, domestic work and services; recruitment agencies in South and South-East Asia; wage differences of five to ten times.', '1 mark per factor [4]'),
        ('Explain how remittances can contribute to development.', 'Provide household income for food, education and health care; fund housing and small businesses; foreign exchange for the economy; more stable than aid or investment; but may increase inequality and dependency.', '1 mark per point [3]'),
        ('Explain the problems that labour migrants can face in destination countries.', 'Exploitation and low pay; poor housing; restricted rights (kafala); debt to recruiters; discrimination; separation from families.', '[3]'),
    ],
    'claims': [
        ('Remittances to LICs and MICs are larger than official development aid.', True, 'Remittances to LMICs (about US$650 billion in 2023) are several times larger than aid.'),
        ('Most international migrants move from LICs to HICs.', False, 'Many move between LICs or MICs (South-South migration), often to neighbouring countries.'),
        ('Brain drain only affects the country of origin negatively.', False, 'Remittances, diaspora investment and returning skilled migrants can bring benefits (brain gain).'),
    ],
    'essays': [
        ('international labour migration benefits source countries more than receiving countries',
         ['Remittances reduce poverty and fund development (Philippines, Nepal); emigration eases unemployment; returning migrants bring skills.'],
         ['Receiving countries gain labour for construction, care and services and pay taxes (Gulf, UK, Germany); source countries suffer brain drain of doctors and nurses, ageing and family separation.'],
         'Both gain economically, but receiving countries usually gain more in output while source countries gain income at a social cost.',
         ['remittances', 'brain drain', 'labour shortages', 'social impacts']),
    ],
})


@data(c15a)
def c15a_remit(r, D):
    rows = r.sample(REMIT, 4)
    stem = 'Table 15.1 shows approximate remittance inflows and GDP (US$ billion, 2023): ' + '; '.join(f'{n}: remittances {fmt(a, 1)}, GDP {nf(b)}' for n, a, b in rows) + '.'
    pc = [(n, a / b * 100) for n, a, b in rows]
    hi = max(pc, key=lambda x: x[1])
    big = max(rows, key=lambda x: x[1])
    if D == 1:
        n, a, b = rows[0]
        opts, ans = mcq(r, f'{dp(a / b * 100)}%', [f'{dp(b / a, 1)}%', f'{dp(a / b * 10)}%', f'{dp(a / b * 1000)}%', f'{dp(a / b * 100 + 5)}%'])
        return {'stem': stem + f' What percentage of {n}’s GDP do remittances represent?', 'options': opts, 'answer': ans, 'key': f'{fmt(a, 1)} ÷ {nf(b)} × 100 = {dp(a / b * 100)}%. [1]'}
    parts = [
        lambda r: ('Calculate remittances as a percentage of GDP for each country.', '; '.join(f'{n} {dp(v)}%' for n, v in pc), 'remittances ÷ GDP × 100 [2]'),
        lambda r: ('Identify the country most dependent on remittances and the one that receives the largest total.', f'Most dependent: {hi[0]} ({dp(hi[1])}%); largest total: {big[0]} (US${fmt(big[1], 1)} bn)', '1 mark each [2]'),
        lambda r: ('Explain why a country can receive large remittances but not be very dependent on them.', 'A large economy (high GDP) means even large remittances are a small share of national income, e.g. India or Mexico.', '[2]'),
        lambda r: ('Explain the risks of high dependence on remittances.', 'Vulnerable to recession or policy changes in destination countries (e.g. Russia for Tajikistan); may reduce incentives to develop local industry; inflation in land and housing; inequality between households.', '1 mark per point [3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 15.2 refugees
c15b = T('Refugees, asylum seekers and forced international migration', 'refugees asylum seekers forced international migration')
HOSTS = [('Iran', 3.8), ('Türkiye', 3.3), ('Colombia', 2.9), ('Germany', 2.6), ('Pakistan', 2.0), ('Uganda', 1.6)]
ORIG = [('Afghanistan', 6.4), ('Syria', 6.4), ('Venezuela', 6.1), ('Ukraine', 6.0), ('South Sudan', 2.3)]
B(c15b, {
    'terms': [
        ('refugee', 'a person who has fled their country owing to a well-founded fear of persecution, war or violence and is unable or unwilling to return'),
        ('asylum seeker', 'a person who has applied for protection as a refugee and is awaiting a decision'),
        ('non-refoulement', 'the principle that refugees must not be returned to a country where they face serious threats to their life or freedom'),
        ('UNHCR', 'the United Nations Refugee Agency, which protects and supports refugees'),
        ('protracted refugee situation', 'one in which 25 000 or more refugees from the same country have been in exile for five years or more'),
        ('resettlement', 'the transfer of refugees from a first host country to a third country that has agreed to admit them permanently'),
    ],
    'mcq': [
        ('The legal definition of a refugee comes from the', '1951 Refugee Convention', ['Kyoto Protocol', 'Paris Agreement', 'Schengen Agreement'], '[1]'),
        ('At the end of 2023, the number of forcibly displaced people worldwide was about', '117 million', ['11 million', '1.2 billion', '40 million'], 'UNHCR Global Trends. [1]'),
        ('Most refugees are hosted by', 'low- and middle-income countries neighbouring their country of origin', ['the richest European countries', 'the USA', 'countries in Oceania'], 'About 70% live in neighbouring countries. [1]'),
        ('Kakuma and Dadaab are large refugee camps in', 'Kenya', ['Jordan', 'Bangladesh', 'Turkey'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of forced international migration.', 'Armed conflict and civil war (Syria, Sudan, Ukraine); persecution of ethnic or religious groups (Rohingya); political repression; economic collapse (Venezuela); environmental disasters and climate change.', '1 mark per cause with example [4]'),
        ('Explain the impacts of large refugee inflows on host countries.', 'Pressure on housing, water, schools and health care; competition for jobs; strain on public finances; possible tension; but labour, skills, consumer spending and international aid.', '1 mark per point [4]'),
        ('Explain why many refugees remain in camps for many years.', 'Conflict continues so return is unsafe; host countries restrict work and settlement; few resettlement places are offered by third countries.', '[3]'),
    ],
    'claims': [
        ('Most refugees in the world live in Europe.', False, 'Iran, Türkiye, Colombia, Pakistan and Uganda are among the largest hosts.'),
        ('An asylum seeker and a refugee are the same thing.', False, 'An asylum seeker has applied for protection; a refugee has been recognised as needing it.'),
        ('Refugee movements can change the population structure of host areas.', True, 'Lebanon’s population grew by about a quarter with Syrian refugees after 2011.'),
    ],
    'cs': [
        ('forced international migration', [
            ('Syrian refugees since 2011', {'causes': 'Civil war from 2011; bombing of cities such as Aleppo and Homs; persecution; collapse of services; ISIS control in the east.',
                                            'impacts': 'About 6.4 million refugees by 2023: Türkiye about 3.3 million, Lebanon about 0.8-1.5 million (up to a quarter of its population), Jordan about 0.7 million (Zaatari camp), Germany about 0.8 million; pressure on services; EU-Turkey deal (2016); loss of skilled people from Syria.'}),
            ('the Rohingya from Myanmar', {'causes': 'Long-term statelessness after the 1982 citizenship law; military violence in Rakhine State in August 2017 burnt hundreds of villages.',
                                           'impacts': 'About 750 000 fled to Bangladesh in 2017; Kutupalong-Balukhali near Cox’s Bazar became the world’s largest refugee camp (about 1 million people); deforestation of hillsides, landslide risk; tension with host communities; relocation of some to Bhasan Char island.'}),
            ('Ukrainian refugees since 2022', {'causes': 'Russian invasion of February 2022; bombardment of cities such as Kharkiv and Mariupol.',
                                               'impacts': 'About 6 million refugees, mostly women and children (men 18-60 were restricted from leaving); EU Temporary Protection Directive gave rights to work; Poland and Germany hosted about 1 million each; some return as fighting moved.'}),
        ], [
            ('explain the causes of the forced migration', 'causes', 'Political, conflict, persecution, linked to places and dates.'),
            ('describe the impacts on the host countries', 'impacts', 'Numbers, camps, services, economy, politics.', 'evaluate the impacts of the forced migration on the receiving countries.'),
        ]),
    ],
    'essays': [
        ('the impacts of refugees on host countries are mainly negative',
         ['Pressure on housing, water, health care and schools (Lebanon, Bangladesh); environmental damage near camps; political tension.'],
         ['Refugees provide labour and skills, start businesses and consume goods (Syrians in Türkiye; Ukrainians in Poland); international aid flows in; long-term integration brings benefits.'],
         'Short-term impacts in poor host countries are often negative, but with rights to work and support the long-term impacts can be positive.',
         ['services', 'labour', 'aid', 'integration']),
    ],
})


@data(c15b)
def c15b_hosts(r, D):
    rows = r.sample(HOSTS, 4)
    total = 31.6
    stem = f'At the end of 2023, about {total} million refugees were under UNHCR’s mandate. Table 15.2 shows approximate numbers (millions) in selected host countries: ' + ', '.join(f'{n} {fmt(v, 1)}' for n, v in rows) + '.'
    pc = [(n, v / total * 100) for n, v in rows]
    s = sum(v for _, v in rows)
    if D == 1:
        n, v = rows[0]
        opts, a = mcq(r, f'{dp(v / total * 100)}%', [f'{dp(total / v)}%', f'{dp(v / total * 10)}%', f'{dp(v)}%', f'{dp(v / total * 100 + 6)}%'])
        return {'stem': stem + f' What percentage of these refugees were hosted by {n}?', 'options': opts, 'answer': a, 'key': f'{fmt(v, 1)} ÷ {total} × 100 = {dp(v / total * 100)}%. [1]'}
    parts = [
        lambda r: ('Calculate the percentage of refugees hosted by each country.', '; '.join(f'{n} {dp(v)}%' for n, v in pc), '÷ 31.6 × 100 [2]'),
        lambda r: ('Calculate the share hosted by these four countries together.', f'{dp(s / total * 100)}%', f'{dp(s, 1)} ÷ {total} × 100 [1]'),
        lambda r: ('Suggest why most of these hosts are neighbours of countries in conflict.', 'Refugees flee to the nearest safe country on foot or by road; cultural and language ties; cost and legal barriers prevent longer journeys.', '[2]'),
        lambda r: ('Explain the challenges faced by a lower-income host country.', 'Limited resources for shelter, water, health and schools; competition for jobs and land; environmental degradation; dependence on international aid.', '1 mark per point [3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 15.3 impacts: case study
c15c = T('Impacts of international migration: a case study of source and receiving countries', 'impacts of international migration case study source receiving countries')
B(c15c, {
    'terms': [
        ('source country', 'the country that migrants leave'),
        ('receiving (host) country', 'the country to which migrants move'),
        ('diaspora', 'people who have settled outside their country of origin but keep links with it'),
        ('multiculturalism', 'the presence and acceptance of several cultural or ethnic groups within a society'),
        ('integration', 'the process by which migrants become part of the host society while keeping their own identity'),
        ('labour shortage', 'a lack of workers with the skills needed in particular sectors of the economy'),
    ],
    'mcq': [
        ('Which receiving country has the highest proportion of migrants in its population (about 75-88%)?', 'United Arab Emirates', ['Japan', 'Brazil', 'India'], '[1]'),
        ('About how many Filipinos work overseas (Overseas Filipino Workers) at any time?', 'About 2 million on contracts, with about 10 million in the wider diaspora', ['About 20 000', 'About 200 million', 'None'], '[1]'),
        ('A benefit of emigration for a source country is', 'reduced unemployment and inflows of remittances', ['loss of skilled doctors', 'ageing population', 'family separation'], '[1]'),
        ('After Poland joined the EU in 2004, the UK', 'allowed Polish workers free access to its labour market', ['banned Polish migration', 'required work permits for all EU migrants', 'closed its borders'], '[1]'),
    ],
    'explain': [
        ('Explain the economic impacts of emigration on a source country.', 'Remittances support consumption, education and businesses; lower unemployment; foreign exchange; but loss of skilled workers (brain drain), labour shortages and dependency.', '1 mark per impact [4]'),
        ('Explain the social impacts of immigration on a receiving country.', 'Cultural diversity and new businesses; pressure on housing and schools in some areas; possible discrimination or tension; changes in population structure and birth rates.', '1 mark per impact [3]'),
        ('Explain why the impacts of migration change over time.', 'Initial pressures ease as migrants integrate; migrants age and may return; second generations change; economic cycles and policies alter flows.', '[3]'),
    ],
    'claims': [
        ('Receiving countries gain nothing from migration.', False, 'Migrants fill labour shortages, pay taxes and contribute to economic growth.'),
        ('The loss of nurses and doctors can harm health care in source countries.', True, 'For example, many nurses trained in the Philippines, Zimbabwe and Ghana work in the UK and USA.'),
        ('Migration can change the political debate in receiving countries.', True, 'Immigration was a key issue in the UK’s 2016 EU referendum.'),
    ],
    'cs': [
        ('international migration between a source and a receiving country', [
            ('migration from the Philippines (source) to the Gulf and elsewhere', {'source': 'Remittances of about US$39 billion (about 9% of GDP) in 2023; reduced unemployment; brain drain of nurses and seafarers; children brought up by relatives; government Department of Migrant Workers protects workers.',
                                                                                     'receiving': 'Filipinos fill jobs in health care, domestic work, construction and hospitality in Saudi Arabia, UAE and Qatar; concerns over the kafala system and abuse of domestic workers.'}),
            ('migration from Poland (source) to the UK (receiving)', {'source': 'Over 1 million Poles left after 2004; remittances; labour shortages in Polish construction; ageing population; many returned after 2008 and 2016 with skills and savings.',
                                                                       'receiving': 'Polish workers filled shortages in construction, food processing, farming and care; paid taxes; Polish shops and churches; pressure on some local services such as schools in Peterborough and Boston (Lincolnshire); became a political issue in the 2016 referendum.'}),
            ('migration from Mexico (source) to the USA (receiving)', {'source': 'Remittances of about US$66 billion (2023), important to states such as Michoacán and Oaxaca; rural depopulation and ageing; loss of young workers.',
                                                                         'receiving': 'About 11 million Mexican-born residents; labour for agriculture, construction and services; growth of Spanish-speaking communities; debates over undocumented migration and border security.'}),
        ], [
            ('explain the impacts of the migration on the source country', 'source', 'Economic, social, demographic impacts with figures.'),
            ('explain the impacts of the migration on the receiving country', 'receiving', 'Labour market, services, culture, politics, with figures.', 'evaluate whether the source or the receiving country has gained more from the migration.'),
        ]),
    ],
    'essays': [
        ('the costs of international migration are greater than the benefits for source countries',
         ['Brain drain of doctors and nurses (Zimbabwe, Philippines); ageing; family breakdown; labour shortages; dependency on remittances.'],
         ['Remittances exceed aid and reduce poverty; reduced unemployment; return of skilled migrants; diaspora investment and trade links (India’s IT sector).'],
         'For most source countries the economic benefits outweigh the costs, but the balance depends on how many skilled workers leave and how remittances are used.',
         ['remittances', 'brain drain', 'demographic change', 'return migration']),
    ],
})


@data(c15c, c4=False)
def c15c_uae(r, D):
    cases = [('UAE', 10.0, 88), ('Qatar', 2.7, 77), ('Kuwait', 4.9, 70), ('Saudi Arabia', 36.0, 42), ('Singapore', 5.9, 30), ('Australia', 26.5, 30), ('Canada', 39.0, 22)]
    rows = r.sample(cases, 3)
    stem = 'Table 15.3 gives approximate total population (millions) and the percentage born abroad: ' + '; '.join(f'{n}: {fmt(p, 1)} million, {m}%' for n, p, m in rows) + '.'
    nums = [(n, p * m / 100) for n, p, m in rows]
    if D == 1:
        n, p, m = rows[0]
        opts, a = mcq(r, f'{dp(p * m / 100, 2)} million', [f'{dp(p * (100 - m) / 100, 2)} million', f'{dp(p / m, 2)} million', f'{dp(p * m / 10, 1)} million', f'{dp(p * m / 100 + 1, 2)} million'])
        return {'stem': stem + f' About how many foreign-born people live in {n}?', 'options': opts, 'answer': a, 'key': f'{fmt(p, 1)} × {m}% = {dp(p * m / 100, 2)} million. [1]'}
    parts = [
        lambda r: ('Calculate the number of foreign-born residents in each country.', '; '.join(f'{n} {dp(v, 2)} million' for n, v in nums), 'population × % ÷ 100 [2]'),
        lambda r: ('Suggest why the Gulf states have such high proportions of migrants.', 'Oil wealth funds construction and services; small citizen populations; recruitment of temporary contract workers from South Asia and the Philippines; citizenship is very hard to obtain.', '[3]'),
        lambda r: ('Explain one effect of this migration on the population structure of a Gulf state.', 'Large surplus of males aged 20-50, giving a very unbalanced pyramid and sex ratio (e.g. about 2.5 males per female in Qatar).', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[15] = [c15a, c15b, c15c]


# ============================================================== CHAPTER 16: Changes in rural settlements

c16a = T('Rural settlement change in HICs: counter-urbanisation and rural depopulation', 'rural settlement change in hics counter-urbanisation rural depopulation')
B(c16a, {
    'terms': [
        ('rural depopulation', 'the decline in the population of remote rural areas, mainly through out-migration of young people'),
        ('suburbanised village', 'a village close to a city that has grown with new housing for commuters'),
        ('second home', 'a property owned in addition to a main residence, often in attractive rural or coastal areas, used for holidays'),
        ('rural-urban fringe', 'the zone of transition between the built-up urban area and the countryside'),
        ('key settlement', 'a village chosen by planners to receive investment in services so that it can serve surrounding smaller settlements'),
        ('rural deprivation', 'a lack of access to services, jobs and affordable housing in rural areas'),
    ],
    'mcq': [
        ('A remote village with an ageing population, closed school and few young adults is most likely experiencing', 'rural depopulation', ['suburbanisation', 'gentrification of the inner city', 'reurbanisation'], '[1]'),
        ('Which change is typical of a suburbanised (commuter) village?', 'New housing estates and rising house prices', ['Closure of all roads', 'Rapid growth of farm employment', 'Falling car ownership'], '[1]'),
        ('High numbers of second homes in a rural area can lead to', 'house prices rising beyond the reach of local young people', ['falling house prices', 'more year-round residents', 'new schools opening'], '[1]'),
        ('Japan’s “akiya” are', 'abandoned or empty homes, many in depopulating rural areas', ['new commuter towns', 'second homes in cities', 'rural factories'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of rural depopulation in remote areas of HICs.', 'Mechanisation reduces farm jobs; few alternative jobs; young people leave for education and work; services close as thresholds fall; poor transport; isolation.', '1 mark per cause [4]'),
        ('Explain how rural settlements near large cities have changed.', 'Growth of new housing for commuters; rising house prices; change from farming to service and commuter populations; increased traffic; some services (shops) close as people shop in cities, others (cafés, gastropubs) open.', '1 mark per change [4]'),
        ('Explain the “cycle of decline” in remote rural areas.', 'Out-migration of young adults reduces population and births; services lose thresholds and close; fewer jobs and services encourage further out-migration; the population ages.', '[3]'),
    ],
    'claims': [
        ('All rural areas in HICs are losing population.', False, 'Accessible rural areas near cities are growing through counter-urbanisation; remote areas may decline.'),
        ('Counter-urbanisation can cause the loss of rural services.', True, 'Commuters often use services in the city, so village shops and buses may still close.'),
        ('Rural areas in HICs have higher proportions of elderly people than cities.', True, 'Young adults leave and retired people move in, raising the median age.'),
    ],
    'essays': [
        ('rural areas in HICs face more problems from population growth than from population decline',
         ['Accessible villages face rising house prices, loss of character, traffic, conflict between newcomers and locals and pressure on schools and roads.'],
         ['Remote areas (Scottish Highlands, rural Japan, rural Spain) face ageing, closure of schools and shops, abandoned homes and declining services.'],
         'Both are significant; decline creates more severe long-term problems for remote areas, while growth creates manageable but contested pressures near cities.',
         ['house prices', 'services', 'ageing', 'accessibility']),
    ],
})


@data(c16a)
def c16a_village(r, D):
    kind = r.choice(['accessible', 'remote'])
    vil = r.choice(['Village A', 'Village B', 'Village C'])
    p1 = r.randint(400, 3000)
    ch = r.uniform(12, 45) if kind == 'accessible' else r.uniform(-30, -8)
    p2 = round(p1 * (1 + ch / 100))
    o1 = r.randint(12, 20)
    o2 = o1 + (r.randint(1, 6) if kind == 'accessible' else r.randint(6, 15))
    s1 = r.randint(6, 14)
    s2 = s1 + (r.randint(-2, 3) if kind == 'accessible' else -r.randint(2, min(6, s1 - 1)))
    dist = r.randint(5, 20) if kind == 'accessible' else r.randint(60, 140)
    stem = f'{vil} lies {dist} km from a major city. In 2001 it had {nf(p1)} residents, {o1}% aged 65+, and {s1} services; in 2021 it had {nf(p2)} residents, {o2}% aged 65+, and {s2} services.'
    pc = pct_change(p1, p2)
    if D == 1:
        opts, a = mcq(r, f'{sgn(pc)}%', [f'{sgn(-pc)}%', f'{sgn(pc / 2)}%', f'{sgn(p2 - p1, 0)}%', f'{sgn(pc + 10)}%'])
        return {'stem': stem + ' What was the percentage change in population?', 'options': opts, 'answer': a, 'key': f'({nf(p2)} − {nf(p1)}) ÷ {nf(p1)} × 100 = {sgn(pc)}%. [1]'}
    parts = [
        lambda r: ('Calculate the percentage change in population.', f'{sgn(pc)}%', '(2021 − 2001) ÷ 2001 × 100 [2]'),
        lambda r: ('Calculate the change in the number of people aged 65 and over.', f'{sgn(p2 * o2 / 100 - p1 * o1 / 100, 0)}', f'{nf(p2)} × {o2}% − {nf(p1)} × {o1}% [2]'),
        lambda r: ('Suggest whether the village is experiencing counter-urbanisation or rural depopulation. Use the data.', ('Counter-urbanisation: population growth close to a city, likely commuters and retirees moving in.' if kind == 'accessible' else 'Rural depopulation: falling population, ageing and loss of services in a remote location.'), '1 mark process; 1 mark data [2]'),
        lambda r: ('Explain the change in the number of services.', ('Growth in population may support some services, but commuters shop in the city, so the change is small.' if kind == 'accessible' else 'Falling population means thresholds are no longer met, so shops, schools and post offices close.'), '[2]'),
        lambda r: ('Suggest two problems the changes may cause for young local people.', ('Rising house prices; competition for housing; few local jobs.' if kind == 'accessible' else 'Lack of jobs, schools and transport; isolation; need to leave for education.'), '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 16.2 LIC rural issues
c16b = T('Rural settlement issues in LICs: services, land and rural poverty', 'rural settlement issues in lics services land rural poverty')
B(c16b, {
    'terms': [
        ('rural poverty', 'a lack of income and access to basic needs such as food, water, health care and education in rural areas'),
        ('land tenure', 'the system by which land is owned or occupied, for example freehold, tenancy, sharecropping or customary ownership'),
        ('landlessness', 'a situation in which rural households have no land of their own and depend on wage labour'),
        ('land fragmentation', 'the division of farms into many small, scattered plots, often through inheritance'),
        ('threshold population', 'the minimum number of people needed to support a service'),
        ('land grabbing', 'large-scale acquisition of farmland by investors or foreign governments, often displacing local users'),
    ],
    'mcq': [
        ('About what proportion of the world’s extremely poor people live in rural areas?', 'About four-fifths', ['About one-tenth', 'About one-third', 'None'], 'World Bank estimate. [1]'),
        ('Which is a cause of land fragmentation?', 'Division of land equally among heirs', ['Land consolidation schemes', 'Mechanisation', 'Large-scale plantations'], '[1]'),
        ('Rural services in LICs are often limited because', 'population is dispersed and incomes are low, so thresholds are not met', ['rural people do not need services', 'rural areas are densely populated', 'transport is too good'], '[1]'),
        ('Mobile money services such as M-Pesa in Kenya have helped rural households by', 'allowing them to receive remittances and make payments without banks', ['providing free land', 'replacing farming', 'stopping migration'], '[1]'),
    ],
    'explain': [
        ('Explain why many rural households in LICs remain poor.', 'Small, fragmented plots; insecure tenure and debt; low prices for crops; lack of irrigation, credit and inputs; poor roads and markets; few non-farm jobs; climate shocks.', '1 mark per factor [4]'),
        ('Explain the problems of providing services in rural areas of LICs.', 'Dispersed population and long distances; poor roads; low incomes; difficulty attracting teachers and doctors; high costs per person.', '[3]'),
        ('Explain how improved rural infrastructure can reduce rural poverty.', 'Roads improve access to markets and services; electricity allows irrigation and small businesses; mobile phones give price information and mobile money; clean water improves health and saves time.', '[3]'),
    ],
    'claims': [
        ('Rural poverty is caused only by a lack of land.', False, 'Lack of credit, markets, infrastructure, education and secure tenure also matter.'),
        ('Women often have less secure access to land than men in rural LICs.', True, 'Customary inheritance and legal systems frequently favour men.'),
        ('Rural-urban migration can be a household strategy against rural poverty.', True, 'Remittances diversify income and reduce risk.'),
    ],
    'essays': [
        ('lack of access to land is the main cause of rural poverty in LICs',
         ['Landlessness and tiny plots limit food production (Bangladesh, Bihar); insecure tenure discourages investment; land grabs displace farmers.'],
         ['Lack of infrastructure, markets, credit, education and health care; climate shocks and conflict; low crop prices; limited non-farm employment.'],
         'Access to land is fundamental, but without infrastructure, credit and services land alone does not lift households out of poverty.',
         ['land tenure', 'infrastructure', 'credit', 'services']),
    ],
})


@data(c16b)
def c16b_land(r, D):
    groups = ['largest 10% of holdings', 'next 20%', 'middle 30%', 'smallest 40%']
    a = r.randint(40, 65)
    b = r.randint(15, 25)
    c = r.randint(8, 15)
    d = 100 - a - b - c
    if d <= 1:
        return None
    vals = [a, b, c, d]
    dist = r.choice(['a district in Bihar, India', 'a province in the Philippines', 'a region of Guatemala', 'a district in Bangladesh'])
    stem = f'Table 16.2 shows the percentage of farmland held by different groups of landholders in {dist}: ' + ', '.join(f'{g} {v}%' for g, v in zip(groups, vals)) + '.'
    ratio = (a / 10) / (d / 40)
    if D == 1:
        opts, ans = mcq(r, f'{dp(ratio)} times', [f'{dp(a / d)} times', f'{dp(ratio / 2)} times', f'{dp(ratio * 2)} times', f'{dp(ratio + 5)} times'])
        return {'stem': stem + ' How many times more land per holding does the largest 10% have on average than the smallest 40%?', 'options': opts, 'answer': ans, 'key': f'({a} ÷ 10) ÷ ({d} ÷ 40) = {dp(ratio)}. [1]'}
    cum = [sum(vals[3 - i:]) for i in range(4)]
    parts = [
        lambda r: ('Calculate how many times more land per holding the largest 10% have, on average, than the smallest 40%.', f'{dp(ratio)} times', f'({a} ÷ 10) ÷ ({d} ÷ 40) [2]'),
        lambda r: ('Calculate the cumulative percentages of land, starting with the smallest holdings, needed to draw a Lorenz curve.', f'40% of holders: {cum[0]}%; 70%: {cum[1]}%; 90%: {cum[2]}%; 100%: {cum[3]}%', '[2]'),
        lambda r: ('Describe the distribution of land.', f'Very unequal: the largest 10% of holdings have {a}% of the land, while the smallest 40% have only {d}%.', '1 mark statement; 1 mark data [2]'),
        lambda r: ('Explain how unequal land distribution contributes to rural poverty.', 'Smallholders cannot produce enough food or income; many become tenants or sharecroppers paying rent; debt to landlords; little security to invest.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 16.3 rural planning
c16c = T('Rural planning and the management of rural change', 'rural planning management of rural change')
B(c16c, {
    'terms': [
        ('key settlement policy', 'a planning policy that concentrates investment in selected villages that serve their surrounding area'),
        ('green belt', 'a zone of protected open land around a city where development is strictly controlled'),
        ('affordable housing', 'housing provided at below market price or rent for people on lower incomes'),
        ('rural diversification', 'the development of new, non-farming economic activities in rural areas, such as tourism or crafts'),
        ('integrated rural development', 'a planning approach that improves farming, infrastructure, services and employment together'),
        ('mobile services', 'services such as libraries, banks or clinics that travel between villages'),
    ],
    'mcq': [
        ('The main purpose of a green belt is to', 'prevent urban sprawl and protect the countryside', ['encourage suburban growth', 'build new towns inside cities', 'increase farm sizes'], '[1]'),
        ('Which policy helps remote villages keep services?', 'Community-run shops and mobile services', ['Closing village schools', 'Removing bus subsidies', 'Encouraging second homes'], '[1]'),
        ('The Indian MGNREGA scheme (2005) guarantees', '100 days of paid work a year to rural households', ['free land for every family', 'a pension for all farmers', 'a car for each village'], '[1]'),
        ('Rural diversification includes', 'converting barns into holiday cottages', ['increasing monoculture', 'closing local shops', 'building motorways through villages'], '[1]'),
    ],
    'explain': [
        ('Explain the advantages and disadvantages of a key settlement policy.', 'Advantages: concentrates services where thresholds can be met, cost-effective, sustains schools and clinics. Disadvantages: smaller villages lose services and decline further; residents must travel.', '1 mark each side, 1 mark development [4]'),
        ('Explain how planners can provide affordable housing in rural areas.', 'Requiring a share of affordable homes in new developments; rural exception sites; community land trusts; limiting second homes (e.g. higher taxes in Wales and Cornwall).', '[3]'),
        ('Explain how rural development schemes in LICs can reduce rural-urban migration.', 'Creating rural jobs (MGNREGA), improving roads, water, electricity, schools and clinics, credit for farmers; reducing push factors.', '[3]'),
    ],
    'claims': [
        ('Green belts have stopped all development around cities.', False, 'Development jumps beyond the green belt and some land is released; commuting increases.'),
        ('Rural diversification can reduce dependence on farming.', True, 'Tourism, crafts and services provide additional incomes.'),
        ('Rural planning in LICs only concerns agriculture.', False, 'It includes infrastructure, services, employment and land reform.'),
    ],
    'cs': [
        ('rural management', [
            ('Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA), India', {'scheme': 'Since 2005, guarantees 100 days of paid manual work a year to rural households; projects include water conservation, rural roads and land development; reached over 50 million households a year.',
                                                                                          'evaluate': 'Raised rural wages and incomes, reduced distress migration in some states and created assets such as ponds and roads; criticised for delays in wage payments, corruption and low-quality assets.'}),
            ('rural planning in a UK national park (Peak District)', {'scheme': 'Planning restricts new housing; affordable housing for local people; support for farm diversification and tourism; community transport.',
                                                                       'evaluate': 'Protects landscape and supports tourism, but high house prices and second homes still push young people out; services remain under pressure.'}),
        ], [
            ('describe the strategies used to manage rural change', 'scheme', 'Aims, measures, scale, dates.'),
            ('evaluate the success of the strategies', 'evaluate', 'Benefits and limitations with evidence.', 'assess the extent to which the management of rural change has been successful.'),
        ]),
    ],
    'essays': [
        ('rural planning is more effective in HICs than in LICs',
         ['HICs have strong planning systems (green belts, national parks, key settlement policies) and funding for services.'],
         ['HIC planning has not solved housing affordability or service decline; LIC schemes such as MGNREGA and Bangladesh’s rural electrification have transformed millions of lives.'],
         'Planning capacity is greater in HICs, but the scale of improvement achieved by some LIC rural programmes is greater.',
         ['green belts', 'services', 'employment schemes', 'funding']),
    ],
})


@data(c16c, c4=False)
def c16c_matrix(r, D):
    sites = ['Village P', 'Village Q', 'Village R']
    crit = ['population', 'road access', 'existing services', 'land available']
    sc = [[r.randint(1, 5) for _ in crit] for _ in sites]
    w = [r.choice([1, 2, 3]) for _ in crit]
    tot = [sum(a * b for a, b in zip(s, w)) for s in sc]
    if len(set(tot)) < 3:
        return None
    best = sites[tot.index(max(tot))]
    stem = ('Planners must choose one village as a key settlement for a new health centre and secondary school. Each village is scored 1-5 against four criteria, which are weighted: '
            + ', '.join(f'{c} (weight {x})' for c, x in zip(crit, w)) + '. Scores: ' + '; '.join(f'{s}: ' + ', '.join(str(v) for v in row) for s, row in zip(sites, sc)) + '.')
    if D == 1:
        opts, a = mcq(r, best, [s for s in sites if s != best] + ['All score equally'])
        return {'stem': stem + ' Which village has the highest weighted score?', 'options': opts, 'answer': a, 'key': '; '.join(f'{s} {t}' for s, t in zip(sites, tot)) + ' [1]'}
    parts = [
        lambda r: ('Calculate the weighted total for each village.', '; '.join(f'{s} {t}' for s, t in zip(sites, tot)), 'Σ score × weight [2]'),
        lambda r: ('State which village should be chosen.', best, '[1]'),
        lambda r: ('Suggest two limitations of using a weighted matrix to make this decision.', 'Weights and scores are subjective; important factors (e.g. community views, environmental impact) may be left out; small differences may not be meaningful.', '1 mark each [2]'),
        lambda r: ('Explain one disadvantage of the key settlement policy for the villages not chosen.', 'They lose investment and services, so residents must travel further and the villages may decline further.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[16] = [c16a, c16b, c16c]


# ============================================================== CHAPTER 17: Urban trends and issues of urbanisation

URB = [('UK', 79, 84), ('Japan', 53, 92), ('Brazil', 36, 87), ('China', 12, 64), ('India', 17, 35), ('Nigeria', 10, 53), ('Kenya', 6, 29), ('Bangladesh', 4, 39), ('Mexico', 43, 81), ('Ethiopia', 5, 22)]

c17a = T('Urbanisation, suburbanisation, counter-urbanisation and re-urbanisation', 'urbanisation suburbanisation counter-urbanisation re-urbanisation')
B(c17a, {
    'terms': [
        ('urbanisation', 'an increase in the proportion of a population living in urban areas'),
        ('urban growth', 'an increase in the number of people living in urban areas or in the area covered by towns'),
        ('suburbanisation', 'the outward spread of urban areas as people, housing and services move to the edge of a city'),
        ('re-urbanisation', 'the movement of people back into city centres after a period of decline'),
        ('cycle of urbanisation', 'the sequence of urbanisation, suburbanisation, counter-urbanisation and re-urbanisation'),
        ('urban sprawl', 'the uncontrolled spread of low-density urban development into the surrounding countryside'),
    ],
    'mcq': [
        ('In about which year did more than half of the world’s population first live in urban areas?', '2007', ['1950', '1980', '2050'], 'UN estimate. [1]'),
        ('Re-urbanisation in cities such as Manchester and London since the 1990s has been encouraged by', 'regeneration of brownfield sites and city-centre apartments', ['closure of city-centre universities', 'new green belts in city centres', 'rising crime in suburbs only'], '[1]'),
        ('Which region has the fastest current rate of urbanisation?', 'Sub-Saharan Africa', ['Western Europe', 'North America', 'Australia'], '[1]'),
        ('About what percentage of the world’s population was urban in 2020?', '56%', ['30%', '80%', '95%'], '[1]'),
    ],
    'explain': [
        ('Explain the difference between urbanisation and urban growth.', 'Urbanisation is an increase in the proportion of people living in urban areas; urban growth is an increase in the urban population or area, which can occur without urbanisation if rural population grows as fast.', '[2]'),
        ('Explain the causes of suburbanisation in HICs.', 'Improved transport (railways, cars, roads); rising incomes; desire for space and gardens; cheaper land; planned housing estates; decline of inner-city environments.', '1 mark per cause [4]'),
        ('Explain the causes of re-urbanisation.', 'Regeneration of inner cities and waterfronts; gentrification; new jobs in services; young professionals and students; government policies (brownfield targets); city-centre amenities.', '1 mark per cause [3]'),
    ],
    'claims': [
        ('All countries pass through the cycle of urbanisation at the same time.', False, 'HICs urbanised in the 19th-20th centuries; many LICs are urbanising rapidly now.'),
        ('Urban growth in LICs today is faster than it was in HICs during the Industrial Revolution.', True, 'Growth rates of 4-5% a year in some African cities exceed those of 19th-century Europe.'),
        ('Counter-urbanisation and re-urbanisation can happen at the same time.', True, 'Different groups move in different directions, e.g. families leave while young professionals move into city centres.'),
    ],
    'essays': [
        ('the cycle of urbanisation is equally applicable to cities in HICs and LICs',
         ['Many MIC cities show suburbanisation (Bangkok, São Paulo) and some re-urbanisation of centres; the sequence is visible in HIC cities such as London.'],
         ['Most LIC cities are still in rapid urbanisation, driven by migration and natural increase; informal growth at the periphery is not suburbanisation in the HIC sense; counter-urbanisation is rare.'],
         'The cycle describes HIC experience well but only partly fits LIC cities, which are at different stages and grow through different processes.',
         ['suburbanisation', 'informal settlements', 're-urbanisation', 'stage of development']),
    ],
})


@data(c17a)
def c17a_urb(r, D):
    rows = r.sample(URB, 4)
    stem = 'Table 17.1 shows the percentage of the population living in urban areas in 1950 and 2020: ' + '; '.join(f'{n}: {a}% to {b}%' for n, a, b in rows) + '.'
    chg = [(n, b - a) for n, a, b in rows]
    rel = [(n, b / a) for n, a, b in rows]
    fast = max(chg, key=lambda x: x[1])
    if [c for _, c in chg].count(fast[1]) > 1:
        return None
    if D == 1:
        opts, a = mcq(r, fast[0], [n for n, _ in chg if n != fast[0]])
        return {'stem': stem + ' Which country had the largest increase in percentage points?', 'options': opts, 'answer': a, 'key': '; '.join(f'{n} +{c}' for n, c in chg) + ' [1]'}
    parts = [
        lambda r: ('Calculate the change in percentage points for each country.', '; '.join(f'{n} +{c}' for n, c in chg), '[2]'),
        lambda r: ('Calculate how many times greater the urban share was in 2020 than in 1950 for each country.', '; '.join(f'{n} {dp(v, 1)} times' for n, v in rel), '2020 ÷ 1950 [2]'),
        lambda r: ('Describe the differences in the level and rate of urbanisation between the countries.', 'HICs were already highly urbanised in 1950 and changed little; MICs urbanised rapidly; LICs still have low levels but are urbanising fast.', '1 mark per point with data [3]'),
        lambda r: ('Explain why urbanisation is slowing in some countries.', 'A high proportion is already urban; counter-urbanisation; fewer rural people left to migrate.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 17.2 megacities and world cities
c17b = T('The growth of megacities and world cities', 'growth of megacities world cities')
MEGA = [('Tokyo', 37.1), ('Delhi', 33.8), ('Shanghai', 29.9), ('Dhaka', 23.9), ('São Paulo', 22.8), ('Cairo', 22.6), ('Mexico City', 22.5), ('Beijing', 22.2), ('Mumbai', 21.7), ('Lagos', 16.5)]
PRIM = [('Thailand', 'Bangkok', 11.2, 'Chiang Mai', 1.2), ('Peru', 'Lima', 11.3, 'Arequipa', 1.1), ('UK', 'London', 9.6, 'Manchester', 2.8), ('Argentina', 'Buenos Aires', 15.6, 'Córdoba', 1.6),
        ('Kenya', 'Nairobi', 5.3, 'Mombasa', 1.4), ('Mexico', 'Mexico City', 22.5, 'Guadalajara', 5.3), ('India', 'Delhi', 33.8, 'Mumbai', 21.7), ('Brazil', 'São Paulo', 22.8, 'Rio de Janeiro', 13.8)]
B(c17b, {
    'terms': [
        ('megacity', 'an urban area with a population of more than 10 million'),
        ('world (global) city', 'a city with major influence on the global economy through finance, trade, culture and decision-making, such as London, New York or Tokyo'),
        ('primate city', 'a city that is much larger than the next largest city in the country and dominates its economy and politics'),
        ('rank-size rule', 'the idea that the nth largest city in a country has a population of 1/n of the largest city'),
        ('megalopolis', 'a very large urban region formed by the merging of several cities, such as the BosWash corridor'),
        ('urban primacy', 'the dominance of a country’s largest city over its urban system'),
    ],
    'mcq': [
        ('Which city was the largest urban agglomeration in the world in the early 2020s?', 'Tokyo', ['Lagos', 'London', 'Paris'], 'About 37 million (UN). [1]'),
        ('Which of these is usually classed as an alpha++ world city?', 'London', ['Dhaka', 'Kinshasa', 'Karachi'], 'GaWC classification with New York. [1]'),
        ('Most new megacities since 1990 have been in', 'Asia and Africa', ['Europe', 'North America', 'Oceania'], '[1]'),
        ('A country where the largest city is ten times larger than the second city shows', 'high urban primacy', ['the rank-size rule exactly', 'counter-urbanisation', 'low urbanisation'], '[1]'),
    ],
    'explain': [
        ('Explain why the number of megacities has increased.', 'Rapid urbanisation in LICs and MICs through rural-urban migration and natural increase; concentration of investment and industry; globalisation; agglomeration of services.', '1 mark per factor [3]'),
        ('Explain the characteristics that make a city a world city.', 'Headquarters of TNCs and banks; stock exchanges; international airports and connectivity; cultural influence; international organisations; global media.', '1 mark per characteristic [3]'),
        ('Explain the problems faced by megacities in LICs.', 'Informal settlements; inadequate water, sanitation and waste disposal; traffic congestion and air pollution; unemployment and informal work; crime; flood and hazard risk.', '1 mark per problem [4]'),
    ],
    'claims': [
        ('All megacities are world cities.', False, 'Some megacities such as Dhaka or Kinshasa have large populations but little global economic influence.'),
        ('Primate cities can concentrate investment at the expense of other regions.', True, 'Bangkok and Lima dominate their national economies, widening regional inequality.'),
        ('Most of the world’s urban population lives in megacities.', False, 'Most live in cities of under 1 million.'),
    ],
    'essays': [
        ('the problems of megacities outweigh their benefits',
         ['Congestion, pollution (Delhi), informal housing (Mumbai’s Dharavi), water shortages, flooding (Jakarta), inequality.'],
         ['Megacities generate a large share of national GDP, innovation and jobs; economies of scale make services cheaper per person; they offer opportunities to migrants; well-managed examples (Tokyo).'],
         'Problems are severe in fast-growing LIC megacities, but benefits are large; the balance depends on governance and investment.',
         ['economic output', 'informal settlements', 'pollution', 'governance']),
    ],
})


@data(c17b)
def c17b_prim(r, D):
    ctry, c1, p1, c2, p2 = r.choice(PRIM)
    pi = p1 / p2
    stem = f'In {ctry}, the largest city, {c1}, has a population of about {fmt(p1, 1)} million and the second city, {c2}, about {fmt(p2, 1)} million.'
    exp = p1 / 2
    if D == 1:
        opts, a = mcq(r, dp(pi, 1), [dp(p2 / p1, 2), dp(p1 - p2, 1), dp(pi * 2, 1), dp(pi + 3, 1)])
        return {'stem': stem + ' What is the primacy index (population of largest city ÷ second city)?', 'options': opts, 'answer': a, 'key': f'{fmt(p1, 1)} ÷ {fmt(p2, 1)} = {dp(pi, 1)}. [1]'}
    parts = [
        lambda r: ('Calculate the primacy index (largest ÷ second-largest city).', dp(pi, 1), f'{fmt(p1, 1)} ÷ {fmt(p2, 1)} [1]'),
        lambda r: ('Using the rank-size rule, calculate the expected population of the second city.', f'{dp(exp, 2)} million', f'{fmt(p1, 1)} ÷ 2 [1]'),
        lambda r: ('Compare the actual population of the second city with the rank-size prediction.', f'Actual {fmt(p2, 1)} million is {"smaller" if p2 < exp else "larger"} than the predicted {dp(exp, 2)} million, so the urban system is {"dominated by a primate city" if p2 < exp else "more balanced (binary or polycentric)"}.', '[2]'),
        lambda r: ('Explain why primate cities develop.', 'Historical capital and colonial port functions; concentration of government, industry and investment; transport hubs; cumulative causation attracts migrants and firms.', '1 mark per reason [3]'),
        lambda r: ('Suggest one problem of high urban primacy for a country.', 'Regional inequality, congestion and overloaded infrastructure in the primate city, neglect of other regions.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


@data(c17b, c4=False)
def c17b_mega(r, D):
    rows = r.sample(MEGA, 5)
    rows.sort(key=lambda x: -x[1])
    stem = 'Table 17.2 shows the populations (millions, about 2023) of five megacities: ' + ', '.join(f'{n} {fmt(p, 1)}' for n, p in rows) + '.'
    tot = sum(p for _, p in rows)
    m = mean([p for _, p in rows])
    md = median([p for _, p in rows])
    if D == 1:
        opts, a = mcq(r, f'{dp(m, 2)} million', [f'{dp(md, 2)} million', f'{dp(tot, 1)} million', f'{dp(rows[0][1] - rows[-1][1], 1)} million', f'{dp(m + 2, 2)} million'])
        return {'stem': stem + ' What is the mean population?', 'options': opts, 'answer': a, 'key': f'{dp(tot, 1)} ÷ 5 = {dp(m, 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the mean and the range of the populations.', f'mean {dp(m, 2)} million; range {dp(rows[0][1] - rows[-1][1], 1)} million', '[2]'),
        lambda r: ('Calculate what percentage of these cities’ combined population lives in the largest city.', f'{dp(rows[0][1] / tot * 100)}%', f'{fmt(rows[0][1], 1)} ÷ {dp(tot, 1)} × 100 [1]'),
        lambda r: ('Suggest why population figures for megacities vary between sources.', 'Different definitions of the boundary (city proper, urban agglomeration, metropolitan region); informal settlements undercounted; census dates differ.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 17.3 informal settlements
c17c = T('Informal settlements and the informal sector in LIC cities', 'informal settlements informal sector in lic cities')
B(c17c, {
    'terms': [
        ('informal settlement', 'an area of unplanned housing built without legal permission, often lacking basic services'),
        ('informal sector', 'economic activity that is not taxed, registered or regulated by the government'),
        ('self-help scheme', 'a scheme in which residents build or improve their own homes with materials, land or loans provided by authorities'),
        ('site-and-service scheme', 'a scheme in which authorities provide plots with basic services such as water and sanitation, and residents build their own homes'),
        ('slum upgrading', 'improving existing informal settlements by adding services, paving and secure tenure rather than demolishing them'),
        ('security of tenure', 'legal protection against eviction, which encourages residents to invest in their homes'),
    ],
    'mcq': [
        ('Dharavi is a large informal settlement in', 'Mumbai', ['Rio de Janeiro', 'Nairobi', 'Lima'], '[1]'),
        ('Which is a characteristic of the informal sector?', 'Workers have no contracts, sick pay or pensions', ['All workers pay income tax', 'Jobs are in large factories with unions', 'Strict health and safety regulation'], '[1]'),
        ('About how many people lived in slums or informal settlements worldwide in the early 2020s?', 'About 1.1 billion', ['About 10 million', 'About 4 billion', 'About 100 million'], 'UN-Habitat. [1]'),
        ('Giving residents legal titles to their plots is likely to', 'encourage them to invest in improving their homes', ['increase evictions', 'reduce investment', 'prevent services being supplied'], '[1]'),
    ],
    'explain': [
        ('Explain why informal settlements develop in LIC cities.', 'Rapid in-migration and natural increase; shortage of affordable formal housing; low incomes; land on steep slopes, floodplains or near railways is vacant; lack of planning control.', '1 mark per factor [4]'),
        ('Explain the advantages and disadvantages of the informal sector.', 'Advantages: provides jobs and incomes, cheap goods and services, flexible, uses skills. Disadvantages: low and irregular pay, no rights or security, no tax revenue, unsafe conditions, child labour.', '1 mark each up to [4]'),
        ('Explain why slum upgrading is often preferred to demolition.', 'It keeps communities and livelihoods intact, is cheaper, uses residents’ labour, and avoids moving people far from work; e.g. Favela-Bairro in Rio, Kampung Improvement in Indonesia.', '[3]'),
    ],
    'claims': [
        ('Informal settlements are always places of despair.', False, 'Many are vibrant communities with businesses, social networks and gradual improvement (e.g. Dharavi’s recycling industry).'),
        ('The informal sector can make up the majority of urban employment in LICs.', True, 'In many sub-Saharan African cities over 70% of jobs are informal.'),
        ('Forced eviction is the most effective solution to informal settlements.', False, 'It destroys homes and livelihoods without addressing the housing shortage; upgrading is generally more effective.'),
    ],
    'cs': [
        ('an informal settlement', [
            ('Dharavi, Mumbai', {'conditions': 'About 1 million people in about 2.1 km²; dense housing; shared toilets (one for hundreds of people in places); but about 5000 businesses and 15 000 single-room factories (recycling, pottery, leather) with an output of several hundred million US dollars a year.',
                                 'management': 'Redevelopment plans since 2004 propose high-rise rehousing with free flats for eligible residents (Adani group project from 2022); critics fear loss of businesses and ineligible residents; NGOs support sanitation and community toilets.'}),
            ('Kibera, Nairobi', {'conditions': 'Estimates of 250 000-700 000 people; lack of piped water and sanitation (“flying toilets”); informal jobs; flooding; tenancy from absentee landlords.',
                                 'management': 'Kenya Slum Upgrading Programme (KENSUP) built blocks of flats at Soweto East; railway relocation; NGO water kiosks and bio-centres; limited impact because rents rose and many original residents did not benefit.'}),
            ('Favela-Bairro, Rio de Janeiro', {'conditions': 'About 1 in 5 Rio residents lived in favelas such as Rocinha on steep hillsides; landslide risk; crime and drug gangs; few services.',
                                               'management': 'Favela-Bairro (1994-2008) upgraded around 150 favelas with paved roads, water, sanitation, crèches and some land titles; later Morar Carioca and police pacification units; improved services but gang violence persists.'}),
        ], [
            ('describe living conditions in the settlement', 'conditions', 'Housing, services, employment, density, with figures.'),
            ('evaluate the attempts to improve the settlement', 'management', 'Schemes, dates, success and limitations.', 'assess how successful attempts to improve living conditions in informal settlements have been.'),
        ]),
    ],
    'essays': [
        ('self-help and upgrading schemes are the most effective way of improving informal settlements',
         ['Upgrading is cheaper, keeps communities and livelihoods, and uses residents’ skills (Favela-Bairro, Kampung Improvement Programme, Orangi Pilot Project in Karachi).'],
         ['Upgrading may not reach the poorest or tenants; densities remain high; some sites are hazardous and need relocation; large-scale public housing (Singapore, China) has rehoused millions.'],
         'Upgrading with secure tenure is usually most effective, but must be combined with new affordable housing and relocation from hazardous sites.',
         ['tenure', 'cost', 'community', 'hazardous sites']),
    ],
})


@data(c17c)
def c17c_survey(r, D):
    n = r.choice([40, 50, 60, 80, 100])
    items = ['piped water inside the home', 'a private toilet', 'electricity', 'a member working in the informal sector', 'a member who migrated from a rural area']
    k = [r.randint(5, n - 2) for _ in items]
    plc = r.choice(['an informal settlement in Lagos', 'a favela in São Paulo', 'a squatter area in Karachi', 'a barriada in Lima', 'an informal settlement in Manila'])
    stem = f'A survey of {n} households in {plc} found the number of households with: ' + '; '.join(f'{a}: {b}' for a, b in zip(items, k)) + '.'
    pc = [b / n * 100 for b in k]
    i = r.randrange(5)
    if D == 1:
        opts, a = mcq(r, f'{dp(pc[i])}%', [f'{dp(100 - pc[i])}%', f'{k[i]}%', f'{dp(pc[i] / 2)}%', f'{dp(min(99, pc[i] + 10))}%', f'{dp(max(1, pc[i] - 12))}%'])
        return {'stem': stem + f' What percentage of households had {items[i]}?', 'options': opts, 'answer': a, 'key': f'{k[i]} ÷ {n} × 100 = {dp(pc[i])}%. [1]'}
    parts = [
        lambda r: ('Convert each figure to a percentage of households surveyed.', '; '.join(f'{a} {dp(v)}%' for a, v in zip(items, pc)), '÷ n × 100 [2]'),
        lambda r: ('Suggest a suitable method of presenting these results.', 'A bar chart (percentages for each service), as the categories are not parts of one whole, so a pie chart is unsuitable.', '1 mark method; 1 mark justification [2]'),
        lambda r: ('Suggest how the households could be sampled to make the results representative.', 'Systematic sampling of every nth dwelling along transects, or stratified sampling by zone of the settlement; random starting point; avoid only main paths.', '[2]'),
        lambda r: ('Explain how the lack of services could affect residents’ health and livelihoods.', 'Lack of clean water and sanitation spreads diarrhoeal disease and cholera; time spent collecting water; illness reduces earnings; women and girls most affected.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[17] = [c17a, c17b, c17c]


# ============================================================== CHAPTER 18: Changing structure and management of urban settlements

c18a = T('Models of urban structure: Burgess, Hoyt and LIC city models', 'models of urban structure burgess hoyt lic city models')
B(c18a, {
    'terms': [
        ('Burgess model', 'the concentric zone model (1925) of urban land use, based on Chicago, with a CBD surrounded by rings of decreasing intensity of use'),
        ('Hoyt model', 'the sector model (1939), in which land uses develop in wedges along transport routes from the CBD'),
        ('bid-rent theory', 'the idea that land values and rents fall with distance from the CBD, so different land uses outbid each other at different distances'),
        ('central business district (CBD)', 'the commercial heart of a city, with the highest land values, offices and shops'),
        ('zone in transition', 'the zone around the CBD with old industry and housing, undergoing change'),
        ('peak land value intersection', 'the point of highest land value in a city, usually at the centre of the CBD'),
        ('multiple nuclei model', 'Harris and Ullman’s model (1945) in which a city grows around several separate centres'),
    ],
    'mcq': [
        ('In many LIC city models, the poorest housing is found', 'on the periphery, in informal settlements', ['in the CBD', 'next to the elite residential spine', 'only in the inner city'], 'Unlike Burgess, where the poor live near the centre. [1]'),
        ('The Hoyt model differs from Burgess in that land uses are arranged in', 'sectors along transport routes', ['perfect concentric rings', 'random patches', 'a single zone'], '[1]'),
        ('The Griffin-Ford model describes cities in', 'Latin America', ['North America', 'Western Europe', 'Australia'], '[1]'),
        ('Land values are highest in the CBD because', 'it is the most accessible location', ['it has the most open space', 'it is furthest from transport', 'it has the most housing'], '[1]'),
    ],
    'explain': [
        ('Explain how bid-rent theory accounts for the pattern of land use in a city.', 'Accessibility is greatest at the centre, so land values are highest; retail and offices can pay the most for central sites; industry and high-density housing outbid others further out; low-density housing and agriculture occupy the edge.', '1 mark per point [4]'),
        ('Explain the limitations of the Burgess model for modern cities.', 'Based on 1920s Chicago; ignores relief, transport routes and planning; car ownership and out-of-town retail; decentralisation and multiple centres; gentrification; LIC cities differ.', '1 mark per limitation [3]'),
        ('Describe the main features of the Griffin-Ford model of Latin American cities.', 'CBD with a commercial spine and elite residential sector along a main boulevard; zone of maturity; zone of in situ accretion; periphery of informal settlements (favelas); industrial sector; gentrification near centre in later versions.', '1 mark per feature [4]'),
    ],
    'claims': [
        ('Urban models describe every city exactly.', False, 'Models are simplifications; real cities are affected by relief, history, planning and transport.'),
        ('In LIC cities, wealthy people often live near the centre.', True, 'Elite residential areas lie close to the CBD and along a spine, with informal settlements on the edge (Griffin-Ford).'),
        ('Land values always fall evenly in all directions from the CBD.', False, 'Secondary peaks occur at suburban centres and along main roads and rail lines.'),
    ],
    'essays': [
        ('models of urban structure are no longer useful for understanding modern cities',
         ['Models are based on historical cities (Chicago 1920s-30s); decentralisation, edge cities, gentrification and globalisation have changed patterns.'],
         ['They provide a framework for comparison, explain processes (bid-rent, filtering, invasion and succession), and modified models (Griffin-Ford, multiple nuclei) describe modern and LIC cities.'],
         'Models remain useful as simplified frameworks for explaining processes, provided their assumptions and limitations are recognised.',
         ['bid-rent theory', 'LIC models', 'decentralisation', 'planning']),
    ],
})


@data(c18a)
def c18a_bidrent(r, D):
    uses = [('retail', r.randint(900, 1200), r.randint(250, 400)), ('offices and industry', r.randint(500, 700), r.randint(80, 140)), ('housing', r.randint(250, 350), r.randint(20, 40))]
    (n1, a1, b1), (n2, a2, b2), (n3, a3, b3) = uses
    x12 = (a1 - a2) / (b1 - b2)
    x23 = (a2 - a3) / (b2 - b3)
    if not (0 < x12 < x23):
        return None
    edge = a3 / b3
    stem = ('Fig. 18.1 is based on bid-rent theory. The rent (US$ per m² per year) each land use is willing to pay falls with distance d (km) from the CBD: '
            + '; '.join(f'{n}: {a} − {b}d' for n, a, b in uses) + '.')
    if D == 1:
        opts, a = mcq(r, f'{dp(x12, 2)} km', [f'{dp(x23, 2)} km', f'{dp(a1 / b1, 2)} km', f'{dp(x12 * 2, 2)} km', f'{dp(x12 + 1, 2)} km'])
        return {'stem': stem + ' At what distance from the CBD do offices and industry begin to outbid retail?', 'options': opts, 'answer': a, 'key': f'{a1} − {b1}d = {a2} − {b2}d → d = {a1 - a2} ÷ {b1 - b2} = {dp(x12, 2)} km. [1]'}
    parts = [
        lambda r: ('Calculate the distance at which offices and industry outbid retail.', f'{dp(x12, 2)} km', f'{a1} − {b1}d = {a2} − {b2}d → d = {a1 - a2} ÷ {b1 - b2} [2]'),
        lambda r: ('Calculate the distance at which housing outbids offices and industry.', f'{dp(x23, 2)} km', f'd = {a2 - a3} ÷ {b2 - b3} [2]'),
        lambda r: ('Calculate the distance beyond which no urban land use will pay rent.', f'{dp(edge, 2)} km', f'{a3} − {b3}d = 0 → d = {a3} ÷ {b3} [1]'),
        lambda r: ('Explain why retail can pay the highest rents near the CBD.', 'The centre is the most accessible point, so shops attract the most customers (high threshold and range) and make high profits; they need little space.', '[2]'),
        lambda r: ('Suggest two reasons why real cities do not show these neat zones.', 'Secondary centres and out-of-town retail; transport routes create sectors; planning controls; relief and rivers; historical land uses.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 18.2 redevelopment, gentrification, retail change
c18b = T('Urban redevelopment, gentrification and retail change', 'urban redevelopment gentrification retail change')
B(c18b, {
    'terms': [
        ('urban redevelopment', 'the clearance of old buildings and their replacement with new buildings and uses'),
        ('urban regeneration', 'the improvement of run-down urban areas through economic, social and environmental investment'),
        ('gentrification', 'the movement of higher-income people into a run-down area, improving housing but displacing lower-income residents'),
        ('brownfield site', 'previously developed land that has become vacant or derelict'),
        ('out-of-town retail park', 'a shopping centre on the edge of a city, with large stores and free parking'),
        ('decentralisation (retail)', 'the movement of shops and services away from the CBD to suburban and out-of-town locations'),
        ('flagship project', 'a large, high-profile development designed to attract further investment, such as a stadium or museum'),
    ],
    'mcq': [
        ('London Docklands was regenerated from 1981 by', 'the London Docklands Development Corporation', ['a local village council', 'the United Nations', 'a private school'], '[1]'),
        ('Which is a negative impact of gentrification?', 'Displacement of lower-income residents as rents rise', ['Improved housing quality', 'New cafés and shops', 'Increased local tax revenue'], '[1]'),
        ('The growth of online shopping has led to', 'closure of many high-street stores and growth of warehouses', ['more department stores in CBDs', 'no change in retailing', 'fewer home deliveries'], '[1]'),
        ('Bilbao’s Guggenheim Museum (1997) is an example of', 'a flagship regeneration project', ['an out-of-town retail park', 'a green belt', 'an informal settlement'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of gentrification.', 'Young professionals attracted by cheap, well-built older housing near city-centre jobs and amenities; changing lifestyles; investment by developers; regeneration policies; rising suburban costs and commuting times.', '1 mark per cause [3]'),
        ('Explain why retailing has decentralised from CBDs.', 'Car ownership; cheaper land and free parking at the edge; congestion and high rents in the CBD; large stores need space; suburbanisation of customers; online shopping.', '1 mark per reason [4]'),
        ('Explain how CBDs have responded to retail decline.', 'Pedestrianisation, improved public transport, leisure and food uses, events, conversions to housing, business improvement districts, covered shopping centres.', '[3]'),
    ],
    'claims': [
        ('Regeneration always benefits the original residents of an area.', False, 'Rising prices and new jobs requiring different skills may exclude original residents.'),
        ('Brownfield redevelopment helps protect green belts.', True, 'Reusing urban land reduces pressure to build on greenfield sites.'),
        ('The high street is dying everywhere.', False, 'Many centres have adapted with leisure, food and housing; some thrive.'),
    ],
    'cs': [
        ('urban regeneration', [
            ('London Docklands', {'scheme': 'After the docks closed (1960s-1981), the LDDC used enterprise zone tax breaks to attract investment; Canary Wharf financial district, Docklands Light Railway, Jubilee Line extension, London City Airport and luxury flats.',
                                  'evaluate': 'Created over 100 000 jobs and a major financial centre; but many jobs went to commuters with different skills; local communities faced rising house prices and loss of community; later schemes added affordable housing.'}),
            ('the regeneration of Bilbao, Spain', {'scheme': 'After the decline of shipbuilding and steel, the Bilbao Ría 2000 project cleaned the river, built the Guggenheim Museum (1997), the metro (Norman Foster) and new waterfront parks and housing.',
                                                   'evaluate': 'Tourism rose sharply (the “Guggenheim effect”), unemployment fell and the image of the city changed; costs were high and some argue benefits were unevenly shared.'}),
        ], [
            ('describe the regeneration strategies used', 'scheme', 'Projects, agencies, investment, dates.'),
            ('evaluate the success of the regeneration', 'evaluate', 'Economic, social, environmental outcomes for different groups.', 'evaluate the extent to which urban regeneration has benefited all groups of people in the area.'),
        ]),
    ],
    'essays': [
        ('gentrification brings more benefits than costs to urban areas',
         ['Improved housing and environment, new businesses and jobs, higher local tax revenue, reduced crime (Islington, Brooklyn).'],
         ['Displacement of lower-income residents and long-established businesses; loss of community and identity; rising rents; social polarisation.'],
         'Gentrification improves the physical environment but the benefits mostly go to newcomers; policies such as rent control and affordable housing are needed for wider benefit.',
         ['housing', 'displacement', 'local economy', 'policy']),
    ],
})


@data(c18b)
def c18b_price(r, D):
    area = r.choice(['an inner-city neighbourhood in London', 'a district of Berlin', 'a neighbourhood in Brooklyn, New York', 'an inner suburb of Melbourne', 'an old district of Lisbon'])
    p1 = r.randint(120, 400) * 1000
    p2 = round(p1 * r.uniform(1.6, 3.2), -3)
    w1 = r.randint(10, 25)
    w2 = w1 + r.randint(10, 30)
    yrs = r.choice([15, 20])
    pc = pct_change(p1, p2)
    agr = ((p2 / p1) ** (1 / yrs) - 1) * 100
    stem = f'In {area}, the mean house price rose from {nf(p1)} to {nf(int(p2))} (local currency units) over {yrs} years, while the percentage of residents in professional and managerial jobs rose from {w1}% to {w2}%.'
    if D == 1:
        opts, a = mcq(r, f'{dp(pc)}%', [f'{dp(p2 / p1 * 100)}%', f'{dp(pc / yrs)}%', f'{dp(pc / 2)}%', f'{dp(pc + 25)}%'])
        return {'stem': stem + ' What was the percentage increase in mean house price?', 'options': opts, 'answer': a, 'key': f'({nf(int(p2))} − {nf(p1)}) ÷ {nf(p1)} × 100 = {dp(pc)}%. [1]'}
    parts = [
        lambda r: ('Calculate the percentage increase in mean house price.', f'{dp(pc)}%', '(new − old) ÷ old × 100 [2]'),
        lambda r: ('Calculate the mean annual (compound) rate of increase in house prices.', f'{dp(agr, 2)}% per year', f'({nf(int(p2))} ÷ {nf(p1)})^(1/{yrs}) − 1 [2]'),
        lambda r: ('Explain how the data provide evidence of gentrification.', 'Rapidly rising house prices together with a growing share of professional workers show higher-income groups moving in.', '1 mark each indicator [2]'),
        lambda r: ('Explain the possible effects of these changes on long-term residents.', 'Rising rents and property taxes force out low-income tenants; loss of local shops and community ties; but owners gain from higher values and the environment improves.', '1 mark per effect [3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


# --------------------------------------------------------------- 18.3 managing urban settlements
c18c = T('Managing urban settlements: transport, housing and sustainable cities', 'managing urban settlements transport housing sustainable cities')
B(c18c, {
    'terms': [
        ('sustainable city', 'a city that meets the needs of its present residents without compromising the ability of future generations to meet theirs'),
        ('bus rapid transit (BRT)', 'a high-capacity bus system with dedicated lanes and stations, such as in Curitiba or Bogotá'),
        ('congestion charge', 'a fee charged to drive into a defined central area at busy times'),
        ('modal split', 'the percentage of journeys made by each form of transport'),
        ('compact city', 'a city with high-density, mixed-use development that reduces travel distances'),
        ('eco-city', 'a city designed to minimise environmental impact, with renewable energy, efficient buildings and green spaces'),
        ('transit-oriented development', 'high-density housing and services clustered around public transport stations'),
    ],
    'mcq': [
        ('Curitiba, Brazil, is well known for', 'its bus rapid transit system introduced in the 1970s', ['the world’s first metro', 'its congestion charge', 'its car-only motorways'], '[1]'),
        ('London introduced a congestion charge in', '2003', ['1975', '1990', '2020'], '[1]'),
        ('Singapore controls car ownership through', 'Certificates of Entitlement purchased at auction', ['banning all cars', 'free car parking', 'removing public transport'], '[1]'),
        ('Which measure most directly reduces urban sprawl?', 'Building at higher densities on brownfield sites', ['Out-of-town retail parks', 'Low-density suburbs', 'New motorways'], '[1]'),
    ],
    'explain': [
        ('Explain how cities can reduce traffic congestion.', 'Investment in public transport (metro, BRT); congestion charging and road pricing; park-and-ride; cycle lanes; car-ownership limits; mixed-use planning to reduce journeys; remote working.', '1 mark per strategy explained [4]'),
        ('Explain the features of a sustainable city.', 'Efficient public transport; renewable energy; green spaces; waste recycling; water conservation; affordable housing; local services; community participation; green jobs.', '1 mark per feature [4]'),
        ('Explain the challenges of providing housing in rapidly growing LIC cities.', 'Rapid population growth; low incomes; high land prices; lack of finance; informal land markets; limited infrastructure.', '[3]'),
    ],
    'claims': [
        ('Building more roads permanently solves congestion.', False, 'New roads often generate extra traffic (induced demand).'),
        ('Public transport can reduce urban air pollution.', True, 'Fewer car journeys mean lower emissions per passenger.'),
        ('Sustainable urban management only concerns the environment.', False, 'It also covers social equity and economic viability.'),
    ],
    'cs': [
        ('sustainable urban management', [
            ('Curitiba, Brazil', {'scheme': 'Bus rapid transit since 1974 with tube stations and dedicated lanes, carrying over 1 million passengers a day at its peak; parks created on floodplains; “Green Exchange” of rubbish for food or bus tickets; pedestrianised Rua XV de Novembro.',
                                  'evaluate': 'Lower car use and emissions than similar Brazilian cities; large green space per person; recycling high; but the BRT is now overcrowded, metropolitan growth has spread beyond planning, and informal settlements remain.'}),
            ('Singapore', {'scheme': 'Electronic road pricing (1998), car ownership certificates, extensive MRT, public housing for about 80% of residents (HDB), water recycling (NEWater), green buildings and Gardens by the Bay.',
                           'evaluate': 'Low congestion for a dense city, high public transport use and housing quality; but very high car costs, limited land and high cost of living; policies depend on strong central government.'}),
            ('Bogotá, Colombia', {'scheme': 'TransMilenio BRT (2000), over 500 km of cycle lanes (ciclorutas), Ciclovía car-free Sundays, “pico y placa” driving restrictions by number plate, library parks in poor districts.',
                                  'evaluate': 'Reduced journey times and emissions on main corridors; improved public space; but TransMilenio is overcrowded and protests have occurred; air pollution remains a problem.'}),
        ], [
            ('describe the strategies used to make the city more sustainable', 'scheme', 'Transport, housing, environment, with dates and figures.'),
            ('evaluate the success of the strategies', 'evaluate', 'Successes and limitations, for different groups.', 'assess the extent to which the city has become more sustainable.'),
        ]),
    ],
    'essays': [
        ('managing transport is the most important challenge in creating sustainable cities',
         ['Transport affects air quality, emissions, congestion, access to jobs and land use; BRT (Curitiba, Bogotá), road pricing (London, Singapore).'],
         ['Housing (informal settlements, affordability), water and sanitation, waste, energy and social equity are equally or more pressing, especially in LIC cities.'],
         'Transport is central because it shapes urban form, but sustainability requires integrated management of housing, services and energy.',
         ['public transport', 'housing', 'energy', 'equity']),
    ],
})


@data(c18c)
def c18c_modal(r, D):
    modes = ['car', 'bus or BRT', 'rail or metro', 'cycling', 'walking']
    y1 = [r.randint(35, 60), r.randint(10, 25), r.randint(5, 15), r.randint(1, 5)]
    y1.append(100 - sum(y1))
    if y1[-1] <= 2:
        return None
    sh = r.randint(5, 15)
    y2 = [y1[0] - sh, y1[1] + r.randint(0, sh), 0, y1[3] + r.randint(1, 4), 0]
    y2[2] = y1[2] + r.randint(0, max(0, sh - (y2[1] - y1[1])))
    y2[4] = 100 - sum(y2[:4])
    if y2[4] <= 1:
        return None
    cityn = r.choice(['Bogotá', 'Curitiba', 'London', 'Singapore', 'Copenhagen', 'Seoul', 'Lagos', 'Bangkok'])
    stem = f'Table 18.3 shows the modal split (% of journeys) in {cityn} before and ten years after a new transport strategy: ' + '; '.join(f'{m}: {a}% to {b}%' for m, a, b in zip(modes, y1, y2)) + '.'
    trips = r.choice([4, 6, 8, 10])  # million trips per day
    if D == 1:
        opts, a = mcq(r, f'{dp(trips * y2[0] / 100, 2)} million', [f'{dp(trips * y1[0] / 100, 2)} million', f'{y2[0]} million', f'{dp(trips * (100 - y2[0]) / 100, 2)} million', f'{dp(trips / y2[0], 2)} million'])
        return {'stem': stem + f' If there are {trips} million journeys a day, how many are now made by car?', 'options': opts, 'answer': a, 'key': f'{trips} × {y2[0]}% = {dp(trips * y2[0] / 100, 2)} million. [1]'}
    sust1 = y1[1] + y1[2] + y1[3] + y1[4]
    sust2 = y2[1] + y2[2] + y2[3] + y2[4]
    parts = [
        lambda r: ('Calculate the percentage of journeys made by sustainable modes (all except car) before and after.', f'{sust1}% to {sust2}%', 'sum of non-car modes [2]'),
        lambda r: (f'If there are {trips} million journeys a day, calculate the reduction in daily car journeys.', f'{dp(trips * (y1[0] - y2[0]) / 100, 2)} million', f'{trips} × ({y1[0]} − {y2[0]})% [2]'),
        lambda r: ('Suggest strategies that may have caused these changes.', 'Bus rapid transit or new metro lines; congestion charging or driving restrictions; cycle lanes and bike-share; pedestrianisation; parking controls.', '1 mark each [3]'),
        lambda r: ('Suggest why the change in car use might not reduce congestion in the long term.', 'Population and car ownership continue to grow; freed road space attracts new traffic (induced demand); journeys move to other times or routes.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[18] = [c18a, c18b, c18c]
