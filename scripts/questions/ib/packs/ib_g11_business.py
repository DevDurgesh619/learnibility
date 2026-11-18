"""IB DP Business Management SL/HL (first assessment 2024) - ib-g11-business, year 1 (Units 1-3).

Assessment model mirrored in the items (the cost sheet marks the paper totals as UNVERIFIED):
  Paper 1 (pre-released statement + unseen case, 30 marks): define [2], explain [4], analyse/apply a
          business management tool [4], discuss [10], evaluate and recommend [10].
  Paper 2 (quantitative, ~50 marks): calculations [2]/[4], construct and interpret (cash-flow forecast,
          break-even, ratios, investment appraisal, decision tree) [6], analyse [8], recommend [10] and an
          extended response using a BM concept (change, creativity, ethics, sustainability) [20].
  Paper 3 HL (social enterprise case, 25 marks): describe a human need [2], explain [4], analyse [4],
          recommend [15].
Command terms follow the 2024 guide (define, describe, outline, state, explain, analyse, apply, comment,
distinguish, calculate, construct, prepare, discuss, evaluate, examine, justify, recommend, to what extent).
Long answers carry markband keys; calculations carry M1/A1 keys and compute their own answers.
Numbers in parametric items are for fictional firms; real organizations appear in cases with rounded,
public facts. The shared machinery (markbands, mock-only templates, social-enterprise cases) is reused by
ib_g12_business.py.
"""
from __future__ import annotations

from _common import F, Registry, T, mcq, name, two_names, CITIES  # noqa: F401

CONFIG = {'minutesPerMark': 2.0, 'mcqMinutes': 1.5}

# One HL mock = Paper 1 (5 items, 30 marks) + Paper 2 (6 items, 50 marks) + Paper 3 (4 items, 25 marks) = 15 items, 105 marks.
MOCK = [
    dict(section='Paper 1 (a) - Define (pre-released statement / case)', count=1, c=['C1'], d=[2], type='short', marks=2, style='p1def'),
    dict(section='Paper 1 (b) - Explain', count=1, c=['C2'], d=[3], type='explain', marks=4, style='p1exp'),
    dict(section='Paper 1 (c) - Analyse using the case', count=1, c=['C3'], d=[3], type='case', marks=4, style='p1ana'),
    dict(section='Paper 1 (d) - Discuss', count=1, c=['C4'], d=[4], type='long', marks=10, style='p1disc'),
    dict(section='Paper 1 (e) - Evaluate and recommend', count=1, c=['C4'], d=[5], type='long', marks=10, style='p1rec'),
    dict(section='Paper 2 (a) - Calculate', count=1, c=['C3'], d=[2], type='numerical', marks=2, style='calc', chapters=[10, 11, 12, 13, 14]),
    dict(section='Paper 2 (b) - Calculate', count=1, c=['C3'], d=[3], type='numerical', marks=4, style='calc', chapters=[10, 11, 12, 13, 14]),
    dict(section='Paper 2 (c) - Construct / prepare and interpret', count=1, c=['C3'], d=[4], type='numerical', marks=6, style='calc', chapters=[10, 11, 12, 13, 14]),
    dict(section='Paper 2 (d) - Analyse', count=1, c=['C4'], d=[3], type='case', marks=8, style='p2ana'),
    dict(section='Paper 2 (e) - Recommend', count=1, c=['C4'], d=[4], type='long', marks=10, style='p1rec'),
    dict(section='Paper 2 (f) - Extended response using a BM concept', count=1, c=['C4'], d=[5], type='long', marks=20, style='concept20'),
    dict(section='Paper 3 (a) - Describe the human need', count=1, c=['C1'], d=[2], type='short', marks=2, style='p3a'),
    dict(section='Paper 3 (b) - Explain', count=1, c=['C2'], d=[3], type='explain', marks=4, style='p3b'),
    dict(section='Paper 3 (c) - Analyse', count=1, c=['C3'], d=[3], type='case', marks=4, style='p3c'),
    dict(section='Paper 3 (d) - Recommend', count=1, c=['C4'], d=[5], type='long', marks=15, style='p3d'),
]

MB10 = ('BM markbands [10]: 9-10 – relevant knowledge and understanding; terms defined; effective use of the case/stimulus '
        'and relevant business management tools; balanced analysis of advantages and disadvantages for stakeholders; a '
        'reasoned, substantiated judgement or recommendation. 7-8 – good understanding and use of the case, balanced '
        'analysis, judgement partly substantiated. 5-6 – some understanding, analysis mostly one-sided or not fully linked '
        'to the case, limited judgement. 3-4 – limited understanding, mostly descriptive. 1-2 – little relevant knowledge. '
        'Answers without explicit reference to the case or organization cannot reach the top bands.')
MB20 = ('BM concept markbands [20], five criteria: A knowledge and understanding of the concept and content (4); B application '
        'to a real organization (4); C reasoned arguments supported by evidence (4); D structure (4); E individuals and '
        'societies – perspectives of different stakeholders (4). Top band in each: precise, well-integrated, balanced and '
        'substantiated; the concept (change, creativity, ethics or sustainability) shapes the whole answer.')
MB15 = ('Paper 3 recommendation markbands [15]: 13-15 – a clear recommendation of one option, justified with the case and '
        'relevant tools; both options weighed against the human need and the social enterprise\'s resources and stakeholders; '
        'limitations of the data acknowledged. 10-12 – recommendation supported, analysis of both options but uneven. '
        '7-9 – some analysis, recommendation partly justified. 4-6 – mostly descriptive. 1-3 – little relevant content.')
STYLE = {'eval_marks': 10, 'essay_marks': 10, 'markband': MB10}
CONCEPTS = ('change', 'creativity', 'ethics', 'sustainability')

# Social enterprises for Paper 3 (name, context, human need, decision, option A, option B, key considerations).
SE = [
    ('Grameen Bank (Bangladesh)', 'Grameen Bank, founded by Muhammad Yunus in 1983, lends small amounts without collateral, mainly to poor rural women organised in borrower groups; it has over 9 million members.',
     'access to finance (credit and savings) for people excluded from formal banking, enabling income and security',
     'expanding its services', 'launch a mobile-phone savings and loans app for younger urban borrowers', 'open 200 new village branches in the poorest districts',
     'cost and digital literacy of members; reach to the poorest; group-lending model and trust; competition from bKash and other mobile money providers; staff retraining'),
    ('SELCO India', 'SELCO, founded in Bengaluru in 1995, sells and finances solar lighting and energy systems for low-income households and micro-enterprises, often through partnerships with rural banks.',
     'reliable, affordable energy (lighting and power) for households without a stable electricity supply',
     'growing its impact', 'franchise its model to local entrepreneurs in other states', 'keep all operations in-house and grow organically',
     'control over quality and mission; speed of growth; finance available; local knowledge of franchisees; brand reputation'),
    ('Aravind Eye Care System (India)', 'Aravind, founded in 1976 in Madurai, performs hundreds of thousands of cataract operations a year; paying patients cross-subsidise free or low-cost surgery for the poor using assembly-line style processes.',
     'access to affordable eye care to prevent avoidable blindness',
     'reaching rural patients', 'build a new hospital in a large city with many paying patients', 'open 50 small rural vision centres linked by telemedicine',
     'cross-subsidy needs paying patients; rural reach and the human need; capital cost; staffing of doctors; quality control'),
    ('Who Gives A Crap (Australia)', 'Who Gives A Crap sells recycled and bamboo toilet paper online and donates 50% of its profits to charities building toilets and sanitation in developing countries.',
     'access to safe sanitation for the roughly 3.5 billion people without safely managed sanitation',
     'distribution', 'sell through major supermarket chains', 'remain online-only with subscription deliveries',
     'margins and the share of profit donated; brand values and customer loyalty; volume growth; supermarket power; environmental footprint of delivery'),
    ('Divine Chocolate (UK/Ghana)', 'Divine Chocolate is co-owned by Kuapa Kokoo, a cooperative of over 100,000 cocoa farmers in Ghana, who receive Fairtrade prices, a premium and a share of profits.',
     'fair and stable incomes for smallholder cocoa farmers',
     'product range', 'launch a premium organic range at a higher price', 'cut prices to compete with mass-market brands',
     'farmers\' income and premium; price elasticity; brand positioning; supply of organic cocoa; competition from large chocolate makers'),
    ('The Big Issue (UK)', 'The Big Issue magazine, launched in 1991, is sold on the street by homeless and vulnerably housed vendors who buy copies for half the cover price and keep the profit.',
     'a legitimate income and a route out of homelessness',
     'responding to falling print sales', 'invest in a digital subscription linked to vendors', 'expand vendor support services funded by donations',
     'vendors\' income; customers\' shift to cashless payment; cost; mission of "a hand up, not a hand out"; funding stability'),
    ('Mondragon Corporation (Spain)', 'Mondragon is a federation of worker cooperatives in the Basque Country, employing around 70,000 people, where worker-members own the businesses and vote on major decisions.',
     'secure, democratic employment and a fair share of the value workers create',
     'international expansion', 'open a factory in Mexico employing non-member workers', 'expand only through new cooperatives in Spain',
     'cooperative values and worker ownership; labour costs and access to markets; ethics of non-member employees; risk'),
    ('BRAC (Bangladesh)', 'BRAC, founded in 1972, is one of the world\'s largest NGOs, running schools, health programmes, microfinance and social businesses such as Aarong craft shops.',
     'education, health and livelihoods for people living in poverty',
     'funding', 'rely more on revenue from its social businesses', 'seek more grants from international donors',
     'financial sustainability; independence from donors; mission drift; scale of need; risk of business losses'),
    ('Ten Thousand Villages (USA)', 'Ten Thousand Villages, founded in 1946, is a non-profit fair trade retailer selling handicrafts made by artisans in developing countries.',
     'fair, long-term income for artisans in developing countries',
     'retail strategy', 'close half of its physical stores and move to e-commerce', 'keep its stores and add community events',
     'costs of rent; online competition; customer experience and storytelling; artisans\' order volumes'),
    ('Amul (India)', 'Amul is a dairy cooperative owned by about 3.6 million milk producers in Gujarat; it collects milk from villages and markets it nationally under the Amul brand.',
     'a fair and reliable price for small dairy farmers\' milk',
     'new markets', 'export dairy products to the USA and Gulf states', 'focus on expanding rural collection in other Indian states',
     'returns to farmer-members; quality standards for export; capacity; brand strength; risk'),
]

R = Registry()
CONC: dict[str, tuple] = {}


KEEP_CAP = {'Pink', 'Maslow', 'Herzberg', 'Taylor', 'Handy', 'Hofstede', 'Porter', 'Ansoff', 'Lewin', 'Fayol', 'McGregor', 'Adams',
            'Mayo', 'Drucker', 'Kotter', 'Elkington', 'Hall', 'Deming', 'Toyota', 'Apple', 'Amazon', 'Netflix', 'Tesla', 'Google',
            'Microsoft', 'McDonald', 'Unilever', 'Nestlé', 'Patagonia', 'Starbucks', 'Fairtrade', 'Internet', 'English'}


def lc(s):
    w = s.split(' ', 1)[0]
    base = w.split("'")[0].rstrip(',.:;')
    if base in KEEP_CAP or (len(base) > 1 and base[1].isupper()):
        return s
    return s[0].lower() + s[1:]


def cap(s):
    return s[0].upper() + s[1:]


def _key(st):
    return st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]


def make_S(reg, conc):
    def S(key, concepts=CONCEPTS, **kw):
        if 'cases' in kw:
            kw['cases'] = [(c, w, k, cap(h)) for c, w, k, h in kw['cases']]
        reg.facts(key, F(**kw))
        conc[key] = tuple(concepts)
    return S


S = make_S(R, CONC)


def more(key, reg=R, **kw):
    f = reg.f[key]
    if 'cases' in kw:
        kw['cases'] = [(c, w, k, cap(h)) for c, w, k, h in kw['cases']]
    for k, v in kw.items():
        getattr(f, k).extend(v)


def calc(key, c='C3', d=(1, 5), ty='numerical', reg=None):
    reg = reg or R

    def deco(fn):
        reg.t.setdefault(key, []).append(T(c, d, fn, ty, 'calc', fn.__name__))
        return fn
    return deco


def bm_templates(reg, conc, st, style=STYLE):
    """Fact templates + mock-only Paper 1/2/3 templates for one subtopic."""
    key = _key(st)
    out = reg.build(st, style)
    f = reg.f.get(key)
    if not f:
        return out
    concepts = conc.get(key, CONCEPTS)

    def ctx(rng):
        if f.cases:
            case, what, _, _ = rng.choice(f.cases)
            return case, what
        return None, None

    if f.terms:
        def p1def(rng, slot):
            t, d = rng.choice(f.terms)
            case, what = ctx(rng)
            if not case:
                return None
            lab = 'Paper 1 (a). ' if slot.style == 'p1def' else ''
            lead = f'{lab}Read the extract.\n\n{what}\n\nDefine the term "{t}". [2]'
            return dict(stem=lead, answer=cap(d), type='short', marks=2,
                        markingKey=f'[2] for a full, accurate definition: {d}. [1] for a partial definition. Examples alone are not credited.')
        out.append(T('C1', (1, 3), p1def, 'short', 'p1def', 'p1def'))
    if f.why:
        def p1exp(rng, slot):
            q, a = rng.choice(f.why)
            case, what = ctx(rng)
            if not case:
                return None
            lab = 'Paper 1 (b). ' if slot.style == 'p1exp' else ''
            stem = f'{lab}Read the extract.\n\n{what}\n\n{q} Refer to the extract or to another organization you have studied. [4]'
            return dict(stem=stem, answer=a, type='explain', marks=4,
                        markingKey=f'{a} [1] for each relevant point identified and [1] for each point explained and applied to the case (2 × 2). Generic answers without application: maximum [2].')
        out.append(T('C2', (2, 4), p1exp, 'explain', 'p1exp', 'p1exp'))

        def p3b(rng, slot):
            if slot.style != 'p3b':
                return None
            q, a = rng.choice(f.why)
            se = rng.choice(SE)
            return dict(stem=f'Paper 3 (b). {se[1]}\n\n{q} Where relevant, apply your answer to {se[0]}. [4]', answer=a, type='explain', marks=4,
                        markingKey=f'{a} Award [2] for a relevant explanation and [2] for applying it to the social enterprise and its human need ({se[2]}).')
        out.append(T('C2', (2, 4), p3b, 'explain', 'p3b', 'p3b'))
    if f.cases:
        def p1ana(rng, slot):
            case, what, concept, how = rng.choice(f.cases)
            lab = 'Paper 1 (c). ' if slot.style == 'p1ana' else ''
            q = rng.choice([f'Using the extract, analyse how {case} illustrates {concept}. [4]',
                            f'With reference to the extract, analyse what the case of {case} shows about {concept}. [4]',
                            f'Analyse the significance of {concept} for the organization(s) in the extract. [4]',
                            f'Using information from the extract, analyse the link between the organization\'s actions and {concept}. [4]'])
            return dict(stem=f'{lab}Read the extract.\n\n{what}\n\n{q}', answer=how, type='case', marks=4,
                        markingKey=f'{how} [1]-[2]: relevant points with limited use of the extract; [3]-[4]: clear analysis explicitly linked to the extract.', gap='G7')
        out.append(T('C3', (2, 4), p1ana, 'case', 'p1ana', 'p1ana'))

        def p3c(rng, slot):
            if slot.style != 'p3c':
                return None
            case, what, concept, how = rng.choice(f.cases)
            se = rng.choice(SE)
            return dict(stem=f'Paper 3 (c). {se[1]}\n\nUsing the example of {case} ({what}) as a comparison, analyse how {concept} could apply to {se[0]}. [4]',
                        answer=f'{how} Applied to {se[0]}: the same logic must be adapted to its social mission ({se[2]}), limited resources and stakeholders.',
                        type='case', marks=4, gap='G7',
                        markingKey=f'[2] for a relevant, explained point about {concept}; [2] for applying it to {se[0]} and its human need. {how}')
        out.append(T('C3', (2, 4), p3c, 'case', 'p3c', 'p3c'))
    if f.evaluate:
        def p1disc(rng, slot):
            claim, pro, con, judge = rng.choice(f.evaluate)
            case, what = ctx(rng)
            if not case:
                return None
            lab = 'Paper 1 (d). ' if slot.style == 'p1disc' else ''
            lead = f'{lab}{what}\n\n'
            stem = lead + rng.choice([f'Discuss the view that {lc(claim)} [10]', f'"{claim}" With reference to {case or "an organization you have studied"}, discuss this statement. [10]'])
            return dict(stem=stem, answer=judge, type='long', marks=10,
                        markingKey='Arguments for: ' + '; '.join(pro) + '. Arguments against: ' + '; '.join(con) + f'. Judgement: {judge} {MB10}')
        out.append(T('C4', (3, 5), p1disc, 'long', 'p1disc', 'p1disc'))

        def p1rec(rng, slot):
            claim, pro, con, judge = rng.choice(f.evaluate)
            case, what = ctx(rng)
            frames = [f'The management team is divided. One manager argues that {lc(claim)} Evaluate this view and recommend a course of action. [10]',
                      f'A consultant claims that {lc(claim)} Evaluate this claim and make a justified recommendation. [10]',
                      f'Using the information and your knowledge of business management, evaluate whether {lc(claim).rstrip(".")}, and recommend what the organization should do. [10]',
                      f'The board must decide whether to act on the view that {lc(claim)} Recommend a course of action, weighing the arguments for and against. [10]']
            fr = rng.choice(frames)
            stem = f'{what}\n\n{fr}' if case else fr
            return dict(stem=stem, answer=judge, type='long', marks=10,
                        markingKey='Supporting: ' + '; '.join(pro) + '. Challenging: ' + '; '.join(con) + f'. Recommendation: {judge} {MB10}')
        out.append(T('C4', (3, 5), p1rec, 'long', 'p1rec', 'p1rec'))

        def p2ana(rng, slot):
            claim, pro, con, judge = rng.choice(f.evaluate)
            case, what = ctx(rng)
            stem = (f'{what}\n\nUsing the extract where relevant, analyse the advantages and disadvantages of acting on the view that {lc(claim)} [8]' if case
                    else f'Analyse the advantages and disadvantages of acting on the view that {lc(claim)} [8]')
            return dict(stem=stem, answer=judge, type='case', marks=8,
                        markingKey='Advantages: ' + '; '.join(pro) + '. Disadvantages: ' + '; '.join(con) +
                        '. 7-8: balanced analysis applied to the case; 5-6: analysis of both sides, partly applied; 3-4: one-sided or generic; 1-2: descriptive.')
        out.append(T('C4', (3, 5), p2ana, 'case', 'p2ana', 'p2ana'))

        def concept20(rng, slot):
            if slot.style != 'concept20':
                return None
            claim, pro, con, judge = rng.choice(f.evaluate)
            c = rng.choice(concepts)
            stem = rng.choice([f'Using the concept of {c}, discuss the view that {lc(claim)} Refer to at least one real organization you have studied. [20]',
                               f'With reference to one or two organizations you have studied, examine how the concept of {c} affects the claim that {lc(claim)} [20]'])
            return dict(stem=stem, answer=judge, type='long', marks=20,
                        markingKey=f'Concept: {c}. Arguments for: ' + '; '.join(pro) + '. Arguments against: ' + '; '.join(con) + f'. Possible conclusion: {judge} {MB20}')
        out.append(T('C4', (4, 5), concept20, 'long', 'concept20', 'concept20'))

    def p3a(rng, slot):
        if slot.style != 'p3a':
            return None
        se = rng.choice(SE)
        return dict(stem=f'Paper 3 (a). {se[1]}\n\nDescribe the human need that {se[0]} is addressing. [2]', answer=cap(se[2]), type='short', marks=2,
                    markingKey=f'[1] for identifying the human need ({se[2]}); [1] for describing it with reference to the case.')
    out.append(T('C1', (1, 3), p3a, 'short', 'p3a', 'p3a'))

    def p3d(rng, slot):
        if slot.style != 'p3d':
            return None
        se = rng.choice(SE)
        nm, txt, need, area, a, b, cons = se
        return dict(stem=f'Paper 3 (d). {txt}\n\nTo meet its human need, {nm} is considering two options for {area}:\nOption 1: {a}.\nOption 2: {b}.\n\nUsing the case and your knowledge of business management, recommend which option {nm} should choose. [15]',
                    answer=f'A justified recommendation of one option weighing: {cons}.', type='long', marks=15,
                    markingKey=f'Relevant considerations: {cons}. Human need: {need}. Either option can be recommended if justified. {MB15}')
    out.append(T('C4', (4, 5), p3d, 'long', 'p3d', 'p3d'))
    return out


def init(subject_id):
    pass


def templates(st):
    return bm_templates(R, CONC, st)


# ---------------------------------------------------------------------------------------------
# numeric helpers
# ---------------------------------------------------------------------------------------------
CURS = ['$', '€', '£']
FIRMS = ['Kofi\'s Bakery', 'NordBike Ltd', 'Lumen Lighting', 'Café Andino', 'Tasman Surf Co.', 'Sakura Stationery', 'Atlas Print',
         'Baobab Juices', 'Fjord Outdoor', 'Medina Textiles', 'Pampas Leather', 'Kiwi Fresh', 'Delta Drones', 'Saffron Spice Co.',
         'Harbour Coffee Roasters', 'Andes Alpaca Wear', 'Zuri Cosmetics', 'Neon Gaming Ltd', 'Mekong Furniture', 'Alpine Ski Rentals']


def firm(rng):
    return rng.choice(FIRMS)


def cur(rng):
    return rng.choice(CURS)


def m(x, c='$'):
    neg = x < 0
    x = abs(x)
    s = f'{int(round(x)):,}' if abs(x - round(x)) < 1e-9 else f'{x:,.2f}'
    return ('−' if neg else '') + c + s


def _hu(x, n):
    from decimal import Decimal, ROUND_HALF_UP
    return str(Decimal(repr(x)).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def p1(x):
    return _hu(x, 1).replace('-', '−')


def p2(x):
    return _hu(x, 2).replace('-', '−')


def MK(steps, ans):
    return f'{steps} [M1] for a correct formula/method with substituted values; [A1] for {ans}. Units (%, $, days, times) required for [A1]. Apply own figure rule (OFR) to later parts.'


# =============================================================================================
# ch01 Unit 1.1 Introduction to business management
# =============================================================================================
S('ch01-st1', concepts=('creativity', 'sustainability', 'change'),
  terms=[('business', 'an organization that uses human, physical and financial resources to produce goods or services to meet the needs and wants of customers'),
         ('human resources', 'the people, their skills and time, that an organization uses to produce goods and services'),
         ('physical resources', 'tangible inputs such as land, buildings, machinery, equipment and raw materials used in production'),
         ('financial resources', 'the money and access to finance that an organization uses to buy other resources and fund its activities'),
         ('goods', 'tangible products that can be seen and touched, such as cars and smartphones'),
         ('services', 'intangible products, such as banking, education and hairdressing, that are consumed as they are produced')],
  facts=[('Which of the following is an example of a physical resource?', 'A delivery van owned by the firm', ['A bank loan', 'A skilled software engineer', 'A brand name'], 'Physical resources are tangible inputs used in production.'),
         ('Which of the following is a service rather than a good?', 'A haircut', ['A loaf of bread', 'A laptop', 'A pair of shoes'], 'Services are intangible.'),
         ('Adding value means:', 'the difference between the price of the final product and the cost of bought-in materials', ['the total revenue of a firm', 'the profit after tax', 'the cost of labour'], 'Value added = selling price − cost of inputs.')],
  why=[('Explain why businesses need to combine human, physical and financial resources to create goods and services.', 'Each resource on its own is unproductive: finance buys machinery and materials, people operate equipment and make decisions, and physical resources transform inputs; combining them creates output of greater value than the inputs.'),
       ('Explain why adding value is important for a business.', 'The value added is the margin from which wages, overheads and profit are paid; a business that adds more value (branding, design, service) can charge higher prices and remain viable.'),
       ('Explain why the purpose of a business is not only to make a profit.', 'Businesses exist to meet customers\' needs and wants; profit rewards owners and funds growth, but many organizations also pursue social, environmental or community goals (e.g. social enterprises).')],
  contrast=[('goods', 'services', 'Goods are tangible products that can be stored and transported; services are intangible, cannot be stored and are usually produced and consumed at the same time.')],
  misc=[('A business only needs money to succeed.', 'Finance is necessary but not sufficient: a business also needs skilled people, physical resources, a product customers want and effective management.'),
        ('Adding value means raising the price as high as possible.', 'Value is added by making the product more desirable (quality, design, convenience, brand) relative to the cost of inputs; simply raising the price without this loses customers.')],
  cases=[('Starbucks', 'Starbucks buys coffee beans that cost a few cents per cup but sells drinks for several dollars, through branding, store design and customer experience.', 'adding value', 'the gap between input costs and price reflects value created by staff, premises and brand'),
         ('IKEA', 'IKEA designs furniture for flat-pack transport and self-assembly, combining design teams, global suppliers, warehouses and customer labour.', 'how businesses combine resources', 'human (designers), physical (warehouses, materials) and financial resources are combined to deliver low-cost furniture'),
         ('Patagonia', 'Patagonia makes outdoor clothing and in 2022 transferred ownership to a trust and a non-profit so that profits not reinvested are used to fight climate change.', 'the purpose of business', 'a business can create goods for customers while using its surplus for environmental goals')],
  evaluate=[('The main purpose of every business is to maximise profit.', ['profit rewards risk-taking owners', 'profit funds investment and survival', 'shareholders of PLCs expect returns'],
             ['social enterprises prioritise social goals', 'long-term survival and reputation may matter more', 'stakeholders expect ethical behaviour', 'start-ups often prioritise growth'], 'Profit is essential for most businesses to survive, but their purpose is to meet needs; the relative importance of profit depends on the type of organization and its stakeholders.')],
  )

S('ch01-st2', concepts=('change', 'creativity'),
  terms=[('human resources (function)', 'the business function responsible for workforce planning, recruitment, training, appraisal, motivation and dismissal of employees'),
         ('finance and accounts', 'the business function that manages money: recording transactions, budgeting, raising finance and preparing final accounts'),
         ('marketing', 'the business function that identifies and satisfies customer needs and wants profitably, through market research and the marketing mix'),
         ('operations management', 'the business function concerned with converting inputs into outputs (goods and services) efficiently and to the required quality')],
  facts=[('Which business function is responsible for recruitment and training?', 'Human resources', ['Marketing', 'Operations', 'Finance'], 'HR manages the workforce.'),
         ('A decision to launch a new product is most likely to require input from:', 'all four business functions', ['marketing only', 'finance only', 'operations only'], 'Functions are interdependent.'),
         ('Which function decides how many units to produce and what production method to use?', 'Operations management', ['Human resources', 'Marketing', 'Finance'], 'Operations converts inputs into outputs.')],
  why=[('Explain why the business functions are interdependent.', 'A decision in one function affects the others: a marketing campaign raises demand, so operations must increase output, HR must recruit staff and finance must fund extra inventory and wages.'),
       ('Explain why poor communication between business functions can harm a business.', 'Functions may pursue conflicting goals (marketing promising delivery dates operations cannot meet), causing waste, delays, unhappy customers and higher costs.'),
       ('Explain why the finance function is important to the other functions.', 'It allocates budgets, raises funds and monitors cash flow and costs; without finance, marketing campaigns, new machinery or recruitment cannot happen.')],
  contrast=[('the marketing function', 'the operations function', 'Marketing identifies and stimulates customer demand (research, product, price, promotion, place); operations produces the goods or services to meet that demand efficiently and to quality.')],
  misc=[('Each business function can make decisions without considering the others.', 'The functions are interrelated: decisions in one (e.g. a price cut in marketing) affect workload, costs and cash flow in the others.')],
  cases=[('Apple\'s product launches', 'Apple\'s iPhone launches require marketing to create anticipation, operations to coordinate suppliers such as Foxconn and TSMC, finance to fund inventory, and HR to staff stores.', 'the interrelationships of business functions', 'a successful launch depends on all functions acting together'),
         ('Boeing 737 MAX', 'After two 737 MAX crashes in 2018-2019 the aircraft was grounded worldwide for about 20 months; investigations highlighted pressure to meet schedules and costs.', 'conflict between business functions', 'financial and marketing pressures overrode engineering and operations concerns, damaging quality and reputation'),
         ('Tesla\'s Model 3 "production hell"', 'In 2017-2018 Tesla had over 400,000 Model 3 reservations but struggled to produce 5,000 cars a week, and Elon Musk described the period as "production hell".', 'interdependence of marketing and operations', 'marketing created demand faster than operations could supply, straining finance and HR')],
  evaluate=[('The marketing function is the most important business function.', ['identifies customer needs and creates revenue', 'shapes product design', 'competitive advantage through branding'],
             ['without operations there is nothing to sell', 'finance controls survival through cash flow', 'HR provides the people for every function', 'importance depends on the industry'], 'No single function is most important; their interdependence means success depends on coordination, although marketing is critical in highly competitive consumer markets.')],
  )


@calc('ch01-st3', 'C3', (1, 4))
def sector_shares(rng, slot):
    e = rng.choice(['Vietnam', 'Kenya', 'Poland', 'Peru', 'Indonesia', 'Morocco', 'a fictional economy, Zedland'])
    y0 = rng.choice([1995, 2000, 2005])
    tot0 = rng.choice([20, 30, 40, 50])
    a0 = rng.choice([45, 50, 55, 60])
    b0 = rng.choice([15, 20, 25])
    c0 = 100 - a0 - b0
    a1 = a0 - rng.choice([15, 20, 25])
    b1 = b0 + rng.choice([2, 5, 8])
    c1 = 100 - a1 - b1
    tot1 = tot0 + rng.choice([5, 8, 10])
    ch_c = c1 * tot1 / 100 - c0 * tot0 / 100
    stem = rng.choice([f'In {e}, {tot0} million people were employed in {y0}: {a0}% in the primary sector, {b0}% in the secondary sector and {c0}% in the tertiary sector. By {y0 + 20}, employment was {tot1} million, with {a1}% primary and {b1}% secondary; the rest worked in the tertiary sector.',
                       f'Employment data ({e}): {y0} – total {tot0} million (primary {a0}%, secondary {b0}%, tertiary {c0}%); {y0 + 20} – total {tot1} million (primary {a1}%, secondary {b1}%, tertiary {c1}%).'])
    if slot.d <= 2:
        return dict(stem=stem + f' Calculate the percentage of workers in the tertiary sector in {y0 + 20}, and identify the type of sectoral change.',
                    answer=f'Tertiary = 100 − {a1} − {b1} = {c1}%; sectoral change from primary towards secondary and tertiary (industrialisation and the growth of services).',
                    markingKey=MK(f'100 − {a1} − {b1} = {c1}%.', f'{c1}%') + ' [R1] direction of change.', marks=2)
    return dict(stem=stem + f' Calculate the change in the number of people employed in the tertiary sector between {y0} and {y0 + 20}, and explain one reason for the change.',
                answer=f'Tertiary: {c0}% × {tot0} m = {c0 * tot0 / 100:.1f} m → {c1}% × {tot1} m = {c1 * tot1 / 100:.1f} m, a rise of {ch_c:.1f} million. Reason: rising incomes increase demand for services (tourism, finance, retail, health), and productivity gains in agriculture release labour.',
                markingKey=MK(f'{c0}/100 × {tot0} = {c0 * tot0 / 100:.1f}; {c1}/100 × {tot1} = {c1 * tot1 / 100:.1f}; difference {ch_c:.1f}.', f'{ch_c:.1f} million') + ' [R1] reason.', marks=4)


S('ch01-st3', concepts=('change', 'sustainability'),
  terms=[('primary sector', 'the sector of the economy that extracts or harvests natural resources, such as agriculture, fishing, forestry and mining'),
         ('secondary sector', 'the sector that manufactures and processes raw materials into finished or semi-finished goods, including construction'),
         ('tertiary sector', 'the sector that provides services to consumers and businesses, such as retail, banking, tourism and health care'),
         ('quaternary sector', 'the sector based on knowledge and information, such as research and development, ICT, consultancy and financial planning'),
         ('sectoral change', 'the shift in the relative importance of each sector of the economy, measured by output or employment, over time'),
         ('deindustrialisation', 'the decline in the relative importance of the secondary (manufacturing) sector in an economy')],
  facts=[('A copper mine in Chile operates in which sector?', 'Primary', ['Secondary', 'Tertiary', 'Quaternary'], 'Extraction of natural resources.'),
         ('Which of the following is part of the quaternary sector?', 'A software research laboratory', ['A car assembly plant', 'A dairy farm', 'A supermarket'], 'Knowledge-based activity.'),
         ('As economies develop, the share of employment in the tertiary sector usually:', 'rises', ['falls', 'stays constant', 'falls to zero'], 'Demand for services rises with income.'),
         ('Deindustrialisation refers to a decline in the relative importance of:', 'the secondary sector', ['the primary sector', 'the tertiary sector', 'exports'], 'Manufacturing\'s share of output and jobs falls.')],
  why=[('Explain why the tertiary sector grows as an economy becomes richer.', 'Demand for services such as tourism, health, education and finance is income elastic, so it rises faster than incomes, while productivity gains in agriculture and manufacturing release labour.'),
       ('Explain why deindustrialisation has occurred in many high-income countries.', 'Manufacturing has moved to lower-cost countries through globalisation, automation has reduced the number of factory jobs, and demand has shifted towards services.'),
       ('Explain why sectoral change may cause structural unemployment.', 'Workers in declining sectors (e.g. coal mining) may lack the skills or be in the wrong location for jobs in growing sectors, so they remain unemployed.')],
  contrast=[('the tertiary sector', 'the quaternary sector', 'The tertiary sector provides services to customers (retail, transport, hospitality); the quaternary sector is a subset of knowledge-based services (R&D, ICT, consultancy) that create and process information.')],
  misc=[('The primary sector is unimportant in high-income countries.', 'It employs few people, but it provides essential raw materials, food and energy, and can be highly productive and export-oriented (e.g. Australian mining, Norwegian oil).')],
  cases=[('China\'s sectoral change', 'Agriculture\'s share of employment in China fell from about 70% in 1978 to around 23% by 2023, while industry and services expanded.', 'sectoral change in an emerging economy', 'rapid industrialisation and urbanisation moved workers from farming into factories and services'),
         ('the decline of UK manufacturing', 'Manufacturing employed about 25% of UK workers in 1980 but under 8% by the 2020s, while services account for around 80% of output.', 'deindustrialisation', 'the economy shifted from secondary to tertiary and quaternary activities'),
         ('India\'s IT services sector', 'India\'s IT and business services exports, led by firms such as TCS and Infosys, were worth around $190 bn in 2023-24.', 'growth of the tertiary and quaternary sectors', 'an educated, English-speaking workforce allowed India to grow services exports before a large manufacturing base developed')],
  evaluate=[('Sectoral change from manufacturing to services is beneficial for an economy.', ['services offer higher value added and wages in some areas', 'less pollution than heavy industry', 'responds to changing consumer demand'],
             ['structural unemployment in former industrial regions', 'many service jobs are low-paid and insecure', 'loss of manufacturing capability and supply-chain resilience', 'trade deficit in goods'], 'It is beneficial in the long run if workers can retrain and move, but the transition creates regional and social costs that require policy support.')],
  )

S('ch01-st4', concepts=('creativity', 'change'),
  terms=[('entrepreneur', 'a person who identifies a business opportunity and organizes resources, taking financial risks, to start and run a new business'),
         ('intrapreneur', 'an employee who acts like an entrepreneur within an existing organization, developing new products or processes'),
         ('start-up', 'a newly established business, often in its early stage of development'),
         ('business plan', 'a document setting out the objectives of a business, its strategies and how it will achieve them, including marketing, operations and financial forecasts'),
         ('venture capital', 'finance provided to high-risk, high-potential start-ups in exchange for a share of ownership')],
  facts=[('Which of the following is a common reason for starting a business?', 'Independence and the desire to be one\'s own boss', ['To pay higher taxes', 'To reduce risk', 'To work fewer hours guaranteed'], 'Autonomy is a major motive.'),
         ('Google\'s policy that allowed engineers time for their own projects, leading to products such as Gmail, encouraged:', 'intrapreneurship', ['franchising', 'outsourcing', 'delayering'], 'Employees innovating within the firm.'),
         ('Which is the most common problem faced by start-ups?', 'Cash-flow problems', ['Too many customers', 'Excessive economies of scale', 'Too much brand loyalty'], 'Start-ups often lack working capital.')],
  why=[('Explain why many start-ups fail in their first few years.', 'They often lack finance and cash-flow management, underestimate costs, face strong established competitors, have limited market research and lack management experience.'),
       ('Explain why a business plan is useful for a new business.', 'It forces the entrepreneur to research the market and plan finances, sets objectives against which progress can be measured, and is needed to persuade banks and investors to provide finance.'),
       ('Explain why large firms encourage intrapreneurship.', 'It harnesses employees\' creativity to develop new products and processes, keeps the firm innovative, and motivates talented staff who might otherwise leave to start their own businesses.')],
  contrast=[('an entrepreneur', 'an intrapreneur', 'An entrepreneur starts a new business and bears the financial risk personally; an intrapreneur innovates within an existing organization, using its resources, and bears less personal financial risk.')],
  misc=[('A business plan guarantees the success of a start-up.', 'A plan helps but cannot guarantee success: forecasts may be wrong, markets change and execution matters.')],
  cases=[('3M\'s Post-it Notes', 'Post-it Notes came from 3M scientists Spencer Silver and Art Fry, using the company\'s "15% time" for employees\' own projects; they were launched in 1980.', 'intrapreneurship', 'an employee used company time and resources to develop a new product that became a major success'),
         ('Canva', 'Canva was founded in Australia in 2013 by Melanie Perkins after more than 100 rejections from investors; by 2024 it had over 180 million monthly users.', 'entrepreneurship and problems faced by start-ups', 'raising finance was a major obstacle, but persistence and a simple product solved a real customer need'),
         ('Quibi', 'Quibi raised about $1.75 bn for a short-form streaming service but shut down in December 2020, six months after launch.', 'problems faced by start-ups', 'despite large finance, poor market research and a product that did not fit customer behaviour led to failure')],
  evaluate=[('Lack of finance is the main reason why start-ups fail.', ['cash-flow problems are very common', 'difficulty raising external finance', 'cannot survive early losses'],
             ['poor market research and product-market fit (Quibi)', 'weak management skills', 'strong competition', 'external shocks'], 'Finance problems are often the immediate cause of failure, but they usually reflect deeper problems such as weak research, planning or management.')],
  )


# =============================================================================================
# ch02 Unit 1.2 Types of business entities
# =============================================================================================
S('ch02-st1', concepts=('ethics', 'change'),
  terms=[('private sector', 'the part of the economy made up of businesses owned and controlled by private individuals and organizations, usually aiming to make a profit'),
         ('public sector', 'the part of the economy owned and controlled by the government, providing goods and services such as health care, education and defence'),
         ('privatisation', 'the transfer of ownership of organizations or assets from the public sector to the private sector'),
         ('nationalisation', 'the transfer of ownership of organizations or assets from the private sector to the public sector'),
         ('public-private partnership (PPP)', 'a long-term arrangement in which the government and private businesses cooperate to fund, build or run public services or infrastructure')],
  facts=[('Which of the following is a public sector organization?', 'A state-owned national health service', ['A publicly held company listed on a stock exchange', 'A sole trader', 'A partnership of lawyers'], 'A "public limited company" is in the private sector.'),
         ('The sale of British Telecom shares to the public in 1984 is an example of:', 'privatisation', ['nationalisation', 'a merger', 'a joint venture'], 'Ownership moved from government to private shareholders.'),
         ('Why do governments provide some services through the public sector?', 'Some goods and services, such as defence, would be under-provided by the private sector', ['Public sector firms always make more profit', 'To avoid all taxation', 'Because private firms cannot employ workers'], 'Public and merit goods.')],
  why=[('Explain why public sector organizations may have different objectives from private sector businesses.', 'Public sector organizations aim to provide essential services to all citizens, efficiently and fairly, rather than to maximise profit for owners; they are accountable to government and taxpayers.'),
       ('Explain why governments privatise state-owned businesses.', 'To raise revenue, improve efficiency through profit incentives and competition, reduce the burden on the budget, and widen share ownership.'),
       ('Explain why some governments nationalise businesses.', 'To protect strategic industries or jobs, rescue failing firms in a crisis (e.g. banks in 2008), control natural monopolies, or ensure universal service.')],
  contrast=[('the private sector', 'the public sector', 'The private sector is owned by individuals and organizations and usually aims for profit; the public sector is owned by the government and aims to provide services for society.'),
            ('privatisation', 'nationalisation', 'Privatisation transfers ownership from the state to private owners; nationalisation transfers ownership from private owners to the state.')],
  misc=[('A public limited company is part of the public sector.', 'A public limited company is a private sector business whose shares can be sold to the public on a stock exchange; the public sector is government-owned.')],
  cases=[('the UK government\'s 2008 rescue of Royal Bank of Scotland', 'In 2008 the UK government took an 84% stake in RBS (now NatWest Group) to prevent its collapse during the financial crisis; the stake was fully sold by 2025.', 'nationalisation', 'the government took ownership to protect the financial system, later returning the bank to the private sector'),
         ('Saudi Aramco\'s 2019 share sale', 'In December 2019 Saudi Aramco sold 1.5% of its shares in the world\'s largest IPO at the time, raising about $25.6 bn.', 'partial privatisation', 'the state kept control while raising finance from private investors'),
         ('the UK railways', 'UK rail was privatised in the 1990s; since 2018 several franchises have returned to public control and the government is creating Great British Railways.', 'the boundary between the private and public sectors', 'concerns about performance and cost led to services moving back into the public sector')],
  evaluate=[('Essential services such as water and railways should be run by the public sector.', ['universal access and fairness', 'natural monopolies need control', 'long-term investment not driven by profit'],
             ['private firms may be more efficient', 'competition encourages innovation', 'government budgets are constrained', 'public firms may lack incentives'], 'Natural monopolies with essential services often need public ownership or strong regulation; the best choice depends on how well regulation works.')],
  )

S('ch02-st2', concepts=('change', 'ethics'),
  terms=[('sole trader', 'a business owned by one person, who has unlimited liability and keeps all the profits'),
         ('partnership', 'a business owned by between two and twenty people (in most jurisdictions) who share the risks, decisions and profits, usually with unlimited liability'),
         ('unlimited liability', 'the legal obligation of owners to pay all the debts of the business, even from their personal assets'),
         ('limited liability', 'the restriction of owners\' liability for business debts to the amount they have invested'),
         ('privately held company', 'a company owned by shareholders whose shares cannot be sold to the general public on a stock exchange'),
         ('publicly held company', 'a company whose shares are traded on a stock exchange and can be bought by members of the public'),
         ('initial public offering (IPO)', 'the first sale of a company\'s shares to the public on a stock exchange')],
  facts=[('Which type of business has unlimited liability?', 'A sole trader', ['A privately held company', 'A publicly held company', 'A cooperative with limited liability'], 'Owners of sole traderships are personally liable.'),
         ('Which of the following is an advantage of becoming a publicly held company?', 'Access to large amounts of finance by selling shares on a stock exchange', ['Complete privacy of accounts', 'No risk of takeover', 'Lower legal requirements'], 'An IPO can raise significant capital.'),
         ('Arm Holdings returned to public share ownership in 2023 by listing on:', 'Nasdaq in New York', ['the London Stock Exchange only', 'the Tokyo Stock Exchange', 'no stock exchange'], 'Arm\'s IPO valued it at about $54 bn.'),
         ('Which is a disadvantage of a partnership?', 'Disagreements between partners can harm decision-making', ['Partners cannot share expertise', 'It is harder to set up than a PLC', 'It must publish its accounts'], 'Shared control can lead to conflict.')],
  why=[('Explain why a sole trader may find it difficult to grow.', 'Finance is limited to the owner\'s savings and loans, banks see sole traders as risky, the owner has limited time and skills, and unlimited liability discourages risk-taking.'),
       ('Explain why limited liability encourages investment.', 'Investors can lose only what they invest, not their personal assets, so they are more willing to buy shares, making it easier for companies to raise finance.'),
       ('Explain why a privately held company might decide to become a publicly held company.', 'To raise large amounts of capital for expansion, allow founders and early investors to sell shares, increase public profile, and use shares to buy other firms.'),
       ('Explain why some publicly held companies return to private ownership.', 'To avoid pressure for short-term results, escape disclosure requirements and the risk of hostile takeover, and allow owners to make long-term decisions privately (e.g. Dell in 2013).')],
  contrast=[('a privately held company', 'a publicly held company', 'Shares in a privately held company are owned by a restricted group and are not traded publicly; shares in a publicly held company trade on a stock exchange, so it can raise more finance but must disclose more and risks takeover.'),
            ('unlimited liability', 'limited liability', 'With unlimited liability owners are personally responsible for all business debts; with limited liability their losses are limited to the amount invested.')],
  misc=[('Shareholders of a company with limited liability can never lose any money.', 'They can lose the full amount they invested if the company fails; limited liability only protects their personal assets beyond that.')],
  cases=[('Dell\'s return to private ownership', 'In 2013 Michael Dell and Silver Lake took Dell private in a $24.9 bn buyout, then relisted in 2018.', 'privately and publicly held companies', 'going private freed management from short-term market pressure while restructuring'),
         ('Arm\'s IPO in 2023', 'Chip designer Arm, owned by SoftBank since 2016, listed on Nasdaq in September 2023, raising about $4.9 bn.', 'reasons for becoming a publicly held company', 'the listing allowed the owner to raise finance and value the business, while keeping majority control'),
         ('the collapse of a sole trader during Covid-19', 'Many small independent cafés and hairdressers that were sole traders closed in 2020-2021 as lockdowns cut revenue and owners\' personal savings ran out.', 'unlimited liability and the risks of sole trading', 'owners bore the losses personally and had limited access to finance')],
  evaluate=[('Becoming a publicly held company is always the best option for a growing business.', ['access to large-scale finance', 'limited liability', 'prestige and liquidity of shares'],
             ['loss of control and risk of takeover', 'short-termism', 'high costs of listing and disclosure', 'owners may prefer privacy (e.g. IKEA, Mars)'], 'It suits firms needing large amounts of capital, but many successful businesses stay private to keep control and long-term focus.')],
  )

S('ch02-st3', concepts=('ethics', 'sustainability'),
  terms=[('social enterprise', 'an organization that uses commercial activities to achieve social, environmental or community objectives, reinvesting most surpluses into its mission'),
         ('for-profit social enterprise', 'a business that seeks to earn revenue and profit but uses most of the surplus to achieve social or environmental objectives'),
         ('non-governmental organization (NGO)', 'a non-profit organization that operates independently of government to address social, humanitarian or environmental issues'),
         ('cooperative', 'a business owned and democratically controlled by its members (workers, customers or producers), who share its benefits'),
         ('non-profit social enterprise', 'an organization that pursues a social mission and does not distribute profits to owners; any surplus is reinvested in the mission')],
  facts=[('Mondragon in Spain is an example of a:', 'worker cooperative', ['sole trader', 'publicly held company', 'government department'], 'Worker-members own and control the businesses.'),
         ('Médecins Sans Frontières (MSF) is best described as:', 'an NGO', ['a for-profit social enterprise', 'a public sector organization', 'a franchise'], 'An independent humanitarian non-profit.'),
         ('Which feature is common to all social enterprises?', 'A primary social or environmental objective', ['No revenue from sales', 'Government ownership', 'Unlimited liability'], 'Mission comes first.'),
         ('Who Gives A Crap donates what share of its profits to sanitation charities?', '50%', ['5%', '100%', '10%'], 'Half of profits fund toilets and sanitation.')],
  why=[('Explain why social enterprises need to generate revenue.', 'Revenue from trading makes them financially sustainable and less dependent on grants and donations, allowing them to plan long-term and scale their social impact.'),
       ('Explain why cooperatives may have more motivated workers.', 'Workers are owners who share profits and vote on decisions, so they have a stake in the success of the business and a voice in how it is run.'),
       ('Explain why NGOs may face difficulties in achieving their objectives.', 'They depend on donations and grants that can be volatile, may face political obstacles in host countries, and must balance accountability to donors with the needs of beneficiaries.')],
  contrast=[('a for-profit social enterprise', 'a non-profit social enterprise', 'A for-profit social enterprise can distribute some profit to owners while pursuing a mission; a non-profit reinvests all surpluses in its mission and has no shareholders receiving dividends.'),
            ('a cooperative', 'a publicly held company', 'A cooperative is owned by its members with one member, one vote; a publicly held company is owned by shareholders with votes in proportion to shares held.')],
  misc=[('Social enterprises do not need to be well managed because they have good intentions.', 'They face the same need for finance, efficiency, marketing and HR as other businesses; poor management can end their social impact.')],
  cases=[('Grameen Bank', 'Grameen Bank lends to over 9 million poor members in Bangladesh, mostly women, without requiring collateral, and reports high repayment rates.', 'a social enterprise', 'commercial lending is used to pursue the social objective of reducing poverty'),
         ('the John Lewis Partnership', 'The John Lewis Partnership (UK) is owned in trust for its employees, called Partners, who share in profits through an annual bonus.', 'employee-owned businesses', 'employee ownership aligns staff with long-term success, although bonuses fall when profits do'),
         ('Amul', 'Amul in India is a cooperative owned by about 3.6 million dairy farmers and is one of India\'s best-known food brands.', 'cooperatives', 'producer-members share the benefits of scale and branding rather than selling to intermediaries')],
  evaluate=[('Social enterprises are more effective than charities at solving social problems.', ['self-financing through trade', 'scalable and sustainable', 'business discipline and efficiency'],
             ['some needs cannot be met by market activity (disaster relief)', 'risk of mission drift towards profit', 'smaller scale than large NGOs', 'charities can access donations and volunteers'], 'Social enterprises are well suited where people can pay something for a service; charities and NGOs remain essential where beneficiaries cannot pay.')],
  )


# =============================================================================================
# ch03 Unit 1.3 Business objectives
# =============================================================================================
S('ch03-st1', concepts=('change', 'ethics', 'sustainability'),
  terms=[('vision statement', 'a statement of what an organization aspires to be or achieve in the long term'),
         ('mission statement', 'a statement of the purpose of an organization, its core values and what it does for its stakeholders'),
         ('aims', 'the long-term, general goals of an organization'),
         ('objectives', 'specific, measurable, time-bound targets that an organization sets in order to achieve its aims'),
         ('strategy', 'a long-term plan of action designed to achieve the objectives of an organization'),
         ('tactics', 'short-term methods used to carry out a strategy'),
         ('SMART objectives', 'objectives that are specific, measurable, achievable, realistic (relevant) and time-bound')],
  facts=[('Which of the following is a SMART objective?', 'Increase market share in Germany from 8% to 10% by December 2027', ['Become the best company in the world', 'Make customers happier', 'Grow as fast as possible'], 'It is specific, measurable and time-bound.'),
         ('Which statement best describes a vision statement?', 'An aspirational description of what the organization wants to become in the future', ['A list of this month\'s sales targets', 'The firm\'s statement of profit or loss', 'A short-term tactic'], 'Vision looks to the long term.'),
         ('A price-cutting promotion for two weeks to clear stock is an example of:', 'a tactic', ['a vision', 'a mission', 'an aim'], 'Tactics are short-term actions.')],
  why=[('Explain why businesses set SMART objectives.', 'SMART objectives give clear targets that can be measured and monitored, help coordinate departments, motivate staff and allow managers to judge whether strategies are working.'),
       ('Explain why a mission statement may be useful to a business.', 'It communicates the organization\'s purpose and values to employees and other stakeholders, guiding decisions and building a shared culture and identity.'),
       ('Explain why mission statements are sometimes criticised.', 'They can be vague public-relations exercises that do not influence behaviour, and can damage trust when actions contradict stated values.')],
  contrast=[('a vision statement', 'a mission statement', 'A vision statement describes the long-term future the organization aspires to; a mission statement describes its present purpose, what it does and for whom.'),
            ('strategies', 'tactics', 'Strategies are long-term, high-level plans to achieve objectives (e.g. enter the Indian market); tactics are short-term actions to implement them (e.g. a launch promotion).')],
  misc=[('Aims and objectives mean the same thing.', 'Aims are broad long-term goals; objectives are specific, measurable targets set to achieve those aims.')],
  cases=[('Tesla\'s mission', 'Tesla\'s stated mission is "to accelerate the world\'s transition to sustainable energy", guiding its products from electric cars to batteries and solar panels.', 'the role of mission statements', 'the mission sets a clear purpose that shapes long-term strategy and attracts employees and investors'),
         ('Google\'s early mission', 'Google\'s mission is "to organize the world\'s information and make it universally accessible and useful", and its original code of conduct included "Don\'t be evil".', 'mission and values', 'a clear mission guided product strategy, while critics argue later practices on privacy contradicted stated values'),
         ('Unilever\'s objectives', 'Unilever set targets such as halving the greenhouse gas footprint of its products and achieving net zero emissions across its value chain by 2039.', 'SMART objectives', 'measurable, time-bound environmental targets turn a general aim of sustainability into objectives that can be monitored')],
  evaluate=[('Mission statements are of little practical value to a business.', ['often vague and generic', 'may be ignored in decision-making', 'can damage trust if contradicted'],
             ['communicate purpose and values', 'guide strategic decisions and culture', 'help recruit staff who share values'], 'Their value depends on whether the mission is specific and genuinely used in decisions; a mission that shapes strategy, like Tesla\'s, is valuable.')],
  )

S('ch03-st2', concepts=('ethics', 'sustainability', 'change'),
  terms=[('growth objective', 'a target to increase the size of the business, for example in sales revenue, market share, number of outlets or employees'),
         ('profit objective', 'a target relating to the level of profit, such as profit maximisation, a target profit margin or profit satisficing'),
         ('shareholder value', 'the value delivered to shareholders through dividends and increases in the share price'),
         ('ethical objectives', 'targets based on moral principles, such as fair treatment of workers and suppliers, honesty and environmental responsibility'),
         ('profit satisficing', 'aiming for a satisfactory level of profit rather than the maximum, to balance profit with other goals such as owner lifestyle')],
  facts=[('A new start-up is most likely to have which objective in its first year?', 'Survival', ['Profit maximisation', 'Protecting shareholder value', 'Global market leadership'], 'Most start-ups aim first to survive.'),
         ('Paying farmers a Fairtrade price for coffee is an example of:', 'an ethical objective', ['a profit-maximising objective', 'a tactic to reduce costs', 'a survival objective'], 'Ethical objectives reflect moral principles.'),
         ('Share buybacks are commonly used by publicly held companies to:', 'increase shareholder value', ['reduce market share', 'increase debt for staff', 'reduce dividends'], 'Fewer shares can raise earnings per share and the share price.')],
  why=[('Explain why business objectives may change over time.', 'As businesses grow and markets change, priorities move from survival to growth and profit; crises, new owners, competition, technology and stakeholder expectations (e.g. sustainability) also change objectives.'),
       ('Explain why a business might pursue growth rather than short-term profit.', 'Growth can bring economies of scale, market power, brand recognition and long-run profitability; many tech firms accept early losses to build market share.'),
       ('Explain why ethical objectives can improve profitability.', 'They can strengthen brand image and customer loyalty, attract and retain motivated staff and investors, and reduce risks of fines and boycotts.')],
  contrast=[('profit maximisation', 'profit satisficing', 'Profit maximisation aims for the highest possible profit; satisficing aims for a satisfactory profit that allows owners to meet other goals such as lifestyle or social aims.')],
  misc=[('Ethical objectives always reduce profit.', 'Ethical behaviour often raises costs in the short run, but it can increase revenue and reduce risks, improving long-run profit.')],
  cases=[('Amazon\'s early growth objective', 'Amazon reported annual net losses in most years until 2003 and made thin profits for years afterwards, reinvesting heavily in growth and infrastructure.', 'growth as an objective', 'the focus on market share and scale over short-term profit built a dominant market position'),
         ('Apple\'s share buybacks', 'Apple has spent more than $600 bn on share buybacks since 2013, together with dividends.', 'protecting shareholder value', 'returning cash reduces the number of shares and supports the share price'),
         ('Ben & Jerry\'s social mission', 'Ben & Jerry\'s, owned by Unilever since 2000, has a social mission that includes sourcing Fairtrade ingredients and campaigning on social issues.', 'ethical objectives', 'a mission beyond profit shapes sourcing and brand identity, although it has caused conflict with its parent company')],
  evaluate=[('Growth is the most important objective for a business.', ['economies of scale', 'market power and security', 'higher long-run profits'],
             ['growth can cause diseconomies and loss of control', 'profit and cash flow matter for survival', 'ethical and sustainability objectives', 'shareholders may prefer dividends'], 'Growth is important for many firms but should be sustainable and profitable; the right objective depends on the firm\'s stage and stakeholders.')],
  )

S('ch03-st3', concepts=('ethics', 'sustainability', 'change'),
  terms=[('corporate social responsibility (CSR)', 'the voluntary actions of a business to act ethically and contribute to economic, social and environmental well-being beyond legal requirements'),
         ('greenwashing', 'making misleading claims that a business or product is more environmentally friendly than it really is'),
         ('B Corporation (B Corp)', 'a private certification for businesses that meet high standards of verified social and environmental performance, transparency and accountability'),
         ('triple bottom line', 'an approach that measures performance in terms of people, planet and profit')],
  facts=[('Which of the following is an example of CSR?', 'A firm funding education programmes in the communities where it operates', ['Paying the legal minimum wage only', 'Raising prices to increase profit', 'Cutting quality to reduce costs'], 'CSR goes beyond legal requirements.'),
         ('Volkswagen\'s "dieselgate" scandal (2015) involved:', 'software that cheated emissions tests', ['child labour in factories', 'tax evasion by directors', 'false advertising of car prices'], 'About 11 million vehicles were affected worldwide.'),
         ('Patagonia, Ben & Jerry\'s and Danone North America are examples of:', 'certified B Corporations', ['state-owned enterprises', 'NGOs', 'cooperatives'], 'They meet B Lab standards.')],
  why=[('Explain why businesses increasingly adopt CSR policies.', 'Customers, employees and investors increasingly expect ethical and sustainable behaviour; CSR can strengthen reputation and loyalty, attract talent and investment (ESG funds), and reduce regulatory and reputational risks.'),
       ('Explain why CSR may be criticised as a public-relations exercise.', 'Some firms publicise small initiatives while their core activities cause harm, or make vague claims (greenwashing), so CSR improves image without real change.'),
       ('Explain why a business\'s objectives may change in response to pressure from stakeholders.', 'Pressure groups, consumers, investors and governments can boycott, campaign, vote at AGMs or regulate, raising the cost of ignoring their concerns and pushing firms towards ethical and sustainability objectives.')],
  contrast=[('CSR', 'legal compliance', 'Legal compliance means meeting the minimum standards required by law; CSR means voluntary action beyond legal requirements to benefit society and the environment.')],
  misc=[('A business that obeys all laws is socially responsible.', 'CSR involves voluntary actions beyond the law; legal behaviour can still be unethical (e.g. aggressive tax avoidance).')],
  cases=[('Volkswagen\'s emissions scandal', 'In 2015 Volkswagen admitted fitting about 11 million diesel cars with software that cheated emissions tests; the scandal cost the company over €30 bn in fines and settlements.', 'the consequences of unethical behaviour', 'unethical decisions led to huge financial costs and lasting damage to trust and reputation'),
         ('Patagonia\'s change of ownership', 'In 2022 founder Yvon Chouinard transferred Patagonia to a trust and a non-profit; profits not reinvested (about $100 m a year) go to fighting climate change.', 'CSR and changing objectives', 'the firm placed environmental objectives at the centre of ownership and profit distribution'),
         ('H&M\'s "Conscious" collection', 'In 2022 H&M faced legal action in the USA over claims that its "Conscious" collection environmental scorecards were misleading.', 'greenwashing', 'exaggerated sustainability claims exposed the firm to legal and reputational risk')],
  evaluate=[('Corporate social responsibility benefits all of a business\'s stakeholders.', ['better reputation and loyalty for owners', 'improved working conditions for employees', 'community and environmental gains'],
             ['higher costs and lower short-term returns', 'trade-offs between stakeholders', 'risk of greenwashing', 'competitors without CSR may undercut prices'], 'Well-designed CSR can create mutual benefits, but there are trade-offs and costs; genuine CSR is most beneficial when integrated into core strategy.')],
  )

S('ch03-st4', concepts=('change', 'sustainability'),
  terms=[('SWOT analysis', 'a business management tool that assesses an organization\'s internal strengths and weaknesses and external opportunities and threats'),
         ('STEEPLE analysis', 'a tool for analysing the external environment of a business: social, technological, economic, environmental, political, legal and ethical factors'),
         ('internal factors', 'factors within the control of the business, such as its brand, workforce, finance and technology'),
         ('external factors', 'factors outside the control of the business, such as the economy, competitors, government policy and social trends')],
  facts=[('In a SWOT analysis, rising interest rates would be classified as:', 'a threat', ['a strength', 'a weakness', 'an opportunity'], 'An external factor that may harm the business.'),
         ('Which of the following is an internal factor in a SWOT analysis?', 'A strong brand reputation', ['A new competitor entering the market', 'A change in government policy', 'A recession'], 'Strengths and weaknesses are internal.'),
         ('Which letter of STEEPLE would cover a new data-protection law?', 'Legal', ['Social', 'Economic', 'Environmental'], 'Laws are legal factors.')],
  why=[('Explain why a SWOT analysis can help a business set its objectives.', 'It identifies internal strengths to build on and weaknesses to fix, and external opportunities and threats, so objectives can be realistic and focused on the most important issues.'),
       ('Explain why STEEPLE analysis is useful before entering a new market.', 'It systematically examines external factors – social trends, technology, economy, environment, politics, laws and ethics – that affect demand, costs and risks in the new market.'),
       ('Explain why SWOT analysis has limitations.', 'It is a snapshot that can become outdated, is subjective, does not rank factors by importance and does not itself provide a strategy.')],
  contrast=[('SWOT analysis', 'STEEPLE analysis', 'SWOT covers both internal (strengths, weaknesses) and external (opportunities, threats) factors; STEEPLE analyses only the external environment in more detail, often feeding into the O and T of a SWOT.')],
  misc=[('Opportunities in a SWOT analysis are things the business already does well.', 'Things the business does well are strengths (internal); opportunities are favourable external factors such as a growing market.')],
  cases=[('Netflix\'s environment in the early 2020s', 'Netflix faced growing competition from Disney+, Amazon Prime Video and others, a shift to ad-supported plans and a crackdown on password sharing in 2023 that added millions of subscribers.', 'SWOT analysis', 'strengths (content, brand) and threats (competitors) shaped new objectives on revenue per user'),
         ('Nestlé in India in 2015', 'In 2015 Indian regulators banned Maggi noodles for about five months over alleged lead levels; sales collapsed before recovering after the ban was lifted.', 'STEEPLE analysis', 'legal and social factors in an external environment can suddenly threaten a market leader'),
         ('electric vehicle makers and STEEPLE', 'Government subsidies, emissions rules, falling battery costs and consumer attitudes all affect demand for electric vehicles, for example the EU\'s plan to end sales of new petrol cars by 2035.', 'external factors affecting objectives', 'political, legal, technological and environmental factors change the opportunities and threats facing car makers')],
  evaluate=[('A SWOT analysis is the most useful tool for setting business objectives.', ['simple and quick', 'combines internal and external factors', 'identifies priorities'],
             ['subjective and static', 'no weighting of factors', 'STEEPLE, Ansoff and stakeholder mapping give more detailed insights', 'does not generate strategies itself'], 'SWOT is a useful starting point, but objectives are best set using several tools and up-to-date data.')],
  )


# =============================================================================================
# ch04 Unit 1.4 Stakeholders
# =============================================================================================
S('ch04-st1', concepts=('ethics', 'sustainability'),
  terms=[('stakeholder', 'an individual or group with an interest in, or affected by, the activities of an organization'),
         ('internal stakeholders', 'stakeholders who are part of the organization, such as employees, managers, directors and shareholders'),
         ('external stakeholders', 'stakeholders who are not part of the organization, such as customers, suppliers, the local community, government, pressure groups and competitors'),
         ('pressure group', 'an organized group of people that tries to influence the decisions of businesses or governments, such as Greenpeace'),
         ('shareholder', 'an owner of shares in a limited company, entitled to a share of profits as dividends and to vote at general meetings')],
  facts=[('Which of the following is an external stakeholder?', 'A supplier', ['An employee', 'A manager', 'A director'], 'Suppliers are outside the organization.'),
         ('Which stakeholder is mainly interested in dividends and share price growth?', 'Shareholders', ['Local residents', 'Customers', 'Pressure groups'], 'Owners seek returns.'),
         ('The government is interested in businesses mainly because of:', 'tax revenue, employment and compliance with laws', ['dividends only', 'product colour', 'internal promotions'], 'Governments regulate and tax businesses.')],
  why=[('Explain why employees are interested in the success of a business.', 'Their income, job security, working conditions, training and career opportunities depend on the business performing well.'),
       ('Explain why the local community is a stakeholder in a large factory.', 'The factory creates jobs and spending locally but may cause noise, traffic and pollution, so residents are affected by its decisions.'),
       ('Explain why customers have an interest in how a business behaves.', 'They want good quality, fair prices, safe products and reliable service, and many care about the ethical and environmental impact of what they buy.')],
  contrast=[('internal stakeholders', 'external stakeholders', 'Internal stakeholders are members of the organization (employees, managers, shareholders); external stakeholders are outside it but affected by it (customers, suppliers, community, government).'),
            ('shareholders', 'stakeholders', 'Shareholders are owners of a company; stakeholders are anyone with an interest in or affected by the business, of whom shareholders are one group.')],
  misc=[('Competitors cannot be stakeholders.', 'Competitors are affected by a firm\'s decisions (pricing, innovation) and can be considered external stakeholders.')],
  cases=[('Greenpeace and Nestlé', 'In 2010 Greenpeace campaigned against Nestlé\'s use of palm oil linked to rainforest destruction, with a viral KitKat video; Nestlé committed to removing deforestation from its supply chain.', 'the influence of pressure groups as external stakeholders', 'a campaign that damaged brand image forced a change in sourcing policy'),
         ('Rana Plaza (2013)', 'The collapse of the Rana Plaza garment factory in Bangladesh in 2013 killed over 1,100 workers producing clothes for Western brands.', 'stakeholders in global supply chains', 'workers, brands, consumers and governments were all stakeholders; the disaster led to the Bangladesh Accord on fire and building safety'),
         ('Tesla\'s Gigafactory Berlin', 'Tesla\'s factory near Berlin, opened in 2022, faced protests from local residents and environmental groups over water use and forest clearing.', 'the interests of the local community', 'jobs and investment conflicted with environmental concerns of residents')],
  evaluate=[('Shareholders are the most important stakeholders of a publicly held company.', ['owners with legal rights and votes', 'provide finance and bear risk', 'directors have duties to shareholders'],
             ['without customers there are no profits', 'employees create value', 'ignoring other stakeholders damages reputation', 'stakeholder capitalism views'], 'Shareholders have formal power, but long-term shareholder value depends on meeting the needs of customers, employees and society.')],
  )

S('ch04-st2', concepts=('ethics', 'change'),
  terms=[('stakeholder conflict', 'a disagreement between stakeholder groups because their interests or objectives differ'),
         ('stakeholder mapping', 'a business management tool (HL) that classifies stakeholders by their level of interest and power to decide how to manage them'),
         ('Mendelow\'s matrix', 'a stakeholder map with four quadrants: minimal effort (low power, low interest), keep informed (low power, high interest), keep satisfied (high power, low interest) and key players (high power, high interest)'),
         ('key players', 'stakeholders with high power and high interest, who must be fully engaged and considered in decisions')],
  facts=[('In Mendelow\'s matrix, stakeholders with high power but low interest should be:', 'kept satisfied', ['ignored', 'kept informed', 'treated as key players'], 'They could become key players if their interest rises.'),
         ('Which is a typical conflict between stakeholders?', 'Shareholders want higher dividends while employees want higher wages', ['Customers and suppliers both want the firm to survive', 'Managers and directors both want growth', 'Employees and managers both want training'], 'Both compete for the same profits.'),
         ('A large institutional shareholder with a strong interest in a takeover bid would be classified as:', 'a key player', ['minimal effort', 'keep informed', 'keep satisfied'], 'High power and high interest.')],
  why=[('Explain why conflicts can arise between stakeholders.', 'Stakeholders have different objectives (profit, wages, low prices, environmental protection) and resources are limited, so a gain for one group may be a cost to another.'),
       ('Explain why stakeholder mapping can help managers.', 'It identifies which stakeholders have most power and interest, so managers can prioritise communication and consultation, anticipate opposition and reduce conflict.'),
       ('Explain why a stakeholder\'s position on a stakeholder map can change.', 'Interest and power change with circumstances: a local community may become highly interested in a factory expansion, and pressure groups may gain power through media campaigns.')],
  contrast=[('keep informed stakeholders', 'keep satisfied stakeholders', 'Keep-informed stakeholders have high interest but low power and need regular communication; keep-satisfied stakeholders have high power but low interest and must be kept content so they do not oppose decisions.')],
  misc=[('Stakeholder conflict can always be avoided.', 'Some conflict is inevitable because resources are limited; managers can only reduce and manage it through communication, compromise and prioritisation.')],
  cases=[('the UAW strike against Detroit\'s car makers in 2023', 'In 2023 the United Auto Workers union struck against Ford, GM and Stellantis for six weeks, winning wage rises of about 25% over the contract.', 'stakeholder conflict', 'employees\' demand for higher pay conflicted with shareholders\' and managers\' goals for costs and profits'),
         ('Heathrow\'s third runway', 'Plans for a third runway at Heathrow Airport have been debated for over 20 years, with airlines and business groups in favour and local residents and environmental groups opposed.', 'stakeholder mapping', 'stakeholders with different levels of power and interest must be managed differently in a major decision')],
  evaluate=[('Stakeholder mapping allows managers to resolve stakeholder conflict effectively.', ['clarifies priorities', 'guides communication strategies', 'anticipates opposition'],
             ['subjective classification', 'positions change quickly', 'does not tell managers how to resolve conflicts', 'ethical issues if low-power groups are ignored'], 'Stakeholder mapping is a useful planning tool, but resolving conflict also requires negotiation, compromise and ethical judgement.')],
  )

S('ch04-st3', concepts=('ethics', 'sustainability'),
  terms=[('mutual benefit', 'a situation where a business decision benefits several stakeholder groups at the same time'),
         ('stakeholder influence', 'the ability of a stakeholder group to affect business decisions, depending on its power, interest and resources'),
         ('consultation', 'the process of seeking the views of stakeholders before making a decision'),
         ('stakeholder capitalism', 'the view that businesses should serve the interests of all stakeholders, not only shareholders')],
  facts=[('Which of the following is an example of mutual benefit for stakeholders?', 'Training that raises employee productivity and pay while improving customer service', ['A wage cut to raise dividends', 'Relocating a factory abroad to cut costs', 'Raising prices during a shortage'], 'Several groups gain together.'),
         ('Customers mainly influence business decisions through:', 'their purchasing decisions and reviews', ['voting at the AGM', 'setting interest rates', 'passing laws'], 'Customers can switch to rivals.'),
         ('In 2019 the US Business Roundtable statement redefined the purpose of a corporation to:', 'serve all stakeholders, not only shareholders', ['maximise shareholder value only', 'avoid paying taxes', 'end all dividends'], 'A move towards stakeholder capitalism.')],
  why=[('Explain why satisfying employees can benefit customers and shareholders.', 'Motivated, well-trained employees are more productive and give better service, raising customer satisfaction and loyalty, which increases sales and profits.'),
       ('Explain why suppliers can influence a business\'s decisions.', 'Suppliers control the price, quality and timing of inputs; a powerful or sole supplier can affect costs and production schedules.'),
       ('Explain why governments have significant influence over business decisions.', 'They make laws and regulations, set taxes and subsidies and award contracts, so firms must comply and often lobby to shape policy.')],
  contrast=[('stakeholder conflict', 'mutual benefit', 'Stakeholder conflict arises when a decision benefits one group at another\'s expense; mutual benefit arises when a decision improves outcomes for several groups at once.')],
  misc=[('Satisfying one stakeholder group always means harming another.', 'Many decisions create mutual benefits, for example improving quality raises customer satisfaction, sales, job security and profits.')],
  cases=[('Costco\'s employee policies', 'Costco pays wages well above the US retail average and has low staff turnover, while remaining highly profitable.', 'mutual benefits for stakeholders', 'higher pay reduces recruitment costs and improves service, benefiting employees, customers and shareholders'),
         ('shareholder votes on climate', 'In 2021 activist fund Engine No. 1, holding only about 0.02% of ExxonMobil, won three board seats with the support of large investors concerned about climate strategy.', 'stakeholder influence', 'a small shareholder gained influence by building a coalition of investors')],
  evaluate=[('Businesses can satisfy all their stakeholders at the same time.', ['mutual benefits from quality, training and ethics', 'long-term alignment of interests', 'examples like Costco'],
             ['limited resources force trade-offs', 'short-term conflicts over wages, prices and dividends', 'environmental costs vs. growth'], 'Businesses can create mutual benefits in the long run, but in the short run trade-offs are inevitable and require prioritisation.')],
  )


# =============================================================================================
# ch05 Units 1.5-1.6 Growth and evolution; multinational companies
# =============================================================================================
@calc('ch05-st1', 'C3', (1, 5))
def econ_scale(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    fc = rng.choice([20_000, 40_000, 60_000, 90_000, 120_000])
    vc = rng.choice([4, 5, 8, 10, 12, 15])
    q1 = rng.choice([2_000, 4_000, 5_000])
    q2 = q1 * rng.choice([2, 3, 4])
    disc = rng.choice([5, 10, 15, 20])
    vc2 = vc * (1 - disc / 100)
    ac1 = (fc + vc * q1) / q1
    ac2 = (fc + vc2 * q2) / q2
    frame = rng.choice([f'{f_} has fixed costs of {m(fc, c)} a month and variable costs of {m(vc, c)} per unit.',
                        f'Monthly overheads at {f_} are {m(fc, c)}; each unit costs {m(vc, c)} in materials and direct labour.'])
    if slot.d <= 2:
        return dict(stem=frame + f' Calculate the average cost per unit at outputs of {q1:,} and {q2:,} units.',
                    answer=f'AC at {q1:,} = {m(ac1, c)}; AC at {q2:,} = {m((fc + vc * q2) / q2, c)}',
                    markingKey=MK(f'AC = (FC + VC × Q)/Q: ({fc:,} + {vc} × {q1:,})/{q1:,} = {ac1:.2f}; ({fc:,} + {vc} × {q2:,})/{q2:,} = {(fc + vc * q2) / q2:.2f}.', 'both average costs'), marks=2)
    return dict(stem=frame + f' If it expands output from {q1:,} to {q2:,} units, bulk buying will reduce variable cost per unit by {disc}%. Calculate the average cost per unit before and after expansion, and identify two types of economy of scale involved.',
                answer=f'Before: {m(ac1, c)}; after: ({fc:,} + {p2(vc2)} × {q2:,})/{q2:,} = {m(ac2, c)}. Economies: spreading fixed costs over more units (technical/indivisibilities) and purchasing (bulk-buying) economies.',
                markingKey=MK(f'AC1 = {ac1:.2f}; new VC = {p2(vc2)}; AC2 = {ac2:.2f}.', 'both average costs') + ' [R1][R1] two types of economies of scale correctly identified.', marks=4 if slot.d <= 4 else 6)


S('ch05-st1', concepts=('change', 'sustainability'),
  terms=[('economies of scale', 'the reductions in average (unit) costs that a business experiences as it increases its scale of operations'),
         ('diseconomies of scale', 'the increases in average costs that occur when a business becomes too large'),
         ('internal economies of scale', 'cost savings arising from the growth of the business itself, such as purchasing, technical, financial, managerial, marketing and risk-bearing economies'),
         ('external economies of scale', 'cost savings arising from the growth of the industry or region, such as a skilled labour pool, specialist suppliers and better infrastructure'),
         ('purchasing economies', 'cost savings from buying inputs in bulk at a discount')],
  facts=[('Which of the following is an internal economy of scale?', 'A large firm obtaining cheaper loans from banks', ['A pool of skilled workers in the region', 'Improved local roads', 'Local training colleges for the industry'], 'Financial economies are internal.'),
         ('Which of the following is a diseconomy of scale?', 'Communication problems in a large organization', ['Bulk-buying discounts', 'Specialised managers', 'Cheaper advertising per unit sold'], 'Communication breaks down as firms grow.'),
         ('The concentration of technology firms in Silicon Valley creates:', 'external economies of scale', ['internal diseconomies', 'purchasing economies only', 'no cost advantages'], 'Shared talent pools and suppliers.')],
  why=[('Explain why large firms can benefit from technical economies of scale.', 'They can afford specialised, high-capacity machinery and automation whose cost is spread over a large output, lowering average costs.'),
       ('Explain why diseconomies of scale may occur as a business grows.', 'Longer chains of command slow communication and decision-making, coordination becomes harder, and employees may feel alienated and less motivated, so average costs rise.'),
       ('Explain why economies of scale can give a business a competitive advantage.', 'Lower average costs allow it to cut prices, earn higher margins or spend more on marketing and R&D, making it hard for smaller rivals to compete.')],
  contrast=[('internal economies of scale', 'external economies of scale', 'Internal economies come from the growth of the firm itself (bulk buying, specialised machinery); external economies come from the growth of the industry or location (skilled labour pools, supplier networks).'),
            ('economies of scale', 'diseconomies of scale', 'Economies of scale lower average costs as output grows; diseconomies raise average costs when a firm becomes too large to manage efficiently.')],
  misc=[('Bigger businesses always have lower average costs.', 'Beyond a certain size, diseconomies such as poor communication and low motivation can raise average costs.')],
  cases=[('Walmart\'s purchasing power', 'Walmart, with annual revenue over $640 bn, negotiates large discounts from suppliers because of the volumes it buys.', 'purchasing economies of scale', 'bulk buying lowers its unit costs and supports its "everyday low prices" strategy'),
         ('Shenzhen\'s electronics cluster', 'Shenzhen in China has thousands of component suppliers, contract manufacturers and engineers within a short distance of one another.', 'external economies of scale', 'firms in the cluster gain from fast access to suppliers and skilled labour, reducing costs and time to market'),
         ('Boeing\'s coordination problems', 'Boeing\'s 787 Dreamliner programme, which outsourced major parts to suppliers around the world, was over three years late and billions over budget.', 'diseconomies of scale', 'coordinating a very large, complex supply network raised costs and delays')],
  evaluate=[('Economies of scale are the main reason why businesses grow.', ['lower average costs', 'pricing power and competitiveness', 'financial and marketing advantages'],
             ['market power and reduced competition', 'diversification of risk', 'managerial ambition', 'diseconomies may outweigh savings'], 'Economies of scale are a major motive, but firms also grow for market power, security and ambition, and growth only lowers costs up to a point.')],
  )

S('ch05-st2', concepts=('change', 'creativity', 'ethics'),
  terms=[('internal (organic) growth', 'growth achieved by expanding the business\'s own operations, for example by opening new outlets or increasing production'),
         ('external (inorganic) growth', 'growth achieved by combining with or buying other businesses, through mergers, acquisitions, joint ventures, strategic alliances or franchising'),
         ('merger', 'the agreement of two companies to combine to form a single new company'),
         ('acquisition', 'the purchase of a controlling interest in another company'),
         ('takeover', 'an acquisition, often hostile, in which one company buys a controlling interest in another without the agreement of its management'),
         ('joint venture', 'an agreement in which two or more businesses create a new, jointly owned business to pursue a specific project'),
         ('strategic alliance', 'an agreement between businesses to cooperate on a project while remaining independent and without forming a new company'),
         ('franchising', 'an arrangement in which a franchisor allows a franchisee to use its brand and business model in return for fees and royalties')],
  facts=[('Disney\'s purchase of Pixar in 2006 for about $7.4 bn is an example of:', 'an acquisition', ['a joint venture', 'organic growth', 'franchising'], 'Disney bought Pixar outright.'),
         ('Tata Starbucks, formed in 2012 to open Starbucks stores in India, is a:', 'joint venture', ['merger', 'sole trader', 'hostile takeover'], 'A jointly owned new business.'),
         ('Which form of growth is usually slowest but least risky?', 'Organic growth', ['A hostile takeover', 'A merger of equals', 'A conglomerate acquisition'], 'Growth is financed and managed internally.'),
         ('Microsoft\'s acquisition of Activision Blizzard, completed in 2023, cost about:', '$69 bn', ['$6.9 bn', '$690 bn', '$1.2 bn'], 'One of the largest deals in gaming history.')],
  why=[('Explain why franchising allows a business to grow rapidly.', 'Franchisees provide the capital and local management for new outlets, so the franchisor can expand quickly without large investment, earning fees and royalties.'),
       ('Explain why many mergers and acquisitions fail to create value.', 'Buyers often overpay, cultures clash, integration of systems and people is difficult, and expected synergies do not materialise.'),
       ('Explain why a business might choose a joint venture to enter a foreign market.', 'A local partner provides market knowledge, contacts and distribution, shares costs and risks, and may be required by host-country rules on foreign ownership.'),
       ('Explain why organic growth may be preferred to external growth.', 'It allows the firm to keep control and its culture, grow at a manageable pace and avoid the high costs and integration risks of mergers and acquisitions.')],
  contrast=[('a joint venture', 'a strategic alliance', 'A joint venture creates a new, jointly owned business; a strategic alliance is cooperation between independent firms without creating a new legal entity.'),
            ('a merger', 'a takeover', 'A merger is an agreed combination of two firms into one; a takeover (acquisition) is the purchase of a controlling stake in one firm by another, sometimes against its management\'s wishes.')],
  misc=[('Franchisees own the brand of the business they operate.', 'The franchisor owns the brand and business model; the franchisee pays fees and royalties for the right to use them.')],
  cases=[('McDonald\'s franchising', 'About 95% of McDonald\'s roughly 40,000 restaurants worldwide are run by independent franchisees.', 'franchising as a method of growth', 'franchisees fund and run outlets, allowing rapid global expansion with less capital from McDonald\'s'),
         ('DaimlerChrysler', 'The 1998 "merger of equals" between Daimler-Benz and Chrysler, worth about $36 bn, ended in 2007 when Chrysler was sold for a fraction of its value.', 'the risks of mergers', 'culture clashes and failed integration destroyed value'),
         ('the Renault-Nissan-Mitsubishi Alliance', 'Renault, Nissan and Mitsubishi have shared platforms, purchasing and technology through a strategic alliance with cross-shareholdings since 1999.', 'strategic alliances', 'the firms gained economies of scale while remaining separate companies, although tensions grew after 2018')],
  evaluate=[('External growth is better than organic growth for a business that wants to expand.', ['rapid growth and market share', 'access to new technology, brands and markets', 'economies of scale and synergies'],
             ['high cost and risk of overpaying', 'culture clashes (DaimlerChrysler)', 'regulatory barriers', 'loss of control and focus'], 'External growth is faster but riskier; organic growth suits firms that value control, while M&A suits firms needing scale or capabilities quickly.'),
            ('Franchising is the best way for a business to grow internationally.', ['low capital requirement', 'local knowledge of franchisees', 'rapid expansion'],
             ['loss of control over quality', 'reputation risk from poor franchisees', 'share of profits goes to franchisees', 'not suitable for every product'], 'Franchising is excellent for standardised services with strong brands, but less suitable where quality control and know-how are critical.')],
  )

S('ch05-st3', concepts=('change', 'creativity'),
  terms=[('small business', 'a business with a small number of employees, low revenue or small market share, often owned by one or a few people'),
         ('niche market', 'a small, specialised segment of a market with particular needs'),
         ('personalised service', 'service tailored to the needs of individual customers, often a strength of small businesses'),
         ('measures of business size', 'indicators such as number of employees, revenue, market share, capital employed and profit')],
  facts=[('Which of the following is a reason for a business to stay small?', 'The owner wants to keep control and provide a personalised service', ['To achieve purchasing economies of scale', 'To raise finance on a stock exchange', 'To dominate the market'], 'Small size can be a choice.'),
         ('Which is the most common way of measuring business size in many countries?', 'Number of employees', ['Number of products', 'Age of the business', 'Number of competitors'], 'The EU defines SMEs by headcount and turnover.'),
         ('Which is an advantage of small size?', 'Flexibility and quick decision-making', ['Lower interest rates on loans', 'Large marketing budgets', 'Bulk-buying discounts'], 'Short chains of command.')],
  why=[('Explain why some businesses choose to remain small.', 'Owners may want to keep control and avoid risk, serve niche markets that are limited in size, provide personalised service, or avoid diseconomies, regulation and the stress of growth.'),
       ('Explain why small businesses can be more flexible than large businesses.', 'With few layers of management, decisions are made quickly, communication is direct and the business can adapt products and services to changing customer needs.'),
       ('Explain why large size can be an advantage in a recession.', 'Large firms have more reserves, easier access to finance, diversified products and markets, and economies of scale that allow them to cut prices and survive.')],
  contrast=[('the advantages of small size', 'the advantages of large size', 'Small size brings flexibility, personal service and control; large size brings economies of scale, market power, easier finance and the ability to diversify risk.')],
  misc=[('A business with high revenue is always large in every other way.', 'Measures of size can disagree: a trading firm may have high revenue but few employees and little capital employed.')],
  cases=[('Morgan Motor Company', 'Morgan, a British car maker founded in 1910, builds a few hundred hand-made cars a year and has deliberately stayed small.', 'reasons for businesses to stay small', 'a niche, craft-based product and brand heritage depend on small-scale production'),
         ('independent bookshops', 'Independent bookshops in the UK grew in number for several years after 2016, competing with Amazon through events, personal recommendations and community roles.', 'the advantages of small size', 'personalised service and local identity provide a competitive advantage that large firms find hard to copy')],
  evaluate=[('Small businesses are more successful than large businesses.', ['flexibility and customer focus', 'niche markets', 'lower overheads'],
             ['lack of economies of scale', 'difficulty raising finance', 'vulnerable to competition and shocks', 'success depends on the market and owner objectives'], 'Neither size is inherently better; success depends on the market, the objectives of the owners and how well the business uses the advantages of its size.')],
  )

S('ch05-st4', concepts=('ethics', 'sustainability', 'change'),
  terms=[('multinational company (MNC)', 'a business that has its headquarters in one country and operates (produces or provides services) in more than one country'),
         ('host country', 'a country in which an MNC operates but where it does not have its headquarters'),
         ('home country', 'the country where an MNC has its headquarters'),
         ('foreign direct investment (FDI)', 'long-term investment by a business in productive assets in another country, such as factories or offices'),
         ('transfer pricing', 'the prices set for transactions between subsidiaries of the same MNC in different countries, which can be used to shift profits to low-tax countries')],
  facts=[('Which of the following is a benefit of an MNC to a host country?', 'Job creation and transfer of technology and skills', ['Lower tax revenue', 'Greater dependence on imports', 'Repatriation of profits'], 'MNCs bring capital and know-how.'),
         ('Which of the following is a possible disadvantage of MNCs for host countries?', 'Profits may be repatriated to the home country', ['More jobs for local workers', 'Higher exports', 'Improved infrastructure'], 'Profits flow abroad.'),
         ('In 2021 over 130 countries agreed through the OECD to a global minimum corporate tax rate of:', '15%', ['5%', '25%', '35%'], 'The agreement aims to reduce profit shifting by MNCs.')],
  why=[('Explain why businesses become multinational companies.', 'To access new markets and customers, reduce costs (labour, materials, transport), avoid trade barriers by producing inside markets, gain economies of scale and diversify risk.'),
       ('Explain why host countries compete to attract MNCs.', 'MNCs bring investment, jobs, tax revenue, exports and technology, which can raise growth and skills, so governments offer tax incentives and grants.'),
       ('Explain why MNCs may have considerable power over host-country governments.', 'Their size and ability to move production elsewhere give them bargaining power to secure tax breaks, subsidies or lighter regulation.')],
  contrast=[('the home country', 'the host country', 'The home country is where the MNC is headquartered; the host country is where it operates subsidiaries or production but is not headquartered.')],
  misc=[('MNCs always exploit host countries.', 'Impacts vary: MNCs can create jobs, pay above local wages and transfer skills, though some exploit weak regulation; outcomes depend on host-country policies.')],
  cases=[('Samsung in Vietnam', 'Samsung has invested over $20 bn in Vietnam since 2008, and its factories produce around half of its smartphones, accounting for a large share of Vietnam\'s exports.', 'the impact of MNCs on host countries', 'the investment created jobs and exports, though most high-value components and profits remain with Samsung'),
         ('Apple\'s tax case in Ireland', 'In 2024 the EU\'s Court of Justice ruled that Apple must pay Ireland €13 bn in back taxes for illegal state aid.', 'MNCs and taxation', 'MNCs can use favourable tax arrangements to shift profits, reducing tax paid in countries where sales are made'),
         ('Toyota in the UK', 'Toyota\'s factory at Burnaston in Derbyshire, opened in 1992, employs around 2,500 people and supplies cars to Europe.', 'reasons for becoming an MNC', 'producing inside the EU market reduced trade barriers and transport costs')],
  evaluate=[('The benefits of multinational companies for host countries outweigh the costs.', ['jobs and higher wages', 'technology and skills transfer', 'tax revenue and exports', 'infrastructure investment'],
             ['profit repatriation', 'tax avoidance through transfer pricing', 'competition harms local firms', 'environmental and labour exploitation'], 'MNCs usually bring net benefits when host governments negotiate well, enforce standards and ensure linkages with local firms.')],
  )


# =============================================================================================
# ch06 Units 2.1-2.2 Introduction to HRM and organizational structure
# =============================================================================================
@calc('ch06-st1', 'C3', (1, 4))
def labour_turnover(rng, slot):
    f_ = firm(rng)
    staff = rng.choice([40, 80, 120, 250, 400, 600])
    left = rng.randint(max(2, staff // 25), staff // 4)
    lt = 100 * left / staff
    days = rng.choice([220, 230, 240])
    lost = rng.randint(staff * 2, staff * 8)
    ab = 100 * lost / (staff * days)
    frame = rng.choice([f'{f_} employed an average of {staff} staff last year, and {left} employees left during the year.',
                        f'Last year {left} of the {staff} workers (average number employed) at {f_} resigned or were dismissed.'])
    if slot.d <= 2:
        return dict(stem=frame + ' Calculate the labour turnover rate.', answer=f'{p1(lt)}%',
                    markingKey=MK(f'Labour turnover = number leaving / average number employed × 100 = {left}/{staff} × 100 = {p1(lt)}%.', f'{p1(lt)}%'), marks=2)
    return dict(stem=frame + f' Each employee was expected to work {days} days, and {lost:,} working days were lost through absence. Calculate the labour turnover rate and the absenteeism rate, and explain one cost to {f_} of high labour turnover.',
                answer=f'Labour turnover = {p1(lt)}%; absenteeism = {lost:,}/({staff} × {days}) × 100 = {p2(ab)}%. Cost: recruitment, induction and training of replacements, and lost productivity while new staff learn the job.',
                markingKey=MK(f'LT = {left}/{staff} × 100 = {p1(lt)}%; absenteeism = days lost / total possible days × 100 = {p2(ab)}%.', 'both rates') + ' [R1] relevant cost explained.', marks=4)


S('ch06-st1', concepts=('change', 'ethics'),
  terms=[('human resource management (HRM)', 'the management of an organization\'s workforce, including workforce planning, recruitment, training, appraisal, motivation, dismissal and redundancy'),
         ('workforce planning', 'forecasting the number and type of employees an organization will need in the future and planning how to meet those needs'),
         ('recruitment', 'the process of identifying the need for a new employee, defining the job, attracting candidates and selecting the most suitable person'),
         ('appraisal', 'the formal assessment of an employee\'s performance against agreed objectives, usually leading to feedback and targets'),
         ('labour turnover', 'the percentage of employees who leave an organization during a period, usually a year'),
         ('on-the-job training', 'training that takes place while the employee is doing the job, for example through mentoring or job shadowing'),
         ('off-the-job training', 'training that takes place away from the normal work situation, such as courses at a college or training centre')],
  facts=[('Which of the following is a form of internal recruitment?', 'Promoting an existing employee to a vacant post', ['Advertising on LinkedIn', 'Using a recruitment agency', 'Attending a university job fair'], 'Internal recruitment fills posts from within.'),
         ('360-degree appraisal involves feedback from:', 'managers, peers, subordinates and sometimes customers', ['the employee only', 'shareholders only', 'the government'], 'Feedback from all directions.'),
         ('Which is a reason for high labour turnover?', 'Low pay and poor working conditions', ['Effective training', 'Good promotion prospects', 'Strong team spirit'], 'Dissatisfied staff leave.'),
         ('Which is an advantage of external recruitment?', 'It brings new ideas and skills into the organization', ['It is always cheaper', 'It motivates existing staff', 'The candidate already knows the culture'], 'Fresh perspectives.')],
  why=[('Explain why workforce planning is important.', 'It ensures the organization has the right number of people with the right skills at the right time, avoiding shortages that limit output or surpluses that raise costs.'),
       ('Explain why training can improve business performance.', 'Training raises skills and productivity, improves quality and customer service, increases motivation and reduces labour turnover.'),
       ('Explain why high labour turnover is costly for a business.', 'It increases recruitment and training costs, reduces productivity while new staff learn, damages morale and customer service, and may signal deeper problems.'),
       ('Explain why demographic change affects workforce planning.', 'Ageing populations, migration and changing participation rates alter the supply of labour and skills, so firms must plan for retirements, recruitment and flexible working.')],
  contrast=[('internal recruitment', 'external recruitment', 'Internal recruitment fills vacancies with existing employees (cheaper, motivating, known candidates); external recruitment attracts candidates from outside (new ideas, wider pool, but costly and slower).'),
            ('on-the-job training', 'off-the-job training', 'On-the-job training takes place while working (cheap, relevant, but may pass on bad habits); off-the-job training is away from the workplace (specialist, focused, but costly and time away from work).')],
  misc=[('Training is a cost that never benefits the business.', 'Training is an investment: it raises productivity, quality and motivation and can reduce turnover, although trained staff may leave for rivals.')],
  cases=[('Amazon\'s Career Choice programme', 'Amazon\'s Career Choice programme pre-pays tuition for warehouse employees to study for in-demand qualifications, even if the skills are for jobs outside Amazon.', 'training as an HR function', 'training improves retention and employer branding, although some trained employees leave'),
         ('Google\'s structured interviews', 'Google uses structured interviews and work-sample tests; its people analytics research found unstructured interviews poor predictors of performance.', 'recruitment and selection', 'evidence-based methods improve the quality of selection decisions'),
         ('Japan\'s ageing workforce', 'About 29% of Japan\'s population is aged 65 or over, and firms such as Toyota have raised retirement ages and employ older workers on new contracts.', 'workforce planning', 'demographic change forces firms to plan for retirements and labour shortages')],
  apply=[('A hotel chain plans to open five new hotels next year, each needing 60 staff. It currently has 900 staff and expects labour turnover of 15%. Calculate the number of staff it must recruit next year and suggest one recruitment method.', 'Replacements: 15% × 900 = 135; new staff: 5 × 60 = 300; total = 435. Method: online job platforms/careers website for large-volume recruitment, or internal promotion for supervisors.', 3),
         ('A retailer finds that 40% of new sales assistants leave within three months. Identify two possible HR causes and recommend one solution.', 'Causes: poor induction/training, low pay, unrealistic job expectations from recruitment adverts, poor management. Solution: structured induction and mentoring, or realistic job previews during recruitment.', 4)],
  evaluate=[('Investing in training is the most effective way for a business to reduce labour turnover.', ['raises skills and confidence', 'shows commitment to staff', 'career development'],
             ['pay and conditions may matter more', 'trained staff become attractive to rivals', 'management style and culture', 'cost'], 'Training helps, but turnover is reduced most effectively by combining development with fair pay, good management and career paths.')],
  )


@calc('ch06-st2', 'C3', (1, 4))
def span_levels(rng, slot):
    f_ = firm(rng)
    span = rng.choice([3, 4, 5, 6, 8])
    levels = rng.choice([3, 4, 5])
    tot = sum(span ** k for k in range(levels))
    bottom = span ** (levels - 1)
    if slot.d <= 2:
        return dict(stem=f'At {f_}, every manager has a span of control of {span}, and there are {levels} levels of hierarchy including the managing director at the top. Calculate the total number of employees and the number of employees at the lowest level.',
                    answer=f'Lowest level = {span}^{levels - 1} = {bottom}; total = ' + ' + '.join(str(span ** k) for k in range(levels)) + f' = {tot}.',
                    markingKey=MK('Each level has span × the number above it.', f'{tot} employees'), marks=2)
    new_span = span * 2
    lv = 1
    cnt = 1
    while cnt < tot:
        cnt += new_span ** lv
        lv += 1
    return dict(stem=f'{f_} has {levels} levels of hierarchy, with each manager supervising {span} subordinates. The company plans to delayer by doubling the span of control to {new_span}. Calculate the current number of employees, and the number of levels needed to employ at least the same number of people after delayering. Explain one benefit and one risk of delayering.',
                answer=f'Current employees = {tot}; with span {new_span}, levels needed = {lv}. Benefit: faster communication and lower management costs; risk: managers overloaded, less supervision and fewer promotion opportunities.',
                markingKey=MK(f'Total = Σ {span}^k = {tot}; with span {new_span}: cumulative 1, 1+{new_span}, ... ≥ {tot} at {lv} levels.', f'{tot} and {lv} levels') + ' [R1] benefit; [R1] risk.', marks=4)


S('ch06-st2', concepts=('change', 'creativity'),
  terms=[('organizational structure', 'the way an organization is arranged in terms of roles, responsibilities, lines of authority and communication'),
         ('hierarchy', 'the levels of authority in an organization, from the top (directors) to the bottom'),
         ('chain of command', 'the formal line of authority through which decisions and instructions are passed down an organization'),
         ('span of control', 'the number of subordinates directly responsible to one manager'),
         ('delayering', 'removing one or more levels of hierarchy from an organization\'s structure'),
         ('delegation', 'passing authority to a subordinate to carry out a task, while the manager retains overall responsibility'),
         ('bureaucracy', 'an organizational system with formal rules, procedures and levels of authority, which can slow decision-making')],
  facts=[('A wide span of control means that:', 'a manager supervises many subordinates', ['a manager supervises very few subordinates', 'there are many levels of hierarchy', 'employees have no manager'], 'Wide spans suit skilled, motivated teams.'),
         ('Delayering usually results in:', 'a flatter structure with wider spans of control', ['a taller structure', 'narrower spans of control', 'more middle managers'], 'Removing layers widens spans.'),
         ('A long chain of command can lead to:', 'slow and distorted communication', ['faster decision-making', 'less bureaucracy', 'wider spans of control'], 'Messages pass through many levels.')],
  why=[('Explain why delayering can reduce costs and speed up decision-making.', 'Removing layers of middle management reduces salary costs and shortens the chain of command, so information and decisions travel faster between top and bottom.'),
       ('Explain why delegation can motivate employees.', 'Being trusted with authority and responsibility gives recognition and opportunities to develop, meeting higher-level needs (Maslow) and motivators (Herzberg).'),
       ('Explain why a narrow span of control may be appropriate in some situations.', 'Where tasks are complex or risky, or staff are inexperienced, close supervision and support are needed, so managers can only effectively supervise a few people.')],
  contrast=[('span of control', 'chain of command', 'Span of control is the number of subordinates directly reporting to a manager; chain of command is the line of authority from the top to the bottom of the organization.'),
            ('delegation', 'empowerment', 'Delegation passes authority for specific tasks to subordinates; empowerment gives employees broader power to make decisions about their own work.')],
  misc=[('Delegating a task means the manager is no longer responsible for it.', 'Authority is delegated but responsibility remains with the manager, who is still accountable for the outcome.')],
  cases=[('Haier\'s micro-enterprises', 'Chinese appliance maker Haier removed around 10,000 middle-management jobs and reorganised into thousands of small, self-managing "micro-enterprises" (the rendanheyi model).', 'delayering and delegation', 'removing hierarchy and delegating decisions to small teams aimed to speed up innovation and customer responsiveness'),
         ('Meta\'s "year of efficiency" in 2023', 'In 2023 Meta cut about 21,000 jobs and removed layers of middle management, with Mark Zuckerberg calling it a "year of efficiency".', 'delayering', 'a flatter structure aimed to reduce costs and speed up decisions, though it increased workload and uncertainty for staff'),
         ('the British Army', 'The army relies on a tall hierarchy with a clear chain of command and narrow spans of control in combat units.', 'hierarchy and chain of command', 'clear authority and close supervision are vital where decisions are high-risk and must be carried out quickly')],
  apply=[('A company has five levels of hierarchy and an average span of control of 4. A consultant recommends removing one level. Explain two likely effects on the remaining managers.', 'Wider spans of control: more subordinates each, heavier workload and less time per employee; more delegation and responsibility, which may motivate but also stress them; faster communication with the top.', 4)],
  evaluate=[('Delayering always improves the performance of an organization.', ['lower costs', 'faster communication and decisions', 'more delegation and empowerment'],
             ['managers become overloaded', 'loss of experience and promotion paths', 'fear and low morale among survivors', 'less supervision may reduce quality'], 'Delayering can improve performance where staff are skilled and systems strong, but it fails if spans become too wide or it is used only to cut costs.')],
  )

S('ch06-st3', concepts=('change', 'creativity'),
  terms=[('flat structure', 'an organizational structure with few levels of hierarchy and wide spans of control'),
         ('tall structure', 'an organizational structure with many levels of hierarchy and narrow spans of control'),
         ('matrix structure', 'a structure in which employees report to both a functional manager and a project or product manager'),
         ('project-based organization', 'a structure in which teams are formed around projects, often temporarily, and disbanded when the project ends'),
         ('centralisation', 'the concentration of decision-making authority at the top of an organization'),
         ('decentralisation', 'the delegation of decision-making authority to lower levels or to regional or local managers')],
  facts=[('Which structure is most associated with employees having two managers?', 'Matrix', ['Tall', 'Flat', 'Centralised'], 'Functional and project managers.'),
         ('A fast-food chain where all menus and prices are decided at head office is an example of:', 'centralisation', ['decentralisation', 'a matrix structure', 'delayering'], 'Decisions are taken at the top.'),
         ('Which is an advantage of decentralisation for a multinational company?', 'Local managers can respond to local market conditions', ['Uniform decisions everywhere', 'Lower need for skilled managers', 'More control by head office'], 'Local knowledge.')],
  why=[('Explain why a matrix structure can encourage creativity.', 'People from different functions work together on projects, combining skills and perspectives, which helps generate innovative ideas.'),
       ('Explain why matrix structures can cause problems.', 'Employees with two managers may face conflicting instructions and priorities, causing confusion, stress and power struggles.'),
       ('Explain why a growing multinational might decentralise decision-making.', 'Head office cannot make good decisions about many local markets; local managers understand customers, laws and culture, so decentralisation speeds response and motivates managers.')],
  contrast=[('a flat structure', 'a tall structure', 'A flat structure has few levels and wide spans of control, with faster communication; a tall structure has many levels and narrow spans, with closer supervision but slower communication.'),
            ('centralisation', 'decentralisation', 'Centralisation keeps decision-making at the top; decentralisation passes decisions to lower levels or regions.')],
  misc=[('Flat structures are always better than tall structures.', 'Flat structures suit innovative, skilled teams, but tall structures provide control, clear promotion paths and supervision where consistency and safety matter.')],
  cases=[('Zappos and holacracy', 'Online shoe retailer Zappos adopted "holacracy" in 2014, replacing managers with self-organising circles; about 18% of staff took a buyout offer to leave.', 'flat and alternative structures', 'removing hierarchy increased autonomy for some but caused confusion and resistance for others'),
         ('Nestlé\'s country-level management', 'Nestlé operates in over 180 countries and gives country managers significant freedom over local products and marketing, while R&D and brands are coordinated centrally.', 'decentralisation in a multinational', 'balancing central control with local decision-making helps adapt products to local tastes'),
         ('Valve\'s flat structure', 'Video game company Valve has described itself as having almost no managers, with employees choosing which projects to work on.', 'flat structures', 'very wide autonomy encourages creativity but can make accountability and coordination difficult')],
  apply=[('A global consulting firm organizes staff by function (strategy, finance, IT) but forms teams for each client project. Identify the structure and explain one advantage and one disadvantage for the employees.', 'Matrix structure. Advantage: varied work and skill development across projects. Disadvantage: two managers can give conflicting priorities, causing stress.', 4)],
  evaluate=[('Decentralised decision-making is more effective than centralised decision-making for a multinational company.', ['local responsiveness', 'faster decisions', 'motivated local managers'],
             ['loss of consistency and brand control', 'duplication of costs', 'local managers may pursue local goals', 'risk of poor decisions'], 'Most MNCs combine both: centralising strategy, brand and finance while decentralising operational and marketing decisions.')],
  )

S('ch06-st4', concepts=('change', 'ethics'),
  terms=[('flexible working', 'working arrangements that vary hours or location, such as flexitime, part-time work, remote or hybrid working and compressed hours'),
         ('gig economy', 'a labour market in which workers are engaged for short-term tasks or "gigs", often through digital platforms, rather than permanent jobs'),
         ('outsourcing', 'contracting out an activity to an external organization rather than doing it in-house'),
         ('offshoring', 'relocating business activities to another country'),
         ('teleworking', 'working away from the employer\'s premises, usually at home, using information and communication technology')],
  facts=[('Uber drivers and Deliveroo riders are examples of workers in:', 'the gig economy', ['the public sector', 'trade unions', 'cooperatives'], 'Task-based work via apps.'),
         ('In 2021 the UK Supreme Court ruled that Uber drivers were:', 'workers entitled to the minimum wage and holiday pay', ['self-employed with no rights', 'employees of the government', 'shareholders'], 'A landmark employment rights ruling.'),
         ('Which of the following is an example of offshoring?', 'A UK bank moving its call centre to India', ['A firm hiring a local cleaning company', 'A firm introducing flexitime', 'A firm opening a new UK branch'], 'Relocation abroad.')],
  why=[('Explain why many businesses introduced hybrid working after the Covid-19 pandemic.', 'Employees valued flexibility, so offering hybrid work helps recruitment and retention; firms can also reduce office space costs, while technology makes remote collaboration possible.'),
       ('Explain why the gig economy can be attractive to businesses.', 'Firms pay only for work done, avoid employment costs such as holiday pay and pensions, and can scale the workforce up or down quickly.'),
       ('Explain why outsourcing can reduce quality.', 'The business has less direct control over the processes and staff of the supplier, which may focus on cost-cutting, leading to errors or poor customer service.')],
  contrast=[('outsourcing', 'offshoring', 'Outsourcing contracts an activity to another organization (in the same or another country); offshoring moves an activity to another country, either to a supplier or to the firm\'s own subsidiary.')],
  misc=[('Gig economy workers always prefer flexible jobs to permanent employment.', 'Many value flexibility, but others face insecure incomes, no sick pay and limited rights, and would prefer stable contracts.')],
  cases=[('Uber and worker status in the UK', 'The UK Supreme Court ruled in 2021 that Uber drivers are "workers", entitled to the minimum wage and holiday pay; Uber then extended these to about 70,000 drivers.', 'changes in work patterns', 'the legal status of gig workers affects their rights and firms\' costs'),
         ('remote working at Atlassian', 'Australian software firm Atlassian introduced "Team Anywhere" in 2020, allowing most staff to work from wherever they choose.', 'flexible working', 'location flexibility widens the talent pool and helps retention, but requires new ways of collaboration'),
         ('Apple and Foxconn', 'Apple designs iPhones in California but outsources assembly to contract manufacturers such as Foxconn in China and increasingly in India.', 'outsourcing and offshoring', 'outsourcing lowers costs and gives flexibility but creates reputational risks over working conditions')],
  apply=[('A software company is considering allowing all staff to work from home four days a week. Explain one benefit and one problem for the company.', 'Benefit: lower office costs and a wider pool of applicants, plus higher retention. Problem: harder collaboration, communication and supervision; weaker culture and onboarding of new staff.', 4)],
  evaluate=[('The growth of the gig economy benefits both businesses and workers.', ['flexibility for workers to choose hours', 'lower costs and scalability for firms', 'easy entry into work'],
             ['job and income insecurity', 'lack of sick pay, pensions and rights', 'legal challenges (Uber)', 'lower loyalty and quality'], 'Firms gain more clearly than workers; the balance depends on regulation that protects gig workers while preserving flexibility.')],
  )


# =============================================================================================
# ch07 Unit 2.3 Leadership and management
# =============================================================================================
S('ch07-st1', concepts=('change', 'ethics'),
  terms=[('management', 'the process of achieving organizational objectives by planning, organizing, commanding, coordinating and controlling resources'),
         ('leadership', 'the ability to influence, inspire and motivate others to work towards achieving goals'),
         ('Fayol\'s functions of management', 'Henri Fayol\'s five functions of management: planning, organizing, commanding, coordinating and controlling'),
         ('planning (management)', 'setting objectives and deciding the strategies and actions needed to achieve them'),
         ('controlling (management)', 'monitoring performance against targets and taking corrective action when needed')],
  facts=[('Which of the following is one of Fayol\'s functions of management?', 'Coordinating', ['Motivating through hygiene factors', 'Delegating to the gig economy', 'Benchmarking'], 'Plan, organize, command, coordinate, control.'),
         ('Which statement best distinguishes leadership from management?', 'Leaders inspire people towards a vision; managers plan and control resources to achieve objectives', ['Managers set the vision; leaders only follow rules', 'Leadership and management are identical', 'Leaders never make decisions'], 'Leadership is about influence; management about processes.'),
         ('Monitoring sales against budget and taking corrective action is an example of:', 'controlling', ['planning', 'commanding', 'organizing'], 'Control compares results to targets.')],
  why=[('Explain why both leadership and management are needed in an organization.', 'Management ensures resources are planned, organized and controlled efficiently; leadership sets direction and inspires people, especially during change; an organization needs both to be efficient and adaptable.'),
       ('Explain why controlling is an important function of management.', 'Without monitoring performance against targets, problems such as overspending or falling quality are not detected and corrected in time.'),
       ('Explain why effective leaders are particularly important during periods of change.', 'Change creates uncertainty and resistance; leaders who communicate a clear vision and build trust help employees accept and support new ways of working.')],
  contrast=[('leadership', 'management', 'Leadership is about setting direction and inspiring people; management is about planning, organizing and controlling resources to achieve objectives efficiently.')],
  misc=[('Every manager is automatically a good leader.', 'Managers have formal authority, but leadership requires the ability to influence and inspire, which not all managers have; leaders can also exist without formal positions.')],
  cases=[('Satya Nadella at Microsoft', 'After becoming CEO in 2014, Satya Nadella promoted a "growth mindset" culture and shifted Microsoft towards cloud computing; its market value rose from about $300 bn to over $3 trillion.', 'leadership versus management', 'a clear vision and cultural change inspired employees, while strong management delivered the cloud strategy'),
         ('Fayol\'s functions at a supermarket', 'A supermarket store manager plans staff rotas, organizes deliveries, gives instructions to supervisors, coordinates departments and controls stock losses against targets.', 'Fayol\'s functions of management', 'the daily work of a store manager illustrates all five of Fayol\'s functions')],
  apply=[('A new restaurant manager finds that food waste is 15% above target and staff often arrive late. Using Fayol\'s functions of management, suggest how the manager could address these problems.', 'Planning: set waste and punctuality targets; organizing: reorganize ordering and rotas; commanding: give clear instructions; coordinating: align kitchen and front-of-house; controlling: monitor waste and lateness weekly and take corrective action.', 4)],
  evaluate=[('Leadership is more important than management for the success of a business.', ['vision and motivation drive innovation', 'leaders guide change', 'culture and engagement'],
             ['without planning and control, resources are wasted', 'routine operations depend on management', 'depends on the situation and industry'], 'Both are essential: leadership matters most in times of change and innovation, management in stable, efficiency-driven operations.')],
  )

S('ch07-st2', concepts=('change', 'ethics', 'creativity'),
  terms=[('autocratic leadership', 'a leadership style in which the leader makes decisions alone and expects employees to follow instructions, with little consultation'),
         ('paternalistic leadership', 'a style in which the leader makes decisions in what he or she believes are the best interests of employees, treating them like a family'),
         ('democratic leadership', 'a style in which the leader involves employees in decision-making, consults and encourages participation'),
         ('laissez-faire leadership', 'a style in which the leader gives employees a high degree of freedom to make decisions and organize their work, with minimal interference'),
         ('situational leadership', 'an approach in which the leader adapts his or her style to the situation, task and the readiness of followers')],
  facts=[('Which leadership style is most suitable in an emergency requiring quick decisions?', 'Autocratic', ['Laissez-faire', 'Democratic', 'Paternalistic'], 'Fast, clear decisions are needed.'),
         ('A leader of a team of highly skilled research scientists who sets broad goals and lets the team decide how to work is using:', 'laissez-faire leadership', ['autocratic leadership', 'paternalistic leadership', 'scientific management'], 'Freedom for experts.'),
         ('George Cadbury\'s provision of housing and facilities for workers at Bournville is associated with:', 'paternalistic leadership', ['laissez-faire leadership', 'democratic leadership', 'autocratic leadership only'], 'Caring for employees\' welfare.'),
         ('Situational leadership theory was developed by:', 'Hersey and Blanchard', ['Maslow and Herzberg', 'Fayol and Taylor', 'Adams and Pink'], 'Style matched to follower readiness.')],
  why=[('Explain why democratic leadership can improve motivation.', 'Employees who are consulted feel valued and have ownership of decisions, meeting esteem and self-actualisation needs; their knowledge also improves decision quality.'),
       ('Explain why autocratic leadership can lead to high labour turnover.', 'Employees have little say, may feel undervalued and frustrated, and their ideas are ignored, so motivated staff may leave.'),
       ('Explain why laissez-faire leadership may fail with inexperienced staff.', 'Without guidance or clear objectives, inexperienced staff may lack direction, make mistakes and feel unsupported, lowering productivity.')],
  contrast=[('autocratic leadership', 'democratic leadership', 'Autocratic leaders make decisions alone and give instructions; democratic leaders consult and involve employees in decisions.'),
            ('paternalistic leadership', 'laissez-faire leadership', 'Paternalistic leaders make decisions they believe benefit employees and care for their welfare; laissez-faire leaders give employees freedom to make their own decisions with little involvement.')],
  misc=[('Democratic leadership is always the best style.', 'Consultation is slow and can be inappropriate in crises or with inexperienced staff; the best style depends on the situation (situational leadership).')],
  cases=[('Elon Musk at Twitter/X', 'After buying Twitter in 2022, Elon Musk cut about 80% of staff and told employees to commit to being "extremely hardcore" or leave.', 'autocratic leadership', 'rapid top-down decisions cut costs quickly but damaged morale, trust and relations with advertisers'),
         ('Jacinda Ardern\'s Covid-19 response', 'New Zealand\'s Prime Minister Jacinda Ardern combined fast, firm decisions in March 2020 with clear, empathetic daily communication.', 'situational leadership', 'she adapted her style, being directive in the crisis while consulting experts and building public trust'),
         ('Tata Group', 'The Tata Group in India built townships, hospitals and schools for workers, beginning with Jamsetji Tata\'s steel works at Jamshedpur in the early 1900s.', 'paternalistic leadership', 'caring for employee welfare built loyalty and long-term commitment')],
  apply=[('A start-up founder makes every decision personally, but the team of 25 software developers complains that their ideas are ignored and two have resigned. Recommend a more suitable leadership style and justify your answer.', 'Democratic or laissez-faire: skilled developers expect involvement and autonomy; consulting them improves motivation, retention and creativity, while the founder retains final authority on strategy.', 4)],
  evaluate=[('There is no single best leadership style.', ['situational theory: depends on task and followers', 'crises need autocratic decisions', 'experts need autonomy'],
             ['democratic leadership generally improves engagement', 'consistency of style builds trust', 'culture may favour one style'], 'Effective leaders adapt their style to the situation, although democratic approaches generally suit knowledge-based organizations.')],
  )

S('ch07-st3', concepts=('ethics', 'change'),
  terms=[('ethical leadership', 'leadership that is guided by moral principles such as honesty, fairness, integrity and respect for stakeholders'),
         ('organizational culture (leadership)', 'the shared values, beliefs and norms in an organization, which leaders shape through their behaviour'),
         ('national culture', 'the shared values, beliefs and practices of people in a country, which influence expectations of leaders'),
         ('power distance', 'Hofstede\'s cultural dimension measuring how far less powerful members of a society accept unequal distribution of power')],
  facts=[('In a country with high power distance, employees are more likely to:', 'accept an autocratic leadership style', ['expect to be consulted on every decision', 'reject all hierarchy', 'prefer laissez-faire leaders'], 'Hierarchy is seen as natural.'),
         ('Which researcher developed the cultural dimensions of power distance and individualism?', 'Geert Hofstede', ['Frederick Taylor', 'Abraham Maslow', 'Daniel Pink'], 'Hofstede\'s cultural dimensions theory.'),
         ('The collapse of Enron in 2001 is often linked to:', 'unethical leadership and accounting fraud', ['excessive democratic leadership', 'too much delegation to workers', 'franchising'], 'Leaders hid debts through fraudulent accounting.')],
  why=[('Explain why national culture can influence the choice of leadership style.', 'Cultures differ in attitudes to hierarchy and individualism; in high power-distance cultures directive leadership may be expected, while in low power-distance cultures employees expect consultation.'),
       ('Explain why ethical leadership can improve business performance.', 'It builds trust with employees, customers and investors, reduces legal and reputational risks and creates a culture where staff behave responsibly.'),
       ('Explain why leaders of multinational companies need cultural awareness.', 'Managing diverse teams and markets requires adapting communication and decision-making to local values to avoid misunderstanding and conflict.')],
  contrast=[('ethical leadership', 'legal compliance', 'Ethical leadership is guided by moral principles beyond the law; legal compliance simply means obeying the law.')],
  misc=[('A leadership style that works in one country will work everywhere.', 'National cultures differ in attitudes to authority, communication and teamwork, so styles must be adapted.')],
  cases=[('Carlos Ghosn at Nissan', 'Carlos Ghosn turned Nissan around after 1999 but was arrested in Japan in 2018 over alleged financial misconduct and fled to Lebanon in 2019.', 'ethical issues in leadership', 'allegations of misconduct by a celebrated leader damaged the company and the Renault-Nissan alliance'),
         ('Indra Nooyi at PepsiCo', 'As CEO of PepsiCo (2006-2018), Indra Nooyi introduced "Performance with Purpose", shifting the portfolio towards healthier products and sustainability goals.', 'ethical influences on leadership', 'linking performance to social and environmental purpose shaped strategy and culture')],
  apply=[('A Scandinavian manager is appointed to run a subsidiary in a country with high power distance. Explain one challenge she may face and how she could adapt her leadership style.', 'Challenge: employees may expect clear instructions and be reluctant to give opinions; adapt by being more directive initially while gradually building trust and consultation.', 3)],
  evaluate=[('Ethical leadership is more important than profitability for long-term business success.', ['trust and reputation', 'lower legal risks', 'employee engagement'],
             ['without profit the firm cannot survive', 'shareholder pressure for returns', 'ethical choices may raise costs'], 'Ethical leadership and long-term profitability are complementary; firms that sacrifice ethics for short-term profit, like Volkswagen or Enron, often destroy value.')],
  )


# =============================================================================================
# ch08 Unit 2.4 Motivation and demotivation
# =============================================================================================
S('ch08-st1', concepts=('change', 'ethics'),
  terms=[('motivation', 'the internal and external factors that stimulate people to work towards achieving a goal'),
         ('scientific management (Taylor)', 'Frederick Taylor\'s approach of breaking jobs into simple tasks, finding the most efficient method and paying workers by piece rate, assuming money is the main motivator'),
         ('Maslow\'s hierarchy of needs', 'a theory that people are motivated by five levels of needs – physiological, safety, social, esteem and self-actualisation – satisfied in order from the bottom'),
         ('Herzberg\'s two-factor theory', 'a theory that hygiene factors (pay, conditions, policies) cause dissatisfaction if inadequate, while motivators (achievement, recognition, responsibility, the work itself) create satisfaction'),
         ('hygiene factors', 'aspects of work, such as pay, working conditions and company policy, that do not motivate but cause dissatisfaction if absent'),
         ('self-actualisation', 'the highest level of Maslow\'s hierarchy: realising one\'s full potential')],
  facts=[('According to Herzberg, which of the following is a motivator?', 'Recognition for achievement', ['Salary', 'Working conditions', 'Company policy'], 'Motivators relate to the work itself.'),
         ('According to Maslow, which need must normally be met first?', 'Physiological needs', ['Esteem needs', 'Self-actualisation', 'Social needs'], 'Basic needs at the base of the hierarchy.'),
         ('Taylor\'s scientific management assumed that workers are mainly motivated by:', 'money', ['self-actualisation', 'social relationships', 'job enrichment'], 'Piece-rate pay.'),
         ('Job security and a safe workplace relate to which level of Maslow\'s hierarchy?', 'Safety needs', ['Social needs', 'Esteem needs', 'Physiological needs'], 'Protection from harm and insecurity.')],
  why=[('Explain why, according to Herzberg, a pay rise may not motivate employees in the long term.', 'Pay is a hygiene factor: adequate pay removes dissatisfaction but does not create lasting motivation, which comes from achievement, recognition, responsibility and interesting work.'),
       ('Explain why Taylor\'s approach can increase productivity but reduce job satisfaction.', 'Specialised, standardised tasks and piece rates raise output, but repetitive work offers little variety, responsibility or social contact, causing boredom and alienation.'),
       ('Explain why Maslow\'s theory may not apply equally to all employees.', 'People do not always satisfy needs in strict order, priorities differ between individuals and cultures, and needs are difficult to measure.')],
  contrast=[('hygiene factors', 'motivators', 'Hygiene factors (pay, conditions, policies) prevent dissatisfaction but do not motivate; motivators (achievement, recognition, responsibility, the work itself) create job satisfaction and motivation.'),
            ('Taylor\'s view of motivation', 'Maslow\'s view of motivation', 'Taylor saw workers as motivated mainly by money and close supervision; Maslow saw them as motivated by a hierarchy of needs, including social, esteem and self-actualisation needs.')],
  misc=[('Herzberg said that pay does not matter at all.', 'Pay is a hygiene factor: if it is too low it causes dissatisfaction; it simply does not create lasting motivation on its own.')],
  cases=[('Taylor at Bethlehem Steel', 'In the late 1890s Taylor studied pig-iron handling at Bethlehem Steel and claimed that, with the right methods, rest breaks and piece rates, a worker\'s daily load rose from about 12.5 to 47 tonnes.', 'scientific management', 'standardised methods and financial incentives raised productivity, but treated workers like parts of a machine'),
         ('Amazon warehouses', 'Amazon warehouse workers\' productivity is tracked by detailed rates of picks per hour, and the firm has faced criticism over injury rates and pressure.', 'Taylorism in modern workplaces', 'close monitoring and targets raise efficiency, but may cause stress and dissatisfaction'),
         ('Google\'s workplace culture', 'Google is known for offering free meals, wellness services and learning opportunities, and for projects that give engineers autonomy.', 'Maslow\'s and Herzberg\'s theories', 'meeting lower-level needs and offering challenging work aims to address hygiene factors and motivators together')],
  apply=[('A call centre pays above-average wages but has high labour turnover. Employees say the work is repetitive and they never receive praise. Using Herzberg\'s theory, explain why staff are demotivated and suggest one solution.', 'Hygiene factors (pay) are met, so dissatisfaction from pay is low, but motivators are missing: no recognition, responsibility or interesting work. Solution: job enrichment, recognition schemes, team leader roles or empowerment.', 4)],
  evaluate=[('Content theories of motivation are of little use to modern managers.', ['based on old studies (Taylor 1900s, Maslow 1943, Herzberg 1959)', 'oversimplify human behaviour', 'cultural bias'],
             ['still explain why pay alone does not motivate', 'guide job design and reward systems', 'provide a common framework'], 'They remain useful frameworks for understanding needs, but managers should combine them with process theories and evidence from their own workforce.')],
  )

S('ch08-st2', concepts=('ethics', 'change'),
  terms=[('Adams\' equity theory', 'a process theory that employees compare the ratio of their inputs (effort, skills) to outputs (pay, recognition) with that of others, and are demotivated if they perceive unfairness'),
         ('Pink\'s drive theory', 'Daniel Pink\'s theory that, for complex creative work, people are motivated mainly by autonomy, mastery and purpose rather than external rewards'),
         ('autonomy', 'the desire to direct one\'s own work and life'),
         ('mastery', 'the desire to get better at something that matters'),
         ('purpose', 'the desire to do something that serves a cause larger than oneself')],
  facts=[('According to Adams, an employee who feels under-rewarded compared with colleagues may:', 'reduce effort or ask for higher pay', ['work harder without complaint', 'always leave immediately', 'ignore the comparison'], 'Restoring perceived equity.'),
         ('Which three elements are central to Pink\'s drive theory?', 'Autonomy, mastery and purpose', ['Pay, conditions and security', 'Planning, organizing and controlling', 'Physiological, safety and social'], 'Intrinsic motivators.'),
         ('Pink argues that "carrot and stick" incentives work best for:', 'simple, routine tasks', ['complex creative tasks', 'all tasks equally', 'no tasks at all'], 'Extrinsic rewards suit algorithmic work.')],
  why=[('Explain why perceived unfairness in pay can demotivate employees.', 'According to Adams, people compare their input-output ratio with others; if colleagues receive more for similar effort, the employee feels inequity and may reduce effort, complain or leave.'),
       ('Explain why bonuses may reduce performance in creative jobs, according to Pink.', 'Extrinsic rewards narrow focus and can crowd out intrinsic motivation; creative work is better driven by autonomy, mastery and purpose.'),
       ('Explain why transparency about pay structures can support equity.', 'Clear criteria and pay bands allow employees to see that rewards reflect inputs, reducing perceptions of unfairness.')],
  contrast=[('content theories', 'process theories', 'Content theories (Maslow, Herzberg) identify what needs motivate people; process theories (Adams, Pink) explain how people decide on effort based on perceptions such as fairness or intrinsic drives.')],
  misc=[('According to Pink, money is irrelevant to motivation.', 'Pink argues pay must be fair and adequate to "take the issue of money off the table"; beyond that, autonomy, mastery and purpose drive motivation in creative work.')],
  cases=[('the BBC gender pay revelations', 'In 2017 the BBC had to publish the salaries of its highest-paid stars, revealing that two-thirds were men; female presenters protested and some pay was adjusted.', 'Adams\' equity theory', 'perceived unfairness relative to colleagues led to demotivation, protest and changes in pay'),
         ('Atlassian\'s "ShipIt" days', 'Software firm Atlassian runs quarterly 24-hour "ShipIt" hackathons where staff work on any project they choose.', 'Pink\'s drive theory', 'giving autonomy over creative work encourages mastery and innovation'),
         ('Patagonia\'s purpose', 'Patagonia\'s stated purpose is "We\'re in business to save our home planet", which it says helps attract and retain committed employees.', 'purpose as a motivator', 'employees motivated by a cause larger than themselves show greater commitment')],
  apply=[('Two engineers at the same firm do similar work, but one discovers that the other earns 15% more. Using Adams\' equity theory, explain how the lower-paid engineer may react and what the manager should do.', 'Perceived inequity: may reduce effort, demand a pay rise, lower quality or leave. Manager should explain any objective differences (experience, performance) or adjust pay to restore equity.', 4)],
  evaluate=[('Pink\'s drive theory is the most relevant motivation theory for twenty-first century businesses.', ['knowledge and creative work dominate', 'evidence that autonomy improves engagement', 'explains why bonuses can fail'],
             ['less relevant for routine jobs', 'pay and security still matter', 'autonomy may not suit all cultures or staff'], 'Pink\'s theory is highly relevant for creative work, but managers should also ensure fair pay (Adams) and basic needs (Maslow, Herzberg).')],
  )


@calc('ch08-st3', 'C3', (1, 5))
def pay_calc(rng, slot):
    who = name(rng)
    c = cur(rng)
    if slot.d <= 2:
        base = rng.choice([1200, 1500, 1800, 2000])
        sales = rng.choice([20_000, 35_000, 50_000, 80_000])
        rate = rng.choice([2, 3, 4, 5])
        tot = base + sales * rate / 100
        return dict(stem=rng.choice([f'{who}, a sales representative, earns a basic salary of {m(base, c)} a month plus {rate}% commission on sales. In March {who} sold goods worth {m(sales, c)}. Calculate {who}\'s total pay for March.',
                                     f'A car dealership pays {who} {m(base, c)} a month plus commission of {rate}% of the value of cars sold. Last month {who} sold cars worth {m(sales, c)}. Calculate total earnings.']),
                    answer=m(tot, c), markingKey=MK(f'{base} + {rate}% × {sales:,} = {base} + {sales * rate / 100:,.0f} = {tot:,.0f}.', m(tot, c)), marks=2)
    pool_pct = rng.choice([5, 8, 10])
    profit = rng.choice([400_000, 600_000, 900_000, 1_200_000])
    staff = rng.choice([40, 50, 80, 100])
    sal = rng.choice([30_000, 36_000, 42_000])
    share = profit * pool_pct / 100 / staff
    if slot.d == 3:
        return dict(stem=f'A firm shares {pool_pct}% of its annual profit of {m(profit, c)} equally among its {staff} employees through profit-related pay. Calculate each employee\'s profit share and express it as a percentage of an average salary of {m(sal, c)}.',
                    answer=f'Profit share = {m(share, c)} per employee = {p1(100 * share / sal)}% of salary',
                    markingKey=MK(f'{pool_pct}% × {profit:,} / {staff} = {share:,.0f}; {share:,.0f}/{sal:,} × 100 = {p1(100 * share / sal)}%.', 'both values'), marks=3)
    hrs = rng.choice([38, 40])
    rate = rng.choice([12, 15, 18, 20])
    units_std = rng.choice([200, 250, 300])
    pr = rng.choice([0.5, 0.6, 0.8, 1.0])
    units = units_std + rng.choice([-30, 20, 50, 80])
    time_pay = hrs * rate
    piece_pay = units * pr * rate / 1.0 if False else units * pr
    piece_pay = units * (time_pay / units_std)
    return dict(stem=f'{who} works {hrs} hours a week at {m(rate, c)} per hour. The firm proposes replacing time rate with a piece rate of {m(time_pay / units_std, c)} per unit (so that a worker producing the standard {units_std} units a week earns the same). {who} normally produces {units} units a week. Calculate {who}\'s weekly pay under each system, and evaluate one advantage and one disadvantage of piece rate for the firm.',
                answer=f'Time rate: {hrs} × {rate} = {m(time_pay, c)}; piece rate: {units} × {p2(time_pay / units_std)} = {m(piece_pay, c)}. Advantage: pay linked to output encourages productivity and controls labour cost per unit. Disadvantage: workers may rush and quality may fall; output may vary, and it suits only measurable tasks.',
                markingKey=MK(f'Time: {time_pay}; piece: {units} × {p2(time_pay / units_std)} = {piece_pay:.2f}.', 'both weekly pays') + ' [R1] advantage; [R1] disadvantage.', marks=4 if slot.d == 4 else 6)


S('ch08-st3', concepts=('ethics', 'change'),
  terms=[('salary', 'a fixed annual payment to an employee, usually paid monthly, regardless of the number of hours worked'),
         ('wages', 'payment to employees based on time worked (time rate) or output produced (piece rate), usually paid weekly'),
         ('commission', 'a payment based on a percentage of the value of sales made by an employee'),
         ('profit-related pay', 'a payment to employees based on the profits made by the business'),
         ('performance-related pay (PRP)', 'a payment to employees based on their individual performance, usually assessed against targets in an appraisal'),
         ('fringe payments', 'benefits in addition to pay, such as company cars, health insurance, pension contributions and discounts')],
  facts=[('Which financial reward is most suitable for sales staff?', 'Commission', ['Fixed salary only', 'Piece rate', 'Profit-related pay only'], 'Linked to the value of sales.'),
         ('A company car and private health insurance are examples of:', 'fringe payments', ['commission', 'piece rates', 'profit-related pay'], 'Non-wage benefits.'),
         ('Which is a disadvantage of performance-related pay?', 'Appraisal targets may be seen as unfair or subjective', ['It never links reward to effort', 'It is always cheaper', 'It cannot be used for managers'], 'Assessment can cause resentment.')],
  why=[('Explain why profit-related pay may encourage teamwork.', 'All employees share in the profits of the whole business, so they have a common interest in improving performance and cooperating rather than competing.'),
       ('Explain why commission can lead to unethical selling practices.', 'Staff paid mainly on sales value may pressure customers into unsuitable products to increase their earnings, damaging trust and reputation (e.g. mis-selling of financial products).'),
       ('Explain why fringe payments can help a business recruit and retain staff.', 'Benefits such as health insurance, pensions and flexible perks increase the total value of the reward package and make the employer more attractive than rivals.')],
  contrast=[('time rate', 'piece rate', 'Time rate pays workers for the hours they work; piece rate pays for each unit produced, linking pay to output.'),
            ('profit-related pay', 'performance-related pay', 'Profit-related pay depends on the profits of the whole business; performance-related pay depends on the individual\'s performance against targets.')],
  misc=[('Financial rewards are the only effective way to motivate employees.', 'Financial rewards matter, but non-financial factors such as recognition, responsibility, purpose and teamwork are also powerful motivators (Herzberg, Pink).')],
  cases=[('Wells Fargo\'s fake accounts scandal', 'Between 2002 and 2016 Wells Fargo employees opened millions of unauthorised customer accounts to meet aggressive sales targets; the bank paid about $3 bn to settle charges in 2020.', 'the risks of sales-based financial rewards', 'incentives tied to sales volume encouraged unethical behaviour and damaged the bank\'s reputation'),
         ('John Lewis Partnership bonus', 'John Lewis Partners received bonuses of up to around 18% of salary in good years, but no bonus was paid in 2021 and 2023 as profits fell.', 'profit-related pay', 'rewards rise and fall with company profits, sharing success but also risk'),
         ('Microsoft\'s abolition of stack ranking', 'In 2013 Microsoft abandoned "stack ranking", which forced managers to rate a fixed share of staff as poor performers.', 'performance-related pay and appraisal', 'forced rankings harmed collaboration, so the firm moved to more qualitative feedback')],
  apply=[('A hotel chain wants to improve customer satisfaction scores. Evaluate whether it should introduce commission, profit-related pay or performance-related pay for reception staff.', 'Commission is unsuitable (reception staff don\'t sell much); profit-related pay encourages teamwork but is distant from individual effort; PRP linked to customer feedback targets links reward to service quality but needs fair appraisal. PRP with team elements is likely best.', 6)],
  evaluate=[('Financial rewards are the most effective way to motivate employees.', ['Taylor: workers respond to pay', 'commission and PRP link reward to effort', 'meet basic needs'],
             ['Herzberg: pay is a hygiene factor', 'Pink: creative work needs autonomy, mastery, purpose', 'can encourage unethical behaviour (Wells Fargo)', 'costly'], 'Financial rewards are necessary and effective for some routine and sales jobs, but sustained motivation usually requires non-financial rewards as well.')],
  )

S('ch08-st4', concepts=('change', 'creativity'),
  terms=[('job enrichment', 'giving employees more challenging tasks and greater responsibility, often for a complete unit of work, to increase motivation'),
         ('job rotation', 'moving employees between different tasks or jobs at the same level of skill to increase variety'),
         ('job enlargement', 'increasing the number of tasks of a similar level in a job (horizontal loading)'),
         ('empowerment', 'giving employees the authority and resources to make decisions about their own work'),
         ('teamwork', 'employees working together in groups towards shared goals, sharing skills and responsibilities')],
  facts=[('Allowing a worker to build a complete product rather than one component is an example of:', 'job enrichment', ['job rotation', 'piece rate', 'delayering'], 'A complete unit of work adds responsibility and meaning.'),
         ('Moving a supermarket employee between the checkout, stocking shelves and the customer service desk is an example of:', 'job rotation', ['job enrichment', 'empowerment', 'commission'], 'Variety at the same skill level.'),
         ('Which motivation theorist most directly supports job enrichment?', 'Herzberg', ['Taylor', 'Fayol', 'Adams'], 'Enrichment provides motivators.')],
  why=[('Explain why job enrichment can increase motivation.', 'It provides Herzberg\'s motivators – responsibility, achievement, recognition and more meaningful work – and helps meet esteem and self-actualisation needs.'),
       ('Explain why empowerment can improve customer service.', 'Front-line staff can solve customers\' problems immediately without referring to managers, making service faster and more responsive.'),
       ('Explain why job rotation may not motivate employees in the long term.', 'Moving between several equally simple tasks adds variety but not responsibility or challenge; employees may see it as "more boring jobs" rather than enrichment.')],
  contrast=[('job enrichment', 'job enlargement', 'Job enrichment adds responsibility and more challenging tasks (vertical loading); job enlargement adds more tasks at the same level (horizontal loading).')],
  misc=[('Non-financial rewards cost the business nothing.', 'Training, restructuring jobs, empowerment and teamwork require time, management effort and often money.')],
  cases=[('Ritz-Carlton\'s $2,000 rule', 'Ritz-Carlton hotels have allowed every employee to spend up to $2,000 per guest to resolve a problem without asking a manager.', 'empowerment', 'trusting staff to act improves customer satisfaction and gives employees responsibility'),
         ('Volvo\'s Kalmar plant', 'In the 1970s Volvo\'s Kalmar plant in Sweden replaced the assembly line with teams that each built large sections of a car.', 'job enrichment and teamwork', 'complete units of work and team responsibility aimed to reduce boredom and absenteeism'),
         ('Toyota\'s quality circles', 'Toyota production workers meet in small teams to suggest improvements; the company receives hundreds of thousands of suggestions a year.', 'teamwork and empowerment', 'involving workers in problem-solving increases motivation and continuous improvement')],
  apply=[('A bank wants to motivate its experienced customer advisers without raising pay. Suggest two non-financial rewards and explain how each could help.', 'Empowerment to approve small loans or resolve complaints (responsibility, faster service); job enrichment through mentoring new staff or managing client portfolios (recognition, achievement); teamworking with shared targets.', 4)],
  evaluate=[('Non-financial rewards are more effective than financial rewards in motivating employees.', ['meet higher-level needs', 'long-lasting motivation (Herzberg, Pink)', 'lower cost than pay rises'],
             ['employees need adequate pay first', 'some workers prefer money', 'job enrichment is not possible in all jobs', 'empowerment needs skills and trust'], 'Non-financial rewards are more effective once pay is fair; the best approach combines both and fits the job and workforce.')],
  )


# =============================================================================================
# ch09 Units 2.5-2.7 Culture, employee relations and communication
# =============================================================================================
S('ch09-st1', concepts=('change', 'creativity'),
  terms=[('organizational culture', 'the attitudes, values, beliefs and norms shared by people in an organization that shape how they behave'),
         ('Handy\'s cultures', 'Charles Handy\'s four types of organizational culture: power, role, task and person'),
         ('power culture', 'a culture in which power is concentrated in a few individuals at the centre, with decisions made quickly by them'),
         ('role culture', 'a bureaucratic culture based on rules, procedures and clearly defined job roles'),
         ('task culture', 'a culture focused on getting projects done, with teams formed around tasks and power based on expertise'),
         ('person culture', 'a culture in which individuals see themselves as more important than the organization, common in professional partnerships'),
         ('culture clash', 'conflict that arises when people or organizations with different cultures work together, for example after a merger')],
  facts=[('Which of Handy\'s cultures is most associated with project teams and expertise?', 'Task culture', ['Power culture', 'Role culture', 'Person culture'], 'Teams form around tasks.'),
         ('A government civil service with detailed rules and job descriptions is most likely to have a:', 'role culture', ['task culture', 'person culture', 'power culture'], 'Bureaucratic rules and procedures.'),
         ('The failure of the Daimler-Chrysler merger is often blamed on:', 'a culture clash', ['economies of scale', 'too much profit', 'too few employees'], 'German and American management cultures conflicted.')],
  why=[('Explain why culture clashes often occur after mergers and acquisitions.', 'The two organizations have different values, decision-making styles and ways of working; employees may resist change, leading to conflict, low morale and loss of staff.'),
       ('Explain why organizational culture may need to change as a business grows.', 'A founder-led power culture that suits a small start-up may become too slow and centralised; growth requires more formal roles, delegation and systems.'),
       ('Explain why a strong organizational culture can be a source of competitive advantage.', 'Shared values guide behaviour without constant supervision, improve motivation and customer service and are difficult for rivals to copy.')],
  contrast=[('a power culture', 'a role culture', 'In a power culture decisions are made by a few powerful individuals quickly; in a role culture decisions follow rules and procedures based on job positions.')],
  misc=[('Organizational culture can be changed quickly by issuing a new mission statement.', 'Culture is deeply embedded in values and behaviours; changing it requires sustained leadership, new systems, recruitment and time.')],
  cases=[('Uber\'s culture change after 2017', 'After reports of a toxic workplace culture, Uber\'s founder Travis Kalanick resigned in 2017 and new CEO Dara Khosrowshahi introduced new cultural norms such as "We do the right thing. Period."', 'changing organizational culture', 'new leadership and values were used to repair an aggressive culture that had damaged reputation'),
         ('Netflix\'s culture of "freedom and responsibility"', 'Netflix\'s culture memo emphasises freedom and responsibility, candid feedback and high performance, with few formal rules on expenses or holidays.', 'organizational culture', 'a distinctive culture shapes recruitment and behaviour and supports rapid innovation'),
         ('Amazon and Whole Foods', 'After Amazon acquired Whole Foods for $13.7 bn in 2017, some Whole Foods staff complained about new data-driven inventory systems replacing local store autonomy.', 'culture clash during growth', 'differences in culture between a decentralised grocer and a data-driven tech firm caused tension')],
  apply=[('A family-owned design agency of 15 people, run by its founder, is acquired by a large advertising group with detailed procedures. Using Handy\'s cultures, explain one likely problem and how it could be reduced.', 'The agency has a power/task culture; the group has a role culture; staff may resist rules and slower decisions, causing loss of creative staff. Reduce by keeping some autonomy, communicating changes and integrating gradually.', 4)],
  evaluate=[('Culture clashes are the main reason why mergers and acquisitions fail.', ['examples: DaimlerChrysler, AOL-Time Warner', 'loss of key staff', 'integration failure'],
             ['overpaying for acquisitions', 'poor strategic fit', 'economic conditions', 'regulatory problems'], 'Culture clashes are a major cause of failure, but they often combine with overpayment and poor strategic fit; careful cultural due diligence can reduce the risk.')],
  )

S('ch09-st2', concepts=('ethics', 'change'),
  terms=[('trade union', 'an organization of workers that represents members\' interests in negotiations with employers on pay, conditions and rights'),
         ('collective bargaining', 'negotiation between employers and trade unions on behalf of employees about pay and conditions'),
         ('industrial action', 'measures taken by employees to put pressure on employers, such as strikes, work-to-rule, go-slows and overtime bans'),
         ('arbitration', 'a method of resolving disputes in which an independent third party considers both sides and makes a decision (binding or non-binding)'),
         ('conciliation', 'a method of resolving disputes in which an independent third party helps the two sides to reach their own agreement'),
         ('work-to-rule', 'industrial action in which employees do only the minimum required by their contracts and follow all rules precisely, slowing work')],
  facts=[('Which of the following is a method of industrial action used by employees?', 'Work-to-rule', ['Lockout', 'Closure threat', 'Arbitration'], 'Lockouts are an employer tactic.'),
         ('In arbitration, the independent third party:', 'listens to both sides and makes a decision', ['only helps the parties to talk', 'represents the employer', 'always sides with the union'], 'Arbitrators decide; conciliators facilitate.'),
         ('The 2023 strike by the Writers Guild of America lasted about:', '148 days', ['3 days', '2 years', '10 days'], 'Writers won protections including on AI use.')],
  why=[('Explain why employees join trade unions.', 'Collective bargaining gives them more power than negotiating individually, helping to secure better pay, conditions and job security, and unions provide legal support and representation.'),
       ('Explain why strikes can be costly for both employers and employees.', 'Employers lose output, revenue and reputation; employees lose wages during the strike and may face job losses if the business is damaged.'),
       ('Explain why employers may prefer conciliation to arbitration.', 'Conciliation lets both sides reach their own agreement, which they are more likely to accept, rather than having a decision imposed by an arbitrator.')],
  contrast=[('conciliation', 'arbitration', 'In conciliation an independent third party helps both sides reach their own agreement; in arbitration the third party hears both sides and makes a decision for them.')],
  misc=[('Trade unions are only interested in higher pay.', 'Unions also negotiate on working conditions, health and safety, job security, training, discrimination and the introduction of new technology.')],
  cases=[('the UAW strike in 2023', 'The United Auto Workers held "stand-up" strikes at selected plants of Ford, GM and Stellantis for about six weeks in 2023, winning wage increases of around 25% over four and a half years.', 'collective bargaining and industrial action', 'targeted strikes increased pressure on employers while limiting strikers\' losses'),
         ('the Writers Guild of America strike in 2023', 'Hollywood writers struck for about 148 days in 2023, winning higher pay, residuals from streaming and limits on the use of AI in writing.', 'industrial action', 'collective action secured protections over technological change'),
         ('ACAS in the UK', 'The UK\'s Advisory, Conciliation and Arbitration Service (ACAS) helps resolve thousands of workplace disputes each year through conciliation.', 'methods of resolving disputes', 'independent third parties help avoid costly strikes and tribunal cases')],
  apply=[('Nurses at a private hospital threaten to strike over pay. Identify two methods management could use to resolve the dispute and explain which is more likely to preserve good employee relations.', 'Negotiation/collective bargaining, conciliation, arbitration, offering non-pay improvements. Conciliation (or collective bargaining) preserves relations better because both sides own the agreement.', 4)],
  evaluate=[('Trade unions benefit businesses as well as employees.', ['single channel of communication', 'help manage change and reduce conflict', 'improve training and productivity'],
             ['raise labour costs', 'industrial action disrupts output', 'may resist change and flexibility'], 'Unions can benefit firms where relations are cooperative; the outcome depends on management\'s approach and the union\'s willingness to work in partnership.')],
  )

S('ch09-st3', concepts=('change', 'creativity'),
  terms=[('formal communication', 'communication through official channels set by the organization, such as reports, memos, meetings and the intranet'),
         ('informal communication', 'unofficial communication between employees, such as conversations and messaging, often called the grapevine'),
         ('barriers to communication', 'factors that prevent a message being received and understood as intended, such as jargon, noise, language, culture, distance and information overload'),
         ('information overload', 'a situation in which a person receives too much information to process effectively'),
         ('feedback', 'the response from the receiver showing whether the message has been understood')],
  facts=[('Which of the following is an example of informal communication?', 'Chat between colleagues at lunch', ['The annual report', 'A formal disciplinary letter', 'Board meeting minutes'], 'Unofficial channels.'),
         ('Using technical jargon with customers is an example of:', 'a barrier to communication', ['formal communication', 'feedback', 'an informal channel'], 'Jargon may not be understood.'),
         ('Which communication method is most appropriate for informing all employees of a new safety procedure?', 'A written policy on the intranet supported by a team briefing', ['A rumour', 'A text to one manager', 'A social media post'], 'Written record plus explanation.')],
  why=[('Explain why effective communication is important in a business.', 'It ensures employees understand objectives and instructions, coordinates functions, improves motivation and reduces errors and conflict.'),
       ('Explain why the grapevine can be harmful to a business.', 'Informal rumours may spread inaccurate information, especially during change, creating fear, low morale and resistance.'),
       ('Explain why cultural differences can be a barrier to communication in multinational companies.', 'Languages, gestures, attitudes to hierarchy and directness differ, so messages may be misunderstood or cause offence.')],
  contrast=[('formal communication', 'informal communication', 'Formal communication follows official channels and is recorded (reports, meetings); informal communication is unofficial and spontaneous (conversations, grapevine).')],
  misc=[('Sending more emails always improves communication.', 'Excessive messages cause information overload, so important information may be missed.')],
  cases=[('P&O Ferries\' mass dismissal by video', 'In March 2022 P&O Ferries dismissed about 800 seafarers with immediate effect in a pre-recorded video message, without consulting unions.', 'formal communication and its consequences', 'the method of communication caused public outrage, legal investigations and lasting reputational damage'),
         ('Slack and internal communication', 'Many firms adopted Slack and Microsoft Teams for internal messaging; Microsoft Teams reported over 300 million monthly active users in 2023.', 'methods of communication', 'instant messaging speeds communication but can cause information overload and constant interruptions')],
  apply=[('A manufacturer is closing one of its three factories. Recommend how management should communicate the decision to employees, explaining two barriers it should try to avoid.', 'Face-to-face meetings led by senior managers, followed by written details and Q&A sessions; avoid rumours spreading first (grapevine), jargon, and emotional barriers such as fear; provide feedback channels.', 4)],
  evaluate=[('Digital communication tools have improved communication within businesses.', ['speed and reach across locations', 'enables remote and hybrid work', 'searchable records'],
             ['information overload', 'misunderstanding without tone or body language', 'blurring work-life boundaries', 'security risks'], 'Digital tools have improved speed and reach, but face-to-face communication remains important for complex or sensitive messages.')],
  )


# =============================================================================================
# ch10 Units 3.1-3.3 Finance, sources of finance, costs and revenues
# =============================================================================================
CAPEX = ['a new delivery van', 'an extension to the factory', 'ten new computers for the office', 'the purchase of a patent',
         'a new bottling machine', 'land for a new warehouse', 'a commercial oven for the bakery', 'solar panels for the roof']
REVEX = ['monthly wages of shop staff', 'the electricity bill', 'raw materials for this month\'s production', 'an online advertising campaign',
         'rent for the office', 'repairs to a broken window', 'insurance premiums', 'fuel for the delivery vans', 'interest on a bank loan']


@calc('ch10-st1', 'C1', (1, 3), 'mcq')
def capex_mcq(rng, slot):
    f_ = firm(rng)
    if rng.random() < 0.5:
        a = rng.choice(CAPEX)
        w = rng.sample(REVEX, 3)
        return mcq(rng, f'Which of the following spending by {f_} is capital expenditure?', cap(a), [cap(x) for x in w], f'{cap(a)} is an asset used for more than one year.')
    a = rng.choice(REVEX)
    w = rng.sample(CAPEX, 3)
    return mcq(rng, f'Which of the following spending by {f_} is revenue expenditure?', cap(a), [cap(x) for x in w], f'{cap(a)} is a day-to-day running cost.')


@calc('ch10-st1', 'C3', (1, 4))
def capex_classify(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    items = rng.sample([(x, 'capital') for x in CAPEX], 2) + rng.sample([(x, 'revenue') for x in REVEX], 3)
    rng.shuffle(items)
    vals = [rng.choice([8000, 12000, 18000, 25000, 40000]) if k == 'capital' else rng.choice([800, 1500, 2400, 3600, 5000]) for _, k in items]
    lst = '; '.join(f'{x} {m(v, c)}' for (x, _), v in zip(items, vals))
    capt = sum(v for (x, k), v in zip(items, vals) if k == 'capital')
    revt = sum(v for (x, k), v in zip(items, vals) if k == 'revenue')
    return dict(stem=f'Last month {f_} spent money on: {lst}. Classify each item as capital or revenue expenditure and calculate the total of each.',
                answer='Capital: ' + ', '.join(x for (x, k) in items if k == 'capital') + f' = {m(capt, c)}; revenue: ' + ', '.join(x for (x, k) in items if k == 'revenue') + f' = {m(revt, c)}.',
                markingKey=f'[2] for correct classification of all five items ([1] for four); [1] capital total {m(capt, c)}; [1] revenue total {m(revt, c)}. Capital expenditure buys fixed assets used for more than a year; revenue expenditure is day-to-day running costs.', marks=4)


S('ch10-st1', concepts=('change', 'sustainability'),
  terms=[('capital expenditure', 'spending on fixed (non-current) assets that are used by the business for more than one year, such as machinery, vehicles and buildings'),
         ('revenue expenditure', 'spending on the day-to-day running costs of a business, such as wages, rent, utilities and raw materials'),
         ('finance', 'the funds a business needs to start, run and grow, and the business function that manages them'),
         ('non-current assets', 'assets held by a business for more than twelve months, such as property, plant and equipment')],
  facts=[('Which of the following is revenue expenditure?', 'Paying the monthly electricity bill', ['Buying a new delivery van', 'Building a warehouse extension', 'Purchasing a patent'], 'Day-to-day running cost.'),
         ('Capital expenditure is recorded in the:', 'statement of financial position as non-current assets', ['statement of profit or loss as an expense in full', 'cash-flow forecast only', 'marketing plan'], 'Assets are capitalised and depreciated.'),
         ('Which source of finance is most suitable for capital expenditure on a new factory?', 'A long-term loan or share capital', ['A bank overdraft', 'Trade credit', 'Debt factoring'], 'Long-term assets need long-term finance.')],
  why=[('Explain why businesses need to distinguish between capital and revenue expenditure.', 'Capital expenditure is recorded as assets and spread over their life through depreciation, while revenue expenditure is an expense in the period; mixing them distorts profit and asset values and leads to wrong finance choices.'),
       ('Explain why capital expenditure should usually be financed by long-term sources.', 'The assets generate returns over many years, so matching them with long-term finance avoids pressure to repay short-term debts before the asset has generated cash.'),
       ('Explain why a business needs finance even if it is profitable.', 'Profitable businesses may still need cash for expansion, new assets, working capital as sales grow, and to cover timing gaps between paying suppliers and receiving payment from customers.')],
  contrast=[('capital expenditure', 'revenue expenditure', 'Capital expenditure buys assets used for more than a year (machinery, buildings); revenue expenditure pays for day-to-day running costs used up within the year (wages, rent, materials).')],
  misc=[('Repairing a broken machine is capital expenditure because it relates to a fixed asset.', 'Repairs that restore an asset to its original condition are revenue expenditure; only improvements or new assets are capital expenditure.')],
  cases=[('TSMC\'s new chip plants', 'Taiwanese chip maker TSMC planned capital expenditure of about $28-32 bn in 2024, mainly for new fabrication plants.', 'capital expenditure', 'huge investment in long-term assets is needed to stay ahead in advanced chip manufacturing'),
         ('airlines during Covid-19', 'In 2020 many airlines cut revenue expenditure such as staff costs through furlough schemes while delaying capital expenditure on new aircraft.', 'the difference between capital and revenue expenditure', 'day-to-day running costs were reduced immediately while long-term asset purchases were postponed')],
  apply=[('A café buys a coffee machine for $6,000, pays $2,500 in wages, $900 for coffee beans and $1,200 to refit the seating area. Classify each item and state where each appears in the final accounts.', 'Capital: coffee machine and refit (non-current assets in the statement of financial position, depreciated). Revenue: wages and beans (expenses in the statement of profit or loss).', 3)],
  evaluate=[('Businesses should cut capital expenditure during a recession.', ['preserves cash and reduces borrowing', 'demand is weak, so new capacity is not needed', 'reduces risk'],
             ['asset prices and interest rates may be low', 'investment prepares for recovery', 'competitors may gain an advantage', 'delaying maintenance raises future costs'], 'Cutting non-essential capital spending is prudent, but firms with strong finances may gain by investing counter-cyclically.')],
  )


@calc('ch10-st2', 'C3', (2, 4))
def loan_cost(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    P = rng.choice([20_000, 50_000, 80_000, 120_000])
    r = rng.choice([5, 6, 7, 8, 9])
    n = rng.choice([3, 4, 5])
    interest = P * r / 100 * n
    lease = round((P * (1 + r * n / 100) / (n * 12)) * rng.choice([0.9, 1.05, 1.15]) / 10) * 10
    lease_tot = lease * 12 * n
    return dict(stem=f'{f_} needs equipment costing {m(P, c)}. Option A: a bank loan at {r}% simple interest per year, repaid in full after {n} years. Option B: leasing the equipment for {m(lease, c)} a month for {n} years, after which it is returned. Calculate the total cost of each option and recommend one, giving one non-financial reason.',
                answer=f'A: {m(P, c)} + interest {m(interest, c)} = {m(P + interest, c)} (and the firm owns the asset). B: {m(lease, c)} × {12 * n} = {m(lease_tot, c)} (no ownership). {"Leasing is cheaper" if lease_tot < P + interest else "The loan is cheaper overall"}; non-financial: leasing includes maintenance/upgrades and preserves borrowing capacity, while the loan gives ownership and residual value.',
                markingKey=MK(f'Interest = {P:,} × {r}% × {n} = {interest:,.0f}; loan total {P + interest:,.0f}; lease total {lease:,} × {12 * n} = {lease_tot:,}.', 'both totals') + ' [R1] justified recommendation.', marks=4)


S('ch10-st2', concepts=('change', 'ethics'),
  terms=[('internal sources of finance', 'funds generated from within the business, such as retained profit, personal funds of owners and the sale of assets'),
         ('external sources of finance', 'funds obtained from outside the business, such as share capital, loans, overdrafts, trade credit, crowdfunding, leasing, microfinance and business angels'),
         ('retained profit', 'profit kept in the business after tax and dividends, used to fund investment'),
         ('share capital', 'money raised by a company by selling shares to investors'),
         ('overdraft', 'a facility that allows a business to withdraw more money than it has in its bank account, up to an agreed limit, for short-term needs'),
         ('trade credit', 'an arrangement in which suppliers allow a business to pay for goods some time after delivery, usually 30-90 days'),
         ('crowdfunding', 'raising finance from a large number of people, usually online, in exchange for rewards, shares or interest'),
         ('business angel', 'a wealthy individual who invests in small, high-potential businesses in return for a share of ownership and often provides advice')],
  facts=[('Which is an internal source of finance?', 'Retained profit', ['A bank loan', 'Share capital', 'Trade credit'], 'Generated within the business.'),
         ('Which source of finance is most suitable for a short-term cash shortage?', 'An overdraft', ['A mortgage', 'Share issue', 'Debentures'], 'Flexible short-term finance.'),
         ('Pebble\'s smartwatch raised over $10 m on Kickstarter in 2012. This is an example of:', 'crowdfunding', ['debt factoring', 'retained profit', 'microfinance'], 'Many small backers online.'),
         ('Which is a disadvantage of raising finance by issuing new shares?', 'Existing owners\' control may be diluted', ['Interest must be paid regardless of profit', 'It must be repaid within a year', 'It increases gearing'], 'New shareholders gain votes.')],
  why=[('Explain why retained profit is often the cheapest source of finance.', 'There are no interest payments, fees or loss of control; however, it has an opportunity cost because shareholders give up dividends.'),
       ('Explain why start-ups often find it difficult to obtain bank loans.', 'They lack a trading record, collateral and proven cash flows, so banks see them as high risk.'),
       ('Explain why a business might choose leasing rather than buying equipment.', 'Leasing avoids a large up-front payment, preserves cash and credit lines, often includes maintenance and allows regular upgrades, although the total cost may be higher.'),
       ('Explain why the appropriateness of a source of finance depends on its purpose.', 'Long-term assets should be financed by long-term sources (loans, shares), while short-term needs such as working capital suit overdrafts or trade credit; mismatching creates repayment pressure.')],
  contrast=[('share capital', 'loan capital', 'Share capital gives investors ownership and possible dividends but does not have to be repaid; loan capital must be repaid with interest but does not dilute ownership.'),
            ('an overdraft', 'a bank loan', 'An overdraft is a flexible short-term facility where interest is paid only on the amount used; a bank loan is a fixed amount for a set period, repaid in instalments.')],
  misc=[('Retained profit is free finance.', 'It has an opportunity cost: the money could have been paid to shareholders as dividends or invested elsewhere.')],
  cases=[('Pebble on Kickstarter', 'Pebble raised over $10 m from about 69,000 backers on Kickstarter in 2012, then over $20 m in 2015, but was sold to Fitbit in 2016 after financial difficulties.', 'crowdfunding as a source of finance', 'crowdfunding tested demand and raised funds, but did not guarantee long-term financial stability'),
         ('Saudi Aramco\'s IPO', 'Saudi Aramco raised about $25.6 bn in its December 2019 IPO, then the largest ever.', 'share capital', 'selling shares raised huge finance without debt, while the government kept control'),
         ('Kiva microloans', 'Kiva, a non-profit platform, has facilitated over $2 bn in small loans from individuals to entrepreneurs in more than 80 countries.', 'microfinance and crowdfunding', 'small loans give finance to people excluded from formal banks')],
  apply=[('A small bakery needs $15,000 to buy a new oven and $3,000 to cover a temporary cash shortfall in January. Recommend a suitable source of finance for each need.', 'Oven: medium-term bank loan, leasing or retained profit (long-life asset). Cash shortfall: overdraft or trade credit (short-term, flexible).', 4)],
  evaluate=[('Share capital is the best source of finance for a growing company.', ['no repayment or interest', 'large amounts available', 'lower gearing'],
             ['dilution of control', 'dividend expectations', 'cost and time of issue', 'risk of takeover'], 'Share capital suits large, risky long-term investments, but debt or retained profit may be cheaper and preserve control for stable businesses.')],
  )


@calc('ch10-st3', 'C3', (1, 5))
def cost_revenue(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    rent = rng.choice([1500, 2500, 4000, 6000])
    sal = rng.choice([3000, 5000, 8000])
    vc = rng.choice([2, 3.5, 4, 6, 8, 12])
    price = vc * rng.choice([2, 2.5, 3])
    q = rng.choice([800, 1000, 1500, 2500, 4000])
    fc = rent + sal
    tc = fc + vc * q
    tr = price * q
    pr = tr - tc
    frame = rng.choice([f'{f_} pays monthly rent of {m(rent, c)} and management salaries of {m(sal, c)}. Each unit costs {m(vc, c)} in materials and packaging, and sells for {m(price, c)}.',
                        f'At {f_}, fixed costs each month are rent ({m(rent, c)}) and salaried staff ({m(sal, c)}); direct costs are {m(vc, c)} per unit and the selling price is {m(price, c)}.'])
    if slot.d <= 2:
        return dict(stem=frame + f' In May it sold {q:,} units. Calculate total cost and total revenue.',
                    answer=f'TC = {m(fc, c)} + {m(vc, c)} × {q:,} = {m(tc, c)}; TR = {m(price, c)} × {q:,} = {m(tr, c)}',
                    markingKey=MK(f'TC = FC + VC × Q = {tc:,.0f}; TR = P × Q = {tr:,.0f}.', 'both values'), marks=2)
    if slot.d == 3:
        return dict(stem=frame + f' In May it sold {q:,} units. Calculate the profit or loss, and classify rent and materials as fixed or variable costs.',
                    answer=f'Profit = {m(tr, c)} − {m(tc, c)} = {m(pr, c)}. Rent: fixed (does not change with output); materials: variable (change with output).',
                    markingKey=MK(f'TR {tr:,.0f} − TC {tc:,.0f} = {pr:,.0f}.', m(pr, c)) + ' [1] classification.', marks=3)
    q2 = int(q * 1.2)
    pr2 = price * 0.9 * q2 - (fc + vc * q2)
    return dict(stem=frame + f' In May it sold {q:,} units. The manager believes that a 10% price cut would raise sales by 20%. Calculate profit before and after the price cut and comment on whether it should go ahead.',
                answer=f'Before: {m(pr, c)}. After: TR = {m(price * 0.9, c)} × {q2:,} = {m(price * 0.9 * q2, c)}; TC = {m(fc + vc * q2, c)}; profit = {m(pr2, c)}. {"Profit rises, so the price cut appears worthwhile" if pr2 > pr else "Profit falls, so the price cut is not worthwhile on these figures"}, though the sales forecast may be unreliable and rivals may respond.',
                markingKey=MK(f'Before {pr:,.0f}; after: {price * 0.9:.2f} × {q2:,} − ({fc:,} + {vc} × {q2:,}) = {pr2:,.0f}.', 'both profits') + ' [R1] comment.', marks=4 if slot.d == 4 else 6)


S('ch10-st3', concepts=('change', 'creativity'),
  terms=[('fixed costs', 'costs that do not change with the level of output in the short run, such as rent, insurance and salaries'),
         ('variable costs', 'costs that change directly with the level of output, such as raw materials and packaging'),
         ('direct costs', 'costs that can be clearly attributed to the production of a particular product or service, such as its raw materials'),
         ('indirect costs (overheads)', 'costs that cannot be attributed to a single product, such as rent of head office, administration and marketing of the whole firm'),
         ('total revenue', 'the income a business receives from selling its output: price × quantity sold'),
         ('revenue streams', 'the different sources of revenue of a business, such as product sales, subscriptions, advertising, licensing, commissions and leasing')],
  facts=[('Which of the following is a variable cost for a car manufacturer?', 'Tyres fitted to each car', ['Factory rent', 'Insurance of the factory', 'Salaries of directors'], 'Rises with each car produced.'),
         ('If price is $8 and 2,500 units are sold, total revenue is:', '$20,000', ['$2,508', '$312.50', '$10,000'], 'TR = 8 × 2,500.'),
         ('Spotify earns money from premium subscriptions and from advertising. These are examples of:', 'revenue streams', ['fixed costs', 'capital expenditure', 'variable costs'], 'Different sources of revenue.'),
         ('Head-office administration costs shared by several product lines are:', 'indirect costs', ['direct costs', 'variable costs', 'capital expenditure'], 'Not attributable to one product.')],
  why=[('Explain why it is useful for a business to classify costs as fixed and variable.', 'It allows the business to calculate contribution and break-even, predict how costs change with output and make pricing and production decisions.'),
       ('Explain why businesses try to develop several revenue streams.', 'Several sources of income spread risk, increase total revenue and use existing assets and customers more fully (e.g. subscriptions plus advertising).'),
       ('Explain why fixed costs per unit fall as output rises.', 'Total fixed costs stay the same, so spreading them over more units reduces the fixed cost per unit, lowering average cost.')],
  contrast=[('fixed costs', 'variable costs', 'Fixed costs do not change with output in the short run (rent, salaries); variable costs change directly with output (materials, packaging).'),
            ('direct costs', 'indirect costs', 'Direct costs can be traced to a specific product (its materials); indirect costs are shared overheads that cannot be traced to one product (head-office rent).')],
  misc=[('Fixed costs never change.', 'They do not change with output in the short run, but they can change over time (rent increases) or when capacity changes (a new factory).')],
  cases=[('Netflix\'s ad tier and password-sharing fees', 'Netflix introduced a cheaper ad-supported plan in 2022 and began charging for password sharing in 2023, adding advertising revenue to subscriptions.', 'revenue streams', 'adding new revenue sources increases income from the same content library'),
         ('airline fixed costs', 'Airlines have high fixed costs (aircraft leases, maintenance, staff), so they use dynamic pricing to fill seats; an empty seat earns nothing but costs almost the same.', 'fixed and variable costs', 'high fixed costs mean each extra passenger adds a lot to profit once variable costs are covered')],
  apply=[('A streaming service pays $40 m a year for content licences and $2 per subscriber per month for data and customer service. Classify these costs and explain why gaining more subscribers is especially profitable.', 'Licences: fixed (do not depend on subscribers); $2: variable. With high fixed costs, each extra subscriber adds revenue well above the variable cost, so profit rises quickly once fixed costs are covered.', 3)],
  evaluate=[('Reducing fixed costs is the best way for a business to increase profit.', ['lowers break-even point', 'reduces risk in downturns', 'outsourcing turns fixed into variable costs'],
             ['cutting fixed costs may reduce capacity and quality', 'raising revenue may be more effective', 'variable cost savings matter at high output'], 'The best approach depends on the cost structure: high fixed-cost firms gain most from higher volume, while others may benefit from cost cuts.')],
  )


# =============================================================================================
# ch11 Unit 3.4 Final accounts
# =============================================================================================
S('ch11-st1', concepts=('ethics', 'change'),
  terms=[('final accounts', 'the financial statements prepared at the end of the financial year: the statement of profit or loss and the statement of financial position'),
         ('stakeholders\' use of accounts', 'the use of financial statements by shareholders, managers, employees, lenders, suppliers, government and competitors to assess performance and make decisions'),
         ('ethical accounting', 'preparing accounts honestly and accurately according to accounting standards, without manipulation to mislead stakeholders'),
         ('window dressing', 'manipulating accounts to make a business\'s financial position look better than it is'),
         ('auditor', 'an independent accountant who checks that a company\'s accounts give a true and fair view')],
  facts=[('Which stakeholder would use final accounts mainly to decide whether to lend to a business?', 'A bank', ['A customer', 'A local resident', 'A pressure group'], 'Lenders assess ability to repay.'),
         ('The German payments company that collapsed in 2020 after admitting that €1.9 bn of cash did not exist was:', 'Wirecard', ['SAP', 'Siemens', 'Adidas'], 'A major accounting fraud.'),
         ('Which principle of ethical accounting requires that accounts give a true and fair view?', 'Integrity', ['Secrecy', 'Profit maximisation', 'Window dressing'], 'Honesty and accuracy.')],
  why=[('Explain why shareholders are interested in a company\'s final accounts.', 'They show profitability, dividends paid and the value of assets, helping shareholders judge management performance and decide whether to buy, hold or sell shares.'),
       ('Explain why employees and trade unions may study a company\'s accounts.', 'Profits and cash indicate whether the firm can afford pay rises and whether jobs are secure.'),
       ('Explain why ethical accounting is important.', 'Stakeholders rely on accurate accounts to make decisions; manipulation misleads investors, lenders and employees and can lead to collapses, legal penalties and loss of trust (Enron, Wirecard).')],
  contrast=[('internal users of accounts', 'external users of accounts', 'Internal users (managers, employees) use accounts to plan and control the business; external users (shareholders, lenders, suppliers, government) use them to judge performance, risk and tax liability.')],
  misc=[('Final accounts are only useful to the owners of a business.', 'Many stakeholders use them: lenders, suppliers, employees, governments (tax), competitors and potential investors.')],
  cases=[('Wirecard\'s collapse', 'In June 2020 Wirecard admitted that €1.9 bn of cash supposedly held in Asian bank accounts probably did not exist and filed for insolvency.', 'principles of ethical accounting', 'fraudulent accounts misled investors, auditors and regulators, destroying a company once worth over €20 bn'),
         ('Enron', 'Energy firm Enron hid billions of dollars of debt in off-balance-sheet entities and collapsed in 2001; its auditor Arthur Andersen also collapsed.', 'the importance of reliable accounts', 'manipulated accounts gave a false picture to stakeholders and led to new rules (Sarbanes-Oxley Act, 2002)'),
         ('Carillion\'s collapse', 'UK construction firm Carillion went into liquidation in January 2018 with debts of about £7 bn, months after its accounts showed a healthy position.', 'stakeholders\' use of accounts', 'accounts that hid problems left suppliers, employees and pension scheme members exposed')],
  apply=[('A supplier is deciding whether to give a new customer 60 days\' trade credit. Explain what information it would look for in the customer\'s final accounts.', 'Liquidity (current and acid-test ratios, cash balance), level of current liabilities and creditor days, profitability trend, and whether the statement of financial position shows heavy debt.', 3)],
  evaluate=[('Published accounts give stakeholders all the information they need to judge a business.', ['standardised and audited', 'show profit, assets and liabilities', 'allow comparison over time'],
             ['historical, not future-oriented', 'can be window dressed', 'exclude non-financial information (morale, brand, ESG)', 'summarised data hides detail'], 'Accounts are essential but not sufficient; stakeholders should also consider forecasts, non-financial information and the reliability of the accounts.')],
  )


@calc('ch11-st2', 'C3', (2, 5))
def pl_statement(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    sales = rng.choice([400, 600, 850, 1200, 2000]) * 1000
    cogs = int(sales * rng.choice([0.4, 0.5, 0.55, 0.6]))
    exp_ = int(sales * rng.choice([0.15, 0.2, 0.25]))
    interest = rng.choice([10, 20, 30]) * 1000
    tax_r = rng.choice([20, 25, 30])
    gp = sales - cogs
    pbit = gp - exp_
    pbt = pbit - interest
    tax = pbt * tax_r / 100
    pat = pbt - tax
    div = round(pat * rng.choice([0.3, 0.4, 0.5]), -3)
    ret = pat - div
    frame = rng.choice([f'For the year ended 31 December, {f_} recorded: sales revenue {m(sales, c)}; cost of sales {m(cogs, c)}; expenses {m(exp_, c)}; interest {m(interest, c)}; corporation tax at {tax_r}% of profit before tax; dividends {m(div, c)}.',
                        f'Financial data for {f_} (year to 31 March): revenue {m(sales, c)}, cost of goods sold {m(cogs, c)}, overheads {m(exp_, c)}, interest paid {m(interest, c)}; tax rate {tax_r}%; dividends declared {m(div, c)}.'])
    if slot.d <= 3:
        return dict(stem=frame + ' Calculate gross profit and profit before interest and tax.',
                    answer=f'Gross profit = {m(gp, c)}; profit before interest and tax = {m(pbit, c)}',
                    markingKey=MK(f'GP = revenue − cost of sales = {gp:,}; PBIT = GP − expenses = {pbit:,}.', 'both values'), marks=3)
    return dict(stem=frame + ' Construct a statement of profit or loss, showing gross profit, profit before interest and tax, profit before tax, profit for the period and retained profit.',
                answer=f'Revenue {m(sales, c)}; cost of sales ({m(cogs, c)}); gross profit {m(gp, c)}; expenses ({m(exp_, c)}); PBIT {m(pbit, c)}; interest ({m(interest, c)}); profit before tax {m(pbt, c)}; tax ({m(tax, c)}); profit for the period {m(pat, c)}; dividends ({m(div, c)}); retained profit {m(ret, c)}.',
                markingKey=f'[1] gross profit {m(gp, c)}; [1] PBIT {m(pbit, c)}; [1] PBT {m(pbt, c)}; [1] tax {m(tax, c)} and profit for the period {m(pat, c)}; [1] retained profit {m(ret, c)}; [1] correct format/labels. Apply OFR.', marks=6)


@calc('ch11-st2', 'C3', (2, 5))
def sofp(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    ppe = rng.choice([300, 450, 600, 800]) * 1000
    inv = rng.choice([40, 60, 90]) * 1000
    debt = rng.choice([30, 50, 70]) * 1000
    cash = rng.choice([15, 25, 40]) * 1000
    cred = rng.choice([35, 50, 65]) * 1000
    od = rng.choice([0, 10, 20]) * 1000
    ltl = rng.choice([100, 150, 250]) * 1000
    sc = rng.choice([200, 300]) * 1000
    ca = inv + debt + cash
    cl = cred + od
    na = ppe + ca - cl - ltl
    re = na - sc
    if re < 0:
        return None
    return dict(stem=f'The following balances relate to {f_} at the end of the year: property, plant and equipment {m(ppe, c)}; inventories {m(inv, c)}; trade receivables (debtors) {m(debt, c)}; cash {m(cash, c)}; trade payables (creditors) {m(cred, c)}; overdraft {m(od, c)}; long-term loan {m(ltl, c)}; share capital {m(sc, c)}; retained earnings – to be calculated. Calculate current assets, current liabilities, net assets and retained earnings, and construct the statement of financial position.',
                answer=f'Current assets = {m(ca, c)}; current liabilities = {m(cl, c)}; net current assets = {m(ca - cl, c)}; total assets less current liabilities = {m(ppe + ca - cl, c)}; net assets = {m(na, c)}; equity: share capital {m(sc, c)} + retained earnings {m(re, c)} = {m(na, c)}.',
                markingKey=f'[1] CA {m(ca, c)}; [1] CL {m(cl, c)}; [1] net assets {m(na, c)}; [1] retained earnings {m(re, c)} (balancing figure); [2] correct layout with non-current assets, current assets, current liabilities, non-current liabilities and equity. Apply OFR.', marks=6)


S('ch11-st2', concepts=('ethics', 'change'),
  terms=[('statement of profit or loss', 'a financial statement showing a business\'s revenue, costs and profit (or loss) over a period, usually a year'),
         ('statement of financial position', 'a financial statement showing the assets, liabilities and equity of a business at a particular date'),
         ('gross profit', 'sales revenue minus cost of sales'),
         ('profit before interest and tax', 'gross profit minus expenses (overheads)'),
         ('retained profit', 'profit for the period after tax and dividends, kept in the business'),
         ('current assets', 'assets expected to be converted into cash within twelve months, such as inventories, trade receivables and cash'),
         ('current liabilities', 'debts that must be paid within twelve months, such as trade payables and overdrafts'),
         ('equity', 'the value of the business belonging to its owners: share capital plus retained earnings')],
  facts=[('Gross profit is calculated as:', 'sales revenue − cost of sales', ['sales revenue − expenses', 'profit before tax − tax', 'assets − liabilities'], 'Before overheads.'),
         ('Which item appears under current liabilities?', 'Trade payables', ['Inventories', 'Long-term loans', 'Share capital'], 'Owed to suppliers within a year.'),
         ('In the statement of financial position, net assets equal:', 'total equity', ['gross profit', 'sales revenue', 'current liabilities'], 'Assets − liabilities = equity.'),
         ('Which item would reduce profit before tax but not gross profit?', 'Interest on loans', ['Cost of raw materials sold', 'Sales returns', 'Purchases of stock'], 'Interest is deducted after PBIT.')],
  why=[('Explain why a business can have high gross profit but a low profit for the period.', 'High expenses (overheads such as rent, salaries, marketing), interest and tax are deducted after gross profit, so poor control of overheads or high borrowing reduces final profit.'),
       ('Explain why the statement of financial position is described as a "snapshot".', 'It shows assets, liabilities and equity at one point in time, which can change the next day, unlike the statement of profit or loss which covers a period.'),
       ('Explain why retained profit is important for a company\'s future.', 'It adds to equity and provides internal finance for investment without borrowing or issuing shares.')],
  contrast=[('the statement of profit or loss', 'the statement of financial position', 'The statement of profit or loss shows income, costs and profit over a period; the statement of financial position shows assets, liabilities and equity at a point in time.'),
            ('gross profit', 'profit for the period', 'Gross profit is revenue minus cost of sales; profit for the period is what remains after deducting expenses, interest and tax.')],
  misc=[('A large profit in the statement of profit or loss means the business has a lot of cash.', 'Profit is not cash: sales on credit, inventory purchases and capital spending mean a profitable business can have little cash.')],
  cases=[('Apple\'s 2024 annual results', 'In its 2024 financial year Apple reported revenue of about $391 bn and gross margin of about 46%.', 'the statement of profit or loss', 'high gross profit reflects premium pricing over the cost of components and manufacturing'),
         ('Amazon\'s thin margins', 'Amazon\'s retail business has historically had low profit margins, with most operating profit coming from Amazon Web Services.', 'interpreting final accounts', 'segment information in the accounts shows which activities generate profit')],
  apply=[('A firm has sales revenue of $500,000, cost of sales of $300,000, expenses of $120,000 and interest of $10,000. Calculate gross profit and profit before tax.', 'Gross profit = $200,000; PBIT = $80,000; profit before tax = $70,000.', 3)],
  evaluate=[('The statement of profit or loss is more useful to stakeholders than the statement of financial position.', ['shows performance and profitability', 'used to assess dividends and pay rises', 'trend over time'],
             ['SOFP shows liquidity, debts and solvency', 'lenders and suppliers need SOFP', 'both are needed for ratio analysis'], 'Different stakeholders need different statements; both are needed for a full picture.')],
  )


@calc('ch11-st3', 'C3', (1, 5))
def depreciation(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    asset = rng.choice(['a delivery van', 'a printing machine', 'a refrigerated truck', 'a CNC cutting machine', 'a fleet of laptops'])
    cost = rng.choice([24_000, 40_000, 60_000, 90_000, 150_000])
    res = int(cost * rng.choice([0.1, 0.15, 0.2, 0.25]))
    life = rng.choice([4, 5, 6, 8])
    dep = (cost - res) / life
    y = rng.randint(1, life - 1)
    nbv = cost - dep * y
    if slot.d <= 2:
        return dict(stem=f'{f_} buys {asset} for {m(cost, c)}. It expects to use it for {life} years and sell it for {m(res, c)} at the end. Using the straight-line method, calculate the annual depreciation charge.',
                    answer=m(dep, c), markingKey=MK(f'({cost:,} − {res:,}) / {life} = {dep:,.2f}.', m(dep, c)), marks=2)
    if slot.d == 3:
        return dict(stem=f'{f_} buys {asset} for {m(cost, c)} with an expected life of {life} years and residual value of {m(res, c)}. Using straight-line depreciation, calculate the annual depreciation and the net book value at the end of year {y}.',
                    answer=f'Annual depreciation = {m(dep, c)}; NBV after {y} years = {m(cost, c)} − {y} × {m(dep, c)} = {m(nbv, c)}',
                    markingKey=MK(f'Dep = {dep:,.2f}; NBV = {cost:,} − {y} × {dep:,.2f} = {nbv:,.2f}.', 'both values'), marks=3)
    units = rng.choice([100_000, 200_000, 250_000, 400_000])
    use = [int(units * x) for x in rng.choice([(0.3, 0.3, 0.2, 0.2), (0.4, 0.3, 0.2, 0.1), (0.25, 0.25, 0.25, 0.25), (0.35, 0.25, 0.25, 0.15)])]
    rate = (cost - res) / units
    deps = [u * rate for u in use]
    unit_word = 'km' if 'van' in asset or 'truck' in asset else 'units'
    return dict(stem=f'{f_} buys {asset} for {m(cost, c)}. Its residual value will be {m(res, c)} after a working life of {units:,} {unit_word}, expected to be used as follows: year 1 {use[0]:,}, year 2 {use[1]:,}, year 3 {use[2]:,}, year 4 {use[3]:,}. Using the units of production method, calculate the depreciation charge for each year and the net book value at the end of year 2. Explain one reason why this method may be more appropriate than straight-line for this asset.',
                answer=f'Rate = ({cost:,} − {res:,})/{units:,} = {m(rate, c)} per {unit_word[:-1] if unit_word == "units" else "km"}; charges: ' + ', '.join(m(d, c) for d in deps) + f'; NBV end of year 2 = {m(cost - deps[0] - deps[1], c)}. The method matches depreciation to actual use/wear, so cost is charged when the asset generates revenue.',
                markingKey=MK(f'Rate = {rate:.4f}; yearly charges = usage × rate; NBV2 = {cost:,} − {deps[0]:,.0f} − {deps[1]:,.0f} = {cost - deps[0] - deps[1]:,.0f}.', 'all charges and NBV') + ' [R1] reason.', marks=4 if slot.d == 4 else 6)


S('ch11-st3', concepts=('change', 'creativity', 'ethics'),
  terms=[('depreciation', 'the fall in the value of a non-current asset over time due to wear and tear, use or obsolescence, recorded as an expense'),
         ('straight-line depreciation', 'a method that charges an equal amount of depreciation each year: (cost − residual value) / useful life'),
         ('units of production method', 'a depreciation method that charges depreciation according to the asset\'s use: (cost − residual value) / total expected units × units used in the year'),
         ('net book value', 'the value of an asset in the accounts: its cost minus accumulated depreciation'),
         ('residual value', 'the expected value of an asset at the end of its useful life'),
         ('intangible assets', 'non-physical assets with value, such as brands, patents, copyrights, trademarks and goodwill'),
         ('goodwill', 'the amount by which the price paid for a business exceeds the fair value of its net assets, reflecting reputation, customer base and brand')],
  facts=[('A machine costs $50,000, has a residual value of $10,000 and a life of 5 years. Annual straight-line depreciation is:', '$8,000', ['$10,000', '$12,000', '$40,000'], '(50,000 − 10,000)/5.'),
         ('Which is an intangible asset?', 'A patent', ['A delivery van', 'Inventory', 'Cash at bank'], 'Non-physical but valuable.'),
         ('Depreciation appears in the statement of profit or loss as:', 'an expense', ['revenue', 'a current asset', 'share capital'], 'It reduces profit.')],
  why=[('Explain why businesses depreciate non-current assets.', 'Assets lose value through use and obsolescence; depreciation spreads the cost over the years the asset generates revenue (matching principle) and gives a realistic asset value.'),
       ('Explain why intangible assets are difficult to value.', 'They have no physical form and no active market price; their value depends on future earnings, which are uncertain, so valuations are subjective.'),
       ('Explain why depreciation does not involve a cash outflow.', 'The cash was paid when the asset was bought; depreciation is an accounting allocation of that cost over time.')],
  contrast=[('straight-line depreciation', 'the units of production method', 'Straight-line charges the same amount every year; units of production charges depreciation according to how much the asset is used each year.'),
            ('tangible assets', 'intangible assets', 'Tangible assets are physical (machinery, buildings); intangible assets are non-physical (patents, brands, goodwill).')],
  misc=[('Depreciation is money set aside in a bank account to replace an asset.', 'Depreciation is a non-cash expense that allocates the cost of an asset; it does not create a fund of cash.')],
  cases=[('Coca-Cola\'s brand value', 'Interbrand values the Coca-Cola brand at around $58 bn (2024), but most of this does not appear in Coca-Cola\'s statement of financial position because it was internally generated.', 'intangible assets', 'internally created brands are not usually recorded as assets, so accounts can understate a firm\'s value'),
         ('Microsoft\'s acquisition of Activision Blizzard', 'After paying about $69 bn for Activision Blizzard in 2023, Microsoft recorded large amounts of goodwill and intangible assets such as game franchises.', 'goodwill and intangible assets', 'paying above the value of net tangible assets creates goodwill, reflecting brands, intellectual property and expected future profits')],
  apply=[('A taxi company buys a car for $30,000. It expects to drive it 200,000 km and sell it for $6,000. In year 1 it drives 60,000 km. Calculate depreciation for year 1 using the units of production method and the net book value at the end of year 1.', 'Rate = 24,000/200,000 = $0.12 per km; year 1 = 60,000 × 0.12 = $7,200; NBV = $22,800.', 3)],
  evaluate=[('The units of production method is better than the straight-line method for all businesses.', ['matches cost to actual use', 'realistic for vehicles and machines', 'profit reflects activity'],
             ['harder to estimate total usage', 'more record-keeping', 'not suitable for assets that lose value with time (computers)', 'straight-line is simple and comparable'], 'Units of production suits assets that wear with use; straight-line is better for assets that lose value with time or obsolescence.')],
  )


# =============================================================================================
# ch12 Units 3.5-3.6 Ratio analysis
# =============================================================================================
@calc('ch12-st1', 'C3', (1, 5))
def profit_ratios(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    rev = rng.choice([200, 350, 500, 800, 1200]) * 1000
    gp = int(rev * rng.choice([0.25, 0.32, 0.4, 0.45, 0.55]))
    pbit = int(gp * rng.choice([0.3, 0.4, 0.5]))
    ce = rng.choice([400, 600, 900, 1500]) * 1000
    gpm, pm, roce = 100 * gp / rev, 100 * pbit / rev, 100 * pbit / ce
    frame = rng.choice([f'Extract from the accounts of {f_}: sales revenue {m(rev, c)}; gross profit {m(gp, c)}; profit before interest and tax {m(pbit, c)}; capital employed {m(ce, c)}.',
                        f'{f_} reports revenue of {m(rev, c)}, gross profit of {m(gp, c)} and PBIT of {m(pbit, c)}. Non-current liabilities plus equity total {m(ce, c)}.'])
    if slot.d <= 2:
        return dict(stem=frame + ' Calculate the gross profit margin.', answer=f'{p1(gpm)}%',
                    markingKey=MK(f'GPM = gross profit / sales revenue × 100 = {gp:,}/{rev:,} × 100 = {p1(gpm)}%.', f'{p1(gpm)}%'), marks=2)
    if slot.d == 3:
        return dict(stem=frame + ' Calculate the profit margin and the return on capital employed (ROCE).',
                    answer=f'Profit margin = {p1(pm)}%; ROCE = {p1(roce)}%',
                    markingKey=MK(f'PM = PBIT/revenue × 100 = {p1(pm)}%; ROCE = PBIT/capital employed × 100 = {pbit:,}/{ce:,} × 100 = {p1(roce)}%.', 'both ratios'), marks=4)
    gpm0 = gpm + rng.choice([-6, -4, 3, 5])
    pm0 = pm + rng.choice([-3, 2, 4])
    return dict(stem=frame + f' Last year the gross profit margin was {p1(gpm0)}% and the profit margin was {p1(pm0)}%. Calculate this year\'s gross profit margin, profit margin and ROCE, and comment on the changes, suggesting one strategy to improve profitability.',
                answer=f'GPM {p1(gpm)}% ({"up" if gpm > gpm0 else "down"} from {p1(gpm0)}%), PM {p1(pm)}% ({"up" if pm > pm0 else "down"} from {p1(pm0)}%), ROCE {p1(roce)}%. ' + ('A falling GPM suggests higher cost of sales or price cuts; ' if gpm < gpm0 else 'A rising GPM suggests better pricing or cheaper supplies; ') + ('a falling PM suggests weaker control of expenses. ' if pm < pm0 else 'a rising PM suggests better control of expenses. ') + 'Strategies: negotiate lower supplier prices, raise prices where demand is inelastic, cut overheads.',
                markingKey=MK(f'GPM = {p1(gpm)}%; PM = {p1(pm)}%; ROCE = {p1(roce)}%.', 'three ratios') + ' [R1][R1] comment on changes using both ratios; [R1] relevant strategy.', marks=6)


S('ch12-st1', concepts=('change', 'ethics'),
  terms=[('gross profit margin (GPM)', 'gross profit as a percentage of sales revenue: (gross profit / sales revenue) × 100'),
         ('profit margin (PM)', 'profit before interest and tax as a percentage of sales revenue: (PBIT / sales revenue) × 100'),
         ('return on capital employed (ROCE)', 'profit before interest and tax as a percentage of capital employed: (PBIT / capital employed) × 100, where capital employed = non-current liabilities + equity'),
         ('capital employed', 'the total long-term finance invested in a business: non-current liabilities plus equity'),
         ('ratio analysis', 'the use of financial ratios to interpret and compare the performance of a business over time or against competitors')],
  facts=[('If gross profit is $40,000 and sales revenue is $160,000, the gross profit margin is:', '25%', ['40%', '4%', '400%'], '40,000/160,000 × 100.'),
         ('ROCE measures:', 'how efficiently a business uses its long-term capital to generate profit', ['the ability to pay short-term debts', 'how quickly stock is sold', 'the proportion of debt finance'], 'Profit relative to capital employed.'),
         ('A business\'s GPM is unchanged but its profit margin falls. The most likely cause is:', 'an increase in expenses (overheads)', ['a rise in cost of sales', 'a rise in selling prices', 'a fall in interest rates'], 'Overheads sit between GP and PBIT.')],
  why=[('Explain why the gross profit margin may fall even if sales revenue increases.', 'If the cost of sales rises faster than revenue, for example because of higher supplier prices or discounting to win sales, gross profit grows less than revenue.'),
       ('Explain why ROCE is useful to investors.', 'It shows the return generated on all long-term capital and can be compared with interest rates or returns elsewhere to judge whether the investment is worthwhile.'),
       ('Explain why profitability ratios should be compared with other businesses in the same industry.', 'Margins vary greatly by industry (supermarkets have low margins, software firms high), so only comparisons with similar firms or over time show whether performance is good.')],
  contrast=[('the gross profit margin', 'the profit margin', 'The GPM shows profit after cost of sales as a share of revenue (pricing and production costs); the profit margin also deducts expenses, showing overall cost control.')],
  misc=[('A business with a high gross profit margin must be very profitable overall.', 'High expenses, interest and tax can turn high gross profit into a low or negative final profit; the profit margin and ROCE must also be checked.')],
  cases=[('Tesco\'s margins', 'UK supermarket Tesco typically earns an operating margin of around 3-4%, while luxury firm LVMH earns over 20%.', 'comparing profitability ratios', 'margins depend on the industry and business model, so ratios must be compared with similar firms'),
         ('Nvidia\'s profitability in 2024', 'Strong demand for AI chips pushed Nvidia\'s gross margin to over 70% in its 2024-25 financial year.', 'the gross profit margin', 'pricing power and a high-value product mean revenue far exceeds the cost of producing chips')],
  apply=[('Company A has revenue of $2 m and PBIT of $300,000; Company B has revenue of $5 m and PBIT of $500,000. Calculate the profit margin of each and explain why the larger company is not necessarily more profitable.', 'A: 15%; B: 10%. B earns more profit in total but less per dollar of sales; ROCE and industry comparisons are needed.', 3)],
  evaluate=[('ROCE is the most important ratio for judging the performance of a business.', ['combines profit and capital used', 'comparable with interest rates', 'used by investors'],
             ['ignores liquidity and cash flow', 'can be distorted by old, depreciated assets', 'short-term focus', 'industry differences'], 'ROCE is a key summary of performance, but it should be used with liquidity, efficiency and non-financial measures.')],
  )


@calc('ch12-st2', 'C3', (1, 5))
def liquidity(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    inv = rng.choice([30, 50, 80, 120]) * 1000
    debt = rng.choice([20, 40, 60]) * 1000
    cash = rng.choice([5, 10, 20, 35]) * 1000
    cl = rng.choice([40, 60, 80, 110]) * 1000
    ca = inv + debt + cash
    cr = ca / cl
    at = (ca - inv) / cl
    frame = rng.choice([f'{f_} has inventories of {m(inv, c)}, trade receivables of {m(debt, c)}, cash of {m(cash, c)} and current liabilities of {m(cl, c)}.',
                        f'The statement of financial position of {f_} shows current assets made up of stock {m(inv, c)}, debtors {m(debt, c)} and cash {m(cash, c)}; current liabilities total {m(cl, c)}.'])
    if slot.d <= 2:
        return dict(stem=frame + ' Calculate the current ratio.', answer=f'{p2(cr)} : 1',
                    markingKey=MK(f'Current ratio = current assets / current liabilities = {ca:,}/{cl:,} = {p2(cr)}.', f'{p2(cr)}:1'), marks=2)
    comment = ('below the usual 1.5-2 range, suggesting possible difficulty paying short-term debts' if cr < 1.5 else 'within or above the usual 1.5-2 range' if cr <= 2 else 'above 2, which may mean too much cash or stock tied up')
    if slot.d == 3:
        return dict(stem=frame + ' Calculate the current ratio and the acid-test ratio, and comment on the liquidity of the business.',
                    answer=f'Current ratio = {p2(cr)}:1 ({comment}); acid-test = ({ca:,} − {inv:,})/{cl:,} = {p2(at)}:1 ({"below 1, so it depends on selling stock to pay debts" if at < 1 else "at least 1, so it can meet short-term debts without selling stock"}).',
                    markingKey=MK(f'CR = {p2(cr)}; ATR = (CA − inventories)/CL = {p2(at)}.', 'both ratios') + ' [R1] comment.', marks=4)
    return dict(stem=frame + ' Calculate the current and acid-test ratios. Explain two strategies the business could use to improve its liquidity, and one drawback of each.',
                answer=f'CR = {p2(cr)}:1; ATR = {p2(at)}:1. Strategies: sell surplus stock (drawback: discounts reduce margins); chase debtors / offer early payment discounts (lower revenue); arrange longer credit with suppliers (supplier relations); sell and lease back assets (long-term cost); inject equity (dilution).',
                markingKey=MK(f'CR = {ca:,}/{cl:,} = {p2(cr)}; ATR = {ca - inv:,}/{cl:,} = {p2(at)}.', 'both ratios') + ' [R1][R1] strategies; [R1][R1] drawbacks.', marks=6)


S('ch12-st2', concepts=('change', 'ethics'),
  terms=[('liquidity', 'the ability of a business to pay its short-term debts as they fall due'),
         ('current ratio', 'current assets divided by current liabilities; a measure of liquidity, often considered healthy between 1.5 and 2'),
         ('acid-test (quick) ratio', '(current assets − inventories) / current liabilities; a stricter liquidity measure that excludes stock'),
         ('working capital', 'current assets minus current liabilities; the funds available for day-to-day operations'),
         ('sale and leaseback', 'selling an asset such as property and then leasing it back, to release cash while continuing to use it')],
  facts=[('Why does the acid-test ratio exclude inventories?', 'Inventories may be hard to convert quickly into cash without loss of value', ['Inventories are a current liability', 'Inventories are always worthless', 'Inventories are non-current assets'], 'Stock is the least liquid current asset.'),
         ('A current ratio of 0.8:1 suggests that:', 'current liabilities exceed current assets', ['the business is very profitable', 'the business has excess cash', 'stock levels are too low'], 'Possible liquidity problems.'),
         ('Supermarkets often operate with current ratios below 1 because:', 'they sell for cash quickly but pay suppliers on credit', ['they hold no stock', 'they have no debts', 'they never use trade credit'], 'Negative working capital model.')],
  why=[('Explain why a very high current ratio is not necessarily good for a business.', 'It may mean excessive stock or cash sitting idle that could be invested more profitably, or slow collection of debts.'),
       ('Explain why liquidity is important even for a profitable business.', 'If a business cannot pay suppliers, wages or lenders on time it may be forced into insolvency, even if it is profitable on paper.'),
       ('Explain why offering discounts for early payment can improve liquidity.', 'Customers pay sooner, so trade receivables turn into cash faster, although the discount reduces revenue.')],
  contrast=[('the current ratio', 'the acid-test ratio', 'The current ratio compares all current assets with current liabilities; the acid-test excludes inventories, giving a stricter measure of the ability to pay short-term debts.'),
            ('liquidity', 'profitability', 'Liquidity is the ability to pay short-term debts; profitability is the ability to generate profit relative to revenue or capital.')],
  misc=[('An acid-test ratio below 1 always means the business is about to fail.', 'Industries such as supermarkets and fast food operate safely below 1 because they sell for cash and receive credit from suppliers; context and trends matter.')],
  cases=[('the collapse of Thomas Cook', 'Travel company Thomas Cook collapsed in September 2019 after failing to raise £200 m of extra funds, stranding about 150,000 UK customers abroad.', 'liquidity', 'large debts and insufficient cash meant it could not meet short-term obligations'),
         ('Tesco\'s negative working capital', 'Large supermarkets such as Tesco usually report current ratios below 1 because they sell inventory quickly for cash while paying suppliers weeks later.', 'interpreting liquidity ratios', 'a low ratio can be sustainable when cash comes in faster than payments go out')],
  apply=[('A firm has current assets of $90,000 (including inventories of $50,000) and current liabilities of $60,000. Calculate its current and acid-test ratios and recommend one way to improve liquidity.', 'CR = 1.5; ATR = 0.67. Improve by reducing stock (JIT, clearance sales), chasing debtors, or negotiating longer supplier credit.', 4)],
  evaluate=[('Liquidity ratios give a reliable picture of a business\'s financial health.', ['quick indicators of ability to pay debts', 'comparable over time', 'warn of insolvency risk'],
             ['snapshot at one date (window dressing)', 'industry norms differ', 'ignore timing of cash flows', 'need cash-flow forecasts too'], 'They are useful warning signs but should be read alongside cash-flow forecasts, industry norms and trends.')],
  )


@calc('ch12-st3', 'C3', (1, 5))
def efficiency(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    cogs = rng.choice([240, 365, 480, 730, 900]) * 1000
    open_s, close_s = rng.choice([20, 30, 40]) * 1000, rng.choice([25, 35, 50]) * 1000
    avg = (open_s + close_s) / 2
    st_t = cogs / avg
    st_d = avg / cogs * 365
    rev = int(cogs * rng.choice([1.4, 1.6, 2.0]))
    debtors = rng.choice([30, 45, 60, 90]) * 1000
    creditors = rng.choice([25, 40, 55]) * 1000
    dd = debtors / rev * 365
    cd = creditors / cogs * 365
    ltl = rng.choice([100, 200, 300]) * 1000
    eq = rng.choice([200, 300, 500]) * 1000
    gear = 100 * ltl / (ltl + eq)
    if slot.d <= 2:
        return dict(stem=f'{f_} had opening inventory of {m(open_s, c)} and closing inventory of {m(close_s, c)}. Cost of sales for the year was {m(cogs, c)}. Calculate the stock turnover (number of times per year).',
                    answer=f'{p1(st_t)} times', markingKey=MK(f'Average stock = ({open_s:,} + {close_s:,})/2 = {avg:,.0f}; turnover = cost of sales / average stock = {p1(st_t)}.', f'{p1(st_t)} times'), marks=2)
    if slot.d == 3:
        return dict(stem=f'{f_} has sales revenue of {m(rev, c)}, cost of sales of {m(cogs, c)}, trade receivables of {m(debtors, c)} and trade payables of {m(creditors, c)}. Calculate debtor days and creditor days, and comment on the result.',
                    answer=f'Debtor days = {p1(dd)}; creditor days = {p1(cd)}. {"Customers pay more slowly than the firm pays suppliers, which puts pressure on cash flow." if dd > cd else "The firm collects from customers faster than it pays suppliers, which helps cash flow."}',
                    markingKey=MK(f'Debtor days = receivables/revenue × 365 = {p1(dd)}; creditor days = payables/cost of sales × 365 = {p1(cd)}.', 'both ratios') + ' [R1] comment.', marks=4)
    return dict(stem=f'Data for {f_}: cost of sales {m(cogs, c)}; average inventory {m(avg, c)}; sales revenue {m(rev, c)}; trade receivables {m(debtors, c)}; trade payables {m(creditors, c)}; non-current liabilities {m(ltl, c)}; equity {m(eq, c)}. Calculate stock turnover (in days), debtor days, creditor days and the gearing ratio, and comment on what they show.',
                answer=f'Stock turnover = {p1(st_d)} days; debtor days = {p1(dd)}; creditor days = {p1(cd)}; gearing = {p1(gear)}% ({"highly geared (above 50%)" if gear > 50 else "moderately geared" if gear >= 25 else "low gearing"}). Comment on the cash conversion cycle and financial risk.',
                markingKey=MK(f'Stock days = {avg:,.0f}/{cogs:,} × 365 = {p1(st_d)}; DD = {p1(dd)}; CD = {p1(cd)}; gearing = NCL/(NCL + equity) × 100 = {p1(gear)}%.', 'four ratios') + ' [R1][R1] interpretation.', marks=6)


@calc('ch12-st3', 'C3', (2, 4))
def gearing(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    ltl = rng.choice([150, 250, 400, 600]) * 1000
    eq = rng.choice([200, 300, 450, 600]) * 1000
    newl = rng.choice([100, 200, 300]) * 1000
    g0 = 100 * ltl / (ltl + eq)
    g1 = 100 * (ltl + newl) / (ltl + newl + eq)
    return dict(stem=f'{f_} has non-current liabilities of {m(ltl, c)} and equity of {m(eq, c)}. It plans to borrow a further {m(newl, c)} with a ten-year loan to build a new store. Calculate the gearing ratio before and after the loan, and explain one risk of higher gearing.',
                answer=f'Before: {p1(g0)}%; after: {p1(g1)}%. Risk: higher interest payments reduce profit and become hard to meet if sales fall or interest rates rise; lenders may refuse further credit.',
                markingKey=MK(f'Gearing = NCL/(NCL + equity) × 100: {p1(g0)}% → {p1(g1)}%.', 'both ratios') + ' [R1] risk.', marks=4)


S('ch12-st3', concepts=('change', 'ethics'),
  terms=[('stock turnover', 'the number of times a business sells and replaces its stock in a period (cost of sales / average stock), or the average number of days stock is held'),
         ('debtor days', 'the average number of days it takes a business to collect payment from its customers: (trade receivables / sales revenue) × 365'),
         ('creditor days', 'the average number of days a business takes to pay its suppliers: (trade payables / cost of sales) × 365'),
         ('gearing ratio', 'non-current liabilities as a percentage of capital employed: (non-current liabilities / (non-current liabilities + equity)) × 100'),
         ('highly geared', 'a business with a gearing ratio above 50%, financed mainly by long-term debt')],
  facts=[('A gearing ratio of 60% means that the business is:', 'highly geared and more exposed to interest-rate rises', ['low geared', 'unable to borrow at all', 'financed mainly by equity'], 'More than half of capital employed is debt.'),
         ('If debtor days rise from 30 to 55, which is true?', 'Customers are taking longer to pay, worsening cash flow', ['The firm is paying suppliers faster', 'Stock is selling faster', 'Gearing has fallen'], 'Cash is tied up in receivables.'),
         ('A fresh fruit retailer is likely to have:', 'a high stock turnover', ['a very low stock turnover', 'no stock', 'very high creditor days'], 'Perishable goods sell quickly.')],
  why=[('Explain why a high stock turnover is usually desirable.', 'Stock sells quickly, so less cash is tied up in inventory, storage costs fall and there is less risk of obsolescence or spoilage.'),
       ('Explain why a business might want to increase its creditor days.', 'Paying suppliers later keeps cash in the business longer, improving liquidity, although it may damage supplier relations and lose discounts.'),
       ('Explain why a highly geared business is more vulnerable when interest rates rise.', 'Interest payments on its large debts increase, reducing profit and cash available, and raising the risk of being unable to meet repayments.')],
  contrast=[('debtor days', 'creditor days', 'Debtor days measure how long customers take to pay the business; creditor days measure how long the business takes to pay its suppliers.')],
  misc=[('Low gearing is always better than high gearing.', 'Low gearing reduces risk, but moderate debt can be cheaper than equity and boosts returns to shareholders when profits are strong; the right level depends on the stability of cash flows and interest rates.')],
  cases=[('Zara\'s fast-fashion supply chain', 'Inditex (Zara) designs and delivers new styles to stores within weeks and holds less inventory than many rivals, with stock turning over faster.', 'stock turnover', 'fast-moving inventory reduces markdowns and the cash tied up in stock'),
         ('Evergrande\'s debt', 'Chinese property developer Evergrande accumulated liabilities of over $300 bn and was ordered to liquidate by a Hong Kong court in January 2024.', 'gearing and financial risk', 'very high borrowing to fund growth left it unable to service its debts when property sales fell')],
  apply=[('A furniture retailer has stock turnover of 120 days, while the industry average is 75 days. Suggest two reasons and one way of improving the ratio.', 'Reasons: slow-selling or out-of-fashion lines, over-ordering, weak demand. Improve: just-in-time ordering, clearance sales, better demand forecasting, narrower range.', 4)],
  evaluate=[('Efficiency ratios are more useful than profitability ratios for managers.', ['show how well working capital is managed', 'identify causes of cash problems', 'operational targets'],
             ['profitability determines survival and returns', 'efficiency norms vary by industry', 'both needed for full picture'], 'Efficiency ratios help managers control operations, but they must be used alongside profitability and liquidity ratios.')],
  )

S('ch12-st4', concepts=('ethics', 'change'),
  terms=[('insolvency', 'the situation in which a business or individual is unable to pay its debts as they fall due'),
         ('bankruptcy', 'a legal process in which an insolvent individual (or in some countries a business) is declared unable to pay debts, and assets are sold to pay creditors'),
         ('liquidation', 'the process of closing a company and selling its assets to pay creditors'),
         ('administration', 'a legal process in which an insolvency practitioner takes control of an insolvent company to try to rescue it or sell it as a going concern'),
         ('limitations of ratio analysis', 'weaknesses of using ratios, such as reliance on historical data, differences in accounting policies, window dressing and the omission of qualitative factors')],
  facts=[('Insolvency means that a business:', 'cannot pay its debts when they are due', ['has made a loss for one year', 'has a high gross profit margin', 'has paid no dividend'], 'A cash-flow test.'),
         ('Which is a limitation of ratio analysis?', 'Ratios are based on historical data and may not predict the future', ['Ratios cannot be calculated from accounts', 'Ratios are always the same for every firm', 'Ratios include all qualitative factors'], 'Past figures, snapshot.'),
         ('Thomas Cook\'s collapse in 2019 resulted in:', 'compulsory liquidation', ['a merger with TUI', 'a successful share issue', 'a management buyout'], 'Its assets were sold to pay creditors.')],
  why=[('Explain why a profitable business can become insolvent.', 'Profit is not cash: if customers pay late, stock builds up or large debts fall due, the business may lack cash to pay creditors even though it is profitable.'),
       ('Explain why ratio analysis should be used with caution when comparing two businesses.', 'They may use different accounting policies (depreciation, stock valuation), have different year-ends and operate in different markets, so ratios are not directly comparable.'),
       ('Explain why qualitative information is needed alongside ratios.', 'Ratios do not show factors such as management quality, staff morale, brand strength, innovation or upcoming regulation, which strongly affect future performance.')],
  contrast=[('insolvency', 'bankruptcy', 'Insolvency is the financial state of being unable to pay debts on time; bankruptcy is a legal process (mainly for individuals) that may follow insolvency, in which assets are used to repay creditors.')],
  misc=[('A business that is insolvent must immediately close down.', 'It may enter administration, restructure debts, be sold or be rescued; liquidation is only one possible outcome.')],
  cases=[('Silicon Valley Bank in 2023', 'Silicon Valley Bank failed in March 2023 after depositors withdrew $42 bn in a day; its bond holdings had lost value as interest rates rose.', 'insolvency', 'a sudden loss of liquidity and asset values made the bank unable to meet withdrawals'),
         ('Wilko\'s administration', 'UK discount retailer Wilko entered administration in August 2023; about 12,500 jobs were lost and stores closed after no buyer was found for the whole business.', 'insolvency versus bankruptcy', 'administration attempted a rescue before the business was broken up and liquidated')],
  apply=[('A manager says: "Our current ratio is 1.8 and ROCE is 15%, so the business is safe." Explain two limitations of relying on these ratios.', 'They are historical and a snapshot (may be window dressed); they ignore future cash flows, industry trends and qualitative factors; comparisons depend on accounting policies.', 4)],
  evaluate=[('Ratio analysis is of limited value in predicting business failure.', ['historical data', 'window dressing', 'qualitative factors omitted', 'failure often sudden'],
             ['trends in liquidity and gearing give early warnings', 'used by lenders and investors', 'combined ratios (e.g. Altman Z-score) predict failure'], 'Ratios give useful warnings, especially in trends, but predicting failure also requires cash-flow forecasts and qualitative judgement.')],
  )


# =============================================================================================
# ch13 Units 3.7-3.8 Cash flow and investment appraisal
# =============================================================================================
S('ch13-st1', concepts=('change', 'ethics'),
  terms=[('cash flow', 'the movement of money into (inflows) and out of (outflows) a business over a period'),
         ('profit', 'the difference between revenue and costs over a period, which may include sales and costs not yet paid in cash'),
         ('working capital cycle', 'the time between paying for raw materials and receiving cash from the sale of finished goods'),
         ('cash inflow', 'money received by a business, for example from cash sales, payments by debtors, loans and asset sales'),
         ('cash outflow', 'money paid out by a business, for example for wages, materials, rent, loan repayments and taxes')],
  facts=[('Which of the following increases profit but does not immediately increase cash?', 'A sale on 60 days\' credit', ['A cash sale', 'A new bank loan', 'Selling shares'], 'Revenue is recorded before cash arrives.'),
         ('A business takes out a $50,000 loan. This:', 'increases cash but does not increase profit', ['increases profit and cash', 'reduces cash', 'increases revenue'], 'Loans are not revenue.'),
         ('Shortening the working capital cycle means:', 'cash is received sooner after paying for inputs', ['stock is held for longer', 'customers pay more slowly', 'suppliers are paid earlier'], 'Faster conversion of inputs into cash.')],
  why=[('Explain why a profitable business may have cash-flow problems.', 'Sales may be on credit while suppliers and wages must be paid now; high stock levels, rapid growth (overtrading) and capital spending all use cash before profits are received.'),
       ('Explain why cash flow is especially important for start-ups.', 'They often have high initial outflows (equipment, stock, marketing), low early sales and little access to credit, so running out of cash is a common cause of failure.'),
       ('Explain why a long working capital cycle can create problems.', 'Cash is tied up in stock and receivables for longer, so the business needs more finance to pay suppliers and wages in the meantime.')],
  contrast=[('profit', 'cash flow', 'Profit is revenue minus costs over a period, including credit sales and non-cash items such as depreciation; cash flow is the actual money coming in and going out.')],
  misc=[('A business that makes a profit will always have enough cash.', 'Timing differences, credit sales, stock purchases, loan repayments and capital expenditure mean profitable businesses can run out of cash.')],
  cases=[('overtrading at a fast-growing start-up', 'Many fast-growing firms, such as some UK fintech and food-delivery start-ups in 2021-22, have struggled to fund rapid expansion despite rising sales.', 'the difference between profit and cash flow', 'rapid growth requires paying for stock, staff and marketing before customers\' cash arrives (overtrading)'),
         ('Carillion\'s late payment to suppliers', 'Before its collapse in 2018, Carillion was known for paying small suppliers up to 120 days after invoice.', 'the working capital cycle', 'stretching creditor days improved Carillion\'s own cash position but shifted cash-flow problems onto suppliers')],
  apply=[('A furniture maker pays for timber on delivery, takes 30 days to make and sell its products and gives customers 60 days\' credit. Calculate the length of its working capital cycle and suggest one way to shorten it.', 'About 90 days (0 days\' credit from suppliers + 30 days production/storage + 60 days customer credit). Shorten by negotiating credit with timber suppliers, reducing customer credit or offering early-payment discounts.', 3)],
  evaluate=[('Cash flow is more important than profit for a business.', ['lack of cash causes insolvency', 'needed to pay wages and suppliers', 'start-ups fail through cash shortages'],
             ['long-run survival requires profit', 'profit attracts investors and finance', 'cash can be borrowed if profitable'], 'Cash flow is more important in the short run for survival; profit is more important in the long run for sustainability and growth.')],
  )


@calc('ch13-st2', 'C3', (2, 5))
def cash_forecast(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    months = rng.choice([['January', 'February', 'March'], ['April', 'May', 'June'], ['July', 'August', 'September'], ['October', 'November', 'December']])
    opening = rng.choice([2, 5, 8, 10, 15]) * 1000
    sales = [rng.choice([18, 20, 24, 28, 32, 40]) * 1000 for _ in range(3)]
    other_in = [0, rng.choice([0, 10_000]), 0]
    wages = rng.choice([8, 10, 12]) * 1000
    rent = rng.choice([2, 3, 4]) * 1000
    mats = [int(s * rng.choice([0.35, 0.4, 0.5])) for s in sales]
    capex = [0, 0, rng.choice([0, 15_000, 25_000])]
    open_ = opening
    rows = []
    for i in range(3):
        tin = sales[i] + other_in[i]
        tout = wages + rent + mats[i] + capex[i]
        net = tin - tout
        close = open_ + net
        rows.append((open_, tin, tout, net, close))
        open_ = close
    data = (f'Opening balance for {months[0]}: {m(opening, c)}. Cash sales: ' + ', '.join(f'{mo} {m(s, c)}' for mo, s in zip(months, sales)) +
            (f'. A loan of {m(other_in[1], c)} will be received in {months[1]}' if other_in[1] else '') +
            f'. Monthly wages {m(wages, c)} and rent {m(rent, c)}. Materials: ' + ', '.join(f'{mo} {m(x, c)}' for mo, x in zip(months, mats)) +
            (f'. A new machine costing {m(capex[2], c)} will be paid for in {months[2]}' if capex[2] else '') + '.')
    tab = '; '.join(f'{months[i]}: opening {m(r[0], c)}, inflows {m(r[1], c)}, outflows {m(r[2], c)}, net {m(r[3], c)}, closing {m(r[4], c)}' for i, r in enumerate(rows))
    neg = [months[i] for i, r in enumerate(rows) if r[4] < 0]
    if slot.d <= 3:
        r = rows[0]
        return dict(stem=f'{f_} prepares a cash-flow forecast. {data} Calculate the net cash flow and closing balance for {months[0]}.',
                    answer=f'Net cash flow = {m(r[1], c)} − {m(r[2], c)} = {m(r[3], c)}; closing balance = {m(r[4], c)}',
                    markingKey=MK(f'Inflows {r[1]:,}; outflows {wages:,} + {rent:,} + {mats[0]:,} + {capex[0]:,} = {r[2]:,}; net {r[3]:,}; closing = opening + net = {r[4]:,}.', 'net flow and closing balance'), marks=3)
    return dict(stem=f'{f_} prepares a cash-flow forecast for the next three months. {data} Construct a cash-flow forecast for the three months and, {"identify any month with a negative closing balance and " if neg else ""}recommend one strategy to improve the firm\'s cash position.',
                answer=f'{tab}. ' + (f'Negative closing balance in {", ".join(neg)}. ' if neg else 'Closing balances remain positive. ') + 'Strategies: arrange an overdraft, delay the machine purchase or lease it, negotiate trade credit for materials, chase sales / offer incentives.',
                markingKey=f'[1] inflows each month; [1] outflows each month; [1] net cash flows; [1] closing balances carried forward as next opening balance ({tab}); [1] format; [1] justified strategy. Apply OFR.', marks=6)


S('ch13-st2', concepts=('change', 'ethics'),
  terms=[('cash-flow forecast', 'a prediction of the cash inflows and outflows of a business over a future period, usually month by month, showing opening and closing balances'),
         ('net cash flow', 'cash inflows minus cash outflows for a period'),
         ('opening balance', 'the amount of cash a business has at the start of a period, equal to the previous period\'s closing balance'),
         ('closing balance', 'opening balance plus net cash flow for the period'),
         ('debt factoring', 'selling a business\'s trade receivables to a specialist firm (factor) at a discount in return for immediate cash')],
  facts=[('If the opening balance is $5,000, inflows are $12,000 and outflows are $15,000, the closing balance is:', '$2,000', ['$8,000', '−$3,000', '$32,000'], '5,000 + 12,000 − 15,000.'),
         ('Which strategy improves cash flow by increasing inflows?', 'Offering discounts for early payment by customers', ['Buying more stock', 'Paying suppliers earlier', 'Buying new machinery'], 'Customers pay sooner.'),
         ('Debt factoring involves:', 'selling receivables to a third party for immediate cash', ['borrowing from shareholders', 'leasing equipment', 'increasing the overdraft limit'], 'The factor collects the debts.')],
  why=[('Explain why businesses prepare cash-flow forecasts.', 'To predict periods of cash shortage, arrange finance in advance (e.g. an overdraft), plan spending, and support applications for loans and investment.'),
       ('Explain why cash-flow forecasts may be inaccurate.', 'They rely on predictions of sales, costs, customer payments and the economy, which can change; unexpected events and over-optimism reduce accuracy.'),
       ('Explain why reducing stock levels can improve cash flow.', 'Less cash is spent on buying and storing inventory, so more is available for other payments; it also reduces storage costs and waste.')],
  contrast=[('strategies that increase cash inflows', 'strategies that reduce cash outflows', 'Increasing inflows: chase debtors, early-payment discounts, debt factoring, sale and leaseback, new sources of finance. Reducing outflows: delay payments to suppliers, lease rather than buy, cut costs, reduce stock.')],
  misc=[('A negative closing balance in a cash-flow forecast means the business is unprofitable.', 'It means cash outflows exceed inflows plus the opening balance in that month; it can be temporary (e.g. seasonal) and does not show profitability.')],
  cases=[('seasonal cash flow at a ski resort', 'Ski resort operators in the Alps receive most of their cash between December and April but must pay staff, maintenance and lift investment all year.', 'cash-flow forecasting', 'forecasts help the business arrange overdrafts for the off-season'),
         ('the UK furlough scheme', 'In 2020 the UK Coronavirus Job Retention Scheme paid up to 80% of furloughed employees\' wages (up to £2,500 a month), supporting about 11.7 million jobs over its lifetime.', 'strategies to deal with cash-flow problems', 'government support reduced firms\' cash outflows for wages when inflows collapsed')],
  apply=[('A toy shop expects closing cash balances of $4,000 in October, −$6,000 in November and $12,000 in December. Explain why this pattern might occur and recommend one strategy for November.', 'Stock for Christmas is bought in October-November (large outflows) before peak sales in December (large inflows). Strategy: arrange a short-term overdraft, negotiate trade credit with suppliers, or delay non-essential spending.', 4)],
  evaluate=[('Debt factoring is the best way for a small business to solve cash-flow problems.', ['immediate cash', 'factor manages collection', 'no new debt'],
             ['costly – loses a percentage of receivables', 'customers may see it as a sign of weakness', 'does not solve underlying problems', 'only works if the firm has receivables'], 'Factoring helps quickly where receivables are large, but cheaper solutions such as better credit control or an overdraft may be preferable.')],
  )


def payback_text(cf, cost):
    cum = -cost
    for i, v in enumerate(cf, 1):
        if cum + v >= 0:
            months = (-cum) / v * 12
            return i - 1, months
        cum += v
    return None


@calc('ch13-st3', 'C3', (1, 5))
def payback_arr(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    proj = rng.choice(['a new delivery robot fleet', 'an automated packing line', 'a second café outlet', 'a solar energy system', 'new 3D printers', 'an online ordering platform'])
    cost = rng.choice([50, 80, 100, 120, 200, 250]) * 1000
    n = rng.choice([4, 5])
    for _ in range(50):
        cf = [rng.choice([15, 20, 25, 30, 35, 40, 50, 60, 70]) * cost // 200 for _ in range(n)]
        if sum(cf) > cost * 1.1 and payback_text(cf, cost):
            break
    else:
        return None
    yrs, mo = payback_text(cf, cost)
    tot = sum(cf)
    arr = 100 * ((tot - cost) / n) / cost
    flows = ', '.join(f'year {i} {m(v, c)}' for i, v in enumerate(cf, 1))
    frame = rng.choice([f'{f_} is considering {proj} costing {m(cost, c)}. Expected net cash flows are: {flows}.',
                        f'An investment in {proj} by {f_} requires {m(cost, c)} now and is expected to generate net cash inflows of {flows}.'])
    if slot.d <= 2:
        return dict(stem=frame + ' Calculate the payback period (in years and months).', answer=f'{yrs} years and {round(mo)} months',
                    markingKey=MK(f'Cumulative cash flow becomes positive in year {yrs + 1}; months = remaining amount / year {yrs + 1} cash flow × 12 = {mo:.1f}.', f'{yrs} years {round(mo)} months'), marks=2)
    if slot.d == 3:
        return dict(stem=frame + ' Calculate the average rate of return (ARR).', answer=f'{p1(arr)}%',
                    markingKey=MK(f'Total net return = {tot:,} − {cost:,} = {tot - cost:,}; per year = {(tot - cost) / n:,.0f}; ARR = {(tot - cost) / n:,.0f}/{cost:,} × 100 = {p1(arr)}%.', f'{p1(arr)}%'), marks=4)
    return dict(stem=frame + f' Calculate the payback period and the average rate of return. The firm requires payback within 3 years and an ARR of at least 12%. Recommend whether {f_} should invest, referring to one non-financial factor.',
                answer=f'Payback = {yrs} years {round(mo)} months; ARR = {p1(arr)}%. ' + (f'Both criteria are met' if (yrs < 3 or (yrs == 3 and mo == 0)) and arr >= 12 else 'Not all criteria are met') + ', so the financial case is ' + ('strong' if (yrs < 3) and arr >= 12 else 'weak') + '; non-financial factors such as reliability of forecasts, impact on staff, brand and sustainability should also be considered.',
                markingKey=MK(f'Payback {yrs} y {mo:.1f} m; ARR = (({tot:,} − {cost:,})/{n})/{cost:,} × 100 = {p1(arr)}%.', 'both results') + ' [R1][R1] justified recommendation with a non-financial factor.', marks=6)


S('ch13-st3', concepts=('change', 'sustainability', 'creativity'),
  terms=[('investment appraisal', 'the use of quantitative techniques to assess whether an investment project is financially worthwhile'),
         ('payback period', 'the length of time it takes for the net cash inflows from an investment to repay its initial cost'),
         ('average rate of return (ARR)', 'the average annual net return of an investment as a percentage of its initial cost: ((total returns − cost) / years of use) / cost × 100'),
         ('net cash flow (investment)', 'the expected cash inflows minus cash outflows from an investment in each year')],
  facts=[('Which is an advantage of the payback period method?', 'It is simple and focuses on how quickly the cost is recovered', ['It considers all cash flows after payback', 'It discounts future cash flows', 'It measures overall profitability'], 'Useful when cash is short or risk is high.'),
         ('An investment costs $100,000 and generates total net cash flows of $160,000 over 5 years. Its ARR is:', '12%', ['60%', '32%', '16%'], '(60,000 / 5) / 100,000 × 100 = 12%.'),
         ('A limitation of ARR is that it:', 'ignores the timing of cash flows', ['ignores profitability', 'cannot be compared with interest rates', 'only measures time'], 'Early and late returns count equally.')],
  why=[('Explain why the payback period is useful in industries with rapid technological change.', 'Equipment may become obsolete quickly, so recovering the cost fast reduces the risk that the investment is superseded before it pays for itself.'),
       ('Explain why ARR can be compared with the interest rate on a loan.', 'If the ARR exceeds the cost of borrowing, the project earns more than the finance costs; if it is lower, the money might be better saved or used elsewhere.'),
       ('Explain why investment appraisal results should be treated with caution.', 'They depend on forecasts of future cash flows, which are uncertain, and they ignore qualitative factors such as staff reactions, ethics and strategic fit.')],
  contrast=[('the payback period', 'the average rate of return', 'The payback period measures how quickly an investment recovers its cost (liquidity and risk); ARR measures the average annual profitability of the investment over its whole life.')],
  misc=[('The project with the shortest payback period is always the best choice.', 'Payback ignores cash flows after the payback point and overall profitability; a project with longer payback may earn much more over its life.')],
  cases=[('Tesla\'s Gigafactory investments', 'Tesla\'s Gigafactory in Texas cost over $5 bn and began production of the Model Y in 2022.', 'investment appraisal', 'very large capital projects require long payback periods and depend on forecasts of future demand'),
         ('LED lighting in offices', 'Many firms replacing old lighting with LEDs report payback periods of two to four years from lower electricity bills.', 'the payback period', 'quick payback from energy savings makes sustainability investments financially attractive')],
  apply=[('Project A costs $60,000 and returns $20,000 a year for 5 years. Project B costs $60,000 and returns $30,000 in year 1, $20,000 in year 2 and $10,000 a year for years 3-5. Calculate the payback period of each and explain which a cash-strapped firm should prefer.', 'Payback A: 20,000 × 3 = 60,000, so 3 years. Payback B: 30,000 + 20,000 = 50,000 after 2 years; the remaining 10,000 comes from year 3, so 3 years. The paybacks are equal, so compare ARR: A = ((100,000 − 60,000) / 5) / 60,000 × 100 = 13.3%; B = ((80,000 − 60,000) / 5) / 60,000 × 100 = 6.7%. A cash-strapped firm gets the same payback from both but A is more profitable, so it should choose A (B does return more cash earlier, in year 1).', 6)],
  evaluate=[('The average rate of return is a better investment appraisal method than the payback period.', ['measures profitability over the whole life', 'easy to compare with interest rates', 'considers all cash flows'],
             ['ignores timing and the time value of money', 'payback shows risk and liquidity', 'both rely on forecasts', 'NPV is more accurate'], 'ARR is better for judging profitability, payback for risk and liquidity; firms should use both, alongside NPV and qualitative factors.')],
  )

DF = {r: [round(1 / (1 + r / 100) ** n, 4) for n in range(1, 7)] for r in (4, 5, 6, 8, 10, 12)}


@calc('ch13-st4', 'C3', (2, 5))
def npv_calc(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    r = rng.choice(list(DF))
    n = rng.choice([3, 4, 5])
    cost = rng.choice([40, 60, 100, 150, 200]) * 1000
    cf = [rng.choice([15, 20, 25, 30, 35, 40]) * cost // 100 for _ in range(n)]
    dfs = DF[r][:n]
    pv = [v * d for v, d in zip(cf, dfs)]
    npv = sum(pv) - cost
    table = ', '.join(f'year {i} {d:.4f}' for i, d in enumerate(dfs, 1))
    flows = ', '.join(f'year {i} {m(v, c)}' for i, v in enumerate(cf, 1))
    if slot.d <= 3:
        return dict(stem=f'{f_} is considering an investment of {m(cost, c)} with expected net cash flows of {flows}. Using the discount factors at {r}% ({table}), calculate the net present value (NPV).',
                    answer=f'NPV = {m(sum(pv), c)} − {m(cost, c)} = {m(npv, c)}',
                    markingKey=MK('PVs: ' + ', '.join(f'{v:,} × {d:.4f} = {p:,.0f}' for v, d, p in zip(cf, dfs, pv)) + f'; total PV {sum(pv):,.0f}; NPV = {npv:,.0f}.', m(npv, c)), marks=4)
    r2_ = max(k for k in DF if k > r) if any(k > r for k in DF) else r
    npv2 = sum(v * d for v, d in zip(cf, DF[r2_][:n])) - cost
    return dict(stem=f'{f_} is considering an investment of {m(cost, c)} with expected net cash flows of {flows}. Discount factors at {r}%: {table}. At {r2_}% the discount factors are ' + ', '.join(f'year {i} {d:.4f}' for i, d in enumerate(DF[r2_][:n], 1)) + f'. Calculate the NPV at both rates, and recommend whether {f_} should invest if its cost of capital is uncertain.',
                answer=f'NPV at {r}% = {m(npv, c)}; NPV at {r2_}% = {m(npv2, c)}. ' + ('Positive at both rates: invest, since the project adds value even at the higher cost of capital.' if npv > 0 and npv2 > 0 else 'Negative at both rates: do not invest.' if npv <= 0 and npv2 <= 0 else 'Positive at the lower rate but negative at the higher rate: the decision depends on the cost of capital and risk; consider qualitative factors before investing.'),
                markingKey=MK(f'NPV({r}%) = {npv:,.0f}; NPV({r2_}%) = {npv2:,.0f}.', 'both NPVs') + ' [R1][R1] recommendation linked to the cost of capital and qualitative factors.', marks=6)


S('ch13-st4', concepts=('change', 'sustainability'),
  terms=[('net present value (NPV)', 'the sum of the present values of an investment\'s future net cash flows minus its initial cost'),
         ('discounting', 'converting future cash flows into their present values using a discount rate, reflecting the time value of money'),
         ('discount factor', 'the number by which a future cash flow is multiplied to find its present value: 1 / (1 + r)^n'),
         ('time value of money', 'the principle that money received today is worth more than the same amount received in the future, because it can be invested and because of inflation and risk')],
  facts=[('A positive NPV means that:', 'the present value of returns exceeds the cost, so the investment adds value', ['the project will definitely succeed', 'payback is less than one year', 'the ARR is negative'], 'Returns exceed cost in today\'s money.'),
         ('A higher discount rate will:', 'reduce the NPV of a project', ['increase the NPV', 'have no effect on NPV', 'shorten the life of the project'], 'Future flows are worth less.'),
         ('The discount factor for year 2 at 10% is approximately:', '0.8264', ['0.9091', '0.8', '1.21'], '1/1.1² = 0.8264.')],
  why=[('Explain why NPV is considered a more accurate method than ARR.', 'NPV takes into account the timing of cash flows and the time value of money, so earlier returns are valued more highly than later ones.'),
       ('Explain why the choice of discount rate is important in NPV calculations.', 'A higher rate reduces the present value of future cash flows; choosing a rate that does not reflect the cost of capital and risk can make a poor project look profitable or vice versa.'),
       ('Explain why a business might reject a project with a positive NPV.', 'Forecasts may be uncertain, finance may be limited (capital rationing), the project may conflict with strategy or ethics, or another project may have a higher NPV.')],
  contrast=[('NPV', 'payback period', 'NPV measures the value an investment adds in today\'s money over its whole life; payback measures only how long it takes to recover the cost, ignoring later cash flows and discounting.')],
  misc=[('A project with an NPV of zero makes no profit at all.', 'An NPV of zero means the project earns exactly the discount rate (the required return); it covers the cost of capital.')],
  cases=[('offshore wind farms in 2023', 'In 2023 Ørsted cancelled its Ocean Wind projects off New Jersey, taking impairments of about $4 bn, as higher interest rates and costs made the projects unviable.', 'net present value and discount rates', 'higher interest rates raise the discount rate and costs, turning previously positive NPVs negative'),
         ('the UK HS2 railway', 'Cost estimates for the UK\'s HS2 high-speed railway rose from about £33 bn in 2010 to well over £60 bn for a shortened route, and the northern leg was cancelled in 2023.', 'investment appraisal of long-term projects', 'rising costs and distant benefits reduce the present value of large infrastructure projects')],
  apply=[('An investment costs $10,000 and returns $6,000 at the end of each of the next two years. Using discount factors of 0.9091 (year 1) and 0.8264 (year 2), calculate the NPV.', 'PV = 6,000 × 0.9091 + 6,000 × 0.8264 = 5,454.6 + 4,958.4 = $10,413; NPV = $413.', 3)],
  evaluate=[('NPV is the best method of investment appraisal.', ['includes time value of money', 'considers all cash flows', 'gives a clear decision rule'],
             ['relies on uncertain forecasts and discount rate', 'harder to understand', 'ignores qualitative factors', 'does not show payback or liquidity'], 'NPV is the most theoretically sound method, but firms should combine it with payback, sensitivity analysis and qualitative factors.')],
  )


# =============================================================================================
# ch14 Unit 3.9 Budgets and business management tools
# =============================================================================================
@calc('ch14-st1', 'C3', (1, 4))
def profit_centres(rng, slot):
    f_ = rng.choice(['a hotel', 'a department store', 'a sports centre', 'a garden centre'])
    c = cur(rng)
    centres = {'a hotel': ['rooms', 'restaurant', 'spa'], 'a department store': ['clothing', 'electronics', 'café'],
               'a sports centre': ['gym', 'swimming pool', 'tennis courts'], 'a garden centre': ['plants', 'tools', 'café']}[f_]
    rev = [rng.choice([40, 60, 80, 120, 200]) * 1000 for _ in centres]
    cost = [int(r * rng.choice([0.6, 0.8, 0.95, 1.1])) for r in rev]
    pr = [r - k for r, k in zip(rev, cost)]
    rows = '; '.join(f'{n}: revenue {m(r, c)}, direct costs {m(k, c)}' for n, r, k in zip(centres, rev, cost))
    worst = centres[pr.index(min(pr))]
    return dict(stem=f'The managers of {f_} treat each department as a profit centre. Last quarter: {rows}. Calculate the profit of each profit centre and the total, and explain one reason why the business might keep the weakest centre ({worst}) open.',
                answer='; '.join(f'{n} {m(p, c)}' for n, p in zip(centres, pr)) + f'; total {m(sum(pr), c)}. Reason: it may attract customers who spend in other centres, cover some overheads (contribution), or be seasonal.',
                markingKey=MK('Profit = revenue − costs for each centre.', 'all profits and total') + ' [R1] reason.', marks=4)


S('ch14-st1', concepts=('change', 'ethics'),
  terms=[('budget', 'a financial plan of expected revenues and costs for a future period, used to set targets and control spending'),
         ('cost centre', 'a part of a business to which costs can be allocated, such as a department or product line'),
         ('profit centre', 'a part of a business to which both costs and revenues can be allocated, so its profit can be calculated'),
         ('budget holder', 'the manager responsible for meeting a budget'),
         ('zero-based budgeting', 'a method of budgeting in which every item must be justified from zero each period, rather than based on last year\'s budget')],
  facts=[('A school\'s IT department, which incurs costs but earns no revenue, is best described as a:', 'cost centre', ['profit centre', 'revenue stream', 'variance'], 'Only costs can be allocated.'),
         ('Which is a purpose of budgeting?', 'Setting targets and controlling spending', ['Calculating depreciation', 'Recording past transactions only', 'Paying dividends'], 'Planning and control.'),
         ('Each store of a retail chain, with its own sales and costs, can be treated as a:', 'profit centre', ['cost centre only', 'budget holder', 'variance'], 'Revenue and costs allocated.')],
  why=[('Explain why budgets can improve control in a business.', 'Managers can compare actual results with planned figures, identify variances, and take corrective action, and budget holders are accountable for their spending.'),
       ('Explain why dividing a business into profit centres can motivate managers.', 'Managers are responsible for their own centre\'s results, which gives them clear targets, autonomy and recognition when they perform well.'),
       ('Explain why budgets can sometimes demotivate employees.', 'If budgets are imposed without consultation or set unrealistically, staff may feel they cannot meet targets; inflexible budgets can also prevent sensible spending.')],
  contrast=[('a cost centre', 'a profit centre', 'A cost centre is a part of the business to which only costs are allocated; a profit centre has both costs and revenues allocated, so its profit can be measured.')],
  misc=[('Budgets are only useful for the finance department.', 'Budgets coordinate all departments, set targets for marketing, operations and HR, and help allocate resources across the business.')],
  cases=[('Unilever\'s cost-saving programme', 'Unilever adopted zero-based budgeting from 2015, aiming to save about €2 bn over three years by justifying spending from scratch.', 'budgeting methods', 'requiring every cost to be justified can cut waste but is time-consuming and may discourage innovation'),
         ('departments in a hospital', 'In many public hospitals each department (radiology, surgery, A&E) is a cost centre with its own budget.', 'cost centres', 'allocating costs to departments improves accountability but can make departments reluctant to share resources')],
  apply=[('A university decides to treat its catering outlets as profit centres and its library as a cost centre. Explain why the library cannot easily be a profit centre and one benefit of making catering a profit centre.', 'The library does not earn revenue directly from users, so profit cannot be measured; making catering a profit centre gives managers responsibility for revenue and costs, encouraging efficiency.', 3)],
  evaluate=[('Profit and cost centres always improve the performance of a business.', ['accountability and control', 'motivation of managers', 'identify unprofitable areas'],
             ['allocating overheads can be arbitrary', 'competition between centres harms cooperation', 'short-term focus', 'administrative cost'], 'They improve control when costs can be allocated fairly, but can create conflict and arbitrary decisions if overheads are hard to divide.')],
  )


@calc('ch14-st2', 'C3', (1, 5))
def variance(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    items = [('sales revenue', 'rev'), ('raw materials', 'cost'), ('wages', 'cost'), ('marketing', 'cost'), ('rent', 'cost')]
    rows = []
    for nm_, kind in items:
        b = (rng.choice([300, 360, 400, 480, 500]) if kind == 'rev' else rng.choice([10, 20, 25, 40, 60])) * 1000
        a = int(b * rng.choice([0.85, 0.9, 0.95, 1.05, 1.1, 1.2]))
        v = a - b
        fav = (v > 0) if kind == 'rev' else (v < 0)
        rows.append((nm_, b, a, abs(v), 'favourable' if fav else ('adverse' if v != 0 else 'none')))
    tab = '; '.join(f'{nm_}: budget {m(b, c)}, actual {m(a, c)}' for nm_, b, a, _, _ in rows)
    if slot.d <= 2:
        nm_, b, a, v, k = rows[rng.randrange(5)]
        return dict(stem=f'At {f_}, the budget for {nm_} was {m(b, c)} and the actual figure was {m(a, c)}. Calculate the variance and state whether it is favourable or adverse.',
                    answer=f'Variance = {m(v, c)} {k}', markingKey=MK(f'|{a:,} − {b:,}| = {v:,}; ' + ('higher revenue is favourable' if nm_ == 'sales revenue' else 'higher cost is adverse, lower cost favourable') + '.', f'{m(v, c)} {k}'), marks=2)
    bp = rows[0][1] - sum(r[1] for r in rows[1:])
    ap = rows[0][2] - sum(r[2] for r in rows[1:])
    pv = ap - bp
    return dict(stem=f'{f_}\'s budget and actual results for the quarter were: {tab}. Calculate the variance for each item, stating whether each is favourable or adverse, and the profit variance. ' + ('Suggest two possible reasons for the variances.' if slot.d >= 4 else ''),
                answer='; '.join(f'{nm_} {m(v, c)} {k}' for nm_, _, _, v, k in rows) + f'. Budgeted profit {m(bp, c)}, actual profit {m(ap, c)}: profit variance {m(abs(pv), c)} {"favourable" if pv > 0 else "adverse" if pv < 0 else "(none)"}.' + (' Possible reasons: changes in demand or prices, supplier price changes, overtime, unplanned marketing campaigns, inaccurate budgets.' if slot.d >= 4 else ''),
                markingKey=MK('Variance = actual − budget; revenue above budget and costs below budget are favourable.', 'all variances and the profit variance') + (' [R1][R1] reasons.' if slot.d >= 4 else ''), marks=4 if slot.d <= 3 else 6)


S('ch14-st2', concepts=('change', 'ethics'),
  terms=[('variance', 'the difference between a budgeted (planned) figure and the actual figure'),
         ('favourable variance', 'a variance that increases profit compared with the budget: revenue higher than budgeted or costs lower than budgeted'),
         ('adverse variance', 'a variance that reduces profit compared with the budget: revenue lower than budgeted or costs higher than budgeted'),
         ('variance analysis', 'the process of calculating and investigating variances to understand performance and take corrective action')],
  facts=[('Budgeted wages were $50,000 and actual wages were $54,000. The variance is:', '$4,000 adverse', ['$4,000 favourable', '$104,000 adverse', '$54,000 adverse'], 'Higher cost reduces profit.'),
         ('Actual sales revenue of $95,000 against a budget of $90,000 is a:', '$5,000 favourable variance', ['$5,000 adverse variance', '$185,000 variance', 'no variance'], 'Higher revenue increases profit.'),
         ('A favourable variance in raw material costs could be caused by:', 'a supplier offering a discount', ['higher wastage', 'a rise in world commodity prices', 'more units produced than planned at the same price'], 'Lower cost than budgeted.')],
  why=[('Explain why a favourable variance is not always good news for a business.', 'Lower costs might come from cheaper, lower-quality materials or cuts in training and maintenance that harm future performance; higher revenue may come with higher costs.'),
       ('Explain why variance analysis helps managers.', 'It shows where actual results differ from plans, so managers can investigate causes, take corrective action and improve future budgets.'),
       ('Explain why an adverse cost variance may be acceptable.', 'If output and sales were higher than planned, total variable costs would naturally exceed budget; the extra revenue may more than offset the higher costs.')],
  contrast=[('a favourable variance', 'an adverse variance', 'A favourable variance increases profit relative to budget (higher revenue or lower costs); an adverse variance reduces it (lower revenue or higher costs).')],
  misc=[('An adverse variance always means the manager has performed badly.', 'It may be caused by external factors (price rises, exchange rates), unrealistic budgets or higher output; the cause must be investigated.')],
  cases=[('European manufacturers\' energy bills in 2022', 'Many European manufacturers reported large adverse energy cost variances in 2022 as gas and electricity prices rose far above budget after Russia\'s invasion of Ukraine.', 'adverse variances', 'external shocks can create adverse variances that managers cannot control'),
         ('a blockbuster film release', 'Universal\'s "Oppenheimer" (2023) cost about $100 m to make and earned over $950 m worldwide, far above early projections.', 'favourable variances', 'revenue far above budget created a large favourable variance')],
  apply=[('A café budgeted for revenue of $30,000 and costs of $24,000 for July. Actual revenue was $27,000 and costs were $23,000. Calculate the variances and the profit variance.', 'Revenue $3,000 adverse; costs $1,000 favourable; budgeted profit $6,000, actual $4,000, so profit variance $2,000 adverse.', 3)],
  evaluate=[('Variance analysis is an effective way to control a business.', ['identifies problems quickly', 'accountability of budget holders', 'improves planning'],
             ['budgets may be unrealistic', 'variances may be outside managers\' control', 'focus on short-term numbers', 'costly to monitor'], 'Variance analysis is effective when budgets are realistic and causes are investigated, rather than used only to blame managers.')],
  )


@calc('ch14-st3', 'C3', (2, 5))
def decision_tree(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    oa, ob = rng.choice([('launch a new product range', 'expand into a new region'), ('open a flagship store', 'invest in e-commerce'),
                         ('buy a new machine', 'outsource production'), ('advertise on TV', 'run a social media campaign')])
    costA, costB = rng.choice([50, 80, 100]) * 1000, rng.choice([30, 60, 90]) * 1000
    pA = rng.choice([0.4, 0.5, 0.6, 0.7])
    pB = rng.choice([0.3, 0.5, 0.6, 0.8])
    hiA, loA = rng.choice([200, 250, 300]) * 1000, rng.choice([40, 60, 80]) * 1000
    hiB, loB = rng.choice([150, 180, 220]) * 1000, rng.choice([50, 70, 90]) * 1000
    evA = pA * hiA + (1 - pA) * loA
    evB = pB * hiB + (1 - pB) * loB
    nA, nB = evA - costA, evB - costB
    best = oa if nA > nB else ob
    stem = (f'{f_} must choose whether to {oa} (cost {m(costA, c)}) or {ob} (cost {m(costB, c)}). If it chooses to {oa}, there is a {int(pA * 100)}% chance of success with returns of {m(hiA, c)} and a {int(round((1 - pA) * 100))}% chance of returns of {m(loA, c)}. '
            f'If it chooses to {ob}, there is a {int(pB * 100)}% chance of returns of {m(hiB, c)} and a {int(round((1 - pB) * 100))}% chance of {m(loB, c)}. ')
    if slot.d <= 3:
        return dict(stem=stem + 'Calculate the expected value of each option, net of its cost, and state which option is preferred.',
                    answer=f'{cap(oa)}: EV = {m(evA, c)}, net {m(nA, c)}; {ob}: EV = {m(evB, c)}, net {m(nB, c)}. Preferred: {best}.',
                    markingKey=MK(f'EV = Σ(probability × outcome): {pA} × {hiA:,} + {1 - pA:.1f} × {loA:,} = {evA:,.0f}; {pB} × {hiB:,} + {1 - pB:.1f} × {loB:,} = {evB:,.0f}; subtract costs.', 'both net EVs'), marks=4)
    return dict(stem=stem + 'Construct a decision tree, calculate the expected net returns of each option and recommend which option to choose, explaining one limitation of decision trees.',
                answer=f'Decision node with two branches; chance nodes with probabilities. Net EV: {oa} {m(nA, c)}; {ob} {m(nB, c)}. Recommend {best} on financial grounds. Limitation: probabilities and outcomes are estimates; ignores risk attitudes and qualitative factors.',
                markingKey=MK(f'Tree drawn with decision (square) and chance (circle) nodes; EVs {evA:,.0f} and {evB:,.0f}; net {nA:,.0f} and {nB:,.0f}.', 'both net EVs') + ' [1] correct tree; [R1] recommendation; [R1] limitation.', marks=6)


@calc('ch14-st3', 'C3', (1, 4))
def force_field(rng, slot):
    f_ = firm(rng)
    change = rng.choice(['introducing a four-day working week', 'replacing paper systems with cloud software', 'moving production to a new automated plant', 'switching to 100% recycled packaging'])
    drv = rng.sample([('lower long-term costs', 4), ('customer demand', 3), ('competitor pressure', 4), ('staff support', 2), ('government incentives', 3), ('brand image', 3)], 3)
    res = rng.sample([('cost of change', 4), ('staff fear of job losses', 3), ('lack of skills', 3), ('disruption to production', 2), ('union opposition', 4), ('uncertain returns', 3)], 3)
    d = sum(v for _, v in drv)
    r = sum(v for _, v in res)
    return dict(stem=f'{f_} is considering {change}. A force field analysis scores driving forces – ' + ', '.join(f'{n} ({v})' for n, v in drv) + ' – and restraining forces – ' + ', '.join(f'{n} ({v})' for n, v in res) + ' (scores out of 5). Calculate the total for each side and state what the analysis suggests. Suggest one way to reduce the strongest restraining force.',
                answer=f'Driving forces = {d}; restraining forces = {r}. ' + ('Driving forces are stronger, so the change is likely to succeed.' if d > r else 'Restraining forces are at least as strong, so the change is unlikely to succeed without action.') + f' Strongest restraint: {max(res, key=lambda x: x[1])[0]} – reduce it through consultation, training or phased implementation.',
                markingKey=f'[1] driving total {d}; [1] restraining total {r}; [1] conclusion; [1] relevant way to reduce the strongest restraining force.', marks=4)


S('ch14-st3', concepts=('change', 'creativity'),
  terms=[('decision tree', 'a business management tool that sets out the options, possible outcomes, probabilities and financial results of a decision, to calculate expected values'),
         ('expected value', 'the weighted average outcome of a decision: the sum of each outcome multiplied by its probability'),
         ('decision node', 'a point in a decision tree, shown by a square, where a choice must be made between options'),
         ('chance node', 'a point in a decision tree, shown by a circle, where different outcomes are possible with given probabilities'),
         ('force field analysis', 'a tool developed by Kurt Lewin that weighs the driving forces for a change against the restraining forces against it'),
         ('driving forces', 'factors that push an organization towards a change'),
         ('restraining forces', 'factors that resist or hinder a change')],
  facts=[('In a decision tree, a square represents:', 'a decision node', ['a chance node', 'an outcome', 'a probability'], 'Squares are decisions; circles are chance events.'),
         ('An option has a 60% chance of $100,000 and a 40% chance of $20,000. Its expected value is:', '$68,000', ['$60,000', '$120,000', '$80,000'], '0.6 × 100,000 + 0.4 × 20,000.'),
         ('Force field analysis was developed by:', 'Kurt Lewin', ['Henri Fayol', 'Frederick Taylor', 'Igor Ansoff'], 'Lewin\'s model of change.'),
         ('In force field analysis, staff fear of job losses would be a:', 'restraining force', ['driving force', 'chance node', 'favourable variance'], 'It resists change.')],
  why=[('Explain why decision trees help managers make decisions.', 'They set out options and outcomes clearly, force managers to estimate probabilities and returns, and allow expected values to be compared quantitatively.'),
       ('Explain why the results of a decision tree may be unreliable.', 'Probabilities and financial outcomes are estimates that may be biased or wrong, and the tree ignores qualitative factors and managers\' attitudes to risk.'),
       ('Explain why force field analysis can help a business manage change.', 'It identifies and weighs the forces for and against change, helping managers decide whether to proceed and how to strengthen drivers or reduce resistance.')],
  contrast=[('a decision node', 'a chance node', 'A decision node (square) is where managers choose between options; a chance node (circle) is where outcomes depend on probabilities beyond managers\' control.'),
            ('a decision tree', 'force field analysis', 'A decision tree compares options quantitatively using probabilities and expected values; force field analysis weighs qualitative and quantitative forces for and against a single change.')],
  misc=[('The option with the highest expected value will always produce the highest return.', 'Expected value is a probability-weighted average; the actual outcome could be the low-return branch.')],
  cases=[('Netflix\'s decision to stream', 'In 2007 Netflix began streaming while still dominant in DVD rentals, a decision with uncertain outcomes and high costs.', 'decision-making under uncertainty', 'a decision tree could compare expected returns of staying with DVDs or investing in streaming, although probabilities were hard to estimate'),
         ('a four-day week trial in the UK', 'In 2022, 61 UK companies trialled a four-day week; 56 continued afterwards, reporting stable revenue and lower staff turnover.', 'force field analysis', 'driving forces (well-being, recruitment) outweighed restraining forces (customer cover, workload) for most firms')],
  apply=[('A firm can launch a product at a cost of $40,000. There is a 0.7 chance of earning $90,000 and a 0.3 chance of earning $20,000. Calculate the expected net return and state whether it should launch.', 'EV = 0.7 × 90,000 + 0.3 × 20,000 = 63,000 + 6,000 = $69,000; net = $29,000 > 0, so launch on financial grounds.', 3)],
  evaluate=[('Decision trees are a reliable tool for making business decisions.', ['clear structure', 'quantitative comparison', 'encourage consideration of risk'],
             ['probabilities are subjective estimates', 'ignore qualitative factors', 'may oversimplify', 'risk attitudes not considered'], 'Decision trees improve decision-making discipline, but their results are only as good as the estimates and should be combined with qualitative judgement.')],
  )


# --- extra application items and cases for thinner C3 cells ---
more('ch02-st2',
     apply=[('Priya and Sam run a partnership with business debts of $90,000 and business assets of only $50,000. Explain what unlimited liability means for them and suggest one way they could reduce this risk.', 'The $40,000 shortfall must be paid from the partners\' personal assets (savings, homes), and each partner may be liable for the whole amount. They could convert to a privately held company (or limited liability partnership) so that liability is limited to the capital invested.', 4),
            ('A family-owned privately held company wants $200 million for global expansion. Analyse one advantage and one disadvantage of an IPO for the family.', 'Advantage: an IPO raises large-scale permanent capital without interest, and shares become tradable. Disadvantage: the family dilutes ownership and may lose control, faces disclosure requirements and short-term pressure from shareholders, and risks a hostile takeover.', 4)],
     cases=[('Birkenstock\'s IPO in 2023', 'Sandal maker Birkenstock, controlled by private equity firm L Catterton, listed on the New York Stock Exchange in October 2023 at a valuation of about $7.5 bn; its shares fell on the first day.', 'publicly held companies and IPOs', 'the listing raised finance and let existing owners sell shares, but exposed the firm to market sentiment and scrutiny')])

more('ch04-st1',
     apply=[('A city plans to build a new airport runway. Identify two internal and two external stakeholders and explain one interest of each group.', 'Internal: employees (job security, overtime) and managers (growth, bonuses). External: local residents (noise and pollution, property values) and the government (economic growth, emissions targets). Any valid stakeholders with clear interests.', 4),
            ('A garment supplier in Bangladesh supplies a European retailer. Explain why the retailer\'s shareholders and the supplier\'s workers may have different interests.', 'Shareholders want low costs and high profits/dividends; workers want higher wages and safe conditions, which raise costs. Pressure to cut prices can therefore conflict with workers\' welfare (e.g. the 2013 Rana Plaza collapse).', 4)],
     cases=[('Rana Plaza and fashion retailers', 'In 2013 the Rana Plaza factory complex in Bangladesh collapsed, killing over 1,100 garment workers who made clothes for Western brands.', 'stakeholder interests', 'pressure for low costs from customers and shareholders ignored the interests of workers, leading to reforms such as the Bangladesh Accord')])

more('ch04-st2',
     apply=[('A mining company wants to open a new lithium mine. Local residents fear water pollution; the government wants jobs and tax revenue; shareholders want quick returns. Use stakeholder mapping to suggest how management should treat residents and the government.', 'Government: high power, high interest – a key player to manage closely. Residents: high interest, and their power rises with protests or legal action – keep them informed and consult them, e.g. with water-monitoring commitments. Management should prioritize the key players while reducing conflict with residents.', 6),
            ('Explain one way a business could resolve a conflict between employees demanding a pay rise and shareholders wanting higher dividends.', 'For example, link pay to performance through profit-related pay, so higher pay is funded by higher profits; or negotiate a phased pay rise with productivity improvements. Compromise reduces conflict while protecting profits.', 4)],
     cases=[('Thacker Pass lithium mine', 'Lithium Americas\' Thacker Pass mine in Nevada faced lawsuits from Indigenous groups and ranchers in 2021-2023, but had US government support for electric-vehicle supply chains.', 'stakeholder conflict', 'the government\'s goals and investors\' interests clashed with local and Indigenous communities\' concerns about land and water')])

more('ch04-st3',
     apply=[('A coffee chain pays farmers a guaranteed premium price. Explain how both the chain and the farmers may benefit.', 'Farmers gain stable, higher incomes and can invest in quality; the chain secures reliable, high-quality supply and an ethical brand image that supports premium prices and customer loyalty – a mutual benefit.', 4),
            ('Explain how stakeholder interests can be aligned when a firm introduces employee share ownership.', 'Employees become part owners, so they share the shareholders\' interest in profit; this can raise motivation and productivity, which also benefits customers and shareholders.', 4)],
     cases=[('Starbucks C.A.F.E. Practices', 'Starbucks\' C.A.F.E. Practices programme sets ethical and environmental standards for coffee farmers and in return offers price premiums and long-term contracts.', 'mutual benefits of stakeholders', 'farmers gain income security and the firm gains secure, ethically sourced supply')])

more('ch05-st3',
     apply=[('A local bakery has a loyal customer base and the owner wants to keep control. Explain two reasons why the bakery may choose to stay small.', 'Small size allows personal service and flexibility, and lets the owner keep control and avoid diseconomies of scale; the local market may be too small for growth to be profitable, and growth would require finance and risk.', 4),
            ('Explain one impact of small and medium-sized enterprises on an economy.', 'SMEs create a large share of jobs (around two-thirds of private-sector employment in the EU), encourage competition and innovation, and supply larger firms, contributing to economic growth.', 2)],
     cases=[('Morgan Motor Company', 'British sports car maker Morgan builds only around 800 hand-made cars a year at its Malvern factory.', 'reasons to stay small', 'small scale supports craftsmanship, exclusivity and premium prices in a niche market')])

more('ch07-st2',
     apply=[('A hospital emergency department faces a sudden major incident. Explain which leadership style is most appropriate and why.', 'An autocratic style is most appropriate: decisions must be made quickly and clearly under pressure, with clear lines of command. Consultation would waste time; afterwards a more democratic style could be used to review the response.', 4),
            ('A software start-up employs highly skilled, motivated programmers. Explain why a laissez-faire style may suit it.', 'Skilled, self-motivated staff need little supervision; freedom encourages creativity and innovation, and trusting staff raises motivation. The risk is a lack of direction or coordination.', 4)],
     cases=[('Satya Nadella at Microsoft', 'Since becoming CEO in 2014, Satya Nadella has promoted a collaborative "growth mindset" culture at Microsoft, replacing a competitive internal ranking system.', 'democratic leadership', 'a more consultative style encouraged collaboration and innovation, helping Microsoft grow in cloud computing')])

more('ch11-st1',
     apply=[('An investor is deciding whether to buy shares in a listed company. Explain why the company\'s published accounts are useful to the investor.', 'The accounts show profitability, assets and liabilities, so the investor can judge returns, the risk of failure and the likely dividends, and compare the company with rivals.', 4),
            ('Explain why a business\'s accountants must follow the principle of integrity.', 'Stakeholders such as investors, lenders and governments rely on accurate accounts; dishonest accounts mislead them, can hide fraud and destroy trust (e.g. Wirecard).', 2)],
     cases=[('Wirecard\'s accounting fraud', 'In 2020 German payments firm Wirecard admitted that €1.9 bn shown in its accounts probably did not exist, and it collapsed into insolvency.', 'principles of ethical accounting', 'false accounts misled investors, lenders and regulators, showing why integrity and objectivity matter')])


# --- extra numerical generators so every finance subtopic can serve Paper 2 calculation slots ---
@calc('ch11-st1', 'C3', (1, 5))
def dividend_retained(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    pbt = rng.choice([200, 240, 300, 360, 400, 500]) * 1000
    taxr = rng.choice([20, 25, 30])
    divp = rng.choice([30, 40, 50, 60])
    shares = rng.choice([100, 200, 250, 400, 500]) * 1000
    tx = pbt * taxr / 100
    pat = pbt - tx
    div = pat * divp / 100
    ret = pat - div
    dps = div / shares
    who = rng.choice(['shareholders', 'a potential investor', 'employees asking for a pay rise', 'a bank considering a loan'])
    stem = (f'{f_} made a profit before tax of {m(pbt, c)}. Corporation tax is {taxr}% and the directors pay out {divp}% of profit after tax as dividends. '
            f'There are {shares:,} shares. Calculate profit after tax, total dividends, retained profit and the dividend per share.')
    if slot.d >= 4:
        stem += f' Explain why this information is useful to {who}.'
    ans = f'Tax = {m(tx, c)}; profit after tax = {m(pat, c)}; dividends = {m(div, c)}; retained profit = {m(ret, c)}; dividend per share = {c}{p2(dps)}.'
    if slot.d >= 4:
        ans += f' Use to {who}: the figures show the return paid out and the profit kept for reinvestment, helping them judge performance, risk and future growth.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'{pbt:,} × {taxr}% = {tx:,.0f}; {pbt:,} − {tx:,.0f} = {pat:,.0f}; {divp}% × {pat:,.0f} = {div:,.0f}; {pat:,.0f} − {div:,.0f} = {ret:,.0f}; {div:,.0f}/{shares:,} = {p2(dps)}.', 'all four values') + (' [2] explanation applied to the stakeholder.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


@calc('ch12-st4', 'C3', (1, 5))
def insolvency_check(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    cash = rng.choice([5, 8, 10, 12, 15]) * 1000
    rec = rng.choice([10, 20, 25, 30]) * 1000
    inv = rng.choice([30, 40, 60, 80]) * 1000
    pay = rng.choice([30, 40, 50, 60]) * 1000
    od = rng.choice([10, 15, 20, 25]) * 1000
    cl = pay + od
    ca = cash + rec + inv
    cr = ca / cl
    at = (ca - inv) / cl
    stem = (f'{f_} has cash of {m(cash, c)}, trade receivables of {m(rec, c)}, inventories of {m(inv, c)}, trade payables of {m(pay, c)} and a bank overdraft of {m(od, c)}, all due within 30 days. '
            'Calculate the current ratio and the acid-test ratio, and comment on the risk that the business becomes insolvent.')
    if slot.d >= 4:
        stem += ' Suggest two actions it could take to reduce this risk.'
    risk = ('Liquid assets do not cover current liabilities, so it may be unable to pay its debts as they fall due unless it sells stock quickly – a real risk of insolvency.' if at < 1
            else 'Liquid assets cover current liabilities, so the short-term risk of insolvency is low.')
    ans = f'Current ratio = {ca:,}/{cl:,} = {p2(cr)}:1; acid-test = {ca - inv:,}/{cl:,} = {p2(at)}:1. {risk}'
    if slot.d >= 4:
        ans += ' Actions: chase debtors or use debt factoring, sell surplus stock at a discount, negotiate longer credit with suppliers, or convert the overdraft into a long-term loan.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'current assets {ca:,}; current liabilities {cl:,}; ratios {p2(cr)} and {p2(at)}.', 'both ratios') + ' [1] comment on insolvency risk.' + (' [1][1] actions.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


@calc('ch13-st1', 'C3', (1, 5))
def profit_vs_cash(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    sales = rng.choice([80, 100, 120, 150, 200]) * 1000
    credit = rng.choice([40, 50, 60, 75])
    costs = int(sales * rng.choice([0.7, 0.75, 0.8, 0.85]))
    paid_pct = rng.choice([70, 80, 90, 100])
    equip = rng.choice([0, 10, 20, 30]) * 1000
    profit = sales - costs
    cash_in = sales * (100 - credit) / 100
    cash_out = costs * paid_pct / 100 + equip
    ncf = cash_in - cash_out
    eq = f' It also paid {m(equip, c)} in cash for new equipment (a capital item, not counted as a cost in this month\'s profit).' if equip else ''
    stem = (f'In its first month {f_} made sales of {m(sales, c)}, of which {credit}% were on 60-day credit. Its costs for the month were {m(costs, c)}, '
            f'of which it paid {paid_pct}% in cash during the month.{eq} Calculate the profit for the month and the net cash flow, and explain why they differ.')
    ans = (f'Profit = {m(sales, c)} − {m(costs, c)} = {m(profit, c)}. Cash in = {m(cash_in, c)}; cash out = {m(cash_out, c)}; net cash flow = {m(ncf, c)}. '
           'They differ because credit sales count as revenue before the cash is received, unpaid costs are not yet cash outflows'
           + (', and the equipment is a cash outflow but not a cost in the profit calculation.' if equip else '.'))
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'profit {sales:,} − {costs:,} = {profit:,}; cash in {100 - credit}% × {sales:,} = {cash_in:,.0f}; cash out {paid_pct}% × {costs:,}' + (f' + {equip:,}' if equip else '') + f' = {cash_out:,.0f}; net {ncf:,.0f}.', 'profit and net cash flow') + ' [1] explanation of the difference (timing of receipts and payments).',
                marks=4 if slot.d <= 3 else 6)
