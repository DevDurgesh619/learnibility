"""Cambridge International A Level Economics 9708 (A Level content, grade 12).

Topics 7-11 of the syllabus: the price system and the microeconomy (utility, indifference curves,
efficiency, externalities, costs, market structures, growth of firms, objectives, labour markets),
government microeconomic intervention, the macroeconomy, government macroeconomic intervention and
international economic issues. Items mirror Paper 3 (multiple choice) and Paper 4 (data response and
essays). Contexts use fictional countries and firms with realistic, generic figures.
"""
import math
import re

from ._lib import topic, mcq, compose, sf, fmt, person, city, near

PROFILE = {'mark_scale': {'long': (2, 2), 'case': (1.5, 1.5)}, 'wordy': True}
CHAPTERS = {}

# ----------------------------------------------------------------------------- contexts
COUNTRIES = ['Zentara', 'Kestria', 'Lunaria', 'Marvona', 'Nordavia', 'Pelora', 'Sundara', 'Valdoria', 'Calvania', 'Dravonia',
             'Esteria', 'Fendaria', 'Gorvania', 'Halvoria', 'Istrana', 'Jovania', 'Korvia', 'Loristan', 'Merania', 'Ostrelia',
             'Quentara', 'Rovania', 'Selmaria', 'Tarvia', 'Umbria Nova', 'Westaria']
FIRMS = ['Apex Ltd', 'Borealis plc', 'Cobalt Group', 'Delta Foods', 'Everline', 'Fenwick & Co', 'Granite Holdings', 'Horizon Corp',
         'Ironleaf', 'Juniper Brands', 'Keystone plc', 'Lumen Ltd', 'Meridian Group', 'Northwind', 'Orchid Ltd', 'Pinnacle plc',
         'Quarry Bay Ltd', 'Redwood Corp', 'Silverline', 'Tidewater plc']
GOODS = ['smartphones', 'bottled water', 'cinema tickets', 'coffee', 'running shoes', 'chocolate bars', 'bus journeys', 'electric scooters',
         'laptops', 'streaming subscriptions', 'rice', 'bicycles', 'restaurant meals', 'concert tickets', 'textbooks', 'gym memberships',
         'fresh fruit', 'airline seats', 'cement', 'printed newspapers']
INDUSTRIES = ['airline', 'cement', 'banking', 'supermarket', 'mobile telecommunications', 'car manufacturing', 'brewing', 'pharmaceutical',
              'steel', 'hotel', 'coffee shop', 'cinema', 'electricity supply', 'rail transport', 'fast-food', 'hairdressing', 'publishing',
              'soft drinks', 'shipbuilding', 'software']
_PH = re.compile(r'\{(\w+)\}')


def ctx(r):
    c1, c2, c3 = r.sample(COUNTRIES, 3)
    f1, f2 = r.sample(FIRMS, 2)
    g1, g2 = r.sample(GOODS, 2)
    i1, i2 = r.sample(INDUSTRIES, 2)
    return {'country': c1, 'country2': c2, 'country3': c3, 'firm': f1, 'firm2': f2, 'good': g1, 'good2': g2,
            'ind': i1, 'ind2': i2, 'a_ind': ('an ' if i1[0] in 'aeiou' else 'a ') + i1, 'city': city(r), 'person': person(r)}


def fill(s, d):
    return _PH.sub(lambda m: str(d.get(m.group(1), m.group(0))), s)


def money(x, cur='$', dp=2):
    neg = x < 0
    x = abs(x)
    if abs(x - round(x)) < 1e-9:
        s = f'{int(round(x)):,}'
    else:
        s = f'{x:,.{dp}f}'
    return ('−' if neg else '') + cur + s


def art(w):
    return ('an ' if w[:1].lower() in 'aeiou' else 'a ') + w


def pct(x, dp=1):
    return num(x, dp) + '%'


def num(x, dp=2):
    x = round(x, dp)
    if abs(x - round(x)) < 1e-9:
        v = int(round(x))
        return f'{v:,}' if abs(v) >= 10000 else str(v)
    return fmt(x, dp)


def dis_num(r, val, f, extra=()):
    """Distractor strings for a numeric answer."""
    c = f(val)
    out = []
    for v in list(extra) + [val * m for m in r.sample([0.5, 2, 1.5, 0.8, 1.25, 0.9, 1.1, 0.6], 8)] + [val + 1, val - 1] + ([-val] if val < 0 else []):
        s = f(v).replace('$-', '−$')
        if s != c and s not in out:
            out.append(s)
    return out


def cq(r, D, stem, ans, key, dis=None, mcq_D=(1,), typ=None):
    """Calculation item: MCQ at low difficulty when distractors are supplied."""
    if D in mcq_D and dis:
        opts, a = mcq(r, ans, dis)
        return {'stem': re.sub(r'^Calculate', 'What is', stem) if stem.startswith('Calculate') else stem, 'options': opts, 'answer': a, 'key': key}
    q = {'stem': stem, 'answer': ans, 'key': key}
    if typ:
        q['type'] = typ
    return q


def items(t, C, D, entries, typ=None, name='items'):
    """Register a template that draws one entry and fills its {placeholders} from a random context.
    entries: (stem, answer, key[, distractors]); with distractors the item is an MCQ."""
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


ESSAY_FORMS = ['Assess whether {p}.', 'Discuss whether {p}.', 'Evaluate the view that {p}.', 'Consider whether {p}.',
               '‘{P}.’ Discuss this view.', 'To what extent do you agree that {p}?', 'Discuss the extent to which {p}.',
               '‘{P}.’ Evaluate this statement.']


def essays(t, prompts, scenes, D=(2, 3, 4, 5)):
    """Paper 4 style essays. prompts: (claim, part_a_task, analysis, evaluation). scenes: context sentences with placeholders."""
    def fn(r, D_):
        claim, part_a, ana, ev = r.choice(prompts)
        d = ctx(r)
        scene = fill(r.choice(scenes), d) + ' ' if scenes and r.random() < 0.85 else ''
        form = r.choice(ESSAY_FORMS)
        main = fill(form.replace('{p}', claim).replace('{P}', claim[0].upper() + claim[1:]), d)
        a_ana, a_ev = fill(ana, d), fill(ev, d)
        if part_a and D_ >= 3 and r.random() < 0.55:
            pa = fill(part_a, d)
            stem = f'{scene}(a) {pa} (b) {main}'
            ans = (f'(a) Explanation of the theory (with a described diagram where relevant), drawing on: {a_ana} '
                   f'(b) Case for the view: {a_ana} Case against / evaluation: {a_ev} Conclusion: a judgement on the conditions under which the view holds.')
            key = ('(a) Knowledge and understanding of the theory, clear analytical chain; diagram described accurately with labelled axes and curves. '
                   '(b) Analysis of arguments for and against; evaluation reaches a justified conclusion that weighs the conditions under which the claim holds. '
                   'Top level needs a judgement, not just a summary.')
        else:
            stem = scene + main
            ans = f'Arguments for: {a_ana} Arguments against / evaluation: {a_ev} Conclusion: a supported judgement that depends on the conditions identified.'
            key = ('Knowledge and analysis (about 60%): accurate theory, logical chains of reasoning and a relevant diagram described with axes, curves and shifts. '
                   'Evaluation (about 40%): considers both sides, the assumptions and the context, and reaches a justified conclusion.')
        return {'stem': stem, 'answer': ans, 'key': key, 'type': 'long'}
    fn.__name__ = 'essay'
    t.add('C4', D, 'long')(fn)
    return fn


def table(headers, rows):
    """Render a small data table inline: 'Output: 1, 2, 3; Total cost ($): 10, 18, 24'."""
    cols = list(zip(*rows))
    return '; '.join(f'{h}: ' + ', '.join(num(v) if isinstance(v, (int, float)) else str(v) for v in col) for h, col in zip(headers, cols))


def add_many(topics, C, D, typ, fn):
    for tt in topics:
        tt.add(C, D, typ)(fn)


# ============================================================================ 1 Utility
t1_1 = topic('Total and marginal utility', 'total and marginal utility', 'diminishing marginal utility', 'utility')
t1_1.fixed('C1', (1, 2, 3), [
    ('What is meant by marginal utility?', 'The additional satisfaction gained from consuming one more unit of a good',
     'Marginal utility = change in total utility from one extra unit consumed (ΔTU/ΔQ).',
     ['The total satisfaction gained from all units consumed', 'Total utility divided by the number of units consumed', 'The price a consumer pays for the last unit bought']),
    ('The law of diminishing marginal utility states that, as consumption of a good increases,', 'each additional unit eventually adds less to total utility than the previous unit',
     'With other consumption held constant, MU of successive units eventually falls.',
     ['total utility falls from the first unit', 'the price of the good falls', 'marginal utility becomes negative immediately']),
    ('When total utility from a good is at its maximum, marginal utility is', 'zero', 'TU peaks where the next unit adds nothing: MU = 0.',
     ['at its maximum', 'equal to the price of the good', 'equal to average utility']),
    ('If marginal utility is positive but falling, total utility is', 'rising at a decreasing rate', 'Positive MU means TU rises; falling MU means each rise is smaller.',
     ['falling at an increasing rate', 'constant', 'rising at an increasing rate']),
    ('A consumer’s total utility rises from 40 to 52 utils when a fifth unit is consumed. The marginal utility of the fifth unit is', '12 utils', 'MU = 52 − 40 = 12 utils.',
     ['52 utils', '10.4 utils', '92 utils']),
    ('Define total utility.', 'The total satisfaction a consumer gains from consuming a given quantity of a good in a period of time.', '1 mark: total satisfaction from all units consumed in a time period [1]'),
])
t1_1.fixed('C2', (2, 3, 4), [
    ('Explain how the law of diminishing marginal utility helps to explain why an individual demand curve slopes downwards.',
     'A consumer buys a unit only if its marginal utility (in money terms) is at least its price. Because MU falls as more is consumed, the consumer will only buy extra units if the price falls, so quantity demanded rises as price falls.',
     '1 mark: consumer buys while MU ≥ P (or MU/P equalised); 1 mark: MU falls with extra units; 1 mark: so more units bought only at lower price, giving a downward-sloping demand curve [3]'),
    ('Explain the paradox of value (the diamonds–water paradox) using the distinction between total and marginal utility.',
     'Water has a very high total utility but, because it is plentiful, the marginal utility of the last unit consumed is low, so its price is low. Diamonds are scarce, so the marginal utility of the last unit is high and so is the price. Price reflects marginal, not total, utility.',
     '1 mark: water high TU, diamonds low TU; 1 mark: water abundant so low MU; 1 mark: price is linked to MU, not TU [3]'),
    ('Explain why total utility can still be increasing when marginal utility is falling.',
     'As long as marginal utility is positive, each extra unit adds something to total utility, so total utility rises, but by smaller amounts each time.',
     '1 mark: MU positive means TU rises; 1 mark: falling MU means TU rises at a decreasing rate [2]'),
    ('Explain why marginal utility theory assumes that utility is cardinal and why this is a weakness.',
     'Marginal utility theory measures satisfaction in units (utils) that can be added and compared, so it assumes utility is cardinal. In practice satisfaction is subjective and cannot be measured or compared numerically between people.',
     '1 mark: cardinal = measurable in units/utils; 1 mark: satisfaction subjective, cannot be measured [2]'),
])
items(t1_1, 'C2', (2, 3, 4), [
    ('{person} buys {good} every week. Explain, using the concept of marginal utility, why {person} is unlikely to buy many more units of {good} even if their income rises a little.',
     'Each additional unit gives less extra satisfaction than the last, so beyond a point the marginal utility of an extra unit falls below its price; {person} prefers to spend extra income on other goods with a higher MU per dollar.',
     '1 mark: diminishing MU of extra units; 1 mark: compares MU with price / MU per dollar of other goods [2]'),
    ('A cinema in {city} offers a second ticket in the same week at half price. Using marginal utility, explain why this pricing may increase the number of tickets sold.',
     'The marginal utility of a second film in a week is lower than the first, so many consumers would not pay full price for it. A lower price for the second ticket brings its price closer to (or below) its lower marginal utility, so more consumers buy it.',
     '1 mark: MU of second unit lower; 1 mark: price cut matches lower MU so purchase becomes worthwhile [2]'),
    ('Explain why a buffet restaurant in {city} can charge a single price yet expect most diners to stop eating long before they have eaten all the food on offer.',
     'Once the meal is paid for, the marginal price of extra food is zero, so diners eat until marginal utility falls to zero. Because marginal utility diminishes quickly, this happens after a limited number of plates.',
     '1 mark: marginal price zero so eat until MU = 0; 1 mark: diminishing MU limits consumption [2]'),
])


def _tu_table(r, D):
    n = 6 if D < 4 else 7
    start = r.choice([24, 30, 36, 40, 45, 50, 60])
    drops = [r.choice([3, 4, 5, 6, 8]) for _ in range(n - 1)]
    mu = [start]
    for dd in drops:
        mu.append(mu[-1] - dd)
    if D >= 3:  # make the last unit(s) negative so TU peaks
        mu[-1] = -r.choice([2, 3, 4])
        if mu[-2] <= 0:
            mu[-2] = r.choice([1, 2])
    mu = sorted(mu, reverse=True)
    for i in range(1, len(mu)):
        if mu[i] >= mu[i - 1]:
            mu[i] = mu[i - 1] - 1
    tu = []
    s = 0
    for m in mu:
        s += m
        tu.append(s)
    return mu, tu


@t1_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t1_1_tu(r, D):
    mu, tu = _tu_table(r, D)
    g = r.choice(GOODS)
    n = len(tu)
    tab = table(['Units of ' + g + ' consumed per week', 'Total utility (utils)'], list(zip(range(1, n + 1), tu)))
    k = r.randint(2, n)
    mode = r.choice(['mu', 'price', 'surplus', 'peak']) if D >= 3 else r.choice(['mu', 'price'])
    if mode == 'mu' or D <= 2 and mode not in ('price',):
        ans = f'{mu[k - 1]} utils'
        return cq(r, D, f'The table shows a consumer’s total utility. {tab}. Calculate the marginal utility of unit {k}.', ans,
                  f'MU = TU({k}) − TU({k - 1}) = {tu[k - 1]} − {tu[k - 2]} = {mu[k - 1]} utils.', dis_num(r, mu[k - 1], lambda x: f'{num(x)} utils', [tu[k - 1], tu[k - 1] / k]))
    if mode == 'price':
        p = r.choice([m for m in mu if m > 0][1:-1] or [mu[1]])
        p = p - r.choice([0, 1]) if p > 2 else p
        q = sum(1 for m in mu if m >= p)
        ans = f'{q} units'
        return cq(r, D, f'The table shows a consumer’s total utility, where 1 util is worth $1 to the consumer. {tab}. The price is ${p} per unit. Calculate how many units a rational consumer buys and explain your answer.',
                  ans, f'MU of each unit: {", ".join(map(str, mu))}. Buy every unit whose MU ≥ price (${p}) → {q} units [2]; the next unit has MU {mu[q] if q < n else "n/a"} < price [1].',
                  [f'{x} units' for x in (q + 1, q - 1 if q > 1 else q + 2, n, q + 2) if x != q][:3] + ['0 units'])
    if mode == 'surplus':
        p = max(1, mu[2] - r.choice([0, 1, 2]))
        q = sum(1 for m in mu if m >= p)
        cs = sum(m - p for m in mu if m >= p)
        return {'stem': f'A consumer values 1 util at $1. {tab}. The price is ${p}. Calculate (a) the quantity the consumer buys and (b) the consumer surplus gained.',
                'answer': f'(a) {q} units (b) ${cs}', 'key': f'MU per unit: {", ".join(map(str, mu))}. (a) Buy while MU ≥ ${p}: {q} units [2]. (b) CS = Σ(MU − P) = {" + ".join(str(m - p) for m in mu if m >= p)} = ${cs} [2].', 'type': 'multi_step'}
    peak = tu.index(max(tu)) + 1
    return {'stem': f'{tab}. (a) Calculate the marginal utility of each unit. (b) State the number of units at which total utility is maximised and explain the link with marginal utility. (c) Identify where diminishing marginal utility begins.',
            'answer': f'(a) {", ".join(map(str, mu))} (b) {peak} units: MU is positive up to unit {peak} and {"negative" if peak < n else "still positive"} after (c) from the second unit, MU falls continuously.',
            'key': f'(a) differences of TU [2]; (b) TU max at {peak} where MU ≥ 0 for last unit and next MU < 0 [2]; (c) MU falls from unit 1 to 2 onward [1].', 'type': 'multi_step'}


t1_2 = topic('Equi-marginal principle and demand', 'equi-marginal principle', 'derivation of an individual demand curve', 'demand curve')
t1_2.fixed('C1', (1, 2, 3), [
    ('A consumer with a fixed income maximises total utility from two goods, A and B, when', 'MU of A ÷ price of A = MU of B ÷ price of B',
     'Equi-marginal principle: marginal utility per dollar is equal for all goods, with all income spent.',
     ['MU of A = MU of B', 'the price of A equals the price of B', 'total utility from A equals total utility from B']),
    ('If MU(A)/P(A) is greater than MU(B)/P(B), a utility-maximising consumer should', 'buy more of A and less of B',
     'The last dollar gives more satisfaction spent on A; switching raises TU until the ratios are equal.',
     ['buy more of B and less of A', 'buy equal quantities of both goods', 'stop buying both goods']),
    ('The price of good X falls while its marginal utility schedule is unchanged. For a consumer in equilibrium, the immediate effect is that', 'MU(X)/P(X) rises above the ratio for other goods, so more X is bought',
     'Lower P raises MU per dollar for X; consumer buys more X until MU(X) falls and ratios are equal again: a downward-sloping demand curve.',
     ['MU(X)/P(X) falls, so less X is bought', 'the marginal utility of X rises', 'the consumer buys less of every good']),
    ('The equi-marginal principle assumes that consumers', 'are rational and aim to maximise utility with full information',
     'Assumptions: rationality, utility maximisation, known prices and MU, given income and tastes.',
     ['aim to maximise the number of goods bought', 'always buy the cheapest good', 'have unlimited income']),
])
t1_2.fixed('C2', (2, 3, 4), [
    ('Explain, using the equi-marginal principle, how a fall in the price of one good leads to a higher quantity demanded of that good.',
     'Initially MU/P is equal across goods. A fall in the price of X raises MU(X)/P(X), so the consumer gains more utility per dollar from X and switches spending towards it. As more X is consumed its MU falls until MU(X)/P(X) is again equal to the ratio for other goods, at a higher quantity of X.',
     '1 mark: initial equality; 1 mark: price fall raises MU/P for X; 1 mark: buy more X until MU falls and ratios equal [3]'),
    ('Explain why a consumer who spends all their income does not necessarily maximise utility.',
     'Spending all income is necessary but not sufficient: utility is only maximised if the last dollar spent on each good gives the same marginal utility. If MU/P differs, reallocating spending raises total utility.',
     '1 mark: equal MU/P condition; 1 mark: reallocation raises TU if ratios differ [2]'),
    ('Distinguish between the equi-marginal principle and the law of diminishing marginal utility.',
     'Diminishing MU describes how satisfaction from extra units of one good falls; the equi-marginal principle is the rule for allocating a budget across goods so that MU per dollar is equal for all goods. The second relies on the first.',
     '1 mark each definition; 1 mark link: diminishing MU makes the equalisation possible [3]'),
])
items(t1_2, 'C2', (2, 3), [
    ('{person} spends a weekly budget on {good} and {good2}. The marginal utility per dollar from {good} is higher than from {good2}. Explain what {person} should do and why.',
     'Switch spending from {good2} to {good}. Each dollar moved raises total utility because it buys more satisfaction. As more {good} is bought its MU falls and as less {good2} is bought its MU rises, until MU per dollar is equal.',
     '1 mark: buy more {good}, less {good2}; 1 mark: diminishing MU brings ratios into equality [2]'),
])


@t1_2.add('C3', (1, 2, 3), 'numerical')
def t1_2_price(r, D):
    pa = r.choice([2, 3, 4, 5, 6, 8])
    lam = r.choice([2, 3, 4, 5, 6])
    pb = r.choice([x for x in (1, 2, 3, 4, 5, 6, 10, 12) if x != pa])
    mua, mub = pa * lam, pb * lam
    g1, g2 = r.sample(GOODS, 2)
    stem = f'A consumer is in equilibrium buying {g1} and {g2}. The marginal utility of the last unit of {g1} is {mua} utils and its price is ${pa}. The marginal utility of the last unit of {g2} is {mub} utils. Calculate the price of {g2}.'
    return cq(r, D, stem, f'${pb}', f'MU(A)/P(A) = MU(B)/P(B): {mua}/{pa} = {lam} = {mub}/P(B) → P(B) = {mub}/{lam} = ${pb}.',
              dis_num(r, pb, lambda x: money(x), [mub / pa if mub % pa == 0 else pb * 2, pa]))


@t1_2.add('C3', (2, 3, 4, 5), 'multi_step')
def t1_2_alloc(r, D):
    pa, pb = r.sample([1, 2, 3, 4, 5], 2)
    lam = r.choice([4, 5, 6])
    qa, qb = r.randint(2, 4), r.randint(2, 4)
    mua = [pa * (lam + (qa - q)) for q in range(1, 7)]
    mub = [pb * (lam + (qb - q)) for q in range(1, 7)]
    inc = qa * pa + qb * pb
    g1, g2 = r.sample(GOODS, 2)
    tab = table(['Units', f'MU of {g1} (utils)', f'MU of {g2} (utils)'], list(zip(range(1, 7), mua, mub)))
    stem = (f'A consumer has ${inc} a week to spend on {g1} (price ${pa}) and {g2} (price ${pb}). {tab}. '
            f'Calculate the combination of the two goods that maximises the consumer’s total utility and show that the equi-marginal condition holds.')
    ans = f'{qa} units of {g1} and {qb} units of {g2}; MU/P = {lam} for both and spending = ${inc}.'
    key = (f'MU/P for {g1}: {", ".join(str(m // pa) for m in mua)}; for {g2}: {", ".join(str(m // pb) for m in mub)} [1]. '
           f'Equal ratio ({lam}) at {qa} of {g1} and {qb} of {g2} [1]; cost {qa}×{pa} + {qb}×{pb} = ${inc} = income [1].')
    if D >= 4:
        stem += f' Then explain what would happen to the consumer’s purchases if the price of {g1} fell, other things equal.'
        ans += f' A fall in the price of {g1} raises MU/P for {g1}, so more {g1} is bought (a downward-sloping demand curve).'
        key += ' Price fall raises MU/P for the good; buy more until MU falls and ratios equalise [2].'
    return {'stem': stem, 'answer': ans, 'key': key}


@t1_2.add('C3', (2, 3, 4), 'numerical')
def t1_2_demand(r, D):
    mu, tu = _tu_table(r, 2)
    g = r.choice(GOODS)
    p1 = mu[1] - r.choice([0, 1])
    p2 = mu[3] - r.choice([0, 1])
    q1 = sum(1 for m in mu if m >= p1)
    q2 = sum(1 for m in mu if m >= p2)
    return {'stem': f'A consumer values each util at $1. The marginal utility of successive units of {g} is {", ".join(map(str, mu))} utils. Calculate the quantity demanded at a price of ${p1} and at ${p2}, and explain how these points relate to the consumer’s demand curve.',
            'answer': f'{q1} units at ${p1}; {q2} units at ${p2}. These are two points on a downward-sloping individual demand curve.',
            'key': f'Buy units with MU ≥ P: at ${p1}, {q1} units [1]; at ${p2}, {q2} units [1]; the lower price gives the higher quantity because MU diminishes, tracing the demand curve [1].'}


t1_3 = topic('Limitations of utility theory and behavioural economics', 'limitations of marginal utility theory', 'rational consumer', 'behavioural economics')
t1_3.fixed('C1', (1, 2, 3), [
    ('Which concept describes consumers making decisions that are “good enough” because of limited information and time?', 'Bounded rationality',
     'Bounded rationality: decision-making limited by information, cognitive ability and time.', ['Perfect rationality', 'Allocative efficiency', 'Consumer sovereignty']),
    ('A shop displays a “recommended price” of $120 next to its selling price of $80. Which behavioural idea is it using?', 'Anchoring',
     'Anchoring: consumers judge value relative to a reference figure presented first.', ['Herd behaviour', 'Diminishing marginal utility', 'Bounded self-control']),
    ('Enrolling workers into a pension scheme automatically unless they opt out is an example of', 'a nudge using a default choice',
     'Default options exploit inertia: changing the default changes behaviour without restricting choice.', ['a tax on saving', 'a price ceiling', 'perfect information']),
    ('Buying a product mainly because many other people are buying it is called', 'herd behaviour', 'Herd behaviour: imitating others’ choices.',
     ['rational choice', 'anchoring', 'satisficing by firms']),
    ('Which is a limitation of marginal utility theory?', 'Utility cannot be measured objectively in units',
     'MU theory assumes cardinal measurement of satisfaction, which is not possible in practice.',
     ['It explains why demand curves slope upwards', 'It assumes consumers have no income', 'It ignores the price of goods']),
    ('Define behavioural economics.', 'The study of how psychological, social and emotional factors affect economic decisions, so that people do not always act as rational utility-maximisers.', '1 mark: psychology/social factors affect decisions; departure from the rational model [1]'),
])
t1_3.fixed('C2', (2, 3, 4), [
    ('Explain two reasons why consumers may not behave in the way predicted by marginal utility theory.',
     'Consumers have imperfect information about products and prices; decisions are often made by habit or on impulse rather than by calculation; consumers are influenced by others (herd behaviour) and by how choices are framed.',
     '1 mark each reason identified, 1 mark each explained [4]'),
    ('Explain what is meant by bounded self-control and give an example.',
     'Bounded self-control is where people know what is best for them in the long run but lack the willpower to do it, e.g. intending to save but spending on impulse, or overeating despite wanting to lose weight.',
     '1 mark: meaning; 1 mark: example [2]'),
    ('Explain how a government might use a “nudge” to reduce sugar consumption without banning sugary drinks.',
     'It could change choice architecture, for example requiring healthy drinks to be placed at eye level and sugary drinks less visibly, using clear traffic-light labels or setting water as the default drink with meals. Choice is preserved but the easiest option becomes the healthier one.',
     '1 mark: definition of nudge (choice architecture, freedom kept); 1 mark: developed example [2]'),
    ('Explain why consumers might value a $50 loss more highly than a $50 gain.',
     'Loss aversion: people feel the pain of a loss more strongly than the pleasure of an equal gain, so their behaviour is asymmetric, contradicting the assumption that utility depends only on final outcomes.',
     '1 mark: loss aversion; 1 mark: contradicts rational model [2]'),
])
BIASES = [
    ('A gym in {city} finds that most members who sign up in January stop attending by March but keep paying.', 'Bounded self-control', ['Anchoring', 'Herd behaviour', 'Perfect information']),
    ('{firm} offers a “medium” coffee size mainly so that its “large” size looks better value.', 'Anchoring', ['Bounded self-control', 'Default choice', 'Diminishing marginal utility']),
    ('Sales of {good} in {country} triple after a social media post shows celebrities using them.', 'Herd behaviour', ['Anchoring', 'Loss aversion', 'Rational utility maximisation']),
    ('Organ donation rates are far higher in {country}, where citizens must opt out, than in {country2}, where they must opt in.', 'The default choice effect', ['Herd behaviour', 'Diminishing marginal utility', 'Perfect competition']),
    ('Shoppers in {city} choose the first acceptable mobile phone contract rather than comparing all 40 contracts available.', 'Bounded rationality', ['Anchoring', 'Herd behaviour', 'The equi-marginal principle']),
    ('A meat product labelled “90% fat-free” sells better than an identical product labelled “10% fat”.', 'Framing', ['Herd behaviour', 'Bounded self-control', 'Diminishing marginal utility']),
    ('Investors in {country} refuse to sell shares at a loss, hoping prices will recover, even though they would not buy the shares at today’s price.', 'Loss aversion', ['Anchoring to the default', 'Herd behaviour', 'Utility maximisation']),
]


@t1_3.add('C3', (1, 2, 3), 'mcq')
def t1_3_bias(r, D):
    s, a, ds = r.choice(BIASES)
    d = ctx(r)
    s = fill(s, d)
    opts, ans = mcq(r, a, ds)
    return {'stem': f'{s} Which behavioural concept best explains this?', 'options': opts, 'answer': ans,
            'key': f'{a}: the situation departs from the rational consumer model in exactly this way.'}


@t1_3.add('C3', (2, 3, 4, 5), 'case')
def t1_3_pension(r, D):
    d = ctx(r)
    before = r.choice([38, 42, 45, 49, 52, 55])
    after = r.choice([82, 86, 88, 90, 92])
    workers = r.choice([1200, 1500, 2000, 2400, 3000])
    pp = after - before
    ch = 100 * pp / before
    extra = round(workers * pp / 100)
    stem = (f'{d["firm"]} in {d["country"]} changed its pension scheme from “opt in” to automatic enrolment with the right to opt out. '
            f'Participation among its {workers:,} workers rose from {before}% to {after}%. ')
    parts = [
        lambda r: ('Calculate the percentage point change and the percentage change in participation.', f'{pp} percentage points; {pct(ch)}',
                   f'pp change = {after} − {before} = {pp} [1]; % change = {pp}/{before} × 100 = {pct(ch)} [1] [2]'),
        lambda r: ('Calculate how many more workers joined the scheme.', f'{extra:,} workers', f'{workers:,} × {pp}% = {extra:,} [1]'),
        lambda r: ('Explain why this result is difficult to explain using the model of the rational consumer.', 'A rational consumer would join if the benefits exceeded costs whatever the default; the large change shows inertia and the power of defaults (status quo bias).',
                   '1 mark: rational model predicts no change; 1 mark: default/inertia explanation [2]'),
        lambda r: ('Discuss whether governments should use defaults like this more widely.', 'For: cheap, keeps freedom of choice, overcomes bounded self-control. Against: paternalistic, people may stay in unsuitable options, does not address low incomes; depends on whether the default is in people’s interests.',
                   '2 marks analysis; 2 marks evaluation with judgement [4]'),
    ]
    return compose(r, stem, parts, k=(2, 3, 4), type_='case')


essays(t1_1, [
    ('the law of diminishing marginal utility provides a convincing explanation of the shape of an individual demand curve',
     'Explain how the law of diminishing marginal utility is used to derive an individual demand curve.',
     'MU falls as consumption rises; consumers buy while MU ≥ P (or equalise MU/P), so more is bought only at a lower price, giving a downward-sloping demand curve.',
     'Utility is not measurable; consumers lack information; Giffen and Veblen goods, habits and impulse buying break the link; income and substitution effects (indifference analysis) give a better account without cardinal utility.'),
    ('price reflects marginal utility rather than total utility, so essential goods are usually cheap',
     'Explain the difference between total utility and marginal utility, using the paradox of value.',
     'Price depends on MU of the last unit; plentiful goods (water) have low MU and low prices despite high TU; scarce goods (diamonds) have high MU.',
     'Price is also set by supply and costs; essential goods can be expensive when scarce (medicines, housing); market power and information gaps distort prices.'),
], ['Consumers in {country} are spending more of their rising incomes on {good}.', 'A survey in {city} asked consumers how much extra satisfaction they gained from each additional purchase of {good}.'])
essays(t1_2, [
    ('the equi-marginal principle is an accurate description of how consumers allocate their income',
     'Explain the equi-marginal principle and how it leads a consumer to an equilibrium.',
     'Consumers equalise MU per dollar across goods, spending all income; a price change disturbs the equality and changes the bundle.',
     'Consumers rarely calculate; bounded rationality, habit, imperfect information and indivisible goods; yet the model predicts the direction of responses to price changes well.'),
], ['A household in {country} has a fixed monthly budget for food and transport.', 'Prices of {good} in {country} have fallen sharply while incomes are unchanged.'])
essays(t1_3, [
    ('behavioural economics has shown that the traditional model of the rational consumer is of little use',
     'Explain the assumptions of the rational consumer in marginal utility theory.',
     'Behavioural insights (bounded rationality, anchoring, defaults, herd behaviour, bounded self-control) show systematic departures from rational choice.',
     'The traditional model still predicts average responses to price changes and is simple; behavioural effects vary across contexts; best seen as complementary.'),
    ('governments should use nudges rather than taxes to change consumer behaviour',
     'Explain, with examples, what is meant by a nudge.',
     'Nudges keep freedom of choice, are cheap and can overcome bounded self-control (defaults, framing, placement).',
     'Effects may be small or temporary; taxes give a reliable price signal and raise revenue; nudges can be manipulative; mix of measures likely best, depending on the scale of the problem.'),
], ['The government of {country} is concerned about rising obesity and low household saving.', 'A study in {country} found that most shoppers could not recall the price of goods they had just bought.'])

CHAPTERS[1] = [t1_1, t1_2, t1_3]

# ============================================================================ 2 Indifference curves and budget lines
t2_1 = topic('Indifference curves and MRS', 'indifference curves', 'marginal rate of substitution')
t2_1.fixed('C1', (1, 2, 3), [
    ('An indifference curve shows', 'combinations of two goods that give a consumer the same level of satisfaction',
     'Every point on one indifference curve gives equal utility; ICs further from the origin give higher utility.',
     ['combinations of two goods that a consumer can afford with a given income', 'the quantity demanded of a good at each price', 'combinations of two goods that a firm can produce']),
    ('Indifference curves are normally convex to the origin because of', 'a diminishing marginal rate of substitution',
     'As a consumer has more X and less Y, they are willing to give up less and less Y for each extra unit of X.',
     ['increasing marginal utility', 'a constant price ratio', 'economies of scale']),
    ('The marginal rate of substitution of X for Y measures', 'the amount of Y a consumer is willing to give up for one more unit of X while keeping utility constant',
     'MRS = −ΔY/ΔX along an indifference curve; equals the (absolute) slope of the IC.',
     ['the ratio of the price of X to the price of Y', 'the extra utility from one more unit of X', 'the change in income needed to buy one more unit of X']),
    ('Two indifference curves for the same consumer cannot cross because', 'this would imply one bundle gives two different levels of utility',
     'Crossing ICs contradict transitivity and “more is preferred to less”.',
     ['the budget line would then be vertical', 'prices are fixed', 'marginal utility would be zero']),
    ('If two goods are perfect substitutes for a consumer, the indifference curves are', 'straight downward-sloping lines',
     'Perfect substitutes: constant MRS, so ICs are straight lines; perfect complements give L-shaped ICs.',
     ['L-shaped', 'vertical lines', 'upward-sloping curves']),
    ('Define an indifference map.', 'A set of indifference curves for one consumer, each showing a different level of satisfaction; curves further from the origin represent higher utility.', '1 mark: set of ICs; 1 mark: higher curves = higher utility [2]'),
])
t2_1.fixed('C2', (2, 3, 4), [
    ('Explain why an indifference curve slopes downwards from left to right.',
     'If a consumer gains more of one good they must give up some of the other to stay equally satisfied, assuming both goods give positive utility (more is preferred to less).',
     '1 mark: more of X requires less of Y for same utility; 1 mark: assumption that both goods are desirable [2]'),
    ('Explain why the marginal rate of substitution diminishes as a consumer moves down an indifference curve.',
     'As the consumer has more X and less Y, the marginal utility of X falls and the marginal utility of Y rises, so each extra unit of X is worth giving up less Y. MRS = MUx/MUy falls.',
     '1 mark: MUx falls/MUy rises; 1 mark: MRS = MUx/MUy so declines [2]'),
    ('Describe the shape of indifference curves for perfect complements, such as left and right shoes, and explain why.',
     'L-shaped (right-angled) curves: extra units of one good without the other add no utility, so utility only rises when both are increased together in fixed proportions.',
     '1 mark: L-shape; 1 mark: fixed proportions, extra of one alone adds no utility [2]'),
    ('Explain one advantage of indifference curve analysis over marginal utility theory.',
     'It requires only ordinal utility: consumers just need to rank bundles, not measure utility in utils. It also separates the income and substitution effects of a price change.',
     '1 mark: ordinal not cardinal; 1 mark: explanation/second advantage [2]'),
])
items(t2_1, 'C2', (2, 3), [
    ('{person} is indifferent between 4 units of {good} with 10 units of {good2} and 6 units of {good} with 7 units of {good2}. Explain what this tells you about the marginal rate of substitution and the shape of the indifference curve.',
     '{person} gives up 3 units of {good2} for 2 more {good}, so MRS = 1.5 over this range; the curve slopes downwards, and if MRS falls further along it, the curve is convex.',
     '1 mark: MRS = 3/2 = 1.5; 1 mark: downward slope, convexity from diminishing MRS [2]'),
])


@t2_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t2_1_mrs(r, D):
    y0 = r.choice([24, 28, 30, 32, 36, 40])
    drops = sorted(r.sample([12, 10, 8, 6, 5, 4, 3, 2], 4), reverse=True)
    ys = [y0]
    for d_ in drops:
        ys.append(ys[-1] - d_)
    xs = list(range(1, 6))
    g1, g2 = r.sample(GOODS, 2)
    tab = table([f'Units of {g1} (X)', f'Units of {g2} (Y)'], list(zip(xs, ys)))
    i = r.randint(0, 3)
    if D <= 2:
        m = ys[i] - ys[i + 1]
        return cq(r, D, f'The bundles below all lie on one indifference curve. {tab}. Calculate the marginal rate of substitution of X for Y when X rises from {xs[i]} to {xs[i + 1]}.',
                  f'{m}', f'MRS = −ΔY/ΔX = ({ys[i]} − {ys[i + 1]})/1 = {m} units of Y per unit of X.', dis_num(r, m, num, [ys[i], ys[i + 1], ys[i] / xs[i]]))
    mrs = [ys[k] - ys[k + 1] for k in range(4)]
    stem = f'The bundles below all lie on one indifference curve for a consumer. {tab}. (a) Calculate the marginal rate of substitution of X for Y between each pair of bundles. (b) Explain what your results show about the shape of the curve.'
    ans = f'(a) {", ".join(map(str, mrs))} (b) MRS diminishes, so the curve is convex to the origin.'
    key = '(a) MRS = −ΔY/ΔX for each move [2]; (b) falling MRS → convex IC, because MUx falls as X rises [2]'
    if D >= 4:
        j = r.randint(1, 2)
        stem += f' (c) The price ratio Px/Py is {mrs[j]}. Identify where on this curve a budget line with this slope would be tangent, and explain why that point is the consumer’s equilibrium.'
        ans += f' (c) Between the bundles with X = {xs[j]} and X = {xs[j + 1]}, where MRS = {mrs[j]} = Px/Py; other points on this curve lie beyond the budget line (unaffordable) and no higher indifference curve can be reached.'
        key += '; (c) tangency where MRS = Px/Py identified [1]; reason: highest attainable IC [1]'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t2_2 = topic('Budget lines', 'budget lines', 'changes in income and relative prices')
t2_2.fixed('C1', (1, 2, 3), [
    ('A budget line shows', 'all combinations of two goods a consumer can just afford with a given income and prices',
     'Budget line: Px·X + Py·Y = M.', ['combinations of two goods giving equal satisfaction', 'how demand changes with income', 'the cost of producing two goods']),
    ('The slope of a budget line with good X on the horizontal axis is equal to', '−Px/Py', 'Slope = −(price of X)/(price of Y).',
     ['−Py/Px', '−M/Px', 'MUx/MUy']),
    ('An increase in a consumer’s income, with prices unchanged, causes the budget line to', 'shift outwards parallel to the original line',
     'Both intercepts (M/Px, M/Py) rise in proportion; slope unchanged.', ['pivot outwards on the X axis', 'pivot inwards on the Y axis', 'become steeper']),
    ('A fall in the price of good X only (on the horizontal axis) causes the budget line to', 'pivot outwards from the Y-axis intercept',
     'X intercept M/Px rises; Y intercept M/Py unchanged; line becomes flatter.', ['shift outwards in parallel', 'pivot inwards from the X-axis intercept', 'become steeper']),
    ('If income and both prices all double, the budget line', 'does not change', 'Intercepts M/Px and M/Py are unchanged, so real income is the same.',
     ['shifts out in parallel', 'shifts in in parallel', 'pivots on the Y axis']),
])
t2_2.fixed('C2', (2, 3, 4), [
    ('Explain why a consumer cannot choose a point outside their budget line.', 'Points outside require more spending than the consumer’s income at current prices, so they are unattainable.', '1 mark: spending exceeds income; 1 mark: unattainable at given prices [2]'),
    ('Explain the effect on a budget line of a rise in the price of the good on the vertical axis.', 'The Y intercept (M/Py) falls while the X intercept is unchanged, so the line pivots inwards from the X intercept and becomes flatter.', '1 mark: Y intercept falls; 1 mark: pivot on X intercept, flatter [2]'),
    ('Distinguish between a change in real income caused by a rise in money income and one caused by a fall in the price of one good.',
     'A rise in money income shifts the budget line out in parallel (relative prices unchanged). A fall in one price pivots the line, raising real income and also changing relative prices, so it causes a substitution effect as well.',
     '1 mark: parallel shift; 1 mark: pivot; 1 mark: relative price change only in the second case [3]'),
])


@t2_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t2_2_budget(r, D):
    px, py = r.sample([2, 3, 4, 5, 6, 8, 10], 2)
    k = r.choice([5, 6, 10, 12, 15])
    M = px * py * k
    g1, g2 = r.sample(GOODS, 2)
    xi, yi = M // px, M // py
    if D <= 2:
        which = r.choice(['x', 'y'])
        v = xi if which == 'x' else yi
        return cq(r, D, f'A consumer has an income of ${M} to spend on {g1} (X) at ${px} each and {g2} (Y) at ${py} each. Calculate the maximum quantity of {"X" if which == "x" else "Y"} the consumer can buy.',
                  f'{v} units', f'Intercept = M/P = {M}/{px if which == "x" else py} = {v}.', dis_num(r, v, lambda x: f'{num(x)} units', [xi if which == 'y' else yi, M]))
    change = r.choice(['income', 'px', 'py'])
    if change == 'income':
        f = r.choice([1.5, 2, 0.5])
        M2 = M * f
        new = f'income {"rises" if f > 1 else "falls"} to ${num(M2)}'
        ans2 = f'X intercept {num(M2 / px)}, Y intercept {num(M2 / py)}; parallel {"outward" if f > 1 else "inward"} shift, slope unchanged at −{num(px / py)}'
    elif change == 'px':
        p2 = r.choice([x for x in (px // 2, px * 2, px + px // 2) if x and M % x == 0 and x != px] or [px * 2])
        new = f'the price of X changes to ${p2}'
        ans2 = f'X intercept {num(M / p2)}, Y intercept unchanged at {yi}; line pivots on the Y intercept, slope −{num(p2 / py)}'
    else:
        p2 = r.choice([x for x in (py // 2, py * 2, py + py // 2) if x and M % x == 0 and x != py] or [py * 2])
        new = f'the price of Y changes to ${p2}'
        ans2 = f'Y intercept {num(M / p2)}, X intercept unchanged at {xi}; line pivots on the X intercept, slope −{num(px / p2)}'
    stem = (f'A consumer spends ${M} a month on {g1} (X, ${px} each) and {g2} (Y, ${py} each). (a) Calculate the intercepts and the slope of the budget line. '
            f'(b) Then {new}. Calculate the new intercepts and describe how the budget line changes.')
    if D >= 4:
        bx = r.randint(1, xi - 1)
        by = (M - bx * px) // py + r.choice([1, 2])
        stem += f' (c) State, with a calculation, whether a bundle of {bx} X and {by} Y was affordable before the change.'
    ans = f'(a) X intercept {xi}, Y intercept {yi}, slope −{num(px / py)} (b) {ans2}'
    key = f'(a) M/Px = {M}/{px} = {xi}; M/Py = {M}/{py} = {yi}; slope = −Px/Py = −{num(px / py)} [3]; (b) new intercepts and correct description of shift/pivot [2]'
    if D >= 4:
        cost = bx * px + by * py
        ans += f' (c) Cost = {bx}×{px} + {by}×{py} = ${cost} > ${M}, so not affordable.'
        key += ' (c) cost compared with income [1]'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t2_3 = topic('Consumer equilibrium; income and substitution effects', 'consumer equilibrium', 'income and substitution effects', 'giffen', 'inferior')
t2_3.fixed('C1', (1, 2, 3), [
    ('A consumer is in equilibrium where', 'the budget line is tangent to the highest attainable indifference curve',
     'At the tangency MRS = Px/Py.', ['the budget line cuts the lowest indifference curve', 'the indifference curve meets the X axis', 'two indifference curves intersect']),
    ('For a normal good, when its price falls, the income and substitution effects', 'both increase the quantity demanded',
     'SE always raises Qd when price falls; for a normal good higher real income also raises Qd.', ['work in opposite directions', 'both reduce the quantity demanded', 'cancel each other out']),
    ('A Giffen good is one for which, following a fall in its price,', 'the negative income effect outweighs the substitution effect, so quantity demanded falls',
     'Giffen: strongly inferior good; IE opposite and larger than SE, giving an upward-sloping demand curve.',
     ['the substitution effect outweighs the income effect', 'both effects raise quantity demanded', 'there is no substitution effect']),
    ('For an inferior good that is not a Giffen good, a fall in its price', 'raises quantity demanded because the substitution effect outweighs the negative income effect',
     'Inferior: IE negative but smaller than SE, so demand still slopes downwards.',
     ['reduces quantity demanded', 'has no substitution effect', 'leaves quantity demanded unchanged']),
    ('The substitution effect of a price fall is always', 'an increase in the quantity demanded of the good whose price fell',
     'With utility held constant, a lower relative price always leads to substitution towards the cheaper good.',
     ['a decrease in the quantity demanded', 'zero for inferior goods', 'larger than the income effect']),
    ('At consumer equilibrium, the marginal rate of substitution equals', 'the ratio of the prices of the two goods',
     'Tangency: MRS = Px/Py (slope of IC = slope of budget line).', ['zero', 'the consumer’s income', 'the ratio of the quantities bought']),
])
t2_3.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain the income and substitution effects of a fall in the price of a normal good.',
     'Diagram: X on horizontal axis, Y vertical; original budget line tangent to IC1 at A. Price of X falls, budget line pivots out on Y intercept and is tangent to IC2 at C. A compensating budget line parallel to the new one is drawn tangent to IC1 at B. A→B (movement along IC1) is the substitution effect, an increase in X; B→C (parallel shift) is the income effect, also an increase in X for a normal good.',
     '1 mark: correct pivot; 1 mark: compensated line tangent to original IC; 1 mark: SE = A→B; 1 mark: IE = B→C in same direction [4]'),
    ('Explain why a Giffen good has an upward-sloping demand curve.',
     'A Giffen good is a strongly inferior good taking a large share of a poor household’s budget. When its price rises, real income falls a lot and the positive income effect (buying more of the cheap staple) outweighs the substitution effect away from it, so quantity demanded rises with price.',
     '1 mark: strongly inferior/large budget share; 1 mark: IE opposite to SE; 1 mark: IE larger so Qd and P move together [3]'),
    ('Explain why the substitution effect of a price change always works in the opposite direction to the price change.',
     'The substitution effect holds utility constant and considers only the change in relative prices; a fall in price makes the good relatively cheaper, so the consumer moves along the same IC to more of it (convexity of the IC ensures this).',
     '1 mark: relative price change, utility constant; 1 mark: move along convex IC towards the cheaper good [2]'),
])


@t2_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t2_3_effects(r, D):
    kind = r.choice(['normal', 'inferior', 'Giffen'])
    qa = r.choice([10, 12, 15, 20, 24, 30])
    se = r.choice([4, 5, 6, 8, 10])
    if kind == 'normal':
        ie = r.choice([2, 3, 4, 5])
    elif kind == 'inferior':
        ie = -r.randint(1, se - 1)
    else:
        ie = -(se + r.choice([1, 2, 3]))
    qb, qc = qa + se, qa + se + ie
    g = r.choice(['rice', 'bread', 'bus journeys', 'instant noodles', 'cinema tickets', 'fresh fruit', 'own-brand cereal', 'coffee'])
    stem = (f'The price of {g} falls. In an indifference curve diagram, the consumer’s original equilibrium A involves {qa} units of {g}. '
            f'On the compensated budget line (tangent to the original indifference curve) the consumer would buy {qb} units (point B). The new equilibrium C involves {qc} units.')
    if D == 1:
        opts, a = mcq(r, kind if kind != 'Giffen' else 'Giffen', [k for k in ('normal', 'inferior', 'Giffen', 'luxury') if k != kind])
        return {'stem': stem + ' Which type of good is this for the consumer?', 'options': opts, 'answer': a,
                'key': f'SE = {qb} − {qa} = +{se}; IE = {qc} − {qb} = {ie:+d}. ' + {'normal': 'IE positive: normal good.', 'inferior': 'IE negative but smaller than SE: inferior (not Giffen).', 'Giffen': 'IE negative and larger than SE: Giffen good.'}[kind]}
    ans = f'Substitution effect = +{se} units; income effect = {ie:+d} units; total effect = {qc - qa:+d} units; {kind} good.'
    key = f'SE = B − A = {qb} − {qa} = +{se} [1]; IE = C − B = {qc} − {qb} = {ie:+d} [1]; total = C − A = {qc - qa:+d} [1]; classification: ' + {'normal': 'IE reinforces SE → normal good [1]', 'inferior': 'IE opposes but is smaller than SE → inferior good [1]', 'Giffen': 'IE opposes and outweighs SE → Giffen good, Qd falls when price falls [1]'}[kind]
    stem += ' Calculate the substitution effect, the income effect and the total effect, and identify the type of good.'
    if D >= 4:
        stem += ' Explain why this classification matters for the shape of the consumer’s demand curve.'
        ans += ' ' + ('The demand curve slopes downwards.' if kind != 'Giffen' else 'The demand curve slopes upwards over this range.')
        key += ' Demand curve slope linked to sign of total effect [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'numerical'}


@t2_3.add('C3', (2, 3, 4), 'numerical')
def t2_3_tangency(r, D):
    px, py = r.sample([1, 2, 3, 4, 5, 6], 2)
    ratio = px / py
    mrs = r.choice([x for x in (0.5, 1, 1.5, 2, 3, 4) if abs(x - ratio) > 1e-9])
    g1, g2 = r.sample(GOODS, 2)
    more = g1 if mrs > ratio else g2
    return {'stem': f'A consumer buys {g1} (X, ${px}) and {g2} (Y, ${py}). At the current bundle the marginal rate of substitution of X for Y is {num(mrs)}. Explain whether the consumer is in equilibrium and how they should change their purchases.',
            'answer': f'Not in equilibrium: MRS ({num(mrs)}) ≠ Px/Py ({num(ratio)}). The consumer values X {"more" if mrs > ratio else "less"} than its relative price, so should buy more {more} and less of the other good until MRS = {num(ratio)}.',
            'key': f'Equilibrium requires MRS = Px/Py = {px}/{py} = {num(ratio)} [1]; MRS {">" if mrs > ratio else "<"} price ratio [1]; buy more {more}; diminishing MRS restores equality [1].'}


def _ic_c4(r, D):
    d = ctx(r)
    M = r.choice([120, 180, 240, 360])
    px = r.choice([4, 6, 12])
    py = r.choice([3, 5, 10])
    if M % px or M % py:
        M = px * py * r.choice([4, 5, 6])
    p2 = px // 2
    g = r.choice(['rice', 'bread', 'potatoes', 'maize flour'])
    intro = f'A low-income household in {d["country"]} spends ${M} a week on {g} (X, ${px} per kg) and other food (Y, ${py} per unit). The government subsidises {g} so that its price falls to ${p2} per kg.'
    parts = [
        lambda r: ('Calculate the intercepts of the budget line before and after the subsidy.', f'Before: X {M // px}, Y {M // py}; after: X {M // p2}, Y {M // py}.', f'M/Px = {M}/{px}, M/Py = {M}/{py}; after M/{p2} [2]'),
        lambda r: ('With the aid of a diagram, explain how the budget line changes.', 'The budget line pivots outwards from the Y intercept, becoming flatter; real income rises and X is relatively cheaper.', '1 mark pivot on Y intercept; 1 mark flatter/real income rise [2]'),
        lambda r: (f'Using indifference curves, explain how the household could buy less {g} after the price fall.', f'If {g} is a Giffen good, the substitution effect (more {g}) is outweighed by a negative income effect: with higher real income the household switches to preferred foods, buying less {g}.',
                   '1 mark SE direction; 1 mark negative IE; 1 mark IE larger → Giffen [3]'),
        lambda r: ('Assess whether subsidising a staple food is the best way to raise the living standards of poor households.', 'For: raises real income, improves nutrition, simple. Against: benefits richer households too, cost to government, may be inferior/Giffen so consumption may fall; cash transfers allow free choice. Judgement depends on targeting and budget.',
                   '2 marks analysis; 2 marks evaluation [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t2_1, t2_2, t2_3], 'C4', (3, 4, 5), 'case', _ic_c4)
essays(t2_3, [
    ('indifference curve analysis explains consumer behaviour better than marginal utility theory',
     'With the aid of a diagram, explain the income and substitution effects of a price fall for a normal good.',
     'Ordinal utility only; separates income and substitution effects; explains Giffen and inferior goods; consumer equilibrium at tangency MRS = Px/Py.',
     'Still assumes rationality, full information and smooth preferences; difficult to observe ICs; behavioural economics challenges both models; both predict downward-sloping demand for most goods.'),
    ('a fall in the price of a good will always increase the quantity demanded',
     'Explain the difference between a normal good, an inferior good and a Giffen good using income and substitution effects.',
     'For normal and most inferior goods, SE dominates so Qd rises when price falls.',
     'Giffen goods (strongly inferior staples with a large budget share) and Veblen goods are exceptions; expectations of further price falls; but such cases are rare in practice.'),
], ['The price of {good} in {country} has fallen by 20% over two years.', 'Poor households in {country} spend about half their income on a staple food.'])
essays(t2_1, [
    ('indifference curves are a useful tool for analysing consumer choice even though they cannot be observed',
     'Explain why indifference curves are normally downward sloping and convex to the origin.',
     'Downward slope from non-satiation; convexity from diminishing MRS; with budget lines they show optimal choice and responses to price and income changes.',
     'Preferences change and are unobservable; assumes rationality, consistency and transitivity; the theory is a model, judged by its predictions.'),
], ['Market researchers in {country} want to understand how consumers choose between {good} and {good2}.'])
essays(t2_2, [
    ('a rise in income and a fall in price have the same effect on a consumer’s choices',
     'With the aid of a diagram, explain how a budget line is affected by a change in income and by a change in the price of one good.',
     'Income rise: parallel outward shift, only income effect; price fall: pivot, real income rises plus a substitution effect.',
     'Outcomes depend on whether goods are normal or inferior and on preferences; a price fall changes relative prices, so the bundle chosen differs even if utility is the same.'),
], ['In {country}, money incomes rose by 10% last year while the price of {good} fell by 10%.'])

CHAPTERS[2] = [t2_1, t2_2, t2_3]

# ============================================================================ 3 Efficiency and market failure
t3_1 = topic('Productive and allocative efficiency', 'productive and allocative efficiency', 'productive efficiency', 'allocative efficiency')
t3_1.fixed('C1', (1, 2, 3), [
    ('A firm is productively efficient when it produces at the output where', 'average total cost is at its minimum',
     'Productive efficiency: lowest point of ATC (and for an economy, on the PPC).', ['price equals marginal cost', 'marginal revenue equals marginal cost', 'total revenue is maximised']),
    ('Allocative efficiency occurs where', 'price equals marginal cost', 'P = MC: the value consumers place on the last unit equals the cost of producing it.',
     ['price equals average cost', 'marginal cost is at its minimum', 'average revenue equals average variable cost']),
    ('An economy producing at a point inside its production possibility curve is', 'productively inefficient', 'Inside the PPC more of one good could be produced without less of the other.',
     ['allocatively efficient', 'dynamically efficient', 'producing beyond its capacity']),
    ('In long-run equilibrium, a perfectly competitive firm is', 'both productively and allocatively efficient', 'LR: P = MC = min ATC.',
     ['allocatively efficient only', 'productively efficient only', 'neither productively nor allocatively efficient']),
    ('Define allocative efficiency.', 'A situation where resources are allocated so that the goods and services produced are those most wanted by consumers; where P = MC for every good.', '1 mark: resources match consumer wants; 1 mark: P = MC [2]'),
])
t3_1.fixed('C2', (2, 3, 4), [
    ('Explain why allocative efficiency requires price to equal marginal cost.',
     'Price measures the value consumers place on the last unit (marginal benefit) and MC the opportunity cost of producing it. If P > MC, society values extra units more than they cost, so output should rise; if P < MC, too much is produced. Only at P = MC is welfare maximised.',
     '1 mark: P = marginal benefit; 1 mark: MC = opportunity cost; 1 mark: P > MC under-production and vice versa [3]'),
    ('Explain why a monopolist is unlikely to be productively or allocatively efficient.',
     'A profit-maximising monopolist produces where MC = MR, which is below the output at minimum ATC and where P > MC, so it restricts output and charges a higher price.',
     '1 mark: MC = MR; 1 mark: P > MC (allocative inefficiency); 1 mark: not at min ATC [3]'),
    ('Distinguish between productive efficiency for a firm and for a whole economy.',
     'For a firm it means producing at the minimum point of its average cost curve; for an economy it means being on the PPC so no more of one good can be produced without producing less of another.',
     '1 mark each [2]'),
])
items(t3_1, 'C2', (2, 3), [
    ('{firm}, a producer of {good}, is producing where price exceeds marginal cost. Explain what this implies about allocative efficiency and how output should change.',
     'Consumers value an extra unit more than it costs to produce, so resources are under-allocated to {good}; output should rise until P = MC.',
     '1 mark: under-allocation; 1 mark: raise output to P = MC [2]'),
    ('{firm} has cut its average cost of producing {good} by adopting new machinery, but still produces less than the output at which average cost is lowest. Explain whether it is productively efficient.',
     'No: productive efficiency requires output at the minimum of the ATC curve using the least-cost method; producing below that output means ATC is still above its minimum.',
     '1 mark: definition (min ATC); 1 mark: application [2]'),
])


def _cost_sched(r):
    b = r.choice([10, 12, 14, 16, 18, 20])
    c = r.choice([2, 3, 4])
    q0 = r.choice([2, 3])
    mc = [b + c * (q - q0) ** 2 for q in range(1, 9)]
    F = r.choice([40, 50, 60, 80, 90, 100, 120])
    tc = []
    s = F
    for m in mc:
        s += m
        tc.append(s)
    atc = [tc[i] / (i + 1) for i in range(8)]
    return F, mc, tc, atc


@t3_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t3_1_eff(r, D):
    for _ in range(20):
        F, mc, tc, atc = _cost_sched(r)
        best = min(range(8), key=lambda i: atc[i])
        srt = sorted(atc)
        if srt[1] - srt[0] > 0.05 and best < 7:
            break
    qs = list(range(1, 9))
    g = r.choice(GOODS)
    tab = table(['Output (units)', 'Total cost ($)'], list(zip(qs, tc)))
    qe = best + 1
    if D <= 2:
        opts, a = mcq(r, f'{qe} units', [f'{q} units' for q in qs if q != qe])
        return {'stem': f'A firm producing {g} has the following costs. {tab}. At which output is the firm productively efficient?', 'options': opts, 'answer': a,
                'key': f'ATC = TC/Q: ' + ', '.join(num(x, 1) for x in atc) + f'. Minimum ATC ${num(atc[best], 2)} at {qe} units.'}
    j = r.randint(max(best, 2), 7)
    P = mc[j]
    stem = f'A firm producing {g} has these costs. {tab}. (a) Calculate average total cost at each output and identify the productively efficient output. (b) The market price is ${P}. Identify the allocatively efficient output and explain your answer.'
    ans = f'(a) ATC: {", ".join(num(x, 1) for x in atc)}; productively efficient at {qe} units (ATC ${num(atc[best], 2)}). (b) {j + 1} units, where MC = P = ${P}.'
    key = f'(a) ATC = TC/Q [2]; min ATC at {qe} [1]. (b) MC = ΔTC: {", ".join(map(str, mc))} [1]; P = MC at {j + 1} units [1]; P = MC means marginal benefit = marginal cost [1].'
    if D >= 5:
        stem += ' (c) Explain why the two outputs differ and what this implies about the firm’s profits.'
        ans += f' (c) Price ${P} {"exceeds" if P > atc[j] else "is below"} ATC at {j + 1} units (${num(atc[j], 2)}), so the firm makes {"supernormal profit" if P > atc[j] else "a loss"}; outputs coincide only when P = min ATC (long-run perfect competition).'
        key += ' (c) compare P with ATC at chosen output [1]; outputs equal only when P = min ATC [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t3_2 = topic('Pareto optimality and dynamic efficiency', 'pareto optimality', 'dynamic efficiency')
t3_2.fixed('C1', (1, 2, 3), [
    ('Pareto optimality is a situation in which', 'it is impossible to make one person better off without making someone else worse off',
     'Pareto optimum: no further Pareto improvement is possible.', ['everyone has the same income', 'all firms make normal profit', 'total utility of each person is maximised']),
    ('A Pareto improvement is a change that', 'makes at least one person better off and nobody worse off',
     'Pareto improvement: gains without losers.', ['makes the majority better off', 'raises total GDP', 'redistributes income from rich to poor']),
    ('Dynamic efficiency refers to', 'improvements in efficiency over time through investment and innovation',
     'Dynamic efficiency: new products and processes lowering costs/raising quality over time, often financed by supernormal profit.',
     ['producing at minimum average cost at a point in time', 'setting price equal to marginal cost', 'distributing output equally']),
    ('Which market structure is often argued to promote dynamic efficiency?', 'Monopoly or oligopoly earning long-run supernormal profit',
     'Supernormal profits can fund R&D (Schumpeter); competition may also spur innovation.', ['Perfect competition with normal profit', 'A market with no barriers and no profit', 'A market with a price ceiling below cost']),
    ('Define Pareto optimality.', 'An allocation of resources where no one can be made better off without making at least one other person worse off.', '[1]'),
])
t3_2.fixed('C2', (2, 3, 4), [
    ('Explain the conditions needed for an economy to achieve Pareto optimality.', 'It must be productively efficient (on the PPC, firms at minimum cost) and allocatively efficient (P = MC in all markets), with no market failures.', '1 mark: productive; 1 mark: allocative; 1 mark: P = MC everywhere/no market failure [3]'),
    ('Explain why a Pareto optimal allocation may still be considered unfair.', 'Pareto optimality says nothing about distribution: an allocation where one person has almost everything can be Pareto optimal because any change would make them worse off.', '1 mark: efficiency not equity; 1 mark: example [2]'),
    ('Explain how supernormal profit may lead to dynamic efficiency.', 'Supernormal profit provides funds for research and development and the incentive of protected future profits, leading to new products and lower-cost processes over time.', '1 mark: funds R&D; 1 mark: incentive/outcome [2]'),
    ('Distinguish between static efficiency and dynamic efficiency.', 'Static efficiency (productive and allocative) is efficiency at a point in time with given technology; dynamic efficiency is the improvement in efficiency over time through innovation and investment.', '1 mark each [2]'),
])


@t3_2.add('C3', (1, 2, 3, 4), 'numerical')
def t3_2_pareto(r, D):
    a, b = r.sample(PEOPLE_ECON, 2)
    base = (r.randint(30, 60), r.randint(30, 60))
    names = list('PQRST')
    allocs = {'P': base}
    kinds = r.sample(['imp', 'imp', 'worse', 'trade', 'trade2', 'equal1'], 4)
    for nm, k in zip(names[1:], kinds):
        if k == 'imp':
            v = (base[0] + r.randint(1, 10), base[1] + r.randint(0, 8))
        elif k == 'equal1':
            v = (base[0], base[1] + r.randint(2, 9))
        elif k == 'worse':
            v = (base[0] - r.randint(1, 8), base[1] - r.randint(0, 6))
        elif k == 'trade':
            v = (base[0] + r.randint(5, 15), base[1] - r.randint(1, 6))
        else:
            v = (base[0] - r.randint(2, 7), base[1] + r.randint(5, 15))
        allocs[nm] = v
    imps = [nm for nm in names[1:] if allocs[nm][0] >= base[0] and allocs[nm][1] >= base[1] and allocs[nm] != base]
    desc = '; '.join(f'{nm}: {a} {u[0]}, {b} {u[1]}' for nm, u in allocs.items())
    stem = f'The table shows the utility of two people under five allocations of resources (utility values). {desc}. Starting from allocation P, identify which moves are Pareto improvements and explain.'
    ans = ('Pareto improvements: ' + (', '.join(imps) if imps else 'none') + '. In these moves neither person is worse off and at least one is better off; the other moves make someone worse off.')
    key = 'For each allocation compare both utilities with P [2]; correct list [1]; reason: no-one worse off, someone better off [1].'
    if D == 1 and imps:
        right = imps[0]
        wrong = [nm for nm in names[1:] if nm not in imps]
        if len(wrong) >= 3:
            opts, aa = mcq(r, f'P to {right}', [f'P to {w}' for w in wrong])
            return {'stem': f'Utility of two people under five allocations: {desc}. Which move is a Pareto improvement?', 'options': opts, 'answer': aa,
                    'key': f'P to {right}: neither is worse off and at least one gains.'}
    return {'stem': stem, 'answer': ans, 'key': key}


@t3_2.add('C3', (2, 3, 4), 'numerical')
def t3_2_dynamic(r, D):
    d = ctx(r)
    c1 = r.choice([40, 50, 60, 80, 120, 200])
    fall = r.choice([10, 15, 20, 25, 30, 40])
    yrs = r.choice([2, 3, 4, 5])
    c2 = c1 * (1 - fall / 100)
    rd = r.choice([2, 5, 8, 12, 20])
    out = r.choice([1, 2, 4, 5])
    save = (c1 - c2) * out
    payback = rd / save
    return {'stem': f'{d["firm"]}, a monopoly supplier of {d["good"]} in {d["country"]}, spent ${rd} million on research. Over {yrs} years its average cost fell from ${num(c1)} to ${num(c2)} per unit while output stayed at {out} million units a year. Calculate (a) the percentage fall in average cost and (b) the annual cost saving. (c) Explain whether this is evidence of dynamic efficiency.',
            'answer': f'(a) {fall}% (b) ${num(save)} million a year (c) Yes: costs fell over time through innovation funded by profit; the research cost is recovered in about {num(payback, 1)} years of savings, though consumers gain only if lower costs are passed on in price or quality.',
            'key': f'(a) ({num(c1)} − {num(c2)})/{num(c1)} × 100 = {fall}% [1]; (b) {num(c1 - c2)} × {out}m = ${num(save)}m [1]; (c) definition of dynamic efficiency applied [1] + evaluative point (pass-through to consumers / monopoly) [1].',
            'type': 'multi_step'}


PEOPLE_ECON = ['Amara', 'Lucas', 'Sofia', 'Kenji', 'Zara', 'Mateo', 'Aisha', 'Noah', 'Leila', 'Ethan', 'Priya', 'Omar']

t3_3 = topic('Market failure', 'market failure', 'causes and consequences for efficiency')
t3_3.fixed('C1', (1, 2, 3), [
    ('Market failure occurs when', 'the free market fails to allocate resources efficiently, so welfare is not maximised',
     'Market failure: resource allocation is not allocatively (or productively) efficient.', ['a firm makes a loss', 'prices rise', 'the government intervenes in a market']),
    ('A public good is', 'non-rival and non-excludable', 'Non-rival: one person’s use does not reduce availability; non-excludable: non-payers cannot be prevented from benefiting.',
     ['rival and excludable', 'provided only by the government', 'a good with positive externalities only']),
    ('The free-rider problem arises because', 'people can benefit from a good without paying for it', 'Non-excludability means no one has an incentive to pay, so private firms will not supply the good.',
     ['firms charge prices above marginal cost', 'consumers buy too much of demerit goods', 'goods are rival in consumption']),
    ('Which is an example of information failure?', 'Consumers underestimating the long-term benefits of education',
     'Merit goods are under-consumed partly because of imperfect information about their benefits.', ['A firm producing at minimum average cost', 'A fall in the price of a normal good', 'A government imposing a tax on petrol']),
    ('Asymmetric information exists when', 'one party to a transaction has more information than the other', 'E.g. used-car sellers know more than buyers; can lead to adverse selection and moral hazard.',
     ['both parties have full information', 'information is free', 'the government publishes market data']),
    ('Define a merit good.', 'A good that is under-consumed in a free market, often because consumers underestimate its benefits, and which has positive externalities, e.g. education or healthcare.', '1 mark: under-consumed; 1 mark: reason (information failure/positive externalities) [2]'),
])
t3_3.fixed('C2', (2, 3, 4), [
    ('Explain why a public good such as street lighting would not be provided by a free market.', 'Because it is non-excludable, consumers can free ride, so no firm can charge for it and make a profit; because it is non-rival, the marginal cost of an extra user is zero. The market is missing.', '1 mark: non-excludable → free riding; 1 mark: no profit → missing market; 1 mark: non-rival [3]'),
    ('Explain how monopoly power leads to market failure.', 'A monopolist restricts output and raises price above MC, so P > MC (allocative inefficiency) and there is a deadweight welfare loss; it may also be X-inefficient.', '1 mark: higher price/lower output; 1 mark: P > MC; 1 mark: deadweight loss [3]'),
    ('Explain the difference between a merit good and a public good.', 'A public good is non-rival and non-excludable and would not be provided at all by the market. A merit good is rival and excludable and is provided by the market, but in too small a quantity because its benefits are underestimated.', '1 mark each definition; 1 mark: not provided vs under-provided [3]'),
    ('Explain how adverse selection can cause market failure in insurance markets.', 'Insurers cannot distinguish high-risk from low-risk customers, so they set an average premium. Low-risk customers find this too expensive and leave, raising the average risk and premiums, so the market shrinks or collapses.', '1 mark: asymmetric information; 1 mark: average premium drives out low-risk; 1 mark: market shrinks [3]'),
])
MF_CASES = [
    ('A lighthouse on the coast of {country} warns all passing ships.', 'Public good', ['Merit good', 'Demerit good', 'Negative externality']),
    ('Young people in {city} leave school early because they underestimate the future earnings from education.', 'Information failure leading to under-consumption of a merit good', ['A public good', 'Monopoly power', 'A negative production externality']),
    ('Smoke from a cement works in {city} damages crops on nearby farms.', 'Negative production externality', ['Positive consumption externality', 'Public good', 'Asymmetric information in insurance']),
    ('Used-car sellers in {country} know about hidden faults that buyers cannot detect.', 'Asymmetric information', ['Public good', 'Positive externality', 'Factor immobility']),
    ('Unemployed coal miners in {country} cannot easily move to jobs in software development.', 'Factor immobility', ['Public good', 'Positive consumption externality', 'Allocative efficiency']),
    ('{firm} is the only supplier of {good} in {country} and charges a price well above marginal cost.', 'Monopoly power', ['Public good', 'Merit good', 'Positive externality']),
    ('Vaccination of children in {city} reduces the spread of disease to other people.', 'Positive consumption externality', ['Negative production externality', 'Public good', 'Demerit good']),
    ('Excessive consumption of sugary drinks in {country} leads to obesity, which the consumers did not anticipate.', 'Demerit good (information failure)', ['Public good', 'Merit good', 'Monopoly power']),
]


@t3_3.add('C3', (1, 2, 3), 'mcq')
def t3_3_classify(r, D):
    s, a, ds = r.choice(MF_CASES)
    s = fill(s, ctx(r))
    opts, ans = mcq(r, a, ds)
    return {'stem': f'{s} Which type of market failure is illustrated?', 'options': opts, 'answer': ans, 'key': f'{a}: the market outcome is not allocatively efficient for this reason.'}


items(t3_3, 'C3', (2, 3, 4), [
    ('Free markets in {country} provide almost no flood defences, even though floods regularly damage homes in {city}. Analyse the type of market failure involved and its consequence for efficiency.',
     'Flood defences are a public good: non-excludable (all homes behind the wall are protected) and non-rival. Free riding means no firm can charge, so the market is missing; output is zero where society values it highly, so allocation is inefficient.',
     '1 mark: public good identified; 1 mark: characteristics applied; 1 mark: free rider/missing market; 1 mark: welfare loss/inefficiency [4]'),
    ('In {country}, private health insurers refuse to cover older people at affordable premiums. Analyse why this may be a market failure.',
     'Asymmetric information and adverse selection: insurers cannot assess individual risk and set high average premiums, low-risk people leave, so cover is under-provided; healthcare is also a merit good with positive externalities.',
     '1 mark: asymmetric information; 1 mark: adverse selection chain; 1 mark: under-provision; 1 mark: merit good/externality [4]'),
    ('Fishing boats from several countries over-fish the seas near {country} until fish stocks collapse. Analyse why the market fails in this case.',
     'Fish stocks are a common resource: rival but non-excludable. Each boat ignores the cost it imposes on others (an externality), so the resource is over-used (tragedy of the commons) and future output falls.',
     '1 mark: common resource/rival non-excludable; 1 mark: external cost ignored; 1 mark: over-use; 1 mark: inefficiency over time [4]'),
])
essays(t3_1, [
    ('perfect competition is the most efficient market structure',
     'Explain the meaning of productive and allocative efficiency.',
     'In LR perfect competition P = MC = min ATC, so firms are productively and allocatively efficient; no X-inefficiency.',
     'No funds for R&D so little dynamic efficiency; no economies of scale; assumptions unrealistic; natural monopoly may have lower costs; efficiency must be weighed against equity.'),
    ('a market economy will always allocate resources efficiently',
     'Explain how the price mechanism allocates resources.',
     'Prices act as signals and incentives; competitive markets lead to P = MC.',
     'Market failures: externalities, public goods, information failure, market power, immobility; efficiency is not equity.'),
], ['The government of {country} is reviewing whether markets for {good} and for {ind} services are working efficiently.'])
essays(t3_2, [
    ('dynamic efficiency is more important than static efficiency for consumers in the long run',
     'Explain the difference between Pareto optimality and dynamic efficiency.',
     'Innovation lowers costs and creates new products; benefits compound over time; static gains are one-off.',
     'Monopoly profits may not be reinvested; X-inefficiency; consumers pay higher prices now; competition can also drive innovation; depends on industry (pharmaceuticals vs retail).'),
    ('a Pareto optimal allocation of resources is the best outcome for society',
     'Explain what is meant by a Pareto optimal allocation of resources.',
     'Pareto optimum means no waste; any change would harm someone.',
     'Many Pareto optima exist, some very unequal; equity considerations; dynamic issues; value judgements needed.'),
], ['{firm} argues that its high profits in the {ind} industry are justified because they fund new technology.', 'A report on the economy of {country} claims that resources are allocated optimally.'])
essays(t3_3, [
    ('government intervention is always needed when there is market failure',
     'Explain three causes of market failure.',
     'Public goods are not provided; externalities lead to over/under-production; information failure; monopoly; intervention can correct.',
     'Government failure (information, incentives, cost of intervention); private solutions (Coase bargaining, reputation, warranties); size of failure matters.'),
    ('information failure is the most important cause of market failure',
     'Explain how information failure leads to market failure.',
     'Asymmetric information, merit/demerit goods, adverse selection and moral hazard misallocate resources widely.',
     'Externalities and market power may cause larger welfare losses; information can be improved cheaply; importance varies by market.'),
], ['In {country}, private markets supply too little education and too many sugary drinks.', 'A report found that consumers in {country} often make poor decisions about pensions and insurance.'])

CHAPTERS[3] = [t3_1, t3_2, t3_3]

# ============================================================================ 4 Externalities and cost-benefit analysis
t4_1 = topic('Private, external and social costs and benefits', 'private, external and social costs and benefits', 'social costs')
t4_1.fixed('C1', (1, 2, 3), [
    ('Social cost is equal to', 'private cost plus external cost', 'SC = PC + EC.', ['private cost minus external cost', 'external cost only', 'private cost plus private benefit']),
    ('An external benefit is', 'a benefit enjoyed by a third party who is not directly involved in the transaction', 'Externality: spillover effect on third parties not reflected in the price.',
     ['a benefit received by the buyer', 'the profit made by the seller', 'a benefit paid for by the government']),
    ('Which is an external cost of road transport?', 'Health damage to people living near a busy road', 'Third-party effect, not paid for by drivers.',
     ['The cost of fuel paid by drivers', 'The price of a new car', 'Road tax paid by vehicle owners']),
    ('When there is a negative externality in production, the free market output is', 'greater than the socially optimal output', 'Producers ignore external costs: MPC < MSC, so output where MPC = MSB exceeds output where MSC = MSB.',
     ['less than the socially optimal output', 'equal to the socially optimal output', 'zero']),
    ('Define a negative externality.', 'A cost imposed on a third party, not involved in the production or consumption of a good, for which no compensation is paid.', '1 mark: cost to third party; 1 mark: not reflected in price/no compensation [2]'),
])
t4_1.fixed('C2', (2, 3, 4), [
    ('Explain why the existence of external costs means that the price mechanism leads to over-production.', 'Producers base decisions on private costs; the price does not include the external cost, so output is where MPC = MSB, beyond the social optimum where MSC = MSB.', '1 mark: private decisions ignore EC; 1 mark: MPC < MSC; 1 mark: output too high [3]'),
    ('Distinguish between private benefits and external benefits, using education as an example.', 'Private benefits go to the student (higher earnings, satisfaction); external benefits go to third parties (more productive workforce, lower crime, higher tax revenue).', '1 mark each with example [2]'),
    ('Explain why it is difficult to place a monetary value on external costs.', 'Many effects (health, noise, loss of biodiversity) have no market price, they are spread over many people and over time, and the cause-and-effect link may be uncertain, so shadow prices must be estimated.', '1 mark: no market price; 1 mark: uncertainty/many parties [2]'),
])


@t4_1.add('C3', (1, 2, 3), 'numerical')
def t4_1_sc(r, D):
    d = ctx(r)
    pc = r.choice([40, 60, 80, 120, 150, 200])
    ec = r.choice([10, 15, 20, 25, 30, 45, 50])
    pb = r.choice([70, 90, 110, 160])
    eb = r.choice([5, 10, 20, 30])
    k = r.choice(['sc', 'sb', 'net'])
    if k == 'sc':
        return cq(r, D, f'A factory in {d["city"]} producing {d["good"]} has a private cost of ${pc} per unit. Pollution imposes a cost of ${ec} per unit on local residents. Calculate the social cost per unit.',
                  f'${pc + ec}', f'SC = PC + EC = {pc} + {ec} = ${pc + ec}.', dis_num(r, pc + ec, money, [pc - ec, ec, pc]))
    if k == 'sb':
        return cq(r, D, f'A student in {d["country"]} gains a private benefit of ${pb} thousand from a training course and society gains an external benefit of ${eb} thousand. Calculate the social benefit.',
                  f'${pb + eb} thousand', f'SB = PB + EB = {pb} + {eb} = ${pb + eb} thousand.', dis_num(r, pb + eb, lambda x: money(x) + ' thousand', [pb - eb, eb]))
    net = (pb + eb) - (pc + ec)
    return cq(r, D, f'For a project in {d["country"]}: private cost ${pc}m, external cost ${ec}m, private benefit ${pb}m, external benefit ${eb}m. Calculate the net social benefit and state whether the project should go ahead on these figures.',
              f'{money(net)}m; {"go ahead" if net > 0 else "do not go ahead"}', f'SB − SC = ({pb} + {eb}) − ({pc} + {ec}) = {money(net)}m [2]; positive → proceed [1].',
              [f'{money(pb - pc)}m; {"go ahead" if pb - pc > 0 else "do not go ahead"}', f'{money(-net)}m; {"go ahead" if -net > 0 else "do not go ahead"}', f'{money(pb + eb + pc + ec)}m; go ahead', f'{money(net + 2 * ec)}m; go ahead'])


@t4_1.add('C3', (2, 3, 4, 5), 'multi_step')
def t4_1_table(r, D):
    qs = list(range(1, 7))
    for _ in range(50):
        b0, c0 = r.choice([90, 100, 110, 120]), r.choice([20, 24, 30])
        mpb = [b0 - 12 * i for i in range(6)]
        mpc = [c0 + 10 * i for i in range(6)]
        mec = r.choice([12, 22, 24, 30, 36])
        msc = [c + mec for c in mpc]
        qm = max(q for q, b, c in zip(qs, mpb, mpc) if b >= c)
        qs_ = max([q for q, b, c in zip(qs, mpb, msc) if b >= c] or [0])
        if 1 <= qs_ < qm < 6:
            break
    g = r.choice(['electricity', 'cement', 'paper', 'chemicals', 'steel'])
    tab = table(['Output (000 tonnes)', 'MPB ($)', 'MPC ($)'], list(zip(qs, mpb, mpc)))
    stem = f'Production of {g} causes pollution with a constant marginal external cost of ${mec} per unit. {tab}. Identify (a) the free-market output and (b) the socially optimal output. (c) Explain the difference.'
    return {'stem': stem, 'answer': f'(a) {qm} thousand tonnes (b) {qs_} thousand tonnes (c) The market ignores the external cost, so over-produces by {qm - qs_} thousand tonnes.',
            'key': f'(a) largest output where MPB ≥ MPC: {qm} [1]; (b) MSC = MPC + {mec}: {", ".join(map(str, msc))}; largest output where MPB ≥ MSC: {qs_} [2]; (c) external cost ignored → over-production [1].'}


t4_2 = topic('Externalities and welfare loss diagrams', 'negative and positive externalities', 'welfare loss diagrams', 'externalities in production and consumption')
t4_2.fixed('C1', (1, 2, 3), [
    ('In a diagram of a negative production externality, the welfare loss is shown by the triangle between', 'MSC and MSB from the social optimum to the market output',
     'DWL: area between MSC and MSB (= MPB) over the units produced beyond the social optimum.', ['MPC and MPB below the market output', 'MSB and the horizontal axis', 'the price and the MPC curve up to the social optimum']),
    ('A positive consumption externality means that', 'MSB is greater than MPB, so the good is under-consumed',
     'External benefits make MSB > MPB; free-market output where MPB = MSC is below the optimum.', ['MSC is greater than MPC', 'MSB is less than MPB', 'the good is over-consumed']),
    ('Which is an example of a negative consumption externality?', 'Loud music from a party disturbing neighbours', 'Consumption by one person imposes a cost on third parties.',
     ['A farmer’s bees pollinating a neighbour’s orchard', 'A factory polluting a river', 'A vaccinated child protecting others']),
    ('A positive production externality shifts which curve below the private cost curve?', 'Marginal social cost', 'External benefits in production mean MSC < MPC.',
     ['Marginal private benefit', 'Marginal social benefit', 'Average revenue']),
])
t4_2.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain the welfare loss caused by a negative externality in production.',
     'Diagram: price/cost on vertical axis, quantity horizontal. MPB = MSB downward sloping; MPC upward sloping; MSC above MPC by the marginal external cost. Market output Q1 where MPC = MSB; social optimum Q* where MSC = MSB, at a higher price. Between Q* and Q1, MSC > MSB: the triangle between MSC and MSB from Q* to Q1 is the deadweight welfare loss.',
     '1 mark: correctly drawn curves; 1 mark: Q1 and Q*; 1 mark: identifies welfare loss area; 1 mark: explanation that MSC > MSB for those units [4]'),
    ('With the aid of a diagram, explain why a merit good with positive consumption externalities is under-consumed.',
     'Diagram: MPB below MSB; MPC = MSC. Market output Q1 where MPB = MPC; optimum Q* where MSB = MSC is larger. Units between Q1 and Q* have MSB > MSC but are not consumed: welfare loss triangle between MSB and MSC from Q1 to Q*.',
     '1 mark: MSB above MPB; 1 mark: Q1 < Q*; 1 mark: welfare loss triangle; 1 mark: reasoning [4]'),
    ('Explain why the welfare loss from a negative externality is not the whole of the external cost.', 'Only units produced beyond the social optimum cause a net loss; external costs on units up to the optimum are outweighed by net benefits, so the welfare loss is the triangle, not the full area between MSC and MPC.', '1 mark: only excess units; 1 mark: triangle vs full area [2]'),
])


@t4_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t4_2_dwl(r, D):
    b, dd = r.choice([1, 2]), r.choice([1, 2])
    e = (b + dd) * r.choice([2, 3, 4, 5])
    c = r.choice([10, 20, 30])
    qm = r.choice([20, 30, 40, 50])
    a = c + (b + dd) * qm
    kind = r.choice(['prod', 'cons'])
    g = r.choice(['fertiliser', 'plastic packaging', 'coal-fired electricity']) if kind == 'prod' else r.choice(['vaccinations', 'university places', 'bicycle commuting'])
    dq = e // (b + dd)
    if kind == 'prod':
        qs_ = qm - dq
        ps = a - b * qs_
        dwl = 0.5 * dq * e
        stem = f'In the market for {g}, MPB = MSB: P = {a} − {b}Q and MPC: P = {c} + {dd}Q, where P is in $ and Q in thousand units. Production imposes a constant marginal external cost of ${e}.'
        ans = f'Market output {qm} thousand; social optimum {qs_} thousand at P = ${ps}; welfare loss = ${num(dwl)} thousand.'
        key = (f'Market: {a} − {b}Q = {c} + {dd}Q → Q = {qm} [1]. MSC = {c + e} + {dd}Q; {a} − {b}Q = {c + e} + {dd}Q → Q* = {qs_} [1], P = {a} − {b}×{qs_} = {ps} [1]. '
               f'DWL = ½ × ({qm} − {qs_}) × {e} = {num(dwl)} (thousand $) [1].')
    else:
        qs_ = qm + dq
        ps = c + dd * qs_
        dwl = 0.5 * dq * e
        stem = f'In the market for {g}, MPB: P = {a} − {b}Q and MPC = MSC: P = {c} + {dd}Q, where P is in $ and Q in thousand units. Consumption gives a constant marginal external benefit of ${e}.'
        ans = f'Market output {qm} thousand; social optimum {qs_} thousand (MSC = ${ps}); welfare loss = ${num(dwl)} thousand.'
        key = (f'Market: {a} − {b}Q = {c} + {dd}Q → Q = {qm} [1]. MSB = {a + e} − {b}Q; {a + e} − {b}Q = {c} + {dd}Q → Q* = {qs_} [1], MSC there = {ps} [1]. '
               f'DWL = ½ × ({qs_} − {qm}) × {e} = {num(dwl)} (thousand $) [1].')
    if D <= 2:
        return cq(r, D, stem + ' Calculate the free-market output and the socially optimal output.', f'{qm} thousand and {qs_} thousand',
                  key, [f'{qs_} thousand and {qm} thousand', f'{qm} thousand and {qm} thousand', f'{qm + 2 * dq} thousand and {qm} thousand'], mcq_D=(1,))
    stem += ' Calculate the free-market output, the socially optimal output and price, and the deadweight welfare loss.'
    if D >= 5:
        stem += ' Explain what size of per-unit tax or subsidy would achieve the social optimum.'
        ans += f' A {"tax" if kind == "prod" else "subsidy"} of ${e} per unit (equal to the marginal external {"cost" if kind == "prod" else "benefit"}).'
        key += f' Pigouvian {"tax" if kind == "prod" else "subsidy"} = ${e} [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t4_3 = topic('Cost-benefit analysis', 'cost-benefit analysis', 'stages, uses and limitations')
t4_3.fixed('C1', (1, 2, 3), [
    ('Cost-benefit analysis is mainly used to', 'appraise public projects by comparing all social costs and benefits',
     'CBA weighs social (private + external) costs and benefits, usually discounted to present values.', ['calculate a firm’s profit', 'set the price of a public good', 'measure GDP']),
    ('A shadow price is', 'an estimated money value for a cost or benefit that has no market price', 'E.g. valuing time saved, noise or lives saved.',
     ['a price set below the market price', 'a black-market price', 'the price of an inferior good']),
    ('Future costs and benefits in a CBA are discounted because', 'money received in the future is worth less than the same amount today',
     'Time preference and opportunity cost of capital: PV = FV/(1 + r)ⁿ.', ['they are always smaller', 'inflation is always zero', 'governments do not borrow']),
    ('Which is usually the first stage of a cost-benefit analysis?', 'Identifying all relevant costs and benefits, private and external',
     'Stages: identify → value (shadow prices) → forecast and discount → compare (NPV, ratio) → decide/sensitivity analysis.', ['Calculating the net present value', 'Choosing the discount rate', 'Building the project']),
    ('A project should normally go ahead if', 'the present value of social benefits exceeds the present value of social costs', 'NPV > 0 or benefit–cost ratio > 1.',
     ['private benefits exceed private costs', 'it is profitable for the builder', 'it creates any jobs']),
])
t4_3.fixed('C2', (2, 3, 4), [
    ('Explain two limitations of cost-benefit analysis.', 'Valuing intangibles (noise, lives, environment) relies on uncertain shadow prices; choice of discount rate can change the result; forecasting future benefits is uncertain; distribution of costs and benefits is ignored by a simple total.', '1 mark each limitation identified, 1 mark each explained [4]'),
    ('Explain why the choice of discount rate matters in a cost-benefit analysis of a long-term project.', 'A higher discount rate reduces the present value of benefits far in the future more than near-term costs, so long-lived projects (e.g. flood defences) look less worthwhile; a low rate favours them.', '1 mark: higher rate lowers PV of distant flows; 1 mark: effect on decision [2]'),
    ('Explain how time savings from a new road might be valued in a cost-benefit analysis.', 'By estimating hours saved per journey × number of journeys × a shadow price per hour (e.g. average wage for work time, a lower value for leisure).', '1 mark: hours × journeys; 1 mark: shadow price per hour [2]'),
])


@t4_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t4_3_npv(r, D):
    d = ctx(r)
    rate = r.choice([3, 4, 5, 6, 8, 10])
    n = 3 if D <= 3 else 4
    cost0 = r.choice([100, 150, 200, 250, 300])
    ben = [r.choice([40, 50, 60, 70, 80, 90, 100]) for _ in range(n)]
    ec = r.choice([0, 5, 10, 15])
    proj = r.choice(['a new bypass road', 'a flood barrier', 'a light-rail line', 'a hospital extension', 'a solar farm', 'a sports stadium'])
    pvs = [(b - ec) / (1 + rate / 100) ** (t + 1) for t, b in enumerate(ben)]
    npv = sum(pvs) - cost0
    bcr = sum(pvs) / cost0
    stem = (f'The government of {d["country"]} is appraising {proj}. The initial cost is ${cost0}m (now). Expected social benefits are ' + ', '.join(f'${b}m in year {t + 1}' for t, b in enumerate(ben))
            + (f', with external costs of ${ec}m each year' if ec else '') + f'. The discount rate is {rate}%.')
    if D <= 2:
        t1 = (ben[0] - ec) / (1 + rate / 100)
        return cq(r, D, stem + ' Calculate the present value of the net benefit in year 1.', f'${num(t1, 2)}m', f'PV = ({ben[0]} − {ec})/1.{rate:02d} = ${num(t1, 2)}m.' if rate < 10 else f'PV = ({ben[0]} − {ec})/1.10 = ${num(t1, 2)}m.',
                  dis_num(r, t1, lambda x: f'${num(x, 2)}m', [ben[0] - ec, (ben[0] - ec) * (1 + rate / 100)]))
    stem += ' Calculate the net present value and the benefit–cost ratio, and state whether the project should go ahead.'
    ans = f'NPV = {money(round(npv, 2))}m; benefit–cost ratio = {num(bcr, 2)}; {"go ahead" if npv > 0 else "reject"} on these figures.'
    key = ('PV of net benefits: ' + '; '.join(f'year {t + 1}: {b - ec}/{num(1 + rate / 100, 2)}^{t + 1} = {num(p, 2)}' for t, (b, p) in enumerate(zip(ben, pvs)))
           + f' [2]. Sum = {num(sum(pvs), 2)}; NPV = {num(sum(pvs), 2)} − {cost0} = {num(npv, 2)} [1]; BCR = {num(bcr, 2)} [1]; decision [1].')
    if D >= 5:
        stem += ' Explain one reason why the decision might still be controversial.'
        ans += ' Shadow prices and forecasts are uncertain and the discount rate is a value judgement; those who bear the external costs may not be those who benefit.'
        key += ' Valid limitation (uncertainty, distribution, discount rate) [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


items(t4_3, 'C3', (2, 3, 4), [
    ('A proposed airport runway near {city} is being appraised. Classify each of the following as a private or external cost or benefit: (i) fares paid by passengers, (ii) noise for local residents, (iii) jobs created in local hotels, (iv) construction costs paid by the airport operator.',
     '(i) private benefit to passengers (revenue to airline), (ii) external cost, (iii) external benefit, (iv) private cost.', '1 mark each correct classification [4]'),
    ('A cost-benefit study of a new metro line in {city} values time saved at $12 per hour. Explain how using $6 per hour instead could change the decision and why the choice is difficult.',
     'Time savings are usually the largest benefit, so halving the shadow price could make NPV negative. The value is hard to set because work and leisure time differ and incomes vary across travellers.',
     '1 mark: lowers PV of benefits/NPV; 1 mark: could reverse decision; 1 mark: valuation difficulty [3]'),
])


def _ext_c4(r, D):
    d = ctx(r)
    pc = r.choice([50, 60, 80])
    ec = r.choice([10, 15, 20, 25])
    q = r.choice([200, 300, 400, 500])
    proj = r.choice(['a coal-fired power station', 'an open-cast mine', 'a chemical plant', 'a paper mill'])
    intro = (f'Extract: {proj.capitalize()} near {d["city"]} in {d["country"]} produces {q} thousand units a year at a private cost of ${pc} per unit. '
             f'Scientists estimate that air and water pollution impose an external cost of ${ec} per unit on local farms and residents. The government is considering a tax.')
    parts = [
        lambda r: ('Calculate the social cost per unit and the total external cost per year.', f'${pc + ec} per unit; ${num(ec * q / 1000, 1)}m a year', f'SC = {pc} + {ec} = {pc + ec} [1]; EC total = {ec} × {q},000 = ${num(ec * q / 1000, 1)}m [1] [2]'),
        lambda r: ('With the aid of a diagram, explain why the free market leads to a welfare loss.', 'MSC lies above MPC by the external cost; market output where MPC = MSB exceeds the optimum where MSC = MSB; welfare loss triangle between MSC and MSB over the excess output.', '1 mark curves; 1 mark outputs; 1 mark welfare loss area [3]'),
        lambda r: (f'Explain why the government might set a tax of ${ec} per unit.', 'A tax equal to the marginal external cost internalises the externality, shifting MPC up to MSC so the firm produces the socially optimal output.', '1 mark internalise; 1 mark output falls to optimum [2]'),
        lambda r: ('Assess whether a tax is the best way to deal with the pollution.', 'For: polluter pays, incentive to clean up, revenue. Against: hard to measure EC, inelastic demand limits output fall, regressive effect on prices, regulation or permits may give more certainty. Judgement.', '2 marks analysis, 2 marks evaluation [4]'),
        lambda r: ('Explain two difficulties in measuring the external cost.', 'Health and environmental damage have no market price (shadow pricing needed); effects are spread over many people and time; causation uncertain.', '1 mark each [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t4_1, t4_2, t4_3], 'C4', (3, 4, 5), 'case', _ext_c4)
essays(t4_1, [
    ('the free market will produce too much of goods that create external costs',
     'Explain the difference between private costs, external costs and social costs.',
     'Producers/consumers ignore external costs, so MPC < MSC and output exceeds the social optimum.',
     'Size of the externality and elasticity; Coase bargaining when property rights are clear and few parties; some producers self-regulate for reputation; measurement difficulties.'),
], ['Residents of {city} complain about traffic noise and air pollution from a new logistics centre.', 'Farmers in {country} use fertilisers that run off into rivers.'])
essays(t4_2, [
    ('the welfare loss from positive externalities is less serious than that from negative externalities',
     'With the aid of a diagram, explain the welfare loss from a positive externality in consumption.',
     'Positive externalities: under-consumption, welfare loss triangle between MSB and MSC; negative: over-production and harm to third parties.',
     'Size of loss depends on elasticities and size of externality, not its sign; education and vaccination losses can be large; long-run effects; equity aspects of who bears the cost.'),
    ('externalities provide the strongest case for government intervention in markets',
     'With the aid of a diagram, explain how a negative production externality causes a misallocation of resources.',
     'Externalities create welfare losses that markets cannot correct alone; taxes, subsidies, regulation.',
     'Other failures (public goods, monopoly, information) also justify intervention; government failure; measurement problems.'),
], ['Vaccination rates in {country} have fallen below the level needed to protect the whole population.', 'A chemical works in {city} discharges waste into a river used by fishing communities.'])
essays(t4_3, [
    ('cost-benefit analysis is the best way for a government to decide whether to build a new transport project',
     'Explain the stages involved in carrying out a cost-benefit analysis.',
     'CBA includes external effects, values them in money, discounts and compares, giving a consistent basis for decisions.',
     'Shadow pricing and forecasting uncertainty; discount rate choice; distributional effects ignored; political pressure; sensitivity analysis can help; other criteria (equity, environment) matter.'),
], ['The government of {country} must choose between a new airport and a high-speed rail line.', 'A city council in {city} has commissioned a cost-benefit study of a new bridge.'])

CHAPTERS[4] = [t4_1, t4_2, t4_3]

# ============================================================================ 5 Costs, revenue and profit
t5_1 = topic('Short-run production and diminishing returns', 'short-run production', 'law of diminishing returns', 'total, average and marginal product')
t5_1.fixed('C1', (1, 2, 3), [
    ('The law of diminishing returns states that', 'as more of a variable factor is added to a fixed factor, the marginal product of the variable factor will eventually fall',
     'Short-run law: at least one factor fixed; MP eventually declines.', ['as a firm grows, its long-run average cost rises', 'total product falls as soon as more workers are employed', 'returns fall when all factors are increased in proportion']),
    ('Marginal product of labour is', 'the change in total product from employing one more worker', 'MP = ΔTP/ΔL.',
     ['total product divided by the number of workers', 'the wage paid to the last worker', 'the revenue from the last worker']),
    ('When marginal product is above average product,', 'average product is rising', 'Marginal pulls the average: MP > AP → AP rises; MP cuts AP at its maximum.',
     ['average product is falling', 'total product is falling', 'marginal product must be falling']),
    ('The short run is defined as a period in which', 'at least one factor of production is fixed', 'Short run: some factors fixed; long run: all factors variable.',
     ['all factors are variable', 'output cannot be changed', 'firms cannot make a profit']),
    ('Total product is at its maximum when marginal product is', 'zero', 'TP peaks where the next worker adds nothing.', ['at its maximum', 'equal to average product', 'negative and rising']),
])
t5_1.fixed('C2', (2, 3, 4), [
    ('Explain why the law of diminishing returns applies only in the short run.', 'It depends on at least one factor (e.g. capital or land) being fixed; with more workers sharing the fixed factor, each extra worker eventually adds less. In the long run all factors can be varied.', '1 mark: fixed factor needed; 1 mark: crowding of fixed factor; 1 mark: LR all variable [3]'),
    ('Explain the relationship between marginal product and the marginal cost curve.', 'With a constant wage, MC = wage/MP. When MP rises, MC falls; once diminishing returns set in and MP falls, MC rises, giving a U-shaped MC curve.', '1 mark: MC = W/MP; 1 mark: rising MP lowers MC, falling MP raises MC [2]'),
    ('Explain why average product rises when marginal product is greater than average product.', 'If the extra worker adds more than the current average, the average must rise (like a high mark raising a class average).', '1 mark: marginal above average; 1 mark: pulls the average up [2]'),
])


@t5_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5_1_tp(r, D):
    for _ in range(30):
        peak = r.randint(2, 3)
        mp = []
        v = r.choice([8, 10, 12, 15])
        for i in range(7):
            if i < peak:
                v = v + r.choice([4, 5, 6, 8]) if i else v
            else:
                v = v - r.choice([3, 4, 5, 6])
            mp.append(v)
        if all(m > 0 for m in mp[:6]):
            break
    tp, s = [], 0
    for m in mp:
        s += m
        tp.append(s)
    L = list(range(1, 8))
    g = r.choice(['shirts', 'bicycles', 'loaves', 'chairs', 'meals'])
    tab = table(['Workers', f'Total product ({g} per day)'], list(zip(L, tp)))
    ap = [tp[i] / (i + 1) for i in range(7)]
    dr = mp.index(max(mp)) + 2
    if D <= 2:
        k = r.randint(2, 7)
        if r.random() < 0.5:
            return cq(r, D, f'{tab}. Calculate the marginal product of worker {k}.', f'{mp[k - 1]} {g}', f'MP = TP({k}) − TP({k - 1}) = {tp[k - 1]} − {tp[k - 2]} = {mp[k - 1]}.',
                      dis_num(r, mp[k - 1], lambda x: f'{num(x)} {g}', [tp[k - 1], ap[k - 1]]))
        return cq(r, D, f'{tab}. Calculate the average product when {k} workers are employed.', f'{num(ap[k - 1], 2)} {g}', f'AP = TP/L = {tp[k - 1]}/{k} = {num(ap[k - 1], 2)}.',
                  dis_num(r, ap[k - 1], lambda x: f'{num(x, 2)} {g}', [mp[k - 1], tp[k - 1]]))
    stem = f'A small factory with a fixed amount of machinery employs workers as follows. {tab}. (a) Calculate the marginal and average product for each number of workers. (b) Identify the worker at which diminishing marginal returns set in and explain why they occur.'
    ans = f'(a) MP: {", ".join(map(str, mp))}; AP: {", ".join(num(a, 1) for a in ap)} (b) From worker {dr}: MP falls because extra workers share a fixed stock of machinery.'
    key = '(a) MP = ΔTP [2], AP = TP/L [1]; (b) diminishing returns where MP first falls [1]; fixed factor explanation [1].'
    if D >= 4:
        w = r.choice([40, 50, 60, 80])
        mc = {i: w / mp[i] for i in (dr - 1, dr)}
        stem += f' (c) Each worker is paid ${w} a day. Calculate the marginal cost of output produced by worker {dr} and by worker {dr + 1}, and explain the link with diminishing returns.'
        ans += f' (c) MC = W/MP = {w}/{mp[dr - 1]} = ${num(mc[dr - 1], 2)} and {w}/{mp[dr]} = ${num(mc[dr], 2)}; MC rises as MP falls.'
        key += ' (c) MC = W/MP for both workers [1]; rising MC linked to falling MP [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t5_2 = topic('Short-run cost curves', 'short-run cost curves', 'fixed, variable, total, average and marginal costs')
t5_2.fixed('C1', (1, 2, 3), [
    ('Which cost does not change as output changes in the short run?', 'Total fixed cost', 'TFC (e.g. rent, interest) is independent of output in the SR.',
     ['Total variable cost', 'Marginal cost', 'Average total cost']),
    ('Average fixed cost always', 'falls as output rises', 'AFC = TFC/Q, so it falls continuously (spreading overheads).', ['rises as output rises', 'is U-shaped', 'equals marginal cost']),
    ('The marginal cost curve cuts the average total cost curve', 'at the minimum point of average total cost', 'When MC < ATC, ATC falls; when MC > ATC, ATC rises; so MC cuts ATC at its minimum.',
     ['at its maximum point', 'where AFC is lowest', 'at zero output']),
    ('A firm’s total cost rises from $500 to $540 when output increases from 20 to 21 units. Its marginal cost is', '$40', 'MC = ΔTC/ΔQ = 40/1.', ['$540', '$25.71', '$27']),
    ('The vertical distance between ATC and AVC at any output is equal to', 'average fixed cost', 'ATC = AVC + AFC.', ['marginal cost', 'total fixed cost', 'average revenue']),
])
t5_2.fixed('C2', (2, 3, 4), [
    ('Explain why the short-run average total cost curve is U-shaped.', 'At low output AFC falls rapidly and increasing returns lower AVC, so ATC falls; beyond a point diminishing returns raise AVC and MC by more than AFC falls, so ATC rises.', '1 mark: falling AFC; 1 mark: increasing then diminishing returns to variable factor; 1 mark: net effect [3]'),
    ('Explain why the gap between ATC and AVC narrows as output rises.', 'The gap is AFC = TFC/Q, which falls as fixed costs are spread over more units.', '1 mark: gap = AFC; 1 mark: spreading fixed cost [2]'),
    ('Explain why a firm might continue to produce in the short run even though it is making a loss.', 'If price covers average variable cost, each unit makes a contribution to fixed costs, which must be paid anyway; shutting down would make the loss larger (equal to TFC).', '1 mark: P ≥ AVC; 1 mark: contribution to fixed costs [2]'),
])


@t5_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5_2_costs(r, D):
    F, mc, tc, atc = _cost_sched(r)
    n = 6
    qs = list(range(1, n + 1))
    tvc = [t - F for t in tc[:n]]
    if D <= 2:
        k = r.randint(2, n)
        what = r.choice(['afc', 'avc', 'atc', 'mc'])
        val = {'afc': F / k, 'avc': tvc[k - 1] / k, 'atc': tc[k - 1] / k, 'mc': mc[k - 1]}[what]
        name = {'afc': 'average fixed cost', 'avc': 'average variable cost', 'atc': 'average total cost', 'mc': 'marginal cost'}[what]
        kk = {'afc': f'AFC = TFC/Q = {F}/{k}', 'avc': f'AVC = TVC/Q = {tvc[k - 1]}/{k}', 'atc': f'ATC = TC/Q = {tc[k - 1]}/{k}', 'mc': f'MC = TC({k}) − TC({k - 1}) = {tc[k - 1]} − {tc[k - 2]}'}[what]
        return cq(r, D, f'A firm has total fixed cost of ${F}. Its total variable cost at outputs 1 to {n} is: {", ".join(map(str, tvc))} ($). Calculate the {name} at an output of {k} units.',
                  money(round(val, 2)), kk + f' = {money(round(val, 2))}.', dis_num(r, val, lambda x: money(round(x, 2)), [tc[k - 1] / k, tvc[k - 1] / k, F / k, mc[k - 1]]))
    tab = table(['Output', 'Total cost ($)'], list(zip(qs, tc[:n])))
    stem = f'A firm’s short-run costs are shown. At zero output total cost is ${F}. {tab}. (a) Calculate TFC, AFC, AVC, ATC and MC at each output. (b) Identify the output at which MC cuts ATC and explain why.'
    ans = (f'(a) TFC = ${F}; AFC: {", ".join(num(F / q, 1) for q in qs)}; AVC: {", ".join(num(tvc[q - 1] / q, 1) for q in qs)}; ATC: {", ".join(num(tc[q - 1] / q, 1) for q in qs)}; MC: {", ".join(map(str, mc[:n]))}. '
           f'(b) Near the minimum of ATC (output {min(qs, key=lambda q: tc[q - 1] / q)}), because when MC < ATC the average falls and when MC > ATC it rises.')
    key = '(a) TFC = TC at Q = 0 [1]; AFC, AVC, ATC divisions [2]; MC differences [1]; (b) MC cuts ATC at its minimum, with reason [2].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t5_3 = topic('Long-run costs and economies of scale', 'long-run costs', 'economies and diseconomies of scale', 'lrac')
t5_3.fixed('C1', (1, 2, 3), [
    ('Economies of scale occur when', 'long-run average cost falls as the scale of output increases', 'Internal EoS: lower LRAC from growth of the firm.',
     ['short-run average cost falls as more workers are hired', 'total cost falls as output rises', 'prices fall as demand increases']),
    ('Which is an example of an external economy of scale?', 'A local college training skilled workers for firms in the industry', 'External EoS arise from growth of the industry in an area, lowering costs for all firms.',
     ['Bulk-buying discounts for a large supermarket', 'A large firm borrowing at lower interest rates', 'Using larger, more efficient machines']),
    ('The minimum efficient scale is', 'the lowest output at which long-run average cost is minimised', 'MES: where LRAC first reaches its minimum.',
     ['the output where the firm makes maximum profit', 'the smallest output a firm can produce', 'the output where marginal cost is zero']),
    ('Diseconomies of scale are most likely to be caused by', 'problems of communication, coordination and motivation in very large firms', 'Managerial diseconomies raise LRAC beyond some scale.',
     ['diminishing returns to a fixed factor', 'falling fixed costs per unit', 'bulk-buying discounts']),
    ('If all inputs are doubled and output rises by 150%, the firm experiences', 'increasing returns to scale', 'Output more than doubles (×2.5) when inputs double.',
     ['decreasing returns to scale', 'constant returns to scale', 'diminishing marginal returns']),
    ('Define the long run in production theory.', 'A period long enough for all factors of production to be varied.', '[1]'),
])
t5_3.fixed('C2', (2, 3, 4), [
    ('Explain two types of internal economies of scale.', 'Technical: larger, more efficient machinery and the law of increased dimensions; Purchasing: bulk-buying discounts; Financial: cheaper borrowing; Managerial: specialist managers; Risk-bearing: diversification. Each lowers LRAC.', '1 mark each type, 1 mark each explanation of lower unit cost [4]'),
    ('Explain why the long-run average cost curve is often L-shaped rather than U-shaped in practice.', 'Economies of scale are exhausted at the MES, but firms may avoid diseconomies through decentralisation and technology, so LRAC stays roughly constant over a wide range of output.', '1 mark: falling LRAC to MES; 1 mark: diseconomies avoided, constant beyond [2]'),
    ('Distinguish between diminishing returns and diseconomies of scale.', 'Diminishing returns is a short-run concept with at least one factor fixed (MP falls); diseconomies of scale occur in the long run when all factors vary and LRAC rises as the firm grows.', '1 mark each [2]'),
])


@t5_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5_3_lrac(r, D):
    out = [10, 20, 30, 40, 50, 60, 70]
    for _ in range(30):
        base = r.choice([30, 36, 40, 45, 50, 60])
        mes = r.randint(2, 4)
        lrac = []
        for i in range(7):
            if i < mes:
                lrac.append(base - (mes - i) * 0 + (mes - i) * r.choice([4, 5, 6, 8]))
            elif i < mes + 2:
                lrac.append(base)
            else:
                lrac.append(base + (i - mes - 1) * r.choice([2, 3, 4]))
        lrac = [base + (mes - i) * 5 if i < mes else x for i, x in enumerate(lrac)]
        if len(set(lrac[:mes + 1])) == mes + 1:
            break
    unit = 'thousand units'
    tab = table([f'Output ({unit})', 'LRAC ($)'], list(zip(out, lrac)))
    q_mes = out[mes]
    if D <= 2:
        opts, a = mcq(r, f'{q_mes} {unit}', [f'{q} {unit}' for q in out if q != q_mes])
        return {'stem': f'A firm’s long-run average cost schedule is: {tab}. What is the minimum efficient scale of production?', 'options': opts, 'answer': a,
                'key': f'MES = lowest output at which LRAC reaches its minimum (${base}): {q_mes} {unit}.'}
    small = r.choice(out[:mes])
    adv = 100 * (lrac[out.index(small)] - base) / lrac[out.index(small)]
    mkt = r.choice([60, 80, 100, 120, 200, 400])
    stem = (f'A firm’s long-run average cost schedule is: {tab}. (a) Identify the minimum efficient scale and the range of output with diseconomies of scale. '
            f'(b) Calculate the percentage cost disadvantage of a firm producing {small} {unit} compared with a firm at the MES.')
    ans = f'(a) MES = {q_mes} {unit}; diseconomies from above {out[mes + 1]} {unit} (LRAC rises). (b) ({lrac[out.index(small)]} − {base})/{lrac[out.index(small)]} × 100 = {pct(adv)} higher unit cost.'
    key = '(a) MES identified [1]; rising LRAC = diseconomies [1]; (b) correct % calculation [2].'
    if D >= 4:
        n = mkt / q_mes
        stem += f' (c) Total market demand is {mkt} {unit}. Calculate how many firms of minimum efficient scale the market can support and comment on the likely market structure.'
        ans += f' (c) {mkt}/{q_mes} = {num(n, 1)} firms; ' + ('few firms → oligopoly or natural monopoly.' if n < 5 else 'many firms can operate at low cost → competitive structure possible.')
        key += ' (c) market size ÷ MES [1]; structure inference [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


items(t5_3, 'C2', (2, 3, 4), [
    ('{firm}, {a_ind} business, plans to double its size by opening new plants. Explain two economies of scale it might gain and one diseconomy it might face.',
     'Economies: purchasing (bulk discounts on inputs), financial (lower interest rates as a larger borrower), technical (larger, more efficient capital). Diseconomy: communication and coordination problems or lower worker motivation raise LRAC.',
     '1 mark each economy explained (2 × 1), 1 mark diseconomy [3]'),
    ('Many {ind} firms in {country} have clustered around {city}. Explain how they may benefit from external economies of scale.',
     'Industry growth in one area gives a pool of skilled labour, specialist suppliers and services, shared infrastructure and knowledge spillovers, lowering costs for every firm.',
     '1 mark: definition (industry growth); 1 mark each example (up to 2) [3]'),
])

t5_4 = topic('Revenue and types of profit', 'total, average and marginal revenue', 'normal, subnormal and supernormal profit', 'revenue')
t5_4.fixed('C1', (1, 2, 3), [
    ('Normal profit is', 'the minimum profit needed to keep a firm in the industry, included in average cost', 'Normal profit = opportunity cost of the entrepreneur; AR = ATC.',
     ['any profit above average cost', 'profit after tax', 'the maximum profit a firm can make']),
    ('A firm earns supernormal profit when', 'average revenue is greater than average total cost', 'AR > ATC (including normal profit).', ['average revenue equals average total cost', 'marginal revenue equals marginal cost', 'total revenue equals total variable cost']),
    ('For a firm facing a downward-sloping demand curve, marginal revenue', 'is less than average revenue', 'To sell more it must cut price on all units, so MR < AR (MR falls twice as fast for linear demand).',
     ['equals average revenue', 'is greater than average revenue', 'is always zero']),
    ('Total revenue is maximised where', 'marginal revenue is zero', 'TR peaks where MR = 0, at unit price elasticity.', ['marginal revenue equals marginal cost', 'average revenue is zero', 'price is highest']),
    ('In perfect competition, the firm’s average revenue curve is', 'horizontal and equal to marginal revenue', 'Price taker: P = AR = MR.', ['downward sloping', 'vertical', 'upward sloping']),
    ('Define subnormal profit.', 'Profit below normal profit, so total revenue is less than total cost (AR < ATC); the firm is making an economic loss.', '[1]'),
])
t5_4.fixed('C2', (2, 3, 4), [
    ('Explain the relationship between price elasticity of demand and marginal revenue.', 'Where demand is price elastic, a price cut raises TR so MR > 0; at unit elasticity MR = 0 and TR is at a maximum; where demand is inelastic, MR < 0.', '1 mark each region [3]'),
    ('Explain why normal profit is treated as a cost.', 'It is the opportunity cost of the entrepreneur’s time and capital: the return needed to keep resources in this use rather than the next best alternative.', '1 mark: opportunity cost; 1 mark: needed to keep firm in industry [2]'),
    ('Explain why supernormal profit may be competed away in the long run in some markets but not in others.', 'Where barriers to entry are low, supernormal profit attracts new firms, shifting each firm’s demand left until AR = ATC; where barriers are high (monopoly, oligopoly), entry is blocked and profit persists.', '1 mark: entry signal; 1 mark: demand shifts until normal profit; 1 mark: barriers prevent this [3]'),
])


@t5_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t5_4_rev(r, D):
    a = r.choice([40, 48, 50, 60, 72, 80])
    b = r.choice([2, 4, 5]) if a % 2 == 0 else 5
    qs = list(range(1, 8))
    p = [a - b * q for q in qs]
    tr = [pp * q for pp, q in zip(p, qs)]
    mr = [tr[0]] + [tr[i] - tr[i - 1] for i in range(1, 7)]
    if D <= 2:
        k = r.randint(2, 7)
        return cq(r, D, f'A firm faces the demand schedule: price ($) {", ".join(map(str, p))} for quantities 1 to 7. Calculate the marginal revenue of unit {k}.', money(mr[k - 1]),
                  f'TR({k}) − TR({k - 1}) = {tr[k - 1]} − {tr[k - 2]} = {money(mr[k - 1])}.', dis_num(r, mr[k - 1], money, [p[k - 1], tr[k - 1]]))
    atc = r.choice([p[2] + 4, p[3], p[4] - 3, p[3] - 2])
    q = r.choice([3, 4, 5])
    prof = (p[q - 1] - atc) * q
    kind = 'supernormal' if prof > 0 else ('normal' if prof == 0 else 'subnormal')
    stem = (f'A firm faces this demand schedule: quantity 1 to 7; price ($) {", ".join(map(str, p))}. (a) Calculate total and marginal revenue at each output. '
            f'(b) At an output of {q} units, average total cost (including normal profit) is ${atc}. Calculate the profit and state the type of profit earned.')
    ans = f'(a) TR: {", ".join(map(str, tr))}; MR: {", ".join(map(str, mr))} (b) ({p[q - 1]} − {atc}) × {q} = {money(prof)}: {kind} profit.'
    key = '(a) TR = P × Q [1], MR = ΔTR [1]; (b) profit = (AR − ATC) × Q [1]; correct classification [1].'
    if D >= 4:
        qmax = max(range(7), key=lambda i: tr[i]) + 1
        stem += ' (c) Identify the output that maximises total revenue and explain what this tells you about price elasticity of demand at that point.'
        ans += f' (c) TR is highest at {qmax} units, where MR ≈ 0, so PED ≈ 1 (unit elastic) there; demand is elastic above that price and inelastic below it.'
        key += ' (c) TR max where MR = 0 [1]; unit elasticity [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


def _cost_c4(r, D):
    d = ctx(r)
    F, mc, tc, atc = _cost_sched(r)
    p = r.choice([mc[3], mc[4]]) + 1
    qs = list(range(1, 7))
    tab = table(['Output (000 units)', 'Total cost ($000)'], list(zip(qs, tc[:6])))
    best_q = max(qs, key=lambda q: p * q - tc[q - 1])
    profit = p * best_q - tc[best_q - 1]
    intro = f'{d["firm"]} makes {d["good"]} in {d["country"]} and sells in a competitive market at ${p} per unit. Fixed costs are ${F} thousand. {tab}.'
    parts = [
        lambda r: ('Calculate the marginal cost of each thousand units.', ', '.join(map(str, mc[:6])), 'MC = ΔTC [2]'),
        lambda r: ('Calculate average total cost at each output and identify its minimum.', ', '.join(num(tc[q - 1] / q, 1) for q in qs) + f'; minimum at {min(qs, key=lambda q: tc[q - 1] / q)}', 'ATC = TC/Q [2]'),
        lambda r: ('Identify the profit-maximising output and calculate the profit.', f'{best_q} thousand units; ' + (f'profit ${num(profit)} thousand' if profit >= 0 else f'loss minimised at ${num(-profit)} thousand'), f'Max of TR − TC (or P = MC): TR = {p}×{best_q}, profit = {num(profit)} [3]'),
        lambda r: ('Explain why marginal cost eventually rises in the short run.', 'Diminishing marginal returns to the variable factor: each extra worker adds less output, so the cost of each extra unit rises.', '[2]'),
        lambda r: ('Discuss whether the firm should expand its plant in the long run.', 'Possible economies of scale (bulk buying, technical) lower LRAC; but diseconomies, market size and price may fall as industry supply grows; depends on MES and demand.', '2 analysis, 2 evaluation [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t5_1, t5_2, t5_3, t5_4], 'C4', (3, 4, 5), 'case', _cost_c4)
essays(t5_3, [
    ('growth always reduces a firm’s average costs',
     'Explain the difference between internal and external economies of scale.',
     'Internal economies (technical, purchasing, financial, managerial, risk-bearing) lower LRAC as firm grows; external economies from industry growth.',
     'Diseconomies of scale (communication, motivation, coordination); MES may be reached at low output; L-shaped LRAC; growth by merger may bring culture clashes.'),
    ('small firms can never compete with large firms on cost',
     'With the aid of a diagram, explain the shape of the long-run average cost curve.',
     'Large firms reach MES and enjoy economies of scale.',
     'Small firms can be efficient where MES is small, niche markets, flexibility, lower overheads, external economies and franchising.'),
], ['{firm} has doubled its output by opening a second factory in {city}.', 'The {ind} industry in {country} is dominated by a few very large firms.'])
essays(t5_1, [
    ('the law of diminishing returns explains why firms’ costs eventually rise as output increases',
     'Explain the relationship between marginal product and marginal cost.',
     'With a fixed factor, MP eventually falls so MC and AVC rise; explains U-shaped SR cost curves.',
     'Only applies in the short run; in the long run firms change all inputs and may gain economies of scale; technology and training can raise MP.'),
], ['A farm in {country} hires extra seasonal workers at harvest time but has a fixed amount of land and machinery.'])
essays(t5_2, [
    ('a firm should close down if it is making a loss',
     'Explain the difference between fixed and variable costs and why the distinction matters in the short run.',
     'In the short run the firm should continue if P ≥ AVC because it covers some fixed costs; close if P < AVC.',
     'In the long run must cover ATC; expectations of future demand; strategic reasons (market share, loss leaders); exit costs.'),
], ['{firm} reports a loss for the second year running as demand for {good} falls.'])
essays(t5_4, [
    ('firms will always aim to earn supernormal profit',
     'Explain the difference between normal, subnormal and supernormal profit.',
     'Supernormal profit rewards risk and funds investment; signals entry.',
     'Alternative objectives (sales, revenue, satisficing); fear of regulation or entry; long-run normal profit in competitive markets.'),
], ['{firm} earned profits well above the industry average last year.'])
CHAPTERS[5] = [t5_1, t5_2, t5_3, t5_4]

# ============================================================================ 6 Market structures
t6_1 = topic('Perfect competition', 'perfect competition', 'short-run and long-run equilibrium')
t6_1.fixed('C1', (1, 2, 3), [
    ('Which is a characteristic of perfect competition?', 'Firms are price takers selling a homogeneous product', 'Many buyers and sellers, identical products, perfect information, free entry and exit.',
     ['Firms sell differentiated products', 'There are high barriers to entry', 'There are a few large interdependent firms']),
    ('In the short run a perfectly competitive firm will shut down if price falls below', 'average variable cost', 'If P < AVC the firm cannot cover variable costs; shutting down limits the loss to TFC.',
     ['average total cost', 'marginal cost', 'average fixed cost']),
    ('In long-run equilibrium in perfect competition', 'price equals minimum average total cost and firms earn normal profit', 'Entry/exit drives P to min ATC: P = MC = AR = MR = min ATC.',
     ['firms earn supernormal profit', 'price exceeds marginal cost', 'firms produce on the falling part of ATC']),
    ('The short-run supply curve of a perfectly competitive firm is', 'its marginal cost curve above average variable cost', 'Firm produces where P = MC, provided P ≥ AVC.',
     ['its average total cost curve', 'its marginal revenue curve', 'horizontal at the market price']),
    ('If firms in a perfectly competitive industry are making supernormal profits, in the long run', 'new firms enter, market supply rises and price falls until profits are normal',
     'Free entry eliminates supernormal profit.', ['price rises as demand increases', 'firms leave the industry', 'firms raise prices to increase profits']),
])
t6_1.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain how a perfectly competitive industry moves from short-run supernormal profit to long-run equilibrium.',
     'Diagram pair: industry S and D set price P1; firm’s horizontal AR = MR at P1 above ATC at output where MC = MR, shaded supernormal profit. Free entry shifts industry supply right, price falls to P2 = min ATC; firm’s AR = MR falls until tangent to ATC at its minimum: normal profit.',
     '1 mark: SR profit shown; 1 mark: entry shifts supply; 1 mark: price falls; 1 mark: LR at min ATC with normal profit [4]'),
    ('Explain why a perfectly competitive firm cannot charge a price above the market price.', 'Products are homogeneous and buyers have perfect information, so if it raises its price consumers switch to identical rivals and its sales fall to zero: demand for its output is perfectly elastic.', '1 mark: homogeneous/perfect info; 1 mark: perfectly elastic demand [2]'),
    ('Explain why perfect competition is said to be allocatively and productively efficient in the long run.', 'In LR equilibrium P = MC (allocative) and output is at the minimum point of ATC (productive), with normal profit.', '1 mark each [2]'),
])


@t6_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_1_pc(r, D):
    q = r.choice([100, 200, 400, 500, 1000])
    case = r.choice(['profit', 'loss_stay', 'shut'])
    atc = r.choice([8, 10, 12, 15, 20])
    avc = atc - r.choice([2, 3, 4])
    if case == 'profit':
        p = atc + r.choice([1, 2, 3])
    elif case == 'loss_stay':
        p = r.choice([x for x in range(avc + 1, atc)] or [avc + 1])
    else:
        p = avc - r.choice([1, 2])
    prof = (p - atc) * q
    g = r.choice(['wheat', 'tomatoes', 'eggs', 'potatoes', 'milk'])
    stem = f'A perfectly competitive {g} producer sells {q} units where price = MC = ${p}. At this output ATC is ${atc} and AVC is ${avc}.'
    dec = {'profit': 'continue; supernormal profit attracts entry, so price will fall in the long run',
           'loss_stay': 'continue in the short run because P > AVC (covers some fixed costs), but leave in the long run if the loss persists',
           'shut': 'shut down: P < AVC so it cannot even cover variable costs'}[case]
    if D <= 2:
        return cq(r, D, stem + ' Calculate the firm’s profit or loss.', money(prof), f'(P − ATC) × Q = ({p} − {atc}) × {q} = {money(prof)}.',
                  dis_num(r, prof, money, [(p - avc) * q, p * q, -prof]))
    ans = f'Profit = ({p} − {atc}) × {q} = {money(prof)}; the firm should {dec}.'
    key = f'Profit = (AR − ATC) × Q [1] = {money(prof)} [1]; compare P with AVC and ATC [1]; correct short- and long-run decision [1].'
    stem += ' Calculate the profit or loss and explain what the firm should do in the short run and in the long run.'
    if D >= 5 and case != 'profit':
        loss_shut = -(atc - avc) * q
        stem += ' Show that your recommendation minimises the loss.'
        ans += f' If it shuts down the loss is TFC = (ATC − AVC) × Q = {money(loss_shut)}.'
        key += ' Compare with loss on shutdown (= TFC) [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'numerical'}


t6_2 = topic('Monopoly and natural monopoly', 'monopoly and natural monopoly', 'barriers to entry', 'monopoly')
t6_2.fixed('C1', (1, 2, 3), [
    ('A profit-maximising monopolist produces where', 'marginal cost equals marginal revenue, and charges the price on the demand curve at that output',
     'MC = MR gives Q; price read from AR at that Q.', ['price equals marginal cost', 'average cost is minimised', 'marginal revenue is zero']),
    ('A natural monopoly exists when', 'one firm can supply the whole market at a lower average cost than two or more firms',
     'Economies of scale so large that LRAC falls over the whole market range, e.g. water pipes.', ['the government owns the only firm', 'a firm controls a natural resource', 'a firm has a patent']),
    ('Which is a barrier to entry?', 'Large sunk costs of setting up', 'Barriers: sunk costs, economies of scale, patents, control of resources, brand loyalty, legal barriers.',
     ['Perfect information', 'Homogeneous products', 'Low fixed costs']),
    ('Compared with perfect competition with the same costs, a monopoly is likely to charge', 'a higher price and produce a lower output', 'Monopoly restricts output to where MR = MC < P.',
     ['a lower price and produce a higher output', 'the same price and output', 'a higher price and produce a higher output']),
    ('A monopolist will never choose to produce on the price-inelastic part of its demand curve because', 'marginal revenue is negative there', 'MR < 0 when |PED| < 1; MC > 0, so MR = MC cannot occur there.',
     ['average revenue is zero there', 'marginal cost is negative', 'price is too low to cover fixed costs']),
])
t6_2.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain the profit-maximising equilibrium of a monopolist.',
     'Diagram: downward-sloping AR (demand) with MR below it, twice as steep; U-shaped MC and ATC. Output Qm where MC = MR; price Pm read off AR above Qm; ATC at Qm below Pm; supernormal profit = (Pm − ATC) × Qm shaded rectangle; barriers keep it in the long run.',
     '1 mark: AR and MR; 1 mark: MC = MR output; 1 mark: price from AR; 1 mark: profit area [4]'),
    ('Explain why a natural monopoly may be better for consumers than competition.', 'With huge economies of scale, one firm has lower average costs than several firms duplicating infrastructure, so price could be lower, especially if regulated.', '1 mark: falling LRAC across market; 1 mark: duplication avoided/lower costs [2]'),
    ('Explain why a monopoly may be X-inefficient.', 'Lack of competitive pressure means managers may allow costs to rise above the minimum possible for each output (organisational slack), so the firm operates above its cost curve.', '1 mark: lack of competition; 1 mark: costs above the lowest possible [2]'),
])


@t6_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_2_mono(r, D):
    b = r.choice([1, 2, 0.5])
    c = r.choice([10, 20, 30, 40])
    qm = r.choice([10, 15, 20, 25, 30, 40])
    a = c + 2 * b * qm
    pm = a - b * qm
    qc = 2 * qm
    prof = (pm - c) * qm
    dwl = 0.5 * (qc - qm) * (pm - c)
    F = r.choice([0, 100, 200, 300]) if D >= 4 else 0
    stem = f'A monopolist faces demand P = {num(a)} − {num(b)}Q (so MR = {num(a)} − {num(2 * b)}Q) and has constant marginal and average variable cost of ${c}' + (f' with fixed costs of ${F}' if F else '') + '.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the profit-maximising output.', f'{qm} units', f'MR = MC: {num(a)} − {num(2 * b)}Q = {c} → Q = {qm}.',
                  dis_num(r, qm, lambda x: f'{num(x)} units', [qc, a / b]))
    stem += ' Calculate the profit-maximising output, price and profit. Compare with the output and price if the industry were perfectly competitive, and calculate the deadweight welfare loss.'
    ans = f'Q = {qm}, P = ${num(pm)}, profit = {money(prof - F)}; competitive Q = {num(qc)}, P = ${c}; deadweight loss = {money(dwl)}.'
    key = (f'MR = MC → Q = ({num(a)} − {c})/{num(2 * b)} = {qm} [1]; P = {num(a)} − {num(b)}×{qm} = {num(pm)} [1]; profit = ({num(pm)} − {c})×{qm}' + (f' − {F}' if F else '') + f' = {money(prof - F)} [1]; '
           f'competitive P = MC = {c}, Q = {num(qc)} [1]; DWL = ½ × ({num(qc)} − {qm}) × ({num(pm)} − {c}) = {money(dwl)} [1].')
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t6_3 = topic('Monopolistic competition', 'monopolistic competition')
t6_3.fixed('C1', (1, 2, 3), [
    ('Which is a feature of monopolistic competition?', 'Many firms selling differentiated products with low barriers to entry', 'Monopolistic competition: many firms, product differentiation, free entry, some price-setting power.',
     ['A single firm with high barriers to entry', 'A few interdependent firms', 'Firms selling identical products as price takers']),
    ('In long-run equilibrium under monopolistic competition, the firm’s demand curve is', 'tangent to the average cost curve to the left of its minimum point', 'Entry removes supernormal profit: AR = ATC, with excess capacity.',
     ['tangent to ATC at its minimum', 'horizontal at the market price', 'above ATC at all outputs']),
    ('Firms in monopolistic competition have excess capacity in the long run because', 'they produce less than the output at minimum average cost', 'Tangency on the falling part of ATC: not productively efficient.',
     ['they produce where P = MC', 'they make supernormal profits', 'they face perfectly elastic demand']),
    ('An example of a monopolistically competitive market is', 'restaurants in a large city', 'Many sellers, differentiated menus/locations, easy entry.',
     ['national electricity transmission', 'the market for wheat', 'aircraft manufacturing']),
])
t6_3.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain the long-run equilibrium of a firm in monopolistic competition.',
     'Diagram: downward-sloping AR with MR below; U-shaped ATC and MC. Output where MC = MR; at that output AR is tangent to ATC, so P = ATC and only normal profit is earned; the tangency is to the left of minimum ATC, showing excess capacity; P > MC.',
     '1 mark: MC = MR; 1 mark: AR tangent to ATC; 1 mark: normal profit; 1 mark: excess capacity/P > MC [4]'),
    ('Explain why firms in monopolistic competition spend heavily on advertising and branding.', 'To differentiate their products, build brand loyalty and make demand less price elastic, giving more power to set prices and shift demand to the right.', '1 mark: differentiation; 1 mark: less elastic/more demand [2]'),
    ('Explain why supernormal profits do not last in monopolistic competition.', 'Low barriers to entry let new firms offer close substitutes, taking customers so each firm’s demand shifts left and becomes more elastic until P = ATC.', '1 mark: entry; 1 mark: demand falls until normal profit [2]'),
])


@t6_3.add('C3', (1, 2, 3, 4), 'numerical')
def t6_3_mc(r, D):
    d = ctx(r)
    biz = r.choice(['hair salon', 'café', 'pizza restaurant', 'gym', 'bakery'])
    q = r.choice([400, 500, 600, 800, 1000])
    p = r.choice([12, 15, 18, 20, 25])
    atc = p - r.choice([2, 3, 4, 5])
    prof = (p - atc) * q
    qmin = q + r.choice([100, 150, 200, 250])
    stem = f'A {biz} in {d["city"]} sells {q} units a week at ${p} where MR = MC; average total cost is ${atc}.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate its weekly supernormal profit.', money(prof), f'(P − ATC) × Q = ({p} − {atc}) × {q} = {money(prof)}.',
                  dis_num(r, prof, money, [p * q, atc * q]))
    return {'stem': stem + f' (a) Calculate its supernormal profit. (b) Explain what will happen to this profit in the long run. (c) In the long run the firm sells {q - r.choice([50, 100])} units, while minimum ATC occurs at {qmin} units. Explain what this shows about efficiency.',
            'answer': f'(a) {money(prof)} a week (b) New {biz}s enter, demand for this firm shifts left and becomes more elastic until AR is tangent to ATC: normal profit. (c) Output is below the minimum-ATC output, so there is excess capacity: not productively efficient, and P > MC so not allocatively efficient.',
            'key': '(a) (P − ATC) × Q [2]; (b) entry, demand shifts left, normal profit [2]; (c) excess capacity, productive and allocative inefficiency [2].', 'type': 'multi_step'}


t6_4 = topic('Oligopoly and game theory', 'oligopoly', 'interdependence', 'kinked demand curve', 'collusion and game theory')
t6_4.fixed('C1', (1, 2, 3), [
    ('The key feature that distinguishes oligopoly from other market structures is', 'interdependence between a few large firms', 'Each firm’s decisions depend on expected reactions of rivals.',
     ['a homogeneous product', 'freedom of entry', 'a single seller']),
    ('The kinked demand curve model is used to explain', 'why prices in oligopoly tend to be stable', 'Rivals match price cuts but not rises; the gap in MR means MC can change without changing price.',
     ['why oligopolists always collude', 'why monopolists make losses', 'why prices are flexible in perfect competition']),
    ('In the kinked demand curve model, the demand curve above the current price is relatively', 'elastic, because rivals do not follow a price rise', 'A price rise loses many customers to rivals who keep prices unchanged.',
     ['inelastic, because rivals follow a price rise', 'perfectly inelastic', 'vertical']),
    ('A cartel is', 'a formal agreement between firms to restrict output and fix prices', 'Explicit collusion, usually illegal; e.g. OPEC between countries.',
     ['a merger between two firms', 'a market with one buyer', 'a price war between rivals']),
    ('A Nash equilibrium is a situation in which', 'each player’s strategy is the best response to the other’s strategy, so no one wants to change',
     'Game theory equilibrium: no unilateral incentive to deviate.', ['both players earn the highest possible payoff', 'players collude to maximise joint profit', 'one player always wins']),
    ('A five-firm concentration ratio of 85% means that', 'the five largest firms have 85% of market sales', 'CR5 = combined market share of the five largest firms.',
     ['there are 85 firms', 'each firm has 17% of the market', 'the market is perfectly competitive']),
])
t6_4.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain why prices may be rigid in an oligopoly according to the kinked demand curve model.',
     'Diagram: demand curve kinked at current price P1: elastic above (rivals ignore a rise), inelastic below (rivals match a cut). The MR curve has a vertical gap below the kink. MC can shift up or down within the gap and MC = MR still gives the same output and price.',
     '1 mark: kink and reasons; 1 mark: MR discontinuity; 1 mark: MC shifts within gap leave P unchanged [3]'),
    ('Explain why collusion may break down in an oligopoly.', 'Each firm has an incentive to cheat by cutting price or raising output to gain market share; it is hard to monitor rivals; new entrants, falling demand and competition authorities also undermine agreements.', '1 mark: incentive to cheat; 1 mark: another reason [2]'),
    ('Explain why oligopolists often compete through non-price competition.', 'Price cuts are quickly matched and risk a price war that lowers everyone’s profit, so firms compete through advertising, branding, quality and loyalty schemes, which are harder to copy.', '1 mark: price war risk; 1 mark: non-price methods [2]'),
    ('Distinguish between tacit and explicit collusion.', 'Explicit collusion is a formal (usually illegal) agreement to fix prices or output; tacit collusion is coordination without agreement, e.g. price leadership.', '1 mark each [2]'),
])


def _game(r):
    labels = r.choice([('High price', 'Low price'), ('Advertise', 'Do not advertise'), ('Launch new model', 'Do not launch'), ('Expand capacity', 'Keep capacity')])
    while True:
        pay = {(i, j): (r.choice(range(2, 21)), r.choice(range(2, 21))) for i in range(2) for j in range(2)}
        vals = [v for p in pay.values() for v in p]
        if len(set(vals)) >= 6:
            break
    return labels, pay


def _analyse_game(pay):
    domA = [i for i in range(2) if all(pay[(i, j)][0] > pay[(1 - i, j)][0] for j in range(2))]
    domB = [j for j in range(2) if all(pay[(i, j)][1] > pay[(i, 1 - j)][1] for i in range(2))]
    nash = [(i, j) for i in range(2) for j in range(2) if pay[(i, j)][0] >= pay[(1 - i, j)][0] and pay[(i, j)][1] >= pay[(i, 1 - j)][1]]
    return domA, domB, nash


@t6_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_4_game(r, D):
    labels, pay = _game(r)
    if D >= 3 and r.random() < 0.6:  # prisoners' dilemma structure
        t_, h, l, s = sorted(r.sample(range(2, 30), 4), reverse=True)
        pay = {(0, 0): (h, h), (0, 1): (s, t_), (1, 0): (t_, s), (1, 1): (l, l)}
        labels = r.choice([('High price', 'Low price'), ('Keep to the quota', 'Exceed the quota'), ('Do not advertise', 'Advertise')])
    f1, f2 = r.sample(FIRMS, 2)
    domA, domB, nash = _analyse_game(pay)
    cell = lambda i, j: f'{f1} {labels[i]} and {f2} {labels[j]}: ({pay[(i, j)][0]}, {pay[(i, j)][1]})'
    mat = '; '.join(cell(i, j) for i in range(2) for j in range(2))
    stem = f'Two firms, {f1} and {f2}, choose a strategy at the same time. Payoffs (profit in $m, {f1} first, {f2} second): {mat}.'
    dA = labels[domA[0]] if domA else 'none'
    dB = labels[domB[0]] if domB else 'none'
    ne = '; '.join(f'{f1} {labels[i]}, {f2} {labels[j]}' for i, j in nash) or 'no pure-strategy Nash equilibrium'
    joint = max(pay, key=lambda k: sum(pay[k]))
    if D <= 2:
        right = f'{dA}' if domA else 'It has no dominant strategy'
        opts, a = mcq(r, right, [x for x in (labels[0], labels[1], 'It has no dominant strategy', 'It depends only on its own costs') if x != right])
        return {'stem': stem + f' What is {f1}’s dominant strategy?', 'options': opts, 'answer': a,
                'key': f'Compare {f1}’s payoffs for each choice of {f2}: dominant strategy = {dA}.'}
    stem += f' (a) Identify any dominant strategy for each firm. (b) Identify the Nash equilibrium. (c) Explain whether the firms have an incentive to collude.'
    ans = (f'(a) {f1}: {dA}; {f2}: {dB}. (b) {ne}. (c) Joint profit is highest when {f1} chooses {labels[joint[0]]} and {f2} chooses {labels[joint[1]]} (total ${sum(pay[joint])}m)'
           + (', which differs from the Nash equilibrium, so there is an incentive to collude, but each firm also has an incentive to cheat.' if joint not in nash else ', which is already a Nash equilibrium, so collusion adds little.'))
    key = '(a) compare payoffs column by column and row by row [2]; (b) best response for both [1]; (c) joint-profit outcome vs Nash; incentive to cheat/prisoners’ dilemma [2].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


@t6_4.add('C3', (1, 2, 3, 4), 'numerical')
def t6_4_cr(r, D):
    for _ in range(50):
        sh = sorted(r.sample(range(3, 30), 6), reverse=True)
        if sum(sh) < 100:
            break
    rest = 100 - sum(sh)
    n = r.choice([3, 4, 5])
    cr = sum(sh[:n])
    ind = r.choice(INDUSTRIES)
    stem = f'In the {ind} industry of {r.choice(COUNTRIES)}, the six largest firms have market shares of {", ".join(str(x) + "%" for x in r.sample(sh, 6))}; the remaining {rest}% is shared by many small firms. Calculate the {n}-firm concentration ratio.'
    if D <= 2:
        return cq(r, D, stem, f'{cr}%', f'CR{n} = sum of the {n} largest shares = {" + ".join(map(str, sh[:n]))} = {cr}%.', dis_num(r, cr, lambda x: f'{num(x)}%', [sum(sh), sum(sh[:n - 1])]))
    return {'stem': stem + ' Explain what the result suggests about the market structure and how firms are likely to compete.',
            'answer': f'CR{n} = {cr}%. ' + ('A high concentration ratio suggests oligopoly: interdependent firms likely to use non-price competition and possibly tacit collusion.' if cr >= 60 else 'Moderate concentration: a fairly competitive market with some larger firms; price competition is likely.'),
            'key': f'CR{n} = {cr}% [1]; interpretation [1]; behaviour (interdependence, non-price competition/collusion) [1].', 'type': 'numerical'}


@t6_4.add('C3', (3, 4, 5), 'numerical')
def t6_4_kink(r, D):
    p = r.choice([10, 20, 40, 50])
    q = r.choice([1000, 2000, 5000])
    up = r.choice([0.1, 0.05])
    fall_up = r.choice([0.3, 0.4, 0.25])
    rise_dn = r.choice([0.02, 0.03, 0.04])
    p_up, p_dn = p * (1 + up), p * (1 - up)
    q_up, q_dn = q * (1 - fall_up), q * (1 + rise_dn)
    tr0, tr_up, tr_dn = p * q, p_up * q_up, p_dn * q_dn
    ped_up, ped_dn = fall_up / up, rise_dn / up
    return {'stem': f'An oligopolist sells {q:,} units at ${p}. Market research suggests that if it raises its price by {pct(up * 100, 0)}, sales fall to {num(q_up):s} because rivals keep prices unchanged; if it cuts price by {pct(up * 100, 0)}, sales rise only to {num(q_dn)} because rivals match the cut. Calculate total revenue in each case and the price elasticity of demand for each change, and explain what this implies for the firm’s pricing.',
            'answer': f'TR now {money(tr0)}; after rise {money(round(tr_up, 2))}; after cut {money(round(tr_dn, 2))}. PED (rise) = {num(ped_up, 2)} (elastic); PED (cut) = {num(ped_dn, 2)} (inelastic). Both changes reduce revenue, so the firm keeps its price: price rigidity (kinked demand curve).',
            'key': f'TR = P × Q for each case [2]; PED = %ΔQ/%ΔP: {pct(fall_up * 100, 0)}/{pct(up * 100, 0)} and {pct(rise_dn * 100, 0)}/{pct(up * 100, 0)} [2]; conclusion: price stable at the kink [1].', 'type': 'multi_step'}


t6_5 = topic('Contestable markets and price discrimination', 'contestable markets', 'price discrimination')
t6_5.fixed('C1', (1, 2, 3), [
    ('A perfectly contestable market is one in which', 'there are no sunk costs and entry and exit are free, so the threat of entry disciplines incumbents',
     'Contestability depends on entry/exit costs, not the number of firms.', ['there is only one firm', 'the government sets prices', 'products are always homogeneous']),
    ('Hit-and-run entry is possible when', 'sunk costs are low, so a firm can enter, take profits and leave without loss',
     'Low sunk costs allow quick entry and exit, limiting incumbents’ profits.', ['barriers to entry are high', 'firms have patents', 'the market is a natural monopoly']),
    ('Third-degree price discrimination requires that', 'the firm can separate markets with different price elasticities and prevent resale',
     'Conditions: price-setting power, separable markets with different PED, no arbitrage.', ['all consumers have the same elasticity', 'the product can easily be resold', 'the firm is a price taker']),
    ('Under price discrimination, the higher price is charged in the market where demand is', 'less price elastic', 'MR = MC in each market; inelastic market bears a higher mark-up.',
     ['more price elastic', 'perfectly elastic', 'falling fastest']),
    ('Charging each consumer the maximum price they are willing to pay is', 'first-degree (perfect) price discrimination', 'All consumer surplus is captured by the producer.',
     ['second-degree price discrimination', 'limit pricing', 'cost-plus pricing']),
])
t6_5.fixed('C2', (2, 3, 4), [
    ('Explain how contestable market theory suggests that a market with only one firm may still behave competitively.', 'If entry and exit are costless, any supernormal profit would attract hit-and-run entrants, so the incumbent keeps price close to average cost (limit pricing) and is efficient.', '1 mark: threat of entry; 1 mark: no sunk costs; 1 mark: normal profit/efficient outcome [3]'),
    ('Explain how price discrimination may benefit some consumers.', 'Consumers in the elastic market (e.g. students, off-peak travellers) pay lower prices than under a single price, and the extra revenue may allow a service to run that would otherwise be unprofitable.', '1 mark: lower price for elastic group; 1 mark: service viable/higher output [2]'),
    ('With the aid of a diagram, explain third-degree price discrimination between two markets.', 'Diagram: two markets side by side with a common MC. In each market output where MR = MC; inelastic market (steeper AR) has higher price P1; elastic market (flatter AR) has lower price P2; total profit exceeds that from a single price.', '1 mark: MR = MC in each market; 1 mark: higher price in inelastic market; 1 mark: higher profit [3]'),
])
items(t6_5, 'C2', (2, 3), [
    ('{firm}, an airline in {country}, charges business travellers much more than leisure travellers for seats on the same flight. Explain why this is possible and profitable.',
     'The two groups have different PED (business demand is inelastic, leisure elastic); the airline can separate them by booking time or flexibility rules and tickets cannot be resold, so MR = MC in each market gives higher profit.',
     '1 mark: different PED; 1 mark: separation/no resale; 1 mark: higher profit [3]'),
    ('A railway in {country} charges lower fares for off-peak journeys. Explain whether this is price discrimination.',
     'Yes, if the cost of carrying a passenger is the same at both times: different prices for the same service reflect different PED (commuters inelastic). If off-peak costs are genuinely lower, it is partly cost-based pricing.',
     '1 mark: definition; 1 mark: application/cost caveat [2]'),
])


@t6_5.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t6_5_pd(r, D):
    c = r.choice([10, 20, 30])
    b1, b2 = r.choice([1, 2]), r.choice([0.5, 1])
    q1, q2 = r.choice([10, 20, 30]), r.choice([20, 30, 40])
    a1, a2 = c + 2 * b1 * q1, c + 2 * b2 * q2
    p1, p2 = a1 - b1 * q1, a2 - b2 * q2
    if p1 == p2:
        a2 += 4 * b2; q2 += 2; p2 = a2 - b2 * q2
    e1, e2 = p1 / (p1 - c), p2 / (p2 - c)
    pr = (p1 - c) * q1 + (p2 - c) * q2
    name = r.choice([('adults', 'students'), ('business travellers', 'tourists'), ('peak users', 'off-peak users'), ('domestic buyers', 'export buyers')])
    stem = (f'A firm with constant marginal cost of ${c} sells in two separate markets. {name[0].capitalize()}: P = {num(a1)} − {num(b1)}Q (MR = {num(a1)} − {num(2 * b1)}Q). '
            f'{name[1].capitalize()}: P = {num(a2)} − {num(b2)}Q (MR = {num(a2)} − {num(2 * b2)}Q).')
    if D <= 2:
        return cq(r, D, stem + f' Calculate the profit-maximising price for {name[0]}.', f'${num(p1)}', f'MR = MC: {num(a1)} − {num(2 * b1)}Q = {c} → Q = {q1}; P = {num(a1)} − {num(b1)}×{q1} = {num(p1)}.',
                  dis_num(r, p1, lambda x: f'${num(x)}', [p2, c, a1]))
    stem += ' Calculate the profit-maximising output and price in each market and the total contribution to profit. Show which market has the less elastic demand at these prices.'
    ans = (f'{name[0]}: Q = {q1}, P = ${num(p1)}; {name[1]}: Q = {q2}, P = ${num(p2)}; contribution = {money(pr)}. PED = P/(P − MC): {num(e1, 2)} vs {num(e2, 2)}, so '
           f'{name[0] if e1 < e2 else name[1]} have the less elastic demand and pay the higher price.')
    key = f'MR = MC in each market [2]; prices from AR [2]; profit = Σ(P − MC)Q = {money(pr)} [1]; |PED| = P/(P − MC) at MR = MC, compared [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


def _mkt_c4(r, D):
    d = ctx(r)
    shares = sorted(r.sample(range(8, 35), 4), reverse=True)
    cr4 = sum(shares)
    p = r.choice([2.5, 3, 4, 5])
    intro = (f'Extract: The {d["ind"]} market in {d["country"]} is dominated by four firms with shares of {", ".join(str(s) + "%" for s in shares)}. '
             f'Prices have remained at about ${p} per unit for three years despite rising input costs. Regulators suspect that the firms have colluded, while the firms argue that the market is contestable.')
    parts = [
        lambda r: ('Calculate the four-firm concentration ratio and state the market structure it suggests.', f'{cr4}%; ' + ('oligopoly' if cr4 >= 50 else 'fairly competitive, with some large firms'), '[2]'),
        lambda r: ('Using the kinked demand curve model, explain why prices may have stayed the same.', 'Rivals match cuts but not rises; MR has a discontinuity, so higher MC within the gap leaves price unchanged.', '[3]'),
        lambda r: ('Explain two pieces of evidence that would suggest collusion rather than competition.', 'Identical price changes at the same time, stable market shares, high profits, communication between firms, prices above cost.', '[2]'),
        lambda r: ('Discuss whether the market is likely to be contestable.', 'Depends on sunk costs, brand loyalty, economies of scale and licensing; high sunk costs or regulation reduce contestability; evidence of entry/exit.', '[4]'),
        lambda r: ('Assess whether consumers would be better off if the four firms were replaced by a perfectly competitive industry.', 'Lower price and P = MC; but loss of economies of scale and R&D (dynamic efficiency); depends on MES relative to market size.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t6_1, t6_2, t6_3, t6_4, t6_5], 'C4', (3, 4, 5), 'case', _mkt_c4)
essays(t6_1, [
    ('perfect competition is an unrealistic model and of little use to economists',
     'With the aid of a diagram, explain the long-run equilibrium of a firm in perfect competition.',
     'Assumptions rarely hold, yet the model is a benchmark for efficiency; some markets (agriculture, foreign exchange) come close.',
     'Useful benchmark for policy; predicts effects of entry and exit; but ignores economies of scale and innovation.'),
], ['Farmers in {country} sell identical crops at prices set on a national commodity exchange.'])
essays(t6_2, [
    ('monopoly is always against the public interest',
     'With the aid of a diagram, explain how a profit-maximising monopolist determines its price and output.',
     'Higher prices, lower output, deadweight loss, X-inefficiency, consumer surplus transferred to producer.',
     'Natural monopoly economies of scale; dynamic efficiency from R&D; regulation; contestability; price discrimination may raise output.'),
    ('natural monopolies should be owned by the state',
     'Explain what is meant by a natural monopoly and why it arises.',
     'One firm has lowest costs; state ownership can set P = MC or P = AC and avoid abuse.',
     'Regulation of private firms (price caps) may be more efficient; government failure, X-inefficiency, political interference; investment funding.'),
], ['{firm} is the only supplier of {good} in {country}.', 'Water and electricity networks in {country} are each run by a single company.'])
essays(t6_3, [
    ('monopolistic competition gives consumers a better outcome than perfect competition',
     'With the aid of a diagram, explain the short-run and long-run equilibrium of a firm in monopolistic competition.',
     'Variety and choice; product innovation; normal profit in LR.',
     'Excess capacity, P > MC, wasteful advertising; less efficient than PC; but consumers value variety.'),
], ['There are hundreds of independent cafés and restaurants in {city}.'])
essays(t6_4, [
    ('oligopolies always act against the interests of consumers',
     'Explain, using game theory, why firms in an oligopoly may collude.',
     'Collusion raises prices and restricts output; tacit collusion and price leadership; non-price competition costs.',
     'Price wars can benefit consumers; innovation and economies of scale; competition authorities; cartels unstable (prisoners’ dilemma).'),
    ('game theory is more useful than the kinked demand curve model in explaining the behaviour of oligopolies',
     'With the aid of a diagram, explain the kinked demand curve model.',
     'Game theory explains collusion, cheating and strategy; kinked demand explains rigidity but not how price is set.',
     'Both are simplifications; real behaviour depends on repeated games, trust, regulation and number of firms.'),
], ['Four supermarket chains control most grocery sales in {country}.', 'Two airlines dominate flights between {city} and the capital of {country2}.'])
essays(t6_5, [
    ('price discrimination always benefits producers at the expense of consumers',
     'Explain the conditions necessary for a firm to practise price discrimination.',
     'Producers gain consumer surplus; inelastic group pays more.',
     'Elastic groups pay less; output may rise; services may become viable; cross-subsidisation; first-degree removes all surplus.'),
    ('the number of firms in a market is less important than how contestable the market is',
     'Explain what is meant by a contestable market.',
     'Threat of entry disciplines firms regardless of number; low sunk costs mean efficient behaviour.',
     'Perfect contestability is rare; sunk costs, brand loyalty and incumbents’ strategic behaviour; concentration still matters for competition policy.'),
], ['{firm} charges different prices for the same {good} in {country} and {country2}.', 'Low-cost airlines have entered several routes from {city} in recent years.'])
CHAPTERS[6] = [t6_1, t6_2, t6_3, t6_4, t6_5]

# ============================================================================ 7 Growth and survival of firms
CHAINS = [
    ['cocoa farming', 'chocolate manufacturing', 'confectionery retailing'], ['iron ore mining', 'steel making', 'car manufacturing'],
    ['oil extraction', 'oil refining', 'petrol station retailing'], ['cotton farming', 'textile manufacturing', 'clothing retailing'],
    ['forestry', 'paper making', 'newspaper publishing'], ['film production', 'film distribution', 'cinema chains'],
    ['coffee growing', 'coffee roasting', 'coffee shop chains'], ['wheat farming', 'flour milling', 'bakery chains'],
    ['microchip design', 'smartphone assembly', 'phone retailing'], ['dairy farming', 'cheese making', 'supermarkets'],
]
UNRELATED = ['hotels', 'insurance', 'football clubs', 'cosmetics', 'property development', 'airlines', 'software', 'pet food']
t7_1 = topic('Internal growth and integration', 'internal growth and integration', 'horizontal, vertical and conglomerate', 'integration')
t7_1.fixed('C1', (1, 2, 3), [
    ('Internal (organic) growth occurs when a firm', 'expands by investing in new capacity and increasing its own sales', 'Organic growth: reinvested profit, new plants, new products, new markets.',
     ['merges with another firm', 'is taken over', 'forms a cartel']),
    ('A merger between two firms at the same stage of production in the same industry is', 'horizontal integration', 'Same industry, same stage: e.g. two banks.',
     ['vertical integration', 'conglomerate integration', 'backward integration']),
    ('A car manufacturer buying a tyre producer is an example of', 'backward vertical integration', 'Moving towards the supplier of inputs (earlier stage).',
     ['forward vertical integration', 'horizontal integration', 'conglomerate integration']),
    ('A conglomerate merger is one between firms', 'in unrelated industries', 'Diversification reduces risk.', ['at the same stage of production', 'at successive stages of production', 'in the same market']),
    ('A main motive for forward vertical integration is to', 'secure retail outlets and control how the product reaches consumers', 'Forward: towards the customer; secure outlets, capture retail margin.',
     ['secure supplies of raw materials', 'reduce risk by diversification', 'gain bulk-buying discounts on inputs']),
])
t7_1.fixed('C2', (2, 3, 4), [
    ('Explain two advantages of internal growth compared with growth by merger.', 'Lower risk and cost (no premium paid for another firm); no culture clash; growth can be controlled; avoids competition authority investigation.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why a firm might choose conglomerate integration.', 'To spread risk across unrelated markets, use spare managerial or financial capacity, or grow when its own market is saturated or tightly regulated.', '1 mark: diversification/risk; 1 mark: second reason [2]'),
    ('Distinguish between backward and forward vertical integration.', 'Backward: a firm takes over a supplier at an earlier stage of production; forward: it takes over a firm at a later stage, closer to the consumer.', '1 mark each [2]'),
])


@t7_1.add('C3', (1, 2, 3), 'mcq')
def t7_1_classify(r, D):
    ch = r.choice(CHAINS)
    i = r.randint(0, 2)
    kind = r.choice(['horizontal', 'backward', 'forward', 'conglomerate'])
    if kind == 'backward' and i == 0:
        kind = 'forward'
    if kind == 'forward' and i == 2:
        kind = 'backward'
    f1, f2 = r.sample(FIRMS, 2)
    target = {'horizontal': ch[i], 'backward': ch[i - 1] if i else ch[0], 'forward': ch[i + 1] if i < 2 else ch[2], 'conglomerate': r.choice(UNRELATED)}[kind]
    ans = {'horizontal': 'Horizontal integration', 'backward': 'Backward vertical integration', 'forward': 'Forward vertical integration', 'conglomerate': 'Conglomerate integration'}[kind]
    opts, a = mcq(r, ans, [x for x in ('Horizontal integration', 'Backward vertical integration', 'Forward vertical integration', 'Conglomerate integration') if x != ans])
    return {'stem': f'{f1}, a firm in {ch[i]}, takes over {f2}, a firm in {target}. Which type of integration is this?', 'options': opts, 'answer': a,
            'key': f'Production chain: {" → ".join(ch)}. {ans}.'}


@t7_1.add('C3', (2, 3, 4, 5), 'explain')
def t7_1_analyse(r, D):
    ch = r.choice(CHAINS)
    f1, f2 = r.sample(FIRMS, 2)
    kind = r.choice(['backward', 'forward', 'horizontal'])
    if kind == 'backward':
        s = f'{f1}, {art(ch[1])} business, plans to buy {f2}, its main supplier in {ch[0]}.'
        a = 'Backward vertical integration. Benefits: secure supply and quality of inputs, capture the supplier’s profit margin, better coordination. Risks: less flexibility, management of an unfamiliar activity, rivals’ access to supply may raise competition concerns.'
    elif kind == 'forward':
        s = f'{f1}, {art(ch[1])} business, plans to buy {f2}, a chain in {ch[2]}.'
        a = 'Forward vertical integration. Benefits: secure outlets, control of branding and pricing, capture retail margin, information on consumers. Risks: retail expertise needed, rival suppliers may lose access, high cost.'
    else:
        s = f'{f1} and {f2}, two firms in {ch[1]}, plan to merge.'
        a = 'Horizontal integration. Benefits: economies of scale, larger market share and pricing power, removal of duplication. Risks: diseconomies, culture clash, competition authority investigation, higher prices for consumers.'
    return {'stem': f'{s} Identify the type of integration and analyse two benefits and one risk for the firm.', 'answer': a,
            'key': '1 mark: type; 2 marks: two benefits analysed; 1 mark: risk [4]'}


t7_2 = topic('Mergers and acquisitions', 'mergers and acquisitions', 'motives and consequences for consumers and firms')
t7_2.fixed('C1', (1, 2, 3), [
    ('An acquisition (takeover) differs from a merger because', 'one firm buys a controlling share in another, rather than two firms agreeing to combine', 'Takeovers may be hostile; mergers are agreed combinations.',
     ['it always involves firms in different countries', 'it does not change ownership', 'it is illegal']),
    ('Which is most likely to be a motive for a horizontal merger?', 'Gaining economies of scale and greater market power', 'Same stage: scale economies, market share, removing a competitor.',
     ['Diversifying into unrelated markets', 'Securing raw material supplies', 'Reducing market share']),
    ('Synergy in a merger means that', 'the combined firm is worth more than the two firms separately', '“2 + 2 = 5”: cost savings or revenue gains from combination.',
     ['the firms keep separate managers', 'the firms are in unrelated industries', 'prices must fall']),
    ('The Herfindahl–Hirschman Index (HHI) is calculated by', 'summing the squares of the market shares of all firms in the market', 'HHI = Σ sᵢ²; range up to 10,000.',
     ['adding the shares of the four largest firms', 'dividing the largest share by the smallest', 'multiplying the number of firms by the average share']),
])
t7_2.fixed('C2', (2, 3, 4), [
    ('Explain two reasons why many mergers fail to achieve the expected benefits.', 'Culture clashes between workforces and managers; diseconomies of scale; overpaying for the target; synergies overestimated; loss of key staff and customers.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain how a merger might benefit consumers.', 'Cost savings from economies of scale passed on as lower prices; more funds for R&D and better products; a stronger competitor against a dominant firm.', '1 mark each point developed [2]'),
    ('Explain why managers may pursue mergers even when shareholders do not gain.', 'Managers may gain higher salaries, status and power from running a larger firm (principal–agent problem), so they pursue growth rather than profit.', '1 mark: managerial motives; 1 mark: divorce of ownership and control [2]'),
])


@t7_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t7_2_hhi(r, D):
    for _ in range(50):
        sh = sorted(r.sample(range(4, 36), 5), reverse=True)
        if sum(sh) < 100:
            break
    rest = 100 - sum(sh)
    nsmall = r.choice([5, 10, 20]) if rest else 0
    small = rest / nsmall if nsmall else 0
    hhi = sum(s * s for s in sh) + nsmall * small * small
    i, j = sorted(r.sample(range(5), 2))
    new = hhi + 2 * sh[i] * sh[j]
    cr4 = sum(sh[:4])
    after = sorted(sh[:i] + sh[i + 1:j] + sh[j + 1:] + [sh[i] + sh[j]], reverse=True)
    cr4b = sum(after[:4])
    ind = r.choice(INDUSTRIES)
    names = r.sample(FIRMS, 5)
    desc = ', '.join(f'{n} {s}%' for n, s in zip(names, sh)) + (f', and {nsmall} small firms with {num(small, 2)}% each' if nsmall else '')
    stem = f'Market shares in the {ind} industry: {desc}. {names[i]} proposes to merge with {names[j]}.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the four-firm concentration ratio before the merger.', f'{cr4}%', f'CR4 = {" + ".join(map(str, sh[:4]))} = {cr4}%.', dis_num(r, cr4, lambda x: f'{num(x)}%', [sum(sh), cr4b]))
    stem += ' Calculate the HHI before and after the merger and the four-firm concentration ratio after the merger. Competition authorities investigate mergers that raise the HHI by more than 200 in a market with an HHI above 2,500. State, with a reason, whether this merger is likely to be investigated.'
    inv = new > 2500 and new - hhi > 200
    ans = f'HHI before = {num(hhi, 1)}; after = {num(new, 1)} (rise of {2 * sh[i] * sh[j]}); CR4 after = {cr4b}%. ' + ('Likely to be investigated: post-merger HHI exceeds 2,500 and the rise exceeds 200.' if inv else 'Probably not investigated on these thresholds, because ' + ('the post-merger HHI is below 2,500.' if new <= 2500 else 'the rise is below 200.'))
    key = f'HHI = Σs² = {num(hhi, 1)} [1]; merged share {sh[i] + sh[j]}%, so rise = 2 × {sh[i]} × {sh[j]} = {2 * sh[i] * sh[j]} [1]; new HHI {num(new, 1)} [1]; CR4 after {cr4b}% [1]; threshold applied [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t7_3 = topic('Why small firms survive', 'small firms survive', 'small firms')
t7_3.fixed('C1', (1, 2, 3), [
    ('Which is a reason why small firms survive alongside large firms?', 'They serve niche markets that are too small for large firms', 'Niche markets, personal service, flexibility, small MES, low barriers.',
     ['They always have lower average costs than large firms', 'They benefit from greater economies of scale', 'They can borrow more cheaply']),
    ('Small firms are most common in industries where', 'the minimum efficient scale is small relative to market size', 'Economies of scale are quickly exhausted, so small firms are not at a cost disadvantage.',
     ['economies of scale are very large', 'sunk costs are very high', 'there is a natural monopoly']),
    ('Which is a typical disadvantage faced by small firms?', 'Higher cost of finance and less access to credit', 'Banks see small firms as riskier; limited collateral.',
     ['Diseconomies of scale', 'Too many layers of management', 'Lack of flexibility']),
    ('Franchising allows small firms to', 'operate independently while using an established brand and support of a larger firm', 'Franchisee gains brand, training and bulk-buying; franchisor gains fees.',
     ['avoid paying for the brand', 'become a monopoly', 'avoid all competition']),
])
t7_3.fixed('C2', (2, 3, 4), [
    ('Explain two reasons why small firms survive in an economy dominated by large firms.', 'Niche or local markets; personal service and flexibility; small MES; government support; subcontracting to large firms; owners willing to accept lower returns.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why large firms sometimes subcontract work to small firms.', 'To gain flexibility, specialist skills and lower costs without expanding their own workforce or capacity; risk is shifted to the subcontractor.', '1 mark: flexibility/cost; 1 mark: specialist skills or risk [2]'),
])


@t7_3.add('C3', (2, 3, 4, 5), 'case')
def t7_3_data(r, D):
    d = ctx(r)
    pf = r.choice([95, 96, 97, 98, 99])
    pe = r.choice([40, 45, 50, 55, 60])
    po = r.choice([30, 35, 38, 42])
    nf = r.choice([200, 400, 600, 800])
    small_n = round(nf * pf / 10)
    stem = f'In {d["country"]}, small firms make up {pf}% of the {nf * 10:,} businesses, employ {pe}% of workers and produce {po}% of output. '
    lp = (po / pe) / ((100 - po) / (100 - pe))
    parts = [
        lambda r: ('Calculate the number of small firms.', f'{small_n:,}', f'{pf}% × {nf * 10:,} = {small_n:,} [1]'),
        lambda r: ('Compare output per worker in small and large firms, using an index.', f'Small-firm output per worker is {num(lp, 2)} times that of large firms.', f'({po}/{pe}) ÷ ({100 - po}/{100 - pe}) = {num(lp, 2)} [2]'),
        lambda r: ('Explain why small firms may have lower labour productivity than large firms.', 'Less capital per worker, fewer economies of scale, less specialisation and less access to finance and technology.', '[2]'),
        lambda r: ('Explain two reasons why small firms continue to survive despite this.', 'Niche markets, flexibility and personal service, small MES, franchising/subcontracting, government support.', '[4]'),
        lambda r: ('Assess whether the government should give special support to small firms.', 'For: job creation, competition, innovation, market failure in finance. Against: cost, deadweight (would grow anyway), may protect inefficient firms. Judgement.', '[4]'),
    ]
    return compose(r, stem, parts, k=(2, 3, 4), type_='case')


def _growth_c4(r, D):
    d = ctx(r)
    s1, s2 = r.choice([18, 22, 25, 28]), r.choice([12, 15, 20])
    intro = f'Extract: {d["firm"]} ({s1}% market share) has agreed to take over {d["firm2"]} ({s2}% share), a rival in the {d["ind"]} industry of {d["country"]}. The firms claim savings of 8% on average costs.'
    parts = [
        lambda r: ('Identify the type of integration and calculate the combined market share.', f'Horizontal; {s1 + s2}%', '[2]'),
        lambda r: ('Calculate the rise in the HHI caused by the merger.', f'2 × {s1} × {s2} = {2 * s1 * s2}', '[2]'),
        lambda r: ('Explain two motives for the takeover.', 'Economies of scale, market power, removing a rival, synergies, managerial empire-building.', '[4]'),
        lambda r: ('Discuss whether the takeover will benefit consumers.', 'Cost savings may lower prices; but higher market power may raise prices and reduce choice; depends on contestability, regulation and whether savings are passed on.', '[4]'),
        lambda r: ('Explain why the expected cost savings might not happen.', 'Culture clash, diseconomies of scale, integration costs, loss of staff.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t7_1, t7_2, t7_3], 'C4', (3, 4, 5), 'case', _growth_c4)
essays(t7_1, [
    ('vertical integration benefits firms more than horizontal integration',
     'Explain the difference between horizontal, vertical and conglomerate integration.',
     'Vertical integration secures supply and outlets and captures margins; horizontal gives scale economies and market power.',
     'Depends on industry and motives; vertical can reduce flexibility; horizontal may face competition policy; outcomes depend on management.'),
    ('internal growth is better than external growth for a firm',
     'Explain the ways in which a firm can grow internally.',
     'Internal growth is lower risk, retains culture and control.',
     'Slower; external growth is quicker, gains market share, brands and know-how; depends on finance and market conditions.'),
], ['{firm}, {a_ind} business, wants to double in size within five years.'])
essays(t7_2, [
    ('mergers between large firms should be prevented because they harm consumers',
     'Explain the motives for mergers and acquisitions.',
     'Higher concentration, market power, higher prices, less choice.',
     'Economies of scale, synergies, dynamic efficiency, international competitiveness; case-by-case assessment by competition authorities.'),
], ['Two of the largest {ind} firms in {country} have announced a merger.'])
essays(t7_3, [
    ('small firms will eventually disappear as large firms gain economies of scale',
     'Explain why small firms are able to survive in many industries.',
     'Large firms have cost advantages and market power.',
     'Niche markets, small MES, flexibility, personal service, franchising, technology lowering entry costs, government support.'),
], ['In {country}, most businesses employ fewer than ten people.'])
CHAPTERS[7] = [t7_1, t7_2, t7_3]

# ============================================================================ 8 Objectives of firms
t8_1 = topic('Profit maximisation', 'profit maximisation', 'mc = mr rule')
t8_1.fixed('C1', (1, 2, 3), [
    ('A firm maximises profit at the output where', 'marginal cost equals marginal revenue and MC is rising', 'MC = MR (with MC cutting MR from below).',
     ['average cost is at a minimum', 'total revenue is at a maximum', 'average revenue equals average cost']),
    ('If marginal revenue is greater than marginal cost, a profit-maximising firm should', 'increase output', 'Each extra unit adds more to revenue than to cost.',
     ['reduce output', 'keep output unchanged', 'shut down']),
    ('At an output where MC = MR, the firm’s total profit', 'is at a maximum (or loss at a minimum)', 'MC = MR maximises TR − TC; profit may still be negative.',
     ['is always positive', 'is zero', 'is falling']),
    ('A firm’s marginal revenue from the 10th unit is $25 and marginal cost is $30. To raise profit it should', 'produce fewer units', 'MC > MR: last unit lowers profit.',
     ['produce more units', 'raise output to 11', 'keep producing 10 units']),
])
t8_1.fixed('C2', (2, 3, 4), [
    ('Explain why profit is maximised where marginal cost equals marginal revenue.', 'If MR > MC, producing one more unit adds to profit, so output should rise; if MC > MR, the last unit reduces profit, so output should fall. Profit stops increasing only where MC = MR.', '1 mark: MR > MC → expand; 1 mark: MC > MR → contract; 1 mark: MC = MR maximum [3]'),
    ('Explain why a firm might find it difficult to apply the MC = MR rule in practice.', 'Firms rarely know their marginal cost and marginal revenue precisely; demand is uncertain and rivals react; firms often use cost-plus pricing instead.', '1 mark each reason [2]'),
])


@t8_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t8_1_table(r, D):
    for _ in range(40):
        a = r.choice([60, 70, 80, 90, 100])
        b = r.choice([5, 6, 8])
        F, mc, tc, atc = _cost_sched(r)
        qs = list(range(1, 8))
        tr = [(a - b * q) * q for q in qs]
        prof = [tr[i] - tc[i] for i in range(7)]
        best = max(range(7), key=lambda i: prof[i])
        if sorted(prof)[-1] != sorted(prof)[-2] and 1 <= best <= 5:
            break
    mr = [tr[0]] + [tr[i] - tr[i - 1] for i in range(1, 7)]
    tab = table(['Output', 'Total revenue ($)', 'Total cost ($)'], list(zip(qs, tr, tc[:7])))
    qb = best + 1
    if D <= 2:
        opts, a_ = mcq(r, f'{qb} units', [f'{q} units' for q in qs if q != qb])
        return {'stem': f'{tab}. At which output does the firm maximise profit?', 'options': opts, 'answer': a_,
                'key': f'Profit = TR − TC: {", ".join(map(str, prof))}; maximum ${prof[best]} at {qb} units.'}
    stem = f'A firm’s revenue and costs are shown. {tab}. (a) Calculate marginal revenue and marginal cost for each unit. (b) Use the MC = MR rule to identify the profit-maximising output and calculate the profit.'
    ans = f'(a) MR: {", ".join(map(str, mr))}; MC: {", ".join(map(str, mc[:7]))} (b) {qb} units: last unit with MR ≥ MC; profit = {money(prof[best])}.'
    key = '(a) MR = ΔTR, MC = ΔTC [2]; (b) produce while MR ≥ MC [1]; profit = TR − TC at that output [1].'
    if D >= 4:
        stem += ' (c) Explain why producing one more unit would reduce profit.'
        ans += f' (c) Unit {qb + 1} has MR ${mr[qb]} but MC ${mc[qb]}, so it adds more to cost than to revenue.'
        key += ' (c) MC > MR for the next unit [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t8_2 = topic('Alternative objectives of firms', 'alternative objectives', 'survival, sales and revenue maximisation, satisficing', 'sales maximisation')
t8_2.fixed('C1', (1, 2, 3), [
    ('A firm aiming to maximise total revenue produces where', 'marginal revenue is zero', 'TR is maximised where MR = 0.', ['MC = MR', 'AR = AC', 'MC is at a minimum']),
    ('Sales maximisation, subject to earning normal profit, occurs where', 'average revenue equals average cost', 'Highest output consistent with no loss: AR = AC.', ['MR = 0', 'MC = MR', 'MC = AC']),
    ('Satisficing means that a firm', 'aims for a satisfactory level of profit while meeting other stakeholders’ goals', 'Simon/Cyert–March: managers satisfy several groups rather than maximise one variable.',
     ['always maximises profit', 'maximises the number of units sold', 'aims to make a loss']),
    ('A new firm in a recession is most likely to have the short-term objective of', 'survival', 'Covering costs and staying in business takes priority.',
     ['revenue maximisation regardless of costs', 'maximising dividends', 'reducing market share']),
    ('Compared with a profit-maximising firm with the same costs and demand, a revenue-maximising firm will usually', 'produce more output and charge a lower price', 'MR = 0 occurs at a higher output than MR = MC (MC > 0).',
     ['produce less output and charge a higher price', 'produce the same output', 'make more profit']),
])
t8_2.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, compare the price and output of a firm that maximises profit, revenue and sales.', 'Diagram: AR and MR downward sloping, MC and AC. Profit max at Q1 where MC = MR; revenue max at Q2 where MR = 0 (higher output, lower price); sales max at Q3 where AR = AC (highest output, lowest price, normal profit only). So Q1 < Q2 < Q3 and P1 > P2 > P3 (typically).', '1 mark each output identified, 1 mark ordering of prices [4]'),
    ('Explain why a firm might choose to maximise revenue rather than profit.', 'Managers’ pay or status may be linked to sales; a larger market share may deter entry and give future economies of scale; profit is hard to calculate.', '1 mark each reason explained [2]'),
])


@t8_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t8_2_obj(r, D):
    for _ in range(50):
        b = r.choice([1, 2])
        q1, q2 = sorted(r.sample(range(4, 40, 2), 2))
        if q2 - q1 < 6:
            continue
        c = r.choice([4, 6, 8, 10, 12])
        F = b * q1 * q2
        a = c + b * (q1 + q2)
        if a % (2 * b) == 0:
            break
    qp = (q1 + q2) // 2
    qr = a // (2 * b)
    pp, pr, ps = a - b * qp, a - b * qr, a - b * q2
    profit = (pp - c) * qp - F
    stem = f'A firm faces demand P = {a} − {b}Q (MR = {a} − {2 * b}Q). Its total cost is TC = {F} + {c}Q, so MC = {c} and AC = {F}/Q + {c}.'
    if D <= 2:
        which = r.choice(['profit', 'revenue'])
        v = qp if which == 'profit' else qr
        return cq(r, D, stem + f' Calculate the output that maximises {which}.', f'{v} units', (f'MR = MC: {a} − {2 * b}Q = {c} → Q = {qp}.' if which == 'profit' else f'MR = 0: Q = {a}/{2 * b} = {qr}.'),
                  dis_num(r, v, lambda x: f'{num(x)} units', [qp if which == 'revenue' else qr, q2]))
    stem += ' Calculate the output and price if the firm aims to (a) maximise profit, (b) maximise revenue, (c) maximise sales subject to earning at least normal profit.'
    ans = f'(a) Q = {qp}, P = ${pp} (profit {money(profit)}) (b) Q = {qr}, P = ${pr} (c) Q = {q2}, P = ${ps}.'
    key = (f'(a) MR = MC: {a} − {2 * b}Q = {c} → Q = {qp}, P = {pp} [2]; (b) MR = 0 → Q = {qr}, P = {pr} [2]; '
           f'(c) AR = AC: {a} − {b}Q = {F}/Q + {c} → {b}Q² − {a - c}Q + {F} = 0 → Q = {q2} (larger root), P = {ps} [2].')
    if D >= 5:
        stem += ' (d) Explain which objective is best for consumers.'
        ans += ' (d) Sales maximisation gives the lowest price and highest output, but only normal profit, which may limit investment.'
        key += ' (d) evaluative comment [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t8_3 = topic('Principal-agent problem', 'principal-agent problem', 'divorce of ownership and control')
t8_3.fixed('C1', (1, 2, 3), [
    ('The principal–agent problem in a public limited company arises because', 'managers (agents) may pursue their own objectives rather than those of shareholders (principals)',
     'Divorce of ownership and control plus asymmetric information.', ['shareholders manage the firm directly', 'workers own the company', 'the government sets prices']),
    ('Which measure is most likely to reduce the principal–agent problem?', 'Linking managers’ pay to the firm’s share price or profit', 'Aligning incentives, e.g. share options, profit-related bonuses.',
     ['Paying managers a fixed salary regardless of performance', 'Hiding company accounts from shareholders', 'Reducing the number of shareholders’ meetings']),
    ('The divorce of ownership and control refers to', 'the separation of the owners of a company from the managers who run it', 'Typical of large plcs with dispersed shareholders.',
     ['the sale of a state-owned firm', 'a firm splitting into two', 'a merger of two firms']),
    ('In the principal–agent relationship between a patient and a doctor, the agent is', 'the doctor', 'The agent acts on behalf of the principal and has more information.',
     ['the patient', 'the government', 'the hospital’s shareholders']),
])
t8_3.fixed('C2', (2, 3, 4), [
    ('Explain why the divorce of ownership and control may lead firms not to maximise profits.', 'Shareholders cannot monitor managers closely (asymmetric information); managers may pursue sales growth, perks or a quiet life, satisficing on profit.', '1 mark: separation and information gap; 1 mark: alternative managerial goals [2]'),
    ('Explain one problem with linking managers’ bonuses to short-term profits.', 'Managers may cut investment, training or R&D to raise this year’s profit, harming long-run performance, or take excessive risks.', '1 mark: short-termism; 1 mark: consequence [2]'),
])


@t8_3.add('C3', (2, 3, 4, 5), 'numerical')
def t8_3_pa(r, D):
    qs = [10, 20, 30, 40, 50]
    for _ in range(40):
        rev = sorted(r.sample(range(200, 900, 20), 5))
        costs = [rev[i] - x for i, x in enumerate([r.choice([20, 40, 60]), r.choice([80, 100]), r.choice([130, 150]), r.choice([90, 110]), r.choice([10, 30, 50])])]
        prof = [a - b for a, b in zip(rev, costs)]
        if len(set(prof)) == 5:
            break
    bonus = r.choice([1, 2, 0.5])
    qp = qs[prof.index(max(prof))]
    qrv = qs[-1]
    lost = max(prof) - prof[-1]
    tab = table(['Output (000)', 'Revenue ($m)', 'Profit ($m)'], list(zip(qs, rev, prof)))
    return {'stem': f'{r.choice(FIRMS)} is a public limited company. {tab}. The chief executive receives a bonus of {num(bonus)}% of revenue. (a) Identify the output that shareholders would prefer and the output the chief executive is likely to choose. (b) Calculate the profit lost to shareholders if the chief executive chooses this output. (c) Explain how this illustrates the principal–agent problem.',
            'answer': f'(a) Shareholders: {qp} thousand (profit ${max(prof)}m); chief executive: {qrv} thousand (highest revenue). (b) ${lost}m. (c) The agent’s reward depends on revenue, not profit, so the manager’s choice differs from the owners’ objective; owners cannot easily monitor this.',
            'key': f'(a) profit max at {qp} [1]; revenue max at {qrv} [1]; (b) {max(prof)} − {prof[-1]} = {lost} [1]; (c) principal–agent explanation with incentive mismatch [2].', 'type': 'multi_step'}


def _obj_c4(r, D):
    d = ctx(r)
    pm, pr = r.choice([12, 15, 18]), r.choice([8, 9, 10])
    gm = r.choice([4, 5, 6])
    intro = f'Extract: Shareholders of {d["firm"]}, {art(d["ind"])} company in {d["country"]}, complain that its profit margin has fallen from {pm}% to {pr}% in three years while sales revenue grew by {gm * 5}%. Senior managers receive bonuses based on market share.'
    parts = [
        lambda r: ('Explain what is meant by the divorce of ownership and control.', 'Shareholders own the firm but salaried managers control day-to-day decisions.', '[2]'),
        lambda r: ('Explain why the managers may have pursued sales growth rather than profit.', 'Bonuses linked to market share; status and power from a larger firm; principal–agent problem.', '[2]'),
        lambda r: ('With the aid of a diagram, compare the outputs of a profit-maximising firm and a sales-maximising firm.', 'Profit max where MC = MR; sales max where AR = AC: higher output, lower price, normal profit only.', '[4]'),
        lambda r: ('Discuss how shareholders might ensure that managers act in their interests.', 'Share options, profit-related pay, non-executive directors, voting at AGMs, threat of takeover; limitations: short-termism, information gaps.', '[4]'),
        lambda r: (f'Calculate the percentage change in the profit margin.', f'{num((pr - pm) / pm * 100, 1)}%', f'({pr} − {pm})/{pm} × 100 [1]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t8_1, t8_2, t8_3], 'C4', (3, 4, 5), 'case', _obj_c4)
essays(t8_1, [
    ('all firms aim to maximise profits',
     'With the aid of a diagram, explain why profit is maximised where MC = MR.',
     'Profit maximisation explains entry/exit and pricing; shareholders demand it.',
     'Alternative objectives: survival, sales/revenue, satisficing, social enterprises, managers’ goals; lack of information about MC and MR.'),
], ['{firm} has announced that it will cut prices to increase its market share in {country}.'])
essays(t8_2, [
    ('a firm that maximises sales rather than profit will benefit consumers',
     'Explain the difference between profit maximisation, revenue maximisation and sales maximisation.',
     'Higher output and lower price under sales maximisation.',
     'Lower profit may reduce investment and innovation; predatory pricing may drive out rivals then raise prices; depends on market structure.'),
    ('satisficing is a more realistic objective for large firms than profit maximisation',
     'Explain what is meant by satisficing.',
     'Many stakeholders, imperfect information, divorce of ownership and control.',
     'Competitive pressure and takeover threats force profit focus; shareholder activism; depends on market power.'),
], ['A large {ind} firm in {country} reports that it aims to “balance the needs of customers, employees and shareholders”.'])
essays(t8_3, [
    ('the principal–agent problem means that large companies are run in the interests of managers rather than shareholders',
     'Explain the principal–agent problem with reference to a public limited company.',
     'Managers have information advantages and their own goals.',
     'Incentive schemes, takeover threats, institutional investors and corporate governance reduce the problem; managers’ goals may align with long-run profit.'),
], ['Shareholders of {firm} voted against the chief executive’s pay package this year.'])
CHAPTERS[8] = [t8_1, t8_2, t8_3]

# extra explain items for chapters 7-8
items(t7_3, 'C2', (2, 3, 4), [
    ('A family-run {good} business in {city} has survived for 40 years despite competition from {firm}, a national chain. Explain two reasons why it may have survived.',
     'It may serve a local niche with personal service and specialist knowledge, and be flexible in adapting to customer needs; low overheads and loyal customers help; the MES may be small.',
     '1 mark each reason, 1 mark each developed [4]'),
    ('Explain why the number of small {ind} firms in {country} has increased since online selling became widespread.',
     'Online platforms lower entry costs (no shop rent, cheap marketing), let small firms reach niche customers anywhere and buy services (delivery, payments) from large firms, so the MES falls.',
     '1 mark: lower entry/sunk costs; 1 mark: access to wider/niche markets [2]'),
    ('{firm} buys components from many small suppliers in {country} rather than making them itself. Explain why this helps small firms survive.',
     'Subcontracting gives small firms a steady market and lets them specialise in a narrow activity where economies of scale are small; the large firm gains flexibility.',
     '1 mark: guaranteed demand/specialisation; 1 mark: link to survival [2]'),
])
items(t8_1, 'C2', (2, 3, 4), [
    ('{firm} finds that the marginal revenue from its last batch of {good} was $8,000 while the marginal cost was $9,500. Explain what it should do to increase profit.',
     'MC > MR, so the last batch reduced profit by $1,500. It should cut output until MC = MR.', '1 mark: MC > MR reduces profit; 1 mark: reduce output to MC = MR [2]'),
    ('{firm}, a producer of {good}, sees its marginal cost rise because of higher energy prices while demand is unchanged. Explain the effect on its profit-maximising price and output.',
     'MC shifts upwards, so MC = MR occurs at a lower output; with a downward-sloping demand curve the price read from AR rises.', '1 mark: MC shifts up, new MC = MR at lower Q; 1 mark: higher price [2]'),
    ('Demand for {good} rises, shifting {firm}’s AR and MR curves to the right. Explain how a profit-maximising firm responds.',
     'MR rises at every output, so MC = MR occurs at a higher output; the firm expands output, and the price set from the new AR curve is likely to rise if MC is upward sloping.', '1 mark: MR shift → higher MC = MR output; 1 mark: price effect [2]'),
])
items(t8_2, 'C2', (2, 3, 4), [
    ('{firm}, a new entrant in the {ind} market of {country}, is setting a low price to win customers. Explain why it might aim for sales growth rather than profit in its first years.',
     'To build market share and brand awareness, gain economies of scale and deter rivals; profit can be raised later once customers are loyal.', '1 mark: market share/scale; 1 mark: long-run profit motive [2]'),
    ('Explain why {firm}, a social enterprise in {city}, might deliberately not maximise profit.', 'Its main aim is social (e.g. employment for disadvantaged groups or affordable services), so it satisfices on profit to cover costs and reinvest.', '1 mark: social objective; 1 mark: satisficing/reinvestment [2]'),
    ('During a recession, {firm} cut prices to cover only its variable costs. Explain why survival may be its main objective.', 'With falling demand it must keep cash flowing and customers loyal; covering variable costs keeps it trading until conditions improve.', '1 mark: survival definition; 1 mark: application [2]'),
])
items(t8_3, 'C2', (2, 3, 4), [
    ('Shareholders of {firm} complain that managers have spent heavily on luxury offices and company jets. Explain how this illustrates the principal–agent problem.',
     'Managers (agents) use company resources for their own benefit rather than to maximise shareholders’ (principals’) profit; dispersed shareholders cannot monitor closely.', '1 mark: identify principals and agents; 1 mark: conflicting objectives/information [2]'),
    ('{firm} gives its managers share options. Explain how this might reduce the principal–agent problem and one limitation.',
     'Managers gain when the share price rises, aligning their interests with shareholders. Limitation: encourages short-term share-price boosting or risk taking.', '1 mark: alignment; 1 mark: limitation [2]'),
    ('The government of {country} employs a private firm to run its prisons. Explain why a principal–agent problem might arise.',
     'The government (principal) wants good outcomes at low cost; the firm (agent) may cut quality to raise profit, and the government cannot observe all its actions.', '1 mark: roles; 1 mark: information/incentive gap [2]'),
])

# ============================================================================ 9 Government microeconomic intervention
t9_1 = topic('Policies to correct externalities', 'policies to correct externalities', 'taxes, subsidies, regulation and tradable pollution permits', 'tradable pollution permits')
t9_1.fixed('C1', (1, 2, 3), [
    ('A Pigouvian tax is designed to', 'make the polluter pay a tax equal to the marginal external cost at the social optimum', 'Internalises the externality: MPC + tax = MSC.',
     ['raise as much revenue as possible', 'subsidise producers of merit goods', 'reduce the price paid by consumers']),
    ('Tradable pollution permits reduce pollution at the lowest total cost because', 'firms that can cut pollution most cheaply do most of the abatement and sell their spare permits',
     'Trading equalises marginal abatement cost across firms.', ['every firm must cut pollution by the same amount', 'the government sets the price of each permit', 'permits are given only to the largest polluters']),
    ('The incidence of an indirect tax falls mainly on consumers when', 'demand is price inelastic relative to supply', 'The less elastic side bears more of the tax.',
     ['demand is perfectly elastic', 'supply is perfectly inelastic', 'demand is more elastic than supply']),
    ('A subsidy to producers of a good with positive externalities shifts', 'the supply curve to the right, lowering price and raising output', 'Subsidy lowers MPC, moving output towards the social optimum.',
     ['the demand curve to the left', 'the supply curve to the left', 'the MSB curve downwards']),
    ('Which is a disadvantage of using regulation (e.g. emission limits) to control pollution?', 'It gives no incentive to reduce pollution below the legal limit', 'Command-and-control: no reward for extra abatement; enforcement costs.',
     ['It raises tax revenue', 'It always reduces pollution to zero', 'It is market-based']),
])
t9_1.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain how an indirect tax can correct a negative production externality.', 'Diagram: MPC below MSC by MEC; demand = MSB. Market output Q1 where MPC = MSB. A tax equal to MEC at Q* shifts MPC up to MSC (MPC + tax), so output falls to Q* where MSC = MSB and price rises; the welfare loss triangle is removed and tax revenue is raised.', '1 mark: curves; 1 mark: tax shifts supply up by MEC; 1 mark: new output Q*; 1 mark: welfare loss eliminated [4]'),
    ('Explain two problems a government faces in setting the correct tax on pollution.', 'Difficulty measuring the marginal external cost; MEC varies by location and time; inelastic demand means output falls little; political pressure; firms may relocate.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain how tradable pollution permits work.', 'The government sets a cap on total emissions and issues permits; firms must hold permits for each tonne emitted. Firms with low abatement costs cut emissions and sell surplus permits to firms with high costs, so the cap is met at least cost; the cap can be tightened over time.', '1 mark: cap; 1 mark: permits required; 1 mark: trading by cost [3]'),
])


@t9_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t9_1_tax(r, D):
    b, dd = r.choice([(2, 3), (3, 2), (4, 1), (1, 4), (2, 2), (3, 1)])
    t = (b + dd) * r.choice([1, 2])
    p0 = r.choice([10, 12, 15, 20])
    q0 = r.choice([200, 300, 400])
    a = q0 + b * p0
    c = q0 - dd * p0
    pc = p0 + t * dd / (b + dd)
    pp = pc - t
    q1 = a - b * pc
    rev = t * q1
    cons_share = 100 * (pc - p0) / t
    g = r.choice(['petrol', 'cigarettes', 'plastic bags', 'sugary drinks', 'airline tickets'])
    stem = f'In the market for {g}, demand is Qd = {a} − {b}P and supply is Qs = {c} + {dd}P (Q in thousand units, P in $). The government imposes a specific tax of ${t} per unit on producers.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the equilibrium price before the tax.', f'${p0}', f'{a} − {b}P = {c} + {dd}P → P = {a - c}/{b + dd} = {p0}.', dis_num(r, p0, lambda x: f'${num(x)}', [pc, p0 + t]))
    stem += ' Calculate the equilibrium before the tax, the price paid by consumers and received by producers after the tax, the tax revenue and the share of the tax borne by consumers.'
    ans = f'Before: P = ${p0}, Q = {q0} thousand. After: consumers pay ${num(pc, 2)}, producers receive ${num(pp, 2)}, Q = {num(q1, 1)} thousand; revenue = ${num(rev, 1)} thousand; consumers bear {pct(cons_share, 0)}.'
    key = (f'Equilibrium {a} − {b}P = {c} + {dd}P → P = {p0}, Q = {q0} [1]. With tax supply: Qs = {c} + {dd}(P − {t}); {a} − {b}P = {c - dd * t} + {dd}P → P = {num(pc, 2)} [1]; '
           f'producer price {num(pp, 2)} [1]; Q = {num(q1, 1)}; revenue = {t} × {num(q1, 1)} = {num(rev, 1)} [1]; consumer share = ({num(pc, 2)} − {p0})/{t} = {pct(cons_share, 0)} [1].')
    if D >= 5:
        stem += ' Explain why the share borne by consumers takes this value.'
        ans += f' Consumers bear {"more" if b < dd else ("less" if b > dd else "half")} because demand is {"less" if b < dd else ("more" if b > dd else "equally")} responsive to price than supply.'
        key += ' Incidence linked to relative slopes/elasticities [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


@t9_1.add('C3', (2, 3, 4, 5), 'numerical')
def t9_1_permits(r, D):
    ca, cb = sorted(r.sample([10, 15, 20, 25, 30, 40, 50, 60], 2))
    ea, eb = r.choice([100, 120, 150]), r.choice([100, 120, 150])
    cut = r.choice([40, 50, 60, 80])
    f1, f2 = r.sample(FIRMS, 2)
    uniform = (cut / 2) * ca + (cut / 2) * cb
    traded = cut * ca if cut <= ea else ea * ca + (cut - ea) * cb
    save = uniform - traded
    return {'stem': f'Two firms each emit pollution. {f1} emits {ea} tonnes and can cut emissions at a constant cost of ${ca} per tonne; {f2} emits {eb} tonnes with an abatement cost of ${cb} per tonne. The government wants a total cut of {cut} tonnes. Calculate the total cost if (a) each firm must cut {num(cut / 2)} tonnes, (b) tradable permits are issued so that the total cut is achieved at least cost. (c) Explain why the permit price would lie between ${ca} and ${cb} per tonne.',
            'answer': f'(a) {money(uniform)} (b) {money(traded)}: {f1} makes the whole cut; saving {money(save)} (c) {f2} will pay up to ${cb} (its abatement cost) for a permit rather than cut; {f1} will sell for at least ${ca}, so trade occurs between these prices.',
            'key': f'(a) {num(cut / 2)}×{ca} + {num(cut / 2)}×{cb} = {money(uniform)} [2]; (b) low-cost firm abates {cut} × {ca} = {money(traded)} [2]; (c) willingness to pay vs accept [2].', 'type': 'multi_step'}


items(t9_1, 'C2', (2, 3), [
    ('The government of {country} plans to subsidise electric buses in {city}. Explain how the subsidy could improve the allocation of resources.',
     'Electric buses create external benefits (less pollution and congestion). The subsidy lowers the cost to operators, increasing supply and use towards the social optimum where MSB = MSC, reducing the welfare loss from under-consumption.',
     '1 mark: positive externality identified; 1 mark: subsidy raises output to optimum [2]'),
    ('{country} bans the use of a pesticide that harms rivers. Explain one advantage and one disadvantage of a ban compared with a tax.',
     'Advantage: certain outcome, simple to understand, appropriate when damage is severe. Disadvantage: no revenue, no incentive for innovation beyond compliance, enforcement costs, may be inefficient if some use is socially worthwhile.',
     '1 mark each [2]'),
])

t9_2 = topic('Property rights, nationalisation and privatisation', 'property rights', 'nationalisation and privatisation')
t9_2.fixed('C1', (1, 2, 3), [
    ('Extending property rights can reduce an externality because', 'the owner can charge for, or take legal action over, damage to their property', 'Coase: clear rights allow bargaining to an efficient outcome.',
     ['it removes the need for any market', 'it lowers the price of the good', 'it forces firms to merge']),
    ('Privatisation is', 'the transfer of ownership of assets or firms from the public sector to the private sector', 'Sale of state-owned enterprises; also contracting out.',
     ['the transfer of firms from the private to the public sector', 'the introduction of a minimum wage', 'the deregulation of financial markets']),
    ('Which is an argument for nationalisation of a natural monopoly?', 'The state can set price closer to marginal cost and serve unprofitable areas', 'Public interest, universal service, control of strategic industries.',
     ['It always increases productive efficiency', 'It raises money for the government by selling shares', 'It encourages competition between many firms']),
    ('The Coase theorem suggests that externalities can be resolved without government intervention if', 'property rights are clearly defined and bargaining costs are low',
     'With low transaction costs, private bargaining reaches the efficient outcome whoever holds the rights.', ['taxes are set at the right level', 'the good is a public good', 'there are many affected parties']),
])
t9_2.fixed('C2', (2, 3, 4), [
    ('Explain two arguments for privatisation.', 'Profit motive and competition improve efficiency (reduce X-inefficiency); access to private capital for investment; government revenue from sales; less political interference.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why privatising a natural monopoly may not benefit consumers.', 'It turns a public monopoly into a private one with an incentive to raise prices and restrict output; regulation is needed and may be captured.', '1 mark: private monopoly; 1 mark: higher prices/need for regulation [2]'),
    ('Explain why the Coase theorem is unlikely to solve pollution from a large city’s traffic.', 'There are millions of affected people and polluters, so bargaining costs are huge; it is hard to identify who causes damage and enforce rights.', '1 mark: many parties/high transaction costs; 1 mark: identification/enforcement [2]'),
])


@t9_2.add('C3', (2, 3, 4, 5), 'case')
def t9_2_priv(r, D):
    d = ctx(r)
    ind = r.choice(['telecommunications', 'rail', 'electricity generation', 'postal services', 'water'])
    w0, w1 = r.choice([60, 80, 100, 120]), None
    w1 = int(w0 * r.choice([0.6, 0.7, 0.75, 0.8]))
    o0 = r.choice([400, 500, 600, 800])
    o1 = int(o0 * r.choice([1.05, 1.1, 1.2, 1.25]))
    p0, p1 = r.choice([100, 100]), r.choice([90, 105, 112, 120])
    prod0, prod1 = o0 / w0, o1 / w1
    g = 100 * (prod1 - prod0) / prod0
    stem = (f'Extract: {d["country"]} privatised its {ind} company five years ago. Employment fell from {w0} thousand to {w1} thousand workers while output rose from {o0} to {o1} million units. '
            f'The real price index rose from {p0} to {p1}. ')
    parts = [
        lambda r: ('Calculate output per worker before and after privatisation and the percentage change.', f'{num(prod0, 2)} and {num(prod1, 2)} thousand units per worker; {pct(g)}', f'output ÷ workers [2]; % change [1] [3]'),
        lambda r: ('Explain why productivity may have risen after privatisation.', 'Profit motive and shareholder pressure reduce X-inefficiency; investment from private capital; competition if the market was opened.', '[2]'),
        lambda r: ('Explain what the change in the real price index suggests.', ('Real prices fell, so consumers gained.' if p1 < p0 else 'Real prices rose, so efficiency gains were not passed on to consumers, possibly due to monopoly power.'), '[2]'),
        lambda r: ('Assess whether privatisation has been in the public interest.', 'Efficiency gains vs job losses, prices, quality, investment, universal service; need for regulation; depends on competition and regulator.', '[4]'),
    ]
    return compose(r, stem, parts, k=(2, 3, 4), type_='case')


items(t9_2, 'C3', (2, 3, 4), [
    ('A factory upstream of a fish farm in {country} pollutes the river, costing the fish farm $50,000 a year. The factory could install a filter for $30,000 a year. Explain, using the Coase theorem, how an efficient outcome could be reached if (a) the fish farm has the right to clean water, (b) the factory has the right to pollute.',
     '(a) The factory must stop polluting or compensate; filtering ($30,000) is cheaper than compensation ($50,000), so it installs the filter. (b) The fish farm will pay the factory up to $50,000 to install the $30,000 filter, so the filter is installed. Either way the efficient outcome (filter) is reached; only the distribution of costs differs.',
     '(a) [2] (b) [2]; conclusion on efficiency independent of rights [1]'),
])

t9_3 = topic('Competition policy and regulation of monopolies', 'competition policy', 'regulation of monopolies and mergers')
t9_3.fixed('C1', (1, 2, 3), [
    ('An RPI − X price cap allows a regulated firm to raise its prices each year by', 'the rate of inflation minus an efficiency factor X', 'E.g. inflation 5%, X = 2 → prices may rise 3%.',
     ['the rate of inflation plus X', 'X% regardless of inflation', 'whatever the firm chooses']),
    ('Regulatory capture occurs when', 'a regulator comes to act in the interests of the firms it regulates', 'Close relationships, information asymmetry, revolving door.',
     ['a regulator takes ownership of a firm', 'firms refuse to be regulated', 'consumers set prices']),
    ('Competition authorities are most likely to block a merger that', 'would create a dominant firm with a large market share and high barriers to entry', 'Concern: substantial lessening of competition.',
     ['creates a firm with 5% market share', 'joins firms in unrelated industries with small shares', 'lowers prices for consumers']),
    ('A rate-of-return regulation sets a limit on', 'the profit a firm can earn as a percentage of its capital', 'Can encourage over-investment (Averch–Johnson) and cost padding.',
     ['the number of firms', 'the quantity produced', 'the wages paid']),
])
t9_3.fixed('C2', (2, 3, 4), [
    ('Explain how an RPI − X price cap gives a monopoly an incentive to become more efficient.', 'Prices must rise by less than inflation, so the firm can only keep its profit if it cuts costs by at least X% in real terms; any extra efficiency gains are kept as profit until the next review.', '1 mark: real price falls; 1 mark: must cut costs; 1 mark: keeps extra gains [3]'),
    ('Explain two anti-competitive practices that competition authorities investigate.', 'Price fixing by cartels; predatory pricing to drive out rivals; abuse of dominant position (exclusive dealing, refusal to supply); market sharing.', '1 mark each identified, 1 mark each explained [4]'),
])


@t9_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t9_3_cap(r, D):
    p = r.choice([40, 50, 60, 80, 100, 120])
    inf = r.choice([2, 3, 4, 5, 6, 8])
    x = r.choice([1, 1.5, 2, 3])
    allowed = inf - x
    p1 = p * (1 + allowed / 100)
    ind = r.choice(['water', 'electricity distribution', 'rail fares', 'gas transmission', 'airport charges'])
    stem = f'A regulator sets an RPI − X price cap on {ind} in {r.choice(COUNTRIES)}. The current average charge is ${p}, inflation (RPI) is {inf}% and X = {num(x)}.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the maximum average charge allowed next year.', money(round(p1, 2)), f'Allowed change = {inf} − {num(x)} = {num(allowed)}%; {p} × {num(1 + allowed / 100, 4)} = {money(round(p1, 2))}.',
                  dis_num(r, p1, lambda v: money(round(v, 2)), [p * (1 + (inf + x) / 100), p * (1 + inf / 100), p * (1 - x / 100)]))
    c0 = p * r.choice([0.7, 0.8])
    c1 = c0 * (1 + inf / 100) * (1 - r.choice([1, 2, 3, 4]) / 100)
    m0, m1 = p - c0, p1 - c1
    return {'stem': stem + f' The firm’s average cost is ${num(c0, 2)} now and is expected to be ${num(c1, 2)} next year. (a) Calculate the maximum charge next year. (b) Calculate the profit margin per unit now and next year. (c) Explain how the cap affects incentives and one weakness of this form of regulation.',
            'answer': f'(a) {money(round(p1, 2))} (b) now ${num(m0, 2)}; next year ${num(m1, 2)} (c) The firm keeps any savings beyond X, so it has an incentive to cut costs; weaknesses: setting X needs good information, firms may cut quality, regulatory capture.',
            'key': f'(a) ({inf} − {num(x)})% rise [2]; (b) price − average cost each year [2]; (c) incentive [1] and weakness [1].', 'type': 'multi_step'}


items(t9_3, 'C3', (2, 3, 4), [
    ('Three cement producers in {country} raised prices by exactly 12% on the same day and their market shares have not changed for six years. Analyse whether the competition authority should investigate them.',
     'Simultaneous identical price rises and stable shares suggest collusion (explicit or tacit), which raises price above competitive levels and causes allocative inefficiency. However, identical rises could reflect a common cost shock (energy prices) and price leadership; the authority needs evidence of agreement.',
     '1 mark: collusion signs; 1 mark: welfare effects; 1 mark: alternative explanation; 1 mark: judgement [4]'),
    ('{firm}, which has 70% of the {ind} market in {country}, offers big discounts to retailers that agree not to stock rival products. Analyse why this may be anti-competitive.',
     'Exclusive dealing raises barriers to entry and forecloses rivals’ access to outlets, entrenching dominance; in the long run prices may rise and choice and innovation fall.',
     '1 mark: abuse of dominance; 1 mark: barrier to entry; 1 mark: consumer harm; 1 mark: development [4]'),
])

t9_4 = topic('Government failure', 'government failure', 'microeconomic intervention')
t9_4.fixed('C1', (1, 2, 3), [
    ('Government failure occurs when', 'government intervention leads to a less efficient allocation of resources than before', 'Intervention worsens welfare or costs more than it gains.',
     ['the government runs a budget deficit', 'markets fail to provide public goods', 'tax revenue falls']),
    ('A maximum rent set below the equilibrium can cause government failure by', 'creating a shortage of rented housing', 'Price ceiling below equilibrium: Qd > Qs, queues, black markets, lower quality.',
     ['raising rents', 'creating a surplus of housing', 'increasing the supply of housing']),
    ('Which is a cause of government failure?', 'Imperfect information about the size of external costs', 'Also: unintended consequences, administrative cost, political self-interest, regulatory capture.',
     ['Perfect information', 'Allocative efficiency', 'Diminishing marginal utility']),
    ('A tax on cigarettes that leads to widespread smuggling is an example of', 'an unintended consequence of intervention', 'The policy creates an illegal market, reducing its effectiveness.',
     ['a successful Pigouvian tax', 'a public good', 'a merit good']),
])
t9_4.fixed('C2', (2, 3, 4), [
    ('Explain two causes of government failure.', 'Imperfect information (wrong tax/subsidy levels); unintended consequences (black markets, evasion); administrative costs; political self-interest and short-termism; regulatory capture.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why setting a tax higher than the marginal external cost could reduce welfare.', 'Output falls below the social optimum, so units with MSB > MSC are no longer produced, creating a new welfare loss.', '1 mark: output below optimum; 1 mark: welfare loss [2]'),
])
GF_CASES = [
    ('A government in {country} subsidises biofuel crops; farmers switch land from food, and food prices rise sharply.', 'Unintended consequences'),
    ('A regulator in {country} adopts the views of the energy firms it oversees after many of its staff move to jobs in those firms.', 'Regulatory capture'),
    ('Politicians in {country} cut fuel taxes just before an election, even though road congestion is rising.', 'Political self-interest and short-termism'),
    ('A carbon tax in {country} is set at $5 per tonne, far below the estimated damage of $60 per tonne.', 'Imperfect information / incorrect valuation'),
    ('A scheme to subsidise home insulation in {country} costs more to administer than the energy it saves.', 'Excessive administrative costs'),
    ('Rent controls in {city} lead landlords to sell flats, reducing the supply of rented housing.', 'Unintended consequences'),
]
GF_ALL = ['Unintended consequences', 'Regulatory capture', 'Political self-interest and short-termism', 'Imperfect information / incorrect valuation', 'Excessive administrative costs']


@t9_4.add('C3', (1, 2, 3), 'mcq')
def t9_4_class(r, D):
    s, a = r.choice(GF_CASES)
    opts, ans = mcq(r, a, [x for x in GF_ALL if x != a] + ['Market failure due to a public good'])
    return {'stem': fill(s, ctx(r)) + ' Which cause of government failure is illustrated?', 'options': opts, 'answer': ans, 'key': f'{a}.'}


@t9_4.add('C3', (2, 3, 4, 5), 'numerical')
def t9_4_ceiling(r, D):
    b, dd = r.choice([2, 3, 4]), r.choice([2, 3, 4])
    p0 = r.choice([400, 500, 600, 800])
    q0 = r.choice([20000, 30000, 40000])
    a = q0 + b * p0
    c = q0 - dd * p0
    pmax = p0 - r.choice([100, 150, 200])
    qd, qs = a - b * pmax, c + dd * pmax
    return {'stem': f'In {r.choice(CITIES_ECON)}, the demand for rented flats is Qd = {a:,} − {b}P and supply is Qs = {c:,} + {dd}P, where P is monthly rent in $. The city sets a maximum rent of ${pmax}. Calculate the equilibrium rent, the quantity demanded and supplied at the maximum rent, and the shortage. Explain why this may be an example of government failure.',
            'answer': f'Equilibrium rent ${p0}, {q0:,} flats. At ${pmax}: Qd = {qd:,}, Qs = {qs:,}, shortage = {qd - qs:,} flats. Government failure: fewer flats are available than before, queues and black markets appear and quality may fall, so the policy may harm the tenants it aims to help.',
            'key': f'Equilibrium {a:,} − {b}P = {c:,} + {dd}P → P = {p0} [1]; Qd and Qs at ceiling [2]; shortage {qd - qs:,} [1]; unintended consequences explained [1].', 'type': 'multi_step'}


CITIES_ECON = ['the capital of Zentara', 'Port Kestria', 'New Valdoria', 'Lunaria City', 'Marvona Bay', 'North Pelora']


def _gov_c4(r, D):
    d = ctx(r)
    mec = r.choice([40, 50, 60, 80])
    tax = r.choice([10, 20, 30, 100, 120])
    intro = f'Extract: Scientists estimate the marginal external cost of carbon emissions in {d["country"]} at ${mec} per tonne. The government is debating a carbon tax of ${tax} per tonne, a cap-and-trade permit scheme, or stricter regulation of power stations.'
    parts = [
        lambda r: ('Explain whether the proposed tax is likely to achieve the social optimum.', ('Tax below MEC: output still above the optimum.' if tax < mec else 'Tax above MEC: output would fall below the optimum (government failure).'), '[2]'),
        lambda r: ('With the aid of a diagram, explain how a cap-and-trade scheme sets the quantity of emissions.', 'Vertical supply of permits at the cap; demand for permits from firms; price set by the market; firms with low abatement costs sell.', '[3]'),
        lambda r: ('Compare the effectiveness of a carbon tax and tradable permits.', 'Tax: price certainty, revenue, but quantity uncertain; permits: quantity certainty, price volatile, may be over-allocated; both give incentives.', '[4]'),
        lambda r: ('Discuss whether the government should use regulation instead.', 'Certainty and simplicity vs no incentive to go beyond limits, enforcement costs, inflexibility; combination may be best.', '[4]'),
        lambda r: ('Explain one way in which this intervention could lead to government failure.', 'Wrong valuation, carbon leakage to other countries, lobbying, administrative cost.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t9_1, t9_2, t9_3, t9_4], 'C4', (3, 4, 5), 'case', _gov_c4)
essays(t9_1, [
    ('tradable pollution permits are more effective than taxes in reducing pollution',
     'With the aid of a diagram, explain how a tax can be used to correct a negative externality.',
     'Permits fix the quantity, reduce pollution at least cost, and the cap can be tightened.',
     'Taxes give price certainty and revenue; permits can be over-allocated and prices volatile; monitoring needed for both; choice depends on the pollutant.'),
    ('subsidies are the best way to increase the consumption of merit goods',
     'Explain why merit goods are under-consumed in a free market.',
     'Subsidies lower price and raise consumption towards the optimum.',
     'Information provision, regulation (compulsory schooling) or direct provision may be better; opportunity cost of subsidies; deadweight subsidy for those who would consume anyway.'),
], ['Air quality in {city} has deteriorated sharply in recent years.', 'Vaccination and school attendance rates in rural {country} are low.'])
essays(t9_2, [
    ('privatisation always improves economic efficiency',
     'Explain what is meant by privatisation and nationalisation.',
     'Profit motive, competition and private capital reduce X-inefficiency.',
     'Private monopolies need regulation; quality and universal service may suffer; efficiency gains depend on competition, not ownership.'),
    ('extending property rights is a better solution to externalities than taxation',
     'Explain the Coase theorem.',
     'Clear rights allow bargaining to efficient outcome without government cost.',
     'Transaction costs, many parties, unequal bargaining power, legal costs; works for small-number cases only.'),
], ['The government of {country} plans to sell its state-owned {ind} company.'])
essays(t9_3, [
    ('regulation of monopolies is more effective than breaking them up',
     'Explain how an RPI − X price cap works.',
     'Price caps and regulation keep economies of scale while protecting consumers.',
     'Regulatory capture, information asymmetry, cost of regulation; breaking up may increase competition but lose economies of scale; depends on natural monopoly.'),
    ('competition policy always benefits consumers',
     'Explain the main aims of competition policy.',
     'Prevents abuse of market power, collusion and harmful mergers, lowering prices.',
     'Blocking mergers may lose economies of scale and dynamic efficiency; investigations are costly and slow; global markets.'),
], ['The competition authority of {country} is investigating the {ind} industry.'])
essays(t9_4, [
    ('government failure means that governments should not intervene in markets',
     'Explain what is meant by government failure, using examples.',
     'Imperfect information, unintended consequences and political motives can make outcomes worse.',
     'Market failure may be larger; better information and design reduce failure; compare costs of intervention with costs of market failure.'),
], ['Several recent interventions in {country}, including rent controls and fuel subsidies, have been criticised.'])
CHAPTERS[9] = [t9_1, t9_2, t9_3, t9_4]

# ============================================================================ 10 Equity and redistribution
t10_1 = topic('Lorenz curve and Gini coefficient', 'measuring inequality', 'lorenz curve and gini coefficient', 'gini')
t10_1.fixed('C1', (1, 2, 3), [
    ('A Lorenz curve shows', 'the cumulative percentage of income received by cumulative percentages of the population', 'Plotted against the 45° line of perfect equality.',
     ['the relationship between unemployment and inflation', 'income per head over time', 'the share of each sector in GDP']),
    ('A Gini coefficient of 0 indicates', 'perfect equality of income', 'Gini ranges from 0 (perfect equality) to 1 (one person has all income).',
     ['perfect inequality', 'zero income', 'a balanced budget']),
    ('The Gini coefficient is calculated as', 'the area between the line of equality and the Lorenz curve divided by the total area under the line of equality', 'G = A/(A + B).',
     ['the income share of the top 10% divided by the bottom 10%', 'the slope of the Lorenz curve', 'mean income divided by median income']),
    ('If a Lorenz curve moves further away from the line of equality, income inequality has', 'increased', 'Larger area A → higher Gini.', ['decreased', 'stayed the same', 'become zero']),
    ('Wealth is usually distributed more unequally than income because', 'wealth accumulates over time and is passed on through inheritance', 'Stock vs flow; returns on wealth compound.',
     ['wealth is a flow and income is a stock', 'income cannot be taxed', 'wealth is measured per hour']),
])
t10_1.fixed('C2', (2, 3, 4), [
    ('Distinguish between income and wealth.', 'Income is a flow of money received over a period (wages, rent, interest, profit, benefits); wealth is a stock of assets owned at a point in time (property, shares, savings).', '1 mark each [2]'),
    ('Explain one limitation of the Gini coefficient as a measure of inequality.', 'Different Lorenz curves can give the same Gini, so it does not show where in the distribution inequality occurs; it ignores non-cash benefits and household size.', '1 mark: limitation; 1 mark: explanation [2]'),
    ('Explain how progressive taxation affects the Lorenz curve.', 'Taking a larger proportion of higher incomes reduces post-tax income shares of the rich relative to the poor, moving the Lorenz curve towards the line of equality and lowering the Gini.', '1 mark: higher proportion from rich; 1 mark: curve moves towards equality [2]'),
])


def _quintiles(r):
    while True:
        q = sorted(r.sample(range(3, 52), 4))
        top = 100 - sum(q)
        if top > q[-1] and top < 70:
            return q + [top]


@t10_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_1_gini(r, D):
    sh = _quintiles(r)
    cum = [0]
    for s in sh:
        cum.append(cum[-1] + s)
    B = sum(0.2 * (cum[i] + cum[i - 1]) / 2 / 100 for i in range(1, 6))
    g = (0.5 - B) / 0.5
    c = r.choice(COUNTRIES)
    desc = ', '.join(f'quintile {i + 1}: {s}%' for i, s in enumerate(sh))
    if D <= 2:
        k = r.choice([2, 3, 4])
        return cq(r, D, f'Income shares by quintile (poorest first) in {c} are: {desc}. Calculate the cumulative share of income received by the poorest {20 * k}% of households.', f'{cum[k]}%',
                  f'Sum of first {k} quintiles: {" + ".join(map(str, sh[:k]))} = {cum[k]}%.', dis_num(r, cum[k], lambda x: f'{num(x)}%', [sh[k - 1], 20 * k]))
    stem = f'Income shares by quintile (poorest first) in {c}: {desc}. (a) Calculate the cumulative income shares for plotting a Lorenz curve. (b) Using the trapezium rule, estimate the Gini coefficient.'
    ans = f'(a) 20%: {cum[1]}%, 40%: {cum[2]}%, 60%: {cum[3]}%, 80%: {cum[4]}%, 100%: 100% (b) Area under Lorenz curve B = {num(B, 3)}; Gini = (0.5 − {num(B, 3)})/0.5 = {num(g, 2)}.'
    key = f'(a) cumulative shares [2]; (b) B = Σ 0.2 × (Yᵢ + Yᵢ₋₁)/2 = {num(B, 3)} [2]; G = A/(A + B) with A + B = 0.5 → {num(g, 2)} [1].'
    if D >= 4:
        r2 = r.choice(['the richest 20% paid more tax and transfers raised the share of the poorest 20% by 2 percentage points', 'the poorest 20% gained a 3 percentage point higher share at the expense of the richest 20%'])
        stem += f' (c) After a reform, {r2}. Explain how the Lorenz curve and Gini coefficient would change.'
        ans += ' (c) The Lorenz curve moves closer to the line of equality and the Gini coefficient falls.'
        key += ' (c) direction of movement and Gini fall [2].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t10_2 = topic('Poverty and the poverty trap', 'absolute and relative poverty', 'poverty trap')
t10_2.fixed('C1', (1, 2, 3), [
    ('Absolute poverty is', 'a situation where income is too low to meet basic needs such as food, shelter and clothing', 'Often measured by an international line such as $2.15 a day (PPP).',
     ['having less income than the average person', 'being unemployed', 'paying more tax than others']),
    ('Relative poverty is commonly defined as', 'household income below 60% of median income', 'Relative measure: poverty compared with the living standards of the society.',
     ['income below $2.15 a day', 'income below the minimum wage', 'having no wealth']),
    ('The poverty trap occurs when', 'a rise in gross income leads to little or no rise in net income because of taxes and benefit withdrawal', 'High effective marginal tax rates discourage work.',
     ['wages fall below the minimum wage', 'prices rise faster than incomes', 'a country has too much debt']),
    ('The effective marginal tax rate measures', 'the proportion of an extra dollar of gross income lost through taxes and reduced benefits', 'EMTR = (extra tax + benefit lost)/extra gross income.',
     ['the average rate of tax paid', 'the top rate of income tax', 'the tax paid by firms']),
])
t10_2.fixed('C2', (2, 3, 4), [
    ('Distinguish between absolute and relative poverty.', 'Absolute: income insufficient for basic needs, a fixed standard; relative: income low compared with others in the same society (e.g. below 60% of median), so it changes as average incomes rise.', '1 mark each [2]'),
    ('Explain how means-tested benefits can create a poverty trap.', 'As income rises, means-tested benefits are withdrawn, which together with income tax creates a high effective marginal tax rate, so the gain from working more is small and work incentives fall.', '1 mark: benefit withdrawal; 1 mark: high EMTR; 1 mark: work disincentive [3]'),
    ('Explain why relative poverty may rise even when absolute poverty falls.', 'If the incomes of the poor rise but median income rises faster, more people fall below 60% of median even though fewer lack basic needs.', '1 mark: median rises faster; 1 mark: explanation [2]'),
])


@t10_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_2_trap(r, D):
    extra = r.choice([50, 80, 100, 120, 200])
    tax = r.choice([10, 15, 20, 25])
    nic = r.choice([0, 5, 8, 10])
    wd = r.choice([40, 50, 55, 60, 70])
    lost = extra * (tax + nic + wd) / 100
    gain = extra - lost
    emtr = tax + nic + wd
    p = person(r)
    stem = f'{p} works part-time and receives a means-tested benefit. A pay rise adds ${extra} a week to gross income. Income tax is {tax}%' + (f', social insurance contributions are {nic}%' if nic else '') + f' and the benefit is withdrawn at {wd}% of extra gross income.'
    if D <= 2:
        return cq(r, D, stem + f' Calculate {p}’s effective marginal tax rate.', f'{emtr}%', f'EMTR = {tax}' + (f' + {nic}' if nic else '') + f' + {wd} = {emtr}%.',
                  dis_num(r, emtr, lambda x: f'{num(x)}%', [tax, tax + nic, wd]))
    stem += f' Calculate the increase in {p}’s net income and the effective marginal tax rate, and explain whether this is a poverty trap.'
    ans = f'Change in net income = {money(round(gain, 2))} a week; EMTR = {emtr}%. ' + ('Yes: net income actually falls, so there is no financial incentive to earn more.' if emtr >= 100 else ('Yes: over half of the extra income is lost, weakening the incentive to work more.' if emtr >= 60 else 'There is a strong disincentive, though most of the rise is kept.'))
    key = f'Lost = {extra} × {emtr}% = {num(lost, 2)} [1]; net gain = {num(gain, 2)} [1]; EMTR {emtr}% [1]; poverty trap explained [1].'
    if D >= 5:
        stem += ' Suggest one policy change that would reduce the problem, with its drawback.'
        ans += ' Reduce the withdrawal rate or raise the tax-free allowance; this costs the government more and extends benefits to higher earners.'
        key += ' Policy + drawback [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


@t10_2.add('C3', (2, 3, 4), 'numerical')
def t10_2_rel(r, D):
    inc = sorted(r.sample(range(120, 1200, 10), 9))
    med = inc[4]
    line = 0.6 * med
    below = [x for x in inc if x < line]
    return {'stem': f'The weekly incomes of nine households in a survey are ($): {", ".join(map(str, inc))}. Using a relative poverty line of 60% of median income, calculate the poverty line and the number of households in relative poverty.',
            'answer': f'Median = ${med}; poverty line = ${num(line, 2)}; {len(below)} household{"s" if len(below) != 1 else ""} in relative poverty.',
            'key': f'Median = 5th value = {med} [1]; 0.6 × {med} = {num(line, 2)} [1]; count below: {", ".join(map(str, below)) or "none"} [1].'}


t10_3 = topic('Policies to redistribute income and wealth', 'policies to redistribute income and wealth', 'effectiveness', 'redistribution')
t10_3.fixed('C1', (1, 2, 3), [
    ('A tax is progressive if', 'the proportion of income paid in tax rises as income rises', 'Average tax rate rises with income.',
     ['everyone pays the same amount', 'the proportion of income paid falls as income rises', 'it is paid only by firms']),
    ('Which is usually a regressive tax?', 'A tax on basic food', 'Low-income households spend a larger share of income on it.',
     ['A progressive income tax', 'A tax on inherited wealth', 'A capital gains tax']),
    ('A universal benefit is one that', 'is paid to everyone in a category regardless of income', 'E.g. child benefit for all; simple, high take-up, but costly.',
     ['is paid only to those below an income threshold', 'is paid only to the unemployed', 'requires a means test']),
    ('Which policy is most directly aimed at reducing wealth inequality?', 'An inheritance tax', 'Taxes the transfer of wealth between generations.',
     ['A cut in the top rate of income tax', 'A sales tax on luxuries only', 'A reduction in unemployment benefit']),
])
t10_3.fixed('C2', (2, 3, 4), [
    ('Explain the difference between the marginal and average rate of tax.', 'Marginal: the tax rate on an extra dollar of income; average: total tax paid divided by total income. In a progressive system the marginal rate exceeds the average rate.', '1 mark each; 1 mark relationship [3]'),
    ('Explain one advantage and one disadvantage of means-tested benefits compared with universal benefits.', 'Advantage: targeted at those in need, lower cost. Disadvantage: low take-up due to stigma or complexity, administrative cost, poverty trap.', '1 mark each [2]'),
    ('Explain why a minimum wage may not be an effective way of reducing poverty.', 'Many poor households have no one in work (pensioners, unemployed); some minimum-wage earners live in higher-income households; it may reduce employment if set too high.', '1 mark each reason [2]'),
])


@t10_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t10_3_tax(r, D):
    allow = r.choice([10000, 12000, 12500, 15000])
    b1 = r.choice([30000, 35000, 40000, 50000])
    r1, r2, r3 = r.choice([(10, 25, 40), (15, 30, 45), (20, 40, 45), (10, 20, 35)])
    top = b1 + r.choice([50000, 70000, 100000])
    inc = r.choice([25000, 45000, 60000, 90000, 150000, 200000])
    def taxof(y):
        t = 0
        t += max(0, min(y, b1) - allow) * r1 / 100
        t += max(0, min(y, top) - b1) * r2 / 100
        t += max(0, y - top) * r3 / 100
        return t
    tx = taxof(inc)
    avg = 100 * tx / inc
    marg = 0 if inc <= allow else (r1 if inc <= b1 else (r2 if inc <= top else r3))
    sched = f'income up to ${allow:,}: 0%; ${allow:,}–${b1:,}: {r1}%; ${b1:,}–${top:,}: {r2}%; above ${top:,}: {r3}%'
    stem = f'Income tax bands in {r.choice(COUNTRIES)} are: {sched}. A worker earns ${inc:,} a year.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the total income tax paid.', money(tx), f'Tax by band = {money(tx)}.', dis_num(r, tx, money, [inc * marg / 100, inc * r1 / 100]))
    inc2 = r.choice([x for x in (20000, 40000, 80000, 120000, 250000) if x != inc])
    tx2 = taxof(inc2)
    stem += f' Calculate the tax paid, the average and the marginal tax rate. Compare with a worker earning ${inc2:,} and explain whether the system is progressive.'
    ans = f'${inc:,}: tax {money(tx)}, average rate {pct(avg)}, marginal rate {marg}%. ${inc2:,}: tax {money(tx2)}, average rate {pct(100 * tx2 / inc2)}. ' + ('The average rate rises with income, so the system is progressive.' if (avg - 100 * tx2 / inc2) * (inc - inc2) > 0 else 'Check: average rate should rise with income in a progressive system.')
    key = f'Tax band by band [2]; average = tax/income [1]; marginal = rate on the next dollar [1]; comparison of average rates → progressive [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


items(t10_3, 'C3', (2, 3, 4), [
    ('The government of {country} plans to replace means-tested benefits with a universal basic income of $100 a week for every adult, financed by a higher income tax rate. Analyse two effects of this policy on the distribution of income.',
     'Every adult receives the same amount, which is a much larger share of income for poor households, so the distribution becomes more equal; higher tax on higher earners reduces their post-tax income. It removes the poverty trap from benefit withdrawal, but it is expensive and higher tax rates may weaken work incentives for some.',
     '1 mark each effect identified, 1 mark each analysed [4]'),
    ('A sales tax of 15% is applied to all goods in {country}. Households in the poorest quintile spend 95% of their income; those in the richest spend 50%. Analyse whether the tax is progressive or regressive.',
     'Tax as a share of income: poorest 0.15 × 95% = 14.25%; richest 0.15 × 50% = 7.5%. The poor pay a higher proportion of income, so the tax is regressive.',
     '1 mark: calculation for each group [2]; 1 mark: regressive; 1 mark: reason [4]'),
])


def _eq_c4(r, D):
    d = ctx(r)
    sh = _quintiles(r)
    cum = [0]
    for s in sh:
        cum.append(cum[-1] + s)
    B = sum(0.2 * (cum[i] + cum[i - 1]) / 2 / 100 for i in range(1, 6))
    g = (0.5 - B) / 0.5
    intro = f'Extract: In {d["country"]}, the poorest 20% of households receive {sh[0]}% of income and the richest 20% receive {sh[4]}%. Quintile shares are {", ".join(str(s) + "%" for s in sh)}. The government proposes higher top tax rates and a rise in means-tested benefits.'
    parts = [
        lambda r: ('Calculate the ratio of the income share of the richest quintile to the poorest quintile.', f'{num(sh[4] / sh[0], 2)}', f'{sh[4]}/{sh[0]} [1]'),
        lambda r: ('Estimate the Gini coefficient using the trapezium method.', f'{num(g, 2)}', f'cumulative shares {", ".join(map(str, cum[1:]))}; B = {num(B, 3)}; G = (0.5 − B)/0.5 [3]'),
        lambda r: ('Explain how the proposals would change the Lorenz curve.', 'Higher top taxes and more benefits raise the poor’s share and reduce the rich’s, moving the curve towards the line of equality.', '[2]'),
        lambda r: ('Discuss whether the proposals will reduce poverty effectively.', 'Benefits target the poor; but poverty trap, low take-up, tax avoidance and disincentives to work; supply-side measures (education) may be more lasting.', '[4]'),
        lambda r: ('Explain one reason why higher top tax rates may raise less revenue than expected.', 'Tax avoidance and evasion, migration of high earners, reduced work effort (Laffer curve).', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t10_1, t10_2, t10_3], 'C4', (3, 4, 5), 'case', _eq_c4)
essays(t10_1, [
    ('the Gini coefficient is the best measure of inequality in an economy',
     'Explain how a Lorenz curve and the Gini coefficient are used to measure inequality.',
     'Single summary figure, comparable across countries and time.',
     'Same Gini from different curves; ignores wealth, non-cash benefits, household size and regional prices; quintile ratios and Palma ratio add information.'),
], ['The Gini coefficient in {country} has risen from 0.32 to 0.41 over twenty years.'])
essays(t10_2, [
    ('relative poverty is a more useful measure than absolute poverty in a high-income economy',
     'Explain the difference between absolute and relative poverty.',
     'In high-income countries few lack basic needs; relative poverty captures social exclusion.',
     'Relative measures can rise when everyone is better off; absolute measures matter for developing economies; both needed.'),
    ('the poverty trap is the main reason why poverty persists',
     'Explain how the poverty trap arises.',
     'High EMTRs discourage work, keeping people on low incomes.',
     'Other causes: low skills, discrimination, ill health, lack of jobs, housing costs; reforms to withdrawal rates help but cost money.'),
], ['A report in {country} found that one household in five is below the relative poverty line.'])
essays(t10_3, [
    ('a progressive income tax is the most effective way to redistribute income',
     'Explain how progressive taxes and transfer payments redistribute income.',
     'Takes a larger share from the rich; funds benefits and services.',
     'Disincentive effects, avoidance and migration; benefits and in-kind provision (education, health) may be more effective; wealth taxes for wealth inequality.'),
    ('the government should aim for complete equality of income',
     'Explain why incomes are unequally distributed in a market economy.',
     'Equity, social cohesion, lower relative poverty.',
     'Loss of incentives, efficiency costs; equity vs equality; reward for skill and risk.'),
], ['The government of {country} plans to cut income tax for high earners and reduce benefits.'])
CHAPTERS[10] = [t10_1, t10_2, t10_3]

# ============================================================================ 11 Labour markets
t11_1 = topic('Demand for labour: MRP theory', 'demand for labour', 'marginal revenue product theory')
t11_1.fixed('C1', (1, 2, 3), [
    ('Marginal revenue product of labour is', 'the extra revenue a firm earns from employing one more worker', 'MRP = MPP × MR (= MPP × P in a competitive product market).',
     ['the wage paid to the last worker', 'total revenue divided by the number of workers', 'the extra output from one more worker']),
    ('A profit-maximising firm in a competitive labour market employs workers up to the point where', 'the wage equals the marginal revenue product', 'Hire while MRP ≥ W; MRP curve is the firm’s demand for labour.',
     ['the wage equals average revenue product', 'marginal product is at its maximum', 'total product is maximised']),
    ('The demand for labour is a derived demand because', 'labour is demanded for the output it produces', 'Demand depends on demand for the final product.',
     ['workers demand jobs', 'it is set by the government', 'it does not depend on wages']),
    ('A rise in the price of the product a firm sells will', 'shift the MRP curve to the right, raising the demand for labour', 'MRP = MPP × P.',
     ['shift the MRP curve to the left', 'reduce the wage', 'have no effect on demand for labour']),
    ('The wage elasticity of demand for labour is likely to be high when', 'labour costs are a large proportion of total costs', 'Also when substitutes (capital) are easy and product demand is elastic.',
     ['labour cannot be replaced by machines', 'demand for the product is inelastic', 'labour costs are a tiny share of total costs']),
])
t11_1.fixed('C2', (2, 3, 4), [
    ('Explain why the MRP curve slopes downwards.', 'Because of diminishing marginal returns, each extra worker adds less output (falling MPP); with imperfect competition, MR also falls as output rises; so MRP = MPP × MR falls.', '1 mark: diminishing MPP; 1 mark: MRP = MPP × MR [2]'),
    ('Explain two factors that affect the wage elasticity of demand for labour.', 'Ease of substituting capital; PED for the final product; proportion of labour in total costs; time period.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain two limitations of marginal revenue product theory.', 'Hard to measure the MPP of individual workers, especially in teams or services; many workers are in the public sector without a market price; wages are influenced by unions, custom and discrimination.', '1 mark each identified, 1 mark each explained [4]'),
])


@t11_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_1_mrp(r, D):
    for _ in range(30):
        mpp = sorted(r.sample(range(2, 30), 6), reverse=True)
        if len(set(mpp)) == 6:
            break
    p = r.choice([5, 8, 10, 12, 15, 20])
    mrp = [m * p for m in mpp]
    tp = []
    s = 0
    for m in mpp:
        s += m
        tp.append(s)
    w = r.choice(mrp[1:5]) - r.choice([0, p // 2])
    hire = sum(1 for x in mrp if x >= w)
    L = list(range(1, 7))
    g = r.choice(['shirts', 'boxes of fruit', 'bicycles', 'printed books'])
    tab = table(['Workers', f'Total product ({g} per day)'], list(zip(L, tp)))
    if D <= 2:
        k = r.randint(2, 6)
        return cq(r, D, f'A firm sells {g} at ${p} each in a competitive market. {tab}. Calculate the marginal revenue product of worker {k}.', f'${mrp[k - 1]}',
                  f'MPP = {tp[k - 1]} − {tp[k - 2]} = {mpp[k - 1]}; MRP = MPP × P = {mpp[k - 1]} × {p} = ${mrp[k - 1]}.', dis_num(r, mrp[k - 1], money, [tp[k - 1] * p, mpp[k - 1]]))
    stem = f'A firm sells {g} at ${p} each in a competitive product market and hires labour in a competitive labour market at ${w} per worker per day. {tab}. Calculate the MRP of each worker and the profit-maximising number of workers.'
    ans = f'MRP: {", ".join(map(str, mrp))}. Employ {hire} workers: the last worker hired has MRP ≥ ${w}; the next has MRP below the wage.'
    key = f'MPP = ΔTP [1]; MRP = MPP × P [1]; hire while MRP ≥ W [1]; {hire} workers [1].'
    if D >= 4:
        p2 = p + r.choice([2, 4, 5])
        hire2 = sum(1 for m in mpp if m * p2 >= w)
        stem += f' The product price then rises to ${p2}. Explain the effect on the demand for labour and calculate the new employment.'
        ans += f' At ${p2}, MRP rises (shifts right), so employment rises to {hire2}.'
        key += f' New MRP = MPP × {p2}; employment {hire2} [2].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t11_2 = topic('Supply of labour and wage elasticity', 'supply of labour', 'wage elasticity of labour supply')
t11_2.fixed('C1', (1, 2, 3), [
    ('The wage elasticity of supply of labour measures', 'the responsiveness of the quantity of labour supplied to a change in the wage rate', '%ΔQs labour ÷ %Δwage.',
     ['the responsiveness of labour demand to the wage', 'the change in wages when prices rise', 'the number of hours worked per week']),
    ('A backward-bending individual labour supply curve occurs when', 'the income effect of a higher wage outweighs the substitution effect', 'At high wages workers buy more leisure.',
     ['the substitution effect outweighs the income effect', 'wages fall', 'the firm is a monopsonist']),
    ('The supply of labour to a particular occupation is likely to be inelastic when', 'long training and specific qualifications are required', 'E.g. surgeons, airline pilots.',
     ['the job requires few skills', 'many workers can easily switch into it', 'the time period is long']),
    ('Which would shift the supply of labour to an occupation to the right?', 'An improvement in working conditions in that occupation', 'Non-wage factors shift supply; a wage change moves along it.',
     ['A rise in the wage in that occupation', 'Higher wages in alternative occupations', 'Longer training requirements']),
])
t11_2.fixed('C2', (2, 3, 4), [
    ('Explain the income and substitution effects of a wage rise on the hours an individual wants to work.', 'Substitution effect: leisure becomes more expensive (higher opportunity cost), so the worker supplies more hours. Income effect: with higher income the worker can afford more leisure, so supplies fewer hours. The net effect depends on which is larger.', '1 mark each effect; 1 mark net effect [3]'),
    ('Explain two non-wage factors that influence the supply of labour to an occupation.', 'Working conditions; job security; training and qualifications; status; fringe benefits; location; flexibility.', '1 mark each identified, 1 mark each explained [4]'),
])


@t11_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_2_wes(r, D):
    w0 = r.choice([10, 12, 15, 20, 25])
    dw = r.choice([10, 20, 25, 5])
    l0 = r.choice([1000, 2000, 4000, 5000])
    dl = r.choice([2, 4, 5, 10, 15, 30, 40])
    w1 = w0 * (1 + dw / 100)
    l1 = l0 * (1 + dl / 100)
    e = dl / dw
    occ = r.choice(['care workers', 'delivery drivers', 'nurses', 'software engineers', 'bus drivers', 'hotel staff'])
    stem = f'When the hourly wage of {occ} in {r.choice(COUNTRIES)} rose from ${num(w0)} to ${num(w1, 2)}, the number willing to work rose from {l0:,} to {num(l1)}. Calculate the wage elasticity of supply of labour'
    if D <= 2:
        return cq(r, D, stem + '.', num(e, 2), f'%ΔL = {dl}%, %ΔW = {dw}%; WES = {dl}/{dw} = {num(e, 2)}.', dis_num(r, e, lambda x: num(x, 2), [dw / dl]))
    return {'stem': stem + ' and explain two reasons why the supply of labour to this occupation might be ' + ('inelastic' if e < 1 else 'elastic') + '.',
            'answer': f'WES = {dl}%/{dw}% = {num(e, 2)} ({"inelastic" if e < 1 else "elastic"}). ' + ('Long training/qualifications, vocation-specific skills, geographical immobility, short time period.' if e < 1 else 'Few skills needed, workers can move easily from other jobs, large pool of potential workers.'),
            'key': f'% changes [1]; WES = {num(e, 2)} [1]; two reasons consistent with the value [2].', 'type': 'numerical'}


t11_3 = topic('Wage determination, monopsony and trade unions', 'wage determination in competitive markets', 'monopsony', 'role of trade unions')
t11_3.fixed('C1', (1, 2, 3), [
    ('A monopsonist in a labour market', 'is the single buyer of labour and pays a lower wage and employs fewer workers than a competitive market', 'MCL > ALS; employs where MCL = MRP, pays wage from supply curve.',
     ['is a single seller of labour', 'pays a wage equal to MRP', 'employs more workers than a competitive market']),
    ('For a monopsonist, the marginal cost of labour is above the wage because', 'to hire an extra worker it must raise the wage for all its workers', 'Upward-sloping supply of labour to the firm.',
     ['workers are paid different wages', 'it is a price taker in the labour market', 'labour supply is perfectly elastic']),
    ('Bilateral monopoly in a labour market means', 'a monopsony employer bargaining with a monopoly trade union', 'Wage settled by bargaining between limits.',
     ['two firms selling labour', 'two unions competing', 'a minimum wage set by the government']),
    ('A trade union is most likely to raise wages without reducing employment when', 'the employer is a monopsonist', 'Union wage can be set between the monopsony wage and the competitive wage, raising both W and L.',
     ['labour demand is very wage elastic', 'the labour market is perfectly competitive with elastic demand', 'machines can easily replace workers']),
])
t11_3.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain how wages and employment are determined in a monopsony labour market.', 'Diagram: wage on vertical axis, labour horizontal. Upward-sloping supply (ACL); MCL above and steeper; downward-sloping MRP. Employment Lm where MCL = MRP; wage Wm read from supply curve at Lm, below MRP. Compared with competitive equilibrium (MRP = supply), wage and employment are lower.', '1 mark: curves; 1 mark: MCL = MRP; 1 mark: wage from supply; 1 mark: comparison [4]'),
    ('Explain how a trade union could raise wages in a competitive labour market and the likely effect on employment.', 'By collective bargaining or restricting labour supply; the wage rises above equilibrium, so employers move up their MRP curve and employ fewer workers; the fall in employment is larger if labour demand is wage elastic.', '1 mark: method; 1 mark: wage above equilibrium; 1 mark: employment falls depending on elasticity [3]'),
])


@t11_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_3_mono(r, D):
    base = r.choice([40, 50, 60, 80])
    step = r.choice([10, 20])
    L = list(range(1, 8))
    wage = [base + step * (l - 1) for l in L]
    tcl = [w * l for w, l in zip(wage, L)]
    mcl = [tcl[0]] + [tcl[i] - tcl[i - 1] for i in range(1, 7)]
    k = r.randint(3, 4)
    for _ in range(30):
        sl = r.choice([5, 10, 15, 20])
        e = r.choice([0, 5])
        mrp = [mcl[k - 1] + e + (k - 1 - i) * sl for i in range(7)]
        if mrp[-1] > 0:
            break
    emp = max(i + 1 for i in range(7) if mrp[i] >= mcl[i])
    wm = wage[emp - 1]
    comp = max(i + 1 for i in range(7) if mrp[i] >= wage[i])
    tab = table(['Workers', 'Wage needed to attract this many ($ per day)', 'MRP ($)'], list(zip(L, wage, mrp)))
    if D <= 2:
        kk = r.randint(2, 7)
        return cq(r, D, f'A monopsony employer faces this labour supply schedule: {tab}. Calculate the marginal cost of employing worker {kk}.', f'${mcl[kk - 1]}',
                  f'TCL({kk}) = {wage[kk - 1]} × {kk} = {tcl[kk - 1]}; TCL({kk - 1}) = {tcl[kk - 2]}; MCL = {mcl[kk - 1]}.', dis_num(r, mcl[kk - 1], money, [wage[kk - 1], tcl[kk - 1]]))
    stem = f'A monopsony employer faces this labour market: {tab}. (a) Calculate the total and marginal cost of labour. (b) Identify the profit-maximising employment and wage. (c) Compare with the outcome if the market were competitive.'
    ans = f'(a) TCL: {", ".join(map(str, tcl))}; MCL: {", ".join(map(str, mcl))} (b) {emp} workers (MCL ≤ MRP), wage ${wm} (from supply) (c) Competitive: employ where wage = MRP: {comp} workers at about ${wage[comp - 1]}; monopsony employs fewer and pays less.'
    key = '(a) TCL = W × L, MCL = ΔTCL [2]; (b) MCL = MRP, wage read from supply [2]; (c) competitive outcome where supply = MRP; comparison [2].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


@t11_3.add('C3', (2, 3, 4), 'numerical')
def t11_3_comp(r, D):
    b, dd = r.choice([20, 40, 50]), r.choice([20, 30, 50])
    w = r.choice([10, 12, 15, 20])
    l = r.choice([2000, 3000, 4000])
    a, c = l + b * w, l - dd * w
    occ = r.choice(['warehouse workers', 'cleaners', 'electricians', 'chefs'])
    return {'stem': f'In the market for {occ} in {r.choice(COUNTRIES)}, labour demand is Ld = {a:,} − {b}W and labour supply is Ls = {c:,} + {dd}W, where W is the hourly wage in $. Calculate the equilibrium wage and employment, and explain the effect of an increase in demand for the product these workers make.',
            'answer': f'W = ${w}, employment = {l:,}. Higher product demand raises MRP, shifting labour demand right, so wage and employment both rise.',
            'key': f'{a:,} − {b}W = {c:,} + {dd}W → W = {a - c:,}/{b + dd} = {w} [1]; L = {l:,} [1]; derived demand shift [1].'}


t11_4 = topic('Transfer earnings and economic rent', 'transfer earnings', 'economic rent')
t11_4.fixed('C1', (1, 2, 3), [
    ('Transfer earnings are', 'the minimum payment needed to keep a factor of production in its current use', 'Equal to what it could earn in its next best alternative.',
     ['earnings above the minimum needed to keep a factor in its use', 'payments made by the government', 'the total wage bill']),
    ('Economic rent is', 'any payment to a factor above its transfer earnings', 'Surplus over the supply price; area above supply curve, below wage.',
     ['the payment for renting land', 'the minimum wage', 'the cost of labour to the firm']),
    ('If the supply of a factor is perfectly inelastic, its earnings consist of', 'entirely economic rent', 'Vertical supply: the factor would be supplied at any price.',
     ['entirely transfer earnings', 'half rent and half transfer earnings', 'zero earnings']),
    ('If the supply of labour is perfectly elastic, workers’ earnings consist of', 'entirely transfer earnings', 'Horizontal supply: any wage cut means no labour is supplied.',
     ['entirely economic rent', 'mostly economic rent', 'nothing']),
])
t11_4.fixed('C2', (2, 3, 4), [
    ('Explain why top football players earn a large amount of economic rent.', 'Their talent is scarce and supply is very inelastic; demand (MRP) from clubs is high, so their wages far exceed what they could earn in their next best job (transfer earnings).', '1 mark: inelastic supply/scarce talent; 1 mark: high demand; 1 mark: wage far above transfer earnings [3]'),
    ('With the aid of a diagram, explain the difference between transfer earnings and economic rent.', 'Diagram: upward-sloping supply of labour and demand curve; equilibrium wage W and employment L. The area under the supply curve up to L is transfer earnings; the area above the supply curve and below W is economic rent.', '1 mark: diagram; 1 mark: transfer earnings area; 1 mark: economic rent area [3]'),
])


@t11_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_4_rent(r, D):
    s0 = r.choice([5, 8, 10, 12, 15])
    k = r.choice([0.002, 0.004, 0.005, 0.01])
    L = r.choice([1000, 2000, 2500, 3000])
    W = s0 + k * L
    total = W * L
    rent = 0.5 * (W - s0) * L
    te = total - rent
    occ = r.choice(['accountants', 'pilots', 'web designers', 'plumbers', 'actors'])
    stem = f'The supply curve of {occ} is W = {s0} + {k}L, where W is the hourly wage in $ and L the number of workers. The equilibrium wage is ${num(W, 2)} with {L:,} workers employed.'
    if D <= 2:
        p = person(r)
        star = r.choice([200, 400, 800, 1500])
        alt = r.choice([30, 50, 60, 80])
        return cq(r, D, f'{p}, a famous singer, earns ${star} thousand a year. Their best alternative job would pay ${alt} thousand. Calculate the economic rent {p} earns.', f'${star - alt} thousand',
                  f'Economic rent = earnings − transfer earnings = {star} − {alt} = {star - alt} thousand.', dis_num(r, star - alt, lambda x: f'${num(x)} thousand', [star, alt, star + alt]))
    stem += ' Calculate total hourly earnings, transfer earnings and economic rent.'
    ans = f'Total = ${num(total, 2)}; transfer earnings = ${num(te, 2)}; economic rent = ${num(rent, 2)}.'
    key = f'Total = W × L = {num(W, 2)} × {L:,} [1]; rent = ½ × ({num(W, 2)} − {s0}) × {L:,} = {num(rent, 2)} [1]; transfer earnings = total − rent = {num(te, 2)} [1].'
    if D >= 4:
        stem += ' Explain what would happen to the share of economic rent if labour supply became more inelastic.'
        ans += ' A steeper (more inelastic) supply curve raises the share of earnings that is economic rent.'
        key += ' More inelastic supply → larger rent share [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t11_5 = topic('Minimum wage and wage differentials', 'government intervention in labour markets', 'minimum wage', 'wage differentials')
t11_5.fixed('C1', (1, 2, 3), [
    ('A national minimum wage set above the equilibrium wage in a competitive labour market is likely to', 'reduce employment and create unemployment', 'Ls > Ld at the minimum wage.',
     ['raise employment', 'have no effect', 'reduce the supply of labour']),
    ('In a monopsony labour market, a minimum wage set between the monopsony wage and the competitive wage can', 'raise both the wage and employment', 'The minimum wage makes labour supply horizontal up to the supply curve, removing the MCL wedge.',
     ['reduce both wage and employment', 'raise wages but always reduce employment', 'have no effect on wages']),
    ('Which is a cause of wage differentials between occupations?', 'Differences in skills, training and productivity', 'Also: compensating differentials, discrimination, unions, monopsony, immobility.',
     ['All workers having identical MRP', 'Perfectly mobile labour with identical skills', 'Equal working conditions in all jobs']),
    ('A compensating wage differential is', 'a higher wage paid to compensate for unpleasant or dangerous working conditions', 'E.g. oil rig workers.',
     ['a wage paid by the government', 'a wage below the minimum wage', 'the same wage in every job']),
])
t11_5.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain how a minimum wage can increase employment in a monopsony.', 'Diagram: ACL (supply), MCL above it and MRP. Without intervention: L1 where MCL = MRP, wage W1 from supply. A minimum wage Wmin above W1 makes the firm’s MCL horizontal at Wmin up to the supply curve; employment rises to where Wmin meets supply (or MRP), with a higher wage.', '1 mark: monopsony equilibrium; 1 mark: Wmin creates horizontal MCL; 1 mark: higher employment and wage [3]'),
    ('Explain two reasons for the gender pay gap.', 'Occupational segregation (women concentrated in lower-paid sectors); career breaks and part-time work; discrimination; fewer women in senior roles.', '1 mark each identified, 1 mark each explained [4]'),
])


@t11_5.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t11_5_minw(r, D):
    b, dd = r.choice([200, 300, 400]), r.choice([200, 300, 500])
    w = r.choice([6, 8, 10, 12])
    l = r.choice([10000, 12000, 20000])
    a, c = l + b * w, l - dd * w
    m = w + r.choice([1, 2, 3])
    ld, ls = a - b * m, c + dd * m
    stem = f'In a competitive labour market for unskilled workers, demand is Ld = {a:,} − {b}W and supply is Ls = {c:,} + {dd}W (W in $ per hour). The government sets a minimum wage of ${m}.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the unemployment created by the minimum wage.', f'{ls - ld:,} workers', f'Ls − Ld at ${m} = {ls:,} − {ld:,} = {ls - ld:,}.',
                  dis_num(r, ls - ld, lambda x: f'{int(round(x)):,} workers', [l - ld, ls - l]))
    stem += ' Calculate the equilibrium wage and employment, employment at the minimum wage, the number of jobs lost and the unemployment created. Explain why these two figures differ.'
    ans = f'Equilibrium W = ${w}, L = {l:,}; at ${m}: employed {ld:,}, jobs lost {l - ld:,}, unemployment {ls - ld:,}. Unemployment exceeds jobs lost because the higher wage also attracts {ls - l:,} extra people into the labour market.'
    key = f'Equilibrium [1]; Ld at Wmin [1]; jobs lost = {l:,} − {ld:,} [1]; unemployment = Ls − Ld [1]; extra supply explanation [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


def _lab_c4(r, D):
    d = ctx(r)
    w0 = r.choice([6, 7, 8])
    w1 = w0 + r.choice([1, 1.5, 2])
    rise = 100 * (w1 - w0) / w0
    jobs = r.choice([20, 30, 50])
    intro = f'Extract: {d["country"]} will raise its national minimum wage from ${num(w0)} to ${num(w1)} an hour. Employers in retail and hospitality warn that up to {jobs},000 jobs may be lost; unions argue that many employers have monopsony power.'
    parts = [
        lambda r: ('Calculate the percentage increase in the minimum wage.', pct(rise), f'({num(w1)} − {num(w0)})/{num(w0)} × 100 [1]'),
        lambda r: ('With the aid of a diagram, explain why employers predict job losses.', 'Competitive market: wage above equilibrium, employment falls to Ld, unemployment Ls − Ld.', '[3]'),
        lambda r: ('Explain why unions argue that employment may not fall.', 'In monopsony, a minimum wage between Wm and the competitive wage raises both wage and employment.', '[3]'),
        lambda r: ('Discuss whether a higher minimum wage is the best way to reduce in-work poverty.', 'Raises pay for low-paid; may cut hours/jobs, raise prices; poorly targeted on households; alternatives: tax credits, training.', '[4]'),
        lambda r: ('Explain two factors that determine how many jobs are lost.', 'Wage elasticity of demand for labour (substitutes, labour share of costs, PED of product), size of rise relative to equilibrium, state of economy.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t11_1, t11_2, t11_3, t11_4, t11_5], 'C4', (3, 4, 5), 'case', _lab_c4)
essays(t11_1, [
    ('marginal revenue product theory fully explains the wages paid to workers',
     'Explain how the demand for labour is derived from marginal revenue product.',
     'Wages reflect productivity and product price; derived demand.',
     'Hard to measure MRP; public sector; unions, monopsony, discrimination, minimum wages, custom and practice also set wages.'),
], ['Wages for software engineers in {country} have doubled while wages for retail workers have barely changed.'])
essays(t11_2, [
    ('higher wages will always increase the supply of labour',
     'Explain the factors that determine the wage elasticity of supply of labour.',
     'Substitution effect: higher opportunity cost of leisure; more people enter the occupation.',
     'Income effect and backward-bending supply; non-wage factors; training time; immobility.'),
], ['Hospitals in {country} cannot recruit enough nurses despite pay rises.'])
essays(t11_3, [
    ('trade unions always reduce employment',
     'With the aid of a diagram, explain how wages and employment are determined in a monopsony labour market.',
     'In competitive markets, union wages above equilibrium cut employment.',
     'Monopsony case: union can raise W and L; productivity gains; reduced turnover; depends on elasticity of labour demand.'),
], ['A large mining company is the only major employer in a remote region of {country}.'])
essays(t11_4, [
    ('high earnings of top professionals are mostly economic rent and should be taxed heavily',
     'Explain the meaning of transfer earnings and economic rent.',
     'Inelastic supply of scarce talent means much of their earnings is rent, which can be taxed without reducing supply.',
     'Global mobility increases elasticity; incentive effects; measurement difficulties; fairness arguments.'),
], ['Top footballers and chief executives in {country} earn hundreds of times the average wage.'])
essays(t11_5, [
    ('a national minimum wage does more harm than good',
     'Explain the possible effects of a minimum wage on a competitive labour market.',
     'Unemployment among low-skilled; higher costs and prices; reduced competitiveness.',
     'Monopsony case; higher productivity and morale (efficiency wages); reduced poverty; size of rise and elasticity matter.'),
    ('government intervention is needed to remove wage differentials',
     'Explain three reasons why wage differentials exist.',
     'Discrimination and monopsony create unfair differentials; equal pay laws.',
     'Some differentials reflect skills and conditions and provide incentives; intervention may cause unemployment.'),
], ['The minimum wage in {country} has risen faster than average earnings for five years.'])
CHAPTERS[11] = [t11_1, t11_2, t11_3, t11_4, t11_5]

items(t11_1, 'C2', (2, 3, 4), [
    ('{firm} installs new machinery that raises the output of each worker making {good}. Explain the effect on its demand for labour.',
     'Higher marginal physical product raises MRP (MPP × MR) at every level of employment, shifting the demand for labour to the right, unless the machinery substitutes for workers.', '1 mark: MPP rises → MRP shifts right; 1 mark: substitution caveat [2]'),
    ('Demand for {good} in {country} falls sharply. Explain why workers who make {good} may lose their jobs or see lower wages.',
     'Labour demand is derived: lower product demand reduces price/MR, so MRP falls and the labour demand curve shifts left, reducing wages and/or employment.', '1 mark: derived demand; 1 mark: MRP falls → labour demand shifts left [2]'),
])
items(t11_2, 'C2', (2, 3, 4), [
    ('Explain why a large rise in wages for {ind} workers in {country} might lead some existing workers to work fewer hours.',
     'The income effect: higher wages mean the same income can be earned in fewer hours, so workers may buy more leisure; if this outweighs the substitution effect, the individual supply curve bends backwards.', '1 mark: income effect; 1 mark: outweighs substitution effect [2]'),
    ('Explain why the supply of labour to the {ind} industry in {city} is likely to be more elastic in the long run than in the short run.',
     'In the long run workers can train, gain qualifications and relocate, and new entrants join the labour force, so supply responds more to a wage change.', '1 mark: time to train/relocate; 1 mark: more responsive [2]'),
])
items(t11_3, 'C2', (2, 3, 4), [
    ('{firm} is the only large employer in a small town in {country}. Explain why it may be able to pay lower wages than firms in {city}.',
     'As a monopsonist it faces an upward-sloping labour supply curve and few alternative employers, so it employs where MCL = MRP and pays the lower wage on the supply curve.', '1 mark: monopsony/few alternatives; 1 mark: MCL = MRP, wage below MRP [2]'),
    ('Workers at {firm} in {country} have joined a trade union. Explain two ways the union might try to raise their wages.',
     'Collective bargaining backed by the threat of strike action; restricting labour supply (closed shop, longer training); productivity deals; lobbying for minimum wages.', '1 mark each [2]'),
])
items(t11_4, 'C2', (2, 3, 4), [
    ('{person} earns $90,000 a year as a surgeon in {city} but could earn $40,000 as a university lecturer. Explain how much of the salary is transfer earnings and how much is economic rent.',
     'Transfer earnings are $40,000 (the next best alternative); economic rent is $90,000 − $40,000 = $50,000.', '1 mark each [2]'),
    ('Explain why a tax on economic rent may not reduce the supply of a factor of production.', 'Economic rent is the surplus above transfer earnings; taking part of it still leaves the factor earning at least its transfer earnings, so it stays in its current use.', '1 mark: rent above minimum; 1 mark: supply unaffected [2]'),
])
items(t11_5, 'C2', (2, 3, 4), [
    ('The government of {country} raises the minimum wage by 10%. Explain why the effect on employment in the {ind} industry depends on the wage elasticity of demand for labour.',
     'If demand is wage elastic (labour a large share of costs, easy substitution by machines, elastic product demand), employment falls a lot; if inelastic, few jobs are lost.', '1 mark: elastic → big fall; 1 mark: determinants [2]'),
    ('Workers in dangerous jobs on oil rigs off {country} earn far more than office workers with similar qualifications. Explain why.',
     'A compensating differential: higher pay is needed to attract workers to unpleasant, dangerous, remote work; supply to these jobs is lower at any given wage.', '1 mark: compensating differential; 1 mark: lower supply/non-wage factors [2]'),
])

# ============================================================================ 12 Circular flow of income
t12_1 = topic('Equilibrium national income: the Keynesian cross', 'aggregate expenditure and equilibrium national income', 'keynesian cross')
t12_1.fixed('C1', (1, 2, 3), [
    ('In the Keynesian cross model, equilibrium national income occurs where', 'aggregate expenditure equals national output (income)', 'AE = Y on the 45° line; equivalently injections = withdrawals.',
     ['consumption equals investment', 'saving equals zero', 'government spending equals tax revenue']),
    ('Which is an injection into the circular flow of income?', 'Exports', 'Injections: I, G, X. Withdrawals: S, T, M.', ['Imports', 'Saving', 'Taxation']),
    ('The marginal propensity to consume is', 'the proportion of an extra unit of income that is spent on consumption', 'MPC = ΔC/ΔY.',
     ['total consumption divided by total income', 'the change in saving divided by the change in income', 'the proportion of income paid in tax']),
    ('Autonomous consumption is', 'consumption that does not depend on the level of income', 'The intercept of the consumption function (a in C = a + bY).',
     ['consumption financed by imports', 'consumption that rises with income', 'consumption by the government']),
    ('If injections exceed withdrawals, national income will', 'rise', 'Planned spending exceeds output; firms raise output until W = J.', ['fall', 'stay the same', 'become zero']),
    ('In a two-sector economy, MPC + MPS equals', '1', 'Extra income is either consumed or saved.', ['0', 'the multiplier', 'the APC']),
])
t12_1.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain how equilibrium national income is determined in the Keynesian cross model.', 'Diagram: AE on vertical axis, national income on horizontal; 45° line where AE = Y; AE = C + I + G + (X − M) slopes upwards with slope MPC (less MPM). Equilibrium Ye where AE cuts the 45° line. Below Ye, AE > Y so stocks fall and output rises; above Ye, AE < Y so output falls.', '1 mark: axes and 45° line; 1 mark: AE line; 1 mark: equilibrium; 1 mark: adjustment [4]'),
    ('Explain why equilibrium national income is where withdrawals equal injections.', 'Withdrawals (S, T, M) take spending out of the flow; injections (I, G, X) add to it. If J > W, spending exceeds output and income rises; if W > J, income falls; only when W = J is income stable.', '1 mark: definitions; 1 mark: imbalance adjusts income; 1 mark: equality at equilibrium [3]'),
    ('Explain the difference between the average and marginal propensity to consume.', 'APC = total consumption/total income; MPC = change in consumption/change in income. With autonomous consumption, APC falls as income rises and exceeds MPC.', '1 mark each; 1 mark relationship [3]'),
])


@t12_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_1_eq(r, D):
    c = r.choice([0.6, 0.75, 0.8, 0.9])
    m = 0.0 if D <= 3 else r.choice([0.05, 0.1, 0.15])
    k = 1 / (1 - c + m)
    a = r.choice([40, 50, 60, 80, 100])
    I, G = r.choice([60, 80, 100, 120]), r.choice([0, 100, 120, 150]) if D >= 3 else 0
    X = r.choice([50, 80, 100]) if D >= 4 else 0
    A = a + I + G + X
    Y = A * k
    cn = r.choice(COUNTRIES)
    if D <= 2:
        stem = f'In a closed economy with no government, C = {a} + {c}Y and investment is ${I} billion. Calculate equilibrium national income.'
        return cq(r, D, stem, f'${num(Y, 1)} billion', f'Y = C + I → Y = {a} + {c}Y + {I} → Y(1 − {c}) = {a + I} → Y = {num(Y, 1)}.',
                  dis_num(r, Y, lambda x: f'${num(x, 1)} billion', [a + I, (a + I) / c, (a + I) * c]))
    parts = f'C = {a} + {c}Y, I = {I}, G = {G}' + (f', X = {X} and M = {m}Y' if X else '')
    stem = f'In {cn} (figures in $ billion): {parts}. Calculate equilibrium national income and the value of the multiplier.'
    ans = f'Y = ${num(Y, 1)} billion; multiplier = {num(k, 2)}.'
    key = f'Y = C + I + G' + (' + X − M' if X else '') + f' → Y = {A} + {c}Y' + (f' − {m}Y' if X else '') + f' → Y = {A}/(1 − {c}' + (f' + {m}' if X else '') + f') = {num(Y, 1)} [2]; k = 1/{num(1 - c + m, 2)} = {num(k, 2)} [1].'
    if D >= 5:
        dg = r.choice([10, 20, 25, 40])
        stem += f' Government spending then rises by ${dg} billion. Calculate the new equilibrium and the change in consumption.'
        dy = dg * k
        ans += f' New Y = ${num(Y + dy, 1)} billion (ΔY = {num(dy, 1)}); ΔC = {c} × {num(dy, 1)} = {num(c * dy, 1)}.'
        key += f' ΔY = k × ΔG = {num(dy, 1)} [1]; ΔC = MPC × ΔY [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t12_2 = topic('The multiplier', 'multiplier', 'calculation from mpc, mps, mpt and mpm')
t12_2.fixed('C1', (1, 2, 3), [
    ('In an open economy with a government, the multiplier is equal to', '1 / (MPS + MPT + MPM)', 'k = 1/MPW where MPW = MPS + MPT + MPM.',
     ['1 / MPC', 'MPS + MPT + MPM', '1 / (1 + MPC)']),
    ('If MPS = 0.1, MPT = 0.2 and MPM = 0.2, the multiplier is', '2', 'k = 1/(0.1 + 0.2 + 0.2) = 1/0.5 = 2.', ['5', '0.5', '10']),
    ('A larger marginal propensity to import will', 'reduce the size of the multiplier', 'More leakage abroad in each round of spending.', ['increase the multiplier', 'have no effect on the multiplier', 'make the multiplier negative']),
    ('The multiplier process works because', 'one person’s spending becomes another person’s income, which is partly re-spent', 'Successive rounds of induced consumption.',
     ['prices rise when spending rises', 'governments always borrow', 'saving always equals investment']),
])
t12_2.fixed('C2', (2, 3, 4), [
    ('Explain the multiplier effect of an increase in investment.', 'Extra investment raises incomes of workers and firms producing capital goods; they spend part of it (MPC), creating income for others, who spend part again; total income rises by a multiple of the initial injection, determined by the leakages (MPS, MPT, MPM).', '1 mark: initial injection; 1 mark: rounds of spending; 1 mark: size depends on leakages [3]'),
    ('Explain why the multiplier may be smaller in practice than the simple formula suggests.', 'High import propensity in open economies; progressive taxes; spare capacity may be lacking so prices rise; time lags; crowding out; confidence effects.', '1 mark each reason [2]'),
])


@t12_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_2_mult(r, D):
    combos = [(0.1, 0.2, 0.2), (0.1, 0.15, 0.25), (0.05, 0.2, 0.25), (0.2, 0.2, 0.1), (0.1, 0.1, 0.05), (0.15, 0.25, 0.1), (0.1, 0.2, 0.1), (0.2, 0.25, 0.3)]
    s, t, m = r.choice(combos)
    w = s + t + m
    k = 1 / w
    inj = r.choice([5, 10, 20, 25, 40, 50])
    what = r.choice(['an increase in government spending', 'an increase in investment', 'a rise in exports'])
    dy = inj * k
    stem = f'In {r.choice(COUNTRIES)}, MPS = {s}, MPT = {t} and MPM = {m}.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the value of the multiplier.', num(k, 2), f'k = 1/({s} + {t} + {m}) = 1/{num(w, 2)} = {num(k, 2)}.',
                  dis_num(r, k, lambda x: num(x, 2), [w, 1 / (s + t), 1 / s]))
    stem += f' There is {what} of ${inj} billion. Calculate the multiplier and the final change in national income, and the resulting changes in saving, tax revenue and imports.'
    ans = f'k = {num(k, 2)}; ΔY = ${num(dy, 1)} billion; ΔS = {num(s * dy, 2)}, ΔT = {num(t * dy, 2)}, ΔM = {num(m * dy, 2)} (total withdrawals {num(w * dy, 1)} = injection).'
    key = f'k = 1/{num(w, 2)} [1]; ΔY = {inj} × {num(k, 2)} [1]; each withdrawal = propensity × ΔY [1]; total withdrawals equal the injection [1].'
    if D >= 5:
        stem += ' Explain why the final change may be smaller than calculated.'
        ans += ' Crowding out, price rises near full capacity, time lags and falls in confidence reduce the effect.'
        key += ' Valid reason [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t12_3 = topic('Inflationary and deflationary gaps', 'inflationary and deflationary gaps')
t12_3.fixed('C1', (1, 2, 3), [
    ('A deflationary gap exists when', 'equilibrium national income is below the full-employment level of income', 'AE too low: spare capacity and demand-deficient unemployment.',
     ['equilibrium income is above full employment', 'prices are falling every year', 'the budget is in surplus']),
    ('An inflationary gap is', 'the amount by which aggregate expenditure exceeds the level needed for full-employment output', 'Measured vertically in the Keynesian cross; excess demand causes inflation.',
     ['the difference between actual and potential GDP when output is below potential', 'the rate of inflation minus the target', 'the gap between exports and imports']),
    ('To close a deflationary gap of $20bn of spending when the multiplier is 4, a government should raise spending by about', '$20bn', 'The gap is measured as the shortfall in AE; ΔY = 4 × 20 = 80 of income.',
     ['$80bn', '$5bn', '$4bn']),
    ('The output gap is negative when', 'actual output is below potential output', 'Negative output gap: spare capacity (deflationary gap).',
     ['actual output exceeds potential output', 'inflation is above target', 'exports exceed imports']),
])
t12_3.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain the difference between an inflationary gap and a deflationary gap.', 'Keynesian cross with full-employment income Yf marked. Deflationary gap: AE cuts the 45° line below Yf; the vertical distance between the 45° line and AE at Yf is the shortfall in spending. Inflationary gap: AE cuts above Yf; the vertical excess of AE over the 45° line at Yf is the inflationary gap.', '1 mark each correctly described gap; 1 mark vertical measurement at Yf [3]'),
    ('Explain how a government could close an inflationary gap.', 'Reduce AE: cut government spending or raise taxes (contractionary fiscal policy) or raise interest rates; the fall in AE has a multiplied effect on income until it reaches Yf.', '1 mark: policy; 1 mark: lowers AE with multiplier [2]'),
])


@t12_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_3_gap(r, D):
    k = r.choice([2, 2.5, 4, 5])
    ye = r.choice([400, 500, 600, 800, 1000])
    diff = r.choice([40, 50, 80, 100, 120])
    kind = r.choice(['def', 'inf'])
    yf = ye + diff if kind == 'def' else ye - diff
    gap = diff / k
    stem = f'Equilibrium national income in {r.choice(COUNTRIES)} is ${ye} billion and full-employment income is ${yf} billion. The multiplier is {num(k)}.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the change in aggregate expenditure needed to reach full employment.', f'${num(gap, 1)} billion {"increase" if kind == "def" else "decrease"}',
                  f'Gap in AE = ΔY/k = {diff}/{num(k)} = {num(gap, 1)}.', [f'${num(diff, 1)} billion {"increase" if kind == "def" else "decrease"}', f'${num(diff * k, 1)} billion {"increase" if kind == "def" else "decrease"}', f'${num(gap, 1)} billion {"decrease" if kind == "def" else "increase"}'])
    name = 'deflationary' if kind == 'def' else 'inflationary'
    stem += ' Identify the type of gap, calculate its size, and explain one fiscal policy to close it.'
    if D >= 4:
        stem += ' If the government changed taxes instead of spending, explain why the tax change needed would be larger than the spending change.'
    ans = f'{name.capitalize()} gap of ${num(gap, 1)} billion in AE (income gap {diff}). ' + ('Raise G or cut taxes by enough to raise AE by this amount.' if kind == 'def' else 'Cut G or raise taxes by enough to reduce AE by this amount.')
    key = f'Type [1]; AE gap = ΔY/k = {diff}/{num(k)} = {num(gap, 1)} [2]; policy with multiplier [1].'
    if D >= 4:
        ans += ' Part of a tax cut is saved (or spent on imports), so only MPC × ΔT is spent in the first round; a larger tax change is needed.'
        key += ' Only part of a tax change enters AE [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t12_4 = topic('The accelerator', 'accelerator', 'interaction with the multiplier')
t12_4.fixed('C1', (1, 2, 3), [
    ('The accelerator theory states that net investment depends on', 'the rate of change of national income (or sales)', 'Inet = v × ΔY, where v is the capital–output ratio.',
     ['the level of national income', 'the rate of interest only', 'the level of saving']),
    ('If the capital–output ratio is 3 and national income rises by $10bn, induced net investment is', '$30bn', 'Inet = 3 × 10.', ['$3.3bn', '$13bn', '$10bn']),
    ('The interaction of the multiplier and accelerator helps to explain', 'fluctuations in the business cycle', 'Investment changes magnify income changes and vice versa.',
     ['long-run economic growth only', 'the balance of payments', 'the distribution of income']),
    ('According to the accelerator, net investment will fall when', 'national income grows more slowly than before, even if it is still growing', 'Investment depends on ΔY; slower growth means lower investment.',
     ['national income grows faster', 'interest rates fall', 'the capital–output ratio rises']),
])
t12_4.fixed('C2', (2, 3, 4), [
    ('Explain how the interaction of the multiplier and accelerator can cause a boom to turn into a recession.', 'Rising investment raises income via the multiplier; higher income growth raises investment via the accelerator. When growth slows (e.g. capacity limits), induced investment falls, which via the multiplier reduces income, further reducing investment, so the economy turns down.', '1 mark: multiplier; 1 mark: accelerator; 1 mark: slowing growth reduces investment and income [3]'),
    ('Explain two limitations of the accelerator theory.', 'Firms may have spare capacity; expectations matter; capital goods industries may be at capacity; the capital–output ratio is not fixed; investment also depends on interest rates and technology.', '1 mark each identified, 1 mark each explained [4]'),
])


@t12_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t12_4_acc(r, D):
    v = r.choice([2, 3, 4])
    s0 = r.choice([100, 200, 250])
    gr = [r.choice([10, 20]), r.choice([20, 30]), r.choice([30, 20]), r.choice([10, 0]), r.choice([0, -10])]
    sales = [s0]
    for g_ in gr:
        sales.append(sales[-1] + g_)
    dep = r.choice([20, 30, 40])
    inet = [v * (sales[i + 1] - sales[i]) for i in range(5)]
    gross = [max(0, x + dep) for x in inet]
    years = list(range(1, 7))
    tab = table(['Year', 'Sales ($m)'], list(zip(years, sales)))
    if D <= 2:
        i = r.randint(1, 4)
        return cq(r, D, f'A firm’s capital–output ratio is {v}. {tab}. Calculate its net investment in year {i + 1}.', money(inet[i - 1]) + 'm',
                  f'Inet = v × ΔSales = {v} × ({sales[i]} − {sales[i - 1]}) = {inet[i - 1]}.', dis_num(r, inet[i - 1], lambda x: money(x) + 'm', [sales[i] * v, sales[i] - sales[i - 1]]))
    stem = f'A firm has a capital–output ratio of {v} and replaces ${dep}m of worn-out capital each year. {tab}. Calculate net and gross investment in years 2 to 6 and explain what the results show about the accelerator.'
    ans = f'Net investment: {", ".join(map(str, inet))}; gross investment: {", ".join(map(str, gross))} ($m). Investment rises and falls much more than sales, and falls once sales growth slows even before sales fall.'
    key = f'Inet = {v} × ΔSales [2]; gross = net + {dep} (not below zero) [1]; accelerator: investment depends on change in output, volatile [2].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


def _cf_c4(r, D):
    d = ctx(r)
    s, t, m = r.choice([(0.1, 0.2, 0.2), (0.1, 0.15, 0.25), (0.05, 0.2, 0.25), (0.15, 0.25, 0.1)])
    k = 1 / (s + t + m)
    ye, yf = r.choice([(700, 800), (900, 1000), (450, 500), (1100, 1200)])
    gap = (yf - ye) / k
    intro = f'Extract: National income in {d["country"]} is ${ye} billion, while full-employment income is estimated at ${yf} billion. The marginal propensities to save, tax and import are {s}, {t} and {m}. The finance minister proposes a ${num(gap, 1)} billion infrastructure programme.'
    parts = [
        lambda r: ('Calculate the multiplier.', num(k, 2), f'1/({s} + {t} + {m}) [1]'),
        lambda r: ('Show whether the programme would close the gap.', f'ΔY = {num(k, 2)} × {num(gap, 1)} = {yf - ye}: closes the gap exactly (in theory).', '[2]'),
        lambda r: ('With the aid of a diagram, explain the type of gap facing the economy.', 'Deflationary gap: AE cuts the 45° line below Yf; shortfall of AE at Yf.', '[3]'),
        lambda r: ('Explain how the accelerator might add to the effect of the programme.', 'Rising income raises sales growth, inducing more investment, which further raises income.', '[2]'),
        lambda r: ('Assess whether the programme will achieve full employment.', 'Multiplier uncertain (MPM, confidence), time lags, crowding out, structural unemployment not addressed, inflation risk; borrowing costs.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t12_1, t12_2, t12_3, t12_4], 'C4', (3, 4, 5), 'case', _cf_c4)
essays(t12_1, [
    ('an increase in saving will always harm an economy',
     'With the aid of a diagram, explain how equilibrium national income is determined.',
     'Paradox of thrift: higher saving lowers AE and, through the multiplier, national income.',
     'Saving funds investment in the long run; reduces inflationary pressure; depends on whether saving is channelled into investment and on spare capacity.'),
], ['Households in {country} have sharply increased their saving because of uncertainty about jobs.'])
essays(t12_2, [
    ('the multiplier makes fiscal policy a powerful tool for raising national income',
     'Explain how the multiplier is calculated in an open economy with a government sector.',
     'Injections have multiplied effects on income; a well-targeted increase in G raises Y by k × ΔG.',
     'High leakages (MPM) reduce k; crowding out; time lags; supply constraints; uncertainty about k.'),
], ['The government of {country}, a small open economy that imports most consumer goods, is planning a fiscal stimulus.'])
essays(t12_3, [
    ('a deflationary gap is a more serious problem than an inflationary gap',
     'With the aid of a diagram, explain the difference between inflationary and deflationary gaps.',
     'Deflationary gaps mean lost output and unemployment, hysteresis.',
     'Inflationary gaps erode real incomes and competitiveness and create uncertainty; severity depends on size and duration.'),
], ['{country} is operating well below full employment, while {country2} has inflation above 8%.'])
essays(t12_4, [
    ('the accelerator is the main cause of fluctuations in economic activity',
     'Explain the accelerator principle and its interaction with the multiplier.',
     'Investment is volatile and amplifies changes in demand.',
     'External shocks (commodity prices, financial crises), confidence, policy changes also cause cycles; accelerator assumptions unrealistic.'),
], ['Investment in {country} fell by 15% last year even though GDP still grew by 1%.'])
CHAPTERS[12] = [t12_1, t12_2, t12_3, t12_4]

items(t12_1, 'C2', (2, 3, 4), [
    ('Firms in {country} become more optimistic and raise planned investment. Explain, using the Keynesian cross, the effect on equilibrium national income.',
     'Higher investment shifts the AE line upwards in parallel; at the old income AE > Y, stocks run down, so firms raise output until AE again equals Y at a higher income, by a multiple of the rise in investment.', '1 mark: AE shifts up; 1 mark: adjustment; 1 mark: multiplied rise [3]'),
    ('Households in {country} save a larger share of each extra dollar of income. Explain the effect on the AE line and equilibrium income.',
     'MPC falls, so the AE line becomes flatter (and the multiplier smaller); equilibrium income falls.', '1 mark: flatter AE; 1 mark: lower equilibrium [2]'),
])
items(t12_2, 'C2', (2, 3, 4), [
    ('{country} imports about half of the goods its consumers buy. Explain why its multiplier is likely to be small.',
     'A high MPM means a large share of each round of extra spending leaks abroad, raising the total marginal propensity to withdraw and so reducing k = 1/(MPS + MPT + MPM).', '1 mark: high MPM leakage; 1 mark: smaller k [2]'),
    ('The government of {country} raises income tax rates. Explain the effect on the size of the multiplier.',
     'A higher marginal tax rate (MPT) increases withdrawals in each round of spending, so the multiplier falls.', '1 mark: higher MPT; 1 mark: smaller multiplier [2]'),
])
items(t12_3, 'C2', (2, 3, 4), [
    ('Unemployment in {country} is high and firms have spare capacity. Explain what type of gap exists and how it could be closed.',
     'A deflationary gap: AE is below the level needed for full-employment output. Expansionary fiscal or monetary policy raises AE, and the multiplier raises income towards Yf.', '1 mark: deflationary gap; 1 mark: policy and multiplier [2]'),
    ('Inflation in {country} is rising rapidly while unemployment is very low. Explain what type of gap exists.',
     'An inflationary gap: AE exceeds the level needed for full-employment output, so excess demand pulls up prices rather than output.', '1 mark: inflationary gap; 1 mark: excess demand raises prices [2]'),
])
items(t12_4, 'C2', (2, 3, 4), [
    ('Sales of {good} in {country} are still rising but more slowly than last year. Explain why firms making {good} may cut investment.',
     'Under the accelerator, net investment depends on the change in output. Slower growth means a smaller increase in required capital, so net investment falls even though sales are still rising.', '1 mark: Inet = v × ΔY; 1 mark: slower growth lowers investment [2]'),
])

# ============================================================================ 13 Economic growth and sustainability
t13_1 = topic('Actual and potential growth, output gaps and the business cycle', 'actual and potential growth', 'output gaps and the business cycle')
t13_1.fixed('C1', (1, 2, 3), [
    ('Actual economic growth is', 'an increase in real GDP', 'Measured by % change in real GDP; shown by a movement towards/along the PPC or a rightward AD shift with spare capacity.',
     ['an increase in the productive capacity of the economy', 'an increase in nominal GDP only', 'an increase in the price level']),
    ('Potential economic growth is', 'an increase in the productive capacity of the economy', 'Outward shift of the PPC or LRAS.', ['an increase in real GDP from spare capacity', 'a fall in unemployment', 'a rise in exports']),
    ('A positive output gap exists when', 'actual output is above potential output', 'Economy working above sustainable capacity: inflationary pressure.', ['actual output is below potential output', 'GDP is falling', 'the trade balance is positive']),
    ('Which phase of the business cycle is characterised by falling real GDP for two consecutive quarters?', 'Recession', 'Technical definition of recession.', ['Boom', 'Recovery', 'Peak']),
    ('During the recovery phase of the business cycle, the most likely change is', 'falling unemployment and rising investment', 'Output rises from the trough; spare capacity is used up.',
     ['rising unemployment and falling output', 'very high inflation and shortages', 'falling consumer confidence']),
])
t13_1.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain the difference between actual and potential growth.', 'PPC diagram: actual growth is a movement from a point inside the PPC towards it (using unemployed resources); potential growth is an outward shift of the PPC (more or better resources). In AD/AS: actual = rise in real output, potential = rightward shift of LRAS.', '1 mark: actual growth; 1 mark: potential growth; 1 mark: diagram description [3]'),
    ('Explain why a negative output gap may cause inflation to fall.', 'With spare capacity and unemployment, firms face weak demand and workers have little bargaining power, so firms hold down prices and wage growth slows.', '1 mark: spare capacity; 1 mark: weak price and wage pressure [2]'),
    ('Explain two causes of fluctuations in the business cycle.', 'Changes in investment (accelerator), consumer confidence, external shocks (commodity prices, world demand), financial crises, government policy changes, multiplier–accelerator interaction.', '1 mark each identified, 1 mark each explained [4]'),
])


@t13_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_1_gap(r, D):
    pot = r.choice([400, 500, 800, 1000, 1200])
    g = r.choice([-4, -3, -2.5, -2, 1.5, 2, 3])
    act = pot * (1 + g / 100)
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'Potential GDP in {c} is ${pot} billion and actual GDP is ${num(act, 1)} billion. Calculate the output gap as a percentage of potential GDP.', pct(g),
                  f'({num(act, 1)} − {pot})/{pot} × 100 = {pct(g)}.', dis_num(r, g, pct, [-g, (act - pot) / act * 100 + 0.3]))
    yrs = [r.choice([2.0, 2.5, 3.0]), r.choice([3.0, 3.5, 4.0]), r.choice([1.0, 0.5, 1.5]), r.choice([-1.0, -2.0, -0.5]), r.choice([1.5, 2.0, 2.5])]
    trend = r.choice([2.0, 2.5])
    idx = [100]
    for y in yrs:
        idx.append(idx[-1] * (1 + y / 100))
    pidx = [100 * (1 + trend / 100) ** i for i in range(6)]
    gaps = [100 * (a - p) / p for a, p in zip(idx, pidx)]
    stem = f'Real GDP growth in {c} over five years was {", ".join(pct(y) for y in yrs)}. Potential output grew at a steady {pct(trend)} a year, and the output gap was zero at the start. Calculate the index of real GDP (start = 100) and the output gap at the end of each year, and identify the phases of the business cycle.'
    ans = f'Real GDP index: {", ".join(num(x, 1) for x in idx[1:])}; output gap: {", ".join(pct(x) for x in gaps[1:])}. Boom where growth exceeds trend and the gap is positive; downturn/recession when growth is negative; recovery afterwards.'
    key = 'Index compounding [2]; potential index and gap = (actual − potential)/potential [2]; phases identified with reference to growth vs trend [2].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t13_2 = topic('Policies to promote economic growth', 'policies to promote economic growth')
t13_2.fixed('C1', (1, 2, 3), [
    ('Which policy is most likely to increase potential growth?', 'Increased spending on education and training', 'Raises the quality of labour, shifting LRAS right.',
     ['A temporary cut in VAT', 'A rise in the interest rate', 'Higher import tariffs']),
    ('According to the “rule of 70”, an economy growing at 3.5% a year doubles its real GDP in about', '20 years', '70 ÷ 3.5 = 20.', ['35 years', '7 years', '245 years']),
    ('Investment in infrastructure promotes growth because it', 'raises both aggregate demand and the economy’s productive capacity', 'Shifts AD in the short run and LRAS in the long run.',
     ['reduces aggregate demand', 'only affects consumption', 'lowers labour productivity']),
    ('Which is a demand-side policy to increase actual growth?', 'A cut in interest rates', 'Monetary/fiscal expansion raises AD.', ['Deregulation of labour markets', 'Privatisation', 'Spending on research and development']),
])
t13_2.fixed('C2', (2, 3, 4), [
    ('Explain how supply-side policies can promote sustained economic growth.', 'Education, training, R&D incentives, infrastructure and competition policy raise productivity and the quantity/quality of factors, shifting LRAS right so output can grow without inflation.', '1 mark: policy; 1 mark: productivity/capacity; 1 mark: LRAS shift, non-inflationary [3]'),
    ('Explain why demand-side policies alone cannot sustain economic growth in the long run.', 'Once the output gap is closed, extra AD raises prices rather than output; long-run growth requires more capacity (LRAS shifts).', '1 mark: capacity constraint; 1 mark: inflation rather than growth [2]'),
])


@t13_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_2_rule(r, D):
    g = r.choice([1, 1.4, 2, 2.5, 3.5, 5, 7])
    c1, c2 = r.sample(COUNTRIES, 2)
    if D <= 2:
        return cq(r, D, f'Real GDP per head in {c1} grows at {num(g)}% a year. Using the rule of 70, calculate how long it takes to double.', f'{num(70 / g, 1)} years',
                  f'70 ÷ {num(g)} = {num(70 / g, 1)} years.', dis_num(r, 70 / g, lambda x: f'{num(x, 1)} years', [100 / g, 70 * g / 10]))
    y1, y2 = r.choice([2000, 4000, 6000]), r.choice([20000, 30000, 40000])
    g1, g2 = r.choice([6, 7, 8]), r.choice([1, 1.5, 2])
    n = r.choice([10, 20])
    f1, f2 = y1 * (1 + g1 / 100) ** n, y2 * (1 + g2 / 100) ** n
    return {'stem': f'GDP per head in {c1} is ${y1:,} and grows at {g1}% a year; in {c2} it is ${y2:,} and grows at {num(g2)}% a year. Calculate GDP per head in each country after {n} years and the ratio of {c2}’s to {c1}’s income now and then. Explain one policy that might have allowed {c1} to grow so fast.',
            'answer': f'{c1}: ${num(f1, 0)}; {c2}: ${num(f2, 0)}. Ratio falls from {num(y2 / y1, 1)} to {num(f2 / f1, 1)}. Policy: high investment in infrastructure and education, openness to FDI and trade, which raise productivity (catch-up growth).',
            'key': f'Compound growth Y × (1 + g)ⁿ for each [2]; ratios [1]; policy linked to productivity/capacity [2].', 'type': 'multi_step'}


items(t13_2, 'C2', (2, 3, 4), [
    ('The government of {country} doubles its spending on research and development. Explain how this could raise the trend rate of growth.',
     'R&D leads to new technology and processes, raising productivity of labour and capital; LRAS shifts right repeatedly, so potential output grows faster.', '1 mark: innovation/productivity; 1 mark: LRAS shift [2]'),
    ('{country} has cut corporation tax to attract investment by firms such as {firm}. Explain how this might promote economic growth.',
     'Higher post-tax returns encourage investment, raising AD in the short run and the capital stock (and productivity) in the long run, shifting LRAS right.', '1 mark: investment incentive; 1 mark: AD and LRAS effects [2]'),
])

t13_3 = topic('Sustainability and environmental costs of growth', 'sustainability', 'environmental costs of economic growth')
t13_3.fixed('C1', (1, 2, 3), [
    ('Sustainable economic growth is growth that', 'meets the needs of the present without reducing the ability of future generations to meet their needs', 'Brundtland definition.',
     ['is faster than the world average', 'never causes inflation', 'relies only on exports']),
    ('Which is an environmental cost of economic growth?', 'Depletion of non-renewable resources', 'Also pollution, climate change, loss of biodiversity.', ['A rise in living standards', 'Higher tax revenue', 'Lower unemployment']),
    ('“Green GDP” attempts to', 'adjust GDP for the depletion of natural resources and environmental damage', 'Subtracts environmental costs from measured output.',
     ['measure output of the agricultural sector', 'count only renewable energy output', 'convert GDP into US dollars']),
    ('Decoupling means that', 'output grows while environmental damage (e.g. emissions) does not grow or falls', 'Falling emissions intensity of GDP.', ['GDP falls while emissions rise', 'growth stops completely', 'exports exceed imports']),
])
t13_3.fixed('C2', (2, 3, 4), [
    ('Explain why economic growth may not be sustainable.', 'It may rely on depleting non-renewable resources and creating pollution and climate change whose costs fall on future generations; GDP ignores this loss of natural capital.', '1 mark: resource depletion/pollution; 1 mark: future costs; 1 mark: GDP ignores [3]'),
    ('Explain how growth can provide the resources to improve the environment.', 'Higher incomes give tax revenue for environmental protection, fund cleaner technology, and consumers demand cleaner goods (environmental Kuznets curve).', '1 mark each point [2]'),
])


@t13_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t13_3_green(r, D):
    gdp0, gdp1 = r.choice([500, 600, 800]), None
    g = r.choice([3, 4, 5, 6])
    gdp1 = gdp0 * (1 + g / 100)
    e0 = r.choice([200, 250, 300, 400])
    eg = r.choice([-2, 0, 1, 3, 5])
    e1 = e0 * (1 + eg / 100)
    i0, i1 = e0 / gdp0, e1 / gdp1
    dep = r.choice([20, 30, 40])
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'Real GDP in {c} is ${gdp0} billion. Depletion of natural resources and environmental damage are valued at ${dep} billion. Calculate “green GDP”.', f'${gdp0 - dep} billion',
                  f'{gdp0} − {dep} = {gdp0 - dep}.', dis_num(r, gdp0 - dep, lambda x: f'${num(x)} billion', [gdp0 + dep]))
    return {'stem': f'In {c}, real GDP rose from ${gdp0} billion to ${num(gdp1, 1)} billion in a year, while carbon emissions changed from {e0} million tonnes to {num(e1, 1)} million tonnes. Calculate the emissions intensity of GDP (tonnes per $1,000 of GDP) in each year and the percentage change, and explain whether growth has been decoupled from emissions.',
            'answer': f'Intensity: {num(i0 * 1000, 2)} and {num(i1 * 1000, 2)} tonnes per $1,000; change {pct(100 * (i1 - i0) / i0)}. ' + ('Absolute decoupling: emissions fell while GDP rose.' if eg < 0 else ('Relative decoupling: emissions grew more slowly than GDP.' if eg < g else 'No decoupling.')),
            'key': 'Intensity = emissions/GDP each year [2]; % change [1]; correct classification of decoupling [1].', 'type': 'numerical'}


def _gr_c4(r, D):
    d = ctx(r)
    g = r.choice([6, 7, 8])
    em = r.choice([5, 6, 9])
    intro = f'Extract: {d["country"]} has grown at {g}% a year for a decade, driven by manufacturing exports and coal-fired power. Carbon emissions have risen by {em}% a year and air pollution in {d["city"]} is severe. The government plans to raise growth further through infrastructure spending.'
    parts = [
        lambda r: ('Using the rule of 70, calculate how long it takes real GDP to double at this rate.', f'{num(70 / g, 1)} years', f'70/{g} [1]'),
        lambda r: ('Explain whether emissions growth shows decoupling.', ('Relative decoupling: emissions grow more slowly than GDP.' if em < g else 'No decoupling: emissions grow at least as fast as GDP.'), '[2]'),
        lambda r: ('Explain how infrastructure spending affects both actual and potential growth.', 'Raises AD now (multiplier) and capacity later (LRAS shifts right).', '[3]'),
        lambda r: ('Discuss whether the benefits of rapid growth outweigh its environmental costs.', 'Poverty reduction, jobs, tax revenue vs pollution, health costs, climate risks; future generations; green growth options; depends on development stage.', '[4]'),
        lambda r: ('Explain one policy to make the growth more sustainable.', 'Carbon tax/permits, subsidies for renewables, regulation of emissions, investment in public transport.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t13_1, t13_2, t13_3], 'C4', (3, 4, 5), 'case', _gr_c4)
essays(t13_1, [
    ('governments should try to eliminate the business cycle',
     'Explain the phases of the business cycle and the meaning of an output gap.',
     'Fluctuations cause unemployment, uncertainty and inflation.',
     'Some fluctuation is unavoidable and reallocates resources; policy lags and forecasting errors may worsen cycles; stabilisation rather than elimination.'),
], ['{country} has experienced three recessions in fifteen years.'])
essays(t13_2, [
    ('supply-side policies are the most effective way to achieve long-run economic growth',
     'Explain the difference between demand-side and supply-side policies to promote growth.',
     'Supply-side raises productive capacity non-inflationarily.',
     'Long time lags, costly, uncertain effects; demand-side needed in recessions; policy mix best.'),
], ['The government of {country} wants to raise its trend growth rate from 1.5% to 3%.'])
essays(t13_3, [
    ('the environmental costs of economic growth outweigh its benefits',
     'Explain the costs and benefits of economic growth.',
     'Pollution, resource depletion, climate change, inequality.',
     'Higher living standards, poverty reduction, resources for environmental protection; green technology and decoupling; depends on country.'),
], ['{country} is one of the fastest-growing economies in its region but also one of the most polluted.'])
CHAPTERS[13] = [t13_1, t13_2, t13_3]

# ============================================================================ 14 Employment and unemployment
t14_1 = topic('Full employment and the natural rate of unemployment', 'full employment', 'natural rate of unemployment')
t14_1.fixed('C1', (1, 2, 3), [
    ('The natural rate of unemployment is', 'the rate of unemployment when the labour market is in equilibrium, consisting of frictional and structural unemployment', 'No demand-deficient unemployment.',
     ['zero unemployment', 'the rate of unemployment in a recession', 'cyclical unemployment only']),
    ('Full employment is best described as', 'a situation where unemployment is at its natural rate, with no demand-deficient unemployment', 'Some frictional and structural unemployment remains.',
     ['every person of working age has a job', 'unemployment is zero', 'inflation is zero']),
    ('NAIRU stands for', 'the non-accelerating inflation rate of unemployment', 'Unemployment rate at which inflation is stable.',
     ['the natural annual income rate of unemployment', 'the national average inflation rate', 'the net average investment rate']),
    ('The unemployment rate is calculated as', 'number unemployed ÷ labour force × 100', 'Labour force = employed + unemployed.', ['number unemployed ÷ total population × 100', 'number employed ÷ labour force × 100', 'number unemployed ÷ number employed × 100']),
])
t14_1.fixed('C2', (2, 3, 4), [
    ('Explain why the natural rate of unemployment is not zero.', 'Workers take time to search between jobs (frictional) and skills or locations may not match vacancies (structural); these exist even when the labour market clears.', '1 mark: frictional; 1 mark: structural [2]'),
    ('Explain two factors that may raise the natural rate of unemployment.', 'Generous benefits reducing search intensity; occupational and geographical immobility; minimum wages above equilibrium; trade union power; technological change; poor information.', '1 mark each identified, 1 mark each explained [4]'),
])


@t14_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t14_1_rate(r, D):
    emp = r.choice([18.5, 24.0, 30.2, 42.6, 9.4])
    u = r.choice([0.8, 1.2, 1.5, 2.1, 0.6])
    lf = emp + u
    ur = 100 * u / lf
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'In {c}, {num(emp, 1)} million people are employed and {num(u, 1)} million are unemployed. Calculate the unemployment rate.', pct(ur),
                  f'U/LF = {num(u, 1)}/{num(lf, 1)} × 100 = {pct(ur)}.', dis_num(r, ur, pct, [100 * u / emp]))
    fr, st = round(u * r.choice([0.25, 0.3]), 2), round(u * r.choice([0.3, 0.35, 0.4]), 2)
    cy = u - fr - st
    nat = 100 * (fr + st) / lf
    return {'stem': f'In {c}, {num(emp, 1)} million people are employed and {num(u, 1)} million unemployed. Of the unemployed, {num(fr, 2)} million are frictionally unemployed, {num(st, 2)} million structurally unemployed and the rest are cyclically unemployed. Calculate the unemployment rate and the natural rate of unemployment, and explain which type of unemployment demand-side policy could reduce.',
            'answer': f'Unemployment rate = {pct(ur)}; natural rate = ({num(fr, 2)} + {num(st, 2)})/{num(lf, 1)} × 100 = {pct(nat)}. Demand-side policy can reduce the cyclical ({num(cy, 2)} million) unemployment.',
            'key': f'LF = {num(lf, 1)} [1]; rate [1]; natural rate = frictional + structural [1]; cyclical is demand-deficient, so addressed by demand-side policy [1].', 'type': 'numerical'}


t14_2 = topic('Voluntary and involuntary unemployment; labour market flexibility', 'voluntary and involuntary unemployment', 'labour market flexibility')
t14_2.fixed('C1', (1, 2, 3), [
    ('Voluntary unemployment occurs when', 'workers choose not to accept jobs at the current wage rate', 'Natural unemployment: gap between labour force (LF) and those willing to accept jobs (AJ) at the equilibrium wage.',
     ['workers are willing to work at the current wage but cannot find jobs', 'the economy is in recession', 'firms cannot find workers']),
    ('Involuntary unemployment exists when', 'people willing to work at the current wage cannot find a job', 'Demand-deficient or real-wage (classical) unemployment.',
     ['people choose to remain on benefits', 'students are in full-time education', 'workers retire early']),
    ('Labour market flexibility refers to', 'the ease with which wages, hours and the number of workers adjust to changing conditions', 'Numerical, functional and wage flexibility.',
     ['the number of trade unions', 'the rate of income tax', 'the level of the minimum wage only']),
    ('Real-wage (classical) unemployment is caused by', 'real wages being held above the market-clearing level', 'E.g. minimum wages or union bargaining; excess supply of labour.',
     ['a fall in aggregate demand only', 'workers moving between jobs', 'seasonal changes in demand']),
])
t14_2.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain the natural rate of unemployment using the AJ and LF curves.', 'Diagram: real wage on vertical axis, labour on horizontal; ADL (demand) downward; AJ curve (those willing to accept jobs) upward; LF curve to the right of AJ. Equilibrium where ADL = AJ gives employment Le at real wage We; the horizontal gap between AJ and LF at We is the natural rate (voluntary) unemployment.', '1 mark: curves; 1 mark: equilibrium; 1 mark: gap AJ–LF [3]'),
    ('Explain how greater labour market flexibility can reduce unemployment and one disadvantage of it.', 'Flexible wages and hours allow the labour market to clear quickly, firms hire more readily if they can adjust staff, and workers move between jobs; disadvantage: job insecurity, low pay and zero-hours contracts may reduce worker welfare and training.', '1 mark: mechanism; 1 mark: reduced unemployment; 1 mark: disadvantage [3]'),
])


@t14_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t14_2_ajlf(r, D):
    lf = r.choice([30, 32, 36, 40])
    aj = lf - r.choice([1.5, 2, 2.5, 3])
    w = r.choice([12, 15, 18])
    wh = w + r.choice([2, 3])
    ld_h = aj - r.choice([1, 1.5, 2])
    aj_h = aj + r.choice([0.5, 1])
    lf_h = lf + r.choice([0.2, 0.5])
    c = r.choice(COUNTRIES)
    stem = f'In {c}, at the equilibrium real wage of ${w} an hour, {num(aj, 1)} million people are willing to accept jobs (AJ) and the labour force (LF) is {num(lf, 1)} million.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the natural (voluntary) unemployment.', f'{num(lf - aj, 1)} million', f'LF − AJ = {num(lf, 1)} − {num(aj, 1)} = {num(lf - aj, 1)} million.',
                  dis_num(r, lf - aj, lambda x: f'{num(x, 1)} million', [aj, lf]))
    stem += f' A minimum wage of ${wh} is introduced; at this wage firms demand {num(ld_h, 1)} million workers, AJ = {num(aj_h, 1)} million and LF = {num(lf_h, 1)} million. Calculate the natural unemployment before the change, and the voluntary and involuntary unemployment after it.'
    return {'stem': stem, 'answer': f'Before: natural unemployment {num(lf - aj, 1)} million. After: involuntary (real-wage) unemployment = AJ − Ld = {num(aj_h - ld_h, 1)} million; voluntary = LF − AJ = {num(lf_h - aj_h, 1)} million; total {num(lf_h - ld_h, 1)} million.',
            'key': '1 mark: LF − AJ before; 1 mark: involuntary = AJ − Ld at Wmin; 1 mark: voluntary = LF − AJ; 1 mark: total [4]', 'type': 'multi_step'}


t14_3 = topic('Participation, productivity and policies to reduce unemployment', 'labour force participation', 'productivity', 'policies to reduce unemployment')
t14_3.fixed('C1', (1, 2, 3), [
    ('The labour force participation rate is', 'the labour force as a percentage of the working-age population', 'LF = employed + unemployed seeking work.',
     ['employment as a percentage of the total population', 'unemployment as a percentage of the labour force', 'the share of women in employment']),
    ('Labour productivity is usually measured as', 'output per worker or output per hour worked', 'Real GDP ÷ hours worked.', ['wages per worker', 'number of workers per firm', 'total output']),
    ('Which policy is best suited to reducing structural unemployment?', 'Retraining schemes for workers in declining industries', 'Structural: mismatch of skills/location.',
     ['A cut in interest rates', 'An increase in government spending on defence', 'A devaluation of the currency']),
    ('Demand-deficient unemployment is best reduced by', 'expansionary fiscal or monetary policy', 'Raise AD to close the negative output gap.', ['reducing unemployment benefits', 'retraining workers', 'improving job-search information']),
])
t14_3.fixed('C2', (2, 3, 4), [
    ('Explain two policies to reduce frictional unemployment.', 'Better information on vacancies (job centres, online matching); lower benefit replacement rates or conditional benefits to raise search intensity; help with relocation costs.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why a rise in labour productivity might lead to higher unemployment in the short run but lower unemployment in the long run.', 'Short run: the same output needs fewer workers. Long run: lower unit costs make firms more competitive, raise real incomes and demand, and create new jobs.', '1 mark: short-run effect; 1 mark: long-run competitiveness/demand [2]'),
])


@t14_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t14_3_part(r, D):
    wap = r.choice([40, 45, 50, 60])
    lf = wap * r.choice([0.6, 0.65, 0.7, 0.75])
    u = lf * r.choice([0.04, 0.05, 0.08, 0.1])
    emp = lf - u
    gdp = r.choice([600, 800, 1000, 1200])
    pr = 100 * lf / wap
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'In {c}, the working-age population is {wap} million and the labour force is {num(lf, 1)} million. Calculate the participation rate.', pct(pr),
                  f'{num(lf, 1)}/{wap} × 100 = {pct(pr)}.', dis_num(r, pr, pct, [100 * emp / wap]))
    g2 = r.choice([2, 3, 4])
    e2 = r.choice([0, 1, 2])
    p0 = gdp * 1000 / emp
    p1 = p0 * (1 + g2 / 100) / (1 + e2 / 100)
    return {'stem': f'In {c}: working-age population {wap} million; labour force {num(lf, 1)} million; unemployed {num(u, 2)} million; real GDP ${gdp} billion. Calculate the participation rate, the unemployment rate and output per employed worker. Next year real GDP rises by {g2}% and employment by {e2}%: calculate the percentage change in labour productivity.',
            'answer': f'Participation {pct(pr)}; unemployment {pct(100 * u / lf)}; output per worker ${num(p0, 0)}; productivity change {pct(100 * (p1 - p0) / p0, 2)}.',
            'key': f'LF/WAP [1]; U/LF [1]; GDP/employment = {gdp}bn/{num(emp, 2)}m [1]; (1.0{g2}/1.0{e2} − 1) × 100 [2].', 'type': 'multi_step'}


def _un_c4(r, D):
    d = ctx(r)
    u0, u1 = r.choice([(4.5, 7.8), (5.0, 9.2), (6.1, 10.4)])
    yu = r.choice([18, 22, 25])
    intro = f'Extract: Unemployment in {d["country"]} rose from {u0}% to {u1}% after factory closures in the north and a fall in export demand. Youth unemployment is {yu}%, while firms in {d["city"]} report vacancies for skilled technicians.'
    parts = [
        lambda r: ('Calculate the percentage point and percentage change in the unemployment rate.', f'{num(u1 - u0, 1)} percentage points; {pct(100 * (u1 - u0) / u0)}', '[2]'),
        lambda r: ('Identify and explain two types of unemployment present.', 'Structural (factory closures, skills mismatch with technician vacancies) and cyclical/demand-deficient (fall in export demand).', '[4]'),
        lambda r: ('Explain why vacancies and unemployment can exist at the same time.', 'Occupational and geographical immobility; skills mismatch; information gaps.', '[2]'),
        lambda r: ('Discuss the most effective policies to reduce unemployment in this economy.', 'Training and relocation help for structural; fiscal/monetary stimulus or depreciation for cyclical; time lags, costs, inflation risks; mix needed.', '[4]'),
        lambda r: ('Explain two costs of high youth unemployment.', 'Lost output, lower tax revenue and higher benefits, hysteresis (skills loss), social problems.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t14_1, t14_2, t14_3], 'C4', (3, 4, 5), 'case', _un_c4)
items(t14_2, 'C2', (2, 3, 4), [
    ('Explain why a cut in unemployment benefits in {country} might reduce voluntary unemployment.', 'Lower benefits reduce the reservation wage and the opportunity cost of working, so more people accept jobs at the going wage: AJ moves closer to LF.', '1 mark: incentive; 1 mark: AJ shifts towards LF [2]'),
    ('Many workers in {city} are on zero-hours contracts. Explain how this increases labour market flexibility.', 'Firms can vary hours with demand without hiring and firing costs, so employment adjusts quickly; but workers face insecure incomes.', '1 mark: numerical flexibility; 1 mark: effect/drawback [2]'),
])
items(t14_1, 'C2', (2, 3, 4), [
    ('Unemployment in {country} is 4%, close to its estimated natural rate. Explain why a large increase in government spending might raise inflation rather than employment.',
     'At the natural rate there is no demand-deficient unemployment; extra AD pushes unemployment below the NAIRU only temporarily, creating excess demand for labour and accelerating inflation.', '1 mark: natural rate = no cyclical; 1 mark: inflation result [2]'),
])
items(t14_3, 'C2', (2, 3, 4), [
    ('{country} plans to expand free childcare. Explain how this could raise the labour force participation rate.', 'It lowers the cost of working for parents (especially women), so more of the working-age population join the labour force.', '1 mark: reduced barrier; 1 mark: higher participation [2]'),
    ('Workers in {country} produce 20% less per hour than in {country2}. Explain two reasons for the difference.', 'Less capital per worker, lower skills/education, older technology, poorer infrastructure, weaker management.', '1 mark each [2]'),
])
essays(t14_1, [
    ('governments can reduce unemployment below its natural rate permanently',
     'Explain what is meant by the natural rate of unemployment.',
     'Demand expansion can lower unemployment in the short run.',
     'Long-run Phillips curve vertical; inflation accelerates; supply-side policies needed to lower the natural rate itself; hysteresis arguments.'),
], ['The government of {country} has promised to cut unemployment from 6% to 2%.'])
essays(t14_2, [
    ('greater labour market flexibility is the best way to reduce unemployment',
     'Explain the difference between voluntary and involuntary unemployment.',
     'Flexibility reduces real-wage unemployment and helps markets clear.',
     'Demand-deficient unemployment needs demand policy; insecurity, low productivity, inequality; depends on type of unemployment.'),
], ['Employers in {country} want laws on hiring and firing to be relaxed.'])
essays(t14_3, [
    ('supply-side policies are more effective than demand-side policies in reducing unemployment',
     'Explain the causes of structural and frictional unemployment.',
     'Training, information and incentives cut structural/frictional unemployment permanently.',
     'Demand-side needed for cyclical unemployment; supply-side slow and costly; mixture depends on cause.'),
], ['Unemployment in {country} is concentrated in regions where traditional industries have closed.'])
CHAPTERS[14] = [t14_1, t14_2, t14_3]

# ============================================================================ 15 Money and banking
t15_1 = topic('Functions and characteristics of money; money supply', 'functions and characteristics of money', 'measures of the money supply')
t15_1.fixed('C1', (1, 2, 3), [
    ('Which is a function of money?', 'A store of value', 'Functions: medium of exchange, unit of account, store of value, standard of deferred payment.',
     ['A source of inflation', 'A factor of production', 'A form of taxation']),
    ('Money acting as a unit of account means that it', 'provides a common measure of the value of goods and services', 'Prices expressed in money allow comparison.',
     ['can be exchanged for goods', 'keeps its value over time', 'can be used to repay debts in the future']),
    ('Narrow money mainly consists of', 'notes and coins in circulation and balances that can be spent immediately', 'Narrow (M0/M1): cash and sight deposits.',
     ['all bank deposits including long-term savings', 'government bonds', 'shares in companies']),
    ('Which characteristic of money is most threatened by high inflation?', 'Its ability to act as a store of value', 'Inflation erodes purchasing power.', ['Portability', 'Divisibility', 'Durability']),
    ('Broad money includes', 'notes and coins plus sight and time deposits held by the private sector', 'Broad (M3/M4) includes less liquid deposits.',
     ['only notes and coins', 'only central bank reserves', 'foreign currency reserves of the central bank']),
])
t15_1.fixed('C2', (2, 3, 4), [
    ('Explain the problems of a barter economy and how money overcomes them.', 'Barter needs a double coincidence of wants, has no common measure of value, and goods may be indivisible or perishable. Money is a medium of exchange, a unit of account and a store of value, reducing transaction costs.', '1 mark: double coincidence; 1 mark: other problem; 1 mark: money’s functions [3]'),
    ('Explain two characteristics that an item must have to function well as money.', 'Acceptability, durability, portability, divisibility, homogeneity, limited supply (scarcity), difficult to counterfeit.', '1 mark each identified, 1 mark each explained [4]'),
])


@t15_1.add('C3', (1, 2, 3, 4), 'numerical')
def t15_1_ms(r, D):
    notes = r.choice([40, 50, 60, 80])
    sight = r.choice([300, 400, 500, 600])
    time_ = r.choice([500, 700, 900, 1200])
    cds = r.choice([50, 80, 100])
    res = r.choice([20, 30, 40])
    narrow = notes + sight
    broad = notes + sight + time_ + cds
    c = r.choice(COUNTRIES)
    stem = f'Data for {c} ($ billion): notes and coins in circulation {notes}; sight deposits {sight}; time deposits {time_}; certificates of deposit {cds}; commercial banks’ reserves at the central bank {res}.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate narrow money (cash plus sight deposits).', f'${narrow} billion', f'{notes} + {sight} = {narrow}.',
                  dis_num(r, narrow, lambda x: f'${num(x)} billion', [broad, notes + res, notes]))
    return {'stem': stem + ' Calculate narrow money (cash plus sight deposits) and broad money (narrow money plus time deposits and CDs). Explain why central banks monitor broad money.',
            'answer': f'Narrow = ${narrow} billion; broad = ${broad} billion. Broad money reflects spending power and credit creation that can feed through to aggregate demand and inflation.',
            'key': f'Narrow {notes} + {sight} [1]; broad {narrow} + {time_} + {cds} [1]; banks’ reserves are not part of the money supply held by the public [1]; reason [1].', 'type': 'numerical'}


t15_2 = topic('Commercial banks and credit creation', 'commercial banks and credit creation', 'credit multiplier')
t15_2.fixed('C1', (1, 2, 3), [
    ('If banks keep a reserve ratio of 10%, the credit multiplier is', '10', 'Credit multiplier = 1 / reserve ratio = 1/0.1.', ['0.1', '1.1', '100']),
    ('Commercial banks create credit by', 'lending out a proportion of deposits, which are then re-deposited in the banking system', 'Loans create new deposits; fractional reserve banking.',
     ['printing banknotes', 'buying goods from firms', 'setting the base rate']),
    ('A rise in the required reserve ratio will', 'reduce the ability of banks to create credit', 'Smaller multiplier.', ['increase the credit multiplier', 'have no effect on lending', 'increase the money supply']),
    ('The main conflict in commercial banks’ objectives is between', 'profitability and liquidity', 'Long-term loans earn more but are less liquid.', ['saving and investment', 'imports and exports', 'tax and spending']),
])
t15_2.fixed('C2', (2, 3, 4), [
    ('Explain why the actual credit multiplier is usually smaller than 1 / reserve ratio.', 'Some money leaks out as cash held by the public; banks may hold excess reserves; there may be too few creditworthy borrowers; capital requirements limit lending.', '1 mark each leakage/limit explained [2]'),
    ('Explain the conflict between liquidity and profitability for a commercial bank.', 'Liquid assets (cash, reserves, short-term bills) earn little; profitable assets (long-term loans) cannot quickly be turned into cash. Banks must balance meeting withdrawals against earning returns.', '1 mark: liquid but low return; 1 mark: profitable but illiquid; 1 mark: balance [3]'),
])


@t15_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t15_2_cm(r, D):
    rr = r.choice([5, 8, 10, 12.5, 20, 25])
    dep = r.choice([100, 200, 500, 1000])
    m = 100 / rr
    total = dep * m
    loans = total - dep
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'Banks in {c} keep {num(rr)}% of deposits as reserves. A new deposit of ${dep} million is made. Calculate the maximum total increase in deposits.', f'${num(total)} million',
                  f'Multiplier = 1/{num(rr / 100, 3)} = {num(m, 2)}; ΔDeposits = {dep} × {num(m, 2)} = {num(total)}.', dis_num(r, total, lambda x: f'${num(x)} million', [loans, dep / rr, dep * rr / 100]))
    rounds = []
    d_ = dep
    for _ in range(3):
        rounds.append((d_, d_ * rr / 100, d_ * (1 - rr / 100)))
        d_ = d_ * (1 - rr / 100)
    rr2 = rr * 2
    return {'stem': f'A customer deposits ${dep} million in a bank in {c}. All banks keep a reserve ratio of {num(rr)}% and lend the rest, which is re-deposited. (a) Show the first three rounds of deposits, reserves and loans. (b) Calculate the credit multiplier, the maximum increase in total deposits and new loans created. (c) Calculate the effect if the reserve ratio doubles.',
            'answer': '(a) ' + '; '.join(f'deposit {num(a, 2)}, reserve {num(b, 2)}, loan {num(c_, 2)}' for a, b, c_ in rounds) + f' (b) multiplier {num(m, 2)}; deposits ${num(total)}m; loans ${num(loans)}m (c) multiplier {num(100 / rr2, 2)}; deposits ${num(dep * 100 / rr2)}m.',
            'key': '(a) each round: reserve = rr × deposit, loan re-deposited [2]; (b) 1/rr, deposits = initial × multiplier, loans = deposits − initial [2]; (c) multiplier halves [1].', 'type': 'multi_step'}


t15_3 = topic('Functions of a central bank', 'functions of a central bank', 'central bank')
t15_3.fixed('C1', (1, 2, 3), [
    ('Acting as lender of last resort means that the central bank', 'lends to commercial banks that face a shortage of liquidity', 'Prevents bank runs and financial crises.',
     ['lends directly to households', 'buys all government debt', 'sets income tax rates']),
    ('Open market operations involve the central bank', 'buying or selling government securities to influence the money supply and interest rates', 'Buying bonds injects reserves (expansionary).',
     ['changing income tax rates', 'setting tariffs on imports', 'printing coins only']),
    ('Quantitative easing is', 'the central bank creating money to buy financial assets such as government bonds', 'Used when interest rates are near zero.',
     ['a reduction in the reserve ratio to zero', 'an increase in income tax', 'a rise in the base rate']),
    ('Which is a function of a central bank?', 'Managing the country’s foreign exchange and gold reserves', 'Also: issuing notes, banker to government and banks, monetary policy, supervision.',
     ['Collecting income tax', 'Making loans to small businesses directly', 'Setting the minimum wage']),
])
t15_3.fixed('C2', (2, 3, 4), [
    ('Explain how a central bank can use open market operations to reduce the money supply.', 'It sells government bonds; buyers pay with bank deposits, reducing commercial banks’ reserves at the central bank, which limits their ability to lend and pushes up interest rates.', '1 mark: sells bonds; 1 mark: reserves fall; 1 mark: less lending/higher rates [3]'),
    ('Explain why central banks are often made independent of government.', 'To remove political pressure to cut rates before elections, giving credibility to inflation targets and anchoring expectations.', '1 mark: removes political short-termism; 1 mark: credibility/expectations [2]'),
])
items(t15_3, 'C3', (2, 3, 4), [
    ('The central bank of {country} buys $50 billion of government bonds from commercial banks. Analyse the likely effects on bank lending, interest rates and aggregate demand.',
     'Banks’ reserves rise by $50bn, increasing their ability to lend (credit multiplier); bond prices rise and yields fall, lowering long-term interest rates; cheaper credit raises consumption and investment, increasing AD; effect is limited if banks or borrowers are cautious.',
     '1 mark: reserves rise; 1 mark: lower rates; 1 mark: AD rises; 1 mark: limitation [4]'),
    ('A bank in {country} faces a sudden run as depositors withdraw funds. Analyse the role the central bank might play.',
     'As lender of last resort, it lends to the bank against collateral so depositors can be repaid, preventing contagion to other banks; moral hazard risk if banks expect rescue; supervision role.', '1 mark: lender of last resort; 1 mark: prevents contagion; 1 mark: moral hazard; 1 mark: supervision [4]'),
    ('The central bank of {country} raises banks’ minimum reserve requirement from 8% to 12%. Analyse the effect on the money supply.',
     'Credit multiplier falls from 12.5 to about 8.3, so for a given reserve base banks can support fewer deposits; lending and broad money fall; interest rates on loans rise.', '1 mark: multiplier values; 1 mark: less lending; 1 mark: money supply falls; 1 mark: interest rates [4]'),
])

t15_4 = topic('Liquidity preference and the quantity theory of money', 'liquidity preference theory', 'quantity theory of money')
t15_4.fixed('C1', (1, 2, 3), [
    ('The quantity theory of money is based on the equation', 'MV = PY (or MV = PT)', 'Fisher equation of exchange.', ['M = PV/Y', 'MY = PV', 'P = MY/V']),
    ('According to the quantity theory, if V and Y are constant, an increase in the money supply leads to', 'a proportional increase in the price level', 'Monetarist view: inflation is caused by money growth.', ['a fall in prices', 'higher real output', 'no change in prices']),
    ('In Keynes’s liquidity preference theory, the speculative demand for money rises when', 'interest rates are low and expected to rise', 'Bond prices are expected to fall, so people hold money.',
     ['interest rates are high and expected to fall', 'incomes rise', 'inflation is zero']),
    ('The transactions demand for money depends mainly on', 'the level of income', 'More income → more spending → more money needed for transactions.', ['the interest rate only', 'the exchange rate', 'the reserve ratio']),
    ('Bond prices and interest rates are', 'inversely related', 'Yield = coupon/price; when price rises, the yield falls.', ['positively related', 'unrelated', 'always equal']),
])
t15_4.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain how the interest rate is determined in liquidity preference theory.', 'Diagram: interest rate on vertical axis, quantity of money on horizontal; money supply vertical (set by central bank); liquidity preference (money demand) curve downward sloping, flattening at low rates (liquidity trap). Equilibrium rate where Ms = L. An increase in Ms lowers the rate unless in the liquidity trap.', '1 mark: vertical Ms; 1 mark: downward L curve; 1 mark: equilibrium and shift [3]'),
    ('Explain why the quantity theory of money may not hold in the short run.', 'Velocity is not constant (it changes with confidence and financial innovation) and output may rise when there is spare capacity, so money growth may raise Y rather than P.', '1 mark: V varies; 1 mark: Y can change [2]'),
    ('Explain the three motives for holding money in liquidity preference theory.', 'Transactions (day-to-day spending, depends on income); precautionary (unexpected needs, depends on income); speculative (holding money instead of bonds, inversely related to the interest rate).', '1 mark each [3]'),
])


@t15_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t15_4_qtm(r, D):
    M = r.choice([200, 250, 400, 500])
    V = r.choice([4, 5, 6])
    Y = r.choice([500, 800, 1000, 1250])
    P = M * V / Y
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'In {c}, the money supply is ${M} billion, the velocity of circulation is {V} and real output is {Y} billion units. Calculate the price level using MV = PY.', f'{num(P, 2)}',
                  f'P = MV/Y = {M} × {V}/{Y} = {num(P, 2)}.', dis_num(r, P, lambda x: num(x, 2), [Y / (M * V), M * Y / V / 1000]))
    gm = r.choice([5, 8, 10, 12])
    gv = r.choice([0, -2, 2])
    gy = r.choice([2, 3])
    gp = 100 * ((1 + gm / 100) * (1 + gv / 100) / (1 + gy / 100) - 1)
    approx = gm + gv - gy
    stem = f'In {c}, MV = PY with M = ${M} billion, V = {V} and Y = {Y} billion units. (a) Calculate the price level. (b) Next year the money supply grows by {gm}%, velocity changes by {gv}% and real output grows by {gy}%. Calculate the inflation rate.'
    ans = f'(a) P = {num(P, 2)} (b) inflation = {pct(gp, 2)} (approximately {gm} + ({gv}) − {gy} = {approx}%).'
    key = f'(a) MV/Y [1]; (b) (1 + {gm}%)(1 + {gv}%)/(1 + {gy}%) − 1 = {pct(gp, 2)} [2]; approximation accepted [1].'
    if D >= 4:
        coupon = r.choice([2, 3, 4, 5])
        p0 = r.choice([50, 80, 100])
        y0 = 100 * coupon / p0
        p1 = p0 * r.choice([0.8, 1.25])
        stem += f' (c) A perpetual bond pays ${coupon} a year and its price changes from ${p0} to ${num(p1)}. Calculate the yield before and after and explain the link with liquidity preference.'
        ans += f' (c) Yield = {pct(y0, 2)} then {pct(100 * coupon / p1, 2)}; bond prices and interest rates move inversely, so expectations of rising rates (falling bond prices) increase the speculative demand for money.'
        key += ' (c) yield = coupon/price × 100 each [1]; inverse relationship and speculative motive [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


def _money_c4(r, D):
    d = ctx(r)
    gm = r.choice([12, 15, 20])
    inf = r.choice([3, 4, 6])
    intro = f'Extract: Broad money in {d["country"]} grew by {gm}% last year after the central bank cut its policy rate to 0.5% and began buying government bonds. Inflation is {inf}% and real GDP growth is 1.5%. Some economists warn of future inflation; others say velocity has fallen.'
    parts = [
        lambda r: ('Using the quantity theory, estimate the change in velocity implied by the data.', f'%ΔV ≈ %ΔP + %ΔY − %ΔM = {inf} + 1.5 − {gm} = {num(inf + 1.5 - gm, 1)}%', '[2]'),
        lambda r: ('Explain how bond purchases by the central bank increase the money supply.', 'Central bank pays with new reserves; banks’ reserves and deposits rise; credit multiplier.', '[2]'),
        lambda r: ('Using liquidity preference theory, explain why lower interest rates may not raise spending much.', 'Liquidity trap: at very low rates people hold extra money rather than bonds; low confidence.', '[3]'),
        lambda r: ('Discuss whether the rapid growth of the money supply will lead to high inflation.', 'QTM predicts inflation if V and Y stable; but V has fallen, spare capacity, expectations anchored, banks hoarding reserves; risk when demand recovers.', '[4]'),
        lambda r: ('Explain two functions of the central bank shown in the extract.', 'Monetary policy (setting rates, QE), banker to government (bond market), lender of last resort.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t15_1, t15_2, t15_3, t15_4], 'C4', (3, 4, 5), 'case', _money_c4)
items(t15_1, 'C2', (2, 3, 4), [
    ('Inflation in {country} has reached 300% a year and people are using foreign currency for many purchases. Explain which functions of money the national currency is failing to perform.',
     'It fails as a store of value (purchasing power falls rapidly) and increasingly as a unit of account and medium of exchange, as prices are quoted and paid in foreign currency.', '1 mark: store of value; 1 mark: unit of account/medium of exchange [2]'),
    ('Most payments in {country} are now made by mobile phone rather than cash. Explain whether these balances count as money.', 'Yes: balances that can be spent immediately are generally accepted as a medium of exchange, so they form part of narrow (or broad) money, like sight deposits.', '1 mark: accepted medium of exchange; 1 mark: classification [2]'),
])
items(t15_2, 'C2', (2, 3, 4), [
    ('Banks in {country} became very cautious after a financial crisis and held large excess reserves. Explain the effect on the credit multiplier.', 'Excess reserves mean less of each deposit is lent out, so the actual multiplier falls well below 1/required reserve ratio and credit creation slows.', '1 mark: less lending; 1 mark: smaller multiplier [2]'),
])
items(t15_4, 'C2', (2, 3, 4), [
    ('Interest rates in {country} are expected to rise next year. Explain the effect on the speculative demand for money.', 'Expected rate rises imply falling bond prices; holding bonds risks capital losses, so people hold more money: speculative demand rises.', '1 mark: bond prices fall; 1 mark: hold money [2]'),
])
essays(t15_2, [
    ('commercial banks, not central banks, control the money supply',
     'Explain how commercial banks create credit.',
     'Most broad money is bank deposits created by lending; credit multiplier.',
     'Central banks influence reserves, interest rates and regulation; demand for loans matters; QE and reserve requirements.'),
], ['Bank lending in {country} has grown by 18% in a year.'])
essays(t15_3, [
    ('an independent central bank is essential for controlling inflation',
     'Explain the functions of a central bank.',
     'Independence gives credibility and anchors expectations.',
     'Supply shocks, fiscal policy and global factors affect inflation; accountability concerns; some dependent central banks succeed.'),
], ['The government of {country} is considering giving its central bank full independence.'])
essays(t15_4, [
    ('inflation is always caused by excessive growth of the money supply',
     'Explain the quantity theory of money.',
     'MV = PY: with stable V and Y, money growth causes inflation.',
     'Cost-push and demand-pull from other sources; V unstable; causality may run from prices to money; Keynesian view.'),
    ('liquidity preference theory explains why monetary policy may be ineffective in a recession',
     'With the aid of a diagram, explain how interest rates are determined in liquidity preference theory.',
     'Liquidity trap: extra money is held, not spent.',
     'QE and forward guidance can work; expectations; other channels (exchange rate, asset prices).'),
], ['The central bank of {country} has increased the money supply rapidly.'])
essays(t15_1, [
    ('cryptocurrencies can perform all the functions of money',
     'Explain the functions and characteristics of money.',
     'Some are accepted as a medium of exchange, are divisible, portable and hard to counterfeit; stablecoins aim at stable value.',
     'Volatile value undermines the store of value and unit of account functions; acceptability is limited; supply and regulation are uncertain.'),
], ['A growing number of shops in {country} accept digital currencies.'])
CHAPTERS[15] = [t15_1, t15_2, t15_3, t15_4]

# ============================================================================ 16 Macroeconomic policy objectives
t16_1 = topic('Macroeconomic objectives revisited', 'macroeconomic objectives revisited', 'inflation targets, external balance and income distribution')
t16_1.fixed('C1', (1, 2, 3), [
    ('An inflation target of 2% ± 1% means the central bank aims for inflation', 'between 1% and 3%, with 2% as the central target', 'Symmetric target band.', ['of exactly 3%', 'below 1%', 'of zero']),
    ('External balance usually means', 'a sustainable current account position over time', 'Avoiding large persistent deficits or surpluses.', ['a zero budget deficit', 'zero unemployment', 'equal imports and exports every month']),
    ('Which is NOT usually one of the main macroeconomic objectives?', 'Maximising the profits of firms', 'Main objectives: growth, low unemployment, low stable inflation, external balance, equitable distribution.',
     ['Low and stable inflation', 'Sustainable economic growth', 'Low unemployment']),
    ('Governments usually prefer low positive inflation rather than zero inflation because', 'it reduces the risk of deflation and allows relative price and wage adjustment', 'Deflation risk; real wages can fall without nominal cuts.',
     ['it increases the value of savings', 'it reduces exports', 'it causes unemployment to rise']),
])
t16_1.fixed('C2', (2, 3, 4), [
    ('Explain why a persistent current account deficit may be a problem.', 'It must be financed by borrowing or asset sales abroad, increasing foreign debt and interest payments; it may lead to a sharp depreciation or loss of confidence; it can indicate a lack of competitiveness.', '1 mark: financing/debt; 1 mark: risk of currency crisis/competitiveness [2]'),
    ('Explain why a more equal distribution of income may be a macroeconomic objective.', 'Reduces poverty and social tension, may raise aggregate demand (poor have higher MPC), improves health and human capital, supports sustainable growth.', '1 mark each reason [2]'),
])


@t16_1.add('C3', (1, 2, 3, 4), 'numerical')
def t16_1_ca(r, D):
    gdp = r.choice([400, 500, 800, 1200])
    ca = r.choice([-40, -30, -24, -16, 12, 30])
    inf = r.choice([1.2, 2.4, 3.8, 5.1, 0.4])
    tgt, band = 2, 1
    c = r.choice(COUNTRIES)
    share = 100 * ca / gdp
    if D <= 2:
        return cq(r, D, f'{c} has GDP of ${gdp} billion and a current account balance of {money(ca)} billion. Calculate the current account balance as a percentage of GDP.', pct(share),
                  f'{ca}/{gdp} × 100 = {pct(share)}.', dis_num(r, share, pct, [-share]))
    within = abs(inf - tgt) <= band
    return {'stem': f'{c} has GDP of ${gdp} billion, a current account balance of {money(ca)} billion and inflation of {num(inf, 1)}%. The inflation target is {tgt}% ± {band}%. Calculate the current account as a % of GDP and assess the economy’s performance against its inflation and external balance objectives.',
            'answer': f'CA = {pct(share)} of GDP. Inflation is {"within" if within else "outside"} the target band. ' + ('A deficit above 3–4% of GDP may be unsustainable.' if share < -3 else ('A small imbalance is likely sustainable.' if abs(share) <= 3 else 'A large surplus may indicate weak domestic demand and cause friction with trading partners.')),
            'key': f'{ca}/{gdp} × 100 [1]; compare inflation with {tgt - band}–{tgt + band}% [1]; judgement on external balance [2].', 'type': 'numerical'}


t16_2 = topic('The Phillips curve and expectations', 'phillips curve', 'short run, long run and the role of expectations')
t16_2.fixed('C1', (1, 2, 3), [
    ('The short-run Phillips curve shows', 'an inverse relationship between unemployment and inflation', 'Lower unemployment associated with higher wage/price inflation.',
     ['a positive relationship between unemployment and inflation', 'the link between growth and unemployment', 'that inflation and unemployment are unrelated']),
    ('The long-run Phillips curve is', 'vertical at the natural rate of unemployment', 'Expectations adjust, so there is no long-run trade-off.', ['horizontal at zero inflation', 'downward sloping', 'upward sloping']),
    ('In the expectations-augmented Phillips curve, an increase in expected inflation causes', 'the short-run Phillips curve to shift upwards', 'Each SRPC is drawn for a given expected inflation rate.',
     ['a movement along the long-run Phillips curve', 'the long-run Phillips curve to shift left', 'unemployment to fall permanently']),
    ('Stagflation is', 'high inflation combined with high unemployment', 'Rightward/upward shifts in SRPC; supply shocks.', ['low inflation and low unemployment', 'falling prices with full employment', 'rapid growth with low inflation']),
])
t16_2.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain why there is no long-run trade-off between inflation and unemployment.', 'Diagram: inflation vertical, unemployment horizontal; LRPC vertical at natural rate Un; SRPC1 for expected inflation 2%. Expansionary policy moves along SRPC1 to lower unemployment and higher inflation (4%). Workers revise expectations to 4%, SRPC shifts up to SRPC2 and unemployment returns to Un with inflation at 4%.', '1 mark: LRPC; 1 mark: movement along SRPC; 1 mark: expectations shift SRPC; 1 mark: return to Un at higher inflation [4]'),
    ('Explain how a supply shock such as a rise in oil prices affects the Phillips curve.', 'Costs rise, causing higher inflation and lower output/employment at the same time: the SRPC shifts up/right (stagflation).', '1 mark: cost-push; 1 mark: SRPC shifts outward [2]'),
])


@t16_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t16_2_pc(r, D):
    un = r.choice([4, 5, 6])
    beta = r.choice([0.5, 1, 1.5, 2])
    pe = r.choice([2, 3, 4])
    u = un - r.choice([1, 1.5, 2])
    pi = pe - beta * (u - un)
    c = r.choice(COUNTRIES)
    stem = f'In {c}, the expectations-augmented Phillips curve is π = πᵉ − {num(beta)}(u − {un}), where π is inflation, πᵉ expected inflation and u the unemployment rate (%).'
    if D <= 2:
        return cq(r, D, stem + f' Expected inflation is {pe}%. Calculate inflation if unemployment is {num(u)}%.', pct(pi), f'π = {pe} − {num(beta)}({num(u)} − {un}) = {pct(pi)}.',
                  dis_num(r, pi, pct, [pe, pe + (un - u), pe - beta * (un - u)]))
    pi2 = pi - beta * (u - un)
    stem += f' Expected inflation is {pe}% and the government holds unemployment at {num(u)}%. (a) Calculate inflation this year. (b) If expectations next year equal this year’s inflation, calculate next year’s inflation. (c) Explain what this implies about holding unemployment below its natural rate.'
    return {'stem': stem, 'answer': f'(a) {pct(pi)} (b) {pct(pi2)} (c) Inflation accelerates each year: unemployment can only be held below the natural rate ({un}%) at the cost of ever-rising inflation; in the long run the Phillips curve is vertical.',
            'key': f'(a) substitution [1]; (b) πᵉ = {pct(pi)} → π = {pct(pi2)} [2]; (c) accelerating inflation / vertical LRPC / natural rate = NAIRU [2].', 'type': 'multi_step'}


t16_3 = topic('Measuring the achievement of macroeconomic objectives', 'measuring the achievement of macroeconomic objectives', 'measuring')
t16_3.fixed('C1', (1, 2, 3), [
    ('A consumer price index is calculated using', 'weighted average price changes of a basket of goods and services', 'Weights reflect shares of household spending.',
     ['the average price of all goods with equal weights', 'only food prices', 'export prices only']),
    ('Real GDP growth is calculated by', 'adjusting nominal GDP growth for inflation', 'Real ≈ nominal growth − inflation (or use a deflator).', ['adding inflation to nominal growth', 'dividing GDP by the population', 'subtracting imports from GDP']),
    ('If nominal GDP rises by 7% and the GDP deflator rises by 3%, real GDP rises by approximately', '4%', '7 − 3 = 4 (exactly 1.07/1.03 − 1 = 3.88%).', ['10%', '2.33%', '21%']),
    ('Which indicator best measures the achievement of the external balance objective?', 'The current account balance as a percentage of GDP', 'Scaled by GDP for comparison.', ['The unemployment rate', 'The Gini coefficient', 'The base interest rate']),
])
t16_3.fixed('C2', (2, 3, 4), [
    ('Explain two limitations of using a consumer price index to measure inflation.', 'The basket and weights may not reflect all households; quality changes and new products are hard to include; substitution bias; excludes some housing costs.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why the unemployment rate may underestimate the true extent of unemployment.', 'Discouraged workers stop searching and leave the labour force; underemployed part-time workers count as employed; hidden unemployment in informal sector.', '1 mark each point [2]'),
])


@t16_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t16_3_cpi(r, D):
    items_ = r.sample([('Food', 30), ('Housing', 25), ('Transport', 15), ('Clothing', 10), ('Energy', 12), ('Leisure', 8), ('Health', 10), ('Education', 5)], 4)
    tot = sum(w for _, w in items_)
    ws = [w * 100 // tot for _, w in items_]
    ws[-1] = 100 - sum(ws[:-1])
    idx = [r.choice([102, 104, 105, 108, 110, 96, 115]) for _ in items_]
    cpi = sum(w * i for w, i in zip(ws, idx)) / 100
    names = [n for n, _ in items_]
    desc = '; '.join(f'{n}: weight {w}, price index {i}' for n, w, i in zip(names, ws, idx))
    if D <= 2:
        return cq(r, D, f'Base year index = 100. {desc}. Calculate the weighted consumer price index.', num(cpi, 2),
                  'CPI = Σ(w × index)/Σw = ' + ' + '.join(f'{w}×{i}' for w, i in zip(ws, idx)) + f' ÷ 100 = {num(cpi, 2)}.', dis_num(r, cpi, lambda x: num(x, 2), [sum(idx) / 4]))
    nom = r.choice([5, 6, 8, 10])
    real = 100 * ((1 + nom / 100) / (cpi / 100) - 1)
    return {'stem': f'Base year index = 100. {desc}. (a) Calculate the weighted price index and the inflation rate. (b) Average nominal wages rose by {nom}% over the same period. Calculate the change in real wages and explain what it means for living standards.',
            'answer': f'(a) CPI = {num(cpi, 2)}; inflation = {pct(cpi - 100, 2)} (b) real wages changed by {pct(real, 2)}: workers’ purchasing power {"rose" if real > 0 else "fell"}.',
            'key': '(a) weighted average [2]; inflation = index − 100 [1]; (b) (1 + nominal)/(1 + inflation) − 1 [2]; interpretation [1].', 'type': 'multi_step'}


def _obj16_c4(r, D):
    d = ctx(r)
    u, inf, ca, g = r.choice([(3.5, 6.2, -5.1, 4.0), (8.2, 1.1, 2.3, 0.5), (5.0, 4.5, -3.2, 2.1)])
    intro = f'Extract: Latest data for {d["country"]}: unemployment {u}%, inflation {inf}% (target 2% ± 1%), current account {ca}% of GDP, real GDP growth {g}%. The natural rate of unemployment is estimated at 5%.'
    parts = [
        lambda r: ('Identify which objectives are being met and which are not.', f'Inflation {"within" if 1 <= inf <= 3 else "outside"} target; unemployment {"below" if u < 5 else "above"} natural rate; current account {"deficit" if ca < 0 else "surplus"} of {abs(ca)}%.', '[3]'),
        lambda r: ('Using a Phillips curve diagram, explain the relationship between the unemployment and inflation data.', ('Unemployment below natural rate with high inflation: movement up SRPC; expectations may shift it.' if u < 5 else 'Unemployment above natural rate with low inflation: movement down SRPC.'), '[3]'),
        lambda r: ('Explain one limitation of the data in judging macroeconomic performance.', 'Revisions, hidden unemployment, CPI biases, informal sector, distribution not shown.', '[2]'),
        lambda r: ('Discuss which objective the government should prioritise.', 'Depends on the size of deviations, conflicts (inflation vs unemployment), sustainability of current account, social costs; justified judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t16_1, t16_2, t16_3], 'C4', (3, 4, 5), 'case', _obj16_c4)
items(t16_2, 'C2', (2, 3, 4), [
    ('Workers in {country} expect inflation to rise from 2% to 5% and negotiate higher pay. Explain the effect on the short-run Phillips curve.', 'Higher expected inflation shifts the SRPC upwards: at each unemployment rate, inflation is now higher.', '1 mark: expectations; 1 mark: SRPC shifts up [2]'),
    ('Unemployment in {country} has fallen to a record low but inflation has not risen. Explain one reason why the Phillips curve relationship may have weakened.', 'Credible inflation targeting anchors expectations; globalisation and online competition hold down prices; weaker union bargaining power; the natural rate may have fallen.', '1 mark: reason; 1 mark: explanation [2]'),
])
items(t16_3, 'C2', (2, 3, 4), [
    ('Nominal GDP in {country} rose by 9% last year. Explain why this does not mean that living standards rose by 9%.', 'Part of the rise is inflation; real GDP growth is lower; population growth reduces per capita gains; distribution and non-market factors also matter.', '1 mark: inflation; 1 mark: population/other [2]'),
])
items(t16_1, 'C2', (2, 3, 4), [
    ('Inflation in {country} has fallen below zero for the first time in decades. Explain why the central bank may be concerned.', 'Deflation raises the real value of debt, may lead consumers to delay purchases, depressing AD; nominal interest rates cannot fall far below zero, limiting policy.', '1 mark each concern [2]'),
])
essays(t16_1, [
    ('low and stable inflation should be the most important macroeconomic objective',
     'Explain the main macroeconomic objectives of a government.',
     'Stable prices support confidence, investment and competitiveness and protect real incomes.',
     'Unemployment and growth may matter more in recession; external balance and inequality; objectives depend on circumstances.'),
], ['The central bank of {country} has missed its inflation target for three years.'])
essays(t16_2, [
    ('the Phillips curve shows that governments must choose between inflation and unemployment',
     'With the aid of a diagram, explain the short-run and long-run Phillips curves.',
     'Short-run trade-off exists.',
     'Expectations make long-run curve vertical; supply shocks and stagflation; flattening curve; supply-side policies can improve both.'),
], ['In {country}, unemployment has fallen to 3% while inflation has risen to 7%.'])
essays(t16_3, [
    ('GDP figures are an adequate measure of a government’s macroeconomic success',
     'Explain how inflation and unemployment are measured.',
     'GDP growth captures output and incomes.',
     'Ignores distribution, informal sector, environment, quality of life; other objectives (inflation, unemployment, external balance) need separate indicators.'),
], ['The government of {country} claims success because GDP grew by 5% last year.'])
CHAPTERS[16] = [t16_1, t16_2, t16_3]

# ============================================================================ 17 Links between macroeconomic problems
t17_1 = topic('Internal and external value of money', 'internal and external value of money', 'relationship between internal and external value')
t17_1.fixed('C1', (1, 2, 3), [
    ('The internal value of money refers to', 'its purchasing power over domestic goods and services', 'Falls when the domestic price level rises.', ['its exchange rate against other currencies', 'the interest rate', 'the quantity of money in circulation']),
    ('The external value of money is measured by', 'the exchange rate', 'Value of the currency in terms of other currencies.', ['the consumer price index', 'the money supply', 'the reserve ratio']),
    ('If a country’s inflation rate is persistently higher than that of its trading partners, under a floating exchange rate its currency is likely to', 'depreciate', 'Exports less competitive, demand for currency falls (PPP).', ['appreciate', 'remain unchanged', 'become fixed']),
    ('If prices rise by 25%, the internal value of money falls by', '20%', 'Purchasing power = 1/1.25 = 0.8.', ['25%', '75%', '125%']),
])
t17_1.fixed('C2', (2, 3, 4), [
    ('Explain how a fall in the internal value of money can lead to a fall in its external value.', 'Domestic inflation makes exports dearer and imports relatively cheaper, so demand for the currency falls and supply rises; under a floating rate it depreciates.', '1 mark: inflation reduces competitiveness; 1 mark: demand/supply of currency; 1 mark: depreciation [3]'),
    ('Explain how a depreciation can reduce the internal value of money.', 'Imported goods and raw materials become more expensive, raising costs and consumer prices (imported inflation), and higher demand for exports adds demand-pull pressure.', '1 mark: dearer imports/costs; 1 mark: higher price level [2]'),
])


@t17_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t17_1_val(r, D):
    inf = r.choice([5, 10, 20, 25, 50])
    pp = 100 / (1 + inf / 100)
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'The price level in {c} rises by {inf}%. Calculate the percentage fall in the internal value (purchasing power) of money.', pct(100 - pp, 2),
                  f'Purchasing power = 100/{num(1 + inf / 100, 2)} = {num(pp, 2)}; fall = {pct(100 - pp, 2)}.', dis_num(r, 100 - pp, lambda x: pct(x, 2), [inf]))
    e0 = r.choice([2, 4, 5, 8, 10])
    fi = r.choice([2, 3])
    e1 = e0 * (1 + inf / 100) / (1 + fi / 100)
    return {'stem': f'Over a year, prices rise by {inf}% in {c} and by {fi}% in its trading partners. At the start of the year, $1 (partner currency) = {e0} units of {c}’s currency. (a) Calculate the fall in the internal value of {c}’s money. (b) Using relative purchasing power parity, calculate the exchange rate needed to keep {c}’s exports equally competitive. (c) Explain what happens to competitiveness if the exchange rate does not change.',
            'answer': f'(a) {pct(100 - pp, 2)} (b) about {num(e1, 2)} units per $1 (a depreciation of {pct(100 * (e1 - e0) / e0, 1)}) (c) {c}’s real exchange rate appreciates: exports become dearer abroad and imports cheaper, worsening the current account.',
            'key': f'(a) 1 − 1/{num(1 + inf / 100, 2)} [1]; (b) {e0} × {num(1 + inf / 100, 2)}/{num(1 + fi / 100, 2)} [2]; (c) real appreciation, loss of competitiveness [2].', 'type': 'multi_step'}


t17_2 = topic('Links between the balance of payments, inflation and growth', 'links between the balance of payments, inflation and economic growth', 'balance of payments')
t17_2.fixed('C1', (1, 2, 3), [
    ('Rapid economic growth driven by consumer spending is likely to', 'worsen the current account as imports rise', 'Higher incomes raise imports (income elasticity of demand for imports).',
     ['improve the current account automatically', 'reduce imports', 'have no effect on trade']),
    ('If the income elasticity of demand for imports is 2 and real incomes rise by 3%, imports will rise by about', '6%', '%ΔM = YED × %ΔY.', ['1.5%', '5%', '3%']),
    ('Demand-pull inflation can worsen the current account because', 'domestic goods become less price competitive and demand for imports rises', 'Higher relative prices reduce exports and raise imports.',
     ['exports become cheaper', 'interest rates fall', 'imports become more expensive']),
    ('Export-led growth occurs when', 'rising exports are the main source of growth in aggregate demand', 'X is an injection; also builds capacity in tradables.', ['imports grow faster than exports', 'consumption falls', 'the currency appreciates sharply']),
])
t17_2.fixed('C2', (2, 3, 4), [
    ('Explain how a current account deficit can slow economic growth.', 'Net imports are a withdrawal from the circular flow, reducing AD; financing may require higher interest rates; loss of domestic industry.', '1 mark: withdrawal/lower AD; 1 mark: financing/higher interest rates [2]'),
    ('Explain how economic growth could improve the current account.', 'If growth is supply-side or export-led, productivity rises, lowering costs and improving competitiveness, so exports grow faster than imports.', '1 mark: productivity/competitiveness; 1 mark: exports rise [2]'),
])


@t17_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t17_2_bop(r, D):
    X, M = r.choice([300, 400, 500]), r.choice([320, 420, 480, 520])
    xs, ms = r.choice([80, 100, 120]), r.choice([60, 90, 110])
    pi_in, pi_out = r.choice([20, 30, 40]), r.choice([40, 50, 60])
    sec = r.choice([-10, -5, 5, 15])
    ca = (X - M) + (xs - ms) + (pi_in - pi_out) + sec
    c = r.choice(COUNTRIES)
    stem = f'Balance of payments data for {c} ($ billion): exports of goods {X}; imports of goods {M}; exports of services {xs}; imports of services {ms}; primary income credits {pi_in}; primary income debits {pi_out}; net secondary income {sec}.'
    if D <= 2:
        return cq(r, D, stem + ' Calculate the trade in goods balance.', money(X - M) + ' billion', f'{X} − {M} = {money(X - M)}.', dis_num(r, X - M, lambda x: money(x) + ' billion', [ca, X - M + xs - ms]))
    stem += ' Calculate the balance on trade in goods and services and the current account balance.'
    ans = f'Goods and services balance = {money(X - M + xs - ms)} billion; current account = {money(ca)} billion.'
    key = f'(X − M) + (Xs − Ms) = {X - M} + {xs - ms} [1]; + primary {pi_in - pi_out} + secondary {sec} = {money(ca)} [2].'
    if D >= 4:
        yed = r.choice([1.5, 2, 2.5])
        g = r.choice([3, 4, 5])
        newM = M * (1 + yed * g / 100)
        stem += f' Real GDP then grows by {g}% and the income elasticity of demand for imports of goods is {num(yed)}. With other items unchanged, calculate the new goods imports and current account balance.'
        ans += f' Imports rise by {num(yed * g, 1)}% to {num(newM, 1)}; current account becomes {money(round(ca - (newM - M), 1))} billion.'
        key += f' %ΔM = {num(yed)} × {g} [1]; new CA [1].'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'multi_step'}


t17_3 = topic('Conflicts between macroeconomic objectives', 'conflicts between macroeconomic objectives in practice', 'conflicts')
t17_3.fixed('C1', (1, 2, 3), [
    ('A conflict between objectives arises when', 'a policy that helps achieve one objective makes another harder to achieve', 'E.g. lower unemployment vs inflation; growth vs current account.',
     ['all objectives are achieved together', 'the government has no objectives', 'inflation and unemployment both fall']),
    ('Raising interest rates to reduce inflation is most likely to conflict with', 'reducing unemployment and promoting growth', 'Higher rates reduce AD.', ['a lower inflation rate', 'a stronger currency', 'higher saving']),
    ('Rapid economic growth may conflict with', 'environmental sustainability and the current account', 'More pollution and imports.', ['higher employment', 'higher tax revenue', 'higher incomes']),
    ('Which policy can reduce inflation and unemployment at the same time in the long run?', 'Successful supply-side policy that increases productivity', 'LRAS shift right lowers price level and raises output.', ['Raising income tax', 'Raising interest rates', 'Increasing tariffs']),
])
t17_3.fixed('C2', (2, 3, 4), [
    ('Explain why there may be a conflict between economic growth and a stable current account.', 'Faster growth raises incomes and imports (high YED for imports), and may raise inflation, reducing competitiveness, so the current account deteriorates.', '1 mark: imports rise; 1 mark: inflation/competitiveness [2]'),
    ('Explain why a policy to reduce income inequality might conflict with economic growth.', 'Higher progressive taxes and benefits may reduce incentives to work, save and invest, and raise the cost of government, slowing growth (though better education can help growth).', '1 mark: incentives; 1 mark: possible counter-argument [2]'),
])
CONFLICTS = [
    ('The central bank of {country} raised interest rates from 2% to 5%. Inflation fell from 7% to 3%, but unemployment rose from 4% to 6%.', 'Low inflation vs low unemployment'),
    ('Rapid consumer-led growth in {country} of 6% a year has been accompanied by a current account deficit rising to 5% of GDP.', 'Economic growth vs external balance'),
    ('A sharp depreciation of {country}’s currency improved its exports but pushed inflation above target.', 'External balance vs low inflation'),
    ('Higher top tax rates in {country} reduced inequality but investment by firms fell.', 'Income redistribution vs economic growth'),
    ('Coal-based expansion in {country} raised GDP growth to 8% while emissions doubled.', 'Economic growth vs environmental sustainability'),
]
CONF_ALL = ['Low inflation vs low unemployment', 'Economic growth vs external balance', 'External balance vs low inflation', 'Income redistribution vs economic growth', 'Economic growth vs environmental sustainability']


@t17_3.add('C3', (1, 2, 3), 'mcq')
def t17_3_class(r, D):
    s, a = r.choice(CONFLICTS)
    opts, ans = mcq(r, a, [x for x in CONF_ALL if x != a])
    return {'stem': fill(s, ctx(r)) + ' Which conflict between macroeconomic objectives is illustrated?', 'options': opts, 'answer': ans, 'key': f'{a}.'}


@t17_3.add('C3', (2, 3, 4, 5), 'numerical')
def t17_3_misery(r, D):
    c1, c2 = r.sample(COUNTRIES, 2)
    u1, i1 = r.choice([3.5, 4.2, 5.0]), r.choice([6.5, 7.8, 9.0])
    u2, i2 = r.choice([7.5, 8.5, 10.0]), r.choice([1.0, 1.8, 2.2])
    m1, m2 = u1 + i1, u2 + i2
    return {'stem': f'{c1}: unemployment {u1}%, inflation {i1}%. {c2}: unemployment {u2}%, inflation {i2}%. Calculate the “misery index” (unemployment + inflation) for each country, and explain what the data suggest about the trade-off each faces.',
            'answer': f'{c1}: {num(m1, 1)}; {c2}: {num(m2, 1)}. {c1} has low unemployment but high inflation (high AD, on the upper part of the SRPC); {c2} has high unemployment and low inflation. Policy to cut one problem risks worsening the other in the short run.',
            'key': '1 mark each index; 1 mark trade-off/Phillips curve interpretation; 1 mark comparison/limitation (weights equal, ignores growth) [4]'}


def _links_c4(r, D):
    d = ctx(r)
    dep = r.choice([10, 15, 20])
    inf0, inf1 = r.choice([2, 3]), r.choice([5, 6, 7])
    intro = f'Extract: {d["country"]}’s currency depreciated by {dep}% last year. Inflation rose from {inf0}% to {inf1}%, partly because 40% of consumer goods are imported. The current account deficit narrowed and export firms expanded output.'
    parts = [
        lambda r: ('Explain the link between the depreciation and the rise in inflation.', 'Imported goods and inputs dearer (cost-push); higher export demand (demand-pull).', '[2]'),
        lambda r: ('Calculate the fall in the internal value of money last year.', f'{pct(100 - 100 / (1 + inf1 / 100), 2)}', f'1 − 1/1.0{inf1} [1]'),
        lambda r: ('Explain why the current account improved.', 'Exports cheaper abroad, imports dearer; Marshall–Lerner condition met after the J-curve period.', '[2]'),
        lambda r: ('Discuss whether the benefits of the depreciation outweigh its costs.', 'Growth and jobs in export sector, better current account vs inflation, lower real wages, higher foreign-debt costs; depends on elasticities and duration.', '[4]'),
        lambda r: ('Explain one conflict between macroeconomic objectives shown in the extract.', 'External balance improving vs inflation rising.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t17_1, t17_2, t17_3], 'C4', (3, 4, 5), 'case', _links_c4)
items(t17_1, 'C2', (2, 3, 4), [
    ('Prices in {country} rose by 15% last year while its exchange rate was fixed. Explain what happened to the internal and external value of its currency and to its competitiveness.',
     'Internal value (purchasing power) fell by about 13%; the nominal external value was unchanged, so the real exchange rate appreciated and exports became less competitive.', '1 mark: internal value fall; 1 mark: real appreciation/competitiveness [2]'),
])
items(t17_2, 'C2', (2, 3, 4), [
    ('{country} has grown rapidly through rising household spending on imported cars and electronics. Explain the likely effect on its current account and why this might limit future growth.',
     'Imports rise with income, worsening the current account; financing the deficit may require higher interest rates or cause a depreciation, slowing future growth.', '1 mark: CA worsens; 1 mark: constraint on growth [2]'),
])
items(t17_3, 'C2', (2, 3, 4), [
    ('The government of {country} wants to cut unemployment and the current account deficit at the same time. Explain why expansionary fiscal policy may make this difficult.', 'Higher AD reduces unemployment but raises incomes and imports and may raise inflation, worsening the current account.', '1 mark: unemployment falls; 1 mark: CA worsens [2]'),
])
essays(t17_1, [
    ('a fall in the external value of a currency will always cause inflation',
     'Explain the relationship between the internal and external value of money.',
     'Depreciation raises import prices and export demand.',
     'Depends on import share, pass-through, spare capacity, inflation expectations and firms absorbing costs.'),
], ['{country}’s currency has lost a quarter of its value against the US dollar in a year.'])
essays(t17_2, [
    ('a current account deficit is always harmful to an economy',
     'Explain the links between the balance of payments and economic growth.',
     'Deficits reduce AD, require financing, risk crises.',
     'Deficits financed by FDI for investment can raise growth; temporary deficits in booms; surplus countries may have weak demand.'),
], ['{country} has run a current account deficit of about 4% of GDP for ten years.'])
essays(t17_3, [
    ('it is impossible for a government to achieve all its macroeconomic objectives at the same time',
     'Explain two conflicts between macroeconomic objectives.',
     'Phillips curve trade-off; growth vs current account; growth vs environment.',
     'Supply-side improvements can achieve several; conflicts are short run; policy mix and credibility; priorities change.'),
], ['The government of {country} has set targets for growth, unemployment, inflation and the current account.'])
CHAPTERS[17] = [t17_1, t17_2, t17_3]

# ============================================================================ 18 Effectiveness of policy options
t18_1 = topic('Effectiveness of fiscal policy', 'effectiveness of fiscal policy', 'time lags, crowding out and the multiplier', 'fiscal policy')
t18_1.fixed('C1', (1, 2, 3), [
    ('Crowding out occurs when', 'increased government borrowing raises interest rates and reduces private sector investment', 'Financial crowding out; also resource crowding out near full capacity.',
     ['government spending increases private investment', 'taxes are cut', 'imports fall']),
    ('Automatic stabilisers are', 'features of the tax and benefit system that change automatically to dampen the business cycle', 'E.g. progressive taxes and unemployment benefits.',
     ['decisions made by the central bank', 'changes in tax rates announced in the budget', 'tariffs on imports']),
    ('The time lag between recognising a recession and implementing a fiscal policy response is called the', 'decision (or implementation) lag', 'Recognition, decision, implementation and effect lags.',
     ['multiplier effect', 'J-curve', 'accelerator']),
    ('A budget deficit occurs when', 'government spending exceeds tax revenue in a year', 'Deficit is a flow; national debt is the stock.', ['tax revenue exceeds government spending', 'imports exceed exports', 'the national debt is repaid']),
    ('A structural budget deficit is one that', 'remains even when the economy is at full employment', 'Cyclical deficit disappears as the economy recovers.', ['disappears when the economy recovers', 'is caused only by a recession', 'is always zero']),
])
t18_1.fixed('C2', (2, 3, 4), [
    ('Explain two reasons why fiscal policy may be ineffective in reducing unemployment.', 'Time lags mean the stimulus arrives too late; crowding out reduces private investment; a small multiplier (high MPM, saving); Ricardian equivalence; unemployment may be structural.', '1 mark each identified, 1 mark each explained [4]'),
    ('Distinguish between a cyclical and a structural budget deficit.', 'Cyclical: due to the downturn (lower tax revenue, higher benefits) and disappears with recovery; structural: spending exceeds revenue even at full employment.', '1 mark each [2]'),
])


@t18_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t18_1_crowd(r, D):
    dg = r.choice([10, 20, 30, 40, 50])
    k = r.choice([1.5, 2, 2.5])
    co = r.choice([20, 25, 40, 50])
    c = r.choice(COUNTRIES)
    gross = dg * k
    net_inj = dg * (1 - co / 100)
    net = net_inj * k
    if D <= 2:
        G, T, gdp = r.choice([400, 450, 500]), r.choice([360, 380, 420]), r.choice([1500, 2000, 2500])
        deficit = G - T
        return cq(r, D, f'In {c}, government spending is ${G} billion, tax revenue ${T} billion and GDP ${gdp} billion. Calculate the budget deficit as a percentage of GDP.', pct(100 * deficit / gdp),
                  f'({G} − {T})/{gdp} × 100 = {pct(100 * deficit / gdp)}.', dis_num(r, 100 * deficit / gdp, pct, [100 * deficit / G]))
    return {'stem': f'The government of {c} increases spending by ${dg} billion, financed by borrowing. The multiplier is {num(k)}. Higher interest rates cause private investment to fall by {co}% of the extra government spending. Calculate the change in national income (a) ignoring crowding out and (b) allowing for it. Explain why crowding out may be smaller in a deep recession.',
            'answer': f'(a) ${num(gross, 1)} billion (b) net injection = {dg} − {num(dg * co / 100, 1)} = {num(net_inj, 1)}; ΔY = ${num(net, 1)} billion. In a deep recession, private investment demand is weak and interest rates are low, so borrowing does not push rates up much.',
            'key': f'(a) {dg} × {num(k)} [1]; (b) net injection × k [2]; explanation: spare saving/low rates/weak investment [2].', 'type': 'multi_step'}


t18_2 = topic('Effectiveness of monetary policy', 'effectiveness of monetary policy', 'monetary policy')
t18_2.fixed('C1', (1, 2, 3), [
    ('The real interest rate is approximately', 'the nominal interest rate minus the rate of inflation', 'Fisher: r ≈ i − π.', ['the nominal rate plus inflation', 'the base rate set by the central bank', 'the interest rate on government bonds']),
    ('A cut in interest rates is likely to', 'increase consumption and investment and cause the currency to depreciate', 'Transmission: borrowing, saving, asset prices, exchange rate.',
     ['reduce borrowing', 'cause the currency to appreciate', 'reduce aggregate demand']),
    ('Monetary policy may be ineffective in a recession because', 'interest rates may already be close to zero and confidence is low', 'Liquidity trap; zero lower bound.', ['interest rates cannot be cut', 'it has no time lags', 'banks always lend more']),
    ('The transmission mechanism of monetary policy refers to', 'the channels through which a change in interest rates affects aggregate demand and inflation', 'Market rates, asset prices, expectations, exchange rate.', ['the process of printing money', 'the setting of tax rates', 'the movement of goods across borders']),
])
t18_2.fixed('C2', (2, 3, 4), [
    ('Explain how a rise in interest rates reduces inflation.', 'Higher borrowing costs and returns to saving reduce consumption and investment; mortgage payments rise; the currency appreciates, lowering import prices and reducing net exports; AD falls and inflationary pressure eases.', '1 mark each channel up to 3 [3]'),
    ('Explain two limitations of monetary policy.', 'Time lags of 18–24 months; zero lower bound; banks may not pass on rate cuts; low confidence; cost-push inflation not addressed; exchange rate effects in open economies.', '1 mark each identified, 1 mark each explained [4]'),
])


@t18_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t18_2_real(r, D):
    i0 = r.choice([1, 2, 3, 4, 5])
    pi = r.choice([2, 3, 6, 8])
    c = r.choice(COUNTRIES)
    if D <= 2:
        real = 100 * ((1 + i0 / 100) / (1 + pi / 100) - 1)
        return cq(r, D, f'The nominal interest rate in {c} is {i0}% and inflation is {pi}%. Calculate the approximate real interest rate.', pct(i0 - pi, 0),
                  f'r ≈ i − π = {i0} − {pi} = {pct(i0 - pi, 0)} (exactly {pct(real, 2)}).', [pct(i0 + pi, 0), pct(pi - i0, 0), pct(i0 * pi, 0), pct(i0, 0), pct(-pi, 0)])
    loan = r.choice([100000, 150000, 200000, 250000])
    di = r.choice([0.5, 1, 1.5, 2])
    extra = loan * di / 100
    inc = r.choice([30000, 40000, 50000])
    return {'stem': f'In {c}, the central bank raises the policy rate by {num(di)} percentage points from {i0}%; inflation is {pi}%. A household has a ${loan:,} interest-only variable-rate mortgage and an income of ${inc:,} a year. Calculate the change in annual interest payments, the new real interest rate (approximately) and the change as a percentage of household income. Explain how this helps to reduce inflation and one reason why the effect might be weak.',
            'answer': f'Interest rises by ${num(extra)} a year ({pct(100 * extra / inc, 2)} of income); real rate ≈ {num(i0 + di - pi, 1)}%. Less disposable income reduces consumption and AD. Weak if most mortgages are fixed-rate, if households save less instead of spending less, or if inflation is cost-push.',
            'key': f'{loan:,} × {num(di)}% [1]; real rate [1]; % of income [1]; AD channel [1]; limitation [1].', 'type': 'multi_step'}


t18_3 = topic('Effectiveness of supply-side policies', 'effectiveness of supply-side policies', 'supply-side policies')
t18_3.fixed('C1', (1, 2, 3), [
    ('Which is a market-based supply-side policy?', 'Reducing the power of trade unions', 'Market-based: deregulation, privatisation, tax cuts, labour market reform. Interventionist: education, training, infrastructure, R&D subsidies.',
     ['Government-funded training schemes', 'Building new roads', 'Subsidising research']),
    ('Supply-side policies are mainly intended to', 'increase the productive capacity of the economy', 'Shift LRAS right.', ['increase aggregate demand in the short run', 'reduce the money supply', 'raise import tariffs']),
    ('A major limitation of supply-side policies is that', 'they often take a long time to have an effect', 'Education and infrastructure have long lags.', ['they always cause inflation', 'they reduce productive capacity', 'they cannot affect unemployment']),
    ('Cutting income tax rates as a supply-side policy aims to', 'increase incentives to work and invest', 'Higher post-tax rewards; Laffer curve argument.', ['reduce aggregate demand', 'increase unemployment benefits', 'reduce the labour force']),
])
t18_3.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain how successful supply-side policies can reduce both inflation and unemployment.', 'AD/AS diagram: LRAS (or Keynesian AS) shifts right; with AD unchanged the price level falls (or rises less) and real output rises, reducing unemployment.', '1 mark: LRAS shift; 1 mark: lower price level; 1 mark: higher output and employment [3]'),
    ('Explain why supply-side policies may increase inequality.', 'Tax cuts for higher earners, weaker unions and benefit cuts may raise incomes at the top while reducing them for the low paid.', '1 mark: policy; 1 mark: distributional effect [2]'),
])


@t18_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t18_3_prod(r, D):
    g0 = r.choice([1.0, 1.5, 2.0])
    g1 = g0 + r.choice([0.5, 1.0])
    y0 = r.choice([500, 800, 1000])
    n = r.choice([10, 15, 20])
    a, b = y0 * (1 + g0 / 100) ** n, y0 * (1 + g1 / 100) ** n
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'Productivity growth in {c} rises from {num(g0, 1)}% to {num(g1, 1)}% a year after a training programme. Using the rule of 70, calculate how many fewer years it takes for output per worker to double.', f'{num(70 / g0 - 70 / g1, 1)} years',
                  f'70/{num(g0, 1)} − 70/{num(g1, 1)} = {num(70 / g0, 1)} − {num(70 / g1, 1)} = {num(70 / g0 - 70 / g1, 1)}.', dis_num(r, 70 / g0 - 70 / g1, lambda x: f'{num(x, 1)} years', [70 / g1]))
    return {'stem': f'Potential GDP in {c} is ${y0} billion and grows at {num(g0, 1)}% a year. Supply-side reforms are expected to raise this to {num(g1, 1)}% a year. Calculate potential GDP after {n} years with and without the reforms, and assess two reasons why the reforms may not achieve this.',
            'answer': f'Without: ${num(a, 1)} billion; with: ${num(b, 1)} billion (a gain of ${num(b - a, 1)} billion). Reasons: long time lags, uncertain effect of tax incentives, poor implementation, weak demand so capacity unused, crowding out of finance.',
            'key': f'Compound growth each case [2]; difference [1]; two reasons with evaluation [2].', 'type': 'multi_step'}


t18_4 = topic('Evaluating the policy mix', 'evaluating the policy mix in a given economy', 'policy mix')
t18_4.fixed('C1', (1, 2, 3), [
    ('The policy mix refers to', 'the combination of fiscal, monetary and supply-side policies used to achieve objectives', 'Policies can complement or offset each other.',
     ['the mix of goods in the CPI', 'the mix of imports and exports', 'the share of public and private ownership']),
    ('Combining a fiscal stimulus with tighter monetary policy is likely to', 'raise interest rates and the exchange rate, reducing the effect of the stimulus', 'Policies working against each other.',
     ['strongly increase AD', 'reduce interest rates', 'cause a depreciation']),
    ('A government facing high inflation and a large budget deficit is most likely to choose', 'contractionary fiscal policy with tighter monetary policy', 'Both reduce AD.', ['tax cuts and lower interest rates', 'higher spending and QE', 'higher tariffs only']),
    ('In a recession with interest rates near zero, economists often recommend', 'a greater role for fiscal policy', 'Monetary policy limited by the zero lower bound.', ['raising interest rates', 'cutting government spending sharply', 'reducing the money supply']),
])
t18_4.fixed('C2', (2, 3, 4), [
    ('Explain why a mix of policies is usually more effective than relying on one policy.', 'Different policies target different causes (demand-side for cyclical problems, supply-side for structural); combining them reduces conflicts and side-effects and allows faster and longer-lasting results.', '1 mark: different causes; 1 mark: offset side-effects [2]'),
    ('Explain how a depreciation of the currency could be combined with fiscal policy to correct a current account deficit without causing a recession.', 'Depreciation switches expenditure towards domestic goods (raising AD); a modest fiscal tightening reduces domestic absorption, freeing capacity for exports and limiting inflation.', '1 mark: expenditure switching; 1 mark: expenditure reducing balances AD [2]'),
])
SCEN = [
    ('high inflation (7%), low unemployment (3.5%) and a current account deficit of 5% of GDP', 'Tighter monetary policy and fiscal restraint reduce AD and imports; supply-side measures raise productivity; risk of slower growth.'),
    ('a recession with unemployment at 9%, inflation at 0.5% and interest rates at 0.25%', 'Fiscal stimulus (infrastructure), QE and forward guidance; supply-side training for long-term unemployed; watch the budget deficit.'),
    ('stagflation: inflation of 8% after an oil price shock and unemployment rising to 7%', 'Monetary policy must anchor expectations while targeted fiscal support protects the poor; supply-side energy measures; conflict between objectives.'),
    ('steady growth but a structural budget deficit of 6% of GDP and rising debt', 'Gradual fiscal consolidation offset by lower interest rates; supply-side reforms to raise trend growth; avoid sharp austerity.'),
]


@t18_4.add('C3', (2, 3, 4, 5), 'explain')
def t18_4_scen(r, D):
    s, a = r.choice(SCEN)
    c = r.choice(COUNTRIES)
    return {'stem': f'{c} is experiencing {s}. Analyse an appropriate mix of fiscal, monetary and supply-side policies for this economy.',
            'answer': a, 'key': '1 mark: diagnosis; 1 mark each for appropriate fiscal, monetary and supply-side elements linked to the problem (max 3); 1 mark: recognition of trade-off or limitation [5]'}


def _pol_c4(r, D):
    d = ctx(r)
    u, inf, debt, ir = r.choice([(8.5, 1.0, 95, 0.5), (4.0, 6.5, 60, 4.0), (6.5, 4.0, 110, 2.0)])
    intro = f'Extract: In {d["country"]}, unemployment is {u}%, inflation {inf}%, public debt {debt}% of GDP and the central bank policy rate {ir}%. Productivity growth has been below 1% a year for a decade.'
    parts = [
        lambda r: ('Calculate the real policy interest rate.', f'{num(ir - inf, 1)}%', f'{ir} − {inf} [1]'),
        lambda r: ('Explain one limitation of fiscal policy in this economy.', ('High debt limits borrowing; crowding out; time lags.' if debt > 80 else 'Time lags and crowding out.'), '[2]'),
        lambda r: ('Explain how monetary policy could be used and one limitation.', ('Rates near zero: limited room; QE as alternative.' if ir < 1 else 'Raise rates to reduce inflation; lags and effect on growth.'), '[3]'),
        lambda r: ('Discuss the most appropriate policy mix for this economy.', 'Diagnosis of main problem; combination of demand and supply-side policies; trade-offs; justified judgement.', '[4]'),
        lambda r: ('Explain why supply-side policies may be needed to raise productivity growth.', 'Low productivity is a supply problem: education, infrastructure, R&D, competition.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t18_1, t18_2, t18_3, t18_4], 'C4', (3, 4, 5), 'case', _pol_c4)
items(t18_1, 'C2', (2, 3, 4), [
    ('The government of {country} announces a large infrastructure programme that will start in two years. Explain why time lags may reduce its effectiveness as a response to the current recession.', 'Recognition, decision and implementation lags mean spending arrives after the economy may have recovered, adding to demand at the wrong time and possibly causing inflation.', '1 mark: lags; 1 mark: pro-cyclical risk [2]'),
])
items(t18_2, 'C2', (2, 3, 4), [
    ('Most mortgages in {country} are on fixed rates for five years. Explain how this affects the impact of an interest rate rise.', 'Few households face higher payments quickly, so the cash-flow effect on consumption is delayed and weaker, lengthening the time lag of monetary policy.', '1 mark: fixed payments; 1 mark: weaker/delayed effect [2]'),
])
items(t18_3, 'C2', (2, 3, 4), [
    ('The government of {country} deregulates the {ind} industry. Explain how this could increase aggregate supply.', 'Lower barriers to entry increase competition, reducing X-inefficiency and costs, encouraging innovation; LRAS shifts right.', '1 mark: competition/efficiency; 1 mark: LRAS shift [2]'),
])
essays(t18_1, [
    ('fiscal policy is more effective than monetary policy in ending a recession',
     'Explain how fiscal policy can be used to influence aggregate demand.',
     'Direct impact on AD, works when rates are near zero, targeted.',
     'Time lags, crowding out, debt constraints, multiplier uncertainty; monetary policy faster to change; depends on situation.'),
], ['{country} has entered a recession while interest rates are already close to zero.'])
essays(t18_2, [
    ('monetary policy is the most effective way to control inflation',
     'Explain the transmission mechanism of monetary policy.',
     'Independent central bank, flexible, affects expectations.',
     'Cost-push inflation, time lags, harms growth and exporters, exchange rate effects; supply-side and fiscal policies also needed.'),
], ['Inflation in {country} has risen to 9%, mainly due to higher energy and food prices.'])
essays(t18_3, [
    ('supply-side policies are the only way to achieve long-term economic growth',
     'Explain the difference between market-based and interventionist supply-side policies.',
     'Only LRAS shifts raise sustainable growth.',
     'Demand needed to use capacity; supply-side slow, costly, uncertain; mix required.'),
], ['Productivity growth in {country} has been weak for a decade.'])
essays(t18_4, [
    ('a government can achieve all its macroeconomic objectives with the right policy mix',
     'Explain what is meant by the policy mix.',
     'Combining policies offsets conflicts.',
     'Trade-offs remain in the short run; external shocks; lags and uncertainty; political constraints.'),
], ['{country} faces rising inflation, high unemployment in some regions and a widening trade deficit.'])
CHAPTERS[18] = [t18_1, t18_2, t18_3, t18_4]

# ============================================================================ 19 Policies to correct current account imbalances
t19_1 = topic('Marshall-Lerner condition and J-curve', 'marshall-lerner condition', 'j-curve effect')
t19_1.fixed('C1', (1, 2, 3), [
    ('The Marshall–Lerner condition states that a depreciation will improve the current account if', 'the sum of the price elasticities of demand for exports and imports is greater than 1', '|PEDx| + |PEDm| > 1.',
     ['the sum of the price elasticities is less than 1', 'imports are price inelastic', 'the exchange rate is fixed']),
    ('The J-curve effect suggests that after a depreciation the current account', 'first worsens and then improves', 'Demand is inelastic in the short run (contracts, habits), more elastic later.',
     ['improves immediately and permanently', 'first improves and then worsens', 'never changes']),
    ('The J-curve occurs mainly because', 'price elasticities of demand for exports and imports are low in the short run', 'Short-run inelasticity: the value of imports rises before volumes adjust.',
     ['exports are always price elastic', 'interest rates rise', 'governments impose tariffs']),
    ('If PED for exports is 0.3 and PED for imports is 0.4, a depreciation will', 'worsen the current account', '0.3 + 0.4 = 0.7 < 1, so Marshall–Lerner is not met.', ['improve the current account', 'have no effect', 'cause the currency to appreciate']),
])
t19_1.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain the J-curve effect.', 'Diagram: current account balance on vertical axis, time on horizontal. After a depreciation at t0, the balance falls (import bills rise in domestic currency, volumes slow to adjust) and then rises above its original level as export and import volumes respond, giving a J shape.', '1 mark: initial worsening and reason; 1 mark: later improvement and reason; 1 mark: diagram [3]'),
    ('Explain why the Marshall–Lerner condition must hold for a depreciation to improve the current account.', 'Depreciation lowers foreign-currency export prices and raises domestic-currency import prices. If demand is inelastic, export volumes rise little and import spending in domestic currency rises; only if combined elasticities exceed 1 do volume changes outweigh price changes.', '1 mark: price effects; 1 mark: volume effects; 1 mark: elasticities > 1 [3]'),
])


@t19_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t19_1_ml(r, D):
    while True:
        ex, im = r.choice([0.3, 0.5, 0.6, 0.8, 1.2]), r.choice([0.2, 0.4, 0.5, 0.7, 0.9])
        if abs(ex + im - 1) >= 0.25:
            break
    dep = r.choice([10, 20])
    c = r.choice(COUNTRIES)
    ok = ex + im > 1
    if D <= 2:
        opts, a = mcq(r, 'The current account improves' if ok else 'The current account worsens', ['The current account improves' if not ok else 'The current account worsens', 'The current account is unchanged', 'The exchange rate appreciates'])
        return {'stem': f'The price elasticity of demand for {c}’s exports is {ex} and for its imports is {im}. Its currency depreciates by {dep}%. In the long run, what happens to the current account (starting from balance)?', 'options': opts, 'answer': a,
                'key': f'{ex} + {im} = {num(ex + im, 1)} {">" if ok else "<"} 1: Marshall–Lerner condition {"met" if ok else "not met"}.'}
    X0 = M0 = r.choice([100, 200, 400])
    xv = ex * dep
    xval = X0 * (1 + xv / 100)
    mval = M0 * (1 + dep / 100) * (1 - im * dep / 100)
    return {'stem': f'{c} has exports and imports each worth {X0} billion in domestic currency. Its currency depreciates by {dep}% against all currencies. PED for exports is {ex} and for imports is {im}. Assume export prices in domestic currency are unchanged and import prices in foreign currency are unchanged. Calculate the new values of exports and imports in domestic currency and the change in the trade balance, and state whether the Marshall–Lerner condition is met.',
            'answer': f'Exports ≈ {num(xval, 1)}; imports ≈ {num(mval, 1)} (domestic price +{dep}%, volume −{num(im * dep, 1)}%); balance changes by {num(xval - mval, 1)} billion. M–L condition {"met" if ok else "not met"} ({ex} + {im} = {num(ex + im, 1)}).',
            'key': f'Export volume +{ex}×{dep}% [1]; import value = {X0} × 1.{dep:02d} × (1 − {num(im * dep / 100, 2)}) [2]; balance change [1]; M–L test [1]. (Approximate: small rounding differences accepted.)', 'type': 'multi_step'}


@t19_1.add('C3', (2, 3, 4), 'numerical')
def t19_1_j(r, D):
    base = r.choice([-10, -8, -5])
    path = [base, base - r.choice([3, 4, 5]), base - r.choice([1, 2]), base + r.choice([1, 2]), base + r.choice([4, 5, 6]), base + r.choice([7, 8, 9])]
    c = r.choice(COUNTRIES)
    tab = table(['Quarter', 'Current account ($bn)'], list(zip(['Q0 (depreciation)', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5'], path)))
    return {'stem': f'{c}’s currency depreciated sharply in Q0. {tab}. Describe the pattern shown, explain why it occurs and calculate the overall change in the current account between Q0 and Q5.',
            'answer': f'J-curve: the balance worsens to {path[1]} in Q1 then improves, ending at {path[-1]}, an improvement of {path[-1] - path[0]} billion. Short-run inelastic demand means import bills rise before volumes respond; later elasticities rise and the Marshall–Lerner condition is met.',
            'key': '1 mark: initial deterioration; 1 mark: later improvement; 1 mark: elasticity explanation; 1 mark: overall change [4]'}


t19_2 = topic('Effects of policies on the current account', 'effects of fiscal, monetary, supply-side and protectionist policies on the current account', 'expenditure switching')
t19_2.fixed('C1', (1, 2, 3), [
    ('An expenditure-switching policy aims to', 'shift spending from imports to domestically produced goods', 'Depreciation, tariffs, quotas, subsidies to exporters.',
     ['reduce total spending in the economy', 'increase spending on imports', 'cut government spending']),
    ('An expenditure-reducing policy to cut a current account deficit is', 'raising income tax to reduce domestic demand', 'Lower AD → lower imports.', ['imposing a tariff on imports', 'devaluing the currency', 'subsidising exporters']),
    ('A disadvantage of using tariffs to reduce a current account deficit is that', 'trading partners may retaliate', 'Also inefficiency, higher prices, WTO rules.', ['they make imports cheaper', 'they increase consumer choice', 'they reduce government revenue']),
    ('Higher interest rates are most likely to affect the current account by', 'reducing domestic demand for imports but appreciating the currency', 'Two opposing effects.', ['increasing imports only', 'causing a depreciation', 'having no effect on trade']),
])
t19_2.fixed('C2', (2, 3, 4), [
    ('Explain how supply-side policies could improve the current account in the long run.', 'Higher productivity and innovation reduce unit costs and improve quality, making exports more competitive and domestic goods better substitutes for imports.', '1 mark: productivity/costs; 1 mark: competitiveness of exports and import substitutes [2]'),
    ('Explain why expenditure-reducing policies may be politically unpopular.', 'They lower AD, raising unemployment and slowing growth, so they reduce imports at the cost of lower living standards.', '1 mark: lower AD; 1 mark: unemployment/growth cost [2]'),
])


@t19_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t19_2_tariff(r, D):
    pw = r.choice([100, 200, 250, 400])
    t = r.choice([10, 15, 20, 25])
    qd0, qs0 = r.choice([1000, 1200, 1500]), r.choice([300, 400, 500])
    ped, pes = r.choice([1.0, 1.5, 2.0]), r.choice([0.5, 1.0])
    qd1 = qd0 * (1 - ped * t / 100)
    qs1 = qs0 * (1 + pes * t / 100)
    m0, m1 = qd0 - qs0, qd1 - qs1
    g = r.choice(['steel', 'cars', 'textiles', 'tyres'])
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'The world price of {g} is ${pw} per unit. {c} imposes a {t}% tariff. Calculate the domestic price after the tariff.', money(pw * (1 + t / 100)), f'{pw} × 1.{t:02d} = {money(pw * (1 + t / 100))}.',
                  dis_num(r, pw * (1 + t / 100), money, [pw + t, pw * t / 100]))
    rev = m1 * pw * t / 100
    return {'stem': f'{c} imports {g} at a world price of ${pw}. Domestic demand is {qd0:,} units and domestic supply {qs0} units. A {t}% tariff is imposed; PED for {g} is {num(ped)} and PES for domestic producers is {num(pes)}. Calculate the new domestic price, quantities demanded and supplied, imports before and after, and tariff revenue. Explain one disadvantage of the tariff.',
            'answer': f'Price ${num(pw * (1 + t / 100), 2)}; Qd {num(qd1)}; Qs {num(qs1)}; imports fall from {m0} to {num(m1)}; tariff revenue {money(round(rev))}. Disadvantages: higher prices for consumers, inefficient domestic producers protected, retaliation, deadweight losses.',
            'key': f'Price [1]; %ΔQd = −{num(ped)}×{t}% and %ΔQs = {num(pes)}×{t}% [2]; imports = Qd − Qs [1]; revenue = imports × tariff per unit (${num(pw * t / 100)}) [1]; disadvantage [1].', 'type': 'multi_step'}


items(t19_2, 'C3', (2, 3, 4), [
    ('{country} has a current account deficit of 6% of GDP caused by a consumer boom. Analyse whether expenditure-reducing or expenditure-switching policy would be more appropriate.',
     'The cause is excess domestic demand, so expenditure-reducing policy (higher taxes or interest rates) directly reduces imports and inflationary pressure; expenditure switching (depreciation) adds to demand when the economy is already overheating, raising inflation. A combination may be needed if competitiveness is also weak.',
     '1 mark: diagnosis; 1 mark: expenditure-reducing analysis; 1 mark: switching analysis; 1 mark: judgement [4]'),
])

t19_3 = topic('Policies to correct a current account surplus', 'policies to correct a current account surplus', 'surplus')
t19_3.fixed('C1', (1, 2, 3), [
    ('A country with a persistent current account surplus could reduce it by', 'allowing its currency to appreciate', 'Exports dearer, imports cheaper.', ['devaluing its currency', 'raising tariffs', 'cutting domestic demand']),
    ('A persistent current account surplus may be a problem because', 'it may reflect weak domestic demand and can provoke protectionism by trading partners', 'Also: inflationary pressure, opportunity cost of lower consumption.',
     ['it always causes unemployment', 'it reduces foreign exchange reserves', 'it lowers the exchange rate']),
    ('Expansionary fiscal policy reduces a current account surplus because', 'higher domestic demand increases imports', 'Raise absorption.', ['it reduces imports', 'it increases exports', 'it lowers the exchange rate']),
])
t19_3.fixed('C2', (2, 3, 4), [
    ('Explain two policies a country could use to reduce a current account surplus.', 'Allow currency appreciation; expansionary fiscal policy to raise domestic demand; lower interest rates; removal of import restrictions; policies to reduce high household saving (social safety nets).', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why a current account surplus could lead to inflation.', 'Net exports add to AD; inflows of foreign currency may increase the domestic money supply if the central bank buys foreign currency to hold the exchange rate down.', '1 mark: AD; 1 mark: money supply [2]'),
])


@t19_3.add('C3', (2, 3, 4, 5), 'numerical')
def t19_3_sur(r, D):
    gdp = r.choice([1000, 2000, 4000])
    s = r.choice([6, 7, 8, 10])
    app = r.choice([10, 15, 20])
    ex = r.choice([0.6, 0.8, 1.0])
    X = gdp * r.choice([0.3, 0.4])
    fall = X * ex * app / 100
    c = r.choice(COUNTRIES)
    return {'stem': f'{c} has GDP of ${gdp:,} billion and a current account surplus of {s}% of GDP. Exports are ${num(X)} billion. Its currency appreciates by {app}% and the price elasticity of demand for its exports is {num(ex)}. Calculate the surplus in $ billion and the approximate fall in export volumes (valued at the original domestic price). Explain one other policy that could reduce the surplus.',
            'answer': f'Surplus = ${num(gdp * s / 100)} billion; exports fall by about {num(ex * app, 1)}% ≈ ${num(fall, 1)} billion. Other policy: fiscal expansion or lower saving incentives to raise domestic demand and imports.',
            'key': f'{s}% × {gdp:,} [1]; %Δvolume = {num(ex)} × {app}% [1]; value [1]; policy explained [2].', 'type': 'multi_step'}


def _ca_c4(r, D):
    d = ctx(r)
    ca = r.choice([-4.5, -5.5, -6.8])
    pedx, pedm = r.choice([(0.4, 0.3), (0.8, 0.6), (0.5, 0.7)])
    intro = f'Extract: {d["country"]} has a current account deficit of {abs(ca)}% of GDP. The government is considering a 15% devaluation of its fixed exchange rate. Estimated price elasticities of demand are {pedx} for exports and {pedm} for imports in the long run, but much lower in the first year.'
    parts = [
        lambda r: ('State whether the Marshall–Lerner condition is met.', f'{pedx} + {pedm} = {num(pedx + pedm, 1)}: ' + ('met' if pedx + pedm > 1 else 'not met'), '[2]'),
        lambda r: ('With the aid of a diagram, explain the likely path of the current account after the devaluation.', 'J-curve: worsens initially due to low short-run elasticities, then improves if M–L condition holds.', '[3]'),
        lambda r: ('Explain one expenditure-reducing policy that could be used instead.', 'Higher taxes/interest rates reduce AD and imports.', '[2]'),
        lambda r: ('Discuss whether devaluation is the best way to reduce the deficit.', 'Depends on elasticities, inflation (imported), retaliation, competitiveness; supply-side improvements more lasting; expenditure reducing causes unemployment.', '[4]'),
        lambda r: ('Explain why a fall in export prices may increase export revenue.', 'If demand is price elastic, volume rise outweighs price fall.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t19_1, t19_2, t19_3], 'C4', (3, 4, 5), 'case', _ca_c4)
items(t19_1, 'C2', (2, 3, 4), [
    ('Many of {country}’s imports are bought under contracts fixed in US dollars for 12 months. Explain why a depreciation may worsen its current account at first.', 'Import volumes cannot change quickly, but each dollar now costs more domestic currency, so the import bill rises before export volumes respond: the start of the J-curve.', '1 mark: fixed volumes; 1 mark: higher domestic-currency cost [2]'),
])
items(t19_3, 'C2', (2, 3, 4), [
    ('{country} has had a current account surplus of 8% of GDP for a decade. Explain why its trading partners may object.', 'The surplus implies deficits elsewhere, reducing demand and jobs in partner economies; they may suspect an undervalued currency or protectionism and threaten retaliation.', '1 mark: deficits/jobs elsewhere; 1 mark: undervaluation/retaliation [2]'),
    ('Explain how higher government spending on social insurance in {country} might reduce its current account surplus.', 'Households need to save less for emergencies, so consumption (including imports) rises, raising domestic demand relative to output.', '1 mark: less precautionary saving; 1 mark: higher imports [2]'),
])
items(t19_2, 'C2', (2, 3, 4), [
    ('The central bank of {country} raises interest rates. Explain the two opposing effects on the current account.', 'Lower domestic spending reduces imports (improves CA); but higher rates attract hot money, appreciating the currency, making exports dearer and imports cheaper (worsens CA).', '1 mark each effect [2]'),
])
essays(t19_1, [
    ('a depreciation of the currency will always improve the current account',
     'Explain the Marshall–Lerner condition and the J-curve effect.',
     'Exports cheaper, imports dearer; improvement if M–L holds.',
     'Short-run J-curve, low elasticities, inflation eroding competitiveness, non-price factors, import content of exports.'),
], ['{country}’s currency has fallen by 20% but its trade deficit has widened.'])
essays(t19_2, [
    ('protectionism is the most effective way to reduce a current account deficit',
     'Explain the difference between expenditure-reducing and expenditure-switching policies.',
     'Tariffs and quotas quickly reduce imports.',
     'Retaliation, inefficiency, higher prices, WTO rules; does not address competitiveness; supply-side and exchange rate policies.'),
], ['The government of {country} plans to impose tariffs on imported manufactured goods.'])
essays(t19_3, [
    ('a current account surplus is always beneficial for a country',
     'Explain the causes of a current account surplus.',
     'Strong exports, jobs, foreign assets.',
     'Weak domestic consumption, undervalued currency, protectionist reaction, inflation pressure; opportunity cost of saving abroad.'),
], ['{country} has run large current account surpluses based on manufactured exports.'])
CHAPTERS[19] = [t19_1, t19_2, t19_3]

# ============================================================================ 20 Exchange rates
t20_1 = topic('Floating and fixed exchange rate systems', 'comparing floating and fixed exchange rate systems', 'advantages and disadvantages', 'floating and fixed')
t20_1.fixed('C1', (1, 2, 3), [
    ('In a floating exchange rate system, the exchange rate is determined by', 'the demand for and supply of the currency', 'No official intervention to target a rate.', ['the central bank setting a fixed rate', 'the government’s budget', 'the IMF']),
    ('To maintain a fixed exchange rate when the currency is under downward pressure, the central bank can', 'buy its own currency using foreign exchange reserves', 'Or raise interest rates.', ['sell its own currency', 'cut interest rates', 'print more money']),
    ('An advantage of a fixed exchange rate is', 'certainty for traders and investors', 'Reduces exchange-rate risk; discipline on inflation.', ['automatic correction of current account deficits', 'independent monetary policy', 'no need for reserves']),
    ('An advantage of a floating exchange rate is that', 'monetary policy can be used for domestic objectives', 'No need to target the exchange rate; automatic adjustment of BoP.', ['there is no exchange rate uncertainty', 'it requires large reserves', 'it prevents speculation']),
    ('A managed float is a system in which', 'the rate is mainly market-determined but the central bank intervenes at times', 'Dirty float.', ['the rate never changes', 'the currency is replaced by the dollar', 'there is no central bank']),
])
t20_1.fixed('C2', (2, 3, 4), [
    ('With the aid of a diagram, explain how an increase in demand for a country’s exports affects a floating exchange rate.', 'Diagram: price of currency (in foreign currency) on vertical axis, quantity of currency horizontal. Foreigners need more of the currency to pay for exports, so demand shifts right and the exchange rate appreciates.', '1 mark: diagram; 1 mark: demand shifts right; 1 mark: appreciation [3]'),
    ('Explain two disadvantages of a fixed exchange rate system.', 'Loss of independent monetary policy; need for large reserves; risk of speculative attack; misalignment causing deficits or unemployment; no automatic BoP adjustment.', '1 mark each identified, 1 mark each explained [4]'),
])
items(t20_1, 'C3', (2, 3, 4), [
    ('Speculators expect {country}’s fixed exchange rate to be devalued and sell its currency heavily. Analyse the options available to the central bank and their consequences.',
     'Buy the currency with reserves (reserves may run out); raise interest rates to attract inflows (harms growth and employment); impose capital controls; or devalue/float (loss of credibility, imported inflation).',
     '1 mark each option analysed (up to 3); 1 mark judgement [4]'),
    ('Interest rates in {country} rise relative to those in {country2}. Analyse the likely effect on {country}’s floating exchange rate and its exports.',
     'Higher rates attract financial inflows (hot money), raising demand for the currency: appreciation. Exports become dearer in foreign currency and imports cheaper, so export volumes may fall, depending on PED.',
     '1 mark: capital inflows; 1 mark: appreciation; 1 mark: effect on exports; 1 mark: elasticity caveat [4]'),
])

t20_2 = topic('Nominal, real and trade-weighted exchange rates', 'nominal, real and trade-weighted exchange rates', 'real exchange rate', 'trade-weighted')
t20_2.fixed('C1', (1, 2, 3), [
    ('The real exchange rate adjusts the nominal exchange rate for', 'differences in price levels between countries', 'Real = nominal × (domestic price index / foreign price index).', ['differences in interest rates', 'transport costs only', 'tariffs']),
    ('A trade-weighted exchange rate index measures', 'the value of a currency against a basket of currencies weighted by trade shares', 'Effective exchange rate.', ['the value against the US dollar only', 'the price of gold', 'the inflation rate']),
    ('If a currency’s nominal value is unchanged but domestic inflation is higher than abroad, its real exchange rate', 'appreciates', 'Domestic goods become relatively dearer.', ['depreciates', 'stays the same', 'becomes zero']),
    ('A rise in the real exchange rate means that the country’s goods have become', 'less price competitive internationally', 'Real appreciation.', ['more price competitive', 'cheaper abroad', 'of higher quality']),
])
t20_2.fixed('C2', (2, 3, 4), [
    ('Explain why the real exchange rate is a better measure of competitiveness than the nominal exchange rate.', 'It accounts for relative inflation: even if the nominal rate is constant, higher domestic inflation makes exports dearer, so competitiveness depends on both.', '1 mark: inflation adjustment; 1 mark: link to competitiveness [2]'),
    ('Explain why a trade-weighted index is more useful than a single bilateral exchange rate.', 'A country trades with many partners; the TWI shows the overall change in the currency’s value, weighted by the importance of each partner in trade.', '1 mark: many partners; 1 mark: weighted [2]'),
])


@t20_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t20_2_real(r, D):
    e0 = r.choice([1.5, 2, 4, 5, 8])
    dch = r.choice([-10, -5, 0, 5, 10])
    e1 = e0 * (1 + dch / 100)
    pd, pf = r.choice([104, 106, 108, 110]), r.choice([101, 102, 103])
    c = r.choice(COUNTRIES)
    rer0, rer1 = e0, e1 * pd / pf
    if D <= 2:
        a = 100 * ((1 + dch / 100) * pd / pf - 1)
        return cq(r, D, f'{c}’s nominal exchange rate changes by {dch:+d}% against its main partner. Domestic prices rise by {pd - 100}% and foreign prices by {pf - 100}%. Calculate the approximate percentage change in the real exchange rate.', pct(a, 1),
                  f'(1 {"+" if dch >= 0 else "−"} {abs(dch) / 100}) × {pd}/{pf} − 1 = {pct(a, 1)} (≈ {dch} + {pd - 100} − {pf - 100}).', dis_num(r, a, lambda x: pct(x, 1), [dch, dch - (pd - pf)]))
    w = r.choice([(50, 30, 20), (40, 40, 20), (60, 25, 15)])
    ch = [r.choice([-6, -4, -2, 2, 4, 8]) for _ in range(3)]
    twi = sum(wi * (100 + ci) for wi, ci in zip(w, ch)) / 100
    parts = ['A', 'B', 'C']
    return {'stem': f'{c} trades with three partners with trade weights of {w[0]}%, {w[1]}% and {w[2]}%. Over a year its currency changes by {ch[0]:+d}%, {ch[1]:+d}% and {ch[2]:+d}% against partners {parts[0]}, {parts[1]} and {parts[2]}. (a) Calculate the trade-weighted index (start = 100). (b) Domestic prices rose {pd - 100}% and partners’ prices {pf - 100}% on average. Calculate the change in the real effective exchange rate and explain what it means for competitiveness.',
            'answer': f'(a) TWI = {num(twi, 2)} (b) real ≈ {num(twi, 2)} × {pd}/{pf} = {num(twi * pd / pf, 2)}, a {pct(twi * pd / pf - 100, 2)} change: ' + ('a real appreciation, so competitiveness worsens.' if twi * pd / pf > 100 else 'a real depreciation, so competitiveness improves.'),
            'key': '(a) Σ weight × index [2]; (b) adjust by relative prices [2]; interpretation [1].', 'type': 'multi_step'}


@t20_2.add('C3', (1, 2, 3, 4), 'numerical')
def t20_2_conv(r, D):
    e = r.choice([1.25, 1.5, 2, 4, 5, 8])
    e2 = e * r.choice([0.8, 0.9, 1.1, 1.2])
    p = r.choice([20, 40, 50, 100, 200])
    c = r.choice(COUNTRIES)
    stem = f'The exchange rate between the {c} krona (K) and the US dollar is $1 = K{num(e, 2)}. A {c} product sells for K{p * e:.0f} at home.'
    pd = p
    pd2 = p * e / e2
    if D <= 2:
        return cq(r, D, stem + ' Calculate its price in US dollars.', f'${num(pd, 2)}', f'K{p * e:.0f}/{num(e, 2)} = ${num(pd, 2)}.', dis_num(r, pd, lambda x: f'${num(x, 2)}', [p * e * e]))
    word = 'appreciates' if e2 < e else 'depreciates'
    return {'stem': stem + f' The exchange rate changes to $1 = K{num(e2, 2)}. Calculate the dollar price before and after, state whether the krona has appreciated or depreciated, and explain the likely effect on export revenue.',
            'answer': f'Before ${num(pd, 2)}; after ${num(pd2, 2)}. The krona {word} by {pct(100 * abs(e / e2 - 1), 1)}. ' + ('Dollar price rises, so export volumes fall; revenue depends on PED.' if e2 < e else 'Dollar price falls, so export volumes rise; revenue in krona rises if demand is elastic.'),
            'key': 'Price conversion each rate [2]; correct appreciation/depreciation [1]; PED-based effect on revenue [1].', 'type': 'numerical'}


t20_3 = topic('Purchasing power parity', 'purchasing power parity', 'ppp')
t20_3.fixed('C1', (1, 2, 3), [
    ('Purchasing power parity theory states that, in the long run, exchange rates adjust so that', 'identical goods cost the same in different countries when prices are converted into a common currency', 'Law of one price applied to baskets.',
     ['interest rates are equal in all countries', 'all countries have the same GDP', 'trade balances are zero']),
    ('If a burger costs $5 in the USA and 20 units in Country X, the PPP exchange rate is', '$1 = 4 units of X’s currency', '20/5 = 4.', ['$1 = 0.25 units', '$1 = 25 units', '$1 = 100 units']),
    ('If the market exchange rate is $1 = 6 units but the PPP rate is $1 = 4 units, the currency is', 'undervalued against the dollar', 'Market rate gives more units per dollar than PPP: goods are cheap in dollar terms.', ['overvalued against the dollar', 'at its PPP value', 'fixed']),
    ('PPP-adjusted GDP figures are used to', 'compare living standards between countries by allowing for different price levels', 'Market exchange rates do not reflect domestic purchasing power.', ['measure inflation', 'calculate the exchange rate for tourists', 'set interest rates']),
])
t20_3.fixed('C2', (2, 3, 4), [
    ('Explain two reasons why exchange rates may not move to purchasing power parity.', 'Non-traded goods and services; transport costs and tariffs; capital flows and speculation dominate currency markets; product differentiation; government intervention.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why GDP per head at market exchange rates may understate living standards in low-income countries.', 'Non-traded goods and services (haircuts, local food, housing) are much cheaper, so a dollar buys more there than market rates suggest; PPP adjusts for this.', '1 mark: cheaper non-traded goods; 1 mark: PPP correction [2]'),
])


@t20_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t20_3_ppp(r, D):
    pus = r.choice([4, 5, 5.5, 6])
    ppp = r.choice([2, 4, 5, 8, 10, 20])
    plocal = pus * ppp
    mkt = ppp * r.choice([0.8, 1.25, 1.5, 0.9, 1.1])
    c = r.choice(COUNTRIES)
    item = r.choice(['burger', 'cup of coffee', 'cinema ticket', 'basket of groceries'])
    if D <= 2:
        return cq(r, D, f'A {item} costs ${num(pus, 2)} in the USA and {num(plocal, 2)} units of local currency in {c}. Calculate the implied PPP exchange rate.', f'$1 = {num(ppp, 2)} units',
                  f'{num(plocal, 2)}/{num(pus, 2)} = {num(ppp, 2)}.', [f'$1 = {num(1 / ppp, 3)} units', f'$1 = {num(plocal * pus, 2)} units', f'$1 = {num(mkt, 2)} units'])
    usd = plocal / mkt
    mis = 100 * (usd - pus) / pus
    return {'stem': f'A {item} costs ${num(pus, 2)} in the USA and {num(plocal, 2)} units in {c}. The market exchange rate is $1 = {num(mkt, 2)} units. Calculate the implied PPP rate, the dollar price of the {item} in {c}, and the percentage by which {c}’s currency is over- or undervalued. Explain one limitation of this method.',
            'answer': f'PPP rate $1 = {num(ppp, 2)}; dollar price ${num(usd, 2)}; currency {"overvalued" if mis > 0 else "undervalued"} by {pct(abs(mis), 1)}. Limitation: one product; includes non-traded inputs (rent, wages), taxes and tastes differ.',
            'key': f'PPP = local/US price [1]; dollar price = local/market rate [1]; (dollar price − US price)/US price [2]; limitation [1].', 'type': 'multi_step'}


def _fx_c4(r, D):
    d = ctx(r)
    e0, e1 = r.choice([(4.0, 5.0), (2.0, 2.6), (8.0, 10.0)])
    intro = f'Extract: {d["country"]} abandoned its fixed exchange rate of $1 = {num(e0)} units last year after its foreign exchange reserves fell sharply. The currency now floats and trades at $1 = {num(e1)} units. Inflation has risen and exporters report higher orders.'
    parts = [
        lambda r: ('Calculate the percentage depreciation of the currency against the dollar.', f'{pct(100 * (1 - e0 / e1), 1)} (the dollar has appreciated by {pct(100 * (e1 / e0 - 1), 1)})', '[2]'),
        lambda r: ('Explain why reserves fell under the fixed rate.', 'The central bank sold dollars to buy its currency to defend the peg against excess supply/speculation.', '[2]'),
        lambda r: ('With the aid of a diagram, explain how the floating rate was determined.', 'Demand and supply of the currency; excess supply at the old peg; new lower equilibrium.', '[3]'),
        lambda r: ('Discuss whether a floating exchange rate is better for this economy than a fixed rate.', 'Floating: automatic adjustment, monetary independence, no reserves needed; but volatility, imported inflation, debt in dollars; fixed gives certainty and anti-inflation discipline.', '[4]'),
        lambda r: ('Explain why inflation has risen.', 'Import prices rise in domestic currency; export demand adds to AD.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t20_1, t20_2, t20_3], 'C4', (3, 4, 5), 'case', _fx_c4)
items(t20_2, 'C2', (2, 3, 4), [
    ('{country}’s nominal exchange rate against the dollar has not changed for three years, but its inflation has been 6% a year compared with 2% in the USA. Explain what has happened to its real exchange rate.', 'Domestic prices rose faster than US prices, so the real exchange rate appreciated by roughly 4% a year: its goods became less competitive.', '1 mark: real appreciation; 1 mark: reason/competitiveness [2]'),
])
items(t20_3, 'C2', (2, 3, 4), [
    ('GDP per head in {country} is $2,000 at market exchange rates but $6,000 at PPP. Explain why the figures differ.', 'Prices of many goods and especially non-traded services are lower in {country}, so a dollar converted at the market rate buys more there; PPP adjusts for these price differences.', '1 mark: lower price level; 1 mark: PPP adjustment [2]'),
])
items(t20_1, 'C2', (2, 3, 4), [
    ('Tourism to {country} increases sharply. Explain, using demand and supply, the effect on its floating exchange rate.', 'Tourists must buy the currency to spend in {country}, so demand for the currency shifts right and the exchange rate appreciates.', '1 mark: demand shift; 1 mark: appreciation [2]'),
])
essays(t20_1, [
    ('a floating exchange rate is always better than a fixed exchange rate',
     'Explain how exchange rates are determined in a floating system.',
     'Automatic BoP adjustment, monetary independence, no reserves needed.',
     'Volatility and uncertainty for trade and investment, speculation, imported inflation; fixed rates provide discipline; managed float as compromise.'),
], ['{country} is debating whether to peg its currency to the US dollar.'])
essays(t20_2, [
    ('changes in the real exchange rate are more important than changes in the nominal exchange rate',
     'Explain the difference between nominal, real and trade-weighted exchange rates.',
     'Real rate measures competitiveness.',
     'Nominal rates affect debt servicing, capital flows and import prices immediately; both needed.'),
], ['{country}’s currency has been stable against the dollar but inflation is much higher than in its trading partners.'])
essays(t20_3, [
    ('purchasing power parity theory explains movements in exchange rates',
     'Explain purchasing power parity theory.',
     'Long-run tendency for inflation differentials to be offset by exchange rate changes.',
     'Short-run dominated by capital flows, interest rates and speculation; non-traded goods; transport costs; useful for comparing living standards.'),
], ['A newspaper claims that {country}’s currency is 30% undervalued.'])
CHAPTERS[20] = [t20_1, t20_2, t20_3]

# ============================================================================ 21 Economic development
t21_1 = topic('Economic growth versus economic development', 'economic growth versus economic development', 'economic development')
t21_1.fixed('C1', (1, 2, 3), [
    ('Economic development is best described as', 'an improvement in living standards, including health, education, freedom and reduced poverty', 'Broader than growth in real GDP.',
     ['an increase in real GDP only', 'an increase in exports', 'a rise in the money supply']),
    ('Which could occur with economic growth but without economic development?', 'Real GDP rises but the gains go mainly to a small elite while poverty persists', 'Growth may be unequal or environmentally destructive.',
     ['Life expectancy and literacy both rise', 'Poverty falls and incomes rise for most people', 'Access to clean water increases']),
    ('Real GDP per head is calculated by', 'dividing real GDP by the population', 'Adjusts for population size.', ['dividing nominal GDP by the price level', 'multiplying GDP by population', 'subtracting imports from GDP']),
    ('If real GDP grows by 4% and population by 3%, real GDP per head grows by approximately', '1%', '1.04/1.03 − 1 ≈ 0.97%.', ['7%', '12%', '1.33%']),
])
t21_1.fixed('C2', (2, 3, 4), [
    ('Explain why economic growth is a necessary but not a sufficient condition for economic development.', 'Growth provides resources to improve health, education and infrastructure, but whether development occurs depends on how income is distributed and used, and on environmental and social impacts.', '1 mark: growth provides resources; 1 mark: distribution/use determines development [2]'),
    ('Explain two ways in which economic development can promote further economic growth.', 'Better health and education raise labour productivity; reduced poverty increases saving and demand; better institutions attract investment.', '1 mark each identified, 1 mark each explained [4]'),
])


@t21_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_1_pc(r, D):
    g = r.choice([3, 4, 5, 6, 7])
    p = r.choice([1, 1.5, 2, 2.5, 3])
    pc = 100 * ((1 + g / 100) / (1 + p / 100) - 1)
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'Real GDP in {c} grows by {g}% and population by {num(p, 1)}%. Calculate the growth of real GDP per head.', pct(pc, 2), f'1.0{g}/{num(1 + p / 100, 3)} − 1 = {pct(pc, 2)} (≈ {num(g - p, 1)}%).',
                  dis_num(r, pc, lambda x: pct(x, 2), [g + p, g, g / p]))
    nom = g + r.choice([3, 5, 8])
    inf = nom - g
    return {'stem': f'In {c}, nominal GDP grew by {nom}% last year, the GDP deflator rose by {inf}% and the population grew by {num(p, 1)}%. Life expectancy and school enrolment were unchanged, while the share of income going to the top 10% rose. Calculate the growth in real GDP and real GDP per head, and explain whether the country has experienced economic development.',
            'answer': f'Real GDP ≈ {pct(100 * ((1 + nom / 100) / (1 + inf / 100) - 1), 2)}; real GDP per head ≈ {pct(100 * ((1 + nom / 100) / (1 + inf / 100) / (1 + p / 100) - 1), 2)}. Growth has occurred, but with unchanged health and education and rising inequality, there is little evidence of development.',
            'key': 'Deflate nominal growth [1]; adjust for population [1]; distinguish growth from development using the indicators [2].', 'type': 'multi_step'}


t21_2 = topic('Indicators of living standards: HDI, MEW and MPI', 'indicators of living standards', 'hdi', 'mew', 'multidimensional poverty index')
t21_2.fixed('C1', (1, 2, 3), [
    ('The Human Development Index combines measures of', 'health (life expectancy), education (years of schooling) and income (GNI per head at PPP)', 'Geometric mean of three dimension indices.',
     ['GDP, inflation and unemployment', 'exports, imports and debt', 'population, land area and resources']),
    ('The Measure of Economic Welfare (MEW) adjusts GDP by', 'adding the value of leisure and non-market activity and subtracting “bads” such as pollution', 'Nordhaus–Tobin.', ['subtracting all government spending', 'adding imports', 'dividing by the population']),
    ('The Multidimensional Poverty Index is calculated as', 'the share of people who are multidimensionally poor multiplied by the average intensity of their deprivation', 'MPI = H × A.', ['the share of people below $2.15 a day', 'GDP per head divided by the Gini coefficient', 'the unemployment rate times inflation']),
    ('A country with a high GNI per head but a low HDI rank is likely to have', 'relatively poor health or education outcomes', 'Income rank − HDI rank positive: income not translated into development.', ['very low income', 'perfect income equality', 'no exports']),
])
t21_2.fixed('C2', (2, 3, 4), [
    ('Explain two advantages of the HDI over GDP per head as a measure of living standards.', 'It includes health and education, not just income; it uses PPP-adjusted income; the income index uses logs, reflecting diminishing returns to income.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain two limitations of the HDI.', 'Ignores inequality within the country, environmental damage, political freedom and the informal economy; equal weights are arbitrary; data quality.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain how the MPI differs from income-based measures of poverty.', 'It measures deprivations directly in health, education and living standards (e.g. nutrition, schooling, sanitation, electricity), so it captures aspects of poverty that income does not.', '1 mark: dimensions; 1 mark: contrast with income measure [2]'),
])


@t21_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_2_hdi(r, D):
    le = r.choice([58.0, 62.5, 67.0, 71.5, 76.0, 80.5])
    mys = r.choice([4.5, 6.0, 7.5, 9.0, 11.0, 12.5])
    eys = r.choice([9.0, 11.0, 12.5, 14.0, 16.0])
    gni = r.choice([1500, 3000, 6000, 12000, 25000, 45000])
    lei = (le - 20) / 65
    ei = (mys / 15 + eys / 18) / 2
    ii = (math.log(gni) - math.log(100)) / (math.log(75000) - math.log(100))
    hdi = (lei * ei * ii) ** (1 / 3)
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'Life expectancy in {c} is {num(le, 1)} years. Using the HDI formula (LE − 20)/(85 − 20), calculate the life expectancy index.', num(lei, 3),
                  f'({num(le, 1)} − 20)/65 = {num(lei, 3)}.', dis_num(r, lei, lambda x: num(x, 3), [le / 85, (le - 20) / 85]))
    if D == 3 and r.random() < 0.5:
        h = r.choice([20, 30, 40, 50, 60])
        a = r.choice([40, 45, 50, 55])
        mpi = h * a / 10000
        return {'stem': f'In {c}, {h}% of the population are multidimensionally poor and, on average, they are deprived in {a}% of the weighted indicators. Calculate the MPI and explain what it shows that an income poverty line would not.',
                'answer': f'MPI = {h/100:.2f} × {a/100:.2f} = {num(mpi, 3)}. It shows both how many are poor and how intensely, across health, education and living standards, not just income.',
                'key': 'MPI = H × A [2]; interpretation [1].', 'type': 'numerical'}
    return {'stem': f'Data for {c}: life expectancy {num(le, 1)} years; mean years of schooling {num(mys, 1)}; expected years of schooling {num(eys, 1)}; GNI per head (PPP) ${gni:,}. Using the UNDP method (LEI = (LE − 20)/65; EI = (MYS/15 + EYS/18)/2; II = (ln GNI − ln 100)/(ln 75,000 − ln 100); HDI = geometric mean), calculate the HDI and identify which dimension most limits it.',
            'answer': f'LEI = {num(lei, 3)}; EI = {num(ei, 3)}; II = {num(ii, 3)}; HDI = {num(hdi, 3)}. The lowest index ({["health", "education", "income"][[lei, ei, ii].index(min(lei, ei, ii))]}) limits it most.',
            'key': 'Each dimension index [3]; geometric mean (LEI × EI × II)^(1/3) [1]; identification [1].', 'type': 'multi_step'}


t21_3 = topic('Comparing living standards over time and between countries', 'comparing living standards over time and between countries', 'comparing living standards')
t21_3.fixed('C1', (1, 2, 3), [
    ('To compare living standards between countries, GDP per head should be converted using', 'purchasing power parity exchange rates', 'Adjusts for differences in price levels.', ['market exchange rates only', 'the inflation rate', 'interest rates']),
    ('To compare living standards over time within a country, economists use', 'real GDP per head', 'Removes the effect of inflation and population change.', ['nominal GDP', 'total exports', 'the money supply']),
    ('Which is a problem when comparing GDP per head between countries?', 'Differences in the size of the informal economy', 'Also: income distribution, hours worked, quality of goods, externalities.', ['All countries measure GDP identically', 'Population is the same everywhere', 'Prices are identical in all countries']),
    ('A rise in GDP per head may overstate the rise in living standards if', 'it is accompanied by longer working hours and more pollution', 'GDP ignores leisure and environmental costs.', ['inequality falls', 'life expectancy rises', 'leisure time increases']),
])
t21_3.fixed('C2', (2, 3, 4), [
    ('Explain two problems in using real GDP per head to compare living standards over time.', 'Changes in quality and new products; changes in distribution; changes in hours worked and leisure; environmental costs; growth of the informal economy or non-market activity.', '1 mark each identified, 1 mark each explained [4]'),
])


@t21_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t21_3_cmp(r, D):
    c1, c2 = r.sample(COUNTRIES, 2)
    g1, g2 = r.choice([200, 400, 800]), r.choice([50, 120, 300])
    p1, p2 = r.choice([20, 40, 60]), r.choice([30, 80, 150])
    e2 = r.choice([10, 20, 40])
    ppp2 = e2 * r.choice([0.3, 0.4, 0.5])
    pc1 = g1 * 1000 / p1
    pc2_mkt = g2 * 1000 / p2
    pc2_ppp = pc2_mkt * e2 / ppp2
    if D <= 2:
        return cq(r, D, f'{c1} has GDP of ${g1} billion and a population of {p1} million. Calculate GDP per head.', money(pc1), f'{g1} billion/{p1} million = {money(pc1)}.',
                  dis_num(r, pc1, money, [g1 / p1, g1 * p1]))
    return {'stem': f'{c1}: GDP ${g1} billion, population {p1} million. {c2}: GDP ${g2} billion at market exchange rates, population {p2} million; its market exchange rate is $1 = {e2} units but the PPP rate is $1 = {num(ppp2, 1)} units. Calculate GDP per head for each country at market rates and for {c2} at PPP, and explain why the PPP figure gives a better comparison of living standards.',
            'answer': f'{c1}: {money(round(pc1))}; {c2}: {money(round(pc2_mkt))} at market rates and {money(round(pc2_ppp))} at PPP. Prices are lower in {c2}, so its income buys more than market rates suggest; PPP adjusts for this.',
            'key': 'GDP/population for each [2]; PPP adjustment × (market rate/PPP rate) [2]; explanation [1].', 'type': 'multi_step'}


def _dev_c4(r, D):
    d = ctx(r)
    g = r.choice([6, 7, 8])
    le0, le1 = r.choice([(61, 62), (64, 64.5)])
    intro = f'Extract: Real GDP in {d["country"]} has grown by {g}% a year for a decade, mainly from oil exports. Population grows at 2.5% a year. Life expectancy has risen only from {le0} to {le1} years and many rural households lack electricity.'
    parts = [
        lambda r: ('Calculate the approximate annual growth of real GDP per head.', f'{num(g - 2.5, 1)}% (exactly {pct(100 * ((1 + g / 100) / 1.025 - 1), 2)})', '[2]'),
        lambda r: ('Explain why the data suggest growth without much development.', 'Health barely improved; deprivation persists; oil revenue may be concentrated; inequality.', '[3]'),
        lambda r: ('Explain why the HDI may be a better indicator of development than GDP per head here.', 'Includes health and education; would show limited progress.', '[2]'),
        lambda r: ('Discuss how the government could turn growth into development.', 'Use oil revenue for health, education, rural electrification; sovereign wealth fund; reduce corruption; diversify; risks and constraints.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t21_1, t21_2, t21_3], 'C4', (3, 4, 5), 'case', _dev_c4)
items(t21_1, 'C2', (2, 3, 4), [
    ('{country}’s GDP has risen rapidly due to mining, but most profits go to foreign owners and mining areas suffer pollution. Explain why this may not be economic development.', 'Development requires improvements in living standards for most people; if gains flow abroad or to a few, and health and environment worsen, welfare may not improve.', '1 mark: definition; 1 mark: application [2]'),
])
items(t21_2, 'C2', (2, 3, 4), [
    ('{country} and {country2} have similar GNI per head, but {country} has a much higher HDI. Explain how this could happen.', '{country} may spend more on public health and education, or distribute income more equally, so life expectancy and schooling are higher for the same income.', '1 mark: health/education; 1 mark: policy/distribution [2]'),
])
items(t21_3, 'C2', (2, 3, 4), [
    ('Average working hours in {country} rose from 40 to 50 a week while real GDP per head rose by 10%. Explain why living standards may not have risen by 10%.', 'People have less leisure, which has value; stress and health may suffer; the gain per hour worked is lower; GDP excludes leisure.', '1 mark: leisure loss; 1 mark: GDP limitation [2]'),
])
essays(t21_1, [
    ('economic growth will always lead to economic development',
     'Explain the difference between economic growth and economic development.',
     'Growth funds public services and reduces poverty.',
     'Distribution, environmental costs, corruption, enclave growth, jobless growth.'),
], ['{country} has had rapid GDP growth but poverty remains widespread.'])
essays(t21_2, [
    ('the Human Development Index is the best indicator of living standards',
     'Explain how the HDI is calculated.',
     'Broader than GDP, includes health and education.',
     'Ignores inequality, environment, freedom; MPI and MEW capture other aspects; data quality.'),
], ['{country} ranks 60 places higher on GNI per head than on the HDI.'])
essays(t21_3, [
    ('GDP per head is an unreliable way to compare living standards between countries',
     'Explain why PPP exchange rates are used for international comparisons.',
     'Price levels, informal economy, distribution and non-market output differ.',
     'PPP adjustment helps; GDP still correlates with health and education; combine with other indicators.'),
], ['A report compares living standards in {country}, {country2} and {country3}.'])
CHAPTERS[21] = [t21_1, t21_2, t21_3]

# ============================================================================ 22 Characteristics of countries at different levels of development
t22_1 = topic('Population growth, age structure and dependency ratios', 'population growth', 'age structure and dependency ratios')
t22_1.fixed('C1', (1, 2, 3), [
    ('The dependency ratio is calculated as', 'the number of people aged under 15 and over 64 divided by the number aged 15 to 64, × 100', 'Dependants per 100 people of working age.',
     ['the number unemployed divided by the labour force', 'the number of children per family', 'the population divided by the land area']),
    ('The natural rate of population increase is', 'the birth rate minus the death rate', 'Excludes migration; usually per 1,000.', ['births plus deaths', 'immigration minus emigration', 'the fertility rate']),
    ('A population pyramid with a wide base and narrow top indicates', 'high birth rates and a young population', 'Typical of low-income countries.', ['an ageing population', 'low birth rates', 'high life expectancy and low fertility']),
    ('A demographic dividend may occur when', 'the share of the working-age population rises as birth rates fall', 'Lower dependency ratio can boost growth.', ['the population is ageing rapidly', 'birth rates rise sharply', 'emigration of young workers increases']),
])
t22_1.fixed('C2', (2, 3, 4), [
    ('Explain two economic problems caused by a high dependency ratio of young people.', 'High spending needed on education and health; fewer workers to support dependants; low saving; pressure on jobs when they enter the labour force.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why birth rates tend to fall as countries develop.', 'Lower infant mortality, more education and employment for women, access to contraception, children cost more and are needed less for farm work or old-age support, urbanisation.', '1 mark each reason [2]'),
])


@t22_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_1_dep(r, D):
    y = r.choice([12, 18, 22, 28, 35, 40])
    o = r.choice([3, 5, 8, 12, 18, 22])
    w = 100 - y - o
    dr = 100 * (y + o) / w
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'In {c}, {y}% of the population is aged under 15, {o}% is over 64 and the rest are aged 15–64. Calculate the dependency ratio.', num(dr, 1),
                  f'({y} + {o})/{w} × 100 = {num(dr, 1)}.', dis_num(r, dr, lambda x: num(x, 1), [y + o, 100 * y / w]))
    br, dth = r.choice([18, 24, 32, 38]), r.choice([6, 8, 10, 12])
    mig = r.choice([-3, -1, 0, 2, 4])
    pg = (br - dth + mig) / 10
    dt = 70 / pg if pg > 0 else None
    return {'stem': f'{c}: {y}% of the population aged under 15, {o}% over 64. Birth rate {br} per 1,000; death rate {dth} per 1,000; net migration {mig:+d} per 1,000. Calculate the dependency ratio, the natural rate of increase and the population growth rate (%), and the approximate doubling time. Explain one economic implication.',
            'answer': f'Dependency ratio = {num(dr, 1)}; natural increase = {br - dth} per 1,000 ({num((br - dth) / 10, 1)}%); growth = {num(pg, 1)}%' + (f'; doubling time ≈ {num(dt, 0)} years' if dt else '') + '. ' + ('A young population needs heavy spending on schools and jobs.' if y > o * 2 else 'An ageing population raises pension and health costs.'),
            'key': 'Dependency ratio [1]; natural increase [1]; growth incl. migration [1]; rule of 70 [1]; implication [1].', 'type': 'multi_step'}


t22_2 = topic('Employment structure: primary, secondary and tertiary', 'employment structure', 'primary, secondary and tertiary sectors')
t22_2.fixed('C1', (1, 2, 3), [
    ('In most low-income countries, the largest share of employment is in the', 'primary sector', 'Agriculture, fishing, mining.', ['secondary sector', 'tertiary sector', 'quaternary sector']),
    ('As countries develop, employment typically shifts', 'from the primary to the secondary and then the tertiary sector', 'Clark–Fisher model.', ['from tertiary to primary', 'from secondary to primary', 'only into the primary sector']),
    ('Which job is in the tertiary sector?', 'A bank clerk', 'Services.', ['A cocoa farmer', 'A steel worker', 'A coal miner']),
    ('Deindustrialisation refers to', 'a decline in the share of manufacturing in output and employment', 'Typical of high-income economies.', ['a rise in agricultural employment', 'the growth of manufacturing', 'the privatisation of industries']),
])
t22_2.fixed('C2', (2, 3, 4), [
    ('Explain why employment shifts from the primary sector as an economy develops.', 'Agricultural productivity rises so fewer workers are needed; income elasticity of demand for food is low while that for manufactures and services is high; urban jobs pay more.', '1 mark: productivity; 1 mark: income elasticities; 1 mark: wage differences [3]'),
    ('Explain one problem for a country with a large share of employment in agriculture.', 'Low productivity and incomes; vulnerability to weather and commodity prices; underemployment and seasonal unemployment.', '1 mark: problem; 1 mark: explanation [2]'),
])


@t22_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_2_struct(r, D):
    tot = r.choice([10, 20, 25, 40])
    p = r.choice([45, 55, 62, 70, 30, 12])
    s_ = r.choice([10, 15, 20, 25])
    t = 100 - p - s_
    c = r.choice(COUNTRIES)
    out_p = r.choice([15, 20, 25, 8])
    if D <= 2:
        return cq(r, D, f'In {c}, {tot} million people are employed: {p}% in the primary sector and {s_}% in the secondary sector. Calculate the number employed in the tertiary sector.', f'{num(tot * t / 100, 2)} million',
                  f'Tertiary = {100 - p - s_}% × {tot} = {num(tot * t / 100, 2)} million.', dis_num(r, tot * t / 100, lambda x: f'{num(x, 2)} million', [tot * (p + s_) / 100]))
    rel = (out_p / p) / ((100 - out_p) / (100 - p))
    return {'stem': f'In {c}, {p}% of the {tot} million workers are in the primary sector, which produces {out_p}% of GDP. {s_}% work in industry and the rest in services. Calculate the number of workers in each sector and the productivity of primary-sector workers relative to the rest of the economy. Explain what this suggests about the country’s level of development.',
            'answer': f'Primary {num(tot * p / 100, 2)}m, secondary {num(tot * s_ / 100, 2)}m, tertiary {num(tot * t / 100, 2)}m. Relative productivity = ({out_p}/{p}) ÷ ({100 - out_p}/{100 - p}) = {num(rel, 2)}. ' + ('Low productivity in a large primary sector is typical of a low-income economy; moving labour out of agriculture would raise output.' if p >= 40 else 'A smaller primary sector suggests a more developed economy.'),
            'key': 'Workers in each sector [2]; relative productivity ratio [2]; interpretation [1].', 'type': 'multi_step'}


t22_3 = topic('Urbanisation, income distribution and the informal economy', 'urbanisation', 'income distribution and the informal economy', 'informal economy')
t22_3.fixed('C1', (1, 2, 3), [
    ('The informal economy consists of', 'economic activity that is not registered, taxed or regulated by the state', 'E.g. street vendors, casual labour.', ['activity of state-owned firms', 'exports of manufactured goods', 'activity of large registered firms only']),
    ('Rapid urbanisation in developing countries often leads to', 'the growth of informal settlements and pressure on infrastructure', 'Rural–urban migration outpaces housing and services.', ['falling urban populations', 'lower demand for housing', 'fewer jobs in services']),
    ('A large informal economy means that official GDP figures are likely to', 'understate actual output', 'Unrecorded activity.', ['overstate output', 'be completely accurate', 'measure only exports']),
    ('Rural–urban migration is mainly driven by', 'higher expected wages and better services in cities', 'Push and pull factors (Todaro model: expected income).', ['higher wages in rural areas', 'lower urban rents', 'falling urban employment']),
])
t22_3.fixed('C2', (2, 3, 4), [
    ('Explain two disadvantages of a large informal economy.', 'Low tax revenue for public services; workers lack legal protection, social insurance and access to credit; low productivity; GDP data unreliable.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why income inequality is often high in countries at an early stage of development.', 'Ownership of land and capital is concentrated; small modern sector with high wages alongside large low-productivity sector; limited taxes and transfers (Kuznets curve).', '1 mark: dual economy/ownership; 1 mark: weak redistribution [2]'),
])


@t22_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t22_3_urb(r, D):
    pop0, u0 = r.choice([20, 30, 50]), r.choice([25, 30, 35, 40])
    pop1 = pop0 * r.choice([1.2, 1.25, 1.3])
    u1 = u0 + r.choice([8, 10, 15])
    c = r.choice(COUNTRIES)
    city0, city1 = pop0 * u0 / 100, pop1 * u1 / 100
    if D <= 2:
        return cq(r, D, f'{c} has a population of {pop0} million, of whom {u0}% live in urban areas. Calculate the urban population.', f'{num(city0, 2)} million', f'{u0}% × {pop0} = {num(city0, 2)}.',
                  dis_num(r, city0, lambda x: f'{num(x, 2)} million', [pop0 - city0]))
    inf = r.choice([30, 40, 55])
    gdp = r.choice([100, 200])
    return {'stem': f'Over 15 years, {c}’s population grew from {pop0} million to {num(pop1, 1)} million and the urban share from {u0}% to {u1}%. The informal economy is estimated at {inf}% of official GDP of ${gdp} billion. Calculate the urban population at each date and the percentage growth, and the estimated size of the informal economy. Explain one consequence of these trends.',
            'answer': f'Urban: {num(city0, 2)}m → {num(city1, 2)}m ({pct(100 * (city1 - city0) / city0, 1)}). Informal economy ≈ ${num(gdp * inf / 100)} billion. Consequence: pressure on housing, transport and services; growth of slums and informal jobs; lower tax base.',
            'key': 'Urban populations [2]; % growth [1]; informal size [1]; consequence [1].', 'type': 'multi_step'}


def _char_c4(r, D):
    d = ctx(r)
    y, o = r.choice([(40, 4), (35, 5), (42, 3)])
    agr = r.choice([55, 60, 65])
    intro = f'Extract: In {d["country"]}, {y}% of the population is under 15 and {o}% over 64. {agr}% of workers are in agriculture, many in the informal sector, and the urban population is growing by 5% a year.'
    parts = [
        lambda r: ('Calculate the dependency ratio.', f'{num(100 * (y + o) / (100 - y - o), 1)}', '[2]'),
        lambda r: ('Explain two economic problems associated with this age structure.', 'High spending on schooling/health; low savings; future job creation needs.', '[4]'),
        lambda r: ('Explain why rapid urbanisation may increase the informal economy.', 'Migrants exceed formal job creation; informal work and housing absorb them.', '[2]'),
        lambda r: ('Discuss policies that could raise living standards in this economy.', 'Education (especially girls), family planning, agricultural productivity, infrastructure, formalisation incentives; evaluation of cost and time.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t22_1, t22_2, t22_3], 'C4', (3, 4, 5), 'case', _char_c4)
items(t22_1, 'C2', (2, 3, 4), [
    ('The birth rate in {country} has fallen sharply over 20 years. Explain how this could create a demographic dividend.', 'As fewer children are born, the working-age share rises and the dependency ratio falls, so more people produce and save relative to dependants, raising income per head if jobs are available.', '1 mark: lower dependency; 1 mark: more workers/saving → growth [2]'),
])
items(t22_2, 'C2', (2, 3, 4), [
    ('Explain why {country}’s share of employment in services has risen as incomes have grown.', 'Demand for services (health, finance, leisure) is income elastic, so it rises faster than income; productivity gains in agriculture and manufacturing release labour.', '1 mark: YED; 1 mark: productivity releases labour [2]'),
])
items(t22_3, 'C2', (2, 3, 4), [
    ('Explain why street traders in {city} may choose to stay in the informal economy.', 'Registration and taxes are costly and complicated; regulation is burdensome; benefits of formality (credit, protection) may seem small.', '1 mark each reason [2]'),
])
essays(t22_1, [
    ('rapid population growth is the main obstacle to economic development',
     'Explain the meaning and significance of the dependency ratio.',
     'High dependency, pressure on resources, low saving.',
     'Demographic dividend; larger labour force and market; other obstacles (institutions, infrastructure, debt).'),
], ['The population of {country} is expected to double in 25 years.'])
essays(t22_2, [
    ('countries should move workers out of agriculture as quickly as possible',
     'Explain how the structure of employment changes as countries develop.',
     'Higher productivity in industry and services.',
     'Urban unemployment, food security, need for agricultural productivity first; premature deindustrialisation.'),
], ['Most workers in {country} are small-scale farmers.'])
essays(t22_3, [
    ('the informal economy does more harm than good in developing countries',
     'Explain the characteristics of the informal economy.',
     'Low tax revenue, low productivity, no protection.',
     'Provides jobs and incomes, entrepreneurship, flexibility; safety net; formalisation should be gradual.'),
], ['Over half of all workers in {country} are employed informally.'])
CHAPTERS[22] = [t22_1, t22_2, t22_3]

# ============================================================================ 23 Relationships between countries at different levels of development
t23_1 = topic('FDI and multinational companies', 'foreign direct investment', 'role of multinational companies', 'fdi')
t23_1.fixed('C1', (1, 2, 3), [
    ('Foreign direct investment is', 'investment by a firm in productive assets in another country, with a lasting management interest', 'E.g. building a factory abroad; differs from portfolio investment.',
     ['buying foreign government bonds', 'a loan from the IMF', 'aid given by a foreign government']),
    ('Transfer pricing by a multinational company involves', 'setting internal prices between its subsidiaries to shift profits to low-tax countries', 'Reduces tax paid in high-tax host countries.', ['setting the same price in all countries', 'transferring workers between countries', 'paying higher wages abroad']),
    ('Which is a likely benefit of FDI for a host developing country?', 'Transfer of technology and skills', 'Also jobs, tax revenue, exports, capital.', ['Repatriation of profits', 'Loss of domestic firms', 'Reduced tax base']),
    ('Repatriation of profits by a multinational appears in the host country’s balance of payments as', 'a debit in primary income on the current account', 'Investment income paid abroad.', ['a credit in trade in goods', 'a credit on the financial account', 'secondary income credit']),
])
t23_1.fixed('C2', (2, 3, 4), [
    ('Explain two possible disadvantages of FDI for a developing country.', 'Repatriation of profits; transfer pricing and tax avoidance; crowding out of domestic firms; environmental damage; low-skilled jobs only; political influence; footloose firms.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why multinational companies invest in developing countries.', 'Lower labour and land costs; access to raw materials and new markets; to avoid trade barriers; tax incentives; economies of scale.', '1 mark each reason [2]'),
])


@t23_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_1_fdi(r, D):
    inv = r.choice([200, 400, 500, 800])
    prof = r.choice([40, 60, 80, 100])
    rep = r.choice([50, 60, 75, 80])
    tax = r.choice([15, 20, 25, 30])
    jobs = r.choice([1500, 2000, 3000])
    wage = r.choice([3000, 4000, 6000])
    c = r.choice(COUNTRIES)
    taxpaid = prof * tax / 100
    repd = (prof - taxpaid) * rep / 100
    wages = jobs * wage / 1e6
    if D <= 2:
        return cq(r, D, f'A multinational in {c} makes a profit of ${prof} million and pays {tax}% tax there. It sends {rep}% of after-tax profit home. Calculate the profit repatriated.', f'${num(repd, 2)} million',
                  f'After-tax {prof} × (1 − {tax / 100}) = {num(prof - taxpaid, 2)}; × {rep}% = {num(repd, 2)}.', dis_num(r, repd, lambda x: f'${num(x, 2)} million', [prof * rep / 100, prof - taxpaid]))
    shift = r.choice([20, 30, 40])
    lost = prof * shift / 100 * tax / 100
    return {'stem': f'A multinational invests ${inv} million in {c}, employing {jobs:,} local workers at ${wage:,} a year. Annual profit is ${prof} million, taxed at {tax}%, and {rep}% of after-tax profit is repatriated. (a) Calculate tax paid, the local wage bill and profit repatriated. (b) If transfer pricing moved {shift}% of the profit to a zero-tax country, calculate the tax lost to {c}. (c) Assess whether the FDI benefits {c}.',
            'answer': f'(a) Tax ${num(taxpaid, 2)}m; wages ${num(wages, 2)}m; repatriated ${num(repd, 2)}m (b) ${num(lost, 2)}m (c) Benefits: jobs, wages, tax, technology, exports; costs: repatriation, transfer pricing, environmental or competition effects; net benefit depends on linkages and regulation.',
            'key': '(a) three calculations [3]; (b) shifted profit × tax rate [1]; (c) balanced assessment [2].', 'type': 'multi_step'}


t23_2 = topic('Foreign aid', 'foreign aid', 'types, benefits and drawbacks', 'aid')
t23_2.fixed('C1', (1, 2, 3), [
    ('Tied aid is aid that', 'must be spent on goods and services from the donor country', 'Reduces value to recipient; benefits donor exporters.', ['is given without conditions', 'is given only in emergencies', 'must be repaid with interest']),
    ('Bilateral aid is', 'aid given directly from one government to another', 'Multilateral aid is channelled through agencies like the World Bank.', ['aid given through the World Bank', 'aid from charities', 'private investment']),
    ('The UN target for official development assistance from rich countries is', '0.7% of gross national income', 'Few donors meet it.', ['7% of GDP', '0.07% of GDP', '10% of government spending']),
    ('Aid dependency refers to', 'a situation where a country relies on aid for a large share of its budget and has weak incentives to develop its own revenue', 'Long-term reliance.', ['a country that gives aid', 'aid that is tied', 'aid given for disaster relief']),
])
t23_2.fixed('C2', (2, 3, 4), [
    ('Explain two reasons why foreign aid may not promote development.', 'Corruption and misuse; tied aid reduces value; aid dependency; crowding out of local producers (food aid); spending on prestige projects; conditions that harm the poor.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain how aid can help to close the savings gap in a developing country.', 'Low incomes mean low saving and investment (Harrod–Domar); aid supplements domestic saving to fund investment in capital and infrastructure, raising growth.', '1 mark: savings gap; 1 mark: aid funds investment/growth [2]'),
])


@t23_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_2_aid(r, D):
    gni = r.choice([500, 1500, 2000, 3000])
    oda = r.choice([1.5, 3, 6, 9, 14])
    c = r.choice(COUNTRIES)
    share = 100 * oda / gni
    if D <= 2:
        return cq(r, D, f'{c} has GNI of ${gni:,} billion and gives ${num(oda)} billion in official development assistance. Calculate aid as a percentage of GNI.', pct(share, 2),
                  f'{num(oda)}/{gni:,} × 100 = {pct(share, 2)}.', dis_num(r, share, lambda x: pct(x, 2), [0.7]))
    need = gni * 0.007
    tied = r.choice([30, 40, 50])
    prem = r.choice([15, 20, 25])
    loss = oda * tied / 100 * prem / 100
    return {'stem': f'{c} has GNI of ${gni:,} billion and gives ${num(oda)} billion in aid. {tied}% of its aid is tied, and tied goods cost {prem}% more than on the world market. (a) Calculate aid as a % of GNI and the extra aid needed to meet the 0.7% target. (b) Calculate the loss in value to recipients from tying. (c) Explain one other drawback of tied aid.',
            'answer': f'(a) {pct(share, 2)}; extra needed ${num(max(0, need - oda), 2)} billion (b) ${num(loss, 3)} billion (c) Recipients cannot choose suitable or cheapest goods; may not match needs; benefits donor firms; may create dependency on donor parts and services.',
            'key': '(a) share [1]; 0.7% × GNI − aid [1]; (b) tied aid × premium [2]; (c) drawback [1].', 'type': 'multi_step'}


t23_3 = topic('External debt and the IMF and World Bank', 'external debt', 'role of the imf and world bank', 'debt')
t23_3.fixed('C1', (1, 2, 3), [
    ('The debt service ratio is', 'debt service payments as a percentage of export earnings', 'Shows ability to service external debt from exports.', ['total debt divided by population', 'interest rates minus inflation', 'imports divided by exports']),
    ('The main role of the IMF is to', 'promote international monetary stability and lend to countries with balance of payments problems', 'Short-term BoP support with conditionality.',
     ['fund long-term development projects only', 'set world trade rules', 'set exchange rates for all countries']),
    ('The World Bank mainly', 'provides loans and grants for long-term development projects', 'IBRD and IDA: infrastructure, health, education.', ['regulates international trade', 'acts as a central bank for the world', 'sets interest rates']),
    ('A depreciation of a developing country’s currency makes its foreign-currency debt', 'more expensive to service in domestic currency', 'More local currency needed per dollar.', ['cheaper to service', 'disappear', 'unaffected']),
])
t23_3.fixed('C2', (2, 3, 4), [
    ('Explain two causes of high external debt in developing countries.', 'Persistent current account deficits; borrowing for projects that did not generate returns; rising world interest rates; currency depreciation; falling commodity prices reducing export earnings.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why IMF conditions attached to loans are controversial.', 'Austerity and structural adjustment may cut public services and raise unemployment and poverty in the short run, though they aim to restore stability and growth.', '1 mark: conditions; 1 mark: social cost vs stability [2]'),
])


@t23_3.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_3_debt(r, D):
    debt = r.choice([20, 30, 40, 60])
    rate = r.choice([4, 5, 6, 8])
    repay = r.choice([1, 2, 3])
    X = r.choice([10, 15, 20, 25])
    gdp = r.choice([50, 80, 100])
    service = debt * rate / 100 + repay
    dsr = 100 * service / X
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'{c} has external debt of ${debt} billion and GDP of ${gdp} billion. Calculate the debt-to-GDP ratio.', pct(100 * debt / gdp, 1), f'{debt}/{gdp} × 100 = {pct(100 * debt / gdp, 1)}.',
                  dis_num(r, 100 * debt / gdp, lambda x: pct(x, 1), [100 * gdp / debt]))
    dep = r.choice([20, 25, 50])
    return {'stem': f'{c} has external debt of ${debt} billion in dollars at an interest rate of {rate}%, and repays ${repay} billion of principal each year. Export earnings are ${X} billion and GDP is ${gdp} billion. (a) Calculate annual debt service and the debt service ratio. (b) The currency depreciates by {dep}% against the dollar. Explain the effect on the burden of the debt.',
            'answer': f'(a) Debt service = {num(debt * rate / 100, 2)} + {repay} = ${num(service, 2)} billion; DSR = {pct(dsr, 1)} of exports. (b) The dollar debt is unchanged but costs more local currency (each dollar needs more units); if export prices are in dollars the DSR is unchanged, but the burden on the government budget and local firms rises.',
            'key': '(a) interest + principal [1]; ÷ exports [1]; (b) depreciation raises local-currency cost [2].', 'type': 'multi_step'}


t23_4 = topic('Trade, terms of trade and commodity dependence', 'trade, terms of trade', 'commodity dependence', 'terms of trade')
t23_4.fixed('C1', (1, 2, 3), [
    ('The terms of trade index is calculated as', 'index of export prices ÷ index of import prices × 100', 'A rise is an “improvement” (favourable).', ['index of import prices ÷ index of export prices × 100', 'value of exports − value of imports', 'export volume ÷ import volume']),
    ('If the export price index rises from 100 to 110 and the import price index from 100 to 125, the terms of trade index is', '88', '110/125 × 100 = 88: a deterioration.', ['114', '113.6', '15']),
    ('Commodity dependence makes a country vulnerable mainly because', 'commodity prices are volatile and demand is income inelastic', 'Export earnings fluctuate; long-run decline in ToT (Prebisch–Singer).', ['commodities are not traded', 'commodity prices never change', 'commodities are only consumed domestically']),
    ('The Prebisch–Singer hypothesis suggests that', 'the terms of trade of primary-product exporters tend to deteriorate over time', 'Low income elasticity for primary goods vs manufactures.', ['the terms of trade of all countries improve', 'manufactures become cheaper than commodities', 'trade always benefits developing countries equally']),
])
t23_4.fixed('C2', (2, 3, 4), [
    ('Explain why an improvement in the terms of trade may not improve the current account.', 'If export prices rise and demand is price elastic, export volumes fall and revenue may fall; a rise in ToT may reflect a loss of competitiveness.', '1 mark: price elastic demand; 1 mark: competitiveness [2]'),
    ('Explain two ways a commodity-dependent country could reduce its vulnerability.', 'Diversify into manufacturing/services; add value through processing; stabilisation funds/sovereign wealth funds; hedging; regional trade agreements.', '1 mark each identified, 1 mark each explained [4]'),
])


@t23_4.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t23_4_tot(r, D):
    xp = r.choice([85, 92, 105, 110, 120, 130])
    mp = r.choice([95, 100, 108, 115, 125])
    tot = 100 * xp / mp
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'In {c}, the export price index rises to {xp} and the import price index to {mp} (base year = 100). Calculate the terms of trade index.', num(tot, 1),
                  f'{xp}/{mp} × 100 = {num(tot, 1)}.', dis_num(r, tot, lambda x: num(x, 1), [100 * mp / xp, xp - mp + 100]))
    com = r.choice(['copper', 'cocoa', 'coffee', 'crude oil', 'cotton'])
    sh = r.choice([45, 60, 70, 80])
    fall = r.choice([20, 30, 40])
    X = r.choice([10, 20, 30])
    loss = X * sh / 100 * fall / 100
    return {'stem': f'{c} earns ${X} billion from exports, of which {sh}% comes from {com}. Its export price index is {xp} and import price index {mp}. (a) Calculate the terms of trade index and state whether it shows an improvement or deterioration since the base year. (b) If the world price of {com} then falls by {fall}% with unchanged volumes, calculate the fall in export earnings. (c) Explain why commodity dependence is a problem.',
            'answer': f'(a) {num(tot, 1)}: {"improvement" if tot > 100 else "deterioration"} (b) ${num(loss, 2)} billion (c) Volatile prices make export earnings, government revenue and growth unstable; low income elasticity limits long-run growth; Dutch disease.',
            'key': '(a) ToT formula and interpretation [2]; (b) share × fall [1]; (c) two developed points [2].', 'type': 'multi_step'}


def _rel_c4(r, D):
    d = ctx(r)
    xp0, mp0 = 100, 100
    xp1, mp1 = r.choice([(78, 104), (82, 110), (70, 98)])
    debt = r.choice([60, 75, 90])
    intro = f'Extract: {d["country"]} relies on copper for 70% of its exports. Over five years its export price index fell to {xp1} while its import price index rose to {mp1}. External debt has reached {debt}% of GDP and the government is negotiating an IMF loan, while a foreign mining company plans a new mine.'
    parts = [
        lambda r: ('Calculate the change in the terms of trade.', f'ToT = {xp1}/{mp1} × 100 = {num(100 * xp1 / mp1, 1)}: a deterioration of {num(100 - 100 * xp1 / mp1, 1)}%', '[2]'),
        lambda r: ('Explain how the change in the terms of trade may have contributed to the debt problem.', 'Lower export earnings relative to imports widen the current account deficit, financed by borrowing.', '[2]'),
        lambda r: ('Explain two conditions the IMF might attach to its loan.', 'Fiscal consolidation, removal of subsidies, exchange-rate flexibility, privatisation, anti-corruption measures.', '[2]'),
        lambda r: ('Discuss whether the new mine will benefit the country’s development.', 'Jobs, tax, FDI inflows, technology vs repatriation, environmental damage, deepening commodity dependence; conditions such as royalties and linkages.', '[4]'),
        lambda r: ('Explain one way the country could reduce its dependence on copper.', 'Diversification into processing/manufacturing or services; sovereign wealth fund.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t23_1, t23_2, t23_3, t23_4], 'C4', (3, 4, 5), 'case', _rel_c4)
items(t23_1, 'C2', (2, 3, 4), [
    ('{firm}, a multinational, plans a car factory in {country}. Explain two ways the factory might benefit local firms.', 'Demand for local suppliers (backward linkages); training of workers who later move to local firms; technology spillovers; improved infrastructure.', '1 mark each [2]'),
])
items(t23_2, 'C2', (2, 3, 4), [
    ('Food aid is shipped free to {country} after a good harvest. Explain how this could harm local farmers.', 'Free food increases supply and lowers local prices, reducing farmers’ incomes and incentives to produce, and may create dependency.', '1 mark: price fall; 1 mark: incomes/incentives [2]'),
])
items(t23_3, 'C2', (2, 3, 4), [
    ('World interest rates rise sharply. Explain the effect on a developing country such as {country} with large variable-rate external debts.', 'Interest payments rise, increasing debt service and the debt service ratio, diverting foreign exchange and budget revenue from development spending.', '1 mark: higher interest cost; 1 mark: diversion of resources [2]'),
])
items(t23_4, 'C2', (2, 3, 4), [
    ('The world price of {country}’s main export, cocoa, rises by 40%. Explain the effect on its terms of trade and on its economy.', 'Export price index rises, so ToT improve; export earnings and government revenue rise, but the currency may appreciate and other exports become less competitive (Dutch disease); the boom may be temporary.', '1 mark: ToT improve; 1 mark: wider effect [2]'),
])
essays(t23_1, [
    ('foreign direct investment by multinational companies always benefits developing countries',
     'Explain the reasons why multinational companies invest in developing countries.',
     'Jobs, capital, technology, tax, exports.',
     'Repatriation, transfer pricing, environmental damage, crowding out, footloose; depends on regulation and linkages.'),
], ['{firm}, a global company, has announced a $2 billion investment in {country}.'])
essays(t23_2, [
    ('foreign aid does more harm than good to developing countries',
     'Explain the different types of foreign aid.',
     'Dependency, corruption, tied aid, crowding out.',
     'Emergency relief, health and education projects, closing savings gap; quality of governance and aid design matter.'),
], ['{country} receives aid equal to 15% of its GNI.'])
essays(t23_3, [
    ('the IMF and World Bank have been successful in helping developing countries with debt problems',
     'Explain the roles of the IMF and the World Bank.',
     'Loans, stabilisation, debt relief (HIPC), technical assistance.',
     'Conditionality and austerity, social costs, recurring crises, voting power of rich countries.'),
], ['{country} has applied to the IMF for emergency support.'])
essays(t23_4, [
    ('specialising in primary commodities is the best strategy for low-income countries',
     'Explain what is meant by the terms of trade and how they are measured.',
     'Comparative advantage, export earnings, FDI in extraction.',
     'Volatile prices, deteriorating ToT, Dutch disease, low value added; diversification and processing.'),
], ['Coffee accounts for most of {country}’s export earnings.'])
CHAPTERS[23] = [t23_1, t23_2, t23_3, t23_4]

# ============================================================================ 24 Globalisation
t24_1 = topic('Causes and features of globalisation', 'causes and features of globalisation', 'globalisation')
t24_1.fixed('C1', (1, 2, 3), [
    ('Globalisation refers to', 'the increasing integration of national economies through trade, capital flows, technology and migration', 'Growing interdependence.',
     ['the growth of national government', 'the end of international trade', 'the use of a single world currency']),
    ('Which is a cause of globalisation?', 'Falling transport and communication costs', 'Containerisation, internet, trade liberalisation, deregulation of capital flows.', ['Rising tariffs', 'Restrictions on capital movement', 'Higher transport costs']),
    ('The trade openness ratio is measured by', '(exports + imports) ÷ GDP × 100', 'Higher ratio → more open.', ['exports ÷ imports', 'GDP ÷ population', 'imports − exports']),
    ('The World Trade Organization mainly aims to', 'promote freer trade and settle trade disputes', 'Rules-based trading system.', ['lend to countries with debt problems', 'fix exchange rates', 'set interest rates']),
])
t24_1.fixed('C2', (2, 3, 4), [
    ('Explain two causes of globalisation.', 'Improvements in transport (containers, air freight) and ICT; trade liberalisation through the WTO and trading blocs; deregulation of financial markets; growth of MNCs; opening of China and other economies.', '1 mark each identified, 1 mark each explained [4]'),
])


@t24_1.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t24_1_open(r, D):
    X, M = r.choice([150, 200, 400, 600]), r.choice([180, 220, 350, 550])
    gdp = r.choice([500, 800, 1000, 1500])
    o = 100 * (X + M) / gdp
    c = r.choice(COUNTRIES)
    if D <= 2:
        return cq(r, D, f'{c} has exports of ${X} billion, imports of ${M} billion and GDP of ${gdp} billion. Calculate the trade openness ratio.', pct(o, 1), f'({X} + {M})/{gdp} × 100 = {pct(o, 1)}.',
                  dis_num(r, o, lambda x: pct(x, 1), [100 * (X - M) / gdp, 100 * X / gdp]))
    X2, M2, gdp2 = X * 1.5, M * 1.6, gdp * 1.3
    o2 = 100 * (X2 + M2) / gdp2
    return {'stem': f'{c}: exports ${X}bn, imports ${M}bn, GDP ${gdp}bn. Ten years later exports have risen 50%, imports 60% and GDP 30%. Calculate the openness ratio at both dates and explain what the change suggests about globalisation and one risk for {c}.',
            'answer': f'Openness {pct(o, 1)} → {pct(o2, 1)}: trade has grown faster than GDP, so {c} is more integrated into the world economy. Risk: greater exposure to external shocks (world recessions, commodity prices), competition for domestic firms.',
            'key': 'Ratios at both dates [2]; interpretation [1]; risk [1].', 'type': 'numerical'}


t24_2 = topic('Trading blocs: trade creation and trade diversion', 'trading blocs', 'trade creation and trade diversion')
t24_2.fixed('C1', (1, 2, 3), [
    ('Trade creation occurs when', 'joining a trading bloc replaces higher-cost domestic production with lower-cost imports from a member', 'Welfare gain.', ['imports from a low-cost non-member are replaced by higher-cost imports from a member', 'tariffs are raised on all imports', 'exports fall']),
    ('Trade diversion occurs when', 'lower-cost imports from a non-member are replaced by higher-cost imports from a member because of the common external tariff', 'Welfare loss.', ['domestic production replaces imports', 'tariffs are removed for all countries', 'a country leaves a trading bloc']),
    ('A customs union differs from a free trade area because members of a customs union', 'apply a common external tariff to non-members', 'FTA: each member sets its own tariffs on non-members.', ['have a single currency', 'have no internal free trade', 'cannot trade with non-members']),
    ('Which is the most integrated form of trading bloc listed?', 'Economic union', 'FTA < customs union < common market < economic (and monetary) union.', ['Free trade area', 'Customs union', 'Preferential trade agreement']),
])
t24_2.fixed('C2', (2, 3, 4), [
    ('Distinguish between trade creation and trade diversion, giving an example of each.', 'Creation: a member switches from high-cost domestic production to cheaper imports from a partner after internal tariffs are removed. Diversion: a member switches from a cheaper non-member supplier to a dearer partner because the common external tariff makes non-member goods more expensive.', '1 mark each definition, 1 mark each example [4]'),
    ('Explain two benefits of a common market beyond those of a customs union.', 'Free movement of labour and capital allows resources to move to their most productive uses; larger market gives economies of scale; harmonised regulations lower costs.', '1 mark each [2]'),
])


@t24_2.add('C3', (1, 2, 3, 4, 5), 'numerical')
def t24_2_tc(r, D):
    dom = r.choice([30, 32, 35])
    partner = r.choice([24, 26, 28])
    world = r.choice([18, 20, 22])
    tariff = r.choice([40, 50, 60])
    pw_t = world * (1 + tariff / 100)
    pp_t = partner * (1 + tariff / 100)
    good = r.choice(['shoes', 'televisions', 'tyres', 'shirts'])
    c = r.choice(COUNTRIES)
    before = min([('domestic producers', dom), ('the partner country', pp_t), ('the rest of the world', pw_t)], key=lambda x: x[1])
    after = min([('domestic producers', dom), ('the partner country', partner), ('the rest of the world', pw_t)], key=lambda x: x[1])
    if before[0] == 'domestic producers' and after[0] == 'the partner country':
        res = 'trade creation'
    elif before[0] == 'the rest of the world' and after[0] == 'the partner country':
        res = 'trade diversion'
    else:
        res = 'no change in the source of supply'
    stem = (f'{c} can buy {good} from domestic producers at ${dom}, from a neighbouring country at ${partner} and from the rest of the world at ${world} (prices before tariffs). '
            f'{c} applies a {tariff}% tariff on all imports. It then forms a customs union with the neighbour, removing the tariff on its goods but keeping the tariff on the rest of the world.')
    if D <= 2:
        opts, a = mcq(r, after[0].capitalize(), [x for x in ('Domestic producers', 'The partner country', 'The rest of the world', 'No supplier') if x != after[0].capitalize()])
        return {'stem': stem + ' Which supplier is cheapest after the customs union is formed?', 'options': opts, 'answer': a,
                'key': f'Prices after: domestic {dom}, partner {partner}, rest of world {num(pw_t, 1)} → {after[0]}.'}
    return {'stem': stem + ' Calculate the price from each source before and after the customs union, identify the cheapest source in each case, and state whether this is trade creation or trade diversion. Explain the welfare effect.',
            'answer': f'Before: domestic ${dom}, partner ${num(pp_t, 1)}, world ${num(pw_t, 1)} → {before[0]}. After: domestic ${dom}, partner ${partner}, world ${num(pw_t, 1)} → {after[0]}. Result: {res}. '
                      + ({'trade creation': 'Welfare gain: resources move from higher-cost domestic production to a lower-cost producer.',
                          'trade diversion': f'Welfare loss: supply moves from the lowest-cost world producer (${world}) to a higher-cost partner (${partner}); the government also loses tariff revenue.',
                          'no change in the source of supply': 'No welfare change from the source of supply.'}[res]),
            'key': 'Tariff-inclusive prices [2]; cheapest source before and after [1]; classification [1]; welfare explanation [1].', 'type': 'multi_step'}


t24_3 = topic('Consequences of globalisation', 'consequences of globalisation for developed and developing economies', 'consequences of globalisation')
t24_3.fixed('C1', (1, 2, 3), [
    ('Which is a likely benefit of globalisation for consumers?', 'Lower prices and greater choice of goods', 'Specialisation by comparative advantage; competition.', ['Higher tariffs', 'Fewer imported goods', 'Less competition']),
    ('Globalisation may increase structural unemployment in developed economies because', 'manufacturing jobs move to lower-cost countries', 'Offshoring; deindustrialisation.', ['tariffs rise', 'exports become cheaper', 'productivity falls']),
    ('Contagion in the context of globalisation refers to', 'financial crises spreading rapidly from one country to others', 'Integrated capital markets.', ['the spread of diseases only', 'falling transport costs', 'the growth of trading blocs']),
    ('Which is a criticism of globalisation for developing countries?', 'Exploitation of low-wage labour and environmental damage by multinationals', 'Race to the bottom concerns.', ['Access to larger export markets', 'Inflows of FDI and technology', 'Lower import prices']),
])
t24_3.fixed('C2', (2, 3, 4), [
    ('Explain two ways in which globalisation can benefit developing economies.', 'Access to larger markets for exports; FDI bringing capital, jobs and technology; cheaper imported inputs; knowledge spillovers; specialisation by comparative advantage.', '1 mark each identified, 1 mark each explained [4]'),
    ('Explain why globalisation may increase income inequality within developed countries.', 'Low-skilled workers face competition from imports and offshoring, lowering their wages, while high-skilled workers and capital owners gain from larger markets.', '1 mark: losers; 1 mark: winners [2]'),
])


@t24_3.add('C3', (2, 3, 4, 5), 'numerical')
def t24_3_data(r, D):
    c = r.choice(COUNTRIES)
    m0, m1 = r.choice([22, 25, 28]), r.choice([12, 14, 16])
    s0, s1 = r.choice([60, 62]), r.choice([72, 75])
    w_lo, w_hi = r.choice([2, 4, 5]), r.choice([18, 22, 30])
    return {'stem': f'Over 20 years of rapid globalisation in {c}, manufacturing’s share of employment fell from {m0}% to {m1}% and services rose from {s0}% to {s1}%. Real wages of low-skilled workers rose by {w_lo}% in total while those of graduates rose by {w_hi}%. Calculate the percentage change in manufacturing’s share of employment and analyse how globalisation could explain these trends.',
            'answer': f'Manufacturing share fell by {num(m0 - m1)} percentage points ({pct(100 * (m1 - m0) / m0, 1)}). Offshoring and import competition shifted manufacturing to lower-cost countries; growth of tradable services; rising demand for skilled workers raised their relative wages, increasing inequality.',
            'key': '% change [1]; offshoring/comparative advantage [1]; skill-biased effect on wages [1]; inequality conclusion [1].', 'type': 'case'}


def _glob_c4(r, D):
    d = ctx(r)
    o0, o1 = r.choice([(35, 70), (40, 85), (25, 60)])
    intro = f'Extract: {d["country"]}’s trade openness ratio has risen from {o0}% to {o1}% since it joined a regional customs union with {d["country2"]} and {d["country3"]}. Manufacturing exports have grown rapidly, but some domestic farmers complain that they cannot compete with imports.'
    parts = [
        lambda r: ('Calculate the percentage change in the openness ratio.', pct(100 * (o1 - o0) / o0, 1), '[1]'),
        lambda r: ('Explain the difference between trade creation and trade diversion in this customs union.', 'Creation: cheaper partner imports replace domestic output; diversion: dearer partner imports replace cheaper non-member imports due to the common external tariff.', '[4]'),
        lambda r: ('Explain why farmers may lose from the customs union.', 'Removal of tariffs exposes them to lower-cost partner producers; prices fall.', '[2]'),
        lambda r: ('Discuss whether membership of the customs union has benefited the country.', 'Export growth, economies of scale, FDI, lower prices vs adjustment costs, diversion, loss of tariff revenue, inequality; judgement.', '[4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='case')


add_many([t24_1, t24_2, t24_3], 'C4', (3, 4, 5), 'case', _glob_c4)
items(t24_1, 'C2', (2, 3, 4), [
    ('Explain how the growth of the internet has contributed to globalisation of the {ind} industry.', 'Lower communication costs allow firms to coordinate global supply chains, sell to customers worldwide and outsource services; information flows freely, increasing competition.', '1 mark: lower communication costs; 1 mark: global supply chains/markets [2]'),
])
items(t24_2, 'C2', (2, 3, 4), [
    ('{country} plans to join a customs union with {country2}. Explain why it must give up control of its tariffs on imports from other countries.', 'A customs union has a common external tariff, so members must apply the same tariff to non-members; otherwise goods would enter via the lowest-tariff member.', '1 mark: CET; 1 mark: reason [2]'),
])
items(t24_3, 'C2', (2, 3, 4), [
    ('A clothing factory in {country} closes after production moves to {country2}. Explain how this illustrates a consequence of globalisation.', 'Firms relocate production to lower-cost countries (comparative advantage, offshoring), causing structural unemployment in the original country but jobs and growth in the new location.', '1 mark: relocation; 1 mark: structural unemployment/gains elsewhere [2]'),
])
essays(t24_1, [
    ('globalisation is mainly the result of technological change rather than government policy',
     'Explain the main features of globalisation.',
     'Transport and ICT innovations lowered trade costs dramatically.',
     'Trade liberalisation, WTO, capital deregulation and opening of economies were essential; both interact.'),
], ['Trade in {country} has doubled as a share of GDP in 30 years.'])
essays(t24_2, [
    ('joining a trading bloc always benefits a country',
     'Explain the difference between a free trade area, a customs union and a common market.',
     'Trade creation, larger markets, economies of scale, FDI.',
     'Trade diversion, loss of sovereignty, adjustment costs, unequal gains; depends on members’ costs and tariffs.'),
], ['{country} is deciding whether to join a customs union with its neighbours.'])
essays(t24_3, [
    ('the benefits of globalisation outweigh the costs for developing economies',
     'Explain the possible benefits of globalisation for developing economies.',
     'Export markets, FDI, technology, lower prices, faster growth.',
     'Exploitation, inequality, environmental damage, volatility and contagion, commodity dependence; depends on policies and institutions.'),
    ('globalisation has harmed workers in developed economies',
     'Explain how globalisation affects employment in developed economies.',
     'Offshoring, import competition, lower wages for low-skilled.',
     'Cheaper goods raise real incomes, new jobs in services and exports, retraining; technology also responsible.'),
], ['Several factories in {country} have moved production overseas in the last decade.', '{country} has become a major exporter of manufactured goods to developed economies.'])
CHAPTERS[24] = [t24_1, t24_2, t24_3]


items(t17_2, 'C2', (1, 2, 3, 4), [
    ('Inflation in {country} is higher than in its main trading partners. Explain the likely effect on its current account.', 'Its exports become less price competitive and imports relatively cheaper, so export volumes fall and imports rise, worsening the current account.', '1 mark: competitiveness; 1 mark: current account worsens [2]'),
    ('{country}’s exports to {country2} rise sharply as {country2} enters a boom. Explain the effect on {country}’s economic growth.', 'Exports are an injection: AD rises and, via the multiplier, real GDP grows; firms may invest more to expand capacity.', '1 mark: injection/AD; 1 mark: multiplier/investment [2]'),
    ('Explain why a fast-growing economy such as {country} may see its current account deficit widen.', 'Rising incomes increase spending on imports (income elasticity of demand for imports is often above 1) faster than exports grow.', '1 mark: income-related imports; 1 mark: exports grow more slowly [2]'),
    ('Explain how a current account deficit could reduce inflationary pressure in {country}.', 'Net imports are a withdrawal from the circular flow, lowering AD; cheaper imports also hold down prices.', '1 mark: lower AD; 1 mark: import competition [2]'),
])

# ---------------------------------------------------------------------------- marks from marking keys
# Fixed and context items end their marking key with the total in brackets, e.g. "... [4]". Use it as the
# item's mark so the stated key and the mark allocation agree.
_TOT = re.compile(r'\[(\d+)\]\s*$')


def _with_marks(fn):
    def g(r, D):
        q = fn(r, D)
        if q and 'marks' not in q and not q.get('options'):
            m = _TOT.search(q['key'])
            if m:
                q['marks'] = max(1, min(6, int(m.group(1))))
        return q
    g.__name__ = fn.__name__
    return g


for _tps in CHAPTERS.values():
    for _tp in _tps:
        for _tpl in _tp.templates:
            if _tpl.name in ('fixed', 'items'):
                _tpl.fn = _with_marks(_tpl.fn)
