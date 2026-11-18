"""IB DP Economics SL/HL (first assessment 2022) - ib-g11-economics, year 1 (Units 1 and 2).

Assessment model mirrored in the items:
  Paper 1 extended response: (a) explain, with a diagram [10] and (b) evaluate with real-world examples [15].
  Paper 2 data response: definitions [2], data/diagram analysis [4], calculations (HL) and an evaluation
          using the text and the student's own knowledge [15].
  Paper 3 (HL) policy paper: quantitative questions with computed answers and a policy recommendation [10].
Command terms follow the IB guide (define, outline, describe, explain, distinguish, analyse, calculate,
evaluate, discuss, to what extent, justify, recommend). Numerical items are parametric and compute their
answers; markschemes award [1] for valid working and [1] for the correct answer with units, as in IB.
Note: XED is not in the 2022 syllabus, so it is only used where the curriculum names it (it does not).
"""
from __future__ import annotations

import math
from fractions import Fraction as Fr

from _common import F, Registry, T, mcq, name, two_names, CITIES


def fmt(x, sf=3):
    """Numbers for economics answers: integers as integers, otherwise at most 2 decimal places."""
    x = float(x)
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    s = f'{x:.2f}'.rstrip('0').rstrip('.')
    return s


def sm(x, cur='$'):
    """Signed money: -281.6 -> −$281.6."""
    return ('−' if x < 0 else '') + cur + fmt(abs(x))

CONFIG = {'minutesPerMark': 2.0, 'mcqMinutes': 1.5}

# One HL mock = Paper 1 (2 parts) + Paper 2 (3 parts) + Paper 3 (2 parts): 7 questions, 60 marks.
MOCK = [
    dict(section='Paper 1 (a) - Explain, using a diagram', count=1, c=['C3'], d=[4], type='long', marks=10, style='p1a'),
    dict(section='Paper 1 (b) - Evaluate, using real-world examples', count=1, c=['C4'], d=[5], type='long', marks=15),
    dict(section='Paper 2 (a) - Definition', count=1, c=['C1'], d=[2], type='short', marks=2),
    dict(section='Paper 2 (b) - Data / diagram analysis', count=1, c=['C3'], d=[3], type='case', marks=4),
    dict(section='Paper 2 (c) - Evaluate using the text and own knowledge', count=1, c=['C4'], d=[5], type='long', marks=15, style='p2'),
    dict(section='Paper 3 (a) - Calculation', count=1, c=['C3'], d=[4], type='numerical', marks=4),
    dict(section='Paper 3 (b) - Policy recommendation', count=1, c=['C4'], d=[4], type='long', marks=10, style='p3'),
]

MB15 = ('IB Paper 1(b)/2(d) markbands [15]: Level 5 (13-15) relevant terms defined; theory explained clearly with an accurate, '
        'fully explained diagram where relevant; appropriate real-world examples; effective synthesis and a supported evaluation '
        '(short- vs long-run, stakeholders, assumptions, priorities). Level 4 (10-12) evaluation present but not fully developed. '
        'Level 3 (7-9) some evaluation, explanation partly developed. Level 2 (4-6) limited explanation, little evaluation. '
        'Level 1 (1-3) little understanding.')
MB10 = ('IB Paper 1(a) markbands [10]: Level 4 (9-10) terms defined; clear, focused explanation; relevant, accurate and fully '
        'labelled diagram(s) that are explained. Level 3 (6-8) mostly accurate with some development. Level 2 (3-5) limited '
        'explanation or diagram errors. Level 1 (1-2) little understanding.')
MBP3 = ('Policy recommendation markbands [10]: Level 4 (9-10) a clear recommendation that is justified with economic theory, '
        'the information provided and its likely consequences for stakeholders; trade-offs and risks weighed. Level 3 (6-8) '
        'recommendation supported but justification partly developed. Level 2 (3-5) limited justification. Level 1 (1-2) '
        'recommendation asserted.')
STYLE = {'eval_marks': 10, 'essay_marks': 15, 'markband': MB15}

R = Registry()
DIAG: dict[str, list] = {}

GOODS = ['coffee', 'bus tickets', 'smartphones', 'cinema tickets', 'bottled water', 'running shoes', 'bread',
         'electric scooters', 'concert tickets', 'chocolate bars', 'streaming subscriptions', 'avocados']
CUR = [('$', ''), ('€', ''), ('£', ''), ('', ' Kenyan shillings'), ('', ' pesos'), ('', ' rupees')]


def init(subject_id):
    pass


def S(key, diag=(), **kw):
    """Register a subtopic fact pack plus Paper 1(a) diagram questions (phrase, answer)."""
    R.facts(key, F(**kw))
    DIAG[key] = list(diag)


def _key(st):
    return st['id'].rsplit('-', 2)[-2] + '-' + st['id'].rsplit('-', 1)[-1]


def lc(s):
    return s[0].lower() + s[1:]


def templates(st):
    key = _key(st)
    out = R.build(st, STYLE)
    f = R.f.get(key)
    items = DIAG.get(key) or []
    if items:
        def diag(rng, slot, items=items):
            phrase, ans = rng.choice(items)
            if slot.d <= 3:
                stem = rng.choice([f'Draw a diagram to illustrate {phrase}, and outline what it shows.',
                                   f'With the help of a labelled diagram, outline {phrase}.'])
                m = 6
            else:
                stem = rng.choice([f'Using an appropriate diagram, explain {phrase}.',
                                   f'Explain, with the help of a fully labelled diagram, {phrase}.'])
                m = 10
            return dict(stem=stem, answer=ans, type='long', marks=m,
                        markingKey=f'Indicative content: {ans} {MB10 if m == 10 else "Award up to 2 marks for an accurate, fully labelled diagram and up to 4 for the explanation linked to it."}')
        out.append(T('C3', (3, 5), diag, 'long', 'p1a', 'diag'))
    if f and f.evaluate:
        srcs = [(x[0], x[1]) for x in f.sources] or [(cs[1], f'Based on {cs[0]}') for cs in f.cases]

        def p2(rng, slot, f=f):
            if slot.style != 'p2' or not srcs:   # reserved for Paper 2 mock sections
                return None
            claim, pro, con, judge = rng.choice(f.evaluate)
            src, attr = rng.choice(srcs)
            ask = rng.choice([f'evaluate the view that {lc(claim)}',
                              f'discuss whether {lc(claim).rstrip(".")}.',
                              f'examine the extent to which {lc(claim).rstrip(".")}.'])
            stem = (f'Read the extract below.\n\n{src}\n— {attr}\n\nUsing information from the extract and your knowledge of '
                    f'economics, {ask}')
            key = ('Arguments for: ' + '; '.join(pro) + '. Arguments against: ' + '; '.join(con) +
                   f'. Judgement: {judge} Reward explicit use of the extract. {MB15}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=15, gap='G7')
        out.append(T('C4', (4, 5), p2, 'long', 'p2', 'p2'))

        def p1b(rng, slot, f=f):
            claim, pro, con, judge = rng.choice(f.evaluate)
            stem = rng.choice([f'Using real-world examples, evaluate the view that {lc(claim)}',
                               f'Using real-world examples, discuss the claim that {lc(claim)}'])
            key = ('Arguments for: ' + '; '.join(pro) + '. Arguments against: ' + '; '.join(con) +
                   f'. Judgement: {judge} Credit relevant diagrams and specific real-world examples. {MB15}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=15)
        out.append(T('C4', (4, 5), p1b, 'long', None, 'p1b'))

        def p3(rng, slot, f=f):
            if slot.style != 'p3':   # reserved for Paper 3 mock sections
                return None
            claim, pro, con, judge = rng.choice(f.evaluate)
            role = rng.choice(['an economist advising the government', 'a policy adviser to the ministry of finance',
                               'an analyst at the competition and consumer authority', 'an adviser to a regional development agency'])
            stem = (f'You are {role}. A minister argues that {lc(claim)} Using your knowledge of economics, write a policy '
                    f'recommendation that evaluates this view and recommends a course of action.')
            key = ('Supporting points: ' + '; '.join(pro) + '. Counter-points: ' + '; '.join(con) +
                   f'. Recommendation: {judge} {MBP3}')
            return dict(stem=stem, answer=judge, markingKey=key, type='long', marks=10)
        out.append(T('C4', (4, 5), p3, 'long', 'p3', 'p3'))
    return out


# ---------------------------------------------------------------------------------------------
# numeric helpers
# ---------------------------------------------------------------------------------------------
def money(x, cur=('$', '')):
    pre, post = cur
    if abs(x - round(x)) < 1e-9:
        s = f'{int(round(x)):,}'
    else:
        s = f'{x:,.2f}'
    return f'{pre}{s}{post}'


def r2(x):
    s = f'{x:.2f}'
    s = s.rstrip('0').rstrip('.') if '.' in s else s
    return s.replace('-', '−')


def pct(new, old):
    return 100.0 * (new - old) / old


def lin_d(a, b):
    return f'Qd = {a} − {b}P' if b != 1 else f'Qd = {a} − P'


def lin_s(c, d):
    dd = '' if d == 1 else str(d)
    if c == 0:
        return f'Qs = {dd}P'
    if c < 0:
        return f'Qs = −{-c} + {dd}P'
    return f'Qs = {c} + {dd}P'


def market(rng, need_cneg=True, big=False):
    """Random linear market with integer equilibrium: returns a, b, c, d, P*, Q*."""
    for _ in range(200):
        b = rng.choice([1, 2, 2, 3, 4, 5] if not big else [2, 4, 5, 10])
        d = rng.choice([1, 2, 3, 3, 4, 5, 6] if not big else [3, 5, 6, 10])
        P = rng.randint(4, 30)
        c = rng.choice([-40, -30, -20, -10, -5, 0, 10, 20] if not need_cneg else [-60, -40, -30, -20, -10, -5])
        Q = c + d * P
        a = Q + b * P
        if Q > 5 and a > 0 and a % b == 0 and (c == 0 or (-c) % d == 0):
            return a, b, c, d, P, Q
    return None


MKT_FRAMES = [
    'In the market for {g} in {city}, demand and supply are given by {D} and {S}, where P is the price in dollars and Q is quantity in thousands of units per week.',
    'A researcher estimates that the weekly demand for {g} in {city} is {D} and the weekly supply is {S} (P in $, Q in thousands).',
    'The following functions describe the market for {g} in {city}: {D} and {S}, with P in $ and Q in hundreds of units per day.',
    'Data from a consumer survey and from producers in {city} give the demand function {D} and the supply function {S} for {g} (P in $; Q in thousands per month).',
]


def mkt_intro(rng, a, b, c, d, g=None):
    g = g or rng.choice(GOODS)
    return rng.choice(MKT_FRAMES).format(g=g, city=rng.choice(CITIES), D=lin_d(a, b), S=lin_s(c, d)), g


# =============================================================================================
# ch01 Unit 1.1 What is economics? Economics as a social science
# =============================================================================================
S('ch01-st1',
  terms=[("economics", "the social science that studies how individuals, firms and governments allocate scarce resources among competing, unlimited wants"),
         ("ceteris paribus", "the assumption that all other variables are held constant while the effect of one variable is examined"),
         ("economic model", "a simplified representation of reality, based on assumptions, used to explain and predict economic behaviour"),
         ("hypothesis", "a testable statement about the relationship between economic variables, derived from a theory or model"),
         ("social science", "a discipline that studies human behaviour and society, in which controlled laboratory experiments are rarely possible")],
  facts=[("Which of the following best explains why economics is classed as a social science?", "It studies human behaviour, which cannot usually be tested in controlled experiments", ["It uses mathematics and graphs", "It is concerned only with money and prices", "Its predictions are always exact"], "Economics studies people's choices; unlike the natural sciences, controlled experiments are rarely possible, so economists rely on models and ceteris paribus."),
         ("Which of the following is the correct order of the social scientific method?", "Observe, form a hypothesis, test it against data, accept, reject or refine the theory", ["Form a theory, publish it, then collect data", "Collect data, publish results, then form a hypothesis", "Assume ceteris paribus, then observe the result"], "Economists move from observation to a testable hypothesis, test it with real-world data and revise the model."),
         ("Which of the following is the main purpose of the ceteris paribus assumption?", "To isolate the effect of one variable on another", ["To make a model completely realistic", "To remove the need for data", "To ensure a market reaches equilibrium"], "Holding other things constant lets economists study the effect of, for example, price alone on quantity demanded.")],
  why=[("Explain why economists use simplifying assumptions when building models.", "The real economy has countless interacting variables; assumptions (e.g. rational agents, ceteris paribus) strip away detail so that a cause-and-effect relationship can be identified and predictions made, which can then be tested against data."),
       ("Explain why it is difficult for economists to run controlled experiments.", "Economies involve millions of people whose behaviour changes over time; variables cannot be held constant in the real world and it is often unethical or impractical to manipulate people's incomes or prices, so economists rely on observed data and natural experiments."),
       ("Explain how the ceteris paribus assumption is used when drawing a demand curve.", "A demand curve shows the relationship between price and quantity demanded only, holding income, tastes, prices of related goods and other determinants constant; if one of these changes the whole curve shifts."),
       ("Explain why economic predictions may turn out to be wrong even if the model is logically correct.", "Predictions depend on assumptions holding; in reality other factors change at the same time (ceteris paribus is violated), people may not behave rationally and data may be incomplete, so outcomes differ from what the model predicts.")],
  contrast=[("a theory", "a hypothesis", "A hypothesis is a single testable statement about how variables are related; a theory is a broader, tested explanation built from hypotheses that have been supported by evidence."),
            ("economics as a social science", "a natural science such as physics", "Both use models and test hypotheses against evidence, but economics studies human behaviour, which changes and cannot be placed in controlled laboratory conditions, so results are less exact and depend on ceteris paribus.")],
  misc=[("Economic models are useless because they are unrealistic.", "Models are deliberately simplified; their value lies in isolating key relationships and generating testable predictions. A model is judged by how well it explains and predicts, not by how realistic its assumptions are."),
        ("Ceteris paribus means that nothing in the economy ever changes.", "Ceteris paribus is an analytical assumption that other variables are held constant only while the effect of one variable is studied; in reality many variables change together.")],
  apply=[("A researcher wants to know whether a rise in bus fares in Nairobi reduces the number of journeys. Identify one variable she must hold constant (ceteris paribus) and explain why.", "For example the price of matatu (minibus) fares, household income or fuel prices; if these changed at the same time, the fall in journeys could not be attributed to the fare rise alone.", 2),
         ("A model predicts that higher cigarette taxes reduce smoking. State one piece of real-world evidence an economist could use to test this hypothesis.", "Data on cigarette sales or smoking rates before and after a tax rise (e.g. in Australia, where large tobacco excise increases from 2010 were followed by falling smoking rates), controlling for other factors.", 2),
         ("Outline how an economist might test the hypothesis that a higher minimum wage reduces youth employment.", "Collect employment data for young workers before and after the change, compare with a similar region that did not change its minimum wage (a natural experiment), hold other factors constant as far as possible and accept, reject or refine the hypothesis.", 3)],
  cases=[("Card and Krueger's 1994 study of fast-food employment in New Jersey and Pennsylvania", "After New Jersey raised its minimum wage in 1992, employment in fast-food restaurants did not fall relative to neighbouring Pennsylvania.", "the use of natural experiments to test economic hypotheses", "Economists cannot run controlled experiments, so they compare similar groups exposed to different policies; the result challenged the simple model's prediction and led to refined theories of labour markets."),
         ("Finland's basic income experiment (2017-2018)", "2,000 unemployed people received €560 a month unconditionally and their outcomes were compared with a control group.", "how economists test hypotheses with real-world data", "A randomised trial let researchers isolate the effect of an unconditional payment on employment and well-being, holding other factors constant by comparison with the control group.")],
  sources=[("Economists predicted that a sugar tax would reduce consumption of sugary drinks. When the UK introduced its Soft Drinks Industry Levy in 2018, many manufacturers cut the sugar content of their drinks before the tax began, so the amount of sugar sold fell even though volumes of soft drinks sold did not fall by much.", "Extract based on reporting of the UK Soft Drinks Industry Levy", "Using the extract, explain why the outcome of the policy was different from a simple model's prediction.", "The simple model assumes the product is unchanged and predicts lower quantity demanded as price rises; in reality firms responded by reformulating, so sales volumes held up while sugar intake fell – other variables (product characteristics) did not stay constant.")],
  evaluate=[("The use of ceteris paribus makes economic models of little value for real-world policy decisions.", ["real markets never hold other variables constant", "policy makers need predictions that hold when many variables change together", "unrealistic assumptions can lead to policy mistakes"], ["isolating one relationship is the only way to understand cause and effect", "models can be extended to include more variables and tested with data", "models such as supply and demand predict the direction of change well"], "Ceteris paribus limits precision but is essential for analysis; models remain valuable if their assumptions are understood and predictions are tested against evidence."),
            ("Economics can never be as scientific as physics.", ["human behaviour is less predictable than physical laws", "controlled experiments are rarely possible", "value judgements influence the questions economists ask"], ["economists use the scientific method: hypotheses tested against data", "randomised controlled trials and natural experiments are increasingly used (e.g. Nobel prize 2019 for field experiments)", "econometric methods allow some variables to be controlled statistically"], "Economics uses scientific methods but its subject matter makes results probabilistic rather than exact; it is a science of tendencies.")],
  extended=[("Explain how an economist would use the social scientific method to investigate whether higher fuel prices reduce car use in a city such as Singapore.", "Observation (fuel prices rising, traffic data); hypothesis (higher fuel prices reduce car journeys, ceteris paribus); collect data on fuel prices and journeys; control for other factors such as income, public transport fares and COE prices; test the hypothesis; accept, reject or refine; recognise limitations of real-world data.", 6)],
  diag=[("how a demand curve is drawn on the assumption of ceteris paribus, and what happens to the curve when one of the other factors changes", "Diagram: price on the vertical axis, quantity demanded on the horizontal axis; downward-sloping D1. With other factors constant a price change causes a movement along D1. If income (a non-price determinant) rises for a normal good, ceteris paribus no longer holds and the curve shifts right to D2; at every price more is demanded.")])

S('ch01-st2',
  terms=[("scarcity", "the condition in which human wants are unlimited but the resources available to satisfy them are limited"),
         ("opportunity cost", "the value of the next best alternative forgone when a choice is made"),
         ("free good", "a good that is not scarce, so it has zero opportunity cost, such as air in most places"),
         ("economic good", "a good that is scarce and therefore has an opportunity cost to produce or consume"),
         ("needs", "goods and services essential for survival, such as food, water and shelter"),
         ("wants", "goods and services that people desire beyond their basic needs; they are effectively unlimited")],
  facts=[("Which of the following are the three basic economic questions?", "What to produce, how to produce and for whom to produce", ["What to buy, where to buy and when to buy", "How much to tax, how much to spend and how much to borrow", "What to export, what to import and what to save"], "Every society must decide what to produce, how to produce it and for whom, because resources are scarce."),
         ("Which of the following is the best example of opportunity cost for a government?", "A hospital that cannot be built because funds are spent on a new airport", ["The money spent on the airport", "The tax revenue raised to build the airport", "The profit earned by the construction firm"], "Opportunity cost is the next best alternative forgone, not the money spent."),
         ("Which of the following goods is most likely to be a free good?", "Sea water on a beach", ["Bottled water", "Clean tap water in a city", "Water used for crop irrigation"], "Sea water at a beach is not scarce relative to demand, so its use involves no sacrifice."),
         ("Why does scarcity exist?", "Resources are finite while wants are unlimited", ["Prices are too high", "Governments restrict production", "Some people are poor"], "Scarcity is a universal condition facing all economies, rich and poor.")],
  why=[("Explain why scarcity forces individuals and societies to make choices.", "Because resources are limited relative to unlimited wants, using resources for one purpose means they cannot be used for another; therefore every economic agent must choose, and each choice has an opportunity cost."),
       ("Explain why opportunity cost is not the same as the money price of a good.", "The money price is what is paid; opportunity cost is the next best alternative given up, which can include time and other uses of the money. Two people paying the same price may face different opportunity costs."),
       ("Explain why scarcity is a problem for rich countries as well as poor countries.", "Even rich economies have finite land, labour, capital and time while wants keep growing; they too must choose between, for example, healthcare, education and defence, so opportunity costs remain."),
       ("Explain why the question 'for whom to produce' is linked to equity.", "It concerns how output is distributed among people; market systems distribute according to purchasing power, which may be unequal, so societies decide whether to redistribute to achieve a fairer outcome.")],
  contrast=[("a free good", "an economic good", "An economic good is scarce, so producing or consuming it has an opportunity cost; a free good is so plentiful relative to wants that it has zero opportunity cost."),
            ("needs", "wants", "Needs are the basic requirements for survival (food, shelter, clothing); wants are desires beyond needs and are unlimited, which is the root of scarcity.")],
  misc=[("Something that is free to consumers, such as state school education, is a free good.", "State education is free at the point of use but uses scarce resources (teachers, buildings) paid for through taxes, so it has an opportunity cost; it is an economic good, not a free good."),
        ("Opportunity cost is the total of all the alternatives that are given up.", "Opportunity cost is only the value of the single next best alternative forgone, not all the alternatives."),
        ("Scarcity only exists when there is a shortage of a product in the shops.", "Scarcity is the permanent condition of limited resources relative to unlimited wants; a shortage is a temporary situation where quantity demanded exceeds quantity supplied at a given price.")],
  apply=[("A government in Ghana has a budget of $50 million that it can spend on either a new hospital or 200 km of rural roads. It chooses the hospital. Identify the opportunity cost of this decision.", "The 200 km of rural roads that are given up (the next best alternative).", 1),
         ("Priya has one free evening. She can work at a café, revise for an economics test, or go to the cinema. She ranks revision first and the café second. State her opportunity cost of revising.", "The café work (and the wages she would have earned) – the next best alternative, not the cinema.", 1),
         ("Explain how a country deciding whether to produce rice using tractors or using many farm workers is answering one of the basic economic questions.", "It is answering 'how to produce': choosing between a capital-intensive and a labour-intensive method, depending on the relative cost and availability of capital and labour.", 2)],
  cases=[("the Covid-19 vaccine roll-out in 2021", "Governments had limited doses and had to decide who would be vaccinated first, usually the elderly and health workers.", "scarcity and the 'for whom' question", "Doses were scarce relative to demand, so a rationing rule had to decide who received them; giving a dose to one group meant another group waited."),
         ("Germany's decision in 2022 to create a €100 billion fund for its armed forces", "After the invasion of Ukraine, the German government committed €100 billion to defence modernisation.", "opportunity cost for governments", "The funds could have been used for other priorities such as climate investment or education, which is the opportunity cost of higher defence spending.")],
  sources=[("A university student in Toronto calculates that a year of full-time study costs CAD 8,000 in tuition and CAD 2,000 in books. By studying she also gives up a full-time job paying CAD 38,000 a year after tax.", "Hypothetical data", "Using the information, calculate the opportunity cost of one year of study and explain your answer.", "Opportunity cost = forgone earnings CAD 38,000 plus the CAD 10,000 of tuition and books that could have been spent elsewhere = CAD 48,000 (living costs are excluded because they are paid whether she studies or works).")],
  evaluate=[("The concept of opportunity cost is the most important idea in economics.", ["every choice under scarcity has an opportunity cost", "it applies to individuals, firms and governments", "it underlies the PPC, comparative advantage and cost-benefit analysis"], ["opportunity costs are hard to measure in money terms", "people may not consider opportunity costs (bounded rationality)", "other concepts such as equity or sustainability also matter"], "Opportunity cost is fundamental because it follows directly from scarcity, but it must be used alongside other concepts and is often difficult to quantify."),
            ("Free public services such as healthcare have no opportunity cost.", ["users pay nothing at the point of use", "the service may be provided using otherwise idle resources"], ["resources (doctors, hospitals) could be used elsewhere", "taxes that fund them have alternative uses", "waiting lists show the resources are scarce"], "Public services are free at the point of use but not free to society; they always involve an opportunity cost."),
            ("Scarcity will eventually disappear as technology improves.", ["technology increases productivity and potential output", "some goods (digital files) can be copied at near-zero cost"], ["wants grow as incomes rise", "natural resources and time remain finite", "environmental limits create new scarcities"], "Technology can ease scarcity of particular goods but scarcity as a condition remains because wants are unlimited.")],
  extended=[("A city council in Lisbon can spend €20 million on either a new metro line extension or modernising 15 schools. Explain the concepts of scarcity, choice and opportunity cost using this example, and discuss one factor the council should consider in making its choice.", "Scarcity: limited budget versus many needs; choice: council must pick one; opportunity cost: whichever project is not chosen; factors: number of people who benefit, long-term returns (education human capital vs reduced congestion), equity, external benefits, opinion of voters.", 6)],
  diag=[("how the concept of opportunity cost arises from scarcity, using a production possibilities curve", "Diagram: two goods (e.g. healthcare and education) on the axes; a concave PPC. Points on the curve are attainable and efficient; a point outside is unattainable because of scarcity. Moving along the curve from A to B gives more of one good only by giving up some of the other: that amount is the opportunity cost. Increasing opportunity cost explains the concave shape.")])


@R.add('ch01-st2', 'C3', (1, 4), 'numerical')
def oc_calc(rng, slot):
    who = name(rng)
    wage = rng.choice([12, 14, 15, 18, 20, 22, 25])
    hrs = rng.choice([3, 4, 5, 6])
    ticket = rng.choice([30, 40, 45, 55, 60, 75])
    travel = rng.choice([0, 5, 8, 10, 12])
    ev = rng.choice(['a football match', 'a music festival', 'a theatre show', 'a cricket match', 'a gaming tournament'])
    city = rng.choice(CITIES)
    total = ticket + travel + wage * hrs
    if slot.d <= 2:
        stem = f'{who} pays ${ticket} for a ticket to {ev} in {city} instead of working a {hrs}-hour shift at ${wage} per hour. Calculate the opportunity cost of attending.'
        total = ticket + wage * hrs
        key = f'Opportunity cost = ticket ${ticket} + forgone earnings {hrs} × ${wage} = ${ticket + wage * hrs}. [1] working, [1] answer.'
        return dict(stem=stem, answer=f'${total}', markingKey=key, type='numerical', marks=2)
    stem = (f'{who} could work {hrs} hours at a café in {city} for ${wage} an hour. Instead {who} goes to {ev}: the ticket costs ${ticket} '
            f'and travel costs ${travel}. Calculate the full opportunity cost of attending and explain why the money cost alone understates it.')
    key = (f'Explicit costs ${ticket} + ${travel} = ${ticket + travel}; forgone earnings {hrs} × ${wage} = ${wage * hrs}; total = ${total}. '
           f'[1] explicit costs, [1] forgone wages, [1] total, [1] explanation: the money price ignores the next best use of time.')
    return dict(stem=stem, answer=f'${total}', markingKey=key, type='numerical', marks=4)


S('ch01-st3',
  terms=[("efficiency", "making the best use of scarce resources so that waste is minimised; allocative efficiency occurs when resources produce the mix of goods society values most"),
         ("equity", "fairness in the distribution of income, wealth or opportunity; it is a normative concept and differs from equality"),
         ("economic well-being", "the level of prosperity and quality of life of people, including income, health, security and opportunities"),
         ("sustainability", "the ability of the present generation to meet its needs without compromising the ability of future generations to meet theirs"),
         ("interdependence", "the way economic agents, sectors and countries rely on each other, so a change in one affects others"),
         ("intervention", "government involvement in markets, through policies such as taxes, subsidies, regulation and provision, to change market outcomes")],
  facts=[("Which of the following lists contains only IB Economics key concepts?", "Scarcity, choice, efficiency, equity, sustainability", ["Scarcity, profit, wages, interest, rent", "Demand, supply, price, market, equilibrium", "Inflation, unemployment, growth, deficit, debt"], "The nine key concepts are scarcity, choice, efficiency, equity, economic well-being, sustainability, change, interdependence and intervention."),
         ("Which key concept is most directly illustrated by a global semiconductor shortage halting car production in Europe?", "Interdependence", ["Equity", "Scarcity only", "Intervention"], "Car makers depend on chip producers in Asia; a disruption in one part of the supply chain affects production elsewhere."),
         ("Which of the following best describes the key concept 'change'?", "Economies are dynamic, so conditions, technologies and policies evolve over time", ["Prices always rise over time", "Governments change every election", "Consumers change their preferences every year"], "Change refers to the dynamic nature of economies and the need for theory and policy to respond.")],
  why=[("Explain why equity and equality are not the same.", "Equality means everyone receives the same; equity means fairness, which may require unequal treatment (e.g. larger transfers to people with disabilities). Whether an outcome is equitable is a normative judgement."),
       ("Explain why sustainability can conflict with economic growth.", "Growth often uses more natural resources and generates pollution; if resources are depleted faster than they regenerate, future generations' ability to meet their needs is reduced, so a trade-off between current output and sustainability may exist."),
       ("Explain how the key concept of intervention links to market failure.", "When markets fail to allocate resources efficiently or equitably (e.g. externalities, public goods), governments may intervene with taxes, subsidies, regulation or provision to improve the outcome."),
       ("Explain why economic well-being cannot be measured by income alone.", "Well-being also depends on health, education, security, the environment and leisure; a country can have high income per capita but poor health outcomes or high inequality, so composite measures are needed.")],
  contrast=[("efficiency", "equity", "Efficiency concerns making the best use of resources (maximising output or welfare); equity concerns the fairness of how that output is distributed. A market can be efficient but inequitable."),
            ("scarcity", "choice", "Scarcity is the condition of limited resources relative to wants; choice is the decision it forces, which always involves an opportunity cost.")],
  misc=[("An equitable distribution of income means everyone earns exactly the same.", "That describes equality. Equity is about fairness, which is a normative idea; many people regard some differences in income (e.g. for effort or skill) as fair."),
        ("Sustainability is only about the environment.", "Sustainability also includes social and economic aspects, such as sustainable public finances and maintaining human capital for future generations.")],
  apply=[("Identify the key concept most relevant to a news article about drought in Brazil raising coffee prices in Europe, and explain your choice.", "Interdependence: European consumers depend on Brazilian producers, so a supply shock in Brazil affects prices in Europe (scarcity and change could also be argued).", 2),
         ("A government introduces free school meals for low-income families. Identify two key concepts that this policy illustrates.", "Equity (helping disadvantaged households) and intervention (government provision); economic well-being is also acceptable.", 2),
         ("Explain how the key concept of change applies to the growth of ride-hailing apps such as Uber and Grab.", "Technology has changed how transport services are supplied, disrupting taxi markets, creating new jobs (gig work) and prompting new regulations; economies and policies must adapt.", 3)],
  cases=[("the Paris Agreement of 2015", "Nearly 200 countries agreed to limit global warming to well below 2°C above pre-industrial levels.", "the key concept of sustainability", "It recognises that current production and consumption threaten future generations, and sets targets to reduce emissions so that needs can be met over the long run."),
         ("the 2021 Suez Canal blockage by the container ship Ever Given", "A single ship blocked the canal for six days, delaying an estimated $9-10 billion of trade per day.", "the key concept of interdependence", "Global supply chains depend on key routes; a disruption in one place delayed goods and raised costs for firms and consumers around the world.")],
  sources=[("Bhutan measures progress using a Gross National Happiness index, which includes psychological well-being, health, education, time use, cultural diversity, good governance, community vitality, ecological resilience and living standards.", "Based on the Centre for Bhutan Studies", "Explain which key concept is illustrated by Bhutan's approach and why it differs from using GDP alone.", "Economic well-being: Bhutan includes non-income dimensions of quality of life; GDP measures only the value of output, so it ignores health, environment and how time is used.")],
  evaluate=[("Efficiency should always be the main goal of economic policy.", ["efficient use of resources maximises output and living standards", "waste of scarce resources has an opportunity cost"], ["efficient outcomes may be inequitable", "short-run efficiency may undermine sustainability", "well-being depends on more than output"], "Efficiency is important, but policy must balance it against equity and sustainability; the right balance is a normative choice."),
            ("Government intervention is the best way to achieve equity.", ["markets distribute according to purchasing power, not need", "taxes and transfers can redistribute effectively", "governments can provide merit goods to all"], ["intervention can reduce incentives and efficiency", "government failure: poorly targeted policies", "NGOs, communities and firms (CSR) also improve equity"], "Intervention is usually necessary for equity, but its design matters to limit efficiency losses and government failure.")],
  extended=[("Using one real-world example, explain how two of the nine key concepts can be in conflict.", "e.g. coal mining in Australia or Indonesia: efficiency/economic well-being (jobs, export earnings, cheap energy) versus sustainability (emissions, environmental damage); or efficiency vs equity in a minimum wage. Explain each concept, show the trade-off and comment on how policy might balance them.", 6)],
  diag=[("how a market outcome may be efficient but not equitable, using a supply and demand diagram for a basic good such as housing", "Diagram: rental price vs quantity of housing; equilibrium at Pe, Qe where demand equals supply, so the allocation is efficient (social surplus maximised assuming no externalities). But households with low incomes are priced out: those to the right of Qe on the demand curve want housing but cannot pay Pe. The outcome is efficient yet may be judged inequitable, so governments may intervene (subsidies, social housing).")])


S('ch01-st4',
  terms=[("positive economics", "statements about what is, was or will be that can be tested against evidence"),
         ("normative economics", "statements about what ought to be, based on value judgements, which cannot be tested"),
         ("value judgement", "an opinion based on personal values or beliefs about what is good or desirable"),
         ("invisible hand", "Adam Smith's idea that individuals pursuing their own self-interest in competitive markets unintentionally promote the interest of society"),
         ("laissez-faire", "the view that governments should not interfere in the operation of free markets")],
  facts=[("Which of the following is a positive economic statement?", "An increase in the minimum wage in 2023 was followed by a fall in youth employment", ["The minimum wage should be raised to reduce poverty", "It is unfair that young workers earn less", "Governments ought to reduce taxes on the rich"], "A positive statement can be tested against evidence, even if it turns out to be false."),
         ("Which economist argued in The General Theory (1936) that governments should increase spending to fight unemployment?", "John Maynard Keynes", ["Adam Smith", "Friedrich Hayek", "Karl Marx"], "Keynes argued that insufficient aggregate demand could cause persistent unemployment and that government intervention was needed."),
         ("Which economist is associated with The Wealth of Nations (1776), the division of labour and the 'invisible hand'?", "Adam Smith", ["David Ricardo", "John Maynard Keynes", "Milton Friedman"], "Smith's 1776 work is regarded as the founding text of classical economics."),
         ("Which economist argued in The Road to Serfdom (1944) that central planning threatens freedom because planners lack the dispersed knowledge held by individuals?", "Friedrich Hayek", ["Karl Marx", "John Maynard Keynes", "Thomas Malthus"], "Hayek emphasised the price mechanism as a way of coordinating dispersed knowledge.")],
  why=[("Explain why the statement 'the government should ban single-use plastics' is normative.", "It expresses a value judgement about what ought to be done and cannot be proven true or false by evidence; it depends on how one weighs environmental benefits against costs to firms and consumers."),
       ("Explain why economists who agree on positive analysis may still disagree on policy.", "They may agree on the likely effects of a policy (positive) but place different values on the outcomes, such as efficiency versus equity, so their normative conclusions differ."),
       ("Explain why Karl Marx was critical of the capitalist system.", "Marx argued that capitalists exploit workers by paying them less than the value they produce (surplus value), causing inequality, class conflict and recurring crises; he predicted capitalism would be replaced by socialism.")],
  contrast=[("positive economics", "normative economics", "Positive statements are about what is and can be tested with evidence; normative statements are about what ought to be and contain value judgements."),
            ("Keynes's view of government", "Hayek's view of government", "Keynes saw an active role for government in managing demand to reduce unemployment; Hayek warned that intervention and planning distort price signals and threaten freedom, favouring free markets.")],
  misc=[("A positive statement must be true.", "A positive statement only needs to be testable; it can be shown to be false by evidence (e.g. 'raising tariffs increases employment')."),
        ("Adam Smith believed governments should play no role at all in the economy.", "Smith supported a limited role for the state, including defence, justice and some public works and education; he was not opposed to all government activity.")],
  apply=[("Classify each statement as positive or normative: (i) 'Inflation in the euro area was above 8% in 2022.' (ii) 'The central bank should prioritise employment over low inflation.'", "(i) positive – it can be checked against data; (ii) normative – it is a value judgement about priorities.", 2),
         ("Rewrite the normative statement 'Petrol taxes are too high' as a positive statement that could be tested.", "e.g. 'A 10% rise in petrol taxes reduces petrol consumption by 2% within a year' – a testable claim about cause and effect.", 2)],
  cases=[("the rise of behavioural economics, recognised by Nobel prizes to Daniel Kahneman (2002) and Richard Thaler (2017)", "Economists showed that people systematically deviate from rational choice, for example through loss aversion and present bias.", "the development of economic thought", "Economic theory changes when evidence challenges its assumptions; behavioural findings led to new policy tools such as nudges.")],
  evaluate=[("Economists should restrict themselves to positive economics and leave normative questions to politicians.", ["positive analysis is testable and objective", "economists have no special authority on values"], ["policy choices always involve values", "economists' expertise helps clarify trade-offs", "choosing which questions to study is itself normative"], "Economists should make clear when they move from positive to normative statements, but their analysis is valuable in normative debates.")],
  diag=[("how a positive analysis of a tax can inform, but not settle, a normative debate about whether it should be introduced", "Diagram: supply and demand for a good with a specific tax shifting S to S+tax; price rises, quantity falls, tax revenue and welfare loss shown. These effects are positive (testable). Whether the tax should be introduced depends on value judgements, e.g. weighing revenue and reduced consumption of a harmful good against higher prices for low-income consumers.")])

# =============================================================================================
# ch02 Unit 1.1 Production possibilities curve and economic systems
# =============================================================================================
S('ch02-st1',
  terms=[("production possibilities curve (PPC)", "a curve showing the maximum combinations of two goods an economy can produce with all its resources fully and efficiently employed, given technology"),
         ("productive efficiency (on the PPC)", "a situation where output is on the PPC, so it is impossible to produce more of one good without producing less of the other"),
         ("increasing opportunity cost", "the situation where each extra unit of one good requires giving up more and more of the other good, because resources are not equally suited to both"),
         ("unattainable combination", "a combination of goods lying outside the PPC that cannot be produced with current resources and technology"),
         ("unemployment of resources", "a situation in which some factors of production are idle, so the economy produces inside its PPC")],
  facts=[("Which of the following explains why a PPC is usually concave (bowed out) to the origin?", "Resources are not equally suited to producing both goods, so opportunity cost increases", ["Opportunity cost is constant", "Technology improves as output rises", "Demand for both goods falls as more is produced"], "As more of one good is produced, less suitable resources must be transferred, so more of the other good is sacrificed."),
         ("Which of the following does a point inside the PPC represent?", "Unemployed or inefficiently used resources", ["Economic growth", "An unattainable combination", "Allocative efficiency"], "Inside the curve the economy could produce more of both goods by using idle resources."),
         ("Which of the following does a straight-line PPC indicate?", "Constant opportunity cost", ["Increasing opportunity cost", "Zero opportunity cost", "Economic growth"], "A constant slope means each extra unit costs the same amount of the other good, as when resources are perfectly substitutable.")],
  why=[("Explain why any point on the PPC is productively efficient.", "On the curve all resources are fully employed with the best available technology, so more of one good can only be produced by giving up some of the other – there is no waste."),
       ("Explain why moving along a PPC illustrates opportunity cost.", "Moving from one point to another on the curve increases output of one good only by reducing output of the other; the amount given up is the opportunity cost of the extra units."),
       ("Explain why a point on the PPC is not necessarily allocatively efficient.", "Every point on the curve is productively efficient, but only one combination matches the mix of goods society values most; producing too many weapons and too little food, for example, is efficient in production but not in allocation.")],
  contrast=[("a movement along the PPC", "a movement from inside to onto the PPC", "A movement along the curve reallocates fully employed resources, so one good is sacrificed for the other; moving from inside to the curve uses previously unemployed resources, so output of both goods can rise with no opportunity cost."),
            ("constant opportunity cost", "increasing opportunity cost", "With constant opportunity cost the PPC is a straight line because resources are equally suited to both goods; with increasing opportunity cost it is concave because resources are specialised.")],
  misc=[("A point inside the PPC is unattainable.", "A point inside the PPC is attainable but inefficient (resources are unemployed or wasted); points outside the curve are unattainable."),
        ("If an economy is on its PPC it must be producing the best combination of goods for society.", "Being on the curve means productive efficiency only; the best combination (allocative efficiency) depends on society's preferences.")],
  cases=[("the Covid-19 lockdowns of 2020", "Many workers and factories were idle as shops, restaurants and factories closed.", "a point inside the PPC", "Resources were unemployed, so actual output fell below potential: the economy moved from a point on its PPC to a point inside it."),
         ("the shift of US factories to military production during the Second World War", "Car plants such as Ford's were converted to build tanks and aircraft, and civilian car production almost stopped.", "opportunity cost shown by a PPC", "The economy moved along its PPC towards military goods; the opportunity cost was the civilian goods no longer produced.")],
  sources=[("In 2020, India's government imposed a strict national lockdown. Official data showed GDP fell by about 24% in the April-June quarter compared with a year earlier, as millions of migrant workers lost their jobs.", "Based on data from India's National Statistical Office", "Using a PPC, explain what the data suggest happened to India's economy.", "Output fell sharply while productive capacity was largely unchanged: the economy moved from a point on (or near) its PPC to a point well inside it because labour and capital were unemployed.")],
  evaluate=[("The PPC model is too simple to be useful in analysing a real economy.", ["it shows only two goods", "it assumes fixed resources and technology", "it cannot show prices or the distribution of income"], ["it clearly illustrates scarcity, choice and opportunity cost", "it distinguishes unemployment (inside) from growth (shift)", "it can show trade-offs such as consumer vs capital goods"], "The PPC is a simplification, but it is a powerful way of illustrating core concepts; its usefulness is conceptual rather than predictive.")],
  extended=[("A country produces only food and machinery. Explain, using a PPC, the effect of a decision to devote more resources to machinery production on present and future living standards.", "Movement along the PPC towards machinery: opportunity cost is food now (lower current consumption); more capital goods raise future productive capacity, shifting the PPC outward later; trade-off between present and future living standards.", 6)],
  diag=[("why a production possibilities curve is concave to the origin and how it illustrates increasing opportunity cost", "Diagram: good X on the horizontal axis, good Y on the vertical axis; a concave PPC. Moving from A to B to C, each equal increase in X requires a larger fall in Y, because resources best suited to Y are increasingly used for X. Points on the curve are productively efficient; inside: unemployment; outside: unattainable."),
        ("the difference between a point inside a PPC, a point on it and a point outside it", "Diagram: concave PPC for two goods. Point inside (U): unemployed or inefficient resources, more of both goods possible. Point on (E): full employment, productive efficiency, opportunity cost in moving along the curve. Point outside (O): unattainable with current resources and technology; reachable only through economic growth (outward shift).")])


@R.add('ch02-st1', 'C3', (1, 5), 'numerical')
def ppc_table(rng, slot):
    for _ in range(50):
        goods = rng.choice([('wheat (tonnes)', 'tractors'), ('rice (tonnes)', 'textiles (rolls)'), ('healthcare (units)', 'education (units)'),
                            ('solar panels', 'wind turbines'), ('fish (tonnes)', 'timber (m³)'), ('consumer goods', 'capital goods')])
        country = rng.choice(['Country A', 'Ruritania', 'an island economy', 'Country Z', 'a small agricultural economy'])
        n = 5
        xs = [0, 10, 20, 30, 40] if slot.d <= 3 else [0, 5, 10, 15, 20]
        gaps = sorted(rng.sample(range(2, 30), 4))  # increasing opportunity cost
        ymax = sum(gaps) + rng.randint(0, 5)
        ys = [ymax]
        for g in gaps:
            ys.append(ys[-1] - g)
        if ys[-1] < 0:
            continue
        rows = ', '.join(f'({xs[i]}, {ys[i]})' for i in range(n))
        i = rng.randint(1, 3)
        oc = (ys[i] - ys[i + 1])
        per = Fr(oc, xs[i + 1] - xs[i])
        stem = (f'The table shows the production possibilities of {country} producing {goods[0]} (first number) and {goods[1]} (second number): {rows}. ')
        if slot.d <= 2:
            stem += f'Calculate the opportunity cost of increasing output of {goods[0].split(" (")[0]} from {xs[i]} to {xs[i + 1]}.'
            ans = f'{oc} {goods[1]}'
            key = f'{ys[i]} − {ys[i + 1]} = {oc} {goods[1]} given up. [1] working [1] answer.'
            return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=2)
        stem += (f'Calculate the opportunity cost per unit of {goods[0].split(" (")[0]} when output rises from {xs[i]} to {xs[i + 1]}, '
                 f'and from {xs[i + 1] if i < 3 else xs[i - 1]} to {xs[i + 2] if i < 3 else xs[i]}. Explain what your results show about the shape of the PPC.')
        j = i + 1 if i < 3 else i - 1
        oc2 = ys[j] - ys[j + 1]
        per2 = Fr(oc2, xs[j + 1] - xs[j])
        ans = f'{fmt(float(per), 3)} and {fmt(float(per2), 3)} units of {goods[1]} per unit; opportunity cost changes, so the PPC is concave (increasing opportunity cost).'
        key = (f'First: {oc}/{xs[i + 1] - xs[i]} = {fmt(float(per), 3)}; second: {oc2}/{xs[j + 1] - xs[j]} = {fmt(float(per2), 3)} [2]. '
               f'Opportunity cost rises as more is produced because resources are not equally suited to both goods, so the curve is bowed out [2].')
        return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=4)
    return None


S('ch02-st2',
  terms=[("economic growth", "an increase in real output (real GDP) over time; long-term growth is an increase in potential output, shown by an outward shift of the PPC"),
         ("actual output", "the real output an economy produces in a period, shown by a point on or inside the PPC"),
         ("potential output", "the maximum output an economy can produce when all resources are fully and efficiently employed, shown by the PPC itself"),
         ("capital goods", "man-made goods, such as machinery and infrastructure, used to produce other goods and services"),
         ("output gap", "the difference between actual and potential output, often expressed as a percentage of potential output")],
  facts=[("Which of the following would shift a country's PPC outwards?", "An improvement in technology", ["A fall in unemployment", "A rise in the price of exports", "A reduction in income tax rates for consumers only"], "Better technology increases the maximum output possible from existing resources."),
         ("Which of the following would cause the PPC to shift inwards?", "A natural disaster that destroys factories and infrastructure", ["A recession that raises unemployment", "A rise in interest rates", "A fall in consumer confidence"], "Destroying capital reduces potential output; a recession only moves the economy inside an unchanged PPC."),
         ("Which of the following would shift the PPC outwards only along the axis for one good?", "A new technology that raises productivity in one industry only", ["An increase in the labour force", "An increase in education across the economy", "A discovery of new resources used in all industries"], "If only one industry benefits, the maximum of that good rises while the other intercept is unchanged.")],
  why=[("Explain why a fall in unemployment does not shift the PPC.", "Lower unemployment uses existing resources more fully, moving actual output from inside the PPC towards the curve; potential output (the curve itself) is unchanged."),
       ("Explain why producing more capital goods today can lead to faster economic growth in future.", "Capital goods increase the quantity of capital available for production; this raises productive capacity, shifting the PPC outward in the future, although current consumption must be sacrificed."),
       ("Explain why an improvement in education can lead to an outward shift of the PPC.", "Education raises human capital – the skills and productivity of labour – so more output can be produced from the same number of workers, increasing potential output.")],
  contrast=[("actual growth", "potential growth", "Actual growth is a rise in real output, shown by a movement from inside towards (or along) the PPC; potential growth is an increase in productive capacity, shown by an outward shift of the PPC."),
            ("a movement from inside the PPC to the curve", "an outward shift of the PPC", "The first uses previously unemployed resources so actual output rises with capacity unchanged; the second increases the maximum output possible because of more or better resources or technology.")],
  misc=[("Any increase in a country's GDP is shown by an outward shift of the PPC.", "If an economy moves from inside its PPC towards the curve (e.g. recovery from recession), GDP rises without the PPC shifting; only an increase in potential output shifts the curve."),
        ("Mass emigration of young workers shifts a country's PPC outwards because there are fewer people to feed.", "Emigration reduces the quantity of labour, which reduces potential output and shifts the PPC inwards.")],
  apply=[("Ukraine's economy contracted by about 29% in 2022 after the Russian invasion, as factories, power stations and ports were destroyed. Explain the effect on Ukraine's PPC.", "Destruction of capital and the loss of labour (displacement, mobilisation) reduced productive capacity, so the PPC shifted inwards; actual output also fell as resources were idle, moving further inside the curve.", 3),
         ("Explain how the discovery of large oil reserves off the coast of Guyana from 2015 affects its PPC.", "More natural resources (land) increase potential output, so the PPC shifts outward, especially along the axis of goods using oil; actual output rose rapidly as production started in 2019.", 2)],
  cases=[("China's high investment rate since the 1990s", "China invested over 40% of GDP in factories, infrastructure and housing for many years.", "the link between capital goods and economic growth", "Large investment in capital goods raised productive capacity, shifting China's PPC outward and helping average growth of around 9-10% a year for three decades.")],
  sources=[("In 2023 a central bank estimated that its economy's potential output was $520 billion while actual output was $494 billion. Unemployment had risen to 7.5% from 5% a year earlier.", "Hypothetical central bank report", "Using a PPC and the data, explain the position of the economy and calculate its output gap as a percentage of potential output.", "Output gap = (494 − 520)/520 × 100 = −5%: actual output is below potential, so the economy is at a point inside its PPC; rising unemployment confirms idle resources.")],
  evaluate=[("Investment in capital goods is the most important cause of economic growth.", ["more capital raises labour productivity", "infrastructure reduces costs across the economy", "evidence from East Asian economies"], ["human capital and technology may matter more", "institutions and the rule of law are needed", "investment that is wasted (unproductive projects) adds little"], "Capital accumulation is a key cause but long-run growth depends on technology, human capital and institutions that make investment productive.")],
  extended=[("A government faces a choice between increasing spending on consumer goods to raise current living standards and spending on infrastructure. Using a PPC, explain the trade-off and the likely long-run outcome of each choice.", "Moving along the PPC: more consumer goods now means fewer capital goods; less capital accumulation means slower outward shifts later; choosing capital goods sacrifices current consumption but shifts the PPC further out in future, allowing more of both later.", 6)],
  diag=[("the difference between actual economic growth and an increase in potential output", "Diagram: two goods on the axes; PPC1. Point A inside PPC1 moving to B on PPC1 is actual growth using idle resources (e.g. recovery). An outward shift of PPC1 to PPC2 (more resources, better technology, more human capital) is an increase in potential output; point C on PPC2 was previously unattainable.")])


@R.add('ch02-st2', 'C3', (1, 4), 'numerical')
def growth_calc(rng, slot):
    c = rng.choice(['Vietnam', 'Kenya', 'Peru', 'Poland', 'Indonesia', 'Morocco', 'Chile', 'Bangladesh'])
    pot = rng.randint(300, 900)
    gap = rng.choice([-6, -5, -4, -3, -2, 2, 3])
    act = round(pot * (1 + gap / 100))
    g = rng.choice([2, 3, 4, 5, 6])
    if slot.d <= 2:
        y0 = rng.randint(200, 800)
        y1 = round(y0 * (1 + g / 100) + rng.randint(-3, 3), 0)
        gr = pct(y1, y0)
        return dict(stem=f'Real GDP in {c} rose from ${y0} billion to ${int(y1)} billion over one year. Calculate the rate of economic growth.',
                    answer=f'{r2(gr)}%', markingKey=f'({int(y1)} − {y0})/{y0} × 100 = {r2(gr)}%. [1] working [1] answer.', type='numerical', marks=2)
    og = (act - pot) / pot * 100
    pos = 'inside its PPC (negative output gap: idle resources)' if act < pot else 'beyond its sustainable potential (positive output gap), producing near or temporarily beyond the PPC by over-using resources'
    return dict(stem=f'An estimate for {c} puts potential output at ${pot} billion and actual output at ${act} billion. Calculate the output gap as a percentage of potential output and explain where the economy is relative to its PPC.',
                answer=f'{r2(og)}%; {pos}', markingKey=f'({act} − {pot})/{pot} × 100 = {r2(og)}% [2]. Interpretation: {pos} [2].', type='numerical', marks=4)


S('ch02-st3',
  terms=[("factors of production", "the resources used to produce goods and services: land, labour, capital and entrepreneurship"),
         ("entrepreneurship", "the factor that organises the other factors of production and takes the risks of running a business"),
         ("free market economy", "an economic system in which resources are allocated by the price mechanism and are mainly privately owned"),
         ("planned (command) economy", "an economic system in which the government owns most resources and decides what, how and for whom to produce"),
         ("mixed economy", "an economic system in which resources are allocated by both the price mechanism and the government, with private and public sectors"),
         ("transition economy", "an economy moving from central planning towards a market system, such as the former Soviet bloc after 1991")],
  facts=[("Which of the following is the reward to the factor of production land?", "Rent", ["Wages", "Interest", "Profit"], "Land earns rent, labour earns wages, capital earns interest and entrepreneurship earns profit."),
         ("Which of the following is an example of capital as a factor of production?", "A delivery van used by a bakery", ["Money saved in a bank account", "A worker's skills", "Farmland"], "Capital is man-made goods used to produce other goods; financial capital is not a factor of production in this sense."),
         ("Which of the following countries is closest to a centrally planned economy today?", "North Korea", ["Singapore", "Sweden", "Chile"], "North Korea's state controls most production and prices."),
         ("In a free market economy, how are the basic economic questions answered?", "Through the price mechanism, by the interaction of buyers and sellers", ["By a central planning committee", "By elected local councils", "By the central bank"], "Prices signal scarcity and give incentives to producers and consumers.")],
  why=[("Explain why planned economies often suffered from shortages of consumer goods.", "Planners set prices and output targets without accurate information on consumer wants; prices did not signal scarcity, managers lacked profit incentives, and resources were directed to heavy industry and defence, so queues and shortages were common (e.g. the USSR in the 1980s)."),
       ("Explain why almost all economies today are mixed economies.", "Markets allocate most goods efficiently, but they fail to provide public goods, under-provide merit goods and may be inequitable; governments therefore provide some goods (defence, education) and regulate markets, combining both systems."),
       ("Explain why entrepreneurship is considered a separate factor of production.", "Entrepreneurs combine land, labour and capital, make decisions and bear risk; without this organising role production would not take place, and the reward (profit) is distinct from wages, rent or interest.")],
  contrast=[("a free market economy", "a planned economy", "In a free market, private owners and the price mechanism decide what, how and for whom; in a planned economy the state owns resources and planners make these decisions."),
            ("human capital", "physical capital", "Physical capital is man-made equipment and infrastructure; human capital is the education, skills and health of workers. Both raise productivity.")],
  misc=[("Money is a factor of production because firms need it to buy machines.", "Money (financial capital) is not itself a factor; it is used to buy capital goods, which are the factor of production."),
        ("In a mixed economy the government owns all the major industries.", "A mixed economy has both private and public sectors; many mixed economies (e.g. Germany) have mostly private industry with government providing services and regulating.")],
  apply=[("Identify the factor of production in each case: (i) a coffee plantation in Colombia; (ii) a barista; (iii) an espresso machine; (iv) the person who starts the café chain.", "(i) land; (ii) labour; (iii) capital; (iv) entrepreneurship.", 2),
         ("Since 1978 China has moved from central planning towards a 'socialist market economy'. Outline two changes this involved.", "e.g. farmers allowed to sell surplus output at market prices (household responsibility system); private firms and foreign investment permitted (Special Economic Zones such as Shenzhen); prices freed for many goods; state-owned enterprises reformed.", 2)],
  cases=[("the collapse of the Soviet Union in 1991", "Russia and other former Soviet states moved rapidly from central planning to markets, privatising state firms and freeing prices.", "the transition from a planned to a market economy", "Freeing prices ended shortages but caused high inflation and a deep fall in output in the early 1990s, showing the costs of transition."),
         ("Singapore's Housing and Development Board (HDB)", "Around 80% of Singapore's residents live in public housing built by the state, while the rest of the economy is highly market-oriented.", "a mixed economy", "Singapore combines free markets in most goods with substantial government provision of housing, showing that real economies mix both systems.")],
  sources=[("In Venezuela, the government fixed the prices of many basic goods from 2003 and nationalised hundreds of firms. By 2016 supermarkets regularly had empty shelves and many producers had stopped production because the fixed prices were below their costs.", "Extract based on news reporting, 2016", "Using the extract, explain one weakness of extensive state control of the economy.", "Fixed prices below costs removed the incentive to produce, so supply fell and shortages appeared; price signals no longer reflected scarcity, showing the information and incentive problems of planning.")],
  evaluate=[("A free market economy is the best system for allocating resources.", ["price mechanism signals scarcity and gives incentives", "consumer sovereignty and choice", "competition encourages efficiency and innovation"], ["market failure: public goods, externalities, merit goods", "inequality of income and wealth", "instability and unemployment"], "Markets allocate most goods efficiently, but all successful economies are mixed because of market failure and equity concerns.")],
  diag=[("how the price mechanism answers the question 'what to produce' when consumer tastes change", "Diagram: market for plant-based milk; demand shifts from D1 to D2 as tastes change; excess demand at the original price raises price from P1 to P2; quantity supplied rises from Q1 to Q2 along S. The higher price signals producers to allocate more resources to this good and gives them the incentive (profits) to do so; the opposite occurs in the market for dairy milk.")])

# =============================================================================================
# ch03 Unit 1.1 The circular flow of income model
# =============================================================================================
S('ch03-st1',
  terms=[("circular flow of income", "a model showing the flows of money and real resources between households and firms (and, in the full model, government, financial and foreign sectors)"),
         ("household", "an economic agent that owns the factors of production and consumes goods and services"),
         ("factor market", "a market in which households sell factors of production (e.g. labour) to firms in return for factor incomes"),
         ("product market", "a market in which firms sell goods and services to households"),
         ("real flow", "the flow of goods, services and factors of production in the circular flow, opposite to the money flow")],
  facts=[("In the simple two-sector circular flow model, which of the following flows from households to firms?", "Factors of production and consumer spending", ["Wages, rent, interest and profits", "Goods and services", "Taxes and savings"], "Households supply factors (real flow) and spend income on output (money flow); firms pay factor incomes and supply goods."),
         ("Which of the following correctly matches the factor of production with its income?", "Labour – wages; capital – interest", ["Labour – profit; land – interest", "Capital – rent; entrepreneurship – wages", "Land – profit; labour – rent"], "Land earns rent, labour wages, capital interest and entrepreneurship profit."),
         ("Which of the following is the main assumption of the simple two-sector circular flow model?", "Households spend all their income and there is no government or foreign trade", ["Firms save all their profits", "Households save part of their income", "Imports equal exports"], "In the closed model all income is spent, so the flow stays constant.")],
  why=[("Explain why in the simple circular flow model the value of output equals the value of income and of expenditure.", "Firms' revenue from selling output is paid out as factor incomes (wages, rent, interest, profit), and households spend all income on firms' output, so output = income = expenditure."),
       ("Explain why the circular flow shows that households and firms are interdependent.", "Households depend on firms for incomes and goods, while firms depend on households for factors of production and for spending; a fall in spending by households reduces firms' revenue and therefore incomes."),
       ("Explain why the money flow and the real flow move in opposite directions.", "Money is paid in exchange for real goods and resources: households give labour to firms and receive wages, firms give goods to households and receive spending.")],
  contrast=[("the money flow", "the real flow", "The money flow is the payments (incomes and spending); the real flow is the goods, services and factors of production exchanged for those payments, moving in the opposite direction."),
            ("the factor market", "the product market", "In the factor market households sell land, labour, capital and enterprise to firms; in the product market firms sell goods and services to households.")],
  misc=[("In the circular flow, firms own the factors of production.", "Households own the factors of production and sell their services to firms in factor markets."),
        ("Profit is not part of the circular flow because firms keep it.", "Profit is the reward to entrepreneurship and is paid to the households who own firms, so it is part of factor income.")],
  apply=[("A taxi driver in Bogotá earns wages from a ride-hailing company and spends them at a supermarket. Identify the flows in the circular flow model that this involves.", "Labour (real) flows from the household to a firm and wages (money) flow back – factor market; spending at the supermarket (money) flows to firms and groceries (real) flow to the household – product market.", 2),
         ("Explain what happens to the circular flow if households in a two-sector economy suddenly cut their spending by 10%.", "Firms' revenues fall by 10%, so they cut output and pay less in factor incomes; household incomes fall, which reduces spending further – the flow shrinks.", 3)],
  cases=[("the fall in tourist spending in Thailand in 2020", "International tourist arrivals fell from almost 40 million in 2019 to under 7 million in 2020.", "the circular flow of income", "Less spending on hotels and restaurants reduced firms' revenues, so they cut wages and jobs; households' incomes fell, reducing their own spending – the flow of income shrank.")],
  evaluate=[("The circular flow model is too simple to explain how a real economy works.", ["ignores prices and inflation", "assumes all income is spent in the simple model", "does not show distribution of income"], ["shows interdependence clearly", "explains why output = income = expenditure (basis of national accounts)", "can be extended with leakages and injections"], "The simple model is a starting point; extended with leakages and injections it is the basis of national income accounting and macroeconomic analysis.")],
  extended=[("Explain, with reference to the circular flow of income, why the three methods of measuring national income should give the same result.", "Output method values goods produced; income method adds factor incomes paid by firms; expenditure method adds spending on output. In the circular flow, the value of output is paid as incomes, which are spent on output, so all three are equal (subject to statistical discrepancies).", 6)],
  diag=[("the simple two-sector circular flow of income between households and firms", "Diagram: two boxes, households and firms. Inner loop (real flows): factors of production from households to firms; goods and services from firms to households. Outer loop (money flows): factor incomes (wages, rent, interest, profit) from firms to households; consumption expenditure from households to firms. With no leakages or injections income = output = expenditure and the flow is constant.")])


@R.add('ch03-st1', 'C3', (1, 4), 'numerical')
def income_method(rng, slot):
    w, rnt, i, p = rng.randint(200, 600), rng.randint(20, 80), rng.randint(30, 90), rng.randint(60, 200)
    c = rng.choice(['Country K', 'Atlantis', 'a closed economy', 'Country M', 'Lumeria'])
    tot = w + rnt + i + p
    if slot.d <= 2:
        return dict(stem=f'In {c} households receive wages of ${w}bn, rent of ${rnt}bn, interest of ${i}bn and profits of ${p}bn. Assuming a simple two-sector circular flow, calculate total household spending.',
                    answer=f'${tot}bn', markingKey=f'All income is spent: {w} + {rnt} + {i} + {p} = ${tot}bn. [1] working [1] answer.', type='numerical', marks=2)
    cut = rng.choice([5, 8, 10, 12, 15])
    new = tot * (1 - cut / 100)
    return dict(stem=f'Factor incomes in {c} are: wages ${w}bn, rent ${rnt}bn, interest ${i}bn, profits ${p}bn. Households then decide to spend {cut}% less in a two-sector economy. Calculate the new value of expenditure and explain what happens to factor incomes in the next round.',
                answer=f'${r2(new)}bn; factor incomes fall to ${r2(new)}bn as firms receive less revenue', markingKey=f'Income = {tot}; new spending = {tot} × {1 - cut / 100:.2f} = ${r2(new)}bn [2]; firms\' revenue falls so they pay out less: incomes fall, the flow shrinks [2].', type='numerical', marks=4)


S('ch03-st2',
  terms=[("leakage (withdrawal)", "income that is not passed on in the circular flow through spending on domestic output: saving, taxes and imports"),
         ("injection", "spending that enters the circular flow and does not come from households' consumption: investment, government spending and exports"),
         ("saving", "the part of household income that is not spent on consumption"),
         ("investment", "spending by firms on capital goods such as machinery, buildings and technology"),
         ("imports", "goods and services produced abroad and bought by domestic residents; they are a leakage from the domestic circular flow")],
  facts=[("Which of the following is a leakage from the circular flow?", "Spending on imported cars", ["Government spending on schools", "Foreign tourists spending in hotels", "Firms buying new machinery"], "Spending on imports leaves the domestic economy; the others are injections."),
         ("Which of the following correctly lists the three injections?", "Investment, government spending, exports", ["Saving, taxes, imports", "Consumption, investment, imports", "Exports, imports, taxes"], "Injections add spending to the flow from outside household consumption."),
         ("Which sector of the circular flow is linked with saving and investment?", "The financial sector", ["The government sector", "The foreign sector", "The household sector only"], "Banks and other financial institutions channel household savings to firms for investment.")],
  why=[("Explain why saving is a leakage from the circular flow.", "Saving is income that households do not spend on domestic output; it is taken out of the flow of spending, so firms' revenues are lower unless the savings are lent and spent on investment."),
       ("Explain why exports are an injection into the circular flow.", "Exports are spending by foreigners on domestic output; this money enters the domestic circular flow from outside, adding to firms' revenues and to incomes."),
       ("Explain why the size of the circular flow increases when injections exceed leakages.", "More spending enters the flow than leaves it, so firms' revenues rise; they expand output and pay more factor incomes, increasing national income until leakages rise to match injections.")],
  contrast=[("leakages", "injections", "Leakages (saving, taxes, imports) take money out of the circular flow; injections (investment, government spending, exports) add spending to it."),
            ("the four-sector model", "the two-sector model", "The two-sector model includes only households and firms with no leakages or injections; the four-sector open model adds the financial, government and foreign sectors with saving/investment, taxes/government spending and imports/exports.")],
  misc=[("Taxes are an injection into the circular flow because the government spends them.", "Taxes are a leakage – they take income out of the flow; government spending is a separate injection, and the two need not be equal."),
        ("Saving always reduces national income.", "Saving is a leakage, but if it is channelled by banks into investment (an injection) the flow need not shrink; national income only falls if total leakages exceed total injections.")],
  apply=[("Classify each as a leakage or an injection for Kenya: (i) a German tourist on safari; (ii) a Kenyan family buying a Japanese car; (iii) the government building a new railway; (iv) a household putting money in a savings account.", "(i) injection (export); (ii) leakage (import); (iii) injection (government spending); (iv) leakage (saving).", 2),
         ("Outline the likely effect on the circular flow of Germany's economy of a sharp fall in exports to China.", "Exports are an injection; a fall reduces spending on German output, so firms' revenues and incomes fall and the circular flow shrinks (unless other injections rise or leakages fall).", 2)],
  cases=[("remittances to the Philippines", "Overseas Filipino workers sent home around $37 billion in 2023, about 9% of GDP.", "injections into the circular flow from the foreign sector", "Remittances add to household incomes from abroad, increasing spending and the size of the domestic circular flow.")],
  evaluate=[("A rise in household saving is always bad for an economy.", ["saving is a leakage that reduces spending and can cause recession (paradox of thrift)", "lower consumption reduces firms' revenues"], ["savings fund investment, which raises future productive capacity", "households build buffers against shocks", "higher saving can reduce reliance on foreign borrowing"], "Higher saving reduces demand in the short run, especially in a recession, but supports investment and long-run growth if the financial sector channels it effectively.")],
  extended=[("Using the four-sector circular flow model, explain how a government budget deficit can offset a rise in household saving.", "Higher saving increases leakages, which would shrink the flow; if government spending (injection) exceeds tax revenue (leakage), the deficit adds net injections that can offset the extra saving, keeping total injections equal to total leakages at the original level of income.", 6)],
  diag=[("the circular flow of income in an open economy with a government sector, showing leakages and injections", "Diagram: households and firms with factor incomes and consumption flows; leakages leaving the flow: saving to the financial sector, taxes to government, imports to the foreign sector; injections entering the flow to firms: investment from the financial sector, government spending, exports. If injections > leakages, income rises; if leakages > injections, income falls.")])


@R.add('ch03-st2', 'C3', (2, 5), 'numerical')
def leak_inj(rng, slot):
    s, t, m = rng.randint(40, 120), rng.randint(60, 180), rng.randint(50, 150)
    i, g, x = rng.randint(40, 120), rng.randint(60, 180), rng.randint(50, 150)
    if s + t + m == i + g + x:
        return None
    c = rng.choice(['Country P', 'Freedonia', 'an open economy', 'Country Q', 'Valdoria'])
    L, J = s + t + m, i + g + x
    res = 'rise (injections exceed leakages)' if J > L else 'fall (leakages exceed injections)'
    return dict(stem=f'In {c}, saving is ${s}bn, taxes ${t}bn, imports ${m}bn, investment ${i}bn, government spending ${g}bn and exports ${x}bn. Calculate total leakages and total injections, and state what will happen to national income.',
                answer=f'Leakages ${L}bn, injections ${J}bn; national income will {res}', markingKey=f'Leakages = {s} + {t} + {m} = {L} [1]; injections = {i} + {g} + {x} = {J} [1]; income will {res} [2].', type='numerical', marks=4)


S('ch03-st3',
  terms=[("equilibrium in the circular flow", "the situation where total leakages equal total injections, so the level of national income is stable"),
         ("national income", "the total value of income earned by a country's factors of production in a year; equal in principle to output and expenditure"),
         ("gross domestic product (GDP)", "the total market value of all final goods and services produced within a country in a given period"),
         ("expenditure approach", "measuring national output as C + I + G + (X − M)")],
  facts=[("Which of the following conditions gives equilibrium in the four-sector circular flow?", "S + T + M = I + G + X", ["S = I only", "T = G only", "X = M only"], "Total leakages must equal total injections; individual pairs need not balance."),
         ("Which of the following is the expenditure method of calculating GDP?", "C + I + G + (X − M)", ["C + S + T", "Wages + rent + interest + profit − taxes", "C + I + G + X + M"], "Imports are subtracted because they are spending on foreign output."),
         ("If a country has a trade deficit of $20bn, what must be true in equilibrium?", "(S − I) + (T − G) = −$20bn", ["S must equal I", "The government must have a surplus of $20bn", "National income must fall"], "From S + T + M = I + G + X, (S − I) + (T − G) = X − M.")],
  why=[("Explain why the circular flow can be in equilibrium even if the government runs a budget deficit.", "Equilibrium requires total leakages to equal total injections; a deficit (G > T) can be offset by saving exceeding investment or imports exceeding exports."),
       ("Explain why imports are subtracted in the expenditure method of measuring GDP.", "C, I and G include spending on imported goods; that spending creates income abroad, not domestically, so it must be removed to measure domestic output."),
       ("Explain why national income changes when the economy is out of equilibrium.", "If injections exceed leakages, firms' revenues rise and they expand output and incomes; leakages rise with income until they equal injections. The reverse happens if leakages exceed injections.")],
  contrast=[("nominal GDP", "real GDP", "Nominal GDP is measured at current prices; real GDP is adjusted for inflation, so changes reflect changes in the quantity of output."),
            ("equilibrium national income", "full employment national income", "Equilibrium is where leakages equal injections, so income is stable; this need not be at full employment – the economy may be in equilibrium with unemployment.")],
  misc=[("For the circular flow to be in equilibrium, saving must equal investment, taxes must equal government spending and imports must equal exports.", "Only the totals must be equal: S + T + M = I + G + X. Individual pairs can be unbalanced as long as they offset each other."),
        ("Equilibrium national income means the economy has no unemployment.", "Equilibrium only means income is not changing; it can occur at a level below full employment.")],
  apply=[("An economy has S = $90bn, T = $120bn, M = $70bn, I = $80bn, G = $130bn and X = $70bn. Is the circular flow in equilibrium? Explain.", "Leakages = 280, injections = 280, so yes – total leakages equal total injections even though S > I and G > T.", 2)],
  cases=[("Germany's large current account surplus in the 2010s", "Germany's exports exceeded imports by around 7-8% of GDP, while households saved a high share of income.", "the link between leakages and injections in national income", "High saving (leakage) was offset by a high level of net exports (injection), so (S − I) + (T − G) = (X − M) was positive.")],
  evaluate=[("A country that saves more than it invests must run a trade surplus.", ["from the identity (S − I) + (T − G) = X − M", "examples: Germany, China"], ["a government deficit can absorb excess private saving", "the identity does not show causation", "exchange rates and capital flows also adjust"], "The identity links them, but excess private saving can be offset by a government deficit; the trade balance results from all sectoral balances together.")],
  extended=[("Using the circular flow, explain what happens to equilibrium national income if a fall in business confidence reduces investment by $15bn while all other injections are unchanged.", "Injections fall below leakages; firms' revenues fall, they cut output and incomes; as income falls, saving, taxes and imports fall until total leakages again equal the lower level of injections, at a lower equilibrium national income.", 6)],
  diag=[("how equilibrium national income is restored after an increase in government spending, using the circular flow model", "Diagram: four-sector circular flow; G (injection) rises, so injections > leakages; spending and incomes rise; as income rises, saving, taxes and imports rise; a new equilibrium is reached at a higher national income where S + T + M = I + G + X.")])


@R.add('ch03-st3', 'C3', (1, 5), 'numerical')
def gdp_exp(rng, slot):
    C, I, G, X, M = rng.randint(400, 900), rng.randint(80, 250), rng.randint(150, 350), rng.randint(100, 400), rng.randint(100, 400)
    c = rng.choice(['Country R', 'Estovia', 'Country T', 'Arcadia', 'an open economy'])
    gdp = C + I + G + X - M
    if slot.d <= 2:
        return dict(stem=f'In {c}, consumption is ${C}bn, investment ${I}bn, government spending ${G}bn, exports ${X}bn and imports ${M}bn. Calculate GDP using the expenditure method.',
                    answer=f'${gdp}bn', markingKey=f'{C} + {I} + {G} + ({X} − {M}) = ${gdp}bn. [1] formula [1] answer.', type='numerical', marks=2)
    T_ = rng.randint(120, 330)
    S_ = I + G + X - T_ - M
    if S_ <= 0:
        return None
    return dict(stem=f'In equilibrium, {c} has investment ${I}bn, government spending ${G}bn, exports ${X}bn, taxes ${T_}bn and imports ${M}bn. Calculate the level of saving consistent with equilibrium, and state the government budget balance.',
                answer=f'Saving = ${S_}bn; budget balance = ${T_ - G}bn ({"surplus" if T_ > G else "deficit" if T_ < G else "balanced"})',
                markingKey=f'S + T + M = I + G + X ⇒ S = {I} + {G} + {X} − {T_} − {M} = {S_} [2]; T − G = {T_} − {G} = {T_ - G} [1]; correct label [1].', type='numerical', marks=4)


def E(key, *claims):
    """Add evaluation claims (claim, [for], [against], judgement) to a subtopic."""
    R.f[key].evaluate.extend(claims)


def X(key, *srcs):
    R.f[key].sources.extend(srcs)


E('ch03-st2', ("Imports are harmful to an economy because they are a leakage from the circular flow.", ["imports reduce spending on domestic output", "can reduce domestic employment in import-competing industries"], ["imports give consumers choice and lower prices", "imported capital goods and inputs raise productivity", "other countries' import spending is our export injection"], "Imports are a leakage in the accounting sense, but they raise living standards and efficiency; what matters is the overall balance of leakages and injections."))
E('ch03-st1', ("Households, rather than firms, are the most important economic agents in the circular flow.", ["households own all factors of production", "consumption is the largest component of spending"], ["firms organise production and create income", "the two are interdependent: neither can function alone"], "Neither is more important: the model's central message is the interdependence of households and firms."))
E('ch03-st3', ("Equilibrium national income is always a desirable outcome for an economy.", ["stable income avoids inflationary or deflationary pressures"], ["equilibrium may occur with high unemployment", "equilibrium can hide large trade or budget imbalances"], "Equilibrium only means stability; it is desirable only if it is close to full employment and sustainable."))
E('ch02-st1', ("Every economy should aim to produce at a point on its PPC.", ["points inside mean wasted, unemployed resources", "full use of resources maximises output"], ["being on the PPC does not guarantee the right mix (allocative efficiency)", "full use of natural resources may be unsustainable", "some unemployment (frictional) is unavoidable"], "Producing on the PPC is desirable for productive efficiency, but the chosen point must also reflect society's preferences and sustainability."))
E('ch02-st2', ("Economic growth shown by an outward shift of the PPC always improves economic well-being.", ["more goods and services can be produced", "higher incomes and employment"], ["growth may be unequally distributed", "environmental costs and depletion of resources", "the mix may be capital goods or defence rather than consumer goods"], "An outward shift increases potential well-being, but actual improvements depend on distribution, sustainability and what is produced."))
E('ch02-st3', ("Central planning can achieve faster development than a market economy.", ["state can mobilise savings for heavy industry quickly (USSR 1930s)", "can prioritise basic needs and equity"], ["information and incentive problems create waste and shortages", "lack of innovation and consumer choice", "collapse of Soviet-style systems"], "Planning may achieve rapid early industrialisation but sustained development has generally relied on markets combined with government action."))

# =============================================================================================
# ch04 Unit 2.1 Demand
# =============================================================================================
S('ch04-st1',
  terms=[("demand", "the quantity of a good or service that consumers are willing and able to buy at different possible prices in a given time period, ceteris paribus"),
         ("law of demand", "the inverse relationship between the price of a good and the quantity demanded, ceteris paribus"),
         ("market demand", "the sum of all individual consumers' demands for a good at each price"),
         ("quantity demanded", "the amount of a good consumers are willing and able to buy at one particular price"),
         ("effective demand", "a desire to buy a good that is backed by the ability to pay")],
  facts=[("Which of the following is shown by a movement along a demand curve?", "A change in quantity demanded caused by a change in the good's own price", ["A change in demand caused by a change in income", "A change in tastes", "A change in the price of a substitute"], "Only the good's own price causes a movement along the curve."),
         ("How is a market demand curve derived from individual demand curves?", "By adding the quantities demanded by each consumer at each price (horizontal summation)", ["By adding the prices each consumer is willing to pay", "By averaging individual demand curves", "By multiplying price by quantity"], "Market demand is the horizontal sum of individual demands."),
         ("Which of the following is the best description of the axes of a demand diagram?", "Price on the vertical axis and quantity on the horizontal axis", ["Quantity on the vertical axis and price on the horizontal axis", "Income on the vertical axis and quantity on the horizontal axis", "Price on both axes"], "By convention price (P) is on the y-axis and quantity (Q) on the x-axis.")],
  why=[("Explain why the demand curve normally slopes downwards from left to right.", "As price falls, the good becomes cheaper relative to substitutes (substitution effect) and consumers' real income rises (income effect); with diminishing marginal utility consumers buy more only at lower prices, so quantity demanded rises as price falls."),
       ("Explain why demand must be 'effective' to be shown on a demand curve.", "A demand curve shows quantities consumers are willing and able to buy; wanting a good without the purchasing power to buy it does not affect the market."),
       ("Explain why the demand curve is drawn for a given time period.", "Quantity demanded is a flow (e.g. per week); without a time period, quantities cannot be compared, and other determinants are more likely to change over longer periods.")],
  contrast=[("demand", "quantity demanded", "Demand is the whole relationship between price and quantity (the entire curve); quantity demanded is the amount demanded at one specific price (a point on the curve)."),
            ("individual demand", "market demand", "Individual demand is one consumer's willingness and ability to buy at each price; market demand is the sum of all individual quantities demanded at each price.")],
  misc=[("When the price of a good falls, demand increases.", "A fall in the good's own price increases the quantity demanded (a movement along the curve), not demand; demand only increases when a non-price determinant shifts the curve right."),
        ("The market demand curve is found by adding together the prices that each consumer would pay.", "Market demand is found by adding the quantities demanded by each consumer at each price – a horizontal summation.")],
  apply=[("Using the law of demand, explain what would happen to the number of rides taken on the Singapore MRT if fares rose by 10%, ceteris paribus.", "The quantity demanded of MRT rides would fall (movement up along the demand curve) as rides become more expensive relative to buses or taxis and real incomes fall.", 2)],
  cases=[("Netflix's price increases and password-sharing crackdown in 2023", "Netflix raised subscription prices in several markets; some users cancelled, though sign-ups rose after password-sharing rules made more people pay for their own accounts.", "the law of demand", "Higher prices reduced the quantity of subscriptions demanded by some consumers, while the rule change (a non-price factor) created new paying demand.")],
  sources=[("A survey of 400 students in Vienna found that at a price of €3 per coffee they would buy 2,600 coffees a week from the campus café. When the price fell to €2.50 in a promotion, purchases rose to 3,100 coffees a week.", "Hypothetical student survey", "Using the data, explain how it illustrates the law of demand.", "As the price fell from €3 to €2.50, quantity demanded rose from 2,600 to 3,100 a week, ceteris paribus – an inverse relationship between price and quantity demanded (a movement down along the demand curve).")],
  evaluate=[("The law of demand applies to all goods.", ["substitution and income effects work for nearly all goods", "strong empirical support across markets"], ["Veblen (status) goods may be demanded more at higher prices", "Giffen goods in extreme poverty (Jensen and Miller's study of rice in China)", "expectations of further price rises (speculative demand)"], "The law of demand holds for the vast majority of goods; exceptions are rare and usually short-lived."),
            ("Price is the most important factor influencing how much of a good consumers buy.", ["the law of demand shows strong price effects for most goods", "firms' pricing strategies work"], ["income, tastes and the prices of substitutes can shift demand substantially", "for necessities and addictive goods price has a weak effect", "advertising and habits matter (behavioural economics)"], "Price matters for quantity demanded, but non-price determinants often cause larger changes in demand.")],
  extended=[("Explain why a market demand curve may be flatter than an individual's demand curve for a good such as cinema tickets.", "Market demand adds quantities across consumers; at lower prices more consumers enter the market (those who would buy none at higher prices), so total quantity responds more to price than one person's demand, making the market curve flatter.", 4)],
  diag=[("the law of demand and the difference between a change in quantity demanded and a change in demand", "Diagram: P on the vertical axis, Q on the horizontal; downward-sloping D1. A fall in price from P1 to P2 moves along D1 from Q1 to Q2: an increase in quantity demanded. A change in a non-price determinant (e.g. rising income) shifts the whole curve from D1 to D2: an increase in demand – more is demanded at every price.")])


@R.add('ch04-st1', 'C3', (1, 4), 'numerical')
def market_demand(rng, slot):
    g = rng.choice(GOODS)
    people = rng.sample(['Ana', 'Kenji', 'Leila', 'Omar', 'Freya', 'Diego'], 3)
    prices = [2, 4, 6, 8]
    rows = []
    tot = []
    for p in prices:
        pass
    sched = {}
    for nme in people:
        base = rng.randint(8, 16)
        slope = rng.choice([1, 2])
        sched[nme] = [max(0, base - slope * p) for p in prices]
    tot = [sum(sched[n][i] for n in people) for i in range(4)]
    tab = '; '.join(f'{n}: ' + ', '.join(f'${p} → {q}' for p, q in zip(prices, sched[n])) for n in people)
    i = rng.randint(0, 3)
    if slot.d <= 2:
        return dict(stem=f'Three consumers are the only buyers of {g} in a small market. Their weekly demand schedules are – {tab}. Calculate the market quantity demanded at a price of ${prices[i]}.',
                    answer=str(tot[i]), markingKey=f'Market demand = horizontal sum: ' + ' + '.join(str(sched[n][i]) for n in people) + f' = {tot[i]}. [1] method [1] answer.', type='numerical', marks=2)
    j = (i + 2) % 4
    return dict(stem=f'The weekly demand schedules of the three buyers of {g} in a village market are – {tab}. Calculate market quantity demanded at ${prices[i]} and at ${prices[j]}, and explain how your answers illustrate the law of demand.',
                answer=f'{tot[i]} at ${prices[i]}; {tot[j]} at ${prices[j]}', markingKey=f'Sum each column: {tot[i]} and {tot[j]} [2]; quantity demanded is higher at the lower price, an inverse relationship ceteris paribus [2].', type='numerical', marks=4)


S('ch04-st2',
  terms=[("normal good", "a good for which demand increases when consumers' income increases"),
         ("inferior good", "a good for which demand falls when consumers' income increases, because consumers switch to better alternatives"),
         ("substitutes", "goods that can be used in place of each other, so a rise in the price of one increases demand for the other"),
         ("complements", "goods that are used together, so a rise in the price of one reduces demand for the other"),
         ("non-price determinants of demand", "factors other than the good's own price that shift the demand curve: income, tastes and preferences, prices of related goods, future price expectations and the number of consumers")],
  facts=[("Which of the following would shift the demand curve for electric cars to the right?", "A rise in the price of petrol", ["A fall in the price of electric cars", "A rise in the price of electricity", "A rise in interest rates on car loans"], "Petrol cars are substitutes; higher petrol prices make electric cars relatively more attractive."),
         ("If incomes rise and demand for instant noodles falls, the noodles are best described as which of the following?", "An inferior good", ["A normal good", "A complement", "A luxury good"], "Demand falls as income rises, so the good is inferior."),
         ("Which of the following would cause a movement along the demand curve for coffee rather than a shift?", "A fall in the price of coffee", ["A fall in the price of tea", "A health report praising coffee", "A rise in consumer incomes"], "Only a change in the good's own price causes a movement along the curve."),
         ("A rise in the price of printers would most likely cause which of the following in the market for printer ink?", "A fall in demand for ink", ["A rise in demand for ink", "A rise in quantity demanded of ink", "No change"], "Printers and ink are complements.")],
  why=[("Explain why an expected future price rise can increase demand today.", "If consumers expect prices to rise (e.g. before a tax increase), they bring forward purchases to avoid paying more later, so demand at every current price rises and the curve shifts right."),
       ("Explain why an increase in population shifts the market demand curve.", "More consumers means that at every price a larger total quantity is demanded (market demand is the sum of individual demands), so the curve shifts right."),
       ("Explain why the demand for a complement falls when the price of the related good rises.", "Complements are consumed together; a higher price of one reduces its quantity demanded, so fewer units of the complement are needed at every price – its demand curve shifts left.")],
  contrast=[("substitutes", "complements", "Substitutes are used instead of each other, so a rise in one's price raises demand for the other; complements are used together, so a rise in one's price lowers demand for the other."),
            ("a normal good", "an inferior good", "Demand for a normal good rises with income; demand for an inferior good falls as income rises because consumers switch to preferred alternatives.")],
  misc=[("A fall in the price of a good shifts its demand curve to the right.", "A change in the good's own price causes a movement along the demand curve; only non-price determinants shift it."),
        ("Inferior goods are goods of poor quality.", "'Inferior' refers only to how demand responds to income: demand falls as income rises. Many inferior goods (e.g. bus travel in some cities) are perfectly good quality.")],
  apply=[("In 2020 demand for home-workout equipment rose sharply. Identify the non-price determinant that changed and state the effect on the demand curve.", "Tastes and preferences (and the closure of gyms, which are substitutes) changed in favour of home exercise; demand shifted to the right.", 2),
         ("The price of beef in Argentina rises sharply. Explain the likely effect on the market for chicken.", "Chicken is a substitute for beef; consumers switch to chicken, so demand for chicken shifts right, raising its price and quantity.", 2),
         ("A recession reduces incomes in Spain. Explain the effect on demand for (i) restaurant meals and (ii) supermarket own-brand pasta.", "(i) restaurant meals are a normal good, so demand falls (shifts left); (ii) own-brand pasta is likely inferior, so demand rises (shifts right) as consumers trade down.", 3)],
  cases=[("the rapid growth of oat milk sales in Europe and the US", "Sales of plant-based milks rose strongly in the late 2010s as consumers became more concerned about health, animal welfare and climate change.", "a change in tastes and preferences as a non-price determinant of demand", "Changing preferences increased demand for oat milk at every price (rightward shift), while demand for dairy milk fell."),
         ("panic buying of toilet paper in March 2020", "Shoppers in Australia, the UK and the US emptied shelves as they expected shortages.", "the effect of expectations on demand", "Expected future shortages and price rises increased current demand sharply, shifting the demand curve to the right.")],
  sources=[("Sales of electric vehicles in Norway reached about 80% of new car sales in 2022. The government exempted EVs from VAT and purchase taxes, allowed them to use bus lanes and cut toll charges, while petrol prices rose sharply.", "Extract based on reporting of Norway's EV policies", "Using the extract, identify two non-price determinants that increased demand for electric vehicles and explain their effect.", "Higher petrol prices (substitute became dearer) and non-price benefits such as bus-lane access (tastes/preferences) shifted EV demand right; tax exemptions lowered the price, a movement along the demand curve.")],
  evaluate=[("Changes in consumer tastes are more important than changes in income in explaining demand for products.", ["examples: plant-based food, fast fashion trends", "firms spend heavily on advertising to influence tastes"], ["income determines ability to pay: recessions sharply cut demand for normal goods", "income effects are systematic and predictable (YED)", "importance varies by product"], "Both matter; tastes dominate for fashion and lifestyle goods while income is more important for big-ticket and luxury items.")],
  extended=[("Using demand diagrams, explain the effect of a large rise in the price of air travel on the demand for (i) international hotel rooms and (ii) high-speed rail travel within Europe.", "(i) hotels are complements to air travel: demand shifts left, lower price and quantity; (ii) rail is a substitute: demand shifts right, higher price and quantity. Each diagram: P/Q axes, original D1 and new D2, new equilibrium.", 6)],
  diag=[("the effect of a fall in consumer incomes on the demand for a normal good and an inferior good", "Two diagrams: P vs Q. Normal good (e.g. restaurant meals): demand shifts left from D1 to D2, equilibrium price and quantity fall. Inferior good (e.g. bus travel or discount supermarket brands): demand shifts right from D1 to D2, price and quantity rise. Income is a non-price determinant, so the curves shift."),
        ("how a change in the price of a complement affects demand for a good", "Diagram: market for printer ink; a rise in the price of printers reduces the quantity of printers bought, so demand for ink shifts left from D1 to D2; at the original price there is excess supply; price falls from P1 to P2 and quantity from Q1 to Q2.")])


@R.add('ch04-st2', 'C2', (1, 3), 'mcq')
def shift_or_move(rng, slot):
    cases = [("the price of tea falls", "coffee", "Demand for coffee shifts left", "tea is a substitute"),
             ("the price of smartphones falls", "phone cases", "Demand for phone cases shifts right", "phones and cases are complements"),
             ("the price of bus tickets rises", "bus tickets", "A movement up along the demand curve for bus tickets", "own-price change"),
             ("consumer incomes rise", "designer handbags", "Demand for designer handbags shifts right", "a normal (luxury) good"),
             ("consumer incomes rise", "second-hand clothing", "Demand for second-hand clothing shifts left", "likely inferior good"),
             ("a medical report links sugar to diabetes", "sugary drinks", "Demand for sugary drinks shifts left", "change in tastes"),
             ("people expect the price of houses to rise next year", "houses", "Demand for houses shifts right now", "expectations"),
             ("the price of petrol rises", "large cars", "Demand for large cars shifts left", "petrol and cars are complements"),
             ("the population of a city grows rapidly", "rental flats", "Demand for rental flats shifts right", "more consumers"),
             ("the price of streaming subscriptions falls", "streaming subscriptions", "A movement down along the demand curve for streaming subscriptions", "own-price change")]
    ev, g, ans, why = rng.choice(cases)
    pool = [f'Demand for {g} shifts right', f'Demand for {g} shifts left', f'A movement down along the demand curve for {g}',
            f'A movement up along the demand curve for {g}', f'Supply of {g} shifts left']
    pool = [p for p in pool if p != ans]
    rng.shuffle(pool)
    return mcq(rng, f'Which of the following describes the effect on the market for {g} when {ev}, ceteris paribus?', ans, pool[:3], f'{ans}: {why}.')


S('ch04-st3',
  terms=[("income effect", "the change in quantity demanded resulting from the change in real income (purchasing power) caused by a change in the good's price"),
         ("substitution effect", "the change in quantity demanded resulting from the good becoming relatively cheaper or dearer compared with substitutes"),
         ("marginal utility", "the extra satisfaction a consumer gains from consuming one more unit of a good"),
         ("law of diminishing marginal utility", "as a consumer consumes more units of a good, the extra satisfaction from each additional unit eventually falls"),
         ("total utility", "the total satisfaction a consumer gains from consuming a given quantity of a good")],
  facts=[("When the price of a normal good falls, which of the following is true?", "The income and substitution effects both increase quantity demanded", ["Only the substitution effect increases quantity demanded", "The income effect reduces quantity demanded", "Both effects reduce quantity demanded"], "Lower price raises real income and makes the good relatively cheaper; for a normal good both raise quantity demanded."),
         ("When total utility is at its maximum, what is marginal utility?", "Zero", ["At its maximum", "Equal to total utility", "Negative and falling"], "Total utility stops rising when the extra unit adds nothing."),
         ("Diminishing marginal utility helps to explain which of the following?", "Why the demand curve slopes downwards", ["Why the supply curve slopes upwards", "Why costs rise in the short run", "Why markets reach equilibrium"], "Consumers are willing to pay less for additional units that give less extra satisfaction.")],
  why=[("Explain how diminishing marginal utility explains the downward slope of the demand curve.", "Each extra unit gives less additional satisfaction, so a consumer is willing to pay less for it; to persuade consumers to buy more units the price must fall, giving an inverse price-quantity relationship."),
       ("Explain the substitution effect of a rise in the price of bus fares.", "Buses become more expensive relative to substitutes such as cycling or the metro, so consumers switch away and buy fewer bus journeys."),
       ("Explain the income effect of a fall in the price of rice for a low-income household.", "A lower price increases the household's real income (purchasing power); for a normal good it can afford to buy more rice and other goods, so quantity demanded rises.")],
  contrast=[("the income effect", "the substitution effect", "The substitution effect arises because the good's relative price changes compared with substitutes; the income effect arises because the price change alters consumers' real purchasing power."),
            ("total utility", "marginal utility", "Total utility is the overall satisfaction from all units consumed; marginal utility is the extra satisfaction from the last unit.")],
  misc=[("Diminishing marginal utility means total utility falls as more is consumed.", "Diminishing marginal utility means each extra unit adds less satisfaction; total utility still rises as long as marginal utility is positive."),
        ("The income effect only occurs if a consumer's money income changes.", "The income effect arises from a change in real income caused by a price change, even if money income is unchanged.")],
  apply=[("Explain why a café might offer a second slice of cake at half price, using the concept of diminishing marginal utility.", "The second slice gives less extra satisfaction than the first, so customers are only willing to pay a lower price for it; the discount persuades them to buy an extra unit.", 2)],
  cases=[("all-you-can-eat buffets", "Diners eat until the satisfaction from another plate is very low or zero, because each extra plate has a zero price.", "diminishing marginal utility", "Consumers keep eating while marginal utility is positive; because the price of extra food is zero they stop only when MU falls to zero.")],
  evaluate=[("Marginal utility theory gives a realistic explanation of how consumers make choices.", ["explains downward-sloping demand", "consistent with observed behaviour such as volume discounts"], ["utility cannot be measured", "consumers lack time and information to compare marginal utilities (bounded rationality)", "habits, impulse and social influences matter"], "The theory is useful for explaining the shape of demand but unrealistic as a description of how people actually decide; behavioural economics adds realism.")],
  extended=[("Using the income and substitution effects, explain why a fall in the price of a normal good leads to a larger increase in quantity demanded than a fall in the price of an inferior good.", "For a normal good both effects increase quantity demanded; for an inferior good the substitution effect raises quantity demanded but the income effect works the other way (higher real income reduces demand), so the net increase is smaller.", 6)],
  diag=[("how the law of diminishing marginal utility leads to a downward-sloping demand curve", "Diagram 1: marginal utility (vertical) against quantity consumed (horizontal), a downward-sloping MU curve. Diagram 2: price against quantity, downward-sloping demand. Because each unit gives less extra satisfaction, the price consumers are willing to pay for each extra unit falls, so the demand curve slopes down; the consumer buys up to the point where marginal benefit equals price.")])


@R.add('ch04-st3', 'C3', (1, 5), 'numerical')
def mu_table(rng, slot):
    g = rng.choice(['slices of pizza', 'cups of bubble tea', 'mangoes', 'songs downloaded', 'bus rides', 'chocolate bars'])
    who = name(rng)
    mus = sorted(rng.sample(range(2, 30), 4), reverse=True)
    tu = []
    s = 0
    for m in mus:
        s += m
        tu.append(s)
    tab = ', '.join(f'{i + 1} unit{"s" if i else ""}: {tu[i]}' for i in range(4))
    if slot.d <= 2:
        k = rng.randint(1, 3)
        return dict(stem=f'{who}\'s total utility (in utils) from {g} per day is: {tab}. Calculate the marginal utility of unit {k + 1}.',
                    answer=f'{mus[k]} utils', markingKey=f'MU = TU({k + 1}) − TU({k}) = {tu[k]} − {tu[k - 1]} = {mus[k]}. [1] [1]', type='numerical', marks=2)
    stem = (f'The table shows {who}\'s total utility (in utils) from consuming {g}: {tab}. Calculate the marginal utility of each unit and explain whether the data show diminishing marginal utility.')
    return dict(stem=stem, answer=', '.join(map(str, mus)) + ' utils; yes, MU falls with each unit',
                markingKey=f'MU = {", ".join(map(str, mus))} [2]; each extra unit adds less to total utility, so marginal utility diminishes [1], while total utility still rises because MU > 0 [1].', type='numerical', marks=4)


S('ch04-st4',
  terms=[("linear demand function", "an equation of the form Qd = a − bP showing quantity demanded as a function of price, where a is the quantity-axis intercept and b gives the change in Qd per $1 change in price"),
         ("'a' term in Qd = a − bP", "the quantity demanded when price is zero; a change in 'a' represents a shift of the demand curve caused by a non-price determinant"),
         ("'b' term in Qd = a − bP", "the change in quantity demanded for each $1 change in price; it determines the slope of the demand curve"),
         ("price intercept of a linear demand curve", "the price at which quantity demanded is zero, found as a/b")],
  facts=[("For the demand function Qd = 120 − 4P, what is the price at which quantity demanded is zero?", "$30", ["$120", "$4", "$480"], "Set Qd = 0: 4P = 120, so P = 30."),
         ("In Qd = a − bP, which change shows an increase in demand?", "An increase in a", ["An increase in b", "An increase in P", "A decrease in a"], "A larger a shifts the curve right: more is demanded at every price."),
         ("If the demand function changes from Qd = 80 − 2P to Qd = 80 − 4P, which of the following happens?", "The curve pivots: the price intercept falls from $40 to $20 while the quantity intercept stays at 80", ["The demand curve shifts right, parallel to the original", "The price intercept doubles to $80", "The quantity intercept doubles to 160"], "Price intercept = a/b: 80/2 = 40 becomes 80/4 = 20; a is unchanged, so the curve pivots around Q = 80 and quantity becomes more responsive to price.")],
  why=[("Explain why a change in the value of 'a' in Qd = a − bP shifts the demand curve.", "'a' captures the effect of all non-price determinants; if one changes (e.g. income rises) quantity demanded changes at every price, so the whole curve shifts parallel."),
       ("Explain why the slope of a linear demand curve drawn with P on the vertical axis is −1/b.", "Rearranging Qd = a − bP gives P = a/b − (1/b)Q, so price falls by 1/b for each extra unit of quantity; the larger b, the flatter the curve."),
       ("Explain why a change in 'b' changes the steepness of the demand curve.", "b measures how much quantity demanded responds to a $1 price change; a larger b means a bigger response, so with P on the vertical axis the curve is flatter.")],
  contrast=[("a change in 'a'", "a change in 'b'", "A change in 'a' shifts the demand curve parallel (a non-price determinant changes); a change in 'b' changes the slope, i.e. how responsive quantity is to price."),
            ("the price intercept", "the quantity intercept", "The quantity intercept (a) is quantity demanded when P = 0; the price intercept (a/b) is the price at which quantity demanded falls to zero.")],
  misc=[("In Qd = 100 − 5P, the curve crosses the price axis at P = 100.", "Quantity demanded is zero when 5P = 100, so the price intercept is P = 20; 100 is the quantity intercept."),
        ("If 'b' increases, the demand curve shifts to the right.", "A change in b changes the slope (responsiveness), not the position; the curve pivots around the quantity intercept.")],
  apply=[("The demand for concert tickets is Qd = 5,000 − 50P. A celebrity endorsement raises demand by 1,000 tickets at every price. Write the new demand function.", "Qd = 6,000 − 50P", 2)],
  cases=[("estimating demand functions for public transport", "Transport authorities estimate how many journeys are made at different fares, often with linear approximations, to predict the impact of fare changes.", "the use of linear demand functions", "A function Qd = a − bP lets planners predict ridership and revenue at different fares; a change in a (e.g. population growth) shifts the function.")],
  evaluate=[("Linear demand functions are too simple to be useful for real-world decision-making.", ["real demand curves are rarely straight lines", "many determinants change at once", "estimates are uncertain"], ["over a small price range a linear approximation is accurate", "simple functions give clear predictions for policy", "parameters can be updated with new data"], "Linear functions are approximations, useful over limited price ranges and for illustrating change, but should be used with caution for large price changes.")],
  extended=[("A firm estimates demand for its product to be Qd = 900 − 30P. Explain what the values 900 and 30 represent and describe how the demand curve would change if a successful advertising campaign raised quantity demanded by 150 units at every price.", "900: quantity demanded when price is zero (non-price determinants); 30: quantity demanded falls by 30 units for each $1 rise in price; new function Qd = 1,050 − 30P: parallel shift to the right, price intercept rises from $30 to $35.", 6)],
  diag=[("how a demand function Qd = a − bP is plotted, and how a change in income for a normal good changes the function and the diagram", "Diagram: P on the vertical axis, Q on the horizontal; the curve meets the Q axis at a and the P axis at a/b. A rise in income raises a to a′: the curve shifts right parallel (same slope −1/b), with a higher price intercept a′/b.")])


@R.add('ch04-st4', 'C3', (1, 5), 'numerical')
def lin_demand(rng, slot):
    b = rng.choice([2, 3, 4, 5, 10, 20])
    pint = rng.choice([10, 12, 15, 20, 25, 30, 40])
    a = b * pint
    g = rng.choice(GOODS)
    city = rng.choice(CITIES)
    v = slot.d
    if v <= 2:
        P = rng.randint(1, pint - 1)
        frame = rng.choice([f'The weekly demand for {g} in {city} is given by Qd = {a} − {b}P (P in $, Q in units). Calculate the quantity demanded when the price is ${P}.',
                            f'A café in {city} estimates demand for {g} as Qd = {a} − {b}P. How many units are demanded at a price of ${P}?'])
        return dict(stem=frame, answer=str(a - b * P), markingKey=f'Qd = {a} − {b} × {P} = {a - b * P}. [1] substitution [1] answer.', type='numerical', marks=2)
    if v == 3:
        return dict(stem=f'The demand function for {g} in {city} is Qd = {a} − {b}P. Calculate the price and quantity intercepts and explain what each represents.',
                    answer=f'Quantity intercept {a} (P = 0); price intercept ${pint} (Q = 0)',
                    markingKey=f'Q-intercept: P = 0 ⇒ Q = {a} [1]; P-intercept: {a} − {b}P = 0 ⇒ P = {a}/{b} = {pint} [1]; {a} is the quantity demanded at zero price, ${pint} the price at which no one buys [2].', type='numerical', marks=4)
    inc = rng.choice([b * 2, b * 3, b * 5])
    P = rng.randint(2, pint - 1)
    a2 = a + inc
    return dict(stem=f'Demand for {g} in {city} is Qd = {a} − {b}P. Rising incomes increase quantity demanded by {inc} units at every price. Write the new demand function, calculate the new price intercept and calculate the change in quantity demanded at a price of ${P}. State whether {g} is a normal or inferior good here.',
                answer=f'Qd = {a2} − {b}P; price intercept ${fmt(a2 / b)}; +{inc} units at ${P}; normal good',
                markingKey=f'New function Qd = {a2} − {b}P [1]; intercept {a2}/{b} = {fmt(a2 / b)} [1]; at P = {P}: {a - b * P} → {a2 - b * P}, +{inc} [1]; demand rises with income ⇒ normal good [1].', type='numerical', marks=4)

# =============================================================================================
# ch05 Unit 2.2 Supply
# =============================================================================================
S('ch05-st1',
  terms=[("supply", "the quantity of a good or service that producers are willing and able to offer for sale at different possible prices in a given time period, ceteris paribus"),
         ("law of supply", "the positive relationship between the price of a good and the quantity supplied, ceteris paribus"),
         ("market supply", "the sum of the quantities supplied by all firms in a market at each price"),
         ("quantity supplied", "the amount of a good firms are willing and able to sell at one particular price"),
         ("increasing marginal cost", "the rise in the cost of producing each additional unit of output in the short run, which explains the upward slope of the supply curve")],
  facts=[("Which of the following causes a movement along the supply curve for wheat?", "A change in the price of wheat", ["A drought", "A new fertiliser technology", "A subsidy to wheat farmers"], "Only the good's own price causes a movement along the supply curve."),
         ("Which of the following best explains why supply curves slope upwards?", "Higher prices make production more profitable and cover rising marginal costs", ["Consumers buy more at higher prices", "Costs of production fall as output rises", "Governments require firms to produce more"], "Firms increase output when price rises because extra units become profitable despite higher marginal costs."),
         ("A market has three firms supplying 20, 35 and 45 units at a price of $8. What is the market quantity supplied at $8?", "100 units", ["35 units", "33.3 units", "800 units"], "Market supply is the horizontal sum: 20 + 35 + 45 = 100.")],
  why=[("Explain why a higher price gives firms an incentive to increase quantity supplied.", "At a higher price each unit earns more revenue; output that was previously unprofitable now covers its (rising) marginal cost, so profit-maximising firms expand production and new resources are attracted into the industry."),
       ("Explain why the supply curve slopes upwards in the short run because of rising marginal costs.", "In the short run at least one factor (e.g. capital) is fixed; adding more variable factors eventually brings diminishing returns, so each extra unit costs more to produce and firms will only supply more at a higher price."),
       ("Explain why market supply increases when new firms enter an industry.", "Market supply is the sum of all firms' quantities; more firms means more is supplied at each price, so the curve shifts right.")],
  contrast=[("supply", "quantity supplied", "Supply is the whole relationship between price and quantity supplied (the curve); quantity supplied is the amount offered at one particular price."),
            ("a movement along the supply curve", "a shift of the supply curve", "A movement along the curve is caused only by a change in the good's own price; a shift is caused by a non-price determinant such as costs or technology.")],
  misc=[("When the price of a good rises, supply increases.", "A rise in the good's own price increases the quantity supplied – a movement up along the supply curve; supply (the curve) shifts only if a non-price determinant changes."),
        ("Firms supply more at higher prices because consumers want more.", "Consumers demand less at higher prices; firms supply more because higher prices make extra output profitable and cover rising marginal costs.")],
  apply=[("The world price of cocoa rose sharply in 2024. Explain the likely response of cocoa farmers in Côte d'Ivoire in the short run and in the long run.", "Short run: limited increase in quantity supplied (better harvesting, using stocks) – a movement along a steep supply curve; long run: farmers plant more trees and new land is brought into cocoa, so quantity supplied rises more as supply becomes more elastic.", 3)],
  cases=[("US shale oil producers' response to high oil prices from 2010 to 2014", "With oil prices around $100 a barrel, US shale firms rapidly drilled new wells and US output almost doubled.", "the law of supply", "Higher prices made more costly extraction profitable, so quantity supplied increased.")],
  sources=[("When the price of avocados in Mexico doubled between 2015 and 2019 because of strong export demand, farmers in Michoacán planted large new orchards, in some cases clearing forests.", "Extract based on news reporting of the avocado boom", "Using the extract, explain how the law of supply is illustrated.", "The higher price made avocado production more profitable, so farmers increased quantity supplied by planting more trees: a positive price-quantity supplied relationship; the forest clearance shows resources moving into the more profitable use.")],
  evaluate=[("Firms always increase output when the price of their product rises.", ["law of supply: higher price raises profit on extra units", "new firms are attracted"], ["capacity constraints and time lags (PES low in the short run)", "firms may expect the price rise to be temporary", "regulation, quotas or contracts may prevent expansion"], "The law of supply describes a general tendency; the size and speed of response depend on time, capacity and expectations.")],
  extended=[("Explain how a market supply curve is derived from the supply curves of individual firms, and why it shifts when firms leave the industry.", "Market supply is the horizontal sum of individual firms' quantities supplied at each price; if firms exit, fewer units are supplied at every price, so the market curve shifts left.", 4)],
  diag=[("the law of supply and the difference between a change in quantity supplied and a change in supply", "Diagram: P vs Q, upward-sloping S1. A rise in price from P1 to P2 causes a movement up along S1 from Q1 to Q2 (increase in quantity supplied). A fall in costs of production shifts the curve right from S1 to S2: an increase in supply – more is supplied at every price.")])


@R.add('ch05-st1', 'C3', (1, 4), 'numerical')
def market_supply(rng, slot):
    g = rng.choice(['tomatoes (kg)', 'T-shirts', 'loaves of bread', 'bicycles', 'coffee beans (kg)', 'mobile phone cases'])
    firms = rng.sample(['Firm A', 'Firm B', 'Firm C', 'Firm D'], 3)
    prices = [2, 4, 6, 8]
    sched = {f: [max(0, rng.randint(0, 4) + k * p) for p in prices] for f, k in zip(firms, rng.sample([1, 2, 3, 4], 3))}
    tot = [sum(sched[f][i] for f in firms) for i in range(4)]
    tab = '; '.join(f'{f}: ' + ', '.join(f'${p} → {q}' for p, q in zip(prices, sched[f])) for f in firms)
    i = rng.randint(0, 3)
    if slot.d <= 2:
        return dict(stem=f'Three firms supply {g} in a local market. Their weekly supply schedules are – {tab}. Calculate the market quantity supplied at a price of ${prices[i]}.',
                    answer=str(tot[i]), markingKey='Market supply = sum of quantities: ' + ' + '.join(str(sched[f][i]) for f in firms) + f' = {tot[i]}. [1] [1]', type='numerical', marks=2)
    j = (i + 1) % 4 if i < 3 else 0
    lo, hi = sorted([i, j])
    return dict(stem=f'The supply schedules of three producers of {g} are – {tab}. Calculate the market quantity supplied at ${prices[lo]} and ${prices[hi]}, and explain how the result illustrates the law of supply.',
                answer=f'{tot[lo]} at ${prices[lo]}; {tot[hi]} at ${prices[hi]}', markingKey=f'Horizontal summation gives {tot[lo]} and {tot[hi]} [2]; quantity supplied rises with price, a positive relationship ceteris paribus [2].', type='numerical', marks=4)


S('ch05-st2',
  terms=[("non-price determinants of supply", "factors other than the good's own price that shift the supply curve: costs of factors of production, technology, prices of related goods, expectations, indirect taxes and subsidies, the number of firms and supply shocks"),
         ("supply shock", "an unexpected event, such as a natural disaster, war or disease, that suddenly changes the supply of a good"),
         ("joint supply", "a situation where producing one good automatically produces another, such as beef and leather"),
         ("competitive supply", "a situation where producers can use the same resources to produce alternative goods, such as a farmer choosing between wheat and maize"),
         ("subsidy", "a payment by the government to producers per unit of output, which lowers their costs and shifts supply to the right")],
  facts=[("Which of the following would shift the supply curve of smartphones to the right?", "A fall in the price of microchips", ["A rise in the price of smartphones", "A rise in consumer incomes", "A rise in workers' wages"], "Lower input costs increase supply at every price."),
         ("Which of the following would shift the supply of wheat to the left?", "A severe drought in a major producing region", ["A subsidy for wheat farmers", "Improved seed varieties", "A fall in the price of fertiliser"], "A drought is a negative supply shock."),
         ("If the price of maize rises, what happens to the supply of wheat (assuming farmers can grow either crop)?", "Supply of wheat shifts left", ["Supply of wheat shifts right", "Quantity supplied of wheat rises", "Demand for wheat falls"], "Wheat and maize are in competitive supply; farmers switch land to the more profitable maize."),
         ("How does an indirect tax affect the supply curve?", "It shifts the supply curve upwards (to the left) by the amount of the tax", ["It shifts the demand curve to the left", "It causes a movement along the supply curve", "It shifts the supply curve downwards by the amount of the tax"], "A tax raises firms' costs per unit.")],
  why=[("Explain why an improvement in technology shifts the supply curve to the right.", "New technology raises productivity and lowers the cost per unit, so firms can profitably supply more at every price."),
       ("Explain why an expected rise in the future price of a good may reduce its supply today.", "If producers expect higher prices later (e.g. oil or grain), they may hold back stocks to sell later, reducing current supply at every price."),
       ("Explain why a rise in the price of beef could increase the supply of leather.", "Beef and leather are in joint supply: higher beef prices lead to more cattle being slaughtered, which automatically produces more hides, so leather supply shifts right.")],
  contrast=[("joint supply", "competitive supply", "In joint supply producing one good automatically produces another (beef and leather); in competitive supply resources can produce one good or another, so producing more of one means less of the other (wheat or maize)."),
            ("an indirect tax", "a subsidy", "An indirect tax raises firms' costs and shifts supply left/up; a subsidy lowers costs and shifts supply right/down.")],
  misc=[("A rise in demand for a good shifts its supply curve to the right.", "A rise in demand shifts the demand curve, leading to a higher price and a movement along the supply curve (more quantity supplied); the supply curve itself does not shift."),
        ("Higher wages for workers increase supply because firms have more motivated staff.", "Higher wages raise costs of production, which normally shifts supply to the left, unless productivity rises enough to offset them.")],
  apply=[("Avian flu led to the culling of over 40 million egg-laying hens in the US in 2022. Explain the effect on the market for eggs.", "A negative supply shock: supply shifts left, creating excess demand at the original price, so the equilibrium price rises (US egg prices more than doubled) and quantity falls.", 3),
         ("Explain the effect of a government subsidy on the supply of solar panels.", "The subsidy reduces firms' costs per unit, so supply shifts right (downwards by the subsidy); price falls and quantity rises.", 2)],
  cases=[("the 2021 frost in Brazil's coffee-growing regions", "Frosts and drought damaged coffee plants in Minas Gerais and arabica futures prices roughly doubled during 2021.", "a negative supply shock", "Lower harvests shifted world coffee supply left, raising price and reducing quantity."),
         ("the fall in the cost of solar panels", "The price of solar photovoltaic modules fell by around 90% between 2010 and 2020 as technology and economies of scale improved.", "technology as a non-price determinant of supply", "Lower production costs shifted supply to the right, lowering price and increasing the quantity of solar capacity installed.")],
  sources=[("Russia and Ukraine together accounted for about 30% of world wheat exports before 2022. After the invasion, Black Sea ports were blockaded and wheat prices on world markets rose to record highs in March 2022.", "Extract based on reporting of grain markets, 2022", "Using a supply and demand diagram and the extract, explain why world wheat prices rose.", "The blockade reduced the quantity of wheat available to world markets, shifting supply left; at the original price there was excess demand, so the equilibrium price rose and quantity traded fell.")],
  evaluate=[("Technological change is the most important determinant of supply in the long run.", ["technology lowers costs and shifts supply right permanently (solar panels, semiconductors)", "it explains falling real prices of manufactured goods"], ["input costs (energy, wages) drive many supply changes", "supply shocks (weather, war) dominate in agriculture", "government taxes, subsidies and regulation matter"], "In the long run technology is usually the dominant force, but in the short run costs, shocks and policy often matter more.")],
  extended=[("Using diagrams, explain the effect on the market for electric cars of (i) a fall in the cost of batteries and (ii) a new government tax on car production.", "(i) supply shifts right: lower price, higher quantity; (ii) supply shifts left by the tax per unit: higher price, lower quantity. Each diagram: P/Q axes, original S1 and new S2 with new equilibrium.", 6)],
  diag=[("the effect of a fall in the cost of an input on the market for a good such as bread", "Diagram: market for bread; fall in the price of flour lowers costs, shifting supply right from S1 to S2. At the original price there is excess supply; price falls from P1 to P2 and quantity rises from Q1 to Q2 along the demand curve."),
        ("the effect of a supply shock in a primary commodity market such as coffee", "Diagram: world coffee market; frost destroys crops, shifting supply left from S1 to S2. Excess demand at P1 pushes price up to P2; quantity falls from Q1 to Q2. With inelastic demand the price rise is large relative to the fall in quantity.")])


@R.add('ch05-st2', 'C2', (1, 3), 'mcq')
def supply_shift_mcq(rng, slot):
    cases = [("wages in the garment industry rise", "T-shirts", "Supply shifts left"), ("a new robot halves assembly time", "cars", "Supply shifts right"),
             ("the government introduces a per-unit subsidy", "organic vegetables", "Supply shifts right"), ("the government imposes a specific tax", "cigarettes", "Supply shifts left"),
             ("the price of the good itself rises", "rice", "Quantity supplied rises along the curve"), ("a hurricane destroys sugar cane fields", "sugar", "Supply shifts left"),
             ("many new firms enter the industry", "bubble tea", "Supply shifts right"), ("the price of maize rises (farmers can grow either crop)", "wheat", "Supply shifts left"),
             ("the price of beef rises", "leather", "Supply shifts right"), ("energy prices rise sharply", "aluminium", "Supply shifts left")]
    ev, g, ans = rng.choice(cases)
    pool = ["Supply shifts left", "Supply shifts right", "Quantity supplied rises along the curve", "Demand shifts right", "Demand shifts left"]
    pool = [p for p in pool if p != ans]
    rng.shuffle(pool)
    return mcq(rng, f'In the market for {g}, which of the following is the effect when {ev}, ceteris paribus?', ans, pool[:3], f'{ans}.')


S('ch05-st3',
  terms=[("linear supply function", "an equation of the form Qs = c + dP showing quantity supplied as a function of price; d is the change in Qs for each $1 change in price"),
         ("'c' term in Qs = c + dP", "the quantity supplied when price is zero (the Q-axis intercept); a change in c shifts the supply curve"),
         ("law of diminishing marginal returns", "as more units of a variable factor are added to a fixed factor in the short run, the marginal product of the variable factor eventually falls"),
         ("marginal product", "the extra output produced by employing one more unit of a variable factor such as labour"),
         ("short run", "the period in which at least one factor of production is fixed")],
  facts=[("For Qs = −20 + 4P, at what price does quantity supplied become positive?", "Above $5", ["Above $20", "Above $4", "Above $80"], "Qs = 0 when 4P = 20, so P = 5; above this firms supply positive quantities."),
         ("In Qs = c + dP, which change represents an increase in supply?", "An increase in c", ["A decrease in c", "An increase in P", "A decrease in d only"], "A higher c means more is supplied at every price: the curve shifts right."),
         ("Diminishing marginal returns explains which of the following?", "Why short-run marginal cost eventually rises, giving an upward-sloping supply curve", ["Why long-run average costs fall", "Why demand curves slope downwards", "Why firms experience economies of scale"], "Falling marginal product of labour means each extra unit of output needs more labour, so marginal cost rises.")],
  why=[("Explain the link between diminishing marginal returns and the upward slope of the supply curve.", "In the short run, adding workers to fixed capital eventually reduces marginal product, so the cost of each extra unit (marginal cost) rises; firms therefore need a higher price to supply more."),
       ("Explain why a specific tax changes the supply function Qs = c + dP to Qs = c + d(P − t).", "With a tax of t per unit, producers receive only P − t per unit, so they supply the quantity that corresponds to the net price; the curve shifts upward by t."),
       ("Explain why diminishing returns only occur in the short run.", "They arise because at least one factor is fixed; in the long run all factors can be varied, so the firm can expand capital along with labour.")],
  contrast=[("diminishing marginal returns", "diseconomies of scale", "Diminishing returns is a short-run concept: adding a variable factor to a fixed factor reduces marginal product. Diseconomies of scale are a long-run concept: average costs rise as the scale of all inputs increases."),
            ("marginal product", "average product", "Marginal product is the extra output from one more worker; average product is total output divided by the number of workers.")],
  misc=[("Diminishing marginal returns means total output falls when more workers are hired.", "Diminishing marginal returns means each extra worker adds less output than the previous one; total output still rises as long as marginal product is positive."),
        ("In Qs = c + dP, a larger d shifts the supply curve to the right.", "d affects the slope (responsiveness of quantity supplied to price); a change in c shifts the curve.")],
  apply=[("A supply function is Qs = −30 + 6P. Calculate quantity supplied at a price of $15 and the minimum price at which firms will supply.", "Qs = −30 + 90 = 60; minimum price where Qs = 0: P = $5.", 2)],
  cases=[("a family farm in Kenya adding workers to a fixed plot of land", "With a fixed area of land, the first few extra workers greatly increase the tea harvest, but later workers add less because the land becomes crowded.", "the law of diminishing marginal returns", "Each extra worker has less land to work with, so marginal product falls even though total output rises.")],
  evaluate=[("The law of diminishing marginal returns is unimportant for modern firms that rely on technology.", ["technology firms (software) have very low marginal costs", "firms can quickly add capital in the cloud"], ["most firms still have fixed factors in the short run (factories, land)", "agriculture, manufacturing and services face capacity limits", "it explains rising short-run marginal costs and upward-sloping supply"], "Diminishing returns still applies wherever a factor is fixed in the short run; digital goods are an important but limited exception.")],
  extended=[("A supply function changes from Qs = −40 + 5P to Qs = −10 + 5P. Explain what might have caused this, calculate the change in quantity supplied at a price of $12 and describe the change on a diagram.", "c rose from −40 to −10: e.g. lower input costs or better technology; at P = 12, Qs rises from 20 to 50 (+30); parallel shift of the supply curve to the right; price intercept falls from $8 to $2.", 6)],
  diag=[("how the law of diminishing marginal returns leads to an upward-sloping short-run supply curve", "Diagram 1: output (vertical) against number of workers (horizontal), total product rising at a decreasing rate after a point; marginal product rising then falling. Diagram 2: upward-sloping supply/marginal cost curve: as marginal product falls, marginal cost rises, so higher prices are needed for firms to supply more.")])


@R.add('ch05-st3', 'C3', (1, 5), 'numerical')
def lin_supply(rng, slot):
    d = rng.choice([2, 3, 4, 5, 6, 10])
    pmin = rng.choice([2, 3, 4, 5, 6, 8])
    c = -d * pmin
    g = rng.choice(GOODS)
    city = rng.choice(CITIES)
    if slot.d <= 2:
        P = rng.randint(pmin + 1, pmin + 20)
        return dict(stem=rng.choice([f'The supply of {g} in {city} is given by {lin_s(c, d)}. Calculate quantity supplied at a price of ${P}.',
                                     f'Producers of {g} near {city} have the supply function {lin_s(c, d)}. How much is supplied when the price is ${P}?']),
                    answer=str(c + d * P), markingKey=f'Qs = {c} + {d} × {P} = {c + d * P}. [1] [1]', type='numerical', marks=2)
    t = rng.choice([1, 2, 3])
    P = rng.randint(pmin + t + 2, pmin + 20)
    return dict(stem=f'The supply function for {g} in {city} is {lin_s(c, d)}. (a) State the minimum price at which firms supply. (b) A specific tax of ${t} per unit is imposed on producers. Write the new supply function and calculate quantity supplied at a market price of ${P}.',
                answer=f'(a) ${pmin}; (b) {lin_s(c - d * t, d)} (from Qs = −{-c} + {d}(P − {t})); Qs = {c + d * (P - t)} at ${P}',
                markingKey=f'(a) −{-c} + {d}P = 0 ⇒ P = {pmin} [1]. (b) Producers receive P − {t}: Qs = −{-c} + {d}(P − {t}) = {lin_s(c - d * t, d)[5:]} [2]; at P = {P}: −{d * t - c} + {d * P} = {c + d * (P - t)} [1].', type='numerical', marks=4)


@R.add('ch05-st3', 'C3', (2, 5), 'numerical')
def dim_returns(rng, slot):
    for _ in range(50):
        mps = [rng.randint(6, 12)]
        mps.append(mps[0] + rng.randint(2, 8))
        mps.append(mps[1] + rng.randint(0, 4))
        k = 3
        while len(mps) < 6:
            mps.append(max(0, mps[-1] - rng.randint(2, 7)))
        if len(set(mps)) >= 5:
            break
    tps = []
    s = 0
    for m in mps:
        s += m
        tps.append(s)
    peak = max(range(6), key=lambda i: mps[i])
    ctx = rng.choice(['a bakery with two ovens', 'a rice farm with a fixed area of land', 'a call centre with 4 desks', 'a car-wash with one washing bay', 'a tailoring workshop with three sewing machines'])
    tab = ', '.join(f'{i + 1} worker{"s" if i else ""}: {tps[i]}' for i in range(6))
    return dict(stem=f'The table shows total output per day for {ctx}: {tab}. Calculate the marginal product of each worker and identify the worker after which diminishing marginal returns set in.',
                answer=f'MP: {", ".join(map(str, mps))}; diminishing returns set in after worker {peak + 1}',
                markingKey=f'MP = change in total product: {", ".join(map(str, mps))} [2]; MP is highest for worker {peak + 1} and falls thereafter, so diminishing marginal returns begin after worker {peak + 1} [1]; caused by the fixed factor [1].', type='numerical', marks=4)

# =============================================================================================
# ch06 Unit 2.3 Competitive market equilibrium
# =============================================================================================
S('ch06-st1',
  terms=[("market equilibrium", "the situation where quantity demanded equals quantity supplied, so there is no tendency for price to change"),
         ("excess demand (shortage)", "a situation where quantity demanded exceeds quantity supplied at the current price, putting upward pressure on price"),
         ("excess supply (surplus)", "a situation where quantity supplied exceeds quantity demanded at the current price, putting downward pressure on price"),
         ("market-clearing price", "the equilibrium price at which all the units that producers want to sell are bought"),
         ("competitive market", "a market with many buyers and sellers, none of whom can influence the price")],
  facts=[("If the price of a good is above the equilibrium price, which of the following occurs?", "Excess supply, which puts downward pressure on price", ["Excess demand, which puts upward pressure on price", "A shift of the demand curve to the right", "Equilibrium in the market"], "At a price above equilibrium Qs > Qd; firms cut prices to sell unsold stock."),
         ("At a price of $6, Qd = 400 and Qs = 250. Which of the following describes the market?", "Excess demand of 150 units", ["Excess supply of 150 units", "Equilibrium", "Excess demand of 650 units"], "Qd − Qs = 400 − 250 = 150 units of shortage."),
         ("Which of the following brings a market back to equilibrium when there is excess demand?", "A rise in price that reduces quantity demanded and increases quantity supplied", ["A fall in price", "A shift of the supply curve to the left", "A shift of the demand curve to the right"], "Price rises, moving along both curves until Qd = Qs.")],
  why=[("Explain how a market with excess supply moves to equilibrium.", "Firms cannot sell all their output at the current price, so they cut prices; as price falls, quantity demanded rises and quantity supplied falls (movements along the curves) until Qd = Qs at the equilibrium price."),
       ("Explain why there is no tendency for price to change at equilibrium.", "At equilibrium every buyer willing to pay the price can buy and every seller willing to sell can sell; there is no shortage to push price up or surplus to push it down."),
       ("Explain why queues and empty shelves suggest that a price is below equilibrium.", "Queues show that quantity demanded exceeds quantity supplied at the current price (excess demand); in a free market price would rise to ration the good.")],
  contrast=[("excess demand", "excess supply", "Excess demand occurs below equilibrium, where Qd > Qs, and pushes price up; excess supply occurs above equilibrium, where Qs > Qd, and pushes price down."),
            ("a shortage", "scarcity", "A shortage is a temporary market condition where Qd > Qs at a given price; scarcity is the permanent condition that resources are limited relative to wants.")],
  misc=[("When there is excess demand, the demand curve shifts left until the market clears.", "Excess demand is removed by a rise in price, which causes movements along the demand and supply curves; neither curve shifts."),
        ("At equilibrium every consumer who wants the good gets it.", "At equilibrium every consumer willing and able to pay the equilibrium price can buy; those unwilling or unable to pay do not.")],
  apply=[("Tickets for a stadium concert in Seoul are priced at ₩150,000, but within minutes all are sold and resale sites list them at ₩600,000. Explain this using the concept of equilibrium.", "The official price is below equilibrium, so there is excess demand; resale prices rise towards the market-clearing level where quantity demanded equals the fixed quantity of seats.", 3)],
  cases=[("the shortage of PlayStation 5 consoles in 2020-2021", "Sony's launch price was fixed while supply was limited by chip shortages; consoles sold out instantly and resold online at far higher prices.", "excess demand", "At the fixed launch price Qd far exceeded Qs, so resale prices rose towards the market-clearing level.")],
  sources=[("Hypothetical market data for mangoes in Accra (per week): at GH₵10 per kg, Qd = 900 kg and Qs = 300 kg; at GH₵15, Qd = 700 kg and Qs = 500 kg; at GH₵20, Qd = 600 kg and Qs = 600 kg; at GH₵25, Qd = 500 kg and Qs = 700 kg.", "Hypothetical data", "Using the data, identify the equilibrium price and quantity and describe the market situation at GH₵10.", "Equilibrium: GH₵20 and 600 kg (Qd = Qs). At GH₵10 there is excess demand of 600 kg (900 − 300), so price will rise.")],
  evaluate=[("Markets always move quickly to equilibrium.", ["excess demand and supply create strong price pressures", "online markets adjust prices instantly (dynamic pricing)"], ["prices can be sticky (menus, contracts, social norms – concert tickets)", "government price controls prevent adjustment", "information is imperfect and expectations may destabilise prices (housing)"], "Many markets adjust quickly, but stickiness, regulation and imperfect information mean disequilibrium can persist.")],
  extended=[("Using a diagram, explain how the price mechanism eliminates a surplus in the market for apples after an unusually large harvest.", "The large harvest shifts supply right; at the original price Qs > Qd; sellers cut prices to clear stock; as price falls, quantity demanded rises and quantity supplied falls along S2 until a new, lower equilibrium price is reached with higher quantity.", 6)],
  diag=[("how excess demand and excess supply are eliminated in a competitive market", "Diagram: downward-sloping D and upward-sloping S intersecting at Pe, Qe. At P1 above Pe, Qs > Qd: excess supply; sellers cut prices, moving along both curves to Pe. At P2 below Pe, Qd > Qs: excess demand; buyers bid up price to Pe. At Pe, Qd = Qs and the market clears.")])


@R.add('ch06-st1', 'C3', (1, 5), 'numerical')
def excess(rng, slot):
    m = market(rng)
    if not m:
        return None
    a, b, c, d, P, Q = m
    intro, g = mkt_intro(rng, a, b, c, d)
    p0 = P + rng.choice([-3, -2, -1, 1, 2, 3, 4])
    if p0 <= 0:
        return None
    qd, qs = a - b * p0, c + d * p0
    if qd < 0 or qs < 0:
        return None
    kind = 'excess demand (shortage)' if qd > qs else 'excess supply (surplus)'
    if slot.d <= 2:
        return dict(stem=f'{intro} Calculate the quantity demanded and quantity supplied at a price of ${p0} and state the market situation.',
                    answer=f'Qd = {qd}, Qs = {qs}: {kind} of {abs(qd - qs)}', markingKey=f'Qd = {a} − {b}×{p0} = {qd}; Qs = {c} + {d}×{p0} = {qs} [1]; {kind} of {abs(qd - qs)} [1].', type='numerical', marks=2)
    return dict(stem=f'{intro} The price is currently ${p0}. Calculate the size of the {"shortage" if qd > qs else "surplus"} and explain how the market will adjust to equilibrium, stating the equilibrium price and quantity.',
                answer=f'{kind} of {abs(qd - qs)}; equilibrium P = ${P}, Q = {Q}',
                markingKey=f'Qd = {qd}, Qs = {qs}, difference {abs(qd - qs)} [1]; {"price rises" if qd > qs else "price falls"}, causing movements along both curves [1]; {a} − {b}P = {c} + {d}P ⇒ P = {P} [1], Q = {Q} [1].', type='numerical', marks=4)


S('ch06-st2',
  terms=[("change in equilibrium", "a movement to a new equilibrium price and quantity caused by a shift in demand, supply or both"),
         ("comparative statics", "comparing the original and the new equilibrium after a change, without analysing the path between them"),
         ("simultaneous shifts", "a situation where demand and supply both shift, so the effect on either price or quantity is indeterminate unless the sizes of the shifts are known")],
  facts=[("If demand increases and supply is unchanged, which of the following occurs?", "Equilibrium price and quantity both rise", ["Price rises and quantity falls", "Price falls and quantity rises", "Both fall"], "A rightward demand shift creates excess demand at the original price; price and quantity rise."),
         ("If supply increases and demand decreases at the same time, what can be predicted?", "Price falls; the change in quantity is uncertain", ["Price rises; quantity falls", "Quantity rises; price is uncertain", "Both price and quantity fall"], "Both shifts lower price; their effects on quantity work in opposite directions."),
         ("A fall in supply with unchanged demand causes which of the following?", "A rise in price and a fall in quantity", ["A fall in price and a rise in quantity", "A rise in both price and quantity", "No change in price"], "Leftward supply shift: excess demand at the original price."),
         ("If demand and supply both increase, which of the following is certain?", "Equilibrium quantity rises", ["Equilibrium price rises", "Equilibrium price falls", "Equilibrium quantity falls"], "Both shifts raise quantity; the effect on price depends on the relative sizes of the shifts.")],
  why=[("Explain why an increase in both demand and supply has an uncertain effect on price.", "The demand increase pushes price up while the supply increase pushes it down; the net effect depends on which shift is larger."),
       ("Explain why a fall in the price of a substitute reduces both the equilibrium price and quantity of a good.", "Consumers switch to the cheaper substitute, so demand for the good shifts left; at the original price there is excess supply, and price and quantity fall to a new equilibrium."),
       ("Explain why a new tax on producers leads to a rise in price that is smaller than the tax (with a normal demand curve).", "The tax shifts supply up by the tax amount; as price rises quantity demanded falls, so the new equilibrium price rises by less than the tax because part of the tax is absorbed by producers.")],
  contrast=[("a rise in demand", "a fall in supply", "Both raise the equilibrium price, but a rise in demand increases equilibrium quantity while a fall in supply reduces it."),
            ("a shift of the demand curve", "a movement along the demand curve", "A shift is caused by a non-price determinant and changes the quantity demanded at every price; a movement along the curve is caused by a change in price, for example when supply shifts.")],
  misc=[("If supply falls, price rises, which then reduces demand, so the demand curve shifts left.", "A higher price reduces quantity demanded – a movement along the demand curve; demand (the curve) does not shift because of a change in the good's own price."),
        ("When demand rises, supply rises too because firms see more customers.", "Firms respond to the higher price by increasing quantity supplied – a movement along the supply curve; supply itself does not shift.")],
  apply=[("A health report links a popular energy drink to heart problems while the price of its main ingredient falls. Predict the effect on equilibrium price and quantity.", "Demand shifts left and supply shifts right: price falls for certain; the effect on quantity is uncertain, depending on the sizes of the shifts.", 3),
         ("Explain the effect on the market for umbrellas in London of an unusually wet summer.", "Demand for umbrellas shifts right (change in conditions/tastes), so equilibrium price and quantity rise.", 2)],
  cases=[("the 2022 surge in natural gas prices in Europe", "Russia cut pipeline gas deliveries to Europe and European gas prices rose to many times their previous level.", "the effect of a fall in supply on equilibrium", "Supply shifted left while demand was inelastic, so the equilibrium price rose sharply and quantity fell modestly."),
         ("the boom in demand for face masks in early 2020", "Demand for masks rose suddenly; initially prices soared, but over the following months manufacturers in China expanded capacity enormously.", "changes in equilibrium from shifts in both demand and supply", "First demand shifted right (higher price and quantity); later supply shifted right, lowering price while quantity rose further.")],
  sources=[("In 2023 the world price of olive oil reached a record high of over €8,000 per tonne after two years of drought in Spain, which produces around 40% of the world's olive oil. Meanwhile, rising interest in the Mediterranean diet continued to increase demand in Asia and North America.", "Extract based on reporting of the olive oil market", "Using a diagram, explain the changes in the olive oil market described in the extract.", "Drought shifted supply left and rising health-driven demand shifted demand right; both raise price, so the equilibrium price rose sharply; the effect on quantity is uncertain (likely fell given the large supply shock).")],
  evaluate=[("Supply and demand analysis can accurately predict changes in the prices of primary commodities.", ["shows the direction of price changes after shocks", "explains volatility when demand and supply are inelastic"], ["many shifts happen at once and are hard to measure", "speculation and expectations move prices", "government stockpiles and export bans interfere"], "The model predicts the direction of changes well but rarely the size, because many simultaneous influences act on commodity markets.")],
  extended=[("Using diagrams, explain the likely effects on the market for beef of (i) a rise in the price of cattle feed and (ii) growing popularity of plant-based burgers, occurring at the same time.", "(i) supply shifts left; (ii) demand shifts left. Quantity falls for certain; price change depends on relative shifts. Draw D1/D2 and S1/S2 with new equilibrium.", 6)],
  diag=[("the effect on equilibrium price and quantity of an increase in demand combined with a decrease in supply", "Diagram: D1, S1 intersect at P1, Q1. Demand shifts right to D2 and supply shifts left to S2; the new equilibrium P2 is clearly higher. Quantity may rise, fall or stay the same depending on the relative size of the shifts – the diagram should show one case and note the ambiguity."),
        ("the effect of a fall in the price of a complement on the equilibrium of a market such as gaming headsets", "Diagram: a fall in the price of consoles increases their quantity demanded, so demand for headsets shifts right from D1 to D2; excess demand at P1 pushes price up to P2 and quantity rises from Q1 to Q2 along S.")])


@R.add('ch06-st2', 'C3', (2, 5), 'numerical')
def new_eq(rng, slot):
    m = market(rng)
    if not m:
        return None
    a, b, c, d, P, Q = m
    for _ in range(30):
        da = rng.choice([1, -1]) * (b + d) * rng.randint(1, 4)
        if a + da > 0:
            break
    a2 = a + da
    P2 = (a2 - c) / (b + d)
    Q2 = c + d * P2
    if Q2 <= 0 or P2 <= 0:
        return None
    intro, g = mkt_intro(rng, a, b, c, d)
    cause = rng.choice(['a rise in consumer incomes', 'a successful advertising campaign', 'a rise in the price of a substitute']) if da > 0 else rng.choice(['a fall in the price of a substitute', 'a health scare', 'a fall in consumer incomes'])
    return dict(stem=f'{intro} Following {cause}, the demand function becomes {lin_d(a2, b)}. Calculate the original and new equilibrium price and quantity, and comment on the direction of change.',
                answer=f'Original P = ${P}, Q = {Q}; new P = ${fmt(P2)}, Q = {fmt(Q2)}',
                markingKey=f'Original: {a} − {b}P = {lin_s(c, d)[5:]} ⇒ P = {P}, Q = {Q} [1]; new: P = ({a2} − ({c}))/{b + d} = {fmt(P2)}, Q = {fmt(Q2)} [2]; demand {"increase raises" if da > 0 else "decrease lowers"} both price and quantity [1].', type='numerical', marks=4)


S('ch06-st3',
  terms=[("price mechanism", "the system in which the interaction of demand and supply determines prices, which then allocate resources through their signalling, incentive and rationing functions"),
         ("signalling function of price", "the role of price changes in conveying information to buyers and sellers about where resources are wanted"),
         ("incentive function of price", "the role of price changes in motivating producers and consumers to change their behaviour, for example to supply more when price rises"),
         ("rationing function of price", "the role of price in allocating scarce goods to those willing and able to pay"),
         ("allocative efficiency", "the allocation of resources that maximises social surplus, achieved when the price consumers pay equals the marginal cost of production (MB = MC)")],
  facts=[("Which of the following is the incentive function of price?", "A higher price encourages firms to produce more because it is more profitable", ["A higher price tells consumers a good is scarce", "A higher price ensures only those who can pay obtain the good", "A lower price reduces producers' profits"], "Prices motivate behaviour: higher prices reward extra production."),
         ("In a competitive market without externalities, allocative efficiency is achieved where which of the following holds?", "Marginal benefit equals marginal cost", ["Total revenue is maximised", "Price is as low as possible", "Producer surplus is maximised"], "At MB = MC, social surplus is maximised."),
         ("Which of the following best describes the rationing function of price?", "Higher prices limit purchases of a scarce good to those most willing and able to pay", ["Prices signal where resources are needed", "Prices give firms an incentive to innovate", "Prices are set by governments to share goods fairly"], "When a good becomes scarcer, rising price reduces quantity demanded.")],
  why=[("Explain how the price mechanism reallocates resources when consumer tastes shift from beef towards plant-based foods.", "Demand for plant-based foods rises and for beef falls; prices rise in one market and fall in the other (signal); higher profits attract resources into plant-based production while losses push resources out of beef (incentive)."),
       ("Explain why allocative efficiency occurs at the competitive market equilibrium.", "At equilibrium the demand curve (marginal benefit) meets the supply curve (marginal cost), so the last unit produced is valued exactly at its cost; producing less or more would reduce social surplus."),
       ("Explain why the price mechanism might be considered an 'invisible hand'.", "Without central direction, self-interested buyers and sellers respond to prices; this coordinates millions of decisions and allocates resources to their most valued uses, as Adam Smith described.")],
  contrast=[("the signalling function", "the incentive function", "The signalling function is the information prices convey about scarcity and demand; the incentive function is the motivation prices give producers and consumers to change behaviour."),
            ("allocative efficiency", "productive efficiency", "Allocative efficiency means producing the combination of goods society values most (MB = MC); productive efficiency means producing at the lowest possible cost (on the PPC / minimum average cost).")],
  misc=[("The price mechanism ensures goods go to those who need them most.", "Price allocates goods to those most willing and able to pay, which depends on income; those in greatest need may be unable to pay, which is why governments intervene for equity."),
        ("Allocative efficiency means consumers pay the lowest possible price.", "Allocative efficiency means resources produce what society values most, where MB = MC; the price is the market price at that point, not the lowest possible price.")],
  apply=[("Explain how rising lithium prices between 2020 and 2022 illustrate the signalling and incentive functions of price.", "The price rise signalled that lithium was increasingly scarce relative to demand from battery makers; higher profits gave mining firms the incentive to open new mines in Australia, Chile and Argentina, increasing quantity supplied.", 3)],
  cases=[("dynamic 'surge pricing' by ride-hailing apps such as Uber", "When demand rises at peak times or in bad weather, prices rise automatically; more drivers go online and some passengers wait or travel another way.", "the rationing and incentive functions of price", "Higher prices ration rides to those who value them most and give drivers an incentive to supply more rides.")],
  evaluate=[("The price mechanism is the most efficient way to allocate scarce resources.", ["prices coordinate decentralised information (Hayek)", "incentives encourage efficiency and innovation", "maximises social surplus in competitive markets without externalities"], ["market failure: externalities, public goods, information problems", "inequitable outcomes – rationing by ability to pay", "market power distorts prices"], "The price mechanism is efficient in competitive markets without market failure, but in many important markets intervention is needed for efficiency and equity.")],
  extended=[("Explain how the price mechanism would respond if a disease sharply reduced the global supply of bananas, referring to the signalling, incentive and rationing functions.", "Supply falls, price rises; signal: bananas are scarcer; rationing: higher price reduces quantity demanded to the limited supply; incentive: producers invest in disease-resistant varieties and new plantations, and consumers switch to substitutes.", 6)],
  diag=[("how the price mechanism reallocates resources in response to an increase in demand, using the signalling and incentive functions of price", "Diagram: D1 shifts right to D2; excess demand at P1; price rises to P2 (signal of scarcity); higher price makes production more profitable, so firms increase quantity supplied along S from Q1 to Q2 (incentive); the higher price also rations the good to those willing and able to pay.")])


S('ch06-st4',
  terms=[("consumer surplus", "the difference between the highest price consumers are willing to pay and the price they actually pay, shown by the area below the demand curve and above the price"),
         ("producer surplus", "the difference between the price producers receive and the lowest price they would accept, shown by the area above the supply curve and below the price"),
         ("social (community) surplus", "the sum of consumer surplus and producer surplus, maximised at the competitive equilibrium when there are no externalities"),
         ("welfare loss (deadweight loss)", "the loss of social surplus that results when output is not at the allocatively efficient level")],
  facts=[("On a demand and supply diagram, where is consumer surplus shown?", "The area below the demand curve and above the market price", ["The area above the supply curve and below the market price", "The area under the supply curve", "The area between the two curves to the right of equilibrium"], "Consumers value those units more than they pay."),
         ("A consumer is willing to pay $50 for a concert ticket and buys it for $35. What is her consumer surplus?", "$15", ["$35", "$50", "$85"], "Willingness to pay minus price: 50 − 35 = 15."),
         ("When is social surplus maximised in a competitive market without externalities?", "At the equilibrium quantity", ["At the highest possible price", "At the quantity where consumer surplus is zero", "At any quantity above equilibrium"], "At equilibrium, marginal benefit equals marginal cost.")],
  why=[("Explain why producing more than the equilibrium quantity reduces social surplus.", "Beyond equilibrium, the cost of each extra unit (supply curve) exceeds the benefit consumers gain from it (demand curve); producing these units subtracts from social surplus, creating a welfare loss."),
       ("Explain why consumer surplus rises when the market price falls.", "Existing consumers pay less for units they were already buying, and new consumers enter the market who now gain surplus on extra units; the area below demand and above price grows."),
       ("Explain why producer surplus exists for most firms in a market.", "The supply curve reflects firms' marginal costs; firms with lower costs would have accepted less than the market price, so they receive more than their minimum acceptable price on many units.")],
  contrast=[("consumer surplus", "producer surplus", "Consumer surplus is the benefit to buyers above what they pay (below demand, above price); producer surplus is the benefit to sellers above their minimum acceptable price (above supply, below price)."),
            ("social surplus", "welfare loss", "Social surplus is the total benefit to society from producing and consuming a good (CS + PS); welfare loss is the part of potential social surplus lost when output is not at the efficient level.")],
  misc=[("Consumer surplus is the money consumers save in a sale.", "Consumer surplus is the difference between willingness to pay and the price paid, measured across all units bought, whether or not there is a sale."),
        ("Social surplus is maximised when consumer surplus is maximised.", "Social surplus is the sum of consumer and producer surplus, maximised at the competitive equilibrium; maximising consumer surplus alone (e.g. a very low price) would reduce output and producer surplus.")],
  apply=[("Five consumers are willing to pay $12, $10, $8, $6 and $4 for one unit each of a good selling at $7. Calculate total consumer surplus.", "Three buy (12, 10, 8): CS = 5 + 3 + 1 = $9.", 2)],
  cases=[("Taylor Swift's Eras Tour ticket sales in 2023", "Face-value tickets were far below what many fans were willing to pay, and resale prices on secondary markets reached thousands of dollars.", "consumer surplus", "Fans who bought at face value gained very large consumer surplus; resellers captured part of it by charging prices closer to willingness to pay.")],
  evaluate=[("Maximising social surplus should be the main goal of economic policy in every market.", ["allocative efficiency maximises total welfare", "a clear, measurable benchmark for policy"], ["ignores the distribution between consumers and producers (equity)", "the market equilibrium is not efficient when there are externalities", "surplus measures depend on ability to pay, giving more weight to the rich"], "Social surplus is a useful efficiency benchmark, but policy also needs to consider equity and external effects.")],
  extended=[("Using a diagram, explain the effect on consumer surplus, producer surplus and social surplus of an increase in supply resulting from new technology.", "Supply shifts right; price falls, quantity rises; consumer surplus increases (larger triangle below D above the lower price); producer surplus changes (may rise as quantity rises); social surplus rises because the efficient output is larger.", 6)],
  diag=[("consumer surplus, producer surplus and social surplus at the competitive market equilibrium", "Diagram: D and S intersect at Pe, Qe. Consumer surplus: triangle between D and the line Pe, up to Qe. Producer surplus: triangle between Pe and S, up to Qe. Together they form social surplus, which is maximised at Qe where MB (demand) = MC (supply), so the outcome is allocatively efficient.")])


@R.add('ch06-st4', 'C3', (2, 5), 'numerical')
def surplus(rng, slot):
    m = market(rng)
    if not m:
        return None
    a, b, c, d, P, Q = m
    pmax = a / b
    pmin = -c / d
    cs = 0.5 * (pmax - P) * Q
    ps = 0.5 * (P - pmin) * Q
    intro, g = mkt_intro(rng, a, b, c, d)
    if slot.d <= 3:
        which = rng.choice(['consumer', 'producer'])
        v = cs if which == 'consumer' else ps
        return dict(stem=f'{intro} The equilibrium price is ${P} and quantity {Q}. Calculate {which} surplus.',
                    answer=fmt(v, 6), markingKey=(f'Demand meets the price axis at {fmt(pmax)}; CS = ½ × ({fmt(pmax)} − {P}) × {Q} = {fmt(cs, 6)}. [1] intercept [1] area' if which == 'consumer' else
                                               f'Supply meets the price axis at {fmt(pmin)}; PS = ½ × ({P} − {fmt(pmin)}) × {Q} = {fmt(ps, 6)}. [1] intercept [1] area'), type='numerical', marks=2)
    return dict(stem=f'{intro} Calculate the equilibrium price and quantity, consumer surplus, producer surplus and social surplus (in the units of the data).',
                answer=f'P = {P}, Q = {Q}; CS = {fmt(cs, 6)}; PS = {fmt(ps, 6)}; social surplus = {fmt(cs + ps, 6)}',
                markingKey=f'Equilibrium P = {P}, Q = {Q} [1]; CS = ½({fmt(pmax)} − {P})({Q}) = {fmt(cs, 6)} [1]; PS = ½({P} − {fmt(pmin)})({Q}) = {fmt(ps, 6)} [1]; total {fmt(cs + ps, 6)} [1].', type='numerical', marks=4)


S('ch06-st5',
  terms=[("equilibrium condition", "Qd = Qs; with linear functions a − bP = c + dP, so P* = (a − c)/(b + d)"),
         ("simultaneous equations", "two equations solved together to find the price and quantity at which both demand and supply hold"),
         ("quantity of excess demand", "Qd − Qs at a price below equilibrium, calculated by substituting the price into both functions"),
         ("graphing linear functions", "plotting demand and supply equations by calculating their intercepts and at least one other point, with price on the vertical axis")],
  facts=[("Qd = 100 − 2P and Qs = −20 + 4P. What is the equilibrium price?", "$20", ["$40", "$30", "$13.33"], "100 − 2P = −20 + 4P ⇒ 120 = 6P ⇒ P = 20."),
         ("Qd = 60 − 3P and Qs = 2P. What is the equilibrium quantity?", "24", ["12", "36", "60"], "60 − 3P = 2P ⇒ P = 12; Q = 2 × 12 = 24."),
         ("If Qd = 200 − 5P and Qs = 20 + 4P, what is the market situation at P = $10?", "Excess demand of 90 units", ["Excess supply of 90 units", "Equilibrium", "Excess demand of 150 units"], "Qd = 150, Qs = 60 ⇒ shortage of 90.")],
  why=[("Explain why the equilibrium price is found by setting Qd equal to Qs.", "Equilibrium is where the quantity consumers want to buy equals the quantity firms want to sell; only at that price is there no excess demand or supply."),
       ("Explain why it is good practice to check an equilibrium calculation by substituting the price into both functions.", "Both functions must give the same quantity at the equilibrium price; if they do not, an arithmetic error has been made."),
       ("Explain how a parallel rightward shift in demand changes the equilibrium calculated from linear functions.", "The constant 'a' rises, so (a − c)/(b + d) rises: equilibrium price increases and, substituting into the supply function, quantity increases too.")],
  contrast=[("solving for equilibrium algebraically", "finding equilibrium from a graph", "Algebra gives an exact solution from the functions; a graph shows the intersection visually but may be imprecise. Both should agree."),
            ("the demand function", "the inverse demand function", "The demand function gives Q in terms of P (Qd = a − bP); the inverse demand function gives P in terms of Q (P = a/b − Q/b), which is what is plotted with price on the vertical axis.")],
  misc=[("To find equilibrium quantity, substitute the equilibrium price into the demand function only, because supply does not matter.", "Either function gives the same quantity at equilibrium; substituting into both is a useful check, and supply matters as much as demand in finding the price."),
        ("If Qd = 50 − P and Qs = 2P, the equilibrium price is $50 because quantity demanded is zero there.", "$50 is the price intercept of demand; equilibrium is where 50 − P = 2P, so P = $16.67 and Q = 33.3.")],
  apply=[("Demand is Qd = 400 − 10P and supply is Qs = 100 + 5P. Calculate equilibrium price and quantity.", "400 − 10P = 100 + 5P ⇒ 300 = 15P ⇒ P = $20; Q = 200.", 2)],
  cases=[("estimating the effect of a new low-cost airline route", "An airport authority estimates linear demand and supply for seats on a route to forecast price and passenger numbers when a new airline enters.", "calculating equilibrium from linear functions", "Entry adds to supply (raising c), so solving the new equations predicts a lower fare and more passengers.")],
  evaluate=[("Calculating equilibrium from linear functions gives policy makers reliable predictions.", ["exact numerical answers", "allows testing of policies such as taxes and subsidies before introducing them"], ["functions are estimates with error", "relationships may be non-linear", "other factors change at the same time"], "Linear models are useful for direction and approximate size, but forecasts must be treated as estimates and tested against outcomes.")],
  extended=[("Given Qd = 240 − 6P and Qs = −60 + 4P, calculate the equilibrium, then calculate the new equilibrium if a subsidy shifts supply to Qs = −20 + 4P, and explain the change.", "Original: 300 = 10P ⇒ P = 30, Q = 60. New: 260 = 10P ⇒ P = 26, Q = 84. Supply increase lowers price by $4 and raises quantity by 24.", 6)],
  diag=[("how to plot the linear functions Qd = 120 − 4P and Qs = −30 + 6P and identify the equilibrium", "Diagram: P on the vertical axis; demand meets Q axis at 120 and P axis at 30; supply meets P axis at 5 and passes through (Q = 30, P = 10). They intersect where 120 − 4P = −30 + 6P: P = 15, Q = 60. Label Pe = 15, Qe = 60.")])


@R.add('ch06-st5', 'C3', (1, 5), 'numerical')
def equilibrium(rng, slot):
    m = market(rng, need_cneg=False)
    if not m:
        return None
    a, b, c, d, P, Q = m
    intro, g = mkt_intro(rng, a, b, c, d)
    if slot.d <= 2:
        return dict(stem=f'{intro} Calculate the equilibrium price.', answer=f'${P}',
                    markingKey=f'{a} − {b}P = {c} + {d}P ⇒ {a - c} = {b + d}P ⇒ P = {P}. [1] equating [1] answer.', type='numerical', marks=2)
    if slot.d == 3:
        return dict(stem=f'{intro} Calculate the equilibrium price and quantity.', answer=f'P = ${P}, Q = {Q}',
                    markingKey=f'{a} − {b}P = {c} + {d}P [1]; P = {a - c}/{b + d} = {P} [1]; Q = {a} − {b}×{P} = {Q} [1]; check with supply: {c} + {d}×{P} = {Q} [1].', type='numerical', marks=4)
    k = rng.choice([b + d, 2 * (b + d), 3 * (b + d)])
    c2 = c - k
    P2 = (a - c2) / (b + d)
    Q2 = a - b * P2
    return dict(stem=f'{intro} A rise in the cost of raw materials changes supply to {lin_s(c2, d)}. Calculate the equilibrium before and after the change and the change in total consumer expenditure.',
                answer=f'Before P = ${P}, Q = {Q}; after P = ${fmt(P2)}, Q = {fmt(Q2)}; expenditure changes from {P * Q} to {fmt(P2 * Q2, 6)}',
                markingKey=f'Before: P = {P}, Q = {Q} [1]; after: P = ({a} − ({c2}))/{b + d} = {fmt(P2)}, Q = {fmt(Q2)} [2]; expenditure P×Q: {P * Q} → {fmt(P2 * Q2, 6)} (change {fmt(P2 * Q2 - P * Q, 6)}) [1].', type='numerical', marks=4)

# =============================================================================================
# ch07 Unit 2.4 Critique of the maximising behaviour of consumers and producers
# =============================================================================================
S('ch07-st1',
  terms=[("rational consumer choice", "the assumption that consumers make choices that maximise their utility, given their preferences, incomes and prices"),
         ("utility maximisation", "the assumption that consumers aim to gain the greatest possible satisfaction from their limited income"),
         ("consistent preferences", "the assumption that a consumer's preferences are stable and transitive: if A is preferred to B and B to C, then A is preferred to C"),
         ("perfect information", "the assumption that consumers know all prices, product characteristics and alternatives when they make choices"),
         ("homo economicus", "the model of the economic agent as a fully rational, self-interested utility maximiser")],
  facts=[("Which of the following is NOT an assumption of rational consumer choice?", "Consumers are influenced by how choices are framed", ["Consumers have consistent preferences", "Consumers have perfect information", "Consumers aim to maximise utility"], "Framing effects are a finding of behavioural economics that challenges rational choice."),
         ("Which of the following best describes transitive preferences?", "If a consumer prefers tea to coffee and coffee to juice, she prefers tea to juice", ["A consumer's preferences change from day to day", "A consumer always chooses the cheapest option", "A consumer prefers whatever others choose"], "Transitivity is part of the assumption of consistent preferences."),
         ("Which of the following is a key assumption about information in the rational choice model?", "Consumers have perfect information about all alternatives", ["Consumers rely on rules of thumb", "Consumers ignore prices", "Sellers know more than buyers"], "Perfect information allows consumers to compare all options.")],
  why=[("Explain why the assumption of perfect information is unrealistic.", "Consumers face thousands of products with complex features and changing prices; gathering and processing all information is costly and time-consuming, and sellers often know more than buyers (asymmetric information)."),
       ("Explain why consistent preferences are important for the rational choice model.", "If preferences changed randomly or were not transitive, consumers' choices could not be predicted and demand curves would not be stable; the model relies on stable preferences to predict behaviour."),
       ("Explain why economists assume utility maximisation even though people do not calculate utility.", "The assumption is a model: people act 'as if' they maximise utility; it generates testable predictions such as downward-sloping demand, even if actual decision processes are simpler.")],
  contrast=[("the rational choice model", "behavioural economics", "Rational choice assumes consistent preferences, perfect information and utility maximisation; behavioural economics uses psychology and evidence to show systematic deviations such as biases and bounded rationality."),
            ("utility", "price", "Utility is the satisfaction a consumer gains from a good; price is what must be paid for it. A rational consumer compares the two at the margin.")],
  misc=[("Rational consumers always buy the cheapest product.", "Rational consumers maximise utility given their budget, which may mean paying more for a product that gives more satisfaction."),
        ("If a consumer buys something they regret later, this proves the rational choice model is useless.", "One mistake does not invalidate a model of average behaviour; however, systematic, predictable errors (e.g. present bias) do challenge its assumptions, which is the focus of behavioural economics.")],
  apply=[("Mateo chooses a phone plan without reading all 15 plans available because comparing them would take hours. Explain which assumption of rational consumer choice this challenges.", "Perfect information (and the ability to process it): information is costly to obtain, so he makes a satisfactory rather than optimal choice – bounded rationality.", 2)],
  cases=[("the large number of mobile phone and energy tariffs in many countries", "Studies by regulators such as the UK's Ofgem found that many consumers stayed on expensive default tariffs rather than switching.", "the limits of the perfect information assumption", "Complex tariffs make full comparison difficult, so consumers do not maximise utility as the rational model predicts.")],
  sources=[("A regulator found that 60% of households had not switched energy supplier in the previous three years, even though switching could save an average of £300 a year. Many said comparing tariffs was 'too complicated' or that they 'never got round to it'.", "Extract based on an energy regulator's market review", "Using the extract, explain why consumer behaviour may not match the assumptions of rational consumer choice.", "Rational consumers with perfect information would switch to save £300; complexity (imperfect information, bounded rationality) and inertia (bounded self-control/status quo bias) prevent utility-maximising choices.")],
  evaluate=[("The assumptions of rational consumer choice are so unrealistic that the theory should be abandoned.", ["evidence of biases, limited information and inconsistent preferences", "behavioural economics predicts some choices better"], ["rational choice explains much market behaviour, e.g. responses to prices", "behavioural economics builds on, rather than replaces, it", "simple assumptions make models tractable"], "The theory should be retained as a benchmark but supplemented by behavioural insights where its assumptions fail.")],
  extended=[("Explain the three main assumptions of rational consumer choice and, for each, give one example of real-world behaviour that challenges it.", "Consistent preferences – preference reversals or framing effects; perfect information – complex insurance or energy tariffs; utility maximisation – satisficing, impulse buying, choosing default options. Each explained with a specific example.", 6)],
  diag=[("why the assumption of utility maximisation by rational consumers leads to a downward-sloping demand curve", "Diagram: P on the vertical axis, Q on the horizontal; downward-sloping demand. A rational consumer buys a unit only if marginal utility (benefit) is at least the price; with diminishing marginal utility, more units are bought only at lower prices, so quantity demanded rises as price falls.")])


S('ch07-st2',
  terms=[("behavioural economics", "a branch of economics that uses insights from psychology to explain why people's decisions often deviate from the rational choice model"),
         ("bounded rationality", "the idea that people's rationality is limited by the information they have, their cognitive limitations and the time available, so they often satisfice"),
         ("bounded self-control", "the idea that people have limited self-control, so they may act against their own long-term interests, for example by overeating or under-saving"),
         ("bounded selfishness", "the idea that people are not purely self-interested and often act out of concern for others, such as giving to charity"),
         ("anchoring bias", "the tendency to rely too heavily on the first piece of information received (the anchor) when making decisions"),
         ("framing bias", "the tendency for decisions to be influenced by the way information is presented rather than by its content"),
         ("availability bias", "the tendency to judge the likelihood of an event by how easily examples come to mind")],
  facts=[("A shop shows a 'was $200, now $120' label to make $120 seem cheap. Which bias does this exploit?", "Anchoring", ["Availability", "Bounded selfishness", "Loss aversion only"], "The original price acts as an anchor against which the new price is judged."),
         ("A yoghurt advertised as '90% fat-free' sells better than one labelled '10% fat'. Which bias is shown?", "Framing", ["Anchoring", "Availability", "Herd behaviour"], "The content is identical; only the frame differs."),
         ("Which economist won the Nobel Prize in 2017 for contributions to behavioural economics?", "Richard Thaler", ["Daniel Kahneman", "Herbert Simon", "Paul Krugman"], "Thaler was awarded the 2017 prize; Kahneman won in 2002 and Simon (bounded rationality) in 1978."),
         ("A person buys flood insurance immediately after seeing news of floods in a nearby town. Which bias is this?", "Availability bias", ["Anchoring bias", "Bounded selfishness", "Framing bias"], "Recent, vivid examples make the risk seem more likely.")],
  why=[("Explain how bounded self-control can lead people to save too little for retirement.", "People value present consumption much more than future benefits (present bias), so even if they intend to save, they postpone it; without commitment devices or defaults, savings are lower than their own long-term plans."),
       ("Explain why the existence of charitable giving challenges the rational choice model.", "The model assumes self-interest; donating money without receiving goods in return shows bounded selfishness – people value others' welfare and fairness."),
       ("Explain why bounded rationality leads consumers to use rules of thumb.", "Because information and time are limited and decisions complex, consumers use simple heuristics (e.g. buying a familiar brand) to reach a satisfactory decision rather than calculating the optimal one."),
       ("Explain how loss aversion can affect consumer choices.", "People feel losses more strongly than equivalent gains, so they may hold on to things they own (endowment effect) or respond more to a charge than to a bonus of the same size.")],
  contrast=[("bounded rationality", "bounded self-control", "Bounded rationality concerns limits on information and cognitive ability, so people satisfice; bounded self-control concerns limited willpower, so people act against their own long-term interests even when they know better."),
            ("anchoring", "framing", "Anchoring is relying on an initial number or piece of information as a reference point; framing is being influenced by how the same information is presented (e.g. as a gain or a loss).")],
  misc=[("Behavioural economics shows that people are irrational and their behaviour cannot be predicted.", "Behavioural economics shows that deviations from rational choice are systematic and predictable (e.g. anchoring, present bias), which is why they can be used in policy design."),
        ("Buying a gym membership and never going is an example of bounded selfishness.", "It is an example of bounded self-control (and over-optimism): people overestimate their future willpower. Bounded selfishness concerns concern for others.")],
  apply=[("A restaurant places an expensive $90 dish at the top of its menu, although few people order it. Explain the behavioural reason for this strategy.", "Anchoring: the expensive item makes other dishes (e.g. $40) seem reasonable by comparison, increasing spending on mid-priced items.", 2),
         ("Explain why a supermarket in Melbourne might advertise 'Buy 2, get 1 free' rather than '33% off'.", "Framing: 'free' is psychologically attractive; consumers respond more to the gain frame even though the discount is equivalent, and it encourages buying more units.", 2)],
  cases=[("Herbert Simon's concept of satisficing", "Simon (Nobel 1978) argued that decision-makers seek a satisfactory outcome rather than the optimal one because they face limited information and processing capacity.", "bounded rationality", "Rather than maximise, consumers and firms stop searching once an acceptable option is found."),
         ("gym memberships in the US", "Research by DellaVigna and Malmendier found that members on monthly contracts paid more per visit than if they had paid per visit, because they attended less than expected.", "bounded self-control", "Consumers over-estimate their future self-control and choose contracts that do not maximise their utility.")],
  sources=[("A charity tested two letters. One said: 'Your gift of $50 will provide clean water to a family for a year.' The other said: 'Millions of people lack clean water.' The first letter raised 60% more money.", "Hypothetical charity trial", "Using the extract, explain which behavioural concepts help explain the result.", "Framing (concrete, identifiable impact) and bounded selfishness (people care about others' welfare); the vivid, specific frame triggers more giving than an abstract statistic (availability/identifiable victim effect).")],
  evaluate=[("Behavioural economics provides a more accurate explanation of consumer behaviour than traditional rational choice theory.", ["evidence of anchoring, framing, present bias and social norms", "explains under-saving, over-eating and inertia", "has produced successful policies (auto-enrolment)"], ["many findings come from laboratory experiments and may not generalise", "rational choice predicts aggregate market responses well", "biases vary across people and contexts and some studies fail to replicate"], "Behavioural economics improves the explanation of many individual decisions, but rational choice remains a useful benchmark for aggregate market behaviour.")],
  extended=[("Explain, with examples, how firms might use their knowledge of consumer biases to increase sales, and discuss whether governments should regulate such practices.", "Anchoring (reference prices), framing ('limited time offer'), default add-ons, drip pricing; regulation arguments: protecting consumers from exploitation, information asymmetry; against: paternalism, consumer freedom, costs; examples: EU rules on pre-ticked boxes, 'fake' discounts.", 6)],
  diag=[("how bounded self-control can lead to overconsumption of a good such as sugary snacks", "Diagram: P vs Q; demand reflects the perceived marginal benefit at the moment of purchase (D = MPB perceived), which is higher than the true long-run marginal benefit to the consumer (MB true) because of present bias. The market quantity Q1 exceeds Q* where the true benefit equals cost, so consumers over-consume relative to their own long-run interest.")])


S('ch07-st3',
  terms=[("nudge", "a feature of choice architecture that alters people's behaviour in a predictable way without forbidding options or significantly changing economic incentives"),
         ("choice architecture", "the design of the way choices are presented to people, which influences the decisions they make"),
         ("default choice", "the option that applies automatically unless the person actively chooses something else"),
         ("restricted choice", "limiting the number of options available to people to make decisions easier or steer behaviour"),
         ("mandated choice", "requiring people to make an explicit decision, for example whether to be an organ donor, rather than relying on a default")],
  facts=[("Which of the following is an example of a default nudge?", "Automatically enrolling workers in a pension scheme unless they opt out", ["Banning cigarettes", "Taxing sugary drinks", "Giving a cash bonus for saving"], "The default changes behaviour without removing choice or changing incentives."),
         ("Who wrote the book Nudge (2008)?", "Richard Thaler and Cass Sunstein", ["Daniel Kahneman and Amos Tversky", "Adam Smith and David Ricardo", "Milton Friedman and Anna Schwartz"], "Thaler and Sunstein popularised the term nudge and 'libertarian paternalism'."),
         ("Requiring every driving licence applicant to state whether they wish to be an organ donor is an example of which of the following?", "Mandated choice", ["Default choice", "Restricted choice", "A tax incentive"], "People must actively make a decision."),
         ("Placing fruit at eye level and sweets out of sight in a school canteen is an example of which of the following?", "Choice architecture", ["Regulation", "An indirect tax", "A subsidy"], "The presentation of options is changed; nothing is banned.")],
  why=[("Explain why default options are so effective at changing behaviour.", "Because of inertia, status quo bias and limited attention, most people stay with the default; the default may also be seen as the recommended option, so changing it changes outcomes for millions of people at low cost."),
       ("Explain why nudges are described as 'libertarian paternalism'.", "They steer people towards choices judged to be in their interest (paternalism) while leaving them free to choose otherwise (libertarian), as no option is banned and incentives are not significantly changed."),
       ("Explain why governments might prefer nudges to taxes or bans.", "Nudges are cheap, preserve freedom of choice, avoid the political unpopularity of taxes and bans and can be tested quickly with trials.")],
  contrast=[("a default choice", "a mandated choice", "A default applies automatically unless a person opts out; mandated choice requires everyone to make an active decision with no pre-set option."),
            ("a nudge", "a regulation", "A nudge changes how choices are presented while keeping all options open; a regulation forbids or requires behaviour by law.")],
  misc=[("A tax on sugary drinks is a nudge.", "A tax changes economic incentives (the price), so it is not a nudge; a nudge alters choice architecture without significantly changing incentives."),
        ("Nudges always benefit consumers.", "Nudges can be used to steer people towards choices that benefit the designer (e.g. firms' pre-ticked add-ons), and governments may misjudge what is in people's interest.")],
  apply=[("Explain how a government could use choice architecture to increase the number of people who get a flu vaccination.", "e.g. send letters with a pre-booked appointment time (default), reminders by text, or make the vaccination point easy to reach; this uses inertia and salience rather than incentives.", 2),
         ("A university canteen puts water rather than soft drinks in the most visible fridge by the checkout. Identify the type of nudge and explain how it works.", "Choice architecture (salience/placement): the healthier option is more prominent, so more students choose it without any ban or price change.", 2)],
  cases=[("automatic enrolment in UK workplace pensions from 2012", "Employers had to enrol eligible workers automatically, who could opt out; participation in private-sector schemes rose from around 42% in 2012 to over 85% by 2019.", "default choices as a nudge", "Workers' inertia now worked in favour of saving, raising participation dramatically without compulsion."),
         ("England's switch to an opt-out organ donation system in 2020", "Under 'Max and Keira's Law', adults are presumed to be donors unless they opt out, following similar changes in Wales (2015).", "default choice architecture", "Changing the default is expected to raise the number of registered donors because most people do not actively opt out."),
         ("the UK Behavioural Insights Team's tax letters", "Adding the line 'most people in your area pay their tax on time' to reminder letters increased timely payment.", "social norms as a nudge", "Telling people what others do uses conformity to change behaviour cheaply.")],
  evaluate=[("Nudges are more effective than taxes in changing consumer behaviour.", ["low cost, preserve freedom", "large effects when defaults are used (pensions, organ donation)", "avoid regressive effects of taxes"], ["effects can be small or short-lived for many nudges", "taxes give strong, reliable incentives and raise revenue (sugar tax reformulation)", "nudges can be seen as manipulative"], "Nudges work well where inertia is the main problem, but for harmful goods with strong habits, price incentives or regulation are usually more effective; the best policy often combines them.")],
  extended=[("Evaluate the use of choice architecture to reduce household food waste.", "Possible nudges: smaller plates in canteens, clearer date labels, default smaller portions, feedback on waste; advantages: cheap, preserve choice; disadvantages: small effects, hard to measure, may need taxes/charges; examples from trials (e.g. removing trays in university canteens).", 6)],
  diag=[("how a nudge such as automatic pension enrolment can increase saving, using the idea of bounded self-control", "Diagram: market for retirement saving; without the nudge, present bias means the quantity saved (Q1, where the perceived marginal benefit curve meets the cost) is below the level Q* consistent with workers' long-run interests (true marginal benefit). Auto-enrolment shifts the effective demand for saving towards the true MB curve, increasing quantity from Q1 towards Q*.")])


@R.add('ch07-st3', 'C3', (1, 5), 'numerical')
def nudge_calc(rng, slot):
    n = rng.choice([20000, 40000, 50000, 80000, 120000, 250000])
    before = rng.choice([30, 35, 40, 45, 50])
    after = rng.choice([75, 80, 85, 88, 90])
    ctx = rng.choice([('employees of a large company in Oslo', 'its pension scheme', 'automatic enrolment with an opt-out'),
                      ('adults in a region of Spain', 'the organ donor register', 'an opt-out (presumed consent) system'),
                      ('customers of an energy firm in Toronto', 'the green-electricity tariff', 'making the green tariff the default'),
                      ('students at a university in Hong Kong', 'the reusable-cup scheme', 'giving every student a cup by default')])
    who, what, how = ctx
    extra = n * (after - before) // 100
    if slot.d <= 2:
        return dict(stem=f'Before a nudge, {before}% of {n:,} {who} joined {what}. After introducing {how}, participation rose to {after}%. Calculate the increase in the number of participants.',
                    answer=f'{extra:,}', markingKey=f'({after} − {before})% × {n:,} = {extra:,}. [1] [1]', type='numerical', marks=2)
    cost = rng.choice([2, 3, 5, 8])
    return dict(stem=f'{n:,} {who} could join {what}. With opt-in, {before}% joined; with {how}, {after}% joined. Administering the change costs ${cost} per person eligible. Calculate the additional participants, the cost per additional participant, and explain why defaults have such a large effect.',
                answer=f'{extra:,} extra; cost ${r2(cost * n / extra)} per extra participant',
                markingKey=f'Extra = {(after - before)}% × {n:,} = {extra:,} [1]; total cost = {cost} × {n:,} = ${cost * n:,} [1]; per extra participant = {r2(cost * n / extra)} [1]; inertia/status quo bias, so most people stay with the default [1].', type='numerical', marks=4)


S('ch07-st4',
  terms=[("profit maximisation", "the business objective of producing the output at which the difference between total revenue and total cost is greatest (where MC = MR)"),
         ("corporate social responsibility (CSR)", "a business objective of acting in an ethical and socially responsible way, taking account of the environment, workers and communities"),
         ("market share", "a firm's sales as a percentage of total sales in the market"),
         ("satisficing", "aiming for a satisfactory level of profit rather than the maximum, often to satisfy several stakeholders"),
         ("growth maximisation", "the objective of maximising the size of the firm, for example its sales revenue or number of outlets")],
  facts=[("Which of the following best explains why firms might satisfice rather than profit-maximise?", "Managers must balance the interests of different stakeholders and have limited information", ["Satisficing always yields the highest profit", "Governments require it", "Consumers prefer satisficing firms"], "Herbert Simon argued that with bounded rationality and many stakeholders, firms aim for satisfactory results."),
         ("A firm cuts prices below rivals to win customers even though profits fall in the short run. Which objective is it most likely pursuing?", "Increasing market share", ["Profit maximisation in the short run", "Satisficing", "Corporate social responsibility"], "Lower prices sacrifice short-run profit for a larger share of the market."),
         ("Which company's founder transferred ownership in 2022 to a trust and non-profit so that profits are used to fight climate change?", "Patagonia", ["Amazon", "Tesla", "Nestlé"], "Yvon Chouinard's decision is a high-profile example of CSR as a business objective.")],
  why=[("Explain why a firm might pursue corporate social responsibility even if it raises costs.", "CSR can improve brand image and customer loyalty, attract talented workers and ethical investors, avoid regulation and reputational damage, so it may raise long-run profits as well as reflecting owners' values."),
       ("Explain why separation of ownership and control may lead firms to pursue goals other than profit maximisation.", "Shareholders own large firms but managers control them; managers may pursue sales growth, status or a quiet life rather than maximum profit, especially when shareholders cannot monitor them closely (principal-agent problem)."),
       ("Explain why a new firm may aim for market share rather than profit in its early years.", "Gaining customers quickly can create network effects, economies of scale and brand loyalty, deterring rivals and allowing higher profits later; e.g. ride-hailing and food delivery platforms ran losses for years.")],
  contrast=[("profit maximisation", "satisficing", "Profit maximisation aims for the greatest possible profit (MC = MR); satisficing aims for a satisfactory profit that keeps stakeholders content."),
            ("market share", "growth maximisation", "Market share is a firm's sales relative to the whole market; growth maximisation aims to increase the absolute size of the firm, which may happen even if market share does not rise.")],
  misc=[("Firms that pursue CSR cannot be profit maximisers.", "CSR and long-run profit maximisation can be compatible: ethical behaviour can increase demand, reduce costs (e.g. energy efficiency) and protect reputation."),
        ("Profit maximisation means charging the highest possible price.", "Profit maximisation means choosing the output where MC = MR; a very high price may reduce quantity so much that profit falls.")],
  apply=[("Amazon reported very low or negative profits for many years while expanding rapidly. Identify and explain the business objective this suggests.", "Growth/market share maximisation: reinvesting revenue in expansion, low prices and infrastructure to dominate the market and gain economies of scale, expecting higher long-run profits.", 2)],
  cases=[("Unilever's Sustainable Living Plan (2010-2020)", "Unilever set targets to halve its environmental footprint and source agricultural materials sustainably while growing the business.", "corporate social responsibility as a business objective", "The firm pursued social and environmental goals alongside profit, arguing that sustainable brands grew faster.")],
  evaluate=[("Profit maximisation is the most realistic assumption about the objectives of firms.", ["firms that fail to make profits do not survive", "shareholders pressure managers for returns", "explains many pricing and output decisions"], ["separation of ownership and control", "CSR, market share and growth goals are common", "firms lack the information to find MC = MR exactly (satisficing)"], "Profit is central in the long run, but in practice firms pursue a mix of objectives, so profit maximisation is a useful simplification rather than a complete description.")],
  diag=[("the difference between the output chosen by a profit-maximising firm and by a revenue-maximising firm", "Diagram: firm with downward-sloping AR (demand) and MR, and MC and AC curves. Profit maximisation at Qπ where MC = MR, price from AR. Revenue maximisation at QR where MR = 0, a higher output and lower price; profit is lower than at Qπ but the firm gains sales and market share.")])

# =============================================================================================
# ch08 Unit 2.5 Elasticity of demand
# =============================================================================================
def ped_class(v):
    v = abs(v)
    if v == 0:
        return 'perfectly inelastic'
    if abs(v - 1) < 1e-9:
        return 'unit elastic'
    return 'price elastic' if v > 1 else 'price inelastic'


S('ch08-st1',
  terms=[("price elasticity of demand (PED)", "a measure of the responsiveness of quantity demanded to a change in the good's own price, calculated as %ΔQd ÷ %ΔP"),
         ("price elastic demand", "demand for which PED is greater than 1 (in absolute value), so quantity demanded changes by a larger percentage than price"),
         ("price inelastic demand", "demand for which PED is between 0 and 1 (in absolute value), so quantity demanded changes by a smaller percentage than price"),
         ("unit elastic demand", "demand for which PED equals 1, so the percentage change in quantity demanded equals the percentage change in price"),
         ("perfectly inelastic demand", "demand for which PED = 0: quantity demanded does not change when price changes, shown by a vertical demand curve"),
         ("perfectly elastic demand", "demand for which PED is infinite: any rise in price above a given level causes quantity demanded to fall to zero, shown by a horizontal demand curve")],
  facts=[("If the price of a good rises by 10% and quantity demanded falls by 25%, what is the PED?", "−2.5 (price elastic)", ["−0.4 (price inelastic)", "−25 (perfectly elastic)", "−1 (unit elastic)"], "PED = −25%/10% = −2.5; |PED| > 1."),
         ("Why is PED usually negative?", "Price and quantity demanded move in opposite directions (law of demand)", ["Because demand curves slope upwards", "Because percentages are always negative", "Because firms reduce supply when prices rise"], "Economists often quote the absolute value."),
         ("Which of the following is represented by a vertical demand curve?", "Perfectly inelastic demand (PED = 0)", ["Perfectly elastic demand", "Unit elastic demand", "Price elastic demand"], "Quantity demanded is the same at every price."),
         ("Which of the following PED values indicates the most price-inelastic demand?", "−0.2", ["−0.8", "−1.5", "−4"], "The closer |PED| is to zero, the less responsive quantity is to price.")],
  why=[("Explain why PED is measured using percentage changes rather than absolute changes.", "Percentages make the measure independent of units (litres, kilograms, dollars, euros), so elasticities can be compared across goods and countries."),
       ("Explain why a horizontal demand curve represents perfectly elastic demand.", "At the given price consumers will buy any quantity, but if price rises even slightly quantity demanded falls to zero, so the percentage change in quantity is infinitely large relative to the price change."),
       ("Explain why PED values for the same good can differ between consumers.", "Responsiveness depends on income, tastes and access to substitutes; a commuter with no alternative transport has inelastic demand for train tickets while a leisure traveller who can drive has more elastic demand.")],
  contrast=[("price elastic demand", "price inelastic demand", "With elastic demand (|PED| > 1) the percentage change in quantity demanded exceeds the percentage change in price; with inelastic demand (0 < |PED| < 1) it is smaller."),
            ("perfectly elastic demand", "perfectly inelastic demand", "Perfectly elastic demand (PED = ∞) is horizontal: any price rise reduces quantity to zero; perfectly inelastic demand (PED = 0) is vertical: quantity does not change with price.")],
  misc=[("A PED of −3 means demand is inelastic because the number is negative.", "The sign only shows the inverse relationship; |PED| = 3 > 1, so demand is price elastic."),
        ("A steep demand curve always means demand is inelastic at every point.", "Elasticity varies along a linear demand curve and depends on the scale of the axes; slope and elasticity are not the same thing.")],
  apply=[("A cinema in Lima cuts ticket prices by 20% and ticket sales rise by 8%. Calculate PED and state whether demand is elastic or inelastic.", "PED = 8%/−20% = −0.4: price inelastic.", 2)],
  cases=[("the response of petrol demand to the 2022 price spike in Europe", "Petrol prices rose by over 30% in many EU countries, yet the volume of fuel sold fell only slightly in the short run.", "price inelastic demand", "Few substitutes in the short run (people must still commute) mean |PED| was low, so quantity responded much less than price.")],
  sources=[("When a ride-hailing company in Nairobi raised average fares from KSh 400 to KSh 460 in 2023, the number of weekly trips fell from 2.0 million to 1.7 million.", "Hypothetical company data", "Calculate the PED for rides and explain what it suggests about the availability of substitutes.", "%ΔP = 15%, %ΔQ = −15%; PED = −1 (unit elastic). Consumers are fairly responsive, suggesting substitutes such as matatus and boda-bodas are available.")],
  evaluate=[("Knowledge of PED is essential for firms setting prices.", ["shows how revenue will change when price changes", "helps target price discrimination", "informs promotions and discounts"], ["PED estimates are uncertain and change over time", "competitors' reactions change outcomes", "firms also consider costs, brand image and long-term objectives"], "PED is valuable for pricing decisions, but estimates are imprecise and must be combined with knowledge of costs and rivals' behaviour.")],
  extended=[("Explain the range of values PED can take, using diagrams to illustrate perfectly elastic, perfectly inelastic and unit elastic demand.", "0 (vertical), between 0 and 1 (inelastic), 1 (unit elastic – rectangular hyperbola, TR constant), >1 (elastic), ∞ (horizontal). Each with P/Q axes and interpretation.", 6)],
  diag=[("the difference between price elastic and price inelastic demand", "Two diagrams with the same price rise from P1 to P2. Elastic demand (relatively flat curve): quantity falls by a larger percentage, from Q1 to Q2, |PED| > 1. Inelastic demand (relatively steep curve): quantity falls by a smaller percentage, |PED| < 1. Label axes P and Q, and the changes in each.")])


PED_FRAMES = [
    ('When a retailer in {city} raised the price of {g} from {c0}{p0} to {c0}{p1}, weekly sales changed from {q0} to {q1}.', '{g}'),
    ('A transport authority in {city} changed the price of {g} from {c0}{p0} to {c0}{p1}; the number sold per day changed from {q0} to {q1}.', '{g}'),
    ('An online retailer in {city} found that when it set the price of {g} at {c0}{p0}, it sold {q0} units a month, and at {c0}{p1} it sold {q1} units.', '{g}'),
    ('Market research in {city} shows that at a price of {c0}{p0} consumers buy {q0} units of {g} per week, while at {c0}{p1} they buy {q1}.', '{g}'),
]


@R.add('ch08-st1', 'C3', (1, 5), 'numerical')
def ped_calc(rng, slot):
    for _ in range(60):
        p0 = rng.choice([2, 4, 5, 8, 10, 12, 15, 20, 25, 40, 50])
        dp = rng.choice([-50, -40, -25, -20, -10, 10, 20, 25, 40, 50])
        p1 = p0 * (1 + dp / 100)
        e = rng.choice([0.2, 0.25, 0.4, 0.5, 0.6, 0.8, 1, 1.2, 1.5, 2, 2.5, 3])
        q0 = rng.choice([200, 400, 500, 800, 1000, 1200, 2000, 5000])
        dq = -e * dp
        q1 = q0 * (1 + dq / 100)
        if q1 > 0 and abs(q1 - round(q1)) < 1e-9 and abs(p1 * 100 - round(p1 * 100)) < 1e-6:
            break
    else:
        return None
    q1 = int(round(q1))
    g = rng.choice(GOODS)
    cur = rng.choice(['$', '€', '£'])
    city = rng.choice(CITIES)
    frame, _ = rng.choice(PED_FRAMES)
    intro = frame.format(city=city, g=g, c0=cur, p0=r2(p0), p1=r2(p1), q0=q0, q1=q1)
    ped = dq / dp
    cls = ped_class(ped)
    if slot.d <= 2:
        return dict(stem=f'{intro} Calculate the price elasticity of demand.', answer=f'{r2(-abs(ped))} ({cls})',
                    markingKey=f'%ΔQ = ({q1} − {q0})/{q0} × 100 = {r2(dq)}%; %ΔP = {r2(dp)}%; PED = {r2(dq)}/{r2(dp)} = {r2(-abs(ped))}. [1] working [1] answer (negative sign or absolute value accepted).', type='numerical', marks=2)
    tr0, tr1 = p0 * q0, p1 * q1
    return dict(stem=f'{intro} Calculate the PED, state whether demand is price elastic or inelastic, and calculate the change in total revenue. Explain whether the result is consistent with the PED value.',
                answer=f'PED = {r2(-abs(ped))} ({cls}); TR changes from {cur}{r2(tr0)} to {cur}{r2(tr1)} (change of {sm(tr1 - tr0, cur)})',
                markingKey=f'PED = {r2(dq)}%/{r2(dp)}% = {r2(-abs(ped))} [1]; {cls} [1]; TR: {r2(p0)}×{q0} = {r2(tr0)} → {r2(p1)}×{q1} = {r2(tr1)} [1]; consistent: {"elastic – price and TR move in opposite directions" if abs(ped) > 1 else "inelastic – price and TR move in the same direction" if abs(ped) < 1 else "unit elastic – TR unchanged"} [1].', type='numerical', marks=4)


@R.add('ch08-st1', 'C3', (2, 5), 'numerical')
def ped_predict(rng, slot):
    e = rng.choice([0.3, 0.4, 0.5, 0.6, 0.8, 1.2, 1.5, 2, 2.5])
    dp = rng.choice([5, 8, 10, 12, 15, 20])
    up = rng.random() < 0.5
    q0 = rng.choice([10000, 20000, 50000, 80000, 120000])
    ctx = rng.choice([('cigarettes', 'packs per week', 'a government tax rise'), ('train tickets', 'journeys per day', 'a fare increase'),
                      ('luxury watches', 'units per month', 'a price increase'), ('domestic flights', 'seats per week', 'a fuel surcharge'),
                      ('restaurant meals', 'covers per week', 'menu price changes'), ('mobile data', 'gigabytes per day', 'a tariff change')])
    g, unit, why = ctx
    sgn = 1 if up else -1
    dq = -e * dp * sgn
    q1 = q0 * (1 + dq / 100)
    return dict(stem=f'The PED for {g} in {rng.choice(CITIES)} is estimated at −{r2(e)}. Following {why}, the price {"rises" if up else "falls"} by {dp}%. Current sales are {q0:,} {unit}. Calculate the new quantity demanded.',
                answer=f'{fmt(q1, 6)} {unit}', markingKey=f'%ΔQd = PED × %ΔP = −{r2(e)} × {"+" if up else "−"}{dp}% = {r2(dq)}% [1]; new Q = {q0:,} × {1 + dq / 100:.4g} = {fmt(q1, 6)} [1].', type='numerical', marks=2)


S('ch08-st2',
  terms=[("determinants of PED", "the factors influencing price elasticity of demand: number and closeness of substitutes, necessity or luxury, proportion of income spent on the good, time period and addictiveness/habit"),
         ("closeness of substitutes", "how easily consumers can switch to an alternative product; the closer the substitutes, the more price elastic demand"),
         ("proportion of income spent", "the share of a consumer's budget spent on a good; the larger the share, the more price elastic demand tends to be"),
         ("PED along a linear demand curve", "elasticity falls continuously along a straight-line demand curve: elastic above the midpoint, unit elastic at the midpoint and inelastic below it")],
  facts=[("Which of the following goods is likely to have the most price elastic demand?", "One particular brand of bottled water", ["Water in general", "Insulin for diabetics", "Electricity for households"], "A single brand has many close substitutes."),
         ("At the midpoint of a straight-line demand curve, what is the PED?", "−1 (unit elastic)", ["0", "Infinite", "−0.5"], "Above the midpoint demand is elastic; below it, inelastic."),
         ("Why does demand tend to become more price elastic over time?", "Consumers have more time to find substitutes and change habits", ["Prices always fall over time", "Incomes always rise", "Supply becomes more elastic"], "E.g. after a fuel price rise, people eventually buy more efficient cars or move closer to work."),
         ("Which of the following best explains why salt has very price inelastic demand?", "It has few substitutes and takes a tiny share of income", ["It is a luxury", "It is heavily advertised", "It is an inferior good"], "Both determinants make consumers unresponsive to price.")],
  why=[("Explain why demand for a broadly defined good (e.g. 'food') is less price elastic than demand for a narrowly defined good (e.g. 'bananas').", "There are few substitutes for food as a whole, but many substitutes for a particular food; consumers can easily switch from bananas to apples if the price of bananas rises."),
       ("Explain why PED varies along a straight-line demand curve even though the slope is constant.", "PED = (ΔQ/ΔP) × (P/Q); ΔQ/ΔP is constant but P/Q falls as we move down the curve, so demand is elastic at high prices and low quantities and inelastic at low prices and high quantities."),
       ("Explain why addictive goods such as cigarettes have price inelastic demand.", "Addiction and habit mean consumers continue to buy even when prices rise; they feel they have no acceptable substitute, so quantity demanded responds little to price.")],
  contrast=[("slope of a demand curve", "price elasticity of demand", "Slope measures the absolute change in price for a change in quantity and is constant on a straight line; PED measures proportional responsiveness and changes along the line."),
            ("a necessity", "a luxury", "Necessities have few acceptable substitutes and inelastic demand (and income-inelastic demand); luxuries can be postponed or replaced, so their demand is more price and income elastic.")],
  misc=[("A straight-line demand curve has the same PED at every point.", "PED varies along a linear demand curve because P/Q changes: it is elastic at high prices, unit elastic at the midpoint and inelastic at low prices."),
        ("Goods that are necessities always have perfectly inelastic demand.", "Necessities usually have inelastic demand, but rarely perfectly inelastic; consumers still buy somewhat less, or switch brands, when prices rise.")],
  apply=[("Explain whether demand for Apple iPhones is likely to be more or less price elastic than demand for smartphones in general.", "More elastic: if the iPhone's price rises, consumers can switch to other brands (Samsung, Xiaomi), whereas there are few substitutes for smartphones as a whole.", 2),
         ("A train company in Japan finds that demand for peak-time Shinkansen tickets is less price elastic than for off-peak tickets. Explain why.", "Peak travellers are often business commuters who must travel at fixed times and whose employers pay; off-peak leisure travellers can change time or mode, so they are more responsive.", 3)],
  cases=[("the UK's tobacco tax policy", "Large, repeated increases in tobacco duty have raised substantial revenue because demand for cigarettes is price inelastic (estimates around −0.4 to −0.6).", "determinants of PED", "Addiction and lack of substitutes keep demand inelastic, so quantity falls by less than price and tax revenue rises.")],
  evaluate=[("The availability of substitutes is the most important determinant of PED.", ["explains differences between brands and product categories", "close substitutes make consumers very responsive"], ["time period: elasticity rises in the long run", "share of income and necessity also matter", "addiction can make demand inelastic despite substitutes"], "Substitutes are usually the most important determinant, but the time period and the nature of the good interact with it.")],
  extended=[("A demand curve is given by Qd = 100 − 2P. Explain, using calculations at P = $10, $25 and $40, how PED changes along the curve.", "PED = −2 × P/Q: at P = 10, Q = 80, PED = −0.25 (inelastic); at P = 25, Q = 50, PED = −1 (unit elastic, midpoint); at P = 40, Q = 20, PED = −4 (elastic).", 6)],
  diag=[("why price elasticity of demand varies along a straight-line demand curve", "Diagram: linear demand from the P-intercept to the Q-intercept, midpoint marked. Above the midpoint |PED| > 1 (elastic), at the midpoint |PED| = 1, below it |PED| < 1 (inelastic). Because ΔQ/ΔP is constant but P/Q falls as price falls, elasticity declines down the curve; total revenue is maximised at the midpoint.")])


@R.add('ch08-st2', 'C3', (2, 5), 'numerical')
def ped_point(rng, slot):
    b = rng.choice([2, 4, 5, 10])
    pint = rng.choice([20, 30, 40, 50, 60])
    a = b * pint
    P = rng.choice([p for p in range(2, pint - 1) if p != pint / 2])
    Q = a - b * P
    e = -b * P / Q
    g = rng.choice(GOODS)
    stem = rng.choice([f'The demand for {g} in {rng.choice(CITIES)} is Qd = {a} − {b}P. Calculate the PED at a price of ${P} and state whether demand is elastic or inelastic at this price.',
                       f'A firm estimates the demand function for {g} as Qd = {a} − {b}P. Using the point elasticity formula PED = (ΔQ/ΔP) × (P/Q), calculate PED at P = ${P}.'])
    if slot.d >= 4:
        stem += f' Identify the price at which demand is unit elastic.'
    ans = f'PED = {r2(e)} ({ped_class(e)})' + (f'; unit elastic at P = ${fmt(pint / 2)}' if slot.d >= 4 else '')
    key = f'Q = {a} − {b}×{P} = {Q} [1]; PED = −{b} × {P}/{Q} = {r2(e)} [1]' + (f'; midpoint P = {pint}/2 = {fmt(pint / 2)} [1]; elastic above, inelastic below [1].' if slot.d >= 4 else '.')
    return dict(stem=stem, answer=ans, markingKey=key, type='numerical', marks=4 if slot.d >= 4 else 2)


S('ch08-st3',
  terms=[("total revenue (TR)", "the total amount received by firms from selling their output, equal to price × quantity sold"),
         ("tax incidence", "the distribution of the burden of an indirect tax between consumers and producers, which depends on PED and PES"),
         ("primary commodities", "raw materials produced by agriculture, fishing, forestry and mining, such as wheat, coffee, copper and oil"),
         ("revenue-maximising price", "the price at which PED = −1 and total revenue is at its maximum")],
  facts=[("If demand is price inelastic, what happens to total revenue when a firm raises its price?", "Total revenue rises", ["Total revenue falls", "Total revenue is unchanged", "Total revenue falls to zero"], "The percentage fall in quantity is smaller than the percentage rise in price."),
         ("Why do governments tend to place indirect taxes on goods with price inelastic demand?", "Quantity falls little, so tax revenue is large and reliable", ["Consumption of such goods falls sharply", "Producers bear all of the tax", "These goods are always luxuries"], "Inelastic demand keeps the tax base large."),
         ("When demand is unit elastic, what happens to total revenue after a price cut?", "Total revenue is unchanged", ["Total revenue rises", "Total revenue falls", "It depends on supply"], "The percentage increase in quantity exactly offsets the percentage fall in price."),
         ("Who bears most of the burden of an indirect tax when demand is price inelastic?", "Consumers", ["Producers", "The government", "Neither, the tax is shared equally"], "With inelastic demand, the price paid by consumers rises by most of the tax.")],
  why=[("Explain why primary commodity producers' revenues are very volatile.", "Demand and supply for commodities are both price inelastic, so supply shocks such as weather cause large price swings; with inelastic demand, a bumper harvest lowers price by more than quantity rises, reducing farmers' revenue."),
       ("Explain why a firm facing price elastic demand might cut its price.", "With |PED| > 1 a price cut causes a proportionately larger rise in quantity demanded, so total revenue increases (and profit may rise if costs do not rise too much)."),
       ("Explain why an indirect tax on a good with inelastic demand is ineffective in reducing consumption.", "Consumers are unresponsive to price, so although the price rises, quantity demanded falls only slightly; the tax mainly raises revenue rather than changing behaviour, at least in the short run."),
       ("Explain why total revenue is maximised where PED = −1.", "If demand is elastic, cutting price raises TR; if inelastic, raising price raises TR; only at unit elasticity does a small price change leave TR unchanged, so TR is at its peak.")],
  contrast=[("the effect of a price rise on revenue when demand is elastic", "the effect when demand is inelastic", "With elastic demand a price rise reduces TR because quantity falls proportionately more; with inelastic demand TR rises because quantity falls proportionately less."),
            ("the incidence of a tax on consumers", "the incidence on producers", "The consumer burden is the rise in price paid; the producer burden is the fall in price received after tax. The more inelastic side of the market bears more of the tax.")],
  misc=[("A firm should always raise its price to increase revenue.", "A price rise raises revenue only if demand is price inelastic; with elastic demand, revenue falls."),
        ("A bumper harvest always makes farmers better off because they sell more.", "With price inelastic demand the price falls proportionately more than quantity rises, so total revenue falls.")],
  apply=[("Demand for a city's public swimming pool is estimated to have PED = −1.6. The council wants more revenue. Advise whether it should raise or lower entry prices.", "Lower prices: demand is elastic, so a price cut raises quantity proportionately more, increasing total revenue.", 2),
         ("Explain why the government of Colombia might be concerned when world coffee prices fall by 30% in a year.", "Coffee demand and supply are price inelastic; farmers' revenues and export earnings fall sharply, reducing incomes in coffee-growing regions and tax revenue.", 3)],
  cases=[("the collapse in world cocoa prices in the late 1980s", "Prices fell sharply after supply expanded; farmers in Côte d'Ivoire and Ghana saw large falls in income.", "PED and the revenue of primary commodity producers", "Inelastic demand meant greater output reduced prices more than proportionately, cutting producers' revenues."),
         ("Mexico's 2014 tax on sugary drinks", "A tax of 1 peso per litre (about 10%) reduced purchases of taxed drinks by roughly 6-12% in the first years.", "the effect of an indirect tax when demand is price inelastic", "Quantity fell by a smaller percentage than the price rose, so the tax raised substantial revenue while having a moderate effect on consumption.")],
  sources=[("In 2023 Ghana's cocoa farmers sold 750,000 tonnes at an average of $2,500 per tonne. In 2024, poor weather cut output to 530,000 tonnes, but the world price rose to around $7,000 per tonne.", "Stylised figures based on 2023-2024 market conditions", "Using the data, calculate the change in total revenue and explain what it implies about the PED for cocoa.", "TR rose from $1.875bn to $3.71bn. Price rose by 180% while quantity fell by about 29%: demand is price inelastic, so the supply shortage increased revenue (for producers able to sell at world prices).")],
  evaluate=[("Governments should tax goods with price inelastic demand to raise revenue.", ["large, stable tax revenue", "small efficiency (deadweight) loss because quantity changes little", "many such goods are demerit goods (tobacco, alcohol)"], ["regressive: low-income households spend a higher share of income on many such goods", "does little to reduce consumption", "may encourage smuggling or black markets"], "Taxing inelastic goods is effective for revenue and has a low welfare cost, but equity effects and black markets must be considered; revenue can be used to offset regressivity.")],
  extended=[("Using diagrams, explain how the incidence of an indirect tax differs when demand is price elastic and when it is price inelastic, and explain the implications for government tax revenue.", "Inelastic demand: price rises by most of the tax, consumers bear most of the burden, quantity falls little – large revenue. Elastic demand: price rises little, producers bear most, quantity falls a lot – smaller revenue. Diagrams with S and S + tax, consumer and producer burden areas.", 6)],
  diag=[("why a fall in price leads to an increase in total revenue when demand is price elastic", "Diagram: elastic (relatively flat) demand; price falls from P1 to P2; quantity rises from Q1 to Q2. TR before = P1 × Q1 rectangle; after = P2 × Q2. Revenue lost (P1 − P2) × Q1 is smaller than revenue gained P2 × (Q2 − Q1), so TR rises."),
        ("why price inelastic demand and supply cause volatile prices and revenues for primary commodity producers", "Diagram: steep (inelastic) demand and supply for coffee; a supply shift from good harvests (S1 to S2) causes a large fall in price and a small rise in quantity, so total revenue falls; a poor harvest does the reverse. Small shifts cause large price changes.")])


@R.add('ch08-st3', 'C3', (2, 5), 'numerical')
def ped_tr(rng, slot):
    for _ in range(60):
        e = rng.choice([0.25, 0.4, 0.5, 0.6, 0.75, 1.25, 1.5, 2, 3])
        dp = rng.choice([-20, -10, 10, 20, 25])
        p0 = rng.choice([4, 5, 8, 10, 20, 40])
        q0 = rng.choice([1000, 2000, 4000, 5000, 10000])
        p1 = p0 * (1 + dp / 100)
        q1 = q0 * (1 - e * dp / 100)
        if q1 > 0 and abs(q1 - round(q1)) < 1e-9:
            break
    else:
        return None
    ctx = rng.choice(['a museum in Vienna', 'a bus operator in Accra', 'a theme park near Kuala Lumpur', 'a football club in Lisbon', 'a ferry company in Oslo', 'a music-streaming start-up in Seoul'])
    tr0, tr1 = p0 * q0, p1 * q1
    adv = 'raise' if (e < 1) else 'lower'
    return dict(stem=f'The PED for the service sold by {ctx} is −{r2(e)}. It currently charges ${r2(p0)} and sells {q0:,} units a week, and is considering a price {"rise" if dp > 0 else "cut"} of {abs(dp)}%. Calculate the change in total revenue and advise whether, to maximise revenue, it should raise or lower its price.',
                answer=f'TR changes from ${r2(tr0)} to ${r2(tr1)} (change of {sm(tr1 - tr0)}); to raise revenue it should {adv} price',
                markingKey=f'New P = {r2(p1)}; %ΔQ = −{r2(e)} × {dp}% = {r2(-e * dp)}% so Q = {fmt(q1, 6)} [1]; TR {r2(tr0)} → {r2(tr1)} [2]; demand is {"inelastic" if e < 1 else "elastic"}, so {adv} price [1].', type='numerical', marks=4)


@R.add('ch08-st3', 'C4', (3, 5), 'multi_step')
def tax_incidence_ped(rng, slot):
    m = market(rng)
    if not m:
        return None
    a, b, c, d, P, Q = m
    for t in rng.sample([2, 3, 4, 5, 6, 8, 10], 7):
        Pc = (a - c + d * t) / (b + d)
        if abs(Pc * 100 - round(Pc * 100)) < 1e-6 and a - b * Pc > 0:
            break
    else:
        return None
    Qt = a - b * Pc
    Pp = Pc - t
    intro, g = mkt_intro(rng, a, b, c, d)
    cb, pb = (Pc - P) * Qt, (P - Pp) * Qt
    e_d = b * P / Q
    e_s = d * P / Q
    side = 'consumers' if cb > pb else 'producers' if pb > cb else 'neither side more'
    return dict(stem=f'{intro} The government imposes a specific tax of ${t} per unit on producers. Calculate the consumer and producer share of the tax burden, and explain your result using the price elasticities of demand and supply at the original equilibrium.',
                answer=f'Consumer burden ${r2(cb)}, producer burden ${r2(pb)}; {side} bear more of the tax',
                markingKey=f'Original P = {P}, Q = {Q} [1]; with tax {a} − {b}P = {c} + {d}(P − {t}) ⇒ Pc = {r2(Pc)}, Pp = {r2(Pp)}, Q = {r2(Qt)} [2]; consumer burden ({r2(Pc)} − {P}) × {r2(Qt)} = {r2(cb)}, producer ({P} − {r2(Pp)}) × {r2(Qt)} = {r2(pb)} [2]; at equilibrium |PED| = {r2(e_d)}, PES = {r2(e_s)}: the less elastic side bears more [1].', type='multi_step', marks=6)


S('ch08-st4',
  terms=[("income elasticity of demand (YED)", "a measure of the responsiveness of demand to a change in consumers' income, calculated as %ΔQd ÷ %ΔY"),
         ("necessity (income inelastic normal good)", "a normal good with YED between 0 and 1, so demand rises by a smaller percentage than income"),
         ("luxury (income elastic normal good)", "a normal good with YED greater than 1, so demand rises by a larger percentage than income"),
         ("Engel's law", "the observation that as household income rises, the proportion spent on food falls, because food has income inelastic demand"),
         ("sectoral change", "the shift in the structure of an economy over time from the primary sector to the secondary and then the tertiary sector, linked to differences in YED")],
  facts=[("If income rises by 5% and demand for a good rises by 12%, the good is best described as which of the following?", "A luxury (YED = 2.4)", ["A necessity (YED = 0.42)", "An inferior good", "Unit elastic"], "YED = 12/5 = 2.4 > 1."),
         ("A good with a YED of −0.6 is which of the following?", "An inferior good", ["A luxury", "A necessity", "A normal good"], "Negative YED means demand falls as income rises."),
         ("Which sector's output tends to grow fastest as an economy develops, because of high YED?", "The tertiary (services) sector", ["The primary sector", "Agriculture", "Mining"], "Services such as tourism, health and finance have high YED."),
         ("Which of the following is most likely to have a YED between 0 and 1?", "Basic food such as rice in a high-income country", ["Foreign holidays", "Luxury cars", "Bus travel in a high-income city"], "Rice is a necessity; bus travel may be inferior.")],
  why=[("Explain why primary commodity producers may face falling relative incomes as the world economy grows.", "Demand for most primary commodities (especially food) is income inelastic, so as world incomes rise demand grows more slowly than for manufactures and services; commodity producers' share of world income falls."),
       ("Explain why firms are interested in knowing the YED of their products.", "YED shows how demand will change in booms and recessions; firms selling luxuries can expect big rises in demand as incomes grow and big falls in recessions, helping them plan production, investment and product ranges."),
       ("Explain how YED helps to explain the decline of the share of agriculture in employment as countries develop.", "Food has low YED; as incomes rise, spending shifts to manufactures and services with higher YED, so resources (labour) move out of agriculture into other sectors – sectoral change.")],
  contrast=[("a necessity", "a luxury", "Both are normal goods. For a necessity 0 < YED < 1 (demand rises less than proportionately with income); for a luxury YED > 1 (demand rises more than proportionately)."),
            ("YED", "PED", "PED measures the responsiveness of quantity demanded to the good's own price (a movement along the curve); YED measures the responsiveness of demand to income (a shift of the curve).")],
  misc=[("A good with a YED of 0.4 is an inferior good because the value is less than one.", "Any positive YED indicates a normal good; 0.4 means it is a necessity (income inelastic). Inferior goods have negative YED."),
        ("A rise in income causes a movement along the demand curve.", "Income is a non-price determinant; a change in income shifts the demand curve. YED measures the size of that shift.")],
  apply=[("Real incomes in Vietnam rose by 6% while demand for air travel rose by 15%. Calculate YED and classify air travel.", "YED = 15/6 = 2.5: a luxury (income elastic normal good).", 2),
         ("A supermarket chain expects a recession. Using YED, explain which products it should stock more of.", "Products with negative YED (inferior goods, e.g. own-brand basics) will see demand rise; luxuries with high YED will see demand fall most.", 3)],
  cases=[("the growth of China's middle class since 2000", "Rapid income growth led to soaring demand for cars, overseas travel and dairy products, while demand for some staple grains per person stagnated.", "income elasticity of demand", "Goods with high YED (cars, tourism) grew much faster than income, while staples with low or negative YED did not."),
         ("sectoral change in South Korea", "Agriculture's share of employment fell from about 50% in 1970 to around 5% today, while services grew to about 70% of employment.", "sectoral change linked to YED", "As incomes rose, spending shifted to manufactures and services with higher YED, pulling labour out of agriculture.")],
  evaluate=[("Countries that rely on exporting primary commodities will inevitably fall behind those that export manufactured goods.", ["low YED for food means slow growth in demand", "volatile prices and revenues (low PED and PES)", "declining terms of trade (Prebisch-Singer)"], ["some commodities have high demand growth (lithium, copper for the energy transition)", "revenues can be invested in diversification (Botswana's diamonds, Chile's copper)", "commodity booms (2000s) raised incomes"], "Dependence on low-YED commodities is a disadvantage, but outcomes depend on which commodities and on how revenues are managed and used for diversification.")],
  extended=[("Explain, using the concept of YED, how a firm selling both luxury and budget product lines might be affected by a recession.", "Luxury lines (YED > 1) see demand fall by more than income; budget lines (YED < 0 or low) may see stable or rising demand; overall revenue less volatile; firms may shift marketing and production towards budget lines in recessions.", 6)],
  diag=[("the effect of rising incomes on the demand for a luxury good, a necessity and an inferior good", "Three demand diagrams. Luxury (YED > 1): large rightward shift. Necessity (0 < YED < 1): small rightward shift. Inferior good (YED < 0): leftward shift. In each, the new equilibrium price and quantity are shown with the original supply curve.")])


@R.add('ch08-st4', 'C3', (1, 5), 'numerical')
def yed_calc(rng, slot):
    for _ in range(50):
        y0 = rng.choice([20000, 25000, 30000, 40000, 50000, 60000])
        dy = rng.choice([-10, -5, -4, 2, 4, 5, 8, 10])
        yed = rng.choice([-1.5, -0.8, -0.5, 0.2, 0.4, 0.5, 0.8, 1.5, 2, 2.5, 3])
        q0 = rng.choice([100, 200, 400, 500, 1000, 2000])
        q1 = q0 * (1 + yed * dy / 100)
        if q1 > 0 and abs(q1 - round(q1)) < 1e-9:
            break
    else:
        return None
    y1 = y0 * (1 + dy / 100)
    cls = 'inferior good' if yed < 0 else 'necessity (income inelastic normal good)' if yed < 1 else 'luxury (income elastic normal good)'
    if yed < 0:
        g = rng.choice(['instant noodles', 'bus journeys', 'second-hand clothes', 'own-brand budget pasta'])
    elif yed < 1:
        g = rng.choice(['bread', 'rice', 'toothpaste', 'household electricity', 'milk'])
    else:
        g = rng.choice(['package holidays', 'restaurant meals', 'gym memberships', 'private tutoring', 'designer clothing'])
    who = rng.choice(['A household', 'The average household', 'A consumer survey shows that a typical family'])
    if slot.d <= 2:
        return dict(stem=f'{who} in {rng.choice(CITIES)} saw income change from ${y0:,} to ${int(y1):,} a year, and its consumption of {g} changed from {q0} to {int(round(q1))} units. Calculate the YED and classify the good.',
                    answer=f'YED = {r2(yed)}: {cls}', markingKey=f'%ΔQ = {r2(yed * dy)}%, %ΔY = {dy}% [1]; YED = {r2(yed * dy)}/{dy} = {r2(yed)}; {cls} [1].', type='numerical', marks=2)
    return dict(stem=f'National income per capita in a country {"rises" if dy > 0 else "falls"} by {abs(dy)}%{"" if dy > 0 else " in a recession"}. The YED for {g} is {r2(yed)} and current sales are {q0 * 100:,} units. Calculate the expected change in quantity demanded, classify the good, and explain one implication for firms selling it.',
                answer=f'{r2(yed * dy)}% change: {fmt(q0 * 100 * yed * dy / 100, 6)} units; {cls}',
                markingKey=f'%ΔQ = YED × %ΔY = {r2(yed)} × {dy} = {r2(yed * dy)}% [1]; change = {fmt(q0 * 100 * yed * dy / 100, 6)} units [1]; {cls} [1]; implication e.g. adjust production/stock, product range, marketing [1].', type='numerical', marks=4)

# =============================================================================================
# ch09 Unit 2.6 Elasticity of supply
# =============================================================================================
S('ch09-st1',
  terms=[("price elasticity of supply (PES)", "a measure of the responsiveness of quantity supplied to a change in the good's price, calculated as %ΔQs ÷ %ΔP"),
         ("price elastic supply", "supply for which PES > 1, so quantity supplied changes by a larger percentage than price"),
         ("price inelastic supply", "supply for which 0 < PES < 1, so quantity supplied changes by a smaller percentage than price"),
         ("perfectly inelastic supply", "supply for which PES = 0, shown by a vertical supply curve: quantity supplied is fixed, as with seats in a stadium"),
         ("perfectly elastic supply", "supply for which PES is infinite, shown by a horizontal supply curve: firms will supply any quantity at a given price"),
         ("unit elastic supply", "supply for which PES = 1; any straight-line supply curve through the origin has PES = 1")],
  facts=[("If price rises by 10% and quantity supplied rises by 4%, what is the PES?", "0.4 (inelastic)", ["2.5 (elastic)", "−0.4", "4 (elastic)"], "PES = 4/10 = 0.4."),
         ("Which of the following is true of any straight-line supply curve that passes through the origin?", "PES = 1 at every point", ["PES = 0", "PES is infinite", "PES falls along the curve"], "Along such a line Q is proportional to P, so percentage changes are equal."),
         ("Why is PES normally positive?", "Price and quantity supplied move in the same direction", ["Supply curves slope downwards", "Firms reduce output when prices rise", "Costs fall as output rises"], "The law of supply."),
         ("A straight-line supply curve that cuts the price axis has PES of which value?", "Greater than 1 (elastic)", ["Less than 1 (inelastic)", "Equal to 1", "Zero"], "Lines meeting the price axis are elastic; lines meeting the quantity axis are inelastic.")],
  why=[("Explain why the supply of seats for a concert at a stadium is perfectly inelastic.", "The number of seats is fixed in the short run; however high the price, no more seats can be supplied, so the supply curve is vertical (PES = 0)."),
       ("Explain why a linear supply curve that cuts the quantity axis is price inelastic.", "Such a line has a positive quantity at zero price, so a given percentage change in price produces a smaller percentage change in quantity; PES = (ΔQ/ΔP) × (P/Q) < 1 at every point."),
       ("Explain why PES matters for how a market responds to an increase in demand.", "If supply is elastic, firms expand output easily, so an increase in demand mainly raises quantity with a small price rise; if supply is inelastic, the same increase in demand mainly raises price.")],
  contrast=[("PES", "PED", "PED measures consumers' responsiveness to price (normally negative); PES measures producers' responsiveness to price (normally positive)."),
            ("perfectly elastic supply", "perfectly inelastic supply", "Perfectly elastic supply is horizontal: any quantity at the given price; perfectly inelastic supply is vertical: quantity is fixed whatever the price.")],
  misc=[("A steep supply curve through the origin is inelastic.", "Any straight-line supply curve through the origin has PES = 1 regardless of its slope."),
        ("PES of 0.5 means quantity supplied falls when price rises.", "PES is positive: quantity supplied rises, but by only half the percentage change in price.")],
  apply=[("The price of strawberries in Lisbon rose by 25% and the quantity supplied to the market rose by 5% within a week. Calculate PES and comment.", "PES = 5/25 = 0.2: very inelastic – farmers cannot quickly grow more strawberries in a week.", 2)],
  cases=[("hotel rooms in Edinburgh during the August festival season", "Room prices rise sharply every August as visitors arrive for the festivals, while the number of rooms in the city stays the same.", "price inelastic supply", "The stock of rooms is fixed in the short run, so higher demand mainly raised prices rather than quantity supplied.")],
  sources=[("When the average price of a three-bedroom house in Auckland rose by 20% between 2020 and 2021, the number of new homes completed rose by only 4%. Builders reported shortages of land with planning permission and of skilled workers.", "Extract based on housing-market reporting", "Calculate the PES for new homes and use the extract to explain the value.", "PES = 4/20 = 0.2: inelastic; shortages of land with planning permission and skilled labour, and long construction times, limit how fast supply can respond.")],
  evaluate=[("Increasing the price elasticity of supply is the best way to reduce price volatility in housing markets.", ["more elastic supply means demand shocks raise quantity rather than price", "planning reform and land release can raise PES"], ["housing supply is limited by land and construction time", "demand-side policies (interest rates, taxes on investors) can be quicker", "building more may conflict with environmental goals"], "Raising PES is important for long-run affordability, but in the short run demand-side policies are often needed as well.")],
  extended=[("Explain, using diagrams, the effect of an increase in demand on price and quantity when supply is (i) perfectly inelastic, (ii) price inelastic and (iii) price elastic.", "(i) vertical S: only price rises; (ii) steep S: large price rise, small quantity rise; (iii) flat S: small price rise, large quantity rise. Each diagram shows D1 to D2.", 6)],
  diag=[("how the price elasticity of supply affects the impact of an increase in demand on price and quantity", "Two diagrams: same rightward demand shift D1 to D2. With inelastic (steep) supply, price rises a lot (P1 to P2) and quantity a little; with elastic (flat) supply, price rises little and quantity a lot. Label PES < 1 and PES > 1.")])


PES_CTX = [('wheat farmers in Argentina', 'tonnes', 'per season'), ('a T-shirt factory in Dhaka', 'shirts', 'per week'), ('copper mines in Chile', 'tonnes', 'per month'),
           ('app developers in Bangalore', 'apps', 'per year'), ('dairy farms in New Zealand', 'litres of milk', 'per day'), ('a bakery in Vienna', 'loaves', 'per day'),
           ('salmon farms in Norway', 'tonnes', 'per year'), ('a solar-panel plant in Malaysia', 'panels', 'per week')]


@R.add('ch09-st1', 'C3', (1, 5), 'numerical')
def pes_calc(rng, slot):
    for _ in range(60):
        p0 = rng.choice([2, 4, 5, 10, 20, 50, 100])
        dp = rng.choice([-20, -10, 5, 10, 20, 25, 40, 50])
        e = rng.choice([0.1, 0.2, 0.4, 0.5, 0.8, 1, 1.2, 1.5, 2, 3])
        q0 = rng.choice([500, 1000, 2000, 4000, 5000, 10000])
        q1 = q0 * (1 + e * dp / 100)
        p1 = p0 * (1 + dp / 100)
        if q1 > 0 and abs(q1 - round(q1)) < 1e-9:
            break
    else:
        return None
    who, unit, per = rng.choice(PES_CTX)
    cls = 'unit elastic' if e == 1 else 'price elastic' if e > 1 else 'price inelastic'
    if slot.d <= 2:
        return dict(stem=f'When the price received by {who} changed from ${r2(p0)} to ${r2(p1)}, quantity supplied changed from {q0:,} to {int(round(q1)):,} {unit} {per}. Calculate the PES.',
                    answer=f'PES = {r2(e)} ({cls})', markingKey=f'%ΔQs = {r2(e * dp)}%, %ΔP = {dp}%; PES = {r2(e)}. [1] [1]', type='numerical', marks=2)
    return dict(stem=f'The PES for output from {who} is estimated at {r2(e)}. If the price rises by {abs(dp)}% from ${r2(p0)}, calculate the new quantity supplied (currently {q0:,} {unit} {per}), and explain one reason why supply might have this elasticity.',
                answer=f'{fmt(q0 * (1 + e * abs(dp) / 100), 6)} {unit}; {cls}',
                markingKey=f'%ΔQs = {r2(e)} × {abs(dp)} = {r2(e * abs(dp))}% [1]; new Q = {fmt(q0 * (1 + e * abs(dp) / 100), 6)} [1]; reason linked to time, spare capacity, stocks or factor mobility [2].', type='numerical', marks=4)


S('ch09-st2',
  terms=[("time period (as a determinant of PES)", "the longer the time producers have to respond to a price change, the more elastic supply becomes"),
         ("spare capacity", "the ability of a firm to increase output using existing equipment and workers that are not fully used, which makes supply more elastic"),
         ("mobility of factors of production", "the ease with which resources can be moved from one use to another; greater mobility makes supply more elastic"),
         ("stocks (inventories)", "goods held in storage that can be released onto the market quickly, increasing the elasticity of supply"),
         ("momentary period", "a period so short that supply is fixed and perfectly inelastic")],
  facts=[("Which of the following would make the supply of a good more price elastic?", "Large stocks of unsold goods in warehouses", ["A long production period", "Firms operating at full capacity", "Specialised, immobile labour"], "Stocks can be released quickly when price rises."),
         ("Why is the supply of fresh flowers on Valentine's Day relatively price inelastic?", "Flowers take time to grow and cannot be stored for long", ["Demand is elastic", "There are many flower sellers", "Flowers are a luxury"], "Production time and perishability limit the supply response."),
         ("In which time period is supply most price elastic?", "The long run", ["The momentary period", "The short run", "It is the same in every period"], "In the long run all factors can change and new firms can enter."),
         ("Which of the following is most likely to have price elastic supply?", "Mass-produced plastic toys", ["Rare paintings by Van Gogh", "Rubber from new plantations", "Beachfront land"], "Toy factories can quickly add shifts and materials are readily available.")],
  why=[("Explain why spare capacity makes supply more price elastic.", "A firm with idle machinery and workers can increase output quickly and without a large rise in costs when price rises, so quantity supplied responds strongly."),
       ("Explain why supply becomes more elastic over time.", "In the short run some factors are fixed and firms can only use existing capacity; in the long run they can build new capacity, hire and train workers and new firms can enter."),
       ("Explain how the mobility of factors of production affects PES.", "If labour and capital can easily switch between uses (e.g. a factory switching from one garment to another), firms can quickly increase output of the good whose price rises, making supply elastic.")],
  contrast=[("the short run", "the long run (for PES)", "In the short run at least one factor is fixed so supply is relatively inelastic; in the long run all factors can change and firms can enter or leave, so supply is more elastic."),
            ("goods that can be stored", "perishable goods", "Storable goods can be released from stocks when price rises, so supply is more elastic; perishable goods cannot be stored, so supply is more inelastic.")],
  misc=[("Supply is always more elastic for expensive goods.", "PES depends on time, spare capacity, stocks and factor mobility, not on whether a good is expensive."),
        ("If a factory is working at full capacity, its supply is perfectly elastic.", "At full capacity, output cannot rise easily, so supply is inelastic in the short run.")],
  apply=[("Explain why the supply of electricity from gas-fired power stations is more price elastic than from nuclear power stations.", "Gas plants can be switched on and off quickly to raise output when prices rise; nuclear stations run at a constant level and cannot easily increase output, so their supply is inelastic.", 3)],
  cases=[("the shortage of semiconductors in 2021", "Car makers faced chip shortages for over a year because building a new fabrication plant takes 2-3 years and costs over $10 billion.", "time and capacity as determinants of PES", "Supply was inelastic in the short run because capacity was fully used and new plants take years to build.")],
  evaluate=[("Time is the most important determinant of the price elasticity of supply.", ["in the long run new capacity and firms enter (all goods)", "explains why commodity supply responds slowly"], ["spare capacity allows a quick response even in the short run", "stocks and storability matter for many goods", "some supplies are fixed whatever the time (land, rare art)"], "Time is usually the most important determinant because it governs the ability to change all inputs, but stocks and spare capacity determine short-run responses.")],
  extended=[("A sudden rise in demand increases the price of bicycles. Explain how the PES of bicycles might differ in the momentary period, the short run and the long run.", "Momentary: only existing stock – very inelastic; short run: overtime, use of spare capacity – more elastic; long run: new factories, new firms – elastic. Diagram with three supply curves pivoting through the original equilibrium.", 6)],
  diag=[("how the price elasticity of supply changes over time after an increase in demand", "Diagram: three supply curves through the original equilibrium – vertical momentary supply, steeper short-run supply, flatter long-run supply. After demand shifts right, price rises most in the momentary period and least in the long run, while quantity rises most in the long run.")])


S('ch09-st3',
  terms=[("primary commodity", "an unprocessed product of agriculture, fishing, forestry or mining, such as coffee, wheat, copper or oil"),
         ("manufactured product", "a good produced in the secondary sector by processing raw materials, often in factories"),
         ("gestation period", "the time needed for agricultural production to respond, such as growing trees or raising livestock"),
         ("price volatility", "large and frequent fluctuations in price, common in primary commodity markets because of inelastic demand and supply")],
  facts=[("Which of the following best explains why PES for coffee is low?", "Coffee plants take three to four years to start producing", ["Coffee is a necessity", "Demand for coffee is inelastic", "Coffee is produced in many countries"], "Long gestation periods prevent a quick supply response."),
         ("Why is PES for manufactured goods usually higher than for primary commodities?", "Factories can increase output quickly by adding shifts, using stocks and spare capacity", ["Manufactured goods are cheaper", "Manufactured goods have elastic demand", "Manufacturing uses no natural resources"], "Manufacturing is less dependent on fixed natural resources and growing seasons."),
         ("Low PES combined with low PED in commodity markets results in which of the following?", "Large price fluctuations when demand or supply shifts", ["Stable prices", "Constant revenues for producers", "Perfectly elastic demand"], "Steep curves mean small shifts cause large price changes.")],
  why=[("Explain why the supply of agricultural products is price inelastic in the short run.", "Crops and livestock take time to grow; once planted, output is fixed until harvest, land is limited and weather affects yields, so farmers cannot respond quickly to price changes."),
       ("Explain why mining output can take years to respond to higher prices.", "Opening a new mine requires exploration, permits, large investment and construction; capacity is fixed in the short run, so supply is inelastic."),
       ("Explain how low PES contributes to income instability for commodity-exporting countries.", "Low PES (and PED) mean shocks cause large price swings; because export revenues depend on prices, incomes, government revenue and the exchange rate fluctuate.")],
  contrast=[("PES for primary commodities", "PES for manufactured products", "Commodities have low PES because of growing times, fixed land and long investment lead times; manufactured goods have higher PES because factories can use spare capacity, stocks and mobile factors to raise output quickly."),
            ("price volatility", "a long-term price trend", "Volatility refers to short-term fluctuations up and down; a trend is the direction of prices over many years.")],
  misc=[("Because commodity prices are volatile, PES for commodities must be high.", "Volatility results from low (inelastic) PES and PED: small shifts in curves cause large price changes."),
        ("Farmers can quickly increase supply when prices rise because land is always available.", "Land is limited and crops take time to grow, so supply is inelastic in the short run.")],
  apply=[("Explain why the world price of cocoa rose to over $10,000 per tonne in 2024 after poor harvests in West Africa.", "Cocoa supply is price inelastic (new trees take years to mature, disease and weather limit output) and demand is inelastic, so a leftward supply shift caused a very large price rise.", 3)],
  cases=[("the 2014-2016 collapse in oil prices", "Oil prices fell from over $100 to under $30 a barrel as US shale output grew and OPEC did not cut production.", "low PES and price volatility in primary commodity markets", "With inelastic short-run demand and supply, rising supply caused a dramatic fall in price.")],
  evaluate=[("Buffer stock schemes are the best way to stabilise primary commodity prices.", ["buying in surplus years and selling in shortage years reduces volatility", "stabilises farmers' incomes"], ["expensive storage and administration", "difficult to set the right target price; schemes such as the International Tin Agreement collapsed in 1985", "perishable goods cannot be stored"], "Buffer stocks can reduce short-term volatility for storable goods but have often failed because of cost and mis-set prices; diversification and insurance may be better long-term solutions.")],
  diag=[("why the prices of primary commodities are more volatile than the prices of manufactured goods", "Two diagrams. Commodity: steep (inelastic) demand and supply; a supply shift (e.g. bad harvest) causes a large price change. Manufactured good: flatter (elastic) supply; the same demand or supply shift causes a smaller price change and a larger quantity change.")])


@R.add('ch09-st3', 'C3', (2, 5), 'numerical')
def pes_compare(rng, slot):
    dp = rng.choice([10, 20, 25, 40])
    c_e = rng.choice([0.1, 0.2, 0.3, 0.4])
    m_e = rng.choice([1.2, 1.5, 2, 2.5])
    comm = rng.choice(['coffee', 'cocoa', 'copper', 'rubber', 'palm oil'])
    man = rng.choice(['bicycles', 'plastic chairs', 'smartphone cases', 'T-shirts', 'kettles'])
    q = rng.choice([1000, 5000, 10000])
    return dict(stem=f'Over one year the price of {comm} rose by {dp}% and the quantity supplied rose by {r2(c_e * dp)}%. Over the same year the price of {man} rose by {dp}% and the quantity supplied rose by {r2(m_e * dp)}%. Calculate the PES for each product and explain the difference.',
                answer=f'{comm}: PES = {r2(c_e)}; {man}: PES = {r2(m_e)}',
                markingKey=f'{comm}: {r2(c_e * dp)}/{dp} = {r2(c_e)} [1]; {man}: {r2(m_e * dp)}/{dp} = {r2(m_e)} [1]; commodity supply inelastic because of gestation periods/fixed land or long mine lead times, manufacturing elastic because of spare capacity, stocks and factor mobility [2].', type='numerical', marks=4)

# =============================================================================================
# ch10 Unit 2.7 Role of government in microeconomics
# =============================================================================================
S('ch10-st1',
  terms=[("government intervention", "action by the government to change market outcomes, using taxes, subsidies, price controls, regulation, direct provision or nudges"),
         ("indirect tax", "a tax on spending on goods and services, paid by firms to the government and partly passed on to consumers"),
         ("regulation", "rules imposed by the government on the behaviour of firms and consumers, such as bans, standards and licences"),
         ("direct provision", "the supply of goods and services by the government itself, such as state schools and public parks"),
         ("government failure", "a situation where government intervention leads to a less efficient allocation of resources than the market outcome")],
  facts=[("Which of the following is NOT a main reason for government intervention in markets?", "To maximise the profits of large firms", ["To correct market failure", "To raise revenue", "To promote equity"], "Governments intervene to raise revenue, support firms/households, influence consumption and production, correct market failure and promote equity."),
         ("Which of the following is an example of a commodity agreement or support for farmers?", "A guaranteed minimum price for wheat", ["A tax on cigarettes", "A ban on smoking in restaurants", "A carbon tax"], "Price floors support producers' incomes."),
         ("Which of the following is an example of direct provision?", "A government-run public hospital", ["A tax on alcohol", "A subsidy for electric cars", "A ban on lead in petrol"], "The government itself supplies the service.")],
  why=[("Explain why governments intervene in markets to support firms in particular industries.", "To protect jobs, encourage strategic industries (e.g. semiconductors, renewable energy), help infant industries grow or support firms through shocks, using subsidies, tax breaks or price support."),
       ("Explain why governments might intervene to change the consumption of particular goods.", "Some goods are over-consumed (demerit goods such as tobacco) or under-consumed (merit goods such as education) because of externalities or imperfect information; taxes, subsidies, regulation or information campaigns can move consumption towards the socially optimal level."),
       ("Explain how government intervention can lead to government failure.", "Governments may lack information, face political pressures, create unintended consequences (e.g. black markets under price ceilings) or administer policies at high cost, so the outcome may be worse than the market.")],
  contrast=[("market-based policies", "command-and-control policies", "Market-based policies (taxes, subsidies, tradable permits) change incentives through prices; command-and-control policies (regulation, bans, standards) directly require or forbid behaviour."),
            ("market failure", "government failure", "Market failure is when the free market allocates resources inefficiently; government failure is when intervention makes the allocation worse.")],
  misc=[("Government intervention always improves market outcomes.", "Intervention can cause government failure through poor information, unintended consequences, administrative costs or political motives."),
        ("Indirect taxes are only used to raise revenue.", "Indirect taxes also aim to discourage consumption of harmful goods and correct negative externalities (e.g. carbon and sugar taxes).")],
  apply=[("Identify the type of government intervention in each case: (i) a tax on plastic bags in Kenya; (ii) free primary schooling in Uganda; (iii) a ban on single-use plastic straws in the EU; (iv) a subsidy for public transport in Germany (the €49 Deutschlandticket).", "(i) indirect tax; (ii) direct provision; (iii) regulation; (iv) subsidy.", 2)],
  cases=[("Germany's €49 Deutschlandticket introduced in 2023", "A subsidised monthly ticket allowing unlimited regional and local public transport, funded jointly by federal and state governments.", "subsidies as a form of government intervention", "The subsidy lowers the price of public transport to encourage use, reducing congestion and emissions, at a cost to taxpayers.")],
  sources=[("In 2022 several EU governments cut fuel taxes and capped energy bills to protect households from rising prices. Critics argued the measures cost billions of euros, helped high-income households most because they consume more energy, and weakened the incentive to save energy.", "Extract based on reporting of EU energy policies, 2022", "Using the extract, explain two reasons for, and one possible consequence of, the government intervention.", "Reasons: protect households' real incomes (equity) and support firms; consequence: high fiscal cost / weaker price signal reducing incentives to save energy / poorly targeted support (government failure).")],
  evaluate=[("Market-based policies are more effective than regulation in changing behaviour.", ["taxes and subsidies use the price mechanism and allow flexibility", "raise revenue", "encourage cost-effective changes (firms that can cut cheaply do most)"], ["regulation gives certainty (bans on dangerous products)", "effects of taxes depend on PED", "monitoring and enforcement still needed"], "Market-based policies are often more efficient, but regulation is better when harm is severe or certainty is required; combinations are common.")],
  diag=[("how an indirect tax can be used to reduce the consumption of a good", "Diagram: market for sugary drinks; specific tax shifts supply from S to S + tax (vertical distance = tax). Price paid by consumers rises from Pe to Pc, quantity falls from Qe to Qt; producers receive Pp = Pc − tax; government revenue = tax × Qt.")])


S('ch10-st2',
  terms=[("price ceiling (maximum price)", "a legal maximum price set by the government below the equilibrium price to make a good more affordable"),
         ("price floor (minimum price)", "a legal minimum price set by the government above the equilibrium price to raise producers' incomes"),
         ("shortage", "a situation where quantity demanded exceeds quantity supplied at the controlled price"),
         ("parallel (black) market", "an illegal market in which goods are sold at prices above the legal maximum"),
         ("minimum wage", "a legal floor on the wage rate employers can pay workers"),
         ("non-price rationing", "methods of allocating a good when price cannot do so, such as queues, waiting lists, lotteries or favouritism")],
  facts=[("A price ceiling is effective only if it is set at which level?", "Below the equilibrium price", ["Above the equilibrium price", "At the equilibrium price", "At zero"], "A ceiling above equilibrium does not bind."),
         ("Which of the following is a likely consequence of a price floor in agriculture?", "A surplus that the government may need to buy and store", ["A shortage of the product", "Lower prices for consumers", "A black market selling below the floor only"], "Qs > Qd at the floor price."),
         ("Which of the following is a likely consequence of rent controls in the long run?", "A fall in the quality and quantity of rental housing", ["An increase in the supply of rental housing", "Lower demand for housing", "A surplus of rental flats"], "Landlords have less incentive to maintain or build rental housing."),
         ("Scotland's minimum unit price for alcohol is an example of which of the following?", "A price floor", ["A price ceiling", "A subsidy", "A specific tax"], "It sets a minimum price per unit of alcohol (50p from 2018, 65p from 2024).")],
  why=[("Explain why a price ceiling leads to a shortage.", "Set below equilibrium, the lower price increases quantity demanded and reduces quantity supplied, so Qd > Qs; the price cannot rise to clear the market."),
       ("Explain why a price ceiling may lead to a parallel market.", "Consumers who cannot buy at the legal price are willing to pay more than the ceiling for the limited supply, so some sellers sell illegally at higher prices."),
       ("Explain why a minimum wage might increase unemployment.", "Set above the equilibrium wage, it raises the quantity of labour supplied and reduces the quantity demanded by employers, creating a surplus of labour (unemployment), especially among low-skilled workers."),
       ("Explain why governments often need to buy the surplus created by an agricultural price floor.", "At the floor price farmers produce more than consumers want; to maintain the floor the government must buy the excess, which it then stores, destroys or sells abroad, at a cost to taxpayers.")],
  contrast=[("a price ceiling", "a price floor", "A price ceiling is a legal maximum set below equilibrium and causes a shortage; a price floor is a legal minimum set above equilibrium and causes a surplus."),
            ("allocative inefficiency from a price ceiling", "allocative inefficiency from a price floor", "A ceiling reduces quantity traded to Qs below the efficient level; a floor reduces quantity bought to Qd and, if the government buys the surplus, resources are used to produce output nobody wants – both create welfare loss.")],
  misc=[("A price ceiling set above the equilibrium price causes a shortage.", "A ceiling above equilibrium is not binding: the market simply clears at the equilibrium price below the ceiling."),
        ("Price controls help all consumers because prices are lower.", "Consumers who obtain the good at the lower price gain, but those who cannot buy it because of the shortage lose, and quality may fall; black markets may also develop.")],
  apply=[("Berlin froze rents for five years in 2020 (the Mietendeckel), before the law was overturned in 2021. Predict two consequences of such a policy.", "Shortage of rental flats (more demand, fewer flats offered for rent – some converted to owner-occupation); queues and long searches, fall in maintenance, black-market payments, less new construction.", 3),
         ("Explain one advantage and one disadvantage of a minimum wage for low-paid workers.", "Advantage: higher income for those who keep their jobs, reducing poverty and inequality; disadvantage: possible job losses or fewer hours as employers demand less labour.", 2)],
  cases=[("Venezuela's price controls on basic foods", "Prices of flour, milk and other staples were fixed below market levels; by 2016 shelves were empty and long queues formed.", "the consequences of price ceilings", "Price below equilibrium cut quantity supplied and raised quantity demanded, creating shortages and black markets."),
         ("Scotland's minimum unit price for alcohol (2018)", "A minimum price of 50p per unit of alcohol was introduced; a later evaluation estimated it reduced alcohol-related deaths by about 13%.", "price floors to reduce consumption of a demerit good", "By raising the price of the cheapest, strongest drinks, the floor reduced consumption among heavy drinkers."),
         ("the EU's Common Agricultural Policy in the 1980s", "Guaranteed prices led to large surpluses known as 'butter mountains' and 'wine lakes' that the EU bought and stored.", "the consequences of price floors in agriculture", "Prices above equilibrium encouraged over-production; the surplus cost taxpayers and was sometimes dumped on world markets.")],
  sources=[("In 2022 Germany raised its national minimum wage from €9.82 to €12 an hour, an increase of about 22%. The government estimated that around 6 million workers would benefit. Some small businesses in hospitality said they would cut hours or raise prices.", "Extract based on reporting of Germany's minimum wage increase", "Using a diagram, explain the possible effect of the higher minimum wage on the labour market.", "Labour market diagram: wage on vertical axis, quantity of labour on horizontal; the minimum wage set above equilibrium raises quantity supplied and reduces quantity demanded, creating a surplus of labour (unemployment); the size depends on elasticities; workers who keep jobs earn more.")],
  evaluate=[("Rent controls are an effective way to make housing affordable.", ["lower rents for existing tenants", "protects low-income households from rapid rent rises", "greater security of tenure"], ["shortages and long waiting lists", "less investment in maintenance and new rental housing", "black markets and discrimination between tenants", "benefits not targeted at the poorest"], "Rent controls help sitting tenants in the short run, but in the long run they reduce supply; increasing housing supply and targeted subsidies are usually more effective."),
            ("Minimum wages do more good than harm.", ["raise incomes of low-paid workers and reduce in-work poverty", "may increase productivity and reduce staff turnover", "evidence (Card and Krueger; UK national living wage) suggests small employment effects"], ["may cause unemployment for low-skilled and young workers", "higher prices for consumers", "may encourage informal employment in developing countries"], "Moderate minimum wages appear to raise incomes with little job loss, but very high minimum wages relative to median wages risk unemployment.")],
  extended=[("Using a diagram, explain the effects of a maximum price on rice on consumers, producers and the government.", "Ceiling below equilibrium: Qd rises, Qs falls, shortage; consumers who buy pay less (gain), those who cannot buy lose; producers receive lower price and revenue; government may need to ration, subsidise producers or provide rice directly; black markets; welfare loss.", 6)],
  diag=[("the effects of a maximum price (price ceiling) on the market for a staple food", "Diagram: D and S intersect at Pe, Qe; ceiling Pc below Pe. At Pc, Qd > Qs: shortage = Qd − Qs. Quantity traded falls to Qs. Consumer surplus changes (some gain, some lose), producer surplus falls, welfare loss triangle between D and S from Qs to Qe. Possible parallel market price above Pc."),
        ("the effects of a minimum price (price floor) on an agricultural market when the government buys the surplus", "Diagram: floor Pf above Pe. Qs rises to Qs, Qd falls to Qd: surplus Qs − Qd bought by the government at cost Pf × (Qs − Qd). Consumers pay more and buy less; producers gain revenue; allocative inefficiency (over-allocation of resources) and welfare loss.")])


@R.add('ch10-st2', 'C3', (1, 5), 'numerical')
def price_control(rng, slot):
    m = market(rng)
    if not m:
        return None
    a, b, c, d, P, Q = m
    intro, g = mkt_intro(rng, a, b, c, d)
    ceiling = rng.random() < 0.5
    for _ in range(20):
        k = rng.randint(1, max(1, min(6, P - 1)))
        pc = P - k if ceiling else P + k
        qd, qs = a - b * pc, c + d * pc
        if qd > 0 and qs > 0:
            break
    else:
        return None
    if ceiling:
        if slot.d <= 2:
            return dict(stem=f'{intro} The government sets a maximum price of ${pc}. Calculate the resulting shortage.', answer=str(qd - qs),
                        markingKey=f'Qd = {qd}, Qs = {qs} at ${pc}; shortage = {qd - qs}. [1] [1]', type='numerical', marks=2)
        return dict(stem=f'{intro} The government sets a maximum price of ${pc}. Calculate the equilibrium, the shortage at the maximum price, and the change in producers\' total revenue. Outline one likely consequence of the shortage.',
                    answer=f'Equilibrium P = ${P}, Q = {Q}; shortage = {qd - qs}; producer revenue falls from {P * Q} to {pc * qs}',
                    markingKey=f'Equilibrium P = {P}, Q = {Q} [1]; at ${pc}: Qd = {qd}, Qs = {qs}, shortage {qd - qs} [1]; revenue {P}×{Q} = {P * Q} → {pc}×{qs} = {pc * qs} [1]; consequence: queues, black market, rationing, lower quality [1].', type='numerical', marks=4)
    if slot.d <= 2:
        return dict(stem=f'{intro} The government sets a minimum price of ${pc}. Calculate the surplus.', answer=str(qs - qd),
                    markingKey=f'Qs = {qs}, Qd = {qd}; surplus = {qs - qd}. [1] [1]', type='numerical', marks=2)
    return dict(stem=f'{intro} The government sets a minimum price of ${pc} and buys any surplus. Calculate the surplus, the cost to the government of buying it, and the change in consumer expenditure.',
                answer=f'Surplus = {qs - qd}; government cost = {pc * (qs - qd)}; consumer expenditure changes from {P * Q} to {pc * qd}',
                markingKey=f'Equilibrium P = {P}, Q = {Q} [1]; at ${pc}: Qs = {qs}, Qd = {qd}, surplus {qs - qd} [1]; cost {pc} × {qs - qd} = {pc * (qs - qd)} [1]; consumer spending {P * Q} → {pc}×{qd} = {pc * qd} [1].', type='numerical', marks=4)


def A(key, *items):
    R.f[key].apply.extend(items)


def C(key, *items):
    R.f[key].cases.extend(items)


X('ch09-st2', ("After a viral social-media trend in 2023, the price of a particular brand of insulated water bottle doubled on resale sites. The manufacturer said it could not raise output for several months because its factories in China were already running 24 hours a day and new moulds took time to make.", "Extract based on news reporting", "Using the extract, explain why the supply of the bottles was price inelastic in the short run.", "The factories had no spare capacity (already at full use) and new equipment takes time to produce, so quantity supplied could not respond quickly to the higher price: PES was low in the short run."))
C('ch09-st2', ("the global response to demand for Covid-19 vaccines in 2021", "Vaccine output was initially limited, but within a year manufacturers had converted and built plants and supplied billions of doses.", "how PES increases over time", "Supply was very inelastic in the first months but became much more elastic as new capacity was built and factors were moved into production."))
A('ch09-st2', ("A publisher can reprint a best-selling novel within a week, while a vineyard in Chile needs years to plant new vines. Compare the PES of the two products.", "The novel's supply is elastic (spare printing capacity, mobile factors, quick production); the wine's supply is inelastic because new vines take years to mature.", 2))
E('ch09-st2', ("Firms should always hold large stocks so that their supply is price elastic.", ["stocks allow firms to respond quickly to price rises and gain revenue", "reduces the risk of shortages"], ["storage costs, waste and obsolescence", "ties up working capital", "perishable goods cannot be stored"], "Holding stocks increases PES, but the optimal level balances responsiveness against storage and financing costs."))


@R.add('ch09-st2', 'C3', (2, 5), 'numerical')
def pes_time(rng, slot):
    g = rng.choice(['bicycles in Amsterdam', 'Christmas trees in Toronto', 'face masks in Seoul', 'cement in Nairobi', 'avocados in Lima', 'rental scooters in Lisbon'])
    dp = rng.choice([10, 20, 25, 50])
    q0 = rng.choice([1000, 2000, 5000, 10000])
    es = sorted(rng.sample([0, 0.2, 0.4, 0.5, 0.8, 1.2, 1.5, 2], 3))
    qs = [q0 * (1 + e * dp / 100) for e in es]
    return dict(stem=f'The price of {g} rose by {dp}% from an initial quantity supplied of {q0:,} units. Quantity supplied was {fmt(qs[0], 6)} after one week, {fmt(qs[1], 6)} after six months and {fmt(qs[2], 6)} after three years. Calculate PES for each period and explain the pattern.',
                answer=f'PES = {r2(es[0])}, {r2(es[1])}, {r2(es[2])}',
                markingKey=f'%ΔQs each period / {dp}%: {r2(es[0])}, {r2(es[1])}, {r2(es[2])} [2]; supply becomes more elastic over time as firms add capacity, workers and new firms enter [2].', type='numerical', marks=4)

S('ch10-st3',
  terms=[("specific (excise) tax", "an indirect tax of a fixed amount per unit of a good, which shifts the supply curve up parallel by the amount of the tax"),
         ("ad valorem tax", "an indirect tax charged as a percentage of the price, such as VAT, which shifts the supply curve up by a widening amount as price rises"),
         ("incidence of a tax", "how the burden of a tax is shared between consumers (higher price paid) and producers (lower price received)"),
         ("per-unit subsidy", "a payment by the government to producers for each unit produced, which shifts the supply curve down by the amount of the subsidy"),
         ("welfare (deadweight) loss of a tax", "the loss of social surplus caused by the reduction in quantity below the free-market equilibrium, not offset by tax revenue")],
  facts=[("How does an ad valorem tax shift the supply curve?", "Upwards, with the gap between the curves widening as price rises", ["Upwards by a constant amount", "Downwards by the tax rate", "It shifts the demand curve to the left"], "A percentage tax is larger in absolute terms at higher prices."),
         ("Who gains from a per-unit subsidy to producers?", "Both consumers (lower price) and producers (higher price received)", ["Only producers", "Only consumers", "Only the government"], "The subsidy is shared according to elasticities."),
         ("If demand is perfectly inelastic, who bears the full burden of a specific tax?", "Consumers", ["Producers", "The government", "It is shared equally"], "Quantity does not fall and price rises by the full tax."),
         ("Which of the following is the government revenue from a specific tax?", "Tax per unit × quantity sold after the tax", ["Tax per unit × original quantity", "New price × new quantity", "The welfare loss triangle"], "Revenue is the rectangle between the consumer and producer prices up to the new quantity.")],
  why=[("Explain why an indirect tax causes a welfare loss.", "The tax raises the price paid and lowers the price received, reducing quantity below the free-market level; units between the new and original quantity, which consumers valued above their cost, are no longer produced, so social surplus is lost beyond the revenue raised."),
       ("Explain why producers bear a larger share of a tax when demand is price elastic.", "If consumers are very responsive to price, firms cannot pass much of the tax on without losing many sales; the price paid rises only a little and the price producers receive falls by most of the tax."),
       ("Explain why a subsidy may lead to an over-allocation of resources.", "In a market without externalities the subsidy increases output beyond the free-market equilibrium where MB = MC; the extra units cost more to produce than consumers value them, causing a welfare loss and an opportunity cost for taxpayers."),
       ("Explain why governments subsidise producers of goods such as solar panels.", "To lower costs and prices, increase production and consumption of goods with positive externalities, support strategic industries and jobs, and help meet climate targets.")],
  contrast=[("a specific tax", "an ad valorem tax", "A specific tax is a fixed amount per unit, shifting supply up in parallel; an ad valorem tax is a percentage of price, so the vertical shift increases with price (curves diverge)."),
            ("the consumer burden of a tax", "the producer burden", "The consumer burden is the increase in price paid per unit times quantity sold; the producer burden is the fall in price received per unit times quantity.")],
  misc=[("When a specific tax of $2 is imposed, the price consumers pay always rises by $2.", "The price paid rises by the full $2 only if demand is perfectly inelastic or supply perfectly elastic; normally the burden is shared and the price rises by less than $2."),
        ("Subsidies only benefit producers because the money is paid to them.", "The subsidy shifts supply down, lowering the price consumers pay, so consumers also gain; the split depends on elasticities.")],
  apply=[("The EU applies VAT of around 20% on most goods. Explain whether VAT is a specific or an ad valorem tax and how it affects the supply curve.", "Ad valorem (a percentage of price); supply shifts upwards with a gap that widens as price rises.", 2),
         ("India subsidises fertiliser so that farmers pay well below the cost of production. Outline one benefit and one cost of this subsidy.", "Benefit: lower costs for farmers, higher crop output and food security; cost: large fiscal burden (opportunity cost), overuse of fertiliser damaging soil and water.", 3)],
  cases=[("the UK Soft Drinks Industry Levy (2018)", "A tax of 18p per litre on drinks with 5g+ sugar per 100ml and 24p for 8g+ led many firms to reformulate; the sugar sold in soft drinks fell by around 35-45%.", "the effects of a specific tax", "The tax increased costs for high-sugar drinks; firms avoided it by cutting sugar, so consumption of sugar fell while revenue was lower than forecast."),
         ("US subsidies for corn ethanol", "Subsidies and mandates have led to around 40% of the US corn crop being used for ethanol.", "the effects of subsidies", "The subsidy increased supply and production, but diverted land from food crops, raised corn prices and imposed costs on taxpayers.")],
  sources=[("In 2022 Indonesia spent over $30 billion on fuel subsidies, keeping petrol prices far below world levels. In September 2022 the government raised subsidised petrol prices by about 30%, arguing that most of the subsidy benefited wealthier households who own cars.", "Extract based on reporting of Indonesia's fuel subsidies", "Using the extract, explain two disadvantages of the fuel subsidy.", "Large fiscal cost/opportunity cost of $30bn (could fund health, education); poorly targeted – benefits richer car owners (inequity); also over-consumption of fuel and emissions (negative externality).")],
  evaluate=[("Indirect taxes are the best way to reduce consumption of harmful products.", ["raise price and reduce quantity", "generate revenue that can fund health services", "firms may reformulate (sugar levy)"], ["inelastic demand limits the effect", "regressive impact on low-income households", "smuggling and black markets", "regulation or education may be more effective for addictive goods"], "Taxes can reduce consumption and raise revenue, but their effectiveness depends on PED and they work best alongside regulation and education."),
            ("Subsidies to producers are a waste of taxpayers' money.", ["opportunity cost of government spending", "firms may become inefficient and dependent", "can cause overproduction and welfare loss"], ["correct positive externalities (renewable energy, vaccines)", "support strategic industries and employment", "lower prices for consumers of necessities"], "Subsidies are justified where there are positive externalities or strategic needs, but should be targeted, time-limited and evaluated.")],
  extended=[("Using a diagram, explain the effect of a per-unit subsidy on consumers, producers, the government and society.", "Supply shifts down by the subsidy; price paid by consumers falls (consumer gain), price received by producers rises (producer gain), quantity increases; government spending = subsidy × new quantity; welfare loss if no externality because cost of subsidy exceeds gains to consumers and producers.", 6)],
  diag=[("the effects of a specific tax on the market for cigarettes, including the incidence of the tax", "Diagram: steep (inelastic) demand; supply S shifts up to S + tax. Consumer price rises from Pe to Pc, producer price falls to Pp = Pc − tax, quantity falls from Qe to Qt. Tax revenue = (Pc − Pp) × Qt; consumer burden (Pc − Pe) × Qt is larger than producer burden (Pe − Pp) × Qt because demand is inelastic; welfare loss triangle between Qt and Qe."),
        ("the effects of a subsidy on producers of a good such as electric buses", "Diagram: supply shifts down from S to S − subsidy; price to consumers falls from Pe to Pc, price received by producers rises to Pp = Pc + subsidy, quantity rises from Qe to Qs. Government spending = subsidy × Qs; gains to consumers and producers are shown, and a welfare loss triangle if there are no external benefits.")])


@R.add('ch10-st3', 'C3', (2, 5), 'numerical')
def tax_calc(rng, slot):
    m = market(rng)
    if not m:
        return None
    a, b, c, d, P, Q = m
    for t in rng.sample([1, 2, 3, 4, 5, 6, 8, 10], 8):
        Pc = (a - c + d * t) / (b + d)
        if abs(Pc - round(Pc)) < 1e-9 and a - b * Pc > 0:
            break
    else:
        return None
    Pc = int(round(Pc))
    Qt = a - b * Pc
    Pp = Pc - t
    intro, g = mkt_intro(rng, a, b, c, d)
    rev = t * Qt
    dwl = 0.5 * t * (Q - Qt)
    if slot.d <= 3:
        return dict(stem=f'{intro} A specific tax of ${t} per unit is imposed on producers. Calculate the new price paid by consumers, the price received by producers and the government\'s tax revenue.',
                    answer=f'Pc = ${Pc}, Pp = ${Pp}, revenue = {rev}',
                    markingKey=f'New supply: Qs = {c} + {d}(P − {t}) [1]; {a} − {b}P = {c - d * t} + {d}P ⇒ Pc = {Pc}, Q = {Qt} [1]; Pp = {Pc} − {t} = {Pp} [1]; revenue = {t} × {Qt} = {rev} [1].', type='numerical', marks=4)
    return dict(stem=f'{intro} A specific tax of ${t} per unit is imposed. Calculate (i) the change in consumer expenditure, (ii) the change in producer revenue (after tax), (iii) government revenue and (iv) the welfare loss.',
                answer=f'(i) {P * Q} → {Pc * Qt}; (ii) {P * Q} → {Pp * Qt}; (iii) {rev}; (iv) {fmt(dwl, 6)}',
                markingKey=f'Equilibrium {P}, {Q}; with tax Pc = {Pc}, Pp = {Pp}, Q = {Qt} [1]; consumer expenditure {P}×{Q} = {P * Q} → {Pc}×{Qt} = {Pc * Qt} [1]; producer revenue {Pp}×{Qt} = {Pp * Qt} [1]; tax revenue {t}×{Qt} = {rev} [1]; welfare loss ½ × {t} × ({Q} − {Qt}) = {fmt(dwl, 6)} [2].', type='numerical', marks=6)


@R.add('ch10-st3', 'C3', (2, 5), 'numerical')
def subsidy_calc(rng, slot):
    m = market(rng)
    if not m:
        return None
    a, b, c, d, P, Q = m
    for s in rng.sample([1, 2, 3, 4, 5, 6], 6):
        Pc = (a - c - d * s) / (b + d)
        if abs(Pc - round(Pc)) < 1e-9 and Pc > 0:
            break
    else:
        return None
    Pc = int(round(Pc))
    Qs = a - b * Pc
    Pp = Pc + s
    intro, g = mkt_intro(rng, a, b, c, d)
    return dict(stem=f'{intro} The government grants producers a subsidy of ${s} per unit. Calculate the new price paid by consumers, the price received by producers, the new quantity and the total cost of the subsidy to the government.',
                answer=f'Pc = ${Pc}, Pp = ${Pp}, Q = {Qs}, cost = {s * Qs}',
                markingKey=f'New supply Qs = {c} + {d}(P + {s}) [1]; solve: Pc = {Pc}, Q = {Qs} [1]; Pp = {Pc} + {s} = {Pp} [1]; cost = {s} × {Qs} = {s * Qs} [1].', type='numerical', marks=4)


S('ch10-st4',
  terms=[("stakeholder", "an individual or group affected by a market outcome or policy, such as consumers, producers, workers, the government and society"),
         ("consumer expenditure", "the total amount spent by consumers on a good, equal to the price paid × quantity bought"),
         ("producer revenue", "the amount received by producers, equal to the price received (after any tax or including any subsidy) × quantity sold"),
         ("government expenditure on a subsidy", "the subsidy per unit multiplied by the quantity produced after the subsidy"),
         ("welfare loss triangle", "the area between the demand and supply curves over the units no longer traded (or over-produced) because of intervention")],
  facts=[("A price floor of $10 leads to Qs = 500 and Qd = 300. If the government buys the surplus, what does it spend?", "$2,000", ["$3,000", "$5,000", "$8,000"], "Surplus = 200; cost = 200 × $10."),
         ("With a $3 tax, Pc = $11, Pp = $8 and Q = 400. What is the tax revenue?", "$1,200", ["$4,400", "$3,200", "$3,600"], "3 × 400 = 1,200."),
         ("A $2 subsidy leads to Q = 600. What is the government's expenditure?", "$1,200", ["$600", "$300", "$2,400"], "Subsidy × quantity = 2 × 600."),
         ("If Pe = $20 and Qe = 100, and after a tax Pc = $23 and Q = 80, what is the change in consumer expenditure?", "It falls by $160", ["It rises by $160", "It rises by $300", "It is unchanged"], "Before 2,000; after 23 × 80 = 1,840.")],
  why=[("Explain why the government revenue from a tax is less than the tax per unit multiplied by the original quantity.", "The tax raises the price paid and reduces quantity bought; revenue is the tax per unit times the new, lower quantity."),
       ("Explain why calculating the welfare loss is important for evaluating a policy.", "The welfare loss measures the reduction in social surplus caused by the policy; comparing it with the benefits (revenue, reduced external costs, equity) shows whether the policy improves overall welfare."),
       ("Explain why producer revenue may rise after a price floor even though quantity bought by consumers falls.", "Producers sell Qd to consumers and the surplus to the government at the higher floor price, so total revenue = floor price × quantity supplied, which is higher than at equilibrium.")],
  contrast=[("consumer expenditure", "producer revenue (with a tax)", "With a tax, consumer expenditure = price paid × quantity; producer revenue = price received × quantity. The difference is the tax revenue."),
            ("government revenue from a tax", "government expenditure on a subsidy", "A tax raises revenue equal to tax × new quantity; a subsidy costs the government subsidy × new (higher) quantity.")],
  misc=[("The welfare loss of a tax equals the tax revenue.", "Tax revenue is a transfer from consumers and producers to the government; the welfare loss is only the triangle of surplus lost on units no longer traded."),
        ("After a subsidy, consumer expenditure always falls because the price is lower.", "Price falls but quantity rises; consumer expenditure may rise or fall depending on PED.")],
  apply=[("Before a tax, P = $15 and Q = 2,000. After a $4 tax, P = $18 and Q = 1,600. Calculate the consumer burden, the producer burden and government revenue.", "Consumer burden (18 − 15) × 1,600 = $4,800; producer price 14, producer burden (15 − 14) × 1,600 = $1,600; revenue 4 × 1,600 = $6,400.", 4)],
  cases=[("Thailand's rice pledging scheme (2011-2014)", "The government bought rice from farmers at prices around 50% above market levels, building up huge stocks and losses estimated at over $15 billion.", "the costs of price support for stakeholders", "Farmers gained higher revenue, but taxpayers bore the cost of buying and storing the surplus, and Thailand lost export market share.")],
  sources=[("Hypothetical data for a market for wheat: before intervention P = $200 per tonne and Q = 10 million tonnes. The government sets a minimum price of $240; quantity supplied rises to 11.5 million tonnes and quantity demanded falls to 9 million tonnes. The government buys the surplus.", "Hypothetical data", "Calculate the cost to the government and the change in farmers' revenue.", "Surplus = 2.5m tonnes; cost = $240 × 2.5m = $600m. Farmers' revenue: before $2,000m; after $240 × 11.5m = $2,760m, a rise of $760m.")],
  evaluate=[("Policies that benefit producers, such as price floors and subsidies, are always paid for by consumers and taxpayers.", ["consumers pay higher prices under floors", "taxpayers fund subsidies and surplus purchases", "welfare loss means society as a whole loses"], ["subsidies can lower consumer prices", "where external benefits exist, society may gain overall", "stable farm incomes may protect food security"], "Producer support usually has costs for consumers or taxpayers, but whether society loses overall depends on externalities and on wider goals such as food security.")],
  extended=[("A government is choosing between a price ceiling and a subsidy to make a basic food more affordable. Using calculations from a hypothetical example, compare the effects on consumers, producers and the government.", "Ceiling: lower price but shortage, lower producer revenue, no direct cost but welfare loss and black market; subsidy: lower price with more output, producers gain, government cost = subsidy × Q. Calculation with linear functions and comparison; recommendation.", 8, 'long')],
  diag=[("the effects of a specific tax on stakeholders, identifying consumer expenditure, producer revenue, government revenue and welfare loss", "Diagram: S, S + tax, D. Areas: consumer expenditure Pc × Qt; producer revenue Pp × Qt; tax revenue (Pc − Pp) × Qt split into consumer burden above Pe and producer burden below Pe; welfare loss triangle between D and S from Qt to Qe. Consumers pay more, producers receive less, government gains revenue, society loses the triangle.")])


@R.add('ch10-st4', 'C3', (2, 5), 'numerical')
def stakeholders(rng, slot):
    m = market(rng)
    if not m:
        return None
    a, b, c, d, P, Q = m
    intro, g = mkt_intro(rng, a, b, c, d)
    for _ in range(20):
        k = rng.randint(1, 5)
        pf = P + k
        qd, qs = a - b * pf, c + d * pf
        if qd > 0:
            break
    else:
        return None
    return dict(stem=f'{intro} The government sets a minimum price of ${pf} and buys the surplus. Calculate the effect on (i) consumer expenditure, (ii) producer revenue and (iii) government spending, and identify which stakeholder gains most.',
                answer=f'(i) {P * Q} → {pf * qd}; (ii) {P * Q} → {pf * qs}; (iii) {pf * (qs - qd)}; producers gain most',
                markingKey=f'Equilibrium P = {P}, Q = {Q} [1]; at ${pf}: Qd = {qd}, Qs = {qs} [1]; consumer expenditure {pf}×{qd} = {pf * qd} [1]; producer revenue {pf}×{qs} = {pf * qs} [1]; government spending {pf}×{qs - qd} = {pf * (qs - qd)} [1]; producers gain (revenue +{pf * qs - P * Q}), consumers and taxpayers lose [1].', type='numerical', marks=6)


@R.add('ch10-st4', 'C4', (3, 5), 'multi_step')
def stakeholders_compare(rng, slot):
    m = market(rng)
    if not m:
        return None
    a, b, c, d, P, Q = m
    for s in rng.sample([1, 2, 3, 4, 5, 6], 6):
        Pc = (a - c - d * s) / (b + d)
        if abs(Pc - round(Pc)) < 1e-9 and Pc > 0:
            break
    else:
        return None
    Pc = int(round(Pc))
    Qs = a - b * Pc
    k = P - Pc
    qd, qsup = a - b * Pc, c + d * Pc
    if qsup <= 0:
        return None
    intro, g = mkt_intro(rng, a, b, c, d, g=rng.choice(['rice', 'bread', 'cooking oil', 'maize flour', 'lentils']))
    return dict(stem=f'{intro} To make it more affordable, the government is considering either (A) a maximum price of ${Pc} or (B) a subsidy of ${s} per unit to producers, which would lower the market price to the same ${Pc}. Calculate the quantity consumers would obtain under each policy and the cost of option B, and recommend one policy.',
                answer=f'A: quantity traded {qsup} (shortage {qd - qsup}); B: quantity {Qs}, cost {s * Qs}; B gives more output at a fiscal cost',
                markingKey=f'Equilibrium P = {P}, Q = {Q} [1]. A: at ${Pc}, Qs = {qsup}, Qd = {qd}, shortage {qd - qsup}; only {qsup} units traded [2]. B: supply Qs = {c} + {d}(P + {s}); Pc = {Pc}, Q = {Qs} [1]; cost {s} × {Qs} = {s * Qs} [1]. Recommendation weighs B\'s higher output and no shortage against its fiscal cost/opportunity cost; A costs nothing directly but causes shortages, queues and black markets [1].', type='multi_step', marks=6)

# =============================================================================================
# ch11 Unit 2.8 Market failure: externalities and common pool resources
# =============================================================================================
S('ch11-st1',
  terms=[("market failure", "the failure of the market to allocate resources efficiently, so that social surplus is not maximised (MSB ≠ MSC at the market output)"),
         ("marginal private benefit (MPB)", "the extra benefit to consumers from consuming one more unit of a good, shown by the demand curve"),
         ("marginal social benefit (MSB)", "the extra benefit to society from one more unit, equal to MPB plus any marginal external benefit"),
         ("marginal private cost (MPC)", "the extra cost to producers of producing one more unit, shown by the supply curve"),
         ("marginal social cost (MSC)", "the extra cost to society of producing one more unit, equal to MPC plus any marginal external cost"),
         ("externality", "a cost or benefit arising from production or consumption that affects third parties and is not reflected in the market price")],
  facts=[("Allocative efficiency for society occurs where which of the following holds?", "MSB = MSC", ["MPB = MPC only", "MSB > MSC", "Price is at its lowest"], "The socially optimal output equates the full benefit and full cost to society."),
         ("If there is a negative externality of production, which of the following is true?", "MSC > MPC", ["MSB > MPB", "MSC < MPC", "MPB > MSB"], "External costs are added to private costs."),
         ("In a free market, firms and consumers produce and consume where which of the following holds?", "MPB = MPC", ["MSB = MSC", "MSB = MPC", "MPB = MSC"], "Market decisions consider only private costs and benefits."),
         ("Who are third parties in the context of externalities?", "People not directly involved in buying or selling the good", ["The buyers of the good", "The sellers of the good", "The government only"], "Externalities fall on others outside the transaction.")],
  why=[("Explain why the free market fails to achieve allocative efficiency when externalities exist.", "Buyers and sellers consider only private costs and benefits, so the market produces where MPB = MPC; if external costs or benefits exist, MSB ≠ MSC at that output, so too much or too little is produced compared with the social optimum."),
       ("Explain why the demand curve can be treated as the MPB curve.", "Consumers are willing to pay up to the extra benefit they gain from one more unit, so the price on the demand curve at each quantity measures their marginal private benefit."),
       ("Explain why welfare loss arises when output exceeds the socially optimal level.", "Beyond the optimum, each extra unit has MSC > MSB: society values it less than it costs, so producing it subtracts from social surplus.")],
  contrast=[("private costs", "social costs", "Private costs are borne by the producer or consumer making the decision; social costs are private costs plus external costs borne by third parties."),
            ("the market equilibrium", "the social optimum", "The market equilibrium is where MPB = MPC; the social optimum is where MSB = MSC. They coincide only if there are no externalities.")],
  misc=[("Market failure means that a market has collapsed and nothing is sold.", "Market failure means resources are misallocated – too much or too little is produced relative to the social optimum – even though the market may be very active."),
        ("When MSC is greater than MPC, the market produces too little.", "When MSC > MPC (negative production externality), the market over-produces because producers ignore the external cost.")],
  apply=[("A factory in Hanoi dumps waste into a river used by fishermen. Identify the private cost, the external cost and explain why the market output is too high.", "Private cost: the factory's own costs of labour, materials etc.; external cost: lost fish catches and health damage; the factory ignores external costs (MPC < MSC), so it produces where MPB = MPC, above the optimum where MSB = MSC.", 3)],
  cases=[("air pollution from coal power in northern India", "Coal-fired power stations around Delhi contribute to severe air pollution linked to respiratory illness.", "the divergence between MPC and MSC", "Producers' costs exclude the health damage to residents, so MSC > MPC and too much electricity is generated from coal.")],
  sources=[("Hypothetical estimates for a city show that each extra tonne of waste burned in an incinerator costs the operator $40 (MPC), while nearby residents suffer health and property damage estimated at $25 per tonne.", "Hypothetical data", "Using the data, calculate the marginal social cost per tonne and explain why the market may burn too much waste.", "MSC = 40 + 25 = $65 per tonne; the operator decides using only the $40 private cost, so it burns where MPB = MPC, beyond the optimum where MSB = MSC = $65.")],
  evaluate=[("The concept of allocative efficiency (MSB = MSC) is of limited practical use because external costs cannot be measured accurately.", ["external costs (health, climate) are hard to value in money", "estimates vary widely (social cost of carbon)"], ["even approximate values improve policy (carbon prices)", "the framework shows the direction of correction", "cost-benefit analysis is widely used"], "Measurement is difficult, but the MSB = MSC framework remains essential for deciding the direction and approximate scale of intervention.")],
  diag=[("why a free market fails to achieve allocative efficiency when there is a negative externality of production", "Diagram: MPB = MSB (demand), MPC (supply) and MSC above MPC. Market output Qm where MPB = MPC at price Pm; social optimum Q* where MSB = MSC. Qm > Q*: over-allocation of resources; welfare loss triangle between MSC and MSB from Q* to Qm.")])


@R.add('ch11-st1', 'C3', (2, 5), 'numerical')
def msb_msc(rng, slot):
    for _ in range(50):
        A_ = rng.choice([60, 80, 100, 120])
        B = rng.choice([1, 2])
        C_ = rng.choice([10, 20])
        D = rng.choice([1, 2, 3])
        e = rng.choice([B + D, 2 * (B + D), 3 * (B + D)])
        Qm = (A_ - C_) / (B + D)
        Qs = (A_ - C_ - e) / (B + D)
        if Qm == int(Qm) and Qs == int(Qs) and Qs > 0:
            break
    else:
        return None
    Qm, Qs = int(Qm), int(Qs)
    Pm = A_ - B * Qm
    ctx = rng.choice(['cement production near a town', 'a chemical plant', 'a coal mine', 'steel production', 'intensive pig farming'])
    dwl = 0.5 * e * (Qm - Qs)
    return dict(stem=f'For {ctx}, MPB = MSB is P = {A_} − {B if B > 1 else ""}Q and MPC is P = {C_} + {D if D > 1 else ""}Q (P in $, Q in thousand units). Production creates a constant external cost of ${e} per unit. Calculate the market output, the socially optimal output and the welfare loss.',
                answer=f'Market Q = {Qm}; optimum Q = {Qs}; welfare loss = {fmt(dwl, 6)} ($ thousand)',
                markingKey=f'Market: {A_} − {B}Q = {C_} + {D}Q ⇒ Q = {Qm} [1]; MSC = {C_ + e} + {D}Q; optimum {A_} − {B}Q = {C_ + e} + {D}Q ⇒ Q = {Qs} [1]; welfare loss = ½ × {e} × ({Qm} − {Qs}) = {fmt(dwl, 6)} [2].', type='numerical', marks=4)


S('ch11-st2',
  terms=[("negative externality of production", "an external cost created by producers that harms third parties, such as pollution from a factory, so that MSC > MPC"),
         ("negative externality of consumption", "an external cost created by consumers that harms third parties, such as second-hand smoke, so that MSB < MPB"),
         ("Pigouvian tax", "a tax on a good equal to the marginal external cost, designed to make producers or consumers internalise the externality"),
         ("internalising an externality", "making producers or consumers bear the external cost of their actions, so that private decisions take account of social costs"),
         ("demerit good", "a good that is considered harmful to consumers and others and is over-consumed in a free market, such as tobacco")],
  facts=[("Which of the following is a negative externality of consumption?", "Noise from a neighbour's late-night party", ["Pollution from a power station", "Vaccination of children", "Bees from a beekeeper pollinating orchards"], "The harm results from consumption and affects third parties."),
         ("With a negative externality of consumption, which of the following holds?", "MSB < MPB", ["MSC > MPC", "MSB > MPB", "MSC < MPC"], "Society gains less than the consumer because of harm to others."),
         ("A Pigouvian tax is set equal to which of the following?", "The marginal external cost at the social optimum", ["The market price", "The firm's average cost", "The welfare loss"], "It shifts MPC up to MSC."),
         ("Which of the following is an example of regulation to reduce a negative externality?", "A ban on smoking in public places", ["A carbon tax", "Tradable permits", "A subsidy for public transport"], "It directly restricts behaviour.")],
  why=[("Explain how a Pigouvian tax can correct a negative externality of production.", "A tax per unit equal to the marginal external cost shifts the supply (MPC) curve up to MSC; producers now pay the full social cost, so output falls from the market level to the socially optimal level where MSB = MSC."),
       ("Explain why second-hand smoke is a negative externality of consumption.", "Smokers consider only their private benefit; non-smokers who breathe the smoke suffer health damage without compensation, so the marginal social benefit of smoking is lower than the marginal private benefit."),
       ("Explain why regulation may be preferred to taxation for some negative externalities.", "If the harm is severe or the externality is dangerous (e.g. toxic chemicals), a ban or strict limit guarantees the outcome, whereas a tax allows the activity to continue for those willing to pay."),
       ("Explain why taxes on negative externalities are difficult to set at the correct level.", "The marginal external cost is hard to measure in money terms (health, environment), varies by location and over time, so the tax may be too high or too low.")],
  contrast=[("a negative externality of production", "a negative externality of consumption", "A production externality arises from firms' output (MSC > MPC, e.g. factory pollution); a consumption externality arises from consumers' use of a good (MSB < MPB, e.g. second-hand smoke or traffic congestion)."),
            ("a carbon tax", "a cap-and-trade (tradable permit) scheme", "A carbon tax fixes the price of emissions and lets the quantity adjust; a cap-and-trade scheme fixes the quantity of emissions and lets the price of permits adjust in the market.")],
  misc=[("A tax on pollution aims to reduce pollution to zero.", "The optimal level of pollution is where MSB = MSC, which is usually above zero; the tax internalises the externality rather than eliminating the activity."),
        ("Banning a good is always the best way to deal with a negative externality.", "Bans can create black markets, remove benefits that consumers value and are costly to enforce; taxes or permits may achieve the optimum more efficiently.")],
  apply=[("Explain the externality caused by congestion when drivers enter central London, and how the congestion charge (introduced 2003) tries to correct it.", "Each driver adds to delays and pollution for others (negative consumption externality, MSB < MPB); the daily charge raises the private cost of driving into the zone, reducing journeys towards the optimum.", 3),
         ("Identify one negative externality of production and one of consumption associated with fast fashion.", "Production: water pollution and emissions from textile factories; consumption: textile waste in landfill (or microplastic shedding when washing).", 2)],
  cases=[("Sweden's carbon tax introduced in 1991", "Sweden taxes carbon at around SEK 1,200 (about $120) per tonne, one of the highest rates in the world; emissions fell by over 30% between 1990 and 2020 while GDP grew strongly.", "a Pigouvian tax to correct negative externalities", "The tax raised the private cost of fossil fuels towards their social cost, encouraging switching to biomass and other low-carbon energy."),
         ("Australia's plain packaging and tobacco tax rises from 2012", "Australia introduced plain packaging and large annual tax increases; smoking rates among adults fell to around 11% by 2019.", "policies to reduce negative consumption externalities", "Combining higher prices with information and regulation reduced consumption of a demerit good with external costs.")],
  sources=[("The EU Emissions Trading System covers around 40% of EU greenhouse gas emissions. The price of an allowance rose from under €10 per tonne in 2017 to over €90 in 2022 after the EU tightened the cap. Emissions from power generation fell sharply as coal plants closed.", "Extract based on reporting of the EU ETS", "Using the extract, explain how tradable permits help to reduce a negative externality.", "The cap limits total emissions; firms must buy allowances, so emitting becomes costly; a tighter cap raised the permit price, giving firms the incentive to cut emissions (e.g. close coal plants) – the externality is internalised.")],
  evaluate=[("Carbon taxes are the most effective policy to reduce greenhouse gas emissions.", ["internalise the externality using the price mechanism", "allow emissions to be cut where cheapest", "raise revenue that can be recycled (British Columbia)"], ["difficult to set at the correct level", "regressive and politically unpopular (France's gilets jaunes, 2018)", "may cause carbon leakage to countries without taxes", "inelastic demand for fuel limits the short-run effect"], "Carbon taxes are efficient in principle and effective in practice where politically sustainable, but they work best alongside regulation, subsidies for clean technology and international cooperation."),
            ("Government regulation is more effective than taxation in reducing negative externalities of consumption.", ["bans and limits give certain outcomes (smoking bans)", "easy to understand"], ["regulation is inflexible and costly to enforce", "taxes raise revenue and change incentives continuously", "black markets may develop under bans"], "Regulation is preferable when harms are severe and immediate; taxes are usually more efficient for widespread, moderate externalities.")],
  extended=[("Using a diagram, explain how a tax on petrol might correct the negative externality associated with its consumption, and discuss one limitation of this policy.", "Diagram: MPB, MSB below MPB, supply = MPC = MSC; market at MPB = MPC above optimum; tax reduces quantity towards Q* where MSB = MSC. Limitations: inelastic demand, regressive, hard to measure external cost, political opposition.", 6)],
  diag=[("the welfare loss caused by a negative externality of production and how a Pigouvian tax can eliminate it", "Diagram: MPB = MSB, MPC and MSC (MSC above MPC by the marginal external cost). Market Qm, Pm at MPB = MPC; optimum Q*, P* at MSB = MSC; welfare loss triangle between Q* and Qm. A tax equal to the external cost shifts MPC up to MSC; output falls to Q* and the welfare loss is removed."),
        ("the over-consumption of a good with a negative consumption externality, such as cigarettes", "Diagram: supply = MPC = MSC; MPB above MSB. Market at Qm where MPB = MPC; optimum Q* where MSB = MSC; Qm > Q* – over-consumption; welfare loss triangle between MSC and MSB from Q* to Qm. Policies: tax, regulation (bans in public places), education.")])


@R.add('ch11-st2', 'C3', (2, 5), 'numerical')
def pigou(rng, slot):
    e = rng.choice([5, 8, 10, 12, 15, 20, 25])
    Qm = rng.choice([400, 500, 600, 800, 1000])
    Qo = Qm - rng.choice([100, 150, 200, 250])
    ctx = rng.choice([('a steel plant in the Ruhr', 'tonnes of steel'), ('a paper mill in Finland', 'tonnes of paper'), ('a fertiliser factory in Gujarat', 'tonnes of fertiliser'),
                      ('a tannery near Dhaka', 'hides processed'), ('a coal power station in Poland', 'MWh of electricity')])
    who, unit = ctx
    dwl = 0.5 * e * (Qm - Qo)
    return dict(stem=f'{who.capitalize()} produces {Qm} {unit} per day, where MPB = MPC. Each unit causes pollution costing local residents ${e} (constant marginal external cost). At the social optimum output would be {Qo}. Calculate the welfare loss per day, state the Pigouvian tax per unit and the daily revenue it would raise.',
                answer=f'Welfare loss ${fmt(dwl, 6)}; tax ${e} per unit; revenue ${e * Qo:,}',
                markingKey=f'Welfare loss = ½ × {e} × ({Qm} − {Qo}) = {fmt(dwl, 6)} [2]; tax = MEC = ${e} [1]; revenue = {e} × {Qo} = {e * Qo:,} [1].', type='numerical', marks=4)


S('ch11-st3',
  terms=[("positive externality of production", "an external benefit created by producers for third parties, such as a firm training workers who later work elsewhere, so MSC < MPC"),
         ("positive externality of consumption", "an external benefit created by consumers for third parties, such as vaccinations reducing disease transmission, so MSB > MPB"),
         ("merit good", "a good that is considered beneficial for people and society and tends to be under-consumed in a free market, such as education and healthcare"),
         ("direct provision", "the government itself supplies a good or service, often free at the point of use, to increase consumption"),
         ("positive advertising", "government information campaigns that increase awareness of the benefits of a good, shifting MPB towards MSB")],
  facts=[("Which of the following is a positive externality of consumption?", "Reduced disease spread when people are vaccinated", ["Pollution from cars", "Firms' spending on research", "Noise from an airport"], "Third parties benefit from lower infection rates."),
         ("With a positive externality of production, which of the following holds?", "MSC < MPC", ["MSC > MPC", "MSB < MPB", "MPB > MSB"], "The external benefit lowers the cost to society of each unit."),
         ("Which policy would shift the MPB curve to the right to correct under-consumption of a merit good?", "An information campaign about the benefits of the good", ["A subsidy to producers", "A tax on the good", "A price ceiling"], "Information raises consumers' perceived private benefit; a producer subsidy shifts supply."),
         ("Why is the market output of goods with positive externalities too low?", "Decision-makers ignore the external benefits to third parties", ["Firms charge too high a price", "Governments tax them heavily", "Demand is perfectly elastic"], "The market produces where MPB = MPC, below the optimum MSB = MSC.")],
  why=[("Explain why education is likely to be under-consumed in a free market.", "Students and families consider only private benefits (higher earnings), not the external benefits to society (higher productivity, lower crime, better civic participation); MSB > MPB, so the market quantity is below the social optimum."),
       ("Explain how a subsidy can correct a positive externality of production.", "A subsidy lowers firms' costs, shifting MPC down towards MSC; output rises from the market level to the socially optimal level where MSB = MSC."),
       ("Explain why governments may provide some merit goods directly rather than subsidise them.", "Direct provision free at the point of use can ensure universal access regardless of income (equity) and large increases in consumption; it may also be easier where markets would under-provide, such as basic healthcare in rural areas."),
       ("Explain why research and development by firms can create positive externalities.", "Knowledge spills over to other firms and society: discoveries can be copied or built upon, raising productivity elsewhere, but the inventing firm does not receive payment for these benefits, so R&D is under-provided.")],
  contrast=[("a positive externality of production", "a positive externality of consumption", "A production externality comes from firms' activities (MSC < MPC, e.g. worker training, R&D spillovers); a consumption externality comes from consumers' use of a good (MSB > MPB, e.g. vaccinations, education)."),
            ("a subsidy", "direct provision", "A subsidy lowers the price of a good produced by private firms; direct provision means the government itself supplies it, often free at the point of use.")],
  misc=[("Goods with positive externalities are over-consumed because they are good for people.", "Because decision-makers ignore the external benefits, goods with positive externalities are under-consumed relative to the social optimum."),
        ("Making healthcare free removes all market failure in healthcare.", "Free provision increases consumption but may cause over-use, waiting lists and a large fiscal burden; asymmetric information and moral hazard remain.")],
  apply=[("Explain why a city like Bogotá might subsidise bicycle-sharing schemes.", "Cycling creates positive externalities (less congestion, pollution and better public health) not considered by individual users, so MSB > MPB; a subsidy lowers the price, increasing use towards the optimum.", 3),
         ("Identify one market-based and one non-market policy to increase the number of children receiving the measles vaccine.", "Market-based: subsidy or making vaccination free (cash incentives); non-market: information campaigns, legislation making vaccination a requirement for school entry.", 2)],
  cases=[("Germany's subsidies for solar panels through feed-in tariffs from 2000", "Guaranteed above-market prices for renewable electricity led to rapid growth in solar capacity and helped drive down global panel costs.", "subsidies to correct positive production externalities", "The subsidy encouraged production with environmental and learning spillovers, increasing output towards the social optimum."),
         ("Rwanda's community-based health insurance (Mutuelles de Santé)", "Heavily subsidised insurance covers over 80% of the population, raising the use of clinics and vaccinations.", "government intervention to increase consumption of merit goods", "Lower costs to households increased consumption of healthcare, generating private and external benefits.")],
  sources=[("Singapore's SkillsFuture programme gives every citizen aged 25 and above a credit (initially S$500) to spend on approved training courses. The government argues that a more skilled workforce raises productivity across the economy.", "Extract based on information about Singapore's SkillsFuture scheme", "Using the extract, explain why the government subsidises training.", "Training creates positive externalities (MSB > MPB): more productive workers benefit other firms and society, so individuals and firms under-invest; the credit lowers the private cost, increasing training towards the optimum.")],
  evaluate=[("Direct government provision is the best way to increase consumption of merit goods.", ["guarantees access for all (equity)", "can achieve large increases in consumption quickly", "avoids reliance on private profit motives"], ["high fiscal cost and opportunity cost", "possible inefficiency and lack of choice", "over-consumption and waiting lists when free", "subsidies or vouchers may achieve similar results at lower cost"], "Direct provision is effective for basic merit goods such as primary education, but subsidies, regulation and information can complement it more efficiently."),
            ("Subsidies are the most effective way to correct positive externalities.", ["lower price and raise quantity towards the optimum", "flexible and targeted"], ["cost to taxpayers and opportunity cost", "difficult to set the right subsidy", "firms may become dependent", "information campaigns and regulation can be cheaper"], "Subsidies are often effective but must be well targeted and combined with other tools.")],
  extended=[("Using a diagram, explain why vaccinations are under-consumed in a free market and evaluate the use of a subsidy to correct this.", "Diagram: MPB below MSB, MPC = MSC; market Qm < Q*; welfare loss triangle. Subsidy lowers price, increases quantity; evaluation: cost, measurement of external benefit, other policies (free provision, mandates, information), equity.", 6)],
  diag=[("why a good with a positive consumption externality, such as education, is under-provided by the free market", "Diagram: MPC = MSC (supply), MPB (demand) and MSB to the right of MPB. Market output Qm where MPB = MPC; social optimum Q* where MSB = MSC; Qm < Q*: under-allocation of resources; welfare loss triangle between MSB and MSC from Qm to Q*."),
        ("how a subsidy can correct a positive externality of production", "Diagram: MPB = MSB, MPC and MSC below MPC. Market at Qm (MPB = MPC) below the optimum Q* (MSB = MSC); a subsidy equal to the marginal external benefit shifts MPC down to MSC, increasing output to Q*.")])


@R.add('ch11-st3', 'C3', (2, 5), 'numerical')
def pos_ext(rng, slot):
    eb = rng.choice([10, 15, 20, 30, 40])
    Qm = rng.choice([2000, 3000, 5000, 8000])
    Qo = Qm + rng.choice([500, 1000, 1500, 2000])
    ctx = rng.choice([('flu vaccinations', 'a city health authority'), ('university places', 'a ministry of education'), ('apprenticeships', 'a regional government'),
                      ('home solar installations', 'an energy ministry'), ('bicycle-share memberships', 'a city council')])
    good, who = ctx
    dwl = 0.5 * eb * (Qo - Qm)
    return dict(stem=f'Each of the {Qm:,} {good} bought in a free market provides a constant external benefit of ${eb} to third parties. {who.capitalize()} estimates the socially optimal quantity is {Qo:,}. Calculate the welfare loss, the subsidy per unit needed and the total cost of the subsidy at the optimum.',
                answer=f'Welfare loss ${fmt(dwl, 6)}; subsidy ${eb} per unit; cost ${eb * Qo:,}',
                markingKey=f'Welfare loss = ½ × {eb} × ({Qo:,} − {Qm:,}) = {fmt(dwl, 6)} [2]; subsidy = MEB = ${eb} [1]; cost = {eb} × {Qo:,} = {eb * Qo:,} [1].', type='numerical', marks=4)


S('ch11-st4',
  terms=[("common pool resource", "a resource that is rivalrous but non-excludable, such as fish stocks, groundwater or forests, so it tends to be over-used"),
         ("tragedy of the commons", "the over-use and depletion of a common pool resource because each user gains the full benefit of their use while the cost of depletion is shared by all"),
         ("sustainability", "using resources in a way that meets present needs without compromising the ability of future generations to meet their needs"),
         ("tradable permits (cap and trade)", "a system in which the government sets a cap on total pollution or resource use and issues permits that firms can buy and sell"),
         ("carbon tax", "a tax on the carbon content of fossil fuels, intended to internalise the external cost of greenhouse gas emissions"),
         ("fishing quota", "a legal limit on the quantity of fish that a country, firm or boat may catch in a period")],
  facts=[("Which of the following is the best example of a common pool resource?", "An ocean fishery outside any country's control", ["A privately owned forest", "A cinema", "A toll road"], "It is non-excludable (open access) but rivalrous (fish caught by one boat cannot be caught by another)."),
         ("Common pool resources are characterised by which pair of features?", "Rivalrous and non-excludable", ["Non-rivalrous and non-excludable", "Rivalrous and excludable", "Non-rivalrous and excludable"], "Public goods are non-rival and non-excludable; private goods are rival and excludable."),
         ("Which economist won the 2009 Nobel Prize for showing that communities can manage common pool resources successfully without privatisation or state control?", "Elinor Ostrom", ["Garrett Hardin", "Ronald Coase", "Joseph Stiglitz"], "Ostrom studied self-governed fisheries, forests and irrigation systems."),
         ("Under a cap-and-trade system, what determines the price of a permit?", "The demand for and supply of permits in the permit market", ["The government sets it directly", "The cost of the cheapest firm's abatement only", "The carbon tax rate"], "The cap fixes supply; firms' demand sets the price.")],
  why=[("Explain why common pool resources are over-used.", "Because no one can be excluded, each user takes as much as is privately beneficial; the cost of depleting the stock is shared by all users and future generations, so the resource is used beyond sustainable levels."),
       ("Explain why tradable permits reduce pollution at the lowest overall cost.", "Firms that can cut emissions cheaply do so and sell spare permits, while firms with high abatement costs buy permits; total emissions equal the cap, and reductions happen where they are cheapest."),
       ("Explain why international cooperation is needed to protect resources such as the atmosphere and oceans.", "These resources cross national boundaries; one country's cuts benefit all, so countries have an incentive to free ride; agreements (Paris Agreement, fishing treaties) are needed to share the costs and enforce limits.")],
  contrast=[("a carbon tax", "tradable permits", "A carbon tax sets the price of emissions and lets the quantity adjust, giving price certainty; tradable permits set the quantity of emissions and let the price adjust, giving certainty about the environmental outcome."),
            ("a common pool resource", "a public good", "Both are non-excludable, but a common pool resource is rivalrous (one person's use reduces what is left), whereas a public good is non-rivalrous.")],
  misc=[("Common pool resources are over-used because they are public goods.", "Common pool resources are rivalrous, unlike public goods; over-use arises because they are non-excludable and rivalrous, so one user's consumption depletes the stock for others."),
        ("A carbon tax guarantees a specific reduction in emissions.", "A carbon tax fixes the price of emissions; the reduction depends on how firms and consumers respond (PED). A cap-and-trade scheme fixes the quantity.")],
  apply=[("Explain how individual transferable fishing quotas (ITQs) in Iceland and New Zealand help prevent the tragedy of the commons.", "The total allowable catch is limited; quotas give each holder a share they can trade, so fishers have an incentive to protect the stock (future quota value rises), reducing over-fishing.", 3)],
  cases=[("the collapse of the Grand Banks cod fishery off Newfoundland", "Decades of over-fishing led to a collapse of cod stocks; Canada imposed a moratorium in 1992 and about 30,000-40,000 people lost their jobs.", "the tragedy of the commons", "Open access led each fleet to maximise its own catch, depleting the shared stock until it collapsed."),
         ("British Columbia's revenue-neutral carbon tax (2008)", "The province introduced a carbon tax starting at CAD 10 per tonne, with revenue returned through cuts in income and business taxes.", "a carbon tax as a sustainability policy", "The tax internalised part of the external cost of emissions while recycling revenue limited its regressive effect; fuel use per person fell relative to the rest of Canada.")],
  sources=[("The Amazon rainforest lost an estimated 13,000 km² of forest in the year to July 2021, the highest in 15 years, as land was cleared for cattle ranching and soy. Deforestation alerts fell by about 50% in 2023 after Brazil increased enforcement against illegal clearing.", "Extract based on data from Brazil's INPE satellite monitoring", "Using the extract, explain why the Amazon is an example of a common pool resource problem and how government action affected the outcome.", "Forest is rivalrous (land cleared is lost) and hard to exclude people from; individual ranchers gain from clearing while the costs (biodiversity, carbon) are shared globally – tragedy of the commons. Stronger enforcement (regulation) reduced clearing.")],
  evaluate=[("Tradable permits are a more effective policy than carbon taxes for achieving sustainability.", ["guarantee the level of emissions (cap)", "firms cut emissions where cheapest", "politically easier when permits are given free initially"], ["permit prices volatile (EU ETS fell below €10 for years)", "over-allocation of permits weakened early schemes", "carbon taxes give price certainty and revenue", "both face carbon leakage"], "Permits give certainty over emissions while taxes give certainty over price; both can work, and effectiveness depends on design (cap stringency, coverage, revenue use)."),
            ("Common pool resources can only be protected by government intervention.", ["regulation, quotas and taxes needed to limit use", "international agreements need governments"], ["Ostrom: communities can self-govern resources successfully", "property rights (ITQs) can create private incentives", "firms and consumers (certification schemes) also help"], "Government action is often necessary, but community management and property rights can be effective, especially for local resources.")],
  extended=[("Explain how a cap-and-trade scheme works, using a diagram of the permit market, and discuss one reason it might fail to reduce emissions sufficiently.", "Permit market: vertical supply at the cap, downward-sloping demand from firms; equilibrium permit price; tighter cap shifts supply left and raises price. Failure: cap set too high (over-allocation), lobbying, carbon leakage, price volatility.", 6)],
  diag=[("how a cap-and-trade scheme sets the price of pollution permits", "Diagram: price of permits on the vertical axis, quantity of permits (emissions) on the horizontal; supply is vertical at the cap set by the government; demand by firms slopes down. The equilibrium permit price P1 is where demand meets the cap. Tightening the cap shifts supply left, raising the permit price and giving firms stronger incentives to cut emissions; higher demand from economic growth raises price without raising emissions.")])


@R.add('ch11-st4', 'C3', (2, 5), 'numerical')
def permits(rng, slot):
    price = rng.choice([30, 50, 60, 80, 90])
    fa, fb = rng.sample(['Firm A (a cement maker)', 'Firm B (a power station)', 'Firm C (a steel mill)', 'Firm D (an airline)'], 2)
    ca = rng.choice([c for c in [20, 25, 40, 45, 70] if c != price])
    cb = rng.choice([c for c in [55, 65, 95, 110, 120] if c != price and c != ca])
    t = rng.choice([1000, 2000, 5000])
    act = lambda c: 'abate (cut emissions) and sell/not buy permits' if c < price else 'buy permits rather than abate'
    cost_a = min(ca, price) * t
    cost_b = min(cb, price) * t
    return dict(stem=f'The permit price in an emissions trading scheme is ${price} per tonne of CO₂. {fa} can cut emissions at ${ca} per tonne and {fb} at ${cb} per tonne. Each must reduce its emissions or hold permits for an extra {t:,} tonnes. State what each firm will do and calculate each firm\'s cost of compliance.',
                answer=f'{fa}: {act(ca)}, cost ${cost_a:,}; {fb}: {act(cb)}, cost ${cost_b:,}',
                markingKey=f'{fa}: abatement ${ca} {"<" if ca < price else ">"} permit ${price} ⇒ {act(ca)}; cost {min(ca, price)} × {t:,} = {cost_a:,} [2]; {fb}: ${cb} {"<" if cb < price else ">"} ${price} ⇒ {act(cb)}; cost {min(cb, price)} × {t:,} = {cost_b:,} [2]. Emissions are cut by the lowest-cost firm.', type='numerical', marks=4)

# =============================================================================================
# ch12 Unit 2.9-2.10 Market failure: public goods and asymmetric information
# =============================================================================================
S('ch12-st1',
  terms=[("public good", "a good that is non-rivalrous and non-excludable, so it is not provided, or is under-provided, by the free market"),
         ("non-rivalry", "the characteristic that one person's consumption of a good does not reduce the amount available for others"),
         ("non-excludability", "the characteristic that it is impossible or very costly to prevent people who have not paid from using a good"),
         ("free-rider problem", "the problem that people can benefit from a good without paying for it, so private firms cannot earn revenue and do not supply it"),
         ("quasi-public good", "a good that has some but not all characteristics of a public good, such as a road that is non-rival until congested"),
         ("private good", "a good that is both rivalrous and excludable")],
  facts=[("Which of the following is the best example of a pure public good?", "National defence", ["A sandwich", "A toll motorway", "A private school place"], "Defence protects everyone (non-rival) and no one can be excluded."),
         ("Why are public goods not provided by the free market?", "Non-excludability leads to free riding, so firms cannot charge users", ["They are too expensive to produce", "Demand for them is zero", "They have negative externalities"], "With no way to exclude non-payers, there is no profit incentive."),
         ("Which of the following characteristics makes street lighting non-rivalrous?", "One more person using the light does not reduce the light available to others", ["People can be stopped from using it", "It is provided by the government", "It is funded by taxes"], "Non-rivalry is about consumption, not about who provides it."),
         ("Which of the following is a common way for governments to provide public goods?", "Direct provision financed by taxation", ["Price ceilings", "Tradable permits", "Indirect taxes on the good"], "Taxes overcome the free-rider problem.")],
  why=[("Explain why the free-rider problem leads to the market failure of missing markets.", "Because non-payers cannot be excluded, people wait for others to pay; firms cannot earn revenue, so they do not produce the good at all even though society values it – the market is missing."),
       ("Explain why a lighthouse has traditionally been considered a public good.", "Its light can be seen by every ship (non-rival) and it is impossible to prevent passing ships that have not paid from benefiting (non-excludable), so private provision is difficult."),
       ("Explain why technology can change whether a good is a public good.", "Technology can make goods excludable: encryption makes TV broadcasts excludable (subscription services), electronic tolling makes roads excludable, so they can be sold privately.")],
  contrast=[("a public good", "a merit good", "A public good is defined by its characteristics (non-rival, non-excludable) and would not be provided by markets; a merit good (e.g. education) is rival and excludable but under-consumed because of positive externalities or imperfect information."),
            ("a public good", "a quasi-public good", "A pure public good is fully non-rival and non-excludable; a quasi-public good has these features only partly, e.g. roads become rival when congested and can be made excludable by tolls.")],
  misc=[("Public goods are any goods provided by the government.", "A public good is defined by non-rivalry and non-excludability; governments also provide private and merit goods such as healthcare and education, which are rival and excludable."),
        ("Because public goods are non-rivalrous, they cost nothing to produce.", "Non-rivalry means one person's use does not reduce availability for others; public goods such as defence and flood barriers still use scarce resources and have opportunity costs.")],
  apply=[("Explain whether the following is a public good: (i) a fireworks display over a harbour; (ii) a seat at a football match.", "(i) public good: everyone in the area can watch (non-rival) and non-payers cannot easily be excluded; (ii) private good: a seat is rival and tickets exclude non-payers.", 2)],
  cases=[("the Thames Barrier in London", "Completed in 1982, the barrier protects around 1.4 million people from tidal flooding and is funded by the government.", "public goods and government provision", "Flood protection benefits everyone in the area (non-rival) and no one can be excluded, so it would not be provided by the market; the government funds it through taxation.")],
  sources=[("A town of 10,000 households is considering a new flood wall costing $3 million. A survey suggests each household would be willing to pay $400 for the protection, but when the council asked for voluntary contributions only $600,000 was pledged.", "Hypothetical council report", "Using the data, explain why the flood wall is under-provided without government action.", "Total willingness to pay = 10,000 × $400 = $4m > $3m cost, so the wall is worth building; but because households cannot be excluded from protection, many free ride and pledges ($0.6m) are far below the cost – the market fails.")],
  evaluate=[("Public goods must always be provided directly by the government.", ["free-rider problem prevents private provision", "taxes ensure funding and universal access"], ["government can contract private firms to build and operate them", "technology can make some goods excludable (toll roads)", "philanthropy and community provision (Wikipedia, open-source software)"], "Governments must usually fund public goods, but they need not produce them directly; contracting out and new technology offer alternatives."),
            ("Government provision of public goods is likely to lead to government failure.", ["hard to know how much people value public goods", "political motives may distort spending", "lack of competition can cause inefficiency"], ["without government, public goods are not provided at all", "cost-benefit analysis can guide spending", "competitive tendering improves efficiency"], "There is a risk of government failure, but the alternative is no provision; careful appraisal and procurement reduce the risk.")],
  extended=[("Explain, with real-world examples, why the free market fails to provide public goods and evaluate two ways in which governments can respond.", "Non-rivalry and non-excludability, free riding; examples: defence, street lighting, flood defences. Responses: direct provision funded by taxes (guarantees provision; risk of over/under-provision, opportunity cost); contracting out to private firms (efficiency, but monitoring costs).", 8, 'long')],
  diag=[("why public goods are not provided by the free market", "Explain non-rivalry and non-excludability; a diagram can show the missing market: demand for the good (society's marginal benefit) is positive, but because individuals free ride, effective demand faced by firms is close to zero, so no output is produced although MSB > MSC for the first units. Government provision financed by taxes moves output to the optimum.")])


@R.add('ch12-st1', 'C3', (2, 5), 'numerical')
def free_rider(rng, slot):
    n = rng.choice([500, 1000, 2000, 5000, 8000])
    wtp = rng.choice([20, 30, 40, 50, 80])
    cost = n * wtp * rng.choice([0.6, 0.7, 0.8, 0.9])
    share = rng.choice([10, 20, 25, 30])
    good = rng.choice(['street lights for a neighbourhood', 'a flood barrier for a village', 'a mosquito-spraying programme for a town', 'a community early-warning siren system', 'a fireworks display for a city festival'])
    raised = n * share / 100 * wtp
    return dict(stem=f'{good.capitalize()} would cost ${int(cost):,}. Each of the {n:,} households values it at ${wtp}. When asked to contribute voluntarily, only {share}% of households pay their full valuation. Calculate total willingness to pay and the money raised, and explain why the good is not provided.',
                answer=f'Willingness to pay ${n * wtp:,}; raised ${int(raised):,}; cost ${int(cost):,} – not provided because of free riding',
                markingKey=f'Total WTP = {n:,} × {wtp} = {n * wtp:,} > cost {int(cost):,} [1]; raised = {share}% × {n:,} × {wtp} = {int(raised):,} [1]; raised < cost, so it is not provided [1]; households free ride because they cannot be excluded [1].', type='numerical', marks=4)


S('ch12-st2',
  terms=[("asymmetric information", "a situation in which one party to a transaction has more or better information than the other, leading to market failure"),
         ("adverse selection", "a situation where the party with better information before a transaction (hidden characteristics) is more likely to participate, such as high-risk people buying insurance"),
         ("moral hazard", "a situation where one party changes their behaviour after a transaction because they do not bear the full consequences, such as taking more risks after being insured"),
         ("signalling", "an action by the better-informed party to reveal information, such as offering a warranty or obtaining a qualification"),
         ("screening", "an action by the less-informed party to find out hidden information, such as medical checks before insurance")],
  facts=[("A driver who has just bought comprehensive car insurance starts parking in unsafe areas. This is an example of which of the following?", "Moral hazard", ["Adverse selection", "Signalling", "Screening"], "Behaviour changes after the contract because the cost of risk is borne by the insurer."),
         ("George Akerlof's 1970 paper 'The Market for Lemons' analysed which of the following?", "Adverse selection in the used-car market", ["Moral hazard in banking", "Public goods", "Price discrimination"], "Buyers cannot tell good cars from 'lemons', so good cars are driven out of the market."),
         ("Which of the following is a response by sellers to asymmetric information?", "Offering a warranty on a used car", ["A government ban on used cars", "A tax on insurance", "A price ceiling"], "A warranty signals quality."),
         ("Which of the following is the best example of adverse selection?", "People with health problems are more likely to buy health insurance", ["Insured people take fewer precautions", "Banks lend more after being bailed out", "Workers shirk when not monitored"], "Hidden characteristics before the transaction.")],
  why=[("Explain why adverse selection can lead to the collapse of a market.", "If buyers cannot distinguish quality, they will pay only an average price; owners of high-quality goods withdraw because the price is below their value, so average quality falls, buyers lower their offers further, and the market may shrink or disappear."),
       ("Explain why government bailouts of banks may create moral hazard.", "If banks expect to be rescued when they fail, they do not bear the full cost of risky lending, so they take more risks than they otherwise would."),
       ("Explain how licensing of professionals such as doctors addresses asymmetric information.", "Patients cannot judge medical competence; licensing requires minimum qualifications and standards, reducing the risk of poor-quality providers and giving consumers confidence.")],
  contrast=[("adverse selection", "moral hazard", "Adverse selection arises from hidden characteristics before a transaction (e.g. high-risk people buying insurance); moral hazard arises from hidden actions after a transaction (e.g. insured people taking more risks)."),
            ("signalling", "screening", "Signalling is action by the better-informed party to reveal information (warranties, qualifications); screening is action by the less-informed party to uncover it (inspections, medical examinations).")],
  misc=[("Moral hazard occurs when sellers lie about the quality of a product before it is sold.", "That is a hidden-characteristics problem (adverse selection); moral hazard is a change in behaviour after a transaction because the person is protected from the consequences."),
        ("Asymmetric information only affects buyers.", "Either side can be less informed: insurers (sellers) know less about buyers' risks, while buyers of used cars know less than sellers.")],
  apply=[("Explain how car-history reports and online seller ratings (e.g. on platforms such as Carousell or eBay) reduce asymmetric information.", "They give buyers verified information about past ownership, accidents and seller reliability, reducing adverse selection and allowing good-quality sellers to receive higher prices.", 2),
         ("An insurance company introduces an excess (deductible) of $500 on claims. Explain how this reduces moral hazard.", "Policyholders now bear part of the cost of any claim, so they have an incentive to take care to avoid losses.", 2)],
  cases=[("the 2008 global financial crisis", "Banks sold mortgage-backed securities whose risks were poorly understood by buyers; when US house prices fell, losses spread worldwide and governments bailed out major banks.", "asymmetric information and moral hazard", "Originators knew more about loan quality than investors (adverse selection), and expectations of bailouts encouraged excessive risk-taking (moral hazard).")],
  sources=[("A used-car market contains 'good' cars worth $12,000 to buyers and 'lemons' worth $4,000. Buyers cannot tell them apart and believe half the cars are lemons. Owners of good cars will not sell for less than $10,000.", "Hypothetical example based on Akerlof (1970)", "Using the data, explain what will happen in this market.", "Buyers offer the expected value 0.5 × 12,000 + 0.5 × 4,000 = $8,000; owners of good cars require $10,000, so they withdraw; only lemons remain, buyers then offer only $4,000 – adverse selection drives good cars out.")],
  evaluate=[("Government regulation is the best response to asymmetric information.", ["licensing, disclosure rules and consumer protection laws", "mandatory insurance reduces adverse selection (health mandates)"], ["private solutions: warranties, reputation, ratings, certification", "regulation can be costly and create barriers to entry", "information technology is reducing asymmetries"], "Regulation is important in high-stakes markets (health, finance), but private signals and technology often address asymmetric information more cheaply."),
            ("Moral hazard makes deposit insurance and bank bailouts more harmful than beneficial.", ["encourages risky lending", "taxpayers bear the cost"], ["prevents bank runs and systemic collapse", "costs of financial crises are enormous", "regulation (capital requirements) limits moral hazard"], "Insurance and bailouts create moral hazard, but their stabilising benefits are large; the answer is strong regulation rather than removing protection.")],
  extended=[("Using the example of health insurance, explain the difference between adverse selection and moral hazard and evaluate one policy to reduce each.", "Adverse selection: high-risk people more likely to buy – premiums rise, healthy people leave; policy: mandatory insurance (US Affordable Care Act mandate), community rating. Moral hazard: insured over-use services; policy: co-payments/excesses. Evaluate effectiveness, equity, costs.", 8, 'long')],
  diag=[("how adverse selection can cause under-consumption in a market such as health insurance", "Diagram: market for insurance; with asymmetric information, insurers charge premiums based on average risk; low-risk buyers' demand falls (their MPB of insurance is below the premium), so demand shifts left from D (full information) to D1 and the quantity of insurance bought falls below the efficient level Q*. Welfare loss from under-provision; policy such as mandates shifts demand back.")])


@R.add('ch12-st2', 'C3', (2, 5), 'numerical')
def lemons(rng, slot):
    good = rng.choice([10000, 12000, 15000, 20000])
    bad = rng.choice([3000, 4000, 5000, 6000])
    p = rng.choice([0.2, 0.3, 0.4, 0.5, 0.6])
    res = rng.choice([int(good * 0.8), int(good * 0.85), int(good * 0.9)])
    ev = p * bad + (1 - p) * good
    stays = ev >= res
    item = rng.choice(['used cars', 'second-hand laptops', 'used motorbikes', 'pre-owned smartphones (×10 value units)'])
    return dict(stem=f'In a market for {item}, high-quality items are worth ${good:,} to buyers and low-quality items (lemons) ${bad:,}. Buyers cannot tell them apart and believe {int(p * 100)}% are lemons. Sellers of high-quality items will not accept less than ${res:,}. Calculate the price buyers are willing to pay and explain whether high-quality items will be sold.',
                answer=f'${fmt(ev, 6)}; high-quality items {"are" if stays else "are not"} sold',
                markingKey=f'Expected value = {p} × {bad:,} + {1 - p:.1f} × {good:,} = {fmt(ev, 6)} [2]; {"≥" if stays else "<"} {res:,} so good sellers {"stay" if stays else "withdraw – adverse selection; average quality falls and the market may collapse to lemons"} [2].', type='numerical', marks=4)


S('ch12-st3',
  terms=[("market power", "the ability of a firm to influence the price of its product, which can lead to higher prices and lower output than in a competitive market"),
         ("competition policy (anti-trust)", "laws and regulations designed to promote competition and prevent abuse of market power, such as banning cartels and blocking mergers"),
         ("concentration ratio", "the share of total market output or sales accounted for by the largest firms, e.g. the four-firm concentration ratio (CR4)"),
         ("cartel", "a formal agreement between firms to fix prices or restrict output to act like a monopoly"),
         ("price regulation", "government rules limiting the price a firm with market power may charge, such as marginal cost or average cost pricing for natural monopolies"),
         ("nationalisation", "transferring a privately owned firm into government ownership")],
  facts=[("Which of the following is an example of competition policy?", "The European Commission fining Google €4.34 billion in 2018 for abusing its Android dominance", ["A subsidy for solar panels", "A minimum wage", "A tax on sugary drinks"], "Competition authorities punish abuse of dominant positions."),
         ("Why is market power considered a market failure?", "Firms restrict output and raise price above marginal cost, causing allocative inefficiency", ["Firms always make losses", "Prices are always too low", "It causes negative externalities"], "P > MC means output is below the allocatively efficient level."),
         ("If the four largest firms in a market have shares of 30%, 20%, 15% and 10%, what is the four-firm concentration ratio?", "75%", ["30%", "18.75%", "100%"], "Sum of the four largest shares."),
         ("Which of the following is a reason for regulating rather than breaking up a natural monopoly?", "Economies of scale mean one firm can supply the market at the lowest cost", ["It has no market power", "It always makes losses", "Consumers prefer monopolies"], "Splitting it would raise average costs.")],
  why=[("Explain why monopolies may lead to allocative inefficiency.", "A monopolist maximises profit where MC = MR, which is below the competitive output; it sets price above marginal cost (P > MC), so consumers value extra units more than they cost to produce, but they are not produced – welfare loss."),
       ("Explain why governments block some mergers.", "A merger can create a firm with significant market power that could raise prices, reduce choice and innovation; competition authorities assess whether the merger would substantially lessen competition."),
       ("Explain why cartels are illegal in most countries.", "Cartels fix prices or share markets, acting like a monopoly: prices rise and output falls, harming consumers and reducing efficiency, while firms gain abnormal profits.")],
  contrast=[("legislation (competition law)", "regulation of a natural monopoly", "Competition law prohibits anti-competitive behaviour such as cartels and abuse of dominance across the economy; regulation of a natural monopoly sets prices or quality standards for a single dominant firm where competition is not efficient."),
            ("a four-firm concentration ratio", "a firm's market share", "Market share is one firm's share of total sales; the CR4 is the combined share of the four largest firms, indicating how concentrated the market is.")],
  misc=[("Large firms always harm consumers.", "Large firms may achieve economies of scale and invest in R&D, lowering prices and improving products; harm arises when market power is abused (higher prices, less innovation)."),
        ("A high concentration ratio proves that firms are colluding.", "Concentration shows that a few firms dominate, but it does not prove collusion; firms may compete fiercely (e.g. in price or innovation) even in concentrated markets.")],
  apply=[("In 2016 the European Commission fined truck makers including Daimler, Volvo and DAF a total of €2.93 billion for a 14-year cartel. Explain how the cartel harmed customers.", "The firms coordinated prices and the timing of passing on emission-technology costs, so trucks were priced above competitive levels; customers (haulage firms) paid more, which also raised transport costs in the wider economy.", 3)],
  cases=[("the EU's €2.42 billion fine on Google in 2017", "The European Commission found that Google had favoured its own comparison-shopping service in search results.", "competition policy against abuse of market power", "Using dominance in search to disadvantage rivals reduced competition; the fine and required changes aimed to restore a level playing field.")],
  sources=[("In the market for mobile phone services in a country, the largest four firms have market shares of 38%, 27%, 19% and 9%. The competition authority is reviewing a proposed merger between the second- and fourth-largest firms.", "Hypothetical competition authority report", "Calculate the four-firm concentration ratio before the merger and explain why the authority may oppose the merger.", "CR4 = 38 + 27 + 19 + 9 = 93%; after the merger the new firm would have 36%, giving two firms with 74% between them; reduced competition could lead to higher prices and less choice and innovation.")],
  evaluate=[("Competition policy is the best way to deal with the market failure caused by market power.", ["promotes competition, lowering prices and raising efficiency", "deters cartels through large fines", "blocks harmful mergers"], ["natural monopolies need regulation, not competition", "large fines may be treated as a cost of doing business", "global tech firms are hard to regulate across borders", "nationalisation or price caps may be needed in some industries"], "Competition policy is central, but regulation is needed for natural monopolies and international coordination for global firms.")],
  extended=[("Evaluate the use of price regulation to control a natural monopoly such as a national electricity grid.", "Options: marginal cost pricing (allocative efficiency but losses requiring subsidy), average cost pricing (normal profit, some inefficiency), price caps such as RPI − X; problems: information asymmetry, regulatory capture, incentives to cut quality; alternatives: nationalisation.", 8, 'long')],
  diag=[("the welfare loss caused by market power compared with a competitive market", "Diagram: a monopolist's AR (demand) and MR, with MC. Profit-maximising output Qm where MC = MR, price Pm on AR. Competitive output Qc where P = MC (AR = MC) at Pc. Pm > Pc, Qm < Qc; welfare loss triangle between AR and MC from Qm to Qc; part of consumer surplus is transferred to the firm as abnormal profit.")])


@R.add('ch12-st3', 'C3', (1, 5), 'numerical')
def conc_ratio(rng, slot):
    for _ in range(30):
        sh = sorted(rng.sample(range(4, 40), 6), reverse=True)
        if sum(sh) <= 100:
            break
    else:
        return None
    mkt = rng.choice(['supermarkets in a country', 'airlines on domestic routes', 'mobile network operators', 'cement producers', 'banks', 'streaming services'])
    cr4 = sum(sh[:4])
    if slot.d <= 2:
        return dict(stem=f'The market shares of the six largest {mkt} are {", ".join(str(s) + "%" for s in sh)}. Calculate the four-firm concentration ratio.',
                    answer=f'{cr4}%', markingKey=f'CR4 = {" + ".join(map(str, sh[:4]))} = {cr4}%. [1] [1]', type='numerical', marks=2)
    i, j = 1, 3
    new = sh[i] + sh[j]
    shares2 = sorted([s for k, s in enumerate(sh) if k not in (i, j)] + [new], reverse=True)
    cr4b = sum(shares2[:4])
    return dict(stem=f'The market shares of the six largest {mkt} are {", ".join(str(s) + "%" for s in sh)}. The second- and fourth-largest firms propose to merge. Calculate the CR4 before and after the merger and explain one reason the competition authority might block it.',
                answer=f'CR4 {cr4}% before, {cr4b}% after; merged firm {new}%',
                markingKey=f'Before: {" + ".join(map(str, sh[:4]))} = {cr4}% [1]; merged firm {sh[i]} + {sh[j]} = {new}%, new top four {" + ".join(map(str, shares2[:4]))} = {cr4b}% [2]; reason: greater market power → higher prices, less choice/innovation, risk of collusion [1].', type='numerical', marks=4)

# =============================================================================================
# ch13 Unit 2.11 (HL) Market power: theory of the firm and market structures
# =============================================================================================
S('ch13-st1',
  terms=[("fixed costs", "costs that do not change with output in the short run, such as rent and insurance"),
         ("variable costs", "costs that change with output, such as raw materials and hourly wages"),
         ("marginal cost (MC)", "the extra cost of producing one more unit of output, ΔTC/ΔQ"),
         ("average total cost (ATC)", "total cost divided by quantity of output, equal to AFC + AVC"),
         ("economies of scale", "falls in long-run average cost as a firm increases the scale of all its inputs"),
         ("diseconomies of scale", "rises in long-run average cost as a firm grows beyond its optimum size, for example because of coordination problems"),
         ("marginal revenue (MR)", "the extra revenue from selling one more unit of output, ΔTR/ΔQ")],
  facts=[("Which of the following explains why the short-run marginal cost curve eventually rises?", "Diminishing marginal returns to the variable factor", ["Economies of scale", "Falling fixed costs", "Rising demand"], "With a fixed factor, extra workers add less output, so each unit costs more."),
         ("The MC curve cuts the ATC and AVC curves at which point?", "At their minimum points", ["At their maximum points", "Where they are rising fastest", "Where ATC equals AFC"], "When MC < average, average falls; when MC > average, average rises."),
         ("Which of the following is an example of a purchasing economy of scale?", "A large supermarket chain obtaining bulk-buying discounts", ["Hiring more managers", "Using a fixed factory more intensively", "A rise in wages"], "Bulk purchasing lowers unit costs for larger firms."),
         ("What happens to average fixed cost as output rises?", "It falls continuously", ["It rises", "It stays constant", "It first falls then rises"], "Fixed cost is spread over more units.")],
  why=[("Explain why the long-run average cost curve is often U-shaped.", "At first, economies of scale (specialisation, bulk buying, technical, financial) lower average costs as the firm grows; beyond the minimum efficient scale, diseconomies of scale (coordination, communication, motivation problems) raise average costs."),
       ("Explain why the short-run average total cost curve is U-shaped.", "Initially AFC falls quickly as fixed costs are spread and AVC falls with increasing returns; later diminishing marginal returns raise AVC and MC, which eventually outweighs the fall in AFC."),
       ("Explain why marginal cost cuts average cost at its minimum.", "If the extra unit costs less than the average, the average falls; if more, the average rises; so the average is at its minimum where MC equals it.")],
  contrast=[("economies of scale", "diminishing marginal returns", "Economies of scale are a long-run concept – average costs fall as all inputs increase; diminishing marginal returns are a short-run concept – marginal product falls as a variable factor is added to a fixed one."),
            ("fixed costs", "variable costs", "Fixed costs do not change with output in the short run (rent); variable costs rise with output (raw materials).")],
  misc=[("Fixed costs never change.", "Fixed costs do not vary with output in the short run, but they can change over time (e.g. a rent increase) and in the long run all costs are variable."),
        ("If marginal cost is rising, average total cost must also be rising.", "ATC rises only when MC is above ATC; MC can be rising while still below ATC, in which case ATC is still falling.")],
  apply=[("Identify two economies of scale a firm such as Toyota might benefit from.", "e.g. technical (large automated assembly lines), purchasing (bulk discounts on steel and parts), financial (borrowing at lower interest rates), marketing (advertising spread over many cars).", 2)],
  cases=[("Maersk's Triple-E container ships", "Ships carrying around 18,000 containers cut fuel and crew costs per container substantially compared with smaller vessels.", "technical economies of scale", "Larger ships spread fixed crew and fuel costs over more units, lowering the long-run average cost of shipping each container.")],
  evaluate=[("Economies of scale mean that large firms are always more efficient than small firms.", ["lower average costs through specialisation, bulk buying, cheaper finance", "can invest in R&D"], ["diseconomies of scale beyond the minimum efficient scale", "small firms can be flexible and innovative", "in some industries (hairdressing) the efficient scale is small"], "Large firms can be more efficient up to a point, but beyond the minimum efficient scale diseconomies arise and in many industries small firms are efficient.")],
  extended=[("A bakery has fixed costs of $200 per day and variable costs that rise as output increases. Explain the shapes of its AFC, AVC, ATC and MC curves in the short run.", "AFC falls continuously (fixed cost spread); AVC and MC fall then rise (increasing then diminishing returns); MC cuts AVC and ATC at their minima; the gap between ATC and AVC equals AFC and narrows as output rises.", 6)],
  diag=[("the shape of the long-run average cost curve with reference to economies and diseconomies of scale", "Diagram: cost on the vertical axis, output on the horizontal; U-shaped LRAC as the envelope of several SRAC curves. Falling section: economies of scale; minimum point: minimum efficient scale; rising section: diseconomies of scale.")])


@R.add('ch13-st1', 'C3', (1, 5), 'numerical')
def cost_table(rng, slot):
    tfc = rng.choice([50, 60, 80, 100, 120])
    mcs = [rng.randint(10, 20)]
    mcs.append(mcs[0] - rng.randint(1, 5))
    for _ in range(3):
        mcs.append(mcs[-1] + rng.randint(3, 10))
    tvc = []
    s = 0
    for m in mcs:
        s += m
        tvc.append(s)
    biz = rng.choice(['a pizza restaurant', 'a T-shirt printer', 'a car-wash', 'a small brewery', 'a bakery'])
    tab = ', '.join(f'Q = {i + 1}: TC = {tfc + tvc[i]}' for i in range(5))
    q = rng.randint(2, 5)
    if slot.d <= 2:
        return dict(stem=f'The total cost of {biz} is: Q = 0: TC = {tfc}, {tab} (units per hour, costs in $). Calculate the marginal cost of unit {q}.',
                    answer=f'${mcs[q - 1]}', markingKey=f'MC = TC({q}) − TC({q - 1}) = {tfc + tvc[q - 1]} − {tfc + (tvc[q - 2] if q > 1 else 0)} = {mcs[q - 1]}. [1] [1]', type='numerical', marks=2)
    atc = (tfc + tvc[q - 1]) / q
    avc = tvc[q - 1] / q
    afc = tfc / q
    return dict(stem=f'The total cost of {biz} is: Q = 0: TC = {tfc}, {tab} (costs in $). State the fixed cost and calculate AFC, AVC, ATC and MC at Q = {q}.',
                answer=f'TFC = ${tfc}; AFC = {r2(afc)}, AVC = {r2(avc)}, ATC = {r2(atc)}, MC = {mcs[q - 1]}',
                markingKey=f'TFC = TC at Q = 0 = {tfc} [1]; AFC = {tfc}/{q} = {r2(afc)}; AVC = ({tfc + tvc[q - 1]} − {tfc})/{q} = {r2(avc)} [1]; ATC = {tfc + tvc[q - 1]}/{q} = {r2(atc)} [1]; MC = {mcs[q - 1]} [1].', type='numerical', marks=4)


S('ch13-st2',
  terms=[("profit maximisation rule", "a firm maximises profit by producing the output at which marginal cost equals marginal revenue (MC = MR), with MC rising"),
         ("normal profit", "the minimum profit needed to keep a firm in its industry, included in costs, so economic profit is zero"),
         ("abnormal (supernormal) profit", "profit above normal profit, when total revenue exceeds total economic cost (AR > ATC)"),
         ("perfect competition", "a market structure with many small firms, identical products, perfect information and free entry and exit, so each firm is a price taker"),
         ("shut-down price", "the price equal to minimum average variable cost, below which a firm should stop producing in the short run"),
         ("break-even price", "the price equal to minimum average total cost, at which the firm earns normal profit")],
  facts=[("In perfect competition, the demand curve facing an individual firm is which of the following?", "Perfectly elastic at the market price (P = AR = MR)", ["Downward-sloping", "Perfectly inelastic", "Upward-sloping"], "Each firm is a price taker."),
         ("In the long run in perfect competition, firms earn which of the following?", "Normal profit only", ["Abnormal profit", "Losses", "Monopoly profit"], "Free entry and exit remove abnormal profits and losses."),
         ("A firm making losses should continue to produce in the short run if price covers which of the following?", "Average variable cost", ["Average total cost", "Marginal cost only", "Average fixed cost"], "It covers variable costs and contributes to fixed costs."),
         ("Perfectly competitive firms in long-run equilibrium are both allocatively and productively efficient because of which condition?", "P = MC and P = minimum ATC", ["MR = 0", "P > MC", "AR > ATC"], "Price equals marginal cost and output is at minimum average cost.")],
  why=[("Explain why a firm maximises profit where MC = MR.", "If MR > MC, producing an extra unit adds more to revenue than to cost, so profit rises; if MC > MR, the last unit reduces profit. Profit is greatest where the two are equal."),
       ("Explain how abnormal profits are eliminated in perfect competition in the long run.", "Abnormal profits attract new firms (free entry, perfect information); market supply shifts right, the price falls until P = minimum ATC and only normal profit is made."),
       ("Explain why a loss-making firm may continue to produce in the short run.", "Fixed costs must be paid whether or not it produces; if price exceeds AVC, revenue covers variable costs and contributes something to fixed costs, so losses are smaller than if it shut down."),
       ("Explain why perfectly competitive markets are allocatively efficient in the long run.", "Firms produce where P = MC; price reflects consumers' marginal benefit, so the value of the last unit equals the cost of producing it, maximising social surplus.")],
  contrast=[("normal profit", "abnormal profit", "Normal profit is the minimum return needed to keep the firm in the industry (TR = TC including opportunity costs); abnormal profit is any profit above this (TR > TC)."),
            ("the shut-down price", "the break-even price", "The shut-down price equals minimum AVC – below it the firm should stop producing in the short run; the break-even price equals minimum ATC – at it the firm makes normal profit.")],
  misc=[("A perfectly competitive firm can raise its price above the market price to increase profit.", "It is a price taker: identical products and perfect information mean that if it raises price, customers buy from rivals and its sales fall to zero."),
        ("Firms should always shut down when they make a loss.", "In the short run a firm should continue if price covers AVC, because shutting down still leaves fixed costs to pay; it shuts down only if P < AVC (and leaves in the long run if P < ATC).")],
  apply=[("Explain why the agricultural market for wheat is often used as an example close to perfect competition.", "Many small farmers, a homogeneous product, buyers well informed about prices (world markets), and relatively free entry and exit; each farmer accepts the market price.", 2)],
  cases=[("the market for foreign exchange", "Huge numbers of buyers and sellers trade identical currencies with near-perfect information and prices that adjust instantly.", "features of perfect competition", "No individual trader can influence the price; they are price takers in a highly competitive market.")],
  evaluate=[("Perfect competition is the ideal market structure.", ["allocative and productive efficiency in the long run", "low prices and consumer sovereignty", "no abnormal profits"], ["no abnormal profits to fund R&D, so less dynamic efficiency", "no economies of scale", "homogeneous products limit consumer choice", "the model is unrealistic"], "Perfect competition is an efficiency benchmark, but dynamic efficiency, economies of scale and product variety mean other structures can deliver benefits.")],
  extended=[("Using diagrams, explain how a perfectly competitive industry adjusts from short-run abnormal profits to long-run equilibrium.", "Firm diagram: P1 above ATC at MC = MR, abnormal profit rectangle; industry diagram: new firms enter, supply shifts right, price falls to P2 = minimum ATC; firm earns normal profit at MC = MR = AR = ATC.", 6)],
  diag=[("the short-run equilibrium of a perfectly competitive firm making abnormal profits", "Two diagrams: industry D and S set market price Pm; firm faces horizontal D = AR = MR at Pm. Firm produces Q where MC = MR; ATC at Q is below Pm; abnormal profit = (Pm − ATC) × Q shaded. In the long run entry lowers price to minimum ATC.")])


@R.add('ch13-st2', 'C3', (2, 5), 'numerical')
def pc_profit(rng, slot):
    for _ in range(50):
        price = rng.choice([20, 24, 30, 36, 40])
        tfc = rng.choice([40, 60, 80, 100])
        mcs = [rng.randint(8, 14)]
        for _ in range(5):
            mcs.append(mcs[-1] + rng.randint(3, 8))
        q = max([i + 1 for i, m in enumerate(mcs) if m <= price], default=0)
        if 2 <= q <= 5 and price not in mcs:
            break
    else:
        return None
    tc = [tfc]
    for m in mcs:
        tc.append(tc[-1] + m)
    tr = [price * i for i in range(7)]
    prof = [tr[i] - tc[i] for i in range(7)]
    best = max(range(7), key=lambda i: prof[i])
    tab = ', '.join(f'Q = {i}: TC = {tc[i]}' for i in range(7))
    firm = rng.choice(['A wheat farm', 'A rose grower in Kenya', 'A small coffee farm in Vietnam', 'A fishing boat in Peru', 'A strawberry grower in Spain'])
    return dict(stem=f'{firm} sells in a perfectly competitive market at a price of ${price} per unit. Its total costs are: {tab}. Using MC = MR, find the profit-maximising output and calculate the profit or loss.',
                answer=f'Q = {best}; {"profit" if prof[best] >= 0 else "loss"} = {sm(prof[best])}',
                markingKey=f'MR = P = {price} [1]; MC: {", ".join(map(str, mcs))} [1]; produce while MC ≤ MR ⇒ Q = {best} [1]; profit = {price}×{best} − {tc[best]} = {prof[best]} ({"abnormal profit" if prof[best] > 0 else "loss" if prof[best] < 0 else "normal profit"}) [1].', type='numerical', marks=4)


S('ch13-st3',
  terms=[("monopoly", "a market structure in which a single firm supplies the whole market, with high barriers to entry"),
         ("barriers to entry", "obstacles that prevent new firms from entering a market, such as economies of scale, legal barriers (patents, licences), control of resources and brand loyalty"),
         ("natural monopoly", "a market in which one firm can supply the whole market at a lower average cost than two or more firms, because economies of scale are very large relative to demand"),
         ("allocative inefficiency of monopoly", "the outcome where a monopolist sets price above marginal cost (P > MC), so output is below the socially optimal level"),
         ("revenue maximisation", "producing where MR = 0, which maximises total revenue rather than profit")],
  facts=[("A profit-maximising monopolist produces where which of the following holds?", "MC = MR", ["P = MC", "P = ATC", "MR = 0"], "It then charges the price on the demand (AR) curve at that output."),
         ("Why can a monopolist earn abnormal profit in the long run?", "High barriers to entry prevent new firms from entering", ["It is productively efficient", "Demand is perfectly elastic", "It sets P = MC"], "Without entry, profits are not competed away."),
         ("Which of the following is the best example of a natural monopoly?", "Water pipe network in a city", ["A coffee shop", "A smartphone brand", "A farm"], "Duplicating the network would raise average costs."),
         ("A monopolist operates on which part of its demand curve?", "The price elastic part, where MR > 0", ["The inelastic part", "The unit elastic point only", "Any part, because demand is perfectly inelastic"], "MC > 0 = MR requires MR positive, i.e. elastic demand.")],
  why=[("Explain why a monopoly is allocatively inefficient.", "It produces where MC = MR; because MR is below price, price is above MC at that output (P > MC), so consumers value extra units more than they cost, but they are not produced – a welfare loss."),
       ("Explain why regulating a natural monopoly by setting price equal to marginal cost would cause losses.", "In a natural monopoly ATC is falling over the relevant range, so MC lies below ATC; a price equal to MC is below ATC and the firm makes a loss, requiring a subsidy."),
       ("Explain why monopolies might benefit consumers.", "Abnormal profits can fund research and development (dynamic efficiency), and large economies of scale can mean lower costs and possibly lower prices than a fragmented industry (natural monopoly)."),
       ("Explain why a monopolist never produces where demand is price inelastic.", "If demand is inelastic, MR is negative; raising price and cutting output would raise revenue and lower costs, increasing profit. So profit is maximised only where MR > 0, on the elastic part.")],
  contrast=[("a monopoly", "a natural monopoly", "A monopoly is any single-firm market protected by barriers; a natural monopoly arises because economies of scale are so large that one firm supplies the market at lowest cost."),
            ("monopoly", "perfect competition", "A monopolist faces the downward-sloping market demand curve, sets P > MC and can earn long-run abnormal profit behind barriers; perfectly competitive firms are price takers that earn normal profit in the long run with P = MC = minimum ATC.")],
  misc=[("A monopolist can charge any price it likes and still sell as much as it wants.", "A monopolist faces the market demand curve: a higher price reduces quantity demanded, so it chooses price and quantity together to maximise profit."),
        ("Natural monopolies should always be broken up into smaller competing firms.", "Breaking up a natural monopoly would raise average costs because economies of scale are lost; regulation or public ownership is usually preferred.")],
  apply=[("De Beers controlled most of the world's rough diamond supply for much of the 20th century. Identify the barrier to entry and explain how it allowed high prices.", "Control of essential resources (mines) and stockpiling; by limiting supply De Beers kept prices well above marginal cost, earning abnormal profit.", 3)],
  cases=[("the patent on Gilead's hepatitis C drug sofosbuvir (Sovaldi)", "Launched in the US in 2013 at about $84,000 for a 12-week course, far above production cost; generic versions in India later cost a few hundred dollars.", "monopoly power from legal barriers", "The patent created a legal monopoly, allowing price far above marginal cost while funding R&D – the trade-off between static and dynamic efficiency.")],
  sources=[("A regulator sets a price cap of RPI − 3% on a national water company, meaning prices may rise by 3 percentage points less than inflation each year. The company says the cap will make investment in new pipes difficult; consumer groups say it makes abnormal profits.", "Hypothetical regulator statement", "Using the extract, explain why the regulator uses a price cap for a natural monopoly.", "A natural monopoly would otherwise set P > MC and earn abnormal profit; the cap limits price increases, forcing efficiency gains (X = 3%) and passing them to consumers, while still letting the firm cover costs; risk of under-investment.")],
  evaluate=[("Monopolies are always against the public interest.", ["higher prices and lower output than competition", "allocative and possibly productive inefficiency", "x-inefficiency from lack of competition"], ["economies of scale (natural monopoly)", "abnormal profits fund R&D and innovation (pharmaceuticals, technology)", "regulation can limit abuse"], "Monopolies impose static efficiency costs, but where economies of scale or innovation are important, regulated monopolies can serve the public interest.")],
  extended=[("Using a diagram, compare the price and output of a profit-maximising monopolist with those of a perfectly competitive industry with the same costs, and explain the welfare loss.", "Monopolist: MC = MR, Qm, Pm on AR. Competitive industry: P = MC, Qc > Qm, Pc < Pm. Welfare loss triangle between AR and MC from Qm to Qc; consumer surplus transferred to the monopolist as abnormal profit.", 6)],
  diag=[("why a natural monopoly exists and the problem with regulating it using marginal cost pricing", "Diagram: falling LRAC over the whole range of market demand; MC below AC; demand AR and MR. Unregulated: MC = MR, Pm > AC, abnormal profit. Marginal cost pricing (P = MC) gives allocative efficiency but P < AC, a loss requiring subsidy; average cost pricing (P = AC) gives normal profit with output below the allocatively efficient level.")])


@R.add('ch13-st3', 'C3', (2, 5), 'numerical')
def monopoly_calc(rng, slot):
    for _ in range(50):
        b = rng.choice([1, 2, 4, 5])
        mc = rng.choice([10, 20, 30, 40])
        a = mc + 2 * b * rng.randint(5, 20)
        Qm = (a - mc) / (2 * b)
        if Qm == int(Qm):
            break
    Qm = int(Qm)
    Pm = a - b * Qm
    Qc = (a - mc) / b
    F_ = rng.choice([0, 100, 200, 500])
    prof = (Pm - mc) * Qm - F_
    dwl = 0.5 * (Pm - mc) * (Qc - Qm)
    firm = rng.choice(['a patented medicine', 'the only ferry service to an island', 'a city\'s sole cable-TV provider', 'a regional rail operator', 'a software platform with no rivals'])
    bb = '' if b == 1 else str(b)
    return dict(stem=f'The demand for {firm} is P = {a} − {bb}Q, so MR = {a} − {2 * b}Q. Marginal cost is constant at ${mc}{f" and fixed costs are ${F_}" if F_ else ""}. Calculate the profit-maximising price and output, the firm\'s profit, and the welfare loss compared with a competitive outcome where P = MC.',
                answer=f'Q = {Qm}, P = ${Pm}; profit = ${fmt(prof, 6)}; welfare loss = ${fmt(dwl, 6)}',
                markingKey=f'MC = MR: {mc} = {a} − {2 * b}Q ⇒ Q = {Qm} [1]; P = {a} − {b}×{Qm} = {Pm} [1]; profit = ({Pm} − {mc}) × {Qm}{f" − {F_}" if F_ else ""} = {fmt(prof, 6)} [1]; competitive Q = ({a} − {mc})/{b} = {fmt(Qc)}; welfare loss = ½ × ({Pm} − {mc}) × ({fmt(Qc)} − {Qm}) = {fmt(dwl, 6)} [1].', type='numerical', marks=4)


S('ch13-st4',
  terms=[("monopolistic competition", "a market structure with many firms selling differentiated products, low barriers to entry and some control over price"),
         ("oligopoly", "a market dominated by a few large interdependent firms, with high barriers to entry"),
         ("collusion", "cooperation between firms to limit competition, for example by fixing prices or sharing markets; formal collusion is a cartel"),
         ("game theory", "the study of strategic decision-making where the outcome for each player depends on the choices of others"),
         ("price discrimination", "charging different prices to different consumers for the same product for reasons not related to differences in cost"),
         ("non-price competition", "competition through advertising, branding, product quality and design rather than price"),
         ("dominant strategy", "a strategy that gives a player the best outcome whatever the other player chooses")],
  facts=[("In the long run, firms in monopolistic competition earn which of the following?", "Normal profit, because low barriers allow entry", ["Abnormal profit", "Losses", "Monopoly profit"], "Entry shifts each firm's demand left until P = ATC."),
         ("Which of the following is a key feature of oligopoly?", "Interdependence between firms", ["Many small firms", "No barriers to entry", "Identical products and perfect information"], "Each firm must consider rivals' reactions."),
         ("Which of the following conditions are necessary for price discrimination?", "Market power, separable markets with different PEDs, and no resale between markets", ["Perfect competition and identical consumers", "Perfectly elastic demand", "Low barriers to entry"], "Without these, arbitrage would remove price differences."),
         ("In the prisoner's dilemma applied to two firms, why do both firms often end up charging low prices?", "Each firm's dominant strategy is to cut price, even though both would earn more by keeping prices high", ["Low prices maximise joint profit", "The government sets the price", "Demand is perfectly inelastic"], "Lack of trust leads to the non-cooperative outcome."),
         ("OPEC+ agreeing production quotas is an example of which of the following?", "Formal collusion (a cartel)", ["Tacit collusion", "Monopolistic competition", "Price discrimination"], "Members explicitly agree output limits to raise prices.")],
  why=[("Explain why firms in oligopoly may prefer non-price competition.", "If one firm cuts price, rivals are likely to match it, starting a price war that reduces all firms' profits; competing through advertising, branding and product innovation avoids this while still gaining market share."),
       ("Explain why cartels tend to be unstable.", "Each member has an incentive to cheat by producing more than its quota at the high cartel price; if members cheat, price falls and the agreement breaks down, especially when there are many members or demand falls."),
       ("Explain how price discrimination can increase a firm's profit.", "By charging higher prices to consumers with inelastic demand and lower prices to those with elastic demand, the firm converts consumer surplus into revenue and sells to customers who would not pay a single high price."),
       ("Explain why firms in monopolistic competition are not productively efficient in the long run.", "Each firm faces a downward-sloping demand curve; in long-run equilibrium demand is tangent to ATC on its falling part, so output is below the minimum ATC level – excess capacity.")],
  contrast=[("formal collusion", "tacit collusion", "Formal collusion is an explicit agreement between firms (a cartel), usually illegal; tacit collusion is coordination without an agreement, such as price leadership, where firms follow a dominant firm's prices."),
            ("monopolistic competition", "oligopoly", "Monopolistic competition has many firms with differentiated products and low barriers, so long-run profits are normal; oligopoly has a few interdependent firms and high barriers, so abnormal profits can persist.")],
  misc=[("Price discrimination means charging different prices because some customers cost more to serve.", "Price discrimination is charging different prices for the same product for reasons not related to cost differences, based on differences in willingness to pay (PED)."),
        ("In oligopoly firms always collude because it maximises their profits.", "Collusion is usually illegal and unstable; firms face incentives to cheat, and many oligopolies compete fiercely on price or through non-price competition.")],
  apply=[("Explain how airlines practise price discrimination, and why business travellers usually pay more.", "Airlines charge different fares for the same seat according to booking time, flexibility and day of travel; business travellers have inelastic demand (urgent, employer pays), so they are charged higher fares, while leisure travellers with elastic demand get cheap advance fares.", 3)],
  cases=[("OPEC+ production cuts in 2016 and 2020", "In April 2020 OPEC+ agreed to cut output by almost 10 million barrels a day as demand collapsed during the pandemic.", "collusion in oligopoly", "Members acted together to restrict supply and support prices, behaving like a monopoly, though compliance with quotas varied."),
         ("cafés and restaurants in a city such as Melbourne", "There are thousands of cafés, each differentiated by location, style, coffee and atmosphere; new cafés open and others close frequently.", "monopolistic competition", "Product differentiation gives each café some price-setting power, but easy entry means abnormal profits are competed away in the long run.")],
  sources=[("Two supermarket chains dominate a country's grocery market. If both keep prices high, each earns $50m profit. If one cuts prices and the other does not, the price-cutter earns $70m and the other $20m. If both cut prices, each earns $35m.", "Hypothetical payoff data", "Using game theory, explain the likely outcome and why it is a dilemma for the firms.", "Whatever the rival does, cutting price gives more profit (70 > 50; 35 > 20), so cutting is a dominant strategy; both cut and earn $35m each, although both keeping prices high would give $50m each – a prisoner's dilemma.")],
  evaluate=[("Oligopolies are harmful to consumers.", ["tendency to collude (cartels, tacit price leadership) raising prices", "high barriers protect abnormal profits", "allocative inefficiency"], ["fierce price and non-price competition (supermarkets, airlines)", "economies of scale lower costs", "abnormal profits fund innovation (smartphones)", "competition policy limits collusion"], "Oligopolies can harm consumers when they collude, but competitive oligopolies often deliver low prices and innovation; outcomes depend on behaviour and regulation."),
            ("Price discrimination always makes consumers worse off.", ["transfers consumer surplus to producers", "consumers in the high-price market pay more"], ["consumers in low-price markets (students, off-peak) may gain access they would otherwise not have", "can make services viable that would otherwise not be supplied (rural rail, medicines)", "output may rise towards the efficient level"], "Price discrimination redistributes surplus to firms but can increase output and access for some groups, so its effect on consumers is mixed.")],
  extended=[("Using a payoff matrix, explain why firms in oligopoly may have an incentive to collude and an incentive to cheat on any agreement.", "Matrix with high/low price strategies; joint profit is highest if both price high (collusion); each firm gains by undercutting (cheating) if the other keeps price high; dominant strategy leads to low-price equilibrium; repeated games, trust and enforcement explain collusion; legal penalties.", 6)],
  diag=[("the long-run equilibrium of a firm in monopolistic competition", "Diagram: downward-sloping AR and MR; MC and ATC. Firm produces where MC = MR; in the long run entry shifts AR left until it is tangent to ATC, so P = ATC and profit is normal; output is to the left of minimum ATC (excess capacity) and P > MC (allocative inefficiency)."),
        ("third-degree price discrimination between two groups of consumers", "Diagrams for market A (inelastic demand) and market B (elastic demand) with a common MC. The firm sets MR = MC in each market: a higher price in A and a lower price in B. Total profit is higher than with a single price because consumer surplus is captured in market A while sales are expanded in market B.")])


@R.add('ch13-st4', 'C3', (2, 5), 'numerical')
def game_theory(rng, slot):
    for _ in range(80):
        hh = rng.randint(30, 80)
        lh = hh + rng.randint(5, 30)
        hl = rng.randint(5, hh - 5)
        ll = rng.randint(hl + 1, hh - 1)
        if hl < ll < hh < lh:
            break
    else:
        return None
    f1, f2 = rng.choice([('Airline A', 'Airline B'), ('Firm X', 'Firm Y'), ('Supermarket 1', 'Supermarket 2'), ('Telecom North', 'Telecom South')])
    strat = rng.choice([('High price', 'Low price'), ('Keep output low', 'Increase output'), ('Maintain fare', 'Cut fare')])
    stem = (f'{f1} and {f2} are the only two firms in a market. Profits ($m) for ({f1}, {f2}): both choose "{strat[0]}": ({hh}, {hh}); {f1} "{strat[1]}", {f2} "{strat[0]}": ({lh}, {hl}); '
            f'{f1} "{strat[0]}", {f2} "{strat[1]}": ({hl}, {lh}); both "{strat[1]}": ({ll}, {ll}). Identify each firm\'s dominant strategy, the likely outcome and explain why the firms might try to collude.')
    return dict(stem=stem, answer=f'Dominant strategy for both: "{strat[1]}"; outcome ({ll}, {ll}); collusion on "{strat[0]}" would give ({hh}, {hh})',
                markingKey=f'If rival chooses "{strat[0]}": {lh} > {hh}; if rival chooses "{strat[1]}": {ll} > {hl} ⇒ "{strat[1]}" dominant [2]; Nash equilibrium ({ll}, {ll}) [1]; joint profit higher at ({hh}, {hh}), so incentive to collude, but each has an incentive to cheat – prisoner\'s dilemma [1].', type='numerical', marks=4)


@R.add('ch13-st4', 'C3', (2, 5), 'numerical')
def price_disc(rng, slot):
    pa, qa = rng.choice([(120, 200), (150, 300), (90, 400), (200, 150)])
    pb, qb = rng.choice([(40, 500), (50, 800), (30, 1000), (60, 600)])
    ps, qs = rng.choice([(80, 450), (70, 600), (100, 350)])
    ctx = rng.choice([('a cinema chain in Mumbai', 'adults at evening shows', 'students at matinees'), ('a rail operator in the UK', 'peak commuters', 'off-peak leisure travellers'),
                      ('a theme park in Florida', 'tourists buying at the gate', 'local residents with annual passes'), ('a software firm', 'corporate licences', 'student licences')])
    who, A_, B_ = ctx
    trd = pa * qa + pb * qb
    tru = ps * qs
    return dict(stem=f'{who.capitalize()} can charge ${pa} to {A_} (selling {qa} units) and ${pb} to {B_} (selling {qb} units), or a single price of ${ps} to everyone (selling {qs} units). Marginal cost is negligible. Calculate total revenue under each option and explain the conditions needed for price discrimination.',
                answer=f'Price discrimination ${trd:,}; single price ${tru:,}',
                markingKey=f'Discrimination: {pa}×{qa} + {pb}×{qb} = {trd:,} [1]; single price: {ps}×{qs} = {tru:,} [1]; conditions: market power, ability to separate groups with different PED, no resale [2].', type='numerical', marks=4)

# =============================================================================================
# ch14 Unit 2.12 The market's inability to achieve equity; the IA commentary
# =============================================================================================
S('ch14-st1',
  terms=[("equality", "a situation in which everyone has the same income, wealth or opportunities"),
         ("equity", "fairness or justice in the distribution of income, wealth and opportunities; a normative concept"),
         ("income inequality", "the unequal distribution of income among individuals or households in an economy"),
         ("Gini coefficient", "a measure of income inequality from 0 (perfect equality) to 1 (one person receives all income), derived from the Lorenz curve"),
         ("equality of opportunity", "a situation in which everyone has the same chances to succeed, regardless of background"),
         ("Lorenz curve", "a curve showing the cumulative percentage of income received by cumulative percentages of the population, compared with a line of perfect equality")],
  facts=[("Why does the free market tend to produce unequal incomes?", "Factor incomes depend on ownership of resources, skills and bargaining power, which are unequally distributed", ["Firms pay everyone the same wage", "Governments prevent people from earning more", "Prices are set by planners"], "Markets reward factors according to their scarcity and productivity."),
         ("Which of the following countries has one of the highest Gini coefficients in the world?", "South Africa", ["Slovenia", "Norway", "Denmark"], "South Africa's Gini is around 0.63, among the highest measured."),
         ("Which of the following is a normative concept?", "Equity", ["Equality", "The Gini coefficient", "Median income"], "Whether a distribution is fair is a value judgement."),
         ("A Lorenz curve that moves further from the line of equality indicates which of the following?", "Greater inequality", ["Greater equality", "Higher average income", "Lower GDP"], "The larger the area between the curve and the line, the higher the Gini.")],
  why=[("Explain why markets may fail to achieve equity.", "Markets distribute income according to ownership of factors and their market value; people with little wealth, low skills, disabilities or caring responsibilities earn little, and inheritance concentrates wealth, so outcomes may be judged unfair."),
       ("Explain why equal outcomes may not be equitable.", "People differ in needs (e.g. disability, family size) and effort; giving everyone the same may be unfair to those with greater needs or who contribute more, so equity may require unequal treatment."),
       ("Explain why inequality of opportunity can perpetuate income inequality across generations.", "Children from poorer families have less access to good education, health and networks, so they earn less as adults; their children face the same disadvantages – low intergenerational mobility.")],
  contrast=[("equality", "equity", "Equality means equal shares; equity means fairness, which may involve unequal shares according to need or contribution. Equality can be measured; equity involves value judgements."),
            ("income", "wealth", "Income is a flow of money received over a period (wages, rent, interest, profit); wealth is a stock of assets owned at a point in time (property, shares, savings). Wealth is usually more unequally distributed than income.")],
  misc=[("A Gini coefficient of 0.25 shows more inequality than one of 0.45.", "A lower Gini indicates a more equal distribution: 0.25 (e.g. Slovakia or Slovenia) is more equal than 0.45 (e.g. the US is around 0.39-0.41)."),
        ("Equity means everyone should receive the same income.", "That describes equality of outcome; equity is about fairness, which most people believe allows some differences in income.")],
  apply=[("In a country the richest 10% of households receive 40% of income and the poorest 40% receive 15%. Calculate the Palma ratio and explain what it indicates.", "Palma = 40/15 = 2.67: the richest tenth receive 2.67 times the income share of the poorest 40%, indicating substantial inequality.", 2)],
  cases=[("inequality in Brazil", "Brazil's Gini coefficient was around 0.53 in 2022, among the highest in Latin America, despite falls since the early 2000s helped by the Bolsa Família cash-transfer programme.", "the market's inability to achieve equity", "Unequal access to land, education and capital produces highly unequal market incomes; government transfers reduced but did not remove inequality.")],
  sources=[("Hypothetical income shares by quintile in Country Z: poorest 20% receive 5%, next 20% receive 10%, middle 20% 15%, next 20% 22%, richest 20% 48%.", "Hypothetical data", "Using the data, calculate the ratio of the income share of the richest 20% to that of the poorest 20%, and explain what it suggests about equity.", "48/5 = 9.6: the richest fifth receive almost ten times the income of the poorest fifth; whether this is inequitable is normative, but such a large gap suggests that the market distribution may be judged unfair.")],
  evaluate=[("Income inequality is necessary for economic efficiency.", ["income differences provide incentives to work, train and take risks", "high rewards attract talent and entrepreneurship"], ["high inequality can reduce growth (lower human capital investment among the poor, political instability)", "Nordic countries combine low inequality with high productivity", "excessive inequality reduces social mobility"], "Some inequality provides incentives, but high inequality can harm efficiency and growth; the evidence suggests moderate inequality is compatible with strong performance.")],
  extended=[("Explain three reasons why market outcomes may be inequitable and discuss whether governments should aim for equality of outcome or equality of opportunity.", "Reasons: unequal ownership of factors/inheritance, differences in human capital and discrimination, market power and bargaining power, unequal access to education and health. Discussion: equality of opportunity preserves incentives but outcomes still unequal; equality of outcome may reduce incentives; most societies pursue both partly.", 8, 'long')],
  diag=[("how a Lorenz curve illustrates income inequality", "Diagram: cumulative % of population on the horizontal axis, cumulative % of income on the vertical; 45° line of perfect equality; Lorenz curve below it. The further the curve sags from the line, the greater the inequality; Gini = A/(A + B), where A is the area between the line and the curve and B the area under the curve.")])


@R.add('ch14-st1', 'C3', (1, 5), 'numerical')
def quintiles(rng, slot):
    for _ in range(50):
        q = sorted(rng.sample(range(3, 50), 5))
        if sum(q) == 100:
            break
        q[-1] += 100 - sum(q)
        if q[-1] > q[-2] and sum(q) == 100:
            break
    else:
        return None
    c = rng.choice(['Country A', 'Country B', 'Ruritania', 'an island economy', 'Country K'])
    ratio = q[4] / q[0]
    cum = [sum(q[:i + 1]) for i in range(5)]
    if slot.d <= 2:
        return dict(stem=f'In {c} the income shares of the five quintiles (poorest to richest) are {", ".join(str(x) + "%" for x in q)}. Calculate the ratio of the richest 20% share to the poorest 20% share.',
                    answer=r2(ratio), markingKey=f'{q[4]}/{q[0]} = {r2(ratio)}. [1] [1]', type='numerical', marks=2)
    return dict(stem=f'In {c} the income shares of the five quintiles (poorest to richest) are {", ".join(str(x) + "%" for x in q)}. Calculate the cumulative income shares needed to plot a Lorenz curve, and the share of income received by the poorest 60%. Explain what the data show about inequality.',
                answer=f'Cumulative: {", ".join(str(x) + "%" for x in cum)}; poorest 60% receive {cum[2]}%',
                markingKey=f'Cumulative shares {", ".join(map(str, cum))} [2]; poorest 60% = {cum[2]}% (vs 60% under perfect equality) [1]; richest quintile has {r2(ratio)} times the share of the poorest – the Lorenz curve lies below the line of equality [1].', type='numerical', marks=4)


S('ch14-st2',
  terms=[("progressive tax", "a tax for which the average tax rate rises as income rises, so higher-income earners pay a larger proportion of their income"),
         ("regressive tax", "a tax for which the average tax rate falls as income rises, such as many indirect taxes as a share of income"),
         ("proportional tax", "a tax for which the average tax rate is the same at all income levels (a flat tax)"),
         ("transfer payments", "payments from the government to individuals for which no good or service is provided in return, such as unemployment benefits and pensions"),
         ("marginal tax rate", "the tax rate paid on the last unit of income, ΔT/ΔY"),
         ("average tax rate", "total tax paid divided by total income")],
  facts=[("Which of the following is an example of a transfer payment?", "A state pension", ["A teacher's salary", "Government spending on roads", "Interest on government bonds paid to banks"], "Nothing is produced in return for the pension."),
         ("Why are indirect taxes such as VAT usually regressive?", "Low-income households spend a larger share of their income, so the tax takes a larger proportion of their income", ["They are charged at higher rates on the poor", "Rich people pay no VAT", "They are only charged on necessities"], "As a share of income, the burden falls as income rises."),
         ("Under a progressive income tax, what happens to the average tax rate as income rises?", "It rises", ["It falls", "It stays the same", "It becomes negative"], "Higher bands are taxed at higher marginal rates."),
         ("Which of the following policies aims to reduce inequality through direct provision?", "Free public education and healthcare", ["A cut in the top income tax rate", "A higher VAT rate", "A price floor for wheat"], "Universal provision gives everyone access regardless of income.")],
  why=[("Explain how a progressive income tax reduces income inequality.", "Higher-income earners pay a larger share of their income in tax, so post-tax incomes are more equal than pre-tax incomes; the revenue can fund transfers and services for lower-income households."),
       ("Explain why means-tested benefits may create a disincentive to work.", "If benefits are withdrawn as income rises, a person taking a job or working more hours may gain little extra income (a high effective marginal tax rate – the poverty trap), reducing the incentive to work."),
       ("Explain why direct provision of education can reduce inequality in the long run.", "Free education raises the human capital of children from low-income families, increasing their future earnings and social mobility, so inequality of opportunity and income falls over time.")],
  contrast=[("a progressive tax", "a regressive tax", "A progressive tax takes a larger proportion of income from higher earners (rising average rate); a regressive tax takes a larger proportion from lower earners (falling average rate)."),
            ("universal benefits", "means-tested benefits", "Universal benefits are paid to everyone in a group regardless of income (e.g. child benefit in some countries); means-tested benefits go only to those whose income or wealth is below a threshold, which targets help but can create disincentives.")],
  misc=[("A flat-rate income tax of 20% is progressive because people with higher incomes pay more money.", "Higher earners pay more money, but the same proportion of income, so a flat tax is proportional, not progressive."),
        ("Raising the minimum wage is the most targeted way to help the poorest households.", "Many of the poorest households have no one in work (pensioners, unemployed), so a minimum wage does not help them; transfers are better targeted.")],
  apply=[("Explain why a universal basic income would be more costly than means-tested benefits, and one potential advantage.", "It is paid to everyone regardless of income, so total spending is much higher; advantage: no poverty trap or stigma, simple to administer, protects against job insecurity.", 3)],
  cases=[("Brazil's Bolsa Família programme", "Launched in 2003, it pays monthly cash transfers to low-income families conditional on children attending school and receiving vaccinations; it reaches over 20 million families.", "conditional cash transfers to reduce inequity", "Transfers raise the incomes of the poorest immediately, while conditions build human capital and reduce future inequality."),
         ("Finland's basic income experiment (2017-2018)", "2,000 unemployed people received €560 a month with no conditions; recipients reported higher well-being and slightly more days in work.", "transfer payments as a response to inequity", "An unconditional transfer reduced insecurity without the disincentives of means-testing, though the employment effect was small.")],
  evaluate=[("Progressive income taxes are the most effective way to reduce income inequality.", ["directly reduce the gap in post-tax incomes", "raise revenue for transfers and services"], ["disincentives to work and invest at high rates", "tax avoidance and evasion, capital flight", "do not help people with no taxable income – transfers and services needed", "wealth inequality requires wealth/inheritance taxes"], "Progressive taxes are important but work best combined with transfers, public services and policies that raise opportunity."),
            ("Governments should use direct provision of services rather than cash transfers to reduce inequity.", ["ensures spending on merit goods such as health and education", "builds human capital and opportunity"], ["cash gives people choice and dignity", "transfers are quicker and cheaper to administer", "evidence from cash-transfer programmes shows positive outcomes"], "Both are needed: services address long-run opportunity, cash addresses immediate poverty.")],
  extended=[("Evaluate the effectiveness of minimum wages and transfer payments as policies to reduce inequity.", "Minimum wage: raises pay of low-paid workers, no direct fiscal cost, but may cause unemployment and does not reach non-workers; transfers: target the poorest, immediate effect, but fiscal cost and disincentives. Examples: Germany's €12 minimum wage, Bolsa Família.", 8, 'long')],
  diag=[("how a progressive income tax and transfer payments can reduce income inequality, using a Lorenz curve", "Diagram: line of equality and two Lorenz curves. The pre-tax (market income) curve lies further from the line of equality; after progressive taxes and transfers, the post-tax curve moves closer to the line, showing a lower Gini coefficient.")])


@R.add('ch14-st2', 'C3', (2, 5), 'numerical')
def tax_bands(rng, slot):
    b1 = rng.choice([10000, 12000, 15000])
    b2 = rng.choice([40000, 50000, 60000])
    r1, r2_, r3 = rng.choice([(0, 20, 40), (0, 15, 35), (5, 20, 45), (0, 25, 45)])
    inc = rng.choice([25000, 35000, 45000, 70000, 90000, 120000])
    if inc <= b1:
        return None
    t = b1 * r1 / 100 + (min(inc, b2) - b1) * r2_ / 100 + max(0, inc - b2) * r3 / 100
    avg = 100 * t / inc
    marg = r2_ if inc <= b2 else r3
    who = name(rng)
    return dict(stem=f'A country taxes income at {r1}% on the first ${b1:,}, {r2_}% on income from ${b1:,} to ${b2:,}, and {r3}% on income above ${b2:,}. {who} earns ${inc:,}. Calculate the tax paid, the average tax rate and the marginal tax rate, and state whether the system is progressive.',
                answer=f'Tax ${fmt(t, 6)}; average rate {r2(avg)}%; marginal rate {marg}%; progressive',
                markingKey=f'Tax = {b1:,}×{r1}% + {min(inc, b2) - b1:,}×{r2_}%' + (f' + {inc - b2:,}×{r3}%' if inc > b2 else '') + f' = {fmt(t, 6)} [2]; average = {fmt(t, 6)}/{inc:,} = {r2(avg)}% [1]; marginal = {marg}% [1]; average rate rises with income ⇒ progressive.', type='numerical', marks=4)


S('ch14-st3',
  terms=[("IA commentary", "a piece of internal assessment of up to 800 words analysing a news article using economic theory, diagrams and one of the nine key concepts"),
         ("key concept lens", "one of the nine IB Economics concepts (scarcity, choice, efficiency, equity, economic well-being, sustainability, change, interdependence, intervention) used to frame a commentary"),
         ("rubric requirements", "the IA rules on the portfolio, e.g. three commentaries on different units (excluding Unit 1), different key concepts, different sources, articles published no earlier than one year before the commentary is written"),
         ("evaluation (in a commentary)", "making supported judgements, for example weighing short- and long-run effects, stakeholders, assumptions and priorities of a policy described in the article"),
         ("real-world application", "linking economic theory explicitly to the specific facts and data in the chosen article")],
  facts=[("What is the maximum word count of each IA commentary?", "800 words", ["1,500 words", "500 words", "2,000 words"], "Each of the three commentaries is up to 800 words (excluding diagrams, labels, headings, footnotes and references)."),
         ("How many commentaries make up the IB Economics internal assessment portfolio?", "Three", ["Two", "Four", "One"], "Each based on a different unit of the syllabus (not the introductory unit)."),
         ("Which of the following is a rubric requirement for an IA article?", "It must be published no earlier than one year before the commentary is written", ["It must be from a textbook", "It must contain at least three diagrams", "It must be about the student's home country"], "Articles must be recent and from different sources."),
         ("Which assessment criterion rewards the use of a key concept in an IA commentary?", "The key concept criterion, which rewards effective and explicit use of the chosen concept", ["Diagrams", "Terminology only", "Rubric requirements only"], "Each commentary is framed by one of the nine key concepts.")],
  why=[("Explain why an IA commentary should focus on a small number of relevant diagrams.", "With only 800 words, one or two accurate, fully explained diagrams that are applied to the article's data show understanding better than many diagrams with little explanation."),
       ("Explain why evaluation is essential in a high-scoring commentary.", "The criteria reward judgements supported by evidence; examining stakeholders, short- and long-run effects, assumptions and alternatives shows critical thinking rather than description."),
       ("Explain why students should choose articles that contain economic data and a clear issue.", "A clear problem or policy (e.g. a new tax) lets the student apply theory and diagrams directly, use the data to support analysis and evaluate the policy, meeting the criteria efficiently.")],
  contrast=[("analysis", "evaluation", "Analysis explains cause and effect using theory and diagrams (e.g. how a tax shifts supply); evaluation weighs the significance of these effects and reaches a supported judgement (e.g. whether the tax is the best policy)."),
            ("describing an article", "applying economic theory to an article", "Description repeats what the article says; application uses economic concepts, diagrams and terminology to explain why the events happened and their consequences.")],
  misc=[("A good commentary summarises the article in detail before applying any theory.", "A brief introduction to the issue is enough; marks come from applying theory, diagrams, terminology, the key concept and evaluation, not from summary."),
        ("All three IA commentaries can be on the same unit if they use different articles.", "Rubric requirements say each commentary must be based on a different unit of the syllabus (excluding Unit 1) and use a different key concept and source.")],
  apply=[("A student chooses an article about Kenya raising the excise duty on fuel. Identify an appropriate diagram and key concept for a commentary.", "Diagram: specific tax shifting supply up (S to S + tax), with inelastic demand showing consumer burden and revenue (or a negative externality diagram); key concept: intervention (or sustainability/equity).", 2),
         ("Suggest two evaluative points a student could make in a commentary about a city introducing a congestion charge.", "e.g. effectiveness depends on PED for driving and availability of public transport; impact on low-income drivers (equity); revenue use; short- vs long-run effects; enforcement costs.", 3)],
  cases=[("an article about Singapore's Certificate of Entitlement (COE) car quotas", "Singapore limits the number of cars through COE auctions; COE prices exceeded S$100,000 in 2023.", "applying a key concept such as intervention in an IA commentary", "The quota can be analysed with a vertical supply curve for COEs, linking to negative externalities of congestion and evaluating equity effects.")],
  sources=[("'The government of Malaysia announced it would remove the blanket subsidy on diesel in Peninsular Malaysia from June 2024, raising the pump price by about 56%. Targeted cash aid will be given to eligible small businesses and farmers.'", "Example news extract for an IA commentary", "Outline how a student could use this article for a commentary, naming a diagram and a key concept.", "Diagram: removal of a subsidy (supply shifts up from S − subsidy to S), price rises and quantity falls; key concept: intervention or equity; evaluate effects on consumers, firms, government budget and the environment, and the targeted aid.")],
  evaluate=[("Using one key concept as a lens strengthens the analysis in an IA commentary.", ["gives the commentary a clear focus", "links micro events to broader economic ideas", "rewarded explicitly in the criteria"], ["forcing a concept can seem artificial", "some articles relate to several concepts", "the concept must be used throughout, not just named"], "A well-chosen concept, used consistently in analysis and evaluation, strengthens the commentary; a superficially named concept does not.")],
  extended=[("Outline the structure of a strong microeconomics IA commentary on an article about a new sugar tax, including the diagram, key concept and evaluation.", "Brief context; define key terms; diagram of a specific tax (or negative consumption externality with tax) applied to article data; explanation of effects on price, quantity, revenue; key concept (intervention/economic well-being) throughout; evaluation: PED, regressive effects, reformulation, alternatives (education, regulation), stakeholders; conclusion.", 6)],
  diag=[("how a student could apply a negative externality diagram to an article about a new tax on single-use plastic bags", "Diagram: market for plastic bags; MPB above MSB (negative consumption externality: litter, marine pollution); MPC = MSC. Market quantity Qm exceeds Q*; welfare loss shown. The tax raises the price paid, reducing quantity towards Q*; article data (e.g. bag use fell by 90% after England's 5p charge in 2015) can be referenced, and the key concept of sustainability applied.")])

A('ch14-st3',
  ("A student's article reports that a drought has raised the price of rice in Bangladesh by 30%. Suggest a suitable diagram and explain how the student could use data from the article in the commentary.", "Supply shifts left with inelastic demand and supply, showing a large price rise; label the diagram with the article's figures (30% price rise) and explain why PED and PES for rice are low; possibly extend to government responses (price ceilings, buffer stocks).", 3),
  ("Explain why a commentary that defines terms such as 'specific tax' and 'incidence' scores more highly on the terminology criterion than one that uses them without definition.", "The terminology criterion rewards relevant economic terms used appropriately throughout; defining key terms shows precise understanding and lets the reader follow the analysis.", 2),
  ("A student wants to write a microeconomics commentary on a news article about a city's new minimum wage. Identify two stakeholders and one evaluative point the student could discuss.", "Stakeholders: low-paid workers, employers (e.g. small restaurants), consumers, government; evaluative point: effect on employment depends on the elasticity of demand for labour; possible higher prices; short- vs long-run effects.", 3),
  ("Explain why a diagram in an IA commentary should be labelled with information from the article rather than generic labels only.", "Applying the diagram to the specific market (e.g. 'market for diesel in Malaysia', actual prices) shows real-world application and links theory to the article, which the application and analysis criterion rewards.", 2))
C('ch14-st3',
  ("an article about England's 5p plastic bag charge (2015)", "Single-use bag sales by major supermarkets fell by over 95% within a few years of the charge.", "how real-world data can support evaluation in a commentary", "The data show a large behavioural response despite a small charge, suggesting framing/behavioural effects; a student can use this to evaluate the effectiveness of the policy."),
  ("an article about Indonesia's ban on palm oil exports in April 2022", "Indonesia briefly banned exports of palm oil to lower domestic cooking-oil prices, causing world prices to rise.", "selecting an article with a clear policy for a microeconomics commentary", "The article provides a clear intervention, effects on several stakeholders (domestic consumers, farmers, importing countries) and data, allowing diagrams, a key concept (intervention or interdependence) and evaluation."))
X('ch14-st3', ("'A city council in Bogotá has introduced a weekday charge for private cars that want to be exempt from the pico y placa driving restrictions. Officials say the revenue will fund public transport.'", "Example news extract for an IA commentary", "Explain how a student could evaluate this policy in a commentary.", "Discuss effectiveness (PED for driving, availability of public transport), equity (wealthier drivers can pay to drive), use of revenue (public transport improves positive externalities), short- vs long-run effects, comparisons with London's congestion charge; reach a supported judgement."))
E('ch14-st1', ("Market economies cannot achieve equity without government intervention.", ["markets reward ownership of factors, which is unequal", "inheritance and discrimination persist", "evidence: high pre-tax Gini coefficients in most countries"], ["charities and community organisations redistribute voluntarily", "economic growth can raise the incomes of the poor (absolute poverty falls)", "competition and education can increase mobility"], "Some redistribution through government is needed for equity in practice, though growth, education and voluntary action also matter."))
E('ch14-st3', ("A commentary that uses a single well-explained diagram is better than one that uses several diagrams.", ["limited word count makes full explanation of many diagrams difficult", "depth of application is rewarded"], ["some issues need two diagrams (e.g. a tax and its effect on a related market)", "criteria reward relevant, accurate diagrams, not a fixed number"], "Quality and relevance matter more than quantity: one or two fully explained, applied diagrams are usually best."))

# ---------------------------------------------------------------------------------------------
# Additional evaluation claims (Paper 1(b) / Paper 2 / Paper 3 material)
# ---------------------------------------------------------------------------------------------
E('ch01-st4', ("The ideas of Adam Smith are more relevant to modern economies than those of Keynes.", ["markets and the price mechanism allocate most resources efficiently", "division of labour and specialisation underpin global supply chains", "competition drives innovation"], ["the 2008 crisis and 2020 pandemic showed the need for active fiscal policy (Keynes)", "market failures require intervention", "modern economies are mixed, drawing on both"], "Both remain relevant: Smith explains how markets coordinate activity, Keynes why governments must stabilise demand; modern mixed economies use both sets of ideas."))
E('ch04-st2', ("Advertising is the most effective way for firms to increase the demand for their products.", ["shifts demand right by changing tastes and awareness", "builds brand loyalty, making demand less price elastic"], ["income and the prices of substitutes have larger effects", "advertising is costly and its effects can be short-lived", "product quality, innovation and word of mouth matter more for many goods"], "Advertising can shift demand, especially for differentiated consumer goods, but its effectiveness is limited compared with income and quality changes."))
E('ch04-st3', ("The income effect is more important than the substitution effect in explaining the law of demand.", ["for goods taking a large share of income (housing, rice for the poor) real income changes are large"], ["for most goods the share of income is small, so the income effect is tiny", "the substitution effect always works in the direction of the law of demand", "for inferior goods the income effect works against the law of demand"], "For most goods the substitution effect dominates; the income effect matters mainly for goods that take a large share of the budget."))
E('ch04-st4', ("Firms should rely on estimated demand functions when setting prices.", ["give clear predictions of sales at different prices", "allow calculation of revenue-maximising prices"], ["estimates may be inaccurate or outdated", "rivals' reactions are not included", "non-price factors change"], "Demand functions are a useful guide but should be combined with market testing and judgement about rivals and changing conditions."))
E('ch05-st1', ("Higher prices always lead to higher output in the long run.", ["profits attract new firms and investment", "supply becomes more elastic over time"], ["natural limits (land, minerals)", "regulation or quotas restrict output", "if high prices are expected to be temporary firms may not invest"], "In most markets higher sustained prices raise long-run output, but physical, legal and expectation constraints can limit the response."))
E('ch05-st2', ("Indirect taxes on producers are always passed on in full to consumers.", ["firms raise prices to cover higher costs", "true when demand is perfectly inelastic"], ["the incidence depends on PED and PES", "with elastic demand producers absorb most of the tax", "competition limits price rises"], "Taxes are usually shared; the more inelastic demand is relative to supply, the more is passed to consumers."))
E('ch05-st3', ("Linear supply functions are a reliable way for governments to predict the effects of a tax.", ["give clear numerical estimates of price and quantity changes", "show how incidence depends on the slopes"], ["real supply curves are not linear", "firms' costs and technology change", "estimates are uncertain"], "Linear functions give useful approximations, especially for small changes, but predictions should be checked against evidence."))
E('ch06-st1', ("Shortages are always a sign that a market is failing.", ["persistent shortages show the price mechanism is not working", "may be caused by price controls"], ["temporary shortages occur as markets adjust to new equilibria", "firms may deliberately price below equilibrium (concerts) for reputation", "supply shocks take time to resolve"], "Persistent shortages suggest market or government failure, but temporary shortages are part of normal market adjustment."))
E('ch06-st2', ("Governments should intervene whenever a supply shock causes a large rise in the price of a necessity.", ["protects low-income households", "prevents hardship and social unrest"], ["price signals encourage more supply and less waste", "intervention (price ceilings) may cause shortages", "targeted transfers may be better than general controls"], "Intervention can be justified for necessities, but targeted support is generally better than measures that blunt the price signal."))
E('ch06-st3', ("The price mechanism allocates resources fairly.", ["prices reflect what people are willing to pay", "voluntary exchange benefits both sides"], ["willingness to pay depends on income, which is unequal", "necessities may be unaffordable for the poor", "market power and externalities distort prices"], "The price mechanism is efficient in many markets but not necessarily fair; equity requires additional policies."))
E('ch06-st4', ("Consumer surplus is a useful measure of the benefit consumers gain from a market.", ["measures willingness to pay above price", "helps evaluate policies such as taxes and price controls"], ["willingness to pay depends on income", "hard to measure demand curves accurately", "ignores external benefits and behavioural biases"], "Consumer surplus is a valuable conceptual measure for policy evaluation, but it must be used with caution because it depends on ability to pay and estimates of demand."))
E('ch06-st5', ("Algebraic calculation of equilibrium is more useful than diagrams in economic analysis.", ["precise numerical answers", "allows calculation of revenue, surplus and tax effects"], ["diagrams show relationships and direction of change clearly", "algebra depends on knowing the functions, which are estimates", "both are needed to communicate analysis"], "Algebra and diagrams complement each other: algebra quantifies effects, diagrams explain them."))
E('ch07-st1', ("Consumers generally act in their own best interests.", ["people know their own preferences best", "markets respond to consumer choices"], ["biases such as present bias and anchoring cause systematic mistakes", "imperfect information and complexity (pensions, insurance)", "addiction and habits"], "Consumers often act in their own interest, but systematic biases and information problems mean they sometimes do not, which justifies some policy responses."))
E('ch07-st2', ("Governments should use insights from behavioural economics to design policy.", ["low-cost nudges with significant effects (auto-enrolment, tax letters)", "policies better matched to how people actually behave"], ["risk of manipulation and paternalism", "effects may be small or fade", "governments also have biases"], "Behavioural insights improve policy design, but they should be transparent, tested and combined with traditional tools."))
E('ch07-st3', ("Nudges are an unacceptable form of manipulation by the government.", ["they work by exploiting biases rather than reasoning", "people may not be aware they are being influenced", "the government decides what is 'good'"], ["choice is preserved – people can opt out", "every choice has an architecture; neutral design is impossible", "transparent nudges can be publicly debated"], "Nudges are acceptable when transparent, easy to avoid and in line with people's own goals; hidden or self-serving nudges are not."))
E('ch07-st4', ("Corporate social responsibility is just a marketing strategy.", ["CSR is often used to improve brand image", "'greenwashing' cases (e.g. misleading environmental claims)"], ["some firms make genuine changes (Patagonia, B-Corps)", "investors and regulation increasingly require ESG reporting", "CSR can reduce costs and risks"], "CSR is sometimes mainly marketing, but there is evidence of real changes; its value depends on transparency and verification."))
E('ch08-st1', ("Price elasticity of demand values are of little practical use because they change over time.", ["PED changes with time, income and tastes", "estimates are uncertain"], ["estimates guide tax and pricing decisions", "elasticities for many goods are fairly stable", "can be re-estimated with new data"], "PED values must be updated, but they remain essential for pricing and tax policy."))
E('ch08-st2', ("Brand loyalty is the most effective way for a firm to reduce the price elasticity of demand for its product.", ["loyal customers do not switch to substitutes", "allows higher prices without large falls in sales"], ["building loyalty requires large advertising spending", "competitors can innovate and win customers", "low share of income or addictiveness also reduce PED"], "Brand loyalty can reduce PED significantly, but it is costly to build and may erode; product differentiation and innovation also matter."))
E('ch08-st3', ("Knowledge of PED is more useful to governments than to firms.", ["guides choice of goods for indirect taxes and predicts revenue", "helps assess the effect of taxes on consumption of demerit goods"], ["firms use PED for pricing and revenue decisions daily", "PED helps firms with price discrimination"], "PED is essential to both: governments use it for tax design and firms for pricing; neither can do without it."))
E('ch08-st4', ("Income elasticity of demand (YED) is the most useful elasticity concept for firms planning future production.", ["predicts how demand will change as incomes grow or fall", "helps firms plan for recessions and booms"], ["PED is more relevant for pricing decisions", "income forecasts are uncertain", "tastes and technology can change demand more than income"], "YED is very useful for long-term planning, but must be combined with PED and analysis of tastes and competition."))
E('ch09-st1', ("Increasing PES is the best way to reduce the price of housing.", ["more elastic supply means demand increases raise quantity rather than price", "planning reform and land release raise PES"], ["housing supply responds slowly even with reform", "demand-side factors (interest rates, investors) also drive prices", "environmental and community objections"], "Raising PES is essential for long-term affordability, but needs to be combined with demand-side measures."))
E('ch09-st3', ("Countries that depend on primary commodity exports should diversify into manufacturing.", ["reduces exposure to volatile commodity prices", "manufacturing has higher YED and PES", "creates more jobs and skills"], ["comparative advantage may lie in commodities", "diversification takes time and investment", "some commodities have strong future demand (energy transition minerals)"], "Diversification reduces risk and supports development, but it should build on existing strengths and be pursued gradually."))
E('ch10-st1', ("Governments intervene in markets mainly to raise revenue.", ["indirect taxes raise large sums (VAT, fuel duty)"], ["many interventions aim to correct market failure (carbon taxes, subsidies for vaccines)", "equity motives (minimum wages, price controls)", "supporting firms and strategic industries"], "Revenue is one motive, but correcting market failure, equity and supporting producers are equally important reasons."))
E('ch10-st4', ("Calculating the effects of intervention on stakeholders is essential for good policy-making.", ["shows who gains and loses and by how much", "allows comparison of alternative policies", "reveals welfare loss and fiscal cost"], ["calculations rely on estimated functions", "some effects (health, environment) are hard to quantify", "political and equity judgements are still needed"], "Quantifying stakeholder effects improves policy decisions, but must be combined with judgement about unquantifiable and distributional effects."))
E('ch11-st1', ("Market failure is so common that governments should intervene in most markets.", ["externalities are widespread (energy, transport, food)", "information problems in health, finance"], ["many markets work well without intervention", "government failure is also common", "intervention has administrative costs"], "Market failure justifies targeted intervention where it is significant, not intervention in all markets."))
E('ch12-st3', ("Breaking up large technology firms is the best way to deal with their market power.", ["restores competition and reduces abuse of dominance", "prevents use of data advantages to exclude rivals"], ["network effects mean a single platform may be efficient", "break-ups are slow and costly", "regulation (EU Digital Markets Act) may be more effective"], "Break-ups may be justified in extreme cases, but regulation of conduct is often a more practical first step."))
E('ch13-st1', ("Firms should always aim to grow to benefit from economies of scale.", ["lower average costs and prices", "greater market power and financial strength"], ["diseconomies of scale beyond the minimum efficient scale", "growth may reduce flexibility", "demand may be too small for large scale"], "Growth is beneficial up to the minimum efficient scale; beyond that diseconomies and market size limit its benefits."))
E('ch13-st2', ("The model of perfect competition has no relevance to real-world markets.", ["assumptions (perfect information, identical products) rarely hold"], ["some markets come close (agriculture, foreign exchange)", "provides an efficiency benchmark for policy", "explains entry and exit and competitive pressure"], "Perfect competition is rarely observed exactly, but it remains a useful benchmark and approximates some markets."))
E('ch13-st3', ("Natural monopolies should be owned by the government.", ["avoids exploitation of consumers", "can price for social objectives and invest in infrastructure"], ["state firms may be inefficient (lack of profit incentive)", "regulated private firms can be efficient (price caps)", "fiscal costs"], "Either public ownership or regulated private ownership can work; the choice depends on governance quality and regulatory capacity."))
