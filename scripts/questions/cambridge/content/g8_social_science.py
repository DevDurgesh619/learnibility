"""Cambridge Lower Secondary Humanities 0839, Stage 9 (grade 8): Past, Places, People.

School-assessed paper in the style of IGCSE History / Geography: recall, explanation,
source-, map- and data-based items, and 'how far' essays.

Each topic is built from a knowledge pack (key terms, dated events, explanations,
misconceptions, sources, case studies, essay claims) by the generic builders below,
plus topic-specific data templates (grid references, climate tables, population data ...).
"""
import math
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


# ============================================================== generic builders

def _year_ds(y):
    return [str(y + d) for d in (-11, -6, -3, -1, 2, 4, 7, 13)]


def add_terms(t, terms):
    """terms: [(term, definition)] -> two C1 items per term (definition -> term, term -> definition)."""
    if len(terms) < 4:
        return
    t.fixed('C1', (1, 2), [(f'Name the term that matches this definition: “{d}”.', cap(term), f'{cap(term)}: {d}. [1]',
                            [cap(x) for x, _ in terms if x != term]) for term, d in terms])
    t.fixed('C1', (2, 3), [(f'What is meant by the term “{term}”?', cap(d) + '.', f'{cap(term)}: {d}. [1]',
                            [cap(y) + '.' for x, y in terms if x != term]) for term, d in terms])


def add_mcqs(t, C, D, entries):
    """entries: (stem, answer, [3+ distractors], key) as stand-alone MCQ templates (not auto-paired)."""
    for e in entries:
        stem, ans, ds, key = e

        def fn(r, D_, stem=stem, ans=ans, ds=ds, key=key):
            opts, a = mcq(r, ans, list(ds))
            return {'stem': stem, 'options': opts, 'answer': a, 'key': key}
        fn.__name__ = 'mcq'
        t.add(C, D, 'mcq')(fn)


def add_dates(t, dates):
    """dates: [(clause, year[, month])] -> C1 year MCQs and C2 chronology items."""
    if not dates:
        return
    t.fixed('C1', (1, 2), [(f'Identify the year in which this happened: {d[0]}.', str(d[1]), f'{cap(d[0])} in {d[1]}. [1]', _year_ds(d[1])) for d in dates])
    if len(dates) < 4:
        return

    def chrono(r, D):
        n = 4 if D <= 2 else 5
        if len(dates) < n:
            n = len(dates)
        ev = r.sample(dates, n)
        keys = [(d[1], d[2] if len(d) > 2 else 0) for d in ev]
        for i in range(n):
            for j in range(i + 1, n):
                if keys[i][0] == keys[j][0] and (keys[i][1] == 0 or keys[j][1] == 0 or keys[i][1] == keys[j][1]):
                    return None
        lab = 'ABCDE'[:n]
        order = sorted(range(n), key=lambda i: keys[i])
        lead = r.choice(['Put these events in chronological order, starting with the earliest.',
                         'Arrange these events in the order in which they happened, earliest first.',
                         'Sequence these events from earliest to latest.'])
        stem = lead + ' ' + ' '.join(f'{lab[i]}: {cap(ev[i][0])}.' for i in range(n))
        if D >= 3:
            stem += ' Then state the year of the earliest and the latest event.'
        ans = ', '.join(lab[i] for i in order) + ' (' + '; '.join(f'{lab[i]} {ev[i][1]}' for i in order) + ')'
        mk = 2 if D <= 2 else 3
        return {'stem': stem, 'answer': ans, 'key': f'Correct order {ans}. 2 marks all correct; 1 mark if one adjacent pair is reversed.' + (' 1 mark for both years.' if D >= 3 else '') + f' [{mk}]',
                'type': 'short', 'marks': mk}
    t.add('C2', (1, 2, 3), 'short')(chrono)


def add_explain(t, entries, D=(2, 3, 4)):
    """entries: (stem, answer, key-with-[n])."""
    t.fixed('C2', D, entries, type='explain')


def add_claims(t, claims):
    """claims: [(claim, is_correct, explanation)] -> claim-checking C2 items."""
    ents = []
    for i, (c, ok, why) in enumerate(claims):
        lead = ['A student writes:', 'In a class discussion, a student says:', 'A revision website states:', 'A classmate claims:'][i % 4]
        ents.append((f'{lead} “{c}” Is this correct? Explain your answer.', ('Correct. ' if ok else 'Not correct. ') + why,
                     '1 mark correct judgement; 1 mark accurate supporting explanation [2]'))
    t.fixed('C2', (1, 2, 3), ents, type='explain')


ESSAY_LEADS = [
    lambda c, p: f'“{cap(c)}.” How far do you agree with this statement? Explain your answer.',
    lambda c, p: f'How far do you agree that {c}? Use your own knowledge to support your answer.',
    lambda c, p: f'Evaluate the view that {c}.',
    lambda c, p: f'{p} argues that {c}. To what extent do you agree? Give reasons for and against before reaching a judgement.',
    lambda c, p: f'“{cap(c)}.” Discuss this view, explaining points for and against, and reach a supported conclusion.',
]


def add_essay(t, claim, pro, con, judge, hints=(), D=(2, 3, 4, 5)):
    """'How far' / evaluate essay (C4, type long)."""
    def fn(r, D_):
        p = person(r)
        if D_ <= 2:
            stem = f'Explain whether you agree that {claim}. Give one reason for and one reason against.'
            lv = 'Level 1 (1 mark): one simple reason. Level 2 (2-3 marks): one explained reason for AND one against, with accurate detail.'
        else:
            stem = r.choice(ESSAY_LEADS)(claim, p)
            if hints and r.random() < 0.7:
                hs = r.sample(list(hints), min(len(hints), r.choice([2, 3])))
                stem += ' You may wish to consider: ' + '; '.join(hs) + '.'
            lv = ('Level 1: simple, generalised statements. Level 2: explains one side with accurate supporting detail. '
                  'Level 3: explains both sides with detail. Level 4 (top marks): balanced, well-supported argument and a reasoned judgement on "how far".')
        ans = 'Agree: ' + ' '.join(pro) + ' Disagree: ' + ' '.join(con) + ' Judgement: ' + judge
        return {'stem': stem, 'answer': ans, 'key': lv, 'type': 'long'}
    fn.__name__ = 'essay'
    t.add('C4', D, 'long')(fn)


def _src_parts(s, L, who):
    kind = s['kind']
    why = s.get('why') or ('it comes from the time being studied, or from someone directly involved in the events' if kind == 'primary'
                           else 'it was produced later by someone who was not there, using other evidence')
    return [
        lambda r: (f'Is Source {L} a primary or a secondary source? Give a reason for your answer.', f'{cap(kind)} source: {why}.', '1 mark correct type; 1 mark reason based on its origin/date [2]'),
        lambda r: (f'What can you infer from Source {L} about {s["about"]}?', s['infer'], '1 mark valid inference; 1 mark supported with a detail from the source [2]'),
        lambda r: (f'Suggest the purpose of Source {L}. Explain your answer.', s['purpose'], '1 mark purpose; 1 mark link to author/audience/date [2]'),
        lambda r: (f'Explain one reason why Source {L} may be reliable and one reason why it may not be reliable.', f'May be reliable: {s["plus"]}. May not be reliable: {s["minus"]}.', '2 marks for each explained reason based on provenance (author, date, purpose) [4]'),
        lambda r: (f'Use your own knowledge to describe one aspect of {s["about"]} that Source {L} does not show.', s['missing'], '1 mark accurate own knowledge; 1 mark developed [2]'),
        lambda r: (f'How useful is Source {L} to {who} investigating {s["enq"]}? Explain your answer using its content and provenance.',
                   f'Useful because {low(s["infer"])} Provenance: {s["plus"]}. Limits: {s["minus"]}; also it does not show {low(s["missing"]).rstrip(".")}. Judgement: useful but should be cross-referenced with other sources.',
                   'Level 1 (1-2): simple comment on content or provenance. Level 2 (3-4): explains usefulness using content AND provenance. Level 3 (5): balanced judgement including limitations [5]'),
    ]


def add_source(t, s, who='a historian'):
    """s: dict(prov, text, kind, about, infer, purpose, plus, minus, missing, enq[, why])."""
    def mk(k, typ):
        def fn(r, D):
            L = r.choice('ABCD')
            intro = r.choice([
                f'Study Source {L}, {s["prov"]}. “{s["text"]}”',
                f'Source {L} is taken from {s["prov"]}. It says: “{s["text"]}” Use it to answer the questions.',
                f'A student investigating {s["enq"]} finds Source {L}. Source {L}: {s["prov"]}. “{s["text"]}”',
                f'Read Source {L} carefully. “{s["text"]}” ({cap(s["prov"])}.)',
            ])
            return compose(r, intro, _src_parts(s, L, who), k=k, type_=typ)
        fn.__name__ = 'source'
        return fn
    t.add('C3', (2, 3, 4, 5), 'case')(mk((2, 3), 'case'))
    t.add('C4', (3, 4, 5), 'case')(mk((3, 4), 'case'))


def add_case(t, intros, parts, C3=(2, 3, 4, 5), C4=(3, 4, 5)):
    """Case study / scenario: intros (list of str), parts [(q, a, key-with-[n])]."""
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


import re as _re


def _markify(t, start):
    """Give fixed items the marks stated in their key ([n]) so marks and key agree."""
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
    add_dates(t, P.get('dates', []))
    if P.get('mcq'):
        add_mcqs(t, 'C1', (1, 2, 3), P['mcq'])
    if P.get('explain'):
        add_explain(t, P['explain'])
    if P.get('claims'):
        add_claims(t, P['claims'])
    for s in P.get('sources', []):
        add_source(t, s, P.get('who', 'a historian'))
    for c in P.get('cases', []):
        add_case(t, c[0], c[1])
    for e in P.get('essays', []):
        add_essay(t, *e)
    _markify(t, start)
    return t


def table(headers, rows):
    """Render a small table in words: 'Header: a | b | c. Row: ...'."""
    out = ' | '.join(headers) + '. '
    out += ' '.join(' | '.join(str(x) for x in row) + '.' for row in rows)
    return out


# ============================================================== climate data (shared ch1/ch6)

ZONES = {
    'equatorial (tropical rainforest)': ([26.5, 27, 27.5, 28, 28, 28, 27.5, 27.5, 27.5, 27.5, 27, 26.5], [240, 165, 185, 180, 170, 160, 155, 170, 165, 190, 255, 290], 'N', 1),
    'hot desert': ([14, 17, 21, 26, 32, 34, 35, 35, 32, 27, 20, 15], [15, 10, 25, 30, 10, 0, 0, 0, 0, 2, 10, 15], 'N', 24),
    'Mediterranean': ([10, 11, 13, 15, 19, 23, 26, 26, 23, 19, 14, 11], [55, 45, 40, 35, 20, 8, 3, 4, 12, 45, 55, 65], 'N', 38),
    'temperate maritime': ([5, 5, 7, 9, 13, 16, 18, 18, 15, 12, 8, 5], [55, 40, 40, 45, 50, 45, 45, 50, 50, 65, 60, 55], 'N', 51),
    'tropical monsoon': ([24, 25, 27, 29, 30, 29, 28, 27, 28, 29, 28, 26], [1, 1, 0, 1, 15, 500, 840, 560, 330, 70, 15, 2], 'N', 19),
    'cold continental': ([-7, -6, -1, 6, 13, 17, 19, 17, 11, 5, -1, -5], [50, 40, 35, 40, 55, 80, 85, 80, 65, 65, 55, 50], 'N', 56),
    'polar (tundra)': ([-28, -29, -27, -19, -8, 1, 5, 4, -1, -11, -21, -25], [10, 10, 10, 10, 10, 15, 25, 30, 25, 20, 15, 10], 'N', 70),
    'Mediterranean (southern hemisphere)': ([21, 21, 20, 18, 15, 13, 12, 13, 14, 16, 18, 20], [15, 15, 20, 50, 90, 85, 90, 75, 45, 30, 15, 15], 'S', 34),
}
ZONE_NOTES = {
    'equatorial (tropical rainforest)': 'hot all year (about 27 °C), a very small temperature range and over 2000 mm of rain spread through the year',
    'hot desert': 'very low rainfall (under 250 mm a year) and very hot summers',
    'Mediterranean': 'hot, dry summers and mild, wet winters',
    'temperate maritime': 'mild winters, cool summers and moderate rain in every month',
    'tropical monsoon': 'high temperatures all year and a very wet season (June to September) followed by a long dry season',
    'cold continental': 'very cold winters below 0 °C, warm summers and a large annual temperature range',
    'polar (tundra)': 'temperatures below 0 °C for most of the year and very low precipitation',
    'Mediterranean (southern hemisphere)': 'warm, dry summers in December to February and mild, wet winters in June to August',
}


def climate(r, zone=None):
    zone = zone or r.choice(list(ZONES))
    tt, pp, hemi, lat = ZONES[zone]
    temps = [round(x + r.choice([-1, -0.5, 0, 0, 0.5, 1]), 1) for x in tt]
    temps = [int(x) if x == int(x) else x for x in temps]
    f = r.choice([0.9, 0.95, 1.0, 1.05, 1.1])
    prec = [int(5 * round(p * f / 5)) if p >= 10 else p for p in pp]
    return zone, temps, prec, hemi, lat


def climate_text(temps, prec):
    return ('Temperature (°C): ' + ', '.join(f'{m} {fmt(x, 1)}' for m, x in zip(MON, temps)) +
            '. Precipitation (mm): ' + ', '.join(f'{m} {p}' for m, p in zip(MON, prec)) + '.')


def climate_stats(temps, prec):
    hi, lo = max(temps), min(temps)
    rng = round(hi - lo, 1)
    tot = sum(prec)
    wet = MONTHS[prec.index(max(prec))]
    mean = round(sum(temps) / 12, 1)
    return hi, lo, rng, tot, wet, mean


# ============================================================== CHAPTER 1: Enquiry, sources and evidence

c1a = T('Asking enquiry questions and planning a humanities investigation', 'enquiry questions', 'planning investigation')
build(c1a, {
    'terms': [
        ('enquiry question', 'a focused question that guides an investigation and can be answered using evidence'),
        ('hypothesis', 'a statement or prediction that can be tested by collecting evidence'),
        ('primary data', 'information collected first-hand by the investigator, for example by a survey, count or measurement'),
        ('secondary data', 'information that has already been collected or published by someone else, such as census figures or a textbook'),
        ('sample', 'a smaller group chosen from a larger population to represent it'),
        ('random sampling', 'choosing people or sites so that each one has an equal chance of being selected'),
        ('systematic sampling', 'choosing people or sites at regular intervals, for example every tenth house'),
        ('pilot study', 'a small trial run of a method to find and fix problems before the main investigation'),
        ('qualitative data', 'information in words, images or descriptions rather than numbers'),
        ('quantitative data', 'information in the form of numbers that can be counted or measured'),
    ],
    'mcq': [
        ('Which of these is the most suitable enquiry question for a school investigation?', 'How has the number of shops in our town centre changed since 2010, and why?',
         ['Are shops good?', 'What is a shop?', 'Why is everything in town worse than it used to be?'], 'A good enquiry question is focused, open and answerable with evidence; the others are vague, closed or biased. [1]'),
        ('Which of these is an example of a closed question in a questionnaire?', 'Do you use the bus to get to school? (Yes / No)',
         ['What do you think about public transport in your area?', 'Describe your journey to school.', 'Why do you prefer walking to taking the bus?'], 'A closed question has a fixed set of answers, which makes results easy to count. [1]'),
        ('Which of these is qualitative data?', 'Interview comments about how safe residents feel at night',
         ['A count of 214 cars in one hour', 'The population of a town in the 2021 census', 'Rainfall of 35 mm on one day'], 'Qualitative data is descriptive (words/opinions); the others are numbers. [1]'),
        ('Which of these statements is an opinion rather than a fact?', 'The new shopping centre is the best thing that has happened to the town.',
         ['The new shopping centre opened in 2019.', 'The shopping centre has 85 shops.', 'The shopping centre car park has 600 spaces.'], 'An opinion is a personal view that cannot be proved; the others can be checked. [1]'),
        ('A student wants to find out how far people travel to visit a market. Which method collects primary data?', 'Asking shoppers at the market where they have travelled from',
         ['Reading a council report about the market', 'Looking at a website about markets', 'Using census data on car ownership'], 'Primary data is collected first-hand by the investigator. [1]'),
        ('What is the main reason for doing a pilot study before a survey?', 'To find and fix problems with the questions or method',
         ['To make the results agree with the hypothesis', 'To avoid having to do the main survey', 'To collect secondary data'], 'A pilot tests the method so the main data collection works well. [1]'),
        ('Which of these is a stage in the enquiry process that comes before collecting data?', 'Planning methods and choosing a sample',
         ['Writing the conclusion', 'Evaluating the results', 'Drawing graphs of the results'], 'Order: question/hypothesis → plan → collect → present → analyse → conclude → evaluate. [1]'),
    ],
    'explain': [
        ('Explain why an enquiry question should be focused rather than very broad.', 'A focused question tells the investigator exactly what data to collect and can be answered within the time and resources available; a broad question cannot be answered properly with evidence.', '1 mark: guides data collection; 1 mark: can be answered with available time/evidence [2]'),
        ('Explain one advantage and one disadvantage of using a questionnaire to find out people’s views.', 'Advantage: it can collect answers from many people quickly and closed questions are easy to compare. Disadvantage: people may not answer honestly or may misunderstand questions; response rates can be low.', '1 mark each for an explained advantage and disadvantage [2]'),
        ('Explain why investigators often use both primary and secondary data.', 'Primary data is up to date and collected for the exact question; secondary data gives a wider picture or a longer time period that the investigator could not collect alone, and allows comparison.', '1 mark: value of primary; 1 mark: value of secondary/comparison [2]'),
        ('Explain why it is important to ask permission and keep answers anonymous when interviewing people.', 'It is ethical: people have a right to privacy and to choose to take part; anonymity also encourages honest answers and protects people from harm.', '1 mark: ethics/consent/privacy; 1 mark: effect on honesty or protection [2]'),
        ('Explain why a larger sample usually gives more reliable results.', 'A larger sample is more likely to represent the whole population, so a few unusual answers have less effect on the results.', '1 mark: more representative; 1 mark: reduces effect of anomalies [2]'),
        ('Describe the difference between random and systematic sampling, and explain one reason for choosing systematic sampling.', 'Random: every person/site has an equal chance of being picked (e.g. random numbers). Systematic: picks at regular intervals (e.g. every 5th person). Systematic sampling is quick and easy and spreads the sample evenly.', '1 mark each definition; 1 mark reason [3]'),
        ('Explain why a hypothesis is useful at the start of an investigation.', 'It gives a clear prediction to test, so the investigator knows what data to collect and can decide at the end whether the evidence supports it.', '1 mark: clear testable prediction; 1 mark: guides data/conclusion [2]'),
    ],
    'claims': [
        ('A hypothesis must be proved correct for an investigation to be successful.', False, 'Finding that the evidence does not support a hypothesis is still a valid result; the conclusion explains why.'),
        ('Secondary data is always less reliable than primary data.', False, 'Reliability depends on who collected the data and how; official secondary data such as a census can be very reliable.'),
        ('Open questions are easier to turn into graphs than closed questions.', False, 'Closed questions have fixed answers that can be counted and graphed; open answers need to be sorted into categories first.'),
        ('Asking only your friends is a fair way to find out what everyone in your school thinks.', False, 'Friends are not a representative sample; they may share views, so the results would be biased.'),
        ('Carrying out a pilot study can save time in the main investigation.', True, 'It finds unclear questions or problems with the method before the main data collection, so data does not have to be collected again.'),
    ],
    'essays': [
        ('primary data is always more useful than secondary data in a humanities investigation',
         ['Primary data is collected for the exact question and is up to date.', 'The investigator knows how it was collected, so its reliability can be judged.'],
         ['Secondary data such as a census covers far more people and places than a student could survey.', 'Secondary data gives change over time (e.g. past maps or records) that cannot be collected now.', 'Primary data from small samples may be unrepresentative.'],
         'Usefulness depends on the question; the best enquiries combine both kinds and cross-check them.',
         ['sample size', 'time periods', 'reliability of who collected the data', 'cost and time']),
        ('a questionnaire is the best way to find out people’s views on a local issue',
         ['It reaches many people quickly.', 'Closed questions give data that is easy to compare and graph.'],
         ['People may not answer honestly or may misunderstand questions.', 'Interviews give more detailed reasons.', 'Who is asked (sampling) matters more than the method itself.'],
         'A questionnaire is useful but works best alongside interviews and a carefully chosen sample.',
         ['open and closed questions', 'sampling', 'interviews', 'honesty of answers']),
    ],
})

PLANS = [
    ('A class in {c} is investigating whether a new shopping mall on the edge of town has affected small shops in the town centre.',
     'The opening of the mall has led to more empty shops in the town centre.', 'counting empty shop units along the main street; questionnaires with shopkeepers and shoppers',
     'council records of business rates or old photographs of the street', 'a bar chart comparing empty shops before and after, and a map showing their locations'),
    ('Students in {c} want to find out how traffic on the road outside their school changes during the day.',
     'Traffic is heaviest at the start and end of the school day.', 'traffic counts for 10 minutes every hour; noting the type of vehicle',
     'local council traffic surveys', 'a line graph of vehicles per hour through the day'),
    ('A group in {c} is investigating how the local river changes from its source to its mouth.',
     'The river becomes wider and deeper further downstream.', 'measuring width and depth at several sites; timing a float to work out speed',
     'maps showing the river course and gradient', 'cross-section diagrams for each site and a scatter graph of width against distance'),
    ('Students in {c} are investigating how life in their town changed after the railway arrived in the 19th century.',
     'The railway caused the town’s population and number of factories to grow.', 'interviewing a local historian; photographing old buildings near the station',
     'census figures from 1841 to 1901, old maps and trade directories', 'a line graph of population and a pair of maps from before and after the railway'),
    ('A class in {c} is investigating whether people feel safe walking in different parts of their neighbourhood.',
     'People feel less safe in areas with poor street lighting.', 'questionnaires using a 1-5 safety score; an environmental quality survey of lighting and litter',
     'crime statistics published by the local police', 'a map with proportional symbols showing average safety scores'),
    ('Students in {c} want to know how far visitors travel to use the town’s weekly market.',
     'Most visitors to the market travel less than 5 km.', 'asking shoppers where they have travelled from; counting visitors each hour',
     'a map of bus routes and the town’s population data', 'a desire-line map and a histogram of distances travelled'),
    ('A group in {c} is investigating how a local memorial is used to remember people who died in war.',
     'The memorial is mainly visited on Remembrance Day.', 'counting visitors on different days; interviewing visitors about why they came',
     'newspaper reports of past ceremonies and the names list from the war graves records', 'a bar chart of visitors by day and a short set of quotations'),
]


@c1a.add('C3', (2, 3, 4, 5), 'case')
def c1a_plan(r, D):
    sc, hyp, prim, sec, pres = r.choice(PLANS)
    c = city(r)
    intro = sc.format(c=c)
    parts = [
        lambda r: ('Write a suitable hypothesis for this investigation.', hyp, '1 mark testable statement linked to the enquiry [1]'),
        lambda r: ('Suggest two methods of collecting primary data for this investigation.', cap(prim) + '.', '1 mark each appropriate method [2]'),
        lambda r: ('Identify one source of secondary data that would help, and explain why.', cap(sec) + ', because it gives evidence from a longer time period or a wider area than the students can collect.', '1 mark source; 1 mark reason [2]'),
        lambda r: ('Explain how the students could choose a fair sample.', 'Use random or systematic sampling (e.g. every 5th person or site at regular intervals) and collect enough data at different times/places so the sample is representative.', '1 mark named sampling method; 1 mark explained fairness/representativeness [2]'),
        lambda r: ('Suggest how the results could be presented, giving a reason.', cap(pres) + ', because it shows the pattern clearly and allows comparison.', '1 mark suitable presentation; 1 mark reason [2]'),
        lambda r: ('Identify one ethical or safety issue the students should consider, and how to deal with it.', 'Ask permission and keep answers anonymous; work in groups, wear high-visibility clothing near roads or water and tell a teacher where they are.', '1 mark issue; 1 mark way of managing it [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


@c1a.add('C4', (3, 4, 5), 'case')
def c1a_eval(r, D):
    sc, hyp, prim, sec, pres = r.choice(PLANS)
    n = r.choice([8, 10, 12, 15, 20])
    when = r.choice(['on one Saturday morning', 'during a single lunch hour', 'on one rainy Tuesday', 'on the first day of the school holidays'])
    intro = sc.format(c=city(r)) + f' Their hypothesis is: “{hyp}” They collected data from {n} people {when}.'
    parts = [
        lambda r: ('Identify two weaknesses in the way the data was collected.', f'The sample of {n} is small and was collected {when}, so it may not represent other times or groups of people.', '1 mark each weakness [2]'),
        lambda r: ('Suggest two improvements to the method and explain how each would make the results more reliable.', 'Increase the sample size; collect data on several days and at different times; use systematic or stratified sampling; do a pilot study first. Each makes the sample more representative.', '1 mark each improvement; 1 mark each explanation [4]'),
        lambda r: ('Explain why the students should also use secondary data.', cap(sec) + ' would let them check (cross-reference) their own results and see change over a longer period.', '1 mark source/role; 1 mark explanation [2]'),
        lambda r: ('Evaluate whether the students can reach a reliable conclusion about their hypothesis.', 'Only a tentative one: the evidence may point one way, but the small, one-off sample limits reliability; with a larger, repeated sample and secondary data the conclusion would be stronger.', '1 mark evidence point; 1 mark limitation; 1 mark judgement [3]'),
    ]
    return compose(r, intro, parts, k=(3, 4), type_='case')


# --------------------------------------------------------------- 1.2 sources
SRC_GENERIC = [
    dict(prov='a diary kept by a 14-year-old cotton mill worker in Manchester, 1833 (adapted)', kind='primary',
         text='We start at half past five and the overlooker beats any child who falls asleep. My fingers bleed from the threads and there is never enough light or air.',
         about='working conditions in textile mills', infer='Conditions were harsh: very long hours, physical punishment and injuries were common for child workers.',
         purpose='To record the writer’s own daily experiences, probably for herself or her family rather than to persuade.',
         plus='it is an eyewitness account written at the time by someone who worked in the mill', minus='it describes only one mill and one person’s experience, and the writer may exaggerate when tired or angry',
         missing='How many hours were allowed by law or how conditions changed after the 1833 Factory Act.', enq='child labour in the 1830s'),
    dict(prov='a school textbook about the Industrial Revolution, published in 2015', kind='secondary',
         text='Historians estimate that children made up a large share of the workforce in early cotton mills. Many worked twelve hours or more a day before the Factory Acts.',
         about='child labour in early factories', infer='Child labour was widespread and hours were long before the law was changed.',
         purpose='To inform students with a clear overview based on historians’ research.',
         plus='it is based on research using many sources and is written with hindsight', minus='it simplifies events and does not give the voices of the children themselves',
         missing='Individual experiences such as punishments or injuries in a particular mill.', enq='child labour in the 1830s'),
    dict(prov='a letter from a mill owner to a newspaper, Lancashire, 1832 (adapted)', kind='primary',
         text='The children in my mill are well fed and cheerful. Work keeps them out of mischief, and their wages help their families. Any law limiting their hours will ruin our trade.',
         about='attitudes of factory owners to reform', infer='Some mill owners opposed factory reform and claimed children benefited from work.',
         purpose='To persuade readers and politicians not to pass laws limiting children’s working hours.',
         plus='it shows genuinely what some owners argued at the time of the 1832-33 debates', minus='the owner profits from child labour, so he has a reason to give a one-sided, positive picture',
         missing='Evidence from the children themselves, or from doctors and inspectors about injuries and health.', enq='why factory reform was controversial'),
    dict(prov='a recruitment poster issued by the British government in 1914', kind='primary',
         text='Your country needs YOU. Join your country’s army! God save the King.',
         about='how the British government encouraged men to join the army in 1914', infer='The government relied on volunteers and used patriotic, personal appeals to persuade men to enlist.',
         purpose='Propaganda: to persuade men to volunteer for the army at the start of the war.',
         plus='it is an official source from 1914, so it shows exactly what message the government wanted to spread', minus='it is propaganda, so it tells us what the government wanted people to think, not how people actually felt',
         missing='How many men actually joined, or why conscription was introduced in 1916.', enq='recruitment in Britain during the First World War'),
    dict(prov='an interview with a survivor of the 2015 Nepal earthquake, recorded by a charity in 2016 (adapted)', kind='primary',
         text='Our village above Gorkha was cut off for nine days because landslides blocked the road. Helicopters brought rice and tarpaulins, but the monsoon came before we could rebuild.',
         about='the effects of the 2015 Nepal earthquake on rural areas', infer='Remote villages were badly affected: landslides cut them off, aid was slow to arrive and rebuilding was delayed by the monsoon.',
         purpose='To record survivors’ experiences, possibly to raise awareness and funds for the charity’s work.',
         plus='it is an eyewitness account from someone who lived through the disaster', minus='it was recorded a year later and by a charity, which may select stories that encourage donations',
         missing='Overall figures such as the number of deaths (about 9000) or the effects in Kathmandu.', enq='the impact of the 2015 Nepal earthquake'),
    dict(prov='a historian writing in 2005 about the British Empire in India', kind='secondary',
         text='British rule brought railways, telegraphs and universities to India, but they were built mainly to serve British trade and administration, and Indian industries such as hand-weaving declined.',
         about='the effects of British rule in India', infer='The effects of British rule were mixed: there was new infrastructure, but it mainly benefited Britain and harmed some Indian industries.',
         purpose='To give a balanced interpretation of British rule based on research.',
         plus='the historian has hindsight and access to many different sources', minus='it is one interpretation; historians disagree, and the extract is short and may leave out other views',
         missing='The views of Indians at the time, or events such as the 1919 Amritsar Massacre.', enq='how British rule affected India'),
]


c1b = T('Primary and secondary sources: origin, purpose and reliability', 'sources origin purpose reliability')
build(c1b, {
    'terms': [
        ('primary source', 'a source produced at the time of the events being studied, often by someone who was there'),
        ('secondary source', 'a source produced after the events, usually by someone who used other sources to interpret them'),
        ('provenance', 'the origin of a source: who produced it, when, where and why'),
        ('bias', 'a one-sided view that favours one person, group or argument over another'),
        ('propaganda', 'information designed to persuade people to think or act in a particular way, often by giving a one-sided message'),
        ('reliability', 'how far a source can be trusted to give an accurate account'),
        ('corroboration', 'checking a source against other sources to see whether they agree (cross-referencing)'),
        ('utility', 'how useful a source is for answering a particular enquiry question'),
        ('interpretation', 'a view or explanation of the past put forward by a historian or other writer'),
        ('anachronism', 'something placed in the wrong time period, such as a detail that did not exist at the time'),
    ],
    'mcq': [
        ('Which of these is a primary source for studying the Industrial Revolution?', 'A diary written by a mill worker in 1832',
         ['A textbook published in 2015', 'A television documentary made in 2010', 'A website summary written in 2022'], 'Primary sources come from the time being studied. [1]'),
        ('Which question helps you judge the provenance of a source?', 'Who produced it, when and why?',
         ['How long is the source?', 'Is the source printed in colour?', 'How many pictures does it contain?'], 'Provenance = origin: author, date, purpose, audience. [1]'),
        ('A newspaper owned by a factory owner praises working conditions in his factory. What is the main problem with this source?', 'It may be biased because the owner benefits from a positive picture',
         ['It is a secondary source', 'It is too recent to be useful', 'Newspapers never contain facts'], 'The author/owner has a motive to give a one-sided account. [1]'),
        ('Which of these is a secondary source about the First World War?', 'A historian’s book about the Battle of the Somme published in 2016',
         ['A letter written by a soldier at the Somme in 1916', 'A photograph taken in a trench in 1916', 'A 1915 recruitment poster'], 'Secondary = produced later, interpreting other sources. [1]'),
        ('What does it mean to cross-reference a source?', 'Compare it with other sources to check whether they agree',
         ['Copy it into your notes', 'Find out how much it cost to produce', 'Decide whether you like it'], 'Cross-referencing (corroboration) tests reliability. [1]'),
        ('Why might a government poster from wartime be of limited use for finding out what ordinary people thought?', 'It is propaganda showing what the government wanted people to think',
         ['It is a secondary source', 'It was produced after the war', 'Posters were never seen by ordinary people'], 'Propaganda reveals government aims, not necessarily public opinion. [1]'),
    ],
    'explain': [
        ('Explain why a primary source is not always more reliable than a secondary source.', 'A primary source may be biased, limited to one viewpoint or written for propaganda; a secondary source can draw on many sources with hindsight, so may be more balanced.', '1 mark: weakness of primary (bias/limited view); 1 mark: strength of secondary (range/hindsight) [2]'),
        ('Explain how the purpose of a source can affect its reliability.', 'If a source was made to persuade (e.g. propaganda or an advert) it may exaggerate or leave out facts, so it is less reliable as evidence of what happened, though it is good evidence of what its author wanted people to believe.', '1 mark: persuasive purpose → selective/exaggerated; 1 mark: still useful for attitudes/aims [2]'),
        ('Explain why an unreliable source can still be useful to a historian.', 'It shows the attitudes, opinions or propaganda of its author and the time it was made, which is useful for questions about views and motives.', '1 mark: shows attitudes/purpose; 1 mark: linked to a suitable enquiry [2]'),
        ('Explain why the date of a source matters when judging its reliability.', 'A source made at the time may be from an eyewitness but lack hindsight; one made much later may suffer from faulty memory or be influenced by later events, but can use more evidence.', '1 mark each point [2]'),
        ('Explain why historians use a range of sources rather than just one.', 'Each source has limits and possible bias; comparing several lets historians check facts, see different viewpoints and build a more accurate picture.', '1 mark: limits of single sources; 1 mark: corroboration/range of views [2]'),
        ('Explain the difference between the reliability and the utility of a source.', 'Reliability is how far it can be trusted to be accurate; utility is how useful it is for a particular question. A biased source can be unreliable about facts but useful for showing attitudes.', '1 mark each definition; 1 mark example/contrast [3]'),
    ],
    'claims': [
        ('A source written by someone who was there is always reliable.', False, 'Eyewitnesses may be biased, see only part of the events, misremember, or write to persuade.'),
        ('Photographs are always reliable because the camera cannot lie.', False, 'Photographs can be staged, cropped, edited or chosen to give one view; they show only one moment.'),
        ('A biased source is useless to a historian.', False, 'Biased sources are useful evidence of attitudes and propaganda at the time.'),
        ('A textbook written today is a secondary source about the Second World War.', True, 'It was produced long after the events by authors who used other sources.'),
        ('Two sources that agree must both be telling the truth.', False, 'They may share the same bias or one may have copied the other; agreement makes a claim stronger but does not prove it.'),
    ],
    'sources': SRC_GENERIC,
    'essays': [
        ('primary sources are always more valuable to historians than secondary sources',
         ['Primary sources give direct evidence from the time, including eyewitness views.', 'They show attitudes and language of the period.'],
         ['Primary sources can be biased, propaganda or limited to one view.', 'Secondary sources use many sources with hindsight and can explain causes and consequences.'],
         'Value depends on the question asked and how the source is used; historians need both and should judge each source on its provenance.',
         ['bias and purpose', 'hindsight', 'eyewitness evidence', 'the question being asked']),
        ('the provenance of a source matters more than its content when judging its usefulness',
         ['Provenance tells us whether the author was in a position to know and whether they had reasons to distort.', 'Propaganda can only be recognised by examining its origin.'],
         ['Content can be checked against own knowledge and other sources.', 'A source with doubtful provenance may still contain accurate details.'],
         'Both matter: usefulness is judged by how content and provenance together help answer a specific enquiry.',
         ['author and purpose', 'date', 'cross-referencing', 'own knowledge']),
    ],
})


@c1b.add('C2', (2, 3, 4), 'explain')
def c1b_compare(r, D):
    a, b = r.sample(SRC_GENERIC, 2)
    return {'stem': f'Source P is {a["prov"]}. Source Q is {b["prov"]}. Compare the two sources: identify which is primary and which is secondary, and explain one advantage of each for a historian.',
            'answer': f'Source P is {a["kind"]}; Source Q is {b["kind"]}. P: {a["plus"]}. Q: {b["plus"]}.',
            'key': '1 mark each correct type; 1 mark each explained advantage based on provenance [4]', 'marks': 4}


@c1b.add('C3', (1, 2, 3), 'mcq')
def c1b_type(r, D):
    s = r.choice(SRC_GENERIC)
    opts, a = mcq(r, cap(s['kind']) + ' source', ['Primary source', 'Secondary source', 'Neither: it is an opinion, not a source', 'It cannot be classified without a date'])
    return {'stem': f'A student is given {s["prov"]}: “{s["text"]}” What type of source is this?', 'options': opts, 'answer': a,
            'key': f'{cap(s["kind"])}: judged by its origin and date of production, not by whether it is accurate. [1]'}


# --------------------------------------------------------------- 1.3 maps
FEATURES = ['church', 'post office', 'school', 'windmill', 'youth hostel', 'bridge', 'campsite', 'lighthouse', 'railway station', 'castle', 'farm', 'museum']
DIRS = [('north', 0, 1, '000'), ('north-east', 1, 1, '045'), ('east', 1, 0, '090'), ('south-east', 1, -1, '135'),
        ('south', 0, -1, '180'), ('south-west', -1, -1, '225'), ('west', -1, 0, '270'), ('north-west', -1, 1, '315')]

c1c = T('Using maps, grid references, scale and direction', 'maps grid references scale direction')
build(c1c, {
    'terms': [
        ('easting', 'a vertical grid line on a map, numbered from west to east and read first in a grid reference'),
        ('northing', 'a horizontal grid line on a map, numbered from south to north and read second in a grid reference'),
        ('contour line', 'a line on a map joining places of equal height above sea level'),
        ('scale', 'the ratio between a distance on a map and the real distance on the ground'),
        ('spot height', 'a dot on a map with a number showing the exact height of that point in metres'),
        ('key', 'the part of a map that explains what its symbols and colours mean'),
        ('relief', 'the shape and height of the land'),
        ('compass bearing', 'a direction measured clockwise from north in degrees, written with three figures'),
    ],
    'mcq': [
        ('In a six-figure grid reference, which part is given first?', 'The easting',
         ['The northing', 'The height of the land', 'The scale of the map'], '"Along the corridor, then up the stairs": eastings before northings. [1]'),
        ('Contour lines that are very close together show', 'a steep slope',
         ['flat land', 'a gentle slope', 'a river'], 'Close contours = height changes quickly over a short distance. [1]'),
        ('Which map scale shows the most detail of a small area?', '1:10 000',
         ['1:50 000', '1:250 000', '1:1 000 000'], 'The smaller the second number, the larger the scale and the more detail. [1]'),
        ('On a 1:50 000 map, what real distance does 1 cm represent?', '0.5 km',
         ['5 km', '50 m', '50 km'], '1 cm = 50 000 cm = 500 m = 0.5 km. [1]'),
        ('Which direction is exactly opposite south-west?', 'North-east', ['North-west', 'South-east', 'East'], 'Opposite directions differ by 180°: SW (225°) ↔ NE (045°). [1]'),
        ('A compass bearing of 090° points', 'east', ['north', 'south', 'west'], 'Bearings measured clockwise from north: 090° = east. [1]'),
        ('How many squares of a 1 km grid are needed to cover an area of 6 km²?', '6', ['3', '12', '36'], 'Each grid square on a 1 km grid = 1 km². [1]'),
    ],
    'explain': [
        ('Explain why a six-figure grid reference is more useful than a four-figure grid reference for finding a building.', 'A four-figure reference only gives the 1 km square; a six-figure reference divides the square into tenths and locates a point to within 100 m.', '1 mark: 4-fig = whole square; 1 mark: 6-fig = point within 100 m [2]'),
        ('Explain how you can tell from contour lines whether a slope is steep or gentle.', 'Close-together contours mean a large change in height over a short distance (steep); widely spaced contours mean a gentle slope.', '1 mark close = steep; 1 mark wide = gentle [2]'),
        ('Explain the difference between a large-scale and a small-scale map, with an example of a use for each.', 'Large-scale (e.g. 1:10 000) shows a small area in detail, useful for a town walk; small-scale (e.g. 1:1 000 000) shows a large area with little detail, useful for a country road map.', '1 mark each type with suitable use [2]'),
        ('Describe how to measure the length of a winding road on a map.', 'Lay a piece of string (or the edge of paper, marking each bend) along the road, then straighten it against the scale line to convert to real distance.', '1 mark method; 1 mark conversion using scale [2]'),
        ('Explain why satellite images and maps are often used together.', 'Satellite images show what the land actually looks like now (e.g. land use, flooding), while maps add names, symbols, heights and grid references for exact location.', '1 mark each [2]'),
    ],
    'claims': [
        ('In a grid reference you read the northing before the easting.', False, 'Eastings (along) are always given before northings (up).'),
        ('A 1:25 000 map shows more detail than a 1:50 000 map.', True, 'It is a larger scale: 1 cm represents 250 m instead of 500 m, so features are shown bigger and in more detail.'),
        ('If contour lines are far apart, the land must be very high.', False, 'Spacing shows steepness, not height; the numbers on the contours show height.'),
        ('A bearing of 270° means travelling west.', True, 'Bearings are measured clockwise from north, so 270° is west.'),
    ],
    'essays': [
        ('digital maps and satellite navigation have made paper maps and map skills unnecessary',
         ['Digital maps update quickly, can zoom and show live traffic or hazards.', 'Satellite navigation calculates routes automatically.'],
         ['Phones lose signal or battery in remote areas, so walkers and emergency teams still need paper maps.', 'Map skills (grid references, contours, scale) are needed to interpret any map, including digital ones.', 'GIS still uses the same ideas of scale, layers and location.'],
         'Digital tools have changed how maps are used, but map skills remain essential to understand and check them.',
         ['reliability of technology', 'remote areas', 'interpreting relief', 'GIS']),
    ],
})


@c1c.add('C3', (1, 2, 3, 4), 'numerical')
def c1c_grid(r, D):
    e, n = r.randint(10, 89), r.randint(10, 89)
    tx, ty = r.randint(1, 9), r.randint(1, 9)
    if tx == ty:
        ty = (ty % 9) + 1
    f = r.choice(FEATURES)
    four, six = f'{e:02d}{n:02d}', f'{e:02d}{tx}{n:02d}{ty}'
    stem = (f'On a 1:{r.choice(["25 000", "50 000"])} map, the {f} lies in the grid square whose bottom-left corner is where easting {e:02d} meets northing {n:02d}. '
            f'The symbol is {tx} tenths of the way across the square (eastwards) and {ty} tenths of the way up (northwards).')
    if D == 1:
        opts, a = mcq(r, six, [f'{n:02d}{ty}{e:02d}{tx}', f'{e:02d}{ty}{n:02d}{tx}', f'{e + 1:02d}{tx}{n + 1:02d}{ty}', f'{n:02d}{e:02d}'])
        return {'stem': stem + f' What is the six-figure grid reference of the {f}?', 'options': opts, 'answer': a, 'key': f'Easting {e:02d}+{tx} tenths, then northing {n:02d}+{ty} tenths = {six}. [1]'}
    if D == 2:
        return {'stem': stem + f' Give (a) the four-figure and (b) the six-figure grid reference of the {f}.', 'answer': f'(a) {four} (b) {six}',
                'key': f'(a) {four} [1] (b) {six}: easting first, then northing [1]', 'marks': 2}
    e2, n2 = e + r.choice([1, 2, 3]), n + r.choice([-2, -1, 1, 2])
    g = r.choice([x for x in FEATURES if x != f])
    dx, dy = e2 - e, n2 - n
    km = math.hypot(dx, dy)
    dirn = ('north-east' if dy > 0 else 'south-east')
    return {'stem': stem + f' A {g} is at the bottom-left corner of square {e2:02d}{n2:02d}. The grid squares are 1 km wide. (a) Give the six-figure reference of the {f}. (b) State the general direction of the {g} from the {f}. (c) Estimate the straight-line distance between them to the nearest 0.5 km.',
            'answer': f'(a) {six} (b) {dirn} (c) about {round(math.hypot(e2 - (e + tx / 10), n2 - (n + ty / 10)) * 2) / 2} km',
            'key': f'(a) {six} [1]; (b) {dirn}: further east and {"north" if dy > 0 else "south"} [1]; (c) Pythagoras on the grid or measured with ruler, ±0.5 km [1]', 'marks': 3}


@c1c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c1c_scale(r, D):
    sc = r.choice([10000, 25000, 50000, 100000])
    cm = r.choice([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7.5, 8, 9, 12])
    km = cm * sc / 100000
    scs = f'1:{sc:,}'.replace(',', ' ')
    a, b = r.sample(FEATURES, 2)
    if D == 1:
        opts, ans = mcq(r, f'{fmt(km, 2)} km', [f'{fmt(km * 10, 2)} km', f'{fmt(km / 10, 3)} km', f'{fmt(cm * sc / 1000, 1)} km', f'{fmt(km * 2, 2)} km'])
        return {'stem': f'On a {scs} map, the {a} and the {b} are {fmt(cm, 1)} cm apart. What is the real distance between them?', 'options': opts, 'answer': ans,
                'key': f'{fmt(cm, 1)} × {sc} = {fmt(cm * sc, 0)} cm = {fmt(km, 2)} km. [1]'}
    if D <= 3:
        return {'stem': f'On a {scs} map, a footpath from the {a} to the {b} measures {fmt(cm, 1)} cm. Calculate the real length of the footpath in kilometres. Show your working.',
                'answer': f'{fmt(km, 2)} km', 'key': f'{fmt(cm, 1)} cm × {sc} = {fmt(cm * sc, 0)} cm (1 mark); ÷ 100 000 = {fmt(km, 2)} km (1 mark) [2]', 'marks': 2}
    speed = r.choice([4, 5])
    mins = km / speed * 60
    return {'stem': f'A walking group plans a route on a {scs} map. The route from the {a} to the {b} measures {fmt(cm, 1)} cm. (a) Calculate the real distance in km. (b) The group walks at {speed} km/h. Calculate how long the walk will take in minutes. (c) Suggest why the walk may take longer than this.',
            'answer': f'(a) {fmt(km, 2)} km (b) {fmt(round(mins, 1), 1)} minutes (c) The route may be uphill (contours close together), winding, or over rough ground; stops for rest.',
            'key': f'(a) {fmt(cm, 1)} × {sc} ÷ 100 000 = {fmt(km, 2)} km [2]; (b) time = distance ÷ speed = {fmt(km, 2)} ÷ {speed} h = {fmt(round(mins, 1), 1)} min [2]; (c) relief/terrain or rests [1]', 'marks': 5}


@c1c.add('C3', (1, 2, 3), 'short')
def c1c_dir(r, D):
    a, b = r.sample(FEATURES, 2)
    name, dx, dy, brg = r.choice(DIRS)
    k = r.choice([1, 2, 3, 4])
    opp = DIRS[(DIRS.index((name, dx, dy, brg)) + 4) % 8]
    parts = []
    if dx:
        parts.append(f'{k} km {"east" if dx > 0 else "west"}')
    if dy:
        parts.append(f'{k} km {"north" if dy > 0 else "south"}')
    stem = f'From the {a}, the {b} is ' + ' and '.join(parts) + '.'
    if D == 1:
        opts, ans = mcq(r, cap(name), [cap(d[0]) for d in DIRS if d[0] != name])
        return {'stem': stem + f' In which direction is the {b} from the {a}?', 'options': opts, 'answer': ans, 'key': f'{cap(name)} (bearing {brg}°). [1]'}
    return {'stem': stem + f' (a) State the compass direction of the {b} from the {a}. (b) Give the three-figure bearing. (c) State the direction you would travel to return from the {b} to the {a}.',
            'answer': f'(a) {cap(name)} (b) {brg}° (c) {cap(opp[0])}', 'key': f'(a) {name} [1]; (b) {brg}° measured clockwise from north [1]; (c) {opp[0]}, the opposite direction ({opp[3]}°) [1]', 'marks': 3}


@c1c.add('C3', (2, 3, 4, 5), 'numerical')
def c1c_contour(r, D):
    ci = r.choice([5, 10, 20])
    h1 = r.choice([50, 100, 120, 150, 200, 240, 300])
    steps = r.choice([3, 4, 5, 6, 8, 10])
    h2 = h1 + ci * steps
    dist = r.choice([400, 500, 600, 800, 1000, 1200, 1500])
    if (dist % (h2 - h1)) and D < 4:
        dist = (h2 - h1) * r.choice([5, 8, 10, 12])
    grad = dist / (h2 - h1)
    stem = (f'On a map with a contour interval of {ci} m, point X lies on the {h1} m contour and point Y, on a hilltop, lies on the {h2} m contour. '
            f'The horizontal distance from X to Y is {dist} m.')
    parts = [
        lambda r: ('Calculate the difference in height between X and Y.', f'{h2 - h1} m', f'{h2} − {h1} = {h2 - h1} m [1]'),
        lambda r: ('State how many contour lines you would cross walking from X to Y (not counting the one at X).', f'{steps}', f'{h2 - h1} ÷ {ci} = {steps} [1]'),
        lambda r: ('Calculate the average gradient from X to Y, as a ratio 1 : n.', f'1 : {fmt(grad, 1)}', f'gradient = height difference ÷ horizontal distance = {h2 - h1} : {dist} = 1 : {fmt(grad, 1)} [2]'),
        lambda r: ('Describe what the spacing of the contour lines would show if the slope is steepest near the top.', 'The contours would be closest together near Y (the hilltop) and further apart near X.', '1 mark close near top; 1 mark wider lower down [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


# --------------------------------------------------------------- 1.4 data
CTX_DATA = [('pedestrians counted in 10 minutes at', 'sites'), ('daily rainfall in mm on', 'days'), ('cars passing the school gate per hour on', 'days'),
            ('litter items counted along 50 m transects at', 'sites'), ('visitors to a museum on', 'days')]

c1d = T('Presenting and interpreting data: graphs, tables and climate charts', 'presenting interpreting data graphs tables climate charts')
build(c1d, {
    'who': 'a geographer',
    'terms': [
        ('mean', 'the average found by adding all the values and dividing by the number of values'),
        ('median', 'the middle value when all the values are put in order'),
        ('mode', 'the value that occurs most often in a set of data'),
        ('range', 'the difference between the highest and lowest values'),
        ('anomaly', 'a result that does not fit the general pattern of the data (an outlier)'),
        ('positive correlation', 'a relationship in which one variable increases as the other increases'),
        ('negative correlation', 'a relationship in which one variable decreases as the other increases'),
        ('choropleth map', 'a map that uses shading of different intensity to show values for areas'),
        ('climate graph', 'a graph showing average monthly temperature as a line and average monthly precipitation as bars for one place'),
    ],
    'mcq': [
        ('Which type of graph is best for showing how the population of a city changed between 1950 and 2020?', 'Line graph',
         ['Pie chart', 'Scatter graph', 'Pictogram of land use'], 'Line graphs show continuous change over time. [1]'),
        ('Which type of graph is best for showing the proportions of different land uses in a town?', 'Pie chart',
         ['Line graph', 'Scatter graph', 'Climate graph'], 'Pie charts show parts of a whole. [1]'),
        ('Which graph is best for testing whether there is a relationship between GDP per person and life expectancy?', 'Scatter graph',
         ['Pie chart', 'Bar chart of one country', 'Climate graph'], 'Scatter graphs show correlation between two variables. [1]'),
        ('On a climate graph, how is precipitation usually shown?', 'As bars', ['As a line', 'As a pie chart', 'As shading on a map'], 'Temperature = line, precipitation = bars. [1]'),
        ('A pie chart has 360°. One category is 25% of the total. What angle should its sector be?', '90°', ['25°', '45°', '120°'], '25% × 360° = 90°. [1]'),
        ('Which statement about correlation is correct?', 'A correlation between two variables does not prove that one causes the other',
         ['A positive correlation always proves cause and effect', 'Negative correlation means there is no relationship', 'Correlation can only be shown on a pie chart'], 'Correlation ≠ causation; another factor may explain both. [1]'),
    ],
    'explain': [
        ('Explain why the median is sometimes a better average than the mean.', 'The median is not affected by one or two extreme values (anomalies), so it can better represent a typical value in uneven data.', '1 mark: median = middle value; 1 mark: not distorted by extremes [2]'),
        ('Explain why a scatter graph showing a correlation does not prove that one variable causes the other.', 'Both may be linked to a third factor, or the relationship may be coincidence; correlation only shows that they change together.', '1 mark third factor/coincidence; 1 mark correlation ≠ causation [2]'),
        ('Explain why climate graphs use averages taken over about 30 years.', 'Weather varies from year to year; averaging over a long period removes unusual years and shows the typical climate.', '1 mark weather varies; 1 mark long-term average shows typical pattern [2]'),
        ('Explain one advantage and one disadvantage of using a choropleth map.', 'Advantage: shows patterns across areas clearly at a glance. Disadvantage: assumes the value is the same across each whole area and hides variation within areas; boundaries are sharp.', '1 mark each [2]'),
        ('Explain why it is helpful to describe a pattern in data using figures from the graph.', 'Quoting values (e.g. highest, lowest, change) gives precise evidence and supports the description, making it more convincing and checkable.', '1 mark precision/evidence; 1 mark supports conclusion [2]'),
    ],
    'claims': [
        ('The range tells you the average value of a data set.', False, 'The range is the difference between the highest and lowest values; it shows spread, not average.'),
        ('A line graph is suitable for showing data that changes continuously over time.', True, 'The line joins points in sequence to show trends over time.'),
        ('If two variables show a strong positive correlation, one must cause the other.', False, 'Correlation does not prove causation; another factor may cause both.'),
        ('On a climate graph for a southern hemisphere city, the hottest months are usually December to February.', True, 'Summer in the southern hemisphere is from December to February.'),
    ],
    'essays': [
        ('a climate graph tells us everything we need to know about the climate of a place',
         ['It shows monthly temperature and precipitation, the annual range and the wet and dry seasons.'],
         ['It shows averages, hiding extremes such as heatwaves, storms and droughts.', 'It does not show wind, humidity, sunshine hours or daily (diurnal) range.', 'It may not show recent climate change or variation within the area.'],
         'It is a very useful summary but needs other data to give a full picture.',
         ['averages and extremes', 'other elements of weather', 'change over time']),
        ('choosing the right type of graph is the most important part of presenting data',
         ['The right graph makes patterns clear; the wrong one can hide or distort them.'],
         ['Accurate data collection matters more: a good graph of poor data is still misleading.', 'Clear labelling, scales and a key are equally important.', 'Interpretation with figures turns a graph into evidence.'],
         'Graph choice matters a great deal, but accuracy, labelling and interpretation are just as important.',
         ['data accuracy', 'labelling and scales', 'interpretation']),
    ],
})


@c1d.add('C3', (1, 2, 3, 4), 'numerical')
def c1d_stats(r, D):
    what, unit = r.choice(CTX_DATA)
    n = r.choice([5, 7, 9])
    vals = [r.randint(3, 60) for _ in range(n)]
    if len(set(vals)) < n:
        return None
    s = sorted(vals)
    mean = round(sum(vals) / n, 1)
    med = s[n // 2]
    rng = s[-1] - s[0]
    labels = [f'{u}' for u in ('ABCDEFGHI'[:n])] if unit == 'sites' else ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon (wk 2)', 'Tue (wk 2)'][:n]
    data = ', '.join(f'{l} {v}' for l, v in zip(labels, vals))
    stem = f'A student recorded the number of {what} {n} {unit}: {data}.'
    if D == 1:
        opts, a = mcq(r, str(rng), [str(s[-1]), str(med), str(s[-1] + s[0]), str(rng + 1), str(rng - 1)])
        return {'stem': stem + ' What is the range of the data?', 'options': opts, 'answer': a, 'key': f'{s[-1]} − {s[0]} = {rng}. [1]'}
    parts = [
        lambda r: ('Calculate the mean to one decimal place.', fmt(mean, 1), f'sum {sum(vals)} ÷ {n} = {fmt(mean, 1)} [2]'),
        lambda r: ('Find the median.', str(med), f'ordered: {", ".join(map(str, s))}; middle value = {med} [1]'),
        lambda r: ('Calculate the range.', str(rng), f'{s[-1]} − {s[0]} = {rng} [1]'),
        lambda r: (f'Identify the {unit[:-1]} with the highest value and suggest one reason why it might be an anomaly.', f'{labels[vals.index(s[-1])]} ({s[-1]}); it may be due to a one-off event (e.g. an event, market day or weather) or a recording error.', '1 mark identification; 1 mark plausible reason [2]'),
        lambda r: ('Suggest a suitable graph to present this data and give a reason.', 'A bar chart, because the data is for separate (discrete) categories, so values can be compared easily.', '1 mark graph; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c1d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c1d_climate(r, D):
    zone, temps, prec, hemi, lat = climate(r)
    hi, lo, rng, tot, wet, mean = climate_stats(temps, prec)
    place = r.choice(['Station P', 'Station Q', 'Weather station R', 'Town S', 'Site T'])
    stem = f'The table shows climate data for {place}. ' + climate_text(temps, prec)
    if D == 1:
        opts, a = mcq(r, wet, [m for m in MONTHS if m != wet][:: r.choice([2, 3])][:6] + ['July', 'January'])
        return {'stem': stem + ' Which is the wettest month?', 'options': opts, 'answer': a, 'key': f'{wet}: {max(prec)} mm. [1]'}
    parts = [
        lambda r: ('Calculate the annual temperature range.', f'{fmt(rng, 1)} °C', f'{fmt(hi, 1)} − ({fmt(lo, 1)}) = {fmt(rng, 1)} °C [2]'),
        lambda r: ('Calculate the total annual precipitation.', f'{tot} mm', f'sum of the 12 months = {tot} mm [2]'),
        lambda r: ('Identify the wettest month and give its rainfall.', f'{wet}, {max(prec)} mm', '[1]'),
        lambda r: ('Calculate the mean annual temperature to one decimal place.', f'{fmt(mean, 1)} °C', f'sum ÷ 12 = {fmt(mean, 1)} °C [2]'),
        lambda r: ('Describe the pattern of precipitation through the year, using figures.', f'Wettest in {wet} ({max(prec)} mm), driest in {MONTHS[prec.index(min(prec))]} ({min(prec)} mm); total {tot} mm.', '1 mark pattern/season; 1 mark figures quoted [2]'),
        lambda r: ('Describe how this data would be drawn on a climate graph.', 'Temperature as a line graph (left axis, °C) and precipitation as bars (right axis, mm), with months along the bottom.', '1 mark line for temperature; 1 mark bars for precipitation [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c1d.add('C3', (2, 3, 4), 'numerical')
def c1d_pie(r, D):
    N = r.choice([60, 72, 90, 120, 180])
    per = 360 // N
    cats = r.choice([['walk', 'bus', 'car', 'bicycle'], ['shopping', 'work', 'visiting family', 'leisure'], ['very safe', 'safe', 'unsafe', 'very unsafe']])
    a = r.randint(N // 6, N // 3)
    b = r.randint(N // 6, N // 3)
    c = r.randint(N // 10, N // 5)
    d = N - a - b - c
    if d <= 0:
        return None
    cnt = [a, b, c, d]
    q = r.choice(['how they travel to the town centre', 'the main reason for their visit', 'how safe they feel in the park'])
    stem = f'In a survey, {N} people were asked about {q}. Results: ' + ', '.join(f'{x} {y}' for x, y in zip(cats, cnt)) + '.'
    i = r.randrange(4)
    parts = [
        lambda r: (f'Calculate the angle of the sector for “{cats[i]}” on a pie chart.', f'{cnt[i] * per}°', f'{cnt[i]}/{N} × 360° = {cnt[i] * per}° [2]'),
        lambda r: (f'Calculate the percentage of people who answered “{cats[0]}”, to one decimal place.', f'{fmt(round(100 * a / N, 1), 1)}%', f'{a}/{N} × 100 = {fmt(round(100 * a / N, 1), 1)}% [2]'),
        lambda r: ('Give one reason why a pie chart is suitable for this data.', 'The categories are parts of one whole (all people surveyed), so a pie chart shows the proportions clearly.', '[1]'),
        lambda r: ('Suggest one other way to present the data and explain an advantage.', 'A bar chart: makes it easier to compare the exact size of each category.', '1 mark method; 1 mark advantage [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


# --------------------------------------------------------------- 1.5 conclusions
c1e = T('Reaching a supported conclusion and reflecting on the enquiry', 'supported conclusion reflecting enquiry')
build(c1e, {
    'who': 'an investigator',
    'terms': [
        ('conclusion', 'a summary of what the evidence shows, answering the enquiry question'),
        ('evaluation', 'a judgement on the strengths and weaknesses of the methods, data and conclusions'),
        ('limitation', 'a weakness in the data or methods that reduces confidence in the results'),
        ('evidence', 'information or data used to support a claim or conclusion'),
        ('judgement', 'a reasoned decision reached after weighing up evidence on different sides'),
        ('counter-argument', 'a point that challenges or goes against the main argument'),
        ('reliability', 'how far results would be the same if the investigation were repeated'),
    ],
    'mcq': [
        ('What should a good conclusion always do?', 'Answer the enquiry question using evidence from the results',
         ['Repeat the method', 'Introduce new data not collected', 'Avoid mentioning the hypothesis'], 'A conclusion links back to the question/hypothesis with evidence. [1]'),
        ('Which of these is an evaluation point rather than a conclusion?', 'The sample of 20 people was too small to be representative',
         ['Traffic was heaviest at 8 a.m.', 'Most shoppers travelled less than 5 km', 'The hypothesis was supported'], 'Evaluation comments on the quality of methods/data. [1]'),
        ('Which phrase best shows a supported judgement?', '“The evidence mostly supports the hypothesis because 72% of people…”',
         ['“I think this is true.”', '“Everyone knows this.”', '“This is obviously the answer.”'], 'A judgement is supported with evidence (figures). [1]'),
    ],
    'explain': [
        ('Explain why it is important to identify limitations in an investigation.', 'It shows how far the conclusion can be trusted and helps suggest improvements for future investigations.', '1 mark trust in conclusion; 1 mark improvements [2]'),
        ('Explain how an investigator could make a conclusion more reliable.', 'Collect more data, repeat at different times and places, and cross-check with secondary sources, so that one-off results do not distort the conclusion.', '1 mark method; 1 mark why it increases reliability [2]'),
        ('Explain why a conclusion should consider evidence that does not support the hypothesis.', 'Ignoring evidence makes the conclusion biased; weighing evidence on both sides gives a more balanced and convincing judgement.', '1 mark avoids bias; 1 mark balanced judgement [2]'),
        ('Explain the difference between a conclusion and an evaluation.', 'A conclusion states what the evidence shows in answer to the question; an evaluation judges how good the methods and evidence were and how far the conclusion can be trusted.', '1 mark each [2]'),
    ],
    'claims': [
        ('If the results do not support the hypothesis, the investigation has failed.', False, 'Rejecting a hypothesis is a valid finding; the conclusion explains why the evidence went the other way.'),
        ('A conclusion should include figures from the results.', True, 'Data gives evidence for the judgement and makes it precise.'),
        ('Reflecting on an enquiry means writing about how much you enjoyed it.', False, 'Reflection evaluates methods, data and conclusions and suggests improvements.'),
    ],
    'essays': [
        ('the most important part of an enquiry is collecting a large amount of data',
         ['More data makes results more representative and reliable.'],
         ['Data must be accurate and relevant to the question; lots of poor data is still poor.', 'A good question and careful analysis are needed to reach a valid conclusion.', 'Evaluation shows how far conclusions can be trusted.'],
         'Quantity helps, but the quality of the question, method, analysis and evaluation matters as much.',
         ['quality versus quantity', 'the enquiry question', 'analysis and evaluation']),
        ('an investigation that disproves its hypothesis has failed',
         ['The investigator did not find the expected pattern.'],
         ['A rejected hypothesis is still new knowledge.', 'The conclusion can explain why the result was different.', 'Science and humanities enquiries both progress by testing and rejecting ideas.'],
         'Disagree: an investigation succeeds if it answers the question with reliable evidence, whatever the result.',
         ['testing ideas', 'reliability', 'what counts as success']),
    ],
})


@c1e.add('C3', (2, 3, 4, 5), 'case')
def c1e_results(r, D):
    sites = ['A', 'B', 'C', 'D']
    hyp_kind = r.choice(['traffic', 'survey'])
    if hyp_kind == 'traffic':
        near = r.randint(150, 320)
        far = near + r.choice([-90, -60, -30, 20, 40, 70])
        stem = (f'A student tested the hypothesis “Traffic is heavier near the town centre than on the edge of town.” Counts of vehicles in one hour: near the centre {near}, '
                f'on the edge of town {far}. Data was collected once, on a weekday morning.')
        sup_ = near > far
        diff = abs(near - far)
        pc = round(100 * diff / min(near, far), 1)
        verdict = f'{"Supported" if sup_ else "Not supported"}: the centre had {near} vehicles and the edge {far}, a difference of {diff} ({fmt(pc, 1)}% of the lower value).'
    else:
        n = r.choice([40, 50, 60, 80])
        yes = r.randint(int(n * 0.3), int(n * 0.8))
        pc = round(100 * yes / n, 1)
        stem = (f'A student tested the hypothesis “Most residents think the new park has improved the area.” In a survey of {n} residents, {yes} said yes. '
                f'All the interviews were done at the park entrance on a Sunday.')
        sup_ = yes > n / 2
        verdict = f'{"Supported" if sup_ else "Not supported"}: {yes} of {n} = {fmt(pc, 1)}% said yes, which is {"more" if sup_ else "not more"} than half.'
    parts = [
        lambda r: ('Does the evidence support the hypothesis? Use figures in your answer.', verdict, '1 mark judgement; 1 mark figures [2]'),
        lambda r: ('Identify one limitation of the data and explain how it affects the conclusion.', 'Data collected only once/at one place and time (e.g. one weekday morning or at the park entrance on a Sunday), so it may not be representative and the conclusion is tentative.', '1 mark limitation; 1 mark effect [2]'),
        lambda r: ('Suggest two improvements to make the conclusion more reliable.', 'Repeat on different days and times; increase the sample/sites; use systematic sampling; compare with secondary data.', '1 mark each [2]'),
        lambda r: ('Write a supported conclusion of two sentences for this enquiry.', verdict + ' However, because of the small, one-off sample the conclusion should be treated with caution.', '1 mark answer to hypothesis with evidence; 1 mark reflection/qualification [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


CHAPTERS[1] = [c1a, c1b, c1c, c1d, c1e]


# ============================================================== CHAPTER 2: Industrial Revolution

c2a = T('Causes of the Industrial Revolution in Britain: population, agriculture, coal and capital', 'causes industrial revolution population agriculture coal capital')
build(c2a, {
    'terms': [
        ('Industrial Revolution', 'the change from making goods by hand at home to making them by machine in factories, which began in Britain in the 18th century'),
        ('enclosure', 'the fencing off of open fields and common land into separate, privately owned farms'),
        ('crop rotation', 'growing different crops on a field in a set order each year to keep the soil fertile'),
        ('selective breeding', 'choosing the best animals to breed from so that offspring have the most useful features'),
        ('capital', 'money and wealth available to invest in new businesses, machines and buildings'),
        ('entrepreneur', 'a person who takes risks by investing money to set up or expand a business'),
        ('domestic system', 'a way of producing goods, especially cloth, by hand in workers’ own homes'),
        ('raw materials', 'natural resources, such as cotton, coal or iron ore, used to make goods'),
    ],
    'dates': [
        ('Jethro Tull developed his horse-drawn seed drill', 1701),
        ('Abraham Darby first smelted iron using coke at Coalbrookdale', 1709),
        ('Thomas Newcomen built his first steam engine to pump water out of mines', 1712),
        ('the Bridgewater Canal opened, carrying coal from Worsley to Manchester', 1761),
        ('the first national census was taken in Britain', 1801),
        ('the Bank of England was founded', 1694),
    ],
    'mcq': [
        ('Which change in farming helped to provide workers for the new factories?', 'Enclosure, which forced many small farmers and labourers off the land',
         ['The abolition of all farms', 'The end of crop rotation', 'A fall in food production'], 'Enclosure and more efficient farming meant fewer labourers were needed, so many moved to towns. [1]'),
        ('Why was coal so important to the Industrial Revolution in Britain?', 'It fuelled steam engines and was needed to smelt iron',
         ['It was used to make cotton cloth', 'It was imported cheaply from India', 'It was needed to build canals'], 'Coal powered engines and (as coke) smelted iron; Britain had large coalfields. [1]'),
        ('Roughly how much did the population of England and Wales grow between 1801 and 1851?', 'It doubled, from about 9 million to about 18 million',
         ['It halved', 'It stayed about the same', 'It grew from 1 million to 2 million'], 'Census: about 8.9 million (1801) and 17.9 million (1851). [1]'),
        ('Where did much of the capital to build early factories come from?', 'Profits from trade, banking and farming, including the Atlantic trade',
         ['Loans from the United Nations', 'Taxes paid by factory workers', 'Gold mined in Britain'], 'Merchants, landowners and banks invested profits from trade (including slave-produced goods) and agriculture. [1]'),
        ('Which crop rotation system was associated with Norfolk and Viscount “Turnip” Townshend?', 'A four-field rotation of wheat, turnips, barley and clover',
         ['Leaving half of every field empty each year', 'Growing only wheat every year', 'A rotation of rice and cotton'], 'Turnips and clover restored the soil and fed animals in winter. [1]'),
        ('Why did a rising population help British industry to grow?', 'It provided both more workers and more customers for goods',
         ['It reduced the demand for food', 'It meant fewer people needed jobs', 'It made machines unnecessary'], 'Labour supply + demand for goods. [1]'),
    ],
    'explain': [
        ('Explain how changes in agriculture helped the Industrial Revolution.', 'New methods (crop rotation, seed drill, selective breeding) and enclosure produced more food to feed growing towns, and fewer farm workers were needed, so labour moved to factories; farmers’ profits could also be invested.', '1 mark food supply; 1 mark labour released; 1 mark capital [3]'),
        ('Explain why Britain’s supplies of coal and iron helped it to industrialise first.', 'Britain had large coalfields close to iron ore, so fuel for steam engines and for smelting iron was cheap and plentiful; machines, rails and engines could be made at home.', '1 mark coal for power/smelting; 1 mark location/cheapness; 1 mark use of iron [3]'),
        ('Explain how trade and the empire helped to provide capital for industry.', 'Merchants made large profits from overseas trade (sugar, tobacco, cotton, enslaved people) and banks lent money, so there was capital to invest in factories, canals and machines. Colonies also supplied raw cotton and markets.', '1 mark profits/capital; 1 mark banks/investment; 1 mark raw materials/markets [3]'),
        ('Explain why canals were important in the early Industrial Revolution.', 'They carried heavy, bulky goods such as coal cheaply and smoothly; the Bridgewater Canal (1761) roughly halved the price of coal in Manchester.', '1 mark cheap bulk transport; 1 mark example/effect [2]'),
        ('Explain how population growth and industrial growth affected each other.', 'More people meant more workers and customers, encouraging factories to expand; industrial growth created jobs and wages that supported larger families and towns.', '1 mark each direction of the link [2]'),
    ],
    'claims': [
        ('The Industrial Revolution happened suddenly in the year 1800.', False, 'It was a gradual process from about 1750 to 1850, building on earlier changes in farming, trade and technology.'),
        ('Britain had to import most of the coal used in its factories.', False, 'Britain had large coalfields of its own, in places such as South Wales, the North East and the Midlands.'),
        ('Enclosure increased farm output but forced many poor families off the land.', True, 'Larger enclosed farms were more efficient, but labourers lost common grazing rights and many moved to towns.'),
        ('Population growth in Britain after 1750 was caused only by a falling death rate.', False, 'Historians link it to both a falling death rate and a rising birth rate, as people married younger.'),
    ],
    'sources': [
        dict(prov='a report on farming written by the agricultural writer Arthur Young in 1771 (adapted)', kind='primary',
             text='Where the open fields have been enclosed, the land produces twice as much corn. The farmers are richer and the rents higher, though the cottager has lost his cow and his common.',
             about='the effects of enclosure', infer='Enclosure increased output and profits for farmers and landowners but harmed poorer cottagers who lost common rights.',
             purpose='To inform and persuade landowners about the benefits of improved farming and enclosure.',
             plus='Young toured many farms and wrote at the time, so he saw the changes himself', minus='he was a strong supporter of agricultural improvement, so he may exaggerate the benefits',
             missing='How many labourers moved to the industrial towns, or the scale of enclosure nationally.', enq='why farming changed in the 18th century'),
        dict(prov='a modern historian writing in 2010 about why Britain industrialised first', kind='secondary',
             text='No single factor explains Britain’s lead. Cheap coal, high wages that encouraged machines, an expanding empire and a stable government all combined in the decades after 1750.',
             about='the causes of the Industrial Revolution', infer='The Industrial Revolution had several linked causes rather than one main cause.',
             purpose='To explain and interpret the causes, based on research, for readers of history.',
             plus='the historian has hindsight and can compare evidence from many sources', minus='it is one interpretation; other historians stress different factors such as population or capital',
             missing='Detailed evidence such as population figures or the role of particular inventors.', enq='why Britain was the first country to industrialise'),
    ],
    'essays': [
        ('the supply of coal was the most important reason why Britain was the first country to industrialise',
         ['Coal fuelled steam engines and, as coke, smelted iron (Darby, 1709).', 'Britain’s coalfields were large and close to iron ore and ports.'],
         ['Agricultural change fed the towns and released labour.', 'Capital from trade and banking paid for factories and canals.', 'Population growth supplied workers and customers; the empire supplied cotton and markets.'],
         'Coal was essential, but it mattered because it combined with capital, labour and markets; together they explain Britain’s lead.',
         ['population growth', 'agriculture', 'capital and trade', 'transport']),
        ('population growth was the main cause of the Industrial Revolution',
         ['England and Wales grew from about 9 million (1801) to 18 million (1851), providing workers and demand.'],
         ['Population growth alone does not explain mechanisation; other countries also grew.', 'Coal, inventions, capital and transport were needed to turn demand into factory production.'],
         'Population growth was an important condition but not the main cause on its own.',
         ['labour supply', 'demand for goods', 'coal and iron', 'capital']),
    ],
})


@c2a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c2a_towns(r, D):
    towns = [('Manchester', 75000, 303000), ('Liverpool', 78000, 376000), ('Birmingham', 74000, 233000), ('Leeds', 53000, 172000), ('Glasgow', 77000, 329000)]
    a, b = r.sample(towns, 2)
    pa = round(100 * (a[2] - a[1]) / a[1])
    pb = round(100 * (b[2] - b[1]) / b[1])
    stem = (f'The table shows the approximate populations of two industrial towns. {a[0]}: 1801 about {a[1]:,}, 1851 about {a[2]:,}. '
            f'{b[0]}: 1801 about {b[1]:,}, 1851 about {b[2]:,}.').replace(',', ' ')
    if D == 1:
        big = a if a[2] - a[1] > b[2] - b[1] else b
        opts, ans = mcq(r, big[0], [a[0] if big is b else b[0], 'Both grew by the same amount', 'Neither town grew'])
        return {'stem': stem + ' Which town grew by more people between 1801 and 1851?', 'options': opts, 'answer': ans, 'key': f'{big[0]} grew by {big[2] - big[1]:,} people. [1]'.replace(',', ' ')}
    parts = [
        lambda r: (f'Calculate the increase in the population of {a[0]} between 1801 and 1851.', f'{a[2] - a[1]:,}'.replace(',', ' '), f'{a[2]} − {a[1]} [1]'),
        lambda r: (f'Calculate the percentage increase in the population of {b[0]}, to the nearest whole number.', f'{pb}%', f'({b[2]} − {b[1]}) ÷ {b[1]} × 100 = {pb}% [2]'),
        lambda r: ('Which town grew faster in percentage terms?', f'{a[0] if pa > pb else b[0]} ({max(pa, pb)}% compared with {min(pa, pb)}%)', f'{a[0]} {pa}%, {b[0]} {pb}% [1]'),
        lambda r: ('Explain two reasons why industrial towns grew so quickly in this period.', 'Migration from the countryside for factory jobs (after enclosure and farm mechanisation); natural increase as birth rates stayed high; railways and canals brought trade and work.', '1 mark each explained reason [4]'),
        lambda r: ('Suggest one problem that such rapid growth caused for the towns.', 'Overcrowded, poorly built housing without clean water or sewers, leading to diseases such as cholera and typhus.', '1 mark problem; 1 mark development [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c2b = T('New technology and the factory system: textiles, steam power and railways', 'technology factory system textiles steam power railways')
build(c2b, {
    'terms': [
        ('factory system', 'a way of producing goods in which workers use power-driven machines in one large building, working fixed hours under supervision'),
        ('mechanisation', 'the replacement of work done by hand with work done by machines'),
        ('spinning jenny', 'a hand-powered machine invented by James Hargreaves that spun several threads at once'),
        ('water frame', 'Richard Arkwright’s spinning machine powered by a water wheel, which produced strong thread'),
        ('power loom', 'a machine for weaving cloth driven by water or steam power, invented by Edmund Cartwright'),
        ('steam engine', 'a machine that uses the pressure of steam from boiling water to produce movement'),
        ('division of labour', 'splitting a production process into separate simple tasks, each done by a different worker'),
        ('locomotive', 'an engine that moves along a railway track pulling carriages or wagons'),
    ],
    'dates': [
        ('John Kay invented the flying shuttle', 1733),
        ('James Hargreaves invented the spinning jenny', 1764),
        ('Richard Arkwright patented the water frame', 1769),
        ('Arkwright opened his water-powered mill at Cromford in Derbyshire', 1771),
        ('Samuel Crompton invented the spinning mule', 1779),
        ('Edmund Cartwright invented the power loom', 1785),
        ('the Stockton and Darlington Railway opened', 1825),
        ('Stephenson’s Rocket won the Rainhill Trials', 1829),
        ('the Liverpool and Manchester Railway opened', 1830),
    ],
    'mcq': [
        ('What was the main improvement James Watt made to the steam engine?', 'He added a separate condenser, which made it far more efficient',
         ['He invented the first steam engine ever built', 'He made it run on petrol', 'He used it only for pumping water'], 'Watt’s separate condenser (patented 1769) saved fuel; later rotary motion let it drive machines. [1]'),
        ('Why were early factories, such as Cromford Mill, built beside fast-flowing rivers?', 'Water wheels provided power for the machines',
         ['Rivers supplied the raw cotton', 'Workers needed to wash after work', 'Steam engines needed to float'], 'Before steam power, water power drove the water frame. [1]'),
        ('Why was the Liverpool and Manchester Railway (1830) important?', 'It was the first inter-city railway to use only steam locomotives and carry passengers to a timetable',
         ['It was the first canal in Britain', 'It connected London and Scotland', 'It used horses instead of engines'], 'It linked the port of Liverpool with the cotton mills of Manchester. [1]'),
        ('How did steam power change where factories could be built?', 'Factories could be built in towns and near coalfields instead of only beside rivers',
         ['Factories had to move to mountain areas', 'Factories could only be built at ports', 'It made no difference'], 'Steam engines freed factories from water power. [1]'),
        ('Approximately how many miles of railway did Britain have by 1850?', 'About 6000 miles', ['About 60 miles', 'About 600 miles', 'About 60 000 miles'], 'Rapid “railway mania” of the 1840s: about 6000 miles by 1850. [1]'),
    ],
    'explain': [
        ('Explain how the factory system was different from the domestic system.', 'Domestic system: families worked by hand at home, set their own hours. Factory system: workers went to a large building with power-driven machines, worked long fixed hours under supervision and were paid wages.', '1 mark place/power; 1 mark hours/discipline; 1 mark contrast [3]'),
        ('Explain why inventions in spinning led to inventions in weaving.', 'Faster spinning machines (jenny, water frame, mule) produced more thread than hand-loom weavers could use, creating demand for a faster weaving machine – the power loom.', '1 mark imbalance; 1 mark leads to power loom [2]'),
        ('Explain two effects of the railways on British society.', 'Goods such as coal and food moved faster and cheaper; people could travel for work or leisure (day trips to the seaside); standard “railway time” was adopted; new jobs and towns grew (e.g. Crewe, Swindon).', '2 marks each explained effect [4]'),
        ('Explain why steam power was so important to the factory system.', 'Steam engines gave reliable power that did not depend on rivers or weather, so factories could be bigger, run more machines and be built in towns near coal and workers.', '1 mark reliable power; 1 mark location/size [2]'),
        ('Explain why some hand-loom weavers opposed new machines.', 'Power looms produced cloth faster and cheaper, so hand-loom weavers’ wages collapsed and many lost their livelihoods; some, like the Luddites (1811-16), smashed machines.', '1 mark loss of wages/jobs; 1 mark example of protest [2]'),
    ],
    'claims': [
        ('James Watt invented the first steam engine.', False, 'Thomas Newcomen built a working steam engine in 1712; Watt greatly improved it from 1769 with a separate condenser.'),
        ('The first factories were powered by water rather than steam.', True, 'Early mills such as Arkwright’s Cromford Mill (1771) used water wheels.'),
        ('Railways only helped to move goods, not people.', False, 'Railways carried millions of passengers, allowing commuting, day trips and cheap post and newspapers.'),
        ('The power loom made hand-loom weavers richer.', False, 'Hand-loom weavers could not compete with cheap machine-made cloth and their wages fell sharply.'),
    ],
    'sources': [
        dict(prov='a description of a cotton mill by a visitor to Manchester, 1835 (adapted)', kind='primary',
             text='Hundreds of spinning machines turn in a single room, driven by one great steam engine below. The noise is so great that the workers speak by signs, and the overlookers walk the rows to see that no machine stands idle.',
             about='the factory system', infer='Factories were large, noisy and steam-powered, with many workers supervised closely to keep machines running.',
             purpose='To describe and possibly marvel at the new industry for readers who had never seen a mill.',
             plus='the visitor saw the mill in person in 1835', minus='a visitor saw only one mill on one day and may have been shown the best parts',
             missing='Workers’ wages, hours or accidents, or how the mill compared with the domestic system.', enq='how the factory system changed work'),
        dict(prov='a newspaper report on the opening of the Liverpool and Manchester Railway, September 1830 (adapted)', kind='primary',
             text='The engines drew carriages filled with passengers at a speed of more than twenty miles an hour. The whole route was lined with crowds who had come to see this wonder of the age.',
             about='attitudes to the early railways', infer='The railway was seen as an exciting new wonder and attracted huge public interest.',
             purpose='To report a major public event and interest readers.',
             plus='it was written at the time of the event by a reporter who was there', minus='the reporter may have exaggerated the excitement to make a good story; it does not mention the accident that killed the MP William Huskisson on the opening day',
             missing='The impact of railways on trade, jobs or canal companies in later years.', enq='the impact of railways in the 1830s and 1840s'),
    ],
    'essays': [
        ('the steam engine was the most important invention of the Industrial Revolution',
         ['Watt’s engine powered factories, mines, locomotives and ships.', 'It freed factories from rivers and allowed large-scale production in towns.'],
         ['Textile inventions (jenny, water frame, mule, power loom) started factory production before steam was widespread.', 'Railways transformed transport and markets.', 'Coke smelting of iron made machines and rails possible.'],
         'The steam engine was the most important because it linked and powered the other changes, though it depended on earlier textile and iron inventions.',
         ['textile machines', 'railways', 'iron', 'power for factories']),
        ('railways changed British society more than factories did',
         ['Railways changed how and where people lived and travelled: commuting, seaside holidays, national newspapers and standard time.'],
         ['Factories changed the daily lives of millions of workers, including children, and created industrial towns.', 'Factories came first and created the demand for railways.'],
         'Both mattered; factories changed work more, while railways changed travel, trade and leisure.',
         ['work and hours', 'travel and leisure', 'growth of towns']),
    ],
})


@c2b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c2b_rail(r, D):
    yrs = [(1830, 100), (1840, 1500), (1850, 6000), (1860, 10400), (1870, 13600)]
    i = r.randrange(len(yrs) - 1)
    y1, m1 = yrs[i]
    y2, m2 = yrs[i + 1]
    stem = 'The table shows the approximate length of railway in Britain: ' + ', '.join(f'{y} – {m:,} miles'.replace(',', ' ') for y, m in yrs) + '.'
    if D == 1:
        best = max(range(len(yrs) - 1), key=lambda k: yrs[k + 1][1] - yrs[k][1])
        lab = f'{yrs[best][0]}-{yrs[best + 1][0]}'
        opts, ans = mcq(r, lab, [f'{yrs[k][0]}-{yrs[k + 1][0]}' for k in range(len(yrs) - 1) if k != best])
        return {'stem': stem + ' In which decade did the railway network grow by the most miles?', 'options': opts, 'answer': ans, 'key': f'{lab}: +{yrs[best + 1][1] - yrs[best][1]} miles (the "railway mania" of the 1840s). [1]'}
    d = r.choice([200, 300, 320])
    coach, train = r.choice([8, 10, 12]), r.choice([30, 40])
    parts = [
        lambda r: (f'Calculate the increase in miles of railway between {y1} and {y2}.', f'{m2 - m1:,} miles'.replace(',', ' '), f'{m2} − {m1} [1]'),
        lambda r: ('Describe the trend shown by the data, using figures.', 'Rapid growth throughout, fastest in the 1840s (1500 to 6000 miles), then continued but slower growth to 13 600 miles by 1870.', '1 mark trend; 1 mark figures [2]'),
        lambda r: (f'A journey of {d} km took a stagecoach averaging {coach} km/h and a train averaging {train} km/h. Calculate how many hours were saved by train.', f'{fmt(d / coach - d / train, 1)} hours', f'{d}/{coach} = {fmt(d / coach, 1)} h; {d}/{train} = {fmt(d / train, 1)} h; saving {fmt(d / coach - d / train, 1)} h [2]'),
        lambda r: ('Explain two ways the growth of railways helped industry.', 'Cheap, fast transport of coal, raw materials and finished goods; wider markets; huge demand for iron, coal and engineering; fresh food to towns.', '2 marks each [4]'),
        lambda r: ('Suggest one group of people who might have opposed the railways, and why.', 'Canal and stagecoach owners (lost business) or landowners (lines crossed their estates).', '1 mark group; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c2c = T('Living and working conditions in industrial towns', 'living working conditions industrial towns')
build(c2c, {
    'terms': [
        ('back-to-back houses', 'cheap terraced houses built sharing a back wall, with no back yard and little ventilation'),
        ('cholera', 'a water-borne disease spread by sewage-contaminated water, which killed tens of thousands in British epidemics in 1831-32 and 1848-49'),
        ('overlooker', 'a supervisor in a mill who kept workers, including children, at work, sometimes by beating them'),
        ('scavenger', 'a child mill worker who crawled under moving machines to collect loose cotton'),
        ('trapper', 'a young child in a coal mine who opened and closed ventilation doors for coal wagons'),
        ('cellar dwelling', 'a damp, dark underground room rented out as a home to the poorest families'),
        ('privy', 'an outdoor toilet, often shared by many households and emptied rarely'),
        ('typhus', 'a disease spread by lice that thrived in crowded, dirty housing'),
    ],
    'dates': [
        ('the first cholera epidemic struck Britain', 1831),
        ('the Sadler Committee heard evidence from child factory workers', 1832),
        ('Edwin Chadwick published his Report on the Sanitary Condition of the Labouring Population', 1842),
        ('Friedrich Engels published The Condition of the Working Class in England', 1845),
        ('Dr John Snow linked cholera to the Broad Street water pump in London', 1854),
        ('the “Great Stink” hit London as the River Thames overflowed with sewage', 1858),
    ],
    'mcq': [
        ('According to Chadwick’s 1842 report, what was the average age of death of labourers in Liverpool?', 'About 15 years',
         ['About 35 years', 'About 50 years', 'About 70 years'], 'Chadwick: Liverpool labourers 15, tradesmen 22, gentry 35. The low average reflected very high infant and child deaths. [1]'),
        ('What did John Snow’s investigation in 1854 show?', 'Cholera was spread by contaminated water',
         ['Cholera was spread by bad air (miasma)', 'Cholera was caused by poor diet', 'Cholera was spread by lice'], 'Snow mapped deaths around the Broad Street pump; removing the handle helped end the outbreak. [1]'),
        ('Which job was often given to small children in coal mines?', 'Trapper, opening and closing ventilation doors',
         ['Overlooker', 'Engine driver', 'Mine owner'], 'Trappers as young as five sat alone in the dark for 12 hours. [1]'),
        ('Why did diseases spread quickly in industrial towns?', 'Overcrowded housing, shared privies and polluted water supplies',
         ['People ate too much fresh food', 'There were too many doctors', 'Houses had too many windows'], 'Lack of sanitation + overcrowding = cholera, typhus, typhoid, TB. [1]'),
        ('Which of these was a common punishment in early textile mills?', 'Beatings or fines for lateness and mistakes',
         ['Extra paid holidays', 'Being sent to school', 'Shorter working hours'], 'Overlookers enforced discipline with straps and fines. [1]'),
    ],
    'explain': [
        ('Explain why the average age of death was so low in industrial towns in the 1840s.', 'Very high infant and child death rates from diseases spread by overcrowding, polluted water and lack of sewers pulled the average down; dangerous work and poor diet added to deaths.', '1 mark disease/sanitation; 1 mark infant mortality lowers average; 1 mark work/diet [3]'),
        ('Explain why factory owners employed so many children.', 'Children were cheap (paid much less than adults), small enough to crawl under machines and easy to discipline; families needed the extra income.', '1 mark cheap; 1 mark size/obedience; 1 mark family need [3]'),
        ('Describe two dangers faced by children working in textile mills.', 'Injuries or death from unguarded machinery (e.g. scavengers); lung disease from cotton dust; exhaustion from 12-14 hour days; beatings by overlookers.', '1 mark each danger, 1 mark each development [4]'),
        ('Explain why many people at first did not believe that dirty water caused disease.', 'Most people accepted the miasma theory that disease came from bad air; germs had not yet been identified (Pasteur’s germ theory came in the 1860s), so Snow’s evidence was doubted.', '1 mark miasma; 1 mark lack of germ theory [2]'),
        ('Explain why workers moved to industrial towns despite poor conditions.', 'Factories offered regular wages and jobs, often higher than farm wages; enclosure and farm machinery reduced rural work; families could all earn.', '1 mark pull of jobs/wages; 1 mark push from the countryside [2]'),
    ],
    'claims': [
        ('Life expectancy in industrial towns was low only because adults died young at work.', False, 'The very high number of babies and young children dying from disease was the main reason the average was so low.'),
        ('Cholera was spread through water contaminated with sewage.', True, 'John Snow showed this in 1854 by mapping deaths around the Broad Street pump.'),
        ('Everyone in industrial towns lived in the same poor conditions.', False, 'Wealthy factory owners and professionals lived in larger houses in cleaner areas and lived much longer on average.'),
        ('Children in mills often worked for twelve hours or more a day before 1833.', True, 'Evidence to the Sadler Committee (1832) described days of 12-16 hours.'),
    ],
    'sources': [
        dict(prov='evidence given by a former child mill worker to the Sadler Committee, 1832 (adapted)', kind='primary',
             text='At busy times we worked from three in the morning until ten at night. When I was too tired the overlooker strapped me. I was made crooked by the work and now cannot walk without crutches.',
             about='conditions for child workers', infer='Children worked extremely long hours, were physically punished and could be permanently injured.',
             purpose='To give evidence to a parliamentary committee investigating child labour, supporting the case for reform.',
             plus='it is first-hand testimony from someone who worked in a mill, given at the time', minus='Sadler wanted a Ten Hours law and chose witnesses who supported his case; the committee did not hear mill owners before reporting',
             missing='Whether conditions were the same in all mills, or what owners said in reply.', enq='working conditions for children in the 1830s'),
        dict(prov='Friedrich Engels, The Condition of the Working Class in England, 1845 (adapted)', kind='primary',
             text='In the old town of Manchester the houses are filthy and crowded together. A single privy serves a whole court of families, and the river is a black stream full of rubbish and filth.',
             about='living conditions in Manchester', infer='Living conditions were overcrowded and unsanitary, with very few toilets and a heavily polluted river.',
             purpose='To expose the poverty created by industry and criticise the factory owners and the system.',
             plus='Engels lived and worked in Manchester and saw the conditions himself', minus='he was a critic of capitalism (later co-author of the Communist Manifesto), so he may have chosen the worst areas',
             missing='How wealthier areas of Manchester looked, or the death rates in the town.', enq='living conditions in industrial towns'),
        dict(prov='a book defending factories written by Andrew Ure, 1835 (adapted)', kind='primary',
             text='I have visited many factories and never saw a child punished. The children seemed always cheerful and active, taking pleasure in the light play of their muscles.',
             about='how some people defended factory work', infer='Some writers claimed factory work was healthy and that children were happy and well treated.',
             purpose='To defend the factory system and argue against reform.',
             plus='Ure visited factories at the time', minus='he was a supporter of factory owners and was probably shown the best mills; his view contradicts much other evidence',
             missing='Evidence from children themselves or from doctors about injuries and deformities.', enq='attitudes to factory work in the 1830s'),
    ],
    'essays': [
        ('living conditions in industrial towns were a bigger threat to health than working conditions',
         ['Cholera, typhus and typhoid killed thousands; Chadwick found Liverpool labourers died at an average age of 15.', 'Infant deaths from disease were very high.'],
         ['Factory and mine work caused injuries, deformities and lung diseases, and long hours exhausted children.', 'Poor wages from work were the reason families lived in bad housing.'],
         'Living conditions probably killed more people, especially children, but working conditions and low wages were closely linked to them.',
         ['disease and sanitation', 'injuries at work', 'child labour', 'wages']),
        ('life in industrial towns in the 1840s was worse than life in the countryside',
         ['Overcrowding, pollution and disease made towns deadlier; average ages of death were lower than in rural areas such as Rutland.'],
         ['Rural labourers were also poor, with low wages and seasonal work.', 'Towns offered regular wages and more jobs for women and children.'],
         'Towns were more dangerous for health, but people chose to move because rural life offered few opportunities.',
         ['health', 'wages and jobs', 'housing']),
    ],
})


@c2c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c2c_chadwick(r, D):
    data = {'Manchester': (38, 20, 17), 'Liverpool': (35, 22, 15), 'Rutland (rural)': (52, 41, 38)}
    town = r.choice(['Manchester', 'Liverpool'])
    g, t_, l = data[town]
    rg, rt, rl = data['Rutland (rural)']
    stem = (f'Chadwick’s 1842 report gave the average age of death by social group. {town}: professional persons and gentry {g}, tradesmen {t_}, labourers {l}. '
            f'Rutland (a rural county): gentry {rg}, farmers and tradesmen {rt}, labourers {rl}.')
    if D == 1:
        opts, ans = mcq(r, f'{g - l} years', [f'{g + l} years', f'{rg - rl} years', f'{g - t_} years', f'{l} years'])
        return {'stem': stem + f' How many years longer did gentry live on average than labourers in {town}?', 'options': opts, 'answer': ans, 'key': f'{g} − {l} = {g - l}. [1]'}
    parts = [
        lambda r: (f'Calculate the difference between the average age of death of labourers in {town} and in Rutland.', f'{rl - l} years', f'{rl} − {l} = {rl - l} [1]'),
        lambda r: ('Describe two patterns shown by the data.', f'Wealthier groups lived longer in both places (gentry {g} vs labourers {l} in {town}); every group lived longer in rural Rutland than in the town.', '1 mark each pattern with figures [2]'),
        lambda r: (f'Explain why labourers in {town} had such a low average age of death.', 'Very high infant and child deaths from cholera, typhus and other diseases spread by overcrowding, polluted water and lack of sewers; poor diet and dangerous work.', '1 mark disease/sanitation; 1 mark infant mortality; 1 mark work/diet [3]'),
        lambda r: ('Explain one limitation of using this data alone to judge living conditions.', 'Averages hide the range (many died as babies while some lived long lives); figures cover only some places and Chadwick wanted to prove the case for reform.', '1 mark limitation; 1 mark explanation [2]'),
        lambda r: ('Suggest how this report helped to lead to change.', 'It provided evidence linking dirt and disease to death rates and led to the Public Health Act of 1848.', '1 mark link to evidence; 1 mark Act [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c2d = T('Reform and protest: factory acts, public health and trade unions', 'reform protest factory acts public health trade unions')
build(c2d, {
    'terms': [
        ('trade union', 'an organisation of workers that acts together to improve pay and working conditions'),
        ('Luddites', 'textile workers who smashed new machinery between 1811 and 1816 because it threatened their jobs and wages'),
        ('Chartism', 'a mass working-class movement (1838-1850s) demanding political reform through the six points of the People’s Charter'),
        ('factory inspector', 'an official appointed by the government to check that factories obeyed the law'),
        ('strike', 'when workers refuse to work in order to force employers to meet their demands'),
        ('public health', 'the health of the whole population and the measures, such as clean water and sewers, taken to protect it'),
        ('Medical Officer of Health', 'an official responsible for public health in a town, compulsory under the 1875 Public Health Act'),
        ('petition', 'a written request to the government signed by many people'),
    ],
    'dates': [
        ('the Combination Acts, which banned trade unions, were repealed', 1824),
        ('the Factory Act banned children under 9 from working in textile mills', 1833),
        ('six Dorset farm labourers, the Tolpuddle Martyrs, were sentenced to transportation', 1834),
        ('the People’s Charter was published', 1838),
        ('the Mines Act banned women, girls and boys under 10 from working underground', 1842),
        ('the Ten Hours Act limited women and young people to ten hours a day in textile mills', 1847),
        ('the first Public Health Act set up a General Board of Health', 1848),
        ('the Trades Union Congress (TUC) was founded', 1868),
        ('the Public Health Act forced councils to provide clean water and sewers', 1875),
        ('soldiers attacked a peaceful crowd at St Peter’s Field in Manchester, the Peterloo Massacre', 1819),
    ],
    'mcq': [
        ('Which was a term of the 1833 Factory Act?', 'Children aged 9 to 13 could work no more than 9 hours a day',
         ['All children under 16 were banned from factories', 'Adults could work no more than 8 hours a day', 'Women were given the vote'], '1833: no under-9s in textile mills; 9-13s max 9 h/day; 13-18s max 12 h/day; four inspectors; 2 h schooling a day. [1]'),
        ('Why was the 1833 Factory Act difficult to enforce?', 'There were only four inspectors for thousands of mills',
         ['There were no factories left to inspect', 'Children were not allowed to give evidence', 'The Act only applied in London'], 'Few inspectors and no birth certificates (until 1837) made ages hard to prove. [1]'),
        ('Why were the Tolpuddle Martyrs transported to Australia in 1834?', 'For swearing a secret oath when forming a trade union',
         ['For smashing machines', 'For leading the Peterloo protest', 'For refusing to pay taxes'], 'They were convicted under an old law against secret oaths; mass protests led to their pardon in 1836. [1]'),
        ('Which was one of the six points of the People’s Charter?', 'A vote for every man aged 21 and over',
         ['A vote for all women', 'An end to the monarchy', 'Free schools for all children'], 'Six points: votes for men 21+, secret ballot, no property qualification for MPs, payment of MPs, equal constituencies, annual parliaments. [1]'),
        ('What did the 1875 Public Health Act require?', 'Local councils had to provide clean water, sewers and a Medical Officer of Health',
         ['All factories had to close on Sundays', 'Every family had to own its own house', 'Children had to attend secondary school'], 'Unlike 1848 (voluntary), the 1875 Act was compulsory. [1]'),
        ('What was the main weakness of the 1848 Public Health Act?', 'It was voluntary: towns did not have to set up boards of health unless death rates were very high',
         ['It banned all doctors', 'It only applied to factories', 'It was never passed by Parliament'], 'Local boards were optional unless the death rate exceeded 23 per 1000. [1]'),
    ],
    'explain': [
        ('Explain why the government began to pass factory laws in the 1830s.', 'Campaigners such as Richard Oastler, Michael Sadler and Lord Ashley (Shaftesbury) exposed child labour; the Sadler Committee (1832) provided evidence; public opinion and religious humanitarian ideas put pressure on Parliament.', '1 mark campaigners; 1 mark evidence/reports; 1 mark public pressure [3]'),
        ('Explain why many factory owners opposed factory reform.', 'They feared shorter hours would cut output and profits, make British goods less competitive and that the government should not interfere in business (laissez-faire).', '1 mark profits/competition; 1 mark laissez-faire [2]'),
        ('Explain why the Chartists failed to achieve their aims in the 1840s.', 'Parliament rejected their petitions (1839, 1842, 1848); the movement was divided between “moral force” and “physical force” leaders; the government used troops and arrests; improving economic conditions reduced support.', '1 mark each explained reason up to [3]'),
        ('Explain the importance of the Tolpuddle Martyrs to the trade union movement.', 'Their harsh sentence caused a huge public protest and petition, leading to their pardon in 1836; they became a symbol of workers’ rights to organise.', '1 mark protest/pardon; 1 mark symbol [2]'),
        ('Explain how the work of John Snow and Edwin Chadwick helped to improve public health.', 'Chadwick’s 1842 report linked dirt and disease to high death rates and led to the 1848 Act; Snow’s 1854 investigation proved cholera spread through water, supporting investment in clean water and sewers (e.g. Bazalgette’s London sewers after 1858).', '1 mark Chadwick; 1 mark Snow; 1 mark resulting change [3]'),
        ('Explain the difference between the 1848 and 1875 Public Health Acts.', 'The 1848 Act was permissive (voluntary) for most towns; the 1875 Act was compulsory, forcing councils to provide clean water, drains and sewers and appoint a Medical Officer of Health.', '1 mark each Act; 1 mark contrast [3]'),
    ],
    'claims': [
        ('The 1833 Factory Act ended child labour in Britain.', False, 'It banned only under-9s from textile mills and limited hours for older children; it did not cover mines or other industries, and enforcement was weak.'),
        ('The Chartists achieved none of their six points in the 19th century.', False, 'None were achieved in the 1840s, but the secret ballot came in 1872 and the property qualification for MPs was abolished in 1858; five of the six points were eventually achieved.'),
        ('Trade unions were illegal in Britain until the Combination Acts were repealed in 1824.', True, 'The Combination Acts of 1799-1800 had banned workers from combining; their repeal made unions legal, though still restricted.'),
        ('The 1875 Public Health Act was compulsory for local councils.', True, 'Councils had to provide clean water, drainage and sewers and appoint a Medical Officer of Health.'),
        ('The Luddites were opposed to all forms of technology.', False, 'They targeted specific machines that cut wages and jobs in their trades, often in particular employers’ workshops.'),
    ],
    'sources': [
        dict(prov='a letter by Richard Oastler, “Yorkshire Slavery”, published in the Leeds Mercury, 1830 (adapted)', kind='primary',
             text='Thousands of little children are this very moment existing in a state of slavery more horrid than the victims of colonial slavery, working from six in the morning to seven at night with only thirty minutes for food.',
             about='the campaign for factory reform', infer='Campaigners used shocking comparisons with slavery to shame the public and demand shorter hours for children.',
             purpose='To shock readers and persuade them, and Parliament, to support laws limiting children’s working hours.',
             plus='Oastler knew local mills and wrote at the time, and his claims were supported by later evidence', minus='it is a campaigning letter, deliberately emotional and one-sided',
             missing='The views of mill owners, or what the law said at the time.', enq='why factory reform happened in the 1830s'),
        dict(prov='the People’s Charter, 1838 (adapted summary of its six points)', kind='primary',
             text='A vote for every man twenty-one years of age; the secret ballot; no property qualification for Members of Parliament; payment of Members; equal electoral districts; annual parliaments.',
             about='what the Chartists wanted', infer='The Chartists wanted ordinary working men to have political power through the vote and to be able to stand as MPs.',
             purpose='To set out the movement’s demands clearly so that people would sign the petitions to Parliament.',
             plus='it is the official statement of the Chartists’ aims, written at the time', minus='it shows aims, not how much support there was or what methods Chartists used',
             missing='That women were not included, or that the petitions of 1839, 1842 and 1848 were rejected.', enq='the aims and failure of Chartism'),
    ],
    'essays': [
        ('the Factory Acts quickly improved life for working children',
         ['The 1833 Act banned under-9s from textile mills and limited hours; the 1847 Ten Hours Act reduced hours further.', 'Inspectors made enforcement possible for the first time.'],
         ['There were only four inspectors in 1833 and ages were hard to prove.', 'Mines were not covered until 1842 and many other trades much later.', 'Children still worked long hours in workshops and at home.'],
         'The Acts were an important start, but improvement was slow and uneven; real change came over several decades.',
         ['inspectors and enforcement', 'industries covered', 'later Acts']),
        ('workers’ own protests did more than the government to improve working conditions',
         ['Trade unions and strikes won better pay; protests over Tolpuddle won a pardon; Chartist pressure kept reform in the public eye.'],
         ['Laws passed by Parliament (Factory Acts, Mines Act, Public Health Acts) changed conditions for millions.', 'Middle-class reformers such as Shaftesbury, Chadwick and Oastler drove much change.', 'Protest was often repressed, e.g. Peterloo 1819.'],
         'Government action had the widest effect, but it often came in response to pressure from workers and reformers.',
         ['trade unions', 'Chartism', 'Factory Acts', 'middle-class reformers']),
        ('new scientific knowledge was the main reason public health improved in the 19th century',
         ['Snow’s work on cholera (1854) and later germ theory showed the importance of clean water.'],
         ['Chadwick’s statistics and campaigning led to the 1848 Act before germ theory.', 'The Great Stink (1858) pushed Parliament to fund Bazalgette’s sewers.', 'The extension of the vote in 1867 made politicians respond to working-class needs, leading to the 1875 Act.'],
         'Science helped, but government action, public pressure and events such as the Great Stink were just as important.',
         ['John Snow', 'Chadwick', 'the Great Stink', 'the 1875 Act']),
    ],
})


@c2d.add('C3', (2, 3, 4), 'numerical')
def c2d_hours(r, D):
    age = r.choice([10, 11, 12])
    before = r.choice([12, 13, 14])
    days = 6
    after = 9
    wk_b, wk_a = before * days, after * days
    pc = round(100 * (wk_b - wk_a) / wk_b)
    stem = f'Before 1833 a {age}-year-old child in a cotton mill worked {before} hours a day, {days} days a week. The 1833 Factory Act limited children aged 9 to 13 to 9 hours a day (and no more than 48 hours a week).'
    parts = [
        lambda r: ('Calculate the child’s weekly hours before 1833.', f'{wk_b} hours', f'{before} × {days} = {wk_b} [1]'),
        lambda r: (f'If the mill kept the 9-hour daily limit for {days} days, calculate the weekly hours and state whether this is within the 48-hour limit.', f'{wk_a} hours: over the 48-hour limit, so the child could work only 48 hours.', f'9 × {days} = {wk_a} > 48 [2]'),
        lambda r: ('Calculate the percentage reduction in weekly hours if the child worked the maximum 48 hours.', f'{round(100 * (wk_b - 48) / wk_b)}%', f'({wk_b} − 48) ÷ {wk_b} × 100 [2]'),
        lambda r: ('Explain why some mill owners still broke the law.', 'Only four inspectors; ages hard to prove before birth registration (1837); fines were small compared with profits.', '1 mark each reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


CHAPTERS[2] = [c2a, c2b, c2c, c2d]


# ============================================================== CHAPTER 3: Empire, colonialism and independence

c3a = T('Why European empires expanded in the 19th century', 'european empires expanded 19th century')
build(c3a, {
    'terms': [
        ('imperialism', 'a policy by which a powerful country extends its control over other territories and peoples'),
        ('colony', 'a territory ruled by another country, usually far away'),
        ('protectorate', 'a territory that keeps its own ruler but is controlled and “protected” by a stronger power'),
        ('Scramble for Africa', 'the rapid division and colonisation of most of Africa by European powers between about 1880 and 1914'),
        ('civilising mission', 'the belief used by Europeans to justify empire, that they had a duty to spread their religion, culture and government'),
        ('social Darwinism', 'the false idea that some races were naturally superior and had a right to rule others'),
        ('cash crop', 'a crop grown to be sold or exported for profit rather than eaten by the farmer’s family'),
        ('strategic', 'important for military or naval purposes, such as protecting trade routes'),
    ],
    'dates': [
        ('the First Opium War between Britain and China began', 1839),
        ('the British Crown took direct control of India from the East India Company', 1858),
        ('the Suez Canal opened', 1869),
        ('Queen Victoria was proclaimed Empress of India', 1876),
        ('the Berlin Conference on Africa opened', 1884),
        ('Ethiopia defeated an invading Italian army at the Battle of Adwa', 1896),
        ('British forces defeated the Mahdist army at the Battle of Omdurman in Sudan', 1898),
    ],
    'mcq': [
        ('Which two African states were still independent of European rule in 1914?', 'Ethiopia and Liberia',
         ['Egypt and Kenya', 'Nigeria and Ghana', 'Congo and Angola'], 'By 1914 about 90% of Africa was under European control; Ethiopia (Adwa, 1896) and Liberia stayed independent. [1]'),
        ('What was the main purpose of the Berlin Conference of 1884-85?', 'To agree rules among European powers for claiming African territory',
         ['To give African states independence', 'To end the slave trade in Asia', 'To start the First World War'], 'Hosted by Bismarck; no Africans were invited. [1]'),
        ('Which invention helped Europeans to survive malaria in tropical Africa?', 'The use of quinine', ['The telephone', 'The steam hammer', 'The radio'], 'Quinine reduced deaths from malaria, making inland expansion possible. [1]'),
        ('Why was the Suez Canal strategically important to Britain?', 'It shortened the sea route to India',
         ['It connected Britain to Australia by land', 'It gave Britain control of the Atlantic', 'It carried coal from Wales to Egypt'], 'Opened 1869; Britain bought shares in 1875 and occupied Egypt in 1882. [1]'),
        ('Which weapon gave European armies a huge advantage in colonial wars from the 1880s?', 'The Maxim machine gun',
         ['The longbow', 'The musket', 'The cannonball'], 'E.g. Omdurman 1898: over 10 000 Sudanese killed, fewer than 50 British. [1]'),
        ('Which of these was an economic motive for empire?', 'Gaining raw materials such as rubber, cotton and palm oil',
         ['Spreading Christianity', 'Gaining national prestige', 'Protecting sea routes'], 'Economic: raw materials, markets and investment. [1]'),
    ],
    'explain': [
        ('Explain two economic reasons why European countries wanted colonies in the 19th century.', 'Raw materials (rubber, cotton, palm oil, gold, diamonds) for industry; new markets to sell manufactured goods; places to invest capital profitably.', '2 marks each explained reason [4]'),
        ('Explain how new technology made European expansion easier.', 'Steamships and railways moved troops and goods inland; the telegraph improved communication; quinine protected against malaria; machine guns such as the Maxim gave military superiority.', '1 mark each explained example up to [3]'),
        ('Explain why rivalry between European powers speeded up the Scramble for Africa.', 'Britain, France, Germany, Belgium, Italy and Portugal competed for prestige and strategic advantage; each feared rivals would take land first, so they rushed to claim territory.', '1 mark rivalry/prestige; 1 mark fear of rivals [2]'),
        ('Explain how religious and racial ideas were used to justify empire.', 'Missionaries wanted to spread Christianity; ideas of a “civilising mission” and social Darwinism claimed Europeans were superior and had a duty to rule – ideas now rejected as racist.', '1 mark religion; 1 mark racial ideas; 1 mark evaluation [3]'),
        ('Explain why the Battle of Adwa (1896) was significant.', 'Ethiopia under Emperor Menelik II defeated Italy, keeping its independence and showing that African states could defeat a European army.', '1 mark result; 1 mark significance [2]'),
    ],
    'claims': [
        ('By 1914 every country in Africa was ruled by a European power.', False, 'Ethiopia and Liberia remained independent.'),
        ('African leaders were invited to the Berlin Conference of 1884-85.', False, 'No Africans took part; Europeans divided the continent among themselves.'),
        ('The telegraph and steamships helped Europeans to control distant colonies.', True, 'They made communication and the movement of troops and goods much faster.'),
        ('Empires were built only for economic reasons.', False, 'Political rivalry, strategic bases, prestige and religious and racial ideas were also important motives.'),
    ],
    'sources': [
        dict(prov='the opening lines of Rudyard Kipling’s poem “The White Man’s Burden”, 1899', kind='primary',
             text='Take up the White Man’s burden— / Send forth the best ye breed— / Go bind your sons to exile / To serve your captives’ need.',
             about='attitudes that were used to justify empire', infer='Some Europeans saw empire as a duty to rule and “help” other peoples, a view based on ideas of racial superiority.',
             purpose='To encourage the USA (then taking over the Philippines) and Western readers to see empire as a noble duty.',
             plus='it shows directly an attitude that was popular at the time it was written', minus='it is a poem by one writer and shows a viewpoint, not what colonised peoples experienced',
             missing='The economic motives for empire or the resistance of colonised peoples.', enq='why Europeans believed they had the right to rule other peoples'),
        dict(prov='a speech by a French politician to the French parliament, 1885 (adapted)', kind='primary',
             text='Colonies are for rich countries one of the most profitable investments. France needs markets for her factories, and coaling stations and ports for her navy across the world.',
             about='the motives for French expansion', infer='French leaders wanted colonies for economic profit (markets) and strategic reasons (naval bases).',
             purpose='To persuade the French parliament to support and pay for colonial expansion.',
             plus='it shows what a politician argued in parliament at the time', minus='it is a persuasive speech, so it stresses benefits and ignores costs or the views of colonised peoples',
             missing='Religious or “civilising” motives, or the violence used to take territory.', enq='the motives for European expansion'),
        dict(prov='a modern historian writing in 2015 about the Scramble for Africa', kind='secondary',
             text='Between 1880 and 1914 European powers claimed almost the entire continent. Machine guns, steamships and quinine made conquest possible, while rivalry between the powers made it urgent.',
             about='how and why Africa was colonised so quickly', infer='Technology made conquest possible and rivalry made it happen quickly.',
             purpose='To explain the causes of the Scramble for Africa to readers based on research.',
             plus='it is based on research and hindsight and covers the whole period', minus='it is a short summary that may simplify the causes and leave out African perspectives',
             missing='African resistance, such as the victory at Adwa in 1896.', enq='why the Scramble for Africa happened'),
    ],
    'essays': [
        ('economic motives were the most important reason why European empires expanded in the 19th century',
         ['Industrial economies needed raw materials (rubber, cotton, palm oil, minerals) and markets.', 'Investors and companies such as the British South Africa Company drove expansion.'],
         ['Rivalry and prestige between powers (e.g. Germany’s late entry) caused a rush for land.', 'Strategic aims, such as protecting the route to India via Suez, mattered.', 'Religious and racial ideas (civilising mission) justified expansion.', 'Technology made it possible.'],
         'Economic motives were central, but rivalry turned them into a rapid Scramble, and technology made it possible.',
         ['raw materials and markets', 'rivalry between powers', 'strategic routes', 'religion and ideas', 'technology']),
        ('new technology was the main reason Europeans were able to conquer Africa so quickly',
         ['Maxim guns, steamships, railways, the telegraph and quinine gave Europeans huge advantages.'],
         ['Divisions between African states and alliances with some rulers helped Europeans.', 'Treaties, often misunderstood or forced, were used to claim land.', 'Some African states resisted successfully, e.g. Ethiopia.'],
         'Technology explains the speed of conquest more than any other factor, but European diplomacy and African divisions also mattered.',
         ['weapons', 'medicine', 'transport', 'treaties and divisions']),
    ],
})


@c3a.add('C3', (1, 2, 3, 4), 'numerical')
def c3a_share(r, D):
    rows = r.choice([[('Britain', 30), ('France', 35), ('Germany', 8), ('Belgium', 8), ('Italy', 7), ('Portugal', 7), ('Spain', 1), ('Independent', 4)]])
    stem = ('Approximate share of the land area of Africa controlled by different powers in 1914 (%): ' + ', '.join(f'{a} {b}' for a, b in rows) + '. ')
    tot = sum(b for _, b in rows)
    if D == 1:
        opts, a = mcq(r, 'France', ['Britain', 'Germany', 'Belgium'])
        return {'stem': stem + 'Which power controlled the largest share of Africa’s land area?', 'options': opts, 'answer': a, 'key': 'France (largely the Sahara and West Africa), though Britain ruled more people. [1]'}
    parts = [
        lambda r: ('Calculate the percentage controlled by European powers.', f'{tot - 4}%', f'{tot} − 4 = {tot - 4}% [1]'),
        lambda r: ('Name the two states that made up the independent share.', 'Ethiopia and Liberia', '[1]'),
        lambda r: ('Calculate how many times larger the British share was than the German share.', f'{fmt(30 / 8, 2)} times', '30 ÷ 8 = 3.75 [1]'),
        lambda r: ('Suggest a reason why a large share of land does not necessarily mean the most valuable territory.', 'Much French territory was desert (Sahara) with few people; Britain controlled densely populated, resource-rich areas such as Nigeria, Egypt and South Africa (gold, diamonds).', '1 mark idea; 1 mark example [2]'),
        lambda r: ('Explain why Germany and Italy had smaller African empires than Britain and France.', 'They only became unified countries in 1870-71 and joined the Scramble late, when much land had already been claimed.', '1 mark late unification; 1 mark late start [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c3b = T('The experience of colonised peoples: economy, culture and resistance', 'experience colonised peoples economy culture resistance')
build(c3b, {
    'terms': [
        ('forced labour', 'work that people are made to do against their will, often under threat of punishment'),
        ('indirect rule', 'a system in which colonial powers ruled through existing local chiefs and rulers'),
        ('direct rule', 'a system in which colonial officials governed a territory themselves, replacing local rulers'),
        ('assimilation', 'the French colonial policy of trying to make colonised peoples adopt French language and culture'),
        ('hut tax', 'a tax on each household imposed by colonial governments, which forced people to work for wages or grow cash crops'),
        ('monoculture', 'growing a single crop over a large area, making an economy dependent on it'),
        ('resistance', 'actions taken by colonised peoples to oppose colonial rule, from armed rebellion to protest and non-cooperation'),
        ('deindustrialisation', 'the decline of a country’s own industries, for example Indian hand-weaving after cheap British cloth was imported'),
    ],
    'dates': [
        ('Indian soldiers (sepoys) rose against the East India Company in the Indian Rebellion', 1857),
        ('a Zulu army defeated British forces at the Battle of Isandlwana', 1879),
        ('the Hut Tax War broke out in Sierra Leone', 1898),
        ('Yaa Asantewaa led the Asante War of the Golden Stool against the British', 1900),
        ('the Maji Maji rebellion began against German rule in East Africa', 1905),
        ('the Herero and Nama peoples rose against German rule in South West Africa', 1904),
        ('Belgium took over the Congo Free State from King Leopold II', 1908),
    ],
    'mcq': [
        ('In King Leopold II’s Congo Free State, why were many Congolese people brutally punished?', 'For failing to collect enough wild rubber',
         ['For refusing to learn French', 'For growing too much cotton', 'For building railways'], 'Forced rubber collection, hostage-taking and mutilation; exposed by Roger Casement (1904) and E. D. Morel. [1]'),
        ('Why did colonial governments introduce taxes such as the hut tax?', 'To force people to earn money by working for Europeans or growing cash crops',
         ['To pay for African schools only', 'To reduce the number of houses', 'To encourage people to stay on their own farms'], 'Taxes had to be paid in cash, pushing people into wage labour. [1]'),
        ('What was the immediate trigger of the Indian Rebellion of 1857?', 'Rumours that new rifle cartridges were greased with cow and pig fat',
         ['The opening of the Suez Canal', 'The Salt March', 'The partition of Bengal'], 'The grease offended both Hindu and Muslim sepoys. [1]'),
        ('Which system of rule did Lord Lugard use in Northern Nigeria?', 'Indirect rule through local emirs and chiefs',
         ['Direct rule by French officials', 'Rule by the United Nations', 'Assimilation'], 'Indirect rule was cheaper and used existing power structures. [1]'),
        ('Why were many colonial railways built from the coast to inland mines and plantations?', 'To carry raw materials to ports for export',
         ['To connect African capitals with each other', 'To help Africans travel to Europe', 'To carry soldiers to the Americas'], 'Infrastructure served the export economy. [1]'),
    ],
    'explain': [
        ('Explain how colonial rule changed the economies of colonised countries.', 'Land was taken for plantations and mines; taxes forced people into wage labour; economies were turned to producing one or two cash crops or minerals for export (monoculture), and local industries such as Indian textiles declined.', '1 mark each explained change up to [3]'),
        ('Explain two ways colonial rule affected the culture of colonised peoples.', 'Missionary schools spread Christianity and European languages; traditional authority and customs were weakened or banned; new borders split ethnic groups; Western education created a new educated elite.', '2 marks each explained effect [4]'),
        ('Explain why armed resistance to colonial rule usually failed.', 'European armies had machine guns and modern rifles; they used divide-and-rule and local allies; harsh reprisals and famine (e.g. after Maji Maji) crushed rebellions.', '1 mark each reason up to [3]'),
        ('Explain why some people argue that colonial rule brought benefits, and why others disagree.', 'Some point to railways, schools, hospitals and legal systems; others argue these were built mainly to serve the colonial economy, were paid for by local taxes and came with violence, exploitation and loss of freedom.', '1 mark argument for; 1 mark argument against; 1 mark balance [3]'),
        ('Explain why the Indian Rebellion of 1857 led to changes in how India was governed.', 'The British government ended East India Company rule and took direct control (1858), creating the British Raj; it also reorganised the army and became more cautious about interfering with religion.', '1 mark Crown takes over; 1 mark further change [2]'),
    ],
    'claims': [
        ('Colonised peoples accepted European rule without resistance.', False, 'There was widespread resistance, e.g. Isandlwana 1879, Maji Maji 1905-07, the Asante War of 1900 and the Indian Rebellion of 1857.'),
        ('Railways built in colonies were designed mainly to help export raw materials.', True, 'Most lines ran from mines and plantations to ports, such as the Uganda Railway to Mombasa.'),
        ('The borders drawn by colonial powers followed existing ethnic and cultural boundaries.', False, 'Many borders were drawn by Europeans with straight lines on maps, splitting some peoples and grouping rivals together.'),
        ('German forces killed tens of thousands of Herero and Nama people after the 1904 uprising.', True, 'This is recognised as the first genocide of the 20th century; Germany formally acknowledged it in 2021.'),
    ],
    'sources': [
        dict(prov='a report on the Congo by the British consul Roger Casement, 1904 (adapted)', kind='primary',
             text='In village after village the people told me that soldiers were sent to punish them if the rubber brought in was too little. Many had been killed or had their hands cut off, and whole districts were deserted.',
             about='the treatment of people in the Congo Free State', infer='Congolese people suffered extreme violence, including killings and mutilation, to force them to collect rubber.',
             purpose='To report officially to the British government on conditions in the Congo.',
             plus='Casement travelled through the region and collected eyewitness testimony at the time', minus='he relied partly on what villagers told him through interpreters, and Britain had its own rivalry with Leopold',
             missing='The number of people who died overall or the profits Leopold made from rubber.', enq='the experience of people in the Congo Free State'),
        dict(prov='an interview with an elderly Kenyan woman recorded by a historian in 1970 (adapted)', kind='primary',
             text='When the settlers came, our family’s best land became a coffee farm. My father had to work there to pay the hut tax, and we children were sent to the mission school to learn English.',
             about='the effects of colonial rule on Kenyan families', infer='Colonial rule took African land for settler farms, forced men into wage labour through taxes and changed education.',
             purpose='To record oral history so that African experiences of colonial rule are preserved.',
             plus='it is a first-hand account from someone who lived under colonial rule', minus='it was recorded decades later, so memories may have faded or been shaped by later events such as independence',
             missing='Resistance such as the Mau Mau uprising, or the views of settlers and officials.', enq='how colonial rule changed people’s lives in Kenya',
             why='it is the testimony of someone who lived under colonial rule, even though it was recorded decades later'),
    ],
    'essays': [
        ('the economic impact was the most important effect of colonial rule on colonised peoples',
         ['Land was taken, taxes forced wage labour and economies were based on exporting cash crops and minerals.', 'Local industries declined and wealth flowed to Europe.'],
         ['Cultural effects – language, religion, education – were deep and long-lasting.', 'Political effects such as new borders and loss of self-rule shaped later conflicts.', 'Violence and loss of life, e.g. in the Congo, were devastating.'],
         'Economic effects were central to why empires existed, but cultural and political effects lasted longest.',
         ['land and labour', 'culture and education', 'borders', 'violence']),
        ('resistance to colonial rule before 1914 achieved very little',
         ['Most armed uprisings, such as Maji Maji and the Herero rising, were crushed with huge loss of life.'],
         ['Ethiopia kept its independence after Adwa (1896).', 'Resistance forced changes, such as the end of Company rule in India after 1857.', 'It inspired later independence movements.'],
         'In the short term resistance usually failed, but it had important long-term effects.',
         ['military defeats', 'Adwa', 'changes in colonial policy', 'inspiration for later movements']),
    ],
})


c3c = T('Independence movements: the case of India and Gandhi', 'independence movements india gandhi')
build(c3c, {
    'terms': [
        ('satyagraha', 'Gandhi’s method of non-violent resistance, meaning “truth-force”'),
        ('swaraj', 'self-rule or independence for India'),
        ('swadeshi', 'the campaign to buy Indian-made goods and boycott British imports'),
        ('civil disobedience', 'deliberately and peacefully breaking unjust laws as a form of protest'),
        ('non-cooperation', 'refusing to work with the British authorities, for example by boycotting schools, courts and British goods'),
        ('partition', 'the division of British India in 1947 into two independent states, India and Pakistan'),
        ('the Raj', 'British rule over India from 1858 to 1947'),
        ('ahimsa', 'the principle of non-violence towards all living things'),
    ],
    'dates': [
        ('the Indian National Congress was founded', 1885),
        ('the All-India Muslim League was founded', 1906),
        ('Gandhi returned to India from South Africa', 1915),
        ('British troops fired on a crowd at Jallianwala Bagh in Amritsar', 1919, 4),
        ('Gandhi led the Salt March to Dandi', 1930, 3),
        ('Congress launched the Quit India movement', 1942),
        ('India and Pakistan became independent', 1947),
        ('Gandhi was assassinated in Delhi', 1948),
        ('Gandhi called off the Non-cooperation movement after violence at Chauri Chaura', 1922),
    ],
    'mcq': [
        ('What happened at Jallianwala Bagh, Amritsar, on 13 April 1919?', 'Troops under General Dyer fired on an unarmed crowd, killing hundreds',
         ['Gandhi began the Salt March', 'India was declared independent', 'Congress was founded'], 'Official figure 379 dead (Indian estimates over 1000); it turned many moderates against British rule. [1]'),
        ('Why did Gandhi choose salt as the focus of his 1930 campaign?', 'The salt tax affected every Indian, rich or poor, and making salt was simple to do',
         ['Salt was India’s main export to Britain', 'The British had banned eating salt', 'Salt was only used by the rich'], 'A universal, easy-to-understand symbol of unjust British laws. [1]'),
        ('Approximately how far did Gandhi walk on the Salt March from Sabarmati to Dandi?', 'About 385 km (240 miles)', ['About 38 km', 'About 3850 km', 'About 15 km'], '12 March – 6 April 1930, 24 days. [1]'),
        ('Who became the first Prime Minister of independent India?', 'Jawaharlal Nehru', ['Mahatma Gandhi', 'Muhammad Ali Jinnah', 'Lord Mountbatten'], 'Jinnah became Governor-General of Pakistan; Mountbatten was the last Viceroy. [1]'),
        ('What did the Quit India movement of 1942 demand?', 'An immediate end to British rule in India',
         ['That India should join the Axis powers', 'That India should become part of Pakistan', 'That Britain should build more railways'], 'Congress leaders were arrested within days. [1]'),
        ('What was a major consequence of the partition of India in 1947?', 'Mass migration of 10-15 million people and communal violence that killed hundreds of thousands',
         ['India became part of Pakistan', 'Britain kept control of Delhi', 'There was no movement of people'], 'Estimates of deaths range from about 200 000 to 2 million. [1]'),
    ],
    'explain': [
        ('Explain why the Amritsar Massacre (1919) was a turning point for Indian nationalism.', 'The killing of hundreds of unarmed people, and Dyer’s praise by some in Britain, convinced many Indians, including Gandhi, that British rule could not be trusted; support for Congress and non-cooperation grew.', '1 mark event; 1 mark loss of trust; 1 mark growth of movement [3]'),
        ('Explain why Gandhi’s methods of non-violent protest were effective.', 'Mass, peaceful protests (boycotts, Salt March) involved millions of ordinary Indians, gained worldwide publicity and made British repression look unjust; arrests filled the jails and made India harder and costlier to govern.', '1 mark mass support; 1 mark publicity/moral pressure; 1 mark cost to Britain [3]'),
        ('Explain how the Second World War helped India to gain independence.', 'Britain was economically exhausted and in debt; over 2 million Indians served in the army and expected reward; the Labour government elected in 1945 supported independence; unrest such as the 1946 naval mutiny showed Britain could no longer rely on Indian forces.', '1 mark each explained factor up to [3]'),
        ('Explain why India was partitioned in 1947.', 'The Muslim League under Jinnah feared Hindu domination in a united India and demanded Pakistan (Lahore Resolution, 1940); communal violence such as Direct Action Day in 1946 convinced Britain and Congress that partition was the only way to avoid civil war.', '1 mark Muslim League fears/demand; 1 mark violence; 1 mark British decision [3]'),
        ('Describe two methods used by Gandhi to oppose British rule.', 'Non-cooperation (1920-22): boycotting British goods, schools and courts; civil disobedience: the Salt March (1930), breaking the salt law; fasting; spinning khadi cloth (swadeshi).', '1 mark each method, 1 mark each description [4]'),
    ],
    'claims': [
        ('India gained independence because of Gandhi alone.', False, 'Other leaders (Nehru, Patel, Jinnah, Bose), mass movements, the impact of the Second World War and British weakness were all important.'),
        ('The Salt March involved breaking a British law peacefully.', True, 'Gandhi made salt at Dandi on 6 April 1930, breaking the salt monopoly law; tens of thousands were later arrested.'),
        ('India and Pakistan became independent on the same day in 1947 without any violence.', False, 'Partition caused terrible communal violence and one of the largest mass migrations in history.'),
        ('Gandhi called off the Non-cooperation movement in 1922 because protesters had used violence.', True, 'After a crowd killed 22 policemen at Chauri Chaura, Gandhi stopped the campaign.'),
    ],
    'sources': [
        dict(prov='Jawaharlal Nehru’s speech to India’s Constituent Assembly, 14-15 August 1947', kind='primary',
             text='At the stroke of the midnight hour, when the world sleeps, India will awake to life and freedom.',
             about='how Indian leaders presented independence', infer='Independence was presented as a historic, almost miraculous new beginning for India.',
             purpose='To celebrate independence and inspire Indians with hope and unity at a difficult moment.',
             plus='it is the actual speech made by India’s first Prime Minister at the moment of independence', minus='it is a celebratory speech, so it does not mention the violence of partition happening at the same time',
             missing='The partition violence and mass migration, or the role of the Muslim League.', enq='how India became independent in 1947'),
        dict(prov='a British newspaper report on the Salt March, April 1930 (adapted)', kind='primary',
             text='Mr Gandhi’s march has drawn enormous crowds in every village. Officials say it is a theatrical gesture, but the government is clearly worried that the salt law will be broken all over India.',
             about='reactions to the Salt March', infer='The Salt March gained huge popular support and worried the British government, even if officials tried to dismiss it.',
             purpose='To inform British readers about events in India.',
             plus='it was written at the time and reports both the crowds and the official view', minus='a British newspaper might reflect the government’s view and play down Indian grievances',
             missing='What happened after the march, such as the mass arrests including Gandhi’s in May 1930.', enq='the impact of the Salt March'),
        dict(prov='a historian writing in 2017 about the end of British rule in India', kind='secondary',
             text='By 1945 Britain could no longer afford to hold India. Years of mass protest had made the Raj unworkable, while the war had left Britain bankrupt and its new Labour government committed to withdrawal.',
             about='why Britain left India', infer='Britain left India because of a combination of Indian protest and Britain’s weakness after the Second World War.',
             purpose='To explain the causes of independence for readers of history.',
             plus='the historian can use evidence from both sides and knows what happened later', minus='it is one interpretation and stresses British weakness; other historians give more weight to Indian leaders',
             missing='The role of specific leaders such as Gandhi, Nehru and Jinnah, or the causes of partition.', enq='why India gained independence in 1947'),
    ],
    'essays': [
        ('Gandhi was the main reason India gained independence in 1947',
         ['Gandhi turned Congress into a mass movement through non-cooperation and civil disobedience.', 'The Salt March gained world attention and made British rule look unjust.'],
         ['The Second World War left Britain bankrupt and changed its priorities.', 'The Labour government elected in 1945 supported independence.', 'Other leaders and groups (Nehru, Patel, Jinnah, Bose’s Indian National Army) and unrest such as the 1946 naval mutiny mattered.'],
         'Gandhi was crucial in building mass opposition, but the timing of independence in 1947 owed most to Britain’s weakness after the war.',
         ['non-violent protest', 'the Second World War', 'British politics', 'other Indian leaders']),
        ('the Amritsar Massacre was the most important turning point in the struggle for Indian independence',
         ['It destroyed trust in British rule and pushed Gandhi and Congress to demand self-rule.'],
         ['The Salt March (1930) made the movement truly national and international.', 'The Second World War and Quit India (1942) were decisive for timing.'],
         'Amritsar was the key turning point in attitudes, but later events decided when independence came.',
         ['1919', 'the Salt March', 'Quit India', 'the Second World War']),
    ],
})


c3d = T('Decolonisation in Africa and Asia after 1945 and its legacies', 'decolonisation africa asia after 1945 legacies')
build(c3d, {
    'terms': [
        ('decolonisation', 'the process by which colonies gained their independence from colonial powers'),
        ('nationalism', 'the belief that a people sharing a culture or history should govern themselves'),
        ('self-determination', 'the right of a people to choose their own government'),
        ('neo-colonialism', 'continuing economic or political control of a former colony by a richer country or companies after independence'),
        ('Commonwealth', 'a voluntary association of countries, most of them former parts of the British Empire'),
        ('Mau Mau uprising', 'an armed rebellion against British rule and settler land-ownership in Kenya, 1952-1960'),
        ('“wind of change”', 'Harold Macmillan’s phrase in 1960 describing the growth of African nationalism that Britain had to accept'),
        ('legacy', 'something left behind by the past that continues to have effects'),
    ],
    'dates': [
        ('Indonesia declared independence from the Netherlands', 1945),
        ('India and Pakistan became independent', 1947),
        ('French forces were defeated at Dien Bien Phu in Vietnam', 1954),
        ('Ghana, led by Kwame Nkrumah, became independent', 1957),
        ('seventeen African countries gained independence, the “Year of Africa”', 1960),
        ('Algeria won independence from France after an eight-year war', 1962),
        ('Kenya became independent with Jomo Kenyatta as leader', 1963),
        ('the Organisation of African Unity was founded in Addis Ababa', 1963, 5),
        ('Mozambique and Angola became independent from Portugal', 1975),
        ('Zimbabwe became independent', 1980),
    ],
    'mcq': [
        ('Which country was led to independence in 1957 by Kwame Nkrumah?', 'Ghana', ['Kenya', 'Nigeria', 'Tanzania'], 'Ghana (formerly the Gold Coast), 6 March 1957. [1]'),
        ('Where did Harold Macmillan make his “wind of change” speech in 1960?', 'Cape Town, South Africa', ['London', 'Nairobi', 'New Delhi'], 'To the South African parliament, 3 February 1960. [1]'),
        ('Why is 1960 called the “Year of Africa”?', 'Seventeen African countries became independent that year',
         ['The Scramble for Africa began', 'The African Union was founded', 'All of Africa joined the European Union'], 'Mostly former French colonies, plus Nigeria, Somalia and the Congo. [1]'),
        ('Which war of independence lasted from 1954 to 1962?', 'The Algerian War against France', ['The Indian Rebellion', 'The Mau Mau uprising', 'The Boer War'], 'Hundreds of thousands died; independence came in 1962. [1]'),
        ('Why did Portugal’s African colonies gain independence in 1975?', 'A revolution in Portugal in 1974 ended the dictatorship that had fought to keep them',
         ['The United Nations bought them', 'Portugal lost the Second World War', 'They joined the Commonwealth'], 'The Carnation Revolution (1974) led to independence for Angola, Mozambique and others. [1]'),
        ('Which of these is a legacy of colonial borders in Africa?', 'Some states contain many rival ethnic groups, contributing to conflicts such as the Nigerian Civil War (1967-70)',
         ['All African borders follow natural rivers', 'Every ethnic group has its own country', 'Borders were decided by African referendums'], 'Borders drawn by Europeans often ignored peoples and cultures. [1]'),
    ],
    'explain': [
        ('Explain how the Second World War weakened European empires.', 'Britain, France and the Netherlands were economically exhausted and in debt; Japan’s victories in Asia destroyed the myth of European invincibility; colonial soldiers who fought for “freedom” expected it at home; the USA and USSR opposed old-style empires.', '1 mark each explained point up to [3]'),
        ('Explain why some colonies gained independence peacefully while others fought wars.', 'Where there were few European settlers and strong nationalist parties (e.g. Ghana) Britain negotiated; where large settler populations or strategic interests existed (Algeria, Kenya) colonial powers resisted and violent conflicts followed.', '1 mark peaceful example/reason; 1 mark violent example/reason; 1 mark comparison [3]'),
        ('Explain two economic legacies of colonialism for newly independent countries.', 'Economies depended on exporting one or two raw materials (e.g. copper, cocoa) with unstable prices; infrastructure linked mines to ports rather than connecting regions; few industries; debt and foreign ownership (neo-colonialism).', '2 marks each explained legacy [4]'),
        ('Explain why the Suez Crisis of 1956 is seen as a sign of British decline.', 'Britain and France invaded Egypt after Nasser nationalised the canal, but were forced to withdraw under pressure from the USA and the UN, showing Britain could no longer act as a great imperial power alone.', '1 mark event; 1 mark withdrawal under US pressure; 1 mark significance [3]'),
        ('Explain the role of nationalist leaders in decolonisation, using one example.', 'Leaders such as Kwame Nkrumah (Ghana) built mass parties, organised strikes and boycotts (“Positive Action”), won elections and negotiated independence, showing that colonial rule had lost legitimacy.', '1 mark leader; 1 mark methods; 1 mark outcome [3]'),
    ],
    'claims': [
        ('All African countries gained independence peacefully through negotiation.', False, 'Some, such as Algeria (1954-62) and Kenya (Mau Mau, 1952-60), involved long and violent conflicts.'),
        ('The Second World War speeded up decolonisation.', True, 'It weakened the colonial powers economically and militarily and increased demands for self-determination.'),
        ('Independence immediately ended all economic links between colonies and the former colonial powers.', False, 'Trade, investment, debt, language and membership of groups such as the Commonwealth kept strong links (sometimes called neo-colonialism).'),
        ('Ghana was one of the first colonies in sub-Saharan Africa to gain independence after 1945.', True, 'Ghana became independent in 1957, inspiring nationalist movements across Africa.'),
    ],
    'sources': [
        dict(prov='Kwame Nkrumah’s speech on Ghana’s independence day, 6 March 1957', kind='primary',
             text='At long last, the battle has ended! And thus, Ghana, your beloved country, is free forever! Our independence is meaningless unless it is linked up with the total liberation of the African continent.',
             about='how African leaders saw independence', infer='Nkrumah saw Ghana’s independence as the first step towards freeing the whole of Africa.',
             purpose='To celebrate independence, inspire Ghanaians and encourage nationalists elsewhere in Africa.',
             plus='it is the actual words of Ghana’s leader at the moment of independence', minus='it is a celebratory political speech that does not discuss the difficulties ahead',
             missing='The economic problems Ghana faced, or how independence was achieved through strikes and elections.', enq='the decolonisation of Africa'),
        dict(prov='a speech by British Prime Minister Harold Macmillan to the South African parliament, Cape Town, February 1960', kind='primary',
             text='The wind of change is blowing through this continent, and whether we like it or not, this growth of national consciousness is a political fact.',
             about='British attitudes to African independence by 1960', infer='The British government had accepted that African nationalism could not be stopped and that colonies would become independent.',
             purpose='To signal to South Africa and to British settlers that Britain would not resist African independence.',
             plus='it is a speech by the British Prime Minister, so it shows government policy', minus='it is diplomatic and may hide Britain’s own economic and strategic reasons for withdrawing',
             missing='The views of African nationalists, or conflicts such as the Mau Mau uprising.', enq='why Britain gave up its African colonies'),
        dict(prov='a historian writing in 2012 about the legacies of empire in Africa', kind='secondary',
             text='The new states inherited borders drawn in European capitals, economies built to export a single crop or mineral, and armies trained to keep order rather than to defend nations.',
             about='the legacies of empire', infer='Newly independent African states faced serious problems inherited from colonial rule: artificial borders, dependent economies and powerful armies.',
             purpose='To explain the long-term effects of colonialism on Africa.',
             plus='it uses hindsight to see effects that were not clear at independence', minus='it is a generalisation about a whole continent; experiences varied greatly between countries',
             missing='Achievements after independence or the decisions of African leaders themselves.', enq='the legacies of colonial rule'),
    ],
    'essays': [
        ('decolonisation happened mainly because European powers were weakened by the Second World War',
         ['Britain and France were economically exhausted and dependent on US loans.', 'Japan’s wartime victories ended the myth of European invincibility.'],
         ['Nationalist movements and leaders (Gandhi, Nkrumah, Kenyatta) made colonies ungovernable or won elections.', 'The USA, USSR and the UN supported self-determination.', 'Wars such as Algeria and Indochina were costly and unpopular.'],
         'The war created the conditions, but nationalist pressure decided when and how colonies became independent.',
         ['economic weakness', 'nationalist movements', 'superpowers and the UN', 'colonial wars']),
        ('the most important legacy of empire in Africa has been its borders',
         ['Borders drawn at Berlin and after split peoples and grouped rivals, contributing to conflicts such as the Nigerian Civil War (1967-70).'],
         ['Economic legacies – dependence on raw material exports, debt and foreign ownership – limited development.', 'Languages, legal systems and education still reflect colonial rule.', 'Migration links, such as to Britain and France, are a lasting legacy.'],
         'Borders are a major legacy, but economic dependence has arguably had an even wider impact.',
         ['borders and conflict', 'economic dependence', 'language and culture', 'migration']),
    ],
})


@c3d.add('C3', (1, 2, 3, 4), 'numerical')
def c3d_count(r, D):
    rows = [('1950', 4), ('1956', 8), ('1960', 27), ('1965', 37), ('1975', 48), ('1990', 52)]
    stem = 'The table shows the approximate number of independent states in Africa: ' + ', '.join(f'{a}: {b}' for a, b in rows) + '.'
    i = r.randrange(len(rows) - 1)
    if D == 1:
        opts, a = mcq(r, '1956-1960', ['1950-1956', '1965-1975', '1975-1990'])
        return {'stem': stem + ' In which period did the number of independent African states grow fastest?', 'options': opts, 'answer': a, 'key': '19 more states in 4 years, including 17 in the "Year of Africa", 1960. [1]'}
    parts = [
        lambda r: (f'Calculate the increase in independent states between {rows[i][0]} and {rows[i + 1][0]}.', f'{rows[i + 1][1] - rows[i][1]}', f'{rows[i + 1][1]} − {rows[i][1]} [1]'),
        lambda r: ('Describe the pattern shown by the data.', 'Very few independent states in 1950 (4); rapid growth around 1960 (27 by 1960); continued but slower growth to 52 by 1990 as the last colonies, such as Portuguese territories (1975) and Namibia (1990), became independent.', '1 mark pattern; 1 mark figures [2]'),
        lambda r: ('Explain why so many countries became independent around 1960.', 'Britain and France accepted the “wind of change”; France negotiated independence for almost all its sub-Saharan colonies in 1960; nationalist movements were strong and the UN supported self-determination.', '1 mark each reason up to [3]'),
        lambda r: ('Explain why some countries became independent much later, in the 1970s and after.', 'Colonial powers with many settlers or a dictatorship (Portugal until 1974, white-minority rule in Rhodesia and South Africa’s control of Namibia) resisted; independence came after long wars.', '1 mark reason; 1 mark example [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


CHAPTERS[3] = [c3a, c3b, c3c, c3d]


# ============================================================== CHAPTER 4: The World Wars

c4a = T('Long-term and short-term causes of the First World War', 'long-term short-term causes first world war')
build(c4a, {
    'terms': [
        ('militarism', 'the belief that a country should build up strong armed forces and be ready to use them'),
        ('alliance', 'an agreement between countries to support each other, especially in war'),
        ('imperialism', 'competition between powers to gain and control colonies and empires'),
        ('nationalism', 'strong pride in and loyalty to one’s nation, sometimes including the wish of a people to have its own state'),
        ('Triple Alliance', 'the alliance of Germany, Austria-Hungary and Italy formed in 1882'),
        ('Triple Entente', 'the understanding between Britain, France and Russia completed in 1907'),
        ('Schlieffen Plan', 'Germany’s plan to defeat France quickly by attacking through Belgium before turning to fight Russia'),
        ('long-term cause', 'a cause that built up over many years and created the conditions for an event'),
        ('short-term cause', 'a cause that happened shortly before an event and triggered it'),
    ],
    'dates': [
        ('Germany, Austria-Hungary and Italy formed the Triple Alliance', 1882),
        ('Britain and France signed the Entente Cordiale', 1904),
        ('Britain launched HMS Dreadnought', 1906),
        ('Britain and Russia signed an agreement completing the Triple Entente', 1907),
        ('Austria-Hungary annexed Bosnia, causing the Bosnian Crisis', 1908),
        ('Archduke Franz Ferdinand was assassinated in Sarajevo', 1914, 6),
        ('Britain declared war on Germany', 1914, 8),
        ('the Second Moroccan Crisis took place at Agadir', 1911),
    ],
    'mcq': [
        ('Who assassinated Archduke Franz Ferdinand in Sarajevo on 28 June 1914?', 'Gavrilo Princip, a Bosnian Serb linked to the Black Hand',
         ['Kaiser Wilhelm II', 'A Russian soldier', 'A French spy'], 'Princip was a member of Young Bosnia, armed by the Serbian Black Hand group. [1]'),
        ('Why did Britain declare war on Germany on 4 August 1914?', 'Germany invaded Belgium, whose neutrality Britain had promised to protect in 1839',
         ['Germany attacked London', 'Austria-Hungary invaded Britain', 'Russia asked Britain to attack Serbia'], 'Treaty of London (1839) guaranteed Belgian neutrality. [1]'),
        ('What was special about HMS Dreadnought (1906)?', 'It made all earlier battleships out of date, starting a naval arms race with Germany',
         ['It was the first submarine', 'It was an aircraft carrier', 'It was a German ship captured by Britain'], 'Faster, bigger guns; Britain and Germany raced to build dreadnoughts. [1]'),
        ('Which of these is a short-term cause of the First World War?', 'The assassination of Franz Ferdinand in June 1914',
         ['The alliance system', 'The naval race', 'Imperial rivalry in Africa'], 'Short-term: trigger events of summer 1914. [1]'),
        ('What was the “blank cheque” of July 1914?', 'Germany’s promise to support Austria-Hungary in whatever action it took against Serbia',
         ['A loan from Britain to France', 'A treaty ending the war', 'Payment of reparations'], 'It encouraged Austria-Hungary to issue a harsh ultimatum to Serbia. [1]'),
        ('Which country was in the Triple Alliance in 1914 but did not join the war on Germany’s side?', 'Italy', ['Austria-Hungary', 'Russia', 'France'], 'Italy stayed neutral in 1914 and joined the Allies in 1915. [1]'),
    ],
    'explain': [
        ('Explain how the alliance system turned a local crisis into a European war.', 'When Austria-Hungary declared war on Serbia, Russia mobilised to support Serbia; Germany backed Austria-Hungary and declared war on Russia and France; the Schlieffen Plan took Germany through Belgium, bringing in Britain.', '1 mark each link in the chain up to [3]'),
        ('Explain how the naval race increased tension between Britain and Germany.', 'Germany’s build-up of a large navy threatened British naval supremacy, which Britain relied on to protect its empire and trade; the race to build dreadnoughts created fear and suspicion and pushed Britain closer to France and Russia.', '1 mark threat; 1 mark fear/suspicion; 1 mark effect on alliances [3]'),
        ('Explain why nationalism in the Balkans was a cause of the First World War.', 'Serbian nationalists wanted to unite South Slavs, including those in Austria-Hungary’s Bosnia; Austria-Hungary feared this would break up its empire; Russia supported fellow Slavs – so the region was a “powder keg”.', '1 mark Serbian aims; 1 mark Austrian fear; 1 mark Russian role [3]'),
        ('Explain the difference between long-term and short-term causes, using examples from 1914.', 'Long-term causes built up tension over years (alliances, naval race, imperial rivalry, nationalism); short-term causes triggered war (assassination of Franz Ferdinand, the ultimatum to Serbia, mobilisation, invasion of Belgium).', '1 mark definitions; 1 mark long-term example; 1 mark short-term example [3]'),
        ('Explain why the Schlieffen Plan helped to widen the war.', 'It required Germany to attack France through neutral Belgium; this brought Britain into the war and meant that a Balkan conflict became a war in Western Europe.', '1 mark plan; 1 mark Britain’s entry [2]'),
    ],
    'claims': [
        ('The assassination of Franz Ferdinand was the only cause of the First World War.', False, 'It was the trigger; long-term causes such as alliances, militarism, imperial rivalry and nationalism made a wider war likely.'),
        ('Italy fought alongside Germany throughout the First World War.', False, 'Italy stayed neutral in 1914 and joined the Allies in 1915.'),
        ('The Moroccan Crises increased tension between Germany and France and Britain.', True, 'In 1905 and 1911 Germany challenged French influence in Morocco; Britain backed France and the Entente grew stronger.'),
        ('Britain went to war in 1914 partly because Germany invaded Belgium.', True, 'Britain had guaranteed Belgian neutrality by the Treaty of London (1839).'),
    ],
    'sources': [
        dict(prov='the memoirs of Sir Edward Grey, British Foreign Secretary in 1914, published in 1925', kind='primary',
             text='The lamps are going out all over Europe; we shall not see them lit again in our lifetime.',
             about='how British leaders felt at the outbreak of war', infer='Grey feared the war would be long and would destroy the European way of life.',
             purpose='To record his memories and explain his actions in 1914 to later readers.',
             plus='Grey was a senior decision-maker in 1914, so he knew what leaders felt', minus='it was published in 1925, with hindsight of how terrible the war became, and he may want to defend his reputation',
             missing='Why the war started, or the enthusiasm many ordinary people showed in August 1914.', enq='attitudes to the outbreak of war in 1914',
             why='it was written by someone who took part in the events of 1914 as Foreign Secretary, even though it was published later'),
        dict(prov='a German newspaper editorial, July 1914 (adapted)', kind='primary',
             text='Serbia has shed royal blood and must be punished. If Russia stands behind Serbia, Germany will stand beside Austria-Hungary as a loyal ally. We are surrounded by enemies who envy our strength.',
             about='German attitudes in July 1914', infer='Many Germans felt encircled by enemies and supported standing by Austria-Hungary even if it meant war with Russia.',
             purpose='To persuade German readers to support the government’s backing of Austria-Hungary.',
             plus='it shows views published in Germany during the crisis', minus='a single newspaper may reflect government influence and nationalist feeling rather than all opinion',
             missing='The reactions of other countries, such as Britain’s concern over Belgium.', enq='why the July Crisis led to war'),
        dict(prov='a historian writing in 2013 about the outbreak of war', kind='secondary',
             text='The statesmen of 1914 were like sleepwalkers: watchful but unseeing. Each took decisions that made sense to them, yet together they led Europe into catastrophe.',
             about='responsibility for the war', infer='The historian argues that many leaders, not one country, shared responsibility for the war.',
             purpose='To offer an interpretation of the causes of the war based on research.',
             plus='it is based on detailed research in the archives of several countries', minus='it is one interpretation; others, such as Fritz Fischer in the 1960s, blamed Germany much more',
             missing='The role of long-term factors such as the naval race in detail.', enq='who was to blame for the First World War'),
    ],
    'essays': [
        ('the alliance system was the main cause of the First World War',
         ['Alliances turned a Balkan dispute into a European war in a few days.', 'Germany’s blank cheque and Russia’s support for Serbia show how commitments drove decisions.'],
         ['Militarism and the naval race created fear and plans such as Schlieffen that made war hard to stop.', 'Nationalism in the Balkans created the crisis.', 'Imperial rivalry (Morocco 1905, 1911) built tension.', 'Alliances were defensive and did not force anyone to fight – Italy stayed out.'],
         'Alliances explain why the war spread, but militarism and nationalism explain why war broke out; the causes worked together.',
         ['militarism', 'alliances', 'imperialism', 'nationalism', 'the assassination']),
        ('Germany was mainly to blame for the outbreak of war in 1914',
         ['Germany gave Austria-Hungary the blank cheque and invaded Belgium.', 'Weltpolitik and the naval race alarmed Britain.'],
         ['Austria-Hungary issued an ultimatum Serbia could not fully accept.', 'Russia mobilised early.', 'Serbian nationalists caused the crisis; all the powers had war plans.'],
         'Germany carries a large share of the blame, but responsibility was shared among several powers.',
         ['the blank cheque', 'Austria-Hungary and Serbia', 'Russian mobilisation', 'the Schlieffen Plan']),
    ],
})


c4b = T('Life in the trenches and the home front, 1914-18', 'life trenches home front 1914-18')
build(c4b, {
    'terms': [
        ('no man’s land', 'the area of ground between the front-line trenches of the two opposing armies'),
        ('trench foot', 'a painful condition caused by standing for long periods in cold, wet, muddy trenches, which could lead to amputation'),
        ('shell shock', 'the term used in the First World War for mental and physical breakdown caused by the stress of combat'),
        ('stalemate', 'a situation in which neither side can win or make progress'),
        ('home front', 'the civilian population and activities of a country at war'),
        ('DORA', 'the Defence of the Realm Act (1914), which gave the British government wide powers over civilian life'),
        ('conscription', 'compulsory military service required by law'),
        ('conscientious objector', 'a person who refuses to fight on moral or religious grounds'),
        ('rationing', 'limiting the amount of food or goods each person can buy'),
        ('propaganda', 'information designed to influence people’s opinions, such as recruitment posters'),
    ],
    'dates': [
        ('the Defence of the Realm Act was passed', 1914, 8),
        ('German forces first used chlorine gas at Ypres', 1915),
        ('conscription was introduced in Britain', 1916, 1),
        ('the Battle of the Somme began', 1916, 7),
        ('tanks were used in battle for the first time, on the Somme', 1916, 9),
        ('rationing of sugar was introduced in Britain', 1918, 1),
        ('women over 30 who met a property qualification gained the vote in Britain', 1918, 2),
        ('the Armistice ended fighting on the Western Front', 1918, 11),
        ('Allied troops landed at Gallipoli', 1915),
    ],
    'mcq': [
        ('Approximately how many British casualties were there on the first day of the Somme, 1 July 1916?', 'About 57 000, including about 19 000 killed',
         ['About 570', 'About 5700', 'About 570 000'], 'The worst day in British military history. [1]'),
        ('Roughly how long was the Western Front?', 'About 700 km, from the Channel coast to Switzerland', ['About 7 km', 'About 70 km', 'About 7000 km'], 'About 440 miles. [1]'),
        ('Why were women munitions workers nicknamed “canaries”?', 'Chemicals such as TNT turned their skin yellow', ['They sang while they worked', 'They wore yellow uniforms', 'They worked in coal mines'], 'TNT poisoning was dangerous and sometimes fatal. [1]'),
        ('What did the Defence of the Realm Act (DORA) allow the government to do?', 'Take over factories and land, censor newspapers and control civilian life',
         ['Give all men the vote', 'End the war', 'Ban women from working'], 'DORA (August 1914) gave wide wartime powers. [1]'),
        ('Why was conscription introduced in Britain in 1916?', 'Not enough men were volunteering to replace heavy losses',
         ['The war had ended', 'Women demanded it', 'The army had too many soldiers'], 'Military Service Act, January 1916: single men 18-41 first. [1]'),
        ('Why was it so difficult to break through enemy trenches?', 'Machine guns, barbed wire and artillery made attacks across no man’s land very costly',
         ['Soldiers were not allowed to attack', 'The trenches were made of steel', 'There were no weapons'], 'Defensive technology favoured defenders, causing stalemate. [1]'),
    ],
    'explain': [
        ('Explain why the war on the Western Front became a stalemate.', 'After the Schlieffen Plan failed (Battle of the Marne, 1914), both sides dug trenches; machine guns, barbed wire and artillery made defence much stronger than attack, so neither side could break through.', '1 mark failure of mobile war; 1 mark defensive weapons; 1 mark result [3]'),
        ('Describe two problems soldiers faced in the trenches apart from enemy attack.', 'Trench foot from standing in cold mud and water; rats and lice (spreading trench fever); boredom and lack of sleep; cold and wet; the smell of unburied bodies.', '1 mark each problem, 1 mark each description [4]'),
        ('Explain how the war changed the lives of women in Britain.', 'Women took jobs in munitions, transport and offices left by men, gaining independence and better wages; they joined auxiliary services; their contribution helped win some women the vote in 1918, though many lost their jobs when men returned.', '1 mark work; 1 mark independence/pay; 1 mark vote/limitations [3]'),
        ('Explain why the British government used propaganda during the First World War.', 'To encourage men to volunteer (before conscription), keep up morale, encourage saving food and money, and create hatred of the enemy so people would support the war.', '1 mark each purpose up to [3]'),
        ('Explain why rationing was introduced in Britain in 1918.', 'German U-boats sank many merchant ships, causing shortages; queues and rising prices led to unfair distribution, so the government rationed sugar, meat and butter to share food fairly.', '1 mark U-boats/shortages; 1 mark fairness [2]'),
        ('Explain why the Battle of the Somme is so controversial.', 'Over 1 million casualties on both sides for about 10 km of ground; critics blame General Haig’s tactics; others argue it relieved pressure on the French at Verdun, wore down the German army and taught the British army new tactics.', '1 mark losses; 1 mark criticism; 1 mark counter-argument [3]'),
    ],
    'claims': [
        ('Soldiers spent all their time in the front-line trench fighting.', False, 'Soldiers rotated between front-line, support and reserve trenches and rest areas; much time was spent on routine work and waiting.'),
        ('Tanks were used for the first time in 1916 during the Battle of the Somme.', True, 'British tanks were first used at Flers-Courcelette in September 1916.'),
        ('All women in Britain gained the vote in 1918.', False, 'Only women over 30 who met a property qualification; equal voting with men came in 1928.'),
        ('Civilians in Britain were never attacked from the air during the First World War.', False, 'German Zeppelin airships and later Gotha bombers raided British towns from 1915, killing about 1500 people.'),
        ('Over a million soldiers from India served in the First World War.', True, 'Indian soldiers fought on the Western Front, at Gallipoli and in the Middle East and East Africa.'),
    ],
    'sources': [
        dict(prov='lines from the poem “Dulce et Decorum Est” by Wilfred Owen, a British officer, written in 1917-18', kind='primary',
             text='Bent double, like old beggars under sacks, / Knock-kneed, coughing like hags, we cursed through sludge.',
             about='soldiers’ experience of the Western Front', infer='Soldiers were exhausted, ill and miserable, struggling through mud – far from the heroic image of war.',
             purpose='To show the horror of war and challenge the idea that it is glorious to die for one’s country.',
             plus='Owen was a soldier who experienced the trenches himself and wrote during the war', minus='it is a poem written to make an anti-war point, so it focuses on the worst experiences',
             missing='Comradeship, periods of rest behind the lines, or the views of soldiers who supported the war.', enq='what life was like in the trenches'),
        dict(prov='a letter home from a British soldier on the Western Front, 1916 (adapted)', kind='primary',
             text='Don’t worry about me, mother. We are in good spirits and the food is better than you would think. The worst thing is the rats, which are as big as cats.',
             about='soldiers’ morale', infer='Some soldiers kept up good morale and wanted to reassure their families, though conditions such as rats were unpleasant.',
             purpose='To reassure his family that he was safe and well.',
             plus='it was written at the front by a soldier at the time', minus='letters were censored and soldiers often hid the worst details to avoid worrying their families',
             missing='The danger of shelling and attacks, or illnesses such as trench foot.', enq='what life was like in the trenches'),
        dict(prov='a British government poster, 1917 (adapted)', kind='primary',
             text='Eat less bread and save the ships. Every slice you waste helps the enemy.',
             about='the home front', infer='Food shortages caused by U-boat attacks were serious, and the government wanted civilians to help save food.',
             purpose='Propaganda: to persuade civilians to reduce food waste and support the war effort.',
             plus='it is an official source showing government concerns in 1917', minus='it shows what the government wanted people to do, not whether they actually did it',
             missing='That rationing was introduced in 1918 or how people reacted to shortages.', enq='how the war affected civilians in Britain'),
    ],
    'essays': [
        ('the greatest danger to soldiers on the Western Front came from enemy weapons rather than conditions in the trenches',
         ['Artillery caused the majority of wounds and deaths; machine guns killed thousands in attacks such as the first day of the Somme.', 'Gas, though it killed relatively few, caused terror and injury.'],
         ['Disease, trench foot and infections from wounds killed and disabled many.', 'Shell shock caused long-term mental illness.', 'Conditions lowered resistance and morale.'],
         'Enemy weapons, especially artillery, were the main killer, but conditions caused enormous suffering and illness.',
         ['artillery and machine guns', 'disease and trench foot', 'gas', 'shell shock']),
        ('the First World War changed life on the British home front more for women than for any other group',
         ['Women took on new jobs in munitions and transport; some gained the vote in 1918.'],
         ['Many women lost their jobs after 1918 and only those over 30 with property could vote.', 'Men faced conscription from 1916; conscientious objectors were imprisoned.', 'Everyone faced DORA, rationing (1918) and air raids.'],
         'Women’s lives changed significantly, but the war changed life for all civilians and some changes for women were temporary.',
         ['work', 'the vote', 'DORA and rationing', 'conscription']),
    ],
})


@c4b.add('C3', (1, 2, 3, 4), 'numerical')
def c4b_somme(r, D):
    br, k = 57470, 19240
    total_br, total_g, total_f = 420000, 465000, 200000
    stem = (f'Approximate casualties (killed, wounded, missing and captured) in the Battle of the Somme, July-November 1916: British Empire {total_br:,}, France {total_f:,}, Germany {total_g:,}. '
            f'On the first day, 1 July, the British suffered {br:,} casualties, of whom {k:,} were killed.').replace(',', ' ')
    if D == 1:
        opts, a = mcq(r, f'{fmt(round(100 * k / br, 1), 1)}%', ['19.2%', '57.5%', '50%', '3.4%'])
        return {'stem': stem + ' What percentage of British first-day casualties were killed?', 'options': opts, 'answer': a, 'key': f'{k} ÷ {br} × 100 = {fmt(round(100 * k / br, 1), 1)}%. [1]'}
    allied = total_br + total_f
    parts = [
        lambda r: ('Calculate the total Allied (British Empire and French) casualties.', f'{allied:,}'.replace(',', ' '), f'{total_br} + {total_f} [1]'),
        lambda r: ('Calculate the total casualties on both sides.', f'{allied + total_g:,}'.replace(',', ' '), f'{allied} + {total_g} = {allied + total_g} – over a million [1]'),
        lambda r: ('Calculate the percentage of first-day British casualties who were killed, to one decimal place.', f'{fmt(round(100 * k / br, 1), 1)}%', f'{k} ÷ {br} × 100 [2]'),
        lambda r: ('Explain why casualties on the first day were so high.', 'The week-long bombardment failed to destroy the barbed wire and deep German dugouts; troops walked slowly across no man’s land carrying heavy kit and were cut down by machine guns.', '1 mark failed bombardment; 1 mark machine guns/tactics [2]'),
        lambda r: ('Explain why historians disagree about whether the Somme was a failure.', 'Huge losses for about 10 km of ground suggest failure; but it relieved pressure on Verdun, wore down the German army and taught new tactics, so some see it as a necessary step to victory in 1918.', '1 mark failure argument; 1 mark success argument; 1 mark judgement [3]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c4c = T('From peace treaties to the rise of dictators, 1919-39', 'peace treaties rise dictators 1919-39')
build(c4c, {
    'terms': [
        ('Treaty of Versailles', 'the peace treaty between the Allies and Germany signed on 28 June 1919'),
        ('reparations', 'payments for war damage that Germany was made to pay to the Allies'),
        ('war guilt clause', 'Article 231 of the Treaty of Versailles, which made Germany accept blame for the war'),
        ('League of Nations', 'an international organisation set up in 1920 to keep peace through cooperation and collective security'),
        ('dictator', 'a ruler with total power who is not limited by laws, elections or a parliament'),
        ('appeasement', 'the policy of giving in to some of a dictator’s demands in order to avoid war'),
        ('hyperinflation', 'extremely rapid rise in prices, as in Germany in 1923, making money almost worthless'),
        ('Anschluss', 'the union of Germany and Austria, forbidden in 1919 but carried out by Hitler in March 1938'),
        ('fascism', 'a nationalist, anti-democratic political system with a single party and an all-powerful leader, first in Mussolini’s Italy'),
    ],
    'dates': [
        ('the Treaty of Versailles was signed', 1919, 6),
        ('the League of Nations held its first meeting', 1920),
        ('Mussolini came to power in Italy after the March on Rome', 1922),
        ('hyperinflation reached its peak in Germany', 1923),
        ('the Wall Street Crash began the Great Depression', 1929),
        ('Japan invaded Manchuria', 1931),
        ('Hitler became Chancellor of Germany', 1933),
        ('Italy invaded Abyssinia', 1935),
        ('German troops marched into the Rhineland', 1936),
        ('the Munich Agreement gave the Sudetenland to Germany', 1938, 9),
        ('Germany and the Soviet Union signed the Nazi-Soviet Pact', 1939, 8),
        ('Germany invaded Poland', 1939, 9),
    ],
    'mcq': [
        ('Which term was part of the Treaty of Versailles?', 'The German army was limited to 100 000 men',
         ['Germany gained Alsace-Lorraine', 'Germany was allowed a large air force', 'Germany could unite with Austria'], 'Also: no air force, 6 battleships, no submarines, demilitarised Rhineland. [1]'),
        ('Who were the “Big Three” at the Paris Peace Conference of 1919?', 'Wilson, Clemenceau and Lloyd George',
         ['Hitler, Mussolini and Stalin', 'Churchill, Roosevelt and Stalin', 'Kaiser Wilhelm, Lenin and Wilson'], 'USA, France and Britain. [1]'),
        ('Which major power never joined the League of Nations?', 'The USA', ['Britain', 'France', 'Italy'], 'The US Senate rejected membership, weakening the League. [1]'),
        ('Why did many Germans hate the Treaty of Versailles?', 'It was a “diktat” imposed without negotiation, blaming Germany and taking land, colonies and money',
         ['It gave Germany too many colonies', 'It made Germany a monarchy again', 'It forced France to pay reparations'], 'War guilt, reparations (£6600 million), land losses and disarmament. [1]'),
        ('Which event greatly increased support for the Nazi Party after 1929?', 'The Great Depression and mass unemployment',
         ['The Treaty of Versailles being cancelled', 'Germany winning the First World War', 'The League of Nations moving to Berlin'], 'About 6 million unemployed by 1932. [1]'),
        ('What did the Munich Agreement of September 1938 do?', 'Allowed Germany to take the Sudetenland from Czechoslovakia',
         ['Ended the Second World War', 'Created the League of Nations', 'Divided Poland between Germany and the USSR'], 'Chamberlain claimed “peace for our time”; Hitler took the rest of Czechoslovakia in March 1939. [1]'),
    ],
    'explain': [
        ('Explain why the Treaty of Versailles caused resentment in Germany.', 'Germans had not been allowed to negotiate (a diktat); Article 231 blamed Germany for the war; reparations damaged the economy; Germany lost about 13% of its land, all its colonies and was disarmed, which felt humiliating.', '1 mark each explained point up to [3]'),
        ('Explain why the League of Nations failed to keep peace in the 1930s.', 'The USA never joined and Germany, Japan and Italy left; it had no army of its own; sanctions were weak and slow; it failed to stop Japan in Manchuria (1931) and Italy in Abyssinia (1935-36), so aggressors saw it could be ignored.', '1 mark each explained weakness or example up to [3]'),
        ('Explain how the Great Depression helped Hitler to come to power.', 'Mass unemployment (about 6 million by 1932) and poverty made people lose faith in the Weimar government; the Nazis promised jobs, strong leadership and to overturn Versailles; they became the largest party in the Reichstag in July 1932 and Hitler became Chancellor in January 1933.', '1 mark economic crisis; 1 mark Nazi promises; 1 mark result [3]'),
        ('Explain why Britain and France followed a policy of appeasement.', 'Memories of the First World War made people fear another war; Britain’s armed forces were not ready; many thought the Treaty of Versailles was too harsh; some saw Hitler as a barrier to communism.', '1 mark each reason up to [3]'),
        ('Explain why the Nazi-Soviet Pact of August 1939 made war more likely.', 'It meant Hitler could invade Poland without fear of fighting the USSR; secretly the two agreed to divide Poland; Britain and France had promised to defend Poland, so war followed.', '1 mark no two-front war; 1 mark secret division of Poland; 1 mark link to war [3]'),
        ('Explain how Hitler turned Germany into a dictatorship in 1933-34.', 'After the Reichstag Fire (February 1933) the Enabling Act (March 1933) let him make laws without the Reichstag; other parties and trade unions were banned; the Night of the Long Knives (1934) removed rivals; when Hindenburg died (August 1934) Hitler became Führer.', '1 mark each step up to [3]'),
    ],
    'claims': [
        ('The Treaty of Versailles allowed Germany to keep its colonies.', False, 'Germany lost all its overseas colonies, which became League of Nations mandates run mainly by Britain and France.'),
        ('Hitler seized power by force in 1933.', False, 'He was appointed Chancellor legally by President Hindenburg in January 1933, then used legal and illegal methods to build a dictatorship.'),
        ('The League of Nations failed to stop Italy invading Abyssinia.', True, 'Sanctions were weak and did not include oil; Britain and France made a secret deal (Hoare-Laval Pact) to give Italy part of Abyssinia.'),
        ('Appeasement had no supporters in Britain in 1938.', False, 'Chamberlain was cheered on his return from Munich; many people feared another war.'),
    ],
    'sources': [
        dict(prov='a German cartoon published in 1919, described in words', kind='primary',
             text='The cartoon shows Germany as a figure lying on a guillotine while Wilson, Clemenceau and Lloyd George stand over it. The caption reads: “The verdict of Versailles.”',
             about='German reactions to the Treaty of Versailles', infer='Germans saw the treaty as a cruel punishment, almost a death sentence, imposed by the Allied leaders.',
             purpose='To express anger at the treaty and encourage German readers to reject it.',
             plus='it shows genuine German feeling at the time the treaty was signed', minus='it is deliberately exaggerated and one-sided, designed to provoke anger',
             missing='The Allies’ reasons for the terms, such as French losses and fears.', enq='German reactions to the Treaty of Versailles'),
        dict(prov='a statement by British Prime Minister Neville Chamberlain on returning from Munich, 30 September 1938', kind='primary',
             text='My good friends, this is the second time in our history that there has come back from Germany to Downing Street peace with honour. I believe it is peace for our time.',
             about='British attitudes to appeasement in 1938', infer='Chamberlain believed, or wanted the public to believe, that appeasement had secured lasting peace.',
             purpose='To reassure the British public and win support for the Munich Agreement.',
             plus='it is Chamberlain’s own words at the time, showing government policy', minus='he wanted to justify his policy, so he may have been more confident in public than in private; Britain was also rearming',
             missing='Czechoslovakia’s view, or that Hitler occupied the rest of Czechoslovakia in March 1939.', enq='why Britain followed a policy of appeasement'),
        dict(prov='a historian writing in 2008 about the 1930s', kind='secondary',
             text='Appeasement was not simply cowardice. Britain’s leaders knew their country was not ready for war, and the extra year gained at Munich was used to build fighter aircraft and radar.',
             about='appeasement', infer='The historian argues that appeasement was a sensible policy that gave Britain time to rearm.',
             purpose='To challenge the view that appeasement was a cowardly mistake.',
             plus='the historian can use evidence such as rearmament figures not available to people in 1938', minus='it is a revisionist interpretation; others argue that appeasement encouraged Hitler and allowed Germany to grow stronger too',
             missing='How appeasement affected Czechoslovakia, or Hitler’s growing demands.', enq='whether appeasement was a mistake'),
    ],
    'essays': [
        ('the Treaty of Versailles was the main cause of the Second World War',
         ['It created resentment that Hitler exploited; he promised to overturn it (Rhineland 1936, Anschluss 1938).', 'Reparations contributed to economic problems.'],
         ['The Great Depression brought Hitler to power and weakened democracies.', 'The failure of the League of Nations (Manchuria, Abyssinia) encouraged aggression.', 'Appeasement allowed Germany to grow stronger; the Nazi-Soviet Pact made invasion of Poland possible.', 'Hitler’s own aims for Lebensraum went beyond reversing Versailles.'],
         'Versailles created the grievances, but Hitler’s aims, the Depression and the failure to stop him explain why war came in 1939.',
         ['the Treaty of Versailles', 'the Depression', 'the League of Nations', 'appeasement', 'Hitler’s aims']),
        ('appeasement was a mistake',
         ['It encouraged Hitler to make more demands; Czechoslovakia was abandoned; the USSR distrusted Britain and France and made the Nazi-Soviet Pact.'],
         ['Britain was not ready for war in 1938; the extra year allowed rearmament (Spitfires, radar).', 'Public opinion and the Dominions did not support war over the Sudetenland.'],
         'With hindsight appeasement failed to stop Hitler, but in 1938 it was an understandable policy.',
         ['British rearmament', 'public opinion', 'Hitler’s demands', 'the USSR']),
        ('the Great Depression was the most important reason for the rise of dictators in the 1930s',
         ['Unemployment and poverty made people turn to extreme parties promising work and strong leadership, e.g. the Nazis in 1930-33.'],
         ['Mussolini came to power in 1922, before the Depression.', 'Resentment of Versailles, fear of communism and weak democratic traditions mattered.', 'Propaganda and the use of violence helped dictators.'],
         'The Depression was the key reason for Hitler’s rise, but dictators also rose because of fear, resentment and weak democracies.',
         ['unemployment', 'Versailles', 'fear of communism', 'propaganda']),
    ],
})


c4d = T('The Second World War and the Holocaust: causes, events and impact on civilians', 'second world war holocaust causes events impact civilians')
build(c4d, {
    'terms': [
        ('Blitzkrieg', '“lightning war”: fast attacks using tanks, aircraft and motorised troops together'),
        ('the Blitz', 'the German bombing campaign against British cities from September 1940 to May 1941'),
        ('evacuation', 'moving people, especially children, away from cities in danger of bombing'),
        ('Holocaust', 'the systematic, state-sponsored persecution and murder of about six million Jews by Nazi Germany and its collaborators'),
        ('genocide', 'the deliberate killing of a large number of people from a particular national, ethnic or religious group'),
        ('ghetto', 'a closed-off area of a city where Jews were forced to live by the Nazis'),
        ('Final Solution', 'the Nazi plan for the systematic murder of all European Jews, coordinated at the Wannsee Conference in 1942'),
        ('antisemitism', 'hatred of, or prejudice against, Jewish people'),
        ('total war', 'a war in which a country uses all its resources, including civilians and industry, and civilians become targets'),
    ],
    'dates': [
        ('the Nuremberg Laws took away the citizenship rights of German Jews', 1935),
        ('Kristallnacht, a night of violence against Jews, took place across Germany', 1938, 11),
        ('Germany invaded Poland', 1939, 9),
        ('British forces were evacuated from Dunkirk', 1940, 5),
        ('Germany invaded the Soviet Union (Operation Barbarossa)', 1941, 6),
        ('Japan attacked the US fleet at Pearl Harbor', 1941, 12),
        ('Nazi officials met at the Wannsee Conference to coordinate the “Final Solution”', 1942, 1),
        ('the German Sixth Army surrendered at Stalingrad', 1943, 2),
        ('Allied forces landed in Normandy on D-Day', 1944, 6),
        ('Soviet troops liberated Auschwitz-Birkenau', 1945, 1),
        ('atomic bombs were dropped on Hiroshima and Nagasaki', 1945, 8),
        ('the United Nations was founded', 1945, 10),
    ],
    'mcq': [
        ('About how many Jews were murdered in the Holocaust?', 'About 6 million', ['About 60 000', 'About 600 000', 'About 60 million'], 'About two-thirds of Europe’s Jews. [1]'),
        ('Which groups, besides Jews, were also persecuted and murdered by the Nazis?', 'Roma and Sinti, disabled people, Slavs, gay men and political opponents',
         ['Only British prisoners of war', 'Only American soldiers', 'No other groups'], 'Nazi racial and political policies targeted many groups. [1]'),
        ('Why is 27 January marked as Holocaust Memorial Day?', 'Auschwitz-Birkenau was liberated on that day in 1945',
         ['The war ended on that day', 'Hitler came to power on that day', 'The Nuremberg Laws were passed on that day'], 'Liberated by the Soviet army. [1]'),
        ('Which battle is often seen as the turning point of the war on the Eastern Front?', 'Stalingrad (1942-43)', ['Dunkirk', 'Pearl Harbor', 'the Battle of Britain'], 'The German Sixth Army surrendered in February 1943. [1]'),
        ('Why did the Japanese attack on Pearl Harbor in December 1941 matter?', 'It brought the USA into the war', ['It ended the war in Europe', 'It caused Germany to surrender', 'It led to the Munich Agreement'], 'The USA declared war on Japan; Germany then declared war on the USA. [1]'),
        ('What was Operation Pied Piper (September 1939)?', 'The evacuation of about 1.5 million people, mostly children, from British cities',
         ['The D-Day landings', 'The bombing of Dresden', 'The invasion of Poland'], 'Children were sent to the countryside to escape expected bombing. [1]'),
        ('About how many British civilians were killed in the Blitz of 1940-41?', 'About 43 000', ['About 430', 'About 4300', 'About 430 000'], 'London, Coventry, Liverpool and other cities were hit. [1]'),
    ],
    'explain': [
        ('Explain how Nazi persecution of Jews increased between 1933 and 1945.', 'From boycotts of Jewish shops (1933) and the Nuremberg Laws (1935) removing citizenship, to violence on Kristallnacht (1938), ghettos in occupied Poland, mass shootings by the Einsatzgruppen (from 1941) and death camps such as Auschwitz after the Wannsee Conference (1942).', '1 mark each correctly sequenced stage up to [4]'),
        ('Explain two ways the Second World War affected civilians in Britain.', 'Bombing in the Blitz killed about 43 000 and destroyed homes; evacuation separated families; rationing from January 1940 limited food and clothes; women were conscripted for war work from 1941.', '2 marks each explained effect [4]'),
        ('Explain why civilians suffered more in the Second World War than in the First.', 'Mass bombing of cities (Blitz, Dresden, Hiroshima), occupation and genocide (the Holocaust), sieges such as Leningrad and the targeting of civilian industry meant civilians were deliberately attacked on a huge scale; about half or more of all deaths were civilians.', '1 mark bombing; 1 mark genocide/occupation; 1 mark scale/deliberate targeting [3]'),
        ('Explain why the Holocaust is important to remember today.', 'It shows where prejudice, propaganda and dehumanisation can lead; it honours the victims; it helps people recognise warning signs of genocide and led to the 1948 Genocide Convention and the Universal Declaration of Human Rights.', '1 mark each reason up to [3]'),
        ('Explain why the D-Day landings of June 1944 were important.', 'They opened a second front in Western Europe, liberated France and forced Germany to fight on two fronts, leading to Germany’s defeat in May 1945.', '1 mark second front; 1 mark consequence [2]'),
    ],
    'claims': [
        ('The Holocaust happened suddenly in 1942 without any warning signs.', False, 'Persecution built up step by step from 1933: boycotts, the Nuremberg Laws, Kristallnacht and ghettos came before mass murder.'),
        ('The Soviet Union suffered the greatest number of deaths of any country in the Second World War.', True, 'Estimates are around 24-27 million Soviet deaths, military and civilian.'),
        ('Only soldiers were killed in the Second World War.', False, 'Tens of millions of civilians died from bombing, genocide, starvation, sieges and reprisals.'),
        ('Evacuation in Britain in 1939 was compulsory for all children.', False, 'Evacuation was voluntary; many children returned home during the “Phoney War” before the Blitz.'),
    ],
    'sources': [
        dict(prov='Winston Churchill’s speech to the House of Commons, 4 June 1940, after the Dunkirk evacuation', kind='primary',
             text='We shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields and in the streets, we shall fight in the hills; we shall never surrender.',
             about='how the British government responded to the fall of France', infer='Churchill wanted to show that Britain would keep fighting even if invaded, despite the defeat in France.',
             purpose='To boost morale in Britain and show the world, especially the USA, that Britain would not make peace with Hitler.',
             plus='it is the Prime Minister’s own words, so it shows government policy and tone in 1940', minus='it is a morale-boosting speech, so it hides how serious the military situation was',
             missing='What ordinary people thought, or the scale of the losses of equipment at Dunkirk.', enq='British morale in 1940'),
        dict(prov='the diary of a Jewish teenager hiding in Amsterdam, 1943 (adapted)', kind='primary',
             text='We hear that our Jewish friends are being taken away in groups. The Gestapo treat them roughly and transport them in cattle trucks to the camps in the east. We must keep very quiet here.',
             about='the persecution of Jews in occupied Europe', infer='Jews in occupied countries lived in fear as they were rounded up and deported to camps; some went into hiding.',
             purpose='To record private thoughts and experiences during hiding.',
             plus='it is a personal account written at the time by someone directly affected', minus='the writer heard about deportations second-hand and could only know part of what was happening',
             missing='What happened in the camps, or the scale of the Holocaust across Europe.', enq='how the Holocaust affected Jewish people'),
        dict(prov='a report by a British army officer after the liberation of Bergen-Belsen camp, April 1945 (adapted)', kind='primary',
             text='Thousands of starving prisoners lay in huts and on the ground. Typhus was everywhere, and piles of unburied bodies lay around the camp.',
             about='the Nazi camp system', infer='Conditions in the camps were horrific, with starvation, disease and mass death.',
             purpose='To report officially what troops found when they liberated the camp.',
             plus='it is an eyewitness account by an officer who entered the camp', minus='it describes one camp at the end of the war; Belsen was not a death camp like Auschwitz with gas chambers',
             missing='How the Nazis organised the deportation and murder of Jews across Europe.', enq='what happened in Nazi camps'),
    ],
    'essays': [
        ('civilians suffered more than soldiers in the Second World War',
         ['More civilians than soldiers died overall; about 6 million Jews were murdered in the Holocaust.', 'Bombing (the Blitz, Dresden, Hiroshima), sieges such as Leningrad and occupation killed millions.'],
         ['Soldiers faced the direct dangers of combat; millions of soldiers died, e.g. at Stalingrad.', 'Prisoners of war suffered badly, especially Soviet prisoners in German hands.', 'In some countries, such as Britain, civilian deaths were much lower than military deaths.'],
         'Overall civilians suffered on an unprecedented scale, though experiences varied greatly between countries.',
         ['the Holocaust', 'bombing', 'occupation', 'military deaths']),
        ('the bombing of cities was the most important way the Second World War affected civilians',
         ['The Blitz, Dresden and Tokyo raids and the atomic bombs killed hundreds of thousands and destroyed homes.'],
         ['Genocide in the Holocaust killed millions.', 'Starvation, sieges and occupation affected more people in Eastern Europe and Asia.', 'Evacuation, rationing and war work changed daily life everywhere.'],
         'Bombing was terrible, but genocide and occupation had an even greater impact on civilians.',
         ['the Blitz', 'the Holocaust', 'occupation', 'rationing and evacuation']),
    ],
})


@c4d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c4d_deaths(r, D):
    rows = [('Soviet Union', 8.7, 17.0), ('China', 3.8, 16.0), ('Germany', 5.3, 1.5), ('Poland', 0.2, 5.6), ('Japan', 2.1, 0.6), ('United Kingdom', 0.38, 0.07), ('USA', 0.41, 0.01)]
    pick = [rows[0], rows[5]] + r.sample([x for i, x in enumerate(rows) if i not in (0, 5)], r.choice([2, 3]))
    r.shuffle(pick)
    stem = 'Estimated deaths in the Second World War (millions, military then civilian): ' + '; '.join(f'{a} {fmt(m, 2)} and {fmt(c, 2)}' for a, m, c in pick) + '. Estimates vary between historians.'
    mx = max(pick, key=lambda x: x[1] + x[2])
    civ = max(pick, key=lambda x: x[2] / (x[1] + x[2]))
    if D == 1:
        opts, a = mcq(r, mx[0], [x[0] for x in pick if x is not mx])
        return {'stem': stem + ' Which of these countries had the greatest total number of deaths?', 'options': opts, 'answer': a, 'key': f'{mx[0]}: {fmt(mx[1] + mx[2], 2)} million. [1]'}
    p = r.choice(pick)
    parts = [
        lambda r: (f'Calculate the total deaths for {p[0]}.', f'{fmt(p[1] + p[2], 2)} million', f'{fmt(p[1], 2)} + {fmt(p[2], 2)} [1]'),
        lambda r: (f'Calculate the percentage of {p[0]}’s deaths that were civilians, to the nearest whole number.', f'{round(100 * p[2] / (p[1] + p[2]))}%', f'{fmt(p[2], 2)} ÷ {fmt(p[1] + p[2], 2)} × 100 [2]'),
        lambda r: ('Identify the country with the highest proportion of civilian deaths and suggest a reason.', f'{civ[0]}: ' + {'Poland': 'occupation, the Holocaust (about 3 million Polish Jews) and mass killings.', 'China': 'Japanese invasion, massacres, famine and disease.', 'Soviet Union': 'invasion, sieges such as Leningrad, mass killings and famine.'}.get(civ[0], 'bombing and occupation.'), '1 mark country; 1 mark reason [2]'),
        lambda r: ('Explain why estimates of deaths in the Second World War vary.', 'Records were destroyed or never kept, especially in occupied areas; borders changed; deaths from famine and disease are hard to count; governments sometimes changed figures for political reasons.', '1 mark each reason [2]'),
        lambda r: ('Compare the experience of civilians in the United Kingdom with those in the Soviet Union, using the data.', 'UK civilian deaths (about 0.07 million, mainly from bombing) were tiny compared with the Soviet Union (about 17 million) because the USSR was invaded and occupied, with sieges, massacres and famine.', '1 mark comparison with figures; 1 mark reason [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c4e = T('How and why we remember war: memorials and significance', 'remember war memorials significance')
build(c4e, {
    'terms': [
        ('memorial', 'a structure, place or event created to remember people who died or events of the past'),
        ('commemoration', 'the act of honouring and remembering an event or people, for example in a ceremony'),
        ('significance', 'the importance of an event or person, judged by its impact, how many it affected and how long its effects lasted'),
        ('Remembrance Day', '11 November, the anniversary of the 1918 Armistice, when the dead of wars are remembered'),
        ('Cenotaph', 'an “empty tomb” memorial; the one in Whitehall, London, is the focus of Britain’s national Remembrance service'),
        ('Unknown Warrior', 'an unidentified soldier buried in Westminster Abbey in 1920 to represent all those whose bodies were never found or identified'),
        ('interpretation', 'a particular view of the past, which memorials and museums also present'),
    ],
    'dates': [
        ('John McCrae wrote the poem “In Flanders Fields”', 1915),
        ('the Unknown Warrior was buried in Westminster Abbey', 1920),
        ('the first poppy appeal was held in Britain', 1921),
        ('the Menin Gate memorial was unveiled at Ypres', 1927),
        ('India Gate, the All India War Memorial in New Delhi, was inaugurated', 1931),
        ('the Thiepval Memorial to the Missing of the Somme was unveiled', 1932),
        ('the Hiroshima Peace Memorial (Genbaku Dome) became a UNESCO World Heritage Site', 1996),
        ('the Memorial to the Murdered Jews of Europe opened in Berlin', 2005),
    ],
    'mcq': [
        ('Why is the red poppy a symbol of remembrance?', 'Poppies grew on the battlefields of Flanders, as described in John McCrae’s poem',
         ['Poppies were used to treat wounds', 'Soldiers carried poppies into battle', 'The poppy was the flag of Belgium'], '"In Flanders fields the poppies blow / Between the crosses, row on row" (1915). [1]'),
        ('What happens at the Menin Gate in Ypres every evening?', 'Buglers play the Last Post', ['A parade of tanks', 'A firework display', 'A football match'], 'A tradition since 1928, interrupted only during the German occupation in the Second World War. [1]'),
        ('Why do many war memorials list names but have no graves?', 'The bodies of many soldiers were never found or identified',
         ['Soldiers did not want graves', 'Graves were not allowed in Belgium', 'All soldiers were buried at sea'], 'Thiepval lists over 72 000 missing from the Somme. [1]'),
        ('What is Anzac Day (25 April) a commemoration of?', 'The landing of Australian and New Zealand troops at Gallipoli in 1915',
         ['The end of the Second World War', 'The signing of the Treaty of Versailles', 'D-Day'], 'Now remembers all Australians and New Zealanders who served. [1]'),
        ('What does the Hiroshima Peace Memorial mainly encourage visitors to think about?', 'The horror of nuclear weapons and the need for peace',
         ['Celebrating victory in the war', 'Remembering the First World War only', 'The history of Japanese emperors'], 'The ruined dome was left as it was after 6 August 1945. [1]'),
    ],
    'explain': [
        ('Explain why so many war memorials were built in towns and villages after 1918.', 'Almost every community lost men; many bodies were never brought home (the government did not repatriate the dead), so local memorials gave families a place to grieve and honour names.', '1 mark scale of loss; 1 mark no bodies/place to grieve [2]'),
        ('Explain why memorials can tell us about the time they were built as well as the war they remember.', 'Their design, words and who is included show the attitudes of the time – e.g. early memorials stressed sacrifice and glory, later ones stress peace, loss or previously forgotten groups such as colonial troops.', '1 mark memorial reflects attitudes; 1 mark example [2]'),
        ('Explain one reason why some people choose to wear a white poppy.', 'White poppies (from 1933) remember all victims of war, including civilians, and express a commitment to peace rather than appearing to honour the military alone.', '1 mark meaning; 1 mark reason [2]'),
        ('Explain how a historian might decide whether an event is significant.', 'By judging how far it caused change, how many people it affected, how long its effects lasted and whether it still matters or is remembered today.', '1 mark each criterion up to [3]'),
        ('Explain why the contribution of colonial soldiers has sometimes been overlooked in remembrance.', 'Memorials and histories often focused on European soldiers; records of African and Asian labourers and soldiers were poorer; some were not commemorated equally – a 2021 report found that the Imperial War Graves Commission had not commemorated many as individuals.', '1 mark reason; 1 mark example [2]'),
    ],
    'claims': [
        ('Remembrance Day is held on 11 November because the First World War Armistice began at 11 a.m. that day in 1918.', True, 'The two-minute silence marks “the eleventh hour of the eleventh day of the eleventh month”.'),
        ('War memorials only remember soldiers from Britain and France.', False, 'Memorials such as India Gate and the Menin Gate name soldiers from across the British Empire, and countries around the world have their own memorials.'),
        ('Memorials are neutral and do not present any interpretation of the past.', False, 'What a memorial shows, who it names and what words it uses reflect particular views of the war.'),
    ],
    'sources': [
        dict(prov='the inscription on a village war memorial in England, unveiled in 1921 (adapted)', kind='primary',
             text='To the glorious memory of the men of this parish who gave their lives for King and Country, 1914-1918. Their name liveth for evermore.',
             about='how communities remembered the First World War in the 1920s', infer='Communities in the 1920s remembered the dead as heroes who sacrificed themselves for a noble cause.',
             purpose='To honour the local dead and give families comfort and pride.',
             plus='it shows the attitudes of the community at the time the memorial was built', minus='it presents an official, positive view and hides the horror or doubts some survivors felt',
             missing='How the men died or what the families felt privately.', enq='how attitudes to war were shown in memorials'),
        dict(prov='a museum guide written in 2018 for visitors to a First World War exhibition', kind='secondary',
             text='Over a million Indian soldiers served overseas, and hundreds of thousands of labourers from China, Egypt and South Africa dug trenches and moved supplies. Their stories are now being told for the first time.',
             about='how remembrance of the First World War has changed', infer='Remembrance today increasingly includes groups, such as colonial soldiers and labourers, who were overlooked in the past.',
             purpose='To inform visitors and widen understanding of who took part in the war.',
             plus='it is based on modern research and records', minus='it is a short guide that cannot give detail and reflects the museum’s choices about what to highlight',
             missing='Personal accounts from the soldiers and labourers themselves.', enq='how and why remembrance of war has changed'),
    ],
    'essays': [
        ('war memorials tell us more about the people who built them than about the wars they remember',
         ['Their words, symbols and choice of names reflect the values of their time (e.g. “glorious sacrifice” in 1920s Britain).', 'Later memorials such as the Berlin Holocaust memorial (2005) reflect modern concerns.'],
         ['Lists of names give valuable evidence of the scale of loss in each community.', 'They record dates, battles and units.'],
         'They tell us about both, but are most valuable as evidence of how societies chose to remember.',
         ['inscriptions', 'names and numbers', 'changing attitudes']),
        ('it is still important to hold Remembrance ceremonies for the First World War now that no veterans are alive',
         ['Remembrance honours the dead and teaches young people the cost of war.', 'It now includes all conflicts and forgotten groups.'],
         ['Some argue it can glorify war or focus too much on one nation’s soldiers.', 'Other forms of learning, such as history lessons and museums, may be more effective.'],
         'Remembrance remains important if it is inclusive and encourages reflection on peace.',
         ['honouring the dead', 'learning from the past', 'inclusiveness', 'glorifying war']),
    ],
})


@c4e.add('C3', (2, 3, 4, 5), 'case')
def c4e_signif(r, D):
    ev = r.choice([('the first day of the Battle of the Somme (1916)', 'It caused about 57 000 British casualties in one day, affected communities across Britain (Pals battalions), changed tactics and is still remembered at Thiepval.'),
                   ('the Treaty of Versailles (1919)', 'It redrew the map of Europe, created lasting German resentment exploited by Hitler and is still debated as a cause of the Second World War.'),
                   ('the Holocaust (1941-45)', 'About 6 million Jews were murdered; it led to the Genocide Convention and the UDHR (1948) and is remembered on 27 January worldwide.'),
                   ('the atomic bombing of Hiroshima (1945)', 'It killed about 70 000-140 000 people, ended the war with Japan, began the nuclear age and is remembered at the Hiroshima Peace Memorial.'),
                   ('the Battle of Stalingrad (1942-43)', 'It cost over a million lives, turned the war on the Eastern Front and is remembered in Russia as a symbol of national survival.')])
    intro = f'A class is investigating the significance of {ev[0]}. One student uses these criteria: how many people were affected, how far it caused change, and whether it is still remembered today.'
    parts = [
        lambda r: ('Apply the criteria to explain why this event is significant.', ev[1], '1 mark each criterion applied with accurate detail [3]'),
        lambda r: ('Suggest one type of evidence the class could use to judge how the event is remembered today, and explain why.', 'Memorials, ceremonies, museum displays, school textbooks or media coverage on anniversaries, because they show what people choose to remember now.', '1 mark evidence; 1 mark reason [2]'),
        lambda r: ('Explain why significance can change over time.', 'New research, anniversaries, changing values and new groups telling their stories can make an event seem more or less important to later generations.', '1 mark reason; 1 mark development/example [2]'),
        lambda r: ('Explain why people in different countries might judge the significance of this event differently.', 'National experiences differ: a victory for one side is a defeat for another; some countries lost far more people; memory is shaped by national identity.', '1 mark idea; 1 mark example [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


CHAPTERS[4] = [c4a, c4b, c4c, c4d, c4e]


# ============================================================== CHAPTER 5: Plate tectonics and hazards

c5a = T('Structure of the Earth and plate boundaries', 'structure earth plate boundaries')
build(c5a, {
    'who': 'a geographer',
    'terms': [
        ('crust', 'the thin, solid outer layer of the Earth, 5-10 km thick under oceans and up to about 70 km under mountains'),
        ('mantle', 'the thick layer of hot, mostly solid but slowly flowing rock between the crust and the core, about 2900 km deep'),
        ('outer core', 'the layer of liquid iron and nickel surrounding the inner core'),
        ('inner core', 'the solid centre of the Earth, made of iron and nickel at temperatures of about 5000-6000 °C'),
        ('tectonic plate', 'a large, rigid section of the Earth’s crust and upper mantle (lithosphere) that moves slowly'),
        ('convection currents', 'circular movements in the mantle caused by heat from the core, which help move the plates'),
        ('subduction', 'the sinking of a denser oceanic plate beneath another plate at a destructive boundary'),
        ('constructive boundary', 'a plate boundary where plates move apart and new crust is formed from rising magma'),
        ('destructive boundary', 'a plate boundary where plates move towards each other and oceanic crust is destroyed by subduction'),
        ('conservative boundary', 'a plate boundary where plates slide past each other and crust is neither made nor destroyed'),
    ],
    'dates': [
        ('Alfred Wegener first put forward his theory of continental drift', 1912),
        ('scientists mapped the Mid-Atlantic Ridge in detail, supporting sea-floor spreading', 1953),
        ('the island of Surtsey began to form from a volcanic eruption off Iceland', 1963),
    ],
    'mcq': [
        ('Which is the correct order of the Earth’s layers from the surface to the centre?', 'Crust, mantle, outer core, inner core',
         ['Mantle, crust, inner core, outer core', 'Crust, outer core, mantle, inner core', 'Inner core, mantle, crust, outer core'], '[1]'),
        ('Which type of crust is denser and sinks at a destructive boundary?', 'Oceanic crust', ['Continental crust', 'Granite crust', 'Both sink equally'], 'Oceanic (basalt) is denser than continental (granite). [1]'),
        ('What type of plate boundary is the San Andreas Fault in California?', 'Conservative', ['Constructive', 'Destructive', 'Collision'], 'The Pacific and North American plates slide past each other. [1]'),
        ('Which landform is created where the Indian plate collides with the Eurasian plate?', 'The Himalayas (fold mountains)', ['The Mid-Atlantic Ridge', 'The Andes', 'The Hawaiian Islands'], 'Collision of two continental plates. [1]'),
        ('What happens at the Mid-Atlantic Ridge?', 'The North American and Eurasian plates move apart and new crust forms',
         ['Two plates collide to form mountains', 'Oceanic crust is subducted', 'Plates slide past with no volcanoes'], 'Constructive boundary; Iceland sits on it. [1]'),
        ('About how fast do tectonic plates move?', 'A few centimetres a year', ['A few metres a day', 'A few kilometres a year', 'They do not move'], 'Roughly 2-10 cm per year – about as fast as fingernails grow. [1]'),
        ('Where are most of the world’s active volcanoes found?', 'Around the Pacific “Ring of Fire”', ['In the middle of continents', 'At the North Pole', 'Along the equator only'], 'About 75% of active volcanoes. [1]'),
    ],
    'explain': [
        ('Explain why volcanoes form at destructive plate boundaries.', 'Denser oceanic plate subducts beneath the continental plate; as it sinks it melts (helped by water released) to form magma, which rises through cracks in the crust and erupts as volcanoes, e.g. the Andes.', '1 mark subduction; 1 mark melting to magma; 1 mark magma rises/example [3]'),
        ('Explain why earthquakes but not volcanoes occur at conservative boundaries.', 'Plates slide past each other and stick; pressure builds then is released suddenly as an earthquake; no crust is destroyed or created, so no magma rises.', '1 mark plates stick and release; 1 mark no magma [2]'),
        ('Describe the differences between oceanic and continental crust.', 'Oceanic: thinner (5-10 km), denser (basalt), younger, can be subducted. Continental: thicker (25-70 km), less dense (granite), older, is not subducted.', '1 mark each comparison point up to [3]'),
        ('Explain how convection currents in the mantle are thought to move tectonic plates.', 'Heat from the core makes mantle rock rise, spread beneath the plates and sink as it cools; this slow circular flow drags the plates along (helped by ridge push and slab pull).', '1 mark heating/rising; 1 mark cooling/sinking; 1 mark drags plates [3]'),
        ('Explain what evidence Wegener used to support continental drift.', 'The coastlines of South America and Africa fit together; matching fossils (e.g. Mesosaurus) and rock types are found on continents now separated by oceans; evidence of past climates such as glacial deposits in tropical areas.', '1 mark each piece of evidence up to [3]'),
        ('Explain why Iceland has volcanic eruptions.', 'It lies on the Mid-Atlantic Ridge, a constructive boundary where the Eurasian and North American plates move apart; magma rises to fill the gap, and a hotspot adds extra magma.', '1 mark constructive boundary; 1 mark magma rising [2]'),
    ],
    'claims': [
        ('The Earth’s mantle is a liquid ocean of lava.', False, 'The mantle is mostly solid rock that flows very slowly because it is so hot; only small parts melt to form magma.'),
        ('Continental crust is less dense than oceanic crust.', True, 'Continental crust is mainly granite, oceanic crust is basalt, so oceanic crust sinks at destructive boundaries.'),
        ('Earthquakes only happen at destructive plate boundaries.', False, 'Earthquakes occur at all types of plate boundary, and occasionally away from boundaries.'),
        ('At collision boundaries between two continental plates, fold mountains form.', True, 'Neither plate subducts easily, so the crust crumples upwards, e.g. the Himalayas.'),
    ],
    'essays': [
        ('constructive plate boundaries are less hazardous to people than destructive plate boundaries',
         ['Constructive boundaries usually produce gentle, effusive eruptions and smaller earthquakes.', 'Many lie under oceans away from people.'],
         ['Iceland’s Eyjafjallajökull (2010) ash cloud disrupted about 100 000 flights; Laki (1783) caused famine.', 'Hazard also depends on how many people live nearby and how vulnerable they are.'],
         'Generally true – destructive boundaries produce the most violent eruptions, largest earthquakes and tsunamis – but impacts depend on population and preparedness.',
         ['types of eruption', 'earthquake size', 'population density', 'Iceland']),
    ],
})


@c5a.add('C3', (1, 2, 3, 4), 'numerical')
def c5a_rate(r, D):
    pl = r.choice([('the North American and Eurasian plates at the Mid-Atlantic Ridge', 2.5, 'apart'), ('the Indian plate moving north into the Eurasian plate', 5, 'together'),
                   ('the Pacific plate sliding past the North American plate along the San Andreas Fault', 4, 'past each other'), ('the Nazca plate moving towards the South American plate', 7, 'together')])
    yrs = r.choice([10000, 100000, 1000000, 2000000, 5000000])
    km = pl[1] * yrs / 100000
    stem = f'Scientists measure that {pl[0]} move {pl[2]} at about {fmt(pl[1], 1)} cm per year.'
    if D == 1:
        opts, a = mcq(r, f'{fmt(km, 2)} km', [f'{fmt(km * 10, 2)} km', f'{fmt(km / 10, 3)} km', f'{fmt(km * 100, 1)} km', f'{fmt(pl[1] * yrs, 0)} km'])
        return {'stem': stem + f' How far would they move in {yrs:,} years?'.replace(',', ' '), 'options': opts, 'answer': a, 'key': f'{fmt(pl[1], 1)} × {yrs} = {fmt(pl[1] * yrs, 0)} cm = {fmt(km, 2)} km. [1]'}
    btype = {'apart': 'constructive', 'together': 'destructive (or collision)', 'past each other': 'conservative'}[pl[2]]
    parts = [
        lambda r: (f'Calculate how far they move in {yrs:,} years, in kilometres.'.replace(',', ' '), f'{fmt(km, 2)} km', f'{fmt(pl[1], 1)} × {yrs} cm ÷ 100 000 = {fmt(km, 2)} km [2]'),
        lambda r: ('Name the type of plate boundary.', cap(btype), '[1]'),
        lambda r: ('Describe one landform or hazard found at this type of boundary.', {'apart': 'Ocean ridges and gentle volcanic eruptions (e.g. Iceland).', 'together': 'Fold mountains (Himalayas, Andes), ocean trenches, explosive volcanoes and powerful earthquakes.', 'past each other': 'Strong, shallow earthquakes along faults, e.g. San Francisco 1906.'}[pl[2]], '1 mark landform/hazard; 1 mark example [2]'),
        lambda r: ('Explain what causes the plates to move.', 'Convection currents in the mantle, together with ridge push and slab pull.', '[2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


QUAKES = {
    'Nepal 2015': dict(date='25 April 2015', mag=7.8, deaths='about 9000', where='Gorkha district, about 80 km north-west of Kathmandu', plate='the Indian plate pushing north into the Eurasian plate (collision boundary)', income='a low-income country'),
    'Tōhoku, Japan 2011': dict(date='11 March 2011', mag=9.0, deaths='about 18 500 dead or missing, mostly from the tsunami', where='about 70 km off the north-east coast of Honshu', plate='the Pacific plate subducting beneath the plate under northern Japan (destructive boundary)', income='a high-income country'),
    'Haiti 2010': dict(date='12 January 2010', mag=7.0, deaths='estimates range from about 100 000 to over 220 000', where='about 25 km from the capital, Port-au-Prince', plate='the Caribbean and North American plates sliding past each other (conservative boundary)', income='a low-income country'),
    'Christchurch, New Zealand 2011': dict(date='22 February 2011', mag=6.2, deaths='185', where='about 10 km south-east of the city centre', plate='stresses near the boundary of the Pacific and Australian plates', income='a high-income country'),
    'Chile 2010': dict(date='27 February 2010', mag=8.8, deaths='about 525', where='off the coast of central Chile', plate='the Nazca plate subducting beneath the South American plate (destructive boundary)', income='an upper-middle-income country'),
}

c5b = T('Causes and effects of earthquakes and volcanic eruptions', 'causes effects earthquakes volcanic eruptions')
build(c5b, {
    'who': 'a geographer',
    'terms': [
        ('focus', 'the point underground where an earthquake starts (the hypocentre)'),
        ('epicentre', 'the point on the Earth’s surface directly above the focus of an earthquake'),
        ('seismic waves', 'waves of energy released by an earthquake that travel through the Earth'),
        ('magnitude', 'a measure of the energy released by an earthquake, measured on the moment magnitude scale'),
        ('primary effects', 'the immediate effects of a hazard, such as collapsed buildings and deaths caused directly by shaking or lava'),
        ('secondary effects', 'effects that result from the primary effects, such as fires, tsunamis, landslides, disease and economic losses'),
        ('tsunami', 'a series of large sea waves caused by the sudden movement of the sea floor, usually by an earthquake'),
        ('pyroclastic flow', 'a fast-moving cloud of very hot gas, ash and rock that flows down the side of a volcano'),
        ('lahar', 'a mudflow of volcanic ash and water that rushes down a volcano’s slopes and valleys'),
        ('liquefaction', 'when shaking makes waterlogged ground behave like a liquid, so buildings sink or tilt'),
    ],
    'dates': [
        ('Mount St Helens erupted in the USA', 1980),
        ('Mount Pinatubo erupted in the Philippines', 1991),
        ('the Indian Ocean tsunami struck 14 countries', 2004),
        ('an earthquake devastated Port-au-Prince in Haiti', 2010, 1),
        ('ash from Eyjafjallajökull in Iceland closed European airspace', 2010, 4),
        ('the Tōhoku earthquake and tsunami struck Japan', 2011, 3),
        ('the Gorkha earthquake struck Nepal', 2015),
    ],
    'mcq': [
        ('On the moment magnitude scale, an earthquake of magnitude 7 releases about how much more energy than one of magnitude 6?', 'About 32 times more', ['About 2 times more', 'About 10 times less', 'Exactly the same'], 'Each whole number = about 32× energy and 10× ground motion. [1]'),
        ('Which of these is a secondary effect of an earthquake?', 'A tsunami that floods coastal towns', ['Ground shaking', 'Buildings collapsing during the shaking', 'The fault moving'], 'Secondary effects follow from primary ones. [1]'),
        ('What caused most of the deaths in the 2011 Tōhoku disaster?', 'The tsunami', ['Volcanic ash', 'Lava flows', 'Building collapse in Tokyo'], 'Waves up to about 40 m high flooded the coast. [1]'),
        ('Which volcanic hazard is a mixture of ash and water flowing down valleys?', 'Lahar', ['Pyroclastic flow', 'Lava bomb', 'Ash cloud'], '[1]'),
        ('What was the magnitude of the earthquake that struck Nepal on 25 April 2015?', '7.8', ['5.8', '6.2', '9.1'], 'The Gorkha earthquake killed about 9000 people. [1]'),
        ('What was a major secondary effect of the Tōhoku earthquake in 2011?', 'A nuclear accident at the Fukushima Daiichi power plant', ['A volcanic eruption in Tokyo', 'A drought', 'A hurricane'], 'The tsunami knocked out cooling systems, causing meltdowns and evacuation of over 150 000 people. [1]'),
        ('Why did the eruption of Eyjafjallajökull in 2010 affect people across Europe?', 'Its ash cloud closed airspace, cancelling about 100 000 flights',
         ['Its lava flowed into France', 'It caused a tsunami in the Mediterranean', 'It caused an earthquake in London'], 'Ash can damage jet engines. [1]'),
    ],
    'explain': [
        ('Explain the difference between the focus and the epicentre of an earthquake.', 'The focus is the point underground where the rocks break and energy is released; the epicentre is the point on the surface directly above it, where shaking is usually strongest.', '1 mark each [2]'),
        ('Explain why shallow-focus earthquakes usually cause more damage than deep ones.', 'The seismic waves travel a shorter distance to the surface and lose less energy, so shaking at the surface is stronger.', '1 mark shorter distance; 1 mark stronger shaking [2]'),
        ('Explain how an earthquake at sea can cause a tsunami.', 'The sudden upward movement of the sea floor at a subduction zone displaces a huge volume of water, creating waves that travel across the ocean and grow taller in shallow water near the coast.', '1 mark sea floor displaced; 1 mark waves build in shallow water [2]'),
        ('Explain why volcanoes at destructive boundaries are more explosive than those at constructive boundaries.', 'Destructive boundary magma is thick (viscous, rich in silica) and gas-rich, so pressure builds until it explodes; constructive boundary magma is runny basalt, so gas escapes easily and lava flows gently.', '1 mark viscosity; 1 mark gas pressure; 1 mark contrast [3]'),
        ('Describe two primary and two secondary effects of the 2015 Nepal earthquake.', 'Primary: about 9000 deaths; hundreds of thousands of houses and historic buildings in Kathmandu destroyed. Secondary: landslides blocked roads and cut off villages; an avalanche on Mount Everest; loss of tourism income; a large aftershock on 12 May.', '1 mark each correct effect [4]'),
        ('Explain why the number of deaths from an earthquake does not depend only on its magnitude.', 'It also depends on depth, distance from cities, population density, building quality, time of day, preparedness and the speed of rescue; e.g. Haiti 2010 (magnitude 7.0) killed far more than Chile 2010 (8.8).', '1 mark factors; 1 mark example [2]'),
    ],
    'claims': [
        ('An earthquake of magnitude 8 is twice as powerful as one of magnitude 4.', False, 'The scale is logarithmic: each whole number is about 32 times more energy, so magnitude 8 releases about a million times more energy.'),
        ('Most deaths in earthquakes are caused by collapsing buildings rather than the ground shaking itself.', True, 'Shaking rarely kills directly; collapsing buildings, fires, landslides and tsunamis cause most deaths.'),
        ('Volcanic eruptions only affect people living right next to the volcano.', False, 'Ash clouds can disrupt air travel across continents (Eyjafjallajökull 2010) and large eruptions can cool global climate (Pinatubo 1991).'),
        ('A tsunami is a single giant wave.', False, 'A tsunami is a series of waves, and the first is not always the largest.'),
    ],
    'sources': [
        dict(prov='a newspaper report from Kathmandu, 26 April 2015 (adapted)', kind='primary',
             text='The nine-storey Dharahara tower, a symbol of the city, collapsed in seconds. Families slept in the open, afraid of aftershocks, while rescuers dug through the rubble of brick houses with their bare hands.',
             about='the immediate effects of the Nepal earthquake', infer='The earthquake destroyed historic and poorly built brick buildings; rescue equipment was lacking and people feared aftershocks.',
             purpose='To report the disaster quickly to readers in Nepal and around the world.',
             plus='it was written by a reporter in Kathmandu the day after the earthquake', minus='it focuses on the capital, where reporters were based, and early reports often get numbers wrong',
             missing='The effects in remote rural areas, where many villages were cut off by landslides.', enq='the effects of the 2015 Nepal earthquake'),
        dict(prov='a Japanese government report on the 2011 disaster, published in 2012 (adapted)', kind='primary',
             text='Most buildings withstood the shaking because of strict building codes. However, the tsunami exceeded the height of many sea walls, and over 90% of deaths were caused by drowning.',
             about='the effects of the Tōhoku earthquake and tsunami', infer='Building codes protected people from the shaking, but the tsunami was larger than defences were designed for and caused most deaths.',
             purpose='To review the disaster and improve future planning.',
             plus='it was produced by the government using official data from the whole affected area', minus='a government may present its own preparations positively and play down failures such as at Fukushima',
             missing='The nuclear accident at Fukushima Daiichi or the experiences of individual survivors.', enq='the effects of the 2011 Tōhoku disaster'),
    ],
    'essays': [
        ('secondary effects of earthquakes are more serious than primary effects',
         ['The Tōhoku tsunami (2011) caused over 90% of deaths and the Fukushima nuclear accident.', 'In Haiti (2010) a cholera outbreak later killed thousands; landslides cut off Nepali villages in 2015.'],
         ['In many earthquakes, such as Nepal 2015 and Haiti 2010, most deaths came from buildings collapsing during the shaking.', 'Primary effects destroy homes and infrastructure needed for recovery.'],
         'It depends on the event: for coastal subduction earthquakes secondary effects are often worse, for inland earthquakes primary effects usually dominate.',
         ['Tōhoku 2011', 'Nepal 2015', 'Haiti 2010', 'long-term economic effects']),
        ('volcanic eruptions are a greater hazard than earthquakes',
         ['Large eruptions can affect the whole world (Pinatubo 1991 cooled global temperatures).', 'Pyroclastic flows and lahars can destroy towns.'],
         ['Earthquakes strike without warning, whereas many eruptions can be predicted and people evacuated (Pinatubo).', 'Earthquakes and tsunamis have killed far more people in recent decades (Indian Ocean 2004, Haiti 2010).'],
         'Earthquakes are generally the greater hazard because they are harder to predict and kill more people.',
         ['prediction', 'number of deaths', 'global effects']),
    ],
})


@c5b.add('C3', (1, 2, 3, 4), 'numerical')
def c5b_mag(r, D):
    m1 = r.choice([5.0, 5.5, 6.0, 6.2, 6.5, 7.0])
    d = r.choice([1, 2, 3])
    m2 = m1 + d
    e = 32 ** d
    a = 10 ** d
    stem = f'Earthquake A has a magnitude of {fmt(m1, 1)} and earthquake B has a magnitude of {fmt(m2, 1)}. Each increase of 1 on the magnitude scale means about 10 times more ground movement and about 32 times more energy.'
    if D == 1:
        opts, ans = mcq(r, f'About {e:,} times'.replace(',', ' '), [f'About {d * 32} times', f'About {a:,} times'.replace(',', ' '), f'About {d} times', f'About {2 * d} times'])
        return {'stem': stem + ' About how many times more energy does B release than A?', 'options': opts, 'answer': ans, 'key': f'32^{d} = {e}. [1]'}
    parts = [
        lambda r: ('Calculate how many times more energy earthquake B releases.', f'about {e:,} times'.replace(',', ' '), f'32^{d} = {e} [2]'),
        lambda r: ('Calculate how many times greater the ground movement is in B.', f'{a:,} times'.replace(',', ' '), f'10^{d} [1]'),
        lambda r: ('Explain why earthquake A could still cause more deaths than earthquake B.', 'If A is shallow, close to a densely populated city with poorly built buildings and little preparation, while B is deep, remote or in a well-prepared country.', '1 mark each factor up to [3]'),
        lambda r: ('Name one instrument used to measure earthquakes.', 'A seismometer (seismograph).', '[1]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


@c5b.add('C3', (2, 3, 4, 5), 'case')
def c5b_case(r, D):
    name = r.choice(list(QUAKES))
    q = QUAKES[name]
    intro = f'Case study: {name}. On {q["date"]} an earthquake of magnitude {fmt(q["mag"], 1)} struck {q["where"]}. It was caused by {q["plate"]}. Deaths: {q["deaths"]}.'
    eff = {'Nepal 2015': 'Hundreds of thousands of homes and historic temples destroyed; landslides blocked roads; avalanche on Everest; tourism collapsed; damage of about a third of GDP.',
           'Tōhoku, Japan 2011': 'Tsunami waves up to about 40 m; towns such as Minamisanriku and Rikuzentakata destroyed; Fukushima nuclear meltdowns; over 150 000 evacuated; the costliest natural disaster recorded.',
           'Haiti 2010': 'About 1.5 million people made homeless; the presidential palace, hospitals and the port destroyed; a cholera outbreak later in 2010.',
           'Christchurch, New Zealand 2011': 'Collapse of two office buildings caused most deaths; liquefaction damaged homes in eastern suburbs; the cathedral spire fell; the city centre was closed for months.',
           'Chile 2010': 'A tsunami struck coastal towns; hundreds of thousands of homes damaged; roads and bridges damaged, but strict building codes limited deaths.'}[name]
    parts = [
        lambda r: ('Describe the plate movement that caused this earthquake.', cap(q['plate']) + '; stress built up and was released suddenly.', '1 mark plates/boundary; 1 mark sudden release [2]'),
        lambda r: ('Describe the effects of the earthquake.', eff, '1 mark each accurate effect up to [3]'),
        lambda r: ('Classify one of the effects you described as primary or secondary, and explain your choice.', 'E.g. building collapse is primary because it was caused directly by shaking; landslides, tsunami, disease or loss of income are secondary because they followed from the shaking.', '1 mark classification; 1 mark reason [2]'),
        lambda r: (f'Explain how the country’s level of development (it was {q["income"]}) affected the impact.', 'Higher-income countries have stricter building codes, warning systems, trained emergency services and money to rebuild, which reduce deaths; lower-income countries have more poorly built homes and fewer resources, so deaths are higher and recovery slower.', '1 mark link to development; 1 mark applied to this case [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


c5c = T('Why people live in hazardous areas and how risk is reduced', 'people live hazardous areas risk reduced')
build(c5c, {
    'who': 'a geographer',
    'terms': [
        ('hazard', 'a natural event, such as an earthquake or eruption, that threatens people and property'),
        ('risk', 'the chance of a hazard causing loss of life or damage, which increases with vulnerability'),
        ('vulnerability', 'how likely people are to be harmed by a hazard, depending on factors such as poverty and building quality'),
        ('geothermal energy', 'heat energy from rocks below the Earth’s surface, used to heat homes and generate electricity'),
        ('hazard map', 'a map showing areas at greatest risk from a hazard, used to plan land use and evacuation routes'),
        ('base isolator', 'a flexible pad or spring placed under a building to absorb earthquake shaking'),
        ('monitoring', 'using instruments such as seismometers, tiltmeters and gas sensors to watch for signs of a hazard'),
        ('evacuation', 'moving people away from a dangerous area before or during a hazard'),
    ],
    'mcq': [
        ('Why do many farmers live on the slopes of volcanoes such as Mount Etna?', 'Volcanic soils are very fertile', ['Volcanoes are never dangerous', 'Land is always flat there', 'Rainfall is always low'], 'Weathered volcanic ash and lava are rich in minerals. [1]'),
        ('Which method helps scientists predict a volcanic eruption?', 'Measuring changes in the shape of the volcano with tiltmeters', ['Counting tourists', 'Measuring rainfall in the capital', 'Watching animal migrations only'], 'Swelling, small earthquakes and gas emissions often come before eruptions. [1]'),
        ('Which design feature helps a building survive an earthquake?', 'Rubber shock absorbers (base isolators) in its foundations', ['Heavy concrete roofs', 'Large glass windows', 'Unreinforced brick walls'], 'Base isolators let the ground move beneath the building. [1]'),
        ('How does Iceland benefit from living on a plate boundary?', 'Geothermal energy heats about 90% of homes', ['It has no earthquakes', 'It exports lava', 'It has a tropical climate'], 'Geothermal power also generates about a quarter or more of its electricity. [1]'),
        ('Why does Japan hold earthquake drills on 1 September each year?', 'It is the anniversary of the 1923 Great Kantō earthquake, and drills prepare people to react quickly',
         ['It is the start of the school holidays', 'Earthquakes only happen in September', 'It is Japan’s national day'], 'Disaster Prevention Day. [1]'),
    ],
    'explain': [
        ('Explain two reasons why people continue to live near active volcanoes.', 'Fertile soils for farming; jobs in tourism and geothermal energy; minerals; family ties and a sense of home; eruptions are infrequent so people think the risk is low; poorer people may have nowhere else to go.', '2 marks each explained reason [4]'),
        ('Explain how earthquake-resistant buildings reduce risk.', 'Steel frames and cross-bracing let buildings sway without collapsing; base isolators absorb shaking; counterweights reduce movement in tall buildings; shatterproof glass and automatic gas shut-offs reduce injuries and fires.', '1 mark each explained feature up to [3]'),
        ('Explain why earthquakes are much harder to predict than volcanic eruptions.', 'Volcanoes give warning signs such as swelling, small earthquakes and gas emissions that can be monitored; stress building on a fault cannot be measured precisely, so scientists can only give probabilities.', '1 mark volcano warning signs; 1 mark earthquakes no reliable signs [2]'),
        ('Explain how education and preparation can reduce deaths from hazards.', 'Drills teach people to “drop, cover and hold on” or evacuate to high ground after a tsunami warning; emergency kits and family plans help people survive until help arrives.', '1 mark action; 1 mark how it saves lives [2]'),
        ('Explain how hazard mapping can reduce risk.', 'It shows which areas are most dangerous (e.g. lahar paths, liquefaction zones), so governments can stop building there, plan evacuation routes and place emergency services.', '1 mark identifies danger zones; 1 mark use in planning [2]'),
    ],
    'claims': [
        ('People only live near volcanoes because they do not know about the danger.', False, 'Many know the risks but stay for fertile land, jobs, geothermal energy and family ties, or because they cannot afford to move.'),
        ('Scientists can predict exactly when an earthquake will happen.', False, 'They can identify areas at risk and give probabilities, but not the exact time.'),
        ('Monitoring helped save thousands of lives when Mount Pinatubo erupted in 1991.', True, 'Scientists predicted the eruption and over 60 000 people were evacuated.'),
        ('Earthquake-resistant buildings are equally affordable everywhere.', False, 'They cost more, so poorer countries and families often cannot afford them, although cheap methods (e.g. reinforced bamboo or tyre foundations) exist.'),
    ],
    'essays': [
        ('the benefits of living in hazardous areas outweigh the risks',
         ['Fertile volcanic soils (Java, Etna), geothermal energy (Iceland), tourism and jobs in big cities such as Tokyo and San Francisco.', 'Large hazards are infrequent and monitoring reduces danger.'],
         ['Major disasters can kill thousands and destroy livelihoods, e.g. Nepal 2015, Haiti 2010.', 'Poorer people often live there because they have no choice, not because of benefits.'],
         'For most people most of the time benefits outweigh risks, especially where risk is managed well, but for the poorest the risks are much greater.',
         ['farming', 'energy and tourism', 'poverty and choice', 'risk management']),
        ('prediction is the most effective way of reducing the impact of tectonic hazards',
         ['Monitoring allowed the Pinatubo evacuation (1991); tsunami warnings give time to reach high ground.'],
         ['Earthquakes cannot be predicted precisely, so protection (building design) saves more lives.', 'Planning – hazard maps, drills, land-use rules – reduces vulnerability.', 'Warnings only help if people receive them and know what to do.'],
         'Prediction is vital for volcanoes and tsunamis, but protection and planning matter more for earthquakes.',
         ['monitoring volcanoes', 'building design', 'education and drills', 'warning systems']),
    ],
})


@c5c.add('C3', (2, 3, 4, 5), 'numerical')
def c5c_risk(r, D):
    a, b = r.sample(['Town A', 'Town B', 'Town C', 'Village D', 'City E'], 2)
    ha, hb = r.randint(5, 9), r.randint(5, 9)
    va, vb = r.randint(3, 9), r.randint(3, 9)
    ca, cb = r.choice([1, 2, 3, 4]), r.choice([1, 2, 3, 4])
    ra, rb = round(ha * va / ca, 1), round(hb * vb / cb, 1)
    if ra == rb:
        return None
    hi = a if ra > rb else b
    stem = (f'A geographer scores two places at risk from earthquakes using the formula risk = hazard × vulnerability ÷ capacity to cope (all scores out of 10 except capacity, out of 4). '
            f'{a}: hazard {ha}, vulnerability {va}, capacity {ca}. {b}: hazard {hb}, vulnerability {vb}, capacity {cb}.')
    parts = [
        lambda r: (f'Calculate the risk score for {a}.', fmt(ra, 1), f'{ha} × {va} ÷ {ca} = {fmt(ra, 1)} [1]'),
        lambda r: (f'Calculate the risk score for {b}.', fmt(rb, 1), f'{hb} × {vb} ÷ {cb} = {fmt(rb, 1)} [1]'),
        lambda r: ('State which place is at greater risk.', f'{hi} ({fmt(max(ra, rb), 1)} compared with {fmt(min(ra, rb), 1)})', '[1]'),
        lambda r: ('Suggest two ways to increase a place’s capacity to cope.', 'Train emergency services, build earthquake-resistant hospitals, set up warning systems, hold drills, store emergency supplies.', '1 mark each [2]'),
        lambda r: ('Explain why reducing vulnerability may be more realistic than reducing the hazard.', 'People cannot stop earthquakes happening, but they can improve buildings, reduce poverty and plan land use so fewer people are harmed.', '1 mark hazard cannot be controlled; 1 mark vulnerability can be reduced [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c5c.fixed('C3', (2, 3, 4), [
    ('A family farms on the lower slopes of Mount Merapi in Java, Indonesia, one of the world’s most active volcanoes. Suggest two reasons why the family stays and two ways their risk could be reduced.',
     'Reasons: fertile volcanic soil gives good harvests; their land, home and community are there and they may not be able to afford land elsewhere. Reducing risk: monitoring and warning systems with evacuation plans; hazard maps showing lahar and pyroclastic flow paths; evacuation shelters and drills.',
     '1 mark each reason, 1 mark each method [4]'),
    ('Tokyo has over 35 million people in its metropolitan area and lies in one of the most earthquake-prone regions on Earth. Explain two reasons why the city continues to grow despite the risk.',
     'It is Japan’s capital and economic centre with many jobs and services; Japan’s strict building codes, warning systems and drills make people feel the risk is managed; large earthquakes are infrequent.',
     '2 marks each explained reason [4]'),
    ('Iceland lies on the Mid-Atlantic Ridge. Using Iceland as an example, explain how living on a plate boundary can bring economic benefits.',
     'Geothermal power provides cheap electricity and heats about 90% of homes; this attracts industries such as aluminium smelting; volcanoes, geysers and hot springs (e.g. the Blue Lagoon) attract tourists.',
     '1 mark geothermal; 1 mark industry; 1 mark tourism [3]'),
], type='explain')
_markify(c5c, len(c5c.templates) - 3)


c5d = T('Comparing hazard responses in countries at different levels of development', 'comparing hazard responses countries different levels development')
build(c5d, {
    'who': 'a geographer',
    'terms': [
        ('immediate response', 'action taken in the hours and days after a disaster, such as search and rescue, medical care and emergency shelter'),
        ('long-term response', 'action taken in the months and years after a disaster, such as rebuilding homes and improving building codes'),
        ('aid', 'help given by governments, charities or international organisations, such as money, food, tents or expertise'),
        ('high-income country (HIC)', 'a country with a high average income per person, such as Japan or New Zealand'),
        ('low-income country (LIC)', 'a country with a low average income per person, such as Nepal or Haiti'),
        ('early warning system', 'technology that detects a hazard and alerts people in time to take action'),
        ('reconstruction', 'the rebuilding of homes, infrastructure and services after a disaster'),
    ],
    'mcq': [
        ('Which was an immediate response to the 2011 Tōhoku earthquake?', 'Bullet trains were stopped automatically and tsunami warnings were issued within minutes',
         ['Japan asked for no help from anyone', 'The government built new sea walls the next day', 'People were told to stay on the beaches'], 'About 100 000 Self-Defence Force troops were also deployed. [1]'),
        ('Why was the response to the 2015 Nepal earthquake slow in rural areas?', 'Landslides blocked mountain roads and many villages could only be reached by helicopter or on foot',
         ['There were no people living in rural Nepal', 'The earthquake did not affect rural areas', 'Aid agencies refused to help'], 'Mountain relief and the monsoon made access difficult. [1]'),
        ('Which statement about deaths from earthquakes is generally correct?', 'Low-income countries tend to suffer more deaths, while high-income countries suffer higher economic losses',
         ['High-income countries always suffer more deaths', 'Development makes no difference', 'Economic losses are always higher in low-income countries'], 'Better buildings save lives; more expensive property and infrastructure raise costs. [1]'),
        ('What was set up in Nepal in December 2015 to manage rebuilding?', 'The National Reconstruction Authority', ['The United Nations', 'The Pacific Tsunami Warning Center', 'The Red Cross'], 'Rebuilding was slow; many families lived in temporary shelters for years. [1]'),
    ],
    'explain': [
        ('Explain why the Tōhoku earthquake (magnitude 9.0) had a much higher economic cost than the Nepal earthquake (magnitude 7.8).', 'Japan is a high-income country with expensive buildings, infrastructure, ports, factories and a nuclear power plant in the affected area; the tsunami destroyed property worth far more, so costs (estimated at over US$200 billion) were much higher.', '1 mark value of property/infrastructure; 1 mark tsunami/nuclear damage [2]'),
        ('Explain two reasons why low-income countries often rely on international aid after a disaster.', 'They lack money to pay for rescue and rebuilding; they have fewer trained rescue teams, helicopters and heavy equipment; hospitals and roads may be destroyed.', '2 marks each [4]'),
        ('Explain why long-term responses are as important as immediate responses.', 'Immediate responses save lives, but long-term responses (rebuilding with better codes, restoring jobs and services, improving warnings) reduce the impact of the next disaster and help the economy recover.', '1 mark immediate saves lives; 1 mark long-term reduces future risk [2]'),
        ('Explain why the earthquake in Haiti (2010) killed so many more people than the stronger earthquake in Chile (2010).', 'Haiti is a low-income country: buildings in Port-au-Prince were poorly constructed and densely packed, building codes were not enforced, and emergency services were weak; Chile had strict building codes and experienced earthquake planning. Haiti’s epicentre was also very close to the capital and shallow.', '1 mark buildings/codes; 1 mark emergency capacity; 1 mark location/depth [3]'),
    ],
    'claims': [
        ('Earthquakes in high-income countries cause no deaths.', False, 'Even well-prepared countries suffer deaths, e.g. about 18 500 dead or missing in Japan in 2011 and 185 in Christchurch in 2011.'),
        ('International aid always reaches the people who need it most quickly.', False, 'Damaged roads, landslides, poor coordination and corruption can delay aid, as in rural Nepal in 2015.'),
        ('Strict building codes help explain why Chile’s magnitude 8.8 earthquake in 2010 killed far fewer people than Haiti’s magnitude 7.0 earthquake.', True, 'Chile’s buildings were designed to withstand shaking; Haiti’s were not.'),
    ],
    'essays': [
        ('a country’s level of development is the most important factor affecting the impact of an earthquake',
         ['Wealthier countries have building codes, warning systems and emergency services: Chile 2010 (8.8) about 525 deaths vs Haiti 2010 (7.0) over 100 000.', 'Wealth allows faster rebuilding.'],
         ['Physical factors matter: magnitude, depth, distance to cities and secondary hazards (the Tōhoku tsunami killed about 18 500 in a high-income country).', 'Time of day and population density matter.', 'Governance and preparation vary within the same income level.'],
         'Development is usually the most important factor in deaths, but physical factors can overwhelm even rich countries.',
         ['Haiti and Chile 2010', 'Japan 2011', 'Nepal 2015', 'physical factors']),
        ('international aid is the most important response to disasters in low-income countries',
         ['Aid provides money, rescue teams, medicine and shelter that local governments cannot supply, e.g. in Nepal 2015.'],
         ['Local people and communities carry out most rescues in the first hours.', 'Long-term reconstruction, governance and better building matter most for future disasters.', 'Aid can be slow, poorly coordinated or create dependency (Haiti after 2010).'],
         'Aid is vital in the short term, but local capacity and long-term reconstruction decide how well a country recovers.',
         ['immediate aid', 'local responses', 'long-term rebuilding']),
    ],
})


@c5d.add('C3', (1, 2, 3, 4, 5), 'case')
def c5d_table(r, D):
    a, b = r.sample([('Nepal 2015', 7.8, 9000, 'low income'), ('Haiti 2010', 7.0, 160000, 'low income'), ('Chile 2010', 8.8, 525, 'upper-middle income'),
                     ('Tōhoku, Japan 2011', 9.0, 18500, 'high income'), ('Christchurch 2011', 6.2, 185, 'high income')], 2)
    stem = (f'Compare two earthquakes. {a[0]}: magnitude {fmt(a[1], 1)}, about {a[2]:,} deaths, {a[3]} country. {b[0]}: magnitude {fmt(b[1], 1)}, about {b[2]:,} deaths, {b[3]} country. (Death figures are estimates.)').replace(',', ' ')
    if D == 1:
        more = a if a[2] > b[2] else b
        opts, ans = mcq(r, more[0], [a[0] if more is b else b[0], 'They had the same number of deaths', 'Neither caused any deaths'])
        return {'stem': stem + ' Which earthquake caused more deaths?', 'options': opts, 'answer': ans, 'key': f'{more[0]}: about {more[2]} deaths. [1]'}
    stronger = a if a[1] > b[1] else b
    deadlier = a if a[2] > b[2] else b
    ratio = max(a[2], b[2]) / min(a[2], b[2])
    parts = [
        lambda r: ('How many times more deaths did the deadlier earthquake cause? Give your answer to the nearest whole number.', f'{round(ratio)} times', f'{max(a[2], b[2])} ÷ {min(a[2], b[2])} [1]'),
        lambda r: ('Describe the relationship between magnitude and deaths shown by these two examples.', ('The stronger earthquake also caused more deaths here, but development and secondary effects also matter.' if stronger is deadlier else f'The stronger earthquake ({stronger[0]}) caused fewer deaths, so magnitude alone does not explain deaths.'), '1 mark relationship; 1 mark data [2]'),
        lambda r: ('Explain how the level of development helps to explain the difference in deaths.', 'Richer countries have stricter building codes, warning systems, trained emergency services and better hospitals; poorer countries have weaker buildings and fewer resources.', '1 mark each linked point up to [3]'),
        lambda r: ('Suggest one other factor, apart from magnitude and development, that affects deaths.', 'Depth of the focus, distance to a city, population density, time of day, or secondary hazards such as a tsunami.', '[1]'),
        lambda r: ('Suggest why the death figures should be used with caution.', 'They are estimates; counting is difficult in low-income or remote areas; some include people missing; different organisations give different totals.', '1 mark reason; 1 mark development [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


CHAPTERS[5] = [c5a, c5b, c5c, c5d]


# ============================================================== CHAPTER 6: Weather, climate and climate change

c6a = T('Elements of weather and how they are measured', 'elements weather measured')
build(c6a, {
    'who': 'a geographer',
    'terms': [
        ('weather', 'the day-to-day condition of the atmosphere at a particular place and time'),
        ('climate', 'the average weather conditions of a place, usually measured over 30 years or more'),
        ('precipitation', 'water falling from the atmosphere to the ground as rain, snow, sleet or hail'),
        ('air pressure', 'the weight of the air pressing down on the Earth’s surface, measured in millibars (hPa)'),
        ('humidity', 'the amount of water vapour in the air'),
        ('Stevenson screen', 'a white, louvred wooden box on legs that holds thermometers in the shade with air flowing through'),
        ('anemometer', 'an instrument with spinning cups that measures wind speed'),
        ('wind vane', 'an instrument that shows the direction from which the wind is blowing'),
        ('rain gauge', 'a container with a funnel used to collect and measure precipitation in millimetres'),
        ('okta', 'a unit for measuring cloud cover, in eighths of the sky covered'),
        ('barometer', 'an instrument used to measure air pressure'),
    ],
    'mcq': [
        ('Which instrument measures wind speed?', 'Anemometer', ['Barometer', 'Rain gauge', 'Hygrometer'], '[1]'),
        ('A wind blowing from the south-west towards the north-east is called', 'a south-westerly wind', ['a north-easterly wind', 'a westerly wind', 'a southerly wind'], 'Winds are named after the direction they come from. [1]'),
        ('Why is a Stevenson screen painted white?', 'To reflect the Sun’s heat so the thermometers measure air temperature, not direct sunshine',
         ['To make it easy to see in the dark', 'Because white paint is cheaper', 'To absorb more heat'], 'Louvres allow air to flow; it stands about 1.25 m above grass. [1]'),
        ('Cloud cover of 8 oktas means', 'the whole sky is covered by cloud', ['there are no clouds', 'half the sky is covered', 'it is raining heavily'], '0 oktas = clear; 8 oktas = overcast. [1]'),
        ('Falling air pressure usually means', 'cloudy, wet and windy weather is likely', ['clear, calm weather is likely', 'the temperature will be exactly 0 °C', 'there will be an earthquake'], 'Low pressure (depressions) brings rising air, cloud and rain. [1]'),
        ('Why should a rain gauge be placed away from buildings and trees?', 'So that they do not shelter it or drip extra water into it',
         ['So that it is closer to the sea', 'So that it gets more sunshine', 'So that animals can drink from it'], 'Siting must be open for accurate readings. [1]'),
        ('Average air pressure at sea level is about', '1013 millibars', ['101 millibars', '10 130 millibars', '13 millibars'], '[1]'),
    ],
    'explain': [
        ('Explain the difference between weather and climate.', 'Weather is the short-term state of the atmosphere (e.g. today’s rain and temperature); climate is the long-term average pattern of weather, usually over 30 years.', '1 mark each [2]'),
        ('Explain why a rain gauge is sunk partly into the ground.', 'To stop it being knocked over and to prevent splash from the ground or evaporation from heating, so readings are accurate.', '1 mark stability; 1 mark accuracy [2]'),
        ('Describe how to measure the maximum and minimum temperature for a day.', 'Use a maximum-minimum (Six’s) thermometer in a Stevenson screen; read the markers at the same time each day (e.g. 9 a.m.) and then reset them.', '1 mark instrument/siting; 1 mark reading and resetting [2]'),
        ('Explain why weather readings should be taken at the same time each day.', 'Temperature and other elements change through the day, so readings at different times would not be comparable; consistent timing makes the data reliable.', '1 mark variation through day; 1 mark comparability [2]'),
        ('Explain why it is useful to measure air pressure when forecasting weather.', 'Changes in pressure show approaching weather systems: falling pressure means a low (depression) with cloud, rain and wind; rising or high pressure (anticyclone) brings settled, dry weather.', '1 mark low; 1 mark high [2]'),
    ],
    'claims': [
        ('A north wind blows towards the north.', False, 'Winds are named after the direction they blow from, so a north wind blows from the north towards the south.'),
        ('Thermometers should be placed in direct sunlight to measure air temperature accurately.', False, 'They should be kept in the shade, in a Stevenson screen, so they measure air temperature not radiation from the Sun.'),
        ('Climate is the average weather over a long period, usually 30 years.', True, 'This is the standard period used by meteorologists to calculate climate averages.'),
        ('High air pressure is usually linked with settled, dry weather.', True, 'In an anticyclone air sinks, warming and drying, so clouds rarely form.'),
    ],
    'essays': [
        ('a school weather station can give data that is just as reliable as an official weather station',
         ['Simple instruments (rain gauge, max-min thermometer, anemometer) can be accurate if sited and read correctly.'],
         ['School sites are often sheltered by buildings, affecting wind and rain readings.', 'Readings may be missed at weekends and holidays or taken at different times.', 'Official stations use calibrated, automatic equipment and strict siting rules.'],
         'School data can be useful and fairly reliable, but rarely as reliable as official stations without careful siting and routine.',
         ['siting', 'equipment', 'consistency of readings']),
    ],
})


@c6a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6a_week(r, D):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    base = r.choice([8, 14, 20, 26, 30])
    mx = [base + r.randint(-3, 4) for _ in days]
    mn = [x - r.randint(4, 11) for x in mx]
    rain = [r.choice([0, 0, 0, 1, 2, 4, 6, 9, 12, 15]) for _ in days]
    pres = [r.randint(996, 1028) for _ in days]
    rng = [a - b for a, b in zip(mx, mn)]
    big = days[rng.index(max(rng))]
    tot = sum(rain)
    mean_max = round(sum(mx) / 7, 1)
    stem = ('A school weather station recorded this data for one week. Maximum temperature (°C): ' + ', '.join(f'{d} {x}' for d, x in zip(days, mx)) +
            '. Minimum temperature (°C): ' + ', '.join(f'{d} {x}' for d, x in zip(days, mn)) + '. Rainfall (mm): ' + ', '.join(f'{d} {x}' for d, x in zip(days, rain)) + '.')
    if D == 1:
        opts, a = mcq(r, f'{tot} mm', [f'{tot + 5} mm', f'{max(rain)} mm', f'{round(tot / 7, 1)} mm', f'{tot - 3} mm'])
        return {'stem': stem + ' What was the total rainfall for the week?', 'options': opts, 'answer': a, 'key': f'Sum = {tot} mm. [1]'}
    parts = [
        lambda r: ('Calculate the total rainfall for the week.', f'{tot} mm', f'sum = {tot} [1]'),
        lambda r: ('Identify the day with the largest daily temperature range and give the range.', f'{big}: {max(rng)} °C', f'max − min each day; largest {max(rng)} °C [2]'),
        lambda r: ('Calculate the mean maximum temperature to one decimal place.', f'{fmt(mean_max, 1)} °C', f'{sum(mx)} ÷ 7 [2]'),
        lambda r: ('Name the instrument used to measure each type of data in the table.', 'Maximum-minimum (Six’s) thermometer for temperatures; rain gauge for rainfall.', '1 mark each [2]'),
        lambda r: ('Suggest why days with heavy rain often have a small temperature range.', 'Cloud cover reduces heating by the Sun in the day and traps heat at night, so maximum and minimum temperatures are closer together.', '1 mark daytime; 1 mark night-time [2]'),
        lambda r: ('Describe two ways the students could make their readings more reliable.', 'Read the instruments at the same time every day; site them in the open away from buildings; keep the thermometer in a Stevenson screen; continue for longer than one week.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c6b = T('Factors affecting climate: latitude, altitude, distance from sea and winds', 'factors affecting climate latitude altitude distance sea winds')
build(c6b, {
    'who': 'a geographer',
    'terms': [
        ('latitude', 'the distance of a place north or south of the equator, measured in degrees'),
        ('altitude', 'the height of land above sea level'),
        ('lapse rate', 'the rate at which temperature falls with height, on average about 6.5 °C for every 1000 m'),
        ('continentality', 'the effect of distance from the sea, giving inland places hotter summers, colder winters and a larger temperature range'),
        ('maritime climate', 'a climate influenced by the sea, with mild winters, cool summers and a small annual temperature range'),
        ('prevailing wind', 'the direction from which the wind most often blows at a place'),
        ('ocean current', 'a large-scale, permanent movement of seawater that carries warm or cold water around the world'),
        ('rain shadow', 'a dry area on the sheltered (leeward) side of mountains'),
        ('relief rainfall', 'rain formed when moist air is forced to rise over mountains, cools and condenses'),
    ],
    'mcq': [
        ('Why are places near the equator hotter than places near the poles?', 'The Sun’s rays strike at a higher angle, so their energy is concentrated on a smaller area',
         ['The equator is closer to the Sun', 'There is more wind at the equator', 'The equator has more mountains'], 'At high latitudes rays are spread over a larger area and pass through more atmosphere. [1]'),
        ('Which current keeps the coast of north-west Europe warmer than other places at the same latitude?', 'The North Atlantic Drift (Gulf Stream)', ['The Humboldt Current', 'The Benguela Current', 'The Labrador Current'], '[1]'),
        ('Why do inland places have a larger annual temperature range than coastal places?', 'Land heats up and cools down faster than the sea',
         ['The sea heats up faster than land', 'Inland places are closer to the Sun', 'Inland places always have more rain'], 'The sea stores heat and moderates coastal climates. [1]'),
        ('Why is the leeward side of a mountain range often dry?', 'Air has lost most of its moisture on the windward side and warms as it descends',
         ['It is always closer to the sea', 'It faces the prevailing wind', 'Mountains create rain on both sides equally'], 'This is the rain shadow effect. [1]'),
        ('The cold Humboldt Current off the coast of Peru and Chile helps to explain', 'the very dry Atacama Desert', ['the rainforest of the Amazon', 'the monsoon in India', 'the mild winters of the UK'], 'Cold water cools the air, so little evaporation and rain. [1]'),
        ('If a town at sea level is 24 °C, about what temperature would you expect at the top of a nearby 2000 m mountain?', 'About 11 °C', ['About 22 °C', 'About 4 °C', 'About 37 °C'], '24 − (6.5 × 2) = 11 °C. [1]'),
    ],
    'explain': [
        ('Explain why temperature decreases with altitude.', 'Air is heated mainly from the ground; higher up the air is thinner (lower pressure), holds less heat and is further from the heated surface, so it is colder – about 6.5 °C per 1000 m.', '1 mark heated from ground; 1 mark thinner air; 1 mark rate [3]'),
        ('Explain why coastal areas have milder winters than inland areas at the same latitude.', 'The sea heats and cools more slowly than land and stores heat from the summer; in winter it releases this heat, warming coastal air.', '1 mark slow heating/cooling; 1 mark releases heat in winter [2]'),
        ('Explain how prevailing winds affect the climate of a place.', 'Winds from the sea bring moist air, causing rain and mild temperatures; winds from the land are dry and bring more extreme temperatures, e.g. westerly winds from the Atlantic give the UK a wet, mild climate.', '1 mark sea vs land winds; 1 mark example [2]'),
        ('Explain how relief rainfall forms and why it leads to a rain shadow.', 'Moist air is forced to rise over mountains, cools, condenses and forms clouds and rain on the windward side; descending air on the leeward side warms and is dry, creating a rain shadow.', '1 mark rising/cooling; 1 mark condensation/rain; 1 mark leeward dry [3]'),
        ('Explain how ocean currents influence the climate of nearby coasts.', 'Warm currents (e.g. North Atlantic Drift) warm the air above them, giving milder winters and more rain; cold currents (e.g. Humboldt) cool the air, giving cooler, drier conditions.', '1 mark warm; 1 mark cold [2]'),
    ],
    'claims': [
        ('The equator is hotter because it is closer to the Sun.', False, 'The difference in distance is tiny; the equator is hotter because the Sun’s rays are more direct and concentrated.'),
        ('Mountains near the equator can have snow all year round.', True, 'Temperature falls about 6.5 °C per 1000 m, so peaks such as Kilimanjaro (5895 m) are cold enough for glaciers.'),
        ('Places far from the sea have a smaller annual temperature range.', False, 'Continental places have a larger range because land heats and cools quickly.'),
        ('The UK has mild winters partly because of the North Atlantic Drift.', True, 'This warm current carries heat from the Gulf of Mexico across the Atlantic.'),
    ],
    'essays': [
        ('latitude is the most important factor affecting the climate of a place',
         ['Latitude controls the angle of the Sun’s rays and day length, which explains the main pattern of hot equator and cold poles.'],
         ['Altitude can override latitude: equatorial mountains such as Kilimanjaro have glaciers.', 'Distance from the sea and ocean currents explain why the UK is milder than places at the same latitude in Canada.', 'Prevailing winds and relief control rainfall.'],
         'Latitude sets the broad pattern, but local factors can be more important for a particular place.',
         ['altitude', 'distance from the sea', 'ocean currents', 'prevailing winds']),
    ],
})


@c6b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6b_lapse(r, D):
    t0 = r.choice([18, 20, 22, 24, 26, 28, 30])
    h = r.choice([500, 1000, 1500, 2000, 2400, 3000, 3600, 4000])
    t = round(t0 - 6.5 * h / 1000, 1)
    stem = f'A town at sea level has an average temperature of {t0} °C. A mountain village nearby is at {h} m. Assume temperature falls by 6.5 °C for every 1000 m.'
    if D == 1:
        opts, a = mcq(r, f'{fmt(t, 1)} °C', [f'{fmt(t0 - 6.5 * h / 100, 1)} °C', f'{fmt(t0 + 6.5 * h / 1000, 1)} °C', f'{fmt(t0 - h / 1000, 1)} °C', f'{t0} °C'])
        return {'stem': stem + ' What is the expected temperature in the village?', 'options': opts, 'answer': a, 'key': f'{t0} − 6.5 × {h}/1000 = {fmt(t, 1)} °C. [1]'}
    h2 = r.choice([x for x in (1000, 2000, 3000, 4500, 5000) if x != h])
    t2 = round(t0 - 6.5 * h2 / 1000, 1)
    parts = [
        lambda r: ('Calculate the expected temperature in the village.', f'{fmt(t, 1)} °C', f'6.5 × {h / 1000:g} = {fmt(6.5 * h / 1000, 2)}; {t0} − {fmt(6.5 * h / 1000, 2)} = {fmt(t, 1)} °C [2]'),
        lambda r: (f'Calculate the temperature at a summit {h2} m high.', f'{fmt(t2, 1)} °C', f'{t0} − 6.5 × {h2 / 1000:g} = {fmt(t2, 1)} °C [2]'),
        lambda r: ('Explain why temperature decreases with height.', 'The air is heated from the ground; higher air is thinner and further from the warm surface, so it holds less heat.', '1 mark each [2]'),
        lambda r: ('Suggest one way the higher altitude affects farming in the village.', 'Shorter growing season and risk of frost, so farmers grow hardier crops (e.g. potatoes, barley) or keep animals instead of tropical crops.', '1 mark effect; 1 mark example [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c6b.add('C3', (2, 3, 4, 5), 'numerical')
def c6b_contin(r, D):
    cs, cw = r.choice([17, 18, 19]), r.choice([5, 6, 7, 8])
    isu, iw = cs + r.choice([4, 5, 6, 7]), cw - r.choice([8, 10, 12, 14])
    lat = r.choice([45, 48, 50, 52])
    stem = (f'Two places lie at about {lat}° N. Place P is on the west coast, facing prevailing westerly winds from the ocean: July average {cs} °C, January {cw} °C. '
            f'Place Q is 1500 km inland: July average {isu} °C, January {iw} °C.')
    rp, rq = cs - cw, isu - iw
    parts = [
        lambda r: ('Calculate the annual temperature range of P and of Q.', f'P {rp} °C; Q {rq} °C', f'P {cs} − {cw} = {rp}; Q {isu} − ({iw}) = {rq} [2]'),
        lambda r: ('Explain why Q has a larger range than P.', 'Q is far from the sea: land heats quickly in summer and cools quickly in winter (continentality); P is moderated by the sea, which heats and cools slowly, and by mild westerly winds from the ocean.', '1 mark land heats/cools quickly; 1 mark sea moderates P; 1 mark winds [3]'),
        lambda r: ('Suggest which place is likely to have more rainfall, and why.', 'P, because moist westerly winds from the ocean bring rain; by the time air reaches Q it has lost much of its moisture.', '1 mark P; 1 mark reason [2]'),
        lambda r: ('Name the type of climate P and Q are likely to have.', 'P: temperate maritime; Q: continental.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c6c = T('Reading climate graphs and describing climate zones', 'reading climate graphs describing climate zones')
build(c6c, {
    'who': 'a geographer',
    'terms': [
        ('climate zone', 'a large area of the world with a broadly similar climate, such as tropical, arid, temperate or polar'),
        ('annual temperature range', 'the difference between the highest and lowest monthly average temperatures in a year'),
        ('tropical rainforest climate', 'a climate that is hot and wet all year, with average temperatures about 27 °C and over 2000 mm of rain'),
        ('hot desert climate', 'a climate with less than 250 mm of rain a year, very hot days and often cold nights'),
        ('Mediterranean climate', 'a climate with hot, dry summers and mild, wet winters'),
        ('temperate maritime climate', 'a climate with mild winters, cool summers and rain spread through the year'),
        ('monsoon', 'a seasonal reversal of winds that brings a very wet season, as in South Asia from June to September'),
        ('polar climate', 'a very cold climate in which average temperatures stay below 10 °C even in the warmest month and precipitation is low'),
    ],
    'mcq': [
        ('On a climate graph, which feature shows that a place is in the southern hemisphere?', 'The warmest months are December, January and February',
         ['Rain falls in every month', 'The bars are taller than the line', 'The temperature never falls below 0 °C'], 'Seasons are reversed south of the equator. [1]'),
        ('Which climate has the smallest annual temperature range?', 'Equatorial (tropical rainforest)', ['Cold continental', 'Polar', 'Hot desert'], 'The Sun is high all year; range is often only 1-3 °C. [1]'),
        ('Which city has a tropical monsoon climate with very heavy rain from June to September?', 'Mumbai', ['Cairo', 'London', 'Moscow'], 'The south-west monsoon. [1]'),
        ('A place has less than 250 mm of rain a year and summer temperatures above 30 °C. What is its climate?', 'Hot desert', ['Tropical rainforest', 'Temperate maritime', 'Polar'], '[1]'),
        ('Which statement describes a Mediterranean climate?', 'Hot, dry summers and mild, wet winters', ['Hot and wet all year', 'Cold all year with little rain', 'Wet summers and dry winters with snow'], '[1]'),
    ],
    'explain': [
        ('Explain why tropical rainforest areas have heavy rain almost every afternoon.', 'Intense heating by the high Sun causes moist air to rise (convection), cool and condense, forming towering cumulonimbus clouds and heavy convectional rain.', '1 mark heating/rising; 1 mark condensation/rain [2]'),
        ('Explain why hot deserts have a very large difference between day and night temperatures.', 'Clear skies let strong sunshine heat the ground by day, and without cloud cover heat escapes quickly at night, so temperatures fall sharply.', '1 mark day heating; 1 mark night cooling with no cloud [2]'),
        ('Describe how to describe a climate graph fully.', 'State the highest and lowest temperatures and months, calculate the range, give the total rainfall, identify the wettest and driest months and any seasonal pattern, using figures.', '1 mark temperature; 1 mark rainfall; 1 mark use of figures [3]'),
        ('Explain why Mediterranean climates have dry summers.', 'In summer, high pressure (subtropical anticyclones) moves over the region, bringing sinking, dry air and clear skies; in winter it moves south and rain-bearing depressions arrive.', '1 mark high pressure in summer; 1 mark winter rain [2]'),
    ],
    'claims': [
        ('All deserts are hot all year round.', False, 'Many deserts have cold winters or cold nights, and some (e.g. Antarctica or the Gobi) are cold deserts; deserts are defined by low precipitation.'),
        ('The tallest bar on a climate graph shows the hottest month.', False, 'Bars usually show precipitation; temperature is shown by the line.'),
        ('In a monsoon climate most of the year’s rain falls in a few months.', True, 'For example, Mumbai receives most of its rain between June and September.'),
    ],
    'essays': [
        ('describing climates using broad zones is too simple to be useful',
         ['Local factors such as altitude, ocean currents and cities create big differences within zones.', 'Zone boundaries are gradual, not sharp lines.'],
         ['Zones show the main global patterns clearly and help compare places.', 'They link climate to vegetation and human activity (e.g. farming).'],
         'Zones are a useful starting point but must be combined with local data.',
         ['local factors', 'comparing places', 'links to vegetation']),
    ],
})


@c6c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6c_zone(r, D):
    zone, temps, prec, hemi, lat = climate(r)
    hi, lo, rng, tot, wet, mean = climate_stats(temps, prec)
    stem = f'Climate data for a station at about {lat}° {hemi}. ' + climate_text(temps, prec)
    names = list(ZONES)
    if D <= 2:
        opts, a = mcq(r, cap(zone), [cap(z) for z in names if z != zone])
        return {'stem': stem + ' Which climate zone does this station most likely have?', 'options': opts, 'answer': a,
                'key': f'{cap(zone)}: {ZONE_NOTES[zone]} (range {fmt(rng, 1)} °C, total {tot} mm). [1]', 'marks': 1}
    parts = [
        lambda r: ('Calculate the annual temperature range and the total annual precipitation.', f'{fmt(rng, 1)} °C; {tot} mm', f'{fmt(hi, 1)} − ({fmt(lo, 1)}) = {fmt(rng, 1)} [1]; total {tot} [1] [2]'),
        lambda r: ('Describe the climate shown, using figures.', f'Highest temperature {fmt(hi, 1)} °C, lowest {fmt(lo, 1)} °C; wettest month {wet} ({max(prec)} mm); total {tot} mm. Overall: {ZONE_NOTES[zone]}.', '1 mark temperature with figures; 1 mark precipitation with figures; 1 mark seasonal pattern [3]'),
        lambda r: ('Identify the climate zone and give two pieces of evidence from the data.', f'{cap(zone)}: {ZONE_NOTES[zone]}.', '1 mark zone; 1 mark each piece of evidence [3]'),
        lambda r: (f'Explain how the latitude of the station ({lat}° {hemi}) helps to explain its temperatures.', ('Near the equator the Sun is high in the sky all year, so temperatures are high with little seasonal change.' if lat < 10 else
                                                                                                        'At this latitude the angle of the Sun and day length change through the year, causing seasons; higher latitudes receive less concentrated energy.'), '1 mark Sun angle; 1 mark effect on seasons/range [2]'),
        lambda r: ('Calculate the mean annual temperature.', f'{fmt(mean, 1)} °C', 'sum of monthly values ÷ 12 [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c6c.add('C3', (2, 3, 4, 5), 'numerical')
def c6c_two(r, D):
    z1, z2 = r.sample(list(ZONES), 2)
    a = climate(r, z1)
    b = climate(r, z2)
    sa, sb = climate_stats(a[1], a[2]), climate_stats(b[1], b[2])
    stem = (f'Station X: ' + climate_text(a[1], a[2]) + ' Station Y: ' + climate_text(b[1], b[2]))
    parts = [
        lambda r: ('Compare the annual temperature ranges of X and Y.', f'X {fmt(sa[2], 1)} °C, Y {fmt(sb[2], 1)} °C, so {"X" if sa[2] > sb[2] else "Y"} has the larger range by {fmt(abs(sa[2] - sb[2]), 1)} °C.', '1 mark each range; 1 mark comparison [3]'),
        lambda r: ('Compare the total precipitation of X and Y.', f'X {sa[3]} mm, Y {sb[3]} mm; {"X" if sa[3] > sb[3] else "Y"} is wetter by {abs(sa[3] - sb[3])} mm.', '1 mark totals; 1 mark comparison [2]'),
        lambda r: ('Identify the climate zone of each station.', f'X: {z1}; Y: {z2}.', '1 mark each [2]'),
        lambda r: ('Suggest one way the climate of station X affects how people live there.', {'equatorial (tropical rainforest)': 'Crops can grow all year; houses built on stilts with steep roofs for heavy rain.', 'hot desert': 'Water is scarce, so irrigation and shade are needed; activities happen early or late in the day.',
                                                                                          'Mediterranean': 'Summer tourism and crops such as olives and grapes that survive dry summers.', 'temperate maritime': 'Grass grows well, supporting dairy farming; mild winters.',
                                                                                          'tropical monsoon': 'Farming (e.g. rice) depends on the monsoon rains; flooding risk in the wet season.', 'cold continental': 'Heating needed in very cold winters; short growing season.',
                                                                                          'polar (tundra)': 'Very few people; permafrost makes building difficult; hunting and fishing rather than farming.', 'Mediterranean (southern hemisphere)': 'Vineyards and fruit farming; summer drought and wildfire risk from December to February.'}[z1], '1 mark effect; 1 mark link to climate [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c6d = T('Causes of climate change and the enhanced greenhouse effect', 'causes climate change enhanced greenhouse effect')
build(c6d, {
    'who': 'a geographer',
    'terms': [
        ('greenhouse effect', 'the natural process by which gases in the atmosphere trap heat radiated from the Earth’s surface, keeping the planet warm'),
        ('enhanced greenhouse effect', 'the extra warming caused by human activities adding greenhouse gases to the atmosphere'),
        ('greenhouse gas', 'a gas, such as carbon dioxide, methane or nitrous oxide, that absorbs heat radiated from the Earth'),
        ('fossil fuels', 'fuels formed from the remains of ancient plants and animals – coal, oil and natural gas – that release carbon dioxide when burned'),
        ('deforestation', 'the large-scale cutting down of forests, which reduces the absorption of carbon dioxide'),
        ('carbon footprint', 'the total amount of greenhouse gases produced by a person, organisation or product'),
        ('Milankovitch cycles', 'long-term natural changes in the Earth’s orbit and tilt that affect how much solar energy it receives'),
        ('global warming', 'the long-term rise in the average temperature of the Earth’s surface'),
    ],
    'dates': [
        ('regular measurements of carbon dioxide began at Mauna Loa in Hawaii', 1958),
        ('the Intergovernmental Panel on Climate Change (IPCC) was set up', 1988),
        ('Mount Pinatubo’s eruption temporarily cooled global temperatures', 1991),
        ('the Kyoto Protocol was agreed', 1997),
        ('the Paris Agreement was adopted', 2015),
    ],
    'mcq': [
        ('Which human activity releases the most carbon dioxide?', 'Burning fossil fuels for energy and transport', ['Growing rice', 'Recycling paper', 'Planting trees'], '[1]'),
        ('Which source releases large amounts of methane?', 'Cattle farming and rice paddies', ['Wind turbines', 'Solar panels', 'Planting forests'], 'Methane is about 25-30 times more powerful than CO₂ over 100 years. [1]'),
        ('About what was the concentration of carbon dioxide in the atmosphere before the Industrial Revolution?', 'About 280 parts per million', ['About 28 ppm', 'About 2800 ppm', 'About 420 ppm'], 'It was over 420 ppm by 2023. [1]'),
        ('Without the natural greenhouse effect, the Earth’s average temperature would be about', '−18 °C', ['15 °C', '50 °C', '0 °C exactly'], 'The natural greenhouse effect raises it to about 15 °C. [1]'),
        ('Which is a natural cause of climate change?', 'Variations in the Earth’s orbit (Milankovitch cycles)', ['Burning coal', 'Deforestation', 'Driving cars'], 'Also changes in solar output and large volcanic eruptions. [1]'),
        ('How does deforestation contribute to climate change?', 'Fewer trees absorb carbon dioxide and burning or rotting trees release it', ['Trees produce carbon dioxide only', 'It increases rainfall everywhere', 'It cools the oceans'], '[1]'),
    ],
    'explain': [
        ('Explain how the greenhouse effect keeps the Earth warm.', 'Short-wave radiation from the Sun passes through the atmosphere and heats the surface; the Earth gives off long-wave (infrared) radiation; greenhouse gases absorb and re-emit some of this, trapping heat in the lower atmosphere.', '1 mark incoming short-wave; 1 mark outgoing long-wave; 1 mark trapped by gases [3]'),
        ('Explain the difference between the natural and the enhanced greenhouse effect.', 'The natural effect is caused by gases that have always been present and keeps Earth about 33 °C warmer; the enhanced effect is caused by extra gases from human activity, trapping more heat and causing global warming.', '1 mark each; 1 mark contrast [3]'),
        ('Explain two ways human activities have increased greenhouse gases since the Industrial Revolution.', 'Burning coal, oil and gas for electricity, industry and transport releases CO₂; deforestation removes carbon sinks; cattle farming, rice growing and landfill release methane; fertilisers release nitrous oxide.', '2 marks each explained activity [4]'),
        ('Explain how a large volcanic eruption can temporarily cool the climate.', 'It throws ash and sulphur dioxide high into the atmosphere, forming tiny droplets that reflect sunlight back into space; e.g. Pinatubo in 1991 cooled global temperatures by about 0.5 °C for around two years.', '1 mark aerosols reflect sunlight; 1 mark example [2]'),
        ('Explain why scientists are confident that recent warming is mainly caused by humans.', 'CO₂ levels have risen from about 280 ppm to over 420 ppm, matching fossil-fuel use; natural factors (solar output, orbit) cannot explain the rapid warming since 1950; climate models only match observations when human emissions are included.', '1 mark each line of evidence up to [3]'),
    ],
    'claims': [
        ('The greenhouse effect is entirely bad for life on Earth.', False, 'The natural greenhouse effect keeps Earth habitable (about 15 °C instead of about −18 °C); the problem is the enhanced effect.'),
        ('Carbon dioxide levels in the atmosphere are higher now than at any time in the last 800 000 years.', True, 'Ice cores show levels stayed below about 300 ppm over that period; they are now over 420 ppm.'),
        ('The hole in the ozone layer is the main cause of global warming.', False, 'Ozone depletion and global warming are different problems; warming is caused mainly by greenhouse gases such as CO₂.'),
        ('Climate has changed naturally in the past, so current change cannot be caused by humans.', False, 'Natural changes happened over thousands of years; the current rapid warming matches the rise in human emissions.'),
    ],
    'essays': [
        ('human activity is the main cause of climate change today',
         ['CO₂ has risen from about 280 ppm before industrialisation to over 420 ppm, from burning fossil fuels and deforestation.', 'Warming of about 1.1-1.2 °C since the late 19th century is faster than natural changes.'],
         ['Natural factors – Milankovitch cycles, solar variation and volcanic eruptions – have caused big changes in the past.', 'Natural variability (e.g. El Niño) causes short-term ups and downs.'],
         'Natural factors exist, but the evidence strongly shows that human activity is the main cause of current warming.',
         ['fossil fuels', 'deforestation', 'natural causes', 'evidence from data']),
    ],
})


@c6d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6d_co2(r, D):
    rows = [(1960, 317), (1970, 326), (1980, 339), (1990, 354), (2000, 370), (2010, 390), (2020, 414)]
    i, j = sorted(r.sample(range(len(rows)), 2))
    (y1, c1), (y2, c2) = rows[i], rows[j]
    rate = round((c2 - c1) / (y2 - y1), 2)
    stem = 'Annual average carbon dioxide concentration measured at Mauna Loa, Hawaii (parts per million): ' + ', '.join(f'{y}: {c}' for y, c in rows) + '.'
    if D == 1:
        opts, a = mcq(r, f'{c2 - c1} ppm', [f'{c2 + c1} ppm', f'{c2} ppm', f'{y2 - y1} ppm', f'{round((c2 - c1) / 2)} ppm'])
        return {'stem': stem + f' By how much did the concentration rise between {y1} and {y2}?', 'options': opts, 'answer': a, 'key': f'{c2} − {c1} = {c2 - c1} ppm. [1]'}
    r1 = (rows[1][1] - rows[0][1]) / 10
    r2 = (rows[-1][1] - rows[-2][1]) / 10
    parts = [
        lambda r: (f'Calculate the average rate of increase per year between {y1} and {y2}.', f'{fmt(rate, 2)} ppm per year', f'({c2} − {c1}) ÷ {y2 - y1} [2]'),
        lambda r: ('Describe the trend, including whether the rate of increase is changing.', f'A steady rise every decade; the rate has increased from about {fmt(r1, 1)} ppm a year in the 1960s to about {fmt(r2, 1)} ppm a year in 2010-2020.', '1 mark rising trend; 1 mark accelerating with figures [2]'),
        lambda r: ('Calculate the percentage increase compared with the pre-industrial level of about 280 ppm, using the 2020 value.', f'{round(100 * (414 - 280) / 280)}%', '(414 − 280) ÷ 280 × 100 [2]'),
        lambda r: ('Explain the main reasons for the increase.', 'Burning fossil fuels for power, industry and transport, and deforestation, especially as industrial economies such as China and India grew.', '1 mark fossil fuels; 1 mark deforestation/growth [2]'),
        lambda r: ('Suggest why the measurements are taken on Mauna Loa, Hawaii.', 'It is high and far from cities and large sources of pollution, so measurements represent well-mixed global air.', '1 mark remote; 1 mark representative [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c6e = T('Impacts of climate change and local and global responses', 'impacts climate change local global responses')
build(c6e, {
    'who': 'a geographer',
    'terms': [
        ('mitigation', 'actions that reduce the causes of climate change, such as cutting greenhouse gas emissions'),
        ('adaptation', 'actions that help people cope with the effects of climate change, such as building sea walls'),
        ('renewable energy', 'energy from sources that will not run out, such as solar, wind and hydroelectric power'),
        ('sea-level rise', 'the increase in average sea level caused by melting land ice and the expansion of warming seawater'),
        ('coral bleaching', 'when corals lose the algae that live in them, turning white, often because the sea is too warm'),
        ('Paris Agreement', 'the 2015 international agreement to keep global warming well below 2 °C and to try to limit it to 1.5 °C'),
        ('carbon capture and storage', 'technology that captures carbon dioxide from power stations or industry and stores it underground'),
        ('afforestation', 'planting trees where there was no forest before, to absorb carbon dioxide'),
    ],
    'dates': [
        ('the Kyoto Protocol set legally binding emission targets for developed countries', 1997),
        ('the Thames Barrier was completed to protect London from flooding', 1982),
        ('the Paris Agreement was adopted at COP21', 2015),
        ('the COP26 climate conference was held in Glasgow', 2021),
        ('the COP28 climate conference was held in Dubai', 2023),
    ],
    'mcq': [
        ('Which of these is an example of adaptation to climate change?', 'Building higher sea walls in the Maldives', ['Replacing coal power stations with wind farms', 'Taxing carbon emissions', 'Driving electric cars'], 'Adaptation copes with effects; the others are mitigation. [1]'),
        ('Which of these is an example of mitigation?', 'Generating electricity from solar panels instead of coal', ['Planting drought-resistant crops', 'Building flood barriers', 'Raising houses on stilts'], 'Mitigation cuts emissions. [1]'),
        ('What does the Paris Agreement (2015) aim to do?', 'Keep global warming well below 2 °C and try to limit it to 1.5 °C', ['Stop all use of cars by 2020', 'Ban all trade in oil immediately', 'Cool the Earth by 5 °C'], 'Countries set their own Nationally Determined Contributions. [1]'),
        ('Why are countries such as the Maldives and Tuvalu especially threatened by climate change?', 'Most of their land is only about 1 m above sea level', ['They have too many glaciers', 'They are far from the equator', 'They have no coastline'], 'About 80% of the Maldives is less than 1 m above sea level. [1]'),
        ('Which two processes cause sea levels to rise as the climate warms?', 'Melting land ice and the thermal expansion of seawater', ['Melting sea ice only and more rainfall', 'Stronger winds and tides', 'Earthquakes and volcanoes'], 'Floating sea ice melting adds little to sea level. [1]'),
    ],
    'explain': [
        ('Explain two environmental impacts of climate change.', 'Sea-level rise floods low-lying coasts; coral bleaching kills reefs; melting glaciers reduce water supplies; species migrate or become extinct; more frequent droughts, heatwaves and wildfires.', '2 marks each explained impact [4]'),
        ('Explain why climate change may affect people in poorer countries more than in richer countries.', 'Many depend on farming affected by drought and floods; they have less money for adaptation such as sea walls or irrigation; homes are less able to withstand extreme weather; low-lying deltas such as Bangladesh are densely populated.', '1 mark each explained point up to [3]'),
        ('Explain the difference between mitigation and adaptation, with an example of each.', 'Mitigation reduces the causes of climate change (e.g. wind power, reforestation); adaptation reduces the effects (e.g. sea walls, drought-resistant crops).', '1 mark each definition with example [2]'),
        ('Explain why international agreements on climate change are difficult to achieve.', 'Countries have different priorities: richer countries produced most past emissions while developing countries want to grow their economies; cutting emissions has costs; agreements depend on voluntary targets and some countries may not keep them.', '1 mark each reason up to [3]'),
        ('Explain how individuals and local communities can help to reduce climate change.', 'Walk, cycle or use public transport; insulate homes; use less energy; eat less meat; reduce waste and recycle; support local renewable energy schemes and tree planting.', '1 mark each explained action up to [3]'),
    ],
    'claims': [
        ('Melting sea ice in the Arctic is the main cause of sea-level rise.', False, 'Floating sea ice already displaces its own weight of water; melting land ice (glaciers, Greenland, Antarctica) and thermal expansion cause sea-level rise.'),
        ('Climate change may bring some benefits to some places, such as longer growing seasons in cold regions.', True, 'Some high-latitude areas may grow more crops, though overall impacts are mostly negative.'),
        ('Individual actions make no difference to climate change.', False, 'Individual choices add up and influence businesses and governments, though large-scale government and industry action is also essential.'),
        ('The Paris Agreement was signed by almost every country in the world.', True, 'Nearly all UN member states have joined it.'),
    ],
    'essays': [
        ('mitigation is more important than adaptation in responding to climate change',
         ['Cutting emissions tackles the cause; without mitigation warming will continue and adaptation will become impossible in some places.'],
         ['Some climate change is already happening, so adaptation is needed now to protect lives (sea walls, flood warnings, drought-resistant crops).', 'Poorer countries contributing few emissions need adaptation most.'],
         'Both are essential: mitigation limits future change while adaptation protects people from changes already happening.',
         ['renewable energy', 'sea defences', 'poorer countries', 'costs']),
        ('global agreements are more effective than local actions in tackling climate change',
         ['Agreements such as the Paris Agreement set targets for whole countries, covering huge emissions.'],
         ['Targets are voluntary and not always met.', 'Local actions (city cycle schemes, community solar, school projects) can act quickly and change behaviour.', 'Global targets are met only through many local actions.'],
         'Global agreements give direction, but they only work if local actions deliver them.',
         ['the Paris Agreement', 'national targets', 'local schemes', 'individual behaviour']),
    ],
})


@c6e.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c6e_sea(r, D):
    rate = r.choice([3.0, 3.3, 3.7, 4.0, 4.5])
    yrs = r.choice([20, 30, 50, 75])
    rise = rate * yrs
    isl = r.choice(['an island in the Maldives', 'a low-lying atoll in Tuvalu', 'a coastal village in Bangladesh', 'a coastal town in the Netherlands'])
    h = r.choice([50, 80, 100, 120, 150])
    stem = f'Global sea level is currently rising by about {fmt(rate, 1)} mm per year. The lowest homes on {isl} are about {h} cm above high tide.'
    if D == 1:
        opts, a = mcq(r, f'{fmt(rise / 10, 1)} cm', [f'{fmt(rise, 1)} cm', f'{fmt(rise / 100, 2)} cm', f'{fmt(rate * yrs * 10, 0)} cm', f'{fmt(rise / 5, 1)} cm'])
        return {'stem': stem + f' If this rate continues, how much will sea level rise in {yrs} years?', 'options': opts, 'answer': a, 'key': f'{fmt(rate, 1)} × {yrs} = {fmt(rise, 1)} mm = {fmt(rise / 10, 1)} cm. [1]'}
    left = h - rise / 10
    parts = [
        lambda r: (f'Calculate the rise in sea level in {yrs} years, in centimetres.', f'{fmt(rise / 10, 1)} cm', f'{fmt(rate, 1)} × {yrs} = {fmt(rise, 1)} mm ÷ 10 [2]'),
        lambda r: (f'Calculate how far above high tide the lowest homes would then be.', f'{fmt(left, 1)} cm', f'{h} − {fmt(rise / 10, 1)} [1]'),
        lambda r: ('Explain why the real risk may be greater than this calculation suggests.', 'The rate of rise is accelerating; storm surges and higher waves add to flooding; land in deltas may be sinking; salt water can contaminate fresh water and soils before flooding occurs.', '1 mark each reason up to [3]'),
        lambda r: ('Suggest two adaptation strategies for this place, and one disadvantage of each.', 'Sea walls (expensive, can increase erosion elsewhere); raising homes on stilts or building artificial islands (costly); planting mangroves (takes time to grow); managed relocation (loss of homes and culture).', '1 mark each strategy, 1 mark each disadvantage [4]'),
        lambda r: ('Explain why this is an issue of fairness between countries.', 'Low-lying and poorer countries have produced very small emissions but face the worst impacts, while richer countries produced most past emissions.', '1 mark low emissions/high impacts; 1 mark rich countries responsible [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c6e.add('C2', (1, 2, 3), 'mcq')
def c6e_sort(r, D):
    acts = [('installing solar panels on school roofs', 'mitigation'), ('planting mangroves to protect a coastline from storms', 'adaptation'), ('switching buses to electric power', 'mitigation'),
            ('building a flood barrier across a river', 'adaptation'), ('planting drought-resistant maize varieties', 'adaptation'), ('replacing a coal power station with a wind farm', 'mitigation'),
            ('raising houses on stilts in a flood-prone delta', 'adaptation'), ('introducing a carbon tax', 'mitigation'), ('installing early warning systems for heatwaves', 'adaptation'), ('insulating homes to use less heating fuel', 'mitigation')]
    a = r.choice(acts)
    opts, ans = mcq(r, cap(a[1]), ['Mitigation', 'Adaptation', 'Neither: it has no link to climate change', 'Neither: it increases emissions'])
    return {'stem': f'A city council plans to respond to climate change by {a[0]}. Is this mainly mitigation or adaptation?', 'options': opts, 'answer': ans,
            'key': f'{cap(a[1])}: ' + ('it reduces greenhouse gas emissions (tackles the cause).' if a[1] == 'mitigation' else 'it helps people cope with the effects of climate change.') + ' [1]'}


CHAPTERS[6] = [c6a, c6b, c6c, c6d, c6e]


# ============================================================== CHAPTER 7: Population, migration and urbanisation

c7a = T('Population distribution and density', 'population distribution density')
build(c7a, {
    'who': 'a geographer',
    'terms': [
        ('population distribution', 'the way people are spread out across an area'),
        ('population density', 'the number of people living in a given area, usually per square kilometre'),
        ('densely populated', 'an area with many people per square kilometre'),
        ('sparsely populated', 'an area with few people per square kilometre'),
        ('physical factors', 'natural features, such as relief, climate, soils and water supply, that affect where people live'),
        ('human factors', 'factors created by people, such as jobs, transport, services and political stability, that affect where people live'),
        ('census', 'an official count of the population, usually every ten years, recording details such as age and occupation'),
    ],
    'mcq': [
        ('How is population density calculated?', 'Total population ÷ area', ['Area ÷ total population', 'Births − deaths', 'Population × area'], 'Usually in people per km². [1]'),
        ('Which of these areas is sparsely populated?', 'The Sahara Desert', ['The Ganges delta in Bangladesh', 'The island of Java', 'The city-state of Singapore'], 'Extreme heat and lack of water. [1]'),
        ('Which is a physical factor that encourages high population density?', 'Flat, fertile land with a reliable water supply', ['Good motorways', 'Many factories', 'A large number of schools'], 'Physical = natural features. [1]'),
        ('Which is a human factor that encourages high population density?', 'Plenty of jobs in industry and services', ['A cold, polar climate', 'Steep, mountainous relief', 'Thin, infertile soils'], '[1]'),
        ('In 2022 the world’s population reached about', '8 billion', ['800 million', '80 billion', '2 billion'], 'The UN marked 8 billion on 15 November 2022. [1]'),
        ('Which continent has about 60% of the world’s population?', 'Asia', ['Africa', 'Europe', 'South America'], 'China and India each have about 1.4 billion people. [1]'),
        ('Which country overtook China in 2023 to become the most populous in the world, according to UN estimates?', 'India', ['Indonesia', 'USA', 'Nigeria'], '[1]'),
    ],
    'explain': [
        ('Explain why some areas of the world are sparsely populated, using two examples.', 'Extreme climates (Sahara too hot and dry, Antarctica and northern Canada too cold), high mountains (Himalayas) with steep slopes and thin soils, and dense forests (Amazon) make farming, building and transport difficult.', '1 mark each reason with example up to [4]'),
        ('Explain why river valleys and deltas are often densely populated.', 'Flat land and fertile alluvial soils are good for farming; rivers provide water and transport; e.g. the Ganges-Brahmaputra delta and the Nile valley.', '1 mark each factor; 1 mark example [3]'),
        ('Explain why population density figures for a whole country can be misleading.', 'They are averages that hide uneven distribution: e.g. Egypt’s average density is moderate, but about 95% of people live along the Nile and in its delta, while most of the country is empty desert.', '1 mark averages hide variation; 1 mark example [2]'),
        ('Explain how human factors can lead to high population density in areas with difficult physical conditions.', 'Jobs, investment and technology can overcome physical problems: e.g. Dubai and Las Vegas have grown in deserts using desalination, air-conditioning and trade or tourism jobs.', '1 mark human factor; 1 mark example [2]'),
    ],
    'claims': [
        ('Large countries always have the largest populations.', False, 'Russia and Canada are huge but sparsely populated, while Bangladesh is small but has about 170 million people.'),
        ('Singapore has one of the highest population densities in the world.', True, 'About 6 million people live on roughly 730 km², over 8000 people per km².'),
        ('Population distribution is affected only by physical factors.', False, 'Human factors such as jobs, transport, government policy and history are also important.'),
    ],
    'essays': [
        ('physical factors are more important than human factors in explaining population distribution',
         ['Most people live where climate, relief, soil and water allow farming: river valleys, coastal plains.', 'Deserts, mountains and polar areas remain almost empty.'],
         ['Human factors such as jobs, trade, transport and government decisions explain the growth of cities in difficult places (Dubai, Singapore).', 'In high-income countries people live where jobs and services are.'],
         'Physical factors explain the broad global pattern; human factors explain patterns at a local scale and in more developed economies.',
         ['climate and relief', 'water and soils', 'jobs and transport', 'technology']),
    ],
})


@c7a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c7a_density(r, D):
    regs = r.sample(['Northern District', 'Coastal Plain', 'Highland Region', 'River Delta', 'Capital Region', 'Desert Province', 'Forest Zone'], 3)
    data = []
    for nm in regs:
        area = r.choice([500, 800, 1200, 2500, 4000, 6000, 12000, 25000])
        dens = {'Capital Region': r.choice([2000, 3500, 5000]), 'River Delta': r.choice([600, 900, 1200]), 'Coastal Plain': r.choice([250, 400]),
                'Desert Province': r.choice([2, 4, 5]), 'Highland Region': r.choice([15, 25, 40]), 'Forest Zone': r.choice([3, 8, 10]), 'Northern District': r.choice([30, 60, 90])}[nm]
        data.append((nm, area * dens, area, dens))
    stem = 'The table shows population and area for three regions of a country. ' + ' '.join(f'{n}: population {p:,}, area {a:,} km².'.replace(',', ' ') for n, p, a, _ in data)
    hi = max(data, key=lambda x: x[3])
    lo = min(data, key=lambda x: x[3])
    n, p, a, d = r.choice(data)
    if D == 1:
        opts, ans = mcq(r, f'{d:,} people per km²'.replace(',', ' '), [f'{round(a / p, 4)} people per km²', f'{p + a:,} people per km²'.replace(',', ' '), f'{d * 10:,} people per km²'.replace(',', ' '), f'{max(1, d // 10)} people per km²'])
        return {'stem': stem + f' What is the population density of {n}?', 'options': opts, 'answer': ans, 'key': f'{p} ÷ {a} = {d} people per km². [1]'}
    parts = [
        lambda r: (f'Calculate the population density of {n}.', f'{d:,} people per km²'.replace(',', ' '), f'{p} ÷ {a} = {d} [2]'),
        lambda r: ('Identify the most densely and most sparsely populated regions.', f'Most dense: {hi[0]} ({hi[3]} per km²); most sparse: {lo[0]} ({lo[3]} per km²).', 'densities calculated for all three [2]'),
        lambda r: (f'Suggest two reasons why {lo[0]} is sparsely populated.', {'Desert Province': 'Very low rainfall and high temperatures make farming difficult; few jobs or services.', 'Highland Region': 'Steep slopes, thin soils and a colder climate make farming and building difficult; poor transport.',
                                                                              'Forest Zone': 'Dense vegetation, poor soils and few roads make settlement difficult.', 'Northern District': 'Cold climate or poor soils, few jobs and remoteness from the capital.',
                                                                              'Coastal Plain': 'Farming land with few large towns, or flood risk.', 'River Delta': 'Flood risk.', 'Capital Region': 'High land prices.'}[lo[0]], '1 mark each reason [2]'),
        lambda r: (f'Suggest two reasons why {hi[0]} is densely populated.', {'Capital Region': 'Many jobs in government, industry and services; good transport and services such as hospitals and universities.', 'River Delta': 'Flat, fertile alluvial soil and water for farming (e.g. rice); river transport.',
                                                                              'Coastal Plain': 'Flat land for farming and building; ports and trade.', 'Northern District': 'Mining or industrial jobs.', 'Highland Region': 'Mining or a cooler, healthier climate.', 'Forest Zone': 'Timber jobs.', 'Desert Province': 'Oil or an oasis.'}[hi[0]], '1 mark each reason [2]'),
        lambda r: ('Describe how you would show this data on a choropleth map.', 'Choose density categories (e.g. <10, 10-100, 100-1000, >1000 per km²), shade each region with darker colours for higher density and add a key.', '1 mark categories; 1 mark shading/key [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c7b = T('Population change: birth rate, death rate and population pyramids', 'population change birth rate death rate population pyramids')
build(c7b, {
    'who': 'a geographer',
    'terms': [
        ('birth rate', 'the number of live births per 1000 people per year'),
        ('death rate', 'the number of deaths per 1000 people per year'),
        ('natural increase', 'the birth rate minus the death rate, when births are greater than deaths'),
        ('population pyramid', 'a bar graph showing the age and sex structure of a population'),
        ('dependency ratio', 'the number of dependants (aged 0-14 and 65+) for every 100 people of working age (15-64)'),
        ('ageing population', 'a population with a rising proportion of older people, usually because of low birth rates and longer life expectancy'),
        ('life expectancy', 'the average number of years a person can expect to live'),
        ('infant mortality rate', 'the number of babies who die before their first birthday per 1000 live births'),
        ('Demographic Transition Model', 'a model showing how birth rates, death rates and population change as a country develops, in five stages'),
        ('fertility rate', 'the average number of children born to each woman'),
    ],
    'dates': [
        ('China introduced its one-child policy', 1980),
        ('China replaced the one-child policy with a two-child policy', 2016),
        ('China announced a three-child policy', 2021),
        ('the world population reached 8 billion according to the UN', 2022),
    ],
    'mcq': [
        ('A country has a birth rate of 30 per 1000 and a death rate of 10 per 1000. What is its rate of natural increase?', '2% per year', ['20% per year', '3% per year', '40% per year'], '(30 − 10) per 1000 = 20 per 1000 = 2%. [1]'),
        ('A population pyramid with a wide base and narrow top shows', 'a high birth rate and short life expectancy', ['an ageing population', 'a low birth rate', 'a falling population'], 'Typical of stage 2 countries such as Niger. [1]'),
        ('In which stage of the Demographic Transition Model is the death rate falling fast while the birth rate stays high?', 'Stage 2', ['Stage 1', 'Stage 4', 'Stage 5'], 'Rapid population growth. [1]'),
        ('Which country is an example of an ageing population with about 29% of people aged 65 or over?', 'Japan', ['Niger', 'Nigeria', 'Afghanistan'], '[1]'),
        ('Why does the birth rate usually fall as countries develop?', 'Women have more education and careers, contraception is available and fewer children die, so families choose fewer children',
         ['People stop marrying entirely', 'Governments ban children', 'Death rates rise'], '[1]'),
        ('In stage 5 of the Demographic Transition Model', 'the birth rate falls below the death rate and the population declines', ['both rates are high', 'the death rate falls rapidly', 'the population grows fastest'], 'E.g. Japan, Italy. [1]'),
    ],
    'explain': [
        ('Explain why death rates fall in stage 2 of the Demographic Transition Model.', 'Improvements in medical care, vaccinations, clean water, sanitation and food supply reduce deaths, especially of infants and children.', '1 mark each improvement up to [2]'),
        ('Explain two problems caused by an ageing population.', 'Higher costs of pensions and health care paid for by fewer workers; labour shortages; more need for care homes; possible slower economic growth.', '2 marks each explained problem [4]'),
        ('Explain two problems caused by a very youthful population.', 'Need for many more schools and teachers; shortage of jobs as young people reach working age; pressure on food, housing and health services for babies and mothers.', '2 marks each explained problem [4]'),
        ('Explain why birth rates remain high in some low-income countries.', 'Children work on farms and support parents in old age; high infant mortality means families have more children; limited access to contraception and education for girls; cultural and religious traditions.', '1 mark each reason up to [3]'),
        ('Explain what a population pyramid with a “bulge” in the 20-34 age group might show.', 'In-migration of young adult workers (e.g. to cities or Gulf states), or a past baby boom.', '1 mark migration; 1 mark alternative explanation [2]'),
    ],
    'claims': [
        ('A falling birth rate means the population must be falling.', False, 'The population still grows as long as the birth rate is higher than the death rate (and migration does not reduce it).'),
        ('High-income countries usually have low birth rates and low death rates.', True, 'They are in stages 4 or 5 of the Demographic Transition Model.'),
        ('China’s one-child policy had no effect on its population structure.', False, 'It contributed to an ageing population and a gender imbalance, with more young men than women.'),
        ('An ageing population can have benefits such as volunteering and spending by retired people.', True, 'Older people contribute through childcare for grandchildren, volunteering and the “grey” economy.'),
    ],
    'essays': [
        ('an ageing population causes more problems than a youthful population',
         ['Rising pension and health costs fall on a shrinking workforce (e.g. Japan).', 'Labour shortages may slow economic growth.'],
         ['Youthful populations (e.g. Niger) need many schools, jobs and health services and can lead to unemployment.', 'Older people contribute through volunteering, childcare and spending.', 'Ageing countries can attract migrant workers and use technology.'],
         'Both create challenges; youthful populations are often harder for poorer countries to manage, while ageing is a bigger issue for richer countries.',
         ['pensions and health care', 'jobs and education', 'migration', 'level of development']),
        ('the Demographic Transition Model is a useful way to understand population change in all countries',
         ['It describes the experience of many countries, such as the UK, well.', 'It helps predict future changes in birth and death rates.'],
         ['It was based on European experience; some countries moved through stages much faster or got “stuck”.', 'It ignores migration and government policies (e.g. China’s one-child policy).', 'Diseases such as HIV/AIDS raised death rates in some countries.'],
         'It is a useful general model but needs adapting for individual countries.',
         ['European experience', 'migration', 'government policy', 'disease']),
    ],
})


@c7b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c7b_rates(r, D):
    br = r.choice([8, 9, 10, 12, 14, 18, 22, 26, 30, 35, 40, 45])
    dr = r.choice([6, 7, 8, 9, 10, 11, 12, 14])
    ni = br - dr
    pc = ni / 10
    stage = 2 if br >= 30 and dr <= 14 else (3 if br >= 18 else (4 if ni >= 0 else 5))
    country = r.choice(['Country A', 'Country B', 'Country C', 'Country D'])
    stem = f'{country} has a birth rate of {br} per 1000 and a death rate of {dr} per 1000.'
    if D == 1:
        opts, a = mcq(r, f'{fmt(pc, 1)}%', [f'{ni}%', f'{fmt((br + dr) / 10, 1)}%', f'{fmt(pc * 10, 1)}%', f'{fmt(-pc, 1)}%'])
        return {'stem': stem + ' What is its rate of natural change as a percentage?', 'options': opts, 'answer': a, 'key': f'({br} − {dr}) ÷ 10 = {fmt(pc, 1)}%. [1]'}
    pop = r.choice([5, 10, 20, 40, 80])
    dbl = round(70 / pc) if pc > 0 else None
    parts = [
        lambda r: ('Calculate the natural change per 1000 people and as a percentage.', f'{ni:+d} per 1000; {fmt(pc, 1)}%', f'{br} − {dr} = {ni} per 1000 = {fmt(pc, 1)}% [2]'),
        lambda r: (f'The population is {pop} million. Calculate the change in population over one year from natural change alone.', f'{fmt(pop * 1e6 * ni / 1000, 0)} people', f'{pop} million × {ni}/1000 [2]'),
        lambda r: ('Suggest which stage of the Demographic Transition Model the country is in, and explain your choice.', f'Stage {stage}: ' + {2: 'high birth rate and lower death rate, so rapid growth.', 3: 'birth rate falling but still above death rate, so growth is slowing.', 4: 'low birth and death rates, so little growth.', 5: 'birth rate below death rate, so natural decrease.'}[stage], '1 mark stage; 1 mark use of both rates [2]'),
        lambda r: (('Use the “rule of 70” (doubling time ≈ 70 ÷ growth rate %) to estimate how long the population would take to double.', f'about {dbl} years', f'70 ÷ {fmt(pc, 1)} [2]') if dbl else
                   ('Explain what will happen to the population if these rates continue and there is no migration.', 'It will decline because deaths exceed births (natural decrease).', '1 mark decline; 1 mark reason [2]')),
        lambda r: ('Describe the shape of population pyramid you would expect for this country.', ('Wide base narrowing quickly with age (triangular): many children, few elderly.' if stage <= 2 else ('Base starting to narrow, wider middle.' if stage == 3 else 'Narrow base, wide middle and top: an ageing population.')), '1 mark shape; 1 mark link to rates [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c7b.add('C3', (2, 3, 4, 5), 'numerical')
def c7b_dep(r, D):
    young = r.choice([14, 16, 20, 25, 30, 38, 42, 48])
    old = r.choice([3, 4, 6, 10, 15, 20, 24, 29])
    if young + old >= 70:
        return None
    work = 100 - young - old
    ratio = round((young + old) / work * 100, 1)
    stem = f'A population pyramid shows that {young}% of a country’s people are aged 0-14, {work}% are aged 15-64 and {old}% are aged 65 and over.'
    kind = 'youthful' if young > 2 * old + 10 else ('ageing' if old >= 18 else 'balanced')
    parts = [
        lambda r: ('Calculate the dependency ratio.', fmt(ratio, 1), f'({young} + {old}) ÷ {work} × 100 = {fmt(ratio, 1)} [2]'),
        lambda r: ('State whether the population is youthful or ageing, and give evidence.', f'{cap(kind)}: {young}% young and {old}% elderly.', '1 mark judgement; 1 mark evidence [2]'),
        lambda r: ('Suggest two consequences of this dependency ratio for the government.', ('Must spend on schools and child health; must create many jobs for young people entering the workforce.' if kind == 'youthful' else ('Must fund pensions, health and social care for older people with fewer taxpayers; may encourage immigration or raise the retirement age.' if kind == 'ageing' else 'Spending is balanced between schools and pensions; a large workforce can boost the economy (a “demographic dividend”).')), '1 mark each [2]'),
        lambda r: ('Explain why the dependency ratio is only an approximate measure.', 'Many people over 65 still work and many aged 15-19 are in education, not working; some children work; it ignores unemployment.', '1 mark each point [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c7c = T('Migration: push and pull factors, impacts on source and host areas', 'migration push pull factors impacts source host areas')
build(c7c, {
    'who': 'a geographer',
    'terms': [
        ('migration', 'the movement of people from one place to another to live, either permanently or for a long period'),
        ('push factor', 'a reason that makes people want to leave a place, such as unemployment, conflict or drought'),
        ('pull factor', 'a reason that attracts people to a place, such as jobs, safety or better services'),
        ('refugee', 'a person forced to leave their country because of war, persecution or violence, protected under the 1951 Refugee Convention'),
        ('asylum seeker', 'a person who has left their country and asked for protection as a refugee in another country, but whose claim has not yet been decided'),
        ('economic migrant', 'a person who moves voluntarily to find work or a better standard of living'),
        ('remittances', 'money sent home by migrants to their families'),
        ('brain drain', 'the loss of skilled and educated people, such as doctors, from a country through emigration'),
        ('internal migration', 'movement of people within the same country, such as from rural to urban areas'),
        ('host country', 'the country to which migrants move'),
    ],
    'dates': [
        ('the ship Empire Windrush brought Caribbean migrants to Britain', 1948),
        ('the UN Refugee Convention was agreed', 1951),
        ('Poland and seven other central and eastern European countries joined the EU', 2004),
        ('the civil war in Syria began, causing millions to become refugees', 2011),
    ],
    'mcq': [
        ('Which of these is a push factor?', 'Civil war and violence', ['Well-paid jobs', 'Good schools and hospitals', 'Family members already living there'], 'Push factors make people leave. [1]'),
        ('Which of these is a pull factor?', 'Better-paid jobs', ['Drought and crop failure', 'Persecution', 'Lack of health care'], 'Pull factors attract people. [1]'),
        ('What is the main difference between a refugee and an economic migrant?', 'A refugee is forced to flee danger; an economic migrant chooses to move for work',
         ['Refugees always move within their own country', 'Economic migrants are always forced to move', 'There is no difference'], '[1]'),
        ('Which country hosted the largest number of Syrian refugees by the late 2010s?', 'Turkey', ['Germany', 'Brazil', 'Japan'], 'Over 3 million Syrian refugees. [1]'),
        ('Which is a benefit of emigration for the source country?', 'Remittances sent home by migrants', ['Loss of doctors and nurses', 'Fewer young workers', 'Separated families'], 'For countries such as Nepal remittances are a large share of GDP. [1]'),
        ('In Qatar and the UAE, about what share of residents are non-citizens, mainly migrant workers?', 'Around 85-90%', ['Around 5%', 'Around 25%', 'Around 50%'], 'Workers from South Asia, such as Nepal, India and Bangladesh. [1]'),
    ],
    'explain': [
        ('Explain two positive impacts of immigration on a host country.', 'Fills labour shortages (e.g. health care, construction, farming); migrants pay taxes and spend money; cultural diversity in food, music and ideas; young migrants balance an ageing population.', '2 marks each explained impact [4]'),
        ('Explain two negative impacts of emigration on a source country.', 'Loss of young, skilled workers (brain drain), e.g. doctors and nurses; an ageing population left behind; families separated; farms and businesses short of labour.', '2 marks each explained impact [4]'),
        ('Explain how remittances can help development in the source country.', 'Families use them for food, school fees, health care and better housing; money is invested in small businesses and land; it brings foreign currency into the economy.', '1 mark each use up to [3]'),
        ('Explain why many people migrate from rural to urban areas in lower-income countries.', 'Push: poverty, lack of jobs and services, drought, mechanisation of farming. Pull: jobs in factories and services, higher wages, better schools and hospitals, family already in the city.', '1 mark push; 1 mark pull; 1 mark development [3]'),
        ('Explain what is meant by an “intervening obstacle” in migration, with an example.', 'Something that makes migration difficult, such as distance, cost, borders and visa laws, language, or dangerous journeys across seas or deserts.', '1 mark meaning; 1 mark example [2]'),
    ],
    'claims': [
        ('Most migrants move from poorer countries to Europe and North America.', False, 'Many migrants move within their own region, e.g. from South Asia to the Gulf, or within Africa; most refugees are hosted by neighbouring countries.'),
        ('Remittances are a large part of the economy in some countries such as Nepal.', True, 'In Nepal remittances have been equal to about a fifth to a quarter of GDP.'),
        ('Migrants always take jobs away from local people.', False, 'Migrants often fill labour shortages and create jobs through spending and starting businesses.'),
        ('Refugees are people who choose to move for better wages.', False, 'Refugees are forced to flee war or persecution; people moving for better wages are economic migrants.'),
    ],
    'sources': [
        dict(prov='an interview with a Nepali construction worker in Doha, Qatar, recorded by a journalist in 2019 (adapted)', kind='primary',
             text='In my village there is no work except farming, and the land is small. Here I earn four times more. Every month I send money home for my children’s school, but I have not seen them for three years.',
             about='why people migrate from Nepal to the Gulf', infer='Migrants move for higher wages because of a lack of jobs at home; remittances pay for education, but families are separated for long periods.',
             purpose='To report on the lives of migrant workers for newspaper readers.',
             plus='it gives a first-hand account from a migrant worker', minus='it is one person’s experience, chosen by a journalist, and may not represent all migrants',
             missing='Working conditions and rights of migrant workers, or the total value of remittances to Nepal.', enq='the causes and impacts of labour migration'),
        dict(prov='a report by a refugee charity about Syrian refugees in Turkey, 2018 (adapted)', kind='primary',
             text='Most refugees live in towns and cities, not camps. Many children have missed years of school, and adults work in low-paid jobs, often without permits.',
             about='the experience of refugees in a host country', infer='Refugees face poverty, informal work and disrupted education even after reaching safety.',
             purpose='To raise awareness and possibly persuade governments and donors to provide more support.',
             plus='the charity works directly with refugees and collects evidence', minus='a charity may highlight problems to encourage donations',
             missing='Benefits refugees bring, or why they fled Syria.', enq='the impacts of forced migration'),
    ],
    'essays': [
        ('migration brings more benefits than problems to host countries',
         ['Migrants fill labour shortages, pay taxes and start businesses.', 'They add cultural diversity and help balance ageing populations.'],
         ['Rapid immigration can put pressure on housing, schools and health services in some areas.', 'Tensions and discrimination can arise; some migrant workers are exploited.'],
         'Overall the economic benefits are usually greater, though they depend on how well governments plan for and support migrants.',
         ['jobs and the economy', 'public services', 'culture and identity', 'ageing populations']),
        ('the source country loses more than it gains from emigration',
         ['Brain drain removes doctors, nurses and teachers; rural areas lose young workers; families are separated.'],
         ['Remittances raise incomes and pay for schools and health care (e.g. Nepal).', 'Returning migrants bring skills and savings.', 'Emigration reduces unemployment.'],
         'It depends on who leaves: losing skilled professionals is damaging, but remittances from labour migration can bring large benefits.',
         ['remittances', 'brain drain', 'unemployment', 'families']),
    ],
})


@c7c.add('C3', (1, 2, 3, 4), 'numerical')
def c7c_remit(r, D):
    gdp = r.choice([30, 36, 40, 45, 50])
    pc = r.choice([15, 18, 20, 22, 25])
    rem = round(gdp * pc / 100, 1)
    mig = r.choice([1.5, 2, 2.5, 3])
    stem = f'Country N has a GDP of about US${gdp} billion. Remittances from about {fmt(mig, 1)} million citizens working abroad are equal to {pc}% of GDP.'
    if D == 1:
        opts, a = mcq(r, f'US${fmt(rem, 1)} billion', [f'US${fmt(rem * 10, 1)} billion', f'US${pc} billion', f'US${fmt(gdp - rem, 1)} billion'])
        return {'stem': stem + ' What is the value of remittances?', 'options': opts, 'answer': a, 'key': f'{pc}% × {gdp} = {fmt(rem, 1)} billion. [1]'}
    per = round(rem * 1e9 / (mig * 1e6))
    parts = [
        lambda r: ('Calculate the value of remittances.', f'US${fmt(rem, 1)} billion', f'{pc}/100 × {gdp} [1]'),
        lambda r: ('Calculate the average remittance per migrant per year.', f'about US${per:,}'.replace(',', ' '), f'{fmt(rem, 1)} billion ÷ {fmt(mig, 1)} million [2]'),
        lambda r: ('Explain two ways remittances benefit families in Country N.', 'Pay for food, school fees and health care; improve housing; invest in land or small businesses.', '1 mark each, developed [2]'),
        lambda r: ('Suggest one risk of an economy depending heavily on remittances.', 'If the host countries’ economies decline (e.g. a fall in oil prices or a pandemic), remittances fall suddenly; it can discourage investment in local jobs.', '1 mark risk; 1 mark explanation [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


c7d = T('Urbanisation and the growth of megacities', 'urbanisation growth megacities')
build(c7d, {
    'who': 'a geographer',
    'terms': [
        ('urbanisation', 'the increase in the proportion of a country’s population living in towns and cities'),
        ('megacity', 'a city with a population of more than 10 million people'),
        ('rural-urban migration', 'the movement of people from the countryside to towns and cities'),
        ('natural increase', 'growth in population when births are higher than deaths'),
        ('suburbanisation', 'the movement of people and businesses from city centres to the edges of cities'),
        ('counter-urbanisation', 'the movement of people from cities to rural areas'),
        ('urban sprawl', 'the uncontrolled spread of a city into the surrounding countryside'),
        ('primate city', 'a city that is much larger and more important than any other in its country'),
    ],
    'mcq': [
        ('What is a megacity?', 'A city with over 10 million people', ['A city with over 1 million people', 'Any capital city', 'A city covering more than 100 km²'], '[1]'),
        ('About what proportion of the world’s population lived in urban areas in 2018?', 'About 55%', ['About 5%', 'About 30%', 'About 90%'], 'About 30% in 1950; projected about 68% by 2050 (UN). [1]'),
        ('Which city has the largest urban population in the world (about 37 million in its metropolitan area)?', 'Tokyo', ['London', 'Lagos', 'Paris'], 'Delhi is expected to overtake it. [1]'),
        ('Which two processes cause cities in lower-income countries to grow?', 'Rural-urban migration and natural increase', ['Counter-urbanisation and emigration', 'Falling birth rates and suburbanisation', 'Deindustrialisation and drought'], '[1]'),
        ('Which region has many of the world’s fastest-growing cities today?', 'Sub-Saharan Africa and South Asia', ['Western Europe', 'North America', 'Antarctica'], 'E.g. Lagos, Kinshasa, Dhaka, Delhi. [1]'),
        ('Which is an example of counter-urbanisation?', 'A family moves from London to a village in Devon and works from home', ['A farmer moves to Lagos for factory work', 'A city expands onto farmland', 'A shanty town grows on the edge of Mumbai'], '[1]'),
    ],
    'explain': [
        ('Explain why the number of megacities has increased since 1950.', 'Rapid rural-urban migration in lower- and middle-income countries for jobs and services, combined with natural increase as young migrants have children; industrial growth and globalisation have concentrated jobs in large cities.', '1 mark migration; 1 mark natural increase; 1 mark economic growth [3]'),
        ('Explain the difference between urbanisation in high-income and lower-income countries.', 'In HICs urbanisation happened mostly in the 19th and early 20th centuries and is now slow, with suburbanisation and counter-urbanisation; in LICs and NEEs it is happening rapidly now, driven by migration and natural increase.', '1 mark each; 1 mark contrast [3]'),
        ('Explain two opportunities that living in a megacity can offer.', 'More jobs (formal and informal) and higher wages; access to schools, universities and hospitals; better transport and internet; cultural and social opportunities.', '2 marks each [4]'),
        ('Explain why young adults are the group most likely to migrate to cities.', 'They are looking for work and education, have fewer family responsibilities and are more willing to take risks; their move also increases cities’ birth rates.', '1 mark reason; 1 mark development [2]'),
    ],
    'claims': [
        ('Urbanisation means the same as a city growing in size.', False, 'Urbanisation is an increase in the proportion of people living in urban areas; a city can grow while the country’s urban share stays the same.'),
        ('Most of the world’s megacities are now in Asia, Africa and Latin America.', True, 'Examples include Delhi, Shanghai, Dhaka, Cairo, São Paulo, Mexico City, Mumbai and Lagos.'),
        ('Cities grow only because people move to them.', False, 'Natural increase within cities is also a major cause, especially where many young adults live.'),
    ],
    'essays': [
        ('the growth of megacities brings more benefits than problems',
         ['Megacities concentrate jobs, investment, universities and services and produce a large share of national wealth (e.g. Mumbai).'],
         ['Rapid growth leads to informal settlements, congestion, pollution and pressure on water and sanitation (e.g. Lagos, Dhaka).', 'Inequality between rich and poor is often extreme.'],
         'Megacities offer major opportunities, but benefits outweigh problems only where growth is well planned and managed.',
         ['jobs and wealth', 'housing', 'transport and pollution', 'inequality']),
    ],
})


@c7d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c7d_urban(r, D):
    y1, y2 = r.choice([(1960, 2020), (1980, 2020), (1990, 2023), (1970, 2020)])
    tot1, tot2 = r.choice([20, 30, 40, 60]), None
    tot2 = tot1 * r.choice([2, 3, 4])
    u1, u2 = r.choice([10, 15, 20, 25]), r.choice([40, 45, 50, 55])
    up1, up2 = tot1 * u1 / 100, tot2 * u2 / 100
    stem = f'In {y1}, Country K had a population of {tot1} million, of whom {u1}% lived in urban areas. By {y2} its population was {tot2} million and {u2}% lived in urban areas.'
    if D == 1:
        opts, a = mcq(r, f'{fmt(up2, 1)} million', [f'{fmt(up1, 1)} million', f'{u2} million', f'{fmt(tot2 - up2, 1)} million', f'{fmt(up2 - up1, 1)} million'])
        return {'stem': stem + f' How many people lived in urban areas in {y2}?', 'options': opts, 'answer': a, 'key': f'{u2}% of {tot2} million = {fmt(up2, 1)} million. [1]'}
    parts = [
        lambda r: (f'Calculate the urban population in {y1} and in {y2}.', f'{fmt(up1, 1)} million and {fmt(up2, 1)} million', f'{u1}% × {tot1}; {u2}% × {tot2} [2]'),
        lambda r: ('Calculate how many times larger the urban population became.', f'{fmt(up2 / up1, 1)} times', f'{fmt(up2, 1)} ÷ {fmt(up1, 1)} [1]'),
        lambda r: ('Explain why urban population grew faster than total population.', 'Rural-urban migration moved people from the countryside to cities, in addition to natural increase in both areas, so the urban share rose.', '1 mark migration; 1 mark share rises [2]'),
        lambda r: ('Suggest two challenges this growth might create for the government.', 'Providing enough housing, water, sanitation and electricity; transport congestion; creating enough formal jobs; growth of informal settlements.', '1 mark each [2]'),
        lambda r: (f'Calculate the change in the rural population between {y1} and {y2}.', f'{fmt((tot2 - up2) - (tot1 - up1), 1)} million', f'rural = total − urban: {fmt(tot1 - up1, 1)} → {fmt(tot2 - up2, 1)} [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c7e = T('Challenges of urban living: informal settlements and sustainable cities', 'challenges urban living informal settlements sustainable cities')
build(c7e, {
    'who': 'a geographer',
    'terms': [
        ('informal settlement', 'an area of unplanned housing built by residents on land they do not legally own, usually lacking basic services (a slum or shanty town)'),
        ('informal economy', 'work that is not officially registered or taxed, such as street selling or recycling waste'),
        ('slum upgrading', 'improving informal settlements by adding services such as water, sanitation, electricity and paved paths'),
        ('site and service scheme', 'a scheme in which the government provides land with basic services and residents build their own homes'),
        ('sustainable city', 'a city that meets the needs of people today without harming the environment or the ability of future generations to meet their needs'),
        ('bus rapid transit', 'a fast bus system with dedicated lanes and stations, such as in Curitiba, Brazil'),
        ('urban regeneration', 'improving run-down areas of a city through investment in housing, jobs and the environment'),
        ('green belt', 'a protected area of countryside around a city where building is restricted'),
    ],
    'mcq': [
        ('Dharavi is a large informal settlement in which city?', 'Mumbai', ['Lagos', 'Nairobi', 'Rio de Janeiro'], 'About a million people in roughly 2 km². [1]'),
        ('Makoko, a settlement built on stilts over a lagoon, is in which city?', 'Lagos', ['Mumbai', 'Cairo', 'Dhaka'], '[1]'),
        ('Which city is famous for its bus rapid transit system, introduced in the 1970s?', 'Curitiba, Brazil', ['Moscow, Russia', 'Cairo, Egypt', 'Mumbai, India'], 'Dedicated lanes and “tube” stations make buses fast and cheap. [1]'),
        ('Which is a common problem in informal settlements?', 'Lack of clean water and sanitation', ['Too many parks', 'Very low population density', 'Too many hospitals'], 'Shared toilets and open drains spread disease. [1]'),
        ('Which of these is an example of the informal economy in Dharavi?', 'Recycling plastic and making leather goods in small workshops', ['Working for the national government', 'Teaching at a state university', 'Working in a registered bank'], 'Dharavi’s small businesses are worth hundreds of millions of US dollars a year. [1]'),
        ('Medellín in Colombia improved access to hillside neighbourhoods by building', 'cable cars linked to the metro', ['an airport in every district', 'a motorway through the centre', 'a new port'], 'The Metrocable opened in 2004. [1]'),
    ],
    'explain': [
        ('Explain why informal settlements develop in rapidly growing cities.', 'Migrants arrive faster than formal housing can be built; they cannot afford rent or land; they build homes on unused land such as hillsides, river banks and near railways, close to work.', '1 mark rapid migration; 1 mark cannot afford formal housing; 1 mark location [3]'),
        ('Explain two problems faced by people living in informal settlements.', 'Lack of clean water and sanitation spreads diseases such as cholera and diarrhoea; overcrowding and fire risk; no legal ownership, so homes can be demolished; risk of floods and landslides; insecure informal jobs.', '2 marks each explained problem [4]'),
        ('Explain why self-help and upgrading schemes are often better than demolishing informal settlements.', 'They keep communities and jobs together; they are cheaper; residents improve their own homes when given legal ownership and basic services; demolition moves people far from work and can create new slums elsewhere.', '1 mark each point up to [3]'),
        ('Describe three features of a sustainable city.', 'Efficient public transport and cycle lanes; renewable energy; recycling and waste reduction; green spaces; energy-efficient buildings; affordable housing and services for all.', '1 mark each feature [3]'),
        ('Explain why traffic congestion is a major problem in megacities, and one way to reduce it.', 'Rising car ownership and poor public transport cause jams, wasted time and air pollution; solutions include metro systems, bus rapid transit, congestion charges and park-and-ride.', '1 mark cause; 1 mark effect; 1 mark solution [3]'),
    ],
    'claims': [
        ('Informal settlements are places where nobody works.', False, 'Many residents work in the informal economy or formal jobs nearby; Dharavi has thousands of small businesses.'),
        ('Giving residents legal ownership of their homes can encourage them to improve them.', True, 'With secure tenure, people are more willing to invest in better building materials and services.'),
        ('A sustainable city only needs to focus on the environment.', False, 'Sustainability also includes social (housing, services, safety) and economic (jobs) needs.'),
    ],
    'sources': [
        dict(prov='a magazine article about Dharavi, Mumbai, written in 2020 (adapted)', kind='primary',
             text='Narrow lanes are lined with workshops where people recycle plastic, tan leather and make pottery. Up to 1500 people may share one public toilet, and the open drains overflow during the monsoon.',
             about='living conditions in an informal settlement', infer='Dharavi has a busy informal economy but very poor sanitation and severe overcrowding.',
             purpose='To inform readers about life in Dharavi, perhaps to challenge stereotypes and highlight problems.',
             plus='the writer visited Dharavi and describes what they saw', minus='a magazine may choose striking details to interest readers, and figures may be estimates',
             missing='How residents view their community, or plans to redevelop Dharavi.', enq='the challenges and opportunities of informal settlements'),
    ],
    'essays': [
        ('informal settlements should be cleared and replaced with new apartment blocks',
         ['New blocks could provide safe buildings, water and sanitation.', 'Land could be used more efficiently.'],
         ['Clearance destroys communities, informal businesses and livelihoods (e.g. Dharavi’s recycling industry).', 'New flats may be unaffordable or far from jobs.', 'Upgrading schemes such as Rio’s Favela Bairro improved conditions while keeping communities.'],
         'Upgrading with residents’ involvement is usually better than clearance, though some unsafe areas may need rehousing.',
         ['communities and jobs', 'cost', 'upgrading schemes', 'safety']),
        ('public transport is the most important feature of a sustainable city',
         ['It reduces car use, congestion and emissions (Curitiba’s bus rapid transit, Medellín’s Metrocable).'],
         ['Affordable housing, clean water and sanitation are more urgent in many cities.', 'Renewable energy, waste recycling and green space are also essential.', 'Good governance and community involvement make all features work.'],
         'Transport is vital, but a sustainable city needs a combination of features suited to local needs.',
         ['transport', 'housing', 'energy and waste', 'green space']),
    ],
})


@c7e.add('C3', (2, 3, 4, 5), 'case')
def c7e_case(r, D):
    c = r.choice([
        ('Mumbai, India', 'Dharavi', 'about 1 million people in roughly 2 km²', 'recycling, leather, pottery and garment workshops'),
        ('Lagos, Nigeria', 'Makoko', 'tens of thousands of people in homes on stilts over a lagoon', 'fishing, sawmills and trading'),
        ('Nairobi, Kenya', 'Kibera', 'hundreds of thousands of people near the city centre', 'small shops, tailoring, charcoal and recycling'),
        ('Rio de Janeiro, Brazil', 'Rocinha', 'around 70 000-100 000 people on a steep hillside', 'shops, construction and services for the wealthy districts below'),
    ])
    dens = r.choice([60000, 80000, 100000, 300000])
    intro = f'Case study: {c[1]}, an informal settlement in {c[0]}, home to {c[2]}. Many residents work in {c[3]}.'
    parts = [
        lambda r: ('Describe two challenges for people living in this settlement.', 'Lack of clean water and toilets, open drains and disease; overcrowding and fire risk; insecure land rights and risk of eviction; flooding or landslides.', '1 mark each challenge [2]'),
        lambda r: ('Explain why people continue to live there despite the challenges.', 'It is close to jobs and the city centre, rents are cheap, there are strong community and family networks, and residents can run businesses from home.', '1 mark each reason up to [3]'),
        lambda r: (f'A district has a density of {dens:,} people per km². Calculate how many people would live in 0.5 km² at this density.'.replace(',', ' '), f'{dens // 2:,} people'.replace(',', ' '), f'{dens} × 0.5 [1]'),
        lambda r: ('Suggest two ways conditions could be improved, and explain one advantage of each.', 'Upgrading with water pipes and toilet blocks (reduces disease); giving legal ownership (encourages investment); site-and-service schemes; community-led projects (keep communities together).', '1 mark each improvement; 1 mark each advantage [4]'),
        lambda r: ('Evaluate whether the informal economy is good or bad for the city.', 'Good: provides jobs, cheap goods and recycling for millions. Bad: no taxes, no workers’ rights or safety, low pay. Overall it is essential for survival but needs support and regulation.', '1 mark each side; 1 mark judgement [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


CHAPTERS[7] = [c7a, c7b, c7c, c7d, c7e]


# ============================================================== CHAPTER 8: Rights, responsibilities and citizenship

UDHR = [(1, 'All human beings are born free and equal in dignity and rights'), (3, 'the right to life, liberty and security of person'), (4, 'no one shall be held in slavery'),
        (5, 'no one shall be subjected to torture'), (9, 'no one shall be subjected to arbitrary arrest, detention or exile'), (18, 'freedom of thought, conscience and religion'),
        (19, 'freedom of opinion and expression'), (20, 'freedom of peaceful assembly and association'), (21, 'the right to take part in the government of one’s country, directly or through freely chosen representatives'),
        (23, 'the right to work and to equal pay for equal work'), (25, 'the right to an adequate standard of living, including food, clothing, housing and medical care'), (26, 'the right to education')]

c8a = T('Human rights and the Universal Declaration of Human Rights', 'human rights universal declaration')
build(c8a, {
    'who': 'a researcher',
    'terms': [
        ('human rights', 'basic rights and freedoms that belong to every person in the world from birth until death'),
        ('universal', 'applying to everyone, everywhere, regardless of who they are'),
        ('Universal Declaration of Human Rights', 'the document of 30 articles adopted by the UN General Assembly on 10 December 1948 setting out rights for all people'),
        ('responsibility', 'a duty to behave in a particular way, such as respecting the rights of others'),
        ('discrimination', 'treating a person or group unfairly because of characteristics such as race, gender, religion or disability'),
        ('United Nations Convention on the Rights of the Child', 'the 1989 international agreement setting out the rights of everyone under 18'),
        ('apartheid', 'the system of racial segregation and discrimination enforced by law in South Africa from 1948 to the early 1990s'),
        ('genocide', 'the deliberate killing of a large number of people from a particular national, ethnic or religious group'),
    ],
    'dates': [
        ('the United Nations was founded', 1945),
        ('the UN General Assembly adopted the Universal Declaration of Human Rights', 1948),
        ('the European Convention on Human Rights was signed', 1950),
        ('the UN Convention on the Rights of the Child was adopted', 1989),
        ('Nelson Mandela was released from prison after 27 years', 1990),
        ('Malala Yousafzai was awarded the Nobel Peace Prize', 2014),
    ],
    'mcq': [
        ('Who chaired the committee that drafted the Universal Declaration of Human Rights?', 'Eleanor Roosevelt', ['Winston Churchill', 'Mahatma Gandhi', 'Nelson Mandela'], '[1]'),
        ('How many articles does the Universal Declaration of Human Rights contain?', '30', ['10', '17', '100'], '[1]'),
        ('Why was the UDHR written soon after the Second World War?', 'To prevent atrocities like the Holocaust from happening again', ['To end the First World War', 'To create the European Union', 'To start the Cold War'], '[1]'),
        ('Which day is celebrated each year as Human Rights Day?', '10 December', ['1 January', '11 November', '25 December'], 'The anniversary of the UDHR’s adoption in 1948. [1]'),
        ('Which statement about the UDHR is correct?', 'It is a declaration, not a treaty, so it is not legally binding by itself, but it has inspired many binding laws',
         ['It is a law that every country’s courts must apply', 'It only applies to European countries', 'It was written in 2000'], '[1]'),
        ('Why was Malala Yousafzai attacked in 2012?', 'She campaigned for girls’ right to education in Pakistan', ['She was standing for president', 'She was a journalist in Syria', 'She led a strike in a factory'], 'She became the youngest Nobel Peace Prize winner in 2014. [1]'),
    ],
    'explain': [
        ('Explain why human rights are described as “universal”.', 'They belong to every person equally, everywhere in the world, regardless of nationality, gender, race, religion or any other status.', '1 mark everyone; 1 mark regardless of status [2]'),
        ('Explain why rights come with responsibilities.', 'If everyone has rights, each person has a duty to respect others’ rights – e.g. freedom of expression does not include the right to threaten or spread hatred about others.', '1 mark link; 1 mark example [2]'),
        ('Explain why the UDHR is important even though it is not a binding treaty.', 'It sets a common international standard; it has inspired constitutions and binding treaties such as the European Convention on Human Rights (1950) and UN covenants; campaigners use it to hold governments to account.', '1 mark each point up to [3]'),
        ('Explain how two rights can come into conflict, with an example.', 'E.g. freedom of expression (Article 19) can conflict with the right to privacy when newspapers publish private details; or freedom of assembly can conflict with others’ security. Courts must balance them.', '1 mark two rights; 1 mark example; 1 mark balance [3]'),
        ('Explain why apartheid in South Africa was a violation of human rights.', 'It classified people by race and denied Black South Africans the vote, equal education, freedom of movement and the right to live where they chose – breaking Articles 1, 2, 13 and 21 of the UDHR.', '1 mark examples of denial; 1 mark link to equality/UDHR [2]'),
    ],
    'claims': [
        ('Human rights only apply to adults.', False, 'Human rights belong to everyone; children also have extra protection under the 1989 UN Convention on the Rights of the Child.'),
        ('Governments can never limit any right in any circumstances.', False, 'Some rights (such as freedom from torture) are absolute, but others can be limited by law to protect others, e.g. for public safety.'),
        ('The UDHR was adopted by the United Nations in 1948.', True, 'It was adopted by the UN General Assembly in Paris on 10 December 1948.'),
        ('The right to education is included in the UDHR.', True, 'Article 26 states that everyone has the right to education, and elementary education should be free and compulsory.'),
    ],
    'sources': [
        dict(prov='Article 1 of the Universal Declaration of Human Rights, 1948', kind='primary', why='it is the original text adopted by the UN in 1948',
             text='All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.',
             about='the ideas behind human rights', infer='Human rights are based on the idea that every person has equal worth and that people have a duty to treat each other well.',
             purpose='To set out a shared principle for all nations after the horrors of the Second World War.',
             plus='it is the official text agreed by the UN General Assembly', minus='it states ideals, not whether governments actually respected them',
             missing='How rights are enforced, or examples of rights being denied, such as apartheid.', enq='why human rights matter'),
    ],
    'essays': [
        ('the Universal Declaration of Human Rights has been successful in protecting human rights around the world',
         ['It set a global standard and inspired binding treaties, national constitutions and courts.', 'Campaigners and NGOs such as Amnesty International use it to expose abuses.'],
         ['It is not legally binding; many governments still use torture, censorship and discrimination.', 'Genocides, e.g. Rwanda 1994, happened despite it.', 'Rights are often unequal in practice, e.g. access to education.'],
         'It has been very influential in setting standards, but protection depends on governments and enforcement.',
         ['influence on laws', 'enforcement', 'continuing abuses', 'campaigners']),
        ('responsibilities are just as important as rights',
         ['Rights only work if people respect the rights of others.', 'Citizens’ responsibilities (obeying laws, voting, paying taxes) keep society functioning.'],
         ['Human rights are inalienable – people should not lose them for failing a responsibility.', 'Governments’ responsibility to protect rights matters most.'],
         'Rights and responsibilities depend on each other, but basic human rights should not be conditional.',
         ['respecting others', 'the law', 'government duties']),
    ],
})


@c8a.add('C3', (1, 2, 3, 4), 'case')
def c8a_article(r, D):
    sc = r.choice([
        ('A journalist is jailed for writing an article criticising the government.', 19, 'freedom of opinion and expression'),
        ('A girl is told she cannot go to secondary school because she must work at home.', 26, 'the right to education'),
        ('Police arrest a protester and keep him in prison for months without charge or trial.', 9, 'no one shall be subjected to arbitrary arrest, detention or exile'),
        ('A factory pays women less than men for exactly the same job.', 23, 'the right to work and to equal pay for equal work'),
        ('A group of workers is forced to work without pay and cannot leave the farm.', 4, 'no one shall be held in slavery'),
        ('A government bans a peaceful march by students calling for cleaner air.', 20, 'freedom of peaceful assembly and association'),
        ('Citizens of one ethnic group are not allowed to vote in national elections.', 21, 'the right to take part in the government of one’s country'),
        ('A family is forced to leave their home and live on the street with no help.', 25, 'the right to an adequate standard of living, including housing'),
        ('Prisoners are beaten during questioning to make them confess.', 5, 'no one shall be subjected to torture'),
        ('A student is punished at school for practising her religion.', 18, 'freedom of thought, conscience and religion'),
    ])
    if D <= 1:
        opts, a = mcq(r, f'Article {sc[1]}: {dict(UDHR)[sc[1]]}', [f'Article {n}: {t}' for n, t in UDHR if n != sc[1]])
        return {'stem': f'Scenario: {sc[0]} Which article of the UDHR is most clearly being broken?', 'options': opts, 'answer': a, 'key': f'Article {sc[1]}. [1]'}
    parts = [
        lambda r: ('Identify the human right that is being denied.', f'{cap(sc[2])} (UDHR Article {sc[1]}).', '1 mark right [1]'),
        lambda r: ('Explain why this is a violation of human rights.', 'Everyone is entitled to this right equally; the action treats the person as having less dignity and denies a freedom the UDHR says is universal.', '1 mark link to scenario; 1 mark universality/equality [2]'),
        lambda r: ('Suggest two actions that individuals or organisations could take in response.', 'Report it to the media or a human rights NGO (e.g. Amnesty International); take a case to court or a national human rights commission; start a petition or peaceful campaign; contact elected representatives.', '1 mark each [2]'),
        lambda r: ('Explain one reason why it can be difficult to protect this right in practice.', 'The government itself may be responsible; courts may not be independent; the UDHR is not directly enforceable; victims may fear reprisals or lack money for legal help.', '1 mark reason; 1 mark development [2]'),
    ]
    return compose(r, f'Scenario: {sc[0]}', parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


c8b = T('How governments work: democracy, elections and the rule of law', 'governments work democracy elections rule law')
build(c8b, {
    'who': 'a researcher',
    'terms': [
        ('democracy', 'a system of government in which citizens choose their leaders in free and fair elections'),
        ('direct democracy', 'a system in which citizens vote on decisions themselves, for example in referendums'),
        ('representative democracy', 'a system in which citizens elect representatives to make decisions on their behalf'),
        ('rule of law', 'the principle that everyone, including the government, must obey the law and is equal before it'),
        ('separation of powers', 'dividing government into the legislature, executive and judiciary so that no one branch has too much power'),
        ('legislature', 'the branch of government that makes laws, such as a parliament'),
        ('executive', 'the branch of government that carries out laws and runs the country, such as the president or prime minister and ministers'),
        ('judiciary', 'the system of courts and judges that interprets and applies the law'),
        ('constitution', 'the set of basic rules and principles that says how a country is governed'),
        ('authoritarian', 'a system in which power is held by one leader or party and citizens have few political freedoms'),
        ('referendum', 'a vote by all citizens on a single important question'),
        ('first-past-the-post', 'an electoral system in which the candidate with the most votes in each constituency wins'),
    ],
    'dates': [
        ('King John agreed to Magna Carta', 1215),
        ('New Zealand became the first self-governing country to give women the vote in national elections', 1893),
        ('women in the UK gained the vote on equal terms with men', 1928),
        ('India held its first general election as an independent republic', 1951),
        ('South Africa held its first election in which people of all races could vote', 1994),
    ],
    'mcq': [
        ('Which branch of government interprets the law and decides cases?', 'The judiciary', ['The legislature', 'The executive', 'The media'], '[1]'),
        ('In ancient Athens in the 5th century BCE, citizens voted on laws themselves. This is an example of', 'direct democracy', ['representative democracy', 'dictatorship', 'monarchy'], 'Only free adult men counted as citizens. [1]'),
        ('Which country is often called the world’s largest democracy?', 'India', ['China', 'Saudi Arabia', 'Vatican City'], 'Nearly a billion registered voters in 2024. [1]'),
        ('What does the “rule of law” mean?', 'Everyone, including leaders, must obey the law and is equal before it', ['The ruler can make any law and ignore it', 'Only the police must obey the law', 'Laws apply only to poor people'], '[1]'),
        ('Why is a secret ballot important in elections?', 'It allows people to vote freely without fear of pressure or punishment', ['It makes counting votes faster', 'It means only some people can vote', 'It allows people to vote twice'], '[1]'),
        ('In which country is voting compulsory in national elections?', 'Australia', ['The United States', 'The United Kingdom', 'India'], 'Since 1924 for federal elections. [1]'),
    ],
    'explain': [
        ('Explain why the separation of powers is important in a democracy.', 'Dividing power between the legislature, executive and judiciary means each can check the others, preventing any one person or group from abusing power.', '1 mark three branches; 1 mark checks and prevents abuse [2]'),
        ('Explain the difference between a democracy and an authoritarian state.', 'In a democracy citizens choose and can remove leaders in free, fair elections and have freedoms such as speech and a free press; in an authoritarian state power is held by one leader or party, elections are absent or not free, and opposition and media are controlled.', '1 mark each; 1 mark contrast [3]'),
        ('Explain why an independent judiciary is important for the rule of law.', 'Judges who are free from government control can apply the law fairly and rule against the government when it breaks the law, protecting citizens’ rights.', '1 mark independence; 1 mark protects rights/holds government to account [2]'),
        ('Explain one advantage and one disadvantage of the first-past-the-post electoral system.', 'Advantage: simple, quick to count, usually produces strong single-party governments and a clear local representative. Disadvantage: seats do not match vote share, smaller parties win few seats and many votes are “wasted”.', '1 mark each [2]'),
        ('Explain why a free press is important in a democracy.', 'It informs citizens so they can make choices in elections, investigates and exposes wrongdoing by those in power and allows a range of opinions to be heard.', '1 mark informs voters; 1 mark holds power to account [2]'),
    ],
    'claims': [
        ('In a democracy the government can ignore the courts if it has won an election.', False, 'Under the rule of law, the government must obey the law and court rulings like everyone else.'),
        ('A referendum is an example of direct democracy.', True, 'Citizens vote directly on a single question, such as Switzerland’s regular referendums.'),
        ('All democracies use the same voting system.', False, 'Systems include first-past-the-post (UK, India), proportional representation (e.g. the Netherlands) and mixed systems (e.g. Germany).'),
        ('Elections alone are enough to make a country a democracy.', False, 'Democracy also needs fair elections, free media, the rule of law, independent courts and protection of rights.'),
    ],
    'essays': [
        ('free elections are the most important feature of a democracy',
         ['Elections give citizens the power to choose and remove leaders peacefully.'],
         ['Without the rule of law, a free press and independent courts, elections can be manipulated and rights abused.', 'Protection of minorities matters so the majority cannot oppress others.'],
         'Free elections are essential but not sufficient; democracy depends on a set of institutions working together.',
         ['elections', 'the rule of law', 'free press', 'rights of minorities']),
        ('first-past-the-post is a fair way to elect a government',
         ['It is simple, links each MP to a constituency and usually gives a clear result.'],
         ['Parties can win a majority of seats with a minority of votes.', 'Smaller parties are under-represented.', 'Proportional systems match seats more closely to votes.'],
         'It is effective at producing stable governments but less fair in representing voters’ choices.',
         ['simplicity', 'vote share and seats', 'small parties', 'strong government']),
    ],
})


@c8b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c8b_fptp(r, D):
    parties = ['Green Party', 'People’s Party', 'Reform Alliance', 'Workers’ Party']
    r.shuffle(parties)
    p3 = parties[:3]
    cons = []
    for _ in range(5):
        v = [r.randint(2000, 9000) for _ in range(3)]
        if len(set(v)) < 3:
            return None
        cons.append(v)
    seats = [0, 0, 0]
    votes = [0, 0, 0]
    for v in cons:
        seats[v.index(max(v))] += 1
        for k in range(3):
            votes[k] += v[k]
    tv = sum(votes)
    shares = [round(100 * x / tv, 1) for x in votes]
    stem = 'Results in five constituencies (votes for ' + ', '.join(p3) + '): ' + '; '.join(f'C{i + 1}: {v[0]}, {v[1]}, {v[2]}' for i, v in enumerate(cons)) + '. The election uses first-past-the-post.'
    win = p3[seats.index(max(seats))]
    if D == 1:
        opts, a = mcq(r, win, [p for p in parties if p != win])
        return {'stem': stem + ' Which party wins the most seats?', 'options': opts, 'answer': a, 'key': f'Seats: ' + ', '.join(f'{p} {s}' for p, s in zip(p3, seats)) + '. [1]'}
    electorate = r.choice([30000, 40000, 50000])
    t1 = sum(cons[0])
    parts = [
        lambda r: ('Work out how many seats each party wins.', ', '.join(f'{p} {s}' for p, s in zip(p3, seats)), 'winner = most votes in each constituency [2]'),
        lambda r: ('Calculate each party’s share of the total vote.', ', '.join(f'{p} {fmt(s, 1)}%' for p, s in zip(p3, shares)), f'total {tv} votes [2]'),
        lambda r: ('Use the results to explain one criticism of first-past-the-post.', 'Seat shares do not match vote shares: ' + ', '.join(f'{p} {fmt(sh, 1)}% of votes → {s} of 5 seats' for p, sh, s in zip(p3, shares, seats)) + '; votes for losing candidates are “wasted”.', '1 mark comparison with figures; 1 mark criticism [2]'),
        lambda r: (f'Constituency C1 has {electorate:,} registered voters. Calculate the turnout.'.replace(',', ' '), f'{fmt(round(100 * t1 / electorate, 1), 1)}%', f'{t1} ÷ {electorate} × 100 [1]'),
        lambda r: ('Suggest two reasons why turnout in elections may be low.', 'Voters feel their vote will not change the result (safe seats); distrust of politicians; difficulty getting to polling stations; lack of interest or information.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c8c = T('Active citizenship: campaigning, voting and making change', 'active citizenship campaigning voting making change')
build(c8c, {
    'who': 'a researcher',
    'terms': [
        ('active citizen', 'a person who takes part in their community and in decision-making, for example by voting, volunteering or campaigning'),
        ('pressure group', 'an organisation that tries to influence government decisions without standing for election'),
        ('non-governmental organisation (NGO)', 'a non-profit organisation independent of government, such as Amnesty International or Oxfam'),
        ('petition', 'a formal written request signed by many people and sent to those in power'),
        ('boycott', 'refusing to buy, use or take part in something as a protest'),
        ('lobbying', 'trying to persuade politicians to support a cause, for example by meeting or writing to them'),
        ('volunteering', 'giving time and effort without pay to help others or the community'),
        ('civil disobedience', 'deliberately and peacefully breaking a law seen as unjust, as a form of protest'),
    ],
    'dates': [
        ('the Women’s Social and Political Union (suffragettes) was founded by Emmeline Pankhurst', 1903),
        ('Rosa Parks was arrested in Montgomery, Alabama, starting a bus boycott', 1955),
        ('Amnesty International was founded', 1961),
        ('Greenpeace was founded', 1971),
        ('women in the Chipko movement hugged trees to stop logging in the Indian Himalayas', 1973),
        ('Wangari Maathai founded the Green Belt Movement in Kenya', 1977),
        ('Greta Thunberg began her school strike for the climate outside the Swedish parliament', 2018),
    ],
    'mcq': [
        ('Which of these is an example of a boycott?', 'Refusing to buy products from a company that uses child labour', ['Voting in a local election', 'Writing a letter to a newspaper', 'Volunteering at a food bank'], '[1]'),
        ('What was the result of the Montgomery bus boycott (1955-56)?', 'The US Supreme Court ruled that segregation on buses was unconstitutional', ['Rosa Parks became president', 'Buses were banned in Alabama', 'Nothing changed'], 'The boycott lasted about 381 days. [1]'),
        ('In the UK, how many signatures does a parliamentary e-petition need to be considered for debate in Parliament?', '100 000', ['100', '1000', '10 million'], 'At 10 000 the government responds in writing. [1]'),
        ('Wangari Maathai, founder of the Green Belt Movement, was the first African woman to', 'win the Nobel Peace Prize', ['become President of the USA', 'climb Mount Everest', 'lead the United Nations'], 'Awarded in 2004; the movement planted tens of millions of trees. [1]'),
        ('Which is a peaceful method of campaigning?', 'Organising a petition and meeting local representatives', ['Damaging property', 'Threatening politicians', 'Spreading false information'], '[1]'),
    ],
    'explain': [
        ('Explain two ways young people can be active citizens before they are old enough to vote.', 'Join a school council or youth parliament; volunteer in the community; sign or start petitions; write to elected representatives; take part in peaceful campaigns or awareness projects.', '2 marks each explained way [4]'),
        ('Explain why campaigners use social media.', 'It reaches large numbers of people quickly and cheaply, spreads messages globally (e.g. Fridays for Future), helps organise events and puts public pressure on decision-makers; but it can spread misinformation.', '1 mark reach/speed; 1 mark organising/pressure; 1 mark limitation [3]'),
        ('Explain why voting is an important responsibility of citizens in a democracy.', 'Voting chooses representatives and governments; it gives people a say in decisions that affect them; low turnout can make governments less representative.', '1 mark each point up to [2]'),
        ('Explain why some campaigns succeed while others fail.', 'Success depends on clear aims, wide public support, effective leadership, media attention, peaceful methods that win sympathy, and whether decision-makers are willing or able to respond.', '1 mark each factor up to [3]'),
        ('Explain the difference between a pressure group and a political party.', 'A political party stands candidates in elections and wants to form a government covering all issues; a pressure group tries to influence decisions on particular issues without standing for election.', '1 mark each; 1 mark contrast [2]'),
    ],
    'claims': [
        ('Only adults can be active citizens.', False, 'Young people can volunteer, campaign, join youth councils and petitions, as Malala Yousafzai and Greta Thunberg showed.'),
        ('Civil disobedience always involves violence.', False, 'Civil disobedience is usually deliberately peaceful, as in Gandhi’s Salt March or Rosa Parks’ refusal to give up her seat.'),
        ('The Chipko movement was a campaign to protect forests in India.', True, 'Villagers, many of them women, hugged trees to prevent logging in Uttarakhand from 1973.'),
    ],
    'essays': [
        ('peaceful protest is the most effective way for citizens to bring about change',
         ['Peaceful campaigns win public sympathy and media attention: the Montgomery bus boycott, Gandhi’s Salt March, Fridays for Future.'],
         ['Voting and elections change governments and laws directly.', 'Lobbying, petitions and legal challenges can achieve change quietly.', 'Some groups (e.g. some suffragettes) argued militant action was needed when peaceful methods were ignored.'],
         'Peaceful protest is powerful, especially combined with voting, lobbying and legal action.',
         ['protest and boycotts', 'voting', 'lobbying and petitions', 'legal action']),
        ('young people today have more power to make change than ever before',
         ['Social media lets young people organise globally (school climate strikes from 2018).', 'Youth parliaments and votes at 16 in some countries.'],
         ['Many young people cannot vote and have little money or influence.', 'Online campaigns may not lead to real change; decision-makers may ignore them.', 'Young people in the past also led major movements.'],
         'Young people have new tools and reach, but turning attention into change still depends on political systems.',
         ['social media', 'voting age', 'examples of youth campaigns']),
    ],
})

CAMPAIGNS = ['a safe crossing outside the school', 'more recycling bins in the town centre', 'a ban on single-use plastics in the school canteen', 'better lighting in the local park',
             'free bus passes for students', 'protecting a local woodland from development', 'a community vegetable garden on unused land']


@c8c.add('C3', (2, 3, 4, 5), 'case')
def c8c_plan(r, D):
    aim = r.choice(CAMPAIGNS)
    n = r.choice([120, 250, 400, 600, 900])
    pop = r.choice([1500, 2000, 3000, 5000])
    intro = f'A group of students in {city(r)} is campaigning for {aim}. In two weeks their petition has collected {n} signatures in a community of about {pop:,} people.'.replace(',', ' ')
    parts = [
        lambda r: ('Calculate the percentage of the community who have signed.', f'{fmt(round(100 * n / pop, 1), 1)}%', f'{n} ÷ {pop} × 100 [1]'),
        lambda r: ('Identify who the students should try to persuade, and explain why.', 'The local council or school leadership (decision-makers), because they have the power and budget to make the change; also local media to raise awareness.', '1 mark target; 1 mark reason [2]'),
        lambda r: ('Suggest three methods the students could use, apart from the petition.', 'Write to or meet a local councillor; use social media and posters; collect evidence (surveys, photos, traffic counts); hold a peaceful event; contact local newspapers.', '1 mark each [3]'),
        lambda r: ('Explain why collecting evidence would make the campaign more persuasive.', 'Data such as surveys or counts shows the problem is real and how many people it affects, so decision-makers are more likely to act.', '1 mark shows need; 1 mark persuades decision-makers [2]'),
        lambda r: ('Evaluate how the students could judge whether their campaign was successful.', 'Whether the change happened; the number of supporters; media coverage; whether decision-makers responded; what they learned. Partial success (e.g. a promise or trial) still counts.', '1 mark criterion; 1 mark second criterion; 1 mark judgement [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


c8d = T('Identity, diversity and community belonging', 'identity diversity community belonging')
build(c8d, {
    'who': 'a researcher',
    'terms': [
        ('identity', 'the qualities, beliefs, background and relationships that make a person who they are'),
        ('multiple identities', 'the idea that a person belongs to several groups at once, such as a nationality, religion, family and local community'),
        ('diversity', 'the range of differences between people in a community, such as ethnicity, religion, language and culture'),
        ('stereotype', 'a fixed, oversimplified idea about a group of people'),
        ('prejudice', 'an opinion about a person or group formed without knowledge or reason, often negative'),
        ('discrimination', 'treating a person or group unfairly because of who they are'),
        ('community cohesion', 'when people from different backgrounds get on well together and share a sense of belonging'),
        ('multiculturalism', 'the presence of, and support for, several different cultural groups within one society'),
        ('integration', 'the process by which people from different backgrounds become part of a shared community while keeping their own identity'),
    ],
    'mcq': [
        ('Which of these is an example of a stereotype?', '“All teenagers are lazy.”', ['“My brother is 14.”', '“Some students walk to school.”', '“Our town has two mosques and three churches.”'], 'A fixed generalisation about a whole group. [1]'),
        ('How many official languages does Singapore have?', 'Four (English, Malay, Mandarin and Tamil)', ['One', 'Two', 'Twelve'], '[1]'),
        ('Which country adopted an official policy of multiculturalism in 1971, the first in the world?', 'Canada', ['Japan', 'France', 'Brazil'], '[1]'),
        ('What is the difference between prejudice and discrimination?', 'Prejudice is an attitude; discrimination is an action', ['They mean exactly the same', 'Prejudice is always illegal', 'Discrimination is a feeling'], '[1]'),
        ('Which is an example of having multiple identities?', 'Being Kenyan, a Muslim, a footballer and a member of a large family at the same time', ['Having one passport only', 'Living in one house', 'Speaking only one language'], '[1]'),
    ],
    'explain': [
        ('Explain how a person’s identity can change over time.', 'People gain new experiences, move to new places, learn languages, change jobs or beliefs and join new groups, so how they see themselves – and which identity matters most – can change.', '1 mark change factor; 1 mark example [2]'),
        ('Explain two benefits of living in a diverse community.', 'Learning about different cultures, foods, languages and festivals; wider range of skills and ideas for the economy; greater tolerance and understanding.', '2 marks each [4]'),
        ('Explain how stereotypes can lead to discrimination.', 'Stereotypes create fixed, often negative ideas about groups; these can become prejudice, which may lead people to treat members of the group unfairly, e.g. in jobs or housing.', '1 mark stereotype → prejudice; 1 mark → unfair treatment/example [2]'),
        ('Explain two ways a community can help newcomers feel that they belong.', 'Welcome events and clubs; language classes; inclusive festivals celebrating different cultures; mentoring or buddy schemes; making services available in several languages.', '2 marks each [4]'),
        ('Explain why laws against discrimination are important.', 'They protect people’s right to equal treatment in work, education and services; they give victims a way to seek justice and they set clear standards for society.', '1 mark protection; 1 mark justice/standards [2]'),
    ],
    'claims': [
        ('A person can only have one identity.', False, 'People have multiple identities – national, religious, family, local, interests – that overlap.'),
        ('Diversity always weakens a community.', False, 'Many diverse communities are strong and cohesive; diversity brings new skills and ideas when people are included and treated fairly.'),
        ('Stereotypes can be harmful even when they seem positive.', True, 'They still ignore individual differences and can put pressure on people or lead to unfair judgements.'),
    ],
    'essays': [
        ('national identity is the most important part of who a person is',
         ['Nationality shapes language, culture, rights and how others see us.'],
         ['Family, religion, ethnicity, local community, gender and interests may matter more to many people.', 'Migrants and people with mixed heritage may have several national identities.', 'Identity changes over time and in different situations.'],
         'National identity is important for many people, but identity is personal and made up of many parts.',
         ['family and religion', 'migration', 'local community', 'changes over time']),
        ('schools are the most important place for building community cohesion',
         ['Schools bring together children from different backgrounds daily and can teach respect and challenge stereotypes.'],
         ['Families, religious groups, sports clubs and local councils also shape belonging.', 'Housing segregation can limit what schools can do.', 'Media and online spaces strongly influence attitudes.'],
         'Schools play a key role, but cohesion depends on the whole community.',
         ['schools', 'families', 'clubs and religious groups', 'the media']),
    ],
})


@c8d.add('C3', (1, 2, 3, 4), 'numerical')
def c8d_survey(r, D):
    n = r.choice([80, 100, 120, 150, 200])
    a = r.randint(int(n * 0.35), int(n * 0.6))
    b = r.randint(int(n * 0.15), int(n * 0.3))
    c = n - a - b
    if c <= 0:
        return None
    stem = (f'A survey of {n} residents in a diverse neighbourhood asked “Do you feel you belong to this community?” Results: “Strongly” {a}, “A little” {b}, “Not at all” {c}.')
    if D == 1:
        opts, ans = mcq(r, f'{fmt(round(100 * (a + b) / n, 1), 1)}%', [f'{fmt(round(100 * a / n, 1), 1)}%', f'{fmt(round(100 * c / n, 1), 1)}%', f'{a + b}%', '100%'])
        return {'stem': stem + ' What percentage felt they belonged at least a little?', 'options': opts, 'answer': ans, 'key': f'({a} + {b}) ÷ {n} × 100. [1]'}
    parts = [
        lambda r: ('Calculate the percentage who answered “Not at all”.', f'{fmt(round(100 * c / n, 1), 1)}%', f'{c} ÷ {n} × 100 [1]'),
        lambda r: ('Suggest two reasons why some residents may not feel they belong.', 'They may have recently arrived, face language barriers or discrimination, have few local friends or family, or feel excluded from local decisions.', '1 mark each [2]'),
        lambda r: ('Suggest two actions the local council could take to increase belonging.', 'Community festivals and events; language classes; youth clubs and sports; involving residents in decisions; tackling discrimination.', '1 mark each [2]'),
        lambda r: ('Explain one limitation of this survey.', 'A small sample may not represent the whole neighbourhood; people may not answer honestly; “belonging” means different things to different people; who was asked and where may bias results.', '1 mark limitation; 1 mark explanation [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


CHAPTERS[8] = [c8a, c8b, c8c, c8d]


# ============================================================== CHAPTER 9: Globalisation, trade and sustainable development

c9a = T('What is globalisation? Trade, transport and communication links', 'globalisation trade transport communication links')
build(c9a, {
    'who': 'a geographer',
    'terms': [
        ('globalisation', 'the process by which the world’s economies, cultures and peoples are becoming more connected and interdependent'),
        ('interdependence', 'when countries rely on each other for goods, services, money and resources'),
        ('containerisation', 'the use of standard-sized steel containers to transport goods by ship, rail and road'),
        ('imports', 'goods and services bought from other countries'),
        ('exports', 'goods and services sold to other countries'),
        ('free trade', 'trade between countries without taxes (tariffs) or limits (quotas) on imports'),
        ('tariff', 'a tax placed on imported goods'),
        ('time-space compression', 'the feeling that the world is “shrinking” because travel and communication have become much faster'),
        ('World Trade Organization', 'the international organisation, founded in 1995, that sets and enforces rules for trade between countries'),
    ],
    'dates': [
        ('the Suez Canal opened, linking the Mediterranean and the Red Sea', 1869),
        ('the Panama Canal opened, linking the Atlantic and Pacific Oceans', 1914),
        ('the General Agreement on Tariffs and Trade (GATT) was signed', 1947),
        ('the first container ship voyage, organised by Malcom McLean, sailed from New Jersey', 1956),
        ('Tim Berners-Lee proposed the World Wide Web', 1989),
        ('the World Trade Organization was set up', 1995),
        ('the container ship Ever Given blocked the Suez Canal for six days', 2021),
    ],
    'mcq': [
        ('Why did containerisation make global trade much cheaper?', 'Standard containers can be moved quickly between ships, trains and lorries by crane, cutting loading time and labour costs',
         ['Containers float without ships', 'Containers are made of paper', 'Containers can only carry food'], '[1]'),
        ('Which of these is an example of cultural globalisation?', 'The same films, music and fast-food chains being popular in many countries', ['A local farmer selling vegetables at a village market', 'A country closing its borders', 'Building a village well'], '[1]'),
        ('What carries most of the world’s international internet data?', 'Undersea fibre-optic cables', ['Satellites only', 'Radio towers', 'Postal services'], 'Over 95% of intercontinental data. [1]'),
        ('Which port is the world’s busiest container port?', 'Shanghai', ['London', 'Lagos', 'Sydney'], 'Over 45 million standard containers (TEU) a year. [1]'),
        ('Why was the blocking of the Suez Canal in 2021 so disruptive?', 'About 12% of world trade passes through the canal, so hundreds of ships were delayed',
         ['It is the only route to Australia', 'It carries all the world’s oil', 'It is used only by passenger ships'], 'Shows interdependence and fragile supply chains. [1]'),
        ('Which of these is a barrier to free trade?', 'A tariff on imported cars', ['A container ship', 'An undersea cable', 'A trade agreement removing taxes'], '[1]'),
    ],
    'explain': [
        ('Explain how improvements in transport have encouraged globalisation.', 'Container ships, larger aircraft and better ports have made moving goods and people faster and cheaper, so companies can buy and sell around the world and tourism and migration have grown.', '1 mark example; 1 mark faster/cheaper; 1 mark effect on trade/people [3]'),
        ('Explain how the internet and mobile phones have speeded up globalisation.', 'Instant, cheap communication lets companies manage factories and offices worldwide, trade online and outsource services such as call centres; ideas, news and culture spread instantly.', '1 mark each point up to [3]'),
        ('Explain what is meant by interdependence, using an example.', 'Countries rely on each other: e.g. Europe imports smartphones made in China while China imports European machinery; a problem in one place (such as the Suez blockage) affects others.', '1 mark meaning; 1 mark example [2]'),
        ('Explain one advantage and one disadvantage of globalisation for a lower-income country.', 'Advantage: new jobs and investment from foreign companies, access to bigger export markets and technology. Disadvantage: low wages and poor conditions, profits sent abroad, local businesses unable to compete, loss of local culture.', '1 mark each with development [2]'),
        ('Explain how globalisation has affected culture around the world.', 'Global brands, films, music and social media spread worldwide, creating shared cultures; but this can weaken local languages and traditions, though local cultures also spread globally (e.g. K-pop, Bollywood).', '1 mark spread; 1 mark loss; 1 mark two-way exchange [3]'),
    ],
    'claims': [
        ('Globalisation only affects trade in goods.', False, 'It also involves services, money, migration, ideas, culture, information and environmental issues.'),
        ('The internet has helped small businesses sell to customers in other countries.', True, 'Online marketplaces and payment systems allow even small firms to export.'),
        ('Globalisation has made every country equally rich.', False, 'Some countries and groups have gained much more than others; inequality between and within countries remains large.'),
        ('Most goods traded internationally travel by sea.', True, 'Around 80-90% of world trade by volume is carried by ships.'),
    ],
    'essays': [
        ('globalisation has brought more benefits than problems to the world',
         ['World trade has grown hugely, creating jobs and lowering prices; hundreds of millions have escaped extreme poverty in countries such as China and India.', 'Faster communication spreads knowledge and technology.'],
         ['Benefits are unequal; some workers face low wages and poor conditions.', 'Transport and production increase carbon emissions and pollution.', 'Supply chains are vulnerable (Suez 2021, COVID-19).', 'Local cultures and businesses may be lost.'],
         'Globalisation has brought large economic benefits, but they are unevenly shared and come with environmental costs.',
         ['trade and jobs', 'inequality', 'the environment', 'culture']),
        ('improvements in technology have been the main cause of globalisation',
         ['Containerisation, jet aircraft and the internet have made trade and communication fast and cheap.'],
         ['Political decisions – GATT (1947), the WTO (1995), free-trade agreements and China opening its economy – removed barriers.', 'Transnational companies seeking profit drove the spread of production.'],
         'Technology made globalisation possible, but political and economic decisions explain its speed and direction.',
         ['transport', 'communication', 'trade agreements', 'TNCs']),
    ],
})


@c9a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c9a_trade(r, D):
    ex = r.choice([120, 150, 200, 250, 320])
    im = ex + r.choice([-60, -40, -20, 20, 50, 80])
    gdp = r.choice([400, 500, 600, 800, 1000])
    bal = ex - im
    stem = f'Country T exported goods and services worth US${ex} billion and imported goods and services worth US${im} billion in one year. Its GDP was US${gdp} billion.'
    if D == 1:
        opts, a = mcq(r, f'US${bal:+d} billion', [f'US${-bal:+d} billion', f'US${ex + im} billion', f'US${im} billion'])
        return {'stem': stem + ' What was its trade balance (exports − imports)?', 'options': opts, 'answer': a, 'key': f'{ex} − {im} = {bal:+d} billion. [1]'}
    parts = [
        lambda r: ('Calculate the trade balance and state whether it is a surplus or a deficit.', f'US${bal:+d} billion: a {"surplus" if bal > 0 else "deficit"}', f'{ex} − {im} [2]'),
        lambda r: ('Calculate total trade (exports + imports) as a percentage of GDP.', f'{fmt(round(100 * (ex + im) / gdp, 1), 1)}%', f'({ex} + {im}) ÷ {gdp} × 100 [2]'),
        lambda r: ('Explain what a high trade-to-GDP percentage suggests about the country.', 'It is very open and interdependent with the global economy, so it benefits from trade but is vulnerable to changes in world demand and supply chains.', '1 mark openness; 1 mark vulnerability [2]'),
        lambda r: ('Suggest two ways the country could increase its exports.', 'Join trade agreements to reduce tariffs; improve ports and transport; attract foreign companies; develop higher-value manufacturing or services.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3), type_='numerical')


c9b = T('Global supply chains and transnational companies', 'global supply chains transnational companies')
build(c9b, {
    'who': 'a geographer',
    'terms': [
        ('transnational company (TNC)', 'a large company that operates in more than one country, usually with its headquarters in a high-income country'),
        ('supply chain', 'the series of steps and places involved in making a product and getting it to the customer, from raw materials to the shop'),
        ('outsourcing', 'when a company pays another company, often in another country, to carry out part of its work'),
        ('foreign direct investment', 'money invested by a company in factories, offices or businesses in another country'),
        ('assembly', 'putting together components made elsewhere to make a finished product'),
        ('just-in-time', 'a production system in which parts arrive exactly when they are needed, reducing storage costs'),
        ('headquarters', 'the main office of a company, where key decisions and research are usually based'),
        ('ethical consumer', 'a shopper who chooses products based on how fairly and sustainably they were produced'),
    ],
    'dates': [
        ('Tata, an Indian TNC, bought the British car maker Jaguar Land Rover', 2008),
        ('the Rana Plaza garment factory building collapsed in Bangladesh', 2013),
        ('the COVID-19 pandemic disrupted global supply chains', 2020),
        ('the Ever Given blocked the Suez Canal, delaying global shipping', 2021),
    ],
    'mcq': [
        ('Why do many TNCs locate factories in lower-income countries?', 'Labour and land are cheaper and there may be fewer regulations', ['Wages are much higher there', 'There are no workers there', 'Taxes are always higher there'], '[1]'),
        ('What happened at Rana Plaza in Dhaka, Bangladesh, on 24 April 2013?', 'A garment factory building collapsed, killing over 1100 workers', ['A new airport opened', 'A trade agreement was signed', 'A flood destroyed cotton fields'], '1134 deaths; it led to the Bangladesh Accord on Fire and Building Safety. [1]'),
        ('Where are most TNC headquarters and research and development centres located?', 'In high-income countries', ['In rural villages in low-income countries', 'On ships at sea', 'In Antarctica'], 'High-skill, high-pay activities stay near HQ. [1]'),
        ('Which of these is a benefit of a TNC for a host country?', 'New jobs and training for local workers', ['Profits sent back to the home country', 'Pollution from factories', 'Local firms forced out of business'], '[1]'),
        ('About what share of Bangladesh’s export earnings come from clothing?', 'Over 80%', ['About 5%', 'About 25%', 'About 50%'], 'Bangladesh is one of the largest garment exporters in the world. [1]'),
    ],
    'explain': [
        ('Explain two advantages and two disadvantages of TNCs for host countries.', 'Advantages: jobs, training, investment in infrastructure, tax revenue and exports. Disadvantages: low wages and poor conditions, profits sent abroad, pollution, local firms out-competed, the TNC may leave if costs rise.', '1 mark each point [4]'),
        ('Explain why the parts for a smartphone may be made in many different countries.', 'Companies use the cheapest or most skilled location for each stage: design in the USA, chips from Taiwan and South Korea, rare minerals from Africa and South America, assembly in China or India.', '1 mark specialisation/cost; 1 mark examples [2]'),
        ('Explain why long global supply chains can be risky.', 'A problem at one point – a pandemic, disaster, war or blocked canal – can stop production elsewhere, as in COVID-19 (2020) and the Suez blockage (2021); just-in-time systems have few spare stocks.', '1 mark one failure affects whole chain; 1 mark example [2]'),
        ('Explain how consumers can influence the behaviour of TNCs.', 'By choosing ethical or fair-trade brands, boycotting companies with poor records, using social media to expose problems and supporting campaigns, consumers can pressure TNCs to improve conditions.', '1 mark method; 1 mark how it creates pressure [2]'),
        ('Explain why some TNCs now come from emerging economies.', 'Countries such as India and China have grown rapidly, building large companies (e.g. Tata, Huawei) that invest overseas to reach new markets and buy brands and technology.', '1 mark growth; 1 mark example/reason [2]'),
    ],
    'claims': [
        ('All TNCs have their headquarters in Europe or North America.', False, 'Many large TNCs are based in Asia, e.g. Toyota (Japan), Samsung (South Korea), Tata (India) and Huawei (China).'),
        ('Factory jobs created by TNCs can be better paid than many local alternatives.', True, 'Wages are often low by world standards but may be higher than farm or informal work, which is one reason people take them.'),
        ('A product labelled “Made in China” was made entirely in China.', False, 'It may only have been assembled there from parts made in many other countries.'),
    ],
    'sources': [
        dict(prov='a statement by a garment worker in Dhaka, recorded by a trade union in 2014 (adapted)', kind='primary',
             text='After Rana Plaza, inspectors came to our factory and fire exits were added. But we still work ten hours a day, six days a week, and the wage is not enough for rent and food.',
             about='working conditions in global supply chains', infer='Safety improved after Rana Plaza, but long hours and low pay remained problems.',
             purpose='To support the union’s campaign for better wages and conditions.',
             plus='it is first-hand evidence from a worker in the industry', minus='a trade union may select statements that support its campaign',
             missing='The views of factory owners or the overall number of jobs created by the industry.', enq='the impact of TNCs on workers in lower-income countries'),
    ],
    'essays': [
        ('transnational companies bring more benefits than problems to lower-income countries',
         ['They create jobs and training, bring investment and technology, and earn export income (e.g. Bangladesh’s garment exports).'],
         ['Wages can be very low and conditions dangerous (Rana Plaza 2013).', 'Profits are sent abroad and TNCs may move if costs rise.', 'Pollution and loss of local firms.'],
         'TNCs can bring important benefits, but these depend on host-country regulation, workers’ rights and consumer pressure.',
         ['jobs and wages', 'safety', 'profits', 'regulation']),
        ('consumers are mainly responsible for improving conditions in global supply chains',
         ['Consumer choices and campaigns pushed brands to sign the Bangladesh Accord after Rana Plaza.'],
         ['Governments set and enforce labour laws.', 'TNCs control supply chains and prices.', 'Trade unions and NGOs press for change; many consumers cannot afford ethical products.'],
         'Consumers have influence, but governments and companies hold the greatest responsibility.',
         ['consumers', 'TNCs', 'governments', 'trade unions']),
    ],
})


@c9b.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c9b_chain(r, D):
    price = r.choice([20, 25, 30, 40, 50])
    shares = r.choice([[('retailer (shop)', 50), ('brand', 25), ('factory owner', 12), ('materials (cotton, fabric)', 9), ('transport and taxes', 3), ('factory worker’s wages', 1)],
                       [('retailer (shop)', 55), ('brand', 20), ('factory owner', 10), ('materials (cotton, fabric)', 11), ('transport and taxes', 3), ('factory worker’s wages', 1)]])
    stem = f'A study of a T-shirt sold for US${price} in Europe estimated how the price is shared: ' + ', '.join(f'{a} {b}%' for a, b in shares) + '.'
    w = [b for a, b in shares if 'worker' in a][0]
    ret = shares[0][1]
    if D == 1:
        opts, a = mcq(r, f'US${fmt(price * w / 100, 2)}', [f'US${fmt(price * ret / 100, 2)}', f'US${w}', f'US${fmt(price * 0.1, 2)}'])
        return {'stem': stem + ' How much of the price goes to the factory worker?', 'options': opts, 'answer': a, 'key': f'{w}% × {price} = {fmt(price * w / 100, 2)}. [1]'}
    parts = [
        lambda r: ('Calculate how much the retailer receives.', f'US${fmt(price * ret / 100, 2)}', f'{ret}% × {price} [1]'),
        lambda r: ('Calculate how much the factory worker receives.', f'US${fmt(price * w / 100, 2)}', f'{w}% × {price} [1]'),
        lambda r: ('Explain why such a small share goes to the factory worker.', 'Workers have little bargaining power: many people need jobs, trade unions are weak, and brands and retailers control prices and capture most of the value from design, marketing and selling.', '1 mark each point up to [3]'),
        lambda r: (f'If the worker’s share doubled, calculate the new price assuming every other share stays the same in money terms.', f'US${fmt(price * (1 + w / 100), 2)}', f'extra = {w}% of {price} = {fmt(price * w / 100, 2)} [2]'),
        lambda r: ('Suggest why the data should be used with caution.', 'It is an estimate for one product; shares vary between brands, countries and years; the study’s method and source are not given.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


c9c = T('Fair trade, inequality and development indicators', 'fair trade inequality development indicators')
build(c9c, {
    'who': 'a geographer',
    'terms': [
        ('development', 'improvement in people’s standard of living and quality of life, including wealth, health and education'),
        ('GDP per capita', 'the total value of goods and services produced by a country in a year divided by its population'),
        ('Human Development Index (HDI)', 'a UN measure of development from 0 to 1 combining life expectancy, education and income per person'),
        ('infant mortality rate', 'the number of babies who die before their first birthday per 1000 live births'),
        ('literacy rate', 'the percentage of adults who can read and write'),
        ('fair trade', 'a trading system that guarantees producers in poorer countries a minimum price and a premium to invest in their communities'),
        ('Fairtrade premium', 'extra money paid to Fairtrade producer groups to spend on community projects such as schools and clean water'),
        ('development gap', 'the difference in standards of living between the richest and poorest countries'),
        ('primary product', 'a raw material or crop, such as cocoa, coffee or copper, sold without being processed'),
    ],
    'dates': [
        ('the Brandt Report drew a line dividing the rich “North” from the poorer “South”', 1980),
        ('the UN published the first Human Development Index', 1990),
        ('the Fairtrade Mark was launched in the UK', 1994),
    ],
    'mcq': [
        ('Which three things does the Human Development Index combine?', 'Life expectancy, education and income per person', ['Population, area and rainfall', 'Exports, imports and debt', 'Birth rate, death rate and migration'], '[1]'),
        ('Which of these is a social indicator of development?', 'Literacy rate', ['GDP per capita', 'Value of exports', 'Number of banks'], 'Social indicators measure health, education and quality of life. [1]'),
        ('How does Fairtrade help farmers?', 'It guarantees a minimum price and pays a premium for community projects', ['It bans farmers from exporting', 'It sets the lowest possible price', 'It pays supermarkets more'], '[1]'),
        ('Why do countries that depend on exporting primary products often stay poor?', 'Prices are low and change a lot, while most profit is made by processing and selling', ['Primary products never sell', 'They are not allowed to export', 'Primary products are always very expensive'], '[1]'),
        ('Which country, together with Ghana, produces about 60% of the world’s cocoa?', 'Côte d’Ivoire', ['Switzerland', 'Belgium', 'Brazil'], 'Most chocolate profits are made in Europe and North America. [1]'),
        ('Kenya exports large quantities of which Fairtrade product, mainly grown around Lake Naivasha?', 'Cut flowers, especially roses', ['Wheat', 'Wool', 'Iron ore'], 'Much is flown to Europe. [1]'),
    ],
    'explain': [
        ('Explain why GDP per capita alone is not a good measure of development.', 'It is an average that hides inequality within a country; it does not measure health, education, freedom or environmental quality; informal economic activity is not counted.', '1 mark each point up to [3]'),
        ('Explain why the HDI is a better measure of development than GDP per capita.', 'It combines economic (income) and social measures (life expectancy and education), so it gives a broader picture of people’s quality of life.', '1 mark combines measures; 1 mark broader picture [2]'),
        ('Explain how Fairtrade can benefit farming communities, using an example.', 'The minimum price protects farmers when world prices fall; the premium is spent democratically on projects – e.g. Kenyan Fairtrade flower farms have funded schools, clinics and clean water.', '1 mark minimum price; 1 mark premium; 1 mark example [3]'),
        ('Explain two limitations of Fairtrade.', 'Only a small share of trade is Fairtrade; certification costs are high for small farmers; products cost more, so not all consumers buy them; workers on certified farms may still earn low wages; flying products long distances adds emissions.', '2 marks each [4]'),
        ('Explain two reasons for the development gap between countries.', 'Historical factors (colonialism, dependence on primary exports); physical factors (landlocked, hazards, climate, disease); economic factors (debt, unfair trade terms); political factors (conflict, corruption).', '2 marks each [4]'),
    ],
    'claims': [
        ('A country with a high GDP per capita must have a high quality of life for everyone.', False, 'GDP per capita is an average; wealth may be very unequally shared and health or freedoms may still be poor.'),
        ('A higher infant mortality rate usually indicates a lower level of development.', True, 'It reflects poor health care, nutrition, clean water and sanitation.'),
        ('Fairtrade guarantees that products cost the same as ordinary ones.', False, 'Fairtrade products often cost slightly more because farmers receive a minimum price and premium.'),
        ('Kenyan roses flown to Europe always have a bigger carbon footprint than roses grown in Europe.', False, 'Some studies found roses from heated Dutch greenhouses produced more emissions than Kenyan roses grown in natural sunlight, even including the flight.'),
    ],
    'sources': [
        dict(prov='a statement by a worker on a Fairtrade flower farm near Lake Naivasha, Kenya, published by a Fairtrade organisation in 2019 (adapted)', kind='primary',
             text='The premium from our roses has built a nursery school and a clinic for our families. Before, we had to walk two hours to see a nurse.',
             about='the benefits of Fairtrade', infer='The Fairtrade premium has improved health care and education in the workers’ community.',
             purpose='To show the benefits of Fairtrade and encourage consumers to buy Fairtrade products.',
             plus='it is first-hand evidence from a worker who has seen the changes', minus='it was published by a Fairtrade organisation, which has an interest in presenting positive stories',
             missing='Wage levels, environmental concerns such as water use from Lake Naivasha, or the views of non-Fairtrade farms.', enq='whether fair trade reduces inequality'),
    ],
    'essays': [
        ('fair trade is the best way to reduce inequality between countries',
         ['Guaranteed minimum prices and premiums improve farmers’ incomes, schools and health care (e.g. Kenyan flower farms).'],
         ['Fairtrade is a small share of world trade.', 'Processing products locally, investment, education, debt relief and fairer trade rules may have bigger effects.', 'Good governance and reducing conflict matter.'],
         'Fair trade helps specific communities but cannot on its own close the development gap.',
         ['minimum prices', 'scale of fair trade', 'trade rules', 'investment and aid']),
        ('the Human Development Index is the best way to measure development',
         ['It combines health, education and income, giving a broad picture.'],
         ['It ignores inequality, freedom, gender and the environment; national averages hide regional differences.', 'Other measures (e.g. the Multidimensional Poverty Index, Gender Inequality Index) add detail.'],
         'The HDI is a good single measure, but development is best measured with several indicators.',
         ['life expectancy', 'education', 'income', 'inequality']),
    ],
})


@c9c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def c9c_indic(r, D):
    cs = r.sample([('Norway', 0.966, 83, 2, 99), ('Japan', 0.920, 84, 2, 99), ('Brazil', 0.760, 76, 13, 94), ('India', 0.644, 72, 26, 76),
                   ('Kenya', 0.601, 63, 31, 83), ('Nepal', 0.601, 70, 22, 71), ('Niger', 0.394, 62, 60, 38)], 3)
    stem = 'Development indicators (approximate, early 2020s) – HDI, life expectancy (years), infant mortality (per 1000 live births), adult literacy (%): ' + '; '.join(f'{c[0]} {c[1]}, {c[2]}, {c[3]}, {c[4]}' for c in cs) + '.'
    best = max(cs, key=lambda c: c[1])
    worst = min(cs, key=lambda c: c[1])
    if D == 1:
        opts, a = mcq(r, best[0], [c[0] for c in cs if c is not best] + ['They are all equal'])
        return {'stem': stem + ' Which country has the highest level of development according to the HDI?', 'options': opts, 'answer': a, 'key': f'{best[0]} (HDI {best[1]}). [1]'}
    parts = [
        lambda r: ('Calculate the difference in life expectancy between the countries with the highest and lowest HDI.', f'{best[2] - worst[2]} years', f'{best[2]} − {worst[2]} [1]'),
        lambda r: ('Describe the relationship between HDI and infant mortality shown in the table.', 'Countries with a higher HDI have lower infant mortality (negative relationship): ' + ', '.join(f'{c[0]} {c[3]}' for c in sorted(cs, key=lambda c: -c[1])) + '.', '1 mark relationship; 1 mark data [2]'),
        lambda r: ('Explain why infant mortality is higher in countries with a low HDI.', 'Less access to doctors, midwives, vaccinations, clean water, sanitation and good nutrition for mothers and babies.', '1 mark each reason up to [3]'),
        lambda r: ('Suggest one other indicator that would help compare these countries, and explain why.', 'GNI per capita (wealth), percentage with access to clean water, doctors per 1000 people, or gender inequality – each adds a different aspect of quality of life.', '1 mark indicator; 1 mark reason [2]'),
        lambda r: (f'Calculate how many times higher the infant mortality rate is in {worst[0]} than in {best[0]}.', f'{fmt(worst[3] / best[3], 1)} times', f'{worst[3]} ÷ {best[3]} [1]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


@c9c.add('C3', (2, 3, 4, 5), 'numerical')
def c9c_fair(r, D):
    kg = r.choice([20000, 40000, 50000, 80000, 100000])
    world = r.choice([1.6, 1.8, 2.0, 2.2])
    minp = 2.4
    prem = r.choice([0.2, 0.25, 0.3])
    prod = r.choice(['coffee', 'cocoa beans'])
    paid = max(world, minp)
    stem = (f'A farmers’ cooperative sells {kg:,} kg of Fairtrade {prod}. The world market price is US${fmt(world, 2)} per kg. The Fairtrade minimum price is US${fmt(minp, 2)} per kg '
            f'and the Fairtrade premium is US${fmt(prem, 2)} per kg.').replace(',', ' ')
    parts = [
        lambda r: ('Calculate the income from selling at the world market price.', f'US${fmt(kg * world, 0)}', f'{kg} × {fmt(world, 2)} [1]'),
        lambda r: ('Calculate the income from selling at the Fairtrade minimum price.', f'US${fmt(kg * paid, 0)}', f'{kg} × {fmt(paid, 2)} (minimum price applies because the world price is lower) [1]'),
        lambda r: ('Calculate the total Fairtrade premium paid to the cooperative.', f'US${fmt(kg * prem, 0)}', f'{kg} × {fmt(prem, 2)} [1]'),
        lambda r: ('Calculate the total extra income from Fairtrade compared with the world price.', f'US${fmt(kg * (paid - world + prem), 0)}', f'{kg} × ({fmt(paid, 2)} − {fmt(world, 2)} + {fmt(prem, 2)}) [2]'),
        lambda r: ('Suggest two ways the cooperative could use the premium.', 'Build a school or clinic; provide clean water; buy equipment to process crops locally; train farmers in better methods.', '1 mark each [2]'),
    ]
    return compose(r, stem, parts, k=(2, 3) if D <= 3 else (3, 4), type_='numerical')


SDGS = ['No poverty', 'Zero hunger', 'Good health and well-being', 'Quality education', 'Gender equality', 'Clean water and sanitation', 'Affordable and clean energy',
        'Decent work and economic growth', 'Industry, innovation and infrastructure', 'Reduced inequalities', 'Sustainable cities and communities', 'Responsible consumption and production',
        'Climate action', 'Life below water', 'Life on land', 'Peace, justice and strong institutions', 'Partnerships for the goals']

c9d = T('The UN Sustainable Development Goals and taking action', 'un sustainable development goals taking action')
build(c9d, {
    'who': 'a geographer',
    'terms': [
        ('sustainable development', 'development that meets the needs of the present without compromising the ability of future generations to meet their own needs'),
        ('Sustainable Development Goals', 'the 17 goals adopted by all UN member states in 2015 to be achieved by 2030'),
        ('Millennium Development Goals', 'the eight UN goals set in 2000 to reduce poverty and improve lives by 2015'),
        ('extreme poverty', 'living on less than the international poverty line set by the World Bank, unable to meet basic needs'),
        ('target', 'a specific, measurable aim within a goal; the SDGs have 169 targets'),
        ('indicator', 'a measurement used to track progress towards a target'),
        ('three pillars of sustainability', 'the economic, social and environmental parts of sustainable development'),
    ],
    'dates': [
        ('the Brundtland Report defined sustainable development', 1987),
        ('the Earth Summit was held in Rio de Janeiro', 1992),
        ('the Millennium Development Goals were adopted', 2000),
        ('the Sustainable Development Goals were adopted by the UN', 2015),
    ],
    'mcq': [
        ('How many Sustainable Development Goals are there?', '17', ['8', '10', '30'], '17 goals and 169 targets. [1]'),
        ('By which year are the SDGs meant to be achieved?', '2030', ['2020', '2050', '2100'], 'They are also called Agenda 2030. [1]'),
        ('Which goals did the SDGs replace?', 'The Millennium Development Goals', ['The Paris Agreement', 'The Kyoto Protocol', 'The Universal Declaration of Human Rights'], 'MDGs: 8 goals, 2000-2015. [1]'),
        ('Which is a key difference between the SDGs and the MDGs?', 'The SDGs apply to all countries, rich and poor, not just developing countries', ['The SDGs have fewer goals', 'The SDGs ignore the environment', 'The SDGs end in 2015'], '[1]'),
        ('Which report first gave the widely used definition of sustainable development in 1987?', 'The Brundtland Report', ['The Brandt Report', 'The Chadwick Report', 'The Casement Report'], '[1]'),
    ],
    'explain': [
        ('Explain what is meant by the three pillars of sustainable development, with an example of each.', 'Economic (decent jobs and growth, e.g. SDG 8), social (health, education and equality, e.g. SDGs 3, 4, 5) and environmental (protecting climate, land and oceans, e.g. SDGs 13-15); sustainable development balances all three.', '1 mark each pillar with example [3]'),
        ('Explain why the SDGs are linked to each other.', 'Progress on one helps others: e.g. clean water (SDG 6) improves health (SDG 3) and lets girls attend school instead of collecting water (SDGs 4 and 5); climate action (SDG 13) protects food production (SDG 2).', '1 mark link; 1 mark example [2]'),
        ('Explain two reasons why progress towards the SDGs has been slow in some countries.', 'Conflict, the COVID-19 pandemic, debt, climate-related disasters, rising food and energy prices, corruption and lack of funding have slowed or reversed progress.', '2 marks each [4]'),
        ('Explain how young people can take action to support the SDGs.', 'Reduce waste and energy use; campaign and raise awareness; volunteer locally; support fair-trade and sustainable products; take part in school eco-councils or projects linked to specific goals.', '1 mark each action, explained [3]'),
    ],
    'claims': [
        ('The SDGs only apply to low-income countries.', False, 'They are universal and apply to every country, including high-income countries.'),
        ('Clean water and sanitation is one of the 17 SDGs.', True, 'It is SDG 6.'),
        ('Sustainable development means stopping all economic growth.', False, 'It means growth and development that balance economic, social and environmental needs for present and future generations.'),
    ],
    'essays': [
        ('the Sustainable Development Goals are too ambitious to be achieved by 2030',
         ['UN reports show many targets are off track; COVID-19, conflict and climate change have reversed progress on poverty and hunger.'],
         ['Goals set direction and focus funding; some targets (e.g. electricity access, child mortality) have improved significantly.', 'Ambitious goals inspire action by governments, businesses and citizens.'],
         'Many goals will probably not be fully met by 2030, but they remain valuable as a shared plan for action.',
         ['progress so far', 'COVID-19 and conflict', 'funding', 'value of targets']),
        ('governments, not individuals, should take the lead in achieving the SDGs',
         ['Governments control laws, budgets and international agreements, and can act at large scale.'],
         ['Businesses, NGOs, communities and individuals also make a difference, e.g. reducing waste, campaigning, volunteering.', 'Many local projects are led by communities.', 'Individual pressure pushes governments to act.'],
         'Governments must lead, but the goals need action at every level.',
         ['government policy', 'businesses', 'communities', 'individual actions']),
    ],
})


@c9d.add('C1', (1, 2, 3), 'mcq')
def c9d_number(r, D):
    i = r.randrange(17)
    if r.random() < 0.5:
        opts, a = mcq(r, SDGS[i], [g for j, g in enumerate(SDGS) if j != i])
        return {'stem': f'Which Sustainable Development Goal is SDG {i + 1}?', 'options': opts, 'answer': a, 'key': f'SDG {i + 1}: {SDGS[i]}. [1]'}
    opts, a = mcq(r, f'SDG {i + 1}', [f'SDG {j + 1}' for j in range(17) if j != i])
    return {'stem': f'Which number is the Sustainable Development Goal “{SDGS[i]}”?', 'options': opts, 'answer': a, 'key': f'SDG {i + 1}: {SDGS[i]}. [1]'}


@c9d.add('C3', (1, 2, 3, 4, 5), 'case')
def c9d_project(r, D):
    proj = r.choice([
        ('a village in Nepal installs solar panels on the school roof and in homes', [7, 4, 13], 'Affordable and clean energy'),
        ('a community in Kenya builds a rainwater harvesting tank and toilets at the primary school', [6, 3, 4], 'Clean water and sanitation'),
        ('a city in Colombia builds cable cars linking hillside neighbourhoods to the metro', [11, 10, 8], 'Sustainable cities and communities'),
        ('women farmers in Bangladesh receive training and small loans to grow and sell vegetables', [5, 1, 2], 'Gender equality'),
        ('a coastal town in the Philippines replants mangroves and creates a marine protected area', [14, 13, 15], 'Life below water'),
        ('a school in Mexico starts a campaign to cut plastic waste and compost canteen food', [12, 13, 4], 'Responsible consumption and production'),
    ])
    main = proj[1][0]
    if D == 1:
        opts, a = mcq(r, f'SDG {main}: {SDGS[main - 1]}', [f'SDG {j + 1}: {SDGS[j]}' for j in range(17) if j + 1 not in proj[1]])
        return {'stem': f'In a development project, {proj[0]}. Which SDG does this project most directly support?', 'options': opts, 'answer': a, 'key': f'SDG {main}: {SDGS[main - 1]}. [1]'}
    others = ', '.join(f'SDG {g} ({SDGS[g - 1]})' for g in proj[1][1:])
    n = r.choice([200, 350, 500, 800])
    cost = r.choice([10000, 15000, 24000, 40000])
    parts = [
        lambda r: ('Identify the SDG that this project most directly supports.', f'SDG {main}: {SDGS[main - 1]}', '[1]'),
        lambda r: ('Explain how the project could also help to achieve two other SDGs.', f'It links to {others}: e.g. better services improve health, education or the environment.', '1 mark each linked goal, explained [2]'),
        lambda r: (f'The project costs US${cost:,} and benefits {n} people. Calculate the cost per person.'.replace(',', ' '), f'US${fmt(cost / n, 2)}', f'{cost} ÷ {n} [1]'),
        lambda r: ('Explain why community involvement is important for the project to be sustainable.', 'Local people understand their needs, will maintain and repair the project, and feel ownership, so it continues after outside funding ends.', '1 mark ownership/maintenance; 1 mark long-term [2]'),
        lambda r: ('Evaluate whether small local projects can make a real difference to global goals.', 'They improve many lives directly and can be copied elsewhere (scaled up); but global goals also need national policies and international funding. Many small projects together make a large difference.', '1 mark for; 1 mark against; 1 mark judgement [3]'),
    ]
    return compose(r, f'In a development project, {proj[0]}.', parts, k=(2, 3) if D <= 3 else (3, 4), type_='case')


CHAPTERS[9] = [c9a, c9b, c9c, c9d]


# ============================================================== extra essays for topics with fewer C4 items
add_essay(c1c, 'grid references are the most important map skill for a geographer',
          ['They give precise locations, so features can be found, recorded and shared accurately.'],
          ['Scale and distance are needed to plan routes and compare sizes.', 'Reading contours shows relief, which matters for hazards, farming and walking routes.', 'Direction and bearings are essential for navigation.'],
          'Grid references are essential, but they are most useful combined with scale, direction and relief.',
          ['scale', 'contours and relief', 'direction'])
add_essay(c5a, 'the theory of plate tectonics explains where most of the world’s earthquakes, volcanoes and mountains are found',
          ['Most earthquakes and volcanoes lie along plate boundaries such as the Ring of Fire; fold mountains such as the Himalayas and Andes form where plates converge.'],
          ['Hotspots such as Hawaii form volcanoes in the middle of plates.', 'Some earthquakes happen away from boundaries, along old faults or because of human activity such as mining.'],
          'Plate tectonics explains the great majority of these features, with hotspots and intraplate earthquakes as exceptions.',
          ['plate boundaries', 'hotspots', 'intraplate earthquakes'])
add_essay(c6a, 'accurate weather measurement is more important to people today than ever before',
          ['Forecasts protect lives from storms, floods and heatwaves, which are becoming more frequent with climate change.', 'Aviation, shipping, farming and energy supply depend on accurate data.'],
          ['People have always depended on the weather, especially farmers in the past.', 'Technology now makes measurement easier, so its importance has not necessarily grown.'],
          'Weather data matters more today because of climate change, global travel and dense populations in hazardous places.',
          ['extreme weather', 'farming and transport', 'climate change'])
add_essay(c6c, 'climate graphs are the most useful way to compare the climates of different places',
          ['They show temperature and precipitation for every month, so ranges, totals and seasons can be compared quickly.'],
          ['Maps of climate zones show global patterns better.', 'Graphs show averages and hide extremes, wind, sunshine and humidity.', 'Written descriptions and photographs show how climate affects people.'],
          'Climate graphs are very useful for comparing two places, but other sources are needed for a full picture.',
          ['temperature and precipitation', 'extremes', 'climate maps'])
add_essay(c7a, 'population density tells us more than total population about the pressure on a country’s resources',
          ['Density shows how crowded land is, e.g. Bangladesh and Singapore compared with Australia or Canada.'],
          ['Density is an average that hides uneven distribution (e.g. Egypt along the Nile).', 'Resources, technology and wealth matter: Singapore is very dense but wealthy, while some sparsely populated areas struggle.', 'Total population shows overall demand for food, energy and jobs.'],
          'Density is helpful, but pressure on resources depends on how people are distributed and how resources are used.',
          ['uneven distribution', 'wealth and technology', 'demand for resources'])
add_essay(c7d, 'urbanisation in lower-income countries is caused more by rural push factors than by urban pull factors',
          ['Poverty, lack of land, drought, conflict and mechanisation force many people to leave rural areas.'],
          ['Cities attract migrants with jobs, higher wages, education and health care.', 'Natural increase within cities is also a major cause of growth.', 'Push and pull factors usually work together.'],
          'Both matter; push factors often start migration, but pull factors decide where people go, and natural increase adds to growth.',
          ['rural poverty', 'jobs in cities', 'natural increase'])
