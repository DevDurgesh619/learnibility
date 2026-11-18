"""Cambridge International AS Level Economics 9708 (AS content, grade 11).

Syllabus topics 1-6: basic economic ideas and resource allocation, the price system and the microeconomy,
government microeconomic intervention, the macroeconomy, government macroeconomic intervention and
international economic issues (CUP coursebook chapters 1-29). Items mirror Paper 1 (30 multiple-choice
questions, 1 mark each) and Paper 2 (data response and structured essays: part (a) 8 marks, part (b) 12 marks).
Contexts use fictional countries and firms with realistic, generic figures.
"""
import re

from ._lib import topic, mcq, compose, person, city
from .g12_economics import (fill, money, num, pct, dis_num, cq, table, add_many, art,  # noqa: F401
                            COUNTRIES, FIRMS, GOODS, INDUSTRIES)

PROFILE = {'mark_scale': {'long': (2, 2), 'case': (1.5, 1.5)}, 'wordy': True}
CHAPTERS = {}


# ----------------------------------------------------------------------------- helpers
MGOODS = ['bicycles', 'smartphones', 'running shoes', 'laptops', 'furniture', 'cement', 'chocolate bars', 'electric scooters', 'washing machines',
          'textiles', 'car tyres', 'solar panels', 'bottled water', 'televisions', 'paper', 'steel pipes']


def ctx(r):
    c1, c2, c3 = r.sample(COUNTRIES, 3)
    f1, f2 = r.sample(FIRMS, 2)
    g1, g2 = r.sample(GOODS, 2)
    m1, m2 = r.sample(MGOODS, 2)
    i1, i2 = r.sample(INDUSTRIES, 2)
    return {'country': c1, 'country2': c2, 'country3': c3, 'firm': f1, 'firm2': f2, 'good': g1, 'good2': g2, 'mgood': m1, 'mgood2': m2,
            'ind': i1, 'ind2': i2, 'a_ind': art(i1), 'city': city(r), 'person': person(r), 'cur': r.choice(CURS)}


def items(t, C, D, entries, typ=None, name='items'):
    """One entry per call, {placeholders} filled from a random context; with distractors the item is an MCQ."""
    def fn(r, D_):
        e = r.choice(entries)
        d = ctx(r)
        stem, ans, key = fill(e[0], d), fill(e[1], d), fill(e[2], d)
        if len(e) > 3 and e[3]:
            opts, a = mcq(r, ans, [fill(x, d) for x in e[3]])
            return {'stem': stem, 'options': opts, 'answer': a, 'key': key}
        return {'stem': stem, 'answer': ans, 'key': key}
    fn.__name__ = name
    t.add(C, D, typ)(fn)
    return fn


def T(name, *extra):
    """Topic whose first keyword is the exact subtopic name."""
    return topic(name, name, *extra)


def mc(t, entries, D=(1, 2, 3)):
    """Paper 1 style recall items (stem, answer, key, distractors). Stems are written as questions so the
    automatic two-part pairing still reads well without options."""
    t.fixed('C1', D, entries)


def ex(t, entries, D=(1, 2, 3, 4)):
    t.fixed('C2', D, entries, 'explain')


def errs(t, pairs, D=(1, 2, 3, 4)):
    """Spot-the-error items: (incorrect claim, correction), both may use {placeholders}."""
    leads = ['{p} wrote in a homework answer: ', 'A student, {p}, claims: ', 'During a class discussion {p} said: ',
             'In a revision note {p} wrote: ', '{p} makes the following statement: ']
    tails = ['Identify the error in this statement and correct it.', 'Explain why this statement is incorrect.',
             'Identify what is wrong with this reasoning and give the correct explanation.', 'Explain what is wrong with this claim.']

    def fn(r, D_):
        w, c = r.choice(pairs)
        d = ctx(r)
        lead = r.choice(leads).replace('{p}', person(r))
        c2 = fill(c, d)
        return {'stem': f'{lead}‘{fill(w, d)}’ {r.choice(tails)}', 'answer': c2,
                'key': f'1 mark: identifies the error; 1 mark: correct explanation – {c2} [2]', 'type': 'explain', 'marks': 2}
    fn.__name__ = 'err'
    t.add('C2', D, 'explain')(fn)
    return fn


def classify(t, cases, labels, q, multi, D=(1, 2, 3, 4, 5), C='C3', extra=(), name='classify'):
    """Scenario classification. cases: (scenario with {placeholders}, label, reason).
    D1-2: MCQ on one scenario; D3: identify and explain; D4-5: classify two or three scenarios with reasons."""
    def fn(r, D_):
        d = ctx(r)
        if D_ >= 4 and len(cases) >= 3:
            n = 2 if D_ == 4 else 3
            picks = r.sample(cases, n)
            for _ in range(6):
                if len({c[1] for c in picks}) == n or len({c[1] for c in cases}) < n:
                    break
                picks = r.sample(cases, n)
            nums = ['(i)', '(ii)', '(iii)']
            stem = fill(multi, d) + ' ' + ' '.join(f'{nums[i]} {fill(s, d)}' for i, (s, _, _) in enumerate(picks))
            ans = ' '.join(f'{nums[i]} {lab}' for i, (_, lab, _) in enumerate(picks))
            key = ' '.join(f'{nums[i]} {lab} – {fill(why, d)} [2]' for i, (_, lab, why) in enumerate(picks))
            return {'stem': stem, 'answer': ans, 'key': key + f' Total [{2 * n}]', 'marks': 2 * n, 'type': 'explain'}
        s, lab, why = r.choice(cases)
        s = fill(s, d)
        if D_ <= 2:
            opts, a = mcq(r, lab, [x for x in list(labels) + list(extra) if x != lab])
            return {'stem': f'{s} {fill(q, d)}', 'options': opts, 'answer': a, 'key': f'{lab}: {fill(why, d)}'}
        return {'stem': f'{s} {fill(q, d)} Explain your answer.', 'answer': f'{lab}: {fill(why, d)}',
                'key': f'1 mark: {lab}; 1 mark: explanation – {fill(why, d)} [2]', 'marks': 2, 'type': 'explain'}
    fn.__name__ = name
    t.add(C, D, 'explain')(fn)
    return fn


B_FORMS = ['Assess whether {p}.', 'Evaluate whether {p}.', 'Discuss whether {p}.', 'To what extent do you agree that {p}?',
           '‘{P}.’ Evaluate this view.', 'Assess the extent to which {p}.', '‘{P}.’ Discuss this statement.', 'Consider whether {p}.']
A_KEY = ('Indicative content: {pts} Level 3 (6–8): accurate knowledge with a clear, developed analytical chain and, where relevant, an accurate, '
         'labelled diagram that is used in the answer; Level 2 (3–5): some correct explanation but undeveloped or partly inaccurate; '
         'Level 1 (1–2): limited knowledge, mostly assertion [8]')
B_KEY = ('Analysis (AO1/AO2, up to 8): {fr} Evaluation (AO3, up to 4): {ag} Top marks need balanced analysis of both sides and a justified '
         'conclusion that answers the question set, explaining what the outcome depends on [12]')


DEFAULT_SCENES = ['Newspapers in {country} have recently reported a lively debate among economists on this issue.',
                  '{person}, an economics student in {city}, is preparing for a class debate on this topic.',
                  'The government of {country} has asked its economic advisers for a report on this issue.',
                  'A policy institute in {city} has published a report on this issue for the government of {country}.']


def essay(t, prompts, scenes=(), D=(2, 3, 4, 5)):
    """Paper 2 Section B structured essay. prompts: (part (a) task, (a) points, (b) claim, (b) case for, (b) case against).
    D2-3: part (a) only [8]; D4: part (b) only [12] (sometimes both); D5: both parts [20]."""
    pool = list(scenes) or DEFAULT_SCENES

    def fn(r, D_):
        a_task, a_pts, claim, fr, ag = r.choice(prompts)
        d = ctx(r)
        scene = fill(r.choice(pool), d) + ' ' if r.random() < 0.85 else ''
        form = r.choice(B_FORMS)
        claim = fill(claim, d)
        b = form.replace('{p}', claim).replace('{P}', claim[0].upper() + claim[1:])
        a_task, a_pts, fr, ag = fill(a_task, d), fill(a_pts, d), fill(fr, d), fill(ag, d)
        ka, kb = A_KEY.format(pts=a_pts), B_KEY.format(fr=fr, ag=ag)
        both = D_ >= 5 or (D_ == 4 and r.random() < 0.35)
        if both:
            stem, ans, key, m = (f'{scene}(a) {a_task} (b) {b}', f'(a) {a_pts} (b) For: {fr} Against: {ag} Conclusion: a reasoned judgement on when the claim holds.',
                                 f'(a) {ka} (b) {kb}', 20)
        elif D_ >= 4:
            stem, ans, key, m = (scene + b, f'For: {fr} Against: {ag} Conclusion: a reasoned judgement on when the claim holds.', kb, 12)
        else:
            stem, ans, key, m = (scene + a_task, a_pts, ka, 8)
        return {'stem': stem, 'answer': ans, 'key': key, 'type': 'long', 'marks': m, 'minutes': 2 * m if m < 20 else 40}
    fn.__name__ = 'essay'
    t.add('C4', D, 'long')(fn)
    return fn


_SEG = re.compile(r'(?:^|(?<=\s))\(([a-e])\) ')


def _segments(text):
    """Split '(a) ... (b) ...' into {letter: text}."""
    idx = [(m.group(1), m.start(), m.end()) for m in _SEG.finditer(text)]
    out = {}
    for i, (l, s0, e0) in enumerate(idx):
        out[l] = text[e0: idx[i + 1][1] if i + 1 < len(idx) else len(text)].strip()
    return out


def _fill_keys(q):
    """Where a part's marking key is only '[n]', spell out the creditworthy points from the answer."""
    if not q:
        return q
    if re.fullmatch(r'\[\d+\]', q['key'].strip()):
        q['key'] = f'Credit: {q["answer"]} {q["key"].strip()}'
        return q
    ans = _segments(q['answer'])
    q['key'] = re.sub(r'\(([a-e])\) \[(\d+)\]', lambda m: f'({m.group(1)}) Credit: {ans.get(m.group(1), "valid points")} [{m.group(2)}]', q['key'])
    return q


def case(topics, fn, D=(2, 3, 4, 5)):
    """Register a Paper 2 Section A style data-response compose template on every topic of a chapter."""
    def g(r, D_):
        return _fill_keys(fn(r, D_))
    g.__name__ = fn.__name__
    add_many(topics, 'C4', D, 'case', g)


def r1(x):
    return num(x, 1)


def r2(x):
    return num(x, 2)


def chg(a, b):
    """Percentage change from a to b."""
    return 100 * (b - a) / a


def sgn(x, dp=1):
    return ('+' if x > 0 else '') + num(x, dp)


# ============================================================================ 1 Scarcity, choice and opportunity cost
t1_1 = T('The fundamental economic problem: scarcity of resources and unlimited wants', 'scarcity', 'unlimited wants', 'economic problem')
mc(t1_1, [
    ('What is the fundamental economic problem?', 'Unlimited wants but limited resources with which to satisfy them',
     'The economic problem: wants are unlimited, resources (land, labour, capital, enterprise) are finite, so choices must be made.',
     ['Prices that are too high for many consumers', 'Firms that produce more than consumers want to buy', 'A money supply that is too small for the economy']),
    ('What is meant by scarcity in economics?', 'Resources are limited in relation to the wants they could be used to satisfy',
     'Scarcity is relative: resources are insufficient to satisfy all wants, not necessarily absent.',
     ['Goods are temporarily unavailable in shops', 'The general level of prices is rising', 'A resource has been used up completely']),
    ('Which of these is a need rather than a want?', 'Clean drinking water', 'Needs are essential for survival (food, water, shelter, clothing); wants are desires beyond these.',
     ['A designer watch', 'A holiday abroad', 'A games console']),
    ('Why does scarcity mean that choices have to be made?', 'Resources used to satisfy one want cannot be used to satisfy another at the same time',
     'Scarce resources have alternative uses, so using them one way means giving up another use.',
     ['Governments set the prices of all goods', 'Wants are limited in number', 'All resources are owned by firms']),
    ('Which statement about scarcity is correct?', 'Scarcity affects high-income and low-income economies alike',
     'All economies have finite resources relative to unlimited wants; only the nature of unmet wants differs.',
     ['Scarcity exists only in low-income economies', 'Scarcity disappears once an economy grows fast enough', 'Scarcity applies only to natural resources such as oil']),
    ('Why are human wants described as unlimited?', 'When one want is satisfied, new wants arise',
     'Wants grow with income, new products and expectations, so they can never all be satisfied.',
     ['Consumers have unlimited incomes', 'Firms can produce any quantity of goods', 'Governments provide all basic needs']),
])
ex(t1_1, [
    ('Explain why scarcity exists even in high-income economies.', 'Although output per head is high, resources are still finite while wants keep growing as incomes rise, so not every want can be met and choices are still needed.',
     '1 mark: resources finite; 1 mark: wants grow/unlimited so choices still required [2]'),
    ('Explain the difference between needs and wants.', 'Needs are goods and services essential for survival, such as food, water and shelter. Wants are desires for goods and services beyond these, such as entertainment; wants are unlimited.',
     '1 mark: needs essential for survival with example; 1 mark: wants are desires beyond needs/unlimited [2]'),
    ('Explain why the basic economic problem means that every economy must make choices.', 'Because resources are scarce relative to unlimited wants, an economy cannot produce everything people want. It must choose which wants to satisfy, and using resources for one purpose means they cannot be used for another.',
     '1 mark: scarce resources vs unlimited wants; 1 mark: cannot satisfy all wants; 1 mark: resources have alternative uses so choice is needed [3]'),
    ('Explain why time can be regarded as a scarce resource.', 'Each person has only 24 hours a day, which has alternative uses such as work, study and leisure; using time for one activity means it cannot be used for another.',
     '1 mark: fixed amount of time; 1 mark: alternative uses so choice needed [2]'),
])
items(t1_1, 'C2', (1, 2, 3, 4), [
    ('The government of {country} has a fixed budget but faces demands for more hospitals, schools and roads. Explain how this illustrates the basic economic problem.',
     'The government’s resources (its budget) are limited, while the demands on them are effectively unlimited, so it must choose which projects to fund and which to go without.',
     '1 mark: limited budget/resources; 1 mark: unlimited demands so choices must be made [2]'),
    ('{person} has a fixed weekly allowance and wants to buy {good}, {good2} and save for a new phone. Explain why {person} faces the problem of scarcity.',
     'The allowance is limited while {person}’s wants exceed what it can buy, so {person} cannot have everything and must choose between the alternatives.',
     '1 mark: limited income/resources; 1 mark: wants exceed means so choice required [2]'),
    ('Water in {city} is rationed during a long drought. Explain why water has become an economic problem for the city.',
     'Water is now scarce relative to the demands of households, farms and firms; because supply cannot meet all wants, it must be allocated between competing uses.',
     '1 mark: supply limited relative to demand; 1 mark: allocation between competing uses [2]'),
])
errs(t1_1, [
    ('Scarcity means that a good has completely run out.', 'Scarcity means resources are limited relative to wants; a good can be widely available and still be scarce because more of it would be wanted if it were free.'),
    ('High-income countries such as {country} do not face the economic problem because they have plenty of money.', 'Money is not a resource for production; all countries have finite land, labour, capital and enterprise relative to unlimited wants, so all face the economic problem.'),
    ('Healthcare in {country} is free at the point of use, so it is no longer scarce.', 'Healthcare still uses scarce resources (doctors, equipment, buildings) that have alternative uses; a zero price does not remove scarcity, it just changes how the good is rationed.'),
    ('Human wants are limited because people only need food, water and shelter.', 'Needs may be limited, but wants are unlimited: as needs are met and incomes rise, people want new and better goods and services.'),
])


@t1_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t1_1_data(r, D):
    c = r.choice(COUNTRIES)
    kind = r.choice([('hospital beds', 'patients needing a bed each night', 'beds'), ('school places', 'children of school age', 'places'),
                     ('litres of water a day (millions)', 'litres demanded a day (millions)', 'litres'), ('social housing units', 'families on the waiting list', 'units')])
    cap = r.choice([400, 480, 520, 600, 750, 900, 1200])
    want = int(cap * r.choice([1.15, 1.2, 1.25, 1.3, 1.4, 1.5, 1.6]))
    short = want - cap
    sh = 100 * short / want
    stem = f'In {c} there are {cap} {kind[0]} but {want} {kind[1]}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the shortfall as a percentage of what is wanted.', pct(sh),
                  f'Shortfall = {want} − {cap} = {short}; {short}/{want} × 100 = {pct(sh)}.', dis_num(r, sh, pct, [100 * short / cap]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the shortfall as a percentage of what is wanted. (b) Explain how these figures illustrate the basic economic problem.'
            + (' (c) Suggest two ways in which the scarce resource could be allocated between those who want it.' if D >= 4 else ''),
            'answer': f'(a) {pct(sh)} (b) Wants exceed the resources available; the resource has alternative uses and cannot satisfy all wants, so a choice must be made.'
            + (' (c) By price (willingness to pay), by need/priority (e.g. waiting lists or medical need), by queuing or by lottery.' if D >= 4 else ''),
            'key': f'(a) {short}/{want} × 100 = {pct(sh)} [2] (b) limited resource vs greater wants [1]; choice/allocation needed [1] [2]' + (' (c) any two valid rationing methods [2]' if D >= 4 else ''),
            'marks': 4 + (2 if D >= 4 else 0), 'type': 'numerical'}


items(t1_1, 'C3', (2, 3, 4), [
    ('Farmland near {city} can be used for new housing or for growing food. Using the concept of scarcity, explain why the city council must make a choice.',
     'Land is a scarce resource with alternative uses; the same land cannot be used for both housing and farming, so the council must decide which want to satisfy and accept giving up the other.',
     '1 mark: land is scarce/finite; 1 mark: alternative uses; 1 mark: choice means the other use is given up [3]'),
    ('{firm} has one factory in {city} and orders for both {mgood} and {mgood2} that exceed what it can produce. Explain how the basic economic problem applies to {firm}.',
     'The factory’s capacity (machines, workers, time) is limited while orders are greater, so {firm} must choose which product to make and in what quantity.',
     '1 mark: limited capacity/resources; 1 mark: demand exceeds capacity; 1 mark: choice of what to produce [3]'),
    ('A charity in {country} has $2 million to spend and must choose between a clean-water project and a school-building project. Explain how this illustrates scarcity and choice.',
     'The charity’s funds are limited relative to the projects it would like to support, so it must choose; whichever it funds, the other is forgone.',
     '1 mark: limited funds; 1 mark: competing uses; 1 mark: choice involves sacrifice [3]'),
])

t1_2 = T('Choice and opportunity cost in decision-making', 'opportunity cost', 'choice')
mc(t1_2, [
    ('What is meant by opportunity cost?', 'The value of the next best alternative forgone when a choice is made',
     'Opportunity cost = next best alternative given up, not the sum of all alternatives and not the money price.',
     ['The money price paid for a good', 'The total value of all alternatives given up', 'The cost of producing one more unit of a good']),
    ('A student chooses to work in a café on Saturday instead of revising or going to a concert. Revising was her second choice. What is the opportunity cost of working?',
     'The revision she gives up', 'Opportunity cost is only the next best alternative (revising), not every alternative.',
     ['The wage she earns in the café', 'Both the revision and the concert', 'The concert she gives up']),
    ('A government spends $500 million on a new airport rather than on schools, its next best option. What is the opportunity cost of the airport?',
     'The schools that could have been built', 'The forgone next best use of the resources.',
     ['$500 million', 'The flights that will use the airport', 'The taxes needed to finance it']),
    ('Why do economists measure opportunity cost in terms of goods forgone rather than money?', 'Because money is only a claim on resources; the real cost is the alternative use of those resources',
     'Opportunity cost is the real sacrifice of alternatives.', ['Because money has no value', 'Because prices never change', 'Because goods are never scarce']),
    ('Which situation has a zero opportunity cost?', 'Using a resource that has no alternative use', 'If there is no alternative use, nothing is forgone.',
     ['Buying a good that is on sale at half price', 'Receiving a good that the government provides free of charge', 'Using savings rather than borrowing to buy a good']),
    ('A farmer can grow either 200 tonnes of maize or 50 tonnes of beans on a field. What is the opportunity cost of 1 tonne of beans?', '4 tonnes of maize',
     'Opportunity cost of 1 beans = 200/50 = 4 maize.', ['0.25 tonnes of maize', '50 tonnes of maize', '200 tonnes of maize']),
])
ex(t1_2, [
    ('Explain why a good that is provided free to consumers by the government still has an opportunity cost.', 'Producing it uses scarce resources (labour, materials, capital) that could have been used to produce something else; society gives up that alternative even though the consumer pays nothing.',
     '1 mark: uses scarce resources; 1 mark: alternative output forgone by society [2]'),
    ('Explain why the opportunity cost of going to university includes more than the tuition fees.', 'The student also gives up the earnings (and work experience) from a job they could have taken instead; these forgone earnings are often the largest part of the opportunity cost.',
     '1 mark: forgone earnings; 1 mark: real alternative given up, not just money spent [2]'),
    ('Explain how the concept of opportunity cost can help a government decide how to spend its budget.', 'By comparing what is gained from each project with the benefits of the next best project forgone, the government can choose the option whose benefits exceed its opportunity cost.',
     '1 mark: identifies alternatives forgone; 1 mark: compare benefit with opportunity cost; 1 mark: choose best use of scarce funds [3]'),
    ('Explain why the opportunity cost of an unemployed worker’s time may be low.', 'An unemployed worker is not currently producing output or earning a wage, so using their time for training or a new job gives up relatively little paid output.',
     '1 mark: no current paid work; 1 mark: little forgone so low opportunity cost [2]'),
])
items(t1_2, 'C2', (1, 2, 3, 4), [
    ('{person} has one evening free and can either work an extra shift, revise for an economics test or go to the cinema. Explain what determines the opportunity cost of revising.',
     'It is the value of whichever of the other two options {person} ranks next best (the shift or the cinema), not both of them.', '1 mark: next best alternative; 1 mark: only one alternative, not all [2]'),
    ('The council of {city} decides to turn a park into a car park. Explain the opportunity cost of this decision.', 'The leisure, environmental and health benefits of the park that are given up by residents are the opportunity cost.', '1 mark: identifies forgone park benefits; 1 mark: links to next best use of land [2]'),
    ('{firm} uses its factory to make {mgood} instead of {mgood2}. Explain the opportunity cost to {firm}.', 'The profit (or output) from making {mgood2}, the next best use of the factory, is given up.', '1 mark: forgone output/profit of {good2}; 1 mark: next best use of the resources [2]'),
])
errs(t1_2, [
    ('The opportunity cost of buying {good} is the price paid for it.', 'Opportunity cost is the next best alternative given up, i.e. what else that money (or resources) could have bought, not the price itself.'),
    ('If I choose a holiday instead of a new laptop or a bicycle, the opportunity cost is the laptop and the bicycle.', 'Opportunity cost is only the single next best alternative forgone, not all the alternatives.'),
    ('Free school meals in {country} have no opportunity cost because pupils do not pay.', 'The meals still use scarce resources that could have produced something else, so society bears an opportunity cost even though pupils pay nothing.'),
])


@t1_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t1_2_oc(r, D):
    p = person(r)
    w = r.choice([8, 10, 12, 15, 18, 20, 25])
    h = r.choice([4, 5, 6, 8])
    fee = r.choice([0, 20, 30, 40, 50])
    act = r.choice(['a training course', 'a music festival', 'a coding workshop', 'a sports tournament', 'a volunteering day'])
    oc = w * h + fee
    if D <= 2:
        stem = (f'{p} can work for {h} hours at ${w} an hour or attend {act}, which costs ${fee} to enter. {p} attends {act}. '
                f'Calculate the opportunity cost of attending, measured in money.') if fee else (
                f'{p} can work for {h} hours at ${w} an hour or attend {act}, which is free. {p} attends {act}. Calculate the opportunity cost in money terms.')
        return cq(r, D, stem, money(oc), f'Forgone wages ${w} × {h} = {money(w * h)}' + (f' + entry fee ${fee}' if fee else '') + f' = {money(oc)}.',
                  dis_num(r, oc, money, [w * h, fee or w, w * h - fee if fee else w * (h - 1)]), mcq_D=(1, 2))
    # choice between several alternatives with values
    acts = r.sample([('a part-time job', None), ('a private tutoring session', None), ('a weekend trip', None), ('a computer course', None), ('a football coaching job', None)], 3)
    vals = r.sample([60, 75, 90, 110, 120, 140, 150], 3)
    order = sorted(zip(vals, [a for a, _ in acts]), reverse=True)
    chosen, nxt = order[0], order[1]
    stem = (f'{p} values three ways of spending Saturday: ' + '; '.join(f'{a} (worth ${v} to {p})' for v, a in zip(vals, [a for a, _ in acts])) +
            f'. {p} makes the rational choice. (a) Identify the choice made and calculate its opportunity cost. (b) Explain why the opportunity cost is not ${order[1][0] + order[2][0]}.')
    if D >= 4:
        stem += f' (c) The value of {nxt[1]} rises by ${chosen[0] - nxt[0] + 10}. Explain how {p}’s choice changes.'
    ans = (f'(a) {chosen[1]}; opportunity cost = {nxt[1]}, worth ${nxt[0]}. (b) Only the next best alternative is forgone; {p} could not have done both of the others at once.'
           + (f' (c) {nxt[1]} is now worth ${nxt[0] + chosen[0] - nxt[0] + 10}, more than {chosen[1]}, so {p} switches to it and the opportunity cost becomes {chosen[1]} (${chosen[0]}).' if D >= 4 else ''))
    key = (f'(a) highest value option chosen [1]; opportunity cost = next best, ${nxt[0]} [1] [2] (b) only next best alternative counts [1] [1]'
           + (' (c) new ranking [1]; new opportunity cost [1] [2]' if D >= 4 else ''))
    return {'stem': stem, 'answer': ans, 'key': key, 'marks': 3 + (2 if D >= 4 else 0), 'type': 'multi_step'}


@t1_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t1_2_ratio(r, D):
    c = r.choice(COUNTRIES)
    a, b = r.sample([('maize', 'tonnes'), ('cotton', 'bales'), ('rice', 'tonnes'), ('coffee', 'sacks'), ('wheat', 'tonnes'), ('tea', 'crates')], 2)
    qa = r.choice([120, 150, 200, 240, 300, 360])
    qb = r.choice([30, 40, 60, 80, 90])
    if qa == qb:
        return None
    oc = qa / qb
    stem = f'A farmer in {c} can use a field to grow either {qa} {a[1]} of {a[0]} or {qb} {b[1]} of {b[0]} in a season (or any combination at a constant rate).'
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the opportunity cost of producing one {b[1][:-1]} of {b[0]}.', f'{r2(oc)} {a[1]} of {a[0]}',
                  f'{qa}/{qb} = {r2(oc)} {a[1]} of {a[0]} per {b[1][:-1]} of {b[0]}.',
                  [f'{r2(x)} {a[1]} of {a[0]}' for x in (qb / qa, qa, qb, oc * 2)], mcq_D=(1, 2))
    k = r.choice([10, 15, 20, 25])
    if k >= qb:
        return None
    return {'stem': stem + f' (a) Calculate the opportunity cost of one {b[1][:-1]} of {b[0]} in terms of {a[0]}. (b) Calculate how much {a[0]} is given up if the farmer grows {k} {b[1]} of {b[0]}. (c) Explain why the opportunity cost may not stay constant if the farmer uses more fields of differing quality.',
            'answer': f'(a) {r2(oc)} {a[1]} of {a[0]} (b) {num(k * oc, 1)} {a[1]} (c) Land is not equally suited to both crops; as more land switches, less suitable land is used, so more {a[0]} must be given up per extra unit of {b[0]} (increasing opportunity cost).',
            'key': f'(a) {qa}/{qb} [1] (b) {k} × {r2(oc)} = {num(k * oc, 1)} [1] (c) resources not equally suited [1]; increasing opportunity cost [1] [4]', 'marks': 4, 'type': 'numerical'}


t1_3 = T('Economic agents and the basic questions: what, how and for whom to produce', 'economic agents', 'what, how and for whom', 'basic questions')
mc(t1_3, [
    ('Which are the three main economic agents in a closed economy?', 'Households, firms and the government',
     'Economic agents are decision-makers: households (consumers/workers), firms (producers) and government.', ['Banks, shops and factories', 'Exporters, importers and tourists', 'Workers, trade unions and managers']),
    ('Which question is about how to produce?', 'Should cars be built using robots or skilled workers?', 'How to produce = choice of production methods/factor combinations.',
     ['Should more cars or more buses be built?', 'Should cars be sold to people with the highest incomes?', 'Should car prices be controlled?']),
    ('Which question is about for whom to produce?', 'Who should receive the goods and services that are produced?', 'For whom = distribution of output between people.',
     ['Which goods should be produced?', 'Which technique should be used?', 'How many workers should be employed?']),
    ('Why must every economy answer the questions of what, how and for whom to produce?', 'Because resources are scarce and have alternative uses',
     'Scarcity forces choices about resource allocation.', ['Because governments require it', 'Because money is limited', 'Because firms aim to maximise profit']),
    ('In their role as economic agents, what do households mainly supply to firms?', 'Factors of production such as labour', 'Households own and supply factors of production and buy goods and services.',
     ['Finished goods and services', 'Tax revenue', 'Government subsidies']),
    ('Which economic agent is mainly concerned with maximising profit?', 'Firms', 'Firms are usually assumed to aim to maximise profit; households maximise utility; government maximises welfare.',
     ['Households', 'Government', 'Charities']),
])
ex(t1_3, [
    ('Explain the meaning of the question “what to produce?” and why it arises.', 'It concerns which goods and services, and how much of each, an economy should make with its scarce resources; it arises because resources cannot produce everything wanted.',
     '1 mark: which goods and quantities; 1 mark: arises from scarcity [2]'),
    ('Explain the different objectives that households, firms and the government are assumed to pursue.', 'Households aim to maximise utility (satisfaction) from consumption; firms aim to maximise profit; government aims to maximise the welfare of society as a whole.',
     '1 mark each agent correctly linked to objective [3]'),
    ('Explain how the question “for whom to produce?” is linked to the distribution of income.', 'In a market system goods go to those with income to pay for them, so the distribution of income largely determines who receives output; governments may redistribute to change this.',
     '1 mark: goods go to those able to pay; 1 mark: income distribution determines allocation/role of redistribution [2]'),
])
items(t1_3, 'C2', (1, 2, 3, 4), [
    ('The government of {country} must decide whether to build a new hospital or a new motorway. Identify which basic economic question this decision answers and explain why.',
     'What to produce: it decides which output (healthcare or transport) the scarce resources are used for.', '1 mark: what to produce; 1 mark: explanation [2]'),
    ('{firm} decides to replace assembly-line workers in {city} with machines. Identify which basic economic question this answers and explain why.', 'How to produce: it is a choice of production method (more capital, less labour).', '1 mark: how to produce; 1 mark: choice of factor combination [2]'),
    ('{country} introduces free school meals for children from low-income families. Identify which basic economic question this addresses and explain why.', 'For whom to produce: it determines who receives the output (low-income children) regardless of ability to pay.', '1 mark: for whom; 1 mark: distribution explained [2]'),
])
BQ_CASES = [
    ('{firm} must decide whether to make more {good} or more {good2} next year.', 'What to produce', 'the decision is about which goods and how much of each to make.'),
    ('A farm in {country} switches from hand-picking crops to using harvesting machines.', 'How to produce', 'it is a change in the method of production / factor combination.'),
    ('The government of {country} gives food vouchers to the poorest families.', 'For whom to produce', 'it decides who receives the output.'),
    ('A hospital in {city} must decide whether to treat patients in order of arrival or of medical need.', 'For whom to produce', 'it decides who receives the scarce service.'),
    ('The state planning office of {country} sets targets for steel and tractor output for next year.', 'What to produce', 'the targets decide which goods are produced and in what quantities.'),
    ('{firm} decides to use solar power rather than diesel generators in its factory in {city}.', 'How to produce', 'it chooses the technique and inputs used in production.'),
    ('Concert tickets in {city} are sold to the highest bidders in an online auction.', 'For whom to produce', 'the auction determines who receives the tickets (those willing and able to pay most).'),
    ('{country} decides to build more electric buses and fewer diesel cars.', 'What to produce', 'it is a decision about which goods are made with the economy’s resources.'),
]
classify(t1_3, BQ_CASES, ['What to produce', 'How to produce', 'For whom to produce'], 'Which basic economic question is being answered?',
         'Identify which basic economic question each decision answers, giving a reason in each case.', extra=['Why to produce'])
AGENT_CASES = [
    ('{person} works 35 hours a week and spends the wage on food and rent.', 'Household', 'supplies labour and buys goods and services to maximise utility.'),
    ('{firm} hires workers and sells {good} in {country}.', 'Firm', 'employs factors of production and sells output, aiming for profit.'),
    ('The authorities in {country} collect taxes and provide schools.', 'Government', 'raises taxes and provides public and merit goods for society’s welfare.'),
    ('A family in {city} rents out a spare room and buys a new fridge.', 'Household', 'owns and supplies a factor (land/property) and consumes goods.'),
    ('The ministry of transport of {country} builds a new railway.', 'Government', 'it provides infrastructure financed by taxation for society as a whole.'),
    ('{firm2} borrows to buy new machines and expand output of {good2}.', 'Firm', 'it invests in capital and produces output for sale.'),
]
classify(t1_3, AGENT_CASES, ['Household', 'Firm', 'Government'], 'Which economic agent is described?',
         'Identify the economic agent in each case and explain its role.', D=(1, 2, 3, 4), extra=['Trade union'], name='agents')


def _ch1_case(r, D):
    d = ctx(r)
    budget = r.choice([400, 600, 800, 1200])
    hosp, rail, sch = r.sample([150, 200, 250, 300, 350], 3)
    intro = (f'Extract: The government of {d["country"]} has ${budget} million for new projects this year. Ministers have proposed a hospital (${hosp} million), '
             f'a rail link to {d["city"]} (${rail} million) and a programme of school building (${sch} million), as well as a cut in taxes. '
             f'Opposition politicians say the government should “stop wasting money and simply do everything”.')
    tot = hosp + rail + sch
    parts = [
        lambda r: ('Calculate how much more than the budget would be needed to fund all three projects.' if tot > budget else 'Calculate how much of the budget would be left if all three projects were funded.',
                   money(abs(tot - budget)) + ' million', f'{hosp} + {rail} + {sch} = {tot}; |{tot} − {budget}| = {abs(tot - budget)} [2]'),
        lambda r: ('Using the extract, explain the meaning of the basic economic problem.', 'Limited resources (a budget of ${} million) but many competing wants (hospital, rail, schools, tax cuts), so choices must be made.'.format(budget), '1 mark: limited resources; 1 mark: unlimited/competing wants; 1 mark: use of extract [3]'),
        lambda r: ('Explain the opportunity cost to the government of choosing the rail link.', 'The benefits of the next best project that cannot now be funded (e.g. the hospital) are forgone.', '1 mark: next best alternative; 1 mark: applied to extract [2]'),
        lambda r: ('Explain why the opposition’s suggestion to “do everything” does not solve the economic problem.', 'Borrowing or taxing more still uses scarce resources; resources diverted from private uses or future spending have an opportunity cost.', '1 mark: resources still finite; 1 mark: cost moves elsewhere/future [2]'),
        lambda r: ('Discuss how the government should decide which project to fund.', 'Compare benefits and opportunity costs; consider who gains (for whom), long-run effects on growth, equity and public opinion; data may be uncertain; judgement.', '2 marks: analysis of criteria; 2 marks: evaluation and conclusion [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t1_1, t1_2, t1_3], _ch1_case)
essay(t1_1, [
    ('Explain why scarcity is described as the fundamental economic problem and why it requires all economies to make choices.',
     'Unlimited wants vs finite resources (land, labour, capital, enterprise); resources have alternative uses; choice and opportunity cost; the three basic questions follow.',
     'economic growth will eventually solve the problem of scarcity in {country}',
     'Growth raises output per head, satisfying more needs; technology lowers costs and creates new resources; absolute poverty can be eliminated.',
     'Wants grow with income; resources such as the environment are finite; growth has costs (pollution); relative scarcity remains; distribution matters.'),
], ['{country} has grown rapidly for twenty years, yet many families still say they cannot afford everything they want.'])
essay(t1_2, [
    ('Explain, with examples, the concept of opportunity cost and why it is important for decision-makers.',
     'Next best alternative forgone; examples for consumers, firms and governments; helps compare options; real cost of resources not money.',
     'opportunity cost is the most useful concept for governments when deciding how to spend public money',
     'Makes the trade-off explicit; focuses on real alternatives; prevents waste; links to the PPC.',
     'Hard to measure non-market benefits; equity and political objectives also matter; information and time constraints; long-term effects uncertain.'),
], ['The government of {country} must choose between building a new port and expanding free healthcare.'])
essay(t1_3, [
    ('Explain the three basic economic questions that every economy has to answer.',
     'What, how and for whom to produce; arise from scarcity; examples; different systems answer them differently (price mechanism vs planning).',
     'the question of for whom to produce is best left to the market in {country}',
     'Prices reward effort and ration efficiently; consumer sovereignty; incentives to work.',
     'Market allocation depends on income, so the poor may lack necessities; merit goods underconsumed; need for redistribution and government provision.'),
])
CHAPTERS[1] = [t1_1, t1_2, t1_3]

# ============================================================================ 2 Economic methodology
t2_1 = T('Economics as a social science: models, assumptions and ceteris paribus', 'social science', 'models', 'ceteris paribus')
mc(t2_1, [
    ('What does the term ceteris paribus mean?', 'All other things remaining equal', 'Ceteris paribus: holding all other variables constant so the effect of one change can be isolated.',
     ['All prices change together', 'The market is in equilibrium', 'Government does not intervene']),
    ('Why is economics described as a social science?', 'It studies human behaviour in using scarce resources, using scientific methods where possible',
     'Economics uses models, hypotheses and data, but studies people, whose behaviour varies.', ['It can carry out controlled laboratory experiments on whole economies', 'It always produces exact predictions', 'It does not use data']),
    ('Why do economists use models?', 'To simplify reality so that relationships between variables can be analysed', 'Models abstract from detail to explain and predict.',
     ['To describe every detail of the real world', 'To avoid the need for assumptions', 'To make value judgements about policy']),
    ('Why is it difficult for economists to test theories in the same way as natural scientists?', 'Many factors change at once and controlled experiments on economies are rarely possible',
     'Economists cannot easily hold other things equal in the real world.', ['Economic data are never collected', 'Economic theories contain no assumptions', 'People always behave identically']),
    ('Which is an assumption commonly made in simple economic models?', 'Consumers act rationally to maximise their satisfaction', 'Rationality is a core simplifying assumption.',
     ['Consumers always buy the most expensive good', 'Firms never respond to prices', 'Resources are unlimited']),
])
ex(t2_1, [
    ('Explain why economists make use of the ceteris paribus assumption when analysing demand.', 'Demand depends on many variables (price, income, tastes, prices of related goods). Holding the others constant isolates the effect of one change, such as price, on quantity demanded.',
     '1 mark: many variables affect demand; 1 mark: holding others constant isolates one effect [2]'),
    ('Explain one strength and one limitation of using economic models.', 'Strength: they simplify complex reality so cause and effect can be analysed and predictions made. Limitation: assumptions may be unrealistic, so predictions may be inaccurate.',
     '1 mark: strength; 1 mark: limitation [2]'),
    ('Explain why economic predictions are often less precise than predictions in physics.', 'Economics studies human behaviour, which changes with expectations, culture and information; many variables change at once and controlled experiments are rarely possible.',
     '1 mark: human behaviour unpredictable; 1 mark: cannot hold other things equal / no controlled experiments [2]'),
])
items(t2_1, 'C2', (1, 2, 3, 4), [
    ('An economist predicts that a fall in the price of {good} in {country} will increase the quantity demanded “ceteris paribus”. Explain why the prediction might not come true.',
     'Other factors may change at the same time, e.g. incomes fall or tastes change, shifting demand and offsetting the effect of the price fall.', '1 mark: other variables change; 1 mark: example and effect [2]'),
    ('A model used by the central bank of {country} assumes that consumers always act rationally. Explain why this assumption is made and one problem with it.',
     'It simplifies analysis and allows predictions; but consumers may act on habit, emotion or limited information, so the model may predict wrongly.', '1 mark: why assumed; 1 mark: problem [2]'),
])
errs(t2_1, [
    ('Economic models are useless because they are based on unrealistic assumptions.', 'All models simplify; assumptions make analysis manageable, and a model is useful if it explains and predicts reasonably well, even if its assumptions are not exactly true.'),
    ('Ceteris paribus means that prices do not change.', 'Ceteris paribus means all other factors are held constant while one variable (which may be price) is allowed to change.'),
    ('Economics is a natural science because it uses graphs and numbers.', 'Economics uses scientific methods but it studies human behaviour, so it is a social science.'),
])
CP_CASES = [
    ('An economist studies the effect of a rise in the price of {good} on sales, holding incomes, tastes and other prices constant.', 'Ceteris paribus assumption', 'only one variable is changed while others are held equal.'),
    ('A model of {country}’s economy assumes that firms aim only to maximise profit.', 'Simplifying assumption about behaviour', 'it simplifies firms’ objectives to make the model manageable.'),
    ('Economists compare unemployment in {country} before and after a new training scheme, but many other changes happened at the same time.', 'Problem of testing theories', 'other variables changed, so the effect cannot be isolated.'),
    ('A theory predicts that higher interest rates in {country} will reduce borrowing; economists check this using data from the last 20 years.', 'Testing a hypothesis with evidence', 'the prediction is compared with real-world data.'),
    ('A simple model of {city}’s taxi market assumes all taxis are identical.', 'Simplifying assumption about behaviour', 'it ignores differences between firms to focus on price and quantity.'),
]
classify(t2_1, CP_CASES, ['Ceteris paribus assumption', 'Simplifying assumption about behaviour', 'Problem of testing theories', 'Testing a hypothesis with evidence'],
         'Which aspect of economic method does this illustrate?', 'Identify which aspect of economic method each statement illustrates and explain why.')


@t2_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t2_1_cp(r, D):
    g = r.choice(GOODS)
    c = r.choice(COUNTRIES)
    p0, p1 = r.choice([(4, 5), (10, 12), (20, 24), (50, 55), (8, 10)])
    q0 = r.choice([1000, 1200, 1500, 2000, 2400])
    q_pred = int(q0 * r.choice([0.8, 0.85, 0.9]))
    inc = r.choice([4, 5, 6, 8])
    q_act = int(q0 * r.choice([1.02, 1.05, 0.98, 1.0]))
    if q_act == q_pred:
        return None
    stem = (f'A model predicted that when the price of {g} in {c} rose from ${p0} to ${p1}, weekly sales would fall from {q0} to {q_pred} units, ceteris paribus. '
            f'In fact, sales were {q_act} units, and average incomes rose by {inc}% over the same period.')
    pc = chg(q0, q_pred)
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the percentage change in sales predicted by the model.', pct(pc), f'({q_pred} − {q0})/{q0} × 100 = {pct(pc)}.', dis_num(r, pc, pct, [chg(q0, q_act), chg(p0, p1)]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the predicted and the actual percentage changes in sales. (b) Using the idea of ceteris paribus, explain why the prediction was not accurate.'
            + (' (c) Comment on whether this shows the model is wrong.' if D >= 4 else ''),
            'answer': f'(a) Predicted {pct(pc)}; actual {pct(chg(q0, q_act))}. (b) Other things did not stay equal: higher incomes shifted demand to the right (if {g} is normal), offsetting the price effect.'
            + (' (c) Not necessarily: the price effect may still be correct; the model holds other variables constant, so the evidence must be adjusted for the income change before rejecting it.' if D >= 4 else ''),
            'key': '(a) both percentages [2] (b) ceteris paribus violated [1]; income rise shifts demand [1]' + (' (c) reasoned comment [2] [6]' if D >= 4 else ' [4]'),
            'marks': 4 + (2 if D >= 4 else 0), 'type': 'numerical'}


t2_2 = T('Positive and normative statements', 'positive and normative', 'normative', 'value judgement')
mc(t2_2, [
    ('What is a positive statement?', 'A statement of fact that can be tested against evidence', 'Positive statements are objective and testable, whether true or false.',
     ['A statement that expresses an opinion about what ought to happen', 'A statement that is always true', 'A statement that supports government policy']),
    ('What is a normative statement?', 'A statement containing a value judgement about what ought to be', 'Normative = opinion/value judgement, cannot be proved true or false.',
     ['A statement that can be tested using data', 'A statement about past events only', 'A statement made by an economist']),
    ('Which is a normative statement?', 'The government should spend more on public transport', '“Should” signals a value judgement.',
     ['Unemployment rose by 2% last year', 'A rise in price reduces the quantity demanded, ceteris paribus', 'Inflation in the country was 4% in the last year']),
    ('Which is a positive statement?', 'An increase in the minimum wage will reduce employment among young workers', 'It can be tested against evidence, even if it turns out to be false.',
     ['The minimum wage is unfair to employers', 'The minimum wage ought to be increased', 'It is wrong for workers to be paid so little']),
    ('Why can a positive statement be incorrect?', 'It is testable, and the evidence may show it to be false', 'Positive ≠ true; it is a claim that can be checked.',
     ['Because it contains a value judgement', 'Because it uses the word “should”', 'Because it describes the future']),
])
ex(t2_2, [
    ('Explain the difference between positive and normative statements, giving an example of each.', 'Positive: objective statement that can be tested with evidence, e.g. “inflation was 3% last year”. Normative: contains a value judgement about what ought to be, e.g. “inflation should be lower”.',
     '1 mark: positive definition; 1 mark: normative definition; 1 mark: valid examples [3]'),
    ('Explain why economists might agree on positive statements but disagree on normative statements.', 'Positive statements can be settled by evidence, but normative statements depend on value judgements (e.g. about fairness), which differ between people.',
     '1 mark: positive testable; 1 mark: normative depend on values [2]'),
    ('Explain why government policy decisions usually involve normative judgements.', 'Policies create winners and losers; choosing between them requires judgements about what is fair or desirable, not only facts.',
     '1 mark: trade-offs/winners and losers; 1 mark: value judgement required [2]'),
])
POS = ['the unemployment rate in {country} rose to 6% last year', 'a rise in the price of {good} will reduce the quantity demanded, ceteris paribus',
       'a tax on sugary drinks in {country} will reduce consumption of them', 'higher interest rates reduce consumer borrowing in {country}',
       'the average wage in {city} is higher than the national average', 'exports from {country} fell by 3% in the last quarter',
       'a subsidy to bus companies in {city} will lower fares', 'inflation in {country} has been above 5% for three years',
       'increasing the minimum wage will reduce employment of young workers', 'tariffs on imported steel will raise the price of cars made in {country}']
NORM = ['the government of {country} should reduce income tax for low earners', 'it is unfair that the richest 10% in {country} own half of all wealth',
        'the price of {good} is too high', '{country} ought to spend more on healthcare than on defence', 'unemployment is a more serious problem than inflation',
        'the council of {city} should ban cars from the city centre', 'the minimum wage in {country} ought to be raised', 'it is wrong that {firm} pays its managers so much',
        'governments should protect domestic farmers from foreign competition', 'public transport in {city} should be free']


@t2_2.add('C3', (1, 2, 3, 4, 5), 'explain')
def t2_2_class(r, D):
    d = ctx(r)
    if D <= 2:
        pos = r.random() < 0.5
        s = fill(r.choice(POS if pos else NORM), d)
        lab = 'Positive' if pos else 'Normative'
        opts, a = mcq(r, lab, ['Positive', 'Normative', 'Neither positive nor normative', 'Both positive and normative'])
        return {'stem': f'A newspaper report states that {s}. Is this statement positive or normative?', 'options': opts, 'answer': a,
                'key': f'{lab}: ' + ('it can be tested against evidence.' if pos else 'it contains a value judgement about what ought to be.')}
    n = 2 if D == 3 else (3 if D == 4 else 4)
    k = r.randint(1, n - 1)
    sts = [(fill(x, d), 'positive') for x in r.sample(POS, k)] + [(fill(x, d), 'normative') for x in r.sample(NORM, n - k)]
    r.shuffle(sts)
    L = ['(i)', '(ii)', '(iii)', '(iv)']
    stem = f'Classify each of the following statements as positive or normative and explain your choice. ' + ' '.join(f'{L[i]} “{s[0].upper()}{s[1:]}.”' for i, (s, _) in enumerate(sts))
    ans = ' '.join(f'{L[i]} {c}' for i, (_, c) in enumerate(sts))
    key = ' '.join(f'{L[i]} {c} – ' + ('testable with evidence' if c == 'positive' else 'value judgement') + ' [1]' for i, (_, c) in enumerate(sts))
    return {'stem': stem, 'answer': ans, 'key': key + f' Total [{n}]', 'marks': n, 'type': 'explain'}


@t2_2.add('C3', (2, 3, 4, 5), 'explain')
def t2_2_rewrite(r, D):
    d = ctx(r)
    s = fill(r.choice(NORM), d)
    return {'stem': f'A politician in {d["country"]} says that {s}. (a) Explain why this is a normative statement. (b) Write a related positive statement that an economist could test, and state the evidence needed to test it.',
            'answer': '(a) It expresses an opinion/value judgement about what ought to be and cannot be proved true or false. (b) e.g. a cause-and-effect claim about the policy’s outcome (such as its effect on prices, output or employment), tested with data collected before and after the change or compared with similar places.',
            'key': '(a) value judgement / not testable [2] (b) valid testable statement [1]; appropriate evidence [1] [2]', 'marks': 4, 'type': 'explain'}


items(t2_2, 'C2', (1, 2, 3, 4), [
    ('A report on {country} states: “Youth unemployment is 18%, which is unacceptably high.” Explain which parts of this sentence are positive and which are normative.',
     '“Youth unemployment is 18%” is positive (testable); “unacceptably high” is normative (value judgement).', '1 mark: positive part; 1 mark: normative part [2]'),
    ('Two economists in {country} agree that a sugar tax would cut obesity by 5% but disagree about whether it should be introduced. Explain why.',
     'They agree on the positive (testable) effect but differ in value judgements about fairness, freedom of choice and the burden on low-income households.', '1 mark: agree on positive; 1 mark: disagree on normative values [2]'),
])
errs(t2_2, [
    ('“The government should cut taxes” is a positive statement because many economists agree with it.', 'It is normative because it expresses what ought to be done; agreement does not make a value judgement testable.'),
    ('A positive statement must be true.', 'A positive statement is one that can be tested against evidence; it may turn out to be false.'),
    ('“Inflation will fall if interest rates rise” is normative because it is about the future.', 'It is positive: it is a cause-and-effect claim that can be tested with evidence, even though it is a prediction.'),
])

t2_3 = T('Time periods in economics: short run, long run and very long run', 'short run, long run', 'very long run', 'time periods')
mc(t2_3, [
    ('What is meant by the short run in economics?', 'A period in which at least one factor of production is fixed', 'SR: some factors fixed (e.g. capital/plant); LR: all factors variable.',
     ['A period of less than one year', 'A period in which all factors can be varied', 'A period in which technology changes']),
    ('What is meant by the long run?', 'A period in which all factors of production can be varied but technology is given', 'LR: all inputs variable, state of technology fixed.',
     ['A period of more than five years', 'A period in which at least one factor is fixed', 'A period in which technology and all factors change']),
    ('What distinguishes the very long run from the long run?', 'In the very long run technology and the institutional framework can also change', 'VLR: technology, laws and institutions change.',
     ['All factors are fixed in the very long run', 'Prices are fixed in the very long run', 'Only labour can change in the very long run']),
    ('Why is the length of the short run different between industries?', 'Because the time needed to change fixed factors such as plant differs between industries', 'E.g. a café can expand quickly, a power station takes years.',
     ['Because the short run is always six months', 'Because all firms use the same machinery', 'Because governments set it by law']),
    ('Which change can a car manufacturer make only in the long run?', 'Building a new factory', 'Plant size is fixed in the short run.', ['Employing more workers on overtime', 'Buying more steel', 'Increasing the number of shifts']),
])
ex(t2_3, [
    ('Explain the difference between the short run and the long run.', 'Short run: at least one factor (usually capital) is fixed, so output can only be changed by varying other inputs. Long run: all factors can be varied, so the scale of production can change.',
     '1 mark: SR fixed factor; 1 mark: LR all factors variable [2]'),
    ('Explain why price elasticity of supply tends to be greater in the long run than in the short run.', 'In the long run firms can change all factors, build new capacity and new firms can enter, so output responds more to a price change.',
     '1 mark: more factors variable/capacity; 1 mark: greater response to price [2]'),
    ('Explain why the short run for a power station is much longer than for a hairdresser.', 'A power station needs many years to plan and build new capacity, whereas a hairdresser can rent another chair or small premises in weeks.',
     '1 mark: time to change fixed capital differs; 1 mark: applied examples [2]'),
])
TP_CASES = [
    ('{firm} asks its workers in {city} to work overtime to meet a rise in orders.', 'Short run', 'labour is varied while the factory (capital) is fixed.'),
    ('{firm} builds a second factory to double capacity.', 'Long run', 'the quantity of capital (plant size) is changed, so all factors are variable.'),
    ('Scientists in {country} develop a new battery technology that transforms electricity storage.', 'Very long run', 'technology itself changes.'),
    ('A café in {city} buys extra coffee beans and hires a part-time worker for the weekend.', 'Short run', 'variable inputs are added to fixed premises.'),
    ('{country} changes its laws to allow private firms to run the railways.', 'Very long run', 'the institutional framework changes.'),
    ('A hotel group moves out of its old building into a larger purpose-built hotel.', 'Long run', 'all factors, including buildings, are varied.'),
    ('A farm hires extra pickers for the harvest on its existing land.', 'Short run', 'land is fixed; only labour is varied.'),
]
classify(t2_3, TP_CASES, ['Short run', 'Long run', 'Very long run'], 'Which time period does this change illustrate?',
         'Identify the time period illustrated by each change and explain your answer.', extra=['Market period'])
items(t2_3, 'C2', (1, 2, 3, 4), [
    ('Demand for {good} in {country} rises sharply. Explain why producers can increase output only a little in the short run.', 'Some factors (factory space, machines) are fixed in the short run, so output can only be raised by adding variable inputs such as overtime, which is limited.', '1 mark: fixed factors; 1 mark: limited by variable inputs [2]'),
    ('Explain how the {ind} industry in {country} might respond differently to higher prices in the short run and in the long run.', 'Short run: existing firms raise output with existing capacity (overtime, more materials). Long run: firms expand capacity and new firms enter, so output rises much more.', '1 mark: SR response; 1 mark: LR response [2]'),
])
errs(t2_3, [
    ('The short run is always a period of less than one year.', 'The short run is defined by at least one factor being fixed, not by calendar time; its length differs between industries.'),
    ('In the long run, technology can change.', 'In the long run all factors can vary but technology is given; changes in technology belong to the very long run.'),
])


@t2_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t2_3_cap(r, D):
    f = r.choice(FIRMS)
    q = r.choice([500, 800, 1000, 1200])
    ot = r.choice([10, 15, 20])
    lr = r.choice([60, 80, 100])
    m = r.choice([6, 9, 12, 18, 24])
    stem = (f'{f} produces {q} units a week in one factory. Overtime can raise output by up to {ot}% within a month. A new production line, taking {m} months to install, would raise capacity by {lr}%.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the maximum weekly output possible in the short run.', f'{num(q * (1 + ot / 100))} units', f'{q} × {1 + ot / 100} = {num(q * (1 + ot / 100))}.',
                  dis_num(r, q * (1 + ot / 100), lambda x: f'{num(x)} units', [q * (1 + lr / 100), q]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the maximum weekly output in the short run and after the new line is installed (without overtime). (b) Explain why the two figures relate to different time periods.',
            'answer': f'(a) Short run: {num(q * (1 + ot / 100))} units; long run: {num(q * (1 + lr / 100))} units. (b) In the short run the factory is fixed so only labour (overtime) can vary; installing a new line changes capital, which can only be done in the long run.',
            'key': f'(a) {num(q * (1 + ot / 100))} [1]; {num(q * (1 + lr / 100))} [1] (b) SR fixed capital [1]; LR all factors variable [1] [4]', 'marks': 4, 'type': 'numerical'}


t2_4 = T('Decisions at the margin', 'margin', 'marginal')
mc(t2_4, [
    ('What does it mean to make a decision at the margin?', 'Comparing the extra benefit with the extra cost of one more unit', 'Marginal analysis: compare MB and MC of a small change.',
     ['Comparing total benefit with total cost', 'Making a decision without considering costs', 'Choosing the cheapest option available']),
    ('A rational consumer should continue to buy more units of a good as long as', 'the marginal benefit is at least equal to the marginal cost', 'Buy while MB ≥ MC; stop where MB = MC.',
     ['total benefit is rising', 'the price is falling', 'average benefit exceeds average cost']),
    ('A firm’s marginal cost of producing the 50th unit is $12 and the marginal revenue is $15. What should a profit-seeking firm do?', 'Produce the 50th unit, because it adds $3 to profit',
     'MR > MC so the unit adds to profit.', ['Not produce the 50th unit', 'Cut its price', 'Stop production altogether']),
    ('Why do marginal benefits usually fall as more of an activity is undertaken?', 'Each additional unit gives less extra satisfaction than the previous one', 'Diminishing marginal benefit (utility).',
     ['Prices always rise', 'Total benefit falls', 'Costs are fixed']),
    ('At which point is the net benefit of an activity maximised?', 'Where marginal benefit equals marginal cost', 'Net benefit = TB − TC is maximised where MB = MC.',
     ['Where total benefit is maximised', 'Where marginal cost is zero', 'Where average benefit is maximised']),
])
ex(t2_4, [
    ('Explain why a rational decision-maker compares marginal benefit with marginal cost rather than total benefit with total cost.', 'Most decisions are about doing a little more or less; comparing the extra benefit and cost of that change shows whether it raises net benefit, which totals do not show.',
     '1 mark: decisions are about small changes; 1 mark: MB vs MC shows whether net benefit rises [2]'),
    ('Explain why a student might stop revising after four hours even though more revision would still raise the expected mark.', 'The marginal benefit of each extra hour falls (fatigue) while the marginal cost (forgone leisure/sleep) rises; once MC exceeds MB, further revision reduces net benefit.',
     '1 mark: falling MB; 1 mark: rising MC/opportunity cost; 1 mark: stop where MB = MC [3]'),
    ('Explain how marginal analysis helps a government decide how much pollution to allow.', 'Reducing pollution further has a rising marginal cost and a falling marginal benefit; the optimal amount of clean-up is where the two are equal, not zero pollution.',
     '1 mark: MB and MC of reduction; 1 mark: optimum where equal [2]'),
])
items(t2_4, 'C2', (1, 2, 3, 4), [
    ('A bus company in {city} has empty seats on a late-night service. Explain, using marginal analysis, why it may sell remaining seats very cheaply.', 'The marginal cost of carrying one more passenger is almost zero once the bus runs, so any fare above that marginal cost adds to revenue and profit.', '1 mark: MC of extra passenger close to zero; 1 mark: price above MC raises profit [2]'),
    ('{person} is deciding whether to work an extra hour for {firm}. Explain how {person} would make this decision at the margin.', 'Compare the extra wage (marginal benefit) with the value of the leisure given up (marginal cost); work the extra hour only if the benefit is at least the cost.', '1 mark: MB = extra pay; 1 mark: MC = forgone leisure; decision rule [2]'),
])
errs(t2_4, [
    ('A firm should keep producing as long as its total revenue is greater than its total cost.', 'To maximise profit it should produce each extra unit only while marginal revenue is at least marginal cost; total comparisons do not show the best output.'),
    ('If eating a meal gives you a lot of total satisfaction, you should always order another one.', 'The decision should depend on the marginal benefit of the next meal compared with its marginal cost, not on total satisfaction.'),
])


@t2_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t2_4_mbmc(r, D):
    act = r.choice([('hours of tutoring', 'hour'), ('kilometres of new cycle lane', 'kilometre'), ('extra bus services per day', 'service'), ('units of output', 'unit'), ('street cleaning shifts', 'shift')])
    n = 6
    mb0 = r.choice([60, 70, 80, 90, 100])
    mb = [mb0 - i * r.choice([10, 12]) for i in range(n)]
    mc0 = r.choice([20, 25, 30])
    mcs = [mc0 + i * r.choice([8, 10]) for i in range(n)]
    best = max(i + 1 for i in range(n) if mb[i] >= mcs[i]) if mb[0] >= mcs[0] else 0
    if best in (0, n):
        return None
    tab = table([f'Number of {act[0]}', 'Marginal benefit ($)', 'Marginal cost ($)'], list(zip(range(1, n + 1), mb, mcs)))
    nb = sum(mb[i] - mcs[i] for i in range(best))
    stem = f'The table shows the marginal benefit and marginal cost of {act[0]} for a council in {r.choice(COUNTRIES)}. {tab}.'
    if D <= 2:
        return cq(r, 1, stem + ' How many should be provided to maximise net benefit?', str(best), f'Provide while MB ≥ MC: unit {best} has MB {mb[best - 1]} ≥ MC {mcs[best - 1]}; unit {best + 1} has MB {mb[best]} < MC {mcs[best]}.',
                  [str(x) for x in (best + 1, best - 1 if best > 1 else best + 2, n, 1) if x != best], mcq_D=(1, 2))
    return {'stem': stem + ' (a) State the quantity that maximises net benefit and explain why. (b) Calculate the total net benefit at this quantity.' + (f' (c) Explain what would happen to net benefit if {best + 1} were provided.' if D >= 4 else ''),
            'answer': f'(a) {best}: every unit up to {best} has MB ≥ MC; the next has MC > MB. (b) ${nb}' + (f' (c) Net benefit falls by ${mcs[best] - mb[best]} to ${nb - (mcs[best] - mb[best])}.' if D >= 4 else ''),
            'key': f'(a) {best} [1]; MB ≥ MC rule [1] (b) Σ(MB − MC) for units 1–{best} = {nb} [2]' + (f' (c) loss of {mcs[best] - mb[best]} [1]' if D >= 4 else ''),
            'marks': 4 + (1 if D >= 4 else 0), 'type': 'numerical'}


def _ch2_case(r, D):
    d = ctx(r)
    t0, t1 = r.choice([(12, 15), (20, 25), (8, 10)])
    s0 = r.choice([400, 500, 600])
    s1 = int(s0 * r.choice([0.92, 0.95, 0.9]))
    intro = (f'Extract: In {d["country"]} the tax on sugary drinks was raised from {t0} to {t1} cents per litre. Monthly sales fell from {s0} million to {s1} million litres. '
             f'The health minister said: “This shows sugar taxes work and every country should have one.” Over the same months a large advertising campaign on healthy eating was run.')
    parts = [
        lambda r: ('Calculate the percentage fall in monthly sales.', pct(-chg(s0, s1)), f'({s0} − {s1})/{s0} × 100 [2]'),
        lambda r: ('Identify one positive and one normative statement in the minister’s comment.', '“Sugar taxes work” (reduce consumption) is positive/testable; “every country should have one” is normative.', '1 mark each [2]'),
        lambda r: ('Explain why the evidence in the extract may not prove that the tax caused the fall in sales.', 'Ceteris paribus did not hold: the advertising campaign also reduced demand; other factors (prices of substitutes, weather) may have changed.', '1 mark: other variables changed; 1 mark: link to extract [2]'),
        lambda r: ('Explain how the government could use marginal analysis to decide the size of the tax.', 'Raise the tax while the marginal benefit (health gains) of the lower consumption exceeds the marginal cost (lost consumer welfare, burden on the poor).', '[2]'),
        lambda r: ('Discuss whether the effects of the tax are likely to be greater in the long run than in the short run.', 'In the long run habits change, firms reformulate drinks and substitutes appear, so the response is larger; but addiction and brand loyalty may limit it; judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t2_1, t2_2, t2_3, t2_4], _ch2_case)
essay(t2_1, [
    ('Explain why economists use models and assumptions such as ceteris paribus.',
     'Reality is complex; models simplify to isolate relationships; ceteris paribus holds other variables constant; allows predictions and testing; examples (demand curve).',
     'economic models are of little use to governments because their assumptions are unrealistic',
     'Assumptions such as rationality and ceteris paribus rarely hold; predictions often fail; behaviour changes with expectations.',
     'Models clarify cause and effect and give direction of change; tested against data; refined over time; judged by predictive power, not realism.'),
])
essay(t2_2, [
    ('Explain the difference between positive and normative statements and why the distinction matters in economics.',
     'Definitions with examples; positive testable, normative value judgements; economists can settle positive disputes with evidence; policy combines both.',
     'economists should only make positive statements and leave normative statements to politicians',
     'Keeps economics objective; evidence-based; avoids bias; economists have no special authority on values.',
     'Policy advice requires judgements about trade-offs; choice of topics is value-laden; economists can clarify the consequences of different value choices.'),
])
essay(t2_3, [
    ('Explain the difference between the short run, the long run and the very long run, with examples from a manufacturing industry.',
     'Fixed vs variable factors; SR at least one factor fixed; LR all variable, technology given; VLR technology/institutions change; examples.',
     'firms in {country} are more able to respond to changes in demand in the long run than in the short run',
     'Capacity can be expanded, new firms enter, PES higher; costs can be minimised over all inputs.',
     'Some firms can respond quickly with spare capacity or stocks; long-run responses are uncertain and costly; demand may change again; depends on the industry.'),
])
essay(t2_4, [
    ('Explain how decisions at the margin are made by consumers and by firms.',
     'Consumers compare MU/MB with price; firms compare MR with MC; continue while MB ≥ MC; net benefit maximised where MB = MC; example.',
     'people in reality rarely make decisions at the margin',
     'Habits, rules of thumb, limited information and bounded rationality; large indivisible decisions; emotions.',
     'Many everyday decisions (an extra hour of work, one more item) are marginal; firms use marginal costing; outcome is consistent with marginal reasoning even if not calculated.'),
])
CHAPTERS[2] = [t2_1, t2_2, t2_3, t2_4]

# ============================================================================ 3 Factors of production
t3_1 = T('Land, labour, capital and enterprise and their rewards', 'land, labour, capital and enterprise', 'factors of production', 'rewards')
mc(t3_1, [
    ('What is the reward to the factor of production land?', 'Rent', 'Land → rent; labour → wages; capital → interest; enterprise → profit.', ['Wages', 'Interest', 'Profit']),
    ('What is the reward to enterprise?', 'Profit', 'Entrepreneurs bear risk and receive profit.', ['Rent', 'Interest', 'Wages']),
    ('Which is an example of capital as a factor of production?', 'A delivery van used by a firm', 'Capital = man-made goods used to produce other goods and services.',
     ['Money saved in a bank account', 'A field used for crops', 'The skills of a teacher']),
    ('Which is an example of land as a factor of production?', 'Fish in the sea', 'Land = all natural resources: soil, minerals, fish, forests.', ['A fishing boat', 'A fisherman', 'A fish-processing factory']),
    ('What is meant by investment in economics?', 'Spending on capital goods that will be used to produce goods and services in the future', 'Investment = addition to the capital stock.',
     ['Buying shares in a company', 'Saving money in a bank', 'Buying a second-hand house to live in']),
    ('What is the reward to capital?', 'Interest', 'Capital earns interest.', ['Rent', 'Profit', 'Wages']),
    ('What is meant by the mobility of labour?', 'The ease with which workers can change jobs or move location', 'Occupational and geographical mobility.',
     ['The number of workers in the labour force', 'The speed at which workers produce output', 'The movement of capital between countries']),
])
ex(t3_1, [
    ('Explain the difference between capital and enterprise as factors of production.', 'Capital is man-made goods (machines, buildings) used to produce other goods; enterprise is the willingness and ability to organise the other factors and take risks in production.',
     '1 mark: capital definition; 1 mark: enterprise definition [2]'),
    ('Explain why the quality of labour, not only its quantity, matters for an economy’s output.', 'Better educated, trained and healthier workers are more productive, so the same number of workers can produce more output.',
     '1 mark: quality = skills/health; 1 mark: higher productivity/output [2]'),
    ('Explain two reasons why labour may be geographically immobile.', 'Differences in housing costs between regions, family and social ties, cost of moving, lack of information about jobs.',
     '1 mark each reason explained [2]'),
    ('Explain why money is not regarded as a factor of production.', 'Money cannot itself produce goods; it is a means of buying the factors (e.g. capital equipment) that do.', '1 mark: money not productive; 1 mark: used to acquire factors [2]'),
])
FOP_CASES = [
    ('A forest in {country} that is cut for timber.', 'Land', 'a natural resource; earns rent.'),
    ('A nurse working in a hospital in {city}.', 'Labour', 'human effort; earns wages.'),
    ('A crane used to unload ships at the port of {city}.', 'Capital', 'a man-made good used to produce services; earns interest.'),
    ('{person}, who risks her savings to start a {good} business.', 'Enterprise', 'organises factors and bears risk; earns profit.'),
    ('Copper deposits being mined in {country}.', 'Land', 'a natural resource; earns rent.'),
    ('The computers used by software engineers at {firm}.', 'Capital', 'man-made equipment used in production; earns interest.'),
    ('The farm workers who pick fruit in {country}.', 'Labour', 'human effort; earns wages.'),
    ('{person}, who designs and launches a new app and takes the financial risk.', 'Enterprise', 'innovation and risk-bearing; earns profit.'),
    ('The river water used to cool a power station in {country}.', 'Land', 'a natural resource.'),
]
classify(t3_1, FOP_CASES, ['Land', 'Labour', 'Capital', 'Enterprise'], 'Which factor of production is this?',
         'Identify the factor of production in each case and state its reward.')
items(t3_1, 'C2', (1, 2, 3, 4), [
    ('Many skilled nurses have emigrated from {country}. Explain how this affects the quantity and quality of labour in {country}.', 'The labour force is smaller and the average level of skill falls, reducing productive potential, especially in healthcare.', '1 mark: quantity falls; 1 mark: quality/skills fall [2]'),
    ('{firm} has bought new machines for its factory in {city}. Explain why this is described as investment.', 'It adds to the capital stock, raising future capacity to produce {mgood}.', '1 mark: capital goods; 1 mark: future production [2]'),
])
errs(t3_1, [
    ('Money in a bank is capital because firms use it to buy machines.', 'Capital is the man-made goods (machines, buildings) used in production; money is only a claim on resources, not a factor of production.'),
    ('Buying shares in {firm} is investment in the economic sense.', 'Buying existing shares is a financial transfer; investment in economics is spending on new capital goods.'),
    ('The reward to land is interest.', 'Land earns rent; capital earns interest.'),
])


@t3_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t3_1_income(r, D):
    p = person(r)
    w = r.choice([18000, 24000, 30000, 36000])
    rent = r.choice([3000, 4800, 6000, 7200])
    dep = r.choice([10000, 20000, 25000, 40000])
    rate = r.choice([2, 3, 4, 5])
    prof = r.choice([5000, 8000, 12000, 15000])
    inte = dep * rate / 100
    tot = w + rent + inte + prof
    stem = (f'In one year {p} earns ${w:,} as a teacher, receives ${rent:,} from renting out a field, earns {rate}% interest on ${dep:,} lent to a business and makes ${prof:,} profit from a small online shop.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the income earned from capital.', money(inte), f'{rate}% × {dep:,} = {money(inte)} (interest is the reward to capital).', dis_num(r, inte, money, [rent, prof, dep]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the total factor income and the share coming from enterprise. (b) Identify the factor of production that each income rewards.',
            'answer': f'(a) Total = {money(tot)}; enterprise share = {pct(100 * prof / tot)}. (b) Wage → labour; rent → land; interest → capital; profit → enterprise.',
            'key': f'(a) {w} + {rent} + {num(inte)} + {prof} = {num(tot)} [1]; {prof}/{num(tot)} × 100 = {pct(100 * prof / tot)} [1] (b) all four rewards correctly matched [2] [4]', 'marks': 4, 'type': 'numerical'}


t3_2 = T('Division of labour and specialisation: benefits and drawbacks', 'division of labour', 'specialisation')
mc(t3_2, [
    ('What is meant by the division of labour?', 'Breaking down production into separate tasks, each carried out by different workers', 'Workers specialise in particular tasks.',
     ['Dividing workers into skilled and unskilled groups', 'Sharing jobs between part-time workers', 'Allocating workers between firms by the government']),
    ('Which is a benefit of the division of labour?', 'Workers become more skilled at their task, raising productivity', 'Practice makes perfect; less time lost switching tasks; specialised machinery.',
     ['Workers find their jobs more varied', 'Firms become less dependent on each worker', 'Output falls but quality rises']),
    ('Which is a drawback of the division of labour for workers?', 'Repetitive tasks can cause boredom and lower motivation', 'Monotony, deskilling, risk of structural unemployment.',
     ['Workers become more productive', 'Workers earn higher wages', 'Workers learn specialised skills']),
    ('Why does specialisation require a system of exchange?', 'Specialists produce more of one good than they need and must trade for other goods', 'Specialisation → surplus → exchange, ideally with money as a medium.',
     ['Because specialists produce everything they need', 'Because governments ban self-sufficiency', 'Because prices are fixed']),
    ('What limits the extent of the division of labour?', 'The size of the market', 'Small markets cannot absorb the large output of highly specialised production.',
     ['The number of currencies', 'The rate of interest', 'The level of tariffs abroad']),
])
ex(t3_2, [
    ('Explain two reasons why the division of labour increases labour productivity.', 'Workers become skilled through repetition; less time is lost moving between tasks; it allows use of specialised machinery; workers can be matched to tasks they are best at.',
     '1 mark each reason explained [4]'),
    ('Explain why a high degree of specialisation can make a firm vulnerable.', 'Production depends on every stage; if one group of workers is absent or on strike, the whole process stops.', '1 mark: interdependence; 1 mark: disruption halts production [2]'),
    ('Explain why money is important for specialisation in an economy.', 'Money acts as a medium of exchange, removing the need for a double coincidence of wants, so specialists can easily sell their output and buy what they need.',
     '1 mark: medium of exchange; 1 mark: removes barter problem, enables trade [2]'),
])
items(t3_2, 'C2', (1, 2, 3, 4), [
    ('{firm} reorganises its {mgood} factory in {city} so that each worker does a single task. Explain one benefit and one drawback for {firm}.', 'Benefit: higher productivity, lower unit costs. Drawback: boredom and lower motivation, higher absence/labour turnover, or disruption if one stage stops.', '1 mark: benefit; 1 mark: drawback [2]'),
    ('{country} specialises in producing {mgood} for export. Explain one risk to {country} of this specialisation.', 'If world demand or price for {mgood} falls, incomes and jobs in {country} fall sharply because it depends heavily on one product.', '1 mark: dependence; 1 mark: effect of a fall in demand/price [2]'),
])
errs(t3_2, [
    ('Specialisation always benefits workers because they become more skilled.', 'Workers may become skilled at a narrow task, but jobs become repetitive and they may find it harder to change job if demand falls (structural unemployment).'),
    ('The division of labour means that each worker makes a whole product from start to finish.', 'Division of labour means production is split into separate tasks, each done by different workers.'),
])


@t3_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t3_2_prod(r, D):
    f = r.choice(FIRMS)
    g = r.choice(['chairs', 'shirts', 'pairs of shoes', 'bicycles', 'tables', 'cakes'])
    n = r.choice([4, 5, 6, 8])
    each = r.choice([3, 4, 5, 6])
    spec = n * each * r.choice([1.5, 1.6, 1.75, 2, 2.5])
    if abs(spec - round(spec)) > 1e-9:
        return None
    spec = int(spec)
    p0, p1 = each, spec / n
    stem = f'At {f}, {n} workers each make complete {g}, producing {each} a day each. After reorganising so each worker specialises in one task, the team makes {spec} {g} a day.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the percentage increase in output per worker.', pct(chg(p0, p1)), f'Before {p0}; after {spec}/{n} = {r2(p1)}; ({r2(p1)} − {p0})/{p0} × 100 = {pct(chg(p0, p1))}.',
                  dis_num(r, chg(p0, p1), pct, [spec - n * each, 100 * spec / (n * each)]), mcq_D=(1, 2))
    wage = r.choice([40, 50, 60])
    return {'stem': stem + f' Each worker is paid ${wage} a day. (a) Calculate output per worker and the labour cost per unit before and after. (b) Explain why output per worker rose. (c) Explain one possible drawback of the change for {f}.',
            'answer': f'(a) Output per worker {p0} → {r2(p1)}; labour cost per unit {money(wage / p0)} → {money(wage / p1)}. (b) Workers become quicker and more skilled at one task, no time lost switching tasks, specialist tools. (c) Boredom/low motivation, absenteeism or disruption if one stage stops.',
            'key': f'(a) output per worker both [1]; cost per unit {wage}/{p0} and {wage}/{r2(p1)} [2] (b) reason [1] (c) drawback [1] [5]', 'marks': 5, 'type': 'multi_step'}


t3_3 = T('The role of the entrepreneur and risk-taking', 'entrepreneur', 'risk-taking')
mc(t3_3, [
    ('What is the main role of the entrepreneur?', 'To organise the other factors of production and bear the risk of the business', 'Organising, decision-making, risk-bearing, innovation.',
     ['To lend money to firms', 'To supply labour in return for wages', 'To set prices for the government']),
    ('Why is profit regarded as a reward for enterprise?', 'It compensates the entrepreneur for bearing uninsurable risk', 'Uncertainty cannot be insured, so profit rewards risk-bearing.',
     ['It is fixed by contract like wages', 'It is guaranteed by the government', 'It is the same as interest on capital']),
    ('Which risk faced by an entrepreneur is uninsurable?', 'A fall in demand caused by a change in consumer tastes', 'Market risks cannot be insured; fire or theft can.',
     ['Fire damage to the factory', 'Theft of stock', 'Injury to an employee']),
    ('Which characteristic is most associated with entrepreneurs?', 'Willingness to take risks and innovate', 'Enterprise involves risk-taking and new ideas.',
     ['Preference for a fixed salary', 'Avoidance of all uncertainty', 'Working only for large firms']),
    ('In a planned economy, who takes most of the decisions made by entrepreneurs in a market economy?', 'The state', 'State planners decide what, how and for whom.',
     ['Consumers', 'Trade unions', 'Foreign firms']),
])
ex(t3_3, [
    ('Explain why entrepreneurs are important for economic growth.', 'They bring new products and production methods to market, create firms and jobs and raise productivity through innovation, increasing the economy’s productive capacity.',
     '1 mark: innovation/new firms; 1 mark: link to output/growth [2]'),
    ('Explain the difference between insurable and uninsurable risk faced by an entrepreneur.', 'Insurable risks (fire, theft) can be statistically predicted and covered by insurance; uninsurable risks (changes in demand, new competitors) cannot, and profit is the reward for bearing them.',
     '1 mark: insurable defined; 1 mark: uninsurable defined and linked to profit [2]'),
    ('Explain why some entrepreneurs continue in business even when making a loss for a period.', 'They expect future profits, e.g. once the brand is established or demand recovers; they may value independence or have sunk costs.', '1 mark: expectation of future profit; 1 mark: other reason [2]'),
])
items(t3_3, 'C2', (1, 2, 3, 4), [
    ('{person} leaves a salaried job to open a {good} shop in {city}. Explain the risks {person} is taking as an entrepreneur.', 'Loss of a secure salary (opportunity cost), risk of losing invested savings if demand is too low or costs too high; income is uncertain profit rather than fixed wages.', '1 mark: forgone salary; 1 mark: uncertain profit/loss of capital [2]'),
    ('The government of {country} offers start-up loans to young entrepreneurs. Explain why it might do this.', 'To encourage new firms, jobs, innovation and competition; entrepreneurs often lack access to finance because banks see them as risky.', '1 mark: benefits of enterprise; 1 mark: finance barrier [2]'),
])
errs(t3_3, [
    ('An entrepreneur’s profit is guaranteed because they own the business.', 'Profit is a residual and uncertain; entrepreneurs bear the risk that revenue may not cover costs and may make losses.'),
    ('Entrepreneurs receive wages as their reward.', 'The reward to enterprise is profit, which is uncertain; wages are the reward to labour.'),
])


@t3_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t3_3_profit(r, D):
    p = person(r)
    g = r.choice(GOODS)
    price = r.choice([4, 5, 6, 8, 10, 12])
    q = r.choice([800, 1000, 1200, 1500, 2000])
    vc = price * r.choice([0.4, 0.5, 0.6])
    fixed = r.choice([2000, 3000, 4000])
    sal = r.choice([2500, 3000, 3500])
    tr = price * q
    tc = vc * q + fixed
    pr = tr - tc
    stem = (f'{p} runs a business selling {g}. In one month {p} sells {q:,} units at ${price} each. Variable costs are ${r2(vc)} per unit and fixed costs are ${fixed:,}. '
            f'{p} gave up a job paying ${sal:,} a month to run the business.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the monthly accounting profit.', money(pr), f'TR {num(tr)} − TC ({r2(vc)} × {q} + {fixed}) = {money(pr)}.', dis_num(r, pr, money, [tr - fixed, tr - vc * q, pr - sal]), mcq_D=(1, 2))
    ep = pr - sal
    return {'stem': stem + ' (a) Calculate the monthly profit. (b) Taking into account the opportunity cost of the job given up, explain whether running the business is worthwhile. (c) Explain why profit is the reward for the risk taken by ' + p + '.',
            'answer': f'(a) {money(pr)} (b) After deducting the forgone salary of ${sal:,} the gain is {money(ep)}: ' + ('worthwhile, it earns more than the next best alternative.' if ep > 0 else 'not worthwhile in money terms, it earns less than the job forgone (unless non-money benefits or future growth justify it).') + ' (c) Revenue is uncertain; profit compensates for the uninsurable risk of loss.',
            'key': f'(a) TR − TC = {num(pr)} [2] (b) compares with ${sal:,} forgone [1]; conclusion [1] (c) uncertainty/risk [1] [5]', 'marks': 5, 'type': 'multi_step'}


def _ch3_case(r, D):
    d = ctx(r)
    w0, w1 = r.choice([(20, 12), (30, 18), (40, 25)])
    o0, o1 = r.choice([(500, 900), (600, 1200), (400, 700)])
    intro = (f'Extract: {d["firm"]} makes {d["mgood"]} in {d["city"]}. Five years ago it employed {w0} craft workers who each made complete products. '
             f'It now employs {w1} workers on a production line, each doing one task, with new machinery. Monthly output has risen from {o0} to {o1} units. '
             f'The founder, {d["person"]}, says the change was a risk because she borrowed heavily to buy the machines.')
    pw0, pw1 = o0 / w0, o1 / w1
    parts = [
        lambda r: ('Calculate output per worker before and after the change.', f'{r1(pw0)} → {r1(pw1)} units', f'{o0}/{w0} and {o1}/{w1} [2]'),
        lambda r: ('Identify two factors of production mentioned in the extract and their rewards.', 'Labour (workers) → wages; capital (machinery) → interest; enterprise (the founder) → profit.', '1 mark each factor with reward [2]'),
        lambda r: ('Explain why the division of labour raised productivity.', 'Repetition builds skill and speed; no time lost changing tasks; enables specialised machinery.', '[3]'),
        lambda r: ('Explain the risk taken by the founder as an entrepreneur.', 'Borrowing to buy machines commits the firm to interest payments; if demand falls she may make losses and lose her capital.', '[2]'),
        lambda r: ('Discuss whether the workers have benefited from the change.', 'Fewer jobs (some made redundant), repetitive tasks, deskilling vs possibly higher wages from higher productivity, safer work, job security if the firm is more competitive; judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t3_1, t3_2, t3_3], _ch3_case)
essay(t3_1, [
    ('Explain the four factors of production and the reward each one earns.',
     'Land (natural resources) → rent; labour (human effort) → wages; capital (man-made aids) → interest; enterprise (organisation, risk) → profit; quantity and quality.',
     'the quality of its labour force is the most important factor of production for {country}',
     'Human capital raises productivity, drives innovation, attracts FDI; skills needed to use capital.',
     'Capital and technology raise output per worker; natural resources can be decisive (oil); enterprise organises the rest; all are complementary.'),
], ['{country} has few natural resources but has invested heavily in education.'])
essay(t3_2, [
    ('Explain how the division of labour can increase productivity.',
     'Skill through repetition, time saving, use of specialist machinery, matching aptitudes; leads to lower unit costs; requires a large enough market and exchange.',
     'the benefits of specialisation outweigh its drawbacks for workers and firms',
     'Higher productivity, lower costs, higher wages and competitiveness.',
     'Boredom, alienation, deskilling, interdependence and disruption, structural unemployment risk; depends on job design and the market.'),
])
essay(t3_3, [
    ('Explain the role of the entrepreneur in a market economy.',
     'Organises land, labour and capital; takes decisions; bears uninsurable risk; innovates; rewarded by profit; signals from prices.',
     'governments in {country} should actively encourage entrepreneurship',
     'New firms create jobs, competition, innovation and growth; market failures in start-up finance and information.',
     'Many start-ups fail; government may pick losers; subsidies have an opportunity cost; better to remove barriers (red tape) than subsidise; depends on design.'),
])
CHAPTERS[3] = [t3_1, t3_2, t3_3]

# ============================================================================ 4 Resource allocation in different economic systems
SYS_CASES = [
    ('In {country}, prices are set by supply and demand and almost all firms are privately owned.', 'Market economy', 'resources are allocated by the price mechanism with private ownership.'),
    ('In {country}, a central planning office decides how many tractors, flats and tonnes of steel are produced each year.', 'Planned economy', 'the state allocates resources through planning targets.'),
    ('In {country}, private firms produce most goods, but the government provides healthcare and education and regulates monopolies.', 'Mixed economy', 'both the price mechanism and government allocate resources.'),
    ('In {country}, the state owns all land and factories and workers are directed to jobs by government agencies.', 'Planned economy', 'state ownership and direction of factors.'),
    ('In {country}, most shops and farms are private, but the state runs the railways and pays unemployment benefits.', 'Mixed economy', 'a combination of private and public sectors.'),
    ('In {country}, a rise in the price of {good} quickly attracts new private firms into the industry with no government involvement.', 'Market economy', 'price signals and the profit motive guide resource allocation.'),
]
SYS_LABELS = ['Market economy', 'Planned economy', 'Mixed economy']

t4_1 = T('The market economy and the role of the price mechanism', 'market economy', 'price mechanism')
mc(t4_1, [
    ('In a market economy, how are resources allocated?', 'Through the price mechanism, by the decisions of consumers and producers', 'Market economy: private ownership, price mechanism, consumer sovereignty.',
     ['By government planning targets', 'By tradition and custom', 'By a lottery system']),
    ('What is meant by consumer sovereignty?', 'Consumers’ spending decisions determine what is produced', 'Consumers “vote” with their spending; firms respond to profit signals.',
     ['Consumers set the prices of goods', 'The government protects consumers from firms', 'Consumers own the firms that produce goods']),
    ('Which is a feature of a market economy?', 'Private ownership of most resources', 'Private property rights and the profit motive.',
     ['State ownership of all factories', 'Central planning of output', 'Prices fixed by the government']),
    ('What happens in a market economy when demand for a good rises?', 'Its price rises, signalling firms to move resources into producing it', 'Higher price → higher profit → resources reallocated.',
     ['The government orders more to be produced', 'Its price falls', 'Firms leave the industry']),
    ('Which is a disadvantage of a market economy?', 'Public goods are likely not to be provided', 'Market failure: public goods, externalities, inequality.',
     ['Firms have no incentive to be efficient', 'Consumers have little choice', 'Prices do not respond to demand']),
    ('What is the main motive that guides firms in a market economy?', 'The profit motive', 'Firms seek profit, so they produce what consumers will buy.', ['Planning targets', 'Social welfare', 'Tradition']),
])
ex(t4_1, [
    ('Explain how the price mechanism allocates resources in a market economy.', 'Changes in demand and supply change prices; higher prices signal scarcity and raise profits, giving firms an incentive to move resources into that market, while falling prices cause resources to leave. Prices also ration goods to those willing and able to pay.',
     '1 mark: price changes as signal; 1 mark: incentive/profit; 1 mark: reallocation of resources/rationing [3]'),
    ('Explain two advantages of a market economy.', 'Efficiency: competition and the profit motive encourage low costs and innovation. Choice: consumer sovereignty means firms produce what consumers want. Also: no costly planning bureaucracy; quick response to change.',
     '1 mark each advantage, 1 mark each explained [4]'),
    ('Explain why a pure market economy may lead to an unequal distribution of income.', 'Incomes depend on ownership of factors and their market value; those with valuable skills or wealth earn much more, and there is no government redistribution.',
     '1 mark: incomes reflect factor ownership/market value; 1 mark: no redistribution [2]'),
])
items(t4_1, 'C2', (1, 2, 3, 4), [
    ('Demand for electric cars in {country} rises sharply. Explain how the price mechanism reallocates resources in a market economy.', 'Price of electric cars rises; producers’ profits rise, so they expand output and new firms enter, attracting labour and capital from less profitable industries such as petrol cars.', '1 mark: price rises; 1 mark: profit incentive; 1 mark: resources move [3]'),
    ('Explain why a market economy in {country} might fail to provide enough street lighting.', 'Street lighting is a public good: non-excludable, so consumers can free ride; firms cannot charge for it, so there is no profit incentive to supply it.', '1 mark: public good/free rider; 1 mark: no profit incentive [2]'),
])
errs(t4_1, [
    ('In a market economy the government decides what goods are produced.', 'In a market economy consumers and firms decide through the price mechanism; government plays a minimal role.'),
    ('Consumer sovereignty means that consumers set the prices of goods.', 'It means consumers’ spending decisions determine what is produced; prices are set by the interaction of demand and supply.'),
])
classify(t4_1, SYS_CASES, SYS_LABELS, 'Which type of economic system does this describe?', 'Identify the economic system described in each case and explain your answer.', extra=['Traditional economy'], name='systems')


@t4_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t4_1_signal(r, D):
    c = r.choice(COUNTRIES)
    g1, g2 = r.sample(['solar panels', 'diesel generators', 'plant-based milk', 'dairy milk', 'e-books', 'printed books', 'electric bicycles', 'petrol scooters'], 2)
    p0, p1 = r.choice([(200, 260), (40, 50), (80, 96), (12, 15)])
    q0, q1 = r.choice([(10, 14), (5, 8), (20, 26)])
    ac = p0 * r.choice([0.8, 0.85, 0.9])
    pr0 = (p0 - ac) * q0
    pr1 = (p1 - ac) * q1
    stem = (f'In {c}, the price of {g1} rose from ${p0} to ${p1} and sales rose from {q0} to {q1} thousand units, while demand for {g2} fell. '
            f'The average cost of producing {g1} stayed at {money(ac)} per unit.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the percentage increase in the price of ' + g1 + '.', pct(chg(p0, p1)), f'({p1} − {p0})/{p0} × 100 = {pct(chg(p0, p1))}.', dis_num(r, chg(p0, p1), pct, [chg(q0, q1), p1 - p0]), mcq_D=(1, 2))
    return {'stem': stem + f' (a) Calculate the total profit from {g1} before and after the change (in thousands of dollars). (b) Explain how the price mechanism will reallocate resources between {g1} and {g2}.',
            'answer': f'(a) Before: ${num(pr0)}k; after: ${num(pr1)}k. (b) Higher profit signals that consumers want more {g1} and gives firms an incentive to expand output and enter the industry; falling demand and profit for {g2} lead resources to leave that industry and move to {g1}.',
            'key': f'(a) (P − AC) × Q each [2] (b) signalling [1]; incentive [1]; resources move between markets [1] [5]', 'marks': 5, 'type': 'multi_step'}


t4_2 = T('The planned economy: state allocation of resources', 'planned economy', 'state allocation')
mc(t4_2, [
    ('In a planned economy, who decides what to produce?', 'The state (government planners)', 'Central planning; state ownership of resources.', ['Consumers through their spending', 'Private firms seeking profit', 'Trade unions']),
    ('Which is an advantage claimed for a planned economy?', 'A more equal distribution of income', 'Planners can prioritise basic needs and equality.',
     ['Strong incentives for innovation', 'Wide consumer choice', 'Prices that respond quickly to demand']),
    ('Which problem is often found in planned economies?', 'Shortages and queues for many consumer goods', 'Prices fixed below market levels; poor information for planners.',
     ['Too much consumer choice', 'High unemployment from the trade cycle', 'Under-provision of public goods']),
    ('Why do planned economies often suffer from low efficiency?', 'Managers have weak incentives to cut costs or innovate', 'No profit motive or competition; targets rather than efficiency.',
     ['Prices are too high', 'Firms compete too fiercely', 'Consumers are sovereign']),
    ('What is the main information problem facing central planners?', 'They cannot know the preferences of millions of consumers or the costs of all producers', 'Without prices, information about scarcity is lacking.',
     ['They have too much data from markets', 'Consumers report their preferences accurately', 'Prices give too many signals']),
])
ex(t4_2, [
    ('Explain two disadvantages of a planned economy.', 'Lack of incentives (no profit motive) leads to low efficiency and innovation; planners lack information so produce the wrong goods, causing shortages and surpluses; little consumer choice; large bureaucracy.',
     '1 mark each disadvantage, 1 mark each explained [4]'),
    ('Explain why a planned economy might achieve lower unemployment than a market economy.', 'The state directs workers into jobs and sets output targets regardless of demand, so jobs are guaranteed even when they are not efficient.',
     '1 mark: state allocates jobs; 1 mark: not dependent on market demand [2]'),
    ('Explain how shortages arise when prices are fixed by planners.', 'If the fixed price is below the price at which demand equals supply, quantity demanded exceeds quantity supplied, leading to queues, rationing and black markets.',
     '1 mark: price below equilibrium; 1 mark: excess demand/queues [2]'),
])
items(t4_2, 'C2', (1, 2, 3, 4), [
    ('Planners in {country} set a target for factories to produce a fixed weight of nails each month. Explain why this might result in goods that consumers do not want.', 'Factories meet the weight target by making a few very heavy nails rather than the sizes consumers need, because targets reward quantity rather than usefulness.', '1 mark: targets not linked to demand; 1 mark: mismatch [2]'),
    ('Explain why the government of {country}, a planned economy, may find it easier to build large infrastructure projects than a market economy.', 'The state controls resources directly and can direct labour and capital to priority projects without needing profit or private finance.', '1 mark: direct control; 1 mark: no profit requirement [2]'),
])
errs(t4_2, [
    ('In a planned economy there is no scarcity because the state provides everything.', 'Resources are still scarce; the state simply decides how to allocate them, often causing shortages.'),
    ('Planned economies always have more efficient firms because there is no wasteful competition.', 'Without competition and the profit motive firms have weak incentives to cut costs or innovate, so they tend to be less efficient.'),
])
classify(t4_2, SYS_CASES, SYS_LABELS, 'Which type of economic system does this describe?', 'Identify the economic system described in each case and explain your answer.', extra=['Traditional economy'], name='systems')


@t4_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t4_2_short(r, D):
    c = r.choice(COUNTRIES)
    g = r.choice(['flats', 'cars', 'refrigerators', 'televisions', 'washing machines'])
    plan = r.choice([200, 250, 300, 400])
    want = int(plan * r.choice([1.3, 1.5, 1.6, 1.8, 2.0]))
    stem = f'Planners in {c} set the price of {g} below the market level. At this price {want} thousand households want to buy {g} each year, but the plan provides only {plan} thousand.'
    sh = want - plan
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the shortage as a percentage of the quantity supplied.', pct(100 * sh / plan), f'Shortage = {sh}; {sh}/{plan} × 100.',
                  dis_num(r, 100 * sh / plan, pct, [100 * sh / want, sh]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the shortage. (b) Explain two ways in which the shortage might be dealt with, and one likely consequence.',
            'answer': f'(a) {sh} thousand units. (b) Queuing (first come, first served), waiting lists, rationing by allocation or vouchers, priority by need; consequence: black markets selling at higher prices, or time wasted queuing.',
            'key': f'(a) {want} − {plan} = {sh} [1] (b) two allocation methods [2]; consequence [1] [4]', 'marks': 4, 'type': 'numerical'}


t4_3 = T('The mixed economy and the problems of transition', 'mixed economy', 'transition', 'privatisation')
mc(t4_3, [
    ('What is a mixed economy?', 'An economy in which resources are allocated partly by the price mechanism and partly by the government', 'Mixed: private and public sectors coexist.',
     ['An economy that trades with many countries', 'An economy that produces both goods and services', 'An economy with both rich and poor people']),
    ('Which is a problem commonly faced by an economy in transition from planned to market?', 'Unemployment rises as inefficient state firms close', 'Transition: unemployment, inflation when prices are freed, inequality, weak institutions.',
     ['Prices fall sharply as controls are removed', 'Government spending rises to 100% of GDP', 'Consumer choice falls']),
    ('Why does inflation often rise during transition to a market economy?', 'Price controls are removed and prices rise to market levels', 'Previously suppressed prices adjust upwards.',
     ['The government fixes all wages', 'Output rises very quickly', 'Imports are banned']),
    ('Which is an example of a policy used in transition to a market economy?', 'Privatisation of state-owned enterprises', 'Privatisation, price liberalisation, trade liberalisation.',
     ['Nationalisation of private firms', 'Introducing central planning targets', 'Banning foreign investment']),
    ('Why do most real-world economies have a mix of private and public sectors?', 'Markets fail to provide some goods and services and governments want to correct this', 'Market failure and equity motives justify a role for government.',
     ['Governments must own all firms by international law', 'Private firms never make profits', 'Planning has no disadvantages']),
])
ex(t4_3, [
    ('Explain two problems that may occur when a planned economy changes to a market economy.', 'Unemployment as inefficient state firms close; inflation as price controls end; rising inequality; lack of legal and financial institutions (property rights, banks); corruption in privatisation.',
     '1 mark each problem, 1 mark each explained [4]'),
    ('Explain why governments in mixed economies provide some goods and services directly.', 'Public goods would not be provided by the market; merit goods would be under-consumed; equity of access to health and education.',
     '1 mark: market failure reason; 1 mark: equity reason [2]'),
    ('Explain why the balance between the public and private sectors differs between mixed economies.', 'It reflects political values and choices about the role of the state, the extent of market failure and views on equity versus efficiency.', '1 mark: political/normative choices; 1 mark: market failure/equity [2]'),
])
items(t4_3, 'C2', (1, 2, 3, 4), [
    ('{country} is moving from a planned to a market economy. Explain why unemployment may rise in the first few years.', 'Inefficient state firms lose subsidies and face competition, so many close or cut jobs; new private firms take time to grow; workers lack the skills new firms need.', '1 mark: closure of inefficient state firms; 1 mark: slow growth of private sector/skills mismatch [2]'),
    ('The government of {country} privatises its state-owned {ind} company. Explain one possible benefit and one possible cost.', 'Benefit: profit motive raises efficiency and investment. Cost: a private monopoly may raise prices or cut unprofitable services; job losses.', '1 mark: benefit; 1 mark: cost [2]'),
])
errs(t4_3, [
    ('A mixed economy is one that produces both agricultural and manufactured goods.', 'A mixed economy is one where resources are allocated partly by the market and partly by the government.'),
    ('Moving to a market economy always makes everyone better off immediately.', 'Transition often brings unemployment, inflation and inequality in the short run; gains in efficiency and choice take time.'),
])
classify(t4_3, SYS_CASES, SYS_LABELS, 'Which type of economic system does this describe?', 'Identify the economic system described in each case and explain your answer.', extra=['Traditional economy'], name='systems')


@t4_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t4_3_trans(r, D):
    c = r.choice(COUNTRIES)
    s0, s1 = r.choice([(80, 45), (75, 40), (90, 55), (70, 35)])
    u0, u1 = r.choice([(2, 9), (1.5, 8), (3, 11)])
    i0, i1 = r.choice([(3, 25), (4, 40), (2, 18)])
    tab = table(['', 'Year 1', 'Year 5'], [('State sector share of output (%)', s0, s1), ('Unemployment rate (%)', u0, u1), ('Inflation (%)', i0, i1)])
    stem = f'{c} began moving from a planned to a market economy in Year 1. {tab}.'
    if D <= 2:
        return cq(r, 1, stem + ' By how many percentage points did the state sector’s share of output fall?', f'{s0 - s1} percentage points', f'{s0} − {s1} = {s0 - s1}.',
                  [f'{x} percentage points' for x in (s1, round(100 * (s0 - s1) / s0), s0, u1 - u0)], mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the percentage fall in the state sector’s share of output. (b) Using the data, explain two problems of transition. (c) Suggest why these problems might be temporary.',
            'answer': f'(a) {pct(100 * (s0 - s1) / s0)} (b) Unemployment rose from {u0}% to {u1}% as state firms closed; inflation rose from {i0}% to {i1}% as price controls ended. (c) New private firms expand and absorb workers; once prices reach market levels, inflation falls; institutions develop.',
            'key': f'(a) ({s0} − {s1})/{s0} × 100 [1] (b) each problem with data [2] (c) reason [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch4_case(r, D):
    d = ctx(r)
    g0, g1 = r.choice([(2.0, 6.5), (1.5, 5.0), (0.5, 4.5)])
    ineq0, ineq1 = r.choice([(0.25, 0.38), (0.28, 0.42), (0.22, 0.35)])
    intro = (f'Extract: Twenty years ago {d["country"]} was a centrally planned economy. Since reforms began, most state firms have been privatised and prices are set by markets. '
             f'Average annual growth has risen from {g0}% to {g1}%, and shops now offer a wide choice of goods. However, the Gini coefficient has risen from {ineq0} to {ineq1}, '
             f'and the government still runs schools, hospitals and the railway.')
    parts = [
        lambda r: ('State the type of economic system that {} has now. Give a reason.'.format(d['country']), 'Mixed economy: markets allocate most resources, but the state provides schools, hospitals and railways.', '[2]'),
        lambda r: ('Calculate the percentage increase in the Gini coefficient.', pct(chg(ineq0, ineq1)), f'({ineq1} − {ineq0})/{ineq0} × 100 [2]'),
        lambda r: ('Explain why growth may have increased after the reforms.', 'Profit motive and competition raise efficiency and innovation; resources move to where they are most valued; FDI attracted.', '[3]'),
        lambda r: ('Explain why inequality may have increased.', 'Incomes now reflect the market value of skills and ownership of capital; privatisation transferred wealth; less state wage-setting.', '[2]'),
        lambda r: ('Discuss whether the move to a market economy has been beneficial for the people of {}.'.format(d['country']), 'Growth, choice, efficiency vs inequality, insecurity, possible unemployment; state still corrects market failures; depends on who gains and on views of equity; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t4_1, t4_2, t4_3], _ch4_case)
essay(t4_1, [
    ('Explain how the price mechanism allocates resources in a market economy.',
     'Signalling, incentive and rationing functions; demand/supply changes change prices and profits; resources move; consumer sovereignty; diagram of a demand shift.',
     'a market economy is the best way to allocate scarce resources',
     'Efficiency, innovation, choice, quick response to change, no costly planning.',
     'Market failure: public goods, externalities, merit/demerit goods, inequality, monopoly power, information failure; government intervention needed; mixed economy.'),
], ['{country} has recently removed price controls on most goods.'])
essay(t4_2, [
    ('Explain how resources are allocated in a planned economy and the problems that this may cause.',
     'State ownership; planners set output targets and prices; problems: information, incentives, shortages/surpluses, bureaucracy, lack of choice.',
     'a planned economy is better at meeting basic needs than a market economy',
     'Planners can prioritise food, housing, health and education for all; full employment; equality.',
     'Inefficiency and shortages often mean basic goods are poor quality or scarce; market economies with welfare systems meet needs; incentives and growth raise living standards.'),
])
essay(t4_3, [
    ('Explain the problems that an economy may face when moving from a planned economy to a market economy.',
     'Unemployment, inflation from price liberalisation, inequality, weak institutions and property rights, corruption, loss of social services; adjustment takes time.',
     'the benefits of transition to a market economy outweigh the costs for {country}',
     'Long-run efficiency, growth, choice, FDI, innovation.',
     'Short-run costs can be severe and long-lasting; depends on speed of reform (shock therapy vs gradual), institutions and safety nets; inequality may persist.'),
], ['{country} has begun privatising its state-owned industries.'])
CHAPTERS[4] = [t4_1, t4_2, t4_3]

# ============================================================================ 5 Production possibility curves
PAIRS = [('consumer goods', 'capital goods'), ('food', 'manufactured goods'), ('healthcare', 'education'), ('wheat', 'cars'), ('agricultural goods', 'industrial goods'), ('defence', 'public services')]


t5_1 = T('Shape of the PPC: constant and increasing opportunity cost', 'shape of the ppc', 'constant and increasing opportunity cost', 'production possibility')
mc(t5_1, [
    ('What does a production possibility curve show?', 'The maximum combinations of two goods an economy can produce with all its resources fully and efficiently employed',
     'PPC: maximum output combinations given resources and technology.', ['The combinations of two goods consumers want', 'The prices of two goods', 'The actual output of an economy each year']),
    ('Why is a PPC usually drawn concave (bowed outwards) to the origin?', 'Resources are not equally suited to producing both goods, so opportunity cost increases',
     'Increasing opportunity cost: moving resources less suited to the other good.', ['Resources are equally suited to both goods', 'Technology is improving', 'There is unemployment']),
    ('What does a straight-line PPC indicate?', 'Constant opportunity cost', 'A constant slope means the same amount of Y is given up for each extra unit of X.',
     ['Increasing opportunity cost', 'Decreasing opportunity cost', 'Zero opportunity cost']),
    ('What does the slope of a PPC measure?', 'The opportunity cost of one good in terms of the other', 'Slope = ΔY/ΔX = units of Y forgone per unit of X.', ['The price of the goods', 'The rate of economic growth', 'The level of unemployment']),
    ('Moving along a concave PPC towards more of good X, what happens to the opportunity cost of X?', 'It increases', 'Each extra unit of X requires giving up more Y.', ['It falls', 'It stays the same', 'It becomes zero']),
])
ex(t5_1, [
    ('Explain why a PPC is usually concave to the origin.', 'Resources are specialised and not equally efficient in producing both goods. As more of one good is produced, resources less suited to it must be used, so increasing amounts of the other good are given up.',
     '1 mark: resources not equally suited; 1 mark: increasing opportunity cost; 1 mark: link to shape [3]'),
    ('Explain under what conditions a PPC would be a straight line.', 'If resources are equally productive in both uses, each extra unit of one good always costs the same amount of the other, giving constant opportunity cost.',
     '1 mark: resources equally suited; 1 mark: constant opportunity cost [2]'),
    ('Explain how a PPC illustrates the concepts of scarcity, choice and opportunity cost.', 'Scarcity: points beyond the curve are unattainable. Choice: the economy must choose a point on the curve. Opportunity cost: moving along it means giving up some of one good to get more of the other.',
     '1 mark each concept linked to the PPC [3]'),
])
items(t5_1, 'C2', (1, 2, 3, 4), [
    ('{country} moves resources from producing {mgood} to producing {mgood2}. Using a PPC, explain why the opportunity cost of extra {mgood2} rises as more is produced.', 'Workers and machines best suited to {mgood2} move first; later the resources moved are less suited, so more {mgood} must be given up for each extra unit of {mgood2}: a concave PPC.', '1 mark: resources not equally suited; 1 mark: rising sacrifice/concave PPC [2]'),
])
errs(t5_1, [
    ('A concave PPC shows that the opportunity cost of producing more of a good falls as more is produced.', 'A concave PPC shows increasing opportunity cost: more of the other good must be given up for each extra unit.'),
    ('The PPC shows the combinations of goods that consumers want to buy.', 'It shows the maximum combinations an economy can produce with its resources and technology, not consumer preferences.'),
])


@t5_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5_1_table(r, D):
    x, y = r.choice(PAIRS)
    c = r.choice(COUNTRIES)
    inc = r.random() < 0.7 or D >= 4
    step = r.choice([10, 20, 25, 50])
    if inc:
        losses = sorted(r.sample([1, 2, 3, 4, 5, 6], 4))
        losses = [l * step for l in losses]
    else:
        losses = [r.choice([2, 3, 4]) * step] * 4
    dx = r.choice([10, 20, 50, 100])
    ys = [sum(losses)]
    for l in losses:
        ys.append(ys[-1] - l)
    xs = [i * dx for i in range(5)]
    tab = table(['Combination', f'{x} (units)', f'{y} (units)'], list(zip('ABCDE', xs, ys)))
    i = r.randint(0, 3)
    oc = losses[i] / dx
    stem = f'The table shows the production possibilities of {c}. {tab}.'
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the opportunity cost of one unit of {x} when moving from {"ABCDE"[i]} to {"ABCDE"[i + 1]}.', f'{r2(oc)} units of {y}',
                  f'Δ{y} = {losses[i]}, Δ{x} = {dx}; {losses[i]}/{dx} = {r2(oc)}.', [f'{r2(v)} units of {y}' for v in (dx / losses[i], losses[i], oc * 2, ys[i + 1] / xs[i + 1])], mcq_D=(1, 2))
    ocs = [l / dx for l in losses]
    shape = 'increasing' if inc else 'constant'
    return {'stem': stem + f' (a) Calculate the opportunity cost of one unit of {x} for each move from A to E. (b) State whether opportunity cost is constant or increasing and describe the shape of the PPC. (c) Explain why it has this shape.',
            'answer': f'(a) {", ".join(r2(o) for o in ocs)} units of {y} per unit of {x}. (b) {shape.capitalize()} opportunity cost; ' + ('concave (bowed outwards) PPC.' if inc else 'straight-line PPC.') +
                      (' (c) Resources are not equally suited to both goods, so increasingly unsuitable resources are moved.' if inc else ' (c) Resources are equally suited to both goods.'),
            'key': '(a) all four values [2] (b) shape [1] (c) reason [1] [4]', 'marks': 4, 'type': 'numerical'}


t5_2 = T('Points inside, on and beyond the PPC: efficiency and unemployment of resources', 'points inside, on and beyond the ppc', 'efficiency and unemployment of resources', 'inside the ppc')
mc(t5_2, [
    ('What does a point inside a PPC show?', 'Some resources are unemployed or used inefficiently', 'Inside: under-utilisation; output could rise without giving up anything.',
     ['The economy is producing at full capacity', 'An output that cannot be reached', 'Economic growth']),
    ('What does a point beyond the PPC show?', 'An output combination that is unattainable with current resources and technology', 'Beyond: unattainable (in the absence of trade or growth).',
     ['Unemployment of resources', 'Productive efficiency', 'A recession']),
    ('Why do all points on the PPC represent productive efficiency?', 'More of one good cannot be produced without producing less of the other', 'On the curve: resources fully and efficiently used.',
     ['Every point gives the same total output', 'Consumers are equally happy at each point', 'Prices are equal at each point']),
    ('A movement from a point inside the PPC to a point on it, during a recovery, shows', 'a fall in unemployment of resources', 'Using idle resources; actual growth.', ['an outward shift of the PPC', 'an increase in opportunity cost', 'a fall in productive capacity']),
    ('What is the opportunity cost of moving from a point inside the PPC to a point on the curve with more of both goods?', 'Zero', 'Idle resources are brought into use; nothing is given up.', ['The goods produced', 'The cost of the resources used', 'The slope of the PPC']),
])
ex(t5_2, [
    ('Explain why a recession might be shown by a point inside a PPC.', 'In a recession output falls and workers and machines are unemployed, so the economy produces less than it could; it is inside the curve.',
     '1 mark: unemployed resources; 1 mark: output below potential [2]'),
    ('Explain why moving from inside the PPC to the curve has no opportunity cost.', 'The extra output comes from previously unused resources, so no production of the other good has to be given up.', '1 mark: idle resources used; 1 mark: nothing given up [2]'),
    ('Explain how international trade could allow a country to consume at a point beyond its PPC.', 'By specialising according to comparative advantage and trading, the country can import goods at a lower opportunity cost than producing them, so consumption exceeds what it could produce alone.',
     '1 mark: specialisation and trade; 1 mark: consumption beyond production possibilities [2]'),
])
items(t5_2, 'C2', (1, 2, 3, 4), [
    ('Unemployment in {country} has risen to 12%. Explain how this would be shown on {country}’s PPC.', 'A point inside the PPC: resources (labour) are idle, so actual output is below the maximum possible.', '1 mark: inside the PPC; 1 mark: idle resources explained [2]'),
    ('Strikes have closed many factories in {country} for three months. Explain the effect on {country}’s position relative to its PPC.', 'Output falls below potential while workers and machines are idle, so the economy moves to a point inside the PPC; the PPC itself does not shift.', '1 mark: moves inside; 1 mark: PPC unchanged/capacity not destroyed [2]'),
])
errs(t5_2, [
    ('A rise in unemployment shifts the PPC inwards.', 'Unemployment means resources are idle, so the economy moves to a point inside the PPC; the PPC shifts only if the quantity or quality of resources changes.'),
    ('Points beyond the PPC show the economy is producing very efficiently.', 'Points beyond the PPC are unattainable with current resources and technology.'),
])


@t5_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5_2_point(r, D):
    x, y = r.choice(PAIRS)
    c = r.choice(COUNTRIES)
    step = r.choice([10, 20, 25])
    losses = [l * step for l in sorted(r.sample([1, 2, 3, 4, 5, 6], 4))]
    dx = r.choice([10, 20, 50])
    ys = [sum(losses)]
    for l in losses:
        ys.append(ys[-1] - l)
    xs = [i * dx for i in range(5)]
    tab = table(['Combination', f'{x}', f'{y}'], list(zip('ABCDE', xs, ys)))
    i = r.randint(1, 3)
    kind = r.choice(['inside', 'beyond', 'on'])
    px = xs[i]
    py = ys[i] - r.choice([1, 2]) * step if kind == 'inside' else (ys[i] + r.choice([1, 2]) * step if kind == 'beyond' else ys[i])
    lab = {'inside': 'Inside the PPC: some resources are unemployed or used inefficiently', 'beyond': 'Beyond the PPC: unattainable with current resources and technology', 'on': 'On the PPC: resources fully and efficiently employed'}[kind]
    stem = f'The table shows the maximum combinations of {x} and {y} that {c} can produce. {tab}. {c} is currently producing {px} units of {x} and {py} units of {y}.'
    if D <= 2:
        opts, a = mcq(r, lab, [v for k, v in {'inside': 'Inside the PPC: some resources are unemployed or used inefficiently', 'beyond': 'Beyond the PPC: unattainable with current resources and technology', 'on': 'On the PPC: resources fully and efficiently employed'}.items() if k != kind] + ['On the PPC: the economy is experiencing economic growth'])
        return {'stem': stem + ' Which describes this position?', 'options': opts, 'answer': a, 'key': f'At {px} units of {x} the maximum of {y} is {ys[i]}; {py} is ' + ('less than' if kind == 'inside' else 'more than' if kind == 'beyond' else 'equal to') + ' this.'}
    if kind == 'beyond':
        return None
    extra = ys[i] - py
    return {'stem': stem + f' (a) Explain whether this output is efficient. (b) Calculate the extra {y} that could be produced without giving up any {x}. (c) Explain one reason why an economy might be at this point.',
            'answer': f'(a) {lab}. (b) {extra} units. (c) ' + ('Unemployment, e.g. a recession, or inefficient use of resources.' if extra else 'Not applicable: it is already on the PPC, so more requires giving up some ' + x + '.'),
            'key': f'(a) compare with maximum {ys[i]} [1]; conclusion [1] (b) {ys[i]} − {py} = {extra} [1] (c) reason [1] [4]', 'marks': 4, 'type': 'numerical'}


t5_3 = T('Causes and consequences of shifts in the PPC', 'shifts in the ppc', 'causes and consequences of shifts')
mc(t5_3, [
    ('Which would shift a country’s PPC outwards?', 'An improvement in technology', 'Outward shift: more/better resources or technology.', ['A fall in unemployment', 'A rise in the price level', 'A movement of workers from farming to manufacturing']),
    ('Which would shift a country’s PPC inwards?', 'A natural disaster that destroys factories and farmland', 'Loss of resources reduces productive capacity.', ['A recession', 'A fall in interest rates', 'A rise in exports']),
    ('An improvement in technology that only affects the production of good X causes the PPC to', 'pivot outwards along the X axis', 'Maximum X rises; maximum Y unchanged.', ['shift outwards in parallel', 'shift inwards', 'stay the same']),
    ('Why may producing more capital goods today lead to more consumer goods in the future?', 'Capital goods increase productive capacity, shifting the PPC outwards', 'Investment → growth of potential output.',
     ['Capital goods are cheaper than consumer goods', 'Consumer goods do not use resources', 'The PPC becomes a straight line']),
    ('An increase in the size of the labour force due to immigration would cause', 'an outward shift of the PPC', 'More labour → higher potential output.', ['an inward shift of the PPC', 'a movement inside the PPC', 'a movement along the PPC']),
])
ex(t5_3, [
    ('Explain two causes of an outward shift of a country’s PPC.', 'An increase in the quantity of resources (e.g. labour force growth, discovery of minerals, investment in capital); an improvement in quality (education, training) or technology.',
     '1 mark each cause, 1 mark each explained [4]'),
    ('Explain why a country that chooses to produce more capital goods and fewer consumer goods now may enjoy higher living standards in future.', 'Today’s opportunity cost is fewer consumer goods, but more capital raises productive capacity, shifting the PPC outwards, so more of both can be produced later.',
     '1 mark: opportunity cost now; 1 mark: capital raises capacity/PPC shifts out; 1 mark: more consumption later [3]'),
    ('Explain the difference between a movement along a PPC and a shift of a PPC.', 'A movement along shows a reallocation of existing resources between the two goods; a shift shows a change in the total productive capacity (quantity/quality of resources or technology).',
     '1 mark: movement = reallocation; 1 mark: shift = change in capacity [2]'),
])
SHIFT_CASES = [
    ('{country} discovers large new reserves of natural gas.', 'Outward shift of the PPC', 'more natural resources raise productive capacity.'),
    ('A major earthquake destroys many factories and roads in {country}.', 'Inward shift of the PPC', 'capital is destroyed, reducing productive capacity.'),
    ('Unemployment in {country} rises during a recession.', 'Movement to a point inside the PPC', 'resources become idle; capacity is unchanged.'),
    ('{country} moves workers from farming into building houses.', 'Movement along the PPC', 'existing resources are reallocated between goods.'),
    ('Many young skilled workers emigrate from {country}.', 'Inward shift of the PPC', 'the quantity and quality of labour fall.'),
    ('A new irrigation technology raises crop yields in {country} but has no effect on manufacturing.', 'Outward pivot of the PPC on the food axis', 'only the maximum output of food rises.'),
    ('The government of {country} doubles spending on education and training.', 'Outward shift of the PPC', 'the quality of labour (human capital) improves over time.'),
    ('Firms in {country} recover from a recession and rehire workers.', 'Movement from inside towards the PPC', 'idle resources are brought back into use.'),
]
classify(t5_3, SHIFT_CASES, ['Outward shift of the PPC', 'Inward shift of the PPC', 'Movement to a point inside the PPC', 'Movement along the PPC',
                             'Outward pivot of the PPC on the food axis', 'Movement from inside towards the PPC'],
         'How would this be shown on the country’s PPC?', 'For each event, state how it would be shown on a PPC and explain why.')
items(t5_3, 'C2', (1, 2, 3, 4), [
    ('Climate change is causing desertification of farmland in {country}. Explain the likely effect on {country}’s PPC.', 'Less usable land reduces productive capacity, especially for food, so the PPC shifts (or pivots) inwards.', '1 mark: loss of land resource; 1 mark: inward shift/pivot [2]'),
    ('{country} invests heavily in robots for its factories. Explain the effect on its PPC for agricultural and manufactured goods.', 'Productive capacity in manufacturing rises, so the PPC pivots outwards along the manufactured goods axis; capacity in agriculture is unchanged.', '1 mark: capacity in manufacturing; 1 mark: pivot not parallel shift [2]'),
])
errs(t5_3, [
    ('A fall in unemployment causes the PPC to shift outwards.', 'A fall in unemployment moves the economy from inside towards the PPC; the PPC shifts only when capacity changes.'),
    ('An improvement in technology for producing cars shifts the whole PPC outwards in parallel.', 'If the technology only affects cars, the PPC pivots outwards along the car axis; the maximum output of the other good is unchanged.'),
])


@t5_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5_3_shift(r, D):
    c = r.choice(COUNTRIES)
    x, y = r.choice(PAIRS)
    mx, my = r.choice([(100, 200), (200, 400), (150, 300), (80, 240)])
    g = r.choice([10, 20, 25, 50])
    which = r.choice(['both', 'x'])
    nx, ny = mx * (1 + g / 100), my * (1 + g / 100) if which == 'both' else my
    stem = (f'Before a change, {c} could produce a maximum of {mx} units of {x} or {my} units of {y}. After '
            + ('a rise in the size and skills of its labour force' if which == 'both' else f'a new technology used only in producing {x}') +
            f', the maximum output of {x} rose by {g}%' + (f' and that of {y} by {g}%.' if which == 'both' else f' while the maximum output of {y} was unchanged.'))
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the new maximum output of {x}.', f'{num(nx)} units', f'{mx} × {1 + g / 100} = {num(nx)}.', dis_num(r, nx, lambda v: f'{num(v)} units', [mx + g, my]), mcq_D=(1, 2))
    return {'stem': stem + f' (a) Calculate the new maximum outputs of {x} and {y}. (b) Describe how the PPC has changed. (c) Explain what happens to the opportunity cost of {x} in terms of {y} (assume a straight-line PPC).',
            'answer': f'(a) {num(nx)} {x}; {num(ny)} {y}. (b) ' + ('Parallel outward shift.' if which == 'both' else f'Outward pivot along the {x} axis.') +
                      f' (c) Before: {r2(my / mx)} {y} per {x}; after: {r2(ny / nx)}: ' + ('unchanged.' if which == 'both' else 'it falls, because producing ' + x + ' is now more efficient.'),
            'key': '(a) both maxima [2] (b) shift/pivot [1] (c) both opportunity costs and conclusion [2] [5]', 'marks': 5, 'type': 'multi_step'}


def _ch5_case(r, D):
    d = ctx(r)
    u0, u1 = r.choice([(5, 11), (4, 9), (6, 13)])
    inv = r.choice([15, 18, 20, 25])
    intro = (f'Extract: During a recession unemployment in {d["country"]} rose from {u0}% to {u1}%. The government responded with a programme to build new ports and railways, '
             f'raising investment to {inv}% of GDP. Critics argue that the programme diverts resources away from consumer goods. At the same time a drought reduced the area of farmland that could be used.')
    parts = [
        lambda r: ('Calculate the change in unemployment in percentage points.', f'{u1 - u0} percentage points', f'{u1} − {u0} [1]'),
        lambda r: ('Using a PPC, explain how the recession would be shown.', 'A movement to a point inside the PPC: resources idle, capacity unchanged.', '[2]'),
        lambda r: ('Explain the opportunity cost of the investment programme once the economy returns to full employment.', 'Moving along the PPC: more capital goods means fewer consumer goods now.', '[2]'),
        lambda r: ('Explain the effect of the drought on the PPC.', 'Loss of land reduces capacity (especially for food) so the PPC shifts or pivots inwards.', '[2]'),
        lambda r: ('Discuss whether the investment programme will make the people of {} better off.'.format(d['country']), 'Outward shift of the PPC in future, more consumer goods later, jobs now (idle resources used: no opportunity cost in a recession) vs lower consumption at full employment, risk of poor projects, debt; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t5_1, t5_2, t5_3], _ch5_case)
essay(t5_1, [
    ('With the help of a PPC diagram, explain the difference between constant and increasing opportunity cost.',
     'Straight-line PPC: resources equally suited, constant slope; concave PPC: resources specialised, slope steepens; example of moving resources; axes labelled with the two goods.',
     'the PPC is a useful model for explaining the choices facing {country}',
     'Illustrates scarcity, choice, opportunity cost, efficiency, unemployment and growth clearly.',
     'Only two goods; assumes fixed resources and technology; opportunity cost hard to measure; ignores distribution and consumer preferences; still a helpful simplification.'),
])
essay(t5_2, [
    ('Using a PPC diagram, explain the significance of points inside, on and outside the curve.',
     'Inside: unemployment/inefficiency; on: productive efficiency; outside: unattainable without growth or trade; movements between points; zero opportunity cost of using idle resources.',
     'reducing unemployment is always a cost-free way for {country} to increase output',
     'Moving from inside to the curve uses idle resources with zero opportunity cost.',
     'Some unemployment is structural and requires retraining costs; policies have budget costs and may cause inflation; leisure lost; depends on the cause of unemployment.'),
])
essay(t5_3, [
    ('Explain, with the help of a diagram, the factors that could cause a country’s PPC to shift outwards.',
     'More or better resources: labour force growth, education, investment in capital, discovery of resources, technology; parallel shift vs pivot.',
     'investment in capital goods is the most effective way for {country} to shift its PPC outwards',
     'Capital raises productivity and embodies new technology; infrastructure supports all sectors.',
     'Opportunity cost of fewer consumer goods now; education and technology may matter more; capital needs skilled labour; diminishing returns; depends on quality of investment.'),
], ['{country} is choosing between more consumer goods now and more investment in infrastructure.'])
CHAPTERS[5] = [t5_1, t5_2, t5_3]

# ============================================================================ 6 Classification of goods and services
GOOD_CASES = [
    ('Air breathed by people walking in a park in {city}.', 'Free good', 'no resources are needed to provide it and there is no opportunity cost.'),
    ('A loaf of bread bought in a supermarket in {city}.', 'Private good', 'excludable and rivalrous.'),
    ('A lighthouse warning ships off the coast of {country}.', 'Public good', 'non-excludable and non-rivalrous; free riders cannot be prevented.'),
    ('Vaccinations against measles provided in {country}.', 'Merit good', 'more beneficial than consumers realise; under-consumed in a free market.'),
    ('Cigarettes sold in {country}.', 'Demerit good', 'more harmful than consumers realise; over-consumed in a free market.'),
    ('National defence in {country}.', 'Public good', 'no one can be excluded and one person’s protection does not reduce another’s.'),
    ('Sea water used by a desalination plant in {country}.', 'Free good', 'abundant with zero opportunity cost before processing.'),
    ('Education for children in {country}.', 'Merit good', 'benefits are greater than individuals appreciate (information failure) and there are external benefits.'),
    ('Sugary fizzy drinks sold to teenagers in {city}.', 'Demerit good', 'the harm to health is underestimated by consumers.'),
    ('A haircut at a salon in {city}.', 'Private good', 'excludable (pay to receive it) and rivalrous.'),
    ('Street lighting in {city}.', 'Public good', 'non-excludable and non-rivalrous.'),
]
GOOD_LABELS = ['Free good', 'Private good', 'Public good', 'Merit good', 'Demerit good']

t6_1 = T('Free goods and economic goods', 'free goods and economic goods', 'free goods', 'economic goods')
mc(t6_1, [
    ('What is a free good?', 'A good that is not scarce and has zero opportunity cost', 'Free good: unlimited supply relative to demand; no resources used.',
     ['A good provided by the government without charge', 'A good with a price of zero in shops', 'A good given away by firms as a promotion']),
    ('What is an economic good?', 'A good that is scarce and so has an opportunity cost', 'Economic goods use scarce resources.',
     ['A good that is always produced by the private sector', 'A good that can only be bought with money', 'A good that is produced abroad']),
    ('Which is a free good?', 'Sunlight', 'Abundant, no resources needed, zero opportunity cost.', ['Tap water', 'State education', 'A free newspaper']),
    ('Why is healthcare provided free of charge by the state an economic good?', 'It uses scarce resources that have alternative uses', 'Zero price ≠ free good; opportunity cost exists.',
     ['Because patients pay taxes', 'Because doctors are paid wages', 'Because it is a public good']),
    ('Clean air in a heavily polluted city may become', 'an economic good, because resources must be used to provide it', 'When scarce, resources (filters, regulation) are needed.', ['a free good', 'a public good', 'a demerit good']),
])
ex(t6_1, [
    ('Explain the difference between a free good and an economic good.', 'A free good is unlimited relative to demand, so no resources are used and the opportunity cost is zero (e.g. sunlight). An economic good is scarce, uses resources and has an opportunity cost.',
     '1 mark: free good definition; 1 mark: economic good definition [2]'),
    ('Explain why a good that has a zero price is not necessarily a free good.', 'A zero price may be set by government or a firm, but if producing it uses scarce resources it has an opportunity cost and is an economic good.', '1 mark: zero price ≠ zero opportunity cost; 1 mark: example/explanation [2]'),
    ('Explain how a free good can become an economic good.', 'If demand rises or supply falls so that it becomes scarce (e.g. clean water due to pollution), resources must be used to provide it, giving it an opportunity cost.',
     '1 mark: becomes scarce; 1 mark: resources used/opportunity cost [2]'),
])
items(t6_1, 'C2', (1, 2, 3, 4), [
    ('The government of {country} provides free school textbooks. Explain why the textbooks are an economic good.', 'Producing them uses scarce paper, labour and printing capital that could be used elsewhere; there is an opportunity cost even though pupils pay nothing.', '1 mark: uses resources; 1 mark: opportunity cost [2]'),
    ('Fresh water from mountain streams near {city} was once a free good. Explain why it may now be an economic good.', 'Population growth and pollution have made clean water scarce; resources are now used to collect, clean and distribute it.', '1 mark: scarcity; 1 mark: resources used [2]'),
])
errs(t6_1, [
    ('Public healthcare in {country} is a free good because patients do not pay.', 'It is an economic good: it uses scarce resources with an opportunity cost; the price is zero but the cost is borne through taxation.'),
    ('A free good is any good with a price of zero.', 'A free good has zero opportunity cost because it is not scarce; many zero-price goods use scarce resources and are economic goods.'),
])
classify(t6_1, GOOD_CASES, GOOD_LABELS, 'How is this good best classified?', 'Classify each good and explain your answer.', name='goods')


@t6_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_1_free(r, D):
    c = r.choice(COUNTRIES)
    cost = r.choice([0.4, 0.5, 0.8, 1.2, 1.5])
    pop = r.choice([2, 3, 4, 5])
    use = r.choice([100, 120, 150, 200])
    tot = cost * pop * use * 365 / 1000
    stem = (f'In {c}, the state supplies drinking water free of charge. Treating and piping water costs ${cost} per 1,000 litres. The population is {pop} million and each person uses {use} litres a day.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the annual cost of supplying the water, in millions of dollars.', f'${num(tot, 1)} million', f'{pop}m × {use} × 365 / 1,000 × {cost} = {num(tot, 1)}.',
                  dis_num(r, tot, lambda v: f'${num(v, 1)} million', [tot / 365, cost * pop * use]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the annual cost of supplying the water. (b) Explain why the water is an economic good even though consumers pay nothing. (c) Explain one problem that may arise from supplying it at a zero price.',
            'answer': f'(a) ${num(tot, 1)} million (b) Resources (labour, chemicals, pipes) are used with an opportunity cost; the cost is met through taxation. (c) Over-use/waste because the marginal price is zero; shortages in droughts.',
            'key': f'(a) {pop}m × {use} × 365 ÷ 1,000 × {cost} [2] (b) resources/opportunity cost [1] (c) over-consumption at zero price [1] [4]', 'marks': 4, 'type': 'numerical'}


t6_2 = T('Private goods and public goods: excludability, rivalry and the free rider problem', 'private goods and public goods', 'excludability', 'rivalry', 'free rider')
mc(t6_2, [
    ('What are the two characteristics of a pure public good?', 'Non-excludable and non-rivalrous', 'Non-excludability (cannot stop non-payers) and non-rivalry (use by one does not reduce availability to others).',
     ['Excludable and rivalrous', 'Excludable and non-rivalrous', 'Non-excludable and rivalrous']),
    ('What is meant by the free rider problem?', 'People can benefit from a good without paying for it, so it is not provided by the market', 'Non-excludability → free riding → no revenue → missing market.',
     ['Public transport users who do not buy tickets', 'Consumers who buy goods on credit', 'Firms that receive government subsidies']),
    ('What does it mean to say that a good is rivalrous?', 'Consumption by one person reduces the amount available to others', 'Rivalry: one person’s use reduces others’ availability.',
     ['Firms compete to sell it', 'It is sold at a high price', 'It is provided by the government']),
    ('Which is the best example of a public good?', 'A flood defence system protecting a town', 'Non-excludable and non-rivalrous within the protected area.', ['A bus ticket', 'A school meal', 'A private swimming pool']),
    ('Why are public goods usually provided by the government?', 'Private firms cannot charge consumers because non-payers cannot be excluded', 'Missing market due to free riding.',
     ['They are too cheap to produce privately', 'Consumers do not want them', 'They are always demerit goods']),
    ('Why is a toll road not a pure public good?', 'Drivers who do not pay can be excluded', 'Tolls make it excludable (quasi-public good).', ['It is non-rivalrous', 'It is provided by a private firm', 'It has no opportunity cost']),
])
ex(t6_2, [
    ('Explain why the free rider problem leads to a missing market for public goods.', 'Because non-payers cannot be excluded, people can benefit without paying, so few are willing to pay; firms cannot earn revenue, so no firm supplies the good.',
     '1 mark: non-excludability; 1 mark: free riding/no willingness to pay; 1 mark: no profit, so not provided [3]'),
    ('Explain the difference between a private good and a public good.', 'Private goods are excludable and rivalrous (e.g. food); public goods are non-excludable and non-rivalrous (e.g. street lighting).', '1 mark each [2]'),
    ('Explain what is meant by a quasi-public good, using an example.', 'A good with some but not all public-good characteristics, e.g. a road is largely non-rivalrous until congested, and exclusion is possible with tolls.', '1 mark: partly public; 1 mark: example explained [2]'),
])
items(t6_2, 'C2', (1, 2, 3, 4), [
    ('Residents of a street in {city} would all benefit from CCTV cameras, but nobody is willing to pay for them. Explain why.', 'Each resident benefits whether or not they pay (non-excludable), so each waits for others to pay: the free rider problem.', '1 mark: non-excludable; 1 mark: free riding [2]'),
    ('A beach in {country} becomes very crowded at weekends. Explain why it may no longer be non-rivalrous.', 'Extra visitors reduce the space and enjoyment available to others, so consumption becomes rivalrous.', '1 mark: congestion; 1 mark: reduces others’ benefit [2]'),
    ('Explain why a private firm in {country} is unlikely to supply national defence.', 'National defence is non-excludable, so the firm could not charge those who benefit; free riding means no revenue to cover costs.', '1 mark: non-excludable; 1 mark: no revenue [2]'),
])
errs(t6_2, [
    ('Public goods are any goods provided by the government, such as schools.', 'Public goods are defined by non-excludability and non-rivalry, not by who provides them; school places are excludable and rivalrous.'),
    ('A public good is non-rivalrous because everyone can afford it.', 'Non-rivalry means one person’s consumption does not reduce the amount available to others.'),
])
classify(t6_2, GOOD_CASES, GOOD_LABELS, 'How is this good best classified?', 'Classify each good and explain your answer.', name='goods')


@t6_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_2_free(r, D):
    c = r.choice(CITIES_PG)
    n = r.choice([200, 250, 400, 500])
    v = r.choice([20, 25, 30, 40, 50])
    cost = r.choice([4000, 6000, 8000, 10000])
    tot = n * v
    if tot <= cost:
        return None
    stem = f'A neighbourhood in {c} has {n} households. Each values a new set of street lights at ${v}. The lights would cost ${cost:,} to install.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the total value of the lights to the households.', money(tot), f'{n} × ${v} = {money(tot)}.', dis_num(r, tot, money, [tot - cost, v * 10]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the total value to the households and compare it with the cost. (b) Explain why the lights may not be provided by the market even though their value exceeds the cost. (c) Suggest how the lights could be provided.',
            'answer': f'(a) Total value {money(tot)} > cost ${cost:,}, so provision is worthwhile for society. (b) The lights are non-excludable: each household can free ride on others’ payments, so firms cannot collect enough revenue; a missing market. (c) Provision by the local council financed by taxes (or compulsory levy).',
            'key': f'(a) {n} × {v} = {tot} [1]; comparison [1] (b) non-excludable [1]; free rider/missing market [1] (c) government provision via taxation [1] [5]', 'marks': 5, 'type': 'multi_step'}


CITIES_PG = ['Nairobi', 'Lima', 'Hanoi', 'Accra', 'Colombo', 'Lisbon', 'Manila', 'Bogotá', 'Muscat', 'Auckland']

t6_3 = T('Merit and demerit goods and information failure', 'merit and demerit goods', 'information failure', 'merit goods', 'demerit goods')
mc(t6_3, [
    ('What is a merit good?', 'A good that is more beneficial to consumers than they realise and is under-consumed in a free market', 'Merit goods: under-consumption due to information failure (and positive externalities).',
     ['A good that is provided free by the government', 'A good that is non-excludable', 'A good that wins awards for quality']),
    ('What is a demerit good?', 'A good that is more harmful to consumers than they realise and is over-consumed in a free market', 'Demerit: over-consumption due to information failure (and negative externalities).',
     ['A good that is of poor quality', 'A good that has no price', 'A good that is produced inefficiently']),
    ('What is the main reason merit goods are under-consumed in a free market?', 'Consumers lack full information about the benefits', 'Information failure (imperfect information); short-termism.',
     ['Merit goods are always very expensive', 'Firms are unwilling to produce them', 'Merit goods are non-rivalrous']),
    ('Which is an example of a demerit good?', 'Alcohol', 'Harm underestimated by consumers.', ['Fruit and vegetables', 'Vaccinations', 'Public libraries']),
    ('Which policy is most suitable for reducing consumption of a demerit good?', 'An indirect tax on the good', 'Taxes raise the price; also bans, regulation, information campaigns.', ['A subsidy for producers', 'A maximum price below equilibrium', 'Free provision by the state']),
    ('What is meant by information failure?', 'A situation where consumers or producers lack the information needed to make the best decisions', 'Imperfect or asymmetric information.',
     ['A failure of the internet', 'A situation in which prices are too high', 'A shortage of goods in shops']),
])
ex(t6_3, [
    ('Explain why education is regarded as a merit good.', 'Individuals, particularly the young, may underestimate the long-term benefits of education (higher lifetime earnings, better health), so in a free market it is under-consumed; there are also external benefits to society.',
     '1 mark: benefits underestimated/information failure; 1 mark: under-consumed; 1 mark: external benefits [3]'),
    ('Explain how information failure leads to the over-consumption of demerit goods.', 'Consumers underestimate the harm (to health, addiction) of goods such as cigarettes, so they buy more than they would with full information; consumption exceeds the socially optimal level.',
     '1 mark: harm underestimated; 1 mark: over-consumption compared with full information [2]'),
    ('Explain why the classification of goods as merit or demerit involves a value judgement.', 'Deciding that people consume “too much” or “too little” of a good depends on views about what is good for them; individuals may disagree with the government.',
     '1 mark: depends on judgement of what is beneficial; 1 mark: paternalism/consumers may disagree [2]'),
])
items(t6_3, 'C2', (1, 2, 3, 4), [
    ('Many adults in {country} do not have regular dental check-ups. Explain why this may be an example of information failure.', 'People underestimate the long-term benefits of check-ups (and the costs of untreated problems), so they consume less than is in their own interest.', '1 mark: benefits underestimated; 1 mark: under-consumption [2]'),
    ('The government of {country} requires health warnings on packets of cigarettes. Explain how this could correct a market failure.', 'Warnings give consumers better information about harm, reducing information failure, so demand falls towards the socially optimal level.', '1 mark: improves information; 1 mark: demand falls [2]'),
    ('Explain why {city}’s council might provide free swimming lessons for children.', 'Swimming lessons are a merit good: parents may underestimate safety and health benefits; free provision raises consumption towards the optimum.', '1 mark: merit good/info failure; 1 mark: free provision raises consumption [2]'),
])
errs(t6_3, [
    ('A merit good is any good that is provided by the government.', 'A merit good is one whose benefits are underestimated so it is under-consumed in a free market; it may be provided privately or publicly.'),
    ('Demerit goods are over-consumed because they are cheap.', 'They are over-consumed mainly because consumers underestimate their harmful effects (information failure), whatever the price.'),
])
classify(t6_3, GOOD_CASES, GOOD_LABELS, 'How is this good best classified?', 'Classify each good and explain your answer.', name='goods')


@t6_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_3_vacc(r, D):
    c = r.choice(COUNTRIES)
    q0 = r.choice([45, 50, 55, 60])
    q1 = r.choice([80, 85, 90])
    price = r.choice([20, 25, 30, 40])
    pop = r.choice([200, 300, 400, 500])
    cost = pop * 1000 * q1 / 100 * price / 1e6
    stem = (f'In {c}, {q0}% of children receive a flu vaccination when parents must pay ${price}. When the vaccination was made free in a trial region, take-up rose to {q1}%.')
    if D <= 2:
        return cq(r, 1, stem + ' By how many percentage points did take-up rise?', f'{q1 - q0} percentage points', f'{q1} − {q0} = {q1 - q0}.',
                  [f'{x} percentage points' for x in (q1, round(100 * (q1 - q0) / q0), q0, q1 - q0 + 5)], mcq_D=(1, 2))
    return {'stem': stem + f' The national child population is {pop},000. (a) Calculate the cost to the government of free vaccinations nationally at the trial take-up rate, in millions of dollars. (b) Using the concept of a merit good, explain why take-up was low when parents paid. (c) Explain one reason why the policy may be worth its cost.',
            'answer': f'(a) ${num(cost, 2)} million (b) Parents underestimate the benefits (information failure) and ignore benefits to others, so demand is below the social optimum. (c) External benefits: fewer infections in the wider population, lower healthcare costs and fewer days lost from work.',
            'key': f'(a) {pop},000 × {q1}% × ${price} = ${num(cost, 2)}m [2] (b) information failure/under-consumption [1] (c) external benefits/savings [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch6_case(r, D):
    d = ctx(r)
    t = r.choice([20, 25, 30])
    s0, s1 = r.choice([(32, 27), (28, 24), (35, 29)])
    intro = (f'Extract: The government of {d["country"]} has introduced a {t}% tax on sugary drinks and used the revenue to fund free fruit in primary schools and a new public park in {d["city"]}. '
             f'The share of adults who drink sugary drinks daily fell from {s0}% to {s1}%. Some critics argue that people should be free to choose what they consume.')
    parts = [
        lambda r: ('Calculate the percentage fall in the share of adults drinking sugary drinks daily.', pct(-chg(s0, s1)), f'({s0} − {s1})/{s0} × 100 [2]'),
        lambda r: ('Explain why sugary drinks may be classified as a demerit good.', 'Consumers underestimate the long-term health harm, so they over-consume relative to the optimum.', '[2]'),
        lambda r: ('Explain why the park is likely to be provided by the government rather than the market.', 'It is (quasi-)public: non-excludable and largely non-rivalrous, so free riding means firms cannot charge.', '[3]'),
        lambda r: ('Explain why free fruit in schools may increase economic welfare.', 'Merit good under-consumed due to information failure; free provision raises consumption; long-term health benefits.', '[2]'),
        lambda r: ('Discuss whether the government is right to interfere with consumers’ choices in this way.', 'Correcting information failure and external costs (healthcare) vs paternalism, regressive tax, possible substitution to other unhealthy goods; information campaigns as alternative; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t6_1, t6_2, t6_3], _ch6_case)
essay(t6_1, [
    ('Explain the difference between free goods and economic goods, and why the distinction depends on scarcity.',
     'Free goods: no opportunity cost; economic goods: scarce resources used; zero-price goods may still be economic goods; free goods may become economic goods.',
     'no good is truly a free good in the modern world',
     'Pollution and population growth make air and water scarce in many places; resources are needed to keep them clean.',
     'Sunlight, sea water and air in remote areas remain abundant; depends on location and time; useful distinction for opportunity cost.'),
])
essay(t6_2, [
    ('Explain the characteristics of public goods and why the free rider problem means they may not be provided by a market.',
     'Non-excludable and non-rivalrous; free riding; no revenue; missing market; examples; quasi-public goods.',
     'the government of {country} should provide all public goods free of charge',
     'Missing market; non-rivalry means zero marginal cost so charging is inefficient; equity.',
     'Opportunity cost and tax burden; hard to value demand; technology may allow exclusion (tolls, encryption); private provision possible via sponsorship; government failure.'),
], ['{country} is considering whether to charge for the use of its main roads.'])
essay(t6_3, [
    ('Explain why merit goods tend to be under-consumed and demerit goods over-consumed in a free market.',
     'Information failure; consumers under/overestimate benefits and harms; short-termism; externalities; diagram of demand relative to social optimum.',
     'information failure is best corrected by providing information rather than by taxes or subsidies',
     'Tackles the cause; preserves freedom of choice; low cost.',
     'Habits and addiction limit response; information may be ignored; taxes and subsidies change incentives directly; regulation needed for serious harm; combination of policies.'),
], ['Obesity rates in {country} have doubled in twenty years.'])
CHAPTERS[6] = [t6_1, t6_2, t6_3]


# ----------------------------------------------------------------------------- linear market helpers
def lin(r):
    """Integer linear market: Qd = a − bP, Qs = c + dP with equilibrium (P, Q)."""
    for _ in range(50):
        P = r.choice([4, 5, 6, 8, 10, 12, 15, 20, 25])
        b = r.choice([2, 3, 4, 5, 10])
        d = r.choice([2, 3, 4, 5, 6, 10])
        Q = r.choice([40, 50, 60, 80, 100, 120, 150, 200])
        a = Q + b * P
        c = Q - d * P
        if Q > 0 and a > 0 and d * P >= 0.4 * Q and b * P >= 0.3 * Q and c > -Q:
            return a, b, c, d, P, Q
    return 200, 5, 20, 4, 20, 100


GOODS_P = ['restaurant meals', 'concert tickets', 'T-shirts', 'paperback books', 'haircuts', 'gym memberships', 'pizzas', 'cinema tickets',
           'phone cases', 'board games', 'theatre tickets', 'taxi rides', 'museum tickets', 'school backpacks', 'sun hats', 'yoga classes']
SUPPLY_P = ['T-shirts', 'paperback books', 'fresh fish (per kg)', 'tomatoes (per box)', 'wheat (per sack)', 'cement (per bag)', 'car tyres', 'phone cases',
            'cut flowers (per bunch)', 'school backpacks', 'olive oil (per litre)', 'bricks (per hundred)']


def qd_s(a, b):
    return f'Qd = {a} − {b}P'


def qs_s(c, d):
    return f'Qs = {c} + {d}P' if c >= 0 else f'Qs = −{-c} + {d}P'


def pchg(x, dp=1):
    """Signed percentage text such as '+12.5%' or '−8%'."""
    v = round(x, dp)
    s = num(abs(v), dp) + '%'
    return ('+' if v > 0 else '−' if v < 0 else '') + s


# ============================================================================ 7 Demand and supply curves
t7_1 = T('The law of demand, effective demand and the market demand curve', 'law of demand', 'effective demand', 'market demand curve')
mc(t7_1, [
    ('What is meant by effective demand?', 'The desire for a good backed by the ability and willingness to pay for it', 'Effective demand = want + ability to pay.',
     ['The total quantity of a good that consumers would like to have', 'The demand of consumers who are well informed', 'Demand at the equilibrium price only']),
    ('What does the law of demand state?', 'As price falls, quantity demanded rises, ceteris paribus', 'Inverse relationship between price and quantity demanded.',
     ['As price falls, supply rises', 'As income rises, demand rises', 'As price rises, demand rises for all goods']),
    ('How is the market demand curve derived?', 'By adding the quantities demanded by all individual consumers at each price', 'Horizontal summation of individual demand curves.',
     ['By adding the prices that each consumer would pay', 'By averaging individual demand curves', 'By multiplying price by quantity']),
    ('Why does a demand curve usually slope downwards from left to right?', 'At lower prices consumers can afford more and the good becomes better value relative to substitutes', 'Income and substitution effects; diminishing marginal utility.',
     ['Firms produce more at lower prices', 'Costs of production fall as output rises', 'Government sets lower prices for larger quantities']),
    ('Which is a reason for an individual’s demand to be shown by a demand schedule?', 'It lists the quantities the consumer would buy at different prices in a given time period', 'Demand schedule: table of P and Qd.',
     ['It lists the prices set by firms', 'It shows the costs of production', 'It shows how much the consumer earns']),
])
ex(t7_1, [
    ('Explain the difference between demand and effective demand.', 'Demand in economics is effective demand: the quantity consumers are willing and able to buy at each price in a time period. A desire for a good without the ability to pay is not effective demand.',
     '1 mark: willing and able; 1 mark: desire alone not enough [2]'),
    ('Explain why a fall in the price of a good leads to an increase in the quantity demanded.', 'The good becomes cheaper relative to substitutes, so consumers switch to it (substitution effect); real income rises so they can afford more (income effect); new consumers enter the market.',
     '1 mark: substitution effect; 1 mark: income effect/new buyers [2]'),
    ('Explain how a market demand curve is derived from individual demand curves.', 'At each price the quantities demanded by every consumer in the market are added together (horizontal summation) to give total market demand.', '1 mark: summation of quantities; 1 mark: at each price [2]'),
])
items(t7_1, 'C2', (1, 2, 3, 4), [
    ('Many people in {city} would like to own an electric car, but sales remain low. Explain this using the concept of effective demand.', 'Desire is not backed by ability to pay at current prices, so it is not effective demand; only those willing and able to buy count in the market.', '1 mark: definition; 1 mark: application [2]'),
    ('{firm} cuts the price of {good} by 10% and sales rise. Explain why, using the law of demand.', 'Lower price raises quantity demanded: the product is cheaper relative to substitutes and consumers’ real income rises.', '1 mark: inverse relationship; 1 mark: reason [2]'),
])
errs(t7_1, [
    ('When the price of {good} falls, demand for {good} increases, so the demand curve shifts to the right.', 'A fall in the good’s own price causes an extension of demand: a movement along the existing demand curve, not a shift.'),
    ('Everyone who wants a good forms part of its demand.', 'Only effective demand counts: the desire must be backed by the ability and willingness to pay.'),
])


@t7_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t7_1_mkt(r, D):
    g = r.choice(GOODS)
    names = r.sample(['A', 'B', 'C'], 3)
    prices = [2, 4, 6, 8]
    base = [r.choice([10, 12, 15, 20]) for _ in range(3)]
    slopes = [r.choice([1, 2, 3]) for _ in range(3)]
    qs = [[max(0, b - s * i) for i in range(4)] for b, s in zip(base, slopes)]
    mk = [sum(q[i] for q in qs) for i in range(4)]
    tab = table(['Price ($)'] + [f'Consumer {n} (units)' for n in ('X', 'Y', 'Z')], [tuple([p] + [q[i] for q in qs]) for i, p in enumerate(prices)])
    i = r.randint(0, 3)
    stem = f'The table shows the weekly demand for {g} of the only three consumers in a market. {tab}.'
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the market quantity demanded at a price of ${prices[i]}.', f'{mk[i]} units', f'{" + ".join(str(q[i]) for q in qs)} = {mk[i]}.',
                  [f'{x} units' for x in (mk[i] + 2, mk[i] - 2, qs[0][i], round(mk[i] / 3))], mcq_D=(1, 2))
    j = r.choice([k for k in range(4) if k != i])
    return {'stem': stem + f' (a) Calculate the market demand at each price. (b) Calculate the percentage change in market quantity demanded when the price changes from ${prices[i]} to ${prices[j]}. (c) Explain why the market demand curve slopes downwards.',
            'answer': f'(a) {", ".join(map(str, mk))} units at $2, $4, $6, $8. (b) {pchg(chg(mk[i], mk[j]))} (c) Each consumer buys more at lower prices (substitution and income effects), so the sum also rises as price falls.',
            'key': f'(a) horizontal summation [2] (b) ({mk[j]} − {mk[i]})/{mk[i]} × 100 [1] (c) law of demand reason [1] [4]', 'marks': 4, 'type': 'numerical'}


DEM_CASES = [
    ('The price of {good} falls.', 'Movement along the demand curve (extension)', 'a change in the good’s own price causes a movement along the curve.'),
    ('Average incomes in {country} rise and consumers regard {good} as a normal good.', 'Shift of the demand curve to the right', 'higher income raises demand at every price for a normal good.'),
    ('The price of a close substitute for {good} rises.', 'Shift of the demand curve to the right', 'consumers switch from the dearer substitute.'),
    ('The price of a complement to {good} rises sharply.', 'Shift of the demand curve to the left', 'goods are used together, so demand for {good} falls at every price.'),
    ('A widely reported health study warns about the harm caused by {good}, changing tastes.', 'Shift of the demand curve to the left', 'tastes and preferences have moved against the good.'),
    ('The price of {good} rises.', 'Movement along the demand curve (contraction)', 'own-price change: movement up the existing curve.'),
    ('A successful advertising campaign for {good} is launched.', 'Shift of the demand curve to the right', 'tastes/preferences shift in favour of the good.'),
    ('Incomes fall in {country} and consumers regard {good} as an inferior good.', 'Shift of the demand curve to the right', 'demand for inferior goods rises when income falls.'),
    ('The population of {city} grows rapidly.', 'Shift of the demand curve to the right', 'more consumers in the market.'),
]
DEM_LABELS = ['Movement along the demand curve (extension)', 'Movement along the demand curve (contraction)', 'Shift of the demand curve to the right', 'Shift of the demand curve to the left']

t7_2 = T('Movements along versus shifts in the demand curve: conditions of demand', 'movements along versus shifts in the demand curve', 'conditions of demand', 'shifts in the demand curve')
mc(t7_2, [
    ('Which causes a movement along the demand curve for a good?', 'A change in the price of the good itself', 'Own price → movement; other factors → shift.',
     ['A change in consumers’ incomes', 'A change in tastes', 'A change in the price of a substitute']),
    ('Which would shift the demand curve for coffee to the right?', 'A rise in the price of tea', 'Tea is a substitute; demand for coffee rises at every price.', ['A fall in the price of coffee', 'A rise in the price of sugar', 'A fall in consumers’ incomes, if coffee is normal']),
    ('What is meant by the conditions of demand?', 'The factors other than the good’s own price that determine demand', 'Income, prices of related goods, tastes, population, advertising, expectations.',
     ['The prices at which firms are willing to supply', 'The legal rules for selling goods', 'The time it takes to deliver goods']),
    ('A rise in the price of petrol is most likely to shift the demand curve for large cars', 'to the left', 'Petrol and cars are complements.', ['to the right', 'neither way: it causes a movement along', 'to the right, then to the left']),
    ('What is the difference between an increase in demand and an increase in quantity demanded?', 'An increase in demand is a shift of the curve; an increase in quantity demanded is a movement along it', 'Terminology: shift vs extension.',
     ['There is no difference', 'An increase in demand is caused by a fall in price', 'An increase in quantity demanded is caused by a rise in income']),
])
ex(t7_2, [
    ('Explain the difference between a movement along a demand curve and a shift of a demand curve.', 'A movement (extension or contraction) is caused only by a change in the good’s own price; a shift is caused by a change in any other condition of demand, such as income or tastes, changing the quantity demanded at every price.',
     '1 mark: movement = own price; 1 mark: shift = other factors/at every price [2]'),
    ('Explain how an increase in income affects demand for normal and inferior goods.', 'For a normal good demand rises (curve shifts right); for an inferior good demand falls (curve shifts left) as consumers switch to better alternatives.',
     '1 mark: normal; 1 mark: inferior [2]'),
    ('Explain why expectations of a future price rise may shift the current demand curve.', 'Consumers buy now before the price rises, so current demand rises at every price: the demand curve shifts right.', '1 mark: buy now; 1 mark: shift right [2]'),
])
classify(t7_2, DEM_CASES, DEM_LABELS, 'What is the effect on the demand curve for {good}?', 'For each change, state the effect on the demand curve for {good} and explain why.', name='demand')
items(t7_2, 'C2', (1, 2, 3, 4), [
    ('A new train line makes it quicker to travel from {city} to the coast. Explain the effect on the demand for car hire in {city}.', 'Rail travel is a substitute: demand for car hire falls at every price, shifting the demand curve to the left.', '1 mark: substitute; 1 mark: shift left [2]'),
    ('The price of games consoles falls sharply in {country}. Explain the effect on the demand for video games.', 'Consoles and games are complements: more consoles are bought, so demand for games rises at every price (shift right).', '1 mark: complements; 1 mark: shift right [2]'),
])
errs(t7_2, [
    ('A rise in the price of {good} shifts the demand curve for {good} to the left.', 'A change in a good’s own price causes a movement along (contraction), not a shift.'),
    ('When incomes rise, the demand for all goods increases.', 'Demand rises for normal goods but falls for inferior goods.'),
])


@t7_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t7_2_shift(r, D):
    g = r.choice(GOODS)
    a = r.choice([200, 240, 300, 360])
    b = r.choice([4, 5, 6, 10])
    da = r.choice([20, 30, 40, 50, 60]) * r.choice([1, -1])
    P = r.choice([5, 8, 10, 12])
    if a - b * P <= 0 or a + da - b * P <= 0:
        return None
    q0, q1 = a - b * P, a + da - b * P
    cause = r.choice(['rise in incomes (normal good)', 'rise in the price of a substitute', 'successful advertising campaign']) if da > 0 else r.choice(['fall in incomes (normal good)', 'rise in the price of a complement', 'health scare'])
    stem = f'The demand for {g} in {r.choice(COUNTRIES)} is {qd_s(a, b)}. After a {cause}, demand becomes Qd = {a + da} − {b}P.'
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the change in quantity demanded at a price of ${P}.', f'{sgn(da, 0)} units', f'Before {q0}, after {q1}; change {sgn(da, 0)}.',
                  [f'{sgn(x, 0)} units' for x in (-da, da * 2, b * P, da + b)], mcq_D=(1, 2))
    return {'stem': stem + f' (a) Calculate the quantity demanded at ${P} before and after the change. (b) State whether this is a shift or a movement along the demand curve and explain why. (c) Explain the cause using the conditions of demand.',
            'answer': f'(a) {q0} → {q1} units. (b) A shift {"right" if da > 0 else "left"}: quantity demanded changes at every price, not because of the good’s own price. (c) The {cause} changes a condition of demand.',
            'key': f'(a) both values [2] (b) shift and direction [1]; reason [1] (c) cause explained [1] [5]', 'marks': 5, 'type': 'multi_step'}


SUP_CASES = [
    ('Wages paid to workers producing {mgood} rise.', 'Shift of the supply curve to the left', 'higher costs of production reduce supply at every price.'),
    ('A new technology reduces the cost of producing {mgood}.', 'Shift of the supply curve to the right', 'lower unit costs raise supply at every price.'),
    ('The price of {mgood} rises.', 'Movement along the supply curve (extension)', 'own-price change: firms supply more at a higher price.'),
    ('The government gives producers of {mgood} a subsidy.', 'Shift of the supply curve to the right', 'a subsidy lowers producers’ costs.'),
    ('The government imposes an indirect tax on {mgood}.', 'Shift of the supply curve to the left', 'the tax raises costs per unit.'),
    ('A flood destroys factories producing {mgood} in {country}.', 'Shift of the supply curve to the left', 'productive capacity falls.'),
    ('The price of {mgood} falls.', 'Movement along the supply curve (contraction)', 'own-price change: movement down the curve.'),
    ('Several new firms enter the {mgood} industry in {country}.', 'Shift of the supply curve to the right', 'more producers in the market.'),
]
SUP_LABELS = ['Shift of the supply curve to the right', 'Shift of the supply curve to the left', 'Movement along the supply curve (extension)', 'Movement along the supply curve (contraction)']

t7_3 = T('Supply: the law of supply, movements along and shifts in the supply curve', 'law of supply', 'shifts in the supply curve', 'supply')
mc(t7_3, [
    ('What does the law of supply state?', 'As price rises, the quantity supplied rises, ceteris paribus', 'Positive relationship: higher prices → more profitable → more supplied.',
     ['As price rises, demand falls', 'As costs rise, supply rises', 'As price falls, quantity supplied rises']),
    ('Which would shift the supply curve of rice to the right?', 'Improved irrigation that raises yields', 'Lower costs/higher productivity raise supply.', ['A rise in the price of rice', 'An increase in the wages of farm workers', 'A tax on rice production']),
    ('Why does a supply curve usually slope upwards?', 'Higher prices make production more profitable and cover the higher costs of extra output', 'Profit incentive; rising marginal cost.',
     ['Consumers buy more at higher prices', 'Costs fall as output rises', 'Government requires it']),
    ('Which causes a movement along a supply curve?', 'A change in the price of the good', 'Own price → movement; costs, technology, taxes → shift.', ['A change in technology', 'A change in the cost of raw materials', 'A subsidy to producers']),
    ('What effect would an indirect tax have on a supply curve?', 'Shift it to the left (upwards) by the amount of the tax', 'Tax raises cost per unit.', ['Shift it to the right', 'Cause a movement along it', 'Make it vertical']),
])
ex(t7_3, [
    ('Explain why a supply curve slopes upwards from left to right.', 'At higher prices it is more profitable to produce, so existing firms expand output and new firms enter; higher prices also cover the rising marginal cost of extra output.', '1 mark: profit incentive; 1 mark: rising costs/new firms [2]'),
    ('Explain two factors that could cause the supply curve for a good to shift to the left.', 'Higher costs of production (wages, raw materials, energy); indirect taxes; adverse weather/natural disasters; fewer firms; removal of subsidies.', '1 mark each factor explained [2]'),
    ('Explain the difference between an increase in supply and an increase in quantity supplied.', 'An increase in supply is a rightward shift caused by a non-price factor; an increase in quantity supplied is an extension along the curve caused by a rise in the good’s own price.', '1 mark each [2]'),
])
classify(t7_3, SUP_CASES, SUP_LABELS, 'What is the effect on the supply curve of {mgood}?', 'For each change, state the effect on the supply curve and explain why.', name='supply')
items(t7_3, 'C2', (1, 2, 3, 4), [
    ('The cost of electricity rises sharply in {country}. Explain the effect on the supply of {mgood}.', 'Electricity is a cost of production: higher costs reduce profitability at every price, so supply falls (curve shifts left).', '1 mark: higher costs; 1 mark: shift left [2]'),
    ('Farmers in {country} expect the price of their crop to rise next year. Explain why current supply may fall.', 'Farmers hold back stocks to sell later at the higher price, so current supply shifts left.', '1 mark: withhold stock; 1 mark: current supply falls [2]'),
])
errs(t7_3, [
    ('A rise in the price of {mgood} shifts the supply curve to the right.', 'A rise in the good’s own price causes an extension along the supply curve, not a shift.'),
    ('A subsidy to producers shifts the supply curve to the left because the government pays part of the price.', 'A subsidy lowers producers’ costs, so supply increases: the curve shifts to the right.'),
])


@t7_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t7_3_sup(r, D):
    g = r.choice(MGOODS)
    c = r.choice([-20, -10, 0, 10, 20, 30])
    d = r.choice([2, 3, 4, 5])
    P0, P1 = r.sample([5, 8, 10, 12, 15, 20], 2)
    if c + d * min(P0, P1) <= 0:
        return None
    q0, q1 = c + d * P0, c + d * P1
    stem = f'The supply of {g} is given by {qs_s(c, d)}, where Q is in thousands of units and P in dollars.'
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the quantity supplied when the price is ${P1}.', f'{q1} thousand', f'{c} + {d} × {P1} = {q1}.', [f'{x} thousand' for x in (q1 + d, q1 - d, d * P1, q1 + 2 * d)], mcq_D=(1, 2))
    k = r.choice([10, 15, 20])
    return {'stem': stem + f' (a) Calculate the change in quantity supplied when the price changes from ${P0} to ${P1}. (b) A new technology increases supply by {k} thousand units at every price. Write the new supply equation and calculate the quantity supplied at ${P1}. (c) Distinguish between the two changes in (a) and (b).',
            'answer': f'(a) {q0} → {q1}: {sgn(q1 - q0, 0)} thousand. (b) {qs_s(c + k, d)}; {q1 + k} thousand. (c) (a) is a movement along the supply curve (own price); (b) is a rightward shift (non-price factor).',
            'key': f'(a) [1] (b) equation [1]; quantity [1] (c) movement vs shift [2] [5]', 'marks': 5, 'type': 'multi_step'}


def _ch7_case(r, D):
    d = ctx(r)
    p0, p1 = r.choice([(2.0, 2.6), (3.0, 3.9), (1.5, 2.1)])
    inc = r.choice([3, 4, 5])
    intro = (f'Extract: The price of coffee beans on world markets rose from ${p0} to ${p1} per kilogram after frosts damaged crops in major producing countries. '
             f'In {d["country"]}, cafés raised the price of a cup of coffee, yet the number of cups sold in {d["city"]} still rose slightly because incomes grew by {inc}% and coffee became more fashionable among young people. Sales of tea fell.')
    parts = [
        lambda r: ('Calculate the percentage increase in the world price of coffee beans.', pct(chg(p0, p1)), f'({p1} − {p0})/{p0} × 100 [2]'),
        lambda r: ('Explain the effect of the frosts on the supply curve of coffee beans.', 'Shift to the left: fewer beans available at every price.', '[2]'),
        lambda r: ('Explain why sales of cups of coffee rose despite the higher price.', 'Demand shifted right (higher incomes, fashion) by more than the contraction caused by the price rise.', '[3]'),
        lambda r: ('Explain why sales of tea fell.', 'Changes in tastes towards coffee shifted demand for tea (a substitute) to the left.', '[2]'),
        lambda r: ('Discuss whether the rise in coffee prices is likely to be permanent.', 'Supply recovers after frosts (new crops), new producers enter; but climate change may cause repeated shocks; demand growth persists; judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t7_1, t7_2, t7_3], _ch7_case)
essay(t7_1, [
    ('Explain the law of demand and how a market demand curve is derived.',
     'Effective demand; inverse P–Qd relationship; income and substitution effects; diminishing marginal utility; horizontal summation of individual demand curves; diagram.',
     'price is the most important influence on the quantity of {good} that consumers buy',
     'Law of demand; price changes cause large movements for elastic goods.',
     'Income, tastes, advertising and prices of related goods shift demand; for necessities price matters little; depends on PED and time period.'),
])
essay(t7_2, [
    ('With the help of diagrams, explain the difference between a movement along and a shift of a demand curve.',
     'Own price → extension/contraction; conditions of demand (income, related goods, tastes, population, expectations) → shift; diagrams showing both.',
     'changes in income are the main reason for shifts in the demand for {good}',
     'Normal goods respond strongly to income (YED); recessions shift demand.',
     'Tastes, advertising, substitutes/complements, population and expectations also matter; depends on the good (necessity vs luxury) and the period.'),
])
essay(t7_3, [
    ('Explain why the supply curve slopes upwards and the factors that can cause it to shift.',
     'Profit motive, rising marginal cost, entry of firms; shifts from costs, technology, taxes/subsidies, weather, number of firms, expectations; diagram.',
     'technological change is the most important cause of increases in supply in the long run',
     'Lowers unit costs and raises productivity; major shifts in agriculture and electronics.',
     'Factor prices, government taxes and subsidies, entry of firms and weather also shift supply; in the short run weather/costs dominate; depends on industry.'),
])
CHAPTERS[7] = [t7_1, t7_2, t7_3]

# ============================================================================ 8 PED, YED and XED
def ped_word(e):
    e = abs(e)
    if e == 0:
        return 'perfectly inelastic'
    if abs(e - 1) < 1e-9:
        return 'unitary elastic'
    return 'price elastic' if e > 1 else 'price inelastic'


def _pq(r):
    """Price and quantity pair with a clean percentage change."""
    for _ in range(40):
        p0 = r.choice([2, 4, 5, 8, 10, 12, 20, 25, 40, 50])
        dp = r.choice([5, 10, 20, 25, 50]) * r.choice([1, -1])
        e = r.choice([0.2, 0.4, 0.5, 0.6, 0.8, 1, 1.2, 1.5, 2, 2.5, 3])
        q0 = r.choice([100, 200, 400, 500, 800, 1000, 1200, 2000])
        p1 = p0 * (1 + dp / 100)
        dq = -e * dp
        q1 = q0 * (1 + dq / 100)
        if abs(q1 - round(q1)) < 1e-9 and q1 > 0 and abs(p1 * 100 - round(p1 * 100)) < 1e-6:
            return p0, p1, q0, int(round(q1)), -e
    return 10, 12, 1000, 900, -0.5


t8_1 = T('Price elasticity of demand: calculation, values and determinants', 'price elasticity of demand', 'determinants', 'ped')
mc(t8_1, [
    ('How is price elasticity of demand calculated?', 'Percentage change in quantity demanded ÷ percentage change in price', 'PED = %ΔQd / %ΔP (usually negative).',
     ['Percentage change in price ÷ percentage change in quantity demanded', 'Change in quantity demanded ÷ change in price', 'Percentage change in demand ÷ percentage change in income']),
    ('If PED is −0.4, demand is', 'price inelastic', '|PED| < 1: inelastic.', ['price elastic', 'unitary elastic', 'perfectly elastic']),
    ('Which factor makes demand for a good more price elastic?', 'The availability of many close substitutes', 'Substitutes, luxury, large share of income, longer time period, broad vs narrow definition.',
     ['The good is a necessity', 'The good takes a very small share of income', 'The good is habit-forming']),
    ('A vertical demand curve has a PED of', 'zero (perfectly inelastic)', 'Quantity does not respond to price.', ['infinity', 'one', 'minus one']),
    ('Why is PED usually negative?', 'Price and quantity demanded move in opposite directions', 'Law of demand.', ['Prices are always falling', 'Demand curves slope upwards', 'Quantity demanded never changes']),
    ('Why is demand for petrol more price elastic in the long run than in the short run?', 'Consumers have more time to find substitutes such as electric cars or public transport', 'Time allows adjustment.',
     ['Petrol prices fall in the long run', 'Petrol becomes a necessity over time', 'Incomes always rise in the long run']),
])
ex(t8_1, [
    ('Explain two determinants of the price elasticity of demand for a good.', 'Number and closeness of substitutes (more substitutes → more elastic); proportion of income spent (larger → more elastic); necessity vs luxury; habit/addiction; time period; breadth of definition.',
     '1 mark each determinant, 1 mark each explained with direction [4]'),
    ('Explain why the demand for a particular brand of coffee is likely to be more price elastic than the demand for coffee in general.', 'A single brand has many close substitutes (other brands) whereas coffee as a whole has few, so consumers switch brands easily when one brand’s price rises.',
     '1 mark: brand has close substitutes; 1 mark: product as a whole has fewer [2]'),
    ('Explain what is meant by a PED value of −2.', 'A 1% rise in price causes a 2% fall in quantity demanded; demand is price elastic because the quantity response is proportionately greater than the price change.', '1 mark: interpretation; 1 mark: elastic [2]'),
])
items(t8_1, 'C2', (1, 2, 3, 4), [
    ('The price of cigarettes in {country} rises by 10% but the quantity bought falls by only 3%. Explain why demand is so unresponsive.', 'Cigarettes are addictive and have few close substitutes, so demand is price inelastic (PED ≈ −0.3).', '1 mark: PED inelastic value; 1 mark: addiction/few substitutes [2]'),
    ('An airline cuts fares on the route from {city} to a holiday island and sales rise sharply. Explain why demand may be price elastic.', 'Holiday flights are a luxury with many substitutes (other airlines, destinations) and take a large share of income, so demand responds strongly.', '1 mark: identifies elastic; 1 mark: reason [2]'),
])
errs(t8_1, [
    ('If PED is −0.5, a 10% rise in price will cause a 50% fall in quantity demanded.', '%ΔQd = PED × %ΔP = −0.5 × 10% = −5%, not −50%.'),
    ('A good with a PED of −3 is price inelastic because the number is negative.', '|PED| = 3 > 1, so demand is price elastic; the minus sign only shows the inverse relationship.'),
    ('Elasticity is the same as the slope of the demand curve.', 'Elasticity measures proportionate (percentage) changes; on a straight-line demand curve the slope is constant but PED varies along it.'),
])


@t8_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t8_1_ped(r, D):
    g = r.choice(GOODS_P)
    p0, p1, q0, q1, e = _pq(r)
    dp, dq = chg(p0, p1), chg(q0, q1)
    stem = f'When the price of {g} {"rises" if p1 > p0 else "falls"} from {money(p0)} to {money(p1)}, the quantity demanded {"falls" if q1 < q0 else "rises"} from {q0:,} to {q1:,} units a week.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the price elasticity of demand.', num(e, 2), f'%ΔQd = {pchg(dq)}; %ΔP = {pchg(dp)}; PED = {num(dq, 1)}/{num(dp, 1)} = {num(e, 2)}.',
                  [num(x, 2) for x in (1 / e, -e, e * 2, e / 2, e - 1)], mcq_D=(1, 2))
    tr0, tr1 = p0 * q0, p1 * q1
    return {'stem': stem + ' (a) Calculate the price elasticity of demand and state whether demand is elastic or inelastic. (b) Calculate the change in total revenue. (c) Suggest two reasons why demand for ' + g + ' might have this elasticity.',
            'answer': f'(a) PED = {num(e, 2)}: {ped_word(e)}. (b) TR {money(tr0)} → {money(tr1)}, change {money(tr1 - tr0)}. (c) ' + ('Few close substitutes, necessity, habit, small share of income.' if abs(e) < 1 else 'Many close substitutes, luxury, large share of income.' if abs(e) > 1 else 'Proportionate response equal to price change (unit elasticity).'),
            'key': f'(a) {num(dq, 1)}/{num(dp, 1)} = {num(e, 2)} [1]; interpretation [1] (b) {num(tr0)} → {num(tr1)} [2] (c) two consistent reasons [2] [6]', 'marks': 6, 'type': 'multi_step'}


@t8_1.add('C3', (2, 3, 4, 5), 'numerical')
def t8_1_pred(r, D):
    g = r.choice(GOODS_P)
    e = r.choice([-0.2, -0.3, -0.4, -0.5, -0.8, -1.2, -1.5, -2, -2.5])
    dp = r.choice([4, 5, 8, 10, 12, 15, 20]) * r.choice([1, -1])
    q0 = r.choice([2000, 4000, 5000, 8000, 10000])
    dq = e * dp
    q1 = q0 * (1 + dq / 100)
    stem = f'The PED for {g} in {r.choice(COUNTRIES)} is estimated at {num(e, 1)}. Weekly sales are {q0:,} units. The price is {"raised" if dp > 0 else "cut"} by {abs(dp)}%.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the new weekly sales.', f'{num(q1)} units', f'%ΔQd = {num(e, 1)} × {sgn(dp, 0)}% = {pchg(dq)}; {q0:,} × {num(1 + dq / 100, 3)} = {num(q1)}.',
                  [f'{num(x)} units' for x in (q0 * (1 - dq / 100), q0 * (1 + dp / 100), q0 * (1 + dq / 1000), q0 + dq)], mcq_D=(2,))
    return {'stem': stem + ' (a) Calculate the percentage change in quantity demanded and the new weekly sales. (b) State and explain whether total revenue will rise or fall.',
            'answer': f'(a) {pchg(dq)}; {num(q1)} units. (b) ' + ('Demand is inelastic, so TR moves in the same direction as price: ' + ('rises.' if dp > 0 else 'falls.') if abs(e) < 1 else 'Demand is elastic, so TR moves in the opposite direction to price: ' + ('falls.' if dp > 0 else 'rises.')),
            'key': f'(a) {num(e, 1)} × {sgn(dp, 0)} = {pchg(dq)} [1]; {num(q1)} [1] (b) PED–TR link [1]; direction [1] [4]', 'marks': 4, 'type': 'numerical'}


t8_2 = T('PED and total revenue: implications for firms and government', 'ped and total revenue', 'implications for firms and government', 'total revenue')
mc(t8_2, [
    ('If demand is price inelastic, what happens to total revenue when price rises?', 'It rises', 'Inelastic: %ΔQ < %ΔP so TR moves with price.', ['It falls', 'It stays the same', 'It becomes zero']),
    ('If demand is price elastic, a firm that wants to raise total revenue should', 'cut its price', 'Elastic: TR moves opposite to price.', ['raise its price', 'keep its price unchanged', 'reduce output']),
    ('At which PED is total revenue unchanged after a small price change?', 'Unitary (−1)', 'Unit elasticity: %ΔQ = %ΔP.', ['Zero', 'Infinity', '−0.5']),
    ('Why do governments tend to place indirect taxes on goods with price inelastic demand?', 'Sales fall little, so tax revenue is high', 'Inelastic demand → stable tax base.', ['To reduce consumption sharply', 'Because these goods are luxuries', 'To lower prices for consumers']),
    ('A firm raises its price by 10% and total revenue falls. What does this show about demand?', 'It is price elastic', 'TR fell when price rose → %ΔQ > %ΔP.', ['It is price inelastic', 'It is unitary elastic', 'It is perfectly inelastic']),
])
ex(t8_2, [
    ('Explain why a firm needs to know the PED for its product before changing its price.', 'PED shows whether a price change will raise or lower total revenue: with inelastic demand a price rise raises TR; with elastic demand a price cut raises TR.', '1 mark: link to TR; 1 mark: elastic vs inelastic case [2]'),
    ('Explain why an indirect tax on a good with inelastic demand may raise revenue but do little to reduce consumption.', 'With inelastic demand the quantity bought falls only a little when the tax raises price, so the tax base stays large (high revenue) and consumption changes little.', '1 mark: small fall in Q; 1 mark: high revenue/little behaviour change [2]'),
    ('Explain how a firm might make demand for its product less price elastic.', 'Branding and advertising to build loyalty, product differentiation, reducing close substitutes (e.g. by takeovers), loyalty schemes.', '1 mark each method explained [2]'),
])
items(t8_2, 'C2', (1, 2, 3, 4), [
    ('A bus company in {city} raised fares by 20% and its revenue fell. Explain what this suggests about the PED for its services.', 'Revenue fell, so the percentage fall in passengers exceeded 20%: demand is price elastic (|PED| > 1), perhaps because of substitutes such as cars, cycling or rival buses.', '1 mark: elastic; 1 mark: explanation [2]'),
    ('The government of {country} wants to raise more revenue from a tax on {good}. Explain why PED matters.', 'If demand is inelastic, the tax will reduce sales little and raise more revenue; if elastic, sales fall a lot and revenue may be low.', '1 mark: inelastic → revenue; 1 mark: elastic → falling base [2]'),
])
errs(t8_2, [
    ('Raising the price always increases a firm’s total revenue.', 'Only if demand is price inelastic; if demand is elastic, total revenue falls when price rises.'),
    ('If demand is price elastic, a firm should raise its price to increase revenue.', 'With elastic demand, a price rise causes a proportionately larger fall in quantity, so revenue falls; a price cut would raise revenue.'),
])


@t8_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t8_2_tr(r, D):
    f = r.choice(FIRMS)
    g = r.choice(GOODS_P)
    p0, p1, q0, q1, e = _pq(r)
    tr0, tr1 = p0 * q0, p1 * q1
    stem = f'{f} changes the price of its {g} from {money(p0)} to {money(p1)}. Weekly sales change from {q0:,} to {q1:,}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the change in total revenue.', money(tr1 - tr0), f'TR = P × Q: {num(tr0)} → {num(tr1)}; change {money(tr1 - tr0)}.',
                  dis_num(r, tr1 - tr0, money, [tr0 - tr1, p1 * q0 - tr0, (p1 - p0) * (q1 - q0)]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate total revenue before and after the change. (b) Calculate the PED and explain how it accounts for the change in total revenue. (c) Explain why the firm should also consider its costs before deciding on the price.',
            'answer': f'(a) {money(tr0)} → {money(tr1)}. (b) PED = {num(e, 2)} ({ped_word(e)}): ' + ('price and TR move in the same direction.' if abs(e) < 1 else 'price and TR move in opposite directions.' if abs(e) > 1 else 'TR unchanged.') +
                      ' (c) Profit = TR − TC; a change in output changes total cost, so higher TR does not necessarily mean higher profit.',
            'key': '(a) both [2] (b) PED [1]; link to TR [1] (c) profit vs revenue [1] [5]', 'marks': 5, 'type': 'multi_step'}


t8_3 = T('Income elasticity of demand: normal, inferior, necessity and luxury goods', 'income elasticity of demand', 'normal, inferior, necessity and luxury', 'yed')
mc(t8_3, [
    ('How is income elasticity of demand calculated?', 'Percentage change in quantity demanded ÷ percentage change in income', 'YED = %ΔQd / %ΔY.',
     ['Percentage change in income ÷ percentage change in quantity demanded', 'Percentage change in quantity demanded ÷ percentage change in price', 'Change in income ÷ change in price']),
    ('A good with a YED of −0.6 is', 'an inferior good', 'Negative YED: demand falls as income rises.', ['a luxury good', 'a necessity', 'a substitute']),
    ('A good with a YED of +2.1 is', 'a luxury (income elastic normal) good', 'YED > 1.', ['a necessity', 'an inferior good', 'a complement']),
    ('A good with a YED of +0.3 is', 'a necessity (income inelastic normal good)', '0 < YED < 1.', ['an inferior good', 'a luxury good', 'a Giffen good']),
    ('Why is YED useful to firms?', 'It helps them predict how sales will change as the economy grows or contracts', 'Planning output and product range over the cycle.',
     ['It shows the effect of a price change on sales', 'It measures the effect of a rival’s price change', 'It shows how much tax to pay']),
])
ex(t8_3, [
    ('Explain the difference between a normal good and an inferior good, using income elasticity of demand.', 'Normal good: YED positive, demand rises as income rises. Inferior good: YED negative, demand falls as income rises because consumers switch to better-quality alternatives.', '1 mark each [2]'),
    ('Explain why a firm producing a luxury good might be worried about a recession.', 'Luxuries have YED > 1, so a fall in incomes causes a proportionately larger fall in demand and sales.', '1 mark: YED > 1; 1 mark: large fall in sales [2]'),
    ('Explain why the same good may be normal for some consumers and inferior for others.', 'At low incomes a good (e.g. bus travel) may be a step up and demand rises with income; at higher incomes people switch to better alternatives (cars), so demand falls.', '1 mark: income level matters; 1 mark: example [2]'),
])
items(t8_3, 'C2', (1, 2, 3, 4), [
    ('As incomes in {country} rose, sales of cheap instant noodles fell while sales of restaurant meals rose strongly. Explain what this shows about the income elasticities of the two goods.', 'Instant noodles: negative YED (inferior). Restaurant meals: positive and probably > 1 (luxury).', '1 mark each [2]'),
    ('{firm} sells both budget and premium {good}. Explain why it might shift production towards its premium range as {country}’s economy grows.', 'Premium products likely have higher (positive) YED, so their demand grows faster with incomes, while budget versions may be inferior.', '1 mark: premium high YED; 1 mark: budget low/negative YED [2]'),
])
errs(t8_3, [
    ('A good with a YED of 0.5 is an inferior good because the value is less than one.', 'A positive YED below 1 shows a normal necessity; a good is inferior only when YED is negative.'),
    ('Inferior goods are goods of poor quality.', 'Inferior goods are defined by negative YED: demand falls as income rises, regardless of quality.'),
])


def yed_word(e):
    if e < 0:
        return 'inferior good'
    if e > 1:
        return 'luxury (normal, income elastic) good'
    return 'necessity (normal, income inelastic) good'


@t8_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t8_3_yed(r, D):
    g = r.choice(GOODS)
    y0 = r.choice([20000, 25000, 30000, 40000])
    dy = r.choice([4, 5, 8, 10])
    e = r.choice([-1.5, -0.8, -0.5, 0.2, 0.4, 0.6, 1.5, 2, 2.5])
    q0 = r.choice([1000, 2000, 4000, 5000])
    q1 = q0 * (1 + e * dy / 100)
    y1 = y0 * (1 + dy / 100)
    stem = f'Average income in {r.choice(COUNTRIES)} rose from ${y0:,} to ${num(y1)}, and monthly sales of {g} changed from {q0:,} to {num(q1)} units.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the income elasticity of demand.', sgn(e, 2) if e > 0 else num(e, 2), f'%ΔQ = {pchg(e * dy)}; %ΔY = {dy}%; YED = {num(e, 2)}.',
                  [num(x, 2) for x in (1 / e, -e, e * 2, e / 2) if num(x, 2) != num(e, 2)] + ['0'], mcq_D=(1, 2)) if False else cq(
            r, 1, stem + ' Calculate the income elasticity of demand.', num(e, 2), f'%ΔQ = {pchg(e * dy)}; %ΔY = {dy}%; YED = {num(e, 2)}.', [num(x, 2) for x in (1 / e, -e, e * 2, e / 2)], mcq_D=(1, 2))
    return {'stem': stem + f' (a) Calculate the YED and classify the good. (b) Explain how {"a retailer" if e > 0 else "a discount retailer"} could use this information if incomes are expected to fall next year.',
            'answer': f'(a) YED = {num(e, 2)}: {yed_word(e)}. (b) ' + ('Sales will fall if incomes fall; ' + ('by more than the fall in income, so cut stocks and shift to cheaper lines.' if e > 1 else 'but less than proportionately, so sales are fairly stable.') if e > 0 else 'Sales will rise as incomes fall, so increase stocks/marketing of this good.'),
            'key': f'(a) {pchg(e * dy)}/{dy}% = {num(e, 2)} [2]; classification [1] (b) application to falling income [1] [4]', 'marks': 4, 'type': 'numerical'}


t8_4 = T('Cross elasticity of demand: substitutes, complements and unrelated goods', 'cross elasticity of demand', 'substitutes, complements and unrelated goods', 'xed')
mc(t8_4, [
    ('How is cross elasticity of demand between goods A and B calculated?', 'Percentage change in quantity demanded of A ÷ percentage change in price of B', 'XED = %ΔQd(A)/%ΔP(B).',
     ['Percentage change in price of A ÷ percentage change in quantity of B', 'Percentage change in quantity of A ÷ percentage change in price of A', 'Percentage change in quantity of A ÷ percentage change in income']),
    ('A positive XED between two goods shows that they are', 'substitutes', 'Price of B up → demand for A up.', ['complements', 'unrelated goods', 'inferior goods']),
    ('A negative XED between two goods shows that they are', 'complements', 'Price of B up → demand for A down.', ['substitutes', 'unrelated goods', 'luxury goods']),
    ('Which pair of goods is likely to have an XED close to zero?', 'Toothpaste and bicycles', 'Unrelated goods.', ['Tea and coffee', 'Printers and ink cartridges', 'Butter and margarine']),
    ('A large positive XED, such as +3, indicates that the goods are', 'close substitutes', 'Size of XED shows strength of relationship.', ['weak substitutes', 'close complements', 'unrelated']),
])
ex(t8_4, [
    ('Explain how a firm could use cross elasticity of demand when a rival cuts its price.', 'If XED with the rival’s product is high and positive, the firm will lose many sales and may need to respond (cut price or advertise); if low, it can ignore the change.', '1 mark: high XED → large effect; 1 mark: response [2]'),
    ('Explain why the XED between printers and ink cartridges is negative.', 'They are complements used together; a rise in the price of printers reduces printer sales and so demand for ink falls.', '1 mark: complements; 1 mark: direction explained [2]'),
    ('Explain what the size of XED shows about the relationship between two goods.', 'The larger the absolute value, the stronger the relationship: close substitutes have a large positive XED, close complements a large negative XED; near zero means unrelated.', '1 mark: magnitude = strength; 1 mark: sign = type [2]'),
])
items(t8_4, 'C2', (1, 2, 3, 4), [
    ('{firm} makes games consoles and video games. Explain why it might sell consoles at a low price.', 'Consoles and games are complements (negative XED): cheap consoles raise console sales and so raise demand for its profitable games.', '1 mark: complements; 1 mark: strategy explained [2]'),
    ('Bus fares in {city} rise by 10% and train journeys increase by 4%. Calculate the XED and explain the relationship.', 'XED = +4/10 = +0.4: weak substitutes.', '1 mark: +0.4; 1 mark: substitutes, weak [2]'),
])
errs(t8_4, [
    ('If the XED between two goods is negative, they are substitutes.', 'A negative XED shows complements; substitutes have a positive XED.'),
    ('XED measures how the demand for a good responds to a change in its own price.', 'XED measures the response of demand for one good to a change in the price of another good.'),
])


def xed_word(e):
    if abs(e) < 0.1:
        return 'unrelated goods'
    return ('strong ' if abs(e) >= 1 else 'weak ') + ('substitutes' if e > 0 else 'complements')


XPAIRS = [('tea', 'coffee', 1), ('butter', 'margarine', 1), ('printers', 'ink cartridges', -1), ('cars', 'petrol', -1), ('bus journeys', 'train journeys', 1),
          ('smartphones', 'phone cases', -1), ('cinema tickets', 'streaming subscriptions', 1), ('tennis rackets', 'tennis balls', -1), ('rice', 'bread', 1)]


@t8_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t8_4_xed(r, D):
    a, b, sign = r.choice(XPAIRS)
    dp = r.choice([5, 10, 20, 25])
    e = sign * r.choice([0.2, 0.4, 0.5, 0.8, 1.2, 1.5, 2])
    q0 = r.choice([500, 1000, 2000, 4000])
    q1 = q0 * (1 + e * dp / 100)
    stem = f'When the price of {b} rises by {dp}%, the quantity demanded of {a} changes from {q0:,} to {num(q1)} units a week.'
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the cross elasticity of demand for {a} with respect to the price of {b}.', num(e, 2), f'%ΔQ({a}) = {pchg(e * dp)}; ÷ {dp}% = {num(e, 2)}.',
                  [num(x, 2) for x in (-e, 1 / e, e * 2, e / 2)], mcq_D=(1, 2))
    return {'stem': stem + f' (a) Calculate the XED and identify the relationship between the goods. (b) Explain how a producer of {a} could use this information.',
            'answer': f'(a) XED = {num(e, 2)}: {xed_word(e)}. (b) ' + ('Monitor the rival good’s price; if its price rises, expect higher sales (and vice versa); price competitively, advertise to differentiate.' if e > 0 else 'Its sales depend on the complement’s price; it may offer bundles or joint promotions, or expect lower sales if the complement’s price rises.'),
            'key': f'(a) {pchg(e * dp)}/{dp}% [1]; sign and strength [1] (b) application [2] [4]', 'marks': 4, 'type': 'numerical'}


def _ch8_case(r, D):
    d = ctx(r)
    ped = r.choice([-0.3, -0.4, -0.6])
    yed = r.choice([1.5, 1.8, 2.2])
    xed = r.choice([0.6, 0.8, 1.2])
    tax = r.choice([10, 15, 20])
    intro = (f'Extract: Research for the government of {d["country"]} estimates that the PED for petrol is {ped}, the YED for air travel is +{yed} and the XED between bus travel and the price of petrol is +{xed}. '
             f'The government plans a tax that would raise the price of petrol by {tax}%. Incomes are forecast to grow by 3% next year.')
    parts = [
        lambda r: ('Calculate the expected percentage change in petrol consumption after the tax.', pchg(ped * tax), f'{ped} × {tax} [1]'),
        lambda r: ('Calculate the expected percentage change in demand for bus travel.', pchg(xed * tax), f'{xed} × {tax} [1]'),
        lambda r: ('Explain why the PED for petrol is likely to be inelastic.', 'Few close substitutes in the short run, necessity for commuting and business, habit.', '[2]'),
        lambda r: ('Calculate the expected change in demand for air travel and explain what the YED value shows.', f'{pchg(yed * 3)}; luxury good, demand grows faster than income.', '[2]'),
        lambda r: ('Discuss whether the petrol tax will achieve both a large rise in tax revenue and a large fall in pollution.', 'Inelastic demand → revenue rises but consumption falls little; conflict between objectives; long-run PED higher (electric cars, buses with XED > 0); estimates uncertain; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t8_1, t8_2, t8_3, t8_4], _ch8_case)
essay(t8_1, [
    ('Explain the factors that determine the price elasticity of demand for a product.',
     'Substitutes, proportion of income, necessity/luxury, habit, time period, definition of the market; examples; formula.',
     'the availability of substitutes is the most important determinant of PED for {good}',
     'Substitutes allow consumers to switch; brands vs product categories.',
     'Share of income, addiction, time period also important; depends on the product and consumers; time allows substitutes to emerge.'),
])
essay(t8_2, [
    ('Explain the relationship between price elasticity of demand and total revenue.',
     'Elastic: TR moves opposite to price; inelastic: same direction; unitary: unchanged; diagram of revenue areas; numerical example.',
     'knowledge of price elasticity of demand is essential for a government when choosing which goods to tax',
     'Inelastic goods raise revenue; elastic goods for behaviour change; predicting tax revenue and incidence.',
     'Estimates are unreliable; equity (regressive taxes on necessities); externalities and health objectives matter; PED changes over time.'),
])
essay(t8_3, [
    ('Explain how income elasticity of demand can be used to classify goods.',
     'YED formula; negative = inferior; 0–1 = necessity; > 1 = luxury; examples; usefulness for planning.',
     'income elasticity of demand is more useful than price elasticity of demand for a firm planning for the future',
     'Economic growth and recessions change incomes; product portfolio planning; YED predicts long-run trends.',
     'PED needed for pricing decisions; incomes forecasts uncertain; elasticities change; both useful for different decisions.'),
])
essay(t8_4, [
    ('Explain how cross elasticity of demand distinguishes substitutes, complements and unrelated goods.',
     'XED formula; sign: positive substitutes, negative complements, zero unrelated; magnitude = closeness; examples.',
     'firms should always respond to a price cut by a rival',
     'High positive XED means large loss of sales; maintain market share.',
     'Low XED means little effect; price wars reduce profit; non-price competition (branding) may be better; depends on costs and loyalty.'),
])
CHAPTERS[8] = [t8_1, t8_2, t8_3, t8_4]

# ============================================================================ 9 Price elasticity of supply
t9_1 = T('Price elasticity of supply: calculation and values', 'price elasticity of supply', 'calculation and values', 'pes')
mc(t9_1, [
    ('How is price elasticity of supply calculated?', 'Percentage change in quantity supplied ÷ percentage change in price', 'PES = %ΔQs/%ΔP; usually positive.',
     ['Percentage change in price ÷ percentage change in quantity supplied', 'Change in quantity supplied ÷ change in price', 'Percentage change in quantity demanded ÷ percentage change in price']),
    ('A PES of 0.3 means supply is', 'price inelastic', 'PES < 1.', ['price elastic', 'unitary elastic', 'perfectly elastic']),
    ('A vertical supply curve shows a PES of', 'zero', 'Quantity cannot respond to price.', ['one', 'infinity', 'minus one']),
    ('Any straight-line supply curve that passes through the origin has a PES of', 'one', 'Proportional relationship.', ['zero', 'infinity', 'less than one']),
    ('Why is PES normally positive?', 'Higher prices give producers an incentive to supply more', 'Law of supply.', ['Consumers buy more at higher prices', 'Costs fall at higher output', 'Supply curves slope downwards']),
])
ex(t9_1, [
    ('Explain what a PES value of 2.5 means.', 'A 1% rise in price leads to a 2.5% rise in quantity supplied: supply is price elastic, so producers can respond strongly.', '1 mark: interpretation; 1 mark: elastic [2]'),
    ('Explain the difference between perfectly elastic and perfectly inelastic supply.', 'Perfectly inelastic (PES = 0): quantity fixed whatever the price (vertical curve). Perfectly elastic (PES = ∞): any quantity supplied at one price (horizontal curve).', '1 mark each [2]'),
])
items(t9_1, 'C2', (1, 2, 3, 4), [
    ('The price of tickets for a football final in {city} doubles but the number of seats stays the same. Explain what this shows about PES.', 'Supply is perfectly inelastic (PES = 0): the stadium has a fixed capacity.', '1 mark: PES = 0; 1 mark: fixed capacity [2]'),
    ('{firm} can quickly increase production of {mgood} from its large stocks when the price rises. Explain the likely PES.', 'Elastic supply (PES > 1): stocks allow quantity supplied to rise more than proportionately to price.', '1 mark: elastic; 1 mark: stocks [2]'),
])
errs(t9_1, [
    ('A PES of 0.6 means supply is elastic because it is positive.', 'PES of 0.6 is less than 1, so supply is inelastic; nearly all PES values are positive.'),
    ('Price elasticity of supply measures how quantity supplied responds to changes in demand.', 'PES measures the responsiveness of quantity supplied to a change in the good’s price.'),
])


@t9_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t9_1_pes(r, D):
    g = r.choice(SUPPLY_P)
    p0 = r.choice([10, 20, 25, 40, 50])
    dp = r.choice([5, 10, 20, 25, 40])
    e = r.choice([0, 0.2, 0.4, 0.5, 0.8, 1, 1.5, 2, 3])
    q0 = r.choice([200, 500, 800, 1000, 2000])
    p1 = p0 * (1 + dp / 100)
    q1 = q0 * (1 + e * dp / 100)
    stem = f'When the price of {g} rose from {money(p0)} to {money(p1)}, the quantity supplied rose from {q0:,} to {num(q1)} units a month.' if e else f'When the price of {g} rose from {money(p0)} to {money(p1)}, the quantity supplied stayed at {q0:,} units a month.'
    w = 'perfectly inelastic' if e == 0 else 'unitary elastic' if e == 1 else ('price elastic' if e > 1 else 'price inelastic')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the price elasticity of supply.', num(e, 2), f'%ΔQs = {num(e * dp, 1)}%; %ΔP = {dp}%; PES = {num(e, 2)}.',
                  [num(x, 2) for x in (1 / e if e else 1, e * 2 if e else 0.5, e + 0.5, -e if e else 2, dp / 10)], mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the PES and state whether supply is elastic or inelastic. (b) Suggest two reasons why supply of ' + g + ' might have this elasticity.',
            'answer': f'(a) PES = {num(e, 2)}: {w}. (b) ' + ('Long production time, no spare capacity, few stocks, immobile factors.' if e < 1 else 'Spare capacity, stocks available, mobile factors, short production period.' if e > 1 else 'Producers can expand in proportion to price.'),
            'key': f'(a) {num(e * dp, 1)}/{dp} = {num(e, 2)} [2]; interpretation [1] (b) two consistent reasons [2] [5]', 'marks': 5, 'type': 'multi_step'}


t9_2 = T('Determinants of PES: time, spare capacity, stocks and factor mobility', 'determinants of pes', 'spare capacity', 'stocks and factor mobility')
mc(t9_2, [
    ('Which would make supply of a good more price elastic?', 'Firms have large stocks of finished goods', 'Stocks, spare capacity, factor mobility, time, short production period.',
     ['Firms are working at full capacity', 'Production takes several years', 'Factors of production are immobile']),
    ('Why is the supply of agricultural crops usually inelastic in the short run?', 'Crops take a long time to grow', 'Production lag.', ['Farmers have large spare capacity', 'Crops can be stored easily', 'Demand for food is inelastic']),
    ('How does spare capacity affect PES?', 'It makes supply more elastic', 'Output can be raised quickly without large cost increases.', ['It makes supply less elastic', 'It has no effect', 'It makes supply perfectly inelastic']),
    ('Why does PES tend to rise over time?', 'Firms can expand capacity and new firms can enter', 'Long run all factors variable.', ['Prices always rise over time', 'Demand becomes more elastic', 'Stocks run out']),
    ('Which factor makes supply less elastic?', 'Workers need specialist skills that take years to learn', 'Factor immobility.', ['Machines can be switched between products', 'Firms hold large stocks', 'There is high unemployment of suitable labour']),
])
ex(t9_2, [
    ('Explain two factors that determine the price elasticity of supply of a product.', 'Spare capacity; stocks; factor mobility; time period; length of production process; ease of entry.', '1 mark each factor, 1 mark each explained [4]'),
    ('Explain why the supply of housing in a city is likely to be price inelastic.', 'Building takes a long time, land is limited and planning permission is needed, so the number of homes cannot rise quickly when prices rise.', '1 mark: time/land; 1 mark: planning/limited response [2]'),
    ('Explain why manufactured goods often have more elastic supply than primary products.', 'Factories can use spare capacity, overtime and stocks quickly; crops and minerals depend on growing seasons and long development times.', '1 mark: manufactured flexibility; 1 mark: primary constraints [2]'),
])
PES_CASES = [
    ('A cocoa farmer in {country} must wait four years for new trees to produce beans.', 'Inelastic supply', 'long production lag.'),
    ('{firm} operates its {mgood} factory at only 60% of capacity.', 'Elastic supply', 'spare capacity allows output to rise quickly.'),
    ('A warehouse in {city} holds large stocks of {mgood}.', 'Elastic supply', 'stocks can be released quickly.'),
    ('Only a few highly trained surgeons can perform a new operation in {country}.', 'Inelastic supply', 'specialist skills make labour immobile in the short run.'),
    ('Rare paintings by a famous artist who has died.', 'Perfectly inelastic supply', 'no more can be produced.'),
    ('A bakery in {city} can easily switch its ovens from bread to cakes.', 'Elastic supply', 'factors are mobile between uses.'),
    ('Seats in a concert hall in {city} for tonight’s performance.', 'Perfectly inelastic supply', 'capacity is fixed in the market period.'),
]
classify(t9_2, PES_CASES, ['Elastic supply', 'Inelastic supply', 'Perfectly inelastic supply'], 'What is the likely price elasticity of supply?', 'For each case, identify the likely price elasticity of supply and explain why.', extra=['Perfectly elastic supply'])
items(t9_2, 'C2', (1, 2, 3, 4), [
    ('The price of {mgood} in {country} rises sharply but firms are already operating at full capacity. Explain the likely effect on output in the short run.', 'Supply is inelastic: without spare capacity or stocks, output can rise only slightly, so most of the effect is on price.', '1 mark: inelastic; 1 mark: little output response [2]'),
])
errs(t9_2, [
    ('Supply of crops is elastic in the short run because farmers can plant more seeds immediately.', 'Crops take months or years to grow, so supply is inelastic in the short run.'),
    ('Having more spare capacity makes supply less elastic.', 'Spare capacity makes supply more elastic because output can be increased quickly.'),
])


@t9_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t9_2_time(r, D):
    g = r.choice(['apartments in ' + r.choice(CITIES_PG), 'coffee beans', 'electric scooters', 'fresh salmon', 'solar panels'])
    dp = r.choice([10, 20, 25])
    qs = r.choice([2, 3, 4, 5])
    ql = r.choice([15, 20, 25, 30, 40])
    es, el = qs / dp, ql / dp
    stem = f'After a {dp}% rise in the price of {g}, the quantity supplied rose by {qs}% within three months and by {ql}% after three years.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the long-run PES.', num(el, 2), f'{ql}/{dp} = {num(el, 2)}.', dis_num(r, el, lambda v: num(v, 2), [es, dp / ql, el + 1]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the short-run and long-run PES. (b) Explain why the two values differ.',
            'answer': f'(a) SR {num(es, 2)}, LR {num(el, 2)}. (b) In the short run capacity and other factors are fixed; over time firms invest in new capacity, new firms enter and factors move, so supply becomes more elastic.',
            'key': f'(a) {qs}/{dp} and {ql}/{dp} [2] (b) fixed factors in SR [1]; capacity/entry in LR [1] [4]', 'marks': 4, 'type': 'numerical'}


t9_3 = T('Significance of PES for producers and markets', 'significance of pes', 'producers and markets')
mc(t9_3, [
    ('If supply is price inelastic, an increase in demand will mainly cause', 'a large rise in price and a small rise in quantity', 'Inelastic supply: price absorbs most of the change.',
     ['a large rise in quantity and a small rise in price', 'no change in price', 'a fall in quantity']),
    ('Why do prices of agricultural products tend to be volatile?', 'Supply is inelastic in the short run and affected by weather', 'Inelastic supply + supply shocks + inelastic demand.', ['Supply is perfectly elastic', 'Demand is very elastic', 'Governments set prices']),
    ('Why might a firm want to make its supply more elastic?', 'To be able to take advantage of rises in demand quickly', 'Flexibility gains sales and market share.', ['To keep prices high', 'To reduce output', 'To avoid competition']),
    ('With perfectly elastic supply, an increase in demand leads to', 'a rise in quantity with no change in price', 'Horizontal supply.', ['a rise in price only', 'a fall in quantity', 'no change in quantity']),
])
ex(t9_3, [
    ('Explain why the elasticity of supply affects how much the price changes when demand rises.', 'If supply is elastic, output expands easily so most of the adjustment is in quantity and price rises little; if inelastic, output cannot expand, so price rises a lot.', '1 mark: elastic case; 1 mark: inelastic case [2]'),
    ('Explain how firms might increase the price elasticity of supply of their products.', 'Hold stocks; keep spare capacity; use flexible labour contracts and multi-skilled workers; adopt technology that shortens production time.', '1 mark each method [2]'),
])
items(t9_3, 'C2', (1, 2, 3, 4), [
    ('Demand for flats in {city} has risen rapidly. Explain why prices have risen much more than the number of flats.', 'Supply of housing is inelastic (land, planning, construction time), so the increase in demand mainly raises price.', '1 mark: inelastic supply reasons; 1 mark: price effect [2]'),
    ('A sudden heatwave raises demand for fans in {country}. Explain why {firm}, which holds large stocks, could benefit more than its rivals.', 'Stocks make its supply elastic: it can increase sales quickly while rivals cannot, gaining revenue and market share.', '1 mark: elastic supply; 1 mark: benefit [2]'),
])
errs(t9_3, [
    ('If supply is inelastic, an increase in demand mainly increases the quantity sold.', 'With inelastic supply, quantity can rise only a little, so the main effect of higher demand is a large rise in price.'),
])


@t9_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t9_3_shift(r, D):
    g = r.choice(['fresh fish', 'concert tickets', 'apartments', 'tomatoes', 'cement'])
    dq = r.choice([20, 30, 40])
    pes = r.choice([0.25, 0.5, 2, 4])
    ped = r.choice([-0.5, -1])
    # demand shifts right by dq% at the old price; new equilibrium: %ΔP = dq/(PES − PED)
    dp = dq / (pes - ped)
    qch = pes * dp
    stem = f'Demand for {g} increases so that, at the original price, buyers want {dq}% more. The PES is {num(pes, 2)} and the PED is {num(ped, 1)}.'
    if D <= 2:
        return cq(r, 2, stem + ' Which is the most likely outcome?', f'Price rises by about {num(dp, 1)}% and quantity by about {num(qch, 1)}%', f'%ΔP = {dq}/(PES − PED) = {dq}/{num(pes - ped, 2)} = {num(dp, 1)}%; %ΔQ = PES × %ΔP = {num(qch, 1)}%.',
                  [f'Price rises by about {num(x, 1)}% and quantity by about {num(y, 1)}%' for x, y in ((qch, dp), (dq, 0), (0, dq), (dp * 2, qch / 2))], mcq_D=(1, 2, 3))
    return {'stem': stem + ' (a) Using %ΔP = (shift in demand %) ÷ (PES − PED), calculate the percentage change in price and in quantity. (b) Explain why the effect on price would be different if supply were much more elastic.',
            'answer': f'(a) %ΔP ≈ {num(dp, 1)}%; %ΔQ ≈ {num(qch, 1)}%. (b) With more elastic supply, output expands more easily, so more of the adjustment is in quantity and the price rises less.',
            'key': f'(a) {dq}/{num(pes - ped, 2)} = {num(dp, 1)} [1]; {num(pes, 2)} × {num(dp, 1)} = {num(qch, 1)} [1] (b) elastic supply → smaller price rise [2] [4]', 'marks': 4, 'type': 'numerical'}


def _ch9_case(r, D):
    d = ctx(r)
    p0, p1 = r.choice([(200, 260), (300, 360), (150, 210)])
    q0, q1 = r.choice([(10000, 10400), (8000, 8200), (12000, 12600)])
    intro = (f'Extract: Average monthly rents for flats in {d["city"]} rose from ${p0} to ${p1} over two years, while the number of flats available rose from {q0:,} to {q1:,}. '
             f'Builders say planning rules and a shortage of skilled construction workers make it hard to build more quickly. In contrast, the supply of rental scooters in the city doubled within months when prices rose.')
    pes = chg(q0, q1) / chg(p0, p1)
    parts = [
        lambda r: ('Calculate the price elasticity of supply of flats.', num(pes, 2), f'{num(chg(q0, q1), 1)}% ÷ {num(chg(p0, p1), 1)}% [2]'),
        lambda r: ('Explain two reasons from the extract why the supply of flats is inelastic.', 'Planning rules (time lags) and shortage of skilled labour (factor immobility).', '[4]'),
        lambda r: ('Explain why the supply of rental scooters is more elastic than the supply of flats.', 'Scooters can be bought and delivered quickly; low capital cost; easy entry.', '[2]'),
        lambda r: ('Discuss policies that the government could use to make the supply of housing more elastic.', 'Relax planning rules, training for construction workers, release public land, subsidies; costs, environmental objections and time lags; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='case')


case([t9_1, t9_2, t9_3], _ch9_case)
essay(t9_1, [
    ('Explain how price elasticity of supply is measured and what different values show.',
     'PES formula; values 0, < 1, 1, > 1, ∞; diagrams of supply curves; examples.',
     'the supply of most goods in {country} is price inelastic',
     'Primary products and housing face time lags; full capacity in boom.',
     'Manufactured goods and services with spare capacity, stocks and mobile factors are elastic; depends on time period and state of the economy.'),
])
essay(t9_2, [
    ('Explain the factors that determine the price elasticity of supply.',
     'Time, spare capacity, stocks, factor mobility, production period, entry barriers; examples.',
     'time is the most important determinant of the price elasticity of supply',
     'Over time all factors become variable; capacity grows; entry.',
     'In the short run spare capacity and stocks decide; some goods fixed regardless of time (land, antiques); depends on industry.'),
])
essay(t9_3, [
    ('Explain, with the help of diagrams, why the effect of an increase in demand on price depends on the price elasticity of supply.',
     'Elastic supply: small price rise, large quantity rise; inelastic: large price rise; diagrams with the same demand shift.',
     'price instability in agricultural markets in {country} is mainly caused by inelastic supply',
     'Production lags and weather shocks with inelastic supply cause large price swings.',
     'Inelastic demand also matters; speculation and world markets; government policies; buffer stocks can help; combination.'),
])
CHAPTERS[9] = [t9_1, t9_2, t9_3]

# ============================================================================ 10 The interaction of demand and supply
t10_1 = T('Market equilibrium and disequilibrium: excess demand and excess supply', 'market equilibrium and disequilibrium', 'excess demand and excess supply', 'equilibrium')
mc(t10_1, [
    ('What is meant by market equilibrium?', 'A situation where quantity demanded equals quantity supplied and there is no tendency for price to change', 'Equilibrium: market clears.',
     ['A situation where all firms make a profit', 'A situation where price is set by the government', 'A situation where demand is greater than supply']),
    ('If the market price is above the equilibrium price, there will be', 'excess supply, putting downward pressure on price', 'Surplus → price falls.', ['excess demand', 'a shortage', 'no change in price']),
    ('If the market price is below the equilibrium price, there will be', 'excess demand, putting upward pressure on price', 'Shortage → price rises.', ['excess supply', 'a surplus', 'a fall in price']),
    ('How is excess demand removed in a free market?', 'Price rises, causing quantity demanded to contract and quantity supplied to extend', 'Price adjustment eliminates the shortage.', ['Demand shifts to the right', 'Supply shifts to the left', 'Price falls']),
    ('What is meant by disequilibrium?', 'A situation where quantity demanded and quantity supplied are not equal', 'Excess demand or excess supply exists.', ['A situation where prices are falling', 'A situation with no buyers', 'A market with only one seller']),
])
ex(t10_1, [
    ('Explain how a market moves to equilibrium if the price is initially above the equilibrium level.', 'There is excess supply: unsold stocks build up, so sellers cut prices; as price falls quantity demanded extends and quantity supplied contracts until they are equal.', '1 mark: excess supply; 1 mark: price falls; 1 mark: extensions/contractions to equilibrium [3]'),
    ('Explain why equilibrium is described as a position of rest.', 'At equilibrium buyers can buy all they want and sellers can sell all they want at that price, so there is no pressure for price to change unless conditions change.', '1 mark: market clears; 1 mark: no pressure to change [2]'),
])
items(t10_1, 'C2', (1, 2, 3, 4), [
    ('Tickets for a concert in {city} sold out in minutes and were resold online at three times the original price. Explain what this shows about the original price.', 'It was below equilibrium: excess demand meant some buyers were willing to pay much more, creating a secondary market.', '1 mark: below equilibrium/excess demand; 1 mark: resale price evidence [2]'),
    ('Unsold stocks of {mgood} are piling up in warehouses in {country}. Explain what will happen to the price in a free market.', 'Excess supply: firms cut prices to sell stocks; quantity demanded extends and quantity supplied contracts until equilibrium.', '1 mark: excess supply; 1 mark: price falls to equilibrium [2]'),
])
errs(t10_1, [
    ('When there is excess demand, the demand curve shifts to the left until the market clears.', 'Excess demand is removed by a rise in price along the existing curves (contraction of demand, extension of supply), not by a shift.'),
    ('At equilibrium, demand and supply are both at their maximum.', 'At equilibrium the quantity demanded equals the quantity supplied at the market price; neither is at a maximum.'),
])


@t10_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_1_eq(r, D):
    a, b, c, d, P, Q = lin(r)
    g = r.choice(GOODS)
    stem = f'The market for {g} in {r.choice(COUNTRIES)} is described by {qd_s(a, b)} and {qs_s(c, d)}, where Q is in thousands of units a week and P in dollars.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the equilibrium price.', money(P), f'{a} − {b}P = {c} + {d}P → {a - c} = {b + d}P → P = {P}.',
                  dis_num(r, P, money, [Q / 10, (a + c) / (b + d), a / b]), mcq_D=(1, 2))
    p2 = P + r.choice([-2, -1, 1, 2]) * max(1, P // 5)
    if p2 <= 0 or a - b * p2 <= 0 or c + d * p2 < 0:
        return None
    qd2, qs2 = a - b * p2, c + d * p2
    kind = 'excess demand' if qd2 > qs2 else 'excess supply'
    return {'stem': stem + f' (a) Calculate the equilibrium price and quantity. (b) Calculate the {"shortage" if qd2 > qs2 else "surplus"} if the price were ${p2}. (c) Explain how the market would return to equilibrium.',
            'answer': f'(a) P = {money(P)}, Q = {Q} thousand. (b) At ${p2}: Qd = {qd2}, Qs = {qs2}: {kind} of {abs(qd2 - qs2)} thousand. (c) ' + ('Price rises; Qd contracts and Qs extends until equal.' if qd2 > qs2 else 'Price falls; Qd extends and Qs contracts until equal.'),
            'key': f'(a) solve {a} − {b}P = {c} + {d}P [1]; P and Q [1] (b) Qd and Qs at ${p2} [1]; difference [1] (c) adjustment process [1] [5]', 'marks': 5, 'type': 'multi_step'}


@t10_1.add('C3', (1, 2, 3, 4), 'numerical')
def t10_1_table(r, D):
    g = r.choice(GOODS)
    prices = [2, 4, 6, 8, 10]
    a, b = r.choice([(120, 10), (100, 8), (150, 12)])
    c, d = r.choice([(0, 8), (10, 6), (-10, 10)])
    qd = [a - b * p for p in prices]
    qs = [c + d * p for p in prices]
    eq = [p for p, x, y in zip(prices, qd, qs) if x == y]
    if not eq:
        return None
    pe = eq[0]
    tab = table(['Price ($)', 'Quantity demanded', 'Quantity supplied'], list(zip(prices, qd, qs)))
    i = r.choice([k for k, p in enumerate(prices) if p != pe])
    stem = f'The table shows the demand and supply schedules for {g}. {tab}.'
    if D <= 2:
        return cq(r, 1, stem + ' What is the equilibrium price?', money(pe), f'At ${pe}, Qd = Qs = {a - b * pe}.', [money(p) for p in prices if p != pe], mcq_D=(1, 2))
    return {'stem': stem + f' (a) Identify the equilibrium price and quantity. (b) Calculate the excess demand or excess supply at ${prices[i]} and explain what will happen to price.',
            'answer': f'(a) ${pe}; {a - b * pe} units. (b) At ${prices[i]}: ' + (f'excess demand of {qd[i] - qs[i]}; price rises.' if qd[i] > qs[i] else f'excess supply of {qs[i] - qd[i]}; price falls.'),
            'key': '(a) price and quantity [2] (b) amount [1]; direction of price change [1] [4]', 'marks': 4, 'type': 'numerical'}


t10_2 = T('Effects of shifts in demand and supply on equilibrium price and quantity', 'effects of shifts in demand and supply', 'equilibrium price and quantity', 'shifts')
SHIFT_RES = {('D+', ''): ('rises', 'rises'), ('D-', ''): ('falls', 'falls'), ('S+', ''): ('falls', 'rises'), ('S-', ''): ('rises', 'falls')}
mc(t10_2, [
    ('What happens to equilibrium price and quantity when demand increases and supply is unchanged?', 'Both rise', 'Demand shifts right along an upward-sloping supply curve.', ['Price rises, quantity falls', 'Price falls, quantity rises', 'Both fall']),
    ('What happens to equilibrium price and quantity when supply increases and demand is unchanged?', 'Price falls and quantity rises', 'Supply shifts right along a downward-sloping demand curve.', ['Both rise', 'Both fall', 'Price rises and quantity falls']),
    ('If demand and supply both increase, which outcome is certain?', 'Equilibrium quantity rises', 'Both shifts raise quantity; price effect depends on relative sizes.', ['Equilibrium price rises', 'Equilibrium price falls', 'Equilibrium quantity falls']),
    ('If demand falls and supply rises, which outcome is certain?', 'Equilibrium price falls', 'Both shifts push price down; quantity indeterminate.', ['Equilibrium quantity falls', 'Equilibrium quantity rises', 'Equilibrium price rises']),
    ('A bad harvest reduces the supply of wheat. What is the effect on the market for wheat?', 'Price rises and quantity falls', 'Supply shifts left.', ['Price falls and quantity rises', 'Both rise', 'Both fall']),
])
ex(t10_2, [
    ('Explain, using demand and supply analysis, the effect of an increase in costs of production on a market.', 'Supply shifts left: at the original price there is excess demand, so price rises; quantity demanded contracts until the new equilibrium has a higher price and lower quantity.', '1 mark: supply shifts left; 1 mark: excess demand/price rises; 1 mark: new equilibrium higher P lower Q [3]'),
    ('Explain why the effect on equilibrium price is uncertain when demand and supply both increase.', 'The demand increase pushes price up while the supply increase pushes it down; the net effect depends on which shift is larger.', '1 mark: opposing pressures; 1 mark: depends on relative size [2]'),
])
SH_CASES = [
    ('A popular film increases the fashion for {good}.', 'Price rises, quantity rises', 'demand shifts right.'),
    ('New technology cuts the cost of producing {mgood}.', 'Price falls, quantity rises', 'supply shifts right.'),
    ('A tax is imposed on producers of {mgood}.', 'Price rises, quantity falls', 'supply shifts left.'),
    ('Incomes fall and consumers see {good} as a normal good.', 'Price falls, quantity falls', 'demand shifts left.'),
    ('A storm destroys much of the {country} banana crop.', 'Price rises, quantity falls', 'supply shifts left.'),
    ('The price of a substitute for {good} falls sharply.', 'Price falls, quantity falls', 'demand shifts left.'),
    ('The government gives a subsidy to producers of {mgood}.', 'Price falls, quantity rises', 'supply shifts right.'),
    ('The population of {city} increases rapidly, raising demand for housing.', 'Price rises, quantity rises', 'demand shifts right.'),
]
classify(t10_2, SH_CASES, ['Price rises, quantity rises', 'Price falls, quantity rises', 'Price rises, quantity falls', 'Price falls, quantity falls'],
         'What is the likely effect on the equilibrium price and quantity in the market?', 'For each event, state the effect on equilibrium price and quantity and explain why.', name='shifts')
items(t10_2, 'C2', (1, 2, 3, 4), [
    ('A new factory opens in {country} making {mgood}, at the same time as a successful advertising campaign for {mgood}. Explain the effect on the market.', 'Supply and demand both shift right: equilibrium quantity rises; price may rise or fall depending on the relative size of the shifts.', '1 mark: both shifts; 1 mark: Q rises, P indeterminate [2]'),
    ('A rise in the price of fuel increases airlines’ costs while a recession reduces demand for flights from {city}. Explain the effect on the market for flights.', 'Supply shifts left and demand shifts left: quantity falls; price may rise or fall depending on which shift is larger.', '1 mark: both shifts; 1 mark: Q falls, P indeterminate [2]'),
])
errs(t10_2, [
    ('An increase in supply raises the equilibrium price because more goods are sold.', 'An increase in supply creates excess supply at the old price, so the equilibrium price falls while quantity rises.'),
    ('If demand and supply both increase, the equilibrium price must rise.', 'Quantity must rise, but price may rise, fall or stay the same depending on the relative size of the shifts.'),
])


@t10_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_2_shift(r, D):
    a, b, c, d, P, Q = lin(r)
    g = r.choice(GOODS)
    side = r.choice(['D', 'S'])
    k = (b + d) * r.choice([1, 2, 3])
    sg = r.choice([1, -1])
    if side == 'D':
        a2, c2 = a + sg * k, c
        cause = r.choice(['a rise in incomes', 'a successful advertising campaign']) if sg > 0 else r.choice(['a fall in incomes', 'a health scare'])
    else:
        a2, c2 = a, c + sg * k
        cause = r.choice(['an improvement in technology', 'a fall in raw material costs']) if sg > 0 else r.choice(['a rise in wages', 'a new tax on producers'])
    P2 = (a2 - c2) / (b + d)
    Q2 = a2 - b * P2
    if P2 <= 0 or Q2 <= 0:
        return None
    new = qd_s(a2, b) if side == 'D' else qs_s(c2, d)
    stem = f'In the market for {g}, {qd_s(a, b)} and {qs_s(c, d)} (Q in thousands, P in dollars). After {cause}, the {"demand" if side == "D" else "supply"} equation becomes {new}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the new equilibrium price.', money(P2), f'{a2} − {b}P = {c2} + {d}P → P = {num(P2)}.', dis_num(r, P2, money, [P, P + (P - P2)]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the equilibrium price and quantity before and after the change. (b) Explain the process by which the market reaches the new equilibrium.',
            'answer': f'(a) Before: P = {money(P)}, Q = {Q}; after: P = {money(P2)}, Q = {num(Q2)}. (b) ' +
                      ({('D', 1): 'Demand shifts right: excess demand at the old price pushes price up; supply extends until a new equilibrium.',
                        ('D', -1): 'Demand shifts left: excess supply at the old price pushes price down; supply contracts.',
                        ('S', 1): 'Supply shifts right: excess supply at the old price pushes price down; demand extends.',
                        ('S', -1): 'Supply shifts left: excess demand at the old price pushes price up; demand contracts.'}[(side, sg)]),
            'key': '(a) old equilibrium [1]; new equilibrium [2] (b) shift, disequilibrium and adjustment [2] [5]', 'marks': 5, 'type': 'multi_step'}


REL_CASES = [
    ('Cars and petrol.', 'Joint demand', 'the goods are complements used together.'),
    ('Beef and leather.', 'Joint supply', 'producing one automatically produces the other.'),
    ('Steel used to make cars.', 'Derived demand', 'demand for steel depends on demand for the final product.'),
    ('Butter and margarine.', 'Competitive demand', 'the goods are substitutes competing for the same consumers.'),
    ('Milk, which is used for drinking, cheese, yoghurt and butter.', 'Composite demand', 'one good is demanded for several different uses.'),
    ('Construction workers needed to build new houses.', 'Derived demand', 'labour is demanded because of demand for houses.'),
    ('Wool and lamb meat from sheep.', 'Joint supply', 'both are produced from the same process.'),
    ('Tea and coffee.', 'Competitive demand', 'substitutes.'),
    ('Printers and ink cartridges.', 'Joint demand', 'complements used together.'),
    ('Oil, used for petrol, plastics and heating.', 'Composite demand', 'one good with several competing uses.'),
]
REL_LABELS = ['Joint demand', 'Joint supply', 'Derived demand', 'Competitive demand', 'Composite demand']

t10_3 = T('Related markets: joint, competitive, derived and composite demand; joint supply', 'related markets', 'joint, competitive, derived and composite demand', 'joint supply')
mc(t10_3, [
    ('What is meant by derived demand?', 'Demand for a good or factor that arises from the demand for another product', 'e.g. labour, raw materials.', ['Demand that comes from the government', 'Demand for luxury goods', 'Demand that is unrelated to price']),
    ('What is meant by joint supply?', 'Production of one good automatically leads to production of another', 'By-products: beef/leather.', ['Two firms supplying the same market', 'Goods that are used together', 'A good with several uses']),
    ('What is meant by composite demand?', 'A good that is demanded for more than one use', 'e.g. milk for drinking and cheese.', ['Demand for two goods used together', 'Demand for a factor of production', 'Demand from many consumers combined']),
    ('Which pair of goods is in joint demand?', 'Tennis rackets and tennis balls', 'Complements.', ['Tea and coffee', 'Beef and leather', 'Steel and cars']),
    ('A rise in demand for beef is likely to cause the price of leather to', 'fall, because the supply of leather increases', 'Joint supply: more beef → more hides.', ['rise', 'stay the same', 'rise, because leather is a complement']),
])
ex(t10_3, [
    ('Explain, with an example, how a change in the market for one good can affect the market for a good in joint supply.', 'More cattle are slaughtered when demand for beef rises, so the supply of leather increases; leather’s price falls and quantity rises.', '1 mark: example; 1 mark: supply shift; 1 mark: price/quantity effect [3]'),
    ('Explain why the demand for labour is described as a derived demand.', 'Firms hire workers not for their own sake but to produce goods and services that consumers demand; if demand for the product falls, demand for labour falls.', '1 mark: definition; 1 mark: link to product demand [2]'),
    ('Explain how composite demand can cause the price of a good to rise.', 'If demand for one use rises (e.g. milk for cheese), less is available for other uses at the original price, so the overall price rises and other users pay more.', '1 mark: competing uses; 1 mark: price effect [2]'),
])
classify(t10_3, REL_CASES, REL_LABELS, 'Which relationship between markets does this illustrate?', 'Identify the type of relationship in each case and explain your answer.', name='related')
items(t10_3, 'C2', (1, 2, 3, 4), [
    ('A boom in house building in {country} raises demand for bricks and cement. Explain the type of demand involved and its effect on the market for cement.', 'Derived demand: demand for cement comes from demand for houses; it shifts right, raising price and quantity of cement.', '1 mark: derived; 1 mark: market effect [2]'),
    ('The price of petrol in {country} rises sharply. Explain the effect on the market for large cars.', 'Joint demand: cars and petrol are complements, so demand for large cars falls (shift left), lowering their price and quantity.', '1 mark: joint demand; 1 mark: effect [2]'),
])
errs(t10_3, [
    ('Beef and leather are in joint demand because they come from the same animal.', 'They are in joint supply: producing one automatically produces the other.'),
    ('Tea and coffee are in joint demand.', 'Tea and coffee are substitutes: competitive demand. Joint demand refers to complements used together.'),
])


@t10_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_3_joint(r, D):
    c = r.choice(COUNTRIES)
    b0, b1 = r.choice([(100, 120), (200, 230), (400, 500)])
    hide = r.choice([1, 1])  # one hide per animal
    lp0 = r.choice([20, 25, 30, 40])
    pes = r.choice([0.5, 1])
    ped_l = r.choice([-0.5, -1, -2])
    pct_hides = chg(b0, b1)
    dp = pct_hides / (pes - ped_l)  # supply shift of leather: % change in price
    stem = f'In {c}, the number of cattle slaughtered for beef rose from {b0} thousand to {b1} thousand a year after demand for beef increased. Each animal provides one hide used for leather.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the percentage increase in the supply of hides.', pct(pct_hides), f'({b1} − {b0})/{b0} × 100.', dis_num(r, pct_hides, pct, [b1 - b0]), mcq_D=(1, 2))
    return {'stem': stem + f' The price of leather was ${lp0} per hide. (a) Calculate the percentage increase in the supply of hides. (b) Explain, with reference to joint supply, the likely effect on the price of leather. (c) Explain why the size of the effect depends on the price elasticity of demand for leather.',
            'answer': f'(a) {pct(pct_hides)} (b) Leather is in joint supply with beef: supply of hides shifts right, so the price of leather falls and quantity rises. (c) If demand for leather is inelastic, a large fall in price is needed to sell the extra hides; if elastic, price falls only slightly.',
            'key': '(a) [1] (b) joint supply [1]; supply shifts right, price falls [1] (c) PED explanation [2] [5]', 'marks': 5, 'type': 'multi_step'}


PM_CASES = [
    ('A rise in the price of {good} tells producers that consumers want more of it.', 'Signalling function', 'price changes convey information to producers and consumers.'),
    ('Higher profits from producing {good} encourage firms to switch resources into producing more of it.', 'Incentive function', 'the prospect of profit motivates producers to respond.'),
    ('When supplies of {good} run short, the higher price means only those most willing and able to pay obtain it.', 'Rationing function', 'price allocates scarce goods among buyers.'),
    ('A fall in the price of {mgood} tells firms to reduce output and move resources elsewhere.', 'Signalling function', 'information about changing demand.'),
    ('Rising wages for software engineers in {country} encourage more students to train in computing.', 'Incentive function', 'higher rewards motivate a change in behaviour.'),
    ('Hotel rooms in {city} during a festival go to those willing to pay the highest prices.', 'Rationing function', 'price allocates a limited number of rooms.'),
]

t10_4 = T('Functions of the price mechanism: signalling, incentive and rationing', 'functions of the price mechanism', 'signalling, incentive and rationing', 'price mechanism')
mc(t10_4, [
    ('Which function of the price mechanism allocates scarce goods to those most willing and able to pay?', 'Rationing', 'Higher prices ration limited supply.', ['Signalling', 'Incentive', 'Redistribution']),
    ('Which function of price provides information to producers and consumers about market conditions?', 'Signalling', 'Price changes are signals.', ['Rationing', 'Incentive', 'Taxation']),
    ('Which function of price encourages producers to supply more when demand rises?', 'Incentive', 'Higher profits motivate supply.', ['Rationing', 'Signalling', 'Planning']),
    ('In a market economy, how are resources moved from declining to growing industries?', 'Falling prices and profits in declining industries and rising ones in growing industries', 'Price mechanism reallocates resources.',
     ['By government direction', 'By trade union agreements', 'By random allocation']),
    ('Why might the rationing function of price be considered unfair?', 'Goods go to those with the most income, not necessarily those with the greatest need', 'Equity concern.', ['Prices never change', 'Producers cannot respond', 'Consumers have perfect information']),
])
ex(t10_4, [
    ('Explain the signalling, incentive and rationing functions of the price mechanism.', 'Signalling: price changes convey information about demand and supply. Incentive: higher prices/profits encourage producers to supply more (and consumers to buy less). Rationing: price allocates scarce goods to those willing and able to pay.',
     '1 mark each function [3]'),
    ('Explain how the price mechanism responds to an increase in demand for a product.', 'Price rises (signal); higher profits attract resources (incentive), raising supply; the higher price rations the good among buyers until a new equilibrium.', '1 mark each stage [3]'),
])
classify(t10_4, PM_CASES, ['Signalling function', 'Incentive function', 'Rationing function'], 'Which function of the price mechanism does this illustrate?',
         'Identify the function of the price mechanism shown in each case and explain it.', extra=['Redistribution function'], name='pricefn')
items(t10_4, 'C2', (1, 2, 3, 4), [
    ('Demand for electric bicycles in {city} has doubled. Explain how the price mechanism will respond.', 'Price rises, signalling higher demand; profits rise, giving an incentive to increase supply and enter the market; the higher price rations bikes until supply catches up.', '1 mark: signal; 1 mark: incentive; 1 mark: rationing [3]'),
    ('Explain one limitation of using price to allocate places at popular schools in {country}.', 'Places would go to the richest families, not those with the most need or ability; inequity and lost potential.', '1 mark: rationing by ability to pay; 1 mark: inequity/inefficiency [2]'),
])
errs(t10_4, [
    ('The rationing function of price means the government decides who gets scarce goods.', 'In the price mechanism, rationing happens through price: goods go to those willing and able to pay; government rationing is an alternative.'),
])


@t10_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_4_profit(r, D):
    g = r.choice(GOODS_P)
    p0, p1 = r.choice([(10, 14), (20, 26), (8, 11)])
    ac = r.choice([6, 7, 8]) if p0 > 8 else 6
    q0, q1 = r.choice([(1000, 1200), (2000, 2600), (500, 650)])
    pr0, pr1 = (p0 - ac) * q0, (p1 - ac) * q1
    stem = f'Demand for {g} rises and the price increases from ${p0} to ${p1}. Average cost stays at ${ac} per unit and sales rise from {q0:,} to {q1:,} a week.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the increase in weekly profit.', money(pr1 - pr0), f'({p1} − {ac}) × {q1} − ({p0} − {ac}) × {q0} = {num(pr1)} − {num(pr0)}.', dis_num(r, pr1 - pr0, money, [pr1, (p1 - p0) * q1]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate profit per unit and total weekly profit before and after. (b) Using the functions of the price mechanism, explain how resources will be reallocated.',
            'answer': f'(a) Per unit ${p0 - ac} → ${p1 - ac}; total {money(pr0)} → {money(pr1)}. (b) The price rise signals higher demand; higher profit gives an incentive for firms to expand and enter, moving resources from less profitable markets; meanwhile the higher price rations the good.',
            'key': '(a) per-unit and total profits [2] (b) signalling [1]; incentive and reallocation [1]; rationing [1] [5]', 'marks': 5, 'type': 'multi_step'}


def _ch10_case(r, D):
    d = ctx(r)
    a, b, c, dd, P, Q = lin(r)
    k = (b + dd) * r.choice([1, 2])
    P2 = (a - c + k) / (b + dd)
    Q2 = a + k - b * P2
    intro = (f'Extract: The market for {d["good"]} in {d["country"]} can be represented by {qd_s(a, b)} and {qs_s(c, dd)} (Q in thousands per month, P in dollars). '
             f'A popular social media campaign has increased demand by {k} thousand units at every price. Producers say they cannot increase output quickly because of a shortage of skilled workers.')
    parts = [
        lambda r: ('Calculate the original equilibrium price and quantity.', f'P = {money(P)}, Q = {Q}', f'Solve {a} − {b}P = {c} + {dd}P [2]'),
        lambda r: ('Calculate the excess demand at the original price after the campaign.', f'{k} thousand', f'New Qd at {P} = {Q + k}; Qs = {Q} [1]'),
        lambda r: ('Calculate the new equilibrium price and quantity.', f'P = {money(P2)}, Q = {num(Q2)}', f'{a + k} − {b}P = {c} + {dd}P [2]'),
        lambda r: ('Explain how the price mechanism removes the excess demand.', 'Price rises (signal); demand contracts and supply extends (incentive) until the market clears (rationing).', '[3]'),
        lambda r: ('Discuss whether the shortage of skilled workers means the price rise will be large and long-lasting.', 'Inelastic supply → large price rise in short run; in long run training, migration, technology and entry raise supply; campaign may be a fad; judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t10_1, t10_2, t10_3, t10_4], _ch10_case)
essay(t10_1, [
    ('With the help of a diagram, explain how equilibrium price is determined and how a market removes excess demand and excess supply.',
     'Intersection of D and S; above equilibrium surplus → price falls; below shortage → price rises; extensions/contractions; diagram.',
     'markets in {country} will always move quickly to equilibrium',
     'Price flexibility clears markets; competition; information via prices.',
     'Sticky prices, contracts, government controls, inelastic supply, information failures, speculation; disequilibrium can persist (housing, labour markets).'),
])
essay(t10_2, [
    ('With the help of diagrams, explain how a decrease in supply and an increase in demand would each affect equilibrium price and quantity.',
     'Supply left: P up, Q down; demand right: P up, Q up; combined: P rises, Q indeterminate; diagrams.',
     'changes in demand have a greater effect on prices than changes in supply in the market for {good}',
     'Demand shocks (incomes, fashion) can be large; inelastic supply magnifies price effect.',
     'Supply shocks (weather, costs) dominate in agricultural and energy markets; depends on elasticities and size of shifts.'),
])
essay(t10_3, [
    ('Explain, with examples, the difference between joint demand, competitive demand, derived demand, composite demand and joint supply.',
     'Definitions with examples: complements; substitutes; labour/raw materials; milk/oil multiple uses; beef/leather by-products; diagrams of linked markets.',
     'a change in one market will always have significant effects on related markets',
     'Linked through complements, substitutes and joint supply; e.g. oil prices affect many markets.',
     'Depends on strength of relationship (XED), elasticities, share of input in cost; some links weak; time lags.'),
])
essay(t10_4, [
    ('Explain the functions of the price mechanism in allocating resources.',
     'Signalling, incentive and rationing; reallocation between markets; example of a demand increase.',
     'the price mechanism is the most efficient way to allocate resources in {country}',
     'Decentralised information, incentives, quick response, consumer sovereignty, allocative efficiency.',
     'Market failure: public goods, externalities, information failure, inequality, monopoly; need for intervention; mixed economy.'),
])
CHAPTERS[10] = [t10_1, t10_2, t10_3, t10_4]

# ============================================================================ 11 Consumer and producer surplus
def kd(x):
    """Dollar value of an area measured in (thousands of units × dollars)."""
    return money(round(x * 1000))


def cs_ps(a, b, c, d, P, Q):
    pmax = a / b
    cs = 0.5 * (pmax - P) * Q
    pmin = -c / d  # price where Qs = 0 (may be negative → trapezium)
    if pmin >= 0:
        ps = 0.5 * (P - pmin) * Q
    else:
        ps = 0.5 * (c + Q) * P  # area between 0 and P under supply quantity: trapezium
    return pmax, cs, pmin, ps


t11_1 = T('Consumer surplus: meaning and measurement', 'consumer surplus', 'meaning and measurement')
mc(t11_1, [
    ('What is consumer surplus?', 'The difference between what consumers are willing to pay and what they actually pay', 'Area below the demand curve and above the price.',
     ['The profit made by firms', 'The difference between price and cost', 'The surplus stock left unsold']),
    ('On a demand and supply diagram, consumer surplus is the area', 'below the demand curve and above the market price', 'Triangle between D and price line.', ['above the supply curve and below the price', 'below the supply curve', 'between the demand and supply curves to the right of equilibrium']),
    ('What happens to consumer surplus when the market price falls?', 'It increases', 'Existing buyers pay less; new buyers enter.', ['It falls', 'It stays the same', 'It becomes producer surplus']),
    ('A consumer is willing to pay $50 for a ticket that costs $35. What is the consumer surplus?', '$15', '50 − 35.', ['$35', '$50', '$85']),
    ('Why does consumer surplus exist?', 'Many consumers value the good more highly than the market price', 'Willingness to pay above price for intra-marginal units.', ['Firms charge too little', 'Governments subsidise all goods', 'Supply is perfectly elastic']),
])
ex(t11_1, [
    ('Explain the meaning of consumer surplus and how it can be shown on a diagram.', 'Consumer surplus is the extra benefit consumers receive because they pay less than the maximum they are willing to pay. It is the area under the demand curve and above the market price, up to the quantity bought.', '1 mark: definition; 1 mark: area on diagram [2]'),
    ('Explain why a rise in the price of a good reduces consumer surplus.', 'Consumers who still buy pay more, losing some surplus, and some consumers stop buying altogether, losing all their surplus.', '1 mark: existing buyers pay more; 1 mark: some buyers leave [2]'),
])
items(t11_1, 'C2', (1, 2, 3, 4), [
    ('{person} would have paid up to $120 for a concert ticket in {city} but bought it for $75. Explain what is meant by {person}’s consumer surplus and calculate it.', 'Consumer surplus is the difference between willingness to pay and the price paid: $120 − $75 = $45.', '1 mark: definition; 1 mark: $45 [2]'),
    ('An airline in {country} charges different fares to different passengers on the same flight. Explain how this reduces consumer surplus.', 'By charging prices closer to each passenger’s willingness to pay, the airline turns consumer surplus into revenue (price discrimination).', '1 mark: prices nearer willingness to pay; 1 mark: surplus captured by firm [2]'),
])
errs(t11_1, [
    ('Consumer surplus is the amount of a good left unsold at the end of the day.', 'Consumer surplus is the difference between what consumers are willing to pay and what they actually pay; unsold goods are excess supply.'),
    ('Consumer surplus is shown by the area above the supply curve.', 'That area is producer surplus; consumer surplus is below the demand curve and above the price.'),
])


@t11_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_1_cs(r, D):
    a, b, c, d, P, Q = lin(r)
    pmax, cs, _, _ = cs_ps(a, b, c, d, P, Q)
    g = r.choice(GOODS)
    stem = f'The demand for {g} is {qd_s(a, b)} and supply is {qs_s(c, d)}, with Q in thousands and P in dollars. The market is in equilibrium.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate consumer surplus.', f'{kd(cs)}', f'P* = {P}, Q* = {Q}; max price {num(pmax, 2)}; CS = ½ × ({num(pmax, 2)} − {P}) × {Q} = {num(cs)} thousand = {kd(cs)}.',
                  dis_num(r, cs, kd, [cs * 2, P * Q, pmax * Q / 2]), mcq_D=(1, 2))
    P2 = P + r.choice([1, 2])
    Q2 = a - b * P2
    if Q2 <= 0:
        return None
    cs2 = 0.5 * (pmax - P2) * Q2
    return {'stem': stem + f' (a) Calculate the equilibrium price and quantity and the consumer surplus. (b) The price rises to ${P2}. Calculate the new consumer surplus and the loss of consumer surplus. (c) Explain the two parts of this loss.',
            'answer': f'(a) P = {money(P)}, Q = {Q}; CS = {kd(cs)}. (b) Q = {Q2}; CS = {kd(cs2)}; loss {kd(cs - cs2)}. (c) Remaining buyers pay more (rectangle), and buyers priced out lose all their surplus (triangle).',
            'key': f'(a) equilibrium [1]; CS = ½ × ({num(pmax, 2)} − {P}) × {Q} [1] (b) new CS [1]; loss [1] (c) two parts [1] [5]', 'marks': 5, 'type': 'multi_step'}


t11_2 = T('Producer surplus: meaning and measurement', 'producer surplus')
mc(t11_2, [
    ('What is producer surplus?', 'The difference between the price producers receive and the minimum price at which they are willing to supply', 'Area above supply curve and below price.',
     ['The total revenue of producers', 'The profit after tax', 'The surplus stock held by producers']),
    ('On a diagram, producer surplus is the area', 'above the supply curve and below the market price', 'Between price line and S.', ['below the demand curve and above the price', 'under the supply curve', 'between the curves to the right of equilibrium']),
    ('What happens to producer surplus when market price rises?', 'It increases', 'Existing producers gain; new producers enter.', ['It falls', 'It stays the same', 'It becomes consumer surplus']),
    ('A farmer would sell a crate of mangoes for at least $8 and sells it for $12. What is the producer surplus?', '$4', '12 − 8.', ['$8', '$12', '$20']),
    ('Why is producer surplus not the same as profit?', 'It does not take account of fixed costs', 'PS = TR − total variable cost (for a firm).', ['It includes all costs', 'It ignores revenue', 'It is measured in units of output']),
])
ex(t11_2, [
    ('Explain the meaning of producer surplus.', 'The extra amount producers receive above the minimum price at which they would have been willing to supply each unit; the area above the supply curve and below the market price.', '1 mark: definition; 1 mark: area [2]'),
    ('Explain why an increase in demand increases producer surplus.', 'Price rises, so existing output earns more above its minimum supply price, and extra output is supplied at the higher price, adding more surplus.', '1 mark: higher price on existing units; 1 mark: extra units [2]'),
])
items(t11_2, 'C2', (1, 2, 3, 4), [
    ('Coffee growers in {country} receive a higher world price after poor harvests elsewhere. Explain the effect on their producer surplus.', 'They receive a higher price for every bag sold above the minimum they would accept, so producer surplus rises (if their own output is unaffected).', '1 mark: higher price; 1 mark: larger area above supply [2]'),
])
errs(t11_2, [
    ('Producer surplus is the same as total revenue.', 'Producer surplus is revenue above the minimum price producers would accept for each unit (above the supply curve), not total revenue.'),
])


@t11_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_2_ps(r, D):
    for _ in range(20):
        a, b, c, d, P, Q = lin(r)
        if c <= 0:
            break
    pmax, cs, pmin, ps = cs_ps(a, b, c, d, P, Q)
    g = r.choice(MGOODS)
    stem = f'The supply of {g} is {qs_s(c, d)} and demand is {qd_s(a, b)}, with Q in thousands and P in dollars. The market is in equilibrium at P = ${P}.'
    how = (f'PS = ½ × ({P} − {num(pmin, 2)}) × {Q}' if pmin >= 0 else f'PS = ½ × ({c} + {Q}) × {P} (trapezium: supply starts at Q = {c} when P = 0)')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate producer surplus.', f'{kd(ps)}', how + f' = {num(ps)} thousand = {kd(ps)}.', dis_num(r, ps, kd, [ps * 2, P * Q, cs]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the equilibrium quantity and the producer surplus. (b) Calculate consumer surplus. (c) Explain what the total of the two surpluses represents.',
            'answer': f'(a) Q = {Q}; PS = {kd(ps)}. (b) CS = {kd(cs)}. (c) Total economic welfare = {kd(ps + cs)}: the net benefit to consumers and producers from trade in this market.',
            'key': f'(a) Q [1]; {how} [1] (b) ½ × ({num(pmax, 2)} − {P}) × {Q} [1] (c) total welfare [1] [4]', 'marks': 4, 'type': 'numerical'}


t11_3 = T('Changes in consumer and producer surplus when market conditions change', 'changes in consumer and producer surplus', 'market conditions change')
mc(t11_3, [
    ('If supply increases and demand is unchanged, what happens to consumer surplus?', 'It increases', 'Price falls and quantity rises.', ['It falls', 'It is unchanged', 'It becomes zero']),
    ('An indirect tax on a good will usually', 'reduce both consumer and producer surplus', 'Consumers pay more, producers receive less; part becomes tax revenue, part deadweight loss.', ['increase both surpluses', 'increase consumer surplus only', 'have no effect on surpluses']),
    ('If demand for a good falls, what happens to producer surplus?', 'It falls', 'Lower price and quantity.', ['It rises', 'It is unchanged', 'It becomes consumer surplus']),
    ('A subsidy to producers of a good will usually', 'increase both consumer and producer surplus', 'Lower price to consumers, higher price received by producers.', ['reduce both surpluses', 'reduce consumer surplus only', 'have no effect']),
    ('Part of the loss of consumer and producer surplus from a tax that is not received by anyone is called', 'a deadweight loss', 'Welfare loss from reduced trade.', ['tax revenue', 'producer surplus', 'opportunity cost']),
])
ex(t11_3, [
    ('Explain how an increase in supply affects consumer surplus and producer surplus.', 'Price falls and quantity rises: consumer surplus rises (lower price, more buyers); producer surplus may rise or fall depending on the elasticity of demand and the shift.', '1 mark: CS rises; 1 mark: PS effect with reason [2]'),
    ('Explain why an indirect tax creates a deadweight loss.', 'The tax raises price and reduces quantity; trades that would have given benefits greater than costs no longer happen, so some consumer and producer surplus is lost and not collected as tax.', '1 mark: fewer trades; 1 mark: surplus lost not transferred [2]'),
])
items(t11_3, 'C2', (1, 2, 3, 4), [
    ('New technology cuts the cost of producing {mgood} in {country}. Explain the effect on consumer surplus.', 'Supply shifts right; price falls and quantity rises, so consumer surplus increases.', '1 mark: supply shift/lower price; 1 mark: CS rises [2]'),
    ('The government of {country} sets a maximum price for bread below equilibrium. Explain how this changes producer surplus.', 'Producers receive a lower price and sell less, so producer surplus falls.', '1 mark: lower price; 1 mark: lower quantity → PS falls [2]'),
])
errs(t11_3, [
    ('A tax on a good increases producer surplus because the government pays producers.', 'An indirect tax is paid to the government; producers receive a lower net price and sell less, so producer surplus falls.'),
])


@t11_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_3_change(r, D):
    a, b, c, d, P, Q = lin(r)
    k = (b + d) * r.choice([1, 2])
    up = r.random() < 0.5
    c2 = c + k if up else c - k
    P2 = (a - c2) / (b + d)
    Q2 = a - b * P2
    if Q2 <= 0 or P2 <= 0:
        return None
    pmax = a / b
    cs1, cs2 = 0.5 * (pmax - P) * Q, 0.5 * (pmax - P2) * Q2
    g = r.choice(MGOODS)
    cause = 'a fall in production costs' if up else 'a rise in production costs'
    stem = f'Demand for {g} is {qd_s(a, b)}. After {cause}, supply changes from {qs_s(c, d)} to {qs_s(c2, d)} (Q in thousands, P in dollars).'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the change in consumer surplus.', f'{"+" if cs2 > cs1 else "−"}{kd(abs(cs2 - cs1))}',
                  f'CS before ½ × ({num(pmax, 2)} − {P}) × {Q} = {num(cs1)} thousand; after ½ × ({num(pmax, 2)} − {num(P2)}) × {num(Q2)} = {num(cs2)} thousand; change {kd(cs2 - cs1)}.',
                  [f'{s}{kd(x)}' for s, x in (('+' if cs2 < cs1 else '−', abs(cs2 - cs1)), ('+', cs2), ('−', cs1), ('+', abs(cs2 - cs1) * 2))], mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the equilibrium price and quantity before and after. (b) Calculate consumer surplus before and after. (c) Explain why consumers have gained or lost.',
            'answer': f'(a) {money(P)}, {Q} → {money(P2)}, {num(Q2)}. (b) {kd(cs1)} → {kd(cs2)}. (c) ' + ('Lower price for existing buyers and new buyers enter: CS rises.' if up else 'Higher price for remaining buyers and some priced out: CS falls.'),
            'key': '(a) both equilibria [2] (b) both CS values [2] (c) explanation [1] [5]', 'marks': 5, 'type': 'multi_step'}


def _ch11_case(r, D):
    d = ctx(r)
    a, b, c, dd, P, Q = lin(r)
    pmax, cs, pmin, ps = cs_ps(a, b, c, dd, P, Q)
    intro = (f'Extract: The market for {d["good"]} in {d["city"]} is described by {qd_s(a, b)} and {qs_s(c, dd)} (Q in thousands per month, P in dollars). '
             f'The city council is considering a tax on {d["good"]}, which some councillors say would “simply transfer money from consumers to the council”.')
    parts = [
        lambda r: ('Calculate the equilibrium price and quantity.', f'{money(P)}, {Q}', '[2]'),
        lambda r: ('Calculate consumer surplus at equilibrium.', f'{kd(cs)}', f'½ × ({num(pmax, 2)} − {P}) × {Q} [2]'),
        lambda r: ('Calculate producer surplus at equilibrium.', f'{kd(ps)}', '[2]'),
        lambda r: ('Explain how a tax would affect consumer and producer surplus.', 'Price to consumers rises and price received by producers falls; both surpluses fall; part becomes tax revenue, part is a deadweight loss.', '[3]'),
        lambda r: ('Discuss whether the councillors are right that the tax is “simply a transfer”.', 'Not only a transfer: deadweight loss from fewer trades; size depends on elasticities; revenue may fund beneficial spending; externalities could make it welfare-improving; judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t11_1, t11_2, t11_3], _ch11_case)
essay(t11_1, [
    ('With the help of a diagram, explain the meaning of consumer surplus and how it changes when price changes.',
     'Willingness to pay vs price; area under demand above price; price fall raises CS (existing + new buyers); diagram.',
     'consumer surplus is a useful measure of the benefit consumers gain from a market',
     'Measures net benefit; used in cost-benefit analysis and evaluating policies.',
     'Willingness to pay depends on income (rich have higher WTP); hard to measure; ignores externalities; still a useful approximation.'),
])
essay(t11_2, [
    ('With the help of a diagram, explain the meaning of producer surplus.',
     'Price vs minimum supply price; area above supply below price; higher price raises PS; diagram; difference from profit.',
     'producers in {country} always gain when the market price of their product rises',
     'Higher price raises PS on existing and extra units.',
     'If the price rise is caused by higher costs, PS may fall; if output falls (bad harvest), some producers lose; depends on cause and elasticities.'),
])
essay(t11_3, [
    ('Explain, with the help of a diagram, how an increase in supply affects consumer and producer surplus.',
     'Supply shifts right; price falls, quantity rises; CS rises; PS changes depend on elasticities; diagram with areas.',
     'government intervention in markets always reduces total economic welfare',
     'Taxes and price controls cause deadweight losses; both surpluses fall.',
     'With externalities, merit/demerit goods or market power, intervention can raise welfare; equity gains; depends on design and information.'),
])
CHAPTERS[11] = [t11_1, t11_2, t11_3]

# ============================================================================ 12 Reasons for government intervention in markets
MF_CASES = [
    ('No private firm in {country} will build a flood barrier because residents who do not pay would still be protected.', 'Public good (free rider problem)', 'non-excludable; free riders mean no revenue so the market is missing.'),
    ('Teenagers in {city} underestimate the long-term benefits of staying in education.', 'Merit good (information failure)', 'benefits are underestimated, so the good is under-consumed.'),
    ('Smokers in {country} underestimate the risk of lung disease.', 'Demerit good (information failure)', 'harm is underestimated, so the good is over-consumed.'),
    ('A factory near {city} pollutes a river used by fishermen.', 'Negative externality', 'a cost is imposed on third parties who are not compensated.'),
    ('Second-hand car buyers in {country} cannot tell which cars are faulty, but sellers can.', 'Asymmetric information', 'one party has more information than the other.'),
    ('One firm controls the entire water supply in {city} and raises its prices.', 'Monopoly power', 'lack of competition leads to high prices and lower output.'),
    ('Beekeepers in {country} help nearby farmers by pollinating their crops for free.', 'Positive externality', 'a benefit is received by third parties without payment.'),
    ('Street lighting in {city} would not be supplied by any private firm.', 'Public good (free rider problem)', 'non-excludable and non-rivalrous.'),
]
MF_LABELS = ['Public good (free rider problem)', 'Merit good (information failure)', 'Demerit good (information failure)', 'Negative externality', 'Asymmetric information', 'Monopoly power', 'Positive externality']

t12_1 = T('Market failure as a reason for government intervention', 'market failure', 'government intervention')
mc(t12_1, [
    ('What is meant by market failure?', 'A situation where the free market leads to a misallocation of resources', 'Market fails to achieve an efficient (socially optimal) outcome.',
     ['A situation where a firm goes out of business', 'A fall in the stock market', 'A situation where prices rise']),
    ('Which is an example of market failure?', 'The under-provision of public goods', 'Missing markets, externalities, information failure, merit/demerit goods.', ['A fall in the price of a good after a rise in supply', 'A firm making a profit', 'Consumers switching to a cheaper brand']),
    ('What is a negative externality?', 'A cost imposed on a third party that is not reflected in the market price', 'External cost; e.g. pollution.', ['A tax paid by producers', 'A cost paid by consumers', 'The cost of importing goods']),
    ('Why does a negative externality in production lead to over-production?', 'Producers do not pay the full social cost, so the market output is too high', 'Private cost < social cost.', ['Producers pay too much tax', 'Consumers buy too little', 'Prices are set too high']),
    ('Which is the main reason a government might provide a good itself?', 'The market would not provide it because of the free rider problem', 'Public goods.', ['The good is very cheap to produce', 'Consumers prefer state goods', 'Private firms never make profits']),
])
ex(t12_1, [
    ('Explain what is meant by market failure and give two examples.', 'Market failure is when the free market misallocates resources, so output is not at the socially optimal level. Examples: public goods not provided, negative externalities (pollution) over-produced, merit goods under-consumed.', '1 mark: definition; 1 mark each example [3]'),
    ('Explain why positive externalities lead to under-consumption in a free market.', 'Consumers consider only their private benefit; the external benefit to others is ignored, so demand and consumption are below the socially optimal level.', '1 mark: private benefit only; 1 mark: below social optimum [2]'),
    ('Explain why monopoly power may be a reason for government intervention.', 'A monopolist can restrict output and raise price above the competitive level, reducing consumer welfare and misallocating resources.', '1 mark: higher price/lower output; 1 mark: misallocation [2]'),
])
classify(t12_1, MF_CASES, MF_LABELS, 'Which type of market failure is illustrated?', 'Identify the type of market failure in each case and explain why it leads to a misallocation of resources.', name='mf')
items(t12_1, 'C2', (1, 2, 3, 4), [
    ('Traffic congestion in {city} imposes costs on bus passengers and local residents. Explain why this is a market failure.', 'Each driver ignores the extra delay and pollution they impose on others (negative externality), so road use exceeds the socially optimal level.', '1 mark: external cost; 1 mark: over-use [2]'),
    ('{firm} researches a new vaccine that other firms can copy. Explain why the market may provide too little research.', 'Research creates positive externalities (benefits to other firms and society) that {firm} cannot charge for, so it invests less than the social optimum.', '1 mark: external benefits; 1 mark: under-investment [2]'),
])
errs(t12_1, [
    ('Market failure means that firms in a market are making losses.', 'Market failure means resources are misallocated (output not at the social optimum); firms may be very profitable when a market fails.'),
    ('A negative externality is a cost paid by the consumer who buys the good.', 'An externality falls on a third party who is not part of the transaction and is not compensated.'),
])


@t12_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_1_ext(r, D):
    f = r.choice(FIRMS)
    q = r.choice([1000, 2000, 5000])
    pc = r.choice([8, 10, 12, 15])
    ec = r.choice([2, 3, 4, 5])
    stem = f'{f} produces {q:,} tonnes of chemicals a month. Its private cost is ${pc} per tonne, but pollution imposes an extra cost of ${ec} per tonne on local residents.'
    sc = pc + ec
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the social cost per tonne.', money(sc), f'Social cost = private + external = {pc} + {ec}.', dis_num(r, sc, money, [pc, ec, pc - ec]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the total external cost and the total social cost each month. (b) Explain why the free market leads to over-production of the chemicals. (c) Suggest one form of intervention and explain how it would help.',
            'answer': f'(a) External {money(ec * q)}; social {money(sc * q)}. (b) {f} considers only private cost (${pc}), not the social cost (${sc}), so supply is too high and price too low relative to the social optimum. (c) A tax of ${ec} per tonne (or regulation) makes the firm pay the full social cost, reducing output towards the optimum.',
            'key': f'(a) {ec} × {q} and {sc} × {q} [2] (b) private < social cost → over-production [2] (c) policy and mechanism [1] [5]', 'marks': 5, 'type': 'multi_step'}


t12_2 = T('Information failure and the case for government provision', 'information failure', 'case for government provision', 'government provision')
mc(t12_2, [
    ('What is asymmetric information?', 'A situation where one party to a transaction has more information than the other', 'e.g. sellers of used cars, insurance.', ['A situation where both parties have full information', 'Information that is expensive', 'A shortage of data for government']),
    ('Why might the government provide healthcare directly?', 'Patients lack information to judge treatment and may under-consume a merit good', 'Information failure; equity; externalities.', ['Healthcare is a free good', 'Private firms cannot provide healthcare', 'Healthcare is non-rivalrous']),
    ('Which policy most directly addresses information failure?', 'Requiring clear labelling of the sugar content of food', 'Provides missing information.', ['A maximum price on food', 'A subsidy to farmers', 'A tariff on imported food']),
    ('Why may consumers make poor decisions about pensions?', 'They underestimate their future needs and find the products complex', 'Imperfect information; short-termism.', ['Pensions are public goods', 'Pensions are always free', 'Pension prices are too low']),
    ('What is a problem with direct government provision of a good?', 'It may be inefficient because there is no profit motive', 'Government failure risk.', ['Consumers will always pay too much', 'It always leads to monopoly profits', 'It increases free riding']),
])
ex(t12_2, [
    ('Explain how information failure can lead to a misallocation of resources.', 'If consumers misjudge the benefits or costs of a good, they buy too much (demerit) or too little (merit) compared with what they would buy with full information, so output is not at the social optimum.', '1 mark: misjudge benefits/costs; 1 mark: wrong quantity vs optimum [2]'),
    ('Explain the case for the government providing education free at the point of use.', 'Education is a merit good: families underestimate its benefits and there are positive externalities; some cannot afford it. Free provision raises consumption towards the social optimum and improves equity.', '1 mark: merit good/info failure; 1 mark: externalities; 1 mark: equity [3]'),
])
items(t12_2, 'C2', (1, 2, 3, 4), [
    ('Buyers of second-hand cars in {city} often cannot tell whether a car has hidden faults. Explain how this asymmetric information affects the market.', 'Sellers know more than buyers; buyers fear buying a “lemon”, so they offer low prices; owners of good cars withdraw, so the market shrinks and average quality falls.', '1 mark: asymmetric information; 1 mark: effect on price/quality [2]'),
    ('The government of {country} pays for free health check-ups for adults over 50. Explain why.', 'People underestimate the benefits of early diagnosis (information failure); early treatment is cheaper and has external benefits; check-ups are a merit good.', '1 mark: info failure; 1 mark: benefits of provision [2]'),
])
errs(t12_2, [
    ('Information failure only affects consumers, never producers.', 'Producers can also lack information, e.g. about future prices or the true quality of inputs, and asymmetric information affects both sides.'),
])
classify(t12_2, MF_CASES, MF_LABELS, 'Which type of market failure is illustrated?', 'Identify the type of market failure in each case and explain why it leads to a misallocation of resources.', name='mf')


@t12_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_2_info(r, D):
    c = r.choice(COUNTRIES)
    t0, t1 = r.choice([(40, 65), (35, 60), (50, 72)])
    cost = r.choice([20, 30, 40])
    n = r.choice([2, 3, 4])
    save = r.choice([80, 100, 150])
    stem = f'In {c}, {t0}% of adults had a free eye test when it was advertised only in clinics. After a national information campaign, take-up rose to {t1}%.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the percentage increase in take-up.', pct(chg(t0, t1)), f'({t1} − {t0})/{t0} × 100.', dis_num(r, chg(t0, t1), pct, [t1 - t0]), mcq_D=(1, 2))
    extra = n * 1e6 * (t1 - t0) / 100
    return {'stem': stem + f' The adult population is {n} million. Each test costs the state ${cost} and each test avoids, on average, ${save} of later treatment costs. (a) Calculate the number of extra tests and their net saving to the state. (b) Explain why take-up was low before the campaign.',
            'answer': f'(a) {num(extra)} extra tests; net saving ${num(extra * (save - cost))}. (b) Information failure: people underestimated the benefits of the tests or did not know about them, so the merit good was under-consumed.',
            'key': f'(a) {n}m × {t1 - t0}% [1]; × (${save} − ${cost}) [1] (b) information failure/merit good [2] [4]', 'marks': 4, 'type': 'numerical'}


t12_3 = T('Intervening to stabilise prices and incomes in volatile markets', 'stabilise prices and incomes', 'volatile markets', 'buffer stock')
mc(t12_3, [
    ('Why are prices of agricultural products often volatile?', 'Supply varies with the weather while demand and supply are price inelastic', 'Inelastic supply and demand + supply shocks.', ['Demand is perfectly elastic', 'Governments change prices daily', 'Farmers set prices together']),
    ('How does a buffer stock scheme stabilise prices?', 'It buys produce when prices are low and sells from stocks when prices are high', 'Floor and ceiling prices maintained by buying/selling.', ['It taxes farmers in good years', 'It bans imports', 'It sets a fixed quantity for each farmer']),
    ('What is a problem with buffer stock schemes?', 'If the floor price is set too high the agency accumulates large, costly stocks', 'Storage costs, perishability, funding.', ['Prices become more volatile', 'Farmers produce less', 'Consumers pay lower prices']),
    ('Why might a government want to stabilise farmers’ incomes?', 'To protect farmers from sudden falls in income and maintain food supplies', 'Income stability, investment, food security.', ['To increase price volatility', 'To reduce output', 'To raise import prices']),
])
ex(t12_3, [
    ('Explain how a buffer stock scheme works.', 'An agency sets a minimum and maximum price. In good harvests it buys surplus output to stop the price falling below the minimum; in bad harvests it sells from stocks to stop the price rising above the maximum.', '1 mark: price band; 1 mark: buy in surplus; 1 mark: sell in shortage [3]'),
    ('Explain why a good harvest can reduce farmers’ total income.', 'Demand for many crops is price inelastic, so the increase in supply causes a proportionately larger fall in price, reducing total revenue.', '1 mark: inelastic demand; 1 mark: price fall > quantity rise [2]'),
])
items(t12_3, 'C2', (1, 2, 3, 4), [
    ('The price of coffee beans in {country} fell by 40% after a bumper harvest. Explain why the government might intervene.', 'Farmers’ incomes fall sharply, causing hardship and reducing future investment; price volatility creates uncertainty; government may buy into stocks to stabilise prices and incomes.', '1 mark: income/uncertainty problem; 1 mark: form of intervention [2]'),
])
errs(t12_3, [
    ('A good harvest always increases farmers’ incomes because they sell more.', 'If demand is price inelastic, the price falls proportionately more than quantity rises, so total income can fall.'),
])


@t12_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_3_buffer(r, D):
    c = r.choice(COUNTRIES)
    crop = r.choice(['cocoa', 'rice', 'wheat', 'coffee', 'cotton'])
    a, b = r.choice([(300, 10), (400, 20), (500, 25)])
    floor = r.choice([8, 10, 12])
    qd_f = a - b * floor
    harvest = qd_f + r.choice([20, 40, 50, 60])
    p_free = (a - harvest) / b
    if p_free <= 0:
        return None
    buy = harvest - qd_f
    stem = f'Demand for {crop} in {c} is {qd_s(a, b)} (Q in thousand tonnes, P in hundreds of dollars per tonne). A buffer stock agency sets a minimum price of ${floor * 100:,} per tonne (P = {floor}). This year’s harvest is {harvest} thousand tonnes.'
    if D <= 2:
        return cq(r, 1, stem + ' How much must the agency buy to maintain the minimum price?', f'{buy} thousand tonnes', f'Qd at P = {floor} is {qd_f}; harvest {harvest}; buy {buy}.', [f'{x} thousand tonnes' for x in (harvest, qd_f, buy + 10, buy * 2)], mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the free-market price with this harvest. (b) Calculate the quantity the agency must buy and the cost. (c) Explain one problem the agency might face if harvests are good for several years.',
            'answer': f'(a) P = {num(p_free, 2)}, i.e. {money(p_free * 100)} per tonne (b) {buy} thousand tonnes; cost {money(buy * 1000 * floor * 100)}. (c) Stocks build up, raising storage costs and spoiling; the agency may run out of funds; it may have to lower the minimum price.',
            'key': f'(a) {a} − {b}P = {harvest} [1] (b) {harvest} − {qd_f} [1]; {buy},000 × ${floor * 100:,} [1] (c) problem explained [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch12_case(r, D):
    d = ctx(r)
    v0, v1 = r.choice([(55, 78), (60, 82), (48, 70)])
    cost = r.choice([30, 40, 50])
    intro = (f'Extract: In {d["country"]}, childhood vaccination rates were only {v0}% when parents had to pay about ${cost} per course. After the government made vaccinations free and ran an information campaign, the rate rose to {v1}%. '
             f'The health ministry argues that vaccination is a merit good with large external benefits. A newspaper claims that “the market would have sorted this out on its own”.')
    parts = [
        lambda r: ('Calculate the increase in the vaccination rate in percentage points.', f'{v1 - v0} percentage points', '[1]'),
        lambda r: ('Explain why vaccination is a merit good.', 'Parents underestimate the benefits (information failure), so it is under-consumed in a free market.', '[2]'),
        lambda r: ('Explain the external benefits of vaccination.', 'Vaccinated children protect others (herd immunity), lowering infection and healthcare costs for third parties.', '[2]'),
        lambda r: ('Explain why the market alone might fail to achieve the socially optimal rate.', 'Consumers ignore external benefits and underestimate private benefits; price deters low-income families.', '[3]'),
        lambda r: ('Discuss whether making vaccinations free is the best way to correct this market failure.', 'Free provision raises take-up and equity vs opportunity cost, taxpayer burden, possible government failure; alternatives: information only, compulsion, subsidies; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t12_1, t12_2, t12_3], _ch12_case)
essay(t12_1, [
    ('Explain the main types of market failure that may justify government intervention.',
     'Public goods (free riders), externalities, merit and demerit goods, information failure, monopoly power; misallocation vs social optimum.',
     'market failure always justifies government intervention in {country}',
     'Market outcomes are inefficient; intervention can move output towards the social optimum; equity.',
     'Government failure: lack of information, costs, unintended consequences, political motives; sometimes the failure is small; private solutions possible; judgement depends on costs and benefits.'),
])
essay(t12_2, [
    ('Explain how information failure can cause markets to fail.',
     'Imperfect and asymmetric information; merit/demerit goods; second-hand markets; insurance; consumers misjudge benefits and costs.',
     'direct government provision is the best way to deal with information failure in healthcare',
     'Ensures access, overcomes under-consumption, equity, controls quality.',
     'Inefficiency, waiting lists, high cost; regulation, information and subsidies may be better; patients still lack information; judgement.'),
])
essay(t12_3, [
    ('Explain why prices in agricultural markets tend to be unstable.',
     'Supply shocks (weather, disease), inelastic supply and demand, time lags, cobweb behaviour, world market speculation; diagram.',
     'buffer stock schemes are an effective way to stabilise farm prices and incomes in {country}',
     'Buy in surplus, sell in shortage; stabilises prices and incomes; encourages investment.',
     'Costly storage, perishability, setting the right price band, funding, can encourage over-production; schemes have often collapsed; alternatives (insurance, futures, diversification).'),
])
CHAPTERS[12] = [t12_1, t12_2, t12_3]


# ============================================================================ 13 Methods and effects of government intervention in markets
def _tax_eq(r, sub=False):
    for _ in range(60):
        a, b, c, d, P, Q = lin(r)
        t = r.choice([1, 2, 3, 4, 5])
        if t >= P:
            continue
        s = -t if sub else t
        P1 = (a - c + d * s) / (b + d)
        if abs(P1 * 100 - round(P1 * 100)) > 1e-6:
            continue
        Q1 = a - b * P1
        if Q1 <= 0:
            continue
        return a, b, c, d, P, Q, t, P1, Q1
    return None


t13_1 = T('Maximum and minimum prices: effects on markets', 'maximum and minimum prices', 'effects on markets', 'price controls')
mc(t13_1, [
    ('A maximum price set below the equilibrium price will cause', 'a shortage (excess demand)', 'Price ceiling below equilibrium → Qd > Qs.', ['a surplus', 'no effect', 'an increase in supply']),
    ('A minimum price set above the equilibrium price will cause', 'a surplus (excess supply)', 'Floor above equilibrium → Qs > Qd.', ['a shortage', 'no effect', 'a fall in quantity supplied']),
    ('What is a likely consequence of a maximum price on rented housing?', 'A shortage of rental housing and the growth of an illegal market', 'Landlords supply less; queues and black markets.', ['A surplus of rented housing', 'Higher rents for all tenants', 'More new housing built']),
    ('A maximum price set above the equilibrium price will', 'have no effect on the market', 'Not binding.', ['cause a shortage', 'cause a surplus', 'raise the market price']),
    ('Why might a government set a minimum price for alcohol?', 'To reduce consumption of a demerit good', 'Raises price of cheapest drinks.', ['To increase alcohol sales', 'To create a shortage', 'To protect consumers from high prices']),
])
ex(t13_1, [
    ('Explain, with the help of a diagram, the effect of a maximum price set below the equilibrium price.', 'At the lower price quantity demanded rises and quantity supplied falls, causing a shortage (Qd − Qs). Goods must be rationed by queuing or other means, and a black market may develop at higher prices.', '1 mark: below equilibrium; 1 mark: shortage; 1 mark: consequence [3]'),
    ('Explain why a minimum price for an agricultural product may lead to government spending.', 'At the minimum price above equilibrium there is a surplus; to maintain the price the government must buy the surplus, which costs money and storage.', '1 mark: surplus; 1 mark: government buys surplus [2]'),
])
items(t13_1, 'C2', (1, 2, 3, 4), [
    ('The government of {country} sets a maximum price for bread below the market price. Explain one benefit and one problem of this policy.', 'Benefit: bread more affordable for low-income households. Problem: shortages, queues, lower quality, black markets, bakers leave the market.', '1 mark: benefit; 1 mark: problem [2]'),
    ('{city} introduces rent controls that keep rents well below the market level. Explain why the number of flats for rent may fall over time.', 'Lower returns reduce landlords’ incentive to rent out or maintain flats; supply contracts, so shortages grow.', '1 mark: lower incentive; 1 mark: supply falls [2]'),
])
errs(t13_1, [
    ('A maximum price set above the equilibrium price will cause a shortage.', 'A maximum price above equilibrium is not binding; the market stays at equilibrium.'),
    ('A minimum price creates a shortage because the price is higher.', 'A binding minimum price (above equilibrium) creates excess supply: quantity supplied exceeds quantity demanded.'),
])


@t13_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_1_ctrl(r, D):
    a, b, c, d, P, Q = lin(r)
    g = r.choice(GOODS)
    mx = r.random() < 0.5
    pc = P - r.choice([1, 2, 3]) if mx else P + r.choice([1, 2, 3])
    if pc <= 0:
        return None
    qd, qs = a - b * pc, c + d * pc
    if qd <= 0 or qs <= 0:
        return None
    kind = 'maximum' if mx else 'minimum'
    stem = f'In the market for {g}, {qd_s(a, b)} and {qs_s(c, d)} (Q in thousands, P in dollars). The government introduces a {kind} price of ${pc}.'
    gap = abs(qd - qs)
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the {"shortage" if mx else "surplus"} that results.', f'{gap} thousand units', f'Qd = {qd}, Qs = {qs} at ${pc}; difference {gap}.',
                  dis_num(r, gap, lambda x: f'{num(x)} thousand units', [abs(Q - qs), abs(qd - Q), qd, gap * 2]), mcq_D=(1, 2))
    extra = (f' (c) If the government buys the surplus, calculate the cost.' if not mx else ' (c) Explain one way in which the shortage may be allocated and one likely consequence.')
    return {'stem': stem + ' (a) Calculate the equilibrium price and quantity without intervention. (b) Calculate quantity demanded and supplied at the controlled price and the resulting ' + ('shortage.' if mx else 'surplus.') + extra,
            'answer': f'(a) {money(P)}, {Q} thousand. (b) Qd = {qd}, Qs = {qs}: {"shortage" if mx else "surplus"} of {gap} thousand. (c) ' + ('Queuing, waiting lists or rationing; black market at higher prices.' if mx else f'{gap},000 × ${pc} = {money(gap * 1000 * pc)}.'),
            'key': f'(a) [1] (b) Qd and Qs [1]; gap [1] (c) [2] [5]', 'marks': 5, 'type': 'multi_step'}


t13_2 = T('Indirect taxes: specific and ad valorem taxes and tax incidence', 'indirect taxes', 'specific and ad valorem', 'tax incidence')
mc(t13_2, [
    ('What is a specific tax?', 'A fixed amount of tax per unit sold', 'Shifts supply up in parallel by the tax.', ['A tax that is a percentage of the price', 'A tax on income', 'A tax paid only by consumers']),
    ('What is an ad valorem tax?', 'A tax calculated as a percentage of the price', 'e.g. VAT; supply pivots.', ['A fixed amount per unit', 'A tax on profits', 'A tax on imports only']),
    ('What is meant by the incidence of a tax?', 'How the burden of the tax is shared between consumers and producers', 'Depends on relative elasticities.', ['The amount of revenue raised', 'The rate of tax', 'Who legally pays the tax to the government']),
    ('When demand is more price inelastic than supply, the burden of an indirect tax falls mainly on', 'consumers', 'Inelastic side bears more.', ['producers', 'the government', 'equally on both']),
    ('A specific tax causes the supply curve to', 'shift vertically upwards by the amount of the tax', 'Parallel shift.', ['pivot upwards', 'shift to the right', 'become vertical']),
])
ex(t13_2, [
    ('Explain the difference between a specific tax and an ad valorem tax.', 'A specific tax is a fixed amount per unit (parallel upward shift of supply); an ad valorem tax is a percentage of price, so the tax per unit rises with price (supply curve pivots and diverges).', '1 mark each [2]'),
    ('Explain why the incidence of an indirect tax depends on the price elasticity of demand.', 'If demand is inelastic, producers can pass most of the tax on as a higher price without losing many sales, so consumers bear most; if elastic, producers absorb more.', '1 mark: inelastic → consumers; 1 mark: elastic → producers [2]'),
])
items(t13_2, 'C2', (1, 2, 3, 4), [
    ('The government of {country} raises the tax on petrol by 10 cents per litre but pump prices rise by only 7 cents. Explain what this shows about tax incidence.', 'Consumers bear 7 cents (70%) and producers 3 cents (30%): demand is relatively inelastic compared with supply.', '1 mark: shares; 1 mark: elasticity interpretation [2]'),
    ('Explain why a tax on {good} might raise little revenue if demand is very price elastic.', 'Consumers switch away when the price rises, so the quantity sold (tax base) falls sharply.', '1 mark: elastic demand; 1 mark: small tax base [2]'),
])
errs(t13_2, [
    ('An indirect tax is always paid entirely by consumers because the price rises.', 'The burden is shared; the price usually rises by less than the tax, so producers bear part, depending on elasticities.'),
    ('An ad valorem tax shifts the supply curve upwards in parallel.', 'An ad valorem tax is a percentage, so the tax per unit rises with price and the curves diverge (pivot).'),
])


@t13_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_2_tax(r, D):
    x = _tax_eq(r)
    if not x:
        return None
    a, b, c, d, P, Q, t, P1, Q1 = x
    g = r.choice(GOODS)
    pp = P1 - t
    stem = f'In the market for {g}, {qd_s(a, b)} and {qs_s(c, d)} (Q in thousands, P in dollars). The government imposes a specific tax of ${t} per unit.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the new price paid by consumers.', money(P1), f'Supply becomes Qs = {c} + {d}(P − {t}); {a} − {b}P = {c - d * t} + {d}P → P = {num(P1, 2)}.',
                  dis_num(r, P1, money, [P + t, P, pp]), mcq_D=(1, 2))
    cons = (P1 - P) * Q1
    prod = (P - pp) * Q1
    return {'stem': stem + ' (a) Calculate the equilibrium before the tax and the new price paid by consumers, price received by producers and quantity. (b) Calculate the tax revenue and the share of the tax paid by consumers. (c) Explain why consumers bear this share.',
            'answer': f'(a) Before: {money(P)}, {Q}. After: consumers pay {money(P1)}, producers receive {money(pp)}, Q = {num(Q1)}. (b) Revenue = {t} × {num(Q1)} thousand = {kd(t * Q1)}; consumers bear {pct(100 * (P1 - P) / t, 0)} (consumer burden {kd(cons)}, producer burden {kd(prod)}). (c) ' +
                      ('Demand is less elastic than supply (b < d in slope terms), so most of the tax is passed on.' if P1 - P > t / 2 else 'Supply is less elastic than demand, so producers absorb more of the tax.' if P1 - P < t / 2 else 'Demand and supply are equally responsive, so the burden is shared equally.'),
            'key': f'(a) original equilibrium [1]; new prices and quantity [2] (b) revenue [1]; consumer share {num(P1 - P, 2)}/{t} [1] (c) relative elasticities [1] [6]', 'marks': 6, 'type': 'multi_step'}


@t13_2.add('C3', (1, 2, 3, 4), 'numerical')
def t13_2_adval(r, D):
    g = r.choice(GOODS_P)
    pre = r.choice([10, 20, 25, 40, 50, 80])
    rate = r.choice([5, 10, 15, 20, 25])
    tax = pre * rate / 100
    stem = f'A {r.choice(["sales tax", "VAT"])} of {rate}% is charged on {g} in {r.choice(COUNTRIES)}. The price before tax is ${pre}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the price including tax.', money(pre + tax), f'{pre} × {1 + rate / 100} = {num(pre + tax, 2)}.', dis_num(r, pre + tax, money, [pre + rate, tax, pre * rate]), mcq_D=(1, 2))
    pre2 = pre * 1.2
    return {'stem': stem + f' (a) Calculate the tax per unit and the price including tax. (b) If the pre-tax price rises to {money(pre2)}, calculate the new tax per unit. (c) Explain why an ad valorem tax causes the supply curve to pivot rather than shift in parallel.',
            'answer': f'(a) Tax {money(tax)}; price {money(pre + tax)}. (b) {money(pre2 * rate / 100)} (c) The tax per unit is a percentage of price, so it is larger at higher prices; the vertical distance between the supply curves increases with price.',
            'key': f'(a) {rate}% × {pre} [1]; total [1] (b) [1] (c) tax rises with price [1] [4]', 'marks': 4, 'type': 'numerical'}


t13_3 = T('Subsidies: effects and incidence', 'subsidies', 'effects and incidence', 'subsidy')
mc(t13_3, [
    ('What is the effect of a subsidy to producers on the supply curve?', 'It shifts the supply curve downwards (to the right) by the amount of the subsidy', 'Lower costs.', ['It shifts supply to the left', 'It shifts demand to the right', 'It has no effect']),
    ('Who benefits from a producer subsidy when demand is price inelastic?', 'Mainly consumers, through a lower price', 'Inelastic demand → price falls by most of subsidy.', ['Mainly producers', 'Only the government', 'Neither']),
    ('Why might a government subsidise public transport?', 'To encourage use of a service with positive externalities', 'Reduce congestion/pollution.', ['To increase congestion', 'To raise tax revenue', 'To reduce consumer surplus']),
    ('What is the cost of a specific subsidy to the government?', 'The subsidy per unit multiplied by the new quantity', 'Subsidy × Q1.', ['The subsidy per unit multiplied by the old quantity', 'The change in price', 'The change in quantity']),
    ('Which is a possible disadvantage of subsidies?', 'They have an opportunity cost and may make firms inefficient', 'Dependence; cost to taxpayers.', ['They always raise prices', 'They reduce output', 'They create shortages']),
])
ex(t13_3, [
    ('Explain how a subsidy affects the price and quantity in a market.', 'A subsidy lowers producers’ costs, shifting supply right/down; price paid by consumers falls and quantity rises; producers receive the market price plus the subsidy.', '1 mark: supply shift; 1 mark: lower price/higher quantity [2]'),
    ('Explain two possible problems of using subsidies to encourage consumption of merit goods.', 'Opportunity cost/tax burden; firms may become inefficient or dependent; difficult to set the right amount; benefit may go to producers rather than consumers.', '1 mark each problem explained [4]'),
])
items(t13_3, 'C2', (1, 2, 3, 4), [
    ('The government of {country} subsidises solar panels. Explain why it might do this.', 'Solar power creates positive externalities (less pollution) and the subsidy lowers prices, increasing take-up towards the social optimum; it may also support a new industry.', '1 mark: externality; 1 mark: lower price/more use [2]'),
    ('A subsidy of $5 per unit on {mgood} lowers the price paid by consumers by only $1. Explain what this shows about elasticities.', 'Most of the subsidy is kept by producers ($4), so demand is relatively elastic compared with supply.', '1 mark: incidence; 1 mark: elasticity [2]'),
])
errs(t13_3, [
    ('A subsidy always lowers the price paid by consumers by the full amount of the subsidy.', 'The price falls by less than the subsidy unless demand is perfectly inelastic or supply perfectly elastic; producers keep part.'),
])


@t13_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_3_sub(r, D):
    x = _tax_eq(r, sub=True)
    if not x:
        return None
    a, b, c, d, P, Q, s, P1, Q1 = x
    g = r.choice(MGOODS)
    stem = f'In the market for {g}, {qd_s(a, b)} and {qs_s(c, d)} (Q in thousands, P in dollars). The government gives producers a subsidy of ${s} per unit.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the new price paid by consumers.', money(P1), f'Qs = {c} + {d}(P + {s}); {a} − {b}P = {c + d * s} + {d}P → P = {num(P1, 2)}.', dis_num(r, P1, money, [P - s, P, P1 + s]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the new price paid by consumers, the price received by producers and the new quantity. (b) Calculate the total cost of the subsidy to the government. (c) Calculate the share of the subsidy received by consumers and comment.',
            'answer': f'(a) Consumers {money(P1)}, producers {money(P1 + s)}, Q = {num(Q1)} thousand. (b) {s} × {num(Q1)} thousand = {kd(s * Q1)}. (c) Consumers gain {money(P - P1)} per unit ({pct(100 * (P - P1) / s, 0)} of the subsidy): ' + ('consumers gain most, demand relatively inelastic.' if P - P1 > s / 2 else 'producers gain most, supply relatively inelastic.' if P - P1 < s / 2 else 'shared equally.'),
            'key': '(a) [2] (b) [1] (c) share and comment [2] [5]', 'marks': 5, 'type': 'multi_step'}


POL_CASES = [
    ('The government of {country} builds and runs free public libraries.', 'Direct provision', 'the state supplies the good itself, financed by taxes.'),
    ('{country} bans smoking in all restaurants and offices.', 'Rules and regulations', 'a legal restriction on behaviour.'),
    ('Food sold in {country} must show its calorie and sugar content.', 'Provision of information', 'reduces information failure so consumers make better choices.'),
    ('Car makers selling in {country} must meet strict emission limits.', 'Rules and regulations', 'legal standards that firms must meet.'),
    ('The health ministry of {country} runs a TV campaign on the dangers of drink-driving.', 'Provision of information', 'improves knowledge of harms.'),
    ('{city} council operates its own bus network.', 'Direct provision', 'public sector supply of the service.'),
    ('A tax of 20% is added to the price of sugary drinks in {country}.', 'Indirect tax', 'raises the price to reduce consumption.'),
    ('Farmers in {country} receive $50 per hectare for planting trees.', 'Subsidy', 'payment that lowers costs/raises the return to an activity.'),
]
POL_LABELS = ['Direct provision', 'Rules and regulations', 'Provision of information', 'Indirect tax', 'Subsidy']

t13_4 = T('Direct provision, rules and regulations and provision of information', 'direct provision', 'rules and regulations', 'provision of information')
mc(t13_4, [
    ('Which is an example of direct provision by the government?', 'State-run schools that charge no fees', 'Government produces/supplies the good.', ['A tax on cigarettes', 'A ban on advertising', 'A subsidy to private schools']),
    ('Which is an advantage of regulation compared with a tax?', 'It can set a definite limit on a harmful activity', 'Certainty of outcome.', ['It raises revenue for the government', 'It is costless to enforce', 'It always increases efficiency']),
    ('What is the main aim of providing information to consumers?', 'To correct information failure so consumers make better choices', 'Labelling, campaigns.', ['To raise tax revenue', 'To increase prices', 'To reduce competition']),
    ('Which is a problem with regulation?', 'It needs monitoring and enforcement, which is costly', 'Costs and possible evasion.', ['It always leads to shortages', 'It increases tax revenue', 'It has no effect on firms']),
    ('Why might information campaigns have only a small effect on smoking?', 'Addiction and habit mean many smokers ignore the information', 'Behaviour hard to change.', ['Smokers already pay too little', 'Cigarettes are public goods', 'Information is too cheap']),
])
ex(t13_4, [
    ('Explain one advantage and one disadvantage of using regulation to reduce pollution.', 'Advantage: clear, enforceable limits with certain outcomes. Disadvantage: costly to monitor; no incentive to cut below the limit; may be set at the wrong level; firms may relocate.', '1 mark: advantage; 1 mark: disadvantage [2]'),
    ('Explain why a government might choose to provide healthcare directly rather than subsidise private providers.', 'Ensures universal access regardless of ability to pay, controls quality and coverage; avoids profit-driven under-provision in poor areas.', '1 mark: equity/access; 1 mark: control [2]'),
])
classify(t13_4, POL_CASES, POL_LABELS, 'Which method of government intervention is used?', 'Identify the method of intervention in each case and explain how it works.', name='policy')
items(t13_4, 'C2', (1, 2, 3, 4), [
    ('The government of {country} requires all food packaging to carry traffic-light labels for sugar and fat. Explain how this could improve the allocation of resources.', 'Better information reduces information failure, so consumers buy fewer unhealthy foods, moving consumption towards the social optimum.', '1 mark: corrects info failure; 1 mark: consumption change [2]'),
])
errs(t13_4, [
    ('Regulation has no costs for the government because firms simply obey the rules.', 'Regulations must be monitored and enforced, which uses resources; firms may evade them.'),
])


@t13_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_4_reg(r, D):
    c = r.choice(COUNTRIES)
    e0 = r.choice([500, 800, 1000, 1200])
    cap = r.choice([20, 25, 30, 40])
    insp = r.choice([200, 300, 400])
    costi = r.choice([40000, 50000, 60000])
    stem = f'Factories in {c} emit {e0} thousand tonnes of pollutant a year. A regulation requires a {cap}% cut. Enforcement needs {insp} inspectors costing ${costi:,} a year each.'
    cut = e0 * cap / 100
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the permitted level of emissions after the regulation.', f'{num(e0 - cut)} thousand tonnes', f'{e0} × (1 − {cap / 100}).', [f'{num(x)} thousand tonnes' for x in (cut, e0, e0 + cut, e0 * cap / 1000)], mcq_D=(1, 2))
    ec = insp * costi
    return {'stem': stem + ' (a) Calculate the reduction in emissions and the annual enforcement cost. (b) Calculate the enforcement cost per tonne of pollutant removed. (c) Explain one advantage of a pollution tax over this regulation.',
            'answer': f'(a) {num(cut)} thousand tonnes; {money(ec)}. (b) {money(ec / (cut * 1000))} per tonne. (c) A tax gives a continuing incentive to cut pollution below the limit and lets firms with low abatement costs cut most; it also raises revenue.',
            'key': '(a) both [2] (b) cost ÷ tonnes [1] (c) incentive/revenue [1] [4]', 'marks': 4, 'type': 'numerical'}


UC_CASES = [
    ('Rent controls in {city} led landlords to sell their flats rather than let them, reducing the supply of rental housing.', 'Reduced supply/shortage', 'lower returns cut the incentive to supply.'),
    ('A high tax on cigarettes in {country} led to a rise in smuggling.', 'Illegal (black) markets', 'large price gaps make evasion profitable.'),
    ('A subsidy to farmers in {country} produced large surpluses that had to be stored.', 'Over-production and waste', 'the subsidy encouraged output beyond what consumers want.'),
    ('A ban on single-use plastic bags in {city} increased the use of thicker bags made from more plastic.', 'Substitution into other harmful goods', 'consumers switched to alternatives with their own problems.'),
    ('A maximum price for petrol in {country} led to long queues at filling stations.', 'Reduced supply/shortage', 'quantity demanded exceeds quantity supplied at the controlled price.'),
    ('A minimum price for alcohol in {country} led some drinkers to buy cheaper illegal spirits.', 'Illegal (black) markets', 'consumers seek cheaper unregulated sources.'),
]

t13_5 = T('Unintended consequences of government intervention', 'unintended consequences', 'government failure')
mc(t13_5, [
    ('What is meant by an unintended consequence of government intervention?', 'An outcome of a policy that was not planned or expected', 'Side effects that may worsen allocation.', ['The intended result of a policy', 'A policy that is never implemented', 'A tax that raises more revenue than planned']),
    ('Which is an unintended consequence of a high tax on cigarettes?', 'Increased smuggling and illegal sales', 'Black markets.', ['Lower cigarette consumption', 'Higher tax revenue', 'Better health']),
    ('What is meant by government failure?', 'When government intervention leads to a worse allocation of resources than before', 'Intervention makes things worse.', ['When a government loses an election', 'When a firm goes bankrupt', 'When markets fail to provide public goods']),
    ('Why might a government set a tax at the wrong level?', 'It lacks accurate information about external costs', 'Information problems.', ['It knows the exact social cost', 'Taxes cannot be changed', 'Demand never changes']),
])
ex(t13_5, [
    ('Explain two reasons why government intervention may lead to unintended consequences.', 'Imperfect information about costs/benefits; people change behaviour (evasion, substitution, black markets); administrative costs; political pressures; time lags.', '1 mark each reason explained [4]'),
    ('Explain how a maximum price can lead to a black market.', 'The shortage at the controlled price means some buyers are willing to pay more; sellers can sell illegally at higher prices.', '1 mark: shortage; 1 mark: illegal sales above controlled price [2]'),
])
classify(t13_5, UC_CASES, ['Reduced supply/shortage', 'Illegal (black) markets', 'Over-production and waste', 'Substitution into other harmful goods'], 'Which unintended consequence is shown?',
         'Identify the unintended consequence in each case and explain why it arose.', name='uc')
items(t13_5, 'C2', (1, 2, 3, 4), [
    ('The government of {country} pays firms a subsidy for each worker they train. Explain one possible unintended consequence.', 'Firms may claim for training they would have done anyway (deadweight), or provide low-quality training to collect the subsidy.', '1 mark: consequence; 1 mark: explanation [2]'),
])
errs(t13_5, [
    ('Government intervention always improves the allocation of resources because the government acts in the public interest.', 'Intervention can cause government failure through poor information, unintended consequences, administrative costs or political motives.'),
])


@t13_5.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_5_smuggle(r, D):
    c = r.choice(COUNTRIES)
    t0, t1 = r.choice([(2, 4), (3, 5), (1.5, 3)])
    l0, l1 = r.choice([(500, 450), (800, 700), (600, 560)])
    s0, s1 = r.choice([(5, 15), (8, 20), (4, 12)])
    rev0, rev1 = t0 * l0, t1 * l1
    stem = (f'{c} raised the tax on a packet of cigarettes from ${t0} to ${t1}. Legal sales fell from {l0} million to {l1} million packets, while the estimated share of cigarettes smoked that were smuggled rose from {s0}% to {s1}%.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the change in tax revenue (in millions of dollars).', f'${num(rev1 - rev0)} million', f'{t1} × {l1} − {t0} × {l0}.', dis_num(r, rev1 - rev0, lambda v: f'${num(v)} million', [rev1, (t1 - t0) * l0]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate tax revenue before and after. (b) Explain why the fall in legal sales may overstate the health benefit. (c) Discuss briefly whether this is an example of government failure.',
            'answer': f'(a) ${num(rev0)}m → ${num(rev1)}m. (b) Some smokers switched to smuggled cigarettes, so total smoking fell by less than legal sales. (c) Partly: smuggling is an unintended consequence that reduces revenue and effectiveness; but if smoking still fell and revenue rose, the policy may still improve welfare.',
            'key': '(a) [2] (b) substitution to illegal supply [1] (c) judgement [2] [5]', 'marks': 5, 'type': 'multi_step'}


def _ch13_case(r, D):
    d = ctx(r)
    x = _tax_eq(r)
    if not x:
        return None
    a, b, c, dd, P, Q, t, P1, Q1 = x
    intro = (f'Extract: The government of {d["country"]} plans to tax {d["good"]} to reduce consumption. Economists estimate the market as {qd_s(a, b)} and {qs_s(c, dd)} (Q in thousands per week, P in dollars). '
             f'The proposed tax is ${t} per unit. Some ministers prefer a ban on advertising or a public information campaign instead.')
    parts = [
        lambda r: ('Calculate the equilibrium price and quantity before the tax.', f'{money(P)}, {Q}', '[2]'),
        lambda r: ('Calculate the new price paid by consumers and the new quantity.', f'{money(P1)}, {num(Q1)}', '[2]'),
        lambda r: ('Calculate the weekly tax revenue.', kd(t * Q1), f'{t} × {num(Q1)} thousand [1]'),
        lambda r: ('Explain how the incidence of the tax is shared between consumers and producers.', f'Consumers pay {money(P1 - P)} more per unit; producers receive {money(t - (P1 - P))} less; depends on relative elasticities.', '[3]'),
        lambda r: ('Discuss whether a tax is better than regulation or information as a way of reducing consumption.', 'Tax: price signal, revenue, but regressive, smuggling, inelastic demand; regulation certain but costly to enforce; information tackles cause but slow; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t13_1, t13_2, t13_3, t13_4, t13_5], _ch13_case)
essay(t13_1, [
    ('With the help of diagrams, explain the effects of a maximum price and a minimum price on a market.',
     'Max below equilibrium → shortage, rationing, black market; min above → surplus, government purchase; diagrams.',
     'maximum prices are an effective way of helping low-income consumers in {country}',
     'Lower prices for essentials such as food and rent; equity.',
     'Shortages mean many cannot buy at all; black markets, falling quality and supply; better to use income transfers; depends on the level set and enforcement.'),
])
essay(t13_2, [
    ('Explain, with the help of a diagram, how the incidence of an indirect tax depends on price elasticity of demand.',
     'Specific tax shifts supply; incidence shown by price rise vs tax; inelastic demand → consumers bear more; elastic → producers; tax revenue area.',
     'indirect taxes are the best way to reduce consumption of demerit goods',
     'Price signal internalises costs; revenue for health spending; flexible.',
     'Inelastic demand limits effect; regressive; smuggling; regulation or information may be more effective; combination.'),
])
essay(t13_3, [
    ('Explain, with the help of a diagram, how a subsidy affects a market.',
     'Supply shifts right/down by subsidy; lower consumer price, higher producer price, larger quantity; cost to government; incidence.',
     'subsidies are a better method than direct provision to increase the consumption of merit goods',
     'Use private sector efficiency; consumer choice; lower cost.',
     'May not reach the poor; producers capture subsidy; quality uneven; direct provision ensures access; opportunity cost and government failure in both.'),
])
essay(t13_4, [
    ('Explain how direct provision, regulation and the provision of information can each be used to correct market failure.',
     'Direct provision for public/merit goods; regulation sets standards and bans; information corrects information failure; examples.',
     'regulation is the most effective way of reducing pollution in {country}',
     'Certainty, quick, enforceable limits; simple to understand.',
     'Enforcement costs, no incentive beyond the limit, inflexible; taxes and permits more efficient; information campaigns cheap; depends on the pollutant.'),
])
essay(t13_5, [
    ('Explain why government intervention in markets may have unintended consequences.',
     'Information problems, behavioural responses (black markets, substitution), administrative costs, political pressures; examples.',
     'the risk of government failure means governments in {country} should intervene in markets as little as possible',
     'Government lacks information, may be captured by interest groups; intervention can make outcomes worse.',
     'Market failures can be severe (public goods, externalities); careful design and evaluation reduce risk; choose policies with fewer side effects; judgement.'),
])
CHAPTERS[13] = [t13_1, t13_2, t13_3, t13_4, t13_5]

# ============================================================================ 14 Equity and redistribution of income and wealth
t14_1 = T('Equity and equality; income and wealth', 'equity and equality', 'income and wealth')
mc(t14_1, [
    ('What is the difference between equity and equality?', 'Equity means fairness; equality means everyone has the same', 'Equity is a normative concept about fairness; equality is equal shares.',
     ['They mean the same thing', 'Equity means equal incomes; equality means fair incomes', 'Equity refers to wealth; equality refers to income']),
    ('What is the difference between income and wealth?', 'Income is a flow of money over time; wealth is a stock of assets at a point in time', 'Flow vs stock.', ['Income is a stock; wealth is a flow', 'Wealth is earned from work only', 'There is no difference']),
    ('Which is an example of wealth?', 'A house owned by a family', 'Assets: property, shares, savings.', ['A monthly salary', 'A pension payment received each month', 'Interest received this year']),
    ('Why is wealth usually distributed more unequally than income?', 'Wealth accumulates and is passed on through inheritance', 'Returns on assets compound; inheritance.', ['Wealth is taxed more heavily', 'Incomes are fixed by law', 'Wealth cannot be measured']),
    ('Which is a source of income?', 'Interest on savings', 'Factor incomes: wages, rent, interest, profit; transfers.', ['A house', 'A share portfolio', 'A car']),
])
ex(t14_1, [
    ('Explain the difference between horizontal equity and vertical equity.', 'Horizontal equity: people in the same circumstances are treated the same. Vertical equity: people in different circumstances are treated differently, e.g. the rich pay more tax.', '1 mark each [2]'),
    ('Explain why an equal distribution of income may not be equitable.', 'People differ in needs, effort, skills and responsibilities; giving everyone the same income ignores these differences and may reduce incentives.', '1 mark: different needs/effort; 1 mark: incentives [2]'),
    ('Explain how wealth can generate income.', 'Assets earn returns: property earns rent, savings earn interest, shares pay dividends; so wealthy people receive extra income.', '1 mark: assets yield returns; 1 mark: example [2]'),
])
IW_CASES = [
    ('{person} receives a monthly salary of $3,000.', 'Income', 'a flow of money received over time.'),
    ('{person} owns shares in {firm} worth $50,000.', 'Wealth', 'a stock of assets at a point in time.'),
    ('{person} receives $400 rent each month from a flat.', 'Income', 'a flow of money (rent).'),
    ('{person} has $20,000 in a savings account.', 'Wealth', 'a stock of financial assets.'),
    ('{person} owns a house in {city} worth $300,000.', 'Wealth', 'a physical asset.'),
    ('{person} receives a state pension each month.', 'Income', 'a transfer payment received over time.'),
]
classify(t14_1, IW_CASES, ['Income', 'Wealth'], 'Is this an example of income or wealth?', 'Classify each as income or wealth and explain.', extra=['Neither income nor wealth', 'Both income and wealth'], name='iw')
items(t14_1, 'C2', (1, 2, 3, 4), [
    ('In {country}, the richest 10% of households receive 35% of income but own 60% of wealth. Explain why wealth is more unequally distributed than income.', 'Wealth accumulates over generations through inheritance and returns on assets; those with high incomes can save more, adding to wealth, while poorer households save little.', '1 mark: inheritance/accumulation; 1 mark: saving and returns [2]'),
])
errs(t14_1, [
    ('Equity means that everyone should have exactly the same income.', 'Equity means fairness; equality means the same shares. A fair distribution may still be unequal.'),
    ('A person’s salary is part of their wealth.', 'A salary is income (a flow); wealth is the stock of assets owned.'),
])


@t14_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t14_1_share(r, D):
    c = r.choice(COUNTRIES)
    shares = r.choice([[4, 9, 15, 22, 50], [6, 11, 16, 22, 45], [3, 8, 14, 23, 52], [8, 13, 18, 23, 38]])
    pop = r.choice([5, 8, 10, 20])
    tot = pop * r.choice([20, 30, 40, 50])
    tab = table(['Quintile (20% of households)', 'Share of income (%)'], list(zip(['Poorest', 'Second', 'Third', 'Fourth', 'Richest'], shares)))
    ratio = shares[4] / shares[0]
    stem = f'Total household income in {c} is ${tot} billion and there are {pop} million households. {tab}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate how many times greater the income share of the richest 20% is than that of the poorest 20%.', num(ratio, 2), f'{shares[4]}/{shares[0]} = {num(ratio, 2)}.', dis_num(r, ratio, lambda v: num(v, 2), [shares[4] - shares[0]]), mcq_D=(1, 2))
    avg_r = tot * 1e9 * shares[4] / 100 / (pop * 1e6 / 5)
    avg_p = tot * 1e9 * shares[0] / 100 / (pop * 1e6 / 5)
    return {'stem': stem + ' (a) Calculate the average income of a household in the richest and poorest quintiles. (b) Explain whether this distribution is equitable.',
            'answer': f'(a) Richest: {money(avg_r)}; poorest: {money(avg_p)}. (b) It is unequal (ratio {num(ratio, 1)}:1); whether it is equitable is a normative judgement depending on needs, effort and opportunities; many would see large gaps as inequitable.',
            'key': f'(a) {tot}bn × {shares[4]}% ÷ {num(pop / 5, 1)}m and {tot}bn × {shares[0]}% ÷ {num(pop / 5, 1)}m [2] (b) equality vs equity, normative judgement [2] [4]', 'marks': 4, 'type': 'numerical'}


def tax_due(y, bands):
    """bands: list of (upper limit or None, rate%)."""
    t, lo = 0, 0
    for up, rate in bands:
        top = y if up is None else min(y, up)
        if top > lo:
            t += (top - lo) * rate / 100
        if up is None or y <= up:
            break
        lo = up
    return t


t14_2 = T('Policies to reduce inequality: progressive taxation, transfer payments and minimum wage', 'policies to reduce inequality', 'progressive taxation', 'transfer payments', 'minimum wage')
mc(t14_2, [
    ('What is a progressive tax?', 'A tax where the proportion of income paid in tax rises as income rises', 'Average rate rises with income.', ['A tax where everyone pays the same amount', 'A tax that takes a smaller proportion from the rich', 'A tax on goods and services']),
    ('What is a transfer payment?', 'A payment from the government for which no good or service is provided in return', 'e.g. pensions, unemployment benefits.', ['A payment for work done', 'A tax on imports', 'A payment between two firms']),
    ('How does a national minimum wage aim to reduce inequality?', 'By raising the pay of the lowest-paid workers', 'Raises the floor of wages.', ['By reducing the incomes of the rich', 'By lowering prices', 'By cutting income tax']),
    ('Which is a possible disadvantage of a minimum wage set above the equilibrium wage?', 'Unemployment among low-skilled workers', 'Excess supply of labour.', ['Higher profits for firms', 'Lower wages for low-paid workers', 'A shortage of labour']),
    ('What is the marginal rate of tax?', 'The rate of tax paid on an additional unit of income', 'vs average rate = total tax/income.', ['Total tax divided by total income', 'The lowest rate of tax', 'The tax on goods']),
])
ex(t14_2, [
    ('Explain how a progressive income tax combined with transfer payments can reduce income inequality.', 'Higher earners pay a larger proportion of income in tax, reducing top incomes; the revenue funds transfers to low-income households, raising their incomes.', '1 mark: progressive tax reduces high incomes; 1 mark: transfers raise low incomes [2]'),
    ('Explain two possible disadvantages of a national minimum wage.', 'Unemployment if set above equilibrium; higher costs for firms and prices; may not target the poorest households (many are not in work); informal employment.', '1 mark each, 1 mark each explained [4]'),
    ('Explain the difference between the average rate and the marginal rate of income tax.', 'Average rate = total tax ÷ total income; marginal rate = tax on an extra unit of income. In a progressive system the marginal rate is above the average rate.', '1 mark each definition [2]'),
])
items(t14_2, 'C2', (1, 2, 3, 4), [
    ('The government of {country} raises the top rate of income tax from 40% to 50%. Explain one possible benefit and one possible problem.', 'Benefit: more revenue for redistribution, lower inequality. Problem: reduced incentives to work/invest, tax avoidance or emigration of high earners.', '1 mark: benefit; 1 mark: problem [2]'),
    ('{country} raises its minimum wage by 10%. Explain why the effect on employment depends on the elasticity of demand for labour.', 'If demand for labour is inelastic, few jobs are lost; if elastic, firms cut employment significantly.', '1 mark: inelastic small effect; 1 mark: elastic large effect [2]'),
])
errs(t14_2, [
    ('A tax is progressive if rich people pay more dollars of tax than poor people.', 'A tax is progressive if the proportion (average rate) of income paid rises with income; a proportional tax also takes more dollars from the rich.'),
    ('A minimum wage always reduces poverty.', 'It raises pay for those in work, but may cause job losses and does not help households with no one in work.'),
])


@t14_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t14_2_tax(r, D):
    c = r.choice(COUNTRIES)
    l1 = r.choice([10000, 12000, 15000])
    l2 = r.choice([40000, 50000, 60000])
    r1_, r2_, r3_ = r.choice([(0, 20, 40), (0, 25, 45), (10, 20, 40), (5, 20, 35)])
    bands = [(l1, r1_), (l2, r2_), (None, r3_)]
    y1 = r.choice([25000, 30000, 36000])
    y2 = r.choice([80000, 100000, 120000])
    t1, t2 = tax_due(y1, bands), tax_due(y2, bands)
    desc = f'0–${l1:,}: {r1_}%; ${l1:,}–${l2:,}: {r2_}%; above ${l2:,}: {r3_}%'
    stem = f'Income tax bands in {c} are: {desc}.'
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the tax paid on an income of ${y1:,}.', money(t1), f'{r1_}% × {l1:,} + {r2_}% × ({y1:,} − {l1:,}) = {num(t1)}.', dis_num(r, t1, money, [y1 * r2_ / 100, y1 * r1_ / 100 + 500]), mcq_D=(1, 2))
    return {'stem': stem + f' (a) Calculate the tax paid and the average tax rate for incomes of ${y1:,} and ${y2:,}. (b) State the marginal tax rate for each person. (c) Explain whether the tax is progressive.',
            'answer': f'(a) ${y1:,}: tax {money(t1)}, average {pct(100 * t1 / y1)}; ${y2:,}: tax {money(t2)}, average {pct(100 * t2 / y2)}. (b) {r2_}% and {r3_}%. (c) Progressive: the average rate rises with income.',
            'key': f'(a) tax for each [2]; average rates [1] (b) marginal rates [1] (c) rising average rate → progressive [1] [5]', 'marks': 5, 'type': 'multi_step'}


t14_3 = T('Universal and means-tested benefits: trade-offs between equity and efficiency', 'universal and means-tested benefits', 'equity and efficiency', 'means-tested')
mc(t14_3, [
    ('What is a means-tested benefit?', 'A benefit paid only to those whose income or wealth is below a certain level', 'Targeted at those in need.', ['A benefit paid to everyone in a group', 'A tax on high incomes', 'A benefit paid only to workers']),
    ('What is a universal benefit?', 'A benefit paid to everyone in a group regardless of income', 'e.g. child benefit for all families.', ['A benefit paid only to the poorest', 'A benefit paid by employers', 'A benefit paid only to the unemployed']),
    ('Which is an advantage of means-tested benefits?', 'They target help at those most in need, so cost less', 'Targeting.', ['They are cheap to administer', 'Everyone claims them', 'They never reduce work incentives']),
    ('What is the poverty trap?', 'A situation where earning more leaves a person little better off because benefits are withdrawn and taxes rise', 'High effective marginal tax rate.', ['A situation where prices rise faster than wages', 'A situation where everyone receives benefits', 'A trap set by moneylenders']),
    ('Which is a disadvantage of universal benefits?', 'Some of the money goes to people who do not need it', 'Poor targeting; high cost.', ['Low take-up', 'Stigma', 'Complex administration']),
])
ex(t14_3, [
    ('Explain one advantage and one disadvantage of universal benefits compared with means-tested benefits.', 'Advantage: high take-up, no stigma, cheap to administer, no poverty trap. Disadvantage: expensive, part goes to the better-off.', '1 mark: advantage; 1 mark: disadvantage [2]'),
    ('Explain why there may be a trade-off between equity and efficiency in the benefits system.', 'More generous, targeted benefits improve equity, but withdrawing them as income rises reduces incentives to work (efficiency), and higher taxes to finance them may reduce effort.', '1 mark: equity gain; 1 mark: incentive/efficiency cost [2]'),
])
items(t14_3, 'C2', (1, 2, 3, 4), [
    ('{country} replaces a universal child benefit with a means-tested one. Explain one likely effect on government spending and one on low-income families.', 'Spending falls because better-off families no longer receive it; some low-income families may not claim because of complexity/stigma, so take-up falls.', '1 mark: spending; 1 mark: take-up/effect [2]'),
])
errs(t14_3, [
    ('Means-tested benefits are always better because they only go to the poor.', 'They cost less, but take-up is often low, they are costly to administer and can create a poverty trap.'),
])


@t14_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t14_3_trap(r, D):
    c = r.choice(COUNTRIES)
    w = r.choice([100, 150, 200])
    tax = r.choice([10, 20])
    wd = r.choice([50, 60, 70, 80])
    emtr = tax + wd * (1 - tax / 100)
    keep = w * (1 - emtr / 100)
    stem = f'In {c}, a worker on benefits earns an extra ${w} a week. Income tax of {tax}% is paid on the extra earnings, and the means-tested benefit is withdrawn at {wd} cents for each dollar of after-tax earnings.'
    if D <= 2:
        return cq(r, 1, stem + ' How much of the extra $' + str(w) + ' does the worker keep?', money(keep), f'After tax {w * (1 - tax / 100)}; benefit withdrawn {wd}% of that; keep {num(keep, 2)}.', dis_num(r, keep, money, [w * (1 - tax / 100), w * (1 - wd / 100)]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the amount the worker keeps and the effective marginal tax rate. (b) Explain how this illustrates the poverty trap and suggest one policy to reduce it.',
            'answer': f'(a) Keeps {money(keep)}; effective marginal rate {pct(emtr)}. (b) High combined withdrawal of benefits and tax means little gain from working more, discouraging work; reduce the taper rate, raise tax-free allowance, or use in-work benefits.',
            'key': f'(a) {w} × (1 − {tax / 100}) × (1 − {wd / 100}) [1]; EMTR [1] (b) poverty trap [1]; policy [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch14_case(r, D):
    d = ctx(r)
    g0, g1 = r.choice([(0.32, 0.38), (0.35, 0.41), (0.28, 0.34)])
    mw = r.choice([5, 8, 10])
    intro = (f'Extract: Income inequality in {d["country"]} has risen; the Gini coefficient increased from {g0} to {g1}. The government plans to raise the minimum wage by {mw}%, '
             f'introduce a higher top rate of income tax and replace universal child benefit with a means-tested benefit. Business groups warn of job losses and reduced incentives.')
    parts = [
        lambda r: ('Calculate the percentage increase in the Gini coefficient.', pct(chg(g0, g1)), f'({g1} − {g0})/{g0} × 100 [2]'),
        lambda r: ('Explain the difference between equality and equity.', 'Equality = same shares; equity = fairness, a normative concept.', '[2]'),
        lambda r: ('Explain how a higher minimum wage could cause job losses.', 'If above equilibrium wage, demand for labour contracts while supply extends: unemployment, especially if demand for labour is elastic.', '[3]'),
        lambda r: ('Explain one advantage and one disadvantage of switching to a means-tested child benefit.', 'Targets help, lower cost vs low take-up, stigma, admin cost, poverty trap.', '[2]'),
        lambda r: ('Discuss whether the government’s policies will reduce inequality without harming efficiency.', 'Progressive tax and minimum wage raise low incomes and cut top incomes vs disincentives, avoidance, unemployment; depends on rates, elasticities and enforcement; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t14_1, t14_2, t14_3], _ch14_case)
essay(t14_1, [
    ('Explain the difference between income and wealth and between equity and equality.',
     'Income = flow; wealth = stock; sources of each; equity normative fairness (horizontal/vertical); equality same shares.',
     'a more equal distribution of income is always more equitable',
     'Large gaps reflect unequal opportunity; diminishing marginal utility of income; social cohesion.',
     'Differences in effort, skills and needs justify some inequality; incentives; equity is normative; depends on causes of inequality.'),
])
essay(t14_2, [
    ('Explain how progressive taxation and transfer payments can be used to reduce inequality.',
     'Progressive income tax: average rate rises with income; transfers: benefits and pensions to low-income groups; redistribution; examples.',
     'a national minimum wage is the most effective way to reduce poverty in {country}',
     'Raises pay of lowest earners; no direct cost to government; reduces in-work poverty.',
     'Job losses, informal sector, does not help non-workers; transfers and education may be more effective; depends on level set and labour market.'),
])
essay(t14_3, [
    ('Explain the difference between universal and means-tested benefits.',
     'Universal: all in group regardless of income; means-tested: targeted by income/wealth; examples; take-up, cost, stigma, poverty trap.',
     'means-tested benefits are better than universal benefits for {country}',
     'Lower cost, help targeted at the poor, more equity per dollar.',
     'Low take-up, stigma, admin costs, poverty trap reduces work incentives; universal benefits simpler and politically durable; trade-off between equity and efficiency.'),
])
CHAPTERS[14] = [t14_1, t14_2, t14_3]

# ============================================================================ 15 National income statistics
t15_1 = T('GDP, GNI and NNI: output, income and expenditure methods', 'gdp, gni and nni', 'output, income and expenditure methods', 'gdp')
mc(t15_1, [
    ('What is gross domestic product (GDP)?', 'The total value of output produced within a country in a year', 'Domestic: within borders, regardless of ownership.', ['The total income of a country’s citizens wherever they live', 'Total output minus depreciation', 'The value of exports minus imports']),
    ('How is gross national income (GNI) calculated from GDP?', 'GDP plus net primary income from abroad', 'GNI = GDP + income earned abroad by residents − income paid to foreigners.', ['GDP minus depreciation', 'GDP plus indirect taxes', 'GDP minus imports']),
    ('How is net national income (NNI) calculated?', 'GNI minus depreciation (capital consumption)', 'NNI = GNI − depreciation.', ['GDP plus depreciation', 'GNI plus subsidies', 'GDP minus net income from abroad']),
    ('Which is included in GDP using the expenditure method?', 'Government spending on teachers’ salaries', 'C + I + G + (X − M); transfers excluded.', ['State pension payments', 'Unemployment benefits', 'Second-hand car sales']),
    ('Why are transfer payments excluded from GDP?', 'They are not payments for current production', 'Avoids counting income without output.', ['They are too small to measure', 'They are paid by foreigners', 'They are taxed']),
    ('Why do the three methods of measuring national income give the same total in theory?', 'Spending on output becomes income for the factors that produce it', 'Output = income = expenditure.', ['Governments adjust the figures to match', 'They measure different things', 'Prices are fixed']),
])
ex(t15_1, [
    ('Explain why the output, income and expenditure methods of measuring national income should give the same result.', 'The value of output produced is spent by buyers (expenditure) and that spending is paid out as incomes (wages, rent, interest, profit) to the factors that produced it.', '1 mark: output = expenditure; 1 mark: expenditure becomes income [2]'),
    ('Explain the difference between GDP and GNI.', 'GDP measures output produced within a country’s borders; GNI adds income earned abroad by residents and subtracts income paid to foreign residents (net primary income).', '1 mark each [2]'),
    ('Explain why double counting must be avoided when measuring output.', 'Counting intermediate goods and the final goods that contain them would overstate output; use value added or final goods only.', '1 mark: problem; 1 mark: value added solution [2]'),
])
items(t15_1, 'C2', (1, 2, 3, 4), [
    ('Many workers from {country} work abroad and send income home, while foreign firms in {country} send profits overseas. Explain how this affects the difference between {country}’s GDP and GNI.', 'Income earned abroad by residents adds to GNI; profits paid to foreign owners are subtracted. GNI exceeds GDP if inflows are larger than outflows.', '1 mark: inflows add; 1 mark: outflows subtract [2]'),
])
errs(t15_1, [
    ('GNI is GDP minus depreciation.', 'GNI = GDP + net primary income from abroad; NNI = GNI − depreciation.'),
    ('State pensions should be added to GDP because they are government spending.', 'Pensions are transfer payments, not payments for current output, so they are excluded from G in GDP.'),
])


@t15_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t15_1_gdp(r, D):
    c = r.choice(COUNTRIES)
    C_ = r.choice([300, 400, 500, 600])
    I = r.choice([80, 100, 120, 150])
    G = r.choice([100, 120, 150, 180])
    X = r.choice([150, 200, 250])
    M = r.choice([140, 180, 220, 260])
    tr = r.choice([40, 50, 60])
    npi = r.choice([-20, -15, -10, 10, 15, 25])
    dep = r.choice([50, 60, 80])
    gdp = C_ + I + G + X - M
    gni = gdp + npi
    nni = gni - dep
    tab = table(['Item ($ billion)', 'Value'], [('Consumption', C_), ('Investment', I), ('Government spending on goods and services', G), ('Transfer payments', tr), ('Exports', X), ('Imports', M), ('Net primary income from abroad', npi), ('Depreciation', dep)])
    stem = f'The table shows data for {c}. {tab}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate GDP using the expenditure method.', f'${gdp} billion', f'C + I + G + (X − M) = {C_} + {I} + {G} + ({X} − {M}) = {gdp}; transfers excluded.',
                  [f'${x} billion' for x in (gdp + tr, gdp + M * 2 - X * 0 - M, C_ + I + G + X + M, gdp + npi)], mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate GDP, GNI and NNI. (b) Explain why transfer payments are not included.',
            'answer': f'(a) GDP = ${gdp}bn; GNI = ${gni}bn; NNI = ${nni}bn. (b) They are redistributions of income, not payments for current output; including them would double count.',
            'key': f'(a) GDP {C_} + {I} + {G} + {X} − {M} [1]; GNI {gdp} {"+" if npi > 0 else "−"} {abs(npi)} [1]; NNI − {dep} [1] (b) not payment for output [1] [4]', 'marks': 4, 'type': 'numerical'}


t15_2 = T('Nominal and real values, market prices and basic prices, per capita figures', 'nominal and real values', 'market prices and basic prices', 'per capita')
mc(t15_2, [
    ('What is real GDP?', 'GDP adjusted for changes in the price level', 'Real = nominal ÷ price index × 100.', ['GDP measured at current prices', 'GDP per head of population', 'GDP minus depreciation']),
    ('How is GDP at basic prices calculated from GDP at market prices?', 'Subtract indirect taxes and add subsidies', 'Basic prices = factor cost approach.', ['Add indirect taxes and subtract subsidies', 'Subtract depreciation', 'Add net income from abroad']),
    ('Why is GDP per capita used to compare living standards?', 'It takes account of differences in population size', 'GDP ÷ population.', ['It adjusts for inflation', 'It includes non-market output', 'It measures income distribution']),
    ('If nominal GDP rises by 6% and prices rise by 4%, real GDP rises by approximately', '2%', 'Real ≈ nominal − inflation.', ['10%', '6%', '4%']),
    ('What is a GDP deflator used for?', 'To convert nominal GDP into real GDP', 'Price index for all output.', ['To measure unemployment', 'To calculate the balance of payments', 'To measure income inequality']),
])
ex(t15_2, [
    ('Explain why economists use real rather than nominal GDP to measure economic growth.', 'Nominal GDP can rise just because prices rise; real GDP removes the effect of inflation, so it shows changes in the volume of output.', '1 mark: nominal includes price changes; 1 mark: real shows volume [2]'),
    ('Explain the difference between GDP at market prices and GDP at basic prices.', 'Market prices include indirect taxes and exclude subsidies paid; basic prices remove indirect taxes and add subsidies, showing the value received by producers.', '1 mark each [2]'),
])
items(t15_2, 'C2', (1, 2, 3, 4), [
    ('Nominal GDP in {country} rose by 8% last year while the population grew by 3% and prices rose by 6%. Explain whether living standards are likely to have improved.', 'Real GDP grew by about 2%, but population grew 3%, so real GDP per capita fell by about 1%: average living standards probably fell.', '1 mark: real growth ≈ 2%; 1 mark: per capita fall [2]'),
])
errs(t15_2, [
    ('If nominal GDP rises, the economy must be producing more goods and services.', 'Nominal GDP can rise because of inflation alone; only real GDP shows whether output has increased.'),
    ('GDP at basic prices is GDP at market prices plus indirect taxes.', 'Basic prices = market prices − indirect taxes + subsidies.'),
])


@t15_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t15_2_real(r, D):
    c = r.choice(COUNTRIES)
    n0 = r.choice([400, 500, 600, 800])
    p1 = r.choice([104, 105, 108, 110, 112])
    g = r.choice([5, 6, 8, 10, 12, 15])
    n1 = n0 * (1 + g / 100)
    real1 = n1 / p1 * 100
    pop0, pop1 = r.choice([(20, 20.4), (10, 10.3), (50, 50.5), (8, 8.2)])
    stem = f'In {c}, nominal GDP rose from ${n0} billion in the base year to ${num(n1, 1)} billion a year later. The GDP deflator rose from 100 to {p1}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate real GDP in the second year at base-year prices.', f'${num(real1, 1)} billion', f'{num(n1, 1)} ÷ {p1} × 100 = {num(real1, 1)}.', dis_num(r, real1, lambda v: f'${num(v, 1)} billion', [n1 * p1 / 100, n0]), mcq_D=(1, 2))
    rg = chg(n0, real1)
    pc0, pc1 = n0 * 1e9 / (pop0 * 1e6), real1 * 1e9 / (pop1 * 1e6)
    return {'stem': stem + f' Population rose from {num(pop0, 1)} million to {num(pop1, 1)} million. (a) Calculate real GDP and the real growth rate. (b) Calculate real GDP per capita in each year and its percentage change. (c) Comment on what has happened to average living standards.',
            'answer': f'(a) Real GDP ${num(real1, 1)}bn; growth {pchg(rg)}. (b) {money(pc0)} → {money(pc1)}; {pchg(chg(pc0, pc1))}. (c) ' + ('Average material living standards rose, though GDP per capita ignores distribution and non-market factors.' if pc1 > pc0 else 'Average material living standards fell because population grew faster than real output.'),
            'key': f'(a) deflate [1]; growth [1] (b) per capita values [1]; change [1] (c) comment with limitation [1] [5]', 'marks': 5, 'type': 'multi_step'}


@t15_2.add('C3', (1, 2, 3), 'numerical')
def t15_2_basic(r, D):
    c = r.choice(COUNTRIES)
    mp = r.choice([500, 600, 800, 1000])
    it = r.choice([60, 80, 100, 120])
    sb = r.choice([10, 15, 20, 25])
    bp = mp - it + sb
    stem = f'GDP at market prices in {c} is ${mp} billion. Indirect taxes are ${it} billion and subsidies ${sb} billion.'
    return cq(r, 1, stem + ' Calculate GDP at basic prices.', f'${bp} billion', f'{mp} − {it} + {sb} = {bp}.', [f'${x} billion' for x in (mp + it - sb, mp - it - sb, mp + it + sb)], mcq_D=(1, 2, 3)) if D <= 2 else {
        'stem': stem + ' (a) Calculate GDP at basic prices. (b) Explain why the adjustment is made.', 'answer': f'(a) ${bp} billion (b) Indirect taxes raise market prices without adding output; subsidies lower them; basic prices show the value received by producers.',
        'key': f'(a) {mp} − {it} + {sb} [2] (b) explanation [1] [3]', 'marks': 3, 'type': 'numerical'}


t15_3 = T('Uses and limitations of national income statistics', 'uses and limitations of national income statistics', 'limitations')
mc(t15_3, [
    ('Which is a limitation of GDP per capita as a measure of living standards?', 'It does not show how income is distributed', 'Average hides inequality.', ['It is adjusted for population size', 'It is measured in real terms', 'It includes all market output']),
    ('Which activity is not included in GDP?', 'Unpaid housework', 'Non-market output excluded.', ['Wages paid to teachers', 'Spending on new machinery', 'Exports of services']),
    ('Why might GDP understate output in a developing country?', 'A large informal (hidden) economy is not recorded', 'Informal/subsistence activity.', ['Prices are too high', 'Exports are counted twice', 'Population is too small']),
    ('What is purchasing power parity (PPP) used for?', 'To compare GDP between countries taking account of differences in the cost of living', 'Adjusts for price levels.', ['To measure inflation', 'To calculate the trade balance', 'To measure unemployment']),
    ('Why might GDP rise while welfare falls?', 'Higher output may cause more pollution and longer working hours', 'Externalities and leisure not counted.', ['Because GDP excludes all government spending', 'Because GDP is measured in real terms', 'Because GDP counts only exports']),
])
ex(t15_3, [
    ('Explain two limitations of using GDP per capita to compare living standards between countries.', 'Different price levels and exchange rates (use PPP); informal economy; distribution of income; non-market output; environmental costs; hours worked; quality of goods.', '1 mark each limitation, 1 mark each explained [4]'),
    ('Explain two uses of national income statistics.', 'Measuring growth over time; comparing living standards; informing government policy (fiscal/monetary); helping firms plan; international comparisons.', '1 mark each use explained [2]'),
])
items(t15_3, 'C2', (1, 2, 3, 4), [
    ('{country} has a higher GDP per capita than {country2}, but life expectancy is lower and pollution is higher. Explain why GDP per capita may give a misleading view of living standards.', 'GDP ignores health, environmental quality and distribution; higher output may come with costs that reduce welfare.', '1 mark: GDP omits these; 1 mark: welfare implication [2]'),
    ('A large share of economic activity in {country} takes place in the informal sector. Explain how this affects GDP statistics.', 'Informal activity is unrecorded, so official GDP understates true output and income.', '1 mark: unrecorded; 1 mark: understates [2]'),
])
errs(t15_3, [
    ('A country with a higher GDP than another must have higher living standards.', 'Total GDP ignores population, price levels, distribution and non-market factors; GDP per capita at PPP is a better but still imperfect guide.'),
])


@t15_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t15_3_compare(r, D):
    a, b = r.sample(COUNTRIES, 2)
    ga, gb = r.choice([(400, 120), (900, 300), (250, 80)])
    pa, pb = r.choice([(80, 15), (100, 20), (50, 12)])
    pppa, pppb = r.choice([(1.0, 0.5), (1.0, 0.4), (1.1, 0.6)])
    pca, pcb = ga * 1e9 / (pa * 1e6), gb * 1e9 / (pb * 1e6)
    tab = table(['', a, b], [('GDP ($ billion)', ga, gb), ('Population (million)', pa, pb), ('Price level relative to the world average', pppa, pppb)])
    stem = f'{tab}.'
    if D <= 2:
        return cq(r, 1, stem + f' Calculate GDP per capita in {b}.', money(pcb), f'{gb}bn ÷ {pb}m.', dis_num(r, pcb, money, [pca, gb / pb]), mcq_D=(1, 2))
    adj_a, adj_b = pca / pppa, pcb / pppb
    return {'stem': stem + f' (a) Calculate GDP per capita in each country. (b) Adjust each figure for the price level (divide by the relative price level) and comment on the comparison. (c) Explain two other factors that should be considered when comparing living standards.',
            'answer': f'(a) {a}: {money(pca)}; {b}: {money(pcb)}. (b) {a}: {money(adj_a)}; {b}: {money(adj_b)}: the gap narrows because prices are lower in {b}. (c) Income distribution, informal economy, health and education, pollution, hours worked.',
            'key': '(a) both [1] (b) adjusted figures [1]; comment [1] (c) two factors [2] [5]', 'marks': 5, 'type': 'multi_step'}


def _ch15_case(r, D):
    d = ctx(r)
    n0, n1 = r.choice([(500, 560), (800, 880), (300, 342)])
    inf = r.choice([4, 6, 8])
    pg = r.choice([1, 2, 3])
    intro = (f'Extract: Nominal GDP in {d["country"]} rose from ${n0} billion to ${n1} billion, while the price level rose by {inf}% and the population by {pg}%. '
             f'The government claims living standards have “risen sharply”. However, an estimated 30% of activity takes place in the informal economy and air pollution in {d["city"]} has worsened.')
    real = n1 / (1 + inf / 100)
    parts = [
        lambda r: ('Calculate the percentage increase in nominal GDP.', pct(chg(n0, n1)), '[1]'),
        lambda r: ('Calculate real GDP in the second year in base-year prices.', f'${num(real, 1)} billion', f'{n1} ÷ {1 + inf / 100} [2]'),
        lambda r: ('Explain the difference between nominal and real GDP.', 'Nominal at current prices; real adjusted for inflation, shows volume of output.', '[2]'),
        lambda r: ('Explain two reasons why GDP figures may not accurately reflect living standards in the country.', 'Informal economy unrecorded; pollution and other externalities; distribution; population growth.', '[4]'),
        lambda r: ('Discuss whether the government is right to claim that living standards have risen sharply.', f'Real growth ≈ {num(chg(n0, real), 1)}%, per capita ≈ {num(chg(n0, real) - pg, 1)}%: modest; informal sector may understate; pollution and distribution reduce welfare; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t15_1, t15_2, t15_3], _ch15_case)
essay(t15_1, [
    ('Explain the three methods of measuring national income and why they should give the same result.',
     'Output (value added), income (factor incomes), expenditure (C + I + G + X − M); circular flow identity; exclude transfers and second-hand sales; GDP, GNI, NNI.',
     'GNI is a better measure of a country’s economic performance than GDP',
     'GNI includes income earned by residents abroad; reflects income available to the nation.',
     'GDP measures domestic production and employment; for countries with large foreign ownership GNI is lower; both ignore depreciation (NNI) and welfare factors.'),
])
essay(t15_2, [
    ('Explain the difference between nominal and real GDP and between market prices and basic prices.',
     'Nominal vs real (deflator); market vs basic (indirect taxes, subsidies); per capita figures; examples.',
     'real GDP per capita is the best indicator of living standards in {country}',
     'Adjusts for inflation and population; widely available; correlates with health and education.',
     'Ignores distribution, informal sector, environment, leisure, quality; PPP adjustments needed; HDI and other indicators; judgement.'),
])
essay(t15_3, [
    ('Explain the uses of national income statistics.',
     'Measure growth, compare over time and between countries, inform policy, firms’ planning, international organisations.',
     'national income statistics are too inaccurate to be useful for comparing living standards between countries',
     'Informal economy, different price levels, distribution, non-market activity, data quality.',
     'PPP and per capita adjustments reduce problems; trends useful; combine with other indicators; still the best available single measure.'),
])
CHAPTERS[15] = [t15_1, t15_2, t15_3]

# ============================================================================ 16 Introduction to the circular flow of income
FLOW_CASES = [
    ('A firm in {country} buys new machinery.', 'Injection', 'investment adds spending to the circular flow.'),
    ('Households in {country} put part of their income into savings accounts.', 'Leakage (withdrawal)', 'saving is income not passed on as spending.'),
    ('The government of {country} pays nurses’ salaries.', 'Injection', 'government spending adds to the flow.'),
    ('Consumers in {country} buy cars made abroad.', 'Leakage (withdrawal)', 'imports send spending out of the domestic flow.'),
    ('Workers in {country} pay income tax.', 'Leakage (withdrawal)', 'taxation removes income from the flow.'),
    ('Tourists from abroad spend money in hotels in {city}.', 'Injection', 'exports (of services) bring spending into the flow.'),
    ('{firm} sells {mgood} to buyers in {country2}.', 'Injection', 'exports are an injection.'),
]

t16_1 = T('The circular flow of income in closed and open economies', 'circular flow of income', 'closed and open economies')
mc(t16_1, [
    ('In the simplest two-sector circular flow, what do households supply to firms?', 'Factors of production', 'Households → factors; firms → goods/services; income flows back.', ['Goods and services', 'Taxes', 'Exports']),
    ('What is a closed economy?', 'An economy with no international trade', 'No exports or imports.', ['An economy with no government', 'An economy with no savings', 'An economy where all firms are state-owned']),
    ('In the circular flow, what do firms pay households in return for factors of production?', 'Factor incomes such as wages, rent, interest and profit', 'Income flow.', ['Taxes', 'Subsidies', 'Transfer payments only']),
    ('Which sector is added when moving from a closed to an open economy model?', 'The foreign (international) sector', 'Exports and imports.', ['The government sector', 'The financial sector', 'The household sector']),
    ('In a two-sector economy with no saving, what happens to the level of national income?', 'It stays constant', 'All income is spent; no leakages or injections.', ['It rises continuously', 'It falls continuously', 'It becomes zero']),
])
ex(t16_1, [
    ('Explain the circular flow of income in a two-sector economy.', 'Households supply factors of production to firms and receive factor incomes; they spend this income on goods and services produced by firms, so money flows round from firms to households and back.', '1 mark: real flows; 1 mark: money flows; 1 mark: circularity [3]'),
    ('Explain how adding a government sector changes the circular flow.', 'Taxes are withdrawn from the flow and government spending is injected into it; national income depends on the balance between them as well as saving/investment.', '1 mark: taxes leak; 1 mark: spending injects [2]'),
])
classify(t16_1, FLOW_CASES, ['Injection', 'Leakage (withdrawal)'], 'Is this an injection into or a leakage from the circular flow?', 'For each, state whether it is an injection or a leakage and explain.', extra=['Neither: a transfer within the flow', 'A real flow of goods'], name='flows')
items(t16_1, 'C2', (1, 2, 3, 4), [
    ('{country} opens up to international trade. Explain how this changes its circular flow of income.', 'Exports become an injection (foreign spending on domestic output) and imports a leakage (domestic spending on foreign output).', '1 mark: exports injection; 1 mark: imports leakage [2]'),
])
errs(t16_1, [
    ('In the circular flow, households supply goods and services to firms.', 'Households supply factors of production; firms supply goods and services to households.'),
])


@t16_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t16_1_flow(r, D):
    c = r.choice(COUNTRIES)
    Y = r.choice([500, 800, 1000, 1200])
    s = r.choice([10, 15, 20])
    t = r.choice([15, 20, 25])
    m = r.choice([10, 15, 20])
    S, Tx, M = Y * s / 100, Y * t / 100, Y * m / 100
    C_ = Y - S - Tx - M
    stem = f'In {c}, national income is ${Y} billion. Households save {s}%, pay {t}% in tax and spend {m}% on imports.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate spending on domestically produced goods and services.', f'${num(C_)} billion', f'{Y} − {num(S)} − {num(Tx)} − {num(M)}.', dis_num(r, C_, lambda v: f'${num(v)} billion', [Y - S, Y - S - Tx]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate total leakages. (b) Calculate the total injections needed to keep national income constant, and explain why.',
            'answer': f'(a) ${num(S + Tx + M)} billion (b) ${num(S + Tx + M)} billion: income is constant when injections (I + G + X) equal leakages (S + T + M).',
            'key': '(a) S + T + M [2] (b) equal to leakages [1]; equilibrium condition [1] [4]', 'marks': 4, 'type': 'numerical'}


t16_2 = T('Injections and leakages: investment, government spending, exports, saving, taxation and imports', 'injections and leakages', 'investment, government spending, exports', 'saving, taxation and imports')
mc(t16_2, [
    ('Which are the three injections into the circular flow?', 'Investment, government spending and exports', 'I + G + X.', ['Saving, taxation and imports', 'Consumption, saving and investment', 'Wages, rent and profit']),
    ('Which are the three leakages (withdrawals) from the circular flow?', 'Saving, taxation and imports', 'S + T + M.', ['Investment, government spending and exports', 'Consumption, investment and exports', 'Wages, rent and interest']),
    ('Which of the following is an injection?', 'Spending by foreign tourists in the country', 'Export of services.', ['Spending on imported cars', 'Income tax paid', 'Money saved in banks']),
    ('Which of the following is a leakage?', 'Spending on foreign holidays', 'Import of services.', ['Investment by firms', 'Government spending on roads', 'Exports of tea']),
    ('Why is consumption of domestic output not an injection?', 'It is part of the existing circular flow of income', 'Induced spending from income.', ['It is a leakage', 'It is paid by foreigners', 'It is not counted in GDP']),
])
ex(t16_2, [
    ('Explain the difference between an injection and a leakage.', 'An injection is spending that enters the circular flow from outside household consumption (I, G, X); a leakage is income that is not passed on as spending on domestic output (S, T, M).', '1 mark each [2]'),
    ('Explain why imports are a leakage from the circular flow.', 'Spending on imports goes to foreign producers, so it does not become income for domestic factors of production.', '1 mark: spending leaves country; 1 mark: not domestic income [2]'),
])
classify(t16_2, FLOW_CASES, ['Injection', 'Leakage (withdrawal)'], 'Is this an injection into or a leakage from the circular flow?', 'For each, state whether it is an injection or a leakage and explain.', extra=['Neither: a transfer within the flow', 'A real flow of goods'], name='flows')
items(t16_2, 'C2', (1, 2, 3, 4), [
    ('Households in {country} become worried about job security and save more. Explain the effect on the circular flow.', 'Saving is a leakage; higher saving reduces consumption of domestic output, so incomes and output fall unless injections rise.', '1 mark: leakage rises; 1 mark: income falls [2]'),
])
errs(t16_2, [
    ('Exports are a leakage because goods leave the country.', 'Exports are an injection: foreign spending on domestic output adds income to the circular flow.'),
])


@t16_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t16_2_jw(r, D):
    c = r.choice(COUNTRIES)
    I, G, X = r.choice([80, 100, 120]), r.choice([150, 180, 200]), r.choice([120, 150, 180])
    S, T_, M = r.choice([90, 110, 130]), r.choice([160, 180, 210]), r.choice([110, 140, 170])
    J, W = I + G + X, S + T_ + M
    tab = table(['Item ($ billion)', 'Value'], [('Investment', I), ('Saving', S), ('Government spending', G), ('Taxation', T_), ('Exports', X), ('Imports', M)])
    stem = f'Data for {c}: {tab}.'
    if J == W:
        res = 'stay the same'
    else:
        res = 'rise' if J > W else 'fall'
    if D <= 2:
        opts, a = mcq(r, f'National income will {res}', [f'National income will {x}' for x in ('rise', 'fall', 'stay the same', 'become zero') if x != res])
        return {'stem': stem + ' What will happen to national income?', 'options': opts, 'answer': a, 'key': f'Injections {J} vs leakages {W}: income will {res}.'}
    return {'stem': stem + ' (a) Calculate total injections and total leakages. (b) Explain what will happen to national income.',
            'answer': f'(a) Injections ${J}bn; leakages ${W}bn. (b) National income will {res}: ' + ('more is added to the flow than withdrawn, so output and income rise until leakages equal injections.' if J > W else 'more is withdrawn than added, so income falls until leakages equal injections.' if J < W else 'the flow is in equilibrium.'),
            'key': '(a) both totals [2] (b) direction [1]; explanation [1] [4]', 'marks': 4, 'type': 'numerical'}


t16_3 = T('Effects of changes in injections and leakages on national income', 'effects of changes in injections and leakages', 'national income')
mc(t16_3, [
    ('If injections are greater than leakages, national income will', 'rise', 'Net addition to spending.', ['fall', 'stay the same', 'become negative']),
    ('A fall in exports, other things equal, will', 'reduce national income', 'Injection falls.', ['increase national income', 'have no effect', 'increase saving']),
    ('An increase in the rate of income tax, other things equal, will', 'reduce national income', 'Leakage rises.', ['increase national income', 'increase exports', 'increase investment']),
    ('National income is in equilibrium when', 'total injections equal total leakages', 'J = W.', ['saving equals consumption', 'exports equal government spending', 'taxes equal zero']),
])
ex(t16_3, [
    ('Explain why an increase in investment can lead to a larger increase in national income.', 'Investment spending becomes income for workers and firms, who spend part of it, creating further income in successive rounds until leakages rise to match the new injection.', '1 mark: spending becomes income; 1 mark: successive rounds [2]'),
    ('Explain how a recession in a major trading partner affects national income.', 'Demand for exports falls, reducing injections; incomes and spending fall in the domestic economy.', '1 mark: exports fall; 1 mark: income falls [2]'),
])
items(t16_3, 'C2', (1, 2, 3, 4), [
    ('The government of {country} increases spending on roads while leaving taxes unchanged. Explain the effect on national income.', 'Government spending is an injection; with leakages unchanged initially, J > W, so income rises, raising leakages until a new equilibrium.', '1 mark: injection rises; 1 mark: income rises to new equilibrium [2]'),
    ('Consumers in {country} start buying more imported goods instead of local products. Explain the effect on national income.', 'Imports are a leakage; higher imports reduce spending on domestic output, so national income falls.', '1 mark: leakage rises; 1 mark: income falls [2]'),
])
errs(t16_3, [
    ('Higher saving always increases national income because banks lend it to firms.', 'Saving is a leakage; national income rises only if the saving is matched by higher injections such as investment.'),
])
CHG_CASES = [
    ('Firms in {country} increase investment in new factories.', 'National income rises', 'investment is an injection.'),
    ('The government of {country} raises income tax rates.', 'National income falls', 'taxation is a leakage.'),
    ('Exports from {country} fall because of a global recession.', 'National income falls', 'exports are an injection.'),
    ('Households in {country} save a smaller proportion of income.', 'National income rises', 'saving is a leakage.'),
    ('Consumers in {country} spend more on imported goods.', 'National income falls', 'imports are a leakage.'),
    ('The government of {country} increases spending on hospitals.', 'National income rises', 'government spending is an injection.'),
]
classify(t16_3, CHG_CASES, ['National income rises', 'National income falls'], 'What is the likely effect on national income, other things equal?', 'For each change, state the likely effect on national income and explain.', extra=['National income is unchanged', 'Only the price level changes'], name='jw')


@t16_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t16_3_chg(r, D):
    c = r.choice(COUNTRIES)
    Y = r.choice([600, 800, 1000])
    w = r.choice([0.25, 0.4, 0.5])
    dI = r.choice([20, 30, 40, 50])
    dY = dI / w
    stem = f'In {c}, national income is ${Y} billion and in equilibrium. For every extra $1 of income, {num(w * 100)} cents leaks out as saving, taxes and imports. Investment rises by ${dI} billion.'
    if D <= 2:
        return cq(r, 2, stem + ' By how much must national income rise for leakages to increase by the same amount as the injection?', f'${num(dY)} billion', f'ΔW = {w} × ΔY = {dI} → ΔY = {num(dY)}.', dis_num(r, dY, lambda v: f'${num(v)} billion', [dI, dI * w]), mcq_D=(1, 2, 3))
    return {'stem': stem + ' (a) Calculate the rise in national income needed for leakages to rise by the same amount as the injection, and the new level of national income. (b) Explain why the rise in income is larger than the rise in investment.',
            'answer': f'(a) ΔY = ${num(dY)}bn; new Y = ${num(Y + dY)}bn. (b) The extra spending becomes income that is partly re-spent in successive rounds; income keeps rising until the extra leakages ({num(w)} of each extra dollar) equal the extra injection.',
            'key': f'(a) {dI}/{w} [1]; new income [1] (b) successive rounds of spending [1]; stops when ΔW = ΔJ [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch16_case(r, D):
    d = ctx(r)
    x0, x1 = r.choice([(240, 200), (300, 255), (180, 150)])
    g = r.choice([20, 30, 40])
    intro = (f'Extract: Exports from {d["country"]} fell from ${x0} billion to ${x1} billion as its main trading partner entered a recession. Households, worried about jobs, increased saving. '
             f'The government responded by raising its spending by ${g} billion, funded by borrowing, and kept tax rates unchanged.')
    parts = [
        lambda r: ('Calculate the percentage fall in exports.', pct(-chg(x0, x1)), '[1]'),
        lambda r: ('Identify the injections and leakages mentioned in the extract.', 'Injections: exports, government spending; leakage: saving.', '[2]'),
        lambda r: ('Explain the effect of the fall in exports and rise in saving on national income.', 'Injection falls and leakage rises: W > J, so income falls.', '[3]'),
        lambda r: ('Explain whether the extra government spending is enough to offset the fall in exports.', f'Exports fell by ${x0 - x1}bn vs extra G ${g}bn: ' + ('not enough' if g < x0 - x1 else 'enough to offset exports') + '; and saving also rose.', '[2]'),
        lambda r: ('Discuss how effective higher government spending is likely to be in stopping national income from falling.', 'Injection offsets fall; but saving may rise further, imports leak, confidence matters, borrowing has costs, time lags; judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t16_1, t16_2, t16_3], _ch16_case)
essay(t16_1, [
    ('Explain the circular flow of income in an open economy with a government sector.',
     'Households and firms; real and money flows; leakages S, T, M; injections I, G, X; equilibrium J = W; diagram.',
     'the circular flow model is useful for explaining changes in national income in {country}',
     'Shows how spending becomes income; effect of injections and leakages; basis for policy.',
     'Simplistic: ignores prices, supply constraints, time lags and confidence; injections and leakages interdependent; useful starting point.'),
])
essay(t16_2, [
    ('Explain the injections into and leakages from the circular flow of income.',
     'I, G, X as injections; S, T, M as leakages; why each adds or withdraws; examples.',
     'an increase in saving is harmful to an economy',
     'Leakage reduces spending and income; paradox of thrift in a recession.',
     'Saving funds investment, raising long-run growth; reduces inflationary pressure; depends on whether banks lend it and the state of the economy.'),
])
essay(t16_3, [
    ('Explain how changes in injections and leakages affect the level of national income.',
     'J > W → income rises; W > J → income falls; adjustment until equal; successive rounds of spending; examples.',
     'government spending is the most reliable way to raise national income in {country}',
     'Government controls G directly; adds injection quickly.',
     'Financing may raise taxes or crowd out investment; imports leak; time lags; exports and investment matter too; depends on spare capacity.'),
])
CHAPTERS[16] = [t16_1, t16_2, t16_3]

# ============================================================================ 17 Aggregate demand and aggregate supply analysis
AD_CASES = [
    ('Consumer confidence in {country} rises sharply.', 'AD shifts right', 'consumption, a component of AD, rises at every price level.'),
    ('The central bank of {country} cuts interest rates.', 'AD shifts right', 'cheaper borrowing raises consumption and investment.'),
    ('The government of {country} cuts spending on infrastructure.', 'AD shifts left', 'government spending is a component of AD.'),
    ('A recession in {country2} reduces demand for {country}’s exports.', 'AD shifts left', 'net exports fall.'),
    ('The general price level in {country} rises.', 'Movement along the AD curve', 'a change in the price level causes a movement, not a shift.'),
    ('The currency of {country} depreciates, making its exports cheaper.', 'AD shifts right', 'net exports rise.'),
    ('The government of {country} raises income tax rates.', 'AD shifts left', 'disposable income and consumption fall.'),
    ('House prices in {country} rise strongly, making households feel wealthier.', 'AD shifts right', 'wealth effect raises consumption.'),
]
AS_CASES = [
    ('Oil prices rise sharply on world markets.', 'SRAS shifts left', 'higher costs of production for firms.'),
    ('Wages in {country} fall after a period of high unemployment.', 'SRAS shifts right', 'lower costs of production.'),
    ('The government of {country} invests heavily in education and training.', 'LRAS shifts right', 'the quality of labour and productive capacity rise.'),
    ('A new technology raises productivity across {country}’s factories.', 'LRAS shifts right', 'productive capacity increases.'),
    ('A natural disaster destroys much of {country}’s infrastructure.', 'LRAS shifts left', 'productive capacity falls.'),
    ('The government of {country} raises indirect taxes on fuel used by firms.', 'SRAS shifts left', 'higher costs of production.'),
    ('Large numbers of skilled workers migrate into {country}.', 'LRAS shifts right', 'the quantity of labour rises.'),
    ('The currency of {country} appreciates, making imported raw materials cheaper.', 'SRAS shifts right', 'lower import costs.'),
]

t17_1 = T('Components of aggregate demand and the shape of the AD curve', 'components of aggregate demand', 'shape of the ad curve', 'aggregate demand')
mc(t17_1, [
    ('What is aggregate demand?', 'Total planned spending on an economy’s goods and services at each price level', 'AD = C + I + G + (X − M).', ['Total spending by consumers only', 'Total output of the economy', 'Total demand for imports']),
    ('Which is the formula for aggregate demand?', 'C + I + G + (X − M)', 'Components.', ['C + S + T', 'C + I + G + X + M', 'S + T + M']),
    ('Which is usually the largest component of aggregate demand?', 'Consumption', 'Typically 50–70% of AD.', ['Investment', 'Government spending', 'Net exports']),
    ('Why does the AD curve slope downwards?', 'A higher price level reduces real wealth, raises interest rates and makes exports less competitive', 'Wealth, interest rate and trade effects.', ['Firms supply more at higher prices', 'Costs rise with output', 'Government spending falls at lower prices']),
    ('What do the axes of an AD/AS diagram show?', 'The price level and real national output', 'Vertical: price level; horizontal: real GDP.', ['Price and quantity of one good', 'Wages and employment', 'Interest rate and investment']),
])
ex(t17_1, [
    ('Explain why the AD curve slopes downwards from left to right.', 'At a higher price level: real wealth falls so consumption falls; demand for money rises, raising interest rates and reducing borrowing; exports become less competitive and imports more attractive, so net exports fall.', '1 mark each effect explained (max 3) [3]'),
    ('Explain the difference between consumption and investment as components of aggregate demand.', 'Consumption is household spending on goods and services for current use; investment is firms’ spending on capital goods to produce in future.', '1 mark each [2]'),
])
items(t17_1, 'C2', (1, 2, 3, 4), [
    ('In {country}, consumption is $600bn, investment $150bn, government spending $200bn, exports $250bn and imports $300bn. Explain why net exports reduce aggregate demand in {country}.', 'Net exports are X − M = −$50bn: spending on imports exceeds foreign spending on exports, so this component subtracts from AD.', '1 mark: X − M negative; 1 mark: reduces AD [2]'),
])
errs(t17_1, [
    ('Imports are added to aggregate demand because they are part of what consumers buy.', 'Imports are subtracted (X − M) because spending on them goes to foreign producers, not domestic output.'),
    ('The AD curve slopes downwards for the same reason as a demand curve for a single good.', 'A single good’s demand curve relies on substitution between goods; the AD curve reflects wealth, interest rate and international trade effects of a change in the general price level.'),
])


@t17_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t17_1_ad(r, D):
    c = r.choice(COUNTRIES)
    C_, I, G, X, M = r.choice([500, 600, 700]), r.choice([100, 120, 150]), r.choice([150, 200, 250]), r.choice([200, 250, 300]), r.choice([220, 280, 320])
    AD = C_ + I + G + X - M
    stem = f'In {c}: consumption ${C_}bn, investment ${I}bn, government spending ${G}bn, exports ${X}bn and imports ${M}bn.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate aggregate demand.', f'${AD}bn', f'{C_} + {I} + {G} + ({X} − {M}) = {AD}.', [f'${x}bn' for x in (AD + 2 * M, C_ + I + G, AD + M, AD - X)], mcq_D=(1, 2))
    dI = r.choice([-30, -20, 20, 30])
    return {'stem': stem + f' (a) Calculate aggregate demand and the share of consumption in it. (b) Investment {"rises" if dI > 0 else "falls"} by ${abs(dI)}bn. Calculate the new AD and explain how the AD curve is affected.',
            'answer': f'(a) AD = ${AD}bn; consumption share {pct(100 * C_ / AD)}. (b) ${AD + dI}bn; the AD curve shifts {"right" if dI > 0 else "left"} because spending changes at every price level.',
            'key': '(a) AD [1]; share [1] (b) new AD [1]; shift direction and reason [1] [4]', 'marks': 4, 'type': 'numerical'}


t17_2 = T('Causes of shifts in aggregate demand', 'causes of shifts in aggregate demand', 'shifts in aggregate demand')
mc(t17_2, [
    ('Which would shift the AD curve to the right?', 'A cut in interest rates', 'Higher C and I.', ['A rise in income tax', 'A fall in exports', 'A rise in the price level']),
    ('Which would shift the AD curve to the left?', 'A fall in business confidence', 'Lower investment.', ['A rise in government spending', 'A depreciation of the currency', 'A cut in income tax']),
    ('A rise in the general price level causes', 'a movement up along the AD curve', 'Not a shift.', ['a shift of AD to the right', 'a shift of AD to the left', 'a shift of LRAS']),
    ('An appreciation of a country’s currency is likely to', 'shift AD to the left by reducing net exports', 'Exports dearer, imports cheaper.', ['shift AD to the right', 'have no effect on AD', 'shift LRAS to the right']),
])
ex(t17_2, [
    ('Explain two factors that could cause aggregate demand to increase.', 'Lower interest rates (C and I rise); higher consumer/business confidence; expansionary fiscal policy (higher G, lower taxes); currency depreciation (net exports); higher incomes abroad; wealth effects.', '1 mark each factor, 1 mark each explained [4]'),
])
classify(t17_2, AD_CASES, ['AD shifts right', 'AD shifts left', 'Movement along the AD curve'], 'What is the effect on the aggregate demand curve?', 'For each event, state the effect on AD and explain.', extra=['LRAS shifts right'], name='ad')
items(t17_2, 'C2', (1, 2, 3, 4), [
    ('Unemployment in {country} is rising and households fear for their jobs. Explain the likely effect on aggregate demand.', 'Lower confidence reduces consumption and raises precautionary saving; firms invest less; AD shifts left.', '1 mark: C/I fall; 1 mark: AD left [2]'),
])
errs(t17_2, [
    ('A rise in the price level shifts the AD curve to the left.', 'A change in the price level causes a movement along the AD curve, not a shift.'),
])


@t17_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t17_2_comp(r, D):
    c = r.choice(COUNTRIES)
    C0, I0, G0, X0, M0 = 600, r.choice([120, 150]), 200, r.choice([250, 300]), r.choice([260, 280])
    dC, dI, dX, dM = r.choice([-20, 10, 20]), r.choice([-30, -15, 15]), r.choice([-40, -20, 20]), r.choice([-10, 10, 20])
    AD0 = C0 + I0 + G0 + X0 - M0
    AD1 = AD0 + dC + dI + dX - dM
    stem = (f'In {c}, aggregate demand was ${AD0}bn. Over the year consumption changed by {sgn(dC, 0)}bn, investment by {sgn(dI, 0)}bn, exports by {sgn(dX, 0)}bn and imports by {sgn(dM, 0)}bn; government spending was unchanged.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the new level of aggregate demand.', f'${AD1}bn', f'{AD0} + ({dC}) + ({dI}) + ({dX}) − ({dM}) = {AD1}.', dis_num(r, AD1, lambda v: f'${num(v)}bn', [AD0 + dC + dI + dX + dM, AD1 + 2 * dM, AD0]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the new AD and the percentage change. (b) State and explain the direction of the shift in the AD curve and suggest one possible cause of the change in investment.',
            'answer': f'(a) ${AD1}bn; {pchg(chg(AD0, AD1))}. (b) AD shifts {"right" if AD1 > AD0 else "left" if AD1 < AD0 else "neither way"}; investment change could reflect a change in interest rates or business confidence.',
            'key': '(a) [2] (b) direction [1]; cause [1] [4]', 'marks': 4, 'type': 'numerical'}


t17_3 = T('Short-run and long-run aggregate supply: shapes and shifts', 'short-run and long-run aggregate supply', 'shapes and shifts', 'aggregate supply')
mc(t17_3, [
    ('What is aggregate supply?', 'The total output that producers in an economy are willing and able to supply at each price level', 'AS: total planned output.', ['Total spending in an economy', 'The supply of money', 'The output of one industry']),
    ('Why does the SRAS curve slope upwards?', 'In the short run some costs such as wages are fixed, so higher prices raise profits and output', 'Sticky costs.', ['Because consumers spend more at higher prices', 'Because productivity falls', 'Because government spending rises']),
    ('In the classical view the LRAS curve is', 'vertical at the full-employment level of output', 'Output determined by capacity.', ['horizontal', 'downward sloping', 'upward sloping throughout']),
    ('A rise in the price of imported raw materials would shift', 'SRAS to the left', 'Higher costs.', ['LRAS to the right', 'AD to the right', 'SRAS to the right']),
    ('Which would shift LRAS to the right?', 'An improvement in the quality of education', 'Productive capacity rises.', ['A rise in wages', 'A cut in interest rates', 'An increase in government spending on pensions']),
    ('In the Keynesian AS curve, what does the horizontal section show?', 'Output can rise without raising the price level because there is spare capacity', 'Unemployed resources.', ['Full employment', 'Hyperinflation', 'A fall in productivity']),
])
ex(t17_3, [
    ('Explain the difference between a shift in SRAS and a shift in LRAS.', 'SRAS shifts with changes in costs of production (wages, raw materials, taxes); LRAS shifts with changes in the quantity or quality of factors of production or technology, i.e. productive capacity.', '1 mark each [2]'),
    ('Explain why the Keynesian LRAS curve becomes vertical at full employment.', 'At full employment all resources are used, so output cannot rise further; extra demand only raises prices.', '1 mark: full capacity; 1 mark: only prices rise [2]'),
])
classify(t17_3, AS_CASES, ['SRAS shifts left', 'SRAS shifts right', 'LRAS shifts right', 'LRAS shifts left'], 'What is the effect on aggregate supply?', 'For each event, state the effect on aggregate supply and explain.', extra=['AD shifts right'], name='as')
items(t17_3, 'C2', (1, 2, 3, 4), [
    ('A drought raises food prices and the cost of agricultural inputs in {country}. Explain the effect on SRAS.', 'Costs of production rise for firms using these inputs, so they supply less at each price level: SRAS shifts left.', '1 mark: higher costs; 1 mark: SRAS left [2]'),
])
errs(t17_3, [
    ('An increase in wages shifts the LRAS curve to the left.', 'Higher wages raise costs and shift SRAS left; LRAS depends on productive capacity, which is unchanged.'),
])


@t17_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t17_3_prod(r, D):
    c = r.choice(COUNTRIES)
    L0, L1 = r.choice([(20, 21), (10, 10.4), (30, 31.5)])
    p0, p1 = r.choice([(40, 42), (50, 52), (25, 26)])
    y0, y1 = L0 * p0, L1 * p1
    stem = f'In {c}, the labour force grew from {num(L0, 1)} million to {num(L1, 1)} million and output per worker at full employment rose from ${p0},000 to ${p1},000.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate full-employment output after the change, in billions of dollars.', f'${num(y1, 1)}bn', f'{num(L1, 1)}m × ${p1},000 = {num(y1, 1)}bn.', dis_num(r, y1, lambda v: f'${num(v, 1)}bn', [y0, L1 * p0]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate potential output before and after, and the percentage increase. (b) Explain the effect on the LRAS curve and on the economy’s productive capacity.',
            'answer': f'(a) ${num(y0, 1)}bn → ${num(y1, 1)}bn: {pchg(chg(y0, y1))}. (b) LRAS shifts right: more and more productive labour raises full-employment output.',
            'key': '(a) both values [1]; % change [1] (b) LRAS shift [1]; reason [1] [4]', 'marks': 4, 'type': 'numerical'}


EQ_CASES = [
    ('AD shifts right when the economy has a lot of spare capacity.', 'Real output rises with little change in the price level', 'on the flat part of AS, idle resources are used.'),
    ('AD shifts right when the economy is close to full employment.', 'The price level rises with little change in real output', 'capacity constraints; AS is steep/vertical.'),
    ('SRAS shifts left because of higher oil prices.', 'Price level rises and real output falls', 'cost-push inflation and lower output (stagflation).'),
    ('LRAS shifts right with no change in AD.', 'Price level falls and real output rises', 'higher capacity at each price level.'),
    ('AD shifts left in a recession.', 'Real output falls and the price level falls or rises more slowly', 'lower spending reduces output and prices.'),
]

t17_4 = T('Macroeconomic equilibrium and the effects of AD and AS shifts on real output and the price level', 'macroeconomic equilibrium', 'effects of ad and as shifts', 'real output and the price level')
mc(t17_4, [
    ('Where is macroeconomic equilibrium?', 'Where aggregate demand equals aggregate supply', 'AD = AS.', ['Where exports equal imports', 'Where the budget is balanced', 'Where saving equals consumption']),
    ('An increase in AD when the economy is at full employment will mainly cause', 'a rise in the price level', 'Vertical LRAS.', ['a rise in real output', 'a fall in the price level', 'a fall in unemployment']),
    ('A leftward shift of SRAS will cause', 'a higher price level and lower real output', 'Stagflation.', ['a lower price level and higher output', 'higher output and a higher price level', 'no change in the price level']),
    ('An outward shift of LRAS with constant AD will cause', 'higher real output and a lower price level', 'More capacity.', ['lower output and a higher price level', 'no change in output', 'higher prices only']),
    ('An increase in AD when there is a large amount of spare capacity will mainly cause', 'a rise in real output', 'Flat AS section.', ['a rise in the price level only', 'a fall in output', 'a fall in employment']),
])
ex(t17_4, [
    ('Explain, with the help of an AD/AS diagram, why the effect of an increase in AD depends on the level of spare capacity.', 'With spare capacity (flat AS), output rises with little inflation; near full employment (steep AS), output rises little and the price level rises a lot.', '1 mark: spare capacity case; 1 mark: near-capacity case; 1 mark: diagram reference [3]'),
    ('Explain how a supply shock such as a sharp rise in oil prices affects real output and the price level.', 'Higher costs shift SRAS left; the price level rises and real output falls; unemployment may rise (stagflation).', '1 mark: SRAS left; 1 mark: P up, Y down [2]'),
])
classify(t17_4, EQ_CASES, ['Real output rises with little change in the price level', 'The price level rises with little change in real output', 'Price level rises and real output falls', 'Price level falls and real output rises', 'Real output falls and the price level falls or rises more slowly'],
         'What is the likely outcome in an AD/AS model?', 'For each change, state the likely effect on real output and the price level and explain.', name='adas')
items(t17_4, 'C2', (1, 2, 3, 4), [
    ('The government of {country} increases spending while unemployment is at a record low. Explain the likely effect on the price level and real output.', 'With little spare capacity, AD rises along a steep AS curve: the price level rises substantially, real output only a little (demand-pull inflation).', '1 mark: little spare capacity; 1 mark: mainly inflation [2]'),
])
errs(t17_4, [
    ('An increase in aggregate demand always increases real output by the same amount.', 'The effect on output depends on spare capacity; near full employment most of the effect is on the price level.'),
])


@t17_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t17_4_lin(r, D):
    # AD: P = a − bY ; SRAS: P = c + dY (simple linear model)
    for _ in range(40):
        Y = r.choice([400, 500, 600, 800])
        P = r.choice([100, 110, 120])
        b = r.choice([0.1, 0.2, 0.25])
        d = r.choice([0.05, 0.1, 0.2])
        a = P + b * Y
        c = P - d * Y
        if c > 0:
            break
    k = r.choice([10, 20, 30])
    Y1 = (a + k - c) / (b + d)
    P1 = c + d * Y1
    stem = f'In a simple model of {r.choice(COUNTRIES)}, AD is P = {num(a)} − {num(b, 2)}Y and SRAS is P = {num(c)} + {num(d, 2)}Y, where P is the price level and Y real output ($ billion).'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate equilibrium real output.', f'${num(Y)}bn', f'{num(a)} − {num(b, 2)}Y = {num(c)} + {num(d, 2)}Y → Y = {num(a - c)}/{num(b + d, 2)} = {num(Y)}.', dis_num(r, Y, lambda v: f'${num(v)}bn', [a / b, (a + c) / (b + d)]), mcq_D=(1, 2))
    return {'stem': stem + f' (a) Calculate the equilibrium price level and real output. (b) AD increases so that the AD equation becomes P = {num(a + k)} − {num(b, 2)}Y. Calculate the new equilibrium and the percentage changes in P and Y. (c) Explain what the result shows about the slope of SRAS.',
            'answer': f'(a) P = {num(P)}, Y = ${num(Y)}bn. (b) P = {num(P1, 1)}, Y = ${num(Y1, 1)}bn: P {pchg(chg(P, P1))}, Y {pchg(chg(Y, Y1))}. (c) Both rise; the steeper the SRAS, the more of the AD increase goes into prices rather than output.',
            'key': '(a) [2] (b) new equilibrium [1]; % changes [1] (c) slope interpretation [1] [5]', 'marks': 5, 'type': 'multi_step'}


def _ch17_case(r, D):
    d = ctx(r)
    oil = r.choice([40, 50, 60])
    g = r.choice([2.5, 3, 3.5])
    g1 = r.choice([0.5, 1, 1.5])
    i0, i1 = r.choice([(2, 6), (3, 7), (2.5, 6.5)])
    intro = (f'Extract: In {d["country"]}, world oil prices rose by {oil}% this year. Inflation rose from {i0}% to {i1}% while real GDP growth slowed from {g}% to {g1}%. '
             f'At the same time, the government has announced a large programme of training and infrastructure investment, and consumer confidence has fallen.')
    parts = [
        lambda r: ('Calculate the change in the inflation rate in percentage points.', f'{num(i1 - i0, 1)} percentage points', '[1]'),
        lambda r: ('Using an AD/AS diagram, explain how the rise in oil prices could cause both higher inflation and slower growth.', 'SRAS shifts left: higher price level and lower real output.', '[3]'),
        lambda r: ('Explain the likely effect of the fall in consumer confidence on aggregate demand.', 'Consumption falls; AD shifts left; lower output, less inflationary pressure.', '[2]'),
        lambda r: ('Explain how the training and infrastructure programme could affect both AD and LRAS.', 'G raises AD in the short run; better skills and infrastructure shift LRAS right in the long run.', '[3]'),
        lambda r: ('Discuss whether the government’s programme will reduce inflation in the long run.', 'LRAS shift lowers price pressure, but AD boost now may add to inflation; time lags; size of programme vs oil shock; judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t17_1, t17_2, t17_3, t17_4], _ch17_case)
essay(t17_1, [
    ('Explain the components of aggregate demand and why the AD curve slopes downwards.',
     'C, I, G, X − M; wealth effect, interest rate effect, international trade effect; diagram.',
     'consumption is the most important component of aggregate demand in {country}',
     'Largest share of AD; changes in confidence and wealth cause big swings.',
     'Investment and exports are more volatile and drive cycles; government spending key in recessions; depends on the economy’s structure.'),
])
essay(t17_2, [
    ('Explain the factors that could cause the aggregate demand curve to shift.',
     'Interest rates, confidence, fiscal policy, exchange rates, world incomes, wealth; distinguish from movements along.',
     'changes in business confidence are the main cause of fluctuations in aggregate demand',
     'Investment is volatile; expectations drive spending.',
     'Exports, government policy, interest rates and consumer confidence also matter; external shocks; depends on the economy.'),
])
essay(t17_3, [
    ('Explain the difference between short-run and long-run aggregate supply and the causes of shifts in each.',
     'SRAS: costs (wages, raw materials, taxes); LRAS: quantity/quality of factors, technology; classical vs Keynesian shapes; diagrams.',
     'increasing long-run aggregate supply is more important for {country} than increasing aggregate demand',
     'Sustainable non-inflationary growth; higher living standards; competitiveness.',
     'In a recession AD is the constraint; LRAS policies slow and costly; both needed; depends on spare capacity.'),
])
essay(t17_4, [
    ('With the help of AD/AS diagrams, explain how an increase in aggregate demand affects real output and the price level.',
     'Depends on spare capacity: Keynesian AS with flat, rising and vertical sections; classical vertical LRAS; diagrams.',
     'an increase in aggregate demand will always increase real output',
     'With spare capacity, higher AD raises output and employment.',
     'At full employment only prices rise; SRAS slope; supply constraints; long-run classical view; depends on the economy’s position.'),
])
CHAPTERS[17] = [t17_1, t17_2, t17_3, t17_4]

# ============================================================================ 18 Economic growth
t18_1 = T('Actual and potential economic growth; real GDP growth rates', 'actual and potential economic growth', 'real gdp growth rates', 'economic growth')
mc(t18_1, [
    ('What is actual economic growth?', 'An increase in real GDP', 'Measured as % change in real GDP.', ['An increase in productive capacity', 'An increase in nominal GDP', 'An increase in the price level']),
    ('What is potential economic growth?', 'An increase in the productive capacity of the economy', 'Shift of PPC/LRAS.', ['An increase in actual output', 'A rise in employment', 'A rise in exports']),
    ('If real GDP rises from $500bn to $520bn, the growth rate is', '4%', '20/500 × 100.', ['20%', '2%', '5%']),
    ('Which diagram change shows potential growth?', 'An outward shift of the PPC', 'Capacity increases.', ['A movement from inside the PPC to the PPC', 'A movement along the PPC', 'A rightward shift of AD']),
    ('Why must growth be measured using real rather than nominal GDP?', 'Nominal GDP rises with inflation even if output does not', 'Remove price changes.', ['Real GDP includes exports', 'Nominal GDP excludes services', 'Real GDP is always higher']),
])
ex(t18_1, [
    ('Explain the difference between actual and potential economic growth.', 'Actual growth is an increase in real output (using more resources or idle capacity); potential growth is an increase in productive capacity (more/better resources, technology), shown by an outward shift of the PPC or LRAS.', '1 mark each [2]'),
    ('Explain why actual growth cannot exceed potential growth for long.', 'Once spare capacity is used up, output can only rise as fast as capacity grows; trying to grow faster causes inflation.', '1 mark: capacity limit; 1 mark: inflation [2]'),
])
items(t18_1, 'C2', (1, 2, 3, 4), [
    ('Real GDP in {country} grew by 6% last year while unemployment fell sharply. Explain whether this was mainly actual or potential growth.', 'Mainly actual growth: idle resources (unemployed workers) were brought into use, moving towards the PPC.', '1 mark: actual; 1 mark: idle resources used [2]'),
])
errs(t18_1, [
    ('If nominal GDP rises by 5%, the economy has grown by 5%.', 'Growth is measured by the change in real GDP; nominal GDP includes the effect of inflation.'),
])


@t18_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t18_1_growth(r, D):
    c = r.choice(COUNTRIES)
    ys = [r.choice([400, 500, 600])]
    for _ in range(3):
        ys.append(round(ys[-1] * (1 + r.choice([-0.01, 0.01, 0.02, 0.03, 0.04, 0.05])), 1))
    tab = table(['Year', 'Real GDP ($ billion)'], list(zip([1, 2, 3, 4], ys)))
    i = r.randint(1, 3)
    g = chg(ys[i - 1], ys[i])
    stem = f'{c}: {tab}.'
    if D <= 2:
        return cq(r, 1, stem + f' Calculate the growth rate of real GDP in Year {i + 1}.', pchg(g), f'({ys[i]} − {ys[i - 1]})/{ys[i - 1]} × 100.', dis_num(r, g, pchg, [g * 2, -g, chg(ys[0], ys[i])]), mcq_D=(1, 2))
    gs = [chg(ys[k - 1], ys[k]) for k in (1, 2, 3)]
    tot = chg(ys[0], ys[3])
    return {'stem': stem + ' (a) Calculate the growth rate in each of Years 2 to 4 and over the whole period. (b) Comment on the performance of the economy.',
            'answer': f'(a) {", ".join(pchg(x) for x in gs)}; overall {pchg(tot)}. (b) ' + ('Output fell in at least one year, suggesting a slowdown or recession; ' if min(gs) < 0 else 'Positive growth throughout; ') + 'growth was uneven, and per capita and distribution data would be needed to judge living standards.',
            'key': '(a) three annual rates [2]; overall [1] (b) comment using data [1] [4]', 'marks': 4, 'type': 'numerical'}


t18_2 = T('Causes of economic growth', 'causes of economic growth')
mc(t18_2, [
    ('Which is a cause of long-run economic growth?', 'Investment in new capital and technology', 'Increases productive capacity.', ['A rise in the price level', 'A rise in imports', 'A rise in unemployment']),
    ('How does education contribute to economic growth?', 'It raises the quality of labour and its productivity', 'Human capital.', ['It reduces the labour force', 'It increases imports', 'It raises interest rates']),
    ('Which factor causes actual growth in the short run?', 'An increase in aggregate demand when there is spare capacity', 'AD-led growth.', ['A rise in productivity only', 'A fall in the labour force', 'A natural disaster']),
    ('Why does investment have a double effect on growth?', 'It adds to AD now and increases productive capacity later', 'Short and long run.', ['It lowers both AD and AS', 'It raises imports only', 'It reduces saving']),
])
ex(t18_2, [
    ('Explain two causes of potential economic growth.', 'More capital (investment); better technology; more labour (population, migration, participation); better quality labour (education, health); discovery of resources; better institutions.', '1 mark each cause, 1 mark each explained [4]'),
    ('Explain how an increase in investment can lead to both actual and potential growth.', 'Investment spending raises AD now (actual growth if there is spare capacity) and adds to the capital stock, raising LRAS (potential growth).', '1 mark: AD; 1 mark: LRAS [2]'),
])
GR_CASES = [
    ('Households in {country} increase spending after a tax cut while unemployment is high.', 'Actual growth (AD-led)', 'spare capacity is used as AD rises.'),
    ('The government of {country} doubles spending on universities and vocational training.', 'Potential growth (supply-side)', 'better human capital raises productive capacity.'),
    ('Firms in {country} invest in automated production lines.', 'Both actual and potential growth', 'investment raises AD now and capacity later.'),
    ('A new port in {city} cuts transport costs for exporters.', 'Potential growth (supply-side)', 'infrastructure raises productivity.'),
    ('Exports from {country} rise strongly as world demand recovers.', 'Actual growth (AD-led)', 'net exports raise AD.'),
    ('Migration raises the size of {country}’s labour force.', 'Potential growth (supply-side)', 'more labour raises capacity.'),
]
classify(t18_2, GR_CASES, ['Actual growth (AD-led)', 'Potential growth (supply-side)', 'Both actual and potential growth'], 'What type of growth does this mainly cause?', 'For each, identify the type of growth and explain.', extra=['Neither: it causes inflation only'], name='growth')
items(t18_2, 'C2', (1, 2, 3, 4), [
    ('{country} has discovered large offshore gas reserves. Explain how this could cause economic growth.', 'More natural resources raise productive capacity (LRAS/PPC shifts out); investment and exports increase AD.', '1 mark: capacity; 1 mark: AD [2]'),
])
errs(t18_2, [
    ('An increase in aggregate demand always causes long-run economic growth.', 'Higher AD can cause actual growth if there is spare capacity; long-run growth requires an increase in productive capacity.'),
])


@t18_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t18_2_prod(r, D):
    c = r.choice(COUNTRIES)
    L0, L1 = r.choice([(10, 10.2), (20, 20.6), (5, 5.1)])
    o0 = r.choice([300, 600, 900]) if L0 >= 10 else 150
    pg = r.choice([1, 2, 3])
    pr0 = o0 / L0
    pr1 = pr0 * (1 + pg / 100)
    o1 = pr1 * L1
    stem = f'In {c}, the employed labour force rose from {num(L0, 1)} million to {num(L1, 1)} million and output per worker rose by {pg}%. Real GDP was ${o0}bn at the start.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the new level of real GDP.', f'${num(o1, 1)}bn', f'Output per worker {num(pr0, 1)}k × {1 + pg / 100} × {num(L1, 1)}m.', dis_num(r, o1, lambda v: f'${num(v, 1)}bn', [o0 * (1 + pg / 100), o0 * L1 / L0]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the new real GDP and the growth rate. (b) Calculate how much of the growth was due to more workers and how much to higher productivity (approximately). (c) Explain why productivity growth is more important for living standards.',
            'answer': f'(a) ${num(o1, 1)}bn; {pchg(chg(o0, o1))}. (b) Labour ≈ {pchg(chg(L0, L1))}; productivity {pg}%. (c) Only productivity growth raises output per worker (and per head); more workers raise total output but not necessarily income per person.',
            'key': '(a) [2] (b) both components [1] (c) per worker/per capita reasoning [1] [4]', 'marks': 4, 'type': 'numerical'}


t18_3 = T('Recession, the economic cycle and output gaps', 'recession', 'economic cycle', 'output gaps')
mc(t18_3, [
    ('What is a common definition of a recession?', 'Two consecutive quarters of falling real GDP', 'Negative growth for two quarters.', ['A fall in the price level', 'A rise in unemployment for one month', 'A fall in nominal GDP']),
    ('What is a negative output gap?', 'Actual output below potential output', 'Spare capacity, unemployment.', ['Actual output above potential', 'A trade deficit', 'A budget deficit']),
    ('Which phase of the economic cycle has the highest rate of growth and inflationary pressure?', 'Boom', 'Output above trend; capacity constraints.', ['Recession', 'Slump', 'Recovery']),
    ('A positive output gap is most likely to lead to', 'rising inflation', 'Demand exceeds capacity.', ['rising unemployment', 'falling prices', 'a fall in output']),
    ('Which is a feature of a recession?', 'Rising unemployment and falling business investment', 'Lower AD and output.', ['Rising inflation and labour shortages', 'Rising imports and confidence', 'Rising tax revenue']),
])
ex(t18_3, [
    ('Explain the difference between a positive and a negative output gap.', 'Positive: actual output above potential (resources over-used, inflationary pressure). Negative: actual below potential (spare capacity, unemployment, low inflation).', '1 mark each [2]'),
    ('Explain the main phases of the economic cycle.', 'Recovery (growth resumes), boom (rapid growth, inflation, positive gap), slowdown/downturn, recession (falling output, unemployment, negative gap).', '1 mark per two phases correctly described [3]'),
])
items(t18_3, 'C2', (1, 2, 3, 4), [
    ('Real GDP in {country} fell by 0.4% and then by 0.7% in successive quarters. Explain whether {country} is in recession and one likely consequence.', 'Yes: two consecutive quarters of negative growth; consequences include rising unemployment, falling investment and tax revenue.', '1 mark: recession; 1 mark: consequence [2]'),
])
errs(t18_3, [
    ('A negative output gap means that the economy is growing too fast.', 'A negative output gap means actual output is below potential: spare capacity and unemployment.'),
])


@t18_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t18_3_gap(r, D):
    c = r.choice(COUNTRIES)
    qs = [round(r.uniform(-1.2, 1.5), 1) for _ in range(6)]
    if r.random() < 0.5:
        k = r.randint(1, 4)
        qs[k], qs[k + 1] = -abs(qs[k]) - 0.2, -abs(qs[k + 1]) - 0.1
    rec = [i for i in range(5) if qs[i] < 0 and qs[i + 1] < 0]
    tab = table(['Quarter', 'Growth of real GDP (%)'], list(zip(range(1, 7), qs)))
    pot = r.choice([500, 800, 1000])
    act = pot * (1 + r.choice([-4, -3, -2, 2, 3]) / 100)
    gap = 100 * (act - pot) / pot
    stem = f'{c}: {tab}.'
    if D <= 2:
        ans = f'Quarters {rec[0] + 1} and {rec[0] + 2}' if rec else 'There was no recession'
        opts = [ans] + [x for x in ['There was no recession', 'Quarters 1 and 2', 'Quarters 3 and 4', 'Quarters 5 and 6', 'Quarters 2 and 3'] if x != ans]
        o, a = mcq(r, ans, opts[1:])
        return {'stem': stem + ' Using the definition of two consecutive quarters of negative growth, when was the economy in recession?', 'options': o, 'answer': a, 'key': f'Negative quarters: {[i + 1 for i, x in enumerate(qs) if x < 0]}; consecutive pair → {ans}.'}
    return {'stem': stem + f' Potential output is ${pot}bn and actual output is ${num(act)}bn. (a) Identify whether there was a recession in the data. (b) Calculate the output gap as a percentage of potential output and state whether it is positive or negative. (c) Explain one likely consequence of this output gap.',
            'answer': f'(a) ' + (f'Yes, quarters {rec[0] + 1}–{rec[0] + 2}.' if rec else 'No: there were no two consecutive quarters of negative growth.') + f' (b) {pchg(gap)} ({"positive" if gap > 0 else "negative"}). (c) ' + ('Inflationary pressure, labour shortages.' if gap > 0 else 'Unemployment and low inflation; lost output.'),
            'key': '(a) [1] (b) (actual − potential)/potential × 100 [1]; sign [1] (c) consequence [1] [4]', 'marks': 4, 'type': 'numerical'}


t18_4 = T('Costs and benefits of economic growth', 'costs and benefits of economic growth')
mc(t18_4, [
    ('Which is a benefit of economic growth?', 'Higher average living standards', 'More goods and services per head.', ['Greater pollution', 'Depletion of resources', 'More congestion']),
    ('Which is a possible cost of economic growth?', 'Environmental damage', 'Externalities; resource depletion.', ['Higher tax revenue', 'Lower unemployment', 'More choice for consumers']),
    ('How can economic growth improve government finances?', 'Tax revenues rise and spending on benefits falls', 'Fiscal dividend.', ['Spending on benefits rises', 'Tax revenues fall', 'Interest rates rise']),
    ('What is meant by sustainable growth?', 'Growth that meets present needs without compromising future generations', 'Environmental sustainability.', ['Growth of at least 5% a year', 'Growth with no inflation', 'Growth led by exports']),
])
ex(t18_4, [
    ('Explain two benefits and two costs of economic growth.', 'Benefits: higher living standards, lower unemployment, higher tax revenue for public services, reduced poverty. Costs: pollution and resource depletion, inequality, inflation if too fast, stress/longer hours.', '1 mark each [4]'),
])
items(t18_4, 'C2', (1, 2, 3, 4), [
    ('{country} has grown at 8% a year for a decade, but air pollution in {city} has worsened. Explain why growth may not have improved welfare as much as GDP suggests.', 'Pollution harms health and quality of life, a cost not measured in GDP; gains may also be unequally shared.', '1 mark: externality not in GDP; 1 mark: welfare effect [2]'),
])
errs(t18_4, [
    ('Economic growth always benefits everyone in the economy.', 'Gains may be unevenly distributed and growth can impose costs such as pollution, congestion and structural unemployment.'),
])
items(t18_4, 'C3', (1, 2, 3, 4, 5), [
    ('Real GDP per head in {country} rose by 40% over ten years, while CO₂ emissions per head rose by 60% and the income share of the richest 10% rose from 30% to 36%. Using the data, explain one benefit and two costs of this growth.',
     'Benefit: higher average incomes and consumption (40% rise in real GDP per head). Costs: environmental damage (emissions up 60%, faster than output); rising inequality (top 10% share up 6 percentage points).',
     '1 mark: benefit with data; 1 mark each cost with data [3]'),
    ('Unemployment in {country} fell from 9% to 5% during a period of rapid growth, but house prices in {city} doubled. Explain one benefit and one cost of the growth for households.',
     'Benefit: more jobs and higher incomes as unemployment fell 4 percentage points. Cost: housing became much less affordable, especially for young and low-income households.', '1 mark each with data, 1 mark development [3]'),
])


def _ch18_case(r, D):
    d = ctx(r)
    g = [r.choice([3.5, 4, 4.5]), r.choice([1.5, 2]), r.choice([-0.5, -1]), r.choice([-0.8, -0.3]), r.choice([1, 1.5])]
    gap = r.choice([-2, -3, -4])
    intro = (f'Extract: Annual growth of real GDP in {d["country"]} over five years was {g[0]}%, {g[1]}%, {g[2]}%, {g[3]}% and {g[4]}%. The output gap is now estimated at {gap}% of potential GDP. '
             f'The government plans to raise spending on infrastructure and training. Environmental groups warn that a return to rapid growth will increase pollution.')
    parts = [
        lambda r: ('Identify the phases of the economic cycle shown by the data.', 'Boom/slowdown (years 1–2), recession (years 3–4), recovery (year 5).', '[2]'),
        lambda r: ('Explain what the output gap of {}% means.'.format(gap), 'Actual output is below potential: spare capacity, unemployment, low inflationary pressure.', '[2]'),
        lambda r: ('Explain how infrastructure and training spending could lead to both actual and potential growth.', 'Raises AD now (using spare capacity) and LRAS later (productivity).', '[3]'),
        lambda r: ('Explain one cost of economic growth mentioned in the extract.', 'Pollution: negative externality, health costs, not measured in GDP.', '[2]'),
        lambda r: ('Discuss whether the benefits of a return to rapid growth would outweigh the costs.', 'Jobs, incomes, tax revenue vs pollution, inequality, inflation risk once gap closes; green growth possible; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t18_1, t18_2, t18_3, t18_4], _ch18_case)
essay(t18_1, [
    ('Explain the difference between actual and potential economic growth, using diagrams.',
     'Actual: rise in real GDP, movement towards PPC/AD shift with spare capacity; potential: capacity, PPC/LRAS shift; measurement with real GDP.',
     'actual economic growth in {country} is limited by its potential growth',
     'Once spare capacity is used, faster growth causes inflation; capacity is the constraint long-term.',
     'With a large negative output gap actual growth can exceed potential for some time; potential itself depends on demand (investment); depends on cycle position.'),
])
essay(t18_2, [
    ('Explain the causes of economic growth.',
     'AD-side (spending with spare capacity) and supply-side (capital, labour quantity and quality, technology, resources, institutions).',
     'investment in human capital is the most important cause of economic growth for {country}',
     'Productivity, innovation, adaptability; complements capital.',
     'Physical capital, technology, institutions, natural resources also vital; long time lags; brain drain; depends on stage of development.'),
])
essay(t18_3, [
    ('Explain the phases of the economic cycle and the meaning of an output gap.',
     'Recovery, boom, slowdown, recession; trend growth; positive and negative output gaps; indicators.',
     'a recession always has serious long-term consequences for {country}',
     'Hysteresis: long-term unemployment, lost skills, lower investment reduces capacity.',
     'Short, shallow recessions may have limited effects; can remove inefficient firms; policy response matters.'),
])
essay(t18_4, [
    ('Explain the potential benefits of economic growth.',
     'Higher living standards, lower unemployment, more tax revenue, reduced poverty, investment and confidence.',
     'the costs of economic growth outweigh the benefits',
     'Pollution, resource depletion, inequality, inflation, congestion.',
     'Benefits large for low-income countries; green technology and regulation can reduce costs; depends on type of growth and distribution; judgement.'),
])
CHAPTERS[18] = [t18_1, t18_2, t18_3, t18_4]

# ============================================================================ 19 Unemployment
t19_1 = T('Measuring unemployment: claimant count, labour force survey and the unemployment rate', 'measuring unemployment', 'claimant count', 'labour force survey', 'unemployment rate')
mc(t19_1, [
    ('How is the unemployment rate calculated?', 'Number unemployed ÷ labour force × 100', 'Labour force = employed + unemployed.', ['Number unemployed ÷ total population × 100', 'Number employed ÷ labour force × 100', 'Number unemployed ÷ number employed × 100']),
    ('What is the claimant count?', 'The number of people claiming unemployment-related benefits', 'Administrative measure.', ['The number of people answering a survey', 'The number of job vacancies', 'The number of people in work']),
    ('Who is counted as unemployed in the ILO labour force survey?', 'People without a job who are willing, able and actively seeking work', 'ILO definition.', ['Everyone without a job', 'Only people receiving benefits', 'Retired people and students']),
    ('Why might the claimant count understate unemployment?', 'Some unemployed people are not eligible for or do not claim benefits', 'e.g. young people, partners of earners.', ['It includes people in work', 'It counts students', 'It is based on a survey']),
    ('Which group is not part of the labour force?', 'Full-time students not seeking work', 'Economically inactive.', ['Part-time workers', 'Unemployed people seeking work', 'Self-employed workers']),
])
ex(t19_1, [
    ('Explain the difference between the claimant count and the labour force survey measures of unemployment.', 'Claimant count: number receiving unemployment benefits (cheap, frequent, but affected by benefit rules). LFS: survey using the ILO definition of those without work, available and seeking work (internationally comparable but subject to sampling error).', '1 mark each; 1 mark for a comparison [3]'),
    ('Explain why the unemployment rate may fall even if the number of jobs does not increase.', 'Discouraged workers stop searching and leave the labour force, or people retire or emigrate, so the measured number unemployed falls.', '1 mark: leaving labour force; 1 mark: reduces measured unemployment [2]'),
])
items(t19_1, 'C2', (1, 2, 3, 4), [
    ('{country} tightens the rules for unemployment benefits. Explain why the claimant count may fall even if no new jobs are created.', 'Fewer people are eligible or willing to claim, so the count falls although the same number are without work and seeking jobs.', '1 mark: eligibility; 1 mark: no change in actual unemployment [2]'),
])
errs(t19_1, [
    ('The unemployment rate is the number unemployed divided by the whole population.', 'The unemployment rate is the number unemployed as a percentage of the labour force (employed + unemployed), not the whole population.'),
])


@t19_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t19_1_rate(r, D):
    c = r.choice(COUNTRIES)
    E = r.choice([18, 20, 24, 30, 36])
    U = r.choice([1.2, 1.5, 1.8, 2.0, 2.4, 3.0])
    pop = round((E + U) / r.choice([0.6, 0.62, 0.65, 0.7]), 1)
    LF = E + U
    ur = 100 * U / LF
    stem = f'In {c}, {num(E, 1)} million people are employed and {num(U, 1)} million are unemployed. The working-age population is {num(pop, 1)} million.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the unemployment rate.', pct(ur), f'{num(U, 1)}/({num(E, 1)} + {num(U, 1)}) × 100.', dis_num(r, ur, pct, [100 * U / pop, 100 * U / E]), mcq_D=(1, 2))
    part = 100 * LF / pop
    return {'stem': stem + ' (a) Calculate the labour force, the unemployment rate and the participation rate. (b) Explain why the unemployment rate might understate the true extent of joblessness.',
            'answer': f'(a) Labour force {num(LF, 1)}m; unemployment rate {pct(ur)}; participation {pct(part)}. (b) Discouraged workers who have stopped searching are not counted; underemployment (part-time workers wanting full-time); informal work.',
            'key': '(a) labour force [1]; rate [1]; participation [1] (b) reason [1] [4]', 'marks': 4, 'type': 'numerical'}


UN_CASES = [
    ('{person} has left a job in {city} and is spending three weeks looking for a better one.', 'Frictional unemployment', 'short-term, between jobs while searching.'),
    ('Coal miners in {country} lose their jobs when the mines close and lack skills for new industries.', 'Structural unemployment', 'mismatch of skills/location after a change in the structure of the economy.'),
    ('Workers in many industries in {country} lose their jobs during a recession.', 'Cyclical (demand-deficient) unemployment', 'caused by a fall in aggregate demand.'),
    ('Ski instructors in {country} are out of work every summer.', 'Seasonal unemployment', 'demand for their labour varies with the season.'),
    ('Factory workers in {city} are replaced by robots.', 'Structural unemployment', 'technological change makes skills obsolete.'),
    ('A graduate in {city} takes two months to choose between job offers.', 'Frictional unemployment', 'searching between jobs.'),
    ('Fruit pickers in {country} are unemployed after the harvest ends.', 'Seasonal unemployment', 'work is tied to the season.'),
    ('Car sales collapse as consumer spending falls, and car workers in {country} are laid off.', 'Cyclical (demand-deficient) unemployment', 'lower AD reduces demand for labour.'),
]
UN_LABELS = ['Frictional unemployment', 'Structural unemployment', 'Cyclical (demand-deficient) unemployment', 'Seasonal unemployment']

t19_2 = T('Causes and types of unemployment: frictional, structural, cyclical and seasonal', 'causes and types of unemployment', 'frictional, structural, cyclical and seasonal', 'types of unemployment')
mc(t19_2, [
    ('What is frictional unemployment?', 'Short-term unemployment while people move between jobs', 'Search unemployment.', ['Unemployment caused by a recession', 'Unemployment caused by changes in the structure of the economy', 'Unemployment due to seasonal demand']),
    ('What is structural unemployment?', 'Unemployment caused by a mismatch between workers’ skills or location and the jobs available', 'Long-term changes in industry structure.', ['Unemployment between jobs', 'Unemployment due to a fall in AD', 'Unemployment in winter months']),
    ('What causes cyclical unemployment?', 'A fall in aggregate demand', 'Demand-deficient.', ['Changes in technology', 'Seasonal changes', 'Workers changing jobs']),
    ('Which policy is most suitable for reducing structural unemployment?', 'Retraining schemes', 'Address skill mismatch.', ['A cut in interest rates', 'A rise in government spending', 'A rise in unemployment benefits']),
    ('Better information about job vacancies would mainly reduce', 'frictional unemployment', 'Shorter search.', ['cyclical unemployment', 'seasonal unemployment', 'structural unemployment']),
])
ex(t19_2, [
    ('Explain the difference between structural and cyclical unemployment.', 'Structural: long-term mismatch of skills/location due to changes in the economy’s structure (e.g. decline of an industry). Cyclical: caused by a fall in aggregate demand during a downturn, affecting many industries.', '1 mark each; 1 mark contrast of cause/remedy [3]'),
    ('Explain why some frictional unemployment is inevitable.', 'People always change jobs and new entrants search for work; it takes time to find and match to suitable vacancies.', '1 mark: job changes/search; 1 mark: imperfect information/time [2]'),
])
classify(t19_2, UN_CASES, UN_LABELS, 'Which type of unemployment is this?', 'Identify the type of unemployment in each case and explain your answer.', name='untype')
items(t19_2, 'C2', (1, 2, 3, 4), [
    ('Many textile factories in {country} have moved production abroad. Explain the type of unemployment this causes and why it may last a long time.', 'Structural: workers’ skills are specific to textiles and may not match new jobs; they may need retraining or to move region, which takes time.', '1 mark: structural; 1 mark: why persistent [2]'),
])
errs(t19_2, [
    ('Cutting interest rates is the best way to reduce structural unemployment.', 'Lower interest rates raise AD and tackle cyclical unemployment; structural unemployment needs supply-side policies such as retraining and help with mobility.'),
])


@t19_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t19_2_mix(r, D):
    c = r.choice(COUNTRIES)
    f, s, cy, se = r.choice([200, 250, 300]), r.choice([400, 500, 600]), r.choice([300, 450, 600]), r.choice([50, 80, 100])
    tot = f + s + cy + se
    LF = r.choice([20, 25, 30])
    stem = f'Unemployment in {c} (thousands): frictional {f}, structural {s}, cyclical {cy}, seasonal {se}. The labour force is {LF} million.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the unemployment rate.', pct(100 * tot / (LF * 1000)), f'{tot}k ÷ {LF}m × 100.', dis_num(r, 100 * tot / (LF * 1000), pct, [100 * s / (LF * 1000)]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the unemployment rate and the share of unemployment that is cyclical. (b) Calculate the unemployment rate if expansionary policy removed all cyclical unemployment. (c) Explain why demand-side policy cannot remove the rest.',
            'answer': f'(a) {pct(100 * tot / (LF * 1000))}; cyclical {pct(100 * cy / tot)} of the unemployed. (b) {pct(100 * (tot - cy) / (LF * 1000))} (c) Frictional, structural and seasonal unemployment are not caused by lack of demand; they need supply-side measures (information, retraining, mobility).',
            'key': '(a) rate [1]; share [1] (b) [1] (c) explanation [1] [4]', 'marks': 4, 'type': 'numerical'}


t19_3 = T('Consequences of unemployment for individuals, firms and the economy', 'consequences of unemployment', 'individuals, firms and the economy')
mc(t19_3, [
    ('Which is a consequence of high unemployment for the government?', 'Lower tax revenue and higher spending on benefits', 'Budget worsens.', ['Higher tax revenue', 'Lower spending on benefits', 'A budget surplus']),
    ('What is the main opportunity cost of unemployment for the economy?', 'The output that the unemployed could have produced', 'Lost output; inside PPC.', ['The cost of benefits', 'Higher wages', 'Lower imports']),
    ('Which is a possible benefit of unemployment for firms?', 'Easier recruitment and less pressure for wage rises', 'Larger pool of labour.', ['Higher sales', 'More consumer spending', 'Higher prices']),
    ('Why may long-term unemployment reduce an economy’s potential output?', 'Workers lose skills and motivation (hysteresis)', 'Deskilling.', ['It raises productivity', 'It increases investment', 'It lowers wages']),
])
ex(t19_3, [
    ('Explain two consequences of unemployment for individuals.', 'Loss of income and lower living standards; loss of skills and confidence; health problems; social exclusion; harder to find future work.', '1 mark each consequence explained [4]'),
    ('Explain why unemployment can worsen a government’s budget position.', 'Tax revenue falls (less income tax, less spending so less indirect tax) while spending on benefits rises.', '1 mark: revenue falls; 1 mark: spending rises [2]'),
])
items(t19_3, 'C2', (1, 2, 3, 4), [
    ('Unemployment in {city} has been above 15% for many years. Explain two consequences for the local economy.', 'Lower incomes reduce local spending, so businesses close; crime and social problems; skilled workers leave; property values fall.', '1 mark each [2]'),
])
errs(t19_3, [
    ('Unemployment has no cost to the economy because unemployed people receive benefits.', 'Benefits are transfers; the real cost is the output that could have been produced, plus lost skills and social costs.'),
])


@t19_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t19_3_cost(r, D):
    c = r.choice(COUNTRIES)
    U = r.choice([200, 400, 500, 800])
    out = r.choice([20, 25, 30, 40])
    ben = r.choice([5, 6, 8])
    tax = r.choice([4, 5, 6])
    lost = U * out / 1000
    fisc = U * (ben + tax) / 1000
    stem = f'In {c}, {U} thousand people are unemployed. Each could produce output worth ${out},000 a year. Each receives ${ben},000 in benefits and would pay ${tax},000 in tax if employed.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the output lost each year.', f'${num(lost, 1)}bn', f'{U},000 × ${out},000.', dis_num(r, lost, lambda v: f'${num(v, 1)}bn', [fisc, U * ben / 1000]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the output lost each year and the annual cost to the government budget. (b) Explain why the output lost is a better measure of the cost to society than the benefits paid.',
            'answer': f'(a) Output lost ${num(lost, 1)}bn; budget cost ${num(fisc, 1)}bn (benefits + lost tax). (b) Benefits are transfers from taxpayers to the unemployed and do not use up resources; lost output is the real opportunity cost to society.',
            'key': '(a) lost output [1]; budget cost [1] (b) transfers vs real resources [2] [4]', 'marks': 4, 'type': 'numerical'}


def _ch19_case(r, D):
    d = ctx(r)
    u0, u1 = r.choice([(4.5, 7.8), (5, 9), (6, 10.5)])
    y0, y1 = r.choice([(12, 22), (10, 19), (15, 26)])
    intro = (f'Extract: The unemployment rate in {d["country"]} rose from {u0}% to {u1}% over two years, while youth unemployment rose from {y0}% to {y1}%. '
             f'Job losses have been concentrated in manufacturing as firms automate, but retail and construction also cut jobs as consumer spending fell. Vacancies for software engineers remain unfilled.')
    parts = [
        lambda r: ('Calculate the percentage increase in the unemployment rate.', pct(chg(u0, u1)), '[2]'),
        lambda r: ('Identify two types of unemployment indicated by the extract and explain your choice.', 'Structural (automation, unfilled skilled vacancies: mismatch); cyclical (fall in consumer spending).', '[4]'),
        lambda r: ('Explain two consequences of high youth unemployment.', 'Lost skills/hysteresis, lower lifetime earnings, social problems, emigration, lost output.', '[2]'),
        lambda r: ('Discuss which policies would be most effective in reducing unemployment in this economy.', 'Demand-side for cyclical (lower interest rates, fiscal stimulus) and supply-side for structural (retraining in IT, apprenticeships, mobility); time lags and costs; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='case')


case([t19_1, t19_2, t19_3], _ch19_case)
essay(t19_1, [
    ('Explain how unemployment is measured and the problems involved in measuring it accurately.',
     'Labour force, unemployment rate; claimant count vs labour force survey (ILO); hidden unemployment, discouraged workers, underemployment, informal sector.',
     'the claimant count is a poor measure of unemployment in {country}',
     'Depends on benefit rules; excludes ineligible; affected by policy changes.',
     'Cheap, timely and complete; trend is useful; LFS has sampling error; use both.'),
])
essay(t19_2, [
    ('Explain the causes of frictional, structural, cyclical and seasonal unemployment.',
     'Definitions, causes and examples of each type; link to AD and to supply-side factors.',
     'structural unemployment is a more serious problem than cyclical unemployment for {country}',
     'Long-lasting, regional concentration, deskilling; harder to cure.',
     'Cyclical unemployment can be widespread and severe in recessions and may become structural (hysteresis); both serious; depends on scale.'),
])
essay(t19_3, [
    ('Explain the consequences of unemployment for individuals, firms and the economy.',
     'Income loss, skills, health; firms: lower demand but cheaper labour; economy: lost output, budget, inequality, social costs.',
     'reducing unemployment should be the main macroeconomic objective of the government of {country}',
     'Large economic and social costs; lost output; inequality.',
     'Inflation, growth and external balance also matter; some unemployment is natural; policies may conflict; depends on current situation.'),
])
CHAPTERS[19] = [t19_1, t19_2, t19_3]

# ============================================================================ 20 Price stability
t20_1 = T('Inflation, deflation and disinflation; measuring inflation with a consumer price index', 'inflation, deflation and disinflation', 'consumer price index', 'inflation')
mc(t20_1, [
    ('What is inflation?', 'A sustained increase in the general price level', 'Ongoing rise in average prices.', ['A rise in the price of one good', 'A fall in the price level', 'An increase in output']),
    ('What is disinflation?', 'A fall in the rate of inflation, with prices still rising', 'Prices rise more slowly.', ['A fall in the general price level', 'A rise in the inflation rate', 'Zero inflation']),
    ('What is deflation?', 'A sustained fall in the general price level', 'Negative inflation.', ['A fall in the rate of inflation', 'A fall in output', 'A rise in interest rates']),
    ('Why are weights used in a consumer price index?', 'To reflect the share of household spending on each item', 'More important items count more.', ['To adjust for changes in quality', 'To exclude food and energy', 'To measure changes in income']),
    ('If the CPI rises from 120 to 126, the inflation rate is', '5%', '6/120 × 100.', ['6%', '4.8%', '26%']),
    ('Inflation falls from 6% to 3%. What is happening to prices?', 'They are still rising, but more slowly', 'Disinflation.', ['They are falling', 'They are unchanged', 'They are rising faster']),
])
ex(t20_1, [
    ('Explain how a consumer price index is constructed.', 'A base year is chosen (index = 100); a household expenditure survey selects a representative basket and weights; prices are collected regularly; price changes are weighted and averaged to give the index.', '1 mark: basket/survey; 1 mark: weights; 1 mark: base year/index calculation [3]'),
    ('Explain the difference between deflation and disinflation.', 'Deflation is a fall in the general price level (negative inflation); disinflation is a fall in the rate of inflation while prices are still rising.', '1 mark each [2]'),
    ('Explain two limitations of a CPI as a measure of inflation.', 'Basket and weights may not match all households; quality changes and new products; substitution when prices change; excludes some items (e.g. housing costs).', '1 mark each limitation explained [4]'),
])
items(t20_1, 'C2', (1, 2, 3, 4), [
    ('The inflation rate in {country} fell from 8% last year to 4% this year. A newspaper says “prices are falling”. Explain why this is incorrect.', 'Prices are still rising, by 4%; this is disinflation, not deflation.', '1 mark: prices still rising; 1 mark: disinflation [2]'),
])
errs(t20_1, [
    ('If the inflation rate falls from 5% to 2%, prices are falling.', 'Prices are still rising, but more slowly: this is disinflation, not deflation.'),
    ('A rise in the price of petrol is inflation.', 'Inflation is a sustained rise in the general price level, not a rise in one price.'),
])


@t20_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t20_1_cpi(r, D):
    c = r.choice(COUNTRIES)
    items_ = r.sample([('Food', None), ('Housing', None), ('Transport', None), ('Clothing', None), ('Entertainment', None), ('Energy', None)], 3)
    ws = r.choice([(50, 30, 20), (40, 35, 25), (45, 35, 20), (30, 50, 20)])
    ps = [r.choice([2, 3, 4, 5, 6, 8, 10, -2]) for _ in range(3)]
    infl = sum(w * p for w, p in zip(ws, ps)) / 100
    tab = table(['Category', 'Weight', 'Price change (%)'], [(n, w, p) for (n, _), w, p in zip(items_, ws, ps)])
    stem = f'The table shows a simplified consumer price index for {c}. {tab}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the rate of inflation.', pchg(infl, 2), ' + '.join(f'{w}% × {p}' for w, p in zip(ws, ps)) + f' = {num(infl, 2)}%.', dis_num(r, infl, lambda v: pchg(v, 2), [sum(ps) / 3, sum(ps)]), mcq_D=(1, 2))
    base = r.choice([100, 110, 120])
    return {'stem': stem + f' Last year the CPI was {base}. (a) Calculate the weighted inflation rate and the new value of the CPI. (b) Explain why the weighted rate differs from a simple average of the price changes. (c) Explain why this inflation rate may not reflect the experience of every household.',
            'answer': f'(a) {pchg(infl, 2)}; CPI = {num(base * (1 + infl / 100), 1)}. (b) Categories with larger weights (bigger share of spending) influence the index more; the simple average is {num(sum(ps) / 3, 2)}%. (c) Households’ spending patterns differ from the average basket (e.g. low-income households spend more on food).',
            'key': '(a) weighted average [2]; new CPI [1] (b) weights [1] (c) different baskets [1] [5]', 'marks': 5, 'type': 'multi_step'}


DP_CASES = [
    ('Consumer spending in {country} surges after a large tax cut while the economy is at full capacity.', 'Demand-pull inflation', 'AD rises faster than the economy can supply.'),
    ('World oil prices double, raising firms’ costs in {country}.', 'Cost-push inflation', 'higher costs shift SRAS left.'),
    ('Trade unions in {country} win wage increases well above productivity growth.', 'Cost-push inflation', 'higher unit labour costs raise prices.'),
    ('An export boom and rapid credit growth push spending in {country} above capacity.', 'Demand-pull inflation', 'excess AD.'),
    ('The currency of {country} depreciates sharply, raising the price of imported components.', 'Cost-push inflation', 'imported input costs rise.'),
    ('The central bank of {country} keeps interest rates very low and lending booms.', 'Demand-pull inflation', 'cheap credit raises C and I, increasing AD.'),
]

t20_2 = T('Causes of inflation: demand-pull and cost-push', 'causes of inflation', 'demand-pull and cost-push')
mc(t20_2, [
    ('What causes demand-pull inflation?', 'Aggregate demand rising faster than aggregate supply', 'Too much spending chasing too few goods.', ['Rising costs of production', 'A fall in AD', 'A rise in productivity']),
    ('What causes cost-push inflation?', 'Increases in costs of production such as wages and raw materials', 'SRAS shifts left.', ['A rise in consumer spending', 'A fall in interest rates', 'A rise in exports']),
    ('A large rise in world oil prices is most likely to cause', 'cost-push inflation', 'Higher input costs.', ['demand-pull inflation', 'deflation', 'disinflation']),
    ('Which is likely to cause demand-pull inflation?', 'A large increase in government spending at full employment', 'Excess AD.', ['A fall in wages', 'An increase in productivity', 'A rise in unemployment']),
    ('What is a wage–price spiral?', 'Higher prices lead to higher wage demands, which raise costs and prices further', 'Expectations-driven cycle.', ['Falling wages leading to falling prices', 'Wages rising slower than prices', 'Price controls on wages']),
])
ex(t20_2, [
    ('Explain the difference between demand-pull and cost-push inflation, using AD/AS analysis.', 'Demand-pull: AD shifts right near full capacity, raising the price level (and output). Cost-push: higher costs shift SRAS left, raising the price level and reducing output.', '1 mark each; 1 mark diagram reference [3]'),
    ('Explain how inflationary expectations can cause inflation to persist.', 'If people expect prices to rise, workers demand higher wages and firms raise prices in advance, so costs and prices continue rising.', '1 mark: wage demands; 1 mark: firms’ pricing [2]'),
])
classify(t20_2, DP_CASES, ['Demand-pull inflation', 'Cost-push inflation'], 'Which type of inflation is most likely?', 'Identify the type of inflation in each case and explain.', extra=['Deflation', 'Disinflation'], name='inftype')
items(t20_2, 'C2', (1, 2, 3, 4), [
    ('Inflation in {country} has risen while real GDP has fallen. Explain which type of inflation is more likely.', 'Cost-push: an SRAS shift left raises prices and reduces output; demand-pull would normally raise output too.', '1 mark: cost-push; 1 mark: reasoning [2]'),
])
errs(t20_2, [
    ('Higher wages always cause demand-pull inflation.', 'Higher wages raise firms’ costs (cost-push); they may also raise spending, but the main channel is costs unless productivity rises equally.'),
])


@t20_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t20_2_ulc(r, D):
    c = r.choice(COUNTRIES)
    w = r.choice([4, 5, 6, 8])
    p = r.choice([1, 2, 3])
    ulc = (1 + w / 100) / (1 + p / 100) * 100 - 100
    stem = f'In {c}, average wages rose by {w}% while labour productivity rose by {p}%.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the approximate change in unit labour costs.', pchg(ulc), f'(1.0{w} ÷ 1.0{p}) − 1 ≈ {num(ulc, 1)}%.' if w < 10 else f'≈ {num(ulc, 1)}%', dis_num(r, ulc, pchg, [w + p, w]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the approximate change in unit labour costs. (b) Explain how this could lead to cost-push inflation. (c) Explain why wage rises matched by productivity growth need not be inflationary.',
            'answer': f'(a) ≈ {pchg(ulc)} (b) Higher unit labour costs reduce profit margins; firms raise prices and SRAS shifts left, raising the price level. (c) If output per worker rises as fast as wages, unit labour costs are unchanged, so there is no cost pressure on prices.',
            'key': '(a) [1] (b) costs → prices/SRAS [2] (c) unit costs unchanged [1] [4]', 'marks': 4, 'type': 'numerical'}


t20_3 = T('Consequences of inflation and deflation', 'consequences of inflation and deflation', 'consequences of inflation')
mc(t20_3, [
    ('Who is most likely to lose from unanticipated inflation?', 'Savers whose interest rate is below the inflation rate', 'Real value of savings falls.', ['Borrowers with fixed-rate loans', 'Owners of property', 'Governments with large debts']),
    ('What are menu costs?', 'The costs to firms of changing prices frequently', 'Reprinting price lists, updating systems.', ['The cost of food in restaurants', 'The cost of holding cash', 'Taxes on goods']),
    ('Why might inflation that is higher than in other countries harm a country’s exports?', 'Its goods become less price competitive', 'Relative prices rise.', ['Its exchange rate always rises', 'Imports become dearer', 'Its exports become cheaper']),
    ('Why can deflation be harmful?', 'Consumers delay spending, expecting lower prices, which reduces AD', 'Deflationary spiral; real debt burden rises.', ['It always raises output', 'It reduces the real value of debts', 'It makes exports less competitive']),
    ('What is the real interest rate?', 'The nominal interest rate minus the inflation rate', 'r = i − π.', ['The interest rate set by the central bank', 'The nominal rate plus inflation', 'The rate on government bonds']),
])
ex(t20_3, [
    ('Explain two costs of inflation.', 'Redistribution from savers and those on fixed incomes; menu and shoe-leather costs; uncertainty reduces investment; loss of international competitiveness; fiscal drag.', '1 mark each cost, 1 mark each explained [4]'),
    ('Explain why a period of deflation can increase the burden of debt.', 'Debts are fixed in money terms; as prices and incomes fall, the real value of the debt rises, making repayment harder.', '1 mark: fixed nominal debt; 1 mark: real burden rises [2]'),
])
items(t20_3, 'C2', (1, 2, 3, 4), [
    ('{person} has savings earning 2% interest while inflation in {country} is 6%. Explain what is happening to the real value of the savings.', 'The real interest rate is −4%, so the purchasing power of the savings falls by about 4% a year.', '1 mark: real rate −4%; 1 mark: purchasing power falls [2]'),
    ('Pensioners in {country} receive a fixed pension that is not linked to prices. Explain how inflation affects them.', 'Their nominal income is fixed, so rising prices reduce their real income and living standards.', '1 mark: fixed income; 1 mark: real income falls [2]'),
])
errs(t20_3, [
    ('Inflation is always bad for everyone.', 'Borrowers can gain as the real value of debts falls, and mild inflation can ease adjustments; savers and those on fixed incomes lose.'),
    ('Deflation is always good because goods become cheaper.', 'Falling prices can lead consumers to delay spending, raise real debt burdens and cause falling output and unemployment.'),
])


@t20_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t20_3_real(r, D):
    p = person(r)
    sav = r.choice([5000, 10000, 20000])
    i = r.choice([1, 2, 3, 4, 5])
    pi = r.choice([2, 3, 5, 6, 8])
    if i == pi:
        return None
    nom = sav * (1 + i / 100)
    real = nom / (1 + pi / 100)
    stem = f'{p} saves ${sav:,} for a year at a nominal interest rate of {i}%. Inflation over the year is {pi}%.'
    if D <= 2:
        return cq(r, 1, stem + ' What is the approximate real interest rate?', pchg(i - pi, 0), f'r ≈ {i} − {pi}.', dis_num(r, i - pi, lambda v: pchg(v, 0), [i + pi, pi - i]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the nominal value of the savings after one year and their real value in today’s prices. (b) Explain who gains and who loses from this situation.',
            'answer': f'(a) {money(nom)}; real value {money(real)} ({"less" if real < sav else "more"} than ${sav:,}). (b) ' + ('Savers lose purchasing power; borrowers gain because the real value of what they repay falls.' if pi > i else 'Savers gain a positive real return; borrowers pay a positive real cost.'),
            'key': '(a) nominal [1]; real ÷ (1 + inflation) [1] (b) savers vs borrowers [2] [4]', 'marks': 4, 'type': 'numerical'}


t20_4 = T('Using price indices to calculate real values', 'using price indices to calculate real values', 'real values')
mc(t20_4, [
    ('How is a nominal value converted into a real value?', 'Nominal value ÷ price index × 100', 'Deflating by the index (base = 100).', ['Nominal value × price index × 100', 'Nominal value − inflation rate', 'Nominal value + price index']),
    ('A worker’s wage rises from $500 to $550 while prices rise by 10%. What has happened to the real wage?', 'It is unchanged', '10% rise in wage = 10% inflation.', ['It rose by 10%', 'It fell by 10%', 'It rose by 20%']),
    ('If nominal wages rise by 3% and inflation is 5%, real wages', 'fall by about 2%', '3 − 5.', ['rise by 8%', 'rise by 2%', 'are unchanged']),
    ('What does a price index of 125 mean?', 'Prices are 25% higher than in the base year', 'Base = 100.', ['Prices have risen by 125%', 'Inflation this year is 25%', 'Prices are 125 times higher']),
])
ex(t20_4, [
    ('Explain why it is important to use real values when comparing incomes over time.', 'Nominal incomes may rise just because of inflation; real values show changes in purchasing power, i.e. what the income can actually buy.', '1 mark: inflation distorts; 1 mark: real = purchasing power [2]'),
])
items(t20_4, 'C2', (1, 2, 3, 4), [
    ('Teachers in {country} received a 4% pay rise while the CPI rose by 6%. Explain what happened to their living standards.', 'Real pay fell by about 2%, so they can buy less than before.', '1 mark: real fall ≈ 2%; 1 mark: purchasing power [2]'),
])
errs(t20_4, [
    ('If my wage rises by 5%, I am 5% better off.', 'Only if prices are unchanged; the real change is roughly the wage rise minus the inflation rate.'),
])


@t20_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t20_4_real(r, D):
    c = r.choice(COUNTRIES)
    w0 = r.choice([400, 500, 600, 800])
    i0, i1 = r.choice([(100, 112), (100, 108), (120, 132), (110, 121)])
    w1 = int(w0 * r.choice([1.05, 1.08, 1.1, 1.15]))
    r0, r1 = w0 / i0 * 100, w1 / i1 * 100
    stem = f'In {c}, the average weekly wage rose from ${w0} to ${w1} while the CPI rose from {i0} to {i1} (base year = 100).'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the real wage in the second year at base-year prices.', money(r1), f'{w1} ÷ {i1} × 100 = {num(r1, 2)}.', dis_num(r, r1, money, [w1 * i1 / 100, w1 - (i1 - i0)]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the real wage in each year at base-year prices. (b) Calculate the percentage change in the real wage. (c) Explain what this shows about workers’ living standards.',
            'answer': f'(a) {money(r0)} → {money(r1)} (b) {pchg(chg(r0, r1))} (c) ' + ('Real wages rose: workers can buy more.' if r1 > r0 else 'Real wages fell: wages did not keep up with prices, so purchasing power fell.'),
            'key': '(a) both real wages [2] (b) [1] (c) interpretation [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch20_case(r, D):
    d = ctx(r)
    c0, c1, c2 = r.choice([(100, 104, 111), (120, 123, 130), (100, 103, 109)])
    w = r.choice([3, 4])
    intro = (f'Extract: The CPI in {d["country"]} was {c0} two years ago, {c1} last year and {c2} this year. Energy prices rose sharply after a global supply shock, and the central bank warns of a wage–price spiral. '
             f'Average wages rose by {w}% this year. Pensioners and savers complain that their living standards are falling.')
    i1, i2 = chg(c0, c1), chg(c1, c2)
    parts = [
        lambda r: ('Calculate the inflation rate in each of the two years.', f'{pchg(i1)}, {pchg(i2)}', '[2]'),
        lambda r: ('Calculate the approximate change in real wages this year.', pchg(w - i2), f'{w} − {num(i2, 1)} [1]'),
        lambda r: ('Explain whether the inflation is more likely to be demand-pull or cost-push.', 'Cost-push: energy supply shock raised costs (SRAS left).', '[2]'),
        lambda r: ('Explain why pensioners and savers lose from inflation.', 'Fixed nominal incomes and low interest rates mean falling real incomes and real value of savings.', '[3]'),
        lambda r: ('Discuss whether a wage–price spiral is likely to develop.', 'Depends on expectations, union power, labour market tightness, central bank credibility and whether the energy shock is temporary; judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t20_1, t20_2, t20_3, t20_4], _ch20_case)
essay(t20_1, [
    ('Explain how inflation is measured using a consumer price index.',
     'Base year; household expenditure survey; basket; weights; price collection; weighted index; inflation rate from index changes; limitations.',
     'the consumer price index is an accurate measure of the cost of living in {country}',
     'Representative basket, regular updating, weights reflect spending.',
     'Different households have different baskets; quality changes; new products; substitution; housing costs; judgement.'),
])
essay(t20_2, [
    ('Explain, with the help of AD/AS diagrams, the difference between demand-pull and cost-push inflation.',
     'Demand-pull: AD shifts right near capacity; cost-push: SRAS shifts left; expectations and wage–price spiral.',
     'cost-push inflation is harder for a government to control than demand-pull inflation',
     'Reducing AD to fight cost-push worsens unemployment/output (stagflation); causes often external (oil prices).',
     'Demand-pull can be persistent with credit booms; supply-side policies help cost-push; credible central bank anchors expectations; depends on cause.'),
])
essay(t20_3, [
    ('Explain the consequences of inflation for households, firms and the economy.',
     'Redistribution, menu and shoe-leather costs, uncertainty, competitiveness, fiscal drag; anticipated vs unanticipated.',
     'deflation is more harmful to an economy than inflation',
     'Delayed spending, rising real debt, falling output and employment, hard for monetary policy.',
     'High inflation erodes savings and competitiveness, creates uncertainty; mild deflation from productivity gains is benign; depends on cause and size.'),
])
essay(t20_4, [
    ('Explain how price indices are used to convert nominal values into real values, with examples.',
     'Real = nominal ÷ index × 100; real wages, real GDP, real interest rates; approximate rule real ≈ nominal − inflation.',
     'workers in {country} are better off whenever their nominal wages rise',
     'Higher money income allows more spending if prices are stable.',
     'If inflation exceeds wage growth real wages fall; taxes (fiscal drag); distribution; quality of jobs; depends on real values.'),
])
CHAPTERS[20] = [t20_1, t20_2, t20_3, t20_4]

# ============================================================================ 21 Government macroeconomic policy objectives
t21_1 = T('Macroeconomic objectives: growth, low unemployment, stable prices and balance of payments stability', 'macroeconomic objectives', 'balance of payments stability', 'stable prices')
mc(t21_1, [
    ('Which is one of the main macroeconomic objectives of governments?', 'Low and stable inflation', 'Growth, low unemployment, price stability, BoP stability.', ['Maximum profits for firms', 'A balanced budget every year', 'The highest possible exchange rate']),
    ('Why do many central banks target inflation of about 2% rather than 0%?', 'A small positive rate reduces the risk of deflation and allows relative prices to adjust', 'Buffer against deflation; measurement bias.', ['Because 0% inflation is impossible to measure', 'To reduce the value of savings', 'To increase unemployment']),
    ('What is meant by balance of payments stability?', 'Avoiding large and persistent current account deficits or surpluses', 'Sustainable external position.', ['A balanced government budget', 'Equal exports of goods and services', 'A fixed exchange rate']),
    ('What is meant by sustainable economic growth?', 'Growth that can be maintained without causing inflation or long-term damage', 'Steady, non-inflationary, environmentally sound.', ['Growth above 10% a year', 'Growth caused by government borrowing', 'Growth in nominal GDP']),
])
ex(t21_1, [
    ('Explain why governments aim for steady economic growth rather than growth that is as fast as possible.', 'Very rapid growth can exceed capacity, causing inflation, current account deficits and boom–bust cycles; steady growth is sustainable and supports confidence and investment.', '1 mark: risks of rapid growth; 1 mark: benefits of steady growth [2]'),
    ('Explain why low unemployment is a macroeconomic objective.', 'Unemployment wastes resources (lost output), reduces incomes and tax revenue, raises benefit spending and has social costs.', '1 mark: lost output; 1 mark: fiscal/social costs [2]'),
])
items(t21_1, 'C2', (1, 2, 3, 4), [
    ('{country} has inflation of 9%, growth of 1% and unemployment of 8%. Explain which macroeconomic objectives it is failing to meet.', 'Price stability (inflation well above a 2% target), growth (well below trend), low unemployment (8% is high).', '1 mark per objective identified with data [3]'),
])
errs(t21_1, [
    ('A government should aim for zero inflation.', 'Most governments target low positive inflation (about 2%) to avoid the risk of deflation and allow relative price adjustment.'),
])


@t21_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_1_table(r, D):
    a, b = r.sample(COUNTRIES, 2)
    da = (r.choice([1.5, 3, 4.5]), r.choice([3, 5, 9]), r.choice([1.8, 2.2, 6]), r.choice([-1, -3, -7]))
    db = (r.choice([-0.5, 2, 5]), r.choice([4, 7, 12]), r.choice([0.5, 2, 9]), r.choice([1, -2, 4]))
    tab = table(['Indicator', a, b], [('Real GDP growth (%)', da[0], db[0]), ('Unemployment (%)', da[1], db[1]), ('Inflation (%)', da[2], db[2]), ('Current account (% of GDP)', da[3], db[3])])

    def score(x):
        return (x[0] >= 2) + (x[1] <= 5) + (1 <= x[2] <= 3) + (abs(x[3]) <= 3)
    sa, sb = score(da), score(db)
    stem = f'{tab}.'
    if D <= 2:
        best = a if sa > sb else b if sb > sa else 'Both equally'
        opts, ans = mcq(r, best, [x for x in (a, b, 'Both equally', 'Neither country meets any objective') if x != best])
        return {'stem': stem + ' Using targets of growth ≥ 2%, unemployment ≤ 5%, inflation 1–3% and a current account within ±3% of GDP, which country meets more objectives?', 'options': opts, 'answer': ans,
                'key': f'{a} meets {sa}, {b} meets {sb}.'}
    return {'stem': stem + ' (a) Using targets of growth ≥ 2%, unemployment ≤ 5%, inflation 1–3% and a current account within ±3% of GDP, identify which objectives each country meets. (b) Explain which country’s macroeconomic performance is better.',
            'answer': f'(a) {a}: {sa} of 4; {b}: {sb} of 4 (by comparing each indicator with its target). (b) The country meeting more objectives is generally performing better, but the size of any failure matters (e.g. very high inflation or unemployment can outweigh several small successes).',
            'key': '(a) each indicator compared with target [2] (b) reasoned judgement using data [2] [4]', 'marks': 4, 'type': 'numerical'}


CONF_CASES = [
    ('The central bank of {country} raises interest rates to cut inflation, and unemployment rises.', 'Low inflation vs low unemployment', 'reducing AD lowers inflation but also output and jobs.'),
    ('Rapid growth in {country} pulls in imports and the current account deficit widens.', 'Economic growth vs balance of payments stability', 'higher incomes raise imports.'),
    ('An expansionary budget in {country} lowers unemployment but inflation rises.', 'Low inflation vs low unemployment', 'higher AD near capacity raises prices.'),
    ('{country} cuts government spending to reduce a current account deficit and growth slows.', 'Economic growth vs balance of payments stability', 'lower AD reduces imports but also growth.'),
    ('Fast growth in {country} increases air pollution in {city}.', 'Economic growth vs environmental sustainability', 'more output creates more negative externalities.'),
    ('Rapid growth in {country} pushes the economy above capacity and inflation rises.', 'Economic growth vs low inflation', 'a positive output gap creates demand-pull inflation.'),
]

t21_2 = T('Possible conflicts between macroeconomic objectives', 'conflicts between macroeconomic objectives', 'possible conflicts')
mc(t21_2, [
    ('Which pair of objectives is most likely to conflict in the short run?', 'Low inflation and low unemployment', 'Raising AD cuts unemployment but raises inflation.', ['Low unemployment and economic growth', 'Economic growth and higher tax revenue', 'Low inflation and international competitiveness']),
    ('Why might rapid economic growth worsen the current account?', 'Rising incomes increase spending on imports', 'Income-induced imports.', ['Exports always fall', 'The exchange rate falls', 'Taxes rise']),
    ('Raising interest rates to reduce inflation may', 'increase unemployment', 'Lower AD.', ['reduce unemployment', 'increase inflation', 'increase growth']),
    ('Which policy could achieve growth without increasing inflation?', 'Supply-side policies that increase LRAS', 'Shift LRAS right.', ['Cutting interest rates', 'Increasing government spending', 'Cutting taxes on consumption']),
])
ex(t21_2, [
    ('Explain why there may be a conflict between reducing unemployment and keeping inflation low.', 'Policies that raise AD to cut unemployment push the economy towards capacity, increasing demand-pull pressure and wage demands, so inflation rises.', '1 mark: AD increase; 1 mark: inflationary pressure [2]'),
    ('Explain how supply-side policies can reduce conflicts between objectives.', 'By shifting LRAS right, they allow higher output and employment without raising the price level and improve competitiveness for the current account.', '1 mark: LRAS shift; 1 mark: growth without inflation [2]'),
])
classify(t21_2, CONF_CASES, ['Low inflation vs low unemployment', 'Economic growth vs balance of payments stability', 'Economic growth vs environmental sustainability', 'Economic growth vs low inflation'], 'Which conflict between objectives does this illustrate?', 'Identify the conflict in each case and explain it.', name='conflict')
items(t21_2, 'C2', (1, 2, 3, 4), [
    ('The government of {country} wants both faster growth and a smaller current account deficit. Explain why this may be difficult to achieve.', 'Faster growth raises incomes and imports, worsening the current account; cutting AD to reduce imports slows growth.', '1 mark: growth raises imports; 1 mark: trade-off [2]'),
])
errs(t21_2, [
    ('All macroeconomic objectives can always be achieved at the same time with the right policy.', 'In the short run demand-side policies often involve trade-offs (e.g. inflation vs unemployment); supply-side policies can reduce but not always remove conflicts.'),
])


@t21_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_2_data(r, D):
    c = r.choice(COUNTRIES)
    u0, u1 = r.choice([(8, 5), (9, 6), (7, 4.5)])
    i0, i1 = r.choice([(2, 5), (1.5, 4.5), (2.5, 6)])
    ca0, ca1 = r.choice([(-1, -4), (0, -3.5), (-2, -5)])
    stem = f'Over two years of expansionary policy in {c}, unemployment fell from {u0}% to {u1}%, inflation rose from {i0}% to {i1}% and the current account moved from {ca0}% to {ca1}% of GDP.'
    if D <= 2:
        return cq(r, 1, stem + ' By how many percentage points did inflation change?', f'{num(i1 - i0, 1)} percentage points', f'{i1} − {i0}.', dis_num(r, i1 - i0, lambda v: f'{num(v, 1)} percentage points', [i1, 100 * (i1 - i0) / i0, i1 + i0]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the changes in each indicator in percentage points. (b) Explain two conflicts between objectives shown by the data.',
            'answer': f'(a) Unemployment {sgn(u1 - u0)} pp; inflation {sgn(i1 - i0)} pp; current account {sgn(ca1 - ca0)} pp of GDP. (b) Lower unemployment vs higher inflation (higher AD near capacity); higher growth/AD vs worse current account (more imports).',
            'key': '(a) three changes [2] (b) each conflict explained with data [2] [4]', 'marks': 4, 'type': 'numerical'}


POLI_CASES = [
    ('The central bank of {country} raises its policy interest rate.', 'Monetary policy', 'the central bank changes the interest rate/money supply.'),
    ('The government of {country} raises income tax rates.', 'Fiscal policy', 'changes in taxation.'),
    ('{country} privatises its state airline and removes regulations on competition.', 'Supply-side policy', 'aims to raise efficiency and LRAS.'),
    ('The government of {country} increases spending on roads.', 'Fiscal policy', 'changes in government spending.'),
    ('The central bank of {country} buys government bonds to increase the money supply.', 'Monetary policy', 'quantitative easing.'),
    ('{country} expands apprenticeships and vocational training.', 'Supply-side policy', 'improves labour quality and productivity.'),
]

t21_3 = T('Overview of policy instruments: fiscal, monetary and supply-side', 'policy instruments', 'fiscal, monetary and supply-side', 'overview')
mc(t21_3, [
    ('What is fiscal policy?', 'The use of government spending and taxation to influence the economy', 'Budget-based policy.', ['Changes in interest rates', 'Changes in the money supply', 'Policies to raise productivity']),
    ('What is monetary policy?', 'The use of interest rates and the money supply to influence the economy', 'Usually by the central bank.', ['Changes in tax rates', 'Government spending on infrastructure', 'Trade restrictions']),
    ('What do supply-side policies aim to do?', 'Increase the productive capacity of the economy', 'Shift LRAS right.', ['Increase aggregate demand only', 'Reduce the money supply', 'Increase imports']),
    ('Who usually conducts monetary policy?', 'The central bank', 'Often independent.', ['The finance ministry', 'Commercial banks', 'Trade unions']),
])
ex(t21_3, [
    ('Explain the difference between demand-side and supply-side policies.', 'Demand-side policies (fiscal and monetary) change AD to influence output, employment and inflation in the short run; supply-side policies aim to increase LRAS/productive capacity in the long run.', '1 mark each [2]'),
])
classify(t21_3, POLI_CASES, ['Monetary policy', 'Fiscal policy', 'Supply-side policy'], 'Which type of policy is this?', 'Identify the type of policy in each case and explain.', extra=['Trade policy'], name='poltype')
items(t21_3, 'C2', (1, 2, 3, 4), [
    ('The government of {country} faces high unemployment caused by a fall in AD. Explain which type of policy would act most quickly.', 'Demand-side policy: monetary policy (interest rate cuts) can be changed quickly; fiscal stimulus raises AD directly; supply-side policies take years.', '1 mark: demand-side; 1 mark: speed reasoning [2]'),
])
errs(t21_3, [
    ('Changing interest rates is an example of fiscal policy.', 'Interest rate changes are monetary policy; fiscal policy uses government spending and taxation.'),
])


@t21_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_3_mix(r, D):
    c = r.choice(COUNTRIES)
    g = r.choice([10, 20, 30])
    t = r.choice([5, 10, 15])
    stem = f'The government of {c} increases infrastructure spending by ${g}bn, cuts income taxes by ${t}bn, while the central bank raises interest rates by 0.5 percentage points.'
    if D <= 2:
        return cq(r, 1, stem + ' By how much does the government’s budget position worsen, before any change in tax revenue from growth?', f'${g + t}bn', f'{g} + {t}.', [f'${x}bn' for x in (g - t, g, t, (g + t) * 2)], mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the change in the budget balance before any effect on revenue from growth. (b) Classify each measure as fiscal or monetary and state whether it is expansionary or contractionary. (c) Explain why the policies may partly offset each other.',
            'answer': f'(a) The deficit rises by ${g + t}bn. (b) Spending rise and tax cut: expansionary fiscal; rate rise: contractionary monetary. (c) Fiscal measures raise AD while higher interest rates reduce consumption and investment, partly cancelling the effect.',
            'key': '(a) [1] (b) classification [2] (c) offsetting effects [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch21_case(r, D):
    d = ctx(r)
    g, u, i, ca = r.choice([(4.5, 4, 6, -5), (5, 3.5, 7, -6), (4, 4.5, 5.5, -4.5)])
    intro = (f'Extract: {d["country"]} is growing at {g}% a year and unemployment is only {u}%. However, inflation has risen to {i}% (target 2%) and the current account deficit is {abs(ca)}% of GDP. '
             f'The finance minister wants to keep growth high; the central bank wants to raise interest rates.')
    parts = [
        lambda r: ('Identify which macroeconomic objectives are being met and which are not.', f'Met: growth ({g}%), low unemployment ({u}%); not met: price stability ({i}% vs 2%), BoP stability (deficit {abs(ca)}%).', '[2]'),
        lambda r: ('Explain how rapid growth may have caused the inflation and the current account deficit.', 'Demand above capacity → demand-pull inflation; higher incomes → more imports.', '[4]'),
        lambda r: ('Explain the conflict between the finance minister’s and the central bank’s aims.', 'Higher interest rates reduce inflation and imports but slow growth and raise unemployment.', '[2]'),
        lambda r: ('Discuss which policy mix would best achieve the government’s objectives.', 'Contractionary monetary policy to cut inflation; supply-side policies to raise capacity and competitiveness; fiscal restraint; time lags and trade-offs; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='case')


case([t21_1, t21_2, t21_3], _ch21_case)
essay(t21_1, [
    ('Explain the main macroeconomic objectives of a government.',
     'Sustainable growth, low unemployment, low and stable inflation, BoP stability; why each matters; how measured.',
     'price stability should be the most important macroeconomic objective for {country}',
     'Low inflation supports confidence, investment and competitiveness; protects savers and the poor.',
     'Unemployment and growth have large welfare costs; priorities depend on the economy’s situation; trade-offs.'),
])
essay(t21_2, [
    ('Explain why conflicts may arise between macroeconomic objectives.',
     'Inflation vs unemployment; growth vs current account; growth vs inflation; growth vs environment; AD-based reasoning.',
     'the conflict between low inflation and low unemployment cannot be avoided',
     'Demand-side policies move both in opposite directions in the short run.',
     'Supply-side policies raise LRAS; credible inflation targeting anchors expectations; in recessions both can improve; depends on the cause of inflation.'),
])
essay(t21_3, [
    ('Explain the differences between fiscal, monetary and supply-side policies.',
     'Instruments, who controls them, how they work (AD vs LRAS), time scales, examples.',
     'supply-side policies are more effective than demand-side policies in achieving macroeconomic objectives in {country}',
     'Raise capacity, growth without inflation, competitiveness, reduce structural unemployment.',
     'Slow, costly, uncertain; ineffective against cyclical unemployment; demand-side needed in recessions; combination best.'),
])
CHAPTERS[21] = [t21_1, t21_2, t21_3]

# ============================================================================ 22 Fiscal policy
t22_1 = T('The government budget: deficit, surplus and national debt', 'government budget', 'deficit, surplus and national debt', 'national debt')
mc(t22_1, [
    ('What is a budget deficit?', 'Government spending exceeds tax revenue in a year', 'Flow; financed by borrowing.', ['Imports exceed exports', 'National debt exceeds GDP', 'Tax revenue exceeds spending']),
    ('What is the national debt?', 'The total amount the government owes as a result of past borrowing', 'Stock accumulated from deficits.', ['The deficit in one year', 'Debt owed by households', 'Debt owed by foreign governments to the country']),
    ('What happens to the national debt when the government runs a budget surplus?', 'It can be reduced', 'Surplus used to repay debt.', ['It rises', 'It stays the same automatically', 'It becomes a deficit']),
    ('Why is the national debt often measured as a percentage of GDP?', 'To show the burden relative to the size of the economy', 'Ability to service debt.', ['To adjust for inflation only', 'Because debt is measured in goods', 'To compare with exports']),
    ('Which is a cost of a large national debt?', 'High interest payments that use tax revenue', 'Opportunity cost of debt interest.', ['Lower interest rates', 'Higher exports', 'A fall in inflation']),
])
ex(t22_1, [
    ('Explain the difference between a budget deficit and the national debt.', 'A budget deficit is a flow: the shortfall of revenue below spending in one year. The national debt is a stock: the total accumulated borrowing that has not been repaid.', '1 mark each [2]'),
    ('Explain why a government might choose to run a budget deficit.', 'To boost AD in a recession; to finance investment in infrastructure that raises future growth; to smooth taxes over the cycle.', '1 mark each reason explained [2]'),
])
items(t22_1, 'C2', (1, 2, 3, 4), [
    ('The national debt of {country} has risen to 110% of GDP. Explain two possible problems this could cause.', 'High interest payments (opportunity cost); higher interest rates/crowding out; loss of confidence; future tax rises; less room for fiscal stimulus.', '1 mark each [2]'),
])
errs(t22_1, [
    ('A budget deficit is the same as the national debt.', 'A deficit is the annual shortfall (flow); the national debt is the accumulated stock of borrowing.'),
    ('If a government runs a deficit, the national debt falls.', 'A deficit must be financed by borrowing, so the national debt rises.'),
])


@t22_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_1_budget(r, D):
    c = r.choice(COUNTRIES)
    gdp = r.choice([400, 500, 800, 1000])
    G = r.choice([180, 200, 220, 250])
    T_ = r.choice([160, 190, 210, 240])
    if G == T_:
        return None
    debt = r.choice([200, 300, 400, 600])
    bal = T_ - G
    stem = f'In {c}, government spending is ${G}bn, tax revenue is ${T_}bn and GDP is ${gdp}bn. The national debt at the start of the year is ${debt}bn.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the budget balance as a percentage of GDP.', pchg(100 * bal / gdp), f'({T_} − {G})/{gdp} × 100.', dis_num(r, 100 * bal / gdp, pchg, [100 * bal / G, -100 * bal / gdp]), mcq_D=(1, 2))
    nd = debt - bal
    return {'stem': stem + ' (a) Calculate the budget balance and state whether it is a deficit or surplus. (b) Calculate the national debt at the end of the year and as a percentage of GDP. (c) Explain one reason why the debt-to-GDP ratio might fall even if the government runs a deficit.',
            'answer': f'(a) {money(bal)}bn: {"surplus" if bal > 0 else "deficit"}. (b) ${nd}bn; {pct(100 * nd / gdp)} of GDP. (c) If nominal GDP grows faster than the debt (through real growth and inflation), the ratio falls.',
            'key': '(a) [1] (b) debt [1]; ratio [1] (c) GDP growth reason [1] [4]', 'marks': 4, 'type': 'numerical'}


TAX_CASES = [
    ('Income tax in {country} rises from 10% on low incomes to 45% on high incomes.', 'Progressive tax', 'the proportion of income paid rises with income.'),
    ('A sales tax of 15% is charged on all goods in {country}.', 'Regressive tax', 'it takes a higher proportion of the income of the poor, who spend more of their income.'),
    ('Every worker in {country} pays 20% of income in tax regardless of income.', 'Proportional tax', 'the same proportion of income for all.'),
    ('Every adult in {city} pays the same $300 a year local tax.', 'Regressive tax', 'a fixed amount is a larger share of a low income.'),
    ('A tax on company profits in {country} is set at 25% for all firms.', 'Proportional tax', 'same rate on profits of all sizes.'),
    ('Wealthier households in {country} pay a higher percentage of property value in tax.', 'Progressive tax', 'rate rises with the tax base.'),
]

t22_2 = T('Taxation: direct and indirect; progressive, regressive and proportional taxes', 'direct and indirect', 'progressive, regressive and proportional', 'taxation')
mc(t22_2, [
    ('Which is a direct tax?', 'Income tax', 'Levied on income/wealth, paid directly by the taxpayer.', ['Value added tax', 'Excise duty on fuel', 'A tariff on imports']),
    ('Which is an indirect tax?', 'Value added tax on goods and services', 'Levied on spending.', ['Corporation tax', 'Income tax', 'Inheritance tax']),
    ('A regressive tax is one where', 'the proportion of income paid in tax falls as income rises', 'Larger burden on the poor.', ['the rich pay a higher proportion', 'everyone pays the same proportion', 'only the rich pay']),
    ('Why are most indirect taxes regressive?', 'Low-income households spend a larger proportion of their income', 'Tax/income falls as income rises.', ['They are only paid by the rich', 'They are charged on savings', 'They have progressive rates']),
    ('What are the main reasons governments levy taxes?', 'To raise revenue, redistribute income and change behaviour', 'Revenue, redistribution, externalities, macro management.', ['To reduce exports', 'To increase unemployment', 'To raise interest rates']),
])
ex(t22_2, [
    ('Explain the difference between direct and indirect taxes, with an example of each.', 'Direct taxes are levied on income or wealth and paid by the person taxed (income tax, corporation tax). Indirect taxes are levied on spending and collected by sellers (VAT, excise duties).', '1 mark each with example [2]'),
    ('Explain why an indirect tax can be regressive even if every consumer pays the same rate.', 'Low-income households spend a larger proportion of their income, so the tax takes a larger share of their income than of high-income households.', '1 mark: spending share; 1 mark: tax/income higher for poor [2]'),
])
classify(t22_2, TAX_CASES, ['Progressive tax', 'Regressive tax', 'Proportional tax'], 'How is this tax best described?', 'Classify each tax and explain.', extra=['Lump-sum subsidy'], name='taxtype')
items(t22_2, 'C2', (1, 2, 3, 4), [
    ('The government of {country} plans to reduce income tax and raise VAT. Explain the likely effect on the distribution of income.', 'Income tax is usually progressive and VAT regressive, so the switch shifts the tax burden towards lower-income households, increasing inequality.', '1 mark: progressive vs regressive; 1 mark: effect [2]'),
])
errs(t22_2, [
    ('VAT is a direct tax because consumers pay it directly when they buy goods.', 'VAT is an indirect tax: it is levied on spending and collected by sellers, not levied on income or wealth.'),
])


@t22_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_2_regr(r, D):
    c = r.choice(COUNTRIES)
    y1, y2 = r.choice([(10000, 50000), (12000, 60000), (8000, 40000)])
    s1, s2 = r.choice([(90, 50), (95, 60), (100, 55)])
    vat = r.choice([10, 15, 20])
    t1, t2 = y1 * s1 / 100 * vat / (100 + vat), y2 * s2 / 100 * vat / (100 + vat)
    stem = f'In {c}, a household earning ${y1:,} spends {s1}% of its income on goods subject to VAT; a household earning ${y2:,} spends {s2}%. VAT is {vat}% and is included in the prices paid.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the VAT paid by the lower-income household.', money(t1), f'Spending {num(y1 * s1 / 100)} × {vat}/{100 + vat}.', dis_num(r, t1, money, [y1 * s1 / 100 * vat / 100, y1 * vat / 100]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the VAT paid by each household as a percentage of income. (b) Explain whether VAT is progressive, proportional or regressive.',
            'answer': f'(a) Low income: {money(t1)} = {pct(100 * t1 / y1)}; high income: {money(t2)} = {pct(100 * t2 / y2)}. (b) Regressive: the proportion of income paid falls as income rises, because poorer households spend a larger share of income.',
            'key': '(a) VAT each [2]; % of income [1] (b) regressive with reason [1] [4]', 'marks': 4, 'type': 'numerical'}


FIS_CASES = [
    ('The government of {country} cuts income tax rates.', 'Expansionary fiscal policy', 'higher disposable income raises consumption and AD.'),
    ('The government of {country} reduces spending on public sector wages.', 'Contractionary fiscal policy', 'lower G reduces AD.'),
    ('The government of {country} raises VAT from 15% to 20%.', 'Contractionary fiscal policy', 'higher taxes reduce real disposable income and AD.'),
    ('The government of {country} increases spending on new hospitals.', 'Expansionary fiscal policy', 'higher G raises AD.'),
    ('The government of {country} increases unemployment benefits.', 'Expansionary fiscal policy', 'higher transfers raise disposable income and consumption.'),
    ('The government of {country} abolishes a tax allowance, raising income tax bills.', 'Contractionary fiscal policy', 'lower disposable income.'),
]

t22_3 = T('Expansionary and contractionary fiscal policy and effects on AD', 'expansionary and contractionary fiscal policy', 'effects on ad', 'fiscal policy')
mc(t22_3, [
    ('Which is an example of expansionary fiscal policy?', 'A cut in income tax', 'Raises AD.', ['A rise in interest rates', 'A cut in government spending', 'A rise in VAT']),
    ('Which is an example of contractionary fiscal policy?', 'A reduction in government spending', 'Lowers AD.', ['A cut in interest rates', 'A cut in income tax', 'An increase in benefits']),
    ('Expansionary fiscal policy is most likely to be used when', 'unemployment is high and there is spare capacity', 'Negative output gap.', ['inflation is well above target', 'the economy is booming', 'the current account deficit is large']),
    ('Which is a possible disadvantage of expansionary fiscal policy?', 'It may increase the budget deficit and national debt', 'Borrowing.', ['It always reduces employment', 'It reduces AD', 'It lowers inflation']),
    ('Why might fiscal policy take a long time to affect the economy?', 'Decisions need approval and projects take time to start', 'Time lags.', ['Interest rates change immediately', 'Taxes cannot be changed', 'AD does not respond to G']),
])
ex(t22_3, [
    ('Explain how expansionary fiscal policy can reduce unemployment.', 'Higher government spending or lower taxes raise AD; firms increase output to meet demand and hire more workers, reducing cyclical unemployment.', '1 mark: AD rises; 1 mark: output and employment rise [2]'),
    ('Explain two limitations of using fiscal policy to manage AD.', 'Time lags; budget deficits and debt; crowding out of private spending; leakages into imports and saving; inflation if near capacity; political pressures.', '1 mark each, 1 mark each explained [4]'),
])
classify(t22_3, FIS_CASES, ['Expansionary fiscal policy', 'Contractionary fiscal policy'], 'Is this expansionary or contractionary fiscal policy?', 'Classify each measure and explain its effect on AD.', extra=['Expansionary monetary policy', 'Supply-side policy'], name='fis')
items(t22_3, 'C2', (1, 2, 3, 4), [
    ('Inflation in {country} is 8% and rising. Explain how fiscal policy could be used to reduce it.', 'Contractionary fiscal policy: cut G or raise taxes to reduce AD, lowering demand-pull pressure.', '1 mark: contractionary; 1 mark: lower AD → lower inflation [2]'),
])
errs(t22_3, [
    ('A cut in interest rates is an example of expansionary fiscal policy.', 'It is expansionary monetary policy; fiscal policy uses government spending and taxation.'),
])


@t22_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_3_ad(r, D):
    c = r.choice(COUNTRIES)
    dg = r.choice([10, 20, 30])
    dt = r.choice([5, 10, 15])
    mpc = r.choice([0.6, 0.7, 0.8])
    first = dg + mpc * dt
    stem = f'The government of {c} increases spending by ${dg}bn and cuts income taxes by ${dt}bn. Households spend {num(mpc * 100)}% of any extra disposable income.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the initial increase in aggregate demand.', f'${num(first, 1)}bn', f'{dg} + {mpc} × {dt}.', dis_num(r, first, lambda v: f'${num(v, 1)}bn', [dg + dt, dg]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the initial increase in AD. (b) Explain why the tax cut adds less to AD than the same amount of extra government spending. (c) Explain why the final effect on AD may be larger than this initial increase.',
            'answer': f'(a) ${num(first, 1)}bn (b) Part of the tax cut ({num((1 - mpc) * 100)}%) is saved, while government spending adds directly to AD. (c) The extra spending becomes income for others, who spend part of it, in successive rounds.',
            'key': '(a) [1] (b) saving leakage [1] (c) successive rounds of spending [2] [4]', 'marks': 4, 'type': 'numerical'}


STAB_CASES = [
    ('Tax revenue in {country} falls automatically as incomes fall in a recession.', 'Automatic stabiliser', 'revenue changes with the cycle without a policy decision.'),
    ('Unemployment benefit payments in {country} rise as more people lose their jobs.', 'Automatic stabiliser', 'spending rises automatically in a downturn.'),
    ('The government of {country} announces a new $20bn road-building programme to fight a recession.', 'Discretionary fiscal policy', 'a deliberate policy decision.'),
    ('The finance minister of {country} cuts VAT for one year to boost spending.', 'Discretionary fiscal policy', 'a deliberate change in tax rates.'),
    ('In a boom, more people in {country} move into higher tax bands, raising revenue.', 'Automatic stabiliser', 'progressive taxes take more as incomes rise.'),
]

t22_4 = T('Automatic stabilisers and discretionary fiscal policy', 'automatic stabilisers', 'discretionary fiscal policy')
mc(t22_4, [
    ('What is an automatic stabiliser?', 'A form of spending or taxation that changes with the economic cycle without government action', 'e.g. progressive taxes, unemployment benefits.', ['A rule that fixes interest rates', 'A deliberate change in tax rates', 'A subsidy to exporters']),
    ('How do automatic stabilisers affect the budget in a recession?', 'The deficit rises as tax revenue falls and benefit spending rises', 'Cyclical deficit.', ['The budget moves into surplus', 'The budget is unaffected', 'Government spending falls']),
    ('What is discretionary fiscal policy?', 'Deliberate changes in government spending or tax rates', 'Requires decisions.', ['Changes that happen automatically', 'Central bank interest rate changes', 'Changes in exchange rates']),
    ('Which is an advantage of automatic stabilisers over discretionary policy?', 'They work without time lags in decision-making', 'Automatic and immediate.', ['They can be targeted precisely', 'They always eliminate recessions', 'They never affect the budget']),
])
ex(t22_4, [
    ('Explain how progressive income taxes act as an automatic stabiliser.', 'In a boom incomes rise and people move into higher bands, so tax takes a rising share and dampens spending; in a recession tax falls faster than income, supporting spending.', '1 mark: boom; 1 mark: recession [2]'),
    ('Explain one advantage and one disadvantage of discretionary fiscal policy.', 'Advantage: can be large and targeted at specific problems. Disadvantage: time lags in recognising, deciding and implementing; political motives; may be mistimed.', '1 mark each [2]'),
])
classify(t22_4, STAB_CASES, ['Automatic stabiliser', 'Discretionary fiscal policy'], 'Is this an automatic stabiliser or discretionary fiscal policy?', 'Classify each and explain.', extra=['Monetary policy', 'Supply-side policy'], name='stab')
items(t22_4, 'C2', (1, 2, 3, 4), [
    ('During a recession the budget deficit of {country} rose from 2% to 6% of GDP although tax rates and benefit rules were unchanged. Explain why.', 'Automatic stabilisers: falling incomes and spending cut tax revenue and rising unemployment raised benefit spending.', '1 mark: revenue fell; 1 mark: spending rose [2]'),
])
errs(t22_4, [
    ('Automatic stabilisers require the government to pass new laws each recession.', 'They work automatically through existing tax and benefit systems, without new decisions.'),
])


@t22_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_4_cyc(r, D):
    c = r.choice(COUNTRIES)
    y0 = r.choice([500, 600, 800])
    fall = r.choice([2, 3, 4, 5])
    tr = r.choice([30, 35, 40])
    u = r.choice([100, 150, 200])
    b = r.choice([6, 8, 10])
    y1 = y0 * (1 - fall / 100)
    drev = (y0 - y1) * tr / 100
    dben = u * b / 1000
    stem = f'In a recession, GDP in {c} falls by {fall}% from ${y0}bn. Tax revenue is {tr}% of GDP, and {u} thousand more people claim unemployment benefit of ${b},000 a year each.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the fall in tax revenue.', f'${num(drev, 1)}bn', f'{tr}% × ({y0} − {num(y1, 1)}).', dis_num(r, drev, lambda v: f'${num(v, 1)}bn', [dben, y0 * tr / 100]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the fall in tax revenue and the rise in benefit spending. (b) Calculate the total deterioration in the budget balance. (c) Explain how these changes help to stabilise the economy.',
            'answer': f'(a) Revenue −${num(drev, 1)}bn; benefits +${num(dben, 1)}bn. (b) ${num(drev + dben, 1)}bn. (c) They support disposable income and spending, so AD falls less than it otherwise would.',
            'key': '(a) [2] (b) [1] (c) cushions AD [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch22_case(r, D):
    d = ctx(r)
    def0, def1 = r.choice([(2, 7), (3, 8), (1.5, 6.5)])
    debt0, debt1 = r.choice([(60, 85), (50, 75), (70, 95)])
    intro = (f'Extract: After a deep recession, the budget deficit in {d["country"]} rose from {def0}% to {def1}% of GDP and national debt from {debt0}% to {debt1}% of GDP. '
             f'Part of the rise was caused by automatic stabilisers; the rest by a discretionary programme of infrastructure spending and a temporary cut in VAT. The opposition calls for immediate spending cuts.')
    parts = [
        lambda r: ('Calculate the increase in the debt-to-GDP ratio in percentage points.', f'{debt1 - debt0} percentage points', '[1]'),
        lambda r: ('Explain the difference between the budget deficit and the national debt.', 'Deficit = annual flow; debt = accumulated stock.', '[2]'),
        lambda r: ('Explain how automatic stabilisers increased the deficit.', 'Lower incomes reduced tax revenue; higher unemployment raised benefit spending.', '[2]'),
        lambda r: ('Explain how the VAT cut and infrastructure spending were intended to affect AD.', 'Higher disposable income/consumption and higher G raise AD, output and employment.', '[3]'),
        lambda r: ('Discuss whether the government should make immediate spending cuts.', 'Debt interest, confidence and future taxes vs risk of deepening recession, automatic deficit falls with recovery, infrastructure raises LRAS; timing and credibility; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t22_1, t22_2, t22_3, t22_4], _ch22_case)
essay(t22_1, [
    ('Explain the difference between a budget deficit and the national debt, and why a government might run a deficit.',
     'Flow vs stock; financing by borrowing; reasons: recession, investment, smoothing; cyclical vs structural deficits.',
     'a high national debt is always harmful to {country}',
     'Interest payments, crowding out, confidence, future taxes, reduced fiscal space.',
     'Depends on who holds it, interest rates, growth, what it financed (productive investment); in recessions borrowing helps; judgement.'),
])
essay(t22_2, [
    ('Explain the differences between direct and indirect taxes and between progressive, regressive and proportional taxes.',
     'Definitions and examples; tax/income relationships; incidence; examples with numbers.',
     'governments should rely more on direct taxes than indirect taxes',
     'Direct taxes can be progressive and reduce inequality; stable revenue.',
     'Indirect taxes harder to avoid, influence behaviour (externalities), less disincentive to work; mix needed; depends on objectives.'),
])
essay(t22_3, [
    ('Explain how expansionary and contractionary fiscal policy affect aggregate demand.',
     'Changes in G and T; effect on C and AD; multiplied effects; AD/AS diagrams; use in recession vs boom.',
     'fiscal policy is an effective way to reduce unemployment in {country}',
     'Direct injection to AD; targeted spending; works in deep recessions.',
     'Time lags, crowding out, imports leak, debt; ineffective for structural unemployment; inflation near capacity; judgement.'),
])
essay(t22_4, [
    ('Explain how automatic stabilisers work and how they differ from discretionary fiscal policy.',
     'Progressive taxes and benefits change with the cycle; no decision lag; discretionary = deliberate changes; examples.',
     'automatic stabilisers are sufficient to stabilise the economy of {country}',
     'Immediate, no political lags, symmetrical, cushion shocks.',
     'Too small for deep recessions; worsen deficits; discretionary action or monetary policy needed; depends on size of shock.'),
])
CHAPTERS[22] = [t22_1, t22_2, t22_3, t22_4]

# ============================================================================ 23 Monetary policy
t23_1 = T('Money supply, interest rates and the role of the central bank', 'money supply', 'interest rates', 'role of the central bank')
mc(t23_1, [
    ('What is the money supply?', 'The total amount of money (cash and bank deposits) in the economy', 'Narrow and broad measures.', ['The total value of goods produced', 'The amount of cash held by the central bank only', 'Government tax revenue']),
    ('What is the interest rate?', 'The price of borrowing money and the reward for saving', 'Cost of credit.', ['The rate of inflation', 'The exchange rate', 'The tax rate on savings']),
    ('Which is a function of a central bank?', 'Setting the policy interest rate to control inflation', 'Monetary policy, lender of last resort, banker to government.', ['Collecting income tax', 'Lending to households for mortgages', 'Setting government spending']),
    ('Why do many governments make their central bank independent?', 'To make monetary policy decisions free from short-term political pressure', 'Credibility of inflation targets.', ['To increase government control of interest rates', 'To allow banks to print money freely', 'To fix the exchange rate']),
    ('What is meant by the central bank acting as lender of last resort?', 'It lends to commercial banks that are short of funds in a crisis', 'Financial stability.', ['It lends to households who cannot borrow elsewhere', 'It lends to foreign governments', 'It buys shares in failing firms']),
])
ex(t23_1, [
    ('Explain two functions of a central bank.', 'Conducts monetary policy (interest rates, money supply); issues notes and coins; banker to the government; banker to commercial banks/lender of last resort; supervises the financial system; manages reserves and exchange rate.', '1 mark each function explained [2]'),
    ('Explain how commercial banks can increase the money supply.', 'When banks make loans they create deposits in borrowers’ accounts, which can be spent and re-deposited; bank lending therefore increases broad money.', '1 mark: loans create deposits; 1 mark: increases money supply [2]'),
])
items(t23_1, 'C2', (1, 2, 3, 4), [
    ('The central bank of {country} is given independence to set interest rates. Explain why this might lead to lower inflation.', 'Independent central banks can make unpopular decisions (raising rates) without political pressure; this makes inflation targets credible, lowering inflation expectations.', '1 mark: no political pressure; 1 mark: credibility/expectations [2]'),
])
errs(t23_1, [
    ('The central bank of {country} collects taxes and decides government spending.', 'Taxes and spending are fiscal policy decided by the government; the central bank conducts monetary policy.'),
])


@t23_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_1_real(r, D):
    c = r.choice(COUNTRIES)
    i = r.choice([2, 3, 4, 5, 6, 7, 8])
    pi = r.choice([1, 2, 3, 4, 6, 9])
    if i == pi:
        return None
    rr = i - pi
    stem = f'The central bank of {c} sets its policy interest rate at {i}%. Inflation is {pi}%.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the approximate real interest rate.', pchg(rr, 0), f'{i} − {pi}.', dis_num(r, rr, lambda v: pchg(v, 0), [i + pi, -rr]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the real interest rate. (b) Explain how the real interest rate affects the incentive to borrow and to save. (c) Explain whether monetary policy is tight or loose.',
            'answer': f'(a) {pchg(rr, 0)} (b) A higher real rate raises the real cost of borrowing and reward for saving, reducing spending; a negative real rate encourages borrowing and discourages saving. (c) ' + ('Tight: positive real rate restrains AD.' if rr > 1 else 'Loose: low or negative real rate stimulates AD.'),
            'key': '(a) [1] (b) borrowing and saving effects [2] (c) [1] [4]', 'marks': 4, 'type': 'numerical'}


MON_CASES = [
    ('The central bank of {country} cuts its policy interest rate from 3% to 2%.', 'Expansionary monetary policy', 'cheaper borrowing raises consumption and investment.'),
    ('The central bank of {country} buys $50bn of government bonds from banks.', 'Expansionary monetary policy', 'quantitative easing increases the money supply and lowers long-term interest rates.'),
    ('The central bank of {country} raises interest rates to curb inflation.', 'Contractionary monetary policy', 'dearer borrowing reduces spending.'),
    ('The central bank of {country} sells government bonds it holds.', 'Contractionary monetary policy', 'reduces bank reserves and the money supply.'),
    ('The central bank of {country} raises banks’ minimum reserve requirements.', 'Contractionary monetary policy', 'banks can lend less.'),
]

t23_2 = T('Monetary policy instruments: interest rates, money supply and quantitative easing', 'monetary policy instruments', 'quantitative easing', 'monetary policy')
mc(t23_2, [
    ('What is quantitative easing?', 'The central bank buying financial assets to increase the money supply', 'Asset purchases with new central bank money.', ['The government printing money to pay wages', 'Raising interest rates', 'Selling government bonds']),
    ('When is quantitative easing most likely to be used?', 'When interest rates are already close to zero', 'Zero lower bound.', ['When inflation is very high', 'When the economy is booming', 'When the exchange rate is low']),
    ('Which is a monetary policy instrument?', 'The central bank’s policy interest rate', 'Rates, money supply, QE, reserve ratios.', ['Income tax rates', 'Government spending', 'Tariffs']),
    ('Raising the reserve requirement for commercial banks will', 'reduce their ability to lend', 'Tighter credit.', ['increase lending', 'reduce interest rates', 'increase the money supply']),
])
ex(t23_2, [
    ('Explain how quantitative easing is intended to increase aggregate demand.', 'The central bank buys bonds, raising their prices and lowering long-term interest rates; banks gain reserves to lend; cheaper credit and higher asset prices raise consumption and investment.', '1 mark: asset purchases; 1 mark: lower long-term rates/more lending; 1 mark: C and I rise [3]'),
])
classify(t23_2, MON_CASES, ['Expansionary monetary policy', 'Contractionary monetary policy'], 'Is this expansionary or contractionary monetary policy?', 'Classify each measure and explain how it works.', extra=['Expansionary fiscal policy', 'Supply-side policy'], name='mon')
items(t23_2, 'C2', (1, 2, 3, 4), [
    ('Interest rates in {country} are already 0.1% and the economy is in recession. Explain why the central bank might use quantitative easing.', 'It cannot cut rates further, so it buys assets to increase the money supply and reduce long-term rates, encouraging spending.', '1 mark: zero lower bound; 1 mark: QE mechanism [2]'),
])
errs(t23_2, [
    ('Quantitative easing means the government spends more on public services.', 'QE is a monetary policy: the central bank buys financial assets to increase the money supply; it is not government spending.'),
])


@t23_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_2_bond(r, D):
    c = r.choice(COUNTRIES)
    coupon = r.choice([40, 50, 60])
    p0 = r.choice([1000, 800])
    p1 = int(p0 * r.choice([1.1, 1.25, 1.2]))
    y0, y1 = 100 * coupon / p0, 100 * coupon / p1
    stem = f'A government bond in {c} pays a fixed ${coupon} a year. After central bank purchases (quantitative easing), its market price rises from ${p0:,} to ${p1:,}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the new yield on the bond.', pct(y1, 2), f'{coupon}/{p1} × 100.', dis_num(r, y1, lambda v: pct(v, 2), [y0, 100 * coupon / (p1 - p0)]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the yield before and after. (b) Explain how lower bond yields can lead to higher aggregate demand.',
            'answer': f'(a) {pct(y0, 2)} → {pct(y1, 2)} (b) Lower yields reduce long-term borrowing costs (mortgages, corporate loans), encourage investment and consumption, raise asset prices and wealth, and may weaken the currency, raising net exports.',
            'key': '(a) both yields [2] (b) borrowing costs [1]; spending/wealth [1] [4]', 'marks': 4, 'type': 'numerical'}


t23_3 = T('Expansionary and contractionary monetary policy and the transmission to AD', 'expansionary and contractionary monetary policy', 'transmission to ad', 'transmission')
mc(t23_3, [
    ('How does a cut in interest rates increase consumption?', 'It reduces the cost of borrowing and the reward for saving', 'Credit cheaper; mortgage payments fall.', ['It increases income tax', 'It raises the price of imports', 'It reduces the money supply']),
    ('How might a rise in interest rates affect the exchange rate?', 'It may cause the currency to appreciate as foreign funds flow in', 'Hot money inflows.', ['It always causes depreciation', 'It has no effect', 'It fixes the exchange rate']),
    ('Why might a cut in interest rates have little effect on AD in a deep recession?', 'Confidence is low, so households and firms do not want to borrow', 'Pushing on a string.', ['Interest rates cannot be cut', 'Saving becomes more attractive', 'Imports become cheaper']),
    ('Higher interest rates reduce investment because', 'the cost of borrowing to finance projects rises', 'Fewer projects profitable.', ['firms’ profits always rise', 'consumers spend more', 'exports rise']),
])
ex(t23_3, [
    ('Explain how a rise in interest rates reduces inflation.', 'Borrowing becomes dearer and saving more attractive, so consumption and investment fall; mortgage costs rise; the currency may appreciate, reducing net exports and import prices; AD falls, reducing demand-pull inflation.', '1 mark each channel (max 3) [3]'),
    ('Explain one reason why monetary policy may take time to affect inflation.', 'Loans and mortgages may be on fixed rates; firms’ investment plans take time to change; prices adjust slowly; lags of 18–24 months.', '1 mark: reason; 1 mark: explanation [2]'),
])
items(t23_3, 'C2', (1, 2, 3, 4), [
    ('Most mortgages in {country} have variable interest rates. Explain why this makes monetary policy more powerful.', 'A change in the policy rate quickly changes mortgage payments and disposable income, so consumption responds faster and more strongly.', '1 mark: payments change quickly; 1 mark: consumption response [2]'),
])
errs(t23_3, [
    ('A cut in interest rates reduces aggregate demand because savers earn less.', 'Savers earn less, but cheaper borrowing raises consumption and investment by more, so AD usually rises.'),
])


@t23_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_3_mort(r, D):
    p = person(r)
    loan = r.choice([100000, 150000, 200000, 250000])
    i0, i1 = r.choice([(3, 4), (4, 5.5), (2.5, 3.5), (5, 4), (4, 3)])
    pay0, pay1 = loan * i0 / 100, loan * i1 / 100
    stem = f'{p} has an interest-only mortgage of ${loan:,}. The interest rate changes from {num(i0, 1)}% to {num(i1, 1)}% after a central bank decision.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the change in annual interest payments.', ('+' if pay1 > pay0 else '−') + money(abs(pay1 - pay0)), f'{loan:,} × ({num(i1, 1)}% − {num(i0, 1)}%).',
                  [s + money(x) for s, x in (('+' if pay1 < pay0 else '−', abs(pay1 - pay0)), ('+', pay1), ('−', pay0), ('+', abs(pay1 - pay0) * 2))], mcq_D=(1, 2))
    up = i1 > i0
    return {'stem': stem + ' (a) Calculate the annual interest payments before and after. (b) Explain how this change, repeated across many households, affects aggregate demand and inflation.',
            'answer': f'(a) {money(pay0)} → {money(pay1)} (b) ' + ('Higher payments reduce disposable income and consumption; AD falls, reducing inflationary pressure.' if up else 'Lower payments raise disposable income and consumption; AD rises, which may raise inflation.'),
            'key': '(a) both [2] (b) disposable income → C → AD [1]; inflation [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch23_case(r, D):
    d = ctx(r)
    i0, i1 = r.choice([(0.5, 4), (1, 4.5), (0.25, 3.5)])
    inf = r.choice([7, 8, 9])
    intro = (f'Extract: Inflation in {d["country"]} reached {inf}%, well above the central bank’s 2% target. Over 18 months the central bank raised its policy rate from {i0}% to {i1}% and stopped its programme of quantitative easing. '
             f'House prices began to fall and the currency appreciated. Business groups warned that higher rates would push the economy into recession.')
    parts = [
        lambda r: ('Calculate the real policy interest rate at the end of the period, assuming inflation is still {}%.'.format(inf), pchg(i1 - inf), f'{i1} − {inf} [1]'),
        lambda r: ('Explain how higher interest rates could reduce inflation.', 'Dearer credit reduces C and I; appreciation reduces net exports and import prices; AD falls.', '[4]'),
        lambda r: ('Explain why falling house prices might reduce consumption.', 'Negative wealth effect; less equity to borrow against; confidence falls.', '[2]'),
        lambda r: ('Discuss whether raising interest rates is the best way to reduce inflation in this economy.', 'Effective for demand-pull, credibility; but lags, recession risk, ineffective against cost-push, hits borrowers; fiscal or supply-side alternatives; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='case')


case([t23_1, t23_2, t23_3], _ch23_case)
essay(t23_1, [
    ('Explain the functions of a central bank.',
     'Monetary policy, issuing currency, banker to government and banks, lender of last resort, financial regulation, managing reserves.',
     'central banks in {country} should be independent of government',
     'Credibility, long-term focus, lower inflation expectations, no electoral cycle.',
     'Lack of democratic accountability; coordination with fiscal policy; may focus too narrowly on inflation; depends on institutions.'),
])
essay(t23_2, [
    ('Explain the instruments of monetary policy, including quantitative easing.',
     'Policy rate, open market operations, reserve requirements, QE; how each affects money supply and interest rates.',
     'quantitative easing is an effective policy when interest rates are close to zero',
     'Lowers long-term rates, supports asset prices and lending, prevents deflation.',
     'Banks may not lend; benefits asset holders (inequality); inflation risk later; diminishing effect; judgement.'),
])
essay(t23_3, [
    ('Explain how a change in interest rates is transmitted to aggregate demand.',
     'Borrowing and saving, mortgage payments, investment, asset prices/wealth, exchange rate and net exports, expectations; AD/AS diagram.',
     'monetary policy is more effective than fiscal policy in controlling inflation in {country}',
     'Quick to change, independent, credible; affects many spending channels.',
     'Long lags; blunt; ineffective for cost-push; fiscal policy can be targeted; depends on mortgage structure and confidence.'),
])
CHAPTERS[23] = [t23_1, t23_2, t23_3]

# ============================================================================ 24 Supply-side policy
SS_CASES = [
    ('The government of {country} cuts the top rate of income tax to encourage work and enterprise.', 'Market-based supply-side policy', 'improves incentives through the market.'),
    ('{country} privatises its state-owned electricity company.', 'Market-based supply-side policy', 'introduces the profit motive and competition.'),
    ('The government of {country} funds free vocational training for young workers.', 'Interventionist supply-side policy', 'government directly invests in human capital.'),
    ('{country} reduces regulations on opening new businesses.', 'Market-based supply-side policy', 'deregulation lowers barriers to entry.'),
    ('The government of {country} builds a new high-speed rail line.', 'Interventionist supply-side policy', 'public investment in infrastructure.'),
    ('{country} weakens trade union powers and makes hiring and firing easier.', 'Market-based supply-side policy', 'labour market reform increases flexibility.'),
    ('The government of {country} gives grants for research into green technology.', 'Interventionist supply-side policy', 'state support for research and development.'),
]
SS_LABELS = ['Market-based supply-side policy', 'Interventionist supply-side policy']

t24_1 = T('Market-based supply-side policies: tax cuts, deregulation, privatisation and labour market reform', 'market-based supply-side policies', 'deregulation, privatisation', 'labour market reform')
mc(t24_1, [
    ('What is the aim of supply-side policies?', 'To increase the productive capacity of the economy', 'Shift LRAS right.', ['To increase AD in the short run', 'To reduce exports', 'To raise interest rates']),
    ('Which is a market-based supply-side policy?', 'Privatisation of state-owned industries', 'Uses markets/incentives.', ['Government-funded training schemes', 'Building new roads', 'Subsidising research']),
    ('How might a cut in income tax rates increase aggregate supply?', 'It increases the incentive to work and to start businesses', 'Higher post-tax rewards.', ['It increases government spending', 'It reduces the money supply', 'It raises import prices']),
    ('What is deregulation?', 'Removing rules that restrict competition and business activity', 'Lower barriers.', ['Introducing new regulations', 'Nationalising industries', 'Setting maximum prices']),
    ('Which labour market reform is intended to increase flexibility?', 'Reducing the power of trade unions', 'Wages and hiring more flexible.', ['Raising the minimum wage', 'Increasing unemployment benefits', 'Lengthening notice periods']),
])
ex(t24_1, [
    ('Explain how privatisation might increase the efficiency of an industry.', 'Private owners seek profit, so they have an incentive to cut costs and innovate; shareholders monitor managers; access to private capital for investment; competition if the market is opened.', '1 mark: profit motive; 1 mark: cost cutting/investment [2]'),
    ('Explain two possible disadvantages of market-based supply-side policies.', 'Tax cuts may increase inequality and reduce revenue; deregulation may harm consumers or the environment; privatisation may create private monopolies; labour reforms may lower job security and wages.', '1 mark each, 1 mark each explained [4]'),
])
classify(t24_1, SS_CASES, SS_LABELS, 'What type of supply-side policy is this?', 'Classify each policy and explain how it could increase LRAS.', extra=['Demand-side fiscal policy', 'Monetary policy'], name='ss')
items(t24_1, 'C2', (1, 2, 3, 4), [
    ('The government of {country} cuts the corporation tax rate from 30% to 20%. Explain how this might increase aggregate supply.', 'Higher post-tax profits increase funds and incentives for investment and attract FDI, raising the capital stock and LRAS.', '1 mark: incentive/funds; 1 mark: capital stock/LRAS [2]'),
])
errs(t24_1, [
    ('Privatisation always lowers prices for consumers.', 'It may raise efficiency, but a private monopoly may raise prices unless it faces competition or regulation.'),
])


@t24_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t24_1_tax(r, D):
    p = person(r)
    w = r.choice([20, 25, 30])
    t0, t1 = r.choice([(40, 30), (45, 35), (50, 40)])
    n0, n1 = w * (1 - t0 / 100), w * (1 - t1 / 100)
    stem = f'{p} earns ${w} an hour for overtime. The marginal income tax rate is cut from {t0}% to {t1}%.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the post-tax hourly reward after the cut.', money(n1), f'{w} × (1 − {t1 / 100}).', dis_num(r, n1, money, [n0, w * t1 / 100]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the post-tax hourly reward before and after, and the percentage increase. (b) Explain why the tax cut may or may not increase the hours that ' + p + ' chooses to work.',
            'answer': f'(a) {money(n0)} → {money(n1)}: {pchg(chg(n0, n1))}. (b) Substitution effect: leisure is now dearer, so more hours; income effect: the same income can be earned with fewer hours, so some may work less; the net effect is uncertain.',
            'key': '(a) both [1]; % [1] (b) substitution vs income effect [2] [4]', 'marks': 4, 'type': 'numerical'}


t24_2 = T('Interventionist supply-side policies: education, training, infrastructure and research', 'interventionist supply-side policies', 'education, training, infrastructure and research')
mc(t24_2, [
    ('Which is an interventionist supply-side policy?', 'Government spending on education and training', 'State invests in factors.', ['Cutting income tax', 'Privatisation', 'Deregulation']),
    ('How does better infrastructure increase aggregate supply?', 'It reduces firms’ transport and communication costs and raises productivity', 'LRAS shifts right.', ['It raises interest rates', 'It increases imports', 'It reduces the labour force']),
    ('Why might the government fund research and development?', 'R&D creates positive externalities that the market under-provides', 'Spillovers.', ['Firms always over-invest in R&D', 'It reduces productivity', 'It increases unemployment']),
    ('Which is a disadvantage of interventionist supply-side policies?', 'They can be expensive and take a long time to have an effect', 'Opportunity cost and lags.', ['They have no effect on productivity', 'They always cause inflation', 'They reduce the quality of labour']),
])
ex(t24_2, [
    ('Explain how government spending on education can increase long-run aggregate supply.', 'It raises the skills and productivity of the labour force (human capital), increasing potential output and shifting LRAS to the right.', '1 mark: human capital/productivity; 1 mark: LRAS shift [2]'),
    ('Explain why interventionist supply-side policies may also increase aggregate demand.', 'They involve government spending (G), which adds to AD in the short run before capacity effects appear.', '1 mark: G component; 1 mark: short-run AD effect [2]'),
])
classify(t24_2, SS_CASES, SS_LABELS, 'What type of supply-side policy is this?', 'Classify each policy and explain how it could increase LRAS.', extra=['Demand-side fiscal policy', 'Monetary policy'], name='ss')
items(t24_2, 'C2', (1, 2, 3, 4), [
    ('{country} has a shortage of engineers. Explain how an interventionist supply-side policy could help.', 'Fund university places, apprenticeships and scholarships in engineering, raising the supply of skilled labour and productivity over time.', '1 mark: policy; 1 mark: effect on labour supply/LRAS [2]'),
])
errs(t24_2, [
    ('Building new roads is a demand-side policy, so it cannot affect aggregate supply.', 'Infrastructure spending raises AD in the short run, but it also lowers costs and raises productivity, shifting LRAS right.'),
])


@t24_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t24_2_return(r, D):
    c = r.choice(COUNTRIES)
    cost = r.choice([5, 8, 10])
    n = r.choice([100, 200, 250])
    gain = r.choice([3000, 4000, 5000])
    yrs = r.choice([10, 20, 30])
    tot = n * gain * yrs / 1e6
    stem = f'{c} spends ${cost}bn on a training programme for {n},000 workers. Each trained worker’s output rises by ${gain:,} a year for {yrs} years.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the total extra output over the period (ignoring discounting).', f'${num(tot, 1)}bn', f'{n},000 × {gain:,} × {yrs}.', dis_num(r, tot, lambda v: f'${num(v, 1)}bn', [n * gain / 1e6, tot - cost]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the total extra output and compare it with the cost. (b) Explain two reasons why the actual benefit may be smaller than this estimate.',
            'answer': f'(a) ${num(tot, 1)}bn vs cost ${cost}bn: ' + ('benefits exceed cost.' if tot > cost else 'benefits are lower than cost.') + ' (b) Workers may emigrate or not use the skills; future benefits should be discounted; some would have trained anyway; demand for skills may change.',
            'key': '(a) total [1]; comparison [1] (b) two reasons [2] [4]', 'marks': 4, 'type': 'numerical'}


t24_3 = T('Effects and limitations of supply-side policies on LRAS', 'effects and limitations of supply-side policies', 'lras')
mc(t24_3, [
    ('Successful supply-side policies shift', 'the LRAS curve to the right', 'Higher capacity.', ['the AD curve to the left', 'the LRAS curve to the left', 'the SRAS curve to the left']),
    ('Which is a limitation of supply-side policies?', 'Their effects take a long time to appear', 'Time lags.', ['They always cause inflation', 'They reduce productive capacity', 'They have immediate effects on unemployment']),
    ('An outward shift of LRAS, with AD constant, will', 'lower the price level and raise real output', 'Non-inflationary growth.', ['raise the price level and lower output', 'have no effect', 'raise unemployment']),
    ('Why might supply-side policies improve the current account?', 'They make domestic firms more competitive internationally', 'Lower costs, better quality.', ['They raise import demand', 'They raise the exchange rate', 'They reduce exports']),
])
ex(t24_3, [
    ('Explain how supply-side policies can help achieve several macroeconomic objectives at once.', 'Shifting LRAS right allows higher growth and employment without inflation; lower costs and better quality improve competitiveness and the current account.', '1 mark: growth without inflation; 1 mark: current account/employment [2]'),
    ('Explain two limitations of supply-side policies.', 'Long time lags; uncertain effects; high costs/opportunity cost; may increase inequality; ineffective against cyclical unemployment if AD is weak.', '1 mark each, 1 mark each explained [4]'),
])
items(t24_3, 'C2', (1, 2, 3, 4), [
    ('{country} has introduced many supply-side reforms, but unemployment remains high during a global recession. Explain why.', 'Supply-side policies raise capacity but do not create demand; cyclical unemployment from low AD requires demand-side policies.', '1 mark: LRAS not AD; 1 mark: cyclical unemployment [2]'),
])
errs(t24_3, [
    ('Supply-side policies quickly reduce cyclical unemployment.', 'Supply-side policies work slowly and raise capacity; cyclical unemployment is caused by low AD and needs demand-side measures.'),
])


@t24_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t24_3_lras(r, D):
    c = r.choice(COUNTRIES)
    y0 = r.choice([500, 600, 800])
    g = r.choice([2, 3, 4])
    p0 = r.choice([100, 110])
    pf = r.choice([1, 1.5, 2])
    y1 = y0 * (1 + g / 100)
    stem = f'Supply-side reforms in {c} raise full-employment output by {g}% from ${y0}bn. Aggregate demand is unchanged, and the price level falls by {num(pf, 1)}% from {p0}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the new full-employment output.', f'${num(y1, 1)}bn', f'{y0} × {1 + g / 100}.', dis_num(r, y1, lambda v: f'${num(v, 1)}bn', [y0 + g, y0 * (1 - g / 100)]), mcq_D=(1, 2))
    return {'stem': stem + ' (a) Calculate the new full-employment output and the new price level. (b) Using an AD/AS diagram, explain these changes. (c) Explain why the outcome might differ if AD were also rising quickly.',
            'answer': f'(a) ${num(y1, 1)}bn; price level {num(p0 * (1 - pf / 100), 2)}. (b) LRAS shifts right; with AD unchanged, equilibrium real output rises and the price level falls. (c) If AD rises faster than LRAS, the price level would still rise (inflation), though by less than without the reforms.',
            'key': '(a) [2] (b) diagram explanation [1] (c) AD vs LRAS comparison [1] [4]', 'marks': 4, 'type': 'numerical'}


def _ch24_case(r, D):
    d = ctx(r)
    p0, p1 = r.choice([(1.0, 2.5), (0.5, 2.0), (0.8, 2.2)])
    edu = r.choice([3, 4, 5])
    intro = (f'Extract: Productivity growth in {d["country"]} has been only {p0}% a year. The government plans to privatise the state railway, cut corporation tax, and raise spending on education to {edu}% of GDP. '
             f'It hopes productivity growth will rise to {p1}%. Critics argue that privatisation will lead to higher fares and that tax cuts mainly benefit the rich.')
    parts = [
        lambda r: ('Classify the three policies as market-based or interventionist.', 'Privatisation and tax cut: market-based; education spending: interventionist.', '[2]'),
        lambda r: ('Calculate the difference in output per worker after 10 years at the two productivity growth rates (start = 100).', f'{num(100 * (1 + p0 / 100) ** 10, 1)} vs {num(100 * (1 + p1 / 100) ** 10, 1)}', '[2]'),
        lambda r: ('Explain how higher education spending could increase LRAS.', 'Human capital raises productivity and potential output.', '[2]'),
        lambda r: ('Explain why privatisation might raise fares.', 'A private monopoly seeks profit and may raise prices or cut services unless regulated.', '[2]'),
        lambda r: ('Discuss whether these supply-side policies are likely to raise productivity growth.', 'Incentives, investment and skills vs time lags, uncertainty, private monopoly, inequality, funding; depends on implementation; judgement.', '[5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t24_1, t24_2, t24_3], _ch24_case)
essay(t24_1, [
    ('Explain how market-based supply-side policies are intended to increase aggregate supply.',
     'Tax cuts (incentives), deregulation, privatisation, labour market reform; mechanisms; LRAS diagram.',
     'cutting taxes is the most effective supply-side policy for {country}',
     'Incentives to work, invest and take risks; attracts FDI.',
     'Income vs substitution effects; inequality; lost revenue for education/infrastructure; evidence mixed; judgement.'),
])
essay(t24_2, [
    ('Explain how interventionist supply-side policies can increase long-run aggregate supply.',
     'Education and training, infrastructure, R&D, regional policy; market failures they correct; LRAS diagram.',
     'government spending on education is the best way to increase long-run growth in {country}',
     'Human capital drives productivity and innovation; positive externalities.',
     'Long lags, quality matters, brain drain, infrastructure and institutions also needed; opportunity cost.'),
])
essay(t24_3, [
    ('Explain the effects of successful supply-side policies on the economy, using an AD/AS diagram.',
     'LRAS shifts right; higher output, lower price level; lower natural unemployment; competitiveness and current account.',
     'supply-side policies are the best way to reduce unemployment in {country}',
     'Tackle structural unemployment, raise employability and capacity.',
     'Cyclical unemployment needs AD; time lags; some policies increase short-run unemployment (privatisation); depends on type of unemployment.'),
])
CHAPTERS[24] = [t24_1, t24_2, t24_3]

# ============================================================================ 25 The reasons for international trade
TRADE_PAIRS = [('rice', 'cloth', 'tonnes of rice', 'metres of cloth'), ('wheat', 'cars', 'tonnes of wheat', 'cars'),
               ('coffee', 'machine tools', 'bags of coffee', 'machine tools'), ('fish', 'bicycles', 'tonnes of fish', 'bicycles'),
               ('maize', 'computers', 'tonnes of maize', 'computers'), ('tea', 'televisions', 'kilograms of tea', 'televisions'),
               ('cotton', 'shoes', 'bales of cotton', 'pairs of shoes'), ('timber', 'solar panels', 'cubic metres of timber', 'solar panels')]


def _ca_data(r):
    """Two countries, two goods, output per worker per week; opportunity-cost ratios differ."""
    for _ in range(60):
        a1, b1, a2, b2 = r.choice([2, 3, 4, 5, 6, 8, 10, 12]), r.choice([2, 3, 4, 5, 6, 8, 10, 12]), r.choice([2, 3, 4, 5, 6, 8, 10, 12]), r.choice([2, 3, 4, 5, 6, 8, 10, 12])
        if a1 * b2 != a2 * b1 and abs(a1 / b1 - a2 / b2) > 0.15 and a1 != a2 and b1 != b2:
            break
    c1, c2 = r.sample(COUNTRIES, 2)
    gx, gy, ux, uy = r.choice(TRADE_PAIRS)
    return c1, c2, gx, gy, ux, uy, a1, b1, a2, b2


def _oc(a, b):
    return num(a / b, 2)


t25_1 = T('Absolute and comparative advantage', 'absolute advantage', 'comparative advantage', 'opportunity cost ratios')
mc(t25_1, [
    ('What is meant by absolute advantage?', 'The ability of a country to produce more of a good than another country with the same resources',
     'Absolute advantage: higher output per unit of resource (or the same output with fewer resources).',
     ['The ability to produce a good at a lower opportunity cost than another country', 'Having a larger population than a trading partner', 'Exporting more than a country imports']),
    ('What is meant by comparative advantage?', 'The ability of a country to produce a good at a lower opportunity cost than another country',
     'Comparative advantage depends on opportunity cost, not on absolute output.',
     ['The ability to produce more of every good than another country', 'Having lower wages than a trading partner', 'A surplus on the current account']),
    ('Which principle explains why a country with an absolute advantage in all goods can still gain from trade?', 'The principle of comparative advantage',
     'Opportunity costs differ, so both countries gain by specialising according to comparative advantage.',
     ['The law of diminishing returns', 'The principle of absolute advantage', 'The law of demand']),
    ('Country X can produce 10 units of food or 5 units of clothing with one worker. What is the opportunity cost of 1 unit of clothing in Country X?', '2 units of food',
     '10 food / 5 clothing = 2 units of food per unit of clothing.', ['0.5 units of food', '5 units of food', '10 units of food']),
    ('Under which condition will there be no gain from specialisation and trade between two countries?', 'When both countries have the same opportunity cost ratios',
     'Comparative advantage requires different opportunity costs.',
     ['When one country has an absolute advantage in both goods', 'When the two countries have different currencies', 'When one country is larger than the other']),
    ('Which assumption is made in the simple two-country model of comparative advantage?', 'Constant opportunity costs and no transport costs',
     'Linear PPCs, perfect factor mobility within a country, no transport costs or trade barriers.',
     ['Increasing returns to scale in all industries', 'Factors of production move freely between countries', 'High transport costs between the countries']),
    ('If a country has a comparative advantage in good X, what is true of its opportunity cost of good Y?', 'It is higher than in the other country',
     'If OC of X is lower, OC of Y (its reciprocal) must be higher, so the other country has comparative advantage in Y.',
     ['It is lower than in the other country', 'It is the same as in the other country', 'It is zero']),
])
ex(t25_1, [
    ('Explain the difference between absolute advantage and comparative advantage.', 'Absolute advantage means producing more of a good than another country with the same resources. Comparative advantage means producing a good at a lower opportunity cost, i.e. giving up less of the other good.',
     '1 mark: absolute = more output from same resources; 1 mark: comparative = lower opportunity cost [2]'),
    ('Explain why a country with an absolute advantage in both goods can still benefit from trade.', 'Its opportunity costs will still differ from the other country’s; if it specialises where its advantage is greatest (lowest opportunity cost) and trades, both countries can consume beyond their own PPCs.',
     '1 mark: opportunity costs differ; 1 mark: specialise in lower-OC good; 1 mark: consume beyond PPC/both gain [3]'),
    ('Explain how comparative advantage can be shown using production possibility curves.', 'With constant costs each PPC is a straight line; its slope is the opportunity cost. If the slopes differ, each country has a comparative advantage in the good it gives up least of the other good to produce.',
     '1 mark: slope = opportunity cost; 1 mark: different slopes = comparative advantage [2]'),
    ('Explain two limitations of the theory of comparative advantage.', 'It assumes constant costs, no transport costs and perfect factor mobility; in reality costs rise with specialisation, transport costs and trade barriers reduce gains, and comparative advantage changes over time.',
     '1 mark each for two limitations, 1 mark each for explanation [4]'),
    ('Explain why comparative advantage can change over time.', 'Opportunity costs depend on factor endowments, skills, technology and investment, which change; e.g. education and FDI can give a country a new comparative advantage in manufactured goods or services.',
     '1 mark: depends on factor endowments/technology; 1 mark: example of change [2]'),
])
errs(t25_1, [
    ('{country} has an absolute advantage in producing both goods, so it cannot gain from trading with {country2}.', 'Gains from trade depend on comparative, not absolute, advantage; as long as opportunity costs differ, both countries can gain by specialising.'),
    ('A country has a comparative advantage in a good if it can produce more of it than any other country.', 'Producing more is absolute advantage; comparative advantage means producing at a lower opportunity cost.'),
    ('If {country} has a comparative advantage in both goods, it should produce both.', 'A country cannot have a comparative advantage in both goods in a two-good model: if its opportunity cost of one good is lower, its opportunity cost of the other is higher.'),
    ('Comparative advantage means a country has lower wages than its trading partners.', 'Comparative advantage is about lower opportunity cost; low wages may reflect low productivity and do not by themselves create comparative advantage.'),
])
items(t25_1, 'C2', (1, 2, 3, 4), [
    ('{country} has a large area of fertile land and few skilled workers, while {country2} has many engineers but little farmland. Explain which country is likely to have a comparative advantage in agricultural goods.',
     '{country}: abundant fertile land means a lower opportunity cost of farm output in terms of manufactured goods; {country2}’s skilled labour gives it a comparative advantage in engineering products.',
     '1 mark: {country}; 1 mark: factor endowment lowers opportunity cost [2]'),
    ('{country} can produce more {mgood2} and more {mgood} per worker than {country2}. Explain what further information is needed to decide which good {country} should specialise in.',
     'The opportunity cost of each good in each country: the ratio of outputs, to see where {country}’s advantage is relatively greatest (lowest opportunity cost).',
     '1 mark: opportunity cost ratios needed; 1 mark: specialise where relative advantage greatest [2]'),
], name='ca_items')


@t25_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t25_1_ca(r, D):
    c1, c2, gx, gy, ux, uy, a1, b1, a2, b2 = _ca_data(r)
    stem = (f'One worker in {c1} can produce either {a1} {ux} or {b1} {uy} a week. One worker in {c2} can produce either {a2} {ux} or {b2} {uy} a week.')
    ocx1, ocx2 = a1 and b1 / a1, b2 / a2      # OC of 1 X in units of Y
    cax = c1 if ocx1 < ocx2 else c2
    cay = c2 if cax == c1 else c1
    abx = c1 if a1 > a2 else c2
    aby = c1 if b1 > b2 else c2
    if D == 1:
        k = r.choice(['abs', 'oc'])
        if k == 'abs':
            return {'stem': stem + f' Which country has an absolute advantage in {gx}?', 'options': mcq(r, abx, [c2 if abx == c1 else c1, 'Neither country', 'Both countries equally'])[0],
                    'answer': abx, 'key': f'Absolute advantage: higher output per worker ({max(a1, a2)} vs {min(a1, a2)} {ux}).'}
        right = f'{_oc(b1, a1)} {uy}'
        pool = []
        for v in [_oc(a1, b1), _oc(b2, a2), _oc(a2, b2), str(b1), str(a1), _oc(b1 + 1, a1), _oc(b1, a1 + 1)]:
            o = f'{v} {uy}'
            if o != right and o not in pool:
                pool.append(o)
        opts, a = mcq(r, right, pool[:3])
        return {'stem': stem + f' What is the opportunity cost of 1 unit of {gx} in {c1}?', 'options': opts, 'answer': a,
                'key': f'OC of 1 {gx} = {b1}/{a1} = {_oc(b1, a1)} {uy}.'}
    if D == 2:
        opts, a = mcq(r, f'{cax} should specialise in {gx} and {cay} in {gy}', [f'{cay} should specialise in {gx} and {cax} in {gy}', f'{abx} should produce both goods',
                                                                               'Neither country can gain from specialisation'] if abx == aby else
                      [f'{cay} should specialise in {gx} and {cax} in {gy}', 'Each country should produce both goods equally', 'Neither country can gain from specialisation'])
        return {'stem': stem + ' On the basis of comparative advantage, which pattern of specialisation would increase total output?', 'options': opts, 'answer': a,
                'key': f'OC of 1 unit of {gx}: {c1} {_oc(b1, a1)}, {c2} {_oc(b2, a2)} {uy}; {cax} has the lower OC of {gx}.'}
    ans_a = (f'OC of 1 unit of {gx}: {c1} = {b1}/{a1} = {_oc(b1, a1)} {uy}; {c2} = {b2}/{a2} = {_oc(b2, a2)} {uy}. OC of 1 unit of {gy}: {c1} = {_oc(a1, b1)} {ux}; {c2} = {_oc(a2, b2)} {ux}.')
    ans_b = f'{cax} has a comparative advantage in {gx} and {cay} in {gy}.'
    if D == 3:
        return {'stem': stem + f' (a) Calculate the opportunity cost of each good in each country. (b) State which country has a comparative advantage in each good.',
                'answer': f'(a) {ans_a} (b) {ans_b}', 'key': '(a) four opportunity costs, 2 marks for all correct, 1 for two [2] (b) both comparative advantages [1] [3]', 'marks': 3, 'type': 'numerical'}
    lo, hi = sorted([ocx1, ocx2])
    tot = round((lo + hi) / 2, 2)
    ans_c = f'1 unit of {gx} must exchange for between {num(lo, 2)} and {num(hi, 2)} {uy}; e.g. 1 unit of {gx} = {num(tot, 2)} {uy} benefits both.'
    abs_note = (f'{abx} has an absolute advantage in both goods, yet both can still gain because opportunity costs differ.' if abx == aby
                else f'{abx} has an absolute advantage in {gx} and {aby} in {gy}.')
    if D == 4:
        return {'stem': stem + f' (a) Identify which country has an absolute advantage in each good. (b) Using opportunity costs, explain which good each country should specialise in. (c) State the range of terms of trade (units of {gy} per unit of {gx}) within which both countries gain.',
                'answer': f'(a) {abs_note} (b) {ans_a} {ans_b} (c) {ans_c}',
                'key': '(a) [1] (b) opportunity costs [1]; specialisation [1] (c) range [2] [5]', 'marks': 5, 'type': 'numerical'}
    W = r.choice([100, 200, 500])
    E = r.choice([20, 40, 50]) * W // 100
    exporter = cax
    oc_exp = ocx1 if exporter == c1 else ocx2
    ax = a1 if exporter == c1 else a2
    gain = E * ax * (tot - oc_exp)
    return {'stem': stem + f' (a) Explain, using opportunity costs, which good each country should specialise in. (b) Show that terms of trade of 1 unit of {gx} = {num(tot, 2)} {uy} benefit both countries. '
                    f'(c) {exporter} has {W} workers, specialises completely in {gx} and exports the output of {E} workers at these terms of trade. Calculate how many more {uy} it can consume than if it had produced the {gy} itself. (d) Explain two reasons why the actual gains from trade may be smaller.',
            'answer': f'(a) {ans_a} {ans_b} (b) {ans_c} It is above {cax}’s OC of {gx} and below {cay}’s, so each obtains the imported good more cheaply than producing it. '
                      f'(c) Exports = {E} × {ax} = {num(E * ax)} {ux}, which buy {num(E * ax)} × {num(tot, 2)} = {num(E * ax * tot, 1)} {uy}; the {E} workers could instead have produced only {E} × {b1 if exporter == c1 else b2} = {num(E * ax * oc_exp, 1)} {uy} at home; gain = {num(gain, 1)} {uy}. '
                      '(d) Transport costs, trade barriers, rising opportunity costs as specialisation increases, imperfect factor mobility.',
            'key': '(a) [2] (b) comparison with both opportunity costs [2] (c) imports received [1]; home-production alternative [1]; gain [1] (d) two reasons [2] [9]', 'marks': 9, 'type': 'numerical'}


CA_CASES = [
    ('{country} has abundant sunshine and land and exports fruit, while importing machinery.', 'Comparative advantage based on natural resources', 'factor endowments give a low opportunity cost of fruit.'),
    ('{country} has invested heavily in education and now exports software services.', 'Comparative advantage based on human capital', 'skilled labour lowers the opportunity cost of skill-intensive services.'),
    ('{country} has a large supply of low-wage, low-skilled labour and exports garments.', 'Comparative advantage based on labour abundance', 'labour-intensive goods have a low opportunity cost where labour is abundant.'),
    ('{country} has large reserves of copper but few factories, and exports copper ore.', 'Comparative advantage based on natural resources', 'mineral endowment gives a low opportunity cost of ore.'),
    ('{country} has a large stock of capital and advanced technology and exports aircraft parts.', 'Comparative advantage based on capital and technology', 'capital-intensive production has a low opportunity cost.'),
]
classify(t25_1, CA_CASES, ['Comparative advantage based on natural resources', 'Comparative advantage based on human capital', 'Comparative advantage based on labour abundance',
                           'Comparative advantage based on capital and technology'], 'What is the most likely source of this country’s comparative advantage?',
         'For each case, identify the likely source of comparative advantage and explain it.', D=(1, 2, 3, 4, 5), name='ca_src')


t25_2 = T('Free trade, specialisation and the gains from trade', 'free trade', 'specialisation', 'gains from trade')
mc(t25_2, [
    ('What is meant by free trade?', 'International trade without government restrictions such as tariffs or quotas',
     'No barriers imposed by governments.', ['Trade that takes place without money', 'Trade only between members of a trading bloc', 'Trade where exports equal imports']),
    ('Which is a benefit of free trade for consumers?', 'Lower prices and a wider choice of goods', 'Competition and access to lower-cost producers.',
     ['Guaranteed employment in domestic industries', 'Higher prices for imported goods', 'Fewer foreign firms in the market']),
    ('How can free trade allow firms to benefit from economies of scale?', 'It gives them access to larger world markets', 'Larger output lowers average cost.',
     ['It protects them from foreign competition', 'It raises the prices of imports', 'It reduces the size of their market']),
    ('What is a risk for a country that specialises heavily in one export?', 'Its income becomes vulnerable to a fall in world demand or price for that good',
     'Over-specialisation increases exposure to shocks.', ['It cannot benefit from comparative advantage', 'Its imports become cheaper', 'Its terms of trade must improve']),
    ('Which statement about the gains from trade is correct?', 'Trade allows countries to consume outside their own production possibility curves',
     'Specialisation and exchange raise combined output and consumption possibilities.', ['Trade benefits only the exporting country', 'Trade always benefits every individual in both countries',
                                                                                             'Trade reduces total world output']),
    ('How might free trade increase efficiency in a domestic industry?', 'Foreign competition forces firms to cut costs and innovate',
     'Competitive pressure removes X-inefficiency.', ['It allows firms to charge higher prices', 'It removes the need for investment', 'It guarantees firms a protected market']),
])
ex(t25_2, [
    ('Explain how specialisation according to comparative advantage increases world output.', 'Each country moves resources into the good it produces at lowest opportunity cost, so the same resources produce more in total; trade then lets countries share the extra output.',
     '1 mark: resources moved to lowest-OC use; 1 mark: total output rises; 1 mark: trade distributes the gains [3]'),
    ('Explain two benefits of free trade for a developing economy.', 'Access to larger markets for exports, raising income and employment; access to cheaper capital goods and technology; competition and FDI raise efficiency.',
     '1 mark each for two benefits, 1 mark each for explanation [4]'),
    ('Explain why free trade may not benefit everyone in an economy.', 'Workers and firms in industries that cannot compete with imports may lose jobs and income; resources are not perfectly mobile, so structural unemployment can result.',
     '1 mark: losers in import-competing industries; 1 mark: factor immobility/structural unemployment [2]'),
    ('Explain how free trade can benefit consumers.', 'Imports from lower-cost producers lower prices, competition improves quality, and consumers gain a wider choice of products.',
     '1 mark: lower prices; 1 mark: choice/quality [2]'),
])
errs(t25_2, [
    ('Free trade benefits every worker in {country}.', 'Free trade raises total welfare, but workers in import-competing industries may lose jobs; there are winners and losers.'),
    ('Specialisation is always beneficial, so {country} should produce only one good.', 'Over-specialisation creates risk: a fall in world demand or price for that good would cause a large fall in income; diversification reduces vulnerability.'),
    ('A country can only gain from trade if it exports more than it imports.', 'Gains from trade come from consuming goods at a lower opportunity cost; they do not depend on having a trade surplus.'),
])
items(t25_2, 'C2', (1, 2, 3, 4), [
    ('Before trade, {country} produced its own {mgood}. After trade liberalisation it imports them more cheaply and its workers move into producing {mgood2}. Explain how {country} gains.',
     'Resources move to the good in which {country} has a comparative advantage, raising output; cheaper imports raise consumers’ real incomes and allow consumption beyond the PPC.',
     '1 mark: resources reallocated to comparative-advantage good; 1 mark: cheaper imports/consumption beyond PPC [2]'),
    ('About 70% of {country}’s export revenue comes from one commodity. Explain one risk this creates.',
     'If the world price of the commodity falls, export revenue, government revenue and national income fall sharply; the country is vulnerable to price volatility.',
     '1 mark: dependence on one good; 1 mark: effect of price/demand fall [2]'),
    ('{firm} in {country} can now sell to a free-trade market of 400 million people instead of 30 million. Explain how this may lower its costs.',
     'A larger market allows higher output and economies of scale (bulk buying, specialised machinery), reducing long-run average cost.',
     '1 mark: larger output; 1 mark: economies of scale lower average cost [2]'),
], name='gt_items')


@t25_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t25_2_gain(r, D):
    c1, c2, gx, gy, ux, uy, a1, b1, a2, b2 = _ca_data(r)
    W = r.choice([100, 200])
    # Before trade each country splits its workers equally between the goods.
    x0 = W // 2 * (a1 + a2)
    y0 = W // 2 * (b1 + b2)
    ocx1, ocx2 = b1 / a1, b2 / a2
    cx, cy = (c1, c2) if ocx1 < ocx2 else (c2, c1)
    # Specialising country for X keeps enough Y? Use complete specialisation of both and compare.
    x1 = W * (a1 if cx == c1 else a2)
    y1 = W * (b2 if cy == c2 else b1)
    stem = (f'{c1} and {c2} each have {W} workers. One worker in {c1} can produce {a1} {ux} or {b1} {uy}; one worker in {c2} can produce {a2} {ux} or {b2} {uy}. '
            f'Before trade, each country uses half its workers in each industry.')
    if D <= 2:
        opts, a = mcq(r, f'{num(x0)} {ux} and {num(y0)} {uy}', [f'{num(x1)} {ux} and {num(y1)} {uy}', f'{num(W * (a1 + a2))} {ux} and {num(W * (b1 + b2))} {uy}', f'{num(x0 // 2)} {ux} and {num(y0 // 2)} {uy}'])
        return {'stem': stem + ' What is the combined output of the two countries before trade?', 'options': opts, 'answer': a,
                'key': f'{W // 2} × ({a1} + {a2}) = {num(x0)} {ux}; {W // 2} × ({b1} + {b2}) = {num(y0)} {uy}.'}
    a_txt = f'Before: {num(x0)} {ux} and {num(y0)} {uy}. After complete specialisation ({cx} in {gx}, {cy} in {gy}): {num(x1)} {ux} and {num(y1)} {uy}.'
    dx, dy = x1 - x0, y1 - y0
    verdict = ('Output of both goods rises, so there is a clear gain from specialisation.' if dx >= 0 and dy >= 0 else
               f'Output of {gx if dx < 0 else gy} falls, so complete specialisation does not raise output of both goods; partial specialisation would be needed for that, '
               'but valued at any terms of trade between the two opportunity-cost ratios, total output is still higher than before.')
    if D == 3:
        return {'stem': stem + f' (a) Calculate the combined output before trade. (b) Calculate the combined output if {cx} specialises completely in {gx} and {cy} in {gy}. (c) Comment on the change.',
                'answer': f'(a)/(b) {a_txt} (c) Change: {sgn(dx, 0)} {ux}, {sgn(dy, 0)} {uy}. {verdict}',
                'key': '(a) [1] (b) [1] (c) comment on change [1] [3]', 'marks': 3, 'type': 'numerical'}
    return {'stem': stem + f' (a) Explain which good each country should specialise in. (b) Calculate the combined output before trade and after complete specialisation. (c) Explain why both countries need to trade at a suitable rate of exchange to share the gains. '
                    + ('(d) Discuss whether specialisation would benefit everyone in both countries.' if D == 5 else ''),
            'answer': f'(a) OC of 1 unit of {gx}: {c1} {_oc(b1, a1)}, {c2} {_oc(b2, a2)} {uy}, so {cx} specialises in {gx} and {cy} in {gy}. (b) {a_txt} Change: {sgn(dx, 0)} {ux}, {sgn(dy, 0)} {uy}. '
                      f'(c) Each country now produces only one good, so must trade; the terms of trade must lie between the opportunity-cost ratios ({_oc(min(b1 * a2, b2 * a1), a1 * a2)}–{_oc(max(b1 * a2, b2 * a1), a1 * a2)} {uy} per unit of {gx}) for both to gain. ' + verdict + ' '
                      + ('(d) Workers in contracting industries face structural unemployment; transport costs and rising opportunity costs reduce gains; over-specialisation risk; consumers gain overall; judgement.' if D == 5 else ''),
            'key': '(a) [2] (b) before [1]; after [1] (c) terms of trade range [2]' + (' (d) winners and losers, judgement [3] [9]' if D == 5 else ' [6]'),
            'marks': 9 if D == 5 else 6, 'type': 'numerical'}


GT_CASES = [
    ('After {country} joins a free trade agreement, prices of imported {mgood} fall by 15%.', 'Benefit to consumers', 'lower prices raise consumers’ real incomes.'),
    ('{firm} expands output fourfold after gaining access to export markets, and its average cost falls.', 'Economies of scale', 'a larger market allows lower long-run average cost.'),
    ('Domestic {mgood} producers in {country} close factories after cheaper imports arrive.', 'Cost of free trade: structural unemployment', 'workers in import-competing industries lose jobs and may lack transferable skills.'),
    ('Foreign competition forces {firm} to adopt new technology and cut waste.', 'Increased efficiency through competition', 'competitive pressure reduces X-inefficiency.'),
    ('{country} earns 80% of its export revenue from cocoa and suffers when the world price halves.', 'Risk of over-specialisation', 'dependence on one export makes income volatile.'),
]
classify(t25_2, GT_CASES, ['Benefit to consumers', 'Economies of scale', 'Cost of free trade: structural unemployment', 'Increased efficiency through competition', 'Risk of over-specialisation'],
         'Which effect of free trade and specialisation does this illustrate?', 'For each case, identify the effect of free trade and specialisation and explain it.', name='gt_cls')


def tot_word(t):
    return 'improved (favourable)' if t > 100 else ('worsened (unfavourable)' if t < 100 else 'unchanged')


t25_3 = T('Terms of trade: calculation and causes of change', 'terms of trade', 'terms of trade index', 'causes of change in the terms of trade')
mc(t25_3, [
    ('How is the terms of trade index calculated?', '(Index of average export prices ÷ index of average import prices) × 100',
     'ToT = Px index / Pm index × 100.', ['(Index of import prices ÷ index of export prices) × 100', '(Value of exports ÷ value of imports) × 100', 'Export volume minus import volume']),
    ('What is meant by an improvement in the terms of trade?', 'Each unit of exports buys more imports than before', 'Export prices rise relative to import prices.',
     ['The volume of exports rises', 'The current account moves into surplus', 'Import prices rise relative to export prices']),
    ('Which would cause a country’s terms of trade to deteriorate?', 'A fall in world prices of its main exports', 'Export price index falls relative to import index.',
     ['A rise in world prices of its main exports', 'A fall in the prices of its imports', 'An appreciation of its currency']),
    ('Export prices rise by 10% and import prices rise by 10%. What happens to the terms of trade?', 'It is unchanged', '110/110 × 100 = 100.',
     ['It rises by 10%', 'It falls by 10%', 'It rises by 20%']),
    ('How does an appreciation of a country’s currency affect its terms of trade, other things equal?', 'They improve, because export prices in foreign currency rise and import prices in domestic currency fall',
     'Appreciation raises Px relative to Pm.', ['They worsen', 'They are unaffected', 'They improve only if exports rise in volume']),
    ('Why might an improvement in the terms of trade be bad for the current account?', 'Exports become less price competitive, so export volumes may fall',
     'If demand for exports is price elastic, revenue falls.', ['Import prices rise', 'The exchange rate falls', 'Export volumes always rise']),
    ('Which is a likely cause of a long-run decline in the terms of trade of primary-product exporters?', 'Low income elasticity of demand for primary products',
     'Demand for primary goods grows slowly as world income rises (Prebisch-Singer).', ['High income elasticity of demand for primary products', 'Rising world demand for food', 'Falling prices of manufactured imports']),
])
ex(t25_3, [
    ('Explain two causes of an improvement in a country’s terms of trade.', 'A rise in world demand for its exports raising their prices; an appreciation of its currency; higher domestic inflation than abroad; falling world prices of its imports (e.g. oil for an importer).',
     '1 mark each for two causes, 1 mark each for explanation [4]'),
    ('Explain why an improvement in the terms of trade is not necessarily good for an economy.', 'If it results from higher export prices due to inflation or appreciation, export volumes may fall when demand is price elastic, worsening the current account and raising unemployment.',
     '1 mark: loss of price competitiveness; 1 mark: depends on PED/effect on export revenue and jobs [2]'),
    ('Explain the difference between the terms of trade and the balance of trade.', 'The terms of trade is the ratio of export prices to import prices; the balance of trade is the value of exports of goods minus the value of imports of goods.',
     '1 mark: ToT price ratio; 1 mark: balance of trade value difference [2]'),
    ('Explain how a rise in world demand for a country’s main export can improve its terms of trade and its current account at the same time.', 'Higher demand raises the world price of the export (ToT improves) and also the quantity sold, so export revenue rises and the current account improves.',
     '1 mark: price rises/ToT; 1 mark: revenue rises/current account improves [2]'),
])
errs(t25_3, [
    ('The terms of trade of {country} have improved, so its current account must also have improved.', 'An improvement means export prices have risen relative to import prices; if demand for exports is price elastic, export revenue may fall and the current account may worsen.'),
    ('The terms of trade measure the quantity of exports compared with the quantity of imports.', 'The terms of trade compare average export prices with average import prices, not quantities.'),
    ('If the terms of trade index falls from 100 to 95, export prices must have fallen.', 'A fall means export prices fell relative to import prices; export prices may have risen but by less than import prices.'),
])


@t25_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t25_3_tot(r, D):
    c = r.choice(COUNTRIES)
    px = r.choice([88, 92, 95, 98, 104, 106, 108, 112, 115, 120])
    pm = r.choice([90, 94, 96, 102, 105, 110, 114, 118])
    if px == pm:
        pm += 2
    t = 100 * px / pm
    yr = r.choice([2015, 2018, 2020])
    stem = f'In {c}, with {yr} = 100, the export price index in {yr + 5} was {px} and the import price index was {pm}.'
    if D <= 2:
        return cq(r, D, stem + f' Calculate the terms of trade index for {yr + 5}.', num(t, 1), f'{px}/{pm} × 100 = {num(t, 1)}.',
                  dis_num(r, t, lambda v: num(v, 1), [100 * pm / px, px - pm + 100]), mcq_D=(1, 2))
    if D == 3:
        return {'stem': stem + f' (a) Calculate the terms of trade index for {yr + 5}. (b) State whether the terms of trade have improved or worsened, and explain what this means.',
                'answer': f'(a) {px}/{pm} × 100 = {num(t, 1)}. (b) They have {tot_word(t)}: a given quantity of exports now buys {"more" if t > 100 else "fewer"} imports than in {yr}.',
                'key': '(a) [2] (b) direction [1]; meaning [1] [4]', 'marks': 4, 'type': 'numerical'}
    px2 = px + r.choice([-6, -4, 4, 6, 8])
    pm2 = pm + r.choice([-5, -3, 3, 5, 7])
    t2 = 100 * px2 / pm2
    stem2 = stem + f' In {yr + 6} the export price index was {px2} and the import price index was {pm2}.'
    ans = (f'(a) {yr + 5}: {num(t, 1)}; {yr + 6}: {px2}/{pm2} × 100 = {num(t2, 1)}. (b) Change {yr + 5}–{yr + 6}: {pchg(chg(t, t2))}; '
           f'the terms of trade {"improved" if t2 > t else "worsened"} between {yr + 5} and {yr + 6}. ')
    if D == 4:
        return {'stem': stem2 + f' (a) Calculate the terms of trade index for both years. (b) Calculate the percentage change in the terms of trade between {yr + 5} and {yr + 6}. (c) Explain two possible causes of this change.',
                'answer': ans + '(c) ' + ('Rising world demand or prices for its exports; appreciation of the currency; higher domestic inflation; falling import prices such as oil.' if t2 > t else
                                          'Falling world prices for its exports, e.g. a commodity price fall; rising import prices such as oil; depreciation of the currency; lower domestic inflation.'),
                'key': '(a) both indices [2] (b) [1] (c) two causes [2] [5]', 'marks': 5, 'type': 'numerical'}
    return {'stem': stem2 + f' (a) Calculate the terms of trade index for both years and the percentage change between them. (b) Explain two possible causes of this change. (c) Discuss whether the change is likely to benefit {c}.',
            'answer': ans + '(b) ' + ('Higher export prices from rising world demand or appreciation; falling import prices.' if t2 > t else 'Lower export prices from falling world demand or depreciation; rising import prices.') +
            ' (c) Depends on the cause and price elasticities: a demand-led rise in export prices raises export revenue and living standards, but a rise caused by inflation or appreciation reduces competitiveness and may worsen the current account if demand is elastic; a fall caused by depreciation may raise export volumes; judgement.',
            'key': '(a) indices [2]; percentage change [1] (b) two causes [2] (c) depends on cause and PED, judgement [3] [8]', 'marks': 8, 'type': 'numerical'}


@t25_3.add('C3', (2, 3, 4, 5), 'numerical')
def t25_3_pct(r, D):
    c = r.choice(COUNTRIES)
    x = r.choice([-10, -6, -4, 2, 5, 8, 12, 15])
    m = r.choice([-5, -2, 3, 4, 6, 10, 20])
    if x == m:
        m += 1
    t = 100 * (100 + x) / (100 + m)
    stem = f'Over a year, the average price of {c}’s exports {"rose" if x > 0 else "fell"} by {abs(x)}% and the average price of its imports {"rose" if m > 0 else "fell"} by {abs(m)}%. The terms of trade index was 100 at the start of the year.'
    if D <= 3:
        return cq(r, 2 if D == 2 else 9, stem + ' Calculate the terms of trade index at the end of the year.', num(t, 1), f'({100 + x}/{100 + m}) × 100 = {num(t, 1)}' + ('.' if D == 2 else ': method [1]; answer [1] [2]'),
                  dis_num(r, t, lambda v: num(v, 1), [100 + x - m, 100 * (100 + m) / (100 + x)]), mcq_D=(2,))
    return {'stem': stem + f' (a) Calculate the new terms of trade index. (b) Explain what has happened to the purchasing power of {c}’s exports. (c) Explain one possible effect on {c}’s current account.',
            'answer': f'(a) {100 + x}/{100 + m} × 100 = {num(t, 1)}. (b) The terms of trade have {tot_word(t)}; each unit of exports buys {pct(abs(t - 100))} {"more" if t > 100 else "fewer"} imports. '
                      '(c) ' + ('If export demand is price elastic, higher relative export prices reduce export volumes and may worsen the current account; if inelastic, export revenue rises.' if t > 100 else
                                'Relatively cheaper exports may raise export volumes if demand is elastic, improving the current account; if inelastic, revenue falls and the current account worsens.'),
            'key': '(a) [2] (b) [1] (c) effect depends on PED [2] [5]', 'marks': 5, 'type': 'numerical'}


TOT_CASES = [
    ('A global shortage pushes up the world price of copper, {country}’s main export.', 'Improvement in the terms of trade', 'export prices rise relative to import prices.'),
    ('The world price of oil, which {country} imports, doubles.', 'Deterioration in the terms of trade', 'import prices rise relative to export prices.'),
    ('The currency of {country} appreciates by 12%.', 'Improvement in the terms of trade', 'export prices in foreign currency rise and import prices in domestic currency fall.'),
    ('A bumper harvest across producing countries lowers the world price of coffee, {country}’s main export.', 'Deterioration in the terms of trade', 'export prices fall relative to import prices.'),
    ('Inflation in {country} is 9% while inflation in its trading partners is 2%.', 'Improvement in the terms of trade', 'domestic export prices rise faster than import prices.'),
    ('The currency of {country} depreciates sharply after a fall in interest rates.', 'Deterioration in the terms of trade', 'export prices in foreign currency fall and import prices in domestic currency rise.'),
]
classify(t25_3, TOT_CASES, ['Improvement in the terms of trade', 'Deterioration in the terms of trade'], 'What is the likely effect on the terms of trade of {country}?',
         'For each event, state the likely effect on the terms of trade and explain why.', extra=['No change in the terms of trade', 'An increase in export volumes only'], name='tot_cls')


BLOC_CASES = [
    ('Members remove tariffs on trade with each other, but each member sets its own tariffs on imports from non-members.', 'Free trade area', 'no internal tariffs, separate external tariffs.'),
    ('Members remove tariffs on trade with each other and impose a common external tariff on imports from non-members.', 'Customs union', 'free internal trade plus a common external tariff.'),
    ('Members have free internal trade, a common external tariff and free movement of labour and capital.', 'Common market', 'customs union plus free movement of factors of production.'),
    ('Members have free internal trade and factor movement, a single currency and harmonised economic policies.', 'Economic union', 'common market plus common currency/monetary and coordinated fiscal policy.'),
    ('Three neighbouring countries agree to scrap tariffs on goods traded among themselves while keeping their own, different tariffs on goods from elsewhere.', 'Free trade area', 'separate external tariffs, so rules of origin are needed.'),
    ('Two countries agree that both will charge a 10% tariff on cars imported from outside their bloc, and none on cars traded between them.', 'Customs union', 'common external tariff with internal free trade.'),
]
BLOC_LABELS = ['Free trade area', 'Customs union', 'Common market', 'Economic union']

t25_4 = T('Trading blocs and the WTO: free trade areas, customs unions and economic unions', 'trading blocs', 'free trade areas, customs unions', 'economic unions', 'wto')
mc(t25_4, [
    ('What distinguishes a customs union from a free trade area?', 'A customs union has a common external tariff', 'FTA members keep separate external tariffs.',
     ['A customs union has free movement of labour', 'A customs union has a single currency', 'A free trade area has a common external tariff']),
    ('What is meant by trade creation?', 'A shift from higher-cost domestic production to lower-cost imports from a bloc partner', 'Efficiency gain from joining a bloc.',
     ['A shift from low-cost non-member imports to higher-cost member imports', 'An increase in tariffs on non-members', 'The creation of a new trading bloc']),
    ('What is meant by trade diversion?', 'A shift from lower-cost imports from non-members to higher-cost imports from bloc members', 'Caused by the common external tariff.',
     ['A shift from domestic production to imports from members', 'A fall in total world trade', 'The removal of all tariffs worldwide']),
    ('Which is a main function of the World Trade Organization (WTO)?', 'Negotiating reductions in trade barriers and settling trade disputes', 'Rules-based trading system.',
     ['Setting exchange rates between currencies', 'Lending to countries with balance of payments problems', 'Setting interest rates for member countries']),
    ('Which feature is found in an economic union but not in a common market?', 'A single currency and harmonised economic policies', 'Deepest form of integration.',
     ['Free trade between members', 'A common external tariff', 'Free movement of labour and capital']),
    ('Why do free trade areas need rules of origin?', 'To stop non-member goods entering through the member with the lowest external tariff', 'Prevents trade deflection.',
     ['To set a common external tariff', 'To control the movement of labour', 'To decide the bloc’s single currency']),
    ('The WTO principle of ‘most favoured nation’ means that', 'a trade concession given to one member must be given to all members', 'Non-discrimination.',
     ['members must trade only with the largest economies', 'each member can choose its own tariffs on different members', 'developing countries must remove all tariffs']),
])
ex(t25_4, [
    ('Explain the difference between trade creation and trade diversion.', 'Trade creation: joining a bloc replaces high-cost domestic production with lower-cost imports from members (efficiency gain). Trade diversion: the common external tariff causes imports to switch from lower-cost non-members to higher-cost members (efficiency loss).',
     '1 mark: trade creation explained; 1 mark: trade diversion explained; 1 mark: efficiency gain vs loss [3]'),
    ('Explain two benefits to a country of joining a customs union.', 'Tariff-free access to a larger market (exports, economies of scale); greater competition raises efficiency; trade creation lowers prices; more FDI; greater bargaining power in trade negotiations.',
     '1 mark each for two benefits, 1 mark each for explanation [4]'),
    ('Explain why the WTO may find it difficult to achieve free trade.', 'Decisions need consensus among many members with conflicting interests; governments face domestic pressure to protect industries; disputes over agriculture subsidies and developing-country exemptions.',
     '1 mark: consensus/conflicting interests; 1 mark: domestic political pressure or example [2]'),
    ('Explain why joining a trading bloc may reduce a country’s economic welfare.', 'If trade diversion outweighs trade creation, consumers pay more for imports from higher-cost members, and the government loses tariff revenue; members may also lose policy independence.',
     '1 mark: trade diversion; 1 mark: higher cost/loss of revenue or sovereignty [2]'),
])
errs(t25_4, [
    ('Members of a free trade area all charge the same tariff on imports from outside the area.', 'That is a customs union; FTA members keep their own external tariffs, which is why rules of origin are needed.'),
    ('Joining a customs union always increases efficiency because tariffs are removed.', 'Removing internal tariffs can cause trade creation, but the common external tariff can cause trade diversion to higher-cost members, reducing efficiency.'),
    ('The WTO sets the tariffs that each country must charge.', 'The WTO provides rules and a forum for negotiating tariff reductions and settling disputes; members agree their own maximum (bound) tariffs.'),
])
classify(t25_4, BLOC_CASES, BLOC_LABELS, 'What type of trading bloc is described?', 'For each arrangement, identify the type of trading bloc and explain your answer.', extra=['World Trade Organization'], C='C3', name='bloc')


@t25_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t25_4_div(r, D):
    c, cp, cw = r.sample(COUNTRIES, 3)
    g = r.choice(MGOODS)
    w = r.choice([40, 50, 60, 80, 100])
    tar = r.choice([20, 25, 30, 40])
    p = w + r.choice([5, 8, 10, 12]) * w // 100 * 1
    p = round(w * (1 + r.choice([5, 10, 15]) / 100))
    q = r.choice([10, 20, 50])         # thousand units imported
    pw = w * (1 + tar / 100)
    pp = p * (1 + tar / 100)
    stem = (f'{c} imports {g}. Before joining a customs union, {c} charged a {tar}% tariff on all imports. {cw} (outside the union) supplies {g} at ${w} per unit and {cp} (a union partner) at ${p} per unit. '
            f'After joining, imports from {cp} are tariff-free, while the common external tariff on {cw} stays at {tar}%.')
    if D <= 2:
        return cq(r, 1, stem + f' After {c} joins, what is the price of {g} imported from {cw}?', money(pw), f'{w} × {1 + tar / 100} = {money(pw)}.',
                  dis_num(r, pw, money, [w, pp, p]), mcq_D=(1, 2))
    ans = (f'(a) Before: {cw} ${w} + {tar}% = {money(pw)}; {cp} {money(pp)}; buys from {cw} at {money(pw)}. After: {cp} ${p} (no tariff) vs {cw} {money(pw)}, so imports switch to {cp}. '
           f'(b) Trade diversion: imports switch from the lower-cost producer ({cw}, ${w}) to a higher-cost member ({cp}, ${p}). ')
    rev = q * w * tar / 100
    if D == 3:
        return {'stem': stem + f' (a) Identify where {c} buys {g} before and after joining, showing the prices. (b) State whether this is trade creation or trade diversion and explain.',
                'answer': ans, 'key': '(a) prices and source before [1]; after [1] (b) trade diversion [1]; higher-cost source explained [1] [4]', 'marks': 4, 'type': 'numerical'}
    return {'stem': stem + f' {c} imports {q},000 units a year. (a) Identify where {c} buys {g} before and after joining, showing the prices. (b) State whether this is trade creation or trade diversion and explain. '
                    f'(c) Calculate the tariff revenue lost by the government of {c} (assume quantity unchanged) and the saving to consumers. (d) Discuss whether joining the customs union is likely to benefit {c} overall.',
            'answer': ans + f'(c) Tariff revenue lost = {q},000 × ${num(w * tar / 100, 2)} = {money(rev * 1000)}; consumers save {money(pw - p)} per unit = {money((pw - p) * q * 1000)}. '
                      f'(d) Consumers gain from lower prices, but the government loses more revenue than consumers save (the difference reflects the higher real cost of {cp}’s supply); there may be trade creation in other goods, a larger export market, economies of scale and FDI; judgement.',
            'key': '(a) [2] (b) [2] (c) revenue lost [1]; consumer saving [1] (d) evaluation [2] [8]', 'marks': 8, 'type': 'numerical'}


def _ch25_case(r, D):
    c1, c2, gx, gy, ux, uy, a1, b1, a2, b2 = _ca_data(r)
    px = r.choice([92, 96, 105, 110, 118])
    pm = r.choice([94, 100, 108, 112])
    intro = (f'Extract: {c1} and {c2} are negotiating a free trade agreement. One worker in {c1} can produce {a1} {ux} or {b1} {uy} a week; one worker in {c2} can produce {a2} {ux} or {b2} {uy}. '
             f'Over the last five years {c1}’s export price index has moved to {px} and its import price index to {pm} (base year = 100). Trade unions in {c1} fear job losses in its {gx if b1 / a1 > b2 / a2 else gy} industry, '
             'while business groups argue that tariff-free access to a larger market will bring economies of scale. Both countries are members of the WTO.')
    cx = c1 if b1 / a1 < b2 / a2 else c2
    parts = [
        lambda r: (f'Calculate the opportunity cost of 1 unit of {gx} in each country.', f'{c1}: {_oc(b1, a1)} {uy}; {c2}: {_oc(b2, a2)} {uy}.', '[2]'),
        lambda r: (f'Using opportunity costs, explain which country has a comparative advantage in {gx}.', f'{cx}, because it has the lower opportunity cost of {gx} ({c1}: {_oc(b1, a1)}, {c2}: {_oc(b2, a2)} {uy} per unit).', '[2]'),
        lambda r: (f'Calculate {c1}’s terms of trade index and state whether it has improved since the base year.', f'{px}/{pm} × 100 = {num(100 * px / pm, 1)}; {tot_word(100 * px / pm)}.', '[2]'),
        lambda r: ('Explain why trade unions fear job losses.', 'Resources move out of the industry with comparative disadvantage; cheaper imports replace domestic output; workers may be occupationally immobile.', '[3]'),
        lambda r: ('Explain the difference between a free trade area and a customs union.', 'An FTA removes internal tariffs only; a customs union also has a common external tariff.', '[2]'),
        lambda r: (f'Discuss whether {c1} should sign the free trade agreement.', 'Gains: specialisation, lower prices, economies of scale, competition, FDI. Costs: structural unemployment, adjustment costs, over-specialisation, possible trade diversion; depends on size of gains, mobility of labour and support for displaced workers; judgement.', '[6]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t25_1, t25_2, t25_3, t25_4], _ch25_case)
TRADE_SCENES = ['{country} is a lower-middle-income economy that exports agricultural goods and imports most of its manufactured goods.',
                '{country} has recently signed several trade agreements with its neighbours.', 'Exports account for 45% of the GDP of {country}.']
essay(t25_1, [
    ('Explain, using a numerical example or diagram, the difference between absolute and comparative advantage.',
     'Definitions; two-country two-good example or PPCs with different slopes; opportunity cost ratios; a country with absolute advantage in both goods still gains by specialising in its lower-OC good.',
     'the theory of comparative advantage explains the pattern of trade of {country}',
     'Factor endowments give low opportunity costs; specialisation and exchange raise consumption; explains much trade in primary and labour-intensive goods.',
     'Unrealistic assumptions (constant costs, no transport costs, factor mobility); much trade is intra-industry between similar countries, driven by economies of scale and product differentiation; protection and history matter.'),
    ('Explain why a country may gain from specialising according to comparative advantage even if it has an absolute disadvantage in all goods.',
     'Opportunity costs differ; specialising in the good with the smaller disadvantage; trade at terms between OC ratios; consumption beyond PPC.',
     'countries should always specialise according to comparative advantage',
     'Increases world output and consumption; efficiency; lower prices.',
     'Risk of over-specialisation and volatile prices; comparative advantage may be dynamic and can be developed; strategic and security concerns; structural unemployment.'),
], TRADE_SCENES)
essay(t25_2, [
    ('Explain the benefits of free trade and specialisation for an economy.',
     'Higher output through comparative advantage, lower prices and more choice, economies of scale, competition and efficiency, technology transfer.',
     'free trade benefits all groups in {country}',
     'Consumers gain lower prices and choice; exporters gain markets; efficiency rises.',
     'Import-competing workers and firms lose; adjustment costs and structural unemployment; over-specialisation risk; gains unevenly distributed; depends on compensation and mobility.'),
], TRADE_SCENES)
essay(t25_3, [
    ('Explain how the terms of trade are measured and two causes of a change in the terms of trade.',
     'ToT = Px index / Pm index × 100; causes: world demand/supply shifts for exports or imports, exchange rate changes, relative inflation, productivity.',
     'an improvement in the terms of trade is always beneficial for {country}',
     'More imports for a given quantity of exports; higher real income; demand-led rises raise export revenue.',
     'If caused by inflation or appreciation, competitiveness falls; with elastic demand, export revenue and jobs fall; depends on cause and PED.'),
], TRADE_SCENES)
essay(t25_4, [
    ('Explain the differences between a free trade area, a customs union and an economic union.',
     'FTA: no internal tariffs, own external tariffs, rules of origin; customs union adds common external tariff; common market adds factor mobility; economic union adds single currency and harmonised policies.',
     'joining a customs union will benefit {country}',
     'Trade creation, larger market, economies of scale, competition, FDI, bargaining power.',
     'Trade diversion, loss of tariff revenue, loss of trade policy independence, competition harms weaker firms; depends on the size of creation vs diversion and on the partners.'),
    ('Explain the role of the WTO in promoting international trade.',
     'Negotiating rounds to cut tariffs; non-discrimination (MFN, national treatment); dispute settlement; monitoring; special treatment for developing countries.',
     'the WTO has been more successful than trading blocs in promoting free trade',
     'Global, non-discriminatory reductions avoid trade diversion; dispute settlement gives rules-based system.',
     'Slow consensus and stalled rounds; blocs achieve deeper integration faster; disputes over agriculture; judgement depends on the measure of success.'),
], TRADE_SCENES)
CHAPTERS[25] = [t25_1, t25_2, t25_3, t25_4]

# ============================================================================ 26 Protectionism
PROT_CASES = [
    ('The government of {country} adds a 25% tax to the price of imported {mgood}.', 'Tariff', 'a tax on imports raises their price.'),
    ('{country} limits imports of {mgood} to 50,000 units a year.', 'Quota', 'a physical limit on the quantity imported.'),
    ('{country} bans all trade with {country2} after a political dispute.', 'Embargo', 'a complete ban on trade with a country or in a good.'),
    ('The government of {country} pays domestic {mgood} producers $15 per unit produced.', 'Subsidy to domestic producers', 'lowers domestic firms’ costs so they can compete with imports.'),
    ('{country} requires all imported {mgood} to pass lengthy safety tests that domestic products do not face.', 'Administrative barrier', 'red tape and standards that make importing costly or slow.'),
    ('Imports of {mgood} into {country} must enter through one small port with slow customs checks.', 'Administrative barrier', 'bureaucratic procedures raise the cost of importing.'),
    ('{country} prohibits imports of {mgood2} from {country2} for five years.', 'Embargo', 'a ban on imports of a product from a country.'),
    ('The government of {country} allows only 2,000 tonnes of foreign rice to be imported each year.', 'Quota', 'a quantity limit on imports.'),
]
PROT_LABELS = ['Tariff', 'Quota', 'Embargo', 'Subsidy to domestic producers', 'Administrative barrier']


def _tariff(r):
    """Linear domestic market with world price Pw and specific tariff T. Quantities in thousands."""
    for _ in range(80):
        pw = r.choice([4, 5, 6, 8, 10, 12])
        T = r.choice([1, 2, 3]) * (2 if pw >= 8 else 1)
        b, d = r.choice([2, 3, 4, 5, 6]), r.choice([2, 3, 4, 5])
        c = r.choice([-10, -5, 0, 5, 10])
        if c + d * pw <= 2:
            continue
        m1 = r.choice([10, 15, 20, 25, 30, 40])
        a = c + d * (pw + T) + b * (pw + T) + m1
        qd0, qs0 = a - b * pw, c + d * pw
        qd1, qs1 = a - b * (pw + T), c + d * (pw + T)
        if qs1 >= qd1 or qs0 <= 0:
            continue
        return pw, T, a, b, c, d, qd0, qs0, qd1, qs1
    return None


METHODS = ['tariff', 'quota']
t26_1 = T('Methods of protection: tariffs, quotas, embargoes, subsidies and administrative barriers', 'methods of protection', 'tariffs, quotas', 'embargoes, subsidies', 'administrative barriers')
mc(t26_1, [
    ('What is a tariff?', 'A tax on imported goods', 'Raises the price of imports.', ['A limit on the quantity of imports', 'A ban on imports', 'A payment to exporters']),
    ('What is an import quota?', 'A physical limit on the quantity of a good that can be imported', 'Restricts quantity, not price directly.', ['A tax on imports', 'A complete ban on imports', 'A subsidy to domestic producers']),
    ('What is an embargo?', 'A complete ban on trade in a good or with a country', 'The most extreme form of protection.', ['A tax on imports', 'A quota on imports', 'A minimum price for imports']),
    ('Which method of protection raises revenue for the government?', 'A tariff', 'Tariff revenue = tariff per unit × imports.', ['An import quota', 'An embargo', 'A production subsidy']),
    ('Which is an example of an administrative barrier to trade?', 'Complex customs procedures and product standards applied to imports', 'Red tape raises the cost of importing.',
     ['A 10% tax on imports', 'A limit of 1,000 imported cars a year', 'A government payment to domestic farmers']),
    ('How does a subsidy to domestic producers protect them from imports?', 'It lowers their costs, so they can sell at prices that compete with imports', 'Shifts domestic supply right.',
     ['It raises the price of imports', 'It limits the quantity of imports', 'It bans imports completely']),
    ('Who may receive the extra revenue from an import quota?', 'Foreign exporters or licence holders who can sell at the higher domestic price', 'Quota rent; no tariff revenue.',
     ['The government, as tariff revenue', 'Domestic consumers', 'No one, because prices fall']),
])
ex(t26_1, [
    ('Explain the difference between a tariff and a quota.', 'A tariff is a tax on imports that raises their price and earns revenue; a quota is a limit on the quantity imported, which raises the domestic price but earns the government no revenue (unless licences are sold).',
     '1 mark: tariff tax/price/revenue; 1 mark: quota quantity limit/no revenue [2]'),
    ('Explain, with the help of a diagram, how a tariff affects domestic production and imports.', 'The tariff raises the domestic price from Pw to Pw + t; domestic quantity supplied rises along the supply curve, quantity demanded falls, so imports (the gap) fall.',
     '1 mark: price rises by tariff; 1 mark: domestic output rises; 1 mark: demand falls and imports fall [3]'),
    ('Explain why a production subsidy may be a less harmful form of protection than a tariff.', 'Consumers still pay the world price, so consumption is not reduced; the cost is borne by taxpayers and is visible, though it has an opportunity cost.',
     '1 mark: consumers still pay world price; 1 mark: cost to taxpayers/opportunity cost [2]'),
    ('Explain how administrative barriers can act as protection even though they are not taxes.', 'Paperwork, inspections and special standards raise foreign firms’ costs and delay imports, discouraging them in favour of domestic goods.',
     '1 mark: raise costs/delays for importers; 1 mark: favour domestic producers [2]'),
])
classify(t26_1, PROT_CASES, PROT_LABELS, 'Which method of protection is this?', 'Identify the method of protection in each case and explain how it protects domestic producers.', name='prot')
errs(t26_1, [
    ('A quota raises revenue for the government in the same way as a tariff.', 'A quota limits quantity; the higher price benefits licence holders or foreign exporters, so the government earns no revenue unless it sells import licences.'),
    ('A tariff lowers the price that domestic consumers pay for imported {mgood}.', 'A tariff raises the domestic price of imports, so consumers pay more and buy less.'),
    ('A subsidy to domestic producers is not a form of protection because it does not affect imports.', 'Subsidies lower domestic firms’ costs and prices, so domestic output replaces imports; this protects domestic producers.'),
])
items(t26_1, 'C2', (1, 2, 3, 4), [
    ('{country} replaces its 20% tariff on imported {mgood} with a quota that allows the same quantity of imports. Explain one difference this makes.',
     'The domestic price and quantity of imports may be the same, but the government loses tariff revenue; the gain goes to licence holders or foreign exporters as quota rent.',
     '1 mark: same price/quantity; 1 mark: revenue goes to licence holders not government [2]'),
    ('Explain why {country}’s domestic producers of {mgood} might prefer a quota to a tariff.', 'A quota fixes the maximum imports, so domestic producers are protected even if world prices fall or demand rises; a tariff allows imports to rise.',
     '1 mark: quota certain limit; 1 mark: tariff allows more imports if world price falls [2]'),
], name='prot_items')


@t26_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t26_1_tariff(r, D):
    v = _tariff(r)
    if not v:
        return None
    pw, T, a, b, c, d, qd0, qs0, qd1, qs1 = v
    c_ = r.choice(COUNTRIES)
    g = r.choice(MGOODS)
    stem = (f'In {c_}, the domestic demand for {g} is {qd_s(a, b)} and domestic supply is {qs_s(c, d)}, where P is the price in dollars and Q is in thousands of units a year. '
            f'{c_} can import any quantity at the world price of ${pw}. The government imposes a tariff of ${T} per unit.')
    m0, m1 = qd0 - qs0, qd1 - qs1
    rev = T * m1
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the quantity imported after the tariff.', f'{num(m1)} thousand units', f'At ${pw + T}: Qd = {num(qd1)}, Qs = {num(qs1)}; imports = {num(m1)} thousand.',
                  dis_num(r, m1, lambda x: f'{num(x)} thousand units', [m0, qd1, qd0 - qs1]), mcq_D=(1, 2))
    a_txt = (f'Before: P = ${pw}, Qd = {num(qd0)}, Qs = {num(qs0)}, imports = {num(m0)} thousand. After: P = ${pw + T}, Qd = {num(qd1)}, Qs = {num(qs1)}, imports = {num(m1)} thousand.')
    if D == 3:
        return {'stem': stem + ' (a) Calculate domestic production and imports before and after the tariff. (b) Calculate the government’s tariff revenue.',
                'answer': f'(a) {a_txt} (b) {T} × {num(m1)} thousand = {kd(rev)}.', 'key': '(a) before [1]; after [2] (b) revenue [1] [4]', 'marks': 4, 'type': 'numerical'}
    cl = T * (qd0 + qd1) / 2
    pg = T * (qs0 + qs1) / 2
    dwl = cl - pg - rev
    base = f'(a) {a_txt} (b) Tariff revenue = ${T} × {num(m1)} thousand = {kd(rev)}. '
    if D == 4:
        return {'stem': stem + ' (a) Calculate domestic production, consumption and imports before and after the tariff. (b) Calculate the tariff revenue. (c) Explain who gains and who loses from the tariff.',
                'answer': base + '(c) Domestic producers gain (higher price and output); the government gains revenue; consumers lose (higher price, lower consumption); foreign exporters lose sales; there is a net welfare loss.',
                'key': '(a) [3] (b) [1] (c) gainers [1]; losers [1] [6]', 'marks': 6, 'type': 'numerical'}
    return {'stem': stem + ' (a) Calculate domestic production, consumption and imports before and after the tariff. (b) Calculate the tariff revenue. (c) Calculate the loss of consumer surplus, the gain in producer surplus and the deadweight welfare loss. (d) Evaluate whether the tariff is justified.',
            'answer': base + f'(c) Consumer surplus loss = {T} × ({num(qd0)} + {num(qd1)})/2 thousand = {kd(cl)}; producer surplus gain = {T} × ({num(qs0)} + {num(qs1)})/2 thousand = {kd(pg)}; '
                             f'deadweight loss = {kd(cl)} − {kd(pg)} − {kd(rev)} = {kd(dwl)}. (d) Saves domestic jobs and raises revenue, but consumers lose more than producers and government gain; risk of retaliation and inefficiency; may be justified temporarily for an infant industry; judgement.',
            'key': '(a) [3] (b) [1] (c) consumer surplus [1]; producer surplus [1]; deadweight loss [1] (d) evaluation [2] [9]', 'marks': 9, 'type': 'numerical'}


ARG_CASES = [
    ('{country} imposes tariffs on imported electric vehicles so that its new domestic producers can grow and gain economies of scale.', 'Infant industry argument', 'new firms need time to reach the scale and experience to compete.'),
    ('{country} restricts imports of steel from {country2}, which is selling steel below its cost of production.', 'Anti-dumping', 'protection against goods sold abroad below cost or below the home-market price.'),
    ('{country} protects its domestic food and energy producers so that it does not depend on imports in a crisis.', 'Strategic and national security argument', 'self-sufficiency in essential goods reduces vulnerability.'),
    ('{country} imposes a tariff on imported {mgood} to save jobs in a region with high unemployment.', 'Protecting employment', 'imports replaced by domestic output preserve jobs.'),
    ('{country} uses import tariffs to reduce a large current account deficit.', 'Correcting a current account deficit', 'lower imports reduce the deficit, at least in the short run.'),
    ('The government of {country} uses tariffs because it has difficulty collecting income tax.', 'Raising government revenue', 'tariffs are easy to collect at the border.'),
    ('{country} gives temporary protection to its coal industry while workers retrain.', 'Protecting a declining industry', 'slows the pace of structural change to reduce unemployment.'),
]
ARG_LABELS = ['Infant industry argument', 'Anti-dumping', 'Strategic and national security argument', 'Protecting employment', 'Correcting a current account deficit',
              'Raising government revenue', 'Protecting a declining industry']

t26_2 = T('Arguments for protectionism', 'arguments for protectionism', 'infant industry', 'dumping')
mc(t26_2, [
    ('What is the infant industry argument for protection?', 'New industries need temporary protection until they are large enough to compete', 'Grow to achieve economies of scale.',
     ['Old industries should be protected permanently', 'Children’s goods should be exempt from tariffs', 'All industries need protection from imports']),
    ('What is meant by dumping?', 'Selling goods abroad at a price below cost or below the price in the home market', 'Unfair competition.',
     ['Selling goods at a high price abroad', 'Disposing of waste products in another country', 'Exporting goods of low quality']),
    ('Which is a strategic argument for protection?', 'A country should produce its own food and defence equipment to avoid dependence on others', 'National security.',
     ['Imports are always of lower quality', 'Consumers prefer domestic goods', 'Tariffs reduce government revenue']),
    ('Why might a developing country use tariffs to raise revenue?', 'Tariffs are easier to collect than income tax', 'Few collection points at borders.',
     ['Tariffs are paid by foreign governments', 'Tariffs have no effect on prices', 'Tariffs increase imports']),
    ('Which argument is used to justify protecting a declining industry?', 'It slows the loss of jobs while workers retrain and move', 'Reduces adjustment costs.',
     ['It allows the industry to become a world leader', 'It raises world efficiency', 'It reduces prices for consumers']),
    ('Why might protection be used to correct a current account deficit?', 'Restricting imports reduces spending on foreign goods', 'Expenditure switching.',
     ['It raises the value of exports automatically', 'It increases imports of raw materials', 'It causes the currency to appreciate']),
])
ex(t26_2, [
    ('Explain the infant industry argument for protection.', 'New firms have high average costs because they are small and inexperienced; temporary protection lets them grow, gain economies of scale and learning, and then compete internationally, after which protection should be removed.',
     '1 mark: high costs of new firms; 1 mark: grow/economies of scale; 1 mark: temporary [3]'),
    ('Explain why a country might protect its industries against dumping.', 'Dumped goods sold below cost can drive efficient domestic firms out of business; foreign firms may then raise prices once competition is removed.',
     '1 mark: below-cost price harms domestic firms; 1 mark: threat of later monopoly pricing/unfair competition [2]'),
    ('Explain two arguments for protection that a low-income country might use.', 'Infant industry (develop new manufacturing); revenue (tariffs easy to collect); protecting employment; diversification away from primary exports; strategic food security.',
     '1 mark each for two arguments, 1 mark each for explanation [4]'),
])
classify(t26_2, ARG_CASES, ARG_LABELS, 'Which argument for protection is being used?', 'Identify the argument for protection in each case and explain it.', name='arg')
errs(t26_2, [
    ('The infant industry argument means an industry should be protected permanently.', 'Protection should be temporary, until the industry has grown and can compete; permanent protection removes the incentive to become efficient.'),
    ('Dumping means selling poor-quality goods abroad.', 'Dumping is selling goods abroad at a price below cost or below the home-market price.'),
    ('Protection always saves jobs in {country} overall.', 'It may save jobs in protected industries, but jobs can be lost in export industries (retaliation) and in firms using imported inputs.'),
])
items(t26_2, 'C2', (1, 2, 3, 4), [
    ('{country} wants to develop a domestic {mgood} industry. Explain why it might use protection, and what conditions would make this successful.',
     'Infant industry: temporary protection while firms grow and gain economies of scale. It works only if protection is time-limited, firms invest and become efficient, and there is a real potential comparative advantage.',
     '1 mark: infant industry; 1 mark: condition (temporary/potential CA/investment) [2]'),
    ('Foreign firms are selling {mgood} in {country} at prices below what they charge at home. Explain why {country} might impose an anti-dumping duty.',
     'Below-cost imports may drive efficient domestic producers out; the duty restores fair competition and prevents a later foreign monopoly.',
     '1 mark: unfair competition/harm to domestic firms; 1 mark: duty restores fair price [2]'),
], name='arg_items')


@t26_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t26_2_job(r, D):
    c = r.choice(COUNTRIES)
    g = r.choice(MGOODS)
    cost = r.choice([120, 150, 200, 240, 300, 360])          # $m a year extra cost to consumers
    jobs = r.choice([1500, 2000, 2400, 3000, 4000])
    wage = r.choice([18000, 22000, 25000, 30000])
    per = cost * 1e6 / jobs
    stem = f'A tariff on imported {g} in {c} raises consumers’ spending on {g} by ${cost}m a year and is estimated to save {jobs:,} jobs in domestic factories. The average wage in the industry is ${wage:,} a year.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the cost to consumers of each job saved.', money(per, dp=0), f'{cost}m ÷ {jobs:,} = {money(per, dp=0)}.',
                  dis_num(r, per, lambda x: money(round(x)), [per / 10, wage]), mcq_D=(1, 2))
    rat = per / wage
    if D == 3:
        return {'stem': stem + ' (a) Calculate the cost to consumers of each job saved. (b) Compare this with the average wage and comment.',
                'answer': f'(a) ${cost}m / {jobs:,} = {money(round(per))}. (b) This is {num(rat, 1)} times the average wage, so it would be cheaper to pay the workers’ wages directly or to fund retraining; protection is a costly way to save jobs.',
                'key': '(a) [2] (b) comparison [1]; comment [1] [4]', 'marks': 4, 'type': 'numerical'}
    return {'stem': stem + ' (a) Calculate the cost to consumers of each job saved and compare it with the average wage. (b) Explain two other costs of the tariff not included in this figure. (c) Discuss whether saving these jobs justifies the tariff.',
            'answer': f'(a) {money(round(per))}, {num(rat, 1)} times the average wage. (b) Retaliation against {c}’s exports; higher costs for firms using {g}; reduced competition and efficiency; deadweight loss. '
                      '(c) Jobs are concentrated in particular regions and unemployment has social costs; but the cost per job is high, other jobs may be lost, and retraining or regional policy may be cheaper; temporary protection may be justified if the industry can become competitive; judgement.',
            'key': '(a) calculation [1]; comparison [1] (b) two costs [2] (c) evaluation [3] [7]', 'marks': 7, 'type': 'numerical'}


@t26_2.add('C3', (2, 3, 4), 'numerical')
def t26_2_dump(r, D):
    c, c2 = r.sample(COUNTRIES, 2)
    g = r.choice(MGOODS)
    home = r.choice([80, 100, 120, 150])
    cost = round(home * r.choice([0.8, 0.85, 0.9]))
    exp = round(cost * r.choice([0.7, 0.75, 0.8]))
    duty = home - exp
    stem = f'A producer in {c2} sells {g} for ${home} per unit in its home market, its average cost is ${cost}, and it sells to {c} at ${exp} per unit.'
    if D == 2:
        return cq(r, 2, stem + f' {c} sets an anti-dumping duty equal to the difference between the home-market price and the export price. What duty per unit is set?', money(duty),
                  f'{home} − {exp} = {money(duty)}.', dis_num(r, duty, money, [cost - exp, home - cost]), mcq_D=(2,))
    return {'stem': stem + f' (a) Explain why this is dumping. (b) Calculate the anti-dumping duty needed to raise the price to the home-market level and the loss per unit made by the exporter on sales to {c}. '
                    + ('(c) Explain why the exporter might be willing to sell at a loss.' if D == 4 else ''),
            'answer': f'(a) It sells in {c} below its home price (${home}) and below average cost (${cost}). (b) Duty = ${home} − ${exp} = {money(duty)}; loss per unit = ${cost} − ${exp} = {money(cost - exp)}. '
                      + ('(c) To win market share and drive out rivals, to dispose of surplus output, or because it is subsidised by its government; it may raise prices later.' if D == 4 else ''),
            'key': '(a) [1] (b) duty [1]; loss [1]' + (' (c) [2] [5]' if D == 4 else ' [3]'), 'marks': 5 if D == 4 else 3, 'type': 'numerical'}


CONS_CASES = [
    ('After {country} puts tariffs on imported {mgood}, {country2} responds with tariffs on {country}’s exports of {mgood2}.', 'Retaliation', 'trading partners impose their own barriers, so exporters lose.'),
    ('Car makers in {country} face higher costs after tariffs are imposed on imported steel.', 'Higher costs for firms using imported inputs', 'protection raises input costs and lowers competitiveness.'),
    ('Protected {mgood} producers in {country} stop investing in new technology.', 'Reduced efficiency and innovation', 'without competition, there is less incentive to cut costs.'),
    ('Consumers in {country} pay 30% more for {mgood} after an import quota is introduced.', 'Higher prices and less choice for consumers', 'protection raises prices and reduces consumer surplus.'),
    ('World trade falls as several countries raise tariffs at the same time.', 'Lower world output and trade', 'gains from specialisation are lost.'),
    ('Protected firms in {country} lobby the government to keep tariffs long after they were meant to end.', 'Protection becomes permanent (government failure)', 'vested interests make removal difficult.'),
]
CONS_LABELS = ['Retaliation', 'Higher costs for firms using imported inputs', 'Reduced efficiency and innovation', 'Higher prices and less choice for consumers',
               'Lower world output and trade', 'Protection becomes permanent (government failure)']

t26_3 = T('Arguments against protectionism and its consequences', 'arguments against protectionism', 'consequences of protectionism', 'retaliation')
mc(t26_3, [
    ('Which is an argument against protection?', 'It may lead to retaliation by other countries', 'Trade wars reduce exports.', ['It increases government revenue', 'It protects infant industries', 'It reduces imports']),
    ('How does protection affect consumers?', 'They pay higher prices and have less choice', 'Consumer surplus falls.', ['They pay lower prices', 'They have more choice', 'They are unaffected']),
    ('Why might protection reduce the efficiency of domestic firms?', 'They face less competition, so have less incentive to cut costs', 'X-inefficiency.',
     ['They must compete harder with imports', 'They face higher demand for exports', 'They have to pay higher tariffs']),
    ('A tariff on imported components would most likely', 'raise costs for domestic firms that use those components', 'Inputs dearer, competitiveness falls.',
     ['lower costs for all domestic firms', 'raise demand for the country’s exports', 'improve the competitiveness of exporters']),
    ('What is the deadweight loss of a tariff?', 'The loss of welfare from inefficient domestic production and reduced consumption', 'Loss not gained by anyone.',
     ['The revenue raised by the government', 'The gain to domestic producers', 'The fall in imports']),
    ('Why is protection said to misallocate resources?', 'Resources are kept in industries where the country does not have a comparative advantage', 'Departure from comparative advantage.',
     ['Resources move into export industries', 'All resources become unemployed', 'Imports always increase']),
])
ex(t26_3, [
    ('Explain how protection can lead to a misallocation of resources.', 'It keeps resources in high-cost domestic industries where the country lacks comparative advantage, rather than moving them to more efficient uses; world output is lower.',
     '1 mark: resources in comparative-disadvantage industries; 1 mark: lower total/world output [2]'),
    ('Explain two consequences of a trade war for a country’s economy.', 'Exports fall as partners retaliate, reducing output and employment in export industries; import prices rise, raising inflation and costs of inputs; lower growth.',
     '1 mark each for two consequences, 1 mark each for explanation [4]'),
    ('Explain why protection may not improve the current account in the long run.', 'Retaliation reduces exports; higher input costs and lower efficiency reduce export competitiveness; the currency may appreciate as imports fall.',
     '1 mark: retaliation/exports fall; 1 mark: competitiveness falls [2]'),
])
classify(t26_3, CONS_CASES, CONS_LABELS, 'Which consequence of protectionism does this illustrate?', 'Identify the consequence of protection in each case and explain it.', name='cons')
errs(t26_3, [
    ('A tariff makes everyone in {country} better off because domestic firms sell more.', 'Producers and the government gain, but consumers lose more than they gain, so there is a net deadweight loss; exporters may lose through retaliation.'),
    ('Protecting the steel industry in {country} will make all manufacturers more competitive.', 'Firms that use steel face higher input costs, so their competitiveness falls.'),
    ('Protection has no effect on other countries.', 'Foreign exporters lose sales and income, and may persuade their governments to retaliate.'),
])
items(t26_3, 'C2', (1, 2, 3, 4), [
    ('{country} imposed a 25% tariff on imported {mgood} five years ago. Domestic producers have not cut costs since then. Explain why.',
     'With protection from foreign competition, firms can survive with high costs; there is little incentive to innovate (X-inefficiency) and they may lobby to keep the tariff.',
     '1 mark: reduced competition; 1 mark: no incentive to cut costs/X-inefficiency [2]'),
    ('{country2} retaliates against {country}’s tariffs by taxing {country}’s exports of {mgood2}. Explain the likely effect on {country}’s economy.',
     'Exports of {mgood2} fall, reducing output, income and employment in that industry and worsening the current account; the multiplier spreads the effect.',
     '1 mark: exports fall; 1 mark: effect on income/jobs/current account [2]'),
], name='cons_items')


@t26_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t26_3_input(r, D):
    c = r.choice(COUNTRIES)
    steel = r.choice([600, 700, 800, 900])        # $ per tonne
    tonnes = r.choice([0.8, 1.2, 1.5])
    tar = r.choice([10, 20, 25, 30])
    price = r.choice([18000, 20000, 25000])
    extra = steel * tonnes * tar / 100
    pc = 100 * extra / price
    ped = r.choice([1.5, 2.0, 2.5])
    stem = (f'Car makers in {c} use {num(tonnes, 1)} tonnes of imported steel per car, at ${steel} per tonne. The government imposes a {tar}% tariff on imported steel. The average car sells for ${price:,}.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the increase in the steel cost of each car.', money(extra), f'{num(tonnes, 1)} × {steel} × {tar}% = {money(extra)}.',
                  dis_num(r, extra, money, [steel * tar / 100, steel * tonnes]), mcq_D=(1, 2))
    a = f'Extra cost = {num(tonnes, 1)} × ${steel} × {tar}% = {money(extra)} per car, {num(pc, 2)}% of the price.'
    if D == 3:
        return {'stem': stem + ' (a) Calculate the increase in the steel cost of each car and express it as a percentage of the car price. (b) Explain one effect on the car makers.',
                'answer': f'(a) {a} (b) Higher costs reduce profit margins or force higher prices, making exports less competitive.', 'key': '(a) cost [1]; percentage [1] (b) [1] [3]', 'marks': 3, 'type': 'numerical'}
    dq = ped * pc
    return {'stem': stem + f' (a) Calculate the increase in the steel cost of each car and express it as a percentage of the car price. (b) The car makers pass on the full increase. The price elasticity of demand for their cars abroad is −{num(ped, 1)}. Calculate the percentage change in export sales. '
                    f'(c) Explain why this tariff might reduce employment in {c} overall' + (', and discuss whether the steel tariff is justified.' if D == 5 else '.'),
            'answer': f'(a) {a} (b) %ΔQ = −{num(ped, 1)} × {num(pc, 2)}% = −{num(dq, 2)}%. (c) Jobs saved in steel may be outweighed by jobs lost in car making and other steel-using industries, and by retaliation. '
                      + ('Evaluation: depends on numbers employed in each industry, elasticities, retaliation, strategic value of steel; judgement.' if D == 5 else ''),
            'key': '(a) [2] (b) [2] (c) [2]' + (' evaluation [2] [8]' if D == 5 else ' [6]'), 'marks': 8 if D == 5 else 6, 'type': 'numerical'}


def _ch26_case(r, D):
    v = _tariff(r)
    if not v:
        return None
    pw, T, a, b, c, d, qd0, qs0, qd1, qs1 = v
    dd = ctx(r)
    g = dd['mgood']
    intro = (f'Extract: Producers of {g} in {dd["country"]} say they cannot compete with cheap imports from {dd["country2"]}, which they accuse of dumping. At the world price of ${pw}, domestic firms supply {num(qs0)} thousand units '
             f'and consumers buy {num(qd0)} thousand. The government is considering a tariff of ${T} per unit, which would raise domestic output to {num(qs1)} thousand and cut consumption to {num(qd1)} thousand. '
             f'Economists warn that {dd["country2"]} might retaliate against {dd["country"]}’s exports of {dd["mgood2"]}.')
    parts = [
        lambda r: ('Calculate the change in imports caused by the tariff.', f'Before {num(qd0 - qs0)} thousand, after {num(qd1 - qs1)} thousand: a fall of {num(qd0 - qs0 - qd1 + qs1)} thousand.', '[2]'),
        lambda r: ('Calculate the tariff revenue.', f'${T} × {num(qd1 - qs1)} thousand = {kd(T * (qd1 - qs1))}.', '[1]'),
        lambda r: ('Explain what is meant by dumping.', 'Selling exports at a price below cost or below the home-market price.', '[2]'),
        lambda r: ('Using a diagram, explain the effect of the tariff on consumers and domestic producers.', 'Price rises from Pw to Pw + tariff; consumer surplus falls; producer surplus rises; domestic output rises and imports fall; deadweight loss triangles.', '[4]'),
        lambda r: ('Explain one reason why retaliation would harm the economy.', f'Exports of {dd["mgood2"]} fall, reducing income, jobs and the current account.', '[2]'),
        lambda r: ('Discuss whether the government should impose the tariff.', 'For: anti-dumping, jobs, revenue. Against: higher prices, deadweight loss, retaliation, inefficiency; anti-dumping duties through WTO rules may be better; judgement.', '[6]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t26_1, t26_2, t26_3], _ch26_case)
PROT_SCENES = ['{country} has a growing manufacturing sector but a large current account deficit.', 'Unemployment in the industrial regions of {country} is above 12%.',
               'The government of {country} is under pressure from domestic producers to restrict imports.']
essay(t26_1, [
    ('Explain, using a diagram, how a tariff affects the domestic market for an imported good.',
     'Price rises from Pw to Pw + t; domestic supply rises, demand falls, imports fall; tariff revenue rectangle; consumer surplus loss, producer surplus gain, deadweight loss.',
     'a quota is a better method of protection than a tariff for {country}',
     'Certain limit on imports regardless of world price; effective protection.',
     'No revenue for government, quota rents go abroad, can encourage corruption; tariffs more transparent and WTO-preferred; subsidies avoid higher consumer prices; judgement.'),
    ('Explain the different methods of protection a government could use to reduce imports.',
     'Tariffs, quotas, embargoes, subsidies to domestic producers, administrative barriers, exchange controls; how each works.',
     'subsidies to domestic producers are the least harmful form of protection',
     'Consumers still pay the world price; targeted; no deadweight loss on consumption.',
     'Opportunity cost of public funds, taxes needed; may be challenged under WTO rules; still inefficiency in production; judgement.'),
], PROT_SCENES)
essay(t26_2, [
    ('Explain two arguments that a country might use to justify protection.',
     'Infant industry; anti-dumping; strategic/national security; employment; current account; revenue; declining industries; each explained.',
     'the infant industry argument is a valid reason for {country} to protect its manufacturing industries',
     'Economies of scale and learning need time; diversification; successful examples of temporary protection.',
     'Hard to pick winners, protection becomes permanent, lobbying, inefficiency, retaliation; subsidies or credit may be better; judgement.'),
], PROT_SCENES)
essay(t26_3, [
    ('Explain the arguments against protectionism.',
     'Loss of gains from comparative advantage, higher prices and less choice, deadweight loss, inefficiency, retaliation, higher input costs.',
     'protectionism does more harm than good to {country}',
     'Deadweight loss, retaliation, higher costs, inefficiency, government failure.',
     'Short-run job protection, infant industries, anti-dumping, strategic goods; depends on type, duration and retaliation; judgement.'),
], PROT_SCENES)
CHAPTERS[26] = [t26_1, t26_2, t26_3]

# ============================================================================ 27 Current account of the balance of payments
CA_ITEMS = [
    ('A car maker in {country} sells vehicles to buyers in {country2}.', 'Trade in goods (credit)', 'export of goods brings money into {country}.'),
    ('Households in {country} buy {mgood} made in {country2}.', 'Trade in goods (debit)', 'import of goods means money leaves {country}.'),
    ('Tourists from {country2} spend their holidays in {city}, {country}.', 'Trade in services (credit)', 'spending by foreign tourists is an export of services.'),
    ('A firm in {country} pays a shipping company from {country2} to transport its goods.', 'Trade in services (debit)', 'buying transport services from abroad is an import of services.'),
    ('A multinational based in {country2} sends profits from its factory in {country} back to its head office.', 'Primary income (debit)', 'investment income paid to foreign owners.'),
    ('Workers from {country} employed abroad for less than a year are paid wages by foreign firms.', 'Primary income (credit)', 'compensation of employees earned abroad.'),
    ('The government of {country} receives interest on its loans to other governments.', 'Primary income (credit)', 'investment income received from abroad.'),
    ('Migrants from {country} living permanently in {country2} send money home to their families.', 'Secondary income (credit)', 'remittances are current transfers into {country}.'),
    ('The government of {country} gives foreign aid to {country2}.', 'Secondary income (debit)', 'a current transfer abroad with nothing received in return.'),
    ('An insurance company in {country} sells policies to firms in {country2}.', 'Trade in services (credit)', 'export of financial services.'),
]
CA_LABELS = ['Trade in goods (credit)', 'Trade in goods (debit)', 'Trade in services (credit)', 'Trade in services (debit)', 'Primary income (credit)', 'Primary income (debit)',
             'Secondary income (credit)', 'Secondary income (debit)']


def bn(x):
    return ('−' if x < 0 else '') + f'${num(abs(x), 2 if abs(x) < 10 else 1)}bn'


t27_1 = T('Components of the current account: trade in goods and services, primary and secondary income', 'components of the current account', 'trade in goods and services', 'primary and secondary income')
mc(t27_1, [
    ('What is the balance of payments?', 'A record of all financial transactions between residents of a country and the rest of the world over a period',
     'Current account, capital account and financial account.', ['A record of the government’s income and spending', 'The difference between exports and imports of goods only', 'The total debt owed by a country']),
    ('Which is included in primary income in the current account?', 'Profits and interest received on investments abroad', 'Investment income and compensation of employees.',
     ['Remittances from migrant workers', 'Spending by foreign tourists', 'Purchase of shares in a foreign company']),
    ('Which is included in secondary income in the current account?', 'Remittances sent home by migrant workers', 'Current transfers.',
     ['Interest paid on foreign loans', 'Exports of banking services', 'Profits sent home by foreign firms']),
    ('Spending by foreign tourists in a country is recorded as', 'a credit in trade in services', 'Tourism is an export of services.',
     ['a debit in trade in goods', 'a credit in secondary income', 'a credit in the financial account']),
    ('What is the balance of trade in goods?', 'The value of exports of goods minus the value of imports of goods', 'Also called the visible balance.',
     ['Exports of services minus imports of services', 'The current account balance', 'Primary income minus secondary income']),
    ('A foreign firm buys a factory in the country. Where is this recorded?', 'In the financial account', 'Foreign direct investment is a financial account item, not current account.',
     ['In trade in goods', 'In primary income', 'In secondary income']),
    ('Which would be a debit in the current account of a country?', 'Interest paid to foreign holders of its government bonds', 'Primary income outflow.',
     ['Exports of machinery', 'Foreign students paying fees to its universities', 'Remittances received from its citizens abroad']),
])
ex(t27_1, [
    ('Explain the difference between primary income and secondary income in the current account.', 'Primary income is income earned from factors of production abroad: wages, profits, interest and dividends. Secondary income is current transfers with nothing given in return, such as remittances and foreign aid.',
     '1 mark: primary = factor income with example; 1 mark: secondary = transfers with example [2]'),
    ('Explain why the export of a service is recorded as a credit in the current account.', 'Foreign residents pay for the service, so money flows into the country, adding to its earnings from abroad.',
     '1 mark: payment from abroad; 1 mark: inflow = credit [2]'),
    ('Explain the four components of the current account.', 'Trade in goods (exports and imports of physical goods); trade in services (tourism, transport, finance); primary income (wages, profits, interest, dividends); secondary income (transfers such as remittances and aid).',
     '1 mark for each component explained [4]'),
    ('Explain why a country with a deficit on trade in goods can still have a current account surplus.', 'Surpluses on trade in services, primary income or secondary income (e.g. tourism, financial services, investment income, remittances) can outweigh the goods deficit.',
     '1 mark: other components; 1 mark: example of a surplus offsetting the goods deficit [2]'),
])
classify(t27_1, CA_ITEMS, CA_LABELS, 'Where, and on which side, is this transaction recorded in the current account of {country}?',
         'Identify where each transaction is recorded in the current account of {country}, and whether it is a credit or a debit.', extra=['Financial account'], name='ca_item')
errs(t27_1, [
    ('Remittances sent home by migrant workers are recorded in primary income.', 'Remittances are transfers with nothing given in return, so they are recorded in secondary income.'),
    ('Foreign direct investment into {country} is recorded as a credit in the current account.', 'FDI is recorded in the financial account; only the later profits paid on it appear in primary income.'),
    ('The current account balance is exports of goods minus imports of goods.', 'That is the trade in goods balance; the current account also includes services, primary income and secondary income.'),
    ('Spending by {country}’s residents on holidays abroad is an export of services.', 'It is an import of services (a debit), because money flows out of {country}.'),
])


@t27_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t27_1_bal(r, D):
    c = r.choice(COUNTRIES)
    for _ in range(40):
        xg, mg = r.choice(range(80, 300, 10)), r.choice(range(80, 300, 10))
        xs, ms = r.choice(range(20, 120, 5)), r.choice(range(20, 120, 5))
        pi = r.choice([-25, -18, -12, -8, -4, 3, 6, 10, 15])
        si = r.choice([-10, -6, -3, 2, 5, 8, 12])
        if xg != mg:
            break
    gb, sb = xg - mg, xs - ms
    cab = gb + sb + pi + si
    gdp = r.choice([400, 600, 800, 1000, 1200])
    tbl = (f'Exports of goods ${xg}bn; imports of goods ${mg}bn; exports of services ${xs}bn; imports of services ${ms}bn; primary income balance {bn(pi)}; secondary income balance {bn(si)}.')
    stem = f'The table shows data for {c}’s current account in one year. {tbl}'
    if D == 1:
        return cq(r, 1, stem + ' What is the balance of trade in goods?', bn(gb), f'{xg} − {mg} = {bn(gb)}.', dis_num(r, gb, bn, [mg - xg, gb + sb, xg + mg]), mcq_D=(1,))
    if D == 2:
        return cq(r, 2, stem + ' What is the current account balance?', bn(cab), f'({xg} − {mg}) + ({xs} − {ms}) + ({num(pi)}) + ({num(si)}) = {bn(cab)}.',
                  dis_num(r, cab, bn, [gb + sb, cab - 2 * si, gb]), mcq_D=(2,))
    a = f'Goods balance {bn(gb)}; services balance {bn(sb)}; current account = {bn(gb)} + {bn(sb)} + {bn(pi)} + {bn(si)} = {bn(cab)}.'
    if D == 3:
        return {'stem': stem + ' (a) Calculate the balance of trade in goods and the balance of trade in services. (b) Calculate the current account balance.',
                'answer': f'(a)/(b) {a}', 'key': '(a) both balances [2] (b) [1] [3]', 'marks': 3, 'type': 'numerical'}
    sh = 100 * cab / gdp
    return {'stem': stem + f' GDP is ${gdp}bn. (a) Calculate the current account balance and express it as a percentage of GDP. (b) Identify the component that contributes most to the {"deficit" if cab < 0 else "surplus"} and explain one possible cause. '
                    + ('(c) Discuss whether this current account position is a problem for ' + c + '.' if D == 5 else ''),
            'answer': f'(a) {a} As % of GDP: {num(sh, 1)}%. (b) ' + _ca_main(gb, sb, pi, si, cab) +
                      (' (c) Depends on size (under about 3% of GDP is usually sustainable), cause (consumption vs investment-led), how it is financed (FDI vs short-term borrowing) and duration; judgement.' if D == 5 else ''),
            'key': '(a) balance [2]; % of GDP [1] (b) component [1]; cause [1]' + (' (c) evaluation [3] [8]' if D == 5 else ' [5]'), 'marks': 8 if D == 5 else 5, 'type': 'numerical'}


def _ca_main(gb, sb, pi, si, cab):
    comp = {'trade in goods': gb, 'trade in services': sb, 'primary income': pi, 'secondary income': si}
    if cab < 0:
        k = min(comp, key=comp.get)
        why = {'trade in goods': 'uncompetitive manufacturing or strong domestic demand for imported goods',
               'trade in services': 'heavy use of foreign transport, insurance or tourism services', 'primary income': 'large profit and interest payments to foreign investors',
               'secondary income': 'large remittances sent abroad by foreign workers or aid payments'}[k]
    else:
        k = max(comp, key=comp.get)
        why = {'trade in goods': 'competitive exports of goods or commodities', 'trade in services': 'strong exports of tourism, finance or other services',
               'primary income': 'large investment income from assets abroad', 'secondary income': 'large remittances from citizens working abroad'}[k]
    return f'{k[0].upper() + k[1:]} ({bn(comp[k])}): possibly {why}.'


CAUSE_CASES = [
    ('Incomes in {country} grow rapidly during a boom and households buy many more imported goods.', 'Cyclical cause (high domestic demand)', 'rising income raises imports through the marginal propensity to import.'),
    ('Firms in {country} have lower productivity than foreign rivals and lose export markets.', 'Structural cause (lack of competitiveness)', 'long-term weakness in non-price and price competitiveness.'),
    ('The currency of {country} appreciates by 15% against its trading partners.', 'Exchange rate appreciation', 'exports become dearer abroad and imports cheaper.'),
    ('Inflation in {country} is 8% while in its trading partners it is 2%.', 'Relatively high domestic inflation', 'domestic goods become less price competitive.'),
    ('A recession in {country2}, {country}’s main export market, reduces demand for {country}’s exports.', 'Weak foreign demand (recession abroad)', 'lower foreign incomes reduce export demand.'),
    ('The world price of oil, {country}’s main export, rises sharply.', 'Rising world prices of exports', 'export revenue rises if demand is price inelastic, causing a surplus.'),
    ('Households in {country} save a large share of income and spend little on imports.', 'High domestic saving (low demand)', 'low consumption keeps imports down, contributing to a surplus.'),
]
CAUSE_LABELS = ['Cyclical cause (high domestic demand)', 'Structural cause (lack of competitiveness)', 'Exchange rate appreciation', 'Relatively high domestic inflation',
                'Weak foreign demand (recession abroad)', 'Rising world prices of exports', 'High domestic saving (low demand)']

t27_2 = T('Causes of current account deficits and surpluses', 'causes of current account deficits', 'current account surpluses', 'cyclical and structural deficits')
mc(t27_2, [
    ('Which is most likely to cause a current account deficit?', 'Rapid growth in domestic incomes increasing demand for imports', 'Cyclical deficit.',
     ['A recession in the domestic economy', 'A depreciation of the currency', 'Rapid growth in the incomes of trading partners']),
    ('What is meant by a structural current account deficit?', 'A deficit caused by long-term weaknesses such as low productivity or poor product quality', 'Persists through the cycle.',
     ['A deficit that occurs only during a boom', 'A deficit caused by a single bad harvest', 'A deficit on the financial account']),
    ('How might an appreciation of a country’s currency affect its current account?', 'It may worsen it, because exports become dearer and imports cheaper', 'Price competitiveness falls.',
     ['It always improves it', 'It has no effect', 'It raises export volumes']),
    ('Why might a country have a current account surplus?', 'Its exports are highly competitive and domestic saving is high', 'Strong exports, low import demand.',
     ['Its inflation rate is higher than its trading partners’', 'Its currency has appreciated strongly', 'Its domestic demand is growing very fast']),
    ('The marginal propensity to import is 0.3. Income rises by $10bn. By how much do imports rise?', '$3bn', 'ΔM = mpm × ΔY = 0.3 × 10.',
     ['$0.3bn', '$7bn', '$30bn']),
    ('A deficit on the current account that disappears when the economy enters a recession is most likely', 'a cyclical deficit', 'Imports fall as income falls.',
     ['a structural deficit', 'caused by low productivity', 'caused by an undervalued currency']),
])
ex(t27_2, [
    ('Explain the difference between a cyclical and a structural current account deficit.', 'A cyclical deficit results from high demand in a boom (imports rise with income) and falls in a downturn; a structural deficit reflects long-term weaknesses such as low productivity or poor quality and persists through the cycle.',
     '1 mark: cyclical linked to cycle/demand; 1 mark: structural long-term competitiveness [2]'),
    ('Explain how relatively high inflation can cause a current account deficit.', 'If domestic prices rise faster than abroad, exports become less price competitive and imports relatively cheaper, so exports fall and imports rise.',
     '1 mark: loss of price competitiveness; 1 mark: exports fall/imports rise [2]'),
    ('Explain two causes of a current account surplus.', 'Competitive exports (productivity, quality); high world prices for its commodity exports; high saving/low domestic demand; undervalued currency; large investment income from abroad.',
     '1 mark each for two causes, 1 mark each for explanation [4]'),
])
classify(t27_2, CAUSE_CASES, CAUSE_LABELS, 'Which cause of a current account imbalance is described?', 'For each case, identify the cause of the change in the current account and explain it.', name='ca_cause')
errs(t27_2, [
    ('A current account deficit is always caused by uncompetitive firms.', 'It may be cyclical (rapid growth in income and imports), or caused by an appreciation, high inflation or weak foreign demand, not only structural weakness.'),
    ('A recession in {country} will worsen its current account.', 'A recession reduces incomes and so imports, which tends to improve the current account (unless exports fall more).'),
    ('An appreciation of {country}’s currency will increase its exports.', 'Appreciation raises the foreign-currency price of exports, so export volumes tend to fall.'),
])
items(t27_2, 'C2', (1, 2, 3, 4), [
    ('{country} has had a current account deficit in every year for 15 years, in booms and recessions. Explain what this suggests about the cause.',
     'A persistent deficit through the cycle suggests a structural cause, such as low productivity, poor quality or a narrow export base, rather than a cyclical one.',
     '1 mark: structural; 1 mark: example of structural weakness [2]'),
    ('{country}’s current account deficit widened during an investment boom financed by foreign capital. Explain why this deficit may be less worrying.',
     'Imports of capital goods raise productive capacity, which can increase future exports and income to repay the borrowing.',
     '1 mark: imports of capital goods/investment; 1 mark: future capacity and exports [2]'),
], name='cause_items')


@t27_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t27_2_mpm(r, D):
    c, c2 = r.sample(COUNTRIES, 2)
    m = r.choice([0.15, 0.2, 0.25, 0.3, 0.4])
    dy = r.choice([20, 30, 40, 50, 60])
    dx = r.choice([-6, -4, -2, 2, 4, 6])
    cab0 = r.choice([-20, -10, -5, 0, 5, 10])
    dm = m * dy
    cab1 = cab0 + dx - dm
    stem = f'{c} has a marginal propensity to import of {num(m, 2)}. Its national income rises by ${dy}bn.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the increase in imports.', bn(dm), f'{num(m, 2)} × {dy} = {bn(dm)}.', dis_num(r, dm, bn, [dy * (1 - m), dy / m]), mcq_D=(1, 2))
    stem2 = stem + f' At the same time, exports {"rise" if dx > 0 else "fall"} by ${abs(dx)}bn because of {"a boom" if dx > 0 else "a recession"} in {c2}. The current account balance was initially {bn(cab0)}.'
    if D == 3:
        return {'stem': stem2 + ' (a) Calculate the change in imports. (b) Calculate the new current account balance (assume other items are unchanged).',
                'answer': f'(a) {num(m, 2)} × {dy} = {bn(dm)}. (b) {bn(cab0)} + ({bn(dx)}) − {bn(dm)} = {bn(cab1)}.', 'key': '(a) [1] (b) [2] [3]', 'marks': 3, 'type': 'numerical'}
    return {'stem': stem2 + ' (a) Calculate the change in imports and the new current account balance (assume other items are unchanged). (b) Explain whether this change is cyclical or structural. (c) Explain one policy that could reduce the deficit without reducing national income.',
            'answer': f'(a) ΔM = {bn(dm)}; new balance = {bn(cab0)} + ({bn(dx)}) − {bn(dm)} = {bn(cab1)}. (b) Mainly cyclical: imports rise with domestic income and exports depend on foreign incomes over the cycle. '
                      '(c) Supply-side policies to raise competitiveness, or expenditure-switching such as depreciation, which shift spending to domestic goods rather than cutting total demand.',
            'key': '(a) ΔM [1]; new balance [2] (b) [1] (c) policy explained [2] [6]', 'marks': 6, 'type': 'numerical'}


@t27_2.add('C3', (3, 4, 5), 'numerical')
def t27_2_infl(r, D):
    c, c2 = r.sample(COUNTRIES, 2)
    i1, i2 = r.choice([6, 8, 10, 12]), r.choice([1, 2, 3])
    p = r.choice([100, 200, 250, 400])
    yrs = r.choice([2, 3])
    pa, pb = p * (1 + i1 / 100) ** yrs, p * (1 + i2 / 100) ** yrs
    stem = f'A {r.choice(MGOODS[:6])} producer in {c} and a rival in {c2} both sell at the equivalent of ${p}. Inflation is {i1}% a year in {c} and {i2}% a year in {c2}; the exchange rate does not change.'
    return {'stem': stem + f' (a) Calculate both prices after {yrs} years, assuming each rises in line with inflation. (b) Explain the likely effect on {c}’s current account.' + (' (c) Explain one factor that could prevent this effect.' if D >= 4 else ''),
            'answer': f'(a) {c}: {p} × {num(1 + i1 / 100, 2)}^{yrs} = {money(pa)}; {c2}: {money(pb)}. (b) {c}’s goods become relatively dearer, so exports fall and imports rise, worsening its current account. '
                      + ('(c) A depreciation of the currency, better quality or non-price competitiveness, or low price elasticity of demand.' if D >= 4 else ''),
            'key': '(a) both prices [2] (b) [2]' + (' (c) [1] [5]' if D >= 4 else ' [4]'), 'marks': 5 if D >= 4 else 4, 'type': 'numerical'}


CONSQ_CASES = [
    ('{country} finances its large current account deficit by borrowing heavily from abroad.', 'Rising foreign debt', 'future interest payments increase primary income debits.'),
    ('A persistent deficit leads to a fall in demand for {country}’s currency.', 'Pressure for depreciation', 'more currency is supplied to buy imports than is demanded for exports.'),
    ('Imports replace domestic output and factories close in {country}.', 'Lower output and employment', 'net exports are a leakage from aggregate demand.'),
    ('{country}’s large surplus causes its currency to appreciate and trading partners to complain.', 'Pressure for appreciation and international tension', 'surpluses mean deficits elsewhere and demand for the currency.'),
    ('{country} sells foreign currency reserves to support its exchange rate while in deficit.', 'Loss of foreign currency reserves', 'reserves are used to finance the deficit.'),
]
CONSQ_LABELS = ['Rising foreign debt', 'Pressure for depreciation', 'Lower output and employment', 'Pressure for appreciation and international tension', 'Loss of foreign currency reserves']

t27_3 = T('Consequences of current account imbalances', 'consequences of current account imbalances', 'current account deficit', 'current account surplus')
mc(t27_3, [
    ('Which is a likely consequence of a large and persistent current account deficit?', 'Downward pressure on the exchange rate', 'Supply of currency exceeds demand.',
     ['Upward pressure on the exchange rate', 'A rise in foreign currency reserves', 'Lower foreign debt']),
    ('Why might a current account deficit reduce aggregate demand?', 'Net exports (X − M) are a component of aggregate demand', 'Imports are a leakage.',
     ['Exports are a leakage from the circular flow', 'It raises government spending', 'It increases investment']),
    ('How is a current account deficit usually financed?', 'By a surplus on the financial account, such as borrowing or foreign investment', 'The balance of payments balances overall.',
     ['By printing money', 'By raising income tax', 'By cutting exports']),
    ('Why may a current account surplus be a problem for a country?', 'It may cause appreciation and lead to retaliation from deficit countries', 'Global imbalance.',
     ['It always causes unemployment', 'It reduces foreign reserves', 'It increases foreign debt']),
    ('A current account deficit is least likely to be a concern when it', 'is small and financed by long-term foreign direct investment', 'Sustainable financing.',
     ['is large and financed by short-term borrowing', 'has lasted for many years', 'is caused by spending on consumer imports']),
    ('Which consequence of a current account deficit would worsen the current account in later years?', 'Rising interest payments on foreign borrowing', 'Primary income debits increase.',
     ['A fall in the exchange rate', 'Lower domestic inflation', 'Higher foreign reserves']),
])
ex(t27_3, [
    ('Explain why a current account deficit financed by short-term borrowing may be a problem.', 'Short-term capital ("hot money") can leave quickly if confidence falls, causing a sharp depreciation; debt and interest payments build up.',
     '1 mark: capital can leave quickly/currency crisis; 1 mark: rising debt/interest [2]'),
    ('Explain two possible consequences of a large current account surplus for an economy.', 'Appreciation reduces future competitiveness; inflationary pressure from high net exports; accumulation of reserves; criticism or retaliation from partners; it may mean domestic consumption is low.',
     '1 mark each for two consequences, 1 mark each for explanation [4]'),
    ('Explain why a current account deficit is not necessarily a problem.', 'It may be small and temporary, caused by imports of capital goods that raise future output, and financed by FDI; it allows higher consumption and investment now.',
     '1 mark: temporary/small; 1 mark: investment-led or sustainable financing [2]'),
])
classify(t27_3, CONSQ_CASES, CONSQ_LABELS, 'Which consequence of a current account imbalance is described?', 'For each case, identify the consequence of the current account imbalance and explain it.', name='ca_consq')
errs(t27_3, [
    ('A current account deficit always means that {country} is poorer.', 'A deficit means spending abroad exceeds earnings; it can reflect high consumption or investment financed by capital inflows and is not necessarily harmful if small and sustainable.'),
    ('A current account surplus has no disadvantages.', 'It may cause appreciation, inflation, low domestic consumption and tension or retaliation from deficit countries.'),
    ('A current account deficit in {country} will cause its currency to appreciate.', 'A deficit means more of the currency is supplied (to buy imports) than demanded, putting downward pressure on its value.'),
])
items(t27_3, 'C2', (1, 2, 3, 4), [
    ('{country} has a current account deficit of 7% of GDP, financed mainly by short-term bank loans. Explain why investors may become concerned.',
     'A large deficit financed by short-term loans is vulnerable: lenders may refuse to roll over loans, capital may flee, the currency may fall sharply and debt repayments rise.',
     '1 mark: size/short-term finance; 1 mark: risk of capital flight/depreciation [2]'),
    ('{country}’s current account surplus is 9% of GDP. Explain why its trading partners might object.',
     'Its surplus is matched by deficits elsewhere, reducing demand and jobs in partner countries; they may accuse it of an undervalued currency and impose protection.',
     '1 mark: deficits elsewhere/jobs; 1 mark: retaliation or currency criticism [2]'),
], name='consq_items')


@t27_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t27_3_debt(r, D):
    c = r.choice(COUNTRIES)
    gdp = r.choice([200, 400, 500, 800])
    sh = r.choice([3, 4, 5, 6, 8])
    yrs = r.choice([4, 5, 8, 10])
    i = r.choice([3, 4, 5, 6])
    deficit = gdp * sh / 100
    debt = deficit * yrs
    interest = debt * i / 100
    stem = f'{c} has GDP of ${gdp}bn and runs a current account deficit of {sh}% of GDP each year, financed entirely by foreign borrowing.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the annual deficit.', bn(deficit), f'{sh}% × {gdp} = {bn(deficit)}.', dis_num(r, deficit, bn, [sh * 10, gdp / sh]), mcq_D=(1, 2))
    stem2 = stem + f' GDP stays constant. The interest rate on the borrowing is {i}% a year.'
    a = f'(a) Annual deficit = {bn(deficit)}; after {yrs} years foreign debt = {bn(debt)} ({num(100 * debt / gdp, 0)}% of GDP). (b) Annual interest = {i}% × {bn(debt)} = {bn(interest)}, {num(100 * interest / gdp, 2)}% of GDP. '
    if D == 3:
        return {'stem': stem2 + f' (a) Calculate the total foreign debt after {yrs} years. (b) Calculate the annual interest payment on this debt.', 'answer': a,
                'key': '(a) [2] (b) [1] [3]', 'marks': 3, 'type': 'numerical'}
    return {'stem': stem2 + f' (a) Calculate the total foreign debt after {yrs} years as a value and as a percentage of GDP. (b) Calculate the annual interest payment. (c) Explain how this interest affects the current account. (d) Discuss whether the deficit is sustainable.',
            'answer': a + '(c) Interest paid abroad is a primary income debit, so it widens the current account deficit further unless exports rise. (d) Depends on whether borrowing funds investment that raises export capacity, GDP growth, interest rates, the currency of the debt and investor confidence; judgement.',
            'key': '(a) [2] (b) [1] (c) [2] (d) [2] [7]', 'marks': 7, 'type': 'numerical'}


def _ch27_case(r, D):
    c = r.choice(COUNTRIES)
    xg, mg, xs, ms = r.choice([180, 210, 240]), r.choice([260, 290, 320]), r.choice([60, 80, 95]), r.choice([40, 50, 70])
    pi, si = r.choice([-20, -12, -8]), r.choice([10, 15, 22])
    gdp = r.choice([800, 1000, 1200])
    cab = xg - mg + xs - ms + pi + si
    intro = (f'Extract: {c}’s current account, latest year ($bn): exports of goods {xg}, imports of goods {mg}, exports of services {xs}, imports of services {ms}, primary income balance {num(pi)}, '
             f'secondary income balance {num(si)}. GDP is ${gdp}bn. Consumer spending has been rising strongly, financed by credit, and the currency appreciated by 8% last year. '
             'Remittances from citizens working abroad are rising. Foreign investors hold a large share of government bonds.')
    parts = [
        lambda r: ('Calculate the current account balance and express it as a percentage of GDP.', f'{bn(cab)}; {num(100 * cab / gdp, 1)}% of GDP.', '[2]'),
        lambda r: ('Identify which component of the current account includes remittances.', 'Secondary income (current transfers).', '[1]'),
        lambda r: ('Explain two possible causes of the deficit on trade in goods.', 'Strong credit-fuelled consumer demand raises imports (cyclical); the 8% appreciation makes exports dearer and imports cheaper.', '[4]'),
        lambda r: ('Explain why the primary income balance is negative.', 'Interest on government bonds and profits paid to foreign investors exceed investment income received.', '[2]'),
        lambda r: (f'Discuss whether {c}’s current account position is a serious problem.', 'Size relative to GDP, cyclical vs structural cause, consumption- not investment-led, financing by foreign bond holders (risk of capital flight), possible depreciation; judgement.', '[6]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t27_1, t27_2, t27_3], _ch27_case)
CA_SCENES = ['{country} has had a current account deficit of over 5% of GDP for several years.', '{country} is a major exporter of manufactured goods with a large current account surplus.',
             'The currency of {country} has appreciated strongly over the past two years.']
essay(t27_1, [
    ('Explain the components of the current account of the balance of payments.',
     'Trade in goods, trade in services, primary income, secondary income; credits and debits with examples; distinction from the financial account.',
     'a deficit on trade in goods means that {country} has a current account problem',
     'Goods deficit may reflect lack of competitiveness and reduces AD.',
     'Other components (services, income, transfers) may offset it; the whole current account and its financing matter; depends on cause; judgement.'),
], CA_SCENES)
essay(t27_2, [
    ('Explain the possible causes of a current account deficit.',
     'Cyclical (high growth, mpm), structural (productivity, quality, narrow export base), exchange rate appreciation, relative inflation, weak foreign demand, falling export prices.',
     'a current account deficit is mainly caused by a lack of international competitiveness',
     'Structural weaknesses explain persistent deficits; low productivity and high unit labour costs.',
     'Cyclical demand, exchange rates and foreign recessions also matter; investment-led deficits; depends on the country and period; judgement.'),
], CA_SCENES)
essay(t27_3, [
    ('Explain the possible consequences of a large current account deficit.',
     'Lower AD and employment; depreciation; borrowing and foreign debt; interest payments; loss of reserves; risk of crisis if financed short-term.',
     'a current account deficit is always harmful for {country}',
     'Reduces AD, rising debt and interest, vulnerability to capital flight.',
     'Small, temporary or investment-led deficits are sustainable; FDI financing; allows higher living standards; surplus countries face problems too; judgement.'),
], CA_SCENES)
CHAPTERS[27] = [t27_1, t27_2, t27_3]

# ============================================================================ 28 Exchange rates
CURS = ['rand', 'baht', 'yuan', 'rupiah', 'naira', 'kwacha', 'won', 'kip']

XR_SYS = [
    ('The value of the {cur} is determined entirely by demand and supply in the foreign exchange market, with no central bank intervention.', 'Floating exchange rate', 'market forces alone set the rate.'),
    ('The central bank of {country} keeps its currency at 3.75 units to the US dollar by buying and selling currency whenever needed.', 'Fixed exchange rate', 'the rate is pegged to another currency and defended with reserves and interest rates.'),
    ('The {cur} is allowed to move with market forces, but the central bank intervenes when it moves outside a target range.', 'Managed float', 'market-determined within limits, with occasional intervention.'),
    ('{country} links its currency to the euro at a fixed rate and holds large euro reserves to defend it.', 'Fixed exchange rate', 'a peg against an anchor currency.'),
    ('The central bank of {country} occasionally buys its currency to slow a rapid depreciation, without setting any official target.', 'Managed float', 'dirty float with intervention to smooth movements.'),
    ('The exchange rate of {country} changed 40 times last month as supply and demand changed; the government does not intervene.', 'Floating exchange rate', 'no official intervention.'),
]
XR_SYS_LABELS = ['Floating exchange rate', 'Fixed exchange rate', 'Managed float']


def _xr(r):
    return r.choice(CURS), r.choice(COUNTRIES)


t28_1 = T('Floating, fixed and managed exchange rate systems', 'floating, fixed and managed exchange rate systems', 'exchange rate systems', 'managed float')
mc(t28_1, [
    ('What is an exchange rate?', 'The price of one currency in terms of another', 'E.g. 1 euro = 1.10 US dollars.', ['The rate of interest on foreign loans', 'The rate of inflation abroad', 'The ratio of exports to imports']),
    ('In a floating exchange rate system, the exchange rate is determined by', 'the demand for and supply of the currency on the foreign exchange market', 'No official target.',
     ['the central bank setting an official rate', 'the government’s budget balance', 'the WTO']),
    ('What must a central bank do to maintain a fixed exchange rate when there is excess supply of its currency?', 'Buy its own currency using foreign currency reserves', 'Increases demand to restore the peg.',
     ['Sell its own currency', 'Lower interest rates', 'Increase the money supply']),
    ('What is a managed float?', 'A floating rate in which the central bank intervenes from time to time to influence the rate', 'Also called a dirty float.',
     ['A rate fixed permanently by law', 'A rate set by the IMF', 'A rate that never changes']),
    ('Which is an advantage of a fixed exchange rate?', 'Certainty for traders and investors', 'Reduces exchange rate risk.', ['Monetary policy is free to target domestic objectives', 'No need for foreign reserves', 'Automatic correction of a current account deficit']),
    ('Which is an advantage of a floating exchange rate?', 'The exchange rate can adjust to help correct a current account imbalance', 'Automatic adjustment; independent monetary policy.',
     ['It guarantees stable prices for exporters', 'It requires large foreign reserves', 'It removes speculation completely']),
    ('A central bank wanting to raise the value of its currency in a managed float could', 'raise interest rates', 'Attracts hot money, raising demand for the currency.',
     ['sell its own currency', 'cut interest rates', 'buy foreign currency with its own currency']),
])
ex(t28_1, [
    ('Explain the difference between a fixed and a floating exchange rate system.', 'In a floating system the rate is set by market demand and supply with no target; in a fixed system the central bank pegs the rate to another currency and intervenes (reserves, interest rates) to keep it there.',
     '1 mark: floating = market forces; 1 mark: fixed = peg maintained by intervention [2]'),
    ('Explain how a central bank can maintain a fixed exchange rate.', 'It buys its own currency with reserves when there is excess supply and sells it when there is excess demand; it can also raise or lower interest rates to change capital flows.',
     '1 mark: buying/selling with reserves; 1 mark: interest rates [2]'),
    ('Explain two disadvantages of a fixed exchange rate system.', 'Large reserves needed; monetary policy must be used to defend the rate, not domestic goals; a deficit cannot be corrected automatically; speculative attacks; risk of an over- or under-valued rate.',
     '1 mark each for two disadvantages, 1 mark each for explanation [4]'),
    ('Explain why a government might choose a managed float rather than a pure float.', 'It gains the flexibility of market rates but can intervene to reduce excessive volatility and speculation, giving traders more certainty.',
     '1 mark: flexibility; 1 mark: reduces volatility/certainty [2]'),
])
classify(t28_1, XR_SYS, XR_SYS_LABELS, 'Which exchange rate system is being described?', 'For each case, identify the exchange rate system and explain your answer.', extra=['Customs union'], name='xr_sys')
errs(t28_1, [
    ('In a floating exchange rate system, the central bank sets the exchange rate each day.', 'In a floating system the rate is determined by demand and supply on the foreign exchange market; the central bank does not set it.'),
    ('A fixed exchange rate can never change.', 'A fixed rate can be devalued or revalued by the authorities; it is fixed only while they choose to defend it.'),
    ('Under a fixed exchange rate system, {country} does not need foreign currency reserves.', 'Reserves are essential to buy the currency when there is excess supply and so defend the peg.'),
])
items(t28_1, 'C2', (1, 2, 3, 4), [
    ('{country} pegs its currency to the US dollar. Investors expect a devaluation and sell the currency. Explain what the central bank must do.',
     'Excess supply of the currency must be absorbed: the central bank buys its own currency with dollar reserves and may raise interest rates; if reserves run low it may have to devalue.',
     '1 mark: buy currency with reserves; 1 mark: raise interest rates/risk of devaluation [2]'),
    ('{country} has a floating exchange rate and a large current account deficit. Explain how the exchange rate may help to reduce the deficit.',
     'The deficit means more currency is supplied than demanded, so the currency depreciates; exports become cheaper and imports dearer, which can reduce the deficit if demand is price elastic.',
     '1 mark: depreciation from excess supply; 1 mark: price competitiveness/deficit falls [2]'),
], name='xr_items')


def _fx(r):
    """Currency market in US cents per unit: Qd = a − b·e, Qs = c + d·e (millions of units a day)."""
    e = r.choice([20, 25, 40, 50, 60, 80])
    b, d = r.choice([2, 3, 4, 5]), r.choice([2, 3, 4, 6])
    q = r.choice([300, 400, 500, 600])
    a, c = q + b * e, q - d * e
    if c < -q:
        c = None
    return e, b, d, q, a, c


@t28_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t28_1_peg(r, D):
    cur, c = _xr(r)
    e, b, d, q, a, c0 = _fx(r)
    if c0 is None:
        return None
    gap = r.choice([5, 10, 15])
    peg = e + gap
    qd, qs = a - b * peg, c0 + d * peg
    xs = qs - qd
    cost = xs * peg / 100            # US$ millions a day
    stem = (f'In the foreign exchange market for the {cur}, demand is {qd_s(a, b)} and supply is {qs_s(c0, d)}, where P is the price of one {cur} in US cents and Q is millions of {cur} a day. '
            f'The central bank of {c} fixes the exchange rate at {peg} US cents per {cur}.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the excess supply of the currency at the fixed rate.', f'{num(xs)} million {cur}', f'Qs = {num(qs)}, Qd = {num(qd)}; excess supply = {num(xs)} million.',
                  dis_num(r, xs, lambda x: f'{num(x)} million {cur}', [qs, qd, q]), mcq_D=(1, 2))
    a_txt = f'(a) Free-market rate: {qd_s(a, b)} = {qs_s(c0, d)} gives P = {e} US cents, Q = {q} million. (b) At {peg} cents: Qd = {num(qd)}, Qs = {num(qs)}; excess supply = {num(xs)} million {cur} a day. '
    if D == 3:
        return {'stem': stem + ' (a) Calculate the free-market equilibrium exchange rate. (b) Calculate the excess supply at the fixed rate.',
                'answer': a_txt, 'key': '(a) [2] (b) [2] [4]', 'marks': 4, 'type': 'numerical'}
    return {'stem': stem + f' (a) Calculate the free-market equilibrium exchange rate. (b) Calculate the excess supply at the fixed rate. (c) Calculate the US dollars the central bank must spend each day to maintain the rate. (d) Explain two ways the central bank could avoid running down its reserves.',
            'answer': a_txt + f'(c) It must buy {num(xs)} million {cur} at ${num(peg / 100, 2)} each = ${num(cost, 1)} million a day. (d) Raise interest rates to attract capital inflows (raising demand for the {cur}); use contractionary policies or controls to reduce imports (lowering supply); or devalue to the market rate.',
            'key': '(a) [2] (b) [1] (c) [1] (d) two ways [2] [6]', 'marks': 6, 'type': 'numerical'}


SHIFT_CASES = [
    ('Foreign demand for {country}’s exports of {mgood2} rises sharply.', 'Demand for the currency rises; it appreciates', 'foreigners need more of the currency to pay for exports.'),
    ('Households in {country} buy many more imported {mgood}.', 'Supply of the currency rises; it depreciates', 'residents sell their currency to buy foreign currency for imports.'),
    ('The central bank of {country} raises interest rates while rates abroad are unchanged.', 'Demand for the currency rises; it appreciates', 'hot money flows in to earn higher returns.'),
    ('Speculators expect the currency of {country} to fall in value and sell it.', 'Supply of the currency rises; it depreciates', 'speculative selling increases supply.'),
    ('A foreign car maker builds a large factory in {country}.', 'Demand for the currency rises; it appreciates', 'FDI requires buying the currency to pay for the investment.'),
    ('Firms in {country} invest heavily in factories abroad.', 'Supply of the currency rises; it depreciates', 'outward investment requires selling the currency.'),
    ('Tourism to {country} collapses after a natural disaster.', 'Demand for the currency falls; it depreciates', 'fewer foreign tourists need the currency.'),
]
SHIFT_LABELS = ['Demand for the currency rises; it appreciates', 'Supply of the currency rises; it depreciates', 'Demand for the currency falls; it depreciates', 'Supply of the currency falls; it appreciates']

t28_2 = T('Determination of a floating exchange rate by demand and supply of currency', 'determination of a floating exchange rate', 'demand and supply of currency', 'foreign exchange market')
mc(t28_2, [
    ('Which creates a demand for a country’s currency on the foreign exchange market?', 'Foreign residents buying the country’s exports', 'They need the currency to pay.',
     ['Domestic residents buying imports', 'Domestic firms investing abroad', 'Domestic tourists travelling abroad']),
    ('Which creates a supply of a country’s currency on the foreign exchange market?', 'Domestic residents buying imports', 'They sell domestic currency for foreign currency.',
     ['Foreign tourists visiting the country', 'Foreign firms investing in the country', 'Foreigners buying the country’s exports']),
    ('A rise in a country’s interest rates relative to other countries will most likely', 'increase demand for its currency and cause it to appreciate', 'Hot money inflows.',
     ['increase supply of its currency and cause it to depreciate', 'have no effect on the exchange rate', 'reduce demand for its currency']),
    ('Why does the demand curve for a currency slope downwards?', 'A lower exchange rate makes the country’s exports cheaper, so more currency is demanded to buy them', 'Derived demand.',
     ['A lower exchange rate makes imports cheaper', 'Interest rates rise as the currency falls', 'Speculators always buy when the rate falls']),
    ('Which would cause a country’s currency to depreciate in a floating system?', 'A rise in demand for imports by its residents', 'Supply of currency shifts right.',
     ['A rise in foreign demand for its exports', 'An inflow of foreign direct investment', 'Higher domestic interest rates']),
    ('What is ‘hot money’?', 'Short-term capital that moves between countries in search of higher interest rates or speculative gains', 'Volatile flows that move exchange rates.',
     ['Counterfeit currency', 'Money held by the central bank', 'Money spent on imported fuel']),
])
ex(t28_2, [
    ('Explain how a floating exchange rate is determined.', 'Demand for the currency comes from foreigners buying exports and assets; supply comes from residents buying imports and foreign assets; the equilibrium rate is where demand equals supply, and it changes when either shifts.',
     '1 mark: sources of demand; 1 mark: sources of supply; 1 mark: equilibrium where D = S [3]'),
    ('Explain two factors that could cause a currency to appreciate.', 'Higher relative interest rates (hot money); rising demand for exports; FDI inflows; lower relative inflation; speculation that it will rise; lower demand for imports.',
     '1 mark each for two factors, 1 mark each for explanation [4]'),
    ('Explain how speculation can affect a floating exchange rate.', 'If speculators expect the currency to rise they buy it, raising demand and causing the rise they expected; expectations of a fall lead to selling and depreciation; this can increase volatility.',
     '1 mark: buying/selling on expectations; 1 mark: self-fulfilling/volatility [2]'),
])
classify(t28_2, SHIFT_CASES, SHIFT_LABELS, 'What is the most likely effect on the market for the currency of {country}?', 'For each event, explain the effect on the demand for or supply of the currency of {country} and on its exchange rate.', name='xr_shift')
errs(t28_2, [
    ('When residents of {country} buy more imports, demand for {country}’s currency rises.', 'Buying imports means selling the domestic currency for foreign currency, so the supply of the currency rises and it tends to depreciate.'),
    ('Higher interest rates in {country} will cause its currency to depreciate.', 'Higher relative interest rates attract capital inflows, raising demand for the currency, so it tends to appreciate.'),
    ('A floating exchange rate is determined by the government’s budget.', 'It is determined by demand for and supply of the currency, from trade, investment, interest rate and speculative flows.'),
])
items(t28_2, 'C2', (1, 2, 3, 4), [
    ('Explain, using a demand and supply diagram, what happens to the value of the {cur} when foreign tourists visit {country} in greater numbers.',
     'Tourists buy the {cur} to spend in {country}, so demand for the {cur} shifts right; the equilibrium exchange rate rises (appreciation) and quantity traded increases.',
     '1 mark: demand shifts right; 1 mark: exchange rate rises [2]'),
    ('Inflation in {country} rises to 10% while it is 2% in its trading partners. Explain the likely effect on the exchange rate of the {cur}.',
     '{country}’s exports become less competitive and imports more attractive, so demand for the {cur} falls and supply rises; it depreciates.',
     '1 mark: competitiveness/demand and supply changes; 1 mark: depreciation [2]'),
], name='det_items')


@t28_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t28_2_eq(r, D):
    cur, c = _xr(r)
    e, b, d, q, a, c0 = _fx(r)
    if c0 is None:
        return None
    side = r.choice(['D', 'S'])
    k = (b + d) * r.choice([2, 4, 5])
    if side == 'D':
        e1 = e + k / (b + d)
        q1 = a + k - b * e1
        ev = f'Foreign demand for {c}’s exports rises, increasing demand for the {cur} by {k} million a day at every exchange rate.'
        new = qd_s(a + k, b)
    else:
        e1 = e - k / (b + d)
        q1 = c0 + k + d * e1
        ev = f'Residents of {c} increase their spending on imports, increasing the supply of the {cur} by {k} million a day at every exchange rate.'
        new = qs_s(c0 + k, d)
    stem = (f'The market for the {cur} is described by {qd_s(a, b)} and {qs_s(c0, d)}, where P is the price of one {cur} in US cents and Q is millions of {cur} traded a day.')
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the equilibrium exchange rate.', f'{e} US cents', f'{qd_s(a, b)} = {qs_s(c0, d)} → {b + d}P = {a - c0} → P = {e}.',
                  dis_num(r, e, lambda x: f'{num(x, 1)} US cents', [a / b, (a + c0) / (b + d)]), mcq_D=(1, 2))
    a_txt = f'(a) {b + d}P = {a - c0}: P = {e} US cents, Q = {q} million. (b) New {new}: P = {num(e1, 1)} US cents, Q = {num(q1)} million; the {cur} {"appreciates" if e1 > e else "depreciates"} by {num(abs(chg(e, e1)), 1)}%. '
    if D == 3:
        return {'stem': stem + f' (a) Calculate the equilibrium exchange rate and quantity. (b) {ev} Calculate the new equilibrium exchange rate and quantity.',
                'answer': a_txt, 'key': '(a) [2] (b) new rate [1]; quantity [1] [4]', 'marks': 4, 'type': 'numerical'}
    return {'stem': stem + f' (a) Calculate the equilibrium exchange rate and quantity. (b) {ev} Calculate the new equilibrium exchange rate and the percentage change in the value of the {cur}. (c) Explain one effect of this change on {c}’s economy.'
                    + (f' (d) Explain why the central bank of {c} might intervene in this market.' if D == 5 else ''),
            'answer': a_txt + ('(c) Exports become dearer abroad and imports cheaper, so the current account may worsen and inflation fall.' if e1 > e else
                               '(c) Exports become cheaper abroad and imports dearer, so net exports may rise, raising AD, but import prices push up inflation.')
                      + (' (d) To reduce volatility and uncertainty for traders, to protect competitiveness or to limit imported inflation; it could buy or sell currency or change interest rates.' if D == 5 else ''),
            'key': '(a) [2] (b) new rate [1]; % change [1] (c) [2]' + (' (d) [2] [8]' if D == 5 else ' [6]'), 'marks': 8 if D == 5 else 6, 'type': 'numerical'}


DEP_CASES = [
    ('The {cur} falls from 0.50 to 0.40 US dollars as market demand for it weakens; there is no official target.', 'Depreciation', 'a fall in a floating rate caused by market forces.'),
    ('The central bank of {country} announces that its fixed rate will change from 2 to 2.5 {cur} per US dollar.', 'Devaluation', 'an official reduction in a fixed rate (more {cur} per dollar).'),
    ('The {cur} rises against the euro after a rise in foreign demand for {country}’s exports; the currency floats freely.', 'Appreciation', 'a rise in a floating rate caused by market forces.'),
    ('The government of {country} raises its currency peg from 4 to 3.5 {cur} per US dollar.', 'Revaluation', 'an official increase in the value of a fixed rate (fewer {cur} per dollar).'),
    ('Speculators sell the floating {cur} and its value against the dollar falls by 12%.', 'Depreciation', 'market-driven fall in a floating currency.'),
    ('Under its fixed exchange rate system, {country} officially lowers the value of the {cur} by 20% to restore competitiveness.', 'Devaluation', 'deliberate official reduction in a fixed rate.'),
]
DEP_LABELS = ['Depreciation', 'Appreciation', 'Devaluation', 'Revaluation']

t28_3 = T('Depreciation and appreciation; devaluation and revaluation', 'depreciation and appreciation', 'devaluation and revaluation')
mc(t28_3, [
    ('What is a depreciation of a currency?', 'A fall in its value in a floating exchange rate system', 'Market-driven fall.', ['A fall in its value decided by the government in a fixed system', 'A rise in its value', 'A fall in the rate of inflation']),
    ('What is a devaluation?', 'An official reduction in the value of a fixed exchange rate', 'Government/central bank decision.', ['A market-driven fall in a floating rate', 'A rise in a fixed exchange rate', 'A fall in the price level']),
    ('The exchange rate changes from $1 = 10 pesos to $1 = 12 pesos. What has happened?', 'The peso has depreciated against the dollar', 'More pesos per dollar: each peso is worth less.',
     ['The peso has appreciated against the dollar', 'The dollar has depreciated against the peso', 'There has been no change in value']),
    ('What is a revaluation?', 'An official increase in the value of a fixed exchange rate', 'Opposite of devaluation.', ['A market-driven rise in a floating rate', 'A fall in a fixed rate', 'A rise in export prices due to inflation']),
    ('If a currency appreciates, which is most likely to happen?', 'Its imports become cheaper in domestic currency', 'Each unit buys more foreign currency.',
     ['Its exports become cheaper in foreign currency', 'Its imports become dearer', 'Its export volumes increase']),
    ('The euro rises from $1.00 to $1.25. By how much has the dollar fallen against the euro?', '20%', '€ per $ falls from 1 to 0.8: −20%.', ['25%', '12.5%', '80%']),
])
ex(t28_3, [
    ('Explain the difference between a depreciation and a devaluation.', 'Both are falls in a currency’s value; a depreciation is caused by market forces in a floating system, while a devaluation is an official decision to lower a fixed rate.',
     '1 mark: depreciation market forces/floating; 1 mark: devaluation official/fixed [2]'),
    ('Explain why an appreciation of one currency against another means a depreciation of the other.', 'An exchange rate is a ratio: if one unit of A buys more of B, then one unit of B buys less of A, so B has fallen in value against A.',
     '1 mark: exchange rate is relative price; 1 mark: rise in one is fall in other [2]'),
    ('Explain why a government might devalue its currency.', 'To make exports cheaper and imports dearer, improving competitiveness and the current account, or because it can no longer defend the peg with reserves.',
     '1 mark: competitiveness/current account; 1 mark: unable to defend peg [2]'),
])
classify(t28_3, DEP_CASES, DEP_LABELS, 'Which term best describes this change?', 'For each case, identify the type of exchange rate change and explain your answer.', name='dep')
errs(t28_3, [
    ('The exchange rate moved from $1 = 20 {cur} to $1 = 25 {cur}, so the {cur} appreciated.', 'More {cur} are needed to buy one dollar, so each {cur} is worth less: the {cur} has depreciated.'),
    ('A devaluation happens when market forces reduce the value of a floating currency.', 'That is a depreciation; a devaluation is an official decision to lower a fixed exchange rate.'),
    ('If the dollar rises by 25% against the {cur}, the {cur} falls by 25% against the dollar.', 'The percentages differ: a 25% rise in the dollar means the {cur} falls by 20% (1/1.25 = 0.8).'),
])
items(t28_3, 'C2', (1, 2, 3, 4), [
    ('The {cur} has fallen by 15% against the US dollar this year. Explain how this affects a family in {country} planning a holiday in the United States.',
     'Each {cur} buys fewer dollars, so the holiday costs more in {cur}; the family may travel less or choose a domestic holiday.',
     '1 mark: fewer dollars per {cur}; 1 mark: higher cost in {cur}/change in behaviour [2]'),
], name='dep_items')


@t28_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t28_3_pct(r, D):
    cur, c = _xr(r)
    e0 = r.choice([4, 5, 8, 10, 12, 15, 20, 25, 40, 50])
    e1 = round(e0 * r.choice([0.8, 0.85, 0.9, 1.1, 1.2, 1.25, 1.5]), 2)
    if e1 == e0:
        return None
    dep = e1 > e0
    usd_chg = chg(e0, e1)               # value of the dollar in cur
    cur_chg = chg(1 / e0, 1 / e1)       # value of the cur in dollars
    stem = f'The exchange rate between the {cur} and the US dollar changes from $1 = {num(e0, 2)} {cur} to $1 = {num(e1, 2)} {cur}.'
    if D == 1:
        lab = f'The {cur} has {"depreciated" if dep else "appreciated"} against the dollar'
        opts, a = mcq(r, lab, [f'The {cur} has {"appreciated" if dep else "depreciated"} against the dollar', f'The dollar has {"depreciated" if dep else "appreciated"} against the {cur}', 'Neither currency has changed in value'])
        return {'stem': stem + ' Which statement is correct?', 'options': opts, 'answer': a, 'key': f'{"More" if dep else "Fewer"} {cur} per dollar, so each {cur} is worth {"less" if dep else "more"}.'}
    if D == 2:
        return cq(r, 2, stem + f' By what percentage has the value of the {cur} in US dollars changed?', pchg(cur_chg), f'Value of 1 {cur}: ${num(1 / e0, 4)} → ${num(1 / e1, 4)}; change = {e0}/{e1} − 1 = {pchg(cur_chg)}.',
                  [pchg(usd_chg), pchg(-usd_chg) if pchg(-usd_chg) != pchg(cur_chg) else pchg(-cur_chg * 1.5), pchg(-cur_chg)], mcq_D=(2,))
    a = (f'(a) The {cur} has {"depreciated" if dep else "appreciated"}: the dollar’s value in {cur} changes by {pchg(usd_chg)}, and the {cur}’s value in dollars changes by {pchg(cur_chg)} ({num(e0, 2)}/{num(e1, 2)} − 1). ')
    if D == 3:
        return {'stem': stem + f' (a) State whether the {cur} has appreciated or depreciated, and calculate the percentage change in its value against the dollar. (b) Explain why this is not the same as the percentage change in the value of the dollar.',
                'answer': a + f'(b) The base differs: the dollar changes by {pchg(usd_chg)}, but the {cur} by {pchg(cur_chg)}, because the {cur}’s value is the reciprocal of the dollar’s.',
                'key': '(a) direction [1]; percentage [1] (b) [1] [3]', 'marks': 3, 'type': 'numerical'}
    p = r.choice([200, 500, 1000, 2400])
    ps = p * e0
    return {'stem': stem + f' A machine from the United States costs ${p:,}. (a) State whether the {cur} has appreciated or depreciated, and calculate the percentage change in its value against the dollar. '
                    f'(b) Calculate the price of the machine in {cur} before and after the change. (c) Explain whether this change is a depreciation or a devaluation, if the {cur} floats freely, and one effect on firms in {c}.',
            'answer': a + f'(b) Before: {p:,} × {num(e0, 2)} = {num(ps, 2)} {cur}; after: {p:,} × {num(e1, 2)} = {num(p * e1, 2)} {cur}. '
                      f'(c) A floating rate changing through market forces is a{" depreciation" if dep else "n appreciation"}; imported capital goods become {"dearer" if dep else "cheaper"}, so firms’ costs {"rise" if dep else "fall"} but exporters become {"more" if dep else "less"} price competitive.',
            'key': '(a) [2] (b) both prices [2] (c) term [1]; effect [1] [6]', 'marks': 6, 'type': 'numerical'}


t28_4 = T('Effects of exchange rate changes on the economy', 'effects of exchange rate changes', 'marshall-lerner condition', 'j-curve')
mc(t28_4, [
    ('A depreciation of a country’s currency is most likely to', 'make its exports cheaper in foreign currency and its imports dearer in domestic currency', 'Price competitiveness improves.',
     ['make its exports dearer and imports cheaper', 'reduce the price of imported raw materials', 'have no effect on prices']),
    ('What does the Marshall–Lerner condition state?', 'A depreciation improves the current account if the sum of the price elasticities of demand for exports and imports is greater than 1', 'PEDx + PEDm > 1 (in absolute values).',
     ['A depreciation always improves the current account', 'The current account worsens if PED for exports is elastic', 'Exports and imports must be equal']),
    ('What is the J-curve effect?', 'A depreciation first worsens the current account before improving it', 'Demand is inelastic in the short run.',
     ['A depreciation immediately improves the current account', 'An appreciation improves the current account in the long run', 'The exchange rate falls and then rises']),
    ('Why might a depreciation increase inflation?', 'Import prices rise and demand for exports increases aggregate demand', 'Cost-push and demand-pull.',
     ['Import prices fall', 'Aggregate demand falls', 'Wages fall']),
    ('An appreciation of the currency is most likely to', 'reduce inflation by lowering import prices', 'Cheaper imported inputs and consumer goods.',
     ['increase export volumes', 'raise import prices', 'increase aggregate demand']),
    ('Why might a depreciation not improve the current account in the short run?', 'Export and import volumes take time to respond, as demand is price inelastic in the short run', 'Existing contracts and habits.',
     ['Exports become more expensive', 'The Marshall–Lerner condition is always met', 'Import prices fall immediately']),
    ('How might a depreciation affect economic growth?', 'It may raise growth as net exports and aggregate demand increase', 'X − M rises.',
     ['It always reduces growth', 'It reduces aggregate demand', 'It has no effect on output']),
])
ex(t28_4, [
    ('Explain the Marshall–Lerner condition.', 'A depreciation improves the current account only if the sum of the price elasticities of demand for exports and imports exceeds one; then the rise in export volumes and fall in import volumes outweigh the lower price received for exports and higher price paid for imports.',
     '1 mark: PEDx + PEDm > 1; 1 mark: volume effects outweigh price effects [2]'),
    ('Explain the J-curve effect of a depreciation.', 'In the short run demand is price inelastic (contracts, habits), so import spending rises and export revenue rises little: the current account worsens. Over time volumes respond, the Marshall–Lerner condition is met and the current account improves.',
     '1 mark: short run inelastic, worsens; 1 mark: long run elastic, improves [2]'),
    ('Explain how an appreciation can affect inflation, growth and employment.', 'Import prices fall and export demand falls: lower inflation (cheaper imports, weaker AD), but lower net exports reduce AD, growth and employment in export industries.',
     '1 mark: inflation falls; 1 mark: net exports fall; 1 mark: growth/employment fall [3]'),
    ('Explain why the effect of a depreciation on firms depends on how much they import.', 'Exporters gain competitiveness, but firms that import raw materials or components face higher costs, which can offset the price advantage.',
     '1 mark: export competitiveness; 1 mark: higher imported input costs [2]'),
])
errs(t28_4, [
    ('A depreciation will always improve the current account of {country}.', 'It improves only if the Marshall–Lerner condition holds; in the short run (J-curve) it may worsen the current account.'),
    ('An appreciation of the {cur} will make {country}’s exports cheaper abroad.', 'An appreciation raises the foreign-currency price of exports, making them less competitive.'),
    ('A depreciation reduces inflation because exports become cheaper.', 'Exports become cheaper for foreigners, but import prices rise and AD increases, so inflation tends to rise.'),
])
EFF_CASES = [
    ('The {cur} depreciates by 20%. {country} imports most of its fuel and food.', 'Higher inflation (cost-push from imports)', 'import prices rise and feed into production costs and the CPI.'),
    ('The {cur} depreciates by 15% and foreign orders for {country}’s {mgood} increase strongly.', 'Higher net exports and economic growth', 'cheaper exports raise X − M and AD.'),
    ('The {cur} appreciates by 18% and exporters of {mgood} in {country} lay off workers.', 'Higher unemployment in export industries', 'exports become dearer and demand falls.'),
    ('Six months after a depreciation, {country}’s current account deficit has widened before beginning to narrow.', 'J-curve effect', 'demand is price inelastic in the short run.'),
    ('The {cur} appreciates and the prices of imported consumer goods in {country} fall.', 'Lower inflation', 'cheaper imports reduce the price level.'),
]
classify(t28_4, EFF_CASES, ['Higher inflation (cost-push from imports)', 'Higher net exports and economic growth', 'Higher unemployment in export industries', 'J-curve effect', 'Lower inflation'],
         'Which effect of the exchange rate change is shown?', 'For each case, identify the effect of the exchange rate change on the economy and explain it.', name='xr_eff')
items(t28_4, 'C2', (1, 2, 3, 4), [
    ('{firm}, an exporter in {country}, buys 60% of its components from abroad. Explain why a depreciation of the {cur} may not help it much.',
     'Its export prices fall in foreign currency, but the {cur} cost of its imported components rises, raising its costs and reducing the benefit.',
     '1 mark: export price advantage; 1 mark: imported input costs rise [2]'),
    ('Price elasticity of demand for {country}’s exports is −0.3 and for its imports is −0.4. Explain the likely effect of a depreciation on its current account.',
     'The sum of the elasticities is 0.7, less than 1, so the Marshall–Lerner condition is not met; the current account is likely to worsen.',
     '1 mark: sum 0.7 < 1; 1 mark: current account worsens [2]'),
], name='eff_items')


@t28_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t28_4_price(r, D):
    cur, c = _xr(r)
    g = r.choice(MGOODS)
    p = r.choice([300, 600, 900, 1200, 1500, 2400])        # price in cur
    e0 = r.choice([3, 4, 5, 6, 8, 10, 12])                # cur per $
    e1 = e0 * r.choice([1.2, 1.25, 1.5]) if r.random() < 0.6 else e0 * r.choice([0.8, 0.9])
    e1 = round(e1, 2)
    d0, d1 = p / e0, p / e1
    dep = e1 > e0
    stem = f'An exporter in {c} sells {g} for {num(p)} {cur} per unit. The exchange rate changes from $1 = {num(e0, 2)} {cur} to $1 = {num(e1, 2)} {cur}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the new US dollar price of each unit, assuming the exporter keeps its price in ' + cur + ' unchanged.', money(d1),
                  f'{num(p)} ÷ {num(e1, 2)} = {money(d1)}.', dis_num(r, d1, money, [d0, p * e1, p / e0 * 0.8]), mcq_D=(1, 2))
    pc = chg(d0, d1)
    ped = r.choice([0.5, 0.8, 1.5, 2.0, 2.5])
    dq = -ped * pc
    rev = (1 + pc / 100) * (1 + dq / 100) * 100 - 100        # change in dollar revenue
    revc = (1 + dq / 100) * 100 - 100                        # change in revenue in cur (price in cur unchanged)
    a = f'(a) Before: {num(p)}/{num(e0, 2)} = {money(d0)}; after: {num(p)}/{num(e1, 2)} = {money(d1)}; change {pchg(pc)}. '
    if D == 3:
        return {'stem': stem + ' (a) Calculate the US dollar price before and after the change, and the percentage change. (b) Explain the likely effect on the quantity exported.',
                'answer': a + f'(b) The dollar price {"falls" if dep else "rises"}, so the quantity demanded abroad tends to {"rise" if dep else "fall"}; the size depends on price elasticity of demand.',
                'key': '(a) both prices [1]; % change [1] (b) [1] [3]', 'marks': 3, 'type': 'numerical'}
    return {'stem': stem + f' The price elasticity of demand for the exports is −{num(ped, 1)}. (a) Calculate the US dollar price before and after the change, and the percentage change. (b) Calculate the percentage change in the quantity exported. '
                    f'(c) Calculate the percentage change in the exporter’s revenue in {cur}. (d) Explain how far this supports the view that a {"depreciation" if dep else "appreciation"} {"improves" if dep else "worsens"} the current account.',
            'answer': a + f'(b) %ΔQ = −{num(ped, 1)} × ({pchg(pc)}) = {pchg(dq)}. (c) Price in {cur} is unchanged, so revenue in {cur} changes by {pchg(revc)} (dollar revenue changes by {pchg(rev)}). '
                      '(d) The effect on the current account also depends on import elasticity (Marshall–Lerner), the J-curve time lag, imported input costs and whether the exporter changes its price; ' +
                      ('demand here is elastic, so export earnings in dollars rise.' if ped > 1 and dep else 'demand here is inelastic, so export earnings in dollars fall.' if ped < 1 and dep else
                       'demand here is elastic, so dollar export earnings fall.' if ped > 1 else 'demand here is inelastic, so dollar export earnings rise despite lower volumes.'),
            'key': '(a) [2] (b) [1] (c) [1] (d) Marshall–Lerner/J-curve/other factors [3] [7]', 'marks': 7, 'type': 'numerical'}


@t28_4.add('C3', (2, 3, 4, 5), 'numerical')
def t28_4_ml(r, D):
    c = r.choice(COUNTRIES)
    sx, lx = r.choice([0.2, 0.3, 0.4]), r.choice([0.8, 1.0, 1.2])
    sm, lm = r.choice([0.1, 0.2, 0.3]), r.choice([0.5, 0.7, 0.9])
    share = r.choice([20, 25, 30, 40])
    dep = r.choice([10, 15, 20])
    infl = share * dep / 100
    stem = (f'Estimates for {c}: the price elasticity of demand for exports is −{num(sx, 1)} in the short run and −{num(lx, 1)} in the long run; for imports it is −{num(sm, 1)} in the short run and −{num(lm, 1)} in the long run. '
            f'Imports make up {share}% of the consumer price index. The currency depreciates by {dep}%.')
    sr, lr = sx + sm, lx + lm
    if D == 2:
        opts, a = mcq(r, 'It worsens in the short run and improves in the long run', ['It improves in both the short run and the long run', 'It worsens in both the short run and the long run',
                                                                                     'It improves in the short run and worsens in the long run'])
        return {'stem': stem + ' What is the likely effect on the current account?', 'options': opts, 'answer': a,
                'key': f'Short run sum {num(sr, 1)} < 1 (worsens); long run sum {num(lr, 1)} > 1 (Marshall–Lerner met, improves): J-curve.'}
    return {'stem': stem + ' (a) Use the Marshall–Lerner condition to explain the likely effect on the current account in the short run and long run. (b) Estimate the direct effect on the consumer price index of the rise in import prices (assume import prices rise by the full amount of the depreciation).'
                    + (' (c) Explain why the long-run improvement might not happen.' if D >= 4 else ''),
            'answer': f'(a) Short run: {num(sx, 1)} + {num(sm, 1)} = {num(sr, 1)} < 1, so the current account worsens; long run: {num(lx, 1)} + {num(lm, 1)} = {num(lr, 1)} > 1, so it improves (J-curve). '
                      f'(b) {share}% × {dep}% = {num(infl, 1)} percentage points on the CPI. ' + ('(c) Higher import prices may cause wage rises and inflation, eroding the competitive gain; trading partners may retaliate; firms may raise prices; poor non-price competitiveness.' if D >= 4 else ''),
            'key': '(a) short run [2]; long run [1] (b) [1]' + (' (c) [2] [6]' if D >= 4 else ' [4]'), 'marks': 6 if D >= 4 else 4, 'type': 'numerical'}


def _ch28_case(r, D):
    cur, c = _xr(r)
    e0 = r.choice([8, 10, 12, 15])
    e1 = round(e0 * r.choice([1.2, 1.25]), 2)
    infl = r.choice([3, 4, 5])
    cad = r.choice([4, 5, 6])
    intro = (f'Extract: The {cur}, which floats freely, fell from $1 = {num(e0, 2)} {cur} to $1 = {num(e1, 2)} {cur} over the year as investors moved money abroad following a cut in interest rates. '
             f'{c} has a current account deficit of {cad}% of GDP and imports most of its fuel. Inflation has risen to {infl + 3}% from {infl}%. Exporters of manufactured goods report rising orders, '
             'but the central bank is considering intervening to support the currency.')
    parts = [
        lambda r: (f'Calculate the percentage change in the value of the {cur} against the dollar.', f'{num(e0, 2)}/{num(e1, 2)} − 1 = {pchg(chg(1 / e0, 1 / e1))}.', '[2]'),
        lambda r: ('State whether this is a depreciation or a devaluation, and explain why.', 'Depreciation: a fall in a floating rate driven by market forces.', '[2]'),
        lambda r: ('Using a demand and supply diagram, explain how the cut in interest rates caused the fall.', 'Lower returns lead to capital outflows: supply of the currency rises (and demand falls), lowering the equilibrium rate.', '[4]'),
        lambda r: ('Explain why inflation has risen.', 'Import prices, especially fuel, rise in domestic currency (cost-push); higher export demand raises AD.', '[2]'),
        lambda r: ('Explain why the current account may not improve immediately.', 'J-curve: demand is price inelastic in the short run; Marshall–Lerner may not be met yet.', '[3]'),
        lambda r: ('Discuss whether the central bank should intervene to support the currency.', 'For: limit imported inflation, reduce uncertainty, prevent capital flight. Against: uses reserves or higher interest rates that slow growth; depreciation helps exporters and the deficit; depends on inflation target and size of fall; judgement.', '[6]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t28_1, t28_2, t28_3, t28_4], _ch28_case)
XR_SCENES = ['{country} has a floating exchange rate and a current account deficit.', 'The currency of {country} has depreciated by 20% over the past year.',
             '{country} has kept its currency pegged to the US dollar for ten years.']
essay(t28_1, [
    ('Explain the differences between floating, fixed and managed exchange rate systems.',
     'Floating: market D and S; fixed: peg defended by reserves and interest rates; managed: float with intervention; diagrams of intervention.',
     'a fixed exchange rate is better than a floating exchange rate for {country}',
     'Certainty for trade and investment; discipline against inflation; reduces speculation.',
     'Needs reserves; loses monetary independence; no automatic correction of deficits; speculative attacks; floating absorbs shocks; judgement depends on openness and credibility.'),
], XR_SCENES)
essay(t28_2, [
    ('Explain, using a diagram, how a floating exchange rate is determined and why it might change.',
     'Demand from exports, inward investment and hot money; supply from imports and outward investment; equilibrium; shifts from interest rates, inflation, incomes, speculation.',
     'changes in interest rates are the most important influence on the exchange rate of {country}',
     'Hot money flows are large and fast; central banks use interest rates to influence currency.',
     'Trade flows, relative inflation, FDI, speculation and confidence also matter; long-run rates follow competitiveness; judgement.'),
], XR_SCENES)
essay(t28_3, [
    ('Explain the difference between a depreciation and a devaluation, and why a government might devalue its currency.',
     'Depreciation market-driven in floating system; devaluation official in fixed system; reasons: competitiveness, current account, unsustainable peg.',
     'devaluing the currency is the best way for {country} to improve its competitiveness',
     'Immediate fall in export prices and rise in import prices.',
     'Imported inflation erodes the gain; J-curve; retaliation; supply-side improvements are longer lasting; judgement.'),
], XR_SCENES)
essay(t28_4, [
    ('Explain how a depreciation of a country’s currency might affect its current account, using the Marshall–Lerner condition and the J-curve.',
     'Exports cheaper and imports dearer; Marshall–Lerner condition; J-curve because of short-run inelastic demand; diagram of J-curve.',
     'a depreciation of the currency will benefit the economy of {country}',
     'Higher net exports, AD, growth and jobs; improved current account if Marshall–Lerner holds.',
     'Imported inflation and lower real incomes; higher costs of imported inputs; J-curve; foreign-currency debt costs more; depends on elasticities and spare capacity; judgement.'),
    ('Explain how an appreciation of the exchange rate might affect inflation and unemployment.',
     'Cheaper imports lower costs and CPI; dearer exports reduce net exports and AD; job losses in export and import-competing industries.',
     'an appreciation of the currency is more beneficial than harmful for {country}',
     'Lower inflation, higher real incomes, cheaper imported capital and inputs; pressure to raise productivity.',
     'Lower competitiveness, worse current account, unemployment in export industries; depends on size, cause and state of the economy; judgement.'),
], XR_SCENES)
CHAPTERS[28] = [t28_1, t28_2, t28_3, t28_4]

# ============================================================================ 29 Policies to correct imbalances in the current account
POL_CASES = [
    ('{country} imposes a 15% tariff on imported consumer goods.', 'Expenditure-switching policy', 'switches spending from imports to domestic goods.'),
    ('The central bank of {country} devalues the {cur} by 10%.', 'Expenditure-switching policy', 'makes imports dearer and exports cheaper, switching spending to domestic output.'),
    ('The government of {country} raises income tax rates to reduce consumer spending.', 'Expenditure-reducing policy', 'lower disposable income reduces total spending, including on imports.'),
    ('The central bank of {country} raises interest rates to reduce borrowing and spending.', 'Expenditure-reducing policy', 'lower consumption and investment reduce demand for imports.'),
    ('{country} cuts government spending on public sector projects.', 'Expenditure-reducing policy', 'lower AD reduces income and imports.'),
    ('{country} introduces a quota on imported cars.', 'Expenditure-switching policy', 'limits imports so spending switches to domestic cars.'),
    ('{country} subsidises its exporters of {mgood}.', 'Expenditure-switching policy', 'lowers export prices so foreign spending switches to {country}’s goods.'),
    ('The government of {country} funds training to raise productivity in export industries.', 'Supply-side policy', 'improves competitiveness in the long run.'),
]
POL_LABELS = ['Expenditure-switching policy', 'Expenditure-reducing policy', 'Supply-side policy']


def _pol(t, name):
    def fn(r, D):
        d = ctx(r)
        d['cur'] = r.choice(CURS)
        s, lab, why = r.choice(POL_CASES)
        s, why = fill(s.replace('{cur}', d['cur']), d), fill(why, d)
        if D <= 2:
            opts, a = mcq(r, lab, [x for x in POL_LABELS + ['Protection of infant industries only'] if x != lab])
            return {'stem': f'{s} Which type of policy to correct a current account deficit is this?', 'options': opts, 'answer': a, 'key': f'{lab}: {why}'}
        picks = r.sample(POL_CASES, 2 if D <= 4 else 3)
        nums = ['(i)', '(ii)', '(iii)']
        stem = ('Classify each policy as expenditure-switching, expenditure-reducing or supply-side, and explain how it could reduce a current account deficit. '
                + ' '.join(f'{nums[i]} {fill(x[0].replace("{cur}", d["cur"]), d)}' for i, x in enumerate(picks)))
        return {'stem': stem, 'answer': ' '.join(f'{nums[i]} {x[1]}: {fill(x[2], d)}' for i, x in enumerate(picks)),
                'key': ' '.join(f'{nums[i]} {x[1]} [1]; explanation [1]' for i, x in enumerate(picks)) + f' Total [{2 * len(picks)}]', 'marks': 2 * len(picks), 'type': 'explain'}
    fn.__name__ = name
    t.add('C3', (1, 2, 3, 4, 5), 'explain')(fn)


t29_1 = T('Expenditure-switching policies', 'expenditure-switching policies', 'expenditure switching')
mc(t29_1, [
    ('What is an expenditure-switching policy?', 'A policy that changes the relative prices of imports and domestic goods so that spending switches to domestic output', 'Tariffs, quotas, devaluation, export subsidies.',
     ['A policy that reduces total spending in the economy', 'A policy that raises government spending on imports', 'A policy that switches spending from consumption to saving']),
    ('Which is an expenditure-switching policy?', 'A devaluation of the currency', 'Changes relative prices of imports and exports.', ['An increase in income tax', 'A cut in government spending', 'A rise in interest rates']),
    ('How does a tariff help to reduce a current account deficit?', 'It raises the price of imports, so spending switches to domestic goods', 'Expenditure switching.',
     ['It increases the price of exports', 'It reduces domestic incomes', 'It increases the value of the currency']),
    ('Why might expenditure-switching policies be ineffective?', 'Trading partners may retaliate, and demand for imports may be price inelastic', 'Retaliation; low elasticities.',
     ['They always reduce domestic output', 'They reduce import prices', 'They increase the exchange rate']),
    ('Which would be an expenditure-switching policy that is unlikely to break WTO rules?', 'Allowing the currency to depreciate', 'Exchange rate changes are not trade barriers.',
     ['A new import quota', 'An export subsidy', 'An embargo on imports']),
    ('A devaluation will improve the current account in the long run only if', 'the sum of the price elasticities of demand for exports and imports is greater than one', 'Marshall–Lerner.',
     ['demand for exports is price inelastic', 'domestic inflation rises faster than the devaluation', 'trading partners devalue too']),
])
ex(t29_1, [
    ('Explain how a devaluation can be used to reduce a current account deficit.', 'Exports become cheaper in foreign currency and imports dearer in domestic currency; spending switches from imports to domestic goods and foreign demand for exports rises, improving the current account if the Marshall–Lerner condition holds.',
     '1 mark: relative price changes; 1 mark: spending switches; 1 mark: Marshall–Lerner/elasticities [3]'),
    ('Explain two limitations of using tariffs to correct a current account deficit.', 'Retaliation reduces exports; higher prices and inflation; inefficiency in protected industries; demand for imports may be price inelastic; may break WTO rules.',
     '1 mark each for two limitations, 1 mark each for explanation [4]'),
    ('Explain the difference between expenditure-switching and expenditure-reducing policies.', 'Expenditure-switching changes relative prices so that spending moves from imports to domestic goods; expenditure-reducing lowers total spending (AD), which reduces imports as a by-product.',
     '1 mark: switching relative prices; 1 mark: reducing total spending [2]'),
])
_pol(t29_1, 'pol_sw')
errs(t29_1, [
    ('A devaluation of the {cur} will improve {country}’s current account immediately.', 'In the short run demand is price inelastic, so the current account may worsen first (J-curve); improvement depends on the Marshall–Lerner condition.'),
    ('Expenditure-switching policies work by reducing total spending in the economy.', 'They change relative prices so spending switches from imports to domestic goods; reducing total spending is expenditure-reducing.'),
    ('An export subsidy is an expenditure-reducing policy.', 'It lowers export prices to switch foreign spending towards domestic goods, so it is expenditure-switching.'),
])
items(t29_1, 'C2', (1, 2, 3, 4), [
    ('{country} imposes tariffs on imports to reduce its current account deficit, and {country2} retaliates. Explain why the deficit may not fall.',
     'Retaliation reduces {country}’s exports, offsetting the fall in imports; higher import costs may also reduce export competitiveness.',
     '1 mark: exports fall through retaliation; 1 mark: offsets fall in imports [2]'),
    ('{country} devalues its currency, but most of its imports are fuel and medicines. Explain why the devaluation may have little effect on import volumes.',
     'Demand for essential imports with few domestic substitutes is price inelastic, so spending on imports rises with little fall in volume.',
     '1 mark: inelastic demand for essentials; 1 mark: import spending may rise [2]'),
], name='sw_items')


@t29_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t29_1_tar(r, D):
    c = r.choice(COUNTRIES)
    m = r.choice([40, 60, 80, 100, 120])          # import spending $bn before tariff (world prices)
    tar = r.choice([10, 15, 20, 25])
    ped = r.choice([0.4, 0.6, 1.2, 1.5, 2.0])
    dq = -ped * tar
    m1 = m * (1 + dq / 100)                          # at world prices (spending going abroad)
    def_ = r.choice([8, 10, 12, 15])
    rev = m1 * tar / 100
    stem = f'{c} spends ${m}bn a year on imported consumer goods and has a current account deficit of ${def_}bn. It imposes a {tar}% tariff on these imports. The price elasticity of demand for the imports is −{num(ped, 1)}.'
    if D <= 2:
        return cq(r, 1, stem + ' Assuming the full tariff is passed on to consumers, calculate the percentage change in the volume of imports.', pchg(dq), f'−{num(ped, 1)} × {tar}% = {pchg(dq)}.',
                  dis_num(r, dq, pchg, [-tar, -tar / ped]), mcq_D=(1, 2))
    a = (f'(a) Volume of imports changes by −{num(ped, 1)} × {tar}% = {pchg(dq)}. (b) Import spending paid abroad (at world prices) falls from ${m}bn to {bn(m1)}, a fall of {bn(m - m1)}; '
         + (f'the current account deficit would fall to {bn(def_ - (m - m1))} if nothing else changes. ' if def_ > m - m1 else
            f'the current account would move from a deficit of ${def_}bn to a surplus of {bn(m - m1 - def_)} if nothing else changes. '))
    if D == 3:
        return {'stem': stem + ' Assume the full tariff is passed on to consumers. (a) Calculate the percentage change in the volume of imports. (b) Calculate the new value of imports at world prices and the effect on the current account deficit.',
                'answer': a, 'key': '(a) [1] (b) new imports [1]; new deficit [1] [3]', 'marks': 3, 'type': 'numerical'}
    return {'stem': stem + f' Assume the full tariff is passed on to consumers. (a) Calculate the percentage change in the volume of imports. (b) Calculate the new value of imports at world prices and the new deficit, if nothing else changes. (c) Calculate the tariff revenue. (d) Explain why the deficit might not fall by this much.',
            'answer': a + f'(c) {tar}% × {bn(m1)} = {bn(rev)}. (d) Retaliation against exports; higher prices of imported inputs raise export costs; inflation erodes competitiveness; consumers may switch to other imports; the currency may appreciate as imports fall.',
            'key': '(a) [1] (b) [2] (c) [1] (d) two reasons [2] [6]', 'marks': 6, 'type': 'numerical'}


t29_2 = T('Expenditure-reducing policies', 'expenditure-reducing policies', 'contractionary fiscal and monetary policy')
mc(t29_2, [
    ('What is an expenditure-reducing policy?', 'A policy that reduces total spending in the economy, which reduces spending on imports', 'Deflationary fiscal or monetary policy.',
     ['A policy that changes the relative price of imports', 'A policy that bans imports', 'A policy that raises export subsidies']),
    ('Which is an expenditure-reducing policy?', 'An increase in income tax rates', 'Lower disposable income, lower imports.', ['A devaluation', 'A tariff on imports', 'An import quota']),
    ('Why might expenditure-reducing policies cause unemployment?', 'They reduce aggregate demand, which reduces spending on domestic as well as imported goods', 'Output falls.',
     ['They raise import prices', 'They increase exports', 'They reduce the price of domestic goods']),
    ('The marginal propensity to import is 0.25. A fiscal policy reduces national income by $20bn. By how much do imports fall?', '$5bn', '0.25 × 20.',
     ['$15bn', '$0.25bn', '$80bn']),
    ('How might higher interest rates reduce a current account deficit?', 'By reducing consumption and investment, including spending on imports', 'Expenditure-reducing.',
     ['By making imports cheaper', 'By causing the currency to depreciate', 'By raising consumer borrowing']),
    ('Which is a limitation of using higher interest rates to reduce a current account deficit?', 'They may cause the currency to appreciate, making exports less competitive', 'Hot money inflows.',
     ['They make imports more expensive', 'They increase consumer spending', 'They lower the exchange rate']),
])
ex(t29_2, [
    ('Explain how contractionary fiscal policy can reduce a current account deficit.', 'Higher taxes or lower government spending reduce AD and national income; with a marginal propensity to import, spending on imports falls; lower demand may also reduce inflation and improve competitiveness.',
     '1 mark: AD/income fall; 1 mark: imports fall via mpm; 1 mark: lower inflation/competitiveness [3]'),
    ('Explain why expenditure-reducing policies may conflict with other macroeconomic objectives.', 'Lower AD reduces growth and raises unemployment, because spending on domestic goods falls as well as imports.',
     '1 mark: lower growth; 1 mark: higher unemployment [2]'),
    ('Explain why a small marginal propensity to import makes expenditure-reducing policies costly.', 'If only a small share of each extra dollar of income is spent on imports, income must fall by a large amount to reduce imports significantly, causing large output and job losses.',
     '1 mark: small mpm means small fall in imports; 1 mark: large fall in income needed [2]'),
])
_pol(t29_2, 'pol_red')
errs(t29_2, [
    ('Raising interest rates in {country} reduces the current account deficit without any cost to the economy.', 'Lower spending reduces imports but also domestic output and jobs; higher rates may raise the exchange rate, hurting exporters.'),
    ('Expenditure-reducing policies reduce only spending on imports.', 'They reduce total spending, so demand for domestic goods also falls, lowering output and employment.'),
    ('A cut in income tax is an expenditure-reducing policy.', 'A tax cut raises disposable income and spending; an expenditure-reducing policy would raise taxes.'),
])
items(t29_2, 'C2', (1, 2, 3, 4), [
    ('{country} has a current account deficit of 6% of GDP and inflation of 9%. Explain why expenditure-reducing policies might be suitable.',
     'Lower AD reduces both imports and inflationary pressure; lower inflation also improves price competitiveness of exports, helping the current account.',
     '1 mark: reduces imports; 1 mark: also lowers inflation/improves competitiveness [2]'),
    ('{country} has a current account deficit and unemployment of 11%. Explain why expenditure-reducing policies might be unsuitable.',
     'Reducing AD would raise unemployment further and lower growth; expenditure-switching or supply-side policies would be less damaging.',
     '1 mark: higher unemployment; 1 mark: alternative policy [2]'),
], name='red_items')


@t29_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t29_2_mult(r, D):
    c = r.choice(COUNTRIES)
    g = r.choice([5, 8, 10, 12, 15])
    k = r.choice([1.5, 2, 2.5])
    m = r.choice([0.15, 0.2, 0.25, 0.3])
    def_ = r.choice([10, 15, 20, 25])
    dy = g * k
    dm = m * dy
    gdp = r.choice([500, 800, 1000])
    stem = f'To reduce a current account deficit of ${def_}bn, the government of {c} cuts its spending by ${g}bn. The multiplier is {num(k, 1)} and the marginal propensity to import is {num(m, 2)}.'
    if D <= 2:
        return cq(r, 1, stem + ' Calculate the fall in national income.', bn(dy), f'{g} × {num(k, 1)} = {bn(dy)}.', dis_num(r, dy, bn, [g * m, dm, g / k]), mcq_D=(1, 2))
    a = f'(a) ΔY = {g} × {num(k, 1)} = −{bn(dy)}; ΔM = {num(m, 2)} × {bn(dy)} = −{bn(dm)}. (b) New deficit = {bn(def_)} − {bn(dm)} = {bn(def_ - dm)}. '
    if D == 3:
        return {'stem': stem + ' (a) Calculate the fall in national income and the fall in imports. (b) Calculate the new current account deficit, assuming exports are unchanged.',
                'answer': a, 'key': '(a) ΔY [1]; ΔM [1] (b) [1] [3]', 'marks': 3, 'type': 'numerical'}
    need = def_ / (m * k)
    return {'stem': stem + f' GDP is ${gdp}bn. (a) Calculate the fall in national income and the fall in imports. (b) Calculate the new current account deficit, assuming exports are unchanged. '
                    '(c) Calculate the cut in government spending needed to remove the deficit entirely by this method. (d) Comment on the cost of using this policy.',
            'answer': a + f'(c) Need ΔM = {bn(def_)}: ΔY = {bn(def_)}/{num(m, 2)} = {bn(def_ / m)}, so cut G = {bn(def_ / m)}/{num(k, 1)} = {bn(need)}. '
                          f'(d) National income would fall by {bn(def_ / m)}, about {num(100 * def_ / m / gdp, 1)}% of GDP, implying a large rise in unemployment; expenditure-switching or supply-side policies would be less costly.',
            'key': '(a) [2] (b) [1] (c) [2] (d) [2] [7]', 'marks': 7, 'type': 'numerical'}


CONF_CASES = [
    ('{country} raises taxes to cut its current account deficit, and unemployment rises from 5% to 8%.', 'Conflict between the current account and employment', 'lower AD cuts imports but also domestic output and jobs.'),
    ('{country} devalues to reduce its deficit, and inflation rises from 3% to 7%.', 'Conflict between the current account and price stability', 'dearer imports and higher AD raise inflation.'),
    ('{country} raises interest rates to reduce spending on imports, and the currency appreciates, hurting exporters.', 'Policy partly self-defeating', 'appreciation reduces export competitiveness.'),
    ('{country} cuts government spending to reduce its deficit, and economic growth falls to 0.5%.', 'Conflict between the current account and economic growth', 'lower AD reduces real output growth.'),
    ('{country} invests in training and infrastructure; the current account improves slowly over a decade with growth and low inflation.', 'No conflict: supply-side improvement', 'higher productivity improves competitiveness without reducing AD.'),
]
CONF_LABELS = ['Conflict between the current account and employment', 'Conflict between the current account and price stability', 'Policy partly self-defeating',
               'Conflict between the current account and economic growth', 'No conflict: supply-side improvement']

t29_3 = T('Effectiveness of policies and conflicts with other macroeconomic objectives', 'effectiveness of policies', 'conflicts with other macroeconomic objectives', 'policy conflicts')
mc(t29_3, [
    ('Which policy to reduce a current account deficit is most likely to conflict with low unemployment?', 'Higher income tax rates', 'Expenditure-reducing lowers AD and output.',
     ['Investment in training', 'Improved infrastructure', 'Lower corporate tax on exporters']),
    ('Why might a devaluation conflict with the objective of low inflation?', 'It raises the price of imports and increases aggregate demand', 'Imported cost-push and demand-pull.',
     ['It reduces the price of imports', 'It reduces aggregate demand', 'It lowers wages']),
    ('Which policy is least likely to conflict with other macroeconomic objectives in the long run?', 'Supply-side policies that raise productivity', 'Shift LRAS right.',
     ['Higher interest rates', 'Large tax increases', 'Cuts in government spending']),
    ('Why might supply-side policies not be suitable for correcting a current account deficit quickly?', 'They take a long time to have an effect', 'Long time lags.',
     ['They always reduce exports', 'They increase import prices immediately', 'They reduce productivity']),
    ('A government that combines expenditure-switching and expenditure-reducing policies is most likely aiming to', 'switch spending to domestic goods while preventing excess demand and inflation', 'Make room in the economy for extra net exports.',
     ['increase total spending', 'raise imports', 'cause the currency to appreciate']),
    ('Higher interest rates used to cut a current account deficit may be self-defeating because they', 'attract capital inflows that cause the currency to appreciate', 'Exports dearer, imports cheaper.',
     ['make imports more expensive', 'reduce capital inflows', 'cause the currency to depreciate']),
])
ex(t29_3, [
    ('Explain why a policy to reduce a current account deficit may conflict with economic growth.', 'Expenditure-reducing policies lower AD, reducing spending on domestic goods as well as imports, so real GDP growth falls.',
     '1 mark: lower AD; 1 mark: lower growth/output [2]'),
    ('Explain why the effectiveness of policies to correct a current account deficit depends on its cause.', 'A cyclical deficit from booming demand suits expenditure-reducing policy; a structural deficit from low competitiveness needs supply-side reform; an overvalued currency may need depreciation.',
     '1 mark: cyclical vs structural; 1 mark: matching policy [2]'),
    ('Explain why supply-side policies may be the most effective long-run solution to a current account deficit.', 'They raise productivity and quality, lowering costs and improving price and non-price competitiveness, so exports rise and imports fall without reducing AD or raising inflation.',
     '1 mark: competitiveness; 1 mark: no conflict with growth/inflation [2]'),
])
classify(t29_3, CONF_CASES, CONF_LABELS, 'Which outcome does this illustrate?', 'For each case, identify the outcome of the policy for macroeconomic objectives and explain it.', name='conf')
errs(t29_3, [
    ('Using higher interest rates to cut the current account deficit of {country} will also boost growth.', 'Higher rates reduce consumption and investment, so AD and growth fall; there is a conflict of objectives.'),
    ('Supply-side policies will remove {country}’s current account deficit within a few months.', 'Supply-side policies have long time lags; productivity and competitiveness improve slowly.'),
    ('Every policy to correct a current account deficit conflicts with low inflation.', 'Expenditure-reducing policies lower AD and so reduce inflation; it is expenditure-switching policies such as devaluation that tend to raise it.'),
])
items(t29_3, 'C2', (1, 2, 3, 4), [
    ('{country} has a current account deficit, inflation of 2% and unemployment of 9%. Explain which type of policy would cause the least conflict with its other objectives.',
     'With low inflation and high unemployment, expenditure-switching (e.g. depreciation) raises net exports and AD, helping both the deficit and jobs; supply-side policy helps in the long run; expenditure-reducing would raise unemployment.',
     '1 mark: expenditure-switching/supply-side; 1 mark: justified by unemployment and low inflation [2]'),
    ('{country} has a current account deficit, inflation of 10% and unemployment of 3%. Explain why expenditure-reducing policies may cause little conflict.',
     'With excess demand, lower AD cuts imports and inflation together; with low unemployment, the rise in joblessness may be limited.',
     '1 mark: reduces imports and inflation; 1 mark: economy near full employment [2]'),
], name='conf_items')


@t29_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t29_3_data(r, D):
    c = r.choice(COUNTRIES)
    cur = r.choice(CURS)
    dev = r.choice([10, 15, 20])
    share = r.choice([20, 30, 40])
    infl0 = r.choice([2, 3, 4])
    ca = [r.choice([-6.0, -5.5, -5.0])]
    ca.append(ca[0] - r.choice([0.5, 0.8, 1.0]))
    ca.append(ca[1] + r.choice([0.5, 1.0]))
    ca.append(ca[2] + r.choice([1.2, 1.5, 2.0]))
    ca.append(ca[3] + r.choice([1.0, 1.5]))
    u = [r.choice([8, 9, 10])]
    u += [u[0], u[0] - 0.5, u[0] - 1.0, u[0] - 1.5]
    infl = infl0 + share * dev / 100
    tbl = '; '.join(f'year {i}: {num(ca[i], 1)}%' for i in range(5))
    stem = (f'{c} devalued the {cur} by {dev}% at the start of year 1. Imports make up {share}% of its consumer price index. Current account balance as % of GDP: {tbl} (year 0 is before the devaluation). '
            f'Unemployment fell from {num(u[0], 1)}% in year 0 to {num(u[4], 1)}% in year 4.')
    if D <= 2:
        opts, a = mcq(r, 'A J-curve effect', ['The Marshall–Lerner condition was met immediately', 'An expenditure-reducing policy', 'A revaluation'])
        return {'stem': stem.replace(' Unemployment', ' Unemployment') + ' What does the pattern of the current account after the devaluation show?', 'options': opts, 'answer': a,
                'key': 'The balance worsens in year 1 then improves: a J-curve.'}
    a = (f'(a) The deficit widened from {num(-ca[0], 1)}% to {num(-ca[1], 1)}% of GDP in year 1, then narrowed to {num(-ca[4], 1)}% by year 4: a J-curve, as demand was inelastic in the short run and became more elastic later (Marshall–Lerner met). '
         f'(b) Direct effect on inflation ≈ {share}% × {dev}% = {num(share * dev / 100, 1)} percentage points, so inflation may rise from {infl0}% to about {num(infl, 1)}%. ')
    if D == 3:
        return {'stem': stem + f' Inflation was {infl0}% before the devaluation. (a) Describe and explain the change in the current account. (b) Estimate the direct effect of the devaluation on inflation, assuming import prices rise by the full devaluation.',
                'answer': a, 'key': '(a) description [1]; J-curve explanation [1] (b) [2] [4]', 'marks': 4, 'type': 'numerical'}
    return {'stem': stem + f' Inflation was {infl0}% before the devaluation. (a) Describe and explain the change in the current account. (b) Estimate the direct effect of the devaluation on inflation, assuming import prices rise by the full devaluation. '
                    '(c) Explain the change in unemployment. (d) Evaluate whether the devaluation was a successful policy.',
            'answer': a + '(c) Higher net exports raise AD and output, increasing demand for labour. (d) Current account improved and unemployment fell, but inflation rose and real incomes fell; the deficit remains; success depends on whether competitiveness gains last as wages respond and whether supply-side policies follow; judgement.',
            'key': '(a) [2] (b) [2] (c) [1] (d) evaluation [3] [8]', 'marks': 8, 'type': 'numerical'}


def _ch29_case(r, D):
    c = r.choice(COUNTRIES)
    cur = r.choice(CURS)
    cad = r.choice([5, 6, 7])
    u = r.choice([4, 9, 11])
    infl = r.choice([2, 8, 10])
    m = r.choice([0.2, 0.25, 0.3])
    intro = (f'Extract: {c} has a current account deficit of {cad}% of GDP, unemployment of {u}% and inflation of {infl}%. The finance minister proposes higher income tax to cut spending; '
             f'the central bank prefers to let the {cur} depreciate; business leaders call for tariffs on imported consumer goods; economists argue that only supply-side reforms will solve the problem. '
             f'The marginal propensity to import is {num(m, 2)}.')
    parts = [
        lambda r: ('Classify each of the four proposals as expenditure-switching, expenditure-reducing or supply-side.', 'Higher income tax: expenditure-reducing; depreciation and tariffs: expenditure-switching; supply-side reforms: supply-side.', '[2]'),
        lambda r: ('Calculate the fall in national income needed to reduce imports by $6bn.', f'ΔY = 6/{num(m, 2)} = {bn(6 / m)}.', '[2]'),
        lambda r: ('Explain how a depreciation could reduce the deficit, and why it might not do so at first.', 'Exports cheaper, imports dearer; J-curve and Marshall–Lerner condition.', '[4]'),
        lambda r: (f'Explain which policy is likely to cause the greatest conflict with {c}’s other macroeconomic objectives.', ('Higher income tax: with high unemployment, lower AD would raise unemployment further.' if u >= 9 else
                                                                                                                   'Depreciation or tariffs: with high inflation, higher import prices would add to inflation.' if infl >= 8 else 'Higher income tax lowers growth; depreciation raises inflation; depends on the economy.'), '[3]'),
        lambda r: ('Discuss which policy the government should choose.', 'Compare effectiveness, time lags, conflicts with unemployment and inflation, retaliation, cause of the deficit; combination of policies; judgement.', '[6]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


case([t29_1, t29_2, t29_3], _ch29_case)
POL_SCENES = ['{country} has a current account deficit of 6% of GDP and unemployment of 9%.', '{country} has a current account deficit, rising inflation and a floating exchange rate.',
              'The government of {country} wants to reduce its current account deficit before the next election.']
essay(t29_1, [
    ('Explain how expenditure-switching policies can be used to reduce a current account deficit.',
     'Tariffs, quotas, export subsidies, devaluation; change relative prices; Marshall–Lerner and J-curve; retaliation.',
     'a devaluation is the most effective way for {country} to reduce its current account deficit',
     'Changes all relative prices at once; no WTO problems; boosts AD where there is spare capacity.',
     'J-curve, Marshall–Lerner, imported inflation, wage responses erode gains, structural causes need supply-side policy; judgement.'),
], POL_SCENES)
essay(t29_2, [
    ('Explain how expenditure-reducing policies can reduce a current account deficit.',
     'Contractionary fiscal (taxes up, spending down) and monetary (interest rates up) policy; lower AD and income; mpm; lower inflation improves competitiveness.',
     'expenditure-reducing policies are the best way to correct a current account deficit in {country}',
     'Effective for cyclical deficits with excess demand; lower inflation helps competitiveness.',
     'Unemployment and lower growth; small mpm means large income loss; higher interest rates may appreciate the currency; structural causes; judgement.'),
], POL_SCENES)
essay(t29_3, [
    ('Explain why policies to reduce a current account deficit may conflict with other macroeconomic objectives.',
     'Expenditure-reducing vs growth and employment; expenditure-switching vs inflation; interest rates and exchange rate; supply-side lags.',
     'it is impossible for {country} to reduce its current account deficit without harming other macroeconomic objectives',
     'Most short-run policies trade off growth, employment or inflation.',
     'Supply-side policies avoid conflict in the long run; depends on state of the economy (spare capacity, inflation); policy mix; judgement.'),
], POL_SCENES)
CHAPTERS[29] = [t29_1, t29_2, t29_3]


# ----------------------------------------------------------------------------- final pass: marks from keys, minus signs
_TOT = re.compile(r'\[(\d+)\]\s*$')
_NEG = re.compile(r'(?<![\w\d)\]])-(?=[$\d])')


def _tidy(s):
    return _NEG.sub('−', s) if isinstance(s, str) else s


_MCQ_SEEN = {}


def _norm(s):
    s = re.sub(r'\([a-d]\)', ' ', s.lower())
    s = re.sub(r'[^\w\u0900-\u097F]+|_', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def _sh(n):
    w = n.split(' ')
    return {n} if len(w) < 3 else {' '.join(w[i:i + 3]) for i in range(len(w) - 2)}


def _mcq_clash(ch, q):
    """The validator compares MCQ stems together with their (sorted) options; reject an MCQ that would be a near-duplicate
    of one already produced in this chapter, so the generator moves on to another candidate."""
    n = _norm(q['stem'] + ' ' + ' '.join(sorted(map(str, q['options']))))
    sh = _sh(n)
    lst = _MCQ_SEEN.setdefault(ch, [])
    for sh2, ln2, n2 in lst:
        if n2 == n or min(len(n), ln2) / max(len(n), ln2) < 0.7:
            continue
        i = len(sh & sh2)
        if i / (len(sh) + len(sh2) - i or 1) >= 0.84:
            return True
    lst.append((sh, len(n), n))
    return False


def _finish(fn, cap, ch):
    def g(r, D):
        q = fn(r, D)
        if not q:
            return q
        for k in ('stem', 'answer', 'key'):
            q[k] = _tidy(q.get(k, ''))
        if q.get('options'):
            q['options'] = [_tidy(o) for o in q['options']]
            q['answer'] = _tidy(q['answer'])
            q.setdefault('marks', 1)
            if _mcq_clash(ch, q):
                return None
        elif 'marks' not in q:
            m = _TOT.search(q['key'])
            if m:
                q['marks'] = max(1, min(cap, int(m.group(1))))
        if not q.get('options') and q.get('marks') and q.get('type') not in ('case', 'long'):
            m = _TOT.search(q['key'])
            if not m:
                q['key'] = q['key'].rstrip() + f' [{q["marks"]}]'
            elif int(m.group(1)) != q['marks']:
                q['key'] = q['key'].rstrip() + f' Total [{q["marks"]}]'
        return q
    g.__name__ = fn.__name__
    return g


for _ch, _tps in CHAPTERS.items():
    for _tp in _tps:
        for _tpl in _tp.templates:
            _tpl.fn = _finish(_tpl.fn, 6 if _tpl.name in ('fixed', 'items') or _tpl.name.endswith('_items') else 20, _ch)
