"""CBSE class 12 entrepreneurship (066) families: Unit 5 Business Arithmetic and Unit 6 capital requirement.

Computed problems (exact arithmetic with fractions): unit price, cost and margin; break-even point and margin of
safety; EOQ, stock turnover and FIFO inventory valuation; ROI, ROE, current ratio and debt-equity ratio; cash flow
projections and income statements; fixed and working capital estimation with means of finance. Each subtopic also
has a short fact table (g12_business_a.spec + g12_entrepreneurship_a.efacts).
Mock kinds: 'mcq', 'ar', 'm2', 'm3', 'm5'; computed problems use 'm2c', 'm3c', 'm5c'.
"""
from __future__ import annotations

from fractions import Fraction as Fr
from math import isqrt

from g11_accountancy_kit import FF, ctx
from g12_business_a import spec
from g12_entrepreneurship_a import efacts, S
from qbank import inr, mcq, num


def ri(r, lo, hi, step=1):
    return r.randrange(lo // step, hi // step + 1) * step


def pc(x) -> str:
    """Percentage text: up to 2 decimals."""
    return num(float(x), 2) + '%'


def rs(x) -> str:
    x = Fr(x)
    if x.denominator == 1:
        return inr(int(x))
    return inr(round(float(x), 2))


def wrong_money(ans, cands, r):
    out, seen = [], {rs(ans)}
    for c in list(cands) + [ans * 2, ans + 10, ans - 10 if ans > 20 else ans + 25, ans * Fr(3, 2), ans + 5]:
        if c is None or c <= 0:
            continue
        s = rs(c)
        if s not in seen:
            out.append(s)
            seen.add(s)
    if len(out) < 3:
        raise ValueError('few distractors')
    return out[:3]


def wrong_num(ans, cands, unit=''):
    out, seen = [], {num(float(ans), 2) + unit}
    for c in list(cands) + [ans * 2, ans + 1, ans * Fr(1, 2), ans + 2, ans + 10]:
        if c is None or c <= 0:
            continue
        s = num(float(c), 2) + unit
        if s not in seen:
            out.append(s)
            seen.add(s)
    return out[:3]


# ================================================================ ch05 st1 unit of sale, price, cost, margin

BUSINESSES = [
    # (type, business, unit of sale, unit word plural, price range, cost share range)
    ('manufacturing', 'a bakery', 'one cake', 'cakes', (300, 900)),
    ('manufacturing', 'a candle-making unit', 'one candle', 'candles', (60, 250)),
    ('manufacturing', 'a furniture workshop', 'one chair', 'chairs', (1500, 5000)),
    ('trading', 'a stationery shop', 'one notebook', 'notebooks', (40, 120)),
    ('trading', 'a mobile accessories store', 'one phone cover', 'phone covers', (150, 600)),
    ('trading', 'a fruit shop', 'one kilogram of apples', 'kilograms of apples', (120, 260)),
    ('service', 'a tiffin service', 'one meal box', 'meal boxes', (80, 200)),
    ('service', 'a tuition centre', 'one student per month', 'student-months', (1500, 4000)),
    ('service', 'a car-wash centre', 'one car washed', 'car washes', (250, 700)),
    ('service', 'a guest house', 'one room per night', 'room-nights', (1200, 3500)),
    ('service', 'a tailoring shop', 'one shirt stitched', 'shirts stitched', (300, 900)),
]


def _ub(r):
    t, biz, unit, plural, (lo, hi) = r.choice(BUSINESSES)
    d = ctx(r)
    return t, biz, unit, plural, lo, hi, d


def u_margin_mcq(r):
    t, biz, unit, plural, lo, hi, d = _ub(r)
    price = ri(r, lo, hi, 10 if hi < 1000 else 50)
    cost = price * r.choice([Fr(1, 2), Fr(3, 5), Fr(7, 10), Fr(3, 4), Fr(4, 5), Fr(13, 20)])
    if cost.denominator != 1:
        raise ValueError
    m = price - cost
    return mcq(f'{d["p"]} runs {biz}. The unit of sale is {unit}, sold at {rs(price)}; the unit cost is {rs(cost)}. What is the unit margin?',
               rs(m), wrong_money(m, [price + cost, cost, m * 2, price], r),
               f'Unit margin = unit price − unit cost = {rs(price)} − {rs(cost)} = {rs(m)}.', r)


def u_cost2(r):
    t, biz, unit, plural, lo, hi, d = _ub(r)
    for _ in range(200):
        n = ri(r, 200, 3000, 50)
        uc = ri(r, lo // 2, hi * 4 // 5, 5)
        total = n * uc
        rent = ri(r, total // 10, total // 4, 500)
        mat = total - rent - ri(r, total // 10, total // 4, 500)
        lab = total - rent - mat
        if mat > 0 and lab > 0:
            break
    else:
        raise ValueError
    price = uc + ri(r, max(5, uc // 10), max(10, uc // 2), 5)
    m = price - uc
    stem = (f'{d["p"]} runs {biz} in {d["c"]}. In a month {he_she(d)} sold {ind(n)} {plural} at {rs(price)} each (unit of sale: {unit}). '
            f'The month\'s costs were: materials {inr(mat)}, wages {inr(lab)}, rent and other expenses {inr(rent)}. Calculate the unit cost and the unit margin.')
    ans = f'Total cost = {inr(total)}; unit cost = {inr(total)} ÷ {ind(n)} = {rs(uc)}; unit margin = {rs(price)} − {rs(uc)} = {rs(m)}.'
    return {'stem': stem, 'answer': ans, 'key': f'1 mark for unit cost, 1 mark for unit margin. {ans}'}


def he_she(d):
    return d['he']


def ind(n: int) -> str:
    return inr(n)[1:]


def u_target3(r):
    t, biz, unit, plural, lo, hi, d = _ub(r)
    uc = ri(r, lo // 2, hi * 3 // 4, 10)
    mk = r.choice([10, 20, 25, 30, 40, 50])
    price = Fr(uc * (100 + mk), 100)
    if price.denominator != 1:
        raise ValueError
    n = ri(r, 100, 2000, 50)
    tm = (price - uc) * n
    stem = (f'{d["p"]} runs {biz}, where the unit of sale is {unit}. The unit cost is {rs(uc)}. {d["He"]} wants a unit margin of {mk}% on cost. '
            f'(a) What unit price should {d["he"]} charge? (b) What will be the total margin if {ind(n)} {plural} are sold in a month? '
            f'(c) Express the unit margin as a percentage of the unit price.')
    mp = Fr(price - uc, price) * 100
    ans = (f'(a) Unit price = {rs(uc)} + {mk}% of {rs(uc)} = {rs(price)}. (b) Unit margin {rs(price - uc)} × {ind(n)} = {rs(tm)}. '
           f'(c) {rs(price - uc)} ÷ {rs(price)} × 100 = {pc(mp)}.')
    return {'stem': stem, 'answer': ans, 'key': f'1 mark each for (a), (b) and (c). {ans}'}


def u_compare5(r):
    d = ctx(r)
    for _ in range(200):
        items = []
        for nm in r.sample(['chocolate cake', 'cupcake box', 'loaf of bread', 'cookie jar', 'fruit tart', 'pizza base'], 2):
            p = ri(r, 80, 900, 10)
            mat = ri(r, p // 5, p // 2, 5)
            lab = ri(r, p // 10, p // 4, 5)
            oh = ri(r, 5, p // 8, 5)
            q = ri(r, 100, 1500, 50)
            items.append((nm, p, mat, lab, oh, q))
        ok = all(p - (m + l + o) > 0 for (_, p, m, l, o, _) in items)
        (a, b) = items
        ua = a[1] - sum(a[2:5])
        ub = b[1] - sum(b[2:5])
        ta, tb = ua * a[5], ub * b[5]
        if ok and ua != ub and ta != tb and (ua > ub) != (ta > tb):
            break
    else:
        raise ValueError
    rows = ' '.join(f'{nm.capitalize()}: unit price {rs(p)}, material {rs(m)}, labour {rs(l)}, overhead {rs(o)} per unit, monthly sales {ind(q)} units.'
                    for (nm, p, m, l, o, q) in items)
    stem = (f'{d["f"]}, a bakery in {d["c"]}, makes two products. {rows} '
            f'(a) Calculate the unit cost and unit margin of each product. (b) Calculate the total monthly margin from each. '
            f'(c) Which product earns more per unit and which earns more in total? Why do the two answers differ?')
    best_unit = a[0] if ua > ub else b[0]
    best_tot = a[0] if ta > tb else b[0]
    ans = (f'(a) {a[0].capitalize()}: unit cost {rs(sum(a[2:5]))}, unit margin {rs(ua)}; {b[0]}: unit cost {rs(sum(b[2:5]))}, unit margin {rs(ub)}. '
           f'(b) {a[0].capitalize()}: {rs(ua)} × {ind(a[5])} = {rs(ta)}; {b[0]}: {rs(ub)} × {ind(b[5])} = {rs(tb)}. '
           f'(c) The {best_unit} earns more per unit, but the {best_tot} earns more in total, because total margin = unit margin × number of units '
           f'and the {best_tot} sells many more units.')
    return {'stem': stem, 'answer': ans, 'key': f'(a) 2 marks, (b) 2 marks, (c) 1 mark. {ans}'}


CH05_ST1 = spec('''
T: Unit of sale | The basic unit in which a business sells its product or service, such as one cake, one kilogram or one hour.
T: Unit price | The price at which one unit of sale is sold.
T: Unit cost | The total cost of producing or buying and selling one unit of sale.
T: Unit margin | The difference between the unit price and the unit cost.
T: Mark-up | The amount added to the unit cost to arrive at the unit price.
L: uos | units of sale for different types of business | -
- Manufacturing business | One unit of the product made, such as one chair or one cake.
- Trading business | One unit of the goods bought and resold, such as one notebook or one kilogram of rice.
- Service business | One unit of service, such as one hour, one haircut or one room per night.
Q: What is the most suitable unit of sale? | One piece; One kilogram; One hour of service; One plate (meal); One room per night; One student per month | -
- {p} runs a cyber café in {c} and charges customers by time. | One hour of service | Service is sold by time.
- {p} runs a guest house in a hill town. | One room per night | Hotels sell room-nights.
- {p} sells rice and pulses loose from sacks. | One kilogram | Loose goods are sold by weight.
- {p} runs a roadside eatery that serves thalis. | One plate (meal) | Meals are sold by the plate.
- {p} makes handmade wooden toys. | One piece | Each toy is a unit.
- {p} runs a coaching centre that charges a monthly fee. | One student per month | Fees are charged per student per month.
A: Unit margin is the difference between unit price and unit cost. | It shows how much each unit sold contributes to profit. | a | Both true; R explains A.
A: The unit of sale is the same for all businesses. | A guest house sells room-nights while a bakery sells cakes. | d | A is false: it differs by the type of business. R is true.
A: A negative unit margin means a loss on every unit sold. | The unit cost is then higher than the unit price. | a | Both true; R explains A.
A: Raising the unit price always raises the total margin. | Unit margin equals unit price minus unit cost. | d | A is false: a higher price may reduce the number of units sold. R is true.
TT: unit economics
S+: Unit margin equals unit price minus unit cost.
S+: The unit of sale of a guest house is one room per night.
S+: A trading business buys and resells goods.
S+: A negative unit margin means a loss on each unit.
S-: Unit cost is the price charged to the customer.
S-: Unit margin equals unit price plus unit cost.
S-: All businesses have the same unit of sale.
S-: A service business has no unit cost.
''', cat='term', scen2=False)
CH05_ST1['ars'].append(('Unit cost of a trading business includes the purchase price of goods.',
                        'A trading business sells goods without buying them.', 'c',
                        'A is true; R is false: a trader buys goods and resells them.'))

# ================================================================ ch05 st2 break-even point and margin of safety

PRODUCTS = [('LED bulbs', 'bulb'), ('school bags', 'bag'), ('jute bags', 'bag'), ('water bottles', 'bottle'),
            ('notebooks', 'notebook'), ('candles', 'candle'), ('cotton T-shirts', 'T-shirt'), ('pickle jars', 'jar'),
            ('ceiling fans', 'fan'), ('pairs of sandals', 'pair')]


def _be(r):
    for _ in range(300):
        vc = ri(r, 20, 1500, 5)
        c = ri(r, max(5, vc // 6), max(10, vc), 5)
        sp = vc + c
        bep = ri(r, 200, 20000, 50)
        fc = bep * c
        if 50000 <= fc <= 50000000:
            prod, unit = r.choice(PRODUCTS)
            return prod, unit, sp, vc, c, fc, bep
    raise ValueError


def be_mcq(r):
    prod, unit, sp, vc, c, fc, bep = _be(r)
    d = ctx(r)
    w = [Fr(fc, sp), Fr(fc, vc)]
    w = [x for x in w if x.denominator == 1] + [bep * 2, bep + bep // 2, bep - bep // 4]
    return mcq(f'{d["f"]} makes {prod}. Fixed costs are {inr(fc)} a year, the selling price is {rs(sp)} per {unit} and the variable cost is {rs(vc)} per {unit}. '
               f'What is the break-even point in units?', f'{ind(bep)} units', [f'{ind(int(x))} units' for x in w if x != bep][:3],
               f'BEP = fixed cost ÷ (selling price − variable cost) = {inr(fc)} ÷ {rs(c)} = {ind(bep)} units.', r)


def be2(r):
    prod, unit, sp, vc, c, fc, bep = _be(r)
    d = ctx(r)
    stem = (f'{d["p"]} makes {prod} in {d["c"]}. Fixed costs are {inr(fc)} per year; selling price {rs(sp)} and variable cost {rs(vc)} per {unit}. '
            f'Calculate the break-even point in units and in sales value.')
    ans = f'Contribution per {unit} = {rs(sp)} − {rs(vc)} = {rs(c)}. BEP = {inr(fc)} ÷ {rs(c)} = {ind(bep)} units; BEP sales = {ind(bep)} × {rs(sp)} = {inr(bep * sp)}.'
    return {'stem': stem, 'answer': ans, 'key': f'1 mark for BEP in units, 1 mark for BEP in rupees. {ans}'}


def mos3(r):
    prod, unit, sp, vc, c, fc, bep = _be(r)
    d = ctx(r)
    pct = r.choice([10, 20, 25, 40, 50, 60, 75])
    act = Fr(bep * 100, 100 - pct)
    if act.denominator != 1:
        act = bep + ri(r, bep // 5, bep, 10)
    act = int(act)
    mos = act - bep
    stem = (f'{d["f"]} sells {ind(act)} {prod} a year at {rs(sp)} each. Its fixed costs are {inr(fc)} and the variable cost is {rs(vc)} per {unit}. '
            f'Calculate (a) the break-even point in units, (b) the margin of safety in units and in rupees, and (c) the margin of safety as a percentage of actual sales.')
    ans = (f'(a) BEP = {inr(fc)} ÷ ({rs(sp)} − {rs(vc)}) = {ind(bep)} units. (b) MoS = {ind(act)} − {ind(bep)} = {ind(mos)} units = {inr(mos * sp)}. '
           f'(c) {ind(mos)} ÷ {ind(act)} × 100 = {pc(Fr(mos * 100, act))}.')
    return {'stem': stem, 'answer': ans, 'key': f'1 mark each for (a), (b) and (c). {ans}'}


def target3(r):
    prod, unit, sp, vc, c, fc, bep = _be(r)
    d = ctx(r)
    k = ri(r, bep // 4, bep, 50)
    tp = k * c
    stem = (f'{d["p"]} plans to make {prod}. Fixed costs are {inr(fc)} a year, the selling price is {rs(sp)} and the variable cost is {rs(vc)} per {unit}. '
            f'How many units must {d["he"]} sell to (a) break even and (b) earn a profit of {inr(tp)}? (c) What will be the sales value in (b)?')
    n = bep + k
    ans = (f'(a) BEP = {inr(fc)} ÷ {rs(c)} = {ind(bep)} units. (b) Units = ({inr(fc)} + {inr(tp)}) ÷ {rs(c)} = {ind(n)} units. '
           f'(c) {ind(n)} × {rs(sp)} = {inr(n * sp)}.')
    return {'stem': stem, 'answer': ans, 'key': f'1 mark each for (a), (b) and (c). {ans}'}


def be5(r):
    prod, unit, sp, vc, c, fc, bep = _be(r)
    d = ctx(r)
    act = bep + ri(r, bep // 5, bep, 50)
    mos = act - bep
    profit = mos * c
    rise = c * ri(r, max(10, bep // 10), max(20, bep // 3), 10)
    nb = (fc + rise) // c
    stem = (f'{d["f"]}, a small unit in {d["c"]}, makes {prod}. Selling price {rs(sp)} per {unit}; variable cost {rs(vc)} per {unit}; fixed costs {inr(fc)} a year. '
            f'It expects to sell {ind(act)} units this year. (a) Calculate the contribution per unit and the break-even point in units. '
            f'(b) Calculate the margin of safety in units and the expected profit. (c) If rent raises fixed costs by {inr(rise)}, find the new break-even point and comment.')
    ans = (f'(a) Contribution = {rs(sp)} − {rs(vc)} = {rs(c)}; BEP = {inr(fc)} ÷ {rs(c)} = {ind(bep)} units. '
           f'(b) MoS = {ind(act)} − {ind(bep)} = {ind(mos)} units; profit = MoS × contribution = {ind(mos)} × {rs(c)} = {inr(profit)}. '
           f'(c) New BEP = {inr(fc + rise)} ÷ {rs(c)} = {ind(nb)} units; '
           + (f'expected sales still exceed it, so the firm stays profitable but its margin of safety falls to {ind(act - nb)} units.' if act > nb else
              f'expected sales are now {"equal to" if act == nb else "below"} the break-even point, so the firm must raise price, cut costs or sell more.'))
    return {'stem': stem, 'answer': ans, 'key': f'(a) 2 marks, (b) 2 marks, (c) 1 mark. {ans}'}


CH05_ST2 = spec('''
T: Break-even point | The level of sales at which total revenue equals total cost, so there is neither profit nor loss.
T: Fixed cost | A cost that does not change with the level of output, such as rent and salaries.
T: Variable cost | A cost that changes in direct proportion to output, such as raw material.
T: Contribution | Selling price minus variable cost; the amount each unit contributes to fixed costs and profit.
T: Margin of safety | The excess of actual or expected sales over break-even sales.
L: use | uses of break-even analysis for an entrepreneur | -
- Shows the minimum sales needed | The entrepreneur knows the sales required to avoid a loss.
- Helps in pricing | The effect of a price change on the BEP can be seen.
- Helps in planning profit | Sales needed for a target profit can be found.
- Shows the effect of cost changes | A rise in fixed or variable cost raises the BEP.
- Helps in convincing lenders | A low BEP and a high margin of safety show lower risk.
Q: Which type of cost is it for a small manufacturing unit? | Fixed cost; Variable cost; Semi-variable cost; Sunk cost | -
- Monthly rent of the factory shed. | Fixed cost | It does not change with output.
- Cost of raw material used in each unit. | Variable cost | It changes with output.
- Salary of the accountant. | Fixed cost | It does not change with output.
- Packing material for each unit. | Variable cost | It rises with each unit made.
- Electricity bill with a fixed monthly charge plus a charge per unit of power used. | Semi-variable cost | It has a fixed and a variable part.
- Commission paid to salespeople on each unit sold. | Variable cost | It varies with sales.
- Insurance premium of the building. | Fixed cost | It is fixed for the year.
A: At the break-even point there is neither profit nor loss. | Total revenue equals total cost at that point. | a | Both true; R explains A.
A: An increase in fixed cost lowers the break-even point. | BEP = fixed cost ÷ contribution per unit. | d | A is false: it raises the BEP. R is true.
A: A higher margin of safety means lower risk. | Sales can fall more before the business makes a loss. | a | Both true; R explains A.
A: Contribution per unit is selling price minus variable cost. | Fixed cost is included in contribution per unit. | c | A is true; R is false.
TT: break-even analysis
S+: At the break-even point, total revenue equals total cost.
S+: Rent is usually a fixed cost.
S+: A rise in variable cost per unit raises the break-even point.
S+: Margin of safety is actual sales minus break-even sales.
S-: Raw material is a fixed cost.
S-: Break-even point = fixed cost × contribution per unit.
S-: A higher margin of safety means higher risk.
S-: At the break-even point the firm earns maximum profit.
''', cat='term', scen2=False)

# ================================================================ ch05 st3 working capital management and inventory


def _eoq(r):
    for _ in range(400):
        q = r.choice([100, 150, 200, 250, 300, 400, 500, 600, 800, 1000, 1200, 1500, 2000])
        o = r.choice([40, 50, 60, 75, 80, 100, 120, 150, 200, 250, 300])
        h = r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25])
        a = Fr(q * q * h, 2 * o)
        if a.denominator == 1 and 1000 <= a <= 500000 and Fr(int(a), q).denominator == 1:
            return int(a), o, h, q
    raise ValueError


def eoq_mcq(r):
    a, o, h, q = _eoq(r)
    d = ctx(r)
    w = [isqrt(a * o // h) if a * o % h == 0 else None, isqrt(2 * a * h // o) if (2 * a * h) % o == 0 else None, q * 2, q // 2]
    w = [f'{ind(int(x))} units' for x in w if x and x != q]
    w = list(dict.fromkeys(w))
    if len(w) < 3:
        w.append(f'{ind(q + 100)} units')
    return mcq(f'{d["f"]} uses {ind(a)} units of a raw material a year. The cost of placing an order is {rs(o)} and the carrying cost is {rs(h)} per unit per year. '
               f'What is the economic order quantity?', f'{ind(q)} units', w[:3],
               f'EOQ = √(2AO ÷ C) = √(2 × {ind(a)} × {o} ÷ {h}) = √{ind(q * q)} = {ind(q)} units.', r)


def eoq2(r):
    a, o, h, q = _eoq(r)
    d = ctx(r)
    n = a // q
    stem = (f'{d["p"]} runs a small factory that needs {ind(a)} kg of raw material a year. Ordering cost is {rs(o)} per order and carrying cost is {rs(h)} per kg per year. '
            f'Calculate the economic order quantity and the number of orders to be placed in a year.')
    ans = f'EOQ = √(2 × {ind(a)} × {o} ÷ {h}) = √{ind(q * q)} = {ind(q)} kg. Number of orders = {ind(a)} ÷ {ind(q)} = {n}.'
    return {'stem': stem, 'answer': ans, 'key': f'1 mark for EOQ, 1 mark for the number of orders. {ans}'}


def _stock(r):
    for _ in range(300):
        op = ri(r, 20000, 600000, 1000)
        cl = ri(r, 20000, 600000, 1000)
        avg = Fr(op + cl, 2)
        k = r.choice([3, 4, 5, 6, 8, 10, 12])
        cogs = avg * k
        if avg.denominator == 1 and cogs.denominator == 1:
            return op, cl, int(avg), k, int(cogs)
    raise ValueError


def stock_mcq(r):
    op, cl, avg, k, cogs = _stock(r)
    d = ctx(r)
    w = [Fr(cogs, op), Fr(cogs, cl), Fr(cogs, op + cl), k * 2]
    return mcq(f'{d["f"]} had opening stock of {inr(op)} and closing stock of {inr(cl)}. Its cost of goods sold for the year was {inr(cogs)}. '
               f'What is its stock turnover ratio?', f'{k} times', wrong_num(Fr(k), w, ' times'),
               f'Average inventory = ({inr(op)} + {inr(cl)}) ÷ 2 = {inr(avg)}; stock turnover = {inr(cogs)} ÷ {inr(avg)} = {k} times.', r)


def stock3(r):
    op, cl, avg, k, cogs = _stock(r)
    d = ctx(r)
    days = Fr(360, k)
    stem = (f'{d["f"]}, a retail store in {d["c"]}, had opening stock of {inr(op)} and closing stock of {inr(cl)}. Its cost of goods sold was {inr(cogs)}. '
            f'Calculate (a) the average inventory, (b) the stock turnover ratio and (c) the average number of days stock is held (take a year of 360 days).')
    ans = (f'(a) ({inr(op)} + {inr(cl)}) ÷ 2 = {inr(avg)}. (b) {inr(cogs)} ÷ {inr(avg)} = {k} times. '
           f'(c) 360 ÷ {k} = {num(float(days), 1)} days.')
    return {'stem': stem, 'answer': ans, 'key': f'1 mark each for (a), (b) and (c). {ans}'}


def fifo3(r):
    d = ctx(r)
    for _ in range(200):
        q1, q2, q3 = ri(r, 100, 500, 50), ri(r, 100, 500, 50), ri(r, 100, 500, 50)
        p1 = ri(r, 20, 200, 2)
        p2 = p1 + ri(r, 2, 20, 2)
        p3 = p2 + ri(r, 2, 20, 2)
        sold = ri(r, q1 + 50, q1 + q2 + q3 - 50, 50)
        if sold < q1 + q2 + q3:
            break
    left = q1 + q2 + q3 - sold
    # FIFO: closing stock comes from the latest purchases.
    take3 = min(left, q3)
    take2 = min(left - take3, q2)
    take1 = left - take3 - take2
    val = take3 * p3 + take2 * p2 + take1 * p1
    parts = [f'{ind(n)} × {rs(p)}' for n, p in ((take3, p3), (take2, p2), (take1, p1)) if n]
    stem = (f'{d["f"]} bought a raw material as follows: Lot 1, {ind(q1)} units at {rs(p1)}; Lot 2, {ind(q2)} units at {rs(p2)}; Lot 3, {ind(q3)} units at {rs(p3)} '
            f'(in that order). It issued {ind(sold)} units to production. Find the number of units in closing stock and their value under the FIFO method.')
    ans = (f'Closing stock = {ind(q1 + q2 + q3)} − {ind(sold)} = {ind(left)} units. Under FIFO the earliest lots are issued first, so closing stock is from the latest lots: '
           f'{" + ".join(parts)} = {inr(val)}.')
    return {'stem': stem, 'answer': ans, 'key': f'1 mark for units in closing stock, 2 marks for the FIFO value. {ans}'}


def nwc_mcq(r):
    d = ctx(r)
    cash, debt, stock = ri(r, 10000, 200000, 1000), ri(r, 20000, 400000, 1000), ri(r, 20000, 500000, 1000)
    cred, oth = ri(r, 10000, 300000, 1000), ri(r, 5000, 100000, 1000)
    ca, cl = cash + debt + stock, cred + oth
    if ca <= cl:
        raise ValueError
    nwc = ca - cl
    return mcq(f'{d["f"]} has cash {inr(cash)}, debtors {inr(debt)}, stock {inr(stock)}, creditors {inr(cred)} and outstanding expenses {inr(oth)}. '
               f'What is its net working capital?', inr(nwc), wrong_money(nwc, [ca, ca + cl, nwc + oth], r),
               f'Net working capital = current assets ({inr(ca)}) − current liabilities ({inr(cl)}) = {inr(nwc)}.', r)


def wc5(r):
    op, cl, avg, k, cogs = _stock(r)
    a, o, h, q = _eoq(r)
    d = ctx(r)
    days = Fr(360, k)
    stem = (f'{d["p"]} runs {d["f"]}, a small manufacturing unit in {d["c"]}. (a) It uses {ind(a)} units of a component a year; ordering cost is {rs(o)} per order and '
            f'carrying cost {rs(h)} per unit per year. Find the EOQ and the number of orders a year. (b) Its opening stock of finished goods was {inr(op)}, closing stock '
            f'{inr(cl)} and cost of goods sold {inr(cogs)}. Find the stock turnover ratio and the days stock is held (360-day year). (c) State what a low stock turnover would indicate.')
    ans = (f'(a) EOQ = √(2 × {ind(a)} × {o} ÷ {h}) = {ind(q)} units; orders = {ind(a)} ÷ {ind(q)} = {a // q}. '
           f'(b) Average inventory = {inr(avg)}; stock turnover = {inr(cogs)} ÷ {inr(avg)} = {k} times; days = 360 ÷ {k} = {num(float(days), 1)} days. '
           f'(c) A low ratio shows slow-moving or excess stock, which blocks working capital and raises carrying cost.')
    return {'stem': stem, 'answer': ans, 'key': f'(a) 2 marks, (b) 2 marks, (c) 1 mark. {ans}'}


CH05_ST3 = spec('''
T: Working capital | The funds needed for day-to-day operations, invested in current assets such as stock, debtors and cash.
T: Net working capital | Current assets minus current liabilities.
T: Economic order quantity | The order size at which the total of ordering and carrying costs is the lowest.
T: Stock turnover ratio | Cost of goods sold divided by average inventory; it shows how quickly stock is sold.
T: FIFO method | A method of inventory valuation in which goods bought first are issued first, so closing stock is valued at the latest prices.
T: Weighted average method | A method of inventory valuation in which issues are priced at the average cost of all units available.
T: Reorder level | The stock level at which a fresh order should be placed.
L: wcm | aims of working capital management | -
- Ensure liquidity | Enough cash is kept to pay bills on time.
- Avoid excess current assets | Idle stock and cash earn nothing.
- Control debtors | Credit sales are collected on time.
- Use supplier credit wisely | Payables are managed to reduce cash needs.
- Keep optimum inventory | Neither shortage nor excess of stock.
Q: Which inventory concept is applied? | Economic order quantity; Reorder level; FIFO method; Weighted average method; Stock turnover ratio | -
- {f} places an order of the size at which ordering and carrying costs together are lowest. | Economic order quantity | EOQ minimises total inventory cost.
- {f} orders more fabric whenever its stock falls to 400 metres. | Reorder level | A fresh order is placed at this level.
- {f} issues the oldest stock of medicines first and values closing stock at the latest prices. | FIFO method | First in, first out.
- {f} prices every issue at the average cost of all units in stock. | Weighted average method | Issues are priced at the average cost.
- {f} measures how many times its stock is sold and replaced in a year. | Stock turnover ratio | It shows the speed of stock movement.
A: A high stock turnover ratio generally shows efficient inventory management. | Stock is being sold and replaced quickly. | a | Both true; R explains A.
A: EOQ is the order size at which total inventory cost is the lowest. | At EOQ, ordering cost and carrying cost are balanced. | a | Both true; R explains A.
A: Under FIFO, closing stock is valued at the oldest prices. | Under FIFO, goods bought first are issued first. | d | A is false: closing stock is at the latest prices. R is true.
A: Excess working capital is good for profitability. | Idle current assets earn no return. | d | A is false; R is true.
A: Working capital is needed for day-to-day operations. | Working capital is invested in land and buildings. | c | A is true; R is false: it is invested in current assets.
TT: working capital and inventory
S+: Net working capital is current assets minus current liabilities.
S+: EOQ minimises the total of ordering and carrying costs.
S+: Under FIFO, goods bought first are issued first.
S+: A low stock turnover may indicate slow-moving stock.
S-: Working capital is invested mainly in machinery.
S-: EOQ is the largest order a firm can place.
S-: Under FIFO, closing stock is valued at the oldest prices.
S-: Stock turnover ratio = average inventory × cost of goods sold.
''', cat='term', scen2=False)

# ================================================================ ch05 st4 financial ratios


def _bs(r):
    for _ in range(300):
        eq = ri(r, 500000, 5000000, 50000)
        de = r.choice([Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1), Fr(3, 2), Fr(2), Fr(2, 5)])
        debt = eq * de
        cl = ri(r, 100000, 1500000, 10000)
        cr = r.choice([Fr(1), Fr(5, 4), Fr(3, 2), Fr(7, 4), Fr(2), Fr(5, 2), Fr(3)])
        ca = cl * cr
        np_ = ri(r, 50000, 1500000, 5000)
        if debt.denominator == 1 and ca.denominator == 1:
            return int(eq), int(debt), de, cl, int(ca), cr, np_
    raise ValueError


def ratio_txt(x: Fr) -> str:
    x = Fr(x)
    return num(float(x), 2) + ':1'


def cr_mcq(r):
    eq, debt, de, cl, ca, cr, np_ = _bs(r)
    d = ctx(r)
    if r.random() < .5:
        w = [ratio_txt(1 / cr), ratio_txt(cr + 1), ratio_txt(cr * 2), '0.5:1', '4:1', '5:1']
        w = [x for x in dict.fromkeys(w) if x != ratio_txt(cr)]
        return mcq(f'{d["f"]} has current assets of {inr(ca)} and current liabilities of {inr(cl)}. What is its current ratio?',
                   ratio_txt(cr), w[:3],
                   f'Current ratio = current assets ÷ current liabilities = {inr(ca)} ÷ {inr(cl)} = {ratio_txt(cr)}. The commonly accepted ideal is 2:1.', r)
    w = [ratio_txt(1 / de), ratio_txt(de + 1), ratio_txt(de * 2), '3:1', '5:1']
    w = [x for x in dict.fromkeys(w) if x != ratio_txt(de)]
    return mcq(f'{d["f"]} has long-term debt of {inr(debt)} and shareholders\' equity of {inr(eq)}. What is its debt-equity ratio?',
               ratio_txt(de), w[:3], f'Debt-equity ratio = debt ÷ equity = {inr(debt)} ÷ {inr(eq)} = {ratio_txt(de)}.', r)


def roi2(r):
    d = ctx(r)
    inv = ri(r, 200000, 5000000, 50000)
    pct = r.choice([5, 8, 10, 12, 12.5, 15, 16, 18, 20, 24, 25])
    np_ = Fr(inv) * Fr(pct) / 100
    if np_.denominator != 1:
        raise ValueError
    stem = (f'{d["p"]} invested {inr(inv)} in {d["his"]} printing business in {d["c"]} and earned a net profit of {inr(int(np_))} this year. '
            f'Calculate the return on investment and state what it shows.')
    ans = f'ROI = net profit ÷ investment × 100 = {inr(int(np_))} ÷ {inr(inv)} × 100 = {pc(pct)}. It shows the profit earned on every ₹100 invested.'
    return {'stem': stem, 'answer': ans, 'key': f'1 mark for the calculation, 1 mark for the meaning. {ans}'}


def roe3(r):
    d = ctx(r)
    eq = ri(r, 500000, 4000000, 50000)
    debt = ri(r, 0, 3000000, 50000)
    np_ = ri(r, 50000, 1200000, 5000)
    roe = Fr(np_ * 100, eq)
    roi = Fr(np_ * 100, eq + debt)
    stem = (f'{d["f"]} has shareholders\' equity of {inr(eq)} and long-term loans of {inr(debt)}. Its net profit after tax is {inr(np_)}. '
            f'Calculate (a) return on equity and (b) return on investment (on total capital employed). (c) Why is ROE higher than ROI here?' if debt else
            f'{d["f"]} has shareholders\' equity of {inr(eq)} and no loans. Its net profit after tax is {inr(np_)}. '
            f'Calculate (a) return on equity and (b) return on investment. (c) Why are they equal here?')
    ans = (f'(a) ROE = {inr(np_)} ÷ {inr(eq)} × 100 = {pc(roe)}. (b) ROI = {inr(np_)} ÷ {inr(eq + debt)} × 100 = {pc(roi)}. '
           + (f'(c) Part of the capital is borrowed, so the profit is spread over a smaller equity base.' if debt else
              '(c) All the capital is equity, so total capital employed equals equity.'))
    return {'stem': stem, 'answer': ans, 'key': f'1 mark each for (a), (b) and (c). {ans}'}


def ratios5(r):
    eq, debt, de, cl, ca, cr, np_ = _bs(r)
    d = ctx(r)
    roi = Fr(np_ * 100, eq + debt)
    roe = Fr(np_ * 100, eq)
    stem = (f'Extracts from the books of {d["f"]}, {d["c"]}: shareholders\' equity {inr(eq)}; long-term debt {inr(debt)}; current assets {inr(ca)}; '
            f'current liabilities {inr(cl)}; net profit after tax {inr(np_)}. Calculate (a) the current ratio, (b) the debt-equity ratio, (c) the return on equity and '
            f'(d) the return on investment on total capital employed (equity + long-term debt). (e) Comment on the liquidity of the firm.')
    liq = ('satisfactory, at or above the ideal of 2:1' if cr >= 2 else 'below the ideal of 2:1, so the firm may find it hard to pay short-term debts')
    ans = (f'(a) {inr(ca)} ÷ {inr(cl)} = {ratio_txt(cr)}. (b) {inr(debt)} ÷ {inr(eq)} = {ratio_txt(de)}. (c) {inr(np_)} ÷ {inr(eq)} × 100 = {pc(roe)}. '
           f'(d) {inr(np_)} ÷ {inr(eq + debt)} × 100 = {pc(roi)}. (e) Liquidity is {liq}.')
    return {'stem': stem, 'answer': ans, 'key': f'1 mark each for (a) to (e). {ans}'}


CH05_ST4 = spec('''
T: Return on investment | Net profit as a percentage of the total investment (capital employed) in the business.
T: Return on equity | Net profit after tax as a percentage of shareholders' equity.
T: Current ratio | Current assets divided by current liabilities; a measure of short-term liquidity.
T: Debt-equity ratio | Long-term debt divided by shareholders' equity; a measure of long-term solvency.
T: Liquidity | The ability of a business to meet its short-term obligations.
L: use | uses of financial ratios for an entrepreneur | -
- Judging profitability | ROI and ROE show how well funds are being used.
- Judging liquidity | The current ratio shows the ability to pay short-term debts.
- Judging solvency | The debt-equity ratio shows dependence on borrowed funds.
- Comparison | Ratios help compare with past years and with other firms.
- Convincing lenders and investors | Good ratios show that the business is sound.
Q: Which ratio should be used? | Current ratio; Debt-equity ratio; Return on investment; Return on equity | -
- A supplier wants to know whether {f} can pay its bills within the next few months. | Current ratio | It measures short-term liquidity.
- A bank wants to know how much {f} depends on borrowed funds compared with owners' funds. | Debt-equity ratio | It measures long-term solvency.
- {p} wants to know how much profit {his} business earns on the total money invested in it. | Return on investment | It relates profit to total investment.
- The shareholders of {f} want to know the return on their own funds. | Return on equity | It relates profit to equity.
- An investor compares how well two start-ups use all the capital employed in them. | Return on investment | It measures overall profitability.
A: A current ratio of 2:1 is generally considered satisfactory. | Current assets are then twice the current liabilities, giving a cushion. | a | Both true; R explains A.
A: A high debt-equity ratio means low financial risk. | A high ratio shows heavy dependence on borrowed funds. | d | A is false: it means high risk. R is true.
A: Return on equity can be higher than return on investment. | Borrowed funds reduce the equity base on which ROE is calculated. | a | Both true; R explains A.
A: The current ratio measures liquidity. | The current ratio is calculated from long-term debt and equity. | c | A is true; R is false.
TT: financial ratios
S+: Current ratio = current assets ÷ current liabilities.
S+: Debt-equity ratio measures long-term solvency.
S+: Return on equity relates profit to shareholders' funds.
S+: A current ratio of 2:1 is generally considered satisfactory.
S-: Return on investment = investment ÷ net profit.
S-: A high debt-equity ratio means low risk.
S-: The current ratio measures long-term solvency.
S-: Debt-equity ratio = current assets ÷ equity.
''', cat='term', scen2=False)

# ================================================================ ch05 st5 cash flow projections and income statement


def cash2(r):
    d = ctx(r)
    ob = ri(r, 10000, 200000, 1000)
    cs, col = ri(r, 50000, 500000, 1000), ri(r, 20000, 300000, 1000)
    pur, wag, rent = ri(r, 30000, 400000, 1000), ri(r, 20000, 200000, 1000), ri(r, 5000, 60000, 1000)
    cb = ob + cs + col - pur - wag - rent
    if cb <= 0:
        raise ValueError
    stem = (f'For April, {d["f"]} expects: opening cash {inr(ob)}; cash sales {inr(cs)}; collections from debtors {inr(col)}; payments for purchases {inr(pur)}; '
            f'wages {inr(wag)}; rent {inr(rent)}. Prepare a brief cash flow projection and find the closing cash balance.')
    ans = (f'Receipts = {inr(cs)} + {inr(col)} = {inr(cs + col)}; payments = {inr(pur)} + {inr(wag)} + {inr(rent)} = {inr(pur + wag + rent)}. '
           f'Closing balance = {inr(ob)} + {inr(cs + col)} − {inr(pur + wag + rent)} = {inr(cb)}.')
    return {'stem': stem, 'answer': ans, 'key': f'1 mark for total receipts and payments, 1 mark for the closing balance. {ans}'}


def cash5(r):
    d = ctx(r)
    for _ in range(200):
        ob = ri(r, 20000, 150000, 1000)
        rows, bal, lines = [], ob, []
        ok = True
        for m in ('April', 'May', 'June'):
            rec = ri(r, 80000, 400000, 1000)
            pay = ri(r, 80000, 400000, 1000)
            cb = bal + rec - pay
            rows.append((m, bal, rec, pay, cb))
            bal = cb
        if any(x[4] < 0 for x in rows[:2]) or rows[2][4] == 0:
            continue
        break
    else:
        raise ValueError
    data = '; '.join(f'{m}: receipts {inr(rec)}, payments {inr(pay)}' for (m, _, rec, pay, _) in rows)
    stem = (f'{d["p"]} has started {d["f"]} in {d["c"]} with opening cash of {inr(ob)} on 1 April. Expected cash flows: {data}. '
            f'(a) Prepare a cash flow projection for the three months showing opening and closing balances. (b) Is there any month with a cash shortage? '
            f'(c) Suggest one way to manage it, or one use of the surplus.')
    body = ' '.join(f'{m}: opening {inr(o)} + receipts {inr(rec)} − payments {inr(pay)} = closing {inr(c) if c >= 0 else "−" + inr(-c)}.'
                    for (m, o, rec, pay, c) in rows)
    short = [m for (m, o, rec, pay, c) in rows if c < 0]
    ans = (f'(a) {body} (b) ' + (f'Yes, in {short[0]}: the closing balance is negative.' if short else 'No month has a cash shortage.') +
           (' (c) Arrange a short-term bank overdraft, delay a non-urgent payment or speed up collections.' if short else
            ' (c) The surplus can be kept for emergencies, used to repay a loan or invested for a short period.'))
    return {'stem': stem, 'answer': ans, 'key': f'(a) 3 marks (1 per month), (b) 1 mark, (c) 1 mark. {ans}'}


def gp_mcq(r):
    d = ctx(r)
    sales = ri(r, 500000, 5000000, 10000)
    op, pur, cl = ri(r, 50000, 400000, 5000), ri(r, sales // 3, sales * 2 // 3, 5000), ri(r, 50000, 400000, 5000)
    cogs = op + pur - cl
    gp = sales - cogs
    if gp <= 0:
        raise ValueError
    return mcq(f'{d["f"]} had sales of {inr(sales)}, opening stock {inr(op)}, purchases {inr(pur)} and closing stock {inr(cl)}. What is its gross profit?',
               inr(gp), wrong_money(gp, [sales - pur, sales - op - pur - cl, sales - pur + op], r),
               f'Cost of goods sold = {inr(op)} + {inr(pur)} − {inr(cl)} = {inr(cogs)}; gross profit = {inr(sales)} − {inr(cogs)} = {inr(gp)}.', r)


def _inc(r):
    for _ in range(200):
        sales = ri(r, 1000000, 10000000, 10000)
        cogs = ri(r, sales * 2 // 5, sales * 7 // 10, 10000)
        opx = ri(r, sales // 20, sales // 5, 5000)
        intr = ri(r, 0, sales // 40, 1000)
        tr = r.choice([25, 30])
        ebt = sales - cogs - opx - intr
        if ebt > 0 and (ebt * tr) % 100 == 0:
            return sales, cogs, opx, intr, tr, ebt
    raise ValueError


def inc3(r):
    sales, cogs, opx, intr, tr, ebt = _inc(r)
    d = ctx(r)
    tax = ebt * tr // 100
    stem = (f'For the year, {d["f"]} had sales of {inr(sales)}, cost of goods sold {inr(cogs)}, operating expenses {inr(opx)} and interest {inr(intr)}. '
            f'Tax is {tr}% of profit before tax. Calculate (a) gross profit, (b) profit before tax and (c) net profit after tax.')
    ans = (f'(a) {inr(sales)} − {inr(cogs)} = {inr(sales - cogs)}. (b) {inr(sales - cogs)} − {inr(opx)} − {inr(intr)} = {inr(ebt)}. '
           f'(c) Tax = {inr(tax)}; net profit = {inr(ebt)} − {inr(tax)} = {inr(ebt - tax)}.')
    return {'stem': stem, 'answer': ans, 'key': f'1 mark each for (a), (b) and (c). {ans}'}


def inc5(r):
    sales, cogs, opx, intr, tr, ebt = _inc(r)
    d = ctx(r)
    sal = ri(r, opx // 4, opx // 2, 1000)
    rent = ri(r, opx // 10, (opx - sal) // 2, 1000)
    adv = opx - sal - rent
    if adv <= 0:
        raise ValueError
    tax = ebt * tr // 100
    npat = ebt - tax
    stem = (f'Prepare a projected income statement of {d["f"]}, {d["c"]}, for its first year from: sales {inr(sales)}; cost of goods sold {inr(cogs)}; '
            f'salaries {inr(sal)}; rent {inr(rent)}; advertising {inr(adv)}; interest on loan {inr(intr)}; tax rate {tr}%. Also find the net profit as a percentage of sales.')
    ans = (f'Sales {inr(sales)} − cost of goods sold {inr(cogs)} = gross profit {inr(sales - cogs)}. Less operating expenses (salaries {inr(sal)} + rent {inr(rent)} + '
           f'advertising {inr(adv)} = {inr(opx)}) = operating profit {inr(sales - cogs - opx)}. Less interest {inr(intr)} = profit before tax {inr(ebt)}. '
           f'Less tax at {tr}% {inr(tax)} = net profit {inr(npat)}. Net profit ratio = {inr(npat)} ÷ {inr(sales)} × 100 = {pc(Fr(npat * 100, sales))}.')
    return {'stem': stem, 'answer': ans, 'key': f'1 mark each: gross profit, operating profit, profit before tax, net profit, net profit ratio. {ans}'}


CH05_ST5 = spec('''
T: Cash flow projection | An estimate of the cash receipts and payments of a business for a future period, showing the expected cash balance.
T: Income statement | A statement showing the revenue, expenses and profit or loss of a business for a period.
T: Gross profit | Sales minus the cost of goods sold.
T: Operating profit | Gross profit minus operating expenses.
T: Net profit | Profit left after all expenses, interest and tax are deducted.
T: Cash shortage | A situation in which expected payments exceed the cash available.
L: imp | importance of cash flow projections for a small enterprise | -
- Shows future cash needs | The entrepreneur knows when cash will run short.
- Helps arrange finance in advance | Overdrafts or loans can be arranged before a shortage.
- Helps use surplus cash | Idle cash can be invested or used to repay loans.
- Helps in planning payments | Purchases and expenses can be timed.
- Required by lenders | Banks ask for cash projections before lending.
Q: Where will this item appear? | Cash receipts in the cash flow projection; Cash payments in the cash flow projection; Revenue in the income statement; Expense in the income statement | -
- Cash received from debtors during the month. | Cash receipts in the cash flow projection | It is an inflow of cash.
- Rent paid in cash for the shop. | Cash payments in the cash flow projection | It is an outflow of cash.
- Credit sales made during the year. | Revenue in the income statement | Sales are revenue even if not yet received in cash.
- Depreciation on machinery for the year. | Expense in the income statement | It is a non-cash expense.
- Cash paid to suppliers for purchases. | Cash payments in the cash flow projection | It is an outflow of cash.
- Fresh capital brought in by the owner in cash. | Cash receipts in the cash flow projection | It is an inflow of cash, not revenue.
A: A profitable business can still face a cash shortage. | Profit includes credit sales that may not yet be received in cash. | a | Both true; R explains A.
A: Depreciation appears in the cash flow projection as a cash payment. | Depreciation is a non-cash expense. | d | A is false; R is true.
A: Gross profit is sales minus cost of goods sold. | Operating expenses are deducted to find gross profit. | c | A is true; R is false: they are deducted to find operating profit.
A: Banks ask for cash flow projections before lending. | Projections show whether the business can repay the loan. | a | Both true; R explains A.
TT: cash flow projections and income statements
S+: A cash flow projection shows expected receipts and payments.
S+: Gross profit is sales minus cost of goods sold.
S+: Depreciation is a non-cash expense.
S+: Net profit is found after deducting interest and tax.
S-: Depreciation is a cash payment.
S-: Gross profit is found after deducting tax.
S-: A profitable business can never face a cash shortage.
S-: Capital brought in by the owner is revenue in the income statement.
''', cat='term', scen2=False)

# ================================================================ ch06 st1 capital requirement


def _proj(r):
    land = ri(r, 0, 3000000, 50000)
    bldg = ri(r, 300000, 4000000, 50000)
    mach = ri(r, 300000, 5000000, 50000)
    furn = ri(r, 50000, 500000, 10000)
    pre = ri(r, 20000, 200000, 5000)
    rm = ri(r, 50000, 600000, 5000)
    wages = ri(r, 30000, 400000, 5000)
    ovh = ri(r, 20000, 200000, 5000)
    months = r.choice([1, 2, 3])
    return land, bldg, mach, furn, pre, rm, wages, ovh, months


def wc2(r):
    land, bldg, mach, furn, pre, rm, wages, ovh, months = _proj(r)
    d = ctx(r)
    wc = (rm + wages + ovh) * months
    stem = (f'{d["p"]} is planning a small unit in {d["c"]}. Monthly needs: raw material {inr(rm)}, wages {inr(wages)}, other expenses {inr(ovh)}. '
            f'The operating cycle is {months} month{"s" if months > 1 else ""}. Estimate the working capital required.')
    ans = f'Monthly requirement = {inr(rm)} + {inr(wages)} + {inr(ovh)} = {inr(rm + wages + ovh)}; working capital = {inr(rm + wages + ovh)} × {months} = {inr(wc)}.'
    return {'stem': stem, 'answer': ans, 'key': f'1 mark for the monthly requirement, 1 mark for the working capital. {ans}'}


def fc_mcq(r):
    land, bldg, mach, furn, pre, rm, wages, ovh, months = _proj(r)
    d = ctx(r)
    fc = land + bldg + mach + furn + pre
    return mcq(f'For a new project, {d["f"]} needs land {inr(land)}, building {inr(bldg)}, machinery {inr(mach)}, furniture {inr(furn)}, preliminary expenses {inr(pre)} '
               f'and raw material for one month {inr(rm)}. What is the fixed capital required?', inr(fc),
               wrong_money(fc, [fc + rm, fc - pre, land + bldg + mach], r),
               f'Fixed capital = land + building + machinery + furniture + preliminary expenses = {inr(fc)}. Raw material is working capital.', r)


def proj3(r):
    land, bldg, mach, furn, pre, rm, wages, ovh, months = _proj(r)
    d = ctx(r)
    fc = land + bldg + mach + furn + pre
    wc = (rm + wages + ovh) * months
    stem = (f'{d["p"]} plans a food-processing unit. Costs: land {inr(land)}, building {inr(bldg)}, machinery {inr(mach)}, furniture {inr(furn)}, preliminary expenses '
            f'{inr(pre)}. Monthly raw material {inr(rm)}, wages {inr(wages)} and other expenses {inr(ovh)}; working capital is needed for {months} month{"s" if months > 1 else ""}. '
            f'Calculate (a) fixed capital, (b) working capital and (c) total cost of the project.')
    ans = f'(a) Fixed capital = {inr(fc)}. (b) Working capital = {inr(rm + wages + ovh)} × {months} = {inr(wc)}. (c) Total project cost = {inr(fc + wc)}.'
    return {'stem': stem, 'answer': ans, 'key': f'1 mark each for (a), (b) and (c). {ans}'}


def proj5(r):
    land, bldg, mach, furn, pre, rm, wages, ovh, months = _proj(r)
    d = ctx(r)
    fc = land + bldg + mach + furn + pre
    wc = (rm + wages + ovh) * months
    tot = fc + wc
    own = r.choice([20, 25, 30, 40])
    sub = r.choice([0, 10, 15])
    if (tot * own) % 100 or (tot * sub) % 100:
        raise ValueError
    o, s = tot * own // 100, tot * sub // 100
    loan = tot - o - s
    sub_txt = f' A government subsidy of {sub}% of the project cost is available.' if sub else ''
    stem = (f'{d["p"]} is setting up {d["f"]} in {d["c"]}. Land {inr(land)}; building {inr(bldg)}; machinery {inr(mach)}; furniture {inr(furn)}; preliminary expenses {inr(pre)}; '
            f'monthly raw material {inr(rm)}, wages {inr(wages)}, other expenses {inr(ovh)}, with working capital for {months} month{"s" if months > 1 else ""}. '
            f'{d["He"]} will contribute {own}% of the project cost as promoter\'s capital.{sub_txt} The rest will be a bank loan. '
            f'(a) Calculate fixed capital, working capital and total project cost. (b) Show the means of finance.')
    mf = f'promoter\'s capital {own}% = {inr(o)}' + (f'; subsidy {sub}% = {inr(s)}' if sub else '') + f'; bank loan = {inr(loan)}; total = {inr(tot)}'
    ans = f'(a) Fixed capital = {inr(fc)}; working capital = {inr(rm + wages + ovh)} × {months} = {inr(wc)}; total project cost = {inr(tot)}. (b) Means of finance: {mf}.'
    return {'stem': stem, 'answer': ans, 'key': f'(a) 3 marks (1 each), (b) 2 marks. {ans}'}


CH06_ST1 = spec('''
T: Capital requirement | The total funds needed to start and run a business, made up of fixed and working capital.
T: Fixed capital | Funds invested in long-term assets such as land, building, machinery and furniture.
T: Working capital | Funds needed for day-to-day operations, such as raw material, wages and other expenses for the operating cycle.
T: Preliminary expenses | Expenses incurred before the business starts, such as registration and legal fees.
T: Means of finance | The sources from which the project cost will be met, such as promoter's capital, loans and subsidies.
T: Promoter's contribution | The part of the project cost brought in by the entrepreneur from own funds.
L: fac | factors affecting the capital requirement of an enterprise | -
- Nature of business | Manufacturing needs more capital than trading or services.
- Scale of operations | A larger scale needs more capital.
- Technology used | Automated technology needs more fixed capital.
- Length of the operating cycle | A longer cycle needs more working capital.
- Credit policy | Liberal credit to customers needs more working capital.
- Seasonal demand | Seasonal businesses need more working capital in the peak season.
Q: Is this part of fixed capital or working capital? | Fixed capital; Working capital; Neither (it is a source of finance); Neither (it is a revenue receipt) | -
- Cost of machinery for the new unit. | Fixed capital | It is a long-term asset.
- Money needed to buy raw material for two months. | Working capital | It is a day-to-day need.
- Cost of the factory building. | Fixed capital | It is a long-term asset.
- Wages to be paid until sales begin to bring in cash. | Working capital | It is a day-to-day need.
- A term loan from a bank. | Neither (it is a source of finance) | It is a means of finance.
- Registration and legal fees paid before starting the business. | Fixed capital | Preliminary expenses are part of the fixed project cost.
- Stock of finished goods kept for sale. | Working capital | It is a current asset.
- Cash received from customers for goods sold. | Neither (it is a revenue receipt) | It is income, not capital needed.
A: A manufacturing business needs more fixed capital than a trading business. | It needs plant and machinery for production. | a | Both true; R explains A.
A: Working capital is needed for the length of the operating cycle. | Cash is tied up until goods are sold and money is collected. | a | Both true; R explains A.
A: A bank loan is a part of the cost of the project. | A bank loan is a means of finance. | d | A is false: it is a source of finance, not a cost. R is true.
A: Preliminary expenses are part of the project cost. | Preliminary expenses are incurred only after sales begin. | c | A is true; R is false: they are incurred before the business starts.
TT: capital requirement
S+: Fixed capital is invested in long-term assets.
S+: Working capital is needed for day-to-day operations.
S+: Total project cost = fixed capital + working capital.
S+: Preliminary expenses are incurred before the business starts.
S-: Raw material is part of fixed capital.
S-: A bank loan is part of the cost of the project.
S-: Working capital is invested in land and building.
S-: A trading firm needs more machinery than a factory.
''', cat='term', scen2=False)

FAMILIES = {S + k: efacts(v) for k, v in {
    '05-st1': CH05_ST1, '05-st2': CH05_ST2, '05-st3': CH05_ST3, '05-st4': CH05_ST4, '05-st5': CH05_ST5, '06-st1': CH06_ST1,
}.items()}

FAMILIES[S + '05-st1'] += [FF('C2', 'D2', 'mcq', u_margin_mcq), FF('C3', 'D3', 'numerical', u_cost2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', u_target3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D4', 'numerical', u_compare5, marks=5, kinds=('m5c',))]
FAMILIES[S + '05-st2'] += [FF('C2', 'D2', 'mcq', be_mcq), FF('C3', 'D2', 'numerical', be2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', mos3, marks=3, kinds=('m3c',)),
                           FF('C3', 'D4', 'numerical', target3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D4', 'numerical', be5, marks=5, kinds=('m5c',))]
FAMILIES[S + '05-st3'] += [FF('C2', 'D2', 'mcq', eoq_mcq), FF('C2', 'D2', 'mcq', stock_mcq), FF('C2', 'D2', 'mcq', nwc_mcq),
                           FF('C3', 'D3', 'numerical', eoq2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', stock3, marks=3, kinds=('m3c',)),
                           FF('C3', 'D4', 'numerical', fifo3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D5', 'numerical', wc5, marks=5, kinds=('m5c',))]
FAMILIES[S + '05-st4'] += [FF('C2', 'D2', 'mcq', cr_mcq), FF('C3', 'D2', 'numerical', roi2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', roe3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D4', 'numerical', ratios5, marks=5, kinds=('m5c',))]
FAMILIES[S + '05-st5'] += [FF('C2', 'D2', 'mcq', gp_mcq), FF('C3', 'D2', 'numerical', cash2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', inc3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D4', 'numerical', inc5, marks=5, kinds=('m5c',)),
                           FF('C4', 'D5', 'numerical', cash5, marks=5, kinds=('m5c',))]
FAMILIES[S + '06-st1'] += [FF('C2', 'D2', 'mcq', fc_mcq), FF('C3', 'D2', 'numerical', wc2, marks=2, kinds=('m2c',)),
                           FF('C3', 'D3', 'numerical', proj3, marks=3, kinds=('m3c',)),
                           FF('C4', 'D4', 'numerical', proj5, marks=5, kinds=('m5c',))]
