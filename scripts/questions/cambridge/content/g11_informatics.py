"""Cambridge International AS Level Information Technology 9626 (syllabus topics 1-11), grade 11.

Paper 1 (Theory) style structured and multiple-choice items and Paper 2 (Practical) style tasks:
validation, check digits, batch totals, master-file updates, encryption, data logging, control
algorithms, flowchart/pseudocode tracing, licensing costs, transfer times, page layout, database
queries and validation rules, spreadsheet formulae (relative/absolute referencing, IF, VLOOKUP,
HLOOKUP, COUNTIF, SUMIF), goal seek, chart construction and sound/video file sizes. Every computed
answer is produced by the code that builds the stem.

Each topic is built from a content spec by `T()`, which registers generic templates (definitions,
recall MCQs, explain items, assertion-reason, advantage/disadvantage in context, structured
scenario questions and evaluative essays); topics add parameterised templates with computed answers.
"""
import math
import re

from ._lib import topic, mcq, compose, CTX, PEOPLE, CITIES
from .g11_computer_science import MCQ, Q, code, fill, finalize, PC_GENS, IND  # noqa: F401

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

ORGS = [('Riverside Medical Centre', 'medical centre'), ('BlueWave Supermarkets', 'supermarket chain'), ('Northfield Academy', 'school'),
        ('Harbour Bank', 'bank'), ('SkyLink Airways', 'airline'), ('City Central Library', 'library'), ('SwiftCar Rentals', 'car rental company'),
        ('Starlight Cinemas', 'cinema chain'), ('Palm Grove Hotel', 'hotel'), ('TransGlobal Logistics', 'logistics company'),
        ('Eagles Sports Club', 'sports club'), ('GreenLeaf Pharmacy', 'pharmacy'), ('Summit Engineering', 'engineering firm'),
        ('Coral Bay Aquarium', 'aquarium'), ('MetroBus', 'bus company'), ('Sunrise Bakery', 'bakery'), ('Orbit Games Studio', 'games studio'),
        ('Lakeside College', 'college'), ('Pioneer Insurance', 'insurance company'), ('FreshFarm Foods', 'food producer'),
        ('Nova Telecom', 'telecommunications company'), ('Atlas Museum', 'museum'), ('Peak Fitness', 'gym chain'), ('Horizon Travel', 'travel agency'),
        ('Kestrel Architects', 'architecture practice'), ('Lotus Fashion', 'clothing retailer'), ('Delta Water Utility', 'water company'),
        ('Silverline Couriers', 'courier company'), ('Meridian Hospital', 'hospital'), ('Vista Estate Agents', 'estate agency')]


def art(w):
    return ('an ' if w[0].lower() in 'aeiou' else 'a ') + w


def ctx(r):
    p, q = r.sample(PEOPLE, 2)
    (o, ot), (o2, ot2) = r.sample(ORGS, 2)
    c, c2 = r.sample(CITIES, 2)
    return {'p': p, 'q': q, 'org': o, 'otype': ot, 'aot': art(ot), 'org2': o2, 'otype2': ot2, 'city': c, 'city2': c2}


def cap(s):
    s = s.strip()
    return s[0].upper() + s[1:] + ('' if s.endswith(('.', '?', '!')) else '.')


def num(x, dp=2):
    if isinstance(x, int):
        return f'{x:,}'
    s = f'{x:,.{dp}f}'
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s


def money(x, sym='$', dp=2):
    s = f'{abs(x):,.{dp}f}'
    if dp and s.endswith('.00'):
        s = s[:-3]
    return ('−' if x < 0 else '') + sym + s


def nearest(want, allowed, default):
    if want and want >= min(allowed) - 1:
        return min(allowed, key=lambda m: (abs(m - want), m))
    return default


def opts_from(r, ans, pool, k=3):
    ds = [x for x in dict.fromkeys(pool) if x != ans]
    if len(ds) < k:
        return None
    return mcq(r, ans, r.sample(ds, k))


DEFS = {}
AR_OPTS = ['Both A and R are true, and R is the correct explanation of A',
           'Both A and R are true, but R is not the correct explanation of A',
           'A is true but R is false', 'A is false but R is true']


def _mk(key):
    m = re.findall(r'\[(\d+)\]', key)
    return int(m[-1]) if m else 2


def _part(p, d):
    if callable(p):
        return lambda rr, p=p: p(rr, d)
    return lambda rr, p=p: (fill(p[0], d), fill(p[1], d), fill(p[2], d))


def essay_q(r, D, d, task, pro, con, concl, scene):
    m = nearest(CTX.get('want_marks'), (4, 6, 8, 10), {2: 4, 3: 6, 4: 8, 5: 10}[min(5, max(2, D))])
    forms = ['Evaluate {t}.', 'Discuss {t}.'] + ([] if task.startswith(('whether', 'how far')) else ['Assess {t}.'])
    form = r.choice(forms)
    stem = fill(scene, d) + ' ' + form.replace('{t}', fill(task, d))
    pro, con, concl = fill(pro, d), fill(con, d), fill(concl, d)
    ans = f'Points for: {pro} Points against / limitations: {con} Conclusion: {concl}'
    lv = {4: '1-2 marks basic points; 3-4 marks points developed and applied with a conclusion',
          6: '1-2 marks basic points; 3-4 marks developed points on one or both sides; 5-6 marks balanced, applied discussion with a justified conclusion',
          8: '1-2 marks limited points; 3-5 marks developed points on both sides applied to the scenario; 6-8 marks balanced, well-applied discussion with a reasoned conclusion',
          10: '1-3 marks limited points; 4-6 marks developed points on both sides; 7-10 marks detailed, balanced discussion applied to the scenario with a substantiated conclusion'}[m]
    key = f'Levels marking: {lv}. Indicative content — for: {pro} Against: {con} Conclusion may argue: {concl} [{m}]'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'long', 'marks': m}


def T(ch, name, *keys, defs=(), mcqs=(), exps=(), ars=(), falses=(), adv=(), intros=(), parts=(), ev=(), parts4=(), registry=None):
    """Build a topic from a content spec and register its generic templates.

    defs   [(term, definition)]                       -> C1 define / MCQ items
    mcqs   [(stem, answer, [distractors], why)]       -> C1 MCQs
    exps   [(stem, answer, key with [n])]             -> C2 explain items (auto-paired)
    ars    [(assertion, reason that explains it)], falses [false statements] -> C2 assertion-reason
    adv    [(concept, [advantages], [disadvantages])] -> C2 advantage/disadvantage in context
    intros, parts                                     -> C3 structured scenario questions
    ev     [(task, for, against, conclusion)]         -> C4 essays and C4 structured questions (with parts4)
    """
    CH_, DEFS_ = registry or (CHAPTERS, DEFS)
    t = topic(name, name, *keys)
    t.ch = ch
    CH_.setdefault(ch, []).append(t)
    DEFS_.setdefault(ch, []).extend(defs)
    t.defs, t.intros, t.parts, t.ev, t.parts4 = list(defs), list(intros), list(parts), list(ev), list(parts4)

    if defs:
        ents = []
        for i, (term, dd) in enumerate(defs):
            stem = (f"Define the term '{term}'.", f"State what is meant by '{term}'.", f"Explain what is meant by the term '{term}'.")[i % 3]
            ents.append((stem, dd, f'1 mark: the key idea; 1 mark: further detail or a correct example. Model: {dd} [2]'))
        t.fixed('C1', (1, 2, 3), ents, type='short')

        @t.add('C1', (1, 2), 'mcq')
        def def_mcq(r, D):
            term, dd = r.choice(t.defs)
            others = [x[1] for x in DEFS_[ch] if x[0] != term and x[1] != dd]
            if len(others) < 3:
                return None
            opts, ans = mcq(r, dd, r.sample(others, 3))
            return {'stem': f"Which statement best describes '{term}'?", 'options': opts, 'answer': ans, 'key': f'{term}: {dd}', 'marks': 1}

        @t.add('C1', (1, 2, 3), 'mcq')
        def def_rev(r, D):
            term, dd = r.choice(t.defs)
            others = [x[0] for x in DEFS_[ch] if x[0] != term]
            if len(others) < 3:
                return None
            opts, ans = mcq(r, term, r.sample(others, 3))
            return {'stem': f'Which term is described here? "{dd}"', 'options': opts, 'answer': ans, 'key': f'This describes {term}.', 'marks': 1}

    for (stem, a, dis, why) in mcqs:
        def fn(r, D, stem=stem, a=a, dis=dis, why=why):
            d = ctx(r)
            q = MCQ(r, fill(stem, d), fill(a, d), [fill(x, d) for x in dis], f'{fill(a, d)}. {fill(why, d)}')
            return q
        fn.__name__ = 'mcq_fixed'
        t.add('C1', (1, 2, 3), 'mcq')(fn)

    if exps:
        t.fixed('C2', (2, 3, 4), list(exps), type='explain')

    if len(defs) >= 2:
        @t.add('C2', (1, 2, 3), 'explain')
        def distinguish(r, D):
            (a, da), (b, db) = r.sample(t.defs, 2)
            lead = r.choice(['Distinguish between', 'Describe the difference between', 'Explain the difference between'])
            return {'stem': f"{lead} '{a}' and '{b}'.", 'answer': f'{a}: {da} {b}: {db}',
                    'key': f'1 mark: {a} correctly described; 1 mark: {b} correctly described (a comparison is needed for full marks). [2]', 'marks': 2, 'type': 'explain'}

    if len(ars) >= 2 and falses:
        @t.add('C2', (2, 3), 'mcq')
        def ar(r, D):
            case = r.randrange(4)
            i = r.randrange(len(ars))
            if case == 0:
                a, rr = ars[i]
            elif case == 1:
                j = r.choice([x for x in range(len(ars)) if x != i])
                a, rr = ars[i][0], ars[j][1]
            elif case == 2:
                a, rr = ars[i][0], r.choice(falses)
            else:
                a, rr = r.choice(falses), ars[i][1]
            key = {0: 'A is true and R explains why A is true.', 1: 'A and R are both true statements, but R does not explain A.',
                   2: f'A is true; R is false: "{rr}" is incorrect.', 3: f'A is false: "{a}" is incorrect; R is a true statement.'}[case]
            return {'stem': f'Assertion (A): {a} Reason (R): {rr} Which option is correct?', 'options': list(AR_OPTS), 'answer': AR_OPTS[case], 'key': key, 'marks': 1}

    if adv:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def adv_ctx(r, D):
            d = ctx(r)
            concept, pro, con = r.choice(adv)
            concept = fill(concept, d)
            pro = [fill(x, d) for x in pro]
            con = [fill(x, d) for x in con]
            lead = r.choice([f"{d['org']}, {d['aot']} in {d['city']}, is considering {concept}.", f"The manager of {d['org']} in {d['city']} wants to introduce {concept}.",
                             f"{d['p']} works for {d['org']}, {d['aot']} in {d['city']}, which plans to start {concept}."])
            v = r.randrange(2)
            if D <= 2:
                if v == 0:
                    q, a, k, m = 'Explain one advantage to the organisation of this.', cap(pro[0]), f'1 mark: advantage identified, e.g. {"; ".join(pro)}. 1 mark: explained in context. [2]', 2
                else:
                    q, a, k, m = 'Explain one disadvantage to the organisation of this.', cap(con[0]), f'1 mark: disadvantage identified, e.g. {"; ".join(con)}. 1 mark: explained in context. [2]', 2
            elif D == 3:
                q = 'Explain one advantage and one disadvantage of this for the organisation.' if v == 0 else 'Explain two drawbacks of this for the organisation.'
                a = f'Advantage: {pro[0]}. Disadvantage: {con[0]}.' if v == 0 else f'{cap(con[0])} {cap(con[1 % len(con)])}'
                k, m = f'2 × (1 mark point, 1 mark explanation). Advantages: {"; ".join(pro)}. Disadvantages: {"; ".join(con)}. [4]', 4
            else:
                q = 'Explain two benefits of this for the organisation and one problem it may cause.' if v == 0 else 'Explain two advantages and two disadvantages of this for the organisation.'
                m = 5 if v == 0 else 6
                a = f'Benefits: {pro[0]}; {pro[1 % len(pro)]}. Problem: {con[0]}.' if v == 0 else f'Advantages: {pro[0]}; {pro[1 % len(pro)]}. Disadvantages: {con[0]}; {con[1 % len(con)]}.'
                k = f'Up to {m} marks: 1 mark per valid point plus explanation in context. Advantages: {"; ".join(pro)}. Disadvantages: {"; ".join(con)}. [{m}]'
            return {'stem': f'{lead} {q}', 'answer': a, 'key': k, 'type': 'explain', 'marks': m}

    if intros and parts:
        @t.add('C3', (1, 2, 3, 4, 5), 'case')
        def scen3(r, D):
            d = ctx(r)
            k = (1, 2) if D <= 1 else ((2, 3) if D <= 3 else (3, 4))
            return compose(r, fill(r.choice(t.intros), d), [_part(p, d) for p in t.parts], k=k, type_='case')

    if ev and intros:
        @t.add('C4', (3, 4, 5), 'long')
        def essay(r, D):
            d = ctx(r)
            task, pro, con, concl = r.choice(t.ev)
            return essay_q(r, D, d, task, pro, con, concl, r.choice(t.intros))

        @t.add('C4', (2, 3, 4, 5), 'multi_step')
        def struct4(r, D):
            d = ctx(r)
            task, pro, con, concl = r.choice(t.ev)
            ps = [_part(p, d) for p in (t.parts4 or t.parts)]
            em = 6 if D >= 4 else 4
            ev_txt = fill(task, d)
            ev_txt = ev_txt[0].upper() + ev_txt[1:]
            ps.append(lambda rr: (('Evaluate ' if not ev_txt.lower().startswith(('whether', 'how far')) else 'Discuss ') + ev_txt[0].lower() + ev_txt[1:] + '.',
                                  f'For: {fill(pro, d)} Against: {fill(con, d)} Conclusion: {fill(concl, d)}',
                                  f'Up to {em // 2} marks for points on each side applied to the scenario; 1 further mark requires a justified conclusion. [{em}]'))
            return compose(r, fill(r.choice(t.intros), d), ps, k=(3,) if D <= 3 else (3, 4), type_='multi_step')
    return t


def tbl(header, rows):
    """Plain-text table: header list and rows of values."""
    return code([' | '.join(header)] + [' | '.join(str(x) for x in row) for row in rows])


_MKE = re.compile(r'\[(\d+)\]\s*$')


def finish(chapters):
    """Clamp D into each template's declared range (borrowed templates may be called outside it) and
    give single-part items marks equal to the trailing [n] of their key."""
    for tps in chapters.values():
        for tp in tps:
            for tpl in tp.templates:
                if getattr(tpl, '_fin', False):
                    continue
                tpl._fin = True
                f = tpl.fn

                def g(r, D, f=f, lo=min(tpl.D), hi=max(tpl.D)):
                    q = f(r, max(lo, min(hi, D)))
                    if q and 'marks' not in q:
                        if q.get('options'):
                            q['marks'] = 1
                        else:
                            m = _MKE.search(q['key'])
                            if m:
                                q['marks'] = int(m.group(1))
                    return q
                tpl.fn = g


# =============================================================================== Chapter 1 Data processing and information
SOURCES = [
    ('a sports coach records the time each athlete takes to run 400 m using a stopwatch', 'direct'),
    ('a shop owner uses government census figures to estimate the number of teenagers in the town', 'indirect'),
    ('a student hands out a questionnaire she wrote to classmates about their sleep', 'direct'),
    ('a travel company buys a list of email addresses from a marketing firm', 'indirect'),
    ('a scientist places a data logger with a temperature sensor in a river for a week', 'direct'),
    ('a bank uses a credit reference agency\'s records to decide whether to lend money', 'indirect'),
    ('a traffic officer counts the cars passing a junction between 8:00 and 9:00', 'direct'),
    ('a researcher uses weather data published by the national meteorological office', 'indirect'),
    ('a journalist interviews residents about a new bus route', 'direct'),
    ('a politician uses the electoral register to send leaflets to voters', 'indirect'),
    ('a supermarket uses loyalty-card data, collected to give discounts, to decide where to open a new store', 'indirect'),
    ('a teacher observes pupils in a lesson and notes how often they ask questions', 'direct'),
    ('an estate agent uses house prices published on a property website', 'indirect'),
    ('a factory manager reads the output of a sensor counting items on a conveyor belt', 'direct'),
    ('a charity uses a report written by another charity five years ago', 'indirect'),
]

t = T(1, 'Data, information and knowledge; direct and indirect data sources', 'data, information and knowledge', 'direct and indirect data sources',
      defs=[('data', 'Raw facts and figures, such as numbers, characters or symbols, that have no context and so no meaning on their own.'),
            ('information', 'Data that has been processed and given context, so that it has meaning and is useful.'),
            ('knowledge', 'Information that has been understood and combined with experience so that it can be applied, for example to make decisions.'),
            ('direct data source', 'Data that is collected first-hand by the person or organisation that will use it, for the specific purpose it is needed for.'),
            ('indirect data source', 'Data that was collected by someone else, or for a different purpose, and is then used second-hand (e.g. census data, the electoral register).')],
      mcqs=[('Which of these is data rather than information?', '17, 21, 19, 24', ['Maximum temperature in {city} on 3 May: 24 °C', 'Test mark for {p} out of 30: 21', 'Number of customers at {org} on Monday: 17'],
             'A list of numbers with no context has no meaning, so it is data.'),
            ('{p} designs a questionnaire and gives it to 50 shoppers. What type of data source is this?', 'A direct data source', ['An indirect data source', 'A secondary source bought from a third party', 'A knowledge base'],
             'The data is collected first-hand by the person who will use it, for that purpose.'),
            ('Which of these is an indirect data source for a company planning a new store?', 'Government census data on local population', ['A survey the company carries out in the area', 'Counting pedestrians outside the proposed site', 'Interviews with local residents by company staff'],
             'Census data was collected by the government for another purpose and is used second-hand.'),
            ('Which is the main advantage of using an indirect data source?', 'The data is already available, so it is quicker and usually cheaper to obtain', ['The data is guaranteed to be up to date', 'Only the data that is needed is collected', 'The source of the data is always known'],
             'Indirect data already exists; but it may be out of date, biased or contain unnecessary data.')],
      exps=[('Explain why "35, 42, 38" is data and not information.', 'The values have no context: we do not know what they measure or what units they are in, so they have no meaning.', '1 mark: no context/meaning; 1 mark: e.g. we do not know if they are ages, marks or temperatures. [2]'),
            ('Explain two advantages of using a direct data source.', 'The exact data needed is collected, so there is no irrelevant data; the source and collection method are known so the data can be trusted; it is up to date.', '2 × 1 mark point + 1 mark explanation, from: only relevant data; known reliability/origin; up to date; can be sampled appropriately. [4]'),
            ('Explain two disadvantages of using an indirect data source.', 'The data may be out of date because it was collected earlier; it may contain data that is not needed or be missing data that is needed; the original collection method and possible bias are unknown.', '2 × (1 mark point, 1 mark explanation): out of date; irrelevant/extra data; missing data; unknown accuracy or bias; may need to be paid for. [4]'),
            ('Explain how knowledge differs from information, using an example.', 'Information is data with context, e.g. "the temperature is 4 °C"; knowledge is applying understanding to it, e.g. knowing that at 4 °C you should wear a coat or that roads may become icy.', '1 mark: information = data with meaning; 1 mark: knowledge = applying information/experience; 1 mark: suitable example. [3]')],
      ars=[('A list of numbers such as 12, 45, 7 is data, not information.', 'Data has no context and so no meaning until it is processed.'),
           ('Census data used by a supermarket is an indirect data source.', 'It was collected by the government for a different purpose.'),
           ('Indirect data may be out of date.', 'It was collected at an earlier time, possibly for another purpose.'),
           ('Direct data sources usually take longer to obtain than indirect ones.', 'The data has to be collected first-hand, for example by questionnaires or observation.')],
      falses=['Information is raw data before it has been processed.', 'Data collected by questionnaire is always an indirect source.', 'Indirect data is always more accurate than direct data.',
              'Knowledge is the same as data stored in a database.'],
      adv=[('collecting its own customer data using questionnaires instead of buying data', ['only the data needed is collected', 'it knows how the data was collected so can judge its reliability', 'data is up to date'],
            ['it takes time and staff to design and run the survey', 'a small sample may not represent all customers', 'customers may not answer truthfully or may not respond']),
           ('using published government statistics to plan its services', ['data is available immediately', 'cheaper than collecting its own data', 'large sample sizes covering the whole country'],
            ['the data may be several years old', 'it may not be about the exact area or group needed', 'it may contain data that is not relevant'])],
      intros=['{p} works for {org}, {aot} in {city}. {p} needs data to decide whether to open on Sundays.',
              '{org}, {aot} based in {city}, is planning a new branch in a nearby district and needs data about the people who live there.',
              '{p}, a researcher at {org} in {city}, is investigating how local people travel to work and to the shops.',
              'The manager of {org} in {city} wants to know how satisfied customers are with its online service.'],
      parts=[('Describe two methods that could be used to collect direct data in this situation.', 'Questionnaires (paper or online) given to the people concerned; interviews; observation, e.g. counting customers; data logging.', '1 mark per method with a brief description, max 2 methods. [2]'),
             ('Identify two indirect data sources that could be used.', 'Government census data; published reports or statistics; the electoral register; data bought from a marketing company; other organisations\' surveys.', '1 mark each, max 2. [2]'),
             ('Explain one advantage of using a direct data source rather than an indirect one in this situation.', 'Only relevant data is collected and it is up to date, so decisions are based on current, appropriate data.', '1 mark advantage; 1 mark explanation in context. [2]'),
             ('Explain one disadvantage of using indirect data in this situation.', 'It may be out of date or collected for a different purpose, so it may not reflect current customers or this area.', '1 mark disadvantage; 1 mark explanation in context. [2]'),
             ('Give an example of a piece of data that might be collected and explain how it becomes information.', 'e.g. "45" becomes information when it is given context: "45% of customers would shop on Sundays".', '1 mark example of data; 1 mark context/processing added. [2]'),
             ('Describe how the information obtained could be turned into knowledge.', 'The manager interprets the information using experience, e.g. understanding that demand is high enough to cover staff costs, and uses it to make a decision.', '1 mark interpretation/understanding; 1 mark applied to a decision. [2]')],
      ev=[('whether {org} should rely on indirect data sources rather than collecting its own data', 'indirect data is quicker and cheaper; large datasets; available immediately.', 'may be out of date; collected for another purpose so may not fit; unknown accuracy or bias; may have to be bought.', 'a combination is often best: use indirect data for an overview and direct data for the specific decision.'),
          ('the use of direct data collection methods by {org} when making decisions', 'relevant, current data; known reliability; can target the right people.', 'time-consuming and costly; sample may be small or biased; respondents may not answer honestly.', 'direct data is better for specific, important decisions if time and budget allow.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch1_sources(r, D):
    n = {1: 1, 2: 2, 3: 3, 4: 4}[D]
    picks = r.sample(SOURCES, n)
    if n == 1:
        s, k = picks[0]
        return MCQ(r, f'Which type of data source is used when {s}?', f'{k.capitalize()} data source', ['Direct data source' if k == 'indirect' else 'Indirect data source', 'Neither: it is information, not data', 'Both direct and indirect at the same time'],
                   f'{k.capitalize()}: ' + ('collected first-hand for the purpose.' if k == 'direct' else 'collected by someone else / for a different purpose.'))
    lines = [f'{i + 1}. {cap(s)}' for i, (s, _) in enumerate(picks)]
    ans = '; '.join(f'{i + 1} {k}' for i, (_, k) in enumerate(picks))
    stem = 'For each situation, state whether the data source is direct or indirect' + (' and give a reason for each.' if D >= 3 else '.') + '\n' + '\n'.join(lines)
    m = n * (2 if D >= 3 else 1)
    key = '; '.join(f'{i + 1}: {k} ({"first-hand, for this purpose" if k == "direct" else "second-hand / collected for another purpose"})' for i, (_, k) in enumerate(picks))
    return Q(stem, ans, key + (f' — 1 mark each classification, 1 mark each reason. [{m}]' if D >= 3 else f' — 1 mark each. [{m}]'), marks=m, typ='short')


QUALITY = [
    ('accuracy', 'A hotel website shows that a room costs $85 per night, but the hotel actually charges $58.'),
    ('accuracy', 'A delivery driver is given an address with the wrong house number.'),
    ('accuracy', 'A student\'s date of birth was typed as 12/07/2091 in the school database.'),
    ('relevance', 'A manager deciding staff rotas for next week is sent a report on the company\'s sales from ten years ago and the history of its logo.'),
    ('relevance', 'A student researching volcanoes in Iceland is given search results about volcanoes in video games.'),
    ('relevance', 'A doctor looking for a patient\'s allergies is shown the patient\'s list of favourite sports.'),
    ('age', 'A tourist uses a printed bus timetable from four years ago and misses the last bus.'),
    ('age', 'A stock controller orders goods using stock levels that were last updated a month ago.'),
    ('age', 'A satellite navigation system uses a map that does not show a road opened last year.'),
    ('level of detail', 'A head teacher asks for the overall pass rate but is given every mark for every question for every student.'),
    ('level of detail', 'A customer asks for the total cost of a holiday but is only told "it is not expensive".'),
    ('level of detail', 'A weather forecast for a farmer gives only "rain this week" without days or amounts.'),
    ('completeness', 'A sales report for the year is missing the figures for November and December.'),
    ('completeness', 'An online order form submits a customer\'s address without the postal code.'),
    ('completeness', 'A train timetable shows departure times but not which platform each train leaves from.'),
]
QFACT = ['accuracy', 'relevance', 'age', 'level of detail', 'completeness']
QWHY = {'accuracy': 'the information is incorrect, so decisions based on it will be wrong',
        'relevance': 'the information is not related to the purpose it is needed for, so time is wasted finding what matters',
        'age': 'the information is out of date, so it no longer reflects the current situation',
        'level of detail': 'there is either too much or too little detail for the user\'s needs',
        'completeness': 'some of the required information is missing, so it cannot be fully used'}

t = T(1, 'Quality of information: accuracy, relevance, age, level of detail and completeness', 'quality of information', 'accuracy, relevance, age',
      defs=[('accuracy (of information)', 'Information is accurate when it is correct and free from errors, so it can be relied on.'),
            ('relevance (of information)', 'Information is relevant when it relates to, and is needed for, the purpose for which it is being used.'),
            ('age (of information)', 'How up to date information is; out-of-date information may no longer reflect the current situation.'),
            ('level of detail', 'Whether information contains the right amount of detail for its purpose: not too much and not too little.'),
            ('completeness (of information)', 'Information is complete when nothing that is needed for the purpose is missing.')],
      mcqs=[('A report contains every individual transaction for a year, but the manager only needs monthly totals. Which factor affecting the quality of information is the problem?', 'Level of detail', ['Accuracy', 'Age', 'Completeness'], 'There is too much detail for the purpose.'),
            ('Which of these is most likely to reduce the accuracy of information?', 'Data entry errors that were not detected by validation or verification', ['Information being shown in a chart', 'Information being stored in the cloud', 'Information being produced quickly'], 'Inaccurate input data produces inaccurate information (garbage in, garbage out).'),
            ('Which factor is the problem when a customer list does not include telephone numbers that are needed for a marketing campaign?', 'Completeness', ['Relevance', 'Age', 'Level of detail'], 'Required data is missing, so the information is incomplete.')],
      exps=[('Explain why information that is accurate may still be of poor quality.', 'It may be out of date, irrelevant to the purpose, incomplete or have the wrong level of detail, so it still cannot be used to make a good decision.', '1 mark: accuracy is only one factor; 1 mark: example of another factor making it unusable. [2]'),
            ('Explain how the age of information can affect the decisions made by a business.', 'Old information may no longer reflect the current situation (e.g. prices, stock levels, customer numbers), so decisions such as how much to order may be wrong.', '1 mark: out of date no longer reflects reality; 1 mark: consequence for a decision. [2]'),
            ('Explain why too much detail can reduce the quality of information.', 'The user has to search through unnecessary data to find what they need, which wastes time and the key points may be missed.', '1 mark: unnecessary data obscures the key points; 1 mark: time wasted / errors in decisions. [2]'),
            ('Explain how inaccurate data entry leads to inaccurate information.', 'Information is produced by processing data; if the input data is wrong, the processed output will also be wrong (garbage in, garbage out).', '1 mark: information depends on input data; 1 mark: GIGO consequence. [2]')],
      ars=[('Information that is out of date may lead to poor decisions.', 'The situation may have changed since the information was produced.'),
           ('Too much detail can make information less useful.', 'Users must search through unnecessary data to find what they need.'),
           ('Validation helps to improve the accuracy of information.', 'It prevents some unreasonable data from being entered.')],
      falses=['Accurate information is always complete.', 'Information never loses value over time.', 'More detail always improves the quality of information.'],
      intros=['{org}, {aot} in {city}, produces a weekly report for managers using data entered by staff.',
              '{p} is using information from several websites to plan a business trip from {city} to {city2}.',
              'The managers of {org} in {city} complain that the information they receive is not helping them make decisions.'],
      parts=[('Identify three factors that affect the quality of information.', 'Any three of: accuracy, relevance, age, level of detail, completeness.', '1 mark each. [3]'),
             ('Explain why the information must be up to date.', 'Decisions are based on the current situation; old information (e.g. prices, timetables, stock levels) may have changed, leading to wrong decisions.', '1 mark: changes over time; 1 mark: consequence. [2]'),
             ('Explain how the level of detail could affect the usefulness of the information.', 'Too much detail hides the key facts and wastes time; too little detail means decisions cannot be made accurately.', '1 mark too much; 1 mark too little. [2]'),
             ('Describe two ways the accuracy of the data could be improved.', 'Validation checks on input (range, presence, format); verification such as double entry or visual checking; using reliable sources.', '1 mark each, max 2. [2]'),
             ('Explain why the information needs to be complete.', 'If parts are missing, the user cannot make a full judgement and may have to search for more information or make mistakes.', '1 mark: missing parts; 1 mark: consequence. [2]')],
      ev=[('how far the quality of the information affects the decisions made by {org}', 'accurate, relevant, current and complete information leads to better decisions and fewer costly mistakes.', 'managers\' experience (knowledge) also matters; sometimes decisions must be made quickly with imperfect information; collecting perfect information is expensive.', 'quality is critical, but the cost of improving it must be balanced against the benefit to the decision.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch1_quality(r, D):
    if D <= 2:
        f, s = r.choice(QUALITY)
        d = ctx(r)
        stem = f'{s} Which factor affecting the quality of information is the main problem here?'
        if D == 1:
            return MCQ(r, stem, f.capitalize(), [x.capitalize() for x in QFACT if x != f], f'{f.capitalize()}: {QWHY[f]}.')
        return Q(stem.replace('Which factor', 'Identify which factor') .replace('?', ' and explain your answer.'), f'{f.capitalize()}: {QWHY[f]}.',
                 f'1 mark: {f}; 1 mark: explanation — {QWHY[f]}. [2]', marks=2)
    n = 2 if D == 3 else 3
    fs = r.sample(QFACT, n)
    picks = [r.choice([x for x in QUALITY if x[0] == f]) for f in fs]
    lines = [f'{i + 1}. {s}' for i, (_, s) in enumerate(picks)]
    stem = 'For each situation, identify the factor affecting the quality of information and explain how it reduces the usefulness of the information.\n' + '\n'.join(lines)
    return Q(stem, '; '.join(f'{i + 1} {f}' for i, (f, _) in enumerate(picks)),
             '; '.join(f'{i + 1}: {f} — {QWHY[f]}' for i, (f, _) in enumerate(picks)) + f' (1 mark factor, 1 mark explanation each). [{2 * n}]', marks=2 * n)


# ------------------------------------------------------------------ validation and verification
VCHECK = {
    'presence check': 'checks that data has been entered and the field is not left blank',
    'range check': 'checks that data lies between an upper and a lower limit',
    'type check': 'checks that data is of the correct data type, e.g. a number not text',
    'length check': 'checks that data has the required number of characters',
    'format check': 'checks that data follows a set pattern, e.g. two letters followed by four digits',
    'check digit': 'an extra digit calculated from the other digits of a code, recalculated on entry to detect transcription errors',
    'lookup check': 'checks that the data entered matches a value in a list of acceptable values',
    'consistency check': 'checks that data in one field is consistent with data in another field',
    'limit check': 'checks that data is not above (or below) a single limit',
}
VFIELDS = [
    ('the number of children a customer has', 'range check', 'between 0 and 20', '25'),
    ('a customer\'s surname', 'presence check', 'must not be left blank', '(left blank)'),
    ('a product code such as AB1234', 'format check', 'two letters then four digits', '12AB34'),
    ('a mobile phone number with 10 digits', 'length check', 'exactly 10 characters', '07123456'),
    ('the month of a date entered as a number', 'range check', 'between 1 and 12', '13'),
    ('the gender field, which must be M, F or X', 'lookup check', 'value must be in the list M, F, X', 'Q'),
    ('an ISBN of a book', 'check digit', 'last digit recalculated from the others', 'an ISBN with two digits swapped'),
    ('a quantity ordered entered as a whole number', 'type check', 'must be an integer', 'six'),
    ('the date of leaving, which must be after the date of joining', 'consistency check', 'date of leaving > date of joining', 'a leaving date before the joining date'),
    ('a postcode / zip code of a fixed pattern', 'format check', 'must match the pattern', 'a code with letters where digits are needed'),
    ('a password that must have at least 8 characters', 'length check', 'at least 8 characters', 'abc12'),
    ('the number of hours worked in a week, which cannot exceed 60', 'limit check', 'not more than 60', '75'),
    ('a country chosen when registering', 'lookup check', 'must be in the list of countries', 'a misspelt country name'),
    ('an exam percentage mark', 'range check', 'between 0 and 100', '104'),
]
VERIF = {
    'visual check': 'the user compares the data entered on screen with the source document, by eye',
    'double data entry': 'data is entered twice (often by two different people) and the computer compares the two versions, flagging differences',
    'parity check': 'an extra bit is added to each byte so that the number of 1s is even (or odd); the receiver checks the parity',
    'checksum': 'a value calculated from a block of data is sent with it; the receiver recalculates it and compares',
    'hash total': 'a total of a field that has no meaning (e.g. account numbers) is calculated before and after input and compared',
    'control total': 'a meaningful total (e.g. total amount of money) is calculated before and after input and compared',
}

t = T(1, 'Validation and verification methods', 'validation and verification methods', 'validation', 'verification', 'check digit',
      defs=[('validation', 'An automatic check carried out by the computer to make sure that data entered is reasonable and follows set rules.'),
            ('verification', 'A check that data has been copied or entered accurately, i.e. that it matches the original source.'),
            ('check digit', 'An extra digit added to the end of a code, calculated from the other digits, which is recalculated on input to detect errors such as transposed digits.'),
            ('hash total', 'A total of a field that has no meaning on its own, such as account numbers, used to check that all data in a batch has been entered correctly.'),
            ('control total', 'A meaningful total, such as the total value of invoices in a batch, calculated before and after input to check the data has been entered correctly.'),
            ('double data entry', 'A verification method in which data is entered twice and the computer compares the two entries to detect differences.')],
      mcqs=[('Which validation check would detect that the month 14 has been entered in a date?', 'Range check', ['Presence check', 'Length check', 'Type check'], 'Months must lie between 1 and 12.'),
            ('Which method is a verification method?', 'Double data entry', ['Range check', 'Format check', 'Lookup check'], 'Double entry checks the data matches the source; the others are validation.'),
            ('A clerk types 6.25 instead of 2.65 for a price. Which method is most likely to detect this error?', 'Visual check against the source document', ['Type check', 'Presence check', 'Length check'], 'Both values are valid numbers of the same length, so only checking against the source can find the error.'),
            ('Which error would a check digit be designed to detect?', 'Two digits of a product code being swapped', ['A customer entering the wrong name', 'A field being left blank', 'A price that is too high'], 'Check digits detect transcription and transposition errors in codes.'),
            ('Which validation check makes sure a "date of return" is later than the "date of loan"?', 'Consistency check', ['Range check', 'Limit check', 'Format check'], 'It compares two fields with each other.')],
      exps=[('Explain why data that passes validation may still be incorrect.', 'Validation only checks that data is reasonable and follows the rules; a wrong value that is still within the rules (e.g. age 31 typed instead of 13) will be accepted.', '1 mark: validation checks reasonableness/rules only; 1 mark: suitable example. [2]'),
            ('Explain the difference between validation and verification.', 'Validation is an automatic check that data is sensible/obeys rules; verification checks that data has been entered or copied accurately from the source.', '1 mark validation; 1 mark verification. [2]'),
            ('Explain why both validation and verification are used when entering data.', 'Validation stops unreasonable data but cannot detect a valid but wrong value; verification detects transcription errors but cannot tell whether the original data was sensible; together they reduce errors more.', '1 mark: what validation cannot do; 1 mark: what verification cannot do; 1 mark: combined effect. [3]'),
            ('Explain how a hash total is used to check that a batch of documents has been input correctly.', 'Before input, the values of a field such as account number are added up; the computer adds the same field after input; if the totals differ, a document has been missed or mistyped.', '1 mark total calculated before input; 1 mark recalculated by computer; 1 mark compared/difference shows error. [3]'),
            ('Explain one disadvantage of double data entry.', 'It takes twice as long and may need two members of staff, so it is costly; and the same mistake could be made twice if the source is misread.', '1 mark point; 1 mark explanation. [2]')],
      ars=[('A range check cannot ensure that data is correct.', 'A value can be within the range but still be the wrong value.'),
           ('Double data entry is a method of verification.', 'It checks that the data entered matches the original source.'),
           ('A check digit can detect transposed digits in a code.', 'Each digit is multiplied by a different weight, so swapping digits changes the result.'),
           ('A hash total has no meaning in itself.', 'It is the sum of a field, such as account numbers, that is not normally added.')],
      falses=['Validation guarantees that data is correct.', 'A presence check makes sure numbers are within limits.', 'Visual checking is carried out automatically by the computer.',
              'A control total is the number of records in a batch.'],
      intros=['{org}, {aot} in {city}, uses an online form for customers to register and place orders.',
              'Staff at {org} in {city} type details from paper application forms into a database.',
              '{p} is designing a data entry screen for the membership system of {org} in {city}.'],
      parts=[('Describe two validation checks that could be used on the form, naming a field for each.', 'e.g. presence check on surname; range check on age 16–100; format check on postcode; length check on phone number; lookup check on country.', '1 mark per check with suitable field, max 2. [2]'),
             ('Explain why verification is also needed.', 'Data could pass validation but still be entered incorrectly; verification checks it matches the source.', '1 mark valid but wrong data; 1 mark verification compares with source. [2]'),
             ('Describe how double data entry would be carried out.', 'Data is typed in twice, possibly by different people; the computer compares the two entries and flags any differences to be corrected.', '1 mark entered twice; 1 mark compared/differences flagged. [2]'),
             ('Explain why a visual check may not detect all errors.', 'The person checking may be tired or careless, may misread the source, or may read what they expect to see.', '1 mark human error; 1 mark explanation. [2]'),
             ('Suggest suitable normal, extreme and abnormal test data for an age field that must be between 18 and 65.', 'Normal e.g. 30; extreme 18 and 65; abnormal e.g. 12, 70 or "abc".', '1 mark each type. [3]'),
             ('Explain why validation is important for the organisation.', 'It reduces the amount of incorrect data stored, so information produced is more accurate and fewer costly mistakes are made (e.g. deliveries to wrong addresses).', '1 mark fewer errors; 1 mark consequence. [2]')],
      ev=[('whether validation and verification together can guarantee that the data stored by {org} is accurate', 'validation removes unreasonable data; verification detects transcription errors; together they catch most input errors.', 'valid but wrong data that matches a wrong source document will still be accepted; human verification can be careless; data can become out of date.', 'they greatly reduce, but cannot eliminate, inaccurate data; good source data and staff training are also needed.')])


def mod11_digit(digs):
    w = list(range(len(digs) + 1, 1, -1))
    s = sum(a * b for a, b in zip(digs, w))
    c = (11 - s % 11) % 11
    return s, w, c


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch1_checkdigit(r, D):
    n = r.choice([4, 5, 6]) if D <= 3 else r.choice([6, 7, 8])
    for _ in range(30):
        digs = [r.randrange(10) for _ in range(n)]
        s, w, c = mod11_digit(digs)
        if c != 10:
            break
    else:
        return None
    cs = ''.join(map(str, digs))
    rule = (f'Each digit is multiplied by a weight, starting at {n + 1} for the leftmost digit and going down to 2; the products are added; '
            f'the check digit is (11 − (total MOD 11)) MOD 11, with 10 written as X.')
    work = ' + '.join(f'{a}×{b}' for a, b in zip(digs, w)) + f' = {s}'
    if D == 1:
        return MCQ(r, f'A code {cs} has a modulo-11 check digit added. {rule} What is the check digit?', str(c), [str((c + k) % 10) for k in (1, 3, 7, 9)] + [str(s % 11)],
                   f'{work}; {s} MOD 11 = {s % 11}; check digit = {c}.')
    if D in (2, 3):
        return Q(f'A library uses a modulo-11 check digit on its book codes. {rule} Calculate the check digit for the code {cs}. Show your working.', str(c),
                 f'{work} [1]; {s} MOD 11 = {s % 11} [1]; check digit = {c} [1]. [3]', marks=3, typ='numerical')
    # swap two adjacent digits and test
    i = r.randrange(n - 1)
    if digs[i] == digs[i + 1]:
        digs[i + 1] = (digs[i + 1] + 3) % 10
        s, w, c = mod11_digit(digs)
        if c == 10:
            return None
        cs = ''.join(map(str, digs))
        work = ' + '.join(f'{a}×{b}' for a, b in zip(digs, w)) + f' = {s}'
    sw = digs[:]
    sw[i], sw[i + 1] = sw[i + 1], sw[i]
    s2, _, c2 = mod11_digit(sw)
    typed = ''.join(map(str, sw)) + str(c)
    work2 = ' + '.join(f'{a}×{b}' for a, b in zip(sw, w)) + f' = {s2}'
    stem = (f'A code is stored as {cs}{c}, where the final digit is a modulo-11 check digit. {rule} '
            f'An operator types it as {typed}. (a) Show that {c} is the correct check digit for {cs}. (b) Show how the computer detects the error in the typed code.')
    return Q(stem, f'(a) {s}, MOD 11 = {s % 11}, check digit {c}. (b) Recalculated check digit for {"".join(map(str, sw))} is {"X" if c2 == 10 else c2}, which does not match {c}, so the code is rejected.',
             f'(a) {work} [1]; MOD 11 = {s % 11} and check digit {c} [1]. (b) {work2} [1]; check digit {"X" if c2 == 10 else c2} ≠ {c} so error detected [1]. [4]', marks=4, typ='numerical')


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch1_batch_totals(r, D):
    n = 4 if D <= 2 else (5 if D <= 4 else 6)
    accs = r.sample(range(10000, 99999), n)
    amts = [round(r.randrange(1500, 95000) / 100, 2) for _ in range(n)]
    rows = [(f'{a}', f'{m:.2f}') for a, m in zip(accs, amts)]
    hs, cs = sum(accs), round(sum(amts), 2)
    table = tbl(['Account number', 'Amount ($)'], rows)
    if D == 1:
        return MCQ(r, f'A batch of {n} payment slips is to be input. Which value is the batch total (record count) for this batch?\n{table}', str(n), [str(n + 1), f'{cs:.2f}', str(hs)],
                   f'A batch total counts the documents: {n}.')
    if D == 2:
        return Q(f'A clerk at {ctx(r)["org"]} prepares a batch of payment slips for input.\n{table}\nCalculate (a) the hash total of the account numbers and (b) the control total of the amounts.',
                 f'(a) {hs} (b) {cs:,.2f}', f'(a) {" + ".join(map(str, accs))} = {hs} [1] (b) sum of amounts = {cs:,.2f} [1]. [2]', marks=2, typ='numerical')
    # an error in input: one account number mistyped (digits swapped) or one amount missing
    j = r.randrange(n)
    kind = r.choice(['swap', 'miss'])
    if kind == 'swap':
        s = str(accs[j])
        k = r.randrange(4)
        if s[k] == s[k + 1]:
            return None
        bad = int(s[:k] + s[k + 1] + s[k] + s[k + 2:])
        hs2 = hs - accs[j] + bad
        stem = (f'A batch of payment slips is input at {ctx(r)["org"]}.\n{table}\nAfter input, the computer calculates a hash total of {hs2} and a control total of {cs:,.2f}. '
                f'(a) Calculate the hash total of the batch. (b) Explain what the result shows.' + (' (c) Explain why the control total did not detect the problem.' if D >= 4 else ''))
        ans = f'(a) {hs} (b) The totals differ by {abs(hs2 - hs)}, so an account number was entered incorrectly (account {accs[j]} entered as {bad}).' + (' (c) All amounts were entered correctly, so their total is unchanged.' if D >= 4 else '')
        key = f'(a) {hs} [1] (b) {hs2} ≠ {hs} [1], so an account number was mistyped / error in account numbers [1]' + (' (c) control total only checks the amounts, which were correct [1]' if D >= 4 else '') + f'. [{3 + (D >= 4)}]'
        return Q(stem, ans, key, marks=3 + (D >= 4), typ='numerical')
    cs2 = round(cs - amts[j], 2)
    stem = (f'A batch of {n} payment slips is input at {ctx(r)["org"]}.\n{table}\nAfter input, the computer reports a batch total of {n - 1} documents and a control total of {cs2:,.2f}. '
            f'(a) Calculate the correct control total. (b) Identify which slip has not been input, showing how you know.')
    return Q(stem, f'(a) {cs:,.2f} (b) The slip for account {accs[j]}: {cs:,.2f} − {cs2:,.2f} = {amts[j]:.2f}, which is its amount; only {n - 1} documents were counted.',
             f'(a) {cs:,.2f} [1] (b) difference {cs:,.2f} − {cs2:,.2f} = {amts[j]:.2f} [1]; matches account {accs[j]} [1]. [3]', marks=3, typ='numerical')


@t.add('C3', (1, 2, 3, 4), 'short')
def ch1_vfield(r, D):
    f = r.choice(VFIELDS)
    d = ctx(r)
    if D == 1:
        return MCQ(r, f'{d["org"]} in {d["city"]} is designing a data entry form. Which validation check is most suitable for {f[0]}?', cap(f[1]).rstrip('.'),
                   [cap(x).rstrip('.') for x in VCHECK if x != f[1]], f'{f[1]}: {VCHECK[f[1]]} ({f[2]}).')
    if D == 2:
        return Q(f'{d["p"]} is designing a form for {d["org"]}. Name a suitable validation check for {f[0]} and give an example of data it would reject.',
                 f'{f[1].capitalize()} ({f[2]}); it would reject e.g. {f[3]}.', f'1 mark: {f[1]}; 1 mark: suitable invalid example such as {f[3]}. [2]', marks=2)
    g, h = r.sample([x for x in VFIELDS if x[1] != f[1]], 2)
    fs = [f, g] if D == 3 else [f, g, h]
    lines = '\n'.join(f'{i + 1}. {x[0]}' for i, x in enumerate(fs))
    return Q(f'A data entry screen for {d["org"]} contains these fields:\n{lines}\nFor each field, name a suitable validation check and describe how it would work.',
             '; '.join(f'{i + 1}: {x[1]} — {x[2]}' for i, x in enumerate(fs)),
             '; '.join(f'{i + 1}: {x[1]} [1], {VCHECK[x[1]]} / {x[2]} [1]' for i, x in enumerate(fs)) + f'. [{2 * len(fs)}]', marks=2 * len(fs))


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ch1_testdata(r, D):
    fld, lo, hi = r.choice([('the age of a member of a youth club', 11, 18), ('the number of seats booked in one transaction', 1, 10), ('a test score out of 50', 0, 50),
                            ('the quantity of an item ordered', 1, 99), ('the temperature setting of an oven in °C', 50, 250), ('the number of nights booked at a hotel', 1, 28),
                            ('the number of hours worked in a week', 0, 60), ('a month number', 1, 12), ('the age of a person applying for a driving licence', 17, 99),
                            ('a percentage discount', 0, 70), ('the number of passengers in a taxi booking', 1, 8), ('a shoe size', 2, 15)])
    vals = sorted({lo - 1, lo, hi, hi + 1, r.randrange(lo + 1, hi), r.randrange(lo + 1, hi), hi + r.randrange(2, 30), max(-5, lo - r.randrange(2, 20))})
    r.shuffle(vals)
    vals = vals[:6 if D <= 3 else 7]
    if lo not in vals:
        vals[0] = lo
    if hi + 1 not in vals and D >= 4:
        vals[-1] = hi + 1

    def kind(v):
        return 'extreme' if v in (lo, hi) else ('normal' if lo < v < hi else 'abnormal')
    rule = f'the validation rule is: value >= {lo} AND value <= {hi}'
    stem = (f'For {fld}, {rule}. Classify each of these test values as normal, extreme or abnormal, and state whether it will be accepted: '
            + ', '.join(map(str, vals)) + '.')
    ans = '; '.join(f'{v} {kind(v)} ({"accepted" if lo <= v <= hi else "rejected"})' for v in vals)
    m = len(vals)
    if D >= 4:
        stem = stem.replace(f'For {fld}, {rule}.', f'For {fld}, the validation rule is: value > {lo - 1} AND value < {hi + 1}.')
        stem += ' Explain why extreme data must be tested.'
        ans += '. Extreme values test the boundaries, where errors such as using > instead of >= are most likely.'
        m += 1
    return Q(stem, ans, f'1 mark per correct classification with accept/reject: {ans} [{m}]', marks=m, typ='numerical')


# ------------------------------------------------------------------ processing
PROC = [
    ('producing the monthly payroll for 3000 employees', 'batch', 'all the data can be collected first and processed together without user interaction; no immediate output needed'),
    ('printing customer utility bills at the end of each quarter', 'batch', 'bills are produced in one run from meter readings collected over the period'),
    ('booking a seat on a flight through an airline website', 'online', 'the seat must be reserved immediately so it cannot be double-booked; the user interacts with the system'),
    ('withdrawing money from an ATM', 'online', 'the account balance must be checked and updated straight away during the transaction'),
    ('controlling the fuel injection in a car engine', 'real-time', 'sensor input must be processed immediately so the output changes the engine within milliseconds'),
    ('an air-traffic control radar system', 'real-time', 'positions must be processed instantly so that aircraft are kept safe'),
    ('processing cheques cleared by a bank overnight', 'batch', 'cheques are collected during the day and processed together overnight'),
    ('updating stock levels when an item is scanned at a supermarket checkout', 'online', 'each sale updates the stock file as it happens'),
    ('a heart-rate monitor that sounds an alarm in an intensive care unit', 'real-time', 'readings must be processed immediately so an alarm can sound without delay'),
    ('marking multiple-choice exam answer sheets read by an OMR scanner', 'batch', 'sheets are collected and processed together; there is no urgency'),
    ('reserving a cinema ticket using an app', 'online', 'the seat is locked immediately so no other customer can book it'),
    ('controlling the temperature of a chemical reactor', 'real-time', 'immediate response to sensor readings is needed to keep the process safe'),
]
PROCDEF = {'batch': 'data is collected over a period and processed all together in one run, with no user interaction during processing',
           'online': 'transactions are processed as soon as they are entered, with the user interacting with the system and files updated immediately',
           'real-time': 'input is processed immediately and the output affects the next input, e.g. in a control system'}

t = T(1, 'Batch, online and real-time processing; master and transaction files', 'batch, online and real-time processing', 'master and transaction files',
      defs=[('batch processing', 'Processing in which data is collected together over a period of time and then processed all at once, without user interaction.'),
            ('online processing', 'Processing in which each transaction is processed as soon as it is entered, while the user interacts with the system.'),
            ('real-time processing', 'Processing in which input data is processed immediately and the output is fast enough to affect the next input, as in control systems.'),
            ('master file', 'The main file holding the permanent (or semi-permanent) data about the entities in a system, such as customer details and balances.'),
            ('transaction file', 'A temporary file holding the changes (transactions) collected over a period, which are used to update the master file.')],
      mcqs=[('Why is the transaction file sorted into the same order as the master file before a batch update?', 'So each master record only has to be read once, in sequence', ['So the master file can be deleted after the update', 'So the transactions are encrypted', 'So the user can enter data more quickly'],
             'Both files are in key order, so the update can move through the master file sequentially.'),
            ('Which type of processing would be most suitable for producing the monthly payroll?', 'Batch processing', ['Real-time processing', 'Online processing', 'Interactive processing'], 'All data can be collected first and processed together; no immediate response needed.'),
            ('In an online booking system, why must the seat be marked as booked immediately?', 'To stop the same seat being sold to another customer', ['To make the website load faster', 'To reduce the size of the master file', 'To allow batch totals to be calculated'], 'Updating immediately prevents double-booking.')],
      exps=[('Explain why a transaction file is sorted before it is used to update a sequential master file.', 'Both files are then in the same key order, so the master file can be read once from start to end, matching each transaction to its record; this is efficient and needs no searching.', '1 mark same key order; 1 mark read sequentially once / efficient. [2]'),
            ('Explain why a new master file is created during a batch update rather than changing the old one.', 'Records cannot easily be changed in place in a sequential file; writing a new file also keeps the old master and the transaction file as a backup (grandfather–father–son) if the update fails.', '1 mark sequential update writes new file; 1 mark old file kept as backup/recovery. [2]'),
            ('Explain one advantage and one disadvantage of batch processing.', 'Advantage: can run at off-peak times (e.g. overnight) with no staff present, processing large volumes efficiently. Disadvantage: the master file is out of date between runs, and errors are found only after the run.', '1 mark advantage + explanation; 1 mark disadvantage + explanation. [4]'),
            ('Explain the difference between online processing and real-time processing.', 'Online processing handles each transaction as it is entered, with the user waiting for a response; real-time processing responds immediately to inputs (often from sensors) so that the output affects the next input, as in a control system.', '1 mark online; 1 mark real-time with feedback/immediate output. [2]')],
      ars=[('Batch processing is suitable for producing utility bills.', 'Bills do not need to be produced immediately and all readings can be processed together.'),
           ('An ATM uses online processing.', 'The account must be checked and updated during the transaction.'),
           ('The transaction file is sorted before a sequential update.', 'Both files must be in the same key order so each record is read only once.')],
      falses=['Real-time processing collects data for a week before processing it.', 'A master file only holds temporary data.', 'Batch processing requires the user to be present during processing.'],
      intros=['{org}, {aot} in {city}, keeps customer records on a master file that is updated from a transaction file every night.',
              '{p} manages the IT systems at {org} in {city}, which handles both online bookings and a monthly payroll.',
              '{org}, {aot} in {city}, collects data about its customers during each month and sends out invoices in one run.'],
      parts=[('Describe what is stored on the master file and on the transaction file.', 'Master file: permanent data such as customer ID, name, address and balance. Transaction file: changes over the period, such as payments, new orders or meter readings.', '1 mark master; 1 mark transaction. [2]'),
             ('Explain why batch processing is suitable here.', 'Large volumes of similar data can be collected over a period and processed together, at off-peak times, without user interaction.', '1 mark large volume/collected first; 1 mark no interaction/off-peak. [2]'),
             ('Describe the steps in updating the master file using a sorted transaction file.', 'Read first master and first transaction; if keys match, apply the transaction and write the updated record to the new master; if master key is smaller, copy the master record unchanged; repeat until end of files; unmatched transactions written to an error report.', '1 mark per step, max 4. [4]'),
             ('Explain why the old master file is kept after the update.', 'If the new master is lost or corrupted, it can be recreated by running the old master with the transaction file again (backup / recovery).', '1 mark backup; 1 mark recreated from old master + transactions. [2]'),
             ('Explain why online processing would be needed for some of the organisation\'s tasks.', 'Tasks such as bookings or stock enquiries need immediate updating so that data is current and items are not double-booked.', '1 mark immediate update; 1 mark example/consequence. [2]')],
      ev=[('whether {org} should replace its overnight batch processing with online processing', 'files always up to date; customers see current information; errors found immediately.', 'more expensive hardware and continuous availability needed; heavier load at peak times; batch is efficient for large regular jobs such as bills.', 'a mixed approach is usual: online for transactions customers see, batch for large periodic jobs.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch1_proc(r, D):
    s, k, why = r.choice(PROC)
    if D <= 2:
        return MCQ(r, f'Which type of processing is most suitable for {s}?', f'{k.capitalize()} processing', [f'{x.capitalize()} processing' for x in PROCDEF if x != k] + ['Manual processing'],
                   f'{k.capitalize()}: {why}.')
    picks = r.sample(PROC, 2 if D == 3 else 3)
    lines = '\n'.join(f'{i + 1}. {cap(x[0])}' for i, x in enumerate(picks))
    m = 2 * len(picks)
    return Q(f'State the most suitable type of processing (batch, online or real-time) for each task and justify your choice.\n{lines}',
             '; '.join(f'{i + 1}: {x[1]} — {x[2]}' for i, x in enumerate(picks)),
             '; '.join(f'{i + 1}: {x[1]} [1], justification: {x[2]} [1]' for i, x in enumerate(picks)) + f'. [{m}]', marks=m)


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ch1_masterupdate(r, D):
    nm = r.sample(PEOPLE, 5)
    ids = sorted(r.sample(range(101, 160), 5))
    bal = [r.randrange(0, 500) for _ in range(5)]
    nt = 3 if D <= 2 else (4 if D <= 4 else 5)
    tix = sorted(r.sample(range(5), nt))
    trans = []
    for i in tix:
        typ = r.choice(['payment', 'purchase'])
        amt = r.randrange(10, 200)
        trans.append((ids[i], typ, amt))
    bad = None
    if D >= 4:
        bad = r.choice([x for x in range(101, 160) if x not in ids])
        trans.append((bad, 'purchase', r.randrange(10, 200)))
        trans.sort()
    new = dict(zip(ids, bal))
    for i, typ, amt in trans:
        if i in new:
            new[i] += amt if typ == 'purchase' else -amt
    mt = tbl(['CustomerID', 'Name', 'Balance owed ($)'], [(i, n, b) for i, n, b in zip(ids, nm, bal)])
    tt = tbl(['CustomerID', 'Type', 'Amount ($)'], trans)
    stem = (f'{ctx(r)["org"]} updates its sequential master file using a sorted transaction file. A purchase adds to the balance owed; a payment subtracts from it.\n'
            f'Master file:\n{mt}\nTransaction file:\n{tt}\nComplete the new master file, giving the balance for every customer.')
    if D >= 4:
        stem += ' State what happens to any transaction that has no matching master record.'
    ans = '; '.join(f'{i} {new[i]}' for i in ids) + (f'; transaction for {bad} has no master record so it is written to an error report and not applied.' if bad else '')
    changed = [i for i in ids if any(t[0] == i for t in trans)]
    m = len(changed) + 1 + (1 if bad else 0)
    key = ('; '.join(f'{i}: {dict(zip(ids, bal))[i]} → {new[i]}' for i in changed) + ' (1 mark each)'
           + f'; unchanged records copied across unchanged [1]' + (f'; {bad} written to error/exception report [1]' if bad else '') + f'. [{m}]')
    return Q(stem, ans, key, marks=m, typ='numerical')


# ------------------------------------------------------------------ encryption
WORDS_ENC = ['NETWORK', 'SECURE', 'PAYMENT', 'BANKING', 'PRIVATE', 'MESSAGE', 'PASSWORD', 'DATABASE', 'CIPHER', 'ACCOUNT', 'INVOICE', 'TRANSFER', 'LOGIN', 'SERVER']


def caesar(s, k):
    return ''.join(chr((ord(c) - 65 + k) % 26 + 65) if c.isalpha() else c for c in s)


t = T(1, 'Encryption: symmetric and asymmetric, and protocols such as SSL/TLS and HTTPS', 'encryption: symmetric and asymmetric', 'ssl/tls', 'https',
      defs=[('encryption', 'Scrambling data (plaintext) using an algorithm and a key into a form (ciphertext) that cannot be understood without the key to decrypt it.'),
            ('symmetric encryption', 'Encryption in which the same secret key is used both to encrypt and to decrypt the data.'),
            ('asymmetric encryption', 'Encryption that uses a pair of keys: a public key to encrypt data and the matching private key, kept secret by its owner, to decrypt it.'),
            ('digital certificate', 'An electronic document issued by a certificate authority that links a public key to the identity of its owner, such as a website.'),
            ('Transport Layer Security (TLS)', 'A protocol that encrypts data sent between a client and a server and authenticates the server, the successor to SSL.')],
      mcqs=[('{p} wants to send {q} a confidential message using asymmetric encryption. Which key should be used to encrypt it?', "{q}'s public key", ["{q}'s private key", "{p}'s private key", "{p}'s public key"],
             'Only the holder of the matching private key ({q}) can decrypt data encrypted with {q}\'s public key.'),
            ('How can a user tell that a website is using TLS?', 'The address begins with https and a padlock symbol is shown', ['The address ends in .com', 'The page loads very quickly', 'The website asks for a password'], 'HTTPS = HTTP over SSL/TLS.'),
            ('What is the main problem with symmetric encryption?', 'The secret key has to be shared securely with the recipient', ['It cannot be used for large files', 'It needs two different keys', 'It is slower than asymmetric encryption'], 'If the key is intercepted while being shared, the data can be decrypted.'),
            ('In a TLS session, what is asymmetric encryption mainly used for?', 'Securely exchanging the symmetric session key', ['Encrypting all the web page data', 'Compressing the data', 'Checking the user\'s password'], 'Asymmetric encryption is slow, so it is used to agree a session key; the data is then encrypted symmetrically.')],
      exps=[('Explain why encryption does not stop data from being intercepted.', 'Encryption does not prevent data being copied or intercepted; it makes intercepted data meaningless without the decryption key.', '1 mark data can still be intercepted; 1 mark cannot be understood without key. [2]'),
            ('Explain why asymmetric encryption solves the key distribution problem of symmetric encryption.', 'The public key can be shared openly because it can only encrypt; only the private key, which is never sent, can decrypt, so no secret key needs to be transmitted.', '1 mark public key shared openly; 1 mark private key never transmitted/only it decrypts. [2]'),
            ('Describe how a digital certificate helps a browser to trust a website.', 'The certificate is issued by a trusted certificate authority and contains the website\'s public key and identity; the browser checks the CA\'s digital signature and the dates, so it knows the public key really belongs to that site.', '1 mark issued by CA; 1 mark contains public key/identity; 1 mark browser verifies signature/validity. [3]'),
            ('Describe the stages of a TLS handshake.', 'Client sends hello with supported cipher suites; server replies with its choice and its digital certificate; client checks the certificate; a session key is agreed/sent using asymmetric encryption; the rest of the session uses symmetric encryption with the session key.', '1 mark per stage, max 4. [4]')],
      ars=[('Data encrypted with a person\'s public key can only be decrypted with their private key.', 'The keys in an asymmetric pair are mathematically related.'),
           ('Symmetric encryption is faster than asymmetric encryption.', 'It uses a single key and simpler algorithms.'),
           ('HTTPS protects card details sent to an online shop.', 'The data is encrypted using TLS while it travels across the internet.')],
      falses=['The private key must be sent to everyone who wants to send you a message.', 'Encryption prevents hackers from intercepting data.', 'HTTPS stores web pages in encrypted form on the user\'s hard disk.'],
      intros=['{org}, {aot} in {city}, has set up an online shop where customers pay by card.',
              '{p} works from home and connects to the file server of {org} in {city} over the internet.',
              'Staff at {org} in {city} email confidential reports to a partner company in {city2}.'],
      parts=[('Explain why the data should be encrypted.', 'The data may be intercepted while travelling across the internet; encryption makes it unreadable without the key, protecting confidentiality.', '1 mark interception risk; 1 mark unreadable without key. [2]'),
             ('Describe how asymmetric encryption would be used to send the data securely.', 'The sender obtains the receiver\'s public key and uses it to encrypt the data; only the receiver\'s private key can decrypt it.', '1 mark public key of receiver encrypts; 1 mark private key decrypts. [2]'),
             ('Explain how the user knows that the connection is secure.', 'The address starts with https and a padlock is shown; the browser has checked the server\'s digital certificate.', '1 mark https/padlock; 1 mark certificate verified. [2]'),
             ('Explain one drawback of symmetric encryption in this situation.', 'Both parties need the same secret key, which must be shared securely; if it is intercepted, all messages can be decrypted.', '1 mark key must be shared; 1 mark risk if intercepted. [2]'),
             ('Describe the purpose of a digital certificate.', 'It authenticates the server by linking its identity to its public key, signed by a trusted certificate authority.', '1 mark authentication/identity; 1 mark issued/signed by CA. [2]')],
      ev=[('whether using HTTPS is enough to protect the personal data of the customers of {org}', 'TLS encrypts data in transit and authenticates the server; protects card details from interception.', 'data stored on the server is not protected by HTTPS; phishing sites can also have certificates; weak passwords and malware remain threats.', 'HTTPS is essential but must be combined with encryption at rest, access control and staff training.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch1_caesar(r, D):
    w = r.choice(WORDS_ENC)
    k = r.randrange(2, 12)
    c = caesar(w, k)
    if D == 1:
        return MCQ(r, f'A simple symmetric cipher shifts each letter {k} places forward in the alphabet (Z wraps round to A). What is "{w[:5]}" encrypted?', caesar(w[:5], k),
                   [caesar(w[:5], k + 1), caesar(w[:5], -k), caesar(w[:5], k - 1)], f'Each letter moved forward {k}: {w[:5]} → {caesar(w[:5], k)}.')
    if D == 2:
        return Q(f'A Caesar cipher with key {k} shifts each letter {k} places forward in the alphabet, wrapping from Z to A. Encrypt the word {w}.', c,
                 f'Each letter shifted forward {k}: {w} → {c} (1 mark for at least half the letters correct, 2 marks all correct). [2]', marks=2, typ='numerical')
    if D == 3:
        return Q(f'The ciphertext "{c}" was produced with a Caesar cipher that shifts letters {k} places forward. Decrypt it and explain why this is an example of symmetric encryption.',
                 f'{w}. The same key ({k}) is used to encrypt (shift forward) and decrypt (shift back).', f'Decryption {w} [2] (1 mark if one error); same key used for both [1]. [3]', marks=3, typ='numerical')
    bits = r.choice([8, 16, 24, 32, 40, 56])
    rate = r.choice([10 ** 6, 10 ** 8, 10 ** 9, 10 ** 10])
    keys = 2 ** bits
    secs = keys / rate
    if secs < 120:
        if secs < 1:
            from decimal import Decimal
            tstr = f"{Decimal(str(float(f'{secs:.3g}'))):f} seconds"
        else:
            tstr = f'{secs:,.2f} seconds' if secs < 10 else f'{secs:,.0f} seconds'
    elif secs < 7200:
        tstr = f'{secs / 60:,.1f} minutes'
    elif secs < 2 * 86400:
        tstr = f'{secs / 3600:,.1f} hours'
    elif secs < 3 * 365 * 86400:
        tstr = f'{secs / 86400:,.1f} days'
    else:
        tstr = f'{secs / (365 * 86400):,.3g} years'
    stem = (f'A Caesar cipher has only 25 useful keys, so it can be broken by trying every key. A modern cipher uses a {bits}-bit key. '
            f'(a) Calculate how many different keys are possible. (b) A computer can test {rate:,} keys per second. Calculate the maximum time needed to try every key. '
            f'(c) Explain why longer keys make encryption more secure.')
    return Q(stem, f'(a) 2^{bits} = {keys:,} (b) {keys:,} ÷ {rate:,} = {secs:,.2f} s ≈ {tstr} (c) Each extra bit doubles the number of keys, so a brute-force attack takes far longer.',
             f'(a) 2^{bits} = {keys:,} [1] (b) {keys:,} / {rate:,} [1] = {tstr} [1] (c) more possible keys / each bit doubles keys so brute force impractical [1]. [4]', marks=4, typ='numerical')


@t.add('C2', (2, 3, 4), 'mcq')
def ch1_keys(r, D):
    a, b = r.sample(PEOPLE, 2)
    task = r.choice(['send', 'sign', 'decrypt'])
    if task == 'send':
        stem = f'{a} sends a confidential file to {b} using asymmetric encryption. Which key does {a} use to encrypt the file?'
        ans = f"{b}'s public key"
        why = f'Anyone can use {b}\'s public key, but only {b}\'s private key can decrypt the file.'
    elif task == 'sign':
        stem = f'{a} adds a digital signature to a contract sent to {b}. Which key is used to create the signature?'
        ans = f"{a}'s private key"
        why = f'Only {a} has {a}\'s private key, so {b} can verify the signature with {a}\'s public key.'
    else:
        stem = f'{b} receives a message that {a} encrypted using asymmetric encryption. Which key does {b} use to decrypt it?'
        ans = f"{b}'s private key"
        why = 'The message was encrypted with the recipient\'s public key, so the recipient\'s private key decrypts it.'
    pool = [f"{a}'s public key", f"{a}'s private key", f"{b}'s public key", f"{b}'s private key"]
    return MCQ(r, stem, ans, [x for x in pool if x != ans], why)





# =============================================================================== Chapter 2 Hardware and software
t = T(2, 'Mainframe computers and supercomputers: characteristics and uses', 'mainframe computers and supercomputers', 'mainframe', 'supercomputer',
      defs=[('mainframe computer', 'A large, powerful computer used by organisations to process very large volumes of transactions and data reliably for many users at the same time.'),
            ('supercomputer', 'A computer with very high processing speed, built from many processors working in parallel, used for complex calculations such as weather forecasting.'),
            ('RAS (reliability, availability, serviceability)', 'Characteristics of a mainframe: it rarely fails, is almost always available, and can be repaired or upgraded while still running.'),
            ('FLOPS', 'Floating-point operations per second: the unit used to measure the processing speed of supercomputers.'),
            ('MIPS', 'Millions of instructions per second: a measure of processing speed often quoted for mainframe computers.')],
      mcqs=[('Which task is most suited to a supercomputer rather than a mainframe?', 'Running a climate model of the whole planet', ['Processing a bank\'s daily card transactions', 'Producing a census report of population statistics', 'Handling an airline\'s reservations for many users'],
             'Supercomputers are designed for a small number of very complex calculations; mainframes handle large volumes of transactions.'),
            ('Which unit is normally used to compare the performance of supercomputers?', 'FLOPS', ['MIPS', 'Megapixels', 'Megabits per second'], 'Supercomputer performance is measured in floating-point operations per second.'),
            ('Why are mainframe computers often said to have great longevity?', 'They can run for many years and are upgraded rather than replaced', ['They are replaced every six months', 'They contain no moving parts', 'They are only switched on once a year'],
             'Mainframes are expensive and reliable, so organisations keep and upgrade them for decades.'),
            ('Which feature allows a mainframe to keep working if one processor fails?', 'Fault tolerance through duplicated components', ['A graphical user interface', 'A single large hard disk', 'Batch processing'], 'Duplicate (redundant) hardware takes over automatically.')],
      exps=[('Explain why a bank uses a mainframe computer to process transactions.', 'A mainframe can process very large volumes of transactions for thousands of users at the same time, very reliably and securely, with almost no downtime.', '1 mark large volume/many users; 1 mark reliability/availability/security. [2]'),
            ('Explain why supercomputers need special cooling systems.', 'They contain thousands of processors working at high speed in a small space, which produce a great deal of heat that would damage components if not removed.', '1 mark many processors produce heat; 1 mark damage/failure if not cooled. [2]'),
            ('Describe two uses of supercomputers.', 'Weather forecasting and climate research (solving complex models of the atmosphere); quantum mechanics / molecular modelling for drug research; simulating nuclear reactions; genetic analysis.', '1 mark per use with brief description, max 2. [2]'),
            ('Explain why mainframes are suitable for processing a national census.', 'A census involves very large volumes of data from millions of people; mainframes have high throughput of input/output and can process and store this data reliably and securely.', '1 mark large volume of data; 1 mark high throughput/reliability. [2]')],
      ars=[('Supercomputers are used for weather forecasting.', 'Weather models need an enormous number of calculations to be completed quickly.'),
           ('Mainframes have high availability.', 'They have duplicated components and can be serviced while running.'),
           ('Mainframes are measured in MIPS rather than FLOPS.', 'Their work is mainly large volumes of transactions rather than scientific calculation.')],
      falses=['Supercomputers are mainly used to process bank card transactions.', 'Mainframes must be switched off to replace a faulty part.', 'A supercomputer has a single very fast processor.'],
      intros=['{org}, {aot} with branches across the country, processes millions of customer transactions every day on a mainframe in {city}.',
              '{org}, {aot} in {city}, runs a mainframe for its customer transactions and has been asked to advise a national weather service on a new supercomputer.',
              '{p} is writing a report for {org} in {city} comparing mainframes and supercomputers.'],
      parts=[('Describe two characteristics of a mainframe computer.', 'Reliability (rarely fails); availability (runs continuously); serviceability (repaired while running); very high input/output volumes; strong security; longevity.', '1 mark each, max 2. [2]'),
             ('Explain why the organisation needs high availability.', 'Customers and staff need the service at all times; downtime would mean lost transactions, lost income and damaged reputation.', '1 mark continuous service; 1 mark consequence of downtime. [2]'),
             ('Describe one use of a supercomputer and explain why a supercomputer is needed for it.', 'e.g. weather forecasting: complex models with billions of calculations must be completed before the forecast is out of date.', '1 mark use; 1 mark reason (speed/complexity). [2]'),
             ('Explain the difference between how mainframe and supercomputer performance is measured.', 'Mainframes in MIPS (instructions per second, suited to transaction volume); supercomputers in FLOPS (floating-point operations, suited to scientific calculation).', '1 mark MIPS mainframe; 1 mark FLOPS supercomputer. [2]'),
             ('Explain why heat is a problem for supercomputers.', 'Many processors in a small space generate a lot of heat; cooling systems are expensive and use a lot of energy.', '1 mark heat source; 1 mark cost/energy of cooling. [2]')],
      ev=[('whether {org} should move its transaction processing from a mainframe to cloud servers', 'cloud is scalable, pay-as-you-go, no need to maintain hardware or specialist staff.', 'mainframes offer proven reliability and security; data protection concerns over cloud; migration risks and costs; reliance on internet connection.', 'for critical high-volume transaction processing, many organisations keep mainframes, possibly in a hybrid arrangement.')])


PREF = [(10 ** 12, 'teraFLOPS', 'TFLOPS'), (10 ** 15, 'petaFLOPS', 'PFLOPS'), (10 ** 18, 'exaFLOPS', 'EFLOPS')]


def tfmt(secs):
    if secs < 120:
        return f'{num(round(secs, 2))} seconds'
    if secs < 7200:
        return f'{num(round(secs / 60, 1))} minutes'
    if secs < 3 * 86400:
        return f'{num(round(secs / 3600, 2))} hours'
    return f'{num(round(secs / 86400, 1))} days'


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch2_flops(r, D):
    base, nm, ab = r.choice(PREF[:2] if D <= 3 else PREF)
    sp = r.choice([2, 4, 5, 8, 10, 20, 25, 40, 50, 125, 200, 500])
    ops_e = r.choice([15, 16, 17, 18, 19, 20]) if base == 10 ** 12 else r.choice([18, 19, 20, 21, 22])
    if base == 10 ** 18:
        ops_e = r.choice([21, 22, 23])
    mant = r.choice([1, 2, 3, 4, 5, 6, 8])
    ops = mant * 10 ** ops_e
    secs = ops / (sp * base)
    task = r.choice(['a weather simulation', 'a climate model run', 'a protein-folding simulation', 'an earthquake simulation', 'a galaxy-formation model'])
    if D == 1:
        e = int(math.log10(base))
        return MCQ(r, f'A supercomputer is rated at {sp} {nm}. How many floating-point operations per second is this?', f'{sp} × 10^{e}',
                   [f'{sp} × 10^{e - 3}', f'{sp} × 10^{e + 3}', f'{sp} × 10^{e - 6}', f'{sp} × 10^6'], f'1 {ab} = 10^{e} FLOPS, so {sp} {ab} = {sp} × 10^{e} FLOPS.')
    stem = f'{task.capitalize()} needs {mant} × 10^{ops_e} floating-point operations. A supercomputer runs at {sp} {ab} (1 {ab} = 10^{int(math.log10(base))} FLOPS). Calculate how long the task takes.'
    key = f'time = operations ÷ speed = {mant} × 10^{ops_e} ÷ ({sp} × 10^{int(math.log10(base))}) [1] = {num(round(secs, 2))} s [1]' + (f' = {tfmt(secs)}' if secs >= 120 else '')
    m = 2
    ans = f'{num(round(secs, 2))} seconds' + (f' ({tfmt(secs)})' if secs >= 120 else '')
    if D >= 3:
        f2 = r.choice([2, 4, 5, 10])
        stem += f' A new machine is {f2} times faster. State the new time and explain one reason why the faster machine would benefit forecasters.'
        key += f'; new time = {tfmt(secs / f2)} [1]; more detailed models / more runs / forecasts ready sooner [1]'
        ans += f'; new machine: {tfmt(secs / f2)}; forecasts can use finer grids or be produced sooner.'
        m = 4
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


SYS_TASK = [
    ('translate a whole C++ program into machine code once, producing an executable file', 'compiler'),
    ('translate and run a Python program one line at a time, stopping at the first error', 'interpreter'),
    ('combine separately compiled modules and library routines into a single executable program', 'linker'),
    ('allow the operating system to communicate with a newly connected printer', 'device driver'),
    ('manage memory, schedule processes and provide a user interface', 'operating system'),
    ('scan files to detect and quarantine viruses', 'anti-virus utility'),
    ('rearrange file fragments on a hard disk so each file is stored in adjacent blocks', 'disk defragmenter'),
    ('reduce the size of a folder of files before emailing it', 'file compression utility'),
    ('make a copy of data on a separate device so it can be restored if lost', 'backup utility'),
    ('prepare a new disk by creating tracks, sectors and a file system', 'disk formatter'),
]

t = T(2, 'System software: compilers, interpreters, linkers, device drivers, operating systems and utilities', 'system software', 'compilers, interpreters', 'utilities',
      defs=[('compiler', 'A translator that converts the whole of a high-level language program into machine code in one go, producing an executable file.'),
            ('interpreter', 'A translator that translates and executes a high-level program one statement at a time, without producing an executable file.'),
            ('linker', 'System software that combines separately compiled modules (object code) and library routines into a single executable program.'),
            ('device driver', 'Software that allows the operating system to communicate with and control a particular hardware device.'),
            ('utility software', 'System software that performs a specific maintenance task, such as anti-virus, backup, compression, defragmentation or formatting.'),
            ('operating system', 'System software that manages the computer\'s hardware and software resources and provides an interface for the user.')],
      mcqs=[('Which translator produces an executable file that can be run without the translator?', 'Compiler', ['Interpreter', 'Linker', 'Device driver'], 'A compiler translates the whole program into an executable file.'),
            ('Why is an interpreter useful while a program is being developed?', 'It stops at the line containing an error so it can be corrected and the program re-run immediately', ['It produces faster-running code', 'It hides the source code from users', 'It combines modules into one file'],
             'Interpreters report errors line by line, which makes debugging easier.'),
            ('Which utility would most improve the speed of reading files from a heavily used magnetic hard disk?', 'Disk defragmenter', ['File compression', 'Anti-virus', 'Disk formatter'], 'Defragmenting stores each file in contiguous blocks, reducing head movement.'),
            ('A new graphics tablet does not work when it is plugged in. What software is most likely missing?', 'A device driver', ['A compiler', 'A linker', 'A backup utility'], 'The OS needs a driver to communicate with the device.')],
      exps=[('Explain two advantages of compiling a program before distributing it to customers.', 'The executable runs faster because translation is done once; customers do not need the translator; the source code is not distributed so it cannot easily be copied or changed.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why a programmer might use an interpreter during development.', 'Errors are reported as soon as the line is reached, so they can be found and corrected easily; the program can be tested in parts without compiling the whole program.', '1 mark errors located line by line; 1 mark quick testing/debugging. [2]'),
            ('Explain why a linker is needed.', 'Large programs are written and compiled as separate modules and use library routines; the linker joins them into one executable, resolving references between them.', '1 mark separate modules/libraries; 1 mark combined into single executable. [2]'),
            ('Explain why defragmenting a solid-state drive is not recommended.', 'Access time on an SSD does not depend on where data is stored, so there is no speed benefit; unnecessary writes reduce the lifespan of the flash memory.', '1 mark no speed gain (no moving parts); 1 mark extra writes reduce lifespan. [2]')],
      ars=[('A compiled program usually runs faster than an interpreted one.', 'The translation is done once, before the program is run.'),
           ('A device driver is needed for each type of hardware device.', 'The operating system needs instructions specific to that device to control it.'),
           ('Defragmentation can speed up a magnetic hard disk.', 'Each file is stored in adjacent sectors so the read head moves less.')],
      falses=['An interpreter produces an executable file.', 'A linker translates high-level code into machine code.', 'A disk formatter removes viruses from files.'],
      intros=['{p} is a programmer at {org} in {city}, writing a large application that will be sold to customers; {p} also looks after the office computers.',
              '{org} in {city} has a small IT team that writes the organisation\'s own software and maintains its 150 office computers, scanners and printers.',
              'The IT department of {org} in {city} is developing a new booking program and, at the same time, updating the software on all staff computers.'],
      parts=[('Explain why a compiler would be used to produce the final version of the program.', 'Produces an executable that runs quickly without the translator, and the source code is not given to customers.', '1 mark executable/faster; 1 mark source code protected/no translator needed. [2]'),
             ('Explain why an interpreter might be used while the program is being written.', 'Errors are found line by line so debugging is easier; code can be tested without compiling everything.', '1 mark each. [2]'),
             ('Describe the role of a linker.', 'Combines separately compiled modules and library routines into one executable program.', '1 mark modules/libraries; 1 mark single executable. [2]'),
             ('Describe the purpose of a device driver for the new devices.', 'Allows the operating system to communicate with the device by translating general commands into device-specific instructions.', '1 mark OS–device communication; 1 mark device-specific. [2]'),
             ('Describe two utilities that would help maintain the computers.', 'Anti-virus (detects/quarantines malware); backup (copies data for restoring); defragmenter (speeds HDD access); compression (saves space); disk cleanup.', '1 mark per utility with purpose, max 2. [2]'),
             ('Describe two functions of the operating system.', 'Memory management; process/task scheduling; file management; managing peripherals via drivers; security/user accounts; providing a user interface.', '1 mark each, max 2. [2]')],
      ev=[('whether {org} should distribute its software as compiled executables or as source code run with an interpreter', 'compiled code runs faster and protects intellectual property; users need no translator.', 'interpreted source runs on any platform with an interpreter and is easier to modify; compiled code must be recompiled for each platform.', 'for commercial software sold to customers, compilation is usually preferred.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch2_systask(r, D):
    if D <= 2:
        s, k = r.choice(SYS_TASK)
        return MCQ(r, f'Which type of system software is used to {s}?', k.capitalize(), [x[1].capitalize() for x in SYS_TASK if x[1] != k], f'{k.capitalize()}.')
    picks = r.sample(SYS_TASK, 3 if D == 3 else 4)
    lines = '\n'.join(f'{i + 1}. To {x[0]}.' for i, x in enumerate(picks))
    return Q(f'Name the type of system software needed for each task.\n{lines}', '; '.join(f'{i + 1} {x[1]}' for i, x in enumerate(picks)),
             '1 mark each: ' + '; '.join(f'{i + 1} {x[1]}' for i, x in enumerate(picks)) + f'. [{len(picks)}]', marks=len(picks))


t = T(2, 'Custom-written versus off-the-shelf software; proprietary and open-source software', 'custom-written versus off-the-shelf software', 'proprietary and open-source software',
      defs=[('custom-written software', 'Software written specially to meet the exact requirements of one client or organisation.'),
            ('off-the-shelf software', 'Ready-made software that is available to buy or download and is designed for a general market of many users.'),
            ('proprietary software', 'Software owned by a company or individual; users buy a licence to use it but cannot see or change the source code.'),
            ('open-source software', 'Software whose source code is made available so that users can study, modify and redistribute it, usually free of charge.')],
      mcqs=[('Which is an advantage of off-the-shelf software over custom-written software?', 'It is available immediately and has been tested by many users', ['It meets the exact needs of the organisation', 'The organisation owns the source code', 'It contains only the features required'],
             'Off-the-shelf software is ready now, cheaper (cost shared) and well tested, with plenty of support.'),
            ('Which is a feature of open-source software?', 'Users can view and modify the source code', ['It must always be bought from the developer', 'It can never be used by businesses', 'Its source code is kept secret'], 'Open source licences allow the code to be studied, changed and shared.'),
            ('Why might a hospital choose custom-written software for its patient records?', 'It can be designed to match the hospital\'s exact procedures', ['It is always cheaper than off-the-shelf software', 'It is available immediately', 'It has millions of existing users'], 'Custom software fits specific requirements, but costs more and takes longer.')],
      exps=[('Explain two disadvantages of custom-written software.', 'It is expensive because the whole development cost is paid by one client; it takes a long time to develop and test before it can be used; there may be bugs because it has few users.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why off-the-shelf software is usually cheaper than custom-written software.', 'The development cost is shared between thousands of customers, so each pays only a small part.', '1 mark cost shared; 1 mark many users. [2]'),
            ('Explain one advantage and one disadvantage of open-source software for a business.', 'Advantage: usually free and can be modified to fit needs. Disadvantage: support may be limited to online communities, and staff may need specialist skills to modify it.', '1 mark advantage + explanation; 1 mark disadvantage + explanation. [4]'),
            ('Explain why off-the-shelf software may contain features an organisation does not need.', 'It is designed for a wide market, so it includes features for many different users, which makes it larger and possibly harder to learn.', '1 mark general market; 1 mark consequence. [2]')],
      ars=[('Off-the-shelf software is usually cheaper than custom-written software.', 'Its development cost is spread across many customers.'),
           ('Custom-written software can take a long time to become available.', 'It must be designed, written and tested for that client.'),
           ('Open-source software can be adapted by an organisation.', 'Its source code is available to users.')],
      falses=['Proprietary software lets users modify the source code freely.', 'Off-the-shelf software is written for one specific client.', 'Open-source software is always of lower quality than proprietary software.'],
      adv=[('commissioning custom-written software for its booking system', ['meets its exact requirements', 'can give competitive advantage as rivals do not have it', 'the developer can provide tailored support'],
            ['high development cost', 'long wait before it is available', 'may contain bugs as it has few users']),
           ('switching from proprietary office software to an open-source office suite', ['no licence fees', 'source code can be adapted', 'not tied to one supplier'],
            ['staff need retraining', 'file compatibility problems with partners', 'support relies on communities or paid third parties'])],
      intros=['{org}, {aot} in {city}, needs new software to manage its customer bookings and payments.',
              'The directors of {org} in {city} are deciding whether to buy an off-the-shelf package or pay {org2} to write custom software.',
              '{p}, the IT manager of {org} in {city}, is reviewing the cost of software licences.'],
      parts=[('Explain two advantages of custom-written software for this organisation.', 'Exactly matches requirements; no unnecessary features; can be integrated with existing systems; may give an advantage over competitors.', '2 × 1 mark point + 1 mark context, max 2 points. [4]'),
             ('Explain two advantages of off-the-shelf software for this organisation.', 'Cheaper; available immediately; well tested with fewer bugs; lots of support, training and user forums.', '1 mark each point, 1 mark each explanation, max 2 points. [4]'),
             ('Describe what is meant by open-source software.', 'Software whose source code is available to view, modify and redistribute, usually free.', '1 mark source available; 1 mark modify/share. [2]'),
             ('Explain one risk of using proprietary software from a single supplier.', 'Vendor lock-in: the organisation depends on the supplier for updates and prices; if the supplier stops supporting it, the organisation must change systems.', '1 mark dependency; 1 mark consequence. [2]')],
      ev=[('whether {org} should commission custom-written software or buy an off-the-shelf package', 'custom fits needs exactly and may give competitive advantage; off-the-shelf is cheap, quick and tested.', 'custom is expensive, slow and may be buggy; off-the-shelf may not fit processes and contains unneeded features.', 'it depends on how unusual the organisation\'s needs are, its budget and how quickly the system is needed.'),
          ('the use of open-source software by {org}', 'no licence cost; adaptable; large communities; not tied to one supplier.', 'support can be limited; training costs; compatibility issues; may need in-house expertise.', 'suitable if the organisation has technical staff or a support contract.')])


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ch2_costs(r, D):
    hours = r.choice([400, 600, 800, 1000, 1200, 1500])
    rate = r.choice([40, 50, 60, 75, 80])
    maint = r.choice([2000, 3000, 4000, 5000])
    users = r.choice([20, 25, 40, 50, 80, 100])
    lic = r.choice([150, 200, 250, 300, 400])
    sub = r.choice([60, 80, 100, 120, 150])
    yrs = r.choice([3, 4, 5]) if D <= 3 else r.choice([5, 6, 8])
    custom = hours * rate + maint * yrs
    ots = users * lic + users * sub * yrs
    d = ctx(r)
    stem = (f'{d["org"]} in {d["city"]} needs software for {users} staff. Option A: custom-written software taking {hours} hours at ${rate} per hour, plus ${maint:,} per year maintenance. '
            f'Option B: an off-the-shelf package at ${lic} per user licence, plus ${sub} per user per year for support. Calculate the total cost of each option over {yrs} years and state which is cheaper.')
    key = f'A: {hours} × {rate} + {maint:,} × {yrs} = ${custom:,} [1]; B: {users} × {lic} + {users} × {sub} × {yrs} = ${ots:,} [1]; cheaper: {"A" if custom < ots else ("B" if ots < custom else "equal")} [1]'
    ans = f'A ${custom:,}; B ${ots:,}; ' + ('A (custom) is cheaper' if custom < ots else ('B (off-the-shelf) is cheaper' if ots < custom else 'they cost the same'))
    m = 3
    if D >= 4:
        a1, b1 = hours * rate, users * lic
        pa, pb = maint, users * sub
        if pa == pb:
            return None
        n = (a1 - b1) / (pb - pa)
        if n > 0:
            ans += f'; the costs are equal after {n:.1f} years'
            key += f'; break-even: {a1:,} + {pa:,}n = {b1:,} + {pb:,}n → n = {n:.1f} years [1]'
        else:
            ans += '; one option is cheaper in every year, so there is no break-even point'
            key += '; no break-even: one option is cheaper initially and per year [1]'
        stem += ' Calculate after how many years the two options would cost the same, if ever, and give one non-financial factor the organisation should consider.'
        ans += '; non-financial: fit to requirements / time to implement / support / bugs.'
        key += '; non-financial factor e.g. fit to requirements, time until available, quality of support [1]'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


UIS = [
    ('a network technician who needs to configure many servers quickly using scripts', 'command line interface'),
    ('a young child using an educational app on a tablet', 'gesture-based interface'),
    ('a driver who wants to set the destination on a satellite navigation system while driving', 'dialogue (voice) interface'),
    ('an office worker who uses a word processor, spreadsheet and email every day', 'graphical user interface'),
    ('a surgeon who needs to move through X-ray images without touching anything during an operation', 'gesture-based interface'),
    ('a person with limited hand movement controlling smart lights at home', 'dialogue (voice) interface'),
    ('a programmer automating repetitive file operations', 'command line interface'),
    ('a visitor using a touch-screen information kiosk in a museum', 'graphical user interface'),
]

t = T(2, 'User interfaces: command line, graphical, dialogue and gesture-based', 'user interfaces', 'command line, graphical, dialogue and gesture-based',
      defs=[('command line interface (CLI)', 'An interface in which the user types commands at a prompt, using exact syntax, to instruct the computer.'),
            ('graphical user interface (GUI)', 'An interface that uses windows, icons, menus and a pointer (WIMP) so the user can interact by pointing and clicking or touching.'),
            ('dialogue interface', 'An interface in which the user communicates with the computer using spoken (or typed natural-language) words and the computer replies.'),
            ('gesture-based interface', 'An interface in which the computer recognises movements of the user\'s body, such as hand movements or touch gestures, as commands.')],
      mcqs=[('Which interface uses the least memory and processing power?', 'Command line interface', ['Graphical user interface', 'Gesture-based interface', 'Dialogue interface'], 'A CLI has no graphics to display or speech/gesture recognition to perform.'),
            ('Which is a disadvantage of a dialogue (voice) interface?', 'Background noise can stop commands being recognised', ['It needs the user to remember many commands', 'It requires a keyboard', 'It cannot be used hands-free'], 'Speech recognition may fail with noise or accents.'),
            ('Which interface is most suitable for an expert who wants to perform tasks quickly with scripts?', 'Command line interface', ['Gesture-based interface', 'Dialogue interface', 'Graphical user interface'], 'Commands can be combined and scripted, giving direct control.')],
      exps=[('Explain two advantages of a GUI for a beginner.', 'It is intuitive: users click icons and menus rather than remember commands; options are visible so less training is needed; help and undo are easy to find.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why a command line interface is still used by network administrators.', 'Commands give direct, fast access to all system functions and can be scripted to repeat tasks on many machines; it uses few resources and works over remote text connections.', '1 mark speed/direct control; 1 mark scripting/remote/low resources. [2]'),
            ('Explain one advantage and one disadvantage of a gesture-based interface.', 'Advantage: natural and hands-free (no contact needed, e.g. in surgery). Disadvantage: accidental movements may be recognised as commands and it can be tiring to use for long periods.', '1 mark advantage; 1 mark disadvantage. [2]'),
            ('Explain why a dialogue interface is useful in a car.', 'The driver can give commands by voice without taking hands off the wheel or eyes off the road, which is safer.', '1 mark hands-free/eyes-free; 1 mark safety. [2]')],
      ars=[('A command line interface is difficult for beginners.', 'Users must remember exact commands and syntax.'),
           ('A GUI requires more processing power and memory than a CLI.', 'It has to display windows, icons and graphics.'),
           ('Dialogue interfaces can be unreliable in noisy places.', 'Background noise interferes with speech recognition.')],
      falses=['A CLI uses icons and menus.', 'Gesture-based interfaces need the user to type commands.', 'A GUI uses less memory than a CLI.'],
      intros=['{org}, {aot} in {city}, is choosing the interface for a new information system used by staff and the public.',
              '{p} is designing interfaces for the staff, the public and the technicians of {org} in {city}.',
              'The IT team at {org} in {city} use different interfaces for different jobs.'],
      parts=[('Describe two features of a graphical user interface.', 'Windows; icons; menus; pointer (WIMP); drag and drop; touch controls.', '1 mark each, max 2. [2]'),
             ('Explain why a dialogue interface could be useful for some users.', 'Hands-free use; useful for users with limited mobility or sight; natural to use.', '1 mark point; 1 mark explanation. [2]'),
             ('Explain one disadvantage of a gesture-based interface.', 'Unintended gestures may trigger commands; tiring; needs a camera/sensors; limited number of gestures recognised.', '1 mark point; 1 mark explanation. [2]'),
             ('Explain why the technicians might prefer a command line interface.', 'Faster for experts; commands can be scripted and run on many computers; low resource use; access to all settings.', '1 mark point; 1 mark explanation. [2]'),
             ('Compare a GUI and a CLI in terms of ease of learning and use of resources.', 'GUI is easier to learn as options are visible; CLI requires memorising commands; GUI uses more memory and processing power.', '1 mark ease of learning; 1 mark resources. [2]')],
      ev=[('whether {org} should use a dialogue (voice) interface instead of a graphical user interface for its public information system', 'hands-free; accessible to people with visual impairment; natural for occasional users.', 'background noise; accents and languages; privacy of spoken queries; a GUI shows options clearly.', 'a combined interface (GUI with optional voice) is likely to suit most users.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch2_ui(r, D):
    s, k = r.choice(UIS)
    if D <= 2:
        return MCQ(r, f'Which type of user interface is most suitable for {s}?', k.capitalize(), [x.capitalize() for x in ('command line interface', 'graphical user interface', 'dialogue (voice) interface', 'gesture-based interface') if x != k],
                   f'{k.capitalize()} best suits this user.')
    s2, k2 = r.choice([x for x in UIS if x[1] != k])
    return Q(f'Recommend a suitable user interface for each user and justify your choices: (1) {s}; (2) {s2}.', f'(1) {k}; (2) {k2}.',
             f'(1) {k} [1] with reason linked to the user [1]; (2) {k2} [1] with reason linked to the user [1]. [4]', marks=4)


# =============================================================================== Chapter 3 Monitoring and control
SENSORS = [('the temperature in a greenhouse', 'temperature sensor'), ('whether there is enough daylight to switch off street lights', 'light sensor'),
           ('when soil in a field needs watering', 'moisture sensor'), ('the humidity in a museum display case', 'humidity sensor'),
           ('an intruder moving in a building at night', 'infrared (motion) sensor'), ('the acidity of water in a fish tank', 'pH sensor'),
           ('when a car is close to a wall while parking', 'proximity (ultrasonic) sensor'), ('the amount of carbon dioxide in a classroom', 'gas (CO₂) sensor'),
           ('when a vehicle is waiting at a traffic light', 'pressure (or induction loop) sensor'), ('the level of noise near an airport', 'sound sensor'),
           ('a patient\'s blood oxygen level', 'oxygen (pulse oximeter) sensor'), ('the water level in a river', 'pressure (or ultrasonic level) sensor')]
SENS_NAMES = sorted({x[1] for x in SENSORS})

t = T(3, 'Sensors used in monitoring and control systems', 'sensors used in monitoring and control systems', 'sensors',
      defs=[('sensor', 'An input device that measures a physical quantity, such as temperature or light, and sends the reading to the computer.'),
            ('analogue-to-digital converter (ADC)', 'A device that converts the continuous analogue signal from a sensor into digital data that the computer can process.'),
            ('actuator', 'An output device, such as a motor, valve or pump, that carries out a physical action when it receives a signal from the computer.'),
            ('data logger', 'A device that automatically records sensor readings at set intervals over a period of time.')],
      mcqs=[('Why is an analogue-to-digital converter needed between most sensors and a computer?', 'Sensors produce analogue signals but computers process digital data', ['Computers produce analogue signals that sensors cannot read', 'It makes the sensor more accurate', 'It stores the readings permanently'],
             'Physical quantities vary continuously; the ADC converts them to binary values.'),
            ('Which sensor would detect that a door has been opened in a burglar alarm system?', 'A magnetic contact (or infrared) sensor', ['A pH sensor', 'A humidity sensor', 'A temperature sensor'], 'Contact or infrared sensors detect opening/movement.'),
            ('Which statement about sensors is correct?', 'A sensor only sends readings; the computer decides what action to take', ['A sensor switches a heater on and off', 'A sensor turns readings into decisions', 'A sensor stores the preset value'],
             'Sensors are input devices; processing and decisions are done by the microprocessor.')],
      exps=[('Explain why a sensor does not control the device it is monitoring.', 'A sensor is only an input device that measures a quantity; the microprocessor compares the reading with a preset value and sends signals to an actuator to make changes.', '1 mark sensor measures/input only; 1 mark microprocessor decides/actuator acts. [2]'),
            ('Explain why sensor readings are taken at regular intervals rather than continuously.', 'The computer processes digital samples; regular sampling gives enough data to see changes while limiting the amount of data stored and processed.', '1 mark discrete samples; 1 mark enough detail without excess data. [2]'),
            ('Explain why using sensors to monitor a river can be better than sending a person to take readings.', 'Sensors can take readings continuously, day and night, in dangerous places and at accurate intervals; there is no human error and staff costs are lower.', '1 mark per point, max 3. [3]')],
      ars=[('A temperature sensor needs an ADC to be connected to a computer.', 'The sensor produces an analogue signal.'),
           ('Sensors are input devices.', 'They send measurements of physical quantities to the computer.'),
           ('Computer monitoring can take readings more frequently than a person.', 'Readings can be taken automatically at very short intervals without breaks.')],
      falses=['A sensor decides when to switch a heater on.', 'An actuator measures physical quantities.', 'Sensors output digital data that never needs converting.'],
      intros=['{org}, {aot} in {city}, is installing a computer system to monitor conditions in its storage rooms.',
              '{p} is designing an automatic system for the greenhouses of {org} near {city}.',
              'Engineers at {org} in {city} are fitting sensors to a new building.'],
      parts=[('Name two sensors that could be used and state what each measures.', 'e.g. temperature sensor (temperature); humidity sensor (moisture in air); light sensor (light level); infrared sensor (movement).', '1 mark each sensor with quantity, max 2. [2]'),
             ('Explain why an analogue-to-digital converter is needed.', 'Sensors produce continuous analogue signals; the computer can only process digital data.', '1 mark analogue output; 1 mark computer needs digital. [2]'),
             ('Explain why the sensor does not itself control the conditions.', 'Sensors only measure; the microprocessor compares readings with preset values and sends signals to actuators.', '1 mark each. [2]'),
             ('Give two advantages of using sensors rather than human readings.', 'Readings taken 24 hours a day; more accurate; at exact intervals; in dangerous places; staff freed for other work.', '1 mark each, max 2. [2]'),
             ('Describe what is meant by an actuator and give an example.', 'An output device that performs a physical action in response to a signal, e.g. motor, valve, pump, heater switch.', '1 mark description; 1 mark example. [2]')],
      ev=[('whether {org} should replace manual checks by staff with an automatic sensor-based monitoring system', 'continuous, accurate readings; works in dangerous places; staff freed; immediate alerts.', 'cost of sensors and installation; sensors can fail or drift and need calibration; staff may lose skills; reliance on power and network.', 'automatic monitoring is usually worthwhile if readings are frequent or the environment is hazardous, with periodic human checks.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch3_sensor(r, D):
    if D <= 2:
        s, k = r.choice(SENSORS)
        return MCQ(r, f'Which sensor would be used to measure {s}?', k.capitalize(), [x.capitalize() for x in SENS_NAMES if x != k], f'{k.capitalize()}.')
    picks = r.sample(SENSORS, 3 if D == 3 else 4)
    lines = '\n'.join(f'{i + 1}. {cap(x[0])}' for i, x in enumerate(picks))
    return Q(f'Name the most suitable sensor for each application.\n{lines}', '; '.join(f'{i + 1} {x[1]}' for i, x in enumerate(picks)),
             '1 mark each: ' + '; '.join(f'{i + 1} {x[1]}' for i, x in enumerate(picks)) + f'. [{len(picks)}]', marks=len(picks))


t = T(3, 'Monitoring systems: environmental, weather stations and patient monitoring', 'monitoring systems', 'weather stations', 'patient monitoring',
      defs=[('monitoring system', 'A system in which sensors measure physical quantities and the computer records and displays them, and may give warnings, but does not change the conditions.'),
            ('sampling interval', 'The time between one sensor reading being taken and the next.'),
            ('weather station', 'A set of sensors (temperature, rainfall, wind speed, wind direction, pressure, humidity) whose readings are logged and sent to a computer.'),
            ('patient monitoring', 'Using sensors attached to a patient to measure vital signs such as heart rate, blood pressure and temperature, with alarms when readings go out of range.')],
      mcqs=[('What is the difference between a monitoring system and a control system?', 'A monitoring system only records and reports readings; a control system also takes action to change conditions', ['A monitoring system uses actuators', 'A control system never uses sensors', 'Monitoring systems cannot give warnings'],
             'Monitoring = observe and report; control = feedback to actuators.'),
            ('In patient monitoring, what happens when a reading goes outside the preset range?', 'An alarm is sounded to alert the nurse', ['The sensor is switched off', 'The patient\'s medicine is changed automatically', 'The reading is deleted'], 'The computer compares readings with limits and warns staff.'),
            ('Which sensor is used to measure rainfall in a weather station?', 'A rain gauge sensor that counts tipping-bucket movements', ['A pH sensor', 'A light sensor', 'A gas sensor'], 'A tipping-bucket gauge measures rainfall amount.')],
      exps=[('Explain why computerised patient monitoring helps nurses.', 'Vital signs are measured continuously and accurately, and an alarm alerts nurses immediately if a reading is out of range, so nurses can care for more patients and respond faster.', '1 mark continuous/accurate; 1 mark alarm; 1 mark frees staff/faster response. [3]'),
            ('Explain why a shorter sampling interval might be chosen for a patient than for a river.', 'A patient\'s condition can change very quickly and must be detected immediately, whereas river conditions change slowly so fewer readings are enough.', '1 mark patient changes rapidly; 1 mark river slower. [2]'),
            ('Describe how data from a remote weather station reaches a forecasting centre.', 'Sensors take readings, an ADC converts them, a data logger stores them, and they are transmitted via mobile network/satellite to the centre\'s computer for processing.', '1 mark per stage, max 3. [3]')],
      ars=[('A weather station can be left unattended in remote places.', 'Readings are logged automatically and transmitted to a computer.'),
           ('Patient monitoring systems sound an alarm when readings are abnormal.', 'Readings are compared with preset upper and lower limits.'),
           ('A monitoring system does not use actuators to change conditions.', 'It only records, displays and reports readings.')],
      falses=['A monitoring system automatically switches heaters on and off.', 'Patient monitoring removes the need for any nurses.', 'Weather stations only measure temperature.'],
      intros=['{org} in {city} wants to monitor pollution in a nearby river.',
              'A hospital ward run by {org} in {city} uses sensors to monitor patients after surgery.',
              '{p} is setting up an automatic weather station for {org} in a remote area near {city}.'],
      parts=[('Name three sensors that would be used and state what each measures.', 'e.g. temperature, pH (acidity), oxygen level, turbidity/light, rainfall, wind speed, pressure, heart rate, blood pressure.', '1 mark each, max 3. [3]'),
             ('Describe how the computer processes the sensor readings.', 'Readings are converted by an ADC, stored, compared with preset limits; graphs/tables are produced; warnings given if out of range.', '1 mark per point, max 3. [3]'),
             ('Explain why computer monitoring is better than taking manual readings.', 'Readings taken continuously day and night; no human error; works in remote/dangerous places; faster response to problems.', '1 mark per point, max 2. [2]'),
             ('Explain why this is a monitoring system and not a control system.', 'The computer only records and reports readings; it does not use actuators to change the conditions.', '1 mark records/reports; 1 mark no actuators/no feedback. [2]'),
             ('Explain one disadvantage of using a computerised monitoring system here.', 'Sensors can fail, drift or be damaged and give false readings; equipment is expensive; staff may over-rely on alarms.', '1 mark point; 1 mark explanation. [2]')],
      ev=[('whether computerised patient monitoring can replace regular checks by nurses', 'continuous accurate readings; immediate alarms; nurses freed for other care; data stored for trends.', 'false alarms and alarm fatigue; sensors detach or fail; patients need human care and observation of symptoms sensors cannot measure.', 'monitoring supports but cannot fully replace nurses.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch3_logging(r, D):
    unit, per = r.choice([('seconds', 1), ('minutes', 60)])
    iv = r.choice([5, 10, 15, 20, 30]) if unit == 'seconds' else r.choice([1, 2, 5, 10, 15, 30])
    dur_h = r.choice([1, 2, 6, 12, 24, 48]) if unit == 'seconds' else r.choice([24, 48, 72, 168])
    n = dur_h * 3600 // (iv * per)
    sens = r.choice([2, 3, 4, 5])
    b = r.choice([2, 4])
    place = r.choice(['a river', 'a greenhouse', 'a patient on a hospital ward', 'a weather station', 'a museum display case', 'a cold-storage warehouse'])
    dstr = f'{dur_h} hours' if dur_h < 72 else f'{dur_h // 24} days'
    if D == 1:
        return MCQ(r, f'A data logger in {place} takes one reading every {iv} {unit} for {dstr}. How many readings does it take?', f'{n:,}',
                   [f'{n * 60:,}' if unit == 'seconds' else f'{n // 60:,}', f'{n * 2:,}', f'{dur_h * iv:,}', f'{n // 2:,}'], f'{dur_h} × 3600 ÷ {iv * per} = {n:,}.')
    stem = f'A data logger in {place} takes a reading from each of {sens} sensors every {iv} {unit} for {dstr}. Calculate the number of readings taken from each sensor'
    key = f'{dur_h} h = {dur_h * 3600:,} s; {dur_h * 3600:,} ÷ {iv * per} = {n:,} readings [1]'
    ans = f'{n:,} readings per sensor'
    m = 1
    if D >= 2:
        tot = n * sens * b
        stem += f' and the storage needed if each reading is stored in {b} bytes. Give your answer in kilobytes (1 KB = 1024 bytes)'
        key += f'; {n:,} × {sens} × {b} = {tot:,} bytes [1] = {num(round(tot / 1024, 2))} KB [1]'
        ans += f'; {tot:,} bytes = {num(round(tot / 1024, 2))} KB'
        m = 3
    if D >= 4:
        stem += '. Explain why the sampling interval chosen should depend on how quickly the quantity changes'
        key += '; fast-changing quantities need short intervals to catch changes; slow ones can use longer intervals to save storage [1]'
        ans += '; quickly changing quantities need shorter intervals so changes are not missed.'
        m = 4
    return Q(stem + '.', ans, key + f'. [{m}]', marks=m, typ='numerical')


# ------------------------------------------------------------------ control
CTRL = [('greenhouse', 'temperature', '°C', 'heater', 'window motor', (18, 26)), ('central heating system', 'temperature', '°C', 'boiler', 'pump', (19, 23)),
        ('aquarium', 'temperature', '°C', 'heater', 'cooling fan', (24, 27)), ('cold store', 'temperature', '°C', 'compressor', 'alarm', (-20, -16)),
        ('greenhouse', 'soil moisture', '%', 'water valve', 'water valve', (35, 60)), ('server room', 'temperature', '°C', 'air conditioning', 'alarm', (18, 24))]

t = T(3, 'Control systems, microprocessors, actuators and feedback (greenhouse, central heating, traffic lights)', 'control systems', 'microprocessors, actuators and feedback', 'greenhouse, central heating, traffic lights',
      defs=[('control system', 'A system in which a microprocessor uses sensor readings to make decisions and sends signals to actuators to change the conditions being measured.'),
            ('feedback', 'The process in which the output of a control system affects the next input, so the system continually adjusts to keep conditions near the preset value.'),
            ('preset value', 'The target value (or range) stored in the control system, with which sensor readings are compared.'),
            ('microprocessor', 'The processing chip in a control system that receives sensor data, compares it with preset values and sends signals to actuators.')],
      mcqs=[('In a central heating system, what does the microprocessor do when the temperature is below the preset value?', 'Sends a signal to switch the boiler on', ['Sends a signal to switch the boiler off', 'Switches off the temperature sensor', 'Lowers the preset value'],
             'The reading is below target, so heat is needed.'),
            ('Why is a traffic-light control system an example of feedback?', 'Changes to the lights affect the traffic, which affects the next sensor readings', ['The lights change on a fixed timer only', 'The sensors are switched off at night', 'Drivers press a button'],
             'Output (lights) changes the input (queues) in a continuous loop.'),
            ('Which device in a greenhouse control system opens the windows?', 'A motor (actuator)', ['A temperature sensor', 'An ADC', 'A data logger'], 'Actuators carry out physical actions.')],
      exps=[('Describe how a microprocessor controls the temperature in a greenhouse.', 'The temperature sensor sends readings via an ADC; the microprocessor compares each reading with the preset range; if too low it switches the heater on (and closes windows); if too high it switches the heater off and opens windows via a motor; this repeats continuously.', '1 mark per step, max 4. [4]'),
            ('Explain what is meant by feedback in a control system, using an example.', 'The output affects the next input: e.g. switching a heater on raises the temperature, which the sensor measures and the microprocessor uses to decide when to switch the heater off.', '1 mark output affects input; 1 mark continuous loop; 1 mark example. [3]'),
            ('Explain why a DAC may be needed in a control system.', 'Some actuators need an analogue signal (e.g. to vary motor speed), so the digital output from the microprocessor must be converted.', '1 mark actuator needs analogue; 1 mark converts digital output. [2]'),
            ('Explain how sensors are used in a traffic-light control system.', 'Pressure/induction-loop or infrared sensors detect waiting vehicles; the microprocessor uses this to change light timings, e.g. extending green for a busy road.', '1 mark sensor detects vehicles; 1 mark microprocessor adjusts timing. [2]')],
      ars=[('A central heating system is an example of a control system with feedback.', 'Switching the boiler changes the temperature that is measured next.'),
           ('An actuator is needed to open a greenhouse window.', 'A motor is required to carry out the physical movement.'),
           ('The microprocessor compares readings with preset values.', 'Decisions are made by comparing the current reading with the target.')],
      falses=['Sensors switch actuators on directly without a microprocessor.', 'A control system does not use input devices.', 'Feedback means the system only runs once.'],
      intros=['{org} grows tomatoes in computer-controlled greenhouses near {city}.',
              'A new office block owned by {org} in {city} has a microprocessor-controlled central heating system.',
              'The council in {city} has asked {org} to install microprocessor-controlled traffic lights at a busy junction.'],
      parts=[('Name two sensors that would be used in this system.', 'e.g. temperature, light, moisture, humidity, pressure/induction loop, infrared.', '1 mark each, max 2. [2]'),
             ('Name two actuators that would be used and state what each does.', 'e.g. motor (opens windows/moves barrier), heater/boiler switch, pump, valve, light switch.', '1 mark each with action, max 2. [2]'),
             ('Describe how the microprocessor uses the sensor readings to control the system.', 'Reading converted by ADC; compared with preset value; if outside range a signal is sent to the actuator; loop repeats continuously.', '1 mark per step, max 4. [4]'),
             ('Explain how feedback is used in this system.', 'The action of the actuator changes the conditions, which are measured again and affect the next decision, keeping conditions close to the preset value.', '1 mark output affects input; 1 mark continuous adjustment. [2]'),
             ('Explain two advantages of computer control over manual control here.', 'Responds faster; works 24 hours; more accurate/consistent conditions; saves energy and labour costs.', '1 mark each, max 2. [2]')],
      ev=[('whether {org} benefits more than it loses from using microprocessor-controlled systems', 'conditions kept constant; 24-hour operation; energy savings; lower labour costs; faster responses.', 'high installation and maintenance costs; sensor failure may cause damage; staff need training; loss of jobs or skills.', 'the benefits usually outweigh the costs where precise conditions are important, provided there are alarms and manual overrides.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch3_trace(r, D):
    place, qty, u, act1, act2, (lo, hi) = r.choice(CTRL)
    n = 5 if D <= 2 else (6 if D <= 4 else 8)
    vals = []
    for _ in range(n):
        vals.append(r.choice([lo - r.randrange(1, 4), r.randrange(lo, hi + 1), hi + r.randrange(1, 4)]))
    if qty == 'soil moisture':
        def act(v):
            return f'{act1} OPEN' if v < lo else (f'{act1} CLOSED' if v > hi else 'no change')
        rule = [f'IF Moisture < {lo} THEN open the water valve', f'IF Moisture > {hi} THEN close the water valve']
    else:
        def act(v):
            return f'{act1} ON' if v < lo else (f'{act1} OFF, {act2} ON' if v > hi else 'no change')
        rule = [f'IF Temp < {lo} THEN switch {act1} ON', f'IF Temp > {hi} THEN switch {act1} OFF and {act2} ON']
    outs = [act(v) for v in vals]
    if D == 1:
        v = vals[0]
        return MCQ(r, f'A {place} control system uses these rules: {rule[0]}; {rule[1]}; otherwise no change. The {qty} reading is {v}{u}. What does the microprocessor do?',
                   cap(outs[0]).rstrip('.'), [cap(x).rstrip('.') for x in {act(lo - 1), act(hi + 1), 'no change', f'{act1} OFF', 'Sensor switched off'} if x != outs[0]], f'{v}{u} compared with {lo}–{hi}: {outs[0]}.')
    stem = (f'A microprocessor controls a {place}. Every minute it reads the {qty} sensor and applies these rules:\n' + '\n'.join(rule) + '\n'
            f'Readings ({u}): ' + ', '.join(map(str, vals)) + '. State the action taken after each reading.')
    m = n
    key = '; '.join(f'{v}{u} → {o}' for v, o in zip(vals, outs)) + ' (1 mark each)'
    if D >= 4:
        stem += ' Explain why the system uses a range rather than a single preset value.'
        key += '; a range prevents the actuator switching on and off too frequently (rapid cycling) [1]'
        m += 1
    return Q(stem, '; '.join(f'{v} {o}' for v, o in zip(vals, outs)), key + f'. [{m}]', marks=m, typ='numerical')


t = T(3, 'Writing control algorithms for monitoring and control scenarios', 'writing control algorithms', 'control algorithms',
      defs=[('algorithm', 'A sequence of precise steps that solves a problem or carries out a task.'),
            ('infinite loop (in control)', 'A loop with no exit condition, used so that a control system keeps reading sensors and responding for as long as it is switched on.'),
            ('threshold', 'A preset value that a sensor reading is compared with to decide whether an action is needed.')],
      mcqs=[('Why does a control algorithm usually run inside a loop that never ends?', 'So the system continually reads the sensors and responds while it is switched on', ['So it only reads each sensor once', 'Because loops make the program shorter', 'So it can stop after one error'],
             'Control is continuous: read, compare, act, repeat.'),
            ('In a control algorithm, which step comes immediately after reading the sensor value?', 'Compare the value with the preset value', ['Switch the actuator off', 'Stop the program', 'Delete the reading'], 'Read → compare → act.')],
      exps=[('Explain why a control algorithm includes a wait/delay before reading the sensor again.', 'The actuator needs time to change the conditions, and reading constantly wastes processing and may cause the actuator to switch on and off rapidly.', '1 mark time to take effect; 1 mark avoid rapid switching/wasted processing. [2]'),
            ('Explain why ELSE IF is used rather than two separate IF statements when checking upper and lower limits.', 'A value cannot be both below the lower and above the upper limit, so once one condition is true the other does not need testing; it makes the logic clearer and more efficient.', '1 mark mutually exclusive; 1 mark efficiency/clarity. [2]'),
            ('Describe the steps a burglar-alarm control algorithm repeats.', 'Read the infrared/door sensors; if movement detected and the alarm is set, sound the siren and send an alert; otherwise continue; repeat.', '1 mark read; 1 mark compare/condition; 1 mark act; 1 mark repeat. [4]')],
      ars=[('Control algorithms are usually written as continuous loops.', 'The system must keep monitoring for as long as it is switched on.'),
           ('A control algorithm compares sensor readings with stored values.', 'Decisions depend on whether readings are above or below the thresholds.')],
      falses=['Control algorithms read each sensor only once.', 'An actuator decides what the algorithm should do.'],
      intros=['{org} in {city} wants an automatic system to keep its cold store between −20 °C and −16 °C.',
              '{p} is writing the control program for an automatic watering system for the gardens of {org} in {city}.',
              'Engineers at {org} in {city} are programming a car-park barrier that opens when a car arrives and closes when it has passed.'],
      parts=[('Identify the inputs and outputs of the system.', 'Inputs: sensor readings (temperature/moisture/pressure or infrared); outputs: signals to actuators (compressor, valve, motor, alarm).', '1 mark inputs; 1 mark outputs. [2]'),
             ('Write an algorithm, in pseudocode, for the control system.', 'REPEAT; read sensor; IF reading outside limit THEN switch actuator on/open ELSE IF other limit THEN off/close ENDIF; wait; UNTIL system switched off.', '1 mark loop; 1 mark read; 1 mark correct comparisons; 1 mark correct actions. [4]'),
             ('Explain why a delay is included in the loop.', 'Gives time for actuators to affect conditions and prevents rapid switching.', '1 mark each. [2]'),
             ('Describe how the system could warn staff if something goes wrong.', 'If readings stay out of range for a set time, sound an alarm/send a text message.', '1 mark condition; 1 mark warning output. [2]')],
      ev=[('the advantages and disadvantages for {org} of relying on an automatic control algorithm rather than staff', 'consistent decisions; works continuously; fast; lower labour costs.', 'cannot deal with situations not programmed; sensor faults lead to wrong actions; needs testing and maintenance.', 'automatic control is reliable for routine conditions but needs alarms and human oversight for faults.')])

CALGS = [
    ('cold store', 'Temp', 'the temperature in °C', 'compressor', -20, -16),
    ('greenhouse', 'Temp', 'the temperature in °C', 'heater', 18, 25),
    ('plant nursery', 'Moisture', 'the soil moisture in %', 'pump', 30, 55),
    ('public aquarium tank', 'Temp', 'the water temperature in °C', 'heater', 24, 27),
    ('museum storeroom', 'Humidity', 'the humidity in %', 'humidifier', 40, 60),
]


def _ctrl_alg(name, var, lo, hi, act, mode):
    """mode 'low_on': actuator ON when below lo, OFF when above hi (heater/pump/humidifier);
    'high_on': ON when above hi, OFF when below lo (compressor/cooler)."""
    if mode == 'low_on':
        return ['REPEAT', f'{IND}INPUT {var}', f'{IND}IF {var} < {lo} THEN', f'{IND}{IND}{act.capitalize()} ← "ON"', f'{IND}ELSE', f'{IND}{IND}IF {var} > {hi} THEN',
                f'{IND}{IND}{IND}{act.capitalize()} ← "OFF"', f'{IND}{IND}ENDIF', f'{IND}ENDIF', f'{IND}OUTPUT {act.capitalize()}', 'UNTIL SystemOff = TRUE']
    return ['REPEAT', f'{IND}INPUT {var}', f'{IND}IF {var} > {hi} THEN', f'{IND}{IND}{act.capitalize()} ← "ON"', f'{IND}ELSE', f'{IND}{IND}IF {var} < {lo} THEN',
            f'{IND}{IND}{IND}{act.capitalize()} ← "OFF"', f'{IND}{IND}ENDIF', f'{IND}ENDIF', f'{IND}OUTPUT {act.capitalize()}', 'UNTIL SystemOff = TRUE']


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch3_algtrace(r, D):
    name, var, desc, act, lo, hi = r.choice(CALGS)
    mode = 'high_on' if act == 'compressor' else 'low_on'
    lines = _ctrl_alg(name, var, lo, hi, act, mode)
    n = 4 if D <= 2 else (5 if D <= 4 else 7)
    vals = [r.choice([lo - r.randrange(1, 4), r.randrange(lo, hi + 1), hi + r.randrange(1, 4)]) for _ in range(n)]
    st0 = r.choice(['ON', 'OFF'])
    # recompute with stated initial state
    state = st0
    outs = []
    for v in vals:
        if mode == 'low_on':
            state = 'ON' if v < lo else ('OFF' if v > hi else state)
        else:
            state = 'ON' if v > hi else ('OFF' if v < lo else state)
        outs.append(state)
    stem = (f'This algorithm controls a {act} in a {name}. {var} is {desc}. At the start, {act.capitalize()} is "{st0}".\n' + code(lines) +
            f'\nThe inputs for {var} are: ' + ', '.join(map(str, vals)) + f'. Complete a trace table showing the value output after each input.')
    m = n
    key = '; '.join(f'{v} → {o}' for v, o in zip(vals, outs)) + ' (1 mark each)'
    if D >= 4:
        stem += f' Explain why the output does not change when {var} is between {lo} and {hi}.'
        key += f'; between {lo} and {hi} neither condition is true so the variable keeps its previous value (prevents rapid switching) [1]'
        m += 1
    return Q(stem, '; '.join(outs), key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C2', (2, 3, 4), 'explain')
def ch3_algbug(r, D):
    name, var, desc, act, lo, hi = r.choice(CALGS)
    mode = 'high_on' if act == 'compressor' else 'low_on'
    lines = _ctrl_alg(name, var, lo, hi, act, mode)
    kind = r.choice(['op', 'state', 'loop'])
    if kind == 'op':
        i = 2
        good = lines[i]
        lines[i] = lines[i].replace('<', '>') if '<' in lines[i] else lines[i].replace('>', '<')
        expl = f'Line 3 should be "{good.strip()}": the comparison operator is the wrong way round, so the {act} switches on at the wrong time.'
    elif kind == 'state':
        i = 6
        good = lines[i]
        lines[i] = lines[i].replace('"OFF"', '"ON"')
        expl = f'Line 7 should be "{good.strip()}": the {act} is set ON in both branches, so it can never be switched off.'
    else:
        i = 10
        good = lines[i]
        lines[i] = 'UNTIL TRUE'
        expl = f'Line 11 should be "{good}": UNTIL TRUE ends the loop after one pass, so the sensor is read only once instead of continuously.'
    numbered = code([f'{j + 1:>2}  {x}' for j, x in enumerate(lines)])
    stem = f'This algorithm is meant to keep {var} between {lo} and {hi} in a {name} by controlling a {act}. It contains one error.\n{numbered}\nIdentify the line with the error, explain the problem and write the corrected line.'
    return {'stem': stem, 'answer': expl, 'key': f'1 mark line {i + 1}; 1 mark explanation; 1 mark correct line "{good.strip()}". [3]', 'marks': 3, 'type': 'explain'}


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def ch3_write(r, D):
    name, var, desc, act, lo, hi = r.choice(CALGS)
    mode = 'high_on' if act == 'compressor' else 'low_on'
    alarm = D >= 4
    d = ctx(r)
    lines = _ctrl_alg(name, var, lo, hi, act, mode)
    if alarm:
        lines = lines[:-1] + [f'{IND}IF {var} < {lo - 5} OR {var} > {hi + 5} THEN', f'{IND}{IND}OUTPUT "ALARM"', f'{IND}ENDIF', f'{IND}WAIT 60', lines[-1]]
    stem = (f'{d["org"]} in {d["city"]} needs a control program for a {name}. {var} is {desc}. The {act} must be switched ' +
            (f'ON when {var} is below {lo} and OFF when it is above {hi}' if mode == 'low_on' else f'ON when {var} is above {hi} and OFF when it is below {lo}') +
            '. The system must keep running until it is switched off' + (f', and must output "ALARM" if {var} is more than 5 outside the range; it then waits 60 seconds before the next reading' if alarm else '') +
            '. Write an algorithm in pseudocode for this system.')
    m = 6 if alarm else 5
    key = ('1 mark loop until switched off; 1 mark input of reading; 1 mark first comparison correct; 1 mark second comparison correct; 1 mark correct actuator states'
           + ('; 1 mark alarm condition and wait' if alarm else '') + f'. Accept equivalent logic. [{m}]')
    return {'stem': stem, 'answer': 'Model answer:\n' + code(lines), 'key': key, 'marks': m, 'type': 'multi_step'}


# =============================================================================== Chapter 4 Algorithms and flowcharts
SYMBOLS = [('terminator (rounded rectangle)', 'START or STOP'), ('process (rectangle)', 'a calculation or assignment such as Total ← Total + Price'),
           ('input/output (parallelogram)', 'INPUT Mark or OUTPUT Average'), ('decision (diamond)', 'a question such as Is Mark >= 50?'),
           ('subroutine / predefined process (rectangle with double sides)', 'a call to a procedure defined elsewhere'),
           ('flow line (arrow)', 'the direction of flow from one step to the next'), ('connector (small circle)', 'joining parts of a flowchart, e.g. across pages')]

t = T(4, 'Flowchart symbols and algorithms as sequences of instructions', 'flowchart symbols', 'algorithms as sequences of instructions',
      defs=[('algorithm', 'A set of step-by-step instructions that solves a problem or completes a task, in a precise order.'),
            ('flowchart', 'A diagram that represents an algorithm using standard symbols connected by flow lines.'),
            ('decision symbol', 'A diamond-shaped flowchart symbol containing a question with two exits, such as Yes and No.'),
            ('sequence', 'Instructions carried out one after another in the order they are written.')],
      mcqs=[('Which flowchart symbol is used for "INPUT Age"?', 'Parallelogram', ['Diamond', 'Rectangle', 'Rounded rectangle'], 'Inputs and outputs use the parallelogram.'),
            ('Which flowchart symbol must have exactly two exits?', 'Decision (diamond)', ['Process (rectangle)', 'Terminator', 'Input/output'], 'A decision has a Yes/No (True/False) exit.'),
            ('Which symbol is used for "Total ← Total + 1"?', 'Process (rectangle)', ['Decision (diamond)', 'Input/output (parallelogram)', 'Terminator (rounded rectangle)'], 'Calculations and assignments are processes.'),
            ('Which symbol shows the START of a flowchart?', 'Terminator (rounded rectangle)', ['Parallelogram', 'Diamond', 'Circle connector'], 'Start and stop are terminators.')],
      exps=[('Explain why the order of instructions in an algorithm matters.', 'Instructions are carried out in sequence; doing them in a different order can give a different or wrong result, e.g. outputting a total before adding the last value.', '1 mark sequence; 1 mark example of wrong result. [2]'),
            ('Explain one advantage of representing an algorithm as a flowchart.', 'It shows the flow of control visually, so decisions and loops are easy to follow, and it is independent of any programming language.', '1 mark visual flow; 1 mark easy to follow/language independent. [2]'),
            ('Explain why a decision symbol is needed to create a loop in a flowchart.', 'The decision tests a condition; one exit leads back to an earlier step (repeat) and the other leaves the loop, so repetition stops when the condition is met.', '1 mark condition tested; 1 mark one exit loops back/other leaves. [2]')],
      ars=[('A decision box in a flowchart has two exits.', 'It asks a question with two possible answers, such as Yes or No.'),
           ('INPUT and OUTPUT are drawn in parallelograms.', 'The parallelogram is the input/output symbol.'),
           ('An algorithm must have a clear order of steps.', 'Changing the order can change the result.')],
      falses=['A process box contains a question.', 'A terminator is used for calculations.', 'Flowcharts can only be used for computer programs.'],
      intros=['{p} at {org} in {city} is drawing a flowchart for a program that calculates staff bonuses.',
              'Students at {org} in {city} are learning to show algorithms as flowcharts.',
              '{p} has been asked by {org} in {city} to plan a ticket-pricing program using a flowchart.'],
      parts=[('Draw the flowchart symbol used for a decision and state what it contains.', 'A diamond containing a question/condition with Yes and No exits.', '1 mark diamond; 1 mark question with two exits. [2]'),
             ('State which symbol would be used for "OUTPUT Bonus" and for "Bonus ← Salary * 0.05".', 'Parallelogram (input/output); rectangle (process).', '1 mark each. [2]'),
             ('Explain why the flowchart must begin and end with terminators.', 'They show clearly where the algorithm starts and where it finishes.', '1 mark start; 1 mark end. [2]'),
             ('Describe how a loop is shown on a flowchart.', 'A decision box tests a condition; a flow line from one exit returns to an earlier point; the other exit continues.', '1 mark decision; 1 mark flow line back. [2]')],
      ev=[('the use of flowcharts rather than pseudocode to plan programs at {org}', 'visual and easy for non-programmers; shows decisions and loops clearly; language independent.', 'large algorithms become very big and hard to edit; time-consuming to draw; pseudocode is closer to real code.', 'flowcharts suit small algorithms and communication with non-programmers; pseudocode suits larger ones.')])


@t.add('C3', (1, 2, 3), 'short')
def ch4_symbols(r, D):
    if D <= 2:
        s, use = r.choice(SYMBOLS)
        return MCQ(r, f'Which flowchart symbol is used for {use}?', cap(s).rstrip('.'), [cap(x[0]).rstrip('.') for x in SYMBOLS if x[0] != s], f'{s}: {use}.')
    picks = r.sample(SYMBOLS[:5], 3)
    lines = '\n'.join(f'{i + 1}. {cap(x[1])}' for i, x in enumerate(picks))
    return Q(f'Name the flowchart symbol for each step.\n{lines}', '; '.join(f'{i + 1} {x[0]}' for i, x in enumerate(picks)), '1 mark each. [3]', marks=3)


def flow_text(r, D):
    """A simple flowchart described as numbered boxes; returns (text, inputs, output)."""
    a = r.randrange(2, 9)
    lim = r.choice([20, 30, 40, 50, 60, 100])
    step = r.choice([2, 3, 4, 5])
    mult = r.choice([2, 3]) if D >= 3 else None
    boxes = ['1 START', f'2 X ← {a}', '3 C ← 0']
    if mult:
        boxes += [f'4 X ← X * {mult}']
    else:
        boxes += [f'4 X ← X + {step}']
    boxes += ['5 C ← C + 1', f'6 Is X > {lim}? No → go to 4; Yes → go to 7', '7 OUTPUT X, C', '8 STOP']
    x, c = a, 0
    seq = []
    while True:
        x = x * mult if mult else x + step
        c += 1
        seq.append(x)
        if x > lim:
            break
    return boxes, f'{x}, {c}', f'X takes the values {", ".join(map(str, seq))}; C = {c}'


@t.add('C3', (1, 2, 3, 4), 'numerical')
def ch4_flowtrace(r, D):
    boxes, out, why = flow_text(r, D)
    if D == 1:
        x, c = out.split(', ')
        return MCQ(r, 'A flowchart has these boxes:\n' + code(boxes) + '\nWhat is output?', out, [f'{x}, {int(c) + 1}', f'{x}, {int(c) - 1}', f'{int(x) - 1}, {c}', f'{int(x) * 2}, {c}'], why)
    return Q('Trace this flowchart, which is written as numbered boxes, and state the output.\n' + code(boxes), out, f'{why} [1 mark for trace values, 1 mark for output] [2]', marks=2, typ='numerical')


t = T(4, 'Writing algorithms using flowcharts and pseudocode: sequence, selection and iteration', 'writing algorithms using flowcharts and pseudocode', 'sequence, selection and iteration',
      defs=[('selection', 'A construct in which a condition is tested and different instructions are carried out depending on the result, e.g. IF ... THEN ... ELSE or CASE.'),
            ('iteration', 'A construct in which a group of instructions is repeated, e.g. FOR, WHILE or REPEAT loops.'),
            ('count-controlled loop', 'A loop that repeats a set number of times, such as FOR i ← 1 TO 10.'),
            ('condition-controlled loop', 'A loop that repeats until (or while) a condition is met, such as WHILE or REPEAT ... UNTIL.'),
            ('pseudocode', 'A structured, language-independent way of writing an algorithm using keywords similar to a programming language.')],
      mcqs=[('Which loop always runs its body at least once?', 'REPEAT ... UNTIL', ['WHILE ... ENDWHILE', 'FOR ... NEXT with 0 iterations', 'IF ... ENDIF'], 'The condition is tested at the end of a REPEAT loop.'),
            ('Which construct is best for checking a menu choice that can be 1, 2, 3 or 4?', 'CASE OF', ['FOR ... NEXT', 'REPEAT ... UNTIL', 'Sequence only'], 'CASE selects one of many options.'),
            ('Which loop is most suitable for processing exactly 30 students\' marks?', 'FOR loop', ['WHILE loop with no counter', 'REPEAT loop until mark = 0', 'IF statement'], 'The number of repetitions is known in advance.')],
      exps=[('Explain the difference between a WHILE loop and a REPEAT ... UNTIL loop.', 'WHILE tests its condition before each iteration, so it may run zero times; REPEAT tests at the end, so it always runs at least once.', '1 mark WHILE pre-condition/may not run; 1 mark REPEAT post-condition/at least once. [2]'),
            ('Explain why a FOR loop is not suitable for validating an input until it is correct.', 'The number of attempts is not known in advance; a condition-controlled loop is needed to repeat until valid data is entered.', '1 mark unknown repetitions; 1 mark condition-controlled loop needed. [2]'),
            ('Explain why a running total must be set to zero before a loop.', 'Otherwise it may contain an old or undefined value, which will be added to and give a wrong total.', '1 mark initialise; 1 mark wrong result otherwise. [2]')],
      ars=[('A REPEAT ... UNTIL loop always runs at least once.', 'Its condition is tested at the end of each iteration.'),
           ('A FOR loop is a count-controlled loop.', 'It repeats a fixed number of times set by its start and end values.'),
           ('CASE is a form of selection.', 'It chooses which statements to execute depending on a value.')],
      falses=['A WHILE loop always runs at least once.', 'Selection repeats instructions a fixed number of times.', 'A FOR loop stops when a condition becomes true part-way through.'],
      intros=['{p} is writing a program for {org} in {city} that processes the marks of a class of students.',
              '{org} in {city} needs a program that calculates the cost of tickets for groups of visitors.',
              '{p} is designing an algorithm for {org} in {city} that reads daily temperatures and reports statistics.'],
      parts=[('State the purpose of selection in an algorithm, giving an example.', 'To choose between different actions based on a condition, e.g. IF Mark >= 50 THEN OUTPUT "Pass".', '1 mark purpose; 1 mark example. [2]'),
             ('Explain whether a count-controlled or a condition-controlled loop should be used if the number of items is entered first.', 'Count-controlled (FOR), because the number of repetitions is known before the loop starts.', '1 mark choice; 1 mark reason. [2]'),
             ('Write pseudocode to input 10 numbers and output their total and average.', 'Total ← 0; FOR i ← 1 TO 10; INPUT Num; Total ← Total + Num; NEXT i; OUTPUT Total, Total / 10', '1 mark initialise; 1 mark loop; 1 mark input and add; 1 mark outputs. [4]'),
             ('Write pseudocode that keeps asking for a value until one between 1 and 100 is entered.', 'REPEAT; INPUT Value; UNTIL Value >= 1 AND Value <= 100', '1 mark loop; 1 mark input; 1 mark correct condition. [3]')],
      ev=[('the choice of loop types in the algorithm for {org}', 'FOR loops are simple when counts are known; condition-controlled loops handle unknown amounts of data and validation.', 'wrong choice can cause loops that run too many or too few times or never end; REPEAT always runs once even when no data exists.', 'the loop should match whether the number of iterations is known in advance.')])


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ch4_pctrace(r, D):
    gen = r.choice(PC_GENS)
    lines, out, why = gen(r, D)
    stem = 'Study this pseudocode algorithm.\n' + code(lines) + '\nState the output when the algorithm is run' + (' and explain how you obtained it.' if D >= 4 else '.')
    m = 2 if D <= 3 else 3
    return Q(stem, out, f'{why} — output {out} [{"2 marks correct output; 1 mark partial trace" if m == 2 else "2 marks correct output; 1 mark explanation"}] [{m}]', marks=m, typ='numerical')


TASKS = [
    ('input 20 exam marks and output how many are 50 or more', ['Count ← 0', 'FOR i ← 1 TO 20', f'{IND}INPUT Mark', f'{IND}IF Mark >= 50 THEN', f'{IND}{IND}Count ← Count + 1', f'{IND}ENDIF', 'NEXT i', 'OUTPUT Count']),
    ('input the prices of items until a price of 0 is entered, then output the total cost', ['Total ← 0', 'INPUT Price', 'WHILE Price <> 0', f'{IND}Total ← Total + Price', f'{IND}INPUT Price', 'ENDWHILE', 'OUTPUT Total']),
    ('input 15 temperatures and output the highest', ['INPUT Temp', 'Highest ← Temp', 'FOR i ← 2 TO 15', f'{IND}INPUT Temp', f'{IND}IF Temp > Highest THEN', f'{IND}{IND}Highest ← Temp', f'{IND}ENDIF', 'NEXT i', 'OUTPUT Highest']),
    ('input a number of tickets (1 to 10, re-entering until valid) and output the cost at $12 each, with 10% off for 5 or more tickets',
     ['REPEAT', f'{IND}INPUT Tickets', 'UNTIL Tickets >= 1 AND Tickets <= 10', 'Cost ← Tickets * 12', 'IF Tickets >= 5 THEN', f'{IND}Cost ← Cost * 0.9', 'ENDIF', 'OUTPUT Cost']),
    ('input the ages of 30 people and output how many are children (under 13), teenagers (13–19) and adults (20 or over)',
     ['Child ← 0', 'Teen ← 0', 'Adult ← 0', 'FOR i ← 1 TO 30', f'{IND}INPUT Age', f'{IND}IF Age < 13 THEN', f'{IND}{IND}Child ← Child + 1', f'{IND}ELSE', f'{IND}{IND}IF Age <= 19 THEN', f'{IND}{IND}{IND}Teen ← Teen + 1',
      f'{IND}{IND}ELSE', f'{IND}{IND}{IND}Adult ← Adult + 1', f'{IND}{IND}ENDIF', f'{IND}ENDIF', 'NEXT i', 'OUTPUT Child, Teen, Adult']),
    ('input a password and allow up to three attempts to enter "Secret1", outputting "Access granted" or "Locked"',
     ['Attempts ← 0', 'REPEAT', f'{IND}INPUT Password', f'{IND}Attempts ← Attempts + 1', 'UNTIL Password = "Secret1" OR Attempts = 3', 'IF Password = "Secret1" THEN', f'{IND}OUTPUT "Access granted"', 'ELSE', f'{IND}OUTPUT "Locked"', 'ENDIF']),
]


@t.add('C4', (2, 3, 4, 5), 'long')
def ch4_write(r, D):
    task, model = r.choice(TASKS)
    d = ctx(r)
    m = nearest(CTX.get('want_marks'), (4, 5, 6), {2: 4, 3: 5, 4: 6, 5: 6}[D])
    lead = r.choice([f'{d["p"]} works for {d["org"]} in {d["city"]}.', f'{d["org"]} in {d["city"]} needs a short program.', f'A member of staff at {d["org"]} ({d["city"]}) has asked {d["p"]} for an algorithm.'])
    tool = r.choice(['pseudocode', 'pseudocode', 'a flowchart'])
    stem = f'{lead} Write an algorithm, using {tool}, to {task}.'
    key = f'Mark points: variables initialised; correct loop structure; input inside loop; correct condition(s)/selection; correct update of totals/counters; correct output after the loop. 1 mark each, max {m}. [{m}]'
    return {'stem': stem, 'answer': 'Model answer:\n' + code(model), 'key': key, 'marks': m, 'type': 'long'}


t = T(4, 'Tracing and correcting algorithms; comparing flowcharts and pseudocode', 'tracing and correcting algorithms', 'comparing flowcharts and pseudocode',
      defs=[('trace table', 'A table used to record the values of variables, and any outputs, as each step of an algorithm is followed by hand.'),
            ('dry run', 'Working through an algorithm manually, step by step, to check what it does and to find errors.'),
            ('logic error', 'An error in the design of an algorithm that makes it produce the wrong result, although it still runs.'),
            ('syntax error', 'An error in the grammar or rules of the language, such as a misspelt keyword, that stops the program being translated.')],
      mcqs=[('An algorithm to find the average of 10 numbers divides the total by 9. What type of error is this?', 'Logic error', ['Syntax error', 'Run-time error caused by hardware', 'Validation error'], 'The program runs but gives the wrong result.'),
            ('What is the main purpose of a trace table?', 'To record the values of variables at each step so the algorithm can be checked', ['To store the final program', 'To translate pseudocode into machine code', 'To draw the flowchart symbols'], 'Trace tables support dry runs.')],
      exps=[('Explain why a dry run with a trace table can find logic errors.', 'Following each step and recording variable values shows exactly where the values differ from what is expected, so the faulty step can be identified.', '1 mark record values step by step; 1 mark compare with expected/locate error. [2]'),
            ('Explain one advantage of pseudocode over a flowchart for a long algorithm.', 'Pseudocode is quicker to write and edit and is closer to program code, so it is easier to convert into a program; long flowcharts become large and hard to follow.', '1 mark advantage; 1 mark explanation. [2]'),
            ('Explain why test data should include values that are expected to be rejected.', 'To check that the algorithm handles invalid input correctly, e.g. validation rejects it, rather than crashing or giving wrong results.', '1 mark check rejection/validation; 1 mark avoids wrong results/crashes. [2]')],
      ars=[('A logic error is not detected by the translator.', 'The code follows the syntax rules of the language.'),
           ('Trace tables are used during a dry run.', 'They record the value of each variable after each step.')],
      falses=['A syntax error produces a wrong answer but the program still runs.', 'A dry run is carried out by the computer automatically.'],
      intros=['{p} at {org} in {city} has written an algorithm but it gives incorrect results.',
              'A trainee programmer at {org} in {city} is learning to test algorithms by hand.'],
      parts=[('Explain what is meant by a dry run.', 'Working through the algorithm by hand, step by step, recording values, to check it works.', '1 mark manual/step by step; 1 mark purpose. [2]'),
             ('Describe how a trace table is set up.', 'One column for each variable (and for outputs/conditions); a new row each time a value changes.', '1 mark columns; 1 mark rows/values recorded. [2]'),
             ('Explain the difference between a syntax error and a logic error.', 'Syntax error breaks language rules so the code will not translate; logic error runs but gives wrong results.', '1 mark each. [2]'),
             ('Explain why the algorithm should be tested with more than one set of data.', 'Different paths through the algorithm (e.g. each branch of an IF, boundary values) need checking.', '1 mark different paths; 1 mark boundary/invalid values. [2]')],
      ev=[('the use of dry runs and trace tables by {org} to test algorithms before coding', 'finds logic errors early and cheaply; improves understanding; no computer needed.', 'slow for long algorithms; human errors in tracing; cannot test all inputs; real testing on the computer still needed.', 'dry runs are valuable for small, critical sections but should be combined with computer testing.')])


def bug_gen(r, D):
    """An algorithm with one deliberate error; returns (lines, line_no, correct_line, explanation)."""
    kind = r.randrange(5)
    n = r.choice([10, 20, 25, 30])
    if kind == 0:
        lines = ['Total ← 0', f'FOR i ← 1 TO {n}', f'{IND}INPUT Mark', f'{IND}Total ← Total + Mark', 'NEXT i', f'Average ← Total / {n - 1}', 'OUTPUT Average']
        return lines, 6, f'Average ← Total / {n}', f'the total is divided by {n - 1} instead of {n}, so the average is wrong'
    if kind == 1:
        lines = [f'FOR i ← 1 TO {n}', f'{IND}Total ← 0', f'{IND}INPUT Price', f'{IND}Total ← Total + Price', 'NEXT i', 'OUTPUT Total']
        return lines, 2, '(move) Total ← 0 to before the FOR loop', 'Total is reset to 0 on every pass, so only the last price is output'
    if kind == 2:
        lines = ['Count ← 0', f'FOR i ← 1 TO {n}', f'{IND}INPUT Age', f'{IND}IF Age > 18 THEN', f'{IND}{IND}Count ← Count + 1', f'{IND}ENDIF', 'NEXT i', 'OUTPUT "Number aged 18 or over: ", Count']
        return lines, 4, f'{IND}IF Age >= 18 THEN'.strip(), 'people aged exactly 18 are not counted because > is used instead of >='
    if kind == 3:
        lines = ['INPUT Temp', 'Highest ← Temp', f'FOR i ← 2 TO {n}', f'{IND}INPUT Temp', f'{IND}IF Temp < Highest THEN', f'{IND}{IND}Highest ← Temp', f'{IND}ENDIF', 'NEXT i', 'OUTPUT Highest']
        return lines, 5, 'IF Temp > Highest THEN', 'the comparison uses < so the algorithm finds the lowest value, not the highest'
    lines = ['Count ← 0', 'INPUT Value', 'WHILE Value <> -1', f'{IND}Count ← Count + 1', 'ENDWHILE', 'OUTPUT Count']
    return lines, 5, f'insert INPUT Value before ENDWHILE', 'Value is never input again inside the loop, so the loop never ends (infinite loop)'


@t.add('C2', (2, 3, 4), 'explain')
def ch4_bug(r, D):
    lines, ln, fix, why = bug_gen(r, D)
    d = ctx(r)
    numbered = code([f'{j + 1:>2}  {x}' for j, x in enumerate(lines)])
    stem = f'{d["p"]} at {d["org"]} wrote this algorithm, but it contains an error.\n{numbered}\nIdentify the line containing the error, explain why it is wrong and give the correction.'
    return {'stem': stem, 'answer': f'Line {ln}: {why}. Correction: {fix}.', 'key': f'1 mark line {ln}; 1 mark explanation ({why}); 1 mark correction ({fix}). [3]', 'marks': 3, 'type': 'explain'}


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ch4_tracetable(r, D):
    n = 4 if D <= 3 else 5
    vals = [r.randrange(5, 60) for _ in range(n)]
    lim = r.randrange(20, 45)
    lines = ['Count ← 0', 'Total ← 0', f'FOR i ← 1 TO {n}', f'{IND}INPUT Num', f'{IND}IF Num > {lim} THEN', f'{IND}{IND}Count ← Count + 1', f'{IND}{IND}Total ← Total + Num', f'{IND}ENDIF', 'NEXT i', 'OUTPUT Count, Total']
    rows = []
    c = tt = 0
    for i, v in enumerate(vals, 1):
        if v > lim:
            c += 1
            tt += v
        rows.append(f'i={i}, Num={v}, Count={c}, Total={tt}')
    stem = 'Complete a trace table (columns i, Num, Count, Total, OUTPUT) for this algorithm using the input data ' + ', '.join(map(str, vals)) + '.\n' + code(lines)
    m = n + 1
    if D >= 5:
        stem += ' Then state the purpose of the algorithm.'
        m += 1
    return Q(stem, '; '.join(rows) + f'; OUTPUT {c}, {tt}' + (f'. It counts and totals the numbers greater than {lim}.' if D >= 5 else ''),
             '1 mark per correct row: ' + '; '.join(rows) + f'; 1 mark output {c}, {tt}' + ('; 1 mark purpose: counts and totals inputs above ' + str(lim) if D >= 5 else '') + f'. [{m}]', marks=m, typ='numerical')


# =============================================================================== Chapter 5 eSafety and health
DPP = [
    ('Personal data must be processed fairly and lawfully.', 'A website collects visitors\' home addresses without telling them.'),
    ('Personal data must only be used for the specified purpose(s) it was collected for.', 'A dentist sells patients\' phone numbers to a mobile-phone company for marketing.'),
    ('Personal data must be adequate, relevant and not excessive.', 'A gym asks new members for their bank PIN and their parents\' salaries.'),
    ('Personal data must be accurate and kept up to date.', 'A school keeps sending reports to an address a family left two years ago, despite being told of the move.'),
    ('Personal data must not be kept longer than necessary.', 'A shop keeps the card details of one-off customers for twenty years.'),
    ('Personal data must be processed in line with the data subject\'s rights.', 'A company refuses to tell a customer what data it holds about her when she asks.'),
    ('Personal data must be kept secure.', 'An employee leaves an unencrypted laptop containing customer records on a train.'),
    ('Personal data must not be transferred to countries without adequate protection.', 'A company sends its customer database to a country with no data protection laws.'),
]

t = T(5, 'Personal data and protecting personal data online; data protection legislation', 'personal data', 'data protection legislation',
      defs=[('personal data', 'Data that relates to a living person who can be identified from it, such as name, address, date of birth or medical records.'),
            ('sensitive personal data', 'Personal data that could be used to discriminate against a person, such as ethnicity, religion, health, political opinions or sexual orientation.'),
            ('data subject', 'The living individual whom personal data is about.'),
            ('data controller', 'The person or organisation that decides why and how personal data is processed and is responsible for complying with data protection law.')],
      mcqs=[('Which of these is an example of sensitive personal data?', 'A person\'s medical history', ['A person\'s favourite colour', 'The name of a company', 'The price of a product'], 'Health data could be used to discriminate and needs extra protection.'),
            ('A customer asks {org} for a copy of all the data it holds about her. What right is she using?', 'The right of access to her personal data', ['The right to free products', 'The right to see other customers\' data', 'The right to change the company\'s prices'], 'Data subjects can ask to see the data held about them.'),
            ('Which is the best way to protect personal data stored on a laptop?', 'Encrypt the hard disk and use a strong password', ['Store the data in a folder called "Private"', 'Turn the screen brightness down', 'Use a larger hard disk'], 'Encryption makes stolen data unreadable.')],
      exps=[('Explain why sensitive personal data needs more protection than other personal data.', 'It could be used to discriminate against or harm the person (e.g. health or religion), so misuse has serious consequences.', '1 mark could be used to discriminate/harm; 1 mark example or consequence. [2]'),
            ('Explain two ways an organisation can keep personal data secure.', 'Encrypt data so it is unreadable if stolen; use access rights/strong passwords so only authorised staff can see it; firewalls; regular backups; staff training.', '2 × (1 mark method, 1 mark explanation). [4]'),
            ('Explain why data protection legislation is needed.', 'Organisations hold large amounts of personal data; without rules it could be misused, sold, kept inaccurately or not secured, harming individuals\' privacy.', '1 mark large amounts held; 1 mark risk of misuse; 1 mark protects privacy/rights. [3]')],
      ars=[('Organisations should not keep personal data longer than necessary.', 'Old data may be inaccurate and increases the risk if there is a data breach.'),
           ('Encrypting a laptop protects personal data if it is stolen.', 'Encrypted data cannot be understood without the key.'),
           ('A person\'s health records are sensitive personal data.', 'They could be used to discriminate against the person.')],
      falses=['Personal data can be sold to any company once collected.', 'Data protection laws only apply to paper records.', 'A data subject cannot ask to see their own data.'],
      intros=['{org}, {aot} in {city}, stores names, addresses, dates of birth and payment details of its customers.',
              '{p} has just started working in the records office of {org} in {city}, which holds staff and customer data.',
              '{org} in {city} is launching an app that collects users\' locations and contact details.'],
      parts=[('Give two examples of personal data the organisation holds.', 'Name, address, date of birth, phone number, bank details, medical information.', '1 mark each, max 2. [2]'),
             ('Describe three principles of data protection legislation that the organisation must follow.', 'Processed fairly and lawfully; used only for stated purposes; adequate, relevant, not excessive; accurate and up to date; not kept longer than necessary; processed in line with subjects\' rights; kept secure; not transferred abroad without adequate protection.', '1 mark each, max 3. [3]'),
             ('Explain two methods the organisation should use to keep this data secure.', 'Encryption; strong passwords and access levels; firewalls; anti-malware; physical security; staff training.', '2 × (1 mark method, 1 mark explanation). [4]'),
             ('Explain why the organisation should not ask for more data than it needs.', 'Data must be adequate, relevant and not excessive; extra data increases the harm if there is a breach and costs more to store and protect.', '1 mark principle; 1 mark consequence. [2]'),
             ('State two rights that customers have over their personal data.', 'Right to see the data; to have errors corrected; to object to direct marketing; to have data deleted in some cases; to complain to the regulator.', '1 mark each, max 2. [2]')],
      ev=[('whether data protection legislation gives enough protection to the customers of {org}', 'sets clear principles; gives individuals rights; fines encourage compliance; requires security.', 'laws differ between countries and data crosses borders; breaches still happen; enforcement is slow; people often accept terms without reading them.', 'legislation is necessary but must be backed by good security, enforcement and user awareness.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch5_principle(r, D):
    if D <= 2:
        p, s = r.choice(DPP)
        return MCQ(r, f'{s} Which data protection principle is being broken?', p.rstrip('.'), [x[0].rstrip('.') for x in DPP if x[0] != p], p)
    picks = r.sample(DPP, 2 if D == 3 else 3)
    lines = '\n'.join(f'{i + 1}. {x[1]}' for i, x in enumerate(picks))
    m = 2 * len(picks)
    return Q(f'For each situation, identify the data protection principle that has been broken and suggest what the organisation should have done.\n{lines}',
             '; '.join(f'{i + 1}: {x[0].rstrip(".")}' for i, x in enumerate(picks)), '; '.join(f'{i + 1}: {x[0].rstrip(".")} [1] + suitable corrective action [1]' for i, x in enumerate(picks)) + f'. [{m}]', marks=m)


ESAFE = [
    ('A stranger in an online game asks a 13-year-old player for their home address.', 'never give personal details to people met online; block and report the user'),
    ('A teenager posts a photo of their new school uniform with the school badge showing.', 'avoid posting images that reveal location or school; check privacy settings'),
    ('An email claims a parcel is waiting and asks the user to click a link and pay a small fee.', 'do not click links in unexpected emails; check the sender; go to the official website directly'),
    ('A user\'s social media profile is public and shows their full date of birth.', 'set the profile to private and remove personal details such as date of birth'),
    ('A player is offered free in-game currency if they share their account password.', 'never share passwords; enable two-factor authentication'),
    ('A student wants to meet someone they have only chatted to online.', 'do not meet online contacts alone; tell a trusted adult; meet in a public place with an adult if at all'),
    ('A user receives an email attachment called invoice.exe from an unknown sender.', 'do not open attachments from unknown senders; scan with anti-virus; delete'),
    ('A user is being sent abusive messages on a social network.', 'do not reply; keep evidence; block and report the user; tell a trusted adult'),
]

t = T(5, 'eSafety: using the internet, email, social media and online gaming safely', 'esafety', 'social media and online gaming',
      defs=[('eSafety', 'Using the internet and digital devices in a way that protects your personal safety, privacy and wellbeing.'),
            ('cyberbullying', 'Using digital technology, such as social media or messaging, to threaten, embarrass or harass another person.'),
            ('grooming', 'When a person builds an online relationship with a young person in order to exploit or abuse them.'),
            ('privacy settings', 'Settings on social media or apps that control who can see a user\'s posts and personal information.')],
      mcqs=[('Which is the safest choice for a username in an online game?', 'A made-up name that does not reveal identity, age or location', ['First name and year of birth', 'Full name and school', 'Home town and age'], 'Usernames should not reveal personal information.'),
            ('Why should GPS location tagging be switched off when posting photos publicly?', 'It can reveal where the user lives or is at that moment', ['It makes photos lower quality', 'It uses too much storage', 'It stops the photo being posted'], 'Location data can help strangers find the user.'),
            ('What should a user do first if they receive threatening messages online?', 'Keep the evidence, block the sender and report it', ['Reply angrily to stop them', 'Delete their own account immediately without telling anyone', 'Forward the messages to all their friends'], 'Evidence, block, report and tell a trusted adult.')],
      exps=[('Explain why users should not reveal personal information in online games.', 'Other players may not be who they claim; information such as address, school or age could be used for grooming, stalking or identity theft.', '1 mark identity unknown; 1 mark risk (grooming/identity theft). [2]'),
            ('Explain two ways to stay safe when using email.', 'Do not open attachments or links from unknown senders (malware/phishing); never reply to spam or give personal details; check the sender\'s address.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why privacy settings on social media are important.', 'They restrict who can see posts and personal details, so strangers cannot use the information to locate, groom or impersonate the user.', '1 mark restricts audience; 1 mark consequence. [2]')],
      ars=[('Users should not share passwords with other online gamers.', 'Someone with the password can take over the account.'),
           ('Location tagging on public posts can be dangerous.', 'It can show strangers where the user is.'),
           ('Users should not open attachments from unknown senders.', 'Attachments can contain malware.')],
      falses=['It is safe to meet online friends alone because they always tell the truth.', 'Public profiles protect a user\'s privacy.', 'Antivirus software makes it safe to open any attachment.'],
      intros=['{org} in {city} is running an eSafety workshop for students aged 12 to 16.',
              '{p} has just joined a social network and an online gaming community, and has asked {org} in {city} for advice.',
              'Parents at {org} in {city} are worried about their children using the internet at home.'],
      parts=[('Describe three ways a young person can stay safe on social media.', 'Use privacy settings; do not post personal details or location; only accept friends they know; report/block abusive users; think before posting.', '1 mark each, max 3. [3]'),
             ('Explain the risks of meeting someone in person who was met online.', 'They may not be who they say (grooming); risk of abuse or harm; should tell an adult and meet in a public place with an adult.', '1 mark risk; 1 mark explanation/precaution. [2]'),
             ('Describe two ways of staying safe when playing online games.', 'Use a nickname; do not share personal information or passwords; use in-game reporting/blocking; be wary of in-game purchase scams; limit chat to friends.', '1 mark each, max 2. [2]'),
             ('Explain what should be done if a person is being cyberbullied.', 'Do not respond; save evidence; block the bully; report to the platform; tell a trusted adult or the school.', '1 mark per point, max 3. [3]'),
             ('Explain why it is unsafe to click on links in unexpected emails.', 'They may lead to phishing websites that steal login details, or download malware.', '1 mark phishing; 1 mark malware. [2]')],
      ev=[('whether schools such as {org} should teach eSafety rather than simply blocking websites', 'education gives skills for use at home and on phones; blocking cannot cover everything; students learn to recognise risks.', 'blocking provides immediate protection; some students ignore advice; teaching takes time from other subjects.', 'a combination of education and sensible filtering is most effective.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch5_esafe(r, D):
    s, a = r.choice(ESAFE)
    if D <= 2:
        return Q(f'{s} Describe what the user should do to stay safe.', cap(a), f'1 mark for each appropriate action: {a}. [2]', marks=2)
    s2, a2 = r.choice([x for x in ESAFE if x[0] != s])
    return Q(f'Give advice on staying safe in each situation and explain the risk involved: (1) {s} (2) {s2}', f'(1) {cap(a)} (2) {cap(a2)}',
             f'(1) advice: {a} [1], risk explained [1] (2) advice: {a2} [1], risk explained [1]. [4]', marks=4)


HEALTH = [('repetitive strain injury (RSI)', 'typing or using a mouse for long periods with the same repeated movements', 'take regular breaks; use an ergonomic keyboard/mouse and wrist rests; correct posture'),
          ('eye strain', 'looking at a screen for long periods, glare or flickering screens', 'take regular breaks and look into the distance; use anti-glare screens; adjust brightness; have eye tests'),
          ('back and neck problems', 'sitting in a poor position or at a badly arranged workstation for long periods', 'use an adjustable chair with back support; position the screen at eye level; take breaks to move around'),
          ('headaches', 'glare on the screen, poor lighting or long periods of screen use', 'use anti-glare filters; adjust lighting; take regular breaks'),
          ('deep vein thrombosis / poor circulation', 'sitting still for very long periods without moving', 'get up and walk around regularly; use a footrest')]

t = T(5, 'Health issues from using IT: RSI, eyestrain, back problems and their prevention', 'health issues from using it', 'rsi, eyestrain, back problems',
      defs=[('repetitive strain injury (RSI)', 'Pain and damage to muscles, tendons and nerves in the hands, wrists and arms caused by repeating the same movements, such as typing, for long periods.'),
            ('eye strain', 'Tired, sore or dry eyes and blurred vision caused by looking at a screen for long periods without breaks.'),
            ('ergonomics', 'Designing equipment and workstations to fit the user, reducing strain and health problems.')],
      mcqs=[('Which is the best way to reduce the risk of RSI?', 'Use a wrist rest and take regular breaks from typing', ['Use an anti-glare screen', 'Increase the screen brightness', 'Sit closer to the screen'], 'RSI is caused by repeated movements; rests and breaks help.'),
            ('Which health problem is reduced by positioning the top of the screen at eye level?', 'Neck and back problems', ['RSI in the fingers', 'Hearing loss', 'Electric shock'], 'A correctly positioned screen avoids bending the neck.')],
      exps=[('Explain how an employer can reduce eye strain among staff who use computers all day.', 'Provide anti-glare screens and good lighting; allow regular breaks from screen work; pay for eye tests.', '1 mark per method with explanation, max 2 points. [3]'),
            ('Explain why an adjustable chair helps to prevent back problems.', 'It can be set so the user sits upright with the back supported and feet flat, reducing strain on the spine.', '1 mark adjusted to user; 1 mark correct posture/support. [2]')],
      ars=[('Regular breaks reduce the risk of RSI.', 'They stop the same movements being repeated for long periods.'),
           ('Anti-glare screens can reduce eye strain.', 'Reflections on the screen make the eyes work harder.')],
      falses=['RSI is caused by screen glare.', 'Eye strain is prevented by using a wrist rest.'],
      intros=['{org} in {city} has received complaints from office staff about aches and pains.',
              '{p} works long hours entering data at {org} in {city}.'],
      parts=[('Identify two health problems that can be caused by using computers for long periods.', 'RSI; eye strain; back/neck problems; headaches; poor circulation.', '1 mark each, max 2. [2]'),
             ('For one health problem, describe its cause and how it can be prevented.', 'e.g. RSI caused by repetitive typing; prevented by breaks, wrist rests, ergonomic keyboard.', '1 mark cause; 1 mark prevention. [2]'),
             ('Explain how the workstation should be arranged.', 'Screen at eye level and arm\'s length; adjustable chair; keyboard and mouse within reach; feet flat; good lighting without glare.', '1 mark per point, max 3. [3]')],
      ev=[('whether {org} should spend money on ergonomic equipment for its staff', 'fewer health problems and absences; higher productivity; legal duty of care.', 'cost of equipment; staff may not use it correctly; breaks and training may be as effective.', 'ergonomic equipment is usually worth it when combined with training and regular breaks.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch5_health(r, D):
    h, cause, prev = r.choice(HEALTH)
    if D <= 2:
        return MCQ(r, f'Which health problem is most likely to be caused by {cause}?', h.capitalize(), [x[0].capitalize() for x in HEALTH if x[0] != h], f'{h}: caused by {cause}; prevent by: {prev}.')
    d = ctx(r)
    return Q(f'{d["p"]} works at {d["org"]} in {d["city"]} and has started to suffer from {h}. Describe a likely cause and two ways it could be prevented.', f'Cause: {cause}. Prevention: {prev}.',
             f'1 mark cause ({cause}); 2 marks prevention ({prev}). [3]', marks=3)


# =============================================================================== Chapter 6 The digital divide and audience
t = T(6, 'Identifying the target audience and their needs when designing ICT solutions', 'identifying the target audience', 'target audience',
      defs=[('target audience', 'The group of people that an ICT solution, such as a website or presentation, is designed for.'),
            ('audience appreciation', 'Planning and designing a solution by considering the age, knowledge, interests, needs and abilities of the people who will use it.'),
            ('accessibility', 'How easily a product can be used by people with different abilities, including people with disabilities.')],
      mcqs=[('A website is being designed for children aged 5 to 7. Which feature is most appropriate?', 'Large, simple images and spoken instructions', ['Long paragraphs of detailed text', 'Small fonts to fit more on the page', 'Complex drop-down menus'], 'Young children have limited reading skills.'),
            ('Which audience characteristic is most important when choosing the vocabulary used in a presentation?', 'The audience\'s age and level of knowledge', ['The number of slides', 'The speaker\'s favourite colour', 'The file size of the presentation'], 'Language must match what the audience understands.')],
      exps=[('Explain why it is important to identify the target audience before designing a website.', 'The content, language, layout, colours and level of detail must suit the users\' age, knowledge and needs; otherwise they may not understand it or may lose interest.', '1 mark design must match audience; 1 mark consequence of not doing so. [2]'),
            ('Explain two ways a website could be designed for elderly users.', 'Larger font sizes and high contrast for reduced eyesight; simple navigation with clear buttons; avoid jargon; option for audio.', '2 × (1 mark feature, 1 mark reason). [4]'),
            ('Describe two methods that could be used to find out about the needs of a target audience.', 'Questionnaires/surveys; interviews; focus groups; observing how users use existing systems.', '1 mark each with brief description, max 2. [2]')],
      ars=[('A presentation for experts can use technical vocabulary.', 'The audience already understands the subject.'),
           ('Websites for young children should use simple language.', 'Their reading ability is limited.')],
      falses=['The same design suits every audience.', 'Audience needs should only be considered after the solution is finished.'],
      intros=['{org} in {city} is designing a website to sell holidays to people over 65.',
              '{p} is creating a multimedia presentation for {org} in {city} to show to primary school children.',
              '{org} in {city} wants an app that helps new employees learn company procedures.'],
      parts=[('Describe three characteristics of the target audience that should be considered.', 'Age; level of IT and subject knowledge; interests; language; disabilities/accessibility needs; expectations.', '1 mark each, max 3. [3]'),
             ('Explain two design features suitable for this audience.', 'Font size and style; colour scheme/contrast; amount of text vs images; navigation; use of audio/video; vocabulary.', '2 × (1 mark feature, 1 mark justification). [4]'),
             ('Describe how the designer could find out what the audience needs.', 'Questionnaires; interviews; focus groups; testing prototypes with users.', '1 mark method; 1 mark description. [2]'),
             ('Explain why the solution should be tested with members of the target audience.', 'They can show whether it meets their needs and is easy to use, so problems can be fixed before release.', '1 mark feedback on suitability; 1 mark changes made before release. [2]')],
      ev=[('the importance of audience appreciation in the success of the solution for {org}', 'a solution matched to users is easier to use, more engaging and more likely to be adopted.', 'research takes time and money; audiences are varied so one design cannot suit everyone; good content also matters.', 'audience appreciation is essential, though designers must balance it against budget and the needs of different groups.')])

AUD = [('children aged 6 to 8', 'large text, bright colours, many images, simple words, audio narration, very simple navigation'),
       ('elderly users with limited IT experience', 'large font, high contrast, simple layout, clear labels, no jargon, help instructions'),
       ('medical specialists', 'technical vocabulary, detailed data and charts, concise professional layout'),
       ('teenagers', 'informal language, modern design, video and interactive content, mobile-friendly'),
       ('people with visual impairments', 'screen-reader compatible text, alt text for images, high contrast, resizable text, audio options'),
       ('international tourists', 'multiple language options, icons and maps, simple vocabulary')]


@t.add('C3', (1, 2, 3, 4), 'short')
def ch6_aud(r, D):
    a, feat = r.choice(AUD)
    d = ctx(r)
    if D <= 2:
        return Q(f'{d["org"]} in {d["city"]} is creating a website for {a}. Describe two design features that would suit this audience.', cap(feat),
                 f'1 mark each feature with brief justification, e.g. {feat}. [2]', marks=2)
    a2, f2 = r.choice([x for x in AUD if x[0] != a])
    return Q(f'{d["org"]} produces information for two audiences: {a} and {a2}. Compare how the design of the two versions should differ.', f'For {a}: {feat}. For {a2}: {f2}.',
             f'Up to 2 marks for features suited to {a}; up to 2 marks for features suited to {a2}; comparison needed for full marks. [4]', marks=4)


t = T(6, 'The digital divide: causes and effects on individuals, organisations and societies', 'the digital divide', 'causes and effects',
      defs=[('digital divide', 'The gap between people who have access to, and can use, modern information and communication technology and those who do not.'),
            ('digital literacy', 'The skills needed to find, evaluate, use and create information using digital technology.'),
            ('infrastructure (in ICT)', 'The physical systems, such as broadband cables, mobile masts and electricity supply, needed for people to access ICT.')],
      mcqs=[('Which is a cause of the digital divide between urban and rural areas?', 'Poor broadband and mobile coverage in rural areas', ['More people live in rural areas', 'Rural people are not interested in technology', 'Urban areas have more farms'], 'Infrastructure is often less developed outside cities.'),
            ('Which group is most likely to be affected by the digital divide because of age?', 'Elderly people who did not grow up with computers', ['Teenagers', 'University students', 'Software developers'], 'Lack of skills and confidence among older people.')],
      exps=[('Explain two causes of the digital divide.', 'Cost: low-income households cannot afford devices or connection; infrastructure: rural or developing areas lack broadband/electricity; skills: lack of digital literacy, especially among older people; language or disability barriers.', '2 × (1 mark cause, 1 mark explanation). [4]'),
            ('Explain how the digital divide can affect a person\'s job prospects.', 'Many jobs are advertised and applied for online and need IT skills; people without access or skills miss opportunities and are less employable.', '1 mark online applications/IT skills needed; 1 mark disadvantage. [2]'),
            ('Explain how the digital divide affects businesses in areas with poor internet access.', 'They cannot use e-commerce, cloud services or online marketing effectively, so they are less competitive and may relocate, reducing local jobs.', '1 mark limited online services; 1 mark competitiveness/consequence. [2]')],
      ars=[('People without internet access may pay more for some goods and services.', 'Online prices and deals are often cheaper than in shops.'),
           ('The digital divide can exist within a single country.', 'Access differs between groups such as urban and rural or rich and poor.')],
      falses=['The digital divide only exists between countries.', 'The digital divide has no effect on education.'],
      intros=['A government report on the region around {city} says that many households still have no internet access.',
              '{org} in {city} wants to understand why some of its customers do not use its online services.',
              '{p} is writing an article for {org} about the digital divide in and around {city}.'],
      parts=[('Describe two causes of the digital divide in this situation.', 'Cost of devices and connection; lack of infrastructure in rural areas; lack of skills/digital literacy; age; disability; language.', '1 mark each, max 2. [2]'),
             ('Explain two effects of the digital divide on individuals.', 'Fewer job opportunities; less access to online education and services; social isolation; paying more without online deals.', '2 × (1 mark effect, 1 mark explanation). [4]'),
             ('Explain one effect of the digital divide on the economy of the area.', 'Businesses are less competitive and investment goes elsewhere, so there are fewer jobs and lower growth.', '1 mark effect; 1 mark explanation. [2]'),
             ('Explain why the digital divide matters for education.', 'Students without devices or internet cannot do online homework or research, so they fall behind.', '1 mark lack of access; 1 mark consequence. [2]')],
      ev=[('whether the digital divide is mainly caused by cost rather than by lack of skills', 'devices and data plans are unaffordable for low-income households; infrastructure costs money.', 'many people with access lack skills or confidence; age, disability and language also matter; some choose not to use ICT.', 'cost and skills both matter; the main cause varies between groups and places.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch6_divide(r, D):
    groups = r.sample([('urban households', 85, 97), ('rural households', 40, 75), ('households aged 65+', 30, 60), ('households aged 16-34', 88, 99),
                       ('low-income households', 35, 65), ('high-income households', 90, 99)], 2)
    (g1, a1, b1), (g2, a2, b2) = groups
    p1 = r.randrange(a1, b1 + 1)
    p2 = r.randrange(a2, b2 + 1)
    if p1 == p2:
        p2 += 3 if p2 < 95 else -3
    n2 = r.choice([20000, 40000, 50000, 80000, 120000])
    gap = abs(p1 - p2)
    lo, hi = (g1, p1) if p1 < p2 else (g2, p2), (g2, p2) if p1 < p2 else (g1, p1)
    stem = f'A survey in a region near {ctx(r)["city"]} found that {p1}% of {g1} and {p2}% of {g2} have home broadband access. Calculate the gap in access in percentage points'
    key = f'gap = {max(p1, p2)} − {min(p1, p2)} = {gap} percentage points [1]'
    ans = f'{gap} percentage points'
    m = 1
    if D == 1:
        return MCQ(r, stem + '. What is the gap?', f'{gap} percentage points', [f'{p1 + p2} percentage points', f'{round(100 * gap / max(p1, p2))} percentage points', f'{100 - gap} percentage points'], key.replace(' [1]', ''))
    if D >= 2:
        without = round(n2 * (100 - lo[1]) / 100)
        stem += f'. There are {n2:,} {lo[0]} in the region. Calculate how many of them do not have broadband access'
        key += f'; {n2:,} × {100 - lo[1]}% = {without:,} [1]'
        ans += f'; {without:,} {lo[0]} without access'
        m = 2
    if D >= 3:
        stem += f'. Suggest two reasons for the difference between the two groups'
        key += '; reasons such as cost, infrastructure/coverage, skills, age, interest [2]'
        ans += '; reasons: e.g. cost of devices/connection, weaker infrastructure, lack of skills'
        m = 4
    if D >= 5:
        tgt = min(99, hi[1] - 5)
        need = math.ceil(n2 * (tgt - lo[1]) / 100)
        if tgt > lo[1]:
            stem += f', and calculate how many more {lo[0]} must be connected to raise their access to {tgt}%'
            key += f'; ({tgt} − {lo[1]})% × {n2:,} = {need:,} [1]'
            ans += f'; {need:,} more connections needed'
            m = 5
    return Q(stem + '.', ans, key + f'. [{m}]', marks=m, typ='numerical')


ACCESS = [('a user who is blind', 'screen reader software that reads text aloud, with alt text on images'), ('a user with limited hand movement', 'voice recognition / dialogue interface or switch access'),
          ('a user who is deaf', 'subtitles/captions on videos and visual alerts instead of sounds'), ('a user with low vision', 'screen magnifier, large text and high-contrast colour schemes'),
          ('a user with dyslexia', 'clear sans-serif fonts, adjustable spacing and text-to-speech'), ('a user who is colour-blind', 'colour schemes that do not rely on red/green differences, with labels as well as colours')]

t = T(6, 'Reducing the digital divide: initiatives and accessibility features', 'reducing the digital divide', 'initiatives and accessibility features',
      defs=[('accessibility feature', 'A feature of hardware or software that makes it easier for people with disabilities to use, such as a screen reader or captions.'),
            ('screen reader', 'Software that reads out the text on a screen using synthesised speech, used by blind or visually impaired people.'),
            ('community access point', 'A public place, such as a library or community centre, where people can use computers and the internet free or at low cost.')],
      mcqs=[('Which accessibility feature helps a deaf user watch an online lecture?', 'Captions (subtitles)', ['A screen reader', 'Voice recognition', 'A screen magnifier'], 'Captions show the spoken words as text.'),
            ('Which initiative most directly tackles the cost cause of the digital divide?', 'Providing subsidised or free devices and data to low-income families', ['Building faster supercomputers', 'Making websites more colourful', 'Increasing the price of broadband'], 'Reducing cost increases access for poorer households.')],
      exps=[('Explain two initiatives a government could use to reduce the digital divide.', 'Invest in broadband/mobile infrastructure in rural areas; provide free public access in libraries; subsidise devices and data; run digital skills courses.', '2 × (1 mark initiative, 1 mark how it reduces the divide). [4]'),
            ('Explain why websites should be designed to work with screen readers.', 'Blind users rely on screen readers; if images have no alt text or pages are poorly structured, they cannot access the content, which excludes them.', '1 mark blind users rely on them; 1 mark content otherwise inaccessible. [2]')],
      ars=[('Free computer access in public libraries helps to reduce the digital divide.', 'People who cannot afford a computer can still use the internet.'),
           ('Captions on videos improve accessibility.', 'Deaf users can read what is being said.')],
      falses=['Screen readers are designed for deaf users.', 'Raising broadband prices reduces the digital divide.'],
      intros=['The council in {city} and {org} are working together to reduce the digital divide and make online services accessible.',
              '{org} in {city} wants its online services to be available and accessible to everyone in the region.'],
      parts=[('Describe two initiatives that could reduce the digital divide.', 'Rural broadband investment; free public internet access points; subsidised devices; digital skills training; low-cost data plans.', '1 mark each, max 2. [2]'),
             ('Describe two accessibility features that should be included.', 'Alt text for images; captions; resizable text; high contrast; keyboard navigation; compatibility with screen readers; voice input.', '1 mark each, max 2. [2]'),
             ('Explain why training is needed as well as providing equipment.', 'People without digital skills or confidence will not use equipment effectively, so access alone does not close the divide.', '1 mark skills gap; 1 mark consequence. [2]')],
      ev=[('whether providing free devices is the most effective way to reduce the digital divide', 'removes the cost barrier immediately; helps students and job seekers.', 'devices are useless without connectivity and skills; devices become outdated; may be sold; infrastructure and training may have more lasting impact.', 'a combined programme of infrastructure, devices and skills training is more effective than devices alone.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch6_access(r, D):
    u, f = r.choice(ACCESS)
    if D <= 2:
        return MCQ(r, f'Which feature would best help {u} use a website?', cap(f).rstrip('.'), [cap(x[1]).rstrip('.') for x in ACCESS if x[0] != u], f'{u}: {f}.')
    u2, f2 = r.choice([x for x in ACCESS if x[0] != u])
    d = ctx(r)
    return Q(f'{d["org"]} in {d["city"]} is improving its website. Describe a suitable accessibility feature for {u} and for {u2}, explaining how each helps.',
             f'{cap(u)}: {f}. {cap(u2)}: {f2}.', f'1 mark feature + 1 mark explanation for each user. [4]', marks=4)


# =============================================================================== Chapter 7 Copyright and legal issues
t = T(7, 'Copyright legislation and the protection of intellectual property', 'copyright legislation', 'intellectual property',
      defs=[('copyright', 'A legal right that protects the creator of an original work, such as software, music or text, from it being copied, distributed or adapted without permission.'),
            ('intellectual property', 'Creations of the mind, such as inventions, designs, software, music and writing, which can be legally owned and protected.'),
            ('software piracy', 'Illegally copying, distributing or using software without a valid licence.'),
            ('fair use / fair dealing', 'Limited use of copyright material without permission for purposes such as criticism, review, research or teaching, with acknowledgement.')],
      mcqs=[('Which of these would break copyright law?', 'Uploading a purchased film to a public video-sharing site', ['Watching a film you have bought', 'Quoting one sentence of a book in a review with a reference', 'Writing your own song'], 'Distributing copyright material without permission is illegal.'),
            ('Who normally owns the copyright of software written by an employee as part of their job?', 'The employer', ['The employee', 'The customer who buys it', 'Nobody'], 'Work created in the course of employment usually belongs to the employer.')],
      exps=[('Explain why copyright legislation is needed for software.', 'Software is easy and cheap to copy; without protection developers would lose income from their investment, so there would be less incentive to create new software.', '1 mark easy to copy; 1 mark lost income; 1 mark less incentive to innovate. [3]'),
            ('Explain two effects of software piracy on software companies.', 'Loss of sales revenue; less money for development and support; higher prices for legitimate customers; jobs lost.', '2 × (1 mark effect, 1 mark explanation). [4]')],
      ars=[('Copying a purchased music file to share online is illegal.', 'The buyer does not own the copyright.'),
           ('Copyright protects software developers\' income.', 'Others cannot legally copy and sell their work.')],
      falses=['Buying a CD gives you the right to make copies for sale.', 'Copyright only applies to printed books.'],
      intros=['{org}, {aot} in {city}, sells its own software and is making a promotional video using music and images found online.',
              '{p} works in the marketing team of {org} in {city}, which develops software and produces promotional videos.'],
      parts=[('Describe what copyright legislation allows the owner to control.', 'Copying, distributing, adapting, performing, renting or broadcasting the work.', '1 mark per right, max 2. [2]'),
             ('Explain why the material found online cannot simply be used.', 'It is protected by copyright; permission/licence is needed or it must be royalty-free/Creative Commons with attribution.', '1 mark copyright; 1 mark need permission/licence. [2]'),
             ('Describe two methods used to prevent illegal copying of software.', 'Product keys/activation; dongles; digital rights management; holograms on packaging; online licence checks.', '1 mark each, max 2. [2]')],
      ev=[('whether copyright laws are effective in protecting digital content produced by organisations such as {org}', 'legal action possible; deters large-scale copying; supports licensing income.', 'digital content is copied easily and globally; enforcement across countries is difficult; DRM can annoy genuine customers.', 'copyright law is necessary but must be supported by technical protection and affordable legal options.')])


LIC = [('single-user licence', 'the software can be installed and used by one user (or on one computer)'),
       ('multi-user licence', 'the software can be used by a stated number of users, often at the same time (concurrent)'),
       ('site licence', 'the software can be used on any number of computers at one site or within one organisation for a single fee'),
       ('freeware', 'the software is free to use but remains copyright, so it cannot be modified or sold'),
       ('shareware', 'the software can be tried free for a limited period or with limited features; payment is then needed'),
       ('open-source licence', 'the source code is available and can be modified and shared under the licence terms')]

t = T(7, 'Software licensing: single-user, multi-user, site licence, freeware and shareware; preventing piracy', 'software licensing', 'single-user, multi-user, site licence', 'freeware and shareware',
      defs=[('single-user licence', 'A licence that allows the software to be installed and used by one user, or on one computer, only.'),
            ('multi-user licence', 'A licence that allows a stated number of users to use the software, often at the same time (concurrently).'),
            ('site licence', 'A licence that allows software to be used on any number of computers at one site or within one organisation for a single fee.'),
            ('freeware', 'Software that is free to use but is still protected by copyright, so users cannot modify it or sell it.'),
            ('shareware', 'Software that can be used free for a trial period, or with limited features, after which the user must pay to continue using it.'),
            ('open-source licence', 'A licence that makes the source code available so it can be studied, modified and shared under the licence terms.')] + [('product activation', 'A process in which software contacts the developer\'s server to check that its licence key is valid and not already in use on too many computers.')],
      mcqs=[('Which licence lets a school install software on all of its 300 computers for one fee?', 'Site licence', ['Single-user licence', 'Shareware', 'Trial licence'], 'A site licence covers all computers at one site/organisation.'),
            ('Which type of software can be used free for 30 days before payment is required?', 'Shareware', ['Freeware', 'Open-source software', 'Site-licensed software'], 'Shareware is "try before you buy".'),
            ('How does product activation help to prevent piracy?', 'The licence key is checked online and cannot be used on more computers than allowed', ['It encrypts all the user\'s files', 'It deletes the software after one use', 'It prevents the computer connecting to the internet'], 'Activation links a key to installations.')],
      exps=[('Explain the difference between freeware and open-source software.', 'Freeware is free to use but the source code is not available and it cannot be modified; open-source software makes its source code available to be studied, modified and shared.', '1 mark freeware; 1 mark open source. [2]'),
            ('Explain why a large organisation might choose a site licence rather than many single-user licences.', 'One fee covers all users, which is usually cheaper for many computers and easier to manage; new computers are covered without buying more licences.', '1 mark cheaper for many users; 1 mark easier administration. [2]'),
            ('Describe two methods of preventing software piracy.', 'Licence/product keys; online activation; dongles; DRM; holograms on packaging; requiring the original disc.', '1 mark each with description, max 2. [2]')],
      ars=[('A site licence can be cheaper than buying single-user licences for a large organisation.', 'One fee covers every computer at the site.'),
           ('Freeware cannot legally be sold by the user.', 'It is still protected by copyright.')],
      falses=['Shareware never has to be paid for.', 'Freeware always includes the source code.'],
      intros=['{org} in {city} has 120 computers in three buildings and needs a new office software package.',
              '{p}, the IT manager at {org} in {city}, is reviewing how the organisation licenses its software.'],
      parts=[('Describe the difference between a single-user and a multi-user licence.', 'Single-user: one user/computer; multi-user: a set number of users, often concurrent.', '1 mark each. [2]'),
             ('Explain what is meant by shareware.', 'Software that can be used free for a trial period or with limited features before payment.', '1 mark trial; 1 mark payment needed after. [2]'),
             ('Explain two ways the software company may try to prevent piracy.', 'Product keys; online activation; dongles; DRM.', '2 × (1 mark method, 1 mark explanation). [4]')],
      ev=[('whether {org} should use freeware and open-source software instead of buying licences', 'saves licence costs; open source can be adapted; legal to share.', 'less support; compatibility; training costs; may lack features; freeware may contain adverts or be discontinued.', 'a mix is common; key business systems often justify paid licences with support.')])


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ch7_lic(r, D):
    single = r.choice([45, 60, 75, 90, 120, 150])
    site = r.choice([3000, 4500, 6000, 7500, 9000])
    multi_n = r.choice([25, 50])
    multi = r.choice([1000, 1500, 2000, 2500])
    users = r.choice([20, 30, 40, 60, 80, 100, 150])
    d = ctx(r)
    cs = single * users
    packs = math.ceil(users / multi_n)
    cm = packs * multi
    opts = {'single-user licences': cs, f'multi-user licences': cm, 'a site licence': site}
    best = min(opts, key=opts.get)
    stem = (f'{d["org"]} in {d["city"]} needs software for {users} computers. A single-user licence costs ${single}; a multi-user licence for up to {multi_n} users costs ${multi:,}; '
            f'a site licence for unlimited computers costs ${site:,}. Calculate the cost of each option and state the cheapest.')
    key = f'single: {users} × {single} = ${cs:,} [1]; multi-user: {packs} × {multi:,} = ${cm:,} [1]; site ${site:,}; cheapest: {best} [1]'
    ans = f'single ${cs:,}; multi-user ${cm:,}; site ${site:,}; cheapest: {best}'
    m = 3
    if D >= 4:
        be = site // single + 1
        stem += ' Calculate the smallest number of computers for which the site licence would be cheaper than buying single-user licences.'
        key += f'; site < single × n → n > {site} / {single} = {site / single:.2f} → {be} computers [1]'
        ans += f'; site licence cheaper from {be} computers'
        m = 4
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (1, 2, 3), 'short')
def ch7_whichlic(r, D):
    sc = [('A school wants to install a program on every computer in its building.', 'site licence'), ('A home user buys a photo editor for their own laptop.', 'single-user licence'),
          ('A user downloads a game that can be played free for 14 days, then must be paid for.', 'shareware'), ('A user downloads a free media player whose code cannot be changed.', 'freeware'),
          ('An office of 20 staff buys a package that up to 20 people can use at the same time.', 'multi-user licence'), ('A developer downloads a web server and edits its source code.', 'open-source licence')]
    s, k = r.choice(sc)
    if D <= 2:
        return MCQ(r, f'{s} Which type of licence or software is this?', cap(k).rstrip('.'), [cap(x[0]).rstrip('.') for x in LIC if x[0] != k], f'{k}: {dict(LIC)[k]}.')
    s2, k2 = r.choice([x for x in sc if x[1] != k])
    return Q(f'Identify the type of licence or software in each case and describe its terms: (1) {s} (2) {s2}', f'(1) {k} — {dict(LIC)[k]}. (2) {k2} — {dict(LIC)[k2]}.', '1 mark each type, 1 mark each description. [4]', marks=4)


t = T(7, 'Ethical and legal implications of using IT: plagiarism, hacking and acceptable use policies', 'ethical and legal implications', 'plagiarism, hacking', 'acceptable use policies',
      defs=[('plagiarism', 'Presenting someone else\'s work or ideas as your own without acknowledging the source.'),
            ('hacking', 'Gaining unauthorised access to a computer system or data.'),
            ('acceptable use policy (AUP)', 'A set of rules, agreed by users, stating how an organisation\'s IT systems and internet access may and may not be used.'),
            ('ethics', 'Moral principles about what is right and wrong that guide how people behave, including how they use IT.')],
      mcqs=[('Which action is plagiarism?', 'Copying paragraphs from a website into an essay without a reference', ['Quoting a website and listing it in a bibliography', 'Writing an essay in your own words', 'Asking a teacher for feedback'], 'Using others\' work without acknowledgement is plagiarism.'),
            ('Which would normally be in a school\'s acceptable use policy?', 'Users must not share their passwords', ['Users must buy their own printers', 'Users must use the internet for at least 3 hours a day', 'Users may install any software they like'], 'AUPs set rules for safe and appropriate use.'),
            ('A student guesses a teacher\'s password and changes their own marks. Which is the most accurate description?', 'Hacking, which is illegal, and unethical', ['Plagiarism', 'Fair use', 'Permitted under the AUP'], 'Unauthorised access and modification of data is a criminal offence in most countries.')],
      exps=[('Explain why organisations ask employees to sign an acceptable use policy.', 'It sets clear rules for using IT, protecting systems and data from misuse and malware, and lets the organisation take disciplinary action if rules are broken.', '1 mark clear rules; 1 mark protects systems/data; 1 mark basis for discipline. [3]'),
            ('Explain why plagiarism is considered unethical even when it is not illegal.', 'It is dishonest: it takes credit for another person\'s work and misleads the reader or teacher about the author\'s abilities.', '1 mark dishonest/credit; 1 mark misleading. [2]'),
            ('Explain two ways a school can detect or reduce plagiarism.', 'Use plagiarism-detection software that compares work with online sources; teach referencing; set personalised tasks; ask students to explain their work.', '2 × (1 mark method, 1 mark explanation). [4]')],
      ars=[('Hacking is illegal in most countries.', 'It involves gaining unauthorised access to computer systems.'),
           ('Students should reference the sources they use.', 'This acknowledges the original authors and avoids plagiarism.')],
      falses=['Copying from a website is acceptable if the website is free to view.', 'An AUP allows users to do anything that is not illegal.'],
      intros=['{org} in {city} is writing an acceptable use policy after finding personal use of work computers and copied work in reports.',
              'Teachers at {org} in {city} have noticed that several students\' assignments contain identical paragraphs from a website.'],
      parts=[('Describe three rules that could be included in an acceptable use policy.', 'No sharing passwords; no installing unauthorised software; no accessing inappropriate sites; personal use limits; no downloading copyright material; report security problems.', '1 mark each, max 3. [3]'),
             ('Explain what is meant by plagiarism and why it is a problem.', 'Using others\' work without credit; dishonest; work does not show the student\'s ability; may break copyright.', '1 mark meaning; 1 mark problem. [2]'),
             ('Explain the difference between unethical and illegal behaviour, using an example from IT.', 'Illegal breaks the law (e.g. hacking); unethical is morally wrong but may be legal (e.g. reading a colleague\'s screen, plagiarism).', '1 mark each with example. [2]')],
      ev=[('whether monitoring employees\' use of the internet is justified for {org}', 'protects security; enforces the AUP; reduces time wasting; legal compliance.', 'invasion of privacy; reduces trust and morale; cost of monitoring; staff may feel they are not trusted.', 'monitoring can be justified if it is proportionate, transparent and explained in the AUP.')])


# =============================================================================== Chapter 8 Communication and networks
NETDEV = [('router', 'forwards data packets between different networks, such as a LAN and the internet, using IP addresses'),
          ('switch', 'connects devices within a LAN and sends data only to the device it is addressed to, using MAC addresses'),
          ('wireless access point (WAP)', 'allows wireless devices to connect to a wired network'),
          ('network interface card (NIC)', 'hardware in a device that allows it to connect to a network; it has a unique MAC address'),
          ('modem', 'converts digital signals from a computer into analogue signals for transmission over telephone lines, and back again'),
          ('hub', 'connects devices in a LAN but sends incoming data to every connected device'),
          ('bridge', 'connects two LANs that use the same protocol so they behave as one network')]


def ttime(bits, bps):
    return bits / bps


def tstr(secs):
    if secs < 120:
        return f'{num(round(secs, 2))} seconds'
    if secs < 7200:
        return f'{num(round(secs / 60, 2))} minutes'
    return f'{num(round(secs / 3600, 2))} hours'


t = T(8, 'Network types and components: LAN, WAN, routers, switches and the internet', 'network types and components', 'lan, wan, routers, switches',
      defs=[('local area network (LAN)', 'A network covering a small geographical area, such as one building or site, usually owned by the organisation.'),
            ('wide area network (WAN)', 'A network covering a large geographical area, connecting LANs, often using telecommunications links owned by other companies.'),
            ('internet', 'A worldwide network of interconnected networks that communicate using the TCP/IP protocols.')] + [(n, cap(d)) for n, d in NETDEV[:4]],
      mcqs=[('Which device connects a school LAN to the internet?', 'Router', ['Switch', 'Hub', 'Network interface card'], 'Routers connect different networks.'),
            ('Why is a switch more efficient than a hub?', 'It sends data only to the intended device rather than to all devices', ['It connects to the internet', 'It converts analogue to digital signals', 'It is wireless'], 'Less unnecessary traffic and fewer collisions.'),
            ('A file of 40 MB is to be transferred. How many bits is this, using 1 MB = 1 000 000 bytes?', '320 000 000 bits', ['40 000 000 bits', '5 000 000 bits', '320 000 bits'], '40 × 1 000 000 × 8 = 320 000 000 bits.')],
      exps=[('Explain two differences between a LAN and a WAN.', 'A LAN covers a small area such as one building while a WAN covers a large area such as a country; a LAN is usually owned by the organisation while WAN links are often leased from telecoms companies; LANs are usually faster.', '2 × (1 mark difference, explained). [4]'),
            ('Explain why a network interface card is needed.', 'It provides the physical connection to the network and has a unique MAC address so data can be delivered to the correct device.', '1 mark connection; 1 mark MAC address/identification. [2]'),
            ('Explain why transfer speeds are given in bits per second while file sizes are given in bytes.', 'Data is transmitted one bit at a time over a link, so speed is measured in bits; files are stored in bytes; to calculate times, bytes must be multiplied by 8.', '1 mark bits transmitted serially; 1 mark multiply by 8 to convert. [2]')],
      ars=[('A router is needed to connect a LAN to the internet.', 'Routers forward packets between different networks.'),
           ('A switch reduces unnecessary network traffic.', 'It forwards data only to the device whose MAC address matches.')],
      falses=['A hub sends data only to the device it is addressed to.', 'The internet is a single large LAN.'],
      intros=['{org} in {city} is setting up a network for 60 staff in one building, with access to the internet.',
              '{org} has offices in {city} and {city2} and wants staff in both offices to share files.',
              '{p} is installing a network in a small office for {org} in {city}.'],
      parts=[('State whether a LAN or a WAN is needed, giving a reason.', 'LAN for one building/site; WAN to connect offices in different cities.', '1 mark choice; 1 mark reason. [2]'),
             ('Describe the role of a router and of a switch in this network.', 'Router: connects the LAN to the internet/other networks, forwarding packets by IP address. Switch: connects devices within the LAN, sending data to the correct device by MAC address.', '1 mark router; 1 mark switch. [2]'),
             ('Explain why a wireless access point might be added.', 'To let laptops, tablets and phones connect without cables, giving mobility.', '1 mark wireless devices; 1 mark mobility/flexibility. [2]'),
             ('Explain two advantages of networking the computers.', 'Share files, printers and internet connection; central backup; communication by email/messaging; central software installation.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Explain one disadvantage of networking the computers.', 'Viruses can spread; security risks; cost of equipment and technicians; if the server/switch fails many users are affected.', '1 mark point; 1 mark explanation. [2]')],
      ev=[('whether {org} should use a wireless network instead of a cabled network', 'mobility; easy to add devices; no cabling costs or disruption.', 'slower and less reliable; interference; security risks from interception; limited range.', 'many organisations use cables for fixed computers and wireless for mobile devices.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch8_transfer(r, D):
    unit = r.choice(['MB', 'GB']) if D >= 3 else 'MB'
    size = r.choice([5, 8, 12, 25, 40, 64, 120, 250, 500]) if unit == 'MB' else r.choice([1, 2, 4, 5, 8])
    bpsu, mult = r.choice([('Mbps', 10 ** 6), ('Mbps', 10 ** 6), ('kbps', 10 ** 3)]) if D <= 3 else ('Mbps', 10 ** 6)
    sp = r.choice([2, 4, 8, 10, 16, 20, 40, 50, 80, 100]) if bpsu == 'Mbps' else r.choice([256, 512, 800, 1000])
    byt = size * (10 ** 6 if unit == 'MB' else 10 ** 9)
    bits = byt * 8
    secs = bits / (sp * mult)
    what = r.choice(['video file', 'set of photographs', 'software update', 'database backup', 'presentation with embedded video', 'music album'])
    conv = f'1 {unit} = {"1 000 000" if unit == "MB" else "1 000 000 000"} bytes, 1 {bpsu} = {"1 000 000" if bpsu == "Mbps" else "1000"} bits per second'
    if D == 1:
        return MCQ(r, f'A {size} {unit} {what} is sent over a {sp} {bpsu} connection ({conv}). How long does the transfer take?', tstr(secs),
                   [tstr(secs / 8), tstr(secs * 2), tstr(secs / 2), tstr(secs * 8)], f'{size} {unit} × 8 = {bits:,} bits; ÷ {sp * mult:,} = {num(round(secs, 2))} s.')
    stem = f'A {size} {unit} {what} is sent over a connection with a speed of {sp} {bpsu}. Using {conv}, calculate the time taken to transfer the file. Show your working.'
    key = f'{size} {unit} = {byt:,} bytes × 8 = {bits:,} bits [1]; ÷ {sp * mult:,} bps [1] = {num(round(secs, 2))} s' + (f' = {tstr(secs)}' if secs >= 120 else '') + ' [1]'
    m = 3
    ans = tstr(secs)
    if D >= 4:
        f = r.choice([2, 4, 5])
        stem += f' The organisation upgrades to a connection {f} times as fast, but 20% of the bandwidth is used by other traffic. Calculate the new transfer time.'
        eff = sp * f * 0.8 * mult
        s2 = bits / eff
        key += f'; usable speed = {sp} × {f} × 0.8 = {num(sp * f * 0.8)} {bpsu} [1]; time = {bits:,} ÷ {eff:,.0f} = {num(round(s2, 2))} s [1]'
        ans += f'; after upgrade: {tstr(s2)}'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (1, 2, 3), 'short')
def ch8_dev(r, D):
    n, f = r.choice(NETDEV)
    if D <= 2:
        return MCQ(r, f'Which network device {f}?', n.capitalize() if not n.startswith('wireless') else 'Wireless access point (WAP)', [x[0].capitalize() if not x[0].startswith('wireless') else 'Wireless access point (WAP)' for x in NETDEV if x[0] != n], f'{n}: {f}.')
    picks = r.sample(NETDEV, 3)
    return Q('Describe the function of each of these network devices: ' + ', '.join(x[0] for x in picks) + '.', '; '.join(f'{x[0]}: {x[1]}' for x in picks),
             '1 mark each: ' + '; '.join(f'{x[0]} — {x[1]}' for x in picks) + '. [3]', marks=3)


t = T(8, 'Email, instant messaging and video conferencing for communication', 'email, instant messaging and video conferencing', 'video conferencing',
      defs=[('email', 'A method of sending electronic messages, with attachments, from one user to one or more others; messages are stored on a server until read.'),
            ('instant messaging (IM)', 'Real-time text communication between users who are online, often with presence information showing who is available.'),
            ('video conferencing', 'Communication in which people in different places see and hear each other in real time using cameras, microphones, screens and a network.'),
            ('carbon copy (CC) / blind carbon copy (BCC)', 'Email fields that send copies of a message to other recipients; BCC recipients are hidden from the others.')],
      mcqs=[('Which hardware is needed for video conferencing that is not needed for email?', 'A webcam and microphone', ['A keyboard', 'A printer', 'A hard disk'], 'Video and audio must be captured.'),
            ('Why would a manager use BCC when emailing all customers?', 'To keep customers\' email addresses private from each other', ['To make the email arrive faster', 'To encrypt the email', 'To attach larger files'], 'BCC hides other recipients\' addresses.'),
            ('Which is a disadvantage of video conferencing compared with a face-to-face meeting?', 'Poor connections can cause lag and loss of picture or sound', ['Travel costs are higher', 'Meetings cannot be arranged quickly', 'Participants must be in the same room'], 'Quality depends on bandwidth.')],
      exps=[('Explain two advantages of video conferencing for a company with offices in different countries.', 'Reduces travel costs and time; meetings can be arranged quickly; reduces carbon emissions; staff can see body language unlike in email.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why email is more suitable than instant messaging for sending a formal contract.', 'Email supports attachments and formal layout, keeps a permanent record, and the recipient does not need to be online at the same time.', '1 mark per point, max 2. [2]'),
            ('Explain two problems that can arise from using email in an organisation.', 'Spam and phishing emails; malware in attachments; information overload; misunderstandings in tone; sending to the wrong recipient (data breach).', '2 × (1 mark point, 1 mark explanation). [4]')],
      ars=[('Video conferencing can reduce a company\'s travel costs.', 'Staff can meet without travelling to the same place.'),
           ('Email does not require the recipient to be online when it is sent.', 'Messages are stored on a mail server until they are downloaded.')],
      falses=['Instant messaging stores messages for weeks until the user logs in, like letters.', 'Video conferencing needs no special hardware.'],
      intros=['{org} has teams in {city} and {city2} who need to communicate every day.',
              '{p} manages a project at {org} in {city} with partners overseas.'],
      parts=[('Describe the hardware needed for video conferencing.', 'Webcam; microphone; speakers/headset; screen; fast network connection.', '1 mark per item, max 3. [3]'),
             ('Explain when instant messaging would be more suitable than email.', 'For quick, informal questions when the other person is online and an immediate answer is needed.', '1 mark quick/real-time; 1 mark example. [2]'),
             ('Explain two disadvantages of video conferencing.', 'Time zones; lag/poor quality with low bandwidth; cost of equipment; lack of personal contact; security of calls.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Explain how the organisation can protect itself from phishing emails.', 'Train staff to recognise phishing; spam filters; never click unknown links; verify requests by phone.', '1 mark per point, max 2. [2]')],
      ev=[('whether {org} should replace most face-to-face meetings with video conferencing', 'lower travel costs and time; faster decisions; environmental benefits.', 'relationships built in person; technical problems; time zones; fatigue; confidential discussions.', 'video conferencing suits routine meetings; important negotiations may still need face-to-face contact.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch8_video(r, D):
    kbps = r.choice([600, 800, 1200, 1500, 2000, 2500])
    mins = r.choice([30, 45, 60, 90])
    ppl = r.choice([3, 4, 5, 6, 8])
    up_mb = kbps * 1000 * mins * 60 / 8 / 10 ** 6
    if D == 1:
        return MCQ(r, f'A video call uses {kbps} kbps (1 kbps = 1000 bits per second). How many megabytes of data are sent in {mins} minutes (1 MB = 1 000 000 bytes)?', f'{num(round(up_mb, 1))} MB',
                   [f'{num(round(up_mb * 8, 1))} MB', f'{num(round(up_mb / 60, 1))} MB', f'{num(round(up_mb / 8, 1))} MB'], f'{kbps} × 1000 × {mins * 60} ÷ 8 ÷ 10⁶ = {num(round(up_mb, 1))} MB.')
    stem = (f'A video conference between {ppl} offices lasts {mins} minutes. Each office sends a video stream of {kbps} kbps (1 kbps = 1000 bits per second) and receives the streams of all the other offices. '
            f'Calculate (a) the download bandwidth each office needs in kbps and (b) the total data received by one office in MB (1 MB = 1 000 000 bytes).')
    down = kbps * (ppl - 1)
    mb = down * 1000 * mins * 60 / 8 / 10 ** 6
    key = f'(a) {kbps} × ({ppl} − 1) = {down:,} kbps [1] (b) {down:,} × 1000 × {mins} × 60 ÷ 8 ÷ 10⁶ [1] = {num(round(mb, 1))} MB [1]'
    ans = f'(a) {down:,} kbps (b) {num(round(mb, 1))} MB'
    m = 3
    if D >= 4:
        link = r.choice([2, 4, 5, 8, 10])
        ok = down <= link * 1000
        stem += f' (c) One office has a {link} Mbps download link. State whether it is sufficient and explain the effect if it is not.'
        key += f' (c) {link} Mbps = {link * 1000:,} kbps; {"sufficient" if ok else "not sufficient"} [1]; if not, video lags/freezes or quality is reduced [1]'
        ans += f' (c) {"Sufficient" if ok else "Not sufficient"} ({down:,} kbps needed vs {link * 1000:,} kbps); too little bandwidth causes lag or lower quality.'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


CRIT = [('the author and organisation responsible for the site', 'to judge expertise and possible bias'), ('the date the page was last updated', 'to check the information is current'),
        ('the domain, e.g. .gov or .ac', 'government and academic sites are more likely to be reliable'), ('whether sources and references are given', 'so facts can be checked'),
        ('whether the same facts appear on other reliable sites', 'cross-referencing confirms accuracy'), ('the spelling, grammar and presence of adverts', 'poor quality or heavy advertising may indicate an unreliable or commercial site')]

t = T(8, 'Websites, intranets and extranets; search engines and evaluating online information', 'websites, intranets and extranets', 'search engines', 'evaluating online information',
      defs=[('intranet', 'A private network within an organisation, using internet technologies, that can only be accessed by the organisation\'s members.'),
            ('extranet', 'Part of an organisation\'s intranet that authorised outside users, such as suppliers or customers, can access over the internet.'),
            ('search engine', 'Software that searches an index of web pages for given keywords and returns a ranked list of results.'),
            ('website', 'A collection of related web pages on the World Wide Web, accessed using a URL.')],
      mcqs=[('Which would a car manufacturer use to let its suppliers view stock levels securely?', 'An extranet', ['An intranet that only staff can use', 'A public website', 'A search engine'], 'An extranet gives controlled access to outside partners.'),
            ('Which search would find pages containing the exact phrase solar power?', '"solar power"', ['solar OR power', 'solar -power', 'solar power site:gov'], 'Quotation marks search for an exact phrase.'),
            ('Which is the best indicator that information on a website may be unreliable?', 'No author is named and no sources are given', ['The domain ends in .gov', 'The page was updated last week', 'Other reliable sites give the same facts'], 'Unknown authorship and no sources make facts hard to check.')],
      exps=[('Explain two differences between an intranet and the internet.', 'An intranet is private to an organisation while the internet is public; intranet content is controlled and more reliable; an intranet is usually behind a firewall with login needed.', '2 × (1 mark difference, explained). [4]'),
            ('Explain why information found using a search engine may not be reliable.', 'Anyone can publish on the web; results are ranked by popularity or advertising, not accuracy; pages may be out of date or biased.', '1 mark per point, max 3. [3]'),
            ('Describe two ways to refine a search to get more relevant results.', 'Use quotation marks for exact phrases; use AND/OR/NOT (or −) operators; use advanced search filters such as date, site or file type.', '1 mark each, max 2. [2]')],
      ars=[('An extranet allows suppliers to access some company data.', 'It extends the intranet to authorised outside users.'),
           ('Cross-referencing helps check online information.', 'Facts that appear on several reliable sites are more likely to be accurate.')],
      falses=['Search engines only list pages that have been checked for accuracy.', 'An intranet can be accessed by anyone on the internet.'],
      intros=['{org} in {city} wants to share policies and forms with its staff and let its suppliers check orders.',
              '{p} is training staff at {org} in {city} to use the internet, the intranet and the extranet.'],
      parts=[('Explain the difference between an intranet and an extranet.', 'Intranet: private to staff; extranet: gives authorised external users (suppliers, customers) access to part of it.', '1 mark each. [2]'),
             ('Describe three things to check when judging whether a website is reliable.', 'Author/organisation; date updated; domain type; references; cross-check with other sites; bias/advertising; spelling.', '1 mark each, max 3. [3]'),
             ('Describe how a search engine finds and ranks web pages.', 'Web crawlers follow links and index pages; keywords in the query are matched to the index; results ranked using relevance and links/popularity.', '1 mark crawl/index; 1 mark match; 1 mark ranking. [3]'),
             ('Explain one advantage of an intranet for the organisation.', 'Information is shared in one place, up to date and only accessible to staff, which is more secure and reliable.', '1 mark point; 1 mark explanation. [2]')],
      ev=[('whether students should rely on search engines for research rather than on books and libraries', 'fast access to vast, up-to-date information; many formats; searchable.', 'reliability varies; information overload; ranking not by accuracy; books are edited and checked.', 'search engines are valuable if students evaluate sources critically and cross-check facts.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch8_eval(r, D):
    picks = r.sample(CRIT, 2 if D <= 2 else 3)
    d = ctx(r)
    m = 2 * len(picks)
    return Q(f'{d["p"]} found information on a website about health care in {d["city"]}. Describe {len(picks)} checks {d["p"]} could make to decide whether the information is reliable, explaining why each helps.',
             '; '.join(f'Check {x[0]} — {x[1]}' for x in picks), f'1 mark per check, 1 mark per explanation, e.g. ' + '; '.join(f'{x[0]} ({x[1]})' for x in CRIT) + f'. [{m}]', marks=m)


# =============================================================================== Chapter 9 Document production
t = T(9, 'House style, templates and corporate branding', 'house style', 'templates and corporate branding',
      defs=[('house style', 'A set of rules for the appearance of an organisation\'s documents, such as fonts, colours, logo position and layout, so that all documents look consistent.'),
            ('template', 'A pre-designed document or file containing the layout, styles and standard content, used as the starting point for new documents of the same type.'),
            ('corporate branding', 'The use of a consistent name, logo, colour scheme and style across all of an organisation\'s materials so that it is easily recognised.'),
            ('style sheet', 'A stored set of formatting rules (e.g. font, size, colour, spacing) that can be applied to text so that formatting is consistent.')],
      mcqs=[('Why does an organisation use a house style?', 'So that all its documents look consistent and professional', ['So that documents can be printed faster', 'To reduce the file size of documents', 'So that staff can choose their own fonts'], 'Consistency builds a recognisable, professional image.'),
            ('Which is most likely to be included in a letter template?', 'The company logo, address and standard fonts', ['The text of every letter ever sent', 'The recipient\'s bank details', 'A virus checker'], 'Templates hold standard layout and content.')],
      exps=[('Explain two advantages of using templates for business letters.', 'Saves time because standard layout and content already exist; ensures every letter follows the house style; fewer errors because standard details are already correct.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why corporate branding is important to an organisation.', 'Customers recognise the organisation from its logo and colours, which builds trust and loyalty and makes marketing more effective.', '1 mark recognition; 1 mark trust/loyalty/marketing. [2]'),
            ('Describe three items that might be specified in a house style.', 'Font type and size for headings and body; colour scheme; logo size and position; margins and line spacing; paper size; date format.', '1 mark each, max 3. [3]')],
      ars=[('Templates help documents follow a house style.', 'The fonts, layout and logo are already set up in the template.'),
           ('A consistent house style makes an organisation look professional.', 'Every document has the same recognisable appearance.')],
      falses=['A house style means every member of staff chooses their own fonts.', 'Templates can only be used once.'],
      intros=['{org} in {city} has found that staff produce letters and reports that all look different.',
              '{p} is creating a new set of templates for {org} in {city}.'],
      parts=[('Describe what is meant by a house style.', 'Rules for fonts, colours, logo, layout so that documents are consistent.', '1 mark rules; 1 mark consistency. [2]'),
             ('Explain two benefits of using templates.', 'Saves time; consistent house style; fewer mistakes; easier for new staff.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Describe four features that should be specified for the templates.', 'Logo position; heading font and size; body font and size; colour scheme; margins; header/footer content; line spacing.', '1 mark each, max 4. [4]')],
      ev=[('whether {org} should require all staff to use a strict house style', 'consistent professional image; brand recognition; saves time with templates.', 'limits creativity; time to set up and enforce; some documents need different layouts.', 'a house style with templates is beneficial, provided there is flexibility for special documents.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch9_hs(r, D):
    hs = {'heading font': r.choice(['Arial 18 pt bold', 'Calibri 20 pt bold', 'Verdana 16 pt bold']), 'body font': r.choice(['Arial 11 pt', 'Times New Roman 12 pt', 'Calibri 11 pt']),
          'line spacing': r.choice(['1.15', 'single', '1.5']), 'logo': r.choice(['top right, 3 cm wide', 'top left, 4 cm wide', 'centred at the top, 5 cm wide']),
          'margins': r.choice(['2 cm on all sides', '2.5 cm left and right, 2 cm top and bottom'])}
    doc = dict(hs)
    keys = r.sample(list(hs), 2 if D <= 2 else 3)
    alts = {'heading font': ['Comic Sans 14 pt', 'Arial 12 pt italic', 'Times New Roman 24 pt'], 'body font': ['Courier 10 pt', 'Arial 14 pt', 'Calibri 9 pt'],
            'line spacing': ['double', '3.0', '0.8'], 'logo': ['bottom left, 2 cm wide', 'missing', 'top right, 8 cm wide'], 'margins': ['1 cm on all sides', '4 cm left, 1 cm right']}
    for k in keys:
        doc[k] = r.choice([x for x in alts[k] if x != hs[k]])
    d = ctx(r)
    lines = '\n'.join(f'{k}: house style {hs[k]}; document {doc[k]}' for k in hs)
    return Q(f'{d["org"]} in {d["city"]} has a house style. A report produced by {d["p"]} is checked against it:\n{lines}\nIdentify the features that do not follow the house style and state the correction needed for each.',
             '; '.join(f'{k}: change {doc[k]} to {hs[k]}' for k in keys), '1 mark each: ' + '; '.join(f'{k} should be {hs[k]}' for k in keys) + f'. [{len(keys)}]', marks=len(keys))


t = T(9, 'Page layout: headers, footers, columns, tables, section and page breaks', 'page layout', 'headers, footers, columns, tables', 'section and page breaks',
      defs=[('header', 'An area at the top of each page, inside the top margin, used for text such as the document title or logo that repeats on every page.'),
            ('footer', 'An area at the bottom of each page used for repeated items such as page numbers, file name or date.'),
            ('section break', 'A break that divides a document into sections so each can have its own layout, such as orientation, columns or headers.'),
            ('page break', 'A break that forces the text after it to start at the top of a new page.'),
            ('gutter', 'Extra margin space added for binding, or the space between columns of text.')],
      mcqs=[('Which feature lets one page of a report be landscape while the rest are portrait?', 'Section breaks', ['Page breaks', 'Headers', 'Bullet points'], 'Orientation is a section setting.'),
            ('Where should automatic page numbers normally be placed?', 'In the header or footer', ['In a table cell', 'In the main body text of each page', 'In a text box on page 1 only'], 'Headers/footers repeat on every page.'),
            ('Why should a page break be used instead of pressing Enter many times?', 'The new page starts correctly even if text above it is edited', ['It makes the file smaller', 'It changes the font size', 'It adds a page number'], 'Blank lines move when text is added; a page break always forces a new page.')],
      exps=[('Explain why a section break might be used in a newsletter.', 'So that different parts can have different layouts, e.g. a full-width title section followed by a section with two or three columns.', '1 mark different layout per section; 1 mark example. [2]'),
            ('Explain two reasons for using a table rather than tabs to lay out information.', 'Text stays aligned in cells when edited; cells can have borders/shading; columns can be resized and sorted; text wraps within a cell.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why widow and orphan control is used.', 'It prevents a single line of a paragraph appearing alone at the top or bottom of a page, which looks unprofessional and is harder to read.', '1 mark prevents single lines; 1 mark readability/appearance. [2]')],
      ars=[('A section break allows different column layouts in one document.', 'Each section can have its own page layout settings.'),
           ('Page numbers are placed in a footer.', 'Footer content is repeated automatically on every page.')],
      falses=['A page break changes the orientation of the next page.', 'Headers appear only on the first page.'],
      intros=['{p} is producing a 20-page newsletter for {org} in {city}.',
              '{org} in {city} prints a monthly report that must follow strict layout rules.'],
      parts=[('Describe what should be placed in the header and footer.', 'Header: title, logo, organisation name. Footer: page numbers, date, file name, confidentiality notice.', '1 mark header; 1 mark footer. [2]'),
             ('Explain the difference between a page break and a section break.', 'Page break starts a new page; section break starts a new section that can have different layout settings (orientation, columns, headers).', '1 mark each. [2]'),
             ('Explain why the text should be set in columns.', 'Shorter lines are easier to read; typical newspaper/newsletter layout; fits more articles on a page.', '1 mark point; 1 mark explanation. [2]'),
             ('Describe how a table could improve the layout of data in the report.', 'Data aligned in rows and columns; headings; borders/shading; easy to read and compare.', '1 mark per point, max 2. [2]')],
      ev=[('the use of multiple columns rather than a single column of text in documents produced by {org}', 'shorter lines are easier to read; more professional newsletter look; flexible placement of images.', 'harder to edit and fit images; not suitable for long formal reports; can be awkward on screens.', 'columns suit newsletters and leaflets; single columns suit formal reports and on-screen reading.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch9_columns(r, D):
    orient = r.choice(['portrait', 'landscape']) if D >= 3 else 'portrait'
    W = 210 if orient == 'portrait' else 297
    L = r.choice([15, 20, 25, 30])
    R = r.choice([15, 20, 25])
    n = r.choice([2, 3]) if D <= 3 else r.choice([3, 4])
    g = r.choice([5, 8, 10, 12])
    w = (W - L - R - (n - 1) * g) / n
    stem = (f'An A4 page ({W} mm wide in {orient} orientation) has a left margin of {L} mm and a right margin of {R} mm. The text is set in {n} equal columns with a gap of {g} mm between columns. '
            f'Calculate the width of each column.')
    key = f'usable width = {W} − {L} − {R} = {W - L - R} mm [1]; minus {n - 1} × {g} mm gap{'s' if n > 2 else ''} = {W - L - R - (n - 1) * g} mm [1]; ÷ {n} = {num(round(w, 2))} mm [1]'
    if D == 1:
        return MCQ(r, stem.replace('Calculate the width', 'What is the width'), f'{num(round(w, 2))} mm', [f'{num(round((W - L - R) / n, 2))} mm', f'{num(round((W - (n - 1) * g) / n, 2))} mm', f'{num(round(W / n, 2))} mm'], key)
    m = 3
    ans = f'{num(round(w, 2))} mm'
    if D >= 4:
        lh = r.choice([5, 6])
        H = 297 if orient == 'portrait' else 210
        top, bot = r.choice([20, 25]), r.choice([20, 25])
        lines = (H - top - bot) // lh
        nl = r.choice([300, 450, 600, 800])
        pages = math.ceil(nl / (lines * n))
        stem += f' The page is {H} mm high, with top and bottom margins of {top} mm and {bot} mm, and each line of text takes {lh} mm. Calculate how many lines fit in one column and how many pages are needed for {nl} lines of text.'
        key += f'; lines per column = ({H} − {top} − {bot}) ÷ {lh} = {(H - top - bot) / lh:.1f} → {lines} [1]; pages = {nl} ÷ ({lines} × {n}) = {nl / (lines * n):.2f} → {pages} [1]'
        ans += f'; {lines} lines per column; {pages} pages'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


AUTO = [('a table of contents', 'it is generated automatically from heading styles and can be updated when page numbers change'),
        ('automatic page numbering fields', 'numbers update automatically when pages are added or removed'),
        ('an index', 'marked entries are collected and listed alphabetically with page numbers'),
        ('track changes', 'every edit is shown with the reviewer\'s name, so the author can accept or reject each change'),
        ('heading styles', 'formatting is consistent and can be changed in one place; they also build the table of contents'),
        ('a date field', 'the current date is inserted and updates automatically'),
        ('comments', 'reviewers can add notes in the margin without changing the text'),
        ('a mail merge field', 'data from a data source is inserted automatically into each copy of a document')]
AUTO_NEED = {'a table of contents': 'show readers where each chapter starts in a 60-page manual',
             'automatic page numbering fields': 'number every page of a long report so numbers stay correct after editing',
             'an index': 'help readers look up key terms at the back of a textbook',
             'track changes': 'let three managers suggest edits to a contract so the author can see who changed what',
             'heading styles': 'make all headings consistent and change their font in one step',
             'a date field': 'show today\'s date on a letter automatically',
             'comments': 'let a reviewer add notes without altering the text',
             'a mail merge field': 'insert each customer\'s name into a standard letter'}

t = T(9, 'Automating documents: fields, styles, tables of contents, indexes and track changes', 'automating documents', 'fields, styles, tables of contents', 'track changes',
      defs=[('field', 'A placeholder in a document whose content is inserted and updated automatically, such as a page number, date or file name.'),
            ('style', 'A named set of formatting settings (font, size, colour, spacing) that can be applied to text in one step.'),
            ('table of contents', 'A list of the headings in a document with their page numbers, generated automatically from heading styles.'),
            ('track changes', 'A feature that records every edit made to a document, showing who made it, so that changes can be accepted or rejected.')],
      mcqs=[('What must be applied to headings so that a table of contents can be generated automatically?', 'Heading styles', ['Bold formatting only', 'Page breaks', 'Comments'], 'The TOC is built from headings formatted with heading styles.'),
            ('Why is a page-number field better than typing page numbers?', 'It updates automatically when the document changes', ['It uses a larger font', 'It cannot be deleted', 'It prints in colour'], 'Fields recalculate.')],
      exps=[('Explain two advantages of using styles in a long document.', 'Formatting is consistent; the whole document\'s formatting can be changed by editing the style once; heading styles allow an automatic table of contents and navigation pane.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why track changes is useful when several people edit a document.', 'Each edit is shown with who made it, so the author can review and accept or reject each change; nothing is lost and there is a record of changes.', '1 mark shows edits/who; 1 mark accept/reject or record. [2]'),
            ('Explain why an automatically generated table of contents must be updated before printing.', 'If headings or page numbers change after it was generated, it will show wrong page numbers until it is updated.', '1 mark content changes; 1 mark wrong page numbers if not updated. [2]')],
      ars=[('A table of contents can be generated automatically.', 'It is built from text formatted with heading styles.'),
           ('Fields help keep documents up to date.', 'Their contents are recalculated automatically.')],
      falses=['Track changes deletes all edits automatically.', 'Styles must be applied separately to each word.'],
      intros=['{p} is writing a 60-page staff handbook for {org} in {city}, which will be reviewed by several managers.',
              '{org} in {city} produces long technical manuals that are updated every few months.'],
      parts=[('Explain how the table of contents can be produced automatically.', 'Apply heading styles to each heading; insert a TOC which lists headings with page numbers; update it when the document changes.', '1 mark heading styles; 1 mark insert/update TOC. [2]'),
             ('Describe two fields that could be inserted in the footer.', 'Page number; total pages; file name; date; author.', '1 mark each, max 2. [2]'),
             ('Explain how track changes would help the review process.', 'Edits are shown with reviewer names; the author accepts or rejects each; comments explain suggestions.', '1 mark per point, max 2. [2]'),
             ('Explain why styles should be used rather than formatting each heading by hand.', 'Consistent, quicker, change all at once, needed for TOC.', '1 mark per point, max 2. [2]')],
      ev=[('the use of automated features such as styles, fields and an automatic table of contents in the documents of {org}', 'consistency; saves time; fewer errors; easy updates.', 'staff need training; features can be misused (e.g. manual formatting breaks the TOC); setting up takes time.', 'automation is very beneficial for long, frequently updated documents if staff are trained.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch9_auto(r, D):
    f, why = r.choice(AUTO)
    need = AUTO_NEED[f]
    if D <= 2:
        return MCQ(r, f'Which word-processing feature should be used to {need}?', cap(f).rstrip('.'), [cap(x[0]).rstrip('.') for x in AUTO if x[0] != f], f'{f}: {why}.')
    f2, why2 = r.choice([x for x in AUTO if x[0] != f])
    return Q(f'Name the most suitable feature for each task and explain why it is suitable: (1) to {need}; (2) to {AUTO_NEED[f2]}.', f'(1) {f}: {why}. (2) {f2}: {why2}.',
             '1 mark each feature, 1 mark each explanation. [4]', marks=4)


# =============================================================================== Chapter 10 Database and file concepts
SCHEMAS2 = [
    ('CUSTOMER(CustomerID, Name, Email)', 'ORDER(OrderID, OrderDate, CustomerID)', 'CustomerID', 'OrderID', 'CustomerID in ORDER', 'one-to-many', 'one customer can place many orders but each order belongs to one customer'),
    ('TEACHER(TeacherID, Name, Subject)', 'CLASS(ClassID, Room, TeacherID)', 'TeacherID', 'ClassID', 'TeacherID in CLASS', 'one-to-many', 'one teacher teaches many classes but each class has one teacher'),
    ('DEPARTMENT(DeptID, DeptName)', 'EMPLOYEE(EmployeeID, Name, DeptID)', 'DeptID', 'EmployeeID', 'DeptID in EMPLOYEE', 'one-to-many', 'one department has many employees but each employee works in one department'),
    ('AUTHOR(AuthorID, Name, Country)', 'BOOK(ISBN, Title, AuthorID)', 'AuthorID', 'ISBN', 'AuthorID in BOOK', 'one-to-many', 'one author writes many books but (here) each book has one author'),
    ('PATIENT(PatientID, Name, DOB)', 'APPOINTMENT(AppointmentID, Date, Time, PatientID)', 'PatientID', 'AppointmentID', 'PatientID in APPOINTMENT', 'one-to-many', 'one patient has many appointments; each appointment is for one patient'),
    ('EMPLOYEE(EmployeeID, Name)', 'PARKING_SPACE(SpaceNo, Level, EmployeeID)', 'EmployeeID', 'SpaceNo', 'EmployeeID in PARKING_SPACE', 'one-to-one', 'each employee has one parking space and each space is allocated to one employee'),
]

t = T(10, 'Flat-file and relational databases; primary, foreign and compound keys; relationships', 'flat-file and relational databases', 'primary, foreign and compound keys', 'relationships',
      defs=[('flat-file database', 'A database that stores all its data in a single table.'),
            ('relational database', 'A database that stores data in several linked tables, connected by relationships between key fields.'),
            ('primary key', 'A field (or fields) whose value uniquely identifies each record in a table.'),
            ('foreign key', 'A field in one table that is the primary key of another table, used to link the two tables.'),
            ('compound key', 'A primary key made up of two or more fields which together uniquely identify each record.'),
            ('referential integrity', 'A rule that a foreign key value must match an existing primary key value in the linked table, so there are no orphan records.')],
      mcqs=[('Why is a many-to-many relationship replaced by two one-to-many relationships?', 'Relational databases cannot implement many-to-many relationships directly, so a link table is used', ['To make the database flat-file', 'To remove all primary keys', 'To speed up printing'], 'A link (junction) table with a compound key resolves M:M.'),
            ('A STUDENT table and a COURSE table are linked by an ENROLMENT table with fields StudentID and CourseID. What is the primary key of ENROLMENT?', 'A compound key of StudentID and CourseID', ['StudentID only', 'CourseID only', 'There is no primary key'], 'The pair is unique; each alone repeats.'),
            ('What is the main problem with storing customer details in every order record of a flat-file database?', 'Data redundancy, which can lead to inconsistent data', ['The file cannot be sorted', 'Orders cannot be printed', 'Customers cannot have email addresses'], 'Repeated data wastes space and may be updated in one place but not another.')],
      exps=[('Explain two advantages of a relational database over a flat-file database.', 'Less data redundancy, as data is stored once and linked; better data integrity/consistency because updates are made in one place; more flexible queries across tables; easier to control access to specific tables.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why a name is not a suitable primary key.', 'Names are not unique (two people can share a name) and can change, so they cannot reliably identify a record.', '1 mark not unique; 1 mark may change. [2]'),
            ('Explain how referential integrity prevents errors.', 'It stops a foreign key value being entered that does not exist as a primary key in the linked table, and stops linked records being deleted, so there are no orphan records.', '1 mark foreign key must match; 1 mark no orphan records/deletion prevented. [2]')],
      ars=[('A foreign key links two tables.', 'It matches the primary key of another table.'),
           ('Relational databases reduce data redundancy.', 'Data is stored once in one table and referred to by key fields.'),
           ('A compound key uses more than one field.', 'No single field is unique on its own.')],
      falses=['A primary key value can appear many times in its own table.', 'Flat-file databases always contain many linked tables.', 'Foreign keys must be unique in their table.'],
      intros=['{org} in {city} stores all its data about customers, orders and products in one large spreadsheet table.',
              '{p} is designing a relational database for {org} in {city}.'],
      parts=[('Explain what is meant by a primary key and give an example.', 'A field whose value is unique for each record, e.g. CustomerID.', '1 mark definition; 1 mark example. [2]'),
             ('Explain what is meant by a foreign key.', 'A field in one table that is the primary key in another, linking the tables.', '1 mark each part. [2]'),
             ('Explain two problems of storing all the data in one flat file.', 'Redundancy; inconsistency when data is updated in one place but not another; wasted storage; insertion/deletion anomalies.', '2 × (1 mark point, 1 mark explanation). [4]'),
             ('Describe what a compound key is and when it is used.', 'A key made of two or more fields, used when no single field is unique, e.g. in a link table.', '1 mark meaning; 1 mark when used. [2]')],
      ev=[('whether {org} should replace its flat-file system with a relational database', 'less redundancy and fewer inconsistencies; better queries; access control; scalability.', 'design and migration costs; staff training; more complex to set up; a small simple dataset may not need it.', 'for linked data that changes frequently, a relational database is usually worth the cost.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def ch10_keys(r, D):
    a, b, pk1, pk2, fk, rel, why = r.choice(SCHEMAS2)
    if D <= 2:
        k = r.randrange(3)
        if k == 0:
            return MCQ(r, f'A database has the tables {a} and {b}. Which field is the foreign key?', fk, [f'{pk2} in {b.split("(")[0]}', f'{pk1} in {a.split("(")[0]}', f'Name in {a.split("(")[0]}'] if 'Name' in a else [f'{pk2} in {b.split("(")[0]}', f'{pk1} in {a.split("(")[0]}', 'There is no foreign key'],
                       f'{fk} links to the primary key {pk1}.')
        if k == 1:
            return MCQ(r, f'A database has the tables {a} and {b}. What type of relationship is there between the tables?', rel.capitalize(), [x.capitalize() for x in ('one-to-one', 'one-to-many', 'many-to-many', 'many-to-one (from the first table to the second)') if x != rel],
                       f'{rel}: {why}.')
        return Q(f'A database has the tables {a} and {b}. Identify the primary key of each table.', f'{pk1}; {pk2}', f'1 mark each: {pk1}, {pk2}. [2]', marks=2)
    stem = f'A database has the tables {a} and {b}. (a) Identify the primary key of each table. (b) Identify the foreign key. (c) State the type of relationship and explain why.'
    key = f'(a) {pk1}, {pk2} [2] (b) {fk} [1] (c) {rel} [1]: {why} [1]'
    m = 5
    ans = f'(a) {pk1}; {pk2} (b) {fk} (c) {rel}: {why}.'
    if D >= 5:
        stem += ' (d) Explain how referential integrity would apply to these tables.'
        key += f' (d) every {fk.split(" in ")[0]} value in {b.split("(")[0]} must exist in {a.split("(")[0]}; a record in {a.split("(")[0]} cannot be deleted while linked records exist [1]'
        ans += f' (d) A {fk.split(" in ")[0]} cannot be entered in {b.split("(")[0]} unless it exists in {a.split("(")[0]}.'
        m = 6
    return Q(stem, ans, key + f'. [{m}]', marks=m)


def like(pattern, s):
    """Access-style Like: ? any char, # digit, * any sequence, [A-Z] range."""
    rx = ''
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == '?':
            rx += '.'
        elif c == '#':
            rx += r'\d'
        elif c == '*':
            rx += '.*'
        elif c == '[':
            j = pattern.index(']', i)
            rx += '[' + pattern[i + 1:j] + ']'
            i = j
        else:
            rx += re.escape(c)
        i += 1
    return re.fullmatch(rx, s) is not None


VRULES = [
    ('Mark', '>=0 And <=100', lambda v: isinstance(v, int) and 0 <= v <= 100, [45, 100, 0, 101, -3, 72, 150]),
    ('Quantity', '>0 And <=50', lambda v: isinstance(v, int) and 0 < v <= 50, [0, 1, 50, 51, 25, 12, 70]),
    ('Size', 'In ("S","M","L","XL")', lambda v: v in ('S', 'M', 'L', 'XL'), ['M', 'XL', 'XXL', 'm', 'L', 'Small']),
    ('ProductCode', 'Like "??###"', lambda v: isinstance(v, str) and like('??###', v), ['AB123', 'A1234', 'XY12', 'QR987', 'ab555', 'TT1000']),
    ('StudentID', 'Like "S####"', lambda v: isinstance(v, str) and like('S####', v), ['S1234', 'S123', 'T1234', 'S98765', 'S0001', 's4321']),
    ('Postcode', 'Like "[A-Z][A-Z]# #[A-Z][A-Z]"', lambda v: isinstance(v, str) and like('[A-Z][A-Z]# #[A-Z][A-Z]', v), ['AB1 2CD', 'A12 3BC', 'XY9 8ZZ', 'AB12CD', 'QR5 5QQ']),
    ('Age', 'Between 18 And 65', lambda v: isinstance(v, int) and 18 <= v <= 65, [17, 18, 40, 65, 66, 30]),
    ('Rating', '>=1 And <=5', lambda v: isinstance(v, int) and 1 <= v <= 5, [0, 1, 3, 5, 6, 4]),
]

t = T(10, 'Designing data entry forms and validation rules', 'designing data entry forms', 'validation rules',
      defs=[('data entry form', 'A screen layout used to enter, view and edit one record at a time, designed to make data entry quick and accurate.'),
            ('validation rule', 'A rule set on a field that data must obey before it is accepted, such as a range or pattern.'),
            ('validation text', 'The message shown to the user when data breaks the validation rule, explaining what should be entered.'),
            ('drop-down list (combo box)', 'A form control that lets the user choose a value from a list of options instead of typing it.')],
      mcqs=[('Why might a form use a drop-down list for the "Country" field?', 'It prevents spelling mistakes and ensures only valid values are entered', ['It makes the form load faster', 'It allows any text to be entered', 'It removes the need for a primary key'], 'Choosing from a list acts as a lookup check.'),
            ('Which validation rule would accept only whole numbers from 1 to 10 in an Access-style database?', 'Between 1 And 10 (with an integer data type)', ['Like "##"', '>10', 'In (1, 10)'], 'Between is inclusive; the integer type stops decimals.'),
            ('What is the purpose of validation text?', 'To tell the user why the data was rejected and what to enter instead', ['To store the data in the field', 'To encrypt the data', 'To sort the records'], 'Helpful error messages reduce repeated mistakes.')],
      exps=[('Explain three features of a well-designed data entry form.', 'Clear title and labels; fields in a logical order matching the source document; drop-down lists/radio buttons/tick boxes; helpful error messages; consistent layout; navigation buttons; not overcrowded.', '1 mark per feature with explanation, max 3. [3]'),
            ('Explain why radio buttons are suitable for a field with only a few possible values.', 'Users simply click one option, which is quick and prevents invalid entries; only one option can be selected.', '1 mark quick/no typing; 1 mark prevents invalid values/one choice. [2]'),
            ('Explain why the order of fields on a form should match the paper source document.', 'The operator can work through both in the same order, which is quicker and reduces the chance of entering data into the wrong field.', '1 mark quicker; 1 mark fewer errors. [2]')],
      ars=[('Drop-down lists reduce data entry errors.', 'Users choose from valid values instead of typing.'),
           ('Validation text should explain what is expected.', 'Users then know how to correct their entry.')],
      falses=['A validation rule guarantees that data is correct.', 'Validation text is the data stored in the field.'],
      intros=['{p} is designing a form for {org} in {city} so that staff can enter new customer records.',
              '{org} in {city} is creating an online membership form linked to its database.'],
      parts=[('Describe three features that should be included on the form.', 'Title; clear labels; logical order; drop-down lists; radio buttons; tick boxes; navigation/save buttons; help text.', '1 mark each, max 3. [3]'),
             ('Write a validation rule for a field "Age" that must be from 16 to 99, and suitable validation text.', 'Rule: Between 16 And 99 (or >=16 And <=99). Text: "Please enter an age from 16 to 99".', '1 mark rule; 1 mark text. [2]'),
             ('Explain why a drop-down list should be used for the field "MembershipType".', 'Only a small set of valid values; prevents spelling errors; quicker to enter.', '1 mark per point, max 2. [2]'),
             ('Explain why the form should only show one record at a time.', 'It is less confusing and reduces the chance of editing the wrong record.', '1 mark clarity; 1 mark fewer errors. [2]')],
      ev=[('the design of a data entry form that makes heavy use of drop-down lists and validation rules for {org}', 'fewer errors; faster entry; consistent data.', 'lists can be long and slow to scroll; valid but wrong choices still possible; inflexible when new values are needed; rules can frustrate users.', 'controls and validation greatly improve data quality but must be chosen carefully and kept up to date.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def ch10_vrule(r, D):
    fld, rule, ok, vals = r.choice(VRULES)
    vs = r.sample(vals, min(len(vals), 3 if D <= 2 else (4 if D <= 4 else 5)))
    if D == 1:
        v = vs[0]
        res = 'Accepted' if ok(v) else 'Rejected'
        return MCQ(r, f'The field {fld} has the validation rule {rule} (? = any character, # = any digit). Is the value {v!r} accepted or rejected?'.replace("'", '"'), res,
                   ['Rejected' if res == 'Accepted' else 'Accepted', 'Accepted only if the field is a primary key', 'It depends on the validation text'], f'{v} {"meets" if ok(v) else "does not meet"} {rule}.')
    stem = (f'In a database for {ctx(r)["org"]}, the field {fld} has the validation rule {rule}' + (' (? = any single character, # = any digit, [A-Z] = any capital letter)' if 'Like' in rule else '') +
            '. State whether each value is accepted or rejected: ' + ', '.join(str(v) for v in vs) + '.')
    ans = '; '.join(f'{v} {"accepted" if ok(v) else "rejected"}' for v in vs)
    m = len(vs)
    key = '1 mark each: ' + ans
    if D >= 4:
        stem += ' Suggest suitable validation text for this field.'
        key += '; validation text explains the rule in plain language [1]'
        ans += f'; e.g. validation text: "{fld} must match {rule}" written clearly for the user'
        m += 1
    return Q(stem, ans, key + f'. [{m}]', marks=m)


# ------------------------------------------------------------------ queries
FIRSTN = ['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah', 'Leila', 'Ethan', 'Priya', 'Omar', 'Chloe', 'Daniel', 'Mei', 'Tariq', 'Hana', 'Jonas', 'Ines', 'Kwame']


def q_rows(r):
    kind = r.randrange(3)
    if kind == 0:
        hdr = ['ProductID', 'Name', 'Category', 'Price', 'Stock']
        names = r.sample(['Desk', 'Chair', 'Lamp', 'Shelf', 'Sofa', 'Stool', 'Bench', 'Table', 'Cabinet', 'Mirror', 'Rug', 'Clock'], 7)
        rows = [[f'P{r.randrange(100, 999)}', n, r.choice(['Office', 'Home', 'Garden']), r.choice([15, 25, 40, 55, 80, 120, 150, 210, 35, 60]), r.randrange(0, 60)] for n in names]
        return 'PRODUCT', hdr, rows, 'Price', 'Stock', 'Category', 'Name'
    if kind == 1:
        hdr = ['StudentID', 'FirstName', 'Form', 'Maths', 'Science']
        rows = [[f'S{r.randrange(1000, 9999)}', n, r.choice(['11A', '11B', '11C']), r.randrange(30, 100), r.randrange(30, 100)] for n in r.sample(FIRSTN, 7)]
        return 'STUDENT', hdr, rows, 'Maths', 'Science', 'Form', 'FirstName'
    hdr = ['BookingID', 'Guest', 'RoomType', 'Nights', 'RatePerNight']
    rows = [[f'B{r.randrange(100, 999)}', n, r.choice(['Single', 'Double', 'Suite']), r.randrange(1, 9), r.choice([60, 75, 90, 110, 150, 220])] for n in r.sample(FIRSTN, 7)]
    return 'BOOKING', hdr, rows, 'Nights', 'RatePerNight', 'RoomType', 'Guest'


def _ok(row, hdr, c):
    f, op, v = c
    x = row[hdr.index(f)]
    if op == 'Like':
        return like(v, str(x))
    return {'>': x > v, '<': x < v, '>=': x >= v, '<=': x <= v, '=': x == v, '<>': x != v}[op]


def _ctext(c):
    f, op, v = c
    return f'{f} {op} "{v}"' if isinstance(v, str) else f'{f} {op} {v}'


t = T(10, 'Queries with multiple criteria, calculated fields and reports with grouping and summaries', 'queries with multiple criteria', 'calculated fields', 'reports with grouping and summaries',
      defs=[('query', 'A request to search a database for records that meet given criteria, showing only the chosen fields.'),
            ('calculated field', 'A field in a query or report whose value is worked out from other fields, e.g. Total: [Price]*[Quantity], rather than being stored.'),
            ('report', 'A formatted output of data from a table or query, designed for printing or display, which can group records and show summaries.'),
            ('wildcard', 'A symbol such as * or ? used in search criteria to stand for any characters, e.g. Like "S*" finds values starting with S.')],
      mcqs=[('Why is a person\'s age usually calculated in a query rather than stored in a table?', 'It changes over time, so storing it would make the data out of date', ['Ages cannot be stored as numbers', 'Queries are not allowed to use dates', 'It makes the table load faster'], 'Store date of birth; calculate age when needed.'),
            ('Which criterion finds all names beginning with the letter M?', 'Like "M*"', ['Like "*M"', '= "M"', '> "M"'], '* matches any sequence of characters after M.'),
            ('In a report, why might records be grouped by Category?', 'So that subtotals and counts can be shown for each category', ['So that records are deleted', 'To encrypt the data', 'To change the primary key'], 'Grouping allows summaries per group.')],
      exps=[('Explain the difference between using AND and OR to combine two search criteria.', 'AND returns only records that meet both criteria, so fewer records; OR returns records that meet at least one criterion, so more records.', '1 mark AND both; 1 mark OR either. [2]'),
            ('Explain why a calculated field is used instead of storing the total cost of each order.', 'The value can always be worked out from stored fields, so storing it wastes space and could become inconsistent if a price or quantity is changed.', '1 mark derived from other fields; 1 mark avoids redundancy/inconsistency. [2]'),
            ('Explain why reports are used rather than printing a table directly.', 'Reports can be formatted professionally, show only chosen fields, group and sort records and add totals, counts and averages.', '1 mark per point, max 3. [3]')],
      ars=[('A query using AND returns fewer or the same number of records as one using OR with the same criteria.', 'AND requires both conditions to be true.'),
           ('Calculated fields reduce data redundancy.', 'Values that can be derived are not stored.')],
      falses=['A query permanently deletes records that do not meet the criteria.', 'Like "*S" finds values that begin with S.'],
      intros=['{org} in {city} keeps its records in a relational database and managers want regular reports.',
              '{p} is creating queries and reports in the database used by {org} in {city}.'],
      parts=[('Explain what is meant by a calculated field, giving an example.', 'A field computed from other fields, e.g. Total: [Price]*[Quantity].', '1 mark meaning; 1 mark example. [2]'),
             ('Describe how a report can group and summarise data.', 'Records grouped by a field (e.g. Region) with group headers; subtotals, counts or averages in group footers; grand total in report footer.', '1 mark grouping; 1 mark summary functions. [2]'),
             ('Explain why parameter queries are useful.', 'The user enters the criterion when the query runs (e.g. a date), so one query can be reused for different values.', '1 mark prompt for value; 1 mark reuse. [2]'),
             ('Explain the effect of using a wildcard in a search criterion.', 'It matches any characters, so partial matches such as all names starting with "A" are found.', '1 mark matches any characters; 1 mark example. [2]')],
      ev=[('the use of queries and reports by managers at {org} instead of examining raw tables', 'only relevant data is shown; summaries support decisions; reusable and consistent; formatted for audiences.', 'poorly designed criteria can give misleading results; training needed; reports may hide detail.', 'queries and reports are essential for decision-making if they are well designed and tested.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch10_query(r, D):
    name, hdr, rows, n1, n2, cat, lab = q_rows(r)
    v1 = sorted(x[hdr.index(n1)] for x in rows)[3]
    op1 = r.choice(['>', '<', '>=', '<='])
    conds = [(n1, op1, v1)]
    conj = 'AND'
    if D >= 2:
        cv = r.choice([x[hdr.index(cat)] for x in rows])
        conds.append((cat, '=', cv))
        if D >= 4 and r.random() < 0.5:
            conj = 'OR'
    if D >= 5:
        letter = r.choice([x[hdr.index(lab)][0] for x in rows])
        conds = [conds[0], (lab, 'Like', letter + '*')]
        conj = r.choice(['AND', 'OR'])
    sel = [x for x in rows if (all(_ok(x, hdr, c) for c in conds) if conj == 'AND' else any(_ok(x, hdr, c) for c in conds))]
    table = tbl(hdr, rows)
    crit = f' {conj} '.join(_ctext(c) for c in conds)
    show = [hdr[0], lab]
    if D == 1:
        k = len(sel)
        return MCQ(r, f'Table {name}:\n{table}\nHow many records are returned by a query with the criterion {crit}?', str(k), [str(x) for x in (k + 1, k + 2, max(0, k - 1), k + 3) if x != k], f'Records: {", ".join(x[0] for x in sel) or "none"}.')
    sql = f'SELECT {", ".join(show)} FROM {name} WHERE {crit} ORDER BY {lab};'
    form = r.choice(['sql', 'grid'])
    if form == 'sql':
        stem = f'Table {name}:\n{table}\nState the output of this query.\n{sql}'
    else:
        stem = f'Table {name}:\n{table}\nA query shows the fields {show[0]} and {show[1]}, sorted by {lab} in ascending order, for records where {crit}. State the output of the query.'
    sel_s = sorted(sel, key=lambda x: x[hdr.index(lab)])
    out = '; '.join(f'{x[0]} {x[hdr.index(lab)]}' for x in sel_s) or 'no records'
    m = max(2, min(4, len(sel_s) + 1))
    key = f'Matching records: {out} — up to {m - 1} marks for the correct records, 1 mark for correct fields and order'
    ans = out
    if D >= 4:
        calc = f'{n1}*{n2}' if name != 'STUDENT' else f'({n1}+{n2})/2'
        fx = (lambda x: x[hdr.index(n1)] * x[hdr.index(n2)]) if name != 'STUDENT' else (lambda x: (x[hdr.index(n1)] + x[hdr.index(n2)]) / 2)
        stem += f' A calculated field Result: {calc} is added to the query. Give its value for each record returned.'
        vals = '; '.join(f'{x[0]} {num(fx(x))}' for x in sel_s) or 'none'
        ans += f'; Result: {vals}'
        m += 1
        key += f'; calculated field values: {vals} (1 mark)'
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ch10_group(r, D):
    name, hdr, rows, n1, n2, cat, lab = q_rows(r)
    groups = {}
    for x in rows:
        groups.setdefault(x[hdr.index(cat)], []).append(x[hdr.index(n1)])
    fn = r.choice(['Count', 'Sum', 'Avg']) if D >= 3 else r.choice(['Count', 'Sum'])
    res = {g: (len(v) if fn == 'Count' else (sum(v) if fn == 'Sum' else sum(v) / len(v))) for g, v in groups.items()}
    table = tbl(hdr, rows)
    stem = f'Table {name}:\n{table}\nA report groups the records by {cat} and shows the {dict(Count="number of records", Sum=f"total {n1}", Avg=f"average {n1}")[fn]} for each group. Give the value shown for each group.'
    out = '; '.join(f'{g}: {num(round(v, 2))}' for g, v in sorted(res.items()))
    m = len(res)
    key = '1 mark each group: ' + out
    if D >= 4:
        tot = sum(len(v) for v in groups.values()) if fn == 'Count' else (sum(sum(v) for v in groups.values()) if fn == 'Sum' else sum(sum(v) for v in groups.values()) / len(rows))
        stem += ' Also give the value shown in the report footer for all records.'
        out += f'; all records: {num(round(tot, 2))}'
        key += f'; footer {num(round(tot, 2))} [1]'
        m += 1
    return Q(stem, out, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C4', (3, 4, 5), 'multi_step')
def ch10_writeq(r, D):
    name, hdr, rows, n1, n2, cat, lab = q_rows(r)
    v1 = sorted(x[hdr.index(n1)] for x in rows)[3]
    cv = r.choice([x[hdr.index(cat)] for x in rows])
    op = r.choice(['>', '<'])
    wop = {'>': 'more than', '<': 'less than'}[op]
    sel = sorted([x for x in rows if _ok(x, hdr, (n1, op, v1)) and x[hdr.index(cat)] == cv], key=lambda x: x[hdr.index(lab)], reverse=True)
    sql = f'SELECT {hdr[0]}, {lab}, {n1} FROM {name} WHERE {n1} {op} {v1} AND {cat} = "{cv}" ORDER BY {lab} DESC;'
    stem = (f'Table {name}:\n{tbl(hdr, rows)}\n(a) Write a query (in SQL or as a query-grid description) to show {hdr[0]}, {lab} and {n1} for records where {n1} is {wop} {v1} and {cat} is "{cv}", '
            f'sorted by {lab} in descending order. (b) State the output of your query.')
    out = '; '.join(f'{x[0]} {x[hdr.index(lab)]} {x[hdr.index(n1)]}' for x in sel) or 'no records'
    m = 6
    key = f'(a) correct fields [1]; table [1]; criterion {n1} {op} {v1} [1]; {cat} = "{cv}" combined with AND [1]; sort descending [1] (b) {out} [1]. [{m}]'
    return Q(stem, f'(a) {sql} (b) {out}', key, marks=m, typ='multi_step')


NORMS = [
    ('ORDER(OrderID, OrderDate, CustomerID, CustomerName, ProductID, ProductName, Quantity)', 'CUSTOMER(CustomerID, CustomerName); PRODUCT(ProductID, ProductName); ORDER(OrderID, OrderDate, CustomerID); ORDER_LINE(OrderID, ProductID, Quantity)',
     'CustomerName depends on CustomerID, not on OrderID (transitive dependency); ProductName depends only on ProductID (partial dependency on part of the key OrderID+ProductID)'),
    ('STUDENT_COURSE(StudentID, StudentName, CourseID, CourseTitle, TutorID, TutorName, Grade)', 'STUDENT(StudentID, StudentName); COURSE(CourseID, CourseTitle, TutorID); TUTOR(TutorID, TutorName); ENROLMENT(StudentID, CourseID, Grade)',
     'StudentName depends only on StudentID and CourseTitle only on CourseID (partial dependencies); TutorName depends on TutorID (transitive dependency)'),
    ('LOAN(LoanID, MemberID, MemberName, BookID, Title, AuthorName, LoanDate)', 'MEMBER(MemberID, MemberName); BOOK(BookID, Title, AuthorName); LOAN(LoanID, MemberID, BookID, LoanDate)',
     'MemberName depends on MemberID and Title/AuthorName depend on BookID, not on LoanID (transitive dependencies)'),
]
DICT = [('CustomerID', 'Text', 6, 'Format check: "C" followed by 5 digits (Like "C#####")'), ('DateOfBirth', 'Date/Time', 'n/a', 'Must be before today'),
        ('Price', 'Currency', 'n/a', '>0'), ('Quantity', 'Number (integer)', 'n/a', 'Between 1 And 500'), ('Email', 'Text', 50, 'Must contain "@" (Like "*@*.*")'),
        ('IsMember', 'Boolean (Yes/No)', 'n/a', 'Yes or No only'), ('Surname', 'Text', 30, 'Presence check (Is Not Null)'), ('PhoneNumber', 'Text', 15, 'Length check; digits only')]

t = T(10, 'Normalisation to 3NF and data dictionaries', 'normalisation to 3nf', 'data dictionaries',
      defs=[('normalisation', 'The process of organising data into linked tables to reduce data redundancy and remove anomalies.'),
            ('first normal form (1NF)', 'A table is in 1NF when it has no repeating groups of attributes and every field contains a single (atomic) value, with a primary key.'),
            ('second normal form (2NF)', 'A table is in 2NF when it is in 1NF and every non-key attribute depends on the whole primary key, with no partial dependencies.'),
            ('third normal form (3NF)', 'A table is in 3NF when it is in 2NF and no non-key attribute depends on another non-key attribute (no transitive dependencies).'),
            ('data dictionary', 'A file of metadata describing the data in a database, such as field names, data types, field sizes, validation rules and relationships.')],
      mcqs=[('Which is the main purpose of normalisation?', 'To reduce data redundancy and avoid update anomalies', ['To make the database run without a computer', 'To add repeating groups', 'To remove all relationships'], 'Normalised data is stored once.'),
            ('Which data type is most suitable for a telephone number such as 0044 7712 345678?', 'Text', ['Integer', 'Real', 'Boolean'], 'Leading zeros and spaces must be kept, and no arithmetic is done.'),
            ('Which item is NOT normally stored in a data dictionary?', 'The actual records of customers', ['Field names', 'Data types', 'Validation rules'], 'A data dictionary stores metadata, not the data itself.')],
      exps=[('Explain what is meant by a transitive dependency, using an example.', 'A non-key field depends on another non-key field rather than directly on the primary key, e.g. in ORDER(OrderID, CustomerID, CustomerName), CustomerName depends on CustomerID.', '1 mark meaning; 1 mark example. [2]'),
            ('Explain why a data dictionary is useful to database developers.', 'It documents every field\'s name, type, size and validation so developers build and maintain the database consistently and understand the structure.', '1 mark documents metadata; 1 mark consistency/maintenance. [2]'),
            ('Explain one disadvantage of normalising a database to 3NF.', 'More tables are created, so queries need joins, which can be more complex to write and slower to run.', '1 mark more tables/joins; 1 mark complexity/speed. [2]')],
      ars=[('Normalisation reduces data redundancy.', 'Each item of data is stored in only one table.'),
           ('A phone number should be stored as text.', 'It can begin with zero and is not used in calculations.')],
      falses=['A data dictionary contains all the records of the database.', 'A table in 3NF can contain transitive dependencies.'],
      intros=['{org} in {city} keeps all its data in one large table and staff complain of errors when details change.',
              '{p} is normalising the database of {org} in {city} and writing a data dictionary.'],
      parts=[('Explain what is meant by data redundancy and why it is a problem.', 'The same data stored more than once; wastes space and can become inconsistent if updated in one place only.', '1 mark meaning; 1 mark problem. [2]'),
             ('Describe what must be true for a table to be in third normal form.', 'In 2NF (1NF with no partial dependencies) and no non-key field depends on another non-key field.', '1 mark 2NF condition; 1 mark no transitive dependency. [2]'),
             ('List four items of information that would be stored in the data dictionary for each field.', 'Field name; data type; field size; format; validation rule; description; key status; default value.', '1 mark each, max 4. [4]'),
             ('Explain why a numeric data type is not suitable for a code such as 00731.', 'Leading zeros would be lost; codes are not used for calculations.', '1 mark each. [2]')],
      ev=[('whether {org} should always normalise its database to third normal form', 'removes redundancy and anomalies; consistent data; easier maintenance.', 'more tables and joins; slower queries for reporting; more complex design; small databases may not benefit.', '3NF is usually best for operational databases, though some denormalisation may be acceptable for reporting.')])


@t.add('C3', (2, 3, 4, 5), 'short')
def ch10_norm(r, D):
    un, nf, why = r.choice(NORMS)
    d = ctx(r)
    if D <= 3:
        return Q(f'{d["org"]} in {d["city"]} stores data in the table {un}. Explain why this table is not in third normal form.', cap(why), f'1 mark identifies a dependency not on the whole key; 1 mark explains with fields from the table: {why}. [2]', marks=2)
    m = 5 if D == 4 else 6
    return Q(f'{d["org"]} in {d["city"]} stores data in the table {un}. (a) Explain why the table is not in third normal form. (b) Normalise the data to 3NF, showing the tables, their fields and primary keys.' + (' (c) Identify the foreign keys in your tables.' if D >= 5 else ''),
             f'(a) {why}. (b) {nf}' + ('. (c) Foreign keys are the fields that are primary keys of another table (e.g. IDs in the link/transaction table).' if D >= 5 else ''),
             f'(a) dependency identified [1] (b) 1 mark per correct table with key, max 4: {nf}' + ('; (c) foreign keys [1]' if D >= 5 else '') + f'. [{m}]', marks=m)


@t.add('C3', (1, 2, 3, 4), 'short')
def ch10_dict(r, D):
    if D <= 2:
        f, ty, sz, rule = r.choice(DICT)
        return MCQ(r, f'Which data type is most suitable for the field {f}?', ty, [x for x in ('Text', 'Number (integer)', 'Currency', 'Date/Time', 'Boolean (Yes/No)', 'Real') if x != ty], f'{f}: {ty}.')
    picks = r.sample(DICT, 3 if D == 3 else 4)
    m = 2 * len(picks)
    return Q('Complete a data dictionary entry (data type and a suitable validation rule) for each field: ' + ', '.join(x[0] for x in picks) + '.',
             '; '.join(f'{x[0]}: {x[1]}, {x[3]}' for x in picks), '1 mark data type, 1 mark validation rule per field: ' + '; '.join(f'{x[0]} {x[1]} / {x[3]}' for x in picks) + f'. [{m}]', marks=m)


# =============================================================================== Chapter 11 Spreadsheets, modelling and graphics
from decimal import Decimal, ROUND_HALF_UP  # noqa: E402

COLS = 'ABCDEFGHIJ'
REF = re.compile(r'(\$?)([A-Z])(\$?)(\d+)')


def shift(formula, dc, dr):
    def f(m):
        c, rr = m.group(2), int(m.group(4))
        if not m.group(1):
            k = COLS.index(c) + dc
            if not 0 <= k < len(COLS):
                raise ValueError('column out of range')
            c = COLS[k]
        if not m.group(3):
            rr += dr
        return f'{m.group(1)}{c}{m.group(3)}{rr}'
    return REF.sub(f, formula)


def xround(x, dp):
    return float(Decimal(str(x)).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP))


def sheet(r):
    kind = r.randrange(3)
    if kind == 0:
        hdr = ['Name', 'Region', 'Sales']
        rows = [[n, r.choice(['North', 'South', 'East']), r.randrange(20, 99) * 100] for n in r.sample(FIRSTN, 6)]
        return hdr, rows, 'sales'
    if kind == 1:
        hdr = ['Student', 'Form', 'Mark']
        rows = [[n, r.choice(['12A', '12B']), r.randrange(28, 99)] for n in r.sample(FIRSTN, 6)]
        return hdr, rows, 'marks'
    hdr = ['Item', 'Type', 'Price']
    items = r.sample(['Pen', 'Ruler', 'Folder', 'Stapler', 'Glue', 'Tape', 'Marker', 'Notebook', 'Eraser', 'Scissors'], 6)
    rows = [[n, r.choice(['Desk', 'Paper']), xround(r.randrange(50, 1500) / 100, 2)] for n in items]
    return hdr, rows, 'prices'


def sheet_text(hdr, rows):
    lines = ['   | A | B | C', '1  | ' + ' | '.join(hdr)]
    for i, row in enumerate(rows, 2):
        lines.append(f'{i:<3}| ' + ' | '.join(num(x) if isinstance(x, (int, float)) else str(x) for x in row))
    return code(lines)


t = T(11, 'Spreadsheet formulae and functions: absolute and relative referencing, named ranges, nested IF, VLOOKUP and HLOOKUP', 'spreadsheet formulae and functions', 'absolute and relative referencing', 'named ranges', 'nested if', 'vlookup and hlookup',
      defs=[('relative cell reference', 'A cell reference, such as B2, that changes when the formula is copied to another cell, keeping the same relative position.'),
            ('absolute cell reference', 'A cell reference, such as $B$2, that does not change when the formula is copied.'),
            ('named range', 'A name given to a cell or group of cells, such as VATRate, which can be used in formulae instead of the cell reference and acts like an absolute reference.'),
            ('VLOOKUP', 'A function that searches for a value in the first column of a table and returns the value in the same row from a specified column.'),
            ('HLOOKUP', 'A function that searches for a value in the first row of a table and returns the value in the same column from a specified row.'),
            ('nested IF', 'An IF function placed inside another IF function so that more than two outcomes can be tested.')],
      mcqs=[('Which formula, entered in C2 and copied down to C10, always multiplies by the rate in cell F1?', '=B2*$F$1', ['=B2*F1', '=$B$2*F1', '=B2*F$2'], '$F$1 is absolute, so it does not change when copied.'),
            ('What does a mixed reference such as B$3 keep fixed when copied?', 'The row', ['The column', 'Both the row and the column', 'Neither'], 'The $ is in front of the row number.'),
            ('Why is FALSE used as the last argument of VLOOKUP when looking up a product code?', 'So only an exact match is returned', ['So the table is sorted automatically', 'So the result is rounded', 'So the search is from right to left'], 'FALSE = exact match; TRUE = approximate (sorted) match.')],
      exps=[('Explain why an absolute reference is needed when a formula uses a single tax rate stored in one cell.', 'When the formula is copied, a relative reference would change to point to the wrong (often empty) cell; an absolute reference keeps pointing to the tax-rate cell.', '1 mark relative changes when copied; 1 mark absolute stays fixed on rate cell. [2]'),
            ('Explain two advantages of using named ranges in formulae.', 'Formulae are easier to read and understand (e.g. =Price*VATRate); named ranges act as absolute references so copying is safe; easier to update the range in one place.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain when an approximate-match VLOOKUP is appropriate.', 'When looking up a value within bands, such as a mark in a grade table or a weight in a postage table; the first column must be sorted in ascending order.', '1 mark banded data example; 1 mark sorted ascending. [2]')],
      ars=[('$A$1 does not change when a formula is copied.', 'The dollar signs make both the column and the row absolute.'),
           ('An approximate-match VLOOKUP needs its first column sorted in ascending order.', 'It returns the row with the largest value less than or equal to the lookup value.')],
      falses=['HLOOKUP searches down the first column of a table.', 'A relative reference never changes when copied.'],
      intros=['{p} is building a spreadsheet for {org} in {city} to calculate staff pay and bonuses.',
              '{org} in {city} uses a spreadsheet to calculate invoice totals including tax.'],
      parts=[('Explain the difference between relative and absolute cell references.', 'Relative references change when copied; absolute references ($) stay the same.', '1 mark each. [2]'),
             ('Explain why a named range might be used for the tax rate.', 'Easier to read; acts as an absolute reference; one place to change.', '1 mark per point, max 2. [2]'),
             ('Write a nested IF formula for cell D2 that shows "High" if C2 is at least 1000, "Medium" if it is at least 500 and "Low" otherwise.', '=IF(C2>=1000,"High",IF(C2>=500,"Medium","Low"))', '1 mark first IF; 1 mark nested IF; 1 mark correct outputs/order. [3]'),
             ('Explain the purpose of each argument in =VLOOKUP(A2,$F$2:$H$20,3,FALSE).', 'A2 = value to find; $F$2:$H$20 = table searched (first column F); 3 = third column returned; FALSE = exact match.', '1 mark each argument, max 4. [4]')],
      ev=[('the use of lookup functions instead of nested IF functions in the spreadsheets of {org}', 'lookup tables are easier to read and update; handle many bands; fewer errors.', 'nested IF needs no separate table; lookup errors if the table is unsorted or the range is not absolute; #N/A errors need handling.', 'lookups are better for many categories that may change; nested IF suits two or three fixed outcomes.')])


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def ch11_copy(r, D):
    templates = [('C', 2, '=B2*$F$1'), ('D', 3, '=B3+C3'), ('D', 2, '=SUM(A2:C2)'), ('E', 2, '=C2*$B$1+D2'), ('C', 4, '=B4/B$10'), ('D', 2, '=$B2*C$1'),
                 ('E', 3, '=IF(D3>$H$1,"Yes","No")'), ('C', 2, '=VLOOKUP(A2,$F$2:$G$9,2,FALSE)'), ('F', 2, '=AVERAGE(B2:E2)'), ('D', 5, '=C5-C4')]
    col, row, f = r.choice(templates if D >= 3 else templates[:5])
    if D <= 2:
        dc, dr = 0, r.randrange(1, 6)
    else:
        dc, dr = r.choice([(0, r.randrange(2, 8)), (1, 0), (2, 0), (1, r.randrange(1, 4))])
    if COLS.index(col) + dc >= len(COLS) or any(COLS.index(m.group(2)) + dc >= len(COLS) for m in REF.finditer(f) if not m.group(1)):
        return None
    new = shift(f, dc, dr)
    target = f'{COLS[COLS.index(col) + dc]}{row + dr}'
    wrong = [f]
    for g in (lambda: shift(f.replace('$', ''), dc, dr), lambda: re.sub(r'\$', '', new), lambda: shift(f, dr, dc), lambda: shift(f, dc, dr + 1),
              lambda: shift(f, dc, max(0, dr - 1)), lambda: shift(f, 0, dr + dc)):
        try:
            wrong.append(g())
        except ValueError:
            pass
    stem = f'Cell {col}{row} contains the formula {f}. It is copied to cell {target}. '
    if D <= 2:
        return MCQ(r, stem + f'What formula is in {target}?', new, wrong, f'Relative parts move {dc} column(s) and {dr} row(s); parts with $ stay fixed: {new}.')
    stem += f'State the formula in {target} and explain why each cell reference did or did not change.'
    return Q(stem, new, f'{new} [2]; explanation: references without $ shift by {dc} column(s) and {dr} row(s), $ parts are absolute and stay fixed [1]. [3]', marks=3)


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch11_func(r, D):
    hdr, rows, kind = sheet(r)
    vals = [x[2] for x in rows]
    cats = sorted({x[1] for x in rows})
    c0 = r.choice(cats)
    n = len(rows)
    last = n + 1
    th = sorted(vals)[n // 2]
    fns = [
        (f'=SUM(C2:C{last})', sum(vals)),
        (f'=MAX(C2:C{last})', max(vals)),
        (f'=MIN(C2:C{last})', min(vals)),
        (f'=COUNTIF(C2:C{last},">={th}")', sum(1 for v in vals if v >= th)),
        (f'=COUNTIF(B2:B{last},"{c0}")', sum(1 for x in rows if x[1] == c0)),
        (f'=SUMIF(B2:B{last},"{c0}",C2:C{last})', sum(x[2] for x in rows if x[1] == c0)),
        (f'=ROUND(AVERAGE(C2:C{last}),1)', xround(sum(vals) / n, 1)),
    ]
    i = r.randrange(n)
    v = vals[i]
    a, b = sorted(r.sample(sorted(set(vals)), 2)) if len(set(vals)) >= 2 else (v, v)
    nested = f'=IF(C{i + 2}>={b},"High",IF(C{i + 2}>={a},"Medium","Low"))'
    nres = 'High' if v >= b else ('Medium' if v >= a else 'Low')
    fns.append((nested, nres))
    lk = rows[r.randrange(n)]
    fns.append((f'=VLOOKUP("{lk[0]}",A2:C{last},3,FALSE)', lk[2]))
    fns.append((f'=VLOOKUP("{lk[0]}",A2:C{last},2,FALSE)', lk[1]))
    pool = fns[:3] if D == 1 else (fns[:6] if D == 2 else fns)
    f, res = r.choice(pool)
    shown = num(res) if isinstance(res, (int, float)) else res
    st = sheet_text(hdr, rows)
    if D <= 2:
        alts = [num(x) for x in (sum(vals), max(vals), min(vals), xround(sum(vals) / n, 1), sum(vals) - vals[0], n)] + ['Medium', 'High', 'Low']
        if isinstance(res, str):
            alts = [x for x in ('High', 'Medium', 'Low', '#N/A', 'North', 'South', 'East', 'Desk', 'Paper', '12A', '12B')]
        return MCQ(r, f'A spreadsheet contains:\n{st}\nWhat value is displayed by {f}?', shown, alts, f'{f} → {shown}.')
    picks = r.sample(pool, 2 if D == 3 else 3)
    if (f, res) not in picks:
        picks[0] = (f, res)
    m = len(picks) + (1 if D >= 5 else 0)
    stem = f'A spreadsheet contains:\n{st}\nState the value displayed by each formula: ' + '; '.join(f'({j + 1}) {x[0]}' for j, x in enumerate(picks)) + '.'
    ans = '; '.join(f'({j + 1}) {num(x[1]) if isinstance(x[1], (int, float)) else x[1]}' for j, x in enumerate(picks))
    key = '1 mark each: ' + ans
    if D >= 5:
        stem += f' Explain why =VLOOKUP("Zed",A2:C{last},3,FALSE) would display #N/A.'
        ans += '; "Zed" is not in column A and an exact match is required, so #N/A (not available) is shown.'
        key += '; #N/A because exact match not found in first column [1]'
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ch11_approx(r, D):
    kind = r.choice(['grade', 'postage', 'discount'])
    if kind == 'grade':
        bands = [(0, 'U'), (40, 'E'), (50, 'D'), (60, 'C'), (70, 'B'), (80, 'A')]
        vals = r.sample(range(25, 100), 4 if D <= 3 else 5)
        what = 'Mark'
    elif kind == 'postage':
        bands = [(0, 3.5), (1, 5.25), (2, 7.8), (5, 12.4), (10, 18.95)]
        vals = [r.choice([0.4, 0.9, 1.0, 1.6, 2.0, 3.7, 4.99, 5.0, 8.2, 10.0, 12.5]) for _ in range(4 if D <= 3 else 5)]
        what = 'Weight (kg)'
    else:
        bands = [(0, 0), (100, 0.05), (250, 0.1), (500, 0.15), (1000, 0.2)]
        vals = r.sample([60, 99, 100, 180, 250, 300, 499, 500, 750, 1000, 1400], 4 if D <= 3 else 5)
        what = 'Order value ($)'
    vals = list(dict.fromkeys(vals))

    def look(v):
        out = None
        for k, res in bands:
            if v >= k:
                out = res
        return out
    tbl_lines = code(['   | F | G'] + [f'{i + 2:<3}| {num(k)} | {num(v) if not isinstance(v, str) else v}' for i, (k, v) in enumerate(bands)])
    stem = (f'Cells F2:G{len(bands) + 1} hold this lookup table (column F sorted in ascending order):\n{tbl_lines}\n'
            f'Column B holds {what}. Cell C2 contains =VLOOKUP(B2,$F$2:$G${len(bands) + 1},2,TRUE) and is copied down. State the result for each value in column B: ' + ', '.join(num(v) for v in vals) + '.')
    res = [look(v) for v in vals]
    ans = '; '.join(f'{num(v)} → {num(x) if not isinstance(x, str) else x}' for v, x in zip(vals, res))
    m = len(vals)
    key = '1 mark each: ' + ans + ' (approximate match returns the largest value in F that is ≤ the lookup value)'
    if D >= 4:
        stem += ' Explain why the cell references to the lookup table are absolute.'
        key += '; absolute so the table range does not move when the formula is copied down [1]'
        ans += '; the table range must stay fixed when copied.'
        m += 1
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (2, 3, 4), 'numerical')
def ch11_hlookup(r, D):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    r1 = [r.randrange(10, 60) for _ in days]
    r2 = [r.randrange(100, 900) for _ in days]
    t_ = code(['   | B | C | D | E | F', '1  | ' + ' | '.join(days), '2  | ' + ' | '.join(map(str, r1)), '3  | ' + ' | '.join(map(str, r2))])
    picks = r.sample(range(5), 2 if D <= 3 else 3)
    qs = []
    for j in picks:
        rw = r.choice([2, 3])
        qs.append((f'=HLOOKUP("{days[j]}",B1:F3,{rw},FALSE)', (r1 if rw == 2 else r2)[j]))
    stem = f'Row 1 holds days, row 2 the number of orders and row 3 the takings ($):\n{t_}\nState the value returned by each formula: ' + '; '.join(f'({i + 1}) {q}' for i, (q, _) in enumerate(qs)) + '.'
    ans = '; '.join(f'({i + 1}) {v}' for i, (_, v) in enumerate(qs))
    return Q(stem, ans, '1 mark each: ' + ans + f'. [{len(qs)}]', marks=len(qs), typ='numerical')


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def ch11_build(r, D):
    rate = r.choice([5, 8, 10, 12.5, 15, 20])
    d = ctx(r)
    bonus = r.choice([500, 1000, 2000])
    stem = (f'{d["org"]} in {d["city"]} uses a spreadsheet for invoices. Column B holds the quantity and column C the unit price for rows 2 to 20. Cell H1 holds the tax rate ({num(rate)}%). '
            f'(a) Write a formula for D2 to calculate the net cost (quantity × unit price). (b) Write a formula for E2, to be copied down, that calculates the tax using the rate in H1. '
            f'(c) Write a formula for F2 that shows "Check" if the net cost is more than {bonus} and is otherwise blank. (d) Write a formula for D21 to find the total net cost.')
    ans = f'(a) =B2*C2 (b) =D2*$H$1/100 (c) =IF(D2>{bonus},"Check","") (d) =SUM(D2:D20)'
    key = f'(a) =B2*C2 [1] (b) =D2*$H$1/100 (or =D2*$H$1 if H1 is formatted as a percentage) — 1 mark correct calculation, 1 mark absolute H1 [2] (c) =IF(D2>{bonus},"Check","") — 1 mark condition, 1 mark both outputs [2] (d) =SUM(D2:D20) [1]. [6]'
    m = 6
    if D >= 4:
        stem += ' (e) Explain how a named range could make the formula in (b) easier to understand.'
        ans += ' (e) Name H1 as TaxRate so the formula becomes =D2*TaxRate/100, which is self-explanatory and stays fixed when copied.'
        key = key[:-4] + ' (e) name H1 e.g. TaxRate; formula =D2*TaxRate/100 readable and absolute [2]. [8]'
        m = 8
    return Q(stem, ans, key, marks=m, typ='multi_step')


@t.add('C2', (2, 3, 4), 'explain')
def ch11_err(r, D):
    cases = [
        ('=B2*F1', 'C2', 'C3:C10', 'show 0 or wrong values', 'F1 is a relative reference, so in C3 it becomes F2 (an empty cell)', '=B2*$F$1'),
        ('=SUM(B2:B9)', 'B10', 'only B10', 'leave out the value in B10', 'the range should include every data row; row 10 holds data so the total should be in B11 with =SUM(B2:B10)', '=SUM(B2:B10) placed in B11'),
        ('=VLOOKUP(A2,F2:G9,2,FALSE)', 'C2', 'C3:C10', 'show #N/A in some rows', 'the table range is relative, so it moves down (F3:G10, F4:G11 …) and stops including the first rows of the table', '=VLOOKUP(A2,$F$2:$G$9,2,FALSE)'),
        ('=IF(B2>50,"Pass","Fail")', 'C2', 'C3:C10', 'show Fail for a mark of exactly 50, although 50 is a pass', 'the condition uses > instead of >=', '=IF(B2>=50,"Pass","Fail")'),
        ('=AVERAGE(B2:B10)/9', 'B11', 'only B11', 'give a far too small answer', 'AVERAGE already divides by the number of values, so dividing again by 9 is wrong', '=AVERAGE(B2:B10)'),
    ]
    f, cell, cp, symptom, why, fix = r.choice(cases)
    d = ctx(r)
    stem = f'{d["p"]} at {d["org"]} entered {f} in cell {cell}' + (f' and copied it to {cp}' if cp != f'only {cell}' else '') + f'. The results {symptom}. Explain the error and give a corrected formula.'
    return {'stem': stem, 'answer': f'{cap(why)} Correct: {fix}.', 'key': f'1 mark identifies cause; 1 mark explanation ({why}); 1 mark corrected formula {fix}. [3]', 'marks': 3, 'type': 'explain'}


t = T(11, 'Modelling and what-if analysis: goal seek, scenarios and simulations', 'modelling and what-if analysis', 'goal seek, scenarios and simulations',
      defs=[('computer model', 'A representation of a real system, built with formulae and rules (often in a spreadsheet), used to predict what will happen when inputs change.'),
            ('what-if analysis', 'Changing one or more input values in a model to see the effect on the results.'),
            ('goal seek', 'A spreadsheet tool that finds the input value needed to make a formula produce a chosen target result.'),
            ('scenario', 'A saved set of input values in a model (e.g. best case, worst case) that can be switched between to compare outcomes.'),
            ('simulation', 'Using a model to imitate the behaviour of a real system over time, often to test situations that would be dangerous, expensive or impossible to try in reality.')],
      mcqs=[('Which tool would find the selling price needed to make exactly $5000 profit?', 'Goal seek', ['Conditional formatting', 'Sorting', 'Mail merge'], 'Goal seek works backwards from a target result.'),
            ('Why are flight simulators used to train pilots?', 'Dangerous situations can be practised safely and cheaply', ['They are more exciting than real planes', 'They use no software', 'They replace all real flying'], 'Simulation lets trainees experience emergencies without risk.'),
            ('What is a limitation of any computer model?', 'Its results are only as reliable as its rules and input data', ['It can never be changed', 'It always predicts the future exactly', 'It cannot use formulae'], 'Models simplify reality.')],
      exps=[('Explain why a business uses a spreadsheet model to answer what-if questions.', 'It can change inputs such as price or costs and see the effect on profit instantly, without the risk and cost of trying it in reality, helping it plan and make decisions.', '1 mark change inputs/see effect; 1 mark no real-world risk/cost; 1 mark supports decisions. [3]'),
            ('Explain the difference between goal seek and what-if analysis.', 'What-if analysis changes inputs to see the effect on outputs; goal seek sets a target output and works out the input needed to reach it.', '1 mark what-if forward; 1 mark goal seek backward. [2]'),
            ('Explain two limitations of using a computer model to predict weather.', 'The model is a simplification, so it may not include all factors; input data may be inaccurate or incomplete; small errors grow over time so long-range forecasts are unreliable.', '2 × (1 mark point, 1 mark explanation). [4]')],
      ars=[('Goal seek finds the input needed to reach a target result.', 'It repeatedly changes the input cell until the formula gives the target.'),
           ('Simulations are used to train pilots.', 'Emergencies can be practised without risk to life.')],
      falses=['A model always gives exactly correct predictions.', 'Goal seek changes the formula itself.'],
      intros=['{org} in {city} has built a spreadsheet model to plan the price of a new product.',
              '{p} uses a spreadsheet model at {org} in {city} to plan staffing and costs for an event.'],
      parts=[('Explain what is meant by a computer model.', 'A representation of a real situation using formulae and rules to predict outcomes.', '1 mark representation; 1 mark formulae/prediction. [2]'),
             ('Describe how goal seek could be used in this model.', 'Set the profit cell to a target value by changing an input such as price or units; the spreadsheet calculates the required input.', '1 mark target cell/value; 1 mark changing input. [2]'),
             ('Explain the advantage of using scenarios.', 'Several sets of inputs (best, expected, worst case) can be stored and compared quickly.', '1 mark stored sets; 1 mark comparison. [2]'),
             ('Explain one limitation of the model.', 'It relies on assumptions and estimates, e.g. demand, which may be wrong.', '1 mark point; 1 mark explanation. [2]')],
      ev=[('the use of spreadsheet models by {org} to make financial decisions', 'quick what-if testing; no real-world risk; goal seek and scenarios support planning.', 'models depend on assumptions and accurate data; errors in formulae; may give false confidence.', 'models are valuable decision aids if assumptions are tested and results are used with judgement.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch11_goal(r, D):
    fixed = r.choice([2000, 3000, 4500, 6000, 8000, 12000])
    var = r.choice([4, 5, 6, 7.5, 8, 12])
    units = r.choice([400, 500, 800, 1000, 1200, 1500])
    price = var + r.choice([6, 8, 10, 12, 15])
    profit = units * (price - var) - fixed
    d = ctx(r)
    model = (f'{d["org"]} in {d["city"]} has a spreadsheet model: B1 Units sold = {units}; B2 Selling price = ${num(price)}; B3 Variable cost per unit = ${num(var)}; B4 Fixed costs = ${fixed:,}; '
             f'B5 contains =B1*(B2-B3)-B4 (profit).')
    if D == 1:
        return MCQ(r, f'{model} What value is displayed in B5?', money(profit, dp=0), [money(units * price - fixed, dp=0), money(units * (price - var), dp=0), money(profit + fixed * 2, dp=0)], f'{units} × ({num(price)} − {num(var)}) − {fixed:,} = {money(profit, dp=0)}.')
    if D == 2:
        nu = units + r.choice([100, 200, 300])
        np_ = nu * (price - var) - fixed
        return Q(f'{model} (a) Calculate the profit shown in B5. (b) What-if: calculate the profit if units sold rise to {nu}.', f'(a) {money(profit, dp=0)} (b) {money(np_, dp=0)}',
                 f'(a) {units} × ({num(price)} − {num(var)}) − {fixed:,} = {money(profit, dp=0)} [1] (b) {nu} × {num(price - var)} − {fixed:,} = {money(np_, dp=0)} [1]. [2]', marks=2, typ='numerical')
    target = r.choice([5000, 8000, 10000, 15000])
    kind = r.choice(['price', 'units']) if D >= 4 else 'price'
    if kind == 'price':
        p = (target + fixed) / units + var
        stem = f'{model} Goal seek is used to set B5 to {target:,} by changing B2. Calculate the selling price that goal seek will find.'
        key = f'{target:,} = {units} × (P − {num(var)}) − {fixed:,} [1]; P − {num(var)} = ({target:,} + {fixed:,}) / {units} = {num(round((target + fixed) / units, 4))} [1]; P = ${num(round(p, 2))} [1]'
        ans = f'${num(round(p, 2))}'
    else:
        u = (target + fixed) / (price - var)
        stem = f'{model} Goal seek is used to set B5 to {target:,} by changing B1. Calculate the number of units needed and explain why the answer should be rounded up.'
        key = f'units = ({target:,} + {fixed:,}) / ({num(price)} − {num(var)}) = {num(round(u, 2))} [2]; round up to {math.ceil(u):,} because fewer units would not reach the target / units are whole numbers [1]'
        ans = f'{num(round(u, 2))}, so {math.ceil(u):,} units'
    m = 3
    if D >= 5:
        be = fixed / (price - var)
        stem += ' Also calculate the break-even number of units at the original price.'
        key += f'; break-even = {fixed:,} / {num(price - var)} = {num(round(be, 2))} → {math.ceil(be):,} units [1]'
        ans += f'; break-even {math.ceil(be):,} units'
        m = 4
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


CHARTS = [('show the percentage of a company\'s budget spent on each department', 'pie chart', 'it shows parts of a whole as proportions'),
          ('show how the monthly temperature in {city} changed over a year', 'line graph', 'it shows a trend in continuous data over time'),
          ('compare the number of students choosing each of six subjects', 'bar (column) chart', 'it compares separate categories'),
          ('show whether there is a relationship between hours of revision and exam mark', 'scatter graph', 'it shows correlation between two numeric variables'),
          ('compare sales of three products in each of four quarters', 'clustered bar (column) chart', 'it compares several series across categories'),
          ('show the share of votes each party received in an election', 'pie chart', 'it shows proportions of a total'),
          ('show the share price of a company each day for a month', 'line graph', 'it shows change over time')]
CTYPES = ['Pie chart', 'Line graph', 'Bar (column) chart', 'Scatter graph']

t = T(11, 'Charts and graphs: choosing appropriate types and formatting for an audience', 'charts and graphs', 'choosing appropriate types',
      defs=[('pie chart', 'A circular chart divided into sectors, each showing a category\'s proportion of the whole.'),
            ('line graph', 'A graph that joins data points with lines, used to show trends or changes over time.'),
            ('scatter graph', 'A graph that plots pairs of numeric values as points to show whether there is a correlation between two variables.'),
            ('chart legend', 'A key that explains what each colour or symbol in a chart represents.')],
      mcqs=[('Which feature should every chart include so the audience understands it?', 'A title and axis labels (or a legend)', ['3D effects', 'As many colours as possible', 'Animated sectors'], 'Labels make the chart meaningful.'),
            ('Why is a pie chart not suitable for showing monthly sales over two years?', 'Pie charts show parts of a whole, not changes over time', ['Pie charts cannot show numbers', 'Pie charts need negative values', 'Pie charts only work with two categories'], 'A line graph suits trends over time.')],
      exps=[('Explain why the vertical axis of a bar chart should normally start at zero.', 'If it starts at a higher value, small differences look much bigger, which can mislead the audience.', '1 mark exaggerates differences; 1 mark misleading. [2]'),
            ('Explain two ways a chart can be formatted to suit a presentation to a large audience.', 'Large clear fonts for title and labels; high-contrast colours; few categories; data labels so values can be read from a distance; no clutter.', '2 × (1 mark point, 1 mark explanation). [4]')],
      ars=[('A scatter graph is suitable for showing correlation.', 'It plots pairs of values for two numeric variables.'),
           ('Starting an axis above zero can mislead.', 'Differences between bars appear larger than they are.')],
      falses=['Pie charts are best for showing trends over time.', 'Charts do not need titles.'],
      intros=['{p} is preparing charts for a presentation to the directors of {org} in {city}.',
              '{org} in {city} publishes a report with charts of its sales and customer data.'],
      parts=[('Explain why a title and axis labels are needed.', 'They tell the audience what the chart shows and what the values and units are.', '1 mark each. [2]'),
             ('Explain when a legend is needed.', 'When there is more than one data series or category shown by colours/symbols.', '1 mark multiple series; 1 mark explains colours. [2]'),
             ('Explain why a line graph is suitable for monthly sales figures.', 'It shows the trend over time clearly; points are joined in time order.', '1 mark each. [2]')],
      ev=[('the use of charts rather than tables to present data in the reports of {org}', 'trends and comparisons are seen quickly; engaging; suitable for non-specialists.', 'exact values harder to read; charts can mislead with poor scales; tables are better for detail.', 'charts suit summaries and presentations; tables suit detailed analysis — often both are used.')])


@t.add('C3', (1, 2, 3, 4), 'short')
def ch11_chart(r, D):
    task, typ, why = r.choice(CHARTS)
    d = ctx(r)
    task = fill(task, d)
    if D <= 2:
        a = 'Pie chart' if typ.startswith('pie') else ('Line graph' if typ.startswith('line') else ('Scatter graph' if typ.startswith('scatter') else 'Bar (column) chart'))
        return MCQ(r, f'Which type of chart is most appropriate to {task}?', a, [x for x in CTYPES if x != a] + ['Radar chart'], f'{typ}: {why}.')
    return Q(f'{d["p"]} at {d["org"]} wants to {task}. Recommend a type of chart, justify your choice and describe two formatting features that should be used.',
             f'{cap(typ)}: {why}. Formatting: clear title; axis labels/legend; data labels; suitable colours.', f'1 mark chart type; 1 mark justification ({why}); 2 marks formatting features. [4]', marks=4)


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch11_pie(r, D):
    cats = r.sample(['Car', 'Bus', 'Walk', 'Cycle', 'Train', 'Taxi'], 4 if D <= 3 else 5)
    tot = r.choice([120, 180, 240, 360, 400, 600, 720])
    # generate counts that sum to tot
    cuts = sorted(r.sample(range(1, tot), len(cats) - 1))
    cnt = [b - a for a, b in zip([0] + cuts, cuts + [tot])]
    if min(cnt) < 5:
        return None
    ang = [c / tot * 360 for c in cnt]
    i = r.randrange(len(cats))
    d = ctx(r)
    data = ', '.join(f'{c} {k}' for k, c in zip(cats, cnt))
    if D == 1:
        return MCQ(r, f'In a survey of {tot} people in {d["city"]}: {data}. What angle should the "{cats[i]}" sector have in a pie chart (to the nearest degree)?', f'{round(ang[i])}°',
                   [f'{round(cnt[i] / tot * 100)}°', f'{round(ang[i]) + 10}°', f'{cnt[i]}°', f'{round(ang[i] / 2)}°'], f'{cnt[i]} / {tot} × 360 = {ang[i]:.1f}°.')
    stem = f'{d["org"]} surveyed {tot} people in {d["city"]} about how they travel to work: {data}. Calculate the angle of each sector of a pie chart, to the nearest degree.'
    ans = '; '.join(f'{k} {round(a)}°' for k, a in zip(cats, ang))
    m = len(cats)
    key = '1 mark each: ' + '; '.join(f'{k} {c}/{tot} × 360 = {a:.1f}°' for k, c, a in zip(cats, cnt, ang))
    if D >= 4:
        stem += f' Also give the percentage for {cats[i]} and explain why a pie chart is suitable for this data.'
        ans += f'; {cats[i]} {num(round(cnt[i] / tot * 100, 1))}%; the data are parts of a whole.'
        key += f'; {cats[i]} = {num(round(cnt[i] / tot * 100, 1))}% [1]; parts of a whole/proportions [1]'
        m += 2
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


t = T(11, 'Sound and video editing: trimming, transitions, compression and file formats', 'sound and video editing', 'trimming, transitions, compression and file formats',
      defs=[('sample rate', 'The number of times per second that the amplitude of a sound wave is measured when it is recorded digitally, measured in hertz (Hz).'),
            ('bit depth (sample resolution)', 'The number of bits used to store each sound sample; a greater bit depth records the amplitude more precisely.'),
            ('lossy compression', 'Compression that permanently removes some data, such as sounds people cannot hear, to reduce file size (e.g. MP3, MP4).'),
            ('lossless compression', 'Compression that reduces file size without losing any data, so the original can be reconstructed exactly (e.g. FLAC, PNG, ZIP).'),
            ('trimming', 'Removing unwanted parts from the start or end of a sound or video clip.'),
            ('transition', 'An effect used when one video clip changes to the next, such as a fade, dissolve or wipe.')],
      mcqs=[('Which file format uses lossy compression for audio?', 'MP3', ['WAV', 'FLAC', 'TXT'], 'MP3 removes sounds the human ear is unlikely to notice.'),
            ('What happens to the file size of a recording if the sample rate is doubled and everything else stays the same?', 'It doubles', ['It halves', 'It stays the same', 'It quadruples'], 'Twice as many samples are stored per second.'),
            ('Why might a video for a website be compressed?', 'To reduce file size so it downloads or streams faster', ['To increase its resolution', 'To add subtitles', 'To make it lossless'], 'Smaller files use less bandwidth.')],
      exps=[('Explain why lossy compression is suitable for music streamed to mobile phones.', 'It greatly reduces file size so music streams quickly with less data, and the lost data is mostly sound that listeners cannot easily hear.', '1 mark smaller files/less data; 1 mark quality loss barely noticeable. [2]'),
            ('Explain why a sound engineer records in WAV format before editing.', 'WAV is uncompressed, so no quality is lost during editing; repeated lossy saves would degrade the audio.', '1 mark uncompressed/full quality; 1 mark avoids repeated loss. [2]'),
            ('Explain how increasing the bit depth affects the quality and size of a sound file.', 'More bits per sample allow more amplitude levels, so the recording is more accurate (better quality), but each sample needs more storage so the file is larger.', '1 mark quality; 1 mark size. [2]')],
      ars=[('Increasing the sample rate improves sound quality.', 'The sound wave is measured more often, so it is represented more accurately.'),
           ('Lossless compression allows the original file to be restored exactly.', 'No data is permanently removed.')],
      falses=['MP3 is a lossless format.', 'Trimming adds extra frames to a video.'],
      intros=['{p} is editing a promotional video and soundtrack for {org} in {city}.',
              '{org} in {city} is producing podcasts and short videos for its website.'],
      parts=[('Explain the purpose of trimming a clip.', 'Removes unwanted content at the start/end so the clip is shorter and focused.', '1 mark removes parts; 1 mark benefit. [2]'),
             ('Describe two transitions that could be used between video clips.', 'Fade; dissolve/cross-fade; wipe; slide; zoom.', '1 mark each, max 2. [2]'),
             ('Explain why the final video should be compressed before uploading.', 'Smaller file uploads/streams faster and uses less storage and bandwidth.', '1 mark smaller; 1 mark faster/less bandwidth. [2]'),
             ('Explain the difference between lossy and lossless compression.', 'Lossy permanently removes data (smaller files, lower quality); lossless removes no data (original restored exactly).', '1 mark each. [2]')],
      ev=[('whether {org} should publish its videos in a highly compressed lossy format', 'small files stream quickly on mobile; less storage; reaches users with slow connections.', 'loss of quality, visible artefacts; cannot recover original; brand may look unprofessional.', 'moderate compression with an adaptive-quality streaming option is usually best; keep uncompressed masters.')])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ch11_sound(r, D):
    sr = r.choice([22050, 44100, 48000])
    bd = r.choice([8, 16, 24])
    ch = r.choice([1, 2])
    secs = r.choice([30, 45, 60, 90, 120, 180, 240])
    byt = sr * bd * ch * secs / 8
    mb = byt / 10 ** 6
    chn = 'mono' if ch == 1 else 'stereo'
    stem = f'A sound clip of {secs} seconds is recorded in {chn} with a sample rate of {sr:,} Hz and a bit depth of {bd} bits. Calculate the file size in megabytes (1 MB = 1 000 000 bytes).'
    key = f'{sr:,} × {bd} × {ch} × {secs} = {sr * bd * ch * secs:,} bits [1]; ÷ 8 = {byt:,.0f} bytes [1]; = {num(round(mb, 2))} MB [1]'
    if D == 1:
        return MCQ(r, stem.replace('Calculate the file size', 'What is the file size'), f'{num(round(mb, 2))} MB', [f'{num(round(mb * 8, 2))} MB', f'{num(round(mb / ch / 2, 2))} MB' if ch == 2 else f'{num(round(mb * 2, 2))} MB', f'{num(round(mb / 60, 2))} MB'], key)
    m = 3
    ans = f'{num(round(mb, 2))} MB'
    if D >= 3:
        trim = r.choice([5, 10, 15])
        ratio = r.choice([4, 8, 10, 11])
        nb = sr * bd * ch * (secs - trim) / 8 / ratio / 10 ** 6
        stem += f' The clip is then trimmed by {trim} seconds and compressed to MP3 with a compression ratio of {ratio}:1. Calculate the new file size.'
        key += f'; new length {secs - trim} s → {num(round(sr * bd * ch * (secs - trim) / 8 / 10 ** 6, 2))} MB [1]; ÷ {ratio} = {num(round(nb, 2))} MB [1]'
        ans += f'; after trimming and compression {num(round(nb, 2))} MB'
        m = 5
    if D >= 5:
        stem += ' Explain one disadvantage of the MP3 version.'
        key += '; lossy: some audio data permanently lost / lower quality [1]'
        ans += '; MP3 is lossy so some quality is permanently lost.'
        m = 6
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ch11_video(r, D):
    w, h = r.choice([(640, 480), (1280, 720), (1920, 1080)])
    cd = r.choice([24, 24, 16])
    fps = r.choice([24, 25, 30])
    secs = r.choice([5, 10, 20, 30, 60])
    frame = w * h * cd / 8
    tot = frame * fps * secs
    stem = (f'An uncompressed video clip is {w} × {h} pixels with a colour depth of {cd} bits, at {fps} frames per second, and lasts {secs} seconds. '
            f'Calculate (a) the size of one frame in MB and (b) the size of the whole clip in GB (1 MB = 10⁶ bytes, 1 GB = 10⁹ bytes).')
    key = f'(a) {w} × {h} × {cd} ÷ 8 = {frame:,.0f} bytes = {num(round(frame / 1e6, 3))} MB [1] (b) × {fps} × {secs} = {tot:,.0f} bytes [1] = {num(round(tot / 1e9, 3))} GB [1]'
    ans = f'(a) {num(round(frame / 1e6, 3))} MB (b) {num(round(tot / 1e9, 3))} GB'
    m = 3
    if D >= 4:
        sp = r.choice([10, 20, 50])
        stem += f' (c) Explain why this clip must be compressed before it is streamed over a {sp} Mbps connection.'
        rate = frame * fps * 8 / 1e6
        key += f' (c) it needs {num(round(rate))} Mbps, far more than {sp} Mbps, so compression is needed for smooth streaming [2]'
        ans += f' (c) Uncompressed it needs about {num(round(rate))} Mbps, more than {sp} Mbps, so it would buffer.'
        m = 5
    return Q(stem, ans, key + f'. [{m}]', marks=m, typ='numerical')
finish(CHAPTERS)
