"""IB DP Environmental Systems and Societies SL/HL (guide for first assessment 2026) - ib-g11-environmental, year 1.

Year 1 covers Topic 1 Foundation (1.1 Perspectives, 1.2 Systems, 1.3 Sustainability), Topic 2 Ecology (2.1-2.5),
Topic 3 Biodiversity and conservation (3.1-3.3) and Topic 4 Water (4.1-4.4).

Item styles
  * C1 define / state / identify (1-2 marks), MCQ knowledge checks,
  * C2 outline / explain / distinguish / misconception (2-4 marks),
  * C3 application to named case studies (real ecosystems, fisheries, cities, policies) and data-based items in
    Paper 1 style (resource booklet extracts described in words) whose numerical answers are COMPUTED: energy
    efficiency between trophic levels, GPP/NPP/GSP/NSP, Lincoln index, Simpson's reciprocal index, population growth
    and doubling time, logistic growth, ecological footprint vs biocapacity, carbon budgets, ocean pH, MSY, BOD,
    BMWP/ASPT, nitrate load, water balance, water stress, IUCN criterion A, reserve core area, extinction rates,
    lapse rates and biome classification,
  * C4 Paper 1 evaluate [6] and Paper 2 Section B structured-essay parts (b) explain [7] and (c) evaluate / discuss /
    to what extent [9] with ESS markband keys.
Figures quoted for real places are rounded published values (FAO, IUCN, Global Footprint Network, Global Carbon
Project, Water Footprint Network, NOAA); parametric data sets are labelled as sample / survey / illustrative data.
Shared machinery (Pack, gens, markbands, MOCK) is imported by ib_g12_environmental.py.
"""
from __future__ import annotations

import math
import random

from _common import F, Registry, T, mcq, name

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}

# One mock = HL Paper 1 (unseen case study with resource booklet) + Paper 2 (Section A short-answer and data-based
# questions; Section B structured essays (a) outline [4], (b) explain [7], (c) evaluate / discuss [9]).
# 18 items, 80 marks.
MOCK = [
    dict(section='Paper 1 (unseen case study) - define / state from the resource booklet', count=2, c=['C1'], d=[1, 2], type='short', marks=2),
    dict(section='Paper 1 (unseen case study) - data analysis and calculation', count=3, c=['C3'], d=[2, 3, 3], type='numerical', marks=3, style='data'),
    dict(section='Paper 1 (unseen case study) - explain using the case study and own knowledge', count=2, c=['C3'], d=[3], type='case', marks=4, style='p1case'),
    dict(section='Paper 1 (unseen case study) - evaluate', count=1, c=['C4'], d=[4], type='long', marks=6, style='p1ev'),
    dict(section='Paper 2 Section A - short answer: outline / explain', count=3, c=['C2'], d=[2, 3], type='explain', marks=3, style='sa3'),
    dict(section='Paper 2 Section A - data-based question', count=2, c=['C3'], d=[3], type='numerical', marks=4, style='data'),
    dict(section='Paper 2 Section B - structured essay (a) outline', count=1, c=['C2'], d=[3], type='explain', marks=4, style='sa3'),
    dict(section='Paper 2 Section B - structured essay (b) explain', count=2, c=['C3'], d=[4], type='explain', marks=7, style='b7'),
    dict(section='Paper 2 Section B - structured essay (c) evaluate / discuss / to what extent', count=2, c=['C4'], d=[4, 5], type='long', marks=9, style='essay9'),
]

# ---------------------------------------------------------------------------------------------
# markbands
# ---------------------------------------------------------------------------------------------
MB9 = ('ESS markbands [9]: 7-9 the response shows a thorough understanding of concepts and correct use of terminology; '
       'a broad range of relevant knowledge; well-developed, specific examples (named, located, quantified); clear '
       'analysis; a balanced evaluation that weighs strengths and limitations from more than one perspective and a '
       'well-substantiated conclusion consistent with the arguments. 4-6 reasonable understanding and mostly correct '
       'terminology; some breadth of knowledge; examples relevant but partly developed; analysis and evaluation present '
       'but not fully balanced; a conclusion is stated but only partly supported. 1-3 limited understanding; few '
       'relevant terms; little or no use of examples; mainly descriptive with little evaluation; no clear conclusion. '
       '0 does not reach the standard described by the descriptors.')
MB6 = ('[6]: award [1] for each valid, developed evaluative point (strength or limitation) up to [4], and up to [2] for '
       'a balanced, justified conclusion; at least one point must refer explicitly to the case study for full marks.')
MB4 = ('[4]: [1] for a valid argument for and [1] for its development; [1] for a valid argument against and [1] for '
       'its development; generic points with no environmental context are capped at [2].')
MB7 = ('[7]: award [1] per valid, developed point up to [7]; credit accurate terminology, the mechanism or process, '
       'specific detail from the named example(s) and explicit links to the question; max [4] if no specific example.')


def lc(s):
    w = s.split(' ')[0].strip('"')
    if w in KEEP or w.isupper() or (len(w) > 1 and any(ch.isupper() for ch in w[1:])):
        return s
    return s[0].lower() + s[1:]


KEEP = {'Earth', 'Earth\'s', 'Gaia', 'Carson', 'Rachel', 'Lovelock', 'Indigenous', 'Chipko', 'Minamata', 'Bhopal', 'Chernobyl',
        'Lincoln', 'Simpson\'s', 'Simpson', 'Lindeman', 'Odum', 'Hadley', 'Ferrel', 'Montreal', 'Paris', 'Kyoto', 'CITES',
        'IUCN', 'Ramsar', 'Amazon', 'Arctic', 'Antarctic', 'Atlantic', 'Pacific', 'Great', 'Lake', 'Aral', 'Yellowstone',
        'Costa', 'Galápagos', 'Madagascar', 'Borneo', 'Peru', 'Peruvian', 'Grand', 'Newfoundland', 'Mekong', 'Nile',
        'Cape', 'Singapore', 'Israel', 'China', 'India', 'Brazil', 'Norway', 'Iceland', 'Japan', 'UN', 'SDGs', 'SDG',
        'EIAs', 'EIA', 'GPP', 'NPP', 'DDT', 'BOD', 'MSY', 'Gross', 'Net', 'Doughnut', 'Kate', 'Raworth', 'Hardin',
        'Easter', 'Ehrlich', 'Malthus', 'Boserup', 'Ostrom', 'Thunberg', 'Wangari', 'Maathai', 'Hawaiian', 'Māori',
        'Aboriginal', 'Bishnoi', 'Australia', 'Australian', 'Kenya', 'Europe', 'European', 'Gulf', 'Chesapeake', 'Baltic'}


def sent(x):
    x = x.strip()
    x = x[0].upper() + x[1:]
    return x if x[-1] in '.!?' else x + '.'


def mk(slot, default):
    return slot.marks or default


def r1(x):
    return f'{x:.1f}'


def r2(x):
    return f'{x:.2f}'


def comma(x):
    return f'{int(round(x)):,}'


def pick(rng, seq):
    return seq[rng.randrange(len(seq))]


# ---------------------------------------------------------------------------------------------
# parametric generators (shared registry; g12 adds its own)
# ---------------------------------------------------------------------------------------------
GENS: dict = {}          # name -> (c, (dmin, dmax), fn, type, style)


def gen(nm, c='C3', d=(1, 5), type='numerical', style='data'):
    def deco(fn):
        GENS[nm] = (c, d, fn, type, style)
        return fn
    return deco


# ---------------------------------------------------------------------------------------------
# ESS item templates built from the fact packs (Paper 1 case study, Paper 2 A and B)
# ---------------------------------------------------------------------------------------------
def ess_templates(f: F, res: list) -> list:
    out = []
    ev = f.evaluate

    if ev:
        def ev4(rng, slot):
            claim, pro, con, judge = pick(rng, ev)
            stem = pick(rng, [
                f'Outline one argument for and one argument against the view that {lc(claim)}',
                f'Give one strength and one limitation of the claim that {lc(claim)}',
                f'Briefly analyse two contrasting points of view on the statement: "{claim}"',
            ])
            return dict(stem=stem, answer=judge, type='case', marks=mk(slot, 4),
                        markingKey=f'For: {pro[0]}. Against: {con[0]}. {MB4}')
        out.append(T('C4', (2, 3), ev4, 'case', 'ev4', 'ev4'))

        def p1ev(rng, slot):
            claim, pro, con, judge = pick(rng, ev)
            stem = pick(rng, [
                f'Using the case study and your own knowledge, evaluate the view that {lc(claim)}',
                f'With reference to the resource booklet and examples you have studied, evaluate the claim: "{claim}"',
            ])
            key = ('Strengths / supporting points: ' + '; '.join(pro) + '. Limitations / counter-points: ' + '; '.join(con) +
                   f'. Conclusion: {judge} {MB6}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=mk(slot, 6))
        out.append(T('C4', (3, 4), p1ev, 'long', 'p1ev', 'p1ev'))

        def essay9(rng, slot):
            claim, pro, con, judge = pick(rng, ev)
            stem = pick(rng, [
                f'Evaluate the claim that {lc(claim)} [9]',
                f'"{claim}" Discuss this statement with reference to named examples. [9]',
                f'To what extent do you agree that {lc(claim).rstrip(".")}? [9]',
                f'Discuss, from more than one environmental value system, the view that {lc(claim)} [9]',
            ])
            key = ('Indicative content - arguments supporting the statement: ' + '; '.join(pro) +
                   '. Arguments challenging it: ' + '; '.join(con) +
                   f'. A supported conclusion might be: {judge} {MB9}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=mk(slot, 9))
        out.append(T('C4', (4, 5), essay9, 'long', 'essay9', 'essay9'))

    if res:
        def data(rng, slot):
            text, qs = pick(rng, res)
            q, a = pick(rng, qs)
            intro = pick(rng, ['Study the extract from the resource booklet.', 'Refer to the data below.',
                               'The following information comes from a case study.'])
            m = mk(slot, 2 if slot.d <= 2 else 3 if slot.d == 3 else 4)
            return dict(stem=f'{intro}\n\n{text}\n\n{q}', answer=a, type='case', marks=m, gap='G7',
                        markingKey=f'{a} Award [1] per valid point or correct step, up to [{m}]; quoted data must include '
                                   'units; points must be drawn from the resource.')
        out.append(T('C3', (2, 4), data, 'case', 'data', 'data'))

    if f.cases:
        def p1case(rng, slot):
            case, what, concept, how = pick(rng, f.cases)
            stem = pick(rng, [
                f'Case study extract - {case}: {what}\n\nUsing the extract and your own knowledge, explain how this case illustrates {concept}.',
                f'Resource booklet summary ({case}): {what}\n\nExplain what this information reveals about {concept}.',
            ])
            m = mk(slot, 4)
            return dict(stem=stem, answer=how, type='case', marks=m, gap='G7',
                        markingKey=f'{how} Award [1] for each valid point linking the extract to {concept}, up to [{m}]; '
                                   'at least one point must use detail from the extract.')
        out.append(T('C3', (2, 4), p1case, 'case', 'p1case', 'p1case'))

        def b7(rng, slot):
            case, what, concept, how = pick(rng, f.cases)
            stem = pick(rng, [
                f'Explain {concept}, referring in detail to {case} and to at least one other example you have studied. [7]',
                f'With reference to {case}, explain in detail the causes and consequences involved in {concept}. [7]',
            ])
            m = mk(slot, 7)
            ans = f'{what} {how} A second, contrasting example should be developed in the same way.'
            return dict(stem=stem, answer=ans, type='explain', marks=m,
                        markingKey=f'Indicative content: {what} {how} {MB7}')
        out.append(T('C3', (3, 5), b7, 'explain', 'b7', 'b7'))

        def casedata(rng, slot):
            case, what, concept, how = pick(rng, f.cases)
            m = mk(slot, 3)
            frames = [f'Resource booklet, data extract on {case}: "{what}"\n\nUsing evidence from the extract, analyse what it shows about {concept}.']
            if any(ch.isdigit() for ch in what):
                frames.append(f'The resource booklet states: "{what}" (source: {case}).\n\n(a) Identify one quantitative piece of evidence in the extract. (b) Use it to outline {concept}.')
            stem = pick(rng, frames)
            ans = how if stem == frames[0] else f'(a) any figure quoted from the extract with its unit/context, e.g. "{what}" (b) {how}'
            return dict(stem=stem, answer=sent(ans), type='case', marks=m, gap='G7',
                        markingKey=f'Evidence quoted from the extract with figures/units [1]; {how} [1] per valid linked point up to [{m}].')
        out.append(T('C3', (2, 4), casedata, 'case', 'data', 'casedata'))

    if f.why or f.contrast:
        def sa3(rng, slot):
            use_c = f.contrast and (not f.why or rng.random() < 0.35)
            m = mk(slot, 3)
            if use_c:
                a, b, diff = pick(rng, f.contrast)
                stem = pick(rng, [f'State two differences between {a} and {b}.',
                                  f'Compare {a} with {b}.'])
                return dict(stem=stem, answer=diff, type='explain', marks=m,
                            markingKey=f'{diff} [1] per valid, explicit comparison up to [{m}].')
            q, a = pick(rng, f.why)
            if q.startswith('Explain why'):
                q2 = 'Outline why' + q[len('Explain why'):]
            elif q.startswith('Explain how'):
                q2 = 'Outline how' + q[len('Explain how'):]
            elif q.startswith('Explain'):
                q2 = 'Outline' + q[len('Explain'):]
            else:
                q2 = 'Briefly outline: ' + q
            return dict(stem=q2, answer=a, type='explain', marks=m,
                        markingKey=f'{a} [1] per valid point, up to [{m}].')
        out.append(T('C2', (2, 4), sa3, 'explain', 'sa3', 'sa3'))
    return out


def _ext_fn(items):
    def extended(rng, slot):
        it = pick(rng, items)
        stem, ans = it[0], it[1]
        m = it[2] if len(it) > 2 else (4 if slot.d <= 3 else 6)
        ty = it[3] if len(it) > 3 else 'multi_step'
        band = MB9 if m >= 8 else MB7 if m >= 5 else '[1] per valid, developed point.'
        return dict(stem=stem, answer=ans, markingKey=f'Indicative content: {ans} {band}', type=ty, marks=m)
    return extended


class Pack:
    """Registry of fact packs, parametric gens and resources for one subject."""

    def __init__(self):
        self.R = Registry()
        self.USE: dict = {}
        self.RES: dict = {}

    def S(self, key, gens=(), res=(), **kw):
        if 'cases' in kw:
            kw['cases'] = [(c, sent(w), concept, sent(h)) for c, w, concept, h in kw['cases']]
        self.R.facts(key, F(**kw))
        self.USE[key] = list(gens)
        self.RES[key] = list(res)

    def templates(self, st):
        key = st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]
        f = self.R.f.get(key)
        out = [t for t in self.R.build(st, {'eval_marks': 9, 'essay_marks': 9, 'markband': MB9})
               if t.name not in ('evaluate', 'source', 'extended')]
        if f and f.extended:
            out.append(T('C4', (2, 5), _ext_fn(f.extended), 'multi_step', None, 'extended'))
        for g in self.USE.get(key, []):
            c, d, fn, ty, sty = GENS[g]
            out.append(T(c, d, fn, ty, sty, g))
        if f:
            out += ess_templates(f, self.RES.get(key, []))
        return out


P = Pack()
S = P.S
R = P.R


def init(subject_id):
    pass


def templates(st):
    return P.templates(st)


# =============================================================================================
# Parametric generators - every answer is computed
# =============================================================================================
LINCOLN = [('woodlice', 'under logs in a school woodland', 'a dot of non-toxic paint on the carapace'),
           ('freshwater shrimps (Gammarus pulex)', 'in a riffle section of a chalk stream', 'a small nick in the tail fan'),
           ('grasshoppers', 'in an unmown meadow', 'a spot of correction fluid on the thorax'),
           ('bank voles', 'in a beech woodland using Longworth traps', 'a small fur clip'),
           ('ground beetles', 'caught in pitfall traps on a heathland', 'a dot of enamel paint on the elytra'),
           ('garden snails', 'along a hedgerow', 'a numbered dot of nail varnish on the shell'),
           ('brown trout', 'in a 200 m reach of an upland river', 'a fin clip'),
           ('common lizards', 'on a coastal sand-dune system', 'a photograph of the unique belly pattern')]


@gen('lincoln')
def g_lincoln(rng, slot):
    sp_, where, how = pick(rng, LINCOLN)
    n_true = rng.choice([80, 120, 150, 200, 240, 300, 360, 450, 600])
    m1 = rng.randint(max(15, n_true // 12), max(25, n_true // 4))
    c2 = rng.randint(max(15, n_true // 12), max(25, n_true // 4))
    r = max(1, round(m1 * c2 / n_true))
    if r >= min(m1, c2):
        return None
    N = m1 * c2 / r
    who = name(rng)
    head = pick(rng, [
        f'{who} investigated a population of {sp_} {where}. In the first sample {m1} individuals were caught, marked with {how} and released. A day later a second sample of {c2} was caught, of which {r} were marked.',
        f'A student group used capture-mark-release-recapture on {sp_} {where}: first sample {m1} (all marked with {how}); second sample {c2}, including {r} marked animals.',
        f'Data from a mark-recapture survey of {sp_} {where}: number marked and released (M) = {m1}; number caught in the second sample (C) = {c2}; number of marked individuals recaptured (R) = {r}.',
    ])
    if slot.d <= 2:
        return dict(stem=f'{head} Calculate the estimated population size using the Lincoln index.',
                    answer=f'N = M × C / R = {m1} × {c2} / {r} ≈ {N:.0f}',
                    markingKey=f'M1 correct substitution into N = (M × C) / R; A1 {N:.0f} (accept {math.floor(N)}-{math.ceil(N)}).', marks=mk(slot, 2))
    if slot.d == 3:
        return dict(stem=f'{head} (a) Estimate the population size using the Lincoln index. (b) State two assumptions of the method.',
                    answer=f'(a) {m1} × {c2} / {r} ≈ {N:.0f} (b) e.g. marks are not lost and do not affect survival or behaviour; marked individuals mix fully with the population; no births, deaths or migration between samples; equal chance of capture.',
                    markingKey=f'(a) M1 substitution, A1 ≈ {N:.0f}. (b) [1] each for two valid assumptions.', marks=mk(slot, 4))
    lost = rng.choice([0.2, 0.25, 0.3])
    r2_ = max(1, round(r * (1 - lost)))
    if r2_ == r:
        return None
    N2 = m1 * c2 / r2_
    return dict(stem=f'{head} (a) Estimate the population size. (b) A later check showed that about {int(lost * 100)}% of the marks had rubbed off or been predated, so only {r2_} marked animals would have been found had marks been retained differently. Calculate the estimate using R = {r2_} and explain how loss of marks biases the Lincoln index. (c) Suggest one improvement to the method.',
                answer=f'(a) ≈ {N:.0f} (b) {m1} × {c2} / {r2_} ≈ {N2:.0f}; losing marks lowers R, so the population is OVER-estimated. (c) e.g. use a more durable, non-toxic mark; shorten the interval between samples; repeat sampling and take a mean; check marks do not increase predation.',
                markingKey=f'(a) A1 {N:.0f}. (b) A1 {N2:.0f}; R1 fewer recaptures counted as marked → smaller denominator → overestimate. (c) R1 valid improvement linked to an assumption.', marks=mk(slot, 6))


SIMPSON_SITES = [
    ('a rocky shore at mid-tide level', ['barnacles', 'limpets', 'dog whelks', 'mussels', 'periwinkles', 'beadlet anemones']),
    ('a freshwater pond (kick-sample)', ['water boatmen', 'mayfly nymphs', 'pond snails', 'caddisfly larvae', 'water louse', 'damselfly nymphs']),
    ('a lowland meadow (ten 1 m² quadrats)', ['meadow buttercup', 'ribwort plantain', 'red clover', 'yarrow', 'common knapweed', 'oxeye daisy']),
    ('leaf litter in a tropical forest plot', ['ants', 'springtails', 'mites', 'beetles', 'spiders', 'millipedes']),
    ('a coral reef transect (fish counts)', ['parrotfish', 'damselfish', 'butterflyfish', 'wrasse', 'surgeonfish', 'groupers']),
    ('an urban park lawn', ['perennial ryegrass', 'white clover', 'dandelion', 'daisy', 'greater plantain', 'creeping buttercup']),
]


def simpson(ns):
    N = sum(ns)
    return N * (N - 1) / sum(n * (n - 1) for n in ns)


@gen('simpson')
def g_simpson(rng, slot):
    site, spp = pick(rng, SIMPSON_SITES)
    k = 4 if slot.d <= 2 else 5 if slot.d == 3 else 6
    sp_ = spp[:k]
    ns = [rng.randint(2, 30) for _ in sp_]
    if sum(n * (n - 1) for n in ns) == 0:
        return None
    D = simpson(ns)
    N = sum(ns)
    tab = '; '.join(f'{s} {n}' for s, n in zip(sp_, ns))
    formula = 'D = N(N − 1) / Σn(n − 1)'
    if slot.d <= 3:
        stem = pick(rng, [f'Sample counts from {site}: {tab}. Calculate Simpson\'s reciprocal index of diversity, {formula}.',
                          f'A survey of {site} recorded the following numbers of individuals: {tab}. Using {formula}, calculate the diversity index for the site.',
                          f'Field data ({site}): {tab}. Determine Simpson\'s diversity index (D = N(N−1)/Σn(n−1)) to two decimal places.'])
        sn = sum(n * (n - 1) for n in ns)
        return dict(stem=stem, answer=f'N = {N}; Σn(n − 1) = {sn}; D = {N}×{N - 1}/{sn} = {D:.2f}',
                    markingKey=f'M1 N = {N} and Σn(n−1) = {sn}; A1 D = {D:.2f}.' + (' ' if slot.d < 3 else ' A1 correct rounding/working shown.'),
                    marks=mk(slot, 2 if slot.d <= 2 else 3))
    ns2 = ns[:]
    # second site dominated by one species
    ns2 = [max(1, n // 4) for n in ns2]
    ns2[0] = sum(ns) - sum(ns2[1:])
    if ns2[0] <= 0:
        return None
    D2 = simpson(ns2)
    tab2 = '; '.join(f'{s} {n}' for s, n in zip(sp_, ns2))
    hi = 'Site X' if D > D2 else 'Site Y'
    return dict(stem=f'Two areas of {site} were sampled. Site X: {tab}. Site Y (next to a nutrient-rich outfall): {tab2}. (a) Calculate Simpson\'s reciprocal index ({formula}) for each site. (b) Compare the two sites and explain the difference in terms of richness and evenness. (c) Suggest why a high index is often taken to indicate a stable, undisturbed community.',
                answer=f'(a) X: D = {D:.2f}; Y: D = {D2:.2f} (b) both have the same richness ({k} species) but {hi} has the higher index because individuals are spread more evenly; at Y one species ({sp_[0]}) dominates. (c) many species and even abundances suggest complex food webs and no single stress favouring tolerant species.',
                markingKey=f'(a) A1 X {D:.2f}, A1 Y {D2:.2f}. (b) R1 same richness, R1 evenness explains the difference. (c) R1 stability / complex interactions; disturbance or pollution favours a few tolerant species.', marks=mk(slot, 6))


GROWTH_POP = [('a population of duckweed (Lemna) fronds in a laboratory tank', 'fronds'),
              ('a herd of red deer on a Scottish island with no predators', 'deer'),
              ('the number of breeding pairs of white storks in a nature reserve', 'pairs'),
              ('an introduced population of cane toads in a region of northern Australia', 'toads'),
              ('a colony of grey seals at a protected breeding beach', 'seals'),
              ('yeast cells in a 10 cm³ culture', 'million cells')]


@gen('growth')
def g_growth(rng, slot):
    what, unit = pick(rng, GROWTH_POP)
    if slot.d <= 2:
        n0 = rng.randint(40, 400)
        pct = rng.choice([8, 12, 15, 20, 25, 35, 40, 60])
        n1 = round(n0 * (1 + pct / 100))
        g = (n1 - n0) / n0 * 100
        return dict(stem=pick(rng, [f'Over one year {what} increased from {n0} to {n1} {unit}. Calculate the percentage increase.',
                                    f'Survey data: {what} numbered {n0} {unit} in year 1 and {n1} {unit} in year 2. Calculate the percentage change.']),
                    answer=f'({n1} − {n0}) / {n0} × 100 = {g:.1f}%', markingKey=f'M1 change ÷ original × 100; A1 {g:.1f}%.', marks=mk(slot, 2))
    if slot.d == 3:
        r = rng.choice([1.5, 2, 2.5, 3.5, 4, 5, 7, 10])
        n0 = rng.randint(200, 900)
        dt = 70 / r
        return dict(stem=pick(rng, [f'{what[0].upper() + what[1:]} ({n0} {unit}) is growing exponentially at {r}% per year. (a) Use the rule of 70 to estimate the doubling time. (b) Estimate the size of the population after two doubling times.',
                                    f'An ecologist estimates that {what} grows at a constant {r}% per year from {n0} {unit}. Calculate (a) its doubling time and (b) the expected size after {2 * dt:.0f} years.']),
                    answer=f'(a) 70 / {r} ≈ {dt:.1f} years (b) {n0} × 4 = {4 * n0} {unit}',
                    markingKey=f'(a) M1 70 ÷ r, A1 {dt:.1f} years. (b) A1 two doublings = ×4 = {4 * n0}.', marks=mk(slot, 3))
    K = rng.choice([500, 800, 1000, 1200, 2000, 5000])
    r = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6])
    N = rng.choice([0.2, 0.3, 0.5, 0.7, 0.8, 0.9]) * K
    dn = r * N * (1 - N / K)
    mx = r * K / 4
    return dict(stem=pick(rng, [f'{what[0].upper() + what[1:]} follows logistic growth, dN/dt = rN(1 − N/K), with r = {r} per year and carrying capacity K = {K} {unit}. (a) Calculate the growth rate when N = {N:.0f}. (b) State the population size at which growth is fastest and calculate that maximum rate. (c) Describe and explain the shape of the S-curve as N approaches K.',
                                f'A model of {what} uses r = {r} per year and K = {K} {unit} in the logistic equation dN/dt = rN(1 − N/K). (a) Find dN/dt at N = {N:.0f}. (b) Find N and dN/dt at the inflection point. (c) Explain, with reference to limiting factors, why the growth rate falls near K.']),
                answer=f'(a) {r} × {N:.0f} × (1 − {N:.0f}/{K}) = {dn:.0f} {unit} per year (b) N = K/2 = {K // 2}; maximum dN/dt = rK/4 = {mx:.0f} {unit} per year (c) environmental resistance (food, space, disease, predation) increases with density, so birth rate falls / death rate rises until they balance at K (negative feedback).',
                markingKey=f'(a) M1 substitution, A1 {dn:.0f}. (b) A1 {K // 2}, A1 {mx:.0f}. (c) R1 limiting factors / density dependence, R1 negative feedback stabilises at K.', marks=mk(slot, 6))


TROPHIC = [('a temperate grassland', ['grasses', 'grasshoppers', 'shrews', 'barn owls']),
           ('a kelp forest off California', ['giant kelp', 'sea urchins', 'sea otters', 'orcas']),
           ('a freshwater lake', ['phytoplankton', 'zooplankton', 'perch', 'pike']),
           ('an East African savanna', ['grasses', 'zebra', 'lions', 'vultures (scavenging)']),
           ('a Southern Ocean food chain', ['diatoms', 'Antarctic krill', 'Adélie penguins', 'leopard seals']),
           ('a rice paddy in the Mekong Delta', ['rice and algae', 'brown planthoppers', 'wolf spiders', 'frogs'])]


@gen('trophic')
def g_trophic(rng, slot):
    eco, chain = pick(rng, TROPHIC)
    e0 = rng.choice([12000, 18000, 24000, 30000, 45000, 60000, 85000])
    effs = [rng.choice([5, 8, 10, 12, 15, 18, 20]) for _ in range(3)]
    levels = [e0]
    for e in effs:
        levels.append(round(levels[-1] * e / 100))
    unit = 'kJ m⁻² yr⁻¹'
    if slot.d <= 2:
        i = rng.randint(0, 1)
        eff = levels[i + 1] / levels[i] * 100
        return dict(stem=pick(rng, [f'In {eco}, the energy in {chain[i]} is {comma(levels[i])} {unit} and in {chain[i + 1]} is {comma(levels[i + 1])} {unit}. Calculate the efficiency of energy transfer between these trophic levels.',
                                    f'Energy flow data for {eco}: {chain[i]} {comma(levels[i])} {unit}; {chain[i + 1]} {comma(levels[i + 1])} {unit}. Calculate the percentage of energy transferred.']),
                    answer=f'{comma(levels[i + 1])} / {comma(levels[i])} × 100 = {eff:.1f}%',
                    markingKey=f'M1 energy at higher level ÷ energy at lower level × 100; A1 {eff:.1f}%.', marks=mk(slot, 2))
    tab = '; '.join(f'{c} {comma(v)}' for c, v in zip(chain, levels))
    if slot.d == 3:
        e1 = levels[1] / levels[0] * 100
        e2 = levels[2] / levels[1] * 100
        return dict(stem=f'Energy stored in each trophic level of {eco} ({unit}): {tab}. (a) Calculate the transfer efficiency from producers to primary consumers and from primary to secondary consumers. (b) Outline two reasons why energy is lost between trophic levels.',
                    answer=f'(a) {e1:.1f}% and {e2:.1f}% (b) e.g. energy lost as heat in respiration; not all biomass is eaten (roots, bones); not all ingested food is absorbed (egested in faeces); energy remains in dead organic matter passing to decomposers.',
                    markingKey=f'(a) A1 {e1:.1f}%, A1 {e2:.1f}%. (b) [1] each for two valid losses (respiration/heat; uneaten parts; egestion).', marks=mk(slot, 4))
    eff = rng.choice([8, 10, 12])
    top = e0 * (eff / 100) ** 3
    min_e = rng.choice([5, 10, 20])
    n = 0
    e = e0
    while e * eff / 100 >= min_e:
        e = e * eff / 100
        n += 1
    return dict(stem=f'Producers in {eco} fix {comma(e0)} {unit} as NPP. Assume an average transfer efficiency of {eff}% between all levels. (a) Calculate the energy available to tertiary consumers. (b) If a viable trophic level requires at least {min_e} {unit}, determine how many levels of consumers the ecosystem could support. (c) Use the second law of thermodynamics to explain why food chains are rarely longer than four or five links.',
                answer=f'(a) {comma(e0)} × {eff / 100}³ = {top:.1f} {unit} (b) {n} consumer levels (c) at each transfer most energy is degraded to heat through respiration and cannot be reused; energy available falls geometrically until too little remains to sustain a population.',
                markingKey=f'(a) M1 repeated ×{eff / 100}, A1 {top:.1f}. (b) A1 {n}. (c) R1 second law / entropy, heat lost in respiration; R1 energy declines with each level so higher levels are limited.', marks=mk(slot, 6))


PROD = [('a dairy cow grazing a pasture', 'grass', 'kJ per day'),
        ('a cabbage white caterpillar feeding on cabbage leaves in a laboratory', 'cabbage leaf', 'J per day'),
        ('a herd of wildebeest in the Serengeti', 'grass', 'MJ km⁻² day⁻¹'),
        ('juvenile tilapia in a fish farm pond', 'pellet feed', 'kJ per day'),
        ('a population of snowshoe hares in boreal forest', 'browse (twigs and shoots)', 'kJ m⁻² yr⁻¹')]
PLANT = [('a tropical rainforest in Borneo', 'g m⁻² yr⁻¹'), ('a temperate deciduous forest in Germany', 'g m⁻² yr⁻¹'),
         ('a salt marsh in the Wadden Sea', 'g m⁻² yr⁻¹'), ('a field of maize in Iowa', 'g m⁻² yr⁻¹'),
         ('arctic tundra in Svalbard', 'g m⁻² yr⁻¹'), ('a seagrass meadow in Shark Bay', 'g m⁻² yr⁻¹')]


@gen('productivity')
def g_productivity(rng, slot):
    if slot.d <= 2 or rng.random() < 0.35:
        eco, u = pick(rng, PLANT)
        gpp = rng.randint(4, 60) * 100
        rp = round(gpp * rng.uniform(0.35, 0.75) / 10) * 10
        npp = gpp - rp
        if slot.d <= 2:
            if rng.random() < 0.5:
                return dict(stem=f'The gross primary productivity of {eco} is {comma(gpp)} {u} and plant respiration uses {comma(rp)} {u}. Calculate the net primary productivity.',
                            answer=f'NPP = GPP − R = {comma(gpp)} − {comma(rp)} = {comma(npp)} {u}',
                            markingKey=f'M1 NPP = GPP − R; A1 {comma(npp)} {u}.', marks=mk(slot, 2))
            return dict(stem=f'In {eco}, GPP = {comma(gpp)} {u} and NPP = {comma(npp)} {u}. Calculate the energy (as dry biomass) used in plant respiration.',
                        answer=f'R = GPP − NPP = {comma(gpp)} − {comma(npp)} = {comma(rp)} {u}',
                        markingKey=f'M1 R = GPP − NPP; A1 {comma(rp)} {u}.', marks=mk(slot, 2))
        pct = npp / gpp * 100
        return dict(stem=f'{eco[0].upper() + eco[1:]} has GPP = {comma(gpp)} {u} and R = {comma(rp)} {u}. (a) Calculate NPP. (b) Calculate the percentage of GPP available to herbivores as NPP. (c) Explain why NPP rather than GPP determines the biomass available to consumers.',
                    answer=f'(a) {comma(npp)} {u} (b) {pct:.1f}% (c) energy used in the producers\' own respiration is lost as heat; only NPP is stored as new biomass that can be eaten.',
                    markingKey=f'(a) A1 {comma(npp)}. (b) A1 {pct:.1f}%. (c) R1 respiration loss, R1 only stored biomass passes on.', marks=mk(slot, 4))
    eco, food, u = pick(rng, PROD)
    eaten = rng.randint(20, 90) * 10
    fae = round(eaten * rng.uniform(0.25, 0.6) / 5) * 5
    gsp = eaten - fae
    resp = round(gsp * rng.uniform(0.5, 0.85) / 5) * 5
    nsp = gsp - resp
    if nsp <= 0:
        return None
    eff = nsp / eaten * 100
    return dict(stem=pick(rng, [f'Energy budget for {eco}: {food} eaten {eaten} {u}; energy lost in faeces {fae} {u}; energy used in respiration {resp} {u}. (a) Calculate gross secondary productivity (GSP). (b) Calculate net secondary productivity (NSP). (c) Calculate the percentage of the food eaten that becomes new biomass and suggest why it is low.',
                                f'An investigation of {eco} measured: food ({food}) ingested {eaten} {u}; faecal loss {fae} {u}; respiratory loss {resp} {u}. Determine (a) GSP, (b) NSP and (c) the efficiency of conversion of ingested food into biomass, commenting on your answer.']),
                answer=f'(a) GSP = food eaten − faecal loss = {eaten} − {fae} = {gsp} {u} (b) NSP = GSP − R = {gsp} − {resp} = {nsp} {u} (c) {eff:.1f}%; most assimilated energy is respired (movement, homeostasis, in endotherms keeping warm) and lost as heat.',
                markingKey=f'(a) M1 GSP = food eaten − faecal loss, A1 {gsp}. (b) A1 {nsp}. (c) A1 {eff:.1f}%; R1 respiration/heat loss (higher in endotherms).', marks=mk(slot, 5))


BIOMAG = [('DDT', ['water', 'zooplankton', 'small fish (silversides)', 'large fish (needlefish)', 'ospreys']),
          ('methylmercury', ['seawater', 'phytoplankton', 'zooplankton', 'herring', 'harbour seals']),
          ('PCBs', ['Arctic seawater', 'zooplankton', 'Arctic cod', 'ringed seals', 'polar bears']),
          ('dieldrin', ['soil', 'earthworms', 'song thrushes', 'sparrowhawks'])]


@gen('biomag')
def g_biomag(rng, slot):
    chem, chain = pick(rng, BIOMAG)
    c0 = rng.choice([0.00005, 0.0001, 0.0002, 0.0005])
    facts = [rng.choice([40, 80, 100, 200, 500, 800])] + [rng.choice([3, 5, 8, 10, 12, 15]) for _ in chain[2:]]
    conc = [c0]
    for f_ in facts:
        conc.append(conc[-1] * f_)
    conc = conc[:len(chain)]
    tab = '; '.join(f'{c}: {v:.5g} ppm' for c, v in zip(chain, conc))
    tot = conc[-1] / conc[0]
    if slot.d <= 3:
        i = rng.randint(1, len(chain) - 2)
        cf = conc[i + 1] / conc[i]
        return dict(stem=f'Concentrations of {chem} measured along a food chain: {tab}. (a) Calculate how many times more concentrated {chem} is in {chain[i + 1]} than in {chain[i]}. (b) Outline why the concentration increases along the chain.',
                    answer=f'(a) {conc[i + 1]:.5g} / {conc[i]:.5g} = {cf:.0f} times (b) {chem} is persistent and fat-soluble, so it is stored in fatty tissue (bioaccumulation) and not excreted; each predator eats many prey, so the amount accumulates at each trophic level (biomagnification).',
                    markingKey=f'(a) A1 ×{cf:.0f}. (b) R1 persistent/fat-soluble, not broken down or excreted; R1 consumers eat large quantities of prey so concentration increases.', marks=mk(slot, 3))
    return dict(stem=f'Concentrations of {chem} measured along a food chain: {tab}. (a) Calculate the overall biomagnification factor from {chain[0]} to {chain[-1]}. (b) Distinguish between bioaccumulation and biomagnification using these data. (c) Explain why top predators such as {chain[-1]} are most at risk and evaluate one measure to reduce the problem.',
                answer=f'(a) {conc[-1]:.5g} / {conc[0]:.5g} ≈ {tot:,.0f} times (b) bioaccumulation: build-up of {chem} within one organism over its life (e.g. in {chain[1]} relative to {chain[0]}); biomagnification: increase in concentration from one trophic level to the next. (c) top predators feed at the highest level and live longest, so they receive the highest doses (e.g. eggshell thinning or immune and reproductive effects); a ban (e.g. Stockholm Convention 2001) is effective but persistent residues remain for decades.',
                markingKey=f'(a) A1 ≈ {tot:,.0f}. (b) R1 within organism over time, R1 between trophic levels. (c) R1 highest level/long life, R1 named effect, R1 evaluation of a measure.', marks=mk(slot, 6))


@gen('carbon_budget')
def g_carbon(rng, slot):
    fos = round(rng.uniform(8.5, 10.2), 1)
    luc = round(rng.uniform(0.8, 1.6), 1)
    ocean = round(rng.uniform(2.4, 3.0), 1)
    land = round(rng.uniform(1.6, 3.4), 1)
    atm = round(fos + luc - ocean - land, 1)
    ppm = atm / 2.12
    yr = rng.choice([2015, 2018, 2020, 2022, 2023])
    head = pick(rng, [f'Illustrative global carbon budget for {yr} (GtC per year): fossil fuel and cement emissions {fos}; land-use change {luc}; ocean sink {ocean}; land sink {land}.',
                      f'A simplified version of the Global Carbon Project budget gives these annual flows (GtC yr⁻¹): emissions from fossil fuels {fos}, emissions from deforestation and land-use change {luc}, uptake by the oceans {ocean}, uptake by terrestrial vegetation {land}.'])
    if slot.d <= 2:
        return dict(stem=f'{head} Calculate the annual increase in carbon stored in the atmosphere.',
                    answer=f'{fos} + {luc} − {ocean} − {land} = {atm} GtC per year',
                    markingKey=f'M1 sources − sinks; A1 {atm} GtC yr⁻¹.', marks=mk(slot, 2))
    share = atm / (fos + luc) * 100
    if slot.d == 3:
        return dict(stem=f'{head} (a) Calculate the increase in atmospheric carbon. (b) Calculate the percentage of total emissions that remained in the atmosphere (the airborne fraction). (c) Given that 2.12 GtC corresponds to 1 ppm CO₂, calculate the rise in CO₂ concentration.',
                    answer=f'(a) {atm} GtC (b) {share:.0f}% (c) {atm} / 2.12 = {ppm:.2f} ppm',
                    markingKey=f'(a) A1 {atm}. (b) A1 {share:.0f}%. (c) A1 {ppm:.2f} ppm.', marks=mk(slot, 4))
    stock = rng.choice([860, 875, 880, 900])
    flux = rng.choice([180, 200, 210])
    return dict(stem=f'{head} The atmosphere stores about {stock} GtC and exchanges about {flux} GtC per year with the oceans and biosphere. (a) Calculate the net annual change in atmospheric carbon and the rise in CO₂ (2.12 GtC = 1 ppm). (b) Calculate the mean residence time of carbon in the atmosphere. (c) Explain why the ocean sink may become less effective as the climate warms, and evaluate the implication for carbon budgets.',
                answer=f'(a) {atm} GtC yr⁻¹; {ppm:.2f} ppm (b) {stock} / {flux} ≈ {stock / flux:.1f} years (c) CO₂ is less soluble in warmer water, stratification reduces mixing to depth and acidification reduces carbonate buffering, so a larger airborne fraction remains; remaining carbon budgets for 1.5 °C would be smaller than models assuming constant sinks.',
                markingKey=f'(a) A1 {atm}, A1 {ppm:.2f}. (b) M1 storage ÷ flow, A1 {stock / flux:.1f} years. (c) R1 solubility/stratification, R1 implication (positive feedback; smaller budget).', marks=mk(slot, 6))


@gen('ph')
def g_ph(rng, slot):
    p0 = rng.choice([8.25, 8.2, 8.18, 8.15, 8.11])
    drop = rng.choice([0.05, 0.1, 0.15, 0.2, 0.3, 0.4])
    p1 = round(p0 - drop, 2)
    f_ = 10 ** (p0 - p1)
    pct = (f_ - 1) * 100
    head = pick(rng, [f'Surface-ocean pH fell from {p0} to {p1}.',
                      f'At a monitoring station (e.g. the Hawaii Ocean Time-series), seawater pH changed from {p0} to {p1}.',
                      f'A model projects that ocean pH will fall from {p0} to {p1} by 2100 under a high-emissions scenario.'])
    if slot.d <= 2:
        return dict(stem=f'{head} Calculate the factor by which hydrogen-ion concentration increased.',
                    answer=f'10^({p0} − {p1}) = 10^{p0 - p1:.2f} ≈ {f_:.2f} times ({pct:.0f}% increase)',
                    markingKey=f'M1 pH is −log[H⁺], so factor = 10^ΔpH; A1 {f_:.2f}.', marks=mk(slot, 2))
    return dict(stem=f'{head} (a) Calculate the percentage increase in hydrogen-ion concentration. (b) Explain how the absorption of CO₂ lowers ocean pH. (c) Explain one consequence for marine calcifying organisms such as pteropods or reef-building corals.',
                answer=f'(a) 10^{p0 - p1:.2f} = {f_:.2f}, so ≈ {pct:.0f}% increase (b) CO₂ + H₂O → H₂CO₃ → H⁺ + HCO₃⁻; the extra H⁺ lowers pH and combines with carbonate ions (CO₃²⁻ + H⁺ → HCO₃⁻). (c) lower carbonate-ion concentration reduces calcification (aragonite saturation falls), so shells and skeletons grow more slowly or dissolve, weakening reefs and the base of food webs.',
                markingKey=f'(a) M1 10^ΔpH, A1 {pct:.0f}%. (b) R1 carbonic acid forms, R1 H⁺ released / carbonate removed. (c) R1 reduced carbonate availability, R1 consequence.', marks=mk(slot, 5 if slot.d >= 4 else 4))


@gen('footprint')
def g_footprint(rng, slot):
    who = rng.choice(['Country A', 'Country B', 'an island state', 'a landlocked country', 'a city region'])
    ef = round(rng.uniform(1.0, 9.5), 1)
    bc = round(rng.uniform(0.4, 9.0), 1)
    pop = rng.choice([5, 12, 30, 48, 85, 140])
    world_bc = 1.6
    earths = ef / world_bc
    if slot.d <= 2:
        bal = bc - ef
        return dict(stem=pick(rng, [f'{who[0].upper() + who[1:]} has an ecological footprint of {ef} gha per person and a biocapacity of {bc} gha per person. Calculate its ecological reserve or deficit per person and state which it is.',
                                    f'Data for {who}: footprint {ef} global hectares (gha) per capita; biocapacity {bc} gha per capita. Determine whether it runs an ecological deficit and by how much.']),
                    answer=f'{bc} − {ef} = {bal:+.1f} gha per person: ' + ('ecological reserve' if bal >= 0 else 'ecological deficit'),
                    markingKey=f'M1 biocapacity − footprint; A1 {bal:+.1f} gha per person with correct label.', marks=mk(slot, 2))
    tot = (ef - bc) * pop
    s = 'deficit' if tot > 0 else 'reserve'
    return dict(stem=f'{who[0].upper() + who[1:]} has {pop} million people, an ecological footprint of {ef} gha per person and a biocapacity of {bc} gha per person. Global biocapacity is about {world_bc} gha per person. (a) Calculate the national ecological {s} in gha. (b) Calculate how many Earths would be needed if everyone lived like the average resident. (c) Explain two ways a country can sustain a footprint larger than its biocapacity.' + (' (d) Evaluate the ecological footprint as a measure of sustainability.' if slot.d >= 4 else ''),
                answer=f'(a) |{ef} − {bc}| × {pop} million = {abs(tot):.1f} million gha ({s}) (b) {ef} / {world_bc} ≈ {earths:.1f} Earths (c) importing food, timber and other resources (using other countries\' biocapacity); emitting CO₂ absorbed by the global commons (oceans, forests elsewhere); running down its own natural capital (overfishing, deforestation).' + (' (d) strengths: single, communicable figure; links consumption to land area; limitations: excludes some impacts (water, toxic pollution, biodiversity), assumes current technology and yields, carbon footprint dominates.' if slot.d >= 4 else ''),
                markingKey=f'(a) A1 {abs(tot):.1f} million gha. (b) A1 {earths:.1f}. (c) R1 R1 trade / global commons / depletion.' + (' (d) R1 strength, R1 limitation.' if slot.d >= 4 else ''),
                marks=mk(slot, 6 if slot.d >= 4 else 4))


NAT_INCOME = [('a managed beech forest in the Black Forest', 'm³ of timber', 'hectare'),
              ('a stock of North Sea plaice', 'tonnes of fish', 'stock'),
              ('a mangrove plantation in the Sundarbans', 'tonnes of biomass', 'hectare'),
              ('a community woodland in Nepal', 'tonnes of fuelwood', 'hectare'),
              ('a seaweed farm in Zanzibar', 'tonnes of seaweed', 'farm')]


@gen('natural_income')
def g_natural_income(rng, slot):
    what, u, per = pick(rng, NAT_INCOME)
    t = rng.choice([1, 2, 4, 5, 10])
    s0 = rng.randint(100, 900)
    s1 = s0 + rng.randint(5, 40) * t
    sy = (s1 - s0) / t
    if slot.d <= 2:
        return dict(stem=f'The natural capital of {what} increased from {s0} to {s1} {u} per {per} over {t} year(s) with no harvesting. Calculate the sustainable yield per year.',
                    answer=f'SY = (total biomass/energy at t + 1 − at t) / time = ({s1} − {s0}) / {t} = {sy:.1f} {u} per {per} per year',
                    markingKey=f'M1 increase ÷ time; A1 {sy:.1f}.', marks=mk(slot, 2))
    h = round(sy * rng.choice([0.6, 0.8, 1.2, 1.5, 2.0]), 1)
    years = 10
    end = s0 + (sy - h) * years
    verdict = 'sustainable (natural capital maintained or rising)' if h <= sy else 'unsustainable (natural capital declining)'
    return dict(stem=f'The natural capital of {what} grows from {s0} to {s1} {u} per {per} in {t} year(s) without harvesting. A manager proposes harvesting {h} {u} per {per} each year. (a) Calculate the sustainable yield. (b) Assuming constant growth, calculate the stock after {years} years of the proposed harvest and state whether it is sustainable. (c) Explain why sustainable yield is hard to set in practice.',
                answer=f'(a) {sy:.1f} {u} per {per} per year (b) {s0} + ({sy:.1f} − {h}) × {years} = {end:.0f}; {verdict} (c) growth rates vary with climate, disease and stock size (density dependence); data are uncertain; economic pressure favours over-setting quotas; time lags in monitoring.',
                markingKey=f'(a) A1 {sy:.1f}. (b) M1 (SY − harvest) × years, A1 {end:.0f} and verdict. (c) R1 R1 valid reasons.', marks=mk(slot, 5))


SYSTEM_STORE = [('a reservoir behind a hydroelectric dam', 'million m³', 'river inflow', 'outflow through turbines and evaporation'),
                ('a lake in the Swiss Plateau', 'km³', 'inflow from rivers', 'outflow plus evaporation'),
                ('an unconfined aquifer under an agricultural plain', 'million m³', 'recharge by infiltration', 'pumped abstraction and springs'),
                ('a valley glacier in the Alps', 'million m³ water equivalent', 'snowfall accumulation', 'melting and sublimation'),
                ('soil organic carbon in a hectare of farmland', 't C', 'leaf litter and root inputs', 'decomposition (respiration) and erosion')]


@gen('storage')
def g_storage(rng, slot):
    what, u, i_, o_ = pick(rng, SYSTEM_STORE)
    S0 = rng.randint(50, 900)
    inn = rng.randint(5, 80)
    out = inn + rng.choice([-12, -8, -5, -3, 3, 5, 8, 12])
    if out <= 0:
        return None
    dS = inn - out
    if slot.d <= 2:
        return dict(stem=pick(rng, [f'{what[0].upper() + what[1:]} stores {S0} {u}. Each year it receives {inn} {u} from {i_} and loses {out} {u} through {o_}. Calculate the change in storage after one year and state whether the system is in steady state.',
                                    f'A systems diagram of {what} shows a storage of {S0} {u}, an input ({i_}) of {inn} {u} per year and an output ({o_}) of {out} {u} per year. Calculate the storage after one year.']),
                    answer=f'ΔS = inputs − outputs = {inn} − {out} = {dS:+d} {u}; storage = {S0 + dS} {u}; not in steady state (inputs ≠ outputs)',
                    markingKey=f'M1 inputs − outputs; A1 {dS:+d} (storage {S0 + dS}).', marks=mk(slot, 2))
    rt = S0 / out
    yrs = S0 / -dS if dS < 0 else None
    return dict(stem=f'{what[0].upper() + what[1:]} stores {S0} {u}, with an input ({i_}) of {inn} {u} per year and an output ({o_}) of {out} {u} per year. (a) Calculate the mean residence time. (b) ' + ('Calculate how long the storage would last if these flows continued.' if yrs else 'Calculate the storage after 10 years.') + ' (c) Explain whether the system is open, closed or isolated and whether it is in steady-state equilibrium.',
                answer=f'(a) storage ÷ output = {S0} / {out} ≈ {rt:.1f} years (b) ' + (f'{S0} / {-dS} ≈ {yrs:.0f} years' if yrs else f'{S0} + {dS} × 10 = {S0 + 10 * dS} {u}') + ' (c) open - it exchanges both matter and energy with its surroundings; not in steady state because inputs ≠ outputs, so storage is ' + ('falling' if dS < 0 else 'rising') + '.',
                markingKey=f'(a) M1 storage/flow, A1 {rt:.1f}. (b) A1. (c) R1 open system with reason, R1 not steady state.', marks=mk(slot, 5))


EFF = [('a coal-fired power station', 'chemical energy in coal', 'electricity', 'heat in cooling water and flue gases'),
       ('a field of sugar cane in Brazil', 'solar radiation reaching the crop', 'chemical energy stored in biomass (GPP)', 'reflection, transmission and heat'),
       ('an incandescent light bulb', 'electrical energy', 'light', 'heat'),
       ('a car with a petrol engine', 'chemical energy in petrol', 'kinetic energy', 'heat from the engine and exhaust'),
       ('a sheep grazing upland pasture', 'energy in grass eaten', 'energy stored in new tissue', 'heat from respiration and energy in faeces and urine')]


@gen('thermo')
def g_thermo(rng, slot):
    sys_, i_, o_, l_ = pick(rng, EFF)
    inp = rng.choice([500, 1000, 2000, 2500, 4000, 10000])
    eff = rng.choice({'power': [33, 35, 38, 40], 'sugar': [1, 2], 'bulb': [2, 4, 5], 'car': [20, 25, 30], 'sheep': [2, 4, 5]}[
        next(k for k in ('power', 'sugar', 'bulb', 'car', 'sheep') if k in sys_)])
    useful = inp * eff / 100
    loss = inp - useful
    if slot.d <= 2:
        return dict(stem=f'In {sys_}, {comma(inp)} kJ of {i_} produces {fmt_n(useful)} kJ of {o_}. Calculate the efficiency of the energy transformation.',
                    answer=f'useful output / input × 100 = {fmt_n(useful)} / {comma(inp)} × 100 = {eff}%',
                    markingKey=f'M1 useful energy out ÷ energy in × 100; A1 {eff}%.', marks=mk(slot, 2))
    return dict(stem=f'In {sys_}, {comma(inp)} kJ of {i_} produces {fmt_n(useful)} kJ of {o_}. (a) Calculate the efficiency and the energy dissipated. (b) Use the first and second laws of thermodynamics to explain these figures.',
                answer=f'(a) {eff}%; {fmt_n(loss)} kJ lost as {l_} (b) first law: energy is conserved, so input = useful output + losses ({comma(inp)} = {fmt_n(useful)} + {fmt_n(loss)}); second law: every transformation is inefficient and increases entropy, so some energy is always degraded to low-grade heat that cannot do further work.',
                markingKey=f'(a) A1 {eff}%, A1 {fmt_n(loss)} kJ. (b) R1 first law (conservation), R1 second law (degradation to heat / entropy).', marks=mk(slot, 4))


def fmt_n(x):
    return comma(x) if abs(x - round(x)) < 1e-9 else f'{x:,.1f}'


CLIMATES = [  # (place, monthly mean T °C, monthly precipitation mm, biome)
    ('Manaus, Brazil', [26.1, 26.0, 26.1, 26.2, 26.5, 26.6, 26.9, 27.5, 27.9, 27.7, 27.3, 26.7], [264, 278, 300, 287, 193, 99, 61, 41, 62, 112, 165, 220], 'tropical rainforest'),
    ('Singapore', [26.5, 27.1, 27.5, 28.0, 28.3, 28.3, 27.9, 27.9, 27.6, 27.6, 27.0, 26.4], [243, 159, 185, 179, 172, 162, 158, 175, 170, 194, 256, 288], 'tropical rainforest'),
    ('Riyadh, Saudi Arabia', [14.6, 17.0, 21.2, 26.6, 32.6, 35.2, 36.6, 36.3, 33.2, 27.9, 20.8, 16.1], [12, 8, 22, 25, 9, 0, 0, 0, 0, 1, 7, 13], 'hot desert'),
    ('Alice Springs, Australia', [29.3, 28.1, 25.4, 20.8, 15.9, 12.5, 12.0, 14.6, 19.0, 23.0, 26.0, 28.0], [40, 44, 33, 17, 18, 13, 15, 9, 8, 21, 29, 37], 'hot desert'),
    ('Utqiaġvik (Barrow), Alaska', [-25.6, -27.3, -25.8, -17.4, -5.8, 1.9, 4.9, 3.6, -0.6, -8.9, -17.6, -23.6], [4, 4, 3, 4, 4, 8, 25, 25, 17, 11, 6, 4], 'tundra'),
    ('Fairbanks, Alaska', [-21.9, -18.8, -10.5, 0.6, 9.8, 15.9, 17.0, 14.1, 7.8, -3.6, -15.3, -19.6], [12, 10, 8, 7, 16, 34, 55, 47, 27, 20, 16, 14], 'boreal forest (taiga)'),
    ('London, UK', [5.2, 5.3, 7.6, 9.9, 13.3, 16.5, 18.7, 18.5, 15.7, 12.0, 8.0, 5.5], [55, 41, 42, 44, 49, 45, 45, 50, 49, 69, 59, 55], 'temperate deciduous forest'),
    ('Nairobi, Kenya', [19.4, 20.2, 20.6, 20.1, 18.9, 17.4, 16.6, 17.1, 18.5, 19.6, 19.0, 18.8], [45, 54, 92, 193, 125, 31, 15, 22, 24, 52, 128, 76], 'tropical grassland (savanna)'),
    ('Winnipeg, Canada', [-16.4, -13.2, -5.8, 4.4, 11.6, 17.0, 19.7, 18.8, 12.7, 5.0, -4.9, -13.2], [18, 12, 25, 31, 60, 90, 79, 76, 49, 36, 26, 19], 'temperate grassland (prairie)'),
]


CLIM_EXPL = {
    'tropical rainforest': 'near the equator the ITCZ / rising limb of the Hadley cell gives intense insolation, convection and convectional rain all year; small temperature range because the sun is always high',
    'hot desert': 'at about 20-30° latitude descending air in the Hadley cell forms the subtropical high-pressure belt; sinking air warms and dries, so clouds and rain are rare; clear skies give hot days and a large temperature range',
    'tundra': 'at high latitude under the polar cell, descending cold, dry air gives polar high pressure and low precipitation; low sun angle and long winters keep temperatures very low',
    'boreal forest (taiga)': 'between the Ferrel and polar cells at about 50-65° N; continental interior far from the sea gives a very large annual range; low precipitation mainly from summer depressions',
    'temperate deciduous forest': 'in the Ferrel cell at mid-latitudes, westerly winds and depressions along the polar front bring rain all year; a maritime location moderates temperatures',
    'tropical grassland (savanna)': 'the seasonal migration of the ITCZ brings a wet season when it is overhead and a dry season when subtropical high pressure dominates; altitude at Nairobi lowers temperatures',
    'temperate grassland (prairie)': 'mid-latitude (Ferrel cell) continental interior far from oceans, with a rain shadow; summer convectional rain and depressions, a very large annual temperature range',
}


@gen('climograph')
def g_climograph(rng, slot):
    place, T_, P_, biome = pick(rng, CLIMATES)
    tot = sum(P_)
    rngT = max(T_) - min(T_)
    meanT = sum(T_) / 12
    mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    tab = '; '.join(f'{m} {t}°C/{p} mm' for m, t, p in zip(mon, T_, P_))
    loc = 'Station X' if slot.d >= 3 else place
    if slot.d <= 2:
        return dict(stem=f'Climate data for {place} (mean monthly temperature / precipitation): {tab}. Calculate (a) the annual precipitation total and (b) the annual temperature range.',
                    answer=f'(a) {tot} mm (b) {max(T_)} − ({min(T_)}) = {rngT:.1f} °C',
                    markingKey=f'(a) A1 {tot} mm. (b) A1 {rngT:.1f} °C.', marks=mk(slot, 2))
    return dict(stem=f'Climate data for {loc} (mean monthly temperature / precipitation): {tab}. (a) Calculate the annual precipitation, the mean annual temperature and the annual temperature range. (b) Identify the most likely biome and justify your answer using the data. (c) Explain how the tricellular model accounts for this climate.',
                answer=f'(a) {tot} mm; {meanT:.1f} °C; {rngT:.1f} °C (b) {biome} ({place}) - justified by the totals, seasonality and temperature range calculated (c) {CLIM_EXPL[biome]}.',
                markingKey=f'(a) A1 {tot}, A1 {meanT:.1f}, A1 {rngT:.1f}. (b) A1 {biome}, R1 justification from data. (c) R1 link to atmospheric circulation cell / pressure belt.', marks=mk(slot, 6))


@gen('lapse')
def g_lapse(rng, slot):
    mt = pick(rng, [('Mount Kilimanjaro', 5895, 'Moshi', 890), ('Mont Blanc', 4806, 'Chamonix', 1035),
                    ('Mauna Kea', 4207, 'Hilo', 10), ('Aconcagua', 6961, 'Mendoza', 750), ('Mount Kinabalu', 4095, 'Kota Kinabalu', 10),
                    ('Denali', 6190, 'Talkeetna', 105), ('Ben Nevis', 1345, 'Fort William', 10)])
    peak, h, town, h0 = mt
    T0 = rng.choice([12, 16, 18, 21, 24, 27, 30])
    rate = 6.5
    Ts = T0 - rate * (h - h0) / 1000
    if slot.d <= 2:
        return dict(stem=f'The mean temperature at {town} ({h0} m) is {T0} °C. Using an environmental lapse rate of 6.5 °C per 1,000 m, calculate the expected mean temperature at the summit of {peak} ({comma(h)} m).',
                    answer=f'{T0} − 6.5 × ({h} − {h0})/1,000 = {Ts:.1f} °C',
                    markingKey=f'M1 height difference × 6.5/1,000; A1 {Ts:.1f} °C.', marks=mk(slot, 2))
    tl = rng.choice([10, 8, 6])
    zh = h0 + (T0 - tl) / rate * 1000
    return dict(stem=f'On {peak}, the mean temperature at {town} ({h0} m) is {T0} °C and the environmental lapse rate is 6.5 °C per 1,000 m. (a) Calculate the summit temperature ({comma(h)} m). (b) If trees cannot grow where the mean temperature of the warmest month is below about {tl} °C, estimate the altitude of the tree line (assume {T0} °C is the warmest-month mean at {town}). (c) Explain how altitudinal zonation on mountains resembles latitudinal changes in biomes.',
                answer=f'(a) {Ts:.1f} °C (b) {h0} + ({T0} − {tl}) / 6.5 × 1,000 ≈ {zh:,.0f} m (c) temperature falls with altitude as with latitude, so mountains show zones (e.g. forest → montane shrub → alpine grassland/tundra → ice) similar to the sequence from the equator to the poles; precipitation, aspect and soils modify the pattern.',
                markingKey=f'(a) A1 {Ts:.1f}. (b) M1 (T − tl)/6.5 × 1,000, A1 ≈ {zh:,.0f} m. (c) R1 temperature decrease, R1 analogous zones / named example.', marks=mk(slot, 5))


@gen('pr_ratio')
def g_pr(rng, slot):
    stages = [('a bare lava field colonised by lichens', 'pioneer'), ('an abandoned field 5 years after ploughing', 'early'),
              ('a 40-year-old birch-pine woodland', 'mid-successional'), ('an old-growth oak woodland', 'climax')]
    st, stage = pick(rng, stages)
    gpp = rng.randint(10, 300) * 10
    ratio = {'pioneer': rng.choice([1.6, 1.8, 2.2]), 'early': rng.choice([1.4, 1.5]), 'mid-successional': rng.choice([1.15, 1.2, 1.25]), 'climax': rng.choice([1.0, 1.02, 0.98])}[stage]
    resp = round(gpp / ratio)
    pr = gpp / resp
    npp = gpp - resp
    return dict(stem=pick(rng, [f'In {st}, community GPP = {gpp} g m⁻² yr⁻¹ and total community respiration R = {resp} g m⁻² yr⁻¹. (a) Calculate the P:R ratio and the net productivity of the community. (b) Use your answer to suggest the stage of succession and explain how P:R changes during succession.',
                                f'Productivity data for {st}: gross productivity {gpp}, respiration {resp} (both g m⁻² yr⁻¹). Calculate P:R and net community productivity, then explain what these values suggest about biomass accumulation at this stage of succession.']),
                answer=f'(a) P:R = {gpp}/{resp} = {pr:.2f}; net productivity = {npp} g m⁻² yr⁻¹ (b) ' + ('P:R > 1, biomass is accumulating, typical of early/mid succession' if pr > 1.05 else 'P:R ≈ 1, little net accumulation, typical of a climax community') + '; P:R starts high in pioneer stages, then falls towards 1 as biomass and respiring tissue accumulate.',
                markingKey=f'(a) A1 {pr:.2f}, A1 {npp}. (b) R1 interpretation of ratio, R1 trend during succession.', marks=mk(slot, 4))


@gen('transect')
def g_transect(rng, slot):
    frames = [('a sand-dune transect at Studland, Dorset', ['embryo dune', 'fore dune', 'yellow dune', 'grey dune', 'dune slack', 'heath'], 'marram grass', 'wind speed and sand burial, soil moisture, soil organic matter and pH (decreasing with distance inland), salt spray'),
              ('a rocky-shore transect from low to high tide', ['lower shore', 'lower-middle shore', 'middle shore', 'upper-middle shore', 'upper shore', 'splash zone'], 'channel wrack', 'exposure / desiccation time between tides, temperature range, salinity, wave action'),
              ('a transect from a pond edge into grassland', ['open water margin', 'reed swamp', 'sedge zone', 'wet grassland', 'drier grassland', 'hedge'], 'common reed', 'soil moisture / waterlogging, depth of water table, soil oxygen, nutrient levels'),
              ('an altitudinal transect on a mountain slope in Nepal', ['subtropical forest', 'temperate forest', 'subalpine forest', 'rhododendron scrub', 'alpine meadow', 'scree'], 'blue pine', 'temperature (falling with altitude), length of growing season, soil depth, exposure to wind, frost')]
    where, zones, sp_, abio = pick(rng, frames)
    k = 5 if slot.d <= 3 else 6
    zones = zones[:k]
    peak = rng.randrange(k)
    covers = []
    for i in range(k):
        covers.append(max(0, 70 - 22 * abs(i - peak) + rng.randint(-6, 6)))
    q = [[max(0, c + rng.randint(-8, 8)) for _ in range(3)] for c in covers]
    means = [sum(x) / 3 for x in q]
    tab = '; '.join(f'{z}: {a}%, {b}%, {c}%' for z, (a, b, c) in zip(zones, q))
    best = zones[max(range(k), key=lambda i: means[i])]
    if slot.d <= 2:
        i = rng.randrange(k)
        return dict(stem=f'Percentage cover of {sp_} in three quadrats at each station along {where}: {tab}. Calculate the mean percentage cover at the {zones[i]}.',
                    answer=f'({" + ".join(map(str, q[i]))}) / 3 = {means[i]:.1f}%', markingKey=f'M1 sum ÷ 3; A1 {means[i]:.1f}%.', marks=mk(slot, 2))
    return dict(stem=f'Percentage cover of {sp_} in three quadrats at each station along {where}: {tab}. (a) Calculate the mean cover at each station and identify where the species is most abundant. (b) Name a suitable way to present these data and explain why a transect is used here. (c) Suggest two abiotic factors that could explain the distribution.',
                answer='(a) ' + '; '.join(f'{z} {m:.1f}%' for z, m in zip(zones, means)) + f'; most abundant at the {best} (b) a kite diagram; a transect samples systematically along an environmental gradient to show zonation (c) e.g. {abio}.',
                markingKey=f'(a) A1 means correct, A1 {best}. (b) A1 kite diagram, R1 gradient/zonation. (c) R1 R1 relevant abiotic factors.', marks=mk(slot, 6))


@gen('extinction')
def g_extinction(rng, slot):
    grp = pick(rng, [('birds', 11000, 'birds'), ('mammals', 6500, 'mammals'), ('amphibians', 8700, 'amphibians'),
                     ('freshwater fish', 18000, 'freshwater fish'), ('reptiles', 12000, 'reptiles')])
    g, n, _ = grp
    ext = rng.randint(8, 190)
    yrs = rng.choice([100, 120, 200, 500])
    emsy = ext / (n * yrs) * 1e6
    bg = rng.choice([0.1, 1])
    fac = emsy / bg
    return dict(stem=pick(rng, [f'About {ext} species of {g} (out of roughly {comma(n)} described species) are documented to have gone extinct in the last {yrs} years. (a) Calculate the extinction rate in extinctions per million species-years (E/MSY). (b) The background rate is often estimated at about {bg} E/MSY. Calculate how many times faster than background the observed rate is. (c) Explain why this is likely to be an underestimate.',
                                f'Records suggest that {ext} of about {comma(n)} {g} species have become extinct over {yrs} years. Express this as E/MSY, compare it with a background rate of {bg} E/MSY, and explain whether this supports the claim that a sixth mass extinction is under way.']),
                answer=f'(a) {ext} / ({comma(n)} × {yrs}) × 10⁶ = {emsy:.1f} E/MSY (b) ≈ {fac:.0f} times background (c) many species go extinct before they are described; extinctions are only confirmed after long searches; "living dead" (committed) extinctions from habitat loss have not yet happened; some groups are poorly studied.',
                markingKey=f'(a) M1 extinctions ÷ (species × years) × 10⁶, A1 {emsy:.1f}. (b) A1 ×{fac:.0f}. (c) R1 R1 valid reasons / link to mass extinction (≥ 75% of species lost in a geologically short time).', marks=mk(slot, 5))


IUCN_SP = [('Sunda pangolin', 'years (3 generations ≈ 21 years)'), ('African forest elephant', 'years (3 generations ≈ 93 years)'),
           ('hawksbill turtle', 'years (3 generations ≈ 100 years)'), ('vaquita porpoise', 'years'), ('a species of Andean frog', 'years'),
           ('Bornean orangutan', 'years (3 generations ≈ 75 years)'), ('European eel', 'years'), ('a species of Hawaiian honeycreeper', 'years')]


@gen('iucn')
def g_iucn(rng, slot):
    sp_, _ = pick(rng, IUCN_SP)
    n0 = rng.randint(20, 900) * 100
    red = rng.choice([22, 35, 45, 55, 62, 78, 84, 92])
    n1 = round(n0 * (1 - red / 100))
    pct = (n0 - n1) / n0 * 100
    cat = 'Critically Endangered' if pct >= 80 else 'Endangered' if pct >= 50 else 'Vulnerable' if pct >= 30 else 'not threatened under criterion A (possibly Near Threatened)'
    rule = 'Criterion A2 thresholds (reduction over 10 years or 3 generations, causes may not have ceased): ≥ 80% Critically Endangered; ≥ 50% Endangered; ≥ 30% Vulnerable.'
    if slot.d <= 2:
        return dict(stem=f'A population of the {sp_} fell from {comma(n0)} to {comma(n1)} mature individuals over three generations. Calculate the percentage reduction.',
                    answer=f'({comma(n0)} − {comma(n1)}) / {comma(n0)} × 100 = {pct:.1f}%', markingKey=f'M1 reduction ÷ original × 100; A1 {pct:.1f}%.', marks=mk(slot, 2))
    return dict(stem=f'Surveys show the {sp_} declined from {comma(n0)} to {comma(n1)} mature individuals over three generations, mainly due to poaching and habitat loss. {rule} (a) Calculate the percentage reduction and assign the Red List category. (b) Outline two other factors the IUCN considers when assessing conservation status.' + (' (c) Evaluate the usefulness of Red List categories for conservation decision-making.' if slot.d >= 4 else ''),
                answer=f'(a) {pct:.1f}% → {cat} (b) e.g. geographic range (extent of occurrence / area of occupancy), number of mature individuals, degree of fragmentation, probability of extinction in the wild (quantitative analysis), number of sub-populations.' + (' (c) strengths: objective, global, repeatable criteria; raise funding and public attention; inform CITES listings. Limitations: data-deficient species, bias towards vertebrates, categories do not set priorities or solutions alone, reassessment is slow.' if slot.d >= 4 else ''),
                markingKey=f'(a) A1 {pct:.1f}%, A1 {cat}. (b) R1 R1 valid factors.' + (' (c) R1 strength, R1 limitation.' if slot.d >= 4 else ''), marks=mk(slot, 6 if slot.d >= 4 else 4))


@gen('reserve')
def g_reserve(rng, slot):
    L = rng.choice([4, 5, 6, 8, 10, 12, 20])
    e = rng.choice([0.5, 1, 1.5, 2])
    if L <= 2 * e + 0.5:
        return None
    area = L * L
    core = (L - 2 * e) ** 2
    pct = core / area * 100
    if slot.d <= 2:
        return dict(stem=f'A square forest reserve measures {L} km × {L} km. Edge effects (light, wind, invasive species, predators) penetrate {e} km into the forest. Calculate the core area unaffected by edge effects.',
                    answer=f'({L} − 2 × {e})² = {core:g} km² (of {area} km² total)', markingKey=f'M1 side reduced by 2e; A1 {core:g} km².', marks=mk(slot, 2))
    n = 4
    s = L / 2
    core_s = n * max(0, s - 2 * e) ** 2
    return dict(stem=f'A conservation agency can protect {area} km² either as one square reserve ({L} km × {L} km) or as four square reserves of {s:g} km × {s:g} km. Edge effects penetrate {e} km. (a) Calculate the total core area for each option. (b) With reference to the SLOSS debate, discuss which design is preferable and suggest one feature that would improve either design.',
                answer=f'(a) one large: ({L} − {2 * e:g})² = {core:g} km² ({pct:.0f}%); four small: 4 × ({s:g} − {2 * e:g})² = {core_s:g} km² (b) the single large reserve keeps more core habitat for interior species and wide-ranging animals and reduces edge effects; several small reserves spread risk (fire, disease), may include more habitat types and can be easier to acquire; corridors or buffer zones (e.g. UNESCO biosphere reserve model) improve either design.',
                markingKey=f'(a) A1 {core:g}, A1 {core_s:g}. (b) R1 large: edge/area ratio, R1 small: risk-spreading/heterogeneity, R1 corridor/buffer/shape.', marks=mk(slot, 6))


@gen('habitat_loss')
def g_habitat_loss(rng, slot):
    place, lo, hi = pick(rng, [('a lowland rainforest region of Sumatra', 150, 600), ('one state of the Brazilian Cerrado', 300, 1500),
                               ('a Philippine province with coastal mangroves', 2, 8), ('a peat swamp forest region in Sarawak', 40, 120),
                               ('the Paraguayan Gran Chaco', 800, 1600), ('a Mexican state with cloud forest', 5, 40)])
    a0 = rng.randint(lo, hi) * 100
    r = rng.choice([0.5, 1, 1.5, 2, 2.5, 3, 4])
    n = rng.choice([5, 10, 20])
    a1 = a0 * (1 - r / 100) ** n
    if slot.d <= 2:
        a_ = round(a0 * (1 - r * n / 100))
        return dict(stem=f'Satellite images show that {place} had {comma(a0)} km² of forest in 2000 and {comma(a_)} km² {n} years later. Calculate the mean annual rate of loss in km² per year and as a percentage of the 2000 area.',
                    answer=f'({comma(a0)} − {comma(a_)}) / {n} = {(a0 - a_) / n:,.0f} km² per year; {(a0 - a_) / n / a0 * 100:.1f}% of the 2000 area per year',
                    markingKey=f'M1 change ÷ years; A1 {(a0 - a_) / n:,.0f} km² yr⁻¹; A1 {(a0 - a_) / n / a0 * 100:.1f}%.', marks=mk(slot, 3))
    half = math.log(0.5) / math.log(1 - r / 100)
    return dict(stem=f'In {place} there were {comma(a0)} km² of forest, and {r}% of the remaining forest is being lost each year. (a) Calculate the forest area remaining after {n} years. (b) Calculate how long it would take to lose half the forest at this rate. (c) Explain two reasons why biodiversity loss may be greater than the percentage of area lost suggests.',
                answer=f'(a) {comma(a0)} × (1 − {r / 100})^{n} ≈ {a1:,.0f} km² (b) ln 0.5 / ln(1 − {r / 100}) ≈ {half:.0f} years (c) fragmentation increases edge effects and isolates populations (small populations, inbreeding); loss is concentrated in lowland, species-rich areas; species–area relationship and extinction debt; roads open remaining forest to hunting and fire.',
                markingKey=f'(a) M1 compound decline, A1 {a1:,.0f}. (b) A1 ≈ {half:.0f} years (accept rule of 70: {70 / r:.0f}). (c) R1 R1 valid reasons.', marks=mk(slot, 5))


BASINS = [('the River Severn catchment above Bewdley', 4325), ('a small catchment in the Scottish Highlands', 85),
          ('the Rhine basin above Basel', 36000), ('an experimental forested catchment in Plynlimon, Wales', 10),
          ('a sub-catchment of the Mekong in Laos', 2400), ('a catchment in the Western Ghats, India', 650)]


@gen('water_balance')
def g_water_balance(rng, slot):
    b, area = pick(rng, BASINS)
    P = rng.randint(60, 300) * 10
    E = round(P * rng.uniform(0.2, 0.6) / 10) * 10
    dS = rng.choice([-60, -40, -20, 0, 20, 40])
    Q = P - E - dS
    if slot.d <= 2:
        return dict(stem=f'In one year, {b} received {P} mm of precipitation; evapotranspiration was {E} mm and storage (soil and groundwater) changed by {dS:+d} mm. Using P = Q + E ± ΔS, calculate the runoff (Q) in mm.',
                    answer=f'Q = P − E − ΔS = {P} − {E} − ({dS:+d}) = {Q} mm', markingKey=f'M1 rearranging the water-balance equation; A1 {Q} mm.', marks=mk(slot, 2))
    vol = Q / 1000 * area * 1e6 / 1e6  # million m³
    return dict(stem=f'Water-balance data for {b} (area {comma(area)} km²): precipitation {P} mm; evapotranspiration {E} mm; change in storage {dS:+d} mm. (a) Calculate annual runoff in mm. (b) Convert this to a volume in million m³. (c) Predict and explain how deforestation of the catchment would change E, Q and flood risk.',
                answer=f'(a) {Q} mm (b) {Q} mm = {Q / 1000} m over {comma(area)} × 10⁶ m² = {vol:,.1f} million m³ (c) less interception and transpiration → E falls; infiltration falls as soils compact → overland flow and Q rise; shorter lag time and higher peak discharge increase flood risk.',
                markingKey=f'(a) A1 {Q}. (b) M1 depth × area, A1 {vol:,.1f}. (c) R1 E falls, R1 Q/overland flow rises, R1 flood risk with reason.', marks=mk(slot, 6))


WATER_C = [('Israel', 1.8, 9.8), ('Egypt', 57.5, 111), ('India', 1911, 1430), ('China', 2840, 1410),
           ('Jordan', 0.94, 11.3), ('Norway', 393, 5.5), ('Brazil', 8650, 216), ('the United Kingdom', 147, 67.7),
           ('Pakistan', 247, 240), ('South Africa', 51.4, 60.4), ('Ethiopia', 122, 126), ('Canada', 2900, 39.6)]


@gen('water_stress')
def g_water_stress(rng, slot):
    c, vol, pop = pick(rng, WATER_C)
    if slot.d >= 3 or vol == 0:
        c = rng.choice(['Country P', 'Country Q', 'a river basin state', 'an arid island nation'])
        vol = round(rng.uniform(0.5, 300), 1)
        pop = round(rng.uniform(2, 180), 1)
    pc = vol * 1e9 / (pop * 1e6)
    cat = ('absolute scarcity (< 500 m³)' if pc < 500 else 'water scarcity (500-1,000 m³)' if pc < 1000
           else 'water stress (1,000-1,700 m³)' if pc < 1700 else 'no stress (> 1,700 m³)')
    rule = 'Falkenmark indicator (renewable freshwater per person per year): > 1,700 m³ no stress; 1,000-1,700 m³ stress; 500-1,000 m³ scarcity; < 500 m³ absolute scarcity.'
    if slot.d <= 2:
        return dict(stem=f'{c[0].upper() + c[1:]} has about {vol} km³ of total renewable freshwater per year and a population of {pop} million. {rule} Calculate the water available per person and classify it.',
                    answer=f'{vol} × 10⁹ m³ / {pop} × 10⁶ = {pc:,.0f} m³ per person per year → {cat}',
                    markingKey=f'M1 convert km³ to m³ (×10⁹) and divide by population; A1 {pc:,.0f} m³; A1 category.', marks=mk(slot, 3))
    g = rng.choice([1.5, 2, 2.5, 3])
    yrs = rng.choice([20, 25, 30])
    pop2 = pop * (1 + g / 100) ** yrs
    pc2 = vol * 1e9 / (pop2 * 1e6)
    cat2 = ('absolute scarcity' if pc2 < 500 else 'scarcity' if pc2 < 1000 else 'stress' if pc2 < 1700 else 'no stress')
    return dict(stem=f'{c[0].upper() + c[1:]} has {vol} km³ of renewable freshwater per year and {pop} million people, growing at {g}% per year. {rule} (a) Calculate current water availability per person and classify it. (b) Calculate the availability after {yrs} years if supply is unchanged and classify it. (c) Evaluate two strategies the government could use to improve water security.',
                answer=f'(a) {pc:,.0f} m³ → {cat} (b) population {pop2:.1f} million; {pc2:,.0f} m³ → {cat2} (c) e.g. desalination (reliable supply, as in Israel\'s Sorek plant, but energy-intensive and produces brine); wastewater recycling (Singapore NEWater; public acceptance needed); drip irrigation and pricing to cut agricultural demand; inter-basin transfer (costly, conflict risk).',
                markingKey=f'(a) A1 {pc:,.0f}, A1 category. (b) M1 compound growth, A1 {pc2:,.0f} and category. (c) R1 R1 evaluated strategies.', marks=mk(slot, 6))


VW = [('beef', 15415, 'kg'), ('pork', 5988, 'kg'), ('chicken', 4325, 'kg'), ('rice', 2497, 'kg'), ('wheat bread', 1608, 'kg'),
      ('potatoes', 287, 'kg'), ('tomatoes', 214, 'kg'), ('apples', 822, 'kg'), ('cheese', 5060, 'kg'), ('milk', 1020, 'litre'),
      ('eggs', 3265, 'kg'), ('chocolate', 17196, 'kg')]


@gen('water_footprint')
def g_water_fp(rng, slot):
    k = 2 if slot.d <= 2 else 3 if slot.d == 3 else 4
    items = rng.sample(VW, k)
    qty = [rng.choice([0.25, 0.5, 1, 1.5, 2, 3]) for _ in items]
    tot = sum(v * q for (_, v, _), q in zip(items, qty))
    tab = '; '.join(f'{n} {v:,} L per {u}' for n, v, u in items)
    buy = ', '.join(f'{q:g} {u} of {n}' for (n, v, u), q in zip(items, qty))
    who = name(rng)
    if slot.d <= 3:
        return dict(stem=f'Global average water footprints (Water Footprint Network): {tab}. {who}\'s family buys {buy} each week. Calculate the weekly virtual-water footprint of these items.',
                    answer=' + '.join(f'{q:g} × {v:,}' for (n, v, u), q in zip(items, qty)) + f' = {tot:,.0f} L per week',
                    markingKey=f'M1 quantity × footprint for each item; A1 total {tot:,.0f} L.', marks=mk(slot, 3 if slot.d == 3 else 2))
    sw = max(items, key=lambda x: x[1])
    alt = min(VW, key=lambda x: x[1])
    q_sw = qty[items.index(sw)]
    saving = q_sw * (sw[1] - alt[1])
    return dict(stem=f'Global average water footprints (Water Footprint Network): {tab}; {alt[0]} {alt[1]:,} L per {alt[2]}. {who}\'s household buys {buy} each week. (a) Calculate the weekly water footprint. (b) Calculate the annual saving if the {sw[0]} were replaced by the same mass of {alt[0]}. (c) Explain why water footprints vary between places and evaluate their usefulness for consumers.',
                answer=f'(a) {tot:,.0f} L per week (b) {q_sw:g} × ({sw[1]:,} − {alt[1]:,}) × 52 = {saving * 52:,.0f} L per year (c) depends on climate (evapotranspiration), irrigation efficiency, feed type and yields; green vs blue vs grey water differ in impact. Useful for awareness and comparing products, but a litre of rain-fed (green) water in a wet region has less impact than blue water from a stressed aquifer, so a single figure can mislead.',
                markingKey=f'(a) A1 {tot:,.0f}. (b) M1 difference × quantity × 52, A1 {saving * 52:,.0f}. (c) R1 variation reasons, R1 evaluation (green/blue/grey; local scarcity).', marks=mk(slot, 6))


FISH = [('Atlantic cod on the Grand Banks', 'thousand tonnes'), ('North Sea herring', 'thousand tonnes'),
        ('Peruvian anchoveta', 'million tonnes'), ('a lake whitefish stock in Lake Superior', 'tonnes'),
        ('southern bluefin tuna', 'thousand tonnes'), ('Pacific halibut', 'thousand tonnes'), ('Patagonian toothfish', 'thousand tonnes')]


@gen('msy')
def g_msy(rng, slot):
    sp_, u = pick(rng, FISH)
    K = rng.choice([200, 400, 600, 800, 1000, 1500, 2400])
    r = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.8])
    msy = r * K / 4
    head = f'A Schaefer surplus-production model for {sp_} gives intrinsic growth rate r = {r} per year and carrying capacity K = {comma(K)} {u}; surplus yield Y = rN(1 − N/K).'
    if slot.d <= 2:
        return dict(stem=f'{head} Calculate the maximum sustainable yield (MSY) and the stock size at which it occurs.',
                    answer=f'MSY occurs at N = K/2 = {K / 2:g} {u}; MSY = rK/4 = {r} × {K} / 4 = {msy:g} {u} per year',
                    markingKey=f'A1 N = K/2 = {K / 2:g}; M1 rK/4, A1 {msy:g}.', marks=mk(slot, 3))
    N = rng.choice([0.2, 0.3, 0.7, 0.8]) * K
    Y = r * N * (1 - N / K)
    q = rng.choice([1.1, 1.25, 1.4])
    quota = round(msy * q, 1)
    return dict(stem=f'{head} The stock is currently estimated at {N:g} {u}. (a) Calculate the MSY and the current surplus yield. (b) A fishing industry body proposes a quota of {quota:g} {u} per year. Explain the likely consequence for the stock. (c) Evaluate the use of MSY as the basis of fisheries management, with reference to a named fishery.',
                answer=f'(a) MSY = {msy:g} {u} per year at N = {K / 2:g}; current Y = {r} × {N:g} × (1 − {N:g}/{K}) = {Y:.1f} {u} per year (b) the quota exceeds both MSY and current surplus production, so the catch removes more than natural increase; the stock will decline, reducing future yields and risking collapse (as with Grand Banks cod, 1992). (c) MSY gives a clear, science-based target, but r and K are uncertain and change with environment; it ignores age structure, bycatch and ecosystem interactions; variable recruitment and political pressure lead to quotas above advice; precautionary targets (e.g. F below F_MSY, ecosystem-based management) are safer.',
                markingKey=f'(a) A1 {msy:g}, M1 substitution, A1 {Y:.1f}. (b) R1 harvest > surplus → decline, R1 named consequence. (c) R1 strength, R1 limitation with example.', marks=mk(slot, 7 if slot.d >= 5 else 6))


AQUA = [('Atlantic salmon in Norwegian sea cages', 1.2, 1.35), ('tilapia in ponds in Egypt', 1.4, 1.8),
        ('whiteleg shrimp in Thai ponds', 1.4, 1.8), ('pangasius catfish in the Mekong Delta', 1.5, 1.8),
        ('rainbow trout in Danish raceways', 1.0, 1.2), ('carp in Chinese polyculture ponds', 1.5, 2.0)]


@gen('fcr')
def g_fcr(rng, slot):
    sp_, lo, hi = pick(rng, AQUA)
    gain = rng.randint(20, 400) * 10
    fcr = round(rng.uniform(lo, hi), 2)
    feed = round(gain * fcr)
    fcr2 = feed / gain
    if slot.d <= 2:
        return dict(stem=f'A farm raising {sp_} used {comma(feed)} tonnes of feed to produce a {comma(gain)}-tonne increase in fish biomass. Calculate the feed conversion ratio (FCR).',
                    answer=f'FCR = feed ÷ weight gain = {comma(feed)} / {comma(gain)} = {fcr2:.2f}',
                    markingKey=f'M1 feed ÷ gain; A1 {fcr2:.2f}.', marks=mk(slot, 2))
    fm = rng.choice([0.15, 0.2, 0.25, 0.3])
    ratio = rng.choice([4.0, 4.5, 5.0])
    wild = feed * fm * ratio
    fifo = wild / gain
    return dict(stem=f'A farm raising {sp_} used {comma(feed)} t of feed to produce {comma(gain)} t of fish. {int(fm * 100)}% of the feed is fishmeal, and it takes about {ratio:g} t of wild forage fish (e.g. anchoveta) to make 1 t of fishmeal. (a) Calculate the FCR. (b) Calculate the wild fish used and the fish-in : fish-out ratio. (c) Discuss whether this form of aquaculture reduces pressure on wild fish stocks.',
                answer=f'(a) {fcr2:.2f} (b) {comma(feed)} × {fm} × {ratio:g} = {comma(wild)} t of wild fish; FIFO = {fifo:.2f} (c) ' + ('FIFO > 1, so the farm consumes more wild fish than it produces - it increases pressure on forage fisheries; ' if fifo > 1 else 'FIFO < 1, so the farm produces more fish than it consumes; ') + 'replacing fishmeal with plant proteins, insect meal or algal oils, and farming herbivorous species (carp, tilapia) lowers pressure; impacts also include escapes, disease (sea lice) and nutrient pollution.',
                markingKey=f'(a) A1 {fcr2:.2f}. (b) A1 {comma(wild)} t, A1 FIFO {fifo:.2f}. (c) R1 interpretation, R1 evaluation with alternatives.', marks=mk(slot, 6))


@gen('bod')
def g_bod(rng, slot):
    sites = pick(rng, [('upstream of a sewage-treatment works', 'downstream of the outfall'),
                       ('above a dairy farm on the River Usk', 'below the farm drainage ditch'),
                       ('at a spring-fed headwater', 'below a paper mill'),
                       ('in a clean reference stream', 'in an urban canal after a storm overflow')])
    d0a = round(rng.uniform(9.0, 11.0), 1)
    d5a = round(d0a - rng.uniform(0.5, 2.5), 1)
    d0b = round(rng.uniform(7.0, 9.5), 1)
    d5b = round(d0b - rng.uniform(4.0, 6.5), 1)
    if d5b < 0.5:
        return None
    ba, bb = d0a - d5a, d0b - d5b
    rule = 'Guide: BOD₅ < 3 mg/L clean; 3-5 mg/L moderately polluted; > 5 mg/L polluted.'
    cls = lambda b: 'clean' if b < 3 else 'moderately polluted' if b <= 5 else 'polluted'
    if slot.d <= 2:
        return dict(stem=f'A water sample taken {sites[0]} had {d0a} mg/L dissolved oxygen when collected and {d5a} mg/L after incubation in the dark at 20 °C for 5 days. Calculate the BOD₅. {rule}',
                    answer=f'BOD₅ = {d0a} − {d5a} = {ba:.1f} mg/L → {cls(ba)}', markingKey=f'M1 initial DO − DO after 5 days; A1 {ba:.1f} mg/L.', marks=mk(slot, 2))
    return dict(stem=f'Dissolved-oxygen readings (mg/L) when sampled and after 5 days\' dark incubation at 20 °C: {sites[0]} {d0a} → {d5a}; {sites[1]} {d0b} → {d5b}. {rule} (a) Calculate the BOD₅ at each site and classify the water. (b) Explain why BOD rises downstream of organic pollution. (c) Explain why the samples are incubated in the dark.',
                answer=f'(a) {ba:.1f} mg/L ({cls(ba)}); {bb:.1f} mg/L ({cls(bb)}) (b) organic matter (sewage, slurry, pulp) is broken down by aerobic decomposers whose respiration uses dissolved oxygen; more organic matter → more decomposers → greater oxygen demand (and lower DO for fish and invertebrates). (c) to stop photosynthesis by algae adding oxygen, so the fall in DO reflects only respiration.',
                markingKey=f'(a) A1 {ba:.1f}, A1 {bb:.1f} with classes. (b) R1 decomposition by aerobic microbes, R1 uses DO. (c) R1 prevents photosynthesis.', marks=mk(slot, 5))


BMWP = [('Heptageniidae (flat mayfly nymphs)', 10), ('Perlidae (stonefly nymphs)', 10), ('Leptoceridae (cased caddisfly larvae)', 10),
        ('Ephemeridae (burrowing mayfly nymphs)', 10), ('Rhyacophilidae (caseless caddis larvae)', 7), ('Gammaridae (freshwater shrimps)', 6),
        ('Baetidae (swimming mayfly nymphs)', 4), ('Asellidae (water louse)', 3), ('Lymnaeidae (pond snails)', 3),
        ('Glossiphoniidae (leeches)', 3), ('Chironomidae (non-biting midge larvae)', 2), ('Oligochaeta (sludge worms)', 1)]


@gen('bmwp')
def g_bmwp(rng, slot):
    clean = rng.random() < 0.5
    pool = BMWP[:8] if clean else BMWP[5:]
    k = rng.randint(4, min(7, len(pool)))
    fams = rng.sample(pool, k)
    tot = sum(s for _, s in fams)
    aspt = tot / k
    tab = '; '.join(f'{n}: {s}' for n, s in fams)
    verdict = 'good water quality (ASPT above about 5)' if aspt > 5 else 'moderate to poor water quality (ASPT 5 or below)'
    return dict(stem=pick(rng, [f'A kick-sample from a river contained these invertebrate families, with their BMWP scores: {tab}. (a) Calculate the BMWP score and the average score per taxon (ASPT). (b) Use the ASPT to comment on water quality and explain why indicator species are used.',
                                f'Families found in a stream survey (BMWP score after each family): {tab}. (a) Calculate the BMWP score and the ASPT. (b) Interpret the result and explain why biotic indices complement chemical tests.']),
                answer=f'(a) BMWP = {tot}; ASPT = {tot}/{k} = {aspt:.1f} (b) {verdict}; high-scoring taxa (stoneflies, mayflies) need high dissolved oxygen, so their presence or absence integrates water quality over time, whereas a chemical test gives only a snapshot.',
                markingKey=f'(a) A1 {tot}, A1 {aspt:.1f}. (b) R1 interpretation, R1 indicator species reflect conditions over time / pollution-sensitive taxa.', marks=mk(slot, 4))


@gen('nitrate_load')
def g_nitrate(rng, slot):
    river = pick(rng, ['the River Wensum, Norfolk', 'a tributary of the Mississippi in Iowa', 'a river draining into the Baltic Sea',
                       'a stream flowing into Lake Taihu', 'a river entering Chesapeake Bay', 'a canal draining into the Lagoon of Venice'])
    c = round(rng.uniform(2, 18), 1)
    q = round(rng.uniform(0.5, 40), 1)
    load = c * q * 86.4
    if slot.d <= 2:
        c2 = round(c * rng.uniform(1.2, 2.5), 1)
        pct = (c2 - c) / c * 100
        return dict(stem=f'Nitrate concentration in {river} rose from {c} mg/L to {c2} mg/L after fertiliser was applied to the catchment. Calculate the percentage increase.',
                    answer=f'({c2} − {c}) / {c} × 100 = {pct:.0f}%', markingKey=f'M1 change ÷ original × 100; A1 {pct:.0f}%.', marks=mk(slot, 2))
    red = rng.choice([20, 30, 40, 50])
    return dict(stem=f'{river[0].upper() + river[1:]} has a nitrate concentration of {c} mg/L and a mean discharge of {q} m³/s. (1 mg/L = 1 g/m³; there are 86,400 s in a day.) (a) Calculate the daily nitrate load in kg. (b) Calculate the load if catchment measures cut the concentration by {red}%. (c) Explain how this nitrate could cause eutrophication downstream and suggest two measures to achieve the reduction.',
                answer=f'(a) {c} g/m³ × {q} m³/s × 86,400 s = {load:,.0f} kg per day (b) {load * (1 - red / 100):,.0f} kg per day (c) nitrate fertilises algal growth → algal bloom shades out plants → algae die and are decomposed by bacteria → BOD rises and DO falls → fish die (hypoxic "dead zone"). Measures: buffer strips and wetlands, precision fertiliser application / nitrate vulnerable zones, cover crops, upgrading sewage treatment.',
                markingKey=f'(a) M1 concentration × discharge × time, A1 {load:,.0f}. (b) A1. (c) R1 R1 eutrophication sequence, R1 two measures.', marks=mk(slot, 6))


# =============================================================================================
# ch01 1.1 Perspectives
# =============================================================================================
S('ch01-st1',
  terms=[('environmental value system (EVS)', 'a worldview or paradigm that shapes the way an individual or group perceives and evaluates environmental issues, influenced by cultural, religious, economic and socio-political context'),
         ('ecocentrism', 'a nature-centred worldview that gives intrinsic value to all life and ecosystems, emphasises self-restraint and minimal disturbance of natural processes, and distrusts large-scale technology'),
         ('anthropocentrism', 'a human-centred worldview in which humans manage the environment sustainably for human benefit, often through regulation, taxes and incentives'),
         ('technocentrism', 'a worldview that trusts science and technology to solve environmental problems and allow continued economic growth'),
         ('intrinsic value', 'the value something has in itself, independent of its usefulness to humans'),
         ('instrumental value', 'the value something has because it is useful to humans, e.g. timber, food or recreation')],
  facts=[('Which of the following positions is most typical of a deep ecologist?', 'Nature has intrinsic value and human population and consumption should be reduced', ['Geo-engineering can offset any emissions', 'Markets will price scarcity and drive substitution', 'Resources should be managed for maximum human benefit'], 'Deep ecology (Arne Næss, 1973) is a strongly ecocentric position.'),
         ('Which response to climate change is most technocentric?', 'Deploying direct-air capture and solar radiation management', ['Reducing consumption and flying less', 'A carbon tax with dividends', 'Protecting peatlands as sacred landscapes'], 'Technocentrists expect technological solutions to allow continued growth.'),
         ('Which statement best describes an environmental manager (anthropocentric) EVS?', 'The environment should be managed through legislation and economic tools for long-term human benefit', ['Nature should be left entirely undisturbed', 'Technology will always find substitutes', 'Spiritual connection with land is the main goal'], 'Environmental managers sit in the middle of the spectrum.'),
         ('Which of the following is NOT a factor that shapes an individual\'s EVS?', 'The second law of thermodynamics', ['Religion and culture', 'Education and the media', 'Economic and political context'], 'EVSs are shaped by social influences, not physical laws.')],
  why=[('Explain why two people can reach different conclusions about the same environmental data.', 'Each interprets evidence through an EVS shaped by culture, religion, economics, politics and personal experience; values decide which outcomes matter (jobs, wildlife, rights), how risk is weighed and which solutions are acceptable.'),
       ('Explain how an EVS can be understood as a system.', 'It has inputs (education, culture, religion, media, peers, experience), processes (thinking, weighing evidence), and outputs (decisions, actions, voting, consumer choices), with feedback as experiences reinforce or change values.'),
       ('Explain why a technocentrist and an ecocentrist might respond differently to declining fish stocks.', 'A technocentrist would favour aquaculture, better stock models or new feed technology to keep supply rising; an ecocentrist would favour reduced consumption, no-take marine reserves and protecting the ecosystem for its own sake.'),
       ('Explain why EVSs are said to lie on a spectrum rather than in fixed categories.', 'Most people hold mixed views that vary with issue and context (e.g. supporting renewables but also wilderness protection); positions shade from deep ecologist and self-reliance soft ecologist through environmental manager to cornucopian.')],
  contrast=[('ecocentrism', 'technocentrism', 'Ecocentrism puts nature first, values self-restraint and small-scale, low-impact solutions and distrusts technology; technocentrism trusts human ingenuity and technology to solve problems and sustain growth.'),
            ('intrinsic value', 'instrumental value', 'Intrinsic value is value in itself regardless of human use; instrumental value is value because it serves human ends (resources, services, recreation).'),
            ('a cornucopian', 'a deep ecologist', 'A cornucopian sees resources as effectively unlimited through technology and markets; a deep ecologist gives nature equal value to humans and argues for reducing human impact and population.')],
  misc=[('Anthropocentrists do not care about the environment.', 'Anthropocentrists (environmental managers) actively protect the environment, but mainly for its value to people, through laws, quotas, taxes and incentives.'),
        ('A person\'s EVS is fixed for life.', 'EVSs change with education, experience, media, culture and events (e.g. a disaster or travel can shift views).'),
        ('Technocentrism means ignoring environmental problems.', 'Technocentrists recognise problems but believe science and technology (e.g. renewables, GM crops, carbon capture) can solve them.')],
  apply=[('A government proposes a dam that will flood a forest valley. Suggest how an ecocentrist, an anthropocentrist and a technocentrist might each respond.', 'Ecocentrist: oppose; the valley has intrinsic value, favour energy saving and small-scale renewables. Anthropocentrist: support only with an EIA, compensation, fish passes and protected areas elsewhere. Technocentrist: support; hydropower is low-carbon and engineering can mitigate impacts.', 3),
         ('Identify the EVS shown by each statement: (i) "Nuclear fusion will give us unlimited clean energy." (ii) "A carbon tax will make polluters pay." (iii) "Rivers have the right to flow freely."', '(i) technocentric (cornucopian) (ii) anthropocentric (environmental manager) (iii) ecocentric (deep ecology / rights of nature).', 3),
         ('Outline how the media could influence the EVS of a teenager.', 'Documentaries (e.g. Blue Planet II on plastics), social media campaigns and news of disasters can raise awareness and shift values towards ecocentrism; advertising can reinforce consumerist, technocentric values.', 2)],
  cases=[('the rights-of-nature status of the Whanganui River, New Zealand (2017)', 'Te Awa Tupua Act granted the river legal personhood, reflecting the Māori view that the river is an ancestor', 'an ecocentric EVS embedded in law', 'the river is given rights in itself, independent of its usefulness, and guardians speak for it'),
         ('the Three Gorges Dam, China', 'the dam (completed 2006, 22.5 GW) displaced about 1.3 million people to provide hydroelectricity and flood control', 'a technocentric EVS', 'large-scale engineering was trusted to meet energy needs and control nature for economic growth'),
         ('the EU Emissions Trading System (2005)', 'a cap-and-trade market sets a falling cap on CO₂ emissions and lets firms trade allowances', 'an anthropocentric, environmental-manager EVS', 'markets and regulation are used to manage the environment for long-term human benefit'),
         ('the Bishnoi community of Rajasthan', 'in 1730, 363 Bishnoi were killed protecting khejri trees at Khejarli, and the community still protects trees and blackbuck', 'an ecocentric EVS rooted in religion', 'religious principles give intrinsic value to trees and animals and motivate self-sacrifice to protect them')],
  evaluate=[('Technocentric solutions are the most effective way to address climate change.', ['renewable costs have fallen ~90% (solar PV since 2010)', 'technology allows emissions cuts without large lifestyle change', 'innovation spreads globally'], ['rebound effects can cancel efficiency gains', 'unproven technologies (direct-air capture) may delay action', 'ecocentric demand reduction is cheaper and immediate'], 'Technology is essential but insufficient; a mix of technological, regulatory (anthropocentric) and behavioural (ecocentric) responses is most effective.'),
            ('An ecocentric value system is unrealistic in a world of eight billion people.', ['billions depend on intensive agriculture and energy use', 'self-restraint is hard to enforce', 'economic development is a priority for low-income countries'], ['ecocentric practices (agroecology, Indigenous land management) sustain productivity', 'overshoot of planetary boundaries requires reduced consumption', 'rights-of-nature laws (Ecuador 2008) show it can work'], 'Pure ecocentrism is hard to implement at scale, but ecocentric principles are increasingly embedded in policy and are needed to avoid overshoot.')],
  extended=[('Discuss how the EVS of a society might influence its response to plastic pollution. [9]', 'Ecocentric societies: bans, reduce/reuse, zero-waste lifestyles; anthropocentric: levies (UK 5p bag charge cut supermarket bag use by over 95%), deposit-return schemes, regulation (EU Single-Use Plastics Directive 2019); technocentric: bioplastics, chemical recycling, ocean clean-up technology. Evaluate effectiveness and conclude that mixed approaches work best.', 9, 'long')],
  res=[('Survey of 200 students at an international school: "Which statement best matches your view?" Technology will solve environmental problems 34%; Governments should regulate and tax pollution 41%; Humans must consume less and respect nature\'s rights 25%.',
        [('Identify the EVS represented by each statement and the most common EVS in the sample.', 'Technocentric, anthropocentric (environmental manager), ecocentric; anthropocentric is most common (41%).'),
         ('Calculate how many students held an ecocentric view and suggest one limitation of the survey.', '25% of 200 = 50 students; e.g. forced choice hides mixed views; sample from one school is not representative; wording may bias answers.')])])

S('ch01-st2',
  terms=[('environmental movement', 'the social and political movement, growing from the 1960s, that seeks to protect the environment through awareness, lobbying, legislation and direct action'),
         ('Silent Spring', 'the 1962 book by Rachel Carson describing the effects of pesticides such as DDT on birds and ecosystems, often seen as the start of the modern environmental movement'),
         ('Earth Day', 'an annual day of environmental awareness first held on 22 April 1970 in the USA, now observed worldwide'),
         ('Brundtland Report', 'the 1987 UN report "Our Common Future" that defined sustainable development as meeting the needs of the present without compromising the ability of future generations to meet their own needs'),
         ('NGO', 'a non-governmental organisation, such as Greenpeace or WWF, that campaigns or acts independently of governments')],
  facts=[('Which event in 1984 killed thousands of people when methyl isocyanate gas leaked from a pesticide plant?', 'The Bhopal disaster, India', ['The Chernobyl accident, Ukraine', 'The Minamata poisoning, Japan', 'The Exxon Valdez spill, Alaska'], 'The Union Carbide leak killed at least 3,800 people immediately (estimates up to 16,000).'),
         ('Which 1972 conference was the first major UN conference on the human environment and led to UNEP?', 'The Stockholm Conference', ['The Rio Earth Summit', 'The Kyoto conference', 'The Montreal conference'], 'UNEP was established in 1972 following Stockholm.'),
         ('Which 1986 event spread radioactive contamination across Europe and increased public opposition to nuclear power?', 'The Chernobyl accident', ['The Three Mile Island accident', 'The Fukushima accident', 'The Windscale fire'], 'Chernobyl reactor 4 exploded on 26 April 1986.'),
         ('Which disease, first identified in Japan in 1956, was caused by industrial mercury discharged into a bay?', 'Minamata disease', ['Itai-itai disease', 'Legionnaires\' disease', 'Black lung disease'], 'Chisso Corporation discharged methylmercury that biomagnified in fish.'),
         ('Who founded the Green Belt Movement in Kenya in 1977?', 'Wangari Maathai', ['Vandana Shiva', 'Greta Thunberg', 'Chico Mendes'], 'The movement has planted over 50 million trees; Maathai won the Nobel Peace Prize in 2004.')],
  why=[('Explain why Silent Spring was so influential.', 'It used scientific evidence in accessible language to show that DDT biomagnified, thinning eggshells of birds of prey; it raised public awareness, challenged industry and led to the US DDT ban (1972) and the creation of the EPA (1970).'),
       ('Explain how major disasters have shaped the environmental movement.', 'Disasters such as Minamata, Bhopal, Chernobyl and the Exxon Valdez gave vivid evidence of harm, generated media coverage and public anger, and led to new laws, institutions and international agreements.'),
       ('Explain the role of social media in the modern environmental movement.', 'It spreads information and images rapidly, allows global coordination (e.g. Fridays for Future strikes from 2018 involving millions), gives a voice to young people and Indigenous groups, but can also spread misinformation.'),
       ('Explain why international conferences have been important to environmental progress.', 'Environmental problems cross borders; conferences (Stockholm 1972, Rio 1992, Paris 2015) set shared goals, create treaties and institutions (UNEP, UNFCCC, CBD) and put pressure on governments.')],
  contrast=[('a pressure group (NGO)', 'a government agency', 'An NGO is independent, campaigns and can use direct action or lobbying but cannot make law; a government agency (e.g. the US EPA) has legal authority to regulate and enforce.'),
            ('the Stockholm Conference (1972)', 'the Rio Earth Summit (1992)', 'Stockholm was the first UN conference on the human environment and created UNEP; Rio produced Agenda 21, the Rio Declaration and opened the UNFCCC and the Convention on Biological Diversity for signature.')],
  misc=[('The environmental movement began with climate-change protests in the 2010s.', 'The modern movement grew from the 1960s (Silent Spring, Earth Day 1970); earlier roots include 19th-century conservation such as Yellowstone National Park (1872).'),
        ('Environmental disasters only lead to local changes.', 'Disasters often trigger national laws and international agreements, e.g. Minamata led to the Minamata Convention on Mercury (2013).')],
  apply=[('Suggest two ways in which a named environmental disaster changed policy or attitudes.', 'e.g. Chernobyl (1986): Europe-wide radiation monitoring, increased opposition to nuclear power (Italy voted to phase it out in 1987), international nuclear safety conventions.', 2),
         ('Outline how one named individual has influenced environmental attitudes.', 'e.g. Greta Thunberg: school strike from 2018 grew into the global Fridays for Future movement, increasing youth engagement and pressure on governments.', 2),
         ('Outline the significance of the 1992 Rio Earth Summit.', 'It produced Agenda 21 and the Rio Declaration, and opened the UNFCCC and the Convention on Biological Diversity for signature, putting sustainable development on the global agenda.', 3)],
  cases=[('the Minamata mercury poisoning, Japan', 'Chisso Corporation discharged methylmercury into Minamata Bay from 1932 to 1968; it biomagnified in fish and caused severe neurological disease in thousands', 'how disasters shape environmental law', 'public outrage and court cases led to Japanese pollution-control laws and eventually the global Minamata Convention (2013)'),
         ('the Chipko movement, India (1973)', 'villagers in Uttarakhand, many of them women, hugged trees to prevent commercial logging', 'grassroots environmental activism', 'local people used non-violent direct action to defend forests and livelihoods, leading to a 15-year ban on green felling in the Himalayan forests of Uttar Pradesh in 1980'),
         ('the Exxon Valdez oil spill, Alaska (1989)', 'about 41 million litres of crude oil spilled into Prince William Sound, killing hundreds of thousands of seabirds', 'the influence of media coverage on policy', 'television images drove public pressure and led to the US Oil Pollution Act (1990) requiring double-hulled tankers')],
  evaluate=[('Individuals have had more influence on the environmental movement than governments.', ['Carson, Maathai and Thunberg changed public attitudes', 'grassroots movements (Chipko) achieved real protection'], ['governments create binding law (Clean Air Acts, Montreal Protocol)', 'international agreements require state action'], 'Individuals often start change by shifting values, but lasting impact depends on governments translating it into law and policy.'),
            ('Environmental disasters have been the main driver of environmental awareness.', ['Minamata, Bhopal and Chernobyl created public outrage and new laws', 'media images spread quickly'], ['science and education (IPCC reports) build awareness steadily', 'literature, documentaries and activists also drive change'], 'Disasters accelerate awareness, but sustained change depends on science, education and activism.')],
  extended=[('Examine the role of NGOs in the environmental movement. [9]', 'Roles: raising awareness (WWF campaigns), research and monitoring, lobbying at conferences (COP), direct action (Greenpeace Rainbow Warrior protests), legal challenges (ClientEarth), on-the-ground conservation. Limits: no legal authority, funding constraints, may be seen as biased. Judgement on effectiveness.', 9, 'long')],
  res=[('Timeline: 1872 Yellowstone National Park; 1962 Silent Spring; 1970 first Earth Day (about 20 million Americans took part); 1972 Stockholm Conference; 1987 Montreal Protocol and Brundtland Report; 1992 Rio Earth Summit; 2015 Paris Agreement; 2018 Fridays for Future begins.',
        [('Calculate the number of years between Silent Spring and the Paris Agreement, and identify two events in the timeline that created international institutions or treaties.', '2015 − 1962 = 53 years; e.g. Stockholm (UNEP), Montreal Protocol, Rio (UNFCCC, CBD), Paris Agreement.'),
         ('Suggest why the pace of international agreements increased after 1970.', 'Growing scientific evidence, media coverage of disasters, rise of NGOs and public pressure, recognition that problems such as ozone depletion cross borders.')])])

S('ch01-st3',
  terms=[('Indigenous knowledge', 'the knowledge, practices and beliefs developed by Indigenous peoples over many generations through close interaction with their environment, often passed on orally'),
         ('traditional ecological knowledge (TEK)', 'cumulative knowledge of relationships between living things and their environment, held by Indigenous and local communities'),
         ('stewardship', 'the responsible care and management of the environment on behalf of others and future generations'),
         ('cultural burning', 'the deliberate, low-intensity use of fire by Indigenous peoples, such as Aboriginal Australians, to manage landscapes and reduce fuel loads'),
         ('rights of nature', 'the legal principle that ecosystems or natural entities have rights of their own, as recognised in Ecuador\'s 2008 constitution')],
  facts=[('Which country\'s 2008 constitution was the first to recognise the rights of nature (Pachamama)?', 'Ecuador', ['Bolivia', 'New Zealand', 'Costa Rica'], 'Article 71 gives nature the right to exist and regenerate.'),
         ('Approximately what share of the world\'s land area is managed or held by Indigenous peoples?', 'About a quarter', ['About 2%', 'About two-thirds', 'About 90%'], 'Studies estimate about 25% of land, overlapping about 40% of terrestrial protected areas.'),
         ('Which Indigenous practice in Australia reduces the risk of intense late-dry-season wildfires?', 'Early dry-season cultural burning', ['Planting eucalyptus monocultures', 'Draining wetlands', 'Fire suppression'], 'Cool burns create a mosaic of burnt patches that act as firebreaks.'),
         ('Which document, adopted in 2007, sets out the rights of Indigenous peoples including rights to land and free, prior and informed consent?', 'UN Declaration on the Rights of Indigenous Peoples (UNDRIP)', ['The Paris Agreement', 'The Ramsar Convention', 'Agenda 21'], 'UNDRIP was adopted by the UN General Assembly in 2007.')],
  why=[('Explain why Indigenous land management is often associated with high biodiversity.', 'Long-term, place-based knowledge and customary rules limit over-harvesting; practices such as rotational farming and cultural burning maintain habitat mosaics; secure land tenure resists deforestation (e.g. Indigenous territories in the Brazilian Amazon have lower deforestation rates).'),
       ('Explain why some Indigenous worldviews are described as ecocentric.', 'They often see humans as part of nature, with kinship or spiritual ties to land, rivers and animals; nature has intrinsic and sacred value and is held in trust for future generations.'),
       ('Explain why conflicts can arise between conservation projects and Indigenous peoples.', '"Fortress conservation" has removed people from protected areas, denying access to land and resources; outside priorities may ignore Indigenous rights, knowledge and consent.')],
  contrast=[('traditional ecological knowledge', 'Western scientific knowledge', 'TEK is holistic, place-based, built over generations and often transmitted orally and through practice; Western science is based on hypothesis testing, controlled measurement and peer review, and seeks generalisable laws. They can complement each other.'),
            ('fortress conservation', 'community-based conservation', 'Fortress conservation excludes local people from protected areas; community-based conservation involves local and Indigenous people in management and benefits (e.g. Namibian conservancies).')],
  misc=[('Indigenous peoples have no role in modern environmental management.', 'Indigenous rangers, co-management and TEK are central to many programmes, e.g. Kakadu National Park is jointly managed by Aboriginal owners and Parks Australia.'),
        ('All Indigenous peoples share one environmental value system.', 'There are about 476 million Indigenous people in over 90 countries with very diverse cultures, beliefs and practices.')],
  apply=[('Suggest two ways in which traditional ecological knowledge could help manage a fishery.', 'Seasonal closures linked to spawning knowledge (e.g. rāhui in Māori and Hawaiian tradition); knowledge of local stock changes over long periods; customary tenure limiting access.', 2),
         ('Outline how cultural burning in northern Australia contributes to climate-change mitigation.', 'Early dry-season cool burns reduce the area burnt by hot late fires, cutting greenhouse-gas emissions; Indigenous groups earn carbon credits under the Savanna Fire Management method.', 2)],
  cases=[('Kakadu National Park, Australia', 'the park is jointly managed by its Bininj/Mungguy traditional owners and Parks Australia, using early dry-season burning', 'Indigenous co-management of protected areas', 'Indigenous fire knowledge reduces destructive late-season fires and maintains habitat mosaics, while owners keep cultural ties to country'),
         ('the Kayapó territories in the Brazilian Amazon', 'about 10 million ha of Kayapó land form a barrier to deforestation along the agricultural frontier', 'the role of Indigenous land rights in conservation', 'secure tenure and active defence of the territory keep forest cover high compared with surrounding ranch land'),
         ('Te Urewera, New Zealand (2014)', 'a former national park was granted legal personhood under the Te Urewera Act, managed with Tūhoe', 'Indigenous worldviews shaping law', 'the law treats the land as a living entity with its own identity, reflecting Tūhoe relationships with the land')],
  evaluate=[('Indigenous knowledge should be given equal weight to scientific knowledge in environmental decision-making.', ['TEK holds long-term observations that science lacks', 'Indigenous management often protects biodiversity effectively', 'UNDRIP supports rights and consent'], ['TEK may be local and hard to generalise', 'integrating knowledge systems raises issues of ownership and verification', 'some traditional practices may not suit changed conditions'], 'Both should be valued and integrated; co-management that respects Indigenous rights and uses scientific monitoring achieves the best outcomes.'),
            ('Granting legal rights to nature is the most effective way to protect ecosystems.', ['gives ecosystems standing in court (Whanganui, Ecuador)', 'shifts values towards ecocentrism'], ['enforcement is weak - mining continues in Ecuador', 'courts and guardians need funding', 'conventional regulation may be more practical'], 'Rights of nature are a powerful symbolic and legal tool but need enforcement and integration with other policies to be effective.')],
  extended=[('Discuss the contribution of Indigenous and cultural perspectives to sustainable land management, with reference to named examples. [9]', 'Kakadu fire management, Kayapó territorial defence, Whanganui/Te Urewera personhood, Bishnoi tree protection, Satoyama landscapes in Japan; strengths (long-term knowledge, biodiversity outcomes) vs limits (pressure from development, weak rights, changing climate). Conclusion.', 9, 'long')],
  res=[('Data (study of the Brazilian Amazon, 2000-2012): mean annual deforestation rate inside Indigenous territories 0.15%; in strictly protected areas 0.40%; on unprotected land 2.0%.',
        [('Calculate how many times higher deforestation was on unprotected land than in Indigenous territories, and suggest one reason for the difference.', '2.0 / 0.15 ≈ 13 times; Indigenous peoples actively defend territories and have customary rules limiting clearance; legal tenure blocks ranching expansion.'),
         ('Suggest one limitation of comparing these rates directly.', 'Areas differ in accessibility (distance from roads and agricultural frontier), so lower rates may partly reflect remoteness rather than management.')])])


# =============================================================================================
# ch02 1.2 Systems
# =============================================================================================
S('ch02-st1', gens=['storage'],
  terms=[('system', 'a set of interrelated parts working together to make a complex whole, with storages, flows, inputs and outputs'),
         ('storage (stock)', 'a part of a system where matter or energy is held, such as a lake, a forest\'s biomass or the atmosphere\'s carbon'),
         ('flow', 'the movement of matter or energy into, out of or within a system, shown by arrows in a systems diagram'),
         ('open system', 'a system that exchanges both matter and energy with its surroundings, e.g. an ecosystem'),
         ('closed system', 'a system that exchanges energy but not matter with its surroundings, e.g. Earth (approximately) or Biosphere 2'),
         ('isolated system', 'a hypothetical system that exchanges neither matter nor energy with its surroundings; the universe may be the only example')],
  facts=[('Which of the following is the best example of an open system?', 'A pond ecosystem', ['Planet Earth', 'A sealed terrarium', 'The universe'], 'A pond gains and loses both matter (water, nutrients, organisms) and energy.'),
         ('In a systems diagram, what do boxes usually represent?', 'Storages', ['Flows', 'Feedback loops', 'Boundaries'], 'Boxes are storages; arrows are flows; arrow width may show flow size.'),
         ('Why is Earth described as approximately a closed system?', 'It exchanges energy with space but almost no matter', ['It exchanges neither matter nor energy', 'It exchanges matter but not energy', 'It has no internal flows'], 'Solar radiation enters and heat leaves; only tiny amounts of matter (meteorites, gas escape) cross the boundary.'),
         ('Which approach studies how components interact rather than examining each in isolation?', 'A systems approach (holistic)', ['A reductionist approach', 'A single-variable experiment', 'A taxonomic approach'], 'Systems thinking emphasises interactions, feedback and emergent properties.')],
  why=[('Explain why the systems approach is useful in environmental science.', 'Environmental issues involve many interacting parts across ecological, social and economic components; a systems approach shows flows, storages and feedback, allows prediction, reveals unintended consequences and links disciplines.'),
       ('Explain why Biosphere 2 is described as an attempt to create a closed system.', 'The 1.27-hectare sealed facility in Arizona allowed sunlight (energy) in and heat out but aimed to recycle all matter; oxygen levels fell from 21% to about 14% in 1991-93, showing how hard it is to sustain a closed system.'),
       ('Explain why boundaries of a system must be defined for a study.', 'Defining a boundary decides which storages and flows are internal and which are inputs and outputs, allows measurement and comparison, and makes the scale of the study clear (e.g. a single field vs a watershed).')],
  contrast=[('an open system', 'a closed system', 'An open system exchanges both matter and energy with its surroundings (a forest); a closed system exchanges energy but not matter (Earth approximately, a sealed bottle garden).'),
            ('a storage', 'a flow', 'A storage is a stock of matter or energy held at a moment (e.g. carbon in soil, in tonnes); a flow is a rate of movement between storages or across the boundary (tonnes per year).')],
  misc=[('A sealed terrarium is an isolated system.', 'It exchanges energy (light in, heat out), so it is a closed system; an isolated system exchanges neither matter nor energy.'),
        ('Systems diagrams show only physical components.', 'Systems in ESS can include social and economic components, e.g. a food system includes farmers, markets and consumers.')],
  apply=[('Draw (describe in words) a simple systems diagram for a lake, naming two inputs, two storages and two outputs.', 'Inputs: river inflow, precipitation, solar energy; storages: lake water, fish biomass, sediment; outputs: outflow, evaporation, heat, fish harvested.', 3),
         ('Classify each as open, closed or isolated: a city, the planet Earth, a sealed bottle of pond water left on a windowsill.', 'City: open; Earth: closed (approximately); sealed bottle: closed (energy only).', 3)],
  cases=[('Biosphere 2, Arizona (1991-1993)', 'eight people lived in a sealed 1.27 ha structure; oxygen fell from about 21% to 14% and oxygen had to be pumped in', 'the difficulty of maintaining a closed system', 'soil microbes respired more than expected and concrete absorbed CO₂, showing that matter cycling in closed systems is hard to balance'),
         ('the Aral Sea basin', 'irrigation diversions from the Amu Darya and Syr Darya reduced inflows, so the storage (sea volume) shrank by about 90%', 'how changing flows alters storages in an open system', 'when outputs (evaporation) exceed reduced inputs, the storage falls and the system shifts to a new state')],
  evaluate=[('A systems approach is more useful than a reductionist approach for understanding environmental issues.', ['shows interactions and feedback', 'reveals unintended consequences', 'integrates social and ecological components'], ['reductionist experiments give precise cause-and-effect evidence', 'systems models can be oversimplified or hard to test'], 'Both are needed: reductionist studies provide data, and the systems approach integrates them to understand whole issues.')],
  extended=[('Using a named example, explain how a change in one flow can affect several storages in an environmental system. [7]', 'e.g. Aral Sea: reduced river inflow → lower water storage, higher salinity, loss of fish biomass, exposed seabed salt storage → dust outputs, local climate change.', 7, 'explain')],
  res=[('Systems description - a tropical forest plot: storages: living biomass 300 t C/ha, soil 120 t C/ha, litter 5 t C/ha; flows: photosynthesis 25 t C/ha/yr, plant and soil respiration 24 t C/ha/yr, litterfall 8 t C/ha/yr, decomposition 8 t C/ha/yr.',
        [('Calculate the total carbon storage of the plot and the net annual exchange with the atmosphere.', '300 + 120 + 5 = 425 t C/ha; net uptake = 25 − 24 = 1 t C/ha/yr (a small sink).'),
         ('Identify whether the litter storage is in steady state and justify your answer.', 'Yes - inputs (litterfall 8) equal outputs (decomposition 8) so the litter storage stays constant.')])])

S('ch02-st2', gens=['storage'],
  terms=[('transfer', 'a process in which matter or energy moves from one place to another without changing state, e.g. water flowing in a river'),
         ('transformation', 'a process in which matter or energy changes state or form, e.g. evaporation of water or photosynthesis converting light to chemical energy'),
         ('model', 'a simplified version of reality used to understand, explain or predict how a system works'),
         ('emergent property', 'a characteristic of a system as a whole that is not present in its individual parts, e.g. resilience of an ecosystem')],
  facts=[('Which of the following is a transformation rather than a transfer?', 'Water evaporating from the ocean surface', ['Water flowing downhill in a river', 'Wind carrying pollen', 'Groundwater moving through an aquifer'], 'Evaporation changes the state of water (liquid to vapour).'),
         ('Which is the best example of an energy-to-matter transformation?', 'Photosynthesis', ['Respiration', 'Decomposition', 'Evaporation'], 'Light energy is converted into chemical energy stored in glucose.'),
         ('Which is a main limitation of climate models?', 'They simplify complex processes such as clouds and cannot include every variable', ['They never use real data', 'They cannot be run on computers', 'They always overestimate warming'], 'Models are useful but rely on assumptions and parameterisations.')],
  why=[('Explain why models are useful despite being simplified.', 'They allow complex systems to be visualised and understood, allow predictions and "what if" scenarios (e.g. IPCC emissions pathways), can be tested and improved with data, and help communicate ideas.'),
       ('Explain two limitations of models of environmental systems.', 'They omit variables and simplify interactions, so predictions may be inaccurate; assumptions and input data may be uncertain; results can be interpreted differently by people with different EVSs.'),
       ('Explain why photosynthesis and respiration are both examples of transformations.', 'Photosynthesis transforms light energy into chemical energy and inorganic CO₂ and water into organic glucose; respiration transforms chemical energy into usable energy (ATP) and heat, and organic matter back to CO₂ and water.')],
  contrast=[('a transfer', 'a transformation', 'A transfer moves matter or energy without changing its form or state (river flow); a transformation changes its form, state or chemical nature (evaporation, photosynthesis).'),
            ('a physical model', 'a computer (mathematical) model', 'A physical model is a tangible scaled representation (e.g. a stream table or terrarium); a computer model uses equations to simulate a system and can run many scenarios (e.g. a global climate model).')],
  misc=[('A model that has been tested is a perfect representation of reality.', 'All models simplify reality; even well-tested models have uncertainty and must be refined with new data.'),
        ('Rain falling into a lake is a transformation.', 'Rain falling is a transfer of water (no change of state); condensation in the cloud was the transformation.')],
  apply=[('Classify each process as a transfer or transformation: (i) runoff, (ii) condensation, (iii) a fox eating a rabbit, (iv) decomposition of leaf litter.', '(i) transfer (ii) transformation (iii) transfer of energy/matter between trophic levels (iv) transformation (organic to inorganic).', 4),
         ('Suggest one way a model of a fish population could be tested.', 'Compare model predictions with stock assessment surveys or catch data from previous years (hindcasting) and adjust parameters.', 2)],
  cases=[('IPCC climate models (AR6, 2021)', 'models project about 1.4 °C to 4.4 °C of warming by 2100 depending on the emissions scenario (SSP1-1.9 to SSP5-8.5)', 'the use and limitations of models', 'scenarios allow decision-makers to compare pathways, but the range reflects uncertainty about emissions, feedback and cloud processes'),
         ('the Limits to Growth World3 model (1972)', 'a computer model of population, resources, food and pollution projected overshoot and collapse in the 21st century under business as usual', 'how models can influence debate', 'it was criticised as too pessimistic but stimulated discussion of finite resources and sustainability')],
  evaluate=[('Computer models are the most reliable way to predict future environmental change.', ['integrate many variables and feedbacks', 'can be tested by hindcasting', 'allow scenarios'], ['uncertainty in inputs and processes', 'tipping points are hard to model', 'observations remain essential'], 'Models are powerful tools when combined with observations, but their predictions should be treated as ranges with uncertainty.')],
  extended=[('Evaluate the usefulness of systems diagrams as models of a named ecosystem. [9]', 'Strengths: show storages, flows, feedback; simplify complexity; communicate; allow quantification (e.g. Silver Springs energy flows). Limits: oversimplify, static, omit human factors, boundaries arbitrary. Judgement.', 9, 'long')],
  res=[('Description of a model of a sand-dune system: inputs - sand from the beach (wind transfer), seeds, solar energy; processes - colonisation by marram grass, accumulation of humus (transformation of dead organic matter); outputs - sand blown inland, heat.',
        [('Identify one transfer and one transformation in this model.', 'Transfer: wind blowing sand from the beach; transformation: dead plant material decomposed into humus (or photosynthesis by marram).'),
         ('Suggest one limitation of this model.', 'It omits human trampling, storms and rabbit grazing, and does not show the rates of flows.')])])

S('ch02-st3',
  terms=[('negative feedback', 'a feedback loop that counteracts change and tends to return a system to its original state, promoting stability'),
         ('positive feedback', 'a feedback loop that amplifies change and moves a system away from its starting state, towards a new equilibrium'),
         ('steady-state equilibrium', 'a condition of an open system in which there are fluctuations but no long-term change in average state, maintained by negative feedback'),
         ('tipping point', 'a critical threshold at which a small change causes a system to shift to a new, often irreversible, state'),
         ('resilience', 'the tendency of a system to avoid tipping points and maintain stability through steady-state equilibrium'),
         ('stable equilibrium', 'an equilibrium to which a system tends to return after a disturbance')],
  facts=[('Which of the following is an example of negative feedback?', 'A rise in prey numbers increases predators, which then reduce prey numbers', ['Melting sea ice exposes dark water which absorbs more heat', 'Thawing permafrost releases methane causing more warming', 'Forest loss reduces rainfall, causing more forest loss'], 'The predator response counteracts the initial change.'),
         ('Which feedback is linked to the ice-albedo effect?', 'Positive feedback', ['Negative feedback', 'Steady-state feedback', 'No feedback'], 'Less ice → lower albedo → more absorption → more warming → less ice.'),
         ('Which ecosystem is considered at risk of a tipping point to savanna if about 20-25% of it is deforested?', 'The Amazon rainforest', ['The Sahara Desert', 'The Antarctic ice sheet', 'The Great Barrier Reef'], 'Lovejoy and Nobre (2018) suggested 20-25% deforestation could trigger dieback.'),
         ('Which property describes a system with high diversity, large storages and fast regeneration?', 'High resilience', ['Low resilience', 'A tipping point', 'Positive feedback'], 'Diversity and large storages buffer disturbance.')],
  why=[('Explain why most natural ecosystems are dominated by negative feedback.', 'Negative feedback (e.g. predator-prey, density-dependent limiting factors) counteracts change and keeps populations and processes near a steady state, so systems that persist are generally those stabilised by negative feedback.'),
       ('Explain why tipping points are difficult to predict.', 'Systems are complex with many interacting feedbacks, time lags and non-linear responses; thresholds may only be recognised after they are crossed; data are limited and conditions vary.'),
       ('Explain how high biodiversity increases the resilience of an ecosystem.', 'More species means more feeding pathways and functional redundancy, so if one species declines another can fill its role; genetic diversity allows adaptation to change.'),
       ('Explain how melting of Arctic sea ice is an example of positive feedback.', 'Warming melts reflective ice (albedo ~0.6-0.8), exposing dark ocean (albedo ~0.06) which absorbs more solar radiation, causing further warming and more melting.')],
  contrast=[('positive feedback', 'negative feedback', 'Negative feedback counteracts a change and stabilises a system around an equilibrium; positive feedback amplifies a change and drives the system away from equilibrium, possibly to a tipping point.'),
            ('steady-state equilibrium', 'static equilibrium', 'Steady-state equilibrium is dynamic: inputs and outputs continue but balance, with small fluctuations (most natural systems); static equilibrium has no change or flow at all (e.g. a rock), which does not occur in living systems.')],
  misc=[('Positive feedback is always good for the environment.', '"Positive" means amplifying, not beneficial; positive feedback often drives harmful changes such as runaway warming.'),
        ('Once a tipping point is crossed the system can easily return to its original state.', 'Systems past a tipping point often show hysteresis; returning may require a much larger reverse change or be impossible on human timescales (e.g. loss of ice sheets).')],
  apply=[('Describe a negative feedback loop involving body temperature or a population, and a positive feedback loop involving climate.', 'Negative: predator-prey (snowshoe hare and lynx), or more deer → less food → more starvation → fewer deer. Positive: warming → permafrost thaw → methane release → more warming.', 4),
         ('Suggest how human activities can reduce the resilience of a coral reef.', 'Overfishing herbivorous fish, nutrient pollution favouring algae, and warming causing bleaching reduce diversity and storages, making the reef more likely to shift to an algal-dominated state.', 3)],
  cases=[('the Amazon rainforest', 'about 17-20% of the Amazon has been deforested; forest recycles rainfall through evapotranspiration, so loss reduces rainfall', 'a potential tipping point driven by positive feedback', 'deforestation reduces moisture recycling, causing drought and fire, which kills more forest and could shift parts of the system to degraded savanna'),
         ('snowshoe hare and Canada lynx populations', 'Hudson\'s Bay Company fur records show roughly 10-year cycles in both species, with lynx peaks lagging hare peaks', 'negative feedback in predator-prey systems', 'more hares support more lynx, whose predation reduces hares, which then reduces lynx - the populations oscillate about an equilibrium'),
         ('Lake eutrophication in Lake Erie', 'phosphorus inputs led to algal blooms in the 1960s-70s and again since 2011 (Toledo drinking water ban, 2014)', 'a shift between alternative stable states', 'once phosphorus exceeds a threshold, the lake flips from clear water to algal dominance, and internal phosphorus release from sediments maintains the new state')],
  evaluate=[('Tipping points make the precautionary principle essential in environmental management.', ['thresholds are uncertain and changes may be irreversible', 'costs of crossing (Amazon dieback) are enormous'], ['precaution can delay development', 'some systems are more resilient than feared'], 'Because tipping points are uncertain and potentially irreversible, precautionary action is justified, particularly for high-impact global systems.'),
            ('Human societies are more resilient than natural ecosystems.', ['technology, trade and planning allow adaptation', 'societies can learn and reorganise'], ['dependence on global supply chains creates vulnerability', 'societies depend on ecosystem services', 'past societies collapsed (Easter Island debate, Norse Greenland)'], 'Human resilience depends on the resilience of the ecosystems that support it, so the two cannot be separated.')],
  extended=[('Discuss the extent to which feedback mechanisms help to maintain equilibrium in natural systems. [9]', 'Negative feedback examples (predator-prey, Daisyworld/Gaia hypothesis), positive feedback examples (albedo, permafrost, Amazon dieback), tipping points and alternative stable states; human influence; judgement.', 9, 'long')],
  res=[('Graph description: Arctic September sea-ice extent (NSIDC) - 1980: 7.8 million km²; 2000: 6.3 million km²; 2012: 3.6 million km² (record low); 2020: 4.0 million km².',
        [('Calculate the percentage decrease in September sea-ice extent between 1980 and 2012.', '(7.8 − 3.6)/7.8 × 100 ≈ 54%.'),
         ('Explain how the trend shown could accelerate warming in the Arctic.', 'Ice-albedo positive feedback: less reflective ice and more dark ocean absorbs more energy, warming the water and melting more ice; the Arctic is warming about 3-4 times faster than the global average.')])])

S('ch02-st4', gens=['thermo'],
  terms=[('first law of thermodynamics', 'energy can be neither created nor destroyed; it can only be transformed from one form to another (the principle of conservation of energy)'),
         ('second law of thermodynamics', 'in any energy transformation, entropy increases and some energy is degraded to a less useful form, usually heat, so no transformation is 100% efficient'),
         ('entropy', 'a measure of the amount of disorder in a system; it increases as energy is dissipated'),
         ('efficiency', 'useful energy, work or output ÷ total energy, work or input, often expressed as a percentage')],
  facts=[('Which statement is a consequence of the second law of thermodynamics in ecosystems?', 'Energy decreases along a food chain as heat is lost in respiration', ['Energy increases at each trophic level', 'Matter is lost from ecosystems', 'Energy is recycled by decomposers'], 'Energy flows through ecosystems and is dissipated as heat.'),
         ('A coal power station converts 35% of the chemical energy in coal to electricity. What happens to most of the rest?', 'It is released as waste heat', ['It is destroyed', 'It is stored in ash', 'It is recycled into coal'], 'First law: energy is conserved; second law: it is degraded to low-grade heat.'),
         ('What is the typical efficiency of photosynthesis in converting incoming sunlight into biomass?', 'About 1-3%', ['About 10%', 'About 50%', 'About 90%'], 'Much light is reflected, the wrong wavelength or lost as heat.')],
  why=[('Explain why energy cannot be recycled in an ecosystem but matter can.', 'Matter (carbon, nitrogen) is conserved and returned to inorganic forms by decomposers; energy is degraded to heat at each transformation (second law) and radiated to space, so ecosystems need a continuous input of solar energy.'),
       ('Explain why food chains rarely have more than four or five trophic levels.', 'At each transfer much energy is lost as heat through respiration (second law), plus uneaten and egested material, so typically only about 10% passes on; after a few levels too little energy remains to support a viable population.'),
       ('Explain how living systems maintain order despite the second law of thermodynamics.', 'Organisms are open systems that use a continuous input of energy (sunlight or food) to build and maintain ordered structures, while increasing the entropy of their surroundings by releasing heat.')],
  contrast=[('the first law of thermodynamics', 'the second law of thermodynamics', 'The first law says energy is conserved (total input = total output); the second law says that in every transformation some energy is degraded to unusable heat, so efficiency is always below 100% and entropy rises.')],
  misc=[('Energy is lost from ecosystems, so the first law of thermodynamics does not apply.', 'Energy is not destroyed; it leaves the ecosystem as heat. "Lost" means no longer available to organisms, consistent with the first law.'),
        ('Decomposers recycle energy back to producers.', 'Decomposers recycle nutrients (matter); the energy they release in respiration is lost as heat.')],
  apply=[('Use the laws of thermodynamics to explain why eating plants rather than meat can support more people from the same area of land.', 'Each transfer between trophic levels loses ~90% of energy as heat (second law); eating producers directly avoids one transfer, so roughly ten times more food energy is available per hectare.', 3),
         ('Apply the laws of thermodynamics to a food chain grass → rabbit → fox.', 'First law: energy fixed by grass is conserved, passed on or lost as heat/in faeces/dead matter; second law: each transformation is inefficient, so the fox receives only a small fraction of the energy fixed by grass.', 3)],
  cases=[('the Silver Springs ecosystem, Florida (H.T. Odum, 1957)', 'producers fixed about 20,810 kcal m⁻² yr⁻¹ of GPP while top carnivores received only about 21 kcal m⁻² yr⁻¹', 'the second law of thermodynamics in ecosystems', 'energy declines by about two orders of magnitude at each step as respiration releases heat, so only about 0.1% of producer energy reaches top carnivores')],
  evaluate=[('The laws of thermodynamics place absolute limits on economic growth.', ['all production requires energy transformations that dissipate heat', 'resource use increases entropy; recycling cannot be 100%'], ['the Sun supplies a vast energy input (~174 PW), so energy is not the binding limit', 'growth can occur in services and efficiency'], 'Thermodynamics limits material throughput, but growth in value through efficiency and renewables is possible within those limits.')],
  extended=[('Explain, with reference to the laws of thermodynamics, the shape of a pyramid of energy. [4]', 'First law: energy entering each level equals energy stored + lost; second law: energy degraded as heat at each transformation; so each level is smaller (~10% passes on) and pyramids of energy are never inverted.', 4, 'explain')],
  res=[('Energy budget for a sheep in one day: energy in food eaten 20,000 kJ; energy in faeces and urine 8,000 kJ; respiration 11,000 kJ; new tissue (growth) 1,000 kJ.',
        [('Show that these data obey the first law of thermodynamics.', '8,000 + 11,000 + 1,000 = 20,000 kJ = input, so energy is conserved.'),
         ('Calculate the efficiency of conversion of food into new tissue and explain why it is low.', '1,000/20,000 × 100 = 5%; most assimilated energy is used in respiration (movement, maintaining body temperature) and lost as heat (second law).')])])


# =============================================================================================
# ch03 1.3 Sustainability
# =============================================================================================
S('ch03-st1', gens=['natural_income'],
  terms=[('sustainability', 'the use and management of resources that allows full natural replacement of the resources exploited and full recovery of the ecosystems affected by their extraction and use'),
         ('natural capital', 'the stock of natural resources and ecosystems, such as forests, soils, fish stocks and aquifers, that yields goods and services'),
         ('natural income', 'the yield (flow of goods and services) obtained from natural capital, e.g. annual timber growth or fish recruitment'),
         ('sustainable yield', 'the rate of increase in natural capital that can be exploited without depleting the original stock or its potential for replenishment'),
         ('ecosystem services', 'the benefits people obtain from ecosystems: provisioning, regulating, supporting and cultural services'),
         ('strong sustainability', 'the view that natural capital cannot be replaced by human-made capital and must be maintained')],
  facts=[('Which of the following is a regulating ecosystem service?', 'Mangroves reducing storm-surge damage', ['Timber from a forest', 'Fish caught from a reef', 'Tourism in a national park'], 'Regulating services include climate, flood and pollination regulation; timber and fish are provisioning; tourism is cultural.'),
         ('Which statement best describes the sustainable use of a forest?', 'Harvesting no more than its annual growth so the stock is maintained', ['Clear-felling and replanting with a different species', 'Harvesting the oldest trees as fast as possible', 'Banning all use of the forest'], 'Living off the natural income maintains natural capital.'),
         ('Which pillars are usually included in sustainable development?', 'Environmental, social and economic', ['Political, military and economic', 'Scientific, religious and economic', 'Urban, rural and coastal'], 'The three pillars (Brundtland, 1987; often shown as overlapping circles).'),
         ('The 2021 Dasgupta Review on the economics of biodiversity found that between 1992 and 2014 global natural capital per person:', 'Fell by almost 40%', ['Doubled', 'Stayed constant', 'Rose by 13%'], 'Produced capital per person doubled over the same period.')],
  why=[('Explain why natural capital is not always valued in economic decisions.', 'Many ecosystem services (climate regulation, pollination) are public goods with no market price, so they are treated as free externalities; GDP counts depletion of natural capital as income.'),
       ('Explain how the concept of natural income can be used to manage a fishery sustainably.', 'The fish stock is natural capital; recruitment and growth each year are natural income; setting catches at or below the sustainable yield (e.g. MSY or lower) maintains the stock.'),
       ('Explain why sustainability requires consideration of social and economic as well as environmental factors.', 'Policies that ignore livelihoods, equity or costs fail politically or push activities elsewhere; long-term environmental health depends on people being able to meet needs and having incentives to conserve.')],
  contrast=[('natural capital', 'natural income', 'Natural capital is the stock (e.g. a forest); natural income is the flow it yields each year (e.g. annual timber growth). Living off income keeps capital intact; consuming capital is unsustainable.'),
            ('strong sustainability', 'weak sustainability', 'Strong sustainability holds that critical natural capital cannot be substituted and must be conserved; weak sustainability allows natural capital to be replaced by human-made capital as long as total capital is maintained.')],
  misc=[('Renewable resources are always used sustainably.', 'Renewable resources can be over-exploited beyond their regeneration rate (e.g. Grand Banks cod, tropical timber, groundwater), becoming depleted.'),
        ('Sustainability means not using natural resources at all.', 'Sustainability allows use, provided harvests do not exceed natural income and ecosystems can fully recover.')],
  apply=[('Classify each ecosystem service as provisioning, regulating, supporting or cultural: pollination of crops; nutrient cycling; freshwater supply; spiritual value of a sacred grove.', 'Pollination: regulating; nutrient cycling: supporting; freshwater: provisioning; sacred grove: cultural.', 4),
         ('Suggest two indicators that could show whether a forest is managed sustainably.', 'Standing stock / area of forest stable or increasing over time; harvest ≤ annual increment; biodiversity indicators stable; soil quality maintained; certification (FSC).', 2)],
  cases=[('the collapse of the Grand Banks cod fishery, Newfoundland', 'catches peaked at about 800,000 t in 1968; the stock collapsed by over 95% and a moratorium in 1992 put about 35,000 people out of work', 'the consequences of consuming natural capital rather than natural income', 'catches far above sustainable yield depleted the stock itself, removing the income on which the industry depended; recovery has been very slow'),
         ('Costa Rica\'s payments for ecosystem services (PSA, since 1997)', 'landowners are paid to protect forest, funded partly by a fuel tax; forest cover rose from about 21% in the 1980s to over 50% by 2020', 'valuing natural capital', 'paying for regulating services (carbon, water, biodiversity, scenery) gives landowners an incentive to conserve natural capital')],
  evaluate=[('Putting a monetary value on ecosystem services is the best way to protect natural capital.', ['makes hidden values visible in decisions (Costanza 1997 ~US$33 trillion/yr)', 'enables payment schemes (Costa Rica PSA)'], ['some values (intrinsic, spiritual) cannot be priced', 'risks commodifying nature; valuations are uncertain', 'markets may still trade nature away if a higher price is offered'], 'Valuation is a useful tool for decision-making, but should complement legal protection and recognition of intrinsic value.'),
            ('Weak sustainability is an acceptable goal for modern economies.', ['technology substitutes some resources', 'economic development reduces poverty'], ['critical natural capital (climate, biodiversity) cannot be substituted', 'planetary boundaries are already exceeded'], 'Weak sustainability is risky because some natural capital is irreplaceable; strong sustainability is needed for critical systems.')],
  extended=[('Discuss whether the concept of natural capital helps or hinders conservation. [9]', 'Helps: makes values visible (Dasgupta Review, natural capital accounting in UK/China GEP), supports PES; hinders: anthropocentric framing, commodification, valuation uncertainty, ignores intrinsic value. Judgement.', 9, 'long')],
  res=[('Data: global per capita stocks of capital, 1992 → 2014 (Dasgupta Review, 2021): produced capital approximately doubled; human capital rose by about 13%; natural capital fell by nearly 40%.',
        [('Describe the changes shown and suggest what they imply about sustainability.', 'Produced and human capital increased while natural capital declined sharply; growth has been achieved by drawing down natural capital, which is unsustainable (weak sustainability at best).'),
         ('Suggest two reasons for the decline in natural capital per person.', 'Population growth (more people sharing the stock); deforestation, soil degradation, overfishing and biodiversity loss.')])])

S('ch03-st2', gens=['footprint'],
  terms=[('ecological footprint (EF)', 'the area of land and water required to sustainably provide all the resources at the rate at which they are being consumed by a given population and to absorb its wastes, measured in global hectares'),
         ('biocapacity', 'the capacity of a given biologically productive area to generate a supply of renewable resources and to absorb its wastes'),
         ('global hectare (gha)', 'a hectare with world-average biological productivity, used as the unit of ecological footprints and biocapacity'),
         ('ecological overshoot', 'the situation in which humanity\'s ecological footprint exceeds Earth\'s biocapacity'),
         ('Earth Overshoot Day', 'the date in a year when humanity\'s demand on nature exceeds what Earth can regenerate in that year')],
  facts=[('Which component makes up the largest share of the global ecological footprint?', 'The carbon footprint', ['Built-up land', 'Fishing grounds', 'Grazing land'], 'Carbon accounts for about 60% of humanity\'s footprint.'),
         ('In recent years humanity has used resources at a rate equivalent to about how many Earths?', 'About 1.7', ['About 0.5', 'About 1.0', 'About 4.5'], 'Global Footprint Network estimates ~1.7 Earths; Earth Overshoot Day fell on 1 August in 2024.'),
         ('Which country has one of the largest ecological reserves (biocapacity well above footprint)?', 'Brazil', ['Japan', 'Singapore', 'the United Arab Emirates'], 'Brazil\'s biocapacity (~8 gha/person) far exceeds its footprint (~2.6).'),
         ('Which of the following would REDUCE an individual\'s ecological footprint the most?', 'Replacing beef with plant-based protein and taking fewer flights', ['Recycling more paper', 'Using a reusable shopping bag', 'Switching off phone chargers'], 'Diet and transport dominate personal footprints.')],
  why=[('Explain why the ecological footprint of a high-income country is usually larger than that of a low-income country.', 'Higher income brings greater consumption of meat, energy, goods and travel, and more waste and CO₂ emissions per person, so more land and sea are needed to supply resources and absorb carbon.'),
       ('Explain how a country can have a footprint larger than its biocapacity.', 'It imports resources produced on other countries\' land, emits CO₂ absorbed by the global commons, and may deplete its own natural capital (overfishing, groundwater mining).'),
       ('Explain two limitations of the ecological footprint as a sustainability indicator.', 'It omits some impacts (freshwater use, toxic pollution, biodiversity loss); it assumes current technology and yields; converting carbon to forest area is hypothetical; data for some countries are poor.')],
  contrast=[('ecological footprint', 'biocapacity', 'Ecological footprint measures demand: the productive area needed to supply a population\'s consumption and absorb its waste; biocapacity measures supply: the productive area available. Footprint > biocapacity is an ecological deficit.'),
            ('ecological footprint', 'carbon footprint', 'The ecological footprint is expressed in global hectares and includes cropland, grazing, forest, fishing, built-up land and carbon; a carbon footprint measures only greenhouse-gas emissions, in tonnes of CO₂-equivalent.')],
  misc=[('A country with a small ecological footprint per person must have a small total footprint.', 'Total footprint = per-capita footprint × population; China and India have modest per-capita footprints but large totals.'),
        ('Recycling is the main way to reduce an ecological footprint.', 'Diet, energy use and transport (the carbon component) dominate most footprints; recycling has a smaller effect.')],
  apply=[('Suggest three changes a school could make to reduce its ecological footprint.', 'Install solar panels and improve insulation; serve more plant-based meals and reduce food waste; encourage walking, cycling and buses; reduce paper use and recycle.', 3),
         ('Compare the ecological footprint per person of Qatar (about 14 gha) with India (about 1.2 gha) and suggest reasons for the difference.', 'Qatar\'s is roughly 12 times larger due to high incomes, energy-intensive air conditioning and desalination, cheap fossil fuels, high car use and imports of food; India has lower incomes and consumption.', 3)],
  cases=[('Earth Overshoot Day', 'it moved from late December in 1971 to 1 August by 2024, except for a temporary shift to 22 August in 2020 due to COVID-19 lockdowns', 'global ecological overshoot', 'humanity\'s footprint now exceeds Earth\'s biocapacity by about 70%, so natural capital is being drawn down'),
         ('Singapore', 'a city-state with a footprint of about 5-6 gha per person but biocapacity close to 0.1 gha per person', 'dependence on imported biocapacity', 'almost all food, water and energy are imported, so the city relies on other countries\' land and on trade')],
  evaluate=[('The ecological footprint is the best measure of a country\'s environmental sustainability.', ['single, easily communicated figure', 'compares demand with supply', 'tracks change over time'], ['ignores water, pollution and biodiversity', 'carbon dominates and is hypothetical', 'does not show inequality within a country'], 'It is a useful headline indicator but must be combined with others (water footprint, planetary boundaries, HDI) for a full picture.')],
  extended=[('To what extent can individual lifestyle choices reduce a country\'s ecological footprint? [9]', 'Individual choices: diet, travel, energy, consumption (e.g. plant-based diet can cut food footprint by about half); limits: infrastructure, energy mix, industry and government policy dominate; rebound effects; need for structural change. Judgement.', 9, 'long')],
  res=[('Ecological footprint and biocapacity (gha per person, Global Footprint Network, approximate): USA EF 8.0, BC 3.4; China EF 3.6, BC 0.9; India EF 1.2, BC 0.4; Brazil EF 2.6, BC 8.1; Japan EF 4.4, BC 0.6.',
        [('Identify which country has an ecological reserve and calculate the per-person deficit of the USA.', 'Brazil (8.1 > 2.6); USA deficit = 8.0 − 3.4 = 4.6 gha per person.'),
         ('Calculate how many times greater Japan\'s footprint is than its biocapacity and explain how Japan sustains this.', '4.4 / 0.6 ≈ 7.3 times; Japan imports food, timber and fuel and emits CO₂ absorbed by the global commons.')])])

S('ch03-st3',
  terms=[('planetary boundaries', 'a framework (Rockström et al., 2009) of nine Earth-system processes with thresholds that define a safe operating space for humanity'),
         ('safe operating space', 'the range within the planetary boundaries in which humanity can develop without destabilising Earth\'s systems'),
         ('doughnut economics', 'a model by Kate Raworth (2012, 2017) in which a social foundation (inner ring) and an ecological ceiling (outer ring) define a safe and just space for humanity'),
         ('social foundation', 'the inner ring of the doughnut model: minimum standards for human wellbeing such as food, water, health, education, housing and political voice'),
         ('ecological ceiling', 'the outer ring of the doughnut model, based on the nine planetary boundaries, beyond which environmental degradation threatens human wellbeing')],
  facts=[('According to the 2023 update (Richardson et al.), how many of the nine planetary boundaries had been transgressed?', 'Six', ['Two', 'Four', 'Nine'], 'Climate change, biosphere integrity, land-system change, freshwater change, biogeochemical flows and novel entities.'),
         ('Which planetary boundary is considered to be within the safe operating space and recovering?', 'Stratospheric ozone depletion', ['Biosphere integrity', 'Biogeochemical flows (N and P)', 'Climate change'], 'The Montreal Protocol has allowed ozone to begin recovering.'),
         ('Which city became the first to formally adopt the doughnut economics model in 2020?', 'Amsterdam', ['London', 'Singapore', 'Mumbai'], 'Amsterdam adopted the City Doughnut to guide its post-COVID recovery and circular economy strategy.'),
         ('The planetary boundary for climate change is set at an atmospheric CO₂ concentration of:', '350 ppm', ['280 ppm', '450 ppm', '550 ppm'], 'Current levels exceed 420 ppm.')],
  why=[('Explain why the doughnut model is described as combining environmental and social sustainability.', 'It places a social foundation (meeting basic needs for all) inside an ecological ceiling (planetary boundaries); a sustainable economy must lift everyone above the foundation without overshooting the ceiling.'),
       ('Explain why biogeochemical flows of nitrogen and phosphorus have exceeded their planetary boundary.', 'Industrial fixation of nitrogen (Haber process) and mining of phosphate rock for fertiliser add far more reactive N and P than natural cycles; runoff causes eutrophication and dead zones.'),
       ('Explain one limitation of the planetary boundaries model.', 'Boundaries are global but impacts are local; thresholds are uncertain; some processes (novel entities) are hard to quantify; it does not address who is responsible or social equity.')],
  contrast=[('the planetary boundaries model', 'the doughnut economics model', 'Planetary boundaries define environmental limits only; the doughnut adds a social foundation, so it identifies a space that is both ecologically safe and socially just.')],
  misc=[('If a planetary boundary is crossed, catastrophic collapse happens immediately.', 'Crossing a boundary moves into a zone of increasing risk; the boundary is set before suspected tipping points, so effects may be gradual and uncertain.'),
        ('The doughnut model says economic growth is always bad.', 'It is "agnostic" about growth: the goal is to meet human needs within planetary boundaries, whether or not GDP grows.')],
  apply=[('Suggest two policies a city could adopt to move into the "safe and just space" of the doughnut.', 'e.g. circular-economy procurement and repair hubs (reduce material use); affordable, energy-efficient social housing (meets social foundation while cutting emissions); public transport and cycling investment.', 2),
         ('State three planetary boundaries and identify one that has been transgressed.', 'e.g. climate change (transgressed), ocean acidification, stratospheric ozone depletion, freshwater change, land-system change, biosphere integrity (transgressed), biogeochemical flows, atmospheric aerosol loading, novel entities.', 3)],
  cases=[('Amsterdam\'s City Doughnut (2020)', 'the city used the doughnut model to plan its circular strategy, aiming to halve use of new raw materials by 2030 and be fully circular by 2050', 'applying the doughnut model to policy', 'it translates global social and ecological limits into local targets for housing, materials and emissions'),
         ('the Gulf of Mexico dead zone', 'nitrogen and phosphorus from Mississippi basin farmland create a hypoxic zone averaging about 14,000 km² each summer', 'transgression of the biogeochemical flows boundary', 'excess fertiliser nutrients overload the ocean, causing eutrophication and oxygen loss far from where the fertiliser was applied')],
  evaluate=[('The planetary boundaries framework is a useful guide for global environmental policy.', ['simple, science-based framing', 'covers multiple Earth-system processes, not just climate'], ['global thresholds are uncertain', 'does not allocate responsibility between countries', 'local thresholds may differ'], 'It is a powerful communication and agenda-setting tool, but must be downscaled and combined with equity considerations to guide policy.'),
            ('The doughnut economics model is more useful than GDP for measuring progress.', ['includes social needs and environmental limits', 'shows overshoot and shortfall'], ['harder to measure and compare', 'no single number; data gaps'], 'The doughnut gives a more complete picture of wellbeing and sustainability, though GDP remains useful for measuring economic activity.')],
  extended=[('Evaluate the doughnut economics model as a framework for sustainable development. [9]', 'Strengths: integrates social and ecological limits; adopted by cities (Amsterdam, Copenhagen, Brussels); shifts focus from growth. Limits: political feasibility, measurement, tension between meeting needs and staying under the ceiling in low-income countries (no country currently meets all needs within limits, O\'Neill et al. 2018). Judgement.', 9, 'long')],
  res=[('Data (O\'Neill et al., 2018) for 150 countries: no country met all 11 social thresholds without transgressing at least some biophysical boundaries; Vietnam met 6 social thresholds while transgressing only 1 boundary; the USA met 11 social thresholds but transgressed 7 boundaries.',
        [('Using the data, explain why no country is yet in the "safe and just space".', 'Meeting social needs has so far been associated with high resource use; countries that meet all needs (USA) overshoot several boundaries, while low-impact countries (Vietnam) still fall short of social thresholds.'),
         ('Suggest one way a country like Vietnam could improve its social outcomes without crossing more boundaries.', 'Invest in renewable energy, public health and education (low resource intensity), efficient public transport and sustainable agriculture rather than copying high-consumption development.')])])

S('ch03-st4',
  terms=[('environmental impact assessment (EIA)', 'a report prepared before a development project that assesses its likely environmental, social and economic impacts, considers alternatives and proposes mitigation'),
         ('baseline study', 'a survey of environmental conditions before a development begins, used as a reference against which impacts can be measured'),
         ('Sustainable Development Goals (SDGs)', 'the 17 goals with 169 targets adopted by all UN member states in 2015 as part of the 2030 Agenda for Sustainable Development'),
         ('mitigation measure', 'an action taken to avoid, reduce or compensate for negative impacts of a development'),
         ('strategic environmental assessment', 'an assessment of the environmental effects of policies, plans and programmes rather than individual projects')],
  facts=[('In which year and in which country did EIAs first become a legal requirement?', '1969, the United States (National Environmental Policy Act)', ['1987, Norway', '1992, Brazil', '2015, France'], 'NEPA came into force in 1970.'),
         ('How many Sustainable Development Goals were adopted in 2015?', '17', ['8', '12', '25'], 'They replaced the eight Millennium Development Goals (2000-2015).'),
         ('Which SDG is "Life below water"?', 'SDG 14', ['SDG 6', 'SDG 13', 'SDG 15'], 'SDG 6 is clean water and sanitation; SDG 13 climate action; SDG 15 life on land.'),
         ('Which of the following is a common criticism of EIAs?', 'They may be prepared by consultants paid by the developer and are rarely followed up after approval', ['They are banned in most countries', 'They only consider social impacts', 'They must always stop the project'], 'EIAs inform decisions but do not themselves decide.')],
  why=[('Explain why baseline studies are essential in an EIA.', 'They record the state of habitats, species, water, air and communities before development so impacts can be predicted, monitored and compared; without a baseline, change cannot be measured or attributed.'),
       ('Explain why EIAs do not always prevent environmental damage.', 'Decisions balance economic and political priorities; EIAs may be biased, rushed or ignore cumulative and indirect impacts; mitigation may not be enforced; monitoring after approval is often weak.'),
       ('Explain why the SDGs are described as interdependent.', 'Progress on one goal affects others: e.g. clean energy (SDG 7) supports climate action (SDG 13) and health (SDG 3), but agricultural expansion for zero hunger (SDG 2) may conflict with life on land (SDG 15).')],
  contrast=[('the Millennium Development Goals', 'the Sustainable Development Goals', 'The 8 MDGs (2000-2015) focused mainly on poverty and health in low-income countries; the 17 SDGs (2015-2030) are universal, apply to all countries and integrate environmental, social and economic sustainability.'),
            ('an EIA', 'a strategic environmental assessment', 'An EIA assesses one project (e.g. a dam); a strategic environmental assessment assesses a whole policy, plan or programme (e.g. a national energy plan), so it can address cumulative impacts earlier.')],
  misc=[('An EIA decides whether a project goes ahead.', 'An EIA informs decision-makers; the final decision is political and may approve a project despite negative findings.'),
        ('The SDGs only apply to low-income countries.', 'The SDGs are universal and apply to all UN member states, including high-income countries (e.g. SDG 12 responsible consumption).')],
  apply=[('Outline four stages of an EIA for a proposed wind farm.', 'Screening (is an EIA needed?), scoping (key impacts: birds and bats, noise, landscape), baseline study (bird surveys, noise levels), impact prediction and evaluation, mitigation (siting away from flight paths, curtailment), public consultation, decision and monitoring.', 4),
         ('Identify two SDGs most relevant to a project to restore mangroves and explain one link for each.', 'SDG 14 (nursery habitat for fish), SDG 13 (blue-carbon storage and storm protection), SDG 1/8 (livelihoods from fisheries and ecotourism).', 4)],
  cases=[('the Belo Monte Dam, Brazil', 'the 11.2 GW dam on the Xingu River was approved in 2011 despite an EIA identifying displacement of about 20,000 people and impacts on Indigenous communities', 'the limitations of EIAs', 'the EIA documented impacts but political and economic priorities overrode them, and mitigation measures were criticised as inadequate'),
         ('the Three Gorges Dam EIA, China', 'a 1991 environmental assessment predicted sedimentation and biodiversity impacts; after completion, landslides around the reservoir, downstream erosion and declining Yangtze fisheries were reported', 'the difficulty of predicting impacts', 'some impacts were underestimated or cumulative, showing the need for monitoring after construction')],
  evaluate=[('EIAs are an effective tool for achieving sustainable development.', ['identify impacts and alternatives before construction', 'involve public consultation', 'lead to mitigation'], ['often biased towards developers', 'cannot stop projects', 'weak follow-up monitoring', 'cumulative impacts ignored'], 'EIAs improve decisions but their effectiveness depends on independence, enforcement of mitigation and post-project monitoring.'),
            ('The SDGs are too broad to be achievable by 2030.', ['17 goals and 169 targets are hard to track', 'the 2023 UN report found only about 15% of targets on track'], ['they provide a shared framework and data', 'progress on extreme poverty and electricity access before COVID-19'], 'Full achievement by 2030 is unlikely, but the SDGs remain valuable for guiding priorities and accountability.')],
  extended=[('Evaluate the role of environmental impact assessments in protecting ecosystems from large infrastructure projects, with reference to named examples. [9]', 'Belo Monte, Three Gorges, HS2 (UK), Hinkley Point C fish deterrents; strengths (baseline, alternatives, consultation) and weaknesses (bias, political override, cumulative impacts); judgement.', 9, 'long')],
  res=[('Extract from an EIA for a coastal resort in Bali: baseline - 3.2 ha of seagrass, nesting by green turtles on 1.5 km of beach, local fishers using the bay; predicted impacts - dredging removes 40% of seagrass, beach lighting disturbs nesting; proposed mitigation - relocate dredging, turtle-friendly lighting, a 200 m no-build setback.',
        [('Calculate the area of seagrass that would be lost and suggest one further mitigation measure.', '40% × 3.2 ha = 1.28 ha; e.g. seagrass transplantation, silt curtains during construction, seasonal timing of works outside nesting season.'),
         ('Explain why consultation with local fishers should be part of this EIA.', 'They depend on the bay for livelihoods, have local knowledge of fish and seagrass, and may suffer economic impacts; consultation improves fairness and the quality of predictions.')])])


# =============================================================================================
# ch04 2.1 Individuals, populations, communities and ecosystems
# =============================================================================================
S('ch04-st1',
  terms=[('species', 'a group of organisms sharing common characteristics that interbreed and produce fertile offspring'),
         ('population', 'a group of organisms of the same species living in the same area at the same time and capable of interbreeding'),
         ('habitat', 'the location in which a community, species, population or organism lives'),
         ('niche', 'the particular set of abiotic and biotic conditions and resources to which an organism or population responds; its role in the ecosystem'),
         ('fundamental niche', 'the full range of conditions and resources in which a species could survive and reproduce'),
         ('realized niche', 'the actual conditions and resources in which a species exists, due to biotic interactions such as competition'),
         ('community', 'a group of populations of different species living and interacting with each other in a common habitat')],
  facts=[('Connell\'s experiments with Chthamalus and Semibalanus barnacles on a Scottish shore showed that:', 'competition restricts Chthamalus to a realized niche higher on the shore', ['Chthamalus cannot survive low on the shore at all', 'both species occupy their full fundamental niche', 'predation by dog whelks has no effect'], 'When Semibalanus was removed, Chthamalus survived lower down - its fundamental niche is wider.'),
         ('Why are horses and donkeys considered different species?', 'Their offspring (mules) are infertile', ['They look different', 'They live in different habitats', 'They eat different food'], 'The biological species concept requires fertile offspring.'),
         ('Which term describes all the organisms and their abiotic environment interacting in an area?', 'Ecosystem', ['Community', 'Population', 'Habitat'], 'A community is only the living populations.'),
         ('Which is the best description of a species\' niche?', 'Its role and the full set of conditions and resources it uses', ['Its location only', 'The number of individuals', 'The food chain it belongs to'], 'Niche includes habitat, diet, activity time and interactions.')],
  why=[('Explain why the realized niche of a species is usually smaller than its fundamental niche.', 'Biotic interactions such as competition, predation and disease prevent a species from occupying all the conditions it could tolerate, so it occupies only part of its fundamental niche.'),
       ('Explain why the biological species concept is difficult to apply in some cases.', 'It cannot be applied to asexual organisms or fossils; some distinct species hybridise and produce fertile offspring (e.g. some plants, ducks); populations separated geographically cannot be tested for interbreeding.'),
       ('Explain why two species cannot occupy exactly the same niche in the same habitat for long.', 'Competitive exclusion (Gause\'s principle): the better competitor will out-compete the other for the limiting resource, causing local extinction, displacement or niche differentiation.')],
  contrast=[('habitat', 'niche', 'Habitat is where an organism lives (its address); niche is its role and the full range of conditions and resources it uses, including when and what it eats and its interactions (its profession).'),
            ('fundamental niche', 'realized niche', 'The fundamental niche is the full range a species could occupy in the absence of competitors; the realized niche is the part it actually occupies because of biotic interactions.'),
            ('a population', 'a community', 'A population is one species in an area; a community is all the populations of different species interacting in that area.')],
  misc=[('Two species with the same habitat must have the same niche.', 'Species can share a habitat but differ in diet, feeding height or time of activity (e.g. MacArthur\'s warblers feeding in different parts of spruce trees), so their niches differ.'),
        ('A community includes the soil and climate.', 'A community is only the living organisms; with the abiotic environment it forms an ecosystem.')],
  apply=[('Five species of warbler feed in the same spruce trees in Maine (MacArthur, 1958). Explain how they can coexist.', 'Resource partitioning: each species feeds mainly in a different zone of the tree (top, outer branches, inner branches, base) and at slightly different times, so their realized niches differ and competition is reduced.', 3),
         ('Suggest how the niche of a red fox differs between a rural and an urban habitat.', 'Rural: hunts rabbits and voles, dens in woodland, active at dusk; urban: scavenges food waste, dens under buildings, nocturnal to avoid people - same species, different realized niche.', 3)],
  cases=[('Connell\'s barnacles on the Isle of Cumbrae, Scotland (1961)', 'Chthamalus stellatus occupied the upper shore and Semibalanus balanoides the lower shore; removing Semibalanus allowed Chthamalus to live lower down', 'fundamental and realized niches', 'competition from Semibalanus restricts Chthamalus to a realized niche narrower than its fundamental niche, while desiccation limits Semibalanus higher up'),
         ('red and grey squirrels in the UK', 'grey squirrels introduced from North America in the 1870s out-compete native red squirrels for food and carry squirrelpox', 'competitive exclusion', 'the greys exploit acorns more efficiently and transmit disease, so reds have been excluded from most of England')],
  evaluate=[('The niche concept is more useful than the habitat concept for understanding species distributions.', ['includes biotic interactions and resources', 'explains coexistence and competitive exclusion'], ['niches are multidimensional and hard to measure', 'habitat data are easier to collect for conservation'], 'The niche concept gives deeper explanation, while habitat is more practical for mapping and management; both are needed.')],
  extended=[('With reference to named examples, explain how competition can determine the niche of a species. [7]', 'Connell\'s barnacles, Gause\'s Paramecium, red vs grey squirrels, MacArthur\'s warblers; fundamental vs realized niche; competitive exclusion; resource partitioning.', 7, 'explain')],
  res=[('Experiment (Gause, 1934): Paramecium aurelia and P. caudatum each grew to a stable population when cultured alone; when grown together, P. aurelia persisted and P. caudatum died out within about 16 days.',
        [('State the principle illustrated by these results and explain it.', 'Competitive exclusion: two species competing for the same limiting resource cannot coexist; P. aurelia used the bacterial food more efficiently and out-competed P. caudatum.'),
         ('Suggest how the two species might have coexisted in a more complex natural habitat.', 'Resource partitioning (different microhabitats or depths), spatial refuges, or fluctuating conditions that sometimes favour each species.')])])

S('ch04-st2', gens=['growth'],
  terms=[('carrying capacity', 'the maximum number of individuals of a species that can be sustainably supported by a given area'),
         ('limiting factor', 'a factor that limits the growth, abundance or distribution of a population, e.g. food, water, light, nutrients or temperature'),
         ('abiotic factor', 'a non-living, physical factor that may influence an organism or ecosystem, e.g. temperature, light, pH, salinity, precipitation'),
         ('biotic factor', 'a living, biological factor that may influence an organism or ecosystem, e.g. predation, competition, disease'),
         ('J-curve', 'a population growth curve showing exponential growth followed by a sudden crash, when resources are not limiting initially'),
         ('S-curve (sigmoid)', 'a population growth curve showing exponential growth followed by a transitional phase and a plateau at carrying capacity'),
         ('density-dependent factor', 'a limiting factor whose effect increases with population density, e.g. disease, competition or predation')],
  facts=[('Which phase of the S-curve shows the fastest population growth?', 'The exponential (log) phase', ['The lag phase', 'The plateau phase', 'The decline phase'], 'Resources are plentiful and environmental resistance is low.'),
         ('The reindeer population on St Matthew Island, Alaska, grew from 29 in 1944 to about 6,000 in 1963 and then crashed to 42. This is an example of:', 'a J-curve with overshoot and crash', ['an S-curve at carrying capacity', 'logistic growth with no overshoot', 'a stable predator-prey cycle'], 'With no predators, the herd overgrazed lichen and starved in the 1963-64 winter.'),
         ('Which of these is a density-independent limiting factor?', 'A severe frost', ['Competition for food', 'Disease spread', 'Predation'], 'Weather events affect populations regardless of density.'),
         ('Shelford\'s law of tolerance states that:', 'each species has a range of tolerance to an abiotic factor with an optimum and limits beyond which it cannot survive', ['all species tolerate the same range', 'population growth is always exponential', 'carrying capacity never changes'], 'Abundance is greatest near the optimum.')],
  why=[('Explain why populations show an S-shaped growth curve in a stable environment.', 'Initially few individuals (lag); then plentiful resources allow exponential growth; as density rises, limiting factors (food, space, disease) increase environmental resistance; birth and death rates equalise at carrying capacity (negative feedback).'),
       ('Explain why a J-curve population often crashes below its original carrying capacity.', 'Rapid growth overshoots carrying capacity, and overgrazing or resource depletion damages the environment, so the carrying capacity itself falls; the population crashes to a low level (St Matthew Island reindeer).'),
       ('Explain how density-dependent factors regulate population size.', 'As density rises, competition, disease transmission and predation increase, raising death rates and reducing birth rates; as density falls they decrease - a negative feedback that stabilises numbers.'),
       ('Explain why carrying capacity is difficult to estimate for a population.', 'It changes with weather, seasons, resource levels, technology (for humans), and interactions with other species; populations rarely sit at an exact equilibrium.')],
  contrast=[('a J-curve', 'an S-curve', 'A J-curve shows exponential growth without limiting factors, followed by a sudden crash; an S-curve shows exponential growth slowing as limiting factors increase, levelling off at carrying capacity.'),
            ('density-dependent factors', 'density-independent factors', 'Density-dependent factors (disease, competition, predation) have a greater effect at higher population density and regulate populations; density-independent factors (floods, fire, frost) act regardless of density.'),
            ('abiotic factors', 'biotic factors', 'Abiotic factors are non-living (temperature, light, pH, salinity); biotic factors are living (predators, competitors, parasites, food organisms).')],
  misc=[('A population at carrying capacity has stopped reproducing.', 'Births still occur, but they are balanced by deaths (and migration), so numbers fluctuate around K.'),
        ('Carrying capacity is a fixed number for each species.', 'K varies with the environment and over time, e.g. it falls during drought or after overgrazing.')],
  apply=[('A population of yeast in a flask shows an S-curve and then declines. Suggest two reasons for the decline.', 'Glucose (food) is used up; toxic ethanol accumulates and kills cells.', 2),
         ('Suggest how the introduction of a predator would change the S-curve of a deer population.', 'Carrying capacity / equilibrium level would fall and fluctuations may develop (predator-prey oscillations), e.g. wolves reintroduced to Yellowstone (1995) reduced elk numbers.', 3)],
  cases=[('reindeer on St Matthew Island, Alaska', '29 reindeer introduced in 1944 grew to about 6,000 by 1963 with no predators, then crashed to 42 after overgrazing lichen and a severe winter', 'J-curve growth and overshoot', 'without limiting factors the population grew exponentially beyond carrying capacity, destroyed its food supply and crashed'),
         ('wolves reintroduced to Yellowstone National Park (1995)', '31 wolves were released in 1995-96; elk numbers fell from about 19,000 in the mid-1990s to about 4,000-6,000 by the 2010s', 'the role of biotic limiting factors', 'predation, and the "landscape of fear", reduced elk density and grazing pressure, allowing willow and aspen to recover along rivers'),
         ('the Kaibab Plateau deer, Arizona', 'predator removal in the early 1900s was followed by a reported rise in mule deer to about 100,000 and a crash by the 1930s', 'carrying capacity and the risks of removing predators', 'removing a density-dependent control allowed overshoot and overgrazing; the classic account is debated, showing uncertainty in population data')],
  evaluate=[('Carrying capacity is a useful concept for managing wildlife populations.', ['guides culling and hunting quotas', 'explains overshoot and crashes'], ['K fluctuates and is hard to measure', 'ignores predator-prey dynamics and human influences'], 'Carrying capacity is a valuable guide when treated as a variable, monitored estimate rather than a fixed number.')],
  extended=[('Explain how limiting factors produce the different phases of an S-shaped population curve. [7]', 'Lag phase (few breeding individuals, acclimatisation); exponential phase (abundant resources, low resistance); transitional phase (limiting factors increase, density-dependent); plateau at K (births = deaths, negative feedback); examples.', 7, 'explain')],
  res=[('Data: wolves and elk in Yellowstone National Park (approximate winter counts) - 1995: wolves 21, elk 17,000; 2003: wolves 174, elk 9,000; 2012: wolves 83, elk 4,000; 2020: wolves 123, elk 6,000.',
        [('Calculate the percentage decrease in elk between 1995 and 2012.', '(17,000 − 4,000)/17,000 × 100 ≈ 76%.'),
         ('Suggest two reasons, other than wolf predation, that could explain the change in elk numbers.', 'Hunting outside the park; drought and severe winters; competition with bison; predation by bears and cougars; elk migrating out of the counted area.')])])

S('ch04-st3',
  terms=[('predation', 'an interaction in which one animal (the predator) kills and eats another (the prey)'),
         ('herbivory', 'an interaction in which an animal eats a plant or alga, often without killing it'),
         ('interspecific competition', 'competition between individuals of different species for the same limited resource'),
         ('intraspecific competition', 'competition between individuals of the same species for the same limited resource'),
         ('parasitism', 'a relationship in which one organism (the parasite) lives in or on another (the host), benefiting at the host\'s expense'),
         ('mutualism', 'a relationship in which two or more species benefit')],
  facts=[('Which relationship exists between reef-building corals and zooxanthellae?', 'Mutualism', ['Parasitism', 'Predation', 'Competition'], 'The algae photosynthesise and provide sugars; the coral provides shelter and nutrients (CO₂, nitrogen).'),
         ('The varroa mite feeding on honeybee colonies is an example of:', 'parasitism', ['mutualism', 'herbivory', 'commensalism'], 'The mite weakens bees and spreads viruses.'),
         ('Why do predator population peaks usually lag behind prey peaks?', 'Predators need time to reproduce after food becomes abundant', ['Predators are always less numerous', 'Prey reproduce more slowly', 'Predators migrate'], 'Numerical response of predators is delayed.'),
         ('Rhizobium bacteria in the root nodules of legumes are an example of:', 'mutualism', ['parasitism', 'predation', 'interspecific competition'], 'Bacteria fix nitrogen for the plant and receive carbohydrates.')],
  why=[('Explain how predator-prey interactions regulate population sizes.', 'More prey → more food for predators → predator numbers rise → prey numbers fall due to predation → predators starve and decline → prey recover; a negative feedback producing oscillations.'),
       ('Explain why coral bleaching shows the importance of mutualism.', 'High sea temperatures cause corals to expel zooxanthellae; without the algae\'s sugars the coral loses most of its energy supply and may starve and die if conditions persist, so both partners depend on each other.'),
       ('Explain why intraspecific competition is a density-dependent factor.', 'At higher densities more individuals compete for the same food, mates or territories, so per-capita birth rates fall and death rates rise in proportion to density.')],
  contrast=[('parasitism', 'predation', 'A predator kills and eats its prey, usually quickly; a parasite lives in or on its host over a long period, harming but usually not immediately killing it.'),
            ('interspecific competition', 'intraspecific competition', 'Interspecific competition is between different species (e.g. red and grey squirrels); intraspecific competition is within one species (e.g. barnacles competing for rock space).'),
            ('mutualism', 'parasitism', 'In mutualism both species benefit (lichen fungus and alga); in parasitism one benefits and the other is harmed (tapeworm and host).')],
  misc=[('Predators always reduce prey populations to extinction.', 'Predator numbers fall when prey are scarce, allowing prey to recover; most predator-prey systems oscillate rather than going extinct.'),
        ('Herbivory always kills the plant.', 'Most herbivores eat parts of plants (grazing, browsing), and many plants regrow; herbivory differs from predation in this way.')],
  apply=[('Classify each interaction: (i) mycorrhizal fungi and tree roots, (ii) cuckoo chicks raised by reed warblers, (iii) lions and hyenas competing for a carcass, (iv) cleaner wrasse removing parasites from groupers.', '(i) mutualism (ii) brood parasitism (iii) interspecific competition (iv) mutualism.', 4),
         ('Suggest one way a parasite can affect a whole ecosystem.', 'e.g. chytrid fungus has caused declines or extinctions of over 500 amphibian species, removing predators of insects and prey for snakes; or Dutch elm disease removed elms from European landscapes.', 2)],
  cases=[('snowshoe hare and Canada lynx', 'Hudson\'s Bay Company pelt records (1845-1935) show about 10-year cycles, with lynx peaks a year or two after hare peaks', 'predator-prey interactions', 'lynx numbers track hare availability, and hare numbers are reduced by predation (and food shortage), producing linked oscillations'),
         ('chytrid fungus (Batrachochytrium dendrobatidis)', 'the fungal disease has contributed to declines of over 500 frog species and about 90 extinctions, e.g. the golden toad of Monteverde', 'the impact of parasitism and disease on populations', 'the pathogen damages amphibian skin, disrupting water and salt balance and killing hosts with no evolved resistance'),
         ('the Great Barrier Reef bleaching events (2016, 2017, 2020, 2022, 2024)', 'marine heatwaves caused mass coral bleaching; in 2016 about 30% of shallow-water corals died on the reef', 'the breakdown of mutualism', 'warm water causes corals to expel zooxanthellae, removing their main energy source and causing mortality')],
  evaluate=[('Biotic interactions are more important than abiotic factors in determining species distribution.', ['competition shapes realized niches (Connell)', 'predators and disease limit populations'], ['abiotic factors set fundamental tolerance limits (temperature, salinity)', 'climate determines biome distribution'], 'Abiotic factors set the broad limits of distribution while biotic interactions determine the realized niche within them.')],
  extended=[('Discuss the importance of mutualistic relationships for the stability of ecosystems. [9]', 'Corals and zooxanthellae, mycorrhizae (80-90% of plants), pollinators (about 75% of crop types benefit), Rhizobium, cleaner fish; loss of mutualists (bleaching, pollinator decline) destabilises ecosystems; other factors matter too. Judgement.', 9, 'long')],
  res=[('Data from a lab study: number of Didinium (predator) and Paramecium (prey) per cm³ over 10 days - day 0: prey 30, predator 3; day 2: 70, 6; day 4: 90, 25; day 6: 20, 40; day 8: 2, 10; day 10: 0, 0.',
        [('Describe the changes in both populations and explain why both died out.', 'Prey rose to 90 then crashed; predators rose with a lag to 40 then crashed; in a simple flask with no refuges, predators ate all the prey and then starved.'),
         ('Suggest how adding a refuge (e.g. sediment) would change the result.', 'Some prey could hide, avoiding complete predation, so prey recovers after predators decline and the populations may oscillate rather than becoming extinct (Gause\'s experiments).')])])

S('ch04-st4', gens=['lincoln', 'simpson'],
  terms=[('quadrat', 'a square frame of known area used to sample sessile or slow-moving organisms and estimate density, frequency or percentage cover'),
         ('transect', 'a line along which samples are taken at regular intervals to show changes in species distribution along an environmental gradient'),
         ('Lincoln index', 'a capture-mark-release-recapture estimate of population size: N = (M × C) / R'),
         ('species richness', 'the number of different species present in an area'),
         ('species evenness', 'how similar the relative abundances of the species in a community are'),
         ('Simpson\'s reciprocal index', 'a measure of biodiversity calculated as D = N(N − 1) / Σn(n − 1), which increases with both richness and evenness'),
         ('random sampling', 'a sampling method in which every point in the area has an equal chance of being sampled, e.g. using random-number coordinates')],
  facts=[('Which method is most suitable for estimating the population of a mobile animal such as a beetle?', 'Capture-mark-release-recapture', ['Percentage-cover quadrats', 'A belt transect of plants', 'Counting from a single photograph'], 'Mobile animals cannot be counted reliably in quadrats.'),
         ('Which sampling strategy should be used to study how vegetation changes from a beach to inland dunes?', 'A systematic transect', ['Random quadrats', 'A single large quadrat', 'Mark-recapture'], 'Transects sample along an environmental gradient.'),
         ('A community with 5 species in equal numbers compared with 5 species where one dominates will have:', 'a higher Simpson\'s index', ['a lower Simpson\'s index', 'the same index', 'a lower species richness'], 'Same richness but higher evenness gives a higher index.'),
         ('How is the minimum number of quadrats for a survey commonly determined?', 'By plotting a species-area or running-mean curve and finding where it levels off', ['By using exactly two quadrats', 'By choosing the number of species', 'By dividing the area by 10'], 'Additional quadrats beyond the plateau add little new information.')],
  why=[('Explain why random sampling is used when estimating plant density in a uniform field.', 'It avoids observer bias in choosing sites, so the sample is representative, and allows statistical analysis of the mean and variability.'),
       ('Explain why Simpson\'s index is a better measure of biodiversity than species richness alone.', 'It accounts for evenness as well as richness; two communities with the same number of species can differ greatly if one species dominates, which richness alone would miss.'),
       ('Explain two limitations of using percentage cover to estimate plant abundance.', 'It is subjective (estimates vary between observers); overlapping layers can total over 100%; small or seasonal plants may be missed; it does not count individuals.')],
  contrast=[('species richness', 'species evenness', 'Richness is the number of species present; evenness is how equal their relative abundances are. Diversity indices combine both.'),
            ('random sampling', 'systematic sampling', 'Random sampling places quadrats at random coordinates to avoid bias in uniform areas; systematic sampling places them at regular intervals (e.g. along a transect) to study change along a gradient.')],
  misc=[('A high Simpson\'s index in one sample proves the whole ecosystem is healthy.', 'An index is only an estimate from a sample and must be compared over time or between sites; it does not identify which species are present (invasive species can raise richness).'),
        ('The Lincoln index works well for any species.', 'It assumes marks are not lost, marking does not affect survival, a closed population and random mixing; it is unsuitable for very large, very mobile or territorial populations.')],
  apply=[('Describe how you would measure the percentage cover of heather in a moorland area.', 'Lay out a grid, generate random coordinates, place 1 m² quadrats (10 × 10 subdivided) at each point, count squares more than half covered by heather to estimate percentage cover, repeat for enough quadrats (species-area curve) and calculate the mean.', 4),
         ('Outline one ethical consideration when using pitfall traps to sample invertebrates.', 'Traps must be checked frequently (e.g. every 12-24 h) and include drainage holes and a cover so animals do not drown, overheat or eat each other; release animals where caught.', 2)],
  cases=[('a Simpson\'s index comparison of logged and unlogged forest in Danum Valley, Borneo', 'dung-beetle surveys found lower species richness and dominance by a few disturbance-tolerant species in logged plots', 'using diversity indices to assess disturbance', 'lower richness and evenness in logged areas give a lower index, indicating that logging simplifies the community')],
  evaluate=[('Mark-release-recapture gives reliable estimates of animal population size.', ['simple, cheap, widely used', 'estimates improve with repeated samples'], ['assumptions often violated (mark loss, trap-happy or trap-shy animals, migration)', 'small recapture numbers give large error'], 'It gives useful estimates when assumptions are checked and samples are large, but should be treated as approximate.')],
  extended=[('Design an investigation to compare the biodiversity of two areas of a school grounds, including how you would ensure reliability. [7]', 'Research question; random sampling in each area with stratification if needed; quadrat size and number (species-area curve); identify species with keys; calculate Simpson\'s index; repeat and calculate mean/SD; control variables (time, season, observer); statistical test (t-test).', 7, 'explain')],
  res=[('Pitfall-trap data from two areas (number of individuals): Mown lawn - beetle sp. A 22, woodlouse 4, spider 2; Wildflower meadow - beetle sp. A 8, beetle sp. B 7, woodlouse 6, spider 5, centipede 4.',
        [('Calculate Simpson\'s reciprocal index for the mown lawn using D = N(N−1)/Σn(n−1).', 'N = 28; Σn(n−1) = 22×21 + 4×3 + 2×1 = 462 + 12 + 2 = 476; D = 28×27/476 = 756/476 ≈ 1.59.'),
         ('Compare the richness of the two areas and suggest why they differ.', 'The meadow has 5 species, the lawn 3; the meadow offers more varied food, shelter and microhabitats, while mowing removes cover and flowers.')])])


# =============================================================================================
# ch05 2.2 Energy and biomass in ecosystems
# =============================================================================================
S('ch05-st1', gens=['trophic'],
  terms=[('trophic level', 'the position an organism occupies in a food chain, or a group of organisms in a community that occupy the same position in food chains'),
         ('producer (autotroph)', 'an organism that makes its own food from inorganic substances, usually by photosynthesis'),
         ('food web', 'a network of interconnected food chains showing the feeding relationships in a community'),
         ('pyramid of energy', 'a diagram showing the flow of energy through each trophic level per unit area per unit time (e.g. kJ m⁻² yr⁻¹); it is never inverted'),
         ('pyramid of biomass', 'a diagram showing the standing stock of dry mass of organisms at each trophic level at one time (e.g. g m⁻²)'),
         ('pyramid of numbers', 'a diagram showing the number of organisms at each trophic level at one time'),
         ('decomposer', 'an organism (bacterium or fungus) that breaks down dead organic matter, releasing nutrients')],
  facts=[('Why can a pyramid of numbers be inverted?', 'One large producer (e.g. an oak tree) can support many small herbivores', ['Energy increases at higher levels', 'Biomass is created by consumers', 'Producers are always small'], 'Numbers ignore organism size.'),
         ('Which pyramid can be inverted in some aquatic ecosystems at certain times of year?', 'Pyramid of biomass', ['Pyramid of energy', 'Pyramid of productivity', 'None can'], 'Phytoplankton have small standing crop but very high turnover, so zooplankton biomass can exceed it.'),
         ('On average, about what percentage of energy is passed from one trophic level to the next?', 'About 10%', ['About 50%', 'About 1%', 'About 90%'], 'Values range roughly 5-20%; 10% is a common approximation.'),
         ('Which units are appropriate for a pyramid of energy?', 'kJ m⁻² yr⁻¹', ['g m⁻²', 'number per m²', 'kg'], 'Energy pyramids show flow per area per time.')],
  why=[('Explain why pyramids of energy are never inverted.', 'They show energy flow over time; by the second law of thermodynamics energy is lost as heat at each transfer, so each level receives less energy than the level below.'),
       ('Explain why top carnivores are often rare and vulnerable.', 'Only a small fraction of energy reaches the top of food chains, so populations are small; they need large ranges, reproduce slowly, accumulate toxins (biomagnification) and are often persecuted.'),
       ('Explain how the removal of a keystone species can affect a food web.', 'Keystone species have a disproportionate effect on community structure; e.g. hunting sea otters allowed sea urchins to increase and destroy kelp forests, removing habitat for many species.'),
       ('Explain why food webs are more realistic than food chains.', 'Most organisms eat and are eaten by several species and may feed at more than one trophic level; webs show these interconnections and help predict knock-on effects.')],
  contrast=[('a pyramid of biomass', 'a pyramid of energy', 'A pyramid of biomass shows standing stock (g m⁻²) at one time and can be inverted; a pyramid of energy shows productivity over time (kJ m⁻² yr⁻¹) and is never inverted.'),
            ('a food chain', 'a food web', 'A food chain is a single linear sequence of feeding; a food web is many interconnected chains showing that organisms have several food sources and predators.')],
  misc=[('Energy is recycled within ecosystems by decomposers.', 'Matter (nutrients) is recycled; energy flows through and is lost as heat.'),
        ('A pyramid of numbers always has more producers than herbivores.', 'Pyramids of numbers can be inverted, e.g. one oak tree supporting thousands of caterpillars.')],
  apply=[('In a kelp forest, sea otters eat sea urchins, which eat kelp. Predict and explain the effect of removing sea otters.', 'Urchin numbers rise without predation, they overgraze kelp, forming "urchin barrens"; fish and invertebrates that depend on kelp decline - a trophic cascade.', 3),
         ('Explain why a field of wheat fed to people can support more people than the same field used to raise beef cattle.', 'Eating producers directly avoids an extra trophic transfer where ~90% of energy is lost; beef needs several kg of feed per kg of meat.', 3)],
  cases=[('sea otters and kelp forests in the Aleutian Islands', 'when orcas began eating otters in the 1990s, otter numbers fell by about 90%, urchins increased and kelp density declined sharply', 'top-down control in food webs (trophic cascade)', 'removing the top predator released the herbivores from predation, which overgrazed the producers'),
         ('Silver Springs, Florida (H.T. Odum, 1957)', 'energy flow was measured at each trophic level: GPP of producers about 20,810, herbivores about 3,368, carnivores about 383 and top carnivores about 21 kcal m⁻² yr⁻¹', 'energy flow and pyramids of energy', 'energy declined at each level, giving an upright pyramid and showing large respiratory losses'),
         ('Lake Victoria and the Nile perch', 'the introduction of Nile perch in the 1950s contributed to the extinction of about 200 species of endemic cichlid fish', 'the effect of adding a top predator to a food web', 'a new predator restructured the food web, removing many herbivorous and detritivorous cichlids')],
  evaluate=[('Ecological pyramids are useful models of ecosystems.', ['show energy loss and trophic structure simply', 'allow comparison between ecosystems'], ['omnivores and decomposers are hard to place', 'pyramids of numbers and biomass can be inverted and misleading', 'collecting energy data is difficult and destructive'], 'Pyramids, especially of energy, are useful simplifications, but food webs and energy-flow diagrams give a fuller picture.')],
  extended=[('Explain, using named examples, how energy flow limits the length of food chains and the size of top predator populations. [7]', 'Second law, ~10% transfer, losses in respiration/egestion/uneaten; Silver Springs data; tigers need about 50 km² or more per individual; implications for conservation.', 7, 'explain')],
  res=[('Energy flow at Silver Springs, Florida (kcal m⁻² yr⁻¹, Odum 1957): producers GPP 20,810; herbivores 3,368; carnivores 383; top carnivores 21.',
        [('Calculate the efficiency of energy transfer from herbivores to carnivores.', '383 / 3,368 × 100 ≈ 11.4%.'),
         ('Calculate the percentage of the producers\' energy that reaches top carnivores and explain why it is so small.', '21 / 20,810 × 100 ≈ 0.10%; at each transfer energy is lost as heat in respiration and in uneaten or egested material.')])])

S('ch05-st2',
  terms=[('photosynthesis', 'the process by which producers use light energy to convert carbon dioxide and water into glucose and oxygen: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂'),
         ('cellular respiration', 'the process by which organic compounds are broken down to release energy for life processes: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + energy'),
         ('chemosynthesis', 'the production of organic compounds using energy from oxidising inorganic chemicals rather than light, e.g. by bacteria at hydrothermal vents'),
         ('autotroph', 'an organism that synthesises its own organic molecules from inorganic sources (photosynthesis or chemosynthesis)'),
         ('heterotroph', 'an organism that obtains energy and organic molecules by consuming other organisms or organic matter')],
  facts=[('In terms of energy, photosynthesis converts:', 'light energy into chemical energy', ['chemical energy into heat', 'heat into light', 'kinetic energy into chemical energy'], 'Glucose stores chemical energy.'),
         ('What are the main outputs of aerobic respiration?', 'Carbon dioxide, water and energy (ATP and heat)', ['Glucose and oxygen', 'Oxygen and water', 'Nitrogen and heat'], 'Respiration reverses photosynthesis.'),
         ('Which organisms form the base of food webs at deep-sea hydrothermal vents?', 'Chemosynthetic bacteria', ['Phytoplankton', 'Kelp', 'Seagrass'], 'They oxidise hydrogen sulfide to fix carbon without light.'),
         ('Which wavelengths of light are mainly absorbed by chlorophyll?', 'Red and blue', ['Green', 'Infrared only', 'Ultraviolet only'], 'Green is reflected, giving plants their colour.')],
  why=[('Explain why photosynthesis and respiration are described as complementary processes.', 'The products of one are the raw materials of the other (CO₂ and water ↔ glucose and oxygen); together they cycle carbon and oxygen between the atmosphere and organisms.'),
       ('Explain why respiration is described as a transformation in terms of energy.', 'Chemical energy in glucose is transformed into usable energy (ATP) for work and into heat, which is lost from the organism and eventually the ecosystem.'),
       ('Explain how the rate of photosynthesis is affected by light intensity, CO₂ and temperature.', 'Each can be limiting: rate rises with light and CO₂ until another factor limits; enzymes work faster as temperature rises to an optimum, then denature.')],
  contrast=[('photosynthesis', 'respiration', 'Photosynthesis occurs in producers in light, absorbs CO₂, releases O₂ and stores chemical energy; respiration occurs in all organisms continuously, uses O₂, releases CO₂ and releases energy (much as heat).'),
            ('photosynthesis', 'chemosynthesis', 'Photosynthesis uses light energy to fix carbon; chemosynthesis uses energy from oxidising inorganic chemicals (e.g. H₂S at vents), so it can occur in darkness.')],
  misc=[('Plants photosynthesise but do not respire.', 'Plants respire all the time, day and night; in light, photosynthesis usually exceeds respiration.'),
        ('Respiration creates energy.', 'Energy cannot be created (first law); respiration transforms chemical energy into ATP and heat.')],
  apply=[('A sealed bottle of pond water with an aquatic plant shows rising dissolved oxygen in daylight and falling oxygen at night. Explain these changes.', 'In daylight photosynthesis rate > respiration rate, so net O₂ is released; at night only respiration occurs, consuming O₂.', 3),
         ('Outline the inputs, outputs and transformations of photosynthesis as a system.', 'Inputs: light energy, CO₂, water; transformation: light to chemical energy, inorganic to organic carbon; outputs: glucose (stored chemical energy), O₂, heat.', 3)],
  cases=[('hydrothermal vent communities on the East Pacific Rise', 'giant tube worms (Riftia) host chemosynthetic bacteria that oxidise hydrogen sulfide to fix carbon in total darkness', 'energy entering ecosystems without sunlight', 'chemosynthesis replaces photosynthesis as the energy source, supporting dense communities 2,500 m deep'),
         ('the Mauna Loa CO₂ record', 'atmospheric CO₂ shows a seasonal cycle of about 6 ppm, falling in the northern summer and rising in winter', 'the global balance of photosynthesis and respiration', 'in the northern summer photosynthesis by the large land area of northern forests exceeds respiration, drawing down CO₂; in winter respiration dominates')],
  evaluate=[('Photosynthesis is the most important process in the biosphere.', ['captures almost all energy entering ecosystems', 'produces oxygen and removes CO₂', 'supports food production'], ['respiration and decomposition are equally essential for cycling', 'chemosynthesis supports some ecosystems'], 'Photosynthesis is fundamental, but ecosystems depend on its balance with respiration and decomposition.')],
  extended=[('Explain how photosynthesis and respiration link the carbon cycle and energy flow in an ecosystem. [7]', 'Photosynthesis transforms light to chemical energy and fixes carbon; respiration releases energy as heat and CO₂; carbon is recycled while energy flows; NPP = GPP − R; seasonal CO₂ cycle.', 7, 'explain')],
  res=[('Experiment: an aquatic plant (Elodea) was placed at different distances from a lamp and bubbles of gas counted per minute: 10 cm 42; 20 cm 24; 30 cm 12; 40 cm 6; 50 cm 5.',
        [('Describe the relationship shown and explain it.', 'Bubble rate falls as distance increases (light intensity falls with distance); light is the limiting factor for photosynthesis at greater distances.'),
         ('Suggest two variables that should be controlled and one limitation of counting bubbles.', 'Temperature (heat from lamp - use a heat shield), CO₂ concentration (add sodium hydrogencarbonate), same plant; bubbles vary in size and some O₂ dissolves - measure volume with a gas syringe.')])])

S('ch05-st3', gens=['productivity'],
  terms=[('gross primary productivity (GPP)', 'the total gain in energy or biomass per unit area per unit time fixed by photosynthesis in green plants'),
         ('net primary productivity (NPP)', 'the gain by producers in energy or biomass per unit area per unit time remaining after allowing for respiratory losses: NPP = GPP − R'),
         ('gross secondary productivity (GSP)', 'the total energy or biomass assimilated by consumers: GSP = food eaten − faecal loss'),
         ('net secondary productivity (NSP)', 'the gain by consumers in energy or biomass per unit area per unit time remaining after allowing for respiratory losses: NSP = GSP − R'),
         ('productivity', 'the rate of production of biomass or energy per unit area per unit time, e.g. g m⁻² yr⁻¹ or kJ m⁻² yr⁻¹'),
         ('biomass', 'the mass of organic material in organisms or ecosystems, usually per unit area, measured as dry mass')],
  facts=[('Which ecosystem has the highest NPP per unit area?', 'Tropical rainforest (or estuaries and swamps)', ['Open ocean', 'Tundra', 'Desert'], 'Rainforest NPP is about 2,200 g m⁻² yr⁻¹; open ocean about 125.'),
         ('Why does the open ocean contribute a large share of global NPP despite low productivity per m²?', 'It covers a very large area (about 65% of Earth\'s surface)', ['It has the highest NPP per m²', 'It contains most land plants', 'It has no respiration'], 'Low productivity × huge area = large total.'),
         ('Why is dry mass rather than fresh mass used to measure biomass?', 'Water content varies and contains no energy', ['Dry mass is heavier', 'Fresh mass cannot be measured', 'Water has high energy content'], 'Drying gives a consistent measure of organic matter.'),
         ('The formula for net secondary productivity is:', 'NSP = GSP − R', ['NSP = GPP − R', 'NSP = food eaten + faeces', 'NSP = NPP × 10%'], 'GSP = food eaten − faecal loss.')],
  why=[('Explain why tropical rainforests have high NPP while deserts have low NPP.', 'Rainforests have high, constant temperatures, high rainfall and high light all year, so photosynthesis is fast and continuous; deserts are limited by water (and sometimes extreme temperature), so plant cover and photosynthesis are low.'),
       ('Explain why NSP is a small fraction of the food eaten by an animal.', 'Much food is egested as faeces (not assimilated), and most of what is assimilated is respired to power movement and maintain body temperature, lost as heat; only the remainder becomes new tissue.'),
       ('Explain why endotherms have lower NSP efficiency than ectotherms.', 'Endotherms (birds, mammals) use much more assimilated energy in respiration to maintain a constant body temperature, so less is available for growth and reproduction.')],
  contrast=[('gross primary productivity', 'net primary productivity', 'GPP is the total energy fixed by photosynthesis; NPP is what remains after plant respiration (NPP = GPP − R) and is the energy available to consumers.'),
            ('productivity', 'biomass', 'Productivity is a rate (g m⁻² yr⁻¹); biomass is a standing stock at one time (g m⁻²). A system can have high biomass but low productivity, e.g. an old-growth forest.')],
  misc=[('An old-growth forest has the highest net productivity because it has the most biomass.', 'Mature forests have high biomass but high respiration, so net productivity is lower than in younger, rapidly growing stages.'),
        ('GSP is the total amount of food an animal eats.', 'GSP is food eaten minus faecal losses (the amount assimilated).')],
  apply=[('Describe how the GPP of an aquatic plant could be estimated using light and dark bottles.', 'Measure initial dissolved O₂; incubate one clear bottle (photosynthesis + respiration → net production) and one dark bottle (respiration only); GPP = (light − initial) + (initial − dark) = light − dark.', 4),
         ('Describe how to measure the NPP of a grassland.', 'Harvest the vegetation from quadrats at the start and end of a period, dry samples at 60-80 °C to constant mass, and calculate the increase in dry mass per m² per year; repeat with several quadrats.', 3)],
  cases=[('the Amazon rainforest vs the Sahara Desert', 'tropical rainforest NPP is about 2,200 g m⁻² yr⁻¹ compared with less than 90 g m⁻² yr⁻¹ in hot deserts', 'climatic control of primary productivity', 'productivity is limited by water in deserts but not in rainforests where warmth, light and rainfall are all high'),
         ('the Peruvian upwelling', 'cold, nutrient-rich water rising off Peru supports some of the world\'s highest marine productivity and the anchoveta fishery (up to about 10 million t a year)', 'nutrient limitation of marine productivity', 'upwelling brings nitrates and phosphates to the sunlit surface, removing the nutrient limitation found in most of the open ocean')],
  evaluate=[('NPP is the most useful measure of the value of an ecosystem.', ['shows energy available to consumers and humans', 'indicates carbon uptake'], ['ignores biodiversity and cultural value', 'high-NPP crops can be low in biodiversity', 'stock (biomass) matters for carbon storage'], 'NPP is a valuable ecological measure but must be combined with biodiversity, stock and ecosystem-service measures.')],
  extended=[('Explain how GPP, NPP, GSP and NSP are related in an ecosystem and how each could be measured. [7]', 'Definitions and equations; NPP harvest method; light/dark bottle; GSP = eaten − faeces (feeding experiments); NSP = GSP − R; losses as heat; units.', 7, 'explain')],
  res=[('Mean NPP (g m⁻² yr⁻¹) and area (million km²): tropical rainforest 2,200 and 17.0; temperate forest 1,250 and 12.0; savanna 900 and 15.0; tundra 140 and 8.0; open ocean 125 and 332.0.',
        [('Calculate the total annual NPP of the open ocean and of tropical rainforest (in 10¹⁵ g, i.e. Pg).', 'Ocean: 125 × 332 × 10¹² m² = 41.5 × 10¹⁵ g ≈ 41.5 Pg; rainforest: 2,200 × 17 × 10¹² = 37.4 Pg.'),
         ('Explain why the open ocean has such low NPP per m².', 'Nutrients (N, P, Fe) sink below the sunlit zone and are scarce at the surface; light is limited below about 200 m.')])])

S('ch05-st4', gens=['biomag'],
  terms=[('bioaccumulation', 'the build-up of a persistent or non-biodegradable pollutant within an organism or trophic level because it cannot be broken down'),
         ('biomagnification', 'the increase in concentration of a persistent or non-biodegradable pollutant along a food chain'),
         ('persistent organic pollutant (POP)', 'a toxic organic chemical that resists breakdown, accumulates in fatty tissue and travels long distances, e.g. DDT and PCBs'),
         ('Stockholm Convention', 'the 2001 international treaty to eliminate or restrict the production and use of persistent organic pollutants')],
  facts=[('Which property makes a pollutant likely to biomagnify?', 'It is persistent and fat-soluble', ['It is water-soluble and quickly excreted', 'It is biodegradable', 'It is a gas at room temperature'], 'Fat-soluble, persistent chemicals are stored in tissues.'),
         ('DDT caused the decline of which group of birds in the 1950s-1970s?', 'Birds of prey such as peregrine falcons, ospreys and bald eagles', ['Seed-eating finches', 'Penguins', 'Hummingbirds'], 'DDE interfered with calcium deposition, thinning eggshells.'),
         ('In the Minamata Bay disaster, which pollutant biomagnified in fish?', 'Methylmercury', ['Cadmium', 'Lead', 'Nitrate'], 'Chisso Corporation discharged mercury compounds.'),
         ('Why is DDT still used in some countries?', 'Indoor residual spraying to control malaria-carrying mosquitoes is permitted under the Stockholm Convention', ['It is no longer toxic', 'It breaks down quickly', 'It is used as a fertiliser'], 'The WHO supports limited indoor use for malaria control.')],
  why=[('Explain why biomagnification affects top predators most.', 'Each consumer eats many prey, and the persistent pollutant is stored rather than excreted, so the dose increases at each trophic level; top predators also live long and accumulate over their lifetime.'),
       ('Explain why polar bears and Inuit communities have high PCB levels despite being far from industry.', 'POPs evaporate in warm regions, travel by air and ocean currents and condense in cold polar regions (global distillation); they then biomagnify through long Arctic marine food chains rich in fat.'),
       ('Explain why plastics can act as a pathway for biomagnification.', 'Microplastics adsorb POPs from seawater and are eaten by plankton and fish, transferring toxins into food chains, where they can accumulate in higher consumers.')],
  contrast=[('bioaccumulation', 'biomagnification', 'Bioaccumulation is the build-up of a pollutant within one organism over its lifetime; biomagnification is the increase in concentration from one trophic level to the next.'),
            ('a persistent pollutant', 'a biodegradable pollutant', 'A persistent pollutant (DDT, PCBs, mercury) resists breakdown and can accumulate and biomagnify; a biodegradable pollutant (sewage, food waste) is broken down by decomposers.')],
  misc=[('Biomagnification happens because predators are bigger than their prey.', 'It happens because pollutants are persistent and stored in tissues, and predators eat many prey, not simply because of size.'),
        ('Banning DDT immediately removed it from ecosystems.', 'DDT and its breakdown products persist for decades in soils and sediments; residues are still found in wildlife.')],
  apply=[('Suggest why killer whales in the North-East Atlantic are particularly at risk from PCBs.', 'They are top predators eating seals and large fish, live up to 90 years, and pass PCBs to calves through fat-rich milk; some populations have very high blubber PCB levels and reproductive failure.', 3),
         ('Outline two ways to reduce the impact of persistent pollutants on food chains.', 'Ban production (Stockholm Convention; US DDT ban 1972); replace with biodegradable alternatives or integrated pest management; clean up contaminated sediments; fish consumption advisories.', 2)],
  cases=[('DDT in Long Island Sound, USA (Woodwell, 1967)', 'DDT residues rose from about 0.00005 ppm in water to about 0.04 ppm in zooplankton, 2 ppm in needlefish and about 25 ppm in ospreys', 'biomagnification', 'the concentration increased about 500,000-fold from water to top predators because DDT is fat-soluble and persistent'),
         ('the recovery of the peregrine falcon in the UK and USA', 'peregrines declined sharply in the 1950s-60s due to eggshell thinning from DDT and dieldrin; numbers recovered after bans in the 1970s-80s', 'the effectiveness of banning persistent pollutants', 'removing the source allowed residues to decline and breeding success to recover over decades'),
         ('Minamata Bay, Japan', 'methylmercury discharged by the Chisso factory accumulated in fish and shellfish eaten by local people, causing over 2,000 officially recognised cases of Minamata disease', 'biomagnification affecting humans', 'humans eating top-level fish received high doses of mercury that had concentrated along the food chain')],
  evaluate=[('International bans are the most effective way to prevent harm from persistent pollutants.', ['Stockholm Convention covers 30+ chemicals; peregrines recovered after DDT bans'], ['legacy pollutants persist for decades', 'new chemicals (PFAS) emerge faster than bans', 'trade-offs (DDT for malaria)'], 'Bans are essential, but must be combined with clean-up, monitoring and testing of new chemicals before release.')],
  extended=[('Explain, with reference to a named pollutant, how bioaccumulation and biomagnification can affect top predators and humans. [7]', 'DDT/methylmercury/PCBs: persistence, fat solubility, uptake, concentration at each level (Long Island data), effects (eggshell thinning, neurological damage, reproductive failure), human exposure via fish.', 7, 'explain')],
  res=[('Concentrations of PCBs (mg/kg lipid) in an Arctic food chain: seawater < 0.000001; zooplankton 0.04; Arctic cod 0.3; ringed seal 1.5; polar bear 20.',
        [('Calculate the magnification factor between ringed seals and polar bears.', '20 / 1.5 ≈ 13 times.'),
         ('Explain why these values are so high in a region with little industry.', 'POPs are carried to the Arctic by winds and ocean currents (global distillation), persist in the cold and biomagnify through fat-rich Arctic food chains.')])])


# =============================================================================================
# ch06 2.3 Biogeochemical cycles
# =============================================================================================
S('ch06-st1', gens=['carbon_budget'],
  terms=[('carbon sink', 'a pathway or storage that removes carbon from the atmosphere at a greater rate than it releases it, e.g. a growing forest or the ocean'),
         ('carbon source', 'a pathway or storage that releases more carbon to the atmosphere than it absorbs, e.g. burning fossil fuels or a degraded peatland'),
         ('carbon store', 'a reservoir that holds carbon, such as the atmosphere, oceans, biomass, soils, fossil fuels or limestone'),
         ('carbon flux', 'the rate of transfer of carbon between stores, e.g. GtC per year'),
         ('residence time', 'the average time a carbon atom remains in a store, calculated as store size ÷ flux in or out'),
         ('carbon sequestration', 'the process of capturing and storing atmospheric carbon dioxide, naturally (photosynthesis) or artificially (carbon capture and storage)')],
  facts=[('Which is the largest store of carbon on Earth?', 'Sedimentary rocks (limestone and other carbonates)', ['The atmosphere', 'Living biomass', 'Fossil fuels'], 'Rocks hold tens of millions of GtC; the deep ocean holds about 37,000 GtC; the atmosphere about 875 GtC.'),
         ('Approximately what was the atmospheric CO₂ concentration before the Industrial Revolution?', '280 ppm', ['180 ppm', '350 ppm', '420 ppm'], 'Ice cores show about 280 ppm around 1750; it exceeded 420 ppm in 2023.'),
         ('Which process transfers carbon from the atmosphere to biomass?', 'Photosynthesis', ['Combustion', 'Respiration', 'Decomposition'], 'Producers fix CO₂ into glucose.'),
         ('Roughly what fraction of human CO₂ emissions is absorbed by the oceans each year?', 'About a quarter', ['About 5%', 'About three-quarters', 'All of it'], 'The ocean takes up about 25-26%; land about 30%; the rest stays in the atmosphere.')],
  why=[('Explain why peatlands are important carbon stores.', 'Waterlogged, acidic, anaerobic conditions slow decomposition, so dead plant material accumulates over thousands of years; peatlands cover about 3% of land but store about 600 GtC, roughly twice the carbon of all the world\'s forest biomass.'),
       ('Explain how human activities have altered the carbon cycle.', 'Burning fossil fuels transfers carbon from long-term lithosphere stores to the atmosphere; deforestation and land-use change reduce biomass stores and sinks; cement production releases CO₂; the result is rising atmospheric CO₂ and ocean acidification.'),
       ('Explain why a mature forest may be carbon-neutral whereas a young forest is a carbon sink.', 'In a young forest photosynthesis (GPP) greatly exceeds respiration, so biomass accumulates; in a mature forest GPP is roughly balanced by respiration of plants and decomposers, so net uptake is small.')],
  contrast=[('a carbon store', 'a carbon sink', 'A store is any reservoir holding carbon (a quantity); a sink is a store that is gaining carbon because it absorbs more than it releases (a net flow into it).'),
            ('the fast carbon cycle', 'the slow carbon cycle', 'The fast cycle involves exchanges among the atmosphere, biosphere, soils and surface ocean over years to centuries; the slow cycle involves rocks, sediments and fossil fuels over millions of years.')],
  misc=[('The oceans will continue to absorb a fixed share of CO₂ emissions regardless of warming.', 'Warmer water holds less CO₂, stratification reduces mixing, and acidification reduces buffering, so the ocean sink may weaken.'),
        ('Planting trees can easily offset all fossil-fuel emissions.', 'Global emissions (~10 GtC/yr) far exceed realistic afforestation capacity; forests can burn or be cleared, and land is needed for food.')],
  apply=[('Identify two transformations and two transfers in the carbon cycle.', 'Transformations: photosynthesis (CO₂ to glucose), respiration, combustion, fossilisation, calcification; transfers: diffusion of CO₂ into ocean, feeding (consumption), runoff of dissolved carbon, sedimentation.', 4),
         ('Suggest how the draining of Indonesian peat swamps for oil-palm plantations affects the carbon cycle.', 'Drained peat is exposed to oxygen and decomposes, and is vulnerable to fire (the 1997 and 2015 fires released hundreds of Mt C), turning a long-term store into a source.', 3)],
  cases=[('the 2015 Indonesian peat fires', 'fires on drained peatland released an estimated 0.3-0.4 GtC (over 1 Gt CO₂e) and caused haze across South-East Asia', 'human conversion of a carbon store into a source', 'drainage for plantations dried the peat, so it burned and decomposed, releasing carbon stored for thousands of years'),
         ('the Global Carbon Budget (Global Carbon Project)', 'annual fossil CO₂ emissions reached about 10 GtC in the early 2020s, with about half absorbed by ocean and land sinks', 'measuring stores and fluxes', 'the budget balances sources against sinks and the observed atmospheric increase, revealing how much the natural sinks are buffering emissions')],
  evaluate=[('Protecting existing carbon stores is more important than creating new carbon sinks.', ['old-growth forests and peat store carbon accumulated over centuries that cannot be quickly replaced', 'avoids emissions immediately', 'protects biodiversity'], ['new sinks (afforestation, mangrove restoration) add uptake', 'both are needed for net zero'], 'Protecting existing stores is the priority because losses are rapid and recovery takes centuries, but new sinks are also needed.')],
  extended=[('Explain how the carbon cycle links the atmosphere, hydrosphere, biosphere and lithosphere, including the effects of human activities. [7]', 'Stores and fluxes: photosynthesis/respiration, ocean dissolution and the biological pump, sedimentation and fossilisation, volcanic outgassing, weathering; human combustion and deforestation; quantities.', 7, 'explain')],
  res=[('Carbon stores (GtC, approximate, IPCC AR6): atmosphere 875; vegetation 450; soils (including permafrost) 3,200; surface ocean 900; intermediate and deep ocean 37,100; fossil fuel reserves 930.',
        [('Calculate the percentage of the combined atmosphere, vegetation, soil and ocean carbon that is in the deep ocean.', 'Total = 875 + 450 + 3,200 + 900 + 37,100 = 42,525 GtC; deep ocean 37,100 / 42,525 × 100 ≈ 87%.'),
         ('Suggest why the burning of the fossil-fuel reserves would have a large effect on the atmosphere even though it is small compared with the deep ocean.', 'Burning 930 GtC would roughly double the atmospheric store; transfer to the deep ocean is very slow (centuries to millennia), so much remains in the atmosphere for a long time.')])])

S('ch06-st2',
  terms=[('nitrogen fixation', 'the conversion of atmospheric nitrogen (N₂) into ammonia or ammonium compounds by bacteria (e.g. Rhizobium, Azotobacter), lightning or the Haber process'),
         ('nitrification', 'the conversion of ammonium ions into nitrites and then nitrates by nitrifying bacteria (Nitrosomonas, Nitrobacter) in aerobic soils'),
         ('denitrification', 'the conversion of nitrates into nitrogen gas by denitrifying bacteria in anaerobic conditions, such as waterlogged soils'),
         ('ammonification', 'the decomposition of organic nitrogen (proteins, urea) into ammonium by decomposers'),
         ('assimilation', 'the uptake of nitrates or ammonium by plants and their incorporation into proteins and nucleic acids'),
         ('Haber-Bosch process', 'the industrial fixation of nitrogen and hydrogen into ammonia at high temperature and pressure, used to make fertiliser')],
  facts=[('Which bacteria live in the root nodules of legumes and fix nitrogen?', 'Rhizobium', ['Nitrosomonas', 'Nitrobacter', 'Pseudomonas'], 'Nitrosomonas and Nitrobacter are nitrifiers; Pseudomonas includes denitrifiers.'),
         ('Under which conditions does denitrification mainly occur?', 'Anaerobic, waterlogged soils', ['Well-aerated sandy soils', 'Very dry deserts', 'The upper atmosphere'], 'Denitrifiers use nitrate instead of oxygen.'),
         ('Approximately what share of the nitrogen in human bodies is estimated to have come from the Haber-Bosch process?', 'About half', ['Almost none', 'About 10%', 'All of it'], 'Synthetic fertiliser supports about half the world\'s food production.'),
         ('Which form of nitrogen do most plants absorb from the soil?', 'Nitrate ions (and ammonium)', ['Nitrogen gas', 'Nitrous oxide', 'Proteins'], 'Plants cannot use N₂ directly.')],
  why=[('Explain why farmers grow legumes such as clover or beans in crop rotations.', 'Legumes host Rhizobium that fix atmospheric nitrogen into ammonium, enriching soil nitrogen when residues decompose, so less synthetic fertiliser is needed for the following crop.'),
       ('Explain why waterlogged soils are often low in nitrate.', 'Lack of oxygen inhibits nitrifying bacteria and favours denitrifying bacteria, which convert nitrate to N₂ gas, which is lost to the atmosphere.'),
       ('Explain how human activities have altered the nitrogen cycle.', 'The Haber-Bosch process and cultivation of legumes now fix more nitrogen than all natural terrestrial processes; fertiliser runoff causes eutrophication, burning fuels releases NOx (acid rain, smog), and nitrous oxide from fertilised soils is a greenhouse gas.')],
  contrast=[('nitrification', 'denitrification', 'Nitrification is the aerobic conversion of ammonium to nitrite and nitrate by nitrifying bacteria, increasing soil nitrate; denitrification is the anaerobic conversion of nitrate to N₂ gas, removing nitrogen from the soil.'),
            ('nitrogen fixation', 'nitrification', 'Fixation converts unreactive N₂ gas into ammonia/ammonium (Rhizobium, lightning, Haber process); nitrification converts ammonium into nitrate.')],
  misc=[('Plants can absorb nitrogen gas directly from the air.', 'Plants cannot use N₂; it must first be fixed into ammonium or nitrate by bacteria, lightning or industry.'),
        ('Denitrifying bacteria are always harmful.', 'They return N₂ to the atmosphere, completing the cycle, and are used in wastewater treatment and constructed wetlands to remove nitrate.')],
  apply=[('Describe the route by which nitrogen in a dead leaf becomes available to a growing plant.', 'Decomposers break down proteins to ammonium (ammonification); Nitrosomonas oxidises ammonium to nitrite; Nitrobacter oxidises nitrite to nitrate; plant roots absorb nitrate (assimilation).', 4),
         ('Suggest why ploughing and draining a wetland could increase nitrate in nearby rivers.', 'Aeration increases decomposition and nitrification, and removal of the anaerobic wetland removes denitrification, so more nitrate is produced and leached.', 3)],
  cases=[('the Haber-Bosch process', 'industrial fixation produces about 150 million tonnes of ammonia a year and uses about 1-2% of global energy', 'human alteration of the nitrogen cycle', 'synthetic fixation now roughly doubles the natural rate of terrestrial nitrogen fixation, feeding billions but causing nutrient pollution'),
         ('the Baltic Sea dead zones', 'nitrogen and phosphorus from farmland and sewage in nine countries have created hypoxic areas of up to about 70,000 km²', 'the consequences of excess reactive nitrogen', 'surplus nitrates leach into rivers and the sea, fuelling algal blooms whose decomposition removes oxygen')],
  evaluate=[('The benefits of synthetic nitrogen fertiliser outweigh its environmental costs.', ['supports food for about half the world\'s population', 'raised yields during the Green Revolution'], ['eutrophication and dead zones', 'nitrous oxide emissions (~300 times as potent as CO₂)', 'energy-intensive, fossil-fuel based'], 'Fertiliser is indispensable for food security, but costs can be reduced through precision application, legumes and recycling of nutrients.')],
  extended=[('Explain the role of bacteria in the nitrogen cycle. [7]', 'Fixation (Rhizobium, Azotobacter, cyanobacteria), ammonification (decomposers), nitrification (Nitrosomonas, Nitrobacter), denitrification (Pseudomonas); conditions (aerobic/anaerobic); link to plant uptake.', 7, 'explain')],
  res=[('Experiment: soil nitrate (mg/kg) was measured in plots after one growing season - wheat after wheat 12; wheat after clover 28; wheat after clover, waterlogged plot 9.',
        [('Calculate the percentage increase in soil nitrate in the clover rotation compared with continuous wheat, and explain the result.', '(28 − 12)/12 × 100 ≈ 133%; clover root nodules contain Rhizobium that fixed N₂, adding organic nitrogen that was converted to nitrate.'),
         ('Explain why the waterlogged plot had the lowest nitrate.', 'Anaerobic conditions favoured denitrifying bacteria, converting nitrate to N₂ gas, and inhibited nitrification.')])])

S('ch06-st3', gens=['ph'],
  terms=[('ocean acidification', 'the decrease in the pH of the oceans caused by the absorption of atmospheric carbon dioxide'),
         ('biological pump', 'the transfer of carbon from the surface ocean to the deep ocean through photosynthesis by phytoplankton and the sinking of dead organisms and faecal pellets'),
         ('solubility pump', 'the transfer of CO₂ into the deep ocean as cold, dense water at high latitudes dissolves CO₂ and sinks'),
         ('calcification', 'the formation of calcium carbonate shells or skeletons by marine organisms such as corals, molluscs and coccolithophores'),
         ('blue carbon', 'carbon captured and stored by coastal and marine ecosystems such as mangroves, salt marshes and seagrass meadows')],
  facts=[('By about how much has surface ocean pH fallen since the pre-industrial period?', 'About 0.1 units (from about 8.2 to 8.1)', ['About 1 unit', 'About 2 units', 'It has risen by 0.1'], 'A 0.1 fall is about a 26% increase in hydrogen-ion concentration.'),
         ('Which organisms are most directly threatened by ocean acidification?', 'Calcifying organisms such as pteropods, oysters and corals', ['Jellyfish', 'Seagrass', 'Sharks'], 'Lower carbonate saturation hinders shell formation.'),
         ('Which coastal ecosystems store carbon at up to several times the rate per hectare of tropical forests?', 'Mangroves, salt marshes and seagrass meadows', ['Coral reefs', 'Sandy beaches', 'Rocky shores'], 'Blue-carbon ecosystems bury carbon in waterlogged sediments.'),
         ('Which equation shows the first step of ocean acidification?', 'CO₂ + H₂O → H₂CO₃', ['CaCO₃ → CaO + CO₂', '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂', 'N₂ + 3H₂ → 2NH₃'], 'Carbonic acid then dissociates releasing H⁺.')],
  why=[('Explain why the ocean is an important carbon sink.', 'CO₂ dissolves in surface water (solubility pump), and phytoplankton fix carbon that sinks to the deep ocean (biological pump); the ocean has absorbed about a quarter of human CO₂ emissions.'),
       ('Explain how ocean acidification could affect marine food webs.', 'Pteropods and other calcifying plankton at the base of food webs form weaker shells; declines could affect fish such as salmon that feed on them; reef degradation removes habitat for about a quarter of marine species.'),
       ('Explain why mangrove loss is a significant source of carbon emissions.', 'Mangroves store large amounts of carbon in waterlogged sediments; clearing for shrimp farms exposes sediments to oxygen, releasing stored carbon, and removes future sequestration.')],
  contrast=[('the biological pump', 'the solubility pump', 'The biological pump moves carbon to depth through photosynthesis and sinking organic matter; the solubility pump moves dissolved CO₂ to depth as cold, dense, CO₂-rich water sinks at high latitudes.')],
  misc=[('Ocean acidification means the oceans will become acidic (pH below 7).', 'Seawater remains alkaline (pH about 8.1); "acidification" refers to a fall in pH towards acidity.'),
        ('Because the ocean absorbs CO₂, emissions have no effect on marine life.', 'Absorption lowers pH and carbonate availability, harming calcifying organisms and food webs.')],
  apply=[('Suggest why oyster hatcheries in Oregon and Washington, USA, suffered larval die-offs from 2007.', 'Upwelling brought cold, CO₂-rich, low-pH water to the coast; larvae could not build shells; hatcheries now monitor and buffer seawater.', 3),
         ('Suggest two ways blue-carbon ecosystems could be used in climate mitigation.', 'Protect and restore mangroves, seagrass and salt marshes; fund them through carbon credits; include them in national climate plans (NDCs).', 2)],
  cases=[('oyster hatcheries in the US Pacific Northwest', 'from 2007 hatcheries such as Whiskey Creek in Oregon lost up to 70-80% of larvae when corrosive, low-pH upwelled water entered the hatchery', 'the effects of ocean acidification on calcifiers', 'low carbonate saturation prevented larval oysters from forming shells'),
         ('mangrove restoration in the Sundarbans and Mikoko Pamoja, Kenya', 'Mikoko Pamoja sells carbon credits from protecting and replanting mangroves in Gazi Bay', 'blue carbon as a carbon sink', 'carbon finance rewards communities for protecting mangroves that sequester carbon and protect coasts')],
  evaluate=[('Ocean acidification is a greater long-term threat to marine ecosystems than ocean warming.', ['affects calcifiers at the base of food webs', 'irreversible on human timescales'], ['warming already causes mass coral bleaching', 'deoxygenation and warming shift species ranges now'], 'Warming causes more immediate damage, but acidification compounds it, and the two together are the greatest threat.')],
  extended=[('Discuss the importance of the oceans as carbon sinks and the consequences of their changing chemistry. [9]', 'Solubility and biological pumps; ~25% of emissions absorbed; acidification (0.1 pH fall, 26% H⁺ rise); impacts on calcifiers, reefs and fisheries; weakening sink with warming; blue carbon; judgement.', 9, 'long')],
  res=[('Data from the Hawaii Ocean Time-series (Station ALOHA): 1990 - atmospheric CO₂ 354 ppm, seawater pH 8.11; 2020 - atmospheric CO₂ 413 ppm, seawater pH 8.06.',
        [('Calculate the percentage increase in atmospheric CO₂ and the change in pH over this period.', 'CO₂: (413 − 354)/354 × 100 ≈ 16.7%; pH fell by 0.05 units.'),
         ('Calculate the percentage increase in hydrogen-ion concentration and explain the link with CO₂.', '10^0.05 ≈ 1.12, so about 12% increase; more atmospheric CO₂ dissolves, forming carbonic acid which releases H⁺.')])])


# =============================================================================================
# ch07 2.4 Climate and biomes; 2.5 Zonation, succession and change
# =============================================================================================
S('ch07-st1', gens=['climograph'],
  terms=[('biome', 'a collection of ecosystems sharing similar climatic conditions, grouped by dominant vegetation, e.g. tropical rainforest, desert, tundra'),
         ('tricellular model', 'a model of atmospheric circulation in each hemisphere consisting of three cells - Hadley, Ferrel and polar - which redistributes heat and explains global patterns of pressure and precipitation'),
         ('Hadley cell', 'the circulation cell in which warm air rises at the equator (low pressure, high rainfall) and sinks at about 30° latitude (high pressure, deserts)'),
         ('Intertropical Convergence Zone (ITCZ)', 'the belt of low pressure near the equator where the trade winds converge and air rises, producing heavy convectional rainfall'),
         ('insolation', 'incoming solar radiation received at Earth\'s surface; it is highest near the equator and decreases towards the poles')],
  facts=[('Why are many of the world\'s hot deserts found at about 30° N and S?', 'Air descends in the Hadley cell, creating high pressure and dry conditions', ['They are closest to the Sun', 'Ocean currents bring rain', 'They lie in the ITCZ'], 'Descending air warms and inhibits cloud formation.'),
         ('Which two factors are most important in determining the distribution of biomes?', 'Temperature and precipitation', ['Soil colour and altitude', 'Wind speed and day length', 'Latitude and longitude only'], 'These determine productivity and the types of plants that can survive.'),
         ('Which cell of the tricellular model lies between about 30° and 60° latitude?', 'The Ferrel cell', ['The Hadley cell', 'The polar cell', 'The Walker cell'], 'The Ferrel cell is driven by the other two cells.'),
         ('Why does the equator receive more insolation than the poles?', 'The Sun\'s rays strike at a higher angle and pass through less atmosphere', ['The equator is closer to the Sun', 'The poles have more cloud', 'The equator has darker soils'], 'At high latitudes energy is spread over a larger area.')],
  why=[('Explain how the tricellular model accounts for the location of tropical rainforests.', 'At the equator intense insolation heats the surface; air rises in the ascending limb of the Hadley cells (ITCZ), cools and condenses, producing high rainfall all year with high temperatures - ideal for rainforest.'),
       ('Explain why biomes shift in latitude with the seasons in some regions.', 'The ITCZ and pressure belts follow the overhead Sun north and south, bringing seasonal rains (e.g. wet and dry seasons in the savanna and monsoon regions).'),
       ('Explain why climate change is expected to shift biome boundaries.', 'Changing temperature and precipitation alter the conditions each biome requires; boreal forest is expected to move polewards into tundra, deserts may expand, and species may be unable to migrate fast enough.')],
  contrast=[('the Hadley cell', 'the polar cell', 'The Hadley cell is driven by intense equatorial heating, with air rising at the equator and sinking at 30°; the polar cell has cold dense air sinking at the poles and flowing to about 60°, where it rises.'),
            ('weather', 'climate', 'Weather is the short-term state of the atmosphere (hours to days); climate is the average weather over a long period, usually 30 years.')],
  misc=[('Deserts are always hot.', 'Deserts are defined by low precipitation (< 250 mm/yr); cold deserts include the Gobi and Antarctica.'),
        ('Biomes are determined only by latitude.', 'Altitude, continentality, ocean currents and rain shadows also affect temperature and precipitation (e.g. the Atacama is a desert due to the cold Humboldt Current).')],
  apply=[('Describe the location of the world\'s tropical rainforests and explain their distribution using the tricellular model.', 'Between about 10° N and 10° S (Amazon, Congo, South-East Asia); rising air in the ITCZ gives heavy convectional rain and high insolation gives warmth all year.', 4),
         ('Suggest why the west coast of South America at 20° S is a desert while the Amazon at the same latitude receives over 1,500 mm of rain.', 'Descending Hadley-cell air plus the cold Humboldt Current and the Andes rain shadow keep the Atacama dry; the Amazon receives moist trade winds from the Atlantic.', 3)],
  cases=[('the Atacama Desert, Chile', 'some weather stations have recorded almost no rain for decades (mean < 1 mm/yr in places)', 'the influence of atmospheric circulation and ocean currents on biomes', 'subsiding Hadley-cell air, a cold offshore current and the Andes rain shadow combine to create extreme aridity'),
         ('the Sahel', 'rainfall depends on the northward movement of the ITCZ in summer; droughts in the 1970s-80s were linked to its failure to move far north', 'the seasonal migration of pressure belts', 'variability in the ITCZ position causes large year-to-year changes in rainfall and vegetation')],
  evaluate=[('The tricellular model fully explains the global distribution of biomes.', ['explains major rainfall and pressure belts', 'accounts for deserts at 30° and rainforest at the equator'], ['ignores ocean currents, altitude, continentality and monsoons', 'real circulation is more complex (jet streams, Rossby waves)'], 'The model explains the broad pattern but must be combined with local factors to explain the actual distribution.')],
  extended=[('Explain how the tricellular model accounts for the distribution of three named biomes. [7]', 'Rainforest (ITCZ rising air), hot desert (descending air at 30°), temperate forest (Ferrel cell, mid-latitude depressions), tundra (polar high, low insolation).', 7, 'explain')],
  res=[('Biome climate summary: tropical rainforest - mean temperature 26-28 °C, rainfall 2,000-4,000 mm; hot desert - 20-30 °C mean, < 250 mm; tundra - warmest month < 10 °C, 150-400 mm; temperate deciduous forest - 5-20 °C, 600-1,500 mm.',
        [('A station has a warmest-month mean of 8 °C and 220 mm of precipitation. Identify the biome and explain one adaptation of plants there.', 'Tundra; low-growing, cushion forms reduce wind exposure and stay under snow; shallow roots above permafrost; dark leaves absorb heat.'),
         ('Explain why the productivity of tundra is so much lower than tropical rainforest.', 'Low temperatures slow enzyme activity, the growing season is short, permafrost limits roots and nutrients are slowly recycled; rainforests are warm and wet all year.')])])

S('ch07-st2',
  terms=[('tropical rainforest', 'a biome near the equator with high temperatures (about 26-28 °C) and high rainfall (over 2,000 mm) all year, very high biodiversity and NPP'),
         ('hot desert', 'a biome with less than 250 mm of rainfall a year, high daytime temperatures and sparse vegetation adapted to drought'),
         ('tundra', 'a biome of high latitudes or altitudes with low temperatures, a short growing season, permafrost and low-growing vegetation'),
         ('temperate deciduous forest', 'a biome of mid-latitudes with mild summers, cool winters and broadleaved trees that shed leaves in winter'),
         ('boreal forest (taiga)', 'a biome of high mid-latitudes dominated by coniferous trees, with long cold winters and short summers'),
         ('biome shift', 'a change in the location of a biome as climate changes, e.g. boreal forest moving northwards into tundra')],
  facts=[('Which biome contains about half of the world\'s terrestrial species while covering about 6% of the land surface?', 'Tropical rainforest', ['Boreal forest', 'Tundra', 'Temperate grassland'], 'High productivity and stable climate support high diversity.'),
         ('Which is a typical adaptation of cacti in hot deserts?', 'Spines instead of leaves and water storage in a thick stem', ['Large thin leaves', 'Shallow roots in permafrost', 'Buttress roots'], 'Spines reduce transpiration and deter herbivores.'),
         ('Why do soils in tropical rainforests tend to be nutrient-poor?', 'Nutrients are rapidly recycled into biomass and leached by heavy rain', ['Decomposition is very slow', 'There is little leaf litter', 'They are frozen'], 'Most nutrients are stored in vegetation rather than soil.'),
         ('Which biome is most threatened by thawing permafrost?', 'Tundra', ['Tropical rainforest', 'Hot desert', 'Mediterranean scrub'], 'Permafrost holds about 1,400-1,600 GtC.')],
  why=[('Explain why tropical rainforests have high biodiversity.', 'High, constant temperatures and rainfall give high NPP and year-round growth; a stable climate over long periods allowed speciation; multiple vertical layers create many niches.'),
       ('Explain how climate change is affecting the tundra biome.', 'The Arctic is warming about 3-4 times faster than the global average; permafrost thaws releasing CO₂ and methane, shrubs expand northwards ("greening"), and specialist species (lemmings, Arctic fox) face competition from southern species.'),
       ('Explain why boreal forests are important carbon stores.', 'Cold temperatures slow decomposition, so carbon accumulates in deep soils, peat and permafrost; the boreal forest stores about a third of all terrestrial carbon.')],
  contrast=[('tropical rainforest', 'temperate deciduous forest', 'Tropical rainforests are hot and wet all year with very high diversity, many layers and rapid nutrient cycling; temperate deciduous forests have seasonal temperatures, trees that shed leaves in winter, lower diversity and richer soils with slower decomposition.'),
            ('tundra', 'boreal forest', 'Tundra is treeless with permafrost and a very short growing season; boreal forest is dominated by conifers and has a slightly longer, warmer summer.')],
  misc=[('Rainforest soils are fertile because the vegetation is so lush.', 'Most nutrients are held in the biomass; once cleared, soils quickly lose fertility through leaching.'),
        ('Biomes will simply move towards the poles as the climate warms.', 'Barriers (oceans, cities, mountains), slow dispersal of trees and soil development mean shifts are uneven, and some biomes (alpine, polar) have nowhere to move.')],
  apply=[('Describe two adaptations of animals to the hot desert biome.', 'e.g. fennec fox: large ears radiate heat, nocturnal; camel: stores fat in hump, concentrated urine, tolerates dehydration; kangaroo rat: obtains water from seeds, very concentrated urine.', 2),
         ('Suggest two ways in which climate change could alter the Amazon rainforest biome.', 'More frequent droughts (2005, 2010, 2015-16, 2023) and fires; shift towards savanna in the south and east; species moving upslope in the Andes; reduced carbon sink.', 2)],
  cases=[('Arctic greening in the tundra', 'satellite records show shrub expansion and longer growing seasons across Alaska and Siberia since the 1980s', 'biome shift due to climate change', 'warmer temperatures allow taller shrubs to spread into tundra, changing albedo and habitats'),
         ('the Amazon carbon sink', 'studies (Gatti et al., 2021) found parts of the south-eastern Amazon have become a net carbon source due to deforestation and drought', 'the effect of climate change and land use on biome function', 'stressed forest loses more carbon through tree death and fire than it gains through growth')],
  evaluate=[('Tundra is the biome most vulnerable to climate change.', ['fastest warming region', 'permafrost thaw is a positive feedback', 'no room to shift north'], ['coral reefs and mountain ecosystems also highly vulnerable', 'rainforests face combined climate and deforestation pressure'], 'Tundra is among the most vulnerable because of the speed of Arctic warming and its feedbacks, though other biomes face comparable threats.')],
  extended=[('Compare the structure and productivity of two named biomes and explain the differences. [7]', 'e.g. Amazon rainforest vs Sahara: temperature, precipitation, NPP (2,200 vs < 90 g m⁻² yr⁻¹), layers, biodiversity, nutrient cycling; explanation through climate (tricellular model).', 7, 'explain')],
  res=[('Mean NPP (g m⁻² yr⁻¹): tropical rainforest 2,200; temperate deciduous forest 1,200; boreal forest 800; temperate grassland 600; tundra 140; hot desert 90.',
        [('Calculate how many times more productive tropical rainforest is than tundra and explain the difference.', '2,200/140 ≈ 15.7 times; rainforest is warm and wet all year with high insolation, while tundra has low temperatures, a short growing season and limited liquid water.'),
         ('Suggest why boreal forest has a large carbon store despite moderate NPP.', 'Decomposition is very slow in the cold, acidic, often waterlogged soils, so organic matter (peat, permafrost) accumulates over thousands of years.')])])

S('ch07-st3', gens=['pr_ratio'],
  terms=[('succession', 'the process of change over time in an ecosystem involving pioneer, intermediate and climax communities'),
         ('primary succession', 'succession that occurs on a newly formed surface with no soil, such as bare rock, a lava flow or sand'),
         ('secondary succession', 'succession on a site where soil already exists after an existing community has been cleared, e.g. after fire or abandoned farmland'),
         ('pioneer species', 'the first organisms to colonise a bare area, such as lichens and mosses, tolerant of harsh conditions'),
         ('climax community', 'a relatively stable community at the end of succession, in equilibrium with the environment'),
         ('seral stage (sere)', 'one of the stages of community change in a succession'),
         ('plagioclimax', 'a community whose succession has been halted or deflected by human activity, e.g. grazed grassland or managed heather moorland')],
  facts=[('Which is an example of primary succession?', 'Colonisation of the volcanic island of Surtsey, Iceland, from 1963', ['Regrowth of a field after farming stops', 'A forest recovering after a fire', 'A meadow after a flood'], 'Surtsey formed from an eruption in 1963 with no soil.'),
         ('Which change usually occurs during succession?', 'Soil depth, organic matter and species diversity increase', ['Biomass decreases', 'Soil becomes thinner', 'Only one species survives'], 'Pioneers modify conditions, allowing other species to establish.'),
         ('A heather moorland in Scotland maintained by burning is an example of:', 'a plagioclimax', ['a climax community', 'primary succession', 'a pioneer community'], 'Burning stops succession to woodland.'),
         ('How does gross productivity compare with respiration in a climax community?', 'They are approximately equal (P:R ≈ 1)', ['Productivity is much greater', 'Respiration is zero', 'Productivity is zero'], 'In early stages P:R > 1 and biomass accumulates.')],
  why=[('Explain how pioneer species change the environment to allow succession.', 'Lichens weather rock and add organic matter when they die, forming thin soil that holds water and nutrients; this allows mosses, grasses and later shrubs to establish, which in turn shade and change conditions.'),
       ('Explain why species diversity often peaks before the climax community.', 'Mid-successional stages contain a mix of early and late species and varied habitats; at climax, dominant species out-compete others, slightly reducing diversity.'),
       ('Explain why secondary succession is faster than primary succession.', 'Soil, seed banks, roots and nutrients are already present, so plants can establish quickly without the slow process of soil formation.'),
       ('Explain how human activity can create a plagioclimax.', 'Grazing, burning, mowing or felling repeatedly removes later-successional species, holding the community at an earlier stage, e.g. grazed chalk grassland or burnt grouse moors.')],
  contrast=[('primary succession', 'secondary succession', 'Primary succession starts on bare, lifeless surfaces with no soil (lava, sand dunes); secondary succession starts where soil already exists after a disturbance (fire, abandoned field) and is faster.'),
            ('a climax community', 'a plagioclimax', 'A climax community is the stable end-point determined by climate and soils; a plagioclimax is held at an earlier stage by human activity (grazing, burning).'),
            ('r-selected species', 'K-selected species', 'r-selected species (pioneers) reproduce quickly, produce many small offspring and disperse widely; K-selected species (climax) are long-lived, compete well and produce few offspring with more parental care.')],
  misc=[('Succession always ends in forest.', 'The climax depends on climate and soils - it may be grassland, tundra or desert scrub where trees cannot grow.'),
        ('Once a climax community is reached it never changes.', 'Climax communities are in dynamic equilibrium; disturbances (storms, fire, disease) create gaps that start small-scale succession.')],
  apply=[('Describe the changes in biomass, soil depth and species diversity during a succession from bare sand to woodland.', 'Biomass increases greatly (grasses → shrubs → trees); soil deepens and gains organic matter and moisture; diversity rises then may fall slightly at climax.', 3),
         ('Suggest how the eruption of Mount St Helens in 1980 provided opportunities to study succession.', 'Areas buried by pyroclastic flows show primary succession; areas with surviving soil and buried plants show faster secondary succession; prairie lupines fixed nitrogen and accelerated soil development.', 3)],
  cases=[('Surtsey, Iceland', 'the island formed by eruption in 1963-67; mosses and lichens arrived first, a gull colony from 1985 added nutrients and plant diversity rose to about 80 vascular species', 'primary succession', 'colonisers arriving by sea, wind and birds gradually formed soil and communities on new volcanic rock'),
         ('Krakatau (Rakata), Indonesia', 'after the 1883 eruption sterilised the island, ferns and grasses arrived within three years, and forest covered much of it by the 1930s', 'primary succession on volcanic islands', 'pioneers built up organic matter, allowing later-successional trees dispersed by birds and bats to establish'),
         ('abandoned farmland in the eastern USA', 'fields abandoned in the 19th century passed from annual weeds to grasses, pine and then hardwood forest over about 150 years', 'secondary succession', 'existing soil and seed banks allowed rapid colonisation and a predictable sequence of seral stages')],
  evaluate=[('Human disturbance always reduces the biodiversity of ecosystems.', ['deforestation and urbanisation remove habitats', 'invasive species spread with disturbance'], ['intermediate disturbance can increase diversity', 'plagioclimaxes (chalk grassland, hay meadows) are biodiversity-rich'], 'Severe or frequent disturbance reduces biodiversity, but moderate, traditional management can maintain species-rich plagioclimax communities.')],
  extended=[('Explain the changes in energy flow, productivity and nutrient cycling that occur during a named succession. [7]', 'Early: low biomass, high P:R, open nutrient cycling; later: higher biomass, P:R → 1, more closed nutrient cycling, longer food webs, more niches; Surtsey or sand dune example.', 7, 'explain')],
  res=[('Data from the Surtsey survey (approximate): number of vascular plant species recorded - 1965: 1; 1975: 12; 1985: 20 (gull colony established); 1995: 40; 2008: 69.',
        [('Calculate the mean rate of species increase per year between 1985 and 2008 and compare it with 1965-1985.', '1985-2008: 49/23 ≈ 2.1 per year; 1965-1985: 19/20 ≈ 0.95 per year - the rate more than doubled.'),
         ('Suggest why the arrival of the gull colony increased the rate of colonisation.', 'Gull droppings added nitrogen and phosphorus, and gulls carried seeds; enriched soils allowed more plant species to establish.')])])

S('ch07-st4', gens=['transect', 'lapse'],
  terms=[('zonation', 'the arrangement or patterning of plant communities or ecosystems into parallel or sub-parallel bands in response to a change in some environmental factor over a distance'),
         ('environmental gradient', 'a gradual change in an abiotic factor over space, such as altitude, tidal exposure, salinity or soil moisture'),
         ('belt transect', 'a sampling strip in which quadrats are placed continuously or at intervals along a line to record changes in species distribution'),
         ('kite diagram', 'a graph showing the abundance of species along a transect, with the width of each "kite" proportional to abundance'),
         ('tree line', 'the altitude or latitude beyond which trees cannot grow, mainly because of low temperatures')],
  facts=[('How does zonation differ from succession?', 'Zonation is change in space along a gradient; succession is change over time at one place', ['They are the same process', 'Zonation is change over time', 'Succession only occurs on mountains'], 'Some sand-dune transects show both.'),
         ('Which abiotic factor mainly causes zonation on a rocky shore?', 'Time of exposure to air (desiccation) between tides', ['Soil pH', 'Altitude', 'Day length'], 'Organisms higher up are exposed for longer.'),
         ('By roughly how much does air temperature fall per 1,000 m increase in altitude?', 'About 6.5 °C', ['About 1 °C', 'About 15 °C', 'It increases'], 'This is the average environmental lapse rate.'),
         ('Which is the most appropriate graph to show species abundance along a transect?', 'A kite diagram', ['A pie chart', 'A climograph', 'A population pyramid'], 'Kite width shows abundance at each station.')],
  why=[('Explain why distinct vegetation zones occur on high mountains.', 'Temperature falls with altitude (lapse rate), while wind exposure, UV, snow cover and soil depth change; each species has a tolerance range, so different communities dominate at different altitudes.'),
       ('Explain why a transect is a suitable sampling method for investigating zonation.', 'Zonation occurs along an environmental gradient; a transect samples systematically along the gradient, recording how species and abiotic factors change with distance.'),
       ('Explain how climate change is altering zonation on mountains.', 'Warming shifts the tree line and species ranges upslope (about 30-60 m per decade in some studies); alpine species at the summit have nowhere to move and may face local extinction ("escalator to extinction").')],
  contrast=[('zonation', 'succession', 'Zonation is the spatial arrangement of communities along an environmental gradient at one time; succession is the temporal change of a community at one place.')],
  misc=[('Zonation on a mountain is caused only by temperature.', 'Precipitation, wind, soil depth, slope, aspect and human land use (grazing) also influence zonation.'),
        ('A transect gives an exact picture of every species in an area.', 'A transect samples only a narrow strip; it may miss species and needs repeats to be representative.')],
  apply=[('Describe how you would investigate zonation on a sand-dune system.', 'Lay a tape from the strandline inland; at regular intervals (e.g. every 10 m) place a quadrat and record percentage cover of each species; measure abiotic factors (wind, soil moisture, pH, organic content); repeat transects; present as a kite diagram.', 4),
         ('Suggest how trampling by visitors could affect zonation on a dune system.', 'Trampling breaks marram grass, causing blowouts; zones may be reduced or shifted; management includes boardwalks and fencing.', 2)],
  cases=[('altitudinal zonation on Mount Kilimanjaro', 'zones change from cultivated land and montane forest (about 1,800-2,800 m) through heath and moorland to alpine desert above about 4,000 m and ice at the summit', 'zonation along an altitudinal gradient', 'decreasing temperature and precipitation with height produce distinct bands of vegetation'),
         ('the Studland sand-dune system, Dorset', 'transects show embryo dunes with sea couch, yellow dunes dominated by marram, grey dunes with lichens and heath further inland', 'zonation linked to succession on dunes', 'gradients in sand movement, salinity, soil organic matter and pH produce bands that also represent stages of succession'),
         ('rocky shores of the Atlantic coast of Europe', 'channel wrack and lichens dominate the upper shore, barnacles and limpets the middle shore and kelp the lower shore', 'zonation caused by tidal exposure', 'tolerance of desiccation decreases down the shore, while competition and predation increase')],
  evaluate=[('Mountain ecosystems are the most useful indicators of climate change impacts.', ['species shift upslope quickly and measurably', 'long-term records exist (Alps, Andes)'], ['other factors (grazing, land use) confound trends', 'polar and marine indicators also strong'], 'Mountains are valuable indicators because gradients are compressed, but trends must be separated from land-use changes.')],
  extended=[('Explain how abiotic factors produce zonation in a named ecosystem and how it could be investigated. [7]', 'e.g. rocky shore: exposure, desiccation, wave action, salinity; species tolerances and biotic interactions; interrupted belt transect, percentage cover/counts, abiotic measurements, kite diagram.', 7, 'explain')],
  res=[('Belt-transect data up a mountain slope in the Alps: 1,000 m - beech-fir forest 85% cover; 1,600 m - spruce forest 70%; 2,000 m - larch and dwarf pine 40%; 2,400 m - alpine meadow 60% grass/herb; 3,000 m - scattered cushion plants 5%. Mean temperature at 1,000 m is 9 °C.',
        [('Using a lapse rate of 6.5 °C per 1,000 m, calculate the mean temperature at 2,400 m.', '9 − 6.5 × 1.4 = 9 − 9.1 = −0.1 °C.'),
         ('Describe the pattern shown and explain why tree cover falls with altitude.', 'Tree cover falls from 85% to none above about 2,000-2,400 m; lower temperatures shorten the growing season, wind and snow damage increase and soils are thinner, so trees cannot survive above the tree line.')])])


# =============================================================================================
# ch08 3.1 Biodiversity and evolution
# =============================================================================================
S('ch08-st1', gens=['simpson'],
  terms=[('biodiversity', 'the variety of life in all its forms, levels and combinations, including ecosystem, species and genetic diversity'),
         ('genetic diversity', 'the range of genetic material present in a population or species'),
         ('species diversity', 'the variety of species per unit area, including both the number of species present (richness) and their relative abundance (evenness)'),
         ('habitat diversity', 'the range of different habitats in an ecosystem or biome'),
         ('biodiversity hotspot', 'a region with at least 1,500 endemic vascular plant species that has lost at least 70% of its original habitat'),
         ('endemic species', 'a species that is found naturally in only one geographical area')],
  facts=[('Approximately how many species have been described by scientists?', 'About 1.8-2 million', ['About 50,000', 'About 100 million', 'About 500 million'], 'Estimates of total species range from about 8.7 million upwards.'),
         ('Why is genetic diversity important for crop species?', 'It provides traits for breeding resistance to disease, pests and drought', ['It makes all plants identical', 'It increases fertiliser use', 'It has no practical importance'], 'Seed banks such as the Svalbard Global Seed Vault store it.'),
         ('Which index increases with both species richness and evenness?', 'Simpson\'s reciprocal index', ['Lincoln index', 'Population density', 'Percentage cover'], 'D = N(N − 1)/Σn(n − 1).'),
         ('The Irish potato famine of 1845-1852 was made worse by:', 'low genetic diversity of the potato crop (mostly the "Lumper" variety)', ['too many potato varieties', 'high species diversity in fields', 'irrigation'], 'Phytophthora infestans spread through genetically uniform crops.')],
  why=[('Explain why a community with high evenness is considered more diverse than one dominated by one species.', 'Diversity includes how individuals are distributed among species; if one species dominates, the chance that two random individuals are different species is low, so effective diversity is lower even if richness is the same.'),
       ('Explain why the total number of species on Earth is uncertain.', 'Many groups (insects, fungi, nematodes, microbes) are poorly studied; many habitats (deep sea, canopy, soils) are under-sampled; taxonomy is slow; cryptic species are revealed only by DNA analysis.'),
       ('Explain why genetic diversity is important for the survival of a species.', 'Variation allows some individuals to survive new diseases, predators or climate change, so the population can adapt by natural selection; low diversity increases inbreeding depression and extinction risk (e.g. cheetahs).')],
  contrast=[('species diversity', 'genetic diversity', 'Species diversity is the variety and relative abundance of species in an area; genetic diversity is the variety of genes and alleles within a population or species.'),
            ('species richness', 'species diversity', 'Richness is just the number of species; diversity combines richness with evenness (relative abundance).')],
  misc=[('Biodiversity simply means the number of species in an area.', 'Biodiversity includes genetic, species and habitat (ecosystem) diversity, and species diversity includes evenness as well as richness.'),
        ('A monoculture plantation with many trees has high biodiversity.', 'A monoculture has very low species and genetic diversity regardless of how many individuals it has.')],
  apply=[('Suggest why the cheetah is vulnerable to extinction even in protected areas.', 'A population bottleneck about 10,000 years ago left very low genetic diversity, causing reduced sperm quality, high cub mortality and vulnerability to disease.', 2),
         ('Outline three reasons why biodiversity should be conserved.', 'Ecological (stability, ecosystem services such as pollination); economic (food, medicines - about half of modern drugs derive from natural compounds; tourism); aesthetic, cultural and ethical (intrinsic value).', 3)],
  cases=[('the Irish potato famine (1845-1852)', 'about 1 million people died and 1 million emigrated after potato blight destroyed crops of the genetically uniform Lumper potato', 'the importance of genetic diversity', 'low genetic diversity meant almost no plants were resistant, so the pathogen spread through the whole crop'),
         ('the Svalbard Global Seed Vault, Norway', 'opened in 2008 in permafrost rock, it holds over 1.2 million seed samples from almost every country', 'ex situ conservation of genetic diversity', 'it backs up crop genetic diversity so lost varieties can be restored, e.g. Syrian ICARDA withdrawals in 2015')],
  evaluate=[('Diversity indices are the best way to measure the health of an ecosystem.', ['quantitative and comparable over time', 'include richness and evenness'], ['do not identify which species (invasives, rare species)', 'depend on sampling effort', 'ignore genetic and ecosystem diversity'], 'Indices are useful indicators but must be combined with indicator species, ecosystem function and conservation status data.')],
  extended=[('Explain why genetic, species and habitat diversity are all important for the resilience of ecosystems. [7]', 'Genetic: adaptation, disease resistance (potato famine, cheetah); species: functional redundancy, food-web stability; habitat: niches and refuges; links to resilience and tipping points.', 7, 'explain')],
  res=[('Field data, two grasslands (individuals per species): Meadow A - 10, 10, 10, 10, 10; Meadow B - 46, 1, 1, 1, 1.',
        [('Calculate Simpson\'s reciprocal index for both meadows using D = N(N−1)/Σn(n−1).', 'A: N = 50, Σn(n−1) = 5 × 90 = 450, D = 2,450/450 ≈ 5.44; B: Σn(n−1) = 46×45 = 2,070, D = 2,450/2,070 ≈ 1.18.'),
         ('Explain why the meadows have the same richness but different diversity.', 'Both have 5 species, but Meadow A has perfect evenness whereas Meadow B is dominated by one species, so diversity is much lower.')])])

S('ch08-st2', gens=['extinction'],
  terms=[('natural selection', 'the process by which individuals with heritable traits better suited to their environment survive and reproduce more, so those traits become more common over generations'),
         ('speciation', 'the formation of new and distinct species through evolution'),
         ('allopatric speciation', 'speciation that occurs when populations are geographically isolated and evolve separately'),
         ('sympatric speciation', 'speciation that occurs without geographical isolation, e.g. through polyploidy or behavioural isolation'),
         ('mass extinction', 'an event in which at least 75% of species are lost in a geologically short period'),
         ('adaptive radiation', 'the rapid evolution of many species from a common ancestor to fill different niches')],
  facts=[('How many mass extinctions are recognised in the fossil record?', 'Five', ['Two', 'Ten', 'Twenty'], 'End-Ordovician, Late Devonian, end-Permian, end-Triassic, end-Cretaceous.'),
         ('Which mass extinction, about 252 million years ago, killed an estimated 90-96% of marine species?', 'The end-Permian extinction', ['The end-Cretaceous extinction', 'The Late Devonian extinction', 'The end-Ordovician extinction'], 'Linked to Siberian Traps volcanism and ocean acidification.'),
         ('The end-Cretaceous extinction 66 million years ago is mainly attributed to:', 'an asteroid impact at Chicxulub, Mexico, combined with Deccan volcanism', ['human hunting', 'an ice age only', 'the evolution of flowering plants'], 'It ended the non-avian dinosaurs.'),
         ('Darwin\'s finches on the Galápagos are a classic example of:', 'adaptive radiation', ['convergent evolution', 'mass extinction', 'artificial selection'], 'Beak shapes evolved to exploit different food sources.')],
  why=[('Explain how natural selection can lead to changes in a population.', 'Individuals vary; there is overproduction and competition; individuals with advantageous heritable traits survive and reproduce more; their alleles increase in frequency over generations (e.g. beak depth of Galápagos finches after the 1977 drought).'),
       ('Explain how geographical isolation can lead to speciation.', 'A barrier (mountain range, sea, river) splits a population; gene flow stops; different selection pressures, mutation and genetic drift cause divergence; eventually the populations can no longer interbreed - reproductive isolation.'),
       ('Explain why many scientists argue that a sixth mass extinction is under way.', 'Current extinction rates are estimated at tens to hundreds of times the background rate; about 1 million species are threatened (IPBES 2019); causes are habitat loss, overexploitation, climate change, pollution and invasive species - all human.')],
  contrast=[('allopatric speciation', 'sympatric speciation', 'Allopatric speciation follows geographical separation of populations; sympatric speciation occurs in the same area through reproductive isolation such as polyploidy or different breeding times.'),
            ('background extinction', 'mass extinction', 'Background extinction is the normal, low rate of species loss (about 0.1-1 E/MSY); a mass extinction is a geologically rapid loss of at least 75% of species.')],
  misc=[('Individual organisms evolve during their lifetime to suit their environment.', 'Populations evolve over generations; individuals do not change their genes in response to the environment.'),
        ('Mass extinctions have always been caused by asteroids.', 'Most were linked to massive volcanism, climate change, ocean anoxia and acidification; only the end-Cretaceous is strongly linked to an impact.')],
  apply=[('In 1977 a drought on Daphne Major (Galápagos) killed many medium ground finches. Survivors had deeper beaks. Explain this observation.', 'Drought reduced small soft seeds; only large hard seeds remained; birds with deeper beaks could crack them and survived; beak depth is heritable, so the next generation had deeper beaks (natural selection - Grant and Grant).', 3),
         ('Suggest how continental drift could lead to the formation of new species.', 'Splitting of landmasses isolates populations (e.g. ratites - ostrich, emu, rhea - after Gondwana broke up); separate evolution under different conditions leads to allopatric speciation.', 3)],
  cases=[('Darwin\'s finches on the Galápagos Islands', 'about 15-18 species evolved from a single ancestral species that arrived from South America about 2-3 million years ago', 'adaptive radiation and speciation', 'isolation on different islands and different food sources selected different beak shapes, producing species that no longer interbreed'),
         ('the cichlid fish of Lake Malawi', 'over 500-800 species evolved within the lake in less than a few million years', 'sympatric and allopatric speciation', 'specialisation of jaws and diets plus mate choice by colour created reproductive isolation within one lake'),
         ('the peppered moth in industrial England', 'the dark (carbonaria) form rose to over 90% in Manchester by about 1895 as soot darkened trees, then declined after clean air laws', 'natural selection', 'predation by birds favoured the better-camouflaged form, changing allele frequencies in response to environmental change')],
  evaluate=[('The current biodiversity crisis should be considered a sixth mass extinction.', ['extinction rates 10-100+ times background', '1 million species threatened (IPBES)', 'rapid, global, human-driven'], ['documented extinctions are still far below 75% of species', 'data are incomplete and biased', 'losses are reversible if action is taken'], 'We are not yet in a mass extinction by the 75% definition, but current trends could produce one within centuries, which justifies urgent action.')],
  extended=[('Explain how plate tectonics, natural selection and isolation can lead to speciation, with named examples. [7]', 'Isolation (oceanic islands, continental drift, mountains), variation and selection, genetic drift, reproductive isolation; Galápagos finches, cichlids, ratites, Madagascar lemurs.', 7, 'explain')],
  res=[('Graph description: number of marine animal families over time shows five sharp drops - end-Ordovician (444 Ma) about 85% of species lost; Late Devonian (372 Ma) about 75%; end-Permian (252 Ma) about 96%; end-Triassic (201 Ma) about 80%; end-Cretaceous (66 Ma) about 76%.',
        [('Identify the most severe mass extinction and calculate how long ago it occurred relative to the end-Cretaceous event.', 'End-Permian (~96%); 252 − 66 = 186 million years earlier.'),
         ('Suggest why biodiversity recovered after each mass extinction.', 'Surviving species underwent adaptive radiation into vacant niches (e.g. mammals after the dinosaurs), over millions of years.')])])

S('ch08-st3',
  terms=[('plate tectonics', 'the theory that Earth\'s lithosphere is divided into plates that move over the mantle, causing continents to drift, join and separate'),
         ('Pangaea', 'the supercontinent that existed about 335-175 million years ago before breaking into Laurasia and Gondwana'),
         ('geographical isolation', 'the separation of populations by physical barriers such as oceans, mountains or rivers'),
         ('land bridge', 'a strip of land connecting two landmasses that allows the movement of species, e.g. the Isthmus of Panama or Beringia'),
         ('biodiversity hotspot', 'a region with at least 1,500 endemic vascular plant species that has lost at least 70% of its primary vegetation')],
  facts=[('How many biodiversity hotspots have been identified by Conservation International?', '36', ['5', '12', '100'], 'They cover about 2.5% of land but support over half of endemic plant species.'),
         ('The formation of the Isthmus of Panama about 3 million years ago led to:', 'the Great American Biotic Interchange of mammals between North and South America', ['the extinction of all marine species', 'the formation of the Galápagos', 'the separation of Africa and Asia'], 'It also separated Caribbean and Pacific marine species, causing speciation.'),
         ('Why does Madagascar have very high endemism (e.g. all lemurs)?', 'It has been isolated from Africa for about 160 million years and from India for about 88 million years', ['It is close to the equator', 'It has no predators', 'It was recently formed by volcanoes'], 'Long isolation allowed independent evolution.'),
         ('Why are marsupials diverse in Australia?', 'Australia separated from other continents before placental mammals became dominant there, allowing marsupials to radiate', ['Marsupials evolved only in Australia', 'Placentals cannot survive the climate', 'Humans introduced them'], 'Isolation since about 35 million years ago.')],
  why=[('Explain how plate movements have influenced the distribution of species.', 'Separation of continents isolated populations, leading to allopatric speciation (ratites, marsupials); collisions created land bridges allowing migration and competition (Panama); plate movement also changed climates and created mountains that act as barriers.'),
       ('Explain why biodiversity hotspots are a priority for conservation.', 'They contain a very high proportion of endemic species in a small area (about half of plant species on 2.5% of land) and are highly threatened (≥70% habitat lost), so conservation here prevents many extinctions per dollar spent.'),
       ('Explain why islands often have high endemism but also high extinction rates.', 'Isolation allows unique evolution, but small populations, limited ranges, lack of defences against introduced predators and limited space make island species vulnerable (e.g. the dodo of Mauritius).')],
  contrast=[('a biodiversity hotspot', 'a high-biodiversity wilderness area', 'A hotspot combines high endemism with heavy habitat loss (≥ 70%); a high-biodiversity wilderness area (e.g. the Amazon, Congo) is species-rich but still largely intact.')],
  misc=[('Biodiversity hotspots are the areas with the most species overall.', 'Hotspots are defined by endemism and threat; some very species-rich areas (the Amazon) are not hotspots because they remain largely intact.'),
        ('Continents have always been in their present positions.', 'Continents have moved over hundreds of millions of years; Pangaea broke up from about 175 million years ago.')],
  apply=[('Suggest why the ostrich, emu and rhea are found on different continents.', 'They descend from a common ancestor on Gondwana; when the supercontinent split, populations were isolated and evolved into separate species.', 3),
         ('Suggest two criticisms of using hotspots to set conservation priorities.', 'They focus on plant endemism, ignoring other taxa, genetic diversity and ecosystem services; they overlook threatened areas with fewer endemics and marine ecosystems; they may neglect local people\'s needs.', 2)],
  cases=[('Madagascar', 'isolated for about 88 million years, it has over 100 lemur species and about 90% of its plants are endemic, but has lost about 90% of its original forest', 'the role of isolation in creating a biodiversity hotspot', 'long isolation produced unique species, while high habitat loss makes it a priority hotspot'),
         ('the Great American Biotic Interchange', 'the Isthmus of Panama formed about 2.7-3 million years ago, allowing armadillos and opossums to move north and big cats, deer and camelids to move south', 'land bridges and species distribution', 'connection of landmasses mixed faunas, causing competition and extinctions of many South American mammals'),
         ('the Sundaland hotspot (Borneo, Sumatra, Java)', 'land bridges during glacial periods connected the islands; today it holds about 15,000 endemic plants but has lost over 90% of lowland forest in parts', 'plate tectonics, sea-level change and hotspots', 'changing connections promoted both dispersal and isolation, producing high endemism now threatened by oil-palm expansion')],
  evaluate=[('Concentrating conservation funding on biodiversity hotspots is the best strategy for protecting global biodiversity.', ['protects many endemic species cheaply', 'focuses on urgent threats'], ['neglects intact wilderness and oceans', 'ignores ecosystem services and genetic diversity', 'may displace local communities'], 'Hotspots are an efficient priority-setting tool but should be combined with protection of wilderness areas, marine systems and community-based conservation.')],
  extended=[('Discuss the extent to which plate tectonics explains present-day patterns of biodiversity. [9]', 'Continental drift and isolation (marsupials, ratites, Madagascar), land bridges (Panama, Beringia), mountain building and climate; other factors - climate gradients, glaciation, human activity, island biogeography; judgement.', 9, 'long')],
  res=[('Data: Madagascar - endemic plants about 90%; endemic mammals about 92%; original forest lost about 90%; human population 30 million, growing at about 2.4% per year.',
        [('Using the hotspot criteria, explain why Madagascar qualifies as a hotspot.', 'It has far more than 1,500 endemic vascular plants (about 90% of ~12,000 species) and has lost more than 70% of its original vegetation.'),
         ('Calculate the doubling time of Madagascar\'s population and suggest one implication for its forests.', '70 / 2.4 ≈ 29 years; growing demand for farmland (tavy slash-and-burn) and charcoal will increase pressure on remaining forest.')])])


# =============================================================================================
# ch09 3.2 Human impact on biodiversity; 3.3 Conservation and regeneration
# =============================================================================================
S('ch09-st1', gens=['habitat_loss'],
  terms=[('habitat fragmentation', 'the breaking up of a continuous habitat into smaller, isolated patches, increasing edge effects and isolating populations'),
         ('invasive species', 'a non-native species introduced by humans that spreads and causes ecological or economic harm'),
         ('overexploitation', 'the harvesting of a species faster than it can replace itself, e.g. overfishing, poaching or logging'),
         ('edge effect', 'changes in conditions (light, wind, temperature, predators) at the boundary of a habitat that affect species near the edge'),
         ('HIPPO', 'an acronym for the main causes of biodiversity loss: Habitat loss, Invasive species, Pollution, Population (human) and Overexploitation')],
  facts=[('According to IPBES (2019), what is the largest direct driver of biodiversity loss on land?', 'Land-use change (habitat loss)', ['Climate change', 'Light pollution', 'Volcanic eruptions'], 'In the oceans the largest driver is direct exploitation (fishing).'),
         ('The brown tree snake caused the extinction of most native forest birds on which island?', 'Guam', ['Madagascar', 'Hawaii', 'Mauritius'], 'Introduced accidentally after World War II, it had no predators.'),
         ('The Living Planet Index (WWF, 2024) reported an average decline in monitored vertebrate populations since 1970 of about:', '73%', ['5%', '25%', '95%'], 'Freshwater populations declined most (about 85%).'),
         ('Which invasive species has spread through Lake Victoria\'s cichlid communities since the 1950s?', 'Nile perch', ['Zebra mussel', 'Cane toad', 'Grey squirrel'], 'About 200 cichlid species were lost.')],
  why=[('Explain why habitat fragmentation reduces biodiversity even when the total area of habitat lost is small.', 'Small patches support smaller populations (more vulnerable to inbreeding and chance events), edge effects reduce interior habitat, and isolation prevents dispersal and recolonisation.'),
       ('Explain why invasive species are often successful in their new environment.', 'They lack natural predators, parasites and competitors (enemy release); they often reproduce rapidly, are generalists and tolerate a wide range of conditions; native species have not evolved defences.'),
       ('Explain why island species are particularly vulnerable to human impacts.', 'Small ranges and populations, high endemism, and evolution without predators (e.g. flightless birds) mean introduced predators and habitat loss quickly cause extinction.'),
       ('Explain how climate change contributes to biodiversity loss.', 'Species ranges shift faster than many can move, phenology becomes mismatched (e.g. caterpillar peak and bird breeding), coral bleaching, and extreme events and droughts increase mortality.')],
  contrast=[('habitat loss', 'habitat fragmentation', 'Habitat loss is the outright destruction of habitat area; fragmentation splits remaining habitat into isolated patches, which can reduce biodiversity even without large area loss.'),
            ('a native species', 'an invasive species', 'A native species occurs naturally in an area; an invasive species has been introduced by humans and spreads, causing harm.')],
  misc=[('All non-native species are invasive.', 'Most introduced species do not become invasive; only those that spread and cause harm are called invasive (e.g. many crop plants are non-native but not invasive).'),
        ('Extinction is mainly caused by natural events today.', 'Current extinctions are overwhelmingly caused by human activities - habitat loss, overexploitation, invasive species, pollution and climate change.')],
  apply=[('Suggest why the cane toad has spread so successfully in Australia since its introduction in 1935.', 'It is toxic to native predators that lack resistance (quolls, goannas), breeds prolifically (up to 30,000 eggs per clutch), tolerates many habitats and has no natural predators; it has spread over 1.2 million km².', 3),
         ('Identify two causes of biodiversity loss shown by oil-palm expansion in Borneo.', 'Habitat loss and fragmentation of lowland rainforest (orangutan populations fell by over 100,000 from 1999-2015), pollution from fertiliser and pesticide runoff, fires on drained peat.', 2)],
  cases=[('the brown tree snake on Guam', 'accidentally introduced after World War II, it caused the extinction of 10 of 12 native forest bird species', 'invasive species as a cause of biodiversity loss', 'a predator with no natural enemies met prey with no evolved defences on an isolated island'),
         ('the Bornean orangutan', 'populations declined by over 100,000 individuals between 1999 and 2015, and the species was listed as Critically Endangered in 2016', 'habitat loss and hunting', 'logging and conversion to oil palm and pulpwood, plus killing in conflicts, reduced and fragmented habitat'),
         ('the passenger pigeon', 'once numbering perhaps 3-5 billion in North America, the last individual, Martha, died in Cincinnati Zoo in 1914', 'overexploitation', 'commercial hunting and forest clearance reduced colonies below the size needed for successful breeding')],
  evaluate=[('Habitat loss is a greater threat to biodiversity than climate change.', ['IPBES ranks land-use change as the top driver on land', 'immediate and widespread (tropical deforestation ~10 million ha/yr)'], ['climate change impacts are accelerating and affect all habitats including protected areas', 'it interacts with and worsens other threats'], 'Habitat loss is currently the largest driver, but climate change is likely to rival or exceed it this century, and the two reinforce each other.')],
  extended=[('Evaluate the relative importance of different human activities in causing biodiversity loss, with reference to named examples. [9]', 'HIPPO factors with examples: oil-palm in Borneo, brown tree snake on Guam, DDT and peregrines, passenger pigeon, Grand Banks cod, coral bleaching; IPBES rankings; interactions; judgement.', 9, 'long')],
  res=[('Living Planet Index (WWF 2024): average decline in monitored vertebrate populations 1970-2020 - global 73%; Latin America and Caribbean 95%; Africa 76%; Asia-Pacific 60%; North America 39%; Europe and Central Asia 35%; freshwater species 85%.',
        [('Identify the region with the greatest decline and suggest two reasons for it.', 'Latin America and the Caribbean (95%); tropical deforestation for cattle and soy, overexploitation, disease (chytrid in amphibians), climate change.'),
         ('Suggest why declines appear smaller in Europe and North America.', 'Much habitat loss occurred before 1970, so the baseline is already degraded; stronger environmental regulation and conservation since 1970.')])])

S('ch09-st2', gens=['iucn'],
  terms=[('IUCN Red List', 'the International Union for Conservation of Nature\'s global inventory of the conservation status of species, assessed using standard criteria'),
         ('Critically Endangered', 'the IUCN category for species facing an extremely high risk of extinction in the wild'),
         ('Endangered', 'the IUCN category for species facing a very high risk of extinction in the wild'),
         ('Vulnerable', 'the IUCN category for species facing a high risk of extinction in the wild'),
         ('Extinct in the Wild', 'the IUCN category for a species known only to survive in cultivation, captivity or as naturalised populations outside its past range'),
         ('Data Deficient', 'the IUCN category for a species with inadequate information to assess its extinction risk')],
  facts=[('Which factors are used by the IUCN to determine conservation status?', 'Population size, rate of decline, geographical range and degree of fragmentation', ['Body size and colour only', 'Commercial value only', 'Number of zoos holding the species'], 'Criteria A-E cover these factors.'),
         ('Approximately how many species on the IUCN Red List are threatened with extinction (2024)?', 'More than 46,000', ['About 500', 'About 5,000', 'More than 1 million'], 'This includes about 41% of amphibians and 26% of mammals assessed.'),
         ('The vaquita, the world\'s most endangered marine mammal, lives only in:', 'the northern Gulf of California, Mexico', ['the Baltic Sea', 'the Ganges', 'the Southern Ocean'], 'Gillnet bycatch reduced it to about 10 individuals by 2023.'),
         ('Which species was successfully moved from Endangered to Vulnerable (2016) after conservation efforts?', 'The giant panda', ['The vaquita', 'The Sumatran rhino', 'The northern white rhino'], 'Wild numbers rose to about 1,864 adults (2014 census).')],
  why=[('Explain why the IUCN Red List is useful for conservation.', 'It uses objective, standard criteria to rank extinction risk, identifies priorities, informs legislation (e.g. CITES, national laws), monitors trends over time (Red List Index) and raises public awareness.'),
       ('Explain why some species are listed as Data Deficient.', 'There is insufficient information on population, range or threats - common for small, cryptic, deep-sea or tropical species; it does not mean they are safe.'),
       ('Explain how the characteristics of a species can make it vulnerable to extinction.', 'Small population, narrow range or habitat specialism, slow reproduction (K-selected), large body size and need for large territories, low genetic diversity and high commercial value (e.g. rhino horn).')],
  contrast=[('Critically Endangered', 'Vulnerable', 'Critically Endangered species face an extremely high risk of extinction (e.g. ≥ 80% decline over 10 years or 3 generations); Vulnerable species face a high risk (e.g. ≥ 30% decline).'),
            ('Extinct', 'Extinct in the Wild', 'Extinct means no individuals remain anywhere; Extinct in the Wild means the species survives only in captivity or cultivation (e.g. the scimitar-horned oryx before reintroduction).')],
  misc=[('A species not on the Red List is safe.', 'Only about 166,000 of the ~2 million described species have been assessed; many unassessed species may be threatened.'),
        ('Large populations can never be threatened.', 'Species with large populations can still qualify under criterion A if they are declining rapidly (e.g. the European eel).')],
  apply=[('Using a named example, outline the ecological, socio-political and economic pressures that caused a species to become threatened.', 'e.g. the Sumatran rhino (fewer than 50): ecological - small fragmented populations, slow breeding; economic - demand for horn in traditional medicine; socio-political - weak enforcement, forest clearance for plantations.', 4),
         ('Suggest why the vaquita has continued to decline despite a gillnet ban.', 'Illegal gillnets for totoaba fish (swim bladders sold in China for high prices) continue; enforcement in the Gulf is weak; fishers lack alternative livelihoods.', 3)],
  cases=[('the vaquita (Phocoena sinus)', 'numbers fell from about 600 in 1997 to about 10 by 2023 because of drowning in illegal gillnets set for totoaba', 'a Critically Endangered species', 'a small range, slow reproduction and an economic driver (totoaba swim bladder trade) combined with weak enforcement'),
         ('the giant panda', 'habitat protection (67 reserves), reforestation and captive breeding increased wild numbers by about 17% between 2004 and 2014', 'a successful downgrading of conservation status', 'sustained habitat protection reduced the main threat, and the species moved from Endangered to Vulnerable in 2016'),
         ('the northern white rhino', 'only two females remain (2024), after poaching reduced the subspecies to near zero; scientists are attempting IVF using stored embryos', 'functional extinction', 'with no breeding males the population cannot recover naturally, showing the cost of acting too late')],
  evaluate=[('The IUCN Red List is an effective tool for preventing extinctions.', ['objective criteria', 'shapes funding and legislation', 'tracks trends'], ['assessments are slow and biased to vertebrates', 'listing does not remove threats', 'many species Data Deficient'], 'The Red List is essential for prioritising and monitoring, but it is a diagnostic tool; prevention depends on enforcement and funding.')],
  extended=[('With reference to a named Critically Endangered species, explain the factors that have led to its status and evaluate measures taken to protect it. [9]', 'e.g. vaquita, Sumatran rhino, kākāpō, Philippine eagle: ecological, economic and political factors; measures (bans, reserves, captive breeding, CITES); evaluation and judgement.', 9, 'long')],
  res=[('IUCN Red List (2024) - percentage of assessed species threatened: amphibians 41%; reef-building corals 44%; sharks and rays 37%; mammals 26%; conifers 34%; birds 12%.',
        [('Identify the two groups with the highest proportion threatened and suggest a reason for each.', 'Reef-building corals (44%) - warming and bleaching, acidification; amphibians (41%) - chytrid fungus, habitat loss, pollution.'),
         ('Suggest one reason why these figures may underestimate the true number of threatened species.', 'Only a fraction of species have been assessed; invertebrates, fungi and plants are under-represented; Data Deficient species are excluded.')])])

S('ch09-st3', gens=['reserve'],
  terms=[('in situ conservation', 'the conservation of species in their natural habitat, e.g. national parks and nature reserves'),
         ('ex situ conservation', 'the conservation of species outside their natural habitat, e.g. zoos, botanic gardens, seed banks and captive breeding'),
         ('species-based conservation', 'conservation focused on protecting a particular species, often a flagship or keystone species, e.g. CITES, captive breeding'),
         ('habitat-based conservation', 'conservation focused on protecting whole habitats or ecosystems, e.g. protected areas and wildlife corridors'),
         ('wildlife corridor', 'a strip of habitat connecting isolated habitat patches, allowing species to move, disperse and maintain gene flow'),
         ('SLOSS debate', 'the debate over whether a Single Large Or Several Small reserves of the same total area better conserve biodiversity'),
         ('flagship species', 'a charismatic species used to attract public support and funding for conservation, e.g. the giant panda or tiger')],
  facts=[('Which design feature reduces edge effects in a protected area?', 'A compact shape such as a circle rather than a long thin shape', ['Many roads through the centre', 'Long, thin boundaries', 'A large perimeter-to-area ratio'], 'Compact shapes minimise the edge-to-area ratio.'),
         ('The Kunming-Montreal Global Biodiversity Framework (2022) set a target to protect what fraction of land and sea by 2030?', '30%', ['5%', '50%', '100%'], 'Known as the "30 by 30" target.'),
         ('Which is an example of ex situ conservation?', 'The Millennium Seed Bank at Kew', ['Kruger National Park', 'A marine protected area', 'A wildlife corridor'], 'Ex situ means outside the natural habitat.'),
         ('Which type of species is the grey wolf in Yellowstone, because its removal or return changes the whole ecosystem?', 'A keystone species', ['A pioneer species', 'An invasive species', 'An endemic plant'], 'Keystone species have a disproportionate effect relative to abundance.')],
  why=[('Explain why habitat-based conservation is often more effective than species-based conservation.', 'Protecting habitats conserves whole communities, food webs and ecosystem processes, benefiting many species (including unknown ones) at once, whereas species-based approaches protect one species and may fail if its habitat is lost.'),
       ('Explain why wildlife corridors are important in protected-area design.', 'They link fragments so animals can move, find mates and new territories, maintaining gene flow and allowing recolonisation and range shifts under climate change.'),
       ('Explain why involving local communities improves the success of protected areas.', 'Communities gain income (ecotourism, sustainable harvesting) and have a stake in protection; local knowledge improves management; it reduces conflict and illegal use.'),
       ('Explain why a single large reserve may be better than several small ones.', 'It has a lower edge-to-area ratio and more interior habitat, supports larger populations of wide-ranging and interior species, and is more resilient to chance events; however several small reserves spread risk.')],
  contrast=[('in situ conservation', 'ex situ conservation', 'In situ conservation protects species in their natural habitat with their ecological interactions; ex situ conservation keeps them outside it (zoos, seed banks) as a back-up or for captive breeding.'),
            ('species-based conservation', 'habitat-based conservation', 'Species-based conservation targets a single species (e.g. CITES listings, captive breeding of the kākāpō); habitat-based conservation protects whole ecosystems (e.g. national parks), benefiting many species.')],
  misc=[('Zoos are the best way to save endangered species.', 'Zoos can help through captive breeding and education, but most species can only survive long term in their habitats; reintroduction needs habitat protection.'),
        ('Protected areas automatically protect biodiversity.', 'Many are "paper parks" with little enforcement; poaching, encroachment and climate change can still cause losses.')],
  apply=[('Suggest four features of a well-designed protected area.', 'Large area; compact (circular) shape; corridors to other reserves; buffer zone of sustainable use around a strictly protected core; inclusion of a range of habitats; few roads; local community involvement.', 4),
         ('Describe how the UNESCO biosphere reserve model is organised.', 'A strictly protected core area, surrounded by a buffer zone for research, education and low-impact activities, and an outer transition zone where sustainable settlement and economic activity are allowed.', 3)],
  cases=[('the Mesoamerican Biological Corridor', 'launched in 1997, it aims to link protected areas from southern Mexico to Panama to allow species such as jaguars to move', 'wildlife corridors in protected-area design', 'connecting fragments maintains gene flow and range movement across countries'),
         ('the kākāpō recovery programme, New Zealand', 'by moving all birds to predator-free islands and intensive management, numbers rose from 51 in 1995 to about 250 by 2024', 'species-based conservation', 'intensive, single-species management removed predation and boosted breeding of a flightless parrot'),
         ('the Great Barrier Reef Marine Park rezoning (2004)', 'no-take zones were increased from about 5% to 33% of the park', 'habitat-based conservation in a marine protected area', 'protecting a third of the reef from fishing increased fish biomass in no-take zones and supported reef resilience')],
  evaluate=[('Species-based conservation is less effective than habitat-based conservation.', ['habitat protection benefits whole communities', 'species programmes are costly per species', 'without habitat, species cannot be reintroduced'], ['flagship species attract funding that protects habitats', 'some species need targeted action (kākāpō, Arabian oryx)', 'captive breeding prevents immediate extinction'], 'Habitat-based conservation is generally more effective, but species-based measures are vital for critically low populations; an integrated approach is best.'),
            ('The "30 by 30" target is the best way to halt biodiversity loss.', ['clear, measurable target', 'protects ecosystems and carbon'], ['quality and management matter more than area', 'risks displacing Indigenous peoples', 'does not tackle drivers such as consumption and climate change'], 'Expanding protected areas is necessary but not sufficient; effective, equitable management and reduced drivers are also needed.')],
  extended=[('Evaluate the design and management of a named protected area. [9]', 'e.g. Yellowstone, Great Barrier Reef, Serengeti, Kakadu: size, shape, corridors, buffer zones, zoning, community involvement, funding, enforcement, threats (climate change, tourism); judgement.', 9, 'long')],
  res=[('Plan of two proposed reserves of equal area (100 km²): Reserve A is a 10 km × 10 km square; Reserve B is a 50 km × 2 km strip along a river. Edge effects extend 0.5 km.',
        [('Calculate the core area of each reserve and identify the better design.', 'A: (10 − 1)² = 81 km²; B: (50 − 1) × (2 − 1) = 49 km²; A has more core habitat.'),
         ('Suggest one advantage of Reserve B despite its shape.', 'It follows the river, acting as a corridor and including riparian habitat and an environmental gradient; it may connect other reserves.')])])

S('ch09-st4',
  terms=[('rewilding', 'a large-scale form of restoration that aims to reinstate natural processes and missing species (often keystone species) so that ecosystems become self-sustaining'),
         ('ecological restoration', 'the process of assisting the recovery of an ecosystem that has been degraded, damaged or destroyed'),
         ('CITES', 'the Convention on International Trade in Endangered Species of Wild Fauna and Flora (1973), which regulates international trade in listed species through Appendices I-III'),
         ('Convention on Biological Diversity (CBD)', 'the 1992 treaty opened at the Rio Earth Summit aiming at the conservation of biodiversity, sustainable use and fair sharing of benefits from genetic resources'),
         ('trophic cascade', 'a series of changes in a food web caused by the addition or removal of a top predator')],
  facts=[('Which CITES appendix bans commercial international trade in a species?', 'Appendix I', ['Appendix II', 'Appendix III', 'Appendix IV'], 'Appendix II allows controlled trade with permits.'),
         ('In which year did CITES enter into force?', '1975', ['1962', '1992', '2015'], 'It was agreed in 1973 in Washington DC.'),
         ('Which reintroduction is often cited as causing a trophic cascade in Yellowstone National Park?', 'Grey wolves (1995)', ['Bison (1902)', 'Brown trout (1890)', 'Grizzly bears (2000)'], 'Reduced elk browsing allowed willow and aspen to recover in some areas.'),
         ('Which large-scale rewilding project in the Netherlands used Konik horses and Heck cattle?', 'Oostvaardersplassen', ['Knepp Estate', 'Yellowstone', 'Białowieża'], 'Animal numbers crashed in harsh winters, raising welfare controversy.')],
  why=[('Explain why reintroducing a keystone predator can restore an ecosystem.', 'The predator controls herbivore numbers and behaviour, reducing overgrazing; vegetation recovers, stabilising riverbanks and providing habitat for birds, beavers and insects - a trophic cascade.'),
       ('Explain why CITES is not always effective in protecting species.', 'It controls only international trade, not habitat loss or domestic trade; enforcement depends on national customs and police; illegal trade continues where demand and prices are high (rhino horn, pangolin scales); some countries enter reservations.'),
       ('Explain why rewilding is controversial with some farmers and landowners.', 'Fears of predation on livestock (wolves, lynx), loss of farmland and income, changes to traditional landscapes and cultural identity, and lack of consultation.')],
  contrast=[('rewilding', 'ecological restoration', 'Ecological restoration aims to return a degraded site towards a specific past state with active management; rewilding restores natural processes and missing species at large scale, then minimises intervention.'),
            ('CITES', 'the Convention on Biological Diversity', 'CITES regulates international trade in listed species; the CBD is a broader treaty on conserving all biodiversity, sustainable use and benefit sharing, with targets such as the Kunming-Montreal framework.')],
  misc=[('Rewilding means abandoning land and doing nothing.', 'Rewilding often involves active steps - reintroducing species, removing drainage or fences - before stepping back to let processes operate.'),
        ('CITES bans all trade in endangered species.', 'Only Appendix I species have commercial trade banned; Appendix II species can be traded with permits.')],
  apply=[('Outline how beaver reintroduction can benefit biodiversity and reduce flood risk.', 'Beaver dams create wetlands and ponds that store water, slow peak flows and reduce downstream flooding, trap sediment and create habitat for amphibians, invertebrates and fish (e.g. Devon beaver trial).', 3),
         ('Suggest two indicators that could be used to judge the success of a rewilding project.', 'Increase in species richness or populations of target species (e.g. turtle doves, nightingales at Knepp); recovery of vegetation structure; restoration of natural processes (flooding, grazing); visitor numbers and income.', 2)],
  cases=[('the Knepp Estate, West Sussex', 'since 2001, 1,400 ha of intensive farmland were rewilded with free-roaming longhorn cattle, Exmoor ponies, Tamworth pigs and deer; nightingales, purple emperor butterflies and turtle doves have increased', 'rewilding through natural processes', 'grazing animals act as proxies for extinct herbivores, creating a mosaic of scrub and grassland that supports high biodiversity'),
         ('the ivory trade and CITES', 'African elephants were moved to Appendix I in 1989; poaching fell, but rose again after one-off ivory sales in 1999 and 2008, with about 100,000 elephants killed in 2010-2012', 'the strengths and limitations of international conventions', 'trade bans reduce legal markets, but enforcement and demand reduction are also needed'),
         ('the restoration of the Loess Plateau, China', 'from 1994, terracing, tree planting and grazing bans on about 35,000 km² reduced sediment entering the Yellow River and raised incomes', 'large-scale ecological restoration', 'restoration of vegetation reduced erosion and improved livelihoods, showing that restoration can deliver both social and ecological benefits')],
  evaluate=[('Rewilding is the most effective strategy for restoring biodiversity in Europe.', ['restores natural processes cheaply after initial phase', 'large biodiversity gains (Knepp)', 'reconnects people with nature'], ['conflict with farmers and food production', 'welfare problems (Oostvaardersplassen)', 'requires large areas'], 'Rewilding can deliver large gains where land is available, but must be combined with sustainable farming and conventional protected areas.'),
            ('International conventions such as CITES have been successful in protecting endangered species.', ['near-universal membership (184 parties)', 'reduced trade in many species'], ['illegal trade worth billions continues', 'does not address habitat loss', 'weak enforcement'], 'CITES has prevented some overexploitation but cannot succeed alone; national enforcement and demand reduction are essential.')],
  extended=[('Discuss the effectiveness of rewilding projects in restoring ecosystems, with reference to named examples. [9]', 'Yellowstone wolves (debated trophic cascade), Knepp, beavers in Scotland and Devon, Oostvaardersplassen, Iberian lynx recovery; benefits, conflicts, scale, monitoring; judgement.', 9, 'long')],
  res=[('Knepp Estate monitoring (approximate): breeding pairs of turtle doves - 2005: 0; 2014: 11; 2018: 16; nightingale singing males - 2001: 0; 2012: 34; 2020: 42.',
        [('Calculate the mean annual increase in nightingale singing males between 2001 and 2020.', '42 / 19 ≈ 2.2 males per year.'),
         ('Suggest why scrub development during rewilding benefits these species.', 'Thorny scrub provides nesting cover and insect food; nightingales and turtle doves are declining nationally due to loss of scrub and hedgerows on intensive farms.')])])


# =============================================================================================
# ch10 4.1 Water systems; 4.2 Water access, use and security
# =============================================================================================
S('ch10-st1', gens=['water_balance'],
  terms=[('hydrological cycle', 'the system of storages and flows by which water circulates between the oceans, atmosphere, land and living things, driven by solar energy and gravity'),
         ('evapotranspiration', 'the combined loss of water to the atmosphere by evaporation from surfaces and transpiration from plants'),
         ('infiltration', 'the movement of water from the ground surface into the soil'),
         ('surface runoff (overland flow)', 'the flow of water over the ground surface when rainfall exceeds the infiltration capacity or the soil is saturated'),
         ('residence time', 'the average time a water molecule spends in a storage, e.g. about 9 days in the atmosphere and over 3,000 years in the oceans'),
         ('aquifer', 'a body of permeable rock that can store and transmit groundwater')],
  facts=[('What proportion of Earth\'s water is fresh water?', 'About 2.5%', ['About 25%', 'About 50%', 'About 0.01%'], 'Most fresh water is locked in ice caps and glaciers (about 69%) and groundwater (about 30%).'),
         ('Which is the largest storage of fresh water?', 'Ice caps and glaciers', ['Lakes', 'Rivers', 'The atmosphere'], 'Antarctica alone holds about 60% of the world\'s fresh water.'),
         ('Which processes drive the hydrological cycle?', 'Solar radiation and gravity', ['Earth\'s magnetism', 'Plate movements only', 'Tides'], 'Solar energy evaporates water; gravity returns it as precipitation and runoff.'),
         ('Which of the following is a transformation in the hydrological cycle?', 'Condensation', ['Advection of water vapour', 'Throughflow', 'Surface runoff'], 'Condensation changes state from vapour to liquid.')],
  why=[('Explain how urbanisation affects the hydrological cycle.', 'Impermeable surfaces (concrete, tarmac) reduce infiltration and groundwater recharge, increase surface runoff and peak discharge, shorten lag times and increase flood risk; less vegetation reduces evapotranspiration.'),
       ('Explain why the residence time of water in the atmosphere is short while in the oceans it is long.', 'The atmosphere stores a tiny volume (about 13,000 km³) relative to the large flows of evaporation and precipitation (about 500,000 km³/yr), so turnover is fast (~9 days); the oceans store about 1.3 billion km³ so turnover takes thousands of years.'),
       ('Explain how deforestation can change the hydrological cycle of a region.', 'Less interception and transpiration reduce atmospheric moisture and local rainfall; more runoff and soil erosion; faster flood peaks; in the Amazon, about a third to half of rainfall is recycled by forest transpiration.')],
  contrast=[('infiltration', 'percolation', 'Infiltration is water entering the soil from the surface; percolation is the deeper movement of water from the soil into underlying rock to become groundwater.'),
            ('a transfer', 'a transformation in the hydrological cycle', 'A transfer moves water without change of state (runoff, throughflow, advection); a transformation changes state (evaporation, condensation, freezing).')],
  misc=[('Groundwater is a renewable resource everywhere.', 'Fossil groundwater (e.g. the Nubian Sandstone Aquifer) recharges extremely slowly and is effectively non-renewable.'),
        ('Most fresh water on Earth is in lakes and rivers.', 'Lakes and rivers hold well under 1% of fresh water; most is in ice and groundwater.')],
  apply=[('Describe the inputs, storages, flows and outputs of a drainage basin.', 'Input: precipitation; storages: interception, surface, soil water, groundwater, channel; flows: throughfall, stemflow, infiltration, percolation, overland flow, throughflow, baseflow; outputs: evapotranspiration, river discharge.', 4),
         ('Suggest two ways in which melting glaciers could affect communities that depend on rivers such as the Indus.', 'Short term: higher summer flows and glacial-lake outburst floods; long term: reduced dry-season flows once glaciers shrink ("peak water"), threatening irrigation and hydropower.', 2)],
  cases=[('the Amazon "flying rivers"', 'forest transpiration recycles moisture that is carried west and south, supplying rainfall to farmland in southern Brazil and Argentina', 'the role of vegetation in the hydrological cycle', 'evapotranspiration is a major flow returning water to the atmosphere, so deforestation can reduce rainfall far away'),
         ('Himalayan glaciers and the Indus basin', 'glacier and snowmelt contribute about 40-60% of the Indus flow, supporting irrigation for over 200 million people', 'glaciers as freshwater storages', 'ice stores water in winter and releases it in summer; shrinking glaciers will reduce long-term flows')],
  evaluate=[('Human activity now has a greater influence on the hydrological cycle than natural processes in many drainage basins.', ['dams store huge volumes (Three Gorges)', 'groundwater abstraction lowers water tables', 'urbanisation changes runoff'], ['climate and precipitation remain the main drivers', 'remote basins are little modified'], 'In heavily developed basins human influence is dominant locally, but natural climate drivers still control the global cycle.')],
  extended=[('Explain how storages and flows in the hydrological cycle are affected by two named human activities. [7]', 'Deforestation (Amazon), urbanisation, dams (Three Gorges), irrigation (Aral Sea), groundwater abstraction (Ogallala); changes to evapotranspiration, infiltration, runoff, storages.', 7, 'explain')],
  res=[('Global water stores (km³, approximate): oceans 1,338,000,000; ice caps and glaciers 24,064,000; groundwater 23,400,000; lakes 176,400; soil moisture 16,500; atmosphere 12,900; rivers 2,120.',
        [('Calculate the percentage of all water stored in the oceans.', 'Total ≈ 1,385,672,000 km³; oceans 1,338,000,000/1,385,672,000 × 100 ≈ 96.6%.'),
         ('Given that about 505,000 km³ of water evaporates each year, calculate the residence time of water in the atmosphere in days.', '12,900 / 505,000 = 0.0255 yr × 365 ≈ 9.3 days.')])])

S('ch10-st2',
  terms=[('ocean conveyor belt', 'the global thermohaline circulation that moves water, heat and nutrients around the world\'s oceans over about 1,000 years'),
         ('thermohaline circulation', 'deep ocean circulation driven by differences in density caused by temperature (thermo) and salinity (haline)'),
         ('upwelling', 'the rising of cold, dense, nutrient-rich water from depth to the surface, often along western coasts of continents where winds push surface water offshore'),
         ('El Niño', 'a periodic warming of the eastern tropical Pacific when trade winds weaken, suppressing upwelling off South America and altering global weather'),
         ('gyre', 'a large system of circulating surface ocean currents driven by wind and the Coriolis effect, e.g. the North Pacific Gyre')],
  facts=[('Where does deep water form in the North Atlantic to drive thermohaline circulation?', 'Near Greenland and the Labrador and Nordic Seas', ['Off the coast of Peru', 'In the Mediterranean only', 'At the equator'], 'Cold, salty water sinks there.'),
         ('Why does upwelling increase productivity?', 'It brings nutrient-rich water to the sunlit surface', ['It warms surface water', 'It reduces light', 'It adds fresh water'], 'Nitrate and phosphate are often limiting at the surface.'),
         ('Which effect of El Niño has the greatest impact on the Peruvian anchoveta fishery?', 'Warm water suppresses upwelling, reducing plankton', ['Cold water increases nutrients', 'Increased salinity kills fish', 'Sea ice blocks fishing boats'], 'The 1972-73 El Niño contributed to a collapse of the fishery.'),
         ('Which current keeps north-west Europe several degrees warmer than other places at similar latitudes?', 'The Gulf Stream / North Atlantic Drift', ['The Humboldt Current', 'The California Current', 'The Benguela Current'], 'It transports heat from the tropics.')],
  why=[('Explain how thermohaline circulation redistributes heat.', 'Warm surface currents carry heat poleward (Gulf Stream); at high latitudes water cools, becomes saltier as sea ice forms, sinks and returns towards the equator at depth, so the system transports heat from the tropics to high latitudes.'),
       ('Explain why melting Greenland ice could weaken the Atlantic Meridional Overturning Circulation (AMOC).', 'Fresh meltwater reduces surface salinity and density in the North Atlantic, so less water sinks; this slows the circulation, potentially cooling Europe and shifting rainfall belts - a possible tipping point.'),
       ('Explain why the western coasts of continents in the tropics often have rich fisheries but dry climates.', 'Trade winds push surface water offshore, causing upwelling of cold, nutrient-rich water (high productivity); cold water cools air, creating stable conditions and little rain (e.g. Peru and the Atacama, Namibia).')],
  contrast=[('surface ocean currents', 'deep ocean currents', 'Surface currents are driven mainly by wind and the Coriolis effect and move warm or cold water in gyres; deep currents are driven by density differences (temperature and salinity) and move slowly in the thermohaline conveyor.'),
            ('El Niño', 'La Niña', 'In El Niño trade winds weaken, warm water spreads east and upwelling off Peru weakens; in La Niña trade winds strengthen, upwelling intensifies and the eastern Pacific is cooler than normal.')],
  misc=[('Ocean currents only move water near the surface.', 'Thermohaline circulation moves deep water throughout the ocean basins, taking about 1,000 years to complete a circuit.'),
        ('Upwelling zones are found mainly in the middle of oceans.', 'Major upwellings occur along western continental coasts (Peru, California, Canary, Benguela) and around Antarctica.')],
  apply=[('Suggest why the Benguela upwelling off Namibia supports large fisheries for pilchards and hake.', 'The south-east trade winds cause offshore movement of surface water and upwelling of cold, nitrate-rich water, supporting high phytoplankton productivity at the base of the food web.', 3),
         ('Outline two effects of a strong El Niño on people and ecosystems.', 'e.g. collapse of anchoveta catches in Peru; floods in Peru and Ecuador; droughts in Indonesia and Australia (forest fires in 1997-98); global coral bleaching.', 2)],
  cases=[('the Peruvian anchoveta fishery and El Niño', 'catches fell from about 12 million t in 1970 to under 2 million t in 1973 after the 1972-73 El Niño combined with overfishing', 'the dependence of productivity on upwelling', 'warm El Niño water suppressed upwelling of nutrients, cutting plankton and fish numbers, while heavy fishing removed the remaining stock'),
         ('the weakening AMOC', 'studies suggest the AMOC is at its weakest in over 1,000 years, partly due to Greenland meltwater', 'thermohaline circulation as a potential tipping point', 'freshening of North Atlantic surface water reduces sinking and could cause abrupt regional climate change')],
  evaluate=[('Changes in ocean circulation pose a greater threat to human societies than sea-level rise.', ['AMOC collapse could cool Europe and disrupt monsoons', 'fisheries depend on upwelling'], ['sea-level rise is certain and already affecting coastal cities and islands', 'AMOC collapse is uncertain this century'], 'Sea-level rise is the more certain threat, while circulation changes are a lower-probability but high-impact risk.')],
  extended=[('Explain how ocean circulation influences climate and the productivity of marine ecosystems. [7]', 'Surface currents and heat transport (Gulf Stream); thermohaline circulation; upwelling and nutrients (Peru, Benguela); El Niño impacts; climate change effects on AMOC.', 7, 'explain')],
  res=[('Data: Peruvian anchoveta landings (million tonnes, approximate) - 1970: 12.3; 1972: 4.7; 1973: 1.7; 1983 (El Niño year): 0.1; 1994: 9.8; 1998 (El Niño year): 1.2.',
        [('Calculate the percentage fall in landings between 1970 and 1973.', '(12.3 − 1.7)/12.3 × 100 ≈ 86%.'),
         ('Explain why landings fell sharply in El Niño years.', 'Weaker trade winds reduce upwelling; warm, nutrient-poor water lowers phytoplankton productivity; anchoveta move deeper or south or die, so catches fall.')])])

S('ch10-st3', gens=['water_stress'],
  terms=[('water security', 'access to sufficient, safe, affordable water to satisfy needs for drinking, sanitation, food production and ecosystems'),
         ('physical water scarcity', 'a situation where water resources are insufficient to meet demand, typically in arid regions'),
         ('economic water scarcity', 'a situation where water is available but people lack the investment, infrastructure or money to access it'),
         ('water stress', 'a situation where demand for water exceeds the available amount during a certain period, often defined as below 1,700 m³ per person per year'),
         ('transboundary water', 'a river, lake or aquifer shared by two or more countries, such as the Nile or the Mekong')],
  facts=[('Approximately what share of global freshwater withdrawals is used by agriculture?', 'About 70%', ['About 10%', 'About 30%', 'About 95%'], 'Industry uses about 19% and municipal/domestic about 11%.'),
         ('According to WHO/UNICEF (2022), about how many people lacked safely managed drinking water?', 'About 2.2 billion', ['About 50 million', 'About 500 million', 'About 6 billion'], 'About 3.5 billion lacked safely managed sanitation.'),
         ('Cape Town\'s "Day Zero" crisis in 2018 was averted mainly by:', 'severe restrictions limiting residents to 50 litres per person per day and tariff increases', ['building a new dam in three months', 'importing water by ship', 'cloud seeding'], 'Demand roughly halved from 2015 levels.'),
         ('Which Grand Ethiopian Renaissance Dam (GERD) issue has caused tension with Egypt?', 'Egypt fears reduced Nile flow during reservoir filling', ['The dam floods Cairo', 'Ethiopia is a downstream state', 'The dam produces no electricity'], 'Egypt relies on the Nile for about 90% of its fresh water.')],
  why=[('Explain why economic water scarcity is common in sub-Saharan Africa.', 'Many countries have adequate rainfall or rivers, but lack investment in dams, pipes, wells and treatment; poverty and governance limit access, so people (often women and girls) walk long distances to collect water.'),
       ('Explain why transboundary rivers can lead to conflict.', 'Upstream countries can dam or divert water, reducing flow, quality and sediment downstream; demand is rising with population and irrigation; treaties may be outdated or exclude some states (e.g. 1959 Nile Agreement excluded Ethiopia).'),
       ('Explain how climate change threatens water security.', 'Changes in precipitation patterns, more intense droughts, faster evaporation, shrinking glaciers and snowpacks, and sea-level rise causing salinisation of coastal aquifers.')],
  contrast=[('physical water scarcity', 'economic water scarcity', 'Physical scarcity means there is not enough water to meet demand (e.g. the Middle East, Arizona); economic scarcity means water exists but people cannot access it due to lack of investment or money (e.g. much of sub-Saharan Africa).'),
            ('water withdrawal', 'water consumption', 'Withdrawal is water taken from a source (some returned, e.g. cooling water); consumption is water used and not returned to the source, e.g. lost by evapotranspiration from irrigated crops.')],
  misc=[('Water scarcity only affects desert countries.', 'Economic scarcity affects many wetter countries; seasonal scarcity, pollution and over-abstraction affect cities like Chennai, London and Mexico City.'),
        ('Domestic use is the largest use of fresh water globally.', 'Agriculture (about 70%) is the largest; domestic use is about 11%.')],
  apply=[('Suggest three reasons why water demand is increasing globally.', 'Population growth; urbanisation and rising living standards (more showers, appliances); dietary change to meat and dairy; industrial growth; irrigation expansion; energy production.', 3),
         ('Outline how Israel has increased its water security.', 'Large-scale desalination (Sorek, Ashkelon - about 70-80% of domestic water); recycling about 85-90% of wastewater for irrigation; drip irrigation (Netafim); pricing and leak control.', 3)],
  cases=[('Cape Town\'s 2018 water crisis', 'after three years of drought, dam storage fell to about 20%; restrictions to 50 L per person per day and higher tariffs cut demand by about half and avoided "Day Zero"', 'demand management for water security', 'rapid behavioural change and pricing reduced demand faster than new supply could be built'),
         ('the Grand Ethiopian Renaissance Dam', 'Ethiopia began filling the 74 km³ reservoir on the Blue Nile in 2020 to generate about 5 GW of electricity', 'transboundary water conflict', 'an upstream state\'s development of a shared river raised fears of reduced flow in downstream Sudan and Egypt'),
         ('Chennai, India (2019)', 'the city\'s four main reservoirs ran almost dry, and water was brought by train from 200 km away', 'the impact of urban growth and poor management on water security', 'rapid urbanisation over wetlands and lakes, groundwater depletion and a failed monsoon combined to cause a crisis')],
  evaluate=[('Water scarcity is more a problem of management than of physical shortage.', ['economic scarcity affects many', 'leakage and inefficient irrigation waste large volumes', 'Cape Town and Singapore show management works'], ['some regions are genuinely arid (Middle East)', 'climate change reduces supply', 'population growth increases demand'], 'In most places management and investment are the main issues, though physical limits are real in arid regions and worsening with climate change.')],
  extended=[('Evaluate strategies used to resolve water conflicts over a named transboundary river. [9]', 'Nile (1959 agreement, Nile Basin Initiative, GERD negotiations), Mekong River Commission, Indus Waters Treaty (1960); cooperation, data sharing, benefit sharing; weaknesses; judgement.', 9, 'long')],
  res=[('Global freshwater withdrawal by sector (%) - world: agriculture 70, industry 19, domestic 11; high-income countries: agriculture 41, industry 42, domestic 17; low-income countries: agriculture 90, industry 2, domestic 8.',
        [('Compare the pattern of water use in high- and low-income countries.', 'Low-income countries use 90% for agriculture vs 41% in high-income; high-income countries use far more for industry (42% vs 2%) and somewhat more for domestic use.'),
         ('Suggest reasons for the differences.', 'Low-income economies depend on irrigated subsistence and commercial farming; high-income countries have large industrial and energy sectors (power-station cooling) and more domestic appliances.')])])

S('ch10-st4', gens=['water_footprint'],
  terms=[('water footprint', 'the total volume of fresh water used to produce the goods and services consumed by an individual, community or country'),
         ('virtual water', 'the water embedded in a product - the volume used to produce it - which is effectively traded when the product is exported'),
         ('green water', 'rainwater stored in soil and used by plants, part of a water footprint'),
         ('blue water', 'surface water and groundwater withdrawn for irrigation, industry or domestic use'),
         ('grey water footprint', 'the volume of fresh water needed to dilute pollutants to meet water-quality standards'),
         ('desalination', 'the removal of salt from seawater or brackish water to produce fresh water, usually by reverse osmosis')],
  facts=[('About how much water does it take to produce 1 kg of beef (global average)?', 'About 15,000 litres', ['About 150 litres', 'About 1,500 litres', 'About 150,000 litres'], 'Water Footprint Network: 15,415 L/kg.'),
         ('Which country recycles about 85-90% of its wastewater, mainly for agriculture?', 'Israel', ['Canada', 'Norway', 'Brazil'], 'Treated effluent irrigates crops in the Negev.'),
         ('Singapore\'s NEWater programme produces drinking-quality water by:', 'microfiltration, reverse osmosis and UV treatment of used water', ['importing water by tanker', 'melting icebergs', 'cloud seeding'], 'It can meet up to about 40% of demand.'),
         ('What is the main environmental disadvantage of desalination?', 'High energy use and discharge of concentrated brine', ['It produces salty water', 'It reduces rainfall', 'It uses large areas of farmland'], 'Brine can harm seabed ecosystems.')],
  why=[('Explain why the water footprint of a country can be much larger than its domestic water use.', 'Most water is embedded in imported food, clothing and goods (virtual water); e.g. much of the UK\'s water footprint lies abroad in cotton, coffee and food production.'),
       ('Explain how drip irrigation improves the sustainability of water use.', 'Water is delivered directly to roots through pipes, reducing evaporation and runoff; efficiency can be about 90% compared with about 50-60% for flood irrigation, so more crop per drop.'),
       ('Explain why water pricing can encourage sustainable water management.', 'Charging for water (and metering) reflects scarcity, encourages users to reduce waste and fix leaks, and funds infrastructure; tiered tariffs can protect basic needs for the poor.')],
  contrast=[('green water', 'blue water', 'Green water is rainwater held in soil and used by crops (no abstraction); blue water is withdrawn from rivers, lakes or aquifers, often for irrigation, and competes with other uses.'),
            ('supply-side strategies', 'demand-side strategies', 'Supply-side strategies increase water available (dams, desalination, transfers, recycling); demand-side strategies reduce use (pricing, metering, efficient appliances, drip irrigation, education).')],
  misc=[('Desalination is a sustainable solution for all water-scarce countries.', 'It is expensive and energy-intensive, produces brine and is mainly practical for wealthy coastal states; inland and low-income areas need other strategies.'),
        ('A product with a large water footprint always harms water resources.', 'The impact depends on whether the water is green or blue and whether the source region is water-stressed.')],
  apply=[('Suggest four ways a household could reduce its water footprint.', 'Eat less meat and dairy; buy fewer new clothes (cotton); fix leaks and install low-flow fittings; shorter showers; collect rainwater for gardens; reduce food waste.', 4),
         ('Outline Singapore\'s "Four National Taps" strategy.', 'Local catchment water (reservoirs, e.g. Marina Barrage), imported water from Malaysia, NEWater (recycled wastewater) and desalinated water, plus demand management.', 4)],
  cases=[('Singapore\'s Four National Taps', 'Singapore combines local catchments covering two-thirds of its land, imports from Johor, NEWater (up to ~40% of demand) and desalination (up to ~25%)', 'integrated sustainable water management', 'diversifying supply and recycling reduces dependence on imports and increases water security'),
         ('the Murray-Darling Basin Plan, Australia (2012)', 'the plan aimed to return about 2,750 GL a year from irrigation to the environment through buy-backs and efficiency projects', 'balancing water use between people and ecosystems', 'capping and trading water rights reallocated water to restore wetlands and river health, though disputes over farmers\' livelihoods continue')],
  evaluate=[('Reducing demand is more sustainable than increasing supply as a strategy for water security.', ['cheaper and lower-impact than dams or desalination', 'Cape Town and Singapore show large savings possible'], ['growing populations need more supply', 'demand cuts have limits for basic needs and food production'], 'Demand management should be the first priority, supplemented by low-impact supply options such as recycling.'),
            ('The water footprint is a useful tool for consumers.', ['raises awareness of hidden water use', 'allows comparison of products and diets'], ['ignores local scarcity and type of water', 'complex to calculate; global averages mislead'], 'It is a useful awareness tool if interpreted with information about where and how water is used.')],
  extended=[('Evaluate the sustainability of two named strategies for managing water resources. [9]', 'e.g. desalination (Sorek, Israel), wastewater recycling (NEWater), drip irrigation, dams (Three Gorges, GERD), water pricing; environmental, social and economic criteria; judgement.', 9, 'long')],
  res=[('Water footprint of selected products (litres, Water Footprint Network): 1 kg beef 15,415; 1 kg chicken 4,325; 1 kg rice 2,497; 1 cotton T-shirt about 2,700; 1 cup of coffee 140; 1 kg tomatoes 214.',
        [('Calculate the water saved per year if a person replaced 2 kg of beef per month with 2 kg of chicken.', '(15,415 − 4,325) × 2 × 12 = 266,160 L per year.'),
         ('Suggest why the footprint of rice varies greatly between countries.', 'Differences in climate (evapotranspiration), irrigation method and efficiency, yields and the proportion of rain-fed (green) water.')])])


# =============================================================================================
# ch11 4.3 Aquatic food production systems
# =============================================================================================
S('ch11-st1',
  terms=[('aquatic food production', 'the harvesting of fish, shellfish and algae from oceans and fresh water by capture fisheries or aquaculture'),
         ('continental shelf', 'the shallow, gently sloping seabed around continents (usually < 200 m deep) where light and nutrients support high productivity and most fisheries'),
         ('photic zone', 'the upper layer of a water body where there is enough light for photosynthesis, usually down to about 200 m'),
         ('phytoplankton', 'microscopic photosynthetic organisms that are the main producers in aquatic ecosystems'),
         ('estuary', 'the tidal mouth of a river where fresh and salt water mix, often with very high productivity')],
  facts=[('Which marine ecosystems have the highest NPP per unit area?', 'Coral reefs, estuaries and kelp forests', ['The open ocean', 'The deep-sea floor', 'Polar sea ice'], 'Estuaries and reefs reach about 1,500-2,500 g m⁻² yr⁻¹; the open ocean about 125.'),
         ('Why is the open ocean often described as a "marine desert"?', 'Nutrients are scarce in the sunlit surface layer', ['There is no light', 'It is too salty for life', 'Temperatures are too high'], 'Nutrients sink below the photic zone.'),
         ('About what share of the world\'s animal protein intake comes from aquatic foods?', 'About 15-17%', ['About 1%', 'About 50%', 'About 90%'], 'For over 3 billion people fish provides at least 20% of animal protein.'),
         ('In 2022, aquaculture production of aquatic animals:', 'exceeded capture fisheries for the first time', ['fell to zero', 'was less than 5% of total', 'was banned by the FAO'], 'FAO SOFIA 2024: aquaculture 51% of aquatic animal production.')],
  why=[('Explain why most of the world\'s fisheries are on continental shelves.', 'Shallow water lies within the photic zone, nutrients from rivers and upwelling are abundant, and mixing keeps nutrients near the surface, so primary productivity and fish stocks are high.'),
       ('Explain why aquatic food chains are often longer than terrestrial ones.', 'Producers (phytoplankton) are tiny, so several levels of small consumers (zooplankton, small fish) are needed before large fish; energy transfer efficiency in some aquatic systems is also slightly higher.'),
       ('Explain why harvesting at lower trophic levels is more efficient.', 'Less energy has been lost through respiration in earlier transfers, so more biomass is available per unit of primary production; e.g. farming seaweed or mussels rather than tuna.')],
  contrast=[('freshwater ecosystems', 'marine ecosystems', 'Freshwater ecosystems (lakes, rivers, wetlands) have low salinity and are small and often nutrient-rich; marine ecosystems are saline, cover about 71% of Earth\'s surface and are mostly nutrient-poor except on shelves and in upwellings.'),
            ('capture fisheries', 'aquaculture', 'Capture fisheries harvest wild stocks; aquaculture farms aquatic organisms in controlled conditions (cages, ponds, rafts).')],
  misc=[('The open ocean is the most productive marine ecosystem per square metre.', 'The open ocean has very low productivity per m² because surface nutrients are scarce; it is large in total only because of its area.'),
        ('Fish are only an important food in coastal countries.', 'Freshwater fisheries (e.g. Mekong, Lake Victoria, Tonlé Sap) supply protein to many inland communities.')],
  apply=[('Suggest why the Mekong River fishery is important for food security in Cambodia.', 'The Tonlé Sap flood pulse supports one of the world\'s largest inland fisheries; fish provide most of the animal protein consumed by Cambodians; dams upstream threaten migration and sediment.', 3),
         ('Explain why mangrove forests are important to coastal fisheries.', 'They act as nurseries for juvenile fish and shrimp, provide shelter and food from leaf litter, filter sediments and protect coasts.', 3)],
  cases=[('the Tonlé Sap lake, Cambodia', 'the Mekong reverses flow in the wet season, expanding the lake about five-fold and supporting a fish catch of several hundred thousand tonnes a year', 'freshwater ecosystem productivity', 'the seasonal flood pulse brings nutrients and floods forests that act as spawning and feeding grounds'),
         ('the Grand Banks of Newfoundland', 'shallow banks where the cold Labrador Current meets the warm Gulf Stream created one of the most productive fishing grounds in the world', 'high productivity on continental shelves', 'mixing of currents brings nutrients into shallow, sunlit water, supporting abundant plankton and cod')],
  evaluate=[('Aquatic ecosystems can supply a much larger share of future food needs.', ['aquaculture is growing fast', 'low-trophic species (seaweed, mussels) are efficient', 'large ocean area'], ['about a third of wild stocks are overfished', 'productivity is concentrated in small areas', 'pollution and climate change reduce productivity'], 'Aquatic food can grow, mainly through sustainable aquaculture of low-trophic species, but wild capture cannot expand much.')],
  extended=[('Explain why productivity differs between named aquatic ecosystems. [7]', 'Light (photic zone), nutrients (upwelling, river input), temperature, mixing; examples: Peruvian upwelling, Grand Banks, coral reefs, open ocean gyres, Tonlé Sap.', 7, 'explain')],
  res=[('FAO data (SOFIA 2024): total fisheries and aquaculture production 2022 - 223 million t; aquatic animals 185 million t, of which capture 91 million t and aquaculture 94 million t; algae 38 million t.',
        [('Calculate the percentage of aquatic animal production from aquaculture.', '94 / 185 × 100 ≈ 51%.'),
         ('Suggest two reasons why aquaculture has grown while wild capture has stayed roughly constant since the 1990s.', 'Wild stocks are fully exploited or overfished; rising demand from population and income growth; aquaculture technology and investment, especially in Asia (China produces over half).')])])

S('ch11-st2', gens=['msy'],
  terms=[('maximum sustainable yield (MSY)', 'the largest catch that can be taken from a stock over an indefinite period without depleting it, theoretically at about half the carrying capacity'),
         ('overfishing', 'harvesting fish faster than the stock can replenish itself, reducing the population below sustainable levels'),
         ('bycatch', 'non-target species (dolphins, turtles, juvenile fish) caught unintentionally during fishing'),
         ('total allowable catch (TAC)', 'a limit set on the total quantity of a species that may be caught in an area during a period'),
         ('individual transferable quota (ITQ)', 'a share of a TAC allocated to a fisher or company that can be bought, sold or leased'),
         ('marine protected area (MPA)', 'an area of sea where human activities such as fishing are restricted to protect ecosystems')],
  facts=[('According to the FAO (SOFIA 2024), about what percentage of assessed marine fish stocks were overfished in 2021?', 'About 38%', ['About 5%', 'About 60%', 'About 90%'], 'The share has risen from about 10% in 1974.'),
         ('Why is MSY reached at about half the carrying capacity in the logistic model?', 'Population growth (surplus) is greatest at K/2', ['Fish stop breeding above K/2', 'Fishing is easiest at K/2', 'K/2 is the minimum viable population'], 'dN/dt = rN(1 − N/K) is maximal at N = K/2.'),
         ('Which practice causes the greatest seabed damage?', 'Bottom trawling', ['Pole-and-line fishing', 'Hand-gathering', 'Purse seining at the surface'], 'Heavy nets and doors are dragged across the seabed.'),
         ('Iceland\'s fisheries are managed mainly through:', 'individual transferable quotas based on scientific advice', ['open access with no limits', 'a total ban on fishing', 'subsidies for fleet expansion'], 'The ITQ system was introduced from the 1980s.')],
  why=[('Explain why the Grand Banks cod stock collapsed in 1992.', 'Advanced technology (factory trawlers, sonar) and quotas set too high on over-optimistic stock estimates removed more fish than were produced; juveniles were caught; the trawling damaged habitat; political pressure delayed action until the stock fell over 95%.'),
       ('Explain why fisheries are an example of the "tragedy of the commons".', 'Fish in open-access waters are a shared resource; each fisher gains from catching more but the cost of depletion is shared by all, so without regulation the stock is over-exploited.'),
       ('Explain why setting quotas at MSY can still lead to overfishing.', 'MSY depends on uncertain estimates of r and K; environmental variation changes recruitment; illegal and unreported catches and discards increase actual mortality; MSY ignores bycatch and ecosystem effects.'),
       ('Explain how no-take marine reserves can increase catches nearby.', 'Protected fish grow larger and produce many more eggs and larvae; adults and larvae spill over into fished areas, increasing catches around the reserve (e.g. Apo Island, Philippines).')],
  contrast=[('maximum sustainable yield', 'optimum sustainable yield', 'MSY is the largest biological catch that can be taken indefinitely; optimum sustainable yield sets catch below MSY to account for economic, social and ecological factors and uncertainty, giving a safety margin.'),
            ('a total allowable catch', 'an individual transferable quota', 'A TAC sets the total catch for a fishery; an ITQ allocates a tradeable share of that TAC to individual fishers, giving them a long-term stake in the stock.')],
  misc=[('A fishery is sustainable as long as fish are still being caught.', 'Catches can continue while the stock declines (fishing down the stock); sustainability requires the catch to be within the stock\'s capacity to replace itself.'),
        ('Fishing exactly at MSY is the safest approach.', 'Because of uncertainty and natural variability, fishing at or above estimated MSY risks decline; a precautionary target below MSY is safer.')],
  apply=[('Suggest four measures that could help a depleted fish stock recover.', 'Reduce TAC below MSY; larger mesh sizes to let juveniles escape; seasonal closures during spawning; no-take MPAs; reduce subsidies and fleet capacity; monitor catches (observers, vessel tracking); bycatch-reduction devices.', 4),
         ('Outline how Norway managed to rebuild the Norwegian spring-spawning herring stock.', 'After collapse in the late 1960s, a near moratorium and strict quotas based on scientific advice allowed recovery by the 1990s; harvest control rules and international agreements now set TACs.', 3)],
  cases=[('the Grand Banks cod collapse', 'catches peaked at about 800,000 t in 1968; by 1992 the spawning stock had fallen by over 95%, and a moratorium closed the fishery', 'the consequences of fishing beyond MSY', 'overfishing removed the breeding stock, and the ecosystem shifted (more shrimp and crab), so recovery has been very slow'),
         ('Apo Island marine reserve, Philippines', 'a community-managed no-take reserve created in 1982 led to large increases in fish biomass inside the reserve and higher catches nearby', 'marine protected areas in fisheries management', 'protected fish grew and reproduced, spilling over into fished areas and benefiting local fishers'),
         ('the Patagonian toothfish fishery', 'heavy illegal fishing in the 1990s was reduced through CCAMLR catch documentation and the MSC certification of some fisheries', 'international cooperation in fisheries management', 'traceability and certification made illegal catch harder to sell, supporting stock recovery')],
  evaluate=[('Marine protected areas are the most effective way to manage fisheries sustainably.', ['spillover increases catches (Apo Island)', 'protect habitats and breeding stock', 'build resilience'], ['many MPAs are poorly enforced', 'fishing effort shifts elsewhere', 'migratory species (tuna) need quotas and international agreements'], 'MPAs are highly effective when enforced and community-supported, but must be combined with catch limits and gear controls.'),
            ('Quotas based on MSY are sufficient to prevent overfishing.', ['science-based limits', 'clear targets'], ['uncertainty and political pressure', 'illegal fishing and discards', 'ecosystem effects ignored'], 'MSY-based quotas are a starting point but must be precautionary and combined with enforcement and ecosystem-based management.')],
  extended=[('Evaluate the strategies used to manage a named fishery. [9]', 'e.g. Grand Banks cod, North Sea herring, Icelandic cod, Peruvian anchoveta: TAC, ITQs, mesh sizes, closures, MPAs, monitoring, certification (MSC); outcomes; judgement.', 9, 'long')],
  res=[('Northern cod (Grand Banks) landings (thousand tonnes, approximate): 1960 - 450; 1968 - 810; 1975 - 290; 1985 - 230; 1991 - 190; 1993 - 10 (moratorium from 1992).',
        [('Calculate the percentage decline in landings from the 1968 peak to 1991.', '(810 − 190)/810 × 100 ≈ 77%.'),
         ('Explain why the stock had not recovered by the 2010s despite the moratorium.', 'The breeding stock was too small; cod mature slowly (6-7 years); ecosystem changes (more predators such as seals, changes in prey such as capelin); some bycatch and recreational fishing continued.')])])

S('ch11-st3', gens=['fcr'],
  terms=[('aquaculture', 'the farming of aquatic organisms such as fish, molluscs, crustaceans and aquatic plants'),
         ('feed conversion ratio (FCR)', 'the mass of feed needed to produce a unit increase in body mass of a farmed animal'),
         ('integrated multi-trophic aquaculture (IMTA)', 'the farming of species from different trophic levels together (e.g. salmon, mussels and seaweed) so that waste from one species is used by another'),
         ('polyculture', 'the farming of several compatible species together, such as different carp species in Chinese ponds'),
         ('mariculture', 'the cultivation of marine organisms in the sea or in seawater, e.g. salmon cages or oyster beds')],
  facts=[('Which country produces over half of the world\'s aquaculture output?', 'China', ['Norway', 'Chile', 'Peru'], 'China leads in carp, shellfish and seaweed farming.'),
         ('Sea lice from salmon farms are a problem because they:', 'spread to and kill wild salmon and sea trout passing nearby', ['improve fish growth', 'clean the water', 'only affect seaweed'], 'Lice loads are high near dense cages.'),
         ('Which type of aquaculture usually has the lowest environmental impact?', 'Farming filter feeders such as mussels and oysters', ['Intensive shrimp ponds in cleared mangroves', 'Carnivorous fish in open sea cages', 'Bluefin tuna ranching'], 'Filter feeders need no feed and remove nutrients.'),
         ('Approximately what share of mangrove loss in some South-East Asian countries has been linked to shrimp farming?', 'Up to about half in some countries', ['Less than 1%', 'All of it', 'None'], 'e.g. large losses in Thailand and Indonesia from the 1980s.')],
  why=[('Explain why the farming of carnivorous fish such as salmon can increase pressure on wild fish stocks.', 'Their feed contains fishmeal and fish oil made from wild forage fish (anchoveta, sand eels); if the fish-in : fish-out ratio exceeds 1, more wild fish are used than farmed fish produced.'),
       ('Explain how integrated multi-trophic aquaculture reduces pollution.', 'Waste nutrients from fed fish are absorbed by seaweed (dissolved N and P) and filtered by shellfish (particles), turning waste into extra products and reducing eutrophication.'),
       ('Explain why aquaculture could improve food security.', 'It produces protein efficiently (low FCR compared with beef), can be carried out close to markets, reduces pressure on wild stocks if feed is sustainable, and provides livelihoods.')],
  contrast=[('extensive aquaculture', 'intensive aquaculture', 'Extensive aquaculture uses natural food and low stocking densities with little input (e.g. traditional carp ponds); intensive aquaculture uses high densities, formulated feeds, aeration and medicines to maximise yield.'),
            ('open-net cage farming', 'recirculating aquaculture systems (RAS)', 'Open-net cages in the sea allow waste, disease and escapes to pass into the environment; RAS are land-based tanks that filter and recycle water, reducing pollution but using more energy.')],
  misc=[('Aquaculture always reduces pressure on wild fish.', 'Farming carnivorous species can increase demand for wild forage fish; escapes and disease can harm wild populations.'),
        ('Aquaculture has no effect on coastal habitats.', 'Shrimp ponds have replaced large areas of mangrove; cages can smother seabeds with waste.')],
  apply=[('Outline three environmental impacts of salmon farming in Norway or Scotland.', 'Sea lice and disease spreading to wild salmon; escaped farmed fish interbreeding with wild fish; waste feed and faeces enriching the seabed; chemicals (antiparasitics); use of wild fish in feed.', 3),
         ('Suggest how an aquaculture project could be made more sustainable.', 'Use IMTA with seaweed and mussels; plant- or insect-based feeds; lower stocking densities; closed containment; site away from wild salmon rivers; ASC certification.', 3)],
  cases=[('shrimp farming in Thailand', 'from the 1980s large areas of mangrove were cleared for shrimp ponds, many of which were abandoned after a few years because of disease and pollution', 'the environmental costs of aquaculture', 'intensive ponds destroyed coastal protection and nursery habitats, leaving degraded land when disease forced abandonment'),
         ('salmon farming in Norway', 'Norway produces about 1.5 million t of farmed salmon a year; sea lice are linked to declines of wild salmon in some fjords', 'impacts of intensive mariculture', 'high densities of farmed fish amplify parasites that spread to wild fish migrating past the cages'),
         ('seaweed and shellfish farming in Sanggou Bay, China', 'integrated culture of kelp, scallops, oysters and fish produces large yields while seaweed absorbs nutrients', 'integrated multi-trophic aquaculture', 'combining trophic levels recycles waste nutrients into marketable products and limits eutrophication')],
  evaluate=[('Aquaculture is the solution to declining wild fish stocks.', ['already supplies over half of aquatic animal food', 'efficient conversion (FCR 1-2)', 'low-trophic species need no feed'], ['carnivorous species depend on wild fish', 'pollution, disease, escapes', 'mangrove loss'], 'Aquaculture can relieve pressure on wild stocks if it focuses on low-trophic species and sustainable feed, but it is not a solution on its own.')],
  extended=[('Discuss the extent to which aquaculture can be considered sustainable. [9]', 'FCR and FIFO, IMTA, Norwegian salmon and sea lice, Thai shrimp and mangroves, Chinese polyculture, certification (ASC), new feeds; environmental, social, economic criteria; judgement.', 9, 'long')],
  res=[('Feed conversion ratios (kg feed per kg live-weight gain, approximate): farmed salmon 1.2-1.4; tilapia 1.5-1.8; chicken 1.7-2.0; pork 2.7-3.0; beef 6-10; mussels 0 (no added feed).',
        [('Using mid-range values, calculate how much more feed is needed to produce 100 kg of beef than 100 kg of salmon.', 'Beef 8 × 100 = 800 kg; salmon 1.3 × 100 = 130 kg; difference 670 kg (about six times more).'),
         ('Explain why fish generally have lower FCRs than land livestock.', 'Fish are ectotherms, so less energy is used maintaining body temperature; water supports their body so less energy is spent on skeleton and movement.')])])


# =============================================================================================
# ch12 4.4 Water pollution
# =============================================================================================
S('ch12-st1',
  terms=[('point-source pollution', 'pollution released from a single, clearly identifiable site, such as a factory pipe or sewage outfall'),
         ('non-point-source pollution', 'pollution released from many dispersed sources, such as fertiliser runoff from farmland or urban runoff'),
         ('organic pollutant', 'a pollutant made of biodegradable material such as sewage, slurry or food waste that increases oxygen demand when decomposed'),
         ('persistent pollutant', 'a pollutant that is not broken down readily and remains in the environment, e.g. mercury, PCBs, microplastics'),
         ('thermal pollution', 'the release of heated water (e.g. from power-station cooling) that reduces dissolved oxygen and harms aquatic life'),
         ('microplastics', 'plastic particles smaller than 5 mm, from fragmentation of larger plastics, synthetic fibres or cosmetics')],
  facts=[('Which is an example of non-point-source pollution?', 'Nitrate runoff from farmland across a catchment', ['Discharge from a paper-mill pipe', 'Effluent from a sewage-works outfall', 'Oil from a single tanker spill'], 'Diffuse sources are harder to regulate.'),
         ('About how much plastic enters the oceans each year?', 'About 8-11 million tonnes', ['About 1,000 tonnes', 'About 100 million tonnes', 'About 1 billion tonnes'], 'UNEP estimates about 11 million t a year.'),
         ('The Great Pacific Garbage Patch is located in:', 'the North Pacific Gyre between Hawaii and California', ['the Southern Ocean', 'the Mediterranean Sea', 'the Gulf of Mexico'], 'Rotating currents concentrate floating debris.'),
         ('Which pollutant from mining caused "itai-itai" disease in Japan?', 'Cadmium', ['Mercury', 'Lead', 'Arsenic'], 'Cadmium from a zinc mine contaminated rice paddies along the Jinzū River.')],
  why=[('Explain why non-point-source pollution is harder to manage than point-source pollution.', 'It comes from many dispersed sources across a catchment, so it is hard to identify who is responsible, measure, regulate or treat; point sources can be monitored and treated at the outlet.'),
       ('Explain why thermal pollution harms aquatic organisms.', 'Warmer water holds less dissolved oxygen while raising the metabolic rate (and oxygen demand) of organisms; sudden temperature changes cause thermal shock and alter breeding cycles.'),
       ('Explain how microplastics can affect marine food chains.', 'They are ingested by zooplankton, shellfish and fish, causing false satiety and gut blockage, and carry adsorbed toxins (POPs) that may bioaccumulate and biomagnify, reaching seafood eaten by humans.')],
  contrast=[('point-source pollution', 'non-point-source pollution', 'Point-source pollution comes from a single identifiable outlet (a pipe), so it is easier to monitor and treat; non-point-source pollution comes from diffuse sources (farmland runoff), so it is harder to control.'),
            ('organic pollution', 'inorganic pollution', 'Organic pollution (sewage, slurry) is biodegradable and raises BOD; inorganic pollution (nitrates, phosphates, heavy metals, acids) is not decomposed in the same way and may cause eutrophication or toxicity.')],
  misc=[('Biodegradable pollutants are harmless.', 'Biodegradable organic waste is decomposed by bacteria that use oxygen, so large amounts deplete dissolved oxygen and can kill fish.'),
        ('Plastic pollution comes mainly from ships.', 'About 80% of ocean plastic is estimated to come from land-based sources via rivers, coasts and poor waste management.')],
  apply=[('Classify each source as point or non-point: (i) a leaking septic tank, (ii) storm runoff from city streets, (iii) a mine drainage adit, (iv) pesticide spray drift over a valley.', '(i) point (ii) non-point (iii) point (iv) non-point.', 4),
         ('Suggest two sources of pollution in a river flowing through a large city and one effect of each.', 'Untreated sewage and combined sewer overflows (raised BOD, pathogens); industrial effluent (heavy metals, toxic to fish); urban runoff with oil and microplastics.', 2)],
  cases=[('the Citarum River, Indonesia', 'often described as one of the world\'s most polluted rivers, it receives effluent from about 2,000 factories (many textile) and household waste', 'point and non-point sources of water pollution', 'industrial pipes (point) and dispersed household and farm waste (non-point) combine, so a 2018 clean-up programme had to address both'),
         ('the Deepwater Horizon oil spill, Gulf of Mexico (2010)', 'about 4.9 million barrels (780 million litres) of oil escaped over 87 days', 'a major point-source pollution event', 'a single source caused widespread contamination of marshes, fisheries and wildlife, leading to tighter offshore drilling rules'),
         ('the Great Pacific Garbage Patch', 'an estimated 80,000 t of plastic is concentrated in the North Pacific Gyre', 'persistent pollution in the oceans', 'non-biodegradable plastics are carried by currents and accumulate, fragmenting into microplastics that enter food chains')],
  evaluate=[('Plastic pollution is the most serious threat to marine ecosystems.', ['highly visible, global, persistent', 'entanglement and ingestion kill marine life'], ['climate change, overfishing and nutrient pollution cause larger ecosystem-wide damage', 'acidification affects entire food webs'], 'Plastic pollution is serious and growing, but overfishing, warming and nutrient pollution currently cause greater ecological damage.')],
  extended=[('Explain the sources and effects of two named types of water pollution. [7]', 'e.g. organic (sewage - BOD, deoxygenation, pathogens), nutrient (eutrophication), heavy metals (Minamata, itai-itai), oil (Deepwater Horizon), plastics, thermal; point vs non-point.', 7, 'explain')],
  res=[('River survey downstream of a town: distance from outfall (km) and dissolved oxygen (mg/L) - 1 km upstream 9.8; 0 km 9.6; 1 km 4.1; 3 km 2.6; 6 km 5.4; 10 km 8.7.',
        [('Describe the oxygen-sag pattern and identify the point of lowest oxygen.', 'DO drops sharply below the outfall to a minimum of 2.6 mg/L at 3 km, then recovers to 8.7 mg/L by 10 km.'),
         ('Explain the recovery of dissolved oxygen downstream.', 'As organic matter is decomposed, BOD falls; reaeration from turbulence and photosynthesis by algae and plants add oxygen; dilution by tributaries.')])])

S('ch12-st2', gens=['nitrate_load'],
  terms=[('eutrophication', 'the process by which water bodies become enriched with nutrients (mainly nitrates and phosphates), leading to excessive growth of algae and plants and oxygen depletion'),
         ('algal bloom', 'a rapid increase in the population of algae or cyanobacteria in a water body, often turning water green and reducing light'),
         ('hypoxia', 'a condition of low dissolved oxygen (often < 2 mg/L) that cannot support most aquatic animals'),
         ('dead zone', 'an area of water so low in oxygen that most marine life cannot survive, e.g. in the Gulf of Mexico or Baltic Sea'),
         ('cultural eutrophication', 'eutrophication accelerated by human activities such as fertiliser use and sewage discharge')],
  facts=[('Which nutrient is usually the limiting factor for algal growth in freshwater lakes?', 'Phosphate', ['Nitrogen gas', 'Carbon dioxide', 'Sodium'], 'In marine systems nitrogen is more often limiting.'),
         ('Why does dissolved oxygen fall during eutrophication?', 'Bacteria decomposing dead algae use oxygen in respiration', ['Algae absorb oxygen in photosynthesis', 'Nutrients react with oxygen', 'Fish produce too much CO₂'], 'Decomposition increases biological oxygen demand.'),
         ('Approximately how many coastal dead zones have been identified worldwide?', 'Over 400', ['About 5', 'About 40', 'Over 50,000'], 'Diaz and Rosenberg (2008) identified over 400 systems.'),
         ('Which is a positive feedback loop in eutrophication?', 'Dead algae decompose, releasing more nutrients that fuel further algal growth', ['Fish eat algae and reduce the bloom', 'Reed beds absorb nutrients', 'Winter cools the lake'], 'Internal loading from sediments can sustain blooms.')],
  why=[('Explain the sequence of events that leads from fertiliser runoff to fish death in a lake.', 'Nitrates and phosphates enter the water → algae grow rapidly (bloom) → light is blocked, submerged plants die → algae die → aerobic bacteria decompose dead matter, using oxygen (high BOD) → dissolved oxygen falls → fish and invertebrates die (positive feedback as more die and decompose).'),
       ('Explain why eutrophication can be described as involving positive feedback.', 'Dead organisms decompose, releasing nutrients and consuming oxygen; low oxygen releases phosphate from sediments (internal loading), fuelling more algal growth and more deaths - the change is amplified.'),
       ('Explain why restoring a eutrophic lake can take many years even after inputs are cut.', 'Phosphorus stored in sediments is released back into the water (internal loading), especially when oxygen is low; the lake may have shifted to an alternative stable state dominated by algae.')],
  contrast=[('natural eutrophication', 'cultural eutrophication', 'Natural eutrophication is a slow ageing process of lakes over centuries as nutrients accumulate; cultural eutrophication is rapid enrichment caused by human inputs of fertiliser, sewage and detergents.'),
            ('an oligotrophic lake', 'a eutrophic lake', 'An oligotrophic lake has low nutrients, clear water, high oxygen and low productivity; a eutrophic lake has high nutrients, frequent algal blooms, murky water and low oxygen at depth.')],
  misc=[('Eutrophication is caused by toxic chemicals poisoning fish.', 'Eutrophication is caused by excess nutrients; fish die mainly from oxygen depletion when algae decompose (though some cyanobacteria produce toxins).'),
        ('Adding more algae-eating fish is the best way to stop eutrophication.', 'The root cause is nutrient input; reducing inputs at source is essential, although biomanipulation can help restore lakes.')],
  apply=[('Suggest three strategies to reduce eutrophication at the stage of nutrient release.', 'Precision fertiliser application and timing; buffer strips and hedges along watercourses; phosphate-free detergents; upgrading sewage works to remove N and P; nitrate vulnerable zones; cover crops.', 3),
         ('Suggest two strategies to restore a lake that is already eutrophic.', 'Dredge phosphate-rich sediments; aerate the bottom water; biomanipulation (remove planktivorous fish to allow zooplankton to graze algae); harvest algae; add aluminium or lanthanum clays to lock up phosphorus.', 2)],
  cases=[('Lake Erie, North America', 'phosphorus inputs caused severe blooms in the 1960s; the 1972 Great Lakes Water Quality Agreement cut phosphorus and the lake recovered, but blooms returned after 2000 and Toledo\'s water supply was shut for 3 days in 2014', 'causes and management of eutrophication', 'controlling point sources (detergents, sewage) worked, but rising non-point farm runoff later re-created the problem'),
         ('the Gulf of Mexico dead zone', 'nutrients from the Mississippi basin create a summer hypoxic zone, about 22,000 km² at its largest (2017)', 'eutrophication in coastal waters', 'fertiliser from Midwest farms stimulates plankton blooms whose decomposition removes oxygen from bottom water'),
         ('Lake Taihu, China (2007)', 'a massive cyanobacterial bloom cut off drinking water for about 2 million people in Wuxi', 'the human consequences of eutrophication', 'industrial, agricultural and domestic nutrient inputs fuelled a toxic bloom that made water undrinkable')],
  evaluate=[('Reducing nutrient inputs at source is the most effective way to manage eutrophication.', ['tackles the root cause', 'Lake Erie recovered after phosphate controls', 'cheaper long term'], ['non-point sources are hard to control', 'internal loading delays recovery so restoration is also needed', 'farmers need incentives'], 'Source reduction is essential and most effective long term, but must be combined with restoration where internal loading is high.')],
  extended=[('Evaluate strategies for managing eutrophication at different stages of the pollution management model. [9]', 'Altering human activity (diet, fertiliser use), controlling release (buffer strips, sewage treatment, P stripping), clean-up and restoration (dredging, biomanipulation); Lake Erie, Baltic HELCOM, Gulf of Mexico; judgement.', 9, 'long')],
  res=[('Lake Erie monitoring (approximate): total phosphorus load (thousand t/yr) - 1968: 28; 1980: 14; 1995: 9; 2011: 11; algal bloom severity index - 1968: 8; 1995: 1; 2011: 10 (record bloom).',
        [('Calculate the percentage reduction in phosphorus load between 1968 and 1995.', '(28 − 9)/28 × 100 ≈ 68%.'),
         ('Suggest why the 2011 bloom was a record even though phosphorus load was lower than in 1968.', 'More of the load was dissolved reactive phosphorus from farm runoff (more bioavailable); warmer water and heavy spring rain favoured cyanobacteria; invasive zebra mussels changed nutrient cycling.')])])

S('ch12-st3', gens=['bod', 'bmwp'],
  terms=[('biochemical oxygen demand (BOD)', 'the amount of dissolved oxygen required by aerobic microorganisms to decompose the organic matter in a sample of water over a set period, usually 5 days at 20 °C'),
         ('dissolved oxygen (DO)', 'the concentration of oxygen gas dissolved in water, usually measured in mg/L'),
         ('indicator species', 'a species whose presence, absence or abundance indicates specific environmental conditions, such as pollution levels'),
         ('biotic index', 'a scale that gives a measure of water quality based on the types and abundance of indicator organisms present, e.g. the BMWP score or Trent Biotic Index'),
         ('turbidity', 'the cloudiness of water caused by suspended particles, measured with a Secchi disk or turbidity meter')],
  facts=[('Which invertebrates indicate clean, well-oxygenated water?', 'Stonefly and mayfly nymphs', ['Sludge worms (Tubifex)', 'Rat-tailed maggots', 'Bloodworms (Chironomus)'], 'These have high BMWP scores.'),
         ('Why is a high BOD a sign of organic pollution?', 'More organic matter means more aerobic decomposers using oxygen', ['Algae produce too much oxygen', 'Fish need more oxygen', 'Cold water holds more oxygen'], 'Sewage and slurry raise BOD.'),
         ('Which device is used to measure water clarity in lakes?', 'A Secchi disk', ['A quadrat', 'A pitfall trap', 'A Tullgren funnel'], 'The depth at which the disk disappears indicates clarity.'),
         ('Why are biotic indices useful alongside chemical tests?', 'Organisms reflect conditions over time, including intermittent pollution', ['They give instant precise concentrations', 'They need no identification skills', 'They measure only temperature'], 'Chemical tests give a snapshot.')],
  why=[('Explain why the presence of mayfly nymphs indicates good water quality.', 'Mayfly nymphs need high dissolved oxygen and are intolerant of organic pollution; their presence shows that oxygen levels have stayed high over the period of their development.'),
       ('Explain why chemical tests and biotic indices should be used together.', 'Chemical tests give precise values of specific pollutants at one moment but can miss intermittent discharges; biotic indices integrate conditions over time but do not identify the pollutant; together they give a fuller picture.'),
       ('Explain why dissolved oxygen is usually lower in summer than in winter in a river.', 'Warmer water holds less oxygen, and decomposition and respiration rates increase with temperature; low summer flows also reduce dilution and reaeration.')],
  contrast=[('BOD', 'dissolved oxygen', 'Dissolved oxygen is the amount of oxygen present in water at a moment; BOD is the amount of oxygen that microorganisms will use to decompose the organic matter present, so it indicates organic pollution load.'),
            ('direct measurement of pollutants', 'indirect measurement using indicator species', 'Direct measurements (nitrate, phosphate, pH, heavy metals) quantify specific pollutants; indirect measurement uses organisms whose tolerance reveals overall water quality over time.')],
  misc=[('A river with no fish must be heavily polluted.', 'Absence of fish may be due to barriers (dams), natural conditions (fast headwaters), or overfishing; invertebrate surveys and chemical tests are needed.'),
        ('A high dissolved-oxygen reading always means the water is clean.', 'DO can be high in daytime due to photosynthesis by an algal bloom in eutrophic water; readings should be taken at dawn and alongside BOD.')],
  apply=[('Describe how a kick-sample could be used to assess the water quality of a stream.', 'Hold a net downstream, disturb the streambed for a fixed time (e.g. 1 minute) over a set area, transfer organisms to a tray, identify to family using a key, calculate a biotic index (BMWP/ASPT), repeat at several sites.', 4),
         ('Suggest three abiotic variables that should be measured when assessing river water quality, and a method for each.', 'Dissolved oxygen (DO meter or Winkler titration); nitrate/phosphate (colorimeter or test kit); pH (meter); temperature (thermometer); turbidity (Secchi disk/turbidity tube); flow velocity (flow meter).', 3)],
  cases=[('the River Thames, London', 'declared "biologically dead" in 1957, it now supports over 125 fish species after sewage-treatment improvements; the Thames Tideway Tunnel (completed 2025) aims to capture sewage overflows', 'monitoring and improving water quality', 'reduced organic pollution lowered BOD and raised DO, allowing pollution-sensitive species to return'),
         ('the Rhine Action Programme', 'after the 1986 Sandoz chemical spill killed fish for hundreds of kilometres, the "Salmon 2000" programme improved water quality and salmon returned', 'water quality indicators and recovery', 'the return of indicator species such as salmon and mayflies shows sustained improvement in water quality')],
  evaluate=[('Biotic indices are more reliable than chemical tests for monitoring water quality.', ['integrate conditions over time', 'detect intermittent pollution', 'cheap and simple'], ['identification errors', 'natural variation in habitat affects communities', 'do not identify the specific pollutant'], 'Biotic indices are more reliable for overall ecological health, while chemical tests are needed to identify and regulate specific pollutants.')],
  extended=[('Design an investigation to compare water quality upstream and downstream of a sewage outfall. [7]', 'Research question; sites (several up- and downstream); variables (DO, BOD, nitrate, phosphate, temperature, flow); kick-sampling for BMWP/ASPT; replicates; controlled variables (time, depth, substrate); statistical test; safety.', 7, 'explain')],
  res=[('Survey results: Site A (upstream) - DO 10.2 mg/L, BOD₅ 1.8 mg/L, ASPT 6.4, mayflies and stoneflies present; Site B (200 m below a farm drain) - DO 5.1 mg/L, BOD₅ 7.4 mg/L, ASPT 3.2, sludge worms and chironomid larvae dominant.',
        [('Compare the two sites and identify the most likely type of pollution at Site B.', 'Site B has half the DO, about four times the BOD and a much lower ASPT with tolerant species; organic pollution (e.g. slurry or silage effluent).'),
         ('Suggest one further measurement that would help confirm the source.', 'Ammonia or nitrate and phosphate concentrations, faecal coliform counts, or sampling the drain itself and further downstream.')])])

S('ch12-st4',
  terms=[('pollution management model', 'a framework for managing pollution at three levels: altering the human activity producing the pollutant, controlling its release, and cleaning up or restoring damaged ecosystems'),
         ('sewage treatment', 'the removal of contaminants from wastewater through primary (physical settling), secondary (biological) and tertiary (chemical, nutrient removal) stages'),
         ('constructed wetland', 'an artificial wetland designed to treat wastewater or runoff by using plants, soil and microbes to remove nutrients and pollutants'),
         ('polluter pays principle', 'the principle that those who produce pollution should bear the costs of managing it'),
         ('EU Water Framework Directive', 'the 2000 European Union law requiring member states to achieve good ecological and chemical status in all water bodies, managed by river basin')],
  facts=[('Which stage of the pollution management model is the most effective long-term?', 'Altering the human activity that produces the pollutant', ['Cleaning up after release', 'Restoring damaged ecosystems', 'Ignoring the problem'], 'Preventing pollution avoids damage and clean-up costs.'),
         ('Which stage of sewage treatment uses bacteria to break down organic matter?', 'Secondary treatment', ['Primary treatment', 'Screening', 'Tertiary treatment only'], 'Activated sludge or trickling filters.'),
         ('Which international convention aims to reduce marine pollution from ships?', 'MARPOL', ['CITES', 'Ramsar', 'Kyoto Protocol'], 'MARPOL (1973/78) covers oil, sewage, garbage and air pollution from ships.'),
         ('The EU Water Framework Directive manages water by:', 'river basin districts', ['national borders only', 'city boundaries', 'ocean basins'], 'Pollution and water flow cross administrative borders.')],
  why=[('Explain why tertiary sewage treatment is important in preventing eutrophication.', 'Primary and secondary treatment remove solids and organic matter but leave dissolved nitrates and phosphates; tertiary treatment removes these nutrients (chemical precipitation, biological nutrient removal) before discharge.'),
       ('Explain why managing pollution at the catchment scale is more effective than managing individual sources.', 'Pollutants from many dispersed sources combine in rivers; catchment management coordinates farms, towns and industry, addresses non-point sources and considers cumulative impacts upstream and downstream.'),
       ('Explain why clean-up and restoration are the least preferred pollution management strategies.', 'Damage has already occurred, clean-up is expensive and often incomplete, persistent pollutants remain in sediments, and recovery may take decades.')],
  contrast=[('controlling the release of a pollutant', 'cleaning up after pollution', 'Controlling release stops pollutants reaching the environment (filters, buffer strips, treatment); clean-up removes pollutants or restores ecosystems after damage (dredging, oil-spill dispersants), and is usually more costly and less complete.')],
  misc=[('Sewage treatment removes all pollutants from wastewater.', 'Standard treatment does not remove all nutrients, pharmaceuticals, microplastics or PFAS; tertiary treatment is needed for some, and some remain.'),
        ('Pollution management is only the responsibility of governments.', 'Individuals, farmers, industries, NGOs and international bodies all have roles, e.g. consumers choosing phosphate-free detergents.')],
  apply=[('Using the pollution management model, suggest one strategy at each level for reducing plastic pollution in a river.', 'Altering activity: ban single-use plastics, deposit-return schemes; controlling release: litter traps and improved waste collection; clean-up: river booms and beach clean-ups.', 3),
         ('Suggest how a constructed wetland could reduce pollution from a dairy farm.', 'Dirty water and runoff pass through shallow vegetated cells where sediment settles, plants absorb nutrients, and microbes break down organic matter and denitrify nitrate, so cleaner water reaches the river.', 3)],
  cases=[('the Baltic Sea Action Plan (HELCOM, 2007)', 'Baltic states agreed nutrient reduction targets; phosphorus inputs fell by about a quarter, but dead zones persist', 'international cooperation in managing water pollution', 'controlling release from sewage works succeeded, but legacy nutrients in sediments and farm runoff slow recovery'),
         ('the River Thames Tideway Tunnel, London', 'a 25 km "super sewer" completed in 2025 to capture most of the 39 million tonnes of sewage overflow that entered the Thames in a typical year', 'controlling the release of pollutants', 'storing overflow in a tunnel and sending it for treatment stops untreated sewage reaching the river after heavy rain')],
  evaluate=[('Legislation is the most effective way to manage water pollution.', ['US Clean Water Act (1972) and EU WFD improved many rivers', 'enforceable standards and fines', 'polluter pays principle'], ['enforcement varies; many EU rivers still not in good status', 'non-point sources hard to regulate', 'needs funding and public cooperation'], 'Legislation provides the essential framework, but must be combined with funding, incentives for farmers and public action.')],
  extended=[('Evaluate the use of the pollution management model for a named water pollution issue. [9]', 'e.g. Lake Erie, Baltic Sea, River Thames, Citarum, plastics: strategies at each level, effectiveness, costs, stakeholders, political will; judgement.', 9, 'long')],
  res=[('Data: a sewage works serving 50,000 people discharges effluent with 8 mg/L phosphate before an upgrade and 1 mg/L after tertiary treatment. Effluent flow is 10,000 m³ per day.',
        [('Calculate the reduction in phosphate discharged per day in kg (1 mg/L = 1 g/m³).', 'Before: 8 × 10,000 = 80,000 g = 80 kg; after: 10 kg; reduction 70 kg per day (87.5%).'),
         ('State the level of the pollution management model this represents and suggest one complementary measure.', 'Controlling the release of the pollutant; e.g. phosphate-free detergents (altering human activity) or buffer strips on farmland.')])])


# ---------------------------------------------------------------------------------------------
# additional evaluate / discuss claims (C4 variety)
# ---------------------------------------------------------------------------------------------
EXTRA_EV = {
    'ch02-st1': ('Treating Earth as a closed system is a useful basis for environmental management.', ['emphasises that matter is finite and must be recycled', 'highlights waste accumulation (plastics, CO₂)'], ['Earth receives continuous solar energy, so energy is not finite in the same way', 'small inputs of matter (meteorites) and the scale of the system make the analogy imperfect'], 'The closed-system model is a powerful reminder of finite matter and the need for circularity, even though energy inputs are effectively continuous.'),
    'ch02-st2': ('Models of environmental systems are more useful for communicating ideas than for making predictions.', ['simple diagrams communicate complex systems to the public and policymakers', 'model predictions carry wide uncertainty'], ['climate models have accurately projected warming since the 1970s', 'fisheries models guide quotas'], 'Models do both; they communicate well and, when validated with data, give useful though uncertain predictions.'),
    'ch02-st4': ('An understanding of the laws of thermodynamics should shape food and energy policy.', ['eating lower on the food chain saves ~90% of energy losses', 'energy efficiency reduces waste heat and fuel use'], ['cultural and economic factors dominate food choices', 'renewable energy makes efficiency less critical'], 'Thermodynamics provides a sound scientific basis for policies favouring efficiency and plant-rich diets, but must be balanced with social and economic realities.'),
    'ch03-st2': ('High-income countries should be required to reduce their ecological footprints to the global biocapacity per person.', ['fair share of a finite planet (~1.6 gha)', 'high-income countries are responsible for most overshoot'], ['economically and politically unrealistic in the short term', 'footprints depend on trade and global supply chains', 'technology can reduce impacts without reducing wellbeing'], 'A move towards fair-share footprints is justified, but must be gradual and supported by technology and international cooperation.'),
    'ch04-st1': ('Protecting habitats is sufficient to protect the niches of all the species within them.', ['habitat protection conserves resources and interactions', 'cost-effective for many species'], ['niches depend on interactions that can be lost (pollinators, predators)', 'climate change shifts conditions within protected habitats', 'migratory species need several habitats'], 'Habitat protection is necessary but not sufficient; maintaining species interactions and connectivity is also needed.'),
    'ch04-st2': ('Human populations are not limited by carrying capacity in the same way as other species.', ['technology and trade raise carrying capacity (Green Revolution)', 'humans can import resources'], ['global planetary boundaries are a limit', 'local overshoot causes famine and degradation', 'the ecological footprint already exceeds biocapacity'], 'Technology and trade make human carrying capacity flexible, but the planet as a whole still imposes limits.'),
    'ch04-st3': ('Removing a top predator always harms an ecosystem.', ['trophic cascades (sea otters and kelp)', 'herbivore overgrazing'], ['some predators are invasive and their removal benefits natives (cats on islands, stoats in New Zealand)', 'ecosystems may adjust with mesopredators'], 'Removing native top predators usually destabilises ecosystems, but removing invasive predators often benefits biodiversity.'),
    'ch04-st4': ('Citizen science is a reliable method for collecting biodiversity data.', ['very large datasets (eBird, iNaturalist, Big Garden Birdwatch)', 'long-term and wide coverage', 'raises public awareness'], ['identification errors', 'sampling bias towards accessible areas and charismatic species', 'variable effort'], 'Citizen science is valuable when protocols, verification and statistical correction for bias are used.'),
    'ch05-st1': ('Food webs are more resilient when they contain many top predators.', ['predators regulate herbivores and prevent overgrazing', 'keystone predators maintain diversity (Paine\'s starfish)'], ['too many predators can deplete prey', 'resilience also depends on producer and decomposer diversity'], 'Healthy predator populations generally increase resilience, but diversity at all trophic levels matters.'),
    'ch05-st2': ('Increasing the efficiency of photosynthesis in crops is the best way to improve food security.', ['photosynthesis converts only ~1-3% of sunlight', 'research (RIPE project) suggests yield gains of 20%+'], ['food waste, distribution and poverty are bigger problems', 'yields also limited by water and nutrients'], 'Improved photosynthesis could help, but reducing waste and improving access are more immediate solutions.'),
    'ch05-st3': ('Measuring productivity is more useful than measuring biomass for managing ecosystems.', ['productivity shows sustainable yield (natural income)', 'indicates energy available to consumers'], ['biomass shows carbon storage and habitat structure', 'productivity is harder to measure'], 'Both are needed: productivity guides harvesting, while biomass guides carbon and habitat conservation.'),
    'ch05-st4': ('The benefits of using persistent pesticides outweigh the risks.', ['DDT controls malaria mosquitoes (indoor spraying)', 'protects crops and yields'], ['biomagnification harms top predators and humans', 'pests evolve resistance', 'alternatives such as integrated pest management exist'], 'In most uses the long-term risks outweigh the benefits, though limited, controlled uses (malaria) can be justified.'),
    'ch06-st1': ('Afforestation is the most effective method of increasing carbon sinks.', ['natural, cheap, co-benefits for biodiversity and water', 'large potential area'], ['slow; carbon can be lost to fire and disease', 'competes with food production', 'monoculture plantations have low biodiversity', 'ocean and soil sinks also important'], 'Afforestation helps but is limited; protecting existing stores, restoring peat and blue carbon, and cutting emissions are equally important.'),
    'ch06-st2': ('Organic farming is the best way to reduce human impacts on the nitrogen cycle.', ['relies on legumes and manure instead of synthetic N', 'lower nitrate leaching per hectare'], ['lower yields need more land', 'manure can also leach nitrate', 'precision farming can reduce surplus N'], 'Organic methods reduce synthetic inputs but are not always best; a combination of precision agriculture, legumes and nutrient recycling is likely most effective.'),
    'ch06-st3': ('Restoring blue-carbon ecosystems is a cost-effective climate strategy.', ['high sequestration per hectare', 'co-benefits: coastal protection, fisheries', 'community carbon credits (Mikoko Pamoja)'], ['small total area limits global impact', 'measurement and permanence uncertain', 'sea-level rise may drown them'], 'Blue-carbon restoration is cost-effective because of its co-benefits, though its global mitigation potential is modest compared with emissions cuts.'),
    'ch07-st1': ('Climate change will cause the distribution of biomes to change faster than species can adapt.', ['climate zones are shifting at an average of about 0.4 km per year (much faster in flat lowlands)', 'trees disperse slowly; barriers block movement'], ['some species adapt or shift quickly (birds, insects)', 'refugia allow persistence', 'conservation corridors can help'], 'For many slow-moving species and specialist biomes change is likely to outpace adaptation, so assisted migration and corridors may be needed.'),
    'ch07-st2': ('The tropical rainforest is the most important biome to conserve.', ['highest biodiversity and NPP', 'major carbon store and rainfall regulator'], ['tundra and boreal forests hold huge carbon stores', 'oceans and coral reefs equally threatened and valuable', 'every biome provides unique services'], 'Rainforests are a priority but conserving a range of biomes is necessary for global biodiversity and climate stability.'),
    'ch07-st4': ('Field studies of zonation are of limited value because conditions change over time.', ['one-off transects give a snapshot', 'seasonal and tidal variation'], ['repeated transects reveal long-term trends (climate change)', 'zonation patterns are relatively stable over years', 'cheap and informative'], 'Single studies are limited, but repeated transects are valuable for monitoring change.'),
    'ch08-st1': ('Genetic diversity is more important to conserve than species diversity.', ['allows adaptation to climate change and disease', 'crop genetic diversity underpins food security'], ['species diversity maintains ecosystem function', 'genetic diversity cannot be conserved without species and habitats'], 'All levels are interdependent; genetic diversity is essential for long-term resilience, but it is conserved mainly by protecting species and habitats.'),
    'ch08-st2': ('Natural selection will allow most species to adapt to rapid climate change.', ['short-generation species can evolve quickly (insects, microbes)', 'examples of rapid evolution (peppered moth, finches)'], ['many large species reproduce slowly', 'rate of change is unprecedented', 'habitat fragmentation reduces gene flow'], 'Some species will adapt, but most long-lived species cannot evolve fast enough, so conservation is needed.'),
    'ch08-st3': ('Isolation is the most important factor in producing high biodiversity.', ['islands and continents show high endemism (Madagascar, Galápagos)', 'allopatric speciation'], ['climate and productivity explain tropical diversity', 'habitat heterogeneity and time are also important'], 'Isolation is key for endemism, but overall richness depends on climate, productivity, habitat diversity and time.'),
    'ch09-st1': ('Invasive species are the greatest threat to island biodiversity.', ['responsible for most island bird extinctions (Guam, Hawaii, New Zealand)', 'predators and diseases spread rapidly'], ['habitat loss and climate change also severe on islands', 'sea-level rise threatens low islands'], 'On islands invasive species are the leading historical cause of extinction, though climate change is becoming increasingly important.'),
    'ch09-st2': ('Charismatic species receive too much conservation attention.', ['funding biased to large mammals', 'invertebrates and plants under-studied'], ['flagship species raise funds that protect whole habitats (pandas, tigers)', 'umbrella effect benefits many species'], 'Flagship species can benefit wider biodiversity if funds are used for habitat protection, but more attention is needed for neglected taxa.'),
    'ch10-st1': ('Groundwater should be managed as a non-renewable resource.', ['many aquifers recharge far slower than abstraction (Ogallala, North China Plain)', 'fossil aquifers do not recharge'], ['shallow aquifers in humid regions recharge quickly', 'managed aquifer recharge can replenish stores'], 'Groundwater should be managed according to recharge rate; fossil and slowly recharging aquifers should be treated as non-renewable.'),
    'ch10-st2': ('Protecting upwelling ecosystems is essential for global food security.', ['upwelling areas cover ~1% of ocean but produce ~20% of catch', 'support fishmeal for aquaculture'], ['catches fluctuate naturally with El Niño', 'aquaculture and land-based food dominate total supply'], 'Upwelling ecosystems are disproportionately important for fisheries and should be protected, though they are only one part of food security.'),
    'ch10-st3': ('International agreements are the best way to manage shared water resources.', ['Indus Waters Treaty has survived wars since 1960', 'cooperation shares benefits (Mekong River Commission)'], ['agreements may be outdated or exclude parties (1959 Nile Agreement)', 'weak enforcement', 'upstream power dominates'], 'Agreements are essential but succeed only when inclusive, flexible and backed by data sharing and benefit sharing.'),
    'ch11-st1': ('Freshwater fisheries deserve as much protection as marine fisheries.', ['support food security for millions inland (Mekong, Lake Victoria)', 'freshwater biodiversity declining fastest (85% LPI)'], ['smaller total catch', 'marine stocks have larger global economic value'], 'Freshwater fisheries deserve equal or greater protection because of their importance to the poorest communities and steep biodiversity decline.'),
    'ch11-st3': ('Consumers can make aquaculture sustainable through their purchasing choices.', ['certification (ASC) rewards better practice', 'demand for low-trophic species (mussels, seaweed)'], ['labels can be confusing or weak', 'most production in Asia is for domestic markets without labels', 'regulation is needed'], 'Consumer choice helps drive improvement but regulation and industry standards are also needed.'),
    'ch12-st1': ('Point-source pollution is no longer a major problem in high-income countries.', ['regulation and treatment have cleaned many rivers (Thames, Rhine)'], ['sewage overflows still frequent (England 2023: ~3.6 million hours of spills)', 'industrial accidents and legacy pollution', 'emerging pollutants (PFAS) from point sources'], 'Point sources are much better controlled than in the past, but overflows and new pollutants mean they remain significant.'),
    'ch12-st3': ('Indicator species provide better evidence of pollution than chemical analysis.', ['integrate conditions over time', 'reflect ecological impact directly'], ['cannot identify the specific pollutant', 'affected by habitat and season', 'chemical tests needed for legal action'], 'Indicator species are excellent for assessing ecological health, but chemical analysis is required to identify sources and enforce laws.'),
    'ch12-st4': ('Preventing pollution is always more cost-effective than cleaning it up.', ['clean-up is costly and incomplete (Deepwater Horizon cost BP over US$60 billion)', 'avoids ecological damage'], ['prevention can have high upfront costs (Tideway ~£4.5 billion)', 'some pollution is accidental or historic and requires clean-up'], 'Prevention is generally more cost-effective, but clean-up and restoration remain necessary for accidents and legacy pollution.'),
}
for _k, _ev in EXTRA_EV.items():
    P.R.f[_k].evaluate.append(_ev)
