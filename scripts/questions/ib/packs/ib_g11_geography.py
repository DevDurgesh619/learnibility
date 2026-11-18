"""IB DP Geography SL/HL (guide for first assessment 2019) - ib-g11-geography, year 1.

Year 1 covers the SL/HL core (Unit 1 Changing population, Unit 2 Global climate - vulnerability and
resilience, Unit 3 Global resource consumption and security), Option A Freshwater, Option G Urban
environments and fieldwork for the internal assessment.

Item styles
  * C1 define / state / identify (Paper 1 and 2 structured part (a), 2 marks),
  * C2 explain / distinguish / misconception (structured parts, 2-4 marks),
  * C3 case-study application with named, located places and real figures; data- and resource-based items
    described in text (tables, graphs, maps) whose answers are COMPUTED (natural increase, doubling time,
    dependency ratio, percentage change, density, Spearman's rank, nearest-neighbour index, discharge,
    gradients, recurrence intervals, footprints, chi-squared) with M1/A1 markschemes,
  * C4 Paper 1 extended response [10] ("Examine", "Evaluate", "Discuss", "To what extent"), Paper 2
    infographic / visual stimulus [10] and Paper 2 Section C essays [15] with markband keys.
Figures quoted for real places are rounded published values (UN DESA, World Bank, IPCC, Global Footprint
Network, Water Footprint Network); parametric data sets are labelled as survey / sample data.
Shared machinery (gens, essay templates, markbands) is imported by ib_g12_geography.py.
"""
from __future__ import annotations

import math
import random
import re

from _common import F, Registry, T, mcq, name, fmt

CONFIG = {'minutesPerMark': 1.8, 'mcqMinutes': 1.5}

# One mock = Paper 1 (Option A Freshwater and Option G Urban environments: each a structured question [10]
# + one extended response [10]) + Paper 2 core (Section A: three structured questions [10 each]; Section B:
# infographic / visual stimulus [10]; Section C: one extended response [15]). 18 items, 95 marks.
# Sections draw only on the chapters of the matching option / core unit (chapter orders).
OPT_A, OPT_G, CORE = [10, 11], [12, 13], list(range(1, 10))
MOCK = []
for _opt, _ch in (('Option A Freshwater', OPT_A), ('Option G Urban environments', OPT_G)):
    MOCK += [
        dict(section=f'Paper 1 {_opt} - structured question (a): define / state', count=1, c=['C1'], d=[2], type='short', marks=2, chapters=_ch),
        dict(section=f'Paper 1 {_opt} - structured question (b): data / resource interpretation', count=1, c=['C3'], d=[2, 3], type='numerical', marks=2, style='data', chapters=_ch),
        dict(section=f'Paper 1 {_opt} - structured question (c): explain', count=1, c=['C2'], d=[3], type='explain', marks=3, chapters=_ch),
        dict(section=f'Paper 1 {_opt} - structured question (d): explain with a named example', count=1, c=['C3'], d=[3], type='short', marks=3, chapters=_ch),
        dict(section=f'Paper 1 {_opt} - extended response', count=1, c=['C4'], d=[4], type='long', marks=10, style='p1ext', chapters=_ch),
    ]
MOCK += [
    dict(section='Paper 2 Section A (core) - structured question: data analysis', count=3, c=['C3'], d=[3, 4], type='numerical', marks=4, style='data', chapters=CORE),
    dict(section='Paper 2 Section A (core) - structured question: explain', count=3, c=['C2'], d=[3, 4], type='explain', marks=6, chapters=CORE),
    dict(section='Paper 2 Section B - infographic / visual stimulus', count=1, c=['C4'], d=[4], type='long', marks=10, style='infographic', chapters=CORE),
    dict(section='Paper 2 Section C - extended response essay', count=1, c=['C4'], d=[5], type='long', marks=15, style='essay15', chapters=CORE),
]

# ---------------------------------------------------------------------------------------------
# markbands
# ---------------------------------------------------------------------------------------------
MB10 = ('Paper 1 extended-response markbands [10]: 9-10 responds to all demands of the question; accurate, detailed '
        'knowledge and understanding; well-developed, relevant examples and case studies with specific (named, located, '
        'quantified) detail; balanced, well-structured evaluation leading to a substantiated conclusion. 7-8 responds to most '
        'demands; mostly accurate knowledge; examples relevant but not always fully developed; evaluation present but uneven. '
        '5-6 some demands addressed; knowledge partly accurate; examples general or loosely linked; evaluation mostly '
        'implicit. 3-4 limited, largely descriptive; little use of examples. 1-2 little relevant knowledge or understanding. '
        '0 does not reach the standard of the descriptors.')
MB15 = ('Paper 2 Section C markbands [15]: 13-15 thorough response to all demands including the command term; accurate, '
        'detailed geographical knowledge and terminology; well-chosen, located and quantified examples at more than one '
        'scale; explicit, balanced evaluation (perspectives, places, scales, time) with a well-substantiated conclusion. '
        '10-12 most demands addressed; accurate knowledge; examples relevant and developed; evaluation is balanced but not '
        'sustained. 7-9 some demands addressed; knowledge mostly accurate; examples partly developed; evaluation partial or '
        'one-sided. 4-6 limited, mainly descriptive; generalised examples; little evaluation. 1-3 little relevant '
        'knowledge; no examples or evaluation. 0 does not reach the standard of the descriptors.')
MBINF = ('Infographic markscheme [10]: part (a) [4] - award 1 mark per valid point taken from the resource (data must be '
         'quoted with units for full marks); part (b) [6] - up to 2 marks for each developed explanation linking the '
         'resource to own knowledge; reward named examples; maximum 3 marks if the resource is not used.')
MB4 = ('[4]: 1 mark for a valid argument for, 1 for its development; 1 mark for a valid argument against, 1 for its '
       'development; generic points without geographical context are capped at 2.')

R = Registry()
GENS: dict = {}          # name -> (c, (dmin, dmax), fn, type, style)
USE: dict = {}           # 'chNN-stN' -> [gen names]
RES: dict = {}           # 'chNN-stN' -> [(resource text, [(question, answer), ...])]
HL = {'p3': False}


def init(subject_id):
    pass


def _key(st):
    return st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]


def lc(s):
    w = re.sub(r"['’]s$", '', s.split(' ')[0].strip('"'))
    if w in KEEP or w.isupper() or (len(w) > 1 and any(ch.isupper() for ch in w[1:])):
        return s
    return s[0].lower() + s[1:]


KEEP = {'Malthus', 'Boserup', 'China', 'Japan', 'Singapore', 'India', 'Paris', 'Kyoto', 'Bangladesh', 'Africa', 'Europe',
        'Asia', 'Nigeria', 'Brazil', 'Germany', 'Egypt', 'Ethiopia', 'Pakistan', 'Australia', 'Canada', 'Kerala', 'Malthusian',
        'Rostow', 'Friedmann', 'Burgess', 'Hoyt', 'Christaller', 'Ravenstein', 'Lee', 'Sweden', 'Costa', 'Curitiba', 'Masdar',
        'Songdo', 'Delhi', 'London', 'Detroit', 'Dharavi', 'Mumbai', 'Lagos', 'Tokyo', 'Netherlands', 'Rotterdam', 'Venice',
        'Nile', 'Indus', 'Mekong', 'Three', 'Narmada', 'Aswan', 'Ramsar', 'Spearman', 'Hjulström', 'Horton', 'Western', 'Sub-Saharan',
        'Gulf', 'Russia', 'Europe\'s', 'Japan\'s', 'China\'s', 'India\'s', 'Singapore\'s', 'Earth', 'Earth\'s', 'Global', 'Ehrlich',
        'Simon', 'Raworth', 'Sendai', 'Hyogo', 'Haiti', 'Nepal', 'Chile', 'Indonesia', 'Italy', 'Iceland', 'Montserrat', 'Mount',
        'Kobe', 'Christchurch', 'Hawaii', 'Tōhoku', 'Ring', 'Wegener', 'Richter', 'Mercalli', 'Gini', 'Greenberg', 'TNCs', 'TNC',
        'KOF', 'Hollywood', 'Bollywood', 'K-pop', 'McDonald\'s', 'Apple', 'Nike', 'Brexit', 'Trump', 'Covid-19', 'COVID-19',
        'Ukraine', 'Suez', 'Belt', 'Chinese', 'American', 'Indian', 'African', 'Arctic', 'Antarctic', 'Amazon', 'Montreal',
        'Basel', 'Stockholm', 'Greta', 'Extinction', 'Fridays', 'Facebook', 'Twitter', 'X', 'Internet', 'Kenya', 'Mexico', 'Turkey',
        'Syria', 'Syrian', 'Rohingya', 'Sudan', 'Philippine', 'Filipino', 'Polish', 'Gulf-state', 'Qatar', 'Dubai', 'Mongolia', 'Peru',
        'Bolivia', 'Tuvalu', 'Kiribati', 'Maldives', 'Pacific', 'Atlantic', 'Fiji', 'Sahel', 'Lake', 'Great', 'Room', 'Thames'}


def S(key, gens=(), res=(), **kw):
    """Register a subtopic: fact pack (F fields), parametric gens by name, and resources (text, [(q, a)])."""
    def sent(x):
        x = x.strip()
        x = x[0].upper() + x[1:]
        return x if x[-1] in '.!?)' else x + '.'
    if 'cases' in kw:
        kw['cases'] = [(c, sent(w), concept, sent(h)) for c, w, concept, h in kw['cases']]
    R.facts(key, F(**kw))
    USE[key] = list(gens)
    RES[key] = list(res)


def gen(nm, c='C3', d=(1, 5), type='numerical', style='data'):
    def deco(fn):
        GENS[nm] = (c, d, fn, type, style)
        return fn
    return deco


def mk(slot, default):
    return slot.marks or default


def r1(x):
    return f'{x:.1f}'


def r2(x):
    return f'{x:.2f}'


def comma(x):
    return f'{int(round(x)):,}'


# ---------------------------------------------------------------------------------------------
# geography item templates (essays, infographic, resources) built from the fact packs
# ---------------------------------------------------------------------------------------------
def geo_templates(f: F, res: list, hl: bool) -> list:
    out = []
    ev = f.evaluate

    if ev:
        def ev4(rng, slot):
            claim, pro, con, judge = rng.choice(ev)
            stem = rng.choice([
                f'Outline one argument for and one argument against the view that {lc(claim)}',
                f'Give one strength and one weakness of the claim that {lc(claim)}',
                f'Briefly analyse two contrasting points of view on the statement: "{claim}"',
            ])
            return dict(stem=stem, answer=judge, type='case', marks=mk(slot, 4),
                        markingKey=f'For: {pro[0]}. Against: {con[0]}. {MB4}')
        out.append(T('C4', (2, 3), ev4, 'case', None, 'ev4'))

        def p1ext(rng, slot):
            claim, pro, con, judge = rng.choice(ev)
            stem = rng.choice([
                f'Examine the view that {lc(claim)}',
                f'Evaluate the claim that {lc(claim)}',
                f'"{claim}" Discuss this statement, with reference to examples you have studied.',
                f'To what extent do you agree that {lc(claim).rstrip(".")}?',
            ])
            key = ('Indicative content - for: ' + '; '.join(pro) + '. Against / limitations: ' + '; '.join(con) +
                   f'. A supported conclusion might be: {judge} {MB10}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=mk(slot, 10))
        out.append(T('C4', (3, 5), p1ext, 'long', 'p1ext', 'p1ext'))

        def essay15(rng, slot):
            claim, pro, con, judge = rng.choice(ev)
            stem = rng.choice([
                f'"{claim}" To what extent do you agree with this statement?',
                f'To what extent is it true that {lc(claim).rstrip(".")}? Refer to places and scales you have studied.',
            ])
            key = ('Indicative content - arguments supporting the statement: ' + '; '.join(pro) +
                   '. Arguments challenging it: ' + '; '.join(con) +
                   f'. Evaluation should weigh places, scales, perspectives and time. Judgement: {judge} {MB15}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=mk(slot, 15), minutes=27.0)
        out.append(T('C4', (4, 5), essay15, 'long', 'essay15', 'essay15'))

        if hl:
            def p3a(rng, slot):
                claim, pro, con, judge = rng.choice(ev)
                stem = rng.choice([
                    f'Examine the reasons why {lc(claim).rstrip(".")} in some places but not in others.',
                    f'Explain the arguments that geographers use to support the view that {lc(claim)}',
                ])
                key = ('Paper 3 (a) indicative content: ' + '; '.join(pro + con) +
                       '. Markbands [12]: 10-12 detailed, accurate explanation with well-developed, located examples and '
                       'clear links between factors; 7-9 accurate explanation, examples partly developed; 4-6 some relevant '
                       'knowledge, mostly descriptive; 1-3 little relevant knowledge.')
                return dict(stem=stem, answer='; '.join(pro), markingKey=key, type='long', marks=mk(slot, 12))
            out.append(T('C4', (4, 5), p3a, 'long', 'p3a', 'p3a'))

            def p3b(rng, slot):
                claim, pro, con, judge = rng.choice(ev)
                persp = rng.choice(['different stakeholders', 'people in high- and low-income countries',
                                    'different places and scales', 'short-term and long-term'])
                stem = (f'"{claim}" To what extent do you agree with this statement? In your answer, consider the '
                        f'perspectives of {persp}.')
                key = ('Paper 3 (b) indicative content - for: ' + '; '.join(pro) + '. Against: ' + '; '.join(con) +
                       f'. Judgement: {judge} Markbands [16]: 14-16 well-structured, balanced argument that synthesises '
                       'HL concepts (power, places, processes, possibilities) across scales; perspectives evaluated explicitly; '
                       'detailed, located evidence; substantiated conclusion. 11-13 balanced with developed evidence but '
                       'synthesis uneven. 8-10 some evaluation, evidence partly developed. 5-7 mainly descriptive. 1-4 little '
                       'relevant knowledge.')
                return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=mk(slot, 16), minutes=30.0)
            out.append(T('C4', (4, 5), p3b, 'long', 'p3b', 'p3b'))

    if res:
        def data(rng, slot):
            text, qs = rng.choice(res)
            q, a = rng.choice(qs)
            intro = rng.choice(['Study the resource below.', 'Refer to the data below.', 'The following information is provided.'])
            m = mk(slot, 2 if slot.d <= 2 else 3 if slot.d == 3 else 4)
            return dict(stem=f'{intro}\n\n{text}\n\n{q}', answer=a, type='case', marks=m, gap='G7',
                        markingKey=f'{a} Award 1 mark per valid point or correct step, up to [{m}]; data quoted must include units; '
                                   'points must be drawn from the resource.')
        out.append(T('C3', (2, 4), data, 'case', 'data', 'data'))

        def infographic(rng, slot):
            text, qs = rng.choice(res)
            if len(qs) < 2:
                return None
            (qa, aa), (qb, ab) = qs[0], qs[1]
            if rng.random() < 0.5 and len(qs) > 2:
                qb, ab = qs[2]
            stem = (f'Study the infographic / visual stimulus described below.\n\n{text}\n\n(a) {qa} [4]\n'
                    f'(b) Using the resource and your own knowledge, {lc(qb)} [6]')
            return dict(stem=stem, answer=f'(a) {aa} (b) {ab}', type='long', marks=mk(slot, 10), gap='G7',
                        markingKey=f'(a) {aa} (b) {ab} Credit relevant own knowledge and named examples in (b). {MBINF}')
        out.append(T('C4', (3, 5), infographic, 'long', 'infographic', 'infographic'))
    if f.extended:
        def extended(rng, slot):
            it = rng.choice(f.extended)
            stem, ans = it[0], re.sub(r'^(Award|Indicative)( content)?:\s*', '', it[1])
            ans = ans[0].upper() + ans[1:]
            m = mk(slot, it[2] if len(it) > 2 else 10)
            ty = it[3] if len(it) > 3 else 'long'
            band = MB10 if m >= 8 else ('Award 1 mark per relevant, developed point, up to [' + str(m) + ']; full marks need specific, '
                                        'located examples or justified fieldwork detail.')
            return dict(stem=stem, answer='Indicative content: ' + ans, markingKey=f'Indicative content: {ans} {band}', type=ty, marks=m)
        out.append(T('C4', (2, 5), extended, 'long', 'p1ext', 'extended'))
    return out


def templates(st):
    key = _key(st)
    f = R.f.get(key)
    out = [t for t in R.build(st, {'eval_marks': 10, 'essay_marks': 15, 'markband': MB15})
           if t.name not in ('evaluate', 'source', 'extended')]
    for g in USE.get(key, []):
        c, d, fn, ty, sty = GENS[g]
        out.append(T(c, d, fn, ty, sty, g))
    if f:
        out += geo_templates(f, RES.get(key, []), HL['p3'])
    return out


# ---------------------------------------------------------------------------------------------
# parametric data / skills generators (answers computed)
# ---------------------------------------------------------------------------------------------
NIR_C = [('Niger', 44, 9), ('Nigeria', 36, 12), ('Pakistan', 27, 7), ('India', 16, 7), ('Brazil', 12, 7),
         ('Bangladesh', 18, 5), ('Japan', 6, 13), ('Germany', 9, 12), ('Italy', 7, 12), ('Ethiopia', 31, 6),
         ('the Philippines', 21, 6), ('Mexico', 15, 7), ('South Korea', 5, 7), ('the United Kingdom', 10, 9),
         ('Egypt', 22, 5), ('Kenya', 27, 5), ('Indonesia', 16, 7), ('the DR Congo', 42, 9)]


@gen('nir')
def g_nir(rng, slot):
    c, b0, d0 = rng.choice(NIR_C)
    cbr = round(b0 + rng.uniform(-1.5, 1.5), 1)
    cdr = round(d0 + rng.uniform(-1.0, 1.0), 1)
    nir = (cbr - cdr) / 10
    head = rng.choice([
        f'Estimates for {c} give a crude birth rate (CBR) of {cbr} per 1,000 and a crude death rate (CDR) of {cdr} per 1,000.',
        f'A population data sheet lists {c} with {cbr} births and {cdr} deaths per 1,000 people per year.',
        f'In a recent year {c} recorded a CBR of {cbr}‰ and a CDR of {cdr}‰ (ignore migration).',
    ])
    if slot.d <= 2 or nir <= 0:
        ans = f'NIR = ({cbr} − {cdr}) / 10 = {nir:.2f}% per year' + (' (natural decrease)' if nir < 0 else '')
        return dict(stem=f'{head} Calculate the rate of natural increase (NIR) as a percentage.', answer=ans,
                    markingKey=f'M1 subtracting CDR from CBR ({cbr - cdr:.1f} per 1,000); A1 dividing by 10: {nir:.2f}%.', marks=mk(slot, 2))
    dt = 70 / nir
    if slot.d == 3:
        return dict(stem=f'{head} Calculate (i) the rate of natural increase as a percentage and (ii) the doubling time, using the rule of 70.',
                    answer=f'(i) {nir:.2f}% (ii) 70 / {nir:.2f} ≈ {dt:.0f} years',
                    markingKey=f'(i) M1 ({cbr} − {cdr}) / 10, A1 {nir:.2f}%. (ii) M1 70 ÷ NIR, A1 ≈ {dt:.0f} years.', marks=mk(slot, 4))
    p0 = rng.choice([12, 25, 48, 60, 110, 220])
    n = rng.choice([10, 15, 20, 25])
    p1 = p0 * (1 + nir / 100) ** n
    return dict(stem=f'{head} The population is {p0} million. (a) Calculate the NIR and the doubling time (rule of 70). '
                     f'(b) Assuming the NIR stays constant, project the population after {n} years. (c) Suggest one reason why the projection may be inaccurate.',
                answer=f'(a) {nir:.2f}%; ≈ {dt:.0f} years (b) {p0} × (1 + {nir / 100:.4f})^{n} ≈ {p1:.1f} million (c) e.g. fertility decline as the country moves through the DTM, or migration is ignored.',
                markingKey=f'(a) A1 {nir:.2f}%, A1 {dt:.0f} years. (b) M1 compound growth, A1 {p1:.1f} million (accept {p1 - 0.2:.1f}-{p1 + 0.2:.1f}). (c) R1 valid reason, e.g. falling CBR, migration, mortality shocks.',
                marks=mk(slot, 6))


DEP_C = [('Niger', 49, 3), ('Uganda', 45, 2), ('Nigeria', 42, 3), ('Kenya', 37, 3), ('India', 25, 7), ('Bangladesh', 26, 6),
         ('Mexico', 24, 8), ('Brazil', 20, 10), ('China', 17, 14), ('the USA', 18, 17), ('the UK', 17, 19), ('Germany', 14, 22),
         ('Italy', 12, 24), ('Japan', 12, 29), ('South Korea', 11, 19), ('France', 17, 21)]


@gen('dep')
def g_dep(rng, slot):
    if slot.d <= 2:
        place = rng.choice(['a district in Tanzania', 'a municipality in northern Portugal', 'a province of Vietnam',
                            'a rural county in Romania', 'a suburb of Lima', 'a prefecture in rural Japan'])
        y, w, o = rng.randint(8, 60) * 1000, rng.randint(40, 120) * 1000, rng.randint(5, 40) * 1000
        dr = (y + o) / w * 100
        return dict(stem=f'Census data for {place}: aged 0-14: {y:,}; aged 15-64: {w:,}; aged 65 and over: {o:,}. Calculate the total dependency ratio.',
                    answer=f'({y:,} + {o:,}) / {w:,} × 100 = {dr:.1f}',
                    markingKey=f'M1 (young + old) ÷ working-age × 100; A1 {dr:.1f} dependants per 100 people of working age.', marks=mk(slot, 2))
    (c1, y1, o1), (c2, y2, o2) = rng.sample(DEP_C, 2)
    w1, w2 = 100 - y1 - o1, 100 - y2 - o2
    d1, d2 = (y1 + o1) / w1 * 100, (y2 + o2) / w2 * 100
    yd1, od1 = y1 / w1 * 100, o1 / w1 * 100
    tbl = f'{c1}: 0-14 {y1}%, 15-64 {w1}%, 65+ {o1}%. {c2}: 0-14 {y2}%, 15-64 {w2}%, 65+ {o2}%.'
    if slot.d == 3:
        return dict(stem=f'The table shows the approximate age structure of two countries. {tbl} Calculate the total dependency ratio for each country and state which has the higher burden of dependency.',
                    answer=f'{c1}: {d1:.1f}; {c2}: {d2:.1f}; higher: {c1 if d1 > d2 else c2}',
                    markingKey=f'M1 method, A1 {c1} {d1:.1f}, A1 {c2} {d2:.1f}; R1 correct comparison.', marks=mk(slot, 4))
    kind = 'youthful' if y1 > o1 * 2 else 'ageing'
    return dict(stem=f'Age-structure data (percentage of total population): {tbl} (a) Calculate the young and the old dependency ratios for {c1}. '
                     f'(b) Calculate the total dependency ratio for both countries. (c) Explain one implication of the structure of {c1} for government spending.',
                answer=f'(a) young {yd1:.1f}, old {od1:.1f} (b) {c1} {d1:.1f}, {c2} {d2:.1f} (c) {c1} has a {kind} structure: '
                       + ('spending pressure on schools, maternal health and job creation.' if kind == 'youthful' else 'spending pressure on pensions, health and elderly care, with a shrinking tax base.'),
                markingKey=f'(a) A1 {yd1:.1f}, A1 {od1:.1f}. (b) A1 {d1:.1f}, A1 {d2:.1f}. (c) R1 identifies {kind} structure, R1 developed implication.', marks=mk(slot, 6))


PCT_CTX = {
    'pop': [('population of {p}', 'people', 20000, 900000, ['a peri-urban district of Dhaka', 'a municipality on the edge of Nairobi', 'a county in rural Ireland', 'a town in the Ruhr, Germany', 'a district of Kinshasa']),
            ('number of international migrants living in {p}', 'people', 5000, 90000, ['a London borough', 'a canton of Switzerland', 'a Gulf city district', 'a suburb of Toronto']),
            ('number of births registered in {p}', 'births', 800, 20000, ['a region of South Korea', 'a province of Italy', 'a prefecture of Japan', 'a district of Kerala'])],
    'climate': [('annual CO₂ emissions of {p}', 'Mt CO₂', 20, 900, ['a newly industrialised country', 'an EU member state', 'a South-East Asian economy', 'a Gulf state']),
                ('area of Arctic summer (September) sea ice measured by {p}', 'million km²', 5.5, 7.5, ['a satellite record', 'a polar research centre'], (0.6, 0.92)),
                ('number of days above 35 °C per year in {p}', 'days', 5, 60, ['a city in northern India', 'a town in southern Spain', 'an Australian inland town'], (1.05, 1.9))],
    'resource': [('daily water use per person in {p}', 'litres', 50, 400, ['a city in California', 'a town in Jordan', 'a suburb of Melbourne', 'a district of Chennai']),
                 ('meat consumption per person in {p}', 'kg per year', 10, 120, ['an East Asian middle-income country', 'a South American country', 'a South-East Asian country', 'a West African country']),
                 ('electricity generated by solar power in {p}', 'TWh', 1, 300, ['a European country', 'an Indian state', 'a Chinese province', 'a South American country'], (1.4, 2.2))],
    'water': [('mean annual discharge of a river at {p}', 'm³/s', 20, 2000, ['a gauging station in the Danube basin', 'a station on a Mekong tributary', 'a gauging station in the Murray-Darling basin']),
              ('volume of water stored in {p}', 'million m³', 50, 5000, ['a reservoir in Spain', 'a reservoir in South Africa', 'a reservoir in Turkey']),
              ('groundwater level below the surface at {p}', 'm', 5, 80, ['a well in Punjab', 'a borehole in the Central Valley', 'a well near Mexico City'])],
    'urban': [('urban population of {p}', 'million', 1, 30, ['a West African country', 'a South Asian state', 'an Andean country']),
              ('number of private cars registered in {p}', 'vehicles', 50000, 3000000, ['a Chinese city', 'a Latin American capital', 'a South-East Asian city']),
              ('mean house price in {p}', 'thousand US$', 80, 900, ['an inner-city ward undergoing gentrification', 'a regenerated docklands area', 'a suburban district'])],
}


@gen('pct')
def g_pct(rng, slot, themes=None):
    th = themes or list(PCT_CTX)
    theme = rng.choice(th)
    phrase, unit, lo, hi, places, *fr = rng.choice(PCT_CTX[theme])   # optional 6th item: (min, max) change factor
    p = rng.choice(places)
    a = rng.uniform(lo, hi)
    b = a * (rng.uniform(*fr[0]) if fr else rng.uniform(0.85, 2.2) if theme in ('pop', 'urban') else rng.uniform(0.55, 1.9))
    if hi >= 1000:
        a, b = round(a), round(b)
        sa, sb = f'{a:,}', f'{b:,}'
    else:
        a, b = round(a, 1), round(b, 1)
        sa, sb = r1(a), r1(b)
    if a == b:
        return None
    n = rng.choice([10, 12, 15, 20])
    y1 = rng.choice([1990, 1995, 2000, 2004]) if n == 20 else rng.choice([1990, 1995, 2000, 2005, 2010])
    y2 = y1 + n
    pc = (b - a) / a * 100
    sub = phrase.format(p=p)
    lead = rng.choice([f'The {sub} was {sa} {unit} in {y1} and {sb} {unit} in {y2}.',
                       f'Between {y1} and {y2} the {sub} changed from {sa} to {sb} {unit}.',
                       f'A data table shows the {sub}: {y1} - {sa} {unit}; {y2} - {sb} {unit}.'])
    if slot.d <= 3:
        return dict(stem=f'{lead} Calculate the percentage change over the period.', answer=f'{pc:+.1f}%',
                    markingKey=f'M1 (new − old) ÷ old × 100 = ({sb} − {sa}) ÷ {sa} × 100; A1 {pc:+.1f}% (sign or "increase/decrease" required).',
                    marks=mk(slot, 2))
    cagr = ((b / a) ** (1 / n) - 1) * 100
    return dict(stem=f'{lead} Calculate (a) the percentage change and (b) the average annual compound rate of change over the {n} years.',
                answer=f'(a) {pc:+.1f}% (b) {cagr:+.2f}% per year',
                markingKey=f'(a) M1 A1 {pc:+.1f}%. (b) M1 (new/old)^(1/{n}) − 1, A1 {cagr:+.2f}% per year (simple average {pc / n:+.2f}% earns M0 A0).',
                marks=mk(slot, 4))


def pct_theme(nm, themes):
    def fn(rng, slot):
        return g_pct(rng, slot, themes)
    GENS[nm] = ('C3', (1, 5), fn, 'numerical', 'data')


for _t in PCT_CTX:
    pct_theme(f'pct_{_t}', [_t])

DENS = [('Bangladesh', 171.5, 148460), ('Mongolia', 3.4, 1564116), ('Singapore', 5.9, 734), ('Australia', 26.6, 7692024),
        ('the Netherlands', 17.9, 41850), ('Canada', 40.1, 9984670), ('Nigeria', 223.8, 923768), ('Egypt', 112.7, 1001450),
        ('Japan', 124.5, 377975), ('Rwanda', 14.1, 26338), ('Iceland', 0.39, 103000), ('India', 1428.6, 3287263)]


@gen('density')
def g_density(rng, slot):
    if slot.d <= 2:
        place = rng.choice(['an island in the Philippines', 'a district in the Nile delta', 'a Scottish Highland council area',
                            'a Saharan region of Algeria', 'a commune in the Mekong delta', 'a sparsely populated Andean province'])
        pop = rng.randint(4, 900) * 1000
        area = rng.randint(50, 30000)
        dn = pop / area
        return dict(stem=f'{place[0].upper() + place[1:]} has a population of {pop:,} and an area of {area:,} km². Calculate its population density.',
                    answer=f'{dn:.1f} people per km²', markingKey=f'M1 population ÷ area; A1 {dn:.1f} people/km² (units required).', marks=mk(slot, 2))
    (a, pa, aa), (b, pb, ab) = rng.sample(DENS, 2)
    da, db = pa * 1e6 / aa, pb * 1e6 / ab
    ratio = max(da, db) / min(da, db)
    return dict(stem=f'{a[0].upper() + a[1:]} has a population of about {pa} million and an area of {aa:,} km²; {b} has about {pb} million people in {ab:,} km². '
                     f'(a) Calculate the population density of each. (b) How many times more densely populated is the denser country? (c) Explain why national density can hide uneven distribution, using one of these countries.',
                answer=f'(a) {a}: {da:,.1f} /km²; {b}: {db:,.1f} /km² (b) ≈ {ratio:,.1f} times (c) e.g. most people cluster in favourable areas (coasts, river valleys, cities) while deserts/mountains are almost empty.',
                markingKey=f'(a) A1 {da:,.1f}, A1 {db:,.1f}. (b) A1 {ratio:,.1f}. (c) R1 uneven distribution explained with a physical or human factor.', marks=mk(slot, 5))


# Spearman contexts: (xlabel, ylabel, sign, frame, places, (xlo, xhi, xdp), (ylo, yhi, ydp))
SP_CTX = {
    'urban': [
        ('distance from the CBD (km)', 'land value (US$ per m²)', -1, 'sample points along a transect from the CBD of {city}', ['Nairobi', 'Kuala Lumpur', 'Lima', 'Lisbon', 'Hanoi', 'Toronto'], (0.2, 6, 1), (150, 5000, 0)),
        ('distance from the city centre (km)', 'percentage of green space', 1, 'wards of {city} surveyed in a fieldwork project', ['Melbourne', 'Vienna', 'Seoul', 'Cape Town', 'Mexico City'], (0.5, 15, 1), (2, 60, 0)),
        ('distance from the peak land value intersection (m)', 'pedestrian count (per 10 min)', -1, 'streets surveyed in central {city}', ['Oslo', 'Lisbon', 'Dubai', 'Vienna', 'Bogotá'], (50, 2000, 0), (5, 400, 0)),
        ('distance from the city centre (km)', 'air temperature at 22:00 (°C)', -1, 'a night-time temperature transect across {city}', ['Paris', 'Delhi', 'Tokyo', 'Madrid', 'Athens'], (0, 20, 1), (18, 27, 1)),
        ('distance from the city centre (km)', 'mean household income (US$ thousand)', 1, 'census districts of {city}', ['Chicago', 'Sydney', 'Johannesburg', 'Santiago'], (0.5, 25, 1), (8, 90, 1)),
        ('index of multiple deprivation score', 'life expectancy (years)', -1, 'wards of {city} (public health data)', ['Glasgow', 'Manchester', 'Liverpool', 'Birmingham'], (5, 60, 1), (70, 86, 1)),
    ],
    'phys': [
        ('distance downstream (km)', 'channel width (m)', 1, 'sites along a river in {city} studied by students', ['the Lake District', 'the Ardennes', 'the Blue Mountains', 'the Black Forest', 'the Jura'], (0.5, 20, 1), (0.8, 14, 1)),
        ('distance downstream (km)', 'mean pebble long axis (mm)', -1, 'sites on a stream in {city}', ['Snowdonia', 'the Vosges', 'the Southern Alps, New Zealand', 'the Cairngorms'], (0.5, 18, 1), (15, 160, 0)),
        ('mean slope angle (°)', 'infiltration rate (mm/h)', -1, 'sites in a drainage basin in {city}', ['Snowdonia', 'the Pyrenees', 'Kerala', 'Yunnan'], (2, 35, 0), (3, 90, 0)),
        ('percentage of impermeable surface', 'lag time (hours)', -1, 'small urban sub-catchments in {city}', ['Manchester', 'Hamburg', 'Kuala Lumpur', 'São Paulo'], (5, 85, 0), (1.5, 16, 1)),
        ('distance from the coast (km)', 'mean annual rainfall (mm)', -1, 'weather stations inland from the coast of {city}', ['Western Australia', 'Namibia', 'Chile', 'Peru'], (2, 200, 0), (150, 1400, 0)),
        ('percentage vegetation cover', 'infiltration rate (mm/h)', 1, 'quadrats on hillslopes in {city}', ['the Peak District', 'Tasmania', 'the Drakensberg', 'Sri Lanka\'s hill country'], (5, 100, 0), (4, 120, 0)),
    ],
    'dev': [
        ('GDP per capita (US$ thousand, PPP)', 'CO₂ emissions per capita (t)', 1, 'a sample of countries compiled by a class in {city}', ['Geneva', 'Singapore', 'Accra', 'Oslo', 'Bogotá'], (1, 70, 1), (0.1, 18, 1)),
        ('female mean years of schooling', 'total fertility rate', -1, 'a sample of countries in {city}', ['sub-Saharan Africa and South Asia', 'Africa, Asia and Latin America'], (1, 13, 1), (1.2, 6.8, 1)),
        ('GDP per capita (US$ thousand, PPP)', 'life expectancy at birth (years)', 1, 'a sample of countries from {city}', ['the World Bank database', 'UNDP Human Development Report data'], (1, 70, 1), (55, 84, 1)),
        ('urban population (%)', 'total fertility rate', -1, 'a sample of countries from {city}', ['UN DESA data', 'the World Population Data Sheet'], (15, 95, 0), (1.3, 6.5, 1)),
        ('GDP per capita (US$ thousand, PPP)', 'employment in agriculture (%)', -1, 'a sample of countries from {city}', ['ILO data', 'World Bank data'], (1, 70, 1), (2, 75, 0)),
    ],
}
SP_CRIT = {6: 0.829, 7: 0.714, 8: 0.643, 9: 0.600, 10: 0.564, 11: 0.536, 12: 0.503}   # one-tailed 0.05


def ranks_desc(v):
    order = sorted(range(len(v)), key=lambda i: -v[i])
    rk = [0] * len(v)
    for r_, i in enumerate(order, 1):
        rk[i] = r_
    return rk


def _num(v, dp):
    return f'{v:.{dp}f}' if dp else str(int(v))


def spearman_fn(themes):
    def fn(rng, slot):
        xl, yl, sign, frame, places, (xlo, xhi, xdp), (ylo, yhi, ydp) = rng.choice([c for t in themes for c in SP_CTX[t]])
        n = {1: 6, 2: 6, 3: 8, 4: 10, 5: 12}.get(slot.d, 8)
        noise = rng.choice([0.05, 0.12, 0.2, 0.35])
        xs = [round(rng.uniform(xlo, xhi), xdp) for _ in range(n)]
        ys = []
        for x in xs:
            t = (x - xlo) / (xhi - xlo)
            t = t if sign > 0 else 1 - t
            t = min(1, max(0, t + rng.uniform(-noise, noise)))
            ys.append(round(ylo + (yhi - ylo) * t, ydp))
        if len(set(xs)) < n or len(set(ys)) < n:
            return None
        rx, ry = ranks_desc(xs), ranks_desc(ys)
        d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
        rs = 1 - 6 * d2 / (n * (n * n - 1))
        crit = SP_CRIT[n]
        sig = abs(rs) >= crit
        city = rng.choice(places)
        rows = '; '.join(f'{chr(65 + i)}: {_num(xs[i], xdp)}, {_num(ys[i], ydp)}' for i in range(n))
        lead = rng.choice(['The data below were collected for', 'A student recorded the following data for', 'The table shows data for'])
        stem = (f'{lead} {frame.format(city=city)} (site: {xl}, {yl}).\n{rows}.\n'
                f'Calculate Spearman\'s rank correlation coefficient (rs = 1 − 6Σd² / (n³ − n)) and state whether the relationship '
                f'is significant at the 0.05 level (one-tailed test; critical value for n = {n}: {crit}).')
        if slot.d >= 4:
            stem += ' Suggest one geographical reason for the relationship and one limitation of the data.'
        direction = 'negative' if rs < 0 else 'positive'
        ans = f'Σd² = {d2}; rs = 1 − 6×{d2}/({n}³ − {n}) = {rs:.3f}; a {direction} correlation that is {"significant" if sig else "not significant"} at the 0.05 level.'
        return dict(stem=stem, answer=ans, marks=mk(slot, 4 if slot.d <= 3 else 6), type='numerical',
                    markingKey=f'M1 ranking both variables (rank 1 = highest); M1 d² summed: Σd² = {d2}; A1 rs = {rs:.3f}; '
                               f'R1 |rs| {">=" if sig else "<"} {crit} so {"reject" if sig else "accept"} the null hypothesis. '
                               + ('R1 plausible geographical explanation; R1 limitation e.g. small sample, correlation is not causation.' if slot.d >= 4 else ''))
    return fn


for _nm, _th in (('spearman', ['urban', 'phys', 'dev']), ('spearman_urban', ['urban']), ('spearman_phys', ['phys']), ('spearman_dev', ['dev'])):
    GENS[_nm] = ('C3', (2, 5), spearman_fn(_th), 'numerical', 'data')


NNI_CTX = [('convenience stores in a district of {c}', ['Tokyo', 'Seoul', 'Taipei', 'Bangkok']),
           ('rural settlements on a 1:50 000 map of {c}', ['the Paris Basin', 'the Ganges plain', 'East Anglia', 'the Nile delta']),
           ('mobile-phone repair kiosks in an informal market in {c}', ['Nairobi', 'Lagos', 'Accra', 'Dhaka']),
           ('primary schools in a county in {c}', ['Kenya', 'Ireland', 'Poland', 'Nepal']),
           ('wells in a drylands district of {c}', ['Niger', 'Rajasthan', 'Mali', 'Botswana']),
           ('coffee shops in the CBD of {c}', ['Melbourne', 'Vienna', 'Lisbon', 'Toronto'])]


@gen('nni', d=(2, 5))
def g_nni(rng, slot):
    what, cs = rng.choice(NNI_CTX)
    n = rng.randint(12, 60)
    A = rng.choice([4, 9, 16, 25, 36, 50, 64, 100])
    dbar = round(rng.uniform(0.1, 1.6) * math.sqrt(A / n), 2)
    rn = 2 * dbar * math.sqrt(n / A)
    pat = 'clustered' if rn < 0.7 else 'tending towards clustered' if rn < 0.9 else 'random' if rn <= 1.2 else 'tending towards regular' if rn < 1.8 else 'regular (uniform)'
    stem = (f'A student mapped {n} {what.format(c=rng.choice(cs))} within a study area of {A} km². The mean distance between each '
            f'point and its nearest neighbour was {dbar} km. Calculate the nearest-neighbour index (Rn = 2d̄√(n/A)) and describe the pattern.')
    if slot.d >= 4:
        stem += ' Explain one limitation of the nearest-neighbour index for this study.'
    return dict(stem=stem, answer=f'Rn = 2 × {dbar} × √({n}/{A}) = {rn:.2f}; pattern {pat} (0 = clustered, 1.0 = random, 2.15 = perfectly regular).',
                markingKey=f'M1 substitution; A1 Rn = {rn:.2f}; R1 interpretation: {pat}. '
                           + ('R1 limitation e.g. choice of boundary changes A and Rn; it ignores clusters within a generally regular pattern; physical barriers ignored.' if slot.d >= 4 else ''),
                marks=mk(slot, 3 if slot.d <= 3 else 5))


@gen('discharge', d=(2, 5))
def g_discharge(rng, slot):
    k = rng.randint(4, 7)
    width = round(rng.uniform(1.5, 12), 1)
    depths = [round(rng.uniform(0.08, 0.9), 2) for _ in range(k)]
    v = round(rng.uniform(0.15, 1.4), 2)
    md = sum(depths) / k
    area = width * md
    q = area * v
    site = rng.choice(['site 3 on the River Kent, Cumbria', 'a riffle on a tributary of the Rhône', 'a site on the Afon Glaslyn, Wales',
                       'a stream draining the Cameron Highlands, Malaysia', 'a site on a tributary of the Waikato, New Zealand',
                       'a station on a headwater stream of the Ganges'])
    stem = (f'At {site}, students measured a channel width of {width} m and depths of {", ".join(str(x) for x in depths)} m at equal '
            f'intervals across the channel. Mean velocity (from a flow meter) was {v} m/s. Calculate the cross-sectional area and the discharge.')
    ans = f'Mean depth {md:.3f} m; area = {width} × {md:.3f} = {area:.2f} m²; Q = {area:.2f} × {v} = {q:.2f} m³/s (cumecs)'
    key = f'M1 mean depth {md:.3f} m; A1 area {area:.2f} m²; M1 Q = A × v; A1 {q:.2f} m³/s with units.'
    if slot.d >= 4:
        wp = round(width + 2 * md * rng.uniform(1.0, 1.6), 2)
        hr = area / wp
        stem += f' The wetted perimeter was {wp} m: calculate the hydraulic radius and explain what it shows about channel efficiency.'
        ans += f'; hydraulic radius = {area:.2f} / {wp} = {hr:.3f} m - a higher value means less water is in contact with the bed and banks, so less energy is lost to friction (more efficient).'
        key += f' A1 hydraulic radius {hr:.3f} m; R1 efficiency explanation.'
    return dict(stem=stem, answer=ans, markingKey=key, marks=mk(slot, 4 if slot.d <= 3 else 6))


@gen('gradient', d=(1, 4))
def g_gradient(rng, slot):
    scale = rng.choice([25000, 50000])
    cm = round(rng.uniform(2, 14), 1)
    dist = cm * scale / 100      # metres
    h1 = rng.randint(80, 600)
    drop = rng.randint(10, 300)
    h2 = h1 - drop
    grad = dist / drop
    deg = math.degrees(math.atan(drop / dist))
    ctx = rng.choice(['a stream long profile', 'a valley-side slope', 'a hillslope above a landslide scar',
                      'the course of a river between two contour crossings', 'a street climbing out of a river valley'])
    stem = (f'On a 1:{scale:,} map, two points on {ctx} are {cm} cm apart. The upper point is at {h1} m and the lower point at {h2} m. '
            'Calculate the real horizontal distance and the average gradient (as 1 in n).')
    if slot.d >= 3:
        stem += ' Also give the slope angle in degrees.'
    return dict(stem=stem, answer=f'Distance = {cm} × {scale:,} cm = {dist:,.0f} m; gradient = {drop} / {dist:,.0f} = 1 in {grad:.1f}' + (f'; angle = tan⁻¹({drop}/{dist:,.0f}) = {deg:.1f}°' if slot.d >= 3 else ''),
                markingKey=f'A1 distance {dist:,.0f} m; M1 vertical ÷ horizontal; A1 1 in {grad:.1f}' + (f'; A1 {deg:.1f}°.' if slot.d >= 3 else '.'),
                marks=mk(slot, 3 if slot.d <= 2 else 4))


@gen('hydrograph', d=(1, 4))
def g_hydrograph(rng, slot):
    if rng.random() < 0.5:
        basin = rng.choice(['a small urban catchment in Kuala Lumpur', 'the Valency catchment at Boscastle, Cornwall', 'a steep upland catchment in the Pennines',
                            'a catchment draining Mumbai\'s northern suburbs', 'a deforested hillslope catchment in Nepal', 'an urban stream in Hamburg'])
        lag = rng.randint(1, 8)
    else:
        basin = rng.choice(['the River Severn at Bewdley', 'the chalk River Itchen, Hampshire', 'a forested catchment in the Black Forest',
                            'the Loire at Orléans', 'a large lowland catchment in the Murray-Darling basin', 'a peat-covered catchment in the Scottish Highlands'])
        lag = rng.randint(10, 36)
    pr = rng.randint(0, 23)
    base = round(rng.uniform(2, 40), 1)
    peak = round(base * rng.uniform(2, 9), 1)
    stem = (f'A storm hydrograph for {basin} shows peak rainfall at {pr:02d}:00 on day 1 and peak discharge {lag} hours later. '
            f'Discharge rose from a baseflow of {base} m³/s to a peak of {peak} m³/s.')
    hours_after = (pr + lag)
    day = 1 + hours_after // 24
    t = hours_after % 24
    if slot.d <= 2:
        return dict(stem=stem + ' State the time of peak discharge and the lag time.', answer=f'Peak at {t:02d}:00 on day {day}; lag time {lag} hours',
                    markingKey=f'A1 {t:02d}:00 day {day}; A1 lag time {lag} h (time from peak rainfall to peak discharge).', marks=mk(slot, 2))
    rise = peak - base
    flash = 'flashy (short lag, steep rising limb)' if lag <= 8 else 'subdued (long lag, gentle rising limb)'
    return dict(stem=stem + ' (a) Calculate the lag time and the increase in discharge above baseflow. (b) Describe the shape of the hydrograph and suggest two catchment characteristics that explain it.',
                answer=f'(a) {lag} h; {rise:.1f} m³/s above baseflow (b) {flash}; e.g. ' + ('impermeable urban surfaces, steep slopes, thin soils, high drainage density' if lag <= 8 else 'permeable rock, forest interception, gentle slopes, large basin'),
                markingKey=f'(a) A1 {lag} h, A1 {rise:.1f} m³/s. (b) R1 shape, R1 R1 two linked catchment factors.', marks=mk(slot, 5))


@gen('recurrence', d=(2, 5))
def g_recurrence(rng, slot):
    n = rng.choice([10, 12, 15])
    peaks = sorted(rng.sample(range(120, 2400, 7), n), reverse=True)
    m = rng.randint(1, 5)
    ri = (n + 1) / m
    prob = 100 / ri
    river = rng.choice(['the River Ouse at York', 'the Elbe at Dresden', 'the Brisbane River', 'the Yamuna at Delhi', 'the Mississippi at St Louis (scaled)', 'the Rhine at Cologne'])
    yrs = rng.randint(1995, 2008)
    stem = (f'Annual maximum discharges (m³/s) recorded for {river} over {n} years ({yrs}-{yrs + n - 1}), ranked from highest: {", ".join(map(str, peaks))}. '
            f'Calculate the recurrence interval of the flood ranked {m} ({peaks[m - 1]} m³/s) using RI = (n + 1)/m, and its annual probability.')
    if slot.d >= 4:
        stem += ' Explain why planners should be cautious when using this result.'
    return dict(stem=stem, answer=f'RI = ({n} + 1)/{m} = {ri:.1f} years; probability ≈ {prob:.1f}% in any year',
                markingKey=f'M1 (n+1)/m; A1 {ri:.1f} years; A1 {prob:.1f}%. ' + ('R1 short record; climate and land-use change make past floods a poor guide to future frequency (non-stationarity).' if slot.d >= 4 else ''),
                marks=mk(slot, 3 if slot.d <= 3 else 5))


WATER_C = [('Saudi Arabia', 2.4, 36.9), ('Jordan', 0.94, 11.3), ('Egypt', 57.5, 112.7), ('India', 1911, 1428.6), ('Bangladesh', 1227, 171.5),
           ('the UK', 147, 67.7), ('Brazil', 8647, 216.4), ('Israel', 1.78, 9.7), ('Pakistan', 246.8, 240.5), ('Kenya', 30.7, 55.1),
           ('Canada', 2902, 40.1), ('China', 2840, 1410.0)]


@gen('water_stress', d=(1, 4))
def g_water(rng, slot):
    c, km3, popm = rng.choice(WATER_C)
    pc = km3 * 1e9 / (popm * 1e6)
    cls = 'no water stress' if pc >= 1700 else 'water stress' if pc >= 1000 else 'water scarcity' if pc >= 500 else 'absolute water scarcity'
    frm = rng.choice([f'{c[0].upper() + c[1:]} has total renewable water resources of about {km3} km³ per year and a population of about {popm} million.',
                      f'FAO AQUASTAT lists total renewable freshwater for {c} as roughly {km3} km³/yr; the population is approximately {popm} million.'])
    stem = frm + ' Calculate the renewable water available per person (m³ per year) and classify it using the Falkenmark indicator (1,700 / 1,000 / 500 m³).'
    if slot.d >= 3:
        future = popm * rng.choice([1.2, 1.3, 1.5])
        pcf = km3 * 1e9 / (future * 1e6)
        stem += f' If the population grows to {future:.1f} million with no change in supply, what would the new figure be?'
        return dict(stem=stem, answer=f'{pc:,.0f} m³/person/yr ({cls}); future {pcf:,.0f} m³/person/yr',
                    markingKey=f'M1 km³ × 10⁹ ÷ population; A1 {pc:,.0f} m³; R1 {cls}; A1 {pcf:,.0f} m³.', marks=mk(slot, 4))
    return dict(stem=stem, answer=f'{pc:,.0f} m³ per person per year: {cls}', markingKey=f'M1 conversion (1 km³ = 10⁹ m³); A1 {pc:,.0f}; R1 {cls}.', marks=mk(slot, 3))


EF_C = [('Qatar', 14.3, 1.0), ('the USA', 8.0, 3.4), ('Australia', 6.6, 12.3), ('Germany', 4.7, 1.5), ('China', 3.7, 0.9),
        ('Brazil', 2.6, 8.6), ('India', 1.2, 0.4), ('Kenya', 1.0, 0.5), ('Japan', 4.4, 0.6), ('Canada', 8.1, 14.0), ('Bangladesh', 0.8, 0.4)]


@gen('footprint', d=(1, 4))
def g_fp(rng, slot):
    c, ef, bc = rng.choice(EF_C)
    ef = round(ef * rng.uniform(0.95, 1.05), 1)
    gl = 1.6
    earths = ef / gl
    bal = bc - ef
    stem = rng.choice([f'Global Footprint Network data give {c} an ecological footprint of about {ef} global hectares (gha) per person and a biocapacity of {bc} gha per person.',
                       f'{c[0].upper() + c[1:]}: ecological footprint ≈ {ef} gha/person; biocapacity ≈ {bc} gha/person.'])
    stem += f' World biocapacity is about {gl} gha per person. Calculate (a) the ecological balance per person and (b) how many Earths would be needed if everyone lived like the average resident.'
    return dict(stem=stem, answer=f'(a) {bal:+.1f} gha per person ({"ecological reserve" if bal > 0 else "ecological deficit"}) (b) {ef} / {gl} ≈ {earths:.1f} Earths',
                markingKey=f'(a) M1 biocapacity − footprint, A1 {bal:+.1f} gha and correct label. (b) M1 A1 {earths:.1f} Earths.', marks=mk(slot, 4))


VW = [('beef', 15400, 'kg'), ('chocolate', 17000, 'kg'), ('rice', 2500, 'kg'), ('wheat bread', 1600, 'kg'), ('cotton T-shirt (250 g)', 2700, 'shirt'),
      ('cup of coffee', 130, 'cup'), ('chicken meat', 4300, 'kg'), ('apples', 820, 'kg'), ('cheese', 3200, 'kg'), ('avocados', 1980, 'kg')]


@gen('virtual_water', d=(1, 4))
def g_vw(rng, slot):
    k = 2 if slot.d <= 2 else 3
    items = rng.sample(VW, k)
    qty = [rng.choice([0.5, 1, 2, 3, 5, 10]) if u == 'kg' else rng.randint(1, 6) for _, _, u in items]
    parts = [f'{q:g} {u if u == "kg" else u + "(s)"} of {nm}' if u == 'kg' else f'{q} {nm}' for (nm, _, u), q in zip(items, qty)]
    tot = sum(v * q for (_, v, _), q in zip(items, qty))
    ref = ', '.join(f'{nm} {v:,} L per {u}' for nm, v, u in items)
    who = rng.choice(['a household in Madrid', 'a student in Singapore', 'a family in Toronto', 'a café in Melbourne', 'a school canteen in Geneva'])
    stem = (f'Water Footprint Network averages: {ref}. Calculate the virtual water embedded in a weekly purchase by {who} of {", ".join(parts)}.')
    if slot.d >= 3:
        stem += ' Explain why virtual water trade matters for water-scarce importing countries.'
    return dict(stem=stem, answer=f'{tot:,.0f} litres' + ('; importing water-intensive goods lets scarce countries (e.g. Jordan, Egypt) "save" domestic water, but creates dependence on exporters.' if slot.d >= 3 else ''),
                markingKey='M1 multiplying each quantity by its water content; A1 ' + f'{tot:,.0f} L.' + (' R1 virtual-water explanation.' if slot.d >= 3 else ''),
                marks=mk(slot, 2 if slot.d <= 2 else 4))


@gen('energy_mix', d=(1, 5))
def g_mix(rng, slot):
    c = rng.choice(['a European country', 'a Latin American country', 'an East Asian economy', 'a sub-Saharan African country', 'an Indian state'])
    src = ['coal', 'natural gas', 'oil', 'nuclear', 'hydro', 'wind', 'solar']
    vals = {s: rng.randint(0, 120) for s in src}
    vals['coal'] += 10
    tot = sum(vals.values())
    ren = vals['hydro'] + vals['wind'] + vals['solar']
    fos = vals['coal'] + vals['natural gas'] + vals['oil']
    tbl = ', '.join(f'{s} {vals[s]} TWh' for s in src)
    stem = f'Electricity generation in {c} in one year: {tbl}. Calculate the percentage of electricity from renewable sources.'
    ans = f'Total {tot} TWh; renewables {ren} TWh = {ren / tot * 100:.1f}%'
    key = f'M1 total {tot} TWh; M1 renewables (hydro + wind + solar) {ren}; A1 {ren / tot * 100:.1f}%.'
    if slot.d >= 3:
        stem += ' Also calculate the share from fossil fuels and the share that is low-carbon (renewables + nuclear).'
        ans += f'; fossil {fos / tot * 100:.1f}%; low-carbon {(ren + vals["nuclear"]) / tot * 100:.1f}%'
        key += f' A1 fossil {fos / tot * 100:.1f}%; A1 low-carbon {(ren + vals["nuclear"]) / tot * 100:.1f}%.'
    if slot.d >= 5:
        stem += ' Evaluate how secure this energy mix is.'
        key += ' R1 R1 security judgement: diversity of supply, dependence on imported fuels, intermittency of wind/solar.'
    return dict(stem=stem, answer=ans, markingKey=key, marks=mk(slot, 3 if slot.d <= 2 else 5 if slot.d <= 4 else 7))


CO2_C = [('China', 11900, 1410), ('the USA', 4900, 335), ('India', 2800, 1428), ('Russia', 1800, 144), ('Japan', 1000, 124.5),
         ('Germany', 670, 84), ('Saudi Arabia', 690, 37), ('Indonesia', 690, 278), ('Brazil', 480, 216), ('Nigeria', 130, 224),
         ('Bangladesh', 100, 172), ('Qatar', 110, 2.7), ('Ethiopia', 19, 127)]


@gen('carbon', d=(1, 5))
def g_carbon(rng, slot):
    (a, ea, pa), (b, eb, pb) = rng.sample(CO2_C, 2)
    pca, pcb = ea / pa, eb / pb
    world = 37400
    if slot.d <= 2:
        return dict(stem=f'{a[0].upper() + a[1:]} emitted about {ea:,} Mt of CO₂ from fossil fuels in a recent year and has a population of about {pa} million. Calculate the emissions per person.',
                    answer=f'{ea:,} / {pa} = {pca:.2f} t CO₂ per person', markingKey=f'M1 Mt ÷ million people = t per person; A1 {pca:.2f} t.', marks=mk(slot, 2))
    stem = (f'Recent fossil CO₂ emissions: {a} ≈ {ea:,} Mt (population ≈ {pa} million); {b} ≈ {eb:,} Mt (≈ {pb} million). World total ≈ {world:,} Mt. '
            f'Calculate for each country (a) the share of world emissions and (b) emissions per capita.')
    ans = f'(a) {a} {ea / world * 100:.2f}%, {b} {eb / world * 100:.2f}% (b) {a} {pca:.2f} t, {b} {pcb:.2f} t per person'
    key = f'A1 {ea / world * 100:.2f}%, A1 {eb / world * 100:.2f}%, A1 {pca:.2f} t, A1 {pcb:.2f} t.'
    if slot.d >= 4:
        stem += ' (c) Explain why the two measures could lead to different views on which country should reduce emissions more.'
        key += ' R1 R1 total vs per-capita responsibility, development stage / historic emissions (common but differentiated responsibilities).'
    return dict(stem=stem, answer=ans, markingKey=key, marks=mk(slot, 4 if slot.d <= 3 else 6))


ALB = [('fresh snow', 0.85), ('sea ice', 0.6), ('open ocean', 0.06), ('tropical rainforest', 0.13), ('desert sand', 0.4),
       ('grassland', 0.25), ('asphalt road', 0.05), ('a white "cool" roof', 0.7), ('cropland', 0.2), ('coniferous forest', 0.09)]


@gen('albedo', d=(1, 4))
def g_albedo(rng, slot):
    (s1, a1), (s2, a2) = rng.sample(ALB, 2)
    inc = rng.choice([180, 240, 300, 340, 420])
    abs1, abs2 = inc * (1 - a1), inc * (1 - a2)
    if slot.d <= 2:
        return dict(stem=f'Incoming shortwave radiation at a site is {inc} W/m². The surface is {s1} with an albedo of {a1}. Calculate the radiation reflected and absorbed.',
                    answer=f'reflected {inc * a1:.1f} W/m²; absorbed {abs1:.1f} W/m²', markingKey=f'M1 albedo × incoming; A1 {inc * a1:.1f} reflected; A1 {abs1:.1f} absorbed.', marks=mk(slot, 3))
    return dict(stem=f'Incoming shortwave radiation is {inc} W/m². A surface of {s1} (albedo {a1}) is replaced by {s2} (albedo {a2}). Calculate the change in absorbed radiation and explain its significance for climate feedbacks.',
                answer=f'Absorbed changes from {abs1:.1f} to {abs2:.1f} W/m², a change of {abs2 - abs1:+.1f} W/m²; ' + ('more energy absorbed - warming, e.g. ice-albedo positive feedback.' if abs2 > abs1 else 'less energy absorbed - a cooling effect.'),
                markingKey=f'M1 (1 − albedo) × incoming for both; A1 {abs1:.1f} and {abs2:.1f}; A1 change {abs2 - abs1:+.1f} W/m²; R1 feedback explained.', marks=mk(slot, 4))


@gen('uhi', d=(1, 4))
def g_uhi(rng, slot):
    city = rng.choice(['Paris', 'Delhi', 'Tokyo', 'Madrid', 'Athens', 'Phoenix', 'Cairo', 'Melbourne', 'Shanghai', 'London'])
    n = rng.choice([6, 7, 8])
    dists = [0] + sorted(rng.sample(range(1, 25), n - 1))
    peak = rng.uniform(22, 32)
    temps = [round(peak - 0.25 * d - rng.uniform(0, 0.8), 1) for d in dists]
    uhi = max(temps) - min(temps)
    grad = (temps[0] - temps[-1]) / dists[-1]
    rows = ', '.join(f'{d} km {t} °C' for d, t in zip(dists, temps))
    stem = f'A night-time car traverse from central {city} to its rural edge recorded: {rows}. Calculate the urban heat island intensity (maximum − minimum temperature).'
    if slot.d >= 3:
        stem += ' Also calculate the mean temperature gradient (°C per km) from the centre to the last point, and give two reasons for the pattern.'
        return dict(stem=stem, answer=f'UHI intensity {uhi:.1f} °C; gradient {grad:.2f} °C/km; reasons e.g. heat stored in concrete and asphalt (low albedo, high thermal capacity), anthropogenic heat, less evapotranspiration, canyon geometry trapping longwave radiation.',
                    markingKey=f'A1 {uhi:.1f} °C; M1 A1 {grad:.2f} °C/km; R1 R1 two reasons.', marks=mk(slot, 5))
    return dict(stem=stem, answer=f'{max(temps)} − {min(temps)} = {uhi:.1f} °C', markingKey=f'A1 {uhi:.1f} °C with units.', marks=mk(slot, 2))


STAT_CTX = {
    'phys': [('pebble long-axis lengths (mm) at a site on the River {r}', ['Wharfe', 'Tees', 'Ourthe', 'Isar', 'Dart'], 12, 140),
             ('infiltration times (seconds for 100 ml) at sites in a catchment in {r}', ['the Pennines', 'the Jura', 'Kerala', 'Tasmania'], 8, 300),
             ('channel depths (cm) measured across the River {r}', ['Kent', 'Afon Glaslyn', 'Ilz', 'Waipa'], 5, 95),
             ('slope angles (°) along a hillslope profile in {r}', ['Snowdonia', 'the Vosges', 'Yunnan', 'the Drakensberg'], 2, 38)],
    'hum': [('pedestrian counts per 10 minutes at sites in {r}', ['Lisbon city centre', 'central Vienna', 'Orchard Road, Singapore', 'Shibuya, Tokyo'], 5, 380),
            ('environmental quality scores (out of 40) in wards of {r}', ['Bogotá', 'Cape Town', 'Mumbai', 'Seoul'], 4, 40),
            ('household water use (litres per person per day) from a questionnaire in {r}', ['Amman', 'Chennai', 'Cape Town', 'Lima'], 40, 260),
            ('journey times to work (minutes) given by residents of {r}', ['Lagos', 'Jakarta', 'São Paulo', 'Nairobi'], 10, 150),
            ('household sizes recorded in a survey in {r}', ['Dharavi, Mumbai', 'Kibera, Nairobi', 'a village in Niger', 'a suburb of Seoul'], 1, 12)],
}


def stats_fn(themes):
    def fn(rng, slot):
        what, ps, lo, hi = rng.choice([c for t in themes for c in STAT_CTX[t]])
        n = {1: 7, 2: 9, 3: 11, 4: 11, 5: 12}[slot.d]
        data = [rng.randint(lo, hi) for _ in range(n)]
        s = sorted(data)
        mean = sum(s) / n

        def medf(v):
            k = len(v)
            return v[k // 2] if k % 2 else (v[k // 2 - 1] + v[k // 2]) / 2
        med = medf(s)
        rng_ = s[-1] - s[0]
        stem = f'The following {what.format(r=rng.choice(ps))} were recorded: {", ".join(map(str, data))}.'
        if slot.d <= 2:
            return dict(stem=stem + ' Calculate the mean, median and range.', answer=f'mean {mean:.1f}; median {med:g}; range {rng_}',
                        markingKey=f'A1 mean {mean:.1f}; A1 median {med:g} (data ordered); A1 range {rng_}.', marks=mk(slot, 3))
        lower, upper = s[: n // 2], s[(n + 1) // 2:]
        q1, q3 = medf(lower), medf(upper)
        sd = math.sqrt(sum((x - mean) ** 2 for x in s) / n)
        stem += ' Calculate the median, the interquartile range (quartiles as medians of the lower and upper halves) and the standard deviation (σ = √(Σ(x − x̄)²/n)).'
        if slot.d >= 5:
            stem += ' Explain why the IQR may be a better measure of dispersion than the range for these data.'
        return dict(stem=stem, answer=f'median {med:g}; Q1 {q1:g}, Q3 {q3:g}, IQR {q3 - q1:g}; σ = {sd:.2f}',
                    markingKey=f'A1 median {med:g}; M1 quartiles from ordered data (Q1 {q1:g}, Q3 {q3:g}); A1 IQR {q3 - q1:g}; M1 A1 σ = {sd:.2f}.'
                               + (' R1 IQR ignores extreme values / outliers.' if slot.d >= 5 else ''), marks=mk(slot, 5 if slot.d <= 4 else 6))
    return fn


for _nm, _th in (('stats', ['phys', 'hum']), ('stats_phys', ['phys']), ('stats_hum', ['hum'])):
    GENS[_nm] = ('C3', (1, 5), stats_fn(_th), 'numerical', 'data')


CHI_CTX = {
    'hum': [('land-use categories recorded at {tot} random sample points in {p}', ['residential', 'commercial', 'industrial', 'open space'], ['the inner city of Manchester', 'a district of Johannesburg', 'central Hanoi']),
            ('reasons for moving given by {tot} migrants interviewed in {p}', ['employment', 'family', 'education', 'housing'], ['Shenzhen', 'Dubai', 'Nairobi']),
            ('the mode of transport of {tot} shoppers interviewed in {p}', ['car', 'bus/metro', 'bicycle', 'walking', 'taxi/ride-hail'], ['Copenhagen', 'Bogotá', 'Kuala Lumpur']),
            ('the housing type of {tot} households sampled in {p}', ['detached', 'semi-detached', 'terraced', 'apartment'], ['a Dublin suburb', 'a district of Melbourne', 'a ward of Bristol'])],
    'phys': [('the aspect of {tot} landslide scars mapped in {p}', ['north-facing', 'east-facing', 'south-facing', 'west-facing'], ['the Nepal Himalaya', 'Hong Kong country parks', 'the Italian Alps']),
             ('the shape (Powers\' categories) of {tot} pebbles sampled on a river bar in {p}', ['angular', 'sub-angular', 'sub-rounded', 'rounded'], ['the Lake District', 'the Ardennes', 'Snowdonia']),
             ('the land cover at {tot} points sampled across a drainage basin in {p}', ['forest', 'grassland', 'arable', 'urban'], ['Devon', 'the Black Forest', 'the Cameron Highlands'])],
}
CHI_CRIT = {1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49}


def chi_fn(themes):
    def fn(rng, slot):
        what, cats, ps = rng.choice([c for t in themes for c in CHI_CTX[t]])
        k = len(cats)
        tot = rng.choice([40, 48, 60, 80, 100])
        tot -= tot % k
        e = tot / k
        cuts = sorted(rng.sample(range(1, tot), k - 1))
        obs = [b - a for a, b in zip([0] + cuts, cuts + [tot])]
        if min(obs) < 1:
            return None
        chi = sum((o - e) ** 2 / e for o in obs)
        df = k - 1
        crit = CHI_CRIT[df]
        rows = ', '.join(f'{c} {o}' for c, o in zip(cats, obs))
        stem = (f'A fieldwork survey recorded {what.format(p=rng.choice(ps), tot=tot)}: {rows}. Test the null hypothesis that there is no preference between '
                f'categories using the chi-squared test (χ² = Σ(O − E)²/E; critical value at 0.05 for {df} degrees of freedom = {crit}).')
        sig = chi >= crit
        return dict(stem=stem, answer=f'E = {e:g} per category; χ² = {chi:.2f}; df = {df}; {"significant - reject" if sig else "not significant - accept"} the null hypothesis',
                    markingKey=f'M1 expected {tot}/{k} = {e:g}; M1 Σ(O − E)²/E; A1 χ² = {chi:.2f}; A1 df = {df}; R1 compare with {crit}: {"reject" if sig else "accept"} H₀.',
                    marks=mk(slot, 5))
    return fn


for _nm, _th in (('chi', ['hum', 'phys']), ('chi_hum', ['hum']), ('chi_phys', ['phys'])):
    GENS[_nm] = ('C3', (3, 5), chi_fn(_th), 'numerical', 'data')


@gen('migration', d=(1, 4))
def g_migration(rng, slot):
    c, pop, ilo, ihi, elo, ehi = rng.choice([('Germany', 84, 8, 18, 5, 12), ('Canada', 40, 8, 14, 1, 3), ('the Philippines', 114, 0.2, 1, 2, 6),
                                             ('Poland', 37, 1, 4, 1, 4), ('Australia', 27, 7, 20, 3, 6), ('Mexico', 129, 0.5, 2, 1, 4),
                                             ('Spain', 48, 10, 25, 4, 9), ('Nepal', 30, 0.5, 2, 8, 20), ('the UAE', 10, 30, 80, 10, 40)])
    imm = round(pop * rng.uniform(ilo, ihi))
    emi = round(pop * rng.uniform(elo, ehi))
    if imm < 1 or emi < 1:
        return None
    nm = (imm - emi) / (pop * 1000) * 1000
    if slot.d <= 2:
        return dict(stem=f'In one year {c} (population {pop} million) received {imm} thousand immigrants and lost {emi} thousand emigrants. Calculate the net migration rate per 1,000 people.',
                    answer=f'({imm} − {emi}) thousand / {pop} million × 1,000 = {nm:+.1f} per 1,000',
                    markingKey=f'M1 immigrants − emigrants; A1 {nm:+.1f} per 1,000.', marks=mk(slot, 2))
    nir0 = {'Germany': -3, 'Canada': 1, 'the Philippines': 13, 'Poland': -2, 'Australia': 4, 'Mexico': 8, 'Spain': -1, 'Nepal': 11, 'the UAE': 10}[c]
    nir = round(nir0 + rng.uniform(-1, 1), 1)
    tot = nir + nm
    return dict(stem=f'{c[0].upper() + c[1:]} (population {pop} million) has a natural increase of {nir} per 1,000. In one year it received {imm} thousand immigrants and {emi} thousand people emigrated. '
                     'Calculate the net migration rate and the overall rate of population change per 1,000, and state which component dominates.',
                answer=f'net migration {nm:+.1f} per 1,000; total change {tot:+.1f} per 1,000; dominant component: {"migration" if abs(nm) > abs(nir) else "natural change"}',
                markingKey=f'A1 {nm:+.1f}; M1 natural change + net migration; A1 {tot:+.1f}; R1 {"migration" if abs(nm) > abs(nir) else "natural change"}.', marks=mk(slot, 4))


# (country, remittances % of GDP, approximate GDP US$ billion, ODA as a fraction of remittances) - World Bank / OECD, early 2020s
REM_C = [('Tajikistan', 45, 12, 0.07), ('Nepal', 26, 41, 0.13), ('Lebanon', 30, 20, 0.23), ('Honduras', 26, 34, 0.07), ('El Salvador', 24, 34, 0.04),
         ('the Philippines', 9, 437, 0.04), ('Mexico', 4, 1790, 0.01), ('India', 3.4, 3550, 0.025), ('Egypt', 5, 396, 0.1), ('Kyrgyzstan', 19, 14, 0.2),
         ('Bangladesh', 5, 437, 0.23), ('Nigeria', 5, 363, 0.18)]


@gen('remit', d=(1, 4))
def g_remit(rng, slot):
    c, share, gdp0, odar = rng.choice(REM_C)
    gdp = round(gdp0 * rng.uniform(0.9, 1.1))
    rem = gdp * share / 100 * rng.uniform(0.9, 1.1)
    s = rem / gdp * 100
    stem = f'{c[0].upper() + c[1:]} received about US${rem:.1f} billion in personal remittances in a year when its GDP was about US${gdp:,} billion. Calculate remittances as a percentage of GDP.'
    if slot.d >= 3:
        aid = rem * odar * rng.uniform(0.8, 1.25)
        stem += f' Official development assistance (ODA) was US${aid:.1f} billion: how many times larger were remittances? Explain one advantage of remittances over aid for households.'
        return dict(stem=stem, answer=f'{s:.1f}% of GDP; {rem / aid:.1f} times ODA; remittances go directly to families (spent on food, schooling, housing) and are counter-cyclical.',
                    markingKey=f'A1 {s:.1f}%; A1 {rem / aid:.1f}×; R1 R1 developed advantage.', marks=mk(slot, 4))
    return dict(stem=stem, answer=f'{s:.1f}%', markingKey=f'M1 remittances ÷ GDP × 100; A1 {s:.1f}%.', marks=mk(slot, 2))


@gen('rank_size', d=(2, 5))
def g_rank(rng, slot):
    c = rng.choice(['Peru', 'Thailand', 'Kenya', 'Argentina', 'Germany', 'India', 'Uruguay', 'Bangladesh'])
    p1 = round(rng.uniform(2, 12), 1)
    others = sorted([round(p1 / k * rng.uniform(0.25, 1.4), 2) for k in range(2, 6)], reverse=True)
    pops = [p1] + others
    prim = p1 / pops[1]
    expect = [p1 / k for k in range(1, 6)]
    rows = '; '.join(f'rank {i + 1}: {p} million' for i, p in enumerate(pops))
    stem = f'The five largest cities in a census of {c} (rounded, illustrative): {rows}. Calculate the primacy index (P1/P2) and the populations predicted by the rank-size rule (Pn = P1/n) for ranks 2-5.'
    if slot.d >= 4:
        stem += ' Explain what your results suggest about the urban hierarchy.'
    return dict(stem=stem, answer=f'primacy = {p1} / {pops[1]} = {prim:.2f}; predicted ' + ', '.join(f'{e:.2f}' for e in expect[1:]) + ' million',
                markingKey=f'A1 primacy {prim:.2f}; M1 P1/n; A1 predictions; ' + ('R1 primacy > 2 indicates a primate city dominating the hierarchy, typical where the capital concentrates investment.' if slot.d >= 4 else ''),
                marks=mk(slot, 4 if slot.d <= 3 else 6))


@gen('urban_pct', d=(1, 5))
def g_urban(rng, slot):
    c = rng.choice(['Nigeria', 'Bangladesh', 'Kenya', 'Indonesia', 'Ethiopia', 'Vietnam', 'Pakistan', 'Tanzania', 'Egypt'])
    tot = round(rng.uniform(20, 230), 1)
    share = rng.uniform(0.2, 0.6)
    urb = round(tot * share, 1)
    pc = urb / tot * 100
    if slot.d <= 2:
        return dict(stem=f'{c} has a total population of {tot} million, of whom {urb} million live in urban areas. Calculate the level of urbanisation.',
                    answer=f'{pc:.1f}%', markingKey=f'M1 urban ÷ total × 100; A1 {pc:.1f}%.', marks=mk(slot, 2))
    g = round(rng.uniform(2, 5.5), 1)
    n = rng.choice([10, 15, 20])
    fut = urb * (1 + g / 100) ** n
    dt = 70 / g
    return dict(stem=f'{c} has {urb} million urban residents out of {tot} million. The urban population is growing at {g}% per year. Calculate (a) the current level of urbanisation, (b) the doubling time of the urban population and (c) the urban population in {n} years if the rate is constant.',
                answer=f'(a) {pc:.1f}% (b) {dt:.1f} years (c) {fut:.1f} million',
                markingKey=f'A1 {pc:.1f}%; M1 A1 70/{g} = {dt:.1f}; M1 compound growth A1 {fut:.1f} million.', marks=mk(slot, 5))


@gen('sampling', d=(1, 4))
def g_sampling(rng, slot):
    pops = {'owner-occupied': rng.randint(200, 900), 'privately rented': rng.randint(100, 700), 'social housing': rng.randint(50, 500)}
    n = rng.choice([40, 50, 60, 80, 100])
    tot = sum(pops.values())
    alloc = {k: v / tot * n for k, v in pops.items()}
    area = rng.choice(['a ward in Bristol', 'a district of Melbourne', 'a neighbourhood of Toronto', 'an estate in Dublin', 'a suburb of Cape Town'])
    if slot.d <= 2:
        street = rng.randint(120, 600)
        k = rng.choice([10, 15, 20, 25])
        return dict(stem=f'A student wants a systematic sample of {k} households from a list of {street} houses on the electoral register of {area}. Calculate the sampling interval and explain how the sample is selected.',
                    answer=f'interval = {street} / {k} = {street / k:.1f} → every {round(street / k)}th house, starting from a random number between 1 and {round(street / k)}',
                    markingKey=f'A1 interval ≈ {round(street / k)}; R1 random start then every nth.', marks=mk(slot, 2))
    rows = ', '.join(f'{k} {v}' for k, v in pops.items())
    return dict(stem=f'Households in {area} by tenure: {rows}. A student will interview {n} households using stratified sampling. Calculate how many of each tenure type should be interviewed, and give one advantage of stratified sampling here.',
                answer='; '.join(f'{k} {v:.1f} ≈ {round(v)}' for k, v in alloc.items()) + '; advantage: each tenure group is represented in proportion, reducing sampling bias.',
                markingKey='M1 (group ÷ total) × sample; A1 all three values (rounded, total = sample size); R1 advantage.', marks=mk(slot, 4))


@gen('sea_level', d=(1, 4))
def g_sea(rng, slot):
    st = rng.choice(['Manila', 'Venice', 'Dhaka (Bay of Bengal gauge)', 'Rotterdam', 'Jakarta', 'Funafuti, Tuvalu', 'Miami', 'Lagos'])
    y1 = rng.choice([1970, 1980, 1990, 1993])
    y2 = y1 + rng.choice([20, 25, 30])
    h1 = rng.randint(6900, 7100)
    rate = rng.uniform(2.0, 12.0)
    h2 = round(h1 + rate * (y2 - y1))
    rr = (h2 - h1) / (y2 - y1)
    yrs = rng.choice([50, 75])
    stem = f'Tide-gauge records at {st} show mean sea level of {h1} mm (relative to a local datum) in {y1} and {h2} mm in {y2}. Calculate the mean rate of relative sea-level rise.'
    if slot.d >= 3:
        stem += f' Project the additional rise over the next {yrs} years at this rate, and explain why the rate here may differ from the global mean (about 3.7 mm/yr recently).'
        return dict(stem=stem, answer=f'{rr:.1f} mm/yr; ≈ {rr * yrs / 10:.0f} cm in {yrs} years; local subsidence (groundwater pumping, delta compaction), tectonics or ocean circulation alter relative rise.',
                    markingKey=f'A1 {rr:.1f} mm/yr; A1 {rr * yrs:.0f} mm; R1 R1 relative vs eustatic explanation.', marks=mk(slot, 4))
    return dict(stem=stem, answer=f'{rr:.1f} mm per year', markingKey=f'M1 change ÷ years; A1 {rr:.1f} mm/yr.', marks=mk(slot, 2))


@gen('yield', d=(1, 4))
def g_yield(rng, slot):
    crop = rng.choice([('maize', 'Malawi'), ('rice', 'Vietnam'), ('wheat', 'India (Punjab)'), ('sorghum', 'Burkina Faso'), ('cassava', 'Nigeria'), ('soybeans', 'Brazil (Mato Grosso)')])
    area = rng.randint(200, 9000)
    y1 = rng.uniform(0.8, 6)
    y2 = y1 * rng.uniform(0.7, 2.2)
    p1, p2 = area * y1, area * y2 * rng.uniform(0.9, 1.1)
    yy1, yy2 = p1 / area, p2 / area
    stem = (f'A cooperative growing {crop[0]} in {crop[1]} harvested {p1:,.0f} t from {area:,} ha in 2005 and {p2:,.0f} t from the same area in 2020. '
            'Calculate the yield (t/ha) in each year and the percentage change in yield.')
    pc = (yy2 - yy1) / yy1 * 100
    if slot.d >= 3:
        stem += ' Suggest two reasons for the change.'
    return dict(stem=stem, answer=f'{yy1:.2f} t/ha → {yy2:.2f} t/ha; {pc:+.1f}%' + ('; e.g. improved seeds/fertiliser/irrigation (if rising) or drought, soil degradation, pests (if falling).' if slot.d >= 3 else ''),
                markingKey=f'A1 {yy1:.2f}, A1 {yy2:.2f}, A1 {pc:+.1f}%.' + (' R1 R1 two reasons consistent with the direction.' if slot.d >= 3 else ''),
                marks=mk(slot, 3 if slot.d <= 2 else 5))


@gen('carbon_tax', d=(2, 5))
def g_ctax(rng, slot):
    juris = rng.choice([('Sweden', 'SEK', 1200), ('Canada (federal fuel charge)', 'CAD', 80), ('Switzerland', 'CHF', 120), ('the EU ETS (allowance price)', '€', 85), ('Singapore', 'SGD', 25), ('South Africa', 'ZAR', 190)])
    j, cur, price = juris
    em = rng.randint(2, 900) * 1000
    cut = rng.choice([10, 15, 20, 25, 30])
    cost = em * price
    cost2 = em * (1 - cut / 100) * price
    stem = (f'A cement plant covered by {j} emits {em:,} t CO₂ per year. The carbon price is about {cur} {price} per tonne. '
            f'Calculate the annual carbon cost, and the saving if the plant cuts emissions by {cut}%.')
    if slot.d >= 4:
        stem += ' Evaluate carbon pricing as a mitigation strategy.'
    return dict(stem=stem, answer=f'cost {cur} {cost:,.0f}; after cut {cur} {cost2:,.0f}; saving {cur} {cost - cost2:,.0f}',
                markingKey=f'A1 {cur} {cost:,.0f}; M1 A1 saving {cur} {cost - cost2:,.0f}.' + (' R1 R1 incentive to cut emissions / revenue recycling vs carbon leakage, regressive impacts, prices often too low.' if slot.d >= 4 else ''),
                marks=mk(slot, 3 if slot.d <= 3 else 6))


@gen('mapscale', d=(1, 3))
def g_scale(rng, slot):
    sc = rng.choice([10000, 25000, 50000, 100000, 250000])
    cm = round(rng.uniform(1.5, 18), 1)
    real = cm * sc / 100000
    feat = rng.choice(['the CBD and a peripheral shopping mall', 'two settlements on a river floodplain', 'a dam and the town downstream',
                       'two sampling sites on a beach transect', 'a refugee camp and the nearest market town', 'two weather stations'])
    return dict(stem=f'On a map at a scale of 1:{sc:,}, the straight-line distance between {feat} measures {cm} cm. Calculate the real distance in kilometres.',
                answer=f'{cm} × {sc:,} = {cm * sc:,.0f} cm = {real:.2f} km', markingKey=f'M1 multiply by the scale; A1 {real:.2f} km (unit conversion correct).', marks=mk(slot, 2))


def pc(a, b):
    return f'{(b - a) / a * 100:+.1f}%'


# =============================================================================================
# Unit 1 Changing population
# =============================================================================================
S('ch01-st1', gens=['density', 'pct_pop', 'mapscale'],
  terms=[('population distribution', 'the way in which people are spread out across an area, described as even, uneven, clustered or sparse'),
         ('population density', 'the number of people per unit area, usually people per km²; total population ÷ land area'),
         ('ecumene', 'the permanently inhabited part of the Earth\'s surface'),
         ('physiological density', 'the number of people per unit of arable (cultivable) land, a better indicator of pressure on farmland than crude density'),
         ('sparsely populated area', 'an area with few people per km², often limited by extreme climate, relief, poor soils or remoteness')],
  facts=[('Approximately what share of the world\'s population lives in Asia?', 'About 59%', ['About 25%', 'About 40%', 'About 80%'], 'Asia has about 4.8 of the world\'s 8.1 billion people (≈59%).'),
         ('Which statement best describes the distribution of Egypt\'s population?', 'About 95% live on roughly 5% of the land, along the Nile valley and delta', ['It is evenly spread across the country', 'Most people live in the Western Desert oases', 'Most people live along the Red Sea coast'], 'The Nile provides water and fertile alluvium in an otherwise hyper-arid country.'),
         ('In 2023, which country overtook China as the most populous in the world?', 'India', ['Indonesia', 'Nigeria', 'the USA'], 'UN DESA estimated India passed about 1.43 billion in April 2023.'),
         ('Which factor best explains the very low population density of Mongolia (about 2 people per km²)?', 'An extreme continental climate, arid steppe and desert, and limited arable land', ['Its high level of urbanisation', 'Strict anti-natalist laws', 'A tropical rainforest climate'], 'Physical constraints limit farming; much of the population is nomadic or in Ulaanbaatar.')],
  why=[('Explain why population density is a limited measure of population distribution.', 'Density is an average for a whole area; it hides uneven clustering within it (e.g. Australia averages 3.5 /km² but about 85% of people live within 50 km of the coast), and ignores land quality, so physiological density may be more meaningful.'),
       ('Explain why river valleys and deltas often have high population densities.', 'They provide reliable water for drinking and irrigation, fertile alluvial soils, flat land for building and transport routes (e.g. the Nile, Ganges and Mekong deltas).'),
       ('Explain how human factors can produce high population densities in physically unfavourable areas.', 'Economic opportunity (e.g. oil wealth in Gulf cities), political decisions (planned capitals such as Brasília), technology (desalination, air-conditioning) and historical trade routes can attract and support large populations despite harsh climate.'),
       ('Explain why most Canadians live close to the border with the USA.', 'About 90% live within about 160 km of the US border, where the climate is milder, the growing season longer, soils better and trade links with the USA strongest; the north is cold, has permafrost and is remote.')],
  contrast=[('population density', 'population distribution', 'Density is a numerical measure (people per km²) for an area; distribution describes the spatial pattern of where people are located (clustered, linear, dispersed) and is shown on a dot map.'),
            ('crude population density', 'physiological density', 'Crude density divides population by total land area; physiological density divides by arable land only, so Egypt\'s physiological density is many times higher than its crude density.')],
  misc=[('Countries with high population densities are always poor and overpopulated.', 'Density does not determine wealth: Singapore and the Netherlands are densely populated and rich; overpopulation depends on resources and technology relative to population.'),
        ('Population distribution today is mainly the result of climate.', 'Climate matters, but human factors (economic development, history, politics, accessibility) now strongly influence distribution, e.g. the growth of Dubai in a desert.'),
        ('A low national population density means everyone lives far apart.', 'National averages mask clustering: Australians are concentrated in a few coastal cities such as Sydney and Melbourne.')],
  apply=[('Using a named country, describe the pattern of population distribution and suggest two reasons for it.', 'e.g. Australia: concentrated on the east and south-east coast (Sydney, Melbourne, Brisbane) and around Perth; the interior is sparsely populated because of aridity, high temperatures and distance; coasts have moderate climate, ports and historic colonial settlement.', 3),
         ('Suggest why Java holds over half of Indonesia\'s population on about 7% of its land area.', 'Fertile volcanic soils support intensive wet-rice farming; colonial and post-colonial investment and the capital Jakarta concentrated jobs and infrastructure on Java.', 3)],
  cases=[('the Nile valley and delta, Egypt', 'about 95% of Egypt\'s 110+ million people live on roughly 5% of the land beside the river', 'the influence of water availability on population distribution', 'the river creates a linear belt of high density through a hyper-arid desert'),
         ('Australia', 'around 85% of people live within 50 km of the coast, yet the national density is only about 3.5 people per km²', 'the uneven distribution hidden by a national average', 'a low average density conceals a highly clustered coastal pattern'),
         ('Japan\'s Tokaido corridor', 'the Tokyo-Nagoya-Osaka belt holds around half of Japan\'s population on coastal plains, as about 70% of Japan is mountainous', 'the role of relief in population distribution', 'mountains confine dense settlement to narrow lowland plains'),
         ('Dubai, United Arab Emirates', 'the city grew from under 100,000 people in 1970 to over 3.5 million on oil, trade and tourism wealth in a hot desert', 'the role of economic factors in overriding physical limits', 'investment, migrant labour and technology (desalination, air-conditioning) support a large population in an arid environment')],
  evaluate=[('Physical factors are more important than human factors in explaining global population distribution.', ['large empty areas coincide with deserts, ice caps and high mountains', 'early agricultural civilisations clustered in fertile river valleys (Nile, Indus, Huang He)'], ['economic opportunity and technology now override physical limits (Gulf cities, Singapore)', 'political and historical factors (colonial ports, planned capitals, migration policies) shape distribution'], 'Physical factors set broad global limits, but human factors increasingly explain where people cluster within habitable areas.'),
            ('Population density is the most useful indicator of population pressure on resources.', ['easy to calculate and compare between countries', 'high densities can signal pressure on land and services'], ['it ignores resource levels, technology and trade (Singapore vs Bangladesh)', 'physiological density or footprint data may be more meaningful'], 'Density is a useful starting point but must be combined with resource and development indicators.')],
  extended=[('Examine the relative importance of physical and human factors in explaining the population distribution of one named country.', 'Award for specific locations, figures and factors: e.g. Brazil - coastal concentration (São Paulo, Rio) from colonial history and the coastal economy; sparse Amazon interior (dense forest, poor soils, disease) but growth along BR-highways and in Manaus Free Trade Zone; planned capital Brasília 1960; judgement balancing both.', 10, 'long')],
  res=[('Table: population and area of three countries (approximate) - Bangladesh 171 million, 148,460 km²; Mongolia 3.4 million, 1,564,116 km²; Netherlands 17.9 million, 41,850 km².',
        [('Calculate the population density of each country and rank them.', f'Bangladesh {171e6 / 148460:,.0f} /km²; Netherlands {17.9e6 / 41850:,.0f} /km²; Mongolia {3.4e6 / 1564116:.1f} /km²; ranking Bangladesh > Netherlands > Mongolia.'),
         ('Using the data, explain why density alone does not indicate living standards.', 'The Netherlands has a high density but is a high-income country; Bangladesh is denser and lower-income; Mongolia is sparsely populated but not wealthy - density is unrelated to development without considering resources, economy and technology.')]),
       ('A dot map of Canada shows a band of dots within about 160 km of the US border, dense clusters around Toronto, Montreal and Vancouver, and almost no dots north of 60° N.',
        [('Describe the distribution shown on the map.', 'Highly uneven and linear: concentrated in the south along the US border, clustered in a few large cities; very sparse in the north.'),
         ('Suggest two reasons for the distribution shown.', 'Milder climate and longer growing season in the south; trade/transport links to the USA and historic settlement along the St Lawrence; the north has permafrost, cold and isolation.')])])

S('ch01-st2', gens=['rank_size', 'urban_pct', 'pct_urban'],
  terms=[('megacity', 'an urban agglomeration with a population of more than 10 million'),
         ('core-periphery model', 'Friedmann\'s model of uneven development in which a dynamic, wealthy core region dominates a poorer, dependent periphery'),
         ('backwash effect', 'the flow of people, capital and resources from the periphery to the core that increases regional inequality'),
         ('spread effect', 'the diffusion of growth from the core to the periphery, e.g. through demand for raw materials and the relocation of industry'),
         ('cumulative causation', 'Myrdal\'s idea that once a region gains an advantage, multiplier effects attract further investment and growth')],
  facts=[('Which city was the world\'s largest urban agglomeration in UN 2018 estimates, with about 37 million people?', 'Tokyo', ['Delhi', 'Shanghai', 'Mexico City'], 'Tokyo (37.4 million in 2018), followed by Delhi and Shanghai; Delhi is projected to overtake it around 2028.'),
         ('According to the UN (2018 revision), how many megacities were there in 2018?', '33', ['10', '19', '60'], 'There were 33 megacities in 2018, projected to rise to 43 by 2030, most in Asia and Africa.'),
         ('In which region are most of the world\'s fastest-growing megacities located?', 'South Asia and sub-Saharan Africa', ['Western Europe', 'North America', 'Australasia'], 'Cities such as Dhaka, Lagos and Kinshasa are growing by natural increase and rural-urban migration.')],
  why=[('Explain why most megacity growth now occurs in low- and middle-income countries.', 'High natural increase (youthful populations) combines with large rural-urban migration flows driven by rural poverty and urban jobs; high-income countries are already highly urbanised and have low fertility.'),
       ('Explain how cumulative causation can widen the gap between core and periphery.', 'Initial advantages attract firms and migrants; the multiplier effect creates jobs, tax revenue and services, attracting further investment, while backwash drains young, skilled people and capital from the periphery.'),
       ('Explain why primate cities develop in some countries.', 'Colonial administration and ports concentrated investment in one city; governments locate ministries, airports and universities there; economies of scale attract TNCs, so the city becomes many times larger than the second city (e.g. Lima, Bangkok).'),
       ('Explain how population change in the periphery can differ from that in the core region.', 'The periphery loses young adults through out-migration, leaving an ageing population and lower birth totals; the core gains young migrants, raising natural increase and population growth.')],
  contrast=[('the core', 'the periphery', 'The core is the dominant region with high investment, wages and population growth (e.g. coastal eastern China); the periphery is less developed, dependent and often losing population (e.g. western interior China).'),
            ('backwash effects', 'spread effects', 'Backwash effects move resources and people towards the core and increase inequality; spread effects transmit growth outward to the periphery and reduce it.')],
  misc=[('Megacities grow only because of rural-urban migration.', 'Natural increase within the city is often as important as migration, especially where migrants are young adults with high fertility (e.g. Lagos).'),
        ('The core-periphery pattern is permanent once it forms.', 'Friedmann argued that spread effects and government policy can reduce inequality over time, e.g. China\'s Western Development Strategy (from 2000).'),
        ('Most megacities are in high-income countries.', 'Only a minority are (e.g. Tokyo, Osaka, New York, Los Angeles, Paris); most are in Asia, Latin America and Africa.')],
  apply=[('Using a named country, describe its core-periphery pattern and one consequence for population change.', 'e.g. China: the eastern coastal core (Pearl River Delta, Yangtze River Delta) attracted FDI and hundreds of millions of internal migrants, so interior provinces such as Sichuan and Guizhou lost working-age people and aged faster.', 3),
         ('Suggest two challenges faced by a rapidly growing megacity such as Lagos.', 'Housing shortages and informal settlements (e.g. Makoko), traffic congestion and inadequate transport, unreliable electricity and water, flooding of low-lying areas.', 3)],
  cases=[('Lagos, Nigeria', 'the city grew from under 1 million in 1960 to around 15 million today, through high natural increase and migration from across Nigeria and West Africa', 'megacity growth in a low-income country', 'growth outpaced infrastructure, creating informal settlements, congestion and an expanding informal economy'),
         ('the north-south divide in Italy', 'the industrial north (Milan, Turin) is far wealthier than the south, which experienced decades of out-migration', 'the core-periphery model', 'out-migration of young southerners is a backwash effect that reinforced northern growth and southern ageing'),
         ('the Pearl River Delta, China', 'Special Economic Zones such as Shenzhen (from 1980) drew FDI and tens of millions of migrants from interior provinces', 'the link between economic development and population change in a core region', 'rapid economic growth pulled young workers to the core, boosting urban populations and depopulating rural periphery'),
         ('Delhi, India', 'the urban agglomeration reached about 32 million and is projected to become the world\'s largest by around 2028', 'the shifting distribution of megacities', 'the world\'s largest cities are moving from high-income countries to Asia')],
  evaluate=[('The growth of megacities brings more benefits than problems.', ['economies of scale and agglomeration raise productivity (megacities generate a large share of national GDP)', 'better access to jobs, education and health care than rural areas'], ['informal settlements, congestion and pollution (Dhaka, Lagos)', 'regional inequality and backwash from the periphery'], 'Benefits are real but depend on governance and investment in infrastructure; without them problems can outweigh benefits for the urban poor.'),
            ('Government policy can successfully reduce core-periphery inequality.', ['China\'s Western Development Strategy and infrastructure (rail, roads) spread investment inland', 'the EU Cohesion Fund has supported growth in peripheral regions such as Poland'], ['decades of Cassa per il Mezzogiorno spending did not close Italy\'s north-south gap', 'market forces and agglomeration continue to favour the core'], 'Policy can narrow but rarely eliminate inequality; success depends on long-term investment and the strength of agglomeration forces.')],
  extended=[('Examine the relationship between economic development and population change at the national scale.', 'Indicative: as development rises, death rates then birth rates fall (DTM); urbanisation and female education reduce fertility; core regions gain migrants; examples Japan, Brazil, Niger; recognise exceptions (Gulf states, China\'s policy-driven change).', 10, 'long')],
  res=[('Graph description: number of megacities (UN DESA) - 1990: 10; 2000: 17; 2018: 33; 2030 (projected): 43.',
        [('Calculate the percentage increase in the number of megacities between 1990 and 2018.', f'(33 − 10)/10 × 100 = {pc(10, 33)}'),
         ('Describe the trend shown and suggest one reason for it.', 'Steady and accelerating increase - the number more than tripled in 28 years and is projected to reach 43; driven by rapid urban growth in Asia and Africa through natural increase and rural-urban migration.')]),
       ('Table: population of the two largest cities (approximate, millions) - Peru: Lima 10.9, Arequipa 1.1; Thailand: Bangkok 11.0, Chiang Mai 1.2 (metropolitan); Brazil: São Paulo 22.4, Rio de Janeiro 13.6.',
        [('Calculate the primacy index (largest ÷ second-largest) for each country.', f'Peru {10.9 / 1.1:.1f}; Thailand {11.0 / 1.2:.1f}; Brazil {22.4 / 13.6:.2f}.'),
         ('Using the data, identify which countries have primate cities and suggest a reason.', 'Peru and Thailand (index > 2, about 9-10); investment, government and trade are concentrated in the capital; Brazil has a more balanced hierarchy.')])])

S('ch01-st3', gens=['migration', 'pct_pop', 'chi_hum'],
  terms=[('internal migration', 'the movement of people within a country\'s borders, involving a change of permanent residence'),
         ('rural-urban migration', 'the movement of people from the countryside to towns and cities, usually for work, services and higher incomes'),
         ('push factor', 'a negative feature of the place of origin that encourages people to leave, e.g. drought, landlessness, lack of services'),
         ('pull factor', 'a perceived attraction of a destination that encourages people to move there, e.g. jobs, higher wages, education'),
         ('intervening obstacle', 'in Lee\'s model, a barrier between origin and destination, such as distance, cost, or legal restrictions like China\'s hukou')],
  facts=[('About how many rural migrant workers did China record in 2023 (National Bureau of Statistics)?', 'About 297 million', ['About 30 million', 'About 80 million', 'About 900 million'], 'The "floating population" of rural migrant workers was about 297 million in 2023.'),
         ('What is China\'s hukou?', 'A household registration system that ties access to public services to a person\'s registered place of origin', ['A tax on urban land', 'A rural pension scheme', 'A one-child certificate'], 'Hukou restrictions are an intervening obstacle and limit migrants\' access to urban schools and healthcare.'),
         ('Which of these is one of Ravenstein\'s "laws" of migration (1885)?', 'Most migrants move only a short distance', ['Most migrants are elderly', 'Migration decreases as transport improves', 'Rural people are less likely to migrate than urban people'], 'Ravenstein also noted that each flow produces a counter-flow and that long-distance migrants tend to go to large cities.')],
  why=[('Explain why rural-urban migration tends to be selective by age and gender.', 'Young adults are most likely to move because they seek work and education and have fewer ties; in many countries young men dominate flows to construction and industry, though young women dominate factory flows in some (e.g. Bangladesh garment sector).'),
       ('Explain how out-migration can affect the population structure of rural source areas.', 'Loss of young adults narrows the 20-39 bars of the pyramid, leaving older people and children; birth rates fall and dependency ratios rise, e.g. "left-behind" villages in Sichuan or rural Bulgaria.'),
       ('Explain how remittances from internal migrants can benefit rural areas.', 'Money sent home funds food, school fees, housing and farm investment; it can reduce poverty and create a multiplier effect, although it can increase dependency on urban income.'),
       ('Explain why rural-urban migration continues even when urban unemployment is high.', 'Migrants respond to expected rather than actual income (Todaro model); the informal sector offers survival work; social networks reduce risk and costs; rural push factors remain strong.')],
  contrast=[('push factors', 'pull factors', 'Push factors are negative conditions at the origin that drive people away; pull factors are attractions of the destination that draw them; most decisions combine both.'),
            ('voluntary migration', 'forced migration', 'Voluntary migration is chosen, usually for economic or social reasons; forced migration results from conflict, persecution or disaster, leaving people little or no choice.')],
  misc=[('Rural-urban migrants always become better off.', 'Many migrants end up in informal settlements and insecure informal work; outcomes depend on skills, networks and policy (e.g. hukou restrictions in China).'),
        ('Internal migration only affects the destination cities.', 'Source areas are also changed: loss of labour, ageing, remittance flows and the return of skills and ideas.'),
        ('Lee\'s model says that migration happens only because of pull factors.', 'Lee\'s model combines positive and negative factors at origin and destination, intervening obstacles and personal factors.')],
  apply=[('Using a named example, outline two consequences of internal migration for the destination area.', 'e.g. Shenzhen: supplied labour for export manufacturing, driving rapid economic growth; pressure on housing created "urban villages" (chengzhongcun) and migrants without local hukou had limited access to schools.', 4),
         ('Suggest two reasons why migrants from Bihar move to Mumbai and Delhi.', 'Push: low farm incomes, landlessness and floods in Bihar; pull: construction, manufacturing and service jobs with higher wages, and existing migrant networks.', 2)],
  cases=[('the migration of China\'s rural workers', 'about 297 million people from rural provinces such as Sichuan, Henan and Anhui work in eastern cities, many without local hukou', 'the role of intervening obstacles in internal migration', 'the hukou system lets people move but restricts urban rights, encouraging circular migration and "left-behind" children'),
         ('north-east Brazil to São Paulo', 'drought, poverty and land concentration in the Nordeste pushed millions to the industrial south-east from the 1950s', 'push and pull factors in rural-urban migration', 'rural push combined with urban jobs to swell São Paulo and its favelas'),
         ('Dhaka, Bangladesh', 'the city receives an estimated 1,700 or more migrants a day, many displaced by river-bank erosion and cyclones', 'environmental push factors in internal migration', 'environmental hazards in rural deltas add to economic push factors and accelerate urban growth'),
         ('the Bangladesh garment industry', 'about 4 million workers, mostly young women from rural districts, moved to Dhaka and Chittagong factories', 'the selectivity of migration by gender and age', 'the sector created a female-dominated migrant stream of young adults')],
  evaluate=[('The consequences of rural-urban migration are mainly negative for the places of origin.', ['loss of young, skilled labour reduces farm output and services', 'ageing and "left-behind" children in rural China'], ['remittances raise incomes and investment in housing and farming', 'reduced pressure on land and return migrants bring skills'], 'Consequences are mixed; remittances and return migration can offset losses, but long-term depopulation damages some regions.'),
            ('Government restrictions are the main factor controlling internal migration flows.', ['China\'s hukou has shaped the scale and circular nature of migration', 'some countries use permits or resettlement programmes'], ['economic differences in wages are the key driver everywhere', 'environmental hazards and social networks also shape flows'], 'Economic forces drive most internal migration; policy modifies its form more than its overall direction.')],
  extended=[('Examine the reasons for, and consequences of, rural-urban migration in one named country.', 'Award specific causes (push/pull, intervening obstacles), consequences for origin and destination with figures (e.g. China, India, Brazil, Bangladesh) and evaluation of who benefits.', 10, 'long')],
  res=[('Survey of 80 recent migrants in a Nairobi informal settlement - main reason for moving: employment 46, joining family 14, education 12, land shortage 8.',
        [('Calculate the percentage of migrants who moved mainly for employment.', f'46/80 × 100 = {46 / 80 * 100:.1f}%'),
         ('Classify each reason as push or pull and comment on what the data suggest.', 'Employment, family and education are pull factors (72 of 80 = 90%); land shortage is a push factor (10%); pull factors dominate but survey may under-record push factors.')]),
       ('Population pyramids described: Village A in rural Sichuan has narrow bars for ages 20-44 and wide bars for 0-14 and 60+; District B in Shenzhen has very wide bars for ages 20-34, especially males, and narrow bars for 60+.',
        [('Describe the differences between the two pyramids.', 'Village A has a deficit of working-age adults and many children and elderly; District B is dominated by young working adults with few elderly or children.'),
         ('Explain how internal migration accounts for the differences.', 'Young adults migrate from rural Sichuan to Shenzhen for factory work, leaving children with grandparents; hukou rules discourage family migration, so destination is adult-dominated.')])])

S('ch02-st1', gens=['nir', 'pct_pop'],
  terms=[('demographic transition model', 'a model showing how birth rates, death rates and population growth change through five stages as a country develops'),
         ('total fertility rate', 'the average number of children a woman would have during her reproductive years at current age-specific fertility rates'),
         ('replacement level fertility', 'the TFR (about 2.1 in high-income countries) needed for each generation to replace itself, excluding migration'),
         ('crude birth rate', 'the number of live births per 1,000 people per year'),
         ('natural increase', 'the difference between births and deaths in a population, excluding migration, usually expressed per 1,000 or as a percentage'),
         ('demographic momentum', 'continued population growth after fertility falls to replacement level, because of a large number of people in or entering reproductive ages')],
  facts=[('Which country had the world\'s lowest recorded total fertility rate in 2023, at about 0.72?', 'South Korea', ['Japan', 'Italy', 'Niger'], 'South Korea\'s TFR fell to 0.72 in 2023 (0.75 in 2024).'),
         ('In which stage of the DTM do birth rates fall rapidly while death rates are already low?', 'Stage 3', ['Stage 1', 'Stage 2', 'Stage 5'], 'Stage 3 (late expanding) sees falling birth rates, so natural increase slows.'),
         ('Which country has one of the world\'s highest TFRs, at around 6?', 'Niger', ['Brazil', 'India', 'Bangladesh'], 'Niger\'s TFR is about 6 children per woman, with a median age near 15.'),
         ('Which stage of the DTM, added later to the model, shows a death rate higher than the birth rate?', 'Stage 5', ['Stage 1', 'Stage 2', 'Stage 3'], 'Stage 5 (declining) is illustrated by Japan, Italy and Germany, where deaths exceed births.')],
  why=[('Explain why death rates fall before birth rates in stage 2 of the demographic transition model.', 'Improvements in food supply, clean water, sanitation and vaccination reduce mortality quickly, while high fertility persists because of cultural norms, the need for family labour and high infant mortality expectations.'),
       ('Explain why total fertility rate is a better measure of fertility than the crude birth rate.', 'TFR is not affected by the age structure of the population; CBR depends on how many women are of child-bearing age, so a youthful population may have a high CBR even if fertility per woman is falling.'),
       ('Explain how demographic momentum causes populations to keep growing after fertility falls.', 'Past high fertility produced large cohorts that are now entering reproductive age; even with two children per couple the number of births stays high for decades, e.g. India.'),
       ('Explain why the DTM may not predict the future population change of low-income countries accurately.', 'It is based on the experience of western Europe; transitions in Asia have been faster, some African countries\' fertility decline has stalled, and the model ignores migration, HIV/AIDS, policies and globalisation.')],
  contrast=[('crude birth rate', 'total fertility rate', 'CBR counts births per 1,000 of the whole population per year; TFR is the average number of children per woman over her lifetime and is independent of age structure.'),
            ('stage 2', 'stage 4 of the demographic transition model', 'In stage 2 death rates fall rapidly while birth rates remain high, so growth is rapid; in stage 4 both rates are low and growth is slow or stable.')],
  misc=[('Once a country reaches stage 4, its population stops changing.', 'Stage 4 populations can still grow slowly through momentum and immigration, or start to decline (stage 5).'),
        ('Falling death rates are mainly caused by better hospitals.', 'In stage 2 the biggest gains come from clean water, sanitation, vaccination and better nutrition rather than hospital care.'),
        ('Every country must pass through the DTM stages at the same pace.', 'Pace varies widely: South Korea and Iran moved from high to low fertility within a generation, far faster than England.')],
  apply=[('Niger has a CBR of about 44 per 1,000 and a CDR of about 9 per 1,000. Identify its DTM stage and justify your answer.', 'Stage 2 (early expanding): the death rate has fallen but the birth rate remains very high, giving a natural increase of about 3.5% per year.', 3),
         ('Japan\'s population peaked in 2008 at about 128 million. Use the DTM to explain what has happened since.', 'Japan has entered stage 5: very low fertility (TFR about 1.2) and an ageing population mean deaths exceed births, so the population has declined to about 124 million.', 3)],
  cases=[('Niger', 'a TFR of about 6, median age of around 15 and natural increase above 3% per year', 'stage 2 of the demographic transition', 'high fertility persists while mortality has fallen, giving very rapid growth'),
         ('South Korea', 'a TFR that fell from about 4.5 in 1970 to 0.72 in 2023', 'the speed of fertility decline in East Asia', 'rapid urbanisation, female education and high living costs compressed the transition into a few decades'),
         ('Japan', 'the population has fallen since 2008, with deaths exceeding births by over 800,000 a year in recent years', 'stage 5 of the demographic transition model', 'very low fertility and an elderly population cause natural decrease'),
         ('Bangladesh', 'the TFR fell from about 6.3 in the mid-1970s to around 2 by the 2020s despite low incomes', 'the role of family planning and female education in fertility decline', 'fertility fell before high incomes were reached, challenging a strictly economic reading of the DTM')],
  evaluate=[('The demographic transition model is of limited use in explaining population change in today\'s low-income countries.', ['based on 19th-century European experience; ignores migration and policy', 'some African fertility declines have stalled; HIV/AIDS raised death rates'], ['broad sequence (death rates then birth rates fall) has occurred almost everywhere', 'useful for predicting dependency and planning needs'], 'The DTM remains a useful descriptive framework, but its timing and causes must be adapted to each country.'),
            ('Economic development is the main cause of fertility decline.', ['urbanisation and higher incomes raise the cost of children', 'industrial economies reduce the need for child labour'], ['Bangladesh and Kerala show fertility can fall with low incomes through female education and family planning', 'cultural and policy factors (China\'s one-child policy, Iran\'s programme)'], 'Development helps, but female education, contraception access and policy often explain the timing and speed better.')],
  extended=[('Examine the factors that cause fertility rates to vary between countries.', 'Indicative: female education and employment, contraception, infant mortality, religion and culture, urbanisation, policy; contrasting examples (Niger vs South Korea, Kerala, Iran); judgement on most important factor.', 10, 'long')],
  res=[('Table: CBR and CDR (per 1,000) for four countries - Niger 44, 9; India 16, 7; Brazil 12, 7; Japan 6, 13.',
        [('Calculate the natural increase rate (%) for each country.', 'Niger 3.5%; India 0.9%; Brazil 0.5%; Japan −0.7% (natural decrease).'),
         ('Assign each country to a DTM stage, justifying with the data.', 'Niger stage 2 (high CBR, low CDR); India late stage 3 (falling CBR); Brazil stage 3-4 (low rates, slow growth); Japan stage 5 (CDR > CBR).')]),
       ('Line graph description: South Korea\'s TFR - 1970: 4.5; 1985: 1.7; 2000: 1.5; 2015: 1.2; 2023: 0.72.',
        [('Calculate the percentage fall in TFR between 1970 and 2023.', f'(0.72 − 4.5)/4.5 × 100 = {pc(4.5, 0.72)}'),
         ('Describe the trend and identify when the TFR fell below replacement level.', 'A rapid fall then slower continued decline; it dropped below replacement (2.1) between 1970 and 1985 (by the mid-1980s) and has continued falling to the lowest in the world.')])])

S('ch02-st2', gens=['dep', 'pct_pop', 'stats_hum'],
  terms=[('population pyramid', 'a bar chart showing the age and sex structure of a population, with males and females on either side of a central axis'),
         ('dependency ratio', 'the ratio of people of non-working age (0-14 and 65+) to people of working age (15-64), multiplied by 100'),
         ('ageing population', 'a population in which the proportion of older people (usually 65+) is increasing, raising the median age'),
         ('youthful population', 'a population with a large proportion of children under 15, typically giving a wide-based pyramid'),
         ('sex ratio', 'the number of males per 100 females in a population (or at birth)'),
         ('median age', 'the age that divides a population into two equal halves; about 15 in Niger and about 49 in Japan')],
  facts=[('What percentage of Japan\'s population was aged 65 or over in 2023?', 'About 29%', ['About 9%', 'About 15%', 'About 45%'], 'Japan has the highest share of older people of any large country (29.1% in 2023).'),
         ('Which shape of pyramid indicates high birth rates and short life expectancy?', 'A wide base that narrows rapidly towards a narrow top', ['A narrow base with a wide middle', 'Straight vertical sides', 'A bulge only in the 20-39 age group'], 'This "triangular" shape typifies stage 2 countries such as Niger or Uganda.'),
         ('What would explain a large surplus of males aged 20-40 in the population pyramid of Qatar?', 'Immigration of male migrant workers', ['A high female death rate in childbirth', 'A pro-natalist policy', 'Emigration of older men'], 'Gulf states rely on male migrant labour; Qatar has roughly three males for every female.'),
         ('What is the formula for the old-age dependency ratio?', '(population aged 65+ ÷ population aged 15-64) × 100', ['(population aged 0-14 ÷ total population) × 100', '(population aged 65+ ÷ total population) × 100', '(population aged 15-64 ÷ population aged 65+) × 100'], 'The old-age ratio compares the elderly with the working-age group.')],
  why=[('Explain why a high dependency ratio can be a challenge for a government.', 'A smaller working-age group pays taxes to fund services for dependants - schools for the young or pensions and health care for the elderly - which raises tax burdens or deficits.'),
       ('Explain why the dependency ratio is an imperfect measure of economic dependency.', 'Many 15-64-year-olds are students, unemployed or carers, while many over-65s work and many children work in low-income countries; it ignores productivity and participation rates.'),
       ('Explain how an ageing population can affect a country\'s economy.', 'A shrinking labour force can slow growth and create labour shortages; pension and health costs rise; consumption shifts towards health and care; but the "silver economy" creates new markets.'),
       ('Explain why the sex ratio at birth in China rose above 115 in the 2000s.', 'Son preference combined with the one-child policy and access to ultrasound led to sex-selective abortion, producing around 115-118 boys per 100 girls at birth.')],
  contrast=[('a youthful population', 'an ageing population', 'A youthful population has a large share under 15 and a wide-based pyramid (e.g. Uganda); an ageing population has a growing share over 65 and a narrow base with wide upper bars (e.g. Italy).'),
            ('young dependency', 'old-age dependency', 'Young dependency compares 0-14-year-olds with the working-age group and drives demand for schools; old-age dependency compares the 65+ group and drives pensions and elderly care.')],
  misc=[('An ageing population is a sign that a country is failing.', 'Ageing mainly reflects success - longer life expectancy and lower fertility - though it creates new challenges.'),
        ('A high dependency ratio always means a country has many elderly people.', 'Many of the highest dependency ratios are in youthful countries such as Niger, where the 0-14 group is about half of the population.'),
        ('Population pyramids show only the effect of births and deaths.', 'They also show migration (e.g. male bulge in the UAE), wars (missing cohorts in Russia) and past policies (China\'s one-child generation).')],
  apply=[('Describe the population structure you would expect in a city dominated by retirees, such as a coastal town in southern Spain.', 'A narrow base, small working-age bars and wide bars above 60-65, possibly with more women at the oldest ages because of higher female life expectancy.', 2),
         ('Suggest two policies that Japan could use to respond to its ageing population.', 'Raising the pension age (e.g. encouraging work to 70), increasing immigration through the Specified Skilled Worker visa, using robotics and care technology, pro-natalist childcare support.', 3)],
  cases=[('Japan', 'about 29% of the population is aged 65+, the median age is about 49 and the working-age population has been shrinking since the mid-1990s', 'the challenges of an ageing population', 'pension and care costs rise while the labour force and tax base shrink'),
         ('Uganda', 'around 45% of the population is under 15 and the median age is about 16', 'the needs of a youthful population', 'large cohorts require schools, health care and, soon, millions of new jobs'),
         ('the population of Qatar and the United Arab Emirates', 'migrant workers make up around 85-90% of the population, mostly men aged 20-45', 'the effect of migration on population structure', 'labour immigration produces a pyramid with a large male bulge in working ages'),
         ('the legacy of China\'s one-child policy', 'the 1980-2015 policy produced a narrowing base and a sex ratio at birth of about 118 by the late 2000s', 'the impact of policy on population structure', 'policy and son preference distorted both age and sex structure')],
  evaluate=[('An ageing population is a greater challenge than a youthful population.', ['rising pension and health costs with a shrinking workforce (Japan, Italy)', 'difficult to reverse once fertility is very low'], ['youthful populations need schools, jobs and health services that poor countries struggle to provide', 'a youthful population can become a demographic dividend'], 'Both are challenging; the scale depends on income, policy and timing - a youthful population with good investment offers more opportunity.'),
            ('The dependency ratio is a reliable indicator of the economic burden on the working population.', ['simple, comparable across countries', 'signals future pension and education demand'], ['ignores working elderly and non-working adults', 'ignores productivity, unemployment and informal work'], 'It is a useful but crude indicator that should be combined with labour participation data.')],
  extended=[('Examine the consequences of a changing population structure for one named country.', 'Award: named country with data (e.g. Japan 29% over 65 or Niger 49% under 15); economic, social and political consequences; responses; judgement.', 10, 'long')],
  res=[('Table: age structure (% of total population) - Niger: 0-14 49%, 15-64 48%, 65+ 3%; Italy: 0-14 12%, 15-64 64%, 65+ 24%.',
        [('Calculate the total dependency ratio for each country.', f'Niger (49 + 3)/48 × 100 = {52 / 48 * 100:.1f}; Italy (12 + 24)/64 × 100 = {36 / 64 * 100:.1f}.'),
         ('Compare the composition of dependency in the two countries.', f'Niger\'s dependency is almost entirely young (young ratio {49 / 48 * 100:.1f}, old {3 / 48 * 100:.1f}); Italy\'s is mainly old (young {12 / 64 * 100:.1f}, old {24 / 64 * 100:.1f}).')]),
       ('Description of a population pyramid for the United Arab Emirates: very narrow bars for 0-19 and 50+, but very wide male bars for ages 25-44, where males outnumber females by about three to one.',
        [('Describe the pyramid.', 'Dominated by working-age adults, especially men aged 25-44; few children and elderly; highly unbalanced sex ratio.'),
         ('Explain the shape of the pyramid.', 'Large-scale temporary male labour migration (construction, services) from South Asia under the kafala system; migrants rarely bring families or retire there.')])])

S('ch02-st3', gens=['pct_pop', 'migration'],
  terms=[('refugee', 'a person who has fled their country owing to a well-founded fear of persecution, conflict or violence and is protected under the 1951 Refugee Convention'),
         ('internally displaced person (IDP)', 'a person forced to flee their home who remains within the borders of their own country'),
         ('asylum seeker', 'a person who has applied for international protection as a refugee but whose claim has not yet been decided'),
         ('forced migration', 'movement in which people have little or no choice, caused by conflict, persecution, disasters or development projects'),
         ('non-refoulement', 'the principle of international law that refugees must not be returned to a country where they face serious threats to life or freedom'),
         ('environmental refugee', 'an informal term for a person displaced by environmental change or disaster, not recognised under the 1951 Convention')],
  facts=[('According to UNHCR, approximately how many people were forcibly displaced worldwide by mid-2024?', 'About 120 million', ['About 12 million', 'About 40 million', 'About 500 million'], 'UNHCR reported about 122.6 million forcibly displaced people in mid-2024, more than half of them IDPs.'),
         ('Which camp complex near Cox\'s Bazar, Bangladesh, hosts most of the Rohingya refugees from Myanmar?', 'Kutupalong', ['Dadaab', 'Zaatari', 'Kakuma'], 'Around 1 million Rohingya live in the Cox\'s Bazar camps, mostly arriving after August 2017.'),
         ('Which international agreement defines who is a refugee?', 'The 1951 Refugee Convention and its 1967 Protocol', ['The Paris Agreement', 'The Sendai Framework', 'The Kyoto Protocol'], 'The Convention defines refugees and establishes non-refoulement.'),
         ('Which displacement crisis became the world\'s largest after war broke out in April 2023?', 'Sudan', ['Haiti', 'Venezuela', 'Colombia'], 'Over 10 million people were displaced inside and outside Sudan.')],
  why=[('Explain why most refugees live in neighbouring low- and middle-income countries rather than in high-income countries.', 'Refugees flee to the nearest safe place; long-distance travel is costly and visas are restricted; family and ethnic ties cross borders - so countries like Turkey, Uganda, Pakistan, Bangladesh and Colombia host most refugees.'),
       ('Explain why IDPs may be more vulnerable than refugees.', 'They remain in the country affected by conflict or disaster, have no special international legal status, may be inaccessible to aid agencies and depend on the same government that may be failing or persecuting them.'),
       ('Explain how a large refugee influx can affect a host country.', 'Pressure on water, housing, schools and health care; competition for jobs and lower wages; environmental degradation around camps; but also labour supply, aid funding and new markets.'),
       ('Explain why protracted refugee situations develop.', 'Conflicts continue for years (Syria, Afghanistan, Somalia), return is unsafe, local integration is restricted and resettlement places are few, so camps such as Dadaab (Kenya, since 1991) become semi-permanent.')],
  contrast=[('a refugee', 'an internally displaced person', 'A refugee has crossed an international border and is protected by the 1951 Convention; an IDP has fled but remains inside their own country under its government\'s responsibility.'),
            ('a refugee', 'an economic migrant', 'A refugee is forced to flee persecution or conflict and cannot safely return; an economic migrant chooses to move to improve income or opportunities and can usually return home.')],
  misc=[('Most of the world\'s refugees live in Europe.', 'Around 70% live in countries neighbouring their own, and most are hosted by low- and middle-income countries such as Turkey, Iran, Colombia, Uganda and Pakistan.'),
        ('People displaced by climate disasters are legally refugees.', 'The 1951 Convention does not cover environmental displacement; most disaster-displaced people are IDPs within their own country.'),
        ('Forced migration is always temporary.', 'Many situations are protracted: some Palestinian, Afghan and Somali refugees have been displaced for decades.')],
  apply=[('Using a named example, outline two impacts of forced migration on the host area.', 'e.g. Rohingya in Cox\'s Bazar: deforestation of about 2,000+ ha of hillsides for shelters and fuelwood increased landslide risk; local wages fell and prices rose, but aid spending created jobs.', 4),
         ('Suggest two reasons why the number of forcibly displaced people has risen since 2012.', 'New and continuing conflicts (Syria, South Sudan, Ukraine, Sudan, DR Congo), persecution (Rohingya), and fewer durable solutions such as return or resettlement.', 2)],
  cases=[('the Rohingya crisis of 2017', 'over 700,000 Rohingya fled Myanmar\'s Rakhine State to Bangladesh in 2017 after military violence', 'the causes and impacts of forced migration', 'ethnic persecution caused mass flight, and the influx strained the environment and services of Cox\'s Bazar district'),
         ('the Syrian civil war', 'from 2011 over 13 million Syrians were displaced, about half as refugees, with Turkey hosting over 3 million', 'the scale and geography of conflict-driven displacement', 'most refugees remained in neighbouring countries (Turkey, Lebanon, Jordan) rather than Europe'),
         ('Ukraine after February 2022', 'about 6 million refugees were recorded across Europe and millions more became IDPs', 'the role of host-country policy in shaping refugee outcomes', 'the EU Temporary Protection Directive gave immediate rights to work, housing and schooling'),
         ('the 2022 Pakistan flood disaster', 'about 8 million people were displaced when around a third of the country was inundated', 'disaster-induced internal displacement', 'most people displaced by disasters remain IDPs within their own country')],
  evaluate=[('The impacts of refugees on host countries are mainly negative.', ['pressure on services and infrastructure (Lebanon hosted about 1 refugee per 4-5 residents)', 'environmental damage around camps (Cox\'s Bazar)'], ['refugees bring labour and skills (Syrians in Turkish industry)', 'Uganda\'s self-reliance policy allows refugees to farm and work, boosting local economies'], 'Impacts depend largely on host policies, international support and the scale and duration of displacement.'),
            ('Internal displacement is a more serious global issue than international refugee flows.', ['IDPs outnumber refugees (over 70 million conflict IDPs)', 'they lack international legal protection'], ['refugee flows cause international tensions and long-term camps', 'IDPs may return home more quickly after disasters'], 'IDPs are the larger and less protected group, so internal displacement deserves more attention.')],
  extended=[('Examine the causes and consequences of one forced migration you have studied.', 'Award: named case (Rohingya, Syria, Ukraine, Sudan), causes (persecution, conflict), numbers, consequences for source and host areas and migrants; evaluation of responses.', 10, 'long')],
  res=[('Table: forcibly displaced people worldwide (UNHCR, millions) - 2012: 45.2; 2017: 68.5; 2022: 108.4; mid-2024: 122.6.',
        [('Calculate the percentage increase between 2012 and mid-2024.', f'(122.6 − 45.2)/45.2 × 100 = {pc(45.2, 122.6)}'),
         ('Describe the trend and suggest two reasons for it.', 'A near tripling with acceleration after 2017 and 2022; new conflicts (Syria, Ukraine, Sudan, DR Congo) and protracted crises with few returns.')]),
       ('Pie chart description: share of the world\'s refugees hosted by country income group - low- and middle-income countries 71%; high-income countries 29%.',
        [('Describe what the chart shows.', 'Most (about 7 in 10) refugees are hosted by low- and middle-income countries, less than a third by high-income countries.'),
         ('Suggest two implications of this pattern.', 'The burden falls on countries least able to afford it; international funding and burden-sharing (e.g. resettlement) are needed.')])])

S('ch02-st4', gens=['remit', 'migration', 'pct_pop'],
  terms=[('remittances', 'money or goods sent by migrants to family or communities in their country of origin'),
         ('brain drain', 'the emigration of highly educated or skilled people from their country of origin'),
         ('brain gain', 'the benefit to a country from inflows of skilled migrants or the return of emigrants with new skills'),
         ('diaspora', 'a population of migrants and their descendants living outside their country of origin while keeping links with it'),
         ('circular migration', 'repeated temporary movement between origin and destination, e.g. seasonal or contract labour')],
  facts=[('Approximately how much did officially recorded remittance flows to low- and middle-income countries total in 2023 (World Bank)?', 'About US$650 billion', ['About US$65 billion', 'About US$6 billion', 'About US$6 trillion'], 'Remittances to LMICs were about US$656 billion in 2023, larger than FDI and ODA combined.'),
         ('Which country receives the largest volume of remittances in the world?', 'India', ['Mexico', 'the Philippines', 'Nigeria'], 'India received around US$120-125 billion in 2023.'),
         ('Which country has remittances equal to about 45-50% of GDP, one of the highest shares in the world?', 'Tajikistan', ['Brazil', 'China', 'South Africa'], 'Most Tajik migrants work in Russia; remittances are about 45-50% of GDP.')],
  why=[('Explain why remittances can be more effective than aid in reducing poverty.', 'They go directly to households, are spent on food, schooling, health and housing, are stable or counter-cyclical in crises and avoid government bureaucracy and corruption.'),
       ('Explain how brain drain can harm the health systems of source countries.', 'Emigration of trained doctors and nurses (e.g. from Zimbabwe or the Philippines) leaves staff shortages, wastes public spending on training and reduces access to care, especially in rural areas.'),
       ('Explain how host countries can benefit from international migration.', 'Migrants fill labour shortages (care, construction, health), pay taxes, offset ageing and bring entrepreneurship and cultural diversity, e.g. Germany and Canada.'),
       ('Explain why dependence on remittances can be risky for a source country.', 'Flows depend on host-country economies and policies (e.g. Tajikistan\'s fall when Russia\'s economy weakened in 2014-15), may discourage local investment and labour, and can widen inequality between migrant and non-migrant households.')],
  contrast=[('brain drain', 'brain circulation', 'Brain drain is the permanent loss of skilled people from a source country; brain circulation is the flow of skilled migrants back and forth, bringing skills, capital and networks home (e.g. Indian IT professionals returning to Bengaluru).'),
            ('the impacts of migration on source countries', 'the impacts on host countries', 'Source countries gain remittances but may lose young and skilled labour; host countries gain labour and taxes but may face pressure on services and social tensions.')],
  misc=[('Remittances only benefit the families who receive them.', 'Spending creates a multiplier effect in local economies (construction, shops) and earns foreign exchange for the country.'),
        ('Brain drain is always harmful to the source country.', 'Some source countries benefit from remittances, diaspora investment and return migration; the Philippines trains nurses partly for export.'),
        ('International migrants mostly move from low-income to high-income countries.', 'Large flows are South-South (e.g. Burkina Faso to Côte d\'Ivoire, Nepal to India, Bangladesh to the Gulf).')],
  apply=[('Using a named source country, outline two economic impacts of emigration.', 'e.g. the Philippines: about 10 million overseas Filipinos send remittances of roughly US$37-40 billion a year (about 9% of GDP), supporting consumption and the peso; but loss of nurses creates domestic shortages.', 4),
         ('Suggest two reasons why the Gulf states attract migrant workers from South Asia.', 'High wages relative to home, labour demand in construction and services funded by oil wealth, recruitment agencies and established networks.', 2)],
  cases=[('the Philippines', 'about 10 million overseas Filipino workers and migrants send remittances worth about 9% of GDP, and the state actively manages labour export', 'the role of remittances in a source economy', 'remittances underpin household consumption and national foreign exchange, encouraging further emigration'),
         ('the emigration of Zimbabwe\'s health workers', 'thousands of doctors and nurses have left for the UK, South Africa and elsewhere since the 2000s', 'brain drain', 'the loss of trained staff weakens health services in the source country'),
         ('Germany\'s 2015-16 asylum intake', 'about 1.2 million asylum seekers arrived in 2015-16, many from Syria', 'host-country impacts of international migration', 'initial pressure on housing and integration services was followed by many entering the labour market and offsetting ageing'),
         ('Tajik labour migration to Russia', 'around a million Tajiks work in Russia and their remittances equal about 45-50% of Tajikistan\'s GDP', 'dependence on remittances', 'the economy is highly exposed to changes in Russia\'s economy and migration rules')],
  evaluate=[('International migration brings more benefits to host countries than to source countries.', ['hosts gain labour, taxes and offset ageing (Gulf states, Germany)', 'brain drain removes skilled workers from source countries'], ['remittances are worth over US$650 billion a year to LMICs', 'return migrants bring skills and investment'], 'Both gain; hosts often gain more in the long term, but remittances make migration highly significant for source economies.'),
            ('Remittances are the most important consequence of international migration for source countries.', ['larger than ODA and often FDI', 'reduce poverty directly'], ['loss of labour and skills, family separation and ageing', 'social and cultural change from return migrants'], 'Remittances are the most visible benefit, but demographic and social consequences can be equally important.')],
  extended=[('Examine the impacts of international migration on one named source country and one named host country.', 'Award: named countries, data (remittances, numbers), economic, social, demographic and political impacts; balanced evaluation.', 10, 'long')],
  res=[('Table: remittances as % of GDP (World Bank, 2023) - Tajikistan 48; Tonga 41; Nepal 26; Philippines 9; Mexico 4; India 3.',
        [('Describe the pattern shown by the data.', 'Small, low-income countries (Tajikistan, Tonga, Nepal) depend heavily on remittances; larger economies (Mexico, India) receive large totals that are small shares of GDP.'),
         ('Explain why a high share of GDP from remittances may be a risk.', 'Vulnerability to shocks in host economies, exchange rates and migration policy; possible dependency and lower domestic investment.')]),
       ('Bar chart description: remittances to India (US$ billion) - 2010: 53; 2015: 69; 2020: 83; 2023: 120.',
        [('Calculate the percentage increase from 2010 to 2023.', f'(120 − 53)/53 × 100 = {pc(53, 120)}'),
         ('Suggest two reasons for the trend.', 'Growth of the Indian diaspora in the Gulf, USA and UK; higher-skilled migrants (IT, health) earning more; better digital transfer channels.')])])

S('ch03-st1', gens=['nir', 'dep', 'pct_pop'],
  terms=[('anti-natalist policy', 'a government policy that aims to reduce birth rates, e.g. through family planning, incentives or legal limits'),
         ('pro-natalist policy', 'a government policy that aims to increase birth rates, e.g. through child benefits, tax breaks, parental leave and childcare'),
         ('population policy', 'a set of government measures designed to influence the size, growth, structure or distribution of a population'),
         ('ageing policy', 'measures to manage the consequences of an older population, such as raising pension ages, encouraging immigration or funding elderly care'),
         ('one-child policy', 'China\'s anti-natalist policy (1980-2015) limiting most urban couples to one child, enforced by incentives and penalties')],
  facts=[('In which year did China replace its one-child policy with a universal two-child policy?', '2016', ['1979', '2000', '2023'], 'The two-child policy began in January 2016; a three-child policy followed in 2021.'),
         ('What was Singapore\'s slogan in the 1970s anti-natalist campaign?', '"Stop at Two"', ['"Have Three or More if You Can Afford It"', '"Small Family, Happy Family"', '"Children are Our Future"'], 'Singapore later reversed this with a pro-natalist policy (1987) and the Baby Bonus (2001).'),
         ('Which country introduced a lifetime income-tax exemption for mothers of four or more children in 2020?', 'Hungary', ['France', 'Japan', 'Sweden'], 'Hungary\'s family policy is one of the most generous pro-natalist packages in Europe.'),
         ('Which policy did Japan introduce in 1994 to support childbearing?', 'The Angel Plan', ['The Baby Bonus', 'The Stop at Two campaign', 'The Hukou reform'], 'The Angel Plan expanded childcare; fertility nevertheless stayed around 1.2-1.4.')],
  why=[('Explain why pro-natalist policies often have only a small effect on fertility.', 'Incentives are small relative to the lifetime cost of a child; fertility decisions reflect housing costs, women\'s careers, work culture and gender roles, which cash benefits do not change - e.g. Singapore\'s TFR stays near 1.0 despite the Baby Bonus.'),
       ('Explain why China ended its one-child policy.', 'It produced a rapidly ageing population, a shrinking labour force from about 2012, a sex ratio imbalance (about 118 boys per 100 girls) and "4-2-1" families with heavy care burdens.'),
       ('Explain why France has one of the highest fertility rates in Europe.', 'Long-standing family policy: generous family allowances, tax relief by family size (quotient familial), subsidised childcare (crèches) and paid parental leave that help women combine work and family.'),
       ('Explain why governments with ageing populations may encourage immigration.', 'Young migrants add workers and taxpayers, fill care and health shortages and slow the rise in old-age dependency, e.g. Japan\'s Specified Skilled Worker visa (2019) and Germany\'s Skilled Immigration Act (2020).')],
  contrast=[('pro-natalist policies', 'anti-natalist policies', 'Pro-natalist policies try to raise fertility (Singapore Baby Bonus, Hungary tax exemptions); anti-natalist policies try to reduce it (China\'s one-child policy, Iran\'s 1989 family planning programme).'),
            ('coercive population policies', 'incentive-based population policies', 'Coercive policies use legal force or penalties (India\'s 1975-77 forced sterilisation, China\'s fines and forced abortions); incentive-based policies rely on voluntary rewards and services.')],
  misc=[('China\'s one-child policy was the only reason for its fall in fertility.', 'Fertility had already fallen from about 5.8 (1970) to 2.7 (1979) under the earlier "later, longer, fewer" campaign; urbanisation and education also played a part.'),
        ('Pro-natalist policies always raise birth rates substantially.', 'Most produce small or temporary changes (tempo effects); South Korea spent over US$200 billion from 2006 but its TFR kept falling to 0.72.'),
        ('Raising the pension age is a pro-natalist policy.', 'It is an ageing policy that keeps people in work longer; it does not aim to raise births.')],
  apply=[('Using a named example, outline one success and one problem of an anti-natalist policy.', 'e.g. China: success - an estimated 400 million fewer births (government claim) and reduced pressure on resources; problem - rapid ageing, labour shortages and a sex ratio imbalance.', 4),
         ('Suggest two measures, other than cash payments, that could raise fertility in South Korea.', 'Affordable housing for young couples, shorter working hours and flexible work, better parental leave uptake by fathers, cheaper education to reduce competitive hagwon costs.', 2)],
  cases=[('China\'s population policy 1980-2021', 'the one-child policy was replaced by two-child (2016) and three-child (2021) policies as the population began to fall in 2022', 'the long-term consequences of an anti-natalist policy', 'a rapid fall in fertility created ageing, labour shortages and gender imbalance that later required pro-natalist reversal'),
         ('Singapore', 'moved from "Stop at Two" (1972) to pro-natalist incentives (1987, Baby Bonus 2001), yet TFR is about 1.0', 'the limited effectiveness of pro-natalist policy', 'financial incentives did not overcome high living costs and work pressures'),
         ('Japan', 'combines childcare expansion (Angel Plan 1994) with raising pension ages, robotics in care and new migrant worker visas (2019)', 'policies for an ageing population', 'Japan uses a mix of pro-natalist, labour and immigration measures to manage population decline'),
         ('Iran', 'fertility fell from about 6.5 in the mid-1980s to around 2 by 2000 after a voluntary family planning programme from 1989', 'a voluntary anti-natalist policy', 'free contraception, education and premarital counselling produced one of the fastest fertility declines recorded')],
  evaluate=[('Population policies are rarely effective in changing fertility rates.', ['pro-natalist incentives in Singapore, South Korea and Japan have had little effect', 'fertility often fell before policies started'], ['China and Iran show policy can accelerate change', 'France\'s long-term family policy helps sustain TFR near 1.7-1.8'], 'Policies work best when aligned with social change; they can speed decline more easily than they can reverse it.'),
            ('China\'s one-child policy did more harm than good.', ['ageing, sex ratio imbalance, human rights abuses (forced abortions, sterilisations)', '"4-2-1" family burden'], ['slowed population growth during rapid industrialisation', 'contributed to rising living standards and a demographic dividend'], 'It contributed to development but at serious social and human-rights cost, with lasting demographic problems.')],
  extended=[('Examine the effectiveness of pro-natalist and anti-natalist policies, using examples.', 'Award: at least two contrasting named policies with dates and data (China, Iran, Singapore, France, South Korea, Hungary), effectiveness against aims, wider impacts, judgement.', 10, 'long')],
  res=[('Table: total fertility rate, Singapore - 1960: 5.8; 1975: 2.1; 1987: 1.6; 2001: 1.4; 2023: 0.97.',
        [('Describe the trend in TFR in relation to Singapore\'s population policies.', 'TFR fell rapidly to replacement by 1975 (Stop at Two, 1972) and kept falling; after pro-natalist policies (1987) and the Baby Bonus (2001) it continued to decline to below 1.0.'),
         ('Calculate the percentage change in TFR between 1987 and 2023.', f'(0.97 − 1.6)/1.6 × 100 = {pc(1.6, 0.97)}')]),
       ('Graph description: China\'s population peaked at about 1.412 billion in 2021 and fell to about 1.409 billion in 2023; births fell from 17.9 million (2016) to 9.0 million (2023).',
        [('Calculate the percentage fall in births between 2016 and 2023.', f'(9.0 − 17.9)/17.9 × 100 = {pc(17.9, 9.0)}'),
         ('Suggest why births fell despite the two- and three-child policies.', 'High costs of housing and education, delayed marriage, smaller cohorts of women aged 20-35 (a legacy of the one-child era), changing attitudes and the COVID-19 period.')])])

S('ch03-st2', gens=['spearman_dev', 'pct_pop'],
  terms=[('gender equality', 'equal rights, responsibilities and opportunities for women and men, girls and boys'),
         ('Gender Inequality Index (GII)', 'a UNDP composite measure of gender disadvantage in reproductive health, empowerment and labour-market participation (0 = equality)'),
         ('son preference', 'a cultural preference for male children, which can lead to sex-selective abortion and neglect of girls'),
         ('missing women', 'Amartya Sen\'s term for the shortfall of women (estimated at around 100 million in 1990) caused by sex-selective practices and neglect'),
         ('child marriage', 'formal or informal marriage before the age of 18, strongly linked to early childbearing and high fertility')],
  facts=[('Which Indian state is known for a TFR below replacement (about 1.8) despite modest incomes, linked to high female literacy?', 'Kerala', ['Bihar', 'Uttar Pradesh', 'Rajasthan'], 'Kerala\'s female literacy is over 90%, with low infant mortality and late marriage.'),
         ('Which factor shows the strongest negative correlation with fertility across countries?', 'Female secondary school enrolment', ['Average temperature', 'Country area', 'Male literacy only'], 'Educated women marry later, use contraception more and have greater opportunity costs of childbearing.'),
         ('Approximately what was the sex ratio at birth in China in the late 2000s?', 'About 118 boys per 100 girls', ['About 95 boys per 100 girls', 'About 105 boys per 100 girls', 'About 150 boys per 100 girls'], 'The natural ratio is about 105; son preference and the one-child policy pushed it to about 118.')],
  why=[('Explain why female education is associated with lower fertility.', 'Educated women marry later, know about and use contraception, have more say in household decisions and higher earning potential (raising the opportunity cost of children); their children are more likely to survive, reducing the need for many births.'),
       ('Explain why gender inequality can contribute to high population growth.', 'Where women lack education, income and autonomy, early marriage and pressure to have sons persist and access to contraception is limited, keeping fertility high (e.g. Niger, where most girls marry before 18).'),
       ('Explain how son preference can distort population structure.', 'Sex-selective abortion and neglect of daughters produce more boys than girls, leading to "surplus" men who cannot find marriage partners, e.g. China and northern India.'),
       ('Explain why women are often more affected than men by low-fertility work cultures.', 'Long working hours and expectations that women do most childcare and housework force a choice between career and children, depressing fertility (South Korea, Japan).')],
  contrast=[('gender equality', 'gender equity', 'Equality means the same rights and opportunities for all genders; equity means fair treatment according to needs, which may require targeted measures such as girls\' school stipends.'),
            ('female literacy', 'female labour-force participation', 'Literacy measures women\'s ability to read and write, an outcome of schooling; labour-force participation measures the share of women working or seeking work, linked to income and autonomy.')],
  misc=[('Fertility falls only when countries become rich.', 'Kerala and Bangladesh reduced fertility to around replacement with low incomes through female education, health care and family planning.'),
        ('Gender equality is only a social issue, not a population issue.', 'Women\'s education, empowerment and reproductive rights are among the most powerful influences on fertility, mortality and population growth.'),
        ('Greater gender equality always raises fertility in high-income countries.', 'The relationship is not simple: Nordic countries with high equality have TFRs that have also fallen to around 1.4-1.5 since 2010.')],
  apply=[('Using a named example, explain how improving girls\' education has affected fertility.', 'e.g. Bangladesh\'s Female Secondary School Stipend Programme (from 1994) raised girls\' enrolment; together with community family-planning workers, TFR fell from about 6.3 (1975) to around 2.0.', 3),
         ('Suggest two ways that a government could reduce child marriage.', 'Enforcing a minimum marriage age of 18, cash transfers conditional on girls staying in school, community awareness campaigns with religious leaders.', 2)],
  cases=[('Kerala, India', 'female literacy above 90%, low infant mortality and a TFR of about 1.8, compared with about 3 in Bihar', 'the link between female education and fertility', 'high female education and health care reduced fertility without high incomes'),
         ('Bangladesh', 'TFR fell from about 6.3 to around 2.0 through community family-planning workers and girls\' school stipends', 'the role of women\'s empowerment in fertility decline', 'improved schooling and contraception access for women drove one of the fastest declines in South Asia'),
         ('Niger', 'one of the highest rates of child marriage in the world (about three-quarters of girls married before 18) and a TFR around 6', 'the effect of gender inequality on fertility', 'early marriage and low female schooling keep fertility very high'),
         ('South Korea', 'a gender pay gap around 30% (the largest in the OECD) and long working hours alongside the world\'s lowest TFR', 'gender roles in very low fertility', 'women face a stark choice between careers and family, depressing fertility')],
  evaluate=[('Female education is the most important factor in reducing fertility.', ['strong cross-country correlation; Kerala and Bangladesh examples', 'education changes age at marriage, contraception use and aspirations'], ['access to contraception and family planning services', 'urbanisation, falling infant mortality and policy (China, Iran)'], 'Female education is arguably the most powerful long-term factor, but it works through and alongside health, contraception and economic change.'),
            ('Gender equality is essential for a country to benefit from its demographic dividend.', ['women\'s employment raises the labour force and household incomes', 'educated mothers invest more in children'], ['East Asian dividends occurred with significant gender inequality', 'investment, governance and jobs matter too'], 'Gender equality greatly increases the size of the dividend, though it is not the only condition.')],
  extended=[('Examine the relationship between gender equality and fertility in contrasting countries.', 'Award: named contrasting cases (Niger, Kerala/Bangladesh, South Korea, Nordic countries), mechanisms (education, autonomy, contraception, work culture), data, non-linear relationship, judgement.', 10, 'long')],
  res=[('Table: female mean years of schooling and TFR - Niger 1.3, 6.1; Mali 1.9, 5.6; Nigeria 6.0, 5.1; India 5.4, 2.0; Bangladesh 6.6, 1.9; Brazil 8.2, 1.6.',
        [('Describe the relationship shown.', 'Generally negative: countries with more female schooling have lower TFR; Niger and Mali (low schooling) have the highest fertility; Nigeria is an exception with higher schooling but high TFR.'),
         ('Suggest one reason for the anomaly in the data.', 'Nigeria\'s national average hides strong regional contrasts (higher schooling in the south, low in the north); cultural and religious norms, child marriage and limited contraception access also matter.')]),
       ('Text: "In Bangladesh, the proportion of girls enrolled in secondary school rose from about 33% in 1990 to over 70% by 2018, while the TFR fell from 4.5 to 2.1." - World Bank data summary.',
        [('Calculate the percentage fall in TFR over the period.', f'(2.1 − 4.5)/4.5 × 100 = {pc(4.5, 2.1)}'),
         ('Explain one way the rise in girls\' schooling could have contributed to this change.', 'Girls stayed in school longer, delaying marriage and first births; educated women used contraception more and had paid employment opportunities (e.g. garment industry).')])])

S('ch03-st3', gens=['dep', 'migration', 'pct_pop'],
  terms=[('demographic dividend', 'the economic growth potential that arises when the working-age share of a population is large relative to dependants, following a fall in fertility'),
         ('window of opportunity', 'the limited period (often 30-50 years) during which the dependency ratio is low enough to generate a demographic dividend'),
         ('points-based immigration system', 'a system that selects migrants by awarding points for characteristics such as skills, age, education and language, used by Canada and Australia'),
         ('kafala system', 'a sponsorship system used in Gulf states that ties a migrant worker\'s legal status to their employer'),
         ('managed migration', 'policies that control the number and type of migrants to meet labour-market and demographic needs')],
  facts=[('Approximately what share of East Asia\'s rapid economic growth (1965-1990) has been attributed to the demographic dividend?', 'About one-third', ['Almost none', 'About 5%', 'Nearly all'], 'Bloom and Williamson estimated about a quarter to a third of the "economic miracle" came from the dividend.'),
         ('Which country introduced the first points-based immigration system, in 1967?', 'Canada', ['Australia', 'the UK', 'Germany'], 'Canada\'s 1967 points system is now administered through Express Entry.'),
         ('Which agreement removed internal border controls between many European countries?', 'The Schengen Agreement', ['The Paris Agreement', 'The Dublin Regulation', 'The Lisbon Treaty'], 'The Schengen Area allows passport-free travel across 29 European countries.')],
  why=[('Explain why a demographic dividend is not automatic.', 'The larger working-age population boosts growth only if there are jobs, education and health, good governance, savings and investment; without them a "youth bulge" can bring unemployment and unrest.'),
       ('Explain how female employment can increase the size of a demographic dividend.', 'Lower fertility frees women to enter paid work, raising the labour force, household incomes and savings, and educated mothers invest more in their children\'s schooling.'),
       ('Explain why some high-income countries use points-based immigration systems.', 'To select skilled migrants who fill labour shortages, integrate quickly and pay taxes, while controlling numbers in line with economic needs, e.g. Canada and Australia.'),
       ('Explain why the kafala system has been criticised.', 'Tying workers to employers allows abuse - confiscated passports, unpaid wages and inability to change jobs - as reported for migrant workers in Qatar before the 2022 World Cup reforms.')],
  contrast=[('a demographic dividend', 'a youth bulge', 'A dividend is the growth gained when a large working-age population is productively employed; a youth bulge is a large share of young people that can bring unemployment and instability if jobs are lacking.'),
            ('a points-based system', 'a temporary guest-worker programme', 'A points system selects permanent migrants by skills and attributes; guest-worker programmes admit temporary workers for specific jobs, often without a path to settlement (e.g. Gulf kafala, Germany\'s 1960s Gastarbeiter).')],
  misc=[('Any country with a falling birth rate will automatically become richer.', 'The dividend requires jobs, investment, education and governance; without them a large working-age population may be unemployed.'),
        ('Immigration restrictions always reduce the number of migrants.', 'Restrictions often divert migrants to irregular routes or change the type rather than the total number of migrants.'),
        ('A demographic dividend lasts indefinitely.', 'It is temporary: as the large working-age cohorts age, the old-age dependency ratio rises (as in Japan and now China).')],
  apply=[('Using a named country, outline two policies that could help it gain a demographic dividend.', 'e.g. Ethiopia: expand secondary and vocational education and attract labour-intensive manufacturing (e.g. Hawassa Industrial Park); also expand family planning and girls\' education to lower fertility faster.', 4),
         ('Suggest two reasons why Japan began admitting more foreign workers after 2019.', 'Its working-age population has shrunk since the mid-1990s and care, construction and agriculture face severe labour shortages; ageing raised dependency.', 2)],
  cases=[('South Korea 1960-1990', 'fertility fell sharply while investment in education and export industries absorbed a growing workforce', 'the demographic dividend', 'a falling dependency ratio combined with job creation to fuel rapid growth'),
         ('Nigeria', 'about 42% of the population is under 15 and 3-4 million young people enter the labour market each year', 'the risks of a youth bulge', 'without enough formal jobs the potential dividend may become unemployment and insecurity'),
         ('Canada\'s Express Entry', 'a points-based system that selects about 100,000 skilled permanent residents a year within an immigration target of around 400,000+', 'managed international migration policy', 'Canada uses selective immigration to offset ageing and fill skills shortages'),
         ('Qatar\'s 2020 labour reform', 'the minimum wage was introduced and workers allowed to change employers without permission after criticism of kafala', 'the human-rights dimension of migration policy', 'international scrutiny pushed reforms to a system that tied workers to employers')],
  evaluate=[('Countries with youthful populations in sub-Saharan Africa are likely to gain a demographic dividend.', ['fertility is falling in many countries (Kenya, Ethiopia, Rwanda)', 'young workforces could attract labour-intensive industry as Chinese wages rise'], ['fertility decline is slow and has stalled in some countries', 'job creation, education quality and governance are weak; automation reduces manufacturing jobs'], 'A dividend is possible but not guaranteed; it depends on rapid fertility decline and investment in skills and jobs.'),
            ('Selective immigration policies are the best response to an ageing population.', ['migrants add workers and taxpayers quickly (Canada, Australia)', 'skills targeting fills specific shortages'], ['migrants also age; very large numbers would be needed to stabilise dependency', 'political opposition; raising pension ages, automation and pro-natalism are alternatives'], 'Immigration helps but is best combined with labour participation, productivity and pension reforms.')],
  extended=[('Examine the conditions needed for a country to benefit from a demographic dividend.', 'Award: definition; conditions (fertility decline, education, health, jobs, savings, governance, female employment); East Asia vs sub-Saharan Africa examples; judgement.', 10, 'long')],
  res=[('Table: working-age share (15-64) of population, % - South Korea 1960: 53, 1990: 69, 2020: 72; Nigeria 1990: 51, 2020: 54, 2050 (projected): 62.',
        [('Calculate the change in South Korea\'s working-age share 1960-1990 in percentage points.', '69 − 53 = 16 percentage points'),
         ('Compare the trends for the two countries and comment on the implications.', 'South Korea\'s working-age share rose quickly (by 16 points in 30 years), supporting rapid growth; Nigeria\'s rise is slow (3 points) and expected to accelerate, so its dividend window lies in the future if jobs are created.')]),
       ('Text: "Canada set immigration levels of 485,000 permanent residents for 2024, about 1.2% of its population, with around 60% in economic categories." - Government of Canada immigration levels plan.',
        [('Calculate the approximate number of economic-category immigrants planned.', f'0.6 × 485,000 ≈ {0.6 * 485000:,.0f}'),
         ('Suggest why Canada targets mainly economic migrants.', 'To offset ageing and a TFR of about 1.3, fill labour and skills shortages and support tax revenues and growth.')])])


# =============================================================================================
# Unit 2 Global climate - vulnerability and resilience
# =============================================================================================
S('ch04-st1', gens=['albedo', 'pct_climate'],
  terms=[('albedo', 'the proportion of incoming solar radiation reflected by a surface, from 0 (none) to 1 (all); fresh snow about 0.8-0.9, ocean about 0.06'),
         ('natural greenhouse effect', 'the warming of the Earth\'s surface because greenhouse gases absorb and re-emit outgoing longwave radiation, raising the mean temperature from about −18 °C to about +15 °C'),
         ('global energy balance', 'the balance between incoming shortwave solar radiation and outgoing reflected and longwave radiation at the top of the atmosphere'),
         ('shortwave radiation', 'high-energy radiation emitted by the Sun, mostly visible light and ultraviolet, that passes easily through the atmosphere'),
         ('longwave radiation', 'infrared radiation emitted by the Earth\'s surface and atmosphere, which greenhouse gases absorb'),
         ('greenhouse gas', 'a gas that absorbs and emits longwave radiation, e.g. water vapour, carbon dioxide, methane and nitrous oxide')],
  facts=[('What is the approximate average albedo of the Earth as a whole?', '0.30', ['0.06', '0.60', '0.90'], 'About 30% of incoming solar radiation is reflected by clouds, aerosols and bright surfaces.'),
         ('Without the natural greenhouse effect, the Earth\'s mean surface temperature would be about:', '−18 °C', ['0 °C', '+5 °C', '+33 °C'], 'The natural greenhouse effect adds about 33 °C, giving roughly +15 °C.'),
         ('Which is the most abundant greenhouse gas in the atmosphere?', 'Water vapour', ['Carbon dioxide', 'Methane', 'Nitrous oxide'], 'Water vapour contributes most to the natural effect but acts mainly as a feedback.'),
         ('Approximately how much solar radiation reaches the top of the atmosphere, averaged over the whole Earth?', 'About 340 W/m²', ['About 34 W/m²', 'About 1,000 W/m²', 'About 3,400 W/m²'], 'The solar constant is about 1,361 W/m², which averages to about 340 W/m² over the sphere.')],
  why=[('Explain why the Earth\'s surface is warmer than it would be without an atmosphere.', 'Greenhouse gases are largely transparent to incoming shortwave radiation but absorb outgoing longwave radiation and re-emit part of it back to the surface, so the surface receives extra energy and warms by about 33 °C.'),
       ('Explain why high-latitude regions have an energy deficit and the tropics a surplus.', 'At high latitudes the Sun\'s rays strike at a low angle and pass through more atmosphere, so energy is spread over a larger area, and snow/ice albedo is high; the tropics receive more concentrated radiation all year. Winds and ocean currents transfer the surplus poleward.'),
       ('Explain how clouds can both warm and cool the Earth.', 'Clouds reflect incoming shortwave radiation (cooling, especially low, thick clouds) and absorb and re-emit outgoing longwave radiation (warming, especially high, thin cirrus); the net effect depends on cloud type and height.'),
       ('Explain why changes in albedo can amplify climate change.', 'Melting snow and ice expose darker land or ocean with lower albedo, so more radiation is absorbed, causing more warming and more melting - a positive feedback.')],
  contrast=[('shortwave radiation', 'longwave radiation', 'Shortwave radiation comes from the hot Sun and passes through the atmosphere; longwave (infrared) radiation is emitted by the cooler Earth and is absorbed by greenhouse gases.'),
            ('the natural greenhouse effect', 'the enhanced greenhouse effect', 'The natural effect is caused by naturally occurring greenhouse gases and keeps the Earth habitable; the enhanced effect is the extra warming from human emissions that raise greenhouse-gas concentrations.')],
  misc=[('The greenhouse effect is entirely harmful.', 'The natural greenhouse effect is essential for life; it is the human-enhanced effect that is causing dangerous warming.'),
        ('Greenhouse gases trap incoming sunlight.', 'They mainly absorb outgoing longwave (infrared) radiation from the Earth, not incoming shortwave sunlight.'),
        ('The hole in the ozone layer is the main cause of global warming.', 'Ozone depletion and global warming are different issues; warming is caused mainly by increased CO₂, methane and other greenhouse gases.')],
  apply=[('A city replaces dark asphalt roofs (albedo 0.05) with white roofs (albedo 0.7). Explain the likely effect on local temperatures.', 'Higher albedo reflects much more incoming radiation, so roofs absorb less energy and emit less heat, reducing the urban heat island and indoor cooling demand.', 3),
         ('Suggest why Arctic temperatures have risen about four times faster than the global average since 1979.', 'Arctic amplification: loss of sea ice lowers albedo; open water absorbs more energy; changes in atmospheric heat transport and a shallower boundary layer concentrate warming.', 3)],
  cases=[('Arctic sea ice', 'September sea-ice extent has declined by about 13% per decade since satellite records began in 1979', 'the ice-albedo effect', 'replacing bright ice (albedo about 0.6) with dark ocean (about 0.06) increases absorption of solar energy'),
         ('the 1991 eruption of Mount Pinatubo, Philippines', 'about 15-20 million tonnes of sulphur dioxide formed aerosols that cooled global temperatures by around 0.5 °C for over a year', 'how aerosols alter the global energy balance', 'aerosols increased the reflection of incoming solar radiation, temporarily reducing the energy reaching the surface'),
         ('Venus', 'its dense carbon dioxide atmosphere produces surface temperatures of about 460 °C', 'the greenhouse effect', 'an extreme greenhouse effect shows how strongly greenhouse gases can raise surface temperature')],
  evaluate=[('Changes in albedo are the most important influence on the global energy balance.', ['ice-albedo feedback amplifies warming in the Arctic', 'clouds and aerosols (Pinatubo) change reflected radiation significantly'], ['greenhouse-gas concentrations control outgoing longwave radiation and are the main driver of current change', 'solar output and orbital cycles alter incoming energy'], 'Albedo is an important modifier and feedback, but greenhouse gases are the dominant cause of the current imbalance.'),
            ('The natural greenhouse effect is more significant for life on Earth than the enhanced greenhouse effect.', ['it raises temperatures by about 33 °C and enables liquid water', 'human additions so far have added about 1.1-1.3 °C'], ['the enhanced effect is changing climate rapidly with large impacts on people', 'small changes in mean temperature have big effects on extremes'], 'The natural effect is far larger, but the enhanced effect matters more for future human well-being.')],
  extended=[('Explain the components of the global energy balance and how human activity is altering it.', 'Award: incoming shortwave, reflection (albedo ≈ 0.3), absorption, longwave emission, greenhouse absorption, latent and sensible heat; human changes - CO₂/CH₄ increases, aerosols, land-use albedo; current imbalance ≈ +1 W/m².', 10, 'long')],
  res=[('Diagram description (simplified global energy budget, W/m²): incoming solar 340; reflected by clouds and atmosphere 77; reflected by the surface 23; absorbed by the atmosphere 79; absorbed by the surface 161.',
        [('Calculate the Earth\'s albedo from the data.', f'(77 + 23)/340 = {100 / 340:.2f} (about 0.29-0.30)'),
         ('Calculate the percentage of incoming radiation absorbed by the surface.', f'161/340 × 100 = {161 / 340 * 100:.1f}%')]),
       ('Table: typical albedo values - fresh snow 0.85; sea ice 0.6; desert sand 0.4; grassland 0.25; forest 0.12; open ocean 0.06.',
        [('Describe the variation in albedo shown.', 'Bright, light-coloured surfaces (snow 0.85, sea ice 0.6) reflect most radiation; dark surfaces (forest 0.12, ocean 0.06) absorb most.'),
         ('Explain the significance of the difference between sea ice and open ocean.', 'When sea ice melts, albedo falls from about 0.6 to 0.06, so about ten times more energy is absorbed, warming the ocean and melting more ice - a positive feedback.')])])

S('ch04-st2', gens=['pct_climate', 'albedo', 'spearman_dev'],
  terms=[('enhanced greenhouse effect', 'the additional warming caused by human emissions of greenhouse gases that increase their atmospheric concentration'),
         ('climate forcing', 'a change that alters the Earth\'s energy balance (in W/m²), such as changes in solar output, aerosols or greenhouse gases'),
         ('positive feedback', 'a process that amplifies an initial change, e.g. melting ice lowering albedo and causing more warming'),
         ('negative feedback', 'a process that dampens an initial change, e.g. increased plant growth absorbing more CO₂'),
         ('Milankovitch cycles', 'long-term variations in the Earth\'s orbit (eccentricity ~100,000 years, obliquity ~41,000 years, precession ~23,000 years) that change the distribution of solar energy'),
         ('tipping point', 'a critical threshold beyond which a system changes abruptly and often irreversibly, e.g. collapse of the Greenland ice sheet')],
  facts=[('What was the approximate atmospheric CO₂ concentration before the Industrial Revolution?', '280 ppm', ['180 ppm', '350 ppm', '420 ppm'], 'Ice cores show about 280 ppm; it passed 420 ppm in 2023 at Mauna Loa.'),
         ('According to the IPCC AR6, by how much had global surface temperature risen in 2011-2020 compared with 1850-1900?', 'About 1.1 °C', ['About 0.1 °C', 'About 3 °C', 'About 5 °C'], 'IPCC AR6 (2021) gives 1.09 °C; 2024 was the first calendar year above 1.5 °C.'),
         ('Which Milankovitch cycle has a period of about 41,000 years?', 'Obliquity (axial tilt)', ['Eccentricity', 'Precession', 'Sunspot cycle'], 'Tilt varies between about 22.1° and 24.5°.'),
         ('What is the length of the sunspot cycle?', 'About 11 years', ['About 1 year', 'About 100 years', 'About 41,000 years'], 'Total solar irradiance varies by only about 0.1% over the cycle.')],
  why=[('Explain why scientists conclude that recent warming is not caused by the Sun.', 'Solar output has been flat or slightly declining since the 1980s while temperatures rose; the upper atmosphere (stratosphere) has cooled while the lower atmosphere warmed, a fingerprint of greenhouse gases, not increased solar input.'),
       ('Explain how melting permafrost could create a positive feedback.', 'Permafrost stores about 1,400-1,600 Gt of carbon; thawing lets microbes decompose organic matter, releasing CO₂ and methane, which enhances the greenhouse effect and causes more thawing.'),
       ('Explain how water vapour acts as a feedback rather than a forcing.', 'Warmer air holds about 7% more water vapour per °C (Clausius-Clapeyron); extra vapour absorbs more longwave radiation, amplifying warming caused by other forcings, but it does not stay long enough in the air to drive change on its own.'),
       ('Explain why volcanic eruptions usually cause short-term cooling.', 'Large explosive eruptions inject sulphur dioxide into the stratosphere where it forms sulphate aerosols that reflect sunlight for 1-3 years, e.g. Pinatubo 1991 cooled the globe by about 0.5 °C.')],
  contrast=[('a positive feedback', 'a negative feedback', 'A positive feedback amplifies the initial change (ice-albedo, permafrost methane); a negative feedback reduces it (CO₂ fertilisation of plant growth, more low cloud reflecting sunlight).'),
            ('natural climate forcing', 'anthropogenic climate forcing', 'Natural forcings include solar variation, orbital cycles and volcanic aerosols; anthropogenic forcings include greenhouse-gas emissions, aerosols and land-use change.')],
  misc=[('Climate has always changed, so current change must be natural.', 'Past changes had natural causes, but current warming is far faster than most past changes and matches the fingerprint of rising greenhouse gases from fossil fuels.'),
        ('Because CO₂ is only about 0.04% of the atmosphere it cannot affect climate.', 'Concentration is not the same as effect: CO₂ strongly absorbs infrared radiation, and a 50% increase since 1750 adds about 2 W/m² of forcing.'),
        ('All feedbacks in the climate system make warming worse.', 'Some feedbacks are negative, such as increased plant uptake of CO₂ and greater longwave emission from a warmer surface.')],
  apply=[('Describe the shape of the Keeling Curve and explain its seasonal pattern.', 'A steady upward trend (about 316 ppm in 1958 to over 420 ppm) with an annual saw-tooth: CO₂ falls in the northern summer when vegetation photosynthesises and rises in winter when respiration and decay dominate.', 3),
         ('Suggest how loss of the Amazon rainforest could become a positive feedback.', 'Deforestation and drought reduce transpiration and rainfall, causing forest dieback and fires that release carbon, further warming and drying the region.', 3)],
  cases=[('the Keeling Curve at Mauna Loa, Hawaii', 'CO₂ rose from about 316 ppm in 1958 to over 420 ppm by 2023', 'the enhanced greenhouse effect', 'the record documents a rapid human-caused increase in a key greenhouse gas'),
         ('Siberian permafrost', 'thaw has created methane-emitting thermokarst lakes and craters on the Yamal Peninsula', 'a positive feedback loop', 'warming releases stored carbon that causes further warming'),
         ('the Maunder Minimum (about 1645-1715)', 'very few sunspots coincided with part of the Little Ice Age in Europe', 'solar forcing of climate', 'a reduction in solar activity is associated with cooler conditions, though volcanic activity also contributed'),
         ('the West Antarctic Ice Sheet', 'glaciers such as Thwaites are retreating as warm ocean water melts them from below', 'climate tipping points', 'once retreat passes a threshold it may become self-sustaining, committing the world to metres of sea-level rise')],
  evaluate=[('Feedback loops are a greater threat to the global climate than direct human emissions.', ['permafrost, ice-albedo and forest dieback could add warming beyond human control', 'tipping points may be irreversible'], ['feedbacks are triggered by human emissions in the first place', 'emissions are still the largest driver and can be reduced'], 'Human emissions are the root cause; feedbacks magnify them, so cutting emissions is the way to avoid crossing tipping points.'),
            ('Natural factors can explain most climate change in the past 150 years.', ['solar and volcanic changes do affect climate (Maunder Minimum, Pinatubo)', 'natural variability (El Niño) affects individual years'], ['solar output has not increased since the 1980s', 'IPCC AR6: it is unequivocal that human influence has warmed the atmosphere, ocean and land'], 'Natural factors explain short-term variation but not the long-term warming trend since 1850.')],
  extended=[('Explain how feedback loops can amplify changes in the global energy balance.', 'Award: definitions; ice-albedo, water vapour, permafrost carbon, forest dieback; negative feedbacks; tipping points; examples and data.', 10, 'long')],
  res=[('Table: atmospheric CO₂ (ppm, Mauna Loa annual means) - 1960: 317; 1980: 339; 2000: 370; 2023: 421.',
        [('Calculate the mean annual rate of increase between 1960 and 1980, and between 2000 and 2023.', f'1960-80: {(339 - 317) / 20:.2f} ppm/yr; 2000-23: {(421 - 370) / 23:.2f} ppm/yr - the rate has more than doubled.'),
         ('Calculate the percentage increase since 1960.', f'(421 − 317)/317 × 100 = {pc(317, 421)}')]),
       ('Graph description: global temperature anomaly relative to 1850-1900 (°C) - 1960: 0.3; 1980: 0.4; 2000: 0.7; 2016: 1.3; 2024: 1.55.',
        [('Describe the trend shown.', 'Accelerating warming: about 0.1 °C between 1960 and 1980, 0.3 °C 1980-2000 and about 0.85 °C 2000-2024, with peaks in El Niño years (2016, 2024).'),
         ('Suggest why individual years such as 2016 stand out.', 'Strong El Niño events release ocean heat into the atmosphere, adding short-term warming on top of the long-term trend.')])])

S('ch04-st3', gens=['carbon', 'pct_climate'],
  terms=[('carbon cycle', 'the movement of carbon between stores (atmosphere, oceans, biosphere, soils, lithosphere) through flows such as photosynthesis, respiration, decomposition and combustion'),
         ('carbon sink', 'a store that absorbs more carbon than it releases, e.g. oceans and growing forests'),
         ('land-use change', 'human alteration of land cover, e.g. deforestation, agriculture and urbanisation, which changes carbon storage and albedo'),
         ('fossil fuel', 'a carbon-rich energy source (coal, oil, natural gas) formed from ancient organic matter, releasing CO₂ when burned'),
         ('anthropogenic emissions', 'greenhouse gases released by human activity, such as burning fossil fuels, cement production, agriculture and deforestation')],
  facts=[('Approximately how much CO₂ was emitted from fossil fuels and industry globally in 2023?', 'About 37 Gt', ['About 3.7 Gt', 'About 370 Gt', 'About 3,700 Gt'], 'The Global Carbon Project estimated about 37.4 Gt CO₂ in 2023.'),
         ('Which sector produces about 8% of global CO₂ emissions through the chemical process of making clinker?', 'Cement production', ['Aviation', 'Shipping', 'Rice farming'], 'Calcination of limestone releases CO₂ in addition to fuel combustion.'),
         ('Which of these is a major source of methane?', 'Livestock (enteric fermentation) and rice paddies', ['Solar power stations', 'Nuclear power', 'Wind turbines'], 'Agriculture produces about 40% of human methane emissions.'),
         ('Approximately what fraction of human CO₂ emissions is absorbed by the oceans?', 'About a quarter', ['Almost none', 'About three-quarters', 'All of it'], 'Oceans absorb roughly 25% and land sinks about 30%, leaving about 45% in the atmosphere.')],
  why=[('Explain how deforestation contributes to climate change.', 'Burning and decay of trees release stored carbon as CO₂; the loss of forest removes a carbon sink; soils exposed to erosion and oxidation release more carbon, e.g. Amazon deforestation.'),
       ('Explain why ocean uptake of CO₂ is a mixed blessing.', 'Oceans slow atmospheric warming by absorbing about a quarter of emissions, but dissolved CO₂ forms carbonic acid, lowering pH (ocean acidification) and harming corals and shell-forming organisms.'),
       ('Explain why methane is an important greenhouse gas even though its concentration is low.', 'Methane is about 80 times more powerful than CO₂ over 20 years (about 28 times over 100 years); concentrations have more than doubled since pre-industrial times, from agriculture, landfill and fossil fuels.'),
       ('Explain why emissions per capita vary greatly between countries.', 'They reflect income, energy mix, industrial structure, transport and climate: Qatar and the USA emit over 14 t per person, India about 2 t and Ethiopia about 0.15 t.')],
  contrast=[('a carbon store', 'a carbon flux', 'A store is a reservoir that holds carbon (e.g. the ocean holds about 38,000 GtC); a flux is the transfer of carbon between stores (e.g. photosynthesis, combustion).'),
            ('territorial emissions', 'consumption-based emissions', 'Territorial emissions are produced within a country\'s borders; consumption-based emissions are attributed to the country where goods are consumed, so the UK\'s are higher and China\'s lower than their territorial totals.')],
  misc=[('China is the biggest cause of climate change because it emits the most CO₂ today.', 'China has the largest annual emissions, but the USA and Europe have larger cumulative historical emissions, and China\'s per-capita emissions are lower than the USA\'s.'),
        ('Planting trees can fully offset fossil fuel emissions.', 'Forests take decades to absorb carbon, may burn or be cleared, and available land is limited; emissions cuts are still needed.'),
        ('Carbon dioxide is the only greenhouse gas that humans emit.', 'Humans also emit methane, nitrous oxide and fluorinated gases, which together contribute about a quarter of current warming.')],
  apply=[('Using data, compare the CO₂ emissions of a high-income country and a low-income country.', 'e.g. the USA emits about 4.9 Gt (about 14.5 t per person) and Ethiopia about 0.02 Gt (about 0.15 t per person): over 90 times more per person, reflecting energy use, industry and transport.', 3),
         ('Suggest two reasons why Indonesia\'s land-use emissions have been high.', 'Clearance and drainage of carbon-rich peat swamp forests for oil palm and pulpwood plantations, and peat fires (e.g. 2015).', 2)],
  cases=[('the Brazilian Amazon', 'deforestation peaked at about 27,000 km² in 2004, fell sharply after 2005, rose again after 2019 and fell again in 2023', 'the effect of land-use change on the carbon cycle', 'cleared forest releases stored carbon and reduces a major sink'),
         ('Indonesia\'s 2015 peat-fire crisis', 'fires on drained peatlands released an estimated 1.5 Gt CO₂-equivalent and created a regional haze', 'land-use change as a source of greenhouse gases', 'draining carbon-rich peat for plantations turned a store into a large source'),
         ('China\'s emissions growth', 'China\'s CO₂ emissions rose from about 3 Gt in 2000 to about 11-12 Gt by 2023, largely from coal power and heavy industry', 'the link between industrialisation and carbon emissions', 'rapid coal-based industrial growth made China the largest annual emitter')],
  evaluate=[('Land-use change is now a more important human cause of climate change than burning fossil fuels.', ['tropical deforestation releases about 4 Gt CO₂ a year and removes sinks', 'agriculture is a major source of methane and nitrous oxide'], ['fossil fuels and industry produce about 37 Gt CO₂ a year, nearly 90% of CO₂ emissions', 'land-use emissions have been broadly stable while fossil emissions grew'], 'Fossil fuels are by far the dominant cause; land-use change is significant mainly in a few tropical countries.'),
            ('Responsibility for climate change should be based on historical emissions rather than current emissions.', ['the USA and EU account for a large share of cumulative CO₂ since 1850', 'principle of common but differentiated responsibilities'], ['current emitters (China, India) will determine future warming', 'past emitters could not know the effects before the 1980s'], 'Both matter: historical emissions justify greater obligations for early industrialisers, but all major current emitters must cut.')],
  extended=[('Examine the role of human activity in changing the carbon cycle.', 'Award: stores and fluxes; fossil fuels, cement, deforestation, agriculture; sinks and their limits; ocean acidification; data (CO₂ 280 → 420 ppm; 37 Gt/yr).', 10, 'long')],
  res=[('Table: global carbon budget 2014-2023 averages (Gt CO₂ per year) - fossil fuels and industry 36.1; land-use change 4.4; atmospheric growth 19.1; ocean sink 10.4; land sink 11.6.',
        [('Calculate the percentage of total emissions that remained in the atmosphere.', f'19.1 / (36.1 + 4.4) × 100 = {19.1 / 40.5 * 100:.1f}%'),
         ('Calculate the share of emissions absorbed by the ocean and land sinks combined.', f'(10.4 + 11.6)/40.5 × 100 = {22.0 / 40.5 * 100:.1f}%')]),
       ('Bar chart description: CO₂ per capita (t, recent year) - Qatar 37; USA 14.5; China 8.4; Germany 8.0; India 2.0; Nigeria 0.6; Ethiopia 0.15.',
        [('How many times greater are emissions per capita in the USA than in India?', f'14.5 / 2.0 = {14.5 / 2.0:.2f} times'),
         ('Suggest two reasons for the very high figure for Qatar.', 'Energy-intensive oil and gas production and processing (LNG), desalination and air-conditioning in a hot climate, a small population and high incomes.')])])

S('ch05-st1', gens=['sea_level', 'yield', 'pct_climate', 'water_stress'],
  terms=[('sea-level rise', 'the increase in mean sea level caused mainly by thermal expansion of seawater and melting of glaciers and ice sheets'),
         ('thermal expansion', 'the increase in volume of seawater as it warms, a major contributor to sea-level rise'),
         ('food security', 'when all people at all times have physical and economic access to sufficient, safe and nutritious food (FAO, 1996)'),
         ('water security', 'reliable access to an acceptable quantity and quality of water for health, livelihoods and production, with acceptable water-related risks'),
         ('extreme weather event', 'a weather event that is rare at a particular place and time of year, such as a severe heatwave, flood or tropical cyclone')],
  facts=[('According to the IPCC AR6, by about how much did global mean sea level rise between 1901 and 2018?', 'About 0.20 m', ['About 2 cm', 'About 2 m', 'About 5 m'], 'The rate has accelerated to about 3.7 mm per year (2006-2018).'),
         ('In the 2022 Pakistan floods, approximately how many people were affected?', 'About 33 million', ['About 3 million', 'About 330,000', 'About 330 million'], 'Monsoon rains and glacial melt flooded about a third of the country; about 1,700 died.'),
         ('Approximately how much of the Maldives lies less than 1 m above sea level?', 'About 80%', ['About 10%', 'About 40%', 'None of it'], 'This makes the Maldives one of the most exposed countries to sea-level rise.'),
         ('The European heatwave of summer 2003 is estimated to have caused about how many deaths?', 'About 70,000', ['About 700', 'About 7,000', 'About 700,000'], 'Most victims were elderly people in France, Italy and Spain.')],
  why=[('Explain why sea-level rise threatens low-lying deltas such as the Ganges-Brahmaputra delta.', 'Large populations live less than a few metres above sea level; rising seas increase coastal flooding and storm-surge reach, cause salt-water intrusion into soils and groundwater, and subsidence (from sediment compaction and groundwater pumping) makes relative rise faster.'),
       ('Explain how climate change can threaten food security.', 'Higher temperatures and droughts reduce yields of maize and wheat; changing rainfall disrupts growing seasons; extreme events destroy crops; pests and diseases spread; price spikes reduce access for the poor.'),
       ('Explain why glacier retreat threatens water security in the Andes and Himalaya.', 'Glaciers act as water towers, releasing meltwater in dry seasons; as they shrink, dry-season river flows will eventually fall, affecting cities such as La Paz and Lima and irrigated farming downstream.'),
       ('Explain why a warmer climate is expected to increase the intensity of extreme rainfall.', 'Warmer air holds about 7% more water vapour per °C, so storms can produce heavier downpours, increasing flash-flood risk.')],
  contrast=[('thermal expansion', 'ice-sheet melt', 'Thermal expansion raises sea level as warming water expands; ice-sheet melt adds water from land-based ice (Greenland, Antarctica) to the oceans; both contribute, with ice melt becoming more important.'),
            ('impacts on food availability', 'impacts on food access', 'Availability concerns how much food is produced (yields, harvests); access concerns whether people can afford or obtain it (prices, incomes) - climate shocks can affect both.')],
  misc=[('Melting sea ice is a major cause of sea-level rise.', 'Sea ice already floats, so its melting barely changes sea level; land ice and thermal expansion are the main causes.'),
        ('Climate change will reduce crop yields everywhere.', 'Some high-latitude areas (e.g. parts of Canada and Russia) may gain longer growing seasons, though extremes and pests may offset gains.'),
        ('Sea level is rising by the same amount everywhere.', 'Relative sea-level rise varies with subsidence, uplift, ocean currents and gravity effects; Jakarta and Manila experience much faster relative rise than the global mean.')],
  apply=[('Using a named example, outline two impacts of an extreme weather event linked to climate change.', 'e.g. 2022 Pakistan floods: about 33 million people affected and 1,700 deaths; about US$30 billion of damage and losses, with crops (cotton, rice) and 1 million+ homes destroyed.', 4),
         ('Suggest two ways that sea-level rise could affect the economy of Bangladesh.', 'Loss of farmland to flooding and salinisation, reducing rice output; damage to infrastructure and displacement of coastal communities, increasing rural-urban migration to Dhaka.', 2)],
  cases=[('Tuvalu', 'a Pacific nation of about 11,000 people whose highest point is under 5 m above sea level, facing inundation and salt-water intrusion', 'the threat of sea-level rise to small island developing states', 'low elevation and limited land leave nowhere to retreat'),
         ('the 2022 Pakistan flood disaster', 'record monsoon rainfall and glacial melt affected 33 million people and caused about US$30 billion of damage and losses', 'the impact of extreme weather on people and places', 'one event damaged homes, crops, infrastructure and health across a third of the country'),
         ('glacier retreat above La Paz, Bolivia', 'the Chacaltaya glacier disappeared by 2009 and many glaciers supplying La Paz and El Alto are shrinking', 'climate threats to water security', 'loss of glacial storage will reduce dry-season water supplies'),
         ('the 2021 Pacific Northwest heat dome', 'Lytton, British Columbia reached 49.6 °C, a Canadian record, and hundreds of excess deaths occurred', 'changes in heat extremes', 'attribution studies found the event would have been virtually impossible without human-caused warming')],
  evaluate=[('Sea-level rise is the most serious consequence of climate change for people.', ['threatens hundreds of millions in low-lying coasts and deltas', 'existential threat to small island states such as Tuvalu and the Maldives'], ['heat, drought and food insecurity affect more people now', 'sea-level rise is slow and can be partly adapted to (Netherlands)'], 'Sea-level rise is the gravest long-term threat for coastal places, but for most people heat, water and food impacts are more immediate.'),
            ('Climate change impacts on food security will be greatest in low-latitude countries.', ['tropical crops are already near heat thresholds; Sahel and South Asia yields fall', 'high dependence on rain-fed agriculture and low adaptive capacity'], ['global food prices transmit shocks everywhere', 'mid-latitude breadbaskets face drought (2010 Russia, 2012 USA)'], 'Low-latitude, low-income countries face the largest impacts because of exposure and vulnerability, though global markets spread effects.')],
  extended=[('Examine the impacts of climate change on water and food security in contrasting places.', 'Award: located examples (Sahel, Pakistan, Andes, Bangladesh, Canada), mechanisms, data and scale; recognition of uneven impacts; judgement.', 10, 'long')],
  res=[('Table: global mean sea level rise rate (IPCC AR6, mm per year) - 1901-1971: 1.3; 1971-2006: 1.9; 2006-2018: 3.7.',
        [('Describe the trend shown by the data.', 'The rate has accelerated: it rose by about 46% from 1.3 to 1.9 mm/yr, then roughly doubled to 3.7 mm/yr.'),
         ('Calculate the total rise implied over a century at the 2006-2018 rate.', '3.7 mm × 100 = 370 mm ≈ 0.37 m (if the rate stays constant, which is unlikely as it is accelerating).')]),
       ('Map description: projected change in maize yields by 2050 (%) - Southern Africa −15 to −25; West Africa −10 to −20; South Asia −5 to −15; northern USA 0 to −10; Canadian prairies +5 to +10.',
        [('Describe the pattern of projected change.', 'Largest losses in low-latitude regions (southern and West Africa); smaller losses in mid-latitudes; gains only in high-latitude Canada.'),
         ('Suggest why the largest losses are projected for southern Africa.', 'Crops are already near temperature thresholds; increased drought frequency; reliance on rain-fed maize; limited irrigation and adaptive capacity.')])])

S('ch05-st2', gens=['pct_climate', 'stats_hum', 'spearman_dev'],
  terms=[('vulnerability', 'the degree to which people or places are susceptible to harm from a hazard and unable to cope, shaped by poverty, location, age, gender and governance'),
         ('exposure', 'the presence of people, livelihoods and assets in places that could be affected by a hazard'),
         ('resilience', 'the ability of people, communities or systems to absorb, recover from and adapt to shocks such as climate hazards'),
         ('adaptive capacity', 'the ability of a system or community to adjust to climate change, moderate damage and take advantage of opportunities'),
         ('climate justice', 'the idea that the people and countries least responsible for emissions often suffer most from climate change and should be supported fairly')],
  facts=[('Which group accounted for most deaths in the 2003 European heatwave?', 'Elderly people, especially those living alone', ['Young children in rural areas', 'Outdoor sports players', 'Tourists'], 'Physiological vulnerability and social isolation increased risk; about 15,000 died in France alone.'),
         ('In Hurricane Katrina (2005), which New Orleans neighbourhood with a mainly low-income African-American population was devastated by levee failure?', 'The Lower Ninth Ward', ['The French Quarter', 'The Garden District', 'Uptown'], 'Low elevation and poverty combined to raise exposure and reduce capacity to evacuate.'),
         ('The ND-GAIN index ranks countries on:', 'vulnerability to climate change and readiness to adapt', ['carbon emissions per capita', 'renewable energy capacity', 'GDP growth rates'], 'ND-GAIN combines vulnerability and readiness indicators for about 185 countries.')],
  why=[('Explain why poverty increases vulnerability to climate hazards.', 'The poor often live in exposed locations (floodplains, informal settlements), have weaker housing, fewer savings or insurance, depend on climate-sensitive livelihoods such as rain-fed farming and have less access to information and health care.'),
       ('Explain why women can be more vulnerable than men to some climate hazards.', 'In some societies women have less access to warnings, swimming skills, land titles and credit, and caring roles and clothing norms limit evacuation, as in the 1991 Bangladesh cyclone where female death rates were much higher.'),
       ('Explain why the elderly and very young are particularly vulnerable to heatwaves.', 'They have weaker thermoregulation, more chronic illness and are more dependent on others; isolation and lack of air-conditioning raise risk.'),
       ('Explain why vulnerability can differ greatly within a single city.', 'Informal settlements on steep slopes or floodplains, lack of drainage and services, and low incomes contrast with protected, wealthier districts - e.g. Mumbai\'s slums in the 2005 floods.')],
  contrast=[('exposure', 'vulnerability', 'Exposure is being in the path of a hazard; vulnerability is the susceptibility to harm once exposed - two people equally exposed can have very different vulnerability.'),
            ('vulnerability', 'resilience', 'Vulnerability is susceptibility to harm; resilience is the ability to absorb, recover and adapt - reducing vulnerability builds resilience.')],
  misc=[('Everyone in a country faces the same climate risk.', 'Risk varies with location, income, age, gender, health and social networks, so impacts are highly uneven within countries.'),
        ('High-income countries are not vulnerable to climate change.', 'Exposed and marginalised groups in rich countries suffer badly (Katrina 2005, the 2003 European heatwave, 2021 heat dome).'),
        ('Vulnerability depends only on physical location.', 'Social, economic and political factors - poverty, governance, gender and age - strongly shape vulnerability.')],
  apply=[('Using a named example, explain how two different factors increased vulnerability to a climate-related hazard.', 'e.g. Hurricane Katrina 2005: poverty (about 100,000 residents had no car to evacuate) and location (Lower Ninth Ward below sea level behind failed levees) combined, causing over 1,800 deaths.', 4),
         ('Suggest why smallholder farmers in the Sahel are highly vulnerable to drought.', 'They depend on rain-fed crops and livestock, have little irrigation, savings or insurance, and face land degradation and insecurity.', 2)],
  cases=[('Hurricane Katrina in New Orleans (2005)', 'over 1,800 deaths, with the greatest losses among poor, mainly African-American, residents of low-lying areas', 'disparities in exposure and vulnerability', 'social inequality determined who could evacuate and who lived in the most exposed areas'),
         ('the 1991 Bangladesh cyclone', 'about 138,000 people died and death rates among women were several times those among men', 'gender and vulnerability', 'social norms on mobility, clothing and access to warnings increased women\'s risk'),
         ('the 2003 European heatwave in Paris', 'many of the victims were elderly people living alone in top-floor apartments', 'age and social isolation as vulnerability factors', 'physiological sensitivity and isolation raised mortality among older people'),
         ('Mumbai\'s 2005 flood', 'about 944 mm of rain in 24 hours flooded informal settlements along blocked drains and the Mithi River', 'the uneven vulnerability of urban populations', 'poor drainage and informal housing in exposed locations raised impacts for the urban poor')],
  evaluate=[('Poverty is the most important factor determining vulnerability to climate change.', ['the poor live in exposed places with weak housing and few assets', 'poor countries have lower adaptive capacity'], ['age, gender, disability and isolation matter even in rich places (2003 heatwave)', 'location and governance (levees, warnings) are crucial'], 'Poverty is the strongest underlying factor, but it interacts with location, demographic and social factors.'),
            ('Those who have contributed least to climate change are the most vulnerable to it.', ['least-developed countries emit a small share of CO₂ but suffer severe impacts (Bangladesh, Sahel, Pacific islands)', 'within countries, the poor emit least but are most exposed'], ['high emitters such as Australia and the USA also suffer severe impacts', 'vulnerability depends on governance and adaptation'], 'Broadly true at the global scale, which underpins climate justice arguments and the loss-and-damage fund.')],
  extended=[('Examine why the impacts of climate change are unequal between and within countries.', 'Award: exposure vs vulnerability; poverty, gender, age, location; examples at two scales (Katrina, Bangladesh, Sahel, 2003 heatwave); judgement.', 10, 'long')],
  res=[('Table: deaths from tropical cyclones of similar strength - Cyclone Nargis, Myanmar 2008: about 138,000; Hurricane Katrina, USA 2005: about 1,800; Cyclone Yasi, Australia 2011: 1.',
        [('Describe the differences shown.', 'Deaths ranged from about 138,000 in Myanmar to 1,800 in the USA and just 1 in Australia despite comparable intensities.'),
         ('Suggest two reasons for the differences.', 'Warning systems and evacuation capacity (Australia), poverty and housing quality, governance (Myanmar initially restricted aid), exposure of the Irrawaddy delta population.')]),
       ('Survey of 50 households in a Dhaka informal settlement after a 2023 flood: households with no savings 34; households with a member unable to work for over a week 21; households receiving no warning 28.',
        [('Calculate the percentage of households with no savings and with no warning.', f'No savings {34 / 50 * 100:.0f}%; no warning {28 / 50 * 100:.0f}%'),
         ('Explain how these factors increase vulnerability.', 'No savings means households cannot recover or rebuild quickly; lack of warning prevents moving people and assets, raising losses.')])])

S('ch05-st3', gens=['pct_climate', 'migration'],
  terms=[('threat multiplier', 'a factor (climate change) that worsens existing threats such as poverty, disease, resource scarcity and conflict'),
         ('climate migration', 'movement of people driven wholly or partly by climate-related changes such as drought, sea-level rise or extreme events'),
         ('vector-borne disease', 'an illness transmitted by organisms such as mosquitoes or ticks, e.g. malaria and dengue, whose range is affected by climate'),
         ('planned relocation', 'the organised movement of a community away from a high-risk area, e.g. coastal villages in Fiji'),
         ('resource conflict', 'a dispute or violence linked to competition for scarce resources such as water or grazing land')],
  facts=[('By about how much has the surface area of Lake Chad shrunk since the 1960s?', 'About 90%', ['About 10%', 'About 30%', 'It has grown'], 'The lake shrank from about 25,000 km² to under 2,000 km² due to drought and irrigation.'),
         ('In 2014 Kiribati purchased land in which country as a possible food-security and relocation option?', 'Fiji', ['Australia', 'New Zealand', 'Samoa'], 'About 20 km² on Vanua Levu was bought for about US$9 million.'),
         ('The 2023 Falepili Union treaty allows up to 280 citizens a year from which country to move to Australia?', 'Tuvalu', ['Kiribati', 'Fiji', 'Papua New Guinea'], 'The treaty created a special mobility pathway linked to climate threats.')],
  why=[('Explain why climate change is described as a threat multiplier.', 'It rarely causes problems on its own but intensifies existing stresses - drought on farmland, water scarcity, food prices, disease and weak governance - which can push vulnerable places into crisis, migration or conflict.'),
       ('Explain how climate change may increase the spread of vector-borne diseases.', 'Warmer temperatures allow mosquitoes and parasites to survive at higher altitudes and latitudes and breed faster, spreading malaria into East African highlands and dengue into southern Europe.'),
       ('Explain why the link between climate change and conflict is debated.', 'Conflict has many causes (politics, ethnicity, governance, economics); climate may contribute through drought and resource scarcity, but evidence is mixed and attributing a war to climate risks ignoring human responsibility, e.g. the debate over the 2006-10 Syrian drought.'),
       ('Explain why most climate-related migration is internal and short-distance.', 'Most people move to nearby towns or cities temporarily; international migration needs money, documents and networks that the poorest lack, and many prefer to stay close to land and family.')],
  contrast=[('climate migrants', 'refugees', 'Refugees are legally protected under the 1951 Convention because of persecution or conflict; people moving because of climate change have no specific legal status and are mostly internal migrants.'),
            ('slow-onset climate impacts', 'sudden-onset climate impacts', 'Slow-onset impacts (sea-level rise, desertification, glacier retreat) build over years and lead to gradual migration; sudden-onset events (floods, cyclones) cause rapid, often temporary displacement.')],
  misc=[('Climate change was the sole cause of the Syrian civil war.', 'The 2006-10 drought may have added to rural hardship and migration, but repression, governance failure and politics were the main causes.'),
        ('Millions of climate refugees are already protected by international law.', 'There is no legal category of "climate refugee"; such migrants rely on national policies or regional agreements.'),
        ('Climate change will only affect health in tropical countries.', 'Heat stress, air quality, wildfires smoke and new disease ranges (e.g. ticks, dengue in Europe) also affect high-latitude countries.')],
  apply=[('Using a named example, explain how climate change has acted as a threat multiplier.', 'e.g. Lake Chad basin: lake shrinkage of about 90% reduced fishing, farming and grazing; competition for resources and unemployment helped armed groups such as Boko Haram to recruit, contributing to displacement of about 3 million people.', 4),
         ('Suggest two health impacts of more frequent heatwaves in South Asian cities.', 'Heatstroke deaths among outdoor workers; worsening cardiovascular and respiratory illness; reduced labour productivity; water-borne disease when supplies fail.', 2)],
  cases=[('the Lake Chad basin', 'the lake shrank by about 90% while the population of the basin grew, and insurgency displaced about 3 million people', 'climate change as a threat multiplier', 'reduced water and livelihoods combined with poverty and weak governance to fuel conflict and displacement'),
         ('Kiribati\'s "migration with dignity" policy', 'the government bought land in Fiji and promoted skills for labour migration to Australia and New Zealand', 'planned adaptation through migration', 'migration is treated as a response to sea-level rise rather than only a failure to adapt'),
         ('the spread of malaria in the East African highlands', 'cases have appeared at higher altitudes in Ethiopia and Kenya as temperatures rose', 'climate impacts on health', 'warming allows disease vectors to survive in previously cool places'),
         ('the 2006-2010 Syrian drought', 'it caused crop failures and the migration of perhaps 1-1.5 million rural people to cities', 'the contested link between climate and conflict', 'climate stress added to grievances, but most researchers stress political causes of the war')],
  evaluate=[('Climate change will be the main driver of international migration in the 21st century.', ['sea-level rise threatens small island states and deltas', 'the World Bank (Groundswell) projected up to 216 million internal climate migrants by 2050'], ['most climate migration is internal and short-term', 'economic, political and social drivers dominate migration decisions'], 'Climate will increasingly influence migration, but mostly within countries and in combination with economic factors.'),
            ('Describing climate change as a threat multiplier helps governments respond effectively.', ['links climate to security encourages funding and planning', 'highlights vulnerable regions (Sahel, Lake Chad)'], ['risks securitising migrants and justifying border controls', 'can distract from political causes of conflict'], 'The concept is useful if it promotes adaptation and development rather than militarised responses.')],
  extended=[('Examine the ways in which climate change can increase risks to human health and security.', 'Award: heat, disease vectors, food/water insecurity, displacement, conflict; named examples (Lake Chad, Syria, East Africa, Pacific); debate on attribution; judgement.', 10, 'long')],
  res=[('Table: area of Lake Chad (km², approximate) - 1963: 25,000; 1973: 15,400; 1987: 1,700; 2010s: about 1,350-2,500 (seasonal).',
        [('Calculate the percentage decrease between 1963 and 1987.', f'(1,700 − 25,000)/25,000 × 100 = {pc(25000, 1700)}'),
         ('Suggest two causes of the decrease.', 'Prolonged Sahel droughts and lower rainfall in the 1970s-80s; increased irrigation withdrawals from rivers feeding the lake (Chari, Komadugu-Yobe).')]),
       ('Text: "Groundswell (World Bank, 2021) projects that, without action, up to 216 million people could be internal climate migrants by 2050, including 86 million in sub-Saharan Africa and 40 million in South Asia."',
        [('Calculate the share of the projected total in sub-Saharan Africa and South Asia combined.', f'(86 + 40)/216 × 100 = {126 / 216 * 100:.1f}%'),
         ('Suggest why these regions are expected to have the most climate migrants.', 'Large rural populations dependent on rain-fed agriculture, rapid population growth, high exposure to drought, sea-level rise and floods, and low adaptive capacity.')])])

S('ch06-st1', gens=['carbon_tax', 'energy_mix', 'carbon'],
  terms=[('mitigation', 'action to reduce or prevent greenhouse-gas emissions or enhance sinks, reducing the scale of climate change'),
         ('carbon tax', 'a charge on fossil fuels or emissions per tonne of CO₂, intended to make polluters pay and encourage low-carbon choices'),
         ('carbon capture and storage (CCS)', 'technology that captures CO₂ from power stations or industry and stores it underground, e.g. in depleted oil and gas fields'),
         ('geo-engineering', 'large-scale deliberate intervention in the climate system, such as solar radiation management or ocean fertilisation'),
         ('emissions trading scheme', 'a cap-and-trade system in which a limit on emissions is set and permits are traded, e.g. the EU ETS (2005)'),
         ('afforestation', 'planting trees on land that has not recently been forested, to create carbon sinks')],
  facts=[('Which country introduced one of the world\'s first carbon taxes in 1991, now among the highest at about SEK 1,200 per tonne?', 'Sweden', ['the USA', 'China', 'Brazil'], 'Sweden cut emissions by about a third while its economy grew.'),
         ('Where has CO₂ been stored under the North Sea since 1996, at about 1 million tonnes a year?', 'Sleipner, Norway', ['Boundary Dam, Canada', 'Drax, UK', 'Kemper, USA'], 'Sleipner injects CO₂ separated from natural gas into a saline aquifer.'),
         ('Which country generates nearly all its electricity from renewable sources (hydro, geothermal, wind)?', 'Costa Rica', ['Poland', 'South Africa', 'Saudi Arabia'], 'Costa Rica has produced about 98-99% of its electricity from renewables in most recent years.'),
         ('Which of the following is a solar radiation management proposal?', 'Injecting sulphate aerosols into the stratosphere', ['Planting mangroves', 'Building sea walls', 'Raising the price of petrol'], 'It mimics volcanic cooling but does not reduce CO₂ or ocean acidification.')],
  why=[('Explain how a carbon tax can reduce emissions.', 'It raises the price of carbon-intensive goods and fuels, giving firms and consumers an incentive to switch to low-carbon alternatives and invest in efficiency; revenues can fund renewables or be returned as dividends.'),
       ('Explain why carbon capture and storage has not been widely adopted.', 'High costs, energy penalty (it uses 15-25% of a plant\'s output), few suitable storage sites near emitters, technical problems (Boundary Dam underperformed) and a low carbon price make it uneconomic.'),
       ('Explain why geo-engineering is controversial.', 'Solar radiation management could be cheap but does not cut CO₂ or acidification, may disrupt monsoons, creates a "termination shock" risk if stopped and raises governance questions about who controls the global thermostat.'),
       ('Explain why reforestation is an attractive but limited mitigation strategy.', 'Trees absorb carbon and give co-benefits (biodiversity, soil, water), but they take decades to grow, need large areas that compete with food, may burn or be cleared, and cannot offset fossil emissions alone.')],
  contrast=[('mitigation', 'adaptation', 'Mitigation tackles the causes of climate change by reducing emissions or increasing sinks; adaptation reduces the harm from climate impacts that cannot be avoided.'),
            ('a carbon tax', 'an emissions trading scheme', 'A carbon tax fixes the price of carbon and lets emissions adjust; a cap-and-trade scheme fixes the quantity of emissions and lets the permit price adjust.')],
  misc=[('Renewable energy can be expanded without any environmental costs.', 'Dams flood valleys and displace people, wind and solar farms use land and minerals (lithium, cobalt), and intermittency requires storage or backup.'),
        ('Carbon taxes always hurt the poor most.', 'They can be regressive, but revenue recycling (e.g. Canada\'s rebates) can leave most low-income households better off.'),
        ('Geo-engineering would solve climate change, so emissions cuts are unnecessary.', 'Solar geo-engineering would mask warming but not remove CO₂, leaving ocean acidification and the risk of rapid warming if it stopped.')],
  apply=[('Using a named country, outline two mitigation strategies and their effectiveness.', 'e.g. Sweden: carbon tax since 1991 helped cut emissions by about a third since 1990 while GDP grew; expansion of hydro, nuclear and bioenergy produced almost carbon-free electricity.', 4),
         ('Suggest why mitigation requires international rather than only national action.', 'Greenhouse gases mix globally; one country\'s cuts can be offset by others\' growth or carbon leakage; free-riding means coordinated agreements are needed.', 2)],
  cases=[('Sweden\'s carbon tax', 'introduced in 1991 and now around SEK 1,200 (about US$120) per tonne, while emissions fell by about a third since 1990', 'the effectiveness of carbon pricing', 'a high, stable carbon price shifted heating and industry towards low-carbon options without stopping growth'),
         ('the Great Green Wall in the Sahel', 'launched in 2007 to restore 100 million ha across 11 countries, but only a small fraction had been restored by 2020', 'the opportunities and limits of reforestation', 'large-scale tree planting brings carbon and livelihood benefits but faces funding, survival and governance problems'),
         ('the Sleipner gas field, Norway', 'about 1 million tonnes of CO₂ a year has been injected into a saline aquifer since 1996, encouraged by Norway\'s offshore carbon tax', 'carbon capture and storage', 'CCS can work where there is a strong carbon price and suitable geology'),
         ('Costa Rica\'s electricity system', 'about 98-99% of electricity comes from hydro, geothermal, wind and biomass', 'the potential of renewable energy for mitigation', 'favourable physical geography and policy enabled near-total renewable electricity')],
  evaluate=[('Technological solutions such as carbon capture and geo-engineering offer the best hope of mitigating climate change.', ['net-zero pathways in IPCC scenarios include CO₂ removal', 'CCS can decarbonise cement and steel'], ['CCS is expensive and slow to scale; geo-engineering is risky and does not cut CO₂', 'renewables and efficiency are cheaper and available now'], 'Technology helps, but proven measures (renewables, efficiency, carbon pricing, forests) must lead; risky geo-engineering is not a substitute.'),
            ('Carbon taxes are the most effective mitigation strategy available to governments.', ['Sweden shows strong reductions with growth', 'economists favour pricing for efficiency'], ['political resistance (France\'s gilets jaunes 2018)', 'regressive effects and carbon leakage; regulation and investment also needed'], 'Carbon pricing is highly effective where politically sustainable, but it works best with regulation and public investment.')],
  extended=[('Evaluate the effectiveness of two contrasting climate change mitigation strategies.', 'Award: two named strategies with locations and data (e.g. Swedish carbon tax, EU ETS, Great Green Wall, Sleipner CCS, Costa Rica renewables); costs, benefits, scale; judgement.', 10, 'long')],
  res=[('Table: share of renewables in electricity generation (%, approximate recent year) - Costa Rica 99; Norway 98; Denmark 84; Germany 52; China 31; USA 22; Saudi Arabia 1.',
        [('Describe the variation shown.', 'Very high shares in Costa Rica and Norway (hydro), high in Denmark (wind) and Germany, moderate in China and the USA, almost none in Saudi Arabia.'),
         ('Suggest two reasons for the variation.', 'Physical resources (rivers, wind, geothermal, sunshine); government policy and subsidies (Energiewende); availability of cheap domestic fossil fuels (Saudi Arabia).')]),
       ('Text: "Sweden\'s territorial greenhouse-gas emissions fell by about 33% between 1990 and 2020 while real GDP rose by about 80%." - Swedish Environmental Protection Agency summary.',
        [('Describe what the data show about the relationship between growth and emissions.', 'Absolute decoupling: emissions fell substantially while GDP rose, showing growth does not require rising emissions.'),
         ('Suggest one limitation of using territorial emissions to judge Sweden\'s performance.', 'It excludes emissions embedded in imported goods (consumption-based emissions) and international aviation and shipping.')])])

S('ch06-st2', gens=['sea_level', 'pct_climate', 'yield'],
  terms=[('adaptation', 'adjustments in natural or human systems in response to actual or expected climate change to reduce harm or exploit opportunities'),
         ('community-based adaptation', 'adaptation planned and led by local communities using local knowledge, often supported by NGOs'),
         ('early warning system', 'an integrated system of hazard monitoring, forecasting, risk communication and preparedness that enables timely action'),
         ('managed retreat', 'the planned relocation of people and infrastructure away from areas at high risk, such as eroding coasts'),
         ('maladaptation', 'an action intended to reduce climate risk that increases vulnerability elsewhere or in the future, e.g. sea walls that encourage building in exposed areas')],
  facts=[('Approximately how many cyclone shelters has Bangladesh built along its coast?', 'About 4,000 or more', ['About 40', 'About 400', 'About 400,000'], 'Shelters plus the Cyclone Preparedness Programme volunteers have cut cyclone deaths sharply.'),
         ('The Netherlands\' "Room for the River" programme (2006-2015) mainly involved:', 'giving rivers more space by lowering floodplains, moving dykes and creating overflow channels', ['building higher concrete walls in every town', 'diverting the Rhine into Germany', 'pumping river water into the sea'], 'More than 30 projects cost about €2.3 billion.'),
         ('Hulhumalé, built to protect people from sea-level rise, is a reclaimed island in which country?', 'the Maldives', ['Tuvalu', 'Fiji', 'Vietnam'], 'It is about 2 m above sea level, higher than most Maldivian islands.')],
  why=[('Explain why early warning systems have greatly reduced cyclone deaths in Bangladesh.', 'Forecasts from the Bangladesh Meteorological Department are spread by about 76,000 Cyclone Preparedness Programme volunteers using megaphones and flags; people evacuate to shelters - deaths fell from about 300,000 (1970) and 138,000 (1991) to about 4,000 (Sidr 2007) and 26 (Amphan 2020).'),
       ('Explain why adaptation is necessary even if emissions are reduced quickly.', 'Past emissions have already committed the world to further warming and sea-level rise because of the long lifetime of CO₂ and ocean thermal inertia, so impacts will occur regardless.'),
       ('Explain why poorer communities often have less capacity to adapt.', 'They lack money, insurance, technology and access to credit and information; governments may be unable to fund infrastructure; livelihoods depend on climate-sensitive resources.'),
       ('Explain how mangrove restoration can build coastal resilience.', 'Mangroves dissipate wave energy and storm surge, trap sediment that raises land, store carbon and support fisheries, as in Vietnam\'s Mekong delta and the Sundarbans.')],
  contrast=[('hard adaptation measures', 'soft adaptation measures', 'Hard measures are engineered structures such as sea walls and embankments; soft measures include early warnings, land-use planning, insurance, ecosystem restoration and education.'),
            ('top-down adaptation', 'bottom-up adaptation', 'Top-down adaptation is planned and funded by governments or international agencies; bottom-up adaptation is led by local communities using local knowledge.')],
  misc=[('Adaptation means giving up on reducing emissions.', 'Adaptation and mitigation are complementary; both are needed because some impacts are already unavoidable.'),
        ('Building higher sea walls is always the best adaptation.', 'Sea walls are expensive, can fail, push erosion elsewhere and encourage development in risky places (maladaptation); soft or nature-based options may be better.'),
        ('Only low-income countries need to adapt to climate change.', 'All countries need adaptation, e.g. the Netherlands, Rotterdam\'s water squares and heat plans in European cities.')],
  apply=[('Using a named example, outline two adaptation strategies used by a vulnerable community.', 'e.g. coastal Bangladesh: raised homesteads and plinths above flood level; floating gardens (baira) for crops during floods; cyclone shelters with warnings.', 4),
         ('Suggest why Rotterdam is considered a world leader in climate adaptation.', 'It combines hard defences (Maeslantkering barrier) with water squares that store storm water, green roofs, floating pavilions and planning to be "climate proof".', 2)],
  cases=[('Bangladesh\'s Cyclone Preparedness Programme', 'about 76,000 volunteers and thousands of shelters helped cut deaths from 138,000 in 1991 to 26 in Cyclone Amphan (2020)', 'the effectiveness of early warning and community preparedness', 'low-cost, community-based warning systems save lives even in a low-income country'),
         ('the Room for the River programme, Netherlands', 'over 30 projects (2006-2015) lowered floodplains and relocated dykes, e.g. at Nijmegen on the Waal', 'adaptation through working with natural processes', 'giving rivers space reduces flood levels and adds amenity'),
         ('the Mekong delta, Vietnam', 'mangrove belts have been replanted and farmers are switching from rice to shrimp or salt-tolerant crops as salinity increases', 'adaptation to sea-level rise and salinisation', 'livelihood change and nature-based defences help communities cope with a changing environment'),
         ('Hulhumalé, Maldives', 'a reclaimed island about 2 m above sea level, planned to house over 200,000 people', 'land-raising as adaptation', 'creating higher land reduces exposure, though at high cost and environmental impact on reefs')],
  evaluate=[('Adaptation is a more urgent priority than mitigation for low-income countries.', ['impacts are already occurring and these countries emit little', 'adaptation saves lives immediately (Bangladesh cyclone shelters)'], ['without global mitigation, adaptation limits will be exceeded (small islands)', 'low-carbon development brings co-benefits and finance'], 'For low-income countries adaptation is the immediate priority, but it depends on global mitigation to remain feasible.'),
            ('Community-based adaptation is more effective than large-scale engineering.', ['cheap, uses local knowledge, builds social capital (Bangladesh volunteers)', 'avoids maladaptation'], ['some threats need large infrastructure (Dutch delta works, Thames Barrier)', 'communities lack funds and technical capacity'], 'The most effective approaches combine community action with appropriate infrastructure and state support.')],
  extended=[('Examine how communities can build resilience to the impacts of climate change.', 'Award: hard and soft, top-down and bottom-up strategies; named places (Bangladesh, Netherlands, Mekong, Maldives); limits; judgement.', 10, 'long')],
  res=[('Table: deaths from major cyclones in Bangladesh - Bhola 1970: about 300,000-500,000; 1991 cyclone: 138,000; Sidr 2007: about 4,200; Amphan 2020: 26.',
        [('Calculate the percentage reduction in deaths between the 1991 cyclone and Sidr.', f'(4,200 − 138,000)/138,000 × 100 = {pc(138000, 4200)}'),
         ('Suggest two reasons for the trend.', 'Improved forecasting and warnings through the Cyclone Preparedness Programme; thousands of cyclone shelters and embankments; better evacuation and community awareness.')]),
       ('Infographic description: Rotterdam Climate Proof - Maeslantkering storm-surge barrier (1997, two 210 m gates); Benthemplein water square stores 1.7 million litres of storm water; 400,000+ m² of green roofs; floating pavilion.',
        [('Classify the measures shown as hard or soft adaptation.', 'Hard: the Maeslantkering barrier; multifunctional / green-blue infrastructure: water square, green roofs, floating buildings (soft or nature-based approaches).'),
         ('Explain how the water square reduces flood risk.', 'It temporarily stores heavy rainfall (1.7 million litres), slowing runoff into sewers and preventing surface-water flooding, then releases it slowly.')])])

S('ch06-st3', gens=['carbon', 'pct_climate'],
  terms=[('UNFCCC', 'the United Nations Framework Convention on Climate Change, agreed at the 1992 Rio Earth Summit, which aims to stabilise greenhouse-gas concentrations at a safe level'),
         ('Paris Agreement', 'the 2015 agreement under the UNFCCC to keep warming well below 2 °C and pursue 1.5 °C, through nationally determined contributions'),
         ('nationally determined contribution (NDC)', 'a country\'s self-set climate pledge under the Paris Agreement, to be updated and strengthened every five years'),
         ('Kyoto Protocol', 'the 1997 agreement that set legally binding emissions targets for industrialised (Annex I) countries for 2008-2012'),
         ('loss and damage', 'climate impacts that cannot be avoided by mitigation or adaptation; a fund was agreed at COP27 (2022) to support vulnerable countries'),
         ('civil society', 'non-governmental organisations, social movements, faith groups and individuals acting collectively outside government and business')],
  facts=[('Which country never ratified the Kyoto Protocol?', 'The USA', ['Japan', 'Germany', 'the United Kingdom'], 'The USA signed but did not ratify; Canada withdrew in 2011.'),
         ('At which COP was a fund for loss and damage agreed?', 'COP27, Sharm el-Sheikh (2022)', ['COP3, Kyoto (1997)', 'COP15, Copenhagen (2009)', 'COP21, Paris (2015)'], 'The fund was operationalised at COP28 in Dubai.'),
         ('Under the Paris Agreement, how often should countries submit updated NDCs?', 'Every five years', ['Every year', 'Every ten years', 'Only once'], 'The "ratchet mechanism" aims to increase ambition over time.'),
         ('Which court case led the Dutch Supreme Court (2019) to order the government to cut emissions by 25% from 1990 levels by 2020?', 'Urgenda v the Netherlands', ['Juliana v United States', 'Massachusetts v EPA', 'Milieudefensie v Shell'], 'It was the first case in which citizens forced a government to strengthen climate action on human-rights grounds.')],
  why=[('Explain why the Paris Agreement achieved wider participation than the Kyoto Protocol.', 'It is bottom-up: every country sets its own NDC, so developing countries such as China and India take part, whereas Kyoto set binding targets only for industrialised countries; flexibility made it acceptable to the USA and others.'),
       ('Explain why global climate agreements are difficult to achieve.', 'Climate is a global commons with free-rider problems; countries differ in responsibility, wealth and vulnerability; fossil-fuel interests resist; decisions require consensus among nearly 200 parties.'),
       ('Explain how civil society can influence climate policy.', 'Through protests and campaigns (Fridays for Future, from 2018), litigation (Urgenda), divestment, scientific advocacy and lobbying, which raise public awareness and political pressure.'),
       ('Explain why cities are becoming important actors in climate governance.', 'Cities produce about 70% of energy-related CO₂, control transport, buildings and planning, and networks such as C40 allow them to act faster than national governments.')],
  contrast=[('the Kyoto Protocol', 'the Paris Agreement', 'Kyoto set legally binding targets only for industrialised countries (top-down); Paris requires all parties to submit voluntary, self-determined NDCs with binding procedures for reporting (bottom-up).'),
            ('state actors', 'non-state actors in climate governance', 'State actors are national governments negotiating treaties; non-state actors include cities, businesses, NGOs and social movements that act and lobby independently.')],
  misc=[('The Paris Agreement legally requires each country to meet its emissions target.', 'NDCs are not legally binding in content; the obligations are procedural - to prepare, communicate and report on them.'),
        ('Current pledges will keep warming to 1.5 °C.', 'UNEP estimates that current NDCs put the world on course for roughly 2.5-2.9 °C of warming this century.'),
        ('Individual protest has no effect on climate policy.', 'Movements such as Fridays for Future and Extinction Rebellion have contributed to climate emergency declarations and policy debates.')],
  apply=[('Outline two strengths and one weakness of the Paris Agreement.', 'Strengths: near-universal participation; a clear temperature goal and five-yearly ratchet. Weakness: pledges are voluntary and insufficient for 1.5 °C; no enforcement mechanism.', 3),
         ('Suggest why small island developing states (AOSIS) pushed for the 1.5 °C goal.', 'Their survival is threatened by sea-level rise and coral loss above 1.5 °C; the slogan "1.5 to stay alive" reflected existential risk.', 2)],
  cases=[('the Paris Agreement (2015)', '195 parties agreed to hold warming well below 2 °C and pursue 1.5 °C through NDCs reviewed every five years', 'global governance of climate change', 'a flexible, bottom-up framework achieved broad participation but relies on voluntary ambition'),
         ('Fridays for Future', 'a school strike started by Greta Thunberg in Stockholm in 2018 grew to millions of protesters worldwide in 2019', 'civil society action on climate change', 'youth activism raised awareness and pressure on governments'),
         ('the Urgenda v the Netherlands case', 'the Dutch Supreme Court ruled in 2019 that the state must cut emissions by 25% from 1990 levels by 2020', 'the role of litigation in climate governance', 'citizens used human-rights law to force stronger government action'),
         ('COP28 in Dubai (2023)', 'parties agreed for the first time to "transition away from fossil fuels in energy systems"', 'the slow progress of international negotiations', 'consensus decisions produce compromise wording rather than a clear phase-out')],
  evaluate=[('International agreements have been ineffective in tackling climate change.', ['global emissions have risen about 60% since 1990', 'current pledges imply about 2.5-2.9 °C warming'], ['without agreements warming projections would be higher (about 4 °C pre-Paris)', 'they drive national laws, carbon markets and climate finance'], 'Agreements have been insufficient but not ineffective; they have bent the curve and created frameworks for stronger action.'),
            ('Civil society is now more important than governments in responding to climate change.', ['litigation, protest and divestment are pushing change (Urgenda)', 'cities and businesses set net-zero targets'], ['only governments can set laws, carbon prices and treaties', 'many civil society actions depend on government response'], 'Civil society is a powerful driver, but governments remain decisive because they control regulation and finance.')],
  extended=[('Examine the role of global governance in responding to climate change.', 'Award: UNFCCC, Kyoto, Paris, COPs (Glasgow, Sharm el-Sheikh, Dubai, Baku); successes and limits; role of non-state actors; judgement.', 10, 'long')],
  res=[('Graph description: global CO₂ emissions from fossil fuels and industry (Gt) - 1990: 22.7; 1997 (Kyoto): 24.4; 2015 (Paris): 35.5; 2023: 37.4.',
        [('Calculate the percentage increase from 1990 to 2023.', f'(37.4 − 22.7)/22.7 × 100 = {pc(22.7, 37.4)}'),
         ('Use the data to comment on the effectiveness of international agreements.', 'Emissions kept rising after Kyoto and Paris, though growth slowed after 2015 (about +5% in 8 years vs +45% 1997-2015), suggesting agreements have slowed but not reversed growth.')]),
       ('Table: projected warming by 2100 (UNEP Emissions Gap Report 2023) - current policies: about 2.9 °C; unconditional NDCs: 2.5 °C; conditional NDCs: 2.5 °C; net-zero pledges fully met: 1.9 °C.',
        [('Describe what the data show.', 'Current policies would lead to about 2.9 °C; full delivery of all pledges would reduce warming to about 1.9 °C - still above 1.5 °C.'),
         ('Explain the significance of the "emissions gap".', 'There is a gap between pledged and required reductions; countries must strengthen NDCs and implement them to meet the Paris goals.')])])


# =============================================================================================
# Unit 3 Global resource consumption and security
# =============================================================================================
S('ch07-st1', gens=['pct_resource', 'footprint'],
  terms=[('extreme poverty', 'living on less than the World Bank\'s international poverty line, US$2.15 per person per day at 2017 PPP (revised to US$3.00 at 2021 PPP in 2025)'),
         ('global middle class', 'people living in households spending roughly US$10-100 per person per day (PPP), as defined by Homi Kharas'),
         ('resource consumption', 'the use of natural resources such as water, food, energy, land and minerals by people and economies'),
         ('nutrition transition', 'the shift in diets as incomes rise, from staples towards more meat, dairy, sugar, oils and processed foods'),
         ('purchasing power parity (PPP)', 'an exchange rate that adjusts for differences in the cost of living, allowing fair comparison of incomes between countries')],
  facts=[('Approximately what share of the world\'s population lived in extreme poverty in 1990 and in 2019?', 'About 38% in 1990 and about 9% in 2019', ['About 10% and 5%', 'About 60% and 40%', 'About 20% and 18%'], 'World Bank estimates show a dramatic fall, led by China and India.'),
         ('Around which year did the global middle class (Kharas definition) become more than half of the world\'s population?', 'About 2018', ['About 1950', 'About 1990', 'It has not yet happened'], 'Kharas and Hamel estimated about 3.8 billion people were middle class or rich by 2018.'),
         ('Which country accounted for the largest share of the global reduction in extreme poverty after 1980?', 'China', ['Nigeria', 'Brazil', 'the USA'], 'Around 800 million people left extreme poverty in China.')],
  why=[('Explain why the growth of the global middle class increases resource consumption.', 'Higher incomes are spent on meat and dairy (more land and water), cars and air travel (oil), larger homes, appliances and air-conditioning (electricity) and consumer goods (minerals), so per-capita demand rises sharply.'),
       ('Explain why poverty reduction has been uneven between world regions.', 'East Asia grew rapidly through export manufacturing and investment, while sub-Saharan Africa had slower growth, high population growth, conflict and commodity dependence; by 2019 most of the extremely poor lived in sub-Saharan Africa.'),
       ('Explain why rising consumption in emerging economies has global consequences.', 'Increased demand raises world prices for food, energy and minerals, increases emissions and pressure on land and water, and changes trade flows (e.g. China\'s soy imports from Brazil).'),
       ('Explain how the nutrition transition affects global land use.', 'Meat and dairy need much more land and feed per calorie than crops; rising demand drives expansion of pasture and soy, contributing to deforestation in the Amazon and Cerrado.')],
  contrast=[('absolute poverty', 'relative poverty', 'Absolute poverty is lacking income for basic needs below a fixed line (e.g. US$2.15/day); relative poverty is having much less than the typical person in one\'s own society (e.g. below 60% of median income).'),
            ('consumption per capita', 'total consumption', 'Per-capita consumption is the average used by each person; total consumption is per-capita use multiplied by population - China\'s total is large even though per-capita use is below the USA\'s.')],
  misc=[('Population growth is the only cause of rising global resource use.', 'Rising per-capita consumption from growing incomes has been as important as population growth, especially in Asia.'),
        ('Extreme poverty has been reduced equally in all world regions.', 'Most of the reduction occurred in East and South Asia; in sub-Saharan Africa the number of extremely poor people rose for decades.'),
        ('The middle class lives mainly in Europe and North America.', 'Most of the new global middle class is in Asia, especially China and India.')],
  apply=[('Using data, describe changes in resource consumption that accompany rising incomes in a named country.', 'e.g. China: meat consumption rose from about 20 kg per person in 1990 to about 60 kg; car ownership rose from very few to about 300 million vehicles; electricity use per capita increased more than fivefold.', 3),
         ('Suggest two ways that rising incomes in India could increase water consumption.', 'Greater demand for irrigated crops, meat and dairy; more domestic use (bathrooms, washing machines) and industrial water use.', 2)],
  cases=[('China\'s poverty reduction', 'about 800 million people left extreme poverty between 1980 and 2020 through industrialisation and urbanisation', 'the link between poverty reduction and resource consumption', 'rising incomes increased demand for food, energy and materials, making China the largest consumer of many resources'),
         ('the expansion of India\'s middle class', 'hundreds of millions of people entered the middle class, with rapid growth in air-conditioner, car and smartphone sales', 'the global rise in resource consumption', 'new consumers increase demand for electricity, oil and minerals'),
         ('the nutrition transition in Brazil and China', 'meat consumption rose sharply, and China imports about 60% of the world\'s traded soybeans, much from Brazil, for animal feed', 'the global impact of changing diets', 'rising meat demand in one country drives land-use change in another')],
  evaluate=[('The growth of the global middle class is a greater threat to resource security than population growth.', ['per-capita consumption rises steeply with income (meat, cars, energy)', 'middle-class growth is concentrated where populations are already large (China, India)'], ['population growth in Africa will add over a billion people', 'technology and efficiency can reduce per-capita resource use'], 'Rising affluence is currently the stronger driver, but population growth multiplies its effect.'),
            ('Reducing extreme poverty will inevitably increase pressure on the environment.', ['poverty reduction has coincided with higher emissions and resource use', 'demand for energy, food and housing rises'], ['the extra emissions from ending extreme poverty are small compared with the consumption of the rich', 'clean energy and efficiency can decouple growth'], 'Poverty reduction need not be the main pressure; the consumption patterns of the rich matter more.')],
  extended=[('Examine the relationship between poverty reduction, middle-class growth and global resource consumption.', 'Award: poverty trends and regional contrasts; middle-class definitions; consumption of food, water, energy; data; uneven responsibility; judgement.', 10, 'long')],
  res=[('Table: share of world population in extreme poverty (World Bank, %) - 1990: 38.0; 2000: 29.3; 2010: 16.2; 2019: 8.9.',
        [('Calculate the percentage fall in the extreme poverty rate between 1990 and 2019.', f'(8.9 − 38.0)/38.0 × 100 = {pc(38.0, 8.9)}'),
         ('Describe the trend and suggest one reason why it has slowed since 2019.', 'A steady, rapid fall; since 2019 progress stalled because of COVID-19, conflict and food and energy price shocks, and because the remaining poor are concentrated in fragile states.')]),
       ('Bar chart description: average meat consumption (kg per person per year) - USA 124; Brazil 100; China 63; Japan 50; India 4; Nigeria 9.',
        [('How many times greater is consumption in the USA than in India?', f'124 / 4 = {124 / 4:.0f} times'),
         ('Suggest two reasons for the variation.', 'Income levels (the USA, Brazil high); cultural and religious factors (vegetarianism and taboos on beef in India); availability and price of livestock products.')])])

S('ch07-st2', gens=['footprint', 'nir', 'pct_resource'],
  terms=[('ecological footprint', 'the area of biologically productive land and water (in global hectares) needed to produce the resources a population consumes and absorb its wastes'),
         ('biocapacity', 'the capacity of ecosystems in an area to regenerate resources and absorb wastes, measured in global hectares'),
         ('carrying capacity', 'the maximum population that an area can support sustainably with its resources and technology'),
         ('neo-Malthusian', 'a modern view, following Malthus, that population and consumption growth will exceed resources, leading to crisis unless controlled'),
         ('Earth Overshoot Day', 'the date each year on which humanity\'s demand for ecological resources exceeds what the Earth can regenerate in that year'),
         ('Boserup\'s theory', 'the view (1965) that population pressure stimulates agricultural innovation and intensification, so "necessity is the mother of invention"')],
  facts=[('In which year did Thomas Malthus publish An Essay on the Principle of Population?', '1798', ['1665', '1859', '1965'], 'He argued population grows geometrically while food grows arithmetically.'),
         ('When did Earth Overshoot Day fall in 2024?', '1 August', ['31 December', '1 March', '1 October'], 'Humanity used resources equivalent to about 1.7 Earths.'),
         ('Which 1972 report used computer models to warn of overshoot and collapse?', 'The Limits to Growth (Club of Rome)', ['The Brundtland Report', 'The Stern Review', 'The Population Bomb'], 'Meadows et al. modelled population, industry, food, pollution and resources.'),
         ('Which statement summarises Malthus\'s "positive checks"?', 'Increases in death rates through famine, disease and war', ['Delayed marriage and moral restraint', 'Technological improvements in farming', 'Government family-planning policies'], 'Preventive checks reduce births; positive checks raise deaths.')],
  why=[('Explain why the Green Revolution is often used to challenge Malthusian views.', 'High-yielding varieties, irrigation, fertilisers and pesticides from the 1960s more than doubled cereal yields in Asia and Latin America, so food supply grew faster than population, as Boserup predicted.'),
       ('Explain why the ecological footprint is a useful but limited measure of resource consumption.', 'It converts diverse consumption into one comparable area (gha) and compares it with biocapacity, but it omits some impacts (toxic pollution, freshwater use), depends on assumptions and treats carbon only as forest land needed to absorb it.'),
       ('Explain why some high-income countries have ecological footprints far above their biocapacity.', 'High per-capita consumption of energy, meat and goods combined with limited domestic land means they rely on imports and the global atmosphere, e.g. Japan or the UK run large ecological deficits.'),
       ('Explain how Boserup\'s theory differs from Malthus\'s theory.', 'Malthus saw food supply as the limit to population; Boserup argued that population growth drives agricultural change (shorter fallow, irrigation, terracing), so food supply responds to population.')],
  contrast=[('Malthusian', 'Boserupian views of population and resources', 'Malthusians argue population growth will outstrip food, causing checks such as famine; Boserupians argue population pressure leads to innovation and intensification that raises food supply.'),
            ('ecological footprint', 'biocapacity', 'The footprint measures demand on nature (gha needed for consumption and wastes); biocapacity measures nature\'s supply (gha of productive land and water available).')],
  misc=[('Malthus has been completely proven wrong.', 'Global food supply has kept pace with population, but famines, local overshoot, soil degradation and climate change show resource limits still matter in some places.'),
        ('A country with a small ecological footprint has a large biocapacity.', 'Footprint and biocapacity are separate: Bangladesh has a small footprint per person but also very small biocapacity.'),
        ('Earth Overshoot Day means the world runs out of resources on that date.', 'It means demand exceeds annual regeneration; the rest of the year is met by depleting stocks and accumulating CO₂.')],
  apply=[('Using a named example, explain how population pressure led to agricultural intensification as Boserup suggested.', 'e.g. Machakos district, Kenya: population grew about five-fold (1930-1990) but terracing, tree planting and market farming reversed land degradation ("More People, Less Erosion", Tiffen et al., 1994).', 3),
         ('Suggest two reasons why the ecological footprint of Qatar is among the highest in the world.', 'Very high energy use for air-conditioning, desalination and LNG production; high incomes and car dependence; very small biocapacity in a desert.', 2)],
  cases=[('the Green Revolution in India', 'wheat production rose from about 12 million tonnes in 1965 to over 100 million tonnes today, with Punjab as the leading region', 'the anti-Malthusian argument', 'technology raised food output faster than population growth'),
         ('Machakos district, Kenya', 'population increased about five-fold while terracing and soil conservation reversed erosion', 'Boserup\'s theory', 'population pressure stimulated investment in more intensive, sustainable farming'),
         ('the Simon-Ehrlich wager (1980-1990)', 'Julian Simon bet Paul Ehrlich that the prices of five metals would fall; they did, and Simon won', 'the debate between cornucopian and neo-Malthusian views', 'substitution and innovation reduced scarcity, supporting the optimistic view'),
         ('Earth Overshoot Day', 'the date moved from late December in 1971 to about 1 August by 2024', 'the global ecological footprint', 'humanity now uses resources equivalent to about 1.7 Earths each year')],
  evaluate=[('Malthus\'s ideas are still relevant to the 21st century.', ['climate change, soil degradation and water scarcity may limit food supply', 'the global footprint exceeds biocapacity (about 1.7 Earths)'], ['food production has outpaced population since 1798', 'fertility is falling globally; technology and trade raise carrying capacity'], 'Malthus\'s simple model was wrong about food, but neo-Malthusian concerns about environmental limits remain relevant.'),
            ('The ecological footprint is the best way to measure resource consumption.', ['a single comparable figure that links consumption to biocapacity', 'reveals overshoot and inequality between countries'], ['omits water and pollution; relies on assumptions', 'material footprints and water footprints give other perspectives'], 'It is a powerful communication tool but should be used with other indicators.')],
  extended=[('Evaluate Malthusian and Boserupian views on the relationship between population and resources.', 'Award: both theories accurately explained; evidence (Green Revolution, Machakos, famine, Limits to Growth, overshoot); neo-Malthusian and cornucopian updates; judgement about scale and context.', 10, 'long')],
  res=[('Table: ecological footprint and biocapacity (global hectares per person, recent year) - USA 8.0, 3.4; China 3.7, 0.9; Brazil 2.6, 8.6; India 1.2, 0.4; world 2.6, 1.5.',
        [('Calculate the ecological balance for each country and state whether it is a reserve or deficit.', 'USA −4.6 (deficit); China −2.8 (deficit); Brazil +6.0 (reserve); India −0.8 (deficit); world −1.1 (deficit).'),
         ('Calculate how many Earths would be needed if everyone lived like the average US resident (world biocapacity 1.5 gha).', f'8.0 / 1.5 ≈ {8.0 / 1.5:.1f} Earths')]),
       ('Line graph description: Earth Overshoot Day - 1971: 25 December; 1990: 11 October; 2000: 22 September; 2010: 7 August; 2024: 1 August.',
        [('Describe the trend shown.', 'Overshoot Day moved earlier by nearly five months, rapidly from 1971 to 2010 and more slowly since 2010.'),
         ('Suggest a reason why the trend has slowed since 2010.', 'Slower growth in emissions per person and in some consumption, efficiency gains, and the 2020 COVID-19 dip; population and consumption growth continue but more slowly.')])])

S('ch07-st3', gens=['energy_mix', 'water_stress', 'pct_resource', 'virtual_water'],
  terms=[('water withdrawal', 'the total volume of freshwater taken from surface or groundwater sources for agriculture, industry or domestic use'),
         ('primary energy', 'energy in its raw form before conversion, e.g. coal, crude oil, natural gas, uranium, wind and sunlight'),
         ('energy mix', 'the combination of different energy sources used by a country or the world'),
         ('arable land', 'land used for growing crops that are replanted after each harvest'),
         ('water footprint', 'the total volume of freshwater used to produce the goods and services consumed by an individual, business or country')],
  facts=[('Approximately what share of global freshwater withdrawals is used by agriculture?', 'About 70%', ['About 10%', 'About 30%', 'About 95%'], 'Industry uses about 19% and domestic uses about 11% (FAO AQUASTAT).'),
         ('Approximately what share of global primary energy still came from fossil fuels in 2023?', 'About 80%', ['About 20%', 'About 50%', 'About 98%'], 'Oil, coal and gas together supplied about 81% (Energy Institute Statistical Review 2024).'),
         ('Which country is the largest consumer of energy in the world?', 'China', ['the USA', 'India', 'Russia'], 'China uses about 27% of global primary energy, mainly coal.'),
         ('About what share of the world\'s habitable land is used for agriculture?', 'About half', ['About 5%', 'About 20%', 'About 90%'], 'Most is pasture for livestock (Our World in Data).')],
  why=[('Explain why energy consumption per capita varies greatly between countries.', 'It reflects income, industrial structure, climate (heating/cooling), transport patterns and the price and availability of energy; Iceland and Qatar use over 100 times more per person than Chad or Niger.'),
       ('Explain why agriculture dominates water withdrawals in many low- and middle-income countries.', 'Irrigated farming feeds large rural populations in dry or monsoonal climates (India, Pakistan, Egypt), and industry and domestic supply networks are smaller; in high-income countries industry and power plants take a larger share.'),
       ('Explain why global energy consumption has continued to rise despite efficiency gains.', 'Population growth and rising incomes in Asia and Africa increase demand for electricity, transport and industry; efficiency gains are offset by more use (the rebound effect).'),
       ('Explain why land use patterns are changing globally.', 'Cropland and pasture expand in the tropics (Brazil, Indonesia) to meet rising demand for soy, beef and palm oil, while some high-income countries see farmland abandonment and reforestation.')],
  contrast=[('water withdrawal', 'water consumption', 'Withdrawal is water removed from a source, some of which returns (e.g. cooling water); consumption is water used up and not returned, e.g. evaporated in irrigation or incorporated in products.'),
            ('renewable energy', 'non-renewable energy', 'Renewable energy (solar, wind, hydro) is naturally replenished; non-renewable energy (fossil fuels, uranium) comes from finite stocks that are depleted by use.')],
  misc=[('Most of the world\'s freshwater is used in homes.', 'Domestic use is only about 11% of withdrawals; agriculture uses about 70%.'),
        ('Renewables now supply most of the world\'s energy.', 'Renewables supply about 30% of electricity but under 15% of primary energy; fossil fuels still dominate.'),
        ('Energy use is similar in all high-income countries.', 'Per-capita use varies widely: Canada and the USA use about twice as much as Germany or Japan because of climate, distance, lifestyle and prices.')],
  apply=[('Using data, compare the energy mix of two named countries.', 'e.g. France: about 65-70% of electricity from nuclear; Poland: about 60% from coal (falling); reflects resource endowment and policy choices.', 3),
         ('Suggest why water withdrawals per capita are very high in Turkmenistan and the USA.', 'Turkmenistan irrigates cotton in a desert with inefficient canals from the Amu Darya; the USA uses large amounts for thermoelectric cooling and irrigation in the arid West.', 2)],
  cases=[('China\'s energy consumption', 'China uses about 27% of global primary energy and about half of the world\'s coal', 'global patterns of energy consumption', 'industrialisation has made China the dominant consumer, mainly of coal'),
         ('irrigation in the Punjab (India and Pakistan)', 'canal and tube-well irrigation supports wheat and rice but groundwater is falling by up to 1 m a year in places', 'the dominance of agriculture in water consumption', 'intensive irrigated farming uses most of the region\'s water'),
         ('soy expansion in Brazil\'s Cerrado', 'about half of the Cerrado\'s native vegetation has been converted, much to soy and pasture', 'changing global land use', 'global demand for feed and meat drives conversion of natural ecosystems')],
  evaluate=[('Global resource consumption is mainly driven by high-income countries.', ['the richest 10% account for about half of consumption-based emissions', 'high per-capita energy, water and material use in the USA, Canada, Australia'], ['China is the largest total consumer of energy and many minerals', 'consumption in emerging economies is growing fastest'], 'High-income consumers drive most per-capita use, but emerging economies now dominate growth in total consumption.'),
            ('Water is a more critical global resource issue than energy.', ['there is no substitute for water; 2.2 billion lack safely managed drinking water', 'agriculture depends on it'], ['energy enables water supply (pumping, desalination)', 'energy transitions are central to climate change'], 'Both are critical and interlinked through the water-energy-food nexus; water is more locally critical, energy more globally significant.')],
  extended=[('Examine global patterns and trends in the consumption of water, land and energy.', 'Award: data on each resource; spatial variation (per capita and total); trends; drivers; interconnections; judgement.', 10, 'long')],
  res=[('Table: global primary energy consumption by source, 2023 (EJ, approximate) - oil 196; coal 164; natural gas 144; hydro 40; nuclear 25; wind 22; solar 16; other renewables 13.',
        [('Calculate the percentage share of fossil fuels.', f'(196 + 164 + 144)/{196 + 164 + 144 + 40 + 25 + 22 + 16 + 13} × 100 = {504 / 620 * 100:.1f}%'),
         ('Calculate the share of wind and solar combined.', f'(22 + 16)/620 × 100 = {38 / 620 * 100:.1f}%')]),
       ('Pie chart description: global freshwater withdrawals by sector - agriculture 70%; industry 19%; domestic 11%. Total about 4,000 km³ per year.',
        [('Calculate the volume used by agriculture.', '0.70 × 4,000 = 2,800 km³ per year'),
         ('Suggest how the pie chart for a high-income country such as Germany might differ.', 'A much smaller agricultural share and a much larger industrial share (power-station cooling), because farming is rain-fed and industry is large.')])])

S('ch08-st1', gens=['energy_mix', 'virtual_water', 'water_stress'],
  terms=[('water-food-energy nexus', 'the interdependence of water, food and energy security: water is needed to produce food and energy, energy is needed to supply water and food, and land links all three'),
         ('resource security', 'reliable, affordable and sustainable access to sufficient resources such as water, food and energy'),
         ('biofuel', 'a fuel produced from biomass, e.g. ethanol from sugarcane or maize and biodiesel from palm or rapeseed oil'),
         ('desalination', 'the removal of salt from seawater or brackish water to produce freshwater, an energy-intensive process'),
         ('fossil water', 'groundwater stored in aquifers for thousands of years that is not significantly recharged today')],
  facts=[('Approximately what share of the US maize harvest is used to make ethanol?', 'About 35-40%', ['About 1%', 'About 10%', 'About 90%'], 'The Renewable Fuel Standard drives demand; critics link biofuels to the 2007-08 food price spike.'),
         ('Why did Saudi Arabia phase out wheat production by 2016?', 'To conserve non-renewable fossil groundwater', ['Because of a trade ban', 'Because wheat prices collapsed', 'Because of heavy rainfall'], 'Irrigation had depleted ancient aquifers; Saudi Arabia now imports wheat and invests in farmland abroad.'),
         ('In Indian Punjab, which policy has encouraged over-pumping of groundwater for rice?', 'Free or heavily subsidised electricity for farm pumps', ['A ban on tube wells', 'High water prices', 'Compulsory drip irrigation'], 'Free power removes the incentive to save water and energy.')],
  why=[('Explain how the water-food-energy nexus links the three resources.', 'Agriculture uses about 70% of freshwater and much energy (pumps, fertiliser, machinery); energy production needs water (cooling, hydropower, biofuels); water supply needs energy (pumping, treatment, desalination); a change in one affects the others.'),
       ('Explain why biofuels can threaten food security.', 'Crops and land used for fuel (US maize, Brazilian sugarcane, Indonesian palm oil) compete with food production, raising food prices and driving land-use change.'),
       ('Explain why desalination illustrates trade-offs within the nexus.', 'It increases water security in arid countries (Israel, Saudi Arabia) but uses large amounts of energy - often from fossil fuels - raising emissions and costs, and produces brine waste.'),
       ('Explain how free electricity for irrigation can undermine resource security.', 'It encourages over-pumping of groundwater, lowering water tables, raising energy demand and costs to the state, and threatening future food production, as in Punjab.')],
  contrast=[('water security', 'energy security', 'Water security is reliable access to sufficient safe water for people, economy and ecosystems; energy security is reliable, affordable access to energy supplies, including resilience to supply disruption.'),
            ('first-generation biofuels', 'second-generation biofuels', 'First-generation biofuels use food crops (maize, sugarcane, palm oil); second-generation biofuels use non-food biomass such as crop residues, wood waste and grasses, reducing competition with food.')],
  misc=[('Increasing energy supply always improves water security.', 'Some energy sources (coal, nuclear, biofuels, hydropower) use or divert large amounts of water, so energy expansion can reduce water availability.'),
        ('Resource security problems can be solved one resource at a time.', 'Because of the nexus, solving one problem can worsen another (e.g. biofuels for energy raising food prices); integrated policies are needed.'),
        ('Hydropower has no effect on food production.', 'Dams can flood farmland, alter fisheries and sediment supply to deltas (e.g. the Mekong), affecting food production downstream.')],
  apply=[('Using a named example, explain how a change in one resource has affected another.', 'e.g. Saudi Arabia irrigated desert wheat from fossil aquifers in the 1980s-2000s (becoming an exporter), depleting groundwater; it phased out wheat by 2016 and now imports grain and invests in farmland abroad (Sudan, Ethiopia).', 4),
         ('Suggest how solar-powered irrigation pumps could affect the water-food-energy nexus in India.', 'They provide cheap, low-carbon energy for irrigation, raising yields, but zero marginal cost may encourage over-extraction unless farmers can sell surplus power to the grid.', 3)],
  cases=[('Saudi Arabia\'s wheat programme', 'wheat output peaked at over 4 million tonnes in the early 1990s using fossil groundwater, then was phased out by 2016', 'the water-food nexus', 'self-sufficiency in food was achieved by mining a non-renewable water resource'),
         ('groundwater irrigation in Punjab, India', 'free electricity for about 1.4 million tube wells has led water tables to fall rapidly in most of the state', 'energy-water-food interdependence', 'energy subsidies drive water depletion that threatens food production'),
         ('the US ethanol mandate', 'about 35-40% of US maize is used for ethanol under the Renewable Fuel Standard', 'the energy-food nexus', 'energy policy diverted a major food crop and affected world grain prices'),
         ('the Grand Ethiopian Renaissance Dam', 'a 5.15 GW dam on the Blue Nile filling since 2020', 'trade-offs in the water-energy nexus', 'energy security for Ethiopia raises water security concerns downstream in Sudan and Egypt')],
  evaluate=[('Integrated management of the water-food-energy nexus is essential for resource security.', ['interdependence means single-resource policies create trade-offs (biofuels, Punjab)', 'integrated planning can find synergies (solar irrigation, wastewater reuse)'], ['integrated approaches are complex and institutions are divided by sector', 'some issues are best solved by targeted policies'], 'Integration is essential in principle, though practical progress requires coordinated institutions and pricing.'),
            ('Energy security is the most important element of the nexus.', ['energy enables water supply and modern farming', 'energy shocks (2022) raised fertiliser and food prices'], ['water has no substitutes and limits food and energy', 'food security directly affects survival'], 'Each element is critical; energy often acts as the lever, but water is the fundamental constraint in many regions.')],
  extended=[('Examine the interactions between water, food and energy security, with reference to examples.', 'Award: nexus explained with flows; named examples (Saudi wheat, Punjab, biofuels, GERD, desalination); trade-offs and synergies; judgement.', 10, 'long')],
  res=[('Table: approximate water needed to produce energy (litres per MWh) - coal power (wet cooling) 2,000; nuclear 2,500; natural gas combined cycle 750; solar PV 100; wind about 0.',
        [('How many times more water does nuclear power use than gas combined-cycle per MWh?', f'2,500 / 750 = {2500 / 750:.1f} times'),
         ('Explain what the data suggest about energy choices in water-scarce regions.', 'Solar PV and wind use very little water, so they increase energy security without competing with water for food; thermal plants add water stress.')]),
       ('Text: "Producing 1 m³ of desalinated seawater by reverse osmosis requires about 3-4 kWh of electricity." Israel desalinates about 600 million m³ per year.',
        [('Calculate the electricity needed for Israel\'s desalination at 3.5 kWh/m³ (in GWh).', f'600 million × 3.5 kWh = {600 * 3.5:,.0f} million kWh = {600 * 3.5:,.0f} GWh ≈ {600 * 3.5 / 1000:.1f} TWh'),
         ('Explain one nexus trade-off shown by desalination.', 'It improves water security but increases energy demand and, if powered by gas, emissions; costs also rise.')])])

S('ch08-st2', gens=['water_stress', 'virtual_water', 'pct_water'],
  terms=[('virtual water', 'the volume of water used to produce a good or service, which is effectively traded when the good is traded (J.A. Allan, 1993)'),
         ('physical water scarcity', 'when there is not enough water to meet all demands, including environmental flows, as in arid regions'),
         ('economic water scarcity', 'when water is available but lack of investment, infrastructure or institutions prevents people from accessing it'),
         ('water stress', 'when annual renewable water supplies fall below about 1,700 m³ per person (Falkenmark indicator)'),
         ('Day Zero', 'the date on which a city\'s taps would be turned off because reservoirs are too low, a term popularised in Cape Town in 2018')],
  facts=[('To what daily limit per person was Cape Town\'s water use restricted in 2018?', '50 litres', ['5 litres', '150 litres', '500 litres'], 'Demand management helped avoid Day Zero after three years of drought.'),
         ('Approximately how much virtual water is embedded in 1 kg of beef (global average)?', 'About 15,000 litres', ['About 150 litres', 'About 1,500 litres', 'About 150,000 litres'], 'Water Footprint Network estimate: about 15,400 L/kg, mostly rainwater for feed crops.'),
         ('What are Singapore\'s "Four National Taps"?', 'Local catchment, imported water, NEWater (recycled) and desalinated water', ['Rain, rivers, lakes and glaciers', 'Four reservoirs in Malaysia', 'Bottled, piped, well and tanker water'], 'The strategy reduces reliance on water imported from Malaysia under a 1962 agreement.'),
         ('Below what level of renewable water per person does the Falkenmark indicator define absolute scarcity?', '500 m³ per year', ['1,700 m³ per year', '5,000 m³ per year', '50 m³ per year'], 'Stress is below 1,700 and scarcity below 1,000 m³.')],
  why=[('Explain how virtual water trade can improve water security in arid countries.', 'By importing water-intensive goods such as wheat and beef, countries like Jordan and Egypt avoid using scarce domestic water to grow them, effectively importing water embedded in food.'),
       ('Explain why water demand is rising faster than population in many regions.', 'Rising incomes increase demand for water-intensive diets, industry and energy; urbanisation increases domestic use per person; irrigation expands.'),
       ('Explain why Cape Town came close to Day Zero in 2018.', 'Three consecutive dry winters (2015-2017) - the worst drought in a century - combined with population growth, reliance on surface reservoirs and slow investment in new supply.'),
       ('Explain how Singapore has increased its water security.', 'It diversified supply through NEWater recycling (about 40% of demand), desalination (up to 25-30%), urban catchment reservoirs such as Marina Barrage and demand management, reducing dependence on Malaysia.')],
  contrast=[('physical water scarcity', 'economic water scarcity', 'Physical scarcity means there is insufficient water to meet demand (e.g. Middle East, North Africa); economic scarcity means water exists but people lack infrastructure or money to access it (e.g. much of sub-Saharan Africa).'),
            ('blue water', 'green water', 'Blue water is surface and groundwater used for irrigation and supply; green water is rainwater stored in soil and used by plants, the main source for rain-fed crops.')],
  misc=[('Water scarcity is only a problem in deserts.', 'Economic scarcity affects humid regions too, and cities such as Chennai (2019) and São Paulo (2014-15) faced crises in monsoonal or humid climates.'),
        ('Virtual water trade means water is physically transported.', 'The water is used where the good is produced; trade only shifts the water use embedded in products.'),
        ('Desalination can solve water scarcity everywhere.', 'It is energy-intensive and costly, produces brine and is most practical for wealthy coastal states; inland and poor regions cannot rely on it.')],
  apply=[('Using a named city, outline two strategies used to manage a water crisis.', 'e.g. Cape Town 2018: restricting use to 50 L per person per day with tariffs and public dashboards; pressure management and leak repair; new groundwater and small desalination plants.', 4),
         ('Suggest why Egypt is described as a large importer of virtual water.', 'It imports about 12-13 million tonnes of wheat a year (one of the largest importers), saving domestic Nile water needed for other uses.', 2)],
  cases=[('Cape Town\'s 2018 drought', 'demand was cut by about half to around 500 million litres a day and Day Zero was avoided', 'demand-side management of water security', 'restrictions, pricing and public awareness can rapidly cut urban water use'),
         ('Singapore\'s Four National Taps strategy', 'NEWater and desalination together can meet much of the city-state\'s demand', 'technological solutions to water insecurity', 'diversifying sources reduces dependence on imported water'),
         ('Chennai\'s 2019 water crisis', 'the city\'s four main reservoirs ran almost dry and water trains were brought from Jolarpettai, about 200 km away', 'the impact of failed monsoons and urban growth on water security', 'loss of wetlands and lakes to urban expansion reduced natural storage'),
         ('Jordan', 'one of the most water-scarce countries, with under 100 m³ of renewable water per person per year', 'physical water scarcity', 'very low rainfall, rapid population growth and refugee inflows exceed supply')],
  evaluate=[('Technology offers the best solution to water insecurity.', ['desalination and recycling transformed Israel and Singapore', 'drip irrigation increases efficiency'], ['high cost and energy use limit access for poor countries', 'demand management, pricing and governance address root causes'], 'Technology is powerful for wealthy states, but governance, pricing and demand reduction are more widely applicable.'),
            ('Virtual water trade increases global water security.', ['allows water-scarce countries to import food', 'trade can shift production to water-rich areas'], ['exporters such as India and Pakistan export virtual water from depleting aquifers', 'dependence on imports exposes importers to price shocks'], 'Virtual water trade helps when exporters are water-rich, but can shift stress to vulnerable exporters.')],
  extended=[('Examine the factors that affect water security at different scales.', 'Award: physical and economic scarcity; demand growth; quality; governance; named cases (Cape Town, Singapore, Chennai, Jordan); virtual water; judgement.', 10, 'long')],
  res=[('Table: renewable freshwater per capita (m³ per year, approximate) - Canada 72,000; Brazil 40,000; UK 2,200; India 1,340; Egypt 510; Jordan 80.',
        [('Classify each country using the Falkenmark indicator.', 'Canada, Brazil, UK: no stress (>1,700); India: stress (1,000-1,700); Egypt: scarcity (500-1,000); Jordan: absolute scarcity (<500).'),
         ('How many times more water per person does Canada have than India?', f'72,000 / 1,340 ≈ {72000 / 1340:.0f} times')]),
       ('Graph description: Cape Town dam storage (% full) - 2014: 100; 2015: 72; 2016: 60; 2017: 38; January 2018: 26; September 2018: 70.',
        [('Describe the trend shown.', 'A steady decline from full in 2014 to 26% in early 2018, then recovery to 70% by September 2018 after winter rains and restrictions.'),
         ('Suggest two reasons for the recovery in 2018.', 'Return of winter rainfall; demand cut by about half through restrictions (50 L/person/day), pricing and agricultural cutbacks.')])])

S('ch08-st3', gens=['yield', 'pct_resource', 'virtual_water'],
  terms=[('food security', 'when all people at all times have physical and economic access to sufficient, safe and nutritious food (FAO, 1996)'),
         ('land grabbing', 'large-scale acquisition of farmland, often in low-income countries, by foreign governments, investors or corporations'),
         ('food miles', 'the distance food travels from where it is produced to where it is consumed'),
         ('undernourishment', 'a condition in which a person\'s regular food intake is insufficient to provide the dietary energy needed for a normal, active, healthy life'),
         ('food sovereignty', 'the right of peoples to define their own food and agriculture systems, as promoted by La Vía Campesina')],
  facts=[('According to the FAO (SOFI 2024), approximately how many people faced hunger in 2023?', 'About 733 million', ['About 73 million', 'About 2 billion', 'About 3 billion'], 'About 9% of the world\'s population was undernourished.'),
         ('Which 2008 land deal in Madagascar, for about 1.3 million hectares, contributed to political unrest and was cancelled?', 'The Daewoo Logistics deal', ['The Cargill deal', 'The Nestlé deal', 'The Wilmar deal'], 'The South Korean company planned maize and palm oil for export.'),
         ('What are the four dimensions (pillars) of food security?', 'Availability, access, utilisation and stability', ['Production, export, import and storage', 'Price, taste, quality and quantity', 'Land, water, labour and capital'], 'The FAO framework distinguishes these four pillars.'),
         ('Which country imports about 60% of the world\'s traded soybeans?', 'China', ['India', 'Germany', 'Japan'], 'Soy is used mainly for pig and poultry feed.')],
  why=[('Explain why changing diets increase pressure on food systems.', 'Rising demand for meat and dairy requires several kilograms of feed per kilogram of meat, more land and water, and higher emissions; it diverts grain from direct human consumption.'),
       ('Explain why food insecurity can exist even when global food production is sufficient.', 'Hunger is mainly about access: poverty, conflict, high prices, poor infrastructure and inequality prevent people buying or obtaining enough food (Sen\'s entitlement approach).'),
       ('Explain why land grabbing is controversial.', 'Investors gain land, water and exports, but local farmers and pastoralists may lose customary land without consent, food may be exported from food-insecure countries, and benefits (jobs, infrastructure) are often smaller than promised.'),
       ('Explain how the 2022 war in Ukraine affected global food security.', 'Ukraine and Russia supplied about 30% of world wheat exports; blockade of Black Sea ports and higher fertiliser and energy costs raised world prices, hitting import-dependent countries such as Egypt, Lebanon and Somalia.')],
  contrast=[('food availability', 'food access', 'Availability is whether enough food is produced or imported; access is whether people can obtain it through income, markets or entitlements.'),
            ('food security', 'food sovereignty', 'Food security focuses on whether people have enough food from any source; food sovereignty emphasises local control over how and what food is produced.')],
  misc=[('Hunger exists because the world does not produce enough food.', 'Global production exceeds calorie needs; hunger is mainly caused by poverty, conflict, waste and unequal access.'),
        ('Land grabs always harm the host country.', 'Some investments bring jobs, infrastructure and technology; outcomes depend on contracts, governance and respect for land rights.'),
        ('Reducing food miles always reduces the carbon footprint of food.', 'Production methods often matter more: tomatoes grown in heated UK greenhouses can emit more than tomatoes trucked from Spain.')],
  apply=[('Using a named example, outline two impacts of a land acquisition on local people.', 'e.g. Ethiopia\'s Gambela region: large leases to foreign investors such as Karuturi (India) were linked to relocation ("villagisation") of local Anuak communities and loss of grazing and forest land, while promised jobs were few.', 4),
         ('Suggest two ways that reducing food waste could improve food security.', 'About a third of food produced is lost or wasted; better storage and cold chains in low-income countries and reduced retail/household waste in high-income countries would increase supply and lower prices.', 2)],
  cases=[('the 2007-2008 food price crisis', 'world prices of rice, wheat and maize roughly doubled and food riots occurred in over 30 countries', 'the vulnerability of food access to price shocks', 'poor households spending most of their income on food lost access when prices rose'),
         ('the Daewoo-Madagascar land deal (2008)', 'a plan to lease about 1.3 million ha for export crops contributed to the fall of the government in 2009 and was cancelled', 'land grabbing', 'foreign acquisition of farmland in a food-insecure country provoked resistance'),
         ('China\'s soybean trade with Brazil', 'China imports about 100 million tonnes of soy a year, much from Brazil', 'the globalisation of food systems', 'a dietary shift in one country drives land-use change and exports in another'),
         ('famine in Somalia (2011)', 'drought, conflict and restricted humanitarian access led to about 260,000 deaths', 'the role of conflict and governance in food insecurity', 'drought became famine because conflict blocked markets and aid')],
  evaluate=[('Poverty, rather than food production, is the main cause of food insecurity.', ['global calorie supply exceeds needs; most hungry people are poor rural households', 'price spikes harm access (2008)'], ['low yields and climate shocks reduce availability in the Sahel', 'conflict causes most famines (Somalia, Yemen, Sudan)'], 'Poverty is the dominant underlying cause, but conflict and climate increasingly drive acute hunger.'),
            ('Large-scale land acquisitions bring more costs than benefits to host countries.', ['loss of customary land and displacement (Gambela)', 'export orientation in food-insecure countries'], ['investment, jobs and technology transfer', 'underused land can be made productive'], 'Costs usually outweigh benefits where land rights are weak; good governance can change the balance.')],
  extended=[('Examine the factors that threaten global food security.', 'Award: four pillars; diets, climate, conflict, prices, land grabbing, biofuels, waste; named examples and data; judgement on most important factor at different scales.', 10, 'long')],
  res=[('Table: FAO Food Price Index (2014-2016 = 100) - 2006: 72; 2008: 118; 2011: 131; 2020: 98; 2022: 144; 2024: 122.',
        [('Calculate the percentage change in the index from 2020 to 2022.', f'(144 − 98)/98 × 100 = {pc(98, 144)}'),
         ('Suggest two reasons for the peak in 2022.', 'War in Ukraine disrupted wheat, maize and sunflower-oil exports; high energy and fertiliser costs; post-COVID demand recovery.')]),
       ('Table: number of undernourished people (FAO, millions) - 2005: 805; 2014: 572; 2019: 613; 2023: 733.',
        [('Describe the trend shown.', 'A fall from 805 to 572 million between 2005 and 2014, then a rise to 733 million by 2023.'),
         ('Calculate the percentage increase from 2014 to 2023 and suggest one reason for it.', f'{pc(572, 733)}; conflict, climate extremes and the COVID-19 economic shock.')])])

S('ch08-st4', gens=['energy_mix', 'pct_resource', 'carbon'],
  terms=[('energy security', 'the uninterrupted availability of energy sources at an affordable price (IEA)'),
         ('energy mix', 'the combination of primary energy sources that a country uses'),
         ('energy geopolitics', 'the influence of energy resources, supply routes and dependence on relations between states'),
         ('chokepoint', 'a narrow sea passage through which large volumes of energy are shipped, e.g. the Strait of Hormuz or Strait of Malacca'),
         ('critical minerals', 'minerals essential for low-carbon technologies and with supply risks, e.g. lithium, cobalt, rare earth elements')],
  facts=[('Approximately what share of EU gas imports came from Russia in 2021?', 'About 40%', ['About 5%', 'About 20%', 'About 80%'], 'The share fell to under 15% by 2023 after the invasion of Ukraine.'),
         ('About what share of global oil consumption passes through the Strait of Hormuz?', 'About 20%', ['About 2%', 'About 50%', 'About 80%'], 'Around 20 million barrels a day transit the strait.'),
         ('Which country produces about 70% of the world\'s mined cobalt?', 'The Democratic Republic of the Congo', ['Chile', 'Australia', 'China'], 'Cobalt is essential for many lithium-ion batteries.'),
         ('After which event did Japan shut down all its nuclear reactors, increasing imports of LNG?', 'The Fukushima Daiichi disaster (2011)', ['The Chernobyl disaster (1986)', 'The 1973 oil crisis', 'The Kobe earthquake (1995)'], 'Japan imports about 90% of its primary energy.')],
  why=[('Explain why dependence on imported energy reduces energy security.', 'Supply can be cut by political disputes, conflict or chokepoint closure, and prices are set by world markets, e.g. Europe\'s dependence on Russian gas before 2022.'),
       ('Explain how the transition to renewable energy changes energy geopolitics.', 'Countries reduce dependence on fossil-fuel exporters but become dependent on critical minerals and manufacturing (China makes about 80% of solar panels and refines most rare earths), creating new supply risks.'),
       ('Explain why some countries choose nuclear power to increase energy security.', 'Uranium is energy-dense, can be stockpiled and comes from stable suppliers (Canada, Australia); nuclear provides steady low-carbon baseload power, as in France.'),
       ('Explain why intermittency is a challenge for energy security.', 'Wind and solar output varies with weather and time of day, so grids need storage, interconnectors or backup capacity to match supply and demand.')],
  contrast=[('energy security', 'energy poverty', 'Energy security is national reliability and affordability of supply; energy poverty is the inability of households to access or afford modern energy services (about 685 million people lack electricity).'),
            ('energy independence', 'energy diversification', 'Independence means meeting demand from domestic sources; diversification means using a range of sources and suppliers to reduce risk, even if imports continue.')],
  misc=[('Renewable energy removes all energy security risks.', 'Renewables reduce fuel import risks but create risks of intermittency and dependence on critical minerals and foreign manufacturing.'),
        ('Countries with large fossil-fuel reserves are always energy secure.', 'Exporters may lack refining capacity (Nigeria imported petrol), and energy poverty can coexist with large reserves.'),
        ('Energy security is only about the quantity of supply.', 'Affordability, reliability, sustainability and the security of transport routes all matter.')],
  apply=[('Using a named example, explain how a geopolitical event affected energy security.', 'e.g. after Russia invaded Ukraine (2022), gas prices in Europe rose to record levels; the EU cut Russian gas imports, built LNG terminals (e.g. Germany\'s Wilhelmshaven, opened in about 10 months) and accelerated renewables.', 4),
         ('Suggest two strategies a country could use to improve its energy security.', 'Diversify suppliers and sources (LNG, renewables, nuclear); build storage and strategic reserves; improve efficiency; develop interconnectors with neighbours.', 2)],
  cases=[('Europe\'s 2022 gas crisis', 'Russian supply cuts and the Nord Stream sabotage pushed gas prices to record highs', 'the geopolitics of energy security', 'dependence on a single supplier exposed Europe to political leverage'),
         ('Germany\'s Energiewende', 'renewables rose to over half of electricity, but nuclear closure (2023) and gas dependence created vulnerability', 'trade-offs in energy transitions', 'a rapid transition improved sustainability but also changed supply risks'),
         ('China\'s "Malacca dilemma"', 'about 80% of China\'s oil imports pass through the Strait of Malacca', 'chokepoints and energy security', 'dependence on one shipping route encourages pipelines through Myanmar and Central Asia and the Belt and Road Initiative'),
         ('France\'s nuclear programme', 'the Messmer Plan after the 1973 oil crisis gave France about 56 reactors producing about 65-70% of its electricity', 'policy responses to energy insecurity', 'a state-led shift to domestic nuclear generation reduced reliance on imported oil')],
  evaluate=[('The transition to renewable energy will increase global energy security.', ['reduces dependence on fossil-fuel exporters and chokepoints', 'domestic resources (wind, sun) are widely distributed'], ['new dependence on critical minerals and Chinese manufacturing', 'intermittency requires storage and grid investment'], 'Renewables improve security overall but create new risks that require diversified supply chains and storage.'),
            ('Geopolitics is the main threat to energy security.', ['2022 Russian gas cuts, Hormuz tensions, 1973 oil embargo', 'chokepoints and pipeline politics'], ['extreme weather (Texas 2021 freeze), underinvestment and demand growth', 'energy poverty reflects low incomes and infrastructure'], 'Geopolitics causes the most dramatic shocks, but physical and economic factors also threaten security.')],
  extended=[('Examine the factors that influence a country\'s energy security.', 'Award: energy mix, import dependence, geopolitics, chokepoints, technology, price; named countries (Germany, Japan, France, China); judgement.', 10, 'long')],
  res=[('Table: EU natural gas imports by supplier (% share) - 2021: Russia 40, Norway 23, USA (LNG) 6, Algeria 11, others 20; 2023: Russia 15, Norway 30, USA (LNG) 19, Algeria 12, others 24.',
        [('Describe the change in the EU\'s gas suppliers between 2021 and 2023.', 'Russia\'s share fell from 40% to 15%; Norway (23 → 30%) and US LNG (6 → 19%) replaced much of it; supply became more diversified.'),
         ('Explain how the change affects EU energy security.', 'Less dependence on a hostile supplier reduces political risk, but LNG is more expensive and exposed to global market competition.')]),
       ('Text: "Japan imports about 88% of its primary energy. After the 2011 Fukushima disaster, the share of nuclear in electricity fell from about 25% to almost zero, and LNG imports rose by about a quarter."',
        [('Explain why Japan is described as energy insecure.', 'It has very few domestic fossil resources and imports nearly 90% of its energy, mostly by sea, so is vulnerable to price and supply shocks.'),
         ('Suggest one consequence of the fall in nuclear output.', 'Higher fuel import bills and trade deficits, higher electricity prices and higher CO₂ emissions from gas and coal plants.')])])

S('ch09-st1', gens=['pct_resource', 'footprint'],
  terms=[('resource stewardship', 'the careful and responsible management of resources to ensure they are available for future generations'),
         ('circular economy', 'an economic system that designs out waste, keeps products and materials in use and regenerates natural systems, in contrast to "take-make-dispose"'),
         ('linear economy', 'the "take-make-dispose" model in which raw materials are extracted, made into products and discarded'),
         ('recycling', 'processing used materials into new products, reducing the need for raw materials'),
         ('sustainable consumption', 'using goods and services in ways that meet needs while minimising the use of resources, waste and emissions')],
  facts=[('Which Japanese town aims for zero waste by sorting rubbish into about 45 categories?', 'Kamikatsu', ['Kyoto', 'Osaka', 'Sapporo'], 'Kamikatsu recycles or composts about 80% of its waste.'),
         ('Which organisation is best known for promoting the circular economy concept?', 'The Ellen MacArthur Foundation', ['OPEC', 'The World Bank', 'NATO'], 'Founded in 2010, it publishes circular economy frameworks used by firms and governments.'),
         ('Which African country banned plastic bags in 2008?', 'Rwanda', ['Nigeria', 'Egypt', 'South Africa'], 'Rwanda later banned most single-use plastics (2019).'),
         ('Which city adopted Kate Raworth\'s "doughnut" model as a basis for policy in 2020?', 'Amsterdam', ['Paris', 'New York', 'Beijing'], 'The model sets a social foundation and an ecological ceiling.')],
  why=[('Explain why a circular economy can increase resource security.', 'Keeping materials in use through reuse, repair, remanufacturing and recycling reduces demand for virgin resources and imports, cuts waste and emissions, and protects supply of critical materials.'),
       ('Explain why recycling rates vary between countries.', 'They depend on infrastructure (collection, sorting, processing), policy (landfill taxes, deposit schemes, extended producer responsibility), markets for recycled materials and public attitudes - Germany recycles about two-thirds of municipal waste, many low-income countries very little.'),
       ('Explain why reducing consumption is considered more effective than recycling.', 'Reduction avoids resource use and waste altogether, whereas recycling still uses energy and degrades material quality; the waste hierarchy places reduce and reuse above recycle.'),
       ('Explain how extended producer responsibility encourages stewardship.', 'Producers are made responsible for collecting and recycling their products, so they design goods to be durable, repairable and recyclable.')],
  contrast=[('a linear economy', 'a circular economy', 'A linear economy follows take-make-dispose; a circular economy keeps materials in loops through reuse, repair and recycling, designing out waste.'),
            ('recycling', 'reuse', 'Reuse keeps a product in its original form (refillable bottles, second-hand clothes); recycling breaks it down into material to make new products, which uses more energy.')],
  misc=[('Recycling alone can make consumption sustainable.', 'Recycling recovers only part of material flows and uses energy; reducing demand and redesigning products are also required.'),
        ('Circular economy policies are only relevant to rich countries.', 'Repair, reuse and informal recycling are widespread in low-income countries (e.g. Dharavi in Mumbai), and circular models can create jobs.'),
        ('Banning plastic bags solves the plastic pollution problem.', 'Bags are a small share of plastic waste; bans must be combined with wider reductions, deposit schemes and better waste management.')],
  apply=[('Using a named example, outline how one place has promoted resource stewardship.', 'e.g. Kamikatsu, Japan: zero-waste declaration (2003), 45 sorting categories and a reuse shop, achieving about 80% recycling and composting.', 3),
         ('Suggest two ways that a school could apply the circular economy.', 'A uniform and textbook reuse scheme; composting canteen waste; buying refillable and repairable equipment; recycling e-waste.', 2)],
  cases=[('Kamikatsu, Japan', 'the town sorts waste into about 45 categories and recycles or composts about 80% of it', 'local-scale resource stewardship', 'community commitment can transform waste management'),
         ('the EU Circular Economy Action Plan (2020)', 'targets include 65% recycling of municipal waste by 2035 and a "right to repair"', 'regional-scale stewardship policy', 'legislation sets targets and responsibilities that change producer and consumer behaviour'),
         ('informal recycling in Dharavi, Mumbai', 'thousands of small units recycle plastics, metals and paper, employing many thousands of people', 'the informal circular economy', 'informal workers recover materials efficiently but face health and safety risks'),
         ('Rwanda\'s plastics ban', 'plastic bags were banned in 2008 and Kigali became known as one of Africa\'s cleanest cities', 'regulation as a stewardship strategy', 'strong enforcement can change consumption and reduce waste')],
  evaluate=[('The circular economy is the most effective strategy for resource stewardship.', ['reduces virgin extraction, waste and emissions', 'creates jobs in repair and remanufacturing'], ['global material use is still about 90% linear (Circularity Gap Report: about 7% circular)', 'reducing consumption and population pressure may matter more'], 'The circular economy is powerful but must be combined with reducing overall consumption.'),
            ('Individual consumer choices are less important than government regulation in achieving sustainable consumption.', ['regulation changes whole markets (EU directives, Rwanda\'s ban)', 'individual choices are limited by price and availability'], ['consumer demand drives markets for sustainable products', 'collective individual action (diet change) has large impact'], 'Regulation is more powerful and equitable, but it often depends on public support created by consumer movements.')],
  extended=[('Examine the strategies used to promote resource stewardship at different scales.', 'Award: local (Kamikatsu), national (Rwanda, Germany), regional (EU), global (SDG 12); circular economy, recycling, reduction; effectiveness; judgement.', 10, 'long')],
  res=[('Table: municipal waste recycling and composting rates (%, recent year) - Germany 68; South Korea 59; UK 44; USA 32; Turkey 12; Chile 1.',
        [('Describe the variation shown.', 'Germany and South Korea recycle or compost over half; the UK and USA about a third to a half; Turkey and Chile very little.'),
         ('Suggest two reasons why Germany\'s rate is so high.', 'Landfill restrictions, a deposit return scheme (Pfand), extended producer responsibility (Green Dot) and well-established sorting by households.')]),
       ('Infographic description: The Circularity Gap Report 2023 - 100 billion tonnes of materials enter the global economy each year; only 7.2% are cycled back; 70% of greenhouse-gas emissions are linked to material handling and use.',
        [('Calculate the mass of materials cycled back each year.', '7.2% × 100 billion t = 7.2 billion tonnes'),
         ('Explain what the infographic suggests about the global economy.', 'It remains overwhelmingly linear; increasing circularity could reduce extraction and emissions significantly.')])])

S('ch09-st2', gens=['pct_resource', 'water_stress', 'energy_mix'],
  terms=[('Sustainable Development Goals (SDGs)', 'the 17 global goals with 169 targets adopted by all UN member states in 2015, to be achieved by 2030'),
         ('Millennium Development Goals (MDGs)', 'the eight international development goals for 2000-2015, such as halving extreme poverty'),
         ('sustainable development', 'development that meets the needs of the present without compromising the ability of future generations to meet their own needs (Brundtland Report, 1987)'),
         ('payments for ecosystem services', 'schemes that pay landowners to manage land to provide services such as forest carbon storage or clean water, e.g. Costa Rica\'s PSA programme'),
         ('community-based natural resource management', 'management of local resources such as forests, water or wildlife by the communities that depend on them')],
  facts=[('How many Sustainable Development Goals are there?', '17', ['8', '12', '169'], 'There are 17 goals and 169 targets for 2030.'),
         ('Which SDG focuses on "clean water and sanitation"?', 'SDG 6', ['SDG 2', 'SDG 7', 'SDG 13'], 'SDG 2 is zero hunger, SDG 7 affordable and clean energy, SDG 13 climate action.'),
         ('According to the UN Sustainable Development Goals Report 2024, approximately what share of SDG targets were on track?', 'About 17%', ['About 50%', 'About 80%', 'All of them'], 'Nearly half showed minimal or moderate progress and over a third had stalled or regressed.'),
         ('Which country\'s Payment for Environmental Services programme (from 1997) helped forest cover recover from about 21% in the 1980s to over 50%?', 'Costa Rica', ['Brazil', 'Indonesia', 'Kenya'], 'It is funded partly by a fuel tax.')],
  why=[('Explain why the SDGs are broader than the MDGs.', 'The MDGs focused mainly on poverty, health and education in developing countries; the SDGs apply to all countries and add environmental goals (climate, oceans, consumption), inequality, cities and governance.'),
       ('Explain why progress towards the SDGs has been uneven.', 'Countries differ in income, governance and conflict; shocks such as COVID-19, war in Ukraine and climate disasters reversed gains; funding gaps are large (trillions of dollars a year).'),
       ('Explain why resource management is often more successful at the local scale.', 'Local users have knowledge and a direct stake, rules can be adapted to conditions and monitored by the community, as in Nepal\'s community forests; global agreements are harder to enforce.'),
       ('Explain how SDG 7 is linked to other goals.', 'Affordable clean energy supports health (clean cooking), education (lighting), economic growth, water supply (pumping) and climate action (SDG 13).')],
  contrast=[('the MDGs', 'the SDGs', 'The MDGs (8 goals, 2000-2015) targeted developing countries and social needs; the SDGs (17 goals, 2015-2030) are universal and integrate economic, social and environmental sustainability.'),
            ('top-down resource management', 'bottom-up resource management', 'Top-down management is directed by governments or international bodies; bottom-up management is led by local communities and users.')],
  misc=[('The SDGs apply only to developing countries.', 'The SDGs are universal: high-income countries must also act, e.g. on consumption (SDG 12) and climate (SDG 13).'),
        ('The SDGs are legally binding treaties.', 'They are a non-binding political commitment; countries report progress voluntarily.'),
        ('Global goals are the only effective scale for resource management.', 'National and local actions (Costa Rica PES, Nepal community forests) often deliver results more directly.')],
  apply=[('Using a named example, outline how a resource management scheme contributes to the SDGs.', 'e.g. Nepal\'s community forestry: about 22,000 user groups manage around a third of the forest, increasing forest cover and supporting livelihoods (SDGs 1, 13, 15).', 3),
         ('Suggest two reasons why SDG 6 (water and sanitation) is off track.', 'Rapid urban growth outpaces infrastructure investment; funding shortfalls and weak governance; climate change and pollution reduce supply.', 2)],
  cases=[('Costa Rica\'s Payment for Environmental Services programme', 'landowners have been paid to conserve or restore forest since 1997, and forest cover rose to over 50%', 'national-scale resource stewardship', 'economic incentives can reverse deforestation'),
         ('community forestry in Nepal', 'about 22,000 community forest user groups manage roughly a third of Nepal\'s forests', 'local-scale resource management', 'giving communities rights and responsibilities improved forest condition and livelihoods'),
         ('the SDG Report 2024', 'only about 17% of targets were on track and over a third had stalled or reversed', 'the challenges of global goals', 'global goals depend on funding, stability and political commitment that have been disrupted')],
  evaluate=[('The Sustainable Development Goals are too ambitious to be achieved.', ['only about 17% of targets on track in 2024', 'financing gap of trillions per year; shocks reversed progress'], ['the MDGs achieved major gains (halving extreme poverty early)', 'goals drive policy, data and funding even if not fully met'], 'The SDGs will not all be met by 2030, but they are valuable as a framework that directs action.'),
            ('Resource management is most effective at the local scale.', ['local knowledge and ownership (Nepal forests)', 'easier monitoring and enforcement'], ['global commons (climate, oceans) need international agreements', 'national policies (Costa Rica PES) provide funding and laws'], 'Different scales are needed together; local management works best within supportive national and global frameworks.')],
  extended=[('Examine the role of the Sustainable Development Goals in promoting resource stewardship.', 'Award: SDGs 2, 6, 7, 12, 13; examples at different scales; progress data; limitations; judgement.', 10, 'long')],
  res=[('Table: progress towards SDG targets (UN SDG Report 2024, % of assessable targets) - on track 17; moderate progress 18; marginal progress 30; stagnated 18; regressed 17.',
        [('Calculate the percentage of targets that had stagnated or regressed.', '18 + 17 = 35%'),
         ('Suggest two reasons why so few targets are on track.', 'COVID-19 reversed gains in poverty and education; conflict and food/energy price shocks; climate disasters; insufficient finance.')]),
       ('Graph description: Costa Rica forest cover (% of land area) - 1940: 75; 1987: 21; 2000: 47; 2021: 57.',
        [('Calculate the percentage-point change in forest cover from 1987 to 2021.', '57 − 21 = +36 percentage points'),
         ('Explain how policy contributed to the change after 1987.', 'A 1996 Forest Law banned conversion of forest; Payments for Environmental Services (1997) rewarded conservation and reforestation; ecotourism created income from standing forest.')])])

S('ch09-st3', gens=['footprint', 'nir', 'pct_resource'],
  terms=[('cornucopian', 'a view that human ingenuity and technology will overcome resource limits, as argued by Julian Simon'),
         ('doughnut economics', 'Kate Raworth\'s model of a safe and just space between a social foundation of human needs and an ecological ceiling of planetary boundaries'),
         ('planetary boundaries', 'nine Earth-system limits (e.g. climate change, biodiversity loss, nitrogen cycle) within which humanity can operate safely (Rockström et al., 2009)'),
         ('degrowth', 'the idea that high-income countries should reduce production and consumption to stay within ecological limits while improving well-being'),
         ('ecomodernism', 'the view that technology (nuclear power, intensive agriculture, urbanisation) can decouple human well-being from environmental impact')],
  facts=[('How many of the nine planetary boundaries were assessed as transgressed in the 2023 update?', 'Six', ['One', 'Three', 'All nine'], 'Richardson et al. (2023) found six boundaries crossed, including climate, biosphere integrity and novel entities.'),
         ('Who wrote The Population Bomb (1968)?', 'Paul Ehrlich', ['Julian Simon', 'Thomas Malthus', 'Ester Boserup'], 'It predicted mass famine in the 1970s-80s.'),
         ('The UN (2024) projects that the world population will peak at about what level in the mid-2080s?', 'About 10.3 billion', ['About 8.5 billion', 'About 15 billion', 'About 20 billion'], 'World Population Prospects 2024 projects a peak around 10.3 billion.')],
  why=[('Explain why neo-Malthusians are concerned about future resource availability.', 'Population will rise to about 10 billion and consumption per person is rising; planetary boundaries are already exceeded, soils are degrading and climate change threatens food and water, suggesting limits may be reached.'),
       ('Explain why cornucopians are optimistic about future resources.', 'Rising prices stimulate substitution, efficiency and new technology (e.g. shale, renewables, precision agriculture); history shows famines have declined and resources have become cheaper (Simon-Ehrlich wager).'),
       ('Explain how the doughnut model combines social and environmental goals.', 'It defines a social foundation (food, water, health, education, income) below which people are deprived and an ecological ceiling (planetary boundaries) above which the environment is degraded; the aim is to live between them.'),
       ('Explain why falling fertility changes debates about population and resources.', 'With global TFR about 2.3 and falling, population will peak this century, so future resource pressure depends more on consumption and technology than on population growth.')],
  contrast=[('neo-Malthusian views', 'cornucopian views', 'Neo-Malthusians argue population and consumption growth will exceed environmental limits; cornucopians argue technology, markets and innovation will expand resources.'),
            ('degrowth', 'green growth', 'Degrowth calls for reduced material production and consumption in rich countries; green growth argues economies can keep growing while decoupling from emissions and resource use through technology.')],
  misc=[('Population growth is the only factor that will determine future resource use.', 'Consumption per person, technology, trade and governance matter as much or more; the richest 10% cause about half of consumption emissions.'),
        ('Cornucopians deny that resources are finite.', 'They accept finite stocks but argue that useful resources depend on technology, so effective supply can expand.'),
        ('Planetary boundaries are fixed thresholds that cause immediate collapse when crossed.', 'They mark zones of increasing risk based on uncertain science; crossing them raises the likelihood of abrupt, irreversible change.')],
  apply=[('Using examples, outline one argument supporting and one challenging a neo-Malthusian view of the future.', 'Supporting: six planetary boundaries crossed and Earth Overshoot Day on 1 August. Challenging: cereal yields have tripled since 1960 and global fertility is falling, so population will peak at about 10.3 billion.', 4),
         ('Suggest how Amsterdam is applying doughnut economics.', 'Its 2020 Circular Strategy aims to halve use of new raw materials by 2030, promotes circular construction and second-hand goods, and links this to social goals such as affordable housing.', 2)],
  cases=[('the Simon-Ehrlich wager', 'between 1980 and 1990 the prices of chromium, copper, nickel, tin and tungsten fell, and Ehrlich paid Simon', 'contrasting perspectives on resource futures', 'the outcome supported the cornucopian argument that innovation offsets scarcity, though over other periods prices rose'),
         ('the Limits to Growth (1972)', 'the "standard run" model projected overshoot and decline in the 21st century, and later studies found data broadly tracking it', 'the neo-Malthusian perspective', 'modelling raised concern that exponential growth in a finite system leads to collapse'),
         ('Amsterdam\'s doughnut strategy (2020)', 'the city adopted the doughnut model and aims for a fully circular economy by 2050', 'alternative economic perspectives on resource futures', 'policy can aim at well-being within ecological limits rather than growth alone')],
  evaluate=[('Technology will ensure that future resource needs are met.', ['Green Revolution, renewables, desalination have expanded supply', 'prices of many resources fell over the 20th century'], ['planetary boundaries are already crossed; rebound effects offset efficiency', 'technology is unevenly accessible to poor countries'], 'Technology can meet needs only if combined with lower consumption by the rich and fair access.'),
            ('Future resource security depends more on consumption patterns than on population size.', ['richest 10% produce about half of emissions; population growth is slowing', 'diet change could reduce farmland needs substantially'], ['an extra 2 billion people will raise demand for food and energy, mainly in Africa', 'population momentum is hard to change quickly'], 'Consumption is the bigger lever in the short term, though population growth matters in fast-growing regions.')],
  extended=[('Examine contrasting perspectives on the relationship between population, resources and the future.', 'Award: Malthus, Boserup, neo-Malthusian, cornucopian, doughnut/degrowth; evidence; scale and time; judgement.', 10, 'long')],
  res=[('Table: world population projections (UN WPP 2024, billions) - 2024: 8.2; 2050: 9.7; 2084 (peak): 10.3; 2100: 10.2.',
        [('Calculate the percentage increase from 2024 to the projected peak.', f'(10.3 − 8.2)/8.2 × 100 = {pc(8.2, 10.3)}'),
         ('Suggest what the projection implies for debates about resource futures.', 'Growth is slowing and will end this century, so long-term resource pressure depends more on consumption and technology than on endless population growth.')]),
       ('Diagram description: the doughnut model - inner ring "social foundation" with 12 dimensions (food, water, health, education, income, housing, energy, gender equality etc.); outer ring "ecological ceiling" with 9 planetary boundaries; the green ring between is the "safe and just space for humanity".',
        [('Describe the two boundaries shown in the model.', 'The inner boundary is the minimum social conditions everyone needs; the outer boundary is the environmental limit humanity should not exceed.'),
         ('Explain why most countries fail to reach the "safe and just space".', 'Rich countries overshoot ecological limits while poorer countries fall short of the social foundation; no country currently meets basic needs for all within planetary boundaries (O\'Neill et al., 2018).')])])


# =============================================================================================
# Option A Freshwater
# =============================================================================================
S('ch10-st1', gens=['hydrograph', 'pct_water', 'stats_phys'],
  terms=[('drainage basin', 'an area of land drained by a river and its tributaries, separated from neighbouring basins by a watershed'),
         ('watershed', 'the boundary of a drainage basin, usually a ridge of high land'),
         ('infiltration', 'the downward movement of water from the surface into the soil'),
         ('percolation', 'the downward movement of water from the soil into the underlying rock to become groundwater'),
         ('throughflow', 'the lateral movement of water through the soil towards a river channel'),
         ('evapotranspiration', 'the combined loss of water from evaporation and transpiration by plants'),
         ('interception', 'the capture of precipitation by vegetation before it reaches the ground')],
  facts=[('Which of the following is an output from a drainage basin system?', 'Evapotranspiration', ['Infiltration', 'Interception', 'Throughflow'], 'Outputs are evaporation, transpiration and river discharge to the sea.'),
         ('The water balance equation is:', 'P = Q + E ± ΔS', ['Q = A × v', 'P = E − Q', 'Q = P × E'], 'Precipitation equals runoff plus evapotranspiration plus or minus changes in storage.'),
         ('Overland flow that occurs when rainfall intensity exceeds infiltration capacity is called:', 'Hortonian (infiltration-excess) overland flow', ['saturation-excess overland flow', 'baseflow', 'stemflow'], 'Named after Robert Horton; common on compacted or urban surfaces.'),
         ('Which store holds most of the Earth\'s liquid freshwater?', 'Groundwater', ['Rivers', 'Lakes', 'The atmosphere'], 'About 30% of freshwater is groundwater; about 69% is in ice; rivers hold a tiny fraction.')],
  why=[('Explain why the drainage basin is described as an open system.', 'It receives inputs of energy (solar) and matter (precipitation) from outside and loses outputs (evapotranspiration, river discharge to the sea), with stores and flows inside the system.'),
       ('Explain how vegetation affects the drainage basin hydrological cycle.', 'Interception stores water on leaves and increases evaporation; roots increase infiltration; transpiration returns water to the atmosphere; leaf litter slows overland flow - so forested basins have lower and slower runoff.'),
       ('Explain why infiltration rates vary within a drainage basin.', 'They depend on soil texture (sand high, clay low), antecedent moisture, vegetation cover, slope angle, land use (compaction, impermeable surfaces) and rainfall intensity.'),
       ('Explain how urbanisation changes drainage basin flows.', 'Impermeable surfaces reduce infiltration and storage, increasing overland flow; drains speed water to channels; less evapotranspiration; so runoff is greater and faster.')],
  contrast=[('infiltration', 'percolation', 'Infiltration is the movement of water from the surface into the soil; percolation is the deeper movement from the soil into permeable rock to become groundwater.'),
            ('throughflow', 'overland flow', 'Throughflow is the slow lateral movement of water within the soil; overland flow is the rapid movement of water across the ground surface when the soil cannot absorb more.')],
  misc=[('All precipitation that falls in a drainage basin reaches the river.', 'Much is lost to evapotranspiration or held in stores such as soil, groundwater and lakes; only part becomes runoff.'),
        ('Infiltration and percolation are the same process.', 'Infiltration is water entering the soil; percolation is deeper movement into rock.'),
        ('Groundwater flow is the fastest route for water to reach a river.', 'Groundwater flow is the slowest route (days to years); overland flow is fastest.')],
  apply=[('A basin receives 900 mm of precipitation a year; evapotranspiration is 450 mm and there is no change in storage. Calculate the annual runoff and explain the result.', 'Q = P − E = 900 − 450 = 450 mm; half of the precipitation leaves as river discharge, typical of a temperate humid basin.', 2),
         ('Suggest how deforestation in the Amazon basin could affect drainage basin flows.', 'Less interception and transpiration, more overland flow and soil erosion, higher and faster peak discharges, and reduced regional rainfall recycling.', 3)],
  cases=[('the Amazon basin', 'up to a third of rainfall is recycled through transpiration, and the basin discharges about 209,000 m³/s on average', 'the role of vegetation in the drainage basin system', 'forest transpiration and interception strongly control the basin\'s water balance'),
         ('the River Severn catchment, UK', 'it drains about 11,400 km² of upland Wales and lowland England, with flashy upland tributaries and slower lowland reaches', 'variation in drainage basin flows', 'rock type, relief and land use alter the relative importance of overland flow and throughflow'),
         ('the Plynlimon catchment experiment, Wales', 'experiments showed forested catchments lost more water to interception and evaporation than grassland catchments', 'the influence of land use on water balance', 'conifer forests reduce runoff compared with grassland')],
  evaluate=[('Human activity now has a greater influence on drainage basin systems than physical factors.', ['urbanisation, deforestation and dams alter flows (Amazon, Yangtze)', 'irrigation and abstraction remove large volumes'], ['climate, geology and relief remain the basic controls', 'many remote basins are little modified'], 'Human activity dominates in heavily used basins, but physical factors still set the framework.'),
            ('Vegetation is the most important factor controlling drainage basin flows.', ['interception and transpiration reduce runoff', 'roots increase infiltration'], ['rock permeability and soil determine infiltration and groundwater', 'rainfall intensity and antecedent moisture control flood response'], 'Vegetation is important, but geology and precipitation characteristics are often more important.')],
  extended=[('Explain the stores and flows of the drainage basin system and how they are affected by human activity.', 'Award: inputs, stores, flows and outputs; water balance; effects of urbanisation, deforestation, farming and dams; named examples.', 10, 'long')],
  res=[('Table: annual water balance for a basin in Scotland (mm) - precipitation 1,600; evapotranspiration 400; runoff 1,150.',
        [('Calculate the change in storage over the year.', 'ΔS = P − Q − E = 1,600 − 1,150 − 400 = +50 mm (storage increased).'),
         ('Calculate runoff as a percentage of precipitation and comment.', f'1,150/1,600 × 100 = {1150 / 1600 * 100:.1f}%; a high runoff ratio typical of a wet, upland basin with thin soils and impermeable rock.')]),
       ('Systems diagram description: precipitation → interception storage → throughfall/stemflow → surface storage → infiltration → soil water → percolation → groundwater; flows out via overland flow, throughflow and groundwater flow to channel; outputs: evaporation, transpiration, channel discharge.',
        [('Identify two stores and two flows shown.', 'Stores: interception, surface, soil water, groundwater, channel. Flows: throughfall, stemflow, infiltration, percolation, throughflow, overland flow, groundwater flow.'),
         ('Explain what happens to flows when the soil becomes saturated.', 'Infiltration falls to zero, so additional rain becomes saturation-excess overland flow, raising and speeding river discharge.')])])

S('ch10-st2', gens=['hydrograph', 'discharge', 'recurrence', 'spearman_phys'],
  terms=[('discharge', 'the volume of water passing a point in a river channel per unit of time, measured in cumecs (m³/s); cross-sectional area × velocity'),
         ('storm hydrograph', 'a graph showing how river discharge changes over time in response to a period of rainfall'),
         ('lag time', 'the time between peak rainfall and peak discharge'),
         ('baseflow', 'the part of river discharge supplied by groundwater flow and slow throughflow, which sustains the river between storms'),
         ('rising limb', 'the part of a hydrograph showing the increase in discharge after rainfall begins'),
         ('drainage density', 'the total length of river channels in a basin divided by its area (km/km²)')],
  facts=[('Which basin characteristic tends to produce the shortest lag time?', 'Small, steep basin with impermeable rock and high drainage density', ['Large basin with permeable chalk', 'Forested basin with deep soils', 'Gentle slopes with sandy soils'], 'Water reaches the channel quickly by overland flow.'),
         ('A river is 8 m wide, with a mean depth of 0.5 m and a velocity of 1.2 m/s. Its discharge is:', '4.8 m³/s', ['9.6 m³/s', '2.4 m³/s', '0.6 m³/s'], 'Q = 8 × 0.5 × 1.2 = 4.8 m³/s.'),
         ('In August 2004, Boscastle in Cornwall flooded after about how much rain fell in about five hours?', 'About 200 mm', ['About 20 mm', 'About 2 mm', 'About 2,000 mm'], 'The small, steep Valency catchment produced a flash flood; around 100 people were rescued by helicopter.')],
  why=[('Explain why urban catchments have "flashy" storm hydrographs.', 'Impermeable surfaces and storm drains reduce infiltration and speed runoff to channels, so lag time is short, the rising limb is steep and the peak discharge high.'),
       ('Explain how antecedent moisture affects the shape of a storm hydrograph.', 'If soil is already saturated from earlier rain, infiltration is low, so more rain becomes overland flow, giving a shorter lag time and higher peak.'),
       ('Explain why basins on permeable rock have high baseflow and subdued hydrographs.', 'Rain infiltrates and percolates into the rock (e.g. chalk), recharging groundwater that is released slowly, so storm peaks are low and lagged and flow is maintained in dry periods.'),
       ('Explain how basin shape influences flood response.', 'In a circular basin tributaries reach the main channel at similar times, giving a high, early peak; in an elongated basin water arrives over a longer period, giving a lower, later peak.')],
  contrast=[('a flashy hydrograph', 'a subdued hydrograph', 'A flashy hydrograph has a short lag time, steep rising limb and high peak (urban, steep, impermeable basins); a subdued hydrograph has a long lag, gentle limbs and lower peak (forested, permeable, gentle basins).'),
            ('baseflow', 'storm flow', 'Baseflow is the steady contribution from groundwater; storm flow (quickflow) is the extra discharge from overland flow and rapid throughflow after rainfall.')],
  misc=[('Lag time is measured from the start of rainfall to the peak discharge.', 'Lag time is measured from peak rainfall to peak discharge.'),
        ('Bigger basins always have higher flood peaks than small basins.', 'Large basins have higher total discharge, but small steep basins can have more extreme, flashier responses (e.g. Boscastle).'),
        ('Discharge depends only on the amount of rainfall.', 'Intensity, duration, antecedent moisture, basin characteristics and land use all affect discharge.')],
  apply=[('Describe and explain the hydrograph you would expect for a small, steep, deforested catchment after an intense storm.', 'Short lag time, steep rising limb, high peak and rapid return to baseflow - because thin soils and lack of interception lead to rapid overland flow.', 3),
         ('Suggest two ways that afforestation could change a river\'s storm hydrograph.', 'Increased interception and infiltration lengthen lag time and lower peak discharge; more transpiration reduces total runoff.', 2)],
  cases=[('the Boscastle flood (2004)', 'about 200 mm of rain in roughly five hours on the steep, small Valency catchment produced a flash flood that destroyed cars and buildings', 'factors influencing the storm hydrograph', 'intense rainfall on a small, steep basin with saturated soils produced a very short lag time'),
         ('the chalk River Itchen, Hampshire', 'about 90% of its flow is baseflow from the chalk aquifer and it rarely floods rapidly', 'the influence of geology on discharge', 'permeable rock stores water and releases it slowly, subduing the hydrograph'),
         ('flash flooding in Kuala Lumpur', 'rapid urbanisation has increased flash flooding, leading to the SMART tunnel (2007) for stormwater', 'the effect of urbanisation on discharge', 'impermeable surfaces shortened lag times and increased peaks')],
  evaluate=[('Human factors are now more important than physical factors in shaping storm hydrographs.', ['urbanisation and deforestation shorten lag times and raise peaks', 'channel engineering speeds flow'], ['rainfall intensity, geology, slope and basin shape determine response', 'extreme storms overwhelm human influences (Boscastle)'], 'Physical factors still dominate for extreme events, but human factors are decisive in urban and modified catchments.'),
            ('Lag time is the most useful characteristic of a storm hydrograph for flood management.', ['it shows how long people have to prepare and warn', 'easy to measure and compare'], ['peak discharge determines whether the channel overflows', 'flood volume and duration matter for damage'], 'Lag time is valuable for warnings, but peak discharge and volume are equally important for flood risk.')],
  extended=[('Explain how physical and human factors influence the shape of a storm hydrograph.', 'Award: hydrograph components; physical factors (rainfall, antecedent moisture, size, shape, slope, geology, soils, drainage density, vegetation); human factors (urbanisation, deforestation, farming, channels); examples.', 10, 'long')],
  res=[('Hydrograph data: rainfall peaked at 10:00 (25 mm/h); discharge rose from a baseflow of 4 m³/s at 09:00 to a peak of 38 m³/s at 16:00, returning to 6 m³/s by 08:00 the next day.',
        [('Calculate the lag time and the peak storm flow above baseflow.', 'Lag time = 16:00 − 10:00 = 6 hours; 38 − 4 = 34 m³/s above baseflow.'),
         ('Suggest why discharge did not return fully to its original baseflow.', 'Groundwater and throughflow recharged by the storm continue to feed the channel, raising baseflow for a time.')]),
       ('Table: lag times for two catchments after the same storm - Catchment A (urban, 65% impermeable): 2.5 h, peak 28 m³/s; Catchment B (forested, 5% impermeable): 11 h, peak 9 m³/s.',
        [('How many times higher is the peak in A than in B?', f'28 / 9 = {28 / 9:.1f} times'),
         ('Explain the differences shown.', 'Impermeable surfaces and drains in A cause rapid overland flow; in B interception, infiltration and throughflow delay and reduce runoff.')])])

S('ch10-st3', gens=['gradient', 'stats_phys', 'spearman_phys', 'discharge'],
  terms=[('hydraulic action', 'erosion caused by the force of moving water, which compresses air in cracks in the bed and banks and dislodges material'),
         ('abrasion', 'erosion caused when the river\'s load scrapes and wears away the bed and banks (also called corrasion)'),
         ('attrition', 'the wearing down of load particles as they collide with each other, making them smaller and more rounded'),
         ('saltation', 'the bouncing movement of medium-sized particles such as sand and small pebbles along the river bed'),
         ('meander', 'a sinuous bend in a river channel, with erosion on the outer bank and deposition on the inner bank'),
         ('levée', 'a raised natural embankment along a river, formed by deposition of coarser sediment when the river floods')],
  facts=[('According to the Hjulström curve, which particle size is eroded at the lowest velocity?', 'Sand (about 0.1-1 mm)', ['Clay', 'Boulders', 'Silt'], 'Clay and silt are cohesive and need higher velocities to be eroded.'),
         ('Where is the fastest current (thalweg) usually found in a meander?', 'Near the outer bank', ['Near the inner bank', 'In the exact centre', 'On the point bar'], 'Higher velocity on the outside causes erosion and a river cliff.'),
         ('Which landform is created when a meander neck is cut through during a flood?', 'An oxbow lake', ['A delta', 'A waterfall', 'A braided channel'], 'Deposition seals the abandoned loop.'),
         ('Niagara Falls has retreated upstream historically at roughly what rate?', 'About 1 m per year', ['About 1 mm per year', 'About 100 m per year', 'It does not retreat'], 'Retreat has slowed to about 0.3 m/yr because of water diversion for hydroelectricity.')],
  why=[('Explain the formation of a meander.', 'Riffles and pools develop; helicoidal flow concentrates the fastest flow towards the outer bank, causing erosion (river cliff), while slower flow on the inner bank deposits sediment (point bar); the bend migrates and becomes more sinuous.'),
       ('Explain the formation of a waterfall.', 'Where resistant rock overlies weaker rock, the weaker rock is eroded faster by hydraulic action and abrasion, creating an overhang and plunge pool; the overhang collapses and the waterfall retreats upstream, forming a gorge.'),
       ('Explain why levées form along lowland rivers.', 'When the river floods, velocity falls sharply at the channel edge, depositing coarser sediment close to the channel; repeated floods build raised banks, while finer silt is carried further across the floodplain.'),
       ('Explain why particle size usually decreases downstream.', 'Attrition and abrasion wear particles down during transport, and selective transport carries finer material further while coarse material is deposited upstream.')],
  contrast=[('suspension', 'traction', 'Suspension carries fine particles (clay, silt) within the water; traction rolls large boulders and cobbles along the bed.'),
            ('a river cliff', 'a point bar', 'A river cliff is a steep erosional bank on the outside of a meander; a point bar is a gentle depositional slope of sand and gravel on the inside.')],
  misc=[('Rivers erode most in their upper course because they flow fastest there.', 'Velocity often increases downstream as channel efficiency improves; upper courses erode vertically because of steep gradients and coarse load.'),
        ('Clay is easy to erode because its particles are very small.', 'Clay particles are cohesive, so higher velocities are needed to erode them than sand (Hjulström curve).'),
        ('Deltas form wherever a river reaches the sea.', 'Deltas form only where sediment supply exceeds removal by waves, tides and currents, e.g. the Nile and Mississippi but not the Amazon mouth.')],
  apply=[('Using the Hjulström curve, explain what happens to a 10 mm pebble when velocity falls from 150 cm/s to 50 cm/s.', 'At 150 cm/s the pebble can be eroded and transported; at 50 cm/s velocity is below the settling velocity for that size, so it is deposited.', 2),
         ('Suggest two field measurements that could test whether pebble size decreases downstream.', 'Long-axis length with callipers at each site; roundness using Powers\' index; repeated at sites at regular intervals with random sampling of 20-30 pebbles.', 2)],
  cases=[('the Nile delta', 'an arcuate delta built by sediment deposition, now shrinking because the Aswan High Dam (1970) traps about 98% of the sediment', 'the formation and change of depositional landforms', 'deposition built the delta, and reduced sediment supply now allows coastal erosion'),
         ('the retreat of Niagara Falls', 'resistant dolomite caprock overlies weaker shale, and the falls have retreated about 11 km over 12,000 years, forming the Niagara Gorge', 'the formation of waterfalls and gorges', 'differential erosion undercuts resistant rock, which collapses and retreats upstream'),
         ('the Mississippi River', 'it has meanders, oxbow lakes, levées and a bird\'s-foot delta', 'lowland fluvial landforms', 'deposition on a low gradient with high sediment load creates distinctive landforms'),
         ('the Rakaia River, New Zealand', 'a braided river crossing the Canterbury Plains with many channels separated by gravel bars', 'braiding', 'high loads of coarse sediment and variable discharge from glacial meltwater produce multiple channels')],
  evaluate=[('Deposition is more important than erosion in creating river landforms.', ['floodplains, levées, point bars, deltas are depositional', 'lowland rivers deposit most of their load'], ['waterfalls, gorges, V-shaped valleys and river cliffs are erosional', 'meanders depend on both erosion and deposition'], 'Both processes are important; many landforms, such as meanders, result from their interaction.'),
            ('The Hjulström curve fully explains how rivers erode, transport and deposit sediment.', ['shows thresholds of erosion and settling velocity for particle sizes', 'explains why sand is eroded at lowest velocities'], ['based on uniform sediments in laboratory flumes', 'ignores turbulence, channel shape and mixed sediment'], 'It is a useful model but simplifies real river conditions.')],
  extended=[('Explain the processes involved in the formation of two river landforms.', 'Award: named landforms (e.g. meander, oxbow lake, waterfall, levée, delta); processes of erosion, transport and deposition; sequence; located examples.', 10, 'long')],
  res=[('Table: mean pebble long axis (mm) at sites downstream - Site 1 (0 km): 112; Site 2 (2 km): 86; Site 3 (4 km): 61; Site 4 (6 km): 48; Site 5 (8 km): 32.',
        [('Calculate the percentage decrease in mean size from site 1 to site 5.', f'(32 − 112)/112 × 100 = {pc(112, 32)}'),
         ('Explain the pattern shown.', 'Particle size decreases downstream because of attrition and abrasion and the selective transport of finer material further.')]),
       ('Cross-section description: at a meander bend, depth is 0.2 m at the inner bank, 0.5 m mid-channel and 1.3 m at the outer bank; velocity is 0.3 m/s near the inner bank and 1.1 m/s near the outer bank.',
        [('Describe the asymmetry of the cross-section.', 'Shallow, gently sloping inner bank (point bar) and deep, steep outer bank (river cliff); depth increases from 0.2 to 1.3 m.'),
         ('Explain the asymmetry using the velocity data.', 'Faster flow (1.1 m/s) on the outer bank erodes it by hydraulic action and abrasion; slower flow (0.3 m/s) on the inner bank causes deposition.')])])

S('ch10-st4', gens=['recurrence', 'hydrograph', 'pct_water'],
  terms=[('flood', 'when a river overflows its banks, inundating land that is not normally covered by water'),
         ('hard engineering', 'built structures used to control rivers, such as dams, embankments, flood walls and channelisation'),
         ('soft engineering', 'approaches that work with natural processes, such as floodplain zoning, afforestation, wetland restoration and flood warnings'),
         ('floodplain zoning', 'restricting land uses in areas at risk of flooding, keeping high-value development out of the most hazardous zones'),
         ('channelisation', 'straightening, deepening or lining a river channel to increase its capacity and speed water away'),
         ('recurrence interval', 'the average time between floods of a given magnitude, calculated as (n + 1)/m from ranked records')],
  facts=[('What was the approximate cost of the 2011 floods in Thailand, which affected Bangkok and its industrial estates?', 'About US$45 billion', ['About US$450 million', 'About US$4.5 billion', 'About US$450 billion'], 'The World Bank estimated about US$46.5 billion of damage and losses; global electronics and car supply chains were disrupted.'),
         ('The Netherlands\' "Room for the River" programme is an example of:', 'soft engineering that gives rivers more space', ['building a single large dam', 'concrete channelisation', 'a coastal storm-surge barrier'], 'It lowered floodplains, relocated dykes and created bypass channels.'),
         ('The July 2021 floods in western Germany killed over 180 people mainly in which valley?', 'The Ahr valley', ['The Rhine Gorge', 'The Elbe valley', 'The Danube valley'], 'Extreme rainfall on saturated ground in steep valleys caused flash flooding.')],
  why=[('Explain why urbanisation increases flood risk.', 'Impermeable surfaces reduce infiltration and storm drains speed runoff, raising peak discharge; building on floodplains increases exposure of people and property.'),
       ('Explain why flood defences can increase flood damage in the long term.', 'They encourage development behind levées (the "levée effect"); when an extreme flood overtops or breaches them, damage is greater; channelisation can move flooding downstream.'),
       ('Explain how deforestation upstream can increase flooding downstream.', 'Reduced interception and infiltration increase overland flow; soil erosion adds sediment that reduces channel capacity, e.g. debated links between Himalayan deforestation and Ganges-Brahmaputra floods.'),
       ('Explain why soft engineering is increasingly preferred to hard engineering.', 'It is cheaper to maintain, works with natural processes, provides habitat and amenity, reduces downstream impacts and is more resilient to climate change.')],
  contrast=[('hard engineering', 'soft engineering', 'Hard engineering controls rivers with structures such as dams, levées and channelisation; soft engineering works with natural processes through zoning, afforestation, wetland restoration and warnings.'),
            ('flood prediction', 'flood prevention', 'Prediction forecasts when and where floods will occur so people can prepare; prevention attempts to stop floods happening by controlling discharge or channel capacity.')],
  misc=[('Flood defences make floodplains completely safe.', 'Defences are designed for a given recurrence interval (e.g. 1 in 100 years) and can be exceeded or fail, as New Orleans levees did in 2005.'),
        ('A 1-in-100-year flood happens only once every hundred years.', 'It has a 1% chance of occurring in any year; two can occur in consecutive years.'),
        ('Floods are entirely negative.', 'Floods deposit fertile silt, recharge groundwater and wetlands and support floodplain agriculture, e.g. in Bangladesh.')],
  apply=[('Using a named example, outline two consequences of a river flood.', 'e.g. 2011 Thailand floods: over 800 deaths and 13 million people affected; industrial estates north of Bangkok flooded, disrupting global hard-disk and car supply chains (about US$45 billion losses).', 4),
         ('Suggest two flood management strategies suitable for a low-income country.', 'Community early warning systems and evacuation plans; raised homes and flood shelters; mangrove/wetland protection; land-use zoning.', 2)],
  cases=[('the 1993 Mississippi flood', 'over 1,000 levées failed and damage reached about US$15-20 billion', 'the limitations of hard engineering', 'confining the river behind levées raised flood levels and failures caused widespread damage'),
         ('the Room for the River programme, Netherlands', 'over 30 projects on the Rhine branches (2006-2015) cost about €2.3 billion', 'soft flood management', 'giving the river space lowered flood levels while improving landscape and habitats'),
         ('the 2011 Thailand flood disaster', 'months-long flooding of the Chao Phraya basin affected 13 million people and global supply chains', 'the economic consequences of flooding', 'industrial estates on the floodplain spread losses through global production networks'),
         ('the Three Gorges Dam and Yangtze flood control', 'the dam provides 22 billion m³ of flood-storage capacity to protect the middle Yangtze', 'large-scale hard engineering for flood control', 'reservoir storage reduces peak discharges downstream, though very large floods still occur')],
  evaluate=[('Soft engineering is more effective than hard engineering in managing flood risk.', ['works with natural processes, lower maintenance, sustainable (Room for the River)', 'avoids the levée effect and downstream impacts'], ['dense cities need hard defences (Thames Barrier, Three Gorges)', 'soft measures need land and time'], 'A combination is most effective; soft engineering is preferable where land is available, hard engineering where high-value assets must be protected.'),
            ('Human activity is now the main cause of river flooding.', ['urbanisation, deforestation and channelisation increase peaks', 'floodplain development increases exposure'], ['extreme rainfall and snowmelt are the primary triggers (Ahr 2021, Pakistan 2022)', 'climate change intensifies rainfall - a human cause acting through physical processes'], 'Physical events trigger floods, but human actions increasingly determine their frequency and impacts.')],
  extended=[('Evaluate the effectiveness of different flood management strategies.', 'Award: hard and soft strategies with named examples (Mississippi levées, Room for the River, Three Gorges, warnings in Bangladesh); costs, benefits, sustainability; judgement.', 10, 'long')],
  res=[('Table: annual maximum discharge, ranked (m³/s) for 9 years - 1,850; 1,420; 1,260; 1,100; 980; 910; 860; 790; 720.',
        [('Calculate the recurrence interval of the largest flood.', 'RI = (n + 1)/m = (9 + 1)/1 = 10 years'),
         ('Calculate the annual probability of the third-ranked flood and explain one limitation of this method.', 'RI = 10/3 = 3.3 years, probability = 30%; a 9-year record is too short to estimate rare floods reliably.')]),
       ('Text: "Germany 2021 - In the Ahr valley about 100-150 mm of rain fell in 24-48 hours on already saturated soils; the river rose to about 7 m, far above the previous record of 3.7 m." - summary of reports by the German Weather Service.',
        [('Calculate the percentage by which the 2021 level exceeded the previous record.', f'(7 − 3.7)/3.7 × 100 = {pc(3.7, 7)}'),
         ('Suggest two physical factors that explain the extreme flood.', 'Saturated soils reduced infiltration; steep, narrow valley slopes concentrated runoff quickly; intense, slow-moving rainfall.')])])

S('ch11-st1', gens=['water_stress', 'pct_water', 'stats_hum'],
  terms=[('physical water scarcity', 'a situation where water resources are insufficient to meet all demands, typically in arid regions, with over 75% of river flows withdrawn'),
         ('economic water scarcity', 'a situation where water is available but human, institutional or financial capital limits access'),
         ('eutrophication', 'excessive enrichment of water by nutrients (nitrates, phosphates) from fertilisers and sewage, causing algal blooms and oxygen depletion'),
         ('water quality', 'the chemical, physical and biological characteristics of water that determine its suitability for drinking, farming, industry and ecosystems'),
         ('safely managed drinking water', 'drinking water from an improved source that is on premises, available when needed and free from contamination (SDG 6.1 indicator)')],
  facts=[('According to WHO/UNICEF (2022), approximately how many people lacked safely managed drinking water?', 'About 2.2 billion', ['About 220 million', 'About 22 million', 'About 5 billion'], 'About 3.5 billion lacked safely managed sanitation.'),
         ('Which naturally occurring contaminant in groundwater has affected tens of millions of people in Bangladesh?', 'Arsenic', ['Fluoride only', 'Mercury', 'Uranium'], 'Shallow tube wells drilled from the 1970s tapped arsenic-rich groundwater.'),
         ('In which US city did a switch of water source in 2014 lead to lead contamination of drinking water?', 'Flint, Michigan', ['Toledo, Ohio', 'Phoenix, Arizona', 'Miami, Florida'], 'Corrosive river water leached lead from old pipes.'),
         ('Which region is most affected by economic (rather than physical) water scarcity?', 'Much of sub-Saharan Africa', ['The Arabian Peninsula', 'Northern Europe', 'Antarctica'], 'IWMI mapping shows water is available but infrastructure is lacking.')],
  why=[('Explain why economic water scarcity is common in sub-Saharan Africa.', 'Rainfall and rivers are often sufficient, but lack of investment in dams, pipes, pumps and treatment, weak institutions and poverty prevent people accessing safe water; women and girls spend hours collecting it.'),
       ('Explain how agriculture can reduce water quality.', 'Fertiliser and manure runoff add nitrates and phosphates (eutrophication), pesticides contaminate water, soil erosion increases turbidity and over-irrigation causes salinisation of return flows.'),
       ('Explain why poor water quality reduces water availability.', 'Polluted water cannot be used for drinking or irrigation without costly treatment, so the effective supply is smaller - e.g. the polluted Yamuna in Delhi or the Ganges.'),
       ('Explain how eutrophication affects freshwater ecosystems.', 'Nutrient enrichment causes algal blooms that block light; when algae die, bacterial decomposition uses up dissolved oxygen, killing fish and creating dead zones; some algae produce toxins.')],
  contrast=[('physical water scarcity', 'economic water scarcity', 'Physical scarcity is a lack of water relative to demand (e.g. Jordan, Saudi Arabia); economic scarcity is lack of access despite adequate water because of poverty and missing infrastructure (e.g. Uganda, Niger).'),
            ('point-source pollution', 'diffuse (non-point) pollution', 'Point sources are single identifiable outlets such as a factory pipe or sewage works; diffuse pollution comes from many dispersed sources such as farm runoff and urban surfaces.')],
  misc=[('Countries with high rainfall cannot suffer from water scarcity.', 'They can suffer economic scarcity or pollution-related scarcity, e.g. Bangladesh\'s arsenic-contaminated groundwater.'),
        ('Water scarcity is only about quantity.', 'Quality is equally important: polluted water reduces usable supply and harms health.'),
        ('Eutrophication is caused only by industrial waste.', 'Most nutrient pollution comes from agricultural fertilisers, manure and sewage.')],
  apply=[('Using a named example, outline two consequences of poor water quality.', 'e.g. Lake Erie 2014: a toxic algal bloom (microcystin) left about 400,000 people in Toledo without drinking water for three days; fisheries and tourism were affected.', 4),
         ('Suggest two strategies that could reduce economic water scarcity in rural Africa.', 'Low-cost boreholes with hand pumps maintained by communities; rainwater harvesting tanks; community water committees and NGO-funded infrastructure (e.g. WaterAid).', 2)],
  cases=[('arsenic in Bangladesh\'s groundwater', 'millions of shallow tube wells drilled from the 1970s exposed tens of millions of people to arsenic levels above WHO guidelines', 'the role of water quality in water security', 'water that was abundant became unsafe, creating a public health crisis'),
         ('Lake Erie\'s 2014 algal bloom', 'phosphorus from farms in the Maumee basin fed a toxic bloom that cut off drinking water to about 400,000 people in Toledo', 'eutrophication', 'diffuse agricultural pollution reduced the usability of a major freshwater supply'),
         ('the Yamuna River in Delhi', 'the 22 km stretch through Delhi carries about 80% of the river\'s pollution load, with toxic foam visible', 'the effect of urban pollution on water scarcity', 'untreated sewage and industrial waste make water unusable'),
         ('rural Ethiopia', 'many households, mainly women and girls, walk long distances to collect water from unprotected sources', 'economic water scarcity', 'lack of infrastructure rather than lack of water limits access')],
  evaluate=[('Economic water scarcity is a more serious global problem than physical water scarcity.', ['affects far more people (sub-Saharan Africa, South Asia)', 'causes disease and lost education'], ['physical scarcity is harder to solve and worsening with climate change', 'affects food production in major breadbaskets'], 'Economic scarcity affects more people and is more solvable, so it is the more serious immediate problem.'),
            ('Water quality is now a greater threat to water security than water quantity.', ['pollution reduces usable supply (Yamuna, Lake Erie)', 'arsenic, nitrates and microplastics affect huge populations'], ['droughts and over-abstraction cause acute shortages (Cape Town)', 'climate change reduces quantity in many regions'], 'Both threaten security; quality issues are more widespread, while quantity crises are more acute.')],
  extended=[('Examine the causes of water scarcity in contrasting places.', 'Award: physical and economic scarcity explained; quality issues; named places (Jordan, Ethiopia, Bangladesh, Delhi); human and physical factors; judgement.', 10, 'long')],
  res=[('Table: access to safely managed drinking water (% of population, 2022) - Germany 99; Brazil 88; India 76; Nigeria 32; Ethiopia 13.',
        [('Describe the pattern shown by the data.', 'Access is nearly universal in Germany, high in Brazil, moderate in India and very low in Nigeria and Ethiopia.'),
         ('Explain why Ethiopia\'s figure is so low despite the Blue Nile rising there.', 'Economic scarcity: lack of piped networks and treatment, a large dispersed rural population and limited investment, not lack of water resources.')]),
       ('Water quality survey of a river near Kathmandu: dissolved oxygen 8.5 mg/L upstream, 1.8 mg/L downstream of the city; nitrate 1.2 mg/L upstream, 14.6 mg/L downstream.',
        [('Calculate the percentage change in dissolved oxygen and nitrate downstream.', f'Oxygen {pc(8.5, 1.8)}; nitrate {pc(1.2, 14.6)}'),
         ('Suggest causes and consequences of the change.', 'Untreated sewage and urban runoff add organic matter and nutrients; decomposition consumes oxygen, killing fish and making water unsafe.')])])

S('ch11-st2', gens=['pct_water', 'energy_mix'],
  terms=[('multipurpose scheme', 'a river management project, usually a large dam, that provides several functions such as hydroelectric power, irrigation, flood control, water supply and navigation'),
         ('hydroelectric power (HEP)', 'electricity generated by water flowing through turbines, usually from a reservoir behind a dam'),
         ('reservoir-induced seismicity', 'earthquakes triggered by the weight of water in a large reservoir and increased pore pressure in rocks'),
         ('sediment trapping', 'the accumulation of sediment behind a dam, which reduces reservoir capacity and starves downstream channels and deltas of sediment'),
         ('dam decommissioning', 'the removal of a dam to restore river processes and ecosystems, e.g. the Elwha River dams in Washington State')],
  facts=[('What is the installed generating capacity of the Three Gorges Dam?', 'About 22.5 GW', ['About 2.25 GW', 'About 225 GW', 'About 0.225 GW'], 'It is the world\'s largest power station by capacity.'),
         ('Approximately how many people were relocated for the Three Gorges Dam?', 'About 1.3 million', ['About 13,000', 'About 130,000', 'About 13 million'], 'Cities such as Fengjie were submerged and rebuilt upslope.'),
         ('Which social movement, led by Medha Patkar, opposed the Sardar Sarovar Dam on the Narmada River?', 'Narmada Bachao Andolan', ['Chipko', 'Green Belt Movement', 'La Vía Campesina'], 'It campaigned for the rights of displaced Adivasi (tribal) communities.'),
         ('Which disease increased around Lake Nasser and irrigation canals after the Aswan High Dam was built?', 'Schistosomiasis (bilharzia)', ['Malaria only', 'Cholera only', 'Ebola'], 'Perennial irrigation created habitats for the host snails.')],
  why=[('Explain why large dams are described as multipurpose schemes.', 'A single dam can generate HEP, store water for irrigation and urban supply, regulate floods and improve navigation (e.g. Three Gorges allows 10,000-tonne ships to reach Chongqing).'),
       ('Explain how a large dam can affect the river downstream.', 'Trapping of sediment causes clear-water erosion of the bed and banks and delta retreat; altered flow regimes reduce floodplain fertility and fisheries; water temperature and quality change.'),
       ('Explain why large dams are controversial.', 'Benefits (energy, irrigation, flood control) go mainly to cities and industry, while costs (displacement, loss of farmland and heritage, ecological damage) fall on rural and indigenous people; dams can also create transboundary tensions.'),
       ('Explain why some dams are being removed.', 'Old dams may be unsafe or uneconomic, and removal restores fish migration, sediment flow and river ecosystems, as on the Elwha River where salmon returned after 2011-2014 removal.')],
  contrast=[('the benefits of large dams', 'the costs of large dams', 'Benefits include renewable electricity, irrigation, water supply and flood control; costs include displacement, loss of land and heritage, sediment trapping, ecological change and greenhouse emissions from reservoirs.'),
            ('large dams', 'small-scale water schemes', 'Large dams store vast volumes and serve national needs but have major social and environmental costs; small schemes (check dams, run-of-river hydro, tanks) serve local needs with lower impacts.')],
  misc=[('Hydroelectric power has no greenhouse-gas emissions.', 'Reservoirs, especially in the tropics, can emit methane from decomposing flooded vegetation, and construction uses cement.'),
        ('Dams always prevent flooding downstream.', 'Dams reduce moderate floods but can fail or be forced to release water in extreme events, and may encourage floodplain development.'),
        ('The benefits of dams are shared equally.', 'Benefits often go to urban consumers and commercial farmers while displaced rural and indigenous people bear the costs.')],
  apply=[('Using a named dam, outline two benefits and two costs.', 'e.g. Three Gorges: benefits - about 100 TWh/yr of electricity and flood storage of 22 billion m³; costs - 1.3 million people relocated and landslides around the reservoir; sediment trapping affects the Yangtze delta.', 4),
         ('Suggest why the Grand Ethiopian Renaissance Dam is important to Ethiopia.', 'About half the population lacked electricity; the 5.15 GW dam could double national generation and allow power exports to neighbours.', 2)],
  cases=[('the Three Gorges Dam, China', 'completed in 2006-2012, it is 2.3 km long, generates up to 22.5 GW and relocated about 1.3 million people', 'the costs and benefits of a multipurpose scheme', 'huge national benefits in energy and flood control came with major social and environmental costs'),
         ('the Sardar Sarovar Dam on the Narmada, India', 'inaugurated in 2017, it supplies water to Gujarat and Rajasthan but displaced tens of thousands of families', 'conflict over large dams', 'benefits for drought-prone regions were weighed against the rights of displaced tribal communities'),
         ('the Aswan High Dam, Egypt', 'completed in 1970, it ended the annual flood, enabled perennial irrigation and generated HEP, but trapped silt and displaced about 100,000 Nubians', 'long-term impacts of dams', 'it brought water security but the Nile delta now erodes and farmers need artificial fertiliser'),
         ('the removal of the Elwha River dams, USA', 'two dams were removed in 2011-2014, the largest dam removal in history', 'restoration through dam decommissioning', 'removal restored sediment flow to the coast and salmon migration')],
  evaluate=[('The benefits of large multipurpose dams outweigh their costs.', ['renewable electricity, irrigation and flood control for millions (Three Gorges, Aswan)', 'water storage for drought resilience'], ['displacement, ecological damage, sediment trapping', 'transboundary disputes (GERD)'], 'Benefits can outweigh costs at the national scale, but rarely for displaced people and ecosystems; outcomes depend on planning and compensation.'),
            ('Large dams are a sustainable way to manage water resources.', ['long life, renewable energy, storage', 'adaptation to variable rainfall'], ['sedimentation reduces lifespan; reservoir emissions', 'social costs and loss of river ecosystems'], 'Dams can contribute to sustainability only if well sited and managed; small-scale and integrated approaches are often more sustainable.')],
  extended=[('Evaluate the costs and benefits of a named multipurpose river scheme.', 'Award: named scheme with figures; economic, social, environmental impacts at different scales and for different stakeholders; judgement.', 10, 'long')],
  res=[('Table: Three Gorges Dam statistics - length 2,335 m; height 181 m; reservoir length about 660 km; installed capacity 22.5 GW; annual output about 100 TWh; people relocated about 1.3 million.',
        [('Calculate the capacity factor (annual output ÷ maximum possible output).', f'Maximum = 22.5 GW × 8,760 h = {22.5 * 8760 / 1000:.1f} TWh; capacity factor = 100 / {22.5 * 8760 / 1000:.1f} = {100 / (22.5 * 8.76) * 100:.0f}%'),
         ('Explain why the capacity factor is below 100%.', 'Output varies with river flow (lower in the dry season), water is released for flood storage and navigation, and turbines need maintenance.')]),
       ('Graph description: sediment discharge of the Nile reaching the Mediterranean (million tonnes per year) - before 1964: about 120; after 1970: about 2.',
        [('Calculate the percentage reduction.', f'(2 − 120)/120 × 100 = {pc(120, 2)}'),
         ('Explain two consequences of the change.', 'The delta coastline retreats (e.g. Rosetta promontory eroded by tens of metres a year); farmers lose natural silt and depend on fertilisers; sardine fisheries declined.')])])

S('ch11-st3', gens=['pct_water', 'water_stress'],
  terms=[('integrated drainage basin management (IDBM)', 'the coordinated management of land, water and related resources across a whole drainage basin, involving all stakeholders, to maximise economic and social welfare sustainably'),
         ('transboundary river', 'a river whose drainage basin crosses international borders, e.g. the Nile, Indus, Mekong and Danube'),
         ('riparian state', 'a country through which a river flows or which borders it'),
         ('hydropolitics', 'the politics of conflict and cooperation over shared water resources'),
         ('upstream-downstream conflict', 'tension between riparian states when upstream use (dams, abstraction, pollution) affects downstream users')],
  facts=[('Under the 1959 Nile Waters Agreement, how much water per year was allocated to Egypt?', '55.5 km³', ['5.5 km³', '18.5 km³', '84 km³'], 'Sudan was allocated 18.5 km³; upstream states were not party to the agreement.'),
         ('Which organisation brokered the Indus Waters Treaty in 1960?', 'The World Bank', ['The United Nations Security Council', 'The African Union', 'The Mekong River Commission'], 'The eastern rivers went to India and the western rivers to Pakistan.'),
         ('Under the Indus Waters Treaty, which rivers were allocated mainly to Pakistan?', 'The Indus, Jhelum and Chenab', ['The Ravi, Beas and Sutlej', 'The Ganges and Brahmaputra', 'The Amu Darya and Syr Darya'], 'India placed the treaty "in abeyance" in April 2025 after the Pahalgam attack.'),
         ('Which body was set up in 1995 by Cambodia, Laos, Thailand and Vietnam to manage a shared river?', 'The Mekong River Commission', ['The Nile Basin Initiative', 'ICPR', 'The Murray-Darling Basin Authority'], 'China and Myanmar are dialogue partners, not members.')],
  why=[('Explain why transboundary rivers can cause conflict.', 'Water is shared by states with different needs and power; upstream dams or abstraction reduce flows downstream; historical treaties may exclude some riparians; climate and population growth increase competition (e.g. GERD and Egypt).'),
       ('Explain why integrated drainage basin management is considered more sustainable than single-purpose management.', 'It treats the basin as a single system, balancing water supply, agriculture, energy, flood control and ecosystems, and involves stakeholders across sectors and borders, reducing conflict and environmental harm.'),
       ('Explain why the Grand Ethiopian Renaissance Dam has caused tension in the Nile basin.', 'Ethiopia sees it as essential for electricity and development; Egypt, which depends on the Nile for about 97% of its water, fears reduced flows during filling and droughts; no binding agreement on filling and operation was reached.'),
       ('Explain why the Indus Waters Treaty has been described as a success.', 'It survived several India-Pakistan wars for over 60 years by clearly dividing rivers, setting up a Permanent Indus Commission and dispute mechanisms - showing water cooperation is possible between rivals.')],
  contrast=[('upstream states', 'downstream states', 'Upstream states control the headwaters and can build dams or abstract water; downstream states depend on flows passing through other countries and are vulnerable to upstream decisions.'),
            ('cooperation', 'conflict over shared rivers', 'Cooperation involves treaties, joint commissions and data sharing (Indus treaty, Rhine ICPR); conflict involves disputes over allocation, dams and pollution (Nile, Mekong).')],
  misc=[('Wars over water between states are common.', 'Interstate "water wars" are rare; most transboundary water relations involve cooperation or diplomatic tension, though water adds to wider conflicts.'),
        ('Downstream countries are always weaker than upstream countries.', 'Egypt has historically been the dominant Nile power despite being downstream, because of military, economic and diplomatic strength.'),
        ('IDBM means one organisation controls all decisions in a basin.', 'IDBM emphasises coordination and participation among many stakeholders, not single control.')],
  apply=[('Using a named example, outline how a shared river has been managed cooperatively.', 'e.g. the Rhine: the International Commission for the Protection of the Rhine (1950) coordinated pollution control, especially after the 1986 Sandoz chemical spill; the Rhine Action Programme brought salmon back.', 4),
         ('Suggest two reasons why China\'s dams on the upper Mekong (Lancang) concern downstream countries.', 'They alter the timing of flows and trap sediment needed by the Mekong delta; reduced flows during droughts (2019) affected fisheries and rice farming downstream.', 2)],
  cases=[('the Nile and the GERD', 'Ethiopia began filling the 74 km³ reservoir in 2020 despite Egyptian and Sudanese objections', 'hydropolitics in a transboundary basin', 'an upstream state used its geographical position to challenge historical downstream allocations'),
         ('the Indus Waters Treaty (1960)', 'it divided the six Indus rivers between India and Pakistan and survived for over 60 years', 'cooperation over shared rivers', 'a clear allocation and a standing commission enabled long-lasting cooperation between rivals'),
         ('the Murray-Darling Basin Plan, Australia', 'adopted in 2012, it set sustainable diversion limits and bought back water entitlements to return about 2,750 GL a year to the environment', 'integrated drainage basin management', 'basin-wide limits balance irrigation with ecosystem health across four states'),
         ('the Rhine Action Programme', 'after the 1986 Sandoz spill killed fish over hundreds of kilometres, riparian states cut pollution and salmon returned', 'international basin cooperation', 'joint commissions and shared targets improved water quality across borders')],
  evaluate=[('Cooperation is more common than conflict in the management of shared rivers.', ['hundreds of water treaties exist; Indus and Rhine examples', 'interstate water wars are very rare'], ['tensions on the Nile, Mekong and Tigris-Euphrates', 'treaties can collapse (Indus in abeyance, 2025)'], 'Cooperation is more common, but rising demand and climate change are increasing tensions in key basins.'),
            ('Integrated drainage basin management is the most effective way to manage water resources.', ['whole-basin approach balances uses and ecosystems (Murray-Darling)', 'reduces upstream-downstream conflict'], ['difficult across borders and sectors; requires data and strong institutions', 'political interests may override plans'], 'IDBM is the best framework in principle, though effectiveness depends on governance and political will.')],
  extended=[('Examine the challenges of managing an internationally shared river.', 'Award: named basin(s) (Nile, Indus, Mekong, Rhine); upstream-downstream issues; treaties and institutions; power; climate; judgement.', 10, 'long')],
  res=[('Table: dependence on the Nile and allocations - Egypt: about 97% of renewable water from outside its borders, 1959 allocation 55.5 km³; Sudan: allocation 18.5 km³; Ethiopia: source of about 85% of Nile flow (Blue Nile, Atbara, Sobat), allocation 0 km³.',
        [('Calculate the combined 1959 allocation to Egypt and Sudan, and Egypt\'s share of it.', f'55.5 + 18.5 = 74 km³; Egypt\'s share = {55.5 / 74 * 100:.0f}%'),
         ('Explain why the data help to explain tension over the GERD.', 'Ethiopia supplies most of the water but received no allocation, while Egypt depends almost entirely on flows from upstream; the dam challenges the 1959 arrangement.')]),
       ('Map description: the Mekong flows about 4,900 km from the Tibetan Plateau through China (Lancang), Myanmar, Laos, Thailand, Cambodia and Vietnam; China has built 11 large dams on the main stem; the Tonlé Sap lake in Cambodia reverses flow seasonally.',
        [('Identify the upstream and downstream states.', 'Upstream: China (and Myanmar); downstream: Laos, Thailand, Cambodia and Vietnam (delta).'),
         ('Suggest one impact of upstream dams on the Tonlé Sap.', 'Lower wet-season flows reduce the reverse flow that fills the lake, cutting fish stocks that provide much of Cambodia\'s protein.')])])

S('ch11-st4', gens=['pct_water', 'water_stress'],
  terms=[('wetland', 'an area of land saturated with water permanently or seasonally, such as marshes, swamps, peatlands and floodplains'),
         ('aquifer', 'a body of permeable rock that can store and transmit groundwater, such as sandstone or chalk'),
         ('Ramsar Convention', 'the 1971 international treaty (signed in Ramsar, Iran) for the conservation and wise use of wetlands'),
         ('water table', 'the upper surface of the saturated zone in rocks or soil'),
         ('managed aquifer recharge', 'deliberately adding water to an aquifer, e.g. through infiltration ponds or injection wells, to store it for later use'),
         ('land subsidence', 'the sinking of the ground surface, often caused by the over-extraction of groundwater')],
  facts=[('The Ogallala (High Plains) Aquifer underlies parts of how many US states?', 'Eight', ['Two', 'Four', 'Fifteen'], 'It supplies about 30% of US irrigation groundwater and is being depleted.'),
         ('By about how much did the Aral Sea shrink from the 1960s to the 2010s?', 'About 90% of its area', ['About 10%', 'About 30%', 'It grew'], 'Soviet diversion of the Amu Darya and Syr Darya for cotton irrigation caused the collapse.'),
         ('Which dam, completed in 2005, helped the North Aral Sea to recover?', 'The Kok-Aral Dam', ['The Aswan High Dam', 'The Kariba Dam', 'The Tarbela Dam'], 'Levels rose and fisheries partly returned.'),
         ('Why is Indonesia moving its capital from Jakarta to Nusantara?', 'Partly because parts of Jakarta are sinking by up to 25 cm a year due to groundwater extraction', ['Because Jakarta has too much rainfall', 'Because of an earthquake in 2020', 'Because Jakarta ran out of land for airports'], 'About 40% of the city lies below sea level.')],
  why=[('Explain why wetlands are valuable in drainage basins.', 'They store floodwater and release it slowly, recharge groundwater, filter pollutants, store carbon (peatlands), support biodiversity and fisheries and provide livelihoods.'),
       ('Explain why groundwater depletion is difficult to reverse.', 'Many aquifers recharge slowly (fossil water may take thousands of years), compaction of clay layers permanently reduces storage, and users have little incentive to cut pumping in a common-pool resource.'),
       ('Explain why wetlands have been lost worldwide.', 'Drainage for agriculture, urban expansion, dams and abstraction reducing inflows, pollution and peat extraction; about 35% of wetlands have been lost since 1970.'),
       ('Explain how over-extraction of groundwater can cause land subsidence.', 'Pumping lowers pore-water pressure in aquifers and clay layers, which compact under the weight of overlying material, causing the ground to sink, as in Mexico City and Jakarta.')],
  contrast=[('confined aquifers', 'unconfined aquifers', 'An unconfined aquifer is open to the surface and recharged directly by infiltration; a confined aquifer is sealed above and below by impermeable layers and is under pressure, recharging slowly from distant areas.'),
            ('renewable groundwater', 'fossil groundwater', 'Renewable groundwater is replenished by current recharge; fossil groundwater accumulated in past wetter climates and is effectively non-renewable, e.g. the Nubian Sandstone Aquifer.')],
  misc=[('Wetlands are wasteland that should be drained.', 'Wetlands provide flood control, water purification, carbon storage and biodiversity worth far more than many drained uses.'),
        ('Groundwater is unlimited because it is hidden underground.', 'Many aquifers are being depleted faster than recharge (Ogallala, Punjab, North China Plain).'),
        ('The Aral Sea disaster was caused by climate change.', 'It was caused mainly by Soviet diversion of rivers for cotton irrigation from the 1960s.')],
  apply=[('Using a named example, outline two consequences of the loss of a wetland or inland water body.', 'e.g. the Aral Sea: the fishing industry at Muynak and Aralsk collapsed (about 40,000 jobs lost); exposed salty, pesticide-laden seabed caused dust storms and respiratory disease.', 4),
         ('Suggest two strategies to manage a depleting aquifer.', 'Metering and pricing groundwater; switching to drip irrigation and less thirsty crops; managed aquifer recharge; local water districts setting extraction limits (e.g. Kansas LEMAs on the Ogallala).', 2)],
  cases=[('the Aral Sea', 'diversion of the Amu Darya and Syr Darya for cotton shrank the lake by about 90%, but the Kok-Aral Dam (2005) partly restored the North Aral', 'the mismanagement and restoration of water bodies', 'unsustainable irrigation destroyed a lake, while targeted engineering allowed partial recovery'),
         ('the Ogallala Aquifer, USA', 'irrigation has lowered water tables by over 30 m in parts of Texas and Kansas', 'groundwater depletion', 'abstraction far exceeds the slow natural recharge of a largely fossil aquifer'),
         ('the Florida Everglades', 'about half the original wetland was drained, and the Comprehensive Everglades Restoration Plan (2000) aims to restore flows', 'wetland restoration', 'large-scale engineering is being used to restore natural water flows'),
         ('Mexico City', 'groundwater pumping supplies a large share of the city\'s water and parts of the city are sinking by up to about 35-50 cm a year', 'land subsidence from aquifer over-use', 'over-extraction compacts lake-bed clays, damaging buildings and pipes')],
  evaluate=[('Groundwater depletion is a greater threat to water security than surface-water scarcity.', ['aquifers supply about half of drinking water and 40% of irrigation; depletion is hidden and slow to reverse', 'subsidence is irreversible (Jakarta, Mexico City)'], ['surface droughts cause immediate crises (Cape Town)', 'groundwater can be managed and recharged'], 'Groundwater depletion is the more insidious long-term threat, though surface scarcity causes more visible short-term crises.'),
            ('Wetlands are best protected through international agreements such as the Ramsar Convention.', ['over 2,500 Ramsar sites covering about 250 million ha', 'raises awareness and international obligations'], ['the convention has weak enforcement; losses continue', 'national laws and local management (Everglades plan) achieve more'], 'Ramsar provides a framework, but effective protection depends on national policy and local action.')],
  extended=[('Examine the importance of wetlands and groundwater for sustainable water management.', 'Award: functions and values; threats (drainage, abstraction, subsidence); named cases (Aral Sea, Ogallala, Everglades, Jakarta); management responses; judgement.', 10, 'long')],
  res=[('Table: Aral Sea area (km²) - 1960: 68,000; 1989: 40,000; 2007: 17,400; 2014: about 7,000 (excluding seasonal areas).',
        [('Calculate the percentage reduction between 1960 and 2014.', f'(7,000 − 68,000)/68,000 × 100 = {pc(68000, 7000)}'),
         ('Describe the rate of change shown.', 'Decline throughout, from about 970 km² a year (1960-89) to about 1,250 km² a year (1989-2007) and then about 1,490 km² a year (2007-14).')]),
       ('Graph description: depth to groundwater in a monitoring well in western Kansas (Ogallala) - 1960: 25 m; 1980: 38 m; 2000: 49 m; 2020: 57 m.',
        [('Calculate the average rate of decline per year between 1960 and 2020.', f'(57 − 25)/60 = {32 / 60:.2f} m per year'),
         ('Suggest why the rate of decline appears to have slowed after 2000.', 'Some farmers switched to more efficient irrigation or dryland farming; local management areas reduced pumping; wells in the thinnest areas became uneconomic.')])])


# =============================================================================================
# Option G Urban environments
# =============================================================================================
S('ch12-st1', gens=['rank_size', 'nni', 'spearman_urban', 'density'],
  terms=[('urban hierarchy', 'the ranking of settlements by size and the range of functions and services they provide'),
         ('central place theory', 'Christaller\'s (1933) model explaining the size, number and spacing of settlements as market centres, using threshold and range'),
         ('threshold', 'the minimum number of customers needed to make a good or service viable'),
         ('range', 'the maximum distance people are willing to travel to obtain a good or service'),
         ('site', 'the physical characteristics of the land on which a settlement is built, e.g. a defensive hill, bridging point or water supply'),
         ('situation', 'the location of a settlement in relation to its surroundings, such as routes, resources and other settlements'),
         ('central business district (CBD)', 'the commercial core of a city, with the highest land values, tallest buildings and greatest accessibility')],
  facts=[('Which urban land-use model, based on Chicago, proposes a series of rings around the CBD?', 'Burgess\'s concentric zone model (1925)', ['Hoyt\'s sector model (1939)', 'Harris and Ullman\'s multiple nuclei model (1945)', 'The Griffin-Ford model (1980)'], 'Burgess identified CBD, zone in transition, working-class housing, middle-class and commuter zones.'),
         ('In the Griffin-Ford model of the Latin American city, where are the wealthiest residents located?', 'In a spine/sector extending from the CBD along a commercial boulevard', ['On the outer periphery in squatter settlements', 'Only in the zone in transition', 'Evenly spread throughout the city'], 'Peripheral squatter settlements house many poor migrants.'),
         ('Which model emphasises several separate centres of activity in a city?', 'The multiple nuclei model', ['The concentric zone model', 'The sector model', 'The bid-rent model only'], 'Harris and Ullman (1945) noted specialised nuclei such as industrial areas and suburban centres.')],
  why=[('Explain why land values are highest in the CBD.', 'The CBD is most accessible to the whole urban population, so competition between land users (especially retail and offices) for limited space is greatest; bid-rent theory explains the decline of land values with distance.'),
       ('Explain why classical urban land-use models are less useful for cities in the Global South.', 'They were based on 20th-century US cities; in many Latin American, African and Asian cities the poorest live on the periphery in informal settlements, colonial planning and rapid migration shape land use, and multiple centres develop.'),
       ('Explain how threshold and range determine the spacing of settlements in central place theory.', 'Higher-order goods need large thresholds and have long ranges, so they are found in fewer, larger, widely spaced centres; low-order goods have small thresholds and short ranges, so many small settlements provide them.'),
       ('Explain why cities develop distinct sectors of land use.', 'Transport routes, relief, rivers and early high-status areas attract similar uses, which then expand outward along routes (Hoyt), e.g. industrial corridors along railways.')],
  contrast=[('site', 'situation', 'Site refers to the physical land a settlement is built on (e.g. a river terrace); situation refers to its location relative to surrounding features, routes and settlements (e.g. at a crossroads).'),
            ('the concentric zone model', 'the sector model', 'The concentric model arranges land uses in rings around the CBD; the sector model arranges them in wedges along transport routes from the centre.')],
  misc=[('Urban land-use models describe every city accurately.', 'Models are simplifications; real cities are shaped by relief, history, planning and culture.'),
        ('The largest settlement always provides the most specialised functions in a region.', 'Usually true, but some small settlements have specialised functions (resorts, university towns, administrative capitals).'),
        ('In all cities the richest people live on the edge.', 'In many Latin American and African cities, wealthy residents cluster near the centre or in specific sectors while the poorest live on the periphery.')],
  apply=[('Using a named city, describe how its land use compares with one urban model.', 'e.g. Rio de Janeiro fits the Griffin-Ford model in part: a CBD (Centro), an elite spine along the coast (Copacabana, Ipanema, Barra), and favelas both on hillsides near the centre (Rocinha) and on the periphery.', 3),
         ('Suggest two reasons why many cities now have several centres rather than one CBD.', 'Car ownership and ring roads allowed out-of-town retail and business parks; high CBD land costs and congestion pushed firms out; planning created new centres (e.g. La Défense, Paris).', 2)],
  cases=[('Chicago in the 1920s', 'Burgess observed rings of land use from the Loop (CBD) outwards', 'the concentric zone model', 'immigrants arriving in the zone in transition and wealthier groups moving outward produced a ring pattern'),
         ('Rio de Janeiro', 'elite districts form a coastal spine while favelas occupy steep hillsides and the periphery', 'the Latin American city model', 'social and physical factors produce a sectoral elite spine with peripheral informal housing'),
         ('La Défense, Paris', 'a planned business district outside the historic centre with about 180,000 workers', 'the multiple nuclei model', 'a secondary centre specialising in offices shows a multi-nuclear city')],
  evaluate=[('Urban land-use models have little value in understanding contemporary cities.', ['based on early 20th-century US cities; ignore planning, culture and globalisation', 'Global South cities differ greatly'], ['bid-rent and accessibility principles still explain land values', 'models provide a framework for comparison'], 'Models remain useful as simplified frameworks but must be adapted to local contexts.'),
            ('Physical site factors are no longer important in explaining the growth of cities.', ['global connections, policy and investment drive growth (Dubai, Shenzhen)', 'technology overcomes site limits (reclamation, desalination)'], ['coasts, rivers and harbours still shape the largest cities', 'site affects hazards and expansion (Hong Kong, Mexico City)'], 'Situation and human factors dominate growth today, but site still shapes city form and risk.')],
  extended=[('Examine the extent to which urban land-use models explain the structure of a named city.', 'Award: named city with specific districts; comparison with at least one model; reasons for differences; judgement.', 10, 'long')],
  res=[('Table: land value and distance from the CBD in a Latin American city (US$ per m²) - 0 km: 4,200; 2 km: 2,100; 4 km: 1,300; 6 km: 2,600 (elite spine); 8 km: 400; 10 km: 150 (peripheral settlement).',
        [('Describe the relationship between land value and distance.', 'Values generally decline with distance from the CBD (4,200 to 150), but with an anomaly at 6 km (2,600) in the elite spine.'),
         ('Explain the anomaly at 6 km using the Griffin-Ford model.', 'A commercial-residential spine of high-status housing and services extends from the CBD, raising land values along it.')]),
       ('Settlement survey description: a region has 1 city (population 450,000, 120 services), 4 towns (about 30,000, 35 services), 16 villages (about 2,000, 6 services) and 60 hamlets (under 200, 0-1 services).',
        [('Describe the urban hierarchy shown.', 'A pyramid-shaped hierarchy: few large settlements with many services and many small settlements with few services.'),
         ('Explain the relationship using threshold and range.', 'Large populations exceed the thresholds of high-order services, so these are only found in the city; small settlements support only low-order services with small thresholds.')])])

S('ch12-st2', gens=['urban_pct', 'pct_urban', 'migration'],
  terms=[('urbanisation', 'the increase in the proportion of a population living in urban areas'),
         ('suburbanisation', 'the outward growth of urban areas as people and services move from inner areas to the suburbs'),
         ('counter-urbanisation', 'the movement of people from large urban areas to smaller towns and rural areas beyond the city'),
         ('reurbanisation', 'the movement of people back into city centres and inner areas, often following regeneration'),
         ('gentrification', 'the movement of higher-income residents into a lower-income area, upgrading housing and often displacing existing residents'),
         ('urban sprawl', 'the unplanned, low-density spread of an urban area into surrounding countryside')],
  facts=[('What percentage of the world\'s population lived in urban areas in 2018 according to the UN?', 'About 55%', ['About 25%', 'About 40%', 'About 80%'], 'The UN projects 68% by 2050.'),
         ('China\'s level of urbanisation rose from about 18% in 1978 to about what level in 2023?', 'About 66%', ['About 25%', 'About 40%', 'About 95%'], 'Hundreds of millions moved to cities after economic reforms.'),
         ('Which US suburb, built from 1947, became a symbol of post-war suburbanisation?', 'Levittown, New York', ['Harlem, New York', 'Detroit city centre', 'Venice, California'], 'Mass-produced houses were sold to returning veterans.'),
         ('Which body regenerated London\'s Docklands from 1981 to 1998?', 'The London Docklands Development Corporation', ['The Greater London Council', 'The Olympic Delivery Authority', 'Transport for London'], 'Canary Wharf became a second financial centre.')],
  why=[('Explain why suburbanisation occurred in high-income countries after 1945.', 'Rising car ownership and new roads, cheaper land and mortgages, desire for space and gardens, slum clearance and new housing, and decentralisation of jobs and retail.'),
       ('Explain why counter-urbanisation has occurred in some high-income countries.', 'Improved transport and remote working (accelerated by COVID-19) let people live in rural areas; retirees and families seek quality of life, lower house prices and less crime.'),
       ('Explain why reurbanisation has taken place in many western city centres.', 'Regeneration of brownfield sites, new apartments and amenities, jobs in finance and services, young professionals and students attracted by city life, and policies favouring dense development.'),
       ('Explain why urbanisation is rapid in low-income countries.', 'Rural-urban migration driven by rural poverty and urban job prospects combined with high natural increase among young urban populations.')],
  contrast=[('urbanisation', 'urban growth', 'Urbanisation is an increase in the proportion of people living in urban areas; urban growth is an increase in the absolute number of urban residents or area.'),
            ('counter-urbanisation', 'suburbanisation', 'Suburbanisation moves people to the edges of the same urban area; counter-urbanisation moves them beyond it to small towns and rural areas.')],
  misc=[('Urbanisation and urban growth mean the same thing.', 'Urbanisation is a rising urban share of the population; urban growth is an increase in urban population or area, which can occur without urbanisation.'),
        ('Gentrification benefits everyone in a neighbourhood.', 'It improves housing and services but can raise rents and displace lower-income residents and businesses.'),
        ('Counter-urbanisation means cities are declining in all high-income countries.', 'Many cities grow through reurbanisation and immigration even as some residents leave for rural areas.')],
  apply=[('Using a named example, describe the process of reurbanisation and one consequence.', 'e.g. Manchester: city-centre population grew from about 1,000 (1990s) to over 60,000 by the 2020s through apartment building in former warehouses and new towers; consequence - rising rents and gentrification of nearby Ancoats.', 4),
         ('Suggest two impacts of suburbanisation on a city centre.', 'Loss of population and tax base; decline of inner-city retail and services; vacant buildings; but reduced inner-city overcrowding.', 2)],
  cases=[('Shenzhen, China', 'a fishing area of about 30,000 people in 1979 became a city of over 17 million after becoming a Special Economic Zone in 1980', 'rapid urbanisation', 'economic reforms and FDI drove massive rural-urban migration'),
         ('the regeneration of the London Docklands', 'the LDDC (1981-1998) regenerated derelict docks; Canary Wharf now employs over 100,000 people', 'reurbanisation and regeneration', 'investment brought new jobs and residents into a declining inner area, though many original residents felt excluded'),
         ('Levittown, New York', 'about 17,000 houses were built from 1947 for commuters to New York City', 'suburbanisation', 'cheap mortgages, cars and mass housing pulled families out to the suburbs'),
         ('the rise of "Zoom towns" in the USA after 2020', 'remote workers moved to small towns such as Bozeman, Montana, raising house prices', 'counter-urbanisation', 'technology freed some workers from cities, spreading urban demand into rural areas')],
  evaluate=[('Urbanisation brings more benefits than costs to low-income countries.', ['higher incomes, services and productivity; cities generate most GDP', 'lower fertility and better access to education'], ['slums, congestion and pollution (Lagos, Dhaka)', 'informal work and inequality'], 'Urbanisation is central to development; costs depend on how well it is planned and governed.'),
            ('Reurbanisation has been successful in regenerating inner-city areas.', ['population and jobs returned (Manchester, London Docklands)', 'brownfield reuse reduces sprawl'], ['gentrification displaces residents; benefits unequal', 'some cities still decline (Detroit)'], 'It has transformed many centres economically, but success for existing communities has been mixed.')],
  extended=[('Examine the factors that cause urbanisation, suburbanisation and reurbanisation.', 'Award: each process defined; drivers (economic, social, transport, policy); named examples in contrasting places; judgement.', 10, 'long')],
  res=[('Table: urban population (% of total, UN WUP) - World 1950: 30, 2018: 55, 2050: 68; Africa 1950: 14, 2018: 43, 2050: 59; Europe 1950: 52, 2018: 74, 2050: 84.',
        [('Calculate the percentage-point change for Africa 2018-2050 and compare it with Europe.', 'Africa +16 points; Europe +10 points - Africa will urbanise faster.'),
         ('Suggest two reasons why Africa is urbanising rapidly.', 'High natural increase in cities; rural-urban migration from poverty, drought and conflict; growth of urban economies.')]),
       ('Population data, Manchester city centre - 1991: about 1,000 residents; 2001: about 10,000; 2011: about 25,000; 2021: about 60,000.',
        [('Calculate the percentage increase 2011-2021.', f'(60,000 − 25,000)/25,000 × 100 = {pc(25000, 60000)}'),
         ('Identify the process shown and suggest two causes.', 'Reurbanisation: conversion of warehouses and new apartment towers; growth of service jobs and universities; regeneration after the 1996 IRA bombing.')])])

S('ch12-st3', gens=['pct_urban', 'stats_hum'],
  terms=[('informal sector', 'economic activity that is not regulated, taxed or protected by the state, such as street vending, waste picking and small workshops'),
         ('deindustrialisation', 'the decline of manufacturing employment and output in a region or country'),
         ('peak land value intersection', 'the most accessible point of the CBD with the highest land values'),
         ('global shift', 'the relocation of manufacturing from high-income to lower-cost countries, especially in Asia, since the 1970s'),
         ('out-of-town retail', 'shopping centres and retail parks located on the edge of urban areas, close to major roads and with large car parks')],
  facts=[('According to the ILO, about what share of the world\'s workers are in informal employment?', 'About 60%', ['About 10%', 'About 30%', 'About 90%'], 'About 2 billion workers; over 85% in Africa.'),
         ('Detroit\'s population fell from about 1.85 million in 1950 to about what in 2020?', 'About 640,000', ['About 1.5 million', 'About 1 million', 'About 100,000'], 'Deindustrialisation of the car industry and suburbanisation led to decline and bankruptcy in 2013.'),
         ('The Zollverein coal mine complex, a UNESCO World Heritage Site and cultural centre, is in which deindustrialised region?', 'The Ruhr, Germany', ['Silesia, Poland', 'The Rust Belt, USA', 'Lorraine, France'], 'It was inscribed in 2001 as an example of industrial heritage regeneration.'),
         ('Dharavi in Mumbai is notable for:', 'a large informal economy including recycling, leather and pottery, estimated at hundreds of millions of US$ a year', ['being the main CBD of Mumbai', 'its car manufacturing plants', 'a population of under 5,000'], 'About 1 million people live in about 2.1 km².')],
  why=[('Explain why the informal sector is large in cities of low-income countries.', 'Rapid urban growth exceeds formal job creation; migrants lack skills or documents; the informal sector has easy entry and low capital needs; regulations and taxes are costly to comply with.'),
       ('Explain why deindustrialisation occurred in cities such as Detroit and Manchester.', 'Competition from lower-cost countries (global shift), automation, decline of traditional industries, lack of investment and suburban relocation of firms led to factory closures and job losses.'),
       ('Explain why CBDs in many cities have changed in recent decades.', 'Competition from out-of-town retail and e-commerce has reduced shopping; offices and finance have grown; city-centre living, leisure and night-time economies have expanded; some CBDs have pedestrianised.'),
       ('Explain the positive contributions of the informal sector to urban economies.', 'It provides jobs and incomes for millions, cheap goods and services, recycling and entrepreneurship, and acts as a safety net when formal jobs are lacking.')],
  contrast=[('the formal sector', 'the informal sector', 'The formal sector consists of registered, taxed and regulated employment with contracts and protections; the informal sector is unregistered, untaxed and insecure.'),
            ('deindustrialisation', 'tertiarisation', 'Deindustrialisation is the decline of manufacturing; tertiarisation is the growth of service-sector employment, which often replaces it.')],
  misc=[('The informal sector is the same as illegal activity.', 'Most informal work (vending, repairs, recycling) is legal but unregistered and unprotected.'),
        ('Deindustrialisation affects only the economy.', 'It also causes unemployment, population decline, derelict land, social deprivation and health problems.'),
        ('E-commerce has completely replaced the CBD as a shopping location.', 'CBDs have declined in retail but adapted with leisure, food, offices, residences and experiences.')],
  apply=[('Using a named city, outline two consequences of deindustrialisation.', 'e.g. Detroit: population fell by about two-thirds, leaving tens of thousands of vacant homes; the city declared bankruptcy in 2013 with about US$18 billion of debt.', 4),
         ('Suggest two ways that city governments could support informal workers.', 'Designated vending zones and licences; microfinance and training; access to water, sanitation and storage; social protection schemes.', 2)],
  cases=[('Detroit, USA', 'the population fell from about 1.85 million in 1950 to about 640,000 in 2020 as car-industry jobs were lost', 'deindustrialisation', 'loss of manufacturing caused population decline, dereliction and municipal bankruptcy'),
         ('Dharavi, Mumbai', 'about 1 million people live in about 2 km², with thousands of small enterprises in recycling, leather and pottery', 'the informal urban economy', 'informal work supports a large population and recycles much of the city\'s waste'),
         ('the Ruhr, Germany', 'coal and steel closures were followed by regeneration such as the Zollverein complex and IBA Emscher Park', 'responses to deindustrialisation', 'industrial heritage, culture and new services helped regenerate a declining region'),
         ('Bluewater, Kent', 'one of Europe\'s largest out-of-town shopping centres opened in 1999 in a former chalk quarry', 'the decentralisation of retail', 'accessible edge-of-city sites drew shoppers away from traditional town centres')],
  evaluate=[('The informal sector does more harm than good to urban economies.', ['lost tax revenue; insecure, unprotected and low-paid work', 'unsafe conditions (e.g. e-waste recycling)'], ['provides jobs for billions and cheap goods and services', 'entrepreneurship and recycling (Dharavi)'], 'The informal sector is essential to urban survival in low-income cities; policy should improve conditions rather than eliminate it.'),
            ('Deindustrialised cities can successfully reinvent their economies.', ['Manchester and the Ruhr developed services, culture and education', 'regeneration attracts investment and residents'], ['Detroit and other Rust Belt cities still face poverty', 'new jobs may not suit former industrial workers'], 'Reinvention is possible with investment and strategy, but benefits are unevenly shared.')],
  extended=[('Examine the changing economic activities in cities in contrasting countries.', 'Award: CBD change, deindustrialisation, tertiary growth, informal sector; named cities (Detroit, Manchester, Mumbai, Lagos); causes and impacts; judgement.', 10, 'long')],
  res=[('Table: employment by sector in Manchester (% of workforce) - 1971: manufacturing 38, services 55, other 7; 2021: manufacturing 6, services 90, other 4.',
        [('Calculate the change in manufacturing share in percentage points.', '6 − 38 = −32 percentage points'),
         ('Describe and explain the change shown.', 'A shift from manufacturing to services (deindustrialisation and tertiarisation) caused by the global shift of textiles and engineering to Asia and growth of finance, media, education and retail.')]),
       ('Pie chart description: informal employment as % of total employment (ILO) - Africa 85.8; Asia-Pacific 68.2; Arab States 68.6; Americas 40.0; Europe and Central Asia 25.1.',
        [('Describe the regional pattern.', 'Informality is highest in Africa (about 86%) and lowest in Europe and Central Asia (about 25%), roughly linked to income levels.'),
         ('Suggest why informality is so high in Africa.', 'Rapid urban growth and young labour forces exceed formal job creation; limited regulation capacity; agriculture and small enterprises dominate.')])])

S('ch13-st1', gens=['pct_urban', 'stats_hum', 'chi_hum', 'density'],
  terms=[('urban stress', 'pressures on people and environments in cities, such as pollution, congestion, poor housing, crime and deprivation'),
         ('slum', 'an urban area with inadequate access to safe water, sanitation, durable housing, sufficient living space or secure tenure (UN-Habitat)'),
         ('multiple deprivation', 'the combined disadvantage of people suffering from several forms of deprivation, such as low income, poor health, poor education and crime'),
         ('traffic congestion', 'a situation where road demand exceeds capacity, slowing traffic, increasing travel times and pollution'),
         ('urban social segregation', 'the separation of different social, ethnic or income groups into distinct residential areas')],
  facts=[('About how many people live in slums or informal settlements worldwide (UN-Habitat)?', 'About 1.1 billion', ['About 110 million', 'About 11 million', 'About 4 billion'], 'Numbers are projected to grow by billions more by 2050 without action.'),
         ('Kibera, one of Africa\'s largest informal settlements, is in which city?', 'Nairobi', ['Lagos', 'Johannesburg', 'Accra'], 'Estimates of its population vary widely, from about 250,000 to over 500,000.'),
         ('Which community-led sanitation project began in Karachi in 1980?', 'The Orangi Pilot Project', ['Slum Upgrading Kibera', 'Favela-Bairro', 'Hoy No Circula'], 'Residents financed and built their own lane sewers at low cost.'),
         ('The annual WHO air-quality guideline (2021) for PM2.5 is:', '5 µg/m³', ['50 µg/m³', '25 µg/m³', '100 µg/m³'], 'Delhi\'s annual mean is often more than 15-20 times this level.')],
  why=[('Explain why informal settlements develop on hazardous land.', 'Migrants cannot afford formal housing; steep slopes, floodplains, rail lines and refuse dumps are unclaimed or cheap; proximity to jobs matters more than safety, e.g. favelas on Rio\'s hillsides.'),
       ('Explain how traffic congestion causes environmental and economic stress.', 'Slow traffic increases fuel use, air pollution (NO₂, PM2.5) and CO₂ emissions, lengthens commuting times, reduces productivity and raises business costs.'),
       ('Explain why deprivation tends to be concentrated in particular parts of a city.', 'Low incomes restrict housing choices to cheap areas; cumulative disadvantage - poor schools, health, crime and unemployment - reinforces itself; discrimination and housing policy concentrate groups.'),
       ('Explain why slum upgrading may be more effective than slum clearance.', 'Upgrading keeps communities and livelihoods intact, gives secure tenure and improves services at lower cost; clearance destroys homes and social networks and often moves people to distant sites without jobs.')],
  contrast=[('slum clearance', 'slum upgrading', 'Clearance demolishes informal settlements and relocates residents; upgrading improves services, housing and tenure in place, often with resident participation.'),
            ('urban environmental stress', 'urban social stress', 'Environmental stresses include air and water pollution, waste and noise; social stresses include crime, deprivation, overcrowding and segregation.')],
  misc=[('Slums are only found in low-income countries.', 'Informal and substandard housing also exists in high-income countries, e.g. homeless encampments and informal settlements in Europe and the USA.'),
        ('All residents of informal settlements are unemployed.', 'Most residents work, often in the informal sector, and many settlements are economically productive (e.g. Dharavi).'),
        ('Building more roads permanently solves traffic congestion.', 'New road capacity often generates more traffic (induced demand), so congestion returns.')],
  apply=[('Using a named city, outline two urban stresses and their causes.', 'e.g. Lagos: severe congestion (average commuting of several hours) caused by rapid growth and limited public transport; flooding and poor sanitation in informal settlements such as Makoko.', 4),
         ('Suggest two indicators that could be used to map deprivation in a city.', 'Unemployment rate, income, educational attainment, life expectancy or illness rates, crime rates, overcrowding.', 2)],
  cases=[('the Orangi Pilot Project, Karachi', 'residents built about 100,000 house sewer connections at a fraction of the government cost', 'community responses to urban stress', 'self-help with technical support improved sanitation for hundreds of thousands of people'),
         ('Rocinha, Rio de Janeiro', 'Brazil\'s largest favela, with over 70,000 residents (some estimates over 100,000) on steep hillsides', 'informal settlements and their stresses', 'rapid growth on hazardous slopes created issues of landslides, sanitation and violence, but strong community networks'),
         ('Delhi\'s air pollution', 'annual PM2.5 levels often exceed 100 µg/m³ and winter smog peaks above 400 µg/m³', 'environmental stress in cities', 'vehicles, industry, construction dust and crop burning combine with winter inversions to create severe pollution'),
         ('Lagos traffic', 'residents can spend several hours a day commuting, and the Lagos Blue Line light rail opened in 2023', 'traffic congestion', 'rapid growth without mass transit created chronic congestion')],
  evaluate=[('Urban stresses are mainly caused by rapid population growth.', ['growth exceeds housing and infrastructure (Lagos, Dhaka)', 'more vehicles and waste'], ['governance, planning and inequality determine outcomes (Singapore is dense but well managed)', 'deindustrialisation causes stress in shrinking cities (Detroit)'], 'Growth adds pressure, but governance and inequality largely determine whether stress results.'),
            ('Community-led schemes are the most effective way to tackle urban deprivation.', ['low cost, local knowledge and ownership (Orangi)', 'build social capital'], ['need state funding and infrastructure for scale', 'some problems (air pollution, transport) need citywide action'], 'Community schemes are highly effective locally, but must be supported by city and national policy.')],
  extended=[('Examine the causes and consequences of urban social and environmental stresses in a named city.', 'Award: named city with specific districts and data; causes; consequences for different groups; responses; judgement.', 10, 'long')],
  res=[('Table: Index of Multiple Deprivation scores in four wards of a UK city (higher = more deprived) - Ward A 54.2; Ward B 38.7; Ward C 12.1; Ward D 7.9.',
        [('Calculate the range and mean of the scores.', f'Range = 54.2 − 7.9 = {54.2 - 7.9:.1f}; mean = {(54.2 + 38.7 + 12.1 + 7.9) / 4:.1f}'),
         ('Suggest two reasons why wards A and B are more deprived.', 'Inner-city location affected by deindustrialisation; older, poorer-quality housing; higher unemployment; lower educational attainment.')]),
       ('Graph description: annual mean PM2.5 (µg/m³, recent year) - Delhi 102; Lahore 99; Dhaka 80; Beijing 38; London 9; Stockholm 5.',
        [('How many times the WHO guideline (5 µg/m³) is Delhi\'s level?', f'102 / 5 = {102 / 5:.1f} times'),
         ('Suggest why Beijing\'s level is much lower than Delhi\'s despite similar size.', 'Beijing\'s action plan since 2013 replaced coal heating with gas and electricity, restricted vehicles and moved industry, reducing PM2.5 by over half.')])])

S('ch13-st2', gens=['uhi', 'albedo', 'spearman_urban', 'pct_urban'],
  terms=[('urban heat island (UHI)', 'the phenomenon whereby urban areas are warmer than surrounding rural areas, especially at night'),
         ('urban microclimate', 'the distinctive climate of an urban area, with differences in temperature, wind, humidity, precipitation and air quality from surrounding areas'),
         ('temperature inversion', 'a layer of warm air above cooler surface air that traps pollutants near the ground'),
         ('photochemical smog', 'air pollution formed when sunlight reacts with nitrogen oxides and volatile organic compounds from vehicles, producing ground-level ozone'),
         ('urban canyon', 'a street flanked by tall buildings that traps heat and pollutants and channels wind'),
         ('congestion charge', 'a fee charged to drivers entering a defined zone, used to reduce traffic and pollution, e.g. London since 2003')],
  facts=[('When is the urban heat island usually most intense?', 'On calm, clear nights', ['On windy, cloudy days', 'During heavy rain', 'At midday in winter'], 'Stored heat is released at night and calm conditions prevent mixing.'),
         ('In which year did Singapore introduce Electronic Road Pricing (ERP)?', '1998', ['1975', '2003', '2019'], 'It replaced the 1975 Area Licensing Scheme, the world\'s first urban congestion charge.'),
         ('Which city\'s "Hoy No Circula" programme (1989) restricts car use by licence plate?', 'Mexico City', ['Bogotá', 'São Paulo', 'Lima'], 'It was a response to severe smog.'),
         ('London\'s Ultra Low Emission Zone (ULEZ) was introduced in central London in:', '2019', ['1995', '2003', '2012'], 'It was expanded to all London boroughs in August 2023.')],
  why=[('Explain the causes of the urban heat island effect.', 'Dark surfaces (low albedo) absorb more radiation; concrete and asphalt store heat and release it at night; less vegetation and water mean less evapotranspiration; heat from vehicles, buildings and air-conditioning; urban canyons trap longwave radiation; pollution increases absorption.'),
       ('Explain why temperature inversions worsen urban air pollution.', 'A layer of warmer air above cooler surface air prevents vertical mixing, so pollutants accumulate near the ground; cities in basins such as Mexico City, Los Angeles and Santiago are especially affected.'),
       ('Explain how green roofs and urban trees can reduce the heat island.', 'Vegetation shades surfaces and cools air through evapotranspiration, has higher albedo than asphalt and stores less heat; Medellín\'s green corridors reduced local temperatures by about 2 °C.'),
       ('Explain why cities may receive more rainfall than surrounding areas.', 'Heat islands create convection; pollutant particles provide condensation nuclei; tall buildings increase turbulence - so thunderstorms are more frequent downwind.')],
  contrast=[('the urban heat island', 'photochemical smog', 'The UHI is an increase in urban temperatures caused by surfaces, heat and reduced evaporation; photochemical smog is air pollution (ground-level ozone) formed from vehicle emissions and sunlight.'),
            ('a congestion charge', 'a low emission zone', 'A congestion charge charges all vehicles entering a zone to cut traffic volume; a low emission zone charges or bans only the most polluting vehicles to improve air quality.')],
  misc=[('The urban heat island is strongest during hot summer afternoons.', 'The urban-rural difference is usually greatest on calm, clear nights when rural areas cool rapidly.'),
        ('Air pollution in cities only comes from factories.', 'Road vehicles, domestic heating and cooking, construction dust and regional sources (e.g. crop burning near Delhi) are major sources.'),
        ('Planting a few trees will eliminate a city\'s heat island.', 'Trees help locally, but large-scale changes to surfaces, building design and energy use are needed.')],
  apply=[('Using a named city, outline two strategies used to improve urban air quality and their effectiveness.', 'e.g. London: the congestion charge (2003) cut traffic in the zone by about 30% initially; ULEZ (2019, expanded 2023) reduced roadside NO₂ in central London by about half compared with no scheme.', 4),
         ('Suggest two reasons why the heat island is a growing health risk.', 'Climate change increases heatwave frequency and intensity; ageing urban populations are more vulnerable; night-time heat prevents recovery, increasing mortality.', 2)],
  cases=[('Medellín\'s Green Corridors project, Colombia', '30 corridors of trees and plants along roads and waterways reduced local temperatures by about 2 °C', 'managing the urban heat island', 'vegetation increases shade and evapotranspiration, cooling streets'),
         ('London\'s ULEZ', 'introduced in 2019 and expanded across London in 2023, charging non-compliant vehicles £12.50 a day', 'urban air-quality management', 'charging polluting vehicles reduced NO₂ concentrations'),
         ('Mexico City\'s smog', 'in 1992 the UN described it as the most polluted city in the world; the basin and altitude trap pollutants', 'the influence of site on urban air pollution', 'mountains and inversions trap emissions in the basin'),
         ('Beijing\'s Clean Air Action Plan (2013)', 'coal heating was replaced by gas and electricity and PM2.5 fell by over 50% by 2020', 'government action on urban pollution', 'large-scale energy switching cut a key pollution source')],
  evaluate=[('Air pollution is the most serious urban microclimate problem.', ['causes about 4 million premature deaths a year from outdoor air pollution worldwide', 'affects all residents, especially the poor'], ['the UHI amplifies heatwaves that kill thousands (2003 Europe)', 'flash flooding from urban rainfall'], 'Air pollution is the largest health burden, but heat is a rapidly growing threat linked to climate change.'),
            ('Traffic management strategies are the most effective way to improve urban air quality.', ['vehicles are a major NO₂ and PM source; London\'s ULEZ and Singapore ERP worked', 'can be targeted and quick'], ['heating, industry and regional sources must also be tackled (Beijing coal, Delhi crop burning)', 'public transport and land-use planning are needed'], 'Traffic measures are essential but must be part of a broader strategy covering all sources.')],
  extended=[('Examine the causes of the urban heat island and evaluate strategies to reduce it.', 'Award: causes (albedo, heat storage, anthropogenic heat, evapotranspiration, canyon geometry); named city data; strategies (green roofs, cool roofs, parks, water, planning); judgement.', 10, 'long')],
  res=[('Transect data, Paris at 23:00 on a calm summer night - city centre 26.8 °C; 3 km 26.1 °C; 6 km 25.0 °C; 10 km 23.4 °C; 15 km (rural) 20.9 °C.',
        [('Calculate the heat island intensity and the mean temperature gradient.', f'Intensity = 26.8 − 20.9 = {26.8 - 20.9:.1f} °C; gradient = {26.8 - 20.9:.1f}/15 = {(26.8 - 20.9) / 15:.2f} °C per km'),
         ('Suggest two reasons why the difference is greatest at night.', 'Urban materials release heat stored during the day; rural areas cool quickly by radiation under clear skies; calm conditions prevent mixing.')]),
       ('Table: roadside NO₂ in central London (annual mean µg/m³) - 2016: 94; 2019: 55; 2022: 41.',
        [('Calculate the percentage fall between 2016 and 2022.', f'(41 − 94)/94 × 100 = {pc(94, 41)}'),
         ('Suggest two factors that contributed to the fall.', 'The ULEZ (2019) and Toxicity Charge (2017); cleaner bus fleets; COVID-19 lockdowns reduced traffic in 2020-21.')])])

S('ch13-st3', gens=['pct_urban', 'energy_mix', 'carbon'],
  terms=[('sustainable city', 'a city that meets the needs of its present residents without compromising future generations, balancing environmental, social and economic goals'),
         ('smart city', 'a city that uses digital technology, sensors and data to manage services such as transport, energy and water more efficiently'),
         ('eco-city', 'a city designed to minimise environmental impact through renewable energy, low-carbon transport, green space and resource efficiency'),
         ('urban resilience', 'the capacity of a city\'s people, institutions and systems to survive, adapt and grow despite chronic stresses and acute shocks'),
         ('bus rapid transit (BRT)', 'a high-capacity bus system with dedicated lanes and stations that offers metro-like service at lower cost, pioneered in Curitiba'),
         ('15-minute city', 'an urban planning concept in which daily needs are within a 15-minute walk or cycle, promoted in Paris')],
  facts=[('Which city pioneered bus rapid transit in 1974 under mayor Jaime Lerner?', 'Curitiba, Brazil', ['Bogotá, Colombia', 'Mexico City', 'Lagos, Nigeria'], 'Its Rede Integrada de Transporte carries over a million passengers a day.'),
         ('Masdar City, a planned zero-carbon eco-city begun in 2006, is in:', 'Abu Dhabi, UAE', ['Seoul, South Korea', 'Copenhagen, Denmark', 'Freiburg, Germany'], 'Its targets and scale were later reduced.'),
         ('Which purpose-built smart city near Incheon, South Korea, has been criticised as "a ghost town" in its early years?', 'Songdo', ['Gangnam', 'Busan', 'Sejong'], 'It was built on reclaimed land with ubiquitous sensors and pneumatic waste collection.'),
         ('Which Freiburg district is known for car-free streets and passive-house design?', 'Vauban', ['Kreuzberg', 'Westend', 'Altstadt'], 'Many households do not own cars; homes are highly energy efficient.')],
  why=[('Explain why Curitiba is often cited as a model sustainable city.', 'Its BRT system integrated with land-use planning (high-density corridors), extensive parks on flood-prone land, recycling programmes (Green Exchange) and affordable public transport reduced car use and flooding at relatively low cost.'),
       ('Explain why some eco-city projects have struggled.', 'High costs, top-down design that ignores residents, economic downturns (Masdar after 2008), difficulty attracting people and businesses, and a focus on technology rather than social needs.'),
       ('Explain how smart technology can make cities more sustainable.', 'Sensors and data optimise traffic signals, public transport, street lighting, energy grids and leak detection, reducing congestion, energy use and waste; apps encourage sharing and active travel.'),
       ('Explain how cities can build resilience to shocks such as floods and heatwaves.', 'Through risk mapping and planning, green-blue infrastructure, early warnings, robust services, diverse economies and strong community networks, e.g. Rotterdam\'s water squares and Medellín\'s green corridors.')],
  contrast=[('a smart city', 'an eco-city', 'A smart city focuses on digital technology and data to improve services; an eco-city focuses on environmental sustainability through design, energy and green space - a city can be one without the other.'),
            ('top-down urban planning', 'bottom-up urban planning', 'Top-down planning is directed by governments or developers (Masdar, Songdo); bottom-up planning involves residents and communities (participatory budgeting in Porto Alegre).')],
  misc=[('Smart cities are automatically sustainable.', 'Technology can improve efficiency, but sustainability also needs social equity, affordable housing and low-carbon lifestyles; smart systems can raise privacy and inclusion concerns.'),
        ('Only new, purpose-built cities can become sustainable.', 'Existing cities such as Copenhagen, Curitiba and Freiburg have become more sustainable through retrofitting and policy.'),
        ('Resilient cities avoid all damage from hazards.', 'Resilience means absorbing shocks, recovering quickly and adapting, not avoiding all damage.')],
  apply=[('Using a named city, outline two features that make it sustainable.', 'e.g. Copenhagen: about 45% of commutes to work or study by bicycle on over 380 km of cycle lanes; district heating from waste-to-energy (Amager Bakke/CopenHill) and wind power.', 4),
         ('Suggest two criticisms of purpose-built smart cities.', 'High cost and exclusion of lower-income residents; surveillance and data privacy concerns; lack of community and vitality ("ghost town" image).', 2)],
  cases=[('Curitiba, Brazil', 'its BRT system carries over a million passengers daily and the city has over 50 m² of green space per person', 'sustainable urban design in a middle-income country', 'integrated transport and land-use planning delivered sustainability at low cost'),
         ('Masdar City, Abu Dhabi', 'planned for 50,000 residents and zero carbon in 2006, it had only a few thousand residents and relaxed targets by the 2020s', 'the challenges of eco-city projects', 'top-down, high-tech eco-cities struggle with cost and attracting residents'),
         ('Songdo, South Korea', 'a smart city built from about 2003 on reclaimed land, with sensors, pneumatic waste collection and 40% green space', 'smart city design', 'technology-led planning created efficiency but criticism over vitality and cost'),
         ('Paris\'s 15-minute city', 'Mayor Anne Hidalgo promoted the concept from 2020, adding cycle lanes and pedestrianising streets', 'retrofitting an existing city for sustainability', 'redesigning neighbourhoods reduces car dependence and emissions')],
  evaluate=[('Technology is the key to creating sustainable cities.', ['smart grids, sensors and electric transport cut energy and emissions (Songdo, Singapore)', 'data improves service management'], ['low-tech planning, cycling and BRT work well (Curitiba, Copenhagen)', 'social equity and governance matter as much'], 'Technology helps, but planning, governance and people\'s behaviour are more fundamental.'),
            ('Eco-cities offer a realistic model for future urban growth.', ['demonstrate low-carbon design and technologies', 'Vauban and Tianjin show reduced car use and energy'], ['expensive, small-scale and often exclusive (Masdar)', 'most growth is in existing, informal cities in Africa and Asia'], 'Eco-cities are useful experiments, but retrofitting existing cities matters more for global sustainability.')],
  extended=[('Evaluate strategies used to make urban systems more sustainable and resilient.', 'Award: smart, eco and resilient strategies with named cities (Curitiba, Copenhagen, Masdar, Songdo, Rotterdam, Paris); environmental, social, economic dimensions; judgement.', 10, 'long')],
  res=[('Table: modal share of trips to work or study (%) - Copenhagen: bicycle 45, public transport 27, car 21, walk 7; Los Angeles: car 84, public transport 6, walk 3, bicycle 1, other 6.',
        [('Compare the modal shares in the two cities.', 'Copenhagen is dominated by cycling (45%) and public transport, with only 21% by car; Los Angeles is overwhelmingly car-based (84%) with very little cycling (1%).'),
         ('Explain how the differences affect urban sustainability.', 'High cycling and transit reduce emissions, congestion, noise and health costs; car dependence in Los Angeles increases pollution, sprawl and CO₂ per capita.')]),
       ('Text: "Curitiba\'s BRT carries about 1.3 million passengers a day on about 80 km of dedicated lanes, built for a fraction of the cost of a metro." - city transport agency summary.',
        [('Suggest two reasons why BRT may be more suitable than a metro for cities in middle-income countries.', 'Much lower cost per km and faster construction; flexibility to extend routes; can use existing roads.'),
         ('Explain how BRT contributes to sustainability.', 'Reduces car trips, congestion and emissions; provides affordable mobility for low-income residents; linked to high-density corridors.')])])


# =============================================================================================
# Fieldwork and internal assessment
# =============================================================================================
S('ch14-st1', gens=['spearman', 'stats', 'mapscale'],
  terms=[('fieldwork question', 'a focused, answerable geographical question that guides an investigation and is linked to the syllabus, e.g. "How does channel width change downstream on the River X?"'),
         ('hypothesis', 'a testable statement predicting a relationship between variables, e.g. "Channel width increases with distance downstream"'),
         ('null hypothesis', 'a statement that there is no significant relationship or difference between variables, which statistical tests try to reject'),
         ('geographic context', 'the location and background of the study area, explained with maps and linked to theory'),
         ('variable', 'a measurable characteristic that changes, such as distance from the CBD (independent) or land value (dependent)')],
  facts=[('What is the word limit for the IB DP Geography internal assessment?', '2,500 words', ['1,500 words', '4,000 words', '5,000 words'], 'The IA is a written report based on fieldwork.'),
         ('What percentage of the final grade does the IA count for at HL?', '20%', ['25%', '35%', '10%'], 'It is 25% at SL.'),
         ('Which is the best example of a focused fieldwork question?', 'To what extent does pedestrian density decrease with distance from the peak land value intersection in central Lisbon?', ['What is Lisbon like?', 'Why are cities important?', 'How do all rivers in Europe behave?'], 'It is specific, measurable, located and linked to the urban option.'),
         ('In the IB IA, the fieldwork question must be linked to:', 'the syllabus of the course (a topic from the core or options)', ['any topic of personal interest', 'the extended essay only', 'Theory of Knowledge'], 'The question must relate to the syllabus and be based on primary data.')],
  why=[('Explain why a fieldwork question should be narrow and focused.', 'A focused question can be investigated with primary data within time, word and safety limits, leads to precise hypotheses and allows meaningful analysis and conclusions.'),
       ('Explain why hypotheses should be based on geographical theory.', 'Theory (e.g. Bradshaw model, bid-rent theory) gives expected patterns to test, so results can be explained and anomalies discussed, linking fieldwork to the syllabus.'),
       ('Explain why the geographic context is important in an IA.', 'Maps and background explain where and why the study area is suitable, help the reader understand the results and allow comparisons with theory.'),
       ('Explain why a null hypothesis is used in statistical testing.', 'Statistical tests assess the probability that a pattern occurred by chance; rejecting the null hypothesis at a significance level (e.g. 0.05) gives confidence that a relationship exists.')],
  contrast=[('a hypothesis', 'a null hypothesis', 'A hypothesis predicts a relationship or difference (e.g. land value falls with distance from the CBD); the null hypothesis states there is no significant relationship.'),
            ('independent variables', 'dependent variables', 'The independent variable is the one that changes or is chosen (distance downstream); the dependent variable responds to it (channel width).')],
  misc=[('A good fieldwork question should cover as many topics as possible.', 'A good question is narrow and focused on one relationship or process so it can be investigated in depth within 2,500 words.'),
        ('A hypothesis must be proven correct for the investigation to be successful.', 'Rejecting or partially supporting a hypothesis is equally valid if it is explained and evaluated.'),
        ('Secondary data alone are enough for the IB IA.', 'The IA must be based on primary data collected in the field; secondary data can only support it.')],
  apply=[('Write a hypothesis and null hypothesis for a study of the urban heat island in a named city.', 'e.g. Hypothesis: air temperature in Vienna decreases with distance from the city centre. Null hypothesis: there is no significant relationship between air temperature and distance from the city centre.', 2),
         ('Suggest a suitable fieldwork question for Option A Freshwater and the data needed to answer it.', 'e.g. "How do channel characteristics change downstream on the River Wharfe?" - data: width, depth, velocity, discharge, pebble size and roundness at 8-10 sites at regular intervals.', 3)],
  cases=[('a river study on the River Wharfe, Yorkshire', 'students measured width, depth and velocity at ten sites to test the Bradshaw model', 'how theory informs a fieldwork question', 'the Bradshaw model predicts downstream changes that can be tested with primary data'),
         ('an urban transect in Lisbon', 'students recorded pedestrian counts, building height and land use from the Baixa outward', 'the use of bid-rent theory in fieldwork', 'the theory predicts declining intensity of land use with distance from the CBD'),
         ('a microclimate survey in a school grounds in Geneva', 'temperature, humidity and wind were measured at 15 sites at different times of day', 'linking fieldwork to an urban microclimate topic', 'a small, safe study area allowed repeated measurements to test a focused hypothesis')],
  evaluate=[('The choice of fieldwork question is the most important factor in a successful investigation.', ['a focused, measurable question shapes methods, data and analysis', 'poorly focused questions lead to descriptive reports'], ['data quality, methods and analysis are equally important', 'evaluation and conclusions earn marks too'], 'The question is the foundation, but success depends on the quality of the whole investigation.'),
            ('Hypothesis testing is the best approach to geographical fieldwork.', ['allows statistical analysis and clear conclusions', 'links data to theory'], ['qualitative, exploratory approaches suit perception or cultural topics', 'hypotheses may narrow thinking'], 'Hypothesis testing suits many topics, but qualitative and mixed approaches are also valid.')],
  extended=[('Explain how a fieldwork question and hypotheses should be developed for an IB Geography internal assessment.', 'Award: link to syllabus; focus and feasibility; geographic context; theory-based hypotheses and null hypothesis; variables; ethics and safety considerations.', 6, 'multi_step')],
  res=[('Student plan: "Question - How does land use change along a 3 km transect from the CBD of Kuala Lumpur? Hypothesis 1 - the percentage of commercial land use decreases with distance from the CBD. Hypothesis 2 - building height decreases with distance. Sites every 300 m."',
        [('Calculate the number of sampling sites if the first site is at 0 km.', '3,000 m ÷ 300 m = 10 intervals + 1 = 11 sites'),
         ('Suggest one improvement to the student\'s plan.', 'Use a stratified or random sample along several transects, define land-use categories clearly, or add a null hypothesis and a planned statistical test (Spearman\'s rank).')]),
       ('Table of possible fieldwork questions - A: "Is tourism good?"; B: "How does infiltration rate vary with land use in the Kranji catchment, Singapore?"; C: "What is the weather like in Asia?"',
        [('Identify the most suitable question and justify your choice.', 'B - it is focused, located, measurable with primary data and linked to Option A (drainage basin flows).'),
         ('Explain why A and C are unsuitable.', 'A is vague and value-laden; C is far too broad to study with primary data and has no clear variables.')])])

S('ch14-st2', gens=['sampling', 'discharge', 'stats', 'nni', 'gradient'],
  terms=[('random sampling', 'a sampling method in which every member of the population has an equal chance of being selected, e.g. using random number tables to choose grid points'),
         ('systematic sampling', 'selecting samples at regular intervals, e.g. every 50 m along a transect or every 10th household'),
         ('stratified sampling', 'dividing a population into sub-groups (strata) and sampling each in proportion to its size'),
         ('primary data', 'data collected first-hand by the investigator through measurement, observation, questionnaires or interviews'),
         ('pilot study', 'a small-scale trial of methods carried out before the main data collection to test and refine them'),
         ('transect', 'a line along which measurements or observations are taken at intervals to show change across space')],
  facts=[('Which instrument is used to measure river velocity accurately?', 'A flow meter (impeller)', ['A clinometer', 'A quadrat', 'An anemometer'], 'A float method is a cheaper but less accurate alternative.'),
         ('Which sampling method would best ensure that owner-occupiers, private renters and social tenants are all represented in proportion?', 'Stratified sampling', ['Random sampling', 'Systematic sampling', 'Opportunistic sampling'], 'Strata are sampled in proportion to their size.'),
         ('A clinometer is used to measure:', 'slope angle', ['wind speed', 'pebble size', 'soil pH'], 'It is used on beach profiles and valley-side slopes.'),
         ('Which index measures pebble shape by visual comparison with a chart?', 'Powers\' roundness index', ['The Gini coefficient', 'The Bradshaw index', 'The nearest-neighbour index'], 'Pebbles are classified from very angular to well rounded.')],
  why=[('Explain why a pilot study is useful before fieldwork.', 'It tests whether methods, equipment and questionnaires work, identifies problems (ambiguous questions, unsafe sites), estimates time needed and improves reliability of the main data collection.'),
       ('Explain why random sampling reduces bias.', 'Every point or person has an equal chance of selection, so the investigator\'s choices (e.g. picking easy sites) do not influence the sample, making it more representative.'),
       ('Explain why repeated measurements improve the reliability of fieldwork data.', 'Taking several readings (e.g. three velocity measurements at each point) and averaging reduces the effect of random errors and anomalies.'),
       ('Explain why a questionnaire should be carefully designed.', 'Closed questions give comparable data and open questions give depth; neutral wording avoids leading respondents; clear, short questions improve response rates and validity.')],
  contrast=[('random sampling', 'systematic sampling', 'Random sampling selects points by chance so all have equal probability; systematic sampling selects at regular intervals, which is easier and gives good coverage but may miss or over-represent patterns that repeat at the interval.'),
            ('quantitative data', 'qualitative data', 'Quantitative data are numerical measurements (discharge, pedestrian counts); qualitative data are descriptive (interviews, photographs, perceptions).')],
  misc=[('Collecting more data always makes results reliable.', 'Reliability depends on consistent, accurate methods and suitable sampling; large amounts of biased or inaccurate data remain unreliable.'),
        ('Systematic sampling is the same as random sampling.', 'Systematic sampling uses regular intervals; random sampling uses chance selection.'),
        ('A float method gives an exact river velocity.', 'Floats measure surface velocity and are affected by wind and eddies; a correction factor (about 0.8) is often applied.')],
  apply=[('Describe how you would measure the discharge of a small stream.', 'Measure width with a tape; measure depth at equal intervals (e.g. every 0.5 m) with a metre rule and calculate mean depth; measure velocity with a flow meter (or float timed over 10 m, repeated three times); discharge = width × mean depth × velocity.', 4),
         ('Suggest how you would sample beach sediment along a 100 m stretch of coast.', 'Use systematic transects every 20 m from low to high water and select pebbles at fixed intervals along each transect (or random points within quadrats), measuring 10-20 pebbles at each point.', 3)],
  cases=[('a Bradshaw model river study', 'students measured width, depth, velocity, gradient and pebble size at 10 sites spaced systematically along a stream', 'systematic sampling in physical geography', 'regular intervals ensure the whole length is represented and allow downstream trends to be identified'),
         ('a questionnaire survey on regeneration in the London Docklands', 'residents were interviewed using stratified sampling by age group and housing tenure', 'stratified sampling in human geography', 'strata ensure that different groups\' views are represented proportionally'),
         ('an environmental quality survey in central Bogotá', 'students scored litter, noise, greenery and building condition on a bi-polar scale at 20 sites', 'subjective data collection', 'standardised scoring makes qualitative judgements comparable, though bias remains')],
  evaluate=[('Quantitative methods produce better fieldwork data than qualitative methods.', ['measurable, comparable and suitable for statistical testing', 'less influenced by opinion'], ['qualitative data explain perceptions and reasons (interviews)', 'measurements can be inaccurate too'], 'The best investigations combine methods suited to the question.'),
            ('Sampling strategy is the most important influence on the reliability of fieldwork results.', ['a biased sample makes results unrepresentative', 'sample size affects significance'], ['equipment accuracy, timing and weather also matter', 'human error in measurement'], 'Sampling is crucial, but reliability depends on the whole method, including equipment and consistency.')],
  extended=[('Describe and justify the primary data collection methods you would use to investigate how environmental quality changes with distance from a city centre.', 'Award: transects with systematic or stratified sites; bi-polar environmental quality survey; pedestrian/traffic counts; land-use mapping; photographs; timing and repetition; justification of sample size and safety.', 6, 'multi_step')],
  res=[('Field sheet: river width 4.2 m; depths at 0.7 m intervals - 0.12, 0.31, 0.46, 0.52, 0.38, 0.15 m; float travelled 10 m in 18.5 s, 17.9 s and 19.2 s.',
        [('Calculate the mean depth and the mean surface velocity.', f'Mean depth = {sum([0.12, 0.31, 0.46, 0.52, 0.38, 0.15]) / 6:.3f} m; mean time = {(18.5 + 17.9 + 19.2) / 3:.2f} s; velocity = 10/{(18.5 + 17.9 + 19.2) / 3:.2f} = {10 / ((18.5 + 17.9 + 19.2) / 3):.3f} m/s'),
         ('Calculate discharge, applying a correction factor of 0.8 to the float velocity.', f'Q = 4.2 × {sum([0.12, 0.31, 0.46, 0.52, 0.38, 0.15]) / 6:.3f} × ({10 / ((18.5 + 17.9 + 19.2) / 3):.3f} × 0.8) = {4.2 * (sum([0.12, 0.31, 0.46, 0.52, 0.38, 0.15]) / 6) * (10 / ((18.5 + 17.9 + 19.2) / 3) * 0.8):.3f} m³/s')]),
       ('Questionnaire extract - Q1 "Don\'t you agree that the new metro has improved the city?" (yes/no); Q2 "How often do you use the metro?" (daily / weekly / monthly / never); Q3 "What is your age?" (open).',
        [('Identify one problem with Q1 and suggest an improvement.', 'It is a leading question; rewrite neutrally, e.g. "To what extent has the metro changed your journey times? (Likert scale 1-5)".'),
         ('Suggest how Q3 could be improved for analysis.', 'Use age bands (e.g. 16-24, 25-44, 45-64, 65+) so data are easy to group and respondents are more comfortable answering.')])])

S('ch14-st3', gens=['spearman', 'chi', 'stats', 'nni'],
  terms=[('Spearman\'s rank correlation coefficient', 'a statistical test of the strength and direction of a relationship between two sets of ranked data, from −1 to +1: rs = 1 − 6Σd²/(n³ − n)'),
         ('chi-squared test', 'a statistical test comparing observed frequencies with expected frequencies to see whether differences are significant: χ² = Σ(O − E)²/E'),
         ('significance level', 'the probability that a result occurred by chance; 0.05 (95% confidence) is commonly used in geography'),
         ('choropleth map', 'a map that shades areas according to the value of a variable, e.g. population density by district'),
         ('proportional symbol', 'a map symbol whose size is proportional to the value it represents, e.g. circles for city populations'),
         ('interquartile range', 'the difference between the upper and lower quartiles, showing the spread of the middle 50% of data')],
  facts=[('A Spearman\'s rank coefficient of −0.92 indicates:', 'a strong negative correlation', ['a weak positive correlation', 'no correlation', 'a strong positive correlation'], 'As one variable increases, the other decreases.'),
         ('For the chi-squared test, the degrees of freedom for a single row of 4 categories is:', '3', ['4', '5', '2'], 'df = number of categories − 1.'),
         ('Which graph is most appropriate for showing continuous change over time, such as river discharge?', 'A line graph', ['A pie chart', 'A choropleth map', 'A dispersion graph'], 'Line graphs show trends in continuous data.'),
         ('A nearest-neighbour index of 0.2 indicates a pattern that is:', 'clustered', ['random', 'regular', 'linear'], 'Rn ranges from 0 (clustered) through 1.0 (random) to 2.15 (regular).')],
  why=[('Explain why Spearman\'s rank correlation does not prove causation.', 'It measures association between variables, which may be coincidental or caused by a third factor; geographical explanation is needed to establish a causal link.'),
       ('Explain why choropleth maps can be misleading.', 'They assume values are uniform within each area and boundaries are sharp; large areas dominate visually; class intervals chosen can exaggerate or hide patterns.'),
       ('Explain why a sample size of at least 10 is recommended for Spearman\'s rank.', 'With very small samples, a high coefficient can occur by chance and critical values are very high, so results are less likely to be significant and reliable.'),
       ('Explain why the choice of graph matters in data presentation.', 'Appropriate graphs (scatter for relationships, line for trends, bar for categories, maps for spatial patterns) make patterns clear; inappropriate graphs can obscure or mislead.')],
  contrast=[('Spearman\'s rank', 'chi-squared', 'Spearman\'s rank tests the correlation between two ranked continuous variables; chi-squared tests whether observed frequencies in categories differ significantly from expected frequencies.'),
            ('a choropleth map', 'a dot map', 'A choropleth map shades areas by value per area; a dot map places dots representing a fixed quantity to show distribution and density.')],
  misc=[('A Spearman\'s coefficient of 0.6 is always significant.', 'Significance depends on sample size: for n = 8 the one-tailed critical value at 0.05 is 0.643, so 0.6 would not be significant.'),
        ('A significant chi-squared result proves the hypothesis is true.', 'It shows the difference is unlikely to be due to chance at the chosen level, not proof; method and sampling must also be sound.'),
        ('Pie charts are suitable for any data set.', 'Pie charts suit proportions of a whole with few categories; they are poor for trends or many categories.')],
  apply=[('A student finds rs = 0.81 for 10 pairs of data (critical value 0.564 at 0.05, one-tailed). Interpret the result.', 'A strong positive correlation that is significant at the 0.05 level: the null hypothesis can be rejected - there is less than a 5% probability the relationship is due to chance.', 2),
         ('Suggest suitable ways to present data on land use and pedestrian counts along an urban transect.', 'Divided bar charts or a land-use transect diagram for land use; line graph or proportional bars of pedestrian counts against distance; annotated map.', 3)],
  cases=[('a downstream study on the River Dart', 'Spearman\'s rank between distance downstream and channel width gave rs = 0.89 for 10 sites', 'statistical testing in fieldwork', 'a coefficient above the critical value allows the null hypothesis to be rejected'),
         ('a shopper survey in Copenhagen', 'chi-squared tested whether transport mode differed from an equal distribution and gave a significant result', 'the chi-squared test', 'comparing observed and expected frequencies shows whether a pattern is likely to be due to chance'),
         ('a choropleth map of deprivation in Glasgow', 'data zones were shaded by SIMD rank, revealing clusters of deprivation in the east end', 'presenting spatial data', 'shading by area reveals spatial patterns but hides variation within zones')],
  evaluate=[('Statistical tests are the most important part of data analysis in a geographical investigation.', ['objective measure of significance; supports conclusions', 'allow comparison with theory'], ['description and explanation of patterns, anomalies and context are essential', 'tests depend on valid data and appropriate choice'], 'Statistics strengthen analysis, but geographical interpretation is what gives results meaning.'),
            ('Maps are more effective than graphs for presenting fieldwork data.', ['show spatial patterns and location', 'combine with photographs and annotations'], ['graphs show relationships and trends more precisely', 'maps can be cluttered'], 'Both are needed; the best choice depends on whether the focus is spatial pattern or relationship.')],
  extended=[('Explain how you would analyse and present data to test the hypothesis that land value decreases with distance from the CBD.', 'Award: scatter graph with line of best fit; Spearman\'s rank with null hypothesis and significance; map of sites; description of pattern and anomalies; link to bid-rent theory.', 6, 'multi_step')],
  res=[('Data for six sites: distance from CBD (km) 0.5, 1.0, 1.5, 2.0, 2.5, 3.0; pedestrian count 210, 175, 180, 90, 60, 25.',
        [('Calculate Spearman\'s rank correlation coefficient (rank 1 = highest).', 'Distance ranks 6,5,4,3,2,1; count ranks 1,3,2,4,5,6; d = 5,2,2,−1,−3,−5; Σd² = 68; rs = 1 − 6×68/(216 − 6) = 1 − 408/210 = −0.943'),
         ('Interpret the result (critical value for n = 6 at 0.05, one-tailed: 0.829).', 'Strong negative correlation, significant at 0.05 (|−0.943| > 0.829): pedestrian counts decrease with distance from the CBD, consistent with bid-rent theory.')]),
       ('Observed land use at 40 random points: residential 18, commercial 9, industrial 5, open space 8. Null hypothesis: all categories are equally common (E = 10).',
        [('Calculate the chi-squared value.', 'χ² = (18−10)²/10 + (9−10)²/10 + (5−10)²/10 + (8−10)²/10 = 6.4 + 0.1 + 2.5 + 0.4 = 9.4'),
         ('Interpret the result (df = 3, critical value 7.81 at 0.05).', '9.4 > 7.81, so reject the null hypothesis: land use is not evenly distributed; residential use is more common than expected.')])])

S('ch14-st4', gens=['stats', 'sampling'],
  terms=[('risk assessment', 'identifying hazards in fieldwork, assessing their likelihood and severity, and planning measures to reduce them'),
         ('ethical fieldwork', 'fieldwork that respects people, property and the environment, with informed consent, anonymity and minimal disturbance'),
         ('reliability', 'the extent to which a method gives consistent results when repeated under the same conditions'),
         ('validity', 'the extent to which data and methods actually measure what the investigation intends to measure'),
         ('accuracy', 'how close a measurement is to the true value'),
         ('informed consent', 'agreement to take part in research given by people who understand its purpose and how their data will be used')],
  facts=[('Which is an example of an ethical consideration in a questionnaire survey?', 'Obtaining informed consent and keeping responses anonymous', ['Interviewing only friends', 'Asking leading questions', 'Recording names and addresses without permission'], 'Respondents must understand and agree, and data must be protected.'),
         ('Which is the most appropriate control measure for river fieldwork?', 'Working in pairs, wearing wellingtons, avoiding deep or fast water and checking weather forecasts', ['Working alone to avoid disturbance', 'Wading into deep water to measure the thalweg', 'Doing fieldwork during floods for interesting data'], 'Risk assessment reduces likelihood and severity of hazards.'),
         ('Measuring velocity three times at each point and averaging mainly improves:', 'reliability', ['ethics', 'the fieldwork question', 'the word count'], 'Repetition reduces random error.')],
  why=[('Explain why a risk assessment is needed before fieldwork.', 'It identifies hazards (deep water, traffic, weather, uneven ground, unfriendly encounters), evaluates their likelihood and severity and sets control measures, protecting students and meeting school requirements.'),
       ('Explain why evaluating methods is an important part of a fieldwork report.', 'It shows understanding of limitations (sampling, equipment, timing, human error), how they affected reliability and validity of conclusions, and how the investigation could be improved or extended.'),
       ('Explain how the timing of data collection can affect fieldwork results.', 'Pedestrian counts vary by time of day and day of week; river discharge varies after rain; temperature varies with time of day - so inconsistent timing introduces bias.'),
       ('Explain why environmental impact should be minimised in fieldwork.', 'Trampling, removing pebbles or plants and disturbing wildlife damage sites and affect future studies; responsible practice follows codes such as "leave no trace".')],
  contrast=[('reliability', 'validity', 'Reliability is about consistency of results when repeated; validity is whether the method measures what it claims to and answers the question.'),
            ('accuracy', 'precision', 'Accuracy is closeness to the true value; precision is the level of detail and consistency of repeated measurements - a measurement can be precise but inaccurate.')],
  misc=[('An investigation with unexpected results has failed.', 'Unexpected results are valuable if explained and evaluated; they may reveal local factors or method limitations.'),
        ('Ethical issues only apply to human geography fieldwork.', 'Physical fieldwork also has ethical issues: access to private land, environmental damage and safety of participants.'),
        ('A risk assessment removes all risks from fieldwork.', 'It reduces risks to acceptable levels with control measures; some residual risk remains.')],
  apply=[('Identify two hazards and their control measures for an urban fieldwork survey.', 'Traffic - stay on pavements and cross at designated crossings; personal safety - work in groups, carry a phone, stay in public areas; weather - suitable clothing and sun protection.', 2),
         ('Suggest two limitations of a pedestrian count carried out on one weekday afternoon and how they could be addressed.', 'Not representative of other times/days - repeat counts at different times and days; short count period (5 min) - extend to 10-15 min and average; observer error - use tally counters and two observers.', 4)],
  cases=[('a coastal fieldwork day at Dawlish Warren, Devon', 'groups checked tide times, worked above the strandline and avoided cliffs during a beach profile survey', 'risk assessment', 'identifying tidal and cliff hazards and planning around them kept the survey safe'),
         ('a questionnaire in a regenerated district of Hamburg', 'students gave participants an information sheet, did not record names and allowed them to withdraw', 'ethical practice in human fieldwork', 'informed consent and anonymity protect respondents'),
         ('a river discharge study in the Lake District', 'readings after heavy overnight rain were much higher than those collected on dry days', 'evaluating the reliability of fieldwork data', 'changing conditions between sites reduced the comparability of the results')],
  evaluate=[('The evaluation section is the most important part of a fieldwork investigation.', ['shows critical understanding of limitations', 'suggests improvements and extensions'], ['without good data and analysis there is little to evaluate', 'analysis carries more marks in the IA'], 'Evaluation is essential but depends on strong data collection and analysis.'),
            ('Ethical and safety considerations limit the quality of geographical fieldwork.', ['restrict sites (deep water, private land) and timing', 'anonymity limits follow-up'], ['ethical practice improves trust and response rates', 'safe methods are more consistent'], 'They impose some constraints but ultimately support valid, reliable fieldwork.')],
  extended=[('Evaluate the methods used in a geographical fieldwork investigation you have studied or carried out.', 'Award: sampling, equipment, timing, sample size, human error; impact on reliability and validity; ethical/safety constraints; specific improvements and extensions; judgement on confidence in conclusions.', 6, 'multi_step')],
  res=[('Repeat measurements of velocity (m/s) at one point - student A: 0.42, 0.45, 0.43; student B: 0.31, 0.52, 0.47.',
        [('Calculate the mean and range for each student.', f'A: mean {(0.42 + 0.45 + 0.43) / 3:.3f}, range 0.03; B: mean {(0.31 + 0.52 + 0.47) / 3:.3f}, range 0.21'),
         ('Comment on the reliability of the two sets of measurements.', 'A\'s readings are consistent (small range), so more reliable; B\'s large range suggests inconsistent technique (e.g. impeller not held at 40% depth or facing upstream).')]),
       ('Risk assessment table - Hazard: slippery rocks in stream (likelihood medium, severity medium); Hazard: road crossing (likelihood low, severity high); Hazard: sudden rise in water level (likelihood low, severity high).',
        [('Suggest a control measure for each hazard.', 'Slippery rocks - wear boots with grip, avoid rocks, work in pairs; road - cross at designated crossing with supervision; water rise - check forecast, stop if water rises, stay near the bank.'),
         ('Explain why hazards with low likelihood but high severity must be controlled.', 'Even if unlikely, consequences such as drowning or a road accident would be catastrophic, so precautions are essential.')])])
