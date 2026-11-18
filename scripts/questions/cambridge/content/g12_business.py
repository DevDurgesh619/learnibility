"""Cambridge International A Level Business 9609, A Level extension content (grade 12), 17 chapters.

Paper 3 (Business Decision-Making, case study) and Paper 4 (Business Strategy) style items.
Each topic is built from a data spec (definitions, MCQs, explain items, case-application frames,
evaluation frames) by `T()`, which registers generic case-study templates; quantitative topics add
parameterised calculation templates with computed answers. Case contexts come from CASES.
"""
import math
from ._lib import topic, mcq, compose, sf, near, num_mcq, CTX

PROFILE = {'mark_scale': {'long': (3, 2.5), 'case': (2, 2)}, 'wordy': True}
CHAPTERS = {}

# =====================================================================================
# Case bank: fictional international businesses
# =====================================================================================

CASES = [
    dict(b='Savanna Fresh', full='Savanna Fresh Ltd', form='private limited company', country='Kenya', city='Nairobi', cur='Kenyan shilling',
         sector='horticulture', does='grows cut flowers and green beans and exports them by air to supermarkets in Europe', emp=850,
         prod='cut flowers and green beans', newprod='ready-to-eat salad packs', newmkt='the Gulf states',
         sit='Its largest European customer has just demanded lower prices and proof of sustainable water use.'),
    dict(b='Andes Textil', full='Andes Textil SA', form='family-owned private company', country='Peru', city='Lima', cur='Peruvian sol',
         sector='textile manufacturing', does='makes premium alpaca knitwear for fashion retailers in North America and Japan', emp=320,
         prod='alpaca knitwear', newprod='a range of alpaca home furnishings', newmkt='China',
         sit='The founder is retiring and the new managing director wants to modernise production.'),
    dict(b='Lumen Robotics', full='Lumen Robotics plc', form='public limited company', country='Singapore', city='Singapore', cur='Singapore dollar',
         sector='industrial engineering', does='designs and builds robots used on factory assembly lines', emp=2400,
         prod='industrial robots', newprod='robots for hospital logistics', newmkt='India',
         sit='Shareholders are pressing for higher dividends while engineers want more spending on research.'),
    dict(b='Desert Bloom', full='Desert Bloom Hotels plc', form='public limited company', country='the United Arab Emirates', city='Dubai', cur='UAE dirham',
         sector='hospitality', does='operates fourteen four- and five-star hotels', emp=3100,
         prod='hotel rooms and conference facilities', newprod='serviced apartments for long-stay guests', newmkt='Saudi Arabia',
         sit='Occupancy rates have fallen since two new rival hotels opened nearby.'),
    dict(b='Cape Brew', full='Cape Brew Co. (Pty) Ltd', form='private limited company', country='South Africa', city='Cape Town', cur='South African rand',
         sector='beverages', does='brews craft beers and low-sugar soft drinks sold through bars and supermarkets', emp=140,
         prod='craft beer and soft drinks', newprod='alcohol-free craft beer', newmkt='Namibia and Botswana',
         sit='Demand has grown faster than its small brewery can produce.'),
    dict(b='Tejo Mobility', full='Tejo Mobility SA', form='public limited company', country='Portugal', city='Lisbon', cur='euro',
         sector='vehicle manufacturing', does='assembles electric scooters and e-bikes for sale across the European Union', emp=600,
         prod='electric scooters and e-bikes', newprod='electric cargo bikes for delivery firms', newmkt='Brazil',
         sit='Battery supply problems from Asia have delayed several large orders.'),
    dict(b='BatikPay', full='BatikPay Sdn Bhd', form='private limited company', country='Malaysia', city='Kuala Lumpur', cur='Malaysian ringgit',
         sector='financial technology', does='runs a mobile payments app used by 4 million customers and 90 000 small shops', emp=210,
         prod='mobile payment services', newprod='small loans for app users', newmkt='Indonesia',
         sit='The central bank has announced tighter rules on data protection for payment apps.'),
    dict(b='Café Cordillera', full='Café Cordillera SAS', form='private limited company', country='Colombia', city='Bogotá', cur='Colombian peso',
         sector='food and drink retail', does='roasts coffee and runs a chain of 60 cafés', emp=900,
         prod='roasted coffee and café meals', newprod='bottled cold-brew coffee for supermarkets', newmkt='Mexico',
         sit='The owners want to double the number of cafés within three years.'),
    dict(b='Nile Pharma', full='Nile Pharma plc', form='public limited company', country='Egypt', city='Cairo', cur='Egyptian pound',
         sector='pharmaceuticals', does='manufactures generic medicines for hospitals and pharmacies in Africa and the Middle East', emp=1800,
         prod='generic medicines', newprod='over-the-counter vitamin supplements', newmkt='East Africa',
         sit='Most of its raw ingredients are imported and paid for in US dollars.'),
    dict(b='Mekong Furniture', full='Mekong Furniture JSC', form='joint stock company', country='Vietnam', city='Hanoi', cur='Vietnamese dong',
         sector='furniture manufacturing', does='makes wooden and rattan furniture for large retailers in the USA and Europe', emp=1200,
         prod='wooden furniture', newprod='flat-pack furniture sold online', newmkt='Australia',
         sit='A major US retailer has asked it to cut delivery times from twelve weeks to six.'),
    dict(b='Lagos Bites', full='Lagos Bites Ltd', form='private limited company', country='Nigeria', city='Lagos', cur='Nigerian naira',
         sector='food processing', does='produces packaged snacks such as plantain chips and chin chin', emp=700,
         prod='packaged snacks', newprod='healthy breakfast cereals', newmkt='Ghana and Senegal',
         sit='Rising costs of imported packaging have cut its profit margins.'),
    dict(b='Pearl Logistics', full='Pearl Logistics WLL', form='private limited company', country='Qatar', city='Doha', cur='Qatari riyal',
         sector='logistics', does='provides freight forwarding, warehousing and lorry delivery services', emp=1500,
         prod='freight and warehousing services', newprod='temperature-controlled storage for food and medicines', newmkt='Oman',
         sit='Large customers are asking for real-time tracking of every delivery.'),
    dict(b='Nusantara Apparel', full='Nusantara Apparel Tbk', form='public limited company', country='Indonesia', city='Jakarta', cur='Indonesian rupiah',
         sector='clothing manufacturing', does='makes sportswear under contract for global brands', emp=4000,
         prod='sportswear', newprod='its own brand of affordable sportswear', newmkt='the Philippines',
         sit='A global brand has threatened to cancel its contract after a report on long working hours.'),
    dict(b='IslaConnect', full='IslaConnect Inc.', form='private limited company', country='the Philippines', city='Manila', cur='Philippine peso',
         sector='business process outsourcing', does='runs customer-service call centres for banks and airlines in the USA and Australia', emp=2600,
         prod='call-centre and back-office services', newprod='AI chatbot services', newmkt='Canada',
         sit='Clients are starting to replace human call handlers with artificial intelligence.'),
    dict(b='Indus Sports', full='Indus Sports Goods Ltd', form='private limited company', country='Pakistan', city='Karachi', cur='Pakistani rupee',
         sector='sports equipment manufacturing', does='makes hand-stitched and machine-stitched footballs and cricket equipment', emp=950,
         prod='footballs and cricket equipment', newprod='smart footballs with built-in sensors', newmkt='West Africa',
         sit='A rival in China has started selling machine-made balls at lower prices.'),
    dict(b='Andina Solar', full='Andina Solar SpA', form='private limited company', country='Chile', city='Santiago', cur='Chilean peso',
         sector='renewable energy', does='designs and installs solar power systems for farms, mines and homes', emp=380,
         prod='solar installations', newprod='battery storage systems', newmkt='Peru',
         sit='The government has announced new subsidies for business investment in renewable energy.'),
    dict(b='Gold Coast Cocoa', full='Gold Coast Cocoa Ltd', form='private limited company', country='Ghana', city='Accra', cur='Ghanaian cedi',
         sector='confectionery', does='buys cocoa from local co-operatives and makes premium chocolate bars', emp=450,
         prod='chocolate bars', newprod='cocoa-based beauty products', newmkt='the United Kingdom',
         sit='World cocoa prices have doubled in eighteen months.'),
    dict(b='Lanka Tea', full='Lanka Tea Estates plc', form='public limited company', country='Sri Lanka', city='Colombo', cur='Sri Lankan rupee',
         sector='agriculture and food', does='grows, processes and packs tea on its own estates', emp=5000,
         prod='packaged tea', newprod='ready-to-drink iced tea', newmkt='Russia',
         sit='Many young workers are leaving the estates for jobs in the cities.'),
    dict(b='Kiwi Trails', full='Kiwi Trails Ltd', form='private limited company', country='New Zealand', city='Auckland', cur='New Zealand dollar',
         sector='tourism', does='runs guided hiking, kayaking and cycling tours', emp=90,
         prod='adventure tours', newprod='corporate team-building retreats', newmkt='Japan',
         sit='Bookings are highly seasonal and most guides are employed only for the summer.'),
    dict(b='Maple Learning', full='Maple Learning Inc.', form='private limited company', country='Canada', city='Toronto', cur='Canadian dollar',
         sector='education technology', does='runs an online tutoring and test-preparation platform for school students', emp=260,
         prod='online tutoring subscriptions', newprod='a teacher-training platform for schools', newmkt='Latin America',
         sit='Venture capital investors expect it to become profitable within two years.'),
    dict(b='Iberia Moda', full='Iberia Moda SA', form='public limited company', country='Spain', city='Madrid', cur='euro',
         sector='clothing retail', does='runs 180 fast-fashion clothing stores and an online shop', emp=6000,
         prod='fast-fashion clothing', newprod='a second-hand clothing resale service', newmkt='Morocco',
         sit='Online sales are growing quickly while sales in its high-street stores are falling.'),
    dict(b='Bosphorus Home', full='Bosphorus Home AŞ', form='public limited company', country='Turkey', city='Istanbul', cur='Turkish lira',
         sector='household appliance manufacturing', does='makes washing machines, fridges and ovens sold in Europe and the Middle East', emp=3500,
         prod='household appliances', newprod='energy-efficient heat pumps', newmkt='Egypt',
         sit='Inflation in Turkey has been above 40% for two years.'),
    dict(b='Siam Ready Meals', full='Siam Ready Meals Co. Ltd', form='private limited company', country='Thailand', city='Bangkok', cur='Thai baht',
         sector='food manufacturing', does='produces chilled and frozen ready meals for supermarkets and convenience stores', emp=1100,
         prod='ready meals', newprod='plant-based ready meals', newmkt='South Korea',
         sit='Its biggest customer, a convenience-store chain, wants deliveries twice a day.'),
    dict(b='Deccan Auto', full='Deccan Auto Components Ltd', form='public limited company', country='India', city='Mumbai', cur='Indian rupee',
         sector='automotive components', does='supplies brakes and steering parts to car manufacturers', emp=2200,
         prod='brake and steering components', newprod='components for electric vehicles', newmkt='Mexico',
         sit='Its car-maker customers are switching rapidly to electric vehicles.'),
    dict(b='Han River Games', full='Han River Games Co.', form='private limited company', country='South Korea', city='Seoul', cur='South Korean won',
         sector='video game development', does='develops mobile games that earn revenue from in-game purchases', emp=340,
         prod='mobile games', newprod='a subscription gaming service', newmkt='Brazil',
         sit='One game earns 70% of its revenue and its popularity is starting to fall.'),
    dict(b='Muscat Dates', full='Muscat Dates & Co. LLC', form='family-owned limited company', country='Oman', city='Muscat', cur='Omani rial',
         sector='food processing', does='processes, packs and exports dates and date syrup', emp=160,
         prod='packed dates and date syrup', newprod='date-based energy bars', newmkt='Europe',
         sit='Three family members disagree about whether to sell shares to an outside investor.'),
]

FX = {'Kenyan shilling': 130, 'Peruvian sol': 3.8, 'Singapore dollar': 1.35, 'UAE dirham': 3.67, 'South African rand': 18, 'euro': 0.92, 'Malaysian ringgit': 4.5, 'Colombian peso': 4000, 'Egyptian pound': 48, 'Vietnamese dong': 25000, 'Nigerian naira': 1500, 'Qatari riyal': 3.64, 'Indonesian rupiah': 16000, 'Philippine peso': 57, 'Pakistani rupee': 280, 'Chilean peso': 950, 'Ghanaian cedi': 15, 'Sri Lankan rupee': 300, 'New Zealand dollar': 1.65, 'Canadian dollar': 1.37, 'Turkish lira': 34, 'Thai baht': 35, 'Indian rupee': 84, 'South Korean won': 1350, 'Omani rial': 0.385}
for _c in CASES:
    _c['fx'] = FX[_c['cur']]
    _c['bp'] = _c['b'] + ("'" if _c['b'].endswith('s') else "'s")
    _c['cs'] = _c['cur'] + 's' if not _c['cur'].endswith(('euro', 'won', 'baht', 'yen', 'rand')) else _c['cur']
    if _c['cur'] == 'euro':
        _c['cs'] = 'euros'


def fmtc(s, c):
    return s.format(**c) if '{' in s else s


def intro(r, c):
    e = f"{c['emp']:,}"
    v = r.randrange(3)
    if v == 0:
        place = c['city'] if c['city'] == c['country'] else f"{c['city']}, {c['country']}"
        return f"{c['full']} is a {c['form']} based in {place}. It {c['does']} and employs about {e} people. {c['sit']}"
    if v == 1:
        return f"Based in {c['city']}, {c['full']} ({c['form']}) {c['does']}. The business has around {e} employees. {c['sit']}"
    return f"{c['sit']} {c['full']}, a {c['form']} in {c['country']} with about {e} employees, {c['does']}."


def ctx(c):
    return f"{c['b']}: {c['sector']}, about {c['emp']:,} employees, {c['form']} in {c['country']}; {c['sit'][0].lower() + c['sit'][1:-1]}"


def cap(s):
    s = s.strip()
    return s[0].upper() + s[1:] + ('' if s.endswith('.') else '.')


def money(x, dp=0):
    neg = x < 0
    x = abs(x)
    s = f'{x:,.{dp}f}' if dp else f'{round(x):,}'
    return ('−$' if neg else '$') + s


def pct(x, dp=1):
    s = f'{x:.{dp}f}'
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s + '%'


def num(x, dp=2):
    s = f'{x:,.{dp}f}'
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s


def nearest(want, allowed, default):
    if want and want >= min(allowed) - 1:
        return min(allowed, key=lambda m: (abs(m - want), m))
    return default


AO_EV = {8: (2, 2, 2, 2), 10: (2, 2, 3, 3), 12: (2, 2, 4, 4), 16: (3, 3, 5, 5), 20: (3, 3, 6, 8)}
AO_AN = {2: (1, 1, 0), 3: (1, 1, 1), 4: (1, 1, 2), 6: (2, 2, 2), 8: (2, 2, 4)}


def key_an(m, c, pts):
    k, a, n = AO_AN[m]
    s = f"AO1 Knowledge [{k}]: {pts[0]}. AO2 Application [{a}]: answer uses the case ({ctx(c)})."
    if n:
        s += f" AO3 Analysis [{n}]: developed chains of reasoning showing the consequence for {c['b']}, e.g. {'; '.join(pts[1:4])}."
    s += f' Levels: L1 knowledge only; L2 applied to the case; L3 applied and analysed. [{m}]'
    return s


def key_ev(m, c, fo, ag, dep):
    k, a, n, e = AO_EV[m]
    return (f"AO1 Knowledge [{k}]: relevant concepts/theory. AO2 Application [{a}]: uses case evidence ({ctx(c)}). "
            f"AO3 Analysis [{n}]: arguments for, e.g. {'; '.join(fo)}; arguments against, e.g. {'; '.join(ag)}. "
            f"AO4 Evaluation [{e}]: a supported judgement that weighs the arguments, e.g. it depends on {'; '.join(dep)}. "
            f"Highest level needs a justified conclusion specific to {c['b']}, not a generic one. [{m}]")


def ans_ev(c, fo, ag, dep):
    return (f"For: {'; '.join(fo)}. Against: {'; '.join(ag)}. Judgement: the decision for {c['b']} depends mainly on {dep[0]}"
            + (f", and also on {dep[1]}" if len(dep) > 1 else '') + '.')


DEFS = {}      # chapter -> [(term, definition)]
TOPICS = []


def _frame(fr, r, c):
    """A frame is (question, points[, ...]) with {placeholders} or a callable (r, c) -> same tuple."""
    if callable(fr):
        return fr(r, c)
    return tuple(fmtc(x, c) if isinstance(x, str) else [fmtc(y, c) for y in x] for x in fr)


def T(ch, name, keys, defs=(), mcqs=(), exps=(), adv=(), anl=(), ev=()):
    """Build a topic from a content spec and register its generic templates."""
    t = topic(name, *keys)
    t.ch = ch
    t.defs, t.adv, t.anl, t.ev, t.parts = list(defs), list(adv), list(anl), list(ev), []
    t.entries = {}
    DEFS.setdefault(ch, []).extend(defs)
    CHAPTERS.setdefault(ch, []).append(t)
    TOPICS.append(t)

    # --- C1: definitions (short, 2 marks) -------------------------------------------
    for i, (term, d) in enumerate(defs):
        stem = (f"Define the term '{term}'." if i % 2 == 0 else f"What is meant by '{term}'?")
        key = f'2 marks: full definition, {d[0].lower() + d[1:]} 1 mark: partial definition or relevant example only. [2]'
        t.entries.setdefault('C1', []).append(((stem, d, key), (1, 2)))

        def fn(r, D, stem=stem, d=d, key=key):
            return {'stem': stem, 'answer': d, 'key': key, 'type': 'short', 'marks': 2}
        fn.__name__ = 'def_short'
        t.add('C1', (1, 2, 3), 'short')(fn)

    # --- C1: MCQs --------------------------------------------------------------------
    for (stem, a, dis, why) in mcqs:
        def fn(r, D, stem=stem, a=a, dis=dis, why=why):
            opts, ans = mcq(r, a, list(dis))
            return {'stem': stem, 'options': opts, 'answer': ans, 'key': f'{a}. {why}', 'marks': 1}
        fn.__name__ = 'mcq_fixed'
        t.add('C1', (1, 2), 'mcq')(fn)

    if defs:
        @t.add('C1', (1, 2), 'mcq')
        def def_mcq(r, D):
            term, d = r.choice(t.defs)
            others = [x for x in DEFS[ch] if x[0] != term]
            ds = [x[1] for x in r.sample(others, min(3, len(others)))]
            opts, ans = mcq(r, d, ds)
            return {'stem': f"Which of the following best defines '{term}'?", 'options': opts, 'answer': ans,
                    'key': f'{term}: {d}', 'marks': 1}

        @t.add('C1', (2, 3), 'mcq')
        def def_rev(r, D):
            term, d = r.choice(t.defs)
            others = [x for x in DEFS[ch] if x[0] != term]
            ds = [x[0] for x in r.sample(others, min(3, len(others)))]
            opts, ans = mcq(r, term, ds)
            return {'stem': f'Which business term is described here: "{d}"', 'options': opts, 'answer': ans,
                    'key': f'This is the definition of {term}.', 'marks': 1}

    # --- C2: explain items -------------------------------------------------------------
    for e in exps:
        t.entries.setdefault('C2', []).append((e, (2, 3)))

        def fn(r, D, e=e):
            m = int(e[2].rsplit('[', 1)[1].rstrip('].')) if '[' in e[2] else 2
            return {'stem': e[0], 'answer': e[1], 'key': e[2], 'type': 'explain', 'marks': m}
        fn.__name__ = 'exp_fixed'
        t.add('C2', (2, 3, 4), 'explain')(fn)

    # --- C2: advantage / disadvantage in context -------------------------------------
    if adv:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def adv_ex(r, D):
            c = r.choice(CASES)
            concept, pro, con = _frame(r.choice(t.adv), r, c)
            v = r.randrange(2)
            if D <= 2:
                if v == 0:
                    q, a, k = f'Explain one advantage to {c["b"]} of {concept}.', pro[0], f'1 mark: relevant advantage, e.g. {"; ".join(pro[:3])}. 1 mark: explained in the context of {c["b"]} ({c["sector"]}). [2]'
                else:
                    q, a, k = f'Explain one disadvantage to {c["b"]} of {concept}.', con[0], f'1 mark: relevant disadvantage, e.g. {"; ".join(con[:3])}. 1 mark: explained in the context of {c["b"]} ({c["sector"]}). [2]'
                m = 2
            elif D == 3:
                q = f'Explain one advantage and one disadvantage to {c["b"]} of {concept}.' if v == 0 else f'Explain two reasons why {concept} might not benefit {c["b"]}.'
                a = f'Advantage: {pro[0]}. Disadvantage: {con[0]}.' if v == 0 else f'{con[0]}; {con[1]}.'
                k = (f'For each point: 1 mark identification, 1 mark explanation applied to {c["b"]}. Advantages: {"; ".join(pro)}. Disadvantages: {"; ".join(con)}. [4]')
                m = 4
            else:
                q = (f'Explain two benefits to {c["b"]} of {concept}, using the case to support your answer.' if v == 0
                     else f'Explain why {concept} could be both an opportunity and a threat for {c["b"]}.')
                a = f'{pro[0]}; {pro[1]}.' if v == 0 else f'Opportunity: {pro[0]}. Threat: {con[0]}.'
                k = (f'2 × (1 mark point, 1 mark application to {c["b"]}: {c["sector"]}, {c["emp"]:,} employees). Points: {"; ".join(pro + con)}. [4]')
                m = 4
            a = a[0].upper() + a[1:] + ('' if a.endswith('.') else '.')
            return {'stem': intro(r, c) + ' ' + q, 'answer': a, 'key': k, 'type': 'explain', 'marks': m}

    # --- C3: analyse in the case ---------------------------------------------------------
    if anl:
        @t.add('C3', (2, 3, 4, 5), 'case')
        def anl_case(r, D):
            c = r.choice(CASES)
            q, pts = _frame(r.choice(t.anl), r, c)[:2]
            m = nearest(CTX.get('want_marks'), (4, 6, 8), {2: 4, 3: 6, 4: 8, 5: 8}[min(5, max(2, D))])
            if m == 4 and q.startswith('Analyse'):
                q = 'Explain' + q[len('Analyse'):]
            if D == 5:
                q = q.rstrip('.') + f', and judge which point is most important for {c["b"]}.'
            return {'stem': intro(r, c) + ' ' + q, 'answer': f'Points to develop for {c["b"]}: ' + '; '.join(pts) + '.',
                    'key': key_an(m, c, pts), 'type': 'case', 'marks': m}

    # --- C4: evaluate / recommend ----------------------------------------------------------
    if ev:
        @t.add('C4', (2, 3, 4, 5), 'long')
        def ev_case(r, D):
            c = r.choice(CASES)
            q, fo, ag, dep = _frame(r.choice(t.ev), r, c)
            m = nearest(CTX.get('want_marks'), (8, 10, 12, 16, 20), {2: 8, 3: 12, 4: 16, 5: 20}[min(5, max(2, D))])
            if m >= 16 and r.random() < 0.5:
                q = 'Using the case and your own knowledge, ' + q[0].lower() + q[1:]
            return {'stem': intro(r, c) + ' ' + q, 'answer': ans_ev(c, fo, ag, dep), 'key': key_ev(m, c, fo, ag, dep),
                    'type': 'long', 'marks': m}

    # --- C4: structured case question (Paper 3 style) ------------------------------------
    @t.add('C4', (2, 3, 4, 5), 'case')
    def case_comp(r, D):
        c = r.choice(CASES)
        parts = []
        if t.defs:
            term, d = r.choice(t.defs)
            parts.append(lambda r, term=term, d=d: (f"Define '{term}'.", d, '1 mark partial, 2 marks full definition [2]'))
        if t.adv:
            concept, pro, con = _frame(r.choice(t.adv), r, c)
            parts.append(lambda r, concept=concept, pro=pro: (f'Explain one advantage to {c["b"]} of {concept}.', cap(pro[0]),
                                    f'1 mark point ({"; ".join(pro[:3])}), 1 mark explanation, 1 mark application to {c["b"]} [3]'))
        for p in t.parts:
            x = p(r, c)
            if x:
                parts.extend(x)
        if t.anl:
            q, pts = _frame(r.choice(t.anl), r, c)[:2]
            parts.append(lambda r, q=q, pts=pts: (q, cap('; '.join(pts)), key_an(6, c, pts)))
        if t.ev:
            q, fo, ag, dep = _frame(r.choice(t.ev), r, c)
            m = 10
            parts.append(lambda r, q=q, fo=fo, ag=ag, dep=dep, m=m: (q, ans_ev(c, fo, ag, dep), key_ev(m, c, fo, ag, dep)))
        if len(parts) < 2:
            return None
        return compose(r, intro(r, c), parts, k=(2, 3), type_='case')
    return t


def calc_part(t):
    """Register a case-part provider (r, c) -> [part lambdas] used in structured case items."""
    def deco(fn):
        t.parts.append(fn)
        return fn
    return deco


def mc_num(r, correct, wrong, f):
    """Numeric MCQ: correct value and wrong values formatted by f, guaranteeing 3 distinct distractors."""
    c = f(correct)
    ds = []
    for w in list(wrong) + [correct * k for k in (1.1, 0.9, 1.25, 0.8, 1.5, 0.5, 2)]:
        s = f(w)
        if s != c and s not in ds:
            ds.append(s)
    return mcq(r, c, ds[:6])


# =====================================================================================
# 1 External influences: the economic environment
# =====================================================================================

t = T(1, 'Macroeconomic objectives', ['macroeconomic objectives: growth, inflation, unemployment, exchange rates', 'macroeconomic objectives', 'inflation unemployment'],
      defs=[('economic growth', 'An increase in the real value of a country\'s output (real GDP) over time.'),
            ('inflation', 'A sustained rise in the general price level in an economy, usually measured by a consumer price index.'),
            ('unemployment', 'The situation where people of working age who are willing and able to work, and are actively seeking a job, cannot find one.'),
            ('real gross domestic product (GDP)', 'The total value of goods and services produced in a country in a year, adjusted to remove the effect of inflation.')],
      mcqs=[('Which type of unemployment is caused by the long-term decline of an industry?', 'Structural unemployment', ['Cyclical unemployment', 'Frictional unemployment', 'Seasonal unemployment'],
             'Structural unemployment arises when the skills of workers no longer match the jobs available, e.g. after an industry declines.'),
            ('Which group is most likely to gain from an unexpected rise in inflation?', 'Businesses with large fixed-interest loans', ['Savers holding cash', 'Employees on fixed money wages', 'Banks lending at fixed interest rates'],
             'Inflation reduces the real value of debt, so fixed-rate borrowers gain while lenders and savers lose.'),
            ('Which is most likely to happen to a business during a period of high inflation?', 'Long-term planning and investment become harder because future costs and prices are uncertain', ['The real value of its cash reserves rises', 'Employees accept lower money wage increases', 'Its exports become cheaper in foreign markets'],
             'High, unstable inflation creates uncertainty, raises costs and wage demands and makes exports less competitive.'),
            ('Which of these is a government macroeconomic objective?', 'Low and stable inflation', ['Higher market share for domestic firms', 'Maximum profit for state-owned businesses', 'Lower prices for imported luxury goods'],
             'The main macroeconomic objectives are economic growth, low unemployment, low stable inflation and a stable exchange rate / balance of payments.')],
      exps=[('Explain the difference between nominal GDP growth and real GDP growth.', 'Nominal growth measures the rise in the money value of output; real growth removes the effect of inflation, so it measures the change in the volume of output.', '1 mark nominal = money value at current prices; 1 mark real = adjusted for inflation / volume of output. [2]'),
            ('Explain why low and stable inflation benefits businesses as well as consumers.', 'Stable prices make costs and revenues predictable, so firms can plan and invest with confidence; consumers keep their purchasing power so demand is steadier; exports stay price-competitive.', '1 mark planning/certainty; 1 mark investment confidence or stable demand; 1 mark international competitiveness. [3]'),
            ('Explain two ways in which rising unemployment can affect a business that sells luxury products.', 'Demand falls because household incomes fall and luxuries are income elastic; but the business finds it easier and cheaper to recruit staff because more people are looking for work.', '2 × (1 mark effect, 1 mark explanation): falling demand (income elastic); easier recruitment / less wage pressure. [4]'),
            ('Explain why a government may find it difficult to achieve all of its macroeconomic objectives at the same time.', 'Objectives conflict: policies that boost growth and reduce unemployment can raise inflation and worsen the trade balance; reducing inflation with higher interest rates can slow growth and raise unemployment.', '1 mark idea of conflicting objectives; 2 marks a developed example (e.g. growth v inflation trade-off). [3]')],
      adv=[('a period of rapid economic growth in {country}', ['rising household incomes increase demand for its {prod}', 'higher sales allow economies of scale', 'easier to raise finance as banks and investors are confident'],
            ['labour shortages push up wage costs', 'suppliers raise prices as demand for materials grows', 'capacity may be insufficient, leading to lost orders or lower quality']),
           ('inflation of about 8% a year in {country}', ['it may be able to raise its prices without losing customers', 'the real value of its debts falls', 'the value of its stocks of materials rises'],
            ['costs of materials and wages rise', 'customers\' real incomes fall so demand may fall', 'it becomes harder to plan and its exports become less price competitive'])],
      anl=[('Analyse how an increase in the inflation rate in {country} from 3% to 9% could affect {b}.', ['inflation means a sustained rise in the general price level', 'higher input and wage costs squeeze profit margins unless prices rise', 'falling real incomes reduce demand, especially for income-elastic {prod}', 'if inflation is higher than in trading partners, exports lose price competitiveness']),
           ('Analyse the likely impact on {b} of a rise in unemployment in {country} from 5% to 11%.', ['unemployment reduces household income and consumer confidence', 'lower demand for {prod} reduces revenue and capacity utilisation', 'a larger pool of job applicants makes recruitment easier and reduces wage pressure', 'staff morale may fall if employees fear redundancy']),
           ('Analyse how faster economic growth in {country} could affect both the revenue and the costs of {b}.', ['real GDP growth raises incomes and demand', 'revenue rises, more so if {prod} are income elastic', 'skills shortages and rising wages increase costs', 'need to expand capacity may require investment and finance'])],
      ev=[('Evaluate the extent to which high inflation is the most serious macroeconomic problem facing {b}.', ['rising costs of materials and labour cut margins', 'uncertainty discourages investment', 'loss of export competitiveness'],
           ['unemployment or a recession may reduce demand by more', 'exchange-rate movements may matter more for a business that trades internationally', 'if demand is price inelastic, cost increases can be passed on'],
           ['how price elastic demand for its {prod} is', 'the share of its sales that are exported', 'whether its competitors face the same pressures']),
          ('Discuss whether {b} should postpone its planned expansion because economic growth in {country} is forecast to slow to 0.5%.', ['lower growth means weaker demand and spare capacity', 'expansion financed by borrowing increases risk', 'cash could be kept as a buffer'],
           ['forecasts are often wrong and the slowdown may be brief', 'costs of building and recruiting may be lower in a slowdown', 'expansion may target export markets that are still growing'],
           ['the income elasticity of demand for its {prod}', 'how the expansion is financed', 'the strategic importance of moving ahead of competitors'])])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def macro_calc(r, D):
    kind = r.randrange(3)
    if kind == 0:
        g1 = r.randrange(120, 900, 10)
        n = r.choice([4, 5, 6, 7, 8, 9, 10, 12])
        i = r.choice([x for x in (1, 2, 3, 4, 5, 6) if x < n])
        g2 = g1 * (1 + n / 100)
        real = (g2 / (1 + i / 100) / g1 - 1) * 100
        if D == 1:
            opts, ans = mcq(r, pct(n - i), [pct(n + i), pct(n), pct(i)])
            return {'stem': f'A country\'s nominal GDP grew by {n}% last year while inflation was {i}%. What was the approximate growth in real GDP?', 'options': opts, 'answer': ans,
                    'key': f'Real growth ≈ nominal growth − inflation = {n} − {i} = {n - i}%.', 'marks': 1}
        if D == 2:
            return {'stem': f'Nominal GDP in a country rose from ${g1} billion to ${num(g2, 1)} billion in one year. Inflation was {i}%. Calculate (a) the nominal growth rate and (b) the approximate real growth rate.',
                    'answer': f'(a) {n}% (b) about {n - i}%', 'key': f'(a) ({num(g2, 1)} − {g1}) / {g1} × 100 = {n}% [1]; (b) real ≈ {n} − {i} = {n - i}% [1]. [2]', 'marks': 2}
        return {'stem': f'Nominal GDP in a country rose from ${g1} billion to ${num(g2, 1)} billion, while the price level rose by {i}%. Calculate the real GDP growth rate to two decimal places' + (' and explain what the figure means for businesses selling income-elastic products.' if D >= 4 else '.'),
                'answer': f'{real:.2f}%' + ('; real output and incomes are rising, so demand for income-elastic products should rise faster than GDP.' if D >= 4 else ''),
                'key': f'Real GDP = {num(g2, 1)} / {1 + i / 100:.2f} = {g2 / (1 + i / 100):.2f} [1]; growth = ({g2 / (1 + i / 100):.2f} − {g1}) / {g1} × 100 [1] = {real:.2f}% [1]' + (' ; interpretation linked to income elasticity [1]. [4]' if D >= 4 else '. [3]'),
                'marks': 4 if D >= 4 else 3}
    if kind == 1:
        lf = r.choice([12.5, 18.0, 24.0, 30.5, 42.0, 8.8, 15.2])
        u1 = r.choice([4.0, 5.0, 6.0, 7.5, 8.0])
        u2 = u1 + r.choice([-1.5, -1.0, 1.0, 1.5, 2.5, 3.0])
        U1, U2 = lf * u1 / 100, lf * u2 / 100
        if D == 1:
            opts, ans = mc_num(r, u1, [U1 * 100 / (lf - U1), lf / U1, u1 / 10], lambda x: pct(x))
            return {'stem': f'A country has a labour force of {num(lf)} million people, of whom {num(U1, 3)} million are unemployed. What is the unemployment rate?', 'options': opts, 'answer': ans,
                    'key': f'Unemployment rate = unemployed / labour force × 100 = {num(U1, 3)} / {num(lf)} × 100 = {pct(u1)}.', 'marks': 1}
        stem = f'In a country with a labour force of {num(lf)} million, the number unemployed changed from {num(U1, 3)} million to {num(U2, 3)} million over a year (labour force unchanged). Calculate the unemployment rate in each year'
        key = f'Year 1: {num(U1, 3)}/{num(lf)} × 100 = {pct(u1)} [1]; year 2: {num(U2, 3)}/{num(lf)} × 100 = {pct(u2)} [1]'
        if D >= 3:
            stem += ' and the change in percentage points'
            key += f'; change = {u2 - u1:+.1f} percentage points [1]'
        if D >= 4:
            stem += ', and explain one likely effect of this change on a retailer'
            key += f'; effect: {"falling" if u2 > u1 else "rising"} incomes and consumer confidence change demand / recruitment conditions [1]'
        m = 2 + (D >= 3) + (D >= 4)
        return {'stem': stem + '.', 'answer': f'{pct(u1)} and {pct(u2)}' + (f'; change {u2 - u1:+.1f} percentage points' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m}
    p1 = r.choice([104.0, 110.0, 112.5, 120.0, 125.0, 136.0])
    inf = r.choice([2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 12.0])
    p2 = round(p1 * (1 + inf / 100), 1)
    inf = (p2 / p1 - 1) * 100
    w = r.choice([2.0, 3.0, 5.0, 6.0, 7.0, 10.0])
    if D == 1:
        opts, ans = mc_num(r, inf, [p2 - p1, (p2 - p1) / p2 * 100, p2 / 100], lambda x: pct(x))
        return {'stem': f'A consumer price index rose from {num(p1, 1)} to {num(p2, 1)} over one year. What was the rate of inflation (to one decimal place)?', 'options': opts, 'answer': ans,
                'key': f'Inflation = ({num(p2, 1)} − {num(p1, 1)}) / {num(p1, 1)} × 100 = {pct(inf)}.', 'marks': 1}
    stem = f'The consumer price index in {r.choice(CASES)["country"]} rose from {num(p1, 1)} to {num(p2, 1)} over one year. Calculate the rate of inflation'
    key = f'({num(p2, 1)} − {num(p1, 1)}) / {num(p1, 1)} × 100 = {pct(inf)} [2]'
    m = 2
    if D >= 3:
        rw = ((1 + w / 100) / (1 + inf / 100) - 1) * 100
        stem += f'. Employees received a {pct(w)} pay rise in the same year. Calculate the approximate change in their real wages'
        key += f'; real wage change ≈ {pct(w)} − {pct(inf)} = {w - inf:+.1f}% (exact {rw:+.2f}%) [1]'
        m = 3
        if D >= 4:
            stem += ' and explain how this might affect employees\' motivation'
            key += '; falling/rising purchasing power affects motivation and wage claims (e.g. Maslow physiological/safety needs, trade union pressure) [1]'
            m = 4
    return {'stem': stem + '.', 'answer': pct(inf) + (f'; real wages change by about {w - inf:+.1f}%' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m}


t = T(1, 'Business cycle', ['business cycle and its impact on business', 'business cycle', 'recession boom'],
      defs=[('business cycle', 'The regular pattern of rises and falls in real GDP over time, through the phases of boom, downturn, recession and recovery.'),
            ('recession', 'A period of falling real GDP, often defined as two consecutive quarters of negative economic growth.'),
            ('boom', 'The phase of the business cycle with high growth, high demand, low unemployment and rising inflationary pressure.'),
            ('inferior good', 'A product for which demand falls as consumer incomes rise and rises as incomes fall (negative income elasticity).')],
      mcqs=[('In which phase of the business cycle are capacity shortages and rising inflation most likely?', 'Boom', ['Recession', 'Recovery', 'Slump'],
             'In a boom demand exceeds capacity, so firms face shortages of labour and materials and prices rise.'),
            ('During a recession, demand is most likely to rise for which type of product?', 'Inferior goods such as budget own-label groceries', ['Luxury holidays', 'New cars', 'Restaurant meals'],
             'Inferior goods have negative income elasticity, so demand rises when incomes fall.'),
            ('Why are businesses that make capital goods often hit hardest in a recession?', 'Other firms postpone investment in new machinery when demand falls', ['Capital goods have negative income elasticity', 'Interest rates always rise in a recession', 'Governments ban imports of capital goods'],
             'Investment is the most volatile part of demand: firms with spare capacity delay buying new equipment.')],
      exps=[('Explain why a business selling luxury products is likely to be affected more by the business cycle than one selling basic foods.', 'Luxuries have high positive income elasticity, so demand rises and falls more than incomes; basic foods have low income elasticity, so demand is stable.', '1 mark income elasticity idea; 1 mark luxuries elastic/large swings; 1 mark necessities stable. [3]'),
            ('Explain one way a business could use knowledge of the business cycle when planning capacity.', 'It could avoid committing to large fixed-cost expansion near the peak of a boom and instead invest during recovery, so new capacity arrives as demand rises.', '1 mark planning action; 1 mark link to cycle phase and demand. [2]'),
            ('Explain why a business may cut prices during a recession even though this reduces its profit margin.', 'To protect sales volume and market share when consumers trade down; keeping capacity utilised spreads fixed costs and keeps cash flowing.', '1 mark protect volume/market share; 1 mark fixed costs/cash flow. [2]')],
      adv=[('cutting prices during a recession', ['protects market share as customers trade down', 'keeps capacity utilisation and cash flow up', 'can win customers from weaker rivals'],
            ['lower margins reduce profit', 'may damage brand image of {prod}', 'competitors may start a price war']),
           ('investing in new capacity during an economic recovery', ['ready to meet rising demand before rivals', 'building and equipment costs may still be low', 'gains economies of scale as output rises'],
            ['the recovery may stall, leaving spare capacity', 'borrowing increases gearing and interest costs', 'cash flow pressure before sales rise'])],
      anl=[('Analyse how a recession in {country} is likely to affect {b}.', ['recession is falling real GDP and incomes', 'demand for {prod} falls, especially if income elastic', 'lower capacity utilisation raises unit fixed costs', 'cash-flow problems and possible redundancies affect morale']),
           ('Analyse two strategies {b} could use to reduce the impact of a recession.', ['cost reduction (e.g. renegotiating supplier contracts, delayering)', 'introducing lower-priced versions of {prod}', 'diversifying into less cyclical markets or export markets', 'protecting cash flow by reducing inventory and credit periods']),
           ('Analyse how {b} might be affected as {country} moves from recession into recovery.', ['incomes and confidence start to rise', 'sales of {prod} increase, so spare capacity is used', 'need for working capital rises as output grows', 'may need to recruit and train staff again'])],
      ev=[('Evaluate the most suitable strategy for {b} if {country} enters a recession next year.', ['cost cutting protects profit and cash', 'a value range of {prod} keeps price-sensitive customers', 'export growth spreads risk'],
           ['cost cutting can damage quality and morale', 'lower prices may harm the brand', 'export markets may also be in recession'],
           ['the income elasticity of demand for its {prod}', 'its cash reserves and gearing', 'how long the recession lasts']),
          ('Discuss whether {b} should increase its capacity now that {country}\'s economy is in the recovery phase of the business cycle.', ['demand for {prod} is likely to rise', 'acting early may gain market share', 'construction and equipment costs may be lower now'],
           ['recovery may be weak or short', 'borrowing increases risk', 'existing spare capacity could be used first'],
           ['the accuracy of economic forecasts', 'current capacity utilisation', 'how the expansion is financed'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def cycle_yed(r, D):
    c = r.choice(CASES)
    S = r.choice([12000, 20000, 25000, 40000, 60000, 80000, 150000])
    e = r.choice([2.5, 2.0, 1.8, 1.5, 0.6, 0.4, -0.5, -0.8])
    g = r.choice([-4, -3, -2, -1.5, 2, 2.5, 3, 4])
    ch = e * g
    S2 = S * (1 + ch / 100)
    if D == 1:
        opts, ans = mc_num(r, ch, [g / e, e + g, -ch], lambda x: pct(x))
        return {'stem': f'The income elasticity of demand for a product is {e}. If real incomes change by {g:+}%, what is the expected percentage change in quantity demanded?', 'options': opts, 'answer': ans,
                'key': f'%ΔQd = YED × %ΔY = {e} × {g:+} = {ch:+.1f}%.', 'marks': 1}
    stem = f'{c["full"]} sells {S:,} units a month of a product with an income elasticity of demand of {e}. Real incomes in {c["country"]} are forecast to change by {g:+}% as the business cycle {"turns down" if g < 0 else "recovers"}. Calculate the expected monthly sales after the change'
    key = f'%ΔQ = {e} × {g:+} = {ch:+.1f}% [1]; new sales = {S:,} × {1 + ch / 100:.3f} = {round(S2):,} units [1]'
    m = 2
    if D >= 3:
        p = r.choice([4, 5, 8, 12, 15, 20])
        stem += f' and the change in monthly revenue if the price is ${p}'
        key += f'; Δrevenue = {round(S2 - S):+,} × ${p} = {money(abs((S2 - S) * p)) if S2 > S else "−" + money(abs((S2 - S) * p))} [1]'
        m = 3
    if D >= 4:
        kind = 'a luxury (income elastic)' if e > 1 else ('a normal necessity (income inelastic)' if e > 0 else 'an inferior good')
        stem += '. Explain what the elasticity figure suggests about the product'
        key += f'; YED {e} means it is {kind}, so sales {"move more than" if abs(e) > 1 else "move less than"} incomes{" and in the opposite direction" if e < 0 else ""} [1]'
        m = 4
    if D >= 5:
        stem += ', and evaluate one limitation of using this forecast for planning'
        key += '; limitation: YED estimated from past data, other factors (prices, competitors, tastes) not held constant, forecast of income may be wrong [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'{round(S2):,} units a month ({ch:+.1f}%)', 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(1, 'Fiscal, monetary and supply-side policies', ['fiscal, monetary and supply-side policies', 'fiscal policy', 'monetary policy', 'supply-side'],
      defs=[('fiscal policy', 'Government decisions on taxation and government spending used to influence the level of economic activity.'),
            ('monetary policy', 'Decisions by the central bank on interest rates and the money supply, used mainly to control inflation.'),
            ('supply-side policy', 'Government measures that aim to increase the productive capacity and efficiency of the economy, e.g. training, deregulation, infrastructure.'),
            ('interest rate', 'The cost of borrowing money and the reward for saving, expressed as a percentage of the sum borrowed or saved per year.')],
      mcqs=[('Which is an example of contractionary fiscal policy?', 'Raising income tax rates', ['Cutting the central bank interest rate', 'Increasing government spending on roads', 'Reducing the rate of sales tax'],
             'Fiscal policy uses tax and spending; raising taxes reduces aggregate demand.'),
            ('A central bank raises interest rates. Which business is likely to be most affected?', 'A highly geared firm with large variable-rate bank loans', ['A cash-rich firm with no borrowing', 'A firm selling low-priced basic foods', 'A sole trader who rents a market stall'],
             'Higher rates raise interest costs for borrowers, especially with variable-rate debt.'),
            ('Which of the following is a supply-side policy?', 'Increasing state funding for vocational training', ['Raising the interest rate', 'Increasing unemployment benefits', 'Devaluing the currency'],
             'Supply-side policies raise productive capacity, e.g. through education and training.')],
      exps=[('Explain why a rise in interest rates is likely to reduce demand for consumer durables such as cars.', 'Many durables are bought on credit, so higher rates raise monthly repayments; higher mortgage costs also reduce disposable income, and saving becomes more attractive.', '1 mark credit cost; 1 mark lower disposable income / incentive to save. [2]'),
            ('Explain how a cut in corporation tax might encourage businesses to invest.', 'Firms keep a larger share of profit, so more retained earnings are available and the after-tax return on new projects rises.', '1 mark more retained profit; 1 mark higher after-tax return. [2]'),
            ('Explain the difference between fiscal policy and monetary policy.', 'Fiscal policy is government taxation and spending; monetary policy is the central bank\'s control of interest rates and the money supply.', '1 mark each correct description. [2]')],
      adv=[('a rise in interest rates in {country}', ['interest earned on cash reserves rises', 'lower inflation may reduce cost pressures', 'a stronger {cur} makes imported materials cheaper'],
            ['higher interest payments on loans', 'customers buying on credit reduce spending', 'investment projects become less attractive']),
           ('a large government infrastructure programme in {country}', ['better transport cuts distribution costs', 'higher incomes from construction jobs raise demand', 'improved digital networks raise productivity'],
            ['may be financed by higher taxes', 'could push up wages and interest rates', 'benefits take years to arrive'])],
      anl=[('Analyse how an increase in interest rates from 4% to 7% could affect {b}.', ['higher cost of borrowing raises interest payments', 'consumer demand for {prod} may fall', 'investment projects have lower net returns', 'exchange rate may appreciate, affecting exports and imports']),
           ('Analyse how an increase in the rate of sales tax (VAT) in {country} could affect {b}.', ['indirect tax raises prices to consumers', 'if demand is price elastic, sales fall sharply', 'the business may absorb part of the tax, cutting margins', 'administration costs of collecting the tax']),
           ('Analyse how government supply-side policies to improve training could affect {b}.', ['supply-side policy raises productive potential', 'better-skilled workers raise labour productivity', 'lower recruitment and training costs', 'improved competitiveness against foreign rivals'])],
      ev=[('Evaluate whether a cut in corporation tax or a cut in interest rates would benefit {b} more.', ['a tax cut raises retained profit for investment', 'an interest cut reduces borrowing costs', 'an interest cut may boost consumer demand'],
           ['a tax cut helps only if the business is profitable', 'an interest cut helps little if it has no debt', 'effects take time and depend on confidence'],
           ['its current profitability and gearing', 'whether its customers buy {prod} on credit', 'the size of each change']),
          ('Discuss the extent to which government economic policies in {country} are likely to affect the success of {b}.', ['interest rates affect borrowing costs and demand', 'tax changes affect prices and profits', 'supply-side policies affect skills and costs'],
           ['internal factors such as management and products matter more', 'competition and global demand may dominate', 'policies may change before they have effect'],
           ['how much it borrows and exports', 'the size and timing of policy changes', 'the quality of its strategy'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def interest_calc(r, D):
    c = r.choice(CASES)
    L = r.choice([2, 4, 5, 6, 8, 10, 12, 15, 20, 25])
    r1 = r.choice([3, 4, 5, 6])
    r2 = r1 + r.choice([1, 1.5, 2, 3])
    OP = r.choice([0.15, 0.2, 0.25, 0.3, 0.4, 0.6]) * L
    i1, i2 = L * r1 / 100, L * r2 / 100
    if D == 1:
        opts, ans = mc_num(r, i2 - i1, [i2, i1, (r2 - r1)], lambda x: money(x * 1e6))
        return {'stem': f'A business has a variable-rate loan of ${L} million. The interest rate rises from {r1}% to {num(r2)}%. By how much do its annual interest payments rise?', 'options': opts, 'answer': ans,
                'key': f'Increase = ${L}m × ({num(r2)} − {r1})% = {money((i2 - i1) * 1e6)}.', 'marks': 1}
    stem = f'{c["full"]} has variable-rate loans of ${L} million and an operating profit of {money(OP * 1e6)}. The central bank raises interest rates so that its loan rate rises from {r1}% to {num(r2)}%. Calculate the increase in annual interest payments'
    key = f'Interest before = {money(i1 * 1e6)}, after = {money(i2 * 1e6)} [1]; increase = {money((i2 - i1) * 1e6)} [1]'
    m = 2
    if D >= 3:
        stem += ' and the percentage fall in profit before tax'
        fall = (i2 - i1) / (OP - i1) * 100
        key += f'; PBT falls from {money((OP - i1) * 1e6)} to {money((OP - i2) * 1e6)}, a fall of {fall:.1f}% [1]'
        m = 3
    if D >= 4:
        stem += f'. Calculate the interest cover (operating profit ÷ interest) before and after the change'
        key += f'; interest cover {OP / i1:.2f} times → {OP / i2:.2f} times [1]'
        m = 4
    if D >= 5:
        stem += ', and assess how serious this change is for the business'
        key += '; judgement: cover above about 2–3 times is usually manageable; consider effect on demand and future borrowing [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'Interest rises by {money((i2 - i1) * 1e6)}' + (f'; PBT falls by {(i2 - i1) / (OP - i1) * 100:.1f}%' if D >= 3 else '') + (f'; cover {OP / i1:.2f} → {OP / i2:.2f}' if D >= 4 else ''),
            'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(1, 'Exchange rate changes and international trade', ['exchange rate changes and international trade', 'exchange rate', 'appreciation depreciation'],
      defs=[('exchange rate', 'The price of one currency expressed in terms of another currency.'),
            ('appreciation', 'A rise in the value of a currency against other currencies in a floating exchange-rate system.'),
            ('depreciation', 'A fall in the value of a currency against other currencies in a floating exchange-rate system.'),
            ('hedging (currency)', 'Reducing the risk of exchange-rate changes, e.g. by agreeing today a fixed rate for a future currency transaction (a forward contract).')],
      mcqs=[('A country\'s currency appreciates. What is the most likely effect on its exporters?', 'Their prices in foreign currencies rise, so they become less competitive', ['Their export prices in foreign currencies fall', 'Their imported raw materials become more expensive', 'Their profit per unit always rises'],
             'Strong pound/peso imports cheap, exports dear: foreign buyers need more of their own currency to buy the exports.'),
            ('A currency depreciates. Which business is most likely to suffer?', 'A firm that imports most of its raw materials and sells only in the home market', ['A firm that exports most of its output', 'A hotel that relies on foreign tourists', 'A domestic firm competing against imports'],
             'Depreciation raises the home-currency cost of imports, hurting importers who cannot pass costs on.'),
            ('Why might a depreciation fail to increase an exporter\'s revenue much?', 'Foreign demand for its products is price inelastic', ['Foreign demand is price elastic', 'Its products are sold in the home currency only', 'Its competitors\' currencies appreciate'],
             'If PED is low, cheaper foreign prices increase quantity only slightly.')],
      exps=[('Explain why a depreciation of a country\'s currency is not always good for its exporters.', 'Exports become cheaper abroad, but imported components and fuel cost more, raising costs; if foreign demand is price inelastic, volume gains are small.', '1 mark cheaper exports; 1 mark higher import costs; 1 mark elasticity. [3]'),
            ('Explain how a business could reduce the risk caused by exchange-rate changes.', 'It could hedge using forward contracts, invoice in its own currency, or match costs and revenues in the same currency (e.g. by producing abroad).', '1 mark method; 1 mark explanation of how it reduces risk. [2]'),
            ('Explain how an appreciation of its currency could benefit a business.', 'Imported materials, components and machinery become cheaper in home currency, cutting costs and raising margins on domestic sales.', '1 mark cheaper imports; 1 mark effect on costs/margins. [2]')],
      adv=[('a 15% depreciation of the {cur}', ['its exports become cheaper in foreign currencies', 'imported rival products become dearer in {country}', 'foreign-currency revenue is worth more in {cs}'],
            ['imported materials and components cost more', 'foreign-currency loans become more expensive to repay', 'higher import prices may raise inflation and wage claims']),
           ('invoicing its overseas customers in {cs} rather than US dollars', ['it knows exactly how much revenue it will receive', 'no need to pay for hedging', 'simpler cash-flow forecasting'],
            ['customers bear the risk and may switch to suppliers who invoice in dollars', 'may lose orders if the {cur} appreciates', 'less competitive in markets where prices are set in dollars'])],
      anl=[('Analyse how an appreciation of the {cur} against the US dollar could affect {b}.', ['appreciation raises the foreign-currency price of exports', 'export volume falls if demand is price elastic', 'imported inputs become cheaper, cutting costs', 'overseas earnings are worth less when converted into {cs}']),
           ('Analyse the likely effects on {b} of a large and sudden depreciation of the {cur}.', ['depreciation lowers foreign prices of exports', 'imported materials become more expensive', 'margins depend on how much of the cost base is imported', 'uncertainty makes pricing and planning harder'])],
      ev=[('Evaluate the impact on {b} of a 20% fall in the value of the {cur} against the US dollar.', ['exports become more price competitive', 'foreign rivals in {country} become more expensive', 'overseas revenue converts into more {cs}'],
           ['imported inputs rise in price', 'higher inflation may follow', 'gains depend on price elasticity of foreign demand'],
           ['the share of sales exported and of costs imported', 'the price elasticity of demand for its {prod}', 'whether it has hedged']),
          ('Discuss whether {b} should use forward contracts to protect itself from exchange-rate changes.', ['certainty of future costs and revenues', 'easier budgeting and pricing', 'protects margins against sharp movements'],
           ['forward contracts cost money (fees, spreads)', 'it loses gains if the rate moves favourably', 'only covers known transactions for a limited period'],
           ['how volatile the {cur} is', 'the size of its foreign-currency transactions', 'its attitude to risk'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def fx_calc(r, D):
    c = r.choice(CASES)
    base = c['fx'] * r.choice([0.9, 1.0, 1.1])
    e1 = float(sf(base, 2).replace(',', ''))
    chg = r.choice([-20, -15, -10, 10, 15, 20, 25])
    e2 = e1 * (1 + chg / 100)
    usd = r.choice([12, 15, 20, 24, 30, 40, 50, 60, 75, 120, 250])
    P = float(sf(e1 * usd, 3).replace(',', ''))
    usd1, usd2 = P / e1, P / e2
    word = 'depreciates' if chg > 0 else 'appreciates'
    cs = c['cs']
    E1, E2, PP = sf(e1, 3), sf(e2, 4), sf(P, 3)
    if D == 1:
        opts, ans = mc_num(r, usd1, [P * e1, usd1 * 1.2, e1 / P], lambda x: money(x, 2))
        return {'stem': f'A product sells for {PP} {cs} in {c["country"]}. The exchange rate is US$1 = {E1} {cs}. What is its price in US dollars?', 'options': opts, 'answer': ans,
                'key': f'US$ price = {PP} / {E1} = {money(usd1, 2)}.', 'marks': 1}
    stem = f'{c["full"]} sells one of its main export lines at {PP} {cs} per unit. The exchange rate changes from US$1 = {E1} {cs} to US$1 = {E2} {cs}, so the {c["cur"]} {word}. Calculate the US-dollar price before and after the change'
    key = f'Before: {PP}/{E1} = {money(usd1, 2)} [1]; after: {PP}/{E2} = {money(usd2, 2)} [1]'
    m = 2
    pc = (usd2 / usd1 - 1) * 100
    if D >= 3:
        stem += ' and the percentage change in the US-dollar price'
        key += f'; % change = {pc:+.1f}% [1]'
        m = 3
    if D >= 4:
        ped = r.choice([-0.5, -0.8, -1.5, -2.0])
        stem += f'. Price elasticity of demand in its US market is {ped}. Estimate the percentage change in export volume'
        key += f'; %ΔQ = {ped} × {pc:+.1f} = {ped * pc:+.1f}% [1]'
        m = 4
        if D >= 5:
            stem += ' and comment on whether the change is good for the business'
            key += f'; comment: volume {"rises" if ped * pc > 0 else "falls"}; revenue in {cs} {"rises" if ped * pc > 0 else "falls"}; also consider imported input costs and margins [1]'
            m = 5
    return {'stem': stem + '.', 'answer': f'{money(usd1, 2)} → {money(usd2, 2)}' + (f' ({pc:+.1f}%)' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m,
            'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 2 External influences: political, legal, social, technological and environmental
# =====================================================================================

t = T(2, 'Government intervention and competition policy', ['government intervention, regulation and competition policy', 'competition policy', 'regulation'],
      defs=[('competition policy', 'Government laws and regulators that promote competition and prevent abuse of market power, e.g. by investigating mergers, cartels and monopolies.'),
            ('monopoly', 'A market dominated by one firm; in competition law a firm with a large market share (often 25% or more) may be treated as having monopoly power.'),
            ('cartel', 'An agreement between competing firms to fix prices, limit output or share out markets, which is illegal in most countries.'),
            ('deregulation', 'The removal of government rules and controls that restrict competition or business activity in a market.')],
      mcqs=[('Which action is most likely to be investigated by a competition authority?', 'Two leading firms agreeing to charge the same price', ['A firm cutting its costs through new technology', 'A small firm entering a new market', 'A firm advertising its products on social media'],
             'Price fixing is collusion between rivals and is illegal under competition law.'),
            ('Why might a government prevent a proposed merger between two large supermarkets?', 'The merged firm could gain market power and raise prices to consumers', ['The merged firm would be too small to compete', 'Mergers always reduce employment', 'The government owns all supermarkets'],
             'Regulators block mergers that substantially lessen competition and harm consumers.'),
            ('Which is an example of government regulation of business?', 'A legal limit on the pollution a factory may emit', ['A firm choosing to cut prices', 'A trade union negotiating wages', 'A bank lending to a small business'],
             'Regulation uses rules backed by law to control business behaviour.')],
      exps=[('Explain why governments use competition policy.', 'To stop firms abusing market power by charging high prices, restricting choice or blocking new entrants, so consumers get lower prices, more choice and more innovation.', '1 mark prevent abuse of market power; 1 mark benefit to consumers (price/choice/innovation). [2]'),
            ('Explain one benefit and one cost to a business of stricter government regulation of its industry.', 'Benefit: rules create a level playing field and can raise consumer trust; cost: compliance costs (staff, reporting, equipment) raise unit costs.', '1 mark benefit + explanation; 1 mark cost + explanation. [2]'),
            ('Explain how deregulation of a market might affect an existing firm in that market.', 'New competitors can enter, so prices and market share may fall; but the firm also gains freedom to enter new activities and may become more efficient.', '1 mark more competition / lower prices; 1 mark new freedoms or efficiency pressure. [2]')],
      adv=[('stricter government regulation of its industry', ['protects reputation of compliant firms', 'barriers to entry deter new rivals', 'consumer confidence in {prod} may rise'],
            ['higher compliance costs', 'slower decision-making and product launches', 'risk of fines for breaches']),
           ('the government deregulating its market', ['freedom to change prices and products', 'lower administration costs', 'opportunity to enter new segments'],
            ['new competitors enter', 'prices and margins may fall', 'loss of protection for incumbents'])],
      anl=[('Analyse how a decision by the competition authority to investigate {bp} pricing could affect the business.', ['competition law prevents abuse of a dominant position', 'possible fines and legal costs', 'damage to reputation with customers and investors', 'may have to change pricing or contracts, reducing profit']),
           ('Analyse two ways in which new government regulations on product safety could affect {b}.', ['regulation sets legal minimum standards', 'higher costs of testing and redesigning {prod}', 'delays to new product launches', 'can become a source of competitive advantage if rivals struggle to comply'])],
      ev=[('Evaluate whether government regulation of its industry is more of a threat than an opportunity for {b}.', ['compliance costs and fines', 'restrictions on pricing and products', 'management time diverted'],
           ['raises barriers to entry for rivals', 'improves consumer trust', 'early compliance can be a selling point'],
           ['how strict and how well enforced the rules are', 'its size relative to competitors', 'whether it can pass costs on']),
          ('Discuss whether {b} should seek to grow by taking over a major competitor, given the risk of an investigation by the competition authority.', ['larger market share and economies of scale', 'removes a rival', 'faster than organic growth'],
           ['merger could be blocked or conditions imposed', 'legal costs and delay', 'reputational risk'],
           ['the combined market share', 'the authority\'s past decisions', 'the benefits to consumers it can demonstrate'])])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def conc_calc(r, D):
    names = r.sample([c['b'] for c in CASES], 5)
    sales = sorted(r.sample(range(20, 160, 5), 5), reverse=True)
    other = r.choice([80, 120, 150, 200, 260])
    tot = sum(sales) + other
    shares = [s / tot * 100 for s in sales]
    cr3 = sum(shares[:3])
    tbl = ', '.join(f'{n} ${s}m' for n, s in zip(names, sales)) + f'; all other firms ${other}m'
    if D == 1:
        opts, ans = mc_num(r, shares[0], [sales[0], shares[0] * 2, 100 - shares[0]], lambda x: pct(x))
        return {'stem': f'Annual sales in a market are: {tbl}. What is the market share of {names[0]}?', 'options': opts, 'answer': ans,
                'key': f'Total market = ${tot}m; share = {sales[0]}/{tot} × 100 = {pct(shares[0])}.', 'marks': 1}
    i, j = r.sample(range(1, 5), 2)
    comb = shares[i] + shares[j]
    stem = f'Annual sales in a market are: {tbl}. Calculate the three-firm concentration ratio'
    key = f'Total = ${tot}m [1]; CR3 = ({sales[0]} + {sales[1]} + {sales[2]})/{tot} × 100 = {pct(cr3)} [1]'
    m = 2
    if D >= 3:
        stem += f'. {names[i]} and {names[j]} propose to merge. Calculate their combined market share'
        key += f'; combined = ({sales[i]} + {sales[j]})/{tot} × 100 = {pct(comb)} [1]'
        m = 3
    if D >= 4:
        stem += ' and explain whether the competition authority, which investigates mergers creating a market share of 25% or more, is likely to investigate'
        key += f'; {pct(comb)} is {"at or above" if comb >= 25 else "below"} 25%, so an investigation is {"likely" if comb >= 25 else "unlikely on share alone"} [1]'
        m = 4
    return {'stem': stem + '.', 'answer': f'CR3 = {pct(cr3)}' + (f'; combined share {pct(comb)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m}


t = T(2, 'Employment and consumer protection law', ['employment and consumer protection law', 'employment law', 'consumer protection'],
      defs=[('minimum wage', 'The lowest hourly rate of pay that an employer is legally allowed to pay a worker.'),
            ('consumer protection law', 'Laws that protect buyers from unsafe products, misleading descriptions and unfair trading, and give them rights such as refunds for faulty goods.'),
            ('unfair dismissal', 'Ending an employee\'s contract without a fair reason (such as misconduct, incapability or genuine redundancy) or without following a fair procedure.'),
            ('health and safety legislation', 'Laws requiring employers to provide a safe working environment, training and protective equipment, and to assess workplace risks.')],
      mcqs=[('Which of these is an example of consumer protection law?', 'A ban on describing products in a misleading way', ['A law setting the minimum wage', 'A law requiring safe working conditions', 'A tax on company profits'],
             'Consumer protection covers product descriptions, safety, weights and measures, and consumer rights.'),
            ('Which is a likely cost to a business of a large rise in the national minimum wage?', 'Higher labour costs, especially in labour-intensive businesses', ['Lower labour turnover is impossible', 'Employees will be less motivated', 'Its products become cheaper to produce'],
             'Wage costs rise for low-paid workers, though motivation and turnover may improve.'),
            ('Why might employment protection laws benefit employers as well as employees?', 'They can improve trust and motivation, reducing labour turnover', ['They always reduce wage costs', 'They make it easier to dismiss staff', 'They remove the need for HR departments'],
             'Workers who feel secure and fairly treated tend to be more committed and stay longer.')],
      exps=[('Explain one reason why governments pass consumer protection laws.', 'Consumers often have less information than producers, so laws prevent unsafe or misleadingly described products and give buyers a remedy if goods are faulty.', '1 mark reason (information gap/safety/unfair practices); 1 mark explanation. [2]'),
            ('Explain how a large rise in the minimum wage could affect a labour-intensive business.', 'Wage costs and unit costs rise, cutting margins unless prices rise; it may substitute capital for labour or reduce hours, but motivation and retention may improve.', '1 mark higher costs; 1 mark response (prices/automation); 1 mark possible benefit. [3]'),
            ('Explain why health and safety laws may increase a firm\'s costs in the short run but reduce them in the long run.', 'Training, equipment and inspections cost money now, but fewer accidents reduce absence, compensation claims, fines and lost production later.', '1 mark short-run costs; 1 mark long-run savings. [2]')],
      adv=[('a 12% rise in the national minimum wage in {country}', ['low-paid staff may be more motivated', 'labour turnover and recruitment costs may fall', 'customers on low incomes have more to spend on {prod}'],
            ['higher wage costs', 'pressure to raise prices', 'pay differentials with supervisors narrow']),
           ('new laws giving consumers longer guarantees on {prod}', ['customer trust and repeat purchases may rise', 'quality becomes a selling point', 'weaker rivals may leave the market'],
            ['higher costs of repairs and replacements', 'need to improve quality control', 'admin costs of handling claims'])],
      anl=[('Analyse how stricter employment laws on working hours could affect {b}.', ['employment law sets maximum hours and rest periods', 'more staff may be needed to cover the same work, raising costs', 'less fatigue may improve productivity and safety', 'scheduling and flexibility become more difficult']),
           ('Analyse the possible effects on {b} of a large increase in the minimum wage.', ['minimum wage is a legal floor on hourly pay', 'labour costs rise in proportion to the number of low-paid staff', 'may raise prices or automate to protect margins', 'motivation and retention may improve'])],
      ev=[('Evaluate the impact of a large rise in the minimum wage on {b}.', ['higher labour costs and lower margins', 'need to raise prices', 'differentials with supervisors narrow'],
           ['better motivation and lower turnover', 'customers may have more to spend', 'rivals face the same cost increase'],
           ['how labour-intensive its operations are', 'the price elasticity of demand for its {prod}', 'how many of its staff are on the minimum wage']),
          ('Discuss whether employment and consumer protection laws are a benefit or a burden for {b}.', ['set fair standards that build trust', 'reduce accidents and disputes', 'protect reputation'],
           ['compliance and legal costs', 'reduced flexibility in managing staff', 'slower launches of new {prod}'],
           ['how far the business already meets the standards', 'how strictly the laws are enforced', 'whether competitors abroad face similar laws'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def minwage_calc(r, D):
    c = r.choice(CASES)
    n = r.choice([40, 60, 80, 120, 150, 200, 250, 400])
    h = r.choice([35, 37.5, 40, 45])
    w1 = r.choice([6.0, 7.5, 8.0, 9.0, 10.0, 11.5, 12.0])
    rise = r.choice([5, 8, 10, 12, 15])
    w2 = w1 * (1 + rise / 100)
    wk = 52
    inc = n * h * wk * (w2 - w1)
    if D == 1:
        opts, ans = mc_num(r, w2, [w1 + rise / 10, w1 * rise / 100, w1 + rise], lambda x: money(x, 2))
        return {'stem': f'The minimum wage of ${num(w1)} per hour rises by {rise}%. What is the new minimum wage?', 'options': opts, 'answer': ans,
                'key': f'${num(w1)} × {1 + rise / 100:.2f} = {money(w2, 2)}.', 'marks': 1}
    stem = f'{c["full"]} employs {n} workers on the minimum wage, each working {num(h)} hours a week for {wk} weeks a year. The minimum wage rises by {rise}% from ${num(w1)} per hour. Calculate the increase in the annual wage bill for these workers'
    key = f'New rate = {money(w2, 2)} (+{money(w2 - w1, 2)}) [1]; increase = {n} × {num(h)} × {wk} × {money(w2 - w1, 3)} = {money(inc)} [1]'
    m = 2
    if D >= 3:
        P = r.choice([2, 3, 4, 5, 8]) * inc
        stem += f'. Its annual profit was {money(P)}. Calculate the percentage fall in profit if none of the cost is passed on'
        key += f'; % fall = {money(inc)}/{money(P)} × 100 = {pct(inc / P * 100)} [1]'
        m = 3
    if D >= 4:
        stem += ', and explain two ways the business could respond'
        key += '; responses: raise prices (depends on PED), improve productivity/automation, reduce hours, renegotiate other costs [2]'
        m = 5
    return {'stem': stem + '.', 'answer': money(inc) + (f'; profit falls by {pct(inc / P * 100)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m}


t = T(2, 'Social and demographic change; CSR', ['social and demographic change; corporate social responsibility', 'demographic change', 'corporate social responsibility', 'csr'],
      defs=[('corporate social responsibility (CSR)', 'The idea that a business should take account of the interests of all its stakeholders and society, not just its shareholders, when making decisions.'),
            ('demographic change', 'Changes in the structure of the population, such as its age profile, size, birth rate, migration and household composition.'),
            ('stakeholder', 'Any individual or group with an interest in, or affected by, the activities of a business, e.g. employees, customers, suppliers, local community.'),
            ('social audit', 'An independent report on the impact of a business\'s activities on employees, the community and the environment.')],
      mcqs=[('Which demographic change is most likely to increase demand for healthcare products?', 'An ageing population', ['A rising birth rate', 'Falling life expectancy', 'Emigration of older people'],
             'More older people increase demand for medicines, care and health services.'),
            ('Which is the best example of corporate social responsibility?', 'Paying suppliers in developing countries a fair price above the legal minimum', ['Cutting prices to increase market share', 'Paying the lowest legal wage', 'Raising dividends to shareholders'],
             'CSR means going beyond legal requirements to consider stakeholders and society.'),
            ('Why might a business publish a social audit?', 'To show stakeholders its social and environmental impact and build trust', ['Because it is required for all businesses', 'To calculate its tax bill', 'To reduce wages'],
             'Social audits are mostly voluntary and support reputation and accountability.')],
      exps=[('Explain why accepting corporate social responsibility might increase a firm\'s long-term profits.', 'A responsible image attracts customers and staff, reduces the risk of boycotts and fines, and can lower costs (e.g. less waste), raising long-run profit even if short-run costs rise.', '1 mark reputation/demand; 1 mark recruitment/retention or reduced risk; 1 mark short-run cost v long-run gain. [3]'),
            ('Explain one way an ageing population could affect a business\'s workforce planning.', 'More employees retire and fewer young people join, so the business may face skills shortages and need to retain older workers, retrain staff or recruit migrants.', '1 mark effect on labour supply; 1 mark planning response. [2]'),
            ('Explain why the interests of shareholders and the local community may conflict.', 'Shareholders want higher profit and dividends, which may mean cutting costs or relocating; the community wants jobs, a clean environment and support for local projects.', '1 mark shareholder objective; 1 mark community objective and conflict. [2]')],
      adv=[('adopting a strong corporate social responsibility policy', ['better brand image and customer loyalty', 'easier to recruit and keep staff', 'reduced risk of legal action or boycotts'],
            ['higher costs in the short run', 'may be seen as \'greenwashing\' if not genuine', 'shareholders may receive lower dividends']),
           ('targeting older consumers as the population of {country} ages', ['a growing market segment with high disposable income', 'less competition than youth markets', 'loyal customers once won'],
            ['products and promotion may need redesigning', 'risk of alienating younger customers', 'older consumers may be cautious spenders'])],
      anl=[('Analyse how changes in the age structure of the population of {country} could affect {b}.', ['demographic change alters the size and needs of market segments', 'demand for {prod} may rise or fall in different age groups', 'labour shortages if fewer young workers', 'need to adapt marketing mix and recruitment']),
           ('Analyse how {b} could benefit from publishing a social audit.', ['a social audit reports social and environmental impact', 'transparency builds trust with customers and investors', 'identifies areas to improve and cut waste', 'may attract ethical investors and staff'])],
      ev=[('Evaluate whether {b} should increase its spending on corporate social responsibility.', ['improves reputation and loyalty', 'helps recruitment and motivation', 'reduces risk of regulation and boycotts'],
           ['higher costs reduce short-term profit', 'benefits are hard to measure', 'customers may not pay more for ethical {prod}'],
           ['how important ethics are to its customers', 'its profitability and shareholders\' attitudes', 'whether the CSR is genuine and visible']),
          ('Discuss the extent to which social and demographic change is the most important external influence on {b}.', ['changes the size of its market segments', 'affects labour supply and skills', 'shifts consumer tastes'],
           ['economic factors such as incomes may matter more', 'technology and competition may be more urgent', 'demographic change is slow and predictable'],
           ['the time horizon being considered', 'the products it sells', 'how quickly it can adapt'])])


t = T(2, 'Technological change and environmental pressures', ['technological change and environmental pressures on business', 'technological change', 'environmental pressures'],
      defs=[('technological change', 'The development of new products, processes and ways of working through advances in knowledge, e.g. automation, artificial intelligence and e-commerce.'),
            ('carbon footprint', 'The total amount of greenhouse gases produced directly and indirectly by a business\'s activities, measured in tonnes of CO₂ equivalent.'),
            ('environmental audit', 'An assessment of the impact of a business on the environment, e.g. its emissions, energy use, waste and recycling.'),
            ('pressure group', 'An organisation that tries to influence business or government decisions on a particular issue without seeking political power, e.g. an environmental campaign group.')],
      mcqs=[('Which is most likely to be a benefit to a business of introducing new technology?', 'Lower unit costs through higher labour productivity', ['Lower initial capital cost', 'No need to train staff', 'Immediate rise in employee morale'],
             'Technology often raises productivity but needs investment and training.'),
            ('Why might a business respond to an environmental pressure group campaign?', 'To protect its reputation and sales', ['Because pressure groups can pass laws', 'Because campaigns always reduce costs', 'Because shareholders must obey pressure groups'],
             'Pressure groups influence customers and the media; firms respond to protect their brand.'),
            ('A carbon tax is introduced. Which business is likely to face the largest increase in costs?', 'A cement manufacturer using coal-fired kilns', ['An online tutoring business', 'A small accountancy practice', 'A software developer'],
             'The tax falls most heavily on energy-intensive, high-emission producers.')],
      exps=[('Explain why some employees resist the introduction of new technology.', 'They may fear job losses, loss of skills or status, and the stress of learning new methods; changes to routines create uncertainty.', '1 mark fear of redundancy/deskilling; 1 mark uncertainty/retraining. [2]'),
            ('Explain how reducing its environmental impact could lower a business\'s costs.', 'Using less energy and materials, recycling waste and avoiding fines or carbon taxes all cut costs.', '1 mark method; 1 mark link to cost saving. [2]'),
            ('Explain one way artificial intelligence could change the operations of a service business.', 'Chatbots and automated systems can handle routine customer queries 24 hours a day, cutting labour costs, while staff focus on complex cases.', '1 mark use; 1 mark effect on costs/quality. [2]')],
      adv=[('investing heavily in automation', ['lower unit labour costs', 'more consistent quality of {prod}', 'faster output and flexibility'],
            ['high capital cost and risk', 'possible redundancies and resistance', 'need for new technical skills']),
           ('setting a target of net-zero carbon emissions by 2035', ['attracts environmentally aware customers', 'lower long-run energy costs', 'protects against future carbon taxes'],
            ['high investment costs', 'may raise prices of {prod}', 'risk of criticism if the target is missed'])],
      anl=[('Analyse how rapid technological change in its industry could affect {b}.', ['technological change creates new products and processes', 'opportunity to cut costs and improve quality', 'risk that existing {prod} become obsolete', 'investment and retraining needed to keep up']),
           ('Analyse how pressure from customers and governments to reduce environmental damage could affect {b}.', ['environmental pressure from stakeholders and regulation', 'higher costs of cleaner processes and materials', 'opportunity to differentiate {prod} as sustainable', 'risk of reputational damage if it fails to act'])],
      ev=[('Evaluate whether {b} should invest in new technology to replace some of its workforce.', ['lower unit costs', 'higher quality and speed', 'keeps up with competitors'],
           ['high capital cost and uncertain returns', 'redundancy costs and morale', 'loss of flexibility or personal service'],
           ['the cost of labour in {country}', 'the availability of finance', 'how competitors are using technology']),
          ('Discuss whether becoming more environmentally sustainable will improve the competitiveness of {b}.', ['differentiation and brand image', 'lower energy and waste costs', 'avoids carbon taxes and fines'],
           ['higher short-term costs', 'customers may not pay a premium', 'rivals with lower costs may undercut it'],
           ['the attitudes of its target customers', 'the likely future regulation', 'the payback period of green investments'])])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def carbon_calc(r, D):
    c = r.choice(CASES)
    em = r.choice([2000, 4500, 8000, 12000, 20000, 35000])
    tax = r.choice([15, 20, 25, 30, 40, 50])
    cut = r.choice([20, 25, 30, 40])
    inv = em * cut / 100 * tax * r.choice([2, 2.5, 3, 4, 5])
    cost = em * tax
    saving = em * cut / 100 * tax
    if D == 1:
        opts, ans = mc_num(r, cost, [em / tax, tax * 100, cost / 10], lambda x: money(x))
        return {'stem': f'A firm emits {em:,} tonnes of CO₂ a year. A carbon tax of ${tax} per tonne is introduced. What is its annual carbon tax bill?', 'options': opts, 'answer': ans,
                'key': f'{em:,} × ${tax} = {money(cost)}.', 'marks': 1}
    stem = f'{c["full"]} emits {em:,} tonnes of CO₂ a year. The government introduces a carbon tax of ${tax} per tonne. Calculate the annual tax bill'
    key = f'{em:,} × ${tax} = {money(cost)} [1]'
    m = 1
    if D >= 2:
        stem += f'. New equipment costing {money(inv)} would cut emissions by {cut}%. Calculate the annual tax saving'
        key += f'; saving = {em:,} × {cut}% × ${tax} = {money(saving)} [1]'
        m = 2
    if D >= 3:
        stem += ' and the payback period of the equipment (ignoring other savings)'
        key += f'; payback = {money(inv)}/{money(saving)} = {num(inv / saving, 1)} years [1]'
        m = 3
    if D >= 4:
        stem += ', then recommend whether it should buy the equipment'
        key += '; recommendation weighs payback against equipment life, likely future rises in the tax, reputation and energy savings [1]'
        m = 4
    return {'stem': stem + '.', 'answer': money(cost) + (f'; saving {money(saving)} a year' if D >= 2 else '') + (f'; payback {num(inv / saving, 1)} years' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m}

# =====================================================================================
# 3 Business expansion and globalisation
# =====================================================================================

t = T(3, 'Mergers, takeovers and joint ventures', ['mergers, takeovers and joint ventures: reasons and impact', 'mergers takeovers', 'joint ventures'],
      defs=[('merger', 'An agreement by two businesses to combine into a single business, usually with the agreement of both sets of shareholders and managers.'),
            ('takeover', 'When one company buys a controlling interest (more than 50% of the shares) in another company.'),
            ('joint venture', 'Two or more businesses agree to share capital, risks and profits in a new, separately managed project or business.'),
            ('horizontal integration', 'A merger or takeover between two firms in the same industry at the same stage of production.'),
            ('vertical integration', 'A merger or takeover with a firm at a different stage of production in the same industry, either backward (towards suppliers) or forward (towards customers).'),
            ('synergy', 'The idea that the combined business will be more valuable or efficient than the two businesses operating separately ("2 + 2 = 5").')],
      mcqs=[('A chocolate manufacturer takes over a cocoa plantation. What type of integration is this?', 'Backward vertical integration', ['Forward vertical integration', 'Horizontal integration', 'Conglomerate integration'],
             'Buying a supplier at an earlier stage of production is backward vertical integration.'),
            ('Why do many takeovers fail to achieve the expected benefits?', 'Clashes of corporate culture and poor integration of the two businesses', ['They always reduce market share', 'Economies of scale cannot exist in large firms', 'Shareholders are not allowed to vote'],
             'Culture clashes, overpaying and integration problems are common causes of failure.'),
            ('A car maker buys a chain of car dealerships. This is', 'forward vertical integration', ['backward vertical integration', 'horizontal integration', 'a joint venture'],
             'Buying a business closer to the final consumer is forward vertical integration.'),
            ('Which is a key reason for forming a joint venture to enter a foreign market?', 'To share risks and gain a local partner\'s market knowledge', ['To gain full control of the foreign business', 'To avoid sharing any profits', 'To remove the need for any investment'],
             'Joint ventures share costs and risks and combine complementary knowledge.')],
      exps=[('Explain the difference between a merger and a takeover.', 'In a merger two firms agree to combine as equals; in a takeover one firm buys a controlling interest in another, which may be hostile.', '1 mark merger = agreed combination; 1 mark takeover = purchase of >50% of shares / control. [2]'),
            ('Explain two reasons why a business might choose a joint venture rather than a takeover.', 'A joint venture needs less capital and shares risk; it allows the partners to keep their independence and avoids paying a takeover premium; it can be easier to unwind.', '2 × (1 mark reason, 1 mark explanation). [4]'),
            ('Explain why a merger may lead to diseconomies of scale.', 'The larger firm may suffer communication problems, slower decisions, poor coordination and lower motivation, raising average costs.', '1 mark named diseconomy; 1 mark how it raises unit cost. [2]')],
      adv=[('taking over one of its suppliers', ['secures supplies of key inputs', 'captures the supplier\'s profit margin', 'more control over quality and delivery'],
            ['large capital cost', 'lack of expertise in a new stage of production', 'loss of flexibility to switch to cheaper suppliers']),
           ('forming a joint venture with a local firm in {newmkt}', ['shares the cost and risk of entry', 'gains local market knowledge and contacts', 'may overcome rules on foreign ownership'],
            ['profits are shared', 'disagreements over objectives and control', 'risk that know-how is copied by the partner'])],
      anl=[('Analyse the possible benefits to {b} of a horizontal merger with a competitor.', ['horizontal integration combines firms at the same stage', 'economies of scale lower unit costs', 'higher market share and pricing power', 'removes a rival and duplicated costs']),
           ('Analyse why a takeover of a foreign rival might fail to increase the profits of {b}.', ['takeovers often destroy value', 'overpaying through a large takeover premium', 'clash of corporate cultures lowers motivation', 'diseconomies of scale and integration costs'])],
      ev=[('Evaluate whether {b} should grow by takeover rather than by organic growth.', ['faster growth and immediate market share', 'gains existing brands, staff and know-how', 'removes a competitor'],
           ['high cost and takeover premium', 'culture clash and integration problems', 'organic growth is lower risk and keeps control'],
           ['the price of the target', 'compatibility of cultures and systems', 'how quickly it needs to grow']),
          ('Recommend whether {b} should enter {newmkt} through a joint venture or by setting up its own subsidiary.', ['a joint venture shares cost and risk', 'local partner knowledge', 'faster entry'],
           ['a subsidiary keeps full control and profit', 'protects know-how', 'avoids partner conflict'],
           ['how well it understands {newmkt}', 'its available finance', 'the legal rules on foreign ownership'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def takeover_calc(r, D):
    c, tgt = r.sample(CASES, 2)
    sh = r.choice([10, 20, 25, 40, 50, 80])          # million shares
    p = r.choice([2.40, 3.00, 4.50, 5.20, 6.00, 8.00, 12.50])
    prem = r.choice([20, 25, 30, 35, 40])
    offer = p * (1 + prem / 100)
    cost = offer * sh
    syn = r.choice([0.06, 0.08, 0.1, 0.12, 0.15]) * cost
    if D == 1:
        opts, ans = mc_num(r, offer, [p * prem / 100, p + prem / 10, p * (1 - prem / 100)], lambda x: money(x, 2))
        return {'stem': f'A company\'s shares trade at ${p:.2f}. A bidder offers a {prem}% premium. What is the offer price per share?', 'options': opts, 'answer': ans,
                'key': f'${p:.2f} × {1 + prem / 100:.2f} = {money(offer, 2)}.', 'marks': 1}
    stem = f'{c["full"]} plans to take over {tgt["full"]}, which has {sh} million shares trading at ${p:.2f}. To win control it offers a {prem}% premium. Calculate the offer price per share and the total cost of buying all the shares'
    key = f'Offer = ${p:.2f} × {1 + prem / 100:.2f} = {money(offer, 2)} [1]; cost = {sh}m × {money(offer, 2)} = {money(cost * 1e6)} [1]'
    m = 2
    if D >= 3:
        stem += f'. Managers expect cost savings (synergies) of {money(syn * 1e6)} a year. Calculate how many years of savings are needed to recover the premium paid'
        premium_total = (offer - p) * sh
        key += f'; premium paid = {sh}m × {money(offer - p, 2)} = {money(premium_total * 1e6)} [1]; years = {num(premium_total / syn, 1)} [1]'
        m = 4
    if D >= 5:
        stem += ', and evaluate whether the takeover is worthwhile'
        key += '; evaluation: synergies are often overestimated; integration and culture risks; strategic value of market share [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'{money(offer, 2)} per share; total {money(cost * 1e6)}' + (f'; about {num((offer - p) * sh / syn, 1)} years' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m,
            'type': 'numerical' if D < 4 else 'multi_step'}


t = T(3, 'Economies and diseconomies of scale', ['economies and diseconomies of scale', 'economies of scale', 'diseconomies of scale'],
      defs=[('economies of scale', 'Reductions in a firm\'s average (unit) costs of production that result from an increase in the scale of operation.'),
            ('diseconomies of scale', 'Increases in a firm\'s average costs that result from the scale of operation becoming too large, e.g. through poor communication and coordination.'),
            ('purchasing economies', 'Lower unit costs because a large firm can buy inputs in bulk and negotiate discounts from suppliers.'),
            ('external economies of scale', 'Reductions in average cost that a firm gains from the growth of its whole industry or area, e.g. a pool of skilled labour or specialist suppliers nearby.')],
      mcqs=[('A large supermarket chain obtains a 15% discount by buying in bulk. This is an example of', 'a purchasing economy of scale', ['a technical economy of scale', 'an external economy of scale', 'a diseconomy of scale'],
             'Bulk-buying discounts are purchasing (buying) economies.'),
            ('Which is a cause of diseconomies of scale?', 'Longer chains of command slowing down communication', ['Bulk-buying discounts', 'Cheaper borrowing for large firms', 'Use of specialist machinery'],
             'Diseconomies come from coordination, communication and motivation problems in very large organisations.'),
            ('Which economy of scale arises because large firms are seen as less risky by lenders?', 'Financial economies', ['Marketing economies', 'Technical economies', 'Managerial economies'],
             'Large firms can borrow more cheaply and raise capital more easily.')],
      exps=[('Explain how technical economies of scale reduce average costs.', 'Large firms can afford specialised, high-capacity machinery and production lines whose high fixed cost is spread over a very large output.', '1 mark large/specialist equipment; 1 mark fixed cost spread over more units. [2]'),
            ('Explain why a very large business may suffer from lower employee motivation.', 'Workers feel remote from senior managers and their contribution seems small, communication is slow and impersonal, so they feel undervalued.', '1 mark distance/alienation; 1 mark effect on motivation/productivity. [2]'),
            ('Explain the difference between internal and external economies of scale.', 'Internal economies come from the growth of the firm itself (e.g. bulk buying); external economies come from the growth of the industry or area (e.g. specialist suppliers locating nearby).', '1 mark internal; 1 mark external with example. [2]')],
      adv=[('doubling its scale of production', ['bulk-buying discounts lower unit costs', 'more efficient specialist machinery', 'cheaper finance and wider marketing reach'],
            ['communication and coordination problems', 'lower staff motivation', 'risk of overcapacity if demand does not grow'])],
      anl=[('Analyse how {b} could benefit from economies of scale as it grows.', ['economies of scale reduce average cost as output rises', 'purchasing economies on inputs for {prod}', 'technical and financial economies', 'lower unit costs allow lower prices or higher margins']),
           ('Analyse the diseconomies of scale {b} might experience if it doubles in size.', ['diseconomies raise average cost at large scale', 'longer chains of command slow decisions', 'coordination problems between departments or sites', 'lower motivation and higher labour turnover'])],
      ev=[('Evaluate whether {b} should aim to become much larger in order to gain economies of scale.', ['lower unit costs and better margins', 'stronger bargaining power', 'more funds for research and marketing'],
           ['diseconomies of scale', 'loss of flexibility and customer focus', 'demand may not support larger output'],
           ['the size of the market for {prod}', 'how well its management can control a larger organisation', 'competitors\' costs']),
          ('Discuss the extent to which large businesses always have a competitive advantage over small ones in the {sector} sector.', ['economies of scale', 'brand recognition and marketing budgets', 'access to finance'],
           ['small firms are more flexible and personal', 'niche markets reward specialisation', 'diseconomies of scale in large firms'],
           ['the nature of the product and market', 'the importance of personal service', 'the minimum efficient scale in the industry'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def scale_calc(r, D):
    c = r.choice(CASES)
    FC = r.choice([200, 300, 400, 500, 600, 800]) * 1000
    v = r.choice([4, 5, 6, 8, 10, 12])
    q1 = r.choice([20, 25, 40, 50]) * 1000
    q2 = q1 * r.choice([2, 3, 4])
    ac1, ac2 = FC / q1 + v, FC / q2 + v
    if D == 1:
        opts, ans = mc_num(r, ac1, [FC / q1, v, (FC + v) / q1], lambda x: money(x, 2))
        return {'stem': f'A factory has fixed costs of {money(FC)} a month and variable costs of ${v} per unit. What is the average cost per unit at an output of {q1:,} units?', 'options': opts, 'answer': ans,
                'key': f'AC = FC/Q + AVC = {money(FC)}/{q1:,} + ${v} = {money(ac1, 2)}.', 'marks': 1}
    stem = f'{c["full"]} has monthly fixed costs of {money(FC)} and variable costs of ${v} per unit. Calculate the average cost per unit at outputs of {q1:,} and {q2:,} units'
    key = f'AC at {q1:,} = {money(FC)}/{q1:,} + {v} = {money(ac1, 2)} [1]; AC at {q2:,} = {money(ac2, 2)} [1]'
    m = 2
    if D >= 3:
        disc = r.choice([5, 10, 15])
        v2 = v * (1 - disc / 100)
        ac3 = FC / q2 + v2
        stem += f'. At the higher output, bulk buying cuts variable cost by {disc}%. Calculate the new average cost at {q2:,} units'
        key += f'; AVC = {money(v2, 2)}, AC = {money(FC / q2, 2)} + {money(v2, 2)} = {money(ac3, 2)} [1]'
        m = 3
        if D >= 4:
            stem += ' and identify the two economies of scale shown'
            key += '; spreading fixed costs (technical/indivisibilities) and purchasing economies [1]'
            m = 4
        if D >= 5:
            stem += '. Explain why average costs might rise if output grew much further'
            key += '; diseconomies: communication, coordination, motivation; capacity constraints/overtime [1]'
            m = 5
    return {'stem': stem + '.', 'answer': f'{money(ac1, 2)} and {money(ac2, 2)}' + (f'; {money(ac3, 2)} with the discount' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m,
            'type': 'numerical' if D < 4 else 'multi_step'}


t = T(3, 'Globalisation and multinational corporations', ['globalisation and multinational corporations (mncs)', 'globalisation', 'multinational', 'mnc'],
      defs=[('globalisation', 'The growing integration of the world\'s economies through increased trade, movement of capital, people, ideas and technology across borders.'),
            ('multinational corporation (MNC)', 'A business with its headquarters in one country and production or service operations in at least one other country.'),
            ('foreign direct investment (FDI)', 'Investment by a business in productive assets (e.g. factories, offices) in another country.'),
            ('transfer pricing', 'The prices one part of a multinational charges another part in a different country, which can be set to shift profits to low-tax countries.')],
      mcqs=[('Which is a likely benefit to a host country of an MNC opening a factory there?', 'New jobs and transfer of skills and technology', ['Lower competition for local firms in every case', 'Guaranteed higher tax revenue in every case', 'Profits always stay in the host country'],
             'FDI brings jobs, training, technology and investment, though profits may be repatriated.'),
            ('Which development has contributed most to globalisation?', 'Lower transport and communication costs', ['Higher import tariffs', 'Stricter controls on capital movements', 'Fewer international trade agreements'],
             'Cheaper shipping, air freight and the internet make trade across borders easier.'),
            ('Why might an MNC use transfer pricing?', 'To declare more of its profit in countries with low tax rates', ['To pay its workers more', 'To increase the price paid by final consumers', 'To comply with minimum wage laws'],
             'Internal prices can shift profits between countries to reduce the total tax paid.')],
      exps=[('Explain two reasons why a business may decide to become a multinational.', 'To be closer to foreign customers and avoid tariffs and transport costs; to use cheaper labour or resources; to spread risk across several economies.', '2 × (1 mark reason, 1 mark explanation). [4]'),
            ('Explain one potential disadvantage to a host country of a large MNC operating there.', 'Profits may be sent back to the home country, local firms may be forced out, and the MNC may exploit weak labour or environmental laws.', '1 mark disadvantage; 1 mark explanation. [2]'),
            ('Explain how globalisation increases competition for domestic businesses.', 'Lower trade barriers and cheaper transport let foreign firms sell into the domestic market, so local firms face more rivals on price and quality.', '1 mark entry of foreign rivals; 1 mark effect on price/quality pressure. [2]')],
      adv=[('becoming a multinational by opening a production site in {newmkt}', ['closer to customers, lower transport costs', 'avoids import tariffs', 'access to cheaper labour or resources'],
            ['high set-up cost and risk', 'cultural and legal differences', 'difficulty controlling distant operations']),
           ('increasing globalisation of its industry', ['larger export markets for {prod}', 'access to cheaper global suppliers', 'economies of scale from selling worldwide'],
            ['more foreign competition at home', 'exposure to exchange-rate risk', 'pressure on prices and costs'])],
      anl=[('Analyse how increasing globalisation is likely to affect {b}.', ['globalisation integrates world markets', 'new export opportunities for {prod}', 'more intense competition from overseas firms', 'access to global supply chains, but more exposure to disruption']),
           ('Analyse the possible impact on the economy of {country} if a large foreign MNC built a factory competing with {b}.', ['FDI creates jobs and raises incomes', 'technology and skills spill over to local firms', 'local firms such as {b} face stronger competition', 'profits may be repatriated'])],
      ev=[('Evaluate whether {b} should become a multinational by setting up operations in {newmkt}.', ['access to a large new market', 'lower costs or avoiding tariffs', 'spreads risk across economies'],
           ['high cost and risk', 'cultural and legal differences', 'control and communication difficulties'],
           ['the size and growth of the market in {newmkt}', 'political and economic stability there', 'its management experience abroad']),
          ('Discuss whether the benefits of MNCs to a country such as {country} outweigh the costs.', ['jobs and investment', 'technology transfer and training', 'tax revenue and exports'],
           ['repatriation of profits', 'local firms like {b} may be forced out', 'possible exploitation of weak regulation'],
           ['the terms negotiated by the government', 'the behaviour (CSR) of the MNC', 'how long the MNC stays'])])


t = T(3, 'Protectionism and trade blocs', ['protectionism and trade blocs', 'protectionism', 'trade blocs', 'tariffs quotas'],
      defs=[('protectionism', 'Government measures that restrict imports to protect domestic industries from foreign competition, e.g. tariffs, quotas and subsidies.'),
            ('tariff', 'A tax on imported goods, which raises their price in the domestic market.'),
            ('import quota', 'A physical limit on the quantity or value of a good that may be imported in a given period.'),
            ('trade bloc', 'A group of countries that agree to reduce or remove trade barriers between themselves, e.g. a free trade area or customs union.')],
      mcqs=[('Which is an example of a protectionist measure?', 'A 25% tax on imported steel', ['A cut in corporation tax', 'A free trade agreement', 'A rise in the minimum wage'],
             'A tariff is a tax on imports and protects domestic producers.'),
            ('A country joins a trade bloc. Which business is most likely to gain?', 'A domestic exporter selling to other member countries', ['A firm that relied on tariffs to protect it from member-country rivals', 'A firm that imports only from non-members', 'A firm with no international links'],
             'Removing tariffs between members helps exporters to member countries.'),
            ('What is the main difference between a customs union and a free trade area?', 'A customs union also sets a common external tariff on imports from non-members', ['A free trade area has a single currency', 'A customs union has no free trade between members', 'A free trade area sets a common external tariff'],
             'Customs union = free trade between members + common external tariff.')],
      exps=[('Explain how a tariff on imported components could affect a domestic manufacturer.', 'The components become more expensive, so unit costs rise; the firm must raise prices or accept lower margins, or switch to domestic suppliers.', '1 mark higher costs; 1 mark consequence (price/margin/supplier switch). [2]'),
            ('Explain why a government might introduce protectionist measures.', 'To protect jobs and infant industries, to respond to dumping, or to reduce a trade deficit.', '1 mark reason; 1 mark explanation. [2]'),
            ('Explain one advantage for a business of its country being a member of a trade bloc.', 'Tariff-free access to a larger market of member countries allows higher sales and economies of scale.', '1 mark tariff-free/larger market; 1 mark consequence. [2]')],
      adv=[('{country} introducing tariffs on competing imported {prod}', ['imported rivals become more expensive', 'higher domestic sales and market share', 'less pressure to cut prices'],
            ['other countries may retaliate against its exports', 'imported inputs may also become dearer', 'less pressure to become efficient']),
           ('{country} joining a regional trade bloc', ['tariff-free access to member markets', 'cheaper inputs from members', 'economies of scale from a larger market'],
            ['more competition from member-country firms', 'common external tariff may raise costs of some imports', 'new regulations to follow'])],
      anl=[('Analyse how tariffs placed on its exports by a major trading partner could affect {b}.', ['a tariff is a tax on imports', 'its {prod} become more expensive in that market', 'export sales and margins fall', 'it may look for other markets or produce inside the tariff wall']),
           ('Analyse the likely effects on {b} if {country} joined a free trade area with its neighbours.', ['a free trade area removes tariffs between members', 'larger market for exports', 'more competition at home', 'cheaper imported inputs from member countries'])],
      ev=[('Evaluate the likely impact on {b} of rising protectionism in world trade.', ['domestic market may be protected', 'local rivals face fewer imports', 'government support for home firms'],
           ['export markets restrict access', 'retaliation and higher input costs', 'supply chains disrupted'],
           ['how much it exports and imports', 'which countries introduce barriers', 'its ability to relocate production']),
          ('Discuss whether {b} should set up production inside a trade bloc to avoid its common external tariff.', ['avoids tariffs and becomes price competitive', 'closer to customers', 'tariff-free access to every member'],
           ['high investment cost and risk', 'possibly higher labour costs', 'management of distant operations'],
           ['the size of the tariff', 'the importance of the bloc\'s market to sales', 'the likelihood of a future trade deal'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def tariff_calc(r, D):
    c = r.choice(CASES)
    imp = r.choice([40, 50, 60, 80, 100, 120, 150, 200])
    tar = r.choice([10, 15, 20, 25, 30, 40])
    dom = imp * r.choice([1.1, 1.15, 1.2, 1.25, 1.3])
    landed = imp * (1 + tar / 100)
    if D == 1:
        opts, ans = mc_num(r, landed, [imp * tar / 100, imp + tar, imp * (1 - tar / 100)], lambda x: money(x, 2))
        return {'stem': f'An imported product costs ${imp} before tax. The government imposes a {tar}% tariff. What is its price after the tariff?', 'options': opts, 'answer': ans,
                'key': f'${imp} × {1 + tar / 100:.2f} = {money(landed, 2)}.', 'marks': 1}
    stem = (f'{c["full"]} sells a product in {c["country"]} for {money(dom, 2)}. A similar imported product sells for ${imp}. The government imposes a {tar}% tariff on imports, '
            f'which is passed on in full. Calculate the new price of the imported product and the price difference between the two products')
    key = f'Import price = ${imp} × {1 + tar / 100:.2f} = {money(landed, 2)} [1]; difference = {money(abs(landed - dom), 2)} ({"import now dearer" if landed > dom else "import still cheaper"}) [1]'
    m = 2
    if D >= 3:
        stem += '. State which product is now cheaper and explain one likely effect on the business'
        key += f'; {"domestic product cheaper → sales/market share of " + c["b"] + " likely to rise" if landed > dom else "import still cheaper → limited benefit to " + c["b"]} [1]'
        m = 3
    if D >= 4:
        stem += ', and evaluate whether the tariff will benefit the business in the long run'
        key += '; evaluation: retaliation against exports, higher imported input costs, less pressure to be efficient, consumer welfare loss [2]'
        m = 5
    return {'stem': stem + '.', 'answer': f'{money(landed, 2)}; difference {money(abs(landed - dom), 2)}', 'key': key + f'. [{m}]', 'marks': m,
            'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 4 Human resource management strategy
# =====================================================================================

t = T(4, 'Hard and soft HRM', ['hard and soft hrm approaches', 'hard hrm', 'soft hrm', 'workforce planning'],
      defs=[('hard HRM', 'An approach that treats employees as a resource to be used as efficiently as possible, with a focus on cost control, short-term contracts and close monitoring.'),
            ('soft HRM', 'An approach that treats employees as valuable assets whose commitment is developed through training, involvement, consultation and long-term career development.'),
            ('workforce planning', 'Analysing the current workforce and forecasting the number and skills of employees the business will need in future, then planning how to meet the gap.'),
            ('human resource management (HRM)', 'The strategic approach to recruiting, developing, rewarding and managing people so that they help the business achieve its objectives.')],
      mcqs=[('Which policy is most closely associated with soft HRM?', 'Long-term training and career development for all staff', ['Paying the lowest possible wages', 'Using short-term contracts to cut costs', 'Close supervision with little consultation'],
             'Soft HRM sees staff as assets to be developed and involved.'),
            ('Which policy is most closely associated with hard HRM?', 'Hiring temporary staff when demand rises and releasing them when it falls', ['Empowering teams to make decisions', 'Regular consultation with employees', 'Paying for staff to gain qualifications'],
             'Hard HRM treats labour as a cost to be matched to demand.'),
            ('What is the first stage of workforce planning?', 'Forecasting the future demand for labour from the business\'s objectives', ['Dismissing surplus staff', 'Setting the minimum wage', 'Appraising each employee'],
             'Planning starts with the future labour requirement, then compares it with current and future supply.')],
      exps=[('Explain the difference between hard HRM and soft HRM.', 'Hard HRM treats workers as a cost to be minimised and controlled; soft HRM treats them as assets to be developed, consulted and motivated for the long term.', '1 mark hard; 1 mark soft. [2]'),
            ('Explain why a business facing strong price competition might adopt a hard HRM approach.', 'It must keep unit labour costs low, so it matches staffing to demand, uses flexible contracts and controls pay closely.', '1 mark cost pressure; 1 mark hard methods used. [2]'),
            ('Explain two benefits of workforce planning to a growing business.', 'It identifies future skill shortages early so recruitment and training can be planned; it avoids over- or under-staffing and the costs they cause.', '2 × (1 mark benefit, 1 mark explanation). [4]')],
      adv=[('adopting a soft HRM approach', ['higher commitment and motivation', 'lower labour turnover and recruitment costs', 'better ideas from involved employees'],
            ['higher training and consultation costs', 'slower decision-making', 'benefits are long-term and hard to measure']),
           ('adopting a hard HRM approach', ['lower and more controllable labour costs', 'easy to adjust staff numbers to demand', 'clear performance targets'],
            ['low motivation and loyalty', 'high labour turnover', 'poor reputation as an employer'])],
      anl=[('Analyse how {b} could benefit from moving from a hard to a soft HRM approach.', ['soft HRM treats staff as assets', 'training raises productivity and quality of {prod}', 'involvement increases motivation (e.g. Herzberg motivators)', 'lower labour turnover cuts recruitment costs']),
           ('Analyse how workforce planning could help {b} achieve its objectives.', ['workforce planning forecasts labour demand and supply', 'identifies skills gaps before they cause problems', 'plans recruitment, training or redeployment', 'controls labour costs'])],
      ev=[('Evaluate whether {b} should adopt a soft rather than a hard approach to HRM.', ['motivated, loyal staff', 'better quality and innovation', 'lower turnover'],
           ['higher costs of training and consultation', 'competitive pressure on costs', 'some roles suit flexible contracts'],
           ['the skills its staff need', 'its competitive strategy (cost or differentiation)', 'its corporate culture']),
          ('Discuss the importance of workforce planning for {b} over the next five years.', ['avoids skills shortages', 'controls labour costs', 'supports growth plans'],
           ['forecasts may be inaccurate', 'labour market changes quickly', 'flexible contracts can fill gaps'],
           ['how fast the business grows', 'the availability of skilled labour in {country}', 'the quality of its data'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def wfp_calc(r, D):
    c = r.choice(CASES)
    out = r.choice([48000, 60000, 72000, 90000, 120000, 150000])
    g = r.choice([10, 20, 25, 50])
    prod = r.choice([400, 500, 600, 750, 800, 1000, 1200])
    now = out // prod
    need = out * (1 + g / 100) / prod
    need = math.ceil(need)
    lt = r.choice([8, 10, 12, 15, 20])
    leavers = round(now * lt / 100)
    rec = need - (now - leavers)
    if D == 1:
        opts, ans = mc_num(r, now, [out * prod, out / 100, now * 2], lambda x: f'{round(x):,}')
        return {'stem': f'A factory produces {out:,} units a year and each worker produces {prod:,} units a year. How many workers does it employ?', 'options': opts, 'answer': ans,
                'key': f'{out:,} / {prod:,} = {now:,} workers.', 'marks': 1}
    stem = f'{c["full"]} produces {out:,} units a year with {now} production workers, each producing {prod:,} units a year. Output is planned to rise by {g}% next year with no change in productivity. Calculate the number of workers needed next year'
    key = f'Output = {out:,} × {1 + g / 100} = {round(out * (1 + g / 100)):,} [1]; workers = {round(out * (1 + g / 100)):,}/{prod:,} = {need} [1]'
    m = 2
    if D >= 3:
        stem += f'. Labour turnover is {lt}% a year. Calculate how many workers must be recruited'
        key += f'; leavers = {lt}% × {now} = {leavers} [1]; recruits = {need} − ({now} − {leavers}) = {rec} [1]'
        m = 4
    if D >= 5:
        stem += ', and explain one non-recruitment way of meeting the requirement'
        key += '; e.g. raise productivity via training/technology, overtime, temporary or zero-hours staff, outsourcing [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'{need} workers' + (f'; recruit {rec}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(4, 'Workforce flexibility and the gig economy', ['workforce flexibility, zero-hours contracts and the gig economy', 'zero-hours', 'gig economy', 'flexible workforce'],
      defs=[('zero-hours contract', 'An employment contract under which the employer does not guarantee any minimum number of hours, and the worker is paid only for hours actually worked.'),
            ('gig economy', 'A labour market in which many people work on short-term, task-by-task contracts, often arranged through online platforms, rather than in permanent jobs.'),
            ('flexible workforce', 'A workforce whose size, hours, location or skills can be changed quickly to match the needs of the business, e.g. part-time, temporary and multi-skilled staff.'),
            ('outsourcing', 'Using another business to carry out activities that were previously done within the organisation.')],
      mcqs=[('Which is the main benefit to an employer of zero-hours contracts?', 'Labour costs can be matched closely to fluctuating demand', ['Workers are guaranteed regular income', 'Staff loyalty is always higher', 'Training costs disappear'],
             'The employer pays only for hours needed.'),
            ('Which is a disadvantage of the gig economy for workers?', 'Irregular income and few employment rights such as sick pay', ['They must work fixed hours', 'They cannot choose when to work', 'They always earn less than the minimum wage'],
             'Gig workers are often self-employed and lack security and benefits.'),
            ('A multi-skilled worker who can do several jobs is an example of', 'functional flexibility', ['numerical flexibility', 'temporal flexibility', 'locational flexibility'],
             'Functional flexibility = staff able to switch between tasks.')],
      exps=[('Explain why zero-hours contracts may reduce employee motivation.', 'Uncertain hours and income threaten security needs (Maslow), so workers feel less valued and less committed, and may leave when they find secure work.', '1 mark insecurity of income/hours; 1 mark link to motivation theory or turnover. [2]'),
            ('Explain one benefit to a business of using gig-economy workers rather than permanent employees.', 'It pays only for completed tasks and avoids costs such as holiday pay and pensions, so costs fall and it can scale up or down quickly.', '1 mark benefit; 1 mark explanation. [2]'),
            ('Explain the difference between numerical flexibility and functional flexibility.', 'Numerical flexibility changes the number of workers or hours (e.g. temporary, part-time staff); functional flexibility means existing staff can perform different tasks.', '1 mark each. [2]')],
      adv=[('employing most of its staff on zero-hours contracts', ['labour costs match seasonal demand', 'no pay for idle time', 'easy to adjust staff levels'],
            ['low motivation and loyalty', 'high labour turnover and training costs', 'damage to reputation and service quality']),
           ('outsourcing some of its non-core activities to gig-economy workers', ['lower fixed costs', 'access to specialist skills when needed', 'management can focus on core activities'],
            ['less control over quality', 'workers may lack commitment', 'risk of legal challenges over employment status'])],
      anl=[('Analyse how {b} could benefit from a more flexible workforce.', ['flexibility matches labour to demand', 'lower labour cost per unit of output', 'multi-skilled staff cover absences', 'faster response to changes in demand for {prod}']),
           ('Analyse the possible effects on employees and customers if {b} moves many staff onto zero-hours contracts.', ['zero-hours contracts give no guaranteed hours', 'insecurity lowers motivation and loyalty', 'higher turnover may reduce service quality', 'customers may react to reputational damage'])],
      ev=[('Evaluate whether {b} should increase its use of zero-hours contracts.', ['matches labour costs to demand', 'reduces idle time', 'flexibility for some workers who want it'],
           ['low motivation and high turnover', 'reputation as an employer', 'possible future legal restrictions'],
           ['how much demand fluctuates', 'the skills and training each job needs', 'what competitors offer']),
          ('Discuss whether the growth of the gig economy is good for businesses such as {b}.', ['lower and flexible labour costs', 'access to wide pool of skills', 'quick scaling'],
           ['less loyalty and control', 'quality risks', 'ethical and legal concerns'],
           ['the type of work involved', 'how far quality depends on staff commitment', 'the legal position in {country}'])])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def flex_calc(r, D):
    c = r.choice(CASES)
    n = r.choice([10, 12, 15, 20, 25, 30])
    sal = r.choice([18000, 20000, 22000, 24000, 26000])
    hr = r.choice([12, 13, 14, 15, 16])
    hrs = [r.choice([150, 200, 250, 300, 400, 500]) for _ in range(4)]
    perm = n * sal
    if D == 1:
        opts, ans = mc_num(r, perm, [sal, n * sal / 12, n + sal], lambda x: money(x))
        return {'stem': f'A firm employs {n} permanent staff, each paid ${sal:,} a year. What is the annual cost of these salaries?', 'options': opts, 'answer': ans, 'key': f'{n} × ${sal:,} = {money(perm)}.', 'marks': 1}
    stem = (f'{c["full"]} needs up to {n} workers in its busy season. It could employ {n} permanent staff on ${sal:,} a year each, or use zero-hours staff paid ${hr} per hour. '
            f'Forecast hours needed per worker are {", ".join(str(h) for h in hrs)} in quarters 1 to 4. Calculate the annual cost of each option')
    key = f'Permanent: {n} × ${sal:,} = {money(perm)} [1]; zero-hours: {n} × ({" + ".join(str(h) for h in hrs)}) = {n * sum(hrs):,} hours × ${hr} = {money(n * sum(hrs) * hr)} [1]'
    zh = n * sum(hrs) * hr
    m = 2
    if D >= 3:
        stem += ' and the saving from the cheaper option'
        key += f'; difference = {money(abs(perm - zh))} in favour of {"zero-hours" if zh < perm else "permanent staff"} [1]'
        m = 3
    if D >= 4:
        stem += '. Recommend which option to choose, giving one non-financial factor'
        key += '; recommendation uses cost result plus motivation/training/service quality/availability of staff [1]'
        m = 4
    return {'stem': stem + '.', 'answer': f'Permanent {money(perm)}; zero-hours {money(zh)}', 'key': key + f'. [{m}]', 'marks': m}


t = T(4, 'Measuring HR performance', ['measuring hr performance: absenteeism, labour productivity, turnover', 'labour turnover', 'absenteeism', 'labour productivity'],
      defs=[('labour turnover', 'The percentage of a firm\'s workforce that leaves during a year: number leaving ÷ average number employed × 100.'),
            ('absenteeism rate', 'The percentage of possible working days lost through staff absence: days lost ÷ total possible working days × 100.'),
            ('labour productivity', 'Output per worker in a given period: total output ÷ number of employees.'),
            ('labour retention rate', 'The percentage of employees with a given length of service (e.g. one year or more) who are still employed at the end of the period.')],
      mcqs=[('Which is most likely to cause high labour turnover?', 'Low pay and poor working conditions compared with other local employers', ['Good promotion prospects', 'Recent pay increases', 'High job security'],
             'Staff leave for better pay and conditions elsewhere.'),
            ('A rise in labour productivity, with wage rates unchanged, will', 'reduce unit labour costs', ['increase unit labour costs', 'increase absenteeism', 'reduce output per worker'],
             'Unit labour cost = labour cost ÷ output; more output per worker spreads the wage bill.'),
            ('Which is a cost of high labour turnover?', 'Spending on recruitment and induction training', ['Lower wage bills', 'Fewer new ideas', 'More experienced staff'],
             'High turnover means frequent recruitment, training and lost productivity.')],
      exps=[('Explain why a high rate of absenteeism may indicate a problem with motivation.', 'Workers who are dissatisfied or stressed are more likely to take days off; Herzberg\'s hygiene factors (conditions, supervision) may be poor.', '1 mark link to dissatisfaction; 1 mark cause/theory. [2]'),
            ('Explain why some labour turnover can benefit a business.', 'New staff bring fresh ideas and skills, and leavers can be replaced with lower-paid or better-matched recruits, or not replaced if cutting costs.', '1 mark benefit; 1 mark explanation. [2]'),
            ('Explain how labour productivity could be increased.', 'Training, better equipment and technology, improved motivation (e.g. bonuses, job enrichment) and better organisation of work.', '1 mark method; 1 mark how it raises output per worker. [2]')],
      adv=[('introducing a bonus scheme linked to labour productivity', ['higher output per worker', 'lower unit labour costs', 'rewards the most productive staff'],
            ['quality may fall as staff rush', 'conflict if targets seem unfair', 'measurement can be difficult in services'])],
      anl=[('Analyse the possible causes and consequences of rising labour turnover at {b}.', ['labour turnover measures the proportion of staff leaving', 'causes: pay, conditions, poor management, better jobs elsewhere', 'consequences: recruitment and training costs, lost productivity', 'customer service and quality of {prod} may suffer']),
           ('Analyse how {b} could use measures of HR performance to improve its competitiveness.', ['HR metrics include productivity, absenteeism and turnover', 'benchmarking metrics identifies problems', 'targeted action (training, pay, job design)', 'lower unit costs and better quality'])],
      ev=[('Evaluate the best way for {b} to reduce its labour turnover.', ['higher pay and benefits', 'training and career paths', 'job enrichment and involvement (Herzberg)'],
           ['pay rises increase costs', 'non-financial methods take time', 'some turnover is healthy'],
           ['the main reasons staff are leaving', 'the cost of each method', 'what local competitors offer']),
          ('Discuss whether labour productivity is the most useful measure of HR performance for {b}.', ['links directly to unit costs', 'easy to compare over time', 'shows effect of training and technology'],
           ['ignores quality and customer service', 'turnover and absenteeism reveal motivation problems', 'hard to measure in services'],
           ['the nature of its work', 'the reliability of the data', 'its strategic priorities'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def hr_calc(r, D):
    c = r.choice(CASES)
    kind = r.randrange(3)
    if kind == 0:
        start = r.choice([200, 240, 300, 360, 400, 480, 520])
        end = start + r.choice([-40, -20, 0, 20, 40, 60])
        avg = (start + end) / 2
        left = round(avg * r.choice([0.08, 0.12, 0.15, 0.18, 0.22, 0.25]))
        lt = left / avg * 100
        if D == 1:
            opts, ans = mc_num(r, lt, [left / start * 100 + 3, left / 10, 100 - lt], lambda x: pct(x))
            return {'stem': f'A business had an average of {num(avg, 1)} employees during the year and {left} left. What was its labour turnover?', 'options': opts, 'answer': ans,
                    'key': f'{left}/{num(avg, 1)} × 100 = {pct(lt)}.', 'marks': 1}
        stem = f'{c["full"]} had {start} employees at the start of the year and {end} at the end. During the year {left} employees left. Calculate the labour turnover rate'
        key = f'Average employees = ({start} + {end})/2 = {num(avg, 1)} [1]; turnover = {left}/{num(avg, 1)} × 100 = {pct(lt)} [1]'
        m = 2
        if D >= 3:
            ind = r.choice([8, 10, 12, 15, 18])
            rc = r.choice([1500, 2000, 2500, 3000])
            stem += f'. The industry average is {ind}% and replacing each leaver costs about ${rc:,}. Calculate the cost of labour turnover above the industry average'
            extra = max(0, left - ind / 100 * avg)
            key += f'; leavers at industry rate = {ind}% × {num(avg, 1)} = {num(ind / 100 * avg, 1)}; excess = {num(extra, 1)} × ${rc:,} = {money(extra * rc)} [2]'
            m = 4
            if D >= 5:
                stem += ', and suggest one reason for the difference'
                key += '; reason linked to pay, conditions, management style, local labour market [1]'
                m = 5
        return {'stem': stem + '.', 'answer': pct(lt) + (f'; excess cost {money(extra * rc)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}
    if kind == 1:
        staff = r.choice([50, 80, 120, 150, 200, 250])
        days = r.choice([220, 225, 230, 240, 250])
        lost = round(staff * days * r.choice([0.02, 0.03, 0.04, 0.05, 0.06, 0.08]))
        ab = lost / (staff * days) * 100
        if D == 1:
            opts, ans = mc_num(r, ab, [lost / staff, lost / days, ab * 10], lambda x: pct(x))
            return {'stem': f'A firm has {staff} staff who could each work {days} days a year. In total {lost:,} days were lost to absence. What is the absenteeism rate?', 'options': opts, 'answer': ans,
                    'key': f'{lost:,}/({staff} × {days}) × 100 = {pct(ab)}.', 'marks': 1}
        stem = f'At {c["full"]}\'s main site, {staff} employees could each work {days} days a year. Last year {lost:,} working days were lost through absence. Calculate the absenteeism rate'
        key = f'Possible days = {staff} × {days} = {staff * days:,} [1]; rate = {lost:,}/{staff * days:,} × 100 = {pct(ab)} [1]'
        m = 2
        if D >= 3:
            dc = r.choice([80, 100, 120, 150])
            stem += f'. Each day of absence costs ${dc} in cover and lost output. Calculate the annual cost of absence and the saving if the rate fell to 2%'
            sav = (lost - 0.02 * staff * days) * dc
            key += f'; cost = {lost:,} × ${dc} = {money(lost * dc)} [1]; saving = ({lost:,} − {round(0.02 * staff * days):,}) × ${dc} = {money(sav)} [1]'
            m = 4
            if D >= 5:
                stem += '. Suggest one way to achieve this reduction'
                key += '; e.g. return-to-work interviews, better conditions, flexible working, job enrichment [1]'
                m = 5
        return {'stem': stem + '.', 'answer': pct(ab) + (f'; cost {money(lost * dc)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}
    e1 = r.choice([40, 50, 60, 80, 100, 120])
    o1 = e1 * r.choice([400, 500, 600, 800, 900, 1000, 1200])
    e2 = e1 + r.choice([-10, -5, 5, 10, 20])
    o2 = round(o1 * r.choice([0.95, 1.0, 1.05, 1.1, 1.2, 1.25]))
    p1, p2 = o1 / e1, o2 / e2
    if D == 1:
        opts, ans = mc_num(r, p1, [o1 * e1, e1 / o1 * 1000, p1 / 2], lambda x: f'{num(x, 1)} units')
        return {'stem': f'A factory with {e1} workers produced {o1:,} units last month. What is its labour productivity?', 'options': opts, 'answer': ans, 'key': f'{o1:,}/{e1} = {num(p1, 1)} units per worker.', 'marks': 1}
    stem = f'{c["full"]} produced {o1:,} units with {e1} workers last year and {o2:,} units with {e2} workers this year. Calculate labour productivity in each year'
    key = f'Year 1: {o1:,}/{e1} = {num(p1, 1)}; year 2: {o2:,}/{e2} = {num(p2, 1)} units per worker [2]'
    m = 2
    if D >= 3:
        stem += ' and the percentage change in productivity'
        key += f'; change = {(p2 / p1 - 1) * 100:+.1f}% [1]'
        m = 3
    if D >= 4:
        w = r.choice([20000, 24000, 30000, 36000])
        stem += f'. Each worker is paid ${w:,} a year. Calculate the labour cost per unit in each year'
        key += f'; ULC = ${w:,}/{num(p1, 1)} = {money(w / p1, 2)} → ${w:,}/{num(p2, 1)} = {money(w / p2, 2)} [1]'
        m = 4
    return {'stem': stem + '.', 'answer': f'{num(p1, 1)} → {num(p2, 1)} units per worker' + (f' ({(p2 / p1 - 1) * 100:+.1f}%)' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(4, 'Employer-employee relations', ['employer-employee relations: trade unions, collective bargaining and acas', 'trade unions', 'collective bargaining', 'acas'],
      defs=[('trade union', 'An organisation of workers that aims to protect and improve its members\' pay, conditions and job security through collective action.'),
            ('collective bargaining', 'Negotiation between employers and representatives of the workforce (usually trade unions) over pay and conditions for a whole group of employees.'),
            ('conciliation', 'A method of resolving industrial disputes in which an independent third party (e.g. ACAS) helps both sides talk and reach their own agreement.'),
            ('arbitration', 'A method of resolving disputes in which an independent third party hears both sides and makes a decision, which may be binding.'),
            ('industrial action', 'Measures taken by employees to put pressure on their employer during a dispute, e.g. strikes, work-to-rule and overtime bans.')],
      mcqs=[('Which is an example of industrial action short of a strike?', 'A work-to-rule', ['A lock-out by the employer', 'Arbitration', 'A no-strike agreement'],
             'Work-to-rule, go-slows and overtime bans are action short of a strike.'),
            ('What is the role of ACAS (or a similar independent body) in an industrial dispute?', 'To provide independent conciliation and arbitration', ['To represent the employer in court', 'To set the national minimum wage', 'To organise strike ballots'],
             'ACAS is an independent advisory, conciliation and arbitration service.'),
            ('In which form of arbitration must the arbitrator choose either the union\'s or the employer\'s final offer?', 'Pendulum arbitration', ['Non-binding arbitration', 'Conciliation', 'Collective bargaining'],
             'Pendulum arbitration discourages extreme claims because only one final position can win.')],
      exps=[('Explain one benefit to an employer of negotiating with a trade union rather than with individual employees.', 'Collective bargaining saves time and cost because one agreement covers many workers, and union representatives communicate decisions to members.', '1 mark benefit; 1 mark explanation. [2]'),
            ('Explain the difference between conciliation and arbitration.', 'In conciliation a third party helps the two sides reach their own agreement; in arbitration the third party decides the outcome.', '1 mark each. [2]'),
            ('Explain why a no-strike agreement may benefit both employers and employees.', 'Employers gain certainty of production; employees usually gain improved consultation, pay deals or binding arbitration in return.', '1 mark employer benefit; 1 mark employee benefit. [2]')],
      adv=[('recognising a trade union for collective bargaining', ['one negotiation covers many workers', 'better communication with staff', 'workers feel represented, raising morale'],
            ['stronger bargaining power of workers can raise costs', 'risk of industrial action', 'slower change and restrictions on flexibility']),
           ('agreeing to binding arbitration in future disputes', ['avoids costly strikes', 'faster resolution', 'independent and seen as fair'],
            ['loss of control over the outcome', 'arbitrator may award higher pay than planned', 'may reduce incentive to negotiate'])],
      anl=[('Analyse how a strike by its employees could affect {b}.', ['industrial action disrupts production and service', 'lost output of {prod} and missed orders', 'damage to customer relationships and reputation', 'long-term worsening of employee relations']),
           ('Analyse the benefits to {b} of good employer-employee relations.', ['good relations come from consultation and trust', 'fewer disputes and lost working days', 'easier to introduce change', 'higher motivation and productivity'])],
      ev=[('Evaluate how {b} should respond to a trade union demand for a 10% pay rise.', ['accepting avoids industrial action', 'improves morale and retention', 'conciliation through an independent body may find a compromise'],
           ['higher costs and lower margins', 'may set expectations for future claims', 'productivity deal may be better'],
           ['its profitability and price elasticity', 'the likely cost of a strike', 'pay rates offered by competitors']),
          ('Discuss whether trade unions are beneficial to businesses such as {b}.', ['efficient channel for communication', 'help manage change', 'protect against poor management practices'],
           ['raise labour costs', 'industrial action risk', 'reduce flexibility'],
           ['the relationship between managers and union', 'the culture of the business', 'the legal framework in {country}'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def union_calc(r, D):
    c = r.choice(CASES)
    n = r.choice([200, 300, 400, 500, 800, 1000])
    w = r.choice([18000, 20000, 24000, 28000, 30000])
    claim = r.choice([6, 8, 10, 12])
    offer = r.choice([x for x in (2, 3, 4, 5) if x < claim])
    bill = n * w
    gap = bill * (claim - offer) / 100
    if D == 1:
        opts, ans = mc_num(r, bill * claim / 100, [bill, w * claim / 100, bill * offer / 100], lambda x: money(x))
        return {'stem': f'A firm employs {n} workers paid ${w:,} a year. The union claims a {claim}% pay rise. What would this add to the annual wage bill?', 'options': opts, 'answer': ans,
                'key': f'{n} × ${w:,} × {claim}% = {money(bill * claim / 100)}.', 'marks': 1}
    stem = f'At {c["full"]}, {n} unionised workers are each paid ${w:,} a year. The union claims a {claim}% pay rise; management offers {offer}%. Calculate the annual cost of the difference between the claim and the offer'
    key = f'Wage bill = {money(bill)} [1]; difference = {claim - offer}% × {money(bill)} = {money(gap)} [1]'
    m = 2
    if D >= 3:
        cpd = r.choice([20000, 30000, 40000, 50000, 80000])
        sd = r.choice([3, 5, 7, 10])
        stem += f'. A strike would cost about {money(cpd)} of lost contribution per day. Calculate the cost of a {sd}-day strike and compare it with the difference'
        key += f'; strike cost = {sd} × {money(cpd)} = {money(sd * cpd)} [1]; strike is {"more" if sd * cpd > gap else "less"} costly than one year of the difference [1]'
        m = 4
        if D >= 5:
            stem += '. Recommend how management should respond'
            key += '; recommendation weighs one-off strike cost against recurring pay cost, morale, reputation, possibility of conciliation/productivity deal [1]'
            m = 5
    return {'stem': stem + '.', 'answer': money(gap) + (f'; strike cost {money(sd * cpd)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 5 Organisational structure
# =====================================================================================

t = T(5, 'Hierarchy, span of control and delayering', ['hierarchy, span of control, chain of command and delayering', 'span of control', 'delayering', 'chain of command'],
      defs=[('hierarchy', 'The levels of management and authority in an organisation, from the most senior to the most junior.'),
            ('span of control', 'The number of subordinates who report directly to one manager or supervisor.'),
            ('chain of command', 'The route through which authority passes down and communication passes up and down an organisation.'),
            ('delayering', 'Removing one or more levels of the management hierarchy, which usually widens spans of control.')],
      mcqs=[('Delayering an organisation usually results in', 'wider spans of control and a shorter chain of command', ['narrower spans of control', 'more levels of hierarchy', 'a longer chain of command'],
             'Removing management layers means each remaining manager has more direct reports.'),
            ('A narrow span of control is most appropriate when', 'tasks are complex and staff need close supervision', ['staff are highly skilled and experienced', 'the business wants to cut management costs', 'tasks are simple and routine'],
             'Close supervision suits complex or high-risk work and inexperienced staff.'),
            ('Which is a likely disadvantage of a long chain of command?', 'Messages are distorted and decisions are slow', ['Managers have too many subordinates', 'There are few promotion opportunities', 'Staff are over-empowered'],
             'More layers slow communication and increase distortion.')],
      exps=[('Explain the link between the span of control and the number of levels of hierarchy.', 'For a given number of employees, wider spans of control mean fewer levels are needed, so the structure is flatter; narrow spans create more levels (a tall structure).', '1 mark inverse relationship; 1 mark tall v flat. [2]'),
            ('Explain two possible drawbacks of delayering.', 'Remaining managers may be overloaded with wider spans; loss of experienced staff and promotion opportunities can reduce morale; redundancy costs.', '2 × (1 mark drawback, 1 mark explanation). [4]'),
            ('Explain why a wide span of control may motivate skilled employees.', 'Managers cannot supervise closely, so staff gain autonomy and responsibility, which are Herzberg motivators.', '1 mark less supervision/more autonomy; 1 mark link to motivation. [2]')],
      adv=[('delayering its management structure', ['lower salary costs of managers', 'faster communication and decisions', 'more empowerment for remaining staff'],
            ['overloaded managers with wide spans', 'fewer promotion opportunities', 'redundancy costs and low morale among survivors'])],
      anl=[('Analyse how delayering could affect the efficiency of {b}.', ['delayering removes management levels', 'lower overhead costs from fewer managers', 'shorter chain of command speeds decisions', 'wider spans may reduce control and overload managers']),
           ('Analyse the factors that should determine the most suitable span of control for managers at {b}.', ['span of control = number of direct subordinates', 'skills and experience of staff', 'complexity of the tasks', 'management style and use of technology to monitor work'])],
      ev=[('Evaluate whether {b} should delayer its organisational structure.', ['lower costs', 'faster decisions and communication', 'empowerment and motivation'],
           ['overloaded managers', 'loss of experience and promotion paths', 'short-term disruption and redundancy costs'],
           ['the skills of its staff', 'how fast its market changes', 'how the change is managed']),
          ('Discuss whether a tall structure with narrow spans of control is suitable for {b}.', ['close supervision and control', 'clear promotion ladder', 'suits complex or high-risk tasks'],
           ['slow communication', 'high management costs', 'less empowerment'],
           ['the nature of its work', 'its size and number of sites', 'its corporate culture'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def span_calc(r, D):
    c = r.choice(CASES)
    s = r.choice([3, 4, 5, 6])
    L = r.choice([4, 5])
    total = sum(s ** i for i in range(L))
    bottom = s ** (L - 1)
    if D == 1:
        opts, ans = mc_num(r, s ** 2, [s * 2, s + 2, s ** 3], lambda x: f'{round(x)}')
        return {'stem': f'In an organisation, every manager has a span of control of {s}. How many employees are at level 3 of the hierarchy (the managing director is level 1)?', 'options': opts, 'answer': ans,
                'key': f'Level 1: 1; level 2: {s}; level 3: {s} × {s} = {s ** 2}.', 'marks': 1}
    stem = f'{c["full"]} has a structure with {L} levels in one division. Everyone above the bottom level has a span of control of {s}. Calculate the number of employees at the bottom level and in total'
    key = f'Bottom level = {s}^{L - 1} = {bottom} [1]; total = ' + ' + '.join(str(s ** i) for i in range(L)) + f' = {total} [1]'
    m = 2
    if D >= 3:
        sal = r.choice([40000, 45000, 50000, 60000])
        lvl2 = s ** (L - 2)
        stem += f'. The business removes level {L - 1} (the {lvl2} junior managers, each paid ${sal:,}) and the {bottom} bottom-level staff now report to the level {L - 2} managers. Calculate the new span of control of these managers and the annual salary saving'
        new_span = bottom // (s ** (L - 3))
        key += f'; new span = {bottom}/{s ** (L - 3)} = {new_span} [1]; saving = {lvl2} × ${sal:,} = {money(lvl2 * sal)} [1]'
        m = 4
        if D >= 5:
            stem += '. Evaluate one risk of this change'
            key += f'; e.g. span of {new_span} may overload managers, reduce supervision and support, lower morale [1]'
            m = 5
    return {'stem': stem + '.', 'answer': f'{bottom} at the bottom level, {total} in total' + (f'; new span {bottom // (s ** (L - 3))}, saving {money(s ** (L - 2) * sal)}' if D >= 3 else ''),
            'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(5, 'Functional, matrix and flat structures', ['functional, matrix and flat structures', 'matrix structure', 'functional structure', 'flat structure'],
      defs=[('functional structure', 'An organisational structure in which the business is divided into departments by function, such as marketing, finance, operations and HR.'),
            ('matrix structure', 'A structure in which staff from different functional departments are organised into project teams, so each employee reports to both a functional manager and a project manager.'),
            ('flat structure', 'An organisational structure with few levels of hierarchy and wide spans of control.'),
            ('product-based (divisional) structure', 'A structure in which the business is divided into divisions, each responsible for one product range or geographical region, with its own functional departments.')],
      mcqs=[('In which structure might an employee report to two managers at the same time?', 'Matrix structure', ['Functional structure', 'Tall hierarchical structure', 'Sole-trader structure'],
             'In a matrix, staff report to a functional head and a project leader.'),
            ('Which is a likely advantage of a flat structure?', 'Faster communication between senior managers and employees', ['More promotion opportunities', 'Narrow spans of control', 'Close supervision of every worker'],
             'Fewer layers mean shorter communication channels.'),
            ('A multinational organises itself into Asian, European and American divisions. This is', 'a geographical (divisional) structure', ['a matrix structure', 'a functional structure', 'an informal structure'],
             'Divisions based on regions form a geographical structure.')],
      exps=[('Explain one advantage and one disadvantage of a matrix structure.', 'Advantage: brings together specialists from different functions, improving coordination and innovation on projects. Disadvantage: two bosses can cause conflicting instructions and confusion.', '1 mark advantage + explanation; 1 mark disadvantage + explanation. [2]'),
            ('Explain why a growing multinational might change from a functional to a divisional structure.', 'As product ranges or markets multiply, divisions allow decisions to be made close to each market and managers to be accountable for each division\'s profit.', '1 mark reason; 1 mark explanation. [2]'),
            ('Explain why a functional structure may lead to poor coordination between departments.', 'Departments focus on their own objectives ("silo" thinking), so marketing, operations and finance may not share information or agree priorities.', '1 mark departmental focus; 1 mark consequence. [2]')],
      adv=[('introducing a matrix structure for new product projects', ['combines specialist skills', 'faster innovation', 'better coordination across functions'],
            ['two bosses causes conflict', 'higher administration costs', 'unclear accountability']),
           ('reorganising into product divisions', ['decisions made close to each market', 'clear profit accountability', 'easier to add new divisions'],
            ['duplication of functions raises costs', 'rivalry between divisions', 'loss of economies of scale in support functions'])],
      anl=[('Analyse the benefits to {b} of introducing a matrix structure.', ['matrix structure combines functional and project teams', 'specialists work together on new products such as {newprod}', 'faster and more innovative problem solving', 'better use of skills across the business']),
           ('Analyse how a change to a flatter structure might affect the employees of {b}.', ['flat structure has fewer layers and wider spans', 'more responsibility and empowerment', 'fewer promotion opportunities', 'possible insecurity during restructuring'])],
      ev=[('Evaluate the most suitable organisational structure for {b} as it expands into {newmkt}.', ['divisional structure gives local responsiveness', 'matrix helps cross-functional projects', 'functional keeps specialist expertise and control'],
           ['divisions duplicate costs', 'matrix creates conflict', 'functional structures respond slowly to local needs'],
           ['the differences between markets', 'its size and growth rate', 'the skills of its managers']),
          ('Discuss whether changing its organisational structure is the best way for {b} to improve communication.', ['fewer layers and shorter chains', 'project teams share information', 'clear lines of accountability'],
           ['culture and leadership matter more', 'technology can improve communication without restructuring', 'restructuring is disruptive'],
           ['the cause of current communication problems', 'how employees react to change', 'the cost of restructuring'])])


t = T(5, 'Delegation, centralisation and decentralisation', ['delegation, centralisation and decentralisation', 'delegation', 'centralisation', 'decentralisation'],
      defs=[('delegation', 'Passing authority to make decisions and complete tasks down the hierarchy to subordinates, while the manager keeps overall responsibility.'),
            ('centralisation', 'Keeping decision-making authority at the top of the organisation or at head office.'),
            ('decentralisation', 'Passing decision-making authority from head office to managers in branches, regions or divisions.'),
            ('empowerment', 'Giving employees the authority, resources and confidence to make decisions about their own work.')],
      mcqs=[('Which is an advantage of decentralised decision-making for a multinational?', 'Local managers can respond quickly to local market conditions', ['All branches follow identical policies', 'Head office has complete control', 'It always reduces management costs'],
             'Decentralisation puts decisions close to customers.'),
            ('Which situation favours centralisation?', 'A crisis that requires quick, consistent decisions across the business', ['Very different local markets', 'Highly skilled local managers', 'A desire to motivate branch staff'],
             'In a crisis, central control gives fast, coordinated responses.'),
            ('When a manager delegates a task, which of the following is retained by the manager?', 'Overall responsibility for the outcome', ['Authority to complete the task', 'All the work involved', 'The right to make every minor decision'],
             'Authority can be delegated, but ultimate responsibility cannot.')],
      exps=[('Explain why delegation might motivate employees.', 'It gives more responsibility, trust and opportunity for achievement, which are Herzberg motivators and help meet esteem and self-actualisation needs.', '1 mark responsibility/trust; 1 mark motivation theory link. [2]'),
            ('Explain two reasons why a manager may be unwilling to delegate.', 'They may lack trust in subordinates\' ability; fear losing control or being blamed for mistakes; think it is quicker to do it themselves.', '2 × (1 mark reason, 1 mark explanation). [4]'),
            ('Explain one disadvantage of decentralisation for a business with a strong brand.', 'Local managers may make inconsistent decisions on pricing, promotion or quality, damaging the consistent brand image.', '1 mark inconsistency; 1 mark effect on brand. [2]')],
      adv=[('decentralising decision-making to its regional managers', ['faster response to local customers', 'motivates local managers', 'senior managers free to focus on strategy'],
            ['inconsistent policies and brand image', 'duplication of functions', 'local managers may lack the skills']),
           ('centralising all purchasing at head office', ['bulk-buying discounts', 'consistent quality of inputs', 'tighter cost control'],
            ['slower response to local needs', 'local managers less motivated', 'head office overloaded'])],
      anl=[('Analyse the benefits to {b} of delegating more decisions to its employees.', ['delegation passes authority down the hierarchy', 'faster decisions close to the customer', 'higher motivation (Herzberg responsibility, Maslow esteem)', 'frees senior managers to plan strategy']),
           ('Analyse why {b} might choose to centralise decision-making.', ['centralisation keeps authority at head office', 'consistent policies and image', 'tighter control of costs and quality', 'uses experienced senior managers'])],
      ev=[('Evaluate whether {b} should decentralise decision-making.', ['faster local responses', 'motivated local managers', 'senior managers focus on strategy'],
           ['loss of consistency and control', 'duplication of costs', 'local managers may lack skills'],
           ['how different its markets are', 'the quality of its local managers', 'the importance of a consistent brand']),
          ('Discuss the extent to which delegation will improve the performance of {b}.', ['better motivation', 'quicker decisions', 'develops future managers'],
           ['risk of mistakes', 'staff may lack training or want responsibility', 'needs good communication and control'],
           ['the training of staff', 'the management style used', 'the type of decisions delegated'])])


t = T(5, 'Informal organisation and line vs staff roles', ['informal organisation and line vs staff roles', 'informal organisation', 'line and staff'],
      defs=[('informal organisation', 'The network of personal relationships, groups and communication channels that develops between employees outside the formal structure.'),
            ('line manager', 'A manager with direct authority over subordinates in the chain of command, responsible for their performance.'),
            ('staff role', 'A specialist role that gives advice and support to line managers but has no direct authority over the line employees, e.g. legal or HR advisers.'),
            ('formal organisation', 'The official structure of roles, reporting lines and communication channels set out in the organisation chart.')],
      mcqs=[('A company lawyer advises the production director on a contract. The lawyer is in a', 'staff role', ['line role', 'matrix role', 'informal role'],
             'Staff roles advise and support without line authority.'),
            ('Which is an example of the informal organisation?', 'A group of colleagues who share information over lunch', ['The organisation chart', 'A job description', 'The official reporting line to a supervisor'],
             'Informal networks develop through friendships and social contact.'),
            ('A possible problem between line and staff managers is that', 'line managers may resent advice from specialists with no line responsibility', ['staff managers have too many subordinates', 'line managers cannot give instructions', 'staff managers control the chain of command'],
             'Conflict arises when line managers see specialist advice as interference.')],
      exps=[('Explain how managers could use the informal organisation to help introduce change.', 'By identifying informal leaders and involving them early, managers can spread accurate information through the grapevine and reduce resistance.', '1 mark use of informal leaders/grapevine; 1 mark effect on resistance. [2]'),
            ('Explain the difference between line and staff roles.', 'Line roles have direct authority over subordinates in the chain of command; staff roles give specialist advice and support but do not command line employees.', '1 mark each. [2]'),
            ('Explain one risk to a business of a strong informal organisation.', 'Rumours spread quickly through the grapevine and groups may develop norms that oppose management targets, reducing productivity.', '1 mark risk; 1 mark explanation. [2]')],
      adv=[('making use of the informal organisation when communicating with staff', ['messages spread quickly', 'informal leaders can build support', 'feedback on staff feelings'],
            ['messages may be distorted', 'rumours can undermine managers', 'informal groups may resist change'])],
      anl=[('Analyse how the informal organisation could affect the success of a new working method at {b}.', ['informal organisation = networks outside formal structure', 'informal leaders can support or oppose change', 'grapevine spreads information or rumours quickly', 'group norms influence productivity (Mayo)']),
           ('Analyse the possible conflicts between line managers and specialist staff advisers at {b}.', ['line managers have authority, staff roles advise', 'line managers may ignore or resent advice', 'specialists may lack practical knowledge of operations', 'unclear responsibility slows decisions'])],
      ev=[('Evaluate the importance of the informal organisation to the managers of {b}.', ['influences motivation and group norms', 'fast communication channel', 'informal leaders can help change'],
           ['formal structure sets authority and accountability', 'informal networks can spread rumours', 'hard to control or measure'],
           ['the culture and size of the business', 'how much change is planned', 'the relationship between managers and staff']),
          ('Discuss whether {b} should employ more specialist staff advisers to support its line managers.', ['expert advice improves decisions', 'compliance with law and regulation', 'frees line managers to manage'],
           ['higher overhead costs', 'conflict with line managers', 'advice may be ignored'],
           ['the complexity of its operations', 'its size', 'whether advice could be bought in when needed'])])

# =====================================================================================
# 6 Marketing analysis
# =====================================================================================

t = T(6, 'Elasticity of demand', ['price, income and promotional elasticity of demand', 'price elasticity', 'income elasticity', 'promotional elasticity'],
      defs=[('price elasticity of demand (PED)', 'The responsiveness of quantity demanded to a change in price: % change in quantity demanded ÷ % change in price.'),
            ('income elasticity of demand (YED)', 'The responsiveness of quantity demanded to a change in consumer incomes: % change in quantity demanded ÷ % change in income.'),
            ('promotional elasticity of demand', 'The responsiveness of quantity demanded to a change in promotional (advertising) spending: % change in quantity demanded ÷ % change in promotional spending.'),
            ('cross elasticity of demand', 'The responsiveness of demand for one product to a change in the price of another product: % change in quantity demanded of A ÷ % change in price of B.')],
      mcqs=[('If demand for a product is price inelastic, a price rise will', 'increase total revenue', ['reduce total revenue', 'leave quantity demanded unchanged', 'always reduce profit'],
             'With |PED| < 1 the % fall in quantity is smaller than the % rise in price.'),
            ('A product has an income elasticity of demand of −0.6. It is', 'an inferior good', ['a luxury good', 'a normal necessity', 'price elastic'],
             'Negative YED means demand falls as incomes rise.'),
            ('Which factor tends to make demand more price elastic?', 'Many close substitutes', ['Strong brand loyalty', 'The product is a necessity', 'It takes a small share of income'],
             'Close substitutes let customers switch when price rises.')],
      exps=[('Explain why knowledge of price elasticity of demand is useful when setting prices.', 'It shows how quantity and revenue will respond: if demand is inelastic a price rise increases revenue; if elastic, a price cut may increase revenue.', '1 mark predicts quantity/revenue response; 1 mark applied to pricing decision. [2]'),
            ('Explain two limitations of using elasticity estimates for marketing decisions.', 'They are based on past data and conditions change; other factors (competitors\' prices, incomes, tastes) do not stay constant; estimates may only be valid for small price changes.', '2 × (1 mark limitation, 1 mark explanation). [4]'),
            ('Explain why a business would prefer the demand for its product to be price inelastic.', 'It can raise prices with only a small loss of sales, so revenue and margins rise; it is less vulnerable to rivals\' price cuts.', '1 mark pricing power; 1 mark effect on revenue/profit. [2]')],
      adv=[('making demand for its {prod} less price elastic through branding', ['able to raise prices without losing many customers', 'higher revenue and margins', 'less vulnerable to price competition'],
            ['heavy promotional spending needed', 'takes time to build loyalty', 'premium image may limit mass-market sales'])],
      anl=[('Analyse how {b} could use estimates of price and income elasticity of demand to plan its marketing.', ['PED shows revenue response to price changes', 'YED shows how demand changes over the business cycle', 'set prices to maximise revenue or profit', 'plan production and promotion for forecast demand']),
           ('Analyse why the price elasticity of demand for {bp} {prod} might change over time.', ['PED depends on substitutes, brand loyalty, necessity and share of income', 'new competitors create closer substitutes', 'branding and quality can reduce elasticity', 'changes in income alter price sensitivity'])],
      ev=[('Evaluate whether {b} should raise the price of its {prod} by 10%.', ['higher revenue if demand is price inelastic', 'higher margins', 'premium image'],
           ['sales fall sharply if demand is elastic', 'competitors may not follow', 'brand loyalty could suffer'],
           ['the estimated price elasticity', 'competitors\' likely reaction', 'its objectives (market share or profit)']),
          ('Discuss the usefulness of elasticity of demand calculations for {b}.', ['help forecast effects of price and promotion', 'guide pricing strategy', 'help plan for the business cycle'],
           ['estimates rely on past data', 'other things do not stay equal', 'hard to measure accurately'],
           ['the quality of its market data', 'how stable its market is', 'how decisions also use qualitative judgement'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ped_calc(r, D):
    c = r.choice(CASES)
    kind = r.randrange(3)
    P = r.choice([4, 5, 8, 10, 12, 15, 20, 25, 40, 50])
    Q = r.choice([10000, 12000, 20000, 25000, 40000, 50000])
    if kind == 0:
        dp = r.choice([-20, -10, -5, 5, 10, 20])
        e = r.choice([-0.4, -0.5, -0.8, -1.5, -2.0, -2.5])
        dq = e * dp
        P2, Q2 = P * (1 + dp / 100), Q * (1 + dq / 100)
        R1, R2 = P * Q, P2 * Q2
        if D == 1:
            opts, ans = mc_num(r, e, [dp / dq if dq else 1, -e, e * 2], lambda x: num(x))
            return {'stem': f'A {abs(dp)}% {"rise" if dp > 0 else "cut"} in price leads to a {abs(dq):g}% {"fall" if dq < 0 else "rise"} in quantity demanded. What is the price elasticity of demand?', 'options': opts, 'answer': ans,
                    'key': f'PED = %ΔQ/%ΔP = {dq:+g}/{dp:+} = {num(e)}.', 'marks': 1}
        stem = f'{c["full"]} sells {Q:,} units a month at ${P}. It plans to {"raise" if dp > 0 else "cut"} the price by {abs(dp)}%. The price elasticity of demand is estimated at {e}. Calculate the new monthly sales volume'
        key = f'%ΔQ = {e} × {dp:+} = {dq:+g}% [1]; new volume = {Q:,} × {1 + dq / 100:g} = {round(Q2):,} [1]'
        m = 2
        if D >= 3:
            stem += ' and the change in total revenue'
            key += f'; revenue {money(R1)} → {money(P2, 2)} × {round(Q2):,} = {money(R2)}, change {"+" if R2 >= R1 else "−"}{money(abs(R2 - R1))} [1]'
            m = 3
        if D >= 4:
            stem += '. Explain whether the price change is a sensible decision'
            key += f'; demand is price {"inelastic" if abs(e) < 1 else "elastic"} so revenue {"rises" if R2 > R1 else "falls"}; also consider costs/contribution, rivals\' reaction, accuracy of estimate [1]'
            m = 4
        return {'stem': stem + '.', 'answer': f'{round(Q2):,} units' + (f'; revenue changes by {"+" if R2 >= R1 else "−"}{money(abs(R2 - R1))}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}
    if kind == 1:
        A1 = r.choice([20000, 40000, 50000, 80000, 100000])
        da = r.choice([10, 20, 25, 40, 50])
        pe = r.choice([0.2, 0.3, 0.4, 0.5, 0.6])
        dq = pe * da
        Q2 = Q * (1 + dq / 100)
        if D == 1:
            opts, ans = mc_num(r, pe, [da / dq, dq, pe * 10], lambda x: num(x))
            return {'stem': f'Advertising spending rises by {da}% and sales volume rises by {dq:g}%. What is the promotional elasticity of demand?', 'options': opts, 'answer': ans,
                    'key': f'Promotional elasticity = {dq:g}/{da} = {num(pe)}.', 'marks': 1}
        stem = f'{c["full"]} sells {Q:,} units a month at ${P}. It increases monthly advertising spending from {money(A1)} by {da}%. The promotional elasticity of demand is {pe}. Calculate the new monthly sales volume'
        key = f'%ΔQ = {pe} × {da} = {dq:g}% [1]; new volume = {round(Q2):,} [1]'
        m = 2
        if D >= 3:
            cm = r.choice([0.3, 0.4, 0.5]) * P
            extra_c = (Q2 - Q) * cm
            extra_a = A1 * da / 100
            stem += f'. Each unit gives a contribution of {money(cm, 2)}. Calculate whether the extra contribution covers the extra advertising cost'
            key += f'; extra contribution = {round(Q2 - Q):,} × {money(cm, 2)} = {money(extra_c)} [1]; extra advertising = {money(extra_a)} [1]; {"worthwhile" if extra_c > extra_a else "not covered"} [1]'
            m = 5
        return {'stem': stem + '.', 'answer': f'{round(Q2):,} units' + (f'; extra contribution {money(extra_c)} v extra cost {money(extra_a)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}
    dy = r.choice([-5, -4, -2, 2, 4, 5])
    y0 = r.choice([2.5, 2.0, 1.5, 0.5, -0.5, -1.0])
    Q1 = Q
    Q2 = round(Q * (1 + y0 * dy / 100))
    dq = (Q2 / Q1 - 1) * 100
    y = dq / dy
    if D == 1:
        opts, ans = mc_num(r, y, [dy / dq, -y, dq], lambda x: num(x))
        return {'stem': f'Average incomes change by {dy:+}% and the quantity demanded of a product changes by {dq:+.0f}%. What is its income elasticity of demand?', 'options': opts, 'answer': ans,
                'key': f'YED = {dq:+.0f}/{dy:+} = {num(y)}.', 'marks': 1}
    stem = f'Average real incomes in {c["country"]} changed by {dy:+}% last year. Monthly sales of one of {c["bp"]} product lines changed from {Q1:,} to {round(Q2):,} units, with prices unchanged. Calculate the income elasticity of demand'
    key = f'%ΔQ = ({round(Q2):,} − {Q1:,})/{Q1:,} × 100 = {dq:+.1f}% [1]; YED = {dq:+.1f}/{dy:+} = {num(y)} [1]'
    m = 2
    if D >= 3:
        typ = 'a luxury (income elastic)' if y > 1 else ('a normal necessity' if y > 0 else 'an inferior good')
        stem += ' and state what type of product this suggests'
        key += f'; {typ} [1]'
        m = 3
        if D >= 4:
            stem += '. Explain one implication for the business if a recession is forecast'
            key += f'; implication: sales likely to {"fall" if y > 0 else "rise"} {"strongly " if abs(y) > 1 else ""}in a recession — adjust production, promotion or product portfolio [1]'
            m = 4
    return {'stem': stem + '.', 'answer': f'YED = {num(y)}', 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(6, 'Sales forecasting', ['sales forecasting: moving averages and trend extrapolation', 'moving averages', 'sales forecasting', 'trend extrapolation'],
      defs=[('sales forecasting', 'Predicting future sales volume or value, using quantitative methods (e.g. moving averages) and/or qualitative methods (e.g. expert opinion).'),
            ('moving average', 'An average of a fixed number of consecutive data values, recalculated each period, used to smooth out fluctuations and reveal the trend.'),
            ('seasonal variation', 'The difference between an actual value and the trend value, caused by regular patterns within a year (e.g. higher sales in December).'),
            ('extrapolation', 'Extending a trend line beyond the existing data to forecast future values.')],
      mcqs=[('Why is a four-quarter moving average "centred"?', 'Because the average of four quarters falls between two quarters, so two averages are averaged to line up with a quarter', ['To remove the trend', 'To calculate the seasonal variation directly', 'Because it uses only odd numbers of data'],
             'An even-period moving average must be centred to match a specific period.'),
            ('What is the main purpose of calculating a moving average of sales data?', 'To identify the underlying trend by smoothing out short-term fluctuations', ['To calculate profit', 'To find the highest sales figure', 'To measure market share'],
             'Moving averages remove seasonal and random variation.'),
            ('Which is a key limitation of trend extrapolation?', 'It assumes past patterns will continue into the future', ['It cannot use numerical data', 'It ignores the trend', 'It is too expensive for any business'],
             'External changes (competition, economy) can break the trend.')],
      exps=[('Explain why a business might use qualitative forecasting methods as well as moving averages.', 'Moving averages only project the past; expert opinion or the Delphi method can allow for new products, competitors or economic shocks that the data do not show.', '1 mark limitation of quantitative methods; 1 mark benefit of qualitative. [2]'),
            ('Explain how accurate sales forecasts help the operations department.', 'They allow capacity, staffing and inventory to be planned, avoiding shortages or excess stock.', '1 mark planning; 1 mark consequence. [2]'),
            ('Explain what is meant by random variation in sales data and why it makes forecasting difficult.', 'Random variations are unpredictable changes (e.g. weather, strikes) not explained by trend or season; they cannot be forecast, so forecasts may be inaccurate.', '1 mark meaning; 1 mark difficulty. [2]')],
      adv=[('using moving averages to forecast sales of its {prod}', ['identifies the trend and seasonal pattern', 'based on objective data', 'helps plan inventory and staffing'],
            ['assumes the past continues', 'ignores external changes', 'needs several years of data'])],
      anl=[('Analyse how more accurate sales forecasts could improve the performance of {b}.', ['sales forecasting predicts future demand', 'better capacity and workforce planning', 'lower inventory holding and fewer stock-outs', 'more accurate cash-flow forecasts and budgets']),
           ('Analyse the factors that could make {bp} sales forecasts inaccurate.', ['forecasts extrapolate past trends', 'changes in the economy and incomes', 'competitors\' actions', 'changes in consumer tastes and random events'])],
      ev=[('Evaluate the usefulness of quantitative sales forecasting methods to {b}.', ['objective and based on data', 'show trend and seasonal patterns', 'help plan production and cash'],
           ['assume the past continues', 'cannot predict shocks', 'new products have no data'],
           ['how stable its market is', 'whether qualitative methods are also used', 'the time period of the forecast']),
          ('Discuss whether {b} should rely on sales forecasts when deciding whether to expand.', ['forecasts give evidence of future demand', 'reduce risk of over-capacity', 'support finance applications'],
           ['forecasts can be wrong', 'external shocks', 'managers may be over-optimistic'],
           ['the forecasting method used', 'the size and reversibility of the investment', 'its experience in the market'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ma_calc(r, D):
    c = r.choice(CASES)
    base = r.choice([200, 300, 400, 500, 800])
    tr = r.choice([4, 5, 6, 8, 10, 12])
    seas = r.choice([(-20, 10, 40, -30), (30, -10, -40, 20), (-40, -10, 20, 30), (10, 30, -10, -30)])
    xs = [base + tr * i + seas[i % 4] + r.choice([-2, 0, 2]) for i in range(12)]
    lab = [f'Y{i // 4 + 1} Q{i % 4 + 1}' for i in range(12)]
    if D <= 2:
        k = r.randrange(0, 8)
        three = xs[k:k + 3]
        ma = sum(three) / 3
        if D == 1:
            opts, ans = mc_num(r, ma, [sum(three), sum(three) / 2, max(three)], lambda x: num(x, 1))
            return {'stem': f'Sales in three consecutive periods were {three[0]}, {three[1]} and {three[2]} units. What is the three-period moving average?', 'options': opts, 'answer': ans,
                    'key': f'({" + ".join(map(str, three))})/3 = {num(ma, 1)}.', 'marks': 1}
        return {'stem': f'{c["full"]} recorded monthly sales (units) of {", ".join(map(str, xs[:6]))}. Calculate the three-month moving averages for this data.',
                'answer': ', '.join(num(sum(xs[i:i + 3]) / 3, 1) for i in range(4)),
                'key': ' ; '.join(f'({"+".join(map(str, xs[i:i + 3]))})/3 = {num(sum(xs[i:i + 3]) / 3, 1)}' for i in range(4)) + ' (1 mark method, 1 mark all values correct). [2]', 'marks': 2}
    t0 = r.randrange(2, 8)
    cma = (xs[t0 - 2] + 2 * xs[t0 - 1] + 2 * xs[t0] + 2 * xs[t0 + 1] + xs[t0 + 2]) / 8
    tot1 = sum(xs[t0 - 2:t0 + 2]); tot2 = sum(xs[t0 - 1:t0 + 3])
    sv = xs[t0] - cma
    data = '; '.join(f'{l}: {x}' for l, x in zip(lab, xs))
    stem = f'Quarterly sales (thousand units) of {c["full"]} were — {data}. Calculate the four-quarter centred moving average (trend) for {lab[t0]}'
    key = f'Four-quarter totals: {tot1} and {tot2} [1]; centred total = {tot1 + tot2} [1]; trend = {tot1 + tot2}/8 = {num(cma, 2)} [1]'
    m = 3
    if D >= 4:
        stem += ' and the seasonal variation for that quarter'
        key += f'; seasonal variation = {xs[t0]} − {num(cma, 2)} = {sv:+.2f} [1]'
        m = 4
    if D >= 5:
        stem += f'. The trend is rising by about {tr} thousand units per quarter and the average seasonal variation for Q{t0 % 4 + 1} is {seas[t0 % 4]:+}. Forecast sales for Q{t0 % 4 + 1} of year 4 and comment on its reliability'
        steps = (12 + (t0 % 4)) - t0
        fc = cma + tr * steps + seas[t0 % 4]
        key += f'; trend in Y4 Q{t0 % 4 + 1} = {num(cma, 2)} + {steps} × {tr} = {num(cma + tr * steps, 2)}; forecast = {num(cma + tr * steps, 2)} {seas[t0 % 4]:+} = {num(fc, 2)} [1]; reliability limited by extrapolation and external change [1]'
        m = 6
    return {'stem': stem + '.', 'answer': f'Trend = {num(cma, 2)}' + (f'; seasonal variation {sv:+.2f}' if D >= 4 else '') + (f'; forecast ≈ {num(fc, 1)}' if D >= 5 else ''),
            'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(6, 'Correlation in marketing data', ['correlation and causal relationships in marketing data', 'correlation', 'causal relationships'],
      defs=[('correlation', 'A statistical measure of the strength and direction of the relationship between two variables, e.g. advertising spending and sales.'),
            ('causation (causal relationship)', 'A relationship in which a change in one variable directly brings about a change in another.'),
            ('positive correlation', 'A relationship in which both variables tend to increase together.'),
            ('scatter graph', 'A graph plotting pairs of values of two variables, used to see whether they are correlated and to draw a line of best fit.')],
      mcqs=[('A correlation coefficient of −0.9 between price and sales indicates', 'a strong negative relationship', ['a weak negative relationship', 'a strong positive relationship', 'no relationship'],
             'Values close to −1 show a strong inverse relationship.'),
            ('Ice cream sales and sunglasses sales are strongly positively correlated. The most likely explanation is', 'both are caused by a third factor, hot weather', ['ice cream causes people to buy sunglasses', 'sunglasses cause people to buy ice cream', 'the correlation must be an error'],
             'Correlation does not prove causation; a third variable may cause both.'),
            ('Which correlation coefficient shows the weakest relationship?', '0.1', ['0.8', '−0.7', '−0.95'],
             'Strength depends on how close the value is to ±1; 0.1 is very weak.')],
      exps=[('Explain why strong correlation between two variables does not prove that one causes the other.', 'Both may be influenced by a third factor, the relationship may be coincidental, or causation may run the other way.', '1 mark third factor/coincidence; 1 mark example or reverse causation. [2]'),
            ('Explain how a business could use correlation to plan its advertising budget.', 'If sales and advertising spending are strongly positively correlated, a line of best fit can estimate the sales likely from different budgets, helping to choose the spending level.', '1 mark identifies relationship; 1 mark use for forecasting/budgeting. [2]'),
            ('Explain one limitation of using a line of best fit to forecast sales.', 'It assumes the relationship stays the same; extrapolating beyond the data range or changes in other factors make forecasts unreliable.', '1 mark limitation; 1 mark explanation. [2]')],
      adv=[('using correlation analysis to decide its advertising budget', ['evidence-based budgeting', 'identifies which factors drive sales', 'can forecast sales from planned spending'],
            ['correlation is not causation', 'relationship may change', 'other factors are ignored'])],
      anl=[('Analyse how {b} could use correlation analysis to improve its marketing decisions.', ['correlation measures the relationship between variables', 'identifies factors linked to sales of {prod}', 'line of best fit forecasts sales', 'must test whether the link is causal before acting']),
           ('Analyse why a strong correlation between {bp} social media spending and its sales might be misleading.', ['correlation does not prove causation', 'sales may rise for other reasons (season, incomes)', 'reverse causation: higher sales fund more spending', 'small samples can give misleading results'])],
      ev=[('Evaluate the usefulness of correlation analysis for {bp} marketing planning.', ['identifies relationships', 'supports forecasts', 'objective evidence'],
           ['not proof of causation', 'relationships change', 'quality of data'],
           ['the strength of the correlation', 'whether a causal mechanism is plausible', 'how stable the market is']),
          ('Discuss whether {b} should increase its advertising budget because sales and advertising have been strongly correlated in the past.', ['past relationship suggests more sales', 'competitors may be advertising more', 'line of best fit predicts gains'],
           ['correlation may not be causal', 'diminishing returns', 'cost may exceed contribution'],
           ['the contribution earned on extra sales', 'other factors driving sales', 'the reliability of the data'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def corr_calc(r, D):
    c = r.choice(CASES)
    a = r.choice([50, 80, 100, 120, 150, 200])
    b = r.choice([1.5, 2, 2.5, 3, 4, 5])
    x = r.choice([10, 15, 20, 25, 30, 40])
    y = a + b * x
    if D == 1:
        opts, ans = mc_num(r, y, [a * x + b, b * x, a + x], lambda v: f'{num(v, 1)}')
        return {'stem': f'The line of best fit for sales (S, thousand units) against advertising (A, $000) is S = {a} + {b}A. What are forecast sales when A = {x}?', 'options': opts, 'answer': ans,
                'key': f'S = {a} + {b} × {x} = {num(y, 1)} thousand units.', 'marks': 1}
    rr = r.choice([0.92, 0.85, 0.78, 0.45, 0.3])
    stem = (f'{c["full"]} plotted monthly sales (S, thousand units) against advertising spending (A, $000). The line of best fit is S = {a} + {b}A, and the correlation coefficient is {rr}. '
            f'Calculate forecast sales when advertising is ${x},000 and the extra sales from increasing advertising by $5,000')
    key = f'S = {a} + {b} × {x} = {num(y, 1)} thousand [1]; extra = {b} × 5 = {num(b * 5, 1)} thousand units [1]'
    m = 2
    if D >= 3:
        stem += '. Comment on the strength of the correlation'
        key += f'; r = {rr} is {"strong" if rr >= 0.75 else "weak to moderate"} positive, so the forecast is {"fairly" if rr >= 0.75 else "not very"} reliable [1]'
        m = 3
    if D >= 4:
        stem += ' and explain why the forecast may still be wrong'
        key += '; correlation ≠ causation, other variables, extrapolation beyond data, changing market [1]'
        m = 4
    return {'stem': stem + '.', 'answer': f'{num(y, 1)} thousand units; +{num(b * 5, 1)} thousand', 'key': key + f'. [{m}]', 'marks': m}


t = T(6, 'Big data and marketing analytics', ['use of big data and marketing analytics', 'big data', 'marketing analytics'],
      defs=[('big data', 'Extremely large and fast-growing sets of data, e.g. from online transactions, social media and sensors, that can be analysed by computers to reveal patterns and trends.'),
            ('marketing analytics', 'Measuring and analysing marketing data to evaluate the effectiveness of marketing activities and improve decisions.'),
            ('data mining', 'Using software to search large data sets for patterns and relationships, e.g. which products customers buy together.'),
            ('conversion rate', 'The percentage of visitors to a website or app (or recipients of a campaign) who complete a desired action such as making a purchase.')],
      mcqs=[('Which is the best example of a business using big data?', 'An online retailer recommending products based on millions of customers\' browsing histories', ['A shop owner asking ten customers their opinion', 'A firm printing leaflets', 'A manager reading last year\'s annual report'],
             'Big data involves analysing very large, fast-changing data sets.'),
            ('Which is a major risk for a business that collects large amounts of customer data?', 'Data breaches and breaking data protection laws', ['Lower understanding of customers', 'Less targeted marketing', 'Lower market research costs'],
             'Data security and privacy laws are key concerns.'),
            ('A campaign reached 50 000 people and 1 000 made a purchase. The conversion rate is', '2%', ['5%', '0.2%', '20%'],
             '1 000/50 000 × 100 = 2%.')],
      exps=[('Explain how big data could help a retailer target its promotions more effectively.', 'Analysis of purchase and browsing data identifies segments and individual preferences, so offers can be personalised and sent at the right time, raising conversion rates.', '1 mark analysis of customer data; 1 mark more targeted/personalised promotion. [2]'),
            ('Explain two problems a business may face when using big data.', 'High cost of software and skilled analysts; privacy and data protection concerns; too much data can make it hard to identify what matters.', '2 × (1 mark problem, 1 mark explanation). [4]'),
            ('Explain why marketing analytics can improve the return on marketing spending.', 'Measuring the results of each campaign shows which channels and messages work, so budget can be moved from poor to effective activities.', '1 mark measurement; 1 mark reallocation of budget. [2]')],
      adv=[('investing in big data analytics', ['personalised marketing raises sales', 'better forecasts of demand', 'faster identification of trends'],
            ['high cost of systems and analysts', 'privacy and legal risks', 'data may be misinterpreted'])],
      anl=[('Analyse how {b} could use big data to increase sales of its {prod}.', ['big data reveals patterns in customer behaviour', 'segment and target customers precisely', 'personalised offers raise conversion rates', 'better demand forecasts reduce stock-outs']),
           ('Analyse the risks to {b} of collecting and analysing large amounts of customer data.', ['data protection laws and fines', 'reputational damage from data breaches', 'high cost of systems and skills', 'over-reliance on data rather than judgement'])],
      ev=[('Evaluate whether {b} should invest heavily in big data and marketing analytics.', ['better targeting and higher conversion rates', 'improved forecasting', 'competitive advantage'],
           ['high cost and skills shortage', 'privacy and security risks', 'benefits uncertain for a firm of its size'],
           ['the volume of customer data it can collect', 'the skills available', 'what competitors are doing']),
          ('Discuss whether big data will replace traditional market research for businesses such as {b}.', ['huge volumes of real behaviour data', 'faster and continuous', 'cheaper per insight once systems exist'],
           ['shows what but not why customers act', 'new products lack data', 'qualitative research gives depth'],
           ['the type of decision', 'the cost of each method', 'the availability of data in its market'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def conv_calc(r, D):
    c = r.choice(CASES)
    vis = r.choice([40000, 50000, 80000, 120000, 200000])
    cr = r.choice([1.5, 2, 2.5, 3, 4])
    buyers = vis * cr / 100
    cost = r.choice([10000, 15000, 20000, 30000, 40000])
    aov = r.choice([20, 25, 30, 40, 50, 60])
    if D == 1:
        opts, ans = mc_num(r, cost / buyers, [cost / vis, buyers / cost, cost / buyers * 10], lambda x: money(x, 2))
        return {'stem': f'An online campaign costing {money(cost)} produced {round(buyers):,} new customers. What was the cost per customer acquired?', 'options': opts, 'answer': ans,
                'key': f'{money(cost)}/{round(buyers):,} = {money(cost / buyers, 2)}.', 'marks': 1}
    stem = f'{c["full"]} ran an online campaign costing {money(cost)}. It attracted {vis:,} visitors, of whom {round(buyers):,} made a purchase. Calculate the conversion rate and the cost per customer acquired'
    key = f'Conversion = {round(buyers):,}/{vis:,} × 100 = {pct(cr)} [1]; cost per customer = {money(cost)}/{round(buyers):,} = {money(cost / buyers, 2)} [1]'
    m = 2
    if D >= 3:
        gm = r.choice([0.3, 0.4, 0.5])
        gp = buyers * aov * gm
        stem += f'. The average order is ${aov} and the gross margin is {round(gm * 100)}%. Calculate the return on the campaign spending'
        key += f'; gross profit = {round(buyers):,} × ${aov} × {round(gm * 100)}% = {money(gp)} [1]; return = ({money(gp)} − {money(cost)})/{money(cost)} × 100 = {pct((gp - cost) / cost * 100)} [1]'
        m = 4
        if D >= 5:
            stem += ', and explain one reason why this may understate the value of the campaign'
            key += '; repeat purchases / customer lifetime value, brand awareness among non-buyers [1]'
            m = 5
    return {'stem': stem + '.', 'answer': f'{pct(cr)}; {money(cost / buyers, 2)} per customer' + (f'; return {pct((gp - cost) / cost * 100)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 7 Marketing strategy
# =====================================================================================

t = T(7, 'Marketing planning', ['marketing planning: objectives, budgets and the marketing plan', 'marketing plan', 'marketing budget', 'marketing objectives'],
      defs=[('marketing plan', 'A detailed document setting out the marketing objectives, the strategies and marketing mix to achieve them, the budget, the timescale and how results will be measured.'),
            ('marketing objective', 'A goal of the marketing department that supports corporate objectives, e.g. increase market share from 12% to 15% within two years.'),
            ('marketing budget', 'The amount of money allocated to marketing activities over a period, often set as a percentage of sales, by competitor parity or by objective-and-task.'),
            ('integrated marketing mix', 'A marketing mix in which the elements (product, price, promotion, place) are consistent with each other and with the target market.')],
      mcqs=[('Which is the best example of a SMART marketing objective?', 'Increase market share in Chile from 8% to 11% within 18 months', ['Become the best brand in the world', 'Sell more products next year', 'Make customers happier'],
             'SMART objectives are specific, measurable, achievable, realistic and time-bound.'),
            ('A business sets its marketing budget equal to 5% of last year\'s sales. This method is', 'percentage of sales', ['competitor parity', 'objective and task', 'zero budgeting'],
             'The budget is a fixed percentage of (past or forecast) sales revenue.'),
            ('Which method sets the marketing budget by costing the activities needed to achieve the marketing objectives?', 'Objective and task', ['Percentage of sales', 'Competitor parity', 'What can be afforded'],
             'Objective-and-task links spending to what must be done.')],
      exps=[('Explain why marketing objectives must be consistent with corporate objectives.', 'Marketing objectives are a means of achieving corporate goals; if they conflict (e.g. a cheap volume strategy when the corporate goal is premium positioning) resources are wasted and the strategy fails.', '1 mark link/hierarchy of objectives; 1 mark consequence of conflict. [2]'),
            ('Explain one advantage and one disadvantage of setting the marketing budget as a percentage of sales.', 'Advantage: simple and affordable because it is linked to revenue. Disadvantage: spending falls when sales fall, just when more promotion may be needed.', '1 mark each with explanation. [2]'),
            ('Explain why a marketing plan should include methods of measuring results.', 'Measuring sales, market share or response rates shows whether objectives are being met, so managers can take corrective action and judge value for money.', '1 mark monitoring; 1 mark corrective action/accountability. [2]')],
      adv=[('preparing a detailed marketing plan', ['clear objectives and coordination', 'budget controlled and measurable', 'helps raise finance and evaluate results'],
            ['time-consuming to prepare', 'may become inflexible as markets change', 'depends on accurate research and forecasts'])],
      anl=[('Analyse how a detailed marketing plan could help {b} launch {newprod}.', ['a marketing plan sets objectives, strategy, budget and timescales', 'coordinates the marketing mix for the target segment', 'allocates the budget to the most effective activities', 'allows results to be measured against targets']),
           ('Analyse the factors {b} should consider when setting its marketing budget.', ['marketing budget allocates spending to marketing', 'marketing objectives and the tasks needed', 'competitors\' spending', 'available finance and expected return'])],
      ev=[('Evaluate the most appropriate method for {b} to set its marketing budget.', ['objective-and-task links spending to goals', 'percentage of sales is simple and affordable', 'competitor parity avoids losing share'],
           ['objective-and-task can be expensive', 'percentage of sales is pro-cyclical', 'competitor parity ignores own objectives'],
           ['its marketing objectives', 'its financial position', 'the intensity of competition']),
          ('Discuss whether a marketing plan is essential for the success of {b}.', ['coordination and focus', 'measurable objectives and budget control', 'supports investment decisions'],
           ['markets change faster than plans', 'plans are only as good as their research', 'flexibility and creativity matter'],
           ['the speed of change in its market', 'its size and resources', 'how the plan is reviewed'])])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def mbudget_calc(r, D):
    c = r.choice(CASES)
    S = r.choice([4, 6, 8, 12, 15, 20, 25]) * 1e6
    p = r.choice([3, 4, 5, 6, 8])
    B = S * p / 100
    shares = r.choice([(40, 30, 20, 10), (50, 25, 15, 10), (35, 35, 20, 10)])
    names = ['digital advertising', 'sales promotion', 'trade shows', 'public relations']
    if D == 1:
        opts, ans = mc_num(r, B, [S / p, S * p / 1000, B * 2], lambda x: money(x))
        return {'stem': f'A business with sales revenue of {money(S)} sets its marketing budget at {p}% of sales. What is the budget?', 'options': opts, 'answer': ans, 'key': f'{p}% × {money(S)} = {money(B)}.', 'marks': 1}
    stem = f'{c["full"]} expects sales revenue of {money(S)} next year and sets its marketing budget at {p}% of forecast sales, split ' + ', '.join(f'{s}% {n}' for s, n in zip(shares, names)) + '. Calculate the total budget and the amount for digital advertising'
    key = f'Budget = {p}% × {money(S)} = {money(B)} [1]; digital = {shares[0]}% × {money(B)} = {money(B * shares[0] / 100)} [1]'
    m = 2
    if D >= 3:
        inc = r.choice([200000, 300000, 400000, 600000])
        stem += f'. Digital advertising is expected to generate extra sales of {money(inc * 4)} at a gross margin of 30%. Calculate the return on the digital advertising spending'
        gp = inc * 4 * 0.3
        key += f'; extra gross profit = 30% × {money(inc * 4)} = {money(gp)} [1]; return = ({money(gp)} − {money(B * shares[0] / 100)})/{money(B * shares[0] / 100)} × 100 = {pct((gp - B * shares[0] / 100) / (B * shares[0] / 100) * 100)} [1]'
        m = 4
    return {'stem': stem + '.', 'answer': f'{money(B)}; digital {money(B * shares[0] / 100)}', 'key': key + f'. [{m}]', 'marks': m}


t = T(7, 'New product development and R&D', ['new product development and research and development (r&d)', 'new product development', 'research and development'],
      defs=[('research and development (R&D)', 'The scientific and technical work carried out to create new products and processes or improve existing ones.'),
            ('new product development (NPD)', 'The process of creating a new product, from generating ideas, screening and concept testing through prototype development, test marketing and launch.'),
            ('test marketing', 'Launching a new product in a limited geographical area or to a small group of customers to assess demand before a full launch.'),
            ('patent', 'A legal right that gives the inventor of a new product or process the sole right to make, use and sell it for a set period.')],
      mcqs=[('What is the main purpose of test marketing a new product?', 'To find out how customers react before spending on a full launch', ['To obtain a patent', 'To reduce the cost of R&D', 'To set the final price for all markets'],
             'Test marketing reduces the risk of an expensive failed launch.'),
            ('Which stage of new product development removes ideas that are unlikely to be profitable?', 'Idea screening', ['Commercialisation', 'Test marketing', 'Product launch'],
             'Screening filters ideas against criteria such as cost, market potential and fit.'),
            ('Why do firms in the pharmaceutical industry spend heavily on R&D?', 'New patented drugs give a period of protection from competition and high margins', ['R&D always succeeds quickly', 'Governments ban copies of all medicines forever', 'R&D reduces fixed costs'],
             'Patents create temporary monopolies that reward innovation.')],
      exps=[('Explain why spending on R&D does not guarantee business success.', 'Most projects fail to produce a viable product; R&D is costly and slow, and competitors may launch first or customers may not want the result.', '1 mark uncertainty/failure rate; 1 mark cost/time or market risk. [2]'),
            ('Explain how new product development links to the product life cycle.', 'New products replace those in decline and extend the portfolio, so the business always has products in growth to generate future cash flow.', '1 mark replacing declining products; 1 mark balanced portfolio/cash flow. [2]'),
            ('Explain one reason why a business might use market research before investing in R&D.', 'Research identifies unmet customer needs, so R&D is focused on products that customers will buy (market orientation), reducing the risk of failure.', '1 mark reason; 1 mark explanation. [2]')],
      adv=[('increasing its R&D spending to develop {newprod}', ['first-mover advantage', 'patents protect from competition', 'higher margins from innovative products'],
            ['high costs reduce short-term profit', 'many projects fail', 'long time before any return'])],
      anl=[('Analyse how investing in research and development could improve the competitiveness of {b}.', ['R&D creates new products and processes', 'differentiation of {prod} allows premium pricing', 'process innovation lowers unit costs', 'patents give temporary protection from rivals']),
           ('Analyse the stages {b} should follow to develop and launch {newprod}.', ['NPD process: idea generation and screening', 'concept testing and market research', 'prototype development and test marketing', 'commercialisation and launch with an integrated marketing mix'])],
      ev=[('Evaluate whether {b} should increase its spending on research and development.', ['new products and processes', 'patents and differentiation', 'long-term growth'],
           ['high cost and uncertain results', 'lower short-term profit and dividends', 'competitors may copy or launch first'],
           ['the pace of innovation in its industry', 'its financial resources', 'its ability to protect ideas']),
          ('Discuss whether {b} should launch {newprod} after a test market or launch it nationally at once.', ['test market reduces risk', 'feedback improves the product', 'lower initial cost'],
           ['delay gives competitors time to copy', 'test area may not be representative', 'national launch gains first-mover advantage'],
           ['the strength of competition', 'the cost of failure', 'how unique the product is'])])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def rd_calc(r, D):
    c = r.choice(CASES)
    rev = r.choice([20, 40, 50, 80, 120, 200])
    rd = rev * r.choice([0.03, 0.04, 0.05, 0.06, 0.08, 0.1])
    rp = rd / rev * 100
    if D == 1:
        opts, ans = mc_num(r, rp, [rev / rd, rd, rp * 10], lambda x: pct(x))
        return {'stem': f'A business has revenue of ${rev}m and spends ${num(rd, 2)}m on R&D. What is R&D spending as a percentage of revenue?', 'options': opts, 'answer': ans, 'key': f'{num(rd, 2)}/{rev} × 100 = {pct(rp)}.', 'marks': 1}
    ind = r.choice([4, 5, 6, 7])
    cost = r.choice([1.5, 2, 3, 4, 5])
    cont = r.choice([0.5, 0.8, 1.0, 1.2, 1.5])
    stem = f'{c["full"]} has annual revenue of ${rev} million and spends ${num(rd, 2)} million on R&D; the industry average is {ind}% of revenue. Calculate its R&D as a percentage of revenue and compare it with the industry'
    key = f'{num(rd, 2)}/{rev} × 100 = {pct(rp)} [1]; {"above" if rp > ind else "below" if rp < ind else "equal to"} the industry average of {ind}% [1]'
    m = 2
    if D >= 3:
        stem += f'. A new product would need R&D of ${cost}m and is expected to earn a contribution of ${cont}m a year. Calculate the payback period on the R&D'
        key += f'; payback = {cost}/{cont} = {num(cost / cont, 1)} years [1]'
        m = 3
    if D >= 4:
        stem += ' and explain one reason why the forecast may be too optimistic'
        key += '; many NPD projects fail; competitors may launch first; contribution forecasts uncertain; product life may be short [1]'
        m = 4
    return {'stem': stem + '.', 'answer': pct(rp) + (f'; payback {num(cost / cont, 1)} years' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m}


t = T(7, 'International marketing', ['international marketing: entry strategies and pan-global vs local marketing', 'international marketing', 'pan-global', 'entry strategies'],
      defs=[('pan-global marketing', 'Using the same standardised marketing mix (product, brand, promotion) in all countries.'),
            ('localised marketing (glocalisation)', 'Adapting the marketing mix to the culture, tastes, laws and incomes of each country while keeping a global brand.'),
            ('franchising (international)', 'Allowing a business in another country to use the brand name, products and methods in return for a fee and royalty.'),
            ('licensing', 'Granting a foreign business the right to produce a product or use a patent or brand, in return for a royalty.')],
      mcqs=[('Which method of entering a foreign market involves the least risk and capital?', 'Exporting through an overseas agent', ['Building a factory abroad', 'Taking over a foreign competitor', 'Opening a wholly owned subsidiary'],
             'Exporting via agents needs little investment, although control is limited.'),
            ('A fast-food chain changes its menu in each country to suit local tastes. This is', 'localised marketing', ['pan-global marketing', 'mass marketing', 'product orientation'],
             'Adapting the mix to local markets is localisation (glocalisation).'),
            ('Which is an advantage of pan-global marketing?', 'Economies of scale in production and promotion', ['It suits every local culture perfectly', 'It avoids all legal differences', 'It always increases prices'],
             'A single standardised mix reduces costs and builds a consistent global brand.')],
      exps=[('Explain one advantage and one disadvantage of entering a foreign market by franchising.', 'Advantage: rapid expansion using the franchisee\'s capital and local knowledge. Disadvantage: less control over quality and service, which could damage the brand.', '1 mark each with explanation. [2]'),
            ('Explain why a business might adapt its products for different countries.', 'Tastes, culture, religion, laws, climate and incomes differ, so a standard product may not meet local needs or regulations.', '1 mark difference between markets; 1 mark need to adapt. [2]'),
            ('Explain two risks of entering an international market.', 'Lack of knowledge of local culture and consumers; exchange-rate risk; political and legal risk; strong local competitors.', '2 × (1 mark risk, 1 mark explanation). [4]')],
      adv=[('using a pan-global marketing strategy for {prod}', ['economies of scale in production and promotion', 'consistent global brand image', 'simpler management'],
            ['ignores local tastes and culture', 'legal restrictions in some countries', 'local competitors may serve customers better']),
           ('entering {newmkt} through franchising', ['fast expansion with low capital', 'local franchisee knowledge', 'franchisee motivated by own investment'],
            ['less control over quality', 'shares profits through fees only', 'risk to brand reputation'])],
      anl=[('Analyse the factors {b} should consider before selling its products in {newmkt}.', ['market research on size, growth and tastes', 'cultural, legal and political differences', 'exchange-rate and payment risk', 'strength of local and global competitors']),
           ('Analyse the benefits to {b} of adapting its marketing mix for customers in {newmkt}.', ['localisation adapts the mix to local needs', 'products better meet local tastes and laws', 'pricing suited to local incomes', 'promotion that fits culture and language'])],
      ev=[('Evaluate whether {b} should use a pan-global or a localised marketing strategy in {newmkt}.', ['pan-global gives economies of scale', 'consistent brand', 'simpler to control'],
           ['local tastes and culture differ', 'local rivals adapt better', 'legal rules may require changes'],
           ['how different consumers in {newmkt} are', 'the nature of its {prod}', 'its budget for adaptation']),
          ('Recommend the most suitable method for {b} to enter the market in {newmkt}.', ['exporting is low risk', 'joint venture brings local knowledge', 'own subsidiary gives control'],
           ['exporting faces tariffs and transport costs', 'joint ventures share profits', 'subsidiaries need large investment'],
           ['its resources and experience', 'the size and risk of the market', 'trade barriers'])])


t = T(7, 'Market positioning and competitive strategy', ['market positioning and competitive strategy', 'market positioning', 'competitive strategy', 'porter generic'],
      defs=[('market positioning', 'The perception customers have of a brand relative to its competitors, e.g. on price and quality, often shown on a perceptual (positioning) map.'),
            ('cost leadership', 'A competitive strategy of being the lowest-cost producer in the industry, so the business can charge average prices with higher margins or undercut rivals.'),
            ('differentiation strategy', 'A competitive strategy of offering products that customers see as unique or superior, allowing a premium price.'),
            ('unique selling point (USP)', 'A feature of a product or brand that customers value and that distinguishes it from all competitors.')],
      mcqs=[('According to Porter, a firm that targets a narrow segment with a unique product is following', 'a differentiation focus strategy', ['a cost leadership strategy', 'a mass market strategy', 'a cost focus strategy'],
             'Focus = narrow target; differentiation focus = unique product for a niche.'),
            ('What does a gap on a perceptual (positioning) map suggest?', 'A possible opportunity for a product, if customers want that combination', ['That the market is saturated', 'That demand is zero', 'That prices are too high'],
             'A gap may be an opportunity, but research must confirm demand exists.'),
            ('What did Porter mean by being "stuck in the middle"?', 'Trying to be both low-cost and differentiated and achieving neither', ['Having a market share of exactly 50%', 'Being in the maturity stage of the product life cycle', 'Selling only in the home market'],
             'Firms without a clear generic strategy lack competitive advantage.')],
      exps=[('Explain how a business can use a perceptual map when positioning a new product.', 'It plots customer perceptions of rival brands on two attributes, showing crowded areas and gaps where a new product could be positioned.', '1 mark plotting perceptions; 1 mark identify gaps/positioning. [2]'),
            ('Explain the difference between cost leadership and differentiation.', 'Cost leadership aims for the lowest costs in the industry; differentiation offers unique features that justify a higher price.', '1 mark each. [2]'),
            ('Explain why repositioning a brand can be risky.', 'Existing customers may be alienated, the new position may not be believed, and repositioning requires costly changes to the whole marketing mix.', '1 mark risk; 1 mark explanation. [2]')],
      adv=[('repositioning its {prod} as a premium brand', ['higher prices and margins', 'less direct price competition', 'stronger brand loyalty'],
            ['may lose price-sensitive customers', 'high cost of upgrading product and promotion', 'customers may not believe the new image']),
           ('following a cost leadership strategy', ['lowest unit costs give pricing flexibility', 'can win price-sensitive segments', 'high margins at average prices'],
            ['needs large scale and efficiency', 'vulnerable to rivals with even lower costs', 'brand may be seen as cheap'])],
      anl=[('Analyse how {b} could use a perceptual map to improve its market positioning.', ['perceptual maps show customers\' views of brands', 'identifies gaps and crowded segments', 'helps choose a distinctive position for {prod}', 'guides the marketing mix to support the position']),
           ('Analyse whether a differentiation strategy would give {b} a competitive advantage.', ['differentiation creates perceived uniqueness', 'allows premium pricing', 'reduces price elasticity of demand', 'requires investment in quality, design and branding'])],
      ev=[('Evaluate whether {b} should follow a cost leadership or a differentiation strategy.', ['cost leadership suits price-sensitive markets', 'differentiation allows premium prices', 'differentiation builds loyalty'],
           ['cost leadership needs scale', 'differentiation needs investment and innovation', 'stuck in the middle risk'],
           ['the size of {b} relative to rivals', 'customer priorities in its market', 'its core competencies']),
          ('Discuss whether {b} should reposition its brand to target a more upmarket segment.', ['higher margins', 'less price competition', 'growing affluent segment'],
           ['loss of existing customers', 'cost of changing the mix', 'credibility of the new position'],
           ['market research evidence', 'competitor positions', 'its quality and capabilities'])])

# =====================================================================================
# 8 Location and scale of operations
# =====================================================================================

t = T(8, 'Quantitative and qualitative location factors', ['quantitative and qualitative factors in location decisions', 'location decisions', 'quantitative factors', 'qualitative factors'],
      defs=[('quantitative location factors', 'Factors that can be measured in money terms, such as site and building costs, labour costs, transport costs and government grants.'),
            ('qualitative location factors', 'Non-numerical factors in a location decision, such as quality of life, safety, attitudes of the local community and management preferences.'),
            ('weighted scoring (location)', 'A decision-making technique in which each location factor is given a weight according to its importance, each site is scored on each factor, and the weighted scores are totalled.'),
            ('industrial inertia', 'The tendency of firms to stay in their original location even when the original advantages have disappeared.')],
      mcqs=[('Which is a qualitative factor in a location decision?', 'The quality of local schools for managers\' families', ['The monthly rent of the site', 'Government investment grants', 'Transport costs per unit'],
             'Qualitative factors cannot easily be measured in money.'),
            ('Which technique allows a business to compare locations using several factors of different importance?', 'Weighted scoring', ['Moving averages', 'Ratio analysis', 'Decision trees'],
             'Weights reflect importance; scores reflect site performance.'),
            ('A business that needs to be close to its customers is most likely to be', 'a hotel or retailer', ['a steel producer using heavy raw materials', 'a mining company', 'a software developer'],
             'Service businesses must locate where customers are.')],
      exps=[('Explain why qualitative factors are important in location decisions.', 'Some factors, such as the availability of skilled staff, local attitudes, safety and quality of life, affect long-run success but cannot be measured in money.', '1 mark examples; 1 mark long-run significance. [2]'),
            ('Explain one limitation of using weighted scoring to choose a location.', 'Weights and scores are subjective, so managers can bias the result; it may ignore factors not included.', '1 mark subjectivity; 1 mark consequence. [2]'),
            ('Explain why break-even analysis is useful when comparing two possible sites.', 'Each site has different fixed and variable costs; comparing break-even outputs shows which site becomes profitable at lower output and the risk at each.', '1 mark different costs; 1 mark comparison of risk/profit. [2]')],
      adv=[('moving its main operation to a cheaper out-of-town site', ['lower rent and labour costs', 'room to expand', 'possible government grants'],
            ['relocation costs and disruption', 'loss of skilled staff who will not move', 'further from customers or suppliers'])],
      anl=[('Analyse the quantitative and qualitative factors {b} should consider when choosing a new site.', ['quantitative: land, building, labour and transport costs, grants', 'qualitative: skills, local attitudes, infrastructure quality', 'access to customers and suppliers for {prod}', 'scope for future expansion']),
           ('Analyse how a poor location decision could affect {b}.', ['location affects costs and revenue', 'higher costs reduce competitiveness', 'difficulty recruiting skilled staff', 'expensive and disruptive to move again'])],
      ev=[('Evaluate the most important factor for {b} when choosing the location of a new site.', ['costs of land and labour', 'access to customers', 'availability of skilled labour'],
           ['qualitative factors such as quality of life', 'government incentives', 'infrastructure and logistics'],
           ['the nature of its {prod}', 'whether the site serves local or export markets', 'its long-term strategy']),
          ('Discuss whether {b} should base its location decision mainly on weighted scoring results.', ['systematic and transparent', 'combines several factors', 'reflects managers\' priorities'],
           ['weights and scores are subjective', 'may ignore key risks', 'quantitative methods like investment appraisal also needed'],
           ['how the weights were chosen', 'the closeness of the scores', 'the cost of a wrong decision'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def wscore_calc(r, D):
    c = r.choice(CASES)
    factors = r.sample(['labour costs', 'site cost', 'transport links', 'skilled labour', 'government grants', 'nearness to customers'], 4)
    w = r.choice([(0.4, 0.3, 0.2, 0.1), (0.35, 0.3, 0.2, 0.15), (0.3, 0.3, 0.25, 0.15), (0.5, 0.2, 0.2, 0.1)])
    A = [r.randint(4, 9) for _ in range(4)]
    B = [r.randint(4, 9) for _ in range(4)]
    if A == B:
        B[0] = 10 - A[0] if A[0] != 5 else 7
    sA = sum(x * y for x, y in zip(w, A)); sB = sum(x * y for x, y in zip(w, B))
    if abs(sA - sB) < 1e-9:
        B[3] = B[3] + 1 if B[3] < 10 else B[3] - 1
        sB = sum(x * y for x, y in zip(w, B))
    tbl = '; '.join(f'{f} (weight {wi}): site X {a}, site Y {b}' for f, wi, a, b in zip(factors, w, A, B))
    if D == 1:
        opts, ans = mc_num(r, sA, [sum(A), sum(A) / 4, sA * 10], lambda x: num(x, 2))
        return {'stem': f'Location factors, weights and scores out of 10 are — {tbl}. What is the total weighted score for site X?', 'options': opts, 'answer': ans,
                'key': ' + '.join(f'{wi} × {a}' for wi, a in zip(w, A)) + f' = {num(sA, 2)}.', 'marks': 1}
    if D <= 3:
        stem = f'{c["full"]} is choosing between two sites. Factors, weights and scores out of 10 are — {tbl}. Calculate the weighted score for each site and state which site should be chosen on this basis.'
        key = f'X = ' + ' + '.join(f'{wi}×{a}' for wi, a in zip(w, A)) + f' = {num(sA, 2)} [1]; Y = ' + ' + '.join(f'{wi}×{b}' for wi, b in zip(w, B)) + f' = {num(sB, 2)} [1]; choose site {"X" if sA > sB else "Y"} [1]. [3]'
        return {'stem': stem, 'answer': f'X {num(sA, 2)}, Y {num(sB, 2)}: site {"X" if sA > sB else "Y"}', 'key': key, 'marks': 3}
    FX, VX, FY, VY = r.choice([(200, 12, 300, 8), (150, 15, 240, 10), (400, 6, 250, 9), (300, 10, 180, 14)])
    p = r.choice([20, 22, 25, 30])
    beX, beY = FX * 1000 / (p - VX), FY * 1000 / (p - VY)
    stem = (f'{c["full"]} is choosing between two sites. Factors, weights and scores out of 10 are — {tbl}. At site X, fixed costs would be ${FX},000 a year and variable cost ${VX} per unit; '
            f'at site Y, ${FY},000 and ${VY}. The selling price is ${p}. Calculate the weighted score and break-even output for each site, and recommend a site.')
    key = (f'Weighted: X {num(sA, 2)}, Y {num(sB, 2)} [2]; break-even X = {FX},000/({p} − {VX}) = {round(beX):,} units, Y = {FY},000/({p} − {VY}) = {round(beY):,} units [2]; '
           f'recommendation weighs both results plus qualitative factors and forecast demand [2]. [6]')
    return {'stem': stem, 'answer': f'Scores X {num(sA, 2)}, Y {num(sB, 2)}; break-even X {round(beX):,}, Y {round(beY):,} units', 'key': key, 'marks': 6, 'type': 'multi_step'}


t = T(8, 'International location, offshoring and reshoring', ['international location, offshoring and reshoring', 'offshoring', 'reshoring', 'international location'],
      defs=[('offshoring', 'Moving some business activities, such as production or customer service, to another country, either within the firm or by outsourcing to a foreign supplier.'),
            ('reshoring', 'Bringing production or other activities back to the home country after they had been moved abroad.'),
            ('multi-site location', 'Operating from several locations, possibly in different countries, rather than from one site.'),
            ('trade barriers', 'Government restrictions on international trade, such as tariffs, quotas and regulations, which can influence where firms locate.')],
      mcqs=[('Which is the most likely reason for a business to reshore production?', 'Rising wages and transport costs abroad combined with a need for faster delivery', ['Lower labour costs abroad', 'Weaker quality standards at home', 'Higher tariffs on its exports'],
             'Reshoring happens when the cost advantage of offshoring shrinks or speed and control matter more.'),
            ('A European bank moves its call centre to the Philippines. This is', 'offshoring', ['reshoring', 'delayering', 'horizontal integration'],
             'Moving an activity to another country is offshoring.'),
            ('Which is a risk of locating production in a country with weak labour laws?', 'Damage to reputation if poor working conditions are exposed', ['Higher wage costs', 'More regulation', 'Higher tariffs'],
             'Ethical issues can lead to boycotts and lost contracts.')],
      exps=[('Explain two reasons why a business might offshore its production.', 'Lower labour and land costs; to be close to growing foreign markets; to avoid tariffs; access to raw materials or skills.', '2 × (1 mark reason, 1 mark explanation). [4]'),
            ('Explain why offshoring customer service may harm a business.', 'Language, cultural and time-zone differences can reduce service quality and customer satisfaction, damaging the brand.', '1 mark problem; 1 mark effect. [2]'),
            ('Explain how reshoring could improve a business\'s supply chain.', 'Shorter distances reduce lead times and transport costs, make just-in-time easier and reduce the risk of disruption.', '1 mark shorter/faster; 1 mark consequence. [2]')],
      adv=[('offshoring production to a lower-cost country', ['lower labour and site costs', 'closer to new markets', 'may avoid tariffs'],
            ['longer supply chains and lead times', 'quality and ethical control problems', 'reputational damage at home']),
           ('reshoring production to {country}', ['faster delivery and better control', '"made in" branding advantage', 'lower supply-chain risk'],
            ['higher labour costs', 'cost of building new capacity', 'skills shortages at home'])],
      anl=[('Analyse the factors {b} should consider before moving production abroad.', ['labour, land and transport costs', 'trade barriers and exchange rates', 'political stability and legal system', 'quality, ethics and supply-chain risk']),
           ('Analyse how a decision to reshore operations could affect {b}.', ['reshoring brings activities back home', 'higher labour costs but lower transport and inventory costs', 'better quality control and faster response', 'possible marketing benefit and government support'])],
      ev=[('Evaluate whether {b} should offshore part of its operations.', ['lower costs', 'access to new markets', 'avoids trade barriers'],
           ['quality and control problems', 'ethical and reputational risks', 'exchange-rate and political risk'],
           ['the size of the cost saving', 'the importance of speed and quality to customers', 'its experience of managing abroad']),
          ('Discuss whether reshoring is likely to become more common for businesses such as {b}.', ['rising wages in former low-cost countries', 'supply-chain disruptions', 'automation reduces labour cost advantage'],
           ['labour costs abroad still much lower', 'established supplier networks', 'growing markets are abroad'],
           ['the industry', 'the cost of automation', 'government incentives'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def offshore_calc(r, D):
    c = r.choice(CASES)
    hl = r.choice([12, 14, 16, 18, 20])
    ol = round(hl * r.choice([0.3, 0.4, 0.5]), 2)
    hm = r.choice([6, 8, 10]); om = hm + r.choice([0, 0.5, 1])
    tr = r.choice([1.5, 2, 2.5, 3, 4])
    tar = r.choice([0, 5, 10])
    home = hl + hm
    base_off = ol + om
    off = base_off * (1 + tar / 100) + tr
    if D == 1:
        opts, ans = mc_num(r, base_off + tr, [base_off, ol + tr, hl + tr], lambda x: money(x, 2))
        return {'stem': f'Producing a product abroad costs ${num(ol)} labour and ${num(om)} materials per unit, plus ${num(tr)} transport per unit. What is the total unit cost?', 'options': opts, 'answer': ans,
                'key': f'{num(ol)} + {num(om)} + {num(tr)} = {money(base_off + tr, 2)}.', 'marks': 1}
    stem = (f'{c["full"]} compares making a product at home and abroad. Home: labour ${num(hl)} and materials ${num(hm)} per unit. Abroad: labour ${num(ol)} and materials ${num(om)} per unit, '
            f'plus shipping of ${num(tr)} per unit' + (f' and a {tar}% import tariff on the production cost (labour + materials) when the goods return' if tar else '') + '. Calculate the unit cost of each option')
    key = f'Home = {num(hl)} + {num(hm)} = {money(home, 2)} [1]; abroad = ({num(ol)} + {num(om)})' + (f' × {1 + tar / 100:.2f}' if tar else '') + f' + {num(tr)} = {money(off, 2)} [1]'
    m = 2
    if D >= 3:
        q = r.choice([50000, 80000, 100000, 200000])
        stem += f' and the annual saving for {q:,} units'
        key += f'; saving = ({money(home, 2)} − {money(off, 2)}) × {q:,} = {money((home - off) * q)} [1]'
        m = 3
    if D >= 4:
        stem += '. Evaluate whether it should offshore production'
        key += '; evaluation: quality, lead times, inventory, ethics, exchange rates, reputation weighed against the saving [2]'
        m = 5
    return {'stem': stem + '.', 'answer': f'Home {money(home, 2)}, abroad {money(off, 2)}' + (f'; saving {money((home - off) * q)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(8, 'Optimal scale of production', ['optimal scale of production', 'optimal scale', 'minimum efficient scale'],
      defs=[('optimum scale of production', 'The scale of operation at which average (unit) cost is at its lowest.'),
            ('minimum efficient scale', 'The lowest level of output at which a firm can achieve the lowest possible average cost.'),
            ('capacity utilisation', 'Actual output as a percentage of the maximum possible output: actual output ÷ maximum capacity × 100.'),
            ('scale of operation', 'The maximum output that can be achieved using the resources currently available to a business.')],
      mcqs=[('At the optimum scale of production, average cost is', 'at its lowest point', ['at its highest point', 'equal to the selling price', 'rising'],
             'Optimum scale = minimum average cost.'),
            ('Why might a small business remain small even though larger rivals have lower unit costs?', 'It serves a niche market where personal service and flexibility matter more than price', ['It cannot sell any products', 'Small firms always have lower costs', 'Economies of scale do not exist'],
             'Small firms survive by focusing on niches, flexibility and service.'),
            ('A factory produces 7 200 units a month and could produce 9 000. Capacity utilisation is', '80%', ['72%', '125%', '90%'],
             '7 200/9 000 × 100 = 80%.')],
      exps=[('Explain why a business may choose to operate below its optimum scale.', 'Demand may be too small to support optimum output, finance may be limited, or the owners may want to keep control and flexibility.', '1 mark reason; 1 mark explanation. [2]'),
            ('Explain how the optimum scale of production differs between industries.', 'Industries with high fixed costs and specialised equipment (e.g. car making) have a large minimum efficient scale; services with personal contact (e.g. hairdressing) have a small one.', '1 mark link to fixed costs/technology; 1 mark examples. [2]'),
            ('Explain why average costs may rise if a business expands beyond its optimum scale.', 'Diseconomies of scale such as poor coordination, slow communication and low motivation increase costs per unit.', '1 mark diseconomies; 1 mark effect on unit cost. [2]')],
      adv=[('increasing its scale of production by 50%', ['economies of scale cut unit costs', 'able to meet growing demand', 'stronger bargaining power'],
            ['risk of diseconomies of scale', 'spare capacity if demand falls', 'large capital investment'])],
      anl=[('Analyse the factors that influence the optimum scale of production for {b}.', ['optimum scale minimises average cost', 'size of market demand for {prod}', 'availability of finance and technology', 'management ability to control a larger operation']),
           ('Analyse how operating at high capacity utilisation could affect {b}.', ['capacity utilisation = output ÷ capacity', 'fixed costs spread over more units', 'pressure on staff and machines', 'no spare capacity for extra orders'])],
      ev=[('Evaluate whether {b} should increase its scale of operation.', ['economies of scale', 'meets rising demand', 'stronger market position'],
           ['diseconomies of scale', 'investment risk', 'demand may not grow'],
           ['forecast demand', 'current capacity utilisation', 'access to finance']),
          ('Discuss whether {b} should aim to operate at the minimum efficient scale for its industry.', ['lowest unit costs', 'price competitiveness', 'higher margins'],
           ['market may be too small', 'loss of flexibility', 'niche strategy may suit it better'],
           ['its competitive strategy', 'the size of its market', 'the cost structure of the industry'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def optscale_calc(r, D):
    c = r.choice(CASES)
    FC = r.choice([200, 300, 400, 500]) * 1000
    v = r.choice([5, 6, 8, 10])
    k = r.choice([0.002, 0.004, 0.005])  # rising variable cost per unit (diseconomies)
    qs = math.sqrt(FC * 100 / k)
    step = max(5000, round(qs / r.choice([2.6, 3, 3.4]) / 5000) * 5000)
    outs = [step * i for i in range(1, 6)]
    ac = [FC / q + v + k * q / 100 for q in outs]
    best = min(range(5), key=lambda i: ac[i])
    tbl = '; '.join(f'{q:,} units: total cost {money(FC + v * q + k * q * q / 100)}' for q in outs)
    if D == 1:
        cap = r.choice([8000, 10000, 12000, 20000]); act = cap * r.choice([0.6, 0.75, 0.8, 0.9])
        opts, ans = mc_num(r, act / cap * 100, [cap / act * 100, (cap - act) / cap * 100, act / 100], lambda x: pct(x))
        return {'stem': f'A plant can make {cap:,} units a month and is making {round(act):,}. What is its capacity utilisation?', 'options': opts, 'answer': ans,
                'key': f'{round(act):,}/{cap:,} × 100 = {pct(act / cap * 100)}.', 'marks': 1}
    stem = f'{c["full"]} estimates its annual total costs at different scales of output — {tbl}. Calculate the average cost at each output and identify the optimum scale'
    key = 'AC = TC/Q: ' + ', '.join(f'{money(a, 2)}' for a in ac) + f' [2]; optimum = {outs[best]:,} units (lowest AC {money(ac[best], 2)}) [1]'
    m = 3
    if D >= 4:
        stem += '. Explain why average cost rises beyond this output'
        key += '; beyond this, diseconomies of scale (coordination, communication, overtime) outweigh economies [1]'
        m = 4
    if D >= 5:
        stem += ', and discuss whether the business should produce at the optimum scale if demand is only ' + f'{outs[max(0, best - 1)]:,} units'
        key += '; producing above demand creates unsold stock; trade-off between unit cost and inventory/price cuts [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'Optimum {outs[best]:,} units at {money(ac[best], 2)} per unit', 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 9 Quality management
# =====================================================================================

t = T(9, 'Quality control and quality assurance', ['quality control and quality assurance', 'quality control', 'quality assurance'],
      defs=[('quality control', 'Checking products at the end of production (or at stages) by inspectors to find and remove faulty items before they reach customers.'),
            ('quality assurance', 'A system that sets quality standards for every stage of production and makes all employees responsible for meeting them, so faults are prevented rather than detected.'),
            ('quality', 'Meeting customer expectations: providing a product or service that is fit for purpose and of an acceptable standard for its price.'),
            ('quality circle', 'A small group of employees who meet regularly to identify and solve quality and production problems in their work area.')],
      mcqs=[('What is the main difference between quality control and quality assurance?', 'Quality assurance aims to prevent faults; quality control aims to detect them', ['Quality control is cheaper in every case', 'Quality assurance only checks finished products', 'Quality control involves every employee'],
             'QA builds quality in at each stage; QC inspects and rejects faulty output.'),
            ('Which is a disadvantage of relying on quality control by inspectors?', 'Faulty products are found only after resources have been wasted making them', ['Workers take responsibility for quality', 'It prevents all faults', 'It requires no extra staff'],
             'End-of-line inspection finds waste after it has occurred.'),
            ('A factory made 25 000 units and 750 were rejected. The reject rate is', '3%', ['7.5%', '0.3%', '33%'],
             '750/25 000 × 100 = 3%.')],
      exps=[('Explain why quality assurance may reduce costs compared with quality control.', 'Preventing faults at each stage means less waste, rework and inspection at the end, and fewer returns and complaints.', '1 mark prevention v detection; 1 mark cost saving. [2]'),
            ('Explain one way a business can measure the quality of a service.', 'Customer satisfaction surveys, mystery shoppers, complaint rates, waiting times or repeat-customer rates.', '1 mark method; 1 mark how it shows quality. [2]'),
            ('Explain why improving quality can increase revenue as well as reduce costs.', 'Higher quality builds reputation and loyalty, allows premium prices and generates repeat purchases and word-of-mouth.', '1 mark reputation/loyalty; 1 mark premium price or more sales. [2]')],
      adv=[('replacing end-of-line inspection with a quality assurance system', ['faults prevented, less waste', 'workers take responsibility for quality', 'consistent quality builds reputation'],
            ['training costs', 'cultural change takes time', 'staff may resist extra responsibility'])],
      anl=[('Analyse how poor quality could affect the performance of {b}.', ['quality means meeting customer expectations', 'returns, rework and waste raise unit costs', 'damage to brand and lost repeat customers', 'possible legal claims and lost contracts']),
           ('Analyse the benefits to {b} of moving from quality control to quality assurance.', ['QA prevents faults at every stage', 'lower waste and inspection costs', 'empowered staff are more motivated', 'more consistent quality of {prod}'])],
      ev=[('Evaluate whether {b} should replace quality control inspectors with a quality assurance system.', ['prevents faults', 'cuts waste and rework', 'staff ownership of quality'],
           ['training and set-up costs', 'needs culture change', 'some inspection still needed'],
           ['its current reject rate', 'the skills and attitudes of staff', 'customer expectations']),
          ('Discuss the importance of quality to the competitiveness of {b}.', ['reputation and loyalty', 'premium pricing', 'lower costs of waste'],
           ['price may matter more to customers', 'improving quality is costly', 'other factors such as delivery speed'],
           ['its market positioning', 'what competitors offer', 'the cost of quality failures'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def reject_calc(r, D):
    c = r.choice(CASES)
    q = r.choice([20000, 25000, 40000, 50000, 80000, 120000])
    rr = r.choice([2, 2.5, 3, 4, 5, 6])
    rej = round(q * rr / 100)
    uc = r.choice([4, 5, 6, 8, 10, 12])
    if D == 1:
        opts, ans = mc_num(r, rr, [rej / 100, q / rej, rr * 10], lambda x: pct(x))
        return {'stem': f'A factory produced {q:,} units, of which {rej:,} failed inspection. What is the reject rate?', 'options': opts, 'answer': ans, 'key': f'{rej:,}/{q:,} × 100 = {pct(rr)}.', 'marks': 1}
    stem = f'{c["full"]} produced {q:,} units last month; {rej:,} were rejected at inspection. Each unit costs ${uc} to make. Calculate the reject rate and the monthly cost of rejected units'
    key = f'Reject rate = {rej:,}/{q:,} × 100 = {pct(rr)} [1]; cost = {rej:,} × ${uc} = {money(rej * uc)} [1]'
    m = 2
    if D >= 3:
        new = r.choice([0.5, 1, 1.5])
        qa = r.choice([5000, 8000, 10000, 15000])
        sav = (rr - new) / 100 * q * uc * 12
        stem += f'. A quality assurance system costing {money(qa)} a month would cut the reject rate to {pct(new)}. Calculate the net annual saving'
        key += f'; annual saving on rejects = ({pct(rr)} − {pct(new)}) × {q:,} × ${uc} × 12 = {money(sav)} [1]; net = {money(sav)} − {money(qa * 12)} = {money(sav - qa * 12)} [1]'
        m = 4
        if D >= 5:
            stem += ', and assess one non-financial benefit'
            key += '; reputation, fewer complaints, motivation from responsibility [1]'
            m = 5
    return {'stem': stem + '.', 'answer': f'{pct(rr)}; {money(rej * uc)} a month' + (f'; net saving {money(sav - qa * 12)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(9, 'TQM and kaizen', ['total quality management (tqm) and kaizen', 'total quality management', 'tqm', 'kaizen'],
      defs=[('total quality management (TQM)', 'An approach in which quality is the responsibility of every employee, every process aims at zero defects and the needs of internal and external customers are put first.'),
            ('kaizen', 'A Japanese approach of continuous improvement through many small, regular changes suggested by employees.'),
            ('internal customer', 'A person or department within the business that receives the output of another part of the business.'),
            ('zero defects', 'The aim of producing goods or services with no faults at all, by getting things right first time.')],
      mcqs=[('Kaizen is best described as', 'continuous improvement through small, regular changes', ['a single large investment in new technology', 'inspection of finished products', 'outsourcing production'],
             'Kaizen relies on many small improvements suggested by staff.'),
            ('Which is essential for TQM to succeed?', 'Commitment to quality from every employee and senior management', ['A large team of quality inspectors', 'Lower wages', 'Centralised decision-making only'],
             'TQM makes quality part of everyone\'s job and culture.'),
            ('In TQM, the next department in a production process is treated as', 'an internal customer', ['an external supplier', 'a competitor', 'a pressure group'],
             'Every stage must meet the needs of the next stage.')],
      exps=[('Explain why kaizen depends on employee involvement.', 'Ideas for small improvements come from workers who know the processes best; they must be trained, empowered and motivated to suggest and implement changes.', '1 mark employees as source of ideas; 1 mark need for empowerment/motivation. [2]'),
            ('Explain two difficulties of introducing TQM.', 'Requires a change of culture and long-term commitment; training costs; resistance from staff and managers; results take time.', '2 × (1 mark difficulty, 1 mark explanation). [4]'),
            ('Explain why TQM is linked to soft HRM.', 'TQM relies on trained, involved and empowered staff who take responsibility, which fits the soft HRM view of employees as assets.', '1 mark empowered/trained staff; 1 mark link to soft HRM. [2]')],
      adv=[('introducing total quality management', ['fewer defects and less waste', 'stronger reputation for quality', 'motivated, involved staff'],
            ['high training costs', 'culture change takes years', 'staff and managers may resist']),
           ('introducing a kaizen programme', ['continuous small cost savings', 'uses employees\' ideas', 'low-cost changes with little disruption'],
            ['small steps may be too slow when big change is needed', 'needs a culture of trust', 'staff may run out of ideas or lose interest'])],
      anl=[('Analyse how introducing TQM could improve the competitiveness of {b}.', ['TQM makes quality everyone\'s responsibility', 'fewer defects lower costs of {prod}', 'improved reputation and customer loyalty', 'motivated staff through involvement']),
           ('Analyse how a kaizen approach could reduce costs at {b}.', ['kaizen = continuous small improvements', 'employees suggest ways to cut waste', 'small savings add up over time', 'improves processes without large investment'])],
      ev=[('Evaluate whether {b} should introduce total quality management.', ['lower defect rates', 'better reputation', 'involved and motivated staff'],
           ['cost and time to train staff', 'culture change needed', 'benefits may take years'],
           ['its current corporate culture', 'leadership commitment', 'the importance of quality to its customers']),
          ('Discuss whether kaizen is a better approach than large-scale change for {b}.', ['low cost', 'less disruption and resistance', 'uses staff knowledge'],
           ['too slow when markets change rapidly', 'may not deliver breakthrough innovation', 'depends on culture'],
           ['the pace of change in its industry', 'the attitudes of employees', 'the size of improvement needed'])])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def coq_calc(r, D):
    c = r.choice(CASES)
    d1 = r.choice([4, 5, 6, 8])
    d2 = d1 * r.choice([0.25, 0.4, 0.5])
    q = r.choice([60000, 100000, 150000, 240000])
    cd = r.choice([6, 8, 10, 15])
    tc = r.choice([40000, 60000, 80000, 120000])
    sav = (d1 - d2) / 100 * q * cd
    if D == 1:
        opts, ans = mc_num(r, (d1 - d2) / d1 * 100, [d1 - d2, d2 / d1 * 100, d1 / d2], lambda x: pct(x))
        return {'stem': f'After a kaizen programme, a factory\'s defect rate fell from {pct(d1)} to {pct(d2)}. What is the percentage reduction in the defect rate?', 'options': opts, 'answer': ans,
                'key': f'({pct(d1)} − {pct(d2)})/{pct(d1)} × 100 = {pct((d1 - d2) / d1 * 100)}.', 'marks': 1}
    stem = f'{c["full"]} produces {q:,} units a year and its defect rate is {pct(d1)}. Each defect costs ${cd} to put right. TQM training costing {money(tc)} is expected to cut the defect rate to {pct(d2)}. Calculate the annual saving'
    key = f'Defects fall from {round(q * d1 / 100):,} to {round(q * d2 / 100):,} [1]; saving = {round(q * (d1 - d2) / 100):,} × ${cd} = {money(sav)} [1]'
    m = 2
    if D >= 3:
        stem += ' and the payback period of the training'
        key += f'; payback = {money(tc)}/{money(sav)} = {num(tc / sav, 2)} years [1]'
        m = 3
    if D >= 4:
        stem += '. Explain one reason why the actual saving may differ'
        key += '; staff commitment, culture, time to implement, other causes of defects [1]'
        m = 4
    return {'stem': stem + '.', 'answer': money(sav) + (f'; payback {num(tc / sav, 2)} years' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m}


t = T(9, 'Benchmarking and quality standards', ['benchmarking and quality standards', 'benchmarking', 'quality standards', 'iso 9000'],
      defs=[('benchmarking', 'Comparing a business\'s products, processes or performance with those of the best firms in the industry (or other industries) in order to identify improvements.'),
            ('ISO 9000', 'An international quality standard awarded to organisations that have a quality management system meeting set requirements, checked by independent audit.'),
            ('quality standard', 'An agreed level of quality, often set by an external body, that products or processes must meet in order to carry a mark or certificate.'),
            ('internal benchmarking', 'Comparing performance between departments, branches or factories of the same business.')],
      mcqs=[('What is the first step in benchmarking?', 'Identify the process or aspect of performance to be improved', ['Copy the competitor\'s product exactly', 'Apply for ISO certification', 'Dismiss underperforming staff'],
             'Benchmarking starts by choosing what to compare, then whom to compare with.'),
            ('Why might a business seek ISO 9000 certification?', 'To show customers that it has an independently checked quality management system', ['Because it guarantees zero defects', 'To avoid paying tax', 'Because it reduces wages'],
             'ISO 9000 certifies systems, not product perfection.'),
            ('Comparing the waiting times at two branches of the same bank is', 'internal benchmarking', ['competitive benchmarking', 'kaizen', 'quality control'],
             'Comparisons within one organisation are internal benchmarking.')],
      exps=[('Explain one limitation of benchmarking.', 'Information on competitors may be hard to obtain; copying others does not create a unique advantage; what works elsewhere may not suit the business\'s culture.', '1 mark limitation; 1 mark explanation. [2]'),
            ('Explain why ISO 9000 certification does not guarantee high-quality products.', 'It certifies that procedures are followed and documented, not that the product standard is high; firms can consistently produce average quality.', '1 mark certifies systems; 1 mark not product quality. [2]'),
            ('Explain how benchmarking could help a business set targets.', 'It shows the performance of the best firms, providing realistic, evidence-based targets and showing how they were achieved.', '1 mark comparison with best practice; 1 mark target setting. [2]')],
      adv=[('benchmarking its processes against the best firms in its industry', ['identifies best practice to copy or adapt', 'realistic targets', 'faster improvement'],
            ['information hard to obtain', 'copying does not create advantage', 'may not suit its culture']),
           ('obtaining ISO 9000 certification', ['reassures customers and buyers', 'may be required for contracts', 'improves systems and consistency'],
            ['costly audits and paperwork', 'does not guarantee product quality', 'bureaucracy may slow change'])],
      anl=[('Analyse how benchmarking could improve the performance of {b}.', ['benchmarking compares performance with the best', 'identifies gaps in cost, quality or speed', 'adopting best practice improves efficiency', 'targets based on evidence motivate staff']),
           ('Analyse the benefits to {b} of gaining an international quality standard such as ISO 9000.', ['ISO 9000 certifies a quality management system', 'reassures overseas buyers of {prod}', 'can win contracts that require certification', 'documented procedures improve consistency'])],
      ev=[('Evaluate whether {b} should apply for ISO 9000 certification.', ['customer confidence', 'access to contracts', 'better systems'],
           ['costs of audit and documentation', 'no guarantee of product quality', 'bureaucracy'],
           ['whether customers demand it', 'the cost relative to benefits', 'what competitors hold']),
          ('Discuss whether benchmarking is the best way for {b} to improve quality.', ['learns from best practice', 'evidence-based targets', 'faster than trial and error'],
           ['TQM and kaizen build quality from within', 'data hard to obtain', 'copying limits innovation'],
           ['availability of comparable firms', 'the culture of the business', 'the size of the quality gap'])])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def bench_calc(r, D):
    c = r.choice(CASES)
    kpis = [('delivery on time (%)', r.choice([82, 85, 88, 90]), r.choice([95, 97, 98]), True),
            ('defect rate (%)', r.choice([3.5, 4, 5, 6]), r.choice([1, 1.5, 2]), False),
            ('average order processing time (hours)', r.choice([36, 40, 48, 60]), r.choice([18, 20, 24]), False),
            ('customer satisfaction score (out of 10)', r.choice([6.5, 7, 7.2]), r.choice([8.5, 8.8, 9]), True)]
    sel = r.sample(kpis, 3)
    if D == 1:
        n, a, b, hi = sel[0]
        gap = (b - a) / a * 100
        opts, ans = mc_num(r, abs(gap), [abs(b - a), abs(a - b) / b * 100, abs(gap) * 2], lambda x: pct(x))
        return {'stem': f'A firm\'s {n} is {num(a)}; the best in the industry is {num(b)}. By what percentage of the firm\'s own figure does it differ from the benchmark?', 'options': opts, 'answer': ans,
                'key': f'|{num(b)} − {num(a)}|/{num(a)} × 100 = {pct(abs(gap))}.', 'marks': 1}
    tbl = '; '.join(f'{n}: {c["b"]} {num(a)}, benchmark {num(b)}' for n, a, b, hi in sel)
    stem = f'{c["full"]} benchmarks its performance against the best firm in its industry — {tbl}. Calculate the percentage gap between {c["b"]} and the benchmark for each measure'
    key = '; '.join(f'{n}: ({num(b)} − {num(a)})/{num(a)} × 100 = {(b - a) / a * 100:+.1f}%' for n, a, b, hi in sel) + ' [3]'
    m = 3
    worst = max(sel, key=lambda x: abs(x[2] - x[1]) / x[1])
    if D >= 4:
        stem += ' and identify the measure with the largest gap, suggesting one way to close it'
        key += f'; largest relative gap: {worst[0]} [1]; suggestion e.g. process redesign, training, quality circles, technology [1]'
        m = 5
    return {'stem': stem + '.', 'answer': '; '.join(f'{n} {(b - a) / a * 100:+.1f}%' for n, a, b, hi in sel), 'key': key + f'. [{m}]', 'marks': m}

# =====================================================================================
# 10 Operations strategy
# =====================================================================================

t = T(10, 'Lean production', ['lean production: jit, kaizen and cell production', 'lean production', 'just-in-time', 'jit', 'cell production'],
      defs=[('lean production', 'An approach to operations that aims to minimise all forms of waste (time, materials, inventory, movement, defects) while maintaining quality.'),
            ('just-in-time (JIT)', 'An inventory management system in which materials and components arrive exactly when they are needed in production, so little or no buffer inventory is held.'),
            ('cell production', 'Organising production into self-contained teams (cells), each responsible for making a complete product or component.'),
            ('buffer inventory', 'The minimum level of inventory held to allow for unexpected demand or late deliveries.')],
      mcqs=[('Which condition is essential for just-in-time production to work?', 'Reliable suppliers who can deliver frequently at short notice', ['Large warehouses for inventory', 'Unpredictable demand', 'Suppliers located on another continent with slow shipping'],
             'JIT depends on reliable, frequent deliveries.'),
            ('Which is a benefit of cell production?', 'Team working increases motivation and responsibility', ['It always needs more inventory', 'It removes the need for training', 'Each worker performs one repetitive task'],
             'Cells give teams ownership of a whole product, linked to Herzberg/Mayo.'),
            ('Which is a likely disadvantage of JIT?', 'Production may stop if a delivery is late', ['Higher inventory holding costs', 'More working capital tied up in stock', 'More waste of materials'],
             'With no buffer stock, supply disruption halts production.')],
      exps=[('Explain how JIT reduces costs.', 'Less inventory means lower storage, insurance and financing costs, less working capital tied up and less waste from obsolete or damaged stock.', '1 mark lower holding costs; 1 mark working capital/waste. [2]'),
            ('Explain why lean production requires a flexible and multi-skilled workforce.', 'Production responds quickly to orders and waste is removed continuously, so staff must switch tasks, work in teams and suggest improvements.', '1 mark flexibility needed; 1 mark link to teams/kaizen. [2]'),
            ('Explain two risks of using JIT for a business that imports components from abroad.', 'Long supply chains increase the risk of delays (shipping, customs, strikes); exchange-rate and political disruption; no buffer stock to cope.', '2 × (1 mark risk, 1 mark explanation). [4]')],
      adv=[('introducing just-in-time inventory management', ['lower inventory holding costs', 'less working capital tied up', 'less waste of obsolete stock'],
            ['risk of production stopping if supplies are late', 'loss of bulk-buying discounts', 'more frequent ordering and transport costs']),
           ('reorganising production into cells', ['team ownership raises motivation', 'quality improves through responsibility', 'less movement and waiting time'],
            ['training costs', 'reorganisation disrupts production', 'conflict within teams'])],
      anl=[('Analyse how introducing lean production could affect {b}.', ['lean production minimises waste', 'lower inventory and unit costs', 'improved quality and faster response', 'requires reliable suppliers and trained staff']),
           ('Analyse the risks to {b} of using just-in-time inventory management.', ['JIT holds little or no buffer inventory', 'supply disruption stops production', 'unable to meet sudden rises in demand', 'higher transport costs from frequent deliveries'])],
      ev=[('Evaluate whether {b} should adopt just-in-time inventory management.', ['lower holding costs', 'less working capital tied up', 'less waste'],
           ['risk from supply disruption', 'loss of bulk discounts', 'demand may be unpredictable'],
           ['the reliability and location of its suppliers', 'how predictable demand is', 'the cost of a stock-out']),
          ('Discuss whether lean production is suitable for all businesses such as {b}.', ['cuts waste and costs', 'improves quality', 'more responsive'],
           ['needs stable demand and reliable suppliers', 'cultural change', 'vulnerable to shocks'],
           ['its industry and supply chain', 'its workforce skills', 'its competitive strategy'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def jit_calc(r, D):
    c = r.choice(CASES)
    inv1 = r.choice([400, 500, 600, 800, 1000, 1200]) * 1000
    inv2 = inv1 * r.choice([0.2, 0.25, 0.3, 0.4])
    hc = r.choice([15, 20, 25])
    extra = r.choice([20000, 30000, 40000])
    sav = (inv1 - inv2) * hc / 100
    if D == 1:
        opts, ans = mc_num(r, inv1 * hc / 100, [inv1 / hc, inv1 * hc / 10, hc * 1000], lambda x: money(x))
        return {'stem': f'A firm holds average inventory worth {money(inv1)}. Holding costs are {hc}% of inventory value a year. What is the annual holding cost?', 'options': opts, 'answer': ans,
                'key': f'{hc}% × {money(inv1)} = {money(inv1 * hc / 100)}.', 'marks': 1}
    stem = f'{c["full"]} holds average inventory worth {money(inv1)}. Annual holding costs (storage, insurance, finance) are {hc}% of the value. Under JIT, average inventory would fall to {money(inv2)}. Calculate the annual saving in holding costs'
    key = f'Saving = ({money(inv1)} − {money(inv2)}) × {hc}% = {money(sav)} [2]'
    m = 2
    if D >= 3:
        stem += f'. More frequent deliveries would add {money(extra)} a year in transport and ordering costs. Calculate the net saving'
        key += f'; net = {money(sav)} − {money(extra)} = {money(sav - extra)} [1]'
        m = 3
    if D >= 4:
        stem += '. Explain one non-financial factor the business should consider'
        key += '; supplier reliability, risk of disruption, quality, flexibility to meet demand [1]'
        m = 4
    if D >= 5:
        stem += ' and recommend whether to adopt JIT'
        key += '; justified recommendation [1]'
        m = 5
    return {'stem': stem + '.', 'answer': money(sav) + (f'; net {money(sav - extra)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


# ---- critical path analysis -----------------------------------------------------------------
NETS = [
    {'A': [], 'B': ['A'], 'C': ['A'], 'D': ['B'], 'E': ['C'], 'F': ['D', 'E']},
    {'A': [], 'B': [], 'C': ['A'], 'D': ['A'], 'E': ['B'], 'F': ['C'], 'G': ['D', 'E'], 'H': ['F', 'G']},
    {'A': [], 'B': ['A'], 'C': ['A'], 'D': ['A'], 'E': ['B'], 'F': ['C', 'D'], 'G': ['E', 'F']},
    {'A': [], 'B': [], 'C': ['A'], 'D': ['A', 'B'], 'E': ['C'], 'F': ['D'], 'G': ['E', 'F']},
    {'A': [], 'B': ['A'], 'C': ['B'], 'D': ['A'], 'E': ['D'], 'F': ['C', 'E'], 'G': ['F']},
]
PROJECTS = ['opening a new branch', 'launching a new product', 'installing a new production line', 'moving to a new warehouse', 'introducing a new IT system',
            'refurbishing its head office', 'setting up a stand at an international trade fair', 'building an extension to its factory']


def cpa(net, dur):
    est = {}
    for a in net:
        est[a] = max([est[p] + dur[p] for p in net[a]], default=0)
    end = max(est[a] + dur[a] for a in net)
    succ = {a: [b for b in net if a in net[b]] for a in net}
    lft = {}
    for a in reversed(list(net)):
        lft[a] = min([lft[s] - dur[s] for s in succ[a]], default=end)
    tf = {a: lft[a] - dur[a] - est[a] for a in net}
    crit = [a for a in net if tf[a] == 0]
    return est, lft, tf, end, crit


def _net(r):
    while True:
        net = r.choice(NETS)
        dur = {a: r.randint(2, 12) for a in net}
        est, lft, tf, end, crit = cpa(net, dur)
        if any(v > 0 for v in tf.values()) and len(crit) < len(net):
            return net, dur, est, lft, tf, end, crit


def _net_tbl(net, dur):
    return '; '.join(f'{a} ({dur[a]} days' + (f', after {" and ".join(net[a])})' if net[a] else ', starts at once)') for a in net)


def cpa_calc(r, D):
    c = r.choice(CASES)
    net, dur, est, lft, tf, end, crit = _net(r)
    proj = r.choice(PROJECTS)
    nc = [a for a in net if tf[a] > 0]
    x = r.choice(nc)
    stem = f'{c["full"]} is {proj}. The activities, durations and dependencies are: {_net_tbl(net, dur)}. Identify the critical path and the minimum project duration'
    key = f'EST: ' + ', '.join(f'{a}={est[a]}' for a in net) + f'; LFT: ' + ', '.join(f'{a}={lft[a]}' for a in net) + f' [1]; critical path {"–".join(crit)} (zero total float) [1]; duration {end} days [1]'
    m = 3
    if D >= 3:
        stem += f', and calculate the total float of activity {x}'
        key += f'; total float {x} = LFT {lft[x]} − duration {dur[x]} − EST {est[x]} = {tf[x]} days [1]'
        m = 4
    if D >= 4:
        dl = tf[x] + r.choice([1, 2, 3])
        stem += f'. Activity {x} is then delayed by {dl} days. State the effect on the project'
        key += f'; delay {dl} > float {tf[x]}, so project extends by {dl - tf[x]} day{"s" if dl - tf[x] != 1 else ""} to at least {end + dl - tf[x]} days, because the path through it becomes the longest [1]'
        m = 5
        if D >= 5:
            stem += ' and explain one way the business could use the network to recover the lost time'
            key += '; redeploy resources from activities with float to critical ones, overtime, run activities in parallel, crash critical activities [1]'
            m = 6
    ans = f'Critical path {"–".join(crit)}; duration {end} days' + (f'; float of {x} = {tf[x]} days' if D >= 3 else '')
    return {'stem': stem + '.', 'answer': ans, 'key': key + f'. [{m}]', 'marks': m, 'type': 'multi_step'}


t = T(10, 'Project management and critical path analysis', ['project management and critical path analysis (cpa)', 'critical path analysis', 'project management', 'network analysis'],
      defs=[('critical path', 'The sequence of activities in a network that determines the minimum duration of a project; any delay to a critical activity delays the whole project.'),
            ('total float', 'The amount of time an activity can be delayed without delaying the whole project: LFT − duration − EST.'),
            ('earliest start time (EST)', 'The earliest time at which an activity can begin, once all the activities it depends on are complete.'),
            ('latest finish time (LFT)', 'The latest time by which an activity must be completed if the project is not to be delayed.'),
            ('project', 'A specific and temporary set of activities with a clear objective, a start and finish date and a budget.')],
      mcqs=[('Activities on the critical path have a total float of', 'zero', ['one day', 'the length of the project', 'at least the duration of the activity'],
             'Critical activities cannot be delayed without delaying the project.'),
            ('Total float for an activity is calculated as', 'LFT − duration − EST', ['EST + duration − LFT', 'LFT − EST + duration', 'duration − EST'],
             'Total float = latest finish − duration − earliest start.'),
            ('Which is a limitation of critical path analysis?', 'It relies on estimated durations that may be inaccurate', ['It cannot show which activities can be done in parallel', 'It cannot identify the critical path', 'It ignores the order of activities'],
             'CPA is only as good as the time estimates.')],
      exps=[('Explain how critical path analysis can help a business manage working capital.', 'Knowing the EST of each activity means materials can be ordered to arrive just in time, reducing inventory and cash tied up.', '1 mark timing of resources; 1 mark lower inventory/cash. [2]'),
            ('Explain why identifying activities with float is useful to project managers.', 'Resources (staff, machines) can be moved from non-critical activities to critical ones to prevent or recover delays without extending the project.', '1 mark flexibility; 1 mark resource redeployment. [2]'),
            ('Explain two limitations of critical path analysis.', 'Durations are estimates; it does not guarantee completion or quality; complex projects make networks hard to draw and keep up to date; it does not show costs directly.', '2 × (1 mark limitation, 1 mark explanation). [4]')],
      adv=[('using critical path analysis to manage its project', ['identifies minimum duration and critical activities', 'resources and deliveries can be scheduled', 'shows where float allows flexibility'],
            ['estimates may be wrong', 'time-consuming for complex projects', 'does not ensure quality or motivate staff'])],
      anl=[('Analyse how critical path analysis could help {b} complete a major project on time.', ['CPA identifies the critical path and float', 'focus management attention on critical activities', 'schedule resources and deliveries just in time', 'monitor progress and react to delays']),
           ('Analyse the consequences for {b} if a critical activity in its expansion project is delayed.', ['critical activities have zero float', 'delay extends the whole project', 'extra costs and lost revenue', 'damage to customer relationships and reputation'])],
      ev=[('Evaluate the usefulness of critical path analysis to {b} when planning a major project.', ['identifies critical activities and duration', 'efficient scheduling of resources', 'monitoring tool'],
           ['relies on estimates', 'does not guarantee success', 'complex to maintain'],
           ['the complexity of the project', 'the accuracy of time estimates', 'how the network is updated']),
          ('Discuss whether good project management is more important than good planning tools for {b}.', ['tools like CPA provide structure', 'identify risks early', 'communicate the plan'],
           ['tools rely on people to use them', 'leadership and motivation matter', 'unexpected events need judgement'],
           ['the experience of the project manager', 'the size of the project', 'stakeholder involvement'])])
t.add('C3', (2, 3, 4, 5), 'numerical')(cpa_calc)


@t.add('C3', (1, 2), 'numerical')
def cpa_simple(r, D):
    net, dur, est, lft, tf, end, crit = _net(r)
    x = r.choice([a for a in net if tf[a] > 0])
    if D == 1:
        opts, ans = mc_num(r, tf[x], [lft[x] - est[x], tf[x] + dur[x], 0 if tf[x] else 1], lambda v: f'{round(v)} days')
        return {'stem': f'In a network, activity {x} has an earliest start time of {est[x]} days, a duration of {dur[x]} days and a latest finish time of {lft[x]} days. What is its total float?', 'options': opts, 'answer': ans,
                'key': f'Float = {lft[x]} − {dur[x]} − {est[x]} = {tf[x]} days.', 'marks': 1}
    return {'stem': f'A project has these activities: {_net_tbl(net, dur)}. Calculate the earliest start time of every activity and the minimum project duration.',
            'answer': ', '.join(f'{a} {est[a]}' for a in net) + f'; duration {end} days',
            'key': 'EST = latest of (EST + duration) of preceding activities: ' + ', '.join(f'{a}={est[a]}' for a in net) + f' [1]; duration = {end} days [1]. [2]', 'marks': 2}


@calc_part(t)
def cpa_parts(r, c):
    net, dur, est, lft, tf, end, crit = _net(r)
    x = r.choice([a for a in net if tf[a] > 0])
    tbl = _net_tbl(net, dur)
    return [lambda r: (f'For its project the activities are: {tbl}. Identify the critical path and the project duration.', f'{"–".join(crit)}; {end} days', f'EST/LFT method; critical path {"–".join(crit)}, {end} days [3]'),
            lambda r: (f'Using the same network, calculate the total float of activity {x}.', f'{tf[x]} days', f'{lft[x]} − {dur[x]} − {est[x]} = {tf[x]} [2]')]


t = T(10, 'ERP and innovation in operations', ['enterprise resource planning (erp) and innovation in operations', 'enterprise resource planning', 'erp', 'innovation in operations'],
      defs=[('enterprise resource planning (ERP)', 'Integrated software that links all the main functions of a business (operations, inventory, purchasing, finance, HR, sales) in one database so information is shared in real time.'),
            ('process innovation', 'Introducing a new or significantly improved method of production or delivery, e.g. robotics or automated warehousing.'),
            ('product innovation', 'Introducing a new or significantly improved good or service.'),
            ('automation', 'Using machines and computer-controlled systems to perform tasks previously done by people.')],
      mcqs=[('What is the main benefit of an ERP system?', 'All departments share accurate, real-time information from one database', ['It removes the need for any managers', 'It is cheap and quick to install', 'It guarantees higher sales'],
             'Integration of data across functions improves coordination and decisions.'),
            ('Which is a common problem when introducing an ERP system?', 'High cost and disruption during implementation', ['Too little information for managers', 'Departments become more separate', 'Inventory data become less accurate'],
             'ERP projects are expensive, complex and often delayed.'),
            ('A bank introducing a new mobile app service for customers is an example of', 'product (service) innovation', ['process innovation only', 'delayering', 'benchmarking'],
             'A new service offered to customers is product innovation.')],
      exps=[('Explain how ERP could reduce inventory costs.', 'Sales, production and purchasing data are linked, so materials are ordered automatically when needed, avoiding excess inventory and stock-outs.', '1 mark integrated real-time data; 1 mark lower/optimal inventory. [2]'),
            ('Explain the difference between product innovation and process innovation.', 'Product innovation creates new or improved products for customers; process innovation changes how products are made or delivered.', '1 mark each. [2]'),
            ('Explain why employees may resist the introduction of ERP.', 'They must learn new systems, may fear job losses from automation, and lose familiar ways of working and control over information.', '1 mark reason; 1 mark explanation. [2]')],
      adv=[('introducing an enterprise resource planning system', ['real-time shared data across departments', 'better inventory and production planning', 'faster and better-informed decisions'],
            ['high cost of software and training', 'disruption and risk of failure during installation', 'staff resistance and dependence on IT']),
           ('investing in process innovation such as robotics', ['lower unit costs', 'consistent quality', 'faster output'],
            ['high capital cost', 'redundancies and resistance', 'rapid obsolescence'])],
      anl=[('Analyse how an ERP system could improve the efficiency of {b}.', ['ERP integrates data from all departments', 'better coordination of purchasing, production and sales', 'lower inventory and fewer stock-outs', 'faster, more accurate management information']),
           ('Analyse how innovation in operations could give {b} a competitive advantage.', ['process innovation lowers costs and improves quality', 'faster delivery of {prod}', 'product innovation differentiates', 'innovation is hard for rivals to copy quickly'])],
      ev=[('Evaluate whether {b} should invest in an enterprise resource planning system.', ['integrated real-time information', 'lower inventory and better planning', 'improved customer service'],
           ['high cost and long implementation', 'risk of failure and disruption', 'training and staff resistance'],
           ['its size and complexity', 'its existing IT systems', 'the quality of implementation support']),
          ('Discuss whether innovation in operations is essential for the long-term success of {b}.', ['lower costs', 'higher quality', 'competitive advantage'],
           ['high cost and risk', 'marketing and HR may matter more', 'incremental improvement (kaizen) may be enough'],
           ['the pace of technological change in its industry', 'its finance', 'its competitors\' actions'])])


@t.add('C3', (1, 2, 3, 4), 'numerical')
def erp_calc(r, D):
    c = r.choice(CASES)
    cost = r.choice([400, 600, 800, 1000, 1500]) * 1000
    s_inv = r.choice([80, 100, 150, 200]) * 1000
    s_lab = r.choice([50, 60, 80, 100]) * 1000
    run = r.choice([20, 30, 40]) * 1000
    net = s_inv + s_lab - run
    if D == 1:
        opts, ans = mc_num(r, cost / net, [cost / (s_inv + s_lab), net / cost, cost / s_inv], lambda x: f'{num(x, 1)} years')
        return {'stem': f'An ERP system costs {money(cost)} and is expected to save {money(net)} a year (net). What is the payback period?', 'options': opts, 'answer': ans,
                'key': f'{money(cost)}/{money(net)} = {num(cost / net, 1)} years.', 'marks': 1}
    stem = (f'{c["full"]} is considering an ERP system costing {money(cost)}. It is expected to cut inventory holding costs by {money(s_inv)} a year and administration labour costs by {money(s_lab)} a year, '
            f'with running costs of {money(run)} a year. Calculate the net annual saving and the payback period')
    key = f'Net saving = {money(s_inv)} + {money(s_lab)} − {money(run)} = {money(net)} [1]; payback = {money(cost)}/{money(net)} = {num(cost / net, 2)} years [1]'
    m = 2
    if D >= 3:
        mo = (cost / net - int(cost / net)) * 12
        stem += ' in years and months'
        key += f'; = {int(cost / net)} years {round(mo)} months [1]'
        m = 3
    if D >= 4:
        stem += '. Explain one reason why the payback could be longer than forecast'
        key += '; implementation delays, training costs, staff resistance, savings overestimated [1]'
        m = 4
    return {'stem': stem + '.', 'answer': f'{money(net)} a year; payback {num(cost / net, 2)} years', 'key': key + f'. [{m}]', 'marks': m}


t = T(10, 'Flexibility and process innovation', ['flexibility and process innovation', 'operational flexibility', 'mass customisation', 'capacity utilisation'],
      defs=[('operational flexibility', 'The ability of a business to vary the volume, range or delivery times of its output quickly in response to changes in demand.'),
            ('mass customisation', 'Using flexible production systems to produce large volumes of products that are tailored to individual customers\' requirements.'),
            ('capacity utilisation', 'The proportion of maximum possible output that is being achieved: actual output ÷ maximum output × 100.'),
            ('outsourcing (operations)', 'Contracting another firm to carry out some production or operations activities, e.g. to cope with peaks in demand.')],
      mcqs=[('Which best describes mass customisation?', 'Producing large volumes of products tailored to individual orders using flexible systems', ['Producing identical products in huge batches', 'Making one-off handmade products', 'Producing only for a single customer'],
             'Combines low unit costs of mass production with tailoring.'),
            ('A business is working at 98% capacity utilisation. Which is a likely problem?', 'No spare capacity to meet extra orders and pressure on staff and machines', ['High unit fixed costs', 'Too much idle time', 'Low labour productivity'],
             'Very high utilisation leaves no slack for maintenance or extra demand.'),
            ('Which is a way of increasing operational flexibility?', 'Training staff to be multi-skilled', ['Holding fewer product lines with longer production runs', 'Using single-purpose machinery', 'Signing long fixed contracts with all staff'],
             'Multi-skilled staff can move to where they are needed.')],
      exps=[('Explain why low capacity utilisation increases unit costs.', 'Fixed costs are spread over fewer units, so fixed cost per unit and average cost rise.', '1 mark fixed costs; 1 mark spread over fewer units. [2]'),
            ('Explain two ways a business could respond to excess capacity.', 'Cut capacity (close a site, sell machinery, reduce staff) or increase demand (price cuts, promotion, new markets), or rent out capacity to other firms.', '2 × (1 mark method, 1 mark explanation). [4]'),
            ('Explain how flexible production can give a business a competitive advantage.', 'It can respond quickly to changes in demand and offer a wider range or customised products without large cost increases.', '1 mark responsiveness; 1 mark range/customisation. [2]')],
      adv=[('introducing flexible manufacturing systems', ['quick response to changing demand', 'wider product range', 'mass customisation possible'],
            ['high investment in technology', 'need for multi-skilled staff', 'complex scheduling']),
           ('subcontracting extra output to another firm at busy times', ['no extra fixed costs', 'meets peak demand', 'avoids turning orders away'],
            ['higher variable cost per unit', 'less control over quality', 'dependence on the subcontractor'])],
      anl=[('Analyse how greater operational flexibility could benefit {b}.', ['flexibility means varying volume, range and delivery quickly', 'meet seasonal or sudden changes in demand for {prod}', 'offer customised products at competitive cost', 'reduce inventory and waste']),
           ('Analyse the effects on {b} of operating at very high capacity utilisation for a long period.', ['capacity utilisation = output ÷ capacity', 'low fixed cost per unit', 'stress, overtime and maintenance problems', 'unable to accept new orders; quality may fall'])],
      ev=[('Evaluate how {b} should deal with a long-term fall in capacity utilisation to 60%.', ['rationalise capacity to cut fixed costs', 'boost demand through marketing', 'use spare capacity for new products'],
           ['cutting capacity is costly and hard to reverse', 'marketing may not raise demand enough', 'new products need investment'],
           ['whether the fall is temporary or permanent', 'its finance', 'the market outlook']),
          ('Discuss whether {b} should invest in flexible production technology.', ['responsiveness and range', 'mass customisation', 'lower inventory'],
           ['high capital cost', 'training needs', 'uncertain demand for customised {prod}'],
           ['customer demand for variety', 'competitors\' capabilities', 'the payback period'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def cap_calc(r, D):
    c = r.choice(CASES)
    cap = r.choice([10000, 12000, 15000, 20000, 25000, 40000])
    out = round(cap * r.choice([0.6, 0.65, 0.7, 0.75, 0.8]))
    FC = r.choice([60000, 90000, 120000, 150000, 200000])
    cu = out / cap * 100
    if D == 1:
        opts, ans = mc_num(r, cu, [cap / out * 100, 100 - cu, out / 1000], lambda x: pct(x))
        return {'stem': f'A plant has maximum capacity of {cap:,} units a month and produces {out:,}. What is its capacity utilisation?', 'options': opts, 'answer': ans,
                'key': f'{out:,}/{cap:,} × 100 = {pct(cu)}.', 'marks': 1}
    stem = f'{c["full"]} has a maximum capacity of {cap:,} units a month and currently produces {out:,} units. Monthly fixed costs are {money(FC)}. Calculate capacity utilisation and fixed cost per unit'
    key = f'CU = {out:,}/{cap:,} × 100 = {pct(cu)} [1]; FC per unit = {money(FC)}/{out:,} = {money(FC / out, 2)} [1]'
    m = 2
    if D >= 3:
        t2 = r.choice([85, 90, 95])
        o2 = cap * t2 / 100
        stem += f'. Calculate the fixed cost per unit if utilisation rose to {t2}%'
        key += f'; output = {round(o2):,}, FC per unit = {money(FC / o2, 2)} [1]'
        m = 3
    if D >= 4:
        stem += ' and explain one disadvantage of operating close to full capacity'
        key += '; no spare capacity for orders/maintenance, staff stress, quality problems [1]'
        m = 4
    if D >= 5:
        stem += '. Recommend one way to increase utilisation'
        key += '; e.g. extra marketing, new markets, subcontracting for other firms, rationalising capacity [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'{pct(cu)}; {money(FC / out, 2)} per unit' + (f'; {money(FC / o2, 2)} at {t2}%' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 11 Financial statements
# =====================================================================================

def _is_data(r):
    rev = r.choice([2.4, 3.6, 4.8, 6.0, 7.5, 9.0, 12.0, 15.0, 20.0, 25.0])
    cos = round(rev * r.choice([0.45, 0.5, 0.55, 0.6, 0.65]), 2)
    ex = round(rev * r.choice([0.15, 0.2, 0.25]), 2)
    intr = round(rev * r.choice([0.01, 0.02, 0.03]), 3)
    tax = r.choice([20, 25, 30])
    return rev, cos, ex, intr, tax


t = T(11, 'Income statement', ['income statement: revenue, gross profit and operating profit', 'income statement', 'gross profit', 'operating profit'],
      defs=[('income statement', 'A financial statement showing a business\'s revenue, costs and profit (or loss) over a period of time, usually one year.'),
            ('gross profit', 'Revenue minus cost of sales.'),
            ('operating profit', 'Gross profit minus operating (overhead) expenses; the profit made from the business\'s normal trading activities before interest and tax.'),
            ('profit for the year', 'The profit remaining after interest (finance costs) and corporation tax have been deducted from operating profit; it is available for dividends and retained earnings.'),
            ('retained earnings', 'The part of profit for the year that is kept in the business rather than paid out as dividends.')],
      mcqs=[('Which item is deducted from gross profit to calculate operating profit?', 'Overhead (operating) expenses', ['Cost of sales', 'Corporation tax', 'Dividends'],
             'Operating profit = gross profit − operating expenses.'),
            ('Cost of sales is best defined as', 'the direct cost of the goods sold during the period', ['all the expenses of the business', 'the value of closing inventory', 'the cost of new non-current assets'],
             'Cost of sales = opening inventory + purchases − closing inventory.'),
            ('Why might a business with rising revenue have falling operating profit?', 'Its cost of sales and overheads have risen faster than revenue', ['Its dividends have increased', 'It has bought new machinery', 'Its share price has fallen'],
             'Profit falls if costs grow faster than revenue.')],
      exps=[('Explain the difference between gross profit and operating profit.', 'Gross profit is revenue minus cost of sales; operating profit also deducts overhead expenses such as rent, salaries and marketing.', '1 mark each. [2]'),
            ('Explain why the quality of profit matters as well as the amount.', 'Profit from one-off events (e.g. selling assets) cannot be repeated; high-quality profit comes from continuing trading and is sustainable.', '1 mark one-off v recurring; 1 mark sustainability. [2]'),
            ('Explain two ways a business could increase its gross profit margin.', 'Raise selling prices (if demand is inelastic) or reduce cost of sales, e.g. by negotiating with suppliers, cutting waste or switching to cheaper materials.', '2 × (1 mark method, 1 mark explanation). [4]')],
      adv=[('retaining most of its profit for the year rather than paying dividends', ['internal finance for investment with no interest', 'no dilution of ownership', 'strengthens the statement of financial position'],
            ['shareholders may be dissatisfied', 'share price may fall', 'opportunity cost of the funds'])],
      anl=[('Analyse what {bp} income statement could tell its managers and shareholders.', ['the income statement shows revenue, costs and profit over a period', 'gross and operating profit margins show efficiency', 'trends over years reveal performance', 'profit for the year shows funds for dividends and reinvestment']),
           ('Analyse why {bp} operating profit might fall even though its gross profit has risen.', ['operating profit = gross profit − overheads', 'rising overheads (rent, salaries, marketing)', 'expansion costs before revenue grows', 'one-off expenses such as restructuring'])],
      ev=[('Evaluate whether {b} should pay a higher dividend or retain more of its profit.', ['higher dividends satisfy shareholders', 'support share price', 'signal confidence'],
           ['retained profit funds growth cheaply', 'avoids borrowing', 'keeps cash for uncertain times'],
           ['its investment opportunities', 'shareholders\' expectations', 'its cash position']),
          ('Discuss the usefulness of the income statement in judging the performance of {b}.', ['shows profitability and margins', 'trends over time', 'comparisons with rivals'],
           ['profit is not cash', 'historic data', 'ignores non-financial performance'],
           ['the quality of profit', 'the use of other statements', 'comparability of data'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def is_calc(r, D):
    c = r.choice(CASES)
    rev, cos, ex, intr, tax = _is_data(r)
    gp = rev - cos; op = gp - ex; pbt = op - intr; tx = pbt * tax / 100; pfy = pbt - tx
    if D == 1:
        opts, ans = mc_num(r, gp, [rev - cos - ex, cos, rev + cos], lambda x: f'${num(x, 2)}m')
        return {'stem': f'A business has revenue of ${num(rev, 2)}m and cost of sales of ${num(cos, 2)}m. What is its gross profit?', 'options': opts, 'answer': ans, 'key': f'{num(rev, 2)} − {num(cos, 2)} = ${num(gp, 2)}m.', 'marks': 1}
    stem = f'Extracts from the latest income statement of {c["full"]} ($m): revenue {num(rev, 2)}; cost of sales {num(cos, 2)}; overhead expenses {num(ex, 2)}'
    if D <= 2:
        stem += '. Calculate the gross profit and the operating profit.'
        return {'stem': stem, 'answer': f'Gross profit ${num(gp, 2)}m; operating profit ${num(op, 2)}m', 'key': f'GP = {num(rev, 2)} − {num(cos, 2)} = {num(gp, 2)} [1]; OP = {num(gp, 2)} − {num(ex, 2)} = {num(op, 2)} [1]. [2]', 'marks': 2}
    stem += f'; finance costs {num(intr, 3)}; corporation tax at {tax}% of profit before tax. Calculate the operating profit and the profit for the year'
    key = f'GP = {num(gp, 2)}; OP = {num(gp, 2)} − {num(ex, 2)} = {num(op, 2)} [1]; PBT = {num(op, 2)} − {num(intr, 3)} = {num(pbt, 3)} [1]; tax = {num(tx, 3)}; profit for the year = {num(pfy, 3)} [1]'
    m = 3
    if D >= 4:
        stem += ', and the gross and operating profit margins'
        key += f'; GPM = {num(gp, 2)}/{num(rev, 2)} × 100 = {pct(gp / rev * 100)}; OPM = {pct(op / rev * 100)} [1]'
        m = 4
    if D >= 5:
        dv = round(pfy * r.choice([0.3, 0.4, 0.5]), 3)
        stem += f'. Dividends of ${num(dv, 3)}m are paid. Calculate retained earnings for the year'
        key += f'; retained = {num(pfy, 3)} − {num(dv, 3)} = {num(pfy - dv, 3)} [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'Operating profit ${num(op, 2)}m; profit for the year ${num(pfy, 3)}m' + (f'; GPM {pct(gp / rev * 100)}, OPM {pct(op / rev * 100)}' if D >= 4 else ''),
            'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


def _sfp(r):
    nca = r.choice([4.0, 5.5, 6.0, 8.0, 10.0, 12.5])
    inv = round(r.choice([0.4, 0.6, 0.8, 1.0, 1.2, 1.5]) * nca / 5, 2)
    rec = round(r.choice([0.3, 0.5, 0.7, 0.9]) * nca / 5, 2)
    cash = round(r.choice([0.1, 0.2, 0.4, 0.6]) * nca / 5, 2)
    cl = round((inv + rec + cash) * r.choice([0.5, 0.65, 0.8, 1.0, 1.2]), 2)
    ncl = round(nca * r.choice([0.2, 0.3, 0.4, 0.5]), 2)
    return nca, inv, rec, cash, cl, ncl


t = T(11, 'Statement of financial position', ['statement of financial position: assets, liabilities and equity', 'statement of financial position', 'balance sheet', 'assets liabilities'],
      defs=[('statement of financial position', 'A financial statement showing the value of a business\'s assets, liabilities and equity at a particular date.'),
            ('non-current assets', 'Assets the business expects to keep and use for more than one year, such as buildings, machinery and vehicles.'),
            ('current liabilities', 'Debts the business must repay within one year, such as trade payables, overdrafts and tax owed.'),
            ('working capital', 'Current assets minus current liabilities; the finance available for day-to-day operations (net current assets).'),
            ('equity (total equity)', 'The shareholders\' stake in the business: share capital plus reserves such as retained earnings; equal to total assets minus total liabilities.')],
      mcqs=[('Which of these is a current asset?', 'Trade receivables', ['Machinery', 'Bank loan repayable in five years', 'Share capital'],
             'Current assets are cash or items expected to become cash within a year.'),
            ('Total equity is equal to', 'total assets minus total liabilities', ['current assets minus current liabilities', 'revenue minus costs', 'non-current assets plus current liabilities'],
             'Net assets = equity.'),
            ('A business with negative working capital is most likely to have', 'difficulty paying its short-term debts', ['too much cash', 'too many non-current assets', 'high profitability'],
             'Current liabilities exceed current assets, a liquidity risk.')],
      exps=[('Explain why a business needs enough working capital.', 'It must pay suppliers, wages and other short-term debts as they fall due; too little working capital risks insolvency even if profitable.', '1 mark meets short-term obligations; 1 mark consequence of shortage. [2]'),
            ('Explain why the value of non-current assets on the statement of financial position may differ from their market value.', 'They are recorded at historical cost less depreciation, which may not reflect what they could be sold for; intangible assets such as brands may not be shown.', '1 mark historical cost/depreciation; 1 mark market value or intangibles. [2]'),
            ('Explain the difference between current liabilities and non-current liabilities.', 'Current liabilities must be paid within a year (e.g. trade payables, overdraft); non-current liabilities are due after more than a year (e.g. long-term loans).', '1 mark each. [2]')],
      adv=[('selling and leasing back its premises to raise cash', ['large inflow of cash', 'improves liquidity and working capital', 'can repay debt or fund expansion'],
            ['loses ownership of a valuable asset', 'ongoing lease payments reduce profit', 'loses gains from rising property values'])],
      anl=[('Analyse how {b} could use its statement of financial position to assess its financial health.', ['the SFP shows assets, liabilities and equity at a date', 'working capital shows liquidity', 'balance of debt and equity shows gearing', 'changes over time show investment and financing']),
           ('Analyse the possible consequences for {b} of having too little working capital.', ['working capital = current assets − current liabilities', 'difficulty paying suppliers and wages', 'loss of supplier credit and discounts', 'risk of insolvency even when profitable'])],
      ev=[('Evaluate the best way for {b} to improve its working capital position.', ['reduce inventory (JIT)', 'collect receivables faster', 'negotiate longer credit from suppliers'],
           ['lower inventory risks stock-outs', 'tight credit may lose customers', 'suppliers may refuse'],
           ['the cause of the shortage', 'its relationship with suppliers and customers', 'how quickly cash is needed']),
          ('Discuss how useful the statement of financial position is to potential investors in {b}.', ['shows assets and liabilities', 'liquidity and gearing', 'shareholders\' equity'],
           ['historic, at one date', 'assets at book value', 'window dressing possible'],
           ['comparison with other years and firms', 'use alongside the income statement', 'quality of the notes'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def sfp_calc(r, D):
    c = r.choice(CASES)
    nca, inv, rec, cash, cl, ncl = _sfp(r)
    ca = inv + rec + cash
    wc = ca - cl
    eq = nca + ca - cl - ncl
    if D == 1:
        opts, ans = mc_num(r, wc, [ca + cl, cl - ca if cl != ca else 1, ca], lambda x: f'${num(x, 2)}m')
        return {'stem': f'A business has current assets of ${num(ca, 2)}m and current liabilities of ${num(cl, 2)}m. What is its working capital?', 'options': opts, 'answer': ans, 'key': f'{num(ca, 2)} − {num(cl, 2)} = ${num(wc, 2)}m.', 'marks': 1}
    stem = f'Extracts from the statement of financial position of {c["full"]} ($m): non-current assets {num(nca, 2)}; inventory {num(inv, 2)}; trade receivables {num(rec, 2)}; cash {num(cash, 2)}; current liabilities {num(cl, 2)}; non-current liabilities {num(ncl, 2)}. Calculate the working capital'
    key = f'Current assets = {num(inv, 2)} + {num(rec, 2)} + {num(cash, 2)} = {num(ca, 2)} [1]; working capital = {num(ca, 2)} − {num(cl, 2)} = {num(wc, 2)} [1]'
    m = 2
    if D >= 3:
        stem += ' and the total equity'
        key += f'; total assets = {num(nca + ca, 2)}; total liabilities = {num(cl + ncl, 2)}; equity = {num(eq, 2)} [1]'
        m = 3
    if D >= 4:
        sc = round(eq * r.choice([0.3, 0.4, 0.5]), 2)
        stem += f'. Share capital is ${num(sc, 2)}m. Calculate retained earnings (assume no other reserves)'
        key += f'; retained earnings = {num(eq, 2)} − {num(sc, 2)} = {num(eq - sc, 2)} [1]'
        m = 4
        if D >= 5:
            stem += ', and comment on the liquidity position'
            key += f'; working capital {"positive" if wc > 0 else "negative"}, current ratio {num(ca / cl, 2)} — {"adequate" if ca / cl >= 1.5 else "possible liquidity concern"} [1]'
            m = 5
    return {'stem': stem + '.', 'answer': f'Working capital ${num(wc, 2)}m' + (f'; equity ${num(eq, 2)}m' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(11, 'Inventory valuation and depreciation', ['inventory valuation and depreciation', 'depreciation', 'inventory valuation', 'straight-line'],
      defs=[('depreciation', 'The fall in the value of a non-current asset over its useful life, recorded as an expense in the income statement each year.'),
            ('straight-line depreciation', 'A method that charges the same amount of depreciation each year: (cost − residual value) ÷ expected useful life.'),
            ('net book value', 'The value of a non-current asset shown in the accounts: original cost minus accumulated depreciation.'),
            ('net realisable value', 'The amount for which inventory could be sold, minus any costs of making it ready for sale and selling it.')],
      mcqs=[('Inventory should be valued in the accounts at', 'the lower of cost and net realisable value', ['the higher of cost and selling price', 'its expected selling price', 'its replacement cost in every case'],
             'Prudence: inventory is not valued above what it can be sold for.'),
            ('Which statement about depreciation is correct?', 'It spreads the cost of a non-current asset over its useful life', ['It is a cash outflow each year', 'It increases operating profit', 'It applies to current assets'],
             'Depreciation is a non-cash expense matching cost to the years that benefit.'),
            ('A machine cost $50 000, has a residual value of $10 000 and a life of 5 years. Annual straight-line depreciation is', '$8 000', ['$10 000', '$12 000', '$6 000'],
             '(50 000 − 10 000)/5 = 8 000.')],
      exps=[('Explain why businesses depreciate non-current assets.', 'To match the cost of an asset to the years in which it helps earn revenue, so profit is not overstated, and to show a realistic asset value.', '1 mark matching/accurate profit; 1 mark realistic asset value. [2]'),
            ('Explain how overvaluing inventory affects the financial statements.', 'Closing inventory too high reduces cost of sales, so gross and operating profit are overstated, and current assets on the SFP are overstated.', '1 mark profit overstated; 1 mark assets overstated. [2]'),
            ('Explain why depreciation is not a cash flow.', 'The cash leaves when the asset is bought; depreciation only allocates that cost over time in the accounts, so no money is paid each year.', '1 mark cash paid at purchase; 1 mark accounting allocation. [2]')],
      adv=[('choosing a short estimated useful life for its new equipment', ['prudent: assets not overvalued', 'higher depreciation reduces taxable profit sooner', 'realistic if technology changes fast'],
            ['lower reported profit in early years', 'may worry shareholders', 'book value may understate usefulness'])],
      anl=[('Analyse how {bp} choice of depreciation policy could affect its reported results.', ['depreciation is a non-cash expense', 'higher depreciation lowers operating profit', 'net book value of assets falls faster', 'affects ratios such as ROCE and gearing']),
           ('Analyse why {b} must value its inventory carefully.', ['inventory valued at lower of cost and NRV', 'affects cost of sales and profit', 'affects current assets and liquidity ratios', 'obsolete or damaged stock must be written down'])],
      ev=[('Evaluate the importance of accurate inventory valuation for {b}.', ['profit accuracy', 'reliable liquidity ratios', 'tax and investor confidence'],
           ['valuation involves judgement', 'small effect if inventory is small', 'other estimates also matter'],
           ['the size of its inventory', 'the risk of obsolescence of {prod}', 'its accounting controls']),
          ('Discuss whether depreciation figures give a true picture of the value of {bp} non-current assets.', ['systematic, consistent method', 'matches cost to use', 'prudent'],
           ['based on estimates of life and residual value', 'market values may differ', 'ignores inflation'],
           ['the type of asset', 'the pace of technological change', 'the method chosen'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def dep_calc(r, D):
    c = r.choice(CASES)
    if r.random() < 0.3 and D <= 3:
        units = r.choice([200, 400, 500, 800, 1000])
        cost = r.choice([12, 15, 20, 25, 40])
        nrv = cost * r.choice([0.6, 0.75, 0.8, 1.2, 1.5])
        val = min(cost, nrv) * units
        opts, ans = mc_num(r, val, [max(cost, nrv) * units, cost * units if nrv < cost else nrv * units * 1.1, (cost + nrv) / 2 * units], lambda x: money(x))
        return {'stem': f'{c["full"]} holds {units} units of inventory that cost ${cost} each. They could now be sold for {money(nrv + 2, 2)} each, with selling costs of $2 per unit. At what value should the inventory be shown?', 'options': opts, 'answer': ans,
                'key': f'NRV = {money(nrv + 2, 2)} − $2 = {money(nrv, 2)}; lower of cost ${cost} and NRV → {money(min(cost, nrv), 2)} × {units} = {money(val)}.', 'marks': 2 if D > 1 else 1}
    cost = r.choice([24, 30, 40, 48, 60, 80, 120, 150, 200]) * 1000
    res = cost * r.choice([0, 0.1, 0.2, 0.25])
    life = r.choice([4, 5, 6, 8, 10])
    dep = (cost - res) / life
    n = r.randint(2, life - 1)
    nbv = cost - dep * n
    if D == 1:
        opts, ans = mc_num(r, dep, [cost / life, (cost + res) / life, dep * 2], lambda x: money(x))
        return {'stem': f'A machine costs {money(cost)}, has a residual value of {money(res)} and a useful life of {life} years. What is the annual straight-line depreciation?', 'options': opts, 'answer': ans,
                'key': f'({money(cost)} − {money(res)})/{life} = {money(dep)}.', 'marks': 1}
    stem = f'{c["full"]} buys equipment for {money(cost)}. It expects to use it for {life} years and then sell it for {money(res)}. Using the straight-line method, calculate the annual depreciation and the net book value after {n} years'
    key = f'Depreciation = ({money(cost)} − {money(res)})/{life} = {money(dep)} a year [1]; NBV after {n} years = {money(cost)} − {n} × {money(dep)} = {money(nbv)} [1]'
    m = 2
    if D >= 3:
        op = r.choice([3, 4, 5, 8]) * dep
        stem += f'. Operating profit before depreciation is {money(op)}. Calculate operating profit after depreciation'
        key += f'; {money(op)} − {money(dep)} = {money(op - dep)} [1]'
        m = 3
    if D >= 4:
        stem += '. Explain the effect on profit if the useful life were estimated at ' + f'{life + 2} years instead'
        dep2 = (cost - res) / (life + 2)
        key += f'; depreciation falls to {money(dep2)}, so profit rises by {money(dep - dep2)} a year [1]'
        m = 4
    if D >= 5:
        stem += ', and why managers might be tempted to do this'
        key += '; higher reported profit/ROCE, bonuses, investor confidence — but it does not change cash [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'{money(dep)} a year; NBV {money(nbv)}', 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 12 Analysis of published accounts
# =====================================================================================

t = T(12, 'Liquidity ratios', ['liquidity ratios: current ratio and acid test', 'current ratio', 'acid test', 'liquidity'],
      defs=[('liquidity', 'The ability of a business to pay its short-term debts as they fall due.'),
            ('current ratio', 'Current assets ÷ current liabilities; a measure of a firm\'s ability to meet its short-term liabilities.'),
            ('acid test ratio', '(Current assets − inventory) ÷ current liabilities; a stricter liquidity measure that excludes inventory because it may be hard to turn into cash quickly.'),
            ('overtrading', 'Expanding sales too quickly without enough working capital to finance the extra inventory and receivables, causing liquidity problems.')],
      mcqs=[('Why does the acid test ratio exclude inventory?', 'Inventory may not be easily or quickly converted into cash', ['Inventory is a liability', 'Inventory is always worthless', 'Inventory is a non-current asset'],
             'Inventory is the least liquid current asset.'),
            ('A current ratio of 0.7 suggests', 'the business may struggle to pay its short-term debts', ['the business holds too much cash', 'the business is highly profitable', 'the business has no current liabilities'],
             'Current liabilities exceed current assets.'),
            ('Which action would improve a firm\'s acid test ratio?', 'Selling surplus inventory for cash', ['Buying inventory on credit', 'Using cash to repay a long-term loan', 'Taking out a bank overdraft to buy inventory'],
             'Converting inventory into cash raises liquid assets without changing current liabilities.')],
      exps=[('Explain why a very high current ratio is not necessarily good.', 'It may mean too much money is tied up in idle cash, excess inventory or slow-paying receivables that could be used more profitably.', '1 mark idle resources; 1 mark opportunity cost/profitability. [2]'),
            ('Explain how a supermarket can operate with a current ratio below 1.', 'It sells inventory quickly for cash but pays suppliers on credit, so cash flows in before payables fall due.', '1 mark fast inventory turnover/cash sales; 1 mark credit from suppliers. [2]'),
            ('Explain two ways a business could improve its liquidity.', 'Sell surplus assets or inventory; chase receivables; sale and leaseback; convert short-term debt into long-term loans; raise share capital.', '2 × (1 mark method, 1 mark explanation). [4]')],
      adv=[('reducing its inventory levels to improve liquidity', ['releases cash', 'lower storage costs', 'less risk of obsolescence'],
            ['risk of stock-outs', 'loss of bulk discounts', 'customers may switch if orders are delayed'])],
      anl=[('Analyse how a fall in {bp} acid test ratio could affect the business.', ['acid test = liquid assets ÷ current liabilities', 'harder to pay suppliers and short-term debts', 'suppliers and banks may restrict credit', 'may need costly short-term finance']),
           ('Analyse the reasons why {bp} current ratio might have fallen over the last year.', ['current ratio = CA ÷ CL', 'cash used for investment in non-current assets', 'more short-term borrowing or overdraft', 'trade payables rising as purchases grow'])],
      ev=[('Evaluate the best way for {b} to improve its liquidity.', ['sale and leaseback releases large sums', 'reducing inventory releases cash', 'faster collection of receivables'],
           ['loss of assets and lease costs', 'stock-outs', 'tighter credit may lose customers'],
           ['the size and urgency of the problem', 'the cause of the low liquidity', 'its long-term plans']),
          ('Discuss whether liquidity ratios are more important than profitability ratios when assessing {b}.', ['firms fail through lack of cash', 'short-term survival', 'suppliers and banks focus on liquidity'],
           ['profit drives long-term success', 'investors focus on returns', 'liquidity can be managed with finance'],
           ['who is using the ratios', 'its current financial situation', 'industry norms'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def liq_calc(r, D):
    c = r.choice(CASES)
    nca, inv, rec, cash, cl, ncl = _sfp(r)
    ca = inv + rec + cash
    cr, at = ca / cl, (ca - inv) / cl
    if D == 1:
        opts, ans = mc_num(r, cr, [at, cl / ca, cr * 2], lambda x: num(x, 2))
        return {'stem': f'A business has current assets of ${num(ca, 2)}m and current liabilities of ${num(cl, 2)}m. What is its current ratio?', 'options': opts, 'answer': ans, 'key': f'{num(ca, 2)}/{num(cl, 2)} = {num(cr, 2)}.', 'marks': 1}
    stem = f'{c["full"]} has inventory ${num(inv, 2)}m, trade receivables ${num(rec, 2)}m, cash ${num(cash, 2)}m and current liabilities ${num(cl, 2)}m. Calculate the current ratio and the acid test ratio'
    key = f'CA = {num(ca, 2)} [1]; current ratio = {num(ca, 2)}/{num(cl, 2)} = {num(cr, 2)} [1]; acid test = ({num(ca, 2)} − {num(inv, 2)})/{num(cl, 2)} = {num(at, 2)} [1]'
    m = 3
    if D >= 4:
        stem += ' and comment on the liquidity of the business'
        key += f'; comment: CR {"above" if cr >= 1.5 else "below"} the usual 1.5–2 guide, acid test {"at or above" if at >= 1 else "below"} 1 — {"satisfactory" if cr >= 1.5 and at >= 1 else "possible difficulty meeting short-term debts"}; depends on industry [1]'
        m = 4
    if D >= 5:
        x = round(inv * 0.5, 2)
        stem += f'. Calculate the acid test ratio if half the inventory (${num(x, 2)}m) were sold for cash at cost'
        key += f'; new acid test = ({num(ca - inv, 2)} + {num(x, 2)})/{num(cl, 2)} = {num((ca - inv + x) / cl, 2)} [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'Current ratio {num(cr, 2)}; acid test {num(at, 2)}', 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(12, 'Profitability and efficiency ratios', ['profitability and efficiency ratios: roce, inventory turnover, receivables and payables days', 'roce', 'inventory turnover', 'receivables days', 'payables days'],
      defs=[('return on capital employed (ROCE)', 'Operating profit ÷ capital employed × 100, where capital employed = total equity + non-current liabilities; measures how well the business uses its long-term capital.'),
            ('inventory turnover', 'Cost of sales ÷ average inventory held; the number of times inventory is sold and replaced in a year.'),
            ('trade receivables (days)', 'Trade receivables ÷ revenue × 365; the average number of days customers take to pay.'),
            ('trade payables (days)', 'Trade payables ÷ cost of sales × 365; the average number of days the business takes to pay its suppliers.')],
      mcqs=[('Capital employed for ROCE is calculated as', 'total equity + non-current liabilities', ['current assets − current liabilities', 'total assets + current liabilities', 'revenue − cost of sales'],
             'Capital employed is the long-term finance invested in the business.'),
            ('A rise in trade receivables days means', 'customers are taking longer to pay', ['the business is paying suppliers faster', 'inventory is selling more quickly', 'profit margins have risen'],
             'More days = slower collection of debts.'),
            ('A fall in inventory turnover from 12 to 8 times a year suggests', 'inventory is being sold more slowly', ['inventory is selling faster', 'the business is more liquid', 'cost of sales has risen'],
             'Fewer turns = inventory held longer.')],
      exps=[('Explain why ROCE is often regarded as the most important profitability ratio.', 'It compares operating profit with the capital invested, so it shows the return on all long-term finance and can be compared with interest rates and other firms.', '1 mark profit relative to capital; 1 mark comparison use. [2]'),
            ('Explain how a business could reduce its trade receivables days.', 'Offer discounts for early payment, tighten credit checks and terms, chase late payers, or use debt factoring.', '1 mark method; 1 mark explanation. [2]'),
            ('Explain why a business may want its payables days to be higher than its receivables days.', 'It receives cash from customers before it must pay suppliers, improving cash flow and reducing the need for short-term finance.', '1 mark cash timing; 1 mark benefit. [2]')],
      adv=[('offering customers longer credit periods', ['attracts and keeps customers', 'can increase sales', 'matches competitors\' terms'],
            ['cash tied up in receivables', 'higher risk of bad debts', 'may need overdraft finance'])],
      anl=[('Analyse what a fall in ROCE could indicate about the performance of {b}.', ['ROCE = operating profit ÷ capital employed', 'falling margins from rising costs or price cuts', 'new investment not yet earning returns', 'less efficient use of assets']),
           ('Analyse how {b} could improve its inventory turnover.', ['inventory turnover = cost of sales ÷ average inventory', 'JIT and better forecasting reduce stock', 'removing slow-moving lines', 'promotions to sell excess inventory'])],
      ev=[('Evaluate the most effective way for {b} to improve its ROCE.', ['raise operating profit margins', 'sell under-used assets', 'improve asset utilisation'],
           ['price rises may cut sales', 'selling assets may limit growth', 'cost cuts may harm quality'],
           ['the cause of its low ROCE', 'competition in its market', 'its long-term strategy']),
          ('Discuss whether efficiency ratios give a complete picture of how well {b} is managed.', ['show inventory and credit control', 'comparisons over time', 'link to cash flow'],
           ['ignore quality and customer service', 'industry differences', 'based on year-end figures'],
           ['use with other ratios', 'comparison with competitors', 'non-financial information'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def prof_calc(r, D):
    c = r.choice(CASES)
    rev, cos, ex, intr, tax = _is_data(r)
    op = rev - cos - ex
    ce = round(op * r.choice([4, 5, 6, 8, 10]), 2)
    inv0 = round(cos * r.choice([0.08, 0.1, 0.125, 0.15]), 3); inv1 = round(inv0 * r.choice([0.9, 1.1, 1.2]), 3)
    rec = round(rev * r.choice([0.08, 0.1, 0.12, 0.15]), 3)
    pay = round(cos * r.choice([0.1, 0.12, 0.15]), 3)
    roce = op / ce * 100
    it = cos / ((inv0 + inv1) / 2)
    rd = rec / rev * 365; pd = pay / cos * 365
    if D == 1:
        opts, ans = mc_num(r, roce, [op / rev * 100, ce / op, roce / 2], lambda x: pct(x))
        return {'stem': f'A business has operating profit of ${num(op, 2)}m and capital employed of ${num(ce, 2)}m. What is its ROCE?', 'options': opts, 'answer': ans, 'key': f'{num(op, 2)}/{num(ce, 2)} × 100 = {pct(roce)}.', 'marks': 1}
    stem = f'Data for {c["full"]} ($m): revenue {num(rev, 2)}; cost of sales {num(cos, 2)}; operating profit {num(op, 2)}; capital employed {num(ce, 2)}; opening inventory {num(inv0, 3)}; closing inventory {num(inv1, 3)}; trade receivables {num(rec, 3)}; trade payables {num(pay, 3)}.'
    if D == 2:
        return {'stem': stem + ' Calculate the return on capital employed.', 'answer': pct(roce), 'key': f'ROCE = {num(op, 2)}/{num(ce, 2)} × 100 [1] = {pct(roce)} [1]. [2]', 'marks': 2}
    stem += ' Calculate the ROCE, the inventory turnover' + (', the trade receivables days and the trade payables days' if D >= 4 else ' and the trade receivables days')
    key = f'ROCE = {num(op, 2)}/{num(ce, 2)} × 100 = {pct(roce)} [1]; average inventory = {num((inv0 + inv1) / 2, 4)}, turnover = {num(cos, 2)}/{num((inv0 + inv1) / 2, 4)} = {num(it, 1)} times [1]; receivables days = {num(rec, 3)}/{num(rev, 2)} × 365 = {num(rd, 1)} days [1]'
    m = 3
    if D >= 4:
        key += f'; payables days = {num(pay, 3)}/{num(cos, 2)} × 365 = {num(pd, 1)} days [1]'
        m = 4
    if D >= 5:
        stem += '. Comment on the firm\'s management of working capital'
        key += f'; customers take {num(rd, 0)} days, suppliers paid in {num(pd, 0)} days: {"cash comes in before it goes out" if rd < pd else "cash goes out before it comes in, a pressure on liquidity"}; inventory turnover judged against industry [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'ROCE {pct(roce)}; inventory turnover {num(it, 1)} times; receivables {num(rd, 1)} days' + (f'; payables {num(pd, 1)} days' if D >= 4 else ''),
            'key': key + f'. [{m}]', 'marks': m, 'type': 'multi_step'}


t = T(12, 'Gearing and shareholder ratios', ['gearing and shareholder ratios: dividend yield, dividend cover, p/e', 'gearing', 'dividend yield', 'dividend cover', 'price earnings'],
      defs=[('gearing ratio', 'Non-current liabilities ÷ capital employed (total equity + non-current liabilities) × 100; the proportion of long-term finance that comes from borrowing.'),
            ('dividend yield', 'Dividend per share ÷ current share price × 100; the return a shareholder receives in dividends relative to the share price.'),
            ('dividend cover', 'Profit for the year (after tax) ÷ total annual dividends; how many times the dividend could be paid out of profit.'),
            ('price/earnings (P/E) ratio', 'Current share price ÷ earnings per share; shows how much investors are willing to pay for each $1 of earnings.'),
            ('earnings per share (EPS)', 'Profit for the year ÷ number of ordinary shares issued.')],
      mcqs=[('A business is usually described as highly geared when its gearing ratio is above about', '50%', ['10%', '25%', '100% exactly'],
             'Gearing above 50% means more than half of capital employed is borrowed.'),
            ('A high P/E ratio usually suggests that investors', 'expect strong future growth in earnings', ['expect earnings to fall sharply', 'receive high dividends', 'think the firm is about to fail'],
             'Investors pay more per $ of current earnings when they expect growth.'),
            ('Which is a risk of high gearing?', 'Interest payments must be made even when profits fall', ['Shareholders lose control to lenders automatically', 'Dividends must always be paid', 'Interest rates cannot change'],
             'Interest is a fixed commitment; higher rates or lower profits squeeze the business.')],
      exps=[('Explain why a highly geared business is more at risk when interest rates rise.', 'Most of its capital is borrowed, so higher rates raise interest costs sharply, reducing profit and possibly making repayments difficult.', '1 mark large debt; 1 mark interest cost/profit effect. [2]'),
            ('Explain why a low dividend cover may concern shareholders.', 'Most of the profit is paid out, so little is retained for investment and the dividend may be cut if profits fall.', '1 mark little retained/at risk; 1 mark explanation. [2]'),
            ('Explain one advantage of high gearing for shareholders.', 'If the return on borrowed funds exceeds the interest rate, the extra profit goes to shareholders, raising earnings per share, without diluting ownership.', '1 mark advantage; 1 mark explanation. [2]')],
      adv=[('financing its expansion with a large long-term loan', ['shareholders keep control', 'interest is tax-deductible', 'higher returns to shareholders if the project succeeds'],
            ['higher gearing and financial risk', 'interest must be paid even if profits fall', 'lenders may impose conditions'])],
      anl=[('Analyse how an increase in gearing could affect {b} and its shareholders.', ['gearing = NCL ÷ capital employed', 'higher interest costs and financial risk', 'possible higher returns on equity if investment succeeds', 'harder to borrow more in future']),
           ('Analyse what {bp} dividend yield and P/E ratio could tell potential investors.', ['dividend yield shows income return on the share price', 'P/E shows market expectations of growth', 'compare with other firms and interest rates', 'high P/E may mean shares are overvalued'])],
      ev=[('Evaluate whether {b} should raise finance for expansion by borrowing or by issuing new shares.', ['borrowing keeps control', 'interest tax-deductible', 'may raise EPS'],
           ['higher gearing and risk', 'new shares carry no repayment', 'dividends are not compulsory'],
           ['current gearing', 'interest rates', 'shareholders\' attitudes to control']),
          ('Discuss whether shareholder ratios are the best way to judge the success of {b}.', ['show returns to owners', 'reflect market confidence', 'easy to compare'],
           ['share price affected by market sentiment', 'ignore other stakeholders', 'short-term focus'],
           ['the type of investor', 'the time horizon', 'use of other measures'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def gear_calc(r, D):
    c = r.choice(CASES)
    eq = r.choice([8, 10, 12, 15, 20, 25, 40])
    ncl = round(eq * r.choice([0.25, 0.5, 0.8, 1.0, 1.5]), 2)
    g = ncl / (eq + ncl) * 100
    sh = r.choice([10, 20, 25, 40, 50])
    pfy = round(eq * r.choice([0.08, 0.1, 0.12, 0.15]), 2)
    dv = round(pfy * r.choice([0.25, 0.4, 0.5, 0.6]), 3)
    eps = pfy / sh
    dps = dv / sh
    price = round(eps * r.choice([8, 10, 12, 15, 20]), 2)
    if D == 1:
        opts, ans = mc_num(r, g, [ncl / eq * 100, eq / (eq + ncl) * 100, g / 2], lambda x: pct(x))
        return {'stem': f'A business has non-current liabilities of ${num(ncl, 2)}m and total equity of ${eq}m. What is its gearing ratio?', 'options': opts, 'answer': ans,
                'key': f'{num(ncl, 2)}/({eq} + {num(ncl, 2)}) × 100 = {pct(g)}.', 'marks': 1}
    stem = f'{c["full"]} has total equity of ${eq}m and non-current liabilities of ${num(ncl, 2)}m. Its profit for the year was ${num(pfy, 2)}m, it has {sh} million shares and it paid total dividends of ${num(dv, 3)}m. The share price is ${num(price, 2)}. Calculate '
    items = ['the gearing ratio']
    key = f'Gearing = {num(ncl, 2)}/{num(eq + ncl, 2)} × 100 = {pct(g)} [1]'
    m = 1
    if D >= 2:
        items.append('the dividend cover')
        key += f'; dividend cover = {num(pfy, 2)}/{num(dv, 3)} = {num(pfy / dv, 2)} times [1]'
        m = 2
    if D >= 3:
        items.append('the dividend yield')
        key += f'; DPS = {num(dv, 3)}/{sh} = ${num(dps, 4)}; yield = {num(dps, 4)}/{num(price, 2)} × 100 = {pct(dps / price * 100, 2)} [1]'
        m = 3
    if D >= 4:
        items.append('the P/E ratio')
        key += f'; EPS = {num(pfy, 2)}/{sh} = ${num(eps, 4)}; P/E = {num(price, 2)}/{num(eps, 4)} = {num(price / eps, 1)} [1]'
        m = 4
    stem += (', '.join(items[:-1]) + ' and ' + items[-1]) if len(items) > 1 else items[0]
    if D >= 5:
        stem += '. Comment on whether the business could safely borrow more'
        key += f'; gearing {pct(g)} is {"high (above 50%)" if g > 50 else "moderate/low"}; consider interest cover, profitability, interest rates [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'Gearing {pct(g)}' + (f'; cover {num(pfy / dv, 2)}' if D >= 2 else '') + (f'; yield {pct(dps / price * 100, 2)}' if D >= 3 else '') + (f'; P/E {num(price / eps, 1)}' if D >= 4 else ''),
            'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(12, 'Uses and limitations of ratio analysis', ['uses and limitations of ratio analysis', 'ratio analysis limitations', 'uses of ratios'],
      defs=[('ratio analysis', 'Comparing figures from the financial statements as ratios to assess a business\'s profitability, liquidity, efficiency, gearing and returns to shareholders.'),
            ('window dressing', 'Presenting the accounts in a way that makes the business look better than it really is, e.g. by timing transactions just before the year end.'),
            ('inter-firm comparison', 'Comparing a business\'s ratios with those of other firms in the same industry.'),
            ('trend analysis', 'Comparing a business\'s ratios over several years to identify improvement or deterioration.')],
      mcqs=[('Which is a limitation of ratio analysis?', 'Ratios are based on past data and may not predict future performance', ['Ratios cannot be compared over time', 'Ratios use no data from the accounts', 'Ratios always include non-financial information'],
             'Historical data may not reflect current conditions.'),
            ('Comparing ratios with firms in other industries is unreliable because', 'industries have different norms, e.g. for inventory and liquidity', ['all industries have identical ratios', 'ratios cannot be calculated for other firms', 'other firms do not publish accounts'],
             'Compare like with like.'),
            ('Which stakeholder is most interested in gearing and liquidity ratios?', 'A bank considering a loan', ['A customer buying one product', 'A local resident', 'A competitor\'s employee'],
             'Lenders care about repayment ability and risk.')],
      exps=[('Explain why ratios should be compared over time and with other firms.', 'A single ratio has little meaning; trends show improvement or decline, and inter-firm comparison shows performance relative to competitors.', '1 mark trend; 1 mark inter-firm. [2]'),
            ('Explain two limitations of using ratio analysis to judge a business.', 'Historic data; different accounting policies; window dressing; inflation; ignores qualitative factors such as staff morale or brand strength.', '2 × (1 mark limitation, 1 mark explanation). [4]'),
            ('Explain why different stakeholders are interested in different ratios.', 'Shareholders focus on returns (ROCE, dividend yield); lenders on liquidity and gearing; managers on efficiency; each has different objectives.', '1 mark example of different interests; 1 mark explanation. [2]')],
      adv=[('relying on ratio analysis to compare itself with competitors', ['objective comparison', 'identifies strengths and weaknesses', 'sets targets'],
            ['different accounting policies', 'historic data', 'ignores qualitative factors'])],
      anl=[('Analyse how the managers of {b} could use ratio analysis to improve decision-making.', ['ratios measure profitability, liquidity, efficiency, gearing', 'trends identify problems early', 'inter-firm comparison benchmarks performance', 'sets targets for departments']),
           ('Analyse why ratio analysis alone might give a misleading view of {bp} performance.', ['ratios use historical data', 'window dressing and accounting policies', 'industry and economic context matter', 'non-financial factors ignored'])],
      ev=[('Evaluate the usefulness of ratio analysis to a potential investor in {b}.', ['shows profitability and returns', 'risk via gearing and liquidity', 'comparisons with rivals'],
           ['historic and possibly window-dressed', 'ignores future plans and qualitative factors', 'differences in accounting policies'],
           ['access to several years of data', 'comparable firms', 'other information such as strategy and management']),
          ('Discuss whether non-financial information is more important than ratio analysis in assessing {b}.', ['brand, staff, innovation drive future success', 'ratios are backward-looking', 'stakeholder concerns such as CSR'],
           ['ratios are objective and comparable', 'financial health determines survival', 'non-financial data are hard to measure'],
           ['the purpose of the assessment', 'the stakeholder involved', 'quality of information available'])])


@t.add('C3', (2, 3, 4, 5), 'numerical')
def ratio_compare(r, D):
    c, k = r.sample(CASES, 2)
    a = dict(op=r.choice([2.0, 2.5, 3.0, 4.0]), ce=r.choice([15, 20, 25, 30]), ca=r.choice([3.0, 4.0, 5.0]), inv=r.choice([1.0, 1.5, 2.0]), cl=r.choice([2.0, 2.5, 3.0, 4.0]))
    b = dict(op=r.choice([1.5, 2.0, 3.5, 5.0]), ce=r.choice([12, 18, 24, 40]), ca=r.choice([2.5, 3.5, 6.0]), inv=r.choice([0.5, 1.0, 2.5]), cl=r.choice([1.5, 2.0, 3.5]))
    ra = (a['op'] / a['ce'] * 100, a['ca'] / a['cl'], (a['ca'] - a['inv']) / a['cl'])
    rb = (b['op'] / b['ce'] * 100, b['ca'] / b['cl'], (b['ca'] - b['inv']) / b['cl'])
    def row(n, d):
        return f'{n}: operating profit ${num(d["op"])}m, capital employed ${d["ce"]}m, current assets ${num(d["ca"])}m (inventory ${num(d["inv"])}m), current liabilities ${num(d["cl"])}m'
    stem = f'An investor is comparing two businesses in the same industry. {row(c["b"], a)}. {row(k["b"], b)}. Calculate the ROCE, current ratio and acid test ratio of each business'
    key = (f'{c["b"]}: ROCE {pct(ra[0])}, CR {num(ra[1], 2)}, acid test {num(ra[2], 2)} [2]; {k["b"]}: ROCE {pct(rb[0])}, CR {num(rb[1], 2)}, acid test {num(rb[2], 2)} [2]')
    m = 4
    if D >= 4:
        better = c['b'] if ra[0] > rb[0] else k['b']
        stem += ' and advise the investor which appears the better investment'
        key += f'; {better} has the higher ROCE; weigh against liquidity and risk; limitations: one year only, accounting policies, non-financial factors [2]'
        m = 6
    return {'stem': stem + '.', 'answer': f'{c["b"]}: {pct(ra[0])}, {num(ra[1], 2)}, {num(ra[2], 2)}; {k["b"]}: {pct(rb[0])}, {num(rb[1], 2)}, {num(rb[2], 2)}', 'key': key + f'. [{m}]', 'marks': m, 'type': 'multi_step'}

# =====================================================================================
# 13 Investment appraisal
# =====================================================================================

DF = {6: (0.943, 0.890, 0.840, 0.792, 0.747), 8: (0.926, 0.857, 0.794, 0.735, 0.681), 10: (0.909, 0.826, 0.751, 0.683, 0.621), 12: (0.893, 0.797, 0.712, 0.636, 0.567)}


def _project(r, n=None):
    n = n or r.choice([4, 5])
    I = r.choice([100, 120, 150, 200, 240, 300, 400, 500]) * 1000
    tot = I * r.choice([1.25, 1.3, 1.4, 1.5, 1.6, 1.8])
    shape = r.choice([(1, 1, 1, 1, 1), (0.6, 0.9, 1.1, 1.2, 1.2), (1.4, 1.2, 1, 0.8, 0.6), (0.8, 1, 1.2, 1, 1)])[:n]
    cfs = [round(tot * w / sum(shape) / 1000) * 1000 for w in shape]
    return I, cfs


def payback(I, cfs):
    cum = 0
    for i, cf in enumerate(cfs):
        if cum + cf >= I:
            frac = (I - cum) / cf
            return i + frac, i, I - cum, cf
        cum += cf
    return None


def fmt_pb(pb):
    y = int(pb); mo = round((pb - y) * 12)
    if mo == 12:
        y, mo = y + 1, 0
    return f'{y} years {mo} months'


t = T(13, 'Payback and average rate of return', ['payback and average rate of return (arr)', 'payback', 'average rate of return', 'arr'],
      defs=[('investment appraisal', 'Evaluating the profitability or desirability of an investment project using quantitative methods (payback, ARR, NPV) and qualitative factors.'),
            ('payback period', 'The length of time it takes for the net cash inflows from an investment to repay its initial capital cost.'),
            ('average rate of return (ARR)', 'The average annual profit from an investment expressed as a percentage of its initial cost: (total net profit ÷ years) ÷ initial cost × 100.'),
            ('net cash flow', 'Cash inflows minus cash outflows for a period.')],
      mcqs=[('Which is a main advantage of the payback method?', 'It is simple and highlights how quickly the investment is recovered, reducing risk', ['It considers all cash flows over the project\'s life', 'It takes account of the time value of money', 'It measures profitability as a percentage'],
             'Payback is easy and focuses on liquidity and risk.'),
            ('Which is a key limitation of the ARR method?', 'It ignores the timing of cash flows', ['It ignores profitability', 'It cannot be compared with interest rates', 'It only uses the first year\'s cash flow'],
             'ARR averages profit, so early and late returns are treated the same.'),
            ('A project costs $60 000 and returns $15 000 a year. Its payback period is', '4 years', ['3 years', '5 years', '2.5 years'],
             '60 000/15 000 = 4 years.')],
      exps=[('Explain why a business might prefer a project with a shorter payback period.', 'Cash is recovered sooner, reducing risk from uncertain future cash flows and improving liquidity; useful when technology changes fast.', '1 mark lower risk; 1 mark liquidity/uncertainty. [2]'),
            ('Explain one advantage and one limitation of ARR.', 'Advantage: uses all cash flows and gives a percentage that can be compared with interest rates or targets. Limitation: ignores timing of cash flows / time value of money.', '1 mark each with explanation. [2]'),
            ('Explain why the results of investment appraisal are uncertain.', 'They rely on forecasts of costs and revenues several years ahead, which may be wrong because of economic change, competition or technology.', '1 mark forecasts; 1 mark reasons for error. [2]')],
      adv=[('using the payback method to choose between projects', ['simple to calculate and understand', 'focuses on early cash recovery and risk', 'useful when cash is short'],
            ['ignores cash flows after payback', 'ignores profitability', 'ignores time value of money'])],
      anl=[('Analyse how {b} could use payback and ARR to decide whether to invest in {newprod}.', ['payback shows how quickly the cost is recovered', 'ARR shows average annual return as a percentage', 'compare with criteria such as target ARR or interest rate', 'limitations: forecasts and timing of cash flows']),
           ('Analyse why {b} might reject a project with a high ARR.', ['ARR averages profit over the life', 'long payback increases risk', 'cash flows uncertain in later years', 'qualitative factors or better alternatives'])],
      ev=[('Evaluate whether {b} should rely on payback when choosing investment projects.', ['simple and quick', 'emphasises liquidity and risk', 'suitable when technology changes fast'],
           ['ignores later cash flows', 'ignores profitability', 'ignores time value of money'],
           ['its cash position', 'the riskiness of the projects', 'use alongside ARR and NPV']),
          ('Discuss whether quantitative investment appraisal is enough for {b} to decide whether to invest.', ['objective comparison', 'shows financial return', 'helps raise finance'],
           ['based on forecasts', 'ignores qualitative factors (staff, image, strategy)', 'risk not fully captured'],
           ['the reliability of forecasts', 'strategic importance of the project', 'stakeholder impacts'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def pb_arr_calc(r, D):
    c = r.choice(CASES)
    I, cfs = _project(r)
    pb, yrs, rem, cf = payback(I, cfs)
    n = len(cfs)
    profit = sum(cfs) - I
    arr = profit / n / I * 100
    if D == 1:
        opts, ans = mc_num(r, arr, [profit / I * 100, sum(cfs) / n / I * 100, arr / 2], lambda x: pct(x))
        return {'stem': f'A project costs {money(I)} and generates total net cash inflows of {money(sum(cfs))} over {n} years. What is its ARR?', 'options': opts, 'answer': ans,
                'key': f'Total profit = {money(profit)}; average = {money(profit / n)}; ARR = {money(profit / n)}/{money(I)} × 100 = {pct(arr)}.', 'marks': 1}
    flows = ', '.join(f'year {i + 1} {money(x)}' for i, x in enumerate(cfs))
    stem = f'{c["full"]} is considering investing {money(I)} in {c["newprod"]}. Forecast net cash inflows are: {flows}. Calculate the payback period'
    key = f'Cumulative after {yrs} years = {money(I - rem)}; remaining {money(rem)} recovered in {money(rem)}/{money(cf)} × 12 = {round(rem / cf * 12)} months [1]; payback = {fmt_pb(pb)} [1]'
    m = 2
    if D >= 3:
        stem += ' and the average rate of return'
        key += f'; total profit = {money(sum(cfs))} − {money(I)} = {money(profit)} [1]; average annual profit = {money(profit / n)} [1]; ARR = {pct(arr)} [1]'
        m = 5
    if D >= 4:
        tgt = r.choice([8, 10, 12, 15])
        stem += f'. The business requires a payback within 3 years and an ARR of at least {tgt}%. Recommend whether it should invest'
        key += f'; payback {"meets" if pb <= 3 else "fails"} the 3-year criterion and ARR {"meets" if arr >= tgt else "fails"} the {tgt}% target; recommendation also considers forecast reliability and qualitative factors [1]'
        m = 6
    return {'stem': stem + '.', 'answer': f'Payback {fmt_pb(pb)}' + (f'; ARR {pct(arr)}' if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


def _npv(I, cfs, rate):
    dfs = DF[rate][:len(cfs)]
    pv = [cf * d for cf, d in zip(cfs, dfs)]
    return sum(pv) - I, pv, dfs


t = T(13, 'Net present value', ['discounted cash flow: net present value (npv)', 'net present value', 'npv', 'discounted cash flow'],
      defs=[('net present value (NPV)', 'The total present value of a project\'s future net cash flows minus the initial cost of the investment.'),
            ('discounting', 'Reducing the value of future cash flows to give their present value, because money received in the future is worth less than money received today.'),
            ('discount factor', 'The number by which a future cash flow is multiplied to find its present value; it depends on the discount rate and the year.'),
            ('time value of money', 'The idea that a sum of money is worth more now than the same sum in the future, because it could be invested to earn interest.')],
      mcqs=[('A project has a positive NPV at a discount rate of 10%. This means', 'its discounted cash inflows exceed the initial cost', ['its payback is less than one year', 'its ARR is exactly 10%', 'it will definitely be profitable'],
             'Positive NPV: the project earns more than the 10% cost of capital, if forecasts are correct.'),
            ('If a business raises the discount rate it uses, the NPV of a project will', 'fall', ['rise', 'stay the same', 'become infinite'],
             'Higher rates give smaller discount factors and lower present values.'),
            ('Why are future cash flows discounted?', 'Money received in the future is worth less than money received today', ['To include inflation in the initial cost', 'Because future cash flows are always negative', 'To calculate payback'],
             'The time value of money: money now can earn interest.')],
      exps=[('Explain why NPV is often considered better than payback for appraising investments.', 'NPV uses all cash flows over the project\'s life and allows for the time value of money, so it measures the true increase in value, not just speed of repayment.', '1 mark all cash flows; 1 mark time value of money. [2]'),
            ('Explain how the choice of discount rate affects investment decisions.', 'A higher rate reduces present values, so fewer projects have positive NPVs; the rate should reflect the cost of finance and risk.', '1 mark effect on PV/NPV; 1 mark link to cost of capital/risk. [2]'),
            ('Explain one limitation of NPV.', 'The discount rate and future cash flows are estimates; the result is hard for non-specialists to understand; it ignores qualitative factors.', '1 mark limitation; 1 mark explanation. [2]')],
      adv=[('using net present value to appraise its investment in {newprod}', ['allows for the time value of money', 'uses all forecast cash flows', 'shows the increase in value in money terms'],
            ['depends on choosing the right discount rate', 'complex to explain', 'relies on uncertain forecasts'])],
      anl=[('Analyse why {b} should use discounted cash flow methods when appraising long-term projects.', ['DCF allows for the time value of money', 'later cash flows are worth less in present value terms', 'discount rate can reflect cost of capital and risk', 'NPV shows value created']),
           ('Analyse how a rise in interest rates could affect {bp} investment decisions.', ['higher interest rates raise the cost of capital', 'higher discount rate lowers NPV', 'some projects become unprofitable', 'borrowing to invest becomes more expensive'])],
      ev=[('Evaluate whether {b} should invest in a project with a small positive NPV but a long payback period.', ['positive NPV adds value', 'all cash flows considered', 'strategic benefits'],
           ['long payback increases risk', 'small NPV means little margin for error', 'cash flow pressure'],
           ['the reliability of the forecasts', 'its liquidity', 'alternative uses of the funds']),
          ('Discuss whether NPV is the most useful investment appraisal method for {b}.', ['time value of money', 'whole life of project', 'clear decision rule'],
           ['depends on discount rate and forecasts', 'harder to understand', 'payback may matter more when cash is tight'],
           ['the length of the project', 'its financial position', 'use of several methods together'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def npv_calc(r, D):
    c = r.choice(CASES)
    I, cfs = _project(r, r.choice([3, 4, 5]))
    rate = r.choice([6, 8, 10, 12])
    npv, pv, dfs = _npv(I, cfs, rate)
    if D == 1:
        y = r.randrange(len(cfs))
        opts, ans = mc_num(r, pv[y], [cfs[y] / dfs[y], cfs[y] * (1 - dfs[y]), cfs[y]], lambda x: money(x))
        return {'stem': f'A cash inflow of {money(cfs[y])} is expected in year {y + 1}. The discount factor at {rate}% for year {y + 1} is {dfs[y]:.3f}. What is its present value?', 'options': opts, 'answer': ans,
                'key': f'{money(cfs[y])} × {dfs[y]:.3f} = {money(pv[y])}.', 'marks': 1}
    flows = ', '.join(f'year {i + 1} {money(x)}' for i, x in enumerate(cfs))
    facs = ', '.join(f'year {i + 1} {d:.3f}' for i, d in enumerate(dfs))
    stem = f'{c["full"]} is appraising a project costing {money(I)} with forecast net cash inflows: {flows}. Discount factors at {rate}% are: {facs}. Calculate the net present value'
    key = 'PVs: ' + ', '.join(f'{money(cf)} × {d:.3f} = {money(p)}' for cf, d, p in zip(cfs, dfs, pv)) + f' [2]; total PV = {money(sum(pv))} [1]; NPV = {money(sum(pv))} − {money(I)} = {money(npv)} [1]'
    m = 4
    if D >= 4:
        stem += ' and state whether the project is financially worthwhile'
        key += f'; NPV is {"positive" if npv > 0 else "negative"}, so the project {"earns more than" if npv > 0 else "does not cover"} the {rate}% cost of capital [1]'
        m = 5
    if D >= 5:
        stem += '. Explain one reason why the business might not go ahead even if the NPV is positive'
        key += '; uncertain forecasts, high risk, long payback, better alternatives, qualitative factors [1]'
        m = 6
    if D == 2:
        stem = stem.replace('Calculate the net present value', 'Calculate the present value of each year\'s cash flow and the net present value')
    return {'stem': stem + '.', 'answer': f'NPV = {money(npv)}', 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


@calc_part(t)
def npv_parts(r, c):
    I, cfs = _project(r, 3)
    rate = r.choice([8, 10, 12])
    npv, pv, dfs = _npv(I, cfs, rate)
    pb = payback(I, cfs)
    flows = ', '.join(f'year {i + 1} {money(x)}' for i, x in enumerate(cfs))
    facs = ', '.join(f'{d:.3f}' for d in dfs)
    return [lambda r: (f'A proposed project costs {money(I)} with net cash inflows of {flows}. Using discount factors at {rate}% of {facs}, calculate the NPV.', money(npv),
                       'PVs ' + ', '.join(money(p) for p in pv) + f'; NPV {money(npv)} [4]')] + ([lambda r: (f'Calculate the payback period of the same project (inflows {flows}; cost {money(I)}).', fmt_pb(pb[0]), f'cumulative method; {fmt_pb(pb[0])} [2]')] if pb else [])


t = T(13, 'Qualitative factors and risk in investment decisions', ['qualitative factors and risk in investment decisions', 'qualitative factors', 'risk', 'sensitivity analysis'],
      defs=[('sensitivity analysis', 'Testing how the outcome of an investment appraisal changes if key forecasts (e.g. sales, costs, discount rate) turn out differently.'),
            ('qualitative factors (investment)', 'Non-numerical influences on an investment decision, such as the effect on staff morale, the environment, brand image and fit with corporate objectives.'),
            ('risk (investment)', 'The possibility that the actual results of an investment differ from those forecast, especially that returns are lower.'),
            ('criterion level', 'The minimum acceptable result set by a business for an appraisal method, e.g. a maximum payback of 3 years or a minimum ARR of 12%.')],
      mcqs=[('Which is a qualitative factor in an investment decision to automate a factory?', 'The likely reaction of the workforce and trade unions', ['The payback period', 'The net present value', 'The ARR'],
             'Qualitative factors cannot be easily expressed in numbers.'),
            ('Sensitivity analysis is used to', 'see how the result changes if forecasts are wrong', ['calculate the payback period', 'fix the discount rate', 'remove all risk from investment'],
             'It tests the robustness of the appraisal to changes in assumptions.'),
            ('Why might a business accept a project with a negative NPV?', 'It is essential for legal compliance or long-term strategy', ['Negative NPV means high profit', 'NPV always overstates returns', 'Negative NPV reduces risk'],
             'Strategic, legal or ethical reasons can override financial results.')],
      exps=[('Explain why managers should consider qualitative factors in investment decisions.', 'Numbers cannot capture effects on morale, reputation, the environment or strategic fit, which may decide long-run success.', '1 mark examples; 1 mark long-run impact. [2]'),
            ('Explain how sensitivity analysis helps managers deal with risk.', 'It shows how much the forecasts can change before the project becomes unviable, so managers can judge how safe the margin is.', '1 mark testing assumptions; 1 mark judging margin of safety. [2]'),
            ('Explain why forecasts of cash flows for a five-year project may be unreliable.', 'Future sales, costs, prices, competition, exchange rates and the economy are all uncertain, and errors compound over time.', '1 mark uncertainty; 1 mark examples. [2]')],
      adv=[('carrying out sensitivity analysis before investing', ['identifies key risks', 'shows margin of safety', 'improves confidence of lenders'],
            ['takes time and expertise', 'does not reduce risk itself', 'still based on estimates'])],
      anl=[('Analyse the qualitative factors {b} should consider before investing in {newprod}.', ['qualitative factors are non-numerical influences', 'fit with corporate objectives and brand image', 'impact on staff morale and skills', 'environmental and ethical effects on stakeholders']),
           ('Analyse the risks {b} faces when making a large investment in new capacity.', ['risk = actual results differ from forecasts', 'demand for {prod} may be lower than forecast', 'costs and interest rates may rise', 'technology or competitors may change'])],
      ev=[('Evaluate whether {b} should go ahead with an investment that has a positive NPV but strong opposition from its employees.', ['positive NPV adds value', 'strategic advantage', 'competitiveness'],
           ['resistance could lower productivity', 'reputation and morale damage', 'forecasts may be optimistic'],
           ['the size of the NPV', 'whether staff can be consulted and involved', 'the strategic importance of the project']),
          ('Discuss the extent to which risk can be managed in investment decisions made by {b}.', ['sensitivity analysis', 'use of several appraisal methods', 'contingency plans'],
           ['the future is uncertain', 'external shocks', 'optimism bias in forecasts'],
           ['the length and size of the project', 'the quality of market research', 'the volatility of its market'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def sens_calc(r, D):
    c = r.choice(CASES)
    while True:
        I, cfs = _project(r, 4)
        rate = r.choice([8, 10, 12])
        npv, pv, dfs = _npv(I, cfs, rate)
        if npv > 0.05 * I:
            break
    cut = r.choice([10, 15, 20, 25])
    npv2 = sum(pv) * (1 - cut / 100) - I
    if D == 1:
        opts, ans = mc_num(r, sum(pv) * (1 - cut / 100), [sum(pv), sum(pv) * cut / 100, sum(pv) - cut], lambda x: money(x))
        return {'stem': f'The total present value of a project\'s cash inflows is {money(sum(pv))}. What is the total present value if every inflow is {cut}% lower?', 'options': opts, 'answer': ans,
                'key': f'{money(sum(pv))} × {1 - cut / 100:.2f} = {money(sum(pv) * (1 - cut / 100))}.', 'marks': 1}
    flows = ', '.join(money(x) for x in cfs)
    facs = ', '.join(f'{d:.3f}' for d in dfs)
    stem = f'{c["full"]} is considering a project costing {money(I)} with forecast net inflows in years 1–4 of {flows}. Discount factors at {rate}% are {facs}. Calculate the NPV, and the NPV if all cash inflows are {cut}% lower than forecast'
    key = f'PV of inflows = {money(sum(pv))}; NPV = {money(npv)} [2]; with inflows −{cut}%: PV = {money(sum(pv) * (1 - cut / 100))}, NPV = {money(npv2)} [1]'
    m = 3
    if D >= 4:
        be = (1 - I / sum(pv)) * 100
        stem += '. Calculate the percentage fall in inflows at which NPV becomes zero'
        key += f'; break-even fall = (1 − {money(I)}/{money(sum(pv))}) × 100 = {pct(be)} [1]'
        m = 4
    if D >= 5:
        stem += ', and evaluate how risky the project is'
        key += '; judgement on margin of safety compared with likely forecast errors; plus qualitative factors [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'NPV {money(npv)}; {money(npv2)} with {cut}% lower inflows', 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 14 Costing methods and decision-making
# =====================================================================================

t = T(14, 'Full costing and contribution costing', ['full costing and contribution costing', 'full costing', 'contribution costing', 'absorption'],
      defs=[('full costing', 'A costing method in which all indirect costs (overheads) are allocated to products or cost centres, so each product bears a share of total costs.'),
            ('contribution costing', 'A costing method that charges only variable (direct) costs to products; the contribution each product makes towards fixed costs and profit is calculated.'),
            ('contribution', 'Revenue minus variable costs; the amount available to pay fixed costs and provide profit.'),
            ('cost centre', 'A section of a business, such as a department or product line, to which costs can be allocated.'),
            ('indirect costs (overheads)', 'Costs that cannot be traced directly to a particular product or cost centre, such as rent, insurance and management salaries.')],
      mcqs=[('Under full costing, overheads are allocated to products', 'on a chosen basis such as floor space or labour hours', ['only to the most profitable product', 'never', 'according to their selling price only'],
             'Full costing apportions indirect costs using an allocation basis.'),
            ('A product has a selling price of $20 and variable cost of $12. Its contribution per unit is', '$8', ['$32', '$12', '$20'],
             'Contribution = price − variable cost = 20 − 12.'),
            ('Why can full costing lead to wrong decisions about dropping a product?', 'The allocation of fixed overheads is arbitrary and these costs remain if the product is dropped', ['Full costing ignores variable costs', 'Full costing does not include overheads', 'It always overstates contribution'],
             'Fixed overheads do not disappear when a product is dropped.')],
      exps=[('Explain why a product that makes a loss under full costing may still be worth keeping.', 'If it has a positive contribution, it covers its variable costs and helps pay fixed costs, which would still have to be paid if it were dropped.', '1 mark positive contribution; 1 mark fixed costs remain. [2]'),
            ('Explain one advantage and one disadvantage of full costing.', 'Advantage: all costs are covered, useful for setting prices. Disadvantage: overhead allocation is arbitrary and may distort product profitability.', '1 mark each with explanation. [2]'),
            ('Explain why contribution costing is useful for short-term decisions.', 'It separates fixed and variable costs, showing how profit changes when output, prices or product mix change, without arbitrary overhead allocation.', '1 mark separates variable/fixed; 1 mark decision use. [2]')],
      adv=[('using contribution costing rather than full costing for product decisions', ['avoids arbitrary overhead allocation', 'shows each product\'s contribution to fixed costs', 'useful for special orders and product mix'],
            ['fixed costs may be ignored in pricing', 'long-run prices must cover all costs', 'variable/fixed split may be unclear'])],
      anl=[('Analyse how {b} could use contribution costing to decide which product lines to keep.', ['contribution = revenue − variable costs', 'products with positive contribution help cover fixed costs', 'dropping such products would reduce total profit', 'consider spare capacity and links between products']),
           ('Analyse why the way {b} allocates overheads could affect its pricing decisions.', ['full costing allocates overheads to products', 'different bases (floor space, labour hours) give different costs', 'over-costed products may be priced too high', 'under-costed products may seem more profitable than they are'])],
      ev=[('Evaluate whether {b} should stop producing a product that shows a loss under full costing.', ['loss-making on full cost', 'resources could go to more profitable lines', 'simpler range'],
           ['positive contribution helps pay fixed costs', 'complementary sales may be lost', 'fixed costs remain after closure'],
           ['the contribution of the product', 'alternative uses of capacity', 'effect on customers and brand']),
          ('Discuss whether full costing or contribution costing is more useful to the managers of {b}.', ['full costing ensures all costs covered', 'useful for pricing', 'simple to understand'],
           ['contribution costing better for short-term decisions', 'arbitrary allocation', 'risk of wrong decisions'],
           ['the type of decision', 'its cost structure', 'how overheads are allocated'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def fullcost_calc(r, D):
    c = r.choice(CASES)
    names = ['Product X', 'Product Y', 'Product Z']
    q = [r.choice([2000, 4000, 5000, 8000]) for _ in range(3)]
    p = [r.choice([20, 25, 30, 40]) for _ in range(3)]
    v = [round(pi * r.choice([0.5, 0.6, 0.7, 0.8])) for pi in p]
    fs = r.choice([(50, 30, 20), (40, 40, 20), (30, 30, 40), (60, 25, 15)])
    OH = r.choice([60000, 80000, 100000, 120000])
    contrib = [(pi - vi) * qi for pi, vi, qi in zip(p, v, q)]
    alloc = [OH * f / 100 for f in fs]
    prof = [ci - ai for ci, ai in zip(contrib, alloc)]
    if D == 1:
        opts, ans = mc_num(r, contrib[0], [p[0] * q[0], v[0] * q[0], (p[0] - v[0])], lambda x: money(x))
        return {'stem': f'{names[0]} sells {q[0]:,} units at ${p[0]} with a variable cost of ${v[0]} per unit. What is its total contribution?', 'options': opts, 'answer': ans,
                'key': f'({p[0]} − {v[0]}) × {q[0]:,} = {money(contrib[0])}.', 'marks': 1}
    tbl = '; '.join(f'{n}: {qi:,} units at ${pi}, variable cost ${vi} per unit, floor space {f}%' for n, qi, pi, vi, f in zip(names, q, p, v, fs))
    stem = f'{c["full"]} makes three products — {tbl}. Fixed overheads of {money(OH)} are allocated by floor space. Calculate the total contribution of each product'
    key = '; '.join(f'{n}: ({pi} − {vi}) × {qi:,} = {money(ci)}' for n, pi, vi, qi, ci in zip(names, p, v, q, contrib)) + ' [2]'
    m = 2
    if D >= 3:
        stem += ' and the profit or loss of each product under full costing'
        key += '; allocated overheads ' + ', '.join(money(a) for a in alloc) + '; profit/loss ' + ', '.join(money(x) for x in prof) + ' [2]'
        m = 4
    if D >= 4:
        worst = min(range(3), key=lambda i: prof[i])
        stem += f'. Advise whether {names[worst]} should be discontinued'
        key += f'; {names[worst]} contribution {money(contrib[worst])} is {"positive, so dropping it reduces total profit by this amount because its overheads remain" if contrib[worst] > 0 else "negative, so dropping it increases total profit"}; also consider complementary sales and alternative use of space [2]'
        m = 6
    return {'stem': stem + '.', 'answer': 'Contributions ' + ', '.join(money(x) for x in contrib) + ('; full-cost profit ' + ', '.join(money(x) for x in prof) if D >= 3 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(14, 'Special order decisions', ['special order decisions and contribution', 'special order', 'contribution decisions'],
      defs=[('special order', 'A one-off order from a customer, often at a lower price than normal, which the business must decide whether to accept.'),
            ('spare capacity', 'The difference between the maximum output a business can produce and its current output.'),
            ('marginal cost', 'The extra cost of producing one more unit of output, usually equal to the variable cost per unit.'),
            ('opportunity cost', 'The benefit of the next best alternative that is given up when a decision is made.')],
      mcqs=[('A firm with spare capacity should accept a special order (on financial grounds) if', 'the price per unit is above the variable cost per unit', ['the price is above full cost per unit', 'the order is from a new customer', 'the price equals the normal price'],
             'Fixed costs are already covered; any positive contribution adds to profit.'),
            ('If a firm is at full capacity, accepting a special order means', 'it must consider the contribution lost from normal sales displaced', ['fixed costs fall', 'there is no opportunity cost', 'variable cost per unit falls to zero'],
             'Lost contribution is an opportunity cost.'),
            ('Which is a non-financial risk of accepting a low-price special order?', 'Existing customers may demand the same low price', ['Contribution will be negative', 'Fixed costs will rise', 'Spare capacity will increase'],
             'Price discrimination may become known to regular customers.')],
      exps=[('Explain why a business might accept a special order at a price below full cost.', 'With spare capacity, fixed costs are already paid, so any price above variable cost gives extra contribution and increases profit.', '1 mark fixed costs already covered; 1 mark positive contribution. [2]'),
            ('Explain two non-financial factors to consider when deciding whether to accept a special order.', 'Reaction of existing customers to a lower price; possibility of future orders; effect on brand image; pressure on staff and capacity.', '2 × (1 mark factor, 1 mark explanation). [4]'),
            ('Explain why the opportunity cost of a special order is zero only when there is spare capacity.', 'With spare capacity nothing else is given up; at full capacity normal sales must be lost, so their contribution is the opportunity cost.', '1 mark spare capacity; 1 mark displaced sales. [2]')],
      adv=[('accepting a large special order at a discounted price', ['extra contribution and profit', 'uses spare capacity', 'possible repeat business and new market'],
            ['regular customers may want the same price', 'may displace more profitable work', 'risk to brand image'])],
      anl=[('Analyse the factors {b} should consider before accepting a special order from a new overseas customer.', ['contribution: price compared with variable cost', 'spare capacity and opportunity cost', 'reaction of existing customers', 'future business and payment risk']),
           ('Analyse why {b} might reject a special order that offers a positive contribution.', ['positive contribution adds profit only if capacity is spare', 'displaced regular sales may be more profitable', 'damage to price perception and brand', 'stress on staff and quality'])],
      ev=[('Evaluate whether {b} should accept a special order at a price 20% below its normal price.', ['positive contribution', 'uses spare capacity', 'potential long-term customer'],
           ['existing customers may demand discounts', 'capacity may be needed for regular sales', 'quality and delivery risks'],
           ['the amount of spare capacity', 'whether the markets can be kept separate', 'the strategic value of the customer']),
          ('Discuss whether contribution analysis alone should decide whether {b} accepts special orders.', ['clear financial result', 'easy to calculate', 'shows short-term profit effect'],
           ['ignores customer reactions and brand', 'ignores long-term relationships', 'assumes costs are accurate'],
           ['its capacity position', 'its pricing strategy', 'qualitative factors'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def special_calc(r, D):
    c = r.choice(CASES)
    p = r.choice([20, 25, 30, 40, 50])
    vc = round(p * r.choice([0.5, 0.55, 0.6, 0.65]))
    fc_u = round(p * r.choice([0.15, 0.2, 0.25]))
    op = round((vc + fc_u) * r.choice([0.85, 0.9, 0.95, 1.05, 1.1]), 2)
    qo = r.choice([2000, 3000, 5000, 8000])
    cap = r.choice([20000, 25000, 30000])
    cur = cap - qo + r.choice([-2000, 0, 1000, 2000]) if D >= 4 else cap - qo - r.choice([1000, 2000, 4000])
    spare = cap - cur
    cont = (op - vc) * qo
    if D == 1:
        opts, ans = mc_num(r, cont, [op * qo, (op - vc - fc_u) * qo, (p - vc) * qo], lambda x: money(x))
        return {'stem': f'A business with spare capacity is offered an order for {qo:,} units at {money(op, 2)} each. Variable cost is ${vc} per unit. What contribution would the order earn?', 'options': opts, 'answer': ans,
                'key': f'({money(op, 2)} − ${vc}) × {qo:,} = {money(cont)}.', 'marks': 1}
    stem = (f'{c["full"]} normally sells at ${p} per unit. Variable cost is ${vc} per unit and fixed cost per unit at current output is ${fc_u}. It has a capacity of {cap:,} units and currently produces {cur:,}. '
            f'A customer offers to buy {qo:,} units at {money(op, 2)} each. Calculate the contribution from the order')
    key = f'Contribution per unit = {money(op, 2)} − ${vc} = {money(op - vc, 2)}; total = {money(cont)} [2]'
    m = 2
    if D >= 3:
        stem += ' and explain why the order is acceptable even though the price is ' + ('below' if op < vc + fc_u else 'close to') + f' full cost (${vc + fc_u})'
        key += '; fixed costs are already covered by existing output, so extra contribution adds to profit [1]'
        m = 3
    if D >= 4:
        lost = max(0, qo - spare)
        stem += '. Taking account of the capacity limit, calculate the change in profit if the order is accepted'
        if lost:
            key += f'; spare capacity only {spare:,}, so {lost:,} normal sales lost at contribution ${p - vc}: lost = {money(lost * (p - vc))}; net change = {money(cont - lost * (p - vc))} [2]'
            net = cont - lost * (p - vc)
        else:
            key += f'; spare capacity {spare:,} ≥ {qo:,}, so profit rises by {money(cont)} [2]'
            net = cont
        m = 5
        if D >= 5:
            stem += ', and recommend whether to accept it'
            key += '; recommendation using net result plus customer reaction, future orders, brand [1]'
            m = 6
    return {'stem': stem + '.', 'answer': f'Contribution {money(cont)}' + (f'; profit change {money(net)}' if D >= 4 else ''), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


t = T(14, 'Budgets and variance analysis', ['budgets and variance analysis', 'budgets', 'variance analysis', 'variances'],
      defs=[('budget', 'A detailed financial plan for a future period, setting targets for revenue, costs or other items, agreed in advance.'),
            ('variance', 'The difference between a budgeted figure and the actual result.'),
            ('favourable variance', 'A variance that increases profit compared with the budget, e.g. actual revenue above budget or actual costs below budget.'),
            ('adverse variance', 'A variance that reduces profit compared with the budget, e.g. actual costs above budget or actual revenue below budget.'),
            ('zero budgeting', 'Setting each budget at zero at the start of each period, so that every item of spending must be justified afresh.'),
            ('flexible budget', 'A budget that is adjusted to the actual level of output, so that costs can be compared fairly with actual results.')],
      mcqs=[('Actual material costs were $52 000 against a budget of $48 000. The variance is', '$4 000 adverse', ['$4 000 favourable', '$100 000 adverse', '$48 000 favourable'],
             'Costs above budget reduce profit: adverse.'),
            ('Why might a favourable cost variance be a cause for concern?', 'It may result from using cheaper, lower-quality materials', ['It always means higher profit', 'It shows costs were above budget', 'It means sales fell'],
             'Saving costs by cutting quality can harm sales and reputation.'),
            ('Which is a benefit of involving managers in setting their own budgets?', 'They are more motivated to achieve targets they helped to set', ['Budgets become less accurate', 'Variances cannot occur', 'Senior managers lose all control'],
             'Participation increases ownership and motivation.')],
      exps=[('Explain two benefits of using budgets.', 'They set targets that guide and motivate managers; they help coordinate departments and control spending through variance analysis.', '2 × (1 mark benefit, 1 mark explanation). [4]'),
            ('Explain why a flexible budget gives a better basis for variance analysis than a fixed budget.', 'If output differs from plan, a fixed budget\'s costs are not comparable; flexing to actual output shows whether costs were controlled efficiently.', '1 mark output differences; 1 mark fair comparison. [2]'),
            ('Explain one advantage and one disadvantage of zero budgeting.', 'Advantage: every item is justified, reducing waste. Disadvantage: very time-consuming and may create conflict between managers.', '1 mark each with explanation. [2]')],
      adv=[('introducing zero budgeting', ['every item of spending is justified', 'removes waste and outdated spending', 'resources move to priority areas'],
            ['very time-consuming', 'managers may exaggerate needs', 'conflict between departments'])],
      anl=[('Analyse how {b} could use variance analysis to improve its performance.', ['variance = budget − actual', 'identifies areas of over- and under-spending', 'investigates causes such as prices, efficiency or demand', 'allows corrective action and better future budgets']),
           ('Analyse the possible causes of an adverse sales revenue variance at {b}.', ['adverse revenue variance means revenue below budget', 'lower sales volume because of competition or economy', 'lower prices or discounts', 'unrealistic budget in the first place'])],
      ev=[('Evaluate the usefulness of budgeting to the managers of {b}.', ['planning and coordination', 'control through variances', 'motivation through targets'],
           ['time-consuming', 'may be inflexible when conditions change', 'targets may demotivate if unrealistic'],
           ['how budgets are set (participation)', 'how often they are reviewed', 'the stability of its market']),
          ('Discuss whether {b} should change from incremental budgeting to zero budgeting.', ['removes waste', 'justifies all spending', 'aligns spending with priorities'],
           ['time and cost of preparation', 'managerial conflict', 'incremental is simpler and stable'],
           ['the size of the organisation', 'how much waste exists now', 'management skills'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def var_calc(r, D):
    c = r.choice(CASES)
    items = [('sales revenue', r.choice([400, 500, 600, 800]) * 1000, True), ('direct materials', r.choice([120, 150, 180]) * 1000, False),
             ('direct labour', r.choice([100, 120, 140]) * 1000, False), ('overheads', r.choice([60, 80, 90]) * 1000, False)]
    acts = [round(b * r.choice([0.9, 0.94, 0.96, 1.04, 1.06, 1.1]) / 1000) * 1000 for _, b, _ in items]
    def var(b, a, rev):
        d = (a - b) if rev else (b - a)
        return d, 'F' if d > 0 else ('A' if d < 0 else '—')
    if D == 1:
        n, b, rev = items[1]; a = acts[1]
        d, fa = var(b, a, rev)
        lab = f'{money(abs(d))} {"favourable" if fa == "F" else "adverse"}'
        wrong = f'{money(abs(d))} {"adverse" if fa == "F" else "favourable"}'
        opts, ans = mcq(r, lab, [wrong, f'{money(abs(d) * 2)} {"favourable" if fa == "F" else "adverse"}', f'{money(a)} {"favourable" if fa == "F" else "adverse"}', f'{money(b)} adverse'])
        return {'stem': f'Budgeted {n} were {money(b)}; actual {n} were {money(a)}. What is the variance?', 'options': opts, 'answer': ans,
                'key': f'{money(b)} − {money(a)}: cost {"below" if fa == "F" else "above"} budget, so {lab}.', 'marks': 1}
    tbl = '; '.join(f'{n}: budget {money(b)}, actual {money(a)}' for (n, b, _), a in zip(items, acts))
    stem = f'Budget and actual figures for {c["full"]} last quarter — {tbl}. Calculate the variance for each item, stating whether it is favourable or adverse'
    vs = [var(b, a, rev) for (_, b, rev), a in zip(items, acts)]
    key = '; '.join(f'{n}: {money(abs(d))} {fa}' for (n, _, _), (d, fa) in zip(items, vs)) + ' [2]'
    m = 2
    bp = items[0][1] - sum(b for _, b, _ in items[1:])
    ap = acts[0] - sum(acts[1:])
    if D >= 3:
        stem += ' and the profit variance'
        key += f'; budgeted profit {money(bp)}, actual {money(ap)}, profit variance {money(abs(ap - bp))} {"F" if ap > bp else "A"} [1]'
        m = 3
    if D >= 4:
        stem += '. Suggest one possible cause of the largest adverse variance'
        adv_ = [(abs(d), n) for (n, _, _), (d, fa) in zip(items, vs) if fa == 'A']
        nm = max(adv_)[1] if adv_ else 'none'
        key += f'; largest adverse: {nm} — e.g. higher prices/wage rates, inefficiency, lower demand or prices, unrealistic budget [1]'
        m = 4
    if D >= 5:
        stem += ' and explain why the variances should be interpreted with care'
        key += '; fixed v flexible budget, output changes, interdependence (e.g. cheaper materials → more waste), external factors [1]'
        m = 5
    return {'stem': stem + '.', 'answer': '; '.join(f'{n} {money(abs(d))} {fa}' for (n, _, _), (d, fa) in zip(items, vs)) + (f'; profit {money(abs(ap - bp))} {"F" if ap > bp else "A"}' if D >= 3 else ''),
            'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 15 Strategic management and strategic analysis
# =====================================================================================

t = T(15, 'Corporate strategy, tactics and competitive advantage', ['corporate strategy, tactics and competitive advantage', 'corporate strategy', 'tactics', 'competitive advantage'],
      defs=[('corporate strategy', 'A long-term plan of action for the whole organisation, designed to achieve its corporate objectives, e.g. which markets to compete in and how to grow.'),
            ('tactics', 'Short-term, often departmental, decisions and actions taken to put a strategy into effect.'),
            ('competitive advantage', 'A feature or capability that allows a business to outperform its rivals, by offering better value through lower prices or greater benefits.'),
            ('strategic management', 'The process of analysing the business and its environment, choosing a strategy and implementing and reviewing it to achieve long-term objectives.')],
      mcqs=[('Which is an example of a strategic decision rather than a tactical one?', 'Entering a new overseas market', ['Changing the price of one product for a weekend', 'Rearranging staff rotas', 'Ordering more stationery'],
             'Strategic decisions are long-term, high-risk and affect the whole business.'),
            ('The three stages of strategic management are', 'strategic analysis, strategic choice and strategic implementation', ['planning, pricing and promotion', 'recruitment, training and appraisal', 'input, process and output'],
             'Analysis → choice → implementation (and review).'),
            ('A sustainable competitive advantage is one that', 'rivals find difficult to copy for a long time', ['lasts only until next quarter', 'is based only on a temporary price cut', 'every competitor already has'],
             'Sustainability comes from unique resources, patents, brands or culture.')],
      exps=[('Explain the difference between strategy and tactics.', 'Strategy is the long-term plan to achieve corporate objectives, made by senior managers; tactics are short-term actions, often by middle managers, to carry out the strategy.', '1 mark each. [2]'),
            ('Explain why a competitive advantage based on low prices may not last.', 'Competitors can cut prices too, starting a price war; only a genuine cost advantage (e.g. economies of scale) can sustain low prices profitably.', '1 mark rivals copy; 1 mark need for cost advantage. [2]'),
            ('Explain why strategic decisions are usually made by senior managers.', 'They commit large resources, are long-term, hard to reverse and affect the whole organisation, so they need the overview and authority of senior management.', '1 mark characteristics; 1 mark link to senior managers. [2]')],
      adv=[('developing a formal long-term corporate strategy', ['clear direction and coordination', 'resources focused on objectives', 'easier to monitor progress'],
            ['time-consuming to prepare', 'can become inflexible', 'depends on accurate analysis of the future'])],
      anl=[('Analyse how {b} could build a sustainable competitive advantage.', ['competitive advantage allows the firm to outperform rivals', 'cost leadership through scale or efficiency', 'differentiation through brand, quality or innovation of {prod}', 'core competencies that rivals cannot copy']),
           ('Analyse why {b} needs both a clear strategy and effective tactics.', ['strategy sets long-term direction', 'tactics turn strategy into action', 'poor tactics can undermine a good strategy', 'tactics must be coordinated across departments'])],
      ev=[('Evaluate the most important source of competitive advantage for {b}.', ['low costs', 'brand and reputation', 'innovation and core competencies'],
           ['costs can be matched by rivals', 'brands take time and money', 'innovation can be copied'],
           ['the nature of its market', 'its resources and capabilities', 'what customers value most']),
          ('Discuss whether {b} should spend more time on strategic planning given how quickly its market is changing.', ['direction and coordination', 'anticipates threats', 'allocates resources'],
           ['plans become out of date', 'emergent strategy may be better', 'cost of planning'],
           ['the speed of change', 'the quality of information', 'the flexibility of the plan'])])


SWOT_ITEMS = [('a highly skilled and loyal workforce', 'Strength', 'internal, positive'), ('a well-known brand with loyal customers', 'Strength', 'internal, positive'),
              ('patents on its key technology', 'Strength', 'internal, positive'), ('low gearing and large cash reserves', 'Strength', 'internal, positive'),
              ('old and inefficient machinery', 'Weakness', 'internal, negative'), ('high labour turnover among managers', 'Weakness', 'internal, negative'),
              ('dependence on one main customer', 'Weakness', 'internal, negative'), ('a poor online presence', 'Weakness', 'internal, negative'),
              ('rising incomes in a neighbouring country', 'Opportunity', 'external, positive'), ('a government subsidy for green investment', 'Opportunity', 'external, positive'),
              ('the closure of a major competitor', 'Opportunity', 'external, positive'), ('a new trade agreement removing tariffs on its exports', 'Opportunity', 'external, positive'),
              ('a new low-cost rival entering the market', 'Threat', 'external, negative'), ('stricter environmental regulations', 'Threat', 'external, negative'),
              ('a forecast recession', 'Threat', 'external, negative'), ('a sharp rise in the price of key raw materials', 'Threat', 'external, negative')]
PESTLE_ITEMS = [('a change of government promising higher business taxes', 'Political'), ('a rise in interest rates', 'Economic'), ('an ageing population', 'Social'),
                ('rapid growth of artificial intelligence', 'Technological'), ('a new consumer protection law', 'Legal'), ('more frequent droughts and floods', 'Environmental'),
                ('a fall in unemployment', 'Economic'), ('growing consumer concern about healthy eating', 'Social'), ('political instability in a key export market', 'Political'),
                ('the spread of 5G mobile networks', 'Technological'), ('a ban on single-use plastic packaging', 'Environmental'), ('a higher legal minimum wage', 'Legal')]

t = T(15, 'SWOT and PESTLE analysis', ['swot and pestle analysis', 'swot', 'pestle', 'pest analysis'],
      defs=[('SWOT analysis', 'A strategic analysis tool that identifies a business\'s internal strengths and weaknesses and the external opportunities and threats it faces.'),
            ('PESTLE analysis', 'An analysis of the political, economic, social, technological, legal and environmental factors in a business\'s external environment.'),
            ('strategic analysis', 'The first stage of strategic management: researching and analysing the business and its environment to understand its current position.'),
            ('external environment', 'Factors outside the control of the business, such as the economy, competitors, laws and technology, that affect its performance.')],
      mcqs=[('In SWOT analysis, which elements are internal to the business?', 'Strengths and weaknesses', ['Opportunities and threats', 'Strengths and opportunities', 'Weaknesses and threats'],
             'S and W are internal; O and T are external.'),
            ('PESTLE analysis is mainly used to identify', 'opportunities and threats in the external environment', ['the strengths of the workforce', 'internal weaknesses', 'the critical path of a project'],
             'PESTLE examines external influences, which feed into O and T of SWOT.'),
            ('Which is a limitation of SWOT analysis?', 'It is a snapshot that quickly becomes out of date and may be subjective', ['It considers only external factors', 'It always provides a clear strategy', 'It requires complex calculations'],
             'SWOT lists factors but does not rank them or choose a strategy.')],
      exps=[('Explain how a business can use the results of a SWOT analysis to develop a strategy.', 'It can use strengths to exploit opportunities, address weaknesses that limit it, and plan to counter threats, e.g. by matching a strong brand to a growing market.', '1 mark matching S to O; 1 mark addressing W/T. [2]'),
            ('Explain why PESTLE analysis is important for a business planning to enter a new country.', 'Political stability, economic conditions, culture, technology, laws and environment differ by country and determine the risks and opportunities of entry.', '1 mark external factors differ; 1 mark effect on risk/opportunity. [2]'),
            ('Explain two limitations of PESTLE analysis.', 'Factors change quickly so analysis dates; it may be subjective; it can produce long lists without showing which factors matter most.', '2 × (1 mark limitation, 1 mark explanation). [4]')],
      adv=[('carrying out a regular SWOT analysis', ['structured review of position', 'matches strengths to opportunities', 'identifies risks early'],
            ['subjective', 'quickly out of date', 'does not rank factors or give a strategy'])],
      anl=[('Analyse two external threats that a PESTLE analysis might identify for {b}.', ['PESTLE examines external factors', 'economic: recession or rising interest rates reduce demand for {prod}', 'legal/environmental: stricter regulation raises costs', 'technological: new technology could make products obsolete']),
           ('Analyse how {b} could use a SWOT analysis to decide whether to launch {newprod}.', ['SWOT identifies internal and external factors', 'strengths such as brand or skills support the launch', 'weaknesses such as limited finance increase risk', 'opportunities and threats in the target market'])],
      ev=[('Evaluate the usefulness of SWOT analysis to {b} when planning its future strategy.', ['structured overview', 'links internal capabilities to the environment', 'simple and cheap'],
           ['subjective and static', 'does not prioritise', 'needs other tools such as Porter or Ansoff'],
           ['the quality of the information used', 'how often it is updated', 'whether it leads to action']),
          ('Discuss which PESTLE factor is likely to have the greatest impact on {b} over the next five years.', ['economic factors affect demand and costs', 'technological change can transform the industry', 'environmental and legal pressures are growing'],
           ['impact depends on the sector', 'factors interact', 'some are unpredictable'],
           ['the nature of {bp} {prod}', 'its markets', 'how quickly it can adapt'])])


@t.add('C1', (1, 2, 3), 'mcq')
def swot_class(r, D):
    c = r.choice(CASES)
    if r.random() < 0.5:
        f, cat, why = r.choice(SWOT_ITEMS)
        opts, ans = mcq(r, cat, ['Strength', 'Weakness', 'Opportunity', 'Threat'])
        return {'stem': f'In a SWOT analysis for {c["b"]}, under which heading should "{f}" be placed?', 'options': opts, 'answer': ans, 'key': f'{cat}: it is {why}.', 'marks': 1}
    f, cat = r.choice(PESTLE_ITEMS)
    opts, ans = mcq(r, cat, [x for x in ['Political', 'Economic', 'Social', 'Technological', 'Legal', 'Environmental'] if x != cat])
    return {'stem': f'{c["full"]} is carrying out a PESTLE analysis. Under which heading should "{f}" be listed?', 'options': opts, 'answer': ans, 'key': f'{cat} factor.', 'marks': 1}


@t.add('C3', (1, 2, 3), 'case')
def swot_sort(r, D):
    c = r.choice(CASES)
    k = 4 if D <= 2 else 6
    items = r.sample(SWOT_ITEMS, k)
    stem = f'{intro(r, c)} A consultant lists these factors for {c["b"]}: ' + '; '.join(f'({i + 1}) {f}' for i, (f, _, _) in enumerate(items)) + '. Classify each factor in a SWOT analysis' + (' and explain which one should be the top priority for managers.' if D >= 3 else '.')
    ans = '; '.join(f'({i + 1}) {cat}' for i, (_, cat, _) in enumerate(items))
    m = k // 2 + (2 if D >= 3 else 0)
    key = f'{ans} — ½ mark each, rounded [{k // 2}]' + ('; priority justified by impact and urgency for ' + c['b'] + ' [2]' if D >= 3 else '') + f'. [{m}]'
    return {'stem': stem, 'answer': ans, 'key': key, 'marks': m, 'type': 'case'}


FORCES = [('Many new firms are setting up because start-up costs are low.', 'Threat of new entrants'), ('Customers can easily switch to a rival online.', 'Bargaining power of buyers'),
          ('Only two firms in the world supply a key component.', 'Bargaining power of suppliers'), ('Consumers are switching to a different type of product that meets the same need.', 'Threat of substitutes'),
          ('Six similar-sized firms compete fiercely on price.', 'Rivalry among existing competitors'), ('A large supermarket chain buys 60% of the firm\'s output.', 'Bargaining power of buyers'),
          ('Patents and high capital costs make it hard for new firms to enter.', 'Threat of new entrants'), ('Streaming services are reducing demand for cinema tickets.', 'Threat of substitutes'),
          ('Skilled workers are scarce, so the specialist recruitment agency can set high fees.', 'Bargaining power of suppliers'), ('Market growth has slowed and firms have spare capacity.', 'Rivalry among existing competitors')]

t = T(15, "Porter's five forces and core competencies", ["porter's five forces and core competencies", 'five forces', 'core competencies'],
      defs=[("Porter's five forces", 'A model for analysing the competitive environment of an industry using five forces: threat of new entrants, power of buyers, power of suppliers, threat of substitutes and competitive rivalry.'),
            ('core competence', 'A unique combination of skills, knowledge and technology that gives a business a competitive advantage, can be applied to many markets and is hard to copy (Prahalad and Hamel).'),
            ('barriers to entry', 'Factors that make it difficult for new firms to enter a market, such as high capital costs, patents, strong brands and economies of scale.'),
            ('buyer power', 'The ability of customers to put pressure on a firm to cut prices or improve quality, greater when buyers are few or can switch easily.')],
      mcqs=[('According to Porter, an industry is likely to be most profitable when', 'barriers to entry are high and buyer power is low', ['there are many close substitutes', 'suppliers are few and powerful', 'rivalry is intense'],
             'Weak forces allow firms to earn higher profits.'),
            ('Which is the best example of a core competence?', 'A unique ability to miniaturise electronics, used across many products', ['Having a large car park', 'Paying the minimum wage', 'Owning a delivery van'],
             'Core competencies are distinctive, transferable and hard to copy.'),
            ('Which factor increases the bargaining power of suppliers?', 'There are few suppliers and switching is costly', ['There are many suppliers', 'The buyer can easily make the input itself', 'The input is standard and widely available'],
             'Concentrated suppliers with unique inputs have power.')],
      exps=[('Explain how high barriers to entry benefit existing firms in a market.', 'Fewer new rivals can enter, so competition is limited and existing firms can keep higher prices and profits.', '1 mark fewer entrants; 1 mark higher prices/profits. [2]'),
            ('Explain why core competencies can give a sustainable competitive advantage.', 'They are hard for rivals to copy because they combine skills, knowledge and culture built up over time, and they can be used to enter several markets.', '1 mark hard to copy; 1 mark applicable across markets/value to customers. [2]'),
            ('Explain one limitation of Porter\'s five forces model.', 'It gives a static snapshot of an industry; it ignores government, complementary products and collaboration, and industries can change quickly.', '1 mark limitation; 1 mark explanation. [2]')],
      adv=[('focusing on its core competencies and outsourcing other activities', ['resources concentrated on what it does best', 'lower costs through specialist suppliers', 'stronger competitive advantage'],
            ['dependence on outside suppliers', 'loss of skills in outsourced areas', 'competencies may become outdated'])],
      anl=[("Analyse how Porter's five forces could help {b} understand the competitive pressures in its industry.", ['five forces analyse industry competition', 'buyer and supplier power affect prices and margins', 'threat of entrants and substitutes limits pricing', 'rivalry determines intensity of competition']),
           ('Analyse how {b} could use its core competencies to grow.', ['core competencies are unique, hard-to-copy capabilities', 'apply them to new products such as {newprod}', 'enter new markets using existing strengths', 'reduce risk compared with unrelated diversification'])],
      ev=[("Evaluate the usefulness of Porter's five forces model to {b} when deciding whether to enter a new market.", ['identifies competitive pressures', 'shows likely profitability', 'highlights barriers'],
           ['static snapshot', 'difficult to measure forces', 'ignores the firm\'s own competencies'],
           ['how quickly the market is changing', 'the quality of information', 'use with SWOT and Ansoff']),
          ('Discuss whether {b} should build its strategy around its core competencies.', ['sustainable advantage', 'basis for related growth', 'efficient use of resources'],
           ['competencies may become obsolete', 'may limit vision', 'hard to identify objectively'],
           ['the pace of technological change', 'how unique its competencies are', 'market opportunities'])])


@t.add('C1', (1, 2, 3), 'mcq')
def force_class(r, D):
    s, f = r.choice(FORCES)
    c = r.choice(CASES)
    opts, ans = mcq(r, f, [x for x in ['Threat of new entrants', 'Bargaining power of buyers', 'Bargaining power of suppliers', 'Threat of substitutes', 'Rivalry among existing competitors'] if x != f])
    return {'stem': f'In {c["bp"]} industry: "{s}" Which of Porter\'s five forces does this describe?', 'options': opts, 'answer': ans, 'key': f'{f}.', 'marks': 1}


t = T(15, 'Boston matrix and portfolio analysis', ['boston matrix and portfolio analysis', 'boston matrix', 'portfolio analysis', 'product portfolio'],
      defs=[('Boston matrix', 'A model that classifies a firm\'s products or business units by market growth rate and relative market share into stars, cash cows, question marks (problem children) and dogs.'),
            ('cash cow', 'A product with a high relative market share in a low-growth market, which generates more cash than it needs.'),
            ('question mark (problem child)', 'A product with a low market share in a high-growth market, which needs heavy investment and may or may not succeed.'),
            ('relative market share', 'A product\'s market share divided by the market share of its largest competitor.')],
      mcqs=[('In the Boston matrix, a product with high market share in a fast-growing market is a', 'star', ['cash cow', 'dog', 'question mark'],
             'Stars: high share, high growth.'),
            ('Cash from cash cows is often used to', 'finance question marks and stars', ['pay for dogs indefinitely', 'reduce the market share of stars', 'stop all new product development'],
             'Cash cows fund products with growth potential.'),
            ('Which is a limitation of the Boston matrix?', 'It assumes market share leads to profitability, which may not be true', ['It considers too many variables', 'It cannot be drawn', 'It only works for one product'],
             'High share does not always mean high profit; dogs can be profitable.')],
      exps=[('Explain how a business can use the Boston matrix to manage its product portfolio.', 'It shows the balance of products: cash cows generate funds that can be invested in stars and selected question marks, while weak dogs may be dropped.', '1 mark classification; 1 mark resource allocation decisions. [2]'),
            ('Explain why a business needs a balanced product portfolio.', 'Products at different stages generate and use cash differently; a balance ensures current cash flow and future growth and spreads risk.', '1 mark cash generation/use; 1 mark growth/risk. [2]'),
            ('Explain why a "dog" product might not be withdrawn.', 'It may still make a positive contribution, support sales of other products, or have loyal customers; withdrawal could also harm brand image.', '1 mark reason; 1 mark explanation. [2]')],
      adv=[('using the Boston matrix to plan its product portfolio', ['shows balance of products', 'guides investment of cash', 'identifies products to drop or develop'],
            ['oversimplifies with two variables', 'market definition is subjective', 'ignores links between products'])],
      anl=[('Analyse how {b} could use the Boston matrix to allocate its marketing budget.', ['Boston matrix classifies by growth and relative share', 'build question marks with potential', 'hold and milk cash cows', 'harvest or divest dogs']),
           ('Analyse the risks to {b} of having most of its sales from one cash cow product.', ['cash cows are in low-growth markets', 'decline could sharply reduce revenue', 'few stars to replace it', 'need to develop new products such as {newprod}'])],
      ev=[('Evaluate the usefulness of the Boston matrix to {b} in planning its product strategy.', ['simple visual tool', 'shows balance and cash needs', 'helps allocate resources'],
           ['only two variables', 'ignores profitability', 'snapshot that changes'],
           ['how markets are defined', 'availability of market data', 'use with product life cycle and Ansoff']),
          ('Discuss whether {b} should withdraw its products classified as dogs.', ['frees resources', 'simplifies range', 'focus on stars'],
           ['may still make positive contribution', 'support other products', 'loyal customers'],
           ['their contribution', 'links with other products', 'cost of withdrawal'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def boston_calc(r, D):
    c = r.choice(CASES)
    prods = []
    for nm in ('P1', 'P2', 'P3'):
        g = r.choice([2, 3, 4, 12, 15, 20])
        own = r.choice([8, 12, 20, 25, 30, 35])
        riv = r.choice([10, 15, 20, 30, 40])
        if riv == own:
            riv += 5
        prods.append((nm, g, own, riv))
    def cls(g, rms):
        hi = g >= 10
        return ('Star' if rms > 1 else 'Question mark') if hi else ('Cash cow' if rms > 1 else 'Dog')
    if D == 1:
        nm, g, own, riv = prods[0]
        rms = own / riv
        opts, ans = mcq(r, cls(g, rms), ['Star', 'Cash cow', 'Question mark', 'Dog'])
        return {'stem': f'A product has a market share of {own}% in a market growing at {g}% a year. Its largest rival has a {riv}% share. Using the Boston matrix (high growth = 10% or more), how is it classified?', 'options': opts, 'answer': ans,
                'key': f'Relative share = {own}/{riv} = {num(rms, 2)} ({"above" if rms > 1 else "below"} 1); growth {g}% is {"high" if g >= 10 else "low"} → {cls(g, rms)}.', 'marks': 1}
    tbl = '; '.join(f'{nm}: market growth {g}% a year, own share {own}%, largest rival {riv}%' for nm, g, own, riv in prods)
    stem = f'{c["full"]} has three product lines — {tbl}. Taking high growth as 10% or more, calculate the relative market share of each and classify it using the Boston matrix'
    key = '; '.join(f'{nm}: RMS {own}/{riv} = {num(own / riv, 2)} → {cls(g, own / riv)}' for nm, g, own, riv in prods) + ' [3]'
    m = 3
    if D >= 4:
        stem += ', and comment on the balance of the portfolio'
        key += '; balance: need cash cows to fund stars/question marks; risks if dominated by dogs or question marks [1]'
        m = 4
    if D >= 5:
        stem += ', recommending one action for the product with the weakest position'
        key += '; e.g. invest to build share, harvest, or divest, justified [1]'
        m = 5
    return {'stem': stem + '.', 'answer': '; '.join(f'{nm} {num(own / riv, 2)} {cls(g, own / riv)}' for nm, g, own, riv in prods), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}

# =====================================================================================
# 16 Strategic choice
# =====================================================================================

t = T(16, "Ansoff's matrix", ["ansoff's matrix", 'ansoff', 'market penetration', 'diversification'],
      defs=[("Ansoff's matrix", 'A model showing four growth strategies — market penetration, market development, product development and diversification — according to whether products and markets are existing or new, with risk increasing away from existing products and markets.'),
            ('market penetration', 'Increasing sales of existing products in existing markets, e.g. through promotion or price cuts.'),
            ('market development', 'Selling existing products in new markets, e.g. new countries or new customer segments.'),
            ('product development', 'Selling new or modified products in existing markets.'),
            ('diversification', 'Selling new products in new markets; the riskiest strategy in Ansoff\'s matrix.')],
      mcqs=[("According to Ansoff's matrix, which growth strategy usually carries the highest risk?", 'Diversification', ['Market penetration', 'Market development', 'Product development'],
             'New products in new markets: least knowledge and experience.'),
            ('A business starts selling its existing products in a new country. This is', 'market development', ['market penetration', 'product development', 'diversification'],
             'Existing product, new market.'),
            ('Which is a limitation of Ansoff\'s matrix?', 'It shows the risk of each option but does not tell managers which to choose', ['It ignores products', 'It ignores markets', 'It requires discounted cash flow'],
             'It is a framework for options, not a decision tool.')],
      exps=[('Explain why market penetration is usually the least risky growth strategy.', 'The business already knows its product and customers, so it builds on existing knowledge, brands and distribution.', '1 mark existing knowledge; 1 mark lower uncertainty. [2]'),
            ('Explain one reason why a business might choose diversification despite its risk.', 'To spread risk across markets if its existing market is declining, or to exploit high-growth opportunities and use spare resources.', '1 mark reason; 1 mark explanation. [2]'),
            ('Explain how Ansoff\'s matrix can be used with other strategic tools.', 'SWOT and PESTLE identify opportunities and risks for each option; investment appraisal and decision trees then evaluate the chosen options.', '1 mark link to analysis tools; 1 mark link to choice tools. [2]')],
      adv=[('a strategy of market development by selling {prod} in {newmkt}', ['uses existing product knowledge', 'larger market and growth', 'spreads risk across countries'],
            ['lack of knowledge of the new market', 'cultural and legal differences', 'costs of entry and adaptation']),
           ('a strategy of diversification by launching {newprod} in {newmkt}', ['spreads risk across markets', 'high growth potential', 'uses spare resources'],
            ['highest risk in Ansoff', 'lack of experience in product and market', 'large investment required'])],
      anl=[("Analyse the risks to {b} of launching {newprod} in {newmkt}, using Ansoff's matrix.", ['new product in new market is diversification', 'lack of market knowledge', 'lack of product experience', 'large investment with uncertain demand']),
           ('Analyse how {b} could increase market penetration of its {prod} in {country}.', ['market penetration = existing products, existing markets', 'promotion and loyalty schemes', 'competitive pricing', 'wider distribution'])],
      ev=[("Using Ansoff's matrix, evaluate the most suitable growth strategy for {b}.", ['market penetration is low risk', 'market development uses existing products in {newmkt}', 'product development builds on customers with {newprod}'],
           ['penetration limited in saturated markets', 'development needs market knowledge', 'diversification is highest risk'],
           ['its resources and core competencies', 'the growth of its current market', 'its attitude to risk']),
          ('Discuss whether {b} should diversify by launching {newprod} in {newmkt}.', ['spreads risk', 'growth potential', 'uses core competencies'],
           ['highest-risk strategy', 'lack of experience', 'large investment'],
           ['market research evidence', 'available finance', 'links with existing competencies'])])


@t.add('C1', (1, 2, 3), 'mcq')
def ansoff_class(r, D):
    c = r.choice(CASES)
    opts_ = [(f'{c["b"]} plans to sell more of its {c["prod"]} to existing customers in {c["country"]} through a loyalty scheme.', 'Market penetration'),
             (f'{c["b"]} plans to start selling its {c["prod"]} in {c["newmkt"]}.', 'Market development'),
             (f'{c["b"]} plans to launch {c["newprod"]} for its existing customers in {c["country"]}.', 'Product development'),
             (f'{c["b"]} plans to launch {c["newprod"]} in {c["newmkt"]}.', 'Diversification')]
    s, a = r.choice(opts_)
    opts, ans = mcq(r, a, [x for x in ['Market penetration', 'Market development', 'Product development', 'Diversification'] if x != a])
    return {'stem': s + " Which strategy in Ansoff's matrix is this?", 'options': opts, 'answer': ans, 'key': f'{a}.', 'marks': 1}


@t.add('C3', (1, 2, 3, 4), 'case')
def ansoff_case(r, D):
    c = r.choice(CASES)
    moves = [(f'selling more {c["prod"]} in {c["country"]}', 'market penetration', 1), (f'selling {c["prod"]} in {c["newmkt"]}', 'market development', 2),
             (f'launching {c["newprod"]} in {c["country"]}', 'product development', 2), (f'launching {c["newprod"]} in {c["newmkt"]}', 'diversification', 3)]
    pick = r.sample(moves, 3 if D >= 3 else 2)
    stem = f'{intro(r, c)} The directors of {c["b"]} are considering: ' + '; '.join(f'option {i + 1}, {m[0]}' for i, m in enumerate(pick)) + ". Identify the Ansoff strategy for each option and rank them by risk"
    key = '; '.join(f'option {i + 1}: {m[1]}' for i, m in enumerate(pick)) + f' [{len(pick)}]; ranking by distance from existing products/markets: ' + ' > '.join(f'option {i + 1}' for i, m in sorted(enumerate(pick), key=lambda x: -x[1][2])) + ' [1]'
    m = len(pick) + 1
    if D >= 4:
        stem += ', explaining one reason for your ranking'
        key += '; reason: less knowledge of new product/market increases uncertainty [1]'
        m += 1
    return {'stem': stem + '.', 'answer': '; '.join(f'option {i + 1} {x[1]}' for i, x in enumerate(pick)), 'key': key + f'. [{m}]', 'marks': m, 'type': 'case'}


t = T(16, 'Force field analysis', ['force field analysis', 'force field', 'driving forces', 'restraining forces'],
      defs=[('force field analysis', 'A decision-making technique (Lewin) that identifies and scores the driving forces for a change and the restraining forces against it, to judge whether the change is likely to succeed.'),
            ('driving forces', 'Factors that push an organisation towards a proposed change, e.g. new technology, competitive pressure or cost savings.'),
            ('restraining forces', 'Factors that work against a proposed change, e.g. employee resistance, cost or lack of skills.'),
            ('equilibrium (force field)', 'The current situation, maintained because the driving and restraining forces are balanced.')],
      mcqs=[('In force field analysis, which is most likely to be a restraining force against introducing new technology?', 'Fear of job losses among employees', ['Lower unit costs', 'Pressure from competitors', 'Customer demand for faster service'],
             'Restraining forces resist change.'),
            ('A change is more likely to succeed when', 'total driving forces exceed total restraining forces', ['restraining forces exceed driving forces', 'both totals are zero', 'only restraining forces are weighted'],
             'Change moves the equilibrium when drivers outweigh restrainers.'),
            ('Who developed force field analysis?', 'Kurt Lewin', ['Igor Ansoff', 'Michael Porter', 'John Kotter'],
             'Lewin also proposed the unfreeze–change–refreeze model.')],
      exps=[('Explain how managers can use force field analysis to help implement change.', 'They can strengthen driving forces (e.g. communicate benefits) and reduce restraining forces (e.g. training, consultation), shifting the balance towards change.', '1 mark strengthen drivers; 1 mark weaken restrainers. [2]'),
            ('Explain one limitation of force field analysis.', 'The scores given to forces are subjective and may be biased, so the result may not reflect reality.', '1 mark subjectivity; 1 mark consequence. [2]'),
            ('Explain why reducing restraining forces may be more effective than increasing driving forces.', 'Pushing harder can increase resistance and tension; removing obstacles such as fear or lack of skills makes change smoother.', '1 mark extra pressure creates resistance; 1 mark removing obstacles. [2]')],
      adv=[('using force field analysis before restructuring', ['identifies sources of resistance', 'helps plan actions to support change', 'involves managers in structured discussion'],
            ['scores are subjective', 'may oversimplify', 'time-consuming'])],
      anl=[('Analyse how force field analysis could help {b} introduce a new IT system.', ['force field compares driving and restraining forces', 'identifies resistance from staff', 'plans training and communication to reduce restraining forces', 'judges likelihood of success']),
           ('Analyse the main driving and restraining forces {b} might face if it relocates its main site.', ['driving: lower costs, room to expand', 'driving: government incentives', 'restraining: staff unwilling to move', 'restraining: relocation costs and disruption'])],
      ev=[('Evaluate the usefulness of force field analysis to {b} when making a major strategic change.', ['structured view of pressures', 'identifies resistance', 'supports planning of change'],
           ['subjective scores', 'does not show financial return', 'forces may change'],
           ['who scores the forces', 'use alongside investment appraisal', 'the complexity of the change']),
          ('Discuss whether {b} should go ahead with a change when the driving forces only slightly exceed the restraining forces.', ['change is favoured', 'drivers may grow', 'restrainers can be reduced'],
           ['narrow margin', 'subjective scores', 'risk of failure'],
           ['ability to reduce restraining forces', 'the cost of failure', 'strategic importance'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def ffa_calc(r, D):
    c = r.choice(CASES)
    change = r.choice(['introducing automation in its main factory', 'moving to a flat structure', 'relocating to a new site', 'introducing a new ERP system', 'entering a new export market'])
    dr = r.sample([('cost savings', None), ('pressure from competitors', None), ('customer demand', None), ('government grants', None), ('new technology available', None)], 3)
    rs = r.sample([('employee resistance', None), ('cost of change', None), ('lack of skills', None), ('trade union opposition', None), ('risk of disruption', None)], 3)
    ds = [r.randint(2, 5) for _ in dr]; rs_s = [r.randint(2, 5) for _ in rs]
    if sum(ds) == sum(rs_s):
        ds[0] = ds[0] + 1 if ds[0] < 5 else ds[0] - 1
    td, tr = sum(ds), sum(rs_s)
    tbl = 'driving forces — ' + ', '.join(f'{n} {s}' for (n, _), s in zip(dr, ds)) + '; restraining forces — ' + ', '.join(f'{n} {s}' for (n, _), s in zip(rs, rs_s))
    if D == 1:
        opts, ans = mc_num(r, td, [tr, td + tr, td - tr if td != tr else 1], lambda x: str(round(x)))
        return {'stem': f'In a force field analysis (scores 1–5): {tbl}. What is the total score for the driving forces?', 'options': opts, 'answer': ans, 'key': ' + '.join(map(str, ds)) + f' = {td}.', 'marks': 1}
    stem = f'{c["full"]} is considering {change}. Managers score each force from 1 (weak) to 5 (strong): {tbl}. Calculate the total of each set of forces and state what the analysis suggests'
    key = f'Driving = {" + ".join(map(str, ds))} = {td} [1]; restraining = {" + ".join(map(str, rs_s))} = {tr} [1]; {"drivers exceed restrainers, so change likely to succeed" if td > tr else "restrainers exceed drivers, so change likely to fail unless forces are altered"} [1]'
    m = 3
    if D >= 4:
        big = max(zip(rs_s, [n for n, _ in rs]))[1]
        stem += f'. Suggest how {c["b"]} could reduce the strongest restraining force'
        key += f'; strongest restraining: {big} — e.g. consultation, training, phased introduction, financial support [1]'
        m = 4
    if D >= 5:
        stem += ', and evaluate the reliability of this technique'
        key += '; scores subjective, may reflect managers\' bias; forces change over time [1]'
        m = 5
    return {'stem': stem + '.', 'answer': f'Driving {td}, restraining {tr}: ' + ('change favoured' if td > tr else 'change not favoured'), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


def _tree(r):
    """Two options, each with a cost and 2-3 chance outcomes; returns data and EVs ($000)."""
    opts = []
    names = r.sample(['launch a new product', 'open a new factory', 'expand into a new country', 'upgrade existing equipment', 'run a major advertising campaign', 'acquire a small competitor'], 2)
    for nm in names:
        cost = r.choice([100, 150, 200, 250, 300, 400])
        if r.random() < 0.5:
            p = r.choice([0.6, 0.7, 0.75, 0.8, 0.5, 0.4])
            outs = [('success', p, cost * r.choice([1.5, 2, 2.5, 3])), ('failure', round(1 - p, 2), cost * r.choice([0.2, 0.4, 0.5, 0.8]))]
        else:
            ps = r.choice([(0.5, 0.3, 0.2), (0.4, 0.4, 0.2), (0.3, 0.5, 0.2), (0.6, 0.3, 0.1)])
            outs = [('high demand', ps[0], cost * r.choice([2.5, 3])), ('medium demand', ps[1], cost * r.choice([1.2, 1.5])), ('low demand', ps[2], cost * r.choice([0.3, 0.5]))]
        ev = sum(p * v for _, p, v in outs)
        opts.append((nm, cost, outs, ev, ev - cost))
    return opts


def _tree_txt(o):
    nm, cost, outs, ev, net = o
    return f'{nm} costs ${cost}k, with ' + ', '.join(f'{n} (probability {p:g}) returning ${num(v, 1)}k' for n, p, v in outs)


t = T(16, 'Decision trees: expected values', ['decision trees: expected values', 'decision trees', 'expected values', 'probability'],
      defs=[('decision tree', 'A diagram that sets out the options available to a decision-maker, the possible outcomes of each, their probabilities and financial results, so that expected values can be compared.'),
            ('expected value', 'The weighted average of all the possible financial outcomes of a decision, using their probabilities as weights: Σ (probability × outcome).'),
            ('decision node', 'A point on a decision tree, shown as a square, where the business must choose between options.'),
            ('chance node', 'A point on a decision tree, shown as a circle, where different outcomes may occur, each with a probability.')],
      mcqs=[('On a decision tree, a circle represents', 'a chance node where outcomes have probabilities', ['a decision the manager must make', 'the final outcome', 'the cost of the option'],
             'Squares = decisions; circles = chance events.'),
            ('Two outcomes have probabilities of 0.7 and 0.3 and values of $100 000 and $20 000. The expected value is', '$76 000', ['$60 000', '$120 000', '$50 000'],
             '0.7 × 100 000 + 0.3 × 20 000 = 70 000 + 6 000 = 76 000.'),
            ('Which is a major limitation of decision trees?', 'Probabilities and outcomes are estimates that may be inaccurate', ['They cannot show more than one option', 'They ignore financial outcomes', 'They always give the same answer as payback'],
             'Results depend on the accuracy of the estimates.')],
      exps=[('Explain one advantage of using decision trees.', 'They set out options and outcomes clearly and allow risk (probability) and return to be combined in a single expected value for comparison.', '1 mark advantage; 1 mark explanation. [2]'),
            ('Explain why the option with the highest expected value may not be chosen.', 'Expected value is an average; managers may be risk-averse and avoid an option with a chance of a large loss, or qualitative factors may matter.', '1 mark average/risk; 1 mark risk attitude or qualitative. [2]'),
            ('Explain why the probabilities used in a decision tree are often unreliable.', 'They are usually estimated from past experience or market research, and the future may differ; managers may also be biased.', '1 mark estimated; 1 mark reasons for error. [2]')],
      adv=[('using decision trees to choose between strategic options', ['clear presentation of options and outcomes', 'combines risk and return', 'encourages logical thinking'],
            ['probabilities are estimates', 'ignores qualitative factors', 'expected value is an average not an actual outcome'])],
      anl=[('Analyse how a decision tree could help {b} decide whether to launch {newprod}.', ['decision tree shows options, outcomes and probabilities', 'expected values allow comparison', 'includes costs of each option', 'highlights risk of failure']),
           ('Analyse the limitations for {b} of basing a major decision on expected values.', ['EV is a weighted average', 'probabilities and payoffs are estimates', 'ignores attitude to risk', 'ignores qualitative factors and timing of cash flows'])],
      ev=[('Evaluate the usefulness of decision trees to the directors of {b} when choosing a growth strategy.', ['logical and quantitative', 'combines probability and return', 'compares several options'],
           ['estimated data', 'ignores qualitative factors', 'average outcome may never occur'],
           ['the quality of the estimates', 'the directors\' attitude to risk', 'use with other tools']),
          ('Discuss whether {b} should always choose the option with the highest expected value.', ['maximises long-run average return', 'objective', 'easy to compare'],
           ['risk of large loss', 'estimates may be wrong', 'qualitative and ethical factors'],
           ['the size of the possible loss relative to its finance', 'confidence in probabilities', 'strategic fit'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def tree_calc(r, D):
    c = r.choice(CASES)
    tr = _tree(r)
    if D == 1:
        nm, cost, outs, ev, net = tr[0]
        opts, ans = mc_num(r, ev, [sum(v for _, _, v in outs) / len(outs), ev - cost, max(v for _, _, v in outs)], lambda x: f'${num(x, 1)}k')
        return {'stem': f'An option has outcomes ' + ', '.join(f'${num(v, 1)}k (probability {p:g})' for _, p, v in outs) + '. What is its expected value?', 'options': opts, 'answer': ans,
                'key': ' + '.join(f'{p:g} × {num(v, 1)}' for _, p, v in outs) + f' = ${num(ev, 1)}k.', 'marks': 1}
    a, b = tr
    stem = f'{c["full"]} must choose between two options (or do nothing). Option 1: {_tree_txt(a)}. Option 2: {_tree_txt(b)}. Calculate the expected value of each option'
    key = '; '.join(f'Option {i + 1}: EV = ' + ' + '.join(f'{p:g} × {num(v, 1)}' for _, p, v in o[2]) + f' = {num(o[3], 1)}' for i, o in enumerate(tr)) + ' [2]'
    m = 2
    if D >= 3:
        stem += ', the net expected value after costs, and state which option should be chosen on financial grounds'
        best = max(range(2), key=lambda i: tr[i][4])
        choice = f'option {best + 1}' if tr[best][4] > 0 else 'do nothing (both net EVs negative)'
        key += '; net EV: ' + ', '.join(f'option {i + 1} {num(o[3], 1)} − {o[1]} = {num(o[4], 1)}' for i, o in enumerate(tr)) + f' [1]; choose {choice} [1]'
        m = 4
    if D >= 4:
        stem += '. Explain one reason why the directors might not choose this option'
        key += '; risk of worst outcome, unreliable probabilities, qualitative factors, finance availability [1]'
        m = 5
    if D >= 5:
        stem += ' and evaluate the use of decision trees for this decision'
        key += '; evaluation of estimates, risk attitude and other tools [1]'
        m = 6
    return {'stem': stem + '.', 'answer': '; '.join(f'option {i + 1}: EV ${num(o[3], 1)}k' + (f', net ${num(o[4], 1)}k' if D >= 3 else '') for i, o in enumerate(tr)), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


@calc_part(t)
def tree_parts(r, c):
    a, b = _tree(r)
    return [lambda r: (f'Option 1: {_tree_txt(a)}. Option 2: {_tree_txt(b)}. Calculate the net expected value of each option and recommend one on financial grounds.',
                       f'Option 1 {num(a[4], 1)}k; option 2 {num(b[4], 1)}k',
                       f'EVs {num(a[3], 1)} and {num(b[3], 1)}; minus costs → {num(a[4], 1)} and {num(b[4], 1)}; choose the higher positive [4]')]

# =====================================================================================
# 17 Strategic implementation
# =====================================================================================

t = T(17, 'Business plans and corporate plans', ['business plans and corporate plans', 'business plan', 'corporate plan'],
      defs=[('business plan', 'A document describing a business, its objectives and strategies, the market it operates in and its financial forecasts, often used to obtain finance.'),
            ('corporate plan', 'A long-term plan for the whole organisation, setting out its objectives and the strategies and resources needed to achieve them.'),
            ('mission statement', 'A brief statement of the purpose and values of an organisation, intended to guide stakeholders.'),
            ('contingency plan', 'A plan prepared in advance to deal with possible future events that could disrupt the business.')],
      mcqs=[('What is the main purpose of a business plan for a new business?', 'To set out objectives and forecasts, often to persuade lenders or investors', ['To guarantee success', 'To replace market research', 'To calculate tax owed'],
             'Business plans support finance applications and give direction.'),
            ('Which is a limitation of corporate planning?', 'Plans may become out of date if the environment changes quickly', ['Plans give no direction', 'Plans prevent all risk', 'Plans are always short term'],
             'Rigid plans can fail in fast-changing markets; emergent strategy may be needed.'),
            ('A corporate plan usually covers', 'the whole organisation over several years', ['one department for one week', 'only the marketing mix', 'a single product launch'],
             'Corporate plans are long-term and organisation-wide.')],
      exps=[('Explain two benefits to a business of having a corporate plan.', 'It gives clear direction and coordinates departments; it helps allocate resources to priorities; it provides a benchmark to monitor performance.', '2 × (1 mark benefit, 1 mark explanation). [4]'),
            ('Explain why a business plan may help a business obtain a bank loan.', 'It shows the bank the objectives, market research, cash-flow and profit forecasts, reassuring it that the loan can be repaid.', '1 mark contents; 1 mark reassurance of repayment. [2]'),
            ('Explain the difference between planned (intended) and emergent strategy.', 'Planned strategy is set out in advance in a corporate plan; emergent strategy develops over time as managers respond to unexpected events.', '1 mark each. [2]')],
      adv=[('preparing a detailed five-year corporate plan', ['clear direction', 'coordination of departments', 'targets to monitor'],
            ['may become out of date', 'time and cost of preparation', 'may discourage flexibility'])],
      anl=[('Analyse how a corporate plan could help {b} achieve its long-term objectives.', ['corporate plan sets objectives, strategies and resources', 'coordinates functional plans', 'allocates finance to priorities', 'allows monitoring and review']),
           ('Analyse why a business plan would be important if {b} sought outside finance to launch {newprod}.', ['business plan sets out objectives and forecasts', 'investors and banks assess risk and return', 'shows market research and strategy', 'cash-flow forecasts show ability to repay'])],
      ev=[('Evaluate whether corporate planning is still useful for a business like {b} operating in a rapidly changing market.', ['direction and coordination', 'resource allocation', 'benchmark for control'],
           ['plans date quickly', 'emergent strategy needed', 'cost of planning'],
           ['how often the plan is reviewed', 'speed of change in its market', 'flexibility built into the plan']),
          ('Discuss whether {b} should rely on planned strategy or allow strategy to emerge.', ['planned strategy gives clarity', 'coordinates resources', 'reassures investors'],
           ['emergent strategy responds to change', 'plans may fail', 'learning from experience'],
           ['market volatility', 'management style', 'stage of the business'])])


t = T(17, 'Corporate culture', ['corporate culture and its influence on strategy', 'corporate culture', 'organisational culture'],
      defs=[('corporate culture', 'The values, attitudes, beliefs and ways of behaving shared by people in an organisation ("the way we do things around here").'),
            ('power culture (Handy)', 'A culture in which power is concentrated in one person or a small group at the centre, who make quick decisions.'),
            ('role culture (Handy)', 'A culture based on rules, procedures and job descriptions, typical of large bureaucratic organisations.'),
            ('task culture (Handy)', 'A culture based on teams formed to complete particular projects, valuing expertise and results rather than position.'),
            ('person culture (Handy)', 'A culture in which individuals see themselves as more important than the organisation, e.g. in a partnership of professionals.')],
      mcqs=[('A business where project teams are formed and dissolved as needed is most likely to have', 'a task culture', ['a power culture', 'a role culture', 'a person culture'],
             'Task culture values teams and expertise.'),
            ('Which is a likely effect of a strong customer-focused culture?', 'Employees take initiative to solve customer problems', ['Staff follow rules regardless of customers', 'Decisions are always slower', 'Customer complaints rise'],
             'Shared values shape behaviour.'),
            ('Why is changing corporate culture difficult?', 'Values and habits are deeply held and staff may resist', ['Culture can be changed by one email', 'Culture has no effect on behaviour', 'Culture only exists in small firms'],
             'Culture change takes time, leadership and consistent signals.')],
      exps=[('Explain how corporate culture can influence a firm\'s strategy.', 'Culture shapes attitudes to risk and change; an innovative culture supports new products, while a risk-averse role culture favours cautious strategies.', '1 mark culture shapes attitudes; 1 mark effect on strategic choice. [2]'),
            ('Explain why culture clashes are a common problem after mergers.', 'The two firms have different values, management styles and ways of working, which cause conflict, low morale and poor integration.', '1 mark different values; 1 mark consequence. [2]'),
            ('Explain one way leaders can change corporate culture.', 'By role-modelling new values, changing reward systems, recruiting people who fit the new culture and communicating a clear vision.', '1 mark method; 1 mark explanation. [2]')],
      adv=[('changing from a role culture to a task culture', ['more innovation and flexibility', 'faster response to customers', 'uses expertise better'],
            ['staff used to rules may resist', 'less control and consistency', 'conflict over resources between teams'])],
      anl=[('Analyse how the corporate culture of {b} could affect its ability to grow.', ['culture = shared values and behaviour', 'innovative culture supports new products such as {newprod}', 'risk-averse culture slows change', 'culture affects motivation and recruitment']),
           ('Analyse the problems {b} might face if it tried to change its corporate culture.', ['culture is deeply embedded', 'resistance from long-serving staff', 'time and leadership commitment needed', 'short-term fall in productivity'])],
      ev=[('Evaluate the importance of corporate culture to the success of {bp} strategy.', ['shapes behaviour and decisions', 'supports or blocks change', 'affects motivation and customer service'],
           ['finance and resources also matter', 'strong culture may resist needed change', 'external factors may dominate'],
           ['fit between culture and strategy', 'leadership', 'speed of change required']),
          ('Discuss whether {b} should try to change its corporate culture.', ['needed for new strategy', 'improves innovation', 'attracts talent'],
           ['difficult and slow', 'risk of losing staff', 'current culture may be a strength'],
           ['the gap between current and desired culture', 'leadership commitment', 'how change is managed'])])


@t.add('C1', (1, 2, 3), 'mcq')
def handy_class(r, D):
    c = r.choice(CASES)
    items = [(f'At {c["b"]} the founder makes almost all important decisions personally and quickly.', 'Power culture'),
             (f'At {c["b"]} staff follow detailed procedures and job descriptions, and status depends on position in the hierarchy.', 'Role culture'),
             (f'At {c["b"]} small expert teams are formed for each project and judged on results.', 'Task culture'),
             (f'At {c["b"]} highly qualified specialists work largely independently and the organisation exists to support them.', 'Person culture')]
    s, a = r.choice(items)
    opts, ans = mcq(r, a, [x for x in ['Power culture', 'Role culture', 'Task culture', 'Person culture'] if x != a])
    return {'stem': s + " Which of Handy's cultures does this describe?", 'options': opts, 'answer': ans, 'key': f'{a} (Handy).', 'marks': 1}


KOTTER = ['create a sense of urgency', 'build a guiding coalition', 'form a strategic vision', 'communicate the vision', 'remove obstacles and empower action',
          'generate short-term wins', 'sustain acceleration (build on the change)', 'institute (anchor) the change in the culture']

t = T(17, 'Managing change and Kotter\'s eight steps', ["managing change: resistance and kotter's eight steps", 'managing change', 'kotter', 'resistance to change'],
      defs=[('change management', 'Planning, implementing and controlling changes in an organisation so that they are accepted and achieve their objectives.'),
            ('resistance to change', 'Unwillingness of employees or managers to accept change, often because of fear of the unknown, job loss, loss of status or poor communication.'),
            ("Kotter's eight steps", 'A model for leading change: create urgency, build a guiding coalition, form a vision, communicate it, remove obstacles, create short-term wins, build on the change and anchor it in the culture.'),
            ('project champion', 'A person who leads and promotes a change project, persuading others of its benefits and helping to overcome resistance.')],
      mcqs=[("What is the first of Kotter's eight steps for leading change?", 'Create a sense of urgency', ['Generate short-term wins', 'Anchor the change in the culture', 'Communicate the vision'],
             'People must first see why change is needed.'),
            ("Which of Kotter's steps helps keep momentum by showing early results?", 'Generate short-term wins', ['Build a guiding coalition', 'Create a sense of urgency', 'Form a strategic vision'],
             'Visible early successes build support.'),
            ('Which is the most common reason for employees resisting change?', 'Fear of the unknown and of losing their jobs or status', ['Too much information about the change', 'A wish to work longer hours', 'Higher pay'],
             'Uncertainty and self-interest drive resistance.')],
      exps=[('Explain two reasons why employees may resist change.', 'Fear of job losses or lower pay; loss of status or skills; fear of the unknown; poor communication and lack of trust.', '2 × (1 mark reason, 1 mark explanation). [4]'),
            ('Explain why "anchoring the change in the culture" is the final step in Kotter\'s model.', 'Unless new behaviours become part of the shared values, staff drift back to old habits once pressure eases.', '1 mark embed in culture; 1 mark prevent reversion. [2]'),
            ('Explain how communication can reduce resistance to change.', 'Explaining why change is needed, how it will affect staff and listening to concerns reduces uncertainty and rumours and builds trust.', '1 mark explain reasons/effects; 1 mark reduces fear/builds trust. [2]')],
      adv=[("using Kotter's eight-step model to manage a major change", ['structured approach', 'builds support and momentum', 'embeds the change'],
            ['time-consuming', 'linear steps may not fit reality', 'needs strong leadership']),
           ('involving employees in planning a major change', ['less resistance', 'better ideas from staff', 'greater commitment'],
            ['slower decisions', 'conflict over options', 'may raise expectations'])],
      anl=[('Analyse why employees at {b} might resist a major change and how managers could reduce this resistance.', ['resistance from fear of job loss, status or the unknown', 'communication and consultation', 'training and support', 'involvement and incentives']),
           ("Analyse how {b} could use Kotter's eight steps to introduce a new strategy.", ['create urgency by explaining threats and opportunities', 'build a coalition and vision', 'communicate and remove obstacles', 'short-term wins and anchor in culture'])],
      ev=[('Evaluate the most important factor in successfully managing change at {b}.', ['leadership and vision', 'communication', 'involvement of staff'],
           ['resources and training also needed', 'culture may block change', 'external pressures'],
           ['the scale of the change', 'the current culture', 'trust between managers and staff']),
          ("Discuss whether Kotter's eight steps would help {b} manage a major restructuring.", ['clear sequence', 'addresses people side of change', 'builds momentum'],
           ['linear model', 'time-consuming', 'may not fit urgent change'],
           ['the urgency of the change', 'leadership capability', 'how flexibly the model is used'])])


@t.add('C1', (1, 2, 3), 'mcq')
def kotter_order(r, D):
    i = r.randrange(1, 8)
    opts, ans = mcq(r, KOTTER[i], [k for j, k in enumerate(KOTTER) if j != i])
    return {'stem': f'In Kotter\'s eight-step model, which step comes immediately after "{KOTTER[i - 1]}"?', 'options': opts, 'answer': ans, 'key': f'Step {i + 1}: {KOTTER[i]}.', 'marks': 1}


@t.add('C3', (1, 2, 3, 4), 'case')
def kotter_case(r, D):
    c = r.choice(CASES)
    k = 3 if D <= 2 else 4
    idx = sorted(r.sample(range(8), k))
    shuf = idx[:]
    while shuf == idx:
        r.shuffle(shuf)
    stem = f'{intro(r, c)} {c["b"]} is introducing a major change. Put these steps from Kotter\'s model in the correct order: ' + '; '.join(f'({chr(65 + j)}) {KOTTER[x]}' for j, x in enumerate(shuf))
    order = sorted(range(k), key=lambda j: shuf[j])
    ans = ' → '.join(chr(65 + j) for j in order)
    m = 2 if D <= 2 else 3
    key = f'Correct order {ans} (steps ' + ', '.join(str(shuf[j] + 1) for j in order) + ') [2]'
    if D >= 3:
        stem += ', and explain how one of these steps could be applied at ' + c['b']
        key += f'; application of a step to {c["b"]} [1]'
    return {'stem': stem + '.', 'answer': ans, 'key': key + f'. [{m}]', 'marks': m, 'type': 'case'}


t = T(17, 'Crisis management and contingency planning', ['crisis management and contingency planning', 'crisis management', 'contingency planning'],
      defs=[('crisis management', 'Responding to a sudden, unexpected event that threatens the business, its reputation or stakeholders, in a way that limits the damage.'),
            ('contingency planning', 'Preparing in advance for unexpected events, by identifying possible risks and deciding the actions and resources needed to deal with them.'),
            ('risk assessment', 'Identifying possible risks, estimating their likelihood and potential impact, and deciding how to reduce or manage them.'),
            ('business continuity', 'The ability of a business to keep its essential functions running during and after a crisis.')],
      mcqs=[('What is the main purpose of contingency planning?', 'To be ready to respond quickly to unexpected events', ['To guarantee no crisis will happen', 'To replace the corporate plan', 'To increase short-term profit'],
             'Plans reduce the damage and response time when events occur.'),
            ('Which is the best example of a crisis for a food manufacturer?', 'A product contamination scare reported in the media', ['A planned price increase', 'A routine staff appraisal', 'An annual stocktake'],
             'Crises are sudden, unexpected and threaten reputation or operations.'),
            ('Why is fast, honest communication important during a crisis?', 'It protects trust and reputation with stakeholders', ['It removes the need for any other action', 'It increases the damage', 'It is required only after the crisis ends'],
             'Delays and denial usually worsen reputational damage.')],
      exps=[('Explain why contingency planning can be expensive yet worthwhile.', 'It requires time, training, backup systems and spare resources that may never be used, but it greatly reduces losses and recovery time if a crisis happens.', '1 mark cost; 1 mark benefit in a crisis. [2]'),
            ('Explain two features of effective crisis management.', 'Fast decision-making by a crisis team; clear, honest communication with stakeholders; rapid action to protect people and restore operations.', '2 × (1 mark feature, 1 mark explanation). [4]'),
            ('Explain why it is impossible to plan for every crisis.', 'Some events are unforeseeable and resources are limited, so planning focuses on the most likely and most damaging risks.', '1 mark unforeseeable; 1 mark prioritising. [2]')],
      adv=[('preparing a detailed contingency plan for a supply chain failure', ['faster response and less disruption', 'protects reputation', 'reassures customers and investors'],
            ['cost of planning and backup suppliers', 'may never be used', 'plans may not fit the actual crisis'])],
      anl=[('Analyse how {b} could prepare for a major crisis such as a fire at its main site.', ['contingency planning identifies risks in advance', 'backup facilities and suppliers', 'crisis team and communication plan', 'insurance and data back-ups']),
           ('Analyse the possible effects on {b} of handling a product safety crisis badly.', ['crisis threatens stakeholders and reputation', 'loss of customers and sales of {prod}', 'legal action and fines', 'falling share price or investor confidence'])],
      ev=[('Evaluate the importance of contingency planning for {b}.', ['limits damage from crises', 'faster recovery', 'protects reputation'],
           ['costly', 'cannot foresee every event', 'may give false security'],
           ['the risks in its industry', 'the cost of planning versus potential losses', 'how often plans are tested']),
          ('Discuss whether good leadership is more important than contingency plans when {b} faces a crisis.', ['leaders make fast decisions', 'communicate with stakeholders', 'adapt to unforeseen events'],
           ['plans give structure and resources', 'reduce panic', 'leaders need prepared options'],
           ['the type of crisis', 'the quality of the plans', 'the experience of leaders'])])


@t.add('C3', (1, 2, 3, 4, 5), 'numerical')
def risk_calc(r, D):
    c = r.choice(CASES)
    risks = r.sample([('a fire at the main site', 0.02, 2000), ('failure of the main supplier', 0.1, 400), ('a cyber-attack on its IT systems', 0.15, 300),
                      ('a product recall', 0.05, 800), ('flooding of the warehouse', 0.04, 1000), ('a strike by key staff', 0.08, 250)], 2)
    risks = [(n, p, imp * r.choice([0.5, 1, 1.5])) for n, p, imp in risks]
    ev = [p * imp for _, p, imp in risks]
    if D == 1:
        n, p, imp = risks[0]
        opts, ans = mc_num(r, ev[0], [imp, imp / p, p * 100], lambda x: f'${num(x, 1)}k')
        return {'stem': f'A risk has a probability of {p:g} a year and would cost ${num(imp, 0)}k if it happened. What is its expected annual cost?', 'options': opts, 'answer': ans, 'key': f'{p:g} × {num(imp, 0)} = ${num(ev[0], 1)}k.', 'marks': 1}
    tbl = '; '.join(f'{n}: probability {p:g} a year, cost ${num(imp, 0)}k' for n, p, imp in risks)
    stem = f'{c["full"]} has identified two risks — {tbl}. Calculate the expected annual cost of each risk'
    key = '; '.join(f'{n}: {p:g} × {num(imp, 0)} = ${num(e, 1)}k' for (n, p, imp), e in zip(risks, ev)) + ' [2]'
    m = 2
    if D >= 3:
        pc = r.choice([10, 15, 20, 30])
        red = r.choice([0.5, 0.75])
        stem += f'. A contingency plan costing ${pc}k a year would cut the probability of the first risk by {round(red * 100)}%. Calculate whether the plan is financially worthwhile'
        save = ev[0] * red
        key += f'; saving = {num(ev[0], 1)} × {red:g} = ${num(save, 1)}k v cost ${pc}k → {"worthwhile" if save > pc else "not worthwhile on expected values"} [2]'
        m = 4
        if D >= 5:
            stem += ', and explain why the business might adopt it anyway'
            key += '; catastrophic impact, reputation, insurance requirements, risk aversion [1]'
            m = 5
    return {'stem': stem + '.', 'answer': '; '.join(f'{n} ${num(e, 1)}k' for (n, _, _), e in zip(risks, ev)), 'key': key + f'. [{m}]', 'marks': m, 'type': 'numerical' if D < 4 else 'multi_step'}


# =====================================================================================
# Post-processing: interleave C1 item kinds (so definitions do not crowd out MCQs) and give
# calculation templates extra weight in the quantitative chapters.
# =====================================================================================

GENERIC = {'def_short', 'mcq_fixed', 'def_mcq', 'def_rev', 'exp_fixed', 'adv_ex', 'anl_case', 'ev_case', 'case_comp', 'pair'}
HEAVY = {'cpa_calc', 'tree_calc', 'hr_calc', 'ma_calc', 'ped_calc', 'fx_calc', 'interest_calc'}


def _interleave(tpls):
    groups = {}
    for x in tpls:
        groups.setdefault(x.name, []).append(x)
    out = []
    while any(groups.values()):
        for k in list(groups):
            if groups[k]:
                out.append(groups[k].pop(0))
    return out


for _ch, _ts in CHAPTERS.items():
    for _t in _ts:
        c1 = [x for x in _t.templates if x.C == 'C1']
        rest = [x for x in _t.templates if x.C != 'C1']
        extra = [x for x in rest if x.C == 'C3' and x.name not in GENERIC and (_ch in (6, 11, 12, 13, 14) or x.name in HEAVY)]
        _t.templates = _interleave(c1) + rest + extra
