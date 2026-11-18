"""Cambridge International A Level Accounting 9706, A2 content (grade 12).

Paper 3 (Financial Accounting) and Paper 4 (Cost and Management Accounting) style items:
partnership changes, limited company capital, published statements and cash flows, IAS,
business purchase and merger, consignment and joint ventures, computerised systems, ratio
analysis, activity-based costing, budgeting, standard costing and investment appraisal.
All figures are generated and the answers / mark points computed from them.
"""
import re
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as Fr
from math import lcm

from ._lib import topic, mcq, compose, num_mcq, PEOPLE

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.2, 1.2)}, 'wordy': True}
CHAPTERS = {}

# ----------------------------------------------------------------------------- helpers

FIRMS = ['Baobab Furnishings', 'Andes Supplies', 'Lotus Retail', 'Harbour Electrics', 'Silk Route Textiles', 'Cedar Hardware',
         'Coral Bay Foods', 'Kilimanjaro Coffee', 'Pampas Leather', 'Monsoon Garments', 'Sahara Solar', 'Fjord Fisheries',
         'Atlas Engineering', 'Orchid Pharmacy', 'Jade Ceramics', 'Tundra Outdoor', 'Mekong Rice Mills', 'Zambezi Timber',
         'Aurora Printing', 'Volcano Spices', 'Lagoon Boatworks', 'Savanna Tours', 'Nile Valley Dairy', 'Pacific Tiles']
COS = ['Kestrel plc', 'Meridian Ltd', 'Odyssey plc', 'Vanguard Ltd', 'Sunbird plc', 'Pinnacle Ltd', 'Horizon plc', 'Tamarind Ltd',
       'Equinox plc', 'Banyan Ltd', 'Sirocco plc', 'Galaxy Ltd', 'Nimbus plc', 'Cobalt Ltd', 'Saffron plc', 'Delta Ltd',
       'Marula plc', 'Condor Ltd', 'Ibis plc', 'Lynx Ltd', 'Monarch plc', 'Kauri Ltd', 'Quetzal plc', 'Osprey Ltd']
YE = ['31 December 2025', '31 March 2026', '30 June 2026', '30 September 2025', '31 December 2026', '31 March 2025', '30 April 2026', '31 July 2025']
PRODUCTS = [('Alpha', 'Beta'), ('Standard', 'Deluxe'), ('Kappa', 'Sigma'), ('Classic', 'Premium'), ('X100', 'X200'), ('Lite', 'Pro'),
            ('Basic', 'Elite'), ('Mono', 'Duo'), ('Orion', 'Vega'), ('Nova', 'Astra')]


def _stem(st):
    st = st.strip()
    if st.endswith('?') or st.endswith('.'):
        return st
    return 'Complete the statement: ' + st + ' …'


def _with_marks(fn, key):
    mk = re.findall(r'\[(\d+)\]', key)
    mk = int(mk[-1]) if mk else None

    def g(r, D):
        q = fn(r, D)
        if q and mk:
            q['marks'] = mk
        return q
    g.__name__ = 'fixed'
    return g


def fixed(t, C, D, entries):
    """Register fixed items with full-sentence stems and marks taken from the key's trailing [n]."""
    ents = [(_stem(e[0]),) + tuple(e[1:]) for e in entries]
    n = len(t.templates)
    t.fixed(C, D, ents)
    for tp, e in zip(t.templates[n:], ents):
        tp.fn = _with_marks(tp.fn, e[2])
    return t


def _hu(x, dp=0):
    """Round half away from zero (accounting convention), tolerant of float noise."""
    q = Decimal(1).scaleb(-dp)
    return Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)


def m(x):
    """Money, whole dollars."""
    v = int(_hu(x))
    return ('-' if v < 0 else '') + f'${abs(v):,}'


def m2(x):
    v = _hu(x, 2)
    return ('-' if v < 0 else '') + f'${abs(v):,.2f}'


def pc(x, dp=1):
    return f'{x:.{dp}f}%'


def nm(x):
    x = round(x)
    return f'{x:,}'


def fa(v, money=m):
    """Variance with F/A label (v > 0 favourable)."""
    if round(v) == 0:
        return '$0 (nil)'
    return f'{money(abs(v))} {"F" if v > 0 else "A"}'


def rs(t):
    return ':'.join(str(x) for x in t)


def firm(r):
    return r.choice(FIRMS)


def co(r):
    return r.choice(COS)


def ye(r):
    return r.choice(YE)


def mm(r, correct, ds, f=m):
    return num_mcq(r, correct, ds, fmtf=f)


def step(r, lo, hi, s):
    """Random multiple of s in [lo, hi]."""
    a, b = max(1, -(-lo // s)), max(1, hi // s)
    return s * r.randint(a, max(a, b))


def dr_cr(x):
    return f'credit {m(x)}' if x > 0 else (f'debit {m(-x)}' if x < 0 else 'no adjustment')


def new_after(r, old):
    """New three-partner ratio in which neither old partner gains."""
    so = sum(old)
    c = [n for n in NEW3 if Fr(n[0], sum(n)) <= Fr(old[0], so) and Fr(n[1], sum(n)) <= Fr(old[1], so)]
    if not c or r.random() < 0.4:
        k = r.choice([3, 4, 5])
        n = (old[0] * (k - 1), old[1] * (k - 1), so)
        from math import gcd
        g = gcd(gcd(n[0], n[1]), n[2])
        return tuple(x // g for x in n)
    return r.choice(c)


OLD2 = [(3, 2), (1, 1), (2, 1), (3, 1), (5, 3), (4, 1), (7, 3), (3, 4), (2, 3)]
OLD3 = [(3, 2, 1), (2, 2, 1), (5, 3, 2), (4, 3, 1), (2, 1, 1), (3, 3, 2), (1, 1, 1), (4, 4, 1), (5, 4, 1)]
NEW3 = [(3, 2, 1), (2, 2, 1), (5, 3, 2), (4, 3, 1), (2, 1, 1), (3, 3, 2), (1, 1, 1), (4, 4, 1), (5, 4, 1), (6, 3, 1)]


# ===================================================================== 1 Partnership changes
t1_1 = topic('Goodwill: nature, valuation and treatment', 'goodwill: nature, valuation and treatment on partnership change', 'goodwill', 'valuation')
fixed(t1_1, 'C1', (1, 2), [
    ('Which statement best defines goodwill?', 'The amount by which the value of a business as a whole exceeds the fair value of its separable net assets',
     'Goodwill = value of business as a whole − fair value of identifiable net assets [1].',
     ['The total of the non-current assets of a business', 'The profit earned by a business in its best year', 'The amount owed to the business by its customers']),
    ('In which part of a statement of financial position would purchased goodwill be shown?', 'Intangible non-current assets', 'Purchased goodwill is an intangible non-current asset [1].',
     ['Current assets', 'Non-current liabilities', 'Equity']),
    ('A partnership does not keep a goodwill account. On admission of a new partner, goodwill is first credited to the old partners in their', 'old profit-sharing ratio',
     'Create goodwill: Dr Goodwill, Cr old partners in OLD ratio; write off: Cr Goodwill, Dr all partners in NEW ratio [1].',
     ['new profit-sharing ratio', 'capital ratio', 'equal shares regardless of agreement']),
    ('Goodwill is valued at three years\' purchase of the average profits. This means that goodwill equals', 'average annual profit × 3', 'Years\' purchase method: goodwill = average profit × number of years [1].',
     ['average annual profit ÷ 3', 'the total profit of the last three years ÷ 2', 'the capital employed × 3']),
    ('Which factor is LEAST likely to give a business goodwill?', 'Holding a large amount of slow-moving inventory', 'Goodwill arises from reputation, location, skilled staff, loyal customers; slow inventory adds nothing [1].',
     ['A loyal customer base', 'A convenient trading location', 'A skilled and experienced workforce']),
    ('Super profit used in valuing goodwill is', 'average profit less a normal return on capital employed and partners\' notional salaries',
     'Super profit = average profit − (normal return on capital + reward for partners\' work) [1].',
     ['gross profit less expenses', 'the highest profit earned in recent years', 'profit for the year plus interest on capital']),
])
fixed(t1_1, 'C2', (2, 3, 4), [
    ('Explain why goodwill must be valued and adjusted for when a new partner is admitted.', 'Goodwill was built up by the old partners; the new partner will share future profits that partly come from it, so the old partners must be compensated for the share they give up.',
     'Goodwill created by existing partners [1]; new partner benefits from future profits it generates [1]; adjustment compensates old partners for share sacrificed [1] [3]'),
    ('Explain why many partnerships do not keep a goodwill account in their books after a change in partners.', 'Goodwill is inherent (not purchased); its value is subjective and fluctuates, and IAS 38 does not allow internally generated goodwill to be recognised, so it is written off after the adjustment.',
     'Subjective/uncertain valuation [1]; internally generated, not purchased [1]; prudence / IAS 38 does not allow recognition [1] [3]'),
    ('Distinguish between purchased goodwill and inherent (non-purchased) goodwill.', 'Purchased goodwill arises when one business buys another and pays more than the fair value of its net assets; it can be recorded. Inherent goodwill is built up internally and is not recorded.',
     'Purchased: paid for on acquisition, recognised [1]; inherent: internally generated, not recognised [1] [2]'),
    ('State and explain two limitations of valuing goodwill on the basis of past average profits.', 'Past profits may not be repeated in future (e.g. key partner leaving, new competition); profits may include one-off items that distort the average.',
     'Past not a guide to future [1] + reason [1]; abnormal items distort average [1] + reason [1] [4]'),
    ('Explain why goodwill is written off in the new profit-sharing ratio after being credited in the old ratio.', 'Crediting in the old ratio rewards the partners who built it; debiting in the new ratio charges all partners who now share its future benefit, so the net effect transfers value from gaining to sacrificing partners.',
     'Old ratio rewards creators [1]; new ratio charges future beneficiaries [1]; net effect = sacrifice/gain [1] [3]'),
])


@t1_1.add('C3', (1, 2, 3, 4, 5))
def t11_value(r, D):
    nyrs = 3 if D <= 2 else 4
    profits = [step(r, 40000, 160000, 500 if D > 2 else 1000) for _ in range(nyrs)]
    yrs = r.choice([2, 3, 4]) if D < 4 else r.choice([1.5, 2.5, 3])
    fm = firm(r)
    labels = [f'{2021 + i}' for i in range(nyrs)]
    lst = ', '.join(f'{l} {m(p)}' for l, p in zip(labels, profits))
    note, adj = '', list(profits)
    if D >= 4:
        k = r.randrange(nyrs)
        g = step(r, 4000, 18000, 500)
        adj[k] -= g
        note = f' The {labels[k]} profit included a one-off gain of {m(g)} on the sale of land, which is not expected to recur.'
    if D >= 3:
        w = list(range(1, nyrs + 1))
        avg = Fr(sum(a * b for a, b in zip(adj, w)), sum(w))
        how = f'weighted average profit (weights {", ".join(map(str, w))} with the most recent year weighted highest)'
        wk = f'Σ(profit × weight) = {m(sum(a * b for a, b in zip(adj, w)))}; ÷ {sum(w)} = {m(avg)}'
    else:
        avg = Fr(sum(adj), nyrs)
        how = 'simple average profit'
        wk = f'total = {m(sum(adj))}; ÷ {nyrs} = {m(avg)}'
    G = avg * Fr(str(yrs))
    stem = f'The partners of {fm} have agreed to value goodwill at {yrs} years\' purchase of the {how}. Profits for the last {nyrs} years were: {lst}.{note} Calculate the value of goodwill.'
    key = (f'Adjust for one-off gain [1]; ' if D >= 4 else '') + f'{wk} [1]; goodwill = {m(avg)} × {yrs} = {m(G)} [1]'
    if D == 1:
        opts, ans = mm(r, G, [avg, sum(adj) * yrs, G * 2 / 3 if yrs == 3 else G * 1.5, G + 10000])
        return {'stem': stem.replace('Calculate the value', 'What is the value'), 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem, 'answer': m(G), 'key': key, 'marks': 2 + (D >= 3) + (D >= 4)}


@t1_1.add('C3', (2, 3, 4, 5))
def t11_super(r, D):
    P = step(r, 70000, 220000, 1000)
    K = step(r, 200000, 900000, 10000)
    i = r.choice([5, 6, 8, 10, 12])
    n = r.choice([2, 3])
    sal = step(r, 8000, 30000, 1000) * n
    yrs = r.choice([2, 3, 4, 5])
    normal = K * i // 100
    sp = P - normal - sal
    if sp <= 5000:
        P += normal + sal - sp + step(r, 8000, 30000, 1000)
        sp = P - normal - sal
    G = sp * yrs
    fm = firm(r)
    stem = (f'{fm} is owned by {n} partners. Average annual profits are {m(P)} and capital employed is {m(K)}. A normal return on capital in this industry is {i}% '
            f'and the partners could each earn {m(sal // n)} a year in employment elsewhere. Goodwill is to be valued at {yrs} years\' purchase of super profits. Calculate the value of goodwill.')
    return {'stem': stem, 'answer': m(G),
            'key': f'Normal return = {i}% × {m(K)} = {m(normal)} [1]; notional salaries = {n} × {m(sal // n)} = {m(sal)} [1]; super profit = {m(P)} − {m(normal)} − {m(sal)} = {m(sp)} [1]; goodwill = {m(sp)} × {yrs} = {m(G)} [1]',
            'marks': 4}


def _gw_adm(r):
    A, B, C = r.sample(PEOPLE, 3)
    old = r.choice(OLD2)
    new = new_after(r, old)
    so, sn = sum(old), sum(new)
    base = lcm(so, sn) * 100
    G = step(r, 30000, 200000, base)
    adj = [G * Fr(old[0], so) - G * Fr(new[0], sn), G * Fr(old[1], so) - G * Fr(new[1], sn), -G * Fr(new[2], sn)]
    return A, B, C, old, new, G, adj


@t1_1.add('C3', (1, 2, 3, 4))
def t11_adm(r, D):
    A, B, C, old, new, G, adj = _gw_adm(r)
    frame = r.choice([
        f'{A} and {B} are partners sharing profits and losses {rs(old)}. They admit {C} and the new ratio is {A} {new[0]}, {B} {new[1]}, {C} {new[2]}. Goodwill is valued at {m(G)}; no goodwill account is to be maintained.',
        f'{C} joins the partnership of {A} and {B} (old ratio {rs(old)}). Future profits are to be shared {rs(new)} between {A}, {B} and {C}. Goodwill of {m(G)} is to be adjusted through the capital accounts only.',
        f'In the firm of {A} and {B} profits were shared {rs(old)}. On the admission of {C}, goodwill was agreed at {m(G)} and the new profit-sharing ratio {A}:{B}:{C} became {rs(new)}. Goodwill will not remain in the books.'])
    key = (f'Create goodwill in old ratio: {A} Cr {m(G * Fr(old[0], sum(old)))}, {B} Cr {m(G * Fr(old[1], sum(old)))} [1]; write off in new ratio: {A} Dr {m(G * Fr(new[0], sum(new)))}, '
           f'{B} Dr {m(G * Fr(new[1], sum(new)))}, {C} Dr {m(G * Fr(new[2], sum(new)))} [1]; net: {A} {dr_cr(adj[0])}, {B} {dr_cr(adj[1])}, {C} {dr_cr(adj[2])} [1]')
    if D == 1:
        opts, ans = mm(r, -adj[2], [G * Fr(new[2], sum(new)) * 2, G / 3, G * Fr(old[1], sum(old)), G - (-adj[2]), G * Fr(1, sum(new))])
        return {'stem': frame + f' By how much is {C}\'s capital account debited for goodwill?', 'options': opts, 'answer': ans, 'key': key}
    q = 'Calculate the net adjustment to each partner\'s capital account, stating whether it is a debit or a credit.'
    if D >= 3:
        q = 'Prepare the journal entries (narratives not required) and calculate the net effect on each partner\'s capital account.'
    return {'stem': frame + ' ' + q, 'answer': f'{A} {dr_cr(adj[0])}; {B} {dr_cr(adj[1])}; {C} {dr_cr(adj[2])}', 'key': key, 'marks': 3 + (D >= 3)}


@t1_1.add('C2', (2, 3, 4), 'explain')
def t11_err(r, D):
    A, B, C, old, new, G, adj = _gw_adm(r)
    wrong = r.choice(['old', 'new'])
    if wrong == 'old':
        desc = f'credited and then debited goodwill of {m(G)} to {A} and {B} only, in the old ratio {rs(old)}'
        fix = 'Writing off in the old ratio between the old partners gives no net adjustment at all, so the old partners receive no compensation and the new partner pays nothing.'
    else:
        desc = f'credited goodwill of {m(G)} to all three partners in the new ratio {rs(new)} and left it in the books'
        fix = 'Goodwill must be credited to the OLD partners in the OLD ratio (they created it) and written off in the NEW ratio; crediting the new partner rewards him for goodwill he did not create.'
    return {'stem': f'On the admission of {C} to the partnership of {A} and {B}, a trainee {desc}. The partners did not want a goodwill account to remain. Explain the error and state the correct net adjustment for {C}.',
            'answer': f'{fix} Correct net adjustment: {C} {dr_cr(adj[2])}.',
            'key': f'Identifies wrong ratio/treatment [1]; explains old partners created goodwill [1]; {C} {dr_cr(adj[2])} [1] [3]'}


t1_2 = topic('Revaluation of assets on admission or retirement', 'revaluation of assets on admission or retirement', 'revaluation account', 'revaluation')
fixed(t1_2, 'C1', (1, 2), [
    ('On revaluation, an increase in the value of premises is recorded by', 'debiting premises and crediting the revaluation account', 'Increase in asset: Dr asset, Cr revaluation [1].',
     ['debiting the revaluation account and crediting premises', 'debiting premises and crediting the new partner\'s capital', 'crediting premises and debiting bank']),
    ('A profit on revaluation is shared between the partners in', 'the old profit-sharing ratio', 'The gain arose while the old partnership existed, so old ratio [1].',
     ['the new profit-sharing ratio', 'the ratio of their capitals', 'equal shares']),
    ('Creating an allowance for irrecoverable debts on revaluation will', 'reduce the revaluation profit', 'Dr revaluation, Cr allowance: a loss on revaluation [1].',
     ['increase the revaluation profit', 'have no effect on the revaluation account', 'increase the trade receivables']),
    ('Which account is closed by transferring its balance to the partners\' capital accounts?', 'Revaluation account', 'Revaluation profit/loss is transferred to capitals in old ratio [1].',
     ['Premises account', 'Trade payables account', 'Bank account']),
    ('Why are assets revalued when a partner retires?', 'So the retiring partner receives his share of gains or losses in value up to the date of retirement',
     'Book values may differ from fair values; retiring partner entitled to share of changes [1].',
     ['To reduce the tax payable by the partnership', 'Because IAS 16 requires revaluation every year', 'So that the new ratio can be calculated']),
])
fixed(t1_2, 'C2', (2, 3, 4), [
    ('Explain why a revaluation profit is shared in the old profit-sharing ratio and not the new ratio.', 'The change in value occurred while the old partners owned the business, so it belongs to them; using the new ratio would give the incoming partner a share of gains made before he joined.',
     'Gain earned under old partnership [1]; new partner should not benefit from past gains [1] [2]'),
    ('A partnership decides that the revalued amounts will not be kept in the books. Explain how this is recorded.', 'The revaluation profit/loss is credited to the old partners in the old ratio, then reversed by debiting all partners in the new ratio (a memorandum revaluation), so assets stay at original book values.',
     'Old partners credited in old ratio [1]; reversed through all partners in new ratio [1]; assets remain at book value [1] [3]'),
    ('Distinguish between a revaluation account and a realisation account.', 'A revaluation account records changes in asset and liability values when the business continues after a change in partners; a realisation account records the sale of assets and settlement of liabilities when the partnership is dissolved.',
     'Revaluation: business continues, values change [1]; realisation: business ends, assets sold [1] [2]'),
    ('Explain the effect of a revaluation loss on the capital accounts of the old partners.', 'The loss is debited to the old partners in their old ratio, reducing their capital balances, because the assets were overstated while they owned the business.',
     'Debited in old ratio [1]; reduces capital, assets were overstated [1] [2]'),
])


def _reval(r, D, ratio):
    s = sum(ratio) * 100
    items = []
    up = step(r, 20000, 90000, s)
    items.append(('Premises', f'increased by {m(up)}', up))
    eq = step(r, 2000, 15000, s)
    items.append(('Equipment', f'reduced by {m(eq)}', -eq))
    if D >= 2:
        inv = step(r, 1000, 8000, s)
        items.append(('Inventory', f'written down by {m(inv)}', -inv))
    if D >= 3:
        rec = step(r, 20000, 60000, 1000)
        p = r.choice([2, 4, 5])
        al = rec * p // 100
        diff = (-al) % s
        rec_note = f'an allowance for irrecoverable debts of {p}% to be created on trade receivables of {m(rec)}'
        items.append(('Trade receivables', rec_note, -al))
        if diff:
            items.append(('Vehicles', f'increased by {m(diff)}', diff))
    if D >= 4:
        acc = step(r, 1000, 5000, s)
        items.append(('Accrued expenses', f'an unrecorded liability of {m(acc)} for electricity to be recognised', -acc))
    net = sum(v for _, _, v in items)
    return items, net


@t1_2.add('C3', (1, 2, 3, 4, 5))
def t12_calc(r, D):
    two = r.random() < 0.6
    if two:
        names = r.sample(PEOPLE, 2); ratio = r.choice(OLD2)
    else:
        names = r.sample(PEOPLE, 3); ratio = r.choice(OLD3)
    items, net = _reval(r, D, ratio)
    event = r.choice(['the admission of a new partner', f'the retirement of {names[-1]}', 'a change in the profit-sharing ratio'])
    ppl = ', '.join(names[:-1]) + ' and ' + names[-1]
    desc = '; '.join(f'{a}: {b}' for a, b, _ in items)
    stem = f'{ppl} share profits {rs(ratio)}. On {event} the following revaluations were agreed — {desc}. Calculate the profit or loss on revaluation and each partner\'s share.'
    shares = [net * Fr(x, sum(ratio)) for x in ratio]
    word = 'profit' if net >= 0 else 'loss'
    ans = f'Revaluation {word} {m(abs(net))}: ' + ', '.join(f'{n} {m(abs(v))}' for n, v in zip(names, shares))
    key = 'Gains: ' + ', '.join(f'{a} {m(v)}' for a, _, v in items if v > 0) + ' ; losses: ' + ', '.join(f'{a} {m(-v)}' for a, _, v in items if v < 0) + f' [1 per 2 items]; net {word} {m(abs(net))} [1]; shared {rs(ratio)} old ratio [1]'
    if D == 1:
        opts, ans2 = mm(r, net, [net + 2 * items[1][2], -net, items[0][2], net + items[1][2] * 3])
        return {'stem': stem.replace('Calculate the profit or loss on revaluation and each partner\'s share.', 'What is the net profit (loss) on revaluation?'), 'options': opts, 'answer': ans2, 'key': key}
    return {'stem': stem, 'answer': ans, 'key': key, 'marks': 2 + len(items) // 2 + 1}


@t1_2.add('C2', (2, 3, 4), 'explain')
def t12_err(r, D):
    A, B, C = r.sample(PEOPLE, 3)
    old = r.choice(OLD2)
    new = r.choice(NEW3)
    s = lcm(sum(old), sum(new)) * 100
    gain = step(r, 6000, 48000, s)
    sh_old = [gain * Fr(x, sum(old)) for x in old]
    sh_new = [gain * Fr(x, sum(new)) for x in new]
    return {'stem': f'{A} and {B} (ratio {rs(old)}) admitted {C}; the new ratio is {rs(new)}. A revaluation profit of {m(gain)} was shared {A} {m(sh_new[0])}, {B} {m(sh_new[1])} and {C} {m(sh_new[2])}. Identify the error and state the correct entries in the capital accounts.',
            'answer': f'The profit was shared in the new ratio including {C}. It should be shared in the old ratio between {A} and {B} only: {A} Cr {m(sh_old[0])}, {B} Cr {m(sh_old[1])}; {C} nil.',
            'key': f'Error: new ratio used / {C} included [1]; reason: gain arose before admission [1]; correct {A} {m(sh_old[0])}, {B} {m(sh_old[1])} [1] [3]'}


t1_3 = topic('Admission and retirement of a partner: capital account adjustments', 'admission and retirement of a partner: capital account adjustments', 'retirement', 'admission', 'capital account')
fixed(t1_3, 'C1', (1, 2), [
    ('A retiring partner is not paid immediately. The balance owed to him should be transferred to', 'a loan account (shown as a liability)', 'Amount due unpaid → retiring partner\'s loan account [1].',
     ['the remaining partners\' current accounts', 'the realisation account', 'the goodwill account']),
    ('The sacrificing ratio is the ratio in which', 'old partners give up their share of profit to the new partner', 'Sacrifice = old share − new share [1].',
     ['new partners share losses', 'partners contribute capital', 'goodwill is written off']),
    ('On retirement, the retiring partner\'s current account balance is', 'transferred to his capital account (or paid out with it)', 'Close current account to capital before settlement [1].',
     ['written off to the income statement', 'shared among remaining partners', 'credited to the revaluation account']),
    ('Which of the following does NOT change the amount due to a retiring partner?', 'The new profit-sharing ratio of the remaining partners', 'Amount due = capital + current + share of goodwill + share of revaluation (old ratio) [1].',
     ['His share of the revaluation profit', 'His share of goodwill', 'The balance on his current account']),
    ('A new partner pays a premium for goodwill in cash, which is kept in the business. The premium is credited to', 'the sacrificing partners\' capital accounts in the sacrificing ratio', 'Premium compensates sacrificing partners [1].',
     ['the new partner\'s capital account', 'the income statement', 'all partners in the new ratio']),
])
fixed(t1_3, 'C2', (2, 3, 4), [
    ('Explain why the remaining partners may prefer to pay a retiring partner by instalments through a loan account.', 'Paying in full may drain the bank balance and working capital; a loan spreads the outflow, though interest is payable and it adds gearing.',
     'Liquidity preserved [1]; interest cost/gearing noted [1] [2]'),
    ('Explain why a partner\'s capital account and current account are kept separately.', 'Capital accounts show the fixed amount invested; current accounts record the regular items (share of profit, interest, salary, drawings), so fluctuations do not obscure the agreed capital.',
     'Capital fixed by agreement [1]; current account for appropriation and drawings [1] [2]'),
    ('Explain two ways in which the remaining partners could finance the payment to a retiring partner.', 'Introduce extra capital from their own resources; take a bank loan; sell surplus assets; admit a new partner who brings capital.',
     'Any two methods [1 each] with brief explanation [1 each] [4]'),
])


@t1_3.add('C3', (1, 2, 3, 4, 5))
def t13_ret(r, D):
    A, B, C = r.sample(PEOPLE, 3)
    old = r.choice(OLD3)
    so = sum(old)
    new2 = r.choice([(1, 1), (3, 2), (2, 1), (3, 1), (5, 3)])
    base = lcm(so, sum(new2)) * 100
    cap = step(r, 30000, 120000, 1000)
    cur = step(r, -6000, 15000, 100) if D >= 3 else step(r, 1000, 12000, 100)
    if cur == 0:
        cur = 1500
    G = step(r, 30000, 150000, base)
    R = step(r, 6000, 40000, base) if D >= 2 else 0
    gs = G * Fr(old[2], so)
    rsh = R * Fr(old[2], so)
    due = cap + cur + gs + rsh
    cash = step(r, 10000, int(due * 0.6), 1000)
    loan = due - cash
    cur_txt = f'a current account {"credit" if cur > 0 else "debit"} balance of {m(abs(cur))}'
    stem = (f'{A}, {B} and {C} share profits {rs(old)}. {C} retires on 31 May. At that date {C} has a capital balance of {m(cap)} and {cur_txt}. Goodwill is valued at {m(G)} (no goodwill account is kept)'
            + (f' and a revaluation profit of {m(R)} has been calculated' if R else '') + f'. {C} is paid {m(cash)} in cash and the rest is transferred to a loan account.')
    key = f'Capital {m(cap)} {"+" if cur > 0 else "−"} current {m(abs(cur))} [1]; goodwill share {old[2]}/{so} × {m(G)} = {m(gs)} [1]; ' + (f'revaluation share {m(rsh)} [1]; ' if R else '') + f'total due {m(due)} [1]; loan = {m(due)} − {m(cash)} = {m(loan)} [1]'
    if D == 1:
        opts, ans = mm(r, loan, [due, loan - gs, cap - cash, loan + cash // 2])
        return {'stem': stem + f' What is the balance on {C}\'s loan account?', 'options': opts, 'answer': ans, 'key': key}
    q = f' Calculate the total amount due to {C} and the balance transferred to {C}\'s loan account.'
    if D >= 4:
        nA = G * Fr(old[0], so) - G * Fr(new2[0], sum(new2))
        nB = G * Fr(old[1], so) - G * Fr(new2[1], sum(new2))
        q += f' {A} and {B} will share future profits {rs(new2)}; calculate the net goodwill adjustment to their capital accounts.'
        return {'stem': stem + q, 'answer': f'Due {m(due)}; loan {m(loan)}; {A} {dr_cr(nA)}, {B} {dr_cr(nB)}',
                'key': key + f'; {A}: Cr {m(G * Fr(old[0], so))} Dr {m(G * Fr(new2[0], sum(new2)))} = {dr_cr(nA)}; {B}: {dr_cr(nB)} [2]', 'marks': 6}
    return {'stem': stem + q, 'answer': f'Total due {m(due)}; loan account {m(loan)}', 'key': key, 'marks': 4 + bool(R)}


@t1_3.add('C3', (2, 3, 4))
def t13_prem(r, D):
    A, B, C = r.sample(PEOPLE, 3)
    old = r.choice(OLD2)
    new = new_after(r, old)
    sacA = Fr(old[0], sum(old)) - Fr(new[0], sum(new))
    sacB = Fr(old[1], sum(old)) - Fr(new[1], sum(new))
    cshare = Fr(new[2], sum(new))
    base = lcm(sacA.denominator, sacB.denominator, cshare.denominator) * 100
    G = step(r, 40000, 200000, base)
    prem = G * cshare
    capC = step(r, 20000, 80000, 1000)
    pa, pb = G * sacA, G * sacB
    stem = (f'{A} and {B} share profits {rs(old)}. {C} is admitted for a {new[2]}/{sum(new)} share, bringing {m(capC)} as capital and a cash premium for goodwill. Goodwill of the firm is valued at {m(G)}; the new ratio is {rs(new)}. '
            f'Calculate (a) the sacrificing ratio, (b) the premium {C} pays and (c) how it is credited to {A} and {B}.')
    ss = f'{sacA.numerator * (lcm(sacA.denominator, sacB.denominator) // sacA.denominator)}:{sacB.numerator * (lcm(sacA.denominator, sacB.denominator) // sacB.denominator)}' if sacA and sacB else ('all ' + (A if sacA else B))
    return {'stem': stem, 'answer': f'(a) {A} {sacA}, {B} {sacB} (ratio {ss}) (b) {m(prem)} (c) {A} Cr {m(pa)}, {B} Cr {m(pb)}',
            'key': f'(a) old − new: {A} {Fr(old[0], sum(old))} − {Fr(new[0], sum(new))} = {sacA}; {B} {Fr(old[1], sum(old))} − {Fr(new[1], sum(new))} = {sacB} [2] (b) {cshare} × {m(G)} = {m(prem)} [1] (c) in sacrificing ratio: {A} {m(pa)}, {B} {m(pb)} [2]',
            'marks': 5, 'type': 'multi_step'}


def _p_c4(r, D):
    A, B, C = r.sample(PEOPLE, 3)
    old = r.choice(OLD2)
    new = r.choice(NEW3)
    so, sn = sum(old), sum(new)
    base = lcm(so, sn) * 100
    capA, capB = step(r, 40000, 150000, 1000), step(r, 30000, 120000, 1000)
    capC = step(r, 25000, 90000, 1000)
    G = step(r, 30000, 150000, base)
    up = step(r, 20000, 80000, base); dn = step(r, 2000, 12000, base)
    R = up - dn
    gA = G * Fr(old[0], so) - G * Fr(new[0], sn)
    gB = G * Fr(old[1], so) - G * Fr(new[1], sn)
    gC = -G * Fr(new[2], sn)
    rA, rB = R * Fr(old[0], so), R * Fr(old[1], so)
    fA, fB, fC = capA + rA + gA, capB + rB + gB, capC + gC
    yr = ye(r)
    intro = r.choice([
        f'{A} and {B} are in partnership trading as {firm(r)}, sharing profits {rs(old)}. Their capital balances are {A} {m(capA)} and {B} {m(capB)}. On 1 April {C} is admitted, paying {m(capC)} into the business bank account as capital.',
        f'The partnership of {A} (capital {m(capA)}) and {B} (capital {m(capB)}) shares profits and losses {rs(old)}. {C} joins the firm and brings {m(capC)} in cash as capital.',
        f'{firm(r)} is owned by {A} and {B}, who share profits {rs(old)} and have capital account balances of {m(capA)} and {m(capB)}. They admit {C}, who introduces capital of {m(capC)} by bank transfer.'])
    intro += f' Premises are revalued upwards by {m(up)} and equipment downwards by {m(dn)}; the new values are to be kept. Goodwill is valued at {m(G)} but no goodwill account is to remain. The new profit-sharing ratio for {A}, {B} and {C} is {rs(new)}.'
    parts = [
        lambda r: ('Calculate the profit on revaluation and each old partner\'s share.', f'{m(R)}: {A} {m(rA)}, {B} {m(rB)}', f'{m(up)} − {m(dn)} = {m(R)} [1]; old ratio {rs(old)} [1] [2]'),
        lambda r: ('Calculate the net goodwill adjustment for each partner.', f'{A} {dr_cr(gA)}, {B} {dr_cr(gB)}, {C} {dr_cr(gC)}', f'Cr old ratio, Dr new ratio [1]; correct nets [2] [3]'),
        lambda r: ('Prepare the partners\' capital accounts in columnar form showing the balances after the admission.', f'{A} {m(fA)}, {B} {m(fB)}, {C} {m(fC)}',
                   f'Opening balances and cash [1]; revaluation [1]; goodwill Cr old/Dr new [2]; closing {A} {m(fA)}, {B} {m(fB)}, {C} {m(fC)} [2] [6]'),
        lambda r: (f'Explain why {C} should not receive any share of the revaluation profit.', f'The increase in value arose before {C} joined; it belongs to the old partners.', 'Gain before admission [1]; old partners entitled [1] [2]'),
        lambda r: (f'Advise {C} on one benefit and one drawback of joining the partnership rather than starting a business alone.', 'Benefit: shares an established customer base/goodwill and expertise. Drawback: unlimited liability for partnership debts / shared decision-making and profits.',
                   'Benefit with reason [1]; drawback with reason [1]; conclusion [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


for _t in (t1_1, t1_2, t1_3):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_p_c4)


def _ret_c4(r, D):
    A, B, C = r.sample(PEOPLE, 3)
    old = r.choice(OLD3)
    new2 = r.choice([(1, 1), (3, 2), (2, 1), (3, 1)])
    so = sum(old)
    base = lcm(so, sum(new2)) * 100
    caps = [step(r, 30000, 120000, 1000) for _ in range(3)]
    G = step(r, 36000, 150000, base)
    R = step(r, -12000, 40000, base)
    if R == 0:
        R = base * 10
    gs = G * Fr(old[2], so); rsh = R * Fr(old[2], so)
    due = caps[2] + gs + rsh
    cash = step(r, 10000, int(due * 0.5), 1000)
    loan = due - cash
    rate = r.choice([5, 6, 8])
    nA = G * Fr(old[0], so) - G * Fr(new2[0], sum(new2))
    nB = G * Fr(old[1], so) - G * Fr(new2[1], sum(new2))
    intro = (f'{A}, {B} and {C} share profits {rs(old)} in {firm(r)}. Capital balances (after current accounts have been transferred) are {A} {m(caps[0])}, {B} {m(caps[1])} and {C} {m(caps[2])}. {C} retires. '
             f'Goodwill is valued at {m(G)} (no goodwill account is kept) and the revaluation {"profit" if R > 0 else "loss"} is {m(abs(R))}. {C} receives {m(cash)} immediately; the balance is left as a loan at {rate}% interest. {A} and {B} will share profits {rs(new2)}.')
    parts = [
        lambda r: (f'Calculate the total amount due to {C}.', m(due), f'{m(caps[2])} + goodwill {m(gs)} {"+" if R > 0 else "−"} revaluation {m(abs(rsh))} = {m(due)} [3]'),
        lambda r: (f'Calculate the balance on {C}\'s loan account and the annual interest on it.', f'{m(loan)}; interest {m(loan * rate / 100)}', f'{m(due)} − {m(cash)} = {m(loan)} [1]; × {rate}% = {m(loan * rate / 100)} [1] [2]'),
        lambda r: (f'Calculate the net goodwill adjustment to the capital accounts of {A} and {B}.', f'{A} {dr_cr(nA)}; {B} {dr_cr(nB)}', f'Cr old ratio, Dr new ratio {rs(new2)} [1]; {A} {dr_cr(nA)} [1]; {B} {dr_cr(nB)} [1] [3]'),
        lambda r: (f'Explain how the loan to {C} will be presented in the statement of financial position.', 'As a liability: non-current if repayable after 12 months, current for any instalment due within 12 months.', 'Liability [1]; current/non-current split [1] [2]'),
        lambda r: (f'Evaluate whether {A} and {B} should pay {C} in full now instead of using a loan.', f'Paying {m(due)} at once avoids {rate}% interest but could leave the firm short of working capital; a loan protects liquidity but adds finance cost and gearing. Decision depends on the bank balance.',
                   'Argument for [1]; argument against [1]; reference to interest/liquidity figures [1]; justified conclusion [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t1_3.add('C4', (2, 3, 4, 5), 'multi_step')(_ret_c4)
t1_3.add('C3', (4, 5), 'multi_step')(_ret_c4)
t1_1.add('C4', (3, 4, 5), 'multi_step')(_ret_c4)

t1_4 = topic('Dissolution of a partnership: realisation account', 'dissolution of a partnership: realisation account', 'dissolution', 'realisation')
fixed(t1_4, 'C1', (1, 2), [
    ('On dissolution, the book value of non-current assets is transferred to the', 'debit side of the realisation account', 'Dr Realisation, Cr asset accounts [1].',
     ['credit side of the realisation account', 'partners\' current accounts', 'income statement']),
    ('A partner takes over a vehicle at an agreed value on dissolution. The entry is', 'debit the partner\'s capital account, credit the realisation account', 'Asset taken over: Dr capital, Cr realisation [1].',
     ['debit realisation account, credit the partner\'s capital account', 'debit vehicles, credit bank', 'debit bank, credit realisation account']),
    ('Discount received on settling trade payables during dissolution is', 'a credit to the realisation account (a gain)', 'Payables settled for less than book value: gain to realisation [1].',
     ['a debit to the realisation account', 'credited to the bank account', 'ignored because the business is closing']),
    ('The final entry to close the bank account on dissolution is payment to the partners of', 'the closing balances on their capital accounts', 'Bank pays the credit balances on capital accounts [1].',
     ['their share of the realisation profit only', 'their original capital contributions', 'equal amounts']),
    ('Dissolution expenses paid by the firm are', 'debited to the realisation account', 'Dr Realisation, Cr Bank [1].',
     ['credited to the realisation account', 'debited to trade payables', 'credited to the partners\' capital accounts']),
])
fixed(t1_4, 'C2', (2, 3, 4), [
    ('Explain the purpose of a realisation account.', 'It records the sale of assets and settlement of liabilities on dissolution, so the profit or loss on realisation can be calculated and shared between the partners in their profit-sharing ratio.',
     'Records disposal of assets/liabilities [1]; finds profit or loss shared in PSR [1] [2]'),
    ('State two reasons why a partnership may be dissolved.', 'Death, retirement or bankruptcy of a partner; expiry of an agreed term; disagreement between partners; business no longer profitable; court order.',
     'Any two [1 each] [2]'),
    ('Explain why the bank account and cash are not transferred to the realisation account on dissolution.', 'Cash is not "realised" — it is already in money form and is used to pay liabilities and partners, so it stays in the bank account.',
     'Cash already realised [1]; used to settle with creditors/partners [1] [2]'),
])


@t1_4.add('C3', (1, 2, 3, 4, 5))
def t14_real(r, D):
    two = D <= 3
    names = r.sample(PEOPLE, 2 if two else 3)
    ratio = r.choice(OLD2) if two else r.choice(OLD3)
    s = sum(ratio) * 100
    nca = step(r, 60000, 200000, 1000); inv = step(r, 8000, 40000, 100); rec = step(r, 6000, 30000, 100)
    pay = step(r, 5000, 25000, 100)
    p_nca = nca + step(r, -30000, 40000, 500); p_inv = inv - step(r, 500, 6000, 100); p_rec = rec - step(r, 200, 2000, 100)
    disc = step(r, 100, 1500, 100) if D >= 2 else 0
    exp = step(r, 500, 4000, 100)
    tk = step(r, 4000, 15000, 500) if D >= 3 else 0
    bvv = step(r, 3000, 14000, 500) if tk else 0
    profit = (p_nca + p_inv + p_rec + tk + disc) - (nca + inv + rec + bvv + exp)
    fix = (-profit) % s
    p_nca += fix; profit += fix
    shares = [profit * Fr(x, sum(ratio)) for x in ratio]
    ppl = ' and '.join([', '.join(names[:-1]), names[-1]])
    lines = [f'Non-current assets (book value {m(nca)}) were sold for {m(p_nca)}', f'inventory (book value {m(inv)}) sold for {m(p_inv)}', f'trade receivables of {m(rec)} collected {m(p_rec)}']
    if tk:
        lines.append(f'{names[0]} took over a vehicle with a book value of {m(bvv)} at an agreed value of {m(tk)}')
    if disc:
        lines.append(f'trade payables of {m(pay)} were settled for {m(pay - disc)}')
    lines.append(f'dissolution expenses were {m(exp)}')
    stem = f'{ppl} dissolved their partnership, in which they shared profits {rs(ratio)}. ' + '; '.join(lines) + '. Calculate the profit or loss on realisation and each partner\'s share.'
    word = 'profit' if profit >= 0 else 'loss'
    key = (f'Dr side: assets at book value {m(nca + inv + rec + bvv)} + expenses {m(exp)} [1]; Cr side: proceeds {m(p_nca + p_inv + p_rec)}' + (f' + asset taken over {m(tk)}' if tk else '') + (f' + discount on payables {m(disc)}' if disc else '')
           + f' [1]; {word} {m(abs(profit))} [1]; shares ' + ', '.join(f'{n} {m(abs(v))}' for n, v in zip(names, shares)) + ' [1]')
    if D == 1:
        opts, ans = mm(r, profit, [profit + 2 * exp, -profit, profit - (p_rec - rec) * 2 + 1000, profit + 5000])
        return {'stem': stem.replace('Calculate the profit or loss on realisation and each partner\'s share.', 'What is the profit (loss) on realisation?'), 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem, 'answer': f'Realisation {word} {m(abs(profit))}: ' + ', '.join(f'{n} {m(abs(v))}' for n, v in zip(names, shares)), 'key': key, 'marks': 4}


def _diss_c4(r, D):
    A, B = r.sample(PEOPLE, 2)
    ratio = r.choice(OLD2)
    s = sum(ratio) * 100
    nca = step(r, 50000, 150000, 1000); inv = step(r, 10000, 30000, 100); rec = step(r, 8000, 25000, 100); pay = step(r, 6000, 20000, 100)
    capA = step(r, 40000, 100000, 1000); capB = step(r, 30000, 90000, 1000)
    bank = capA + capB + pay - nca - inv - rec
    if bank < 2000:
        capA += 2000 - bank + step(r, 1000, 8000, 1000)
        bank = capA + capB + pay - nca - inv - rec
    p_nca = nca + step(r, -20000, 25000, 500); p_inv = inv - step(r, 1000, 5000, 100); p_rec = rec - step(r, 300, 2000, 100)
    disc = step(r, 100, 1200, 100); exp = step(r, 800, 3500, 100)
    tk = step(r, 5000, 12000, 500); bvv = step(r, 4000, 11000, 500)
    nca -= bvv
    profit = p_nca + p_inv + p_rec + tk + disc - (nca + bvv + inv + rec + exp)
    fix = (-profit) % s
    p_nca += fix; profit += fix
    pA, pB = profit * Fr(ratio[0], sum(ratio)), profit * Fr(ratio[1], sum(ratio))
    finA, finB = capA + pA - tk, capB + pB
    cash_end = bank + p_nca + p_inv + p_rec - (pay - disc) - exp
    intro = (f'{A} and {B}, sharing profits {rs(ratio)}, dissolve their partnership. Their statement of financial position shows: non-current assets {m(nca + bvv)} (including a car at {m(bvv)}), inventory {m(inv)}, trade receivables {m(rec)}, bank {m(bank)}, '
             f'trade payables {m(pay)}, capital {A} {m(capA)}, capital {B} {m(capB)}. Other non-current assets were sold for {m(p_nca)}, inventory for {m(p_inv)} and receivables realised {m(p_rec)}. {A} took the car at {m(tk)}. '
             f'Payables accepted {m(pay - disc)} in full settlement and dissolution costs were {m(exp)}.')
    parts = [
        lambda r: ('Prepare the realisation account.', f'{"Profit" if profit >= 0 else "Loss"} on realisation {m(abs(profit))}', f'Debits: assets {m(nca + bvv + inv + rec)}, costs {m(exp)} [2]; credits: sales {m(p_nca + p_inv + p_rec)}, car {m(tk)}, discount {m(disc)} [2]; result {m(abs(profit))} [1] [5]'),
        lambda r: ('Calculate the amount paid to each partner to close the business.', f'{A} {m(finA)}, {B} {m(finB)}', f'{A}: {m(capA)} ± {m(abs(pA))} − car {m(tk)} = {m(finA)} [2]; {B}: {m(capB)} ± {m(abs(pB))} = {m(finB)} [1] [3]'),
        lambda r: ('Prepare the bank account to show that it closes with a nil balance.', f'Funds available {m(cash_end)} = payments to partners {m(finA + finB)}', f'Opening {m(bank)} + receipts {m(p_nca + p_inv + p_rec)} − payables {m(pay - disc)} − costs {m(exp)} = {m(cash_end)} [2]; = {m(finA)} + {m(finB)} [1] [3]'),
        lambda r: ('Explain why the car taken over by a partner is credited to the realisation account.', 'It is treated as if sold to the partner at the agreed value; the partner\'s capital is debited instead of cash received.', 'Treated as a sale [1]; capital debited [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t1_4.add('C4', (2, 3, 4, 5), 'multi_step')(_diss_c4)
t1_4.add('C3', (4, 5), 'multi_step')(_diss_c4)


@t1_4.add('C2', (2, 3, 4), 'explain')
def t14_err(r, D):
    A, B = r.sample(PEOPLE, 2)
    bv, tk = step(r, 3000, 12000, 500), step(r, 3000, 12000, 500)
    return {'stem': f'On the dissolution of the partnership of {A} and {B}, {A} took over office equipment with a book value of {m(bv)} at an agreed value of {m(tk)}. The bookkeeper debited the realisation account and credited {A}\'s capital account with {m(tk)}. Explain the error and its effect on the amount paid to {A}.',
            'answer': f'The entry is reversed: {A}\'s capital should be debited (he receives an asset instead of cash) and realisation credited. The error overstates {A}\'s capital by {m(2 * tk)} before sharing, so he would be overpaid.',
            'key': f'Correct entry Dr capital {A}, Cr realisation [1]; reason asset received in lieu of cash [1]; effect: capital overstated by 2 × {m(tk)} = {m(2 * tk)} (before realisation result) [1] [3]'}


t1_5 = topic('Conversion of a partnership into a limited company', 'conversion of a partnership into a limited company', 'conversion', 'limited company')
fixed(t1_5, 'C1', (1, 2), [
    ('When a partnership is converted into a limited company, the purchase consideration is credited to the', 'realisation account', 'Dr Company (purchaser) account, Cr Realisation with purchase consideration [1].',
     ['partners\' current accounts', 'goodwill account', 'share premium account of the partnership']),
    ('Shares received from the new company are distributed to the partners', 'in the ratio agreed (often their final capital balances)', 'Shares are allotted by agreement, normally to settle closing capital balances [1].',
     ['always equally', 'in the profit-sharing ratio only', 'in the ratio of their drawings']),
    ('One advantage to the partners of converting into a limited company is', 'limited liability for the owners', 'Shareholders\' liability limited to amount unpaid on shares [1].',
     ['no need to publish accounts', 'lower set-up costs', 'profits do not have to be shared']),
    ('A company issues 50 000 ordinary shares of $1 at $1.60 as part of the purchase consideration. The amount credited to share premium is', '$30,000', '50 000 × $0.60 = $30,000 [1].',
     ['$50,000', '$80,000', '$20,000']),
])
fixed(t1_5, 'C2', (2, 3, 4), [
    ('Explain one advantage and one disadvantage to the partners of converting their business into a limited company.', 'Advantage: limited liability / easier to raise capital by selling shares. Disadvantage: loss of privacy (accounts published), more regulation and cost, possible loss of control.',
     'Advantage with reason [1+1]; disadvantage with reason [1+1] [4]'),
    ('Explain why goodwill may appear in the new company\'s statement of financial position after a partnership is converted.', 'If the purchase consideration exceeds the fair value of net assets taken over, the excess is purchased goodwill, which the company can recognise as an intangible asset.',
     'Consideration > fair value of net assets [1]; purchased goodwill recognised [1] [2]'),
])


@t1_5.add('C3', (1, 2, 3, 4, 5))
def t15_conv(r, D):
    A, B = r.sample(PEOPLE, 2)
    c = co(r)
    na_bv = step(r, 120000, 400000, 1000)
    na_fv = na_bv + step(r, -20000, 60000, 1000)
    N = step(r, 60000, 300000, 10000)
    p = r.choice([1.2, 1.25, 1.5, 1.6, 1.8, 2.0])
    cash = step(r, 10000, 80000, 1000)
    sh_val = round(N * p)
    PC = sh_val + cash
    if PC <= na_fv:
        cash += na_fv - PC + step(r, 5000, 40000, 1000)
        PC = sh_val + cash
    gw = PC - na_fv
    rp = PC - na_bv
    stem = (f'{c} was formed to take over the partnership of {A} and {B}. All assets and liabilities were taken over; their book value was {m(na_bv)} and the agreed fair value was {m(na_fv)}. '
            f'The purchase consideration was {nm(N)} ordinary shares of $1 each issued at ${p:.2f} per share plus {m(cash)} in cash.')
    key = f'Shares {nm(N)} × ${p:.2f} = {m(sh_val)} [1]; consideration = {m(sh_val)} + {m(cash)} = {m(PC)} [1]; goodwill = {m(PC)} − {m(na_fv)} = {m(gw)} [1]; realisation profit = {m(PC)} − {m(na_bv)} = {m(rp)} [1]; share premium {m(N * (p - 1))} [1]'
    if D == 1:
        opts, ans = mm(r, PC, [sh_val, N + cash, PC - cash * 2, na_fv])
        return {'stem': stem + ' What is the total purchase consideration?', 'options': opts, 'answer': ans, 'key': key}
    if D == 2:
        return {'stem': stem + f' Calculate the purchase consideration and the goodwill recognised by {c}.', 'answer': f'Consideration {m(PC)}; goodwill {m(gw)}', 'key': key, 'marks': 3}
    return {'stem': stem + f' Calculate (a) the purchase consideration, (b) the goodwill in {c}\'s books, (c) the share premium created and (d) the profit on realisation in the partnership books.',
            'answer': f'(a) {m(PC)} (b) {m(gw)} (c) {m(N * (p - 1))} (d) {m(rp)}', 'key': key, 'marks': 5, 'type': 'multi_step'}


def _conv_c4(r, D):
    A, B = r.sample(PEOPLE, 2)
    c = co(r)
    ratio = r.choice(OLD2)
    nca, ca, cl = step(r, 150000, 350000, 1000), step(r, 40000, 120000, 1000), step(r, 20000, 60000, 1000)
    fv_up = step(r, 10000, 50000, 1000)
    capA = step(r, 60000, 200000, 1000)
    capB = nca + ca - cl - capA
    if capB < 30000:
        capA -= 30000 - capB + 10000; capB = nca + ca - cl - capA
    N = step(r, 100000, 250000, 10000); p = r.choice([1.25, 1.5, 2.0]); cash = step(r, 10000, 50000, 1000)
    PC = round(N * p) + cash
    na_fv = nca + fv_up + ca - cl
    if PC <= na_fv:
        cash += na_fv - PC + 20000; PC = round(N * p) + cash
    s = sum(ratio)
    rp = PC - (nca + ca - cl)
    rp_fix = (-rp) % (100 * s)
    cash += rp_fix; PC += rp_fix; rp += rp_fix
    gw = PC - na_fv
    pA, pB = rp * Fr(ratio[0], s), rp * Fr(ratio[1], s)
    intro = (f'{A} and {B} share profits {rs(ratio)}. Their partnership is taken over by {c}. Book values: non-current assets {m(nca)}, current assets {m(ca)}, current liabilities {m(cl)}; capitals {A} {m(capA)}, {B} {m(capB)}. '
             f'{c} values the non-current assets at {m(nca + fv_up)} and other items at book value. The consideration is {nm(N)} ordinary shares of $1 issued at ${p:.2f} each and {m(cash)} in cash.')
    parts = [
        lambda r: ('Calculate the profit on realisation and each partner\'s share.', f'{m(rp)}: {A} {m(pA)}, {B} {m(pB)}', f'Consideration {m(PC)} − net assets {m(nca + ca - cl)} = {m(rp)} [2]; shared {rs(ratio)} [1] [3]'),
        lambda r: (f'Calculate the goodwill to be recorded by {c}.', m(gw), f'{m(PC)} − fair value of net assets {m(na_fv)} = {m(gw)} [2]'),
        lambda r: (f'Prepare the journal entry in the books of {c} to record the acquisition (narrative not required).',
                   f'Dr non-current assets {m(nca + fv_up)}, current assets {m(ca)}, goodwill {m(gw)}; Cr current liabilities {m(cl)}, share capital {m(N)}, share premium {m(N * (p - 1))}, bank {m(cash)}',
                   'Assets at fair value [1]; goodwill [1]; liabilities [1]; share capital and premium [1]; bank [1] [5]'),
        lambda r: ('Evaluate whether the partners should accept shares rather than cash as consideration.', 'Shares: continue to share in profits and growth, but value may fall and are less liquid. Cash: certain and immediate, but no future participation. Decision depends on confidence in the company.',
                   'Two points for shares [2]; one against [1]; conclusion [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t1_5.add('C4', (2, 3, 4, 5), 'multi_step')(_conv_c4)
t1_5.add('C3', (4, 5), 'multi_step')(_conv_c4)


@t1_5.add('C2', (2, 3, 4), 'explain')
def t15_err(r, D):
    A, B = r.sample(PEOPLE, 2)
    N = step(r, 40000, 200000, 10000); p = r.choice([1.25, 1.5, 1.75, 2.0])
    return {'stem': f'When {co(r)} took over the partnership of {A} and {B}, it issued {nm(N)} ordinary shares of $1 at ${p:.2f}. The company accountant credited the whole {m(N * p)} to the ordinary share capital account. Explain the error and state the correct entries.',
            'answer': f'Share capital must show nominal value only: Cr ordinary share capital {m(N)}; the excess {m(N * (p - 1))} is credited to share premium.',
            'key': f'Share capital at nominal value [1]; share capital {m(N)} [1]; share premium {m(N * (p - 1))} [1] [3]'}


CHAPTERS[1] = [t1_1, t1_2, t1_3, t1_4, t1_5]


# ===================================================================== 2 Limited company capital
t2_1 = topic('Issue and forfeiture of shares', 'issue and forfeiture of shares', 'issue of shares', 'forfeiture', 'rights issue', 'bonus issue')
fixed(t2_1, 'C1', (1, 2), [
    ('When shares are issued at a premium, the premium is credited to the', 'share premium account', 'Excess over nominal value → share premium (a capital reserve) [1].',
     ['retained earnings', 'ordinary share capital account', 'general reserve']),
    ('A bonus issue of shares', 'capitalises reserves and raises no cash', 'Bonus issue: Dr reserves, Cr share capital; no cash received [1].',
     ['raises cash from existing shareholders', 'increases total equity', 'reduces the number of shares in issue']),
    ('A rights issue is', 'an offer of new shares to existing shareholders in proportion to their holdings, usually below market price', 'Rights issue raises cash from existing shareholders pro rata [1].',
     ['a free issue of shares from reserves', 'an issue of debentures to the public', 'the purchase by a company of its own shares']),
    ('Shares are forfeited when', 'a shareholder fails to pay a call (instalment) due on the shares', 'Forfeiture follows non-payment of allotment/call money [1].',
     ['the company makes a loss', 'a shareholder sells shares to another person', 'the company issues bonus shares']),
    ('On forfeiture, the amount already paid by the defaulting shareholder (excluding premium) is credited to the', 'forfeited shares account', 'Dr share capital (called-up amount), Cr call account (unpaid), Cr forfeited shares (amount paid) [1].',
     ['share premium account', 'bank account', 'retained earnings']),
    ('Which reserve is a revenue reserve?', 'Retained earnings', 'Revenue reserves come from profits and are distributable [1].',
     ['Share premium', 'Revaluation reserve', 'Capital redemption reserve']),
])
fixed(t2_1, 'C2', (2, 3, 4), [
    ('Explain why a company might make a bonus issue of shares even though it raises no cash.', 'It brings issued share capital more in line with the capital employed, lowers the market price per share making shares more marketable, and signals confidence without paying a cash dividend.',
     'Two reasons [1 each] with explanation [1 each] [4]'),
    ('Explain why a rights issue is usually priced below the current market price.', 'To encourage existing shareholders to take up the shares and ensure the issue is fully subscribed; it also compensates for dilution.',
     'Encourage take-up/full subscription [1]; compensates/attractive to shareholders [1] [2]'),
    ('Distinguish between a capital reserve and a revenue reserve, giving an example of each.', 'A capital reserve (e.g. share premium, revaluation reserve) cannot be used to pay cash dividends; a revenue reserve (e.g. retained earnings, general reserve) arises from profits and can be distributed.',
     'Capital: not distributable + example [1]; revenue: distributable + example [1] [2]'),
    ('Explain what happens to the balance remaining on the forfeited shares account after forfeited shares are reissued.', 'Any balance left after covering the discount on reissue is a capital profit and is transferred to the share premium account.',
     'Discount on reissue debited first [1]; remaining balance transferred to share premium [1] [2]'),
])


@t2_1.add('C3', (1, 2, 3, 4, 5))
def t21_rights_bonus(r, D):
    c = co(r)
    N = step(r, 200000, 1000000, 40000)
    nom = r.choice([1, 0.5])
    sp = step(r, 20000, 150000, 1000)
    re_ = step(r, 80000, 400000, 1000)
    kind = r.choice(['bonus', 'rights']) if D > 1 else 'rights'
    k = r.choice([2, 4, 5, 8])
    new = N // k
    if kind == 'rights':
        price = r.choice([1.2, 1.4, 1.5, 1.75, 2.0]) * (nom if nom == 1 else 2 * nom)
        cash = new * price
        sc_inc = new * nom
        prem = cash - sc_inc
        stem = f'{c} has {nm(N)} ordinary shares of ${nom:.2f} each in issue, share premium of {m(sp)} and retained earnings of {m(re_)}. It makes a 1 for {k} rights issue at ${price:.2f} per share, fully taken up.'
        key = f'New shares = {nm(N)}/{k} = {nm(new)} [1]; cash {nm(new)} × ${price:.2f} = {m(cash)} [1]; share capital +{m(sc_inc)} [1]; share premium + {m(prem)} → {m(sp + prem)} [1]'
        if D == 1:
            opts, ans = mm(r, cash, [sc_inc, N * price, cash / 2, prem])
            return {'stem': stem + ' How much cash is raised?', 'options': opts, 'answer': ans, 'key': key}
        return {'stem': stem + ' Calculate the cash raised and the balances on share capital and share premium after the issue.',
                'answer': f'Cash {m(cash)}; share capital {m((N + new) * nom)}; share premium {m(sp + prem)}', 'key': key, 'marks': 4}
    bon = new * nom
    from_sp = min(sp, bon) if D >= 3 else min(sp, bon)
    from_re = bon - from_sp
    stem = (f'{c} has {nm(N)} ordinary shares of ${nom:.2f} each, share premium of {m(sp)} and retained earnings of {m(re_)}. The directors make a 1 for {k} bonus issue, using the share premium account as far as possible.'
            ' Calculate the balances on share capital, share premium and retained earnings after the issue.')
    return {'stem': stem, 'answer': f'Share capital {m((N + new) * nom)}; share premium {m(sp - from_sp)}; retained earnings {m(re_ - from_re)}',
            'key': f'Bonus shares {nm(new)}, nominal {m(bon)} [1]; share premium used {m(from_sp)} [1]; retained earnings used {m(from_re)} [1]; total equity unchanged at {m(N * nom + sp + re_)} [1]', 'marks': 4}


@t2_1.add('C3', (2, 3, 4, 5))
def t21_forfeit(r, D):
    c = co(r)
    N = step(r, 100000, 500000, 10000)
    price = r.choice([1.5, 1.6, 1.8, 2.0, 1.4])
    prem = round(price - 1, 2)
    appl = r.choice([0.3, 0.4, 0.5])
    call = r.choice([0.2, 0.25, 0.3, 0.4])
    allot = round(price - appl - call, 2)
    k = step(r, 2000, 20000, 1000)
    q = round(r.choice([call + 0.1, call + 0.2, 0.8, 0.9, 1.0]), 2)
    q = min(max(q, call), 1.0)
    paid_nom = round(1 - call, 2)
    forf = k * paid_nom
    disc = k * (1 - q)
    to_sp = forf - disc
    stem = (f'{c} offered {nm(N)} ordinary shares of $1 each at ${price:.2f} per share, payable: application ${appl:.2f}, allotment ${allot:.2f} (including the premium of ${prem:.2f}) and a final call of ${call:.2f}. '
            f'All money was received except the call on {nm(k)} shares, which were forfeited. These shares were later reissued as fully paid at ${q:.2f} each.')
    key = (f'Forfeiture: Dr share capital {m(k)}, Cr call {m(k * call)}, Cr forfeited shares {m(forf)} [2]; reissue: Dr bank {m(k * q)}' + (f', Dr forfeited shares {m(disc)}' if disc else '') + f', Cr share capital {m(k)} [2]; '
           + (f'balance {m(forf)} − {m(disc)} = {m(to_sp)}' if disc else f'balance {m(forf)}') + ' transferred to share premium [1]')
    if D == 2:
        return {'stem': stem + ' Calculate the amount credited to the forfeited shares account on forfeiture and the amount finally transferred to share premium.',
                'answer': f'Forfeited shares {m(forf)}; transfer to share premium {m(to_sp)}', 'key': key, 'marks': 3}
    tot_cash = N * price - k * call + k * q
    return {'stem': stem + ' Prepare the journal entries for the forfeiture and reissue and calculate the total cash received from the issue and reissue.',
            'answer': f'Entries as key; total cash {m(tot_cash)}; transfer to share premium {m(to_sp)}', 'key': key + f'; total cash = {m(N * price)} − {m(k * call)} + {m(k * q)} = {m(tot_cash)} [1]', 'marks': 6, 'type': 'multi_step'}


@t2_1.add('C2', (2, 3, 4), 'explain')
def t21_err(r, D):
    c = co(r)
    N = step(r, 100000, 600000, 20000); k = r.choice([4, 5, 10])
    return {'stem': f'{c} made a 1 for {k} bonus issue on {nm(N)} ordinary shares of $1. The bookkeeper debited the bank account and credited share capital with {m(N // k)}. Explain the error and state the correct entry.',
            'answer': f'No cash is received in a bonus issue. The correct entry is Dr share premium (or other reserves) {m(N // k)}, Cr ordinary share capital {m(N // k)}.',
            'key': f'Bonus issue raises no cash [1]; Dr reserve {m(N // k)} [1]; Cr share capital {m(N // k)} [1] [3]'}


t2_2 = topic('Redemption and purchase of own shares; capital redemption reserve', 'redemption and purchase of own shares; capital redemption reserve', 'redemption', 'capital redemption reserve', 'purchase of own shares')
fixed(t2_2, 'C1', (1, 2), [
    ('The purpose of a capital redemption reserve is to', 'maintain the company\'s capital so that creditors are protected when shares are redeemed out of profits', 'CRR replaces the share capital cancelled so the capital base is maintained [1].',
     ['provide cash to pay dividends', 'record the premium paid on redemption', 'increase the distributable profits']),
    ('When shares are redeemed entirely out of distributable profits, the amount transferred to the capital redemption reserve equals', 'the nominal value of the shares redeemed', 'CRR = nominal value redeemed − proceeds of any new issue [1].',
     ['the cash paid to shareholders', 'the premium paid on redemption', 'the proceeds of a new share issue']),
    ('A capital redemption reserve can be used to', 'make a bonus issue of shares', 'CRR is a capital reserve; may be used for bonus issues only [1].',
     ['pay a cash dividend', 'pay interest on debentures', 'write off trading losses']),
    ('Which shares can be redeemed by a company?', 'Shares issued as redeemable', 'Only shares issued as redeemable may be redeemed; others may be bought back [1].',
     ['Any shares, at the directors\' choice', 'Only bonus shares', 'Only shares bought by employees']),
])
fixed(t2_2, 'C2', (2, 3, 4), [
    ('Explain why a company must transfer an amount to a capital redemption reserve when redeeming shares out of profits.', 'Redemption reduces share capital; without a transfer, distributable reserves would be available to pay out as dividends and the capital that protects creditors would fall. The CRR locks up an equivalent amount.',
     'Share capital reduced [1]; creditors\' buffer protected [1]; CRR non-distributable [1] [3]'),
    ('Give two reasons why a company might buy back its own ordinary shares.', 'To return surplus cash to shareholders; to increase EPS/share price; to reduce the number of shareholders/prevent a takeover; to buy out a departing shareholder in a private company.',
     'Two reasons [1 each] with explanation [1 each] [4]'),
    ('Explain the difference between redeeming shares and making a bonus issue in terms of their effect on cash and equity.', 'Redemption pays cash out and reduces total equity; a bonus issue involves no cash and leaves total equity unchanged (it only reclassifies reserves as share capital).',
     'Redemption: cash out, equity falls [1]; bonus: no cash, equity unchanged [1] [2]'),
])


@t2_2.add('C3', (1, 2, 3, 4, 5))
def t22_redeem(r, D):
    c = co(r)
    P = step(r, 50000, 300000, 10000)
    prem_pc = r.choice([0, 5, 10, 20]) if D >= 2 else 0
    re_ = step(r, P + 50000, P + 400000, 1000)
    sp = step(r, 10000, 80000, 1000)
    new_n = step(r, 10000, P // 2, 5000) if D >= 3 else 0
    new_p = r.choice([1.2, 1.25, 1.5]) if new_n else 0
    proceeds = round(new_n * new_p)
    if proceeds >= P:
        new_n = P // 4; proceeds = round(new_n * new_p)
    crr = P - proceeds
    prem = P * prem_pc // 100
    re_after = re_ - crr - prem
    stem = f'{c} redeems {m(P)} of redeemable preference shares of $1 each' + (f' at a premium of {prem_pc}%' if prem_pc else ' at par') + f'. Before redemption it had retained earnings of {m(re_)} and share premium of {m(sp)}.'
    if new_n:
        stem += f' To help finance the redemption it issues {nm(new_n)} ordinary shares of $1 at ${new_p:.2f}. Any premium on redemption is charged to retained earnings.'
    key = (f'New issue proceeds {nm(new_n)} × ${new_p:.2f} = {m(proceeds)} [1]; ' if new_n else '') + (f'CRR = {m(P)} − {m(proceeds)} = {m(crr)} [1]; ' if proceeds else f'CRR = nominal value redeemed {m(crr)} [1]; ') + (f'premium {prem_pc}% × {m(P)} = {m(prem)} charged to retained earnings [1]; ' if prem else '') + f'retained earnings = {m(re_)} − {m(crr)}' + (f' − {m(prem)}' if prem else '') + f' = {m(re_after)} [1]'
    if D == 1:
        opts, ans = mm(r, crr, [0, P / 2, P * 1.1, re_ - P])
        return {'stem': stem + ' What amount is transferred to the capital redemption reserve?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + ' Calculate the transfer to the capital redemption reserve and the balance of retained earnings after the redemption.',
            'answer': f'CRR {m(crr)}; retained earnings {m(re_after)}', 'key': key, 'marks': 2 + bool(prem) + bool(new_n)}


@t2_2.add('C3', (2, 3, 4))
def t22_buyback(r, D):
    c = co(r)
    N = step(r, 300000, 1500000, 50000)
    k = step(r, 20000, N // 5, 5000)
    q = r.choice([1.3, 1.45, 1.6, 1.8, 2.1, 2.5])
    re_ = step(r, int(k * q) + 50000, int(k * q) + 500000, 1000)
    bank = step(r, int(k * q) + 10000, int(k * q) + 200000, 1000)
    cost = round(k * q)
    return {'stem': f'{c} has {nm(N)} ordinary shares of $1 in issue, retained earnings of {m(re_)} and a bank balance of {m(bank)}. It buys back and cancels {nm(k)} of its own shares at ${q:.2f} each out of distributable profits. Calculate the balances on ordinary share capital, capital redemption reserve, retained earnings and bank after the purchase.',
            'answer': f'Share capital {m(N - k)}; CRR {m(k)}; retained earnings {m(re_ - cost)}; bank {m(bank - cost)}',
            'key': f'Share capital − {m(k)} → {m(N - k)} [1]; CRR = nominal {m(k)} [1]; retained earnings − {m(k)} − premium {m(cost - k)} = {m(re_ - cost)} [1]; bank − {m(cost)} = {m(bank - cost)} [1]', 'marks': 4}


@t2_2.add('C2', (2, 3, 4), 'explain')
def t22_err(r, D):
    c = co(r)
    P = step(r, 50000, 250000, 10000)
    return {'stem': f'{c} redeemed {m(P)} of redeemable preference shares out of distributable profits. The accountant transferred {m(P)} from the share premium account to the capital redemption reserve. Explain why this is incorrect and state the correct entry.',
            'answer': f'The transfer must come from distributable profits (retained earnings), not from share premium, which is already a capital reserve. Correct entry: Dr retained earnings {m(P)}, Cr capital redemption reserve {m(P)}.',
            'key': f'Share premium is already non-distributable [1]; purpose is to lock up distributable profits [1]; Dr retained earnings, Cr CRR {m(P)} [1] [3]'}


t2_3 = topic('Debentures: issue, interest and redemption', 'debentures: issue, interest and redemption', 'debentures', 'debenture interest')
fixed(t2_3, 'C1', (1, 2), [
    ('Debenture interest is', 'an expense (finance cost) that must be paid whether or not a profit is made', 'Interest on debentures is a finance cost charged before tax [1].',
     ['an appropriation of profit like a dividend', 'paid only if the directors declare it', 'credited to the share premium account']),
    ('Debenture holders are', 'long-term creditors (lenders) of the company', 'Debentures are loans, shown as non-current liabilities [1].',
     ['owners of the company', 'members with voting rights', 'preference shareholders']),
    ('Debentures repayable in eight months\' time are shown in the statement of financial position as', 'current liabilities', 'Due within 12 months → current liability [1].',
     ['non-current liabilities', 'equity', 'non-current assets']),
    ('A secured debenture is one which', 'gives the lender a charge over specified assets of the company', 'Secured on assets (fixed or floating charge) [1].',
     ['can be converted into shares', 'pays no interest', 'is guaranteed by the government']),
])
fixed(t2_3, 'C2', (2, 3, 4), [
    ('Explain two differences between debentures and ordinary shares from the point of view of the investor.', 'Debenture holders are creditors, receive fixed interest whether or not profits are made and are repaid before shareholders; ordinary shareholders are owners, receive variable dividends, have votes and bear the most risk.',
     'Status creditor vs owner [1]; fixed interest vs variable dividend [1]; priority on winding up / votes [1]; risk [1] [4]'),
    ('Explain why a company might prefer to raise finance by issuing debentures rather than ordinary shares.', 'Interest is tax deductible; no dilution of control; cost of debt usually lower; but increases gearing and fixed commitments.',
     'Two advantages [1 each] + development [1] [3]'),
])


@t2_3.add('C3', (1, 2, 3, 4, 5))
def t23_int(r, D):
    c = co(r)
    X = step(r, 100000, 800000, 20000)
    rate = r.choice([4, 5, 6, 7, 8, 9])
    months = r.choice([3, 4, 6, 8, 9]) if D >= 2 else 12
    paid_m = r.choice([0] + [x for x in (3, 6) if x < months]) if D >= 3 else 0
    charge = X * rate * months / 1200
    paid = X * rate * paid_m / 1200
    accr = charge - paid
    stem = f'{c} issued {m(X)} {rate}% debentures' + (f' {months} months before its year end on {ye(r)}' if months < 12 else ' at the start of the financial year') + '.'
    if D >= 3:
        stem += f' Interest of {m(paid)} has been paid during the year.' if paid else ' No interest had been paid by the year end.'
    key = f'Charge = {m(X)} × {rate}% × {months}/12 = {m(charge)} [1]' + (f'; accrual = {m(charge)} − {m(paid)} = {m(accr)} [1]' if D >= 3 else '')
    if D == 1:
        opts, ans = mm(r, charge, [charge * 2, charge / 2, X * (rate + 1) / 100, X * rate / 1000])
        return {'stem': stem + ' What is the debenture interest charge for the year?', 'options': opts, 'answer': ans, 'key': key}
    if D == 2:
        return {'stem': stem + ' Calculate the debenture interest to be charged in the income statement.', 'answer': m(charge), 'key': key, 'marks': 2}
    return {'stem': stem + ' Calculate the finance cost for the year and the amount shown as accrued interest in the statement of financial position.',
            'answer': f'Finance cost {m(charge)}; accrued interest {m(accr)}', 'key': key, 'marks': 3}


@t2_3.add('C3', (2, 3, 4, 5))
def t23_redeem(r, D):
    c = co(r)
    X = step(r, 100000, 600000, 10000)
    p = r.choice([0, 2, 5, 10])
    disc = r.choice([0, 0, 5, 2.5]) if D >= 3 else 0
    issued = X * (100 - disc) / 100
    red = X * (100 + p) / 100
    pr = r.choice(['a new issue of ordinary shares at par', 'the company\'s bank balance', 'a new bank loan'])
    stem = (f'{c} issued {m(X)} debentures' + (f' at a discount of {disc}%' if disc else ' at par') + f'. They are redeemed' + (f' at a premium of {p}%' if p else ' at par') + f', financed by {pr}.')
    return {'stem': stem + ' Calculate the cash received on issue, the cash paid on redemption and the total cost of borrowing excluding interest.',
            'answer': f'Received {m(issued)}; paid {m(red)}; extra cost {m(red - issued)}',
            'key': f'Issue {m(X)} × {100 - disc}% = {m(issued)} [1]; redemption {m(X)} × {100 + p}% = {m(red)} [1]; difference {m(red - issued)} (discount + premium, a finance cost) [1]', 'marks': 3}


def _cap_c4(r, D):
    c = co(r)
    N = step(r, 400000, 1500000, 100000)
    sp = step(r, 50000, 200000, 1000); re_ = step(r, 300000, 900000, 1000)
    pref = step(r, 50000, 200000, 10000)
    k = r.choice([4, 5, 10]); new = N // k; price = r.choice([1.2, 1.5, 1.8])
    cash = round(new * price)
    deb = step(r, 100000, 400000, 50000); rate = r.choice([5, 6, 8])
    prem_r = r.choice([0, 5, 10]); premv = pref * prem_r // 100
    crr = pref
    re_after = re_ - crr - premv
    sp_after = sp + cash - new
    intro = (f'At {ye(r)} the equity of {c} was: ordinary shares of $1 {m(N)}, {pref and m(pref)} redeemable preference shares of $1, share premium {m(sp)}, retained earnings {m(re_)}. '
             f'During the following year: (1) a 1 for {k} rights issue was made at ${price:.2f} and fully taken up; (2) all the preference shares were redeemed' + (f' at a {prem_r}% premium' if prem_r else ' at par') + ' out of retained earnings; '
             f'(3) {m(deb)} {rate}% debentures were issued on the first day of the year.')
    parts = [
        lambda r: ('Calculate the cash raised by the rights issue and the new share premium balance.', f'{m(cash)}; share premium {m(sp_after)}', f'{nm(new)} × ${price:.2f} = {m(cash)} [1]; {m(sp)} + {m(cash - new)} = {m(sp_after)} [1] [2]'),
        lambda r: ('Calculate the transfer to the capital redemption reserve and the closing retained earnings (before the profit for the year).', f'CRR {m(crr)}; retained earnings {m(re_after)}', f'CRR = nominal {m(pref)} [1]; {m(re_)} − {m(crr)} − {m(premv)} = {m(re_after)} [2] [3]'),
        lambda r: ('Calculate the debenture interest for the year and state where it appears in the financial statements.', f'{m(deb * rate / 100)}; finance costs in the income statement', f'{m(deb)} × {rate}% [1]; finance cost [1] [2]'),
        lambda r: ('Prepare the equity section of the statement of financial position after these transactions (ignore the profit for the year).',
                   f'Ordinary shares {m(N + new)}; share premium {m(sp_after)}; CRR {m(crr)}; retained earnings {m(re_after)}; total {m(N + new + sp_after + crr + re_after)}',
                   f'Each correct line [1 each, max 4]; total {m(N + new + sp_after + crr + re_after)} [1] [5]'),
        lambda r: ('Evaluate the decision to finance the company with debentures rather than a further share issue.', 'Debentures: interest tax deductible, no dilution of control, but fixed interest and higher gearing increase risk; shares: no fixed cost but dilute EPS and control.',
                   'Two points for [2]; two against [2]; conclusion [1] [5]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


for _t in (t2_1, t2_2, t2_3):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_cap_c4)
t2_2.add('C3', (4, 5), 'multi_step')(_cap_c4)


def _deb_c4(r, D):
    c = co(r)
    X = step(r, 200000, 800000, 50000); rate = r.choice([5, 6, 7, 8])
    m_issue = r.choice([3, 4, 6, 9])
    pbit = step(r, 150000, 600000, 5000)
    eq = step(r, 600000, 2000000, 10000)
    charge = X * rate * m_issue / 1200
    full = X * rate / 100
    paid = 0
    intro = r.choice([f'{c} needs funds for a new factory in {r.choice(["Kenya", "Peru", "Vietnam", "Egypt", "Malaysia"])}. It issues {m(X)} {rate}% debentures {m_issue} months before its year end. Profit from operations is {m(pbit)} and equity is {m(eq)}.',
                      f'The directors of {c} raised {m(X)} by issuing {rate}% debentures, secured on its premises, {m_issue} months before the year end. The company\'s profit from operations is {m(pbit)} and total equity is {m(eq)}.'])
    parts = [
        lambda r: ('Calculate the debenture interest charge for the current year and for a full year.', f'{m(charge)}; full year {m(full)}', f'{m(X)} × {rate}% × {m_issue}/12 = {m(charge)} [1]; full {m(full)} [1] [2]'),
        lambda r: ('Calculate the interest cover for the current year and for the next full year (assuming profit is unchanged).', f'{pbit / charge:.1f} times; {pbit / full:.1f} times', f'{m(pbit)} / {m(charge)} [1]; {m(pbit)} / {m(full)} [1] [2]'),
        lambda r: ('Calculate the gearing ratio after the issue (debentures / (equity + debentures)).', pc(X / (eq + X) * 100), f'{m(X)} / {m(eq + X)} × 100 [2]'),
        lambda r: ('State the journal entry to record the accrued interest at the year end if none has been paid.', f'Dr finance costs (debenture interest) {m(charge)}; Cr accrued expenses (interest payable) {m(charge)}', 'Dr expense [1]; Cr accrual [1] [2]'),
        lambda r: ('Advise the directors whether the debenture issue is a sensible way to finance the factory.', 'Consider interest cover, gearing level, security available, cost compared with dividends, and dilution of control; recommend with reasons.',
                   'Uses figures for interest cover/gearing [2]; balanced points [1]; recommendation [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t2_3.add('C4', (2, 3, 4, 5), 'multi_step')(_deb_c4)
t2_3.add('C3', (4, 5), 'multi_step')(_deb_c4)
t2_1.add('C3', (4, 5), 'multi_step')(_cap_c4)


@t2_3.add('C2', (2, 3, 4), 'explain')
def t23_err(r, D):
    c = co(r)
    X = step(r, 100000, 500000, 50000); rate = r.choice([5, 6, 8])
    return {'stem': f'The draft financial statements of {c} show debenture interest of {m(X * rate / 100)} on {m(X)} {rate}% debentures deducted in the statement of changes in equity together with dividends. Explain why this is wrong and state the effect of correcting it on profit for the year.',
            'answer': f'Debenture interest is a finance cost (expense), not an appropriation; it must be charged in the income statement. Profit for the year (before tax) falls by {m(X * rate / 100)}; retained earnings are unaffected overall.',
            'key': f'Interest is an expense owed to creditors [1]; show as finance cost in income statement [1]; profit reduced by {m(X * rate / 100)} [1] [3]'}


CHAPTERS[2] = [t2_1, t2_2, t2_3]


# ===================================================================== 3 Published statements and cash flows
t3_1 = topic('Published income statement and statement of financial position (IAS 1)', 'published income statement and statement of financial position (ias 1)', 'ias 1', 'income statement', 'statement of changes in equity')
fixed(t3_1, 'C1', (1, 2), [
    ('Under IAS 1, which heading comes immediately after gross profit in a published income statement?', 'Distribution costs and administrative expenses', 'Revenue, cost of sales, gross profit, distribution costs, administrative expenses, profit from operations [1].',
     ['Finance costs', 'Tax', 'Dividends paid']),
    ('In a published income statement, debenture interest is shown under', 'finance costs', 'Interest on loans/debentures = finance costs, after profit from operations [1].',
     ['administrative expenses', 'cost of sales', 'the statement of changes in equity']),
    ('Ordinary dividends paid during the year are shown in', 'the statement of changes in equity', 'Dividends are a distribution to owners, not an expense [1].',
     ['the income statement as an expense', 'non-current liabilities', 'cost of sales']),
    ('Which item is shown in the statement of changes in equity?', 'A gain on revaluation of property', 'SOCE: share issues, profit for year, dividends, revaluation surplus [1].',
     ['Depreciation of machinery', 'Trade receivables', 'Interest paid on a bank loan']),
    ('Directors\' fees are normally classified in the published income statement as', 'administrative expenses', 'Directors\' remuneration is an administrative expense [1].',
     ['distribution costs', 'finance costs', 'cost of sales']),
    ('Carriage outwards is classified as a', 'distribution cost', 'Costs of delivering goods to customers = distribution costs [1].',
     ['cost of sales', 'finance cost', 'administrative expense']),
])
fixed(t3_1, 'C2', (2, 3, 4), [
    ('Explain why companies are required to publish financial statements in a standard format such as IAS 1.', 'Standard formats make statements comparable between companies and over time, give users consistent and reliable information and help prevent misleading presentation.',
     'Comparability [1]; reliability/consistency for users [1]; prevents manipulation [1] [3]'),
    ('Explain why a proposed final dividend at the year end is not shown as a liability in the statement of financial position.', 'Under IAS 10 the dividend is not an obligation until approved by shareholders after the reporting date, so it is disclosed in a note only.',
     'Not a present obligation at year end [1]; disclosed by note (IAS 10) [1] [2]'),
    ('Distinguish between the income statement and the statement of changes in equity.', 'The income statement shows income and expenses and the profit for the period; the SOCE shows all changes in equity including profit, dividends, share issues and revaluations.',
     'Income statement: performance/profit [1]; SOCE: movements in equity components [1] [2]'),
])


@t3_1.add('C3', (1, 2, 3, 4, 5))
def t31_is(r, D):
    c = co(r)
    rev = step(r, 800000, 3000000, 10000)
    cos = round(rev * r.choice([0.55, 0.6, 0.62, 0.65, 0.7]) / 1000) * 1000
    dist = step(r, 40000, 150000, 1000)
    adm = step(r, 50000, 200000, 1000)
    dep = step(r, 20000, 80000, 1000)
    dsh = r.choice([40, 50, 60, 75])
    deb = step(r, 100000, 500000, 50000); rate = r.choice([5, 6, 8])
    fin = deb * rate // 100
    tax = step(r, 20000, 90000, 1000)
    gp = rev - cos
    distT = dist + (dep * dsh // 100 if D >= 3 else 0)
    admT = adm + (dep - dep * dsh // 100 if D >= 3 else 0)
    if D < 3:
        admT += dep
    pfo = gp - distT - admT
    if pfo <= fin + tax + 10000:
        rev += (fin + tax + 50000 - pfo) * 2; cos = round(rev * 0.6 / 1000) * 1000; gp = rev - cos; pfo = gp - distT - admT
    pbt = pfo - fin
    pfy = pbt - tax
    stem = f'Extracts from the records of {c} for the {r.choice(["year ended", "financial year to"])} {ye(r)}: revenue {m(rev)}, cost of sales {m(cos)}, distribution costs {m(dist)}, administrative expenses {m(adm)}, depreciation {m(dep)}'
    stem += (f' (to be split {dsh}% distribution and {100 - dsh}% administration)' if D >= 3 else ' (all administrative)')
    stem += f', interest on {m(deb)} {rate}% debentures (none yet paid), tax on profits {m(tax)}.'
    key = f'Gross profit {m(gp)} [1]; distribution {m(distT)}, administrative {m(admT)} [1]; profit from operations {m(pfo)} [1]; finance costs {m(fin)} → PBT {m(pbt)} [1]; profit for the year {m(pfy)} [1]'
    if D == 1:
        opts, ans = mm(r, pfo, [gp, pbt, pfo + dep, pfy])
        return {'stem': stem + ' What is the profit from operations?', 'options': opts, 'answer': ans, 'key': key}
    if D == 2:
        return {'stem': stem + ' Calculate the profit from operations and the profit for the year.', 'answer': f'Profit from operations {m(pfo)}; profit for the year {m(pfy)}', 'key': key, 'marks': 3}
    return {'stem': stem + ' Prepare the income statement for publication in accordance with IAS 1.', 'answer': f'Gross profit {m(gp)}; distribution costs {m(distT)}; administrative expenses {m(admT)}; profit from operations {m(pfo)}; finance costs {m(fin)}; profit before tax {m(pbt)}; tax {m(tax)}; profit for the year {m(pfy)}',
            'key': key, 'marks': 5 + (D >= 4), 'type': 'multi_step'}


@t3_1.add('C3', (2, 3, 4, 5))
def t31_soce(r, D):
    c = co(r)
    sc = step(r, 300000, 1200000, 50000); sp = step(r, 0, 150000, 5000); rr = step(r, 0, 100000, 5000); re_ = step(r, 100000, 600000, 1000)
    k = r.choice([4, 5, 10]); price = r.choice([1.25, 1.5, 2.0])
    new = sc // k; prem = round(new * (price - 1))
    pfy = step(r, 80000, 400000, 1000); dps = r.choice([0.04, 0.05, 0.06, 0.08, 0.1])
    timing = r.choice(['before', 'after'])
    shares_div = sc + (new if timing == 'after' else 0)
    div = round(shares_div * dps)
    reval = step(r, 10000, 120000, 1000) if D >= 3 else 0
    stem = (f'At the start of the year {c} had ordinary shares of $1 {m(sc)}, share premium {m(sp)}, revaluation reserve {m(rr)} and retained earnings {m(re_)}. During the year it issued {nm(new)} shares at ${price:.2f}, '
            f'paid an ordinary dividend of ${dps:.2f} per share {timing} the share issue and made a profit for the year of {m(pfy)}.' + (f' Land was revalued upwards by {m(reval)}.' if reval else '') + ' Prepare the statement of changes in equity, showing closing balances for each reserve.')
    return {'stem': stem, 'answer': f'Share capital {m(sc + new)}; share premium {m(sp + prem)}; revaluation reserve {m(rr + reval)}; retained earnings {m(re_ + pfy - div)}; total {m(sc + new + sp + prem + rr + reval + re_ + pfy - div)}',
            'key': f'Share issue: capital +{m(new)}, premium +{m(prem)} [1]; dividend {nm(shares_div)} × ${dps:.2f} = {m(div)} [1]; retained earnings {m(re_)} + {m(pfy)} − {m(div)} = {m(re_ + pfy - div)} [1]' + (f'; revaluation +{m(reval)} [1]' if reval else '') + ' ; totals [1]',
            'marks': 4 + bool(reval), 'type': 'multi_step'}


@t3_1.add('C2', (2, 3, 4), 'explain')
def t31_err(r, D):
    c = co(r)
    items = [('dividends paid', 'statement of changes in equity (a distribution to owners)', 'administrative expenses'),
             ('carriage outwards', 'distribution costs', 'cost of sales'),
             ('debenture interest', 'finance costs', 'administrative expenses'),
             ('a revaluation gain on land', 'other comprehensive income / revaluation reserve in the SOCE', 'revenue'),
             ('audit fees', 'administrative expenses', 'finance costs'),
             ('salaries of sales staff', 'distribution costs', 'administrative expenses'),
             ('carriage inwards', 'cost of sales', 'distribution costs')]
    a, b = r.sample(items, 2)
    va, vb = step(r, 5000, 90000, 500), step(r, 5000, 90000, 500)
    return {'stem': f'A junior accountant preparing the published income statement of {c} included {a[0]} of {m(va)} in {a[2]} and {b[0]} of {m(vb)} in {b[2]}. Explain where each item should be shown under IAS 1.',
            'answer': f'{a[0].capitalize()}: {a[1]}. {b[0].capitalize()}: {b[1]}.',
            'key': f'{a[0]} → {a[1]} [1] with reason [1]; {b[0]} → {b[1]} [1] with reason [1] [4]'}


t3_2 = topic('Notes to the financial statements and the directors\' report', 'notes to the financial statements and the directors\' report', 'notes to the financial statements', 'directors\' report')
fixed(t3_2, 'C1', (1, 2), [
    ('Which of the following is normally disclosed in a note to the published financial statements?', 'A schedule of movements in property, plant and equipment', 'PPE note: cost, depreciation, additions, disposals, carrying amounts [1].',
     ['The names of the company\'s customers', 'The minutes of directors\' meetings', 'The selling prices of products']),
    ('The directors\' report would normally include', 'the principal activities of the company and the dividends recommended', 'Directors\' report: principal activities, directors, dividends, review of business [1].',
     ['the auditor\'s opinion', 'the detailed nominal ledger', 'each employee\'s salary']),
    ('The accounting policies note explains', 'the bases used to prepare the statements, e.g. depreciation methods and inventory valuation', 'Accounting policies note: measurement bases and specific policies [1].',
     ['the prices of the company\'s shares', 'the directors\' personal assets', 'future budgets']),
    ('Which statement about a proposed final dividend at the year end is correct?', 'It is disclosed in a note but not recognised as a liability', 'IAS 10: non-adjusting; disclosure only [1].',
     ['It is shown as a current liability', 'It is deducted in the income statement', 'It is ignored completely']),
])
fixed(t3_2, 'C2', (2, 3, 4), [
    ('Explain why notes to the financial statements are useful to shareholders.', 'They give detail behind the totals (e.g. PPE movements, borrowings, contingencies) and explain policies, so users can understand, compare and assess the figures.',
     'Detail behind figures [1]; explain policies/judgements [1]; aid comparison [1] [3]'),
    ('Explain the purpose of the directors\' report.', 'It gives narrative information about the company\'s activities, performance, dividends, directors and future developments, supplementing the numerical statements.',
     'Narrative/stewardship info [1]; examples [1] [2]'),
])


@t3_2.add('C3', (1, 2, 3, 4, 5))
def t32_ppe(r, D):
    c = co(r)
    cost = step(r, 300000, 1200000, 10000); acc = step(r, 80000, cost // 2, 1000)
    add = step(r, 40000, 250000, 1000)
    dcost = step(r, 20000, 90000, 1000) if D >= 3 else 0
    dacc = step(r, 5000, dcost - 5000, 1000) if dcost else 0
    rate = r.choice([10, 15, 20, 25])
    meth = r.choice(['straight-line on cost at the year end', 'reducing balance']) if D >= 4 else 'straight-line on cost at the year end'
    cl_cost = cost + add - dcost
    if meth.startswith('straight'):
        dep = cl_cost * rate // 100
    else:
        dep = (cl_cost - (acc - dacc)) * rate // 100
    cl_acc = acc - dacc + dep
    ca = cl_cost - cl_acc
    stem = (f'The plant and machinery of {c} at the start of the year: cost {m(cost)}, accumulated depreciation {m(acc)}. During the year machines costing {m(add)} were bought'
            + (f' and machines that had cost {m(dcost)} (accumulated depreciation {m(dacc)}) were sold' if dcost else '') + f'. Depreciation is {rate}% per annum {meth}, a full year\'s charge in the year of purchase and none in the year of sale.')
    key = f'Closing cost {m(cost)} + {m(add)}' + (f' − {m(dcost)}' if dcost else '') + f' = {m(cl_cost)} [1]; charge {m(dep)} [1]; closing depreciation {m(acc)}' + (f' − {m(dacc)}' if dcost else '') + f' + {m(dep)} = {m(cl_acc)} [1]; carrying amount {m(ca)} [1]'
    if D == 1:
        opts, ans = mm(r, dep, [cost * rate // 100, (cl_cost - acc) * rate // 100 if cl_cost != cost else dep + 5000, add * rate // 100, dep * 2])
        return {'stem': stem + ' What is the depreciation charge for the year?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + ' Prepare the property, plant and equipment note for plant and machinery, showing the carrying amount at the year end.',
            'answer': f'Cost c/f {m(cl_cost)}; depreciation charge {m(dep)}; accumulated depreciation c/f {m(cl_acc)}; carrying amount {m(ca)}', 'key': key, 'marks': 4 + (D >= 4)}


@t3_2.add('C2', (2, 3, 4), 'explain')
def t32_classify(r, D):
    pool = [('the principal activities of the company', 'directors\' report'), ('the depreciation methods and rates used', 'accounting policies note'),
            ('movements in property, plant and equipment', 'PPE note'), ('the dividend recommended by the directors for approval', 'directors\' report (and a note under IAS 10)'),
            ('a court case that the company may lose', 'contingent liabilities note (IAS 37)'), ('the names of the directors during the year', 'directors\' report'),
            ('the basis of inventory valuation', 'accounting policies note'), ('details of debentures and their interest rates and repayment dates', 'note on non-current liabilities'),
            ('a fire that destroyed a warehouse after the year end', 'note on events after the reporting period (IAS 10)'), ('employee involvement and policy on employing disabled persons', 'directors\' report')]
    a, b, cc = r.sample(pool, 3)
    return {'stem': f'State where each of the following would be disclosed in the annual report of {co(r)}, and explain why users need it: (i) {a[0]}; (ii) {b[0]}; (iii) {cc[0]}.',
            'answer': f'(i) {a[1]}; (ii) {b[1]}; (iii) {cc[1]}. Users need these to understand the business, judge the reliability of figures and assess risk.',
            'key': f'(i) {a[1]} [1]; (ii) {b[1]} [1]; (iii) {cc[1]} [1]; valid reason for users [1] [4]'}


t3_3 = topic('Statement of cash flows using the indirect method (IAS 7)', 'statement of cash flows using the indirect method (ias 7)', 'statement of cash flows', 'cash flow', 'ias 7')
fixed(t3_3, 'C1', (1, 2), [
    ('In the indirect method, depreciation is', 'added back to profit from operations', 'Non-cash expense → add back [1].',
     ['deducted from profit from operations', 'shown under investing activities', 'ignored']),
    ('An increase in trade receivables during the year is', 'deducted from profit from operations', 'More cash tied up in receivables → deduct [1].',
     ['added to profit from operations', 'shown under financing activities', 'shown under investing activities']),
    ('Proceeds from the sale of a non-current asset appear under', 'investing activities', 'IAS 7: purchase/sale of PPE are investing [1].',
     ['operating activities', 'financing activities', 'cash and cash equivalents']),
    ('Proceeds from an issue of shares are shown under', 'financing activities', 'Financing: shares, debentures, loans, dividends paid (usually) [1].',
     ['investing activities', 'operating activities', 'not shown']),
    ('A profit on disposal of a non-current asset is', 'deducted from profit from operations in the reconciliation', 'Gain included in profit is non-operating cash → deduct (proceeds go to investing) [1].',
     ['added to profit from operations', 'shown as a financing inflow', 'added to the proceeds of sale']),
    ('A decrease in trade payables is', 'deducted from profit from operations', 'Paying suppliers more than purchases uses cash → deduct [1].',
     ['added to profit from operations', 'shown under investing activities', 'ignored in the indirect method']),
])
fixed(t3_3, 'C2', (2, 3, 4), [
    ('Explain why a profitable company may still have a decrease in cash and cash equivalents.', 'Profit is not cash: cash may be spent on non-current assets, inventory build-up, increased receivables, loan repayments or dividends, none of which reduce profit.',
     'Profit ≠ cash (accruals) [1]; two examples [2] [3]'),
    ('Explain two uses of a statement of cash flows to a lender.', 'Shows ability to generate cash from operations to pay interest and repay loans; reveals how investment was financed and whether liquidity is improving.',
     'Two uses [1 each] with explanation [1 each] [4]'),
    ('Explain why depreciation is added back in the indirect method even though it is not a source of cash.', 'Depreciation was deducted in arriving at profit but no cash left the business; adding it back reverses a non-cash charge to find cash from operations.',
     'Non-cash expense deducted in profit [1]; adding back reverses it [1] [2]'),
])


@t3_3.add('C3', (1, 2, 3, 4, 5))
def t33_ops(r, D):
    c = co(r)
    pfo = step(r, 100000, 600000, 1000); dep = step(r, 20000, 120000, 1000)
    di, dr_, dp = step(r, -30000, 30000, 500), step(r, -25000, 25000, 500), step(r, -20000, 20000, 500)
    gain = step(r, -8000, 8000, 500) if D >= 3 else 0
    inv0 = step(r, 40000, 120000, 1000); rec0 = step(r, 30000, 100000, 1000); pay0 = step(r, 30000, 100000, 1000)
    cgo = pfo + dep - di - dr_ + dp - gain
    tax0, taxc = step(r, 10000, 60000, 1000), step(r, 15000, 70000, 1000)
    tax1 = step(r, 10000, 60000, 1000)
    taxp = tax0 + taxc - tax1
    intp = step(r, 2000, 30000, 500)
    net = cgo - (taxp + intp if D >= 4 else 0)
    stem = (f'For {c}: profit from operations {m(pfo)}; depreciation {m(dep)}' + (f'; {"profit" if gain > 0 else "loss"} on disposal of equipment {m(abs(gain))}' if gain else '')
            + f'. Inventory {m(inv0)} → {m(inv0 + di)}, trade receivables {m(rec0)} → {m(rec0 + dr_)}, trade payables {m(pay0)} → {m(pay0 + dp)}.')
    if D >= 4:
        stem += f' Tax payable was {m(tax0)} at the start and {m(tax1)} at the end of the year; the tax charge was {m(taxc)}. Interest paid was {m(intp)}.'
        q = ' Calculate the net cash from operating activities.'
    else:
        q = ' Calculate the cash generated from operations.'
    sign = lambda v, inc_good: ('+' if (v > 0) == inc_good else '−') + m(abs(v))
    key = (f'{m(pfo)} + depreciation {m(dep)}' + (f' {"−" if gain > 0 else "+"} disposal {m(abs(gain))}' if gain else '') + f' [1]; inventory {sign(di, False)}, receivables {sign(dr_, False)}, payables {sign(dp, True)} [2]; = {m(cgo)} [1]'
           + (f'; tax paid {m(tax0)} + {m(taxc)} − {m(tax1)} = {m(taxp)} [1]; interest {m(intp)}; net {m(net)} [1]' if D >= 4 else ''))
    if D == 1:
        opts, ans = mm(r, cgo, [pfo + dep + di + dr_ - dp, pfo - dep - di - dr_ + dp, pfo, cgo + 2 * dp if dp else cgo + 10000])
        return {'stem': stem + ' What is the cash generated from operations?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + q, 'answer': m(net), 'key': key, 'marks': 4 + 2 * (D >= 4)}


@t3_3.add('C3', (2, 3, 4, 5))
def t33_inv(r, D):
    c = co(r)
    o, cl = step(r, 300000, 900000, 1000), 0
    dep = step(r, 30000, 120000, 1000)
    dca = step(r, 10000, 60000, 1000) if D >= 3 else 0
    pr = dca + step(r, -6000, 8000, 500) if dca else 0
    buy = step(r, 50000, 300000, 1000)
    reval = step(r, 20000, 100000, 1000) if D >= 4 else 0
    cl = o + buy + reval - dep - dca
    stem = (f'Property, plant and equipment of {c} had a carrying amount of {m(o)} at the start of the year and {m(cl)} at the end. Depreciation for the year was {m(dep)}.'
            + (f' Equipment with a carrying amount of {m(dca)} was sold for {m(pr)}.' if dca else '') + (f' Land was revalued upwards by {m(reval)} during the year.' if reval else '')
            + ' Calculate the cash paid to purchase PPE' + (' and the net cash used in investing activities.' if dca else '.'))
    key = f'Purchases = closing {m(cl)} − opening {m(o)} + depreciation {m(dep)}' + (f' + disposals {m(dca)}' if dca else '') + (f' − revaluation {m(reval)}' if reval else '') + f' = {m(buy)} [2]' + (f'; investing = −{m(buy)} + {m(pr)} = {m(pr - buy)} [1]; gain/loss on disposal {m(pr - dca)} goes to operating adjustment [1]' if dca else '')
    return {'stem': stem, 'answer': f'Purchases {m(buy)}' + (f'; net cash used in investing activities {m(buy - pr)}' if dca else ''), 'key': key, 'marks': 2 + 2 * bool(dca)}


@t3_3.add('C3', (2, 3, 4))
def t33_fin(r, D):
    c = co(r)
    sc0 = step(r, 200000, 800000, 50000); new = step(r, 20000, 200000, 10000); sp = r.choice([0.2, 0.5, 0.8, 1.0])
    re0 = step(r, 100000, 500000, 1000); pfy = step(r, 60000, 300000, 1000); div = step(r, 20000, pfy - 10000, 1000)
    re1 = re0 + pfy - div
    l0 = step(r, 50000, 300000, 10000); l1 = l0 + step(r, -50000, 80000, 10000)
    sh_cash = round(new * (1 + sp))
    fin = sh_cash + (l1 - l0) - div
    return {'stem': f'{c}: ordinary shares of $1 increased from {m(sc0)} to {m(sc0 + new)} and share premium rose by {m(new * sp)} as a result of a share issue for cash. Retained earnings went from {m(re0)} to {m(re1)} after a profit for the year of {m(pfy)}. Bank loans moved from {m(l0)} to {m(l1)}. Calculate the dividend paid and the net cash from (used in) financing activities.',
            'answer': f'Dividend paid {m(div)}; net financing {m(fin)}',
            'key': f'Dividend = {m(re0)} + {m(pfy)} − {m(re1)} = {m(div)} [1]; share issue {m(sh_cash)} [1]; loan {"+" if l1 >= l0 else "−"}{m(abs(l1 - l0))} [1]; net = {m(fin)} [1]', 'marks': 4}


def _cf_c4(r, D):
    c = co(r)
    pfo = step(r, 150000, 500000, 1000); dep = step(r, 30000, 100000, 1000)
    di, dr_, dp = step(r, 5000, 40000, 500), step(r, -20000, 30000, 500), step(r, -15000, 25000, 500)
    taxp, intp = step(r, 20000, 80000, 1000), step(r, 5000, 25000, 500)
    buy = step(r, 100000, 400000, 1000); pr = step(r, 5000, 40000, 500)
    shares = step(r, 0, 200000, 10000); div = step(r, 20000, 100000, 1000); loan = step(r, -60000, 100000, 10000)
    cgo = pfo + dep - di - dr_ + dp
    op = cgo - taxp - intp
    inv = pr - buy
    fin = shares + loan - div
    chg = op + inv + fin
    open_ = step(r, 10000, 120000, 1000)
    intro = (f'The following information relates to {c} for the year ended {ye(r)}: profit from operations {m(pfo)}; depreciation {m(dep)}; increase in inventories {m(di)}; '
             f'{"increase" if dr_ > 0 else "decrease"} in trade receivables {m(abs(dr_))}; {"increase" if dp > 0 else "decrease"} in trade payables {m(abs(dp))}; tax paid {m(taxp)}; interest paid {m(intp)}; '
             f'purchase of PPE {m(buy)}; proceeds from sale of PPE {m(pr)} (no gain or loss); proceeds of share issue {m(shares)}; {"new loan" if loan >= 0 else "loan repaid"} {m(abs(loan))}; dividends paid {m(div)}. Cash and cash equivalents at the start of the year were {m(open_)}.')
    parts = [
        lambda r: ('Calculate the net cash from operating activities.', m(op), f'Cash generated {m(cgo)} [2]; less tax and interest = {m(op)} [1] [3]'),
        lambda r: ('Calculate the net cash used in investing activities.', m(inv), f'−{m(buy)} + {m(pr)} = {m(inv)} [1]'),
        lambda r: ('Calculate the net cash from (used in) financing activities.', m(fin), f'{m(shares)} {"+" if loan >= 0 else "−"} {m(abs(loan))} − {m(div)} = {m(fin)} [2]'),
        lambda r: ('Calculate the closing cash and cash equivalents.', m(open_ + chg), f'Net change {m(chg)} [1]; {m(open_)} + {m(chg)} = {m(open_ + chg)} [1] [2]'),
        lambda r: ('Evaluate the company\'s cash position for its shareholders, referring to your figures.', f'Operating cash {m(op)} {"covers" if op >= buy + div else "does not cover"} investment {m(buy)} and dividends {m(div)}; ' + ('reliance on external finance.' if op < buy + div else 'internally financed growth.'),
                   'Uses operating vs investing figures [2]; comments on financing/dividend sustainability [1]; conclusion [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t3_3.add('C4', (2, 3, 4, 5), 'multi_step')(_cf_c4)
t3_3.add('C3', (4, 5), 'multi_step')(_cf_c4)
t3_1.add('C4', (3, 4, 5), 'multi_step')(_cf_c4)


@t3_3.add('C2', (2, 3, 4), 'explain')
def t33_err(r, D):
    c = co(r)
    v = step(r, 5000, 40000, 500)
    item = r.choice([('increase in inventories', 'added', 'deducted'), ('increase in trade payables', 'deducted', 'added'), ('decrease in trade receivables', 'deducted', 'added'), ('profit on disposal', 'added', 'deducted'), ('depreciation', 'deducted', 'added')])
    return {'stem': f'In the draft statement of cash flows of {c}, the {item[0]} of {m(v)} was {item[1]} in reconciling profit from operations to cash generated from operations. Explain the error and calculate its effect on the reported cash generated from operations.',
            'answer': f'The {item[0]} should be {item[2]}. Cash generated from operations is misstated by 2 × {m(v)} = {m(2 * v)} ({"overstated" if item[1] == "added" else "understated"}).',
            'key': f'Correct treatment ({item[2]}) [1]; reason linked to cash [1]; effect {m(2 * v)} {"overstated" if item[1] == "added" else "understated"} [1] [3]'}


t3_4 = topic('Role of the auditor and the audit report', 'role of the auditor and the audit report', 'auditor', 'audit report')
fixed(t3_4, 'C1', (1, 2), [
    ('The main purpose of an external audit is to', 'give an independent opinion on whether the financial statements show a true and fair view', 'External auditor reports to shareholders on truth and fairness [1].',
     ['detect every fraud in the company', 'prepare the financial statements', 'manage the company\'s accounting staff']),
    ('External auditors are appointed by and report to the', 'shareholders', 'Auditors are appointed by members at the AGM and report to them [1].',
     ['directors', 'customers', 'tax authorities only']),
    ('An unmodified (clean) audit opinion means the auditor', 'is satisfied the statements give a true and fair view', 'Unmodified = true and fair, prepared per framework [1].',
     ['found no errors at all', 'guarantees the company will make a profit', 'has prepared the statements']),
    ('An adverse opinion is given when misstatements are', 'both material and pervasive', 'Material & pervasive misstatement → adverse; material not pervasive → qualified [1].',
     ['immaterial', 'material but limited to one area', 'not yet investigated']),
    ('Who is responsible for preparing the financial statements of a limited company?', 'The directors', 'Directors prepare; auditors give opinion [1].',
     ['The external auditor', 'The shareholders', 'The bank']),
])
fixed(t3_4, 'C2', (2, 3, 4), [
    ('Distinguish between the role of the directors and the role of the external auditor in relation to the financial statements.', 'Directors prepare the statements and are responsible for their accuracy and for internal controls (stewardship); auditors independently examine them and report an opinion to shareholders.',
     'Directors prepare/responsible [1]; auditors independent opinion to shareholders [1] [2]'),
    ('Explain the meaning of "true and fair view".', 'True: free from material error and factually correct; fair: presented objectively without bias, in accordance with accounting standards.',
     'True explained [1]; fair explained [1] [2]'),
    ('Explain why the independence of the external auditor is important.', 'Shareholders rely on the opinion; if the auditor has financial or personal links with the company the opinion may be biased and the credibility of the statements is lost.',
     'Users rely on opinion [1]; conflict of interest causes bias [1]; credibility [1] [3]'),
    ('Distinguish between an internal auditor and an external auditor.', 'Internal auditors are employees reporting to management on controls and efficiency; external auditors are independent, appointed by shareholders, and report on the financial statements.',
     'Internal: employee, management [1]; external: independent, shareholders, statutory [1] [2]'),
])


@t3_4.add('C3', (1, 2, 3, 4, 5))
def t34_mat(r, D):
    c = co(r)
    pbt = step(r, 200000, 2000000, 10000)
    th = r.choice([5, 5, 10])
    mis = step(r, 2000, int(pbt * 0.12), 500)
    pervasive = r.random() < 0.3 and D >= 3
    mat = pbt * th // 100
    is_mat = mis >= mat
    issue = r.choice(['an unrecorded provision for a legal claim', 'inventory overvalued at cost instead of net realisable value', 'depreciation not charged on a new machine', 'a receivable from a customer who is now insolvent'])
    op = ('adverse' if pervasive else 'qualified ("except for")') if is_mat else 'unmodified'
    stem = f'The auditor of {c} uses a materiality threshold of {th}% of profit before tax, which is {m(pbt)}. The directors refuse to correct {issue} of {m(mis)}.' + (' The auditor considers that the issue affects many areas of the statements.' if pervasive else '')
    key = f'Materiality = {th}% × {m(pbt)} = {m(mat)} [1]; {m(mis)} is {"" if is_mat else "not "}material [1]; opinion: {op} [1]'
    if D == 1:
        opts, ans = mm(r, mat, [pbt * 10 // 100 if th == 5 else pbt * 5 // 100, mis, pbt * th // 1000, mat * 2])
        return {'stem': stem + ' What is the materiality threshold in dollars?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + ' Calculate whether the misstatement is material and state, with a reason, the type of audit opinion the auditor should give.',
            'answer': f'Threshold {m(mat)}; misstatement {"is" if is_mat else "is not"} material; {op} opinion', 'key': key, 'marks': 3}


@t3_4.add('C2', (2, 3, 4), 'explain')
def t34_case(r, D):
    c = co(r)
    cases = [('The auditor\'s brother is the finance director of the company.', 'Independence is compromised; the auditor should decline or resign from the engagement.'),
             ('The audit firm also earns large consultancy fees from the company.', 'Fee dependence threatens independence; safeguards or limits on non-audit services are needed.'),
             ('The directors will not allow the auditor to inspect the inventory records.', 'This is a limitation of scope; if material the auditor issues a qualified opinion or disclaimer.'),
             ('Shareholders claim the auditor should have found a small theft of petty cash.', 'An audit gives reasonable, not absolute, assurance; immaterial frauds may not be detected; primary responsibility for preventing fraud lies with directors.'),
             ('The finance director asks the auditor to prepare the year-end statements as well as audit them.', 'Self-review threat: the auditor would be checking his own work; directors must prepare the statements.')]
    a = r.choice(cases)
    return {'stem': f'Read the situation at {c}: "{a[0]}" Explain the audit issue and what the auditor should do.', 'answer': a[1], 'key': 'Identifies the issue (independence/scope/expectation gap) [1]; explains why it matters to users [1]; appropriate action [1] [3]'}


def _aud_c4(r, D):
    c = co(r)
    pbt = step(r, 300000, 1500000, 10000)
    a, b = step(r, 5000, int(pbt * 0.08), 1000), step(r, 5000, int(pbt * 0.08), 1000)
    mat = pbt * 5 // 100
    intro = (f'The draft profit before tax of {c} is {m(pbt)}. The auditor\'s materiality level is 5% of profit before tax. Two issues remain: inventory is overstated by {m(a)} and a provision for a warranty claim of {m(b)} has not been made. The directors say both are "too small to matter".')
    tot = a + b
    parts = [
        lambda r: ('Calculate the materiality level and the corrected profit before tax.', f'{m(mat)}; corrected PBT {m(pbt - tot)}', f'5% × {m(pbt)} = {m(mat)} [1]; {m(pbt)} − {m(a)} − {m(b)} = {m(pbt - tot)} [1] [2]'),
        lambda r: ('State, with reasons, whether each issue is material on its own and in total.', f'Inventory {"material" if a >= mat else "not material"}; provision {"material" if b >= mat else "not material"}; total {m(tot)} {"is" if tot >= mat else "is not"} material',
                   'Each judged against threshold [2]; aggregate [1] [3]'),
        lambda r: ('Advise the auditor on the type of opinion to give if the directors refuse to make adjustments.', f'{"Qualified (except for) opinion — material but not pervasive" if tot >= mat else "Unmodified opinion — misstatements immaterial in total"}', 'Correct opinion [1]; justified with figures [2] [3]'),
        lambda r: ('Discuss why shareholders rely on the audit report.', 'Shareholders are not involved in management (separation of ownership and control); the report gives independent assurance on the directors\' stewardship.', 'Separation of ownership/control [1]; independence/assurance [1]; stewardship [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t3_4.add('C4', (2, 3, 4, 5), 'multi_step')(_aud_c4)
t3_4.add('C3', (4, 5), 'multi_step')(_aud_c4)


def _pub_c4(r, D):
    c = co(r)
    rev = step(r, 1000000, 4000000, 10000); gp = round(rev * r.choice([0.3, 0.35, 0.4, 0.45]) / 1000) * 1000
    dist, adm = step(r, 60000, 200000, 1000), step(r, 80000, 250000, 1000)
    fin = step(r, 10000, 50000, 1000); tax = step(r, 30000, 120000, 1000)
    pfo = gp - dist - adm; pbt = pfo - fin; pfy = pbt - tax
    N = step(r, 400000, 1500000, 50000); dps = r.choice([0.05, 0.06, 0.08, 0.1]); div = round(N * dps)
    re0 = step(r, 100000, 400000, 1000)
    prop = r.choice([0.02, 0.03, 0.04])
    intro = f'{c} reports revenue of {m(rev)} and gross profit of {m(gp)} for the year ended {ye(r)}. Distribution costs were {m(dist)}, administrative expenses {m(adm)}, finance costs {m(fin)} and tax {m(tax)}. It has {nm(N)} ordinary shares of $1; a dividend of ${dps:.2f} per share was paid during the year. Opening retained earnings were {m(re0)}.'
    parts = [
        lambda r: ('Calculate the profit from operations and the profit for the year.', f'{m(pfo)}; {m(pfy)}', f'{m(gp)} − {m(dist)} − {m(adm)} = {m(pfo)} [1]; − {m(fin)} − {m(tax)} = {m(pfy)} [1] [2]'),
        lambda r: ('Calculate the closing retained earnings.', m(re0 + pfy - div), f'{m(re0)} + {m(pfy)} − dividend {m(div)} = {m(re0 + pfy - div)} [2]'),
        lambda r: (f'After the year end the directors propose a final dividend of ${prop:.2f} per share. Explain how this is treated in the financial statements.', f'Not a liability at the reporting date (IAS 10); disclosed in a note: {m(N * prop)}.', 'Not recognised [1]; note disclosure with amount [1] [2]'),
        lambda r: ('Explain why dividends paid are not shown in the income statement.', 'Dividends are distributions of profit to owners, not expenses incurred to earn revenue; they appear in the statement of changes in equity.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t3_1.add('C4', (2, 3, 4, 5), 'multi_step')(_pub_c4)
t3_2.add('C4', (2, 3, 4, 5), 'multi_step')(_pub_c4)
t3_1.add('C3', (4, 5), 'multi_step')(_pub_c4)
t3_2.add('C3', (4, 5), 'multi_step')(_pub_c4)

CHAPTERS[3] = [t3_1, t3_2, t3_3, t3_4]


# ===================================================================== 4 International Accounting Standards
t4_1 = topic('IAS 16 Property, plant and equipment and IAS 36 Impairment', 'ias 16 property, plant and equipment and ias 36 impairment of assets', 'ias 16', 'ias 36', 'impairment')
fixed(t4_1, 'C1', (1, 2), [
    ('Under IAS 16, which cost should NOT be included in the initial cost of a machine?', 'Training staff to use the machine', 'Cost includes purchase price, duties, delivery, installation, testing; excludes training and general overheads [1].',
     ['Delivery charges', 'Installation costs', 'Import duty']),
    ('Under IAS 36, the recoverable amount of an asset is', 'the higher of fair value less costs to sell and value in use', 'Recoverable amount = max(FV − costs of disposal, VIU) [1].',
     ['the lower of cost and net realisable value', 'the carrying amount less depreciation', 'the original cost']),
    ('An asset is impaired when', 'its carrying amount exceeds its recoverable amount', 'Impairment loss = carrying amount − recoverable amount [1].',
     ['its market value rises', 'it is fully depreciated', 'its useful life is extended']),
    ('When an item of PPE is revalued upwards, the gain is credited to', 'a revaluation surplus (reserve) in equity', 'IAS 16: surplus to OCI/revaluation reserve [1].',
     ['revenue in the income statement', 'retained earnings directly as realised profit', 'the share premium account']),
    ('Depreciation under IAS 16 is defined as', 'the systematic allocation of the depreciable amount of an asset over its useful life', 'Depreciable amount = cost − residual value, allocated over useful life [1].',
     ['a fall in the market value of an asset', 'a fund of cash set aside to replace assets', 'the amount for which an asset could be sold']),
    ('Value in use is', 'the present value of the future cash flows expected from an asset', 'VIU = PV of expected future cash flows (IAS 36) [1].',
     ['the price the asset would fetch on the market', 'the original purchase price', 'the carrying amount at the year end']),
])
fixed(t4_1, 'C2', (2, 3, 4), [
    ('Explain why IAS 36 requires impaired assets to be written down to their recoverable amount.', 'An asset should not be carried at more than the economic benefits it will generate; writing it down applies prudence and gives a faithful representation of the asset.',
     'Asset not overstated [1]; prudence/faithful representation [1] [2]'),
    ('Explain two indicators that an asset may be impaired.', 'External: significant fall in market value, adverse changes in technology/market, increased interest rates. Internal: physical damage, obsolescence, worse performance than expected.',
     'Two indicators [1 each] with explanation [1 each] [4]'),
    ('Explain why the residual value and useful life of assets must be reviewed at least annually under IAS 16.', 'Expectations change; reviewing ensures the depreciation charge reflects the pattern of use of the asset; changes are accounted for prospectively as a change in estimate (IAS 8).',
     'Estimates change [1]; accurate depreciation/matching [1]; prospective change of estimate [1] [3]'),
])


@t4_1.add('C3', (1, 2, 3, 4, 5))
def t41_cost(r, D):
    c = co(r)
    price = step(r, 40000, 300000, 1000)
    tdisc = r.choice([0, 5, 10]) if D >= 2 else 0
    items_in = [('delivery', step(r, 500, 6000, 100)), ('installation', step(r, 1000, 12000, 100)), ('import duty', step(r, 1000, 15000, 100)), ('testing before use', step(r, 300, 4000, 100))]
    items_out = [('staff training', step(r, 500, 5000, 100)), ('a three-year maintenance contract', step(r, 1000, 9000, 100)), ('general administration overheads apportioned', step(r, 500, 6000, 100)), ('a cash discount for prompt payment that was taken', 0)]
    ins = r.sample(items_in, 2 + (D >= 3))
    outs = r.sample(items_out[:3], 1 + (D >= 3))
    net = price * (100 - tdisc) // 100
    cost = net + sum(v for _, v in ins)
    allit = ins + outs
    r.shuffle(allit)
    stem = f'{c} bought a machine with a list price of {m(price)}' + (f' less a trade discount of {tdisc}%' if tdisc else '') + '. It also paid: ' + ', '.join(f'{a} {m(v)}' for a, v in allit) + '. Calculate the cost of the machine to be capitalised under IAS 16.'
    key = (f'Price {m(price)} − {tdisc}% = {m(net)} [1]; ' if tdisc else '') + 'include ' + ', '.join(f'{a} {m(v)}' for a, v in ins) + ' [1]; exclude ' + ', '.join(a for a, _ in outs) + f' (expensed) [1]; cost = {m(cost)} [1]'
    if D == 1:
        opts, ans = mm(r, cost, [cost + sum(v for _, v in outs), price, cost - ins[0][1], cost + 1000])
        return {'stem': stem.replace('Calculate the cost', 'What is the cost'), 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem, 'answer': m(cost), 'key': key, 'marks': 3 + bool(tdisc)}


@t4_1.add('C3', (1, 2, 3, 4, 5))
def t41_imp(r, D):
    c = co(r)
    ca = step(r, 50000, 500000, 1000)
    fv = round(ca * r.uniform(0.55, 1.1) / 1000) * 1000
    cts = step(r, 1000, 9000, 500)
    viu = round(ca * r.uniform(0.5, 1.05) / 1000) * 1000
    rec = max(fv - cts, viu)
    loss = max(0, ca - rec)
    asset = r.choice(['a specialist printing press', 'a delivery fleet', 'a bottling line', 'a retail store fit-out', 'a fishing trawler', 'a solar farm'])
    stem = f'{c} owns {asset} with a carrying amount of {m(ca)}. It could be sold for {m(fv)} with selling costs of {m(cts)}. The present value of the future cash flows from using it is {m(viu)}.'
    key = f'FV less costs to sell = {m(fv - cts)} [1]; value in use = {m(viu)}; recoverable amount = higher = {m(rec)} [1]; impairment = {m(ca)} − {m(rec)} = {m(loss)} [1]' if loss else f'FV less costs = {m(fv - cts)}; VIU {m(viu)}; recoverable {m(rec)} ≥ carrying amount, so no impairment [2]'
    if D == 1:
        opts, ans = mm(r, loss, [ca - min(fv - cts, viu), ca - fv, ca - viu + 5000, 0 if loss else 5000, abs(ca - fv - 2000)])
        return {'stem': stem + ' What is the impairment loss?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the recoverable amount and any impairment loss.'
    if D >= 4:
        q += ' State how the loss is recorded if the asset has not previously been revalued.'
        key += '; Dr impairment loss (income statement), Cr asset/accumulated impairment [1]'
    return {'stem': stem + q, 'answer': f'Recoverable amount {m(rec)}; impairment loss {m(loss)}', 'key': key, 'marks': 3 + (D >= 4)}


@t4_1.add('C3', (2, 3, 4, 5))
def t41_reval(r, D):
    c = co(r)
    cost = step(r, 200000, 1000000, 10000); life = r.choice([20, 25, 40, 50]); yrs = r.choice([2, 4, 5, 8, 10])
    acc = cost * yrs // life
    ca = cost - acc
    newv = ca + step(r, 20000, 300000, 10000)
    rem = life - yrs
    newdep = newv / rem
    return {'stem': f'{c} bought a building for {m(cost)}, depreciated straight-line over {life} years with no residual value. After {yrs} years it is revalued to {m(newv)}; the remaining useful life is unchanged. Calculate the revaluation surplus and the annual depreciation charge after revaluation.',
            'answer': f'Revaluation surplus {m(newv - ca)}; new annual depreciation {m(newdep)}',
            'key': f'Accumulated depreciation {yrs}/{life} × {m(cost)} = {m(acc)} [1]; carrying amount {m(ca)} [1]; surplus {m(newv)} − {m(ca)} = {m(newv - ca)} to revaluation reserve [1]; new depreciation {m(newv)}/{rem} = {m(newdep)} [1]', 'marks': 4}


def _ias16_c4(r, D):
    c = co(r)
    cost = step(r, 80000, 400000, 1000); res = step(r, 0, cost // 10, 1000); life = r.choice([4, 5, 8, 10])
    y = r.choice([2, 3])
    sl = (cost - res) / life
    ca = cost - sl * y
    viu = round(ca * r.uniform(0.5, 0.85) / 1000) * 1000; fv = viu - step(r, 1000, 10000, 1000); cts = step(r, 500, 3000, 500)
    rec = max(viu, fv - cts); loss = ca - rec
    rem = life - y
    nd = (rec - res) / rem if rec > res else 0
    asset = r.choice(['packaging machine', 'refrigeration unit', 'CNC lathe', 'bakery oven', 'printing press'])
    intro = f'{c} bought a {asset} for {m(cost)} with an estimated residual value of {m(res)} and a useful life of {life} years (straight-line). After {y} years, a competitor launches a cheaper technology. The value in use is now estimated at {m(viu)}; the machine could be sold for {m(fv)} less selling costs of {m(cts)}.'
    parts = [
        lambda r: ('Calculate the annual depreciation and the carrying amount before the impairment review.', f'{m(sl)}; {m(ca)}', f'({m(cost)} − {m(res)})/{life} = {m(sl)} [1]; {m(cost)} − {y} × {m(sl)} = {m(ca)} [1] [2]'),
        lambda r: ('Calculate the impairment loss.', m(loss), f'Recoverable = higher of {m(fv - cts)} and {m(viu)} = {m(rec)} [1]; loss {m(ca)} − {m(rec)} = {m(loss)} [1] [2]'),
        lambda r: ('Calculate the depreciation charge for each remaining year after the impairment.', m(nd), f'({m(rec)} − {m(res)}) / {rem} = {m(nd)} [2]'),
        lambda r: ('Explain why the competitor\'s new technology is an indicator of impairment.', 'It reduces the demand/value of the output and the cash flows the machine can generate, so its recoverable amount may fall below carrying amount.', '[2]'),
        lambda r: ('Discuss the effect of the impairment on the company\'s reported profit and return on capital employed.', f'Profit falls by {m(loss)} this year (expense); capital employed falls, so future ROCE may rise as depreciation is lower.', 'Profit effect with figure [1]; capital employed effect [1]; future years [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t4_1.add('C4', (2, 3, 4, 5), 'multi_step')(_ias16_c4)
t4_1.add('C3', (4, 5), 'multi_step')(_ias16_c4)


@t4_1.add('C2', (2, 3, 4), 'explain')
def t41_err(r, D):
    c = co(r)
    tr = step(r, 1000, 8000, 500); inst = step(r, 1000, 8000, 500)
    return {'stem': f'When {c} bought new equipment, the accountant capitalised staff training of {m(tr)} and charged installation costs of {m(inst)} to the income statement. Explain the errors and their net effect on the carrying amount of the equipment.',
            'answer': f'Training is not a cost of bringing the asset to working condition and must be expensed; installation is directly attributable and must be capitalised. The asset is {"overstated" if tr > inst else "understated"} by {m(abs(tr - inst))}.',
            'key': f'Training expensed (IAS 16) [1]; installation capitalised [1]; net effect {m(abs(tr - inst))} {"overstated" if tr > inst else "understated"} [1] [3]'}


t4_2 = topic('IAS 2 Inventories and IAS 8 Accounting policies, estimates and errors', 'ias 2 inventories and ias 8 accounting policies, changes in estimates and errors', 'ias 2', 'ias 8', 'inventories', 'net realisable value')
fixed(t4_2, 'C1', (1, 2), [
    ('Under IAS 2, inventories are valued at', 'the lower of cost and net realisable value', 'IAS 2: lower of cost and NRV, item by item [1].',
     ['the higher of cost and net realisable value', 'selling price', 'replacement cost']),
    ('Net realisable value is', 'estimated selling price less estimated costs of completion and selling', 'NRV = SP − costs to complete − costs to sell [1].',
     ['cost plus profit margin', 'the original purchase price', 'selling price plus delivery costs']),
    ('Which cost method is NOT permitted by IAS 2?', 'LIFO (last in, first out)', 'IAS 2 allows FIFO or weighted average, not LIFO [1].',
     ['FIFO', 'Weighted average cost', 'Specific identification for unique items']),
    ('Under IAS 8 a change in the estimated useful life of a machine is', 'a change in accounting estimate, applied prospectively', 'Estimates: prospective; policies and errors: retrospective [1].',
     ['a change in accounting policy, applied retrospectively', 'a prior period error', 'not allowed']),
    ('Under IAS 8, a material prior period error is corrected', 'retrospectively, by restating the comparative figures', 'Errors restated retrospectively [1].',
     ['only in the current year income statement', 'by a note with no adjustment', 'in the following year']),
    ('Which of these costs may be included in the cost of inventory under IAS 2?', 'Carriage inwards', 'Purchase costs, conversion costs, costs to bring to present location [1].',
     ['Selling costs', 'Storage after production unless necessary', 'Abnormal wastage']),
])
fixed(t4_2, 'C2', (2, 3, 4), [
    ('Explain why IAS 2 requires inventory to be valued at the lower of cost and net realisable value.', 'Prudence: assets should not be overstated; a loss expected on sale is recognised immediately, while profits are recognised only when realised.',
     'Prudence/no overstatement [1]; losses recognised when foreseen [1] [2]'),
    ('Distinguish between a change in accounting policy and a change in accounting estimate under IAS 8, giving an example of each.', 'Policy: change in the principles/bases used, e.g. FIFO to weighted average, applied retrospectively. Estimate: revised judgement, e.g. useful life or allowance for receivables, applied prospectively.',
     'Policy defined + example [1]; estimate defined + example [1]; retrospective vs prospective [1] [3]'),
    ('Explain when a company may change an accounting policy under IAS 8.', 'Only if required by a standard or if the change gives more reliable and relevant information; otherwise policies must be applied consistently.',
     'Required by IFRS [1]; more relevant/reliable [1] [2]'),
])


@t4_2.add('C3', (1, 2, 3, 4, 5))
def t42_nrv(r, D):
    c = co(r)
    n = 2 if D <= 2 else 3 + (D >= 4)
    names = r.sample(['Line A', 'Line B', 'Line C', 'Line D', 'Model P', 'Model Q', 'Model R', 'Batch 7', 'Batch 9'], n)
    rows, tot, wk = [], 0, []
    for nm_ in names:
        cost = step(r, 2000, 30000, 100)
        sp = round(cost * r.uniform(0.7, 1.5) / 100) * 100
        sell = step(r, 100, 2500, 100) if D >= 3 else 0
        nrv = sp - sell
        v = min(cost, nrv)
        tot += v
        rows.append(f'{nm_}: cost {m(cost)}, selling price {m(sp)}' + (f', selling costs {m(sell)}' if sell else ''))
        wk.append(f'{nm_} {m(v)}')
    stem = f'{c} holds the following inventory at the year end — ' + '; '.join(rows) + '. Calculate the value of inventory under IAS 2.'
    key = 'Lower of cost and NRV item by item: ' + ', '.join(wk) + f' [{n - 1}]; total {m(tot)} [1]'
    if D == 1:
        opts, ans = mm(r, tot, [tot + 1500, tot - 1200, tot * 1.1, tot + 2500])
        return {'stem': stem.replace('Calculate the value', 'What is the value'), 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem, 'answer': m(tot), 'key': key, 'marks': n}


@t4_2.add('C3', (2, 3, 4, 5))
def t42_est(r, D):
    c = co(r)
    cost = step(r, 60000, 400000, 1000); life = r.choice([5, 8, 10]); y = r.choice([2, 3])
    newrem = r.choice([2, 3, 4, 6, 8])
    res = step(r, 0, cost // 10, 1000) if D >= 3 else 0
    dep = (cost - res) / life
    ca = cost - dep * y
    nd = (ca - res) / newrem
    return {'stem': f'{c} bought equipment for {m(cost)}, depreciated straight-line over {life} years' + (f' with a residual value of {m(res)}' if res else '') + f'. At the start of year {y + 1} the directors estimate the remaining useful life to be {newrem} years. Explain how IAS 8 applies and calculate the depreciation charge for year {y + 1}.',
            'answer': f'Change in accounting estimate — prospective, no restatement. Year {y + 1} charge {m(nd)}',
            'key': f'Change in estimate, prospective [1]; carrying amount after {y} years {m(ca)} [1]; ({m(ca)} − {m(res)}) / {newrem} = {m(nd)} [1]', 'marks': 3}


@t4_2.add('C2', (2, 3, 4), 'explain')
def t42_err(r, D):
    c = co(r)
    cost = step(r, 5000, 40000, 500); sp = cost - step(r, 1000, 4000, 500); sell = step(r, 200, 900, 100)
    return {'stem': f'{c} valued damaged goods at their cost of {m(cost)}. They can be sold for {m(sp)} after repair costs of {m(sell)}. Explain the error and its effect on profit.',
            'answer': f'IAS 2 requires the lower of cost and NRV. NRV = {m(sp - sell)}, so inventory should be {m(sp - sell)}. Inventory and profit are overstated by {m(cost - sp + sell)}.',
            'key': f'Lower of cost and NRV [1]; NRV {m(sp)} − {m(sell)} = {m(sp - sell)} [1]; profit overstated by {m(cost - sp + sell)} [1] [3]'}


def _inv_c4(r, D):
    c = co(r)
    profit = step(r, 80000, 400000, 1000)
    inv = step(r, 50000, 200000, 1000)
    cost = step(r, 6000, 30000, 500); nrv = cost - step(r, 1500, 5000, 500)
    err = step(r, 2000, 15000, 500)
    old_dep, new_dep = step(r, 8000, 20000, 500), step(r, 5000, 15000, 500)
    adj = profit - (cost - nrv) - err + (old_dep - new_dep)
    intro = (f'The draft profit of {c} for the year is {m(profit)} and closing inventory is {m(inv)}. The auditors find: (1) inventory includes goods at cost {m(cost)} with NRV of {m(nrv)}; (2) purchases of {m(err)} for the current year were omitted from the records in error; '
             f'(3) the directors have revised the useful life of machinery, so the depreciation charge for this year should be {m(new_dep)} instead of the {m(old_dep)} included.')
    parts = [
        lambda r: ('Calculate the revised profit for the year.', m(adj), f'{m(profit)} − {m(cost - nrv)} (NRV) − {m(err)} (purchases) {"+" if old_dep >= new_dep else "−"} {m(abs(old_dep - new_dep))} (depreciation) = {m(adj)} [4]'),
        lambda r: ('Calculate the revised closing inventory.', m(inv - (cost - nrv)), f'{m(inv)} − {m(cost - nrv)} = {m(inv - cost + nrv)} [1]'),
        lambda r: ('State and explain how IAS 8 classifies item (3).', 'Change in accounting estimate: applied prospectively from the current year, no restatement of prior years.', 'Classification [1]; prospective treatment [1] [2]'),
        lambda r: ('Explain why the directors may be reluctant to accept these adjustments.', 'They reduce reported profit, which may affect bonuses, share price and dividends; however the standards require faithful representation.', 'Motive [1]; ethical/standards point [1] [2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t4_2.add('C4', (2, 3, 4, 5), 'multi_step')(_inv_c4)
t4_2.add('C3', (4, 5), 'multi_step')(_inv_c4)


t4_3 = topic('IAS 10 Events after the reporting period and IAS 37 Provisions', 'ias 10 events after the reporting period and ias 37 provisions and contingencies', 'ias 10', 'ias 37', 'provisions', 'contingent')
EVENTS = [
    ('a major customer, owing {v} at the year end, was declared bankrupt', 'adjusting', 'provides evidence of conditions at the year end (receivable was irrecoverable)', -1),
    ('inventory held at the year end at cost of {v} was sold for {w} less than cost', 'adjusting', 'gives evidence of NRV at the year end', -1),
    ('a fire destroyed a warehouse valued at {v}', 'non-adjusting', 'condition arose after the year end; disclose if material', 0),
    ('the company issued new shares raising {v}', 'non-adjusting', 'new transaction after the year end; disclose', 0),
    ('a court case outstanding at the year end was settled, the company paying damages of {v}', 'adjusting', 'confirms an obligation that existed at the year end', -1),
    ('the market value of investments fell by {v} because of a stock market crash', 'non-adjusting', 'decline arose after the year end', 0),
    ('an error was discovered showing that sales of {v} had been recorded twice', 'adjusting', 'discovery of an error in the year-end figures', -1),
    ('the company announced a plan to close a division, costing {v}', 'non-adjusting', 'decision taken after the year end; disclose', 0),
]
fixed(t4_3, 'C1', (1, 2), [
    ('Under IAS 37 a provision is recognised when there is a present obligation, a probable outflow of resources and', 'a reliable estimate of the amount', 'All three conditions required [1].',
     ['the amount is certain', 'the directors agree', 'the auditor approves']),
    ('A contingent liability whose outflow is possible but not probable should be', 'disclosed in a note', 'Possible → disclose; probable → provide; remote → ignore [1].',
     ['provided for in the statement of financial position', 'ignored', 'charged to the income statement']),
    ('A contingent asset that is probable should be', 'disclosed in a note but not recognised', 'Contingent assets recognised only when virtually certain [1].',
     ['recognised as an asset', 'ignored', 'credited to revenue']),
    ('An adjusting event after the reporting period is one that', 'provides evidence of conditions that existed at the end of the reporting period', 'IAS 10 definition [1].',
     ['arises after the year end from new conditions', 'occurs after the financial statements are authorised', 'relates only to dividends']),
    ('Which is a non-adjusting event?', 'A fire destroying a factory two weeks after the year end', 'New condition after year end → non-adjusting, disclose if material [1].',
     ['Discovery of fraud that occurred during the year', 'Sale of year-end inventory below cost', 'Bankruptcy of a customer who owed money at the year end']),
])
fixed(t4_3, 'C2', (2, 3, 4), [
    ('Distinguish between a provision and a contingent liability.', 'A provision is a liability of uncertain timing or amount that is probable and can be measured reliably, so it is recognised; a contingent liability is only possible (or cannot be measured), so it is disclosed only.',
     'Provision: probable, reliable, recognised [1]; contingent liability: possible, disclosed [1] [2]'),
    ('Explain why non-adjusting events should be disclosed even though they do not change the figures.', 'Material events after the year end could influence users\' decisions; without disclosure users would be misled about the company\'s current position.',
     'Material to decisions [1]; avoids misleading users [1] [2]'),
    ('Explain why a company cannot create a provision for future operating losses.', 'There is no present obligation arising from a past event; future losses relate to future activity, so IAS 37 prohibits a provision.',
     'No present obligation [1]; no past event [1] [2]'),
])


@t4_3.add('C3', (1, 2, 3, 4, 5))
def t43_events(r, D):
    c = co(r)
    profit = step(r, 100000, 600000, 1000)
    k = 2 if D <= 2 else 3 + (D >= 4)
    evs = r.sample(EVENTS, k)
    if D == 1:
        evs = [e for e in EVENTS if e[3]][:0] + r.sample([e for e in EVENTS if e[3]], 1) + r.sample([e for e in EVENTS if not e[3]], 1)
    txt, adj, wk = [], 0, []
    for e in evs:
        v = step(r, 3000, 40000, 500); w = step(r, 500, v // 2, 500) if v > 1000 else 500
        d = e[0].format(v=m(v), w=m(w))
        amt = w if 'less than cost' in d else v
        txt.append(d)
        if e[3]:
            adj += amt; wk.append(f'"{d}" adjusting: −{m(amt)}')
        else:
            wk.append(f'"{d}" non-adjusting: disclose only')
    stem = f'The draft profit of {c} for the year ended {ye(r)} is {m(profit)}. Before the financial statements were authorised: ' + '; '.join(f'({i + 1}) {t}' for i, t in enumerate(txt)) + '. Calculate the revised profit, stating whether each event is adjusting or non-adjusting.'
    key = '; '.join(wk) + f' [1 each]; revised profit {m(profit - adj)} [1]'
    if D == 1:
        opts, ans = mm(r, profit - adj, [profit, profit - adj - step(r, 3000, 30000, 500), profit + adj, profit - 2 * adj])
        return {'stem': stem.replace('Calculate the revised profit', 'What is the revised profit'), 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem, 'answer': f'Revised profit {m(profit - adj)}', 'key': key, 'marks': k + 1}


@t4_3.add('C3', (1, 2, 3, 4))
def t43_prov(r, D):
    c = co(r)
    cases = [('a customer is suing for {v}; lawyers advise the company will probably lose', 'provision', True),
             ('a customer is suing for {v}; lawyers advise it is possible but unlikely the company will lose', 'contingent liability (disclose)', False),
             ('the company has guaranteed a supplier\'s bank loan of {v}; the supplier is financially sound', 'contingent liability (disclose) — or ignore if remote', False),
             ('products are sold with a one-year warranty; past experience suggests claims of {v}', 'provision', True),
             ('the company is suing a competitor for {v} and expects to win', 'contingent asset (disclose)', False),
             ('the company plans to refurbish its offices next year at a cost of {v}', 'no provision (no present obligation)', False),
             ('a law requires the company to clean up land it has already contaminated, estimated at {v}', 'provision', True)]
    sel = r.sample(cases, 2 if D <= 2 else 3)
    vals = [step(r, 5000, 80000, 1000) for _ in sel]
    tot = sum(v for (d, t, p), v in zip(sel, vals) if p)
    lines = [d.format(v=m(v)) for (d, _, _), v in zip(sel, vals)]
    stem = f'At the year end, {c} faces the following: ' + '; '.join(f'({i + 1}) {l}' for i, l in enumerate(lines)) + '. Apply IAS 37 to each and calculate the total provision to be recognised.'
    key = '; '.join(f'({i + 1}) {t}' for i, (_, t, _) in enumerate(sel)) + f' [1 each]; total provision {m(tot)} [1]'
    if D == 1:
        opts, ans = mm(r, tot, [sum(vals), 0 if tot else sum(vals) // 2, tot + vals[0] if tot != vals[0] else tot + 5000, sum(vals) - tot + 1000])
        return {'stem': stem.replace('Apply IAS 37 to each and calculate', 'What is'), 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem, 'answer': '; '.join(f'({i + 1}) {t}' for i, (_, t, _) in enumerate(sel)) + f'. Total provision {m(tot)}', 'key': key, 'marks': len(sel) + 1}


def _ias10_c4(r, D):
    c = co(r)
    profit = step(r, 150000, 700000, 1000); ca = step(r, 100000, 400000, 1000); cl = step(r, 60000, 250000, 1000)
    bad = step(r, 5000, 30000, 500); fire = step(r, 20000, 100000, 1000); claim = step(r, 10000, 60000, 1000)
    intro = (f'{c} has a draft profit of {m(profit)}, current assets {m(ca)} and current liabilities {m(cl)} at its year end. After the year end: a customer owing {m(bad)} at the year end went into liquidation; a flood destroyed inventory bought after the year end costing {m(fire)}. '
             f'At the year end a former employee was claiming {m(claim)} for unfair dismissal; lawyers think the claim will probably succeed.')
    np_ = profit - bad - claim
    parts = [
        lambda r: ('Calculate the revised profit.', m(np_), f'Bad debt adjusting −{m(bad)} [1]; flood non-adjusting [1]; provision −{m(claim)} [1]; {m(np_)} [1] [4]'),
        lambda r: ('Calculate the current ratio before and after the adjustments.', f'{ca / cl:.2f}:1 → {(ca - bad) / (cl + claim):.2f}:1', f'{m(ca)}/{m(cl)} [1]; ({m(ca - bad)})/({m(cl + claim)}) [2] [3]'),
        lambda r: ('Explain how the flood should be reported.', 'Non-adjusting event: disclose nature and estimated financial effect in a note if material; no change to figures.', '[2]'),
        lambda r: ('Discuss whether the directors should be allowed to omit the provision because "the case has not been decided yet".', 'No: a present obligation from a past event exists, outflow is probable and estimable, so IAS 37 requires a provision; omitting it overstates profit and misleads users.', 'IAS 37 criteria applied [2]; consequence for users/ethics [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t4_3.add('C4', (2, 3, 4, 5), 'multi_step')(_ias10_c4)
t4_3.add('C3', (4, 5), 'multi_step')(_ias10_c4)


@t4_3.add('C2', (2, 3, 4), 'explain')
def t43_explain(r, D):
    e = r.choice(EVENTS)
    v = step(r, 5000, 60000, 1000)
    d = e[0].format(v=m(v), w=m(v // 3))
    return {'stem': f'Two weeks after the year end of {co(r)}, {d}. State whether this is an adjusting or non-adjusting event under IAS 10 and explain how it is treated.',
            'answer': f'{e[1].capitalize()}: {e[2]}.' + (' The figures are amended.' if e[3] else ' The financial statements are not adjusted.'),
            'key': f'{e[1]} [1]; reason: {e[2]} [1]; treatment [1] [3]'}


t4_4 = topic('IAS 38 Intangible assets', 'ias 38 intangible assets', 'intangible assets', 'research and development')
fixed(t4_4, 'C1', (1, 2), [
    ('Under IAS 38, research expenditure must be', 'written off as an expense when incurred', 'Research: expense; development: capitalise if criteria met [1].',
     ['capitalised as an intangible asset', 'added to the cost of inventory', 'credited to a reserve']),
    ('Which of these may be recognised as an intangible asset?', 'A purchased patent', 'Purchased intangibles are recognised; internally generated brands are not [1].',
     ['An internally generated brand name', 'Internally generated goodwill', 'Staff training costs']),
    ('Capitalised development costs are', 'amortised over the period of expected benefit once the product is available for use', 'Amortisation begins when the asset is ready for use [1].',
     ['never amortised', 'amortised from the date research begins', 'revalued every year']),
    ('Which is NOT a criterion for capitalising development expenditure?', 'The project has been approved by the shareholders', 'Criteria: technical feasibility, intention to complete, ability to use/sell, probable benefits, resources, reliable measurement [1].',
     ['It is technically feasible', 'Future economic benefits are probable', 'Expenditure can be measured reliably']),
])
fixed(t4_4, 'C2', (2, 3, 4), [
    ('Explain why internally generated brands cannot be recognised as assets under IAS 38.', 'Their cost cannot be distinguished from the cost of developing the business as a whole and cannot be measured reliably.',
     'Cost not separable from business development [1]; not reliably measurable [1] [2]'),
    ('Distinguish between research and development expenditure.', 'Research is original investigation to gain new knowledge with uncertain outcome; development applies that knowledge to produce new or improved products before commercial production.',
     'Research defined [1]; development defined [1] [2]'),
    ('Explain why capitalising development costs can improve reported profit in the short term.', 'Costs go to the statement of financial position rather than the income statement, so current expenses fall; the cost is charged later as amortisation.',
     'Expense deferred [1]; amortised later (matching) [1] [2]'),
])


@t4_4.add('C3', (1, 2, 3, 4, 5))
def t44_rd(r, D):
    c = co(r)
    res = step(r, 20000, 150000, 1000)
    dev1 = step(r, 30000, 200000, 1000)
    dev2 = step(r, 20000, 150000, 1000) if D >= 3 else 0
    life = r.choice([4, 5, 8, 10])
    amort = (dev1 + dev2) / life if D >= 4 else 0
    prod = r.choice(['a new vaccine', 'an electric scooter battery', 'a drought-resistant seed', 'a water filtration unit', 'a mobile banking app'])
    stem = f'{c} spent {m(res)} on research into {prod} and {m(dev1)} on development after all IAS 38 criteria were met.'
    if dev2:
        stem += f' A further {m(dev2)} of development was spent before technical feasibility was demonstrated.'
        dev_cap = dev1; exp = res + dev2
    else:
        dev_cap = dev1; exp = res
    if D >= 4:
        stem += f' Production began at the year end and capitalised costs are to be amortised over {life} years from next year.'
        amort = dev_cap / life
    key = f'Research {m(res)} expensed [1]; ' + (f'pre-feasibility development {m(dev2)} expensed [1]; ' if dev2 else '') + f'capitalise {m(dev_cap)} [1]' + (f'; annual amortisation {m(dev_cap)}/{life} = {m(amort)} [1]' if D >= 4 else '')
    if D == 1:
        opts, ans = mm(r, dev_cap, [res + dev1, res, dev1 - res if dev1 > res else dev1 + res // 2, 0 if dev_cap else 1000])
        return {'stem': stem + ' What amount is recognised as an intangible asset?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the amount charged as an expense and the amount capitalised' + (', and the annual amortisation.' if D >= 4 else '.')
    return {'stem': stem + q, 'answer': f'Expense {m(exp)}; capitalised {m(dev_cap)}' + (f'; amortisation {m(amort)} a year' if D >= 4 else ''), 'key': key, 'marks': 2 + bool(dev2) + (D >= 4)}


def _ias38_c4(r, D):
    c = co(r)
    res, dev = step(r, 50000, 200000, 1000), step(r, 100000, 400000, 1000)
    pat = step(r, 30000, 150000, 1000); plife = r.choice([5, 10, 15])
    brand = step(r, 100000, 500000, 10000)
    profit = step(r, 200000, 900000, 1000)
    intro = (f'{c} has a draft profit of {m(profit)}. The directors have capitalised: research costs {m(res)}, development costs meeting all IAS 38 criteria {m(dev)}, a patent bought during the year for {m(pat)} (legal life {plife} years, full year\'s amortisation), '
             f'and an internally generated brand valued by the marketing director at {m(brand)} (credited to profit).')
    rp = profit - res - pat / plife - brand
    parts = [
        lambda r: ('Calculate the revised profit after applying IAS 38.', m(rp), f'− research {m(res)} [1]; − patent amortisation {m(pat / plife)} [1]; − brand {m(brand)} [1]; = {m(rp)} [1] [4]'),
        lambda r: ('Calculate the intangible assets to be shown in the statement of financial position.', m(dev + pat - pat / plife), f'Development {m(dev)} + patent {m(pat)} − {m(pat / plife)} = {m(dev + pat - pat / plife)} [3]'),
        lambda r: ('Explain why the brand cannot be recognised.', 'It is internally generated; its cost cannot be separated from the cost of running the business and its value is not reliably measurable.', '[2]'),
        lambda r: ('Discuss the ethical issues raised by the directors\' treatment.', 'Overstating profit and assets misleads shareholders and lenders; may be motivated by bonuses; breaches integrity/objectivity; auditors should insist on correction.', 'Two issues [2]; consequence [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t4_4.add('C4', (2, 3, 4, 5), 'multi_step')(_ias38_c4)
t4_4.add('C3', (4, 5), 'multi_step')(_ias38_c4)


@t4_4.add('C2', (2, 3, 4), 'explain')
def t44_err(r, D):
    c = co(r)
    res = step(r, 10000, 90000, 1000)
    return {'stem': f'The accountant of {c} capitalised {m(res)} spent on research into a new material, arguing that "it will definitely lead to profitable products". Explain why this treatment is wrong and its effect on the financial statements.',
            'answer': f'Research outcomes are uncertain, so IAS 38 requires research to be expensed. Profit and intangible assets are overstated by {m(res)}.',
            'key': f'Research must be expensed [1]; future benefits not demonstrable [1]; profit/assets overstated {m(res)} [1] [3]'}


CHAPTERS[4] = [t4_1, t4_2, t4_3, t4_4]


# ===================================================================== 5 Business purchase and merger
def _target(r, D):
    """Book and fair values of a business being bought."""
    prem = step(r, 80000, 300000, 1000); eq = step(r, 20000, 90000, 1000); inv = step(r, 10000, 50000, 500); rec = step(r, 8000, 40000, 500)
    pay = step(r, 6000, 30000, 500); bank = step(r, 2000, 15000, 500)
    fv_prem = prem + step(r, 10000, 80000, 1000); fv_eq = eq - step(r, 2000, 10000, 500); fv_inv = inv - step(r, 500, 4000, 500)
    allow = r.choice([2, 4, 5]); fv_rec = rec - rec * allow // 100
    return dict(prem=prem, eq=eq, inv=inv, rec=rec, pay=pay, bank=bank, fv_prem=fv_prem, fv_eq=fv_eq, fv_inv=fv_inv, fv_rec=fv_rec, allow=allow)


t5_1 = topic('Purchase of a sole trader or partnership by a limited company', 'purchase of a sole trader or partnership by a limited company', 'business purchase', 'acquisition')
fixed(t5_1, 'C1', (1, 2), [
    ('When a limited company buys an unincorporated business, the assets acquired are recorded in the company\'s books at', 'their fair values at the date of acquisition', 'IFRS 3: identifiable assets and liabilities at fair value [1].',
     ['the seller\'s book values', 'their original cost', 'their replacement cost in five years']),
    ('Purchase consideration is', 'the total value of cash, shares and other securities given to the seller', 'Consideration = cash + shares (at issue price) + debentures etc. [1].',
     ['the book value of the net assets acquired', 'the profit made by the seller', 'the amount of goodwill only']),
    ('A company buys a business and issues shares as part of the consideration. The shares are recorded at', 'their issue (fair) value, with any excess over nominal value credited to share premium', 'Share capital at nominal, premium to share premium [1].',
     ['nominal value only, ignoring any premium', 'the value of the net assets acquired', 'zero, as no cash is paid']),
    ('Which of the following is usually NOT taken over when a company buys a sole trader\'s business?', 'The seller\'s bank balance', 'The seller normally keeps cash/bank and settles own drawings [1].',
     ['Premises', 'Inventory', 'Trade receivables']),
])
fixed(t5_1, 'C2', (2, 3, 4), [
    ('Explain why a company may prefer to pay for an acquisition with shares rather than cash.', 'It conserves cash/liquidity, avoids borrowing and interest, and keeps the seller involved; but it dilutes existing shareholders\' control and EPS.',
     'Liquidity/no borrowing [1]; seller shares risk [1]; drawback dilution [1] [3]'),
    ('Explain why the net assets of the business bought are revalued to fair value before calculating goodwill.', 'Book values may be out of date; the buyer is paying for current values, so goodwill must be measured against fair values to show the true premium paid.',
     'Book values not current [1]; goodwill = consideration − fair value [1] [2]'),
    ('Explain two factors a company should consider before buying an existing business.', 'Profitability and future cash flows; quality of assets and liabilities taken over; price compared with value; financing method; staff and customer retention; synergies.',
     'Two factors [1 each] + explanation [1 each] [4]'),
])


@t5_1.add('C3', (1, 2, 3, 4, 5))
def t51_na(r, D):
    T = _target(r, D)
    A = r.choice(PEOPLE); c = co(r)
    fvna = T['fv_prem'] + T['fv_eq'] + T['fv_inv'] + T['fv_rec'] - T['pay']
    bvna = T['prem'] + T['eq'] + T['inv'] + T['rec'] - T['pay']
    stem = (f'{c} buys the business of {A}, a sole trader in {r.choice(["Accra", "Lima", "Colombo", "Hanoi", "Muscat", "Santiago", "Lagos", "Doha"])}. {A}\'s statement of financial position shows: premises {m(T["prem"])}, equipment {m(T["eq"])}, inventory {m(T["inv"])}, trade receivables {m(T["rec"])}, bank {m(T["bank"])}, trade payables {m(T["pay"])}. '
            f'{c} takes over all assets except the bank account, and all liabilities. It values premises at {m(T["fv_prem"])}, equipment at {m(T["fv_eq"])}, inventory at {m(T["fv_inv"])} and creates an allowance of {T["allow"]}% for irrecoverable debts.')
    key = f'Premises {m(T["fv_prem"])} + equipment {m(T["fv_eq"])} + inventory {m(T["fv_inv"])} + receivables {m(T["rec"])} − {T["allow"]}% = {m(T["fv_rec"])} [2]; − payables {m(T["pay"])} [1]; fair value of net assets {m(fvna)} [1]'
    if D == 1:
        opts, ans = mm(r, fvna, [bvna, fvna + T['bank'], fvna + T['pay'], fvna - T['rec'] + T['fv_rec'] - 1000])
        return {'stem': stem + ' What is the fair value of the net assets acquired?', 'options': opts, 'answer': ans, 'key': key}
    if D >= 4:
        N = step(r, 50000, 200000, 10000); p = r.choice([1.5, 2.0, 2.5]); cash = step(r, 10000, 60000, 1000)
        PC = round(N * p) + cash
        gw = PC - fvna
        return {'stem': stem + f' The consideration is {nm(N)} ordinary shares of $1 issued at ${p:.2f} and {m(cash)} cash. Calculate the fair value of net assets acquired and the goodwill or gain on bargain purchase, and state how it is shown.',
                'answer': f'Net assets {m(fvna)}; ' + (f'goodwill {m(gw)} (intangible non-current asset)' if gw > 0 else f'gain on bargain purchase {m(-gw)} (credited to profit)'),
                'key': key + f'; consideration {m(PC)} [1]; {"goodwill" if gw > 0 else "bargain purchase"} {m(abs(gw))} [1]', 'marks': 6}
    return {'stem': stem + ' Calculate the fair value of the net assets acquired.', 'answer': m(fvna), 'key': key, 'marks': 4}


def _buy_c4(r, D):
    T = _target(r, D)
    A, B = r.sample(PEOPLE, 2); c = co(r)
    fvna = T['fv_prem'] + T['fv_eq'] + T['fv_inv'] + T['fv_rec'] - T['pay']
    N = step(r, 50000, 200000, 10000); p = r.choice([1.25, 1.5, 2.0]); deb = step(r, 0, 60000, 10000) if D >= 3 else 0
    cash = step(r, 10000, 50000, 1000)
    PC = round(N * p) + cash + deb
    gw = PC - fvna
    cb = step(r, 80000, 300000, 1000)
    sc0 = step(r, 300000, 900000, 50000); sp0 = step(r, 0, 100000, 1000)
    intro = (f'{c} acquires the partnership of {A} and {B} on 1 July. The partnership\'s assets and liabilities taken over, at agreed fair values, are: premises {m(T["fv_prem"])}, equipment {m(T["fv_eq"])}, inventory {m(T["fv_inv"])}, trade receivables {m(T["fv_rec"])}, trade payables {m(T["pay"])}. '
             f'The consideration is {nm(N)} ordinary shares of $1 at ${p:.2f} each, {m(cash)} in cash' + (f' and {m(deb)} 6% debentures at par' if deb else '') + f'. Before the purchase {c} had ordinary share capital {m(sc0)}, share premium {m(sp0)} and a bank balance of {m(cb)}.')
    parts = [
        lambda r: ('Calculate the purchase consideration.', m(PC), f'{nm(N)} × ${p:.2f} = {m(N * p)} + {m(cash)}' + (f' + {m(deb)}' if deb else '') + f' = {m(PC)} [2]'),
        lambda r: ('Calculate the goodwill (or gain on bargain purchase) arising.', m(gw) if gw > 0 else f'Bargain purchase gain {m(-gw)}', f'Net assets {m(fvna)} [1]; {m(PC)} − {m(fvna)} = {m(gw)} [1] [2]'),
        lambda r: (f'Prepare the journal entry to record the purchase in the books of {c} (narrative not required).', 'Dr premises, equipment, inventory, receivables, goodwill; Cr payables, share capital, share premium, bank' + (', debentures' if deb else ''),
                   f'Assets at fair value [1]; goodwill {m(gw)} [1]; payables [1]; share capital {m(N)} and premium {m(N * (p - 1))} [1]; bank {m(cash)}' + (f', debentures {m(deb)}' if deb else '') + ' [1] [5]'),
        lambda r: (f'Calculate the balances on {c}\'s share capital, share premium and bank accounts after the acquisition.', f'Share capital {m(sc0 + N)}; share premium {m(sp0 + N * (p - 1))}; bank {m(cb - cash)}',
                   f'{m(sc0)} + {m(N)} [1]; {m(sp0)} + {m(N * (p - 1))} [1]; {m(cb)} − {m(cash)} [1] [3]'),
        lambda r: (f'Evaluate whether {c} has paid a fair price for the business.', f'Goodwill of {m(gw)} is {pc(gw / PC * 100)} of consideration; justified only if future profits/synergies exceed the premium; consider customer loyalty, staff, risk.',
                   'Uses goodwill figure [1]; future profits/synergies [1]; risks [1]; conclusion [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t5_1.add('C4', (2, 3, 4, 5), 'multi_step')(_buy_c4)
t5_1.add('C3', (4, 5), 'multi_step')(_buy_c4)


@t5_1.add('C2', (2, 3, 4), 'explain')
def t51_err(r, D):
    c = co(r); A = r.choice(PEOPLE)
    bv, fv = step(r, 60000, 200000, 1000), 0
    fv = bv + step(r, 10000, 60000, 1000)
    return {'stem': f'When {c} bought the business of {A}, the accountant recorded premises at {A}\'s book value of {m(bv)} instead of the agreed fair value of {m(fv)}. Explain the error and its effect on goodwill and on the statement of financial position.',
            'answer': f'Assets acquired must be recorded at fair value. Premises are understated by {m(fv - bv)} and goodwill is overstated by the same amount; total assets are unchanged.',
            'key': f'Fair value required [1]; premises understated {m(fv - bv)} [1]; goodwill overstated {m(fv - bv)}, total unchanged [1] [3]'}


t5_2 = topic('Calculating purchase consideration and goodwill or bargain purchase', 'calculating purchase consideration and goodwill or bargain purchase', 'purchase consideration', 'bargain purchase', 'goodwill')
fixed(t5_2, 'C1', (1, 2), [
    ('Goodwill on acquisition is calculated as', 'purchase consideration less the fair value of net assets acquired', 'IFRS 3 [1].',
     ['fair value of net assets less purchase consideration', 'purchase consideration less book value of the seller\'s capital', 'total assets acquired less cash paid']),
    ('A gain on a bargain purchase arises when', 'the fair value of net assets acquired exceeds the purchase consideration', 'Negative goodwill → gain recognised in profit after reassessment [1].',
     ['the consideration exceeds the net assets', 'shares are issued at a premium', 'goodwill is amortised']),
    ('Under IFRS 3, purchased goodwill is', 'tested for impairment annually and not amortised', 'Goodwill: annual impairment review [1].',
     ['amortised over five years', 'written off immediately to reserves', 'revalued upwards each year']),
    ('A gain on a bargain purchase is', 'recognised immediately in profit or loss', 'After reassessing values, credited to profit [1].',
     ['shown as a negative intangible asset', 'credited to share premium', 'deferred and amortised']),
])
fixed(t5_2, 'C2', (2, 3, 4), [
    ('Explain why a buyer might pay more than the fair value of the net assets of a business.', 'To obtain its goodwill: reputation, customer base, skilled staff, location, synergies and future super profits that are not recorded as separate assets.',
     'Goodwill sources [1]; future profits/synergies [1] [2]'),
    ('Explain why a seller might accept less than the fair value of its net assets.', 'The seller may need to sell quickly (forced sale, retirement, financial difficulty) or the business may be making losses, so the assets will not earn a normal return.',
     'Reason [1]; development [1] [2]'),
])


@t5_2.add('C3', (1, 2, 3, 4, 5))
def t52_pc(r, D):
    c = co(r); A = r.choice(PEOPLE)
    na = step(r, 100000, 500000, 1000)
    N = step(r, 40000, 250000, 5000); p = r.choice([1.2, 1.4, 1.5, 1.75, 2.0, 2.4])
    cash = step(r, 0, 80000, 1000)
    deb = step(r, 0, 100000, 10000) if D >= 3 else 0
    PC = round(N * p) + cash + deb
    if D >= 4 and r.random() < 0.5:
        na = PC + step(r, 2000, 30000, 1000)
    gw = PC - na
    stem = f'{c} acquires {firm(r)} from {A}. The fair value of the net assets acquired is {m(na)}. The consideration is {nm(N)} ordinary shares of $1 at ${p:.2f} each' + (f', {m(cash)} in cash' if cash else '') + (f' and {m(deb)} 7% debentures' if deb else '') + '.'
    key = f'Shares {nm(N)} × ${p:.2f} = {m(N * p)} [1]; consideration {m(PC)} [1]; {m(PC)} − {m(na)} = {m(gw)} → {"goodwill" if gw > 0 else "gain on bargain purchase"} [1]'
    if D == 1:
        opts, ans = mm(r, gw, [PC - na + cash if cash else gw + 5000, N + cash + deb - na, na - PC, gw * 2])
        return {'stem': stem + ' What is the goodwill on acquisition?' if gw > 0 else stem + ' What is the difference between consideration and net assets?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the purchase consideration and the goodwill or gain on bargain purchase.' + (' State how the result is treated in the financial statements.' if D >= 4 else '')
    tr = ' Goodwill: intangible non-current asset, tested annually for impairment.' if gw > 0 else ' Gain: credited to profit or loss after reassessing fair values.'
    return {'stem': stem + q, 'answer': f'Consideration {m(PC)}; ' + (f'goodwill {m(gw)}' if gw > 0 else f'gain on bargain purchase {m(-gw)}') + (tr if D >= 4 else ''), 'key': key + (' ; treatment [1]' if D >= 4 else ''), 'marks': 3 + (D >= 4)}


@t5_2.add('C3', (2, 3, 4, 5))
def t52_shares(r, D):
    c = co(r)
    na = step(r, 150000, 600000, 1000)
    gw = step(r, 20000, 120000, 1000)
    cash = step(r, 10000, 80000, 1000)
    p = r.choice([1.25, 1.5, 2.0, 2.5])
    sh = na + gw - cash
    N = sh / p
    if abs(N - round(N)) > 1e-9:
        sh = round(N) * p; N = round(N); gw = sh + cash - na
    N = int(round(N))
    return {'stem': f'{c} agreed to pay {m(na + gw)} for a business whose net assets have a fair value of {m(na)}. It pays {m(cash)} in cash and the balance by issuing ordinary shares of $1 at ${p:.2f} each. Calculate the goodwill, the number of shares issued and the share premium created.',
            'answer': f'Goodwill {m(gw)}; {nm(N)} shares; share premium {m(N * (p - 1))}',
            'key': f'Goodwill {m(na + gw)} − {m(na)} = {m(gw)} [1]; shares value {m(sh)} ÷ ${p:.2f} = {nm(N)} [1]; premium {nm(N)} × ${p - 1:.2f} = {m(N * (p - 1))} [1]', 'marks': 3}


@t5_2.add('C2', (2, 3, 4), 'explain')
def t52_err(r, D):
    c = co(r)
    PC = step(r, 200000, 600000, 1000); na = PC + step(r, 5000, 40000, 1000)
    return {'stem': f'{c} paid {m(PC)} for net assets with a fair value of {m(na)}. The finance director wants to show the difference as "negative goodwill" deducted from intangible assets. Explain the correct treatment.',
            'answer': f'Under IFRS 3 the fair values must first be reassessed; any remaining excess of {m(na - PC)} is a gain on bargain purchase recognised immediately in profit or loss.',
            'key': f'Reassess fair values [1]; gain on bargain purchase {m(na - PC)} [1]; to profit or loss, not intangible assets [1] [3]'}


t5_2.add('C4', (2, 3, 4, 5), 'multi_step')(_buy_c4)


t5_3 = topic('Merger of businesses: opening statement of financial position', 'merger of businesses: opening statement of financial position', 'merger', 'amalgamation')
fixed(t5_3, 'C1', (1, 2), [
    ('In a merger of two businesses to form a new company, shares in the new company are usually issued to the owners', 'in proportion to the agreed values of the businesses they contribute', 'Shares allotted on the value of net assets (plus goodwill) contributed [1].',
     ['equally regardless of value', 'in proportion to their past drawings', 'only to the larger business owner']),
    ('The opening statement of financial position of a merged company shows assets at', 'the agreed values at the date of the merger', 'New entity records assets at agreed (fair) values [1].',
     ['the higher of the two book values', 'historical cost to the original owners', 'zero until audited']),
    ('A merger differs from a takeover because', 'the combining businesses agree to join on broadly equal terms to form one entity', 'Merger: agreed combination; takeover: one acquires control of another [1].',
     ['one business is always bought for cash', 'no shares are issued', 'it is not allowed for sole traders']),
])
fixed(t5_3, 'C2', (2, 3, 4), [
    ('Explain two benefits to the owners of two small businesses of merging into one limited company.', 'Economies of scale; combined skills and resources; larger capital base and easier finance; limited liability; reduced competition.',
     'Two benefits [1 each] + explanation [1 each] [4]'),
    ('Explain why goodwill is often valued separately for each business before a merger.', 'So that owners whose business has greater earning power receive more shares; without it, shares would reflect only tangible net assets and be unfair.',
     'Fair allocation of shares [1]; reflects earning power [1] [2]'),
])


@t5_3.add('C3', (1, 2, 3, 4, 5))
def t53_alloc(r, D):
    A, B = r.sample(PEOPLE, 2)
    newco = co(r)
    naA, naB = step(r, 80000, 300000, 1000), step(r, 80000, 300000, 1000)
    gA, gB = (step(r, 10000, 60000, 1000), step(r, 10000, 60000, 1000)) if D >= 3 else (0, 0)
    p = r.choice([1, 1, 1.25, 2]) if D >= 2 else 1
    vA, vB = naA + gA, naB + gB
    nA, nB = vA / p, vB / p
    stem = (f'{A} (sole trader, net assets {m(naA)}) and {B} (sole trader, net assets {m(naB)}) merge their businesses to form {newco}.' + (f' Goodwill is valued at {m(gA)} for {A}\'s business and {m(gB)} for {B}\'s.' if gA else '')
            + f' Each receives ordinary shares of $1 in {newco}' + (f' issued at ${p:.2f}' if p != 1 else ' at par') + ' equal in value to the business contributed.')
    key = f'{A}: {m(naA)}' + (f' + {m(gA)}' if gA else '') + f' = {m(vA)} → {nm(nA)} shares [1]; {B}: {m(vB)} → {nm(nB)} shares [1]' + (f'; goodwill {m(gA)} + {m(gB)} = {m(gA + gB)} [1]' if gA else '') + (f'; share premium {m((nA + nB) * (p - 1))} [1]' if p != 1 else '')
    if D == 1:
        opts, ans = num_mcq(r, nA, [nB, (nA + nB) / 2, naA + naB, nA * 1.1], fmtf=nm)
        return {'stem': stem + f' How many shares does {A} receive?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + ' Calculate the number of shares issued to each owner' + (', and the total goodwill and share premium in the opening statement of financial position.' if gA else '.'),
            'answer': f'{A} {nm(nA)}; {B} {nm(nB)}' + (f'; goodwill {m(gA + gB)}; share premium {m((nA + nB) * (p - 1))}' if gA else ''), 'key': key, 'marks': 2 + bool(gA) + (p != 1)}


def _merge_c4(r, D):
    A, B = r.sample(PEOPLE, 2); newco = co(r)
    ncaA, ncaB = step(r, 60000, 250000, 1000), step(r, 60000, 250000, 1000)
    caA, caB = step(r, 20000, 80000, 1000), step(r, 20000, 80000, 1000)
    clA, clB = step(r, 10000, 40000, 1000), step(r, 10000, 40000, 1000)
    gA, gB = step(r, 10000, 60000, 1000), step(r, 10000, 60000, 1000)
    adjA = step(r, -15000, 30000, 1000)
    vA = ncaA + adjA + caA - clA + gA; vB = ncaB + caB - clB + gB
    tot = vA + vB
    intro = (f'{firm(r)} (owner {A}) and {firm(r)} (owner {B}) merge to form {newco} on 1 January. Agreed values: {A} — non-current assets {m(ncaA)} (to be revalued by {"+" if adjA >= 0 else "−"}{m(abs(adjA))}), current assets {m(caA)}, current liabilities {m(clA)}, goodwill {m(gA)}; '
             f'{B} — non-current assets {m(ncaB)}, current assets {m(caB)}, current liabilities {m(clB)}, goodwill {m(gB)}. Ordinary shares of $1 are issued at par to each owner equal to the value of the business transferred.')
    parts = [
        lambda r: ('Calculate the number of shares issued to each owner.', f'{A} {nm(vA)}; {B} {nm(vB)}', f'{A} {m(ncaA + adjA)} + {m(caA)} − {m(clA)} + {m(gA)} = {m(vA)} [2]; {B} {m(vB)} [1] [3]'),
        lambda r: (f'Prepare the opening statement of financial position of {newco}.', f'Goodwill {m(gA + gB)}; NCA {m(ncaA + adjA + ncaB)}; CA {m(caA + caB)}; CL {m(clA + clB)}; share capital {m(tot)}',
                   f'Goodwill [1]; NCA [1]; CA [1]; CL [1]; equity = net assets {m(tot)} [1] [5]'),
        lambda r: (f'Calculate the percentage of {newco} owned by {A}.', pc(vA / tot * 100), f'{m(vA)} / {m(tot)} × 100 [2]'),
        lambda r: (f'Advise {B} whether to accept the terms of the merger.', f'{B} owns {pc(vB / tot * 100)}; consider control, share of future profits, goodwill valuation fairness and limited liability; recommend.',
                   'Uses ownership share [1]; two considerations [2]; recommendation [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t5_3.add('C4', (2, 3, 4, 5), 'multi_step')(_merge_c4)
t5_3.add('C3', (4, 5), 'multi_step')(_merge_c4)
t5_1.add('C4', (3, 4, 5), 'multi_step')(_merge_c4)


@t5_3.add('C2', (2, 3, 4), 'explain')
def t53_err(r, D):
    A, B = r.sample(PEOPLE, 2)
    vA, vB = step(r, 100000, 300000, 10000), step(r, 100000, 300000, 10000)
    tot = vA + vB
    return {'stem': f'{A}\'s business (valued at {m(vA)}) and {B}\'s business (valued at {m(vB)}) merged. The adviser proposed issuing {nm(tot // 2)} shares of $1 to each owner. Explain why this may be unfair and calculate a fair allocation.',
            'answer': f'Shares should reflect the value each owner contributes: {A} {nm(vA)} shares, {B} {nm(vB)} shares. Equal allocation transfers value from the owner of the larger business.',
            'key': f'Unequal contributions [1]; {A} {nm(vA)} [1]; {B} {nm(vB)} [1] [3]'}


CHAPTERS[5] = [t5_1, t5_2, t5_3]


# ===================================================================== 6 Consignment and joint ventures
GOODS = [('solar lanterns', 'units', [20, 25, 30, 40]), ('rolls of batik cloth', 'rolls', [20, 25, 30, 45]), ('cases of olive oil', 'cases', [30, 40, 45, 60]),
         ('mountain bicycles', 'bicycles', [120, 150, 180, 240]), ('bags of coffee beans', 'bags', [25, 40, 50, 60]), ('carved teak chairs', 'chairs', [45, 60, 80, 120]),
         ('cartons of tea', 'cartons', [20, 25, 30, 40]), ('water pumps', 'pumps', [80, 120, 150, 200]), ('leather jackets', 'jackets', [40, 50, 60, 80]), ('ceramic vases', 'vases', [20, 30, 45, 50])]


def _consign(r, D):
    g, u, cs = r.choice(GOODS)
    n = r.choice([100, 200, 250, 400, 500, 800, 1000])
    c = r.choice(cs)
    k = n * r.choice([3, 5, 6, 7, 8, 9]) // 10
    p = round(c * r.choice([1.4, 1.5, 1.6, 1.75, 2.0]))
    F = step(r, 500, 6000, 100); ins = step(r, 200, 2000, 100)
    duty = step(r, 300, 4000, 100) if D >= 2 else 0
    sell = step(r, 200, 3000, 100)
    com = r.choice([5, 8, 10, 12])
    dc = r.choice([0, 2, 3]) if D >= 3 else 0
    A = r.choice(PEOPLE); B = r.choice([x for x in PEOPLE if x != A])
    goods = n * c
    nonrec = F + ins + duty
    unsold = n - k
    inv_val = int(_hu(Fr(unsold, n) * (goods + nonrec)))
    sales = k * p
    commission = int(_hu(sales * (com + dc) / 100))
    profit = sales + inv_val - goods - nonrec - sell - commission
    remit = sales - duty - sell - commission
    return dict(g=g, u=u, n=n, c=c, k=k, p=p, F=F, ins=ins, duty=duty, sell=sell, com=com, dc=dc, A=A, B=B, goods=goods, nonrec=nonrec, unsold=unsold, inv=inv_val, sales=sales, commission=commission, profit=profit, remit=remit)


def _cons_text(r, x):
    city_ = r.choice(['Nairobi', 'Dubai', 'Singapore', 'Lisbon', 'Toronto', 'Kuala Lumpur', 'Cape Town', 'Doha', 'Auckland', 'Madrid'])
    t = (f'{x["A"]} of {city_} sent {nm(x["n"])} {x["g"]} costing ${x["c"]} each on consignment to {x["B"]}. {x["A"]} paid freight of {m(x["F"])} and insurance of {m(x["ins"])}. '
         + (f'{x["B"]} paid import duty of {m(x["duty"])} and ' if x['duty'] else f'{x["B"]} paid ') + f'selling expenses of {m(x["sell"])}. {x["B"]} sold {x["k"]} {x["u"]} at ${x["p"]} each and is entitled to commission of {x["com"]}% on sales'
         + (f' plus a del credere commission of {x["dc"]}%' if x['dc'] else '') + '.')
    return t


t6_1 = topic('Consignment accounts in the books of consignor and consignee', 'consignment accounts in the books of consignor and consignee', 'consignment', 'consignor', 'consignee')
fixed(t6_1, 'C1', (1, 2), [
    ('In a consignment, the consignor is', 'the owner who sends the goods to an agent to sell', 'Consignor = principal/owner; consignee = agent [1].',
     ['the agent who sells the goods', 'the final customer', 'the carrier who transports the goods']),
    ('Goods sent on consignment remain the property of', 'the consignor until they are sold', 'Ownership stays with the consignor; not a sale [1].',
     ['the consignee from the date of dispatch', 'the shipping company', 'the customer who orders them']),
    ('In the consignor\'s books, goods sent on consignment are credited to', 'a goods sent on consignment account (transferred to purchases/trading account)', 'Dr Consignment to [agent], Cr Goods sent on consignment [1].',
     ['sales', 'the consignee\'s personal account', 'inventory']),
    ('In the consignee\'s books, the consignor appears as', 'a personal account (the consignor is a creditor for sales proceeds less expenses and commission)', 'Consignee records sales, expenses and commission in consignor\'s account [1].',
     ['a consignment account showing profit', 'an inventory account', 'a sales account']),
    ('Commission earned by the consignee is debited in the consignor\'s books to the', 'consignment account', 'Commission is an expense of the consignment [1].',
     ['consignee\'s capital account', 'sales account', 'goods sent on consignment account']),
])
fixed(t6_1, 'C2', (2, 3, 4), [
    ('Explain why goods sent on consignment are not recorded as sales by the consignor.', 'Ownership does not pass to the consignee; the consignee is only an agent. A sale occurs when the consignee sells to a third party.',
     'No transfer of ownership [1]; sale when agent sells [1] [2]'),
    ('Explain the purpose of a proforma invoice in a consignment.', 'It informs the consignee of the goods sent and the expected selling price; it is not a demand for payment and no entry is made in the consignee\'s ledger.',
     'Information/price guide [1]; not a sale/no ledger entry [1] [2]'),
    ('Distinguish between a consignment and an ordinary credit sale.', 'In a consignment, ownership and risk stay with the consignor and the agent earns commission; in a credit sale ownership passes to the buyer, who owes the price.',
     'Ownership/risk [1]; agent commission vs buyer debt [1] [2]'),
])


@t6_1.add('C3', (1, 2, 3, 4, 5))
def t61_profit(r, D):
    x = _consign(r, D)
    stem = _cons_text(r, x)
    key = (f'Sales {x["k"]} × ${x["p"]} = {m(x["sales"])} [1]; commission {x["com"] + x["dc"]}% = {m(x["commission"])} [1]; unsold inventory {x["unsold"]}/{x["n"]} × ({m(x["goods"])} + {m(x["nonrec"])}) = {m(x["inv"])} [1]; '
           f'profit = {m(x["sales"])} + {m(x["inv"])} − {m(x["goods"])} − {m(x["nonrec"])} − {m(x["sell"])} − {m(x["commission"])} = {m(x["profit"])} [1]')
    if D == 1:
        opts, ans = mm(r, x['commission'], [x['sales'] * 0.1 if x['com'] != 10 else x['sales'] * 0.05, x['n'] * x['p'] * x['com'] / 100, x['commission'] * 2, x['goods'] * x['com'] / 100])
        return {'stem': stem + f' What is the commission due to {x["B"]}?', 'options': opts, 'answer': ans, 'key': key}
    if D == 2:
        return {'stem': stem + f' Calculate the value of the unsold inventory and the profit on consignment in the books of {x["A"]}.', 'answer': f'Unsold inventory {m(x["inv"])}; profit {m(x["profit"])}', 'key': key, 'marks': 4}
    return {'stem': stem + f' Prepare the consignment account in the books of {x["A"]}, showing the profit on consignment.', 'answer': f'Profit on consignment {m(x["profit"])} (unsold inventory c/d {m(x["inv"])})', 'key': key + ' ; layout with c/d inventory [1]', 'marks': 5, 'type': 'multi_step'}


@t6_1.add('C3', (2, 3, 4))
def t61_consignee(r, D):
    x = _consign(r, D)
    stem = _cons_text(r, x) + f' {x["B"]} remits the balance due by bank transfer. Prepare {x["A"]}\'s account in the books of {x["B"]} and calculate the amount remitted.'
    return {'stem': stem, 'answer': f'Amount remitted {m(x["remit"])}',
            'key': f'Cr sales {m(x["sales"])} [1]; Dr expenses paid' + (f' duty {m(x["duty"])} +' if x['duty'] else '') + f' selling {m(x["sell"])} [1]; Dr commission {m(x["commission"])} [1]; balance remitted {m(x["remit"])} [1]', 'marks': 4}


def _cons_c4(r, D):
    x = _consign(r, D)
    intro = _cons_text(r, x)
    parts = [
        lambda r: ('Calculate the value of the unsold inventory at the end of the period.', m(x['inv']), f'{x["unsold"]}/{x["n"]} × ({m(x["goods"])} + freight {m(x["F"])} + insurance {m(x["ins"])}' + (f' + duty {m(x["duty"])}' if x['duty'] else '') + f') = {m(x["inv"])} [2]'),
        lambda r: (f'Calculate the commission due to {x["B"]}.', m(x['commission']), f'{x["com"] + x["dc"]}% × {m(x["sales"])} [1]'),
        lambda r: (f'Prepare the consignment account in the books of {x["A"]}.', f'Profit {m(x["profit"])}', f'Goods {m(x["goods"])}, consignor\'s expenses, consignee\'s expenses, commission on debit [2]; sales and inventory c/d on credit [1]; profit {m(x["profit"])} [1] [4]'),
        lambda r: (f'Calculate the amount {x["B"]} should remit.', m(x['remit']), f'{m(x["sales"])} − expenses {m(x["duty"] + x["sell"])} − commission {m(x["commission"])} = {m(x["remit"])} [2]'),
        lambda r: (f'Explain why selling expenses are not included in the value of unsold inventory.', 'Selling expenses relate to goods already sold; only costs of bringing the goods to their present location and condition (IAS 2) are included.', '[2]'),
        lambda r: (f'Advise {x["A"]} whether to offer a del credere commission.', 'It costs extra commission but transfers the risk of bad debts on credit sales to the agent and encourages careful credit control.', 'Cost [1]; benefit: bad debts borne by agent [1]; recommendation [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t6_1.add('C4', (2, 3, 4, 5), 'multi_step')(_cons_c4)
t6_1.add('C3', (4, 5), 'multi_step')(_cons_c4)


@t6_1.add('C2', (2, 3, 4), 'explain')
def t61_err(r, D):
    x = _consign(r, D)
    return {'stem': f'{x["A"]} sent {x["n"]} {x["g"]} costing {m(x["goods"])} to an agent, {x["B"]}, on consignment, and the bookkeeper recorded the full amount as a credit sale to {x["B"]}. Explain the error and its effect on revenue and on inventory.',
            'answer': f'Goods on consignment are not sold until the agent sells them; revenue is overstated (by the invoiced value) and inventory understated — unsold goods should remain in {x["A"]}\'s inventory at cost plus non-recurring expenses.',
            'key': 'Ownership remains with consignor [1]; revenue/receivables overstated [1]; inventory of unsold goods omitted [1] [3]'}


t6_2 = topic('Valuing unsold consignment inventory and commission', 'valuing unsold consignment inventory and commission', 'unsold inventory', 'del credere', 'commission')
fixed(t6_2, 'C1', (1, 2), [
    ('Which expense is included when valuing unsold consignment inventory?', 'Freight to the consignee\'s premises', 'Non-recurring costs to bring goods to location (freight, insurance in transit, import duty) included [1].',
     ['The consignee\'s selling commission', 'Advertising by the consignee', 'Bad debts on credit sales']),
    ('A del credere commission is paid to the consignee in return for', 'bearing any bad debts on credit sales', 'Del credere agent guarantees payment by credit customers [1].',
     ['selling above the proforma price', 'paying the freight', 'storing the goods free of charge']),
    ('Bad debts on consignment sales where the agent receives del credere commission are borne by', 'the consignee', 'Del credere: agent bears credit risk [1].',
     ['the consignor', 'the customers\' bank', 'both equally']),
    ('Recurring expenses such as the consignee\'s selling costs are', 'charged against the consignment profit and excluded from unsold inventory', 'Selling costs relate to sold goods [1].',
     ['added to the value of unsold inventory', 'capitalised as non-current assets', 'charged to the consignee only']),
])
fixed(t6_2, 'C2', (2, 3, 4), [
    ('Explain why a proportion of freight and insurance is included in the valuation of unsold consignment inventory.', 'These costs were incurred to bring all the goods to the consignee\'s location; under IAS 2 such costs form part of the cost of inventory, so the unsold goods carry their share.',
     'Costs to bring goods to present location [1]; IAS 2 / matching [1] [2]'),
    ('Explain why a consignee might demand a del credere commission.', 'It compensates the agent for accepting the risk of bad debts on credit sales, which would otherwise fall on the consignor.',
     'Compensation for bad debt risk [1]; credit sales [1] [2]'),
])


@t6_2.add('C3', (1, 2, 3, 4, 5))
def t62_inv(r, D):
    x = _consign(r, D)
    loss = r.choice([0, 0, 5, 10, 20]) if D >= 4 else 0
    lost = x['n'] * loss // 100 if loss else 0
    stem = _cons_text(r, x)
    unsold = x['unsold'] - lost
    if unsold <= 0:
        lost, unsold = 0, x['unsold']
    if lost:
        stem += f' During transit {lost} {x["u"]} were lost (a normal loss).'
        good = x['n'] - lost
        inv = Fr(unsold, good) * (x['goods'] + x['nonrec'])
        key = f'Normal loss spreads cost over {good} {x["u"]} [1]; unsold = {x["n"]} − {lost} − {x["k"]} = {unsold} [1]; ({m(x["goods"])} + {m(x["nonrec"])}) × {unsold}/{good} = {m(inv)} [1]'
    else:
        inv = x['inv']
        key = f'Cost of goods {m(x["goods"])} + freight {m(x["F"])} + insurance {m(x["ins"])}' + (f' + duty {m(x["duty"])}' if x['duty'] else '') + f' = {m(x["goods"] + x["nonrec"])} [1]; × {unsold}/{x["n"]} = {m(inv)} [1]; selling expenses excluded [1]'
    if D == 1:
        opts, ans = mm(r, inv, [unsold * x['c'], Fr(unsold, x['n']) * (x['goods'] + x['nonrec'] + x['sell']), unsold * x['p'], inv + x['F']])
        return {'stem': stem + ' What is the value of the unsold inventory?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + ' Calculate the value of the unsold inventory held by the consignee.', 'answer': m(inv), 'key': key, 'marks': 3}


@t6_2.add('C3', (2, 3, 4, 5))
def t62_com(r, D):
    B = r.choice(PEOPLE)
    sales = step(r, 20000, 200000, 1000); cr = r.choice([40, 50, 60, 75])
    com, dc = r.choice([5, 8, 10]), r.choice([2, 2.5, 3])
    bad = step(r, 200, int(sales * cr / 100 * 0.05), 100)
    over = r.choice([0, 10, 15, 20]) if D >= 4 else 0
    ppx = step(r, 15000, int(sales * 0.9), 1000) if over else 0
    base_c = sales * com / 100
    over_c = (sales - ppx) * over / 100 if over else 0
    del_c = sales * dc / 100
    tot = base_c + del_c + over_c
    stem = (f'{B} sells goods on consignment and earns {com}% commission on all sales plus a del credere commission of {dc}% on all sales'
            + (f', and {over}% on sales above the proforma value of {m(ppx)}' if over else '') + f'. Sales were {m(sales)}, of which {cr}% were on credit; one credit customer owing {m(bad)} became insolvent. Calculate the total commission and state who bears the bad debt.')
    return {'stem': stem, 'answer': f'Commission {m(tot)}; the bad debt of {m(bad)} is borne by {B} (del credere agent)',
            'key': f'{com}% × {m(sales)} = {m(base_c)} [1]; del credere {dc}% = {m(del_c)} [1]' + (f'; over-proforma {over}% × {m(sales - ppx)} = {m(over_c)} [1]' if over else '') + f'; total {m(tot)} [1]; bad debt borne by consignee [1]', 'marks': 4 + bool(over)}


t6_2.add('C4', (2, 3, 4, 5), 'multi_step')(_cons_c4)


@t6_2.add('C2', (2, 3, 4), 'explain')
def t62_err(r, D):
    x = _consign(r, D)
    wrong = Fr(x['unsold'], x['n']) * (x['goods'] + x['nonrec'] + x['sell'] + x['commission'])
    return {'stem': f'{x["A"]} consigned {x["n"]} {x["g"]} costing {m(x["goods"])}; freight and insurance were {m(x["F"] + x["ins"])}' + (f', import duty {m(x["duty"])}' if x['duty'] else '') + f', selling expenses {m(x["sell"])} and commission {m(x["commission"])}. {x["unsold"]} {x["u"]} were unsold. A trainee valued them at {m(wrong)}. Explain the error and calculate the correct value.',
            'answer': f'Selling expenses and commission relate to goods sold and must be excluded. Correct value {x["unsold"]}/{x["n"]} × {m(x["goods"] + x["nonrec"])} = {m(x["inv"])}.',
            'key': f'Exclude recurring/selling costs and commission [1]; include non-recurring costs [1]; correct value {m(x["inv"])} [1] [3]'}


t6_3 = topic('Joint venture accounts and memorandum joint venture account', 'joint venture accounts and memorandum joint venture account', 'joint venture', 'memorandum joint venture')
fixed(t6_3, 'C1', (1, 2), [
    ('A memorandum joint venture account is used to', 'calculate the total profit or loss of the joint venture', 'Combines all venturers\' transactions to find profit; not part of double entry [1].',
     ['record the cash paid between venturers', 'replace each venturer\'s ledger', 'show the capital of each venturer']),
    ('In each venturer\'s own books, the joint venture account records', 'only the transactions carried out by that venturer, plus his share of profit', 'Own JV account: own expenses, own sales, own share of profit [1].',
     ['the transactions of all venturers', 'only the final settlement', 'only the sales of the venture']),
    ('A debit balance on a venturer\'s joint venture account after including his share of profit means that', 'the other venturer owes him money', 'Dr balance: he has spent more than received + profit share → due to him [1].',
     ['he owes the other venturer money', 'the venture has made a loss', 'the venture is still continuing']),
    ('A joint venture differs from a partnership because it', 'is formed for a specific short-term project and ends when it is completed', 'JV: temporary, specific purpose [1].',
     ['always has unlimited liability', 'must register as a company', 'has no profit-sharing ratio']),
])
fixed(t6_3, 'C2', (2, 3, 4), [
    ('Explain why the memorandum joint venture account is not part of the double-entry system.', 'Each venturer records only his own transactions in his own books; the memorandum account merely combines the figures to calculate profit, so it is prepared outside the ledgers.',
     'Each venturer keeps own records [1]; memorandum combines for profit only [1] [2]'),
    ('Explain two advantages of a joint venture for two businesses.', 'Shares risk and cost of a one-off project; combines expertise or resources; no permanent commitment; access to new markets.',
     'Two advantages [1 each] + explanation [1 each] [4]'),
])


@t6_3.add('C3', (1, 2, 3, 4, 5))
def t63_jv(r, D):
    A, B = r.sample(PEOPLE, 2)
    proj = r.choice(['buy and resell a shipment of timber', 'organise a trade fair in Dubai', 'build and sell two houses', 'import and sell a batch of laptops', 'stage a music festival', 'export dried fruit to Europe'])
    ratio = r.choice([(1, 1), (3, 2), (2, 1), (3, 1)])
    s = sum(ratio)
    ea, eb = step(r, 10000, 80000, 100), step(r, 5000, 60000, 100)
    sa, sb = step(r, 0, 70000, 100), step(r, 20000, 120000, 100)
    tot_e, tot_s = ea + eb, sa + sb
    if tot_s <= tot_e:
        sb += tot_e - tot_s + step(r, 3000, 20000, 100); tot_s = sa + sb
    fix = (-(tot_s - tot_e)) % (100 * s)
    sb += fix; tot_s += fix
    profit = tot_s - tot_e
    pa, pb = profit * Fr(ratio[0], s), profit * Fr(ratio[1], s)
    balA = ea + pa - sa
    stem = f'{A} and {B} agreed to {proj}, sharing profits {rs(ratio)}. {A} paid expenses of {m(ea)}' + (f' and received sales of {m(sa)}' if sa else '') + f'; {B} paid expenses of {m(eb)} and received sales of {m(sb)}.'
    key = f'Memorandum JV: sales {m(tot_s)} − expenses {m(tot_e)} = profit {m(profit)} [1]; shares {A} {m(pa)}, {B} {m(pb)} [1]; {A}\'s JV account: {m(ea)} + {m(pa)} − {m(sa)} = {m(abs(balA))} {"Dr (due to " + A + ")" if balA > 0 else "Cr (due from " + A + ")"} [1]'
    who = f'{B} pays {A} {m(balA)}' if balA > 0 else f'{A} pays {B} {m(-balA)}'
    if D == 1:
        opts, ans = mm(r, profit, [tot_s, profit / 2, tot_e - sa, profit + ea // 2])
        return {'stem': stem + ' What is the profit on the joint venture?', 'options': opts, 'answer': ans, 'key': key}
    if D == 2:
        return {'stem': stem + ' Calculate the profit on the joint venture and each venturer\'s share.', 'answer': f'Profit {m(profit)}: {A} {m(pa)}, {B} {m(pb)}', 'key': key, 'marks': 2}
    return {'stem': stem + f' Prepare the memorandum joint venture account and the joint venture account in {A}\'s books, showing the final settlement.', 'answer': f'Profit {m(profit)}; settlement: {who}', 'key': key + f'; settlement {who} [1]', 'marks': 4, 'type': 'multi_step'}


def _jv_c4(r, D):
    A, B = r.sample(PEOPLE, 2)
    ratio = r.choice([(1, 1), (3, 2), (2, 1)])
    s = sum(ratio)
    goods = step(r, 20000, 90000, 500); trans = step(r, 1000, 6000, 100); adv = step(r, 500, 4000, 100)
    sa, sb = step(r, 10000, 60000, 500), step(r, 20000, 90000, 500)
    unsold_cost = step(r, 1000, 8000, 100)
    take = unsold_cost - step(r, 0, 800, 100)
    tot_s = sa + sb + take
    tot_e = goods + trans + adv
    if tot_s <= tot_e:
        sb += tot_e - tot_s + step(r, 5000, 15000, 100); tot_s = sa + sb + take
    fix = (-(tot_s - tot_e)) % (100 * s)
    sb += fix; tot_s += fix
    profit = tot_s - tot_e
    pa, pb = profit * Fr(ratio[0], s), profit * Fr(ratio[1], s)
    balA = goods + trans + pa - sa - take
    intro = (f'{A} and {B} entered a joint venture to sell {r.choice(["handmade rugs", "used cars", "mobile phones", "cocoa", "furniture"])}, sharing profits {rs(ratio)}. {A} bought goods for {m(goods)} and paid transport of {m(trans)}; '
             f'{B} paid advertising of {m(adv)}. {A} received sales of {m(sa)} and {B} received sales of {m(sb)}. At the end, {A} took the remaining goods for his own use at an agreed value of {m(take)}.')
    who = f'{B} pays {A} {m(balA)}' if balA > 0 else f'{A} pays {B} {m(-balA)}'
    parts = [
        lambda r: ('Prepare the memorandum joint venture account showing the profit.', f'Profit {m(profit)}', f'Debits {m(goods)}, {m(trans)}, {m(adv)} [1]; credits sales {m(sa + sb)} and goods taken {m(take)} [1]; profit {m(profit)} split {m(pa)}/{m(pb)} [1] [3]'),
        lambda r: (f'Prepare the joint venture with {B} account in {A}\'s books.', f'Balance {m(abs(balA))}; {who}', f'Dr goods, transport, profit share {m(pa)}; Cr sales {m(sa)}, goods taken {m(take)} [2]; balance {m(abs(balA))} [1] [3]'),
        lambda r: ('State the amount and direction of the final settlement.', who, f'[1]'),
        lambda r: (f'Explain how the goods taken by {A} are treated.', f'Treated as a sale to {A}: credit the JV accounts with {m(take)}, so the venture is credited and {A}\'s balance due falls.', '[2]'),
        lambda r: ('Discuss one advantage and one disadvantage of a joint venture compared with forming a partnership.', 'Advantage: temporary, limited to one project, no long-term commitment. Disadvantage: possible disputes, no separate entity; each venturer exposed to the other\'s actions.', '[3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t6_3.add('C4', (2, 3, 4, 5), 'multi_step')(_jv_c4)
t6_3.add('C3', (4, 5), 'multi_step')(_jv_c4)


@t6_3.add('C2', (2, 3, 4), 'explain')
def t63_err(r, D):
    A, B = r.sample(PEOPLE, 2)
    ea, sb = step(r, 5000, 40000, 100), step(r, 10000, 60000, 100)
    return {'stem': f'In a joint venture with {B}, {A} paid expenses of {m(ea)} and {B} received all the sales of {m(sb)}. {A} recorded both the expenses and {B}\'s sales in his own joint venture account and treated the balance as profit. Explain the error.',
            'answer': f'{A}\'s joint venture account should record only {A}\'s own transactions (expenses {m(ea)}) and his share of profit; {B}\'s sales belong in the memorandum JV account, which is used to calculate profit.',
            'key': 'Own transactions only [1]; profit from memorandum account [1]; balance represents amount due, not profit [1] [3]'}


CHAPTERS[6] = [t6_1, t6_2, t6_3]


# ===================================================================== 7 Computerised accounting systems
t7_1 = topic('Features of computerised accounting systems and integrated ledgers', 'features of computerised accounting systems and integrated ledgers', 'computerised accounting', 'integrated ledgers')
fixed(t7_1, 'C1', (1, 2), [
    ('In an integrated computerised accounting system, entering a credit sales invoice once will', 'update the sales ledger, the general ledger and inventory records automatically', 'Single entry posts to all linked ledgers [1].',
     ['update only the sales day book', 'require separate entries in each ledger', 'update the purchases ledger']),
    ('Which report can a computerised accounting system produce instantly from the sales ledger?', 'An aged receivables analysis', 'Aged analysis shows how long each debt has been outstanding [1].',
     ['A cash budget for next year', 'The auditor\'s report', 'The directors\' report']),
    ('A trial balance produced by a computerised system will always balance because', 'the software posts equal debits and credits for every transaction', 'Double entry enforced automatically [1].',
     ['the computer cannot make errors of any kind', 'the auditor checks every entry', 'there is no need for a suspense account in manual systems']),
    ('Which error can still occur in a computerised accounting system?', 'An error of principle, such as posting a non-current asset purchase to purchases', 'Software cannot judge classification; GIGO [1].',
     ['A trial balance that does not agree', 'An arithmetical error in totalling a ledger', 'A single-sided entry']),
    ('A "nominal ledger" in an accounting package is another name for the', 'general ledger', 'Nominal/general ledger holds income, expense, asset, liability accounts [1].',
     ['sales ledger', 'purchases ledger', 'cash book only']),
])
fixed(t7_1, 'C2', (2, 3, 4), [
    ('Explain what is meant by an integrated accounting system.', 'One in which the sales, purchases, inventory, payroll and general ledgers are linked, so a single entry updates all the relevant records and reports.',
     'Linked modules [1]; single entry updates all [1] [2]'),
    ('Explain why control accounts are still useful in a computerised system.', 'They are produced automatically and give totals for receivables/payables for the financial statements and management; they help check that module totals agree with the general ledger after interfaces or imports.',
     'Totals for statements/management [1]; check between modules/data imports [1] [2]'),
    ('Explain the meaning of "garbage in, garbage out" in computerised accounting.', 'The output is only as accurate as the data entered; if wrong figures or codes are input, the reports will be wrong even though the processing is accurate.',
     'Output depends on input [1]; example [1] [2]'),
])


@t7_1.add('C3', (1, 2, 3, 4, 5))
def t71_ctrl(r, D):
    c = co(r)
    ob = step(r, 20000, 120000, 100); cs = step(r, 50000, 300000, 100); rc = step(r, 40000, int(cs * 0.95), 100)
    rt = step(r, 500, 8000, 100); dsc = step(r, 0, 3000, 50) if D >= 2 else 0
    ir = step(r, 0, 4000, 50) if D >= 3 else 0
    contra = step(r, 0, 3000, 50) if D >= 4 else 0
    cl = ob + cs - rc - rt - dsc - ir - contra
    stem = (f'The accounting software of {c} produces the trade receivables control account automatically from the sales ledger. For the month: opening balance {m(ob)}, credit sales {m(cs)}, receipts from customers {m(rc)}, sales returns {m(rt)}'
            + (f', discounts allowed {m(dsc)}' if dsc else '') + (f', irrecoverable debts written off {m(ir)}' if ir else '') + (f', contra with purchases ledger {m(contra)}' if contra else '') + '.')
    key = f'{m(ob)} + {m(cs)} − {m(rc)} − {m(rt)}' + (f' − {m(dsc)}' if dsc else '') + (f' − {m(ir)}' if ir else '') + (f' − {m(contra)}' if contra else '') + f' = {m(cl)} [2]'
    if D == 1:
        opts, ans = mm(r, cl, [cl + 2 * rt, ob + cs + rc - rt, cl - ob, cl + rt])
        return {'stem': stem + ' What is the closing balance on the control account?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the closing balance the system will report.'
    if D >= 3:
        sl = cl + step(r, 100, 2000, 50)
        q = f' The total of the individual customer balances is {m(sl)}. Calculate the control account balance and suggest one reason for the difference, given that the software posts both automatically.'
        return {'stem': stem + q, 'answer': f'Control {m(cl)}; difference {m(sl - cl)}; e.g. a journal (irrecoverable debt or contra) posted to the general ledger only, or a data import to one module',
                'key': key + f'; difference {m(sl - cl)} [1]; plausible reason (manual journal to GL only / import error / input to wrong account) [1]', 'marks': 4}
    return {'stem': stem + q, 'answer': m(cl), 'key': key, 'marks': 2}


@t7_1.add('C3', (2, 3, 4))
def t71_post(r, D):
    c = co(r); cust = firm(r)
    net = step(r, 1000, 20000, 100); tax = r.choice([5, 10, 15, 16, 20]); inv_cost = round(net * r.choice([0.55, 0.6, 0.7]))
    g = net * tax / 100
    return {'stem': f'{c} uses integrated accounting software with perpetual inventory. A clerk enters one credit sales invoice to {cust}: goods {m(net)} plus sales tax at {tax}%; the goods cost {m(inv_cost)}. State the double entries the software will post in the general ledger and the subsidiary ledger affected.',
            'answer': f'Dr trade receivables (control) {m(net + g)}; Cr sales revenue {m(net)}; Cr sales tax payable {m(g)}; Dr cost of sales {m(inv_cost)}, Cr inventory {m(inv_cost)}; {cust}\'s account in the sales ledger debited {m(net + g)}.',
            'key': f'Receivables {m(net + g)} [1]; sales {m(net)} and tax {m(g)} [1]; cost of sales/inventory {m(inv_cost)} [1]; sales ledger customer account [1]', 'marks': 4}


@t7_1.add('C2', (2, 3, 4), 'explain')
def t71_err(r, D):
    c = co(r)
    v = step(r, 2000, 50000, 100)
    err = r.choice([(f'a new delivery van costing {m(v)} was coded to "Motor expenses"', 'error of principle: capital expenditure posted as revenue expenditure; profit understated and non-current assets understated by ' + m(v)),
                    (f'a receipt of {m(v)} from customer K. Osei was posted to the account of K. Owusu', 'error of commission: wrong customer account; control total unaffected but individual balances wrong'),
                    (f'an invoice for {m(v)} was keyed in as {m(v * 10)}', f'error of original entry: both sides overstated by {m(v * 9)}'),
                    (f'a purchase invoice for {m(v)} was never entered', f'error of omission: purchases and payables understated by {m(v)}')])
    return {'stem': f'The finance manager of {c} says, "Our accounting software always produces a balanced trial balance, so our accounts must be correct." The auditor found that {err[0]}. Explain why the manager is wrong, referring to this error.',
            'answer': f'Software enforces double entry, so the trial balance agrees, but it cannot detect errors that do not affect the balance: {err[1]}.',
            'key': 'Balanced TB only proves equal debits/credits [1]; names the type of error [1]; effect on accounts [1] [3]'}


t7_2 = topic('Advantages and disadvantages of computerised systems', 'advantages and disadvantages of computerised systems', 'advantages', 'disadvantages')
fixed(t7_2, 'C1', (1, 2), [
    ('Which is an advantage of a computerised accounting system over a manual system?', 'Reports such as aged receivables can be produced quickly and up to date', 'Speed and up-to-date information [1].',
     ['No staff training is needed', 'Errors of principle are eliminated', 'It costs nothing to set up']),
    ('Which is a disadvantage of a computerised accounting system?', 'Data may be lost or corrupted by system failure or viruses', 'Risk of data loss, hacking, set-up costs, training [1].',
     ['Calculations are faster', 'Ledgers are updated automatically', 'Fewer arithmetical errors occur']),
    ('Staff resistance to a new computerised system is best reduced by', 'consulting staff and providing training before implementation', 'Change management: consultation and training [1].',
     ['installing the system without notice', 'reducing staff wages', 'running the manual system only']),
    ('Which is a cost of computerisation that a small business often underestimates?', 'Staff training and disruption during changeover', 'Hidden costs: training, data conversion, lost productivity [1].',
     ['The cost of paper ledgers', 'The cost of calculators', 'Auditors\' fees for manual systems']),
    ('Cloud-based accounting software allows', 'authorised users to access up-to-date records from any location', 'Remote access, automatic backups, subscription cost [1].',
     ['only one user to work at a time in one office', 'the trial balance to disagree', 'data to be kept only on paper']),
    ('A computerised system reduces which type of error most?', 'Arithmetical and transposition errors in totalling and posting', 'Automatic posting and totalling [1].',
     ['Errors of principle', 'Errors of omission of source documents', 'Fraud by authorised users']),
])
fixed(t7_2, 'C2', (2, 3, 4), [
    ('Explain two advantages of a computerised accounting system for management decision-making.', 'Up-to-date information (e.g. daily cash position, aged receivables) supports quick decisions; reports can be customised and analysed (budgets vs actual, product profitability).',
     'Two advantages [1 each] + explanation [1 each] [4]'),
    ('Explain two disadvantages for a small business of changing from a manual to a computerised accounting system.', 'High initial cost of hardware/software and training; disruption during changeover and risk of data loss; reliance on IT skills and security threats.',
     'Two disadvantages [1 each] + explanation [1 each] [4]'),
    ('Explain why a business might run its manual and computerised systems in parallel for a period.', 'To check the new system produces the same results and to have a fallback if it fails, although it doubles the workload.',
     'Comparison/verification [1]; fallback [1]; drawback cost/time [1] [3]'),
])


@t7_2.add('C3', (1, 2, 3, 4, 5))
def t72_cb(r, D):
    c = co(r)
    setup = step(r, 8000, 60000, 500); lic = step(r, 1000, 8000, 100); hrs = step(r, 5, 30, 1); rate = r.choice([12, 15, 18, 20, 25])
    wks = r.choice([48, 50, 52])
    saving = hrs * rate * wks
    other = step(r, 0, 6000, 100) if D >= 3 else 0
    net = saving + other - lic
    if net <= 0:
        hrs += 20; saving = hrs * rate * wks; net = saving + other - lic
    pb = setup / net
    stem = (f'{c} is considering accounting software costing {m(setup)} to install plus an annual licence of {m(lic)}. It will save {hrs} hours of clerical time per week at ${rate} per hour for {wks} weeks a year'
            + (f' and reduce irrecoverable debts by {m(other)} a year through better credit control' if other else '') + '.')
    key = f'Saving {hrs} × ${rate} × {wks} = {m(saving)} [1]' + (f' + {m(other)}' if other else '') + f'; net annual benefit {m(net)} [1]; payback {m(setup)} / {m(net)} = {pb:.1f} years [1]'
    if D == 1:
        opts, ans = mm(r, net, [saving, saving + lic, net * 2, hrs * rate * 12])
        return {'stem': stem + ' What is the net annual benefit?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the net annual benefit and the payback period.' + (' Advise whether the business should go ahead, giving one non-financial factor.' if D >= 4 else '')
    return {'stem': stem + q, 'answer': f'Net benefit {m(net)} a year; payback {pb:.1f} years' + ('; proceed if payback within target, but consider training, security, staff morale' if D >= 4 else ''), 'key': key + (' ; recommendation with non-financial factor [1]' if D >= 4 else ''), 'marks': 3 + (D >= 4)}


def _comp_c4(r, D):
    c = co(r)
    setup = step(r, 15000, 80000, 500); lic = step(r, 2000, 9000, 100); staff = step(r, 1, 2, 1); sal = step(r, 15000, 30000, 500)
    train = step(r, 1000, 6000, 100)
    benefit = staff * sal - lic
    pb = (setup + train) / benefit
    intro = (f'{c}, a wholesaler in {r.choice(["Bangkok", "Lagos", "Lima", "Karachi", "Manila", "Nairobi"])}, keeps manual ledgers. The owner is considering an integrated accounting package costing {m(setup)} plus training of {m(train)} and an annual licence of {m(lic)}. '
             f'The change would allow {staff} clerk{"s" if staff > 1 else ""} earning {m(sal)} a year to be redeployed.')
    parts = [
        lambda r: ('Calculate the annual net saving and the payback period.', f'{m(benefit)}; {pb:.1f} years', f'{staff} × {m(sal)} − {m(lic)} = {m(benefit)} [1]; ({m(setup)} + {m(train)}) / {m(benefit)} = {pb:.1f} years [2] [3]'),
        lambda r: ('Explain two features of an integrated package that would benefit the business.', 'Single entry updates all ledgers and inventory; instant reports (aged receivables, VAT/tax returns, budgets vs actual); automatic control accounts.', '[4]'),
        lambda r: ('Explain two risks of the change and how each could be controlled.', 'Data loss — regular off-site/cloud backups; unauthorised access/fraud — passwords and user access levels; input errors — validation checks and training.', '[4]'),
        lambda r: ('Advise the owner whether to computerise.', f'Payback of {pb:.1f} years ' + ('is short, so financially worthwhile' if pb < 3 else 'is long, so weigh carefully') + '; also consider staff morale, training, reliability and better information for decisions.', 'Uses payback [1]; financial and non-financial [2]; recommendation [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


for _t in (t7_1, t7_2):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_comp_c4)
t7_2.add('C3', (4, 5), 'multi_step')(_comp_c4)


@t7_2.add('C2', (2, 3, 4), 'explain')
def t72_scen(r, D):
    c = co(r)
    sc = r.choice([('a market stall with 20 cash sales a day', 'a manual system may be adequate; cost of software and training exceeds benefits'),
                   ('a distributor with 2 000 credit customers', 'computerised: volume of transactions, aged receivables, automatic statements'),
                   ('a partnership of three accountants with 40 clients', 'computerised: time recording/billing and reports outweigh moderate cost'),
                   ('a manufacturer with inventory in four warehouses', 'computerised integrated inventory and ledgers give real-time stock levels'),
                   ('a sole trader with poor IT skills and no internet access', 'manual system or simple package; training and reliability issues')])
    return {'stem': f'{c} advises small businesses. One client is {sc[0]}. Explain whether this client should use a computerised accounting system.',
            'answer': sc[1].capitalize() + '.', 'key': 'Considers volume/complexity [1]; cost vs benefit [1]; justified recommendation [1] [3]'}


t7_3 = topic('Implementing a computerised system: data security and controls', 'implementing a computerised system: data security and controls', 'data security', 'controls', 'implementing')
fixed(t7_3, 'C1', (1, 2), [
    ('A check digit is used to', 'detect errors when account or product codes are keyed in', 'Validation check on code numbers (e.g. modulus 11) [1].',
     ['encrypt passwords', 'calculate depreciation', 'back up data']),
    ('Which control restricts staff to only the parts of the system they need?', 'User access levels with individual passwords', 'Access controls/permissions [1].',
     ['A hash total', 'A batch total', 'An aged receivables report']),
    ('A batch total is', 'a total of the values in a batch of documents, compared with the total input', 'Batch control total to detect missing/duplicate items [1].',
     ['a count of the number of passwords', 'the daily backup file', 'the closing balance of the bank account']),
    ('A hash total is', 'a meaningless total (e.g. of account numbers) used only to check completeness of input', 'Hash total has no meaning except as a check [1].',
     ['the total of sales for the month', 'the total of passwords used', 'the balance on the suspense account']),
    ('Which method of changeover runs the old and new systems together for a time?', 'Parallel running', 'Parallel: both run; direct: switch at once; phased: part by part; pilot: one site [1].',
     ['Direct changeover', 'Phased changeover', 'Pilot changeover']),
])
fixed(t7_3, 'C2', (2, 3, 4), [
    ('Explain two methods of protecting accounting data from loss.', 'Regular backups stored off-site or in the cloud; uninterruptible power supply and antivirus software; disaster recovery plan.',
     'Two methods [1 each] + explanation [1 each] [4]'),
    ('Explain why segregation of duties is still important in a computerised system.', 'If one person can set up suppliers, enter invoices and authorise payments, fraud is easier; dividing tasks between users with different access levels reduces this risk.',
     'Fraud risk if one person controls all [1]; access levels divide tasks [1] [2]'),
    ('Compare direct changeover and parallel running when introducing a new accounting system.', 'Direct is cheap and quick but risky if the new system fails; parallel is safer as results can be compared, but doubles the work and costs.',
     'Direct: cost/risk [1]; parallel: safety/cost [1] [2]'),
])


@t7_3.add('C3', (1, 2, 3, 4, 5))
def t73_check(r, D):
    n = 5 if D <= 2 else 6
    while True:
        digits = [r.randint(0, 9) for _ in range(n)]
        w = list(range(n + 1, 1, -1))
        s = sum(a * b for a, b in zip(digits, w))
        cd = (11 - s % 11) % 11
        if cd != 10:
            break
    code = ''.join(map(str, digits))
    stem = f'An accounting system uses modulus 11 check digits on customer account numbers. Weights {", ".join(map(str, w))} are applied to the digits from left to right, and the check digit is 11 minus the remainder after dividing the weighted sum by 11 (a result of 11 gives 0). Calculate the check digit for account number {code}.'
    key = f'Weighted sum = ' + ' + '.join(f'{a}×{b}' for a, b in zip(digits, w)) + f' = {s} [1]; {s} ÷ 11 remainder {s % 11} [1]; check digit {cd} → {code}{cd} [1]'
    if D == 1:
        opts, ans = num_mcq(r, cd, [(cd + 1) % 10, (cd + 3) % 10, s % 11 if s % 11 != cd else (cd + 5) % 10, (cd + 7) % 10], fmtf=str)
        return {'stem': stem.replace('Calculate the check digit', 'What is the check digit'), 'options': opts, 'answer': ans, 'key': key}
    if D >= 4:
        i, j = r.sample(range(n), 2)
        sw = digits[:]
        sw[i], sw[j] = sw[j], sw[i]
        if sw == digits:
            sw[i] = (sw[i] + 1) % 10
        s2 = sum(a * b for a, b in zip(sw, w)) + cd
        ok = s2 % 11 == 0
        stem += f' A clerk then keys in {"".join(map(str, sw))}{cd}. Show whether the system will detect this error.'
        key += f'; check of keyed number: weighted sum incl. check digit (weight 1) = {s2}, {"divisible" if ok else "not divisible"} by 11 → {"not detected" if ok else "rejected"} [1]'
        return {'stem': stem, 'answer': f'Check digit {cd}; the keyed number is {"accepted (not detected)" if ok else "rejected (error detected)"}', 'key': key, 'marks': 4}
    return {'stem': stem, 'answer': str(cd), 'key': key, 'marks': 3}


@t7_3.add('C3', (2, 3, 4))
def t73_batch(r, D):
    c = co(r)
    k = r.choice([4, 5, 6])
    accs = r.sample(range(1001, 9999), k)
    vals = [step(r, 100, 9000, 10) for _ in range(k)]
    miss = r.randrange(k)
    bt, ht = sum(vals), sum(accs)
    in_v = bt - vals[miss]; in_h = ht - accs[miss]
    lst = '; '.join(f'account {a}: {m(v)}' for a, v in zip(accs, vals))
    return {'stem': f'A clerk at {c} prepares a batch of {k} customer receipts: {lst}. After input, the system reports a value total of {m(in_v)} and a hash total of account numbers of {in_h}. Calculate the batch and hash totals for the documents and identify the receipt that was not input.',
            'answer': f'Batch total {m(bt)}, hash total {ht}; missing: account {accs[miss]} ({m(vals[miss])})',
            'key': f'Batch total {m(bt)} [1]; hash total {ht} [1]; differences {m(vals[miss])} and {accs[miss]} identify the missing receipt [1]', 'marks': 3}


def _sec_c4(r, D):
    c = co(r)
    fraud = step(r, 5000, 80000, 500)
    months = r.choice([3, 6, 9, 14])
    intro = (f'At {c}, one accounts clerk sets up new suppliers, enters purchase invoices and releases payments using a shared password. Over {months} months the clerk paid {m(fraud)} to a fictitious supplier before the fraud was found. '
             f'The company has no off-site backup of its accounting data.')
    parts = [
        lambda r: ('Identify two weaknesses in the internal controls.', 'No segregation of duties; shared password/no individual access levels; no review of new suppliers; no backups.', '[2]'),
        lambda r: ('Recommend controls to prevent this type of fraud.', 'Separate supplier set-up, invoice entry and payment approval; individual passwords with access rights; audit trail review; exception reports for new suppliers.', '[4]'),
        lambda r: ('Calculate the average monthly loss and explain how the loss is treated in the financial statements.', f'{m(fraud / months)} per month; loss written off as an expense (unless recoverable by insurance).', f'{m(fraud)} / {months} = {m(fraud / months)} [1]; expense/write-off [1] [2]'),
        lambda r: ('Explain why off-site backups are needed.', 'Fire, theft, hardware failure or ransomware could destroy the only copy of the records; backups allow recovery and continued trading.', '[2]'),
        lambda r: ('Evaluate whether the cost of extra controls is justified.', f'Compare cost of controls with the {m(fraud)} loss and risk of further loss, reputational damage and audit qualification; benefits usually exceed costs.', '[3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t7_3.add('C4', (2, 3, 4, 5), 'multi_step')(_sec_c4)
t7_3.add('C3', (4, 5), 'multi_step')(_sec_c4)


@t7_3.add('C2', (2, 3, 4), 'explain')
def t73_scen(r, D):
    c = co(r)
    s = r.choice([('staff write their passwords on sticky notes next to their screens', 'Passwords can be used by others, so actions cannot be traced to individuals; require private passwords changed regularly.'),
                  ('backups are kept in the same office as the server', 'A fire or theft would destroy both; store backups off-site or in the cloud.'),
                  ('the software is never updated', 'Security weaknesses remain open to hackers/malware; install updates and antivirus.'),
                  ('any user can change the bank details of suppliers', 'Allows payment fraud; restrict to authorised users and require independent verification.'),
                  ('the new system was installed by direct changeover at the busiest time of year', 'High risk of errors and lost data with no fallback; use parallel or phased changeover at a quiet time.')])
    return {'stem': f'During a review at {c} it was found that {s[0]}. Explain the risk this creates and recommend a control.', 'answer': s[1], 'key': 'Risk identified [1]; consequence explained [1]; appropriate control [1] [3]'}


CHAPTERS[7] = [t7_1, t7_2, t7_3]


# ===================================================================== 8 Analysis and communication of information
def _inv_data(r):
    N = step(r, 500000, 5000000, 100000)
    nom = r.choice([1, 0.5, 0.25])
    pat = step(r, 100000, 1500000, 1000)
    pref = step(r, 0, 300000, 50000)
    prate = r.choice([5, 6, 8])
    pdiv = pref * prate // 100
    dps = r.choice([0.04, 0.05, 0.06, 0.08, 0.1, 0.12, 0.15])
    eps = (pat - pdiv) / N
    dps = round(eps * r.choice([0.25, 0.3, 0.4, 0.5, 0.6, 0.7]), 2) or 0.01
    price = round(eps * r.choice([6, 8, 10, 12, 15, 18, 20]), 2)
    return dict(N=N, nom=nom, pat=pat, pref=pref, prate=prate, pdiv=pdiv, dps=dps, eps=eps, price=price, div=N * dps)


t8_1 = topic('Investor ratios: EPS, P/E, dividend cover, dividend yield', 'investor ratios: eps, p/e, dividend cover, dividend yield', 'investor ratios', 'earnings per share', 'price earnings')
fixed(t8_1, 'C1', (1, 2), [
    ('Earnings per share is calculated as', 'profit for the year attributable to ordinary shareholders ÷ number of ordinary shares in issue', 'EPS = (profit after tax − preference dividends) / ordinary shares [1].',
     ['profit before tax ÷ number of ordinary shares', 'dividends paid ÷ number of ordinary shares', 'market price ÷ dividend per share']),
    ('The price/earnings ratio is', 'market price per share ÷ earnings per share', 'P/E = MPS / EPS [1].',
     ['earnings per share ÷ market price per share', 'dividend per share ÷ market price', 'profit for the year ÷ dividends']),
    ('Dividend yield is', 'dividend per share ÷ market price per share × 100', 'Yield = DPS / MPS × 100 [1].',
     ['market price ÷ dividend per share', 'EPS ÷ dividend per share', 'dividend per share ÷ nominal value × 100']),
    ('Dividend cover measures', 'how many times the ordinary dividend could be paid out of profit available to ordinary shareholders', 'Cover = profit for ordinary shareholders / ordinary dividends [1].',
     ['how quickly the company pays its dividends', 'the return on capital employed', 'the proportion of debt in capital']),
    ('A high P/E ratio usually indicates that', 'investors expect strong future growth in earnings', 'Market pays more per $ of current earnings [1].',
     ['the company is about to fail', 'the dividend yield is high', 'the company has high gearing']),
])
fixed(t8_1, 'C2', (2, 3, 4), [
    ('Explain why a high dividend cover may be viewed both favourably and unfavourably by shareholders.', 'Favourably: dividends are secure and profits are retained for growth. Unfavourably: shareholders seeking income receive a small proportion of profit as dividend.',
     'Security/retention [1]; low payout for income investors [1] [2]'),
    ('Explain why preference dividends are deducted before calculating EPS.', 'EPS measures earnings available to ordinary shareholders; preference dividends are paid first and are not available to them.',
     'EPS for ordinary shareholders [1]; preference paid first [1] [2]'),
    ('Explain one limitation of using the P/E ratio to compare two companies.', 'It depends on share price, which reflects market sentiment, and on EPS, which depends on accounting policies; companies in different industries have different typical P/E ratios.',
     'Limitation [1]; explanation [1] [2]'),
])


@t8_1.add('C3', (1, 2, 3, 4, 5))
def t81_ratios(r, D):
    x = _inv_data(r)
    c = co(r)
    stem = (f'{c} has {nm(x["N"])} ordinary shares of ${x["nom"]:.2f} each in issue' + (f' and {m(x["pref"])} {x["prate"]}% preference shares' if x['pref'] else '') + f'. Profit for the year after tax was {m(x["pat"])}. '
            f'An ordinary dividend of ${x["dps"]:.2f} per share was paid and the market price of an ordinary share is ${x["price"]:.2f}.')
    eps, pe, cov, yld = x['eps'], x['price'] / x['eps'], (x['pat'] - x['pdiv']) / x['div'], x['dps'] / x['price'] * 100
    key = (f'EPS = ({m(x["pat"])}' + (f' − {m(x["pdiv"])}' if x['pdiv'] else '') + f') / {nm(x["N"])} = ${eps:.4f} = {eps * 100:.2f} cents [1]; P/E = {x["price"]:.2f}/{eps:.4f} = {pe:.1f} [1]; '
           f'dividend cover = {m(x["pat"] - x["pdiv"])}/{m(x["div"])} = {cov:.2f} times [1]; yield = {x["dps"]:.2f}/{x["price"]:.2f} × 100 = {yld:.2f}% [1]')
    f = lambda v: f'{v * 100:.2f} cents'
    if D == 1:
        opts, ans = num_mcq(r, eps, [x['pat'] / x['N'] if x['pdiv'] else eps * 1.25, x['dps'], eps * 10, x['pat'] / (x['N'] * x['nom']) if x['nom'] != 1 else eps * 0.8], fmtf=f)
        return {'stem': stem + ' What is the earnings per share?', 'options': opts, 'answer': ans, 'key': key}
    if D == 2:
        return {'stem': stem + ' Calculate the earnings per share and the price/earnings ratio.', 'answer': f'EPS {eps * 100:.2f} cents; P/E {pe:.1f}', 'key': key, 'marks': 2}
    return {'stem': stem + ' Calculate the earnings per share, P/E ratio, dividend cover and dividend yield.', 'answer': f'EPS {eps * 100:.2f} cents; P/E {pe:.1f}; dividend cover {cov:.2f} times; dividend yield {yld:.2f}%', 'key': key, 'marks': 4, 'type': 'multi_step'}


@t8_1.add('C3', (2, 3, 4))
def t81_reverse(r, D):
    c = co(r)
    N = step(r, 400000, 4000000, 100000)
    eps_c = r.choice([12, 15, 18, 20, 24, 25, 30, 36, 40])
    pe = r.choice([8, 10, 12, 14, 15, 16])
    cov = r.choice([2, 2.5, 3, 4])
    price = eps_c * pe / 100
    dps = eps_c / cov / 100
    return {'stem': f'{c} has {nm(N)} ordinary shares in issue and no preference shares. Its EPS is {eps_c} cents, its P/E ratio is {pe} and its dividend cover is {cov} times. Calculate the profit for the year, the market price per share, the total dividend paid and the dividend yield.',
            'answer': f'Profit {m(N * eps_c / 100)}; price ${price:.2f}; dividends {m(N * dps)}; yield {dps / price * 100:.2f}%',
            'key': f'Profit = {nm(N)} × ${eps_c / 100:.2f} = {m(N * eps_c / 100)} [1]; price = {eps_c} × {pe} = ${price:.2f} [1]; DPS {eps_c}/{cov} = {dps * 100:.2f} cents, total {m(N * dps)} [1]; yield = {dps:.4f}/{price:.2f} = {dps / price * 100:.2f}% [1]', 'marks': 4}


def _inv_c4(r, D):
    a, b = r.sample(COS, 2)
    xa, xb = _inv_data(r), _inv_data(r)
    inv = r.choice(['a retired teacher seeking regular income', 'a young investor seeking long-term growth', 'a pension fund wanting low risk', 'an investor who wants a balance of income and growth'])
    def line(n, x):
        return f'{n}: profit after tax {m(x["pat"])}, preference dividends {m(x["pdiv"])}, {nm(x["N"])} ordinary shares, ordinary dividend per share ${x["dps"]:.2f}, market price ${x["price"]:.2f}'
    intro = f'An adviser is comparing two listed companies for {inv}. ' + line(a, xa) + '. ' + line(b, xb) + '.'
    def rat(x):
        return x['eps'], x['price'] / x['eps'], (x['pat'] - x['pdiv']) / x['div'], x['dps'] / x['price'] * 100
    ra, rb = rat(xa), rat(xb)
    better_inc = a if ra[3] > rb[3] else b
    better_gr = a if ra[1] > rb[1] else b
    parts = [
        lambda r: ('Calculate the EPS and P/E ratio for each company.', f'{a}: {ra[0] * 100:.2f} cents, {ra[1]:.1f}; {b}: {rb[0] * 100:.2f} cents, {rb[1]:.1f}', 'EPS each [2]; P/E each [2] [4]'),
        lambda r: ('Calculate the dividend cover and dividend yield for each company.', f'{a}: {ra[2]:.2f} times, {ra[3]:.2f}%; {b}: {rb[2]:.2f} times, {rb[3]:.2f}%', 'Cover each [2]; yield each [2] [4]'),
        lambda r: (f'Advise the investor which company to choose.', f'For income choose {better_inc} (higher yield); for growth the market rates {better_gr} more highly (higher P/E). Recommendation follows the investor\'s objective; check dividend cover for safety.',
                   'Links ratios to objective [2]; uses cover/risk [1]; justified recommendation [1] [4]'),
        lambda r: ('State two limitations of basing the decision only on these ratios.', 'Based on past results; share prices fluctuate; different accounting policies; ignores non-financial factors such as management quality and industry outlook.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t8_1.add('C4', (2, 3, 4, 5), 'multi_step')(_inv_c4)
t8_1.add('C3', (4, 5), 'multi_step')(_inv_c4)


@t8_1.add('C2', (2, 3, 4), 'explain')
def t81_err(r, D):
    x = _inv_data(r)
    while not x['pdiv']:
        x = _inv_data(r)
    wrong = x['pat'] / x['N']
    return {'stem': f'An analyst calculated the EPS of {co(r)} as {wrong * 100:.2f} cents, dividing profit after tax of {m(x["pat"])} by {nm(x["N"])} ordinary shares. The company also has {m(x["pref"])} {x["prate"]}% preference shares. Explain the error and calculate the correct EPS.',
            'answer': f'Preference dividends ({m(x["pdiv"])}) must be deducted first. Correct EPS = {m(x["pat"] - x["pdiv"])} / {nm(x["N"])} = {x["eps"] * 100:.2f} cents.',
            'key': f'Preference dividend omitted [1]; {x["prate"]}% × {m(x["pref"])} = {m(x["pdiv"])} [1]; EPS {x["eps"] * 100:.2f} cents [1] [3]'}


t8_2 = topic('Gearing, interest cover and capital structure analysis', 'gearing, interest cover and capital structure analysis', 'gearing', 'interest cover', 'capital structure')
fixed(t8_2, 'C1', (1, 2), [
    ('A company is described as highly geared when', 'a large proportion of its capital comes from fixed-return finance such as loans and preference shares', 'High gearing: debt + preference shares large relative to equity [1].',
     ['it has a large amount of inventory', 'it pays high dividends', 'it has no long-term loans']),
    ('Interest cover is calculated as', 'profit from operations ÷ interest payable', 'Interest cover = PBIT / finance costs [1].',
     ['interest payable ÷ profit for the year', 'profit after tax ÷ interest', 'loans ÷ equity']),
    ('Which is usually included as "debt" when calculating gearing?', 'Redeemable preference shares and debentures', 'Fixed-cost capital: non-current loans, debentures, (redeemable) preference shares [1].',
     ['Trade payables', 'Retained earnings', 'Share premium']),
    ('A highly geared company that increases profit from operations will see', 'a proportionately larger increase in profit available to ordinary shareholders', 'Fixed interest magnifies changes in earnings [1].',
     ['a fall in earnings per share', 'no change in earnings per share', 'its interest charge rise automatically']),
])
fixed(t8_2, 'C2', (2, 3, 4), [
    ('Explain why lenders are concerned about a company\'s gearing and interest cover.', 'High gearing and low interest cover mean a greater risk that the company cannot pay interest or repay loans if profits fall; lenders may demand security or higher rates.',
     'Risk of default [1]; low cover means little margin [1]; consequence [1] [3]'),
    ('Explain why ordinary shareholders might benefit from high gearing when profits are rising.', 'Interest is fixed, so extra profit above the interest cost belongs to the shareholders, raising EPS and return on equity more than in proportion.',
     'Fixed interest [1]; magnified returns [1] [2]'),
])


@t8_2.add('C3', (1, 2, 3, 4, 5))
def t82_gear(r, D):
    c = co(r)
    sc = step(r, 300000, 2000000, 50000); res = step(r, 100000, 1500000, 10000)
    loan = step(r, 100000, 1500000, 50000); pref = step(r, 0, 400000, 50000) if D >= 3 else 0
    pbit = step(r, 80000, 600000, 1000); rate = r.choice([5, 6, 7, 8, 10])
    intr = loan * rate // 100
    debt = loan + pref
    eq = sc + res
    g = debt / (debt + eq) * 100
    cov = pbit / intr
    stem = (f'{c}: ordinary share capital {m(sc)}, reserves {m(res)}, {rate}% debentures {m(loan)}' + (f', redeemable preference shares {m(pref)}' if pref else '') + f'. Profit from operations is {m(pbit)}.')
    key = f'Gearing = {m(debt)} / ({m(debt)} + {m(eq)}) × 100 = {g:.1f}% [1]; interest {rate}% × {m(loan)} = {m(intr)} [1]; cover = {m(pbit)} / {m(intr)} = {cov:.1f} times [1]'
    if D == 1:
        opts, ans = num_mcq(r, g, [debt / eq * 100, eq / (debt + eq) * 100, loan / (loan + sc) * 100 if (loan / (loan + sc) * 100) else g + 5, g + 10], fmtf=lambda v: pc(v))
        return {'stem': stem + ' What is the gearing ratio (debt as a percentage of debt plus equity)?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the gearing ratio and the interest cover.'
    if D >= 4:
        nl = step(r, 100000, 600000, 50000)
        g2 = (debt + nl) / (debt + nl + eq) * 100
        cov2 = pbit / (intr + nl * rate / 100)
        q += f' The company plans to borrow a further {m(nl)} at {rate}%. Recalculate both ratios (assume profit is unchanged) and comment.'
        return {'stem': stem + q, 'answer': f'Gearing {g:.1f}% → {g2:.1f}%; interest cover {cov:.1f} → {cov2:.1f} times; risk to lenders and shareholders increases',
                'key': key + f'; new gearing {g2:.1f}% [1]; new cover {cov2:.1f} [1]; comment [1]', 'marks': 6}
    return {'stem': stem + q, 'answer': f'Gearing {g:.1f}%; interest cover {cov:.1f} times', 'key': key, 'marks': 3}


@t8_2.add('C3', (3, 4, 5))
def t82_eps_effect(r, D):
    c = co(r)
    N = step(r, 400000, 2000000, 100000)
    need = step(r, 200000, 1000000, 50000)
    price = r.choice([1.25, 2.0, 2.5, 4.0])
    rate = r.choice([6, 8, 10]); tax = r.choice([20, 25, 30])
    pbit = step(r, 150000, 800000, 1000); old_int = step(r, 0, 40000, 1000)
    pbt_a = pbit - old_int - need * rate / 100; pat_a = pbt_a * (100 - tax) / 100
    pbt_b = pbit - old_int; pat_b = pbt_b * (100 - tax) / 100
    nsh = need / price
    eps_a = pat_a / N; eps_b = pat_b / (N + nsh)
    return {'stem': f'{c} has {nm(N)} ordinary shares and needs {m(need)}. Option A: issue {rate}% debentures. Option B: issue ordinary shares at ${price:.2f}. Expected profit from operations is {m(pbit)}; existing interest is {m(old_int)}; tax is {tax}%. Calculate the EPS under each option and state which gives the higher EPS.',
            'answer': f'A: {eps_a * 100:.2f} cents; B: {eps_b * 100:.2f} cents; {"A (debt)" if eps_a > eps_b else "B (shares)"} gives the higher EPS',
            'key': f'A: PBT {m(pbt_a)}, PAT {m(pat_a)} / {nm(N)} = {eps_a * 100:.2f}c [2]; B: shares {nm(nsh)}, PAT {m(pat_b)} / {nm(N + nsh)} = {eps_b * 100:.2f}c [2]; conclusion [1]', 'marks': 5, 'type': 'multi_step'}


@t8_2.add('C2', (2, 3, 4), 'explain')
def t82_err(r, D):
    c = co(r)
    loan, eq = step(r, 200000, 900000, 50000), step(r, 400000, 1500000, 50000)
    wrong = loan / eq * 100; right = loan / (loan + eq) * 100
    return {'stem': f'A student calculated the gearing of {c} as {wrong:.1f}% and said the company is "{"highly" if wrong > 50 else "low"} geared". The company has non-current loans of {m(loan)} and equity of {m(eq)}. Using the formula debt ÷ (debt + equity), explain the error and calculate the correct gearing.',
            'answer': f'The student used debt ÷ equity. Correct gearing = {m(loan)} / {m(loan + eq)} × 100 = {right:.1f}%, which is {"high (above 50%)" if right > 50 else "low/moderate (below 50%)"}.',
            'key': f'Identifies formula used [1]; correct {right:.1f}% [1]; conclusion on level [1] [3]'}


def _gear_c4(r, D):
    a = co(r)
    eq1, eq2 = step(r, 500000, 1500000, 50000), step(r, 500000, 1500000, 50000)
    d1, d2 = step(r, 100000, 600000, 50000), step(r, 400000, 1500000, 50000)
    p1, p2 = step(r, 100000, 400000, 1000), step(r, 120000, 450000, 1000)
    i1, i2 = d1 * 6 // 100, d2 * 8 // 100
    yrs = r.choice(['2025', '2026'])
    intro = f'Extracts for {a}: year {int(yrs) - 1}: equity {m(eq1)}, debentures {m(d1)}, profit from operations {m(p1)}, interest {m(i1)}. Year {yrs}: equity {m(eq2)}, debentures {m(d2)}, profit from operations {m(p2)}, interest {m(i2)}.'
    g1, g2 = d1 / (d1 + eq1) * 100, d2 / (d2 + eq2) * 100
    parts = [
        lambda r: ('Calculate the gearing ratio for each year.', f'{g1:.1f}% → {g2:.1f}%', '[2]'),
        lambda r: ('Calculate the interest cover for each year.', f'{p1 / i1:.1f} → {p2 / i2:.1f} times', '[2]'),
        lambda r: ('Calculate the return on capital employed (profit from operations ÷ (equity + debentures)) for each year.', f'{p1 / (eq1 + d1) * 100:.1f}% → {p2 / (eq2 + d2) * 100:.1f}%', '[2]'),
        lambda r: ('Evaluate the change in capital structure from the point of view of a bank considering a further loan.', f'Gearing {"rose" if g2 > g1 else "fell"} to {g2:.1f}% and interest cover is {p2 / i2:.1f} times; ' + ('greater risk — bank may require security/higher rate' if g2 > g1 else 'lower risk — loan more likely'),
                   'Uses gearing trend [1]; uses cover [1]; security/other factors [1]; conclusion [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t8_2.add('C4', (2, 3, 4, 5), 'multi_step')(_gear_c4)


t8_3 = topic('Interpreting financial statements for stakeholders\' decisions', 'interpreting financial statements for stakeholders\' decisions', 'interpreting', 'stakeholders', 'ratios')
fixed(t8_3, 'C1', (1, 2), [
    ('Return on capital employed (ROCE) is calculated as', 'profit from operations ÷ capital employed × 100', 'ROCE = PBIT / (equity + non-current liabilities) × 100 [1].',
     ['profit for the year ÷ revenue × 100', 'revenue ÷ capital employed', 'current assets ÷ current liabilities']),
    ('The liquid (acid test) ratio excludes', 'inventory', 'Acid test = (current assets − inventory) / current liabilities [1].',
     ['trade receivables', 'cash', 'trade payables']),
    ('Trade receivables turnover (days) is calculated as', 'trade receivables ÷ credit sales × 365', 'Collection period [1].',
     ['credit sales ÷ trade receivables × 365', 'trade payables ÷ purchases × 365', 'inventory ÷ cost of sales × 365']),
    ('Which stakeholder is most interested in the liquidity of a company?', 'A trade supplier offering credit', 'Suppliers want to be paid on time → liquidity [1].',
     ['A long-term investor seeking growth', 'The government statistician', 'A competitor']),
    ('Inventory turnover (times) is calculated as', 'cost of sales ÷ average inventory', 'Rate of inventory turnover [1].',
     ['revenue ÷ closing inventory × 365', 'average inventory ÷ cost of sales', 'gross profit ÷ inventory']),
])
fixed(t8_3, 'C2', (2, 3, 4), [
    ('Explain two limitations of using ratio analysis to compare two companies.', 'Different accounting policies (depreciation, inventory valuation); different year ends or sizes; historical data; window dressing; ratios do not explain causes.',
     'Two limitations [1 each] + explanation [1 each] [4]'),
    ('Explain why a fall in the gross margin might occur even though revenue has increased.', 'Prices may have been cut to increase sales volume, or purchase costs may have risen faster than selling prices, or the sales mix changed to lower-margin products.',
     'Reason [1]; development [1] [2]'),
    ('Explain why a very high current ratio is not necessarily good.', 'It may indicate excess inventory, slow-paying receivables or idle cash that could be invested more profitably.',
     'Idle resources [1]; example [1] [2]'),
])


def _fin(r):
    rev = step(r, 400000, 3000000, 10000); gm = r.choice([25, 30, 35, 40, 45, 50])
    gp = rev * gm // 100; cos = rev - gp
    exp = round(gp * r.uniform(0.4, 0.8) / 1000) * 1000
    pfo = gp - exp
    inv0 = step(r, 30000, 200000, 1000); inv1 = step(r, 30000, 220000, 1000)
    rec = step(r, 20000, 400000, 1000); cash = step(r, 0, 80000, 1000); pay = step(r, 20000, 300000, 1000)
    ce = step(r, int(pfo * 3), int(pfo * 10) + 10000, 1000)
    return dict(rev=rev, gp=gp, cos=cos, exp=exp, pfo=pfo, inv0=inv0, inv1=inv1, rec=rec, cash=cash, pay=pay, ce=ce, gm=gm)


@t8_3.add('C3', (1, 2, 3, 4, 5))
def t83_ratios(r, D):
    c = co(r)
    x = _fin(r)
    sel = ['gm', 'roce', 'cur', 'acid', 'rec', 'invt', 'pay', 'pm']
    k = 1 if D == 1 else (2 if D == 2 else (3 if D == 3 else 4))
    pick = r.sample(sel, k)
    ca = x['inv1'] + x['rec'] + x['cash']
    val = {
        'gm': ('gross margin', f'{x["gp"] / x["rev"] * 100:.1f}%', f'{m(x["gp"])}/{m(x["rev"])} × 100'),
        'pm': ('profit margin (profit from operations ÷ revenue)', f'{x["pfo"] / x["rev"] * 100:.1f}%', f'{m(x["pfo"])}/{m(x["rev"])} × 100'),
        'roce': ('return on capital employed', f'{x["pfo"] / x["ce"] * 100:.1f}%', f'{m(x["pfo"])}/{m(x["ce"])} × 100'),
        'cur': ('current ratio', f'{ca / x["pay"]:.2f}:1', f'{m(ca)}/{m(x["pay"])}'),
        'acid': ('liquid (acid test) ratio', f'{(ca - x["inv1"]) / x["pay"]:.2f}:1', f'{m(ca - x["inv1"])}/{m(x["pay"])}'),
        'rec': ('trade receivables turnover in days (all sales on credit)', f'{x["rec"] / x["rev"] * 365:.0f} days', f'{m(x["rec"])}/{m(x["rev"])} × 365'),
        'invt': ('rate of inventory turnover (times, using average inventory)', f'{x["cos"] / ((x["inv0"] + x["inv1"]) / 2):.1f} times', f'{m(x["cos"])}/{m((x["inv0"] + x["inv1"]) / 2)}'),
        'pay': ('trade payables turnover in days (purchases = cost of sales + closing − opening inventory)', f'{x["pay"] / (x["cos"] + x["inv1"] - x["inv0"]) * 365:.0f} days', f'{m(x["pay"])}/{m(x["cos"] + x["inv1"] - x["inv0"])} × 365'),
    }
    stem = (f'Extracts for {c} for the year ended {ye(r)}: revenue {m(x["rev"])}, cost of sales {m(x["cos"])}, expenses {m(x["exp"])}, opening inventory {m(x["inv0"])}, closing inventory {m(x["inv1"])}, trade receivables {m(x["rec"])}, '
            f'cash {m(x["cash"])}, trade payables (the only current liability) {m(x["pay"])}, capital employed {m(x["ce"])}. Calculate the ' + ', '.join(val[p][0] for p in pick) + '.')
    if D == 1:
        p = pick[0]
        corr = val[p][1]
        alts = {'gm': [f'{x["gp"] / x["cos"] * 100:.1f}%', f'{x["cos"] / x["rev"] * 100:.1f}%', f'{x["pfo"] / x["rev"] * 100:.1f}%'],
                'pm': [f'{x["gp"] / x["rev"] * 100:.1f}%', f'{x["pfo"] / x["ce"] * 100:.1f}%', f'{x["exp"] / x["rev"] * 100:.1f}%'],
                'roce': [f'{x["gp"] / x["ce"] * 100:.1f}%', f'{x["pfo"] / x["rev"] * 100:.1f}%', f'{x["ce"] / x["pfo"]:.1f}%'],
                'cur': [f'{x["pay"] / ca:.2f}:1', f'{(ca - x["inv1"]) / x["pay"]:.2f}:1', f'{(ca + x["inv0"]) / x["pay"]:.2f}:1'],
                'acid': [f'{ca / x["pay"]:.2f}:1', f'{x["cash"] / x["pay"]:.2f}:1', f'{x["pay"] / (ca - x["inv1"]):.2f}:1'],
                'rec': [f'{x["rev"] / x["rec"]:.0f} days', f'{x["rec"] / x["cos"] * 365:.0f} days', f'{x["rec"] / x["rev"] * 52:.0f} days'],
                'invt': [f'{x["cos"] / x["inv1"]:.1f} times', f'{x["rev"] / ((x["inv0"] + x["inv1"]) / 2):.1f} times', f'{((x["inv0"] + x["inv1"]) / 2) / x["cos"] * 365:.1f} times'],
                'pay': [f'{x["pay"] / x["rev"] * 365:.0f} days', f'{x["pay"] / x["cos"] * 52:.0f} days', f'{(x["cos"] + x["inv1"] - x["inv0"]) / x["pay"]:.0f} days']}[p]
        opts, ans = mcq(r, corr, alts)
        return {'stem': stem.replace('. Calculate the ', '. What is the ') + '?', 'options': opts, 'answer': ans, 'key': f'{val[p][0]} = {val[p][2]} = {corr} [1]'}
    return {'stem': stem, 'answer': '; '.join(f'{val[p][0].split(" (")[0]} {val[p][1]}' for p in pick), 'key': '; '.join(f'{val[p][0].split(" (")[0]}: {val[p][2]} = {val[p][1]} [1]' for p in pick), 'marks': k}


def _cmp_adv(who, a, b, A, B):
    if 'bank' in who or 'supplier' in who:
        w = a if A[3] > B[3] else b
        return f'Liquidity matters most: liquid ratio {a} {A[3]:.2f} vs {b} {B[3]:.2f}, collection period {A[4]:.0f} vs {B[4]:.0f} days, so {w} is the safer credit risk; also consider profitability and security.'
    w = a if A[1] > B[1] else b
    return f'Profitability matters most: ROCE {a} {A[1]:.1f}% vs {b} {B[1]:.1f}%, gross margin {A[0]:.1f}% vs {B[0]:.1f}%, so {w} is performing better; check liquidity and that the companies are comparable.'


def _cmp_c4(r, D):
    a, b = r.sample(COS, 2)
    xa, xb = _fin(r), _fin(r)
    who = r.choice(['a bank deciding whether to grant an overdraft', 'a supplier deciding whether to offer 60 days\' credit', 'an investor choosing which company to buy shares in', 'the managing director assessing performance'])
    def ln(n, x):
        return f'{n}: revenue {m(x["rev"])}, gross profit {m(x["gp"])}, profit from operations {m(x["pfo"])}, capital employed {m(x["ce"])}, current assets {m(x["inv1"] + x["rec"] + x["cash"])} (inventory {m(x["inv1"])}), current liabilities {m(x["pay"])}, trade receivables {m(x["rec"])}'
    intro = f'The following data is available for {who}. ' + ln(a, xa) + '. ' + ln(b, xb) + '.'
    R = lambda x: (x['gp'] / x['rev'] * 100, x['pfo'] / x['ce'] * 100, (x['inv1'] + x['rec'] + x['cash']) / x['pay'], (x['rec'] + x['cash']) / x['pay'], x['rec'] / x['rev'] * 365)
    A, B = R(xa), R(xb)
    parts = [
        lambda r: ('Calculate the gross margin and ROCE for each company.', f'{a}: {A[0]:.1f}%, {A[1]:.1f}%; {b}: {B[0]:.1f}%, {B[1]:.1f}%', '[4]'),
        lambda r: ('Calculate the current ratio and liquid ratio for each company.', f'{a}: {A[2]:.2f}, {A[3]:.2f}; {b}: {B[2]:.2f}, {B[3]:.2f}', '[4]'),
        lambda r: ('Calculate the trade receivables collection period for each company (all sales on credit).', f'{a}: {A[4]:.0f} days; {b}: {B[4]:.0f} days', '[2]'),
        lambda r: (f'Advise {who.split(" deciding")[0].split(" choosing")[0].split(" assessing")[0]} which company is the better prospect, using your ratios.', _cmp_adv(who, a, b, A, B),
                   'Relevant ratios selected for stakeholder [2]; comparison with figures [2]; limitation [1]; conclusion [1] [6]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t8_3.add('C4', (2, 3, 4, 5), 'multi_step')(_cmp_c4)
t8_3.add('C3', (4, 5), 'multi_step')(_cmp_c4)


@t8_3.add('C2', (2, 3, 4), 'explain')
def t83_trend(r, D):
    c = co(r)
    ratio = r.choice([('trade receivables collection period', 'days', 38, 61, 'customers are paying more slowly — possible weak credit control or a deliberate policy of longer credit to boost sales; cash flow worsens'),
                      ('rate of inventory turnover', 'times', 9.5, 6.2, 'inventory is selling more slowly — possible obsolete or excess stock, tying up cash and increasing storage costs'),
                      ('gross margin', '%', 42.0, 35.5, 'lower selling prices or higher purchase costs; changed sales mix'),
                      ('current ratio', ':1', 1.6, 0.9, 'liquidity has worsened; current assets now barely cover current liabilities, a risk to paying suppliers on time'),
                      ('ROCE', '%', 18.0, 11.5, 'profit is falling relative to capital; new investment may not yet be generating returns'),
                      ('trade payables payment period', 'days', 45, 72, 'the company is taking longer to pay suppliers — perhaps cash shortage; risks losing discounts and supplier goodwill')])
    f = r.uniform(0.9, 1.1)
    v1, v2 = round(ratio[2] * f, 1), round(ratio[3] * f, 1)
    return {'stem': f'The {ratio[0]} of {c} changed from {v1}{" " if ratio[1] in ("days", "times") else ""}{ratio[1]} last year to {v2}{" " if ratio[1] in ("days", "times") else ""}{ratio[1]} this year. Explain two possible causes of the change and its significance for the company.',
            'answer': ratio[4].capitalize() + '.', 'key': 'Direction of change interpreted [1]; two plausible causes [2]; significance for stakeholders [1] [4]'}


t8_4 = topic('Ethics in accounting and limitations of published information', 'ethics in accounting and limitations of published information', 'ethics', 'limitations', 'window dressing')
fixed(t8_4, 'C1', (1, 2), [
    ('Window dressing means', 'arranging transactions near the year end to make the financial statements look better than they are', 'Short-term manipulation of year-end position [1].',
     ['painting the company\'s premises', 'preparing statements in a standard format', 'recording assets at historical cost']),
    ('Which is a fundamental principle of the IFAC/IESBA code of ethics for accountants?', 'Objectivity', 'Principles: integrity, objectivity, professional competence and due care, confidentiality, professional behaviour [1].',
     ['Profitability', 'Prudence in pricing', 'Maximising shareholder wealth']),
    ('A limitation of published financial statements is that they', 'are based largely on historical costs and past events', 'Historical, may ignore inflation and non-financial info [1].',
     ['must be audited', 'follow IAS', 'include a statement of cash flows']),
    ('An accountant who refuses to disclose a client\'s information to a competitor is following the principle of', 'confidentiality', 'Confidentiality [1].',
     ['objectivity', 'professional competence', 'integrity of pricing']),
])
fixed(t8_4, 'C2', (2, 3, 4), [
    ('Explain two limitations of published financial statements for a potential investor.', 'They are historical and may not predict the future; they omit non-financial factors (staff skills, brand, environment); based on estimates and policies chosen by directors; inflation distorts comparisons.',
     'Two limitations [1 each] + explanation [1 each] [4]'),
    ('Explain why an accountant faces an ethical dilemma when a director asks for profits to be "smoothed".', 'Smoothing misleads users and breaches integrity and objectivity, but the accountant may fear losing his job or the director\'s goodwill; he should refuse and, if necessary, report through proper channels.',
     'Breach of principle [1]; pressure/conflict [1]; appropriate action [1] [3]'),
    ('Explain how inflation can limit the usefulness of financial statements.', 'Assets at historical cost may be understated; revenue growth may be due to price rises not volume; comparisons over years become distorted.',
     'Asset values [1]; misleading trends [1] [2]'),
])


@t8_4.add('C3', (1, 2, 3, 4, 5))
def t84_window(r, D):
    c = co(r)
    ca = step(r, 100000, 500000, 1000); cl = step(r, 80000, 400000, 1000)
    inv = step(r, 20000, ca // 2, 1000)
    pay = step(r, 10000, min(ca - inv, cl) - 5000 if min(ca - inv, cl) > 15000 else 15000, 1000)
    act = r.choice(['pay', 'loan']) if D >= 3 else 'pay'
    if act == 'pay':
        ca2, cl2 = ca - pay, cl - pay
        what = f'uses {m(pay)} of cash to pay trade payables'
    else:
        ca2, cl2 = ca + pay, cl
        what = f'takes out a two-year bank loan of {m(pay)}, received in cash'
    stem = f'Before the year end {c} has current assets of {m(ca)} (including inventory {m(inv)}) and current liabilities of {m(cl)}. On the last day of the year it {what}.'
    key = f'Before {ca / cl:.2f}:1 [1]; after {m(ca2)}/{m(cl2)} = {ca2 / cl2:.2f}:1 [1]'
    if D == 1:
        opts, ans = mcq(r, f'{ca2 / cl2:.2f}:1', [f'{ca / cl:.2f}:1', f'{(ca - pay) / cl:.2f}:1', f'{ca / (cl - pay):.2f}:1', f'{(ca2 - inv) / cl2:.2f}:1'])
        return {'stem': stem + ' What is the current ratio after the transaction?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the current ratio before and after, and explain why this may be window dressing.'
    if D >= 4:
        q = ' Calculate the current and liquid ratios before and after the transaction, and discuss whether this is ethical.'
        key += f'; liquid before {(ca - inv) / cl:.2f}, after {(ca2 - inv) / cl2:.2f} [1]; ethics: misleads users if done only to flatter ratios [1]'
    return {'stem': stem + q, 'answer': f'Current ratio {ca / cl:.2f}:1 → {ca2 / cl2:.2f}:1' + (f'; liquid {(ca - inv) / cl:.2f} → {(ca2 - inv) / cl2:.2f}' if D >= 4 else '') + '; it improves the reported position without changing the underlying liquidity, which may mislead users.',
            'key': key + ' ; explanation [1]', 'marks': 3 + (D >= 4)}


@t8_4.add('C3', (2, 3, 4))
def t84_infl(r, D):
    c = co(r)
    r1 = step(r, 500000, 2000000, 10000)
    g = r.choice([6, 8, 10, 12, 15]); inf = r.choice([4, 5, 7, 9, 11, 14])
    r2 = r1 * (100 + g) // 100
    real = r2 / (1 + inf / 100)
    rg = (real / r1 - 1) * 100
    return {'stem': f'The directors\' report of {c} states: "Revenue grew {g}% from {m(r1)} to {m(r2)} — an excellent year." Prices in the economy rose by {inf}% over the year. Calculate the revenue in real terms (at last year\'s prices) and the real growth rate, and comment on the directors\' statement.',
            'answer': f'Real revenue {m(real)}; real growth {rg:.1f}%; the claim overstates performance because part of the growth is inflation.',
            'key': f'{m(r2)} / 1.{inf:02d} = {m(real)} [1]; real growth {rg:.1f}% [1]; comment: inflation limits usefulness of historical figures [1]', 'marks': 3}


@t8_4.add('C2', (2, 3, 4), 'explain')
def t84_dilemma(r, D):
    c = co(r); p = r.choice(PEOPLE)
    v = step(r, 10000, 200000, 1000)
    s = r.choice([(f'reduce the allowance for irrecoverable debts by {m(v)} so that profit meets the bonus target', 'integrity and objectivity'),
                  (f'record {m(v)} of sales made in the first week of the next year in the current year', 'integrity (misstatement of revenue)'),
                  (f'not mention a {m(v)} legal claim to the auditors', 'integrity and professional behaviour'),
                  (f'value obsolete inventory of {m(v)} at cost rather than net realisable value', 'integrity and professional competence (IAS 2)'),
                  (f'give details of a client\'s {m(v)} tax dispute to a friend who is a journalist', 'confidentiality')])
    return {'stem': f'{p}, an accountant at {c}, is asked by a director to {s[0]}. Explain the ethical principles involved and advise {p} what to do.',
            'answer': f'This breaches {s[1]}. {p} should refuse, explain the accounting requirement, record the request and, if pressure continues, raise it with the audit committee or professional body.',
            'key': f'Principle(s): {s[1]} [1]; effect on users of statements [1]; refuse/escalate appropriately [1] [3]'}


def _eth_c4(r, D):
    c = co(r)
    profit = step(r, 100000, 500000, 1000); target = profit + step(r, 10000, 60000, 1000)
    a1, a2 = step(r, 5000, 40000, 500), step(r, 5000, 40000, 500)
    ca, cl = step(r, 150000, 400000, 1000), step(r, 120000, 350000, 1000)
    pay = step(r, 20000, 80000, 1000)
    intro = (f'The draft profit of {c} is {m(profit)}, below the {m(target)} needed for directors\' bonuses. The sales director proposes: (1) delaying recognition of {m(a1)} of maintenance costs until next year; (2) cutting the allowance for irrecoverable debts by {m(a2)}; '
             f'(3) paying {m(pay)} of trade payables from cash on the last day of the year. Current assets are {m(ca)} and current liabilities {m(cl)} before (3).')
    newp = profit + a1 + a2
    parts = [
        lambda r: ('Calculate the profit if proposals (1) and (2) are adopted, and state whether the bonus target is met.', f'{m(newp)}; target {"met" if newp >= target else "not met"}', f'{m(profit)} + {m(a1)} + {m(a2)} = {m(newp)} [2]; comparison [1] [3]'),
        lambda r: ('Calculate the current ratio before and after proposal (3).', f'{ca / cl:.2f} → {(ca - pay) / (cl - pay):.2f}', '[2]'),
        lambda r: ('Discuss the ethical issues raised by the proposals.', 'Breach of accruals concept and IAS; misleading users; self-interest threat from bonuses; accountant must act with integrity and objectivity and may need to escalate.', '[4]'),
        lambda r: ('Explain how users of the financial statements could be misled.', 'Investors overestimate profit and dividends capacity; lenders misjudge liquidity; future profits will fall when costs are recognised.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t8_4.add('C4', (2, 3, 4, 5), 'multi_step')(_eth_c4)
t8_4.add('C3', (4, 5), 'multi_step')(_eth_c4)
t8_3.add('C4', (3, 4, 5), 'multi_step')(_gear_c4)

CHAPTERS[8] = [t8_1, t8_2, t8_3, t8_4]


# ===================================================================== 9 Activity-based costing
POOLS = [('machine set-ups', 'number of set-ups', 'set-ups'), ('purchasing / ordering', 'number of purchase orders', 'orders'), ('quality inspection', 'number of inspections', 'inspections'),
         ('materials handling', 'number of material movements', 'movements'), ('despatch', 'number of despatches', 'despatches'), ('machine maintenance', 'machine hours', 'machine hours'),
         ('customer service', 'number of customer orders', 'customer orders'), ('engineering changes', 'number of design changes', 'design changes')]


def _abc(r, D):
    pa, pb = r.choice(PRODUCTS)
    npool = 2 if D <= 2 else (3 if D <= 4 else 4)
    pools = r.sample(POOLS, npool)
    qa, qb = r.choice([(5000, 500), (10000, 2000), (20000, 4000), (8000, 1000), (12000, 3000), (40000, 5000)])
    data = []
    for name, drv, unit in pools:
        da, db = r.choice([(10, 40), (20, 30), (5, 45), (30, 70), (15, 60), (40, 160), (100, 300), (25, 75)])
        if unit == 'machine hours':
            da, db = qa * r.choice([1, 2]) // 2, qb * r.choice([1, 2, 3])
        rate = r.choice([80, 100, 120, 150, 200, 250, 300, 400, 500, 750]) if unit != 'machine hours' else r.choice([3, 4, 5, 6, 8, 10])
        data.append((name, drv, unit, da, db, rate * (da + db), rate))
    oa = sum(d[3] * d[6] for d in data); ob = sum(d[4] * d[6] for d in data)
    return dict(pa=pa, pb=pb, qa=qa, qb=qb, data=data, oa=oa, ob=ob, total=oa + ob)


def _abc_text(x):
    return (f'Products {x["pa"]} ({nm(x["qa"])} units) and {x["pb"]} ({nm(x["qb"])} units) share overheads in these cost pools: '
            + '; '.join(f'{d[0]} {m(d[5])} (driver: {d[1]}; {x["pa"]} {nm(d[3])}, {x["pb"]} {nm(d[4])})' for d in x['data']) + '.')


t9_1 = topic('Cost pools and cost drivers', 'cost pools and cost drivers', 'cost pools', 'cost drivers')
fixed(t9_1, 'C1', (1, 2), [
    ('A cost driver is', 'the factor that causes the cost of an activity to be incurred', 'Driver = cause of cost (e.g. number of set-ups) [1].',
     ['the manager responsible for a department', 'the total cost of a product', 'a fixed overhead absorption rate']),
    ('A cost pool is', 'a grouping of overhead costs relating to one activity', 'Cost pool: costs of an activity collected together [1].',
     ['a fund of cash for paying overheads', 'the total of direct costs', 'the budgeted profit']),
    ('The most appropriate cost driver for purchasing department costs is', 'the number of purchase orders placed', 'Ordering costs vary with number of orders [1].',
     ['the number of direct labour hours', 'the floor area', 'the number of units sold']),
    ('The most appropriate cost driver for quality inspection costs is', 'the number of inspections', 'Inspection cost driven by inspections [1].',
     ['the value of materials used', 'machine hours', 'the number of employees']),
    ('Activity-based costing assigns overheads to products', 'according to the activities they consume', 'ABC: cost pools → driver rates → products by driver usage [1].',
     ['in proportion to direct labour hours only', 'equally between products', 'according to selling price']),
])
fixed(t9_1, 'C2', (2, 3, 4), [
    ('Explain why machine set-up costs are better charged on the number of set-ups than on machine hours.', 'Set-up cost depends on how many times machines are set up (batches), not on how long they run; using machine hours would overcharge long-run products and undercharge small batch products.',
     'Cost caused by set-ups [1]; distortion with machine hours [1] [2]'),
    ('Explain the steps in calculating overhead costs using ABC.', 'Identify activities and their cost pools; identify the cost driver for each; calculate a cost driver rate (pool ÷ total driver volume); charge products by their use of each driver.',
     'Activities/pools [1]; drivers [1]; rates [1]; charge to products [1] [4]'),
])


@t9_1.add('C3', (1, 2, 3, 4, 5))
def t91_rate(r, D):
    name, drv, unit = r.choice(POOLS)
    vol = step(r, 50, 2000, 10) if unit != 'machine hours' else step(r, 5000, 60000, 500)
    rate = r.choice([12, 15, 18, 20, 25, 30, 40, 45, 60, 75, 90, 120]) if unit != 'machine hours' else r.choice([1.5, 2, 2.5, 3, 4, 5])
    cost = vol * rate
    c = co(r)
    use = vol * r.choice([1, 2, 3]) // 10
    stem = f'{c} has {name} costs of {m(cost)} for the period. The cost driver is the {drv}, which totals {nm(vol)}.'
    key = f'Rate = {m(cost)} / {nm(vol)} = {m2(rate)} per {unit[:-1] if unit.endswith("s") else unit} [1]' + (f'; product uses {nm(use)} → {m(use * rate)} [1]' if D >= 2 else '')
    if D == 1:
        opts, ans = mm(r, rate, [cost / (vol * 2), rate * 10, vol / cost * 1000, rate * 1.5], f=m2)
        return {'stem': stem + ' What is the cost driver rate?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + f' Calculate the cost driver rate and the {name} cost charged to a product that uses {nm(use)} {unit}.', 'answer': f'{m2(rate)} per {unit[:-1] if unit.endswith("s") else unit}; {m(use * rate)}', 'key': key, 'marks': 2}


@t9_1.add('C2', (2, 3, 4), 'explain')
def t91_match(r, D):
    a, b, cc = r.sample(POOLS, 3)
    return {'stem': f'{co(r)} is introducing ABC. Suggest a suitable cost driver for each of these cost pools and explain one choice: (i) {a[0]}; (ii) {b[0]}; (iii) {cc[0]}.',
            'answer': f'(i) {a[1]}; (ii) {b[1]}; (iii) {cc[1]}. E.g. {a[0]} costs rise with the {a[1]}, so this reflects how products cause the cost.',
            'key': f'(i) {a[1]} [1]; (ii) {b[1]} [1]; (iii) {cc[1]} [1]; explanation of cause-and-effect [1] [4]'}


t9_2 = topic('Calculating product costs using ABC', 'calculating product costs using abc', 'abc product cost', 'activity-based costing')
fixed(t9_2, 'C1', (1, 2), [
    ('The overhead cost per unit under ABC for a product is found by', 'adding the overheads charged from each cost pool and dividing by the units produced', 'Σ(driver usage × rate) / units [1].',
     ['dividing total overheads by total units', 'multiplying labour hours by a single rate', 'dividing selling price by units']),
    ('Under ABC, a low-volume product made in many small batches is likely to have', 'a higher overhead cost per unit than under absorption costing', 'Batch-level costs spread over few units [1].',
     ['a lower overhead cost per unit', 'no overheads charged', 'the same cost as under absorption costing']),
    ('Which cost is a batch-level activity cost?', 'Machine set-up costs', 'Batch-level: set-ups, ordering per batch; unit-level: direct materials [1].',
     ['Direct materials per unit', 'Factory rent', 'Chief executive\'s salary']),
])
fixed(t9_2, 'C2', (2, 3, 4), [
    ('Explain why ABC may give a more accurate product cost than a single blanket overhead rate.', 'It recognises that different products use activities in different proportions and charges overheads according to the causes, rather than assuming all overheads vary with labour or machine hours.',
     'Multiple drivers reflect causes [1]; avoids cross-subsidy [1] [2]'),
    ('Explain how ABC information could be used in pricing decisions.', 'More accurate full costs show which products are under-priced (making losses) or over-priced; prices can be set to cover the true cost plus margin.',
     'Accurate cost base [1]; identify mis-priced products [1] [2]'),
])


@t9_2.add('C3', (1, 2, 3, 4, 5))
def t92_cost(r, D):
    x = _abc(r, D)
    c = co(r)
    stem = f'{c}: ' + _abc_text(x)
    wk = '; '.join(f'{d[0]} rate {m(d[5])}/{nm(d[3] + d[4])} = {m2(d[6])}' for d in x['data'])
    ua, ub = x['oa'] / x['qa'], x['ob'] / x['qb']
    key = f'Rates: {wk} [{len(x["data"])}]; {x["pa"]} {m(x["oa"])}, {x["pb"]} {m(x["ob"])} [1]; per unit {x["pa"]} {m2(ua)}, {x["pb"]} {m2(ub)} [1]'
    if D == 1:
        opts, ans = mm(r, ua, [x['total'] / (x['qa'] + x['qb']), ub, x['oa'] / x['qb'], ua * 2], f=m2)
        return {'stem': stem + f' What is the overhead cost per unit of {x["pa"]} using ABC?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the overhead cost per unit of each product using activity-based costing.'
    if D >= 4:
        dm_a, dm_b = r.choice([8, 10, 12, 15, 20]), r.choice([10, 14, 18, 25])
        dl_a, dl_b = r.choice([6, 8, 10, 12]), r.choice([8, 12, 15, 16])
        q += f' Direct costs per unit are: {x["pa"]} materials ${dm_a}, labour ${dl_a}; {x["pb"]} materials ${dm_b}, labour ${dl_b}. Calculate the full cost per unit of each product.'
        key += f'; full cost {x["pa"]} {m2(ua + dm_a + dl_a)}, {x["pb"]} {m2(ub + dm_b + dl_b)} [1]'
        return {'stem': stem + q, 'answer': f'Overhead per unit {x["pa"]} {m2(ua)}, {x["pb"]} {m2(ub)}; full cost {x["pa"]} {m2(ua + dm_a + dl_a)}, {x["pb"]} {m2(ub + dm_b + dl_b)}', 'key': key, 'marks': len(x['data']) + 3, 'type': 'multi_step'}
    return {'stem': stem + q, 'answer': f'{x["pa"]} {m2(ua)}; {x["pb"]} {m2(ub)}', 'key': key, 'marks': len(x['data']) + 2}


@t9_2.add('C2', (2, 3, 4), 'explain')
def t92_err(r, D):
    x = _abc(r, 2)
    d = x['data'][0]
    wrong = d[5] * Fr(x['qa'], x['qa'] + x['qb'])
    right = d[3] * d[6]
    return {'stem': f'{co(r)} makes {nm(x["qa"])} units of {x["pa"]} and {nm(x["qb"])} units of {x["pb"]}. {d[0].capitalize()} costs of {m(d[5])} are driven by the {d[1]} ({x["pa"]} {nm(d[3])}, {x["pb"]} {nm(d[4])}). A trainee charged {m(wrong)} to {x["pa"]} by sharing the cost in proportion to units produced. Explain the error and calculate the correct charge.',
            'answer': f'Under ABC costs are charged by driver usage, not units. Rate = {m2(d[6])}; {x["pa"]} charge = {nm(d[3])} × {m2(d[6])} = {m(right)}.',
            'key': f'Units are not the driver [1]; rate {m2(d[6])} [1]; correct charge {m(right)} [1] [3]'}


t9_3 = topic('Comparing ABC with traditional absorption costing', 'comparing abc with traditional absorption costing', 'absorption costing', 'traditional costing')
fixed(t9_3, 'C1', (1, 2), [
    ('Traditional absorption costing usually absorbs production overheads using', 'a single rate based on direct labour hours or machine hours', 'Blanket/departmental OAR on volume-related basis [1].',
     ['several cost drivers', 'the number of set-ups', 'selling prices']),
    ('Compared with absorption costing, ABC tends to shift overheads', 'from high-volume products to low-volume, complex products', 'Low-volume products consume more batch/support activities per unit [1].',
     ['from low-volume products to high-volume products', 'from overheads into direct materials', 'out of the product cost altogether']),
    ('A disadvantage of ABC is that it', 'is costly and time-consuming to set up and run', 'Requires data on many activities and drivers [1].',
     ['ignores overheads', 'cannot be used for pricing', 'is not allowed by IAS 2']),
])
fixed(t9_3, 'C2', (2, 3, 4), [
    ('Explain two disadvantages of introducing activity-based costing.', 'High cost of collecting data on activities and drivers; choosing drivers can be subjective; some costs (e.g. rent) have no clear driver; staff may resist change.',
     'Two disadvantages [1 each] + explanation [1 each] [4]'),
    ('Explain why ABC is more relevant in modern manufacturing than traditional absorption costing.', 'Overheads now form a large proportion of cost and are driven by complexity (set-ups, orders, inspections) rather than labour hours, which are a small part of cost in automated factories.',
     'Overheads large/support activities [1]; labour no longer a good basis [1] [2]'),
])


@t9_3.add('C3', (2, 3, 4, 5))
def t93_compare(r, D):
    x = _abc(r, D)
    c = co(r)
    la, lb = r.choice([1, 2, 0.5]), r.choice([1, 2, 3])
    lh = x['qa'] * la + x['qb'] * lb
    oar = x['total'] / lh
    ta, tb = oar * la, oar * lb
    ua, ub = x['oa'] / x['qa'], x['ob'] / x['qb']
    stem = f'{c}: ' + _abc_text(x) + f' Each unit of {x["pa"]} needs {la} direct labour hour{"" if la == 1 else "s"} and each unit of {x["pb"]} needs {lb}. Calculate the overhead cost per unit of each product using (a) a single direct labour hour rate and (b) ABC, and comment on the difference.'
    big = x['pb'] if ub > tb else x['pa']
    return {'stem': stem, 'answer': f'(a) OAR {m2(oar)} per hour: {x["pa"]} {m2(ta)}, {x["pb"]} {m2(tb)} (b) {x["pa"]} {m2(ua)}, {x["pb"]} {m2(ub)}. {big} is undercosted under the traditional method.',
            'key': f'(a) total overheads {m(x["total"])} / {nm(lh)} hours = {m2(oar)} [1]; per unit {m2(ta)}, {m2(tb)} [1] (b) ABC rates and totals [2]; per unit {m2(ua)}, {m2(ub)} [1]; comment: {big} consumes more activities than its labour hours suggest [1]',
            'marks': 6, 'type': 'multi_step'}


def _abc_c4(r, D):
    x = _abc(r, 3)
    c = co(r)
    la, lb = r.choice([1, 2]), r.choice([1, 2, 3])
    lh = x['qa'] * la + x['qb'] * lb
    oar = x['total'] / lh
    ua, ub = x['oa'] / x['qa'], x['ob'] / x['qb']
    ta, tb = oar * la, oar * lb
    dca, dcb = r.choice([20, 25, 30, 40]), r.choice([25, 35, 45, 60])
    pa_ = round((dca + ta) * 1.25); pb_ = round((dcb + tb) * 1.25)
    intro = f'{c} sets prices at full cost plus 25% using a single direct labour hour overhead rate. ' + _abc_text(x) + f' Labour hours per unit: {x["pa"]} {la}, {x["pb"]} {lb}. Direct costs per unit: {x["pa"]} ${dca}, {x["pb"]} ${dcb}. Current prices: {x["pa"]} ${pa_}, {x["pb"]} ${pb_}.'
    parts = [
        lambda r: ('Calculate the overhead cost per unit of each product using the labour hour rate.', f'{x["pa"]} {m2(ta)}; {x["pb"]} {m2(tb)}', f'OAR {m(x["total"])}/{nm(lh)} = {m2(oar)} [1]; per unit [1] [2]'),
        lambda r: ('Calculate the overhead cost per unit of each product using ABC.', f'{x["pa"]} {m2(ua)}; {x["pb"]} {m2(ub)}', 'Driver rates [2]; product totals [1]; per unit [1] [4]'),
        lambda r: ('Calculate the profit or loss per unit of each product at current prices using ABC costs.', f'{x["pa"]} {m2(pa_ - dca - ua)}; {x["pb"]} {m2(pb_ - dcb - ub)}', f'{x["pa"]}: ${pa_} − ${dca} − {m2(ua)} [1]; {x["pb"]}: ${pb_} − ${dcb} − {m2(ub)} [1] [2]'),
        lambda r: ('Advise the directors whether they should adopt ABC for pricing.', 'ABC reveals cross-subsidy between products; adopt if benefits of better pricing exceed the cost of the system; consider competitors\' prices and market reaction.', 'Uses results [2]; cost/benefit of ABC [1]; recommendation [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


for _t in (t9_1, t9_2, t9_3):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_abc_c4)
t9_3.add('C3', (4, 5), 'multi_step')(_abc_c4)
t9_1.add('C3', (4, 5), 'multi_step')(_abc_c4)


@t9_3.add('C2', (2, 3, 4), 'explain')
def t93_claim(r, D):
    pa, pb = r.choice(PRODUCTS)
    return {'stem': f'The production manager of {co(r)} says: "Our low-volume product {pb} looks very profitable under absorption costing, so we should make more of it." The product is made in many small batches and needs frequent inspections. Explain why ABC might change this conclusion.',
            'answer': f'{pb} causes many set-ups and inspections; absorption costing spreads these over labour hours, under-costing {pb} and over-costing {pa}. ABC may show {pb} is much less profitable or loss-making.',
            'key': 'Batch-level costs not linked to labour hours [1]; under-costing of low-volume product [1]; possible change in decision [1] [3]'}


CHAPTERS[9] = [t9_1, t9_2, t9_3]


# ===================================================================== 10 Budgeting and budgetary control
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

t10_1 = topic('Purpose of budgets and the budgeting process', 'purpose of budgets and the budgeting process', 'purpose of budgets', 'budgeting process', 'principal budget factor')
fixed(t10_1, 'C1', (1, 2), [
    ('The principal budget factor is', 'the factor that limits the activities of the business and is budgeted first', 'Limiting factor, often sales demand [1].',
     ['the largest expense in the budget', 'the budgeted profit', 'the cash balance at the year end']),
    ('Which is NOT a purpose of budgeting?', 'Guaranteeing that the business will make a profit', 'Purposes: planning, coordination, communication, control, motivation [1].',
     ['Planning future activities', 'Coordinating departments', 'Controlling costs by comparison with actual results']),
    ('Zero-based budgeting means', 'each budget is built from zero and every item must be justified', 'ZBB: no automatic base from last year [1].',
     ['last year\'s budget is increased by inflation', 'budgets are set at zero profit', 'only fixed costs are budgeted']),
    ('Participative (bottom-up) budgeting involves', 'managers who will be responsible for the budget helping to prepare it', 'Participation improves motivation and realism [1].',
     ['senior managers imposing budgets', 'the auditor setting the budget', 'only the sales department']),
    ('A master budget consists of', 'the budgeted income statement, budgeted statement of financial position and cash budget', 'Master budget summarises functional budgets [1].',
     ['the sales budget only', 'the actual financial statements', 'the standard cost card']),
])
fixed(t10_1, 'C2', (2, 3, 4), [
    ('Explain two benefits of involving departmental managers in setting budgets.', 'Managers have detailed knowledge so budgets are more realistic; they are more motivated to achieve targets they helped set.',
     'Two benefits [1 each] + explanation [1 each] [4]'),
    ('Explain the term "budgetary slack" and why it may arise.', 'Slack is deliberate overestimation of costs or underestimation of revenue so that targets are easier to achieve; it arises in participative budgeting when managers are judged against budgets.',
     'Definition [1]; cause [1] [2]'),
    ('Distinguish between incremental budgeting and zero-based budgeting.', 'Incremental adjusts last year\'s budget for expected changes (quick but carries forward inefficiency); ZBB justifies every activity from zero (removes waste but time-consuming).',
     'Incremental defined + evaluation [1]; ZBB defined + evaluation [1] [2]'),
    ('Explain why the principal budget factor must be identified first.', 'All other budgets depend on it; e.g. if sales demand limits activity, production, purchases and labour budgets are derived from the sales budget.',
     'Limits activity [1]; other budgets derive from it [1] [2]'),
])


@t10_1.add('C3', (1, 2, 3, 4, 5))
def t101_pbf(r, D):
    c = co(r); p = r.choice(['kayaks', 'school desks', 'solar panels', 'water tanks', 'bicycles', 'printers'])
    demand = step(r, 8000, 40000, 500)
    mh_u, lh_u, mat_u = r.choice([1, 2, 3]), r.choice([2, 3, 4]), r.choice([3, 4, 5, 6])
    mh = demand * mh_u * r.uniform(0.7, 1.3); lh = demand * lh_u * r.uniform(0.7, 1.3); mat = demand * mat_u * r.uniform(0.7, 1.3)
    mh, lh, mat = round(mh / 100) * 100, round(lh / 100) * 100, round(mat / 100) * 100
    caps = {'sales demand': demand, 'machine hours': mh // mh_u, 'labour hours': lh // lh_u, 'material': mat // mat_u}
    lim = min(caps, key=caps.get)
    stem = (f'{c} makes {p}. Next year: sales demand {nm(demand)} units; machine hours available {nm(mh)} ({mh_u} per unit); labour hours available {nm(lh)} ({lh_u} per unit); material available {nm(mat)} kg ({mat_u} kg per unit). '
            'Identify the principal budget factor and the maximum number of units that can be budgeted.')
    key = ', '.join(f'{k} {nm(v)} units' for k, v in caps.items()) + f' [2]; principal budget factor: {lim}, {nm(caps[lim])} units [1]'
    if D == 1:
        opts, ans = mcq(r, lim, [k for k in caps if k != lim] + ['cash'])
        return {'stem': stem.replace(' and the maximum number of units that can be budgeted', '').replace('Identify the', 'Which is the') + '?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem, 'answer': f'{lim.capitalize()}: {nm(caps[lim])} units', 'key': key, 'marks': 3}


@t10_1.add('C2', (2, 3, 4), 'explain')
def t101_scen(r, D):
    c = co(r)
    s = r.choice([('Budgets are set by the managing director and sent to departments without discussion.', 'Imposed budgets can demotivate managers and be unrealistic; use participation.'),
                  ('The sales manager is rewarded for beating the sales budget that she sets herself.', 'Encourages budgetary slack; set targets jointly and review against market data.'),
                  ('Every department\'s budget is last year\'s actual spending plus 5%.', 'Incremental approach carries forward inefficiency; consider zero-based budgeting for discretionary costs.'),
                  ('Actual results are compared with budget only once a year.', 'Too late for corrective action; monthly variance reports needed.'),
                  ('The production budget was prepared before the sales budget.', 'Sales demand is usually the principal budget factor; production should follow the sales budget.')])
    return {'stem': f'At {c}: "{s[0]}" Explain the weakness in this budgeting practice and recommend an improvement.', 'answer': s[1], 'key': 'Weakness identified [1]; consequence explained [1]; improvement [1] [3]'}


t10_2 = topic('Functional budgets: sales, production, purchases, labour', 'functional budgets: sales, production, purchases, labour', 'functional budgets', 'production budget', 'purchases budget')
fixed(t10_2, 'C1', (1, 2), [
    ('Budgeted production equals', 'budgeted sales + closing inventory of finished goods − opening inventory of finished goods', 'Production = sales + closing FG − opening FG [1].',
     ['budgeted sales − closing inventory + opening inventory', 'budgeted sales only', 'opening inventory + closing inventory']),
    ('The materials purchases budget (in kg) equals', 'materials needed for production + closing materials inventory − opening materials inventory', 'Purchases = usage + closing − opening [1].',
     ['production units × selling price', 'materials needed − closing inventory + opening inventory', 'opening inventory − usage']),
    ('Which budget is normally prepared first when sales demand is the limiting factor?', 'The sales budget', 'Sales budget first [1].',
     ['The cash budget', 'The purchases budget', 'The labour budget']),
    ('The labour budget is calculated from', 'budgeted production × labour hours per unit × rate per hour', 'Labour cost = production × hours × rate [1].',
     ['budgeted sales × selling price', 'total overheads ÷ labour hours', 'the number of employees only']),
])
fixed(t10_2, 'C2', (2, 3, 4), [
    ('Explain why a business may budget to hold closing inventory of finished goods.', 'To meet unexpected demand and avoid lost sales; to allow smooth production; but inventory has holding costs.',
     'Buffer for demand [1]; smooth production/cost noted [1] [2]'),
    ('Explain how the functional budgets are linked to one another.', 'The sales budget determines production; production determines materials usage, purchases and labour; all feed the cash budget and master budget.',
     'Sales → production [1]; production → materials/labour [1]; all → cash/master [1] [3]'),
])


@t10_2.add('C3', (1, 2, 3, 4, 5))
def t102_prod(r, D):
    c = co(r)
    n = 1 if D <= 2 else 3
    ms = r.sample(range(12), 1)[0]
    mons = [MONTHS[(ms + i) % 12] for i in range(n + 1)]
    sales = [step(r, 2000, 12000, 100) for _ in range(n + 1)]
    pct = r.choice([10, 20, 25, 30, 40, 50])
    open0 = step(r, 200, 3000, 50)
    prods, wk = [], []
    o = open0
    for i in range(n):
        cl = sales[i + 1] * pct // 100
        pr = sales[i] + cl - o
        prods.append(pr); wk.append(f'{mons[i]}: {nm(sales[i])} + {nm(cl)} − {nm(o)} = {nm(pr)}')
        o = cl
    stem = (f'{c} budgets sales of ' + ', '.join(f'{nm(s)} units in {mm_}' for s, mm_ in zip(sales, mons)) + f'. Closing inventory of finished goods each month is to be {pct}% of the following month\'s sales. Inventory at the start of {mons[0]} is {nm(open0)} units.')
    key = '; '.join(wk) + f' [{n + 1}]'
    if D == 1:
        opts, ans = num_mcq(r, prods[0], [sales[0] - sales[1] * pct // 100 + open0, sales[0], sales[0] + sales[1] * pct // 100, sales[0] + sales[1] * pct // 100 + open0], fmtf=nm)
        return {'stem': stem + f' What is budgeted production for {mons[0]}?', 'options': opts, 'answer': ans + ' units' if False else ans, 'key': key}
    mat = ''
    if D >= 4:
        kg = r.choice([2, 3, 4]); price = r.choice([2.5, 4, 5, 6, 8])
        mat_open = step(r, 500, 5000, 100); mat_cl = step(r, 500, 5000, 100)
        use = prods[0] * kg; buy = use + mat_cl - mat_open
        stem += f' Each unit uses {kg} kg of material at ${price} per kg; material inventory is {nm(mat_open)} kg at the start and {nm(mat_cl)} kg at the end of {mons[0]}.'
        mat = f'; {mons[0]} purchases: {nm(use)} + {nm(mat_cl)} − {nm(mat_open)} = {nm(buy)} kg × ${price} = {m(buy * price)} [2]'
        return {'stem': stem + f' Prepare the production budget for {", ".join(mons[:n])} and the materials purchases budget (kg and $) for {mons[0]}.', 'answer': '; '.join(f'{mm_} {nm(p)} units' for mm_, p in zip(mons, prods)) + f'; purchases {nm(buy)} kg, {m(buy * price)}', 'key': key + mat, 'marks': n + 3, 'type': 'multi_step'}
    return {'stem': stem + ' Prepare the production budget for ' + (', '.join(mons[:n]) if n > 1 else mons[0]) + '.', 'answer': '; '.join(f'{mm_} {nm(p)} units' for mm_, p in zip(mons, prods)), 'key': key, 'marks': n + 1}


@t10_2.add('C3', (2, 3, 4, 5))
def t102_labour(r, D):
    c = co(r)
    prod = step(r, 2000, 20000, 100); hrs = r.choice([0.5, 1, 1.5, 2, 2.5, 3]); rate = r.choice([9, 10, 12, 14, 15, 18, 20])
    idle = r.choice([0, 0, 5, 10]) if D >= 3 else 0
    prem = r.choice([0, 25, 50]) if D >= 4 else 0
    need = prod * hrs
    paid = need / (1 - idle / 100) if idle else need
    normal = step(r, int(paid * 0.8), int(paid * 0.95), 10) if prem else paid
    ot = paid - normal if prem else 0
    cost = normal * rate + ot * rate * (1 + prem / 100)
    stem = f'{c} plans to produce {nm(prod)} units. Each unit needs {hrs} direct labour hour{"" if hrs == 1 else "s"}, paid at ${rate} per hour.' + (f' {idle}% of hours paid are expected to be idle time.' if idle else '') + (f' Only {nm(normal)} hours are available at the normal rate; the rest is overtime at a premium of {prem}%.' if prem else '') + ' Prepare the direct labour budget in hours and $.'
    key = f'Productive hours {nm(prod)} × {hrs} = {nm(need)} [1]' + (f'; hours paid = {nm(need)} / {(100 - idle) / 100:.2f} = {nm(paid)} [1]' if idle else '') + (f'; overtime {nm(ot)} h × ${rate * (1 + prem / 100):.2f} [1]' if prem else '') + f'; cost {m(cost)} [1]'
    return {'stem': stem, 'answer': f'{nm(paid)} hours; {m(cost)}', 'key': key, 'marks': 2 + bool(idle) + bool(prem)}


@t10_2.add('C2', (2, 3, 4), 'explain')
def t102_err(r, D):
    s, cl, op = step(r, 3000, 15000, 100), step(r, 200, 2000, 50), step(r, 200, 2000, 50)
    return {'stem': f'A trainee at {co(r)} calculated budgeted production as {nm(s)} − {nm(cl)} + {nm(op)} = {nm(s - cl + op)} units, where {nm(s)} is budgeted sales, {nm(cl)} closing inventory and {nm(op)} opening inventory. Explain the error and calculate the correct figure.',
            'answer': f'Closing inventory must be added (it has to be produced) and opening inventory deducted (already available). Production = {nm(s)} + {nm(cl)} − {nm(op)} = {nm(s + cl - op)} units.',
            'key': f'Reversed treatment identified [1]; reason [1]; {nm(s + cl - op)} units [1] [3]'}


t10_3 = topic('Cash budgets and master budget', 'cash budgets and master budget', 'cash budget', 'master budget')
fixed(t10_3, 'C1', (1, 2), [
    ('Which item does NOT appear in a cash budget?', 'Depreciation of equipment', 'Depreciation is a non-cash expense [1].',
     ['Receipts from credit customers', 'Payment for a new machine', 'Wages paid']),
    ('If 60% of sales are on one month\'s credit, the cash received in March from credit customers relates to', 'credit sales made in February', 'One-month lag [1].',
     ['credit sales made in March', 'credit sales made in April', 'cash sales in March']),
    ('A cash budget helps a business to', 'identify periods when it will need an overdraft or have surplus cash', 'Plan financing and investment of surpluses [1].',
     ['calculate profit for the year', 'value its inventory', 'calculate depreciation']),
    ('A cash discount of 2% allowed to customers who pay immediately will', 'reduce the cash received from those sales', 'Receipts = sales × 98% for those customers [1].',
     ['increase the cash received', 'have no effect on the cash budget', 'be shown as a payment to suppliers']),
])
fixed(t10_3, 'C2', (2, 3, 4), [
    ('Explain why profit and cash budgets show different results.', 'Profit uses accruals (credit sales/purchases, depreciation), whereas cash records timing of receipts and payments, including capital items and loans not in profit.',
     'Accruals vs cash timing [1]; examples [1] [2]'),
    ('Explain two actions a business could take if its cash budget shows a deficit.', 'Arrange an overdraft or short-term loan; delay capital expenditure; chase receivables or offer discounts; negotiate longer credit from suppliers.',
     'Two actions [1 each] + explanation [1 each] [4]'),
    ('Explain how a cash budget links to the master budget.', 'The cash budget draws on the sales, purchases, labour and capital expenditure budgets; its closing balance becomes the bank figure in the budgeted statement of financial position.',
     'Uses functional budgets [1]; closing balance to budgeted SOFP [1] [2]'),
    ('Explain why a business with a budgeted profit may still forecast an overdraft.', 'Cash may be tied up in receivables and inventory, spent on non-current assets or loan repayments, or suppliers paid before customers pay.',
     'Timing differences [1]; capital/loan items [1] [2]'),
])


@t10_3.add('C2', (1, 2, 3, 4), 'explain')
def t103_err(r, D):
    x = _cash(r, 3)
    mn = x['rows'][0][0]
    s = x['sales']
    wrong = s[2] * (x['cashp'] + x['c1'] + x['c2']) / 100
    rec = x['rows'][0][1]
    e = r.choice(['dep', 'rec'])
    if e == 'dep':
        return {'stem': f'A draft cash budget of {co(r)} for {mn} shows payments of {m(x["rows"][0][2] + x["dep"])}, which include depreciation of {m(x["dep"])}. Explain the error and state the corrected payments and its effect on the closing balance.',
                'answer': f'Depreciation is a non-cash expense and must be excluded. Payments should be {m(x["rows"][0][2])}; the closing balance rises by {m(x["dep"])}.',
                'key': f'Non-cash item [1]; payments {m(x["rows"][0][2])} [1]; closing balance +{m(x["dep"])} [1] [3]'}
    return {'stem': f'{co(r)} sells {x["cashp"]}% of goods for cash and the rest on credit (' + f'{x["c1"]}% paid one month later' + (f', {x["c2"]}% two months later' if x['c2'] else '') + f'). Sales were {", ".join(m(v) for v in s[:3])} for {", ".join(x["mons"][:3])}' + (f'; cash customers receive a {x["disc"]}% discount' if x['disc'] else '') + f'. A trainee shows receipts of {m(wrong)} for {mn}, equal to {mn} sales. Explain the error and calculate the correct receipts.',
            'answer': f'Receipts depend on when customers pay, not when sales are made. Correct receipts for {mn} = {m(rec)}.',
            'key': f'Timing of credit receipts [1]; correct pattern applied [1]; {m(rec)} [1] [3]'}


def _cash(r, D):
    start = r.randrange(12)
    mons = [MONTHS[(start + i) % 12] for i in range(5)]
    sales = [step(r, 20000, 90000, 1000) for _ in range(5)]
    cashp = r.choice([10, 20, 25, 30]); disc = r.choice([0, 2, 2.5]) if D >= 3 else 0
    c1 = r.choice([40, 50, 60]); c2 = 100 - cashp - c1
    if c2 < 0:
        c1 = 100 - cashp; c2 = 0
    gm = r.choice([25, 30, 40]); purch = [s * (100 - gm) // 100 for s in sales]
    wages = step(r, 5000, 20000, 500); oh = step(r, 3000, 12000, 500); dep = step(r, 1000, 4000, 100)
    capex = step(r, 10000, 40000, 1000) if D >= 2 else 0
    open_ = step(r, -10000, 25000, 500)
    rows = []
    bal = open_
    for i in (2, 3, 4):
        rec = int(_hu(sales[i] * cashp / 100 * (1 - disc / 100) + sales[i - 1] * c1 / 100 + sales[i - 2] * c2 / 100))
        pay = purch[i - 1] + wages + oh + (capex if i == 3 else 0)
        bal2 = bal + rec - pay
        rows.append((mons[i], rec, pay, bal, bal2))
        bal = bal2
    return dict(mons=mons, sales=sales, cashp=cashp, disc=disc, c1=c1, c2=c2, gm=gm, purch=purch, wages=wages, oh=oh, dep=dep, capex=capex, open=open_, rows=rows)


def _cash_text(x):
    return (f'Budgeted sales: ' + ', '.join(f'{mm_} {m(s)}' for mm_, s in zip(x['mons'], x['sales'])) + f'. {x["cashp"]}% of sales are for cash' + (f' (customers receive a {x["disc"]}% cash discount)' if x['disc'] else '')
            + f', {x["c1"]}% are received in the month after sale' + (f' and {x["c2"]}% two months after sale' if x['c2'] else '') + f'. Purchases are made at a gross margin of {x["gm"]}% (purchases = cost of sales of the same month) and paid one month later. '
            f'Monthly wages {m(x["wages"])}, other expenses {m(x["oh"])} paid in the month, depreciation {m(x["dep"])} a month.' + (f' A machine costing {m(x["capex"])} will be paid for in {x["mons"][3]}.' if x['capex'] else '')
            + f' The bank balance at the start of {x["mons"][2]} is {m(x["open"]) if x["open"] >= 0 else "an overdraft of " + m(-x["open"])}.')


t10_3_list = []


@t10_3.add('C3', (1, 2, 3, 4, 5))
def t103_cash(r, D):
    x = _cash(r, D)
    stem = _cash_text(x)
    mn, rec, pay, ob, cb = x['rows'][0]
    s = x['sales']
    rk = f'{mn} receipts: cash {x["cashp"]}% × {m(s[2])}' + (f' × {1 - x["disc"] / 100:.3f}' if x['disc'] else '') + f' + {x["c1"]}% × {m(s[1])}' + (f' + {x["c2"]}% × {m(s[0])}' if x['c2'] else '') + f' = {m(rec)} [2]'
    if D == 1:
        opts, ans = mm(r, rec, [s[2], s[2] * (x['cashp'] + x['c1']) / 100, rec + s[0] * 0.1, s[1] * x['c1'] / 100 + s[2] * x['cashp'] / 100 + 5000])
        return {'stem': stem + f' What are the total receipts from customers in {mn}?', 'options': opts, 'answer': ans, 'key': rk}
    if D <= 3:
        return {'stem': stem + f' Calculate the receipts, the payments and the closing bank balance for {mn}.', 'answer': f'Receipts {m(rec)}; payments {m(pay)}; closing balance {m(cb)}',
                'key': rk + f'; payments: purchases {m(x["purch"][1])} + wages {m(x["wages"])} + expenses {m(x["oh"])} = {m(pay)} [1]; depreciation excluded [1]; closing {m(ob)} + {m(rec)} − {m(pay)} = {m(cb)} [1]', 'marks': 5}
    rows = x['rows']
    return {'stem': stem + f' Prepare the cash budget for {rows[0][0]}, {rows[1][0]} and {rows[2][0]}.', 'answer': '; '.join(f'{mn_}: receipts {m(a)}, payments {m(b)}, closing {m(d)}' for mn_, a, b, _, d in rows),
            'key': '; '.join(f'{mn_} receipts {m(a)}, payments {m(b)}' for mn_, a, b, _, _ in rows) + ' [2 per month]; capital payment in ' + x['mons'][3] + ', depreciation excluded [1]; balances ' + ', '.join(m(d) for *_, d in rows) + ' [1]', 'marks': 8, 'type': 'multi_step'}


def _cash_c4(r, D):
    x = _cash(r, 4)
    intro = f'{co(r)} is preparing its cash budget. ' + _cash_text(x)
    rows = x['rows']
    low = min(rows, key=lambda t: t[4])
    parts = [
        lambda r: (f'Prepare the cash budget for {rows[0][0]}, {rows[1][0]} and {rows[2][0]}.', '; '.join(f'{mn_}: closing {m(d)}' for mn_, a, b, _, d in rows), '; '.join(f'{mn_} receipts {m(a)}, payments {m(b)}' for mn_, a, b, _, _ in rows) + ' [6]; closing balances [2] [8]'),
        lambda r: (f'Calculate the receipts from customers for {rows[1][0]}.', m(rows[1][1]), f'Using the {x["cashp"]}%/{x["c1"]}%' + (f'/{x["c2"]}%' if x['c2'] else '') + ' pattern [2] [2]'),
        lambda r: ('Explain why depreciation is excluded from the cash budget.', 'It is a non-cash expense; the cash outflow occurred when the asset was bought.', '[2]'),
        lambda r: ('Advise the business on how to deal with its lowest forecast balance.', f'Lowest balance {m(low[4])} in {low[0]}: ' + ('arrange an overdraft facility or delay the machine purchase/chase receivables' if low[4] < 0 else 'surplus could be invested short-term or used to pay suppliers early for discounts'), 'Identifies month and figure [1]; two suitable actions [2]; justified [1] [4]'),
        lambda r: (f'Evaluate the effect on cash if customers paying in the month after sale were offered a {r.choice([2, 3])}% discount to pay immediately instead.', 'Cash arrives a month earlier, improving liquidity, but total receipts fall by the discount; worthwhile if the overdraft cost saved exceeds the discount.', '[3]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t10_3.add('C4', (2, 3, 4, 5), 'multi_step')(_cash_c4)
t10_3.add('C3', (4, 5), 'multi_step')(_cash_c4)


@t10_3.add('C3', (3, 4, 5))
def t103_master(r, D):
    c = co(r)
    rev = step(r, 300000, 1200000, 10000); gm = r.choice([30, 35, 40]); exp = step(r, 30000, 150000, 1000); dep = step(r, 10000, 50000, 1000)
    gp = rev * gm // 100; np_ = gp - exp - dep
    rec0, rec_days = step(r, 20000, 100000, 1000), r.choice([30, 45, 60])
    rec1 = round(rev * rec_days / 365)
    cash_in = rev + rec0 - rec1
    return {'stem': f'In the master budget of {c}: revenue {m(rev)} (all on credit), gross margin {gm}%, cash expenses {m(exp)}, depreciation {m(dep)}. Trade receivables at the start of the year are {m(rec0)} and are budgeted to equal {rec_days} days\' sales at the year end. Calculate the budgeted profit for the year, the closing trade receivables and the cash received from customers.',
            'answer': f'Profit {m(np_)}; closing receivables {m(rec1)}; cash received {m(cash_in)}',
            'key': f'Gross profit {m(gp)} − {m(exp)} − {m(dep)} = {m(np_)} [1]; receivables {m(rev)} × {rec_days}/365 = {m(rec1)} [1]; cash {m(rev)} + {m(rec0)} − {m(rec1)} = {m(cash_in)} [1]', 'marks': 3}


t10_4 = topic('Flexible budgets and budgetary control', 'flexible budgets and budgetary control', 'flexible budget', 'budgetary control')
fixed(t10_4, 'C1', (1, 2), [
    ('A flexible budget is', 'a budget adjusted to the actual level of activity achieved', 'Flexed for actual output; variable costs change, fixed costs do not [1].',
     ['a budget that is never revised', 'a budget prepared for one level of activity only', 'the cash budget']),
    ('When flexing a budget, fixed costs', 'remain at the original budgeted amount', 'Fixed costs do not vary with activity [1].',
     ['increase in proportion to output', 'are excluded', 'are halved']),
    ('Budgetary control involves', 'comparing actual results with budget, investigating variances and taking corrective action', 'Control cycle [1].',
     ['preparing the budget only', 'auditing the financial statements', 'setting selling prices']),
    ('Management by exception means', 'concentrating attention on significant variances from budget', 'Investigate only significant variances [1].',
     ['managers ignore all variances', 'every variance is investigated equally', 'budgets are not prepared']),
])
fixed(t10_4, 'C2', (2, 3, 4), [
    ('Explain why comparing actual costs with a fixed (original) budget may be misleading.', 'If actual output differs from budget, variable costs will naturally differ; a flexible budget compares like with like, showing true efficiency.',
     'Activity level differs [1]; flexed budget gives meaningful comparison [1] [2]'),
    ('Explain two behavioural problems of budgetary control.', 'Budgets seen as pressure may demotivate; managers may build in slack or spend to avoid cuts; focus on short-term targets at the expense of quality.',
     'Two problems [1 each] + explanation [1 each] [4]'),
])


@t10_4.add('C3', (1, 2, 3, 4, 5))
def t104_flex(r, D):
    c = co(r)
    bu = step(r, 5000, 30000, 500)
    au = round(bu * r.choice([0.8, 0.85, 0.9, 1.1, 1.15, 1.2]) / 100) * 100
    sp = r.choice([20, 25, 30, 40, 50]); mat = r.choice([4, 5, 6, 8]); lab = r.choice([3, 4, 5, 6]); fix = step(r, 20000, 100000, 1000)
    a_rev = au * (sp + r.choice([-1, 0, 1])); a_mat = round(au * mat * r.uniform(0.95, 1.08)); a_lab = round(au * lab * r.uniform(0.95, 1.08)); a_fix = fix + step(r, -4000, 6000, 500)
    f_rev, f_mat, f_lab = au * sp, au * mat, au * lab
    f_prof = f_rev - f_mat - f_lab - fix; a_prof = a_rev - a_mat - a_lab - a_fix
    stem = (f'{c} budgeted to sell {nm(bu)} units at ${sp} with variable costs per unit of materials ${mat} and labour ${lab}, and fixed costs of {m(fix)}. Actual sales were {nm(au)} units: revenue {m(a_rev)}, materials {m(a_mat)}, labour {m(a_lab)}, fixed costs {m(a_fix)}.')
    var = [('revenue', a_rev - f_rev), ('materials', f_mat - a_mat), ('labour', f_lab - a_lab), ('fixed costs', fix - a_fix)]
    key = f'Flexed at {nm(au)} units: revenue {m(f_rev)}, materials {m(f_mat)}, labour {m(f_lab)}, fixed {m(fix)}, profit {m(f_prof)} [2]; variances ' + ', '.join(f'{a} {fa(v)}' for a, v in var) + f' [2]; total {fa(a_prof - f_prof)} [1]'
    if D == 1:
        opts, ans = mm(r, f_prof, [bu * (sp - mat - lab) - fix, a_prof, au * (sp - mat - lab), f_prof + fix // 2])
        return {'stem': stem + ' What is the flexed budget profit?', 'options': opts, 'answer': ans, 'key': key}
    if D == 2:
        return {'stem': stem + ' Calculate the flexed budget profit and the total variance from it.', 'answer': f'Flexed profit {m(f_prof)}; actual {m(a_prof)}; variance {fa(a_prof - f_prof)}', 'key': key, 'marks': 3}
    return {'stem': stem + ' Prepare a flexible budget statement and calculate the variance for each item, labelling each F or A.', 'answer': f'Flexed profit {m(f_prof)}; ' + ', '.join(f'{a} {fa(v)}' for a, v in var) + f'; total {fa(a_prof - f_prof)}', 'key': key, 'marks': 5, 'type': 'multi_step'}


def _flex_c4(r, D):
    c = co(r)
    bu = step(r, 8000, 30000, 1000); au = round(bu * r.choice([0.8, 0.9, 1.1, 1.25]) / 100) * 100
    sp = r.choice([30, 40, 50, 60]); vc = r.choice([12, 15, 18, 22]); fix = step(r, 40000, 150000, 1000)
    a_rev = au * sp - step(r, -10000, 20000, 500); a_vc = round(au * vc * r.uniform(0.95, 1.1)); a_fix = fix + step(r, -5000, 8000, 500)
    o_prof = bu * (sp - vc) - fix; f_prof = au * (sp - vc) - fix; a_prof = a_rev - a_vc - a_fix
    intro = f'{c} set an original budget for {nm(bu)} units at ${sp} each, variable cost ${vc} per unit and fixed costs {m(fix)}. Actual results: {nm(au)} units sold, revenue {m(a_rev)}, variable costs {m(a_vc)}, fixed costs {m(a_fix)}. The manager claims: "Profit is {"above" if a_prof > o_prof else "below"} budget, so cost control was {"good" if a_prof > o_prof else "poor"}."'
    parts = [
        lambda r: ('Calculate the original budget profit, the flexed budget profit and the actual profit.', f'{m(o_prof)}; {m(f_prof)}; {m(a_prof)}', '[3]'),
        lambda r: ('Calculate the sales volume variance (original vs flexed profit) and the total flexible budget variance.', f'Volume {fa(f_prof - o_prof)}; flexible budget variance {fa(a_prof - f_prof)}', '[2]'),
        lambda r: ('Calculate the revenue, variable cost and fixed cost variances against the flexed budget.', f'Revenue {fa(a_rev - au * sp)}; variable costs {fa(au * vc - a_vc)}; fixed {fa(fix - a_fix)}', '[3]'),
        lambda r: ('Evaluate the manager\'s claim.', f'The fixed-budget comparison mixes volume and efficiency. Against the flexed budget, cost performance is {fa(au * vc - a_vc + fix - a_fix)}, so the claim is ' + ('supported.' if (au * vc - a_vc + fix - a_fix > 0) == (a_prof > o_prof) else 'not supported.'), 'Uses flexed figures [2]; separates volume from cost control [1]; conclusion [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t10_4.add('C4', (2, 3, 4, 5), 'multi_step')(_flex_c4)
t10_4.add('C3', (4, 5), 'multi_step')(_flex_c4)
for _t in (t10_1, t10_2):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_cash_c4)
t10_2.add('C4', (3, 4, 5), 'multi_step')(_flex_c4)
t10_1.add('C3', (4, 5), 'multi_step')(_flex_c4)


@t10_4.add('C2', (2, 3, 4), 'explain')
def t104_err(r, D):
    c = co(r)
    bu = step(r, 5000, 20000, 500); au = bu + step(r, 1000, 5000, 500); vc = r.choice([6, 8, 10, 12])
    act = round(au * vc * r.uniform(0.96, 1.04))
    return {'stem': f'{c} budgeted material costs of {m(bu * vc)} for {nm(bu)} units (${vc} per unit). Actual output was {nm(au)} units and material cost {m(act)}. The production manager was criticised for an adverse variance of {m(act - bu * vc)}. Explain why this criticism may be unfair and calculate a fairer variance.',
            'answer': f'The budget should be flexed to actual output: {nm(au)} × ${vc} = {m(au * vc)}. Fair variance = {fa(au * vc - act)}.',
            'key': f'Fixed budget compares different activity levels [1]; flexed budget {m(au * vc)} [1]; variance {fa(au * vc - act)} [1] [3]'}


CHAPTERS[10] = [t10_1, t10_2, t10_3, t10_4]


# ===================================================================== 11 Standard costing and variances
def _std(r, D):
    p = r.choice(['a garden bench', 'a school bag', 'a ceramic tile pack', 'a bottle of juice concentrate', 'a pair of sandals', 'a wooden toy', 'a solar lamp', 'a carton of yoghurt'])
    kg = r.choice([2, 2.5, 3, 4, 5, 6]); sp_ = r.choice([1.5, 2, 2.5, 3, 4, 5, 6, 8])
    hrs = r.choice([0.5, 1, 1.5, 2, 3]); sr = r.choice([8, 9, 10, 12, 14, 15, 16, 18, 20])
    out = step(r, 1000, 12000, 100)
    aq = round(out * kg * r.uniform(0.93, 1.08))
    ap = round(sp_ * r.uniform(0.9, 1.1), 2)
    if ap == sp_:
        ap = round(sp_ + 0.1, 2)
    ah = round(out * hrs * r.uniform(0.92, 1.09))
    ar = round(sr * r.uniform(0.92, 1.08), 2)
    if ar == sr:
        ar = round(sr - 0.25, 2)
    sq, sh = out * kg, out * hrs
    v = dict(mp=(sp_ - ap) * aq, mu=(sq - aq) * sp_, lr=(sr - ar) * ah, le=(sh - ah) * sr)
    v['mt'] = sq * sp_ - aq * ap; v['lt'] = sh * sr - ah * ar
    return dict(p=p, kg=kg, sp=sp_, hrs=hrs, sr=sr, out=out, aq=aq, ap=ap, ah=ah, ar=ar, sq=sq, sh=sh, v=v)


def _std_text(x, mat=True, lab=True):
    t = f'The standard cost card for {x["p"]} shows'
    bits = []
    if mat:
        bits.append(f'direct materials {x["kg"]} kg at ${x["sp"]:.2f} per kg')
    if lab:
        bits.append(f'direct labour {x["hrs"]} hour{"" if x["hrs"] == 1 else "s"} at ${x["sr"]:.2f} per hour')
    t += ' ' + ' and '.join(bits) + f'. Actual output was {nm(x["out"])} units.'
    if mat:
        t += f' {nm(x["aq"])} kg of material were bought and used at a total cost of {m2(x["aq"] * x["ap"])}.'
    if lab:
        t += f' {nm(x["ah"])} labour hours were worked and paid, costing {m2(x["ah"] * x["ar"])}.'
    return t


t11_1 = topic('Setting standard costs', 'setting standard costs', 'standard cost', 'standard cost card')
fixed(t11_1, 'C1', (1, 2), [
    ('An ideal standard is one that', 'assumes perfect operating conditions with no waste or idle time', 'Ideal: no allowance for inefficiency; attainable: allows normal losses [1].',
     ['can be achieved with normal effort and allows for normal losses', 'is based on last year\'s actual costs', 'is never revised']),
    ('An attainable standard', 'can be achieved under efficient operating conditions with allowances for normal losses and breaks', 'Attainable standards motivate [1].',
     ['assumes no machine breakdowns or waste ever', 'is the same as actual cost', 'ignores labour costs']),
    ('A standard cost is', 'a predetermined estimate of the cost of one unit of output', 'Standard = planned cost per unit [1].',
     ['the actual cost of the last unit made', 'the market price of a product', 'the total budgeted cost for the year']),
    ('Information for setting the standard price of materials would most likely come from', 'the purchasing department and suppliers\' price lists', 'Purchasing dept: prices, discounts, expected changes [1].',
     ['the personnel department', 'the auditor', 'the sales ledger']),
    ('A basic standard is', 'a long-term standard left unchanged, used to show trends', 'Basic standards are not updated [1].',
     ['a standard updated every month', 'the ideal standard', 'a standard that includes only fixed costs']),
])
fixed(t11_1, 'C2', (2, 3, 4), [
    ('Explain why attainable standards are usually preferred to ideal standards.', 'Ideal standards are almost never met, so they produce constant adverse variances and demotivate staff; attainable standards are challenging but achievable, motivating workers and giving meaningful variances.',
     'Ideal demotivating [1]; attainable realistic/motivating [1]; useful variances [1] [3]'),
    ('Explain two difficulties in setting standard costs.', 'Forecasting future prices (inflation, exchange rates); deciding on allowances for waste and idle time; rapid changes in technology or product design; obtaining reliable time studies.',
     'Two difficulties [1 each] + explanation [1 each] [4]'),
    ('Explain two uses of a standard costing system.', 'Basis for budgets and pricing; control through variance analysis; valuing inventory; motivating staff with targets.',
     'Two uses [1 each] + explanation [1 each] [4]'),
])


@t11_1.add('C3', (1, 2, 3, 4, 5))
def t111_card(r, D):
    x = _std(r, D)
    vohr = r.choice([2, 3, 4, 5, 6]); fohr = r.choice([4, 5, 6, 8, 10])
    loss = r.choice([0, 0, 5, 10, 20]) if D >= 4 else 0
    kg_in = x['kg'] / (1 - loss / 100) if loss else x['kg']
    mat = kg_in * x['sp']; lab = x['hrs'] * x['sr']; vo = x['hrs'] * vohr; fo = x['hrs'] * fohr if D >= 3 else 0
    tot = mat + lab + vo + fo
    stem = f'Each unit of {x["p"]} requires {x["kg"]} kg of finished material' + (f'; there is a normal loss of {loss}% of material input' if loss else '') + f'. Material costs ${x["sp"]:.2f} per kg. Each unit needs {x["hrs"]} direct labour hours at ${x["sr"]:.2f} per hour. Variable overheads are absorbed at ${vohr} per labour hour' + (f' and fixed overheads at ${fohr} per labour hour' if fo else '') + '.'
    key = (f'Material input {x["kg"]} / {(100 - loss) / 100:.2f} = {kg_in:.3f} kg [1]; ' if loss else '') + f'materials {m2(mat)} [1]; labour {m2(lab)} [1]; variable overhead {m2(vo)} [1]' + (f'; fixed overhead {m2(fo)} [1]' if fo else '') + f'; standard cost {m2(tot)} [1]'
    if D == 1:
        opts, ans = mm(r, tot, [tot - vo, mat + lab, tot + lab, tot * 1.1], f=m2)
        return {'stem': stem + ' What is the standard cost per unit?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + ' Prepare the standard cost card for one unit.', 'answer': f'Materials {m2(mat)}; labour {m2(lab)}; variable overhead {m2(vo)}' + (f'; fixed overhead {m2(fo)}' if fo else '') + f'; total {m2(tot)}', 'key': key, 'marks': 3 + bool(fo) + bool(loss)}


@t11_1.add('C2', (2, 3, 4), 'explain')
def t111_type(r, D):
    hrs = r.choice([1.5, 2, 2.5, 3]); idle = r.choice([5, 8, 10, 12])
    att = hrs / (1 - idle / 100)
    return {'stem': f'Time studies at {co(r)} show a skilled worker can make a unit in {hrs} hours under perfect conditions. In practice about {idle}% of paid time is lost to breaks and machine set-up. Explain which of {hrs} hours or {att:.2f} hours should be used as the standard, and why.',
            'answer': f'{att:.2f} hours (attainable standard, allowing for normal idle time). {hrs} hours is an ideal standard and would cause constant adverse efficiency variances and demotivation.',
            'key': f'Attainable {hrs}/{(100 - idle) / 100:.2f} = {att:.2f} h [1]; ideal unrealistic [1]; motivation/meaningful variances [1] [3]'}


t11_2 = topic('Material and labour variances', 'material and labour variances: price/rate and usage/efficiency', 'material price variance', 'labour efficiency', 'variances')
fixed(t11_2, 'C1', (1, 2), [
    ('The material price variance is calculated as', '(standard price − actual price) × actual quantity purchased', 'MPV = (SP − AP) × AQ [1].',
     ['(standard quantity − actual quantity) × standard price', '(standard price − actual price) × standard quantity', 'actual cost − budgeted cost']),
    ('The labour efficiency variance is calculated as', '(standard hours for actual output − actual hours worked) × standard rate', 'LEV = (SH − AH) × SR [1].',
     ['(standard rate − actual rate) × actual hours', '(actual hours − budgeted hours) × actual rate', 'standard hours × actual rate']),
    ('Buying cheaper, lower-quality material is most likely to cause', 'a favourable price variance and an adverse usage variance', 'Interrelationship: cheaper material → more waste [1].',
     ['an adverse price variance and a favourable usage variance', 'favourable price and usage variances', 'a favourable labour rate variance only']),
    ('An adverse labour rate variance could be caused by', 'an unplanned pay rise or using more skilled staff than planned', 'Paying above standard rate [1].',
     ['workers taking fewer hours than standard', 'buying cheaper materials', 'a fall in output']),
    ('A favourable material usage variance means', 'less material was used than the standard allowed for the actual output', 'AQ < SQ for actual output [1].',
     ['material cost more than standard', 'more material was used than standard', 'output was higher than budget']),
])
fixed(t11_2, 'C2', (2, 3, 4), [
    ('Explain how employing more skilled workers could cause an adverse labour rate variance but a favourable labour efficiency variance.', 'Skilled workers are paid more than the standard rate (adverse rate) but work faster and waste less time (favourable efficiency).',
     'Higher rate → adverse rate [1]; faster → favourable efficiency [1] [2]'),
    ('Explain why variances should be investigated rather than simply recorded.', 'Investigation finds the cause so that managers can correct problems (or update standards); only significant variances should be investigated where benefit exceeds cost.',
     'Find causes/corrective action [1]; significance/cost-benefit [1] [2]'),
    ('Explain two possible causes of an adverse material usage variance.', 'Poor-quality material; inexperienced workers; faulty machinery; theft or poor storage; unrealistic standard.',
     'Two causes [1 each] with explanation [1 each] [4]'),
])


@t11_2.add('C3', (1, 2, 3, 4, 5))
def t112_mat(r, D):
    x = _std(r, D)
    v = x['v']
    stem = _std_text(x, True, False)
    key = f'Price: (${x["sp"]:.2f} − ${x["ap"]:.2f}) × {nm(x["aq"])} = {fa(v["mp"], m2)} [1]; usage: ({nm(x["sq"])} − {nm(x["aq"])}) × ${x["sp"]:.2f} = {fa(v["mu"], m2)} [1]; total {fa(v["mt"], m2)} [1]'
    if D == 1:
        corr = fa(v['mp'], m2)
        opts, ans = mcq(r, corr, [fa(-v['mp'], m2), fa((x['sp'] - x['ap']) * x['sq'], m2) if x['sq'] != x['aq'] else fa(v['mp'] * 1.1, m2), fa(v['mu'], m2) if fa(v['mu'], m2) != corr else fa(v['mp'] * 2, m2), fa(v['mp'] * 0.5, m2)])
        return {'stem': stem + ' What is the material price variance?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the material price and usage variances, labelling each F or A.'
    if D >= 4:
        q += ' Suggest one reason why the two variances may be linked.'
        key += '; interrelationship (e.g. cheaper lower-quality material → more waste, or vice versa) [1]'
    return {'stem': stem + q, 'answer': f'Price {fa(v["mp"], m2)}; usage {fa(v["mu"], m2)}', 'key': key, 'marks': 3 + (D >= 4)}


@t11_2.add('C3', (1, 2, 3, 4, 5))
def t112_lab(r, D):
    x = _std(r, D)
    v = x['v']
    idle = step(r, 50, int(x['ah'] * 0.06) + 60, 10) if D >= 5 else 0
    stem = _std_text(x, False, True)
    if idle:
        stem = stem.replace('labour hours were worked and paid', 'labour hours were paid')
        stem += f' {nm(idle)} of the hours paid were idle because of a machine breakdown.'
        worked = x['ah'] - idle
        le = (x['sh'] - worked) * x['sr']; it = -idle * x['sr']
        key = f'Rate: (${x["sr"]:.2f} − ${x["ar"]:.2f}) × {nm(x["ah"])} = {fa(v["lr"], m2)} [1]; idle time {nm(idle)} × ${x["sr"]:.2f} = {fa(it, m2)} [1]; efficiency ({nm(x["sh"])} − {nm(worked)}) × ${x["sr"]:.2f} = {fa(le, m2)} [1]; total {fa(v["lt"], m2)} [1]'
        return {'stem': stem + ' Calculate the labour rate, idle time and efficiency variances.', 'answer': f'Rate {fa(v["lr"], m2)}; idle time {fa(it, m2)}; efficiency {fa(le, m2)}', 'key': key, 'marks': 4}
    key = f'Rate: (${x["sr"]:.2f} − ${x["ar"]:.2f}) × {nm(x["ah"])} = {fa(v["lr"], m2)} [1]; efficiency: ({nm(x["sh"])} − {nm(x["ah"])}) × ${x["sr"]:.2f} = {fa(v["le"], m2)} [1]; total {fa(v["lt"], m2)} [1]'
    if D == 1:
        corr = fa(v['le'], m2)
        opts, ans = mcq(r, corr, [fa(-v['le'], m2), fa((x['sh'] - x['ah']) * x['ar'], m2) if x['ar'] != x['sr'] else fa(v['le'] * 1.2, m2), fa(v['lr'], m2) if fa(v['lr'], m2) != corr else fa(v['le'] * 2, m2), fa(v['le'] * 0.5, m2)])
        return {'stem': stem + ' What is the labour efficiency variance?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + ' Calculate the labour rate and efficiency variances, labelling each F or A.', 'answer': f'Rate {fa(v["lr"], m2)}; efficiency {fa(v["le"], m2)}', 'key': key, 'marks': 3}


def _var_c4(r, D):
    x = _std(r, D)
    v = x['v']
    intro = f'{co(r)} uses standard costing. ' + _std_text(x)
    parts = [
        lambda r: ('Calculate the material price and usage variances.', f'Price {fa(v["mp"], m2)}; usage {fa(v["mu"], m2)}', f'(SP − AP) × AQ [1]; (SQ − AQ) × SP with SQ = {nm(x["sq"])} kg [1]; labels [1] [3]'),
        lambda r: ('Calculate the labour rate and efficiency variances.', f'Rate {fa(v["lr"], m2)}; efficiency {fa(v["le"], m2)}', f'(SR − AR) × AH [1]; (SH − AH) × SR with SH = {nm(x["sh"])} hours [1]; labels [1] [3]'),
        lambda r: ('Calculate the total direct cost variance and reconcile standard cost to actual cost.', f'Standard {m2(x["sq"] * x["sp"] + x["sh"] * x["sr"])}; total variance {fa(v["mt"] + v["lt"], m2)}; actual {m2(x["aq"] * x["ap"] + x["ah"] * x["ar"])}',
                   'Standard cost of actual output [1]; sum of variances [1]; actual [1] [3]'),
        lambda r: ('Suggest a possible cause of each labour variance and explain how they may be linked.', 'E.g. higher-grade staff: adverse rate, favourable efficiency; or lower-grade staff: favourable rate, adverse efficiency; poor material can cause adverse efficiency.', '[4]'),
        lambda r: ('Advise management which variance should be investigated first, giving reasons.', f'The largest in value relative to standard cost (here {max([("material price", abs(v["mp"])), ("material usage", abs(v["mu"])), ("labour rate", abs(v["lr"])), ("labour efficiency", abs(v["le"]))], key=lambda t: t[1])[0]}), especially if adverse and controllable.', 'Uses figures [1]; significance/controllability [1]; conclusion [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


for _t in (t11_1, t11_2):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_var_c4)
t11_2.add('C3', (4, 5), 'multi_step')(_var_c4)


@t11_2.add('C2', (2, 3, 4), 'explain')
def t112_err(r, D):
    x = _std(r, D)
    wrong = (x['sp'] - x['ap']) * x['sq']
    return {'stem': f'Material for {x["p"]} has a standard price of ${x["sp"]:.2f} per kg. {nm(x["aq"])} kg were bought for {m2(x["aq"] * x["ap"])}; the standard quantity for actual output was {nm(x["sq"])} kg. A trainee calculated the price variance as {fa(wrong, m2)}. Explain the error and calculate the correct variance.',
            'answer': f'The price variance must use the actual quantity bought, not the standard quantity: (${x["sp"]:.2f} − ${x["ap"]:.2f}) × {nm(x["aq"])} = {fa(x["v"]["mp"], m2)}.',
            'key': f'Actual quantity required [1]; actual price ${x["ap"]:.2f} [1]; {fa(x["v"]["mp"], m2)} [1] [3]'}


def _sales(r, D):
    bq = step(r, 2000, 20000, 100); aq = round(bq * r.uniform(0.85, 1.15) / 10) * 10
    if aq == bq:
        aq += 100
    sp = r.choice([25, 30, 40, 45, 50, 60, 80]); asp = sp + r.choice([-3, -2, -1.5, 1, 2, 2.5, 3])
    sc = round(sp * r.choice([0.55, 0.6, 0.65, 0.7]), 2)
    fohr_u = r.choice([3, 4, 5, 6]); fob = bq * fohr_u
    foa = fob + step(r, -3000, 4000, 100)
    prod = aq + step(r, -300, 300, 50)
    return dict(bq=bq, aq=aq, sp=sp, asp=asp, sc=sc, fohr=fohr_u, fob=fob, foa=foa, prod=prod)


t11_3 = topic('Sales and overhead variances', 'sales and overhead variances', 'sales variances', 'overhead variances', 'fixed overhead')
fixed(t11_3, 'C1', (1, 2), [
    ('The sales price variance is calculated as', '(actual selling price − standard selling price) × actual quantity sold', 'SPV = (AP − SP) × AQ sold [1].',
     ['(actual quantity − budgeted quantity) × standard price', '(standard price − actual price) × budgeted quantity', 'actual revenue − budgeted revenue']),
    ('Under absorption costing the sales volume variance is valued at', 'the standard profit per unit', 'Volume = (AQ − BQ) × standard profit (absorption) or contribution (marginal) [1].',
     ['the standard selling price', 'the actual profit per unit', 'the standard variable cost']),
    ('The fixed overhead expenditure variance is', 'budgeted fixed overhead − actual fixed overhead', 'Expenditure variance [1].',
     ['(actual output − budgeted output) × absorption rate', 'actual fixed overhead × actual hours', 'absorbed overhead − budgeted overhead × 2']),
    ('A favourable fixed overhead volume variance arises when', 'actual output is greater than budgeted output', 'More units absorb overheads → over-absorption [1].',
     ['actual fixed overheads are lower than budget', 'actual output is less than budgeted output', 'the selling price rises']),
    ('Reducing the selling price to increase sales is likely to cause', 'an adverse sales price variance and a favourable sales volume variance', 'Price/volume interrelationship [1].',
     ['a favourable sales price variance and an adverse volume variance', 'two adverse variances', 'no sales variances']),
])
fixed(t11_3, 'C2', (2, 3, 4), [
    ('Explain why a favourable fixed overhead volume variance does not mean that fixed costs were saved.', 'It means more units were produced than budgeted, so overheads were over-absorbed; the actual fixed cost spent is measured by the expenditure variance.',
     'Relates to output/absorption [1]; spending measured by expenditure variance [1] [2]'),
    ('Explain two possible causes of an adverse sales volume variance.', 'Competitor launches or price cuts; economic downturn reducing demand; quality problems; price increased; lost a major customer.',
     'Two causes [1 each] + explanation [1 each] [4]'),
])


@t11_3.add('C3', (1, 2, 3, 4, 5))
def t113_sales(r, D):
    x = _sales(r, D)
    c = co(r)
    spv = (x['asp'] - x['sp']) * x['aq']
    prof = x['sp'] - x['sc']
    svv = (x['aq'] - x['bq']) * prof
    marginal = D >= 4 and r.random() < 0.5
    vc = round(x['sc'] * 0.6, 2)
    cont = x['sp'] - vc
    svv_m = (x['aq'] - x['bq']) * cont
    stem = f'{c} budgeted to sell {nm(x["bq"])} units at ${x["sp"]} each; the standard ' + (f'variable cost is ${vc:.2f}' if marginal else f'full cost is ${x["sc"]:.2f}') + f' per unit. It actually sold {nm(x["aq"])} units for {m2(x["aq"] * x["asp"])}.'
    use = svv_m if marginal else svv
    lab = 'contribution' if marginal else 'profit'
    key = f'Actual price {m2(x["aq"] * x["asp"])}/{nm(x["aq"])} = ${x["asp"]:.2f} [1]; price variance (${x["asp"]:.2f} − ${x["sp"]}) × {nm(x["aq"])} = {fa(spv, m2)} [1]; volume ({nm(x["aq"])} − {nm(x["bq"])}) × standard {lab} ${(cont if marginal else prof):.2f} = {fa(use, m2)} [1]'
    if D == 1:
        corr = fa(spv, m2)
        opts, ans = mcq(r, corr, [fa(-spv, m2), fa((x['asp'] - x['sp']) * x['bq'], m2), fa((x['aq'] - x['bq']) * x['sp'], m2), fa(spv * 2, m2)])
        return {'stem': stem + ' What is the sales price variance?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + f' Calculate the sales price variance and the sales volume variance (valued at standard {lab}).', 'answer': f'Price {fa(spv, m2)}; volume {fa(use, m2)}', 'key': key, 'marks': 3}


@t11_3.add('C3', (2, 3, 4, 5))
def t113_foh(r, D):
    x = _sales(r, D)
    c = co(r)
    exp = x['fob'] - x['foa']
    vol = (x['prod'] - x['bq']) * x['fohr']
    absd = x['prod'] * x['fohr']
    stem = f'{c} budgeted fixed production overheads of {m(x["fob"])} for an output of {nm(x["bq"])} units, absorbed per unit. Actual output was {nm(x["prod"])} units and actual fixed overheads were {m(x["foa"])}. Calculate the fixed overhead expenditure and volume variances and the over- or under-absorption.'
    tot = absd - x['foa']
    return {'stem': stem, 'answer': f'Expenditure {fa(exp)}; volume {fa(vol)}; {"over" if tot > 0 else "under"}-absorbed {m(abs(tot))}',
            'key': f'OAR {m(x["fob"])}/{nm(x["bq"])} = ${x["fohr"]} per unit [1]; expenditure {m(x["fob"])} − {m(x["foa"])} = {fa(exp)} [1]; volume ({nm(x["prod"])} − {nm(x["bq"])}) × ${x["fohr"]} = {fa(vol)} [1]; absorbed {m(absd)} − actual {m(x["foa"])} = {fa(tot)} [1]', 'marks': 4}


@t11_3.add('C3', (2, 3, 4))
def t113_voh(r, D):
    c = co(r)
    out = step(r, 1000, 10000, 100); hrs = r.choice([1, 1.5, 2, 3]); rate = r.choice([2, 3, 4, 5, 6])
    ah = round(out * hrs * r.uniform(0.92, 1.08)); act = round(ah * rate * r.uniform(0.92, 1.08))
    sh = out * hrs
    exp = ah * rate - act; eff = (sh - ah) * rate
    return {'stem': f'{c} absorbs variable overheads at ${rate} per direct labour hour; the standard is {hrs} hours per unit. Output was {nm(out)} units, {nm(ah)} hours were worked and variable overheads cost {m(act)}. Calculate the variable overhead expenditure and efficiency variances.',
            'answer': f'Expenditure {fa(exp)}; efficiency {fa(eff)}',
            'key': f'Expenditure: {nm(ah)} × ${rate} − {m(act)} = {fa(exp)} [1]; efficiency: ({nm(sh)} − {nm(ah)}) × ${rate} = {fa(eff)} [1]', 'marks': 2}


@t11_3.add('C2', (2, 3, 4), 'explain')
def t113_claim(r, D):
    x = _sales(r, D)
    spv = (x['asp'] - x['sp']) * x['aq']; svv = (x['aq'] - x['bq']) * (x['sp'] - x['sc'])
    return {'stem': f'The sales manager of {co(r)} changed the selling price from ${x["sp"]} to ${x["asp"]:.2f}. The sales price variance was {fa(spv, m2)} and the sales volume variance {fa(svv, m2)}. Explain how the two variances may be linked and whether the decision was successful.',
            'answer': f'A {"price cut" if x["asp"] < x["sp"] else "price rise"} is likely to {"raise" if x["asp"] < x["sp"] else "reduce"} volume. Net effect {fa(spv + svv, m2)}, so the decision ' + ('increased' if spv + svv > 0 else 'reduced') + ' profit compared with budget (other factors such as market conditions may also explain volume).',
            'key': 'Price elasticity link [1]; net effect calculated [1]; judgement with caveat [1] [3]'}


t11_4 = topic('Reconciling budgeted and actual profit; interpreting variances', 'reconciling budgeted and actual profit; interpreting variances', 'reconciliation', 'operating statement', 'interpreting variances')
fixed(t11_4, 'C1', (1, 2), [
    ('In an operating statement reconciling budgeted and actual profit, favourable variances are', 'added to budgeted profit', 'Budgeted profit + F − A = actual profit [1].',
     ['deducted from budgeted profit', 'ignored', 'added to actual profit']),
    ('A variance is controllable if', 'the manager responsible can influence it', 'Controllability determines responsibility [1].',
     ['it is favourable', 'it is larger than $1,000', 'it relates to fixed costs']),
    ('Which variance is LEAST likely to be controllable by the production manager?', 'Fixed overhead expenditure variance caused by a rent increase', 'Rent set by head office/landlord [1].',
     ['Material usage variance', 'Labour efficiency variance', 'Variable overhead efficiency variance']),
])
fixed(t11_4, 'C2', (2, 3, 4), [
    ('Explain why a favourable variance is not always good for the business.', 'It may result from lower-quality materials or skimping that causes later adverse variances or customer complaints; or from a slack standard.',
     'Hidden quality cost [1]; slack standard / interrelationship [1] [2]'),
    ('Explain two factors managers should consider when deciding whether to investigate a variance.', 'Size (absolute and % of standard); whether it is adverse and controllable; trend over several periods; cost of investigation vs expected benefit.',
     'Two factors [1 each] + explanation [1 each] [4]'),
])


def _rec(r, D):
    x = _std(r, D)
    s = _sales(r, D)
    bp = step(r, 20000, 150000, 500)
    v = x['v']
    spv = (s['asp'] - s['sp']) * s['aq']; svv = (s['aq'] - s['bq']) * (s['sp'] - s['sc'])
    foe = s['fob'] - s['foa']
    items = [('sales price', spv), ('sales volume', svv), ('material price', v['mp']), ('material usage', v['mu']), ('labour rate', v['lr']), ('labour efficiency', v['le']), ('fixed overhead expenditure', foe)]
    items = [(a, int(_hu(b))) for a, b in items if int(_hu(b)) != 0]
    return bp, items


@t11_4.add('C3', (1, 2, 3, 4, 5))
def t114_rec(r, D):
    bp, items = _rec(r, D)
    k = 3 if D == 1 else (4 if D <= 3 else 6)
    sel = r.sample(items, k)
    ap = bp + sum(v for _, v in sel)
    stem = f'The budgeted profit of {co(r)} for the period was {m(bp)}. Variances were: ' + '; '.join(f'{a} {fa(v)}' for a, v in sel) + '.'
    key = f'{m(bp)} + favourable {m(sum(v for _, v in sel if v > 0))} − adverse {m(-sum(v for _, v in sel if v < 0))} [1]; actual profit {m(ap)} [1]'
    if D == 1:
        opts, ans = mm(r, ap, [bp - sum(v for _, v in sel), bp + sum(abs(v) for _, v in sel), bp, ap + 2 * abs(sel[0][1])])
        return {'stem': stem + ' What was the actual profit?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + ' Prepare a statement reconciling budgeted profit with actual profit.', 'answer': f'Actual profit {m(ap)}', 'key': key + ' ; layout F added, A deducted [1]', 'marks': 3}


@t11_4.add('C3', (2, 3, 4, 5))
def t114_back(r, D):
    x = _std(r, D)
    ap = x['ap']
    mp = x['v']['mp']
    c = co(r)
    return {'stem': f'At {c} the standard price of material is ${x["sp"]:.2f} per kg. {nm(x["aq"])} kg were bought and the material price variance was {fa(mp, m2)}. The material usage variance was {fa(x["v"]["mu"], m2)}. Calculate the actual price per kg and the standard quantity of material for the actual output.',
            'answer': f'Actual price ${ap:.2f} per kg; standard quantity {nm(x["sq"])} kg',
            'key': f'Actual cost = {nm(x["aq"])} × ${x["sp"]:.2f} {"−" if mp > 0 else "+"} {m2(abs(mp))} = {m2(x["aq"] * ap)}, ÷ {nm(x["aq"])} = ${ap:.2f} [2]; SQ = AQ {"+" if x["v"]["mu"] > 0 else "−"} {m2(abs(x["v"]["mu"]))}/${x["sp"]:.2f} = {nm(x["sq"])} kg [2]', 'marks': 4}


def _rec_c4(r, D):
    bp, items = _rec(r, D)
    sel = items[:]
    ap = bp + sum(v for _, v in sel)
    intro = f'{co(r)} budgeted a profit of {m(bp)}. The management accountant has calculated these variances: ' + '; '.join(f'{a} {fa(v)}' for a, v in sel) + '.'
    worst = min(sel, key=lambda t: t[1])
    best = max(sel, key=lambda t: t[1])
    parts = [
        lambda r: ('Prepare an operating statement reconciling budgeted profit with actual profit.', f'Actual profit {m(ap)}', f'Favourable total {m(sum(v for _, v in sel if v > 0))} [1]; adverse total {m(-sum(v for _, v in sel if v < 0))} [1]; actual {m(ap)} [1] [3]'),
        lambda r: (f'Explain one possible cause of the {worst[0]} variance and state who is responsible for it.', f'{worst[0]} {fa(worst[1])}: e.g. ' + {'sales price': 'price cut to meet competition — sales manager', 'sales volume': 'fall in demand — sales manager', 'material price': 'supplier price rise — purchasing manager',
                   'material usage': 'poor-quality material or waste — production manager', 'labour rate': 'pay award or overtime — HR/production', 'labour efficiency': 'inexperienced workers or breakdowns — production manager', 'fixed overhead expenditure': 'higher rent or energy costs — general management'}[worst[0]], '[3]'),
        lambda r: ('Discuss how the variances may be interrelated.', 'E.g. cheaper material: F price, A usage, A labour efficiency; price cut: A price, F volume; skilled labour: A rate, F efficiency.', '[4]'),
        lambda r: (f'Evaluate the overall performance of the business for the period.', f'Actual profit {m(ap)} vs budget {m(bp)} ({fa(ap - bp)}); largest favourable {best[0]}, largest adverse {worst[0]}; consider controllability and whether standards are realistic.', 'Overall comparison [1]; key variances [2]; conclusion [1] [4]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


for _t in (t11_3, t11_4):
    _t.add('C4', (2, 3, 4, 5), 'multi_step')(_rec_c4)
t11_4.add('C3', (4, 5), 'multi_step')(_rec_c4)
t11_3.add('C4', (2, 3, 4, 5), 'multi_step')(_var_c4)


@t11_4.add('C2', (2, 3, 4), 'explain')
def t114_err(r, D):
    bp, items = _rec(r, D)
    sel = r.sample(items, 3)
    wrong = bp - sum(v for _, v in sel)
    return {'stem': f'Budgeted profit was {m(bp)}. Variances: ' + '; '.join(f'{a} {fa(v)}' for a, v in sel) + f'. A trainee calculated actual profit as {m(wrong)}. Explain the error and calculate the correct actual profit.',
            'answer': f'The trainee deducted favourable and added adverse variances. Correct: {m(bp)} + F − A = {m(bp + sum(v for _, v in sel))}.',
            'key': f'Signs reversed [1]; F added, A deducted [1]; {m(bp + sum(v for _, v in sel))} [1] [3]'}


CHAPTERS[11] = [t11_1, t11_2, t11_3, t11_4]


# ===================================================================== 12 Investment appraisal
def dfs(rate, n):
    return [round(1 / (1 + rate / 100) ** t, 3) for t in range(1, n + 1)]


def _proj(r, D, n=None):
    n = n or r.choice([3, 4, 5])
    cost = step(r, 50000, 500000, 5000)
    base = cost / n * r.uniform(1.1, 1.7)
    flows = [round(base * r.uniform(0.7, 1.3) / 500) * 500 for _ in range(n)]
    res = step(r, 0, cost // 8, 1000) if D >= 3 else 0
    asset = r.choice(['a new packaging line', 'a delivery van fleet', 'a solar power system', 'a bakery oven', 'an automated warehouse', 'a fishing vessel', 'a 3D printer', 'a cold-storage unit', 'a bottling machine'])
    return dict(n=n, cost=cost, flows=flows, res=res, asset=asset)


def ym(y, mo):
    if mo == 12:
        y, mo = y + 1, 0
    return f'{y} year{"" if y == 1 else "s"} {mo} month{"" if mo == 1 else "s"}'


def _payback(cost, flows):
    cum = -cost
    for i, f in enumerate(flows):
        if cum + f >= 0:
            frac = -cum / f
            return i + frac, i, -cum, f
        cum += f
    return None, None, None, None


def _flows_text(p, res_in_last=True):
    t = ', '.join(f'year {i + 1} {m(f)}' for i, f in enumerate(p['flows']))
    return t + (f' (plus residual value of {m(p["res"])} at the end of year {p["n"]})' if p['res'] and res_in_last else '')


t12_1 = topic('Payback period and accounting rate of return', 'payback period and accounting rate of return (arr)', 'payback', 'accounting rate of return', 'arr')
fixed(t12_1, 'C1', (1, 2), [
    ('The payback period is', 'the time taken for the net cash inflows from a project to repay the initial investment', 'Payback = time to recover initial outlay [1].',
     ['the average annual profit as a percentage of investment', 'the life of the asset', 'the discount rate that gives zero NPV']),
    ('The accounting rate of return uses', 'profit after depreciation rather than cash flow', 'ARR = average annual profit / (average or initial) investment × 100 [1].',
     ['discounted cash flows', 'only the first year\'s cash flow', 'the payback period']),
    ('Average investment for ARR is usually calculated as', '(initial cost + residual value) ÷ 2', 'Average investment = (cost + scrap) / 2 [1].',
     ['initial cost ÷ useful life', 'initial cost − residual value', 'initial cost × 2']),
    ('A major weakness of the payback method is that it', 'ignores cash flows after the payback period', 'Ignores later flows and (simple) time value [1].',
     ['is difficult to calculate', 'uses accounting profits', 'favours long-term projects']),
    ('To convert annual net cash inflow into annual profit for ARR, you', 'deduct annual depreciation', 'Profit = cash flow − depreciation [1].',
     ['add depreciation', 'deduct the residual value', 'multiply by the discount factor']),
])
fixed(t12_1, 'C2', (2, 3, 4), [
    ('Explain why a business with cash-flow problems might rely on the payback method.', 'Payback focuses on how quickly cash is recovered, reducing liquidity risk and exposure to uncertain later years.',
     'Liquidity [1]; risk of distant flows [1] [2]'),
    ('Explain two disadvantages of the accounting rate of return.', 'Ignores the time value of money; uses profit (affected by depreciation policy) rather than cash; ignores timing of returns; different definitions of investment.',
     'Two disadvantages [1 each] + explanation [1 each] [4]'),
    ('Explain one advantage of ARR over payback.', 'ARR considers profit over the whole life of the project and gives a percentage that can be compared with ROCE or a target return.',
     'Whole life [1]; comparable % [1] [2]'),
])


@t12_1.add('C3', (1, 2, 3, 4, 5))
def t121_pb(r, D):
    p = _proj(r, D)
    pb, i, rem, f = _payback(p['cost'], p['flows'])
    if pb is None:
        p['flows'][-1] += p['cost']; pb, i, rem, f = _payback(p['cost'], p['flows'])
    yrs = int(pb); mo = round((pb - yrs) * 12)
    if mo == 12:
        yrs, mo = yrs + 1, 0
    mo = max(mo, 1) if yrs == 0 else mo
    stem = f'{co(r)} is considering {p["asset"]} costing {m(p["cost"])}. Net cash inflows are expected to be: {_flows_text(p, False)}.'
    key = f'Cumulative cash flow reaches {m(rem)} still to recover at the start of year {i + 1} [1]; {m(rem)}/{m(f)} × 12 = {mo} month{"" if mo == 1 else "s"} [1]; payback {ym(yrs, mo)} [1]'
    ans = ym(yrs, mo)
    if D == 1:
        alts = [ym(yrs, (mo + 3) % 12), ym(yrs + 1, mo), ym(max(0, yrs - 1), (mo + 6) % 12), ym(yrs, (mo + 7) % 12)]
        opts, a = mcq(r, ans, alts)
        return {'stem': stem + ' What is the payback period (to the nearest month)?', 'options': opts, 'answer': a, 'key': key}
    if D >= 4:
        tgt = r.choice([2, 3])
        stem += f' The company requires payback within {tgt} years.'
        return {'stem': stem + ' Calculate the payback period in years and months and advise whether the project meets the target.', 'answer': ans + (' — meets the target' if pb <= tgt else ' — does not meet the target'), 'key': key + ' ; conclusion [1]', 'marks': 4}
    return {'stem': stem + ' Calculate the payback period in years and months.', 'answer': ans, 'key': key, 'marks': 3}


@t12_1.add('C3', (1, 2, 3, 4, 5))
def t121_arr(r, D):
    p = _proj(r, D)
    dep = (p['cost'] - p['res']) / p['n']
    tot_cf = sum(p['flows'])
    avg_profit = (tot_cf - (p['cost'] - p['res'])) / p['n']
    basis = 'average' if D >= 3 else 'initial'
    inv = (p['cost'] + p['res']) / 2 if basis == 'average' else p['cost']
    arr = avg_profit / inv * 100
    stem = f'{co(r)} is evaluating {p["asset"]} costing {m(p["cost"])} with a life of {p["n"]} years' + (f' and a residual value of {m(p["res"])}' if p['res'] else ' and no residual value') + f'. Depreciation is straight-line. Net cash inflows: {_flows_text(p, False)}.'
    key = f'Total profit = {m(tot_cf)} − depreciation {m(p["cost"] - p["res"])} = {m(tot_cf - p["cost"] + p["res"])} [1]; average profit {m(avg_profit)} [1]; {basis} investment {m(inv)} [1]; ARR = {arr:.1f}% [1]'
    if D == 1:
        opts, ans = num_mcq(r, arr, [tot_cf / p['n'] / inv * 100, avg_profit / ((p['cost'] + p['res']) / 2) * 100 if basis == 'initial' else arr * 0.5, arr * 2, avg_profit / tot_cf * 100], fmtf=lambda v: pc(v))
        return {'stem': stem + ' What is the ARR based on the initial investment?', 'options': opts, 'answer': ans, 'key': key}
    return {'stem': stem + f' Calculate the accounting rate of return based on the {basis} investment.', 'answer': pc(arr), 'key': key, 'marks': 4}


def _pb_c4(r, D):
    a, b = _proj(r, D, 4), _proj(r, D, 4)
    b['cost'] = a['cost']
    c = co(r)
    pa = _payback(a['cost'], a['flows'])[0]; pbb = _payback(b['cost'], b['flows'])[0]
    if pa is None or pbb is None:
        a['flows'] = [a['cost'] // 3] * 4; b['flows'] = [b['cost'] // 2, b['cost'] // 4, b['cost'] // 4, b['cost'] // 8]
        pa = _payback(a['cost'], a['flows'])[0]; pbb = _payback(b['cost'], b['flows'])[0]
    arr_a = (sum(a['flows']) - a['cost']) / 4 / (a['cost'] / 2) * 100
    arr_b = (sum(b['flows']) - b['cost']) / 4 / (b['cost'] / 2) * 100
    intro = f'{c} can invest {m(a["cost"])} in one of two projects, each lasting 4 years with no residual value. Project P cash inflows: {_flows_text(a, False)}. Project Q cash inflows: {_flows_text(b, False)}.'
    fy = lambda x: ym(int(x), round((x - int(x)) * 12))
    parts = [
        lambda r: ('Calculate the payback period of each project.', f'P {fy(pa)}; Q {fy(pbb)}', '[4]'),
        lambda r: ('Calculate the ARR of each project on average investment.', f'P {arr_a:.1f}%; Q {arr_b:.1f}%', 'Average profit [2]; average investment [1]; ARR each [1] [4]'),
        lambda r: ('Advise the directors which project to choose.', f'Payback favours {"P" if pa < pbb else "Q"}; ARR favours {"P" if arr_a > arr_b else "Q"}. ' + ('Both methods agree.' if (pa < pbb) == (arr_a > arr_b) else 'The methods conflict, so NPV should be used.') + ' Consider risk and liquidity.',
                   'Uses both results [2]; limitations [1]; recommendation [1] [4]'),
        lambda r: ('Explain why neither method takes account of the time value of money.', 'Both treat $1 received in year 4 as equal to $1 now; they do not discount future flows.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3), type_='multi_step')


t12_1.add('C4', (2, 3, 4, 5), 'multi_step')(_pb_c4)
t12_1.add('C3', (4, 5), 'multi_step')(_pb_c4)


t12_2 = topic('Net present value and discounted cash flow', 'net present value (npv) and discounted cash flow', 'net present value', 'npv', 'discounted cash flow')
fixed(t12_2, 'C1', (1, 2), [
    ('A project should be accepted under the NPV method if', 'its net present value is positive', 'Positive NPV increases shareholder wealth [1].',
     ['its payback is less than 5 years', 'its NPV is negative', 'its total cash inflows exceed cost, ignoring timing']),
    ('Discounting cash flows takes account of', 'the time value of money', '$1 today is worth more than $1 in future [1].',
     ['depreciation', 'inflation only', 'accounting profit']),
    ('The discount factor for year 2 at 10% is approximately', '0.826', '1/1.1² = 0.826 [1].',
     ['0.909', '0.800', '1.210']),
    ('Which cash flow should be EXCLUDED from an NPV calculation?', 'Depreciation of the new machine', 'Depreciation is non-cash; also exclude sunk costs [1].',
     ['Initial cost of the machine', 'Additional working capital', 'Residual value at the end of the project']),
    ('Money already spent on market research before the decision is a', 'sunk cost and is ignored', 'Sunk costs are not relevant [1].',
     ['relevant cost', 'cash inflow', 'discount factor']),
])
fixed(t12_2, 'C2', (2, 3, 4), [
    ('Explain why NPV is considered superior to payback and ARR.', 'It uses cash flows, considers the whole life of the project and the time value of money, and gives an absolute increase in wealth.',
     'Time value [1]; whole life/cash flows [1]; wealth measure [1] [3]'),
    ('Explain two difficulties in using NPV.', 'Estimating future cash flows accurately; choosing an appropriate discount rate (cost of capital); difficult to explain to non-financial managers.',
     'Two difficulties [1 each] + explanation [1 each] [4]'),
    ('Explain why working capital released at the end of a project is a cash inflow.', 'Inventory and receivables tied up at the start are turned back into cash when the project ends.',
     '[2]'),
])


@t12_2.add('C3', (1, 2, 3, 4, 5))
def t122_npv(r, D):
    p = _proj(r, D)
    rate = r.choice([8, 10, 12, 14, 15, 16])
    df = dfs(rate, p['n'])
    wc = step(r, 5000, 30000, 1000) if D >= 4 else 0
    flows = p['flows'][:]
    flows[-1] += p['res'] + wc
    pv = [int(_hu(f * d)) for f, d in zip(flows, df)]
    npv = sum(pv) - p['cost'] - wc
    stem = (f'{co(r)} is considering {p["asset"]} costing {m(p["cost"])}' + (f' which will also need working capital of {m(wc)} at the start, released at the end' if wc else '') + f'. Net cash inflows: {_flows_text(p)}. The cost of capital is {rate}%; discount factors: '
            + ', '.join(f'year {i + 1} {d:.3f}' for i, d in enumerate(df)) + '.')
    key = '; '.join(f'Y{i + 1} {m(f)} × {d:.3f} = {m(v)}' for i, (f, d, v) in enumerate(zip(flows, df, pv))) + f' [2]; total PV {m(sum(pv))} − {m(p["cost"] + wc)} [1]; NPV {m(npv)} [1]'
    if D == 1:
        opts, ans = mm(r, npv, [sum(flows) - p['cost'] - wc, sum(pv), npv - flows[-1] * df[-1], npv + 5000])
        return {'stem': stem + ' What is the net present value?', 'options': opts, 'answer': ans, 'key': key}
    q = ' Calculate the net present value and state whether the project should be accepted.'
    return {'stem': stem + q, 'answer': f'NPV {m(npv)} — {"accept (positive)" if npv > 0 else "reject (negative)"}', 'key': key + ' ; decision [1]', 'marks': 4 + (D >= 4)}


def _npv_c4(r, D):
    p = _proj(r, D, 4)
    rate = r.choice([10, 12, 14])
    df = dfs(rate, 4)
    revs = [step(r, 60000, 250000, 1000) for _ in range(4)]
    costs = [round(v * r.uniform(0.35, 0.6) / 1000) * 1000 for v in revs]
    sunk = step(r, 2000, 15000, 500)
    dep = (p['cost'] - p['res']) / 4
    flows = [a - b for a, b in zip(revs, costs)]
    if sum(int(_hu(f * d)) for f, d in zip(flows, df)) < p['cost'] * 0.6:
        p['cost'] = round(sum(int(_hu(f * d)) for f, d in zip(flows, df)) * r.uniform(0.75, 1.1) / 1000) * 1000
    flows2 = flows[:]; flows2[-1] += p['res']
    pv = [int(_hu(f * d)) for f, d in zip(flows2, df)]
    npv = sum(pv) - p['cost']
    intro = (f'{co(r)} has spent {m(sunk)} on a feasibility study for {p["asset"]} costing {m(p["cost"])}, life 4 years' + (f', residual value {m(p["res"])}' if p['res'] else '') + '. Forecast revenue: ' + ', '.join(f'year {i + 1} {m(v)}' for i, v in enumerate(revs)) + '; cash operating costs: ' + ', '.join(m(v) for v in costs)
             + f'. Straight-line depreciation of {m((p["cost"] - p["res"]) / 4)} a year has been included in the accountant\'s profit forecast. Cost of capital {rate}%; discount factors ' + ', '.join(f'{d:.3f}' for d in df) + '.')
    parts = [
        lambda r: ('Calculate the net cash flow for each year.', ', '.join(m(f) for f in flows2), 'Revenue − cash costs [1]; depreciation and sunk cost excluded [1]; residual in year 4 [1] [3]'),
        lambda r: ('Calculate the net present value.', m(npv), '; '.join(f'{m(f)} × {d:.3f}' for f, d in zip(flows2, df)) + f' [2]; less {m(p["cost"])} = {m(npv)} [1] [3]'),
        lambda r: ('Explain why the feasibility study cost is ignored.', 'It is a sunk cost already incurred whatever the decision, so it is not relevant.', '[2]'),
        lambda r: ('Advise the directors, including two non-financial factors.', f'NPV {m(npv)}: ' + ('accept as it increases shareholder wealth' if npv > 0 else 'reject on financial grounds') + '; non-financial: impact on staff, environment, reliability of forecasts, competitor reaction.', 'Decision from NPV [1]; two non-financial factors [2]; conclusion [1] [4]'),
        lambda r: ('Calculate the payback period (undiscounted).', (lambda pbv: ym(int(pbv), round((pbv - int(pbv)) * 12)) if pbv is not None else 'Not within project life')(_payback(p['cost'], flows2)[0]), '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t12_2.add('C4', (2, 3, 4, 5), 'multi_step')(_npv_c4)
t12_2.add('C3', (4, 5), 'multi_step')(_npv_c4)
t12_1.add('C4', (3, 4, 5), 'multi_step')(_npv_c4)


@t12_2.add('C2', (2, 3, 4), 'explain')
def t122_err(r, D):
    p = _proj(r, D, 3)
    rate = r.choice([8, 10, 12])
    df = dfs(rate, 3)
    dep = p['cost'] / 3
    wrong = sum(int(_hu((f - dep) * d)) for f, d in zip(p['flows'], df)) - p['cost']
    right = sum(int(_hu(f * d)) for f, d in zip(p['flows'], df)) - p['cost']
    return {'stem': f'{co(r)} appraised {p["asset"]} costing {m(p["cost"])} with cash inflows of {_flows_text(p, False)}. The analyst deducted annual depreciation of {m(dep)} from each inflow before discounting at {rate}% (factors {", ".join(f"{d:.3f}" for d in df)}) and obtained an NPV of {m(wrong)}. Explain the error and calculate the correct NPV.',
            'answer': f'Depreciation is not a cash flow; the cost is already counted as the initial outlay, so deducting depreciation double counts it. Correct NPV = {m(right)}.',
            'key': f'Depreciation non-cash/double counting [1]; correct PV of inflows {m(right + p["cost"])} [1]; NPV {m(right)} [1] [3]'}


t12_3 = topic('Internal rate of return by interpolation', 'internal rate of return (irr) by interpolation', 'internal rate of return', 'irr', 'interpolation')
fixed(t12_3, 'C1', (1, 2), [
    ('The internal rate of return is', 'the discount rate at which the net present value of a project is zero', 'IRR: NPV = 0 [1].',
     ['the average accounting profit as a percentage of cost', 'the bank\'s interest rate', 'the rate that maximises NPV']),
    ('A project should be accepted under IRR if', 'its IRR is higher than the cost of capital', 'IRR > cost of capital → positive NPV [1].',
     ['its IRR is lower than the cost of capital', 'its IRR is zero', 'its IRR equals the payback period']),
    ('Interpolation to estimate IRR requires', 'NPVs calculated at two discount rates, ideally one positive and one negative', 'Linear interpolation between the rates [1].',
     ['the payback period and ARR', 'only one NPV', 'the accounting profits']),
])
fixed(t12_3, 'C2', (2, 3, 4), [
    ('Explain why IRR found by linear interpolation is only an approximation.', 'NPV does not change linearly with the discount rate (the NPV curve is convex), so a straight-line estimate between two points differs slightly from the true rate.',
     'Non-linear relationship [1]; estimate depends on rates chosen [1] [2]'),
    ('Explain one advantage and one disadvantage of IRR compared with NPV.', 'Advantage: a percentage is easy to understand and compare with cost of capital. Disadvantage: may rank mutually exclusive projects wrongly; ignores size of project; can have multiple IRRs with unusual cash flows.',
     'Advantage [1]; disadvantage [1] [2]'),
])


@t12_3.add('C3', (1, 2, 3, 4, 5))
def t123_irr(r, D):
    p = _proj(r, D, r.choice([3, 4]))
    lo = r.choice([8, 10, 12])
    hi = lo + r.choice([6, 8, 10])
    dl, dh = dfs(lo, p['n']), dfs(hi, p['n'])
    nl = sum(int(_hu(f * d)) for f, d in zip(p['flows'], dl)) - p['cost']
    nh = sum(int(_hu(f * d)) for f, d in zip(p['flows'], dh)) - p['cost']
    if not (nl > 0 > nh):
        u = r.uniform(0.25, 0.75)
        target = sum(int(_hu(f * d)) for f, d in zip(p['flows'], dl)) * u + sum(int(_hu(f * d)) for f, d in zip(p['flows'], dh)) * (1 - u)
        p['cost'] = round(target / 100) * 100
        nl = sum(int(_hu(f * d)) for f, d in zip(p['flows'], dl)) - p['cost']; nh = sum(int(_hu(f * d)) for f, d in zip(p['flows'], dh)) - p['cost']
    irr = lo + nl / (nl - nh) * (hi - lo)
    if D <= 2:
        stem = f'A project has an NPV of {m(nl)} at {lo}% and {m(nh)} at {hi}%. '
        key = f'IRR = {lo} + {m(nl)}/({m(nl)} + {m(-nh)}) × {hi - lo} [1]; = {irr:.1f}% [1]'
        if D == 1:
            opts, ans = num_mcq(r, irr, [(lo + hi) / 2 if abs((lo + hi) / 2 - irr) > 0.15 else irr + 1.5, hi - nl / (nl - nh) * (hi - lo), lo + nh / (nh - nl) * (hi - lo) if abs(nh) > 1 else irr - 2, irr + 2.5], fmtf=lambda v: pc(v))
            return {'stem': stem + 'What is the IRR estimated by interpolation?', 'options': opts, 'answer': ans, 'key': key}
        return {'stem': stem + f'Estimate the internal rate of return by interpolation and state whether the project is acceptable with a cost of capital of {lo + 2}%.', 'answer': f'IRR ≈ {irr:.1f}%; ' + ('acceptable' if irr > lo + 2 else 'not acceptable'), 'key': key + ' ; decision [1]', 'marks': 3}
    stem = (f'{co(r)} is evaluating {p["asset"]} costing {m(p["cost"])} with net cash inflows {_flows_text(p, False)}. Discount factors at {lo}%: ' + ', '.join(f'{d:.3f}' for d in dl) + f'; at {hi}%: ' + ', '.join(f'{d:.3f}' for d in dh) + '. Calculate the NPV at each rate and estimate the IRR.')
    key = f'NPV at {lo}% = {m(nl)} [2]; NPV at {hi}% = {m(nh)} [2]; IRR = {lo} + {m(nl)}/({m(nl - nh)}) × {hi - lo} = {irr:.1f}% [1]'
    return {'stem': stem, 'answer': f'NPV {lo}%: {m(nl)}; NPV {hi}%: {m(nh)}; IRR ≈ {irr:.1f}%', 'key': key, 'marks': 5, 'type': 'multi_step'}


def _irr_c4(r, D):
    p = _proj(r, D, 4)
    coc = r.choice([9, 10, 11, 12])
    lo, hi = 10, 20
    dl, dh = dfs(lo, 4), dfs(hi, 4)
    pvl = sum(int(_hu(f * d)) for f, d in zip(p['flows'], dl)); pvh = sum(int(_hu(f * d)) for f, d in zip(p['flows'], dh))
    p['cost'] = round((pvl * r.uniform(0.35, 0.65) + pvh * r.uniform(0.35, 0.65)) / 1000) * 1000
    nl, nh = pvl - p['cost'], pvh - p['cost']
    if not (nl > 0 > nh):
        p['cost'] = round((pvl + pvh) / 2000) * 1000; nl, nh = pvl - p['cost'], pvh - p['cost']
    irr = lo + nl / (nl - nh) * (hi - lo)
    intro = (f'{co(r)} is considering {p["asset"]} costing {m(p["cost"])} with cash inflows {_flows_text(p, False)}. Its cost of capital is {coc}%. Discount factors at 10%: ' + ', '.join(f'{d:.3f}' for d in dl) + '; at 20%: ' + ', '.join(f'{d:.3f}' for d in dh) + '.')
    parts = [
        lambda r: ('Calculate the NPV at 10% and at 20%.', f'{m(nl)}; {m(nh)}', '[4]'),
        lambda r: ('Estimate the IRR by interpolation.', f'{irr:.1f}%', f'10 + {m(nl)}/{m(nl - nh)} × 10 [2]'),
        lambda r: ('Advise whether the project should go ahead.', f'IRR {irr:.1f}% {"exceeds" if irr > coc else "is below"} the cost of capital of {coc}%, so {"accept" if irr > coc else "reject"}; margin of safety {irr - coc:.1f} percentage points.', 'Comparison [1]; decision [1]; other factor [1] [3]'),
        lambda r: ('Explain what the IRR tells the directors about the project\'s risk.', 'It shows the maximum cost of capital the project can bear before NPV becomes negative; a small gap above the cost of capital means little margin for error.', '[2]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t12_3.add('C4', (2, 3, 4, 5), 'multi_step')(_irr_c4)
t12_3.add('C3', (4, 5), 'multi_step')(_irr_c4)


@t12_3.add('C2', (2, 3, 4), 'explain')
def t123_err(r, D):
    lo, hi = r.choice([(8, 14), (10, 16), (10, 20), (12, 18)])
    nl, nh = step(r, 2000, 40000, 100), -step(r, 2000, 40000, 100)
    if abs(nl + nh) < 500:
        nh -= 1500
    right = lo + nl / (nl - nh) * (hi - lo)
    wrong = lo + nl / (nl + nh) * (hi - lo)
    return {'stem': f'A project has an NPV of {m(nl)} at {lo}% and {m(nh)} at {hi}%. A student estimated the IRR as {wrong:.1f}% using {lo} + {m(nl)}/({m(nl)} − {m(-nh)}) × {hi - lo}. Explain the error and calculate the correct IRR.',
            'answer': f'The range between the NPVs is {m(nl)} + {m(-nh)} = {m(nl - nh)} because one NPV is negative; IRR = {lo} + {m(nl)}/{m(nl - nh)} × {hi - lo} = {right:.1f}%.',
            'key': f'Denominator should be the total difference {m(nl - nh)} [1]; method [1]; IRR {right:.1f}% [1] [3]'}


t12_4 = topic('Sensitivity analysis and non-financial factors in capital investment', 'sensitivity analysis and non-financial factors in capital investment', 'sensitivity analysis', 'non-financial factors')
fixed(t12_4, 'C1', (1, 2), [
    ('Sensitivity analysis in investment appraisal shows', 'how much a variable can change before the project\'s NPV becomes zero', 'Sensitivity = NPV / PV of the variable × 100 [1].',
     ['the exact future cash flows', 'the payback period', 'the accounting profit']),
    ('A project whose NPV becomes negative after a 2% fall in sales volume is', 'highly sensitive to sales volume', 'Small margin → high sensitivity/risk [1].',
     ['not sensitive to sales volume', 'risk-free', 'certain to make a loss']),
    ('Which is a non-financial factor in a capital investment decision?', 'The effect on employee morale and the local community', 'Non-financial: staff, environment, reputation, legal, flexibility [1].',
     ['The NPV of the project', 'The discount rate', 'The residual value']),
])
fixed(t12_4, 'C2', (2, 3, 4), [
    ('Explain two limitations of sensitivity analysis.', 'It changes one variable at a time while others are held constant; it does not give the probability of a change; it does not tell managers what decision to make.',
     'Two limitations [1 each] + explanation [1 each] [4]'),
    ('Explain why non-financial factors should be considered alongside NPV.', 'Some effects (environmental impact, staff morale, reputation, legal requirements, strategic fit) are hard to quantify but can affect long-term success or the reliability of forecasts.',
     'Hard to quantify but important [1]; two examples [1] [2]'),
])


@t12_4.add('C3', (1, 2, 3, 4, 5))
def t124_sens(r, D):
    p = _proj(r, D, r.choice([3, 4, 5]))
    rate = r.choice([8, 10, 12])
    df = dfs(rate, p['n'])
    ann = step(r, 30000, 150000, 1000)
    af = sum(df)
    pv = ann * af
    cost = round(pv * r.uniform(0.75, 0.95) / 1000) * 1000
    npv = pv - cost
    var = r.choice(['annual net cash inflow', 'initial investment'])
    if var == 'annual net cash inflow':
        s = npv / pv * 100
    else:
        s = npv / cost * 100
    stem = f'{co(r)} plans to invest {m(cost)} in {p["asset"]} producing an annual net cash inflow of {m(ann)} for {p["n"]} years. The cost of capital is {rate}% (cumulative discount factor {af:.3f}).'
    key = f'PV of inflows {m(ann)} × {af:.3f} = {m(pv)} [1]; NPV {m(npv)} [1]; sensitivity of {var} = {m(npv)} / {m(pv if var.startswith("annual") else cost)} × 100 = {s:.1f}% [1]'
    if D == 1:
        opts, ans = mm(r, npv, [ann * p['n'] - cost, pv, npv * 1.5, cost - pv + 2 * npv])
        return {'stem': stem + ' What is the NPV?', 'options': opts, 'answer': ans, 'key': key}
    q = f' Calculate the NPV and the percentage by which the {var} could {"fall" if var.startswith("annual") else "rise"} before the project ceases to be worthwhile.'
    if D >= 4:
        q += ' Comment on the risk of the project.'
        key += ' ; comment linked to size of margin [1]'
    return {'stem': stem + q, 'answer': f'NPV {m(npv)}; sensitivity {s:.1f}%' + ('; ' + ('low margin, high risk' if s < 10 else 'reasonable margin of safety') if D >= 4 else ''), 'key': key, 'marks': 3 + (D >= 4)}


def _sens_c4(r, D):
    p = _proj(r, D, 4)
    rate = r.choice([10, 12])
    df = dfs(rate, 4); af = sum(df)
    units = step(r, 5000, 30000, 500); cont = r.choice([6, 8, 10, 12, 15]); fixed = step(r, 10000, 60000, 1000)
    ann = units * cont - fixed
    pv = ann * af
    cost = round(pv * r.uniform(0.75, 0.92) / 1000) * 1000
    npv = pv - cost
    s_vol = npv / (units * cont * af) * 100
    s_fix = npv / (fixed * af) * 100
    loc = r.choice(['a rural area with high unemployment', 'a river valley protected for wildlife', 'a busy industrial zone', 'a coastal town reliant on tourism'])
    intro = (f'{co(r)} is considering a factory in {loc}, costing {m(cost)}, lasting 4 years. It will sell {nm(units)} units a year at a contribution of ${cont} per unit; extra cash fixed costs are {m(fixed)} a year. Cost of capital {rate}%; cumulative discount factor for 4 years {af:.3f}.')
    parts = [
        lambda r: ('Calculate the NPV.', m(npv), f'Annual cash flow {nm(units)} × ${cont} − {m(fixed)} = {m(ann)} [1]; × {af:.3f} = {m(pv)} [1]; − {m(cost)} = {m(npv)} [1] [3]'),
        lambda r: ('Calculate the percentage fall in sales volume that would reduce the NPV to zero.', pc(s_vol), f'{m(npv)} / PV of contribution {m(units * cont * af)} × 100 [2]'),
        lambda r: ('Calculate the percentage increase in fixed costs that would reduce the NPV to zero.', pc(s_fix), f'{m(npv)} / PV of fixed costs {m(fixed * af)} × 100 [2]'),
        lambda r: ('Discuss two non-financial factors the directors should consider.', f'Location in {loc}: effect on local employment, environmental impact and public opinion, availability of skilled labour, transport links, government grants/regulation.', '[4]'),
        lambda r: ('Advise the directors whether to proceed.', f'NPV {m(npv)} positive, but volume can fall only {s_vol:.1f}% — ' + ('sensitive, so research demand further' if s_vol < 10 else 'reasonable margin') + '; weigh non-financial factors.', 'Uses NPV and sensitivity [2]; recommendation [1] [3]'),
    ]
    return compose(r, intro, parts, k=(2, 3, 4), type_='multi_step')


t12_4.add('C4', (2, 3, 4, 5), 'multi_step')(_sens_c4)
t12_4.add('C3', (4, 5), 'multi_step')(_sens_c4)
t12_2.add('C4', (3, 4, 5), 'multi_step')(_sens_c4)


@t12_4.add('C2', (2, 3, 4), 'explain')
def t124_nf(r, D):
    s = r.choice([('replacing 40 workers with robots', 'staff morale, redundancy costs and union relations; loss of flexibility; reputation'),
                  ('building a plant near a national park', 'environmental damage, planning permission, public protests and brand image'),
                  ('buying machinery from a new overseas supplier', 'reliability of supply, after-sales service, exchange-rate risk and quality'),
                  ('opening a branch in a politically unstable country', 'political and legal risk, safety of staff, repatriation of profits'),
                  ('switching to a cheaper, less durable packaging material', 'customer perception of quality, environmental impact and returns')])
    npv = step(r, 5000, 200000, 1000)
    return {'stem': f'{co(r)} has calculated a positive NPV of {m(npv)} for {s[0]}. Explain two non-financial factors the directors should consider before deciding.', 'answer': s[1].capitalize() + '.',
            'key': 'Two relevant non-financial factors [1 each]; explanation of impact on the decision [1 each] [4]'}


CHAPTERS[12] = [t12_1, t12_2, t12_3, t12_4]


# ----------------------------------------------------------------------------- marks from keys
_TOT = re.compile(r'\[(\d+)\]\s*\[(\d+)\]\s*$')
_ALL = re.compile(r'\[(\d+)(?: each)?\]')


def _key_marks(key):
    m_ = _TOT.search(key)
    if m_:
        return int(m_.group(2))
    xs = [int(x) for x in _ALL.findall(key)]
    return sum(xs) if xs else None


def _auto_marks(fn):
    def g(r, D):
        q = fn(r, D)
        if q and 'marks' not in q and not q.get('options'):
            k = _key_marks(q['key'])
            if k:
                q['marks'] = max(1, min(20, k))
        return q
    g.__name__ = fn.__name__
    return g


for _tops in CHAPTERS.values():
    for _t in _tops:
        for _tp in _t.templates:
            if not getattr(_tp, '_am', False) and _tp.name not in ('fixed', 'pair'):
                _tp.fn = _auto_marks(_tp.fn)
                _tp._am = True
