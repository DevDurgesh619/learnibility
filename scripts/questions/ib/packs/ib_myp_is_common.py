"""Shared builders for the IB MYP Individuals and Societies packs: ib-g8-social-science (MYP 3),
ib-g9-social-science (MYP 4) and ib-g10-social-science (MYP 5).

MYP I&S is assessed on four criteria (each 0-8): A knowing and understanding, B investigating,
C communicating, D thinking critically. There is no external exam before the optional MYP 5
eAssessment (2 h on-screen: source engagement, investigation and extended-response tasks).

Kit(R, year) wraps one pack's Registry:
  K.st(key, topic, src=[...], rq=[...], **F-fields)   one subtopic: an F fact pack (criterion A/C/D items through
                                                      fact_templates) plus
     src  attributed (paraphrased) sources -> criterion D items: message, origin/purpose/value/limitation,
          source + own-knowledge evaluation (style 'source')
     rq   research questions -> criterion B items: refine a weak question, justify relevance, action plan,
          pick the focused question (style 'inquiry')
     why / evaluate content also feeds criterion C items: PEEL paragraph, plan an extended response (style 'comm')
Parametric generators (computed answers): density, pct_change, natural_increase, pop_change, scale, gridref,
longitude_time, climate, discharge, quake, chronology, supply_demand, opp_cost, budget, interest, trade,
exchange, dependency, per_capita, hdi, electoral, footprint, rate_of_change.
mock(year) gives the eAssessment-style mock: 15 items, 80 marks.
"""
from __future__ import annotations

import math

from _common import F, Registry, T, mcq, name, two_names  # noqa: F401

# ---------------------------------------------------------------------------------------------------------------
# Criteria language
# ---------------------------------------------------------------------------------------------------------------
CRIT_D = {
    3: ('MYP I&S criterion D (year 3), scaled to the marks: 7-8 thoroughly analyses concepts and issues, summarises '
        'information to make valid, well-supported arguments, analyses a range of sources in terms of origin and purpose '
        'recognising value and limitations, and clearly recognises different perspectives and their implications; '
        '5-6 substantial; 3-4 adequate, partly descriptive; 1-2 limited, mostly assertion.'),
    4: ('MYP I&S criterion D (year 4), scaled to the marks: 7-8 discusses concepts, issues and theories in detail, '
        'synthesises information to make valid, well-supported arguments, analyses and evaluates a range of sources in '
        'terms of origin and purpose, examining value and limitations, and interprets different perspectives and their '
        'implications; 5-6 substantial; 3-4 adequate, partly descriptive; 1-2 limited, mostly assertion.'),
    5: ('MYP I&S criterion D (year 5), scaled to the marks: 7-8 thoroughly discusses concepts, issues, models and '
        'theories, synthesises information to make valid, well-supported arguments, effectively analyses and evaluates a '
        'wide range of sources in terms of origin and purpose, examining value and limitations, and thoroughly interprets '
        'a range of perspectives and their implications; 5-6 substantial; 3-4 adequate; 1-2 limited.'),
}
CRIT_C = ('Criterion C (communicating): appropriate style and register for the purpose, a clear structure suited to the '
          'format (topic sentence, developed evidence, explanation, link back to the question), accurate subject '
          'terminology, and sources documented with a recognised convention (MLA or APA).')
CRIT_B = ('Criterion B (investigating): a clear, focused research question whose relevance is justified, a realistic '
          'action plan, appropriate and varied methods/sources, and reflection on the process.')
LETTERS = 'ABCD'


def lc(s: str) -> str:
    w = s.split(' ', 1)[0]
    if w in {'The', 'A', 'An', 'How', 'Why', 'What', 'It', 'This', 'There', 'Its', 'Their', 'In', 'Most', 'Many'}:
        return s[0].lower() + s[1:]
    return s


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def mock(year: int) -> list:
    """eAssessment-style paper: 3 tasks, 15 items, 80 marks (2 hours on screen = 1.5 min per mark)."""
    lo = {3: 0, 4: 1, 5: 1}[year]
    hi = {3: 0, 4: 0, 5: 1}[year]
    return [
        dict(section='Task 1 – Knowing and understanding: terminology and content (criterion A)', count=3, c=['C1'],
             d=[1 + lo, 2], type='mcq', marks=1),
        dict(section='Task 1 – Knowing and understanding: explain with examples (criterion A)', count=3, c=['C2'],
             d=[2 + lo, 3], type='explain', marks=4),
        dict(section='Task 1 – Source engagement: message, origin, purpose, value and limitation (criterion D)', count=3,
             c=['C3', 'C3', 'C4'], d=[3, 3 + hi], type='case', marks=5, style='source'),
        dict(section='Task 2 – Investigating: research question and action plan (criterion B)', count=2, c=['C3', 'C4'],
             d=[3, 4], type='multi_step', marks=7, style='inquiry'),
        dict(section='Task 2 – Communicating: structured response (criterion C)', count=2, c=['C3'], d=[3, 3 + hi],
             type='explain', marks=6, style='comm'),
        dict(section='Task 3 – Extended response (criteria C and D)', count=2, c=['C4'], d=[4, 4 + hi], type='long',
             marks=12),
    ]


def style(year: int) -> dict:
    return {'eval_marks': 8, 'essay_marks': 12, 'markband': CRIT_D[year]}


# ---------------------------------------------------------------------------------------------------------------
# Kit
# ---------------------------------------------------------------------------------------------------------------
class Kit:
    def __init__(self, R: Registry, year: int, discipline='history'):
        self.R = R
        self.year = year
        self.weak: dict[str, list] = {}

    def add(self, key, c, d, fn, type='short', style=None):
        self.R.t.setdefault(key, []).append(T(c, d, fn, type, style, fn.__name__))

    def st(self, key, topic, src=(), rq=(), **kw):
        f = F(**kw)
        self.R.facts(key, f)
        ch = key.split('-')[0]
        for r in rq:
            self.weak.setdefault(ch, []).append(r[1])
        if src:
            self._sources(key, topic, list(src), f)
        if rq:
            self._inquiry(key, topic, list(rq), ch)
        self._comm(key, topic, f)
        return f

    # ---- criterion D: sources -------------------------------------------------------------------------------
    def _sources(self, key, topic, src, f):
        """src item: (kind, text, origin, purpose, value, limitation, message)."""
        yr = self.year

        def block(lab, s):
            return f'Source {lab} – {s[0]}: {s[2]}\n\n{s[1]}'

        def message(rng, slot):
            s = rng.choice(src)
            lab = 'A'
            m = slot.marks or (2 if slot.d <= 2 else 3)
            q = rng.choice([
                f'What is the message of Source {lab} about {topic}? Refer to details in the source.',
                f'Identify two points that Source {lab} makes about {topic}, using evidence from the source.',
                f'According to Source {lab}, what can we learn about {topic}? Support your answer with details from the source.',
                f'Outline the main argument or view that Source {lab} presents, quoting or referring to the source.',
            ])
            return dict(stem=block(lab, s) + '\n\n' + q, answer=s[6], type='case', marks=m,
                        markingKey=f'{s[6]} Award 1 mark per relevant point drawn from the source, up to [{m}]; own '
                                   'knowledge is not credited here. Criterion D: interpreting a source.', gap='G7')
        self.add(key, 'C3', (1, 4), message, 'case', 'source')

        def opvl(rng, slot):
            s = rng.choice(src)
            lab = 'A'
            m = slot.marks or (3 if slot.d <= 3 else 4)
            q = rng.choice([
                f'With reference to its origin and purpose, analyse the value and limitations of Source {lab} for a student investigating {topic}.',
                f'Evaluate Source {lab} as evidence about {topic}. Consider its origin, purpose, value and limitations.',
                f'Explain one value and one limitation of Source {lab} for an investigation into {topic}, referring to its origin and purpose.',
                f'How reliable is Source {lab} for someone researching {topic}? Justify your answer using its origin and purpose.',
            ])
            ans = (f'Origin: {s[2]}. Purpose: {s[3]}. Value: {s[4]} Limitation: {s[5]}')
            return dict(stem=block(lab, s) + '\n\n' + q, answer=ans, type='case', marks=m,
                        markingKey=f'{ans} Award up to [{m}]: origin and purpose identified and USED (not just copied), '
                                   'at least one value and one limitation explicitly linked to them. Reliability is judged '
                                   'for a purpose, not as "biased = useless". ' + CRIT_D[yr], gap='G5')
        self.add(key, ('C3', 'C4'), (2, 5), opvl, 'case', 'source')

        if f.evaluate:
            def synth(rng, slot):
                s = rng.choice(src)
                claim, pro, con, judge = rng.choice(f.evaluate)
                lab = 'A'
                m = slot.marks or (6 if slot.d <= 4 else 8)
                q = rng.choice([
                    f'Using Source {lab} and your own knowledge, evaluate the claim that "{claim}"',
                    f'"{claim}" Using Source {lab} and your own knowledge, to what extent do you agree?',
                ])
                key_ = (f'From the source: {s[6]} Own knowledge for: ' + '; '.join(pro) + '. Own knowledge against: ' +
                        '; '.join(con) + f'. Judgement: {judge} Top answers integrate the source with own knowledge and '
                        f'comment on the source\'s origin/purpose. ' + CRIT_D[yr])
                return dict(stem=block(lab, s) + '\n\n' + q, answer=judge, type='long', marks=m, markingKey=key_)
            self.add(key, 'C4', (3, 5), synth, 'long', 'source')

        if len(src) >= 2:
            def purpose_mcq(rng, slot):
                s = rng.choice(src)
                others = [o[3] for o in src if o is not s]
                wrong = others + ['to give a neutral statistical summary with no point of view',
                                  'to entertain readers with an invented story',
                                  'to advertise a product to consumers']
                lab = 'A'
                return mcq(rng, block(lab, s) + f'\n\nWhich of the following best describes the most likely purpose of Source {lab}?',
                           cap(s[3]), [cap(w) for w in wrong[:3]], f'Its origin ({s[2]}) suggests the purpose was {s[3]}.')
            self.add(key, 'C3', (1, 3), purpose_mcq, 'mcq', 'source')

    # ---- criterion B: investigating ------------------------------------------------------------------------
    def _inquiry(self, key, topic, rqs, ch):
        """rq item: (focused RQ, weak RQ, why weak, relevance, action plan / sources)."""

        def refine(rng, slot):
            good, weak, why, rel, plan = rng.choice(rqs)
            m = slot.marks or (3 if slot.d <= 3 else 4)
            who = name(rng)
            stem = rng.choice([
                f'{who} is investigating {topic} and proposes the research question: "{weak}" Explain one weakness of this research question and write a more focused alternative.',
                f'Evaluate the research question "{weak}" for an MYP Individuals and Societies investigation into {topic}. Rewrite it so that it is clear, focused and researchable.',
                f'A class brainstorm on {topic} produced the question "{weak}" Explain why it needs refining, then suggest an improved research question and justify your change.',
            ])
            return dict(stem=stem, answer=f'Weakness: {why} Improved: "{good}"', type='multi_step', marks=m,
                        markingKey=f'1 mark: weakness identified ({why}); 1-2 marks: a focused question such as "{good}" '
                                   '(clear scope – place, period or group – and open, researchable wording); 1 mark: '
                                   'justification of the change. ' + CRIT_B, gap='G5')
        self.add(key, ('C3', 'C4'), (2, 5), refine, 'multi_step', 'inquiry')

        def justify(rng, slot):
            good, weak, why, rel, plan = rng.choice(rqs)
            m = slot.marks or (2 if slot.d <= 2 else 3)
            stem = rng.choice([
                f'Justify the relevance of the research question "{good}"',
                f'Explain why "{good}" is a suitable research question for an MYP investigation into {topic}.',
                f'A student chose the research question "{good}" Explain two reasons why this question is relevant and worth investigating.',
            ])
            return dict(stem=stem, answer=rel, type='explain', marks=m,
                        markingKey=f'{rel} Award marks for relevance to the unit\'s concepts or global context, and for '
                                   'showing the question is focused and can be answered with available sources. ' + CRIT_B)
        self.add(key, 'C3', (1, 4), justify, 'explain', 'inquiry')

        def plan_(rng, slot):
            good, weak, why, rel, plan = rng.choice(rqs)
            m = slot.marks or (4 if slot.d <= 3 else 6)
            stem = rng.choice([
                f'Formulate an action plan to investigate the research question "{good}" Include the main steps, at least one primary and one secondary source, and how you would record your findings.',
                f'Describe the research methods you would use to answer "{good}", naming specific sources and explaining why each is appropriate.',
                f'You have three weeks to investigate "{good}" Outline a step-by-step plan, the sources you would use and one way you would evaluate your process at the end.',
            ])
            return dict(stem=stem, answer=plan, type='multi_step', marks=m,
                        markingKey=f'Indicative plan: {plan} Credit: logical sequence of steps with a timeline; varied, '
                                   'appropriate sources (primary and secondary) named specifically; a method for recording '
                                   'and citing information (e.g. a source log in MLA/APA); a step for evaluating the '
                                   'process and results. ' + CRIT_B, gap='G5')
        self.add(key, ('C3', 'C4'), (2, 5), plan_, 'multi_step', 'inquiry')

        def rq_mcq(rng, slot):
            good, weak, *_ = rng.choice(rqs)
            pool = [w for w in self.weak.get(ch, []) if w != weak]
            rng.shuffle(pool)
            wrong = [weak] + pool[:2]
            if len(wrong) < 3:
                wrong.append(f'Is {topic} important?')
            return mcq(rng, f'Which of the following is the most clear and focused research question for an investigation into {topic}?',
                       good, wrong, 'It is open, has a clear scope (place/period/group) and can be answered with evidence; the others are too broad, closed or off-topic.')
        self.add(key, 'C3', (1, 3), rq_mcq, 'mcq', 'inquiry')

    # ---- criterion C: communicating --------------------------------------------------------------------------
    def _comm(self, key, topic, f):
        if f.why:
            def peel(rng, slot):
                q, a = rng.choice(f.why)
                m = slot.marks or (3 if slot.d <= 3 else 4)
                stem = rng.choice([
                    f'Write one well-structured paragraph (Point, Evidence, Explanation, Link) in answer to this question: {q}',
                    f'Using accurate subject terminology and at least one specific example, write a structured paragraph that responds to: {q}',
                ])
                return dict(stem=stem, answer=a, type='explain', marks=m,
                            markingKey=f'Content: {a} Structure: a clear point that answers the question, specific '
                                       f'evidence, explanation that links evidence to the point, and a closing link. {CRIT_C}', gap='G7')
            self.add(key, 'C3', (2, 4), peel, 'explain', 'comm')

        if f.evaluate:
            def plan_essay(rng, slot):
                claim, pro, con, judge = rng.choice(f.evaluate)
                m = slot.marks or (6 if slot.d <= 4 else 8)
                stem = rng.choice([
                    f'Plan an extended response to the question: "{claim}" To what extent do you agree? Give a thesis, two arguments with specific evidence, a counter-argument and a conclusion.',
                    f'Write the introduction and an outline of the body paragraphs for an essay that evaluates the view that "{claim}"',
                ])
                return dict(stem=stem, answer=f'Thesis: {judge}', type='long', marks=m,
                            markingKey='Arguments for: ' + '; '.join(pro) + '. Counter-arguments: ' + '; '.join(con) +
                                       f'. Thesis/conclusion: {judge} Credit a thesis that answers the question, logically '
                                       f'ordered paragraphs each with specific evidence, a counter-argument that is weighed, and '
                                       f'a conclusion that follows. {CRIT_C}')
            self.add(key, 'C4', (3, 5), plan_essay, 'long', 'comm')

            def compare_view(rng, slot):
                claim, pro, con, judge = rng.choice(f.evaluate)
                a, b = two_names(rng)
                m = slot.marks or 4
                stem = (f'{a} argues that "{claim}" {b} disagrees. Explain one piece of evidence each student could use, '
                        'and state which view you find more convincing and why.')
                return dict(stem=stem, answer=judge, type='explain', marks=m,
                            markingKey=f'{a}: {pro[0]}. {b}: {con[0]}. Judgement (1-2 marks): {judge}', gap='G5')
            self.add(key, 'C3', (3, 4), compare_view, 'explain', 'comm')


# ---------------------------------------------------------------------------------------------------------------
# Number helpers
# ---------------------------------------------------------------------------------------------------------------
def n0(x):
    return f'{x:,.0f}'


def nd(x, dp=1):
    s = f'{x:,.{dp}f}'
    return s


def sgn(x, dp=1):
    return ('+' if x > 0 else '−' if x < 0 else '') + f'{abs(x):,.{dp}f}'


def _distinct(correct, cands, n=3):
    out = []
    for c in cands:
        if c != correct and c not in out:
            out.append(c)
    return out[:n] if len(out) >= n else None


# ---------------------------------------------------------------------------------------------------------------
# Real data tables (approximate; labelled as estimates in stems)
# ---------------------------------------------------------------------------------------------------------------
# (country, population 2023 est., area km²)
PLACES = [
    ('Bangladesh', 171_500_000, 148_460), ('the Netherlands', 17_900_000, 41_850), ('Australia', 26_600_000, 7_692_024),
    ('Canada', 40_100_000, 9_984_670), ('Japan', 124_500_000, 377_975), ('India', 1_428_600_000, 3_287_263),
    ('Nigeria', 223_800_000, 923_768), ('Brazil', 216_400_000, 8_515_767), ('Egypt', 112_700_000, 1_001_450),
    ('Mongolia', 3_400_000, 1_564_116), ('Singapore', 5_900_000, 735), ('Iceland', 390_000, 103_000),
    ('Rwanda', 14_100_000, 26_338), ('Germany', 84_500_000, 357_592), ('the United Kingdom', 68_300_000, 243_610),
    ('Kenya', 55_100_000, 580_367), ('Peru', 34_400_000, 1_285_216), ('Indonesia', 277_500_000, 1_904_569),
    ('Argentina', 46_700_000, 2_780_400), ('South Korea', 51_700_000, 100_210),
]
# (country, crude birth rate, crude death rate) per 1000, approx. early 2020s
RATES = [
    ('Niger', 44, 8), ('Japan', 6.3, 12.9), ('India', 16.4, 7.4), ('Germany', 8.8, 12.3), ('Nigeria', 36, 12),
    ('Brazil', 12.4, 7.0), ('the United Kingdom', 10.0, 9.4), ('Bangladesh', 17.5, 5.5), ('Kenya', 27, 5),
    ('China', 6.4, 7.9), ('Italy', 6.7, 12.1), ('Ethiopia', 32, 6), ('Mexico', 15, 7), ('South Korea', 4.5, 7.3),
]
# (country, % aged 0-14, % aged 15-64, % aged 65+), approx. 2023
AGES = [
    ('Japan', 11.6, 59.3, 29.1), ('Niger', 49.5, 47.9, 2.6), ('India', 25.0, 68.0, 7.0), ('Germany', 14.0, 63.6, 22.4),
    ('Nigeria', 43.0, 54.0, 3.0), ('the United Kingdom', 17.5, 63.5, 19.0), ('Brazil', 20.0, 69.9, 10.1),
    ('Italy', 12.4, 63.4, 24.2), ('Uganda', 45.0, 53.0, 2.0), ('China', 16.5, 69.2, 14.3),
]
# Climate stations: (station, country, monthly mean temperature °C, monthly rainfall mm), long-term approx. averages
STATIONS = [
    ('Manaus', 'Brazil', [26.6, 26.5, 26.6, 26.7, 27.0, 27.1, 27.3, 28.0, 28.4, 28.3, 27.9, 27.2],
     [260, 290, 330, 300, 260, 115, 90, 70, 80, 110, 160, 220]),
    ('Mumbai', 'India', [24, 25, 27, 28, 30, 29, 28, 27, 28, 28, 27, 25], [1, 1, 0, 1, 11, 537, 830, 500, 326, 62, 15, 6]),
    ('London', 'United Kingdom', [5, 5, 7, 9, 13, 16, 18, 18, 15, 12, 8, 6], [55, 40, 42, 44, 49, 45, 45, 50, 49, 69, 59, 55]),
    ('Cairo', 'Egypt', [14, 15, 18, 21, 25, 27, 28, 28, 26, 24, 19, 15], [5, 4, 3, 1, 0, 0, 0, 0, 0, 1, 3, 6]),
    ('Moscow', 'Russia', [-6, -6, -1, 6, 13, 17, 19, 17, 11, 5, -1, -5], [53, 44, 39, 37, 61, 78, 84, 78, 66, 70, 52, 51]),
    ('Singapore', 'Singapore', [26.5, 27, 27.5, 28, 28.5, 28.5, 28, 28, 27.5, 27.5, 27, 26.5],
     [240, 160, 185, 180, 170, 130, 160, 175, 170, 195, 255, 290]),
    ('Darwin', 'Australia', [28.5, 28.5, 28.5, 28, 26.5, 25, 24.5, 25.5, 27.5, 29, 29.5, 29],
     [420, 375, 315, 100, 20, 1, 1, 5, 15, 70, 140, 250]),
    ('Reykjavik', 'Iceland', [0, 0, 1, 3, 7, 10, 12, 11, 8, 4, 1, 0], [76, 72, 82, 58, 44, 50, 52, 62, 67, 86, 73, 79]),
    ('Nairobi', 'Kenya', [19, 20, 20, 19, 18, 17, 16, 16, 18, 19, 18, 18], [60, 55, 120, 210, 150, 40, 15, 25, 30, 55, 150, 100]),
    ('Riyadh', 'Saudi Arabia', [14, 17, 21, 26, 32, 35, 36, 36, 33, 27, 20, 15], [14, 8, 23, 25, 9, 0, 0, 0, 0, 1, 7, 13]),
]
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# (city, longitude in degrees; east positive)
LONGS = [('London', 0), ('Cairo', 31), ('Mumbai', 73), ('Tokyo', 140), ('New York', -74), ('Lima', -77), ('Sydney', 151),
         ('Nairobi', 37), ('Mexico City', -99), ('Jakarta', 107), ('Rio de Janeiro', -43), ('Moscow', 38), ('Beijing', 116),
         ('Lagos', 3), ('Los Angeles', -118), ('Dhaka', 90)]
# (country, CO2 emissions Mt 2022 approx, population millions)
CO2 = [('China', 11_400, 1_412), ('the United States', 5_060, 333), ('India', 2_830, 1_417), ('Germany', 666, 84),
       ('the United Kingdom', 320, 67), ('Brazil', 480, 215), ('Nigeria', 130, 219), ('Japan', 1_050, 125),
       ('Australia', 390, 26), ('Kenya', 22, 54), ('Saudi Arabia', 690, 36), ('France', 300, 68)]


def _lon(v):
    return f'{abs(v)}°{"E" if v > 0 else "W"}' if v else '0° (Greenwich meridian)'


# ---------------------------------------------------------------------------------------------------------------
# Parametric generators (each registers one or more templates on key)
# ---------------------------------------------------------------------------------------------------------------
def density(K, key, c='C3', d=(1, 4)):
    def dens(rng, slot):
        p, pop, area = rng.choice(PLACES)
        v = pop / area
        ans = f'{v:,.0f} people per km²' if v >= 10 else f'{v:.1f} people per km²'
        fr = rng.randrange(3)
        if fr == 0:
            stem = f'In 2023 {p} had an estimated population of {n0(pop)} and an area of {n0(area)} km². Calculate its population density.'
        elif fr == 1:
            stem = f'Using the data below, calculate the population density of {p}.\nPopulation (2023 estimate): {n0(pop)}\nArea: {n0(area)} km²'
        else:
            stem = f'A geography student finds that {p} covers {n0(area)} km² and had about {f"{pop / 1e6:g} million" if pop >= 1e6 else n0(pop)} people in 2023. Work out the number of people per square kilometre and show your method.'
        return dict(stem=stem, answer=ans, type='numerical', marks=2,
                    markingKey=f'Density = population ÷ area (M1) = {n0(pop)} ÷ {n0(area)} = {ans} (A1). Units required.', gap='G3')
    K.add(key, c, d, dens, 'numerical')

    def dens_cmp(rng, slot):
        (p1, a1, b1), (p2, a2, b2) = rng.sample(PLACES, 2)
        d1, d2 = a1 / b1, a2 / b2
        hi, lo = (p1, p2) if d1 > d2 else (p2, p1)
        ratio = max(d1, d2) / min(d1, d2)
        stem = (f'2023 estimates: {p1} – population {n0(a1)}, area {n0(b1)} km²; {p2} – population {n0(a2)}, area {n0(b2)} km². '
                f'Calculate the population density of each country and state how many times more densely populated {hi} is than {lo}.')
        ans = f'{p1}: {d1:,.1f} /km²; {p2}: {d2:,.1f} /km²; {hi} is about {ratio:,.1f} times as dense.'
        return dict(stem=stem, answer=ans, type='numerical', marks=4,
                    markingKey=f'M1 density = population ÷ area for each; A1 {d1:,.1f}; A1 {d2:,.1f}; A1 ratio {ratio:,.1f} (allow ±0.2). '
                               'A high national density can hide very uneven distribution.', gap='G3')
    K.add(key, ('C3', 'C4'), (3, 5), dens_cmp, 'numerical')

    def dens_mcq(rng, slot):
        p, pop, area = rng.choice([x for x in PLACES if x[1] / x[2] >= 10])
        v = pop / area
        right = f'{v:,.0f} people per km²'
        wr = _distinct(right, [f'{v * 10:,.0f} people per km²', f'{v / 10:,.0f} people per km²', f'{area / pop * 1000:,.2f} people per km²',
                               f'{v * 2:,.0f} people per km²'])
        if not wr:
            return None
        return mcq(rng, f'{p} has about {n0(pop)} people (2023) living in {n0(area)} km². What is its population density?', right, wr,
                   f'{n0(pop)} ÷ {n0(area)} = {right}.')
    K.add(key, 'C3', (1, 2), dens_mcq, 'mcq')


def pct_change(K, key, series, c='C3', d=(1, 4)):
    """series: (what, unit, year1, v1, year2, v2, source)."""
    def pc(rng, slot):
        what, unit, y1, v1, y2, v2, srcn = rng.choice(series)
        ch = (v2 - v1) / v1 * 100
        fr = rng.randrange(3)
        if fr == 0:
            stem = f'{cap(what)} was {v1:,} {unit} in {y1} and {v2:,} {unit} in {y2} ({srcn}). Calculate the percentage change.'
        elif fr == 1:
            stem = f'Data from {srcn}: {what} – {y1}: {v1:,} {unit}; {y2}: {v2:,} {unit}. By what percentage did it change over the period? Show your working.'
        else:
            yrs = y2 - y1
            ann = ch / yrs
            stem = (f'According to {srcn}, {what} changed from {v1:,} {unit} ({y1}) to {v2:,} {unit} ({y2}). Calculate (a) the percentage change and '
                    f'(b) the average change in {unit} per year.')
            return dict(stem=stem, answer=f'(a) {sgn(ch)}%; (b) {sgn((v2 - v1) / yrs, 2)} {unit} per year',
                        markingKey=f'(a) (new − old) ÷ old × 100 = ({v2:,} − {v1:,}) ÷ {v1:,} × 100 = {sgn(ch)}% (M1 A1). (b) ({v2:,} − {v1:,}) ÷ {yrs} = {sgn((v2 - v1) / yrs, 2)} {unit}/year (A1).',
                        type='numerical', marks=3, gap='G3')
        return dict(stem=stem, answer=f'{sgn(ch)}%', type='numerical', marks=2,
                    markingKey=f'Percentage change = (new − old) ÷ old × 100 (M1) = ({v2:,} − {v1:,}) ÷ {v1:,} × 100 = {sgn(ch)}% (A1). '
                               'Dividing by the new value is a common error.', gap='G3')
    K.add(key, c, d, pc, 'numerical')

    def pc_mcq(rng, slot):
        what, unit, y1, v1, y2, v2, srcn = rng.choice(series)
        ch = (v2 - v1) / v1 * 100
        right = f'{sgn(ch)}%'
        wr = _distinct(right, [f'{sgn((v2 - v1) / v2 * 100)}%', f'{sgn(-ch)}%', f'{sgn(v2 / v1 * 100)}%', f'{sgn(ch / 10)}%'])
        if not wr:
            return None
        return mcq(rng, f'{cap(what)} went from {v1:,} {unit} in {y1} to {v2:,} {unit} in {y2}. Which is the percentage change?', right, wr,
                   f'({v2:,} − {v1:,}) ÷ {v1:,} × 100 = {right}.')
    K.add(key, 'C3', (1, 3), pc_mcq, 'mcq')


def natural_increase(K, key, c='C3', d=(1, 4)):
    def ni(rng, slot):
        co, b, dr = rng.choice(RATES)
        r = (b - dr) / 10
        fr = rng.randrange(3)
        if fr == 0:
            stem = f'{cap(co)} has a crude birth rate of about {b} per 1000 and a crude death rate of about {dr} per 1000 (early 2020s). Calculate its rate of natural increase as a percentage.'
            return dict(stem=stem, answer=f'{sgn(r, 2)}%', type='numerical', marks=2,
                        markingKey=f'NIR = (CBR − CDR) ÷ 10 = ({b} − {dr}) ÷ 10 = {sgn(r, 2)}% (M1 A1). A negative value means natural decrease.', gap='G3')
        if fr == 1 and r > 0.2:
            dt = 70 / r
            stem = f'Using the "rule of 70", estimate how long the population of {co} would take to double if its birth rate ({b} per 1000) and death rate ({dr} per 1000) stayed the same and there were no migration.'
            return dict(stem=stem, answer=f'about {dt:.0f} years', type='numerical', marks=3,
                        markingKey=f'NIR = ({b} − {dr}) ÷ 10 = {r:.2f}% (M1 A1); doubling time ≈ 70 ÷ {r:.2f} ≈ {dt:.0f} years (A1).', gap='G3')
        pop = rng.choice([5, 12, 30, 48, 85, 120]) * 1_000_000
        chg = pop * (b - dr) / 1000
        stem = f'A country of {n0(pop)} people has the same birth rate ({b}‰) and death rate ({dr}‰) as {co}. Ignoring migration, by how many people would its population change in one year?'
        return dict(stem=stem, answer=f'{sgn(chg, 0)} people', type='numerical', marks=2,
                    markingKey=f'Births − deaths = ({b} − {dr}) × {n0(pop)} ÷ 1000 = {sgn(chg, 0)} (M1 A1).', gap='G3')
    K.add(key, c, d, ni, 'numerical')

    def ni_mcq(rng, slot):
        co, b, dr = rng.choice(RATES)
        r = (b - dr) / 10
        right = f'{sgn(r, 2)}%'
        wr = _distinct(right, [f'{sgn(b - dr, 2)}%', f'{sgn((b + dr) / 10, 2)}%', f'{sgn(-r, 2)}%', f'{sgn(r / 10, 2)}%'])
        if not wr:
            return None
        return mcq(rng, f'{cap(co)}: birth rate {b} per 1000, death rate {dr} per 1000. What is the rate of natural increase?', right, wr,
                   f'({b} − {dr}) ÷ 10 = {right}.')
    K.add(key, 'C3', (1, 3), ni_mcq, 'mcq')


def pop_change(K, key, c=('C3', 'C4'), d=(2, 5)):
    def pcg(rng, slot):
        place = rng.choice(['a town in Ontario', 'a district in Kerala', 'a city in northern Italy', 'a region of Kenya',
                            'a suburb of Melbourne', 'a coastal town in Portugal', 'a province of Vietnam'])
        start = rng.randrange(40, 400) * 1000
        b = round(start * rng.uniform(0.006, 0.03))
        de = round(start * rng.uniform(0.005, 0.014))
        im = rng.randrange(1, 60) * 100
        em = rng.randrange(1, 60) * 100
        end = start + b - de + im - em
        ni_ = b - de
        nm = im - em
        stem = (f'In one year the population of {place} started at {n0(start)}. There were {n0(b)} births, {n0(de)} deaths, '
                f'{n0(im)} immigrants and {n0(em)} emigrants. Calculate (a) the natural change, (b) the net migration, '
                f'(c) the population at the end of the year and (d) state which component contributed more to the change.')
        bigger = 'natural change' if abs(ni_) > abs(nm) else 'net migration'
        return dict(stem=stem, answer=f'(a) {sgn(ni_, 0)}; (b) {sgn(nm, 0)}; (c) {n0(end)}; (d) {bigger}', type='multi_step', marks=4,
                    markingKey=f'(a) births − deaths = {sgn(ni_, 0)} (A1); (b) immigrants − emigrants = {sgn(nm, 0)} (A1); '
                               f'(c) {n0(start)} {sgn(ni_, 0)} {sgn(nm, 0)} = {n0(end)} (A1); (d) {bigger} (larger magnitude) (R1).', gap='G3')
    K.add(key, c, d, pcg, 'multi_step')


def scale(K, key, c='C3', d=(1, 4)):
    SC = [10_000, 25_000, 50_000, 100_000, 250_000]

    def sc(rng, slot):
        s = rng.choice(SC if slot.d >= 3 else SC[1:3])
        cm = rng.choice([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7.5, 8, 9.2, 12])
        km = cm * s / 100_000
        fr = rng.randrange(4)
        if fr == 0:
            stem = f'On a map with a scale of 1:{s:,}, two villages are {cm} cm apart. What is the real distance between them in kilometres?'
        elif fr == 1:
            stem = f'A hiking trail measures {cm} cm on a 1:{s:,} topographic map. Calculate the length of the trail on the ground, in km.'
        elif fr == 2:
            stem = f'On a 1:{s:,} map, a straight stretch of river is {cm} cm long. How long is it in reality? Give your answer in metres and kilometres.'
            return dict(stem=stem, answer=f'{km * 1000:,.0f} m = {km:g} km', type='numerical', marks=2,
                        markingKey=f'{cm} cm × {s:,} = {cm * s:,.0f} cm (M1) = {km * 1000:,.0f} m = {km:g} km (A1).', gap='G3')
        else:
            real = km
            stem = f'Two schools are {real:g} km apart. How far apart would they appear on a map with a scale of 1:{s:,}?'
            return dict(stem=stem, answer=f'{cm:g} cm', type='numerical', marks=2,
                        markingKey=f'{real:g} km = {real * 100_000:,.0f} cm (M1); ÷ {s:,} = {cm:g} cm (A1).', gap='G3')
        return dict(stem=stem, answer=f'{km:g} km', type='numerical', marks=2,
                    markingKey=f'Real distance = map distance × scale denominator = {cm} × {s:,} = {cm * s:,.0f} cm (M1) = {km:g} km (A1; 100 000 cm = 1 km).', gap='G3')
    K.add(key, c, d, sc, 'numerical')

    def sc_mcq(rng, slot):
        s = rng.choice([25_000, 50_000])
        cm = rng.choice([2, 3, 4, 6, 8])
        km = cm * s / 100_000
        right = f'{km:g} km'
        wr = _distinct(right, [f'{km * 10:g} km', f'{km / 10:g} km', f'{cm * s / 1000:g} km', f'{km * 2:g} km'])
        return mcq(rng, f'On a 1:{s:,} map, 1 cm represents {s / 100_000:g} km. What real distance is shown by a line {cm} cm long?', right, wr,
                   f'{cm} × {s:,} cm = {right}.')
    K.add(key, 'C3', (1, 2), sc_mcq, 'mcq')

    def sc_area(rng, slot):
        s = rng.choice([25_000, 50_000])
        side = 4 if s == 25_000 else 2
        n = rng.randint(3, 14)
        stem = (f'On a 1:{s:,} Ordnance Survey-style map, grid lines are {side} cm apart. A lake covers about {n} grid squares. '
                'Estimate the area of the lake in km² and explain your method.')
        return dict(stem=stem, answer=f'about {n} km²', type='numerical', marks=3,
                    markingKey=f'{side} cm × {s:,} = {side * s:,} cm = 1 km, so each grid square is 1 km × 1 km = 1 km² (M1 R1); {n} squares ≈ {n} km² (A1). Partly-filled squares counted as halves.', gap='G3')
    K.add(key, ('C3', 'C4'), (3, 5), sc_area, 'numerical')


def gridref(K, key, c='C3', d=(1, 4)):
    FEAT = ['a church with a tower', 'a youth hostel', 'a railway station', 'a trig point (triangulation pillar)', 'a bridge over the river',
            'a campsite', 'a post office', 'a windmill', 'a lighthouse', 'a car park']

    def gr(rng, slot):
        e, n = rng.randint(10, 88), rng.randint(10, 88)
        te, tn = rng.randint(1, 9), rng.randint(1, 9)
        f = rng.choice(FEAT)
        if slot.d <= 2 and rng.random() < 0.5:
            stem = f'{cap(f)} lies in the grid square whose bottom-left corner is where easting {e} meets northing {n}. Give its four-figure grid reference.'
            return dict(stem=stem, answer=f'{e}{n}', type='short', marks=1,
                        markingKey=f'Eastings first ("along the corridor"), then northings ("up the stairs"): {e}{n}.', gap='G3')
        stem = (f'On a topographic map, {f} lies in grid square {e}{n}. It is {te} tenths of the way east across the square and {tn} tenths of the way north. '
                'Give its six-figure grid reference.')
        return dict(stem=stem, answer=f'{e}{te}{n}{tn}', type='short', marks=2,
                    markingKey=f'Easting {e} + {te} tenths = {e}{te}; northing {n} + {tn} tenths = {n}{tn}; six-figure reference {e}{te}{n}{tn} (A2; A1 if eastings and northings reversed in one part only).', gap='G3')
    K.add(key, c, d, gr, 'short')

    def gr_mcq(rng, slot):
        e, n = rng.randint(10, 88), rng.randint(10, 88)
        te, tn = rng.randint(1, 9), rng.randint(1, 9)
        right = f'{e}{n}'
        wr = _distinct(right, [f'{n}{e}', f'{e + 1}{n}', f'{e}{n + 1}', f'{e - 1}{n - 1}'])
        if not wr:
            return None
        return mcq(rng, f'A point has the six-figure grid reference {e}{te}{n}{tn}. In which four-figure grid square does it lie?', right, wr,
                   f'The first two digits ({e}) are the easting and digits 4-5 ({n}) the northing: square {right}.')
    K.add(key, 'C3', (1, 3), gr_mcq, 'mcq')


def longitude_time(K, key, c='C3', d=(2, 4)):
    def lt(rng, slot):
        (a, la), (b, lb) = rng.sample(LONGS, 2)
        diff = abs(la - lb)
        if diff > 180:
            diff = 360 - diff
        h = diff / 15
        hh, mm = int(h), round((h - int(h)) * 60)
        t0 = rng.randint(6, 14)
        east = (lb > la) if abs(la - lb) <= 180 else (lb < la)
        mins = t0 * 60 + (1 if east else -1) * (hh * 60 + mm)
        mins %= 1440
        tt = f'{mins // 60:02d}:{mins % 60:02d}'
        stem = (f'{a} lies at about {_lon(la)} and {b} at about {_lon(lb)}. Using local solar time (the Sun crosses 15° of longitude per hour), '
                f'if it is {t0:02d}:00 local solar time in {a}, what is the local solar time in {b}?')
        return dict(stem=stem, answer=f'{tt} ({b} is {hh} h {mm:02d} min {"ahead" if east else "behind"})', type='numerical', marks=3,
                    markingKey=f'Longitude difference {diff}° (M1); ÷ 15 = {h:.2f} h = {hh} h {mm:02d} min (A1); {b} is {"east so ahead" if east else "west so behind"} → {tt} (A1). '
                               'Official time zones differ from solar time.', gap='G3')
    K.add(key, c, d, lt, 'numerical')

    def lat_dist(rng, slot):
        a, b = sorted(rng.sample(range(-60, 70, 5), 2))
        km = (b - a) * 111
        stem = f'Two places lie on the same line of longitude, one at {abs(a)}°{"S" if a < 0 else "N"} and the other at {abs(b)}°{"S" if b < 0 else "N"}. Given that 1° of latitude is about 111 km, estimate the distance between them.'
        return dict(stem=stem, answer=f'about {km:,} km', type='numerical', marks=2,
                    markingKey=f'Difference in latitude = {b - a}° (crossing the equator adds both values) (M1); × 111 km = {km:,} km (A1).', gap='G3')
    K.add(key, c, d, lat_dist, 'numerical')


def climate(K, key, c='C3', d=(1, 5)):
    def cl(rng, slot):
        stn, co, t, r = rng.choice(STATIONS)
        table = 'Month: ' + ' '.join(m[:3] for m in MONTHS) + '\nTemp (°C): ' + ' '.join(f'{x:g}' for x in t) + '\nRain (mm): ' + ' '.join(str(x) for x in r)
        q = rng.randrange(4 if slot.d <= 2 else 6)
        rng_t = max(t) - min(t)
        tot = sum(r)
        mean = sum(t) / 12
        wet = MONTHS[r.index(max(r))]
        if q == 0:
            return dict(stem=f'Climate data for {stn} ({co}), approximate long-term averages:\n{table}\nCalculate the annual temperature range.',
                        answer=f'{rng_t:g} °C', type='numerical', marks=2,
                        markingKey=f'Range = highest − lowest monthly mean = {max(t):g} − ({min(t):g}) = {rng_t:g} °C (M1 A1).', gap='G3')
        if q == 1:
            return dict(stem=f'The climate graph for {stn}, {co} shows these approximate averages:\n{table}\nCalculate the total annual rainfall.',
                        answer=f'{tot:,} mm', type='numerical', marks=2,
                        markingKey=f'Sum of the twelve monthly totals = {tot:,} mm (M1 A1).', gap='G3')
        if q == 2:
            return dict(stem=f'Study the climate data for {stn} ({co}):\n{table}\nIdentify the wettest month and state its rainfall.',
                        answer=f'{wet}, {max(r)} mm', type='short', marks=1, markingKey=f'{wet} ({max(r)} mm).', gap='G3')
        if q == 3:
            return dict(stem=f'Using the data for {stn} ({co}) below, calculate the mean annual temperature to one decimal place.\n{table}',
                        answer=f'{mean:.1f} °C', type='numerical', marks=2,
                        markingKey=f'Sum of monthly means = {sum(t):g}; ÷ 12 = {mean:.1f} °C (M1 A1).', gap='G3')
        if q == 4:
            dry = [MONTHS[i][:3] for i, x in enumerate(r) if x < 60]
            return dict(stem=f'Climate data for {stn} ({co}):\n{table}\n(a) Calculate the annual temperature range and the total annual rainfall. (b) How many months receive less than 60 mm of rain? (c) Describe the pattern of rainfall through the year.',
                        answer=f'(a) {rng_t:g} °C; {tot:,} mm (b) {len(dry)} ({", ".join(dry) or "none"}) (c) wettest in {wet}; see key',
                        type='multi_step', marks=5,
                        markingKey=f'(a) {max(t):g} − {min(t):g} = {rng_t:g} °C (A1); total {tot:,} mm (A1). (b) {len(dry)} months (A1). '
                                   f'(c) Description using data: wettest month {wet} ({max(r)} mm), driest {MONTHS[r.index(min(r))]} ({min(r)} mm); '
                                   'say whether rain is spread evenly or concentrated in a season (2 marks; data quoted with units).', gap='G3')
        diffs = [abs(a_ - b_) for a_, b_ in zip(t, t[1:])]
        i = diffs.index(max(diffs))
        return dict(stem=f'Using the climate figures for {stn} ({co}) below, suggest which climate zone it belongs to and justify your answer with two pieces of evidence from the data.\n{table}',
                    answer=f'Range {rng_t:g} °C, total rain {tot:,} mm; zone justified from these figures (see key).', type='case', marks=4,
                    markingKey=f'Evidence must be quoted: mean {mean:.1f} °C, range {rng_t:g} °C, total {tot:,} mm, wettest {wet}. '
                               'Expected zone: ' + {'Manaus': 'equatorial (hot all year, small range, rain all year)',
                                                    'Mumbai': 'tropical monsoon (hot all year, very wet June–September, dry winter)',
                                                    'London': 'temperate maritime (mild, small range, rain all year)',
                                                    'Cairo': 'hot desert (very low rainfall, hot summers)',
                                                    'Moscow': 'cold continental (large range, freezing winters, summer rain maximum)',
                                                    'Singapore': 'equatorial (hot, wet all year, range under 3 °C)',
                                                    'Darwin': 'tropical wet-and-dry / savanna (hot all year, distinct wet season December–March)',
                                                    'Reykjavik': 'cold maritime / subpolar oceanic (cool summers, winters near 0 °C, rain all year)',
                                                    'Nairobi': 'tropical highland (mild because of altitude, two rainy seasons)',
                                                    'Riyadh': 'hot desert (extreme summer heat, under 100 mm rain)'}[stn] +
                               '. 1 mark zone, up to 3 marks for data-based justification.', gap='G5')
    K.add(key, c, d, cl, 'numerical')


def discharge(K, key, c=('C3', 'C4'), d=(1, 5)):
    RIV = ['a tributary of the Rhine', 'a mountain stream in the Himalayan foothills', 'a lowland river in East Anglia',
           'a river in the Scottish Highlands', 'a stream in the Blue Mountains of Australia', 'a tributary of the Mekong']

    def q_(rng, slot):
        w = rng.choice([2.5, 3, 4, 5.5, 6, 8, 12, 15])
        dep = rng.choice([0.2, 0.3, 0.4, 0.5, 0.8, 1.2])
        v = rng.choice([0.2, 0.3, 0.45, 0.6, 0.8, 1.1, 1.5])
        A = w * dep
        Q = A * v
        riv = rng.choice(RIV)
        if slot.d >= 4:
            v2 = round(v * rng.choice([1.5, 2, 2.5]), 2)
            dep2 = round(dep * rng.choice([2, 3]), 2)
            Q2 = w * dep2 * v2
            stem = (f'Students measured {riv}: width {w} m, mean depth {dep} m, mean velocity {v} m/s. After heavy rain the mean depth rose to '
                    f'{dep2} m and velocity to {v2} m/s (width unchanged). Calculate the discharge before and after, and the percentage increase. '
                    'Explain one reason why discharge rises after a storm.')
            return dict(stem=stem, answer=f'{Q:.3g} m³/s → {Q2:.3g} m³/s (+{(Q2 - Q) / Q * 100:.0f}%)', type='multi_step', marks=6,
                        markingKey=f'Q = width × depth × velocity (M1); before {w}×{dep}×{v} = {Q:.3g} m³/s (A1); after {w}×{dep2}×{v2} = {Q2:.3g} m³/s (A1); '
                                   f'% increase = {(Q2 - Q) / Q * 100:.0f}% (A1). Reason (2): surface runoff and throughflow add water quickly; saturated soil reduces infiltration.', gap='G5')
        stem = rng.choice([
            f'A fieldwork group measured {riv}. Width = {w} m, mean depth = {dep} m and mean velocity = {v} m/s. Calculate the discharge in cumecs (m³/s).',
            f'Calculate the discharge of {riv} given a cross-sectional area of {A:g} m² and a mean velocity of {v} m/s.',
        ])
        return dict(stem=stem, answer=f'{Q:.3g} m³/s', type='numerical', marks=2,
                    markingKey=f'Discharge = cross-sectional area × velocity = {A:g} × {v} = {Q:.3g} m³/s (M1 A1).', gap='G3')
    K.add(key, c, d, q_, 'numerical')

    def lag(rng, slot):
        rp = rng.randint(6, 14)
        lagh = rng.randint(3, 30)
        peak_t = rp + lagh
        day = peak_t // 24
        hh = peak_t % 24
        base = rng.choice([4, 6, 10, 15])
        peakq = base * rng.choice([3, 4, 5, 6])
        stem = (f'A storm hydrograph shows peak rainfall at {rp:02d}:00 on day 1 and peak discharge of {peakq} m³/s at {hh:02d}:00 on day {day + 1}. '
                f'Base flow was {base} m³/s. Calculate the lag time and the rise in discharge above base flow, then suggest one land-use change that would shorten the lag time.')
        return dict(stem=stem, answer=f'Lag time {lagh} h; rise {peakq - base} m³/s; e.g. urbanisation / deforestation', type='multi_step', marks=4,
                    markingKey=f'Lag time = time of peak discharge − time of peak rainfall = {lagh} hours (A1); rise = {peakq} − {base} = {peakq - base} m³/s (A1); '
                               'land-use change with reason (2): more impermeable surfaces (concrete, drains) or deforestation reduce infiltration and interception, so water reaches the channel faster.', gap='G3')
    K.add(key, c, d, lag, 'multi_step')


def quake(K, key, c='C3', d=(2, 5)):
    EQ = [('the 2004 Indian Ocean earthquake', 9.1), ('the 2011 Tōhoku earthquake, Japan', 9.0), ('the 2010 Haiti earthquake', 7.0),
          ('the 2015 Gorkha earthquake, Nepal', 7.8), ('the 2023 Türkiye–Syria earthquake', 7.8), ('the 2010 Maule earthquake, Chile', 8.8),
          ('the 2001 Gujarat earthquake, India', 7.7), ('the 2016 Kaikōura earthquake, New Zealand', 7.8), ('the 1960 Valdivia earthquake, Chile', 9.5),
          ('the 2017 Puebla earthquake, Mexico', 7.1), ('the 2023 Al Haouz earthquake, Morocco', 6.8)]

    def mq(rng, slot):
        (a, ma), (b, mb) = rng.sample(EQ, 2)
        if ma == mb:
            return None
        if ma < mb:
            (a, ma), (b, mb) = (b, mb), (a, ma)
        dm = round(ma - mb, 1)
        amp = 10 ** dm
        en = 10 ** (1.5 * dm)
        stem = (f'{cap(a)} had a moment magnitude of {ma}; {b} had a magnitude of {mb}. Each whole step on the magnitude scale means about 10 times '
                'more ground shaking (amplitude) and about 32 times more energy. Calculate how many times greater (a) the amplitude and (b) the energy release of the larger earthquake was.')
        return dict(stem=stem, answer=f'(a) about {amp:,.0f} times; (b) about {en:,.0f} times', type='numerical', marks=3,
                    markingKey=f'Difference {dm} (M1); amplitude 10^{dm} ≈ {amp:,.0f} (A1); energy 10^(1.5×{dm}) ≈ {en:,.0f} (A1; 32^{dm} accepted). '
                               'Magnitude does not on its own decide the death toll – vulnerability does.', gap='G3')
    K.add(key, c, d, mq, 'numerical')


def chronology(K, key, c='C3', d=(1, 4), events=None):
    EV = events or [('the founding of Rome (traditional date)', -753), ('the death of the Buddha (traditional date)', -483),
          ('the start of the Maurya Empire', -322), ('the unification of China by Qin Shi Huang', -221),
          ('the death of Julius Caesar', -44), ('the birth of Muhammad', 570), ('the Battle of Hastings', 1066),
          ('the signing of Magna Carta', 1215), ('the fall of Constantinople', 1453), ('the Battle of Panipat that founded Mughal rule', 1526),
          ('the building of the Great Pyramid of Giza (approx.)', -2560), ('the reign of Hammurabi of Babylon begins (approx.)', -1792),
          ('the reign of Ashoka begins (approx.)', -268), ('the opening of the Silk Road under the Han (approx.)', -130),
          ('Marco Polo reaches the court of Kublai Khan (approx.)', 1275), ('the first printing of the Gutenberg Bible (approx.)', 1455)]

    def yr(v):
        return f'{-v} BCE' if v < 0 else f'{v} CE'

    def ch_(rng, slot):
        (a, ya), (b, yb) = sorted(rng.sample(EV, 2), key=lambda x: x[1])
        if ya == yb:
            return None
        if ya < 0 < yb:
            gap = yb - ya - 1
            how = f'{-ya} + {yb} − 1 = {gap} (subtract 1 because there is no year 0)'
        else:
            gap = yb - ya
            how = f'{abs(yb - ya)} by subtraction'
        fr = rng.randrange(2)
        stem = (f'How many years passed between {a} ({yr(ya)}) and {b} ({yr(yb)})?' if fr == 0 else
                f'On a timeline, {a} is marked at {yr(ya)} and {b} at {yr(yb)}. Calculate the number of years between the two events.')
        return dict(stem=stem, answer=f'{gap} years', type='numerical', marks=2,
                    markingKey=f'{how} (M1 A1). BCE years count down towards 1 BCE; the year after 1 BCE is 1 CE.', gap='G3')
    K.add(key, c, d, ch_, 'numerical')

    def cent(rng, slot):
        a, y = rng.choice(EV)
        if y < 0:
            cn = (-y - 1) // 100 + 1
            right = f'{_ord(cn)} century BCE'
            wr = [f'{_ord(cn + 1)} century BCE', f'{_ord(cn)} century CE', f'{_ord(max(cn - 1, 2))} century BCE' if cn != 2 else '3rd millennium BCE']
        else:
            cn = (y - 1) // 100 + 1
            right = f'{_ord(cn)} century CE'
            wr = [f'{_ord(cn - 1)} century CE', f'{_ord(cn + 1)} century CE', f'{_ord(cn)} century BCE']
        wr = _distinct(right, wr)
        if not wr:
            return None
        return mcq(rng, f'In which century did {a} ({yr(y)}) take place?', right, wr,
                   f'{yr(y)} falls in the {right}: e.g. the 15th century CE runs from 1401 to 1500.')
    K.add(key, 'C3', (1, 3), cent, 'mcq')

    def order_(rng, slot):
        evs = rng.sample(EV, 4)
        if len({e[1] for e in evs}) < 4:
            return None
        srt = sorted(evs, key=lambda x: x[1])
        stem = 'Place these events in chronological order, earliest first: ' + '; '.join(f'{e[0]} ({yr(e[1])})' for e in evs) + '.'
        ans = ' → '.join(e[0] for e in srt)
        return dict(stem=stem, answer=ans, type='short', marks=2,
                    markingKey=f'{ans}. A larger BCE number is earlier. 2 marks all correct, 1 mark one adjacent pair swapped.', gap='G2')
    K.add(key, c, d, order_, 'short')


def _ord(n):
    return f'{n}{"th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")}'


SD_GOODS = [('bubble tea in Taipei', 'cups', 'TWD'), ('second-hand bicycles in Amsterdam', 'bicycles', '€'),
            ('concert tickets in Seoul', 'tickets', 'thousand KRW'), ('mangoes at a market in Mumbai', 'kg', '₹'),
            ('coffee at a café in Nairobi', 'cups', 'KES'), ('umbrellas in Singapore', 'umbrellas', 'S$'),
            ('school notebooks in Lima', 'notebooks', 'soles'), ('ferry tickets in Istanbul', 'tickets', 'lira'),
            ('fresh bread in Lyon', 'loaves', '€'), ('phone cases in Kuala Lumpur', 'cases', 'RM')]


def supply_demand(K, key, c=('C3', 'C4'), d=(1, 5)):
    def eq(rng, slot):
        good, unit, cur = rng.choice(SD_GOODS)
        P = rng.randint(4, 20)
        b = rng.randint(2, 8)
        dd = rng.randint(2, 8)
        Q = rng.randint(5, 40) * 10
        a = Q + b * P
        cc = Q - dd * P
        if cc <= -200:
            return None
        mode = rng.randrange(3) if slot.d >= 3 else 0
        cs = f'{cc:+d}'.replace('+', '+ ').replace('-', '− ')
        fn = f'Qd = {a} − {b}P and Qs = {dd}P {cs}'
        if mode == 0:
            stem = f'In the market for {good}, demand and supply are given by {fn} (P in {cur}, Q in {unit} per day). Calculate the equilibrium price and quantity.'
            return dict(stem=stem, answer=f'P = {P} {cur}, Q = {Q} {unit}', type='numerical', marks=3,
                        markingKey=f'Set Qd = Qs: {a} − {b}P = {dd}P {cs} (M1) → {b + dd}P = {a - cc} → P = {P} (A1); Q = {a} − {b}×{P} = {Q} (A1).', gap='G3')
        if mode == 1:
            pc = P - rng.randint(1, min(3, P - 1))
            qd, qs = a - b * pc, dd * pc + cc
            stem = (f'For {good}: {fn} (P in {cur}). The government sets a maximum price of {pc} {cur}. Calculate the equilibrium, then the size of the '
                    'shortage at the maximum price, and explain one likely consequence.')
            return dict(stem=stem, answer=f'Equilibrium P = {P}, Q = {Q}; shortage = {qd - qs} {unit}', type='multi_step', marks=5,
                        markingKey=f'Equilibrium P = {P}, Q = {Q} (A1 A1). At P = {pc}: Qd = {qd}, Qs = {qs} (M1); shortage = {qd - qs} {unit} (A1). '
                                   'Consequence (R1): queues, rationing or a black market at prices above the ceiling.', gap='G5')
        shift = rng.randint(2, 8) * b * 2
        P2 = (a + shift - cc) / (b + dd)
        Q2 = dd * P2 + cc
        stem = (f'The market for {good} is described by {fn} (P in {cur}). A successful advertising campaign increases demand by {shift} {unit} at every price. '
                'Calculate the old and new equilibrium price and quantity and describe the change.')
        return dict(stem=stem, answer=f'Old P = {P}, Q = {Q}; new P = {P2:g}, Q = {Q2:g}', type='multi_step', marks=5,
                    markingKey=f'Old: P = {P}, Q = {Q} (A1). New demand Qd = {a + shift} − {b}P (M1); {a + shift} − {b}P = {dd}P {cs} → P = {P2:g} (A1), Q = {Q2:g} (A1). '
                               'Demand curve shifts right; price and quantity both rise (R1).', gap='G5')
    K.add(key, c, d, eq, 'numerical')

    def sched(rng, slot):
        good, unit, cur = rng.choice(SD_GOODS)
        P0 = rng.randint(2, 6)
        step = rng.choice([1, 2])
        prices = [P0 + step * i for i in range(5)]
        b, dd = rng.randint(3, 9), rng.randint(3, 9)
        k = rng.randint(1, 3)
        Pe = prices[k]
        Q = rng.randint(6, 30) * 10
        qd = [Q - b * (p - Pe) * 5 for p in prices]
        qs = [Q + dd * (p - Pe) * 5 for p in prices]
        if min(qd + qs) < 0:
            return None
        tbl = '\n'.join(f'{p} {cur}: demand {x}, supply {y}' for p, x, y in zip(prices, qd, qs))
        hi = prices[4]
        stem = f'The table shows the daily demand and supply schedule for {good} ({unit}).\n{tbl}\n(a) Identify the equilibrium price. (b) State whether there is a shortage or surplus at {hi} {cur}, and how large it is.'
        return dict(stem=stem, answer=f'(a) {Pe} {cur} ({Q} {unit}); (b) surplus of {qs[4] - qd[4]} {unit}', type='numerical', marks=3,
                    markingKey=f'(a) Equilibrium where demand = supply: {Pe} {cur}, {Q} {unit} (A1). (b) At {hi}: supply {qs[4]} > demand {qd[4]} → surplus (R1) of {qs[4] - qd[4]} (A1).', gap='G3')
    K.add(key, ('C3',), (1, 3), sched, 'numerical')


def tax_subsidy(K, key, c=('C3', 'C4'), d=(2, 5)):
    def ts(rng, slot):
        good, unit, cur = rng.choice(SD_GOODS + [('sugary drinks in Mexico City', 'bottles', 'pesos'), ('cigarettes in Melbourne', 'packs', 'A$'),
                                                  ('solar panels in Kenya', 'panels', 'thousand KES'), ('electric scooters in Paris', 'scooters', '€')])
        b, dd = rng.randint(2, 6), rng.randint(2, 6)
        P = rng.randint(6, 20)
        Q = rng.randint(10, 40) * 10
        a, cc = Q + b * P, Q - dd * P
        t = rng.randint(1, 4)
        sub = rng.random() < 0.5
        s = -t if sub else t
        # supply with tax t: Qs = dd(P - t) + cc
        P2 = (a - cc + dd * s) / (b + dd)
        Q2 = a - b * P2
        cs = f'{cc:+d}'.replace('+', '+ ').replace('-', '− ')
        word = f'a subsidy of {t} {cur} per unit to producers' if sub else f'a tax of {t} {cur} per unit on producers'
        stem = (f'For {good}: Qd = {a} − {b}P and Qs = {dd}P {cs} (P in {cur}). The government introduces {word}. '
                f'Calculate the new equilibrium price paid by consumers and the new quantity, and explain why governments might do this.')
        why = ('to make a merit good or green technology cheaper and encourage consumption' if sub else
               'to discourage consumption of a good with harmful effects and raise tax revenue')
        rev = abs(t * Q2)
        return dict(stem=stem, answer=f'Consumer price {P2:.2f} {cur}; quantity {Q2:.1f} {unit}', type='multi_step', marks=6,
                    markingKey=f'Original equilibrium P = {P}, Q = {Q} (A1). New supply Qs = {dd}(P {"+" if sub else "−"} {t}) {cs} (M1); solve: P = {P2:.2f} (A1), Q = {Q2:.1f} (A1). '
                               f'{"Government spending" if sub else "Tax revenue"} = {t} × {Q2:.1f} = {rev:.1f} (A1). Reason (R1): {why}. Price changes by less than {t} because the burden/benefit is shared.', gap='G5')
    K.add(key, c, d, ts, 'multi_step')


def opp_cost(K, key, c=('C3', 'C4'), d=(1, 5)):
    def ppc(rng, slot):
        place = rng.choice(['a farm in the Punjab', 'a smallholding in Ghana', 'a cooperative in Vietnam', 'a farm in New Zealand',
                            'a workshop in Morocco', 'a factory in Bangladesh'])
        A, B = rng.choice([('wheat', 'rice'), ('cocoa', 'maize'), ('coffee', 'rice'), ('milk', 'wool'), ('rugs', 'pottery'), ('shirts', 'bags')])
        xa = rng.randint(4, 20) * 10
        xb = rng.randint(4, 20) * 10
        if xa == xb:
            return None
        oc = xa / xb
        stem = (f'Using all its resources, {place} can produce either {xa} units of {A} or {xb} units of {B} per year (a straight-line production possibility curve). '
                f'What is the opportunity cost of producing one unit of {B}?')
        if slot.d >= 3:
            nb = rng.randint(1, xb // 10 - 1) * 10
            na = xa - oc * nb
            stem += f' If it produces {nb} units of {B}, what is the maximum amount of {A} it can produce?'
            return dict(stem=stem, answer=f'{oc:.3g} units of {A}; {na:.3g} units of {A}', type='numerical', marks=3,
                        markingKey=f'Opportunity cost of 1 {B} = {xa} ÷ {xb} = {oc:.3g} {A} (M1 A1); {A} = {xa} − {oc:.3g}×{nb} = {na:.3g} (A1).', gap='G3')
        return dict(stem=stem, answer=f'{oc:.3g} units of {A}', type='numerical', marks=2,
                    markingKey=f'Giving up all {xa} {A} gains {xb} {B}, so 1 {B} costs {xa} ÷ {xb} = {oc:.3g} {A} (M1 A1).', gap='G3')
    K.add(key, c, d, ppc, 'numerical')

    def choice_(rng, slot):
        who = name(rng)
        opts = rng.sample([('going to a football match', 'joy'), ('buying a novel', 'joy'), ('a cinema trip with friends', 'joy'),
                           ('a new pair of trainers', 'joy'), ('saving for a laptop', 'joy'), ('a cooking class', 'joy'),
                           ('a train trip to the coast', 'joy')], 3)
        ranks = [1, 2, 3]
        chosen, nxt, third = opts[0][0], opts[1][0], opts[2][0]
        stem = (f'{who} has one free Saturday and enough money for only one of these: {opts[0][0]}, {opts[1][0]} or {opts[2][0]}. '
                f'{who} ranks them in that order of preference and chooses {chosen}. What is the opportunity cost of this choice? Explain.')
        return dict(stem=stem, answer=f'{cap(nxt)} – the next best alternative forgone', type='explain', marks=2,
                    markingKey=f'Opportunity cost = the next best alternative given up = {nxt} (1); not all the alternatives combined and not the money price (1).', gap='G2')
    K.add(key, ('C2', 'C3'), (1, 3), choice_, 'explain')


def budget(K, key, c=('C3', 'C4'), d=(1, 5)):
    def bud(rng, slot):
        who = name(rng)
        cur, inc = rng.choice([('€', 1800), ('S$', 2400), ('A$', 3100), ('£', 1650), ('CA$', 2900)])
        inc = inc + rng.randint(-4, 8) * 50
        items = {'rent': round(inc * rng.uniform(0.28, 0.38), -1), 'food': round(inc * rng.uniform(0.12, 0.18), -1),
                 'transport': round(inc * rng.uniform(0.05, 0.09), -1), 'phone and internet': round(inc * rng.uniform(0.03, 0.05), -1),
                 'leisure': round(inc * rng.uniform(0.06, 0.12), -1)}
        spend = sum(items.values())
        save = inc - spend
        rate = save / inc * 100
        lst = ', '.join(f'{k} {cur}{v:,.0f}' for k, v in items.items())
        if slot.d <= 2:
            stem = f'{who}\'s monthly take-home income is {cur}{inc:,}. Monthly spending is: {lst}. How much is left to save each month?'
            return dict(stem=stem, answer=f'{cur}{save:,.0f}', type='numerical', marks=2,
                        markingKey=f'Total spending {cur}{spend:,.0f} (M1); saving = {cur}{inc:,} − {cur}{spend:,.0f} = {cur}{save:,.0f} (A1).', gap='G3')
        goal = round(save * rng.randint(5, 14) * rng.uniform(0.9, 1.3), -2)
        months = math.ceil(goal / save) if save > 0 else None
        if not months:
            return None
        stem = (f'{who} earns {cur}{inc:,} a month after tax and spends: {lst}. (a) Calculate the monthly saving and the savings rate as a percentage of income. '
                f'(b) How many whole months will it take to save {cur}{goal:,.0f} for a deposit on a course? (c) Suggest one change to the budget, justified as a need or a want.')
        return dict(stem=stem, answer=f'(a) {cur}{save:,.0f}, {rate:.1f}% (b) {months} months', type='multi_step', marks=5,
                    markingKey=f'(a) {cur}{inc:,} − {cur}{spend:,.0f} = {cur}{save:,.0f} (A1); {save:,.0f} ÷ {inc:,} × 100 = {rate:.1f}% (A1). '
                               f'(b) {goal:,.0f} ÷ {save:,.0f} = {goal / save:.2f} → {months} months (round up) (M1 A1). (c) e.g. reduce leisure (a want) rather than rent or food (needs) (R1).', gap='G3')
    K.add(key, c, d, bud, 'multi_step')

    def best_buy(rng, slot):
        prod = rng.choice([('rice', 'kg'), ('olive oil', 'litre'), ('laundry detergent', 'kg'), ('orange juice', 'litre')])
        s1, s2 = rng.choice([(0.5, 2), (1, 5), (0.75, 3), (2, 5)])
        p1 = round(rng.uniform(1.2, 4) * s1, 2)
        p2 = round(p1 / s1 * s2 * rng.choice([0.8, 0.85, 0.9, 1.1, 1.15]), 2)
        u1, u2 = p1 / s1, p2 / s2
        best = f'{s1} {prod[1]} pack' if u1 < u2 else f'{s2} {prod[1]} pack'
        stem = f'A shop sells {prod[0]} in a {s1} {prod[1]} pack for €{p1:.2f} and a {s2} {prod[1]} pack for €{p2:.2f}. Which is better value? Show the unit prices, and give one reason a shopper might still choose the other pack.'
        return dict(stem=stem, answer=f'{best} (€{min(u1, u2):.2f} per {prod[1]} vs €{max(u1, u2):.2f})', type='numerical', marks=3,
                    markingKey=f'Unit prices €{u1:.2f} and €{u2:.2f} per {prod[1]} (M1 A1); {best} is cheaper per unit. Reason (R1): limited budget now, storage, waste if it spoils.', gap='G3')
    K.add(key, ('C3',), (1, 4), best_buy, 'numerical')


def interest(K, key, c=('C3', 'C4'), d=(1, 5)):
    def intr(rng, slot):
        who = name(rng)
        P = rng.choice([500, 800, 1000, 1500, 2000, 2500, 5000])
        r = rng.choice([2, 2.5, 3, 4, 5, 6])
        n = rng.randint(2, 6)
        si = P * r / 100 * n
        ci = P * (1 + r / 100) ** n - P
        if slot.d <= 2:
            stem = f'{who} deposits €{P:,} in a savings account paying {r}% simple interest per year. How much interest will be earned after {n} years?'
            return dict(stem=stem, answer=f'€{si:,.2f}', type='numerical', marks=2,
                        markingKey=f'Simple interest = P × r × t = {P:,} × {r / 100} × {n} = €{si:,.2f} (M1 A1).', gap='G3')
        stem = (f'{who} can save €{P:,} for {n} years in Account A ({r}% simple interest) or Account B ({r}% interest compounded annually). '
                'Calculate the interest earned in each account and explain why they differ.')
        return dict(stem=stem, answer=f'A: €{si:,.2f}; B: €{ci:,.2f}', type='multi_step', marks=4,
                    markingKey=f'A: {P:,} × {r / 100} × {n} = €{si:,.2f} (A1). B: {P:,} × (1 + {r / 100})^{n} − {P:,} = €{ci:,.2f} (M1 A1). '
                               'B earns more because interest is paid on previous interest (compounding) (R1).', gap='G3')
    K.add(key, c, d, intr, 'numerical')

    def loan(rng, slot):
        P = rng.choice([200, 300, 500, 1000])
        r = rng.choice([18, 24, 30, 36])
        n = rng.choice([6, 12])
        tot = P * (1 + r / 100 * n / 12)
        stem = (f'A street vendor in Dhaka borrows {P} US dollars from a microfinance institution at a flat interest rate of {r}% per year for {n} months. '
                'Calculate the total amount repaid and the equal monthly repayment.')
        return dict(stem=stem, answer=f'Total ${tot:,.2f}; monthly ${tot / n:,.2f}', type='numerical', marks=3,
                    markingKey=f'Interest = {P} × {r / 100} × {n}/12 = ${tot - P:,.2f} (M1); total ${tot:,.2f} (A1); ÷ {n} = ${tot / n:,.2f} per month (A1).', gap='G3')
    K.add(key, c, d, loan, 'numerical')


def trade(K, key, c=('C3', 'C4'), d=(1, 5)):
    def ca(rng, slot):
        (c1, c2) = rng.choice([('Brazil', 'Germany'), ('Vietnam', 'Japan'), ('Kenya', 'the Netherlands'), ('Chile', 'South Korea'),
                               ('Bangladesh', 'the United Kingdom'), ('Ghana', 'Switzerland')])
        g1, g2 = rng.choice([('coffee', 'machinery'), ('rice', 'electronics'), ('flowers', 'tractors'), ('copper', 'cars'),
                             ('T-shirts', 'medicines'), ('cocoa', 'watches')])
        a1, b1 = rng.randint(6, 20) * 10, rng.randint(1, 5) * 10
        a2, b2 = rng.randint(1, 5) * 10, rng.randint(6, 20) * 10
        oc1 = b1 / a1
        oc2 = b2 / a2
        stem = (f'With the same resources, {c1} can produce {a1} units of {g1} or {b1} units of {g2}; {c2} can produce {a2} units of {g1} or {b2} units of {g2}. '
                f'Calculate the opportunity cost of one unit of {g1} in each country and state which good each should specialise in.')
        return dict(stem=stem, answer=f'{c1}: {oc1:.3g} {g2}; {c2}: {oc2:.3g} {g2}; {c1} → {g1}, {c2} → {g2}', type='multi_step', marks=4,
                    markingKey=f'{c1}: {b1} ÷ {a1} = {oc1:.3g} units of {g2} per {g1} (A1); {c2}: {b2} ÷ {a2} = {oc2:.3g} (A1). '
                               f'Lower opportunity cost of {g1} in {c1} → comparative advantage in {g1}; {c2} in {g2} (R1 R1).', gap='G5')
    K.add(key, c, d, ca, 'multi_step')

    def bal(rng, slot):
        co = rng.choice(['Kenya', 'Vietnam', 'New Zealand', 'Peru', 'Morocco', 'Sri Lanka', 'Norway', 'Chile'])
        x = rng.randint(20, 400) / 10
        m = round(x * rng.uniform(0.6, 1.5), 1)
        b = x - m
        stem = f'In one year a country such as {co} exported goods worth US$ {x:.1f} billion and imported goods worth US$ {m:.1f} billion. Calculate its balance of trade in goods and state whether it is a surplus or a deficit.'
        return dict(stem=stem, answer=f'US$ {b:+.1f} billion ({"surplus" if b > 0 else "deficit" if b < 0 else "balanced"})', type='numerical', marks=2,
                    markingKey=f'Balance of trade = exports − imports = {x:.1f} − {m:.1f} = {b:+.1f} bn (M1 A1).', gap='G3')
    K.add(key, ('C3',), (1, 3), bal, 'numerical')


def exchange(K, key, c='C3', d=(1, 4)):
    RATES_ = [('euros', 'Indian rupees', 90), ('US dollars', 'Japanese yen', 150), ('British pounds', 'euros', 1.17),
              ('US dollars', 'Kenyan shillings', 130), ('Singapore dollars', 'Malaysian ringgit', 3.5), ('euros', 'Swiss francs', 0.95)]

    def ex(rng, slot):
        a, b, r = rng.choice(RATES_)
        amt = rng.choice([50, 120, 250, 400, 1000, 1500])
        stem = rng.choice([f'A traveller changes {amt} {a} into {b} at a rate of 1 {a[:-1] if a.endswith("s") else a} = {r} {b}. How much do they receive?',
                           f'At an exchange rate of 1 {a[:-1] if a.endswith("s") else a} = {r} {b}, a souvenir costs {amt * r:,.2f} {b}. What is its price in {a}?'])
        if 'souvenir' in stem:
            return dict(stem=stem, answer=f'{amt:,} {a}', type='numerical', marks=2,
                        markingKey=f'{amt * r:,.2f} ÷ {r} = {amt:,} {a} (M1 A1).', gap='G3')
        return dict(stem=stem, answer=f'{amt * r:,.2f} {b}', type='numerical', marks=2,
                    markingKey=f'{amt} × {r} = {amt * r:,.2f} {b} (M1 A1).', gap='G3')
    K.add(key, c, d, ex, 'numerical')


def dependency(K, key, c=('C3', 'C4'), d=(1, 5)):
    def dep(rng, slot):
        co, y, w, o = rng.choice(AGES)
        r = (y + o) / w * 100
        if slot.d <= 2:
            stem = f'In {co} about {y}% of people are aged 0–14, {w}% are 15–64 and {o}% are 65 or over (2023 estimates). Calculate the dependency ratio.'
            return dict(stem=stem, answer=f'{r:.1f}', type='numerical', marks=2,
                        markingKey=f'Dependency ratio = (0–14 + 65+) ÷ 15–64 × 100 = ({y} + {o}) ÷ {w} × 100 = {r:.1f} (M1 A1).', gap='G3')
        (c2, y2, w2, o2) = rng.choice([a for a in AGES if a[0] != co])
        r2 = (y2 + o2) / w2 * 100
        stem = (f'Population structure (2023 estimates): {co} – 0–14: {y}%, 15–64: {w}%, 65+: {o}%; {c2} – 0–14: {y2}%, 15–64: {w2}%, 65+: {o2}%. '
                'Calculate the dependency ratio of each country and explain how the challenges created by dependants differ between them.')
        return dict(stem=stem, answer=f'{co}: {r:.1f}; {c2}: {r2:.1f}', type='multi_step', marks=5,
                    markingKey=f'{co}: ({y}+{o})/{w}×100 = {r:.1f} (A1); {c2}: ({y2}+{o2})/{w2}×100 = {r2:.1f} (A1). Explanation (3): a youthful structure (large 0–14 share) needs schools, '
                               'maternal health care and future jobs; an ageing structure (large 65+ share) needs pensions, health and social care and may face labour shortages.', gap='G5')
    K.add(key, c, d, dep, 'numerical')


def per_capita(K, key, rows, what='GDP per capita', unit='US$', c=('C3', 'C4'), d=(1, 5)):
    """rows: (country, total value in billions US$, population millions, year)."""
    def pcap(rng, slot):
        co, tot, pop, yr = rng.choice(rows)
        v = tot * 1e9 / (pop * 1e6)
        if slot.d <= 3:
            stem = rng.choice([f'In {yr} {co} had a GDP of about US$ {tot:,} billion and a population of about {pop:,} million. Calculate its GDP per capita.',
                               f'Calculate the {what} of {co} from these {yr} estimates: GDP US$ {tot:,} billion; population {pop:,} million.'])
            return dict(stem=stem, answer=f'about US$ {v:,.0f}', type='numerical', marks=2,
                        markingKey=f'GDP ÷ population = {tot:,} × 10⁹ ÷ ({pop:,} × 10⁶) = US$ {v:,.0f} (M1 A1). Watch the units (billions vs millions).', gap='G3')
        co2, tot2, pop2, yr2 = rng.choice([r for r in rows if r[0] != co])
        v2 = tot2 * 1e9 / (pop2 * 1e6)
        hi, lo = (co, co2) if v > v2 else (co2, co)
        stem = (f'Estimates: {co} – GDP US$ {tot:,} bn, population {pop:,} m ({yr}); {co2} – GDP US$ {tot2:,} bn, population {pop2:,} m ({yr2}). '
                'Calculate GDP per capita for both, the ratio between them, and explain one limitation of GDP per capita as a measure of development.')
        return dict(stem=stem, answer=f'{co}: US$ {v:,.0f}; {co2}: US$ {v2:,.0f}; ratio ≈ {max(v, v2) / min(v, v2):.1f}', type='multi_step', marks=5,
                    markingKey=f'{co} US$ {v:,.0f} (A1); {co2} US$ {v2:,.0f} (A1); {hi} ≈ {max(v, v2) / min(v, v2):.1f} × {lo} (A1). Limitation (2): an average hides inequality; '
                               'ignores informal work, unpaid work and quality of life; not adjusted for cost of living unless PPP is used.', gap='G5')
    K.add(key, c, d, pcap, 'numerical')


def hdi(K, key, c=('C3', 'C4'), d=(3, 5)):
    ROWS = [('Norway', 83.2, 18.6, 13.1, 69_200), ('India', 67.7, 12.6, 6.6, 6_950), ('Niger', 61.6, 7.0, 1.4, 1_240),
            ('Brazil', 72.8, 15.6, 8.3, 14_600), ('Japan', 84.8, 15.2, 13.4, 42_300), ('Kenya', 61.4, 10.7, 6.7, 4_470)]

    def h(rng, slot):
        co, le, eys, mys, gni = rng.choice(ROWS)
        lei = (le - 20) / 65
        ei = (min(eys, 18) / 18 + min(mys, 15) / 15) / 2
        ii = (math.log(gni) - math.log(100)) / (math.log(75_000) - math.log(100))
        v = (lei * ei * ii) ** (1 / 3)
        stem = (f'Approximate UNDP data for {co} (2022): life expectancy {le} years, expected years of schooling {eys}, mean years of schooling {mys}, '
                f'GNI per capita (PPP) US$ {gni:,}. Using: health index = (LE − 20) ÷ 65; education index = (EYS ÷ 18 + MYS ÷ 15) ÷ 2; '
                'income index = (ln GNI − ln 100) ÷ (ln 75 000 − ln 100); HDI = cube root of (health × education × income), calculate the HDI to 3 decimal places.')
        return dict(stem=stem, answer=f'{v:.3f}', type='multi_step', marks=5,
                    markingKey=f'Health {lei:.3f} (A1); education {ei:.3f} (A1); income {ii:.3f} (A1); HDI = ({lei:.3f} × {ei:.3f} × {ii:.3f})^(1/3) = {v:.3f} (M1 A1). '
                               'Small differences from published HDI come from rounding and data revisions.', gap='G3')
    K.add(key, c, d, h, 'multi_step')


def electoral(K, key, c=('C3', 'C4'), d=(2, 5)):
    PARTIES = ['Greens', 'Liberals', 'Labour', 'Conservatives', 'Social Democrats', 'Farmers\' Party', 'Progressives']

    def fptp_pr(rng, slot):
        ps = rng.sample(PARTIES, 3)
        nseat = rng.choice([5, 6, 8, 10])
        votes = []
        wins = {p: 0 for p in ps}
        tot = {p: 0 for p in ps}
        lines = []
        for i in range(nseat):
            v = [rng.randint(20, 60) * 100 for _ in ps]
            if len(set(v)) < 3:
                return None
            w = ps[v.index(max(v))]
            wins[w] += 1
            for p, x in zip(ps, v):
                tot[p] += x
            lines.append(f'District {i + 1}: ' + ', '.join(f'{p} {x:,}' for p, x in zip(ps, v)))
        allv = sum(tot.values())
        share = {p: tot[p] / allv * 100 for p in ps}
        # largest remainder (Hare) PR allocation of nseat
        quotas = {p: tot[p] / allv * nseat for p in ps}
        alloc = {p: int(quotas[p]) for p in ps}
        for p in sorted(ps, key=lambda p: quotas[p] - alloc[p], reverse=True)[: nseat - sum(alloc.values())]:
            alloc[p] += 1
        stem = (f'A small country elects {nseat} seats, one per district, using first past the post. Results:\n' + '\n'.join(lines) +
                f'\n(a) How many seats does each party win? (b) Calculate each party\'s share of the total vote. (c) How many seats would each party get under proportional representation (largest remainder)? (d) Comment on the difference.')
        ans = ('FPTP: ' + ', '.join(f'{p} {wins[p]}' for p in ps) + '; vote share: ' + ', '.join(f'{p} {share[p]:.1f}%' for p in ps) +
               '; PR: ' + ', '.join(f'{p} {alloc[p]}' for p in ps))
        return dict(stem=stem, answer=ans, type='multi_step', marks=6,
                    markingKey=f'(a) winner = most votes in each district (A1). (b) totals ' + ', '.join(f'{p} {tot[p]:,}' for p in ps) + f' of {allv:,} (M1 A1). '
                               f'(c) quota = share × {nseat}; whole parts then largest remainders (A1). (d) FPTP can over-reward the party that wins many districts narrowly and '
                               'under-represent parties whose votes are spread out; PR matches seats more closely to votes (R2).', gap='G5')
    K.add(key, c, d, fptp_pr, 'multi_step')

    def dhondt(rng, slot):
        ps = rng.sample(PARTIES, 3)
        v = sorted([rng.randint(10, 60) * 1000 for _ in ps], reverse=True)
        if len(set(v)) < 3:
            return None
        seats = rng.choice([4, 5, 6])
        alloc = [0, 0, 0]
        for _ in range(seats):
            q = [v[i] / (alloc[i] + 1) for i in range(3)]
            alloc[q.index(max(q))] += 1
        stem = (f'In a regional list election, the {ps[0]} win {v[0]:,} votes, the {ps[1]} {v[1]:,} and the {ps[2]} {v[2]:,}. {seats} seats are shared using the '
                'D\'Hondt method (divide each party\'s votes by 1, 2, 3 … and give seats to the largest quotients). How many seats does each party win?')
        return dict(stem=stem, answer=', '.join(f'{p} {a}' for p, a in zip(ps, alloc)), type='numerical', marks=3,
                    markingKey='Quotients v/1, v/2, v/3 …; award the ' + str(seats) + ' largest (M1). Result: ' + ', '.join(f'{p} {a}' for p, a in zip(ps, alloc)) + ' (A2).', gap='G3')
    K.add(key, c, d, dhondt, 'numerical')


def footprint(K, key, c=('C3', 'C4'), d=(1, 5)):
    def co2(rng, slot):
        co, mt, pop = rng.choice(CO2)
        v = mt / pop
        if slot.d <= 2:
            stem = f'In 2022 {co} emitted about {mt:,} million tonnes of CO₂ from fossil fuels and had about {pop:,} million people. Calculate the emissions per person.'
            return dict(stem=stem, answer=f'about {v:.1f} tonnes per person', type='numerical', marks=2,
                        markingKey=f'{mt:,} Mt ÷ {pop:,} m = {v:.1f} t per person (M1 A1).', gap='G3')
        co2_, mt2, pop2 = rng.choice([x for x in CO2 if x[0] != co])
        v2 = mt2 / pop2
        stem = (f'2022 estimates: {co} – {mt:,} Mt CO₂, {pop:,} million people; {co2_} – {mt2:,} Mt CO₂, {pop2:,} million people. Calculate per-capita emissions for each and '
                'explain why total and per-capita figures can lead to different conclusions about responsibility for climate change.')
        return dict(stem=stem, answer=f'{co}: {v:.1f} t; {co2_}: {v2:.1f} t', type='multi_step', marks=5,
                    markingKey=f'{co} {v:.1f} t/person (A1); {co2_} {v2:.1f} t/person (A1). Explanation (3): a country with a large population can have high total but '
                               'low per-capita emissions; historical (cumulative) emissions and consumption-based accounting (imported goods) also change the picture.', gap='G5')
    K.add(key, c, d, co2, 'numerical')

    def earths(rng, slot):
        # (who, typical national per-person footprint in gha, approx. Global Footprint Network)
        who, fp = rng.choice([('a family in Qatar', 14.3), ('a student in Germany', 4.7), ('a household in India', 1.2), ('a family in Canada', 7.7),
                              ('a farmer in Malawi', 0.7), ('a student in Japan', 4.5), ('a family in the United States', 8.0), ('a household in Brazil', 2.6)])
        bc = 1.6
        e = round(fp / bc + 1e-9, 2)
        stem = (f'The ecological footprint of {who} is estimated at {fp} global hectares (gha) per person, close to the national average. The Earth\'s biocapacity is about {bc} gha per person. '
                'How many Earths would be needed if everyone lived this way? Comment on what this means for sustainability.')
        return dict(stem=stem, answer=f'{e:.2f} Earths', type='numerical', marks=3,
                    markingKey=f'{fp} ÷ {bc} = {e:.2f} Earths (M1 A1). Comment (R1): above 1 means consumption exceeds what the planet can regenerate (ecological overshoot); below 1 is within limits.', gap='G3')
    K.add(key, c, d, earths, 'numerical')


def rate_of_change(K, key, series, c=('C3', 'C4'), d=(2, 5)):
    """series: (what, unit, [(year, value), ...], source)."""
    def roc(rng, slot):
        what, unit, pts, srcn = rng.choice(series)
        (y1, v1), (y2, v2) = sorted(rng.sample(pts, 2))
        r = (v2 - v1) / (y2 - y1)
        tbl = '; '.join(f'{y}: {v:g} {unit}' for y, v in pts)
        stem = (f'The data show {what} ({srcn}): {tbl}. Calculate the average rate of change per year between {y1} and {y2}, and per decade.'
                if slot.d <= 3 else
                f'The data show {what} ({srcn}): {tbl}. Calculate the average rate of change per year between {y1} and {y2}, and use the data to describe whether the change is speeding up or slowing down.')
        early = (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0])
        late = (pts[-1][1] - pts[-2][1]) / (pts[-1][0] - pts[-2][0])
        trend = 'speeding up' if late > early else 'slowing down'
        return dict(stem=stem, answer=f'{r:+.3g} {unit} per year ({r * 10:+.3g} per decade)' + ('' if slot.d <= 3 else f'; {trend}'),
                    type='numerical' if slot.d <= 3 else 'multi_step', marks=3 if slot.d <= 3 else 5,
                    markingKey=f'({v2:g} − {v1:g}) ÷ ({y2} − {y1}) = {r:+.3g} {unit}/year (M1 A1); × 10 = {r * 10:+.3g} per decade (A1).' +
                               ('' if slot.d <= 3 else f' Earliest interval {early:+.3g}/yr vs latest {late:+.3g}/yr → {trend} (R2, data quoted).'), gap='G3')
    K.add(key, c, d, roc, 'numerical')


# ---------------------------------------------------------------------------------------------------------------
# Inquiry-skill generators (criteria B and C)
# ---------------------------------------------------------------------------------------------------------------
BOOKS = [  # (last, first, initials, MLA title, APA title, publisher, year)
    ('Frankopan', 'Peter', 'P.', 'The Silk Roads: A New History of the World', 'The silk roads: A new history of the world', 'Bloomsbury', 2015),
    ('Crosby', 'Alfred W.', 'A. W.', 'The Columbian Exchange: Biological and Cultural Consequences of 1492', 'The Columbian exchange: Biological and cultural consequences of 1492', 'Greenwood', 1972),
    ('Harari', 'Yuval Noah', 'Y. N.', 'Sapiens: A Brief History of Humankind', 'Sapiens: A brief history of humankind', 'Harvill Secker', 2014),
    ('Dalrymple', 'William', 'W.', 'The Anarchy: The Relentless Rise of the East India Company', 'The anarchy: The relentless rise of the East India Company', 'Bloomsbury', 2019),
    ('Marshall', 'Tim', 'T.', 'Prisoners of Geography: Ten Maps That Tell You Everything You Need to Know About Global Politics', 'Prisoners of geography: Ten maps that tell you everything you need to know about global politics', 'Elliott and Thompson', 2015),
    ('Beard', 'Mary', 'M.', 'SPQR: A History of Ancient Rome', 'SPQR: A history of ancient Rome', 'Profile Books', 2015),
    ('Raworth', 'Kate', 'K.', 'Doughnut Economics: Seven Ways to Think Like a 21st-Century Economist', 'Doughnut economics: Seven ways to think like a 21st-century economist', 'Random House Business', 2017),
    ('Hobsbawm', 'Eric', 'E.', 'The Age of Revolution: 1789–1848', 'The age of revolution: 1789–1848', 'Weidenfeld and Nicolson', 1962),
]


def citation(K, key, c='C3', d=(1, 4)):
    def cite(rng, slot):
        last, first, ini, mla_t, apa_t, pub, yr = rng.choice(BOOKS)
        style_ = rng.choice(['MLA (9th edition)', 'APA (7th edition)'])
        mla = f'{last}, {first}. {mla_t}. {pub}, {yr}.'
        apa = f'{last}, {ini} ({yr}). {apa_t}. {pub}.'
        ans = mla if style_.startswith('MLA') else apa
        stem = (f'You used a book by {first} {last} called "{mla_t}", published by {pub} in {yr}. Write the entry for your bibliography in {style_} format '
                '(write the title in plain text; it would be italicised in a typed document).')
        return dict(stem=stem, answer=ans, type='short', marks=2,
                    markingKey=f'{ans} 1 mark for correct order of elements (author, title, publisher, date{" in brackets after the author" if "APA" in style_ else " at the end"}); '
                               f'1 mark for punctuation and {"sentence-case title and initials" if "APA" in style_ else "full first name and title case"}. Criterion C iii: documenting sources.', gap='G3')
    K.add(key, c, d, cite, 'short', 'comm')

    def cite_mcq(rng, slot):
        last, first, ini, mla_t, apa_t, pub, yr = rng.choice(BOOKS)
        right = f'{last}, {ini} ({yr}). {apa_t}. {pub}.'
        wr = [f'{first} {last}. {mla_t}. {pub}, {yr}.', f'{last}, {first}. {mla_t}. {pub}, {yr}.', f'{apa_t}. ({yr}). {last}, {ini} {pub}.']
        return mcq(rng, f'Which of these is the correct APA (7th edition) reference for {first} {last}\'s book "{mla_t}" ({pub}, {yr})?', right, wr,
                   'APA: Author surname, initials (year). Title in sentence case. Publisher.')
    K.add(key, 'C3', (1, 3), cite_mcq, 'mcq', 'comm')


GRAPH_CTX = [
    ('how the population of Lagos changed every five years from 1950 to 2020', 'A line graph', 'it shows change over time continuously'),
    ('the percentage of Kenya\'s electricity that came from each energy source in 2023', 'A pie chart (or divided bar)', 'it shows parts of a whole that add up to 100%'),
    ('the number of international tourists visiting six different countries in 2019', 'A bar chart', 'it compares separate categories'),
    ('whether countries with higher GDP per capita have higher life expectancy', 'A scatter graph', 'it shows the relationship (correlation) between two variables'),
    ('average income in each province of South Africa', 'A choropleth map', 'it shows how a value varies between areas'),
    ('the movement of migrants from five countries to Germany', 'A flow-line map', 'arrow width shows the size of each flow between places'),
    ('monthly temperature and rainfall in Mumbai', 'A climate graph (bars for rainfall, line for temperature)', 'it combines two variables measured monthly'),
    ('the age and sex structure of Japan\'s population', 'A population pyramid', 'it shows males and females in each age group'),
    ('how pebble size changes with distance downstream', 'A scatter graph', 'distance and size are both continuous variables and the trend can be seen'),
    ('the number of votes won by each party in an election', 'A bar chart', 'it compares separate categories'),
]


def graph_choice(K, key, c='C3', d=(1, 3)):
    def gc(rng, slot):
        ctx, right, why = rng.choice(GRAPH_CTX)
        others = list({g for _, g, _ in GRAPH_CTX if g != right})
        rng.shuffle(others)
        return mcq(rng, f'A student wants to present data on {ctx}. Which is the most appropriate way to present it?', right, others[:3],
                   f'{right}: {why}.')
    K.add(key, c, d, gc, 'mcq', 'comm')

    def gj(rng, slot):
        ctx, right, why = rng.choice(GRAPH_CTX)
        return dict(stem=f'Suggest and justify the most appropriate graph or map to present data on {ctx}. State two features your graph must include.',
                    answer=f'{right} – {why}', type='explain', marks=3,
                    markingKey=f'{right} (1); justification: {why} (1); features (1): title, labelled axes with units or key, scale, source of data. Criterion C ii.', gap='G2')
    K.add(key, ('C2', 'C3'), (2, 4), gj, 'explain', 'comm')


def sampling(K, key, c='C3', d=(1, 4)):
    def samp(rng, slot):
        pop_ = rng.choice([240, 360, 480, 600, 750, 900, 1200])
        n = rng.choice([20, 24, 30, 40, 50, 60])
        if pop_ % n:
            return None
        k = pop_ // n
        grp = rng.choice(['students in a school', 'households on a housing estate', 'visitors to a national park on one day', 'shoppers on a high street'])
        if slot.d <= 2:
            stem = f'A student wants to survey {n} of the {pop_} {grp} using systematic sampling. What sampling interval should be used, and how would the sample be chosen?'
            return dict(stem=stem, answer=f'Every {k}th person', type='numerical', marks=2,
                        markingKey=f'Interval = population ÷ sample = {pop_} ÷ {n} = {k} (M1); start at a random number from 1 to {k}, then select every {k}th (A1).', gap='G3')
        a = rng.randint(2, 5) * 10
        share = a / 100
        sa = round(n * share)
        stem = (f'Of the {pop_} {grp}, {a}% are under 16. A student wants a stratified sample of {n}. How many people under 16 should be surveyed, and why is a '
                'stratified sample better than a random one here?')
        return dict(stem=stem, answer=f'{sa} people under 16', type='multi_step', marks=3,
                    markingKey=f'{a}% × {n} = {sa} (M1 A1). Stratified sampling makes each group represented in proportion, avoiding bias (R1).', gap='G3')
    K.add(key, c, d, samp, 'numerical', 'inquiry')

    def tally(rng, slot):
        cats = rng.sample(['car', 'bus', 'walking', 'bicycle', 'train', 'scooter'], 4)
        v = [rng.randint(3, 30) for _ in cats]
        tot = sum(v)
        pc = [x / tot * 100 for x in v]
        ang = [x / tot * 360 for x in v]
        stem = ('A survey of how students travel to school gave these results: ' + ', '.join(f'{c_} {x}' for c_, x in zip(cats, v)) +
                '. Calculate the percentage for each category and the angle each would have in a pie chart.')
        return dict(stem=stem, answer='; '.join(f'{c_} {p:.1f}% ({a:.0f}°)' for c_, p, a in zip(cats, pc, ang)), type='numerical', marks=4,
                    markingKey=f'Total = {tot} (A1); % = value ÷ {tot} × 100 (M1); angle = value ÷ {tot} × 360 (M1); ' +
                               '; '.join(f'{c_} {p:.1f}%, {a:.0f}°' for c_, p, a in zip(cats, pc, ang)) + ' (A1, angles sum to 360°).', gap='G3')
    K.add(key, c, d, tally, 'numerical', 'comm')
