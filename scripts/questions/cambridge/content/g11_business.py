"""Cambridge International AS Level Business 9609, AS content (grade 11), 19 chapters.

Paper 1 (Business Concepts 1: short answers and an essay) and Paper 2 (Business Concepts 2: data
response) style items: business and its environment, human resource management, marketing, operations
management, and finance and accounting at AS Level.

Each topic is built by `T()` from a content spec: definitions, MCQs, explain items, advantage/disadvantage
frames, analysis frames and evaluation frames. It registers C1 definition/MCQ items, C2 explain items,
C3 'Explain/Analyse' items in a case context, and C4 'Evaluate'/essay/structured data-response items.
AS tariffs: define [2], explain [3]/[4], analyse [6]/[8], evaluate [8]/[10]/[12], essay (a) [8] + (b) [12].
Quantitative topics also register calculation specs (`spec`), each giving a C3 calculation (MCQ at D1),
a C2 spot-the-error item and a C4 calculation-plus-evaluation item. Case contexts come from the A Level
case bank in g12_business plus a set of smaller AS-style businesses.
"""
import re

from ._lib import topic, mcq, PEOPLE, CTX
from .g12_business import CASES as _G12CASES, FX, ctx, money, pct, num, nearest, AO_EV, AO_AN

PROFILE = {'mark_scale': {'long': (2.4, 2), 'case': (2, 2)}, 'wordy': True}
CHAPTERS = {}

SMALL = [
    dict(b='Rosa Bakes', full='Rosa Bakes', form='sole trader', country='Mexico', city='Guadalajara', cur='Mexican peso',
         sector='food retail', does='bakes bread and cakes in a small shop and supplies three local cafés', emp=6,
         prod='bread and cakes', newprod='gluten-free cakes', newmkt='online customers in other cities',
         sit='The owner, Rosa, is thinking of opening a second shop.'),
    dict(b='Kaya Cycles', full='Kaya Cycles', form='partnership', country='Kenya', city='Mombasa', cur='Kenyan shilling',
         sector='retail and repairs', does='sells and repairs bicycles and motorbikes', emp=9,
         prod='bicycles and repairs', newprod='electric bicycles', newmkt='tourist hotels on the coast',
         sit='The two partners disagree about whether to borrow money to expand.'),
    dict(b='Petra Prints', full='Petra Prints Ltd', form='private limited company', country='Jordan', city='Amman', cur='Jordanian dinar',
         sector='printing', does='prints leaflets, posters and packaging for local businesses', emp=35,
         prod='printing services', newprod='printed packaging made from recycled card', newmkt='Saudi Arabia',
         sit='A large customer has started to pay its invoices late.'),
    dict(b='Tanvir Textiles', full='Tanvir Textiles Ltd', form='private limited company', country='Bangladesh', city='Dhaka', cur='Bangladeshi taka',
         sector='clothing manufacturing', does='makes shirts and T-shirts for European fashion retailers', emp=420,
         prod='shirts and T-shirts', newprod='organic cotton workwear', newmkt='Japan',
         sit='Labour turnover among machinists has risen sharply this year.'),
    dict(b='Blue Lagoon Tours', full='Blue Lagoon Tours', form='partnership', country='Fiji', city='Nadi', cur='Fijian dollar',
         sector='tourism', does='runs boat trips and diving courses for tourists', emp=14,
         prod='boat trips and diving courses', newprod='overnight island trips', newmkt='cruise-ship passengers',
         sit='Most customers book in the dry season and cash is short in the wet season.'),
    dict(b='Mosaic Apps', full='Mosaic Apps Ltd', form='private limited company', country='Morocco', city='Casablanca', cur='Moroccan dirham',
         sector='software', does='develops booking apps for restaurants and hairdressers', emp=28,
         prod='booking apps', newprod='an app for medical clinics', newmkt='France',
         sit='The founders want to raise finance from venture capitalists.'),
    dict(b='Sunrise Juices', full='Sunrise Juices Ltd', form='private limited company', country='Jamaica', city='Kingston', cur='Jamaican dollar',
         sector='food and drink manufacturing', does='makes fresh fruit juices sold to supermarkets and hotels', emp=60,
         prod='fresh fruit juices', newprod='low-sugar smoothies', newmkt='other Caribbean islands',
         sit='A new supermarket chain wants to stock its juices if it can supply larger quantities.'),
    dict(b='Hamid Engineering', full='Hamid Engineering Ltd', form='private limited company', country='Pakistan', city='Lahore', cur='Pakistani rupee',
         sector='engineering', does='makes pumps and valves for farms and factories', emp=150,
         prod='pumps and valves', newprod='solar-powered water pumps', newmkt='Afghanistan and Central Asia',
         sit='Its factory is working at full capacity and some orders are delivered late.'),
    dict(b='Lotus Spa', full='Lotus Spa', form='sole trader', country='Thailand', city='Chiang Mai', cur='Thai baht',
         sector='personal services', does='offers massages and beauty treatments', emp=8,
         prod='spa treatments', newprod='wellness weekends', newmkt='business travellers',
         sit='The owner wants to introduce online booking and loyalty discounts.'),
    dict(b='Green Valley Dairy', full='Green Valley Dairy Co-operative', form='co-operative', country='India', city='Pune', cur='Indian rupee',
         sector='agriculture and food processing', does='collects milk from 900 member farmers and makes yoghurt and cheese', emp=80,
         prod='yoghurt and cheese', newprod='flavoured milk drinks', newmkt='Mumbai supermarkets',
         sit='The members are arguing about how much of the profit to reinvest.'),
    dict(b='Atlas Furniture', full='Atlas Furniture plc', form='public limited company', country='Egypt', city='Alexandria', cur='Egyptian pound',
         sector='furniture manufacturing and retail', does='makes furniture and sells it through 40 stores', emp=1300,
         prod='furniture', newprod='smart office furniture', newmkt='the Gulf states',
         sit='Sales in its stores have fallen while online sales have grown.'),
    dict(b='Andean Coffee', full='Andean Coffee Ltd', form='private limited company', country='Peru', city='Cusco', cur='Peruvian sol',
         sector='food processing', does='buys coffee beans from small farmers, roasts them and sells them to cafés', emp=45,
         prod='roasted coffee', newprod='coffee capsules', newmkt='the USA',
         sit='The business wants to gain Fairtrade certification.'),
]
for _c in SMALL:
    _c['fx'] = FX.get(_c['cur'], 1)
    _c['bp'] = _c['b'] + ("'" if _c['b'].endswith('s') else "'s")
    _c['cs'] = _c['cur'] + 's'
CASES = list(_G12CASES) + SMALL

ROM = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']
WHO = ['A manager', 'A student', 'The finance director', 'A junior analyst', 'The owner', 'A consultant']
LET = 'abcdefgh'


def fmtc(s, c):
    return s.format_map(_Ctx(c)) if '{' in s else s


class _Ctx(dict):
    def __missing__(self, k):
        return {'f': 'the business', 'b': 'the business', 'bp': "the business's", 'prod': 'products'}.get(k, k)


def cap1(s):
    return s[:1].upper() + s[1:]


def cap(s):
    s = s.strip()
    return s[:1].upper() + s[1:] + ('' if s.endswith('.') else '.')


def intro(r, c):
    e = f"{c['emp']:,}"
    v = r.randrange(4)
    place = c['city'] if c['city'] == c['country'] else f"{c['city']}, {c['country']}"
    if v == 0:
        return f"{c['full']} is a {c['form']} based in {place}. It {c['does']} and employs about {e} people. {c['sit']}"
    if v == 1:
        return f"Based in {c['city']}, {c['full']} ({c['form']}) {c['does']}. The business has around {e} employees. {c['sit']}"
    if v == 2:
        return f"{c['sit']} {c['full']}, a {c['form']} in {c['country']} with about {e} employees, {c['does']}."
    return f"{c['b']} is a {c['form']} in {place} with about {e} staff. It {c['does']}. {c['sit']}"


def pp(r, k=1):
    return r.sample(PEOPLE, k) if k > 1 else r.choice(PEOPLE)


def lst(items):
    return ' '.join(f'({ROM[i]}) {x.rstrip(".")}' for i, x in enumerate(items))


def m(x, dp=0):
    return money(x, dp)


def m2(x):
    return money(x, 2)


def pc(x, dp=1):
    return f'{x:.{dp}f}%'


def step(r, lo, hi, s):
    a, b = max(1, -(-int(lo) // s)), max(1, int(hi) // s)
    return s * r.randint(a, max(a, b))


def num_opts(f, correct, vals):
    c = f(correct)
    ex = []
    for v in vals:
        s = f(v)
        if s != c and s not in ex:
            ex.append(s)
    if len(ex) >= 3:
        return c, ex[:5]
    for v in (correct * 1.1, correct * 0.9, correct * 1.25, correct * 0.8, correct * 2, correct * 0.5, correct + 10, correct - 10):
        s = f(v)
        if s != c and s not in ex:
            ex.append(s)
        if len(ex) >= 3:
            break
    return c, ex


_MK = re.compile(r'\[(\d+)\]\s*$')
_NEG = re.compile(r'(?<![\w)\]])-(?=\$?\d)')


def _fixneg(q):
    if not q:
        return q
    for f in ('stem', 'answer', 'key'):
        if isinstance(q.get(f), str):
            q[f] = _NEG.sub('−', q[f])
    if q.get('options'):
        q['options'] = [_NEG.sub('−', o) for o in q['options']]
    return q


def _pm(key):
    x = _MK.search(key)
    return int(x.group(1)) if x else 1


def build(r, intro_, parts, want, min_parts=1, type_=None, keep_first=True):
    """Structured item: keeps part 1 (if keep_first) and adds others while marks fit `want` (never above 20)."""
    parts = [p for p in parts if p]
    if not parts:
        return None
    idx = list(range(len(parts)))
    if keep_first:
        chosen, rest = [0], idx[1:]
    else:
        r.shuffle(idx)
        chosen, rest = [idx[0]], idx[1:]
    tot = _pm(parts[chosen[0]][2])
    r.shuffle(rest)
    for i in rest:
        mk = _pm(parts[i][2])
        if tot + mk > 20:
            continue
        if tot + mk <= max(want, tot) or len(chosen) < min_parts:
            chosen.append(i)
            tot += mk
    chosen.sort()
    got = [parts[i] for i in chosen]
    if len(got) < min_parts:
        return None
    if len(got) == 1:
        q = {'stem': intro_.strip() + ' ' + got[0][0], 'answer': got[0][1], 'key': got[0][2]}
    else:
        q = {'stem': intro_.strip() + ' ' + ' '.join(f'({LET[j]}) {x[0]}' for j, x in enumerate(got)),
             'answer': ' '.join(f'({LET[j]}) {x[1]}' for j, x in enumerate(got)),
             'key': ' '.join(f'({LET[j]}) {x[2]}' for j, x in enumerate(got))}
    q['marks'] = tot
    q['minutes'] = round(max(1.0, tot * 1.25) * 2) / 2
    if type_:
        q['type'] = type_
    return q


# =====================================================================================
# Mark-scheme text (AS levels of response)
# =====================================================================================

def key_an(mk, c, pts):
    if mk <= 4:
        k, a, n = {2: (1, 1, 0), 3: (1, 1, 1), 4: (1, 1, 2)}[mk]
        s = f"AO1 Knowledge [{k}]: {pts[0]}. AO2 Application [{a}]: point linked to {c['b']} ({c['sector']})."
        if n:
            s += f" AO3 Analysis [{n}]: developed explanation of the consequence, e.g. {'; '.join(pts[1:3])}."
        return s + f' [{mk}]'
    k, a, n = AO_AN[mk]
    return (f"AO1 Knowledge [{k}]: {pts[0]}. AO2 Application [{a}]: uses the case ({ctx(c)}). "
            f"AO3 Analysis [{n}]: developed chains of reasoning showing the impact on {c['b']}, e.g. {'; '.join(pts[1:4])}. "
            f"Levels: L1 knowledge only; L2 applied to the case; L3 developed analysis of two points in context. [{mk}]")


def key_ev(mk, c, fo, ag, dep):
    k, a, n, e = AO_EV[mk]
    return (f"AO1 Knowledge [{k}]: relevant concepts. AO2 Application [{a}]: uses the evidence ({ctx(c)}). "
            f"AO3 Analysis [{n}]: arguments for, e.g. {'; '.join(fo)}; arguments against, e.g. {'; '.join(ag)}. "
            f"AO4 Evaluation [{e}]: a justified judgement that weighs the arguments, e.g. it depends on {'; '.join(dep)}. "
            f"A top-level answer reaches a supported conclusion specific to {c['b']}. [{mk}]")


def key_ev_gen(mk, fo, ag, dep):
    k, a, n, e = AO_EV[mk]
    return (f"AO1 Knowledge [{k}]: accurate understanding of the concepts. AO2 Application [{a}]: relevant business examples or the context in the question. "
            f"AO3 Analysis [{n}]: developed arguments for, e.g. {'; '.join(fo)}; and against, e.g. {'; '.join(ag)}. "
            f"AO4 Evaluation [{e}]: a supported judgement, e.g. it depends on {'; '.join(dep)}. [{mk}]")


def key_an_gen(mk, pts):
    k, a, n = AO_AN[mk]
    return (f"AO1 Knowledge [{k}]: {pts[0]}. AO2 Application [{a}]: relevant examples or the context of the question. "
            f"AO3 Analysis [{n}]: developed chains of reasoning, e.g. {'; '.join(pts[1:4])}. [{mk}]")


def ans_ev(c, fo, ag, dep):
    who = c['b'] if c else 'the business'
    return (f"For: {'; '.join(fo)}. Against: {'; '.join(ag)}. Judgement: for {who} it depends mainly on {dep[0]}"
            + (f", and also on {dep[1]}" if len(dep) > 1 else '') + '.')


DEFS = {}
TOPICS = []


UNINC = ('sole trader', 'partnership', 'co-operative')


def _ok(fr, c):
    """Is a content frame consistent with the case business's legal form?"""
    if callable(fr):
        return True
    txt = ' '.join(x if isinstance(x, str) else ' '.join(x) for x in fr).lower()
    form = c['form']
    if form in UNINC and 'convert' not in txt and re.search(r'share|stock exchange|dividend|public limited', txt):
        return False
    if 'public limited' in form and re.search(r'becom\w* a public limited|convert\w* into a private limited|flotation|float', txt):
        return False
    if form not in UNINC and 'public' not in form and re.search(r'convert\w* into a private limited', txt):
        return False
    return True


def _pick(r, frames, c):
    ok = [f for f in frames if _ok(f, c)]
    return r.choice(ok or frames)


def _case_for(r, *frame_lists):
    """A case business for which every given frame list has at least one consistent frame."""
    for _ in range(30):
        c = r.choice(CASES)
        if all(any(_ok(f, c) for f in fl) for fl in frame_lists if fl):
            return c
    return c


def _frame(fr, r, c):
    if callable(fr):
        return fr(r, c)
    return tuple(fmtc(x, c) if isinstance(x, str) else [fmtc(y, c) for y in x] for x in fr)


def _neutral(s):
    """Frame text without a case: replace case placeholders by generic wording."""
    return (s.replace("{bp}", "a business's").replace('{b}', 'a business').replace('{prod}', 'its products')
            .replace('{newprod}', 'a new product').replace('{newmkt}', 'a new market').replace('{country}', 'its home country')
            .replace('{sector}', 'its industry').replace('{city}', 'its home city'))


def T(ch, name, keys, defs=(), mcqs=(), exps=(), adv=(), anl=(), ev=()):
    """Build an AS topic from a content spec and register its generic templates."""
    t = topic(name, *keys)
    t.ch = ch
    t.defs, t.adv, t.anl, t.ev = list(defs), list(adv), list(anl), list(ev)
    t.entries = {}
    t.disc = []
    DEFS.setdefault(ch, []).extend(defs)
    CHAPTERS.setdefault(ch, []).append(t)
    TOPICS.append(t)

    # ---- C1: definitions [2] and MCQs [1]
    for i, (term, d) in enumerate(defs):
        stem = (f"Define the term '{term}'." if i % 2 == 0 else f"What is meant by '{term}'?")
        key = f'2 marks: full definition – {d.rstrip(".")}. 1 mark: partial definition or a relevant example only. [2]'
        t.entries.setdefault('C1', []).append(((stem, d, key), (1, 2)))

        def fn(r, D, stem=stem, d=d, key=key):
            return {'stem': stem, 'answer': d, 'key': key, 'type': 'short', 'marks': 2}
        fn.__name__ = 'def_short'
        t.add('C1', (1, 2, 3), 'short')(fn)

    for (stem, a, dis, why) in mcqs:
        def fn(r, D, stem=stem, a=a, dis=dis, why=why):
            opts, ans = mcq(r, a, list(dis))
            return {'stem': stem, 'options': opts, 'answer': ans, 'key': f'{a}. {why} [1]', 'marks': 1}
        fn.__name__ = 'mcq_fixed'
        t.add('C1', (1, 2, 3), 'mcq')(fn)

    if defs:
        @t.add('C1', (1, 2), 'mcq')
        def def_mcq(r, D):
            term, d = r.choice(t.defs)
            others = [x for x in DEFS[ch] if x[0] != term]
            if len(others) < 3:
                return None
            ds = [x[1] for x in r.sample(others, 3)]
            opts, ans = mcq(r, d, ds)
            return {'stem': f"Which of the following best defines '{term}'?", 'options': opts, 'answer': ans,
                    'key': f'{term}: {d} [1]', 'marks': 1}

        @t.add('C1', (2, 3), 'mcq')
        def def_rev(r, D):
            term, d = r.choice(t.defs)
            others = [x for x in DEFS[ch] if x[0] != term]
            if len(others) < 3:
                return None
            ds = [x[0] for x in r.sample(others, 3)]
            opts, ans = mcq(r, term, ds)
            return {'stem': f'Which business term is described here: "{d}"', 'options': opts, 'answer': ans,
                    'key': f'This is the definition of {term}. [1]', 'marks': 1}

    # ---- C2: explain items (fixed)
    for e in exps:
        t.entries.setdefault('C2', []).append((e, (2, 3)))

        def fn(r, D, e=e):
            return {'stem': e[0], 'answer': e[1], 'key': e[2], 'type': 'explain', 'marks': _pm(e[2])}
        fn.__name__ = 'exp_fixed'
        t.add('C2', (2, 3, 4), 'explain')(fn)

    # ---- C2: advantage / disadvantage in context
    if adv:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def adv_ex(r, D):
            c = _case_for(r, t.adv)
            concept, pro, con = _frame(_pick(r, t.adv, c), r, c)
            v = r.randrange(2)
            if D <= 2:
                side, pts = (('advantage', pro) if v == 0 else ('disadvantage', con))
                q = r.choice([f'Explain one {side} to {c["b"]} of {concept}.', f'Identify and explain one {side} for {c["b"]} of {concept}.'])
                a = f'{pts[0]}; this would {"help" if side == "advantage" else "be a problem for"} {c["b"]}, which {c["does"]}'
                k = f'1 mark: relevant {side}, e.g. {"; ".join(pts[:3])}. 1 mark: explained in the context of {c["b"]} ({c["sector"]}). [2]'
                mk = 2
            elif D == 3:
                side, pts = (('advantage', pro) if v == 0 else ('disadvantage', con))
                q = f'Explain one {side} to {c["b"]} of {concept}.'
                a = f'{pts[0]}, which matters for {c["b"]} because it {c["does"]}'
                k = (f'1 mark knowledge: a relevant {side}, e.g. {"; ".join(pts[:3])}. 1 mark application to {c["b"]} ({c["sector"]}). '
                     f'1 mark analysis: consequence for the business developed. [3]')
                mk = 3
            else:
                q = (f'Explain one advantage and one disadvantage to {c["b"]} of {concept}.' if v == 0
                     else f'Explain two reasons why {concept} might not benefit {c["b"]}.')
                a = f'Advantage: {pro[0]}. Disadvantage: {con[0]}' if v == 0 else f'{cap1(con[0])}; {con[1]}'
                k = (f'For each point: 1 mark identification, 1 mark explanation applied to {c["b"]}. Advantages: {"; ".join(pro)}. '
                     f'Disadvantages: {"; ".join(con)}. [4]')
                mk = 4
            return {'stem': intro(r, c) + ' ' + q, 'answer': cap(a), 'key': k, 'type': 'explain', 'marks': mk}

    # ---- C3: explain / analyse in context
    if anl:
        @t.add('C3', (2, 3, 4, 5), 'case')
        def anl_case(r, D):
            c = _case_for(r, t.anl)
            q, pts = _frame(_pick(r, t.anl, c), r, c)[:2]
            mk = nearest(CTX.get('want_marks'), (3, 4, 6, 8), {2: 3, 3: 4, 4: 6, 5: 8}[min(5, max(2, D))])
            if mk == 3 and ' two ' in q:
                mk = 4
            if mk <= 4 and q.startswith('Analyse'):
                q = 'Explain' + q[len('Analyse'):]
            if mk >= 6 and q.startswith('Explain'):
                q = 'Analyse' + q[len('Explain'):]
            return {'stem': intro(r, c) + ' ' + q, 'answer': f'Points to develop for {c["b"]}: ' + '; '.join(pts) + '.',
                    'key': key_an(mk, c, pts), 'type': 'case', 'marks': mk}

    # ---- C4: evaluate in context (data response) and Paper 1 style essay
    if ev:
        @t.add('C4', (2, 3, 4, 5), 'long')
        def ev_case(r, D):
            c = _case_for(r, t.ev)
            q, fo, ag, dep = _frame(_pick(r, t.ev, c), r, c)
            mk = nearest(CTX.get('want_marks'), (8, 10, 12), {2: 8, 3: 10, 4: 12, 5: 12}[min(5, max(2, D))])
            return {'stem': intro(r, c) + ' ' + q, 'answer': ans_ev(c, fo, ag, dep), 'key': key_ev(mk, c, fo, ag, dep),
                    'type': 'long', 'marks': mk}

    if ev and anl:
        @t.add('C4', (4, 5), 'long')
        def essay(r, D):
            want = CTX.get('want_marks')
            if want and want < 14:
                return None
            fa = r.choice(t.anl)
            fe = r.choice(t.ev)
            if callable(fa) or callable(fe):
                return None
            qa, pts = [_neutral(x) if isinstance(x, str) else [_neutral(y) for y in x] for x in fa[:2]]
            qe, fo, ag, dep = [_neutral(x) if isinstance(x, str) else [_neutral(y) for y in x] for x in fe]
            if '{' in ' '.join([qa, qe] + list(pts) + list(fo) + list(ag) + list(dep)):
                return None
            if qa.startswith('Explain'):
                qa = 'Analyse' + qa[len('Explain'):]
            return {'stem': f'(a) {qa} (b) {qe}',
                    'answer': f'(a) {cap("; ".join(pts))} (b) {ans_ev(None, fo, ag, dep)}',
                    'key': f'(a) {key_an_gen(8, pts)} (b) {key_ev_gen(12, fo, ag, dep)}', 'type': 'long', 'marks': 20,
                    'minutes': 30}

    # ---- C4: structured data-response question (Paper 2 style)
    @t.add('C4', (2, 3, 4, 5), 'case')
    def case_comp(r, D):
        c = _case_for(r, t.adv, t.anl, t.ev)
        parts = []
        if t.defs:
            term, d = r.choice(t.defs)
            parts.append((f"Define the term '{term}'.", d, '1 mark: partial definition; 2 marks: full definition. [2]'))
        if t.adv:
            concept, pro, con = _frame(_pick(r, t.adv, c), r, c)
            parts.append((f'Explain one {"advantage" if r.random() < 0.5 else "benefit"} to {c["b"]} of {concept}.', cap(pro[0]),
                          f'1 mark point ({"; ".join(pro[:3])}); 1 mark explanation; 1 mark application to {c["b"]}. [3]'))
        if t.anl:
            q, pts = _frame(_pick(r, t.anl, c), r, c)[:2]
            if q.startswith('Explain'):
                q = 'Analyse' + q[len('Explain'):]
            parts.append((q, cap('; '.join(pts)), key_an(8, c, pts)))
        if t.ev:
            q, fo, ag, dep = _frame(_pick(r, t.ev, c), r, c)
            parts.append((q, ans_ev(c, fo, ag, dep), key_ev(12 if D >= 4 else 10, c, fo, ag, dep)))
        if len(parts) < 2:
            return None
        want = CTX.get('want_marks') or {2: 10, 3: 13, 4: 20, 5: 20}[D]
        return build(r, intro(r, c), parts, max(want, 5), min_parts=2, type_='case', keep_first=False)
    return t


# =====================================================================================
# Calculation specs: one scenario function feeds a C3 calculation (MCQ at D1), a C2 error item and a C4 item
# =====================================================================================

def spec(t, D=(1, 2, 3, 4, 5), typ='numerical', err=True, c4=True):
    """fn(r, D) -> dict(setup, parts=[(ask, ans, key[n])], mcq=(q, correct, [ds], key) | None,
    err=(claim, why, right, work, noun) | None, ev=(q, fo, ag, dep) | None, c=case)."""
    def deco(fn):
        nm_ = fn.__name__

        def c3f(r, D):
            s = fn(r, D)
            if not s:
                return None
            if D == 1 and s.get('mcq'):
                q, c, ds, key = s['mcq']
                try:
                    opts, ans = mcq(r, c, ds)
                except ValueError:
                    return None
                return _fixneg({'stem': s['setup'] + ' ' + q, 'options': opts, 'answer': ans, 'key': key + ' [1]', 'marks': 1})
            want = CTX.get('want_marks') or {1: 2, 2: 2, 3: 3, 4: 4, 5: 6}[D]
            return _fixneg(build(r, s['setup'], s['parts'], want, type_=typ if D < 4 else 'multi_step'))
        c3f.__name__ = nm_
        t.add('C3', D, typ)(c3f)
        if err:
            def c2f(r, D):
                s = fn(r, max(2, D))
                if not s or not s.get('err'):
                    return None
                claim, why, right, work, noun = s['err']
                who = r.choice(WHO)
                if D <= 2:
                    ask = r.choice([f'Identify the error and state the correct {noun}.', f'State the mistake made and give the correct {noun}.'])
                    key = f'Error: {why} [1]; correct {noun}: {right} [1] [2]'
                    mk = 2
                else:
                    ask = r.choice([f'Explain the error and calculate the correct {noun}, showing your working.',
                                    f'Explain why this is wrong and calculate the correct {noun}.'])
                    key = f'Error explained: {why} [1]; working: {work} [1]; correct {noun}: {right} [1] [3]'
                    mk = 3
                return _fixneg({'stem': f'{s["setup"]} {who} {claim}. {ask}', 'answer': f'{cap1(why)}. Correct {noun}: {right}.',
                        'key': key, 'marks': mk, 'type': 'explain'})
            c2f.__name__ = nm_ + '_err'
            t.add('C2', (2, 3, 4), 'explain')(c2f)
        if c4:
            def c4f(r, D):
                s = fn(r, min(5, D + 1))
                if not s:
                    return None
                parts = list(s['parts'])
                c = s.get('c')
                evs = []
                if s.get('ev'):
                    evs.append(s['ev'])
                if c and t.ev:
                    evs.append(_frame(_pick(r, t.ev, c), r, c))
                if evs:
                    q, fo, ag, dep = evs[0] if r.random() < 0.6 else evs[-1]
                    mk = 8 if D <= 3 else 10
                    if c:
                        parts.append((q, ans_ev(c, fo, ag, dep), key_ev(mk, c, fo, ag, dep)))
                    else:
                        parts.append((q, ans_ev(None, fo, ag, dep), key_ev_gen(mk, fo, ag, dep)))
                if c and t.anl and s.get('anl', True):
                    q, pts = _frame(_pick(r, t.anl, c), r, c)[:2]
                    if q.startswith('Analyse'):
                        q = 'Explain' + q[len('Analyse'):]
                    parts.append((q, cap('; '.join(pts)), key_an(4, c, pts)))
                want = CTX.get('want_marks') or {2: 8, 3: 10, 4: 12, 5: 14}[D]
                return _fixneg(build(r, s['setup'], parts, max(want, 6), min_parts=2, type_='multi_step'))
            c4f.__name__ = nm_ + '_c4'
            t.add('C4', (2, 3, 4, 5), 'multi_step')(c4f)
        return fn
    return deco


def B(r, min_emp=0):
    """A case business for a calculation context."""
    return r.choice([c for c in CASES if c['emp'] >= min_emp])


# =====================================================================================
# 1 Enterprise
# =====================================================================================

t = T(1, 'Nature of business activity: inputs, outputs and adding value', ['nature of business activity: inputs, outputs and adding value', 'adding value', 'business activity'],
      defs=[('added value', 'The difference between the price a business sells its product for and the cost of the bought-in materials and components used to make it.'),
            ('factors of production', 'The resources needed to produce goods and services: land, labour, capital and enterprise.'),
            ('opportunity cost', 'The benefit of the next best alternative that is given up when a choice is made.'),
            ('economic activity', 'The production of goods and services to satisfy needs and wants, using scarce resources.')],
      mcqs=[('Which of the following is an example of capital as a factor of production?', 'A delivery van owned by a business', ['The skills of a shop assistant', 'A field used to grow wheat', 'The risk taken by a business owner'],
             'Capital means man-made resources used to produce other goods, such as machinery and vehicles.'),
            ('A café buys coffee beans, milk and cups costing $1.20 for each drink and sells each drink for $3.50. What is the added value per drink?', '$2.30', ['$1.20', '$3.50', '$4.70'],
             'Added value = selling price − cost of bought-in materials = $3.50 − $1.20.'),
            ('Which action would most directly increase the added value of a product?', 'Creating a strong brand image so that a higher price can be charged', ['Paying higher wages to production workers', 'Buying more expensive raw materials', 'Increasing the number of units held in inventory'],
             'Added value rises if the price can be raised more than the cost of bought-in inputs.'),
            ('A student chooses to work in a shop on Saturday instead of playing football. The opportunity cost of working is', 'the enjoyment of playing football', ['the wages earned in the shop', 'the cost of travelling to the shop', 'the time spent working'],
             'Opportunity cost is the next best alternative forgone.')],
      exps=[('Explain the difference between added value and profit.', 'Added value is selling price less the cost of bought-in materials only; profit is revenue less all costs, including wages, rent and other overheads, so profit is smaller than added value.', '1 mark added value = price − bought-in materials; 1 mark profit deducts all costs; 1 mark consequence: added value must also pay labour and overheads. [3]'),
            ('Explain why the concept of opportunity cost is important when a business makes decisions.', 'Resources such as finance and time are scarce, so choosing one option means giving up the next best one; comparing the benefit lost helps managers choose the option that gives the greatest return.', '1 mark scarcity; 1 mark next best alternative forgone; 1 mark use in comparing options. [3]'),
            ('Explain two ways a business could increase the value it adds to its products.', 'It could build a brand or improve design and quality so customers pay a higher price; or it could reduce the cost of bought-in materials by finding cheaper suppliers or reducing waste.', '2 × (1 mark method, 1 mark explanation): higher price through branding/quality/convenience/service; lower bought-in costs. [4]')],
      adv=[('raising added value through premium branding of its {prod}', ['customers are willing to pay a higher price', 'higher margin on each sale', 'helps it stand out from competitors'],
            ['branding and promotion are expensive', 'higher prices may reduce sales volume', 'customers may not value the brand enough']),
           ('reducing the cost of bought-in materials for its {prod}', ['added value rises if the price stays the same', 'more competitive prices possible', 'higher profit margins'],
            ['cheaper materials may reduce quality', 'reputation may suffer', 'supplier relationships may be damaged'])],
      anl=[('Analyse two ways in which {b} could increase the added value of its {prod}.', ['added value = selling price − cost of bought-in materials', 'improving quality, design or service allows a higher price', 'building the brand increases what customers will pay', 'reducing waste or finding cheaper suppliers lowers input costs']),
           ('Explain how {b} uses the factors of production to create its {prod}.', ['the four factors are land, labour, capital and enterprise', 'labour and capital transform inputs into outputs', 'enterprise organises the other factors and takes the risk', 'the transformation process adds value']),
           ('Analyse the opportunity cost to {b} of investing in {newprod}.', ['opportunity cost is the next best alternative forgone', 'finance used here cannot be used to improve existing {prod}', 'management time is diverted from the core business', 'the decision depends on the expected return of each option'])],
      ev=[('Evaluate the most effective way for {b} to increase the added value of its {prod}.', ['branding and quality allow a premium price', 'efficiency lowers bought-in costs', 'better customer service differentiates the business'],
           ['price rises may reduce demand', 'cost cutting can harm quality', 'improvements take time and investment'],
           ['how price sensitive its customers are', 'the strength of competitors', 'the finance available']),
          ('Discuss whether increasing added value is more important than increasing sales volume for {b}.', ['higher added value gives a higher margin on every unit', 'a premium position is harder for rivals to copy', 'fewer units need to be sold to cover costs'],
           ['higher volume may bring economies of scale', 'a larger market share gives power over suppliers', 'a price rise may cause customers to switch'],
           ['the nature of its market', 'its capacity', 'its objectives'])])


@spec(t)
def av_calc(r, D):
    c = B(r)
    pr = step(r, 20, 400, 5)
    bi = round(pr * r.uniform(0.25, 0.7))
    q = step(r, 2000, 50000, 500)
    av = pr - bi
    setup = f'{c["b"]} sells its main product for ${pr} per unit. The cost of bought-in materials and components is ${bi} per unit. It sells {q:,} units a year.'
    parts = [('Calculate the added value per unit.', f'${av}', f'${pr} − ${bi} [1]; = ${av} per unit [1] [2]'),
             ('Calculate the total added value for the year.', m(av * q), f'${av} × {q:,} [1]; = {m(av * q)} [1] [2]'),
             ('Calculate the added value as a percentage of the selling price.', pc(av / pr * 100), f'${av} ÷ ${pr} × 100 [1]; = {pc(av / pr * 100)} [1] [2]')]
    if D >= 3:
        ri = step(r, 2, max(2, pr // 8), 2)
        up = ri // 2
        parts.append((f'The supplier raises the cost of materials by ${ri} per unit and {c["b"]} raises its price by ${up}. Calculate the new added value per unit and explain one consequence for the business.',
                      f'${av - ri + up}; lower added value leaves less to pay wages, overheads and profit.',
                      f'${pr + up} − ${bi + ri} = ${av - ri + up} [1]; consequence explained [1] [2]'))
    c_, ds = num_opts(lambda x: f'${int(x)}', av, [pr, bi, pr + bi])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the added value per unit?', c_, ds, f'${pr} − ${bi} = ${av}'),
            'err': (f'calculated the added value per unit as ${pr + bi}', 'the cost of bought-in materials was added to the price instead of being subtracted', f'${av}', f'${pr} − ${bi}', 'added value per unit')}


t = T(1, 'Role and characteristics of entrepreneurs and intrapreneurs', ['role and characteristics of entrepreneurs and intrapreneurs', 'entrepreneurs', 'intrapreneurs'],
      defs=[('entrepreneur', 'A person who has a business idea, organises the factors of production to start a business and takes the risk of doing so.'),
            ('intrapreneur', 'An employee who acts like an entrepreneur inside an existing organisation, developing new ideas, products or processes.'),
            ('enterprise', 'The ability and willingness to take risks, organise resources and start or develop a business.')],
      mcqs=[('Which characteristic is most important for an entrepreneur facing a high risk of business failure?', 'Resilience – the ability to keep going after setbacks', ['A large number of employees', 'A university degree in business', 'Owning premises'],
             'Many new businesses fail; resilience and determination help entrepreneurs survive setbacks.'),
            ('An employee at a software company develops a new app within the company using its resources. This employee is best described as', 'an intrapreneur', ['an entrepreneur', 'a shareholder', 'a sole trader'],
             'Intrapreneurs innovate inside an existing organisation.'),
            ('Which is a major barrier to starting a new business in many countries?', 'Difficulty in raising start-up finance', ['Too many customers', 'Low competition in most markets', 'High government subsidies for new firms'],
             'Banks often see new businesses as risky, so finance is hard to obtain.')],
      exps=[('Explain two characteristics of a successful entrepreneur.', 'Innovation and creativity, so they can spot opportunities and develop new ideas; and willingness to take calculated risks, because starting a business means investing time and money with no guarantee of success.', '2 × (1 mark characteristic, 1 mark explanation): e.g. innovation, risk-taking, determination/resilience, self-confidence, hard work, leadership. [4]'),
            ('Explain why intrapreneurship can benefit a large company.', 'Employees who are encouraged to develop ideas create new products and processes, which keeps the company innovative, helps it respond to change and motivates and retains talented staff.', '1 mark innovation; 1 mark responsiveness/competitiveness; 1 mark motivation/retention. [3]'),
            ('Explain the importance of entrepreneurs to a country\'s economy.', 'Entrepreneurs create new businesses that provide jobs, increase output and economic growth, introduce new products and competition, and pay taxes.', '1 mark each for up to three: employment, output/GDP growth, innovation, competition, tax revenue. [3]')],
      adv=[('encouraging its employees to act as intrapreneurs', ['new ideas for products and processes', 'improves staff motivation', 'helps retain creative employees'],
            ['staff time is taken away from normal duties', 'many ideas will fail and waste resources', 'managers may lose some control']),
           ('relying on the founder\'s entrepreneurial skills', ['quick decisions and a clear vision', 'strong drive to succeed', 'willingness to take risks on new opportunities'],
            ['the business depends on one person', 'the founder may lack management skills as the business grows', 'risk-taking may lead to costly mistakes'])],
      anl=[('Analyse two characteristics that the founder of {b} would need to succeed.', ['entrepreneurs organise resources and take risks', 'creativity to spot opportunities such as {newprod}', 'resilience to survive setbacks in {sector}', 'leadership and communication to manage employees']),
           ('Analyse how {b} could benefit from encouraging intrapreneurship.', ['intrapreneurs innovate inside an existing business', 'new products such as {newprod} could be developed', 'motivated staff are more productive and less likely to leave', 'faster response to competitors and changing tastes'])],
      ev=[('Evaluate whether the personal qualities of the entrepreneur are the most important factor in the success of a new business such as {b}.', ['vision and determination drive the business', 'risk-taking allows opportunities to be exploited', 'leadership motivates staff'],
           ['access to finance is essential', 'the market and level of competition matter', 'economic conditions and government support affect success'],
           ['the nature of the market', 'how much finance is available', 'whether the owner can build a capable team']),
          ('Discuss whether {b} should give employees time to work on their own ideas.', ['innovation could lead to new products', 'staff motivation and retention improve', 'competitive advantage over rivals'],
           ['cost of time away from core work', 'many ideas fail', 'difficult to manage and measure'],
           ['the culture of the business', 'the pace of change in {sector}', 'how ideas are selected and funded'])])


t = T(1, 'Business plans: purpose and contents', ['business plans: purpose and contents', 'business plans', 'business plan'],
      defs=[('business plan', 'A written document that describes a business, its objectives and strategies, the market it is in and its financial forecasts.'),
            ('cash-flow forecast', 'An estimate of the future cash inflows and cash outflows of a business, usually month by month.'),
            ('market analysis', 'The section of a business plan that describes the target market, customers and competitors, based on market research.')],
      mcqs=[('Which is the main reason a new business prepares a business plan when applying for a bank loan?', 'To show the bank that the business is likely to be able to repay the loan', ['To guarantee the business will make a profit', 'To avoid paying tax', 'To register as a limited company'],
             'Lenders want evidence of a viable business that can repay.'),
            ('Which item would normally be included in the financial section of a business plan?', 'A cash-flow forecast', ['The CVs of all customers', 'The design of the company logo only', 'The names of competitors\' employees'],
             'Financial forecasts include cash-flow, profit and break-even forecasts.'),
            ('A limitation of a business plan is that', 'it is based on forecasts that may turn out to be inaccurate', ['it cannot include objectives', 'banks will not read it', 'it must be published'],
             'Plans rely on assumptions about sales and costs that may be wrong.')],
      exps=[('Explain two benefits to an entrepreneur of preparing a business plan.', 'Planning makes the entrepreneur think through the market, costs and risks before starting, reducing the chance of failure; and it can be used to persuade banks or investors to provide finance.', '2 × (1 mark benefit, 1 mark explanation): clarifies objectives/strategy, identifies risks, raises finance, a benchmark to monitor performance. [4]'),
            ('Explain why a business plan does not guarantee the success of a new business.', 'The plan is based on forecasts and assumptions about demand and costs, which may be wrong, and conditions such as competition or the economy may change after it is written.', '1 mark forecasts/assumptions; 1 mark external change; 1 mark plan must be put into action well. [3]'),
            ('Explain why a business plan should include a section on the marketing strategy.', 'It shows how the business will reach its target customers through product, price, promotion and place, giving evidence that sales forecasts are realistic.', '1 mark how customers are reached (marketing mix); 1 mark supports the sales forecast/persuades lenders. [2]')],
      adv=[('preparing a detailed business plan before launching {newprod}', ['forces managers to research the market', 'helps to obtain finance', 'sets targets to measure progress'],
            ['takes time and money to prepare', 'forecasts may be inaccurate', 'may become out of date quickly'])],
      anl=[('Analyse the sections that {b} should include in a business plan for launching {newprod}.', ['a business plan sets out objectives, strategy and forecasts', 'market research and analysis of competitors', 'the marketing plan for {newprod}', 'cash-flow and profit forecasts to show finance needs']),
           ('Analyse why a bank would want to see a business plan before lending to {b}.', ['a business plan shows the business idea and forecasts', 'evidence that there is demand', 'cash-flow forecasts show whether repayments are affordable', 'it shows the experience and skills of the managers'])],
      ev=[('Evaluate the usefulness of a business plan to {b}.', ['helps to raise finance', 'identifies risks in advance', 'provides targets to monitor performance'],
           ['based on forecasts that may be wrong', 'takes time and may become out of date', 'success depends on carrying the plan out'],
           ['how carefully the research was done', 'how quickly the market changes', 'whether the plan is updated']),
          ('Discuss whether the cash-flow forecast is the most important part of a business plan for {b}.', ['shows if the business can pay its bills', 'needed to persuade lenders', 'identifies when an overdraft is needed'],
           ['the market analysis shows whether there is demand at all', 'objectives and strategy guide all decisions', 'the forecast depends on the sales estimates in other sections'],
           ['who the plan is for', 'how risky the market is', 'the stage of development of the business'])])


t = T(1, 'Social enterprise and the triple bottom line', ['social enterprise and the triple bottom line', 'social enterprise', 'triple bottom line'],
      defs=[('social enterprise', 'A business with mainly social or environmental objectives that reinvests most of its surplus in pursuing those objectives rather than paying it to owners.'),
            ('triple bottom line', 'The three objectives of a social enterprise: economic (profit), social (people) and environmental (planet).')],
      mcqs=[('The "planet" element of the triple bottom line refers to', 'environmental objectives', ['profit objectives', 'social objectives', 'growth objectives'],
             'People, planet and profit: planet means environmental sustainability.'),
            ('A social enterprise differs from a charity mainly because it', 'earns most of its income by selling goods or services', ['has no objectives', 'pays all profits to shareholders', 'cannot employ staff'],
             'Social enterprises trade; charities rely mainly on donations.'),
            ('Which is most likely to be a social enterprise?', 'A café that trains and employs young homeless people and reinvests its profits', ['A multinational oil company', 'A family-owned shoe shop', 'A government ministry'],
             'It trades and pursues a social objective with its surplus.')],
      exps=[('Explain the meaning of the triple bottom line.', 'Social enterprises judge success on three objectives: making a surplus (profit), benefiting people such as employees and communities (social), and protecting the environment (planet).', '1 mark economic; 1 mark social; 1 mark environmental. [3]'),
            ('Explain why a social enterprise still needs to make a profit.', 'It must cover its costs to survive, and the surplus is needed to reinvest in its social or environmental aims and to grow.', '1 mark survival/covering costs; 1 mark surplus funds the social objective. [2]')],
      adv=[('operating as a social enterprise', ['attracts customers who share its values', 'motivated employees', 'may receive grants or support'],
            ['may find it harder to raise finance from investors', 'pursuing social aims can raise costs', 'conflict between profit and social objectives'])],
      anl=[('Analyse how {b} could adopt the triple bottom line.', ['the triple bottom line covers profit, people and planet', 'social aims such as training local workers', 'environmental aims such as reducing waste in producing {prod}', 'profits are still needed to fund these aims']),
           ('Analyse the difficulties a social enterprise in {sector} may face.', ['social enterprises have social as well as financial objectives', 'higher costs from paying fair wages or using sustainable materials', 'harder to attract investors seeking a return', 'conflicts when profit and social aims clash'])],
      ev=[('Evaluate whether {b} should become a social enterprise.', ['stronger brand with ethical consumers', 'more motivated staff', 'access to grants'],
           ['lower returns for owners', 'harder to raise finance', 'higher costs may make it uncompetitive'],
           ['the owners\' objectives', 'how much customers value social aims', 'competition in {sector}'])])


# =====================================================================================
# 2 Business structure
# =====================================================================================

t = T(2, 'Economic sectors: primary, secondary, tertiary and quaternary', ['economic sectors: primary, secondary, tertiary and quaternary', 'economic sectors', 'primary secondary tertiary'],
      defs=[('primary sector', 'Businesses that extract natural resources, such as farming, fishing, forestry and mining.'),
            ('secondary sector', 'Businesses that manufacture or process raw materials into finished goods, including construction.'),
            ('tertiary sector', 'Businesses that provide services to consumers and other businesses, such as retail, banking and tourism.'),
            ('quaternary sector', 'Businesses that provide information and knowledge-based services, such as research, IT and consulting.'),
            ('deindustrialisation', 'The decline in the importance of the secondary (manufacturing) sector in an economy.')],
      mcqs=[('A business that designs software and carries out data analysis for other firms is in the', 'quaternary sector', ['primary sector', 'secondary sector', 'public sector'],
             'Knowledge-based and information services form the quaternary sector.'),
            ('As an economy develops, the share of output from the tertiary sector usually', 'increases', ['falls to zero', 'stays exactly the same', 'is replaced by the primary sector'],
             'Rising incomes increase demand for services.'),
            ('Which business is in the secondary sector?', 'A furniture manufacturer', ['A copper mine', 'A hotel', 'An insurance company'],
             'Manufacturing is secondary sector activity.')],
      exps=[('Explain why the tertiary sector usually grows as a country\'s economy develops.', 'As incomes rise, people spend a larger share on services such as leisure, finance and health; manufacturing may move to lower-cost countries.', '1 mark rising incomes/demand for services; 1 mark example; 1 mark manufacturing moving abroad or productivity changes. [3]'),
            ('Explain one problem for a country caused by deindustrialisation.', 'Manufacturing jobs are lost, causing structural unemployment in regions where factories close, because workers lack the skills for service jobs.', '1 mark problem; 1 mark explanation. [2]')],
      adv=[('operating in the quaternary sector', ['high value added and high margins', 'growing demand for information services', 'low need for physical resources'],
            ['needs highly skilled and expensive staff', 'rapid technological change', 'strong international competition'])],
      anl=[('Analyse how a decline in the primary sector in {country} could affect {b}.', ['the primary sector extracts raw materials', 'raw materials may have to be imported at higher cost', 'supply may be less reliable', 'lower incomes in rural areas may reduce demand']),
           ('Analyse why {b} is classified in the sector it operates in, and how it depends on other sectors.', ['businesses are classified by the main activity', 'it relies on suppliers in other sectors', 'it sells to customers in other sectors', 'all sectors are interdependent in the chain of production'])],
      ev=[('Evaluate the impact on businesses in {country} of a shift in output from the secondary to the tertiary sector.', ['new opportunities for service businesses', 'higher incomes increase demand', 'growth of knowledge-based industries'],
           ['manufacturers face decline and closure', 'structural unemployment', 'dependence on imported goods'],
           ['the sector each business operates in', 'the speed of change', 'government support for retraining'])])


t = T(2, 'Public and private sector organisations', ['public and private sector organisations', 'public sector', 'private sector'],
      defs=[('public sector', 'The part of the economy owned and controlled by the government, such as state-owned enterprises and public services.'),
            ('private sector', 'The part of the economy owned and controlled by individuals and companies, not by the government.'),
            ('privatisation', 'The transfer of a business or industry from the public sector to the private sector.'),
            ('mixed economy', 'An economy in which resources are owned and allocated partly by the private sector and partly by the government.')],
      mcqs=[('Which objective is most likely for a state-owned water company?', 'Providing a reliable service to all households at an affordable price', ['Maximising dividends to shareholders', 'Increasing the share price', 'Closing loss-making rural services'],
             'Public sector organisations usually have social objectives.'),
            ('Which is an argument for privatisation?', 'Private owners have a profit incentive to improve efficiency', ['It guarantees lower prices', 'It always protects jobs', 'It increases government control'],
             'The profit motive encourages efficiency and innovation.'),
            ('A business owned by the government but which sells its services to the public is called', 'a public corporation (state-owned enterprise)', ['a public limited company', 'a franchise', 'a partnership'],
             'Public corporations are in the public sector, unlike plcs.')],
      exps=[('Explain the difference between a public limited company and a public sector organisation.', 'A plc is in the private sector, owned by shareholders who can buy its shares on the stock exchange; a public sector organisation is owned and controlled by the government.', '1 mark plc = private sector, shareholders; 1 mark public sector = government owned. [2]'),
            ('Explain two possible disadvantages of privatising a state-owned electricity company.', 'Prices may rise as owners seek profit; and unprofitable services, such as supplying remote areas, may be cut.', '2 × (1 mark point, 1 mark explanation): higher prices, loss of social objectives, job losses, private monopoly. [4]')],
      adv=[('being privatised after years as a state-owned enterprise', ['profit motive improves efficiency', 'access to private finance for investment', 'less political interference'],
            ['pressure to cut jobs and costs', 'social services may be reduced', 'focus on short-term profit'])],
      anl=[('Analyse how the objectives of {b} might differ from those of a state-owned business in the same industry.', ['private sector firms usually aim for profit and growth', 'state-owned firms often have social objectives', 'private firms respond to shareholders', 'public firms are accountable to the government and taxpayers']),
           ('Analyse the effects on {b} if the government privatises a state-owned competitor.', ['privatisation transfers a business to the private sector', 'the competitor may become more efficient and aggressive', 'prices in the market may fall', 'new investment may raise quality standards'])],
      ev=[('Evaluate whether essential services in {country} should be provided by the private sector rather than the public sector.', ['efficiency from the profit motive', 'more investment and innovation', 'reduced burden on taxpayers'],
           ['prices may rise', 'unprofitable services cut', 'private monopolies may exploit consumers'],
           ['the strength of regulation', 'the type of service', 'the level of competition'])])


t = T(2, 'Legal structures: sole trader, partnership, private and public limited companies', ['legal structures: sole trader, partnership, private and public limited companies', 'legal structures', 'limited companies', 'sole trader'],
      defs=[('sole trader', 'A business owned by one person, who has unlimited liability.'),
            ('partnership', 'A business owned by two or more people who share the risks and profits, usually with unlimited liability.'),
            ('limited liability', 'The owners of a business are not personally liable for its debts; they can lose only the amount they invested.'),
            ('private limited company', 'A company owned by shareholders whose shares cannot be sold to the general public; shareholders have limited liability.'),
            ('public limited company', 'A company whose shares can be bought and sold by the public, usually through a stock exchange.')],
      mcqs=[('Which legal structure gives the owner unlimited liability?', 'Sole trader', ['Private limited company', 'Public limited company', 'Co-operative with limited liability'],
             'Sole traders are personally liable for all debts of the business.'),
            ('A main advantage of converting a private limited company into a public limited company is that it can', 'raise large amounts of capital by selling shares to the public', ['keep its accounts private', 'avoid having shareholders', 'make decisions without a board of directors'],
             'Plcs can sell shares on the stock exchange.'),
            ('Which is a disadvantage of a partnership compared with a sole trader?', 'Disagreements between the partners can slow decisions', ['There is less capital available', 'Fewer skills are available', 'The owner has to work alone'],
             'Shared decision-making can cause conflict.'),
            ('The separation of ownership and control in a public limited company means that', 'the shareholders own the company but directors and managers run it', ['the government owns the company', 'shareholders run the company each day', 'the company has no owners'],
             'Shareholders appoint directors to manage the company.')],
      exps=[('Explain the meaning and importance of limited liability.', 'Shareholders can lose only the money they invested, not their personal possessions; this reduces their risk, so people are more willing to invest in companies.', '1 mark meaning; 1 mark only investment at risk; 1 mark encourages investment/growth. [3]'),
            ('Explain two disadvantages for a sole trader of having unlimited liability.', 'The owner\'s personal assets, such as their house, can be taken to pay business debts; and the risk discourages the owner from expanding or borrowing.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain why a private limited company might choose not to become a public limited company.', 'Its owners would lose control because anyone could buy shares and a takeover becomes possible; it would also face higher costs and must publish more financial information.', '1 mark loss of control/takeover risk; 1 mark cost of flotation; 1 mark disclosure/short-term pressure. [3]'),
            ('Explain the meaning of a separate legal identity (incorporation).', 'A company is a legal person separate from its owners: it can own assets, sign contracts, sue and be sued, and continues to exist when shareholders change.', '1 mark legal person separate from owners; 1 mark example/continuity. [2]')],
      adv=[('converting into a private limited company', ['shareholders have limited liability', 'easier to raise finance from new shareholders', 'continuity – the business survives a change of owners'],
            ['costs of setting up and legal requirements', 'accounts must be published', 'shares cannot be sold to the public']),
           ('becoming a public limited company', ['can raise large sums by selling shares', 'higher status with banks and suppliers', 'shares easier to sell for existing owners'],
            ['risk of takeover', 'expensive to float on the stock exchange', 'pressure from shareholders for short-term profit'])],
      anl=[('Analyse the advantages to the owners of {b} of its current legal structure as a {form}.', ['the legal structure determines ownership, liability and control', 'liability of the owners for business debts', 'ability to raise finance', 'control and decision-making']),
           ('Analyse why the owners of {b} might want to change its legal structure as it grows.', ['growth needs more capital', 'limited liability reduces the owners\' risk', 'more shareholders bring finance', 'a new structure affects control and disclosure'])],
      ev=[('Evaluate whether {b} should become a public limited company to finance its expansion.', ['raises large amounts of capital', 'limited liability and status', 'shares become easier to trade'],
           ['owners may lose control', 'flotation is expensive', 'shareholders may demand short-term profits'],
           ['how much finance is needed', 'whether the owners want to keep control', 'conditions in the stock market']),
          ('Discuss whether a sole trader is the most suitable legal structure for a new business.', ['the owner keeps full control and all profits', 'easy and cheap to set up', 'quick decisions and privacy'],
           ['unlimited liability', 'limited sources of finance', 'business depends on one person'],
           ['the risk involved', 'the finance needed', 'the owner\'s skills and goals'])])


t = T(2, 'Franchises, co-operatives, joint ventures and social enterprises', ['franchises, co-operatives, joint ventures and social enterprises', 'franchises', 'co-operatives', 'joint ventures'],
      defs=[('franchise', 'A business arrangement in which the franchisor allows the franchisee to use its brand name, products and business methods in return for a fee and royalties.'),
            ('co-operative', 'A business owned and controlled by its members, who share the benefits; each member usually has one vote.'),
            ('joint venture', 'An agreement between two or more businesses to work together on a specific project, often by creating a separate business.')],
      mcqs=[('In a franchise agreement, the franchisee usually pays the franchisor', 'an initial fee and a percentage of revenue (royalty)', ['nothing, because the franchisor pays the franchisee', 'a share of the franchisor\'s profits', 'only the cost of the premises'],
             'Franchisees pay for the right to use the brand and system.'),
            ('A key feature of a co-operative is that', 'each member has an equal vote regardless of the money invested', ['shares are sold on the stock exchange', 'it is owned by the government', 'one person has unlimited liability'],
             'One member, one vote.'),
            ('Two companies from different countries set up a new business together to sell electric cars in one of the countries. This is', 'a joint venture', ['a franchise', 'a merger', 'a co-operative'],
             'They share costs, risks and control of the new business.')],
      exps=[('Explain two benefits to a franchisee of buying a franchise rather than starting an independent business.', 'The franchisee uses an established brand that customers already trust, so sales are more likely; and it receives training and support from the franchisor, reducing the risk of failure.', '2 × (1 mark point, 1 mark explanation): established brand, lower risk, training/support, national advertising, easier bank finance. [4]'),
            ('Explain why two businesses might form a joint venture to enter a foreign market.', 'They can share the costs and risks of entering the market, and each brings knowledge or resources, such as local market knowledge and technology.', '1 mark shared costs/risks; 1 mark combined expertise or local knowledge; 1 mark legal access to the market. [3]')],
      adv=[('expanding by selling franchises', ['franchisees provide the capital for new outlets', 'rapid growth with lower risk', 'franchisees are motivated as owners'],
            ['less control over quality', 'poor franchisees damage the brand', 'profit is shared with franchisees']),
           ('forming a joint venture with a business in {newmkt}', ['shares costs and risks', 'gains local market knowledge', 'access to the partner\'s distribution'],
            ['disagreements between partners', 'profits are shared', 'different business cultures'])],
      anl=[('Analyse the benefits to {b} of expanding through franchising.', ['in a franchise, franchisees pay to use the brand and system', 'growth without the capital cost of new outlets', 'franchisees are motivated to succeed', 'royalties provide a steady income']),
           ('Analyse why {b} might choose a joint venture to launch {newprod} in {newmkt}.', ['a joint venture shares ownership and risk', 'the partner has local knowledge of {newmkt}', 'costs of entry are shared', 'possible conflict over control and profit'])],
      ev=[('Evaluate whether franchising is the best method for {b} to grow.', ['fast growth with franchisees\' capital', 'motivated owner-managers', 'less financial risk'],
           ['loss of control over quality', 'shared profits', 'risk to brand reputation'],
           ['how strong and standardised the brand is', 'how quickly it wants to grow', 'its ability to monitor franchisees']),
          ('Discuss whether a joint venture is a better way for {b} to enter {newmkt} than opening its own operations there.', ['shares risks and costs', 'local knowledge', 'faster entry'],
           ['loss of control', 'shared profits', 'partner conflicts'],
           ['how different {newmkt} is from its home market', 'the trust between the partners', 'local laws on foreign ownership'])])


# =====================================================================================
# 3 Size of business
# =====================================================================================

t = T(3, 'Measuring business size: employees, revenue, capital employed, market share', ['measuring business size: employees, revenue, capital employed, market share', 'measuring business size', 'business size'],
      defs=[('market share', 'The sales of one business as a percentage of the total sales of the market in a period.'),
            ('capital employed', 'The total long-term finance invested in a business: equity plus non-current liabilities.'),
            ('revenue', 'The total value of sales in a period: price multiplied by quantity sold.')],
      mcqs=[('Why might the number of employees be a misleading measure of the size of a business?', 'Capital-intensive businesses may have large output with few employees', ['Employees cannot be counted', 'All businesses have the same number of employees', 'It is the same as market share'],
             'Highly automated firms employ few workers but may be very large.'),
            ('Which measure of business size is most useful for comparing businesses in the same market?', 'Market share', ['Number of factories', 'Number of shareholders', 'Age of the business'],
             'Market share compares sales within one market.'),
            ('A market has total sales of $80m. A business has sales of $12m. Its market share is', '15%', ['12%', '6.7%', '85%'],
             '12 ÷ 80 × 100 = 15%.')],
      exps=[('Explain why it is useful to use more than one measure of business size.', 'Each measure can mislead: a capital-intensive business may have few employees and a retailer may have high revenue but low capital employed, so using several measures gives a fairer picture.', '1 mark measures can mislead; 1 mark example; 1 mark combined picture. [3]'),
            ('Explain why profit is not usually used as a measure of business size.', 'Profit depends on efficiency, prices and the state of the economy; a large business may make a loss and a small one a high profit in some years.', '1 mark profit reflects performance not size; 1 mark example/variability. [2]')],
      adv=[('using revenue to compare its size with competitors', ['easy to obtain and understand', 'shows the scale of sales', 'useful within the same industry'],
            ['affected by price levels and inflation', 'does not show profitability', 'misleading across different industries'])],
      anl=[('Analyse which measure of size would be most suitable for comparing {b} with its competitors.', ['size can be measured by employees, revenue, capital employed or market share', 'market share compares firms in the same market', 'number of employees misleads if firms differ in capital intensity', 'revenue is affected by prices']),
           ('Explain why {b} might appear large on one measure of size but small on another.', ['different measures capture different aspects of size', 'capital intensity affects employee numbers', 'prices affect revenue', 'market size affects market share'])],
      ev=[('Evaluate the most appropriate way to measure the size of {b}.', ['market share shows position in the market', 'revenue shows scale of sales', 'capital employed shows investment'],
           ['each measure can mislead', 'comparisons across industries are difficult', 'data may not be available for rivals'],
           ['the purpose of the comparison', 'the industry', 'the data available'])])


@spec(t)
def size_calc(r, D):
    c = B(r)
    names = r.sample(['Alpha', 'Beta', 'Gamma', 'Delta', 'Omega', 'Sigma'], 3)
    rows = []
    for n_ in names:
        emp = step(r, 50, 2000, 10)
        rev = step(r, 5, 300, 1)
        ce = step(r, 5, 400, 5)
        rows.append((n_, emp, rev, ce))
    tot = step(r, max(x[2] for x in rows) * 3, max(x[2] for x in rows) * 8, 10)
    setup = (f'{c["b"]} is comparing three businesses in its market, which has total annual sales of ${tot:,}m: ' +
             '; '.join(f'{n_} – {e:,} employees, revenue ${v}m, capital employed ${k}m' for n_, e, v, k in rows) + '.')
    shares = [x[2] / tot * 100 for x in rows]
    big_e = max(rows, key=lambda x: x[1])[0]
    big_r = max(rows, key=lambda x: x[2])[0]
    big_k = max(rows, key=lambda x: x[3])[0]
    parts = [('Calculate the market share of each business.', '; '.join(f'{x[0]} {pc(s)}' for x, s in zip(rows, shares)),
              '; '.join(f'{x[0]} ${x[2]}m ÷ ${tot:,}m × 100 = {pc(s)}' for x, s in zip(rows, shares)) + ' [2] [2]'),
             ('Identify the largest business using each of the three measures given.', f'Employees: {big_e}; revenue: {big_r}; capital employed: {big_k}',
              f'Employees {big_e} [1]; revenue {big_r} [1]; capital employed {big_k} [1] [3]')]
    if D >= 3:
        rp = [x[2] * 1e6 / x[1] for x in rows]
        parts.append(('Calculate the revenue per employee for each business and explain what this shows.', '; '.join(f'{x[0]} ${v:,.0f}' for x, v in zip(rows, rp)) + '. Higher revenue per employee suggests a more capital-intensive or productive business.',
                      '; '.join(f'{x[0]} ${x[2]}m ÷ {x[1]:,} = ${v:,.0f}' for x, v in zip(rows, rp)) + ' [2]; interpretation [1] [3]'))
    c_, ds = num_opts(lambda x: pc(x), shares[0], [rows[0][2] / sum(x[2] for x in rows) * 100, tot / rows[0][2], 100 - shares[0]])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': (f'What is the market share of {rows[0][0]}?', c_, ds, f'${rows[0][2]}m ÷ ${tot:,}m × 100 = {pc(shares[0])}'),
            'err': (f'calculated the market share of {rows[0][0]} as {pc(rows[0][2] / sum(x[2] for x in rows) * 100)}', 'only the three businesses\' sales were used as the total; market share must use total market sales', pc(shares[0]), f'${rows[0][2]}m ÷ ${tot:,}m × 100', 'market share')}


t = T(3, 'Significance and role of small businesses', ['significance and role of small businesses', 'small businesses', 'small business'],
      defs=[('small business', 'A business with few employees and low revenue and capital compared with others in its industry, often owned and run by the same people.'),
            ('niche market', 'A small, specialised segment of a larger market.')],
      mcqs=[('Which is an advantage that small businesses often have over large businesses?', 'Flexibility and close personal contact with customers', ['Lower average costs from economies of scale', 'Easier access to large bank loans', 'Greater bargaining power with suppliers'],
             'Small firms can respond quickly and offer personal service.'),
            ('Why do governments often support small businesses?', 'They create jobs and encourage competition and innovation', ['They pay the most tax', 'They never fail', 'They have no competitors'],
             'Small firms are an important source of employment and new ideas.'),
            ('Which is a typical problem faced by small businesses?', 'Difficulty in raising finance', ['Too many layers of management', 'Lack of contact with customers', 'Slow decision-making due to bureaucracy'],
             'Banks see small firms as risky and they cannot sell shares publicly.')],
      exps=[('Explain two reasons why small businesses are important to an economy.', 'They create many jobs, especially in local communities; and they increase competition, which keeps prices down and encourages innovation, and some grow into large businesses.', '2 × (1 mark point, 1 mark explanation): jobs, competition, innovation, supply large firms, future large firms. [4]'),
            ('Explain why small businesses can survive in markets dominated by large businesses.', 'They can serve niche markets, offer personal and flexible service, and supply specialist products that large firms find unprofitable.', '1 mark niche; 1 mark personal service/flexibility; 1 mark local knowledge. [3]')],
      adv=[('remaining a small business', ['owners keep control', 'flexible and quick to respond to customers', 'personal relationships with customers'],
            ['higher average costs', 'harder to raise finance', 'vulnerable if a large competitor enters'])],
      anl=[('Analyse how {b} could compete with much larger rivals.', ['small firms lack economies of scale', 'focus on a niche such as {newprod}', 'personal service and flexibility', 'local knowledge and reputation']),
           ('Analyse the problems that {b} may face because of its size.', ['small businesses have limited resources', 'difficulty raising finance', 'higher unit costs', 'dependence on a few customers or the owner'])],
      ev=[('Evaluate whether small businesses such as {b} have a future in an economy dominated by large firms.', ['niche markets', 'flexibility and personal service', 'government support'],
           ['large firms have lower costs', 'online giants reach every market', 'finance is hard to obtain'],
           ['the type of market', 'how far customers value personal service', 'government policy'])])


t = T(3, 'Internal and external growth', ['internal and external growth', 'internal growth', 'external growth'],
      defs=[('internal (organic) growth', 'Expansion of a business by increasing its own output and sales, for example by opening new outlets or launching new products.'),
            ('external growth', 'Expansion of a business by merging with or taking over other businesses.'),
            ('economies of scale', 'Reductions in average cost that result from increasing the scale of production.'),
            ('diseconomies of scale', 'Increases in average cost that result from a business growing too large, often because of communication and coordination problems.')],
      mcqs=[('Which is an example of internal growth?', 'Opening ten new branches funded from retained profit', ['Taking over a rival business', 'Merging with a supplier', 'Buying shares in a competitor to gain control'],
             'Organic growth uses the business\'s own expansion.'),
            ('Which is an example of a purchasing economy of scale?', 'Lower prices per unit for buying materials in bulk', ['Higher wages for skilled staff', 'Poor communication between departments', 'Higher rent in city centres'],
             'Bulk buying lowers unit costs.'),
            ('Which is the most likely cause of diseconomies of scale?', 'Poor communication in a very large organisation', ['Bulk-buying discounts', 'Specialist managers', 'Cheaper borrowing'],
             'Coordination and communication become harder as firms grow.')],
      exps=[('Explain two economies of scale that a growing business might benefit from.', 'Purchasing economies: buying in bulk lowers the cost per unit; financial economies: larger firms can borrow more cheaply because banks see them as less risky.', '2 × (1 mark economy, 1 mark explanation): purchasing, technical, financial, marketing, managerial. [4]'),
            ('Explain why internal growth is often slower but less risky than external growth.', 'Internal growth happens gradually using the firm\'s own resources, so managers keep control and the culture is preserved; external growth is fast but involves integrating another business, which often fails.', '1 mark internal gradual; 1 mark lower risk/control; 1 mark external integration risks. [3]')],
      adv=[('growing internally by opening new outlets', ['managers keep control', 'growth can be financed from profits', 'business culture is preserved'],
            ['growth is slow', 'competitors may grow faster', 'may not provide the scale needed for economies of scale']),
           ('growing much larger', ['economies of scale lower average costs', 'greater market power', 'more security and status'],
            ['diseconomies of scale', 'loss of personal contact with customers', 'greater need for finance'])],
      anl=[('Analyse the benefits to {b} of growing internally rather than externally.', ['internal growth expands the business from within', 'lower risk and less finance needed at once', 'managers keep control and the culture is preserved', 'growth may be too slow if rivals expand quickly']),
           ('Analyse how economies of scale could benefit {b} if it doubles its output of {prod}.', ['economies of scale lower average costs', 'purchasing economies from bulk buying', 'technical economies from larger machinery', 'lower costs allow lower prices or higher margins'])],
      ev=[('Evaluate whether {b} should grow internally or externally.', ['internal: lower risk and control', 'external: fast growth and new markets', 'external gives immediate economies of scale'],
           ['internal is slow', 'external may face integration problems and culture clashes', 'both need finance'],
           ['how fast its market is changing', 'the finance available', 'the availability of suitable targets']),
          ('Discuss whether growth always benefits a business such as {b}.', ['economies of scale', 'more market power', 'security from takeover'],
           ['diseconomies of scale', 'loss of flexibility', 'financial risk from borrowing to grow'],
           ['how growth is managed', 'the market conditions', 'the objectives of the owners'])])


t = T(3, 'Mergers, takeovers and integration: horizontal, vertical, conglomerate', ['mergers, takeovers and integration: horizontal, vertical, conglomerate', 'mergers', 'takeovers', 'integration'],
      defs=[('merger', 'An agreement by the owners of two businesses to join together to form one business.'),
            ('takeover', 'When one business buys a controlling interest (more than 50% of the shares) in another business.'),
            ('horizontal integration', 'Joining with a business in the same industry and at the same stage of production.'),
            ('vertical integration', 'Joining with a business in the same industry but at a different stage of production: backward (towards suppliers) or forward (towards customers).'),
            ('conglomerate integration', 'Joining with a business in a different, unrelated industry.')],
      mcqs=[('A chocolate manufacturer takes over a cocoa farm. This is', 'backward vertical integration', ['forward vertical integration', 'horizontal integration', 'conglomerate integration'],
             'The cocoa farm supplies the manufacturer: integration towards suppliers.'),
            ('Two supermarket chains merge. This is', 'horizontal integration', ['backward vertical integration', 'forward vertical integration', 'conglomerate integration'],
             'Same industry, same stage of production.'),
            ('Which is the main reason for conglomerate integration?', 'To spread risk by operating in different markets', ['To control supplies of raw materials', 'To reduce competition in its own market', 'To gain control of retail outlets'],
             'Diversification spreads risk.'),
            ('A clothing manufacturer buys a chain of clothing shops. This is', 'forward vertical integration', ['backward vertical integration', 'horizontal integration', 'a joint venture'],
             'The shops are closer to the final customer.')],
      exps=[('Explain one reason why many mergers and takeovers fail to achieve their objectives.', 'Different business cultures clash and integrating the two businesses\' systems and staff is harder and more costly than expected, so the planned cost savings do not happen.', '1 mark reason (culture clash/integration problems/overpaying); 1 mark explanation. [2]'),
            ('Explain two benefits of horizontal integration.', 'Economies of scale from combined production and purchasing; and higher market share, which reduces competition and gives more control over prices.', '2 × (1 mark point, 1 mark explanation). [4]'),
            ('Explain the benefits of backward vertical integration to a manufacturer.', 'It secures supplies of materials, gives control over quality and cost of inputs, and the supplier\'s profit margin is absorbed.', '1 mark security of supply; 1 mark control over quality/cost; 1 mark absorb supplier margin. [3]')],
      adv=[('taking over one of its suppliers (backward vertical integration)', ['secure supplies of materials', 'control over quality and delivery', 'supplier profit margin is absorbed'],
            ['high cost of the takeover', 'managers may lack experience of supplying', 'less flexibility to change suppliers']),
           ('merging with a competitor (horizontal integration)', ['economies of scale', 'higher market share', 'removes a competitor'],
            ['culture clashes', 'may be investigated by competition authorities', 'possible redundancies harm morale'])],
      anl=[('Analyse the possible benefits to {b} of a takeover of one of its suppliers.', ['backward vertical integration joins with a supplier', 'secure supply of inputs for {prod}', 'better control of quality and delivery times', 'lower costs as the supplier\'s margin is absorbed']),
           ('Analyse the problems {b} might face after merging with a competitor.', ['a merger combines two businesses', 'culture clashes between staff', 'integration of systems is costly', 'diseconomies of scale and redundancies may damage morale']),
           ('Analyse why {b} might choose conglomerate integration.', ['conglomerate integration joins unrelated businesses', 'spreads risk across markets', 'uses spare finance or management skills', 'managers may lack knowledge of the new industry'])],
      ev=[('Evaluate whether {b} should take over a competitor to increase its market share.', ['economies of scale', 'more market power', 'fast growth'],
           ['high cost and debt', 'integration problems', 'competition authorities may block it'],
           ['the price paid', 'how well the cultures fit', 'the reaction of other competitors']),
          ('Discuss which type of integration would be most beneficial for {b}.', ['horizontal for scale and market share', 'vertical for control of supply or distribution', 'conglomerate to spread risk'],
           ['each carries integration risks', 'vertical reduces flexibility', 'conglomerate needs new expertise'],
           ['its main objective', 'the problems it faces now', 'the targets available'])])


# =====================================================================================
# 4 Business objectives
# =====================================================================================

t = T(4, 'Corporate aims, mission and vision statements', ['corporate aims, mission and vision statements', 'mission statements', 'vision statements', 'corporate aims'],
      defs=[('mission statement', 'A statement of the purpose of a business and what it does, usually describing its values and its customers.'),
            ('vision statement', 'A statement of what a business hopes to achieve or become in the long term.'),
            ('corporate aim', 'A long-term goal of the whole business, from which objectives are set.')],
      mcqs=[('Which is the best description of a vision statement?', 'A statement of what the business wants to become in the future', ['A detailed list of monthly sales targets', 'A summary of last year\'s accounts', 'A description of how to make the product'],
             'Vision statements are long-term and aspirational.'),
            ('A criticism of many mission statements is that they are', 'too vague to guide decisions', ['too detailed', 'secret', 'measured in money'],
             'They are often general public relations statements.'),
            ('Aims differ from objectives because aims are', 'general long-term goals, while objectives are specific targets', ['always measured in money', 'set by employees', 'only for small businesses'],
             'Objectives turn aims into measurable targets.')],
      exps=[('Explain the difference between a mission statement and a vision statement.', 'A mission statement describes the business\'s current purpose and values; a vision statement describes what it hopes to become in the future.', '1 mark mission = present purpose; 1 mark vision = future aspiration. [2]'),
            ('Explain two benefits to a business of having a clear mission statement.', 'It tells employees what the business stands for, which can motivate them and guide their decisions; and it communicates the business\'s values to customers and investors, which can improve its image.', '2 × (1 mark benefit, 1 mark explanation). [4]')],
      adv=[('publishing a mission statement', ['gives employees a sense of purpose', 'communicates values to customers', 'guides setting objectives'],
            ['may be vague public relations', 'costs time to develop', 'ignored if not backed by actions'])],
      anl=[('Analyse how a mission statement could help {b} to achieve its aims.', ['a mission statement sets out purpose and values', 'shared purpose motivates employees', 'guides objectives and strategy', 'builds the image of the business with stakeholders']),
           ('Explain why {b} should review its vision statement as it grows.', ['the vision describes what the business wants to become', 'growth into {newmkt} may change its purpose', 'new stakeholders may expect different values', 'an out-of-date vision fails to guide decisions'])],
      ev=[('Evaluate the importance of a mission statement to the success of {b}.', ['provides direction', 'motivates staff', 'communicates values'],
           ['often vague', 'success depends on strategy and implementation', 'stakeholders may be cynical'],
           ['whether it is backed by actions', 'how well it is communicated', 'the size of the business'])])


t = T(4, 'SMART objectives and the hierarchy of objectives', ['smart objectives and the hierarchy of objectives', 'smart objectives', 'hierarchy of objectives'],
      defs=[('SMART objectives', 'Objectives that are Specific, Measurable, Achievable, Realistic (relevant) and Time-bound.'),
            ('hierarchy of objectives', 'The link from corporate aims to corporate objectives, then to departmental objectives and individual targets.'),
            ('profit maximisation', 'Producing the output at which the difference between total revenue and total cost is greatest.'),
            ('profit satisficing', 'Making enough profit to keep the owners satisfied, rather than the maximum possible.')],
      mcqs=[('Which is the best example of a SMART objective?', 'To increase market share from 12% to 15% within two years', ['To be the best company in the world', 'To make customers happier', 'To grow as fast as possible'],
             'It is specific, measurable and time-bound.'),
            ('Which objective is most likely to be the main aim of a new business in its first year?', 'Survival', ['Maximising shareholder dividends', 'Becoming the market leader', 'Diversifying into new markets'],
             'Most new businesses aim first to survive.'),
            ('In the hierarchy of objectives, departmental objectives should be', 'derived from the corporate objectives', ['set independently of corporate objectives', 'the same for every department', 'set only by employees'],
             'Lower-level objectives support corporate objectives.')],
      exps=[('Explain why objectives should be SMART.', 'Specific and measurable objectives make it clear what must be achieved and allow progress to be checked; time limits create urgency; achievable targets motivate rather than discourage staff.', '1 mark clarity; 1 mark measuring progress; 1 mark motivation/time-bound. [3]'),
            ('Explain why a business might aim for profit satisficing rather than profit maximisation.', 'Owners may want a balance with other goals, such as free time, social aims or good relationships with stakeholders, and maximising profit may harm reputation or staff morale.', '1 mark meaning of satisficing; 1 mark reason (owner lifestyle/stakeholders/CSR). [2]'),
            ('Explain two objectives other than profit that a business may have.', 'Growth, to gain economies of scale and market power; and survival, especially for a new business or in a recession; others include market share, CSR and shareholder value.', '2 × (1 mark objective, 1 mark explanation). [4]')],
      adv=[('setting SMART objectives for each department', ['clear targets for managers', 'progress can be measured', 'coordinates departments towards corporate aims'],
            ['may be too rigid when conditions change', 'targets may be unrealistic and demotivate', 'focus on measurable targets only'])],
      anl=[('Analyse how SMART objectives could improve the performance of {b}.', ['SMART: specific, measurable, achievable, realistic, time-bound', 'clear targets focus effort', 'measurement allows control and corrective action', 'achievable targets motivate staff']),
           ('Analyse why the objectives of {b} might change over time.', ['objectives depend on internal and external factors', 'survival is key when the business is new or in recession', 'growth or market share as it becomes established', 'pressure from stakeholders such as shareholders or the community'])],
      ev=[('Evaluate whether profit should be the main objective of {b}.', ['profit rewards owners', 'provides finance for investment', 'measure of success'],
           ['growth or survival may matter more', 'stakeholders expect social responsibility', 'short-term profit can harm long-term success'],
           ['the legal structure and owners\' wishes', 'the stage of the business', 'competition']),
          ('Discuss the usefulness of SMART objectives to {b}.', ['clarity and focus', 'measurable progress', 'motivation'],
           ['rigid in fast-changing markets', 'not all goals are measurable', 'targets may cause short-termism'],
           ['how quickly its market changes', 'whether staff are involved in setting them', 'how they are monitored'])])


t = T(4, 'Corporate social responsibility (CSR) and ethics', ['corporate social responsibility (csr) and ethics', 'corporate social responsibility', 'ethics'],
      defs=[('corporate social responsibility (CSR)', 'The idea that a business should take account of its impact on society and the environment, not just on its owners.'),
            ('business ethics', 'Moral principles that guide decisions in business, about what is right and wrong.')],
      mcqs=[('Which is an example of an ethical business decision?', 'Refusing to use suppliers that employ child labour, even though they are cheaper', ['Choosing the cheapest supplier regardless of working conditions', 'Raising prices during a shortage', 'Cutting safety checks to reduce costs'],
             'Ethical decisions consider what is morally right, not just cost.'),
            ('A possible benefit to a business of CSR is', 'an improved reputation that attracts customers and employees', ['always lower costs', 'guaranteed higher profits', 'no need to follow laws'],
             'CSR can strengthen the brand and help recruitment.'),
            ('Which is a reason why some businesses do not adopt CSR policies?', 'CSR policies can increase costs and reduce short-term profits', ['They are illegal', 'Customers never care about ethics', 'They reduce sales in every case'],
             'Ethical sourcing or pollution controls can be expensive.')],
      exps=[('Explain why behaving ethically may increase a business\'s costs.', 'Paying fair wages, buying from ethical suppliers or reducing pollution often costs more than the cheapest option.', '1 mark example; 1 mark higher cost explained. [2]'),
            ('Explain two benefits to a business of adopting CSR.', 'It improves the brand image, attracting ethically minded customers; and it helps attract and keep motivated employees who want to work for a responsible business.', '2 × (1 mark benefit, 1 mark explanation). [4]')],
      adv=[('adopting a strong CSR policy', ['better reputation with customers', 'attracts and retains staff', 'reduces risk of legal action and bad publicity'],
            ['higher costs', 'may reduce short-term profit', 'accusations of greenwashing if not genuine'])],
      anl=[('Analyse how adopting CSR could benefit {b}.', ['CSR means considering the impact on society and the environment', 'improved reputation and sales of {prod}', 'more motivated employees and easier recruitment', 'reduced risk of fines and boycotts']),
           ('Analyse the ethical issues {b} may face in its industry.', ['business ethics concern moral principles', 'working conditions of employees and suppliers', 'environmental impact of producing {prod}', 'honesty in marketing and pricing'])],
      ev=[('Evaluate whether {b} should accept higher costs in order to behave more ethically.', ['better reputation and customer loyalty', 'motivated staff', 'reduced legal and reputational risk'],
           ['higher costs reduce profit', 'competitors may undercut prices', 'customers may not pay more'],
           ['how much its customers value ethics', 'the size of the extra costs', 'the actions of competitors']),
          ('Discuss whether CSR is just a public relations exercise.', ['some businesses use CSR mainly to improve image', 'greenwashing', 'CSR spending is often small relative to profit'],
           ['genuine CSR changes how products are made', 'stakeholders and laws demand responsibility', 'long-term benefits to the business'],
           ['how CSR is reported and checked', 'the business culture', 'pressure from stakeholders'])])


t = T(4, 'How objectives change and are communicated', ['how objectives change and are communicated', 'objectives change', 'communicating objectives'],
      defs=[('corporate objectives', 'Specific, measurable goals for the whole business that help it achieve its aims.'),
            ('management by objectives', 'A method of management in which objectives are agreed between managers and employees and progress towards them is reviewed regularly.')],
      mcqs=[('A recession is most likely to make a business change its objective from growth to', 'survival', ['diversification', 'market leadership', 'maximum sales revenue'],
             'Falling demand puts survival first.'),
            ('Why should objectives be communicated to all employees?', 'So that employees understand what they are working towards', ['To keep them secret from managers', 'So that competitors can copy them', 'Because the law requires it in all businesses'],
             'Communication coordinates effort.'),
            ('A business that converts to a public limited company is most likely to place more emphasis on', 'shareholder returns', ['the owner\'s lifestyle', 'social objectives only', 'reducing the number of shareholders'],
             'New shareholders expect dividends and share price growth.')],
      exps=[('Explain two reasons why a business might change its objectives.', 'Changes in the economy, such as a recession, may make survival more important; and a change of ownership or legal structure, such as becoming a plc, brings new shareholders with different expectations.', '2 × (1 mark reason, 1 mark explanation): economy, competition, stage of growth, ownership change, new management. [4]'),
            ('Explain why it is important that objectives are communicated to employees.', 'Employees need to know the targets so their work contributes to them; communication helps coordination and can motivate staff if they feel involved.', '1 mark coordination; 1 mark motivation/involvement. [2]')],
      adv=[('changing its main objective from growth to profitability', ['focus on efficiency and margins', 'more cash for investors', 'reduces risk of overtrading'],
            ['may lose market share', 'staff may be confused', 'may miss growth opportunities'])],
      anl=[('Analyse why {b} might need to change its objectives.', ['objectives depend on internal and external conditions', 'changes in competition or the economy', 'new owners or managers', 'growth into {newmkt} creates new targets']),
           ('Analyse how {b} could communicate its objectives to its employees.', ['objectives must be communicated to be achieved', 'meetings and team briefings', 'targets in appraisals (management by objectives)', 'internal digital communication'])],
      ev=[('Evaluate the importance of communicating objectives to employees at {b}.', ['coordinates effort', 'motivates through involvement', 'targets guide decisions'],
           ['communication takes time', 'objectives must also be realistic and resourced', 'leadership and culture matter more'],
           ['the size of the business', 'the method of communication', 'whether staff are involved in setting objectives'])])


# =====================================================================================
# 5 Stakeholders
# =====================================================================================

t = T(5, 'Internal and external stakeholders and their objectives', ['internal and external stakeholders and their objectives', 'stakeholders', 'internal and external stakeholders'],
      defs=[('stakeholder', 'Any individual or group that has an interest in, or is affected by, the activities of a business.'),
            ('internal stakeholder', 'A stakeholder who is part of the business, such as an employee, manager or owner.'),
            ('external stakeholder', 'A stakeholder outside the business, such as a customer, supplier, lender, the government or the local community.'),
            ('shareholder', 'A person or organisation that owns shares in a limited company.')],
      mcqs=[('Which stakeholder is most interested in a business\'s ability to repay a loan?', 'A bank', ['A customer', 'An employee', 'The local community'],
             'Lenders want repayment with interest.'),
            ('Which of these is an internal stakeholder?', 'A manager', ['A supplier', 'A customer', 'The government'],
             'Managers are part of the organisation.'),
            ('A local community is most likely to be concerned about', 'noise, pollution and local jobs', ['the dividend paid', 'the share price', 'the profit margin'],
             'The community is affected by external costs and benefits.')],
      exps=[('Explain the difference between a stakeholder and a shareholder.', 'A shareholder owns part of a company; a stakeholder is anyone with an interest in or affected by the business, which includes shareholders but also employees, customers and the community.', '1 mark shareholder = owner; 1 mark stakeholder broader with example. [2]'),
            ('Explain the objectives of two different stakeholder groups.', 'Employees want job security, good pay and working conditions; customers want good quality products at fair prices with good service.', '2 × (1 mark group, 1 mark objective explained). [4]')],
      adv=[('taking account of all stakeholders in its decisions', ['better reputation', 'more loyal customers and staff', 'fewer conflicts with the community'],
            ['decisions are slower', 'may reduce profit for shareholders', 'impossible to satisfy everyone'])],
      anl=[('Analyse the objectives of two stakeholder groups of {b}.', ['stakeholders have different interests in the business', 'employees seek pay and job security', 'shareholders or owners seek profit and growth', 'customers want quality {prod} at fair prices']),
           ('Analyse how the local community could be affected by the expansion of {b}.', ['the community is an external stakeholder', 'more jobs and income locally', 'more traffic, noise or pollution', 'demand for local suppliers rises'])],
      ev=[('Evaluate which stakeholder group is most important to {b}.', ['shareholders/owners provide capital and control', 'customers provide revenue', 'employees produce the {prod}'],
           ['importance changes with the decision', 'all are interdependent', 'legal duties to some groups'],
           ['the decision being made', 'the legal structure', 'the power of each group'])])


t = T(5, 'Conflicting stakeholder objectives and their resolution', ['conflicting stakeholder objectives and their resolution', 'conflicting stakeholder objectives', 'stakeholder conflict'],
      defs=[('stakeholder conflict', 'A situation where the objectives of different stakeholder groups cannot all be met at the same time.'),
            ('compromise', 'An agreement in which each side gives up part of what it wants in order to settle a conflict.')],
      mcqs=[('Which is the most likely conflict between stakeholders?', 'Shareholders want higher dividends while employees want higher wages', ['Customers and shareholders both want the business to survive', 'Employees and managers both want good working conditions', 'Suppliers want to be paid on time'],
             'Both claims compete for the same profit.'),
            ('A business decides to close a factory to cut costs. Which stakeholder group is most likely to oppose the decision?', 'Employees at the factory', ['Shareholders', 'Lenders', 'Competitors'],
             'They lose their jobs.'),
            ('Which method is most likely to resolve a conflict between a business and its employees about pay?', 'Negotiation leading to a compromise', ['Ignoring the employees', 'Raising prices to customers', 'Paying shareholders more'],
             'Negotiation and compromise help both sides.')],
      exps=[('Explain one example of conflict between the objectives of two stakeholder groups.', 'Shareholders want lower costs to raise profits, while the local community wants the business to install expensive pollution controls; both cannot be fully satisfied.', '1 mark two groups and objectives; 1 mark why they conflict. [2]'),
            ('Explain how a business might resolve a conflict between its stakeholders.', 'Managers can consult the groups, negotiate a compromise (for example a smaller pay rise linked to productivity), and use stakeholder mapping to prioritise the most powerful groups.', '1 mark consultation/negotiation; 1 mark compromise example; 1 mark prioritise. [3]')],
      adv=[('resolving stakeholder conflict through a compromise', ['maintains good relationships', 'avoids strikes or boycotts', 'decisions are more widely accepted'],
            ['no group gets all it wants', 'negotiations take time', 'may need to be repeated'])],
      anl=[('Analyse a possible conflict between the shareholders and employees of {b}.', ['stakeholder objectives can conflict', 'shareholders want higher profits and dividends', 'employees want pay rises and job security', 'cost-cutting to raise profit may threaten jobs']),
           ('Analyse how {b} could resolve conflicts with the local community about its plans.', ['conflict occurs when objectives clash', 'consultation and communication of plans', 'compromise such as reducing noise or creating local jobs', 'CSR initiatives to rebuild trust'])],
      ev=[('Evaluate how {b} should resolve the conflict between its shareholders and its employees.', ['negotiation and compromise', 'linking pay to productivity', 'communication of the business situation'],
           ['shareholders have legal ownership and power', 'employees may strike', 'compromise satisfies no one fully'],
           ['the power and interest of each group', 'the financial position', 'the long-term objectives'])])


t = T(5, 'Stakeholder mapping: power and interest', ['stakeholder mapping: power and interest', 'stakeholder mapping', 'power and interest'],
      defs=[('stakeholder mapping', 'A way of analysing stakeholders according to their power to influence a business and their interest in its decisions.'),
            ('key players', 'Stakeholders with high power and high interest, who must be closely managed and involved in decisions.')],
      mcqs=[('In a stakeholder map, a group with high power but low interest should be', 'kept satisfied', ['managed closely', 'kept informed', 'monitored with minimum effort'],
             'High power, low interest: keep satisfied.'),
            ('A group with low power and low interest should receive', 'minimal effort (monitor)', ['close management', 'regular consultation', 'the most attention'],
             'They are unlikely to affect the decision.'),
            ('A stakeholder map is most useful because it', 'helps managers decide how to communicate with each stakeholder group', ['measures profit', 'removes all conflict', 'is required by law'],
             'It guides stakeholder management.')],
      exps=[('Explain how a business would use a stakeholder map when planning a new factory.', 'It would place each stakeholder on a grid by power and interest, then involve key players closely, keep powerful groups satisfied and keep interested groups informed.', '1 mark power and interest grid; 1 mark action for key players; 1 mark action for other groups. [3]'),
            ('Explain one limitation of stakeholder mapping.', 'The power and interest of stakeholders change over time and are judged subjectively by managers, so the map may become inaccurate.', '1 mark limitation; 1 mark explanation. [2]')],
      adv=[('using stakeholder mapping before a major decision', ['identifies key players', 'helps plan communication', 'reduces risk of opposition'],
            ['judgements are subjective', 'power and interest change', 'takes time'])],
      anl=[('Analyse how {b} could use stakeholder mapping before launching {newprod}.', ['stakeholder mapping uses power and interest', 'identifies key players such as major customers or investors', 'plans how to keep powerful groups satisfied', 'reduces the risk of opposition delaying the launch']),
           ('Analyse which stakeholders would be key players in a decision by {b} to relocate.', ['key players have high power and high interest', 'employees and their representatives', 'shareholders or owners funding the move', 'the local government that grants permission'])],
      ev=[('Evaluate the usefulness of stakeholder mapping to {b}.', ['focuses attention on key players', 'improves communication', 'anticipates opposition'],
           ['subjective judgements', 'positions change', 'does not resolve conflicts itself'],
           ['how often the map is updated', 'the decision being made', 'the quality of management'])])


# =====================================================================================
# 6 Human resource management
# =====================================================================================

t = T(6, 'Purpose and roles of HRM', ['purpose and roles of hrm', 'human resource management', 'hrm'],
      defs=[('human resource management (HRM)', 'The strategic approach to managing the employees of a business, including workforce planning, recruitment, training, appraisal, pay and employee welfare.'),
            ('workforce', 'All the people employed by a business.'),
            ('appraisal', 'A regular review of an employee\'s performance against agreed targets, usually followed by setting new targets and identifying training needs.')],
      mcqs=[('Which is a main role of the human resources department?', 'Recruiting and training employees', ['Setting the price of products', 'Preparing the cash-flow forecast', 'Designing the advertising campaign'],
             'HRM is responsible for the workforce.'),
            ('A business that treats employees as a valuable asset to be developed is said to use', 'soft HRM', ['hard HRM', 'autocratic leadership', 'scientific management'],
             'Soft HRM focuses on developing and motivating staff.'),
            ('Which is a purpose of employee appraisal?', 'To identify training needs and set new targets', ['To calculate the break-even point', 'To decide the company\'s dividend', 'To choose suppliers'],
             'Appraisal reviews performance and development.')],
      exps=[('Explain two roles of the human resources department.', 'It plans the workforce and recruits and selects staff so the business has the right number of people with the right skills; and it trains and develops employees to improve their performance.', '2 × (1 mark role, 1 mark explanation): workforce planning, recruitment/selection, training, appraisal, pay, welfare, discipline. [4]'),
            ('Explain the difference between hard HRM and soft HRM.', 'Hard HRM treats employees as a resource to be used as cheaply and efficiently as possible, with short-term contracts and little involvement; soft HRM treats them as assets to be developed, motivated and involved in decisions.', '1 mark hard HRM; 1 mark soft HRM; 1 mark contrast/example. [3]')],
      adv=[('adopting a soft HRM approach', ['more motivated and loyal staff', 'lower labour turnover', 'better ideas from involved employees'],
            ['higher training and welfare costs', 'decisions may take longer', 'benefits take time to appear'])],
      anl=[('Analyse how the human resources department could help {b} to achieve its objectives.', ['HRM manages the workforce strategically', 'workforce planning ensures the right number of staff with the right skills', 'training raises productivity and quality', 'good welfare and pay reduce labour turnover']),
           ('Analyse the benefits to {b} of treating its employees as assets rather than costs.', ['soft HRM develops employees', 'higher motivation and productivity', 'lower labour turnover and recruitment costs', 'better customer service and quality of {prod}'])],
      ev=[('Evaluate whether a soft approach to HRM would be more effective than a hard approach for {b}.', ['motivation and loyalty', 'innovation from involved staff', 'lower labour turnover'],
           ['higher costs', 'hard HRM may suit routine, low-skilled work', 'competitive pressure to keep costs low'],
           ['the skills needed in {sector}', 'the financial position', 'the management culture'])])


t = T(6, 'Workforce planning, recruitment and selection', ['workforce planning, recruitment and selection', 'recruitment', 'selection', 'workforce planning'],
      defs=[('workforce planning', 'Analysing the current workforce and forecasting the number and skills of employees the business will need in the future.'),
            ('recruitment', 'The process of identifying the need for a new employee, defining the job and attracting suitable candidates.'),
            ('selection', 'Choosing the most suitable candidate from those who apply, for example by interviews and tests.'),
            ('job description', 'A document that sets out the title, duties and responsibilities of a job.'),
            ('person specification', 'A document that sets out the qualifications, skills, experience and personal qualities required of the person who fills a job.')],
      mcqs=[('Which document lists the skills and qualifications needed by the ideal candidate for a job?', 'Person specification', ['Job description', 'Contract of employment', 'Appraisal form'],
             'The person specification describes the person; the job description describes the job.'),
            ('Which is an advantage of internal recruitment?', 'The candidate already knows the business and its culture', ['It brings in new ideas from outside', 'It creates no vacancy elsewhere', 'There is a wider choice of candidates'],
             'Internal candidates are known and need less induction.'),
            ('A business plans to open five new stores next year. The first step in workforce planning is to', 'forecast the number and skills of employees needed', ['dismiss existing employees', 'set the price of products', 'choose the store designs'],
             'Workforce planning starts with forecasting labour needs.')],
      exps=[('Explain one advantage and one disadvantage of external recruitment.', 'Advantage: it brings in new ideas and skills and a wider choice of candidates. Disadvantage: it is more expensive and slower, and the new employee needs longer induction.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain why a business should carry out workforce planning.', 'It ensures the business has the right number of employees with the right skills when needed, avoiding shortages that reduce output or surpluses that raise costs, and allows time for recruitment and training.', '1 mark right number/skills; 1 mark avoid shortage or surplus; 1 mark time to recruit/train. [3]'),
            ('Explain the difference between a job description and a person specification.', 'A job description describes the job: its title, duties and responsibilities; a person specification describes the qualities, skills and qualifications of the person needed to do it.', '1 mark job description; 1 mark person specification. [2]')],
      adv=[('recruiting managers internally', ['cheaper and faster', 'candidate knows the business', 'motivates staff through promotion'],
            ['fewer new ideas', 'creates another vacancy', 'smaller choice of candidates']),
           ('recruiting staff externally through an online recruitment agency', ['wide choice of candidates', 'new skills and ideas', 'agency saves management time'],
            ['agency fees', 'candidates do not know the business', 'risk of a poor choice'])],
      anl=[('Analyse how {b} could recruit and select the staff it needs for {newprod}.', ['recruitment attracts and selection chooses candidates', 'job description and person specification define the role', 'internal or external advertising', 'interviews, tests and references to select']),
           ('Analyse why workforce planning is important for {b} as it expands into {newmkt}.', ['workforce planning forecasts future labour needs', 'new skills may be needed, such as languages', 'time is needed to recruit and train staff', 'avoids costly shortages or surpluses of staff'])],
      ev=[('Evaluate whether {b} should recruit internally or externally for a new senior manager.', ['internal: knows the business, motivates staff, cheaper', 'external: new ideas and skills', 'external: wider choice'],
           ['internal may lack new ideas', 'external is expensive and riskier', 'external may demotivate internal candidates'],
           ['whether suitable internal candidates exist', 'the need for change', 'the cost and time available']),
          ('Discuss the importance of effective recruitment and selection to {b}.', ['the right staff raise productivity and quality', 'reduces labour turnover', 'saves the cost of a poor appointment'],
           ['training and motivation matter as much', 'process can be expensive and slow', 'interviews may not predict performance'],
           ['the skills required', 'the labour market in {country}', 'the methods used'])])


t = T(6, 'Training: induction, on-the-job and off-the-job', ['training: induction, on-the-job and off-the-job', 'training', 'induction training'],
      defs=[('induction training', 'Training given to new employees to introduce them to the business, its procedures, facilities and colleagues.'),
            ('on-the-job training', 'Training given in the workplace while the employee does the job, for example by watching an experienced worker.'),
            ('off-the-job training', 'Training that takes place away from the workplace, for example at a college or training centre.')],
      mcqs=[('Which is an advantage of on-the-job training?', 'It is relatively cheap and the trainee is productive while learning', ['The trainee learns from external experts', 'There are no mistakes during training', 'It always leads to a qualification'],
             'Trainees work while learning.'),
            ('A new employee spends her first day learning about health and safety and meeting colleagues. This is', 'induction training', ['off-the-job training', 'appraisal', 'job rotation'],
             'Induction introduces new staff to the business.'),
            ('A possible disadvantage of training employees is that', 'trained employees may leave for better-paid jobs with competitors', ['productivity always falls', 'training is illegal', 'trained staff need no supervision'],
             'Training raises an employee\'s value to other employers.')],
      exps=[('Explain why induction training is important.', 'It helps new employees become productive quickly, understand rules such as health and safety, and feel welcome, which reduces the chance of them leaving early.', '1 mark faster productivity; 1 mark procedures/safety; 1 mark lower early labour turnover. [3]'),
            ('Explain one advantage and one disadvantage of off-the-job training.', 'Advantage: experts can teach a wider range of skills without workplace distractions. Disadvantage: it is expensive and the employee is not producing while away.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]')],
      adv=[('investing in off-the-job training for its staff', ['higher skills and productivity', 'improves motivation', 'staff can use new technology'],
            ['expensive', 'lost output while staff are away', 'trained staff may leave']),
           ('using on-the-job training', ['cheap', 'staff learn the specific job', 'output continues during training'],
            ['bad habits may be passed on', 'trainer\'s output falls', 'limited range of skills'])],
      anl=[('Analyse the benefits to {b} of training its employees.', ['training improves employee skills', 'higher productivity and quality of {prod}', 'more motivated staff and lower labour turnover', 'staff can adapt to new technology']),
           ('Analyse which type of training would be most suitable for new staff at {b}.', ['induction, on-the-job and off-the-job training differ', 'induction for procedures and safety', 'on-the-job for specific tasks', 'off-the-job for specialist skills'])],
      ev=[('Evaluate whether {b} should increase its spending on training.', ['higher productivity', 'better quality and service', 'motivation and retention'],
           ['costs and lost output', 'trained staff may leave', 'benefits are hard to measure'],
           ['the skills gap', 'labour turnover', 'the financial position']),
          ('Discuss whether on-the-job training is better than off-the-job training for {b}.', ['cheaper and relevant', 'no lost output', 'learn real tasks'],
           ['limited to existing practices', 'quality depends on the trainer', 'off-the-job gives wider skills'],
           ['the type of skills needed', 'the cost', 'the experience of existing staff'])])


t = T(6, 'Labour turnover, redundancy and dismissal', ['labour turnover, redundancy and dismissal', 'labour turnover', 'redundancy', 'dismissal'],
      defs=[('labour turnover', 'The rate at which employees leave a business, usually measured as the number leaving in a year as a percentage of the average number employed.'),
            ('redundancy', 'When an employee loses their job because the job is no longer needed, not because of the employee\'s conduct.'),
            ('dismissal', 'When an employee is told to leave because of misconduct, incompetence or breaking the contract of employment.')],
      mcqs=[('A business employed an average of 200 workers during the year and 30 left. The labour turnover is', '15%', ['30%', '6.7%', '85%'],
             '30 ÷ 200 × 100 = 15%.'),
            ('Which is the most likely cause of high labour turnover?', 'Low pay and poor working conditions', ['Generous training opportunities', 'High job security', 'Good promotion prospects'],
             'Dissatisfied staff leave.'),
            ('An employee whose job is no longer needed after a factory is automated is', 'made redundant', ['dismissed for misconduct', 'promoted', 'on an induction programme'],
             'Redundancy occurs when the job disappears.')],
      exps=[('Explain two costs to a business of high labour turnover.', 'The costs of recruiting and training replacements; and lower productivity and quality while new staff learn, with possible damage to customer service and morale.', '2 × (1 mark cost, 1 mark explanation). [4]'),
            ('Explain the difference between redundancy and dismissal.', 'Redundancy is when the job is no longer needed, for example because of falling demand or automation; dismissal is when the employee is removed because of their own conduct or performance.', '1 mark redundancy; 1 mark dismissal. [2]'),
            ('Explain why some labour turnover can benefit a business.', 'New employees bring fresh ideas and skills, and turnover allows a business to reduce staff numbers without redundancies or to replace poor performers.', '1 mark new ideas/skills; 1 mark flexibility to adjust the workforce. [2]')],
      adv=[('reducing labour turnover by raising pay', ['lower recruitment and training costs', 'more experienced staff', 'better customer service'],
            ['higher wage costs', 'pay alone may not keep staff', 'fewer new ideas from new staff'])],
      anl=[('Analyse the possible causes of high labour turnover at {b}.', ['labour turnover measures how many staff leave', 'low pay compared with competitors', 'poor working conditions or management', 'lack of training or promotion opportunities']),
           ('Analyse the effects of high labour turnover on {b}.', ['high turnover means many staff leave each year', 'higher recruitment and training costs', 'lower productivity and quality of {prod}', 'lower morale among remaining staff'])],
      ev=[('Evaluate the best way for {b} to reduce its labour turnover.', ['higher pay', 'better training and promotion', 'improved working conditions and management'],
           ['cost of each method', 'causes may be outside the business', 'some turnover is healthy'],
           ['the main reasons staff leave', 'the cost of replacing staff', 'pay in competing businesses'])])


@spec(t)
def lt_calc(r, D):
    c = B(r, 40)
    s0 = max(40, round(c['emp'] * r.uniform(0.85, 1.0) / 10) * 10)
    s1 = s0 + step(r, -s0 // 5, s0 // 5, 10)
    avg = (s0 + s1) / 2
    lv = step(r, max(2, avg * 0.04), avg * 0.35, 1)
    lt = lv / avg * 100
    setup = f'{c["b"]} had {s0:,} employees at the start of the year and {s1:,} at the end. During the year {lv:,} employees left the business.'
    parts = [('Calculate the labour turnover for the year.', pc(lt), f'Average employees ({s0:,} + {s1:,}) ÷ 2 = {avg:,.0f} [1]; {lv:,} ÷ {avg:,.0f} × 100 = {pc(lt)} [1] [2]')]
    if D >= 3:
        cost = step(r, 500, 6000, 100)
        tgt = r.choice([5, 8, 10])
        if lt > tgt:
            fewer = lv - round(avg * tgt / 100)
            parts.append((f'It costs ${cost:,} to recruit and train each replacement. Calculate the saving if labour turnover were cut to {tgt}%.',
                          m(fewer * cost), f'Leavers at {tgt}% = {round(avg * tgt / 100):,} [1]; {fewer:,} fewer × ${cost:,} = {m(fewer * cost)} [1] [2]'))
        parts.append(('Explain one possible reason for this level of labour turnover.', 'E.g. low pay, poor working conditions, lack of training or promotion, poor management, or better jobs elsewhere.', 'Reason [1]; explanation linked to the business [1] [2]'))
    c_, ds = num_opts(pc, lt, [lv / s0 * 100, lv / s1 * 100, avg / lv])
    return {'setup': setup, 'parts': parts, 'c': c, 'anl': lt >= 15,
            'mcq': ('What is the labour turnover for the year?', c_, ds, f'{lv:,} ÷ {avg:,.0f} × 100'),
            'err': (f'calculated labour turnover as {pc(lv / s1 * 100)}', 'the number of employees at the end of the year was used instead of the average number employed', pc(lt), f'{lv:,} ÷ {avg:,.0f} × 100', 'labour turnover') if s1 != s0 else None}


t = T(6, 'Employment contracts and flexible working', ['employment contracts and flexible working', 'employment contracts', 'flexible working'],
      defs=[('contract of employment', 'A legal agreement between an employer and an employee that sets out the terms and conditions of employment, such as pay, hours and duties.'),
            ('flexible working', 'Working arrangements that differ from the standard full-time pattern, such as part-time work, flexitime, job sharing and working from home.'),
            ('zero-hours contract', 'A contract under which the employer does not guarantee any minimum number of working hours.'),
            ('temporary contract', 'A contract of employment for a fixed period of time or for a particular project.')],
      mcqs=[('Which is an example of flexible working?', 'Two employees sharing one full-time job', ['A permanent full-time job with fixed hours', 'A promotion to manager', 'A pay rise'],
             'Job sharing is a flexible arrangement.'),
            ('A benefit to a business of using temporary contracts is that', 'the size of the workforce can be changed quickly to match demand', ['employees are always more motivated', 'training costs are eliminated', 'there is no need to pay wages'],
             'Temporary staff give numerical flexibility.'),
            ('Which is a disadvantage to employees of zero-hours contracts?', 'Their income is uncertain from week to week', ['They must work 40 hours a week', 'They cannot work for other employers', 'They have guaranteed overtime'],
             'Hours are not guaranteed.')],
      exps=[('Explain two benefits to a business of offering flexible working.', 'It can match staff numbers to busy periods, reducing costs; and it attracts and keeps employees, such as parents, who want flexible hours, improving motivation.', '2 × (1 mark benefit, 1 mark explanation). [4]'),
            ('Explain why a contract of employment is important to both the employer and the employee.', 'It sets out the rights and duties of each side, such as pay, hours and notice, which reduces disputes and gives the employee legal protection.', '1 mark terms set out; 1 mark benefit to employer; 1 mark benefit to employee. [3]')],
      adv=[('employing more staff on temporary or zero-hours contracts', ['workforce matches changing demand', 'lower costs in quiet periods', 'easy to reduce staff'],
            ['lower motivation and loyalty', 'less training investment', 'damage to reputation']),
           ('allowing office staff to work from home', ['lower office costs', 'attracts and retains staff', 'less commuting time'],
            ['harder to supervise', 'communication and teamwork suffer', 'IT and security costs'])],
      anl=[('Analyse the advantages to {b} of using flexible working arrangements.', ['flexible working includes part-time, flexitime and home working', 'matches labour to demand, reducing costs', 'attracts a wider range of employees', 'improves motivation and work-life balance']),
           ('Analyse the effects on employees of {b} of a switch to temporary contracts.', ['temporary contracts are for a fixed period', 'less job security', 'lower motivation and loyalty', 'less access to training and promotion'])],
      ev=[('Evaluate whether {b} should employ more of its workers on flexible contracts.', ['flexibility to match demand', 'lower costs', 'attract staff wanting flexibility'],
           ['lower loyalty and motivation', 'less training', 'quality of {prod} may suffer'],
           ['how seasonal its demand is', 'the skills required', 'the labour market'])])


# =====================================================================================
# 7 Motivation
# =====================================================================================

t = T(7, 'Content theories: Maslow, Herzberg and McClelland', ['content theories: maslow, herzberg and mcclelland', 'maslow', 'herzberg', 'mcclelland'],
      defs=[('motivation', 'The factors that make a person work willingly and well to achieve goals.'),
            ('hygiene factors', 'In Herzberg\'s theory, aspects of work such as pay, working conditions and supervision that cause dissatisfaction if they are inadequate but do not motivate in themselves.'),
            ('motivators', 'In Herzberg\'s theory, factors such as achievement, recognition, responsibility and the work itself that lead to job satisfaction and motivation.'),
            ('hierarchy of needs', 'Maslow\'s theory that people have five levels of needs – physiological, safety, social, esteem and self-actualisation – which they seek to satisfy in order.')],
      mcqs=[('According to Herzberg, which is a hygiene factor?', 'Pay', ['Recognition', 'Responsibility', 'Achievement'],
             'Pay prevents dissatisfaction but does not motivate in Herzberg\'s theory.'),
            ('In Maslow\'s hierarchy, which need is at the top?', 'Self-actualisation', ['Safety', 'Social', 'Physiological'],
             'Self-actualisation is reaching one\'s full potential.'),
            ('McClelland\'s theory identifies the need for achievement, the need for affiliation and the need for', 'power', ['money', 'safety', 'hygiene'],
             'Achievement, affiliation and power.'),
            ('An employee with job security and a pension scheme has satisfied which of Maslow\'s needs?', 'Safety needs', ['Esteem needs', 'Self-actualisation', 'Social needs'],
             'Security is a safety need.')],
      exps=[('Explain the difference between hygiene factors and motivators in Herzberg\'s theory.', 'Hygiene factors such as pay and conditions prevent dissatisfaction if they are good enough but do not motivate; motivators such as recognition and responsibility come from the job itself and create satisfaction and motivation.', '1 mark hygiene factors; 1 mark motivators; 1 mark contrast with examples. [3]'),
            ('Explain one limitation of Maslow\'s hierarchy of needs for managers.', 'People do not always satisfy needs in the same order and it is hard to know which level each employee is at, so it is difficult to use in practice.', '1 mark limitation; 1 mark explanation. [2]'),
            ('Explain how a manager could use McClelland\'s theory to motivate employees.', 'Give employees with a high need for achievement challenging tasks and feedback, those with a need for affiliation teamwork, and those with a need for power leadership roles.', '1 mark identify the need; 1 mark matching job design; 1 mark second need applied. [3]')],
      adv=[('using Herzberg\'s motivators, such as more responsibility, to motivate its staff', ['higher job satisfaction', 'better quality of work', 'lower labour turnover'],
            ['some staff do not want responsibility', 'training costs', 'hygiene factors must be right first'])],
      anl=[('Analyse how {b} could use Maslow\'s hierarchy of needs to motivate its employees.', ['Maslow\'s five levels of needs', 'fair pay and safe conditions meet lower needs', 'teamwork meets social needs', 'recognition and promotion meet esteem and self-actualisation needs']),
           ('Analyse how Herzberg\'s two-factor theory could help managers at {b} improve motivation.', ['hygiene factors and motivators', 'improve hygiene factors to remove dissatisfaction', 'job enrichment and recognition to motivate', 'motivated staff raise productivity'])],
      ev=[('Evaluate the usefulness of Herzberg\'s two-factor theory to the managers of {b}.', ['shows pay alone does not motivate', 'focus on job design and recognition', 'helps reduce dissatisfaction'],
           ['based on limited research', 'individuals differ', 'pay may motivate low-paid workers'],
           ['the type of work', 'the employees\' needs', 'the resources available']),
          ('Discuss whether Maslow\'s hierarchy of needs is still useful to businesses today.', ['simple framework', 'reminds managers that needs differ', 'links rewards to needs'],
           ['needs are not always in order', 'cultural differences', 'hard to measure'],
           ['the workforce', 'how it is applied', 'other theories used alongside it'])])


t = T(7, 'Process theory: Vroom\'s expectancy theory; Taylor\'s scientific management', ["process theory: vroom's expectancy theory; taylor's scientific management", 'vroom', 'taylor', 'expectancy theory'],
      defs=[('scientific management', 'Taylor\'s approach of studying tasks to find the most efficient method, training workers in it and paying them by results.'),
            ('expectancy theory', 'Vroom\'s theory that motivation depends on whether employees believe effort will lead to performance (expectancy), performance will lead to a reward (instrumentality) and the reward is valued (valence).'),
            ('piece rate', 'A payment system in which workers are paid a fixed amount for each unit they produce.')],
      mcqs=[('Taylor believed that workers were mainly motivated by', 'money', ['recognition', 'social needs', 'self-actualisation'],
             'Scientific management assumes economic motivation.'),
            ('In Vroom\'s theory, valence refers to', 'how much the employee values the reward', ['the belief that effort leads to performance', 'the belief that performance leads to reward', 'the amount of pay'],
             'Valence is the value of the reward to the individual.'),
            ('A criticism of Taylor\'s scientific management is that it', 'treats workers like machines and ignores social needs', ['is too expensive to apply', 'ignores productivity', 'has no link to pay'],
             'Repetitive tasks reduce job satisfaction.')],
      exps=[('Explain the main features of Taylor\'s scientific management.', 'Tasks are studied (time and motion) to find the most efficient method, workers are trained to follow it and are paid by results such as piece rates, with close supervision.', '1 mark time and motion/best method; 1 mark training/supervision; 1 mark pay by results. [3]'),
            ('Explain the three elements of Vroom\'s expectancy theory.', 'Expectancy: effort will lead to better performance; instrumentality: performance will be rewarded; valence: the employee values the reward. Motivation is high only if all three are strong.', '1 mark each for expectancy, instrumentality and valence. [3]')],
      adv=[('applying Taylor\'s scientific management to its production line', ['higher productivity', 'lower unit costs', 'clear methods and targets'],
            ['boring, repetitive work', 'high labour turnover', 'quality may fall as workers rush'])],
      anl=[('Analyse how {b} could use Vroom\'s expectancy theory to improve motivation.', ['motivation depends on expectancy, instrumentality and valence', 'training so staff believe they can reach targets', 'clear links between performance and rewards', 'rewards that employees value']),
           ('Analyse the likely effects of introducing scientific management at {b}.', ['Taylor studied tasks to find the most efficient method', 'productivity rises in routine tasks', 'workers may become demotivated by repetitive work', 'labour relations may suffer'])],
      ev=[('Evaluate whether Taylor\'s approach to motivation is relevant to {b} today.', ['useful for routine, measurable tasks', 'pay by results raises output', 'efficiency gains'],
           ['ignores social and esteem needs', 'not suitable for creative work', 'quality and morale may suffer'],
           ['the type of work', 'the skills of employees', 'the culture'])])


t = T(7, 'Financial methods of motivation: piece rate, commission, bonus, profit sharing', ['financial methods of motivation: piece rate, commission, bonus, profit sharing', 'financial methods of motivation', 'piece rate', 'commission'],
      defs=[('commission', 'A payment to a salesperson based on a percentage of the value of sales they make.'),
            ('bonus', 'An extra payment, in addition to basic pay, given for reaching a target.'),
            ('profit sharing', 'A scheme in which part of the business\'s profit is distributed to employees.'),
            ('performance-related pay', 'A payment system that links part of an employee\'s pay to how well they perform against agreed targets.')],
      mcqs=[('Which payment method is most suitable for a salesperson?', 'Commission', ['Piece rate', 'Time rate only', 'Profit sharing only'],
             'Commission rewards the value of sales.'),
            ('A disadvantage of piece-rate pay is that', 'workers may rush and quality may fall', ['output always falls', 'it cannot be measured', 'it guarantees a fixed income'],
             'Paying per unit encourages quantity over quality.'),
            ('Profit sharing is most likely to', 'encourage employees to identify with the success of the whole business', ['reward individual effort directly', 'reduce the business\'s costs', 'be paid weekly'],
             'Employees share in overall profit.')],
      exps=[('Explain one advantage and one disadvantage of paying production workers a piece rate.', 'Advantage: it encourages higher output because pay rises with production. Disadvantage: workers may rush, reducing quality, and income is uncertain if machines break down.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain why financial rewards may not motivate all employees.', 'According to Herzberg pay is a hygiene factor: once pay is fair, extra money may not motivate, and many employees value recognition, responsibility or security more.', '1 mark Herzberg/hygiene; 1 mark other needs valued. [2]')],
      adv=[('introducing a profit-sharing scheme', ['employees identify with the business', 'encourages cooperation', 'may reduce labour turnover'],
            ['reward is not linked to individual effort', 'payments vary and may be small', 'reduces profit for owners']),
           ('paying sales staff on commission', ['motivates staff to sell more', 'pay is linked to results', 'lower fixed costs'],
            ['staff may use pushy selling', 'income is uncertain', 'may ignore customer service'])],
      anl=[('Analyse how financial rewards could improve the motivation of employees at {b}.', ['financial methods include piece rate, commission, bonus and profit sharing', 'pay linked to output or sales encourages effort', 'bonuses for targets focus effort', 'profit sharing builds identity with the business']),
           ('Analyse the problems {b} might face if it pays its workers by piece rate.', ['piece rate pays per unit produced', 'quality may fall as workers rush', 'difficult to apply to team or service work', 'conflict if rates are cut'])],
      ev=[('Evaluate whether financial rewards are the best way to motivate employees at {b}.', ['money meets basic needs', 'direct link to performance', 'easy to understand'],
           ['pay is a hygiene factor', 'may encourage short-term behaviour', 'non-financial methods may motivate more'],
           ['the type of job', 'the pay level now', 'what employees value'])])


@spec(t)
def pay_calc(r, D):
    c = B(r)
    n_ = pp(r)
    kind = r.randrange(3)
    if kind == 0:
        rate = step(r, 20, 150, 5) / 100
        units = step(r, 300, 1500, 10)
        basic = step(r, 50, 200, 10)
        pay = basic + rate * units
        setup = f'{n_}, a production worker at {c["b"]}, is paid a basic wage of ${basic} a week plus ${rate:.2f} for each unit produced. Last week {n_} produced {units:,} units.'
        parts = [(f'Calculate {n_}\'s pay for the week.', m2(pay), f'{units:,} × ${rate:.2f} = {m2(rate * units)} [1]; + ${basic} = {m2(pay)} [1] [2]')]
        if D >= 3:
            q2 = round(units * 1.1)
            parts.append((f'Calculate the percentage increase in pay if output rises by 10%.', pc((basic + rate * q2 - pay) / pay * 100), f'New pay ${basic} + {q2:,} × ${rate:.2f} = {m2(basic + rate * q2)} [1]; increase ÷ {m2(pay)} × 100 = {pc((basic + rate * q2 - pay) / pay * 100)} [1] [2]'))
        mc = ('What is the pay for the week?', *num_opts(m2, pay, [rate * units, basic + units, basic * rate * units]), f'${basic} + {units:,} × ${rate:.2f}')
        err = (f'calculated the weekly pay as {m2(rate * units)}', 'the basic wage was left out', m2(pay), f'${basic} + {units:,} × ${rate:.2f}', 'weekly pay')
    elif kind == 1:
        basic = step(r, 800, 3000, 50)
        rate = r.choice([2, 2.5, 3, 4, 5, 6])
        sales = step(r, 20000, 120000, 500)
        pay = basic + sales * rate / 100
        setup = f'{n_} is a sales representative for {c["b"]}. {n_} earns a basic salary of ${basic:,} a month plus commission of {rate:g}% on the value of sales. Sales last month were ${sales:,}.'
        parts = [(f'Calculate {n_}\'s total pay for the month.', m(pay), f'Commission {rate:g}% × ${sales:,} = {m(sales * rate / 100)} [1]; + ${basic:,} = {m(pay)} [1] [2]')]
        if D >= 3:
            tgt = round(pay * 1.2 / 10) * 10
            need = (tgt - basic) / (rate / 100)
            parts.append((f'Calculate the value of sales {n_} would need next month to earn ${tgt:,}.', m(need), f'(${tgt:,} − ${basic:,}) ÷ {rate:g}% = {m(need)} [2] [2]'))
        mc = ('What is the total monthly pay?', *num_opts(m, pay, [sales * rate / 100, basic * (1 + rate / 100), basic + sales * rate / 10]), f'${basic:,} + {rate:g}% × ${sales:,}')
        err = (f'calculated the total pay as {m(basic + sales * rate / 10)}', f'the commission was calculated at {rate * 10:g}% instead of {rate:g}% (decimal point error)', m(pay), f'${basic:,} + {rate:g}/100 × ${sales:,}', 'total pay')
    else:
        prof = step(r, c['emp'] * 2000, c['emp'] * 20000, 1000)
        sh = r.choice([5, 8, 10, 12, 15])
        emp = c['emp']
        pool = prof * sh / 100
        per = pool / emp
        setup = f'{c["b"]} made a profit of ${prof:,} last year. It shares {sh}% of profit equally among its {emp:,} employees.'
        parts = [('Calculate the profit-sharing payment received by each employee.', m2(per), f'{sh}% × ${prof:,} = {m(pool)} [1]; ÷ {emp:,} = {m2(per)} [1] [2]')]
        if D >= 3:
            parts.append(('Explain one reason why the profit-sharing scheme may not motivate individual employees.', 'The payment is not linked to each person\'s effort, is paid only once a year and may be small, so some employees free-ride on others.', 'Reason [1]; explanation [1] [2]'))
        mc = ('What is the payment to each employee?', *num_opts(m2, per, [pool, prof / emp, pool / emp / 10]), f'{sh}% × ${prof:,} ÷ {emp:,}')
        err = (f'calculated the payment per employee as {m2(prof / emp)}', f'the whole profit was divided among the employees instead of only {sh}% of it', m2(per), f'{sh}% × ${prof:,} ÷ {emp:,}', 'payment per employee')
    return {'setup': setup, 'parts': parts, 'c': c, 'mcq': mc, 'err': err}


t = T(7, 'Non-financial methods: job enrichment, empowerment, teamwork', ['non-financial methods: job enrichment, empowerment, teamwork', 'non-financial methods', 'job enrichment', 'empowerment'],
      defs=[('job enrichment', 'Redesigning a job to give the employee more responsibility, a complete unit of work and more challenging tasks.'),
            ('job enlargement', 'Increasing the number of tasks an employee does at the same level of responsibility.'),
            ('job rotation', 'Moving employees between different tasks or jobs at the same level.'),
            ('empowerment', 'Giving employees the authority and resources to make decisions about their own work.')],
      mcqs=[('Giving a team of workers responsibility for organising their own work schedule and checking quality is an example of', 'empowerment', ['piece rate', 'job rotation', 'autocratic leadership'],
             'Workers are given authority to make decisions.'),
            ('Job enrichment differs from job enlargement because job enrichment', 'adds more responsibility and challenge', ['only adds more tasks at the same level', 'reduces the number of tasks', 'is a financial reward'],
             'Enrichment is vertical; enlargement is horizontal.'),
            ('Which theory most supports the use of job enrichment?', 'Herzberg\'s two-factor theory', ['Taylor\'s scientific management', 'Theory X', 'The break-even model'],
             'Responsibility and achievement are Herzberg motivators.')],
      exps=[('Explain the difference between job enrichment and job rotation.', 'Job enrichment gives the employee more responsibility and more challenging work; job rotation moves the employee between tasks at the same level, giving variety but not more responsibility.', '1 mark enrichment; 1 mark rotation; 1 mark contrast (responsibility). [3]'),
            ('Explain two benefits of teamworking for a business.', 'Employees share skills and ideas, improving problem solving and quality; and working in a team meets social needs, raising motivation and reducing absence.', '2 × (1 mark benefit, 1 mark explanation). [4]')],
      adv=[('empowering employees to make decisions', ['faster decisions', 'higher motivation', 'better use of staff knowledge'],
            ['some staff lack the skills or want no responsibility', 'risk of poor decisions', 'managers may resist losing control']),
           ('organising production in self-managed teams', ['shared skills and ideas', 'social needs met', 'flexibility'],
            ['conflict within teams', 'some members may not contribute', 'training is needed'])],
      anl=[('Analyse how job enrichment could improve motivation at {b}.', ['job enrichment adds responsibility and challenge', 'meets Herzberg\'s motivators and esteem needs', 'higher quality and productivity', 'lower labour turnover']),
           ('Analyse the possible difficulties of introducing empowerment at {b}.', ['empowerment gives staff authority to make decisions', 'staff need training and confidence', 'managers may resist losing control', 'mistakes are possible while staff learn'])],
      ev=[('Evaluate whether non-financial methods would be more effective than financial methods in motivating employees at {b}.', ['meet higher-level needs', 'long-lasting effect', 'improve quality and ideas'],
           ['pay must be adequate first', 'some staff prefer money', 'costs of training and redesign'],
           ['the type of work', 'current pay levels', 'the culture of the business'])])


# =====================================================================================
# 8 Management
# =====================================================================================

t = T(8, 'Functions of management: Fayol and Mintzberg', ['functions of management: fayol and mintzberg', 'functions of management', 'fayol', 'mintzberg'],
      defs=[('management', 'Getting things done through other people by planning, organising, commanding, coordinating and controlling resources.'),
            ('Mintzberg\'s management roles', 'Mintzberg\'s ten roles of managers, grouped as interpersonal, informational and decisional roles.')],
      mcqs=[('Which is one of Fayol\'s functions of management?', 'Planning', ['Selling', 'Producing', 'Advertising'],
             'Fayol: planning, organising, commanding, coordinating, controlling.'),
            ('In Mintzberg\'s model, a manager who handles a crisis such as a strike is acting as', 'a disturbance handler (decisional role)', ['a figurehead (interpersonal role)', 'a monitor (informational role)', 'a spokesperson (informational role)'],
             'Dealing with unexpected problems is a decisional role.'),
            ('Comparing actual results with targets and taking corrective action is the management function of', 'controlling', ['commanding', 'planning', 'coordinating'],
             'Control means checking performance against plans.')],
      exps=[('Explain two of Fayol\'s functions of management.', 'Planning: setting objectives and deciding how to achieve them; controlling: measuring performance against plans and taking corrective action.', '2 × (1 mark function, 1 mark explanation). [4]'),
            ('Explain how Mintzberg\'s view of management differs from Fayol\'s.', 'Fayol describes what managers should do in a logical sequence; Mintzberg observed what managers actually do – a variety of interpersonal, informational and decisional roles carried out in short, fragmented activities.', '1 mark Fayol prescriptive functions; 1 mark Mintzberg observed roles; 1 mark example. [3]')],
      adv=[('managers spending more time on planning', ['clear direction', 'better use of resources', 'fewer crises'],
            ['less time for day-to-day problems', 'plans may become out of date', 'slower response to change'])],
      anl=[('Analyse how the managers of {b} could use Fayol\'s functions of management when launching {newprod}.', ['Fayol\'s functions: planning, organising, commanding, coordinating, controlling', 'planning objectives and resources for the launch', 'organising and coordinating departments', 'controlling progress against targets']),
           ('Analyse which of Mintzberg\'s roles would be most important for the managing director of {b}.', ['Mintzberg identified interpersonal, informational and decisional roles', 'figurehead and leader roles with staff and stakeholders', 'monitor and spokesperson roles for information', 'entrepreneur and disturbance-handler roles in decisions'])],
      ev=[('Evaluate whether Mintzberg\'s roles are more useful than Fayol\'s functions in explaining the work of managers at {b}.', ['Mintzberg reflects what managers actually do', 'covers interpersonal and information roles', 'suits fast-changing businesses'],
           ['Fayol gives a clear framework', 'planning and control remain essential', 'both are generalisations'],
           ['the level of the manager', 'the nature of the business', 'how fast its environment changes'])])


t = T(8, 'Leadership styles: autocratic, democratic, laissez-faire', ['leadership styles: autocratic, democratic, laissez-faire', 'leadership styles', 'autocratic', 'democratic'],
      defs=[('autocratic leadership', 'A style in which the leader makes decisions alone and tells employees what to do, with little consultation.'),
            ('democratic leadership', 'A style in which the leader involves employees in discussion and decision-making.'),
            ('laissez-faire leadership', 'A style in which the leader gives employees broad objectives and leaves them to make most decisions themselves.'),
            ('paternalistic leadership', 'A style in which the leader makes decisions but considers what is best for employees, like a parent.')],
      mcqs=[('Which leadership style is most suitable in an emergency requiring a quick decision?', 'Autocratic', ['Democratic', 'Laissez-faire', 'Consultative with a full vote'],
             'Autocratic leaders decide quickly.'),
            ('A manager who asks staff for ideas and lets them vote on the final decision is using', 'democratic leadership', ['autocratic leadership', 'paternalistic leadership', 'scientific management'],
             'Staff are involved in the decision.'),
            ('Laissez-faire leadership is most likely to succeed with', 'a team of highly skilled, self-motivated professionals', ['new, untrained employees', 'staff who need close supervision', 'a business in crisis'],
             'Skilled staff can work independently.')],
      exps=[('Explain one advantage and one disadvantage of democratic leadership.', 'Advantage: employees feel valued and contribute ideas, raising motivation and the quality of decisions. Disadvantage: decisions take longer because of consultation.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain why no single leadership style is best in all situations.', 'The best style depends on the task, the urgency of the decision and the skills and attitudes of the employees: autocratic suits crises, democratic suits skilled teams.', '1 mark depends on situation; 1 mark example; 1 mark second example. [3]')],
      adv=[('adopting a democratic leadership style', ['better ideas from staff', 'higher motivation', 'decisions more accepted'],
            ['slower decisions', 'managers may lose control', 'not suitable in a crisis']),
           ('using an autocratic leadership style', ['quick decisions', 'clear lines of control', 'useful in a crisis'],
            ['low motivation', 'staff ideas are not used', 'high labour turnover'])],
      anl=[('Analyse which leadership style would be most suitable for the managers of {b}.', ['autocratic, democratic and laissez-faire styles differ in staff involvement', 'the skills of the workforce', 'the urgency of decisions in {sector}', 'the effect on motivation and productivity']),
           ('Analyse the effects on employees of {b} if the new managing director adopts an autocratic style.', ['autocratic leaders decide without consultation', 'faster decisions and clear instructions', 'lower motivation as ideas are ignored', 'possible increase in labour turnover'])],
      ev=[('Evaluate the most appropriate leadership style for {b} in its current situation.', ['autocratic for quick decisions', 'democratic for motivation and ideas', 'laissez-faire for creative skilled staff'],
           ['each has drawbacks', 'style should match the situation', 'leaders may need to change style'],
           ['the urgency of the situation', 'the skills of the employees', 'the culture of the business']),
          ('Discuss whether a democratic leadership style always improves business performance.', ['better motivation', 'more ideas', 'staff commitment to decisions'],
           ['slow decisions', 'not suitable for unskilled staff or crises', 'conflict among staff'],
           ['the task', 'employee skills', 'the time available'])])


t = T(8, 'McGregor\'s Theory X and Theory Y', ["mcgregor's theory x and theory y", 'theory x', 'theory y', 'mcgregor'],
      defs=[('Theory X', 'McGregor\'s view that managers assume workers dislike work, avoid responsibility and must be controlled and motivated mainly by pay.'),
            ('Theory Y', 'McGregor\'s view that managers assume workers can enjoy work, seek responsibility and are motivated by achievement.')],
      mcqs=[('A Theory X manager is most likely to', 'supervise employees closely', ['delegate responsibility widely', 'encourage staff to set their own targets', 'use laissez-faire leadership'],
             'Theory X assumes workers must be controlled.'),
            ('A Theory Y manager believes that workers', 'want responsibility and can be creative', ['are lazy and avoid work', 'only work for money', 'must be closely supervised'],
             'Theory Y is a positive view of workers.'),
            ('McGregor\'s theory is about', 'managers\' attitudes towards workers', ['methods of production', 'pricing strategies', 'sources of finance'],
             'Theory X and Y describe managers\' assumptions.')],
      exps=[('Explain how a manager\'s view of workers could affect the leadership style used.', 'A Theory X manager is likely to be autocratic and supervise closely; a Theory Y manager is likely to be democratic and delegate.', '1 mark Theory X → autocratic; 1 mark Theory Y → democratic/delegation. [2]'),
            ('Explain why Theory X assumptions could become a self-fulfilling prophecy.', 'If workers are treated as lazy, closely controlled and given no responsibility, they become demotivated and behave in the way the manager expected.', '1 mark close control; 1 mark demotivation; 1 mark behaviour confirms assumption. [3]')],
      adv=[('managers adopting Theory Y assumptions', ['staff given responsibility become more motivated', 'more ideas and creativity', 'less supervision needed'],
            ['some staff may abuse freedom', 'needs trust and training', 'not suitable for all tasks'])],
      anl=[('Analyse how managers at {b} with Theory Y attitudes might affect employee performance.', ['Theory Y assumes workers seek responsibility', 'delegation and empowerment', 'higher motivation and creativity', 'lower supervision costs']),
           ('Explain how Theory X attitudes could cause problems at {b}.', ['Theory X assumes workers dislike work', 'close supervision and little trust', 'low motivation and initiative', 'high labour turnover'])],
      ev=[('Evaluate whether managers at {b} should adopt Theory Y rather than Theory X attitudes.', ['better motivation', 'creativity', 'lower supervision costs'],
           ['some workers prefer clear instructions', 'routine tasks may need control', 'risk of abuse of trust'],
           ['the type of work', 'the workforce', 'the culture'])])


t = T(8, 'Emotional intelligence (Goleman)', ['emotional intelligence (goleman)', 'emotional intelligence', 'goleman'],
      defs=[('emotional intelligence', 'The ability of a person to understand and manage their own emotions and to recognise and influence the emotions of others.'),
            ('empathy', 'The ability to understand and share the feelings of other people.')],
      mcqs=[('Which is one of Goleman\'s competencies of emotional intelligence?', 'Self-awareness', ['Time and motion study', 'Financial literacy', 'Piece-rate pay'],
             'Goleman: self-awareness, self-management, social awareness, relationship management.'),
            ('A manager who recognises that a team member is stressed and adjusts her approach is showing', 'social awareness (empathy)', ['autocratic leadership', 'scientific management', 'Theory X'],
             'Recognising others\' emotions is social awareness.'),
            ('Emotional intelligence is important for leaders mainly because it helps them to', 'build good relationships and motivate others', ['calculate profit', 'set prices', 'reduce inventory'],
             'Leaders work through people.')],
      exps=[('Explain why emotional intelligence is important for a manager.', 'Managers work through people; understanding their own and others\' emotions helps them communicate, resolve conflict and motivate staff.', '1 mark understanding emotions; 1 mark effect on relationships/motivation. [2]'),
            ('Explain two of Goleman\'s competencies of emotional intelligence.', 'Self-awareness: understanding one\'s own emotions and their effect on others; relationship management: using this understanding to influence, inspire and manage conflict.', '2 × (1 mark competency, 1 mark explanation). [4]')],
      adv=[('training its managers in emotional intelligence', ['better relationships with staff', 'improved motivation and teamwork', 'fewer conflicts'],
            ['training costs', 'hard to measure the benefit', 'some managers may resist'])],
      anl=[('Analyse how emotional intelligence could help the managers of {b} manage change.', ['emotional intelligence: understanding own and others\' emotions', 'empathy with staff worried about change', 'better communication reduces resistance', 'relationship management builds commitment']),
           ('Explain why emotional intelligence might be more important than technical skills for senior managers at {b}.', ['senior managers lead through others', 'motivating and inspiring staff', 'managing conflict between stakeholders', 'technical tasks can be delegated'])],
      ev=[('Evaluate the importance of emotional intelligence for the managers of {b}.', ['better relationships', 'effective leadership', 'managing conflict and change'],
           ['technical and planning skills also needed', 'difficult to measure and train', 'results also depend on resources'],
           ['the level of management', 'the type of business', 'the situation the business faces'])])


# =====================================================================================
# 9 The nature of marketing
# =====================================================================================

t = T(9, 'Role of marketing and the marketing objectives', ['role of marketing and the marketing objectives', 'role of marketing', 'marketing objectives'],
      defs=[('marketing', 'The management process of identifying, anticipating and satisfying customer requirements profitably.'),
            ('marketing objective', 'A target for the marketing department, such as increasing market share or sales, that supports the corporate objectives.'),
            ('market orientation', 'An approach in which a business bases its decisions on the needs and wants of customers, identified by market research.'),
            ('product orientation', 'An approach in which a business concentrates on making a product it believes is good and then tries to sell it.')],
      mcqs=[('Which is a marketing objective?', 'To increase market share from 8% to 10% in two years', ['To reduce labour turnover to 5%', 'To cut the time taken to pay suppliers', 'To reduce the gearing ratio'],
             'Marketing objectives relate to sales, market share and brand.'),
            ('A market-oriented business would first', 'carry out market research into what customers want', ['develop the product its engineers prefer', 'set the lowest possible price', 'build a new factory'],
             'Market orientation starts with customers.'),
            ('Marketing objectives should be linked to', 'the corporate objectives of the business', ['the objectives of competitors', 'the views of suppliers only', 'last year\'s advertising budget only'],
             'Departmental objectives support corporate objectives.')],
      exps=[('Explain the difference between market orientation and product orientation.', 'A market-oriented business finds out what customers want through research and then develops products to meet those needs; a product-oriented business develops products it thinks are good and then looks for customers.', '1 mark market orientation; 1 mark product orientation; 1 mark contrast/example. [3]'),
            ('Explain how marketing objectives are linked to corporate objectives.', 'Marketing objectives are set to help achieve the corporate objectives; for example, a corporate objective of growth may lead to a marketing objective of raising sales by 15% in new markets.', '1 mark derived from corporate objectives; 1 mark example. [2]'),
            ('Explain why marketing must be coordinated with other departments.', 'Marketing plans depend on operations to produce enough goods, finance to fund promotion and HR to provide trained staff; without coordination promises to customers cannot be met.', '1 mark operations; 1 mark finance or HR; 1 mark consequence. [3]')],
      adv=[('becoming more market oriented', ['products match customer needs', 'higher sales and loyalty', 'fewer failed products'],
            ['market research is expensive', 'customers may not know what they want', 'frequent changes increase costs'])],
      anl=[('Analyse how the marketing department could help {b} achieve its corporate objectives.', ['marketing identifies and satisfies customer needs', 'market research guides product development such as {newprod}', 'promotion and pricing raise sales and market share', 'marketing objectives turn corporate aims into targets']),
           ('Analyse the benefits to {b} of a market-oriented approach.', ['market orientation bases decisions on customer needs', 'products such as {prod} match what customers want', 'higher sales and customer loyalty', 'early warning of changing tastes'])],
      ev=[('Evaluate whether {b} should be market oriented rather than product oriented.', ['meets customer needs', 'lower risk of product failure', 'competitive advantage'],
           ['research costs', 'innovative products may come from product orientation', 'customers may not know future needs'],
           ['the nature of {sector}', 'the pace of technological change', 'competition']),
          ('Discuss the importance of setting marketing objectives for {b}.', ['provide focus and targets', 'coordinate the marketing mix', 'measure success'],
           ['objectives may be unrealistic', 'external changes', 'the marketing budget matters more'],
           ['how the objectives link to corporate aims', 'resources available', 'market conditions'])])


t = T(9, 'Demand, supply and market equilibrium', ['demand, supply and market equilibrium', 'demand', 'supply', 'market equilibrium'],
      defs=[('demand', 'The quantity of a product that consumers are willing and able to buy at each price in a given time period.'),
            ('supply', 'The quantity of a product that producers are willing and able to sell at each price in a given time period.'),
            ('equilibrium price', 'The price at which the quantity demanded equals the quantity supplied, so the market clears.'),
            ('excess demand', 'A situation where, at the current price, the quantity demanded is greater than the quantity supplied.')],
      mcqs=[('Which would cause the demand curve for a product to shift to the right?', 'An increase in consumer incomes for a normal good', ['A rise in the price of the product', 'A rise in the cost of raw materials', 'A new tax on producers'],
             'Income changes shift demand; price changes move along the curve.'),
            ('A rise in the cost of raw materials will most likely', 'shift the supply curve to the left and raise the equilibrium price', ['shift the demand curve to the right', 'lower the equilibrium price', 'have no effect on supply'],
             'Higher costs reduce supply at each price.'),
            ('If the price is set above the equilibrium price, there will be', 'excess supply', ['excess demand', 'a shortage', 'no effect'],
             'Quantity supplied exceeds quantity demanded.'),
            ('A successful advertising campaign for a product will most likely', 'increase demand, raising both price and quantity', ['reduce supply', 'reduce demand', 'lower the equilibrium quantity'],
             'Demand shifts right.')],
      exps=[('Explain two factors that could cause the demand for a product to increase.', 'A rise in consumer incomes increases demand for normal goods; and a rise in the price of a substitute makes this product relatively cheaper, so more is bought.', '2 × (1 mark factor, 1 mark explanation): income, price of substitutes/complements, tastes, advertising, population. [4]'),
            ('Explain how a fall in supply affects the equilibrium price and quantity.', 'The supply curve shifts left; at the original price there is excess demand, so the price rises until a new equilibrium is reached at a higher price and a lower quantity.', '1 mark shift left; 1 mark excess demand at old price; 1 mark higher price, lower quantity. [3]')],
      adv=[('a sharp rise in demand for its {prod}', ['higher sales and revenue', 'can raise prices', 'better use of capacity'],
            ['capacity may be insufficient', 'new competitors enter', 'rising input costs'])],
      anl=[('Analyse how a rise in the cost of raw materials could affect the market for {prod} and {b}.', ['supply falls when costs rise', 'the supply curve shifts left', 'the equilibrium price rises and quantity falls', 'the effect on revenue depends on how customers respond to price']),
           ('Analyse the factors that could increase demand for {bp} {prod}.', ['demand depends on price and other factors', 'rising incomes in {country}', 'changes in tastes and fashion', 'advertising and prices of substitutes'])],
      ev=[('Evaluate the likely impact on {b} of a large increase in the number of suppliers in its market.', ['supply rises and price falls', 'more choice for customers', 'pressure to cut costs'],
           ['{b} may differentiate its {prod}', 'demand may also be rising', 'loyal customers may stay'],
           ['the strength of its brand', 'whether demand is growing', 'its cost position'])])


@spec(t)
def sd_calc(r, D):
    c = B(r)
    prices = sorted(r.sample([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14], 5))
    k = r.randrange(1, 4)
    pe = prices[k]
    qe = step(r, 300, 3000, 50)
    a = r.choice([50, 100, 150, 200])
    b_ = r.choice([50, 100, 150, 200])
    qd = [qe + a * (k - i) for i in range(5)]
    qs = [qe + b_ * (i - k) for i in range(5)]
    if min(qd + qs) <= 0:
        return None
    rows = '; '.join(f'price ${p}: demand {d:,}, supply {s:,}' for p, d, s in zip(prices, qd, qs))
    good = r.choice(['bottles of fruit juice', 'loaves of bread', 'bags of rice', 'phone cases', 'cinema tickets', 'kilograms of tomatoes', 'bunches of flowers', 'notebooks'])
    setup = f'{c["b"]} is studying a local market. Weekly demand and supply of {good} at different prices are: {rows} (quantities in units).'
    lo = prices[k - 1]
    hi = prices[k + 1]
    parts = [('Identify the equilibrium price and quantity.', f'${pe}; {qe:,} units', f'Price ${pe} [1]; quantity {qe:,} [1] [2]'),
             (f'Calculate the excess demand or excess supply if the price is ${lo}.', f'Excess demand of {qd[k - 1] - qs[k - 1]:,} units', f'{qd[k - 1]:,} − {qs[k - 1]:,} [1]; = excess demand {qd[k - 1] - qs[k - 1]:,} [1] [2]'),
             (f'Calculate the excess demand or excess supply if the price is ${hi}.', f'Excess supply of {qs[k + 1] - qd[k + 1]:,} units', f'{qs[k + 1]:,} − {qd[k + 1]:,} [1]; = excess supply {qs[k + 1] - qd[k + 1]:,} [1] [2]')]
    if D >= 3:
        parts.append(('Explain what will happen to the price if it is set at the higher of these two prices.', 'There is excess supply, so sellers cut prices to clear unsold stock until the price falls back to equilibrium.', 'Excess supply [1]; price falls to equilibrium [1] [2]'))
        parts.append(('Calculate the total revenue of all sellers at the equilibrium.', m(pe * qe), f'${pe} × {qe:,} = {m(pe * qe)} [1] [1]'))
    c_, ds = num_opts(lambda x: f'${int(x)}', pe, [lo, hi, prices[0]])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the equilibrium price?', c_, ds, f'Demand = supply = {qe:,} at ${pe}'),
            'err': (f'stated that at a price of ${lo} there is excess supply of {qd[k - 1] - qs[k - 1]:,} units', 'below the equilibrium price quantity demanded exceeds quantity supplied, so it is excess demand', f'excess demand of {qd[k - 1] - qs[k - 1]:,} units', f'{qd[k - 1]:,} − {qs[k - 1]:,}', 'answer')}


t = T(9, 'Market size, growth and market share', ['market size, growth and market share', 'market size', 'market growth', 'market share'],
      defs=[('market size', 'The total volume or value of sales in a market in a given period.'),
            ('market growth', 'The percentage change in the size of a market over a period of time.'),
            ('market share', 'The percentage of total market sales made by one business or brand.'),
            ('market leader', 'The business or brand with the largest market share.')],
      mcqs=[('A market grew from $40m to $46m in one year. The market growth rate is', '15%', ['6%', '13%', '87%'],
             '(46 − 40) ÷ 40 × 100 = 15%.'),
            ('A business\'s sales rise by 10% but the market grows by 20%. Its market share will', 'fall', ['rise', 'stay the same', 'double'],
             'Its sales grew more slowly than the market.'),
            ('Why is market share important to a business?', 'A high share can give economies of scale and power over retailers', ['It is the same as profit', 'It removes all competition', 'It is required by law'],
             'Market leadership brings advantages.')],
      exps=[('Explain why a business could have rising sales but a falling market share.', 'If the market is growing faster than the business\'s sales, its sales are a smaller percentage of the market, so its share falls even though sales rise.', '1 mark market grows faster; 1 mark share = sales/market. [2]'),
            ('Explain two benefits to a business of being the market leader.', 'Economies of scale lower costs; and retailers want to stock the leading brand, giving it more shelf space and bargaining power.', '2 × (1 mark benefit, 1 mark explanation). [4]')],
      adv=[('aiming to increase its market share', ['economies of scale', 'stronger brand and power over retailers', 'barrier to new competitors'],
            ['price cuts may reduce profit', 'heavy promotion spending', 'competitors may retaliate'])],
      anl=[('Analyse why market share is an important measure of performance for {b}.', ['market share is sales as a percentage of the market', 'shows performance relative to rivals', 'a high share gives economies of scale', 'retailers and investors value market leaders']),
           ('Analyse how {b} could increase its market share.', ['market share depends on sales relative to the market', 'competitive pricing', 'promotion and product improvements such as {newprod}', 'new distribution channels'])],
      ev=[('Evaluate whether increasing market share should be the main marketing objective of {b}.', ['economies of scale', 'brand strength', 'barrier to entry'],
           ['profit may matter more', 'market may be declining', 'costs of winning share'],
           ['whether the market is growing', 'the reaction of competitors', 'corporate objectives'])])


@spec(t)
def mkt_calc(r, D):
    c = B(r)
    m0 = step(r, 20, 900, 5)
    g = r.choice([-8, -5, -4, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    m1 = round(m0 * (1 + g / 100), 1)
    s0 = round(m0 * r.uniform(0.05, 0.35), 1)
    sg = g + r.choice([-6, -4, -2, 2, 4, 6, 8])
    s1 = round(s0 * (1 + sg / 100), 1)
    sh0, sh1 = s0 / m0 * 100, s1 / m1 * 100
    grow = (m1 - m0) / m0 * 100
    setup = f'The market for {c["prod"]} in {c["country"]} was worth ${m0}m in 2024 and ${m1:g}m in 2025. Sales of {c["b"]} were ${s0:g}m in 2024 and ${s1:g}m in 2025.'
    parts = [('Calculate the market growth rate between 2024 and 2025.', pc(grow), f'(${m1:g}m − ${m0}m) ÷ ${m0}m × 100 [1]; = {pc(grow)} [1] [2]'),
             (f'Calculate the market share of {c["b"]} in each year.', f'2024 {pc(sh0)}; 2025 {pc(sh1)}', f'${s0:g}m ÷ ${m0}m × 100 = {pc(sh0)} [1]; ${s1:g}m ÷ ${m1:g}m × 100 = {pc(sh1)} [1] [2]')]
    if D >= 3:
        parts.append((f'Explain what the results show about the performance of {c["b"]}.', f'Its market share {"rose" if sh1 > sh0 else "fell"} because its sales grew {"faster" if sh1 > sh0 else "more slowly"} than the market.',
                      f'Share {"rose" if sh1 > sh0 else "fell"} [1]; comparison of sales growth with market growth [1] [2]'))
    c_, ds = num_opts(pc, grow, [(m1 - m0) / m1 * 100, m1 / m0 * 100, (s1 - s0) / s0 * 100])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the market growth rate between 2024 and 2025?', c_, ds, f'(${m1:g}m − ${m0}m) ÷ ${m0}m × 100'),
            'err': (f'calculated the market growth rate as {pc((m1 - m0) / m1 * 100)}', 'the change was divided by the 2025 value instead of the original (2024) value', pc(grow), f'(${m1:g}m − ${m0}m) ÷ ${m0}m × 100', 'growth rate')}


t = T(9, 'Mass vs niche marketing and market segmentation', ['mass vs niche marketing and market segmentation', 'niche marketing', 'mass marketing', 'market segmentation'],
      defs=[('mass marketing', 'Selling the same product to the whole market with one marketing strategy.'),
            ('niche marketing', 'Identifying and targeting a small, specialised segment of a larger market.'),
            ('market segmentation', 'Dividing a market into groups of consumers with similar characteristics, such as age, income, location or lifestyle.')],
      mcqs=[('Dividing customers into groups by age and income is', 'demographic segmentation', ['geographic segmentation', 'mass marketing', 'product orientation'],
             'Age and income are demographic characteristics.'),
            ('Which is an advantage of niche marketing for a small business?', 'It can avoid direct competition with large firms', ['It gives the largest economies of scale', 'It reaches the whole market', 'It has the lowest risk if tastes change'],
             'Large firms may ignore small niches.'),
            ('A disadvantage of mass marketing is that', 'the product may not fully satisfy any particular group', ['it cannot achieve economies of scale', 'it costs nothing', 'it is illegal'],
             'One product for everyone may not meet specific needs.')],
      exps=[('Explain two benefits to a business of segmenting its market.', 'It can design products and promotions that meet the needs of each group more precisely, raising sales; and it can identify gaps in the market and avoid wasting promotion on people unlikely to buy.', '2 × (1 mark benefit, 1 mark explanation). [4]'),
            ('Explain one risk of niche marketing.', 'The business depends on a small group of customers, so if their tastes change or a large rival enters the niche, sales may fall sharply.', '1 mark risk; 1 mark explanation. [2]')],
      adv=[('targeting a niche market with {newprod}', ['less competition from large firms', 'higher prices possible', 'customer loyalty'],
            ['small market limits growth', 'no economies of scale', 'dependent on one segment']),
           ('moving from niche to mass marketing', ['larger sales volume', 'economies of scale', 'lower unit costs'],
            ['strong competition', 'loss of specialist image', 'heavy promotion spending'])],
      anl=[('Analyse how {b} could segment its market.', ['segmentation divides customers into groups', 'demographic segments such as age and income', 'geographic segments such as {country} and {newmkt}', 'psychographic segments by lifestyle']),
           ('Analyse the benefits to {b} of targeting a niche market.', ['niche marketing targets a small segment', 'less competition and higher prices', 'specialist image and loyalty', 'suits a business with limited resources'])],
      ev=[('Evaluate whether {b} should use niche marketing or mass marketing for {newprod}.', ['niche: less competition, higher margins', 'mass: economies of scale', 'mass: larger sales'],
           ['niche limits growth', 'mass faces intense competition', 'mass needs large promotion budgets'],
           ['the size of the target market', 'its resources', 'the strength of competitors'])])


t = T(9, 'Consumer vs industrial markets; customer relationship marketing', ['consumer vs industrial markets; customer relationship marketing', 'customer relationship marketing', 'industrial markets', 'consumer markets'],
      defs=[('consumer market', 'A market for goods and services bought by individuals for their own use.'),
            ('industrial (business-to-business) market', 'A market for goods and services bought by businesses to use in producing other goods or services.'),
            ('customer relationship marketing (CRM)', 'Using marketing activities to build long-term relationships with customers so that they remain loyal.')],
      mcqs=[('Which is an example of an industrial market?', 'A steel company selling steel to a car manufacturer', ['A supermarket selling bread to shoppers', 'A cinema selling tickets', 'A café selling coffee'],
             'The buyer uses the steel in production.'),
            ('A main aim of customer relationship marketing is to', 'keep existing customers loyal', ['find the cheapest supplier', 'reduce the number of customers', 'cut the price of every product'],
             'Retaining customers is cheaper than finding new ones.'),
            ('Buyers in industrial markets usually', 'buy in large quantities and focus on reliability and price', ['buy on impulse', 'are influenced mainly by celebrity advertising', 'buy very small quantities'],
             'Industrial buying is rational and specification-based.')],
      exps=[('Explain one difference between marketing to consumers and marketing to industrial buyers.', 'Industrial buyers purchase in large quantities on technical specifications, price and reliability, so personal selling and relationships matter; consumer marketing uses mass advertising and branding to influence individual buyers.', '1 mark industrial approach; 1 mark consumer approach. [2]'),
            ('Explain two methods of customer relationship marketing.', 'Loyalty schemes that reward repeat purchases; and personalised communication, such as emails based on past purchases, that makes customers feel valued.', '2 × (1 mark method, 1 mark explanation). [4]')],
      adv=[('introducing a customer relationship marketing programme', ['customer loyalty and repeat sales', 'cheaper than winning new customers', 'feedback to improve products'],
            ['cost of systems and staff', 'data protection issues', 'customers may still switch for price'])],
      anl=[('Analyse how {b} could use customer relationship marketing to increase sales.', ['CRM builds long-term relationships', 'loyalty schemes encourage repeat purchases', 'personalised offers using customer data', 'excellent service and after-sales support']),
           ('Analyse how marketing {prod} to business customers differs from marketing to consumers.', ['industrial markets buy for production', 'larger orders and fewer buyers', 'personal selling and negotiated prices', 'reliability and technical support matter most'])],
      ev=[('Evaluate whether customer relationship marketing is worthwhile for {b}.', ['loyalty and repeat sales', 'lower cost than new customers', 'useful data'],
           ['costs of technology and staff', 'customers may still switch', 'privacy concerns'],
           ['how competitive the market is', 'the value of repeat customers', 'how well data is used'])])


# =====================================================================================
# 10 Market research
# =====================================================================================

t = T(10, 'Primary and secondary market research methods', ['primary and secondary market research methods', 'primary research', 'secondary research', 'market research'],
      defs=[('market research', 'The process of collecting, recording and analysing data about customers, competitors and markets.'),
            ('primary research', 'The collection of first-hand data that did not exist before, for a specific purpose, e.g. by questionnaires, interviews and focus groups.'),
            ('secondary research', 'The use of data that has already been collected for another purpose, e.g. government statistics, reports and websites.'),
            ('focus group', 'A small group of people who are asked to discuss their views on a product or idea in depth.')],
      mcqs=[('Which is an example of primary research?', 'A survey of customers in the business\'s shops', ['Government population statistics', 'A published market report', 'A competitor\'s annual report'],
             'The business collects the data itself.'),
            ('An advantage of secondary research is that it is usually', 'cheaper and quicker to obtain', ['specific to the business\'s needs', 'always up to date', 'unavailable to competitors'],
             'The data already exists.'),
            ('Qualitative research is most likely to provide', 'customers\' opinions and reasons for buying', ['the exact number of units sold', 'the market share of each business', 'the average price in the market'],
             'Qualitative data concerns opinions and attitudes.')],
      exps=[('Explain one advantage and one disadvantage of primary research.', 'Advantage: the data is up to date and collected for the business\'s exact purpose. Disadvantage: it is expensive and time-consuming to collect.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain the difference between quantitative and qualitative research.', 'Quantitative research collects numerical data, such as how many people would buy; qualitative research collects opinions and reasons, such as why people prefer a brand.', '1 mark quantitative; 1 mark qualitative. [2]'),
            ('Explain why a new business might use secondary research before primary research.', 'Secondary data is cheaper and quicker and gives an overview of the market size and competitors, which helps the business decide what primary research it needs.', '1 mark cheaper/quicker; 1 mark overview guides primary research. [2]')],
      adv=[('using online surveys for primary research', ['cheap and quick', 'reaches many people', 'easy to analyse'],
            ['sample may not be representative', 'low response rates', 'answers may be careless']),
           ('using focus groups to test {newprod}', ['detailed opinions', 'reasons behind views', 'ideas for improvements'],
            ['small sample', 'dominant members may influence others', 'expensive per person'])],
      anl=[('Analyse the market research methods {b} could use before launching {newprod}.', ['market research reduces the risk of a new product', 'secondary research on market size and competitors', 'primary research such as surveys and focus groups', 'test marketing in one area']),
           ('Explain the advantages to {b} of using secondary research about {newmkt}.', ['secondary research uses existing data', 'cheap and quick to obtain', 'gives market size and trends in {newmkt}', 'helps plan primary research'])],
      ev=[('Evaluate whether {b} should use primary research or secondary research before entering {newmkt}.', ['primary is specific and up to date', 'secondary is cheap and quick', 'secondary gives an overview of the market'],
           ['primary is expensive and slow', 'secondary may be out of date or irrelevant', 'both may be needed'],
           ['the budget', 'how different {newmkt} is', 'the time available'])])


t = T(10, 'Sampling methods and sample size', ['sampling methods and sample size', 'sampling methods', 'sample size'],
      defs=[('sample', 'A group of people chosen from the target population to take part in market research.'),
            ('random sampling', 'A sampling method in which every member of the target population has an equal chance of being selected.'),
            ('quota sampling', 'A sampling method in which the population is divided into groups and a set number of people is chosen from each group.'),
            ('stratified sampling', 'A method in which the population is divided into groups (strata) and a random sample is chosen from each in proportion to its size.')],
      mcqs=[('Which sampling method gives every member of the population an equal chance of selection?', 'Random sampling', ['Quota sampling', 'Convenience sampling', 'Snowball sampling'],
             'Random sampling is unbiased in selection.'),
            ('A larger sample size is likely to', 'increase the reliability of the results', ['reduce the cost of research', 'make results less accurate', 'remove all bias'],
             'Larger samples reduce sampling error but cost more.'),
            ('An interviewer is told to question 50 men and 50 women in a shopping centre. This is', 'quota sampling', ['random sampling', 'stratified random sampling', 'secondary research'],
             'Fixed numbers from each group.')],
      exps=[('Explain why businesses use samples rather than asking the whole population.', 'Asking everyone would be too expensive and take too long; a representative sample gives reasonably accurate results at a much lower cost.', '1 mark cost/time; 1 mark representative sample gives accurate enough results. [2]'),
            ('Explain one advantage and one disadvantage of quota sampling.', 'Advantage: it is quick and ensures each group is represented. Disadvantage: interviewers choose who to ask, which can introduce bias.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]')],
      adv=[('increasing the sample size of its customer survey', ['more reliable results', 'smaller sampling error', 'can analyse sub-groups'],
            ['higher cost', 'takes longer', 'bias in method still possible'])],
      anl=[('Analyse which sampling method {b} should use for research into {newprod}.', ['sampling methods differ in cost and bias', 'random sampling avoids selection bias', 'quota sampling is quick and represents key groups', 'sample size affects reliability and cost']),
           ('Explain the factors {b} should consider when deciding its sample size.', ['larger samples are more reliable', 'cost and time of research', 'how varied the target population is', 'the risk of the decision'])],
      ev=[('Evaluate the factors that would affect the reliability of a market research survey carried out by {b}.', ['sample size and method', 'question design', 'response rate'],
           ['even good samples can be biased', 'opinions change', 'cost limits the sample'],
           ['the budget', 'how the sample is selected', 'the purpose of the research'])])


t = T(10, 'Presenting and analysing data: averages, range and charts', ['presenting and analysing data: averages, range and charts', 'averages', 'presenting data', 'analysing data'],
      defs=[('mean', 'The arithmetic average: the sum of the values divided by the number of values.'),
            ('median', 'The middle value when the data are arranged in order.'),
            ('mode', 'The value that occurs most frequently in a set of data.'),
            ('range', 'The difference between the highest and the lowest values in a set of data.')],
      mcqs=[('Which chart is best for showing the market shares of different businesses?', 'A pie chart', ['A line graph', 'A scatter graph', 'A break-even chart'],
             'Pie charts show proportions of a whole.'),
            ('Which average is least affected by one very large value?', 'The median', ['The mean', 'The total', 'The range'],
             'Extreme values affect the mean more.'),
            ('A line graph is most suitable for showing', 'sales over several years', ['the proportion of customers by age', 'the number of shops in each country only', 'one figure'],
             'Line graphs show trends over time.')],
      exps=[('Explain why the mean may be misleading when a set of data contains an extreme value.', 'The mean includes every value, so one very high or low value pulls it away from the typical value; the median would better represent the data.', '1 mark extreme value distorts mean; 1 mark median better. [2]'),
            ('Explain why a business might present market research data in charts rather than tables.', 'Charts make patterns and comparisons easier to see quickly, helping managers understand results and communicate them to others.', '1 mark easier to see patterns; 1 mark aids decisions/communication. [2]')],
      adv=[('presenting its sales data as charts', ['trends are easy to see', 'quick to understand', 'useful in presentations'],
            ['detail may be lost', 'charts can be misleading if scales are chosen badly', 'takes time to prepare'])],
      anl=[('Analyse how {b} could use averages and the range to interpret its market research data.', ['averages show a typical value', 'the mean uses all data but is affected by extremes', 'the median and mode are less affected', 'the range shows the spread of views']),
           ('Explain how {b} could present its market research results to its managers.', ['charts and tables summarise data', 'pie charts for proportions', 'line graphs for trends', 'bar charts for comparisons'])],
      ev=[('Evaluate the usefulness of statistical analysis of market research data to {b}.', ['summarises large amounts of data', 'shows trends and typical values', 'supports decisions with evidence'],
           ['depends on the quality of the data', 'averages hide variation', 'qualitative factors ignored'],
           ['the sample used', 'the methods chosen', 'the judgement of managers'])])


@spec(t)
def avg_calc(r, D):
    c = B(r)
    n_ = 7 if D <= 2 else (9 if D <= 4 else 11)
    what = r.choice([('the number of times each person visited a café last month', '', (2, 10)), ('the price in dollars each person said they would pay for ' + c['newprod'], '$', (5, 60)),
                     ('the number of minutes each person spends on social media each day', '', (10, 60)), ('how many kilometres each person travels to the nearest shopping centre', '', (2, 25))])
    base = step(r, *what[2], 1)
    vals = [base + r.randint(0, base) for _ in range(n_)]
    dup = r.choice(vals)
    vals[r.randrange(n_)] = dup
    vals[r.randrange(n_)] = dup
    from collections import Counter
    cnt = Counter(vals)
    top = cnt.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        return None
    mode = top[0][0]
    srt = sorted(vals)
    med = srt[n_ // 2]
    mean = sum(vals) / n_
    rng = max(vals) - min(vals)
    u = what[1]
    setup = f'{c["b"]} asked {n_} people {what[0]}. The answers were: {", ".join(u + str(v) for v in vals)}.'
    parts = [('Calculate the mean.', f'{u}{mean:.2f}', f'Total {u}{sum(vals)} ÷ {n_} [1]; = {u}{mean:.2f} [1] [2]'),
             ('Identify the median and the mode.', f'Median {u}{med}; mode {u}{mode}', f'Median (middle of ordered values) {u}{med} [1]; mode {u}{mode} [1] [2]'),
             ('Calculate the range.', f'{u}{rng}', f'{u}{max(vals)} − {u}{min(vals)} = {u}{rng} [1] [1]')]
    if D >= 3:
        parts.append(('Explain one limitation of using these results to make decisions.', f'The sample of {n_} is very small, so the results may not represent the target market.', 'Small/unrepresentative sample [1]; consequence [1] [2]'))
    c_, ds = num_opts(lambda x: f'{u}{x:.2f}', mean, [med, mode, sum(vals) / (n_ - 1)])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the mean?', c_, ds, f'{sum(vals)} ÷ {n_}'),
            'err': (f'stated that the median is {u}{vals[n_ // 2]}', 'the values were not put in order before finding the middle value', f'{u}{med}', 'ordered values: ' + ', '.join(str(v) for v in srt), 'median') if vals[n_ // 2] != med else None}


t = T(10, 'Reliability and cost-effectiveness of market research', ['reliability and cost-effectiveness of market research', 'reliability of market research', 'cost-effectiveness'],
      defs=[('reliability (of research)', 'The extent to which market research results are accurate and would be the same if the research were repeated.'),
            ('sampling bias', 'Errors in research results caused by a sample that does not represent the target population.')],
      mcqs=[('Which is most likely to reduce the reliability of a questionnaire?', 'Leading questions that suggest an answer', ['A large random sample', 'Clear, simple questions', 'Testing the questionnaire first'],
             'Leading questions bias answers.'),
            ('Market research is cost-effective when', 'the benefits of better decisions exceed the cost of the research', ['it is the cheapest possible', 'it uses only secondary data', 'it gives exact forecasts'],
             'Research must be worth more than it costs.'),
            ('Which would most improve the reliability of a survey?', 'Using a larger, more representative sample', ['Asking only friends and family', 'Using leading questions', 'Reducing the number of respondents'],
             'Larger representative samples reduce error.')],
      exps=[('Explain two reasons why market research results may be unreliable.', 'The sample may be too small or biased, so it does not represent the market; and respondents may not answer honestly or may change their minds.', '2 × (1 mark reason, 1 mark explanation): sample, question design, dishonest answers, out-of-date data, researcher bias. [4]'),
            ('Explain why a small business might decide that extensive market research is not cost-effective.', 'The cost of research may be large relative to its budget and the size of the decision, and the owner\'s knowledge of local customers may be good enough.', '1 mark cost relative to budget/decision; 1 mark alternatives such as owner knowledge. [2]')],
      adv=[('employing a market research agency', ['expert skills and methods', 'larger and better samples', 'objective analysis'],
            ['expensive', 'agency may not know the business', 'takes time'])],
      anl=[('Analyse the factors that could make market research by {b} unreliable.', ['reliability means accurate, repeatable results', 'small or biased samples', 'poorly designed questions', 'changes in the market after research'])],
      ev=[('Evaluate whether {b} should spend more on market research before launching {newprod}.', ['reduces risk of failure', 'better marketing decisions', 'evidence for investors'],
           ['costs time and money', 'results may be unreliable', 'competitors may launch first'],
           ['the size of the investment', 'how new the product is', 'the budget available'])])


# =====================================================================================
# 11 The marketing mix: product and price
# =====================================================================================

t = T(11, 'Product: product portfolio, product life cycle and extension strategies', ['product: product portfolio, product life cycle and extension strategies', 'product life cycle', 'product portfolio', 'extension strategies'],
      defs=[('product life cycle', 'The stages a product goes through from its introduction, through growth and maturity, to decline.'),
            ('extension strategy', 'A plan to extend the life of a product before it goes into decline, for example by finding new markets or new uses, or by changing its design.'),
            ('product portfolio', 'The range of products that a business sells.'),
            ('Boston Matrix', 'A model that analyses a product portfolio by market growth and relative market share, classifying products as stars, cash cows, problem children and dogs.')],
      mcqs=[('At which stage of the product life cycle are sales highest?', 'Maturity', ['Introduction', 'Growth', 'Development'],
             'Sales peak at maturity.'),
            ('Which is an extension strategy?', 'Selling the product in a new export market', ['Stopping production', 'Raising the price sharply', 'Reducing quality'],
             'New markets extend sales.'),
            ('In the Boston Matrix, a product with high market share in a low-growth market is a', 'cash cow', ['star', 'problem child', 'dog'],
             'Cash cows generate cash with little investment.'),
            ('Cash flow is most likely to be negative during the', 'development and introduction stages', ['maturity stage', 'decline stage after costs are cut', 'saturation stage'],
             'Heavy spending with few sales.')],
      exps=[('Explain two extension strategies a business could use for a product in the maturity stage.', 'It could find new markets, for example by exporting; or it could update the product\'s design or packaging so that it appeals to customers again.', '2 × (1 mark strategy, 1 mark explanation): new markets, new uses, redesign, new packaging, promotion. [4]'),
            ('Explain why a business should have a balanced product portfolio.', 'Products at different stages spread risk; cash from mature products (cash cows) can fund new products, so the business is not dependent on one product.', '1 mark spread risk; 1 mark cash from mature funds new; 1 mark avoid dependence. [3]'),
            ('Explain one limitation of the product life cycle model.', 'Not all products follow the same pattern or length of cycle, so it is hard to know which stage a product is in and when decline will start.', '1 mark limitation; 1 mark explanation. [2]')],
      adv=[('using an extension strategy for its main product', ['extends sales and revenue', 'cheaper than developing a new product', 'uses existing brand loyalty'],
            ['may only delay decline', 'costs of redesign or promotion', 'resources diverted from new products'])],
      anl=[('Analyse how {b} could use the product life cycle to plan its marketing of {prod}.', ['the product life cycle has introduction, growth, maturity and decline stages', 'promotion and pricing change at each stage', 'extension strategies in maturity', 'timing the launch of {newprod}']),
           ('Analyse how the Boston Matrix could help {b} manage its product portfolio.', ['the Boston Matrix uses market growth and market share', 'cash cows fund stars and problem children', 'dogs may be withdrawn', 'helps balance the portfolio and cash flow'])],
      ev=[('Evaluate whether {b} should use an extension strategy for its existing {prod} or launch {newprod}.', ['extension is cheaper and uses brand loyalty', 'new product gives long-term growth', 'portfolio balance'],
           ['extension may only delay decline', 'new products often fail', 'both need investment'],
           ['the stage of the existing product', 'the finance available', 'market research evidence'])])


t = T(11, 'Branding and unique selling point (USP)', ['branding and unique selling point (usp)', 'branding', 'unique selling point', 'usp'],
      defs=[('brand', 'A name, symbol or design that identifies a product and distinguishes it from those of competitors.'),
            ('unique selling point (USP)', 'A feature of a product that makes it different from competitors\' products and gives customers a reason to buy it.'),
            ('product differentiation', 'Making a product distinct from competitors\' products in the minds of customers, through design, quality, branding or service.')],
      mcqs=[('A strong brand is most likely to allow a business to', 'charge a higher price without losing many customers', ['avoid all competition', 'reduce production costs automatically', 'stop advertising forever'],
             'Strong brands make demand less price elastic.'),
            ('Which is the best example of a USP?', 'The only smartphone with a battery that lasts for seven days', ['A product that is the same as competitors\'', 'A low advertising budget', 'A large factory'],
             'A USP is a unique feature.'),
            ('Brand loyalty means that customers', 'continue to buy the brand rather than switching to rivals', ['buy any brand at the lowest price', 'never buy the product', 'are paid to buy'],
             'Loyal customers repeat purchases.')],
      exps=[('Explain two benefits to a business of having a strong brand.', 'Customers are loyal and repeat their purchases, giving stable sales; and demand is less price elastic, so a premium price can be charged.', '2 × (1 mark benefit, 1 mark explanation). [4]'),
            ('Explain why a USP is important in a competitive market.', 'It gives customers a clear reason to choose this product over rivals, helping the business win sales and charge a higher price.', '1 mark reason to choose; 1 mark higher sales/price. [2]')],
      adv=[('building a strong brand for its {prod}', ['customer loyalty', 'higher prices possible', 'easier to launch new products'],
            ['expensive promotion', 'bad publicity damages the brand', 'takes time to build'])],
      anl=[('Analyse how {b} could create a USP for its {prod}.', ['a USP makes a product different', 'product design or quality features', 'service or delivery', 'ethical or environmental features']),
           ('Analyse the benefits to {b} of strong branding.', ['a brand identifies and differentiates products', 'loyalty and repeat purchases', 'less price elastic demand', 'easier launch of {newprod}'])],
      ev=[('Evaluate whether branding is the most important factor in the success of {bp} {prod}.', ['loyalty', 'premium pricing', 'recognition'],
           ['product quality and price also matter', 'distribution and availability', 'competitors\' actions'],
           ['the type of market', 'how customers choose', 'the strength of rival brands'])])


t = T(11, 'Pricing strategies: cost-plus, penetration, skimming, competitive, dynamic', ['pricing strategies: cost-plus, penetration, skimming, competitive, dynamic', 'pricing strategies', 'price skimming', 'penetration pricing', 'cost-plus pricing'],
      defs=[('cost-plus pricing', 'Setting the price by adding a fixed percentage mark-up to the unit cost of a product.'),
            ('penetration pricing', 'Setting a low price when a product is launched to gain market share quickly.'),
            ('price skimming', 'Setting a high price when a new product is launched and lowering it later.'),
            ('competitive pricing', 'Setting a price based on the prices charged by competitors.'),
            ('dynamic pricing', 'Changing prices frequently in response to changes in demand and supply, often automatically online.')],
      mcqs=[('Which pricing strategy is most suitable for an innovative new technology product with no competitors?', 'Price skimming', ['Penetration pricing', 'Competitive pricing', 'Cost-plus with a very low mark-up'],
             'Early adopters will pay a high price.'),
            ('A unit cost of $8 and a mark-up of 25% give a cost-plus price of', '$10.00', ['$8.25', '$2.00', '$33.00'],
             '$8 × 1.25 = $10.'),
            ('Airlines that raise ticket prices as a flight fills up are using', 'dynamic pricing', ['penetration pricing', 'cost-plus pricing', 'loss leaders'],
             'Prices change with demand.'),
            ('A disadvantage of penetration pricing is that', 'it is difficult to raise the price later without losing customers', ['it gains market share slowly', 'it gives high profit margins at launch', 'it only works for luxury goods'],
             'Customers expect the low price to continue.')],
      exps=[('Explain one advantage and one disadvantage of cost-plus pricing.', 'Advantage: it is simple and ensures each unit covers its cost. Disadvantage: it ignores demand and competitors\' prices, so the price may be too high to sell or too low to maximise profit.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain why a business might use price skimming for a new product.', 'Early adopters are willing to pay a high price for something new, so the business earns high margins and can recover development costs quickly before competitors enter.', '1 mark early adopters; 1 mark recover development costs/high margin. [2]'),
            ('Explain the difference between penetration pricing and price skimming.', 'Penetration sets a low launch price to gain market share quickly; skimming sets a high launch price to earn high margins from early adopters, then lowers it.', '1 mark penetration; 1 mark skimming. [2]')],
      adv=[('using penetration pricing to launch {newprod}', ['rapid market share', 'discourages competitors', 'economies of scale from high volume'],
            ['low margins', 'hard to raise price later', 'may suggest low quality']),
           ('using price skimming to launch {newprod}', ['high margins', 'recovers development costs quickly', 'premium image'],
            ['attracts competitors', 'limits sales volume', 'early buyers may feel cheated when price falls'])],
      anl=[('Analyse which pricing strategy {b} should use to launch {newprod}.', ['pricing strategies include penetration, skimming and competitive pricing', 'penetration to build market share quickly', 'skimming if the product is innovative', 'the choice depends on competition and costs']),
           ('Analyse the factors {b} should consider when setting the price of its {prod}.', ['price affects revenue and image', 'costs of production', 'competitors\' prices', 'price elasticity of demand'])],
      ev=[('Evaluate the most suitable pricing strategy for {b} to use for {newprod}.', ['skimming for innovation', 'penetration for market share', 'competitive pricing in crowded markets'],
           ['each has risks', 'costs must be covered', 'brand image'],
           ['how innovative the product is', 'the level of competition', 'its objectives'])])


HIGHER = "The cost-plus price is higher than the rival's, so customers may buy from the competitor"
LOWER = "The cost-plus price is below the rival's, so the business may be giving up profit it could earn"


@spec(t)
def cp_calc(r, D):
    c = B(r)
    mat = step(r, 2, 40, 1) + r.choice([0, 0.5])
    lab = step(r, 1, 30, 1) + r.choice([0, 0.25, 0.5])
    fc = step(r, 20000, 400000, 5000)
    q = step(r, 2000, 50000, 1000)
    ohu = fc / q
    uc = mat + lab + ohu
    mu = r.choice([20, 25, 30, 40, 50, 60])
    price = uc * (1 + mu / 100)
    setup = (f'{c["b"]} uses cost-plus pricing for {c["newprod"]}. For each unit, materials cost ${mat:.2f} and direct labour ${lab:.2f}. '
             f'Fixed overheads are ${fc:,} a year and it expects to sell {q:,} units. It adds a mark-up of {mu}% to unit cost.')
    parts = [('Calculate the unit cost.', m2(uc), f'Overhead per unit ${fc:,} ÷ {q:,} = {m2(ohu)} [1]; {m2(mat)} + {m2(lab)} + {m2(ohu)} = {m2(uc)} [1] [2]'),
             ('Calculate the selling price.', m2(price), f'{m2(uc)} × {1 + mu / 100:g} = {m2(price)} [1] [1]')]
    if D >= 3:
        rp = price * r.choice([0.85, 0.9, 1.1, 1.2])
        parts.append((f'The main competitor sells a similar product for {m2(rp)}. Explain one problem with using cost-plus pricing in this situation.',
                      (HIGHER if price > rp else LOWER) + '; cost-plus ignores demand and competition.',
                      'Comparison with competitor price [1]; ignores demand/competition [1] [2]'))
        parts.append(('Calculate the profit per unit at this price.', m2(price - uc), f'{m2(price)} − {m2(uc)} = {m2(price - uc)} [1] [1]'))
    c_, ds = num_opts(m2, price, [uc * mu / 100, (mat + lab) * (1 + mu / 100), uc + mu])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the selling price?', c_, ds, f'{m2(uc)} × {1 + mu / 100:g}'),
            'err': (f'set the price at {m2((mat + lab) * (1 + mu / 100))}', 'fixed overheads per unit were left out of the unit cost', m2(price), f'({m2(mat)} + {m2(lab)} + {m2(ohu)}) × {1 + mu / 100:g}', 'price')}


t = T(11, 'Price elasticity of demand: calculation and significance', ['price elasticity of demand: calculation and significance', 'price elasticity of demand', 'ped'],
      defs=[('price elasticity of demand (PED)', 'The responsiveness of quantity demanded to a change in price: % change in quantity demanded ÷ % change in price.'),
            ('price inelastic demand', 'Demand for which the percentage change in quantity demanded is smaller than the percentage change in price (PED between 0 and −1).'),
            ('price elastic demand', 'Demand for which the percentage change in quantity demanded is greater than the percentage change in price (PED greater than 1, ignoring the sign).')],
      mcqs=[('If PED is −0.4 and the price rises by 10%, quantity demanded will', 'fall by 4%', ['fall by 40%', 'rise by 4%', 'fall by 0.4%'],
             '%ΔQ = −0.4 × 10 = −4%.'),
            ('For a product with price inelastic demand, a price increase will', 'increase total revenue', ['reduce total revenue', 'leave quantity unchanged', 'increase quantity demanded'],
             'Quantity falls proportionally less than price rises.'),
            ('Which product is likely to have the most price elastic demand?', 'One brand of bottled water among many similar brands', ['Petrol', 'Salt', 'A life-saving medicine'],
             'Many close substitutes make demand elastic.')],
      exps=[('Explain two factors that affect the price elasticity of demand for a product.', 'The number of close substitutes: more substitutes make demand more elastic; and whether the product is a necessity: necessities have inelastic demand.', '2 × (1 mark factor, 1 mark explanation): substitutes, necessity/luxury, proportion of income, brand loyalty, time. [4]'),
            ('Explain why knowing PED is useful to a business when setting prices.', 'It shows how sales and revenue will respond to a price change: if demand is inelastic, raising price increases revenue; if elastic, cutting price increases revenue.', '1 mark predict sales response; 1 mark revenue effect explained. [2]'),
            ('Explain one limitation of using PED estimates to make pricing decisions.', 'PED is calculated from past data and assumes other factors are unchanged, but competitors\' prices, incomes and tastes may change.', '1 mark limitation; 1 mark explanation. [2]')],
      adv=[('raising the price of its {prod} because demand is price inelastic', ['higher revenue', 'higher profit margin', 'quantity falls only slightly'],
            ['competitors may not follow', 'customer goodwill may suffer', 'PED estimate may be wrong'])],
      anl=[('Analyse how knowledge of price elasticity of demand could help {b} set the price of its {prod}.', ['PED measures responsiveness of demand to price', 'inelastic demand: a price rise increases revenue', 'elastic demand: a price cut increases revenue', 'helps forecast sales and production']),
           ('Analyse the factors that are likely to affect the price elasticity of demand for {bp} {prod}.', ['PED depends on substitutes and necessity', 'number of competing brands', 'strength of brand loyalty', 'proportion of customers\' income spent'])],
      ev=[('Evaluate the usefulness of price elasticity of demand to {b} when making pricing decisions.', ['predicts effect on revenue', 'guides price changes', 'helps forecast output'],
           ['estimates may be inaccurate', 'other factors change', 'competitors\' reactions'],
           ['how the estimate was made', 'stability of the market', 'other elements of the marketing mix'])])


@spec(t)
def ped_calc2(r, D):
    c = B(r)
    P = step(r, 2, 80, 1)
    Q = step(r, 5000, 80000, 1000)
    kind = r.randrange(2)
    if kind == 0 or D <= 2:
        dp = r.choice([-20, -15, -10, -5, 5, 10, 15, 20])
        e = r.choice([-0.2, -0.4, -0.5, -0.6, -0.8, -1.2, -1.5, -2.0, -2.5])
        dq = e * dp
        P2, Q2 = P * (1 + dp / 100), round(Q * (1 + dq / 100))
        R1, R2 = P * Q, P2 * Q2
        setup = f'{c["b"]} sells {Q:,} units of a product each month at ${P}. It plans to {"raise" if dp > 0 else "cut"} the price by {abs(dp)}%. The price elasticity of demand is estimated to be {e}.'
        parts = [('Calculate the new quantity demanded each month.', f'{Q2:,} units', f'%ΔQ = {e} × {dp:+} = {dq:+g}% [1]; {Q:,} × {1 + dq / 100:g} = {Q2:,} [1] [2]'),
                 ('Calculate the change in total revenue.', f'{"+" if R2 >= R1 else "−"}{m(abs(R2 - R1))}', f'Old revenue {m(R1)}; new {m2(P2)} × {Q2:,} = {m(R2)} [1]; change {"+" if R2 >= R1 else "−"}{m(abs(R2 - R1))} [1] [2]')]
        if D >= 3:
            parts.append(('Explain whether the price change is likely to benefit the business.', f'Demand is price {"inelastic" if abs(e) < 1 else "elastic"}, so revenue {"rises" if R2 > R1 else "falls"}; profit also depends on costs of the change in output and rivals\' reactions.',
                          f'Price {"inelastic" if abs(e) < 1 else "elastic"} → revenue {"rises" if R2 > R1 else "falls"} [1]; costs/rivals/accuracy of estimate [1] [2]'))
        c_, ds = num_opts(lambda x: f'{x:+.1f}%', dq, [dp / e, -dq, e])
        return {'setup': setup, 'parts': parts, 'c': c,
                'mcq': ('By what percentage will quantity demanded change?', c_, ds, f'{e} × {dp:+} = {dq:+g}%'),
                'err': (f'calculated the change in quantity demanded as {dp / e:+.1f}%', 'the price change was divided by PED instead of multiplied by it', f'{dq:+g}%', f'{e} × {dp:+}', 'percentage change in quantity')}
    dp = r.choice([5, 8, 10, 12, 20, 25])
    sgn = r.choice([-1, 1])
    dq = r.choice([2, 4, 5, 6, 10, 15, 20, 30, 40])
    if dq == dp:
        return None
    P2 = round(P * (1 + sgn * dp / 100), 2)
    Q2 = round(Q * (1 - sgn * dq / 100))
    pdq = (Q2 - Q) / Q * 100
    pdp = (P2 - P) / P * 100
    e = pdq / pdp
    setup = f'When {c["b"]} changed the price of a product from ${P:.2f} to ${P2:.2f}, monthly sales changed from {Q:,} to {Q2:,} units. Other factors were unchanged.'
    parts = [('Calculate the price elasticity of demand.', f'{e:.2f}', f'%ΔQ = {pdq:+.1f}%; %ΔP = {pdp:+.1f}% [1]; PED = {pdq:+.1f} ÷ {pdp:+.1f} = {e:.2f} [1] [2]'),
             ('State whether demand is price elastic or price inelastic and explain what this means for revenue.', f'{"Elastic" if abs(e) > 1 else "Inelastic"}: quantity changes {"more" if abs(e) > 1 else "less"} than proportionately, so revenue {"falls" if (abs(e) > 1) == (sgn > 0) else "rises"} when price {"rises" if sgn > 0 else "falls"}.',
              f'{"Elastic" if abs(e) > 1 else "Inelastic"} [1]; revenue effect [1] [2]')]
    c_, ds = num_opts(lambda x: f'{x:.2f}', e, [1 / e, -e, pdq])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the price elasticity of demand?', c_, ds, f'{pdq:+.1f}% ÷ {pdp:+.1f}%'),
            'err': (f'calculated PED as {1 / e:.2f}', 'the percentage change in price was divided by the percentage change in quantity, instead of the other way round', f'{e:.2f}', f'{pdq:+.1f}% ÷ {pdp:+.1f}%', 'PED')}


# =====================================================================================
# 12 The marketing mix: promotion and place
# =====================================================================================

t = T(12, 'Promotion: above-the-line and below-the-line methods', ['promotion: above-the-line and below-the-line methods', 'promotion', 'above-the-line', 'below-the-line'],
      defs=[('above-the-line promotion', 'Promotion through independent mass media, such as television, radio, newspapers and billboards, aimed at a wide audience.'),
            ('below-the-line promotion', 'Promotion that the business controls directly, such as sales promotions, direct mail, personal selling and sponsorship.'),
            ('sales promotion', 'Short-term incentives to encourage customers to buy, such as discounts, free samples and buy-one-get-one-free offers.')],
      mcqs=[('Which is an example of below-the-line promotion?', 'A buy-one-get-one-free offer in shops', ['A television advertisement', 'A national newspaper advertisement', 'A radio advertisement'],
             'Sales promotions are controlled directly by the business.'),
            ('Which promotion method is most suitable for selling expensive industrial machinery?', 'Personal selling', ['Television advertising', 'Free samples', 'Billboards'],
             'Complex products need explanation and negotiation.'),
            ('A disadvantage of television advertising is that', 'it is very expensive and may reach people outside the target market', ['it cannot reach large audiences', 'it is a form of personal selling', 'it cannot show the product'],
             'Mass media costs are high and coverage is broad.')],
      exps=[('Explain the difference between above-the-line and below-the-line promotion.', 'Above-the-line promotion uses mass media such as television and newspapers to reach a wide audience; below-the-line uses methods controlled by the business, such as sales promotions, direct mail and sponsorship, often aimed at specific customers.', '1 mark above-the-line; 1 mark below-the-line; 1 mark example/contrast. [3]'),
            ('Explain two factors a business should consider when choosing a promotion method.', 'The cost compared with the marketing budget; and the target market – the method must reach the customers the business wants, e.g. social media for young people.', '2 × (1 mark factor, 1 mark explanation): budget, target market, product type, competitors, stage of life cycle. [4]')],
      adv=[('using television advertising for its {prod}', ['reaches a mass audience', 'builds brand awareness', 'can demonstrate the product'],
            ['very expensive', 'hard to target', 'effect hard to measure']),
           ('using sales promotions such as discounts', ['quick boost to sales', 'encourages trial', 'clears old stock'],
            ['short-term effect', 'reduces margins', 'may damage brand image'])],
      anl=[('Analyse the promotion methods {b} could use to launch {newprod}.', ['promotion informs and persuades customers', 'above-the-line advertising for awareness', 'below-the-line offers to encourage trial', 'methods must suit the target market and budget']),
           ('Analyse the benefits to {b} of below-the-line promotion.', ['below-the-line methods are controlled by the business', 'targeted at specific customers', 'often cheaper than mass media', 'easier to measure results'])],
      ev=[('Evaluate the most effective promotion methods for {b}.', ['mass media for awareness', 'sales promotions for trial', 'personal selling for business customers'],
           ['cost', 'target market fit', 'short-term effects'],
           ['the budget', 'the target customers', 'the stage of the product life cycle'])])


t = T(12, 'Digital marketing and social media', ['digital marketing and social media', 'digital marketing', 'social media'],
      defs=[('digital marketing', 'Promoting products through digital channels such as websites, search engines, email, apps and social media.'),
            ('social media marketing', 'Using social media platforms to build awareness, engage customers and promote products.'),
            ('viral marketing', 'Marketing messages designed so that people share them quickly with others online.')],
      mcqs=[('An advantage of social media marketing is that', 'it can target specific groups and measure responses cheaply', ['it always reaches older customers best', 'negative comments cannot spread', 'it costs nothing to manage'],
             'Platforms provide targeting and data.'),
            ('A risk of social media marketing is that', 'negative customer comments can spread quickly', ['it cannot be targeted', 'it is always more expensive than television', 'customers cannot respond'],
             'Online criticism spreads rapidly.'),
            ('Paying a popular online personality to promote a product is called', 'influencer marketing', ['direct mail', 'personal selling', 'sponsorship of a sports event'],
             'Influencers promote to their followers.')],
      exps=[('Explain two advantages of digital marketing for a small business.', 'It is cheaper than mass media, so a small budget can still reach customers; and it can be targeted at specific groups and the results measured, for example clicks and sales.', '2 × (1 mark advantage, 1 mark explanation). [4]'),
            ('Explain one disadvantage of using social media to promote a product.', 'Negative comments or poor reviews spread quickly and can damage the brand, and it needs staff time to monitor and respond.', '1 mark disadvantage; 1 mark explanation. [2]')],
      adv=[('using social media influencers to promote {newprod}', ['reaches target audience', 'builds trust through recommendation', 'can go viral'],
            ['influencer fees', 'risk if the influencer\'s reputation suffers', 'hard to measure long-term effect'])],
      anl=[('Analyse how {b} could use digital marketing to increase sales of {prod}.', ['digital marketing uses online channels', 'targeted social media advertising', 'search engine optimisation', 'email and apps for repeat customers']),
           ('Analyse the risks to {b} of relying on social media marketing.', ['social media marketing engages customers online', 'negative reviews spread quickly', 'changes to platform rules or costs', 'not all customers use social media'])],
      ev=[('Evaluate whether {b} should spend most of its promotion budget on digital marketing.', ['targeted and measurable', 'cheaper than mass media', 'engages customers'],
           ['risk of negative publicity', 'not all target customers online', 'crowded and competitive'],
           ['the target market', 'the type of product', 'the skills of its marketing staff'])])


t = T(12, 'Place: distribution channels and online distribution', ['place: distribution channels and online distribution', 'distribution channels', 'online distribution'],
      defs=[('distribution channel', 'The route a product takes from the producer to the final consumer, for example through wholesalers and retailers.'),
            ('intermediary', 'A business such as a wholesaler, retailer or agent that is part of the distribution channel between producer and consumer.'),
            ('e-commerce', 'Buying and selling goods and services over the internet.')],
      mcqs=[('A producer selling directly to consumers through its own website is using', 'a direct channel (zero intermediaries)', ['a channel with a wholesaler and a retailer', 'an agent', 'below-the-line promotion'],
             'No intermediaries are involved.'),
            ('A benefit of using wholesalers is that they', 'buy in bulk and break it down for many small retailers', ['always reduce the final price', 'remove the need for transport', 'give the producer full control'],
             'Wholesalers break bulk and reduce distribution costs for producers.'),
            ('A disadvantage of selling only online is that', 'customers cannot see or try the product before buying', ['it cannot reach customers abroad', 'it has higher rent costs than shops', 'it is open for fewer hours'],
             'Lack of physical contact may deter some buyers.')],
      exps=[('Explain two factors that affect the choice of distribution channel.', 'The type of product: perishable or technical products need short channels; and the target market: customers spread over a wide area may require wholesalers or online sales.', '2 × (1 mark factor, 1 mark explanation): product type, cost, control, target market, competitors\' channels. [4]'),
            ('Explain why many businesses now sell through both shops and online channels.', 'Online sales reach more customers at any time and lower costs, while shops let customers see products and get advice; using both meets different preferences and increases sales.', '1 mark online benefit; 1 mark shop benefit; 1 mark combined effect. [3]')],
      adv=[('selling {prod} directly to consumers online', ['higher margin with no intermediaries', 'wider reach', 'direct customer data'],
            ['delivery costs and logistics', 'website and marketing costs', 'loss of retailer support']),
           ('selling through large retailers', ['wide availability', 'retailers handle selling', 'credibility'],
            ['retailers take a margin', 'less control over display and price', 'retailers have bargaining power'])],
      anl=[('Analyse the advantages to {b} of selling through online channels.', ['online distribution sells via the internet', 'reach customers in {newmkt}', 'lower costs than physical outlets', 'data about customer behaviour']),
           ('Analyse which distribution channel would be most suitable for {newprod}.', ['channels differ in number of intermediaries', 'product characteristics', 'location of target customers', 'cost and control'])],
      ev=[('Evaluate whether {b} should sell more of its {prod} directly to customers online.', ['higher margins', 'wider reach', 'customer data'],
           ['delivery costs', 'loss of retail presence', 'online competition'],
           ['the type of product', 'customer buying habits', 'logistics capability'])])


t = T(12, 'Integrated marketing mix and the 7Ps for services', ['integrated marketing mix and the 7ps for services', 'marketing mix', '7ps', 'integrated marketing mix'],
      defs=[('marketing mix', 'The combination of decisions about product, price, promotion and place used to market a product.'),
            ('7Ps', 'The extended marketing mix for services: product, price, promotion, place, people, process and physical evidence.'),
            ('physical evidence', 'The tangible features that customers see when using a service, such as the premises, uniforms and website.')],
      mcqs=[('Which is one of the three extra Ps for services?', 'People', ['Profit', 'Production', 'Planning'],
             'People, process and physical evidence.'),
            ('An integrated marketing mix means that', 'all the elements of the mix are consistent with each other', ['price is always the most important element', 'only promotion is used', 'every product has the same mix'],
             'For example, a premium product with a premium price and exclusive outlets.'),
            ('In a restaurant, the speed and ease of ordering and payment is part of the', 'process', ['physical evidence', 'product', 'price'],
             'Process covers how the service is delivered.')],
      exps=[('Explain why the elements of the marketing mix must be integrated.', 'If they are inconsistent – for example a luxury product sold at a low price in discount shops – customers receive mixed messages and the brand image is damaged.', '1 mark consistency; 1 mark example of inconsistency and effect. [2]'),
            ('Explain why "people" is an important element of the marketing mix for a service business.', 'Services are delivered by employees, so their skills, attitude and appearance determine the customer\'s experience and whether they return.', '1 mark staff deliver the service; 1 mark effect on customer experience/loyalty. [2]')],
      adv=[('improving the physical evidence of its service', ['better first impressions', 'supports premium pricing', 'reassures customers about quality'],
            ['costly refurbishment', 'must be matched by service quality', 'benefits hard to measure'])],
      anl=[('Analyse how {b} could develop an integrated marketing mix for {newprod}.', ['the marketing mix: product, price, promotion, place', 'price must match the product image', 'promotion must reach the target market', 'place must suit customers\' buying habits']),
           ('Analyse how the extra Ps of the services marketing mix apply to {b}.', ['people, process and physical evidence', 'trained, friendly staff', 'efficient processes for customers', 'premises and website as physical evidence'])],
      ev=[('Evaluate which element of the marketing mix is most important for the success of {b}.', ['product quality', 'competitive price', 'promotion and place'],
           ['all elements must be integrated', 'importance depends on the market', 'people and process matter for services'],
           ['the nature of its {prod}', 'competition', 'the target market'])])


# =====================================================================================
# 13 The nature of operations
# =====================================================================================

t = T(13, 'Transformation process: inputs, processes and outputs', ['transformation process: inputs, processes and outputs', 'transformation process', 'inputs processes outputs'],
      defs=[('operations management', 'The management of the process that transforms inputs into outputs (goods and services) efficiently and to the required quality.'),
            ('transformation process', 'The conversion of inputs such as materials, labour and capital into outputs of goods and services that have more value.'),
            ('inputs', 'The resources used in production: land, labour, capital and enterprise, including materials and energy.')],
      mcqs=[('In a bakery, which is an input?', 'Flour', ['Bread sold to customers', 'Customer satisfaction', 'Profit'],
             'Flour is a material used in production.'),
            ('The main purpose of the transformation process is to', 'add value by turning inputs into outputs customers want', ['increase the cost of inputs', 'reduce the number of customers', 'replace marketing'],
             'Outputs are worth more than inputs.'),
            ('In a hospital, which is the output?', 'Treated patients', ['Doctors\' time', 'Medical equipment', 'Electricity'],
             'The service provided is the output.')],
      exps=[('Explain how operations management adds value.', 'It organises inputs efficiently and transforms them into products of the right quality that customers will pay more for than the cost of the inputs.', '1 mark efficient transformation; 1 mark quality/customer value; 1 mark price exceeds input cost. [3]'),
            ('Explain the transformation process for a service business such as a restaurant.', 'Inputs such as food, staff, equipment and premises are transformed through cooking and serving into outputs of meals and a dining experience for customers.', '1 mark inputs; 1 mark process; 1 mark outputs. [3]')],
      adv=[('investing in new technology in its transformation process', ['higher productivity', 'consistent quality', 'lower unit costs'],
            ['high capital cost', 'training needed', 'staff resistance'])],
      anl=[('Analyse the inputs, processes and outputs in the operations of {b}.', ['operations transform inputs into outputs', 'inputs such as labour, materials and equipment', 'processes that add value to {prod}', 'outputs sold to customers']),
           ('Analyse how better operations management could add value at {b}.', ['operations management controls the transformation process', 'less waste lowers costs', 'better quality raises the price customers pay', 'faster delivery improves customer service'])],
      ev=[('Evaluate the importance of operations management to the success of {b}.', ['efficiency lowers costs', 'quality builds reputation', 'reliable delivery'],
           ['marketing and finance also essential', 'external factors', 'depends on the industry'],
           ['the competitive position', 'the type of product', 'customer expectations'])])


t = T(13, 'Efficiency, effectiveness and productivity measures', ['efficiency, effectiveness and productivity measures', 'productivity', 'efficiency', 'effectiveness'],
      defs=[('labour productivity', 'The output per worker in a given period: total output ÷ number of workers.'),
            ('efficiency', 'Producing output with the minimum use of resources, i.e. at the lowest cost.'),
            ('effectiveness', 'The extent to which a business achieves its objectives, such as meeting customer needs.'),
            ('capital productivity', 'The output per unit of capital (for example per machine) in a given period.')],
      mcqs=[('A factory with 40 workers produces 12,000 units a week. Labour productivity is', '300 units per worker per week', ['480 units', '12,040 units', '3.3 units'],
             '12,000 ÷ 40 = 300.'),
            ('Which is most likely to increase labour productivity?', 'Training workers and providing better equipment', ['Increasing labour turnover', 'Reducing investment', 'Using older machinery'],
             'Skills and capital raise output per worker.'),
            ('A business can be efficient but not effective if it', 'produces at low cost a product that customers do not want', ['achieves all its objectives', 'has high labour productivity and high sales', 'meets customer needs at low cost'],
             'Effectiveness is about meeting objectives.')],
      exps=[('Explain the difference between efficiency and effectiveness.', 'Efficiency means using as few resources as possible to produce output; effectiveness means achieving the objectives, such as producing what customers want. A business can be efficient without being effective.', '1 mark efficiency; 1 mark effectiveness; 1 mark contrast/example. [3]'),
            ('Explain why higher labour productivity may not lead to lower unit costs.', 'If productivity rises because of higher wages or expensive new machinery, the extra costs may outweigh the gain in output per worker.', '1 mark higher costs; 1 mark comparison with output gain. [2]'),
            ('Explain two ways a business could increase labour productivity.', 'Train workers so they work faster and make fewer mistakes; and invest in better machinery or technology so each worker produces more.', '2 × (1 mark method, 1 mark explanation): training, technology, motivation, better methods/lean production. [4]')],
      adv=[('increasing labour productivity', ['lower labour cost per unit', 'more competitive prices', 'higher output without more staff'],
            ['may require investment', 'workers may resist pressure', 'quality may fall'])],
      anl=[('Analyse how {b} could increase its labour productivity.', ['labour productivity is output per worker', 'training improves skills', 'investment in technology', 'motivation and better working methods']),
           ('Analyse the benefits to {b} of improving efficiency.', ['efficiency means minimum resource use', 'lower unit costs', 'more competitive prices or higher margins', 'less waste benefits the environment'])],
      ev=[('Evaluate the best way for {b} to improve its productivity.', ['training', 'new technology', 'motivation schemes'],
           ['costs of each method', 'quality may suffer', 'worker resistance'],
           ['the cause of low productivity', 'the finance available', 'labour relations'])])


@spec(t)
def prod_calc(r, D):
    c = B(r, 40)
    w0 = max(20, round(c['emp'] * r.uniform(0.3, 0.7) / 5) * 5)
    p0 = step(r, 50, 900, 10)
    o0 = w0 * p0
    w1 = w0 + step(r, -w0 // 4, w0 // 4, 5)
    o1 = round(o0 * r.uniform(0.95, 1.3) / 100) * 100
    p1 = o1 / w1
    wage = step(r, 300, 900, 10)
    setup = (f'{c["b"]} employed {w0:,} production workers last year, who produced {o0:,} units a month. This year it employs {w1:,} workers producing {o1:,} units a month. '
             f'Each worker is paid ${wage:,} a month.')
    parts = [('Calculate labour productivity in each year.', f'Last year {p0:,} units; this year {p1:,.1f} units per worker per month', f'{o0:,} ÷ {w0:,} = {p0:,} [1]; {o1:,} ÷ {w1:,} = {p1:,.1f} [1] [2]'),
             ('Calculate the percentage change in labour productivity.', pc((p1 - p0) / p0 * 100), f'({p1:,.1f} − {p0:,}) ÷ {p0:,} × 100 = {pc((p1 - p0) / p0 * 100)} [1] [1]')]
    if D >= 3:
        lc0, lc1 = wage / p0, wage / p1
        parts.append(('Calculate the labour cost per unit in each year.', f'{m2(lc0)}; {m2(lc1)}', f'${wage:,} ÷ {p0:,} = {m2(lc0)} [1]; ${wage:,} ÷ {p1:,.1f} = {m2(lc1)} [1] [2]'))
    c_, ds = num_opts(lambda x: f'{x:,.1f} units', p1, [o1 / w0, o1 - w1, w1 / o1 * 1000])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is labour productivity this year?', c_, ds, f'{o1:,} ÷ {w1:,}'),
            'err': (f'calculated this year\'s labour productivity as {o1 / w0:,.1f} units per worker', 'last year\'s number of workers was used instead of this year\'s', f'{p1:,.1f} units per worker per month', f'{o1:,} ÷ {w1:,}', 'labour productivity') if w1 != w0 else None}


t = T(13, 'Production methods: job, batch, flow and mass customisation', ['production methods: job, batch, flow and mass customisation', 'production methods', 'batch production', 'flow production'],
      defs=[('job production', 'Producing a single, one-off product to the customer\'s individual requirements.'),
            ('batch production', 'Producing a limited number of identical products together, then switching to a different batch.'),
            ('flow production', 'Continuous production of large quantities of identical products on a production line.'),
            ('mass customisation', 'Using flexible, computer-controlled production to make large volumes of products that are tailored to individual customers.')],
      mcqs=[('A wedding dress made to a customer\'s own design is an example of', 'job production', ['flow production', 'batch production', 'mass production'],
             'One-off, made to order.'),
            ('Which is an advantage of flow production?', 'Low unit costs from high-volume production', ['Each product is unique', 'Workers have varied tasks', 'It is easy to change the product'],
             'Economies of scale from continuous production.'),
            ('A bakery that makes 200 white loaves, then 200 brown loaves, is using', 'batch production', ['job production', 'flow production', 'mass customisation'],
             'Groups of identical items in turn.')],
      exps=[('Explain one advantage and one disadvantage of batch production.', 'Advantage: it allows some variety while keeping unit costs lower than job production. Disadvantage: time is lost and costs rise when machines are reset between batches, and inventory of each batch must be stored.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain why flow production may lead to low worker motivation.', 'Workers repeat the same simple task on the production line, which is boring and gives little responsibility or sense of achievement.', '1 mark repetitive tasks; 1 mark link to motivation. [2]'),
            ('Explain how mass customisation combines features of job and flow production.', 'Flexible computer-controlled machines produce in large volumes like flow production, but each product can be tailored to the customer like job production.', '1 mark high volume/low cost; 1 mark individual tailoring. [2]')],
      adv=[('switching from batch to flow production', ['lower unit costs', 'higher output', 'consistent quality'],
            ['high capital cost', 'less flexibility', 'boring work for staff']),
           ('introducing mass customisation', ['meets individual customer needs', 'premium prices', 'competitive advantage'],
            ['expensive flexible technology', 'complex ordering systems', 'longer delivery times'])],
      anl=[('Analyse which production method would be most suitable for {b}.', ['production methods: job, batch, flow, mass customisation', 'volume of demand for {prod}', 'need for variety or customisation', 'cost of equipment and labour skills']),
           ('Analyse the effects on {b} of changing from job production to batch production.', ['job production makes one-off products', 'batch production lowers unit costs', 'less individual choice for customers', 'need for inventory and machine set-up'])],
      ev=[('Evaluate whether {b} should change to flow production.', ['lower unit costs', 'higher output', 'consistent quality'],
           ['high investment', 'inflexible', 'demand may be too small'],
           ['the size and stability of demand', 'the finance available', 'customer need for variety'])])


t = T(13, 'Labour-intensive vs capital-intensive production', ['labour-intensive vs capital-intensive production', 'labour-intensive', 'capital-intensive'],
      defs=[('labour-intensive production', 'Production that uses a high proportion of labour compared with capital.'),
            ('capital-intensive production', 'Production that uses a high proportion of machinery and technology compared with labour.'),
            ('automation', 'The use of machines and computer-controlled systems to carry out tasks previously done by people.')],
      mcqs=[('Which business is most likely to be labour-intensive?', 'A hairdresser', ['An oil refinery', 'A car assembly plant using robots', 'An automated warehouse'],
             'Personal services rely mainly on labour.'),
            ('A business in a country with low wages and expensive machinery is likely to choose', 'labour-intensive production', ['capital-intensive production', 'full automation', 'no production'],
             'Use the relatively cheaper factor.'),
            ('An advantage of capital-intensive production is', 'consistent quality and lower unit costs at high output', ['low initial investment', 'high flexibility to make one-off items', 'personal service'],
             'Machines produce consistently at scale.')],
      exps=[('Explain one advantage and one disadvantage of capital-intensive production.', 'Advantage: machines produce large volumes at consistent quality and low unit cost. Disadvantage: the initial investment is very high and machine breakdowns can stop production.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain two factors that influence whether a business chooses labour-intensive or capital-intensive production.', 'The relative cost of labour and capital; and the scale of production – large-scale production justifies investment in machinery.', '2 × (1 mark factor, 1 mark explanation): relative costs, scale, product type, finance, skills available. [4]')],
      adv=[('automating its production of {prod}', ['lower unit costs at high output', 'consistent quality', 'fewer staff needed'],
            ['high capital cost', 'redundancies harm morale', 'less flexibility'])],
      anl=[('Analyse the benefits to {b} of becoming more capital-intensive.', ['capital-intensive production uses more machinery', 'lower unit costs at high output', 'consistent quality of {prod}', 'less dependence on scarce skilled labour']),
           ('Analyse why {b} might remain labour-intensive.', ['labour-intensive production uses more workers', 'labour may be relatively cheap in {country}', 'flexibility and craft skills', 'lower capital investment needed'])],
      ev=[('Evaluate whether {b} should replace workers with automated machinery.', ['lower unit costs', 'consistent quality', 'higher output'],
           ['high investment', 'redundancies and morale', 'less flexibility'],
           ['relative labour and capital costs', 'the scale of demand', 'access to finance'])])


# =====================================================================================
# 14 Inventory management
# =====================================================================================

t = T(14, 'Purpose and costs of holding inventory', ['purpose and costs of holding inventory', 'holding inventory', 'inventory'],
      defs=[('inventory', 'Stocks of raw materials, work in progress and finished goods held by a business.'),
            ('stock-out', 'A situation where a business runs out of inventory and cannot meet demand.'),
            ('opportunity cost of holding inventory', 'The benefit lost because money tied up in inventory cannot be used for other purposes, such as earning interest or investing.')],
      mcqs=[('Which is a cost of holding too much inventory?', 'Storage and insurance costs', ['Lost sales from stock-outs', 'Idle production lines due to shortages', 'Loss of customer goodwill from late deliveries'],
             'Holding inventory costs money.'),
            ('Which is a cost of holding too little inventory?', 'Lost sales and customer goodwill when items run out', ['Higher storage costs', 'Risk of products becoming out of date', 'More cash tied up'],
             'Stock-outs lose sales.'),
            ('Work in progress is', 'partly finished products', ['raw materials not yet used', 'finished goods ready for sale', 'goods returned by customers'],
             'Goods in the middle of production.')],
      exps=[('Explain two costs of holding large amounts of inventory.', 'Storage costs such as warehouse rent and insurance; and the opportunity cost of cash tied up that could be used elsewhere, plus the risk of goods becoming obsolete or damaged.', '2 × (1 mark cost, 1 mark explanation): storage, opportunity cost, obsolescence, damage/theft. [4]'),
            ('Explain why a business holds inventory of finished goods.', 'To meet unexpected increases in demand and fill orders quickly, so it does not lose sales to competitors.', '1 mark meet demand/unexpected orders; 1 mark avoid lost sales. [2]')],
      adv=[('holding larger inventories of finished goods', ['can meet sudden increases in demand', 'fewer stock-outs', 'bulk-buying discounts'],
            ['higher storage costs', 'cash tied up', 'risk of obsolescence'])],
      anl=[('Analyse the costs to {b} of holding too much inventory.', ['inventory includes raw materials, work in progress and finished goods', 'storage and insurance costs', 'opportunity cost of cash tied up', 'risk of waste and obsolescence of {prod}']),
           ('Analyse the problems {b} could face if it holds too little inventory.', ['low inventory risks stock-outs', 'lost sales and customer goodwill', 'production stops if materials run out', 'higher ordering costs from frequent small orders'])],
      ev=[('Evaluate how {b} should decide how much inventory to hold.', ['avoid stock-outs', 'meet seasonal demand', 'bulk discounts'],
           ['storage and opportunity costs', 'obsolescence', 'cash-flow pressure'],
           ['how predictable demand is', 'supplier reliability', 'the nature of {prod}'])])


t = T(14, 'Inventory control charts: buffer stock, reorder level, lead time', ['inventory control charts: buffer stock, reorder level, lead time', 'inventory control charts', 'buffer stock', 'reorder level', 'lead time'],
      defs=[('buffer inventory', 'The minimum level of inventory held to avoid running out if deliveries are late or demand is higher than expected.'),
            ('reorder level', 'The level of inventory at which a new order is placed.'),
            ('lead time', 'The time between placing an order with a supplier and receiving the delivery.'),
            ('reorder quantity', 'The amount of inventory ordered each time an order is placed.')],
      mcqs=[('A business uses 200 units a day, the lead time is 4 days and buffer inventory is 500 units. The reorder level is', '1,300 units', ['800 units', '700 units', '1,000 units'],
             'Reorder level = buffer + usage × lead time = 500 + 800.'),
            ('On an inventory control chart, buffer inventory is shown as', 'the minimum level below which inventory should not fall', ['the maximum level', 'the reorder quantity', 'the lead time'],
             'Buffer is the safety minimum.'),
            ('If the lead time increases, the reorder level should', 'increase', ['decrease', 'stay the same', 'fall to zero'],
             'More inventory is used while waiting for delivery.')],
      exps=[('Explain why a business holds buffer inventory.', 'In case a delivery is late or demand is higher than expected, so it can keep producing and selling without a stock-out.', '1 mark late deliveries/unexpected demand; 1 mark avoids stock-outs. [2]'),
            ('Explain one limitation of an inventory control chart.', 'It assumes inventory is used at a constant rate and that lead times are fixed, but demand and delivery times vary in reality.', '1 mark limitation; 1 mark explanation. [2]')],
      adv=[('increasing its buffer inventory', ['fewer stock-outs', 'can meet unexpected demand', 'protection against late deliveries'],
            ['higher storage costs', 'cash tied up', 'risk of waste'])],
      anl=[('Analyse how an inventory control chart could help {b} manage its inventory.', ['the chart shows maximum, reorder and buffer levels', 'orders placed at the reorder level', 'buffer inventory protects against delays', 'reduces both stock-outs and excess inventory'])],
      ev=[('Evaluate whether {b} should increase its buffer inventory after recent late deliveries from suppliers.', ['avoids stock-outs', 'protects customer goodwill', 'continuous production'],
           ['higher holding costs', 'cash tied up', 'better to find reliable suppliers'],
           ['how often deliveries are late', 'the cost of a stock-out', 'storage space and cash'])])


@spec(t)
def inv_calc(r, D):
    c = B(r)
    use = step(r, 20, 800, 10)
    lt_ = r.randint(2, 10)
    buf = step(r, use, use * 5, 10)
    roq = step(r, use * 10, use * 30, 50)
    rol = buf + use * lt_
    mx = buf + roq
    setup = (f'{c["b"]} uses {use:,} units of a component each day. The supplier\'s lead time is {lt_} days. '
             f'{c["b"]} keeps a buffer inventory of {buf:,} units and orders {roq:,} units each time.')
    parts = [('Calculate the reorder level.', f'{rol:,} units', f'{buf:,} + ({use:,} × {lt_}) [1]; = {rol:,} units [1] [2]'),
             ('Calculate the maximum inventory level.', f'{mx:,} units', f'{buf:,} + {roq:,} = {mx:,} units [1] [1]'),
             ('Calculate how many days an order lasts after delivery before inventory falls back to the buffer level.', f'{roq / use:g} days', f'{roq:,} ÷ {use:,} = {roq / use:g} days [1] [1]')]
    if D >= 3:
        lt2 = lt_ + r.randint(1, 3)
        parts.append((f'The lead time rises to {lt2} days. Calculate the new reorder level and explain what happens if the reorder level is not changed.',
                      f'{buf + use * lt2:,} units; if not changed, the business will use {use * (lt2 - lt_):,} units of its buffer inventory before the delivery arrives.',
                      f'{buf:,} + {use:,} × {lt2} = {buf + use * lt2:,} [1]; buffer reduced by {use * (lt2 - lt_):,} units/risk of stock-out [1] [2]'))
    c_, ds = num_opts(lambda x: f'{int(x):,} units', rol, [use * lt_, buf + roq, buf * lt_])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the reorder level?', c_, ds, f'{buf:,} + {use:,} × {lt_}'),
            'err': (f'set the reorder level at {use * lt_:,} units', 'the buffer inventory was not added to usage during the lead time', f'{rol:,} units', f'{buf:,} + {use:,} × {lt_}', 'reorder level')}


t = T(14, 'Just-in-time (JIT) inventory management', ['just-in-time (jit) inventory management', 'just-in-time', 'jit'],
      defs=[('just-in-time (JIT)', 'An inventory management system in which materials are delivered just when they are needed for production, so little or no buffer inventory is held.'),
            ('lean production', 'An approach to production that aims to minimise waste of all resources, including time, materials and inventory.')],
      mcqs=[('Which is essential for JIT to work successfully?', 'Reliable suppliers who deliver on time', ['Large buffer inventories', 'Long lead times', 'Infrequent large deliveries'],
             'Without reliable deliveries production stops.'),
            ('An advantage of JIT is', 'less cash tied up in inventory', ['protection against supplier strikes', 'bulk-buying discounts', 'ability to meet sudden large orders from inventory'],
             'Little inventory is held.'),
            ('JIT is part of an approach to production called', 'lean production', ['mass production', 'job production', 'labour-intensive production'],
             'JIT reduces the waste of holding inventory.')],
      exps=[('Explain two disadvantages of using JIT.', 'If a supplier delivers late, production stops because there is no buffer inventory; and frequent small deliveries lose bulk-buying discounts and raise ordering and transport costs.', '2 × (1 mark disadvantage, 1 mark explanation). [4]'),
            ('Explain why JIT can improve a business\'s cash flow.', 'Less cash is spent on inventory before it is needed, so more cash is available for other uses and storage costs fall.', '1 mark less cash tied up in inventory; 1 mark lower storage costs/other uses. [2]')],
      adv=[('introducing just-in-time inventory management', ['lower storage costs', 'less cash tied up', 'less waste'],
            ['production stops if deliveries are late', 'loss of bulk discounts', 'cannot meet sudden increases in demand'])],
      anl=[('Analyse the benefits to {b} of introducing just-in-time inventory management.', ['JIT means materials arrive just when needed', 'lower storage and insurance costs', 'less cash tied up in inventory', 'less waste and obsolescence']),
           ('Analyse the risks to {b} of relying on JIT.', ['JIT holds little buffer inventory', 'supplier delays stop production', 'transport disruption, e.g. to imports into {country}', 'cannot respond to sudden large orders'])],
      ev=[('Evaluate whether {b} should introduce just-in-time inventory management.', ['lower costs', 'better cash flow', 'less waste'],
           ['supply risks', 'needs reliable suppliers nearby', 'loss of bulk discounts'],
           ['reliability of its suppliers', 'how predictable demand is', 'the distance to suppliers'])])


# =====================================================================================
# 15 Capacity utilisation and outsourcing
# =====================================================================================

t = T(15, 'Calculating capacity utilisation', ['calculating capacity utilisation', 'capacity utilisation'],
      defs=[('capacity utilisation', 'The proportion of maximum possible output that is actually being produced: current output ÷ maximum output × 100.'),
            ('maximum capacity', 'The highest output that a business can produce in a given period with its existing resources.')],
      mcqs=[('A factory can produce 50,000 units a month and currently produces 40,000. Capacity utilisation is', '80%', ['125%', '20%', '40%'],
             '40,000 ÷ 50,000 × 100.'),
            ('Higher capacity utilisation usually leads to', 'lower fixed costs per unit', ['higher fixed costs per unit', 'higher total fixed costs', 'lower total output'],
             'Fixed costs are spread over more units.'),
            ('A hotel with 120 rooms has 90 rooms occupied on average. Its capacity utilisation is', '75%', ['133%', '25%', '90%'],
             '90 ÷ 120 × 100.')],
      exps=[('Explain why high capacity utilisation can reduce unit costs.', 'Fixed costs such as rent and machinery are spread over more units of output, so the fixed cost per unit, and therefore average cost, falls.', '1 mark fixed costs spread; 1 mark lower average cost. [2]'),
            ('Explain one problem of operating at 100% capacity utilisation.', 'There is no time for maintenance and no spare capacity for extra orders, so machines may break down, staff may be stressed and new orders may be turned away.', '1 mark problem; 1 mark explanation. [2]')],
      adv=[('increasing its capacity utilisation', ['lower fixed cost per unit', 'better use of resources', 'higher profit'],
            ['less time for maintenance', 'staff stress', 'no spare capacity for new orders'])],
      anl=[('Analyse the effect on the costs of {b} of an increase in capacity utilisation.', ['capacity utilisation = output ÷ maximum output × 100', 'fixed costs spread over more units', 'lower average costs allow lower prices or higher margins', 'at very high levels costs may rise from overtime and breakdowns'])],
      ev=[('Evaluate whether {b} should aim for 100% capacity utilisation.', ['lowest fixed cost per unit', 'maximum use of resources', 'higher profit'],
           ['no spare capacity for orders', 'breakdowns and stress', 'quality may fall'],
           ['how stable demand is', 'maintenance needs', 'the cost of extra capacity'])])


@spec(t)
def cu_calc(r, D):
    c = B(r)
    mx = step(r, 5000, 200000, 1000)
    cu = r.choice([45, 55, 60, 64, 70, 72, 75, 80, 85, 88, 90, 95])
    out = round(mx * cu / 100)
    fc = step(r, 20000, 900000, 5000)
    setup = f'{c["b"]} has a maximum capacity of {mx:,} units a month. Last month it produced {out:,} units. Its fixed costs are ${fc:,} a month.'
    parts = [('Calculate the capacity utilisation.', pc(out / mx * 100), f'{out:,} ÷ {mx:,} × 100 [1]; = {pc(out / mx * 100)} [1] [2]'),
             ('Calculate the fixed cost per unit.', m2(fc / out), f'${fc:,} ÷ {out:,} = {m2(fc / out)} [1] [1]')]
    if D >= 3:
        t2 = min(100, cu + r.choice([5, 10, 15]))
        o2 = round(mx * t2 / 100)
        parts.append((f'Calculate the fixed cost per unit if capacity utilisation rises to {t2}%, and explain the significance of the change.',
                      f'{m2(fc / o2)}; lower fixed cost per unit makes the business more price competitive or raises its profit margin.',
                      f'{o2:,} units [1]; ${fc:,} ÷ {o2:,} = {m2(fc / o2)} [1]; significance [1] [3]'))
    c_, ds = num_opts(pc, out / mx * 100, [mx / out * 100, 100 - out / mx * 100, out / mx])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the capacity utilisation?', c_, ds, f'{out:,} ÷ {mx:,} × 100'),
            'err': (f'calculated capacity utilisation as {pc(mx / out * 100)}', 'maximum capacity was divided by actual output instead of output by maximum capacity', pc(out / mx * 100), f'{out:,} ÷ {mx:,} × 100', 'capacity utilisation')}


t = T(15, 'Excess capacity and capacity shortage: responses', ['excess capacity and capacity shortage: responses', 'excess capacity', 'capacity shortage'],
      defs=[('excess capacity', 'When a business\'s current output is below its maximum capacity, so some resources are under-used.'),
            ('capacity shortage', 'When demand is greater than the business\'s maximum capacity.'),
            ('rationalisation', 'Reducing capacity, for example by closing a factory or selling machinery, to cut costs and increase capacity utilisation.')],
      mcqs=[('Which is a long-term response to excess capacity?', 'Closing one factory (rationalisation)', ['Asking workers to work overtime', 'Subcontracting orders to another firm', 'Buying more machinery'],
             'Reducing capacity raises utilisation.'),
            ('A business with a capacity shortage could', 'subcontract some production to another firm', ['close a factory', 'cut the workforce', 'reduce prices to increase demand'],
             'Outsourcing increases effective capacity.'),
            ('Which is a way of increasing capacity utilisation by raising demand?', 'Using promotion to increase sales', ['Reducing the number of machines only', 'Making workers redundant', 'Closing a branch'],
             'Higher demand fills spare capacity.')],
      exps=[('Explain two ways a business could respond to excess capacity.', 'It could increase demand through promotion, price cuts or new markets so more output is sold; or reduce capacity by rationalisation, such as closing a factory.', '2 × (1 mark response, 1 mark explanation): increase demand, rent out space, make products for other firms, rationalise. [4]'),
            ('Explain why a business might not want to increase its capacity even though demand is greater than capacity.', 'The extra demand may be temporary, so new capacity would later be under-used; and building capacity is expensive and risky.', '1 mark temporary demand; 1 mark cost/risk. [2]')],
      adv=[('closing one of its sites to reduce excess capacity', ['higher capacity utilisation', 'lower fixed costs', 'cash from selling assets'],
            ['redundancy costs and low morale', 'cannot meet future growth in demand', 'bad publicity']),
           ('using overtime to deal with a capacity shortage', ['quick response', 'no investment needed', 'workers earn more'],
            ['higher wage costs', 'tiredness reduces quality', 'only a short-term solution'])],
      anl=[('Analyse how {b} could respond to a capacity shortage.', ['a capacity shortage means demand exceeds capacity', 'overtime or extra shifts in the short term', 'subcontracting or outsourcing', 'investing in new capacity in the long term']),
           ('Analyse how {b} could deal with excess capacity.', ['excess capacity means output is below maximum', 'increase demand through promotion or new markets', 'rent out spare capacity', 'rationalisation by closing a site'])],
      ev=[('Evaluate the best way for {b} to deal with demand that is greater than its capacity.', ['overtime is quick', 'subcontracting avoids investment', 'new capacity allows growth'],
           ['overtime is costly and short-term', 'subcontracting risks quality', 'new capacity is expensive and risky'],
           ['whether the demand is permanent', 'the finance available', 'quality requirements'])])


t = T(15, 'Outsourcing: reasons, benefits and risks', ['outsourcing: reasons, benefits and risks', 'outsourcing', 'subcontracting'],
      defs=[('outsourcing', 'Using another business (a third party) to carry out activities that were previously done within the business.'),
            ('core activities', 'The activities that are central to a business and give it its competitive advantage.')],
      mcqs=[('Which is the best example of outsourcing?', 'A bank paying another firm to run its call centre', ['A bank opening a new branch', 'A bank training its own staff', 'A bank merging with another bank'],
             'An external firm carries out the activity.'),
            ('A main reason for outsourcing is to', 'reduce costs and focus on core activities', ['increase control over quality', 'employ more staff', 'avoid all risks'],
             'Specialist firms may do it cheaper.'),
            ('A risk of outsourcing is', 'loss of control over quality and reliability', ['higher fixed costs', 'more management time on non-core work', 'less flexibility'],
             'The work is done by another firm.')],
      exps=[('Explain two benefits of outsourcing.', 'Specialist firms may do the work more cheaply and to a higher standard; and the business can focus its managers and resources on its core activities.', '2 × (1 mark benefit, 1 mark explanation): lower costs, expertise, focus on core, flexibility, extra capacity. [4]'),
            ('Explain one risk to a business of outsourcing an activity.', 'It loses direct control over quality and delivery, so poor performance by the outsourcing firm can damage its reputation.', '1 mark risk; 1 mark explanation. [2]')],
      adv=[('outsourcing its customer service to another firm', ['lower costs', 'specialist expertise', 'focus on core activities'],
            ['loss of control over service quality', 'customers may dislike it', 'redundancies'])],
      anl=[('Analyse the benefits to {b} of outsourcing some of its activities.', ['outsourcing uses third parties', 'lower costs from specialist firms', 'focus on core activities such as producing {prod}', 'flexibility to increase capacity']),
           ('Analyse the risks to {b} of outsourcing production of {prod}.', ['outsourcing transfers activities to other firms', 'loss of control over quality', 'unreliable deliveries', 'ethical and reputational risks from suppliers'])],
      ev=[('Evaluate whether {b} should outsource part of its operations.', ['lower costs', 'expertise', 'focus on core'],
           ['quality control', 'reputation risks', 'loss of skills'],
           ['whether the activity is core', 'the reliability of the outsourcing partner', 'the cost savings'])])


# =====================================================================================
# 16 Business finance
# =====================================================================================

t = T(16, 'Need for business finance: start-up, working capital, expansion', ['need for business finance: start-up, working capital, expansion', 'business finance', 'start-up capital'],
      defs=[('start-up capital', 'The finance needed to set up a business, for example to buy equipment, premises and initial inventory.'),
            ('capital expenditure', 'Spending on non-current assets, such as buildings and machinery, that will be used for more than one year.'),
            ('revenue expenditure', 'Spending on day-to-day costs, such as wages, materials and rent.')],
      mcqs=[('Which is an example of capital expenditure?', 'Buying a new delivery van', ['Paying monthly wages', 'Buying raw materials', 'Paying the electricity bill'],
             'The van is a non-current asset.'),
            ('Why does a growing business often need more working capital?', 'It must buy more inventory and wait longer for payment from more customers', ['Its non-current assets fall', 'It needs fewer employees', 'It pays less tax'],
             'Growth increases inventory and receivables.'),
            ('Start-up capital is most likely to be needed for', 'buying equipment and initial inventory', ['paying dividends', 'repaying a takeover loan', 'buying back shares'],
             'New businesses need assets before trading.')],
      exps=[('Explain the difference between capital expenditure and revenue expenditure.', 'Capital expenditure is spending on non-current assets that are used for several years, such as machinery; revenue expenditure is spending on day-to-day running costs, such as wages and materials.', '1 mark capital expenditure; 1 mark revenue expenditure. [2]'),
            ('Explain two reasons why a business needs finance.', 'To start up, buying premises, equipment and initial inventory; and to expand, for example by building a new factory or entering new markets; also for working capital.', '2 × (1 mark reason, 1 mark explanation). [4]')],
      adv=[('raising finance to expand into {newmkt}', ['higher sales and growth', 'economies of scale', 'spreads risk across markets'],
            ['cost of finance (interest or dividends)', 'risk if the expansion fails', 'possible loss of control'])],
      anl=[('Analyse why {b} needs finance to launch {newprod}.', ['businesses need finance for start-up, working capital and expansion', 'capital expenditure on equipment', 'working capital for extra inventory and receivables', 'promotion costs before revenue arrives'])],
      ev=[('Evaluate the importance of finance to the growth of {b}.', ['finance needed for capital expenditure', 'working capital for larger operations', 'investment in new markets'],
           ['good management and marketing also needed', 'too much debt increases risk', 'growth can be funded gradually from profit'],
           ['the speed of growth planned', 'the cost of finance', 'the business\'s profitability'])])


t = T(16, 'Working capital and the cash cycle', ['working capital and the cash cycle', 'working capital', 'cash cycle'],
      defs=[('working capital', 'The finance available for day-to-day operations: current assets minus current liabilities.'),
            ('cash cycle', 'The time between paying cash for materials and receiving cash from customers for the finished goods.'),
            ('current assets', 'Assets that are expected to be turned into cash within one year, such as inventory, trade receivables and cash.'),
            ('current liabilities', 'Debts that must be paid within one year, such as trade payables and bank overdrafts.')],
      mcqs=[('Working capital is calculated as', 'current assets − current liabilities', ['non-current assets − current liabilities', 'revenue − cost of sales', 'current assets + current liabilities'],
             'Net current assets.'),
            ('Which would shorten the cash cycle?', 'Collecting cash from customers more quickly', ['Holding more inventory', 'Paying suppliers sooner', 'Allowing longer credit to customers'],
             'Cash comes back sooner.'),
            ('A business with too little working capital may', 'be unable to pay its suppliers on time', ['have too much idle cash', 'pay too much interest on savings', 'have too many non-current assets'],
             'It lacks liquid resources.')],
      exps=[('Explain why a business can have too much working capital.', 'Too much cash or inventory is idle: inventory has storage costs and cash could have been invested in assets that earn a return.', '1 mark idle resources; 1 mark opportunity cost/storage costs. [2]'),
            ('Explain two ways a business could reduce the length of its cash cycle.', 'Hold less inventory, for example using JIT; and collect payment from customers faster, for example by offering discounts for early payment.', '2 × (1 mark method, 1 mark explanation): lower inventory, faster debt collection, longer supplier credit. [4]')],
      adv=[('reducing the credit period it gives to customers', ['cash received sooner', 'shorter cash cycle', 'fewer bad debts'],
            ['customers may go to competitors', 'may lose large customers', 'damages relationships'])],
      anl=[('Analyse how {b} could improve its working capital position.', ['working capital = current assets − current liabilities', 'reduce inventory held', 'collect cash from customers faster', 'negotiate longer credit from suppliers']),
           ('Analyse why a long cash cycle could cause problems for {b}.', ['the cash cycle is the time between paying for inputs and receiving cash from sales', 'cash is tied up in inventory and receivables', 'may need an overdraft with interest', 'may not be able to pay suppliers'])],
      ev=[('Evaluate the best way for {b} to manage its working capital.', ['lower inventory', 'faster collection from customers', 'longer credit from suppliers'],
           ['lower inventory risks stock-outs', 'customers may switch', 'suppliers may refuse'],
           ['its bargaining power', 'the industry\'s normal credit terms', 'the reliability of supply'])])


@spec(t)
def wc_calc(r, D):
    c = B(r)
    inv = step(r, 5000, 300000, 1000)
    rec = step(r, 5000, 300000, 1000)
    cash = step(r, 1000, 80000, 1000)
    pay = step(r, 5000, 250000, 1000)
    od = r.choice([0, 0, step(r, 2000, 50000, 1000)])
    ca, cl = inv + rec + cash, pay + od
    wc = ca - cl
    setup = (f'At the end of the year {c["b"]} had: inventory ${inv:,}; trade receivables ${rec:,}; cash ${cash:,}; trade payables ${pay:,}'
             + (f'; bank overdraft ${od:,}.' if od else '.'))
    parts = [('Calculate the working capital.', m(wc), f'Current assets {m(ca)} − current liabilities {m(cl)} [1]; = {m(wc)} [1] [2]'),
             ('Calculate the current ratio.', f'{ca / cl:.2f}:1', f'{m(ca)} ÷ {m(cl)} = {ca / cl:.2f}:1 [1] [1]')]
    if D >= 3:
        id_ = r.choice([30, 45, 60, 75, 90])
        rd = r.choice([20, 30, 45, 60])
        pd = r.choice([15, 30, 45, 60])
        cc = id_ + rd - pd
        parts.append((f'Inventory is held for {id_} days, customers take {rd} days to pay and suppliers are paid after {pd} days. Calculate the length of the cash cycle and explain one way to shorten it.',
                      f'{cc} days; e.g. collect from customers faster or hold less inventory.', f'{id_} + {rd} − {pd} = {cc} days [1]; method explained [1] [2]'))
    c_, ds = num_opts(m, wc, [ca + cl, ca - pay, inv + rec - cl])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the working capital?', c_, ds, f'{m(ca)} − {m(cl)}'),
            'err': (f'calculated working capital as {m(ca + cl)}', 'current liabilities were added to current assets instead of being subtracted', m(wc), f'{m(ca)} − {m(cl)}', 'working capital')}


t = T(16, 'Liquidity vs profitability', ['liquidity vs profitability', 'liquidity', 'profitability'],
      defs=[('liquidity', 'The ability of a business to pay its short-term debts as they fall due.'),
            ('profit', 'The amount by which revenue exceeds total costs in a period.'),
            ('cash flow', 'The movement of cash into and out of a business over a period of time.')],
      mcqs=[('A profitable business can still fail because', 'it runs out of cash to pay its debts', ['its revenue is greater than costs', 'it has too many customers', 'it pays too little tax'],
             'Profit is not the same as cash.'),
            ('Which transaction increases profit but not cash immediately?', 'A sale on credit', ['A cash sale', 'Receiving a bank loan', 'The owner putting in more capital'],
             'Revenue is recorded before cash is received.'),
            ('Which would improve liquidity but not affect profit?', 'Receiving a bank loan', ['Increasing selling prices', 'Reducing wages', 'Selling more goods at a profit'],
             'The loan is cash but not revenue.')],
      exps=[('Explain the difference between cash and profit.', 'Profit is revenue minus costs over a period; cash is the money actually received and paid. Credit sales and purchases, loans and capital spending mean they differ.', '1 mark profit; 1 mark cash; 1 mark example of difference. [3]'),
            ('Explain why liquidity is important for a business.', 'Without enough cash to pay suppliers, workers and lenders on time, a business may be forced to close even if it is profitable.', '1 mark pay short-term debts; 1 mark consequence of illiquidity. [2]')],
      adv=[('holding a large cash balance', ['can pay debts on time', 'can take advantage of opportunities', 'safety in a downturn'],
            ['cash earns little return', 'could be invested to raise profit', 'shareholders may want it returned'])],
      anl=[('Analyse why {b} could be profitable but have liquidity problems.', ['profit and cash are different', 'customers pay on credit after sales are recorded', 'cash spent on inventory and capital expenditure', 'loan repayments reduce cash but not profit']),
           ('Analyse the importance of liquidity to {b}.', ['liquidity is the ability to pay short-term debts', 'suppliers and staff must be paid on time', 'lack of cash may stop production', 'creditors may force the business into liquidation'])],
      ev=[('Evaluate whether liquidity is more important than profitability for {b}.', ['without cash the business cannot survive', 'short-term survival depends on liquidity', 'lenders and suppliers watch liquidity'],
           ['profit is needed in the long term', 'profitable firms can raise finance', 'too much cash lowers returns'],
           ['the time period considered', 'access to finance', 'the stage of the business'])])


t = T(16, 'Business failure: insolvency, liquidation and administration', ['business failure: insolvency, liquidation and administration', 'business failure', 'insolvency', 'liquidation'],
      defs=[('insolvency', 'When a business cannot pay its debts when they are due.'),
            ('liquidation', 'When a business stops trading and its assets are sold to pay its creditors.'),
            ('administration', 'When an insolvent company is run by an administrator who tries to rescue it or sell it as a going concern.')],
      mcqs=[('A company whose assets are sold to repay creditors after it stops trading is in', 'liquidation', ['administration', 'expansion', 'a joint venture'],
             'Liquidation ends the business.'),
            ('A common cause of business failure is', 'poor cash-flow management', ['high capacity utilisation', 'a strong brand', 'low labour turnover'],
             'Many firms fail because they run out of cash.'),
            ('The aim of administration is usually to', 'rescue the business or sell it as a going concern', ['pay dividends to shareholders', 'take over a competitor', 'float the company on the stock exchange'],
             'Administrators try to save the business.')],
      exps=[('Explain two reasons why new businesses often fail.', 'Poor cash-flow management means they run out of cash to pay debts; and lack of market research means demand is lower than expected.', '2 × (1 mark reason, 1 mark explanation): cash flow, poor planning, lack of experience, competition, economic downturn. [4]'),
            ('Explain the difference between insolvency and liquidation.', 'Insolvency is when the business cannot pay its debts when due; liquidation is the process of closing the business and selling its assets to pay creditors, which may follow insolvency.', '1 mark insolvency; 1 mark liquidation. [2]')],
      adv=[('entering administration rather than liquidation', ['business may be rescued', 'jobs may be saved', 'creditors may get more back'],
            ['loss of control by directors', 'damage to reputation', 'costs of administration'])],
      anl=[('Analyse the factors that could cause {b} to fail.', ['business failure often follows insolvency', 'poor cash-flow management', 'falling demand or strong competition', 'too much debt and high interest costs'])],
      ev=[('Evaluate the most likely cause of failure for a business such as {b}.', ['poor cash-flow management', 'strong competition', 'economic downturn'],
           ['several causes usually combine', 'management quality', 'external shocks'],
           ['the industry', 'the financial position', 'the experience of managers'])])


# =====================================================================================
# 17 Sources of finance
# =====================================================================================

t = T(17, 'Internal sources: retained earnings, sale of assets, working capital', ['internal sources: retained earnings, sale of assets, working capital', 'internal sources', 'retained earnings'],
      defs=[('internal finance', 'Finance raised from within the business, such as retained earnings, the sale of assets and reductions in working capital.'),
            ('retained earnings', 'Profit kept in the business after tax and dividends have been paid, used to finance the business.'),
            ('sale and leaseback', 'Selling an asset, such as a building, to raise cash and then leasing it back so that it can still be used.')],
      mcqs=[('Which is an internal source of finance?', 'Retained earnings', ['A bank loan', 'Issuing new shares', 'Trade credit'],
             'Retained profit comes from within.'),
            ('An advantage of retained earnings as a source of finance is that', 'there are no interest payments and no loss of control', ['it is always available to new businesses', 'it increases the amount of dividends paid', 'it is unlimited in amount'],
             'It is the business\'s own money.'),
            ('Selling a building and leasing it back provides', 'a large amount of cash while the business keeps using the building', ['a permanent reduction in costs', 'a new shareholder', 'an increase in non-current assets'],
             'Cash is released but rent must be paid.')],
      exps=[('Explain one advantage and one disadvantage of using retained earnings to finance expansion.', 'Advantage: there is no interest to pay and no loss of control. Disadvantage: the amount is limited to past profits and shareholders receive lower dividends.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain how a business could raise finance by reducing its working capital.', 'It can reduce inventory and collect cash from customers faster, releasing cash that was tied up in current assets.', '1 mark reduce inventory/receivables; 1 mark releases cash. [2]')],
      adv=[('financing its expansion from retained earnings', ['no interest payments', 'no loss of control', 'no repayment needed'],
            ['limited amount', 'lower dividends', 'opportunity cost of the cash'])],
      anl=[('Analyse the internal sources of finance available to {b}.', ['internal finance comes from within the business', 'retained earnings from past profits', 'sale of unused assets or sale and leaseback', 'releasing cash from working capital'])],
      ev=[('Evaluate whether {b} should use internal sources of finance to fund the launch of {newprod}.', ['no interest or loss of control', 'quick to access', 'no external approval needed'],
           ['may not be enough', 'lower dividends', 'reduces cash buffer'],
           ['the amount needed', 'past profitability', 'shareholders\' expectations'])])


t = T(17, 'External short-term sources: overdraft, trade credit, factoring', ['external short-term sources: overdraft, trade credit, factoring', 'overdraft', 'trade credit', 'factoring'],
      defs=[('bank overdraft', 'An arrangement with a bank allowing a business to spend more than it has in its account, up to an agreed limit.'),
            ('trade credit', 'An arrangement in which suppliers allow a business to pay for goods some time after they are delivered.'),
            ('debt factoring', 'Selling trade receivables to a specialist (factor) for less than their value in order to receive cash immediately.')],
      mcqs=[('Which source of finance is most suitable for a short-term cash shortage?', 'A bank overdraft', ['A 10-year bank loan', 'Issuing shares', 'A mortgage'],
             'Overdrafts are flexible short-term finance.'),
            ('A disadvantage of debt factoring is that', 'the business receives less than the full value of its receivables', ['it takes years to receive cash', 'it increases the number of shareholders', 'it must be repaid with interest over ten years'],
             'The factor charges a fee.'),
            ('Trade credit is', 'a period of time allowed by suppliers before payment is due', ['a long-term loan from a bank', 'a grant from the government', 'retained profit'],
             'Suppliers effectively finance the business.')],
      exps=[('Explain one advantage and one disadvantage of a bank overdraft.', 'Advantage: it is flexible – the business borrows only what it needs and pays interest only on that. Disadvantage: interest rates are high and the bank can demand repayment at short notice.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain how debt factoring improves a business\'s cash flow.', 'The factor pays most of the value of the receivables immediately, so the business does not have to wait for customers to pay.', '1 mark immediate cash; 1 mark no waiting for customers. [2]')],
      adv=[('using debt factoring', ['immediate cash', 'factor collects debts', 'reduces risk of bad debts'],
            ['lower revenue received', 'customers may dislike it', 'cost of the factor\'s fee']),
           ('increasing its use of trade credit', ['no interest', 'improves cash flow', 'easy to arrange'],
            ['loss of early payment discounts', 'damages supplier relations if late', 'suppliers may refuse more credit'])],
      anl=[('Analyse the short-term sources of finance available to {b}.', ['short-term finance is repaid within a year', 'bank overdraft for flexible borrowing', 'trade credit from suppliers', 'debt factoring to receive cash from receivables'])],
      ev=[('Evaluate the most suitable short-term source of finance for {b} to deal with a cash-flow problem.', ['overdraft is flexible', 'trade credit has no interest', 'factoring gives immediate cash'],
           ['overdraft interest is high', 'suppliers may refuse more credit', 'factoring reduces revenue'],
           ['the cause and length of the cash problem', 'its relationship with suppliers and bank', 'the cost of each source'])])


t = T(17, 'External long-term sources: loans, share capital, venture capital, crowdfunding', ['external long-term sources: loans, share capital, venture capital, crowdfunding', 'long-term sources', 'share capital', 'venture capital', 'crowdfunding'],
      defs=[('bank loan', 'A fixed amount of finance borrowed from a bank for an agreed period, repaid with interest in instalments.'),
            ('share capital', 'Finance raised by a limited company by selling shares to investors.'),
            ('venture capital', 'Finance provided to small or new businesses with growth potential by specialist investors in return for shares and often some control.'),
            ('crowdfunding', 'Raising finance from a large number of people, each contributing a small amount, usually through an online platform.')],
      mcqs=[('Which source of finance involves giving up part of the ownership of the business?', 'Selling shares', ['A bank loan', 'A bank overdraft', 'Trade credit'],
             'Shareholders become part-owners.'),
            ('Venture capitalists usually expect', 'a share of ownership and a high return', ['no return at all', 'repayment within one month', 'to manage the business alone'],
             'They take risk in return for equity.'),
            ('An advantage of a bank loan compared with selling shares is that', 'the owners keep control of the business', ['no interest is paid', 'it never has to be repaid', 'it needs no security'],
             'Lenders do not become owners.'),
            ('Crowdfunding is most likely to be used by', 'a new business with an appealing idea for the public', ['a large multinational', 'a government department', 'a business in liquidation'],
             'It suits new businesses that attract many small investors.')],
      exps=[('Explain one advantage and one disadvantage of using share capital to finance expansion.', 'Advantage: it does not have to be repaid and no interest is paid. Disadvantage: the original owners lose some control and future profits are shared as dividends.', '1 mark advantage, 1 mark explanation; 1 mark disadvantage, 1 mark explanation. [4]'),
            ('Explain why a new business might find it difficult to obtain a bank loan.', 'It has no trading record and may have few assets to offer as security, so the bank sees it as high risk.', '1 mark no track record; 1 mark lack of security/high risk. [2]'),
            ('Explain two benefits of crowdfunding for a new business.', 'It can raise finance when banks will not lend; and it tests public interest in the product and creates early customers and publicity.', '2 × (1 mark benefit, 1 mark explanation). [4]')],
      adv=[('taking a long-term bank loan', ['owners keep control', 'fixed repayments help planning', 'interest is a tax-deductible cost'],
            ['interest must be paid even if profits fall', 'security needed', 'increases gearing and risk']),
           ('raising finance from venture capitalists', ['large sums for growth', 'expert advice and contacts', 'no interest payments'],
            ['loss of ownership and control', 'investors expect high returns', 'pressure for fast growth'])],
      anl=[('Analyse the long-term sources of finance {b} could use to expand into {newmkt}.', ['long-term finance is repaid over more than a year', 'bank loans with interest and repayment', 'share capital with dilution of control', 'venture capital or crowdfunding for growth businesses'])],
      ev=[('Evaluate whether {b} should use a bank loan or share capital to fund its expansion.', ['loan keeps control', 'shares need no repayment', 'shares avoid interest costs'],
           ['loan increases risk and interest', 'shares dilute control', 'dividends expected'],
           ['the owners\' attitude to control', 'interest rates', 'the risk of the project'])])


t = T(17, 'Choosing the appropriate source of finance', ['choosing the appropriate source of finance', 'appropriate source of finance', 'choosing finance'],
      defs=[('cost of finance', 'The interest, dividends, fees or loss of control that a business must accept to obtain a source of finance.'),
            ('security (collateral)', 'An asset that a borrower promises to a lender, which the lender can sell if the loan is not repaid.')],
      mcqs=[('Which factor is most important when choosing finance to buy a new factory?', 'The finance should be long term to match the life of the asset', ['The finance should be repayable within one month', 'Only an overdraft should be used', 'The cheapest short-term source should be used'],
             'Long-term assets need long-term finance.'),
            ('A sole trader cannot raise finance by', 'selling shares on the stock exchange', ['taking a bank loan', 'using an overdraft', 'using trade credit'],
             'Only plcs can sell shares publicly.'),
            ('A business with high existing borrowing is most likely to choose', 'equity (share) finance', ['another large bank loan', 'a larger overdraft', 'more trade credit only'],
             'More debt would increase risk.')],
      exps=[('Explain two factors a business should consider when choosing a source of finance.', 'The purpose and time period: long-term assets need long-term finance; and the cost, including interest and loss of control.', '2 × (1 mark factor, 1 mark explanation): purpose/time, cost, amount, legal structure, existing debt, control. [4]'),
            ('Explain why the legal structure of a business affects the sources of finance available.', 'Only limited companies can sell shares, and only plcs can sell them to the public; sole traders and partnerships rely on owners\' funds and loans.', '1 mark shares only for companies; 1 mark consequence for unincorporated businesses. [2]')],
      adv=[('matching long-term finance to long-term investment', ['repayments spread over the asset\'s life', 'avoids cash-flow problems', 'lower annual costs'],
            ['total interest paid is higher', 'commitment over many years', 'may need security'])],
      anl=[('Analyse the factors {b} should consider when choosing how to finance {newprod}.', ['the choice of finance depends on several factors', 'amount and time period needed', 'cost of each source', 'legal structure as a {form} and existing debt'])],
      ev=[('Evaluate the most appropriate source of finance for {b} to fund the launch of {newprod}.', ['retained earnings avoid interest', 'loans keep control', 'shares avoid repayment'],
           ['retained earnings may not be enough', 'loans add risk', 'shares dilute control'],
           ['the amount needed', 'its legal structure', 'the risk of the project'])])


# =====================================================================================
# 18 Forecasting and managing cash flows
# =====================================================================================

t = T(18, 'Purpose and construction of cash-flow forecasts', ['purpose and construction of cash-flow forecasts', 'cash-flow forecasts', 'cash flow forecast'],
      defs=[('cash-flow forecast', 'An estimate of the cash inflows and cash outflows of a business, usually month by month, for a future period.'),
            ('net cash flow', 'Cash inflows minus cash outflows in a period.'),
            ('opening balance', 'The amount of cash a business has at the start of a period, equal to the closing balance of the previous period.'),
            ('closing balance', 'The amount of cash at the end of a period: opening balance plus net cash flow.')],
      mcqs=[('Opening balance $2,000; cash inflows $15,000; cash outflows $18,500. The closing balance is', '−$1,500', ['$1,500', '−$3,500', '$5,500'],
             '2,000 + 15,000 − 18,500.'),
            ('Which is a cash inflow?', 'A bank loan received', ['Wages paid', 'Rent paid', 'Purchase of materials'],
             'Money coming into the business.'),
            ('A main purpose of a cash-flow forecast is to', 'identify periods when the business may need extra finance', ['calculate profit for the year', 'value the business', 'measure market share'],
             'It warns of cash shortages.')],
      exps=[('Explain two benefits to a business of preparing a cash-flow forecast.', 'It shows when cash shortages may occur, so an overdraft can be arranged in advance; and it is needed to support applications for loans.', '2 × (1 mark benefit, 1 mark explanation): identify shortages, plan finance, support loan applications, set targets/monitor. [4]'),
            ('Explain why the closing balance of one month is the opening balance of the next month.', 'The cash the business has at the end of one month is the cash it starts with at the beginning of the next.', '1 mark same cash carried forward; 1 mark link between months. [2]')],
      adv=[('preparing monthly cash-flow forecasts', ['warns of cash shortages', 'helps obtain finance', 'targets to monitor'],
            ['based on estimates', 'takes time', 'may be inaccurate if conditions change'])],
      anl=[('Analyse how a cash-flow forecast could help {b} launch {newprod}.', ['a cash-flow forecast estimates future inflows and outflows', 'shows months with negative balances', 'helps arrange finance in advance', 'supports a loan application to the bank'])],
      ev=[('Evaluate the usefulness of cash-flow forecasting to {b}.', ['plans finance', 'warns of shortages', 'supports loan applications'],
           ['based on estimates', 'external changes', 'only as good as the assumptions'],
           ['how predictable sales are', 'how often it is updated', 'the experience of the managers'])])


@spec(t)
def cf_calc(r, D):
    c = B(r)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    k = 2 if D <= 2 else 3
    i0 = r.randrange(0, 12 - k)
    ms = months[i0:i0 + k]
    ob = step(r, 0, 20000, 500) * r.choice([1, 1, -1])
    rows = []
    bal = ob
    for _ in ms:
        cs = step(r, 10000, 60000, 500)
        cr = step(r, 5000, 40000, 500)
        wa = step(r, 5000, 30000, 500)
        ma = step(r, 5000, 40000, 500)
        ot = step(r, 1000, 15000, 500)
        inflow, outflow = cs + cr, wa + ma + ot
        net = inflow - outflow
        rows.append((cs, cr, wa, ma, ot, inflow, outflow, net, bal, bal + net))
        bal += net
    setup = (f'{c["b"]} has prepared a cash-flow forecast. The opening cash balance for {ms[0]} is {m(ob)}. Forecast figures are: ' +
             '; '.join(f'{mn} – cash sales ${x[0]:,}, receipts from credit customers ${x[1]:,}, wages ${x[2]:,}, materials ${x[3]:,}, other costs ${x[4]:,}' for mn, x in zip(ms, rows)) + '.')
    parts = [(f'Calculate the net cash flow for {ms[0]}.', m(rows[0][7]), f'Inflows {m(rows[0][5])} − outflows {m(rows[0][6])} [1]; = {m(rows[0][7])} [1] [2]'),
             (f'Calculate the closing balance for each month.', '; '.join(f'{mn} {m(x[9])}' for mn, x in zip(ms, rows)),
              '; '.join(f'{mn}: {m(x[8])} + ({m(x[7])}) = {m(x[9])}' for mn, x in zip(ms, rows)) + f' [{k}] [{k}]')]
    neg = [mn for mn, x in zip(ms, rows) if x[9] < 0]
    if D >= 3:
        parts.append(('Recommend one action the business could take based on this forecast.', (f'The balance is negative in {", ".join(neg)}, so arrange an overdraft in advance or delay some payments.' if neg else 'Balances stay positive, so surplus cash could be used, e.g. to pay suppliers early for a discount or to invest.'),
                      'Action linked to the forecast balances [1]; justification [1] [2]'))
    c_, ds = num_opts(m, rows[0][9], [rows[0][7], ob - rows[0][7], rows[0][5] + ob])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': (f'What is the closing balance for {ms[0]}?', c_, ds, f'{m(ob)} + {m(rows[0][7])}'),
            'err': (f'calculated the closing balance for {ms[0]} as {m(rows[0][7])}', 'the opening balance was not added to the net cash flow', m(rows[0][9]), f'{m(ob)} + ({m(rows[0][7])})', 'closing balance') if ob else None}


t = T(18, 'Interpreting cash-flow forecasts and their limitations', ['interpreting cash-flow forecasts and their limitations', 'interpreting cash-flow forecasts', 'limitations of cash-flow forecasts'],
      defs=[('cash shortage', 'A period in which a business does not have enough cash to make its planned payments.'),
            ('cash surplus', 'A period in which a business has more cash than it needs for its planned payments.')],
      mcqs=[('A negative closing balance in a cash-flow forecast means the business', 'will need an overdraft or other finance in that month', ['has made a loss for the year', 'has too much cash', 'has no customers'],
             'Planned payments exceed available cash.'),
            ('Which is a limitation of a cash-flow forecast?', 'Sales and costs are estimates that may be wrong', ['It cannot show monthly figures', 'It ignores cash', 'It is the same as the income statement'],
             'Forecasts depend on assumptions.'),
            ('Which is most likely to make a cash-flow forecast inaccurate?', 'An unexpected rise in the price of materials', ['Stable costs', 'Accurate market research', 'Regular monthly payments'],
             'Unexpected changes alter outflows.')],
      exps=[('Explain two limitations of cash-flow forecasts.', 'Sales are hard to predict, especially for new businesses; and costs may change unexpectedly, for example because of inflation or a change in the exchange rate.', '2 × (1 mark limitation, 1 mark explanation). [4]'),
            ('Explain why a business with a forecast cash surplus should still monitor its cash flow.', 'Actual results may differ from the forecast, so monitoring allows quick action if customers pay late or costs rise.', '1 mark actual differs from forecast; 1 mark early action. [2]')],
      adv=[('regularly comparing actual cash flows with the forecast', ['early warning of problems', 'improves future forecasts', 'better control of spending'],
            ['takes management time', 'may lead to over-reaction', 'needs accurate records'])],
      anl=[('Analyse the reasons why the cash-flow forecast of {b} might be inaccurate.', ['cash-flow forecasts are based on estimates', 'sales may differ from expectations', 'costs may rise because of inflation or exchange rates', 'customers may pay late'])],
      ev=[('Evaluate how far {b} can rely on its cash-flow forecast when planning to launch {newprod}.', ['shows likely finance needs', 'based on research', 'helps negotiate with the bank'],
           ['new product sales hard to predict', 'costs uncertain', 'external events'],
           ['the quality of the market research', 'how often it is updated', 'stability of the market'])])


t = T(18, 'Methods of improving cash flow', ['methods of improving cash flow', 'improving cash flow', 'cash flow problems'],
      defs=[('cash inflow', 'Money coming into a business, for example from sales, loans or the sale of assets.'),
            ('cash outflow', 'Money leaving a business, for example to pay wages, suppliers, rent and loan repayments.')],
      mcqs=[('Which would improve cash flow in the short term?', 'Asking customers to pay more quickly', ['Allowing customers more time to pay', 'Buying more inventory', 'Paying suppliers earlier'],
             'Inflows arrive sooner.'),
            ('Leasing equipment instead of buying it improves cash flow because', 'the business avoids a large single cash outflow', ['it costs less in total in every case', 'the business owns the equipment', 'it increases revenue'],
             'Payments are spread over time.'),
            ('A risk of delaying payments to suppliers is that', 'suppliers may refuse future credit', ['cash flow becomes worse', 'customers pay later', 'interest is earned'],
             'Supplier relationships suffer.')],
      exps=[('Explain two ways a business could improve its cash flow.', 'Increase inflows by offering discounts for early payment or using debt factoring; and reduce or delay outflows, for example by leasing rather than buying equipment or negotiating longer credit from suppliers.', '2 × (1 mark method, 1 mark explanation). [4]'),
            ('Explain one disadvantage of cutting prices to improve cash flow.', 'Cash comes in faster if more is sold, but the profit margin on each sale falls and the brand image may suffer.', '1 mark disadvantage; 1 mark explanation. [2]')],
      adv=[('offering customers a discount for early payment', ['cash received sooner', 'fewer bad debts', 'improved liquidity'],
            ['lower revenue per sale', 'customers may expect discounts permanently', 'some customers still pay late'])],
      anl=[('Analyse how {b} could improve its cash flow.', ['cash flow is the movement of cash in and out', 'speed up inflows: faster collection, factoring', 'delay outflows: longer supplier credit, leasing', 'reduce costs or inventory'])],
      ev=[('Evaluate the best way for {b} to improve its cash flow.', ['faster collection from customers', 'longer supplier credit', 'leasing instead of buying'],
           ['customers may switch', 'suppliers may refuse', 'leasing costs more in the long run'],
           ['the cause of the cash-flow problem', 'its bargaining power', 'whether the problem is short or long term'])])


# =====================================================================================
# 19 Costs
# =====================================================================================

t = T(19, 'Fixed, variable, semi-variable, direct and indirect costs', ['fixed, variable, semi-variable, direct and indirect costs', 'fixed costs', 'variable costs', 'direct costs'],
      defs=[('fixed costs', 'Costs that do not change with the level of output in the short run, such as rent and salaries.'),
            ('variable costs', 'Costs that change in direct proportion to the level of output, such as raw materials.'),
            ('semi-variable costs', 'Costs that have both a fixed and a variable element, such as a phone bill with a fixed rental plus call charges.'),
            ('direct costs', 'Costs that can be identified with a particular product or cost centre, such as materials used in making it.'),
            ('indirect costs (overheads)', 'Costs that cannot be identified with a particular product and are shared across the business, such as rent and administration.')],
      mcqs=[('Which is a variable cost for a furniture maker?', 'Wood used in production', ['Factory rent', 'Manager\'s salary', 'Insurance of the building'],
             'Materials vary with output.'),
            ('Fixed costs $40,000; variable cost $5 per unit; output 10,000 units. Total cost is', '$90,000', ['$45,000', '$50,000', '$400,000'],
             '40,000 + 5 × 10,000.'),
            ('As output increases, average fixed cost', 'falls', ['rises', 'stays the same', 'becomes zero'],
             'Fixed costs are spread over more units.'),
            ('A salesperson paid a basic salary plus commission is an example of a', 'semi-variable cost', ['fixed cost', 'variable cost only', 'direct material cost'],
             'Fixed salary plus variable commission.')],
      exps=[('Explain the difference between fixed costs and variable costs.', 'Fixed costs, such as rent, stay the same whatever the output in the short run; variable costs, such as materials, change in proportion to output.', '1 mark fixed with example; 1 mark variable with example. [2]'),
            ('Explain why it is useful for a business to classify its costs.', 'Knowing which costs are fixed and variable allows it to calculate break-even and contribution, set prices and see how costs change with output.', '1 mark break-even/contribution; 1 mark pricing/decisions. [2]')],
      adv=[('changing more of its fixed costs into variable costs, e.g. by outsourcing', ['lower break-even output', 'less risk if sales fall', 'flexibility'],
            ['higher cost per unit at high output', 'less control', 'supplier margin paid'])],
      anl=[('Analyse how {b} could use information about its fixed and variable costs.', ['costs can be classified as fixed or variable', 'calculate break-even output', 'set prices that cover costs', 'decide whether to accept extra orders'])],
      ev=[('Evaluate whether {b} should try to reduce its fixed costs or its variable costs.', ['lower fixed costs reduce break-even', 'lower variable costs raise contribution per unit', 'both improve profit'],
           ['fixed cost cuts may reduce capacity or quality', 'variable cost cuts may reduce quality', 'supplier relations'],
           ['its level of output', 'the structure of its costs', 'quality needs'])])


@spec(t)
def cost_calc(r, D):
    c = B(r)
    fc = step(r, 10000, 400000, 1000)
    vc = step(r, 2, 80, 1) + r.choice([0, 0.5])
    q = step(r, 1000, 50000, 500)
    tc = fc + vc * q
    ac = tc / q
    setup = f'{c["b"]} has fixed costs of ${fc:,} a month and variable costs of ${vc:.2f} per unit. It produces {q:,} units a month.'
    parts = [('Calculate the total cost.', m(tc), f'${fc:,} + ${vc:.2f} × {q:,} [1]; = {m(tc)} [1] [2]'),
             ('Calculate the average cost per unit.', m2(ac), f'{m(tc)} ÷ {q:,} = {m2(ac)} [1] [1]')]
    if D >= 3:
        q2 = q * 2
        ac2 = (fc + vc * q2) / q2
        parts.append((f'Calculate the average cost per unit if output doubles to {q2:,} units and explain why it changes.', f'{m2(ac2)}; fixed costs are spread over more units.',
                      f'(${fc:,} + ${vc:.2f} × {q2:,}) ÷ {q2:,} = {m2(ac2)} [1]; fixed costs spread [1] [2]'))
    c_, ds = num_opts(m, tc, [fc + vc, vc * q, fc * vc])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the total cost?', c_, ds, f'${fc:,} + ${vc:.2f} × {q:,}'),
            'err': (f'calculated average cost as {m2(vc + fc)}', 'the total fixed costs were added to variable cost per unit instead of fixed cost per unit', m2(ac), f'(${fc:,} + ${vc:.2f} × {q:,}) ÷ {q:,}', 'average cost')}


t = T(19, 'Break-even analysis: contribution, break-even output and margin of safety', ['break-even analysis: contribution, break-even output and margin of safety', 'break-even analysis', 'break-even', 'margin of safety', 'contribution'],
      defs=[('contribution per unit', 'Selling price minus variable cost per unit: the amount each unit contributes to fixed costs and then to profit.'),
            ('break-even output', 'The level of output at which total revenue equals total costs, so there is neither profit nor loss.'),
            ('margin of safety', 'The amount by which actual or planned output exceeds the break-even output.')],
      mcqs=[('Price $20; variable cost $12 per unit; fixed costs $40,000. Break-even output is', '5,000 units', ['2,000 units', '3,333 units', '1,250 units'],
             '40,000 ÷ (20 − 12).'),
            ('If the selling price rises and costs are unchanged, the break-even output', 'falls', ['rises', 'stays the same', 'doubles'],
             'Higher contribution per unit.'),
            ('Output 9,000 units; break-even 6,000 units. The margin of safety is', '3,000 units', ['15,000 units', '1.5 units', '6,000 units'],
             '9,000 − 6,000.')],
      exps=[('Explain the meaning of contribution.', 'Contribution is selling price minus variable cost; it is what each unit contributes first to covering fixed costs and then to profit.', '1 mark price − variable cost; 1 mark covers fixed costs then profit. [2]'),
            ('Explain why a business would want a large margin of safety.', 'Sales could fall by a large amount before the business makes a loss, so it is less risky.', '1 mark amount sales can fall; 1 mark lower risk of loss. [2]'),
            ('Explain how an increase in fixed costs affects break-even output.', 'More contribution is needed to cover the higher fixed costs, so more units must be sold to break even.', '1 mark more contribution needed; 1 mark break-even output rises. [2]')],
      adv=[('using break-even analysis before launching {newprod}', ['shows output needed to avoid a loss', 'tests effect of price changes', 'supports finance applications'],
            ['assumes all output is sold', 'costs and prices may change', 'only as good as the estimates'])],
      anl=[('Analyse how break-even analysis could help {b} decide whether to launch {newprod}.', ['break-even output = fixed costs ÷ contribution per unit', 'shows the sales needed to avoid a loss', 'margin of safety shows risk', 'tests different prices and costs'])],
      ev=[('Evaluate the usefulness of break-even analysis to {b}.', ['simple to calculate', 'shows sales needed', 'what-if analysis'],
           ['assumes constant prices and costs', 'assumes all output sold', 'single product only'],
           ['how accurate the estimates are', 'how stable the market is', 'whether other information is used'])])


@spec(t)
def be_calc(r, D):
    c = B(r)
    cpu = step(r, 2, 60, 1)
    vc = step(r, 2, 120, 1)
    p = vc + cpu
    beq = step(r, 1000, 40000, 100)
    fc = beq * cpu
    q = beq + step(r, -beq // 3, beq, 100)
    mos = q - beq
    prof = cpu * q - fc
    setup = f'{c["b"]} sells {c["newprod"]} for ${p} each. Variable cost is ${vc} per unit and fixed costs are ${fc:,} a year. It expects to sell {q:,} units a year.'
    parts = [('Calculate the contribution per unit.', f'${cpu}', f'${p} − ${vc} = ${cpu} [1] [1]'),
             ('Calculate the break-even output.', f'{beq:,} units', f'${fc:,} ÷ ${cpu} [1]; = {beq:,} units [1] [2]'),
             ('Calculate the margin of safety.', f'{mos:,} units', f'Break-even ${fc:,} ÷ ${cpu} = {beq:,} [1]; {q:,} − {beq:,} = {mos:,} units [1] [2]'),
             ('Calculate the expected profit.', m(prof), f'{q:,} × ${cpu} − ${fc:,} [1]; = {m(prof)} [1] [2]')]
    if D >= 3:
        p2 = p + r.choice([-2, -1, 1, 2, 3]) * max(1, cpu // 5)
        if p2 > vc:
            be2 = fc / (p2 - vc)
            parts.append((f'Calculate the new break-even output if the price changes to ${p2}.', f'{be2:,.0f} units (rounded up: {-(-fc // (p2 - vc)):,})',
                          f'${fc:,} ÷ (${p2} − ${vc}) = {be2:,.1f} [1]; {-(-fc // (p2 - vc)):,} units [1] [2]'))
    c_, ds = num_opts(lambda x: f'{int(round(x)):,} units', beq, [fc / p, fc / vc if vc else beq * 2, q - beq])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the break-even output?', c_, ds, f'${fc:,} ÷ ${cpu}'),
            'err': (f'calculated the break-even output as {fc / p:,.0f} units', 'fixed costs were divided by the selling price instead of contribution per unit', f'{beq:,} units', f'${fc:,} ÷ (${p} − ${vc})', 'break-even output')}


t = T(19, 'Break-even charts and limitations', ['break-even charts and limitations', 'break-even charts', 'limitations of break-even'],
      defs=[('break-even chart', 'A graph showing fixed costs, total costs and total revenue at different levels of output, with the break-even point where total revenue and total costs cross.'),
            ('break-even point', 'The point on a break-even chart where the total revenue line crosses the total cost line.')],
      mcqs=[('On a break-even chart, the total cost line starts', 'at the level of fixed costs on the vertical axis', ['at the origin', 'at the break-even point', 'at maximum output'],
             'At zero output total cost equals fixed cost.'),
            ('On a break-even chart, profit at a given output is shown by', 'the vertical distance between total revenue and total cost to the right of break-even', ['the fixed cost line', 'the gap between fixed and total cost', 'the slope of the revenue line'],
             'Profit = TR − TC.'),
            ('Which is a limitation of break-even analysis?', 'It assumes that all output produced is sold', ['It is very difficult to calculate', 'It uses variable costs', 'It cannot show profit'],
             'In reality not all output is sold.')],
      exps=[('Explain two limitations of break-even analysis.', 'It assumes all output is sold and that the selling price is the same at every level of output; in reality discounts are given and inventory builds up. It also assumes costs are linear.', '2 × (1 mark limitation, 1 mark explanation). [4]'),
            ('Explain what happens to a break-even chart if variable cost per unit rises.', 'The total cost line becomes steeper (starting from the same fixed cost), so it crosses total revenue at a higher output: break-even rises and the margin of safety falls.', '1 mark steeper TC; 1 mark higher break-even. [2]')],
      adv=[('presenting its costs and revenue on a break-even chart', ['shows break-even and profit visually', 'easy to show the effect of changes', 'useful for presentations to lenders'],
            ['time to draw accurately', 'based on simplifying assumptions', 'less precise than calculation'])],
      anl=[('Analyse how a break-even chart could help {b} plan its output of {prod}.', ['a break-even chart shows TR, TC and FC', 'the break-even point and margin of safety', 'profit or loss at any output', 'effects of changing price or costs'])],
      ev=[('Evaluate whether {b} should rely on break-even analysis when setting its price.', ['shows effect of price on break-even', 'simple and visual', 'links to margin of safety'],
           ['ignores demand at each price', 'linear assumptions', 'competitors\' prices'],
           ['price elasticity of demand', 'reliability of cost data', 'the market'])])


@spec(t)
def bec_calc(r, D):
    c = B(r)
    cpu = step(r, 2, 40, 1)
    vc = step(r, 2, 80, 1)
    p = vc + cpu
    beq = step(r, 500, 20000, 100)
    fc = beq * cpu
    mx = beq * r.choice([2, 3])
    q = step(r, beq // 2, mx, 100)
    tr, tc = p * q, fc + vc * q
    setup = (f'A break-even chart for {c["b"]} is drawn for output from 0 to {mx:,} units. The fixed cost line is at ${fc:,}. '
             f'The total revenue line rises by ${p} per unit and the total cost line by ${vc} per unit.')
    parts = [('State the value of total cost at zero output.', f'${fc:,}', f'Total cost = fixed cost = ${fc:,} [1] [1]'),
             ('Calculate the output at which the total revenue and total cost lines cross.', f'{beq:,} units', f'${fc:,} ÷ (${p} − ${vc}) [1]; = {beq:,} units [1] [2]'),
             (f'Calculate the profit or loss shown on the chart at an output of {q:,} units.', ('Profit ' if tr >= tc else 'Loss ') + m(abs(tr - tc)),
              f'TR {q:,} × ${p} = {m(tr)}; TC ${fc:,} + {q:,} × ${vc} = {m(tc)} [1]; {"profit" if tr >= tc else "loss"} {m(abs(tr - tc))} [1] [2]')]
    if D >= 3:
        parts.append(('State two limitations of using this chart for decisions.', 'Assumes all output is sold at the same price; assumes costs rise in a straight line (no bulk discounts or overtime).', 'Two valid limitations [1 each] [2]'))
    c_, ds = num_opts(lambda x: f'{int(round(x)):,} units', beq, [fc / p, mx / 2, fc / vc])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('At what output do the total revenue and total cost lines cross?', c_, ds, f'${fc:,} ÷ ${cpu}'),
            'err': (f'read the profit at {q:,} units as {m(tr - fc)}', 'only fixed costs were deducted from revenue; total costs including variable costs must be used', ('profit ' if tr >= tc else 'loss ') + m(abs(tr - tc)), f'{m(tr)} − {m(tc)}', 'profit or loss')}


t = T(19, 'Uses of cost information: pricing and decisions', ['uses of cost information: pricing and decisions', 'cost information', 'contribution pricing'],
      defs=[('contribution pricing', 'Setting a price based on variable cost plus a contribution to fixed costs, often used for special orders when there is spare capacity.'),
            ('special order', 'A one-off order from a customer, often at a price lower than the normal price.')],
      mcqs=[('A business with spare capacity should accept a special order if the price is', 'above the variable cost per unit', ['above the full cost per unit only', 'below the variable cost per unit', 'equal to fixed costs'],
             'Any positive contribution increases profit when fixed costs are unchanged.'),
            ('Cost information helps managers to', 'set prices and decide whether to continue making a product', ['decide the colour of the logo', 'calculate the number of competitors', 'measure customer satisfaction'],
             'Costs underpin pricing and output decisions.'),
            ('Which is a risk of accepting a special order at a low price?', 'Regular customers may demand the same low price', ['Fixed costs will rise automatically', 'Contribution will be negative', 'Capacity utilisation will fall'],
             'It may undermine normal prices.')],
      exps=[('Explain why a business might accept an order at a price below its average total cost.', 'If it has spare capacity and fixed costs are already covered, any price above variable cost gives a positive contribution that increases profit.', '1 mark spare capacity/fixed costs covered; 1 mark positive contribution adds to profit. [2]'),
            ('Explain two ways that cost information helps a business make decisions.', 'It allows prices to be set that cover costs and give a profit; and it shows whether a product or order makes a positive contribution, helping decisions about continuing or accepting it.', '2 × (1 mark use, 1 mark explanation). [4]')],
      adv=[('accepting special orders at contribution prices', ['uses spare capacity', 'extra contribution to profit', 'may win new customers'],
            ['regular customers may want lower prices', 'uses capacity needed for full-price orders', 'may damage brand image'])],
      anl=[('Analyse how cost information could help {b} decide the price of {newprod}.', ['costs can be classified as fixed and variable', 'cost-plus pricing to cover all costs', 'contribution pricing for special orders', 'comparison with competitors\' prices'])],
      ev=[('Evaluate whether {b} should accept a large one-off order at a price below its normal price.', ['positive contribution', 'uses spare capacity', 'new customer'],
           ['regular customers may want discounts', 'capacity may be needed', 'brand damage'],
           ['spare capacity', 'whether price exceeds variable cost', 'long-term customer relations'])])


@spec(t)
def so_calc(r, D):
    c = B(r)
    vc = step(r, 5, 80, 1)
    p = round(vc * r.uniform(1.4, 2.2))
    fcu = round((p - vc) * r.uniform(0.4, 0.9), 2)
    full = vc + fcu
    oq = step(r, 500, 10000, 100)
    op = round(vc * r.uniform(0.9, 1.3), 2)
    if abs(op - vc) < 0.5:
        return None
    contrib = (op - vc) * oq
    setup = (f'{c["b"]} normally sells a product for ${p}. Variable cost is ${vc} per unit and fixed costs per unit are ${fcu:.2f} at normal output, '
             f'so the full cost is ${full:.2f}. It has spare capacity. A new customer offers to buy {oq:,} units at ${op:.2f} each.')
    parts = [('Calculate the contribution from the order.', m(contrib), f'(${op:.2f} − ${vc}) × {oq:,} [1]; = {m(contrib)} [1] [2]'),
             ('State whether the order should be accepted on financial grounds and why.', ('Yes – the price is above variable cost, so profit rises by ' + m(contrib) if contrib > 0 else 'No – the price is below variable cost, so profit would fall by ' + m(-contrib)) + '.',
              f'Decision based on contribution {"positive" if contrib > 0 else "negative"} [1]; fixed costs unchanged [1] [2]')]
    if D >= 3:
        parts.append(('Explain one non-financial factor the business should consider before accepting.', 'E.g. whether regular customers will hear of the lower price and demand it, or the chance of repeat orders from the new customer.', 'Factor [1]; explanation [1] [2]'))
    c_, ds = num_opts(m, contrib, [(op - full) * oq, op * oq, (p - op) * oq])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the contribution from the order?', c_, ds, f'(${op:.2f} − ${vc}) × {oq:,}'),
            'err': (f'calculated the effect on profit as {m((op - full) * oq)} and so rejected the order' if op < full and contrib > 0 else f'calculated the contribution as {m(op * oq)}',
                    'the full cost including fixed costs was used, but fixed costs do not change with the order' if op < full and contrib > 0 else 'the revenue from the order was used without deducting the variable costs',
                    m(contrib), f'(${op:.2f} − ${vc}) × {oq:,}', 'contribution')}


t = T(19, 'Budgets: purpose, setting and variance basics', ['budgets: purpose, setting and variance basics', 'budgets', 'variance'],
      defs=[('budget', 'A financial plan for a future period, setting targets for revenue, costs or other items.'),
            ('variance', 'The difference between a budgeted figure and the actual figure.'),
            ('favourable variance', 'A variance that increases profit, e.g. actual costs lower than budget or actual revenue higher than budget.'),
            ('adverse variance', 'A variance that reduces profit, e.g. actual costs higher than budget or actual revenue lower than budget.')],
      mcqs=[('Budgeted wages $50,000; actual wages $54,000. The variance is', '$4,000 adverse', ['$4,000 favourable', '$104,000 adverse', '$54,000 adverse'],
             'Costs above budget reduce profit.'),
            ('Budgeted revenue $120,000; actual revenue $126,000. The variance is', '$6,000 favourable', ['$6,000 adverse', '$246,000 favourable', '$126,000 favourable'],
             'Revenue above budget increases profit.'),
            ('A main purpose of budgets is to', 'set targets and control spending', ['calculate the market share', 'replace the income statement', 'recruit staff'],
             'Budgets plan and control.')],
      exps=[('Explain two benefits to a business of setting budgets.', 'They set targets that motivate managers and coordinate departments; and they allow control, as variances show where performance differs from the plan.', '2 × (1 mark benefit, 1 mark explanation): planning, coordination, motivation, control/variance analysis. [4]'),
            ('Explain why involving managers in setting budgets can improve their motivation.', 'Managers who help set targets feel ownership and see them as realistic, so they are more committed to achieving them.', '1 mark involvement/ownership; 1 mark commitment. [2]')],
      adv=[('introducing departmental budgets', ['control of spending', 'clear targets', 'coordination between departments'],
            ['time to prepare', 'may be inflexible', 'managers may spend to use up the budget'])],
      anl=[('Analyse how budgets could help the managers of {b} control the business.', ['a budget is a financial plan', 'targets for revenue and costs', 'variances show differences from the plan', 'corrective action can be taken'])],
      ev=[('Evaluate the usefulness of budgeting to {b}.', ['planning and control', 'motivation', 'coordination'],
           ['may be inflexible', 'time-consuming', 'unrealistic targets demotivate'],
           ['how budgets are set', 'how often they are reviewed', 'the stability of the market'])])


@spec(t)
def var_calc(r, D):
    c = B(r)
    items = r.sample([('Revenue', 'rev'), ('Materials', 'cost'), ('Wages', 'cost'), ('Marketing', 'cost'), ('Rent', 'cost')], 3 if D <= 2 else 4)
    if not any(k == 'rev' for _, k in items):
        items[0] = ('Revenue', 'rev')
    rows = []
    for n_, k in items:
        b = step(r, 5000, 200000, 500)
        a = b + step(r, -b // 5, b // 5, 500) * r.choice([1, -1])
        if a == b:
            a += 500
        fav = (a > b) if k == 'rev' else (a < b)
        rows.append((n_, k, b, a, abs(a - b), 'F' if fav else 'A'))
    setup = f'{c["b"]} has the following budgeted and actual figures for last month: ' + '; '.join(f'{n_} – budget ${b:,}, actual ${a:,}' for n_, _, b, a, _, _ in rows) + '.'
    parts = [('Calculate the variance for each item and state whether it is favourable (F) or adverse (A).', '; '.join(f'{n_} ${v:,} {fa}' for n_, _, _, _, v, fa in rows),
              '; '.join(f'{n_} ${v:,} {fa}' for n_, _, _, _, v, fa in rows) + f' [1 each] [{len(rows)}]')]
    bp_ = sum(b if k == 'rev' else -b for _, k, b, _, _, _ in rows)
    ap_ = sum(a if k == 'rev' else -a for _, k, _, a, _, _ in rows)
    if D >= 3:
        parts.append(('Calculate the overall effect of these variances on profit.', ('Profit ' + ('higher' if ap_ > bp_ else 'lower') + ' than budget by ' + m(abs(ap_ - bp_))),
                      f'Sum of F − A variances [1]; {m(abs(ap_ - bp_))} {"favourable" if ap_ > bp_ else "adverse"} [1] [2]'))
        parts.append(('Suggest one reason for the revenue variance.', 'E.g. higher or lower sales volume or prices than planned, because of competitors, the economy or a promotion.', 'Reason linked to F/A [1] [1]'))
    rv = [x for x in rows if x[1] == 'rev'][0]
    wrong = 'A' if rv[5] == 'F' else 'F'
    c_, ds = (f'${rv[4]:,} {rv[5]}', [f'${rv[4]:,} {wrong}', f'${rv[2] + rv[3]:,} {rv[5]}', f'${rv[3]:,} {rv[5]}'])
    return {'setup': setup, 'parts': parts, 'c': c,
            'mcq': ('What is the revenue variance?', c_, ds, f'${rv[3]:,} − ${rv[2]:,}: actual revenue {"above" if rv[5] == "F" else "below"} budget'),
            'err': (f'described the revenue variance of ${rv[4]:,} as {"adverse" if rv[5] == "F" else "favourable"}', 'for revenue, actual above budget is favourable and actual below budget is adverse', f'${rv[4]:,} {"favourable" if rv[5] == "F" else "adverse"}', f'${rv[3]:,} − ${rv[2]:,}', 'variance')}


# =====================================================================================
# Post-processing: interleave C1 item kinds and give calculation templates extra weight
# =====================================================================================

GENERIC = {'def_short', 'mcq_fixed', 'def_mcq', 'def_rev', 'exp_fixed', 'adv_ex', 'anl_case', 'ev_case', 'case_comp', 'essay', 'pair'}


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
        extra = [x for x in rest if x.C == 'C3' and x.name not in GENERIC]
        _t.templates = _interleave(c1) + rest + extra
