"""CBSE class 11 Economics families: Introductory Microeconomics chapters 9-13 (answers computed in code)."""
from __future__ import annotations

import math
from fractions import Fraction

from qbank import mcq, num, inr, name, frac
from g11_economics_lib import M, W, AR, G, pick_example, classify, cp, table

S = 'cbse-g11-economics-ch'
Q3 = dict(marks=3, kinds=('q3',))
Q4 = dict(marks=4, kinds=('q4',))
CASE = dict(marks=4, kinds=('case',))
ROMAN = ['i', 'ii', 'iii', 'iv', 'v']
LET = 'ABCDEFGH'


def d2(x):
    return num(round(float(x), 2), 2)


def alts(ans, cands, pad=()):
    """Distinct wrong answers (strings), excluding the answer."""
    out, seen = [], {str(ans)}
    for c in list(cands) + list(pad):
        c = str(c)
        if c not in seen:
            out.append(c)
            seen.add(c)
    return out


def ndist(ans, *c):
    ans = float(ans)
    return alts(num(ans), [num(float(x)) if not isinstance(x, str) else x for x in c], [num(ans + 1), num(ans - 1), num(ans * 2), num(ans + 5)])


def units(n):
    return f'{n} unit' if n == 1 else f'{n} units'


def opts_fixed(stem, ans, opts, key, r):
    return mcq(stem, ans, [o for o in opts if o != ans][:3], key, r)


def cumsum(xs):
    out, t = [], 0
    for x in xs:
        t += x
        out.append(t)
    return out


def parts(qs):
    return '\n'.join(f'({ROMAN[i]}) {q}' for i, q in enumerate(qs))


def pans(xs):
    return '; '.join(f'({ROMAN[i]}) {a}' for i, a in enumerate(xs))


def cls_e(e):
    e = float(e)
    if abs(e - 1) < 1e-9:
        return 'unitary elastic'
    return 'elastic' if e > 1 else 'inelastic'


# ====================================================================== ch09 st1 central problems
CP_EX = [('Should the country produce more wheat or more cotton?', 'What to produce'),
         ('How many schools and how many hospitals should be built this year?', 'What to produce'),
         ('Should more consumer goods or more capital goods be produced?', 'What to produce'),
         ('Should more be spent on defence equipment or on roads?', 'What to produce'),
         ('Should cloth be woven on handlooms or on power looms?', 'How to produce'),
         ('Should a highway be built using more workers or more machines?', 'How to produce'),
         ('Should farmers plough with tractors or with bullocks?', 'How to produce'),
         ('Should electricity be generated from coal or from solar panels?', 'How to produce'),
         ('Should more goods be produced for the poor or for the rich?', 'For whom to produce'),
         ('How should the output of the economy be shared among its people?', 'For whom to produce'),
         ('Should the government supply free food grains to poor families?', 'For whom to produce'),
         ('Who should get a larger share of output: workers or owners of capital?', 'For whom to produce')]
CP_OPTS = ['What to produce', 'How to produce', 'For whom to produce', 'Where to sell']


def cp_classify(r):
    x, c = cp('cpx', r, CP_EX)
    return opts_fixed(f'Which central problem of an economy is involved in the question: "{x}"', c, CP_OPTS, f'This is the problem of {c.lower()}.', r)


def cp_case(r):
    xs = r.sample(CP_EX, 4)
    if len({c for _, c in xs}) < 2:
        raise ValueError('one kind')
    land = r.choice(['Navpur', 'Sundarvan', 'Ratnadesh', 'Kalpnagar', 'Amritdesh', 'Swarnapur'])
    return {'stem': f'The planning council of an imaginary economy, {land}, has limited land, labour and capital. It is debating these questions:\n'
                    + parts([x for x, _ in xs]) + '\nIdentify the central problem involved in each question.',
            'answer': pans([c for _, c in xs]), 'key': '1 mark each (4 marks).'}


CP_FACT = [
    ('The central problems of an economy arise mainly because', 'resources are scarce and have alternative uses', ['wants are limited', 'resources are unlimited', 'prices are fixed by law'],
     'Scarcity + alternative uses force choice.'),
    ('The problem of "how to produce" is the problem of', 'choosing the technique of production', ['choosing the goods to be produced', 'distributing the output', 'fixing the price of goods'],
     'Labour-intensive or capital-intensive technique.'),
    ('The problem of "for whom to produce" is the problem of', 'distributing the output among people', ['choosing the technique', 'choosing the goods', 'increasing resources'], 'Distribution of output.'),
    ('A labour-intensive technique of production uses', 'relatively more labour and less capital', ['relatively more capital and less labour', 'only machines', 'no capital at all'], 'Labour-intensive.'),
    ('Deciding between producing more food grains and more cars is the problem of', 'what to produce', ['how to produce', 'for whom to produce', 'how to distribute income'], 'Choice of goods.'),
    ('The resources of an economy include', 'land, labour, capital and entrepreneurship', ['only money', 'only natural resources', 'only finished goods'], 'Factors of production.'),
    ('Economising of resources means', 'making the best possible use of scarce resources', ['spending as little as possible', 'producing only necessities', 'saving all income'], 'Best use of scarce resources.'),
    ('Which of these is NOT a central problem of an economy?', 'How to decorate a shop', ['What to produce', 'How to produce', 'For whom to produce'], 'The three central problems.'),
]
CP_AR = [
    ('Every economy faces the central problems of what, how and for whom to produce.', 'Resources are scarce in relation to wants and have alternative uses.', 'a', 'Scarcity is the root of the central problems.'),
    ('Choice of technique is a part of the problem of "how to produce".', 'Goods can be produced by labour-intensive or capital-intensive methods.', 'a', 'R explains A.'),
    ('The problem of "for whom to produce" is about the choice of technique.', 'It is about how the output is distributed among people.', 'd', 'A is false; R is true.'),
    ('Rich countries do not face central problems.', 'Resources are limited in every economy.', 'd', 'A is false: scarcity is universal; R is true.'),
    ('An economy must decide how much of each good to produce.', 'Producing more of one good means producing less of another when resources are fully used.', 'a', 'R explains A.'),
    ('A labour-surplus country often prefers labour-intensive techniques.', 'Capital-intensive techniques use more machines and fewer workers.', 'b',
     'Both true; R defines capital-intensive methods but the reason for A is the abundance (and low cost) of labour.'),
]
CP_WR = [
    ('Why does an economy face the central problems? Explain briefly.', 'Wants are unlimited, resources are scarce and have alternative uses; so the economy must decide what, how and for whom to produce.',
     '1 mark each: scarcity, alternative uses, need for choice.'),
    ('Explain the central problem of "how to produce" with an example.', 'It is the choice of technique: labour-intensive (more workers, e.g. building a road with many workers) or capital-intensive (more machines, e.g. using earth movers).',
     '1 mark meaning; 2 marks example.'),
    ('Explain the central problem of "for whom to produce".', 'It concerns how output is distributed among people: who gets how much, which depends on the distribution of income; e.g. whether essential goods reach the poor.',
     '1 mark meaning; 2 marks explanation.'),
    ('Explain the central problem of "what to produce" with an example.', 'Deciding which goods and in what quantities to produce with scarce resources; e.g. more food grains or more cars, more consumer goods or more capital goods.',
     '1 mark meaning; 2 marks example.'),
]
CP_LONG = [
    ('Explain the three central problems of an economy. Why do they arise?', 'What to produce (choice of goods and quantities), how to produce (choice of technique), for whom to produce (distribution of output); '
     'they arise because resources are scarce and have alternative uses while wants are unlimited.', '1½ marks each problem; 1½ marks cause (6 marks).'),
]

# ====================================================================== ch09 st2 PPF
PAIRS = [('wheat', 'cloth'), ('guns', 'butter'), ('rice', 'sugar'), ('cars', 'computers'), ('tractors', 'textiles'), ('corn', 'cotton'), ('cement', 'steel'), ('bicycles', 'fans')]


def ppf_sched(r, constant=False):
    x, y = r.choice(PAIRS)
    n = r.choice([4, 5])
    s = r.choice([1, 2, 5, 10])
    if constant:
        mocs = [r.randint(2, 8)] * n
    else:
        mocs = sorted(r.sample(range(1, 13), n))
    xs = [i * s for i in range(n + 1)]
    ys = [sum(mocs) * s]
    for m in mocs:
        ys.append(ys[-1] - m * s)
    return x, y, xs, ys, mocs


def ppf_tab(x, y, xs, ys):
    return table(['Combination', *LET[:len(xs)]], [[f'{x.capitalize()} (units)', *xs], [f'{y.capitalize()} (units)', *ys]])


def ppf_moc(r):
    x, y, xs, ys, mocs = ppf_sched(r)
    k = r.randrange(1, len(mocs))
    m = mocs[k]
    dy, dx = ys[k] - ys[k + 1], xs[k + 1] - xs[k]
    return {'stem': f'The production possibilities of an economy are:\n{ppf_tab(x, y, xs, ys)}\nCalculate the marginal opportunity cost of moving from combination {LET[k]} to {LET[k + 1]} '
                    f'(units of {y} given up per unit of {x}).',
            'answer': num(m), 'key': f'MOC = ΔY/ΔX = ({ys[k]} − {ys[k + 1]})/({xs[k + 1]} − {xs[k]}) = {dy}/{dx} = {num(m)}.',
            'distractors': ndist(m, dy, mocs[k - 1], ys[k + 1], round(dx / dy, 2))}


def ppf_full(r):
    const = r.random() < 0.3
    x, y, xs, ys, mocs = ppf_sched(r, const)
    shape = 'constant, so the PPF is a straight line (downward sloping)' if const else 'increasing, so the PPF is concave to the origin'
    return {'stem': f'Study the production possibilities schedule:\n{ppf_tab(x, y, xs, ys)}\nCalculate the marginal opportunity cost at each step and state the shape of the PPF with reason.',
            'answer': f'MOC ({y} per unit of {x}): {", ".join(num(m) for m in mocs)}. MOC is {shape}.',
            'key': '½ mark per MOC up to 2 marks; 1 mark shape with reason (3 marks).'}


PT_OPTS = {'on': 'On the PPF: resources are fully and efficiently used', 'in': 'Inside the PPF: resources are under-utilised or used inefficiently',
           'out': 'Outside the PPF: it cannot be produced with present resources and technology'}
PT_WRONG = 'On the PPF: some resources are unemployed'


def ppf_point(r):
    x, y, xs, ys, mocs = ppf_sched(r)
    i = r.randrange(1, len(xs) - 1)
    kind = r.choice(['on', 'in', 'out'])
    d = (xs[1] - xs[0]) * r.randint(1, 3)
    yy = ys[i] if kind == 'on' else (ys[i] - d if kind == 'in' else ys[i] + d)
    if yy < 0:
        raise ValueError('neg')
    ans = PT_OPTS[kind]
    return mcq(f'The PPF of an economy is given by:\n{ppf_tab(x, y, xs, ys)}\nWhere does the combination ({xs[i]} {x}, {yy} {y}) lie and what does it show?', ans,
               [v for k, v in PT_OPTS.items() if k != kind] + [PT_WRONG],
               f'At {xs[i]} units of {x} the maximum {y} is {ys[i]}; {yy} is {"equal to" if kind == "on" else ("less than" if kind == "in" else "more than")} that.', r)


PPF_EV = [('New technology raises the production of both goods', 'PPF shifts outward (to the right)'), ('The labour force of the economy grows', 'PPF shifts outward (to the right)'),
          ('Large new deposits of minerals are discovered', 'PPF shifts outward (to the right)'), ('Huge investment adds to the stock of machines and factories', 'PPF shifts outward (to the right)'),
          ('A major earthquake destroys many factories', 'PPF shifts inward (to the left)'), ('A war destroys a large part of the capital stock', 'PPF shifts inward (to the left)'),
          ('A flood permanently damages much of the farmland', 'PPF shifts inward (to the left)'),
          ('With all resources employed, the economy produces more of one good and less of the other', 'Movement along the same PPF'),
          ('Resources are shifted from wheat to cloth production, with full employment', 'Movement along the same PPF'),
          ('Many workers become unemployed during a recession', 'The economy operates at a point inside the PPF'),
          ('Factories lie idle because of a long strike', 'The economy operates at a point inside the PPF'),
          ('A better technique raises the output of only one good', 'PPF rotates outward along the axis of that good')]


def oc_choice(r):
    who = name(r)
    kind = r.randrange(3)
    if kind == 0:
        opts = r.sample([('teacher', 'as a teacher'), ('bank clerk', 'as a bank clerk'), ('own shop', 'by running a shop'), ('call-centre job', 'in a call centre'),
                         ('tuition classes', 'by running tuition classes'), ('designer', 'as a graphic designer')], 3)
        vals = r.sample(range(18, 60), 3)
        vals = [v * 1000 for v in vals]
        ch = r.randrange(3)
        stem = (f'{who} can earn ' + ', '.join(f'{inr(v)} a month {o[1]}' for o, v in zip(opts, vals)) + f'. {who} chooses to work {opts[ch][1]}. What is the opportunity cost of this choice?')
    elif kind == 1:
        crops = r.sample(['rice', 'wheat', 'sugarcane', 'cotton', 'vegetables', 'pulses'], 3)
        vals = [v * 1000 for v in r.sample(range(30, 120), 3)]
        ch = r.randrange(3)
        stem = (f'A farmer can grow {crops[0]}, {crops[1]} or {crops[2]} on a plot of land, earning {inr(vals[0])}, {inr(vals[1])} or {inr(vals[2])} respectively. '
                f'The farmer grows {crops[ch]}. What is the opportunity cost of growing {crops[ch]}?')
    else:
        uses = r.sample(['rent it out as a shop', 'run a restaurant in it', 'use it as a warehouse', 'let it as an office', 'open a coaching centre in it'], 3)
        vals = [v * 1000 for v in r.sample(range(10, 80), 3)]
        ch = r.randrange(3)
        stem = (f'{who} owns a building and can ' + ', '.join(f'{u} (earning {inr(v)} a month)' for u, v in zip(uses, vals)) + f'. {who} decides to {uses[ch]}. What is the opportunity cost?')
    others = [v for i, v in enumerate(vals) if i != ch]
    oc = max(others)
    return {'stem': stem, 'answer': inr(oc), 'key': f'Opportunity cost = value of the next best alternative given up = {inr(oc)} (not the sum of all alternatives).',
            'distractors': alts(inr(oc), [inr(sum(others)), inr(min(others)), inr(vals[ch])], [inr(oc + 1000)])}


def mrt_num(r):
    x, y = r.choice(PAIRS)
    dx = r.choice([2, 4, 5, 10, 20])
    m = r.choice([Fraction(1, 2), Fraction(3, 2), 2, Fraction(5, 2), 3, 4, 5])
    dy = m * dx
    if Fraction(dy).denominator != 1:
        raise ValueError('frac')
    dy = int(dy)
    x1 = r.randint(1, 8) * 5
    y1 = dy + r.randint(2, 20) * 5
    return {'stem': f'When an economy raises the output of {x} from {x1} to {x1 + dx} units, the output of {y} falls from {y1} to {y1 - dy} units. Find the marginal rate of transformation.',
            'answer': num(float(m)), 'key': f'MRT = ΔY/ΔX = {dy}/{dx} = {num(float(m))} units of {y} per unit of {x}.',
            'distractors': ndist(float(m), dx / dy, dy, dx, float(m) + 1)}


def ppf_case(r):
    x, y, xs, ys, mocs = ppf_sched(r)
    k = r.randrange(0, len(mocs))
    i = r.randrange(1, len(xs) - 1)
    d = xs[1] - xs[0]
    qs = [f'Calculate the MOC of moving from {LET[k]} to {LET[k + 1]}.', 'Is the MOC rising, constant or falling? What does this tell you about the shape of the PPF?',
          f'Can the economy produce {xs[i]} units of {x} and {ys[i] + d} units of {y}? Why?', 'How would the PPF change if a new technology raises the output of both goods?']
    ans = [f'{ys[k] - ys[k + 1]}/{d} = {num(mocs[k])}', 'Rising; the PPF is concave to the origin',
           f'No: at {xs[i]} units of {x} the maximum is {ys[i]} units of {y}; the point lies outside the PPF', 'It shifts outward (to the right)']
    return {'stem': f'Study the production possibilities of an economy:\n{ppf_tab(x, y, xs, ys)}\n' + parts(qs), 'answer': pans(ans), 'key': '1 mark each (4 marks).'}


PPF_FACT = [
    ('The production possibility frontier shows', 'the combinations of two goods that can be produced with given resources and technology', ['the combinations of two goods a consumer can buy',
     'the prices of two goods', 'the demand for two goods'], 'PPF = maximum output combinations.'),
    ('The PPF is usually concave to the origin because', 'the marginal opportunity cost increases', ['the marginal opportunity cost falls', 'the marginal opportunity cost is constant',
     'resources are unlimited'], 'Rising MOC.'),
    ('The slope of the PPF is called the', 'marginal rate of transformation', ['marginal rate of substitution', 'marginal utility', 'price ratio'], 'MRT = ΔY/ΔX.'),
    ('A straight-line PPF shows that the marginal opportunity cost is', 'constant', ['increasing', 'decreasing', 'zero'], 'Constant slope.'),
    ('Opportunity cost of a choice is', 'the value of the next best alternative given up', ['the money paid for it', 'the sum of all alternatives given up', 'the cost of raw materials'],
     'Next best alternative.'),
    ('A point inside the PPF shows', 'under-utilisation or inefficient use of resources', ['full employment of resources', 'an unattainable combination', 'growth of resources'], 'Inside = unused resources.'),
    ('An outward shift of the PPF shows', 'growth of resources or improvement in technology', ['unemployment of resources', 'a fall in resources', 'a rise in prices'], 'Growth.'),
    ('The PPF is also known as the', 'production possibility curve or transformation curve', ['indifference curve', 'budget line', 'demand curve'], 'Other names.'),
    ('Marginal opportunity cost along a PPF is', 'the units of one good given up to produce one more unit of the other', ['the total output of both goods', 'the price of a good',
     'the units of labour employed'], 'MOC = ΔY/ΔX.'),
]
PPF_AR = [
    ('The PPF is concave to the origin.', 'Marginal opportunity cost rises because resources are not equally efficient in producing both goods.', 'a', 'R explains A.'),
    ('A point outside the PPF can be reached with existing resources.', 'The PPF shows the maximum combinations possible with given resources and technology.', 'd', 'A is false; R is true.'),
    ('Mass unemployment shifts the PPF to the left.', 'Unemployment means resources are not fully used.', 'd', 'A is false: the economy moves to a point inside the PPF; the PPF itself does not shift. R is true.'),
    ('The PPF slopes downward.', 'With full use of resources, more of one good can be produced only by producing less of the other.', 'a', 'R explains A.'),
    ('Points on the PPF show efficient use of resources.', 'At these points, more of one good can be produced without producing less of the other.', 'c', 'A is true; R is false.'),
    ('Opportunity cost is the value of the next best alternative foregone.', 'Resources used for one purpose cannot be used for another at the same time.', 'a', 'R explains why a cost arises.'),
]
PPF_WR = [
    ('Why is the PPF concave to the origin? Explain.', 'Because MOC increases: as more of one good is produced, resources less suited to it must be shifted, so more and more of the other good is given up per extra unit.',
     '1 mark concave/MOC; 2 marks reason.'),
    ('Explain opportunity cost with an example.', 'The value of the next best alternative given up; e.g. a farmer who grows wheat instead of rice gives up the income from rice.', '1 mark meaning; 2 marks example.'),
    ('What does a point inside the PPF show? How can the economy move to the PPF?', 'Under-utilisation/inefficient use of resources (unemployment); by employing idle resources fully and efficiently.',
     '1½ marks each.'),
    ('Distinguish between a shift of the PPF and a movement along it.', 'Shift: change in resources or technology (outward growth, inward destruction). Movement: reallocation of given resources between the two goods.',
     '1½ marks each.'),
]
PPF_LONG = [
    ('Explain the production possibility frontier with the help of a schedule and a diagram. Why is it downward sloping and concave to the origin?',
     'Schedule of combinations and curve; downward slope: more of one good means less of the other; concave: increasing MOC (ΔY/ΔX rises).', '2 marks schedule; 2 marks diagram; 2 marks reasons (6 marks).'),
    ('Explain with diagrams the effect on the PPF of (i) improvement in technology for both goods, (ii) large-scale unemployment, (iii) an earthquake destroying factories.',
     '(i) Outward shift; (ii) the economy operates inside the PPF, no shift; (iii) inward shift.', '2 marks each with diagram (6 marks).'),
]

# ====================================================================== ch09 st3 planned vs market
ECO_EX = [('Central problems are solved through the free play of demand and supply.', 'Market economy'), ('Prices are determined by market forces without government control.', 'Market economy'),
          ('Producers decide what to produce mainly to earn profit, and the government plays almost no role.', 'Market economy'),
          ('Consumers buy whatever they can afford and firms supply what earns the most profit; no authority directs production.', 'Market economy'),
          ('A central authority decides what, how and for whom to produce.', 'Centrally planned economy'), ('Almost all means of production are owned by the state.', 'Centrally planned economy'),
          ('Prices of all goods are fixed by the planning authority.', 'Centrally planned economy'),
          ('The government plans the output of every industry and allots resources to it.', 'Centrally planned economy'),
          ('Public sector and private sector firms operate side by side.', 'Mixed economy'), ('Market forces work, but the government regulates them and runs key industries.', 'Mixed economy'),
          ('The government provides defence, roads and public health, while private firms produce most consumer goods.', 'Mixed economy'),
          ('Private businesses produce most goods, but the state sets minimum wages and supplies subsidised food to the poor.', 'Mixed economy')]
ECO_OPTS = ['Market economy', 'Centrally planned economy', 'Mixed economy', 'Barter economy']


def eco_cls(r):
    x, c = cp('eco', r, ECO_EX)
    return opts_fixed(f'Identify the type of economy: "{x}"', c, ECO_OPTS, f'{c}.', r)


def eco_case(r):
    xs = r.sample(ECO_EX, 4)
    if len({c for _, c in xs}) < 2:
        raise ValueError('one kind')
    return {'stem': 'Read the descriptions of four imaginary economies and identify each as a market, centrally planned or mixed economy:\n' + parts([x for x, _ in xs]),
            'answer': pans([c for _, c in xs]), 'key': '1 mark each (4 marks).'}


ECO_FACT = [
    ('In a market economy, economic activities are coordinated mainly through', 'the price mechanism', ['government orders', 'tradition', 'rationing'], 'Prices signal scarcity.'),
    ('In a centrally planned economy, the central problems are solved by', 'the government or central authority', ['market forces', 'individual consumers', 'foreign firms'], 'Planning authority.'),
    ('An economy in which both the government and the market play important roles is a', 'mixed economy', ['market economy', 'centrally planned economy', 'barter economy'], 'Mixed.'),
    ('In economics, a market means', 'any arrangement in which buyers and sellers interact to exchange goods', ['only a physical place like a mandi', 'a government office', 'a shopping mall only'],
     'Not necessarily a place.'),
    ('In a market economy, the goods produced are mainly those that', 'are demanded by people who can pay for them', ['the government orders', 'are needed only by the poor', 'are cheapest to make'],
     'Profit and demand guide output.'),
    ('Most economies of the world today are', 'mixed economies', ['pure market economies', 'pure centrally planned economies', 'barter economies'], 'Mix of state and market.'),
]
ECO_AR = [
    ('In a market economy, prices guide the allocation of resources.', 'Rising prices signal that a good is scarce, and producers move resources towards it.', 'a', 'R explains A.'),
    ('In a centrally planned economy, consumers decide what is produced.', 'The central authority plans production in such an economy.', 'd', 'A is false; R is true.'),
    ('India is a mixed economy.', 'Both public and private sectors operate in India.', 'a', 'R explains A.'),
    ('A market economy may not meet the needs of the poor.', 'Firms produce for those who can pay a price for the goods.', 'a', 'R explains A.'),
    ('A centrally planned economy relies on the free play of demand and supply.', 'In such an economy, the state owns most means of production.', 'd', 'A is false; R is true.'),
]
ECO_WR = [
    ('How does a market economy solve the central problems?', 'Through the price mechanism: goods with higher prices and profits are produced; cheapest techniques are used; goods go to those who can pay.', '1 mark each problem.'),
    ('How does a centrally planned economy solve the central problems?', 'The central authority decides what goods to produce, which technique to use and how output is distributed, with social welfare in view.', '1 mark each problem.'),
    ('Give three features of a mixed economy.', 'Co-existence of public and private sectors; government regulation of markets; welfare measures such as subsidies and price controls along with the price mechanism.',
     '1 mark each.'),
]
ECO_LONG = [
    ('Distinguish between a centrally planned economy and a market economy on any four points. Why are most economies mixed?',
     'Decision maker (government vs market), ownership (state vs private), motive (welfare vs profit), price (fixed by state vs demand and supply), distribution; mixed economies combine efficiency of markets with welfare by the state.',
     '1 mark each point; 2 marks reason (6 marks).'),
]

# ====================================================================== ch09 st4 positive/normative, micro/macro
PN = [('India\'s population increased between 2001 and 2011.', 'Positive statement'), ('A rise in the price of petrol, other things remaining the same, reduces the quantity demanded.', 'Positive statement'),
      ('The unemployment rate rose last year.', 'Positive statement'), ('Higher interest rates reduce borrowing by firms.', 'Positive statement'),
      ('Wheat production in the country rose this year.', 'Positive statement'), ('A tax on cigarettes raises their price.', 'Positive statement'),
      ('The government spent more on health this year than last year.', 'Positive statement'),
      ('The government should provide free education up to Class 12.', 'Normative statement'), ('Income inequality ought to be reduced.', 'Normative statement'),
      ('The rich should pay higher taxes.', 'Normative statement'), ('Diesel should be made cheaper for farmers.', 'Normative statement'),
      ('Minimum wages ought to be raised.', 'Normative statement'), ('The government should spend more on health than on defence.', 'Normative statement'),
      ('Controlling inflation should be given priority over reducing unemployment.', 'Normative statement')]
MM = [('Price determination of wheat in a market', 'Microeconomics'), ('Demand for cars of one company', 'Microeconomics'), ('Equilibrium of a consumer', 'Microeconomics'),
      ('Cost of production of a firm', 'Microeconomics'), ('Wages of workers in the textile industry', 'Microeconomics'), ('Supply of tomatoes in a local market', 'Microeconomics'),
      ('Output decision of a firm', 'Microeconomics'), ('National income of India', 'Macroeconomics'), ('General price level (inflation) in the economy', 'Macroeconomics'),
      ('Unemployment in the economy as a whole', 'Macroeconomics'), ('Aggregate demand of the economy', 'Macroeconomics'), ('Budget deficit of the government', 'Macroeconomics'),
      ('Total money supply in the economy', 'Macroeconomics'), ('Balance of payments of the country', 'Macroeconomics')]


def pn_case(r):
    xs = r.sample(PN, 4)
    if len({c for _, c in xs}) < 2:
        raise ValueError('one kind')
    return {'stem': 'Classify each statement as positive or normative, giving a reason:\n' + parts([x for x, _ in xs]),
            'answer': pans([f'{c.split()[0]}: {"describes what is; can be tested with facts" if c.startswith("Pos") else "says what ought to be; a value judgement"}' for _, c in xs]),
            'key': '1 mark each (4 marks).'}


def mm_case(r):
    xs = r.sample(MM, 4)
    if len({c for _, c in xs}) < 2:
        raise ValueError('one kind')
    return {'stem': 'State whether each topic is studied in microeconomics or macroeconomics:\n' + parts([x for x, _ in xs]),
            'answer': pans([c for _, c in xs]), 'key': '1 mark each (4 marks).'}


PNF = [
    ('Positive economic analysis deals with', 'what is, or how the economy actually works', ['what ought to be', 'value judgements only', 'opinions about fairness'], 'Positive = what is.'),
    ('Normative economic analysis deals with', 'what ought to be', ['what is', 'only facts that can be tested', 'statistics of the past'], 'Normative = value judgements.'),
    ('Microeconomics studies', 'the behaviour of individual economic agents such as consumers and firms', ['the economy as a whole', 'national income only', 'the general price level'], 'Individual units.'),
    ('Macroeconomics studies', 'aggregates of the economy as a whole', ['an individual consumer', 'a single firm', 'the price of one good'], 'Aggregates.'),
    ('Which of these is a macroeconomic variable?', 'Aggregate output of the economy', ['Price of tomatoes', 'Output of a firm', 'Demand for a brand of soap'], 'Aggregate.'),
    ('A statement that can be checked against facts is a', 'positive statement', ['normative statement', 'value judgement', 'policy advice'], 'Testable.'),
]
PN_AR = [
    ('"The government should give free laptops to students" is a normative statement.', 'It expresses a value judgement about what ought to be done.', 'a', 'R explains A.'),
    ('Study of national income is a part of microeconomics.', 'Macroeconomics studies aggregates of the whole economy.', 'd', 'A is false; R is true.'),
    ('Positive statements can be verified with facts.', 'They describe what is, not what ought to be.', 'a', 'R explains A.'),
    ('Price determination of a single commodity is studied in microeconomics.', 'Microeconomics studies individual markets and economic agents.', 'a', 'R explains A.'),
    ('"Inflation in India was higher last year than this year" is a normative statement.', 'Normative statements involve value judgements.', 'd', 'A is false: it is a positive statement; R is true.'),
]
PN_WR = [
    ('Distinguish between positive and normative economics with one example each.', 'Positive: what is, testable (e.g. "prices rose 5% last year"). Normative: what ought to be, value judgement (e.g. "prices should be controlled").',
     '1 mark each meaning; 1 mark examples.'),
    ('Distinguish between microeconomics and macroeconomics with examples.', 'Micro: individual units, e.g. demand for a good, a firm\'s output. Macro: economy as a whole, e.g. national income, unemployment, inflation.',
     '1 mark each meaning; 1 mark examples.'),
]

# ====================================================================== ch10 st1 utility
GOODS_U = ['ice-cream cones', 'glasses of lemonade', 'samosas', 'chocolates', 'cups of tea', 'slices of pizza', 'bananas', 'plates of pani puri', 'mangoes', 'oranges']


def mu_list(r, n=6, pos=False):
    for _ in range(100):
        mus = [r.randint(14, 40)]
        for _ in range(n - 1):
            mus.append(mus[-1] - r.randint(2, 7))
        if pos and mus[-1] <= 0:
            continue
        return mus
    raise ValueError('mu')


def tu_to_mu(r):
    g = r.choice(GOODS_U)
    n = r.choice([5, 6])
    mus = mu_list(r, n)
    tus = cumsum(mus)
    k = r.randrange(1, n)
    return {'stem': f'Total utility (in utils) from {g}:\n' + table(['Units', *range(1, n + 1)], [['TU', *map(num, tus)]]) + f'\nFind the marginal utility of unit {k + 1}.',
            'answer': num(mus[k]), 'key': f'MU = TU({k + 1}) − TU({k}) = {num(tus[k])} − {num(tus[k - 1])} = {num(mus[k])}.',
            'distractors': ndist(mus[k], round(tus[k] / (k + 1), 2), tus[k], mus[k - 1])}


def mu_to_tu(r):
    g = r.choice(GOODS_U)
    n = r.choice([5, 6])
    mus = mu_list(r, n)
    tus = cumsum(mus)
    k = r.randrange(2, n)
    return {'stem': f'Marginal utility (in utils) from {g}:\n' + table(['Units', *range(1, n + 1)], [['MU', *map(num, mus)]]) + f'\nFind the total utility from {k + 1} units.',
            'answer': num(tus[k]), 'key': f'TU = sum of MUs = {" + ".join(num(m) for m in mus[:k + 1])} = {num(tus[k])}.',
            'distractors': ndist(tus[k], mus[k] * (k + 1), tus[k - 1], mus[k])}


def tu_max(r):
    z = r.randint(4, 6)
    n = z + r.choice([1, 2])
    pos, v = [], 0
    for _ in range(z - 1):
        v += r.randint(2, 7)
        pos.insert(0, v)
    mus = pos + [0]
    v = 0
    for _ in range(n - z):
        v -= r.randint(2, 6)
        mus.append(v)
    tus = cumsum(mus)
    g = r.choice(GOODS_U)
    return {'stem': f'Total utility (in utils) from {g}:\n' + table(['Units', *range(1, n + 1)], [['TU', *map(num, tus)]]) + '\nAt which unit does marginal utility become zero, and what is TU there?',
            'answer': f'Unit {z}; TU = {tus[z - 1]} utils (maximum)', 'key': f'MU of unit {z} = {tus[z - 1]} − {tus[z - 2]} = 0; TU is maximum when MU = 0 and falls after that.',
            'distractors': [f'Unit {z - 1}; TU = {tus[z - 2]} utils (maximum)', f'Unit 1; TU = {tus[0]} utils (maximum)', f'Unit {n}; TU = {tus[-1]} utils (maximum)']}


def eq_single(r):
    g = r.choice(GOODS_U)
    n = 6
    mus = mu_list(r, n, pos=True)
    k = r.choice([1, 2, 4, 5])
    j = r.randrange(1, n - 1)
    p = mus[j] * k
    return {'stem': f'Marginal utility (in utils) from {g}:\n' + table(['Units', *range(1, n + 1)], [['MU', *mus]]) + f'\nIf 1 util = {inr(k)} and the price is {inr(p)} per unit, how many units will the consumer buy?',
            'answer': units(j + 1), 'key': f'MU in ₹ = MU × {k}: {", ".join(str(m * k) for m in mus)}. The consumer buys while MU (₹) ≥ price; at unit {j + 1}, MU = ₹{p} = price. Equilibrium: {j + 1} units.',
            'distractors': [units(j), units(j + 2), units(n) if n != j + 2 else (units(1) if j != 1 else units(j + 3))]}


def eq_two_data(r):
    for _ in range(200):
        px, py = r.sample([2, 3, 4, 5, 6], 2)
        lam = r.choice([1, 2, 3])
        xs_, ys_ = r.randint(2, 5), r.randint(2, 5)
        mx = [0] * 6
        my = [0] * 6
        mx[xs_ - 1] = lam * px
        my[ys_ - 1] = lam * py
        for arr, i0 in ((mx, xs_ - 1), (my, ys_ - 1)):
            for i in range(i0 - 1, -1, -1):
                arr[i] = arr[i + 1] + r.randint(1, 5)
            for i in range(i0 + 1, 6):
                arr[i] = arr[i - 1] - r.randint(1, 3)
        if min(mx + my) < 0:
            continue
        Mi = px * xs_ + py * ys_
        sols = [(a, b) for a in range(1, 7) for b in range(1, 7) if px * a + py * b == Mi and Fraction(mx[a - 1], px) == Fraction(my[b - 1], py)]
        if sols == [(xs_, ys_)]:
            return px, py, Mi, mx, my, xs_, ys_, lam
    raise ValueError('eq2')


def eq_two(r):
    px, py, Mi, mx, my, a, b, lam = eq_two_data(r)
    return {'stem': f'A consumer spends {inr(Mi)} on goods X and Y. Price of X = {inr(px)}, price of Y = {inr(py)}. Marginal utilities (utils) are:\n'
                    + table(['Units', *range(1, 7)], [['MU of X', *mx], ['MU of Y', *my]]) + '\nFind the equilibrium combination using the law of equi-marginal utility.',
            'answer': f'{a} units of X and {b} units of Y',
            'key': f'MUx/Px = {mx[a - 1]}/{px} = {lam} = MUy/Py = {my[b - 1]}/{py}; spending = {px}×{a} + {py}×{b} = {inr(Mi)} = income. 2 marks ratios; 1 mark budget check; 1 mark answer.',
            'distractors': [f'{b} units of X and {a} units of Y', f'{a + 1} units of X and {b} units of Y', f'{a} units of X and {max(1, b - 1)} units of Y']}


def ut_case(r):
    g = r.choice(GOODS_U)
    n = 6
    mus = mu_list(r, n, pos=True)
    tus = cumsum(mus)
    k = r.choice([1, 2, 5])
    j = r.randrange(1, n - 1)
    p = mus[j] * k
    return {'stem': f'{name(r)} records the marginal utility from {g}:\n' + table(['Units', *range(1, n + 1)], [['MU (utils)', *mus]]) + '\n'
            + parts(['Find TU from 3 units.', 'Which law does the MU schedule show?', f'If 1 util = {inr(k)} and price = {inr(p)}, how many units are bought?', 'What would happen to the quantity bought if the price fell? Why?']),
            'answer': pans([f'{tus[2]} utils', 'Law of diminishing marginal utility', f'{j + 1} units (MU in ₹ = price)', 'It would rise: more units now have MU (₹) ≥ price']),
            'key': '1 mark each (4 marks).'}


UT_FACT = [
    ('Utility means', 'the want-satisfying power of a commodity', ['the usefulness of a good to society only', 'the price of a good', 'the cost of producing a good'], 'Want-satisfying power.'),
    ('Marginal utility is the change in total utility from', 'consuming one more unit of a commodity', ['consuming all units', 'a change in price', 'a change in income'], 'MU = ΔTU.'),
    ('When marginal utility is zero, total utility is', 'maximum', ['zero', 'minimum', 'negative'], 'Point of satiety.'),
    ('When marginal utility is negative, total utility', 'falls', ['rises', 'is at its maximum', 'stays constant'], 'Negative addition.'),
    ('The law of diminishing marginal utility says that', 'MU from successive units of a commodity falls as more is consumed', ['TU always falls', 'MU always rises', 'TU and MU are always equal'],
     'Each extra unit adds less.'),
    ('In the cardinal utility approach, utility is measured in', 'utils', ['ranks only', 'kilograms', 'percentages'], 'Cardinal measure.'),
    ('A consumer buying only one good is in equilibrium when', 'the MU of the good in rupees equals its price', ['TU is zero', 'MU is maximum', 'the price is zero'], 'MU (₹) = P.'),
    ('With two goods, the consumer is in equilibrium when', 'MUx/Px = MUy/Py and the whole income is spent', ['MUx = MUy', 'Px = Py', 'TUx = TUy'], 'Equi-marginal principle.'),
    ('Total utility is the', 'sum of the marginal utilities of all units consumed', ['product of MU and price', 'MU of the last unit', 'average of MUs'], 'TU = ΣMU.'),
]
UT_AR = [
    ('TU rises as long as MU is positive.', 'Each extra unit adds to total satisfaction when its MU is positive.', 'a', 'R explains A.'),
    ('MU can become negative.', 'Consuming beyond the point of satiety reduces total utility.', 'a', 'R explains A.'),
    ('TU is maximum when MU is maximum.', 'TU is the sum of the MUs of all units consumed.', 'd', 'A is false: TU is maximum when MU = 0. R is true.'),
    ('If MUx/Px > MUy/Py, the consumer gains by spending more on X.', 'A rupee spent on X gives more utility than a rupee spent on Y.', 'a', 'R explains A.'),
    ('A consumer buys more of a good when its price falls.', 'At a lower price, more units have MU in rupees at least equal to the price.', 'a', 'R explains A.'),
    ('MU of the first unit of a good is always negative.', 'MU diminishes as consumption increases.', 'd', 'A is false; R is true.'),
]
UT_WR = [
    ('State and explain the law of diminishing marginal utility with a schedule.', 'As more units of a good are consumed, MU from each successive unit falls; schedule showing falling MU and TU rising at a falling rate, maximum when MU = 0.',
     '1 mark statement; 2 marks schedule and explanation.'),
    ('Explain the condition of consumer\'s equilibrium in the case of a single commodity. What happens if MU in rupees is greater than the price?', 'MUx (in ₹) = Px. If MU > price, the consumer buys more; MU falls till it equals the price.',
     '1 mark condition; 2 marks explanation.'),
    ('Explain the relationship between TU and MU.', 'TU rises when MU is positive, is maximum when MU is zero and falls when MU is negative; TU is the sum of MUs.', '1 mark each case.'),
]
UT_LONG = [
    ('Explain consumer\'s equilibrium in the case of two commodities using the law of equi-marginal utility. What happens if MUx/Px > MUy/Py?',
     'Equilibrium when MUx/Px = MUy/Py = MU of a rupee and income is fully spent; if MUx/Px > MUy/Py, the consumer buys more X and less Y; MUx falls and MUy rises till ratios are equal.',
     '2 marks conditions; 2 marks explanation; 2 marks adjustment (6 marks).'),
]

# ====================================================================== ch10 st2 budget line
GOODS_B = [('bananas', 'apples'), ('pens', 'notebooks'), ('chocolates', 'biscuits'), ('movie tickets', 'books'), ('sandwiches', 'juice packs'), ('samosas', 'bus rides'),
           ('mangoes', 'oranges'), ('notebooks', 'pencils')]


def bl_params(r):
    p1, p2 = r.choice([2, 4, 5, 8, 10, 20]), r.choice([2, 4, 5, 10, 20, 25])
    L = p1 * p2 // math.gcd(p1, p2)
    Mi = L * r.randint(2, 8)
    if Mi > 2000 or Mi // min(p1, p2) > 200:
        raise ValueError('big')
    return p1, p2, Mi


def bl_basic(r):
    g1, g2 = r.choice(GOODS_B)
    p1, p2, Mi = bl_params(r)
    v = r.choice(['eq', 'i1', 'i2', 'slope'])
    base = f'A consumer has an income of {inr(Mi)} to spend on {g1} (good 1, price {inr(p1)}) and {g2} (good 2, price {inr(p2)}).'
    if v == 'eq':
        ans = f'{p1}x₁ + {p2}x₂ = {Mi}'
        return {'stem': base + ' Write the equation of the budget line.', 'answer': ans, 'key': 'Budget line: p₁x₁ + p₂x₂ = M.',
                'distractors': alts(ans, [f'{p2}x₁ + {p1}x₂ = {Mi}', f'x₁/{p1} + x₂/{p2} = {Mi}', f'{p1}x₁ − {p2}x₂ = {Mi}'], [f'{p1}x₁ + {p2}x₂ = {Mi * 2}'])}
    if v in ('i1', 'i2'):
        p, g, po = (p1, g1, p2) if v == 'i1' else (p2, g2, p1)
        ans = Mi // p
        return {'stem': base + f' What is the maximum quantity of {g} the consumer can buy?', 'answer': num(ans), 'key': f'Intercept = M/p = {Mi}/{p} = {ans} (spending all income on {g}).',
                'distractors': ndist(ans, Mi // po, round(Mi / (p1 + p2), 2), Mi * p)}
    ans = frac(-p1, p2)
    return {'stem': base + ' What is the slope of the budget line (good 1 on the horizontal axis)?', 'answer': ans, 'key': f'Slope = −p₁/p₂ = −{p1}/{p2} = {ans}.',
            'distractors': alts(ans, [frac(-p2, p1), frac(p1, p2), frac(-p1 * p2, 1)], [frac(-Mi, p2), frac(-1, 2), frac(-3, 1)])}


def bl_afford(r):
    g1, g2 = r.choice(GOODS_B)
    p1, p2, Mi = bl_params(r)
    x1 = r.randint(0, Mi // p1)
    rest = Mi - p1 * x1
    kind = r.choice(['on', 'in', 'out'])
    if kind == 'on':
        if rest % p2:
            raise ValueError('x')
        x2 = rest // p2
    elif kind == 'in':
        if rest < p2:
            raise ValueError('x')
        x2 = r.randint(0, rest // p2 - 1) if rest // p2 >= 1 else 0
    else:
        x2 = rest // p2 + r.randint(1, 4)
    cost = p1 * x1 + p2 * x2
    diff = Mi - cost
    if (kind == 'on') != (diff == 0) or (kind == 'in' and diff <= 0):
        raise ValueError('x')
    on = f'On the budget line: it costs exactly {inr(Mi)}'
    ins = lambda d: f'Inside the budget set: {inr(d)} is left unspent'
    out = lambda d: f'Not affordable: {inr(d)} more is needed'
    if kind == 'on':
        ans, wrong = on, [ins(p1), out(p2), ins(p2 if p2 != p1 else p1 + p2)]
    elif kind == 'in':
        ans, wrong = ins(diff), [on, out(diff), ins(diff + p1)]
    else:
        ans, wrong = out(-diff), [on, ins(-diff), out(-diff + p2)]
    return mcq(f'Income = {inr(Mi)}; price of {g1} = {inr(p1)}, price of {g2} = {inr(p2)}. Where does the bundle ({x1} {g1}, {x2} {g2}) lie?', ans, wrong,
               f'Cost = {p1}×{x1} + {p2}×{x2} = {inr(cost)} against income {inr(Mi)}.', r)


def bl_count(r):
    p1, p2 = r.choice([1, 2, 3, 4, 5]), r.choice([2, 3, 4, 5])
    Mi = r.randint(6, 16)
    on = r.random() < 0.5
    pts = [(a, b) for a in range(0, Mi + 1) for b in range(0, Mi + 1) if (p1 * a + p2 * b == Mi if on else p1 * a + p2 * b <= Mi)]
    n = len(pts)
    if (on and n < 2) or n > 30:
        raise ValueError('few')
    what = 'lie on the budget line' if on else 'are in the budget set (affordable)'
    return {'stem': f'A consumer has {inr(Mi)}. Good 1 costs {inr(p1)} and good 2 costs {inr(p2)}; both are available only in whole units. How many bundles {what}?',
            'answer': str(n), 'key': f'Count (x₁, x₂) with {p1}x₁ + {p2}x₂ {"=" if on else "≤"} {Mi}: ' + ', '.join(f'({a},{b})' for a, b in pts[:12]) + (' …' if n > 12 else '') + f' → {n} bundles.',
            'distractors': ndist(n, n + 1, n - 1, Mi // p1 + Mi // p2)}


def bl_from_int(r):
    g1, g2 = r.choice(GOODS_B)
    p1, p2, Mi = bl_params(r)
    a, b = Mi // p1, Mi // p2
    if r.random() < 0.5:
        return {'stem': f'A budget line meets the {g1} axis at {a} units and the {g2} axis at {b} units. If the price of {g1} is {inr(p1)}, find the income and the price of {g2}.',
                'answer': f'Income = {inr(Mi)}; price of {g2} = {inr(p2)}', 'key': f'M = p₁ × {a} = {inr(Mi)}; p₂ = M/{b} = {inr(p2)}.',
                'distractors': alts(f'Income = {inr(Mi)}; price of {g2} = {inr(p2)}', [f'Income = {inr(Mi)}; price of {g2} = {inr(p1)}', f'Income = {inr(a * b)}; price of {g2} = {inr(p2)}',
                                    f'Income = {inr(Mi * 2)}; price of {g2} = {inr(p2 * 2)}'], [f'Income = {inr(a + b)}; price of {g2} = {inr(p2 + 1)}', f'Income = {inr(Mi + p1)}; price of {g2} = {inr(p2)}'])}
    return {'stem': f'A budget line has slope {frac(-p1, p2)} and meets the {g2} axis at {b} units. If the price of {g2} is {inr(p2)}, find the price of {g1} and the consumer\'s income.',
            'answer': f'Price of {g1} = {inr(p1)}; income = {inr(Mi)}', 'key': f'M = {p2} × {b} = {inr(Mi)}; p₁/p₂ = {frac(p1, p2)} ⇒ p₁ = {inr(p1)}.',
            'distractors': [f'Price of {g1} = {inr(p2)}; income = {inr(Mi)}', f'Price of {g1} = {inr(p1)}; income = {inr(Mi // 2 if Mi % 2 == 0 else Mi + 10)}',
                            f'Price of {g1} = {inr(p1 * 2)}; income = {inr(Mi * 2)}']}


def bl_new(r):
    g1, g2 = r.choice(GOODS_B)
    p1, p2, Mi = bl_params(r)
    v = r.choice(['inc', 'p1'])
    if v == 'inc':
        M2 = Mi + p1 * p2 * r.choice([1, 2, 3])
        a2, b2 = M2 // p1, M2 // p2
        if M2 % p1 or M2 % p2:
            raise ValueError('x')
        ans = f'{a2} units of {g1} and {b2} units of {g2}; the line shifts parallel outward'
        return {'stem': f'Income rises from {inr(Mi)} to {inr(M2)}; prices of {g1} and {g2} stay at {inr(p1)} and {inr(p2)}. Find the new intercepts and describe the change in the budget line.',
                'answer': ans, 'key': f'New intercepts {M2}/{p1} = {a2} and {M2}/{p2} = {b2}; slope −p₁/p₂ unchanged, so a parallel shift.',
                'distractors': [f'{a2} units of {g1} and {b2} units of {g2}; the line rotates outward', f'{Mi // p1} units of {g1} and {b2} units of {g2}; the line rotates outward',
                                f'{b2} units of {g1} and {a2} units of {g2}; the line shifts parallel outward' if a2 != b2 else f'{a2 + 1} units of {g1} and {b2 + 1} units of {g2}; the line shifts parallel outward']}
    q = [d for d in range(max(1, p1 // 2), p1) if Mi % d == 0]
    if not q:
        raise ValueError('x')
    np1 = r.choice(q)
    return {'stem': f'Income is {inr(Mi)}; price of {g2} is {inr(p2)}. The price of {g1} falls from {inr(p1)} to {inr(np1)}. Find the new {g1} intercept and describe the change in the budget line.',
            'answer': f'{Mi // np1} units; the line rotates outward along the {g1} axis ({g2} intercept unchanged at {Mi // p2})',
            'key': f'New intercept = {Mi}/{np1} = {Mi // np1}; the {g2} intercept M/p₂ is unchanged, so the line pivots outward.',
            'distractors': [f'{Mi // np1} units; the line shifts parallel outward', f'{Mi // p1} units; the line rotates inward along the {g1} axis',
                            f'{Mi // np1} units; the line rotates outward along the {g2} axis ({g1} intercept unchanged)']}


BL_EV = [('Income of the consumer rises; prices are unchanged', 'Parallel outward shift'), ('Income of the consumer falls; prices are unchanged', 'Parallel inward shift'),
         ('Price of good 1 falls; income and price of good 2 are unchanged', 'Rotates outward; good 1 intercept moves out'),
         ('Price of good 1 rises; income and price of good 2 are unchanged', 'Rotates inward; good 1 intercept moves in'),
         ('Price of good 2 falls; income and price of good 1 are unchanged', 'Rotates outward; good 2 intercept moves out'),
         ('Price of good 2 rises; income and price of good 1 are unchanged', 'Rotates inward; good 2 intercept moves in'),
         ('Income and both prices double', 'No change in the budget line'), ('Both prices fall to half; income is unchanged', 'Parallel outward shift'),
         ('Both prices double; income is unchanged', 'Parallel inward shift'), ('Income and both prices rise by 10%', 'No change in the budget line')]


def bl_case(r):
    g1, g2 = r.choice(GOODS_B)
    p1, p2, Mi = bl_params(r)
    return {'stem': f'{name(r)} has a pocket allowance of {inr(Mi)} to spend on {g1} (price {inr(p1)}) and {g2} (price {inr(p2)}).\n'
            + parts(['Write the equation of the budget line.', f'Find the maximum quantity of {g1} that can be bought.', 'Find the slope of the budget line.',
                     'What happens to the budget line if the allowance doubles and prices remain the same?']),
            'answer': pans([f'{p1}x₁ + {p2}x₂ = {Mi}', f'{Mi // p1} units', f'−p₁/p₂ = {frac(-p1, p2)}', f'Parallel outward shift (intercepts {2 * Mi // p1} and {2 * Mi // p2})']),
            'key': '1 mark each (4 marks).'}


BL_FACT = [
    ('The budget set is the set of all bundles', 'that a consumer can buy with the given income and prices', ['that give equal satisfaction', 'that a firm can produce', 'on the indifference curve'],
     'p₁x₁ + p₂x₂ ≤ M.'),
    ('The budget line shows bundles that', 'cost exactly the consumer\'s income', ['cost less than the income', 'give maximum utility', 'cost more than the income'], 'p₁x₁ + p₂x₂ = M.'),
    ('The slope of the budget line equals', '−p₁/p₂', ['−p₂/p₁', 'MRS', 'M/p₁'], 'Price ratio.'),
    ('If income rises with prices unchanged, the budget line', 'shifts parallel outward', ['rotates inward', 'becomes steeper', 'does not change'], 'Same slope.'),
    ('If the price of good 1 (on the x-axis) falls, the budget line', 'becomes flatter, rotating outward along the x-axis', ['shifts parallel outward', 'becomes steeper', 'does not change'],
     'Slope −p₁/p₂ falls in size.'),
    ('The budget line is a straight line because', 'the prices of goods are given and constant', ['utility diminishes', 'income keeps changing', 'the MRS diminishes'], 'Constant price ratio.'),
    ('The horizontal intercept of the budget line (good 1 on x-axis) is', 'M/p₁', ['M/p₂', 'p₁/p₂', 'M × p₁'], 'All income on good 1.'),
]
BL_AR = [
    ('The budget line is downward sloping.', 'To buy more of one good with a given income, the consumer must buy less of the other.', 'a', 'R explains A.'),
    ('A rise in income makes the budget line steeper.', 'The slope of the budget line depends only on the price ratio.', 'd', 'A is false: it shifts parallel. R is true.'),
    ('If income and both prices double, the budget line does not change.', 'Intercepts M/p₁ and M/p₂ and the slope remain the same.', 'a', 'R explains A.'),
    ('Bundles inside the budget line are not affordable.', 'Bundles inside the budget line cost less than the income.', 'd', 'A is false: they are affordable. R is true.'),
    ('The slope of the budget line is −p₁/p₂.', 'It shows the rate at which the market allows good 2 to be exchanged for good 1.', 'a', 'R explains A.'),
]
BL_WR = [
    ('Distinguish between the budget set and the budget line.', 'Budget set: all bundles with p₁x₁ + p₂x₂ ≤ M (affordable). Budget line: bundles costing exactly M (p₁x₁ + p₂x₂ = M).', '1½ marks each.'),
    ('Why is the budget line downward sloping? What does its slope show?', 'Given income, more of one good means less of the other; slope −p₁/p₂ shows the rate at which good 2 can be exchanged for good 1 in the market.',
     '1½ marks each.'),
    ('Explain with a diagram the effect on the budget line of a fall in the price of good 1.', 'The line rotates outward along the good 1 axis (intercept M/p₁ rises), good 2 intercept unchanged; it becomes flatter.',
     '1 mark diagram; 2 marks explanation.'),
]
BL_LONG = [
    ('Explain the budget line. Derive its slope. Show with diagrams how it changes when (i) income rises, (ii) price of good 2 rises.',
     'Bundles costing exactly M; p₁x₁ + p₂x₂ = M; slope −p₁/p₂ (from intercepts M/p₁, M/p₂); (i) parallel outward shift; (ii) rotates inward along the good 2 axis, good 1 intercept unchanged.',
     '2 marks meaning and slope; 2 marks each change (6 marks).'),
]

# ====================================================================== ch10 st3 indifference curves
GOODS_I = [('bananas', 'mangoes'), ('pens', 'pencils'), ('chocolates', 'ice-creams'), ('apples', 'oranges'), ('books', 'music downloads'), ('cups of tea', 'biscuit packets')]


def mrs_tab(r):
    g1, g2 = r.choice(GOODS_I)
    s = r.choice([1, 1, 2])
    drops = sorted(r.sample(range(1, 9), 4), reverse=True)
    drops = [d * s for d in drops]
    y0 = sum(drops) + r.randint(2, 8)
    x0 = r.randint(1, 3)
    xs = [x0 + i * s for i in range(5)]
    ys = [y0]
    for d in drops:
        ys.append(ys[-1] - d)
    k = r.randrange(4)
    m = Fraction(drops[k], s)
    return {'stem': f'A consumer is indifferent between these bundles of {g1} (good 1) and {g2} (good 2):\n' + table(['Bundle', *LET[:5]], [[g1.capitalize(), *xs], [g2.capitalize(), *ys]])
            + f'\nFind the MRS (units of {g2} per unit of {g1}) when the consumer moves from {LET[k]} to {LET[k + 1]}.',
            'answer': num(float(m)), 'key': f'MRS = ΔY/ΔX = {drops[k]}/{s} = {num(float(m))}. MRS falls along the curve: {", ".join(num(d / s) for d in drops)}.',
            'distractors': ndist(float(m), drops[k - 1] / s if k else drops[1] / s, ys[k + 1], float(m) + 2)}


OPT_OPTS = ['Buy more of good 1 and less of good 2', 'Buy less of good 1 and more of good 2', 'Stay at the same bundle: it is the optimum', 'Buy more of both goods']


def opt_dir(r):
    p1, p2 = r.sample([2, 3, 4, 5, 6, 8, 10], 2)
    ratio = Fraction(p1, p2)
    kind = r.choice(['gt', 'lt', 'eq'])
    if kind == 'eq':
        m = ratio
    elif kind == 'gt':
        m = ratio + r.choice([Fraction(1, 2), 1, 2])
    else:
        m = ratio - r.choice([Fraction(1, 4), Fraction(1, 2)])
        if m <= 0:
            raise ValueError('neg')
    ans = {'gt': OPT_OPTS[0], 'lt': OPT_OPTS[1], 'eq': OPT_OPTS[2]}[kind]
    rel = {'gt': '>', 'lt': '<', 'eq': '='}[kind]
    return opts_fixed(f'At a bundle on her budget line, a consumer\'s MRS (units of good 2 she is willing to give up for one more unit of good 1) is {num(float(m))}. '
                      f'The prices are p₁ = {inr(p1)} and p₂ = {inr(p2)}. What should she do to raise her satisfaction?', ans, OPT_OPTS,
                      f'MRS = {num(float(m))} {rel} p₁/p₂ = {num(float(ratio))}. ' + {'gt': 'She values good 1 more than the market does, so she substitutes good 1 for good 2.',
                                                                                    'lt': 'She values good 1 less than the market does, so she buys less of good 1.', 'eq': 'MRS = price ratio: optimum.'}[kind], r)


MONO_OPTS = ['Bundle P is preferred', 'Bundle Q is preferred', 'The consumer is indifferent between them', 'Cannot be decided from monotonic preferences alone']


def mono(r):
    a, b = r.randint(2, 10), r.randint(2, 10)
    kind = r.choice(['p', 'q', 'n'])
    if kind == 'n':
        c, d = a + r.randint(1, 4), b - r.randint(1, b - 1)
        P, Q = ((a, b), (c, d)) if r.random() < 0.5 else ((c, d), (a, b))
        ans = MONO_OPTS[3]
        why = 'Neither bundle has at least as much of both goods with more of one.'
    else:
        c, d = (a + r.randint(0, 3), b + r.randint(1, 3)) if r.random() < 0.5 else (a + r.randint(1, 3), b)
        P, Q = ((c, d), (a, b)) if kind == 'p' else ((a, b), (c, d))
        ans = MONO_OPTS[0] if kind == 'p' else MONO_OPTS[1]
        why = 'It has more of at least one good and no less of the other.'
    return opts_fixed(f'A consumer has monotonic preferences. Compare bundle P = ({P[0]}, {P[1]}) with bundle Q = ({Q[0]}, {Q[1]}) (units of good 1, good 2).', ans, MONO_OPTS, why, r)


def ic_case(r):
    g1, g2 = r.choice(GOODS_I)
    drops = sorted(r.sample(range(1, 9), 4), reverse=True)
    y0 = sum(drops) + r.randint(2, 8)
    xs = [i + 1 for i in range(5)]
    ys = [y0]
    for d in drops:
        ys.append(ys[-1] - d)
    k = r.randrange(4)
    return {'stem': f'Bundles of {g1} (good 1) and {g2} (good 2) giving equal satisfaction:\n' + table(['Bundle', *LET[:5]], [[g1.capitalize(), *xs], [g2.capitalize(), *ys]]) + '\n'
            + parts([f'Find the MRS between {LET[k]} and {LET[k + 1]}.', 'Is the MRS diminishing? What shape does this give the indifference curve?',
                     'Why is the indifference curve downward sloping?', 'State the condition for the consumer\'s optimum.']),
            'answer': pans([f'{drops[k]}', f'Yes ({", ".join(map(str, drops))}); convex to the origin', 'With monotonic preferences, more of good 1 must be balanced by less of good 2 to keep satisfaction the same',
                            'MRS = p₁/p₂ at a point on the budget line (tangency), with MRS diminishing']),
            'key': '1 mark each (4 marks).'}


IC_FACT = [
    ('An indifference curve shows bundles that give the consumer', 'the same level of satisfaction', ['the same total cost', 'increasing satisfaction', 'maximum profit'], 'Equal utility.'),
    ('The slope of an indifference curve (in absolute value) is the', 'marginal rate of substitution', ['price ratio', 'marginal utility', 'marginal rate of transformation'], 'MRS.'),
    ('An indifference curve is convex to the origin because', 'the MRS diminishes', ['the MRS increases', 'prices are constant', 'income is fixed'], 'Diminishing MRS.'),
    ('Under monotonic preferences, a higher indifference curve shows', 'a higher level of satisfaction', ['a lower level of satisfaction', 'the same satisfaction', 'a higher price'], 'More is better.'),
    ('Two indifference curves can never', 'intersect each other', ['be drawn on one diagram', 'slope downward', 'be convex'], 'Intersection contradicts monotonicity.'),
    ('A family of indifference curves is called an', 'indifference map', ['budget set', 'isoquant map', 'demand schedule'], 'Indifference map.'),
    ('Preferences are monotonic when a consumer', 'prefers a bundle with more of at least one good and no less of the other', ['prefers fewer goods', 'is indifferent to quantities', 'buys only one good'],
     'More is preferred.'),
    ('At the consumer\'s optimum (with a convex IC), the budget line is', 'tangent to the highest attainable indifference curve', ['parallel to the x-axis', 'cutting the IC twice', 'vertical'],
     'Tangency: MRS = p₁/p₂.'),
]
IC_AR = [
    ('An indifference curve slopes downward.', 'With monotonic preferences, more of one good must be offset by less of the other to keep satisfaction unchanged.', 'a', 'R explains A.'),
    ('Two indifference curves can intersect.', 'Each indifference curve shows a different level of satisfaction.', 'd', 'A is false; R is true.'),
    ('An indifference curve is convex to the origin.', 'The MRS diminishes as the consumer gets more of good 1.', 'a', 'R explains A.'),
    ('At the optimum, MRS equals the price ratio.', 'If MRS > p₁/p₂, the consumer can gain by buying more of good 1.', 'a', 'R shows why any other point is not optimal.'),
    ('A higher indifference curve gives lower satisfaction.', 'Bundles on a higher IC contain more of at least one good.', 'd', 'A is false; R is true.'),
]
IC_WR = [
    ('State any three properties of indifference curves.', 'Slope downward; convex to the origin (diminishing MRS); higher IC = higher satisfaction; two ICs never intersect.', '1 mark each.'),
    ('Why can two indifference curves not intersect? Explain.', 'At the intersection, the common bundle would give two different levels of satisfaction; with monotonic preferences one curve has more of a good at another point, which contradicts both being equal to the common bundle.',
     '3 marks.'),
    ('Explain the meaning of marginal rate of substitution with an example. Why does it diminish?', 'Units of good 2 the consumer is willing to give up for one more unit of good 1; e.g. 4 mangoes for 1 banana; it diminishes because as good 1 becomes more plentiful its relative worth falls.',
     '1 mark meaning; 1 mark example; 1 mark reason.'),
]
IC_LONG = [
    ('Explain the conditions of consumer\'s equilibrium using indifference curve analysis. What happens if MRS > p₁/p₂?',
     'Budget line tangent to the highest IC: MRS = p₁/p₂ and MRS diminishing (IC convex). If MRS > p₁/p₂, the consumer values good 1 more than the market, buys more of it and less of good 2; MRS falls till equal.',
     '2 marks each condition; 2 marks adjustment (6 marks).'),
]

# ====================================================================== ch10 st4 demand
NORMAL = ['branded shirts', 'cars', 'air travel', 'fruits', 'restaurant meals', 'smartphones']
INFERIOR = ['coarse cereals', 'coarse cloth']
SUBS = [('tea', 'coffee'), ('train travel', 'bus travel'), ('gel pens', 'ball pens'), ('butter', 'margarine'), ('cotton shirts', 'polyester shirts')]
COMPS = [('cars', 'petrol'), ('printers', 'ink cartridges'), ('tea', 'sugar'), ('bread', 'butter'), ('mobile phones', 'mobile data'), ('cricket bats', 'cricket balls')]
DEF = ['Movement down along the demand curve (quantity demanded rises)', 'Movement up along the demand curve (quantity demanded falls)',
       'Demand curve shifts to the right (increase in demand)', 'Demand curve shifts to the left (decrease in demand)']
DEM_EV = []
for _g in NORMAL + [s[0] for s in SUBS[:3]]:
    DEM_EV += [(_g, f'the price of {_g} falls', 0), (_g, f'the price of {_g} rises', 1)]
for _g in NORMAL:
    DEM_EV += [(_g, 'consumers\' incomes rise', 2), (_g, 'consumers\' incomes fall', 3)]
for _g in INFERIOR:
    DEM_EV += [(_g, 'consumers\' incomes rise (it is an inferior good)', 3), (_g, 'consumers\' incomes fall (it is an inferior good)', 2)]
for _g, _s in SUBS:
    DEM_EV += [(_g, f'the price of {_s} rises', 2), (_g, f'the price of {_s} falls', 3)]
for _g, _c in COMPS:
    DEM_EV += [(_g, f'the price of {_c} rises', 3), (_g, f'the price of {_c} falls', 2)]
for _g in NORMAL[:4]:
    DEM_EV += [(_g, f'an advertisement campaign makes {_g} more fashionable', 2), (_g, f'consumers\' taste turns away from {_g}', 3)]


def dem_event(r):
    g, e, i = cp('demev', r, DEM_EV)
    return opts_fixed(f'Other things remaining the same, what happens in the market for {g} when {e}?', DEF[i], DEF, f'{DEF[i]}.', r)


def elas_pct(r):
    for _ in range(300):
        P1 = r.choice([10, 20, 25, 40, 50, 80, 100])
        a = r.choice([10, 20, 25, 50])
        up = r.random() < 0.5
        e = r.choice([Fraction(2, 5), Fraction(1, 2), Fraction(3, 5), Fraction(4, 5), 1, Fraction(6, 5), Fraction(3, 2), 2, Fraction(5, 2)])
        b = e * a
        Q1 = r.choice([100, 200, 250, 400, 500, 800, 1000])
        dP = Fraction(P1 * a, 100)
        dQ = Fraction(Q1, 1) * b / 100
        if dP.denominator != 1 or dQ.denominator != 1 or (up and dQ >= Q1):
            continue
        P2 = P1 + int(dP) if up else P1 - int(dP)
        Q2 = Q1 - int(dQ) if up else Q1 + int(dQ)
        g = r.choice(NORMAL + ['sugar', 'salt', 'cooking gas', 'movie tickets'])
        ef = float(e)
        ans = f'{num(ef)} ({cls_e(e)})'
        wrong = [f'{num(1 / ef)} ({cls_e(1 / e)})', f'{num(abs(Q2 - Q1) / Q2 / (abs(P2 - P1) / P2))} ({cls_e(Fraction(abs(Q2 - Q1), Q2) / Fraction(abs(P2 - P1), P2))})',
                 f'{num(ef)} ({"inelastic" if cls_e(e) != "inelastic" else "elastic"})', f'{num(ef + 0.5)} ({cls_e(e + Fraction(1, 2))})']
        return {'stem': f'When the price of {g} {"rises" if up else "falls"} from {inr(P1)} to {inr(P2)}, its quantity demanded {"falls" if up else "rises"} from {Q1} to {Q2} units. '
                        'Calculate the price elasticity of demand (absolute value) by the percentage method and state whether demand is elastic or inelastic.',
                'answer': ans, 'key': f'%ΔQ = {int(dQ)}/{Q1} × 100 = {num(float(b))}%; %ΔP = {int(dP)}/{P1} × 100 = {a}%; |eD| = {num(float(b))}/{a} = {num(ef)} → {cls_e(e)}.',
                'distractors': alts(ans, wrong)}
    raise ValueError('el')


def elas_findq(r):
    for _ in range(300):
        P1 = r.choice([10, 20, 25, 40, 50, 100])
        a = r.choice([10, 20, 25, 50])
        e = r.choice([Fraction(1, 2), Fraction(4, 5), 1, Fraction(3, 2), 2, 3])
        Q1 = r.choice([100, 200, 300, 400, 500, 600, 1000])
        up = r.random() < 0.5
        dP = Fraction(P1 * a, 100)
        dQ = Q1 * e * a / 100
        if dP.denominator != 1 or Fraction(dQ).denominator != 1 or (up and dQ >= Q1):
            continue
        P2 = P1 + int(dP) if up else P1 - int(dP)
        Q2 = Q1 - int(dQ) if up else Q1 + int(dQ)
        g = r.choice(NORMAL + ['sugar', 'cooking oil', 'notebooks'])
        return {'stem': f'The price elasticity of demand for {g} is (−){num(float(e))}. At a price of {inr(P1)}, {Q1} units are demanded. How many units will be demanded if the price {"rises" if up else "falls"} to {inr(P2)}?',
                'answer': f'{Q2} units', 'key': f'%ΔP = {a}%; %ΔQ = {num(float(e))} × {a} = {num(float(e * a))}%; ΔQ = {num(float(e * a))}% of {Q1} = {int(dQ)}; new Q = {Q2}.',
                'distractors': alts(f'{Q2} units', [f'{Q1 + int(dQ) if up else Q1 - int(dQ)} units', f'{Q1 - a if up else Q1 + a} units', f'{Q2 + 10} units'], [f'{Q2 - 20} units'])}
    raise ValueError('el')


def elas_lin(r):
    for _ in range(200):
        b = r.choice([2, 3, 4, 5, 10])
        a = r.choice([100, 120, 150, 200, 240, 300, 400, 500])
        if a % b:
            continue
        pmax = a // b
        p = r.randint(2, pmax - 2)
        q = a - b * p
        e = Fraction(b * p, q)
        if e.denominator > 20:
            continue
        g = r.choice(['notebooks', 'apples', 'pens', 'kites', 'candles'])
        if r.random() < 0.3:
            pu = Fraction(a, 2 * b)
            if pu.denominator != 1:
                continue
            return {'stem': f'The demand function for {g} is q = {a} − {b}p. At what price is the demand unitary elastic?', 'answer': inr(int(pu)),
                    'key': f'|e| = bp/q = 1 ⇒ {b}p = {a} − {b}p ⇒ p = {a}/{2 * b} = {int(pu)} (mid-point of the demand line).',
                    'distractors': alts(inr(int(pu)), [inr(pmax), inr(a // 4 if a % 4 == 0 else int(pu) + 5), inr(int(pu) * 2 - 1)], [inr(int(pu) + 3)])}
        return {'stem': f'The demand function for {g} is q = {a} − {b}p. Find the price elasticity of demand (absolute value) at p = {inr(p)}.',
                'answer': d2(e), 'key': f'q = {a} − {b}×{p} = {q}; |e| = b × p/q = {b} × {p}/{q} = {d2(e)}.',
                'distractors': ndist(round(float(e), 2), round(q / (b * p), 2), round(p / q, 2), b)}
    raise ValueError('lin')


def elas_geo(r):
    P0 = r.choice([20, 30, 40, 50, 60, 80, 100])
    p = r.randint(2, P0 - 2)
    e = Fraction(p, P0 - p)
    ans = d2(e)
    return {'stem': f'A straight-line demand curve meets the price axis at {inr(P0)}. Using the geometric method, find the price elasticity of demand (absolute value) at a price of {inr(p)}.',
            'answer': ans, 'key': f'|e| = lower segment/upper segment = p/(P₀ − p) = {p}/({P0} − {p}) = {ans}. ' + ('Above the mid-point demand is elastic.' if e > 1 else ('At the mid-point |e| = 1.' if e == 1 else 'Below the mid-point demand is inelastic.')),
            'distractors': ndist(round(float(e), 2), round((P0 - p) / p, 2), round(p / P0, 2), 1 if e != 1 else 2)}


TE_OPTS = ['Elastic (|eD| > 1)', 'Unitary elastic (|eD| = 1)', 'Inelastic (|eD| < 1)', 'Perfectly elastic (|eD| = ∞)']


def te_method(r):
    for _ in range(100):
        P1 = r.choice([10, 12, 15, 20, 25, 30, 40])
        P2 = P1 + r.choice([-5, -4, -2, 2, 4, 5, 10])
        if P2 <= 0:
            continue
        Q1 = r.choice([100, 120, 150, 200, 240, 300])
        kind = r.choice(['e', 'u', 'i'])
        if kind == 'u':
            if (P1 * Q1) % P2:
                continue
            Q2 = P1 * Q1 // P2
        elif kind == 'e':
            Q2 = P1 * Q1 // P2 + (r.randint(5, 30) if P2 < P1 else -r.randint(5, 30))
        else:
            Q2 = Q1 + (r.randint(2, 10) if P2 < P1 else -r.randint(2, 10))
            if (P2 * Q2 - P1 * Q1) * (P2 - P1) <= 0:
                continue
        if Q2 <= 0 or Q2 == Q1 or (Q2 - Q1) * (P2 - P1) >= 0:
            continue
        E1, E2 = P1 * Q1, P2 * Q2
        k = 0 if (E2 - E1) * (P2 - P1) < 0 else (1 if E2 == E1 else 2)
        if 'eui'[k] != kind:
            continue
        g = r.choice(['cotton shirts', 'apples', 'cooking gas', 'bus tickets', 'notebooks', 'tea'])
        return opts_fixed(f'When the price of {g} changes from {inr(P1)} to {inr(P2)}, quantity demanded changes from {Q1} to {Q2} units. Using the total expenditure method, the demand is',
                          TE_OPTS[k], TE_OPTS, f'Expenditure: {inr(E1)} → {inr(E2)}; ' + ['it moves opposite to price → elastic.', 'unchanged → unitary elastic.', 'it moves with price → inelastic.'][k], r)
    raise ValueError('te')


def dem_case(r):
    for _ in range(100):
        b = r.choice([2, 4, 5, 10])
        a = r.choice([200, 240, 300, 400, 500])
        p1 = r.choice([5, 10, 15, 20])
        p2 = p1 + r.choice([5, 10])
        q1, q2 = a - b * p1, a - b * p2
        if q2 <= 0:
            continue
        e = Fraction(q1 - q2, q1) / Fraction(p2 - p1, p1)
        g = r.choice(['notebooks', 'kites', 'apples', 'candles', 'pens'])
        return {'stem': f'In a market, the demand for {g} is q = {a} − {b}p.\n'
                + parts([f'Find the quantity demanded at {inr(p1)} and {inr(p2)}.', f'Calculate the price elasticity of demand (absolute value) when price rises from {inr(p1)} to {inr(p2)}, by the percentage method.',
                         'Is demand elastic, inelastic or unitary elastic over this range?', f'Find the total expenditure on {g} at both prices.']),
                'answer': pans([f'{q1} and {q2} units', f'({q1 - q2}/{q1})/({p2 - p1}/{p1}) = {d2(e)}', cls_e(e).capitalize(),
                                f'{inr(p1 * q1)} at {inr(p1)}; {inr(p2 * q2)} at {inr(p2)}']),
                'key': '1 mark each (4 marks).'}
    raise ValueError('dc')


DEM_FACT = [
    ('The law of demand states that, other things remaining the same,', 'quantity demanded falls when the price rises', ['demand rises when price rises', 'supply falls when price rises', 'price falls when demand rises'],
     'Inverse relation.'),
    ('A change in the price of the good itself causes', 'a movement along the demand curve', ['a shift of the demand curve', 'no change in quantity', 'a shift of the supply curve'], 'Own price → movement.'),
    ('A rise in the price of a substitute good causes the demand curve of the good to', 'shift to the right', ['shift to the left', 'stay unchanged', 'become vertical'], 'Substitutes.'),
    ('A good whose demand rises with its price, against the law of demand, is a', 'Giffen good', ['normal good', 'complementary good', 'luxury good'], 'Giffen good.'),
    ('A perfectly inelastic demand curve is', 'vertical', ['horizontal', 'a rectangular hyperbola', 'upward sloping'], 'eD = 0.'),
    ('A perfectly elastic demand curve is', 'horizontal', ['vertical', 'a rectangular hyperbola', 'downward sloping straight line'], 'eD = ∞.'),
    ('Along a straight-line demand curve, price elasticity at the mid-point is', '1', ['0', 'infinity', 'greater than 1'], 'Lower = upper segment.'),
    ('Demand for a good with many close substitutes tends to be', 'elastic', ['inelastic', 'perfectly inelastic', 'unitary elastic always'], 'Easy to switch.'),
    ('Demand for necessities such as salt tends to be', 'inelastic', ['elastic', 'perfectly elastic', 'highly elastic'], 'Needed whatever the price.'),
    ('Price elasticity of demand is the ratio of', 'percentage change in quantity demanded to percentage change in price', ['change in price to change in quantity', 'price to quantity', 'total expenditure to price'],
     'eD = %ΔQ/%ΔP.'),
]
DEM_AR = [
    ('The demand curve usually slopes downward.', 'A fall in price makes the good relatively cheaper (substitution effect) and raises real income (income effect).', 'a', 'R explains A.'),
    ('A rise in consumers\' income shifts the demand curve for an inferior good to the right.', 'Consumers buy less of an inferior good when their income rises.', 'd', 'A is false: it shifts left. R is true.'),
    ('Demand for salt is inelastic.', 'Salt has many close substitutes.', 'c', 'A is true; R is false.'),
    ('Elasticity is different at different points on a straight-line demand curve.', 'The slope is constant but the ratio p/q changes along the line.', 'a', 'R explains A.'),
    ('A rise in the price of petrol reduces the demand for cars.', 'Cars and petrol are complementary goods.', 'a', 'R explains A.'),
    ('If total expenditure falls when price falls, demand is elastic.', 'With elastic demand, expenditure moves opposite to price.', 'd', 'A is false: that is inelastic demand. R is true.'),
]
DEM_WR = [
    ('Distinguish between a movement along the demand curve and a shift of the demand curve.', 'Movement: due to change in own price (extension/contraction). Shift: due to change in other factors such as income, related prices, tastes (increase/decrease).',
     '1½ marks each.'),
    ('Explain any three determinants of demand for a good.', 'Price of the good; income of consumers (normal/inferior); prices of related goods (substitutes/complements); tastes and preferences; expectations; number of consumers.',
     '1 mark each.'),
    ('Explain any three factors affecting the price elasticity of demand.', 'Availability of close substitutes; nature of the good (necessity vs luxury); share of income spent; time period; number of uses.', '1 mark each.'),
    ('Why does a demand curve slope downward? Give two reasons.', 'Substitution effect: good becomes relatively cheaper; income effect: real income rises; also law of DMU.', '1½ marks each.'),
]
DEM_LONG = [
    ('Explain the percentage and geometric methods of measuring price elasticity of demand. Show on a straight-line demand curve where demand is elastic, unitary and inelastic.',
     'Percentage: eD = %ΔQ/%ΔP. Geometric: lower segment/upper segment at a point; mid-point e = 1, above mid-point e > 1, below e < 1, e = ∞ at price axis, 0 at quantity axis.',
     '2 marks percentage; 2 marks geometric; 2 marks diagram (6 marks).'),
    ('Explain with diagrams how the demand curve for a good shifts when (i) the price of a substitute rises, (ii) the price of a complement rises, (iii) income rises for an inferior good.',
     '(i) Rightward shift; (ii) leftward shift; (iii) leftward shift; each with a diagram and reason.', '2 marks each (6 marks).'),
]

# ====================================================================== ch10 st5 related goods, market demand
REL = [('Tea and coffee', 'Substitutes'), ('Train travel and bus travel', 'Substitutes'), ('Butter and margarine', 'Substitutes'), ('Gel pens and ball pens', 'Substitutes'),
       ('Rice and wheat', 'Substitutes'), ('Cars and petrol', 'Complements'), ('Printers and ink cartridges', 'Complements'), ('Bread and butter', 'Complements'),
       ('Cricket bats and cricket balls', 'Complements'), ('Mobile phones and mobile data', 'Complements'), ('Pen and ink', 'Complements'),
       ('Salt and televisions', 'Unrelated goods'), ('Bicycles and table salt', 'Unrelated goods'), ('Shoes and newspapers', 'Unrelated goods')]
NI_OPTS = ['Normal good', 'Inferior good', 'Complementary good', 'Substitute good']


def inc_cls(r):
    Y1 = r.choice([20000, 25000, 30000, 40000, 50000])
    Y2 = Y1 + r.choice([5000, 10000, 15000]) * r.choice([1, -1])
    q1 = r.randint(4, 20)
    q2 = q1 + r.randint(1, 5) * r.choice([1, -1])
    g = r.choice(['Good X', 'Good Y', 'Good Z'])
    normal = (Y2 - Y1) * (q2 - q1) > 0
    ans = NI_OPTS[0] if normal else NI_OPTS[1]
    return opts_fixed(f'When a household\'s monthly income changes from {inr(Y1)} to {inr(Y2)}, its demand for {g} changes from {q1} to {q2} units per month (prices unchanged). {g} is a',
                      ans, NI_OPTS, 'Demand moves in the same direction as income → normal good.' if normal else 'Demand moves opposite to income → inferior good.', r)


CR_OPTS = ['Substitutes', 'Complements', 'Unrelated goods', 'Inferior goods']


def cross_cls(r):
    p1 = r.choice([10, 20, 30, 40, 50])
    p2 = p1 + r.choice([5, 10, -5])
    q1 = r.randint(20, 60)
    sub = r.random() < 0.5
    q2 = q1 + (r.randint(2, 10) if (p2 > p1) == sub else -r.randint(2, 10))
    ans = 'Substitutes' if sub else 'Complements'
    return opts_fixed(f'When the price of good Y changes from {inr(p1)} to {inr(p2)}, the demand for good X changes from {q1} to {q2} units (price of X unchanged). X and Y are',
                      ans, CR_OPTS, 'Demand for X moves with the price of Y → substitutes.' if sub else 'Demand for X moves opposite to the price of Y → complements.', r)


def mkt_tab(r):
    n = r.choice([2, 3])
    who = r.sample(['A', 'B', 'C', 'D'], n)
    c0 = r.choice([5, 10])
    prices = [c0 * k for k in range(1, 6)]
    rows = []
    for _ in range(n):
        q = sorted(r.sample(range(2, 40), 5), reverse=True)
        rows.append(q)
    k = r.randrange(5)
    tot = sum(rw[k] for rw in rows)
    return {'stem': 'Individual demand schedules of consumers in a market:\n' + table(['Price (₹)', *prices], [[f'Demand of {w}', *rw] for w, rw in zip(who, rows)])
            + f'\nFind the market demand at a price of {inr(prices[k])}.',
            'answer': f'{tot} units', 'key': f'Market demand = horizontal sum = {" + ".join(str(rw[k]) for rw in rows)} = {tot}.',
            'distractors': alts(f'{tot} units', [f'{rows[0][k]} units', f'{sum(rw[(k + 1) % 5] for rw in rows)} units', f'{round(tot / n)} units'], [f'{tot + 5} units'])}


def mkt_lin(r):
    for _ in range(100):
        a1, b1 = r.choice([40, 50, 60, 80, 100]), r.choice([1, 2, 4])
        a2, b2 = r.choice([30, 40, 60, 90, 120]), r.choice([1, 2, 3])
        pmax = min(a1 / b1, a2 / b2)
        p = r.randint(1, int(pmax) - 1)
        q1, q2 = a1 - b1 * p, a2 - b2 * p
        if q1 <= 0 or q2 <= 0:
            continue
        return {'stem': f'Two consumers have demand curves q₁ = {a1} − {b1}p and q₂ = {a2} − {b2}p. Find the market demand at p = {inr(p)} and write the market demand function for prices at which both buy.',
                'answer': f'{q1 + q2} units; q = {a1 + a2} − {b1 + b2}p', 'key': f'q₁ = {q1}, q₂ = {q2}; total {q1 + q2}; adding the functions: q = ({a1} + {a2}) − ({b1} + {b2})p.',
                'distractors': [f'{q1 + q2} units; q = {a1 + a2} − {b1 * b2}p' if b1 * b2 != b1 + b2 else f'{q1 + q2} units; q = {a1 + a2} − {b1 + b2 + 1}p', f'{q1} units; q = {a1} − {b1}p',
                                f'{q1 + q2 + b1 + b2} units; q = {a1 + a2} − {b1 + b2}p']}
    raise ValueError('ml')


def mkt_n(r):
    n = r.choice([10, 20, 25, 50, 100])
    a, b = r.choice([20, 30, 40, 50]), r.choice([1, 2])
    p = r.randint(1, a // b - 1)
    q = a - b * p
    return {'stem': f'A market has {n} identical consumers, each with demand q = {a} − {"" if b == 1 else b}p. Find the market demand at p = {inr(p)}.',
            'answer': f'{n * q} units', 'key': f'Each buys {a} − {b}×{p} = {q}; market = {n} × {q} = {n * q}.',
            'distractors': alts(f'{n * q} units', [f'{q} units', f'{n * a - b * p} units', f'{n * (a - p)} units'], [f'{n * q + n} units'])}


def rel_case(r):
    s_, c_ = r.choice(SUBS), r.choice(COMPS)
    return {'stem': f'Consider the markets for {s_[0]}, {s_[1]}, {c_[0]} and {c_[1]}.\n'
            + parts([f'How are {s_[0]} and {s_[1]} related?', f'What happens to the demand curve for {s_[0]} if the price of {s_[1]} rises?',
                     f'How are {c_[0]} and {c_[1]} related?', f'What happens to the demand curve for {c_[0]} if the price of {c_[1]} rises?']),
            'answer': pans(['Substitutes', 'Shifts to the right (demand increases)', 'Complements', 'Shifts to the left (demand decreases)']), 'key': '1 mark each (4 marks).'}


REL_FACT = [
    ('A normal good is one whose demand', 'rises when income rises', ['falls when income rises', 'does not change with income', 'rises when its price rises'], 'Positive income effect.'),
    ('An inferior good is one whose demand', 'falls when income rises', ['rises when income rises', 'rises when its price falls only', 'is fixed'], 'Negative income effect.'),
    ('Goods that are used together, like cars and petrol, are', 'complementary goods', ['substitute goods', 'inferior goods', 'Giffen goods'], 'Jointly demanded.'),
    ('Goods that can be used in place of each other are', 'substitute goods', ['complementary goods', 'inferior goods', 'capital goods'], 'Substitutes.'),
    ('Market demand is obtained by', 'horizontal summation of individual demand curves', ['vertical summation of individual demand curves', 'averaging individual prices', 'multiplying price and quantity'],
     'Add quantities at each price.'),
    ('A good may be normal for a consumer at low incomes and', 'inferior at high incomes', ['always normal at all incomes', 'a Giffen good at all incomes', 'complementary at high incomes'],
     'NCERT: depends on income level.'),
]
REL_AR = [
    ('A rise in the price of coffee increases the demand for tea.', 'Tea and coffee are substitutes.', 'a', 'R explains A.'),
    ('Market demand curve is flatter than individual demand curves.', 'It is the horizontal sum of individual demand curves.', 'a', 'Adding quantities at each price makes it flatter (for linear curves).'),
    ('Demand for an inferior good falls as income rises.', 'Consumers switch to better-quality goods as their income rises.', 'a', 'R explains A.'),
    ('A fall in the price of petrol reduces the demand for cars.', 'Cars and petrol are complementary goods.', 'd', 'A is false: demand for cars rises. R is true.'),
]
REL_WR = [
    ('Distinguish between normal goods and inferior goods with examples.', 'Normal: demand rises with income (fruits, branded clothes). Inferior: demand falls with income (coarse cereals, coarse cloth).', '1½ marks each.'),
    ('How does a change in the price of a related good affect the demand for a good? Explain with examples.', 'Substitute price rises → demand rises (tea/coffee); complement price rises → demand falls (cars/petrol).',
     '1½ marks each.'),
    ('How is the market demand curve derived from individual demand curves?', 'By adding the quantities demanded by all consumers at each price (horizontal summation); shown with a schedule or diagram.', '3 marks.'),
]

# ====================================================================== ch11 st1 production function
FIXV = [('Factory building', 'Fixed factor'), ('Heavy machinery', 'Fixed factor'), ('Land on which the factory stands', 'Fixed factor'), ('Permanent managerial staff', 'Fixed factor'),
        ('Raw materials', 'Variable factor'), ('Casual (daily-wage) labour', 'Variable factor'), ('Electricity used to run machines', 'Variable factor'), ('Packing material', 'Variable factor'),
        ('Fuel for the furnace', 'Variable factor')]


def pf_val(r):
    for _ in range(100):
        A = r.choice([2, 3, 4, 5, 10])
        m, s, t = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
        L, K = m * s * s, m * t * t
        if L == K and r.random() < 0.6:
            continue
        q = A * m * s * t
        if r.random() < 0.6:
            return {'stem': f'A firm\'s production function is q = {A}L^½K^½. Find the output when L = {L} and K = {K}.', 'answer': f'{q} units',
                    'key': f'q = {A} × √({L} × {K}) = {A} × √{L * K} = {A} × {m * s * t} = {q}.',
                    'distractors': alts(f'{q} units', [f'{A * (L + K)} units', f'{A * L * K} units', f'{m * s * t} units'], [f'{q + A} units'])}
        return {'stem': f'A firm\'s production function is q = {A}L^½K^½. With K = {K}, how many units of labour are needed to produce {q} units?', 'answer': f'L = {L}',
                'key': f'{q} = {A}√({K}L) ⇒ √({K}L) = {q // A} ⇒ {K}L = {(q // A) ** 2} ⇒ L = {L}.',
                'distractors': alts(f'L = {L}', [f'L = {q // A}', f'L = {K}', f'L = {L * 2}'], [f'L = {L + 1}'])}
    raise ValueError('pf')


def pf_case(r):
    A = r.choice([2, 4, 5, 10])
    L, K = r.choice([(4, 9), (9, 4), (16, 4), (4, 16), (25, 4), (9, 16), (1, 36), (36, 1)])
    q = A * int(math.isqrt(L * K))
    return {'stem': f'A firm\'s production function is q = {A}L^½K^½.\n'
            + parts([f'Find the output when L = {L} and K = {K}.', 'If K is fixed at this level and L is increased, which time period is this?',
                     'What is the output if both L and K are doubled?', 'What kind of returns to scale does this function show?']),
            'answer': pans([f'{q} units', 'Short run (one factor fixed)', f'{2 * q} units', 'Constant returns to scale (½ + ½ = 1)']), 'key': '1 mark each (4 marks).'}


PF_FACT = [
    ('A production function shows the relation between', 'physical inputs and the maximum output', ['price and quantity', 'cost and revenue', 'income and consumption'], 'Technical relation.'),
    ('The short run is a period in which', 'at least one factor of production is fixed', ['all factors are variable', 'all factors are fixed', 'prices are fixed by the government'], 'SR.'),
    ('The long run is a period in which', 'all factors of production can be varied', ['at least one factor is fixed', 'output cannot change', 'only labour can change'], 'LR.'),
    ('An isoquant shows', 'combinations of labour and capital that give the same output', ['bundles of goods giving equal satisfaction', 'combinations of goods costing the same',
     'the maximum output of two goods'], 'Iso-product curve.'),
    ('A factor whose quantity can be changed in the short run is a', 'variable factor', ['fixed factor', 'free factor', 'scarce factor'], 'Variable factor.'),
    ('Production function analysis is a', 'technological (physical) relationship', ['price relationship', 'demand relationship', 'monetary relationship'], 'Physical quantities.'),
]
PF_AR = [
    ('In the short run, a firm cannot change the size of its factory.', 'Some factors of production are fixed in the short run.', 'a', 'R explains A.'),
    ('In the long run, there are no fixed factors.', 'All factors can be varied in the long run.', 'a', 'R explains A.'),
    ('The short run and long run are defined by calendar time.', 'They depend on whether all factors can be varied.', 'd', 'A is false: they are defined by variability of factors. R is true.'),
    ('Raw materials are a variable factor.', 'Their quantity changes with the level of output.', 'a', 'R explains A.'),
]
PF_WR = [
    ('Distinguish between the short run and the long run production function.', 'SR: some factors fixed, output changed by varying variable factors (returns to a factor). LR: all factors variable, scale changes (returns to scale).',
     '1½ marks each.'),
    ('Distinguish between fixed and variable factors with examples.', 'Fixed: cannot be changed in SR, e.g. building, machinery. Variable: can be changed with output, e.g. raw materials, casual labour.', '1½ marks each.'),
]

# ====================================================================== ch11 st2 TP AP MP
def mp_seq(r):
    a = r.randint(4, 12)
    u, v = r.randint(2, 6), r.randint(1, 5)
    rise = [a, a + u, a + u + v]
    fall = []
    x = rise[-1]
    while x > 0:
        x -= r.randint(3, 8)
        fall.append(max(x, 0))
        if x <= 0:
            break
    if fall[-1] != 0:
        fall.append(0)
    neg = -r.randint(2, 6)
    mps = rise + fall + [neg]
    if len(mps) > 10 or len(mps) < 6:
        raise ValueError('len')
    return mps


def tp_tab(mps):
    tps = cumsum(mps)
    return tps, table(['Labour (units)', *range(1, len(mps) + 1)], [['TP', *map(num, tps)]])


def tp_mp(r):
    mps = mp_seq(r)
    tps, tb = tp_tab(mps)
    k = r.randrange(1, len(mps))
    if r.random() < 0.5:
        return {'stem': f'With fixed capital, a firm\'s total product schedule is:\n{tb}\nFind the marginal product of unit {k + 1} of labour.', 'answer': num(mps[k]),
                'key': f'MP = TP({k + 1}) − TP({k}) = {tps[k]} − {tps[k - 1]} = {num(mps[k])}.', 'distractors': ndist(mps[k], tps[k], round(tps[k] / (k + 1), 2), mps[k - 1])}
    ap = tps[k] / (k + 1)
    return {'stem': f'With fixed capital, a firm\'s total product schedule is:\n{tb}\nFind the average product of labour when {k + 1} units are employed.', 'answer': d2(ap),
            'key': f'AP = TP/L = {tps[k]}/{k + 1} = {d2(ap)}.', 'distractors': ndist(round(ap, 2), mps[k], tps[k], round(tps[k] / k, 2))}


def mp_to_tp(r):
    mps = mp_seq(r)
    tps = cumsum(mps)
    k = r.randrange(2, len(mps))
    return {'stem': 'The marginal product schedule of labour (capital fixed) is:\n' + table(['Labour (units)', *range(1, len(mps) + 1)], [['MP', *map(num, mps)]]) + f'\nFind TP and AP at {k + 1} units of labour.',
            'answer': f'TP = {tps[k]}; AP = {d2(tps[k] / (k + 1))}', 'key': f'TP = ΣMP = {tps[k]}; AP = {tps[k]}/{k + 1} = {d2(tps[k] / (k + 1))}.',
            'distractors': [f'TP = {mps[k] * (k + 1)}; AP = {mps[k]}', f'TP = {tps[k - 1]}; AP = {d2(tps[k - 1] / (k + 1))}', f'TP = {tps[k]}; AP = {d2(tps[k] / k)}']}


PH = ['Phase I: increasing returns to a factor (MP rises)', 'Phase II: diminishing returns to a factor (MP falls but is positive)', 'Phase III: negative returns to a factor (MP is negative)',
      'Constant returns to scale']


def lvp_phase(r):
    mps = mp_seq(r)
    tps, tb = tp_tab(mps)
    cands = [i for i in range(1, len(mps)) if mps[i] != 0]
    k = r.choice(cands)
    ph = 0 if mps[k] > mps[k - 1] else (2 if mps[k] < 0 else 1)
    return opts_fixed(f'With fixed capital, total product is:\n{tb}\nIn which phase of the law of variable proportions is unit {k + 1} of labour?', PH[ph], PH,
                      f'MP of unit {k + 1} = {tps[k]} − {tps[k - 1]} = {num(mps[k])} (previous MP {num(mps[k - 1])}).', r)


def lvp_full(r):
    mps = mp_seq(r)
    tps, tb = tp_tab(mps)
    z = mps.index(0)
    rise_end = max(i for i in range(1, len(mps)) if mps[i] > mps[i - 1]) + 1
    return {'stem': f'With fixed capital, total product is:\n{tb}\nCalculate MP at each level and identify the three phases of the law of variable proportions.',
            'answer': f'MP: {", ".join(num(m) for m in mps)}. Phase I (MP rising): up to {rise_end} units; Phase II (MP falling, positive): {rise_end + 1}–{z + 1} units (TP maximum = {tps[z]} where MP = 0); Phase III (MP negative): beyond {z + 1} units.',
            'key': '2 marks MP; 2 marks phases (4 marks).'}


def tp_case(r):
    mps = mp_seq(r)
    tps, tb = tp_tab(mps)
    z = mps.index(0)
    k = r.randrange(1, z)
    return {'stem': f'A farmer with fixed land increases labour:\n{tb}\n'
            + parts([f'Find MP of unit {k + 1}.', f'Find AP at {k + 1} units.', 'At what level of labour is TP maximum? What is MP there?', 'Should the farmer ever employ labour in Phase III? Why?']),
            'answer': pans([num(mps[k]), d2(tps[k] / (k + 1)), f'{z + 1} units (TP = {tps[z]}); MP = 0', 'No: MP is negative, so extra workers reduce total output']),
            'key': '1 mark each (4 marks).'}


TPF = [
    ('Marginal product of labour is', 'the change in total product from one more unit of labour', ['total product divided by labour', 'total product of all factors', 'output per unit of capital'], 'MP = ΔTP/ΔL.'),
    ('Average product of labour is', 'total product divided by units of labour', ['change in TP per unit change in labour', 'TP minus MP', 'TP times labour'], 'AP = TP/L.'),
    ('When MP is zero, TP is', 'maximum', ['minimum', 'zero', 'falling at an increasing rate'], 'TP peaks.'),
    ('When MP is greater than AP, AP', 'rises', ['falls', 'is constant', 'is zero'], 'Marginal pulls average up.'),
    ('MP cuts AP at', 'the maximum point of AP', ['the minimum point of AP', 'the origin', 'the point where TP is maximum'], 'MP = AP at max AP.'),
    ('The law of variable proportions applies in', 'the short run', ['the long run', 'both runs equally', 'very long run only'], 'One factor fixed.'),
    ('Diminishing returns to a factor set in mainly because', 'the fixed factor becomes scarce relative to the variable factor', ['all factors are increased', 'prices fall', 'demand falls'],
     'Fixed factor shared by more units.'),
    ('In Phase III of the law of variable proportions', 'TP falls and MP is negative', ['TP rises at an increasing rate', 'MP is maximum', 'AP is rising'], 'Negative returns.'),
]
TP_AR = [
    ('TP rises as long as MP is positive.', 'TP is the sum of the marginal products.', 'a', 'R explains A.'),
    ('A rational producer never operates in Phase III.', 'In Phase III, the MP of the variable factor is negative.', 'a', 'R explains A.'),
    ('AP rises when MP is less than AP.', 'MP pulls AP towards itself.', 'd', 'A is false: AP falls when MP < AP. R is true.'),
    ('In Phase I, MP rises.', 'Better use of the fixed factor and division of labour raise efficiency.', 'a', 'R explains A.'),
    ('The law of variable proportions operates in the long run.', 'In the long run all factors are variable.', 'd', 'A is false: it operates in the short run. R is true.'),
]
TP_WR = [
    ('Explain the relationship between AP and MP.', 'When MP > AP, AP rises; when MP = AP, AP is maximum; when MP < AP, AP falls; MP can be negative, AP cannot.', '1 mark each.'),
    ('Explain the relationship between TP and MP.', 'MP rising → TP rises at an increasing rate; MP falling but positive → TP rises at a diminishing rate; MP = 0 → TP maximum; MP negative → TP falls.',
     '3 marks.'),
    ('Give two reasons for the operation of increasing returns to a factor.', 'Better utilisation of the fixed factor; division of labour and specialisation as more variable factor is employed.', '1½ marks each.'),
]
TP_LONG = [
    ('Explain the law of variable proportions with the help of a schedule and a diagram. Give reasons for each phase.',
     'Phase I: MP rises (better use of fixed factor); Phase II: MP falls but positive (fixed factor becomes scarce); Phase III: MP negative (overcrowding). Schedule and TP/MP diagram.',
     '2 marks schedule; 2 marks diagram; 2 marks reasons (6 marks).'),
]

# ====================================================================== ch11 st3 returns to scale
RTS = ['Increasing returns to scale', 'Constant returns to scale', 'Decreasing returns to scale', 'Diminishing returns to a factor']


def rts_cd(r):
    a = Fraction(r.randint(1, 9), 10)
    b = Fraction(r.randint(1, 9), 10)
    A = r.choice([1, 2, 3, 5, 10])
    s = a + b
    k = 0 if s > 1 else (1 if s == 1 else 2)
    return opts_fixed(f'A production function is q = {A if A > 1 else ""}L^{num(float(a))}K^{num(float(b))}. It shows', RTS[k], RTS,
                      f'Sum of exponents = {num(float(a))} + {num(float(b))} = {num(float(s))} ' + ['> 1 → IRS.', '= 1 → CRS.', '< 1 → DRS.'][k], r)


def rts_num(r):
    L, K = r.randint(2, 10), r.randint(2, 10)
    q = r.choice([50, 80, 100, 120, 150, 200])
    m = r.choice([2, 3])
    k = r.randrange(3)
    q2 = q * m + (q // r.choice([2, 4, 5]) if k == 0 else 0) - (q // r.choice([2, 4, 5]) if k == 2 else 0)
    return opts_fixed(f'A firm uses {L} units of labour and {K} units of capital to produce {q} units. When it uses {L * m} units of labour and {K * m} units of capital, output becomes {q2} units. This shows',
                      RTS[k], RTS, f'Inputs × {m}; output × {num(q2 / q)} ' + ['(more than proportionate) → IRS.', '(same proportion) → CRS.', '(less than proportionate) → DRS.'][k], r)


def rts_case(r):
    a = Fraction(r.randint(2, 8), 10)
    b = Fraction(r.randint(2, 8), 10)
    s = a + b
    k = 0 if s > 1 else (1 if s == 1 else 2)
    return {'stem': f'A firm\'s production function is q = L^{num(float(a))}K^{num(float(b))}.\n'
            + parts(['What is the sum of the exponents?', 'Which type of returns to scale does it show?', 'If both inputs are doubled, will output be more than, equal to, or less than double?',
                     'Is returns to scale a short-run or long-run concept? Why?']),
            'answer': pans([num(float(s)), RTS[k], ['More than double', 'Exactly double', 'Less than double'][k], 'Long run: all inputs are changed in the same proportion']),
            'key': '1 mark each (4 marks).'}


RTS_FACT = [
    ('Returns to scale is a', 'long-run concept', ['short-run concept', 'market-period concept', 'consumer concept'], 'All inputs varied.'),
    ('If all inputs are doubled and output more than doubles, there are', 'increasing returns to scale', ['constant returns to scale', 'decreasing returns to scale', 'diminishing returns to a factor'], 'IRS.'),
    ('Under constant returns to scale, output changes', 'in the same proportion as inputs', ['more than inputs', 'less than inputs', 'not at all'], 'CRS.'),
    ('For q = L^aK^b, decreasing returns to scale occur when', 'a + b < 1', ['a + b > 1', 'a + b = 1', 'a = b'], 'DRS.'),
    ('Increasing returns to scale can arise from', 'specialisation and economies of large-scale production', ['difficulties of management', 'a fixed factor', 'falling prices'], 'Economies of scale.'),
]
RTS_AR = [
    ('Returns to scale can be studied only in the long run.', 'In the long run all factors can be varied in the same proportion.', 'a', 'R explains A.'),
    ('q = L^0.5K^0.5 shows constant returns to scale.', 'The exponents add up to 1.', 'a', 'R explains A.'),
    ('Decreasing returns to scale mean output falls when inputs rise.', 'Under DRS, output rises less than proportionately.', 'd', 'A is false; R is true.'),
    ('Returns to a factor and returns to scale mean the same thing.', 'Returns to a factor change only one input while others stay fixed.', 'd', 'A is false; R is true.'),
]
RTS_WR = [
    ('Distinguish between returns to a factor and returns to scale.', 'Returns to a factor: SR, one input varied, others fixed (factor ratio changes). Returns to scale: LR, all inputs varied in the same proportion (factor ratio constant).',
     '1½ marks each.'),
    ('Explain increasing, constant and decreasing returns to scale with a numerical example each.', 'Inputs doubled: output more than double (IRS), exactly double (CRS), less than double (DRS).', '1 mark each.'),
]

# ====================================================================== ch11 st4 costs
COST_ITEMS = [('Rent of the factory building', 'Fixed cost'), ('Salary of permanent staff', 'Fixed cost'), ('Interest on borrowed capital', 'Fixed cost'),
              ('Insurance premium of the factory', 'Fixed cost'), ('Licence fee', 'Fixed cost'), ('Cost of raw materials', 'Variable cost'), ('Wages of daily-wage workers', 'Variable cost'),
              ('Electricity used to run machines', 'Variable cost'), ('Packing and transport of goods', 'Variable cost'), ('Fuel for machines', 'Variable cost')]


def cost_sched(r, n=6):
    tfc = r.choice([60, 120, 180, 240])
    m0 = r.randint(14, 30)
    d1, d2_ = r.randint(2, 6), r.randint(1, 4)
    mcs = [m0, m0 - d1, m0 - d1 - d2_]
    while len(mcs) < n:
        mcs.append(mcs[-1] + r.randint(2, 8))
    if min(mcs) <= 0:
        raise ValueError('mc')
    tvc = cumsum(mcs)
    return tfc, mcs, tvc


def cost_q(r):
    tfc, mcs, tvc = cost_sched(r)
    n = len(mcs)
    k = r.randrange(1, n)
    q = k + 1
    tc = [tfc + v for v in tvc]
    v = r.choice(['TC', 'AFC', 'AVC', 'AC', 'MC'])
    tb = table(['Output (units)', 0, *range(1, n + 1)], [['TC (₹)', tfc, *tc]])
    vals = {'TC': tc[k], 'AFC': tfc / q, 'AVC': tvc[k] / q, 'AC': tc[k] / q, 'MC': mcs[k]}
    keys = {'TC': f'TC at {q} = {tc[k]} (given).', 'AFC': f'TFC = TC at zero output = {tfc}; AFC = {tfc}/{q} = {d2(tfc / q)}.',
            'AVC': f'TFC = {tfc}; TVC = {tc[k]} − {tfc} = {tvc[k]}; AVC = {tvc[k]}/{q} = {d2(tvc[k] / q)}.', 'AC': f'AC = TC/Q = {tc[k]}/{q} = {d2(tc[k] / q)}.',
            'MC': f'MC = TC({q}) − TC({k}) = {tc[k]} − {tc[k - 1]} = {mcs[k]}.'}
    if v == 'TC':
        v = 'AVC'
    ans = vals[v]
    return {'stem': f'A firm\'s total cost schedule is:\n{tb}\nFind the {v} at {q} units of output.', 'answer': inr(round(ans, 2)), 'key': keys[v],
            'distractors': alts(inr(round(ans, 2)), [inr(round(x, 2)) for x in (tc[k] / q, tvc[k] / q, tfc / q, mcs[k], tc[k] / k if k else tc[k]) if abs(x - ans) > 1e-9])}


def cost_fill(r):
    tfc, mcs, tvc = cost_sched(r, 5)
    rows = [[q, tfc, tvc[q - 1], tfc + tvc[q - 1], d2(tfc / q), d2(tvc[q - 1] / q), d2((tfc + tvc[q - 1]) / q), mcs[q - 1]] for q in range(1, 6)]
    return {'stem': f'A firm has total fixed cost of {inr(tfc)}. Its total variable cost is:\n' + table(['Output', *range(1, 6)], [['TVC (₹)', *tvc]])
            + '\nPrepare a table showing TC, AFC, AVC, AC and MC.',
            'answer': table(['Q', 'TFC', 'TVC', 'TC', 'AFC', 'AVC', 'AC', 'MC'], rows), 'key': '½ mark per correct column item set; 4 marks in all (TC, AFC, AVC/AC, MC: 1 mark each).'}


def afc_q(r):
    q1 = r.choice([2, 4, 5, 6, 10])
    afc1 = r.choice([30, 40, 60, 90, 120])
    tfc = q1 * afc1
    q2 = r.choice([x for x in (3, 4, 5, 6, 8, 10, 12, 15, 20) if x != q1 and tfc % x == 0] or [q1 * 2])
    ans = tfc / q2
    return {'stem': f'A firm\'s AFC is {inr(afc1)} when it produces {q1} units. What will AFC be at {q2} units?', 'answer': inr(round(ans, 2)),
            'key': f'TFC = AFC × Q = {afc1} × {q1} = {tfc} (constant); AFC = {tfc}/{q2} = {d2(ans)}.',
            'distractors': alts(inr(round(ans, 2)), [inr(afc1), inr(afc1 * q2 / q1), inr(tfc)], [inr(round(ans + 5, 2))])}


def avc_min(r):
    for _ in range(100):
        avc = [r.randint(20, 30)]
        for _ in range(2):
            avc.append(avc[-1] - r.randint(1, 4))
        for _ in range(3):
            avc.append(avc[-1] + r.randint(1, 4))
        mn = min(avc)
        if avc.count(mn) == 1:
            break
    tvc = [a * (i + 1) for i, a in enumerate(avc)]
    k = avc.index(mn)
    return {'stem': 'A firm\'s total variable cost schedule is:\n' + table(['Output', *range(1, 7)], [['TVC (₹)', *tvc]]) + '\nAt what level of output is AVC minimum?',
            'answer': f'{k + 1} units (AVC = {inr(mn)})', 'key': f'AVC = TVC/Q: {", ".join(str(a) for a in avc)}; minimum {mn} at {k + 1} units.',
            'distractors': alts(f'{k + 1} units (AVC = {inr(mn)})', [f'1 unit (AVC = {inr(avc[0])})', f'{k + 2} units (AVC = {inr(avc[k + 1])})', f'{k} units (AVC = {inr(avc[k - 1])})' if k else f'6 units (AVC = {inr(avc[5])})'])}


def cost_case(r):
    tfc, mcs, tvc = cost_sched(r, 5)
    tc = [tfc + v for v in tvc]
    k = r.randrange(1, 5)
    return {'stem': 'A firm\'s cost schedule is:\n' + table(['Output', 0, 1, 2, 3, 4, 5], [['TC (₹)', tfc, *tc]]) + '\n'
            + parts(['What is the total fixed cost? How do you know?', f'Find AVC at {k + 1} units.', f'Find MC of unit {k + 1}.', 'What happens to AFC as output rises, and why?']),
            'answer': pans([f'{inr(tfc)}: TC at zero output', d2(tvc[k] / (k + 1)), str(mcs[k]), 'It keeps falling (TFC spread over more units); AFC curve is a rectangular hyperbola']),
            'key': '1 mark each (4 marks).'}


COST_FACT = [
    ('The AFC curve is a', 'rectangular hyperbola', ['U-shaped curve', 'horizontal straight line', 'vertical line'], 'AFC × Q = TFC.'),
    ('The TFC curve is a', 'horizontal straight line', ['U-shaped curve', 'straight line from the origin', 'rectangular hyperbola'], 'Constant.'),
    ('The TVC curve starts from', 'the origin', ['the level of TFC', 'the maximum point', 'the y-axis above TFC'], 'TVC = 0 at Q = 0.'),
    ('The MC curve cuts the AVC and AC curves at', 'their minimum points', ['their maximum points', 'the origin', 'any point'], 'Marginal–average relation.'),
    ('The short-run AC curve is U-shaped because of', 'the law of variable proportions', ['returns to scale', 'the law of demand', 'perfect competition'], 'SR U-shape.'),
    ('The vertical gap between the AC and AVC curves equals', 'AFC', ['MC', 'TFC', 'TVC'], 'AC − AVC = AFC.'),
    ('As output rises, the gap between AC and AVC', 'narrows but never becomes zero', ['widens', 'stays constant', 'becomes zero at some output'], 'AFC falls but stays positive.'),
    ('Marginal cost is', 'the change in total cost from producing one more unit', ['total cost divided by output', 'fixed cost per unit', 'total variable cost'], 'MC = ΔTC.'),
    ('The long-run AC curve is U-shaped because of', 'returns to scale', ['the law of variable proportions', 'fixed costs', 'the law of demand'], 'IRS then CRS then DRS.'),
]
COST_AR = [
    ('AFC can never be zero.', 'TFC is a positive constant divided by output.', 'a', 'R explains A.'),
    ('MC is not affected by fixed cost.', 'Fixed cost does not change with output.', 'a', 'R explains A.'),
    ('The AC curve reaches its minimum before the AVC curve.', 'AC = AVC + AFC, and AFC keeps falling.', 'd', 'A is false: AVC reaches its minimum first; R is true.'),
    ('TC and TVC curves are parallel.', 'The vertical distance between them equals TFC, which is constant.', 'a', 'R explains A.'),
    ('When MC is below AC, AC rises.', 'Marginal values pull the average towards themselves.', 'd', 'A is false: AC falls when MC < AC. R is true.'),
]
COST_WR = [
    ('Explain the relationship between AC and MC.', 'When MC < AC, AC falls; MC = AC at minimum AC; MC > AC, AC rises; MC cuts AC from below at its minimum.', '1 mark each.'),
    ('Why is the AFC curve a rectangular hyperbola?', 'AFC × Q = TFC, a constant; so the area under every point is the same and AFC falls continuously, never touching the axes.', '3 marks.'),
    ('Distinguish between fixed costs and variable costs with two examples each.', 'Fixed: do not change with output (rent, salary of permanent staff). Variable: change with output (raw materials, daily wages).', '1½ marks each.'),
]
COST_LONG = [
    ('Explain the shapes of AFC, AVC, AC and MC curves in the short run with a diagram. Why does MC cut AVC and AC at their minimum points?',
     'AFC: rectangular hyperbola; AVC, AC, MC: U-shaped due to law of variable proportions; MC cuts AVC and AC from below at their minima because the average falls while marginal is below it and rises when marginal is above it.',
     '2 marks shapes; 2 marks diagram; 2 marks reason (6 marks).'),
]

# ====================================================================== ch12 st1 perfect competition, revenue
def rev_tab(r):
    p = r.choice([5, 8, 10, 12, 15, 20, 25])
    n = 6
    q = r.randrange(2, n + 1)
    v = r.choice(['TR', 'AR', 'MR'])
    tr = [p * i for i in range(n + 1)]
    tb = table(['Output', *range(n + 1)], [['TR (₹)', *tr]])
    if v == 'TR':
        return {'stem': f'A firm in a perfectly competitive market sells at {inr(p)} per unit. Find its total revenue from {q} units, and its AR and MR.', 'answer': f'TR = {inr(p * q)}; AR = MR = {inr(p)}',
                'key': f'TR = p × q = {p} × {q} = {p * q}; AR = TR/q = {p}; MR = ΔTR = {p}.',
                'distractors': [f'TR = {inr(p * q)}; AR = {inr(p)}, MR = {inr(p * (q - 1))}', f'TR = {inr(p + q)}; AR = MR = {inr(p)}', f'TR = {inr(p * q)}; AR = {inr(p * q)}, MR = {inr(p)}']}
    ans = inr(p)
    return {'stem': f'A perfectly competitive firm\'s total revenue schedule is:\n{tb}\nFind the {v} at {q} units.', 'answer': ans,
            'key': (f'AR = TR/q = {tr[q]}/{q} = {p}.' if v == 'AR' else f'MR = TR({q}) − TR({q - 1}) = {tr[q]} − {tr[q - 1]} = {p}.') + ' Under perfect competition AR = MR = price.',
            'distractors': alts(ans, [inr(tr[q]), inr(tr[q - 1]), inr(p * 2)], [inr(p + 1)])}


def rev_case(r):
    p = r.choice([6, 8, 10, 12, 15, 20])
    q = r.randint(3, 8)
    who = name(r)
    return {'stem': f'{who} sells wheat in a perfectly competitive market where the price is {inr(p)} per kg.\n'
            + parts([f'Find TR from selling {q} kg.', f'What are AR and MR at {q} kg?', 'What is the shape of the TR curve?', f'Can {who} sell more by lowering the price slightly? Why?']),
            'answer': pans([inr(p * q), f'AR = MR = {inr(p)}', 'A straight line through the origin with slope equal to price', 'No need: any quantity can be sold at the market price; the firm is a price taker']),
            'key': '1 mark each (4 marks).'}


PC_FACT = [
    ('Under perfect competition, a firm is a', 'price taker', ['price maker', 'monopolist', 'price leader'], 'Takes market price.'),
    ('Which is NOT a feature of perfect competition?', 'Product differentiation', ['Large number of buyers and sellers', 'Homogeneous products', 'Free entry and exit'], 'Products are identical.'),
    ('For a perfectly competitive firm, AR and MR are', 'equal to the price', ['falling', 'zero', 'greater than price'], 'AR = MR = p.'),
    ('The TR curve of a perfectly competitive firm is', 'an upward sloping straight line from the origin', ['an inverted U-shaped curve', 'a horizontal line', 'a rectangular hyperbola'], 'TR = p × q.'),
    ('The demand curve facing a perfectly competitive firm is', 'perfectly elastic (horizontal)', ['perfectly inelastic', 'downward sloping', 'upward sloping'], 'At market price.'),
    ('Perfect knowledge in perfect competition means that', 'buyers and sellers know the market price', ['firms know each other\'s costs', 'the government sets the price', 'products are different'],
     'No one charges more.'),
]
PC_AR = [
    ('A perfectly competitive firm is a price taker.', 'Each firm\'s output is a very small part of the total market supply.', 'a', 'R explains A.'),
    ('MR is less than AR for a perfectly competitive firm.', 'The firm can sell any quantity at the market price.', 'd', 'A is false: MR = AR. R is true.'),
    ('Firms in perfect competition do not spend on advertisement.', 'Products are homogeneous and buyers have perfect knowledge.', 'a', 'R explains A.'),
    ('The TR curve of a perfectly competitive firm is a straight line through the origin.', 'Price remains constant whatever the output of the firm.', 'a', 'R explains A.'),
]
PC_WR = [
    ('Explain any three features of perfect competition.', 'Large number of buyers and sellers; homogeneous products; free entry and exit; perfect knowledge; perfect mobility.', '1 mark each.'),
    ('Why is a firm under perfect competition a price taker?', 'Large number of firms each with a tiny share; homogeneous product; perfect knowledge; so price is set by market demand and supply.', '3 marks.'),
    ('Why is AR equal to MR under perfect competition?', 'Price is constant; each extra unit adds the same price to TR; so MR = p = AR.', '3 marks.'),
]
PC_LONG = [
    ('Explain the features of perfect competition and show the shapes of TR, AR and MR curves of a firm in such a market.',
     'Features: many buyers and sellers, homogeneous product, free entry/exit, perfect knowledge, perfect mobility; TR straight line from origin, AR = MR horizontal at market price.',
     '4 marks features; 2 marks curves (6 marks).'),
]

# ====================================================================== ch12 st2 profit maximisation
def pm_data(r):
    for _ in range(200):
        tfc = r.choice([20, 30, 40, 50, 60])
        m0 = r.randint(10, 20)
        mcs = [m0, m0 - r.randint(2, 5)]
        mcs.append(mcs[-1] - r.randint(1, 3))
        while len(mcs) < 7:
            mcs.append(mcs[-1] + r.randint(2, 6))
        if min(mcs) <= 0:
            continue
        tvc = cumsum(mcs)
        rising = [i for i in range(3, 7) if mcs[i] > mcs[i - 1]]
        qi = r.choice(rising)
        p = mcs[qi]
        if p < tvc[qi] / (qi + 1):
            continue
        if any(mcs[j] == p for j in range(7) if j != qi and mcs[j] > mcs[j - 1 if j else 0]):
            continue
        return tfc, mcs, tvc, qi, p
    raise ValueError('pm')


def pm_tab(r):
    tfc, mcs, tvc, qi, p = pm_data(r)
    tc = [tfc + v for v in tvc]
    q = qi + 1
    prof = p * q - tc[qi]
    return {'stem': f'A perfectly competitive firm faces a price of {inr(p)}. Its cost schedule is:\n' + table(['Output', 0, *range(1, 8)], [['TC (₹)', tfc, *tc]])
            + '\nFind the profit-maximising output and the profit (or loss) at that output.',
            'answer': f'{q} units; profit = {inr(prof)}' if prof >= 0 else f'{q} units; loss = {inr(-prof)}',
            'key': f'MC: {", ".join(map(str, mcs))}. p = MC = {p} at {q} units with MC rising (and p ≥ AVC = {d2(tvc[qi] / q)}). TR = {p * q}, TC = {tc[qi]} → {"profit" if prof >= 0 else "loss"} {abs(prof)}. '
                   f'(Unit {q} adds nothing to profit, so profit at {q - 1} units is the same; by the rule p = MC the answer is {q} units.)',
            'distractors': alts(f'{q} units; profit = {inr(prof)}' if prof >= 0 else f'{q} units; loss = {inr(-prof)}',
                                [f'{q + 1 if q < 7 else q - 2} units; profit = {inr(abs(prof) + p)}', f'{q} units; profit = {inr(p * q)}', f'{q} units; profit = {inr(abs(prof) + tfc)}',
                                 f'{q} units; loss = {inr(abs(prof) + p)}'])}


PMR_OPTS = ['Increase output', 'Reduce output', 'Keep output unchanged', 'Shut down at once']


def pm_rule(r):
    p = r.randint(10, 40)
    kind = r.choice(['up', 'down', 'eq'])
    mc = p - r.randint(2, 6) if kind == 'up' else (p + r.randint(2, 6) if kind == 'down' else p)
    avc = p - r.randint(1, 5)
    q = r.randint(10, 100)
    ans = {'up': PMR_OPTS[0], 'down': PMR_OPTS[1], 'eq': PMR_OPTS[2]}[kind]
    return opts_fixed(f'A perfectly competitive firm sells at {inr(p)}. At its current output of {q} units, MC = {inr(mc)} and MC is rising; AVC = {inr(avc)}. To maximise profit, the firm should',
                      ans, PMR_OPTS, {'up': 'p > MC: each extra unit adds more to revenue than to cost.', 'down': 'p < MC: the last units cost more than they earn.',
                                      'eq': 'p = MC with MC rising: profit is maximum.'}[kind] + ' p > AVC, so no shut-down.', r)


def profit_area(r):
    p = r.randint(10, 40)
    q = r.choice([10, 20, 25, 40, 50, 100])
    ac = p + r.choice([-6, -4, -3, -2, 2, 3, 5])
    v = (p - ac) * q
    ans = f'Profit of {inr(v)}' if v > 0 else f'Loss of {inr(-v)}'
    return {'stem': f'A perfectly competitive firm produces {q} units at a market price of {inr(p)}. Its average cost at this output is {inr(ac)}. Find its profit or loss.',
            'answer': ans, 'key': f'Profit = (p − AC) × q = ({p} − {ac}) × {q} = {num(v)}.',
            'distractors': alts(ans, [f'Loss of {inr(abs(v))}' if v > 0 else f'Profit of {inr(abs(v))}', f'Profit of {inr(p * q)}', f'Profit of {inr(abs(p - ac))}'], [f'Loss of {inr(ac * q)}'])}


def pm_case(r):
    tfc, mcs, tvc, qi, p = pm_data(r)
    tc = [tfc + v for v in tvc]
    q = qi + 1
    prof = p * q - tc[qi]
    return {'stem': f'A firm sells in a perfectly competitive market at {inr(p)} per unit. Its costs are:\n' + table(['Output', 0, *range(1, 8)], [['TC (₹)', tfc, *tc]]) + '\n'
            + parts(['Calculate MC at each output.', 'At what output is profit maximum? State the conditions used.', 'Calculate TR and profit at that output.', 'Why will the firm not produce one more unit?']),
            'answer': pans([', '.join(map(str, mcs)), f'{q} units: p = MC and MC rising', f'TR = {inr(p * q)}; profit = {inr(prof)}' if prof >= 0 else f'TR = {inr(p * q)}; loss = {inr(-prof)} (but p ≥ AVC)',
                            f'MC of the next unit ({mcs[qi + 1] if qi + 1 < 7 else "higher"}) exceeds the price']),
            'key': '1 mark each (4 marks).'}


PM_FACT = [
    ('A perfectly competitive firm maximises profit where', 'price equals MC and MC is rising', ['price equals AC', 'TR is maximum', 'MC is minimum'], 'p = MC, MC non-decreasing.'),
    ('In the short run, a firm continues production only if price is at least', 'minimum AVC', ['minimum AC', 'MC at zero output', 'AFC'], 'Covers variable cost.'),
    ('In the long run, a firm continues production only if price is at least', 'minimum AC', ['minimum AVC', 'AFC', 'zero'], 'Covers all costs.'),
    ('Profit equals', 'total revenue minus total cost', ['total revenue minus variable cost', 'price minus MC', 'AR minus MR'], 'π = TR − TC.'),
    ('If price is greater than MC at the current output, the firm can raise profit by', 'increasing output', ['reducing output', 'raising price', 'shutting down'], 'Extra unit earns more than it costs.'),
    ('In the TR–TC approach, profit is maximum where', 'the vertical gap between TR and TC is largest with TR above TC', ['TR equals TC', 'TC is minimum', 'TR is maximum'], 'Largest positive gap.'),
]
PM_AR = [
    ('A firm will not produce where MC is falling even if price equals MC.', 'Beyond that point, producing more adds more to revenue than to cost.', 'a', 'R explains A.'),
    ('In the short run, a firm may produce even at a loss.', 'It covers its variable costs and part of its fixed costs if price ≥ AVC.', 'a', 'R explains A.'),
    ('Profit is maximum where TR is maximum.', 'Profit depends on both revenue and cost.', 'd', 'A is false; R is true.'),
    ('If p < MC, the firm should reduce output.', 'The last unit adds more to cost than to revenue.', 'a', 'R explains A.'),
]
PM_WR = [
    ('State the conditions of profit maximisation for a perfectly competitive firm.', 'p = MC; MC is non-decreasing at that output; SR: p ≥ AVC; LR: p ≥ AC.', '1 mark each (any three).'),
    ('Why must MC be rising at the profit-maximising output?', 'If MC is falling where p = MC, producing a little more makes p > MC, adding to profit; so that point is not the maximum.', '3 marks.'),
]
PM_LONG = [
    ('Explain the equilibrium of a perfectly competitive firm using the MR–MC approach with a diagram.', 'MR = AR = p horizontal; profit max where p = MC and MC rising; SR p ≥ AVC, LR p ≥ AC; diagram showing two points where p = MC and explaining which is chosen.',
     '2 marks conditions; 2 marks diagram; 2 marks explanation (6 marks).'),
]

# ====================================================================== ch12 st3 supply curve, shut-down, break-even
def sd_data(r):
    for _ in range(200):
        avc = [r.randint(18, 30)]
        for _ in range(2):
            avc.append(avc[-1] - r.randint(1, 4))
        for _ in range(3):
            avc.append(avc[-1] + r.randint(1, 4))
        tfc = r.choice([60, 120])
        ac = [a + tfc / (i + 1) for i, a in enumerate(avc)]
        if avc.count(min(avc)) == 1 and sum(1 for x in ac if abs(x - min(ac)) < 1e-9) == 1 and ac.index(min(ac)) < 5:
            return avc, tfc, ac
    raise ValueError('sd')


def sd_tab(r):
    avc, tfc, ac = sd_data(r)
    tvc = [a * (i + 1) for i, a in enumerate(avc)]
    tc = [tfc + v for v in tvc]
    v = r.choice(['sd', 'be'])
    tb = table(['Output', 0, *range(1, 7)], [['TC (₹)', tfc, *tc]])
    if v == 'sd':
        mn = min(avc)
        return {'stem': f'A firm\'s cost schedule is:\n{tb}\nFind the short-run shut-down price.', 'answer': inr(mn),
                'key': f'TFC = {tfc}; AVC = (TC − TFC)/Q: {", ".join(map(str, avc))}; shut-down price = minimum AVC = {mn}.',
                'distractors': alts(inr(mn), [inr(round(min(ac), 2)), inr(avc[0]), inr(min(avc) + 1)], [inr(max(avc))])}
    mn = min(ac)
    return {'stem': f'A firm\'s cost schedule is:\n{tb}\nFind the break-even price (the long-run shut-down price).', 'answer': inr(round(mn, 2)),
            'key': f'AC = TC/Q: {", ".join(d2(x) for x in ac)}; break-even price = minimum AC = {d2(mn)}.',
            'distractors': alts(inr(round(mn, 2)), [inr(min(avc)), inr(round(ac[0], 2)), inr(round(mn + 2, 2))])}


DEC = ['Produce and earn supernormal profit', 'Produce and earn only normal profit', 'Produce at a loss in the short run', 'Shut down']


def decision(r):
    mavc = r.randint(10, 30)
    mac = mavc + r.randint(3, 10)
    kind = r.randrange(4)
    p = [mac + r.randint(1, 6), mac, r.randint(mavc + 1, mac - 1), mavc - r.randint(1, 5)][kind]
    if p <= 0:
        raise ValueError('p')
    return opts_fixed(f'For a perfectly competitive firm, minimum AVC = {inr(mavc)} and minimum AC = {inr(mac)}. If the market price is {inr(p)}, in the short run the firm will',
                      DEC[kind], DEC, ['p > min AC.', 'p = min AC: break-even point.', 'min AVC < p < min AC: variable cost covered, part of fixed cost lost.', 'p < min AVC: shut-down.'][kind], r)


def sd_case(r):
    avc, tfc, ac = sd_data(r)
    tvc = [a * (i + 1) for i, a in enumerate(avc)]
    return {'stem': f'A firm has fixed cost {inr(tfc)} and TVC:\n' + table(['Output', *range(1, 7)], [['TVC (₹)', *tvc]]) + '\n'
            + parts(['Find the shut-down price.', 'Find the break-even price.', 'Which part of the MC curve is the firm\'s short-run supply curve?', f'Will the firm produce in the short run if price = {inr(min(avc) - 1)}? Why?']),
            'answer': pans([inr(min(avc)), inr(round(min(ac), 2)), 'The rising part of MC at and above minimum AVC', 'No: price is below minimum AVC']),
            'key': '1 mark each (4 marks).'}


SD_FACT = [
    ('The short-run shut-down point of a firm is where price equals', 'minimum AVC', ['minimum AC', 'maximum MC', 'AFC'], 'Covers only variable cost.'),
    ('The break-even point is where price equals', 'minimum AC', ['minimum AVC', 'MC at zero output', 'AFC'], 'TR = TC; normal profit.'),
    ('The short-run supply curve of a firm is', 'the rising part of the SMC curve at and above minimum AVC', ['the whole MC curve', 'the AVC curve', 'the AC curve'], 'SR supply.'),
    ('The long-run supply curve of a firm is', 'the rising part of the LRMC curve at and above minimum LRAC', ['the LRAC curve', 'the whole LRMC curve', 'the SR AVC curve'], 'LR supply.'),
    ('Normal profit is', 'the minimum profit needed to keep a firm in the business', ['profit above the normal level', 'zero revenue', 'accounting profit only'], 'Part of cost.'),
    ('At the break-even point, the firm earns', 'only normal profit', ['supernormal profit', 'losses equal to fixed cost', 'no revenue'], 'TR = TC.'),
]
SD_AR = [
    ('A firm may continue production in the short run even if price is below AC.', 'If price is above AVC, the firm covers variable cost and part of fixed cost.', 'a', 'R explains A.'),
    ('At the shut-down point, the loss of the firm equals its total fixed cost.', 'At p = min AVC, TR just covers TVC.', 'a', 'R explains A.'),
    ('The supply curve of a firm is the whole of its MC curve.', 'A firm produces only where MC is rising and p ≥ min AVC.', 'd', 'A is false; R is true.'),
    ('At the break-even point, the firm earns supernormal profit.', 'At the break-even point, TR = TC.', 'd', 'A is false: only normal profit. R is true.'),
]
SD_WR = [
    ('Distinguish between the shut-down point and the break-even point.', 'Shut-down: p = min AVC, SR; firm just covers variable cost. Break-even: p = min AC, TR = TC, only normal profit.', '1½ marks each.'),
    ('Why is the short-run supply curve of a firm the rising part of MC above minimum AVC?', 'Profit-maximising output is where p = MC with MC rising; below min AVC the firm shuts down; so supply follows MC from min AVC upward.', '3 marks.'),
]
SD_LONG = [
    ('Derive the short-run supply curve of a perfectly competitive firm with a diagram. Explain the shut-down and break-even points.',
     'Supply curve = SMC above min AVC; shut-down at p = min AVC; break-even at p = min AC (normal profit); between them, losses but production continues in SR.',
     '2 marks diagram; 2 marks derivation; 2 marks points (6 marks).'),
]

# ====================================================================== ch12 st4 market supply, elasticity of supply
SUPPLY_EFF = ['Supply curve shifts to the right (increase in supply)', 'Supply curve shifts to the left (decrease in supply)',
              'Movement up along the supply curve (quantity supplied rises)', 'Movement down along the supply curve (quantity supplied falls)']
SUP_GOODS = ['cotton cloth', 'bicycles', 'cement', 'mobile phones', 'wheat', 'paper', 'steel utensils']
SUP_EV = []
for _g in SUP_GOODS:
    SUP_EV += [(_g, f'a new technology lowers the cost of producing {_g}', 0), (_g, f'the prices of inputs used to make {_g} rise', 1),
               (_g, f'the government imposes a unit tax on {_g}', 1), (_g, f'the price of {_g} rises', 2), (_g, f'the price of {_g} falls', 3),
               (_g, f'many new firms enter the {_g} industry', 0)]


def sup_event(r):
    g, e, i = cp('supev', r, SUP_EV)
    return opts_fixed(f'Other things remaining the same, what happens in the market for {g} when {e}?', SUPPLY_EFF[i], SUPPLY_EFF, f'{SUPPLY_EFF[i]}.', r)


def es_pct(r):
    for _ in range(300):
        P1 = r.choice([10, 20, 25, 40, 50, 100])
        a = r.choice([10, 20, 25, 50])
        e = r.choice([Fraction(1, 2), Fraction(4, 5), 1, Fraction(6, 5), Fraction(3, 2), 2, Fraction(5, 2)])
        Q1 = r.choice([100, 200, 400, 500, 800, 1000])
        up = r.random() < 0.6
        dP, dQ = Fraction(P1 * a, 100), Fraction(Q1) * e * a / 100
        if dP.denominator != 1 or dQ.denominator != 1 or (not up and dQ >= Q1):
            continue
        P2 = P1 + int(dP) if up else P1 - int(dP)
        Q2 = Q1 + int(dQ) if up else Q1 - int(dQ)
        g = r.choice(SUP_GOODS)
        if r.random() < 0.6:
            ans = f'{num(float(e))} ({cls_e(e)})'
            return {'stem': f'When the price of {g} {"rises" if up else "falls"} from {inr(P1)} to {inr(P2)}, the quantity supplied {"rises" if up else "falls"} from {Q1} to {Q2} units. Calculate the price elasticity of supply.',
                    'answer': ans, 'key': f'es = %ΔQ/%ΔP = ({int(dQ)}/{Q1} × 100)/({int(dP)}/{P1} × 100) = {num(float(e * a))}/{a} = {num(float(e))} → {cls_e(e)}.',
                    'distractors': alts(ans, [f'{num(float(1 / e))} ({cls_e(1 / e)})', f'{num(float(e) + 0.5)} ({cls_e(e + Fraction(1, 2))})', f'{num(float(e))} ({"inelastic" if cls_e(e) != "inelastic" else "elastic"})'])}
        return {'stem': f'The price elasticity of supply of {g} is {num(float(e))}. At {inr(P1)}, {Q1} units are supplied. How much will be supplied at {inr(P2)}?', 'answer': f'{Q2} units',
                'key': f'%ΔP = {a}%; %ΔQ = {num(float(e))} × {a} = {num(float(e * a))}%; ΔQ = {int(dQ)}; new Q = {Q2}.',
                'distractors': alts(f'{Q2} units', [f'{Q1 - int(dQ) if up else Q1 + int(dQ)} units', f'{Q1 + a if up else Q1 - a} units', f'{Q2 + 20} units'])}
    raise ValueError('es')


def es_lin(r):
    for _ in range(100):
        d = r.choice([2, 3, 4, 5, 10])
        c = r.choice([-40, -20, -10, 0, 10, 20, 50])
        p = r.randint(5, 30)
        q = c + d * p
        if q <= 0:
            continue
        e = Fraction(d * p, q)
        if e.denominator > 50:
            continue
        g = r.choice(SUP_GOODS)
        ans = f'{d2(e)} ({cls_e(e)})'
        return {'stem': f'The supply function of {g} is q = {sfmt(c, d)}. Find the price elasticity of supply at p = {inr(p)}.',
                'answer': ans, 'key': f'q = {q}; es = (Δq/Δp) × p/q = {d} × {p}/{q} = {d2(e)}. ' + ('Line through origin → es = 1.' if c == 0 else ('Supply line meets the price axis → es > 1.' if c < 0 else 'Supply line meets the quantity axis → es < 1.')),
                'distractors': alts(ans, [f'{d2(Fraction(q, d * p))} ({cls_e(Fraction(q, d * p))})', f'{d2(Fraction(p, q))} ({cls_e(Fraction(p, q))})', f'{d2(e)} ({"inelastic" if cls_e(e) != "inelastic" else "elastic"})'],
                                    [f'{d} ({cls_e(d)})'])}
    raise ValueError('esl')


def mkt_sup(r):
    n = r.choice([2, 3])
    c0 = r.choice([5, 10])
    prices = [c0 * k for k in range(1, 6)]
    rows = [sorted(r.sample(range(0, 50), 5)) for _ in range(n)]
    k = r.randrange(5)
    tot = sum(rw[k] for rw in rows)
    who = ['Firm A', 'Firm B', 'Firm C'][:n]
    return {'stem': 'Supply schedules of firms in a market:\n' + table(['Price (₹)', *prices], [[w, *rw] for w, rw in zip(who, rows)]) + f'\nFind the market supply at {inr(prices[k])}.',
            'answer': f'{tot} units', 'key': f'Market supply = horizontal sum = {" + ".join(str(rw[k]) for rw in rows)} = {tot}.',
            'distractors': alts(f'{tot} units', [f'{rows[0][k]} units', f'{sum(rw[(k + 1) % 5] for rw in rows)} units', f'{round(tot / n)} units'], [f'{tot + 5} units'])}


def es_case(r):
    d = r.choice([2, 4, 5])
    c = r.choice([-20, 0, 20])
    p1 = r.choice([10, 20])
    p2 = p1 + 10
    q1, q2 = c + d * p1, c + d * p2
    if q1 <= 0:
        raise ValueError('q')
    e = Fraction(q2 - q1, q1) / Fraction(p2 - p1, p1)
    sf = f'q = {d}p' if c == 0 else (f'q = {c} + {d}p' if c > 0 else f'q = −{-c} + {d}p')
    return {'stem': f'The supply function of a good is {sf}.\n'
            + parts([f'Find quantity supplied at {inr(p1)} and {inr(p2)}.', 'Calculate the price elasticity of supply by the percentage method for this price rise.', 'Is supply elastic, inelastic or unitary elastic?',
                     'Where does the supply line meet the axes, and what does that tell you about elasticity?']),
            'answer': pans([f'{q1} and {q2}', d2(e), cls_e(e).capitalize(), 'Passes through the origin → es = 1 at every point' if c == 0 else ('Meets the quantity axis → es < 1' if c > 0 else 'Meets the price axis → es > 1')]),
            'key': '1 mark each (4 marks).'}


ES_FACT = [
    ('Price elasticity of supply is the ratio of', 'percentage change in quantity supplied to percentage change in price', ['change in price to change in quantity', 'quantity to price', 'price to cost'],
     'es = %ΔQ/%ΔP.'),
    ('A straight-line supply curve through the origin has elasticity', 'equal to 1 at every point', ['greater than 1', 'less than 1', 'zero'], 'Unitary.'),
    ('A straight-line supply curve that meets the price axis has elasticity', 'greater than 1', ['less than 1', 'equal to 1', 'zero'], 'Elastic.'),
    ('A straight-line supply curve that meets the quantity axis has elasticity', 'less than 1', ['greater than 1', 'equal to 1', 'infinite'], 'Inelastic.'),
    ('Market supply is obtained by', 'horizontal summation of the supply curves of firms', ['vertical summation of supply curves', 'averaging prices', 'multiplying firms by price'], 'Add quantities.'),
    ('An improvement in technology shifts the supply curve of a firm', 'to the right', ['to the left', 'upward only', 'nowhere'], 'Lower MC.'),
    ('A unit tax on a good shifts its supply curve', 'to the left (upward)', ['to the right', 'nowhere', 'to the origin'], 'Raises MC.'),
]
ES_AR = [
    ('An increase in input prices shifts the supply curve to the left.', 'Higher input prices raise the marginal cost of production.', 'a', 'R explains A.'),
    ('A supply curve through the origin has unitary elasticity at every point.', 'For such a line, the percentage change in quantity always equals the percentage change in price.', 'a', 'R explains A.'),
    ('A rise in the price of a good shifts its supply curve to the right.', 'A change in own price causes a movement along the supply curve.', 'd', 'A is false; R is true.'),
    ('Supply of perishable goods is relatively inelastic in the very short run.', 'Their quantity cannot be adjusted quickly and they cannot be stored.', 'a', 'R explains A.'),
]
ES_WR = [
    ('Explain any three determinants of supply of a good.', 'Price of the good; technology; prices of inputs; number of firms; taxes; goals of the firm.', '1 mark each.'),
    ('Distinguish between a movement along the supply curve and a shift of the supply curve.', 'Movement: due to change in own price. Shift: due to technology, input prices, taxes, number of firms.', '1½ marks each.'),
    ('Explain the geometric method of measuring elasticity of supply for straight-line supply curves.', 'Through origin es = 1; meeting price axis es > 1; meeting quantity axis es < 1.', '1 mark each.'),
]

# ====================================================================== ch13 st1 equilibrium
EQ_GOODS = ['wheat', 'sugar', 'tomatoes', 'cotton', 'pulses', 'potatoes', 'notebooks', 'umbrellas']


def eq_params(r):
    for _ in range(200):
        p, q = r.randint(5, 40), r.choice([50, 60, 80, 100, 120, 150, 200])
        b, d = r.choice([1, 2, 3, 4, 5]), r.choice([1, 2, 3, 4, 5])
        a = q + b * p
        c = q - d * p
        return p, q, a, b, c, d
    raise ValueError('eq')


def sfmt(c, d):
    if c == 0:
        return f'{d}p'
    return f'{c} + {d}p' if c > 0 else f'{d}p − {-c}'


def eq_lin(r):
    p, q, a, b, c, d = eq_params(r)
    g = r.choice(EQ_GOODS)
    ans = f'p* = {inr(p)}, q* = {q} units'
    return {'stem': f'In the market for {g}, demand is qD = {a} − {b}p and supply is qS = {sfmt(c, d)}. Find the equilibrium price and quantity.', 'answer': ans,
            'key': f'{a} − {b}p = {sfmt(c, d)} ⇒ {b + d}p = {a - c} ⇒ p = {p}; q = {a} − {b}×{p} = {q}.',
            'distractors': alts(ans, [f'p* = {inr(p + 2)}, q* = {a - b * (p + 2)} units', f'p* = {inr(round((a + c) / (b + d), 2))}, q* = {q} units', f'p* = {inr(p)}, q* = {a} units'],
                                [f'p* = {inr(p - 1)}, q* = {q + b} units'])}


ED_OPTS = lambda n: [f'Excess demand of {n} units; price will rise', f'Excess supply of {n} units; price will fall', f'Excess demand of {n} units; price will fall',
                     f'Excess supply of {n} units; price will rise']


def excess(r):
    p, q, a, b, c, d = eq_params(r)
    p1 = p + r.choice([-4, -3, -2, 2, 3, 5])
    if p1 <= 0:
        raise ValueError('p')
    qd, qs = a - b * p1, c + d * p1
    if qd < 0 or qs < 0:
        raise ValueError('neg')
    n = abs(qd - qs)
    ops = ED_OPTS(n)
    ans = ops[0] if qd > qs else ops[1]
    g = r.choice(EQ_GOODS)
    return mcq(f'For {g}, qD = {a} − {b}p and qS = {sfmt(c, d)}. What is the situation at a price of {inr(p1)}?', ans, [o for o in ops if o != ans],
               f'qD = {qd}, qS = {qs}; ' + ('qD > qS → excess demand; buyers bid the price up.' if qd > qs else 'qS > qD → excess supply; sellers cut the price.'), r)


def eq_tab(r):
    p0 = r.choice([10, 20, 30])
    step = r.choice([5, 10])
    prices = [p0 + step * i for i in range(6)]
    k = r.randrange(1, 5)
    qe = r.choice([60, 80, 100, 120])
    db, sb = r.randint(3, 10), r.randint(3, 10)
    qd = [qe + db * (k - i) for i in range(6)]
    qs = [qe + sb * (i - k) for i in range(6)]
    if min(qd + qs) < 0:
        raise ValueError('neg')
    return {'stem': 'Market demand and supply schedules are:\n' + table(['Price (₹)', *prices], [['Demand', *qd], ['Supply', *qs]]) + '\nFind the equilibrium price and quantity.',
            'answer': f'{inr(prices[k])}; {qe} units', 'key': f'At {inr(prices[k])}, demand = supply = {qe}.',
            'distractors': [f'{inr(prices[k + 1])}; {qs[k + 1]} units', f'{inr(prices[k - 1])}; {qd[k - 1]} units', f'{inr(prices[k])}; {qe + db} units']}


def eq_case(r):
    p, q, a, b, c, d = eq_params(r)
    p1 = p - r.choice([2, 3, 4])
    if p1 <= 0:
        raise ValueError('p')
    qd, qs = a - b * p1, c + d * p1
    if qs < 0:
        raise ValueError('neg')
    g = r.choice(EQ_GOODS)
    return {'stem': f'In the market for {g}, qD = {a} − {b}p and qS = {sfmt(c, d)}.\n'
            + parts(['Find the equilibrium price.', 'Find the equilibrium quantity.', f'What is the excess demand or supply at {inr(p1)}?', 'How will the market move back to equilibrium?']),
            'answer': pans([inr(p), f'{q} units', f'Excess demand = {qd} − {qs} = {qd - qs} units', 'Buyers compete and bid the price up; qD falls and qS rises until they are equal']),
            'key': '1 mark each (4 marks).'}


EQ_FACT = [
    ('Market equilibrium occurs where', 'market demand equals market supply', ['demand is maximum', 'supply is maximum', 'price is minimum'], 'qD = qS.'),
    ('Excess demand exists at a price', 'below the equilibrium price', ['above the equilibrium price', 'equal to the equilibrium price', 'at which supply is maximum'], 'qD > qS.'),
    ('Excess supply exists at a price', 'above the equilibrium price', ['below the equilibrium price', 'at the equilibrium price', 'of zero'], 'qS > qD.'),
    ('Excess demand tends to make the price', 'rise', ['fall', 'stay the same', 'become zero'], 'Buyers bid up.'),
    ('The idea that the market reaches equilibrium through price changes without any central direction is called the', 'invisible hand', ['visible hand', 'price ceiling', 'rationing'],
     'Adam Smith\'s term.'),
    ('At equilibrium, excess demand is', 'zero', ['positive', 'negative', 'maximum'], 'qD − qS = 0.'),
]
EQ_AR = [
    ('At a price below equilibrium, the price tends to rise.', 'There is excess demand at such a price.', 'a', 'R explains A.'),
    ('At equilibrium, there is no tendency for price to change.', 'Quantity demanded equals quantity supplied.', 'a', 'R explains A.'),
    ('Excess supply makes the price rise.', 'Excess supply means quantity supplied exceeds quantity demanded.', 'd', 'A is false: price falls. R is true.'),
    ('Equilibrium price is determined by the government in a free market.', 'In a free market, price is determined by demand and supply.', 'd', 'A is false; R is true.'),
]
EQ_WR = [
    ('Explain how equilibrium price is determined under perfect competition with a fixed number of firms.', 'At the intersection of market demand and supply; above it excess supply lowers price, below it excess demand raises price.',
     '1 mark meaning; 2 marks adjustment.'),
    ('What is excess demand? How is it removed?', 'qD > qS at a price below equilibrium; buyers bid up the price; qD falls and qS rises until they are equal.', '1 mark meaning; 2 marks process.'),
]
EQ_LONG = [
    ('Explain with a schedule and a diagram how market equilibrium is determined. What happens at prices above and below equilibrium?',
     'Schedule of qD and qS; intersection gives p*, q*; above p*: excess supply, price falls; below p*: excess demand, price rises; invisible hand.',
     '2 marks schedule; 2 marks diagram; 2 marks adjustment (6 marks).'),
]

# ====================================================================== ch13 st2 shifts
SH_OPTS = ['Price rises; quantity rises', 'Price falls; quantity rises', 'Price falls; quantity falls', 'Price rises; quantity falls']
SH_EV = []
for _g in ['cars', 'smartphones', 'fruits', 'restaurant meals']:
    SH_EV += [(_g, 'consumers\' incomes rise (it is a normal good)', 0), (_g, 'consumers\' incomes fall (it is a normal good)', 2)]
for _g, _s in SUBS:
    SH_EV += [(_g, f'the price of {_s} (a substitute) rises', 0), (_g, f'the price of {_s} (a substitute) falls', 2)]
for _g, _c in COMPS:
    SH_EV += [(_g, f'the price of {_c} (a complement) rises', 2), (_g, f'the price of {_c} (a complement) falls', 0)]
for _g in SUP_GOODS:
    SH_EV += [(_g, f'an improved technology reduces the cost of producing {_g}', 1), (_g, f'the prices of inputs for {_g} rise', 3), (_g, f'a unit tax is imposed on {_g}', 3)]
SH_EV += [('wheat', 'a severe drought damages the crop', 3), ('rice', 'a bumper harvest occurs', 1), ('coarse cereals', 'consumers\' incomes rise (it is an inferior good)', 2)]


def shift_ev(r):
    g, e, i = cp('shev', r, SH_EV)
    return opts_fixed(f'Other things remaining the same, what happens to the equilibrium price and quantity of {g} when {e}?', SH_OPTS[i], SH_OPTS,
                      ['Demand increases.', 'Supply increases.', 'Demand decreases.' if i == 2 else 'Supply decreases.', 'Supply decreases.'][i] + f' {SH_OPTS[i]}.', r)


SIM = [
    ('Demand and supply both increase by the same amount. Equilibrium', 'quantity rises; price is unchanged', ['price rises; quantity unchanged', 'both price and quantity fall', 'price falls; quantity unchanged'],
     'Equal rightward shifts.'),
    ('Demand increases and supply decreases by the same amount. Equilibrium', 'price rises; quantity is unchanged', ['quantity rises; price unchanged', 'price falls; quantity rises', 'both fall'],
     'Shifts offset on quantity.'),
    ('Demand decreases and supply increases by the same amount. Equilibrium', 'price falls; quantity is unchanged', ['price rises; quantity unchanged', 'quantity falls; price unchanged', 'both rise'],
     'Shifts offset on quantity.'),
    ('Demand increases more than supply increases. Equilibrium', 'price rises and quantity rises', ['price falls and quantity rises', 'price unchanged and quantity falls', 'price falls and quantity falls'],
     'Demand shift dominates.'),
    ('Supply increases more than demand increases. Equilibrium', 'price falls and quantity rises', ['price rises and quantity rises', 'price falls and quantity falls', 'price and quantity unchanged'],
     'Supply shift dominates.'),
    ('Demand and supply both decrease by the same amount. Equilibrium', 'quantity falls; price is unchanged', ['price falls; quantity unchanged', 'both rise', 'price rises; quantity rises'],
     'Equal leftward shifts.'),
]


def shift_num(r):
    p, q, a, b, c, d = eq_params(r)
    dem = r.random() < 0.5
    k = (b + d) * r.randint(1, 4) * r.choice([1, -1])
    g = r.choice(EQ_GOODS)
    if dem:
        a2 = a + k
        p2 = (a2 - c) // (b + d)
        q2 = a2 - b * p2
        txt = f'Demand changes to qD = {a2} − {b}p'
    else:
        c2 = c + k
        p2 = (a - c2) // (b + d)
        q2 = a - b * p2
        txt = f'Supply changes to qS = {sfmt(c2, d)}'
    if p2 <= 0 or q2 <= 0:
        raise ValueError('neg')
    ans = f'p = {inr(p2)}, q = {q2} units'
    return {'stem': f'For {g}, qD = {a} − {b}p and qS = {sfmt(c, d)}. {txt}. Find the new equilibrium price and quantity, and compare them with the old equilibrium.',
            'answer': ans + f' (old: {inr(p)}, {q} units)', 'key': f'Old: p = {p}, q = {q}. New: set qD = qS ⇒ p = {p2}, q = {q2}. 2 marks each equilibrium; 1 mark comparison.',
            'distractors': [f'p = {inr(p)}, q = {q2} units (old: {inr(p)}, {q} units)', f'p = {inr(p2)}, q = {q} units (old: {inr(p)}, {q} units)',
                            f'p = {inr(2 * p - p2 if 2 * p - p2 > 0 else p + 1)}, q = {q2} units (old: {inr(p)}, {q} units)']}


def shift_case(r):
    g, e, i = r.choice(SH_EV)
    return {'stem': f'Suppose {e} in the market for {g}.\n'
            + parts(['Which curve shifts, and in which direction?', 'What is the effect on equilibrium price?', 'What is the effect on equilibrium quantity?', 'At the old price, is there excess demand or excess supply after the shift?']),
            'answer': pans([['Demand curve shifts right', 'Supply curve shifts right', 'Demand curve shifts left', 'Supply curve shifts left'][i],
                            'Rises' if i in (0, 3) else 'Falls', 'Rises' if i in (0, 1) else 'Falls', 'Excess demand' if i in (0, 3) else 'Excess supply']),
            'key': '1 mark each (4 marks).'}


SH_AR = [
    ('An increase in demand, with supply unchanged, raises equilibrium price and quantity.', 'At the old price, there is excess demand after the increase.', 'a', 'R explains A.'),
    ('An improvement in technology lowers the equilibrium price of a good.', 'It shifts the supply curve to the right.', 'a', 'R explains A.'),
    ('If demand and supply increase equally, equilibrium price rises.', 'Equal rightward shifts raise quantity.', 'd', 'A is false: price is unchanged. R is true.'),
    ('A rise in the price of a substitute lowers the equilibrium price of a good.', 'It shifts the demand curve of the good to the right.', 'd', 'A is false: price rises. R is true.'),
]
SH_WR = [
    ('Explain with a diagram the effect of an increase in supply on equilibrium price and quantity.', 'Supply shifts right; at old price excess supply; price falls; quantity rises.', '1 mark diagram; 2 marks explanation.'),
    ('Explain the effect on equilibrium price and quantity when both demand and supply increase by the same amount.', 'Both shift right equally; quantity rises; price unchanged.', '1 mark diagram; 2 marks explanation.'),
]
SH_LONG = [
    ('Explain with diagrams the effect on equilibrium price and quantity when (i) demand increases, (ii) supply decreases, (iii) demand and supply both increase in the same proportion.',
     '(i) p and q rise; (ii) p rises, q falls; (iii) q rises, p unchanged; each with excess demand/supply reasoning.', '2 marks each (6 marks).'),
]

# ====================================================================== ch13 st3 free entry
def free_entry(r):
    for _ in range(200):
        p0 = r.randint(5, 30)
        q0 = r.choice([5, 10, 20, 25, 50])
        n = r.randint(10, 60)
        Q = n * q0
        b = r.choice([1, 2, 5, 10])
        a = Q + b * p0
        g = r.choice(EQ_GOODS)
        if r.random() < 0.6:
            ans = f'p = {inr(p0)}, Q = {Q} units, {n} firms'
            return {'stem': f'In a perfectly competitive market for {g} with free entry and exit, every firm has a minimum long-run AC of {inr(p0)} at an output of {q0} units. '
                            f'Market demand is qD = {a} − {b}p. Find the long-run equilibrium price, market quantity and number of firms.',
                    'answer': ans, 'key': f'p = min AC = {p0}; Q = {a} − {b}×{p0} = {Q}; n = Q/q₀ = {Q}/{q0} = {n}.',
                    'distractors': alts(ans, [f'p = {inr(p0)}, Q = {Q} units, {Q} firms', f'p = {inr(p0 + 1)}, Q = {Q - b} units, {n} firms', f'p = {inr(p0)}, Q = {a} units, {a // q0} firms'])}
        k = r.randint(2, 10) * q0
        a2 = a + k
        n2 = (Q + k) // q0
        ans = f'Price stays at {inr(p0)}; firms rise from {n} to {n2}'
        return {'stem': f'In a market for {g} with free entry and exit, each firm\'s minimum AC is {inr(p0)} at {q0} units. Demand rises from qD = {a} − {b}p to qD = {a2} − {b}p. '
                        'What happens to the equilibrium price and the number of firms?',
                'answer': ans, 'key': f'p stays at min AC = {p0}; Q rises from {Q} to {Q + k}; n = Q/q₀: {n} → {n2}.',
                'distractors': alts(ans, [f'Price rises above {inr(p0)}; firms stay at {n}', f'Price stays at {inr(p0)}; firms stay at {n}', f'Price stays at {inr(p0)}; firms rise from {n} to {n2 + 5}'])}
    raise ValueError('fe')


def fe_case(r):
    p0 = r.randint(5, 20)
    q0 = r.choice([10, 20, 25])
    n = r.randint(10, 40)
    b = r.choice([2, 5, 10])
    Q = n * q0
    a = Q + b * p0
    g = r.choice(EQ_GOODS)
    return {'stem': f'In the market for {g}, firms are identical, entry and exit are free, and each firm\'s minimum AC is {inr(p0)} at {q0} units. Market demand is qD = {a} − {b}p.\n'
            + parts(['What will be the long-run equilibrium price? Why?', 'Find the market quantity.', 'Find the number of firms.', 'What profit does each firm earn in the long run?']),
            'answer': pans([f'{inr(p0)}: entry/exit push price to min AC', f'{Q} units', f'{n} firms', 'Only normal profit (zero supernormal profit)']), 'key': '1 mark each (4 marks).'}


FE_FACT = [
    ('With free entry and exit, the long-run equilibrium price equals', 'minimum average cost', ['minimum AVC', 'maximum MC', 'average revenue at zero output'], 'p = min AC.'),
    ('In long-run equilibrium under free entry, each firm earns', 'only normal profit', ['supernormal profit', 'losses', 'zero revenue'], 'Entry removes extra profit.'),
    ('If firms earn supernormal profit, in the long run', 'new firms enter and price falls', ['firms leave and price rises', 'nothing changes', 'price rises'], 'Entry.'),
    ('If firms incur losses, in the long run', 'some firms exit and price rises', ['new firms enter', 'price falls further', 'output rises'], 'Exit.'),
    ('With free entry and identical firms, an increase in demand in the long run changes', 'the number of firms and the quantity, but not the price', ['only the price', 'the price and the number of firms equally', 'nothing'],
     'Price fixed at min AC.'),
]
FE_AR = [
    ('Under free entry and exit, firms earn only normal profit in the long run.', 'Supernormal profit attracts new firms, which lowers the price to minimum AC.', 'a', 'R explains A.'),
    ('With free entry, a rise in demand raises the long-run equilibrium price.', 'New firms enter until price returns to minimum AC.', 'd', 'A is false; R is true.'),
    ('Losses lead some firms to leave the industry in the long run.', 'Exit reduces supply and raises the price.', 'a', 'R explains A.'),
]
FE_WR = [
    ('Explain why the price equals minimum AC in long-run equilibrium with free entry and exit.', 'If p > min AC, supernormal profit attracts entry, supply rises, price falls; if p < min AC, losses cause exit, price rises; so p = min AC.',
     '3 marks.'),
    ('Explain the effect of an increase in demand on equilibrium price, quantity and number of firms when entry and exit are free.', 'Price unchanged at min AC; quantity rises; number of firms rises (n = Q/q₀).', '1 mark each.'),
]
FE_LONG = [
    ('Explain with a diagram how equilibrium is reached in a perfectly competitive market with free entry and exit. Show the effect of an increase in demand.',
     'Supply curve horizontal at min AC; equilibrium where demand meets it; normal profit; increase in demand raises quantity and number of firms, price unchanged.',
     '2 marks diagram; 2 marks equilibrium; 2 marks demand change (6 marks).'),
]

# ====================================================================== ch13 st4 price ceiling and floor
def ceiling(r):
    p, q, a, b, c, d = eq_params(r)
    g = r.choice(['wheat', 'sugar', 'kerosene', 'rice', 'cooking gas'])
    pc = p - r.randint(2, 5)
    qd, qs = a - b * pc, c + d * pc
    if pc <= 0 or qs < 0:
        raise ValueError('neg')
    ans = f'Shortage (excess demand) of {qd - qs} units'
    return {'stem': f'For {g}, qD = {a} − {b}p and qS = {sfmt(c, d)}. The government fixes a maximum price of {inr(pc)}. Find the effect.', 'answer': ans,
            'key': f'Equilibrium p = {p}; ceiling {pc} < {p}; qD = {qd}, qS = {qs}; shortage = {qd - qs}.',
            'distractors': alts(ans, [f'Surplus (excess supply) of {qd - qs} units', f'Shortage (excess demand) of {abs(q - qs)} units', 'No effect: the ceiling is not binding'], [f'Shortage (excess demand) of {qd} units'])}


def floor(r):
    p, q, a, b, c, d = eq_params(r)
    g = r.choice(['wheat', 'rice', 'cotton', 'pulses', 'sugarcane'])
    pf = p + r.randint(2, 5)
    qd, qs = a - b * pf, c + d * pf
    if qd < 0:
        raise ValueError('neg')
    ans = f'Surplus (excess supply) of {qs - qd} units'
    return {'stem': f'For {g}, qD = {a} − {b}p and qS = {sfmt(c, d)}. The government fixes a minimum support price of {inr(pf)}. Find the effect.', 'answer': ans,
            'key': f'Equilibrium p = {p}; floor {pf} > {p}; qS = {qs}, qD = {qd}; surplus = {qs - qd} (the government may have to buy it).',
            'distractors': alts(ans, [f'Shortage (excess demand) of {qs - qd} units', f'Surplus (excess supply) of {abs(qs - q)} units', 'No effect: the floor is not binding'], [f'Surplus (excess supply) of {qs} units'])}


def bind(r):
    p, q, a, b, c, d = eq_params(r)
    kind = r.choice(['ceil_b', 'ceil_n', 'floor_b', 'floor_n'])
    k = r.randint(2, 6)
    v = {'ceil_b': p - k, 'ceil_n': p + k, 'floor_b': p + k, 'floor_n': p - k}[kind]
    if v <= 0:
        raise ValueError('v')
    word = 'maximum (ceiling)' if kind.startswith('ceil') else 'minimum (floor)'
    opts = ['It creates a shortage', 'It creates a surplus', 'It has no effect on the market', 'It shifts the demand curve']
    ans = {'ceil_b': opts[0], 'floor_b': opts[1], 'ceil_n': opts[2], 'floor_n': opts[2]}[kind]
    return opts_fixed(f'For a good, qD = {a} − {b}p and qS = {sfmt(c, d)}. The government sets a {word} price of {inr(v)}. Which statement is correct?', ans, opts,
                      f'Equilibrium p = {p}. ' + {'ceil_b': 'Ceiling below equilibrium → shortage.', 'ceil_n': 'Ceiling above equilibrium is not binding.', 'floor_b': 'Floor above equilibrium → surplus.',
                                                  'floor_n': 'Floor below equilibrium is not binding.'}[kind], r)


def cf_case(r):
    p, q, a, b, c, d = eq_params(r)
    pc = p - r.randint(2, 4)
    qd, qs = a - b * pc, c + d * pc
    if pc <= 0 or qs < 0:
        raise ValueError('neg')
    return {'stem': f'To help poor consumers, the government fixes the price of wheat at {inr(pc)}. Demand is qD = {a} − {b}p and supply qS = {sfmt(c, d)}.\n'
            + parts(['Find the equilibrium price.', 'Is this a price ceiling or a price floor?', f'Find the shortage or surplus at {inr(pc)}.', 'State two consequences of this policy.']),
            'answer': pans([inr(p), 'Price ceiling (below equilibrium)', f'Shortage of {qd - qs} units', 'Rationing through fair-price shops and queues; black market (some buyers pay more illegally)']),
            'key': '1 mark each (4 marks).'}


CF_FACT = [
    ('A price ceiling is', 'a legal maximum price set below the equilibrium price', ['a legal minimum price above equilibrium', 'the equilibrium price', 'a tax on a good'], 'Maximum price.'),
    ('A price floor is', 'a legal minimum price set above the equilibrium price', ['a legal maximum price below equilibrium', 'the cost of production', 'a subsidy'], 'Minimum price.'),
    ('A price ceiling below equilibrium leads to', 'excess demand (shortage)', ['excess supply', 'no change', 'a fall in demand'], 'qD > qS.'),
    ('A price floor above equilibrium leads to', 'excess supply (surplus)', ['excess demand', 'no change', 'a black market for buyers'], 'qS > qD.'),
    ('Minimum support price for wheat is an example of', 'a price floor', ['a price ceiling', 'a tax', 'equilibrium price'], 'Floor to help farmers.'),
    ('Ration shops selling grain at fixed low prices are linked to', 'a price ceiling', ['a price floor', 'free entry', 'a unit tax'], 'Ceiling with rationing.'),
    ('A minimum wage set above the equilibrium wage can lead to', 'unemployment (excess supply of labour)', ['excess demand for labour', 'a fall in wages', 'no change'], 'Floor in the labour market.'),
    ('A major consequence of a price ceiling is', 'black marketing', ['surplus stocks with the government', 'unemployment', 'higher prices for all buyers in fair-price shops'], 'Illegal sale at higher price.'),
]
CF_AR = [
    ('A price ceiling below the equilibrium price causes shortages.', 'At the lower price, quantity demanded exceeds quantity supplied.', 'a', 'R explains A.'),
    ('A price floor is fixed below the equilibrium price to help producers.', 'A floor raises the price received by producers.', 'd', 'A is false: it is fixed above equilibrium. R is true.'),
    ('Black markets may develop under a price ceiling.', 'Some buyers are willing to pay more than the controlled price.', 'a', 'R explains A.'),
    ('Under a price floor, the government may have to buy the surplus.', 'At the floor price, quantity supplied exceeds quantity demanded.', 'a', 'R explains A.'),
    ('A price ceiling set above the equilibrium price creates a shortage.', 'A ceiling is a maximum legal price.', 'd', 'A is false: it is not binding. R is true.'),
]
CF_WR = [
    ('Explain with a diagram the effects of a price ceiling.', 'Set below equilibrium; excess demand (shortage); rationing and fair-price shops; black market.', '1 mark diagram; 2 marks effects.'),
    ('Explain with a diagram the effects of a price floor (e.g. minimum support price).', 'Set above equilibrium; excess supply (surplus); government buys surplus and stores it, adding to costs.', '1 mark diagram; 2 marks effects.'),
]
CF_LONG = [
    ('Explain price ceiling and price floor with diagrams. Give one example and two consequences of each.',
     'Ceiling below equilibrium → shortage, rationing, black market (e.g. wheat/kerosene through ration shops). Floor above equilibrium → surplus, government procurement and storage (e.g. MSP, minimum wages).',
     '3 marks each (6 marks).'),
]

# ====================================================================== 6-mark numerical long answers
def ppf_long(r):
    x, y, xs, ys, mocs = ppf_sched(r)
    i = r.randrange(1, len(xs) - 1)
    d = xs[1] - xs[0]
    return {'stem': f'The production possibilities of an economy are:\n{ppf_tab(x, y, xs, ys)}\n'
            + parts(['Calculate the marginal opportunity cost at each step.', 'What shape does the PPF have, and why?', f'What does the combination ({xs[i]} {x}, {ys[i] - d} {y}) show?',
                     'Show the effect of a large-scale destruction of machines on the PPF.']),
            'answer': pans([', '.join(num(m) for m in mocs) + f' units of {y} per unit of {x}', 'Concave to the origin: MOC rises because resources are not equally efficient in both goods',
                            f'It is inside the PPF (maximum {y} at {xs[i]} {x} is {ys[i]}): resources are under-utilised', 'The PPF shifts inward (to the left)']),
            'key': '2 marks (i); 1½ marks (ii); 1½ marks (iii); 1 mark (iv) (6 marks).'}


def elas_long(r):
    for _ in range(200):
        b = r.choice([2, 4, 5, 10])
        a = r.choice([200, 240, 300, 400, 500, 600])
        p1 = r.choice([5, 10, 15, 20])
        p2 = p1 + r.choice([5, 10])
        q1, q2 = a - b * p1, a - b * p2
        if q2 <= 0:
            continue
        e = Fraction(q1 - q2, q1) / Fraction(p2 - p1, p1)
        ep = Fraction(b * p1, q1)
        g = r.choice(['notebooks', 'kites', 'apples', 'candles', 'pens'])
        te = 'falls' if p2 * q2 < p1 * q1 else ('is unchanged' if p2 * q2 == p1 * q1 else 'rises')
        return {'stem': f'The demand for {g} is q = {a} − {b}p.\n'
                + parts([f'Find the quantity demanded at {inr(p1)} and {inr(p2)}.', f'Using the percentage method, find |eD| when price rises from {inr(p1)} to {inr(p2)}.',
                         f'Find the point elasticity at {inr(p1)} using |e| = b × p/q.', f'Find total expenditure at both prices and state how it changes.',
                         f'At what price is the demand unitary elastic?']),
                'answer': pans([f'{q1} and {q2} units', f'({q1 - q2}/{q1}) ÷ ({p2 - p1}/{p1}) = {d2(e)} ({cls_e(e)})', f'{b} × {p1}/{q1} = {d2(ep)}',
                                f'{inr(p1 * q1)} and {inr(p2 * q2)}; expenditure {te}', f'p = {a}/{2 * b} = {d2(Fraction(a, 2 * b))} (mid-point of the demand line)']),
                'key': '1 mark (i); 1½ marks (ii); 1 mark (iii); 1½ marks (iv); 1 mark (v) (6 marks).'}
    raise ValueError('el')


def cost_long(r):
    tfc, mcs, tvc = cost_sched(r, 6)
    avc = [v / (i + 1) for i, v in enumerate(tvc)]
    ac = [(tfc + v) / (i + 1) for i, v in enumerate(tvc)]
    k = min(range(6), key=lambda i: avc[i])
    if sum(1 for x in avc if abs(x - avc[k]) < 1e-9) > 1:
        raise ValueError('tie')
    rows = [[q, tfc + tvc[q - 1], d2(tfc / q), d2(avc[q - 1]), d2(ac[q - 1]), mcs[q - 1]] for q in range(1, 7)]
    return {'stem': f'A firm has TFC = {inr(tfc)} and the following TVC:\n' + table(['Output', *range(1, 7)], [['TVC (₹)', *tvc]])
            + '\n(i) Find TC, AFC, AVC, AC and MC at each output. (ii) At which output is AVC minimum? (iii) Show that MC cuts AVC near its minimum.',
            'answer': table(['Q', 'TC', 'AFC', 'AVC', 'AC', 'MC'], rows) + f'\nAVC is minimum ({d2(avc[k])}) at {k + 1} units; MC is below AVC while AVC falls and above it after the minimum.',
            'key': '4 marks table (TC, AFC, AVC/AC, MC: 1 mark each); 1 mark minimum AVC; 1 mark MC–AVC relation (6 marks).'}


def pm_long(r):
    tfc, mcs, tvc, qi, p = pm_data(r)
    tc = [tfc + v for v in tvc]
    q = qi + 1
    prof = p * q - tc[qi]
    avc = [v / (i + 1) for i, v in enumerate(tvc)]
    return {'stem': f'A perfectly competitive firm sells at {inr(p)}. Its cost schedule is:\n' + table(['Output', 0, *range(1, 8)], [['TC (₹)', tfc, *tc]]) + '\n'
            + parts(['Find TFC and the MC at each output.', 'Find the profit-maximising output, stating both conditions.', 'Calculate the profit or loss at that output.',
                     'Find the minimum AVC. Will the firm continue to produce in the short run?']),
            'answer': pans([f'TFC = {inr(tfc)}; MC: {", ".join(map(str, mcs))}', f'{q} units (p = MC = {p}, MC rising)', (f'Profit = {inr(prof)}' if prof >= 0 else f'Loss = {inr(-prof)}') + f' (TR {p * q} − TC {tc[qi]})',
                            f'Minimum AVC = {d2(min(avc))}; p = {p} ≥ min AVC, so it continues']),
            'key': '1½ marks each part (6 marks).'}


def eqm_long(r):
    p, q, a, b, c, d = eq_params(r)
    pc = p - r.randint(2, 4)
    k = (b + d) * r.randint(1, 3)
    if pc <= 0 or c + d * pc < 0:
        raise ValueError('neg')
    qd, qs = a - b * pc, c + d * pc
    p2 = p + k // (b + d)
    q2 = a + k - b * p2
    g = r.choice(EQ_GOODS)
    return {'stem': f'In the market for {g}, qD = {a} − {b}p and qS = {sfmt(c, d)}.\n'
            + parts(['Find the equilibrium price and quantity.', f'The government fixes a maximum price of {inr(pc)}. Find the resulting shortage and state two consequences.',
                     f'Without price control, demand rises to qD = {a + k} − {b}p. Find the new equilibrium.']),
            'answer': pans([f'p = {inr(p)}, q = {q} units', f'qD = {qd}, qS = {qs}: shortage of {qd - qs} units; rationing/queues and black marketing', f'p = {inr(p2)}, q = {q2} units (both rise)']),
            'key': '2 marks each part (6 marks).'}


# ====================================================================== FAMILIES
FAMILIES = {
    S + '09-st1': [M('C1', 'D1', CP_FACT[:4]), M('C1', 'D2', CP_FACT[4:]), G('C2', 'D2', 'mcq', cp_classify), G('C2', 'D3', 'mcq', cp_classify), AR('C2', 'D2', CP_AR),
                   G('C3', 'D2', 'mcq', cp_classify), G('C3', 'D3', 'case', cp_case, **CASE), G('C3', 'D4', 'case', cp_case, **CASE),
                   W('C4', 'D3', 'explain', CP_WR, **Q3), W('C4', 'D4', 'long', CP_LONG, marks=6), W('C2', 'D1', 'short', [(f'Name the central problem: "{x}"', c, 'Correct problem: 1 mark.') for x, c in CP_EX[:6]], marks=1)],
    S + '09-st2': [G('C4', 'D4', 'long', ppf_long, marks=6), M('C1', 'D1', PPF_FACT[:5]), M('C1', 'D2', PPF_FACT[5:]), G('C2', 'D2', 'mcq', classify(PPF_EV, 'What happens to the PPF or the economy\'s position when: {x}?', '{x}: {c}.')),
                   AR('C2', 'D3', PPF_AR), G('C2', 'D3', 'numerical', oc_choice, marks=1), G('C3', 'D1', 'numerical', mrt_num, marks=1), G('C3', 'D2', 'numerical', ppf_moc, marks=1),
                   G('C3', 'D3', 'mcq', ppf_point), G('C3', 'D3', 'numerical', ppf_full, **Q3), G('C3', 'D4', 'case', ppf_case, **CASE), G('C4', 'D3', 'numerical', ppf_moc, **Q3),
                   W('C4', 'D3', 'explain', PPF_WR, **Q3), W('C4', 'D5', 'long', PPF_LONG, marks=6), G('C4', 'D4', 'case', ppf_case, **CASE)],
    S + '09-st3': [M('C1', 'D1', ECO_FACT[:3]), M('C1', 'D2', ECO_FACT[3:]), G('C2', 'D2', 'mcq', eco_cls), G('C2', 'D3', 'mcq', eco_cls), AR('C2', 'D2', ECO_AR),
                   G('C3', 'D2', 'mcq', eco_cls), G('C3', 'D3', 'case', eco_case, **CASE), G('C3', 'D4', 'case', eco_case, **CASE), W('C4', 'D3', 'explain', ECO_WR, **Q3),
                   W('C4', 'D4', 'long', ECO_LONG, marks=6)],
    S + '09-st4': [M('C1', 'D1', PNF[:3]), M('C1', 'D2', PNF[3:]), G('C2', 'D2', 'mcq', pick_example(PN, 'Normative statement', 'Which of the following is a normative statement?')),
                   G('C2', 'D3', 'mcq', pick_example(PN, 'Positive statement', 'Which of the following is a positive statement?')), AR('C2', 'D2', PN_AR),
                   G('C3', 'D2', 'mcq', pick_example(MM, 'Macroeconomics', 'Which of the following is studied in macroeconomics?')),
                   G('C3', 'D1', 'mcq', pick_example(MM, 'Microeconomics', 'Which of the following is studied in microeconomics?')),
                   G('C3', 'D3', 'case', pn_case, **CASE), G('C3', 'D4', 'case', mm_case, **CASE), W('C4', 'D3', 'explain', PN_WR, **Q3)],
    S + '10-st1': [M('C1', 'D1', UT_FACT[:5]), M('C1', 'D2', UT_FACT[5:]), G('C2', 'D2', 'numerical', tu_to_mu, marks=1), G('C2', 'D3', 'numerical', tu_max, marks=1), AR('C2', 'D3', UT_AR),
                   G('C3', 'D1', 'numerical', mu_to_tu, marks=1), G('C3', 'D2', 'numerical', eq_single, **Q3), G('C3', 'D3', 'numerical', eq_two, **Q4), G('C3', 'D4', 'case', ut_case, **CASE),
                   W('C4', 'D3', 'explain', UT_WR, **Q3), G('C4', 'D4', 'numerical', eq_two, **Q4), W('C4', 'D5', 'long', UT_LONG, marks=6)],
    S + '10-st2': [M('C1', 'D1', BL_FACT[:4]), M('C1', 'D2', BL_FACT[4:]), G('C2', 'D2', 'mcq', classify(BL_EV, 'How does the budget line change when: {x}?', '{x}: {c}.')), AR('C2', 'D3', BL_AR),
                   G('C3', 'D1', 'numerical', bl_basic, marks=1), G('C3', 'D2', 'mcq', bl_afford), G('C3', 'D3', 'numerical', bl_count, marks=1), G('C3', 'D3', 'numerical', bl_from_int, **Q3),
                   G('C3', 'D4', 'case', bl_case, **CASE), G('C4', 'D3', 'numerical', bl_new, **Q3), W('C4', 'D3', 'explain', BL_WR, **Q3), W('C4', 'D4', 'long', BL_LONG, marks=6),
                   G('C2', 'D2', 'numerical', bl_basic, marks=1)],
    S + '10-st3': [M('C1', 'D1', IC_FACT[:4]), M('C1', 'D2', IC_FACT[4:]), G('C2', 'D2', 'mcq', mono), AR('C2', 'D3', IC_AR), G('C2', 'D3', 'mcq', opt_dir),
                   G('C3', 'D2', 'numerical', mrs_tab, marks=1), G('C3', 'D3', 'mcq', opt_dir), G('C3', 'D4', 'case', ic_case, **CASE), W('C4', 'D3', 'explain', IC_WR, **Q3),
                   W('C4', 'D4', 'long', IC_LONG, marks=6), G('C3', 'D1', 'mcq', mono)],
    S + '10-st4': [G('C4', 'D4', 'long', elas_long, marks=6), M('C1', 'D1', DEM_FACT[:5]), M('C1', 'D2', DEM_FACT[5:]), G('C2', 'D2', 'mcq', dem_event), G('C2', 'D3', 'mcq', dem_event), AR('C2', 'D3', DEM_AR),
                   G('C3', 'D2', 'numerical', elas_pct, marks=3, kinds=('q3',)), G('C3', 'D3', 'numerical', elas_findq, **Q3), G('C3', 'D3', 'numerical', elas_lin, marks=1),
                   G('C3', 'D2', 'numerical', elas_geo, marks=1), G('C3', 'D3', 'mcq', te_method), G('C3', 'D4', 'case', dem_case, **CASE), W('C4', 'D3', 'explain', DEM_WR, **Q3),
                   G('C4', 'D4', 'numerical', elas_lin, **Q4), W('C4', 'D5', 'long', DEM_LONG, marks=6), G('C3', 'D1', 'mcq', dem_event)],
    S + '10-st5': [M('C1', 'D1', REL_FACT[:3]), M('C1', 'D2', REL_FACT[3:]), G('C2', 'D2', 'mcq', pick_example(REL, 'Complements', 'Which pair of goods are complements?')),
                   G('C2', 'D3', 'mcq', pick_example(REL, 'Substitutes', 'Which pair of goods are substitutes?')), AR('C2', 'D2', REL_AR), G('C3', 'D2', 'mcq', inc_cls), G('C3', 'D3', 'mcq', cross_cls),
                   G('C3', 'D1', 'numerical', mkt_n, marks=1), G('C3', 'D2', 'numerical', mkt_tab, marks=1), G('C3', 'D4', 'case', rel_case, **CASE), G('C4', 'D3', 'numerical', mkt_lin, **Q3),
                   W('C4', 'D3', 'explain', REL_WR, **Q3), G('C4', 'D4', 'numerical', mkt_lin, **Q4)],
    S + '11-st1': [M('C1', 'D1', PF_FACT[:3]), M('C1', 'D2', PF_FACT[3:]), G('C2', 'D2', 'mcq', pick_example(FIXV, 'Fixed factor', 'Which of these is a fixed factor in the short run?')),
                   G('C2', 'D3', 'mcq', pick_example(FIXV, 'Variable factor', 'Which of these is a variable factor in the short run?')), AR('C2', 'D2', PF_AR),
                   G('C3', 'D2', 'numerical', pf_val, marks=1), G('C3', 'D3', 'numerical', pf_val, **Q3), G('C3', 'D4', 'case', pf_case, **CASE), W('C4', 'D3', 'explain', PF_WR, **Q3),
                   G('C3', 'D1', 'numerical', pf_val, marks=1)],
    S + '11-st2': [M('C1', 'D1', TPF[:4]), M('C1', 'D2', TPF[4:]), G('C2', 'D2', 'numerical', tp_mp, marks=1), G('C2', 'D3', 'mcq', lvp_phase), AR('C2', 'D3', TP_AR),
                   G('C3', 'D1', 'numerical', tp_mp, marks=1), G('C3', 'D2', 'numerical', mp_to_tp, marks=1), G('C3', 'D3', 'numerical', lvp_full, **Q4), G('C3', 'D4', 'case', tp_case, **CASE),
                   W('C4', 'D3', 'explain', TP_WR, **Q3), W('C4', 'D4', 'long', TP_LONG, marks=6), G('C4', 'D4', 'numerical', lvp_full, **Q4)],
    S + '11-st3': [M('C1', 'D1', RTS_FACT[:3]), M('C1', 'D2', RTS_FACT[3:]), G('C2', 'D2', 'mcq', rts_cd), G('C2', 'D3', 'mcq', rts_num), AR('C2', 'D2', RTS_AR), G('C3', 'D2', 'mcq', rts_num),
                   G('C3', 'D1', 'mcq', rts_cd), G('C3', 'D4', 'case', rts_case, **CASE), W('C4', 'D3', 'explain', RTS_WR, **Q3)],
    S + '11-st4': [G('C4', 'D4', 'long', cost_long, marks=6), M('C1', 'D1', COST_FACT[:5]), M('C1', 'D2', COST_FACT[5:]), G('C2', 'D2', 'mcq', pick_example(COST_ITEMS, 'Fixed cost', 'Which of these is a fixed cost?')),
                   G('C2', 'D3', 'numerical', afc_q, marks=1), AR('C2', 'D3', COST_AR), G('C3', 'D1', 'numerical', cost_q, marks=1), G('C3', 'D2', 'numerical', cost_q, marks=1),
                   G('C3', 'D3', 'numerical', avc_min, **Q3), G('C3', 'D3', 'numerical', cost_fill, **Q4), G('C3', 'D4', 'case', cost_case, **CASE), W('C4', 'D3', 'explain', COST_WR, **Q3),
                   W('C4', 'D4', 'long', COST_LONG, marks=6), G('C4', 'D4', 'numerical', cost_fill, **Q4)],
    S + '12-st1': [M('C1', 'D1', PC_FACT[:3]), M('C1', 'D2', PC_FACT[3:]), G('C2', 'D2', 'numerical', rev_tab, marks=1), AR('C2', 'D3', PC_AR), G('C3', 'D1', 'numerical', rev_tab, marks=1),
                   G('C3', 'D3', 'case', rev_case, **CASE), W('C4', 'D3', 'explain', PC_WR, **Q3), W('C4', 'D4', 'long', PC_LONG, marks=6), G('C2', 'D3', 'numerical', rev_tab, marks=1)],
    S + '12-st2': [G('C4', 'D4', 'long', pm_long, marks=6), M('C1', 'D1', PM_FACT[:3]), M('C1', 'D2', PM_FACT[3:]), G('C2', 'D2', 'mcq', pm_rule), G('C2', 'D3', 'mcq', pm_rule), AR('C2', 'D3', PM_AR),
                   G('C3', 'D2', 'numerical', profit_area, marks=1), G('C3', 'D3', 'numerical', pm_tab, **Q4), G('C3', 'D4', 'case', pm_case, **CASE), G('C3', 'D1', 'numerical', profit_area, marks=1),
                   W('C4', 'D3', 'explain', PM_WR, **Q3), G('C4', 'D4', 'numerical', pm_tab, **Q4), W('C4', 'D5', 'long', PM_LONG, marks=6)],
    S + '12-st3': [M('C1', 'D1', SD_FACT[:3]), M('C1', 'D2', SD_FACT[3:]), G('C2', 'D2', 'mcq', decision), AR('C2', 'D3', SD_AR), G('C3', 'D2', 'numerical', sd_tab, marks=1),
                   G('C3', 'D3', 'numerical', sd_tab, **Q3), G('C3', 'D4', 'case', sd_case, **CASE), G('C3', 'D1', 'mcq', decision), W('C4', 'D3', 'explain', SD_WR, **Q3),
                   W('C4', 'D4', 'long', SD_LONG, marks=6), G('C2', 'D3', 'mcq', decision)],
    S + '12-st4': [M('C1', 'D1', ES_FACT[:4]), M('C1', 'D2', ES_FACT[4:]), G('C2', 'D2', 'mcq', sup_event), G('C2', 'D3', 'mcq', sup_event), AR('C2', 'D2', ES_AR),
                   G('C3', 'D2', 'numerical', es_pct, marks=1), G('C3', 'D3', 'numerical', es_lin, **Q3), G('C3', 'D1', 'numerical', mkt_sup, marks=1), G('C3', 'D4', 'case', es_case, **CASE),
                   W('C4', 'D3', 'explain', ES_WR, **Q3), G('C4', 'D4', 'numerical', es_pct, **Q3)],
    S + '13-st1': [M('C1', 'D1', EQ_FACT[:3]), M('C1', 'D2', EQ_FACT[3:]), G('C2', 'D2', 'mcq', excess), G('C2', 'D3', 'mcq', excess), AR('C2', 'D2', EQ_AR),
                   G('C3', 'D1', 'numerical', eq_tab, marks=1), G('C3', 'D2', 'numerical', eq_lin, **Q3), G('C3', 'D3', 'numerical', eq_lin, marks=1), G('C3', 'D4', 'case', eq_case, **CASE),
                   W('C4', 'D3', 'explain', EQ_WR, **Q3), W('C4', 'D4', 'long', EQ_LONG, marks=6), G('C4', 'D4', 'case', eq_case, **CASE)],
    S + '13-st2': [M('C1', 'D1', SIM[:3]), M('C1', 'D2', SIM[3:]), G('C2', 'D2', 'mcq', shift_ev), G('C2', 'D3', 'mcq', shift_ev), AR('C2', 'D3', SH_AR), G('C3', 'D2', 'mcq', shift_ev),
                   G('C3', 'D3', 'numerical', shift_num, **Q4), G('C3', 'D4', 'case', shift_case, **CASE), W('C4', 'D3', 'explain', SH_WR, **Q3), G('C4', 'D4', 'numerical', shift_num, **Q4),
                   W('C4', 'D5', 'long', SH_LONG, marks=6), G('C3', 'D1', 'mcq', shift_ev)],
    S + '13-st3': [M('C1', 'D1', FE_FACT[:3]), M('C1', 'D2', FE_FACT[3:]), AR('C2', 'D2', FE_AR), G('C2', 'D3', 'numerical', free_entry, marks=1), G('C3', 'D2', 'numerical', free_entry, **Q3),
                   G('C3', 'D4', 'case', fe_case, **CASE), W('C4', 'D3', 'explain', FE_WR, **Q3), W('C4', 'D4', 'long', FE_LONG, marks=6), G('C3', 'D3', 'numerical', free_entry, **Q4),
                   G('C2', 'D2', 'numerical', free_entry, marks=1)],
    S + '13-st4': [G('C4', 'D4', 'long', eqm_long, marks=6), M('C1', 'D1', CF_FACT[:4]), M('C1', 'D2', CF_FACT[4:]), G('C2', 'D2', 'mcq', bind), G('C2', 'D3', 'mcq', bind), AR('C2', 'D2', CF_AR),
                   G('C3', 'D2', 'numerical', ceiling, marks=1), G('C3', 'D3', 'numerical', floor, **Q3), G('C3', 'D4', 'case', cf_case, **CASE), W('C4', 'D3', 'explain', CF_WR, **Q3),
                   W('C4', 'D4', 'long', CF_LONG, marks=6), G('C3', 'D1', 'numerical', ceiling, marks=1), G('C4', 'D4', 'numerical', floor, **Q4)],
}


# Tidy coefficient 1 in linear functions ("1p" -> "p") in every generated string.
import re as _re
_ONE = _re.compile(r'(?<![\d.,/])1p(?![\w])')
_ONEX = _re.compile(r'(?<![\d.,/])1x(?=[₁₂])')


def _tidy(v):
    if isinstance(v, str):
        return _ONEX.sub('x', _ONE.sub('p', v))
    if isinstance(v, list):
        return [_tidy(x) for x in v]
    if isinstance(v, dict):
        return {k: _tidy(x) for k, x in v.items()}
    return v


def _wrap(g):
    def gen(r):
        return _tidy(g(r))
    return gen


for _fs in FAMILIES.values():
    for _f in _fs:
        _f.gen = _wrap(_f.gen)
